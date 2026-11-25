# Fresh local release receipt: exact sequence and schema rules

This is a preparation recipe, not a passing result for the edited release. The separate `preserved-validator-tests-current.json` and `.log` record the one fresh run performed by this audit: 73 archived validator tests passed, with no failures, errors or skips. The project release integrator owns execution against the completed current candidate.

## Preserve the original and distinguish historical evidence

The uploaded source ZIP has SHA-256 `624d313a45a15749c75a5251b53c40408808ba1ee3c7149e2d4697635bd06588`, size 12,685,526 bytes and 71 files. The original generated manifest covers 70 payload files, excludes itself, and matches every uploaded member. Its payload identity is `96a109e5f0a4180a276ff62a6a61b188a868e18793c21e3c3a6c47a9ef657f51`.

Keep all 71 relative file paths in the updated source package. Necessary code, version, licensing and current documentation changes should be listed with their original and new hashes. A retained path alone does not prove that an edited document retained every meaningful instruction; that requires review of the actual changes.

Keep `skills/skill-builder/references/knowledge-base.zip` and `knowledge-base-manifest.json` byte for byte. The ZIP hash is `9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204`; its size is 11,572,664 bytes. It has 454 entries: 411 non-directory members, of which 182 are substantive files totaling 76,965,199 uncompressed bytes. Retaining the exact ZIP also retains its original metadata members, compression and archive metadata. Do not expand the KB into the final runtime/source package as an additional discoverable skill tree.

Preserve the 25 original validation artifacts other than `validation/README.md` exactly. The README is a current index and can identify those files as history. Add new results under new filenames. Historical licensing conclusions describe their recorded release and scope; a new authorized licensing decision needs its own current statement rather than an altered old result.

The original `final-local-evaluation-receipt.json` is a version 2.0 receipt for the original 47-test panel and runtime ZIP hash `28083dd9c2f0593d1562b9a8ef2b9c6c76c9076b1d188eca2b10b7a4ce7f35e2`. Its five input hashes and four embedded evidence references match the uploaded release. This audit did not recreate that old runtime ZIP. The earlier `local-evaluation-receipt.json` correctly records two pre-final input hashes that differ from the uploaded release; the original README already identifies it as development history. Neither file is execution evidence for the edited candidate.

`compare_preservation.py` reports historical receipt identities and recorded-input differences explicitly as information. It never interprets an old pass as a new pass.

## Freeze and execute the current local panel

1. Finish the current runtime code, tests, version, docs and scoped licensing records. Inspect all executing/imported project code, test modules and hooks before execution. Use the available Python environment; no automatic dependency download is needed. This audit observed Python 3.12.14, PyYAML 6.0.3, jsonschema 4.26.0 and referencing 0.37.0.
2. Before the first attempt, save a panel-definition document with the exact required commands, test selection, acceptance criteria, input snapshot, retry/exclusion policies and scope. Hash its exact bytes for `panel.sha256`. Record the real freeze timestamp in `panel.acceptance_frozen_at`. Acceptance criteria should address actual failures, errors, required skips, output identities and preservation, without claiming native hosts were exercised.
3. Capture each command separately with actual argv, cwd, start/end timestamps, measured elapsed time, exit status, limits enforced, complete combined log, log byte count and SHA-256. Hash the actual test files, helper, builder, project checker, loaded schema/KB, version and other selected build inputs before and after execution. If an executing input changes, retain the attempt and rerun against the new stable snapshot.
4. Run these commands from the completed source root, using isolated Python. The wrappers' exact limits should reflect what the caller really enforces; do not copy a historical capture-policy assertion.

```sh
python3 -I -B -m unittest discover -s tests -v
python3 -I -B tools/check_project.py --require-validators
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb verify
```

The full project suite includes the current regression tests. A separate portable-format execution is already part of `check_project.py` if its current inspected implementation retains that call. Test counts come from the new log; do not copy 47 from the old record.

5. A fresh archived validator run can use the separate, unchanged extracted tree already prepared for this audit. The exact command is:

```sh
python3 -I -B -m unittest discover -s /workspace/scratch/ce88fda257c5/evidence/preservation/preserved-source/agent-skill-project-knowledge-base_final/tools/tests -v
```

The extraction contains all 182 substantive files. Its validator modules load only their known local catalogs/schemas plus installed PyYAML/jsonschema/referencing; the reviewed tests use disposable fixtures and invoke the preserved format validator. Set `TMPDIR` to an owned scratch directory and remove inherited `PYTHONPATH`/`PYTHONHOME` for child CLI processes. This audit inspected those modules first, captured a full 10,840-byte log, and verified afterward that all 182 extracted file hashes remained unchanged and no extra extracted-tree files appeared. No KB bytes or historical results were edited. Reuse this current result only while the archived input hash is the same and the receipt describes its separate scope accurately.

## Obtain package identity without a self-hash cycle

6. Build a preliminary pair of packages into a new sibling output directory after current runtime inputs are fixed:

```sh
python3 -I -B tools/build_release.py --output /absolute/new/preliminary-output
```

Read the emitted `build-receipt.json`, independently hash the runtime ZIP, and validate its manifest against all actual ZIP payload members. The final local evaluation receipt's `artifact.package_sha256` should identify this exact runtime ZIP. `tools/build_release.py --identity` yields a payload identity only; that value must not be mislabeled as a ZIP file SHA-256.

7. Write the new local run record, current project-check output, current runtime identity record, panel definition and evaluation receipt under new source `validation/` filenames. The receipt can refer to the runtime ZIP because those source-level evidence files are outside the runtime payload. Do not record the enclosing source ZIP's SHA-256 inside that same source ZIP. Preserve failed attempts and their input hashes under distinct names.
8. Validate the new version 2.0 receipt with the current helper:

