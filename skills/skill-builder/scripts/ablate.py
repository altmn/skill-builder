#!/usr/bin/env python3
"""Prepare blinded artifact pairs and account for independent preferences offline.

No model calls, automatic grader, installation or target execution. Keep key.json
private from the judge; hashes bind evidence but do not establish reviewer truth.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import random

spec = importlib.util.spec_from_file_location("ablation_evaluation", Path(__file__).absolute().parent / "evaluate.py")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)
require = evaluation.require
MAX_ARTIFACTS = 4096
MAX_COPY_BYTES = 128 * 1024 * 1024


def blind(plan_path, observation_path, output, conditions=()):
    plan, observations = evaluation.read_json(plan_path), evaluation.read_json(observation_path)
    root = Path(observation_path).absolute().parent
    plan_raw = evaluation.builder.bounded_read(Path(plan_path), 16 * 1024 * 1024)
    summary = evaluation.summarize(plan, observations, root, evaluation.builder.sha256(plan_raw))
    selected = list(conditions) if conditions else list(plan.get("variants", {}))
    require(selected and len(selected) == len(set(selected))
            and set(selected) <= (set(plan.get("variants", {})) | {"no_skill", "previous"})
            and set(selected) <= set(plan["execution_conditions"]), "Select frozen variants, no_skill or previous comparisons.")
    unscored = {tuple(row["key"]) for row in summary["unscored"]}
    rows = {(r["case_id"], r["condition"], r["trial"]): r for r in observations["runs"]
            if r["suite"] == "execution" and r["status"] == "completed" and r["isolation_verified"]
            and (r["suite"], r["case_id"], r["condition"], r["trial"]) not in unscored}
    pairs = []
    for (case, condition, trial), row in sorted(rows.items()):
        if condition not in selected or (case, "explicit", trial) not in rows:
            continue
        sides = [(condition, row), ("explicit", rows[(case, "explicit", trial)])]
        random.SystemRandom().shuffle(sides)
        pairs.append((case, trial, sides))
    require(0 < len(pairs) <= 512, "Need one to 512 matched completed variant/explicit pairs.")
    references = [reference for _, _, sides in pairs for _, row in sides for reference in row["artifacts"]]
    require(len(references) <= MAX_ARTIFACTS, "Blinded export exceeds its artifact-count budget.")
    total = 0
    for reference in references:
        total += len(evaluation.evidence(root, reference))
        require(total <= MAX_COPY_BYTES, "Blinded export exceeds its aggregate byte budget.")
    destination = evaluation.builder.checked_destination(output)
    public, private = [], []
    with evaluation.builder.NewTree(destination) as tree:
        for i, (case, trial, sides) in enumerate(pairs, 1):
            pair_id = f"P{i:04d}"
            visible = {"id": pair_id, "case_id": case, "trial": trial}
            hidden = {"id": pair_id, "case_id": case, "trial": trial}
            for side, (condition, row) in zip(("left", "right"), sides):
                visible[side] = []
                hidden[side] = condition
                for index, reference in enumerate(row["artifacts"]):
                    raw = evaluation.evidence(root, reference)
                    path = f"{pair_id}/{side}/{index}.txt"
                    tree.write(path, raw)
                    visible[side].append({"path": path, "sha256": evaluation.builder.sha256(raw)})
            variant = next(c for c, _ in sides if c != "explicit")
            hidden["comparison"] = variant + "_vs_explicit"
            snapshot = plan["identities"].get("previous") if variant == "previous" else plan.get("variants", {}).get(variant)
            hidden["identical_payloads"] = bool(snapshot and snapshot["payload_sha256"] == plan["identities"]["candidate"]["payload_sha256"])
            public.append(visible)
            private.append(hidden)
        public_raw = evaluation.builder.json_bytes({"schema_version": "1.0.0", "pairs": public})
        tree.write("pairs.json", public_raw)
        key = {"schema_version": "1.0.0", "record_type": "skill-builder-blind-key",
               "plan_sha256": evaluation.builder.sha256(plan_raw),
               "observations_sha256": evaluation.builder.sha256(evaluation.builder.bounded_read(Path(observation_path), 16 * 1024 * 1024)),
               "pairs_sha256": evaluation.builder.sha256(public_raw), "panel_outcome": summary["outcome"],
               "invariant_failures": summary["observed_invariant_failures"], "pairs": private}
        key_raw = evaluation.builder.json_bytes(key)
        tree.write("key.json", key_raw)
        tree.write("judgments.json.template", evaluation.builder.json_bytes({
            "key_sha256": evaluation.builder.sha256(key_raw), "grader": "REPLACE: independent reviewer/version",
            "calibration": {"path": "REPLACE: redacted calibration record", "sha256": "REPLACE: digest"},
            "judgments": [{"id": p["id"], "preference": "unknown", "evidence": "REPLACE: rubric-based annotation"} for p in public]}))
    return {"outcome": "prepared", "pairs": len(public), "panel_outcome": summary["outcome"],
            "limit": "Give the judge only pairs.json, copied artifacts and the frozen rubric. Inspect identifying text in artifacts. Keep key.json and the final binding step outside judging."}


def score(key_path, judgments_path):
    key, record = evaluation.read_json(key_path), evaluation.read_json(judgments_path)
    require(isinstance(key, dict) and key.get("record_type") == "skill-builder-blind-key"
            and key.get("panel_outcome") in {"completed", "incomplete", "failed"}, "Invalid blind key.")
    require(isinstance(record, dict) and record.get("key_sha256") == evaluation.builder.sha256(
            evaluation.builder.bounded_read(Path(key_path), 16 * 1024 * 1024)), "Judgments identify another blind key.")
    require(isinstance(record.get("grader"), str) and record["grader"].strip()
            and "REPLACE:" not in record["grader"], "Identify the independent calibrated grader.")
    evaluation.evidence(Path(judgments_path).absolute().parent, record.get("calibration"))
    pairs = key.get("pairs")
    require(isinstance(pairs, list) and pairs and all(isinstance(p, dict) and isinstance(p.get("id"), str) for p in pairs), "Invalid pair index.")
    expected = {p["id"]: p for p in pairs}
    require(len(expected) == len(pairs), "Duplicate pair IDs.")
    public = evaluation.builder.parse_json(evaluation.evidence(Path(key_path).absolute().parent,
        {"path": "pairs.json", "sha256": key.get("pairs_sha256")}))
    require(isinstance(public, dict) and isinstance(public.get("pairs"), list)
            and all(isinstance(p, dict) for p in public["pairs"])
            and [p.get("id") for p in public["pairs"]] == [p["id"] for p in pairs], "Public/private pair index mismatch.")
    for pair in public["pairs"]:
        for side in ("left", "right"):
            require(isinstance(pair.get(side), list) and pair[side], "Missing blinded artifacts.")
            for reference in pair[side]:
                evaluation.evidence(Path(key_path).absolute().parent, reference)
    judgments = record.get("judgments")
    require(isinstance(judgments, list), "Judgments must be an array.")
    seen, groups, unknown = set(), {}, []
    for row in judgments:
        require(isinstance(row, dict) and row.get("id") in expected and row["id"] not in seen, "Unexpected/duplicate judgment.")
        seen.add(row["id"])
        choice = row.get("preference")
        require(choice in {"left", "right", "tie", "unknown"} and isinstance(row.get("evidence"), str)
                and row["evidence"].strip() and "REPLACE:" not in row["evidence"], "Each preference needs independent annotation.")
        pair = expected[row["id"]]
        require(type(pair.get("identical_payloads")) is bool and isinstance(pair.get("comparison"), str)
                and len(set((pair.get("left"), pair.get("right")))) == 2
                and "explicit" in (pair.get("left"), pair.get("right")), "Invalid private pairing.")
        counts = groups.setdefault(pair["comparison"], {"variant_wins": 0, "explicit_wins": 0, "ties": 0,
                                                       "unknown": 0, "identical_payload_pairs": 0})
        counts["identical_payload_pairs"] += int(pair["identical_payloads"])
        if choice == "unknown":
            counts["unknown"] += 1
            unknown.append(row["id"])
        elif choice == "tie":
            counts["ties"] += 1
        else:
            counts["explicit_wins" if pair[choice] == "explicit" else "variant_wins"] += 1
    missing = sorted(set(expected) - seen)
    return {"outcome": "failed" if key["panel_outcome"] == "failed" else
            "incomplete" if missing or unknown or key["panel_outcome"] == "incomplete" else "completed",
            "comparisons": groups, "missing": missing, "unknown": unknown,
            "invariant_failures": key.get("invariant_failures", []),
            "limit": "Descriptive preferences only. Identical-payload pairs estimate ordinary variation; no confidence interval, causal savings or release approval is inferred."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("blind", help="Copy matched variant/explicit artifacts under randomized neutral names.")
    prep.add_argument("--plan", required=True)
    prep.add_argument("--observations", required=True)
    prep.add_argument("--output", required=True)
    prep.add_argument("--condition", action="append", default=[], help="Named frozen variant, no_skill or previous; repeat. Default: all named variants.")
    report = sub.add_parser("score", help="Account for independently annotated blinded preferences.")
    report.add_argument("--key", required=True)
    report.add_argument("--judgments", required=True)
    args = parser.parse_args()
    try:
        result = blind(args.plan, args.observations, args.output, args.condition) if args.command == "blind" else score(args.key, args.judgments)
        print(json.dumps(result, indent=2))
        return {"failed": 1, "incomplete": 3}.get(result["outcome"], 0)
    except (ValueError, OSError, KeyError, TypeError):
        print(json.dumps({"outcome": "blocked", "error": "Invalid, incomplete, mismatched or escaping ablation evidence; inspect the protocol."}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
