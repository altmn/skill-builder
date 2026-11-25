#!/usr/bin/env python3
"""Offline scaffolding, static evidence, and exact knowledge-base retrieval.

Creation and audit commands prepare work for an agent/reviewer. They do not
certify semantic quality, run candidate code, install skills, or publish work.
Core commands use Python 3.10+ and the standard library. Static format checking
uses the preserved validator and PyYAML; evidence checking also needs jsonschema
and referencing. Dependencies are never installed automatically.
Invoke with `python3 -I -B`: isolated mode prevents caller PYTHONPATH/current
directory imports from replacing the reviewed dependencies. Python startup itself
is outside the script's control, so use isolated mode from process launch.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import types
from typing import Any
import zipfile

VERSION = "1.0.0"
SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = SKILL_ROOT / "references"
EXPECTED_ARCHIVE_SHA256 = "9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204"
MAX_ARCHIVE_BYTES = 32 * 1024 * 1024
MAX_MEMBER_BYTES = 64 * 1024 * 1024
MAX_RECORD_BYTES = 4 * 1024 * 1024
PROFILES = ("instruction", "resource_assisted", "suite_runtime")
MODIFIERS = ("network", "publication", "persistent_state", "authenticated_browser", "installer")
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z", re.ASCII)
EXCLUDED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache"}


class BuilderError(ValueError):
    """Expected failure with a message that does not quote input file bodies."""


class JsonParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise BuilderError("Invalid command-line arguments; use the relevant --help command.")


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def emit(value: Any) -> None:
    if isinstance(value, dict):
        value = {"schema_version": "1.0.0", **value}
    sys.stdout.write(json_bytes(value).decode("utf-8"))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BuilderError("Duplicate JSON object key rejected.")
        result[key] = value
    return result


def finite_json_float(value: str) -> float:
    """Reject exponent overflow as well as the separately rejected named tokens."""
    result = float(value)
    if not math.isfinite(result):
        raise BuilderError("Nonfinite JSON number rejected.")
    return result


def parse_json(data: bytes) -> Any:
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_float=finite_json_float,
                          parse_constant=lambda _: (_ for _ in ()).throw(BuilderError("Nonfinite JSON number rejected.")))
    except BuilderError:
        raise
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise BuilderError("Input is not supported UTF-8 JSON.") from exc


def yaml_quoted_scalar(value: str) -> str:
    """Quote without YAML's raw control-character rejection or line folding.

    JSON already escapes quotes, backslashes and C0 controls. YAML additionally
    rejects DEL/C1 characters and two BMP noncharacters, and treats NEL/Unicode
    line separators as line breaks even inside a double-quoted scalar. Escape
    those code points explicitly; ordinary Unicode, including non-BMP scalars,
    remains UTF-8 instead of becoming JSON surrogate pairs.
    """
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise BuilderError("Description must contain Unicode scalar values; surrogate code points are unsupported.")
    quoted = json.dumps(value, ensure_ascii=False)
    return "".join("\\u%04x" % ord(char)
                   if 0x7F <= ord(char) <= 0x9F or ord(char) in {0x2028, 0x2029, 0xFFFE, 0xFFFF}
                   else char for char in quoted)


def bounded_read(path: Path, limit: int) -> bytes:
    """Read one explicit regular file, refusing a symlink in its last component."""
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise BuilderError("Expected a regular file; symbolic links and special files are refused.")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    with os.fdopen(descriptor, "rb") as stream:
        opened = os.fstat(stream.fileno())
        if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            raise BuilderError("File identity changed before reading.")
        data = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
    if len(data) > limit:
        raise BuilderError("Input exceeds the documented size limit.")
    if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
        raise BuilderError("File changed while being read; repeat against a stable snapshot.")
    return data


def safe_relative(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise BuilderError("Expected a portable relative content path.")
    path = PurePosixPath(value)
    if not path.parts or path.is_absolute() or ".." in path.parts or ":" in path.parts[0] or str(path) != value:
        raise BuilderError("Absolute, normalized, or escaping content paths are not accepted.")
    return value


class KnowledgeBase:
    """Read only the anchored supplied ZIP; preserve every original archive byte."""
    def __init__(self, references: Path = REFERENCE_ROOT,
                 expected_sha256: str = EXPECTED_ARCHIVE_SHA256):
        self.references = Path(references)
        self.manifest = parse_json(bounded_read(self.references / "knowledge-base-manifest.json", MAX_RECORD_BYTES))
        if not isinstance(self.manifest, dict) or self.manifest.get("archive") != "knowledge-base.zip":
            raise BuilderError("The knowledge-base manifest is malformed.")
        if self.manifest.get("archive_sha256") != expected_sha256:
            raise BuilderError("The knowledge-base manifest does not match the pinned archive identity.")
        self.archive_bytes = bounded_read(self.references / "knowledge-base.zip", MAX_ARCHIVE_BYTES)
        if len(self.archive_bytes) != self.manifest.get("archive_size_bytes") or sha256(self.archive_bytes) != expected_sha256:
            raise BuilderError("Knowledge-base archive identity mismatch; no content was used.")
        self.archive = zipfile.ZipFile(io.BytesIO(self.archive_bytes))
        infos = self.archive.infolist()
        if len(infos) > 4096 or len({i.filename for i in infos}) != len(infos):
            raise BuilderError("Archive has an unsupported entry count or duplicate names.")
        root = safe_relative(self.manifest.get("archive_root", ""))
        if "/" in root:
            raise BuilderError("The archive must have exactly one named content root.")
        self.files: dict[str, dict[str, Any]] = {}
        for row in self.manifest.get("files", []):
            if not isinstance(row, dict):
                raise BuilderError("Malformed knowledge-base content index.")
            path = safe_relative(row.get("path", ""))
            if path in self.files or row.get("archive_member") != root + "/" + path:
                raise BuilderError("Duplicate or inconsistent content-index path.")
            size = row.get("size_bytes")
            if type(size) is not int or not 0 <= size <= MAX_MEMBER_BYTES or not re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")):
                raise BuilderError("Malformed content size or SHA-256 identity.")
            self.files[path] = row
        actual = set()
        for info in infos:
            name = info.filename.rstrip("/")
            safe_relative(name)
            if stat.S_ISLNK(info.external_attr >> 16):
                raise BuilderError("Symbolic archive entries are refused.")
            p = PurePosixPath(name)
            if info.is_dir() or "__MACOSX" in p.parts or p.name == ".DS_Store":
                continue
            if not name.startswith(root + "/"):
                raise BuilderError("Unexpected archive content outside the indexed root.")
            relative = name[len(root) + 1:]
            actual.add(relative)
            if relative not in self.files or info.file_size != self.files[relative]["size_bytes"]:
                raise BuilderError("Archive content and indexed sizes disagree.")
        if actual != set(self.files) or len(self.files) != self.manifest.get("content_file_count"):
            raise BuilderError("Missing or extra substantive archive content.")
        if sum(r["size_bytes"] for r in self.files.values()) != self.manifest.get("content_bytes"):
            raise BuilderError("Knowledge-base indexed byte totals disagree.")

    def read(self, path: str) -> bytes:
        path = safe_relative(path)
        row = self.files.get(path)
        if row is None:
            raise BuilderError("Content path is not in the preserved knowledge-base index; use kb list.")
        data = self.archive.read(row["archive_member"])
        if len(data) != row["size_bytes"] or sha256(data) != row["sha256"]:
            raise BuilderError("Knowledge-base content failed its preserved SHA-256 identity check.")
        return data

    def json(self, path: str) -> Any:
        return parse_json(self.read(path))

    def verify(self) -> dict[str, Any]:
        for path in self.files:
            self.read(path)
        return {"outcome": "passed", "scope": "Exact archive and every indexed substantive file identity; no host or semantic assurance.",
                "archive_sha256": self.manifest["archive_sha256"], "archive_bytes": len(self.archive_bytes),
                "content_files": len(self.files), "content_bytes": self.manifest["content_bytes"],
                "all_original_archive_members_retained": True, "source_content_rewritten": False}


def is_live_skill_path(path: Path) -> bool:
    parts = {p.casefold() for p in path.parts}
    # Extraction must not make the preserved example skills host-discoverable.
    return bool(parts & {"skills", "remote-skills", ".agents", ".claude", ".codex", ".grok"})


def checked_destination(value: str, target: Path | None = None) -> Path:
    path = Path(value).expanduser().absolute()
    if path.name in {"", ".", ".."} or path.exists() or path.is_symlink():
        raise BuilderError("Choose a new output directory; existing paths are never overwritten.")
    if not path.parent.is_dir():
        raise BuilderError("The output parent directory must already exist.")
    for part in (path.parent, *path.parent.parents):
        if part.is_symlink():
            raise BuilderError("Output paths with symbolic-link ancestors are refused.")
    resolved = path.parent.resolve() / path.name
    if is_live_skill_path(resolved):
        raise BuilderError("Choose an artifact directory outside live skill/configuration roots.")
    if target is not None and resolved.is_relative_to(target):
        raise BuilderError("Audit output must be outside the inspected target.")
    return resolved


class OwnedPath:
    """Expected owned state, excluding access times changed by our own reads."""
    def __init__(self, path: Path, directory: bool, observed: os.stat_result):
        self.path = path
        self.directory = directory
        self.identity = (observed.st_dev, observed.st_ino)
        self.expected_ownership = self.ownership(observed)
        self.expected_links = observed.st_nlink
        self.expected = self.signature(observed)
        self.changed = False
        self.bytes_written = 0
        self.digest = hashlib.sha256()

    @staticmethod
    def ownership(observed: os.stat_result) -> tuple[Any, ...]:
        return (observed.st_dev, observed.st_ino, observed.st_mode, observed.st_uid, observed.st_gid,
                getattr(observed, "st_flags", None), getattr(observed, "st_file_attributes", None))

    @classmethod
    def signature(cls, observed: os.stat_result) -> tuple[Any, ...]:
        return (*cls.ownership(observed), observed.st_nlink, observed.st_size,
                observed.st_mtime_ns, observed.st_ctime_ns)

    def observe(self) -> os.stat_result:
        observed = self.path.lstat()
        if self.signature(observed) != self.expected:
            self.changed = True
        return observed

    def refresh_after_write(self, observed: os.stat_result) -> None:
        # Owned writes/child mutations change size, link count and timestamps,
        # but cannot explain a changed identity, type, mode, owner or flags.
        if (self.ownership(observed) != self.expected_ownership or
                not self.directory and observed.st_nlink != self.expected_links):
            self.changed = True
        self.expected = self.signature(observed)


class NewTree:
    """Exclusive output; caught failures preserve observed external changes."""
    def __init__(self, root: Path):
        self.root = root
        self.created: list[OwnedPath] = []
        self.owned: dict[Path, OwnedPath] = {}

    def remember(self, path: Path, directory: bool, observed: os.stat_result | None = None) -> OwnedPath:
        entry = OwnedPath(path, directory, observed if observed is not None else path.lstat())
        self.created.append(entry)
        self.owned[path] = entry
        return entry

    def before_child_change(self, parent: Path) -> None:
        for ancestor in (parent, *parent.parents):
            entry = self.owned.get(ancestor)
            if entry is not None:
                observed = entry.observe()
                if not stat.S_ISDIR(observed.st_mode) or (observed.st_dev, observed.st_ino) != entry.identity:
                    raise BuilderError("Output directory identity changed.")

    def after_child_change(self, parent: Path) -> None:
        entry = self.owned.get(parent)
        if entry is not None:
            entry.refresh_after_write(parent.lstat())

    def __enter__(self) -> "NewTree":
        self.root.mkdir(mode=0o700)
        self.remember(self.root, True)
        return self

    def write(self, relative: str, data: bytes) -> None:
        safe_relative(relative)
        current_root = self.root.lstat()
        if self.root.is_symlink() or (current_root.st_dev, current_root.st_ino) != self.created[0].identity:
            raise BuilderError("Output root identity changed.")
        target = self.root / relative
        parent = self.root
        for component in PurePosixPath(relative).parts[:-1]:
            parent = parent / component
            if not parent.exists():
                self.before_child_change(parent.parent)
                parent.mkdir(mode=0o700)
                self.remember(parent, True)
                self.after_child_change(parent.parent)
            if parent.is_symlink() or not parent.is_dir():
                raise BuilderError("Output directory identity changed.")
        self.before_child_change(parent)
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        try:
            entry = self.remember(target, False, os.fstat(descriptor))
            self.after_child_change(parent)
            remaining = memoryview(data)
            while remaining:
                count = os.write(descriptor, remaining)
                if not 0 < count <= len(remaining):
                    raise OSError("Output write made no supported progress.")
                entry.digest.update(remaining[:count])
                entry.bytes_written += count
                entry.refresh_after_write(os.fstat(descriptor))
                remaining = remaining[count:]
        finally:
            os.close(descriptor)

    def __exit__(self, kind: Any, value: Any, traceback: Any) -> bool:
        if kind is not None:
            for entry in reversed(self.created):
                try:
                    entry.observe()
                    if entry.changed:
                        continue
                    self.before_child_change(entry.path.parent)
                    if not entry.directory:
                        actual = bounded_read(entry.path, entry.bytes_written)
                        entry.observe()
                        if entry.changed or sha256(actual) != entry.digest.hexdigest():
                            continue
                    self.before_child_change(entry.path.parent)
                    entry.path.rmdir() if entry.directory else entry.path.unlink()
                    self.after_child_change(entry.path.parent)
                except (OSError, BuilderError):
                    pass  # Retain changed, unreadable, uncertain or nonempty state.
        return False


def load_overrides(path: str | None) -> dict[str, Any]:
    if path is None:
        return {}
    value = parse_json(bounded_read(Path(path).expanduser(), MAX_RECORD_BYTES))
    if not isinstance(value, dict):
        raise BuilderError("Rule overrides must be a JSON object.")
    return value


def select_profile(kb: KnowledgeBase, profile: str, modifiers: list[str], overrides: dict[str, Any]) -> dict[str, Any]:
    """Project selection joins canonical data, preserving every original statement."""
    catalog = kb.json("catalogs/requirements.json")["rules"]
    policy = kb.json("catalogs/application-profiles.json")
    known = {r["id"] for r in catalog}
    if len(known) != 99 or len(catalog) != 99 or profile not in policy["profiles"]:
        raise BuilderError("Canonical rule/profile cardinality is invalid.")
    if set(overrides) - known or set(modifiers) - set(policy["modifiers"]):
        raise BuilderError("Unknown rule override or capability modifier.")
    adopted = set(policy["profiles"][profile]["adopted_rule_ids"])
    for modifier in modifiers:
        adopted.update(policy["modifiers"][modifier]["adopted_rule_ids"])
    unassessed = set(policy["unselected_review_rule_ids"])
    rows = []
    for rule in catalog:
        rid = rule["id"]
        decision = "adopted" if rid in adopted else "not_assessed" if rid in unassessed else "not_applicable"
        reason = ("Selected by profile or capability modifier." if decision == "adopted" else
                  "Review whether this additional mechanism exists before deciding." if decision == "not_assessed" else
                  "The selected profile and declared modifiers do not include this capability; verify that declared scope before accepting the exclusion.")
        if rid in overrides:
            item = overrides[rid]
            if not isinstance(item, dict) or set(item) != {"decision", "reason"} or item["decision"] not in {"adopted", "not_applicable", "not_assessed"} or not isinstance(item["reason"], str) or len(item["reason"].strip()) < 20:
                raise BuilderError("Each override needs a known decision and a concrete reason of at least 20 characters.")
            decision, reason = item["decision"], item["reason"]
        rows.append({**rule, "rule_id": rid, "decision": decision, "reason": reason, "override": rid in overrides})
    return {"schema_version": "1.0.0", "outcome": "selected", "profile": profile, "modifiers": sorted(set(modifiers)),
            "canonical_rules": "knowledge-base.zip!catalogs/requirements.json", "archive_sha256": kb.manifest["archive_sha256"],
            "note": "Selection is not verification. Confirm scope, every exclusion, and unresolved mechanisms before release.", "rules": rows}


def traceability(selection: dict[str, Any], project: str) -> dict[str, Any]:
    rows = []
    for rule in selection["rules"]:
        adopted = rule["decision"] == "adopted"
        rows.append({"rule_id": rule["rule_id"], "decision": rule["decision"], "reason": rule["reason"],
                     "local_policy": rule["basis"] == "project", "override": rule["override"],
                     "failure_scenario": "Review and specify the task-specific failure that this rule prevents: " + rule["statement"],
                     "source_ids": rule["source_ids"],
                     "verification": {"method": "not_run", "procedure": rule["verification"],
                                      "outcome": "not_run" if rule["decision"] != "not_applicable" else "not_applicable"},
                     "evidence": [], "release_consequence":
                     ("Block release until this adopted required rule has sufficient evidence or an explicit reviewed policy disposition." if adopted and rule["strength"] == "required" else
                      "Review this recommendation, scope exclusion, or unresolved mechanism and record the release decision; no pass is implied.")})
    return {"schema_version": "2.0", "record_type": "rule-traceability", "project": project,
            "profile": selection["profile"], "modifiers": selection["modifiers"],
            "selected_at": dt.datetime.now(dt.timezone.utc).isoformat(), "records": rows}


def source_identity(kb: KnowledgeBase) -> dict[str, Any]:
    return {"builder_version": VERSION, "knowledge_base_archive_sha256": kb.manifest["archive_sha256"],
            "source_content_condensed": False, "source_rules": "catalogs/requirements.json",
            "evidence_boundary": "Generated scaffolding and static observations do not establish semantic compliance or live host behavior."}


def write_evaluation_support(output: NewTree, mode: str, subject: str) -> None:
    """Supplemental, visibly unfinished worksheets; no target verdicts."""
    assets = SKILL_ROOT / "assets" / "evaluation"
    for source, destination in (("routing.json.template", "evals/routing.json.template"),
                                ("execution.json.template", "evals/execution.json.template"),
                                ("environment.json.template", "evals/environment.json.template"),
                                ("contract.json.template", "workflow-contract.json.template"),
                                ("papercut.json.template", "papercut.json.template"),
                                ("ABLATION.md.template", "ABLATION-PLAN.md"),
                                ("PLAN.md.template", "EVALUATION-PLAN.md"),
                                ("REVIEW.md.template", "EVALUATION-REVIEW.md")):
        # A target directory name is data, never shell source or JSON syntax.
        raw = bounded_read(assets / source, 128 * 1024).decode("utf-8")
        replacement = json.dumps(subject, ensure_ascii=False)[1:-1] if source.endswith(".json.template") else subject.replace("\n", " ").replace("\r", " ")
        output.write(destination, raw.replace("SUBJECT", replacement).replace("MODE", mode).encode("utf-8"))
    topics = ("task_value", "metadata_portability", "routing", "execution_benefit",
              "independent_grading", "context_resources", "trust_recovery", "claims_operations",
              "trajectory", "spec_traceability", "field_feedback", "ablation")
    output.write("evaluation-review.json", json_bytes({
        "schema_version": "1.0.0", "record_type": "skill-builder-evaluation-review",
        "mode": mode, "subject": subject, "semantic_review_performed": False,
        "items": [{"id": topic, "applicability": "not_assessed", "outcome": "not_run",
                   "reason": "Requires task-specific assessment.", "evidence": [], "finding_ids": []}
                  for topic in topics]}))


def create_project(args: argparse.Namespace, kb: KnowledgeBase) -> int:
    if not 1 <= len(args.name) <= 64 or not NAME_RE.fullmatch(args.name):
        raise BuilderError("Name must be 1–64 lowercase ASCII letters/digits with single interior hyphens.")
    if not args.description.strip() or len(args.description) > 1024 or "\0" in args.description:
        raise BuilderError("Description must be nonblank, NUL-free, and at most 1,024 characters.")
    description_scalar = yaml_quoted_scalar(args.description)
    destination = checked_destination(args.output)
    selection = select_profile(kb, args.profile, args.modifier, load_overrides(args.overrides))
    draft = kb.read("templates/minimal-project/skills/example-skill/SKILL.md.template").decode("utf-8")
    draft = draft.replace("name: example-skill", "name: " + args.name, 1)
    draft = draft.replace("description: Replace this with the concrete task, output and trigger boundaries before distribution.",
                          "description: " + description_scalar, 1)
    draft = draft.replace("# Example skill", "# " + args.name + "\n\n**DRAFT: complete the bracketed task contract and evidence before distribution.**", 1)
    with NewTree(destination) as output:
        output.write("skills/" + args.name + "/SKILL.md", draft.encode("utf-8"))
        output.write("evidence/rule-selection.json", json_bytes(selection))
        output.write("evidence/rule-traceability.json", json_bytes(traceability(selection, args.name)))
        output.write("evidence/source-identity.json", json_bytes(source_identity(kb)))
        for name in ("host-capabilities.json", "evaluation-receipt.json", "install-manifest.json", "finding.json"):
            output.write("evidence/templates/" + name + ".template", kb.read("templates/" + name + ".template"))
        for name in ("README.md", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md", "CHANGELOG.md", "NOTICE.md"):
            output.write("project-templates/" + name + ".template", kb.read("templates/minimal-project/" + name + ".template"))
        for name in ("CREATE-PROJECT-INSTRUCTIONS.md", "INSTRUCTION-WORKSHEET.md.template", "AUDIT-REPORT.md.template"):
            output.write("workflows/" + name, kb.read("templates/" + name))
        output.write("README.md", ("# " + args.name + " development scaffold\n\nThis project is incomplete. The CLI created a portable draft and all 99 rule decisions; it did not implement or evaluate the requested task.\n\n"
                     "## Complete the work\n\n1. Define inputs, examples, acceptance conditions, exclusions, effects, and existing authority in `TASK-BRIEF.md`.\n2. Complete the draft skill and use the preserved creation workflow.\n3. Review every rule decision, including default exclusions. Record actual evidence separately from proposals.\n4. Fill the relevant evidence templates and preserve unknown outcomes and usage.\n5. Validate distributed resources and exercise each claimed host; a format pass cannot prove host support.\n6. Select licensing as the rights holder and replace governance templates with actual project information.\n\nComplete EVALUATION-PLAN.md, EVALUATION-REVIEW.md and evaluation-review.json for this subject; adapt evals/*.json.template into domain-specific cases and a fixed held-out split. The installed builder scripts/evaluate.py accepts explicit target cases/fixtures. Preparation is not an evaluation pass.\n\nNo installation, dependency download, publication, or target execution was performed.\n").encode())
        output.write("TASK-BRIEF.md", ("# Task brief\n\nStatus: awaiting task-specific implementation and review.\n\n"
                     "| Field | Required decision |\n|---|---|\n| Result | Define the user-visible result and acceptance oracle. |\n| Examples | Add positive, negative, boundary, and ambiguous requests. |\n| Inputs | Define required inputs, useful defaults, validation and missing-input behavior. |\n| Scope | Define exclusions and conditions that change the workflow. |\n| Effects | Identify local writes, network, external actions, state and current authority. |\n| Hosts | Select exact product, surface, version, OS and policy; keep untested axes unrun. |\n| Resources | Define deterministic contracts, failure states, limits and recovery when needed. |\n| Evaluation | Freeze cases, acceptance checks, control, retries, exclusions and budgets before trials. |\n| Release | Choose owner, license, maintenance, packaging and recovery policy. |\n").encode())
        output.write("LICENSE-DECISION.md", b"# License decision required\n\nThe scaffold does not assign a license. The rights holder must select terms for original work and retain applicable upstream notices before public open reuse.\n")
        write_evaluation_support(output, "create", args.name)
    emit({"outcome": "scaffold_created", "output": str(destination), "skill": "skills/" + args.name + "/SKILL.md",
          "rule_decisions": 99, "semantic_implementation": "not_run", "host_trials": "not_run", "release_ready": False,
          "evaluation_plan": "EVALUATION-PLAN.md", "evaluation_review": "evaluation-review.json"})
    return 0


def inspect_tree(root: Path, max_files: int, max_file_bytes: int, max_total_bytes: int,
                 max_entries: int = 50000) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    omissions: list[dict[str, Any]] = []
    total = 0
    stopped = False
    entries_seen = 0
    def walk(directory: Path, depth: int = 0) -> None:
        nonlocal total, stopped, entries_seen
        if depth > 128:
            omissions.append({"path": directory.relative_to(root).as_posix(), "reason": "maximum_directory_depth_128"})
            return
        if entries_seen >= max_entries:
            omissions.append({"path": directory.relative_to(root).as_posix(), "reason": "max_entries_reached; directory entries were not enumerated"})
            return
        truncated_directory = False
        try:
            entries = []
            with os.scandir(directory) as stream:
                while entries_seen < max_entries:
                    try:
                        entry = next(stream)
                    except StopIteration:
                        break
                    # Charge names when obtained, before recursive processing.
                    # Prefetched sibling entries must consume the same global
                    # budget as entries processed immediately. No lookahead is
                    # used when the budget is exhausted.
                    entries_seen += 1
                    entries.append(entry)
                else:
                    truncated_directory = True
            entries.sort(key=lambda entry: entry.name)
        except OSError:
            omissions.append({"path": directory.relative_to(root).as_posix(), "reason": "directory_inaccessible"})
            return
        for entry in entries:
            if stopped:
                return
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            if len(files) >= max_files:
                omissions.append({"path": relative, "reason": "max_files_reached; remaining tree was not enumerated"})
                stopped = True
                return
            try:
                info = entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    files.append({"path": relative, "kind": "symlink", "status": "not_followed", "review_depth": "symlink_metadata"})
                    omissions.append({"path": relative, "reason": "symlink_content_not_followed"})
                elif stat.S_ISDIR(info.st_mode):
                    if entry.name in EXCLUDED_DIRS:
                        omissions.append({"path": relative, "reason": "explicit_development_or_git_metadata_exclusion"})
                    else:
                        if not path.resolve().is_relative_to(root):
                            raise BuilderError("Directory path changed outside the target boundary.")
                        walk(path, depth + 1)
                elif stat.S_ISREG(info.st_mode):
                    row = {"path": relative, "kind": "regular_file", "size_bytes": info.st_size,
                           "mode": oct(stat.S_IMODE(info.st_mode)), "review_depth": "structural_index"}
                    if info.st_size > max_file_bytes or total + info.st_size > max_total_bytes:
                        row.update(status="not_read", sha256=None)
                        omissions.append({"path": relative, "reason": "file_or_total_byte_budget"})
                    else:
                        if not path.resolve().is_relative_to(root):
                            raise BuilderError("File path changed outside the target boundary.")
                        data = bounded_read(path, min(max_file_bytes, max_total_bytes - total))
                        total += len(data)
                        row.update(status="hashed", sha256=sha256(data))
                    files.append(row)
                else:
                    files.append({"path": relative, "kind": "special_file", "status": "not_read", "review_depth": "metadata_only"})
                    omissions.append({"path": relative, "reason": "special_file_not_read"})
            except (OSError, BuilderError):
                omissions.append({"path": relative, "reason": "unreadable_or_changed_path"})
        if truncated_directory:
            omissions.append({"path": directory.relative_to(root).as_posix(), "reason": "max_entries_reached; further enumeration was not attempted and completeness is unknown"})
    walk(root)
    material_omissions = [x for x in omissions if x["reason"] != "explicit_development_or_git_metadata_exclusion"]
    return {"schema_version": "1.0.0", "target": str(root), "identity_scope": "current filesystem bytes; not an immutable Git commit or distributed package",
            "files": files, "files_recorded": len(files), "entries_seen": entries_seen, "bytes_hashed": total, "omissions": omissions,
            "coverage": "incomplete" if material_omissions else "complete_within_declared_exclusions",
            "tracked_git_coverage": "unknown; Git was not invoked and .git content was excluded",
            "limits": {"max_files": max_files, "max_entries": max_entries, "max_directory_depth": 128,
                       "max_file_bytes": max_file_bytes, "max_total_bytes": max_total_bytes},
            "candidate_code_executed": False, "semantic_review_performed": False,
            "filesystem_race_boundary": "Point-in-time checks, not an operating-system sandbox against adversarial concurrent replacement."}


def trusted_module(kb: KnowledgeBase, path: str) -> types.ModuleType:
    """Execute only SHA-verified supplied utility bytes, never candidate content."""
    source = kb.read(path)
    module = types.ModuleType("skill_builder_preserved_" + Path(path).stem)
    module.__file__ = str(REFERENCE_ROOT / "knowledge-base.zip" / path)
    exec(compile(source, module.__file__, "exec"), module.__dict__)
    return module


def format_checks(kb: KnowledgeBase, target: Path, inventory: dict[str, Any]) -> dict[str, Any]:
    selected = [target / row["path"] for row in inventory["files"] if row.get("kind") == "regular_file" and row.get("status") == "hashed" and PurePosixPath(row["path"]).name == "SKILL.md"]
    if not selected:
        return {"outcome": "blocked", "reason": "No readable actual SKILL.md was selected from this inventory.", "skills": []}
    module = trusted_module(kb, "tools/validate_skill.py")
    if module.yaml is None:
        return {"outcome": "blocked", "reason": "PyYAML is unavailable; provision reviewed dependencies explicitly.", "skills": []}
    reports = [module.validate_skill(path.parent) for path in selected]
    return {"outcome": "failed" if any(x["status"] == "failed" for x in reports) else "passed",
            "scope": "Implemented portable format and direct-resource checks only.",
            "validator": {"version": module.VERSION, "profile": module.PROFILE, "PyYAML": module.yaml.__version__, "tested_PyYAML": module.OBSERVED_PYYAML_VERSION},
            "skills": reports, "not_checked": module.NOT_CHECKED}


def audit_project(args: argparse.Namespace, kb: KnowledgeBase) -> int:
    target_input = Path(args.target).expanduser().absolute()
    if target_input.is_symlink() or not target_input.is_dir():
        raise BuilderError("Audit target must be an explicit existing nonsymlink directory.")
    target = target_input.resolve(strict=True)
    destination = checked_destination(args.output, target)
    selection = select_profile(kb, args.profile, args.modifier, load_overrides(args.overrides))
    inventory = inspect_tree(target, args.max_files, args.max_file_bytes, args.max_total_bytes, args.max_entries)
    checks = format_checks(kb, target, inventory)
    identity_before = {r["path"]: r.get("sha256") for r in inventory["files"] if r.get("status") == "hashed"}
    changed = []
    for path, digest in identity_before.items():
        try:
            if sha256(bounded_read(target / path, args.max_file_bytes)) != digest:
                changed.append(path)
        except (OSError, BuilderError):
            changed.append(path)
    result = {"outcome": "static_preparation_completed", "audit_verdict": "inconclusive", "output": str(destination),
              "static_checks": checks["outcome"], "inventory_coverage": inventory["coverage"], "changed_during_check": changed,
              "full_semantic_review": "not_run", "host_trials": "not_run", "target_code_executed": False, "release_ready": False,
              "evaluation_plan": "EVALUATION-PLAN.md", "evaluation_review": "evaluation-review.json"}
    if changed:
        result["static_checks"] = "failed"
        result["audit_verdict"] = "failed"
    elif checks["outcome"] == "failed":
        result["audit_verdict"] = "failed"
    with NewTree(destination) as output:
        output.write("inventory.json", json_bytes(inventory))
        output.write("static-checks.json", json_bytes(checks))
        output.write("rule-selection.json", json_bytes(selection))
        output.write("rule-traceability.json", json_bytes(traceability(selection, target.name)))
        output.write("source-identity.json", json_bytes(source_identity(kb)))
        output.write("summary.json", json_bytes(result))
        output.write("AUDIT-REPORT.md.template", kb.read("templates/AUDIT-REPORT.md.template"))
        output.write("INSTRUCTION-WORKSHEET.md.template", kb.read("templates/INSTRUCTION-WORKSHEET.md.template"))
        output.write("AUDIT-PROJECT-INSTRUCTIONS.md", kb.read("templates/AUDIT-PROJECT-INSTRUCTIONS.md"))
        write_evaluation_support(output, "audit", target.name)
        output.write("README.md", ("# Audit preparation\n\nVerdict: " + result["audit_verdict"] + ". This is static evidence and an assessment workspace, not a completed semantic audit.\n\n"
                     "## Evidence\n\n`inventory.json` records bounded filesystem identities and all omissions. `static-checks.json` records the preserved portable validator's exact scope and limits. `rule-traceability.json` contains all 99 decisions with no invented passing evidence.\n\n"
                     "## Complete the audit\n\nRead the full preserved audit instructions, inspect authoritative instructions and relevant implementation owners, evaluate every adopted rule and scope exclusion, add evidence-linked findings, and execute only separately authorized reviewed checks. Fill the report template. Keep static inference, reproduced behavior, documentation, and recommendations separate. Do not inherit historical host/test passes for changed bytes.\n\n"
                     "Complete EVALUATION-REVIEW.md and evaluation-review.json with target evidence about routing, controls, independent grading, context/resources and supported claims. EVALUATION-PLAN.md and evals/*.json.template support separately authorized target-specific verification; builder test results do not establish target quality.\n\n"
                     "No candidate script, test, hook, installer, or repository configuration was executed. No Git commit identity or tracked-file completeness is claimed. Host discovery, functional behavior, permissions, and maintenance support remain untested.\n").encode())
    emit(result)
    if checks["outcome"] == "blocked":
        return 2
    return 1 if changed or checks["outcome"] == "failed" or inventory["coverage"] == "incomplete" else 0


def read_page(kb: KnowledgeBase, path: str, offset: int, limit: int,
              expected_sha256: str | None = None) -> dict[str, Any]:
    """An exact UTF-8 byte range, with a stable identity and a resume cursor."""
    if type(offset) is not int or offset < 0 or type(limit) is not int or not 4 <= limit <= 16384:
        raise BuilderError("Read offset must be nonnegative; limit must be 4–16,384 bytes.")
    if offset and expected_sha256 is None:
        raise BuilderError("Resuming a read requires --sha256 from the first page.")
    raw = kb.read(path)
    digest = sha256(raw)
    if expected_sha256 is not None and expected_sha256 != digest:
        raise BuilderError("Read source identity differs from --sha256; do not combine these pages.")
    try:
        raw.decode("utf-8")
        if b"\0" in raw:
            raise UnicodeError
    except UnicodeError as exc:
        raise BuilderError("Selected content is binary; use kb extract for exact binary access.") from exc
    if offset > len(raw) or offset < len(raw) and raw[offset] & 0xC0 == 0x80:
        raise BuilderError("Read offset must be within the file at a UTF-8 character boundary.")
    stop = min(len(raw), offset + limit)
    while stop < len(raw) and raw[stop] & 0xC0 == 0x80:
        stop -= 1
    chunk = raw[offset:stop]
    return {"outcome": "read", "path": path, "sha256": digest,
            "archive_sha256": kb.manifest["archive_sha256"], "total_bytes": len(raw),
            "offset": offset, "returned_bytes": len(chunk), "text": chunk.decode("utf-8"),
            "next_offset": stop if stop < len(raw) else None, "complete": stop == len(raw)}


def search(kb: KnowledgeBase, query: str, prefix: str, offset: int, limit: int, case_sensitive: bool) -> dict[str, Any]:
    if not query or len(query) > 4096:
        raise BuilderError("Search requires a nonempty literal query of at most 4,096 characters.")
    if prefix:
        safe_relative(prefix.rstrip("/"))
    needle = query if case_sensitive else query.casefold()
    matches, total, skipped = [], 0, []
    for path in sorted(kb.files):
        if not path.startswith(prefix):
            continue
        raw = kb.read(path)
        try:
            body = raw.decode("utf-8")
            if "\0" in body:
                raise UnicodeError
        except UnicodeError:
            skipped.append(path)
            continue
        for number, line in enumerate(body.splitlines(), 1):
            haystack = line if case_sensitive else line.casefold()
            if needle not in haystack:
                continue
            if offset <= total < offset + limit:
                # A JSONL or HTML line may be very large; previews are navigation only.
                index = haystack.find(needle)
                start = max(0, index - 80)
                preview = line[start:start + 360]
                matches.append({"path": path, "line": number, "preview": preview,
                                "preview_truncated": start > 0 or start + len(preview) < len(line)})
            total += 1
    return {"outcome": "searched", "mode": "literal", "case_sensitive": case_sensitive, "offset": offset, "limit": limit,
            "total_matching_lines": total, "returned": len(matches), "next_offset": offset + len(matches) if offset + len(matches) < total else None,
            "matches": matches, "binary_files_not_searched": skipped,
            "note": "Previews are explicitly bounded navigation. Use kb read PATH for the complete exact file; no source content was modified."}


def check_records(kb: KnowledgeBase, paths: list[str]) -> dict[str, Any]:
    try:
        # The original checker prints dependency errors at import. Keep those in
        # the private buffer and provide a stable wrapper error without raw data.
        with contextlib.redirect_stdout(io.StringIO()):
            module = trusted_module(kb, "tools/validate_records.py")
    except (ImportError, SystemExit):
        return {"outcome": "blocked", "reason": "Evidence checking requires the pinned jsonschema/referencing dependencies; nothing was installed.", "records": []}
    results = []
    with tempfile.TemporaryDirectory(prefix="skill-builder-evidence-") as directory:
        root = Path(directory)
        for name in list(kb.files):
            if name.startswith("schemas/") and name.endswith(".schema.json") or name == "catalogs/requirements.json":
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(kb.read(name))
        known = module.validators(root)
        for value in paths:
            try:
                try:
                    record_path = Path(value).expanduser()
                except RuntimeError as exc:
                    # An unknown ~user is a bad record path, not a validator or
                    # environment-wide failure. Keep this catch path-specific.
                    raise BuilderError("Record path could not be expanded.") from exc
                record = parse_json(bounded_read(record_path, MAX_RECORD_BYTES))
                if (not isinstance(record, dict) or not isinstance(record.get("record_type"), str)
                        or record["record_type"] not in known):
                    raise BuilderError("Record must be an object with a supported string record_type.")
                errors = module.validate_record(record, known, root)
                results.append({"path": value, "outcome": "failed" if errors else "passed", "error_count": len(errors),
                                "reason": "Detailed input-value diagnostics suppressed; inspect with the preserved checker in a private environment." if errors else None})
            except BuilderError as exc:
                results.append({"path": value, "outcome": "failed", "error_count": 1, "reason": str(exc)})
            except OSError:
                results.append({"path": value, "outcome": "failed", "error_count": 1, "reason": "Record could not be read."})
    return {"outcome": "failed" if any(r["outcome"] == "failed" for r in results) else "passed",
            "scope": "Original versioned schema and cross-field checks; truth of evidence was not verified.", "records": results}


def positive(value: str) -> int:
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Expected an integer.") from exc
    if result < 1:
        raise argparse.ArgumentTypeError("Expected a positive integer.")
    return result


def parser() -> argparse.ArgumentParser:
    root = JsonParser(description=__doc__)
    root.add_argument("--version", action="version", version="skill-builder " + VERSION)
    commands = root.add_subparsers(dest="command", required=True, parser_class=JsonParser)
    def scope(p: argparse.ArgumentParser) -> None:
        p.add_argument("--profile", choices=PROFILES, required=True)
        p.add_argument("--modifier", choices=MODIFIERS, action="append", default=[])
        p.add_argument("--overrides", help="Explicit local JSON of rule decisions/reasons; no existing files are changed.")
    create = commands.add_parser("skill-builder-create", help="Create an incomplete project scaffold and all 99 rule decisions.")
    create.add_argument("--name", required=True)
    create.add_argument("--description", required=True)
    create.add_argument("--output", required=True, help="New project directory outside installed skill/configuration roots; parent must exist.")
    scope(create)
    audit = commands.add_parser("skill-builder-audit", help="Prepare a read-only target inventory, static checks, and an incomplete audit workspace.")
    audit.add_argument("--target", required=True, help="Existing nonsymlink directory; candidate code is never executed.")
    audit.add_argument("--output", required=True, help="New directory outside the target and installed skill roots.")
    audit.add_argument("--max-files", type=positive, default=10000)
    audit.add_argument("--max-entries", type=positive, default=50000, help="Total files and directories inspected; directory depth is capped at 128.")
    audit.add_argument("--max-file-bytes", type=positive, default=16 * 1024 * 1024)
    audit.add_argument("--max-total-bytes", type=positive, default=128 * 1024 * 1024)
    scope(audit)
    profiles = commands.add_parser("profile", help="Return all canonical rules plus scope decisions; no compliance verdict.")
    scope(profiles)
    kb = commands.add_parser("kb", help="Verify, list, read, search, or explicitly extract the preserved archive.")
    kb_commands = kb.add_subparsers(dest="kb_command", required=True, parser_class=JsonParser)
    kb_commands.add_parser("verify", help="Check archive SHA-256 and all indexed substantive file hashes.")
    listing = kb_commands.add_parser("list", help="List complete indexed content paths and sizes.")
    listing.add_argument("--prefix", default="")
    reading = kb_commands.add_parser("read", help="Write one complete exact UTF-8 file to stdout, without a JSON wrapper.")
    reading.add_argument("path")
    reading.add_argument("--offset", type=int, help="Return a JSON byte-range page starting here; default 0 when --limit is used.")
    reading.add_argument("--limit", type=positive, help="Page content-byte budget, 4–16,384; default 4,096. UTF-8 characters stay intact.")
    reading.add_argument("--sha256", help="Expected whole-file SHA-256; required when resuming after offset 0.")
    searching = kb_commands.add_parser("search", help="Search literal text offline, with explicit bounded previews and pagination.")
    searching.add_argument("query")
    searching.add_argument("--path", default="", help="Optional content path prefix.")
    searching.add_argument("--offset", type=int, default=0)
    searching.add_argument("--limit", type=positive, default=20, help="Matching lines per page, 1–200.")
    searching.add_argument("--case-sensitive", action="store_true")
    extract = kb_commands.add_parser("extract", help="Extract all substantive source files to a new non-skill directory; never execute them.")
    extract.add_argument("--output", required=True)
    checks = commands.add_parser("check", help="Verify source preservation and optionally original evidence schemas; no host assurance.")
    checks.add_argument("--record", action="append", default=[], help="Explicit evidence record; repeat for multiple records.")
    return root


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        if (args.command == "skill-builder-audit" or args.command == "check" and args.record) and not sys.flags.isolated:
            raise BuilderError("Run this operation with python3 -I -B so target/CWD/PYTHONPATH cannot supply dependency imports.")
        kb = KnowledgeBase()
        if args.command == "skill-builder-create":
            return create_project(args, kb)
        if args.command == "skill-builder-audit":
            return audit_project(args, kb)
        if args.command == "profile":
            emit(select_profile(kb, args.profile, args.modifier, load_overrides(args.overrides)))
            return 0
        if args.command == "check":
            result = {"preservation": kb.verify()}
            if args.record:
                result["records"] = check_records(kb, args.record)
            outcome = result.get("records", {}).get("outcome", "passed")
            emit({"outcome": outcome, **result})
            return 2 if outcome == "blocked" else 1 if outcome == "failed" else 0
        if args.kb_command == "verify":
            emit(kb.verify())
        elif args.kb_command == "list":
            if args.prefix:
                safe_relative(args.prefix.rstrip("/"))
            rows = [{"path": p, "size_bytes": r["size_bytes"], "sha256": r["sha256"]} for p, r in sorted(kb.files.items()) if p.startswith(args.prefix)]
            emit({"outcome": "listed", "count": len(rows), "files": rows, "archive_content_total": len(kb.files), "complete_for_prefix": True})
        elif args.kb_command == "read":
            if args.offset is not None or args.limit is not None:
                emit(read_page(kb, args.path, args.offset if args.offset is not None else 0,
                               args.limit if args.limit is not None else 4096, args.sha256))
                return 0
            raw = kb.read(args.path)
            if args.sha256 is not None and sha256(raw) != args.sha256:
                raise BuilderError("Read source identity differs from --sha256.")
            try:
                raw.decode("utf-8")
                if b"\0" in raw:
                    raise UnicodeError
            except UnicodeError as exc:
                raise BuilderError("Selected content is binary; use kb extract to preserve its exact bytes.") from exc
            sys.stdout.buffer.write(raw)
        elif args.kb_command == "search":
            if args.offset < 0 or args.limit > 200:
                raise BuilderError("Search offset must be nonnegative and limit must be 1–200.")
            emit(search(kb, args.query, args.path, args.offset, args.limit, args.case_sensitive))
        elif args.kb_command == "extract":
            destination = checked_destination(args.output)
            kb.verify()
            with NewTree(destination) as output:
                for name in sorted(kb.files):
                    output.write(name, kb.read(name))
            emit({"outcome": "extracted", "output": str(destination), "content_files": len(kb.files),
                  "content_rewritten": False, "code_executed": False,
                  "metadata": "macOS filesystem sidecars remain preserved in the original ZIP; only substantive source files were extracted."})
        return 0
    except (BuilderError, OSError, zipfile.BadZipFile, KeyError, TypeError, ValueError) as exc:
        # Only our own contract messages are emitted; never dump source/parser bodies.
        message = str(exc) if isinstance(exc, BuilderError) else "Operation could not complete; inspect paths, permissions, archive integrity, and supported inputs."
        emit({"outcome": "blocked", "error": message, "exception_type": type(exc).__name__, "assurance": "No completed semantic or host assurance is implied."})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
