# Independent requirement-coverage review

## Verdict and scope

**No missing substantive operational instruction was found among the 99 canonical rules.** All 99 have a concrete applicability condition, an assessment or implementation action, a verification obligation, and a substantive procedure owner. This conclusion comes from reading the rules, every implementation-map entry, and the cited operational procedures; it is broader than checking that links exist.

**No material requirement outside the 99-rule catalog was found lost in the reviewed handbook, checklist, schema, profile, template, and evaluation guidance.** The original archive is preserved byte for byte, and the operational layer explicitly retains the major supplementary contracts. No contradiction was established between the reviewed claims about automatic checks and the create/audit/explain procedures.

These are findings about **source preservation and procedural coverage**, not a claim that all 99 rules are automatically enforced, that the candidate meets every applicable rule in execution, or that any native host was exercised. This reviewer executed no candidate code, archived validator, setup, test, hook, installer, or host trial. The review does not supply a release or security certification.

Subject: `/workspace/scratch/1e5ab00a904f/skill-builder-project/skills/skill-builder`.

Original comparison source: `/workspace/scratch/1e5ab00a904f/upload/agent-skill-project-knowledge-base_final.zip`.

Date: 2026-11-23. The source describes historical local dates separately; those dates were not rewritten.

## Coverage denominator and method

| Review population | Denominator | Work completed |
| --- | ---: | --- |
| Canonical requirements in archived `catalogs/requirements.json` | 99 | Read every field of every rule, including basis, strength, applicability, verification, and source references. |
| `references/implementation-map.json` rule entries | 99 | Read every entry and compare its operational meaning against the canonical rule and actual procedure text. |
| Canonical/routing identity checks | 99 | Independently checked matching ID, basis, strength, ordered canonical JSON Pointer, unique coverage, and existing owner anchors. No mismatch found. |
| Original handbook chapters | 13 of 13 | Read completely, `handbook/00-scope-and-conclusions.md` through `handbook/12-audit-an-existing-project.md`. |
| Original checklists | 3 of 3 | Read `checklists/audit.md`, `new-project.md`, and `release.md` completely. |
| Original schemas | 7 of 7 | Read every schema, including shared definitions and cross-field structure; also read `schemas/README.md`. |
| Original evaluation designs | 22 of 22 | Read all complete case records and `evaluations/README.md`; none was executed. |
| Other original guidance | 9 files | Read both application-profile files, `catalogs/README.md`, `methods/README.md`, `templates/README.md`, the create/audit instructions, audit-report template, and instruction worksheet completely. |
| Fully read original archive members | 36 of 182 substantive members | Semantic reading for this bounded coverage review. Remaining members are preserved and hash-checked, not credited as semantically reviewed. |
| Preserved archive and substantive members | 1 archive; 182 substantive files | Independent exact-byte comparison to uploaded ZIP, plus each member's recorded size and SHA-256. |

The operational documents read completely were `SKILL.md`, all three `commands/skill-builder-*.md` procedures, `references/governance.md`, `references/requirement-coverage.md`, `references/implementation-map.json`, `references/cli.md`, and `references/release-status.md`. The preservation manifest was parsed and every indexed member checked; its metadata rows were not treated as semantic source review.

`scripts/skill_builder.py` received targeted static reading: lines 1–182, 261–348, and 438–569. This covered archive identity/access, profile selection, traceability/scaffold construction, original-validator dispatch, audit status handling, search output, and record validation. The remaining implementation was not credited as fully read by this reviewer. No runtime conclusion was inferred from that reading or from other reviewers' reported test results.

## Preservation result

The bundled `references/knowledge-base.zip` exactly equals the uploaded original ZIP:

- SHA-256: `9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204`.
- Archive size: **11,572,664 bytes**.
- Original archive entries retained: **454**, including directory and operating-system metadata entries.
- Substantive manifest entries: **182 files**, totaling **76,965,199 uncompressed bytes**.
- Substantive member size or SHA-256 mismatches: **0**.

The equality comparison establishes preservation of all original bytes, including members not semantically read in this review. It does not establish the truth, freshness, licensing, or runtime correctness of all archived material.

The retained archive and documented closed-archive policy are compatible with complete preservation. Avoiding extraction inside a live discovery root prevents example/probe entry points from becoming unintended active skills. Omitting macOS sidecars from an explicit substantive extraction does not lose them from the preserved ZIP. These distinctions are stated in `SKILL.md` section 3, `references/governance.md#g-source`, `references/requirement-coverage.md#preservation`, and `references/cli.md#explicit-extraction`.

