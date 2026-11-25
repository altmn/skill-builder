# Requirement coverage and evidence boundaries

This skill implements the knowledge base through explicit create, audit and explanation procedures, deterministic retrieval/intake helpers and complete source preservation. Implementation coverage is a map of required work. It is not a claim that every target satisfies every rule, that every control is automatic, or that all hosts have been tested.

## Contents

1. [What remains canonical](#canonical-ownership)
2. [How to apply all 99 rules](#complete-rule-assessment)
3. [How the implementation map works](#implementation-map)
4. [Coverage beyond the rule list](#supplemental-contracts)
5. [Machine checks and semantic review](#evidence-levels)
6. [Preservation and changes](#preservation)
7. [Completion and release claims](#completion)

## Canonical ownership

`references/knowledge-base.zip` is the exact supplied archive, including the original historical metadata. `references/knowledge-base-manifest.json` identifies the substantive source members and their byte identities. The helper exposes the 182 substantive files; archive transport entries do not become active skill instructions. No handbook, catalog, source record, template, script, schema, original receipt, reader or notice is condensed into a replacement.

The original `catalogs/requirements.json` owns the 99 rule statements, verification descriptions, authority basis, strength and source IDs. It distinguishes five specification-based rules and 94 project-policy rules; strengths are 43 required, 34 conditional and 22 recommended. `catalogs/application-profiles.json` selects IDs without rewriting their meaning. The original chapters, checklists and detailed audits retain the context and qualifications that a rule ID alone cannot express.

The operational [governance](governance.md), [create workflow](../commands/skill-builder-create.md), [audit workflow](../commands/skill-builder-audit.md), and [explanation workflow](../commands/skill-builder-explain.md) tell the agent when and how to apply that full source. Read the original files through the helper, for example:

```text
python3 -I -B scripts/skill_builder.py kb read catalogs/requirements.json
python3 -I -B scripts/skill_builder.py kb read catalogs/application-profiles.json
python3 -I -B scripts/skill_builder.py kb read checklists/audit.md
```

These examples assume the activated skill root as working directory. From another directory use the absolute helper path. Never select an unrelated same-name script from the caller's directory.

## Complete rule assessment

For every creation or audit:

1. Read the full canonical rule catalog, profile description/definitions, workflow and applicable handbook chapters. Read the relevant detailed audit/source records when their mechanisms or counterexamples matter. A preview or truncated output is incomplete reading.
2. Select the smallest accurate architecture profile and all actual-effect modifiers. Confirm profile assumptions against actual behavior. Review unselected rules instead of deleting them.
3. Create exactly one disposition for every canonical rule ID. Use `adopted`, `not_applicable` or `not_assessed`. Preserve canonical basis/strength and a concrete applicability/override reason. Record the reviewer in companion metadata if the original schema has no reviewer property.
4. For each adopted rule state the actual failure scenario, source/authority, manual/automated verification procedure, evidence artifact and release consequence. Map the required work to the actual target, rather than copying an example's favorable verdict.
5. Perform each applicable assessment. Record `passed`, `failed`, `blocked`, `not_run`, `inconclusive` or `not_applicable` separately from the applicability decision. A rule's adoption, presence in a prompt, or entry in this map never proves it passed.
6. Validate the original rule-traceability schema and cross-field constraints, then inspect evidence and scope. Structural validity cannot establish whether observations are true.
7. Report unresolved mandatory gates by ID and the exact claim they block. Keep recommendations and justified nonblocking limitations separate. Revisit affected rules when effects, instructions, code, host semantics or dependencies change.

Profile selection is proportionate local policy. It does not require an instruction-only writing skill to acquire a daemon, installer or migration system. It also cannot excuse actual unselected effects: local writes still need destination/ownership handling, and external publication still needs current authorization. An unknown capability is a review gap, not a reason to label its controls nonapplicable.

## Implementation map

[implementation-map.json](implementation-map.json) contains exactly one implementation entry for each original rule. It deliberately does not copy the full statement text into a second manually maintained catalog.

| Field | Meaning |
| --- | --- |
| `id` | Exact unchanged canonical rule identifier. |
| `basis`, `strength` | Canonical classification, retained unchanged for consistency checks. |
| `canonical_pointer` | JSON Pointer into the original rule array, whose matching ID must be verified. |
| `owners` | Concrete operational document sections, with paths relative to the installed `skill-builder` root. |
| `applicability` | The real capability/effect/claim that triggers the procedure. |
| `enforcement` | One or more of `agent-procedure`, `deterministic`, `host-dependent`. |
| `verification` | Concrete work needed to assess the rule at the relevant boundary. |
| `assurance_limit` | What implementation routing and local checks cannot establish. |

`agent-procedure` requires actual reading, judgment and evidence from the agent. `deterministic` identifies a mechanical obligation that can be checked in code; it does not assert that this helper implements every property of every future target. `host-dependent` requires the actual host/product/surface/version/policy and its enforcement or lifecycle behavior. A single rule can require all three layers.

Every entry points to a shared owner and the create/audit phases that apply it. Explanation mode routes users to full original topics and carries the same authority/evidence boundaries. The map is a navigation and maintenance artifact, not a compliance score or test receipt.

To check routing integrity, compare its ID set and classifications with the original catalog; require no omissions or duplicates; check every owner file/anchor exists; verify each applicability trigger and procedure still matches its owner. If source policy is deliberately updated later, version the overlay and preserve the historical original instead of editing the retained snapshot silently.

## Supplemental contracts

The full knowledge base includes detailed obligations that should not disappear just because no new rule ID was added. The operational owners explicitly retain:

| Contract | Operational owner | Original detailed source |
| --- | --- | --- |
| Loaded instruction, invocation-permission and durable-state lifetimes | Governance `g-host` and `g-continuation`; create host/recovery phases; audit claims/recovery phases | `handbook/04-portability.md`; evaluation cases HOST-03–HOST-06 |
| Actual activated artifact, duplicate names, namespaces, resource roots and unsupported identity | Governance `g-host`; create host panel; audit host claims | `sources/host-documentation-register.json`; `evaluations/README.md`; paired identity probes |
| Every lifecycle writer, malformed versus missing settings, local/untracked work and foreign marker folders | Governance `g-lifecycle`; create package phase; audit validation phase | `audits/lifecycle-entrypoints.md`; `handbook/09-installation-and-releases.md` |
| Response bytes, live capture storage, deadline, descendant cleanup and retention as separate controls | Governance `g-command` and `g-performance`; resource implementation and audit effects | `handbook/05-commands-and-resources.md`; `handbook/08-performance-and-cost.md`; runtime capture clarification |
| Numeric source intervals separate from search selectors and exact review-depth labels | Governance `g-evidence`; audit inventory/instructions/report | `schemas/source-review.schema.json`; `handbook/12-audit-an-existing-project.md` |
| Independent support axes and unknown measurements | Governance `g-host`, `g-performance`, `g-evidence`; evaluation/report phases | `schemas/host-capabilities.schema.json`; `schemas/evaluation-receipt.schema.json` |
| Later source observations and resolution events without inherited old passes | Governance `g-source`, `g-oss`, `g-evidence`; audit repair/report | `audits/review-followups.md`; `schemas/finding.schema.json` |
| Source/derived-view ownership, drift checks, deterministic builds and controlled edits | Governance `g-architecture` and `g-oss`; create packaging | `methods/BUILD.md`; `methods/README.md`; `handbook/10-github-and-maintenance.md` |
| Complete knowledge preservation and original-material license decision | Governance `g-source` and `g-oss`; create delivery; audit claims | Original `README.md`, `LICENSE.md`, `NOTICE.md`, `validation/preservation-audit.json` |
| Clean no-skill control, frozen expectations, failed graders and preserved negative results | Governance `g-evaluation`; create evaluation; audit validation | `handbook/06-testing-and-evaluation.md`; `audits/review-followups.md`; completed example receipts |

These are additional reading routes, not abbreviated substitutes for the source. Follow the full applicable chapter and original case/record before making a claim.

## Evidence levels

Keep these activities and their conclusions separate:

| Activity | What it can establish | What it cannot establish alone |
| --- | --- | --- |
| Archive/hash preservation | Supplied member bytes remain intact and reachable. | Every source claim is current, correct or licensed for public open reuse. |
| ID/owner-map check | All 99 IDs route to existing procedures. | The target passed the procedures or the agent actually performed them. |
| File inventory/instruction index | Paths, identities, counts and candidate review locations. | Full semantic review or executed behavior. |
| Portable structural validation | Its documented metadata and recognized direct-resource checks. | Full Markdown coverage, instruction correctness, host discovery or security. |
| Schema validation | Record structure and implemented cross-field consistency. | Truth, independent provenance or sufficiency of observations. |
| Resource boundary test | Observed local inputs/outputs/state/error behavior under that fixture/runtime. | Complete agent improvement, host support or all adversarial environments. |
| Agent task exercise | Outcome for the recorded task/host/model/artifact/policy. | General reliability, native discovery on other surfaces or a statistical advantage. |
| Actual enforcement/lifecycle exercise | The named boundary/scenario on the tested host/platform. | Unrelated controls, versions, writers or future changes. |
| Comparative panel | The measured difference under its declared tasks, controls, attempts and checker. | Universal productivity or correctness. |

A complete static audit may honestly report that execution is blocked. A finished local resource can coexist with unrun native-host discovery and unsupported maintenance. Keep those mixed states explicit rather than converting them to a single optimistic badge.

## Preservation

Never rewrite the archived corpus while fixing wrapper code, updating adapters, building packages or running checks. Extract to a new authorized location when an original tool requires a filesystem tree, inspect its chain before execution and keep generated changes outside the immutable source. Preserve historical receipts as historical; produce a new output for new validation.

The exact original ZIP is retained. Substantive extraction omits only archive transport metadata such as `__MACOSX` and `.DS_Store`; that omission does not remove content from the retained ZIP. Do not install nested example/probe skills accidentally. Preserve required notices and license texts in the distributed package, and document which original-material public rights remain unresolved.

## Completion

State what was completed and which claim is supported. Use named release blockers and nonblocking limitations. Do not equate “all requirements routed” with “all requirements passed,” “downloadable” with “published,” or “files copied” with “installed and discoverable.” Source preservation is complete when exact identities verify; semantic assessment is complete only to its reported scope and depth; public open reuse remains subject to the recorded license decision; native host claims require native evidence.
