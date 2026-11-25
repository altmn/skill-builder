#!/usr/bin/env python3
"""Prepare deterministic, unpublished archives from the reviewed project tree.

No installation, network, Git operation, dependency bootstrap, or publication.
Archive preparation is independent of the licensing/native-host release gates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import struct
import tempfile
import unicodedata
from urllib.parse import urlsplit
import zipfile

# Keep the requested path intact until the component-by-component checks below.
# Resolving here would conceal a symlink used to enter the project.
ROOT = Path(__file__).absolute().parents[1]
SKILL = ROOT / "skills" / "skill-builder"
STAMP = (2026, 11, 22, 0, 0, 0)
SOURCE_FILES = {
    "README.md", "VERSION", "LICENSE.md", "NOTICE.md", "CONTRIBUTING.md",
    "SECURITY.md", "CHANGELOG.md", "AGENTS.md", ".gitignore",
    "requirements-validation.txt",
    "plugin.json", "PRIVACY.md", "TERMS.md", "SUPPORT.md", "CODE_OF_CONDUCT.md",
}
SOURCE_DIRS = {"skills", "docs", "tests", "tools", "evals", "validation", ".github", ".agents", "assets"}
PLUGIN_ASSETS = {"assets/icon.png", "assets/icon-dark.png"}
OMIT_PARTS = {"__pycache__", ".pytest_cache", ".venv", ".git", "dist"}
MAX_INPUT_BYTES = 128 * 1024 * 1024
EXPECTED_KB_HASH = "9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204"
EXPECTED_COPYRIGHT = "Copyright (c) 2026 Alex Allen"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def checked_path(path: Path, *, directory: bool = False,
                 boundary: Path | None = None) -> Path:
    """Reject aliases before resolving; this is a point-in-time filesystem check."""
    requested = path.absolute()
    for component in reversed((requested, *requested.parents)):
        mode = component.lstat().st_mode
        if stat.S_ISLNK(mode):
            raise ValueError(f"Symlink inputs/ancestors are not distributable: {component}")
        if component != requested and not stat.S_ISDIR(mode):
            raise ValueError(f"Input ancestor must be a directory: {component}")
    mode = requested.lstat().st_mode
    required = stat.S_ISDIR if directory else stat.S_ISREG
    if not required(mode):
        raise ValueError(f"Expected a {'directory' if directory else 'regular file'} input: {requested}")
    resolved = requested.resolve(strict=True)
    if boundary is not None:
        root = checked_path(boundary, directory=True)
        if not resolved.is_relative_to(root):
            raise ValueError(f"Input escapes the selected boundary: {requested}")
    return resolved


def regular_bytes(path: Path, *, boundary: Path | None = None) -> bytes:
    checked_path(path, boundary=boundary)
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or path.is_symlink():
        raise ValueError(f"Only regular non-symlink inputs are allowed: {path}")
    if info.st_size > MAX_INPUT_BYTES:
        raise ValueError(f"Input exceeds build byte budget: {path}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(path, flags)
    with os.fdopen(fd, "rb") as handle:
        opened = os.fstat(handle.fileno())
        if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
            raise ValueError(f"Input changed during open: {path}")
        data = handle.read(MAX_INPUT_BYTES + 1)
    if len(data) > MAX_INPUT_BYTES:
        raise ValueError(f"Input grew beyond build byte budget: {path}")
    return data


def walk_files(base: Path, *, boundary: Path | None = None) -> list[Path]:
    base = base.absolute()
    boundary = boundary if boundary is not None else base
    checked_path(base, directory=True, boundary=boundary)
    result = []

    def traversal_error(error: OSError) -> None:
        raise error

    for parent, dirs, files in os.walk(base, followlinks=False, onerror=traversal_error):
        current = Path(parent)
        checked_path(current, directory=True, boundary=boundary)
        for name in list(dirs):
            child = current / name
            checked_path(child, directory=True, boundary=boundary)
            if name in OMIT_PARTS:
                dirs.remove(name)
        for name in files:
            checked_path(current / name, boundary=boundary)
            if name == ".DS_Store" or name.endswith((".pyc", ".pyo")):
                continue
            if (name == ".env" or name.startswith(".env.")
                    or name in {".netrc", ".pypirc", "id_rsa", "id_ed25519"}):
                raise ValueError(f"Local environment/credential filename is not distributable: {current / name}")
            result.append(current / name)
    return sorted(result)


def runtime_files() -> dict[str, bytes]:
    checked_path(SKILL, directory=True, boundary=ROOT)
    files = {p.relative_to(SKILL).as_posix(): regular_bytes(p, boundary=SKILL)
             for p in walk_files(SKILL, boundary=SKILL)}
    if "SKILL.md" not in files:
        raise ValueError("Runtime entrypoint is missing")
    extra_entrypoints = [name for name in files
                         if name != "SKILL.md" and name.endswith("/SKILL.md")]
    if extra_entrypoints:
        raise ValueError(f"Nested discoverable entrypoints: {extra_entrypoints}")
    return files


def license_metadata() -> dict:
    """Read the current scoped decision; frozen historical notices stay unchanged."""
    decision = json.loads(regular_bytes(SKILL / "references/license-decision.json", boundary=SKILL))
    required = {
        "schema_version": "1.0.0", "license": "MIT", "status": "selected",
        "copyright": EXPECTED_COPYRIGHT, "declaration": "LICENSE.md",
        "knowledge_base_archive_sha256": EXPECTED_KB_HASH,
        "scope": "original_work_only; retained third-party terms apply",
    }
    if not isinstance(decision, dict) or any(decision.get(key) != value for key, value in required.items()):
        raise ValueError("Current license decision is missing or inconsistent")
    # The original grant began at rc.2; a later release does not change that date.
    if decision.get("effective_version") != "1.0.0-rc.2":
        raise ValueError("License decision effective version is inconsistent")
    source_license = regular_bytes(ROOT / "LICENSE.md", boundary=ROOT)
    runtime_license = regular_bytes(SKILL / "LICENSE.md", boundary=SKILL)
    if source_license != runtime_license:
        raise ValueError("Source/runtime license declarations disagree")
    declaration = source_license.decode("utf-8")
    attribution = [line.strip() for line in declaration.splitlines()
                   if line.strip().startswith("Copyright (c) ")]
    if attribution != [EXPECTED_COPYRIGHT]:
        raise ValueError("License declaration copyright attribution is inconsistent")
    text = " ".join(declaration.split())
    clauses = (
        "MIT License",
        "Permission is hereby granted, free of charge, to any person obtaining a copy",
        "to deal in the Software without restriction",
        "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.",
        'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND',
        "IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY",
        EXPECTED_KB_HASH,
    )
    if any(clause not in text for clause in clauses):
        raise ValueError("License declaration lacks required MIT terms or component identity")
    if digest(regular_bytes(SKILL / "references/knowledge-base.zip", boundary=SKILL)) != EXPECTED_KB_HASH:
        raise ValueError("License coverage does not match the preserved knowledge-base identity")
    return decision


def payload_manifest(files: dict[str, bytes], kind: str) -> dict:
    license_decision = license_metadata()
    entries = [{"path": name, "size_bytes": len(data), "sha256": digest(data)}
               for name, data in sorted(files.items())]
    return {
        "schema_version": "1.0.0", "kind": kind,
        "version": regular_bytes(ROOT / "VERSION").decode().strip(),
        "identity_algorithm": "sha256 of UTF-8 canonical JSON files array plus LF; manifest excludes itself",
        "payload_sha256": digest(canonical(entries)),
        "file_count": len(entries), "files": entries,
        "release_state": "prepared_unpublished",
        "license": license_decision["license"],
        "license_scope": license_decision["scope"],
        "license_declaration": license_decision["declaration"],
        "open_reuse_gate": "license_selected_with_retained_third_party_terms",
        "native_host_execution": "not_run",
    }


def make_zip(path: Path, prefix: str, files: dict[str, bytes], kind: str) -> dict:
    if "PACKAGE-MANIFEST.json" in files:
        raise ValueError("PACKAGE-MANIFEST.json is generated; remove the stale manifest from build inputs")
    manifest = payload_manifest(files, kind)
    items = dict(files)
    items["PACKAGE-MANIFEST.json"] = canonical(manifest)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED,
                         allowZip64=True) as archive:
        for name, data in sorted(items.items()):
            item = zipfile.ZipInfo(f"{prefix}/{name}", date_time=STAMP)
            item.create_system = 3
            item.external_attr = (stat.S_IFREG | 0o644) << 16
            item.compress_type = zipfile.ZIP_STORED
            archive.writestr(item, data)
    # Verify the bytes we actually wrote, not only the input manifest.
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"Archive CRC failed: {bad}")
        expected = {f"{prefix}/{name}" for name in items}
        if len(archive.namelist()) != len(expected) or set(archive.namelist()) != expected:
            raise ValueError("Archive member set differs from declared payload")
        for name, data in items.items():
            if digest(archive.read(f"{prefix}/{name}")) != digest(data):
                raise ValueError(f"Archive bytes differ: {name}")
    return {"filename": path.name, "size_bytes": path.stat().st_size,
            "sha256": digest(path.read_bytes()),
            "payload_sha256": manifest["payload_sha256"],
            "payload_files": manifest["file_count"]}


def source_paths() -> list[Path]:
    """Validate every required selected root before reading any payload bytes."""
    checked_path(ROOT, directory=True)
    selected = []
    for name in sorted(SOURCE_FILES):
        path = ROOT / name
        checked_path(path, boundary=ROOT)
        selected.append(path)
    for name in sorted(SOURCE_DIRS):
        selected.extend(walk_files(ROOT / name, boundary=ROOT))
    checked_path(SKILL, directory=True, boundary=ROOT)
    return sorted(selected)


def source_files() -> dict[str, bytes]:
    return {path.relative_to(ROOT).as_posix(): regular_bytes(path, boundary=ROOT)
            for path in source_paths()}


def plugin_files(runtime: dict[str, bytes]) -> dict[str, bytes]:
    """Select this project's skills-only upload; never include repository evidence."""
    files = {f"skills/skill-builder/{name}": data for name, data in runtime.items()}
    for name in sorted({"plugin.json", "LICENSE.md", "NOTICE.md"} | PLUGIN_ASSETS):
        files[name] = regular_bytes(ROOT / name, boundary=ROOT)
    validate_plugin(files)
    return files