## All-rule operational coverage

In the following table, **covered** means the wrapper provides substantive instructions for the rule's actual condition. It does not mean that a particular target has passed the rule. Every ID in the stated ranges was individually compared; no unlisted gap is concealed by the group totals.

| Canonical IDs | Count | Assessment and substantive instruction evidence |
| --- | ---: | --- |
| FMT-001–FMT-010 | 10 | Covered. `governance.md#g-format` requires checking actual distributed YAML/body, name/directory/length rules, optional field types, duplicate/coerced/unsafe YAML, explicit adapter extensions, actual resource resolution, payload contents, and exact validator limits. `create-04-implementation`, `create-07-package`, `audit-03-instructions`, and `audit-06-claims` turn these into authoring/review actions. The verification text separately identifies conservative ASCII policy and properties the direct-link validator does not cover. |
| INS-001–INS-012 | 12 | Covered. `g-instruction` supplies the task/output contract, trigger and boundary work, five-part consequential instruction contract, load conditions, implementing-owner repairs, conflict searches, meaningful examples, claim labeling, and removal of irrelevant steps. `g-authority` and the create/audit contract/scope phases preserve authorization and useful work before questions; `g-continuation` requires visible partial/unavailable states. |
| ARC-001–ARC-008 | 8 | Covered. `g-architecture` specifies size selection, coherent independent intent, explicit handoffs, deterministic input/output ownership and drift checks, worker scopes and disjoint writes, confirmed reader termination, and separation of repository policy from runtime task instructions. `g-host` owns the portable/adapter division. `create-03-architecture`, `create-07-package`, `audit-02-inventory`, and `audit-03-instructions` apply these contracts. |
| HOST-001–HOST-007 | 7 | Covered. `g-host` and both host/claims phases require named product/surface/version/policy, independent evidence axes, translation of actual permission and invocation semantics, blocked dependent branches for missing capabilities, installed-root resource checks, shared accepted/denied panels, and bounded support claims. Native trials remain explicitly unrun in release status. |
| CMD-001–CMD-010 | 10 | Covered. `g-command` provides a complete public-command contract, explicit result states, structured data transfer, actual-operation path/ownership review, executable-chain inspection, deadlines/cancellation/termination, retry reconciliation, private temporary state and limited cleanup, durable-write recovery, and identity-bound reuse. The create implementation/evaluation phases and audit effects/validation phases name the corresponding boundary cases. |
| SEC-001–SEC-012 | 12 | Covered. `g-security` distinguishes data from authority and control layers, requires task-specific threat/control/data-flow records, preserves denials, calls for actual filesystem/network checks, scopes authenticated sessions, tests secret sinks and scanner limits, preserves opt-outs, budgets paid work, protects graders, and reviews privileged CI boundaries. `g-performance` and `g-evaluation` supply the budget and evaluator details. |
| EVAL-001–EVAL-014 | 14 | Covered. `g-evaluation` and the create/audit evaluation phases separate structure/resources/agent outcomes; specify independent artifact checks, trigger/adverse panels, clean controls, frozen policies, held-out/repeated work, grader calibration, named safety blockers, nonzero checks, exact candidate identity, meaningful regressions, and complete receipts. `g-evidence` specifies record semantics and prevents schema validity from becoming evidence truth. |
| PERF-001–PERF-006 | 6 | Covered. `g-performance` and both evaluation phases require whole-task measurement, matched cold/warm conditions, source/units/unknown values for metrics, cache identity/invalidation/retention, measured justification for persistent processes, and constant task/safety acceptance during optimization. |
| LIFE-001–LIFE-012 | 12 | Covered. `g-lifecycle` and package/validation phases specify selected host/scope/revision, ownership/predecessors, explicit dependency failure, staged activation, exact channels, bounded migration owner, rollback compatibility, limited uninstall, final artifact checks, checksum trust model, claimed-platform trials, and authorized publication with state reconciliation. `g-authority` and delivery/repair phases govern external effects. |
| OSS-001–OSS-008 | 8 | Covered. `g-oss` and package/claims phases require task-first README examples, truthful evidence and negative results, canonical contribution owners, proportionate PR evidence, complete licensing/attribution, actual reporting/support scope, reviewed immutable workflow dependencies, and dated maintenance/source-update events. |
| **Total** | **99** | **99 procedurally covered; 0 missing substantive operational instructions identified.** |

