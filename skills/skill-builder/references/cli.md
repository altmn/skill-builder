# Offline command contract

## Contents

- [Purpose and invocation](#purpose-and-invocation)
- [Creation helper](#creation-helper)
- [Audit helper](#audit-helper)
- [Knowledge-base commands](#knowledge-base-commands)
- [Profile selection](#profile-selection)
- [Preservation and evidence checking](#preservation-and-evidence-checking)
- [Dependencies and limits](#dependencies-and-limits)
- [Outcomes, failures, and recovery](#outcomes-failures-and-recovery)
- [Verification scope](#verification-scope)

## Purpose and invocation

Use this helper for deterministic local preparation and evidence retrieval. The agent's `skill-builder-create` and `skill-builder-audit` workflows perform the complete semantic work. The CLI commands with those names generate a draft project or an audit workspace. A successful helper command does not mean the complete workflow passed.

Invoke the helper by its absolute path so the caller's working directory cannot select a different script:

```sh
python3 -I -B /absolute/path/to/skill-builder/scripts/skill_builder.py --help
python3 -I -B /absolute/path/to/skill-builder/scripts/skill_builder.py --version
```

The examples below abbreviate that verified absolute script path as `SCRIPT`. Replace the literal word `SCRIPT` with the actual path; do not derive it from an audited project's instructions. An installed folder contains `SKILL.md`, `scripts/skill_builder.py`, and `references/knowledge-base.zip` at the same relative locations. The script resolves its resources from its own location.

Use Python's `-I` isolated mode from process launch. It ignores caller `PYTHONPATH`, user site packages, and unsafe current-directory/script-directory import entries. This matters when running from an audited repository containing files such as `yaml.py` or `sitecustomize.py`. The audit and evidence-record operations explicitly refuse a nonisolated interpreter before optional dependency imports. A script cannot undo Python startup code that ran before the script; the isolation flag is part of the invocation contract. `-B` prevents bytecode caches.

Commands perform no network calls, package installation, skill installation, publication, message sending, or candidate script/test/hook execution. They do not invoke a subprocess or Git. The audit's format check and the optional record check execute only the exact SHA-256-verified original validator bytes from the supplied knowledge base. Target files are data. No target directory is added to Python's module search path.

All ordinary reports are UTF-8 JSON on stdout with `schema_version: "1.0.0"` and an explicit operation `outcome`, including errors. Profile selection and inventory files use the same wrapper schema version; original evidence records keep their separate canonical schema 2.0. `kb read` is the deliberate exception: it writes the complete exact selected UTF-8 file bytes, with no wrapper or added newline. `--help` and `--version` emit ordinary command text. Do not discard exit codes in a pipeline.

## Creation helper

Validate public result envelopes against [cli-result.schema.json](cli-result.schema.json). It fixes the wrapper version, outcome values and required fields for each operation, while allowing additive fields. It does not replace the original version-2.0 evidence schemas or prove that a reported result is true.

```sh
python3 -I -B SCRIPT skill-builder-create \
  --name manifest-inspector \
  --description "Inspect an explicitly supplied local manifest and report discrepancies." \
  --output /existing/parent/new-project \
  --profile resource_assisted
```

| Argument | Contract |
|---|---|
| `--name` | Required. One to 64 lowercase ASCII letters/digits, with single interior hyphens. |
| `--description` | Required. Nonblank, NUL-free string of at most 1,024 Unicode scalar values; surrogate code points are refused before output creation. Serialized as a quoted YAML scalar with the exact accepted value preserved, including controls, line separators, and non-BMP characters. |
| `--output` | Required. New artifact directory; existing parent required. Existing files/directories are refused. |
| `--profile` | Required. `instruction`, `resource_assisted`, or `suite_runtime`. |
| `--modifier` | Repeatable. `network`, `publication`, `persistent_state`, `authenticated_browser`, or `installer`. |
| `--overrides` | Optional explicit local JSON file with rule decisions and concrete reasons. |

The helper creates these outputs:

| Path | Meaning |
|---|---|
| `skills/NAME/SKILL.md` | A portable draft containing the original task-contract template, the selected name/description, a visible draft marker, and task-specific blanks to complete. |
| `TASK-BRIEF.md` | Required decisions covering outcome, examples, inputs, scope, effects, hosts, resources, evaluation, and release. |
| `README.md` | Work remaining and the evidence boundary. |
| `LICENSE-DECISION.md` | Rights-holder license choice remains open; no license is assigned by the helper. |
| `evidence/rule-selection.json` | Every canonical rule and its initial applicability decision, retaining complete rule text and authority. |
| `evidence/rule-traceability.json` | Schema 2.0 assessment worksheet for all 99 rules. Adopted rules start `not_run`; no passing evidence is invented. |
| `evidence/source-identity.json` | Builder version and source archive identity. |
| `evidence/templates/` | Exact original host, evaluation, install-manifest, and finding templates, still visibly incomplete. |
| `project-templates/` | Exact original README, AGENTS, contribution, security, changelog, and notice templates. They remain `.template` files. |
| `workflows/` | Exact original creation instructions, instruction worksheet, and audit-report template. |

Exit 0 and `outcome: scaffold_created` mean only that these files were created. `semantic_implementation` and `host_trials` remain `not_run`; `release_ready` is false. Continue the full creation workflow, complete the task and governance content, validate the actual distribution, and collect real evidence. A draft's format pass does not make its task contract finished.

## Audit helper

```sh
python3 -I -B SCRIPT skill-builder-audit \
  --target /explicit/existing/project \
  --output /different/existing/parent/new-audit \
  --profile resource_assisted
```

The target must be an existing directory whose final component is not a symlink. The output must be new and outside the target. The helper does not repair target content. It inventories the current filesystem, hashes bounded regular files, records symlink/special-file omissions without reading their contents, and invokes the preserved format validator on actual inventoried `SKILL.md` files. `.template` files do not count as actual skills. It does not infer host-discoverability from finding a file.

The profile, repeatable modifiers, and overrides have the same contract as creation. Resource limits are explicit:

| Argument or bound | Default | Behavior when reached |
|---|---:|---|
| `--max-files` | 10,000 recorded files/symlinks/special files | Remaining tree is unenumerated and coverage is incomplete. |
| `--max-entries` | 50,000 total inspected files and directories | Directory enumeration/storage is bounded; remaining entries are disclosed as unenumerated. |
| `--max-file-bytes` | 16,777,216 bytes | Oversized regular files are recorded without content hashes. |
| `--max-total-bytes` | 134,217,728 bytes | Further file reads are omitted when the remaining byte budget is insufficient. |
| Directory depth | 128, fixed | Deeper contents remain explicitly uninspected. |

Limits must be positive integers. Raising them is a deliberate workload decision. The tool does not quietly raise limits or call omitted content reviewed. A verification reread of previously hashed files detects observed content changes; it is additional I/O beyond the inventory's `bytes_hashed` measurement. It does not turn a changing directory into an immutable snapshot.

The entry budget is charged when each name is obtained from `scandir`, including siblings buffered for sorting before descent. Already buffered names consume the same global allowance as processed names. The helper performs no extra lookahead after exhausting that allowance. If the final obtained entry exactly fills the allowance, the tool conservatively marks completeness unknown even when that entry might have been the directory's last; it does not spend an unreported extra read to guess.

Excluded directories are `.git`, `.venv`, `venv`, `node_modules`, `__pycache__`, and `.pytest_cache`. Every encountered exclusion is recorded. `complete_within_declared_exclusions` describes that bounded filesystem scope; it is not every tracked file in a repository. Git was not invoked, so tracked coverage and commit identity are unknown. Use the separately preserved immutable indexer only after selecting and reviewing its explicit source contract.

The audit workspace contains `inventory.json`, `static-checks.json`, `rule-selection.json`, `rule-traceability.json`, `source-identity.json`, `summary.json`, `README.md`, and the original audit/instruction-review templates. The static report preserves the validator's version, profile, dependency version, checks, and `not_checked` list.

`outcome: static_preparation_completed` reports artifact creation. `audit_verdict` remains `inconclusive` when static checks pass because semantic review and host trials have not run. A detected format/resource failure or observed content change makes that verdict `failed`. Inventory truncation remains explicit and returns a nonzero exit. No readable actual skill, or unavailable format-checking dependency, is blocked. Continue the full audit workflow and record manual findings and real execution results separately.

## Knowledge-base commands

The exact original uploaded ZIP, including its macOS sidecar entries, remains intact. Its pinned SHA-256 is checked before content use. The index identifies 182 substantive files; each retrieved file is checked against its own size and SHA-256. Archive reads happen from the bytes already hashed, so a later disk replacement is not treated as the same validated object.

### Verify and list

```sh
python3 -I -B SCRIPT kb verify
python3 -I -B SCRIPT kb list
python3 -I -B SCRIPT kb list --prefix handbook/
```

`kb verify` validates the archive identity and every substantive member identity. Its `passed` outcome is explicitly limited to preservation. `kb list` returns every indexed path, byte count, and SHA-256, with no pagination or hidden truncation. `--prefix` restricts the listing to a literal path prefix and reports that filtered count separately from the archive's total.

### Read exact content

```sh
python3 -I -B SCRIPT kb read handbook/11-create-a-skill.md
python3 -I -B SCRIPT kb read checklists/audit.md
python3 -I -B SCRIPT kb read catalogs/requirements.json
```

Paths are exact, portable, archive-relative content paths. Absolute paths, `..`, backslashes, control characters, normalized-away components, and unknown indexed paths are rejected. `kb read` prints complete text and never summarizes it. Binary files are refused at the terminal; extract them for exact binary access. A caller that limits captured stdout must explicitly continue reading rather than treating its own truncated display as full-file review.

### Search and retrieve

For bounded reads, use `kb read PATH --limit 4096`. It returns JSON with outcome
`read`, exact UTF-8 `text`, whole-file `sha256`, `archive_sha256`, `total_bytes`,
byte `offset`, `returned_bytes`, `next_offset` and `complete` (this page reaches
EOF). Resume with `--offset NEXT_OFFSET --sha256 FIRST_PAGE_HASH`; a nonzero
offset requires the expected hash. File identity must match before any text is
returned. The limit is 4–16,384 content bytes, default 4,096; pages end on UTF-8
boundaries and preserve CRLF and final-newline bytes. Invalid/mid-character or
beyond-EOF offsets, binary input and stale identities fail with exit 2. At EOF
an empty page is valid. No range options preserves the original raw output;
`--sha256` alone verifies identity while retaining that raw output.

`complete` means EOF, not proof that prior ranges were reviewed. Track contiguous
ranges separately and continue through any host display truncation. The content
byte limit does not include JSON escaping/envelope overhead. No tokenizer count
or semantic reading claim is inferred from these bytes.

### Search previews

```sh
python3 -I -B SCRIPT kb search "publication" --path handbook/ --limit 20
python3 -I -B SCRIPT kb search "LIFE-012" --offset 20 --limit 20
```

Search is offline literal text, case-insensitive unless `--case-sensitive` is set. The query must contain 1–4,096 characters. `--path` is an optional literal prefix. `--offset` defaults to 0 and must be nonnegative; `--limit` defaults to 20 and accepts 1–200 matching lines per page. The result reports the full number of matching lines, the returned number, each file/line location, and `next_offset` when more results exist. Previews are capped at 360 characters with `preview_truncated`. Binary files not searched are listed. Use `kb read` or exact extracted files to inspect complete matches and surrounding context. A search match is a review lead, not a verdict or complete reading.

### Explicit extraction

```sh
python3 -I -B SCRIPT kb extract --output /existing/parent/new-kb-reference
```

Extraction first verifies every substantive content identity, then writes all 182 files unchanged to a new directory. It runs no extracted code. macOS sidecars remain preserved in the original ZIP but are not materialized into the extracted content tree. Output directories must stay outside installed skill/configuration roots so bundled example `SKILL.md` files do not become live skills by accident. The conservative path policy rejects any output path containing a component named `skills`, `remote-skills`, `.agents`, `.claude`, `.codex`, or `.grok`; choose an ordinary artifact workspace instead. This same output policy applies to create and audit.

## Target-specific evaluation

Both preparation helpers additionally emit `EVALUATION-PLAN.md`,
`EVALUATION-REVIEW.md`, `evaluation-review.json` and three
`evals/*.json.template` worksheets. These are guide-derived supplemental records
outside the immutable KB and original schemas. All assessment items begin
`not_assessed`/`not_run` without evidence. The agent must adapt task prompts,
held-out labels, fixtures, oracle, environment and budgets; copying scaffolding
does not complete either workflow. Audit input stays read-only.

The runtime includes a standard-library evaluator. From the actual loaded root:

```sh
python3 -I -B "$SKILL_ROOT/scripts/evaluate.py" prepare \
  --candidate /approved/subject-skill \
  --routing-cases /approved/evals/routing.json \
  --execution-cases /approved/evals/execution.json \
  --fixtures-root /approved/evals \
  --environment /approved/evals/environment.json \
  --output /existing/parent/new-panel
```

Supply all three case/root flags together. The runtime has no builder-specific
default corpus. Each case file is a JSON array using the fields in the emitted
worksheets; unresolved REPLACE values are refused. Fixture paths are portable,
root-relative data paths. Source case bytes and fixture identities are frozen.
Symlink ancestors/leaves, escaping paths, special files and incomplete snapshot
identities are refused. Snapshot inventory excludes the helper's documented
development directories (`.git`, `.venv`, `venv`, `node_modules`, `__pycache__`,
`.pytest_cache`); it is not every tracked file or an OS sandbox. Use a stable
explicit runtime snapshot. Neither candidate code nor fixture code is executed.

`--previous` optionally supplies a prior snapshot. Splits and repeated `--case`
selection must retain at least one routing and one execution case. A plan freezes
the same four task conditions and independent trace/artifact contract described
in the [evaluation method](evaluation-method.md). The authorized host adapter
collects observations and an independent reviewer grades actual outputs.

Use `scripts/evaluate.py summarize --plan PLAN --observations OBSERVATIONS` for
the existing hash-bound observation format. Exit 0 means completed accounting,
1 an evidenced invariant failure, 2 invalid input/evidence, and 3 incomplete
coverage. Unknown costs and failed attempts remain visible. These companion
records do not replace the original version-2 formal evaluation receipts.
The source-repository `tools/evaluate.py` delegates to this same engine; without
case flags only that repository adapter selects the builder's own corpus.

## Profile selection

```sh
python3 -I -B SCRIPT profile --profile instruction
python3 -I -B SCRIPT profile --profile resource_assisted --modifier publication
python3 -I -B SCRIPT profile --profile suite_runtime --modifier network --modifier installer
```

Each result joins all 99 complete canonical rules to the selected scope. Statements, strengths, authority labels, sources, applicability, and verification descriptions remain intact. `adopted` means assessment is required. `not_applicable` is an initial scope claim that a reviewer must confirm. `not_assessed` means an unresolved mechanism remains visible. None means passed.

An optional `--overrides /explicit/file.json` accepts a JSON object keyed by known rule IDs. Each value must contain exactly `decision` and `reason`; the decision is `adopted`, `not_applicable`, or `not_assessed`, and the reason contains at least 20 stripped characters. This length rule is structural; a reviewer must assess the explanation. Example:

```json
{
  "LIFE-012": {
    "decision": "not_applicable",
    "reason": "This particular artifact produces a local draft only; no external publication is part of this release."
  }
}
```

The publication modifier normally adopts LIFE-012. Do not use an override to hide a real publication effect or turn a rule selection into authorization. Revalidate the complete traceability record after changes.

## Preservation and evidence checking

```sh
python3 -I -B SCRIPT check
python3 -I -B SCRIPT check --record /explicit/evidence/rule-traceability.json
python3 -I -B SCRIPT check --record /explicit/host.json --record /explicit/evaluation.json
```

`check` verifies complete source preservation. Each `--record` also validates one explicit evidence record using the original local Draft 2020-12 schemas and original cross-field checks. The helper materializes only trusted schemas and canonical rule data in a temporary directory, deletes that temporary data when complete, and performs no remote schema retrieval. It does not modify input records.

Input records are bounded at 4 MiB. Duplicate JSON keys and nonfinite values are rejected at every nesting depth, including exponent overflow such as `1e999` and `-1e999`, and named `NaN`/`Infinity` tokens. Decimal/scientific-notation numbers use Python's finite binary floating-point representation; normal rounding and underflow follow that representation, while integers use Python integers subject to the interpreter's parsing limits. No arbitrary-precision decimal measurement guarantee is claimed. Each record must be an object with a supported string `record_type`. A malformed, unknown-type, unreadable, or nonfinite record produces its own failure, other requested records continue in input order, and the batch returns exit 1. Missing validation dependencies or trusted-schema/integrity problems remain blocked, exit 2.

The checker preserves the original distinctions between artifact identity, target environment, actual attempts, evidence, measurements, and claims. Schema conformity does not establish that observations are true. Detailed schema messages can contain input values, so this wrapper reports failure counts and stable diagnostics instead of echoing record contents. For fuller diagnostics, use the preserved checker explicitly in a suitable private environment. The frozen standalone checker still lacks the wrapper's exponent-overflow and dispatch guards; its original bytes are retained as historical source, not presented as corrected executable code.

## Dependencies and limits

### Workflow review and ablation companions

Read [the workflow supplement](uber-workflows.md) before using these offline,
standard-library helpers. Both create and audit emit draft
`workflow-contract.json.template`, `papercut.json.template`, `ABLATION-PLAN.md`
and four additional unassessed review topics. Templates are not test results.

```sh
python3 -I -B SKILL_ROOT/scripts/review.py lint /explicit/workflow.md
python3 -I -B SKILL_ROOT/scripts/review.py contract --record /explicit/contract.json --target /explicit/subject --execution-cases /explicit/execution.json
python3 -I -B SKILL_ROOT/scripts/review.py papercut --record /explicit/incident.json --evidence-root /explicit/evidence --execution-cases /explicit/execution.json
python3 -I -B SKILL_ROOT/scripts/ablate.py blind --plan /explicit/plan.json --observations /explicit/observations.json --output /existing/parent/new-blind-review
python3 -I -B SKILL_ROOT/scripts/ablate.py score --key /explicit/key.json --judgments /explicit/judgments.json
```

Review operations only read explicit inputs. Lint reads at most 1 MiB of UTF-8
Markdown; source owners are bounded to 1 MiB. Companion JSON and evidence are
bounded to 16 MiB, with existing nonsymlink path/containment checks. Contract
checking detects source drift and invalid case/check links, not semantic truth.
Papercut checking requires independent identity-bound regression evidence for
resolution and never submits a report. Lint exits 0 with advisory diagnostics;
zero diagnostics is not approval. Drift exits 1; invalid inputs exit 2.

The panel preparer additionally accepts `--variants /explicit/variants.json`.
Each named variant adds explicit execution slots and frozen payload identity.
Optional trajectory rules grade observed actions independently of activation
and answer quality; see the supplement for the event contract. The optional
integer counters `tool_calls`, `tool_errors`, `activated_context_tokens` require
measurement-source strings in `metric_sources`. Unknown measurements remain null.

Blinding writes an exclusive private tree of copied artifact bytes, neutral
pair paths, pairs.json, private key.json and a judgment template (maximum 512
pairs, 4,096 artifact copies and 128 MiB total copied artifact bytes, checked
before output creation). It never changes source evidence or overwrites an existing output.
The judge must not receive the key. Scoring verifies the key binding, public
pair/artifact hashes and independent calibration evidence; missing/unknown
judgments and failed/incomplete original panels remain visible. Exit 0 means
prepared/completed accounting, 1 failed underlying panel, 2 invalid input, 3
incomplete scoring. Inspect underlying failures; accounting is not certification.
No helper calls models, executes targets, sends telemetry, installs or publishes.

Python 3.10 or newer is required. Core preservation, listing, reading, search, profile selection, and scaffolding use only the standard library. The preserved format validator requires PyYAML; the recorded pin is 6.0.3. Evidence validation also requires jsonschema 4.26.0 and referencing 0.37.0. Exact requirements are retained in `knowledge-base.zip!tools/requirements.txt`. Provision dependencies through a reviewed process; this helper never installs them.

The archive is capped at 32 MiB, each indexed member at 64 MiB, manifest/override/evidence inputs at 4 MiB, and archive entries at 4,096. These are helper processing bounds, not format-specification requirements. The original preserved format validator independently caps SKILL.md at 1 MiB, frontmatter at 64 KiB, YAML nesting at 32, recognized direct links at 2,048, and link-parenthesis depth at 32. It rejects unsupported ambiguous Markdown coverage rather than reporting that coverage passed.

All created directories request mode 0700 and files mode 0600; effective behavior depends on the operating system. Output creation is exclusive and existing destinations are refused. Output parents must already exist, and symbolic-link ancestors are rejected. Caught-failure cleanup checks each owned path's identity, type, mode, owner, flags, link count, size and modification/change timestamps. File cleanup also verifies the bytes against the exact successfully written content, including a confirmed partial-write prefix. Observed in-place edits, replacements, metadata changes, unreadable or uncertain state, unrelated files and nonempty directories are retained. Access times are excluded because verification reads may update them. Owned directory snapshots account for the operation's own child creation and removal without clearing an already observed external change. No force-overwrite option exists.

These cleanup checks are point-in-time observations, not a filesystem transaction. They cannot prevent or reliably identify changes racing an internal write, snapshot refresh or final deletion. If a write fails without confirming how many bytes were written, unmatched partial content is retained for inspection; cleanup does not guess that it is safe to delete.

These checks reduce ordinary path mistakes and detect observed changes. They do not provide an operating-system sandbox, lock a whole filesystem snapshot, or prove resistance to an adversary replacing ancestor paths concurrently. Use a trusted local workspace and host-enforced confinement for hostile sources. Do not claim these local checks establish permissions, security compliance, or safe later execution of a candidate.

## Outcomes, failures, and recovery

| Exit | Meaning |
|---|---|
| `0` | The requested local helper operation completed within its stated scope. Inspect semantic/host limits and all omissions. |
| `1` | A completed check found failure: format/resources, input evidence records, observed content change, or incomplete audit coverage caused by limits/omissions. |
| `2` | Invocation, missing dependency, missing actual skill, integrity, path, permission, or processing problem blocked completion. No completed assurance is implied. |

Top-level outcomes are operation-specific: `scaffold_created`, `static_preparation_completed`, `selected`, `listed`, `searched`, `extracted`, or a check outcome such as `passed`, `failed`, or `blocked`. They are not interchangeable with the schema 2.0 evidence outcomes. `kb list` includes its listing/count contract; `kb read` returns exact bytes.

There are no automatic retries. After a failure, inspect any named output and its omissions, resolve the cause, and select a fresh destination when appropriate. A caught creation failure attempts ownership-aware cleanup; abrupt process termination can leave partial new output. Do not treat an incomplete directory as a successful result or rerun a create command over it. Long-running operations do not have an internal wall-clock deadline; the caller should apply the task's time budget and preserve a cancellation as incomplete. No paid-model or remote-service budget is consumed by these commands.

## Verification scope

The tests cover exact archive/content preservation, extraction identity, profile parity with the original selector, schema-valid all-rule scaffolding, nonoverwrite and cleanup, bounded traversal, symlink handling, candidate nonexecution, isolated imports, failure statuses, and documented command help. These are local resource contracts. They do not establish live skill discovery, automatic triggering, task success, no-skill improvement, host permission enforcement, or maintenance support on Codex, Claude Code, or Grok.

Treat the actual command implementation and `--help` as the public argument contract. Keep this reference synchronized when it changes. Keep source research and historical receipts intact; a new local helper test cannot relabel those historical observations as new host evidence.
