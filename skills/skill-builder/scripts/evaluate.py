#!/usr/bin/env python3
"""Prepare frozen panels and summarize independently collected observations.

Offline and standard-library only. Does not run an agent, install a skill,
execute a target or grader, or infer activation from an answer's wording.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import re
import statistics
import stat
import sys

SKILL_ROOT = Path(__file__).absolute().parents[1]


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


builder = load(SKILL_ROOT / "scripts/skill_builder.py", "evaluation_builder")
METRICS = ("latency_seconds", "input_tokens", "output_tokens", "cost_usd")
COUNTERS = ("tool_calls", "tool_errors", "activated_context_tokens")
METRICS += COUNTERS


def require(condition, message):
    if not condition:
        raise ValueError(message)


def measurement(value):
    if value is None:
        return True
    if type(value) not in (int, float) or value < 0:
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False  # JSON integers may exceed the finite reporting range.


def checked_path(path, *, boundary=None, directory=False):
    """Point-in-time containment checks, not an OS sandbox."""
    requested = Path(path).absolute()
    for component in reversed((requested, *requested.parents)):
        mode = component.lstat().st_mode
        require(not stat.S_ISLNK(mode), "Symlink paths and ancestors are refused.")
        if component != requested:
            require(stat.S_ISDIR(mode), "Path ancestor must be a directory.")
    require((stat.S_ISDIR if directory else stat.S_ISREG)(requested.lstat().st_mode),
            "Expected a directory." if directory else "Expected a regular file.")
    resolved = requested.resolve(strict=True)
    if boundary is not None:
        require(resolved.is_relative_to(checked_path(boundary, directory=True)), "Path escapes its declared root.")
    return resolved


def read_json(path):
    checked_path(path)
    return builder.parse_json(builder.bounded_read(Path(path), 16 * 1024 * 1024))


def identity(root):
    root = checked_path(root, directory=True)
    inventory = builder.inspect_tree(root, 4096, 128 * 1024 * 1024, 128 * 1024 * 1024)
    require(inventory["coverage"] == "complete_within_declared_exclusions",
            "Snapshot identity is incomplete; inspect file/entry/byte limits or refused files.")
    entries = []
    for row in inventory["files"]:
        require(row["kind"] == "regular_file" and row["status"] == "hashed", "Snapshot contains an unsupported file.")
        entries.append({"path": row["path"], "size_bytes": row["size_bytes"], "sha256": row["sha256"]})
    entries.sort(key=lambda e: e["path"])
    entry = next((e for e in entries if e["path"] == "SKILL.md"), None)
    require(entry is not None, "Snapshot needs SKILL.md at its root.")
    canonical = (json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return {"payload_sha256": builder.sha256(canonical),
            "skill_sha256": entry["sha256"], "files": entries,
            "excluded_directories": sorted(builder.EXCLUDED_DIRS)}


def validate_corpus(corpus):
    require(isinstance(corpus, dict) and set(corpus) == {"routing", "execution"}, "Invalid corpus.")
    ids = set()
    for kind, cases in corpus.items():
        require(isinstance(cases, list) and cases, "Each suite must have cases.")
        for case in cases:
            require(isinstance(case, dict) and isinstance(case.get("id"), str)
                    and case["id"] and case["id"] not in ids, "Case IDs must be unique.")
            ids.add(case["id"])
            require(case.get("split") in {"development", "validation"}
                    and isinstance(case.get("prompt"), str) and case["prompt"].strip(), "Invalid case prompt/split.")
            require("REPLACE:" not in json.dumps(case),
                    "Replace scaffold prompts/rationales with target-specific cases before preparation.")
            if kind == "routing":
                require(type(case.get("should_trigger")) is bool, "Routing labels must be Boolean.")
            else:
                for field in ("checks", "invariants"):
                    values = case.get(field)
                    require(isinstance(values, list) and values and all(isinstance(v, str) and v for v in values)
                            and len(set(values)) == len(values), "Execution cases need check/invariant IDs.")
                require(not set(case["checks"]) & set(case["invariants"]), "Check IDs overlap.")
                if "trajectory" in case:
                    validate_trajectory(case["trajectory"])
    return corpus


def validate_trajectory(rules):
    require(isinstance(rules, dict) and set(rules) == {"required", "forbidden", "before"}, "Invalid trajectory contract.")
    for field in ("required", "forbidden"):
        values = rules[field]
        require(isinstance(values, list) and all(isinstance(v, str) and v.strip() for v in values)
                and len(values) == len(set(values)), "Trajectory action IDs must be unique nonempty strings.")
    require(not set(rules["required"]) & set(rules["forbidden"]), "Required and forbidden actions overlap.")
    require(isinstance(rules["before"], list) and all(isinstance(p, list) and len(p) == 2
            and all(isinstance(v, str) and v.strip() for v in p) and p[0] != p[1]
            for p in rules["before"]), "Ordering rules need two distinct action IDs.")


def trajectory(trace, rules):
    """Grade adapter-observed actions, never hidden reasoning or answer claims."""
    validate_trajectory(rules)
    require(isinstance(trace, dict) and type(trace.get("complete")) is bool
            and isinstance(trace.get("events"), list), "Invalid trajectory trace.")
    actions, completed = [], {}
    for i, event in enumerate(trace["events"]):
        require(isinstance(event, dict), "Invalid trace event.")
        if event.get("kind") != "action":
            continue
        require(isinstance(event.get("name"), str) and event["name"].strip()
                and event.get("outcome") in {"succeeded", "failed", "denied"}, "Invalid observed action.")
        actions.append(event["name"])
        if event["outcome"] == "succeeded":
            completed.setdefault(event["name"], []).append(i)
    forbidden = sorted(set(actions) & set(rules["forbidden"]))
    missing = [name for name in rules["required"] if name not in completed]
    ordering = [pair for pair in rules["before"] if pair[1] in completed
                and (pair[0] not in completed or min(completed[pair[1]]) <= min(completed[pair[0]]))]
    return {"outcome": "failed" if forbidden or trace["complete"] and (missing or ordering)
            else "passed" if trace["complete"] else "inconclusive",
            "forbidden_observed": forbidden, "missing_required": missing if trace["complete"] else None,
            "ordering_violations": ordering if trace["complete"] else None}


def prepare(candidate, previous, environment, trials, split, case_ids=(), *,
            routing_cases=None, execution_cases=None, fixtures_root=None, default_cases_root=None, variants=None):
    require(type(trials) is int and 1 <= trials <= 20, "Trials must be 1–20.")
    custom = (routing_cases, execution_cases, fixtures_root)
    require(all(custom) or not any(custom), "Supply --routing-cases, --execution-cases and --fixtures-root together.")
    if all(custom):
        sources = {"routing": Path(routing_cases), "execution": Path(execution_cases)}
        fixture_root = checked_path(fixtures_root, directory=True)
    else:
        require(default_cases_root is not None, "Installed evaluator requires target-specific case files and fixture root.")
        fixture_root = checked_path(default_cases_root, directory=True)
        sources = {kind: fixture_root / (kind + ".json") for kind in ("routing", "execution")}
    for path in sources.values():
        checked_path(path)
    source_bytes = {kind: builder.bounded_read(path, 16 * 1024 * 1024) for kind, path in sources.items()}
    corpus = validate_corpus({kind: builder.parse_json(raw) for kind, raw in source_bytes.items()})
    source_identities = {kind: {"filename": path.name, "sha256": builder.sha256(source_bytes[kind])}
                         for kind, path in sources.items()}
    if split != "all":
        corpus = {kind: [c for c in cases if c["split"] == split] for kind, cases in corpus.items()}
    if case_ids:
        require(set(case_ids) <= {c["id"] for cases in corpus.values() for c in cases}, "Unknown case or case outside selected split.")
        corpus = {kind: [c for c in cases if c["id"] in case_ids] for kind, cases in corpus.items()}
    validate_corpus(corpus)
    environment = read_json(environment)
    require("REPLACE:" not in json.dumps(environment), "Replace environment scaffold values before preparation.")
    require(isinstance(environment, dict) and all(environment.get(k) for k in
            ("host", "model", "settings", "policy", "catalog_sha256", "budget")), "Freeze the required environment fields.")
    require(isinstance(environment["catalog_sha256"], str) and
            len(environment["catalog_sha256"]) == 64 and all(c in "0123456789abcdef" for c in environment["catalog_sha256"]), "Invalid catalog digest.")
    budget = environment["budget"]
    require(isinstance(budget, dict) and type(budget.get("max_runs")) is int
            and type(budget.get("semantic_retries")) is int and budget["semantic_retries"] == 0
            and type(budget.get("per_run_seconds")) is int and budget["per_run_seconds"] > 0,
            "Declare max_runs, positive per_run_seconds, and zero semantic_retries.")
    snapshots = {"candidate": identity(candidate), "previous": identity(previous) if previous else None}
    variant_snapshots = {}
    if variants is not None:
        definitions = read_json(variants)
        require(isinstance(definitions, dict) and 1 <= len(definitions) <= 4, "Declare one to four named variants.")
        for name, path in definitions.items():
            require(isinstance(name, str) and re.fullmatch(r"[a-z][a-z0-9_]{0,31}", name)
                    and name not in {"no_skill", "explicit", "automatic", "previous"}, "Invalid/reserved variant name.")
            require(isinstance(path, str) and Path(path).is_absolute(), "Variant roots must be explicit absolute paths.")
            variant_snapshots[name] = identity(path)
    for case in corpus["execution"]:
        case["fixture_identities"] = []
        for name in case.get("fixtures", []):
            builder.safe_relative(name)
            path = fixture_root / name
            checked_path(path, boundary=fixture_root)
            raw = builder.bounded_read(path, 4 * 1024 * 1024)
            case["fixture_identities"].append({"path": name, "sha256": builder.sha256(raw)})
    plan = {"schema_version": "1.0.0", "record_type": "skill-builder-panel",
            "trials": trials, "corpus": corpus, "corpus_sources": source_identities,
            "identities": snapshots, "environment": environment,
            "execution_conditions": ["no_skill", "explicit", "automatic"] + (["previous"] if previous else [])}
    if variant_snapshots:
        plan["variants"] = variant_snapshots
        plan["execution_conditions"].extend(variant_snapshots)
    require(len(schedule(plan)) <= budget["max_runs"], "Scheduled runs exceed the declared budget.")
    return plan


def schedule(plan):
    return {(kind, c["id"], condition, trial): c
            for kind, cases in plan["corpus"].items() for c in cases
            for condition in (["automatic"] if kind == "routing" else plan["execution_conditions"])
            for trial in range(1, plan["trials"] + 1)}


def evidence(root, reference):
    require(isinstance(reference, dict), "Missing evidence reference.")
    relative = builder.safe_relative(reference.get("path"))
    path = root / relative
    checked_path(path, boundary=root)
    raw = builder.bounded_read(path, 16 * 1024 * 1024)
    require(builder.sha256(raw) == reference.get("sha256"), "Evidence digest mismatch.")
    return raw


def activation(trace, expected):
    require(isinstance(trace, dict) and type(trace.get("complete")) is bool
            and isinstance(trace.get("events"), list), "Invalid normalized trace.")
    events = trace["events"]
    require(all(isinstance(e, dict) for e in events), "Invalid trace event.")
    successes = [e for e in events if e.get("kind") == "skill_activation_succeeded"]
    if any(e.get("skill_sha256") == expected for e in successes):
        return True
    if not trace["complete"] or successes or any(e.get("kind") == "skill_activation_failed" for e in events):
        return None
    return False


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def confusion(pairs):
    counts = {"tp": 0, "fn": 0, "fp": 0, "tn": 0}
    for wanted, actual in pairs:
        counts["tp" if wanted and actual else "fn" if wanted else "fp" if actual else "tn"] += 1
    tp, fn, fp, tn = (counts[k] for k in ("tp", "fn", "fp", "tn"))
    return {**counts, "scored": len(pairs), "precision": ratio(tp, tp + fp),
            "recall": ratio(tp, tp + fn), "false_activation_rate": ratio(fp, fp + tn),
            "f1": ratio(2 * tp, 2 * tp + fp + fn)}


def summarize(plan, observations, root, plan_sha256):
    require(isinstance(plan, dict) and type(plan.get("trials")) is int and 1 <= plan["trials"] <= 20,
            "Invalid frozen plan/trial count.")
    require(isinstance(observations, dict), "Observations must be an object.")
    require(observations.get("plan_sha256") == plan_sha256, "Observations identify a different frozen plan.")
    validate_corpus(plan["corpus"])
    require(isinstance(plan.get("identities"), dict) and set(plan["identities"]) == {"candidate", "previous"}, "Invalid snapshot identities.")
    variants = plan.get("variants", {})
    require(isinstance(variants, dict) and len(variants) <= 4 and all(isinstance(n, str)
            and re.fullmatch(r"[a-z][a-z0-9_]{0,31}", n) and n not in {"no_skill", "explicit", "automatic", "previous"}
            for n in variants), "Invalid variant identities.")
    for name, snapshot in {**plan["identities"], **variants}.items():
        if name == "previous" and snapshot is None:
            continue
        require(isinstance(snapshot, dict) and all(isinstance(snapshot.get(k), str)
                and len(snapshot[k]) == 64 and all(c in "0123456789abcdef" for c in snapshot[k])
                for k in ("payload_sha256", "skill_sha256")), "Invalid snapshot digests.")
    require(plan["execution_conditions"] == ["no_skill", "explicit", "automatic"]
            + (["previous"] if plan["identities"].get("previous") else []) + list(variants), "Invalid comparison conditions.")
    expected = schedule(plan)
    rows = observations.get("runs")
    require(isinstance(rows, list) and all(isinstance(r, dict) for r in rows), "Runs must be an array of objects.")
    scored, seen, adverse, invariant_failures, trajectories = {}, set(), [], [], []
    for row in rows:
        key = (row.get("suite"), row.get("case_id"), row.get("condition"), row.get("trial"))
        require(type(row.get("trial")) is int and key in expected and key not in seen, "Unexpected or duplicate run.")
        seen.add(key)
        require(row.get("status") in {"completed", "failed", "blocked", "inconclusive"}, "Invalid run status.")
        require(type(row.get("isolation_verified")) is bool, "Record the independent isolation check.")
        for metric in METRICS:
            value = row.get(metric)
            require(measurement(value), "Metrics must be representable finite, nonnegative numbers or null.")
            if metric in COUNTERS and value is not None:
                require(type(value) is int and isinstance(row.get("metric_sources"), dict)
                        and isinstance(row["metric_sources"].get(metric), str)
                        and row["metric_sources"][metric].strip(), "Measured counters need integer values and named sources.")
        grade = None
        if key[0] == "execution" and (row["status"] == "completed" or row.get("checks") is not None):
            case = expected[key]
            checks = row.get("checks")
            require(isinstance(checks, dict) and set(checks) == set(case["checks"] + case["invariants"]), "Execution check set differs from the frozen oracle.")
            for check in checks.values():
                require(isinstance(check, dict) and type(check.get("passed")) is bool
                        and isinstance(check.get("evidence"), str) and check["evidence"], "Each grade needs a Boolean and evidence.")
            artifacts = row.get("artifacts")
            require(isinstance(artifacts, list) and artifacts, "Execution grading needs actual artifacts.")
            for reference in artifacts:
                evidence(root, reference)
            grade = {"success": all(c["passed"] for c in checks.values()),
                     "invariant_failed": any(not checks[c]["passed"] for c in case["invariants"])}
            if grade["invariant_failed"]:
                invariant_failures.append(list(key))
        trace = None
        if key[0] == "execution" and "trajectory" in expected[key] and row.get("trace") is not None:
            trace = builder.parse_json(evidence(root, row["trace"]))
            trajectories.append({"key": list(key), **trajectory(trace, expected[key]["trajectory"])})
        if row["status"] != "completed" or not row["isolation_verified"]:
            require(isinstance(row.get("reason"), str) and row["reason"], "Unscored runs need a reason.")
            adverse.append({"key": list(key), "reason": row["reason"]})
            continue
        identity_key = "previous" if key[2] == "previous" else "candidate"
        snapshot = variants[key[2]] if key[2] in variants else plan["identities"][identity_key]
        require(row.get("payload_sha256") == (None if key[2] == "no_skill" else snapshot["payload_sha256"]), "Run payload identity mismatch.")
        trace = trace if trace is not None else builder.parse_json(evidence(root, row.get("trace")))
        active = activation(trace, snapshot["skill_sha256"])
        if key[2] == "no_skill":
            # Any target activation contaminates a control, including a hidden
            # revision whose body digest differs from the intended candidate.
            if any(e.get("kind") in {"skill_activation_succeeded", "skill_activation_failed"} for e in trace["events"]):
                active = None
        if active is None or key[2] == "no_skill" and active is not False or key[2] in {"explicit", "previous", *variants} and active is not True:
            adverse.append({"key": list(key), "reason": "Activation/clean-control evidence is incomplete or mismatched."})
            continue
        result = {"active": active, "row": row}
        if grade is not None:
            result.update(grade)
        scored[key] = result
    routing = {}
    for split in ("development", "validation"):
        cases = [c for c in plan["corpus"]["routing"] if c["split"] == split]
        pairs, majority = [], []
        for case in cases:
            values = [v["active"] for k, v in scored.items() if k[:2] == ("routing", case["id"])]
            pairs.extend((case["should_trigger"], v) for v in values)
            if len(values) == plan["trials"] and 2 * sum(values) != len(values):
                majority.append((case["should_trigger"], 2 * sum(values) > len(values)))
        routing[split] = {"trial_level": confusion(pairs), "query_majority": confusion(majority),
                          "scheduled_queries": len(cases), "unscored_queries": len(cases) - len(majority)}
    execution = {}
    for condition in plan["execution_conditions"]:
        results = [v for k, v in scored.items() if k[0] == "execution" and k[2] == condition]
        attempts = [r for r in rows if r["suite"] == "execution" and r["condition"] == condition]
        execution[condition] = {"scored": len(results), "successes": sum(v["success"] for v in results),
                                "success_rate": ratio(sum(v["success"] for v in results), len(results)),
                                "invariant_failures": sum(v["invariant_failed"] for v in results)}
        for metric in METRICS:
            # Failed and infrastructure attempts also consume resources.
            values = [r[metric] for r in attempts if r.get(metric) is not None]
            execution[condition][metric] = {"mean": statistics.mean(values) if values else None,
                                           "known": len(values), "unknown": len(attempts) - len(values)}
    comparisons = {}
    for treatment, control in [("explicit", "no_skill"), ("automatic", "no_skill"), ("explicit", "previous")] + [(n, "explicit") for n in variants]:
        differences = []
        for key, value in scored.items():
            other = (key[0], key[1], control, key[3])
            if key[0] == "execution" and key[2] == treatment and other in scored:
                differences.append(int(value["success"]) - int(scored[other]["success"]))
        comparisons[treatment + "_minus_" + control] = {"matched_trials": len(differences),
                                                        "success_rate_difference": statistics.mean(differences) if differences else None}
    missing = sorted(set(expected) - seen)
    resource_usage = {}
    for metric in METRICS:
        values = [r[metric] for r in rows if r.get(metric) is not None]
        resource_usage[metric] = {"known_total": sum(values) if values else None,
                                  "known": len(values), "unknown": len(rows) - len(values)}
    return {"schema_version": "1.0.0", "record_type": "skill-builder-panel-summary", "plan_sha256": plan_sha256,
            "outcome": "failed" if invariant_failures or any(t["outcome"] == "failed" for t in trajectories)
            else "incomplete" if missing or adverse or any(t["outcome"] == "inconclusive" for t in trajectories) else "completed",
            "scheduled": len(expected), "recorded": len(seen), "scored": len(scored),
            "missing": [list(k) for k in missing], "unscored": adverse, "observed_invariant_failures": invariant_failures, "routing": routing,
            "execution": execution, "paired_comparisons": comparisons, "resource_usage": resource_usage,
            "trajectories": trajectories,
            "limitations": ["Normalized traces and semantic grades require an independent trusted adapter/reviewer; hashes verify identity, not truth.",
                            "Repeated trials are clustered by prompt; these descriptive differences are not confidence intervals or a release certification."]}


def main(default_cases_root=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare", help="Freeze corpus, fixtures, environment, and candidate identities; does not run agents.")
    prep.add_argument("--candidate", required=True)
    prep.add_argument("--previous")
    prep.add_argument("--variants", help="JSON mapping of named explicit instruction variants to absolute runtime roots (maximum four).")
    prep.add_argument("--environment", required=True)
    prep.add_argument("--routing-cases", help="Explicit target-specific labeled routing JSON array.")
    prep.add_argument("--execution-cases", help="Explicit target-specific task JSON array.")
    prep.add_argument("--fixtures-root", help="Approved root for paths in target execution cases.")
    prep.add_argument("--trials", type=int, default=3)
    prep.add_argument("--split", choices=("all", "development", "validation"), default="all")
    prep.add_argument("--case", action="append", default=[], help="Freeze a named subset; repeat. Include at least one routing and one execution case.")
    prep.add_argument("--output", required=True)
    report = sub.add_parser("summarize", help="Verify collected evidence and compute routing and matched task metrics.")
    report.add_argument("--plan", required=True)
    report.add_argument("--observations", required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            plan = prepare(args.candidate, args.previous, args.environment, args.trials, args.split, args.case,
                           routing_cases=args.routing_cases, execution_cases=args.execution_cases,
                           fixtures_root=args.fixtures_root, default_cases_root=default_cases_root, variants=args.variants)
            destination = builder.checked_destination(args.output)
            raw = builder.json_bytes(plan)
            with builder.NewTree(destination) as output:
                output.write("plan.json", raw)
                output.write("observations.json", builder.json_bytes({"plan_sha256": builder.sha256(raw), "runs": []}))
            result = {"outcome": "prepared", "scheduled": len(schedule(plan)), "plan_sha256": builder.sha256(raw)}
        else:
            path = Path(args.observations).absolute()
            plan_raw = builder.bounded_read(Path(args.plan), 16 * 1024 * 1024)
            result = summarize(builder.parse_json(plan_raw), read_json(path), path.parent, builder.sha256(plan_raw))
        print(json.dumps(result, indent=2, allow_nan=False))
        return {"failed": 1, "incomplete": 3}.get(result["outcome"], 0)
    except (ValueError, OSError, KeyError, TypeError, OverflowError) as exc:
        print(json.dumps({"outcome": "blocked", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
