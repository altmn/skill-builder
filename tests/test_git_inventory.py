"""Release evidence must survive a Git checkout, including ignored log names."""
from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("git_inventory", ROOT / "tools/check_git_inventory.py")
assert spec and spec.loader
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class GitInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="git inventory ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.git("init", "--quiet", "--template=")
        self.path = self.root / "validation/result.log"
        self.path.parent.mkdir()
        self.path.write_bytes(b"Retained test evidence.\n")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True, timeout=30,
                              env={**os.environ, "GIT_CONFIG_NOSYSTEM": "1",
                                   "GIT_CONFIG_GLOBAL": os.devnull})

    def compare(self, paths=None):
        return inventory.compare_index(self.root, [self.path] if paths is None else paths,
                                       {"README.md"}, {"validation"})

    def test_ignored_local_evidence_cannot_pass_as_git_release_input(self):
        excludes = self.root / "global-ignore"
        excludes.write_text("*.log\n")
        self.git("config", "core.excludesfile", str(excludes))
        self.git("add", "--all")
        result = self.compare()
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["missing_from_git_index"], ["validation/result.log"])
        self.git("add", "--force", "--", "validation/result.log")
        self.assertEqual(self.compare()["outcome"], "passed")

    def test_project_unignore_overrides_global_log_ignore(self):
        excludes = self.root / "global-ignore"
        excludes.write_text("*.log\n")
        self.git("config", "core.excludesfile", str(excludes))
        (self.root / ".gitignore").write_bytes((ROOT / ".gitignore").read_bytes())
        self.git("add", "--", ".gitignore", "validation/result.log")
        self.assertEqual(self.compare()["outcome"], "passed")

    def test_indexed_missing_evidence_is_reported(self):
        self.git("add", "--force", "--", "validation/result.log")
        self.path.unlink()
        result = self.compare([])
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["indexed_files_missing_from_worktree"], ["validation/result.log"])

    def test_packaged_tree_without_git_is_unavailable(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            # A runner may put temporary files beneath a different checkout;
            # ancestor metadata must not qualify this packaged tree either.
            with self.assertRaises(ValueError):
                inventory.compare_index(root, [], set(), set())


if __name__ == "__main__":
    unittest.main()