def validate_plugin(files: dict[str, bytes]) -> dict:
    """Bounded local package checks, not a portal scan or directory approval."""
    expected = {"plugin.json", "LICENSE.md", "NOTICE.md"} | PLUGIN_ASSETS
    runtime_prefix = "skills/skill-builder/"
    for name in files:
        if name not in expected and not name.startswith(runtime_prefix):
            raise ValueError("Unexpected plugin payload member")
        parts = name.split("/")
        if (any(part in {"", ".", ".."} for part in parts) or "\\" in name
                or any(ord(c) < 32 for c in name)):
            raise ValueError("Unsafe plugin member path")
    normalized = [unicodedata.normalize("NFC", n).casefold() for n in files]
    if len(set(normalized)) != len(normalized):
        raise ValueError("Colliding plugin member paths")
    if not expected <= files.keys() or runtime_prefix + "SKILL.md" not in files:
        raise ValueError("Missing required plugin payload")
    manifest = json.loads(files["plugin.json"])
    if not isinstance(manifest, dict):
        raise ValueError("Plugin manifest must be an object")
    version = regular_bytes(ROOT / "VERSION", boundary=ROOT).decode().strip()
    if (manifest.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
            or manifest.get("name") != "skill-builder" or manifest.get("version") != version
            or manifest.get("license") != "MIT"):
        raise ValueError("Plugin identity/version/license is inconsistent")
    extensions = manifest.get("extensions")
    extension = extensions.get("com.openai") if isinstance(extensions, dict) else None
    if not isinstance(extension, dict) or not isinstance(extension.get("interface"), dict):
        raise ValueError("Plugin OpenAI listing is missing")
    if (extension.get("requires_local_executor") is not True
            or any(k in manifest for k in ("apps", "skills", "mcpServers", "interface"))
            or extension.get("apps") is not None or "hooks" in extension):
        raise ValueError("Unexpected plugin integration or missing local executor declaration")
    interface = extension["interface"]
    for key, limit in (("displayName", 30), ("shortDescription", 30),
                       ("longDescription", 4000), ("developerName", 80)):
        value = interface.get(key)
        if (not isinstance(value, str) or not value.strip() or len(value) > limit
                or any(unicodedata.category(c) in {"Cc", "Cf", "Zl", "Zp"} for c in value)):
            raise ValueError("Invalid plugin listing text: " + key)
    if interface.get("category") != "Developer Tools" or interface["developerName"] != "Alex Allen":
        raise ValueError("Plugin category/publisher is inconsistent")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        raise ValueError("Invalid plugin starter prompts")
    normalized_prompts = []
    for prompt in prompts:
        if (not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 128
                or "@" in prompt or any(unicodedata.category(c) in {"Cc", "Cf", "Zl", "Zp"} for c in prompt)):
            raise ValueError("Invalid plugin starter prompt")
        normalized_prompts.append(" ".join(unicodedata.normalize("NFKC", prompt).split()).casefold())
    if len(set(normalized_prompts)) != len(prompts):
        raise ValueError("Duplicate plugin starter prompts")
    base = "https://github.com/altmn/skill-builder"
    urls = {"websiteURL": base, "supportURL": base + "/issues",
            "privacyPolicyURL": base + "/blob/master/PRIVACY.md",
            "termsOfServiceURL": base + "/blob/master/TERMS.md"}
    for key, expected_url in urls.items():
        value = interface.get(key, "")
        if not isinstance(value, str):
            raise ValueError("Invalid plugin listing URL: " + key)
        url = urlsplit(value)
        if (value != expected_url or len(value) > 1024 or url.scheme != "https"
                or url.username or url.password
                or any(c.isspace() or ord(c) < 32 for c in value)):
            raise ValueError("Invalid plugin listing URL: " + key)
    for key in ("logo", "composerIcon", "logoDark", "composerIconDark"):
        name = interface.get(key, "")
        if not isinstance(name, str) or not name.startswith("./") or name[2:] not in PLUGIN_ASSETS:
            raise ValueError("Invalid plugin icon reference")
        data = files[name[2:]]
        if len(data) < 33 or data[:16] != b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR":
            raise ValueError("Plugin icon must be PNG")
        width, height = struct.unpack(">II", data[16:24])
        if width != height or not 256 <= width <= 4096 or len(data) > 5 * 1024 * 1024:
            raise ValueError("Plugin icon dimensions/size exceed listing limits")
    review, publication = extension.get("review"), extension.get("publication")
    if (not isinstance(review, dict) or not isinstance(publication, dict)
            or review.get("commerce") is not False or publication.get("countries") != []):
        raise ValueError("Plugin commerce/country choices are inconsistent")
    kb = files.get(runtime_prefix + "references/knowledge-base.zip", b"")
    if digest(kb) != EXPECTED_KB_HASH:
        raise ValueError("Plugin knowledge archive identity is inconsistent")
    if len(files) + 1 > 5000 or sum(map(len, files.values())) > 512 * 1024 * 1024:
        raise ValueError("Plugin exceeds archive limits")
    return {"outcome": "passed", "scope": "Local project-specific plugin checks; URL reachability, PNG decoding, native activation and portal scans are separate."}


