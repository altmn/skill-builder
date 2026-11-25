# skill-builder-audit

Audit an existing skill project against the complete knowledge base. Default to report-only assessment: read the selected subject and write owned reports to a separate authorized destination. Auditing does not silently authorize repair, target setup, dependency installation, hooks, commits, pushes, account actions or publication. An explicit repair request can authorize scoped edits; honor that authorization without repeated permission questions.

The command-line helper performs deterministic intake and bounded structural checks. Its report is evidence for those checks only. Continue the full semantic, execution-owner, host, test, lifecycle and presentation assessment below.

## Contents

1. [Scope and required source](#audit-01-scope)
2. [Snapshot and inventory](#audit-02-inventory)
3. [Instructions and dependencies](#audit-03-instructions)
4. [Effects and enforcement](#audit-04-effects)
5. [Tests, performance and lifecycle](#audit-05-validation)
6. [Host and external claims](#audit-06-claims)
7. [Rule assessment and report](#audit-07-report)
8. [Authorized repair](#audit-08-repair)
9. [Continuation and failure](#audit-09-recovery)
10. [Output contract](#audit-10-output)

## audit-01-scope

Resolve the audit target from supplied paths, archive or repository reference and the conversation. Confirm the precise subject, requested hosts, revision or working-tree scope, requested depth, execution limits and report location using existing context. Inspect useful available material before asking about a missing consequential choice. If a remote source is required, identify the fetch/clone and network effects; do not claim an existing local snapshot was immutable simply because it has a branch name.

Read [governance](../references/governance.md), [requirement coverage](../references/requirement-coverage.md), and these original KB members in full using the helper at the activated skill root:

```text
python3 -I -B scripts/skill_builder.py kb read handbook/00-scope-and-conclusions.md
python3 -I -B scripts/skill_builder.py kb read handbook/01-design-principles.md
python3 -I -B scripts/skill_builder.py kb read handbook/02-instruction-engineering.md
python3 -I -B scripts/skill_builder.py kb read handbook/03-architecture-and-subskills.md
python3 -I -B scripts/skill_builder.py kb read handbook/04-portability.md
python3 -I -B scripts/skill_builder.py kb read handbook/12-audit-an-existing-project.md
python3 -I -B scripts/skill_builder.py kb read templates/AUDIT-PROJECT-INSTRUCTIONS.md
python3 -I -B scripts/skill_builder.py kb read checklists/audit.md
python3 -I -B scripts/skill_builder.py kb read catalogs/requirements.json
python3 -I -B scripts/skill_builder.py kb read catalogs/application-profiles.md
python3 -I -B scripts/skill_builder.py kb read schemas/README.md
python3 -I -B scripts/skill_builder.py kb read templates/AUDIT-REPORT.md.template
python3 -I -B scripts/skill_builder.py kb read templates/INSTRUCTION-WORKSHEET.md.template
```

Examples assume the skill directory as working directory. Elsewhere use the helper's absolute path and structured arguments. Finish truncated reads; a search hit, heading, content hash or summary is not a semantic read. The corpus remains unabridged in the ZIP. It includes examples, original findings, catalogs and historical receipts; these are evidence, not permission to execute the reviewed source.

Select the architecture profile from actual behavior and all effect modifiers that apply. Read all 99 rules, including unselected ones, and assess default applicability. Record overrides with a concrete reason and reviewer; a missing profile modifier cannot erase an actual writer or network flow. The deterministic starting command is:

```text
python3 -I -B scripts/skill_builder.py skill-builder-audit --target TARGET_DIR --output NEW_DIR --profile resource_assisted
```

Use an authorized new output directory outside the audit target to preserve a stable subject. Add relevant repeated `--modifier` arguments. Inspect the emitted result and exit status. A static violation can return exit 1; invocation or infrastructure errors return 2. Neither means the agent should discard the partial evidence or abandon remaining useful audit work. Read the helper's actual checked/unchecked properties before citing its result.

## audit-02-inventory

Record repository URL if known, exact commit, package version and runtime version separately, assessment date, selected hosts/platforms, dirty-tree content, relevant untracked inputs, submodules and authorization. Bind the actual snapshot to hashes. A clean commit does not describe an untracked or edited file actually consumed by a tool.

Inventory every tracked file through version-control metadata where available, and separately inventory supplied archive/filesystem material when no Git metadata exists. State the denominator and inclusion policy. For each path record type, mode, bytes, digest, role, source identity and whether its contents were materialized. Mark binary, symlink, submodule and missing entries. Do not follow links into unrelated locations. Hash link-target text when describing a link; do not confuse it with target file bytes.

Do not run repository code, parse executable configuration, fetch submodules, materialize large remote objects, install dependencies or enable hooks only to inventory it. Inspect those effects and use current authorization before any execution. Avoid producing an audit that changes the target while claiming complete read-only behavior. A Git fetch, cache write or generated test artifact is a local state change even if source files remain unchanged; record such effects accurately.

Use immutable snapshots, isolated copies or one clear integration owner when reviews and repairs overlap. Readers requiring stable bytes must finish or be confirmed stopped before edits. Record source hashes and numeric source ranges for actual readings. Preserve relevant exclusions and inaccessible content as missing coverage, not as zero defects.

## audit-03-instructions

Find every skill entry point, canonical template, delivered/generated variant, shared block, conditional reference, model overlay, host adapter, repository policy, command example and relevant help/error contract. Separate authoring inputs from installed bytes. Map at least skill→reference, skill→command, command→runtime/library, adapter→capability, generator→output and test→contract relations where those entities exist.

Use exact hashes to identify duplicate bytes. Record the actual source/duplicate relation and surrounding applicability. Identical source macros can expand differently by host, tool or model; inspect meaningful expansions. A unique-block index provides navigation and counts, not an approval verdict for every instruction. Never call an index a full semantic audit.

Read all unique authoritative workflows and relevant delivered expansions for the agreed scope. For each consequential instruction record condition, action, expected evidence, failure/recovery, authority/effect, host assumptions, source revision/path/numeric range, duplicates/conflicts, decision and verification case. Use the original worksheet. Classify keep, rewrite, move, implement in code, remove or needs verification; group broader findings into adopt/adapt/avoid/verify-before-relying-on.

Check trigger/outcome/inputs/exclusions/output, unavailable capabilities, partial completion, existing authorization and consequential scope expansion. Search for contradictions across prompts, code, generated text, help, README and tests. Inspect unsupported numerical claims, hidden-reasoning requests, task-irrelevant promotion/profiling, repeated permission rituals, hardcoded host assumptions and unconditional interviews. Treat domain claims such as accessibility thresholds as factual claims requiring their actual primary standard and units.

Maintain a per-file depth ledger using `semantic_full`, `semantic_targeted`, `structural_index`, `exact_duplicate`, `binary_metadata` and `symlink_metadata`. For targeted reading, state exact numeric intervals and unanswered questions. Search selectors are separate fields. A duplicate can inherit specified byte-level coverage from a fully reviewed original, but context-dependent behavior still needs its own review. Do not increase semantic counts after an automatic scan.

For large subjects, use the original `catalogs/README.md`, `catalogs/approach-catalog.md`, `catalogs/command-catalog.md` and relevant detailed audits to navigate comparable owner/failure patterns. Read the full relevant original records, surrounding source and qualifications before applying a counterexample. Do not copy benchmark severity or transplant a source project's product rules into the target.

## audit-04-effects

Read `handbook/05-commands-and-resources.md` and `handbook/07-security-and-privacy.md` completely. Trace actual sensitive operations end to end, from user input and defaults to their enforcing/consuming operation. Prioritize shell/process execution, local writes/deletes, installation/upgrade, configuration loading, credentials, network/redirects, browser sessions, outside models, paid calls, publication, migration and evidence storage.

For every public command identify name/aliases, invocation surface, owner, callers, prerequisites, input/output schema, encoding/limits/trust, stdout/stderr, effects/authority, errors/status, retries/deadlines/cancellation, cleanup, platforms and tests. Classify internal/retired helpers explicitly. A filename under `bin/` is not evidence of a public API. Preserve unknown fields as review gaps.

Trace both successful and adverse paths: absent/malformed/unreadable input, empty successful output, partial writes, stale receipt, authentication denial, permission denial, concurrent changes, timeout and uncertain completion. Inspect whether untrusted strings enter shell source, whether JSON encoding is mistaken for shell quoting, whether data-bearing values are passed safely, and whether output/diagnostics leak secrets or control sequences.

Map each claimed control to its actual layer: instructions, user approval, hook, wrapper, filesystem/network boundary, service authorization or OS sandbox. Evaluate the named guarantee at that layer. A prompt or selected-tool hook is advisory outside its enforcement reach. Do not call a documented advisory control defective only because it lacks an unclaimed stronger boundary; do report broad claims that the implementation cannot support.

For filesystem behavior inspect traversal, symlink/parent changes, hardlinks where relevant, case/path rules, check/use races, destination ownership and overwrite/deletion semantics. For network behavior inspect exact destinations, redirects, proxies, DNS/private-address limits and account authority. For browser reuse inspect account access, allowed actions, isolation and cleanup. For secret/data flows inspect every output sink, retention, opt-out and default separately; telemetry disabled does not establish no egress.

For process capture evaluate response bytes, bytes retained during execution, deadlines, descendants and retention as separate contracts. A read cap applied after exit does not bound running storage. Confirm startup failure and stderr truncation, not only normal stdout. Parent exit alone cannot prove descendant termination. For state writes inspect atomic visibility, durability claims, multi-file recovery and concurrency. For remote writes verify reconciliation before retries and preservation of original failure evidence.

Record each concern with exact source, conditions, affected resource, impact, confidence basis, evidence type, owner, recommended change and independent verification. Until reproduced, describe a static failure path as a source-level concern. A source finding is not evidence of actual exploitation or measured damage. Keep uncertain conclusions bounded.

## audit-05-validation

Use [workflow evidence and feedback](../references/uber-workflows.md) to assess
the subject's stable requirement/case mappings and source drift, observable
trajectories, annotated field cases, clean environments, local incident closure
and blinded instruction comparisons. The emitted contract/papercut templates
are worksheets, not mandatory formats for every subject. Run the bounded
`scripts/review.py` checks where applicable and review advisory lint locations
semantically. Missing mechanisms need a reasoned consequence, not a fabricated
failure or pass. Keep outcome, trajectory and activation evidence separate;
an unsafe observed action cannot disappear because the trace is incomplete.

Apply [the supplemental evaluation method](../references/evaluation-method.md)
to the audited skill. Complete the helper's `evaluation-review.json` and
`EVALUATION-REVIEW.md` using target file/line evidence. Assess task value and
scope, optional metadata/host variants, target-specific routing labels and fixed
splits, real activation evidence and confusion matrices, clean controls and
explicit/automatic/prior separation, independent grading, context/resources,
trust/recovery and evidence-backed operational claims. These are supplemental
review topics, not new canonical rules or automatic pass/fail findings.

Inspect the target's cases, fixtures and receipts rather than reusing the
builder's corpus. Missing metrics mean routing is unverified, not proven bad;
missing comparisons mean improvement claims are unsupported, not proof of no
benefit. Record applicability, status, source locations, related finding IDs and
the exact blocked claim. Keep absent mechanisms separate from unassessed work.

When evaluation is authorized, adapt the emitted target worksheets and use the
installed `scripts/evaluate.py` with explicit case files and an approved fixture
root. Inspect target code before execution; preparation/accounting alone need no
target execution or model calls. Leave unavailable trials unrun and finish the
source assessment. Require evidence for safety invariants even if activation is
unobservable; an incomplete trace must not hide a known unsafe effect.

Read `handbook/06-testing-and-evaluation.md`, `handbook/08-performance-and-cost.md`, `handbook/09-installation-and-releases.md`, `evaluations/README.md`, all `evaluations/case-designs.json`, `audits/lifecycle-entrypoints.md` and `checklists/release.md` in full when the corresponding capabilities exist. Retain a justified nonapplicability for absent mechanisms; all 99 rules still receive a disposition.

Inspect what tests assert and what they execute. Separate structure, resource, agent outcome, safety, lifecycle and performance evidence. Trace hooks/plugins/configuration/package-manager scripts/downloads before invoking any target check. Keep independent graders and authoritative expected outputs outside the target's control. Prefer controlled inert fixtures for negative security checks. Running audited code requires suitable isolation and actual task authorization; do not execute dangerous setup simply to obtain a green test count.

Check that test discovery is nonempty, omitted providers/skips do not become pass, assertions verify actual files/state, malformed or empty successful outputs fail appropriately, and candidate identity matches the tested/distributed bytes. Review the purpose of each test, meaningful regression boundary and risk hidden by mocks. A code-string match cannot replace behavior evidence unless exact text is the intended protocol.

Inspect evaluation prompts, controls, held-out tasks, predeclared acceptance/retry/exclusion policies, budget, repetitions, grader calibration and preserved failed attempts. Verify the no-skill control is free of candidate instructions through all loading routes. Report denominators, sampling limits, infrastructure exclusions and attempt variability. Reject best-attempt-only reliability and unsupported speed/productivity claims. Keep unknown costs/tokens/calls unknown with reasons, and inspect paid parent/worker bounds before calls where applicable.

Review end-to-end context/latency/resource measurements, loaded references, warm/cold conditions, cache keys/invalidation/retention, failed calls/retries and user interruptions. Performance optimization must preserve task and safety acceptance. Persistent processes need measured benefit plus lifecycle/security support, not an unsupported “lightweight” label.

Map every writer in the lifecycle, not just the main installer: setup, team initialization, update, refresh/repair, migration, rollback and uninstall. Check precise host/scope/version, dependency pin/failure behavior, owned paths and saved predecessors, staging/activation, discovery verification, channels, migration owner/bounds, concurrency and recovery. Distinguish missing settings from malformed/unreadable existing settings. Preserve edits, untracked/local-only work, foreign VERSION folders, unrelated configuration/hooks and selected user data. Do not infer ownership from names or generic marker files.

Check rollback across package, dependencies and schema; a channel change alone may not restore current bytes. Review uninstall's cleanup of only owned integrations, hooks/processes, shared directories and explicit retained data. Verify platform claims through actual evidence. A PowerShell script's existence is not a Windows test. Record each unreviewed branch and unexecuted scenario.

Execute only the reviewed, authorized subset in a suitable environment. Record exact arguments, executable/tool versions, input identity, reset state, status, evidence and limits. If runtime execution is unavailable, finish the static audit and list the exact needed verification; do not substitute a fabricated runtime receipt.

## audit-06-claims

Read `handbook/10-github-and-maintenance.md` and the relevant primary-source entries. Verify changing host behavior, format fields, security mechanisms and domain standards against current primary documentation. Pin source commits, record access/capture dates and retain a bounded supporting excerpt or known revision when permitted. Use dated documentation when current access is blocked, labeling freshness limits.

Separate format requirements, documented host behavior, benchmark observations, reproduced empirical results and project recommendations. Keep Grok Build, Grok Bot and API/custom hosts distinct. Check discovery roots, native invocation, `allowed-tools`, `user-invocable`, implicit invocation, hooks, workers, resource roots, approval and permission lifetime for each named host/surface/version/policy. Shared spelling or YAML parse success cannot establish equivalent semantics.

Assess format, discovery, function, safety and maintenance support independently. Verify advertised secondary-host outcomes with the shared accepted/denied panel. Review continuation/compaction, source replacement and re-invocation, removal/disablement, duplicate names/namespaces and resource/worker identity using HOST-03 through HOST-06. Capture actual activated artifact identity where exposed; intended files or visible markers alone are insufficient. Preserve identity gaps and simulated versus real context transitions.

Review README examples, install effects, data flows, limits/removal, supported versions, public evaluation claims, contribution guidance, security reporting, licenses and attribution. Check full immutable third-party action/reusable-workflow references, effective permissions, checkout/execution under privileged events, untrusted PR strings, caches/artifacts and release credentials. Existing source policies can be local choices; do not recast them as universal standards.

A public open-source release needs actual selected licensing for original components as well as retained third-party licenses. Assess the target's current rights-holder decision and its component/snapshot coverage. For this builder and its identified original KB material, consult the current outer [LICENSE.md](../LICENSE.md) and [license decision](../references/license-decision.json): MIT is selected effective with rc.2. The unchanged archive's pending-selection text is historical and does not keep that choice unresolved. Retained third-party material keeps its own terms; the builder's MIT decision does not supply a grant for another project's original work. Record a genuinely missing or unselected target-specific grant as a publication blocker without stopping the useful audit. Keep licensing separate from authorization to publish, native-host evidence, and other release gates.

## audit-07-report

Include the supplemental evaluation assessment and evidence-linked findings or
reasoned limits for each applicable topic above. Separate format conformance,
documented host behavior, project recommendations and measured results. Require
actual loaded-context/token evidence for efficiency claims; prose length and KB
bytes alone are insufficient. Do not promote this builder's own test passes
into evidence that the audited skill is useful, safe or ready for release.

Finish all 99 canonical rule records. For each record retain applicability/override reason, reviewer, failure scenario, canonical authority basis, source IDs, verification procedure, actual evidence, outcome, release consequence and uncertainty. Keep adopted-but-unrun separate from nonapplicable and unassessed. Check defaults against actual capabilities. Treat all applicability profiles as local selections, not certifications.

Use `templates/AUDIT-REPORT.md.template` for the report and the original versioned schemas for findings, source reviews, capabilities, evaluation receipts and traceability. Do not invent extra fields inside records that prohibit them; place additional reviewer/run metadata in an explicitly documented companion record. Validate records structurally and then inspect their evidence. Conforming JSON can still contain false claims.

Lead with the verdict and specific priority actions. Use severity based on consequences and confidence based on evidence. Name blockers independently of aggregate scores. For every finding include ID, affected paths/revision/ranges, observed behavior, evidence type, failure scenario, impact/severity, recommendation, owning layer, independent verification and known limits. Preserve concrete strengths and useful patterns as well as problems. Avoid statements of total safety or “all clear” when the evidence covers only static source.

Display coverage prominently: total paths/bytes, full and targeted semantic reads, structural indexing, exact duplicates and binary/symlink metadata. State instruction-block and expansion denominator/method, excluded branches, missing capabilities and executed checks. Do not let an inventory of every file imply every line received semantic review. Retain source and uncertainty for every important conclusion.

Give remediation order by impact and dependencies, with owner, estimated effort and completion evidence. Separate mandatory repairs, useful adaptation and optional design/style advice. Preserve historical adverse results. When later source arrives, record both identities, changed-path coverage, affected contracts and dated resolution/reopen/unchanged events; a changed filename is not a verified fix.

## audit-08-repair

When requested, make scoped corrections at the owning layer and preserve unrelated/user work. Separate necessary fixes from optional refactoring. Revisit authorization if the effect materially changes, not only because a new reversible file edit is needed. Confirm reviewers have finished or stopped before changing their snapshot.

Re-run checks for affected contracts against the repaired identity; record both attempts and any required before/after regression evidence. Do not apply old passes to edited bytes. Update dependent instructions/help/docs/generated artifacts and check drift. Append finding resolution events with evidence instead of rewriting the original observation.

Commit, push, merge, publish, install or deploy only when the current task covers those exact effects and destination. Prepare concrete results first. If an external action is unavailable, deliver the repair and remaining precise action. Verify an authorized remote effect, and reconcile uncertain completion before any retry.

## audit-09-recovery

If source identity changes, preserve existing reports, record the new identity and re-scope relevant checks. If a required file/capability cannot be read or used, mark the affected assessment blocked/not run and continue independent coverage. If an execution times out, do not assume it stopped; confirm termination before conflicting work or retain the uncertainty. Never silently fall back from failed isolation into the user's active environment.

For long or interrupted audits keep an owned checkpoint with target identity, authorized effects, source-read coverage/ranges, rule statuses, output paths/hashes, worker states, decisions/authority sources and attempted external effects. Restore from trusted current artifacts after context loss. Recheck actual source and permission lifetime. A summary or old receipt cannot grant new authority.

## audit-10-output

Deliver:

- A prioritized evidence-linked report with `READY`, `BLOCKED`, or `READY WITH EXPLICIT NONBLOCKING LIMITS` scoped to the actual claim.
- Exact subject identity, all-file inventory, per-file review-depth ledger and instruction/dependency index.
- A complete 99-rule applicability/verification record and machine-readable findings.
- Host capability/support matrix, effects/control/lifecycle tables, source register and truthful execution receipts where applicable.
- A concrete remediation plan and any separately authorized fixes, with changed-identity verification.
- Explicit unassessed scope, failed/blocked/unrun checks, measurement limits and next actions.

An audit can be complete as an assessment and still find release blockers. State both the completed work and the target's verdict.
