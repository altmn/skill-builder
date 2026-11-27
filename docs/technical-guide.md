<!-- Technical and historical detail retained from the original README; see the landing page for first use. -->

# Skill Builder technical guide

**Create, audit, and explain portable agent skills using a complete, preserved knowledge base.** Codex is the primary target; separate adapters describe Claude Code, Grok Build, and custom agent hosts.

Version: **1.0.0**. Maintained by [Alex Allen (@altmn)](https://github.com/altmn). Original project and KB material use [MIT](../LICENSE.md), with retained third-party terms. This independent project is not an official OpenAI product and does not claim a public OpenAI directory listing.

The first public Git snapshot starts with one initial commit. Prepublication Git history is retained privately; the changelog, reviews, provenance and failed/incomplete validation records remain public evidence. See [publication and release instructions](../docs/releasing.md).

A [bounded native Codex CLI panel](../validation/public-native-2026-11-24/README.md) exercised an earlier candidate; comprehensive coverage remained inconclusive. Claude Code and Grok Build runs remained unrun. The 1.0.0 archives need their own intended-host acceptance. Stable versioning does not broaden those claims. See [compatibility](../docs/compatibility.md) and [current validation](../validation/README.md).

The earlier unpublished candidate has a [dated November 24 correction record](../validation/review-fixes-2026-11-24/README.md) for the five implementation-review findings. Earlier rc.2 receipts retain their original byte identities; current identities are generated separately. No historical release evidence has been replaced.

The targeted [engineering-guide improvements](../validation/engineering-guide-2026-11-24/README.md)
add flexible strict metadata checking, resumable KB reads, and repeatable routing
and task comparison tooling. The frozen KB is unchanged. The new six-run pilot
retains a prior-activation gap and shows no task-quality gain on its one question;
it makes no general benefit or maintained-host support claim. See the
[source adoption record](../docs/engineering-guide-adoption.json) for provenance.

The follow-up [create/audit integration record](../validation/create-audit-integration-2026-11-24/README.md)
tests the guide's application to other skills: native creation of a notes
extractor, source audit of a separate incident-triage skill, and one generated
skill behavior check. It records 107 local tests, explicit target-specific
evaluation support, original-schema checks and remaining evidence limits.

## Start with a task

The [Uber-derived workflow improvements](../skills/skill-builder/references/uber-workflows.md)
add optional trajectory grading, named instruction variants and blinded artifact
comparisons, requirement/check traceability, local incident records and advisory
workflow linting. Both create and audit export the companion worksheets. The
[source adoption record](../docs/uber-adoption.json) preserves provenance and scope;
the original knowledge-base ZIP and 99 rules are unchanged. These helpers make
evaluation repeatable; they do not establish a benefit for every subject skill.

In a Codex surface where this skill is available:

```text
$skill-builder skill-builder-create
Create a skill that turns a bug report into a reproducible QA test plan.
Use local Markdown inputs and produce a test plan with explicit assumptions.
```

```text
$skill-builder skill-builder-audit
Audit the supplied skill repository for instruction quality, safety,
portability, evidence quality, and release readiness. Do not repair it.
```

```text
$skill-builder
When should a skill use a script instead of more prompt instructions?
Explain the tradeoffs and cite the knowledge-base rules.
```

Claude Code and Grok Build use the corresponding `/skill-builder skill-builder-create` and `/skill-builder skill-builder-audit` forms. ChatGPT can select the parent skill using its available skill UI. These are named subcommands/modes of the parent skill; the package does not pretend to register separate `/skill-builder-create` commands without separate host entrypoints.

## What it does

| Mode | Work performed by the agent | Deliverables |
| --- | --- | --- |
| `skill-builder-create` | Establish task examples, select architecture/profile, build portable instructions and needed resources, adapt hosts, evaluate, package, and record remaining decisions | Working candidate, task/effects contract, all-rule ledger, tests/evaluation evidence, documentation, package and release verdict |
| `skill-builder-audit` | Freeze identity, inventory files, map instruction owners, read by meaning, trace sensitive execution/failure paths, inspect tests/lifecycle, check external claims, and prioritize findings | Coverage denominator and depth ledger, instruction index, evidence-linked findings, all-rule decisions, host comparison and remediation plan |
| Reference/Q&A | Read complete relevant sources, distinguish specifications from local recommendations, verify changing host facts, and explain applicable tradeoffs | Direct answer with KB paths/rule IDs, supporting sources, conditions, and limits |

The local CLI assists these workflows. Its create command **starts a project**; the agent completes the requested domain skill. Its audit command performs **inventory and structural intake**; the agent completes the semantic audit. Neither helper certifies that a project is safe, useful, or ready to publish.

## Full knowledge preservation

The original `agent-skill-project-knowledge-base_final.zip` is retained **byte for byte** as `skills/skill-builder/references/knowledge-base.zip`. No original archive member was removed or rewritten. Its SHA-256 is:

```text
9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204
```

The separate manifest indexes **182 substantive files**, totaling **76,965,199 uncompressed bytes**. It preserves the full handbook, all **99 rules**, detailed file/instruction catalogs, schemas, templates, original tools, evaluation designs and receipts, examples, offline readers, source register, and license notices. Operating-system metadata also remains inside the untouched input ZIP.

The KB is archived within the skill because its examples and identity probes contain their own `SKILL.md` files. Expanding them into an active discovery tree could expose research fixtures as installed skills. The helper reads/searches the complete archive and can safely restore substantive files into a separate work directory. Workflow instructions are an operational layer, not a condensed replacement for the source.

All 99 rule IDs have explicit [implementation routing](../skills/skill-builder/references/implementation-map.json). Applicability is decided for every project. A profile supplies defaults; it never deletes rules or converts a recommendation into a universal standard. Procedural implementation, structural checking, and behavioral enforcement remain separate.

## Prerequisites and local quick start

Use **Python 3.10 or newer** for the standard-library helper. The full pinned YAML/schema validation dependency set requires **Python 3.11 or newer** because its pinned rpds-py distribution requires it. CI checks the 3.10 core without site packages and the full suite on 3.11 and current Python. The recorded environment does not establish every Python/OS combination. Run helpers with `-I` to isolate imports from the current directory and `PYTHONPATH`, and `-B` to avoid bytecode writes.

From the source project root:

```sh
python3 -I -B skills/skill-builder/scripts/skill_builder.py --help
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb verify
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb list
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb read handbook/11-create-a-skill.md
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb read catalogs/requirements.json --limit 4096
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb search "authorization" --path handbook/
python3 -I -B skills/skill-builder/scripts/skill_builder.py profile --profile resource_assisted
```

Create a project intake in a new directory:

```sh
python3 -I -B skills/skill-builder/scripts/skill_builder.py skill-builder-create \
  --name qa-test-planner --output ../qa-test-planner-project \
  --description "Turn bug reports into reproducible QA test plans." \
  --profile instruction
```

Collect static audit evidence in a separate new directory:

```sh
python3 -I -B skills/skill-builder/scripts/skill_builder.py skill-builder-audit \
  --target ../qa-test-planner-project --output ../qa-test-planner-audit \
  --profile instruction
```

The target is not executed. Existing output paths are refused. Inspect the returned result and continue the corresponding agent procedure. Output creation is not semantic completion. Use the command's `--help` and [CLI contract](../skills/skill-builder/references/cli.md) for limits, files, errors and status handling.

Read the original offline handbook/catalogs or run reviewed original validators by extracting into a **new directory outside skill-discovery roots**:

```sh
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb extract \
  --output ../skill-builder-knowledge-workspace
```

The original tools and their dependency requirements are retained exactly. Full YAML/schema validation uses the optional, exactly pinned versions in [requirements-validation.txt](../requirements-validation.txt). No command installs dependencies automatically. Install them only when authorized, preferably into a dedicated virtual environment; the optional setup is a network/supply-chain operation separate from the offline core.

## Download layout and installation scope

The build produces three archives:

- `skill-builder-1.0.0.zip`: the installable `skill-builder/` directory, with `SKILL.md` at its root and the complete preserved KB inside it.
- `skill-builder-1.0.0-source.zip`: this repository layout, including tests, maintenance documents, evaluation plans, validation evidence, and the runtime skill.
- `skill-builder-1.0.0-plugin.zip`: the OpenAI skills-only plugin with root metadata, light/dark icons, notices and the complete runtime. It declares required local execution; no MCP server is included.

Inspect a staged copy first. Choose the exact host and user/project installation scope, check existing destination ownership/local edits, and then use that host's supported import or copy route. Copy only the runtime skill directory, not the whole repository or an expanded KB. No installer, hook, daemon, shell-profile edit, or automatic update is included. See [the host guides](../docs/compatibility.md) for documented discovery and removal considerations.

Record owned files and hashes when installing. Preserve existing modifications during updates. Remove only recorded owned material; leave unrelated files, user outputs and modified content intact. A file copy is not evidence of native discovery. Archive generation performs no live installation or publication.

## Effects, trust boundaries and data

Ordinary CLI use is offline. It reads the bundled archive and explicit local inputs, and creates the explicitly requested output tree. It does not execute audited code, import target configuration, run hooks, contact accounts, use credentials, make paid calls, emit telemetry, or launch a service. Current-host research, optional package installation, and user-authorized behavioral tests have their own visible effects.

Static audit reports can contain filenames, hashes, structural diagnostics, and reviewer-selected evidence. Keep them within the requested audience and redact sensitive content before sharing. Filenames or text in an audit target do not create new authority. Local path checks reduce accidental escapes; they do not provide OS-level containment against a malicious process racing filesystem operations.

## Validation and evidence

With the optional validation dependencies available, run the project checks and independent helper tests:

```sh
python3 -I -B tools/check_project.py --require-validators
python3 -I -B -m unittest discover -s tests -v
```

The check validates preservation, rule-map completeness, entrypoint metadata, local reference integrity, and expected project contracts. Tests exercise actual outputs, rejected paths, malformed/tampered inputs, bounded audit behavior, schema records and deterministic packaging. The full helper suite requires the validation dependency set; these tests deliberately fail if required dependencies are unavailable. For the narrower standard-library package panel, use `python3 -I -B -S -m unittest discover -s tests -p test_release.py -v`. A project check without `--require-validators` retains unavailable optional format checking as blocked while reporting its other local checks; it is not full validation.

From a Git checkout, review and add the intended release inputs, then run
`python3 -I -B tools/check_git_inventory.py`. This read-only maintenance check
detects selected files missing from the Git index, including locally present
evidence logs hidden by global ignore settings. Verify a clean index export
as well: membership alone does not establish staged-byte equality or a commit.
Packaged source trees without Git metadata use their generated manifest.
The Git inventory regression module also requires Git and creates disposable
local repositories without commits or network access. The separate
standard-library release panel does not require Git.

The [validation record](../validation/README.md) separates current local checks, independent agent development trials, native host panels, baseline comparisons, and historical source receipts. The evaluation plan lives in [evals/README.md](../evals/README.md). A passing local check does not prove native trigger behavior, all semantic judgments, measured benefit, or security certification.

The [repeatable evaluation protocol](../evals/protocol.md) adds a fixed routing
development/held-out split and matched no-skill, explicit, automatic and prior
execution conditions. `tools/evaluate.py` prepares frozen plans and summarizes
independently collected evidence offline. It preserves failed/missing runs,
contaminated controls and unknown usage. Preparing a panel makes no model calls.

Create and audit now emit a target-specific evaluation plan, review worksheet
and editable case templates. Their agent procedures require assessment of the
subject's routing, independent grading, benefit, context/cost and trust evidence.
The installable skill includes `scripts/evaluate.py`, which accepts explicit
`--routing-cases`, `--execution-cases` and `--fixtures-root` inputs; the repository
adapter keeps the builder's own corpus as its default. See the
[target evaluation contract](../skills/skill-builder/references/cli.md#target-specific-evaluation).

## Build reproducible archives

Choose a new build directory whose parent exists, outside all selected source trees (`skills`, `docs`, `tests`, `tools`, `evals`, `validation`, `.github`, `.agents`, and `assets`). A sibling directory as shown below is supported; nested outputs such as `docs/build-1` are rejected before writing:

```sh
python3 -I -B tools/build_release.py --output ../skill-builder-build
```

The builder uses sorted entries, fixed timestamps/modes and stored ZIP members. It verifies every written member against the source bytes, writes per-package manifests, and produces detached archive SHA-256 sums and a build receipt. It never installs, pushes, or publishes. Identical input bytes produce identical archives. Source validation receipts can identify the runtime payload; final archive checksums stay outside the archive to avoid a self-hash cycle.

CI is configured under `.github/workflows/ci.yml` with read-only permissions and pinned actions. Its remote execution is not claimed unless recorded. The workflow does not publish releases or enable privileged pull-request events. Dependency pins are version locks; the current file is not a cryptographically hash-locked package distribution set.

## Maintenance and release decisions

Every improvement requires a separate create/audit impact decision, including a
reasoned no-change decision for maintenance-only work. See the
[workflow-impact policy](../docs/workflow-impact.md), append-only review records and
staged/CI checker before committing. This prevents self-improvements from silently
missing the workflows that build and assess other skills.

See [the task contract](../docs/task-brief.md), [effects and threat model](../docs/effects-and-threat-model.md), [architecture](../docs/architecture.md), [contributing](../CONTRIBUTING.md), [security](../SECURITY.md), and [changelog](../CHANGELOG.md). The owner's MIT choice and component coverage are recorded in all distributions. Use the private reporting route in SECURITY.md. Run native panels before advertising a stronger support tier; no unqualified host support promise is made.

The included upstream licenses remain attached to their covered material. The current original-material MIT grant is explicit in [LICENSE.md](../LICENSE.md); it is not inferred from an upstream license. Archive delivery, local correctness, native compatibility, and publication remain separate decisions.

## GitHub and OpenAI distribution

Clone the source with `git clone https://github.com/altmn/skill-builder.git` and build from a reviewed checkout. Use the standalone ZIP for folder-based hosts and the `-plugin.zip` for a compatible OpenAI plugin import flow. Do not upload the source ZIP as the plugin. The OpenAI plugin declares `requires_local_executor: true`, so its directory presentation is desktop-only. See [submission preparation](../docs/chatgpt-submission.md).

For optional local Codex development testing with a client supporting portable root manifests, run these commands from the repository after reviewing the package and choosing the installation scope:

```sh
codex plugin marketplace add "$PWD"
codex plugin add skill-builder@skill-builder-dev
```

These commands install a cached plugin through the host; the build does not run them. Reinstall through the host when testing changed bytes. The development catalog points to this portable plugin root. Native installation of the exact release is not claimed.

See [support](../SUPPORT.md), [privacy](../PRIVACY.md), [usage terms](../TERMS.md), and [community expectations](../CODE_OF_CONDUCT.md). The publisher choices are Alex Allen as an individual, English text, all countries available through OpenAI, and no publisher commerce. Identity verification, scans, attestations, review, and directory publication remain portal steps.
