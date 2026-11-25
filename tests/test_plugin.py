"""Observable upload inventory and malformed-metadata checks; no portal claims."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("plugin_release", ROOT / "tools/build_release.py")
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class PluginPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = release.plugin_files(release.runtime_files())

    def changed(self, mutate):
        files = self.payload.copy()
        manifest = json.loads(files["plugin.json"])
        mutate(manifest)
        files["plugin.json"] = json.dumps(manifest).encode()
        return files

    def test_upload_inventory_is_exact_and_kb_is_preserved(self):
        self.assertEqual(set(self.payload), {"plugin.json", "LICENSE.md", "NOTICE.md"}
                         | release.PLUGIN_ASSETS
                         | {"skills/skill-builder/" + n for n in release.runtime_files()})
        self.assertEqual(release.validate_plugin(self.payload)["outcome"], "passed")
        self.assertEqual(release.digest(self.payload["skills/skill-builder/references/knowledge-base.zip"]),
                         release.EXPECTED_KB_HASH)

    def test_wrong_version_and_nonobject_metadata_are_refused(self):
        with self.assertRaisesRegex(ValueError, "identity/version"):
            release.validate_plugin(self.changed(lambda m: m.update(version="99.0.0")))
        for value in ([], None, {"extensions": None}):
            files = self.payload.copy()
            files["plugin.json"] = json.dumps(value).encode()
            with self.assertRaises(ValueError):
                release.validate_plugin(files)

    def test_listing_limits_and_duplicate_prompts_are_refused(self):
        for change in ({"shortDescription": "x" * 31},
                       {"defaultPrompt": ["Same prompt", "Same   prompt"]},
                       {"defaultPrompt": ["First line\nSecond line"]},
                       {"termsOfServiceURL": "https://github.com/altmn/skill-builder-elsewhere"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.validate_plugin(self.changed(lambda m: m["extensions"]["com.openai"]["interface"].update(change)))

    def test_integrations_and_missing_executor_declaration_are_refused(self):
        for change in ({"apps": "./.app.json"}, {"requires_local_executor": False}, {"hooks": "./hooks/hooks.json"}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                release.validate_plugin(self.changed(lambda m: m["extensions"]["com.openai"].update(change)))

    def test_unrelated_traversal_and_colliding_members_are_refused(self):
        for name in (".app.json", "validation/private.log", "skills/skill-builder/../escape", "skills/skill-builder/skill.md"):
            files = self.payload.copy()
            files[name] = b"inert fixture"
            with self.subTest(name=name), self.assertRaises(ValueError):
                release.validate_plugin(files)

    def test_missing_bad_and_nonsquare_icons_are_refused(self):
        for mode in ("missing", "bad", "nonsquare"):
            files = self.payload.copy()
            if mode == "missing":
                files.pop("assets/icon.png")
            elif mode == "bad":
                files["assets/icon.png"] = b"not a PNG"
            else:
                data = bytearray(files["assets/icon.png"])
                data[20:24] = (300).to_bytes(4, "big")
                files["assets/icon.png"] = bytes(data)
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                release.validate_plugin(files)

    def test_packaged_runtime_creates_and_audits_another_skill_without_executing_it(self):
        with tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve()) as folder:
            root = Path(folder)
            release.make_zip(root / "plugin.zip", "skill-builder", self.payload, "openai-plugin")
            with zipfile.ZipFile(root / "plugin.zip") as archive:
                archive.extractall(root / "unpacked")
            runtime = root / "unpacked/skill-builder/skills/skill-builder"
            self.assertFalse((runtime / "tools").exists())
            script = runtime / "scripts/skill_builder.py"
            created, audited = root / "created", root / "audited"
            result = subprocess.run([sys.executable, "-I", "-B", str(script), "skill-builder-create",
                                     "--name", "publication-note-extractor", "--description",
                                     "Extract decisions from explicitly supplied local notes.",
                                     "--profile", "instruction", "--output", str(created)],
                                    cwd=root, capture_output=True, timeout=45)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            subject = created / "skills/publication-note-extractor"
            marker = root / "should-not-run"
            (subject / "setup.py").write_text("from pathlib import Path\nPath(" + repr(str(marker)) + ").touch()\n")
            before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in subject.iterdir()}
            result = subprocess.run([sys.executable, "-I", "-B", str(script), "skill-builder-audit",
                                     "--target", str(subject), "--profile", "instruction", "--output", str(audited)],
                                    cwd=root, capture_output=True, timeout=45)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads(result.stdout)
            self.assertFalse(summary["target_code_executed"])
            self.assertEqual(summary["audit_verdict"], "inconclusive")
            self.assertFalse(marker.exists())
            self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in subject.iterdir()})
            for output, mode in ((created, "create"), (audited, "audit")):
                review = json.loads((output / "evaluation-review.json").read_text())
                self.assertEqual(review["mode"], mode)
                self.assertFalse(review["semantic_review_performed"])
                self.assertTrue(all(i["outcome"] == "not_run" for i in review["items"]))


if __name__ == "__main__":
    unittest.main()
