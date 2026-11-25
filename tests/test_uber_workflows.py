"""Offline workflow contracts on separate subjects; no model or native-host claims."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/skill-builder"


def load(name):
    spec = importlib.util.spec_from_file_location("uber_test_" + name, SKILL / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


evaluation, review, ablation = (load(name) for name in ("evaluate", "review", "ablate"))


class UberWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.counter = 0

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value if isinstance(value, bytes) else
                         value.encode() if isinstance(value, str) else evaluation.builder.json_bytes(value))
        return path

    def reference(self, value, root=None):
        self.counter += 1
        base = root or self.root
        name = f"evidence-{self.counter}.json"
        raw = value if isinstance(value, bytes) else evaluation.builder.json_bytes(value)
        (base / name).write_bytes(raw)
        return {"path": name, "sha256": hashlib.sha256(raw).hexdigest()}

    def rules(self):
        return {"required": ["read_ticket", "verify_label"], "forbidden": ["send_reply"],
                "before": [["read_ticket", "verify_label"]]}

    def action(self, name, outcome="succeeded"):
        return {"kind": "action", "name": name, "outcome": outcome}

    def panel(self, variants=True, trajectories=False):
        subject = self.write("invoice-labeler/SKILL.md", "# Invoice labeler\nReturn the invoice category; never send a reply.\n").parent
        short = self.write("concise/SKILL.md", "# Invoice labeler\nReturn category only; do not reply.\n").parent
        routing = self.write("cases/routing.json", [
            {"id": "R-DEV", "split": "development", "prompt": "Classify this invoice question.", "should_trigger": True},
            {"id": "R-HELD", "split": "validation", "prompt": "Do not classify; translate this.", "should_trigger": False}])
        execution = [{"id": case_id, "split": split, "prompt": prompt, "fixtures": [],
                      "checks": ["label"], "invariants": ["no_reply"]}
                     for case_id, split, prompt in (("E-DEV", "development", "Label the supplied invoice question."),
                                                   ("E-HELD", "validation", "Report missing ticket text."))]
        if trajectories:
            for case in execution:
                case["trajectory"] = self.rules()
        execution_path = self.write("cases/execution.json", execution)
        environment = self.write("cases/environment.json", {
            "host": "synthetic local accounting fixture", "model": "not invoked",
            "settings": {"tools": "none"}, "policy": "target is inert data",
            "catalog_sha256": "a" * 64, "budget": {"max_runs": 40, "per_run_seconds": 30, "semantic_retries": 0}})
        variant_path = self.write("variants.json", {"short": str(short), "repeat": str(subject)}) if variants else None
        return evaluation.prepare(subject, None, environment, 1, "all", routing_cases=routing,
                                  execution_cases=execution_path, fixtures_root=routing.parent,
                                  variants=variant_path)

    def rows(self, plan):
        rows = []
        for (suite, case_id, condition, trial), case in evaluation.schedule(plan).items():
            active = case["should_trigger"] if suite == "routing" else condition != "no_skill"
            identity = plan.get("variants", {}).get(condition, plan["identities"]["candidate"])
            events = [{"kind": "skill_activation_succeeded", "skill_sha256": identity["skill_sha256"]}] if active else []
            if suite == "execution":
                events.extend([self.action("read_ticket"), self.action("verify_label")])
            row = {"suite": suite, "case_id": case_id, "condition": condition, "trial": trial,
                   "status": "completed", "isolation_verified": True,
                   "payload_sha256": identity["payload_sha256"] if condition != "no_skill" else None,
                   "trace": self.reference({"complete": True, "events": events})}
            if suite == "execution":
                row["checks"] = {name: {"passed": True, "evidence": "Known inert fixture oracle; no host/model invoked."}
                                 for name in case["checks"] + case["invariants"]}
                row["artifacts"] = [self.reference(b"Category: billing\n")]
            rows.append(row)
        return rows

    def summary(self, plan, rows):
        return evaluation.summarize(plan, {"plan_sha256": "b" * 64, "runs": rows}, self.root, "b" * 64)

    def bundle(self, unsafe=False, incomplete=False):
        plan = self.panel()
        rows = self.rows(plan)
        if unsafe:
            next(r for r in rows if r["suite"] == "execution" and r["condition"] == "short")["checks"]["no_reply"]["passed"] = False
        if incomplete:
            rows = [r for r in rows if r["suite"] == "execution"]
        plan_path = self.write("plan.json", plan)
        observation_path = self.write("observations.json", {"plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(), "runs": rows})
        output = self.root / "blind"
        result = ablation.blind(plan_path, observation_path, output)
        return output, result

    def judgments(self, output, preference="tie"):
        record = json.loads((output / "judgments.json.template").read_text())
        record["grader"] = "Independent synthetic fixture reviewer v1"
        record["calibration"] = self.reference({"calibrated": "known synthetic preferences"}, output)
        for row in record["judgments"]:
            row.update(preference=preference, evidence="Compared actual fixture artifacts against the frozen rubric.")
        path = output / "judgments.json"
        path.write_bytes(evaluation.builder.json_bytes(record))
        return path

    def test_trajectory_checks_success_order_and_equivalent_extra_actions(self):
        events = [self.action("read_ticket"), self.action("optional_lookup"), self.action("verify_label")]
        self.assertEqual(evaluation.trajectory({"complete": True, "events": events}, self.rules())["outcome"], "passed")
        events = [self.action("verify_label"), self.action("read_ticket")]
        result = evaluation.trajectory({"complete": True, "events": events}, self.rules())
        self.assertEqual(result["ordering_violations"], [["read_ticket", "verify_label"]])
        self.assertEqual(result["outcome"], "failed")
        events = [self.action("read_ticket", "failed"), self.action("verify_label")]
        self.assertIn("read_ticket", evaluation.trajectory({"complete": True, "events": events}, self.rules())["missing_required"])

    def test_incomplete_trajectory_stays_unknown_but_forbidden_attempt_cannot_pass(self):
        result = evaluation.trajectory({"complete": False, "events": []}, self.rules())
        self.assertEqual(result["outcome"], "inconclusive")
        self.assertIsNone(result["missing_required"])
        for outcome in ("succeeded", "failed", "denied"):
            result = evaluation.trajectory({"complete": False, "events": [self.action("send_reply", outcome)]}, self.rules())
            self.assertEqual(result["outcome"], "failed")
            self.assertEqual(result["forbidden_observed"], ["send_reply"])

    def test_optional_successor_has_no_order_requirement_and_malformed_rules_are_refused(self):
        rules = {"required": [], "forbidden": [], "before": [["read_ticket", "optional_write"]]}
        self.assertEqual(evaluation.trajectory({"complete": True, "events": []}, rules)["outcome"], "passed")
        for invalid in ({**rules, "required": ["same", "same"]},
                        {**rules, "required": ["x"], "forbidden": ["x"]},
                        {**rules, "before": [["x", "x"]]}):
            with self.assertRaises(ValueError):
                evaluation.validate_trajectory(invalid)

    def test_trajectory_failure_is_separate_from_correct_answer_and_survives_unknown_activation(self):
        plan = self.panel(variants=False, trajectories=True)
        rows = self.rows(plan)
        row = next(r for r in rows if r["suite"] == "execution" and r["condition"] == "explicit")
        row["trace"] = self.reference({"complete": True, "events": [
            {"kind": "skill_activation_succeeded", "skill_sha256": plan["identities"]["candidate"]["skill_sha256"]},
            self.action("verify_label"), self.action("read_ticket")]})
        result = self.summary(plan, rows)
        self.assertEqual(result["execution"]["explicit"]["successes"], 2)
        self.assertEqual(result["outcome"], "failed")
        row["trace"] = self.reference({"complete": False, "events": [self.action("send_reply")]})
        result = self.summary(plan, rows)
        self.assertEqual(result["execution"]["explicit"]["scored"], 1)
        self.assertEqual(result["outcome"], "failed")
        self.assertTrue(any(t["forbidden_observed"] for t in result["trajectories"]))

    def test_named_variant_identity_schedule_and_matched_comparisons(self):
        plan = self.panel()
        self.assertEqual(plan["execution_conditions"], ["no_skill", "explicit", "automatic", "short", "repeat"])
        self.assertEqual(len(evaluation.schedule(plan)), 12)
        self.assertEqual(plan["variants"]["repeat"]["payload_sha256"], plan["identities"]["candidate"]["payload_sha256"])
        self.assertNotEqual(plan["variants"]["short"]["skill_sha256"], plan["identities"]["candidate"]["skill_sha256"])
        result = self.summary(plan, self.rows(plan))
        self.assertEqual(result["paired_comparisons"]["short_minus_explicit"], {"matched_trials": 2, "success_rate_difference": 0})
        rows = self.rows(plan)
        next(r for r in rows if r["condition"] == "short")["payload_sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            self.summary(plan, rows)

    def test_reserved_relative_and_oversized_variant_definitions_are_rejected(self):
        self.panel()
        variants = self.root / "variants.json"
        subject = self.root / "invoice-labeler"
        for definitions in ({"explicit": str(subject)}, {"short": "relative/path"},
                            {f"v{i}": str(subject) for i in range(5)}):
            variants.write_bytes(evaluation.builder.json_bytes(definitions))
            with self.subTest(definitions=definitions), self.assertRaises(ValueError):
                evaluation.prepare(subject, None, self.root / "cases/environment.json", 1, "all",
                                   routing_cases=self.root / "cases/routing.json",
                                   execution_cases=self.root / "cases/execution.json",
                                   fixtures_root=self.root / "cases", variants=variants)

    def test_counters_need_integer_measures_and_sources_and_unknown_is_retained(self):
        plan = self.panel(variants=False)
        rows = self.rows(plan)
        row = next(r for r in rows if r["suite"] == "execution")
        row.update(tool_calls=3, metric_sources={"tool_calls": "independent host event count"})
        result = self.summary(plan, rows)
        self.assertEqual(result["resource_usage"]["tool_calls"], {"known_total": 3, "known": 1, "unknown": len(rows) - 1})
        for invalid in ({"tool_calls": 2.5}, {"tool_calls": True}, {"metric_sources": {}}, {"metric_sources": []}):
            changed = copy.deepcopy(rows)
            changed[rows.index(row)].update(invalid)
            with self.assertRaises(ValueError):
                self.summary(plan, changed)

    def test_blind_bundle_uses_neutral_files_and_scores_identical_payload_ties(self):
        output, result = self.bundle()
        self.assertEqual(result["pairs"], 4)
        public = json.loads((output / "pairs.json").read_text())
        self.assertNotIn("short", json.dumps(public))
        self.assertNotIn("repeat", json.dumps(public))
        for pair in public["pairs"]:
            for side in ("left", "right"):
                self.assertEqual(evaluation.evidence(output, pair[side][0]), b"Category: billing\n")
        result = ablation.score(output / "key.json", self.judgments(output))
        self.assertEqual(result["outcome"], "completed")
        self.assertEqual(result["comparisons"]["repeat_vs_explicit"]["identical_payload_pairs"], 2)
        self.assertEqual(result["comparisons"]["short_vs_explicit"]["ties"], 2)
        with self.assertRaises(ValueError):
            ablation.blind(self.root / "plan.json", self.root / "observations.json", output)

    def test_blind_preferences_preserve_unknown_missing_and_unsafe_panel(self):
        output, _ = self.bundle(unsafe=True)
        path = self.judgments(output, "left")
        result = ablation.score(output / "key.json", path)
        self.assertEqual(result["outcome"], "failed")
        self.assertTrue(result["invariant_failures"])
        record = json.loads(path.read_text())
        record["judgments"].pop()
        record["judgments"][0]["preference"] = "unknown"
        path.write_bytes(evaluation.builder.json_bytes(record))
        result = ablation.score(output / "key.json", path)
        self.assertEqual(len(result["missing"]), 1)
        self.assertEqual(len(result["unknown"]), 1)
        self.assertEqual(result["outcome"], "failed")

    def test_whole_skill_ablation_blinds_clean_no_skill_artifacts(self):
        plan = self.panel(variants=False)
        plan_path = self.write("plan.json", plan)
        observations = self.write("observations.json", {"plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
                                                       "runs": self.rows(plan)})
        output = self.root / "whole skill"
        self.assertEqual(ablation.blind(plan_path, observations, output, ["no_skill"])["pairs"], 2)
        result = ablation.score(output / "key.json", self.judgments(output))
        self.assertEqual(result["comparisons"]["no_skill_vs_explicit"]["ties"], 2)
        self.assertEqual(result["comparisons"]["no_skill_vs_explicit"]["identical_payload_pairs"], 0)

    def test_field_cases_bind_historical_sources_fixtures_and_independent_oracles(self):
        root = ROOT / "evals/field"
        corpus = evaluation.validate_corpus({kind: evaluation.read_json(root / (kind + ".json"))
                                             for kind in ("routing", "execution")})
        self.assertEqual({c["split"] for c in corpus["execution"]}, {"development", "validation"})
        for case in corpus["execution"]:
            self.assertEqual(set(case["oracle"]), set(case["checks"] + case["invariants"]))
            for reference in case["provenance"]["source_files"]:
                self.assertEqual(hashlib.sha256((ROOT / reference["path"]).read_bytes()).hexdigest(), reference["sha256"])
            for fixture in case["fixtures"]:
                self.assertTrue((root / fixture).is_file())
                self.assertTrue(fixture.endswith(".fixture"))

    def test_safe_panel_with_unknown_or_missing_preferences_stays_incomplete(self):
        output, _ = self.bundle()
        path = self.judgments(output)
        record = json.loads(path.read_text())
        record["judgments"].pop()
        record["judgments"][0]["preference"] = "unknown"
        path.write_bytes(evaluation.builder.json_bytes(record))
        result = ablation.score(output / "key.json", path)
        self.assertEqual(result["outcome"], "incomplete")
        self.assertEqual(len(result["missing"]), 1)
        self.assertEqual(len(result["unknown"]), 1)

    def test_blind_export_caps_count_and_total_bytes_before_creating_output(self):
        output, _ = self.bundle()
        for constant in ("MAX_ARTIFACTS", "MAX_COPY_BYTES"):
            destination = self.root / constant.lower()
            with self.subTest(limit=constant), mock.patch.object(ablation, constant, 1):
                with self.assertRaises(ValueError):
                    ablation.blind(self.root / "plan.json", self.root / "observations.json", destination)
            self.assertFalse(destination.exists())

    def test_incomplete_panel_remains_incomplete_and_artifact_or_key_tampering_is_rejected(self):
        output, _ = self.bundle(incomplete=True)
        path = self.judgments(output)
        self.assertEqual(ablation.score(output / "key.json", path)["outcome"], "incomplete")
        record = json.loads(path.read_text())
        record["key_sha256"] = "0" * 64
        path.write_bytes(evaluation.builder.json_bytes(record))
        with self.assertRaises(ValueError):
            ablation.score(output / "key.json", path)
        path = self.judgments(output)
        public = json.loads((output / "pairs.json").read_text())
        (output / public["pairs"][0]["left"][0]["path"]).write_text("changed output")
        with self.assertRaises(ValueError):
            ablation.score(output / "key.json", path)

    def contract_fixture(self):
        owner = self.write("refund-labeler/SKILL.md", "Return the refund category. Never send customer messages.\n")
        cases_path = self.write("contract-cases.json", [{"id": "C1", "checks": ["category"], "invariants": ["no_message"]}])
        record = {"schema_version": "1.0.0", "record_type": "workflow-contract", "goal": "Classify refund requests",
                  "outputs": ["category"], "requirements": [
                      {"id": "OUTPUT", "kind": "output", "statement": "Return a category.",
                       "owner": {"path": "SKILL.md", "sha256": hashlib.sha256(owner.read_bytes()).hexdigest()},
                       "verification": [{"case_id": "C1", "check_id": "category"}]},
                      {"id": "BOUNDARY", "kind": "forbidden_action", "statement": "Do not send messages.",
                       "owner": {"path": "SKILL.md", "sha256": hashlib.sha256(owner.read_bytes()).hexdigest()},
                       "verification": [{"case_id": "C1", "check_id": "no_message"}]}]}
        return owner.parent, cases_path, record

    def test_contract_detects_owner_drift_without_rewriting_subject(self):
        target, path, record = self.contract_fixture()
        cases = review.case_index(path)
        self.assertEqual(review.contract(record, target, cases)["outcome"], "passed")
        (target / "SKILL.md").write_text("Changed instructions.\n")
        result = review.contract(record, target, cases)
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual({d["code"] for d in result["diagnostics"]}, {"owner_drift"})
        self.assertEqual((target / "SKILL.md").read_text(), "Changed instructions.\n")

    def test_contract_refuses_unknown_checks_duplicate_ids_forbidden_mapping_and_escapes(self):
        target, path, record = self.contract_fixture()
        for mutation in ("unknown", "duplicate", "ordinary", "escape"):
            bad = copy.deepcopy(record)
            if mutation == "unknown":
                bad["requirements"][0]["verification"][0]["check_id"] = "absent"
            elif mutation == "duplicate":
                bad["requirements"][1]["id"] = "OUTPUT"
            elif mutation == "ordinary":
                bad["requirements"][1]["verification"][0]["check_id"] = "category"
            else:
                bad["requirements"][0]["owner"]["path"] = "../private.txt"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                review.contract(bad, target, review.case_index(path))

    def test_papercut_resolution_needs_independent_identity_bound_regression(self):
        _, path, _ = self.contract_fixture()
        cases = review.case_index(path)
        record = {"schema_version": "1.0.0", "record_type": "skill-papercut", "id": "INC1",
                  "subject": "refund-labeler", "version": "fixed-v2", "attempted": "Classify missing text",
                  "expected": "Report missing input", "observed": "Fabricated a label", "owner": "task instructions",
                  "dedup_key": "missing-input-label", "status": "open", "evidence": [], "regression": None}
        self.assertEqual(review.papercut(record, self.root, cases)["status"], "open")
        record["status"] = "resolved"
        with self.assertRaises(ValueError):
            review.papercut(record, self.root, cases)
        record["evidence"] = [self.reference({"affected_version": "v1", "observed": "known synthetic failure"})]
        receipt = {"case_id": "C1", "outcome": "passed", "subject_version": "fixed-v2", "independent_checker": "fixture oracle v1"}
        record["regression"] = {"case_id": "C1", "receipt": self.reference(receipt)}
        self.assertEqual(review.papercut(record, self.root, cases)["status"], "resolved")
        receipt["subject_version"] = "unrelated-v1"
        record["regression"]["receipt"] = self.reference(receipt)
        with self.assertRaises(ValueError):
            review.papercut(record, self.root, cases)

    def test_linter_returns_advisory_locations_and_does_not_execute_commands(self):
        marker = self.root / "never-created"
        flawed = self.write("flawed.md", "# Workflow\n\n## Step 1\n```sh\npython touch_marker.py\n```\nTry again\n")
        self.write("touch_marker.py", f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
        result = review.lint(flawed)
        self.assertEqual(result["outcome"], "advisory")
        self.assertEqual({d["code"] for d in result["diagnostics"]}, {"completion_condition", "command_result", "recovery"})
        self.assertEqual(result["source_sha256"], hashlib.sha256(flawed.read_bytes()).hexdigest())
        self.assertFalse(marker.exists())
        complete = self.write("complete.md", "## Step 1\nRead explicit ticket text; return a missing-input report when absent.\n")
        self.assertEqual(review.lint(complete)["diagnostics"], [])

    def test_runtime_only_cli_checks_another_subject_with_spaces_unicode_and_denied_paths(self):
        installed = self.root / "standalone runtime"
        shutil.copytree(SKILL, installed)
        target, cases, record = self.contract_fixture()
        spaced = self.root / "refund subject café"
        target.rename(spaced)
        marker = self.root / "target-executed"
        (spaced / "setup.py").write_text(f"from pathlib import Path\nPath({str(marker)!r}).touch()\n")
        record_path = self.write("review records/contract.json", record)
        before = {p.name: p.read_bytes() for p in spaced.iterdir()}
        command = [sys.executable, "-I", "-B", "-S", str(installed / "scripts/review.py"), "contract",
                   "--record", str(record_path), "--target", str(spaced), "--execution-cases", str(cases)]
        result = subprocess.run(command, cwd=self.root, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["outcome"], "passed")
        record["requirements"][0]["owner"]["path"] = "../outside"
        record_path.write_bytes(evaluation.builder.json_bytes(record))
        result = subprocess.run(command, cwd=self.root, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertEqual(json.loads(result.stdout)["outcome"], "blocked")
        self.assertEqual(before, {p.name: p.read_bytes() for p in spaced.iterdir()})
        self.assertFalse(marker.exists())

    def test_runtime_only_ablation_cli_scores_an_external_subject_bundle(self):
        output, _ = self.bundle()
        installed = self.root / "runtime café"
        shutil.copytree(SKILL, installed)
        result = subprocess.run([sys.executable, "-I", "-B", "-S", str(installed / "scripts/ablate.py"), "score",
                                 "--key", str(output / "key.json"), "--judgments", str(self.judgments(output))],
                                cwd=self.root, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["outcome"], "completed")

    def test_unsupported_huge_metric_returns_structured_cli_failure_without_traceback(self):
        plan = self.panel(variants=False)
        rows = self.rows(plan)
        rows[0]["latency_seconds"] = 10 ** 400
        plan_path = self.write("huge-plan.json", plan)
        observation_path = self.write("huge-observations.json", {
            "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(), "runs": rows})
        result = subprocess.run([sys.executable, "-I", "-B", "-S", str(SKILL / "scripts/evaluate.py"), "summarize",
                                 "--plan", str(plan_path), "--observations", str(observation_path)],
                                cwd=self.root, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertEqual(json.loads(result.stdout)["outcome"], "blocked")
        self.assertEqual(result.stderr, b"")


if __name__ == "__main__":
    unittest.main()
