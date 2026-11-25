#!/usr/bin/env python3
"""Offline companion-record checks and advisory Markdown review.

Never execute target code, install dependencies, send reports or grade semantics.
All input/evidence reads use the evaluation helper's bounded containment checks.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location("review_evaluation", ROOT / "evaluate.py")
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)
require = evaluation.require


def text(value):
    return isinstance(value, str) and bool(value.strip()) and "REPLACE:" not in value


def case_index(path):
    cases = evaluation.read_json(path)
    require(isinstance(cases, list) and cases, "Supply nonempty execution cases.")
    result = {}
    for case in cases:
        require(isinstance(case, dict) and text(case.get("id")) and case["id"] not in result,
                "Execution cases need unique IDs.")
        for field in ("checks", "invariants"):
            require(isinstance(case.get(field), list) and case[field] and all(text(v) for v in case[field])
                    and len(set(case[field])) == len(case[field]), "Cases need check/invariant IDs.")
        require(not set(case["checks"]) & set(case["invariants"]), "Check and invariant IDs overlap.")
        result[case["id"]] = case
    return result


def contract(record, target, cases):
    require(isinstance(record, dict) and record.get("record_type") == "workflow-contract"
            and record.get("schema_version") == "1.0.0" and text(record.get("goal"))
            and isinstance(record.get("outputs"), list) and record["outputs"]
            and all(text(v) for v in record["outputs"]), "Complete the workflow contract goal and outputs.")
    target = evaluation.checked_path(target, directory=True)
    requirements = record.get("requirements")
    require(isinstance(requirements, list) and requirements, "Contract needs explicit requirements.")
    seen, diagnostics = set(), []
    for rule in requirements:
        require(isinstance(rule, dict) and text(rule.get("id")) and rule["id"] not in seen,
                "Requirements need unique IDs.")
        seen.add(rule["id"])
        require(rule.get("kind") in {"output", "required_action", "forbidden_action"}
                and text(rule.get("statement")), "Invalid requirement kind/statement.")
        owner = rule.get("owner")
        require(isinstance(owner, dict), "Requirement needs a source owner and digest.")
        relative = evaluation.builder.safe_relative(owner.get("path"))
        path = evaluation.checked_path(target / relative, boundary=target)
        actual = evaluation.builder.sha256(evaluation.builder.bounded_read(path, 1024 * 1024))
        if actual != owner.get("sha256"):
            diagnostics.append({"requirement": rule["id"], "code": "owner_drift"})
        links = rule.get("verification")
        require(isinstance(links, list) and links, "Each requirement needs case/check mappings.")
        for link in links:
            require(isinstance(link, dict) and link.get("case_id") in cases, "Unknown requirement case.")
            case = cases[link["case_id"]]
            allowed = case["invariants"] if rule["kind"] == "forbidden_action" else case["checks"] + case["invariants"]
            require(link.get("check_id") in allowed, "Unknown check or forbidden action mapped outside invariants.")
    return {"outcome": "failed" if diagnostics else "passed", "requirements": len(seen),
            "diagnostics": diagnostics, "limit": "Checks source identity and mappings, not completeness, semantic coverage or actual enforcement."}


def papercut(record, root, cases):
    require(isinstance(record, dict) and record.get("record_type") == "skill-papercut"
            and record.get("schema_version") == "1.0.0", "Invalid papercut record.")
    for field in ("id", "subject", "version", "attempted", "expected", "observed", "owner", "dedup_key"):
        require(text(record.get(field)), "Complete the papercut identity, reproduction and owner fields.")
    require(record.get("status") in {"open", "triaged", "resolved"}, "Invalid papercut status.")
    require(isinstance(record.get("evidence"), list), "Retain redacted incident evidence references.")
    for reference in record["evidence"]:
        evaluation.evidence(root, reference)
    regression = record.get("regression")
    if regression is not None:
        require(isinstance(regression, dict) and regression.get("case_id") in cases,
                "Papercut regression must identify an actual case.")
    if record["status"] == "resolved":
        require(record["evidence"] and regression is not None, "Resolution needs retained incident evidence and a regression.")
        receipt = evaluation.builder.parse_json(evaluation.evidence(root, regression.get("receipt")))
        require(isinstance(receipt, dict) and receipt.get("case_id") == regression["case_id"]
                and receipt.get("outcome") == "passed" and receipt.get("subject_version") == record["version"]
                and text(receipt.get("independent_checker")), "Resolution needs an identity-bound independent passing regression receipt.")
    return {"outcome": "passed", "status": record["status"],
            "limit": "Validates local record/evidence structure, not report truth or proof of a production fix. No report was sent."}


def lint(path):
    path = evaluation.checked_path(path)
    raw = evaluation.builder.bounded_read(path, 1024 * 1024)
    lines = raw.decode("utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if re.match(r"^(?:#{2,6}\s+(?:step\b|\d|create-\d|audit-\d)|\d+\.\s)", line, re.I)]
    diagnostics = []
    checks = re.compile(r"\b(verify|check|confirm|expected|evidence|assert|validate|return|report|stop)\b", re.I)
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:end])
        if not checks.search(block):
            diagnostics.append({"line": start + 1, "code": "completion_condition", "message": "Review this step for an observable completion or stop condition."})
        if re.search(r"^\s*(?:python\d*|git|curl|node|bash)\s", block, re.M) and not re.search(r"\b(exit|stdout|stderr|result|output|status|verify|check)\b", block, re.I):
            diagnostics.append({"line": start + 1, "code": "command_result", "message": "Review how the command result is checked before continuing."})
    for i, line in enumerate(lines):
        if re.search(r"\b(?:try again|retry)[.!]?\s*$", line, re.I):
            diagnostics.append({"line": i + 1, "code": "recovery", "message": "Name the failure cause, remediation and retry/stop bound."})
    if not starts:
        diagnostics.append({"line": 1, "code": "manual_review", "message": "No recognized step boundaries; inspect the workflow manually."})
    return {"outcome": "advisory", "source_sha256": evaluation.builder.sha256(raw),
            "steps_inspected": len(starts), "diagnostics": diagnostics,
            "limit": "Heuristic locators only; zero diagnostics is not semantic, quality or safety approval."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    checker = sub.add_parser("contract", help="Check stable requirements, owner drift and case/check mappings.")
    checker.add_argument("--record", required=True)
    checker.add_argument("--target", required=True)
    checker.add_argument("--execution-cases", required=True)
    incident = sub.add_parser("papercut", help="Validate a local opt-in incident; never submit it.")
    incident.add_argument("--record", required=True)
    incident.add_argument("--evidence-root", required=True)
    incident.add_argument("--execution-cases", required=True)
    advisory = sub.add_parser("lint", help="Return advisory workflow diagnostics for one explicit Markdown file.")
    advisory.add_argument("path")
    args = parser.parse_args()
    try:
        if args.command == "lint":
            result = lint(args.path)
        elif args.command == "contract":
            result = contract(evaluation.read_json(args.record), args.target, case_index(args.execution_cases))
        else:
            root = evaluation.checked_path(args.evidence_root, directory=True)
            result = papercut(evaluation.read_json(args.record), root, case_index(args.execution_cases))
        print(json.dumps({"schema_version": "1.0.0", **result}, indent=2))
        return 1 if result["outcome"] == "failed" else 0
    except (ValueError, OSError, TypeError, KeyError):
        # Do not echo private input values or parser excerpts.
        print(json.dumps({"outcome": "blocked", "error": "Invalid, incomplete, inaccessible or escaping review input; inspect the companion contract."}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
