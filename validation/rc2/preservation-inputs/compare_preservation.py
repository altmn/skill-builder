#!/usr/bin/env python3
"""Read-only preservation comparison against the exact uploaded source ZIP.

No project modules are imported or executed. JSON goes to stdout; --output
creates a new evidence file exclusively. Candidate roots may have any version.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile

EXPECTED_UPLOAD_SHA256 = "624d313a45a15749c75a5251b53c40408808ba1ee3c7149e2d4697635bd06588"
EXPECTED_KB_SHA256 = "9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204"
KB = "skills/skill-builder/references/knowledge-base.zip"
KB_MANIFEST = "skills/skill-builder/references/knowledge-base-manifest.json"
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TOTAL_BYTES = 512 * 1024 * 1024


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_name(name: str) -> PurePosixPath:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError("Unsafe archive path")
    if str(path) != name.rstrip("/") or ":" in path.parts[0]:
        raise ValueError("Noncanonical archive path")
    return path


def read_zip(path: Path) -> tuple[dict[str, bytes], dict]:
    raw = path.read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos = archive.infolist()
        if len(infos) > 10000 or len({i.filename for i in infos}) != len(infos):
            raise ValueError("Duplicate or excessive ZIP entries")
        if sum(i.file_size for i in infos) > MAX_TOTAL_BYTES:
            raise ValueError("ZIP exceeds total inspection budget")
        roots = {safe_name(i.filename).parts[0] for i in infos}
        if len(roots) != 1:
            raise ValueError("Expected one named archive root")
        root = next(iter(roots))
        files = {}
        for info in infos:
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise ValueError("Symlink ZIP member refused")
            if info.is_dir():
                continue
            if info.file_size > MAX_FILE_BYTES:
                raise ValueError("ZIP member exceeds inspection budget")
            relative = safe_name(info.filename).relative_to(root).as_posix()
            if relative == "." or relative in files:
                raise ValueError("Invalid or duplicate relative member")
            files[relative] = archive.read(info)
    return files, {"kind": "zip", "path": str(path), "root": root,
                   "sha256": digest(raw), "size_bytes": len(raw),
                   "entry_count": len(infos), "file_count": len(files)}


def read_tree(path: Path) -> tuple[dict[str, bytes], dict]:
    if path.is_symlink() or not path.is_dir():
        raise ValueError("Candidate tree must be a nonsymlink directory")
    files = {}
    total = 0
    def fail(exc: OSError) -> None:
        raise exc
    for directory, dirs, names in os.walk(path, followlinks=False, onerror=fail):
        for name in dirs:
            if (Path(directory) / name).is_symlink():
                raise ValueError("Candidate directory symlink refused")
        for name in names:
            target = Path(directory) / name
            if not stat.S_ISREG(target.lstat().st_mode):
                raise ValueError("Nonregular candidate file refused")
            with target.open("rb") as stream:
                raw = stream.read(MAX_FILE_BYTES + 1)
            if len(raw) > MAX_FILE_BYTES:
                raise ValueError("Candidate file exceeds inspection budget")
            total += len(raw)
            if total > MAX_TOTAL_BYTES or len(files) >= 10000:
                raise ValueError("Candidate tree exceeds inspection budget")
            files[target.relative_to(path).as_posix()] = raw
    return files, {"kind": "directory", "path": str(path), "file_count": len(files),
                   "limit": "Point-in-time reads; no concurrent-mutation sandbox claim."}


def source_manifest_check(files: dict[str, bytes]) -> dict:
    if "PACKAGE-MANIFEST.json" not in files:
        return {"outcome": "failed", "reason": "Missing generated source manifest"}
    try:
        manifest = json.loads(files["PACKAGE-MANIFEST.json"])
        rows = manifest["files"]
        paths = [row["path"] for row in rows]
        declared = {row["path"]: (row["size_bytes"], row["sha256"]) for row in rows}
        observed = {p: (len(raw), digest(raw)) for p, raw in files.items()
                    if p != "PACKAGE-MANIFEST.json"}
        canonical = (json.dumps(rows, ensure_ascii=False, sort_keys=True,
                                separators=(",", ":")) + "\n").encode()
        okay = (len(paths) == len(set(paths)) == manifest["file_count"]
                and declared == observed and paths == sorted(paths)
                and digest(canonical) == manifest["payload_sha256"])
        return {"outcome": "passed" if okay else "failed", "version": manifest.get("version"),
                "declared_files": manifest["file_count"], "observed_files": len(observed),
                "recorded_payload_sha256": manifest["payload_sha256"],
                "observed_payload_sha256": digest(canonical),
                "missing_or_changed": sorted(p for p in declared if declared[p] != observed.get(p)),
                "undeclared": sorted(set(observed) - set(declared))}
    except (ValueError, TypeError, KeyError) as exc:
        return {"outcome": "failed", "reason": type(exc).__name__}


def compare(original_path: Path, candidate_path: Path, require_manifest: bool) -> dict:
    original, original_identity = read_zip(original_path)
    if original_identity["sha256"] != EXPECTED_UPLOAD_SHA256:
        raise ValueError("Original upload identity mismatch")
    candidate, candidate_identity = (read_tree(candidate_path) if candidate_path.is_dir()
                                    else read_zip(candidate_path))
    missing = sorted(set(original) - set(candidate))
    changed = [{"path": p, "original_sha256": digest(original[p]),
                "candidate_sha256": digest(candidate[p]),
                "original_size_bytes": len(original[p]), "candidate_size_bytes": len(candidate[p])}
               for p in sorted(set(original) & set(candidate)) if original[p] != candidate[p]]
    historical = sorted(p for p in original if p.startswith("validation/")
                        and p != "validation/README.md")
    changed_historical = [p for p in historical if original[p] != candidate.get(p)]
    checks = {
        "all_original_file_paths_retained": not missing,
        "frozen_kb_archive_exact": original[KB] == candidate.get(KB)
            and digest(original[KB]) == EXPECTED_KB_SHA256,
        "frozen_kb_manifest_exact": original[KB_MANIFEST] == candidate.get(KB_MANIFEST),
        "historical_validation_bytes_unchanged": not changed_historical,
    }
    manifest = source_manifest_check(candidate)
    if require_manifest:
        checks["generated_source_manifest_matches_candidate"] = manifest["outcome"] == "passed"
    kb_entries = []
    if checks["frozen_kb_archive_exact"]:
        with zipfile.ZipFile(io.BytesIO(candidate[KB])) as archive:
            for info in archive.infolist():
                parts = PurePosixPath(info.filename).parts
                substantive = (not info.is_dir() and "__MACOSX" not in parts
                               and ".DS_Store" not in parts
                               and not any(p.startswith("._") for p in parts))
                kb_entries.append({"path": info.filename, "size_bytes": info.file_size,
                                   "sha256": digest(archive.read(info)), "substantive": substantive})
    historical_receipts = []
    for path in ("validation/local-evaluation-receipt.json",
                 "validation/final-local-evaluation-receipt.json"):
        if path not in original:
            continue
        receipt = json.loads(original[path])
        recorded_inputs = {}
        for attempt in receipt.get("attempts", []):
            for target, recorded in attempt.get("input_hashes", {}).items():
                old_hash = digest(original[target]) if target in original else None
                new_hash = digest(candidate[target]) if target in candidate else None
                recorded_inputs[target] = {
                    "recorded_sha256": recorded,
                    "uploaded_release_sha256": old_hash,
                    "candidate_sha256": new_hash,
                    "matches_uploaded_release": recorded == old_hash,
                    "matches_candidate": recorded == new_hash,
                }
        historical_receipts.append({
            "path": path, "recorded_at": receipt.get("recorded_at"),
            "stored_artifact_id": receipt.get("artifact", {}).get("artifact_id"),
            "stored_package_sha256": receipt.get("artifact", {}).get("package_sha256"),
            "stored_panel_id": receipt.get("panel", {}).get("id"),
            "is_current_candidate_execution_evidence": False,
            "interpretation": "Retained evidence for its recorded inputs and package only. Differences from current candidate inputs are expected after edits and are not a preservation failure. Earlier development inputs can also differ from the uploaded release.",
            "recorded_inputs": recorded_inputs,
        })
    member_rows = sorted(kb_entries, key=lambda row: row["path"])
    member_json = (json.dumps(member_rows, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")) + "\n").encode()
    return {"schema_version": "1.0.0", "record_type": "current-release-preservation-audit",
            "observed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            "outcome": "passed" if all(checks.values()) else "failed",
            "original": original_identity, "candidate": candidate_identity,
            "candidate_version": candidate.get("VERSION", b"").decode("utf-8").strip(),
            "checks": checks, "missing_original_paths": missing,
            "modified_original_files": changed,
            "added_files": sorted(set(candidate) - set(original)),
            "historical_validation_files_checked": len(historical),
            "changed_historical_validation_files": changed_historical,
            "historical_receipts": historical_receipts,
            "source_manifest": manifest,
            "kb": {"archive_sha256": digest(candidate[KB]) if KB in candidate else None,
                   "archive_size_bytes": len(candidate[KB]) if KB in candidate else None,
                   "entry_count": len(kb_entries),
                   "substantive_file_count": sum(e["substantive"] for e in kb_entries),
                   "substantive_bytes": sum(e["size_bytes"] for e in kb_entries if e["substantive"]),
                   "all_members_rehashed": bool(kb_entries),
                   "member_identities_sha256": digest(member_json),
                   "member_identity_algorithm": "SHA-256 of sorted path/size_bytes/sha256/substantive rows in UTF-8 JSON with sorted keys, compact separators, plus LF; full original entries are in original-kb-inventory.json."},
            "limits": ["Retained paths and exact immutable/history bytes are established; changed prose/code still needs substantive review.",
                       "No candidate code or host integration was executed by this comparison.",
                       "Historical validation README is a current index and may change; historical results themselves are compared byte for byte."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--require-manifest", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = compare(args.original.absolute(), args.candidate.absolute(), args.require_manifest)
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(encoded)
    print(encoded, end="")
    return 0 if result["outcome"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
