"""Meaningful offline contracts for the builder's new resources.

These tests do not establish discovery, agent task success, or enforcement on
Codex, Claude Code, Grok, Windows, or macOS. Fixtures never execute candidate code.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile

PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "skills/skill-builder/scripts/skill_builder.py"
spec = importlib.util.spec_from_file_location("builder", SCRIPT)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BuilderContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = builder.KnowledgeBase()

    def setUp(self):
        self.work = tempfile.TemporaryDirectory(prefix=".test-builder-", dir=PROJECT)
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name)

    def cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), *map(str, args)],
                              cwd=cwd or self.root, capture_output=True, timeout=45,
                              env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})

    def decoded(self, result):
        self.assertFalse(result.stderr, result.stderr.decode(errors="replace"))
        return json.loads(result.stdout)

    def fixture(self, entries=None, rows=None):
        references = self.root / "references"
        references.mkdir()
        entries = entries or [("kb/doc.md", b"# Source\nExact original content.\n", False)]
        buffer = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
                for name, data, symlink in entries:
                    info = zipfile.ZipInfo(name)
                    info.create_system = 3
                    info.external_attr = (0o120777 if symlink else 0o100644) << 16
                    archive.writestr(info, data)
        data = buffer.getvalue()
        digest = hashlib.sha256(data).hexdigest()
        if rows is None:
            rows = [{"path": name[3:], "archive_member": name, "size_bytes": len(content),
                     "sha256": hashlib.sha256(content).hexdigest()} for name, content, _ in entries]
        manifest = {"schema_version": "1.0.0", "archive": "knowledge-base.zip", "archive_sha256": digest,
                    "archive_size_bytes": len(data), "archive_root": "kb", "files": rows,
                    "content_file_count": len(rows), "content_bytes": sum(r["size_bytes"] for r in rows)}
        (references / "knowledge-base.zip").write_bytes(data)
        (references / "knowledge-base-manifest.json").write_bytes(builder.json_bytes(manifest))
        return references, digest, manifest

    def candidate(self, name="example-skill", body="Follow the explicitly requested task.\n", description="Inspect a local example."):
        target = self.root / name
        target.mkdir()
        (target / "SKILL.md").write_text("---\nname: " + name + "\ndescription: " + json.dumps(description) + "\n---\n\n# Example\n\n" + body)
        return target

    def test_received_archive_and_all_182_files_are_verified(self):
        result = self.kb.verify()
        self.assertEqual(result["content_files"], 182)
        self.assertEqual(result["content_bytes"], 76965199)
        self.assertEqual(result["archive_sha256"], builder.EXPECTED_ARCHIVE_SHA256)
        self.assertFalse(result["source_content_rewritten"])

    def test_public_json_results_have_version_and_explicit_outcome(self):
        import jsonschema
        schema = json.loads((SCRIPT.parents[1] / "references/cli-result.schema.json").read_text())
        validator = jsonschema.Draft202012Validator(schema)
        for arguments in (("kb", "verify"), ("kb", "list", "--prefix", "handbook/"),
                          ("profile", "--profile", "instruction"), ("check",), ("unknown-command",)):
            with self.subTest(arguments=arguments):
                result = self.cli(*arguments)
                payload = self.decoded(result)
                self.assertEqual(payload["schema_version"], "1.0.0")
                self.assertIsInstance(payload["outcome"], str)
                self.assertTrue(payload["outcome"])
                validator.validate(payload)

    def test_read_outputs_complete_exact_bytes_without_extra_newline(self):
        path = "handbook/04-portability.md"
        result = self.cli("kb", "read", path)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, self.kb.read(path))

    def test_archive_tamper_rejected_before_retrieval(self):
        references, digest, _ = self.fixture()
        with (references / "knowledge-base.zip").open("ab") as stream:
            stream.write(b"tamper")
        with self.assertRaises(builder.BuilderError):
            builder.KnowledgeBase(references, digest)

    def test_paged_read_reconstructs_exact_utf8_crlf_and_final_line(self):
        raw = "first\r\nAé😀中\r\nlast".encode()
        references, digest, _ = self.fixture([("kb/doc.md", raw, False)])
        kb = builder.KnowledgeBase(references, digest)
        offset, chunks = 0, []
        while True:
            page = builder.read_page(kb, "doc.md", offset, 5, builder.sha256(raw))
            chunk = page["text"].encode()
            self.assertEqual(chunk, raw[offset:offset + page["returned_bytes"]])
            self.assertLessEqual(len(chunk), 5)
            self.assertEqual(page["sha256"], builder.sha256(raw))
            chunks.append(chunk)
            if page["next_offset"] is None:
                self.assertTrue(page["complete"])
                break
            self.assertGreater(page["next_offset"], offset)
            offset = page["next_offset"]
        self.assertEqual(b"".join(chunks), raw)
        self.assertEqual(builder.read_page(kb, "doc.md", len(raw), 4, builder.sha256(raw))["text"], "")

    def test_paged_read_rejects_stale_hash_invalid_cursors_and_binary(self):
        raw = "é😀".encode()
        references, digest, _ = self.fixture([("kb/doc.md", raw, False), ("kb/data.bin", b"\0", False)])
        kb = builder.KnowledgeBase(references, digest)
        for offset, limit, sha in ((1, 4, builder.sha256(raw)), (7, 4, builder.sha256(raw)),
                                   (-1, 4, None), (0, 3, None), (0, 16385, None),
                                   (2, 4, None), (0, 4, "0" * 64)):
            with self.subTest(offset=offset, limit=limit, sha=sha), self.assertRaises(builder.BuilderError):
                builder.read_page(kb, "doc.md", offset, limit, sha)
        with self.assertRaises(builder.BuilderError):
            builder.read_page(kb, "data.bin", 0, 4)

    def test_paged_read_cli_schema_and_resume_identity(self):
        import jsonschema
        schema = json.loads((SCRIPT.parents[1] / "references/cli-result.schema.json").read_text())
        page = self.decoded(self.cli("kb", "read", "catalogs/requirements.json", "--limit", "1024"))
        jsonschema.validate(page, schema)
        self.assertFalse(page["complete"])
        resumed = self.cli("kb", "read", page["path"], "--offset", page["next_offset"], "--sha256", page["sha256"], "--limit", "1024")
        self.assertEqual(resumed.returncode, 0)
        self.assertEqual(self.decoded(resumed)["offset"], page["next_offset"])
        self.assertEqual(self.cli("kb", "read", page["path"], "--offset", page["next_offset"]).returncode, 2)

    def test_manifest_cannot_reassign_pinned_archive(self):
        references, _, _ = self.fixture()
        with self.assertRaises(builder.BuilderError):
            builder.KnowledgeBase(references, "0" * 64)

    def test_duplicate_archive_entries_rejected(self):
        references, digest, _ = self.fixture([("kb/doc.md", b"a", False), ("kb/doc.md", b"b", False)])
        with self.assertRaises(builder.BuilderError):
            builder.KnowledgeBase(references, digest)

    def test_archive_traversal_is_rejected(self):
        references, digest, _ = self.fixture([("kb/../escape", b"a", False)])
        with self.assertRaises(builder.BuilderError):
            builder.KnowledgeBase(references, digest)
        self.assertFalse((self.root / "escape").exists())

    def test_archive_symlink_is_rejected(self):
        references, digest, _ = self.fixture([("kb/link", b"/external", True)])
        with self.assertRaises(builder.BuilderError):
            builder.KnowledgeBase(references, digest)

    def test_extra_substantive_archive_member_cannot_hide_from_manifest(self):
        row = {"path": "doc.md", "archive_member": "kb/doc.md", "size_bytes": 1, "sha256": hashlib.sha256(b"a").hexdigest()}
        references, digest, _ = self.fixture([("kb/doc.md", b"a", False), ("kb/extra", b"b", False)], [row])
        with self.assertRaises(builder.BuilderError):
            builder.KnowledgeBase(references, digest)

    def test_wrong_individual_hash_fails_verification(self):
        references, digest, manifest = self.fixture()
        manifest["files"][0]["sha256"] = "0" * 64
        (references / "knowledge-base-manifest.json").write_bytes(builder.json_bytes(manifest))
        kb = builder.KnowledgeBase(references, digest)
        with self.assertRaises(builder.BuilderError):
            kb.verify()

    def test_content_path_cannot_escape_index(self):
        for path in (".", "./", "../README.md", "/etc/passwd", "C:/file", "a\\b", "x/../README.md", "bad\x7fpath"):
            with self.subTest(path=path), self.assertRaises(builder.BuilderError):
                self.kb.read(path)

    def test_full_manifest_listing_and_prefix_are_explicit(self):
        all_result = self.decoded(self.cli("kb", "list"))
        subset = self.decoded(self.cli("kb", "list", "--prefix", "handbook/"))
        self.assertEqual(all_result["count"], 182)
        self.assertEqual(subset["count"], 13)
        self.assertTrue(subset["complete_for_prefix"])
        self.assertTrue(all(x["path"].startswith("handbook/") for x in subset["files"]))

    def test_search_is_literal_paginated_and_discloses_preview_limits(self):
        references, digest, _ = self.fixture([("kb/doc.md", ("a .* literal\n" + "z" * 600 + " .* tail\na .* last\n").encode(), False)])
        kb = builder.KnowledgeBase(references, digest)
        first = builder.search(kb, ".*", "", 0, 1, False)
        second = builder.search(kb, ".*", "", first["next_offset"], 1, False)
        last = builder.search(kb, ".*", "", 2, 1, False)
        self.assertEqual(first["total_matching_lines"], 3)
        self.assertEqual(first["matches"][0]["line"], 1)
        self.assertTrue(second["matches"][0]["preview_truncated"])
        self.assertIsNone(last["next_offset"])

    def test_search_no_hits_is_not_fabricated_content(self):
        result = builder.search(self.kb, "UNIQUE-NO-SUCH-KB-TERM-0c5d58", "handbook/", 0, 20, False)
        self.assertEqual(result["total_matching_lines"], 0)
        self.assertEqual(result["matches"], [])

    def test_extract_reproduces_every_indexed_file_without_executing(self):
        output = self.root / "extracted"
        result = self.cli("kb", "extract", "--output", output)
        self.assertEqual(result.returncode, 0, result.stdout)
        report = self.decoded(result)
        self.assertFalse(report["code_executed"])
        actual = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
        self.assertEqual(actual, set(self.kb.files))
        for path, row in self.kb.files.items():
            self.assertEqual(hashlib.sha256((output / path).read_bytes()).hexdigest(), row["sha256"], path)

    def test_extract_refuses_installed_skill_locations(self):
        parent = self.root / ".claude" / "skills"
        parent.mkdir(parents=True)
        result = self.cli("kb", "extract", "--output", parent / "unpack")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((parent / "unpack").exists())

    def test_existing_outputs_are_not_overwritten(self):
        output = self.root / "existing"
        output.mkdir()
        (output / "keep").write_text("unchanged")
        result = self.cli("skill-builder-create", "--name", "example", "--description", "Create an example.", "--output", output, "--profile", "instruction")
        self.assertEqual(result.returncode, 2)
        self.assertEqual((output / "keep").read_text(), "unchanged")
        self.assertEqual(list(output.iterdir()), [output / "keep"])

    def test_output_symlink_parent_is_refused(self):
        real = self.root / "real"
        real.mkdir()
        link = self.root / "link"
        try:
            link.symlink_to(real, target_is_directory=True)
        except OSError:
            self.skipTest("Symlinks unavailable on this platform; no platform assurance inferred.")
        with self.assertRaises(builder.BuilderError):
            builder.checked_destination(str(link / "new"))
        self.assertFalse((real / "new").exists())

    def test_create_quotes_description_and_does_not_execute_shell_text(self):
        output = self.root / "new-project"
        description = 'Inspect "quoted" input: yes\n$(touch SENTINEL); `false`'
        result = self.cli("skill-builder-create", "--name", "example-skill", "--description", description,
                          "--output", output, "--profile", "resource_assisted")
        self.assertEqual(result.returncode, 0, result.stdout)
        report = self.decoded(result)
        self.assertFalse(report["release_ready"])
        self.assertFalse((self.root / "SENTINEL").exists())
        import yaml
        skill = (output / "skills/example-skill/SKILL.md").read_text()
        self.assertEqual(yaml.safe_load(skill.split("---", 2)[1])["description"], description)
        self.assertIn("DRAFT", skill)
        trace = json.loads((output / "evidence/rule-traceability.json").read_text())
        self.assertEqual(len(trace["records"]), 99)
        self.assertFalse(any(r["verification"]["outcome"] == "passed" for r in trace["records"]))
        self.assertEqual(builder.check_records(self.kb, [str(output / "evidence/rule-traceability.json")])["outcome"], "passed")

    def test_invalid_names_and_blank_description_fail_without_output(self):
        for name, description in (("../escape", "Valid"), ("UPPER", "Valid"), ("double--hyphen", "Valid"), ("a" * 65, "Valid"), ("fine", "  ")):
            with self.subTest(name=name):
                output = self.root / "new"
                result = self.cli("skill-builder-create", "--name", name, "--description", description,
                                  "--output", output, "--profile", "instruction")
                self.assertEqual(result.returncode, 2)
                self.assertFalse(output.exists())

    def test_created_descriptions_round_trip_unicode_scalars_through_yaml(self):
        import yaml
        descriptions = (
            'Ordinary Unicode: café, Проверка, 中文, e\u0301',
            'Quoted "text" and a backslash \\; line\nbreak\r\ntab\tend',
            *("Before" + character + "After" for character in
              ("\x01", "\x1f", "\x7f", "\x80", "\x84", "\x85", "\x86", "\x9f",
               "\u2028", "\u2029", "\ufffe", "\uffff", "\U0001f600", "\U00020000", "\U0010ffff")),
        )
        for index, description in enumerate(descriptions):
            with self.subTest(description=ascii(description)):
                output = self.root / ("unicode-" + str(index))
                result = self.cli("skill-builder-create", "--name", "unicode-example", "--description", description,
                                  "--output", output, "--profile", "instruction")
                self.assertEqual(result.returncode, 0, result.stdout)
                text = (output / "skills/unicode-example/SKILL.md").read_text(encoding="utf-8")
                actual = yaml.safe_load(text.split("---", 2)[1])["description"]
                self.assertEqual([ord(char) for char in actual], [ord(char) for char in description])
                self.assertFalse(self.decoded(result)["release_ready"])

    def test_surrogate_descriptions_fail_before_output_creation(self):
        for invalid in ("\ud800", "\udfff", "\ud83d\ude00"):
            with self.subTest(codepoints=ascii(invalid)):
                output = self.root / "invalid-unicode"
                args = builder.parser().parse_args([
                    "skill-builder-create", "--name", "example", "--description", "Before" + invalid + "After",
                    "--output", str(output), "--profile", "instruction"])
                with mock.patch.object(builder.NewTree, "__enter__", side_effect=AssertionError("Output creation attempted")) as entered:
                    with self.assertRaisesRegex(builder.BuilderError, "Unicode scalar"):
                        builder.create_project(args, self.kb)
                entered.assert_not_called()
                self.assertFalse(output.exists())

    def test_profiles_match_original_selector_and_preserve_full_rule_text(self):
        source = self.root / "source"
        (source / "catalogs").mkdir(parents=True)
        for name in ("requirements.json", "application-profiles.json"):
            (source / "catalogs" / name).write_bytes(self.kb.read("catalogs/" + name))
        original = builder.trusted_module(self.kb, "tools/profile_view.py")
        for profile in builder.PROFILES:
            for modifiers in ([], ["publication"], list(builder.MODIFIERS)):
                actual = builder.select_profile(self.kb, profile, modifiers, {})
                expected = original.select(profile, modifiers, root=source)
                self.assertEqual(len(actual["rules"]), 99)
                self.assertEqual(len({r["rule_id"] for r in actual["rules"]}), 99)
                for found, wanted in zip(actual["rules"], expected["rules"]):
                    for key in ("rule_id", "statement", "strength", "basis", "decision", "verification", "source_ids", "handbook"):
                        self.assertEqual(found[key], wanted[key], (profile, key))

    def test_publication_authority_is_selected(self):
        selected = builder.select_profile(self.kb, "instruction", ["publication"], {})
        row = next(r for r in selected["rules"] if r["rule_id"] == "LIFE-012")
        self.assertEqual(row["decision"], "adopted")

    def test_overrides_require_known_rule_and_reviewable_reason(self):
        for override in ({"UNKNOWN-001": {"decision": "adopted", "reason": "A specific reason longer than twenty chars."}},
                         {"LIFE-012": {"decision": "not_applicable", "reason": "No"}}):
            with self.assertRaises(builder.BuilderError):
                builder.select_profile(self.kb, "instruction", ["publication"], override)

    def test_audit_is_read_only_and_never_executes_candidate_code_or_hooks(self):
        target = self.candidate()
        (target / "danger.py").write_text("raise RuntimeError('candidate executed')\n")
        hook = target / ".git/hooks/pre-commit"
        hook.parent.mkdir(parents=True)
        hook.write_text("#!/bin/sh\ntouch NOT-ALLOWED\n")
        before = {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}
        output = self.root / "audit"
        result = self.cli("skill-builder-audit", "--target", target, "--output", output, "--profile", "resource_assisted", cwd=target)
        self.assertEqual(result.returncode, 0, result.stdout)
        report = self.decoded(result)
        self.assertEqual(report["audit_verdict"], "inconclusive")
        self.assertFalse(report["target_code_executed"])
        self.assertFalse(report["release_ready"])
        after = {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        inventory = json.loads((output / "inventory.json").read_text())
        self.assertIn("unknown", inventory["tracked_git_coverage"])
        self.assertTrue(any(x["path"] == ".git" for x in inventory["omissions"]))

    def test_audit_missing_resource_propagates_failure(self):
        target = self.candidate(body="Read [required resource](missing.md).\n")
        result = self.cli("skill-builder-audit", "--target", target, "--output", self.root / "audit", "--profile", "instruction")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.decoded(result)["audit_verdict"], "failed")

    def test_isolated_audit_ignores_hostile_cwd_and_pythonpath_modules(self):
        target = self.candidate()
        for name in ("yaml.py", "jsonschema.py", "sitecustomize.py"):
            (target / name).write_text("from pathlib import Path\nPath(__file__).with_name('EXECUTED').write_text('unsafe import')\nraise RuntimeError('unsafe import')\n")
        result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPT), "skill-builder-audit", "--target", str(target),
                                 "--output", str(self.root / "audit"), "--profile", "instruction"], cwd=target,
                                env={**os.environ, "PYTHONPATH": str(target)}, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertFalse((target / "EXECUTED").exists())

    def test_nonisolated_dependency_operation_is_refused(self):
        target = self.candidate()
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "skill-builder-audit", "--target", str(target),
                                 "--output", str(self.root / "audit"), "--profile", "instruction"],
                                cwd=self.root, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"python3 -I -B", result.stdout)
        self.assertFalse((self.root / "audit").exists())

    def test_no_actual_skill_is_blocked_not_passed(self):
        target = self.root / "no-skill"
        target.mkdir()
        (target / "SKILL.md.template").write_text("A template is not an actual skill.")
        result = self.cli("skill-builder-audit", "--target", target, "--output", self.root / "audit", "--profile", "instruction")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(self.decoded(result)["static_checks"], "blocked")

    def test_audit_output_cannot_modify_target(self):
        target = self.candidate()
        result = self.cli("skill-builder-audit", "--target", target, "--output", target / "audit", "--profile", "instruction")
        self.assertEqual(result.returncode, 2)
        self.assertFalse((target / "audit").exists())

    def test_symlink_contents_and_special_files_are_not_read(self):
        target = self.candidate()
        external = self.root / "private.txt"
        external.write_text("SECRET-SHOULD-NOT-BE-READ")
        try:
            (target / "link").symlink_to(external)
        except OSError:
            self.skipTest("Symlinks unavailable on this platform; no platform assurance inferred.")
        inventory = builder.inspect_tree(target, 100, 4096, 8192)
        row = next(r for r in inventory["files"] if r["path"] == "link")
        self.assertEqual(row["status"], "not_followed")
        self.assertNotIn("SECRET", json.dumps(inventory))
        self.assertEqual(inventory["coverage"], "incomplete")

    def test_inventory_budget_does_not_report_complete_coverage(self):
        target = self.candidate()
        (target / "large.bin").write_bytes(b"a" * 2048)
        inventory = builder.inspect_tree(target, 100, 1024, 4096)
        self.assertEqual(inventory["coverage"], "incomplete")
        self.assertTrue(any(x["reason"] == "file_or_total_byte_budget" for x in inventory["omissions"]))
        result = self.cli("skill-builder-audit", "--target", target, "--output", self.root / "audit", "--profile", "instruction", "--max-file-bytes", "1024")
        self.assertEqual(result.returncode, 1)

    def test_file_count_budget_reports_unenumerated_remainder(self):
        target = self.candidate()
        for i in range(4):
            (target / ("z" + str(i))).write_bytes(b"x")
        inventory = builder.inspect_tree(target, 2, 4096, 8192)
        self.assertEqual(inventory["files_recorded"], 2)
        self.assertEqual(inventory["coverage"], "incomplete")
        self.assertTrue(any("remaining tree" in x["reason"] for x in inventory["omissions"]))

    def test_empty_directory_tree_is_bounded_by_entry_budget(self):
        target = self.candidate()
        for i in range(12):
            (target / ("directory-" + str(i))).mkdir()
        inventory = builder.inspect_tree(target, 100, 4096, 8192, max_entries=3)
        self.assertLessEqual(inventory["entries_seen"], 3)
        self.assertEqual(inventory["coverage"], "incomplete")
        self.assertTrue(any("max_entries" in x["reason"] for x in inventory["omissions"]))

    def test_prefetched_siblings_are_charged_to_global_enumeration_budget(self):
        target = self.candidate()
        current = target
        for _ in range(6):
            for i in range(3):
                (current / ("z-file-" + str(i))).write_bytes(b"x")
            current = current / "a-child"
            current.mkdir()
        original = os.scandir
        actual_returned = 0
        class CountedScan:
            def __init__(self, path):
                self.stream = original(path)
            def __enter__(self):
                self.stream.__enter__()
                return self
            def __exit__(self, *args):
                return self.stream.__exit__(*args)
            def __iter__(self):
                return self
            def __next__(self):
                nonlocal actual_returned
                entry = next(self.stream)
                actual_returned += 1
                return entry
        with mock.patch.object(builder.os, "scandir", CountedScan):
            inventory = builder.inspect_tree(target, 100, 4096, 8192, max_entries=6)
        self.assertEqual(actual_returned, inventory["entries_seen"])
        self.assertLessEqual(actual_returned, 6)
        self.assertEqual(inventory["coverage"], "incomplete")

    def test_deep_directory_tree_has_explicit_coverage_limit(self):
        target = self.candidate()
        current = target
        for _ in range(131):
            current = current / "d"
            current.mkdir()
        inventory = builder.inspect_tree(target, 100, 4096, 8192)
        self.assertEqual(inventory["coverage"], "incomplete")
        self.assertTrue(any(x["reason"] == "maximum_directory_depth_128" for x in inventory["omissions"]))

    def test_evidence_validation_rejects_incomplete_and_false_pass_without_echoing_values(self):
        record = self.root / "bad-record.json"
        record.write_text('{"record_type":"host-capabilities","secret":"DO-NOT-ECHO-VALUES"}')
        result = self.cli("check", "--record", record)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertNotIn(b"DO-NOT-ECHO-VALUES", result.stdout)
        self.assertEqual(self.decoded(result)["records"]["outcome"], "failed")

    def test_duplicate_json_record_keys_and_nonfinite_numbers_are_rejected(self):
        for data in (b'{"outcome":"failed","outcome":"passed"}', b'{"cost":NaN}'):
            with self.assertRaises(builder.BuilderError):
                builder.parse_json(data)

    def test_nonfinite_numbers_are_rejected_at_every_json_depth(self):
        for token in (b"1e999", b"-1e999", b"NaN", b"Infinity", b"-Infinity"):
            for data in (token, b"[" + token + b"]", b'{"elapsed":{"value":' + token + b'}}',
                         b'{"attempts":[{"usage":{"cost":{"value":' + token + b'}}}]}'):
                with self.subTest(data=data), self.assertRaises(builder.BuilderError):
                    builder.parse_json(data)
        self.assertEqual(builder.parse_json(b'{"values":[1e3,-2.5e-2,0.0,42]}'),
                         {"values": [1000.0, -0.025, 0.0, 42]})

    def test_overflow_record_failures_keep_finite_controls_and_batch_order(self):
        # Mutations of a known schema-valid preserved example are synthetic
        # fixtures, not new claims about the historical example's observations.
        baseline = self.kb.json("examples/records/evaluation-receipt.json")
        paths, expected = [], []
        for index, (token, nested) in enumerate((
                ("1e3", False), ("1e999", False), ("-1e999", False),
                ("NaN", False), ("Infinity", False), ("-Infinity", False),
                ("1e999", True), ("-1e999", True), ("2.5e-2", True))):
            record = json.loads(json.dumps(baseline))
            target = record["attempts"][0]["elapsed"] if nested else record["elapsed"]
            target["value"] = "NUMBER-TOKEN"
            path = self.root / ("numeric-" + str(index) + ".json")
            path.write_text(json.dumps(record).replace('"NUMBER-TOKEN"', token), encoding="utf-8")
            paths.append(str(path))
            expected.append("passed" if index in (0, 8) else "failed")
        result = self.cli("check", *(argument for path in paths for argument in ("--record", path)))
        self.assertEqual(result.returncode, 1, result.stdout)
        report = self.decoded(result)
        self.assertEqual(report["outcome"], "failed")
        self.assertEqual([row["path"] for row in report["records"]["records"]], paths)
        self.assertEqual([row["outcome"] for row in report["records"]["records"]], expected)

    def test_wrong_type_record_dispatch_preserves_every_result_without_echoing_values(self):
        valid = self.kb.read("examples/records/evaluation-receipt.json")
        paths, expected = [], []
        fixtures = [valid]
        for value in ([], {}, ["DO-NOT-ECHO-VALUES"], {"private": "DO-NOT-ECHO-VALUES"},
                      None, True, 42, "DO-NOT-ECHO-VALUES"):
            fixtures.append(json.dumps({"record_type": value}).encode())
        fixtures.extend((b"[]", b"null", valid))
        for index, data in enumerate(fixtures):
            path = self.root / ("dispatch-" + str(index) + ".json")
            path.write_bytes(data)
            paths.append(str(path))
            expected.append("passed" if index in (0, len(fixtures) - 1) else "failed")
        result = self.cli("check", *(argument for path in paths for argument in ("--record", path)))
        self.assertEqual(result.returncode, 1, result.stdout)
        report = self.decoded(result)
        self.assertEqual(report["outcome"], "failed")
        self.assertEqual([row["path"] for row in report["records"]["records"]], paths)
        self.assertEqual([row["outcome"] for row in report["records"]["records"]], expected)
        self.assertNotIn(b"DO-NOT-ECHO-VALUES", result.stdout)

    def test_unexpandable_record_path_preserves_valid_records_and_safe_diagnostics(self):
        valid = self.kb.json("examples/records/evaluation-receipt.json")
        valid["redaction"] = "DO-NOT-ECHO-VALUES"
        first, last = self.root / "first.json", self.root / "last.json"
        first.write_bytes(builder.json_bytes(valid))
        last.write_bytes(builder.json_bytes(valid))
        bad = "~skill_builder_integration_no_such_user_9a4255/evidence.json"
        paths = [str(first), bad, str(last)]
        result = self.cli("check", *(argument for path in paths for argument in ("--record", path)))
        self.assertEqual(result.returncode, 1, result.stdout)
        report = self.decoded(result)
        self.assertEqual(report["outcome"], "failed")
        rows = report["records"]["records"]
        self.assertEqual([row["path"] for row in rows], paths)
        self.assertEqual([row["outcome"] for row in rows], ["passed", "failed", "passed"])
        self.assertEqual(rows[1]["reason"], "Record path could not be expanded.")
        self.assertNotIn(b"DO-NOT-ECHO-VALUES", result.stdout)

    def test_owned_failure_cleanup_keeps_unrelated_new_file(self):
        output = self.root / "new"
        with self.assertRaises(RuntimeError):
            with builder.NewTree(output) as tree:
                tree.write("owned.txt", b"generated")
                (output / "unrelated.txt").write_text("keep")
                raise RuntimeError("simulated write failure")
        self.assertFalse((output / "owned.txt").exists())
        self.assertEqual((output / "unrelated.txt").read_text(), "keep")

    def test_owned_failure_cleanup_keeps_in_place_modified_file(self):
        output = self.root / "new"
        with self.assertRaises(RuntimeError):
            with builder.NewTree(output) as tree:
                tree.write("owned.txt", b"generated")
                owned = output / "owned.txt"
                original = owned.stat()
                owned.write_text("user's edit")
                self.assertEqual((original.st_dev, original.st_ino),
                                 (owned.stat().st_dev, owned.stat().st_ino))
                raise RuntimeError("simulated later failure")
        self.assertEqual((output / "owned.txt").read_text(), "user's edit")

    def test_owned_failure_cleanup_keeps_replaced_file(self):
        output = self.root / "new"
        replacement = self.root / "replacement.txt"
        replacement.write_text("replacement to keep")
        with self.assertRaises(RuntimeError):
            with builder.NewTree(output) as tree:
                tree.write("owned.txt", b"generated")
                replacement.replace(output / "owned.txt")
                raise RuntimeError("simulated later failure")
        self.assertEqual((output / "owned.txt").read_text(), "replacement to keep")

    def test_owned_failure_cleanup_keeps_contents_beneath_replaced_root(self):
        output = self.root / "new"
        moved = self.root / "moved"
        with self.assertRaises(RuntimeError):
            with builder.NewTree(output) as tree:
                tree.write("nested/owned.txt", b"generated")
                output.rename(moved)
                try:
                    output.symlink_to(moved, target_is_directory=True)
                except OSError:
                    self.skipTest("Symlinks unavailable; no platform assurance inferred.")
                raise RuntimeError("simulated later failure")
        self.assertTrue(output.is_symlink())
        self.assertEqual((moved / "nested/owned.txt").read_bytes(), b"generated")

    def test_owned_failure_cleanup_keeps_files_with_changed_metadata(self):
        for change in ("mode", "timestamp"):
            with self.subTest(change=change):
                output = self.root / change
                with self.assertRaises(RuntimeError):
                    with builder.NewTree(output) as tree:
                        tree.write("owned.txt", b"generated")
                        owned = output / "owned.txt"
                        if change == "mode":
                            owned.chmod(0o640)
                        else:
                            before = owned.stat()
                            os.utime(owned, ns=(before.st_atime_ns, before.st_mtime_ns - 1_000_000_000))
                        raise RuntimeError("simulated later failure")
                self.assertEqual((output / "owned.txt").read_bytes(), b"generated")

    def test_owned_failure_cleanup_keeps_directory_metadata_changes(self):
        output = self.root / "new"
        with self.assertRaises(RuntimeError):
            with builder.NewTree(output) as tree:
                tree.write("nested/owned.txt", b"generated")
                before = (output / "nested").stat()
                os.utime(output / "nested", ns=(before.st_atime_ns, before.st_mtime_ns - 1_000_000_000))
                raise RuntimeError("simulated later failure")
        self.assertFalse((output / "nested/owned.txt").exists())
        self.assertTrue((output / "nested").is_dir())

    def test_owned_failure_cleanup_removes_unchanged_nested_output(self):
        output = self.root / "new"
        with self.assertRaises(RuntimeError):
            with builder.NewTree(output) as tree:
                tree.write("nested/owned.txt", b"generated")
                raise RuntimeError("simulated later failure")
        self.assertFalse(output.exists())

    def test_owned_failure_cleanup_removes_known_partial_write(self):
        output = self.root / "new"
        original_write = os.write
        calls = 0
        def partial_then_failure(descriptor, data):
            nonlocal calls
            calls += 1
            if calls == 1:
                return original_write(descriptor, data[:5])
            raise OSError("simulated write failure")
        with mock.patch.object(builder.os, "write", partial_then_failure):
            with self.assertRaises(OSError):
                with builder.NewTree(output) as tree:
                    tree.write("nested/owned.txt", b"generated content")
        self.assertEqual(calls, 2)
        self.assertFalse(output.exists())

    def test_owned_failure_cleanup_keeps_unconfirmed_partial_write(self):
        output = self.root / "new"
        original_write = os.write
        def unconfirmed_write(descriptor, data):
            original_write(descriptor, data[:5])
            raise OSError("write failed without a confirmed byte count")
        with mock.patch.object(builder.os, "write", unconfirmed_write):
            with self.assertRaises(OSError):
                with builder.NewTree(output) as tree:
                    tree.write("owned.txt", b"generated content")
        self.assertEqual((output / "owned.txt").read_bytes(), b"gener")

    def test_cli_misuse_has_nonzero_json_error(self):
        for arguments in (("unknown-command",), ("kb", "search", "needle", "--offset", "-1"), ("kb", "search", "needle", "--limit", "201")):
            result = self.cli(*arguments)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(self.decoded(result)["outcome"], "blocked")

    def test_every_documented_public_cli_mode_has_help(self):
        for arguments in (("--help",), ("skill-builder-create", "--help"), ("skill-builder-audit", "--help"), ("profile", "--help"),
                          ("check", "--help"), *(('kb', mode, '--help') for mode in ("list", "verify", "read", "search", "extract"))):
            with self.subTest(arguments=arguments):
                result = self.cli(*arguments)
                self.assertEqual(result.returncode, 0)
                self.assertIn(b"usage:", result.stdout)


if __name__ == "__main__":
    unittest.main()