Paths in this table are relative to the subject root: `g-*` sections belong to `references/governance.md`; `create-*` sections belong to `commands/skill-builder-create.md`; `audit-*` sections belong to `commands/skill-builder-audit.md`. Per-ID routes and exact verification obligations remain in `references/implementation-map.json` rather than being copied into another mutable rule catalog.

### Why this is more than link coverage

The owner sections contain actions and failure handling, not just a command to read another document. For example, CMD-007 is tied to reconciling an uncertain mutation before retry; ARC-007 requires confirming a timed-out reader stopped before modifying its snapshot; EVAL-010 prohibits treating zero discovered checks or unavailable providers as success; and FMT-008 requires an independent check for required references outside the preserved validator's direct-link scope. The workflows also require full relevant original source before decisions and require unfinished checks to remain visible.

The implementation map preserves all five specification-based and 94 project-policy classifications. It does not convert recommended or conditional controls into universal format mandates. Required local policy is kept separate from specification authority.

## Conditional applicability and helper responsibilities

No omission was assigned solely because the local helper does not implement network access, a browser service, a paid evaluator, an installer, migration, rollback, or publication. Those mechanisms are not required just to prepare scaffolds and static audit evidence. Their rules are preserved, their triggers are explicit, and the procedures require them when the target's real effects make them applicable.

The original profile defaults can omit controls for effects not declared by the profile. The wrapper addresses that limit substantively: `SKILL.md` section 4, `g-authority`, `create-03-architecture`, and `audit-01-scope` require reading all 99 rules, inspecting actual effects, reviewing unselected IDs, and supplying factual nonapplicability or an explicit override. In particular, real local writes must still receive destination/ownership assessment even if a selected profile did not adopt CMD-004 by default. This is an agent responsibility, not an automatic guarantee of the selector.

The schema-2.0 traceability scaffold intentionally starts applicable work as `not_run` with no passing evidence. The CLI also retains the full canonical selection record, including basis and strength, while the procedures require companion metadata for reviewer fields not allowed by the original schema. That is consistent with `schemas/rule-traceability.schema.json` forbidding undeclared properties.

## Important contracts beyond the 99 IDs

| Additional requirement from original guidance | Operational retention |
| --- | --- |
| Instruction lifetime, invocation permission lifetime, and durable task state are distinct. | `g-host`, `g-continuation`, `create-05-hosts`, `create-09-recovery`, `audit-06-claims`, and `audit-09-recovery` require separate observations and recovery. |
| Actual activated identity; source edits/removal; duplicate names/namespaces; worker/resource identity; simulated versus live compaction. | Host procedures expressly incorporate HOST-03–HOST-06 from all 22 evaluation designs, require exposed native/source identity, and preserve identity gaps. |
| Response bytes, live capture bytes, execution deadline, process-tree cleanup, and retention are five different contracts. | `g-performance` lists all five separately; `create-04-implementation` and `audit-04-effects` reject substituting post-exit truncation or parent exit for stronger capture/descendant guarantees. |
| Every lifecycle writer, malformed versus missing settings, foreign marker folders, edited and untracked work. | `g-lifecycle`, `create-07-package`, and `audit-05-validation` name these cases and prohibit transferring the main installer's evidence to another writer. |
| Numeric source intervals are separate from search selectors; structural indexing is not semantic reading. | `audit-02-inventory`, `audit-03-instructions`, `audit-07-report`, and `g-evidence` prescribe exact depth labels, numeric ranges, denominators, and unreviewed scope. |
| Schema-2.0 record semantics, mixed support outcomes, and unknown measurements. | `g-evidence`, host/evaluation phases, and the all-rule workflow require original schemas and separate unavailable/unrun states. Schema validity is expressly insufficient to prove observation truth. |
| Historical source identity, later updates, and resolution events. | `g-source`, `g-oss`, `g-evidence`, and audit report/repair phases preserve original receipts, append dated events, and invalidate changed-byte evidence. |
| Derived-view ownership, deterministic builds, drift, and controlled canonical changes. | `g-architecture`, `g-oss`, and `create-07-package` require declared inputs/environment, repeat builds, source/output checks, and controlled changes in disposable copies. |
| Clean no-skill controls, failed grader calibration, negative comparisons, and complete attempt accounting. | `g-evaluation` and both evaluation phases explicitly retain those requirements; all 22 case designs remain available unchanged. |
| Rights to original material must be decided separately from retained upstream notices. | `g-oss`, create package/delivery, audit claims, explain answer guidance, and release status keep the original-material license gate explicit. |

