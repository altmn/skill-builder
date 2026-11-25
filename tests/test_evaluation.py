"""Independent accounting contracts; synthetic traces are not native results."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/evaluate.py"
spec = importlib.util.spec_from_file_location("evaluation", SCRIPT)
evaluation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evaluation)


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.digest = "a" * 64
        self.plan_hash = "b" * 64
        snapshot = {"payload_sha256": self.digest, "skill_sha256": self.digest}
        self.plan = {"trials": 1, "identities": {"candidate": snapshot, "previous": snapshot},
                     "execution_conditions": ["no_skill", "explicit", "automatic", "previous"],
                     "corpus": {"routing": [{"id": "R", "prompt": "Create a skill", "split": "development", "should_trigger": True}],
                                "execution": [{"id": "E", "prompt": "Audit a skill", "split": "development", "checks": ["correct"], "invariants": ["safe"]}]}}
        self.counter = 0

    def reference(self, data):
        self.counter += 1
        name = f"evidence-{self.counter}.json"
        raw = json.dumps(data).encode()
        (self.root / name).write_bytes(raw)
        return {"path": name, "sha256": evaluation.builder.sha256(raw)}

    def run_record(self, suite="execution", condition="automatic", active=True, success=True, safe=True, trial=1):
        events = [{"kind": "skill_activation_succeeded", "skill_sha256": self.digest}] if active else []
        row = {"suite": suite, "case_id": "R" if suite == "routing" else "E", "condition": condition, "trial": trial,
               "status": "completed", "isolation_verified": True,
               "payload_sha256": None if condition == "no_skill" else self.digest,
               "trace": self.reference({"complete": True, "events": events}),
               "latency_seconds": 3, "input_tokens": None, "output_tokens": None, "cost_usd": None}
        if suite == "execution":
            row["checks"] = {"correct": {"passed": success, "evidence": "Compared actual answer to frozen oracle."},
                             "safe": {"passed": safe, "evidence": "Independent before/after input and effect check."}}
            row["artifacts"] = [self.reference({"answer": "actual result"})]
        return row

    def summarize(self, rows):
        return evaluation.summarize(self.plan, {"plan_sha256": self.plan_hash, "runs": rows}, self.root, self.plan_hash)

    def test_frozen_corpus_is_balanced_and_split_before_optimization(self):
        corpus = evaluation.validate_corpus({k: evaluation.read_json(ROOT / "evals" / (k + ".json")) for k in ("routing", "execution")})
        for split, count in (("development", 12), ("validation", 8)):
            cases = [c for c in corpus["routing"] if c["split"] == split]
            self.assertEqual(len(cases), count)
            self.assertEqual(sum(c["should_trigger"] for c in cases), count // 2)

    def test_known_confusion_matrix_and_undefined_metrics(self):
        result = evaluation.confusion([(True, True)] * 9 + [(True, False)] + [(False, True)] * 2 + [(False, False)] * 8)
        self.assertEqual([result[k] for k in ("tp", "fn", "fp", "tn")], [9, 1, 2, 8])
        self.assertAlmostEqual(result["precision"], 9 / 11)
        self.assertEqual(result["recall"], 0.9)
        self.assertEqual(result["false_activation_rate"], 0.2)
        self.assertIsNone(evaluation.confusion([])["f1"])

    def test_activation_requires_trace_event_and_matching_identity(self):
        self.assertFalse(evaluation.activation({"complete": True, "events": [{"kind": "answer", "text": "I used skill-builder"}]}, self.digest))
        self.assertIsNone(evaluation.activation({"complete": False, "events": []}, self.digest))
        self.assertIsNone(evaluation.activation({"complete": True, "events": [{"kind": "skill_activation_succeeded", "skill_sha256": "c" * 64}]}, self.digest))
        self.assertIsNone(evaluation.activation({"complete": True, "events": [{"kind": "skill_activation_failed"}]}, self.digest))

    def test_four_conditions_produce_matched_differences_not_best_attempt(self):
        rows = [self.run_record("routing"), self.run_record(condition="no_skill", active=False, success=False),
                self.run_record(condition="explicit"), self.run_record(), self.run_record(condition="previous", success=False)]
        result = self.summarize(rows)
        self.assertEqual(result["outcome"], "completed")
        self.assertEqual(result["paired_comparisons"]["explicit_minus_no_skill"]["success_rate_difference"], 1)
        self.assertEqual(result["paired_comparisons"]["explicit_minus_previous"]["matched_trials"], 1)
        self.assertIsNone(result["execution"]["explicit"]["cost_usd"]["mean"])

    def test_missing_runs_and_infrastructure_failure_never_become_true_negatives(self):
        row = self.run_record("routing")
        row.update(status="blocked", reason="Host unavailable", latency_seconds=10)
        result = self.summarize([row])
        self.assertEqual(result["outcome"], "incomplete")
        self.assertEqual(result["routing"]["development"]["trial_level"]["scored"], 0)
        self.assertEqual(len(result["missing"]), 4)

    def test_failed_attempt_usage_is_retained_and_unknown_is_not_zero(self):
        row = self.run_record()
        row.update(status="failed", reason="Infrastructure error", input_tokens=99)
        result = self.summarize([row])["execution"]["automatic"]
        self.assertEqual(result["scored"], 0)
        self.assertEqual(result["input_tokens"], {"mean": 99, "known": 1, "unknown": 0})
        self.assertEqual(result["cost_usd"]["unknown"], 1)

    def test_invariant_violation_cannot_be_offset_by_correct_answer(self):
        result = self.summarize([self.run_record(safe=False)])
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["execution"]["automatic"]["successes"], 0)
        self.assertEqual(result["execution"]["automatic"]["invariant_failures"], 1)
        self.assertIsNone(result["resource_usage"]["cost_usd"]["known_total"])

    def test_contaminated_control_is_unscored_and_unpaired(self):
        result = self.summarize([self.run_record(condition="no_skill"), self.run_record(condition="explicit")])
        self.assertEqual(result["execution"]["no_skill"]["scored"], 0)
        self.assertEqual(result["paired_comparisons"]["explicit_minus_no_skill"]["matched_trials"], 0)

    def test_incomplete_activation_cannot_hide_an_observed_invariant_failure(self):
        row = self.run_record(condition="explicit", active=False, safe=False)
        result = self.summarize([row])
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["scored"], 0)
        self.assertEqual(len(result["observed_invariant_failures"]), 1)

    def test_even_trial_tie_and_incomplete_query_are_unscored(self):
        self.plan["trials"] = 2
        result = self.summarize([self.run_record("routing", active=True, trial=1), self.run_record("routing", active=False, trial=2)])
        self.assertEqual(result["routing"]["development"]["trial_level"]["scored"], 2)
        self.assertEqual(result["routing"]["development"]["query_majority"]["scored"], 0)

    def test_duplicate_unexpected_and_wrong_plan_records_are_rejected(self):
        row = self.run_record()
        for rows in ([row, row], [{**row, "trial": 2}]):
            with self.assertRaises(ValueError):
                self.summarize(rows)
        with self.assertRaises(ValueError):
            evaluation.summarize(self.plan, {"plan_sha256": "wrong", "runs": []}, self.root, self.plan_hash)

    def test_tampered_and_escaping_evidence_and_changed_check_set_are_rejected(self):
        row = self.run_record()
        (self.root / row["trace"]["path"]).write_text("tampered")
        with self.assertRaises(ValueError):
            self.summarize([row])
        row = self.run_record()
        row["artifacts"][0]["path"] = "../outside"
        with self.assertRaises(ValueError):
            self.summarize([row])
        row = self.run_record()
        row["checks"].pop("safe")
        with self.assertRaises(ValueError):
            self.summarize([row])

    def test_invalid_metrics_and_labels_are_rejected(self):
        for value in (True, -1, float("inf")):
            row = self.run_record()
            row["cost_usd"] = value
            with self.assertRaises(ValueError):
                self.summarize([row])
        corpus = copy.deepcopy(self.plan["corpus"])
        corpus["routing"][0]["should_trigger"] = "false"
        with self.assertRaises(ValueError):
            evaluation.validate_corpus(corpus)

    def test_malformed_plan_or_observation_containers_cannot_report_zero_test_completion(self):
        for observations in ([], {"plan_sha256": self.plan_hash, "runs": [None]}):
            with self.assertRaises(ValueError):
                evaluation.summarize(self.plan, observations, self.root, self.plan_hash)
        self.plan["trials"] = 0
        with self.assertRaises(ValueError):
            self.summarize([])

    def test_prepare_freezes_identities_fixtures_and_budget_without_running_agents(self):
        candidate = self.root / "candidate"
        candidate.mkdir()
        (candidate / "SKILL.md").write_text("instructions")
        env = self.root / "environment.json"
        env.write_text(json.dumps({"host": "synthetic test", "model": "fixture", "settings": {"sampling": "fixed"},
                                   "policy": "read-only", "catalog_sha256": self.digest,
                                   "budget": {"max_runs": 100, "per_run_seconds": 30, "semantic_retries": 0}}))
        output = self.root / "panel"
        args = [sys.executable, "-I", "-B", str(SCRIPT), "prepare", "--candidate", str(candidate),
                "--previous", str(candidate), "--environment", str(env), "--output", str(output)]
        result = subprocess.run(args, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout)
        plan = json.loads((output / "plan.json").read_text())
        self.assertEqual(len(evaluation.schedule(plan)), 96)
        self.assertTrue(plan["corpus"]["execution"][1]["fixture_identities"])
        self.assertEqual(subprocess.run(args, capture_output=True, timeout=30).returncode, 2)
        report = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "summarize", "--plan", str(output / "plan.json"),
                                 "--observations", str(output / "observations.json")], capture_output=True, timeout=30)
        self.assertEqual(report.returncode, 3)
        self.assertEqual(json.loads(report.stdout)["scored"], 0)


if __name__ == "__main__":
    unittest.main()
