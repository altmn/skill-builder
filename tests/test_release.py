"""Independent package output contracts; no native-host assurance."""
from __future__ import annotations

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
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("skill_builder_release", ROOT / "tools/build_release.py")
release = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(release)


class ReleaseContractTests(unittest.TestCase):
    def temporary_directory(self):
        # macOS commonly supplies /var/... while /var aliases /private/var.
        # Canonicalize ordinary fixture roots; intentional aliases stay explicit.
        return tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve(strict=True))

    def copy_project(self, parent: Path) -> Path:
        project = parent / "project"
        project.mkdir()
        # Some restricted runners use the working directory for tempfile.
        # Copy only the project roots so this fixture cannot copy itself.
        for name in sorted(release.SOURCE_FILES):
            shutil.copy2(ROOT / name, project / name)
        for name in sorted(release.SOURCE_DIRS):
            shutil.copytree(ROOT / name, project / name, ignore=shutil.ignore_patterns(
                ".git", "__pycache__", ".pytest_cache", ".venv", "dist"))
        return project

    def symlink(self, link: Path, target: Path, *, directory: bool = False):
        try:
            link.symlink_to(target, target_is_directory=directory)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable on this platform")

    def project_settings(self, project: Path):
        return mock.patch.multiple(release, ROOT=project, SKILL=project / "skills/skill-builder")

    def test_temporary_fixture_canonicalizes_system_temp_alias(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            real = base / "real-temp"
            real.mkdir()
            alias = base / "system-temp-alias"
            self.symlink(alias, real, directory=True)
            with mock.patch.object(tempfile, "gettempdir", return_value=str(alias)):
                with self.temporary_directory() as nested:
                    fixture = Path(nested)
                    self.assertEqual(fixture.parent, real)
                    release.checked_path(fixture, directory=True)
            with self.assertRaisesRegex(ValueError, "Symlink inputs/ancestors"):
                release.checked_path(alias, directory=True)

    def test_exact_bytes_manifest_and_determinism(self):
        with self.temporary_directory() as folder:
            root = Path(folder)
            files = {"SKILL.md": b"example\n", "references/value.bin": b"\x00\xffexact\n"}
            first = release.make_zip(root / "one.zip", "example", files, "fixture")
            second = release.make_zip(root / "two.zip", "example", files, "fixture")
            self.assertEqual(first["sha256"], second["sha256"])
            with zipfile.ZipFile(root / "one.zip") as archive:
                self.assertEqual(set(archive.namelist()), {"example/SKILL.md", "example/references/value.bin", "example/PACKAGE-MANIFEST.json"})
                manifest = json.loads(archive.read("example/PACKAGE-MANIFEST.json"))
                for row in manifest["files"]:
                    data = archive.read("example/" + row["path"])
                    self.assertEqual(hashlib.sha256(data).hexdigest(), row["sha256"])
                self.assertNotIn("PACKAGE-MANIFEST.json", [row["path"] for row in manifest["files"]])
                self.assertEqual(archive.read("example/references/value.bin"), files["references/value.bin"])

    def test_payload_identity_changes_with_bytes_or_path(self):
        base = release.payload_manifest({"x": b"one"}, "fixture")["payload_sha256"]
        self.assertNotEqual(base, release.payload_manifest({"x": b"two"}, "fixture")["payload_sha256"])
        self.assertNotEqual(base, release.payload_manifest({"y": b"one"}, "fixture")["payload_sha256"])

    def test_stale_generated_manifest_is_refused(self):
        with self.temporary_directory() as folder:
            target = Path(folder) / "invalid.zip"
            with self.assertRaises(ValueError):
                release.make_zip(target, "example", {"SKILL.md": b"example", "PACKAGE-MANIFEST.json": b"old"}, "fixture")
            self.assertFalse(target.exists())

    def test_existing_output_preserved(self):
        with self.temporary_directory() as folder:
            output = Path(folder) / "existing"
            output.mkdir()
            sentinel = output / "owner.txt"
            sentinel.write_bytes(b"preserve")
            with self.assertRaises(ValueError):
                release.prepare(output)
            self.assertEqual(sentinel.read_bytes(), b"preserve")

    def test_symlink_source_refused(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            source = base / "source"
            source.write_text("data")
            link = base / "link"
            try:
                link.symlink_to(source)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks unavailable on this platform")
            with self.assertRaises(ValueError):
                release.regular_bytes(link)

    def test_runtime_has_only_one_discoverable_skill(self):
        files = release.runtime_files()
        entries = [p for p in files if Path(p).name == "SKILL.md"]
        self.assertEqual(entries, ["SKILL.md"])
        self.assertIn("references/knowledge-base.zip", files)

    def test_environment_file_in_selected_tree_is_refused(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            (base / "ordinary.md").write_text("safe")
            (base / ".env.local").write_text("DUMMY_VALUE=fixture")
            with self.assertRaises(ValueError):
                release.walk_files(base)

    def test_selected_directory_roots_refused_before_read_or_output(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            for name in sorted(release.SOURCE_DIRS):
                with self.subTest(selected_root=name):
                    selected = project / name
                    external = base / "external"
                    selected.rename(external)
                    self.symlink(selected, external, directory=True)
                    try:
                        with self.project_settings(project), mock.patch.object(release, "regular_bytes") as read:
                            with self.assertRaises(ValueError):
                                release.prepare(base / "output")
                            read.assert_not_called()
                        self.assertFalse((base / "output").exists())
                    finally:
                        selected.unlink()
                        external.rename(selected)

    def test_selected_files_and_broken_links_are_refused(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            selected = project / "README.md"
            external = base / "external.md"
            selected.rename(external)
            for target in (external, base / "missing.md"):
                with self.subTest(broken=not target.exists()):
                    self.symlink(selected, target)
                    try:
                        with self.project_settings(project):
                            with self.assertRaises(ValueError):
                                release.source_files()
                    finally:
                        selected.unlink()

    def test_runtime_root_and_ancestor_symlinks_are_refused(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            for relative in ("skills/skill-builder", "skills"):
                with self.subTest(path=relative):
                    selected = project / relative
                    external = base / "external-runtime"
                    selected.rename(external)
                    self.symlink(selected, external, directory=True)
                    try:
                        with self.project_settings(project):
                            with self.assertRaises(ValueError):
                                release.runtime_files()
                        result = subprocess.run([sys.executable, "-I", "-B", "tools/build_release.py", "--identity"],
                                                cwd=project, capture_output=True, text=True)
                        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                        self.assertEqual(json.loads(result.stderr)["status"], "failed")
                    finally:
                        selected.unlink()
                        external.rename(selected)

    def test_descendant_symlinks_and_file_ancestors_are_refused(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            selected = base / "selected"
            selected.mkdir()
            external = base / "external"
            external.mkdir()
            (external / "marker.txt").write_text("synthetic external marker")
            child = selected / "alias"
            self.symlink(child, external, directory=True)
            with self.assertRaises(ValueError):
                release.walk_files(selected)
            with self.assertRaises(ValueError):
                release.regular_bytes(child / "marker.txt")
            child.unlink()
            self.symlink(child, external / "marker.txt")
            with self.assertRaises(ValueError):
                release.walk_files(selected)

    def test_project_check_rejects_selected_root_before_using_payload(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            external = base / "external-docs"
            (project / "docs").rename(external)
            (external / "synthetic-marker.txt").write_text("SYNTHETIC-EXTERNAL-CONTENT")
            self.symlink(project / "docs", external, directory=True)
            result = subprocess.run([sys.executable, "-I", "-B", "tools/check_project.py"],
                                    cwd=project, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["outcome"], "failed")
            self.assertNotIn("SYNTHETIC-EXTERNAL-CONTENT", result.stdout + result.stderr)

    def test_project_path_alias_is_not_hidden_by_resolve(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            alias = base / "project-alias"
            self.symlink(alias, project, directory=True)
            for tool, flags in (("build_release.py", ["--identity"]), ("check_project.py", [])):
                with self.subTest(tool=tool):
                    result = subprocess.run([sys.executable, "-I", "-B", str(alias / "tools" / tool), *flags],
                                            cwd=base, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_missing_wrong_type_and_unreadable_selected_trees_fail(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            with self.assertRaises(FileNotFoundError):
                release.walk_files(base / "absent")
            (base / "plain-file").write_text("not a tree")
            with self.assertRaises(ValueError):
                release.walk_files(base / "plain-file")
            # A permission-denied scandir must be propagated even on privileged
            # test runners where chmod(0) does not prevent access.
            with mock.patch.object(release.os, "scandir", side_effect=PermissionError("fixture denied")):
                with self.assertRaises(PermissionError):
                    release.walk_files(base)

    def test_nested_output_is_rejected_without_creating_any_files(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            (project / "docs/dist").mkdir()
            for relative in (*sorted(release.SOURCE_DIRS), "docs/dist", "skills/skill-builder"):
                with self.subTest(parent=relative):
                    output = project / relative / "new-release"
                    before = sorted(output.parent.iterdir())
                    with self.project_settings(project):
                        with self.assertRaisesRegex(ValueError, "outside every selected source directory"):
                            release.prepare(output)
                    self.assertFalse(output.exists())
                    self.assertEqual(sorted(output.parent.iterdir()), before)

    def test_output_symlink_ancestor_is_rejected_before_writing(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            real = base / "real"
            real.mkdir()
            self.symlink(base / "alias", real, directory=True)
            with self.assertRaises(ValueError):
                release.prepare(base / "alias/new-output")
            self.assertEqual(list(real.iterdir()), [])

    def test_supported_repeated_builds_keep_exact_archive_identities(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            (project / "dist").mkdir()
            with self.project_settings(project):
                first = release.prepare(project / "dist/first")
                second = release.prepare(project / "dist/second")
                sibling = release.prepare(base / "sibling-release")
            self.assertEqual(first["archives"], second["archives"])
            self.assertEqual(first["archives"], sibling["archives"])
            version = (project / "VERSION").read_text().strip()
            source = project / "dist/second" / f"skill-builder-{version}-source.zip"
            with zipfile.ZipFile(source) as archive:
                self.assertFalse(any("/dist/" in name or name.endswith("/build-receipt.json")
                                     for name in archive.namelist()))

    def test_source_runtime_licenses_and_current_metadata_agree(self):
        with self.temporary_directory() as folder:
            output = Path(folder) / "release"
            result = release.prepare(output)
            self.assertEqual(result["release_verdict"], "PREPARED_UNPUBLISHED")
            self.assertEqual(result["license"], "MIT")
            self.assertEqual(result["blockers"], [])
            self.assertEqual(result["publication"], "not_run")
            self.assertEqual(release.regular_bytes(ROOT / "LICENSE.md"),
                             release.regular_bytes(release.SKILL / "LICENSE.md"))
            for item in result["archives"]:
                with self.subTest(archive=item["filename"]), zipfile.ZipFile(output / item["filename"]) as archive:
                    prefix = archive.namelist()[0].split("/")[0]
                    manifest = json.loads(archive.read(prefix + "/PACKAGE-MANIFEST.json"))
                    self.assertEqual(manifest["license"], "MIT")
                    self.assertEqual(manifest["open_reuse_gate"], "license_selected_with_retained_third_party_terms")
                    self.assertEqual(manifest["native_host_execution"], "not_run")
                    license_text = " ".join(archive.read(prefix + "/LICENSE.md").decode().split())
                    self.assertEqual(
                        [line for line in archive.read(prefix + "/LICENSE.md").decode().splitlines()
                         if line.startswith("Copyright (c) ")],
                        ["Copyright (c) 2026 Alex Allen"])
                    for clause in ("Permission is hereby granted, free of charge",
                                   'THE SOFTWARE IS PROVIDED "AS IS"', "third-party", release.EXPECTED_KB_HASH):
                        self.assertIn(clause, license_text)
                    kb_path = ("skills/skill-builder/" if manifest["kind"] in {"source-project", "openai-plugin"} else "") + "references/knowledge-base.zip"
                    self.assertEqual(hashlib.sha256(archive.read(prefix + "/" + kb_path)).hexdigest(), release.EXPECTED_KB_HASH)

    def test_inconsistent_license_decision_cannot_claim_selected_mit(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            decision_path = project / "skills/skill-builder/references/license-decision.json"
            decision = json.loads(decision_path.read_text())
            decision["status"] = "pending"
            decision_path.write_text(json.dumps(decision))
            with self.project_settings(project):
                with self.assertRaisesRegex(ValueError, "license decision"):
                    release.prepare(base / "release")
            self.assertFalse((base / "release").exists())

    def test_matching_license_copies_with_wrong_full_attribution_are_refused(self):
        with self.temporary_directory() as folder:
            base = Path(folder)
            project = self.copy_project(base)
            source_path = project / "LICENSE.md"
            runtime_path = project / "skills/skill-builder/LICENSE.md"
            original = source_path.read_text()
            for attribution in ("Copyright (c) 2026 Alex",
                                "Copyright (c) 2026 Alex Allen-Synthetic"):
                with self.subTest(attribution=attribution):
                    altered = original.replace("Copyright (c) 2026 Alex Allen\n", attribution + "\n", 1)
                    self.assertNotEqual(altered, original)
                    source_path.write_text(altered)
                    runtime_path.write_text(altered)
                    with self.project_settings(project):
                        with self.assertRaisesRegex(ValueError, "copyright attribution"):
                            release.prepare(base / "release")
                    self.assertFalse((base / "release").exists())


if __name__ == "__main__":
    unittest.main()
