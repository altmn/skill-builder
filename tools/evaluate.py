#!/usr/bin/env python3
"""Repository adapter for the installed, target-specific evaluation helper.

Without case flags this adapter selects the builder's own development corpus.
The installed helper requires explicit target case files and a fixture root.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).absolute().parents[1]
spec = importlib.util.spec_from_file_location(
    "skill_builder_evaluation", ROOT / "skills/skill-builder/scripts/evaluate.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

# Keep the repository analysis API; computation has one runtime owner.
for name in ("builder", "read_json", "identity", "validate_corpus", "schedule",
             "evidence", "activation", "confusion", "summarize"):
    globals()[name] = getattr(engine, name)


def prepare(*args, **kwargs):
    kwargs.setdefault("default_cases_root", ROOT / "evals")
    return engine.prepare(*args, **kwargs)


if __name__ == "__main__":
    raise SystemExit(engine.main(default_cases_root=ROOT / "evals"))