def prepare(output: Path) -> dict:
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("Output must be a new directory; existing content is preserved")
    parent = checked_path(output.parent, directory=True)
    output = parent / output.name
    project = checked_path(ROOT, directory=True)
    if any(output.is_relative_to(project / name) for name in SOURCE_DIRS):
        raise ValueError("Output must be outside every selected source directory (including nested dist directories)")
    # Validate all selected roots before reading version, runtime or source bytes.
    source_paths()
    version = regular_bytes(ROOT / "VERSION").decode().strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.]+)?", version):
        raise ValueError("Unexpected release version")
    if regular_bytes(SKILL / "VERSION").decode().strip() != version:
        raise ValueError("Runtime/project versions disagree")
    # Resolve all input bytes before creating the output tree.
    runtime = runtime_files()
    source = source_files()
    plugin = plugin_files(runtime)
    with tempfile.TemporaryDirectory(prefix=".skill-builder-release-", dir=output.parent) as temp:
        staging = Path(temp)
        runtime_result = make_zip(staging / f"skill-builder-{version}.zip",
                                  "skill-builder", runtime, "installable-skill")
        source_result = make_zip(staging / f"skill-builder-{version}-source.zip",
                                 f"skill-builder-{version}", source, "source-project")
        plugin_result = make_zip(staging / f"skill-builder-{version}-plugin.zip",
                                 "skill-builder", plugin, "openai-plugin")
        if plugin_result["size_bytes"] > 100_000_000:
            raise ValueError("Plugin ZIP exceeds the 100 MB upload limit")
        result = {
            "schema_version": "1.0.0", "version": version,
            "preparation": "passed", "publication": "not_run",
            "release_verdict": "PREPARED_UNPUBLISHED",
            "license": "MIT", "license_scope": license_metadata()["scope"],
            "blockers": [],
            "pending_actions": ["Configure actual private security-reporting route before public release",
                                "Run native host panels before claiming tested native support"],
            "limits": ["Native activation of these exact archives is not established; earlier trials remain historical",
                       "Checksums prove byte identity, not publisher authentication"],
            "archives": [runtime_result, source_result, plugin_result],
            "determinism": "ZIP_STORED, sorted names, fixed timestamp and regular-file mode; exact source bytes",
        }
        (staging / "build-receipt.json").write_bytes(canonical(result))
        checksums = "".join(f"{item['sha256']}  {item['filename']}\n"
                            for item in result["archives"])
        (staging / "SHA256SUMS").write_text(checksums, encoding="ascii")
        output.mkdir(mode=0o700)
        try:
            for path in sorted(staging.iterdir()):
                # Exclusive creation: never replace an unexpected competing file.
                with (output / path.name).open("xb") as handle:
                    handle.write(path.read_bytes())
        except BaseException:
            # Partial output is retained for inspection; no broad rollback/delete.
            raise
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New output directory (parent must exist)")
    parser.add_argument("--identity", action="store_true", help="Print runtime payload identity without writing")
    args = parser.parse_args()
    try:
        if args.identity:
            if args.output:
                parser.error("--identity and --output are mutually exclusive")
            print(json.dumps(payload_manifest(runtime_files(), "installable-skill"), indent=2))
        elif args.output:
            print(json.dumps(prepare(args.output.absolute()), indent=2))
        else:
            parser.error("Provide --output or --identity")
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
