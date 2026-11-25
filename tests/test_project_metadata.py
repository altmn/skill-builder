"""Exercise the actual project gate with alternate valid and invalid YAML."""
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("project_metadata_check", ROOT / "tools/check_project.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class ProjectMetadataTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temp.cleanup)
        self.skill = Path(self.temp.name) / "skill-builder"
        shutil.copytree(checker.SKILL, self.skill)
        self.body = (self.skill / "SKILL.md").read_text().split("\n---\n", 1)[1]
        self.helper = checker.load_module(checker.SKILL / "scripts/skill_builder.py", "metadata_helper")
        loader = checker.load_module
        self.addCleanup(mock.patch.stopall)
        mock.patch.object(checker, "SKILL", self.skill).start()
        mock.patch.object(checker, "load_module", side_effect=lambda p, n:
                          self.helper if p == self.skill / "scripts/skill_builder.py" else loader(p, n)).start()

    def run_gate(self, front):
        (self.skill / "SKILL.md").write_text("---\n" + front + "\n---\n" + self.body)
        result = checker.check()
        return result, {c["name"]: c["outcome"] for c in result["checks"]}

    def test_valid_reordered_optional_fields_and_folded_description_pass_project_gate(self):
        result, checks = self.run_gate('metadata:\n  version: "1.0.0-rc.2"\nlicense: MIT\n'
                                      'compatibility: Python 3.10+\ndescription: >-\n'
                                      '  Create and audit reusable agent skills.\n  Use for skill-building tasks.\n'
                                      'name: skill-builder')
        self.assertEqual(checks["portable_entrypoint"], "passed")
        self.assertEqual(result["outcome"], "passed", result["failed_checks"])

    def test_invalid_metadata_remains_a_failure(self):
        for front in ('name: skill-builder\ndescription: true',
                      'name: skill-builder\nname: skill-builder\ndescription: Review skills.',
                      'name: skill-builder\ndescription: Review skills.\nmetadata:\n  version: 1',
                      'name: skill-builder\ndescription: Review skills.\ncompatibility: ""',
                      'name: wrong-directory\ndescription: Review skills.',
                      'name: skill-builder\ndescription: Review skills.\nunknown-field: value'):
            with self.subTest(front=front):
                result, checks = self.run_gate(front)
                self.assertEqual(checks["portable_entrypoint"], "failed")
                self.assertEqual(result["outcome"], "failed")

    def test_missing_parser_is_blocked_in_both_metadata_records(self):
        with mock.patch.object(self.helper, "format_checks", return_value={"outcome": "blocked", "reason": "PyYAML unavailable"}):
            result = checker.check()
        checks = {c["name"]: c["outcome"] for c in result["checks"]}
        self.assertEqual(checks["portable_entrypoint"], "blocked")
        self.assertEqual(checks["original_portable_validator"], "blocked")


if __name__ == "__main__":
    unittest.main()