The full handbooks remain mandatory input at the relevant decision points. Small details need not be duplicated into every wrapper paragraph to remain available and required: for example, the original instruction-change record's before/after size field remains in the complete required instruction-engineering chapter. The review did not treat preserved, explicitly loaded source as missing simply because its wording was not copied into a second document.

## Automatic-check claims versus procedures

No conflicting complete-audit or automatic-all-99 claim was found in the reviewed operational surface.

| Claimed automated result | Actual boundary described and statically inspected |
| --- | --- |
| `kb verify` / preservation `check` | Exact archive/member identity. `KnowledgeBase.verify` explicitly disclaims host or semantic assurance. |
| `skill-builder-create` | Scaffold and all-rule worksheets. The emitted result says `semantic_implementation: not_run`, `host_trials: not_run`, and `release_ready: false`; the create procedure requires continued domain work. |
| `skill-builder-audit` | Bounded filesystem inventory and original portable format/direct-resource checks. The audit result stays `inconclusive` after successful structure checks and records full semantic review and host trials as `not_run`. |
| `check --record` | Original versioned schemas and implemented cross-field checks. The scope expressly excludes truth of evidence; procedures require evidence review afterward. |
| `deterministic` in the implementation map | A mechanical verification obligation, not a claim this helper automatically enforces every property. This definition is explicit both in the map and in `requirement-coverage.md#implementation-map`. |

The fuller audit procedure requires tracked-file inventory and semantic review, while the helper intentionally reports bounded filesystem coverage and unknown Git/tracked coverage. This is not a contradiction: `audit-02-inventory`, `references/cli.md#audit-helper`, and the helper-generated README identify the remaining work. Likewise, missing optional dependencies block their check instead of producing a favorable native or semantic verdict.

## Remaining limits and action

**Actual new gaps requiring correction from this review: none identified.** There are no finding IDs to add for missing rule instructions or lost knowledge.

The following remain outside this review or already explicit in the candidate and must not be converted into passes:

- Runtime correctness and adversarial behavior of every helper branch.
- Actual execution of generated create/audit projects, independent task quality, or comparative benefit.
- Native discovery, activation, permissions, continuation, or resource identity on Codex, Claude Code, Grok Build, or other hosts.
- Freshness of current external product documentation. This review compared supplied source and procedures; it did not independently browse those products.
- Full semantic review of every original catalog row, historical audit, script, and receipt. Byte preservation covers those files; semantic reading here covers the stated 36-member subset.
- Public open-reuse licensing and an actual maintainer reporting route. `references/release-status.md` already records these unresolved decisions. They are not hidden coverage defects and this review does not resolve them.

Use this report as evidence for the narrow claim that the complete supplied knowledge was preserved and that all 99 rules plus the reviewed supplementary contracts have substantive agent procedures. Retain other reviewers' resource-test evidence and future native-host results as separate evidence sets.

## Reviewed identity checkpoints

| Subject file | SHA-256 at review completion |
| --- | --- |
| `SKILL.md` | `9fa84561bb0e328c29a3bd719412aa52bbc7529e3f4f74ef693afeecb813c373` |
| `commands/skill-builder-create.md` | `4a02ce2a2862cd567fe5ff47fa80c6af1460e33890cdc97494a7b309b9a81caf` |
| `commands/skill-builder-audit.md` | `cf617dbb1426f224ca2565d367a6e5ba7acb02b94de0a9317941907f58528bb1` |
| `commands/skill-builder-explain.md` | `8e9dbfeaa2d5985188908a01847fa3a1ad3e700ac7613a2d11a1de8124b013e9` |
| `references/governance.md` | `89e4de3a74d045e18613b8ee78a45759e23982cd852956b3cc75245ce2dbff51` |
| `references/implementation-map.json` | `b750c09ef869b57bb9baf89ea9df071973b5fb82db48ba31431d4bd4ea387472` |
| `references/requirement-coverage.md` | `8be34aa5f699d837c4014e8ecf7fec085bd756650c6d83612b9f4358add4d4e4` |
| `references/cli.md` | `1b20b662f8bc33e04d1f355179e9022839b013a5351a1bc19607f4726d491db7` |
| `references/release-status.md` | `a03e141e0f457d6d479e1fbbcea06791e9a0c1e42963effc742e556e5f255383` |
| `references/knowledge-base-manifest.json` | `c7efadcddfb5dbf427ae16851b490728b5a2a932140923b99e705688cbc9f101` |
| `scripts/skill_builder.py` (targeted reading only) | `71f7dc8ae9a67b3d0b19f5fdaaafe99441468653efab12147f54a4c24fcba31c` |
