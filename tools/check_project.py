#!/usr/bin/env python3
"""Check preservation and project contracts; do not claim host/security assurance."""
from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import sys
import zipfile

ROOT = Path(__file__).absolute().parents[1]
SKILL = ROOT / "skills" / "skill-builder"
EXPECTED_KB_HASH = "9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204"
EXPECTED_FILES = 182
EXPECTED_BYTES = 76965199
LINK = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)")


def load_module(path: Path, name: str):
    # Bootstrap the shared release checker without importing a symlinked helper.
    # The release checker then validates all selected roots before payload reads.
    requested = path.absolute()
    for component in reversed((requested, *requested.parents)):
        mode = component.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError("Project helper path or ancestor is a symlink")
        if component != requested and not stat.S_ISDIR(mode):
            raise ValueError("Project helper ancestor is not a directory")
    if not stat.S_ISREG(requested.lstat().st_mode) or not requested.resolve(strict=True).is_relative_to(ROOT.resolve(strict=True)):
        raise ValueError("Project helper must be a contained regular file")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ValueError("Cannot load reviewed project helper")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def heading_anchors(text: str) -> set[str]:
    anchors = set()
    counts: dict[str, int] = {}
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            name = re.sub(r"^#{1,6}\s+", "", line).strip().rstrip("#").strip()
            name = re.sub(r"[^\w\- ]", "", name.lower()).replace(" ", "-")
            n = counts.get(name, 0)
            counts[name] = n + 1
            anchors.add(name if n == 0 else f"{name}-{n}")
    return anchors


