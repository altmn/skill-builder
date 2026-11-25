#!/usr/bin/env python3
"""Check that selected release files are present in the Git index.

Read-only repository maintenance check; no fetch, hooks, installation or commit.
Run before a source release from a Git checkout. A packaged tree without Git
metadata must use the package manifest instead; it cannot pass this Git check.
Index membership does not prove staged bytes equal working bytes or a commit.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).absolute().parents[1]


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(root), *arguments],
        capture_output=True, timeout=30,
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    if result.returncode:
        raise ValueError("Git metadata is unavailable or the index could not be read.")
    return os.fsdecode(result.stdout)


def compare_index(root: Path, selected_paths: list[Path],
                  source_files: set[str], source_dirs: set[str]) -> dict:
    root = root.resolve(strict=True)
    actual_root = Path(git(root, "rev-parse", "--show-toplevel").removesuffix("\n")).resolve(strict=True)
    if actual_root != root:
        raise ValueError("The selected source root must be the Git checkout root.")
    indexed = set(git(root, "ls-files", "--cached", "-z").split("\0")) - {""}
    selected = {path.relative_to(root).as_posix() for path in selected_paths}
    missing_from_index = sorted(selected - indexed)
    selected_indexed = {name for name in indexed
                        if name in source_files or Path(name).parts[0] in source_dirs}
    missing_from_worktree = sorted(name for name in selected_indexed
                                   if not (root / name).is_file())
    return {
        "schema_version": "1.0.0",
        "outcome": "failed" if missing_from_index or missing_from_worktree else "passed",
        "scope": "Git index membership and presence of selected source-release inputs only.",
        "selected_files": len(selected),
        "missing_from_git_index": missing_from_index,
        "indexed_files_missing_from_worktree": missing_from_worktree,
        "not_established": ["Index/working-byte equality", "committed or published state",
                            "evidence truth", "native host support"],
    }


def check() -> dict:
    # Execute only this reviewed repository's declared build-input selector.
    # The selector checks selected roots/ancestors before reading payload bytes.
    source = ROOT / "tools/build_release.py"
    for component in (source, *source.parents):
        if component.is_symlink():
            raise ValueError("Build-input selector paths must not contain symlinks.")
    spec = importlib.util.spec_from_file_location("skill_builder_inventory_release", source)
    if spec is None or spec.loader is None:
        raise ValueError("The build-input selector could not be loaded.")
    release = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(release)
    paths = release.source_paths()
    return compare_index(ROOT, paths, release.SOURCE_FILES, release.SOURCE_DIRS)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not sys.flags.isolated:
        parser.error("Use python3 -I -B for isolated execution")
    try:
        result = check()
    except (OSError, ValueError, subprocess.TimeoutExpired):
        result = {"schema_version": "1.0.0", "outcome": "blocked",
                  "error": "Cannot establish the selected Git inventory; inspect checkout metadata and input boundaries."}
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 2 if result["outcome"] == "blocked" else 1 if result["outcome"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
