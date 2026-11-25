"""Git-bound review requirements, including stale records and unstaged changes."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("workflow_impact", ROOT / "tools/check_workflow_impact.py")
impact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(impact)


class WorkflowImpactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        patch = mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"})
        patch.start()
        self.addCleanup(patch.stop)
        self.git("init", "--quiet", "--template=")
        self.write("owner.md", "Existing downstream procedure.\n")
        self.write("evidence.txt", "Independent result retained.\n")
        self.git("add", ".")
        self.commit()
        self.base = self.git("rev-parse", "HEAD").decode().strip()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.PIPE)

    def commit(self):
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "commit", "--quiet", "-m", "fixture")

    def write(self, path, content):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def record(self, paths=None):
        mode = {"decision": "no_change_needed", "reason": "Maintenance change leaves the domain procedure unchanged.",
                "owners": ["owner.md"], "verification": {"status": "not_applicable",
                    "reason": "No domain behavior or output contract changes in this fixture.",
                    "consequence": "No new domain claims or host support evidence is asserted."}}
        return {"schema_version": "1.0.0", "summary": "Assess downstream effects of this isolated fixture change.",
                "reviewed_paths": paths or ["change.txt"],
                "workflows": {"create": mode, "audit": json.loads(json.dumps(mode))}}

    def stage_review(self, record=None, path="docs/change-impact/new.json"):
        self.write(path, json.dumps(record or self.record()))
        self.git("add", "--", path)

    def change(self):
        self.write("change.txt", "New change.\n")
        self.git("add", "--", "change.txt")

    def test_changed_files_without_fresh_review_fail(self):
        self.change()
        result = impact.check(self.root)
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["unreviewed_paths"], ["change.txt"])

    def test_reasoned_no_change_decisions_pass_without_forcing_domain_edits(self):
        self.change()
        self.stage_review()
        result = impact.check(self.root)
        self.assertEqual(result["outcome"], "passed")
        self.assertEqual(len(result["unresolved_verification"]), 2)

    def test_missing_audit_decision_or_placeholder_is_blocked(self):
        self.change()
        record = self.record()
        record["workflows"].pop("audit")
        self.stage_review(record)
        with self.assertRaises(ValueError):
            impact.check(self.root)
        record = self.record()
        record["workflows"]["audit"]["reason"] = "REPLACE with actual reasoning before proceeding."
        self.stage_review(record)
        with self.assertRaises(ValueError):
            impact.check(self.root)

    def test_stale_existing_record_cannot_cover_new_change(self):
        self.stage_review()
        self.commit()
        self.change()
        self.assertEqual(impact.check(self.root)["outcome"], "failed")

    def test_rewriting_or_deleting_prior_record_is_refused(self):
        self.stage_review()
        self.commit()
        self.stage_review(self.record(["other.txt"]))
        with self.assertRaisesRegex(ValueError, "append-only"):
            impact.check(self.root)
        self.git("reset", "--hard", "--quiet", "HEAD")
        self.git("rm", "--quiet", "docs/change-impact/new.json")
        with self.assertRaisesRegex(ValueError, "append-only"):
            impact.check(self.root)

    def test_uncovered_second_path_remains_a_failure(self):
        self.change()
        self.write("second.txt", "Another change\n")
        self.git("add", "second.txt")
        self.stage_review()
        self.assertEqual(impact.check(self.root)["unreviewed_paths"], ["second.txt"])

    def test_pass_requires_existing_evidence_and_commands(self):
        self.change()
        record = self.record()
        record["workflows"]["create"]["verification"] = {
            "status": "passed", "reason": "Independent offline verification passed against the fixture.",
            "commands": ["reviewed fixture command"], "evidence": ["missing.txt"]}
        self.stage_review(record)
        with self.assertRaises(ValueError):
            impact.check(self.root)
        record["workflows"]["create"]["verification"]["evidence"] = ["evidence.txt"]
        self.stage_review(record)
        self.assertEqual(impact.check(self.root)["outcome"], "passed")

    def test_staged_bytes_are_checked_instead_of_unstaged_working_record(self):
        self.change()
        self.stage_review()
        self.write("docs/change-impact/new.json", "broken working bytes")
        self.assertEqual(impact.check(self.root)["outcome"], "passed")

    def test_committed_base_and_ci_event_check_the_complete_range(self):
        self.change()
        self.stage_review()
        self.commit()
        self.assertEqual(impact.check(self.root, base=self.base)["outcome"], "passed")
        self.assertEqual(impact.check(self.root, event={"pull_request": {"base": {"sha": self.base}}})["outcome"], "passed")
        self.assertEqual(impact.check(self.root, event={"before": self.base})["outcome"], "passed")
        self.assertEqual(impact.ci_base(self.root, {"before": "0" * 40}), self.base)

    def test_updated_decision_needs_reviewed_owner_and_blocked_status_needs_consequence(self):
        self.change()
        record = self.record()
        record["workflows"]["create"]["decision"] = "updated"
        self.stage_review(record)
        with self.assertRaises(ValueError):
            impact.check(self.root)
        record = self.record()
        record["workflows"]["audit"]["verification"].pop("consequence")
        self.stage_review(record)
        with self.assertRaises(ValueError):
            impact.check(self.root)

    def test_duplicate_json_keys_cannot_hide_missing_decision(self):
        self.change()
        self.write("docs/change-impact/new.json", '{"schema_version":"1.0.0","schema_version":"1.0.0"}')
        self.git("add", "docs/change-impact/new.json")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            impact.check(self.root)


if __name__ == "__main__":
    unittest.main()