def check(require_validators: bool = False) -> dict:
    checks = []
    errors = []

    def record(name: str, condition: bool, detail: object = None) -> None:
        checks.append({"name": name, "outcome": "passed" if condition else "failed", "detail": detail})
        if not condition:
            errors.append(name)

    release = load_module(ROOT / "tools/build_release.py", "skill_builder_release_check")
    selected_paths = release.source_paths()
    record("release_input_boundary", True, {
        "selected_files": len(selected_paths),
        "policy": "Required selected roots, files and ancestors are nonsymlink and contained; traversal errors fail explicitly.",
        "limit": "Point-in-time checks; not a sandbox against concurrent filesystem mutation.",
    })
    license_decision = release.license_metadata()
    record("current_scoped_license", True, {
        "license": license_decision["license"], "scope": license_decision["scope"],
        "decision": "skills/skill-builder/references/license-decision.json",
        "limit": "Checks declared terms and component identity; does not adjudicate third-party rights.",
    })

    manifest = json.loads((SKILL / "references/knowledge-base-manifest.json").read_text())
    archive_bytes = (SKILL / "references/knowledge-base.zip").read_bytes()
    record("original_archive_identity", hashlib.sha256(archive_bytes).hexdigest() == EXPECTED_KB_HASH)
    record("manifest_archive_identity", manifest["archive_sha256"] == EXPECTED_KB_HASH)
    mismatches = []
    with zipfile.ZipFile(SKILL / "references/knowledge-base.zip") as archive:
        root = manifest["archive_root"] + "/"
        names = [i.filename for i in archive.infolist()
                 if not i.is_dir() and "__MACOSX" not in Path(i.filename).parts
                 and Path(i.filename).name != ".DS_Store"]
        expected_members = {row["archive_member"] for row in manifest["files"]}
        record("substantive_member_set", len(names) == EXPECTED_FILES and set(names) == expected_members)
        for row in manifest["files"]:
            data = archive.read(row["archive_member"])
            if len(data) != row["size_bytes"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                mismatches.append(row["path"])
        record("all_source_file_bytes", not mismatches, {"mismatches": mismatches, "files": len(names)})
        record("uncompressed_content_total", sum(row["size_bytes"] for row in manifest["files"]) == EXPECTED_BYTES)
        rules = json.loads(archive.read(root + "catalogs/requirements.json"))["rules"]
        canonical = {row["id"]: row for row in rules}
        record("canonical_rules", len(rules) == len(canonical) == 99)

    mapping = json.loads((SKILL / "references/implementation-map.json").read_text())
    mapped = mapping["rules"]
    record("all_rule_owners_present", len(mapped) == 99 and {r["id"] for r in mapped} == set(canonical))
    map_errors = []
    for row in mapped:
        original = canonical.get(row["id"], {})
        expected_pointer = "/rules/" + str(next((i for i, item in enumerate(rules) if item["id"] == row["id"]), -1))
        if row.get("canonical_pointer") != expected_pointer:
            map_errors.append({"id": row["id"], "error": "canonical pointer does not identify the matching original rule"})
        if row.get("basis") != original.get("basis") or row.get("strength") != original.get("strength"):
            map_errors.append({"id": row["id"], "error": "changed canonical basis/strength"})
        for key in ("owners", "applicability", "enforcement", "verification", "assurance_limit"):
            if not row.get(key):
                map_errors.append({"id": row["id"], "error": f"missing {key}"})
        for owner in row.get("owners", []):
            path, _, anchor = owner.partition("#")
            target = SKILL / path
            if not target.is_file() or target.is_symlink() or not target.resolve().is_relative_to(SKILL):
                map_errors.append({"id": row["id"], "error": "missing or escaping owner", "owner": owner})
            elif anchor and anchor not in heading_anchors(target.read_text()):
                map_errors.append({"id": row["id"], "error": "missing heading anchor", "owner": owner})
    record("rule_owner_contracts", not map_errors, map_errors)

    version = (ROOT / "VERSION").read_text().strip()
    helper = load_module(SKILL / "scripts/skill_builder.py", "skill_builder_project_check")
    record("version_agreement", version == (SKILL / "VERSION").read_text().strip() == helper.VERSION)
    record("plugin_package_contract", True, release.validate_plugin(release.plugin_files(release.runtime_files())))
    entry = (SKILL / "SKILL.md").read_text()
    # Use the strict preserved YAML validator below, rather than a second
    # regex rejecting optional fields, reordered keys and folded descriptions.
    record("entrypoint_not_placeholder", "TODO" not in entry and len(entry.splitlines()) < 500,
           {"lines": len(entry.splitlines()), "bytes": len(entry.encode())})
    record("single_discoverable_runtime_entry", [p.relative_to(SKILL).as_posix() for p in SKILL.rglob("SKILL.md")] == ["SKILL.md"])

    missing_links = []
    for path in (path for path in selected_paths if path.suffix == ".md"):
        body = path.read_text(encoding="utf-8")
        for link in LINK.findall(body):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link.startswith("#"):
                continue
            local = link.split("#", 1)[0].split("?", 1)[0]
            if not local or any(c in local for c in ("<", ">", "{", "}")):
                continue
            target = path.parent / local
            if not target.exists():
                missing_links.append({"from": path.relative_to(ROOT).as_posix(), "target": link})
    record("local_document_links", not missing_links, missing_links)

    syntax_errors = []
    for path in (path for path in selected_paths if path.suffix == ".py" and (
            path.is_relative_to(ROOT / "tools") or path.is_relative_to(ROOT / "tests")
            or path.is_relative_to(SKILL / "scripts"))):
        try:
            ast.parse(path.read_text(), filename=str(path))
        except SyntaxError as exc:
            syntax_errors.append({"path": path.relative_to(ROOT).as_posix(), "line": exc.lineno})
    record("python_syntax", not syntax_errors, syntax_errors)

    kb = helper.KnowledgeBase()
    structural = helper.format_checks(kb, SKILL, {"files": [{"path": "SKILL.md", "kind": "regular_file", "status": "hashed"}]})
    checks.append({"name": "portable_entrypoint", "outcome": structural["outcome"],
                   "detail": "Strict preserved YAML/field/name-directory validation; see original_portable_validator."})
    if structural["outcome"] == "failed":
        errors.append("portable_entrypoint")
    if structural["outcome"] == "blocked":
        checks.append({"name": "original_portable_validator", "outcome": "blocked", "detail": structural})
        if require_validators:
            errors.append("original_portable_validator unavailable")
    else:
        record("original_portable_validator", structural["outcome"] == "passed", structural)
    if require_validators:
        try:
            import jsonschema  # noqa: F401 -- required capability, never installed here
            import referencing  # noqa: F401
            record("evidence_validator_dependencies", True)
        except ImportError:
            record("evidence_validator_dependencies", False, "Explicitly provision requirements-validation.txt")
    return {
        "schema_version": "1.0.0", "outcome": "failed" if errors else "passed",
        "scope": "Release-input containment, preservation, implemented ownership mapping, entrypoint/links/syntax and available original format checks",
        "checks": checks, "failed_checks": errors,
        "not_established": ["semantic truth of all rule decisions", "native discovery or host enforcement",
                            "clean baseline improvement", "public distribution rights", "GitHub CI execution"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-validators", action="store_true", help="Fail if optional YAML/schema validation dependencies are unavailable")
    args = parser.parse_args()
    if not sys.flags.isolated:
        parser.error("Use python3 -I -B for isolated dependency imports")
    try:
        result = check(args.require_validators)
    except (OSError, KeyError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({"outcome": "failed", "error": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["outcome"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
