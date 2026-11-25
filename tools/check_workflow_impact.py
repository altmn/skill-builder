#!/usr/bin/env python3
"""Check fresh create/audit impact reviews for staged or committed changes.

Read-only, standard-library maintenance check. Never execute evidence or target
code. Checks record structure, freshness and path coverage, not reviewer truth.
"""
import argparse
import json
import os
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).absolute().parents[1]
PREFIX = "docs/change-impact/"
STATES = {"passed", "failed", "blocked", "not_run", "inconclusive", "not_applicable"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def git(root, *args, input=None):
    result = subprocess.run(["git", "--no-optional-locks", "-C", str(root), *args],
                            input=input, capture_output=True, timeout=30,
                            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
    require(result.returncode == 0, "Git object/range is unavailable; inspect the checkout and requested base.")
    return result.stdout


def record_path(path):
    return path.startswith(PREFIX) and path.endswith(".json")


def portable(path):
    require(isinstance(path, str) and path and not any(ord(c) < 32 for c in path), "Invalid review path.")
    logical = PurePosixPath(path)
    require(not logical.is_absolute() and ".." not in logical.parts and "\\" not in path
            and str(logical) == path, "Review paths must be exact repository-relative paths.")
    return path


def explanation(value):
    require(isinstance(value, str) and len(value.strip()) >= 20 and
            not any(word in value.upper() for word in ("REPLACE", "TODO", "TBD")),
            "Provide a concrete explanation of at least 20 characters, without placeholders.")


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key in impact record.")
        result[key] = value
    return result


def blob(root, tree, path):
    spec = tree + ":" + portable(path)
    require(git(root, "cat-file", "-t", spec).strip() == b"blob", "Review reference must identify a file.")
    return spec


def validate(record, changed, exists):
    require(isinstance(record, dict) and record.get("schema_version") == "1.0.0", "Unsupported impact record.")
    explanation(record.get("summary"))
    paths = record.get("reviewed_paths")
    require(isinstance(paths, list) and paths and all(isinstance(p, str) for p in paths)
            and len(paths) == len(set(paths)), "Provide unique reviewed_paths.")
    for path in paths:
        portable(path)
    modes = record.get("workflows")
    require(isinstance(modes, dict) and set(modes) == {"create", "audit"}, "Review create and audit separately.")
    unresolved = []
    for name, mode in modes.items():
        require(isinstance(mode, dict) and mode.get("decision") in {"updated", "no_change_needed"}, "Invalid workflow decision.")
        explanation(mode.get("reason"))
        owners = mode.get("owners")
        require(isinstance(owners, list) and owners, "Identify downstream owners even when no change is needed.")
        for owner in owners:
            exists(portable(owner))
        if mode["decision"] == "updated":
            require(any(owner in paths for owner in owners), "An updated decision needs a reviewed implementation owner.")
        verification = mode.get("verification")
        require(isinstance(verification, dict) and verification.get("status") in STATES, "Record actual verification status.")
        explanation(verification.get("reason"))
        if verification["status"] == "passed":
            commands, evidence = verification.get("commands"), verification.get("evidence")
            require(isinstance(commands, list) and commands and all(isinstance(c, str) and c.strip() for c in commands), "A pass needs commands.")
            require(isinstance(evidence, list) and evidence, "A pass needs retained evidence files.")
            for path in evidence:
                exists(portable(path))
        else:
            explanation(verification.get("consequence"))
            unresolved.append({"workflow": name, "status": verification["status"], "consequence": verification["consequence"]})
    return set(paths) & changed, unresolved


def ci_base(root, event):
    require(isinstance(event, dict), "CI event must be an object.")
    if "pull_request" in event:
        return event["pull_request"]["base"]["sha"]
    before = event.get("before")
    if before and set(before) != {"0"}:
        return before
    # New-branch pushes/manual runs check the latest commit. PRs check the
    # complete branch range. Root commits compare against Git's empty tree.
    parents = git(root, "rev-list", "--parents", "-n", "1", "HEAD").decode().split()
    return parents[1] if len(parents) > 1 else git(root, "hash-object", "-t", "tree", "--stdin", input=b"").decode().strip()


def check(root=ROOT, base=None, event=None):
    if event is not None:
        base = ci_base(root, event)
    if base is None:
        arguments, tree = ["--cached"], ""
    else:
        resolved = git(root, "rev-parse", "--verify", "--end-of-options", base).decode().strip()
        if git(root, "cat-file", "-t", resolved).strip() == b"commit":
            resolved = git(root, "merge-base", resolved, "HEAD").decode().strip()
        arguments, tree = [resolved, "HEAD"], "HEAD"
    def paths(*extra):
        raw = git(root, "diff", "--no-ext-diff", "--no-renames", "--name-only", "-z", *extra, *arguments, "--")
        return set(os.fsdecode(raw).split("\0")) - {""}
    changed, added = paths(), paths("--diff-filter=A")
    reviews = {p for p in changed if record_path(p)}
    require(reviews <= added, "Impact records are append-only; add a follow-up instead of rewriting/deleting one.")
    required = changed - reviews
    coverage, records, unresolved = set(), [], []
    for path in sorted(reviews):
        spec = blob(root, tree, path)
        require(int(git(root, "cat-file", "-s", spec)) <= 1024 * 1024, "Impact record exceeds the 1 MiB limit.")
        data = json.loads(git(root, "show", "--no-textconv", spec), object_pairs_hook=unique,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Nonfinite JSON rejected.")))
        covered, pending = validate(data, required, lambda p: blob(root, tree, p))
        coverage.update(covered)
        unresolved.extend({"record": path, **p} for p in pending)
        records.append(path)
    missing = sorted(required - coverage)
    return {"schema_version": "1.0.0", "outcome": "failed" if missing else "passed",
            "scope": "Staged index" if base is None else "Committed range from merge base (or empty tree) to HEAD",
            "changed_files": len(required), "fresh_records": records, "unreviewed_paths": missing,
            "unresolved_verification": unresolved,
            "limits": "Checks freshness, structure and path coverage only; reviewers assess reasoning and evidence truth. Unresolved verification is not release approval."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--base", help="Committed comparison base; default checks staged changes.")
    group.add_argument("--ci", action="store_true", help="Read base from GITHUB_EVENT_PATH; no fetch or network.")
    args = parser.parse_args()
    try:
        event = None
        if args.ci:
            event_path = Path(os.environ["GITHUB_EVENT_PATH"])
            require(event_path.stat().st_size <= 1024 * 1024, "CI event is too large.")
            event = json.loads(event_path.read_text())
        result = check(base=args.base, event=event)
        code = 0 if result["outcome"] == "passed" else 1
    except (ValueError, TypeError, KeyError, OSError, subprocess.TimeoutExpired) as exc:
        result, code = {"outcome": "blocked", "error": str(exc)}, 2
    print(json.dumps(result, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