```sh
python3 -I -B skills/skill-builder/scripts/skill_builder.py check --record validation/current-local-evaluation-receipt.json
```

This validates record structure and cross-field relations; it does not independently verify the truth of the attached logs. If a new rule ledger is produced, add a separate `--record` argument for that new version 2.0 `rule-traceability` record. Do not pass custom `local-check-run`, raw build receipt or custom audit JSON files to this checker: those are distinct observation contracts, not one of its six supported record types.

9. Build final packages into another new directory after adding source evidence:

```sh
python3 -I -B tools/build_release.py --output /absolute/new/final-output
```

The final runtime ZIP must have the same SHA-256 as the preliminary runtime ZIP. Independently validate both final manifests, each detached ZIP hash and checksum file, and the exact archived file set. If runtime inputs changed after the preliminary build or observed tests, update the evidence with an actual new attempt; never retain a stale runtime hash.

10. Run the independent preservation comparison against the final source ZIP. The versioned archive root may change; the checker compares relative paths.

```sh
python3 -I -B /workspace/scratch/ce88fda257c5/evidence/preservation/compare_preservation.py \
  --original '/workspace/scratch/ce88fda257c5/upload/skill-builder-1.0.0-rc.1-source(2).zip' \
  --candidate /absolute/final-output/skill-builder-CURRENT-source.zip \
  --require-manifest \
  --output /absolute/new/final-preservation-report.json
```

The check is read-only, except for exclusive creation of its requested output report. Store that report detached if it identifies the final source ZIP itself. Adding it inside the already identified source ZIP would change the ZIP and invalidate the recorded enclosing hash.

11. A second build from identical source inputs can establish reproducibility by exact ZIP comparison. Once enough current evidence exists, stop optional runs. A final post-evidence project check can confirm that new documentation/evidence references resolve; describe the ordering rather than implying it was part of an earlier command.

## Version 2.0 evaluation receipt constraints

The frozen `schemas/evaluation-receipt.schema.json` uses JSON Schema Draft 2020-12, `record_type: evaluation-receipt`, `schema_version: "2.0"`, and rejects extra top-level properties. Required fields are:

```text
schema_version, record_type, case_id, recorded_at, artifact, panel, budget,
runtime_versions, attempts, elapsed, usage, outcome, checks, artifacts,
grader, omissions, redaction
```

| Field | Correct current-release treatment |
| --- | --- |
| `artifact` | Exact current runtime ZIP SHA-256 and current artifact ID. Use `source_commit: null` if no actual commit exists. Top-level activation fields can be null with an explanation that no native host was activated. |
| `panel` | ID, SHA-256 of an actual frozen panel definition, actual pre-attempt freeze time, explicit retry and exclusion policies, and structured `control_identity`. Use `kind: not_run`, `artifact: null` and a reason for an unrun comparative control. |
| `budget` | Actual maximum attempts, elapsed limit, cost limit/currency or null, and a concrete enforcement description. A timeout/log threshold is not an OS sandbox. |
| `runtime_versions` | Versions actually observed in the executing environment. |
| `attempts` | Real observed executions only. Include attempt/case IDs, `condition: local_resource`, timestamps, artifact, target, model, input hashes, permissions, outcome, checks, evidence, elapsed, usage and reason. Preserve failed or blocked attempts instead of silently replacing them. |
| Attempt `artifact` | Exact current package hash plus `activated_source` and SHA-256 of the explicit local helper when that describes the execution. State that this is local resource execution, not native skill activation. |
| `target` | Actual product/surface/distribution/version/OS and policy, with missing details. Do not claim enforced network isolation just because inspected scripts make no network calls. |
| `model` | For deterministic tests, name/version null and a reason that no model participated in the test process. |
| `input_hashes` | SHA-256 values for the actual selected test and executing inputs. Do not use a changed post-run hash to identify an earlier run. |
| `evidence` / `artifacts` | Real file references with their SHA-256 values, observed timestamp and bounded scope. Use the actual saved logs and observations. |
| `checks` | Each has ID, allowed outcome, evidence array and reason. A passed check needs at least one evidence item. Keep the scope local and explicit. |
| `elapsed` and `usage` | Each metric has value, unit, source and missing_reason. Measured time uses seconds. Unknown tokens/tool-call count/cost use null, `source: unknown`, and a reason; never substitute zero. |
| `grader` | Actual test-panel identifier/version/hash, `method: deterministic`, and a calibration/coverage explanation. |
| `outcome` | Allowed values: passed, failed, blocked, not_run, inconclusive, not_applicable. An aggregate passed result cannot contain a required check marked failed, blocked, not_run or inconclusive. |
| `omissions` | Explicit unrun native hosts, comparative panel, remote CI, installation/publication and any actual scope limits. A passed local panel does not become a passed overall host support panel. |

A passed receipt requires a package SHA-256, nonempty attempts/checks/artifacts, a panel hash and freeze timestamp. Each passed attempt requires package identity, checks and evidence. Timestamps must parse and end no earlier than start. Unknown/incomplete outcomes need reasons. The six supported version 2.0 record types are evaluation-receipt, host-capabilities, install-manifest, finding, source-review and rule-traceability; `common.schema.json` supplies shared identity/evidence/metric definitions.

## Explicitly unrun by this audit

Native Codex CLI/IDE discovery, Claude Code, Grok, native permission enforcement, complete host task trials, no-skill/prior-version comparative evaluation, remote CI, installation, publication and live account changes remain unrun. The frozen archive and its old host tables are historical sources. A current package's honest local pass can coexist with those explicit omissions.
