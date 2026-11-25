# skill-builder-create

Create a complete, reviewable skill project from the user's task, using the full knowledge base. This is an agent workflow. The command-line helper creates working records and scaffolding; it cannot supply domain judgment, perform semantic review, prove host compatibility, or complete this workflow by itself.

## Contents

1. [Context and complete source loading](#create-01-context)
2. [Task and acceptance contract](#create-02-contract)
3. [Profile, effects and architecture](#create-03-architecture)
4. [Portable instructions and resources](#create-04-implementation)
5. [Host adapters](#create-05-hosts)
6. [Tests and evaluations](#create-06-evaluation)
7. [Packaging and maintenance](#create-07-package)
8. [Release decision and delivery](#create-08-delivery)
9. [Recovery and continuation](#create-09-recovery)
10. [Required output](#create-10-output)

## create-01-context

Establish the requested task and authorized destination from the conversation. Honor already supplied choices. Inspect only supplied or otherwise authorized project files. A request to create a source project or archive authorizes local preparation and verification; it does not automatically authorize live agent installation, remote publication, account changes, external messages, or paid evaluations.

Resolve this skill's root from the activated artifact, rather than from the caller's working directory or a similarly named local directory. Read [governance](../references/governance.md) and [requirement coverage](../references/requirement-coverage.md). Use the helper at that resolved root:

```text
python3 -I -B scripts/skill_builder.py kb read handbook/01-design-principles.md
python3 -I -B scripts/skill_builder.py kb read handbook/02-instruction-engineering.md
python3 -I -B scripts/skill_builder.py kb read handbook/04-portability.md
python3 -I -B scripts/skill_builder.py kb read handbook/11-create-a-skill.md
python3 -I -B scripts/skill_builder.py kb read templates/CREATE-PROJECT-INSTRUCTIONS.md
python3 -I -B scripts/skill_builder.py kb read checklists/new-project.md
python3 -I -B scripts/skill_builder.py kb read catalogs/application-profiles.md
python3 -I -B scripts/skill_builder.py kb read catalogs/requirements.json
```

These examples assume the skill directory as the working directory. Elsewhere pass the absolute path of `scripts/skill_builder.py` as a structured argument. `kb read` returns the original member, not an account of it. Read each required file completely. If the host truncates a response, finish reading the remaining source with a bounded file reader; an ellipsis or search preview is not a completed read. Do not compress or rewrite the original corpus to fit a context budget. Load distinct files at the decision points below, and retain unresolved reading in the work record.

Follow the completed example once before adapting the generic scaffold. Read `examples/README.md`, `examples/manifest-inspector/task-brief.md`, `examples/manifest-inspector/skills/manifest-inspector/SKILL.md`, its `references/contract.md`, `examples/manifest-inspector/audit-report.md`, and the relevant filled records in `examples/records/`. This is an example of connected decisions and evidence, not a requirement to copy the manifest-inspection task or its architecture.

Create or reuse an owned working location. For a new project, the deterministic starting command is:

```text
python3 -I -B scripts/skill_builder.py skill-builder-create --name example-skill --output NEW_DIR --description "Describe the actual task and its triggers." --profile instruction
```

Replace the example values through structured arguments. Choose the real profile and any repeated `--modifier` arguments only after inspecting the intended effects. `NEW_DIR` must be a new, authorized destination. Existing projects need scoped edits that preserve user work, not a forced overwrite of this command's output. Read the emitted result and complete every unfinished decision; scaffold generation is not a finished skill or a passing audit.

## create-02-contract

Apply [the guide-derived evaluation method](../references/evaluation-method.md) to
the skill being created, not to this builder. Capture a recurring baseline
failure or supplied expert correction, why a skill is useful, and which exact
steps belong in deterministic code. Do not require a new live baseline trial
merely to start useful work; record unavailable evidence honestly.

Collect or derive two or three representative requests, their available inputs and observable desired results. Include a meaningful boundary/failure case and a request that should not activate the skill. Preserve domain decisions from supplied examples and existing successful manual work. Do useful reversible work before asking for missing information. Ask only when the answer changes a consequential scope, effect, authority, output, or acceptance decision.

Write a task brief containing:

- Intended user and one concrete outcome.
- Accepted inputs, format, encoding, volume and trust assumptions.
- Actual outputs or state changes and independent acceptance conditions.
- Trigger terms, adjacent tasks, explicit exclusions and opt-out behavior.
- Required versus optional capabilities; unavailable-capability response.
- Files, network destinations, accounts, costs, processes and persistent data affected.
- Existing authorization for those effects, and actions that remain outside scope.
- Normal, boundary, negative, denied and interrupted cases with expected evidence.

Freeze acceptance conditions before optimizing a candidate. Identify who or what checks the result independently. A completion message cannot be the only acceptance condition. Define partial, blocked and uncertain outcomes as well as success. State assumptions and which ones the user must settle before a consequential operation.

Connect consequential requirements to source owner digests and case/check IDs
using `workflow-contract.json.template`. Check mappings and drift with the
installed `scripts/review.py contract`; retain independent semantic review.

## create-03-architecture

Read `handbook/03-architecture-and-subskills.md`, `handbook/07-security-and-privacy.md`, and the complete profile definitions in `catalogs/application-profiles.json`. Choose `instruction`, `resource_assisted`, or `suite_runtime` from actual needs. Add the `network`, `publication`, `persistent_state`, `authenticated_browser`, and `installer` modifiers whenever their effects exist. Review every unselected rule: an inaccurate capability declaration cannot waive a real effect.

Initialize a disposition for every one of the 99 canonical rule IDs. Keep applicability (`adopted`, `not_applicable`, `not_assessed`) separate from verification outcome. For a default that does not fit, record a reasoned override and reviewer. Retain the canonical basis and strength; a local required control is still a project policy unless its canonical basis is `specification`. Use the implementation map as a route to concrete work, not as proof that the target meets a rule.

Choose the smallest useful architecture and explain each nontrivial component. Separate discovery, task, execution, evidence, distribution and maintenance contracts. Keep contribution instructions and repository automation separate from runtime task instructions. Split separately discoverable skills when user intent, effects, tools or authority differ materially; use conditional references when one task has variant detail. Keep deterministic parsing, hashing, path checks and structured transformations in code where they prevent repeated errors.

For a skill with subcommands, define each route's inputs, output, side effects, prerequisites, scope and handoff. Do not claim that a Markdown heading automatically registers a host command. Identify whether the route is a mode of one skill, a separate discoverable skill, a native host command, or a CLI helper.

Write a task-specific threat/control table. Identify lower-trust data, protected files/accounts, boundary, enforcement owner, permitted behavior, denied behavior and evidence needed. Inventory each external data flow separately, including telemetry, crash reporting, model calls, browser traffic, storage, sync and publication. Record destination, content, default, authority, retention, opt-out, failure behavior and cost. Preserve explicit opt-outs across later setup and updates.

If generating artifacts, identify canonical inputs, variable contracts, adapter schema, generator version, output manifest and drift owner. If using workers, give each a source scope, output contract, budget and stop condition; use disjoint writes or one integration owner. Confirm readers finished or stopped before changing their snapshot. If using durable state, define ownership, schema, transaction/recovery and concurrent-writer behavior before implementation. Apply the corresponding full sections of [governance](../references/governance.md).

## create-04-implementation

Use `templates/minimal-project/` only as editable scaffolding. Copy only useful parts into the new project, replace every unresolved instruction/placeholder in its actual payload, and remove `.template` only after editing. Preserve templates inside this skill's immutable knowledge base unchanged. Give each executable and command one owner.

Write the portable `SKILL.md` with valid YAML `name` and `description`, matching name/directory, a meaningful body, and only declared portable fields. Put trigger and boundary terms early in the description. Do not move required safety conditions into optional prose that is loaded after the effect occurs. A compact entry point must still specify outcome, inputs/defaults, authority/effects, workflow, verification, recovery and output.

For every consequential instruction specify condition, action, evidence, failure behavior and authority. Check conflict cases: “read-only” followed by writes; “safe” without an enforcement layer; absent capability followed by a success claim; static fixture described as live monitoring; stale result reused for changed inputs. Search source, generated artifacts, command help, README and tests for other owners before changing a contract.

Provide realistic examples that teach decisions. Require exact output wording only when literal bytes are the public protocol. Remove task-irrelevant promotion, profiling, redundant approval rituals and unsupported productivity claims. Treat word and line counts as design signals; evaluate activated context and task behavior.

Before adding executable resources, read `handbook/05-commands-and-resources.md` completely and apply the command and security sections of governance. Document purpose, invocation, accepted inputs/limits/trust, stdout/stderr, schema, writes/overwrites, errors, exit codes, deadline, cancellation, retry, uncertain outcomes, cleanup and runtime prerequisites. Pass arbitrary data as structured arguments, stdin or private files; never use JSON encoding as shell escaping. Reject unsafe paths and ownership conflicts. Resolve resources from the installed root. Keep dependency preparation explicit and pinned; offline work must not fetch dependencies silently.

If the process captures output, define separate response-byte, capture-byte, deadline, process-tree-cleanup and retention budgets. If it writes state, define recoverable commit points and interruption behavior; atomic visibility alone is not a durability promise. If it uses remote mutations, define reconciliation before retry. If it uses secrets, test synthetic canaries in every relevant output sink. Do not execute target setup, hooks, tests, configuration or generators until their execution chain and effects have been reviewed.

## create-05-hosts

Read the current primary documentation linked by the KB's source register and the relevant supplied adapter guidance. Separate dated source documentation from locally observed behavior. If current documentation cannot be reached, retain the snapshot date and mark the changing claim unverified.

Keep task logic portable. Put discovery paths, invocation, resource-root resolution, tool names, approval semantics, native hooks, subagent lifecycle, OS/shell differences and packaging in explicit host adapters. Start with Codex; add Claude Code and Grok Build as distinct products. Treat Grok Bot and a custom xAI API host as separate targets with separate contracts. A model brand is not a host capability declaration.

Create capability records using `schemas/host-capabilities.schema.json` and its guide/example. For each target record product, surface, distribution, exact version or reason unknown, OS, execution policy, documentation evidence and tested evidence. Each capability needs availability, implementation, documented range, tested versions, case IDs, actual exercise and failure behavior. Maintain format, discovery, functional, safety and support claims independently. An untested feature must not become supported by default. A required missing capability blocks the affected branch; optional gaps remain visible while useful work continues.

Translate semantics rather than copying field names. In particular, recheck `allowed-tools`, `user-invocable`, implicit invocation, permission lifetime and discovery precedence for the target version. Do not treat an advisory instruction as a sandbox or native authorization restriction. Avoid unnecessary permission grants and unneeded hooks.

Define the shared interoperability panel: explicit invocation, implicit positive, negative trigger, unrelated working directory including spaces, missing capability, denied action, malformed result, interruption, artifact verification and cleanup. Include the four temporal/identity families in `evaluations/case-designs.json`: continuation/compaction, re-invocation and source edits/removal/disablement, duplicate names/namespaces, and resource identity. Record what artifact actually activated where exposed. Distinguish loaded text, invocation permission and durable state; record unavailable identity or actual compaction evidence honestly. A simulated context-loss exercise cannot be reported as live host compaction.

## create-06-evaluation

Apply [workflow evidence and feedback](../references/uber-workflows.md) to this
subject: adapt observable trajectory requirements, annotated field cases and
clean-environment checks. Review step completion and recovery with the advisory
`scripts/review.py lint`. Keep incident evidence local using the emitted
`papercut.json.template`, linking fixes to independent regression receipts.
For instruction changes, use `ABLATION-PLAN.md` and named variants, blind paired
artifacts and identical-payload repeats before claiming savings or pruning.
Unavailable trials stay unrun; these companions do not replace the 99-rule ledger.

Complete the helper's `EVALUATION-PLAN.md`, `EVALUATION-REVIEW.md` and
`evaluation-review.json`. The emitted `evals/*.json.template` files are additional
editable worksheets outside the frozen KB, not ready tests. Derive real routing
and execution JSON from this target's examples and domain failures; replace all
scaffold values, define independent check meanings and keep the held-out cases
separate from description optimization. Never substitute the builder's own
20-query corpus or test results for this skill's evidence.

Use the installed `scripts/evaluate.py prepare` with explicit target case files
and fixture root (see [the CLI contract](../references/cli.md#target-specific-evaluation)).
It freezes identities and a plan; it neither invokes agents nor grades output.
Keep no-skill, explicitly loaded candidate, automatically selected candidate and
prior revision distinct. Normalize real activation/full-read evidence, compute
routing confusion/majority metrics, grade actual task artifacts independently,
and retain every attempt, denied effect, unknown measurement and unscored gap.
Only run authorized host trials; missing capability blocks that claim, not all
independent work. The evaluator is available in the runtime package without the
source repository. Record actual loaded context/cold-warm costs before pruning.

Read `handbook/06-testing-and-evaluation.md`, `evaluations/README.md`, all 22 designs in `evaluations/case-designs.json`, `schemas/README.md`, and the full applicable schemas. Instantiate relevant designs with realistic prompts, fixture paths/hashes, reset procedure, allowed resources, forbidden effects and independent acceptance checks. Keep rejected or nonapplicable designs visible with a reason. Separate development and held-out cases.

Run separate evidence layers:

1. Package checks on the exact distributed skill, including metadata, references, unresolved placeholders, resources, notices and debris.
2. Resource checks on actual command boundaries: valid, empty, malformed, unusual, oversized, denied, interrupted, conflicting and missing-prerequisite cases, actual files/state and exit/schema results.
3. Agent discovery and full task evaluations, including near misses, paraphrases, explicit opt-outs, missing capabilities and hostile data.
4. Actual enforcement and lifecycle checks for claimed safety, OS, installer or remote capabilities.

Inspect executable checks before running them. Use an appropriate isolated environment within current authorization. Do not infer containment from a directory name, hook, process exit or reassuring test label. Confirm that discovered tests are nonempty and that skips, unavailability and failures remain distinct. Preserve raw or appropriately redacted evidence, errors and every attempt.

For comparisons, predeclare acceptance, retries, exclusions, budgets, grader and candidate/control identities. Use the same task inputs, tools, settings, budgets and warm/cold conditions. A no-skill control must lack the candidate instructions through all paths, including repository policy, hooks, inherited context and memory. Compare a previous version when available. Keep expected outputs and graders outside attacker-controlled input. Calibrate subjective grading and retain disagreements. Retain negative and inconclusive comparisons; do not silently change the grader or retry until a preferred result appears.

Read `handbook/08-performance-and-cost.md` when measuring or optimizing. Include actual loaded references, total work, retries, verification, worker integration and user interruptions. Record timing and measured usage or clearly labeled estimates; unknown usage stays null with a reason. Keep counts/denominators, repeats, task-selection limits and infrastructure exclusions. Do not claim improved reliability, speed or cost without the relevant comparison.

For every adopted rule update procedure, evidence and outcome in the traceability record. Do not mark a rule passed because its text appears in the skill. Validate all new records with the original schema validator. Read the emitted limitations of the format validator: passing its implemented checks does not establish semantic completeness, recursive link coverage, host discovery, function or security. Where a required property is outside its scope, perform an independent check or leave the gate incomplete.

After a meaningful change, run the affected checks again against the new identity. Keep old receipts unchanged as historical evidence. For a claimed regression fix, retain before/after evidence when practical or explain why historical reproduction was unavailable.

## create-07-package

Read `handbook/09-installation-and-releases.md`, `handbook/10-github-and-maintenance.md`, and `checklists/release.md` in full. Build the actual release artifact from declared inputs. Include all runtime dependencies/resources and applicable licenses/notices; omit local credentials, caches, private traces and unused development material. Do not silently omit knowledge the user explicitly required to preserve. Document any intentional full-corpus payload choice.

Keep repository documentation separate from the installable payload where possible. Write a README that begins with the task, realistic input/output example and honest support matrix, then prerequisites, inspectable quick start, effects/data flows, limits, update/removal, evidence and maintenance. Ensure examples and commands exist and match the packaged artifact. Provide contribution instructions naming canonical/generated ownership, proportionate PR evidence and valid checks. Provide supported-version and security-reporting information without inventing a contact, response promise or maintainer commitment.

Retain source, revision, license and modification attribution for copied/adapted material. Apply an already authorized license choice and full text for each covered original-material scope; do not request the same choice again. Consult the current outer [LICENSE.md](../LICENSE.md) and [license decision](../references/license-decision.json) for this builder's original work and the identified KB snapshot. The archive's older pending-status text remains historical. A new project needs its own applicable grant, and retained upstream excerpts keep their original terms. Complete the reviewable package even when a actually unresolved public-release gate is blocked, and state that exact decision.

If providing an installer or lifecycle command, define target host/scope/version, destinations, existing-file/ownership checks, prerequisite and network effects, staging, validation, activation, receipt and discovery verification. Map every writer, including setup, team initialization, repair/refresh and migration. Test preservation and recovery for local edits, untracked/local-only work, foreign folders, malformed versus missing settings, repeated runs, unrelated hooks, partial dependency/build/activation failures, concurrent changes, rollback, uninstall and reinstall. Do not claim live installation from a package-only manifest.

Give migrations one deterministic owner with current/target schema, ordered bounds, completion receipts, failure recovery and repeat behavior. Define rollback across code, dependencies and state or explicitly limit the claim. Uninstall only owned integrations and preserve modified/unrelated user data and chosen outputs/credentials/logs. No broad deletion based on a familiar directory, VERSION file or nested repository marker.

For generation, build twice under the recorded environment, compare bytes and check drift; exercise a controlled input change in a disposable copy where needed. Validate references/ranges, schema records, exact resources and source/output agreement. Bind receipts to the payload identity without a self-hashing archive cycle; a detached final archive checksum can identify the enclosing deliverable. Describe the checksum trust model rather than claiming publisher authenticity from hashing alone.

## create-08-delivery

Prepare a named release verdict: `READY`, `BLOCKED`, or `READY WITH EXPLICIT NONBLOCKING LIMITS`. List blocker IDs and their release consequences. A severe authority, data-loss, secret, confinement or fabricated-evidence defect cannot be offset by an average score. Unknown required checks block the claim they are meant to support; they do not necessarily block a narrower, honestly described local package.

Deliver the concrete project, requested archive and documentation with the exact checks and outstanding decisions. Mark native host trials, installation, no-skill comparisons and publication unrun when they were not executed. Do not advertise universal compatibility or improvement from structural checks or worker agreement.

Execute external publication, merge, deployment, installation or account changes only when the current task covers that destination and effect. Complete preparatory work before asking about a missing consequential authorization. If already authorized, proceed under the actual host policy and verify remote artifact identity afterward. Reconcile uncertain remote outcomes before retry. A blocked external step does not justify abandoning a completed local deliverable.

## create-09-recovery

On interruption, preserve an owned checkpoint containing task identity, active artifact/root/hash where exposed, user scope, decisions and authority source, profile/modifiers, source reads completed, output identities, per-rule status, pending checks and effects already attempted. Do not record secrets. Reconcile current files and any uncertain external effects before resuming. Do not reuse stale authorization or a pass from changed bytes only because it is recent.

If a mandatory capability is absent, stop only the dependent branch, state what cannot be established and continue independent work. Do not install dependencies, switch to an unsafe execution path, or broaden filesystem/network access silently. On a failed write retain existing user data and truthful status; a partial output is not complete. On worker failure keep missing coverage visible. On timeout establish process/worker termination before changing the shared snapshot.

## create-10-output

Deliver target-specific routing/execution cases and their oracle/fixture
identities, the completed supplemental evaluation review, and either a frozen
plan with observed results or exact unrun/blocked reasons. Do not deliver only
the helper's untouched templates as completed evaluation work.

A completed creation workflow supplies the following, scaled to the actual task while retaining explicit nonapplicability:

- Task brief, architecture/effects/threat decisions and all-99 applicability/verification record.
- Portable skill, every needed resource, explicit host adapters and capability/support evidence.
- Concrete evaluation panel and truthful receipts, including unrun/blocked checks and measurement limits.
- Exact package, owned-file/identity manifest, applicable notices and license status.
- README, contribution/security/maintenance information and release notes where appropriate.
- Release verdict with named blockers, next actions, and artifact links.

Explain what changed, why the design fits, how it was verified, material effects/data flows and the limits of the evidence. Distinguish the generated scaffold, the completed agent workflow and any external release action.
