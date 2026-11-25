# Skill Builder: knowledge fidelity, implementation, and release review

Review date: **November 24, 2026, America/Los_Angeles**  
Subject version: **1.0.0-rc.2**  
Reviewed commit: **`6b80b706d891baed8dde3b8323e383f0072390b9`**  
Reviewed Git tree: **`e9d95cb78a63da1cbf949ed4d4b91ac295136ec6`**  
Review branch: **`codex/skill-builder-comprehensive-review`**

## 1. Verdict

**The implementation substantially follows the knowledge base and preserves its complete contents. Improvements are required before public release. The current checkout's release verdict is BLOCKED.**

The architecture is appropriate for the stated goal: a Codex-first portable parent skill, named creation and audit modes, a question-answering route, explicit host adapters, and small deterministic supporting tools. The original knowledge is available in full. All 99 canonical rules have procedure owners, and their authority classifications and strengths have been retained.

The current source does not justify claiming that every guideline has been successfully exercised. There are two immediate release defects, three additional implementation or maintenance defects, and outstanding behavioral evidence. In particular, the latest license attribution edit breaks the required project check and package builder, and Git omits evidence files that a GitHub checkout needs. Native create/audit/Q&A behavior has not been demonstrated on the advertised agent hosts.

| Area | Assessment |
| --- | --- |
| Complete knowledge preservation | **Passed:** all 182 substantive external KB files match the bundled content byte for byte. |
| Canonical rule fidelity | **Substantially implemented procedurally:** 99 routes, no basis/strength drift; conflicting license instructions require correction. |
| Required creation/audit subcommands | **Implemented:** parent-skill modes and actual CLI subcommands; no unsupported claim of separately registered native slash commands. |
| Question-answering capability | **Implemented procedurally:** source retrieval, source attribution, freshness checks, and topic routing; license advice contains a conflict. |
| Deterministic helper quality | Strong contracts and meaningful adverse-path tests; one reproduced cleanup preservation defect. Current optional validation dependencies are unavailable. |
| Current validation/package preparation | **Failed:** source/runtime license disagreement prevents completion. |
| GitHub source completeness | **Failed:** 23 promised evidence logs are missing from Git. |
| Native Codex, Claude Code, Grok Build behavior | **Not run:** documentation describes this limitation accurately. |
| Demonstrated improvement over a clean no-skill baseline | **Not run:** no supported reliability, speed, token, or cost improvement claim. |

The recommended work is a focused correction and evidence pass. The underlying design and frozen knowledge archive should be preserved.

## 2. Scope, method, and evidence limits

The review compared these supplied locations:

- Knowledge base: `/Users/routerhealthchecker/Dropbox/SoftwareDevelopment/AI-Plugins/skill-building-knowledge/agent-skill-project-knowledge-base_final`.
- Skill source: `/Users/routerhealthchecker/Dropbox/SoftwareDevelopment/AI-Plugins/skill-builder`.

Three parallel reviewers covered rule/procedure fidelity, helper behavior, and portability/licensing/release evidence. The integrating reviewer checked preservation independently, inspected operational code and tests, reproduced current validation failures, and consolidated the findings. Multiple reviewers add distinct coverage; agreement is not a correctness certificate.

The source was clean at the reviewed commit. Before adding these report files, the subject contained **151 tracked files plus 23 ignored local evidence logs: 174 files and 15,475,649 bytes**. All received identity indexing. The conservative depth ledger records **37 full semantic reads, 134 structural/index-only files, and 3 binary identity reviews**. Some historical evidence received additional targeted inspection; its ledger classification remains structural rather than inflating semantic totals. The complete path/hash/depth denominator is in [source-inventory.json](2026-11-24-skill-builder-review-evidence/source-inventory.json).

Full semantic review focused on the runtime entrypoint, all three mode procedures, governance and coverage contracts, CLI contract/schema/helper, implementation map, four host adapters, OpenAI metadata, core repository navigation/licensing/security/task documents, release/check tools, both test modules, evaluation plan/cases, and current validation indexes. Rule review covered all 99 canonical statements and verification descriptions, handbook chapters 00–12, and the core playbook/profile/checklist/template material.

The 77 MB historical KB catalogs and receipts were checked for complete preservation and used as supporting/navigation evidence. Their thousands of historical source records were not manually re-audited one by one. The benchmark's 5,375 files and 25,693 instruction blocks are the KB's historical subject, not this review's semantic denominator. No new claim is made about every line of that benchmark or every original third-party passage's rights.

Execution chains were inspected before project code ran. Checks used local Python and inert temporary fixtures. No dependencies were installed, no target setup/hooks were run, and no installation, push, publication, account change, or deployment occurred. The cleanup probe and test suites created temporary owned files; testing was therefore not literally write-free. Production source and the frozen archive were left unchanged. The final repository changes are review documents and supporting observations only.

Fresh command records and exact captured output are in [fresh-check-results.json](2026-11-24-skill-builder-review-evidence/fresh-check-results.json). These review companions are explicitly separate from the KB's canonical version-2 evidence records. Optional schema validation could not be completed in the available environment.

## 3. Knowledge-base preservation and quality

### 3.1 Complete preservation is established

The preservation comparison found:

| Property | Fresh observation |
| --- | ---: |
| Bundled ZIP bytes | 11,572,664 |
| ZIP entries, including preserved metadata | 454 |
| Substantive indexed files | 182 |
| Substantive uncompressed bytes | 76,965,199 |
| Missing or additional substantive external-directory files | 0 |
| External-directory content hash mismatches | 0 |
| Canonical rules | 99 |
| Unique implementation-map rule IDs | 99 |
| Rule basis/strength mismatches | 0 |

The ZIP SHA-256 remains:

```text
9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204
```

The supplied extracted knowledge base and indexed archive members match exactly. This establishes preservation of the supplied content; it does not independently authenticate an earlier uploader. See [preservation-and-git-inventory.json](2026-11-24-skill-builder-review-evidence/preservation-and-git-inventory.json) and [the fresh KB verification output](2026-11-24-skill-builder-review-evidence/kb-verify.stdout.txt).

Keeping the full corpus archived is sensible. It contains example and identity-probe `SKILL.md` entrypoints that could otherwise become discoverable installed skills. The helper exposes exact reading/search/extraction without activating those fixtures. Its routing documents repeatedly require complete relevant source reads and treat search previews as locators. The shorter operational procedures supplement the unabridged corpus. They do not replace it with condensed source material.

### 3.2 The knowledge base is a strong engineering foundation

Its strongest properties are the separation of task, execution, evidence, distribution, and maintenance contracts; explicit instruction ownership; proportionate profiles; independent acceptance checks; preservation of failed/unrun results; and clear host-adapter boundaries. It also covers concerns often missed in introductory skill guides: actual loaded identity, permission lifetime, compaction/re-invocation, namespace collisions, process descendants, separate output/capture/retention budgets, every lifecycle writer, and missing versus malformed configuration.

The catalog correctly distinguishes **5 specification-based rules from 94 project-policy rules**, with **43 required, 34 conditional, and 22 recommended** strengths. A locally required control remains local policy when its basis is `project`. This is a suitable foundation for consistent development. The 99-rule catalog should not be advertised as a universal industry standard or automatic certification.

The KB's own limits remain material: host documentation is dated, research findings are frequently static, and native-host/no-skill comparisons were not performed for the source research. Its frozen standalone record checker also retains numeric/dispatch limitations described by the wrapper. The current wrapper adds guards around those paths rather than editing historical code. That is consistent with preservation.

Any future source correction should be a new versioned archive with provenance, retained history, changed-rule review, and affected checks. Supplemental current licensing and host evidence belong outside the frozen archive. The defects below do not justify rewriting it.

## 4. Implementation against the requested workflows

### 4.1 Creation

[The creation procedure](../../skills/skill-builder/commands/skill-builder-create.md) covers task examples and exclusions; independent acceptance; profiles and real effects; all-rule dispositions; architecture and threat decisions; portable instructions; deterministic resources; host-specific semantics; evaluation; packaging; maintenance; and release/recovery decisions.

The helper's `skill-builder-create` command creates an intentionally incomplete draft, task brief, exact original templates, source identity, and all-99 evidence worksheets. It does not invent domain behavior or passing evidence. The procedure explicitly tells the agent to continue to a completed task-specific skill. This division is appropriate for an agent skill: deterministic mechanics belong in code, and domain judgment belongs in the agent workflow.

Consequently, running the CLI alone does not satisfy the promise to create a finished skill. The README and command contract state this clearly. A native task trial must still establish that the activated agent reliably continues beyond scaffolding and produces the promised artifacts.

### 4.2 Audit

[The audit procedure](../../skills/skill-builder/commands/skill-builder-audit.md) is substantial. It requires snapshot identity, all-file coverage, instruction/dependency owners, semantic reading depth, sensitive execution traces, allowed/denied paths, test quality, lifecycle writers, current external claims, all-rule decisions, prioritized findings, and explicit limitations.

The CLI performs bounded intake and structural checks. Its inventory records exclusions, unenumerated content, symlinks, byte budgets, changing content, unknown Git coverage, and the absence of semantic/native assessment. Target scripts, hooks, and configuration are treated as data. A zero helper exit does not become a clean semantic audit.

This satisfies the intended audit architecture. F-03 identifies a current instruction contradiction, and F-04 identifies a helper recovery mismatch. Broader audit quality still needs native task evidence.

### 4.3 Questions and best-practice advice

[The explanation procedure](../../skills/skill-builder/commands/skill-builder-explain.md) is a real third route. It resolves the question, retrieves complete relevant sources, separates standards/product documentation/research/recommendations, checks changing claims, cites KB paths/rule IDs, and avoids unrequested scaffolding. Its topic table spans the handbook and detailed evidence.

This fits the requested use as a reference assistant. Correct the stale licensing instruction in F-03 and evaluate both narrow questions and broad design advice. Source availability alone does not establish answer accuracy.

### 4.4 All-99 coverage

| Rule family | Count | Procedural assessment |
| --- | ---: | --- |
| Portable format, FMT | 10 | Delivered-byte validation, metadata/types, paths, conservative-policy distinction, and validator limitations are addressed. |
| Instruction engineering, INS | 12 | Inputs, authority, examples, conflicts, continuation, and verification are addressed; INS-008 has the F-03 conflict. |
| Architecture, ARC | 8 | Portable core, resources, adapters, generation ownership, worker handoff, and shared-state boundaries are addressed. |
| Hosts, HOST | 7 | Independent support axes and temporal/collision identity tests are addressed; native evidence is unrun. |
| Commands/resources, CMD | 10 | Contracts, statuses, data transfer, budgets, identity, and recovery are addressed; F-04 affects the actual cleanup promise. |
| Security/privacy, SEC | 12 | Authority, trust, data flows, controls, actual enforcement, dependencies, and adverse cases are addressed. |
| Evaluation, EVAL | 14 | Independent acceptance, baselines, attempts, evidence identity, negative results, and schema records are addressed; current execution limits remain visible. |
| Performance, PERF | 6 | Whole-task context/latency/cost, concurrency, caching, and budget distinctions are addressed; comparative measurements are unrun. |
| Lifecycle, LIFE | 12 | Installation/ownership, staged changes, migrations, rollback, removal, and separate publication effects are addressed conditionally. |
| Open source/maintenance, OSS | 8 | README, contribution, CI, reporting, licensing, and maintenance are addressed; F-01/F-02/F-03 show implementation drift. |

[The complete 99-row procedural review](2026-11-24-skill-builder-review-evidence/all-99-procedural-fidelity.md) and [machine-readable companion](2026-11-24-skill-builder-review-evidence/all-99-procedural-fidelity.json) retain each rule, its classification, owners, canonical statement/verification, and reviewer note. That subreview classified 97 as procedurally covered and two as conflicting due to the same license instruction issue. **Those numbers are not compliance scores or passing tests.** Cross-cutting helper, release, evidence, and host findings in this report apply in addition to that procedural-only classification.

## 5. Findings requiring correction

### F-01 — License-copy drift blocks the project check and package builder

**Priority: P1. Confidence: high. Evidence: current bytes, Git history, and reproduced command failures.**

Locations: [root LICENSE.md](../../LICENSE.md), line 3; [runtime LICENSE.md](../../skills/skill-builder/LICENSE.md), line 3; [license-decision.json](../../skills/skill-builder/references/license-decision.json), line 6; [build_release.py](../../tools/build_release.py), lines 127–155; [release tests](../../tests/test_release.py), lines 270–290.

The latest commit changed the root copyright to `Alex Allen`; the runtime grant still uses `Alex`. The decision record and builder also hard-code the shorter attribution. The builder intentionally requires identical source/runtime grants and rejects the current state:

```text
python3 -I -B tools/check_project.py
# exit 2: Source/runtime license declarations disagree

python3 -I -B tools/build_release.py --identity
# exit 2: Source/runtime license declarations disagree
```

An actual archive-preparation attempt failed for the same reason and produced no completed release. The root `PACKAGE-MANIFEST.json` also records the previous root-license hash. Of its 173 payload entries, that is the only current byte mismatch before adding this review.

| File state | SHA-256 |
| --- | --- |
| Current root license | `d0c54e4f8ca3b2d45d0c1a575a5298bafd229e4ebb0ed37406f731609e9b35b5` |
| Runtime license / previously recorded root bytes | `3d088fe8079c8c8b6487e232429fb374abc47ccc4ea7e38de8ed8b89493aa959` |

**Impact:** required checks and release preparation cannot complete. Earlier rc.2 passes do not establish the current repository state. The MIT selection itself is already recorded; this is a consistency and evidence-freshness defect.

**Recommended correction:** propagate the intended full attribution through both grants, the current decision record, validation expectations/tests, and any dependent wording. Prefer one clear owner for attribution data. Rebuild current manifests using the release builder after validation; retain older receipts as historical evidence. Preserve the KB ZIP unchanged.

**Completion evidence:** project checks with required validators pass; affected release tests pass; two supported local builds have matching package identities; both archives contain the intended grants and component coverage. Relevant rules include INS-008, EVAL-011, LIFE-009, and OSS-005. See [fresh check records](2026-11-24-skill-builder-review-evidence/fresh-check-results.json).

### F-02 — Git omits 23 evidence logs promised by the source package

**Priority: P1 for GitHub release readiness. Confidence: high. Evidence: filesystem/manifest/Git comparison and isolated checkout reproduction.**

Locations: [validation/README.md](../../validation/README.md), lines 9, 13, and 52; [validation/rc2/README.md](../../validation/rc2/README.md), lines 30 and 47; the independent review's `probe-run.log` reference; root `PACKAGE-MANIFEST.json`; [.gitignore](../../.gitignore).

All **23** local `.log` files are present in the existing source manifest, and **zero** are tracked by Git. The current 65-test raw log, the preserved-validator 73-test raw log, and historical failures are among the omitted files. The actual cause is the user's global Git ignore:

```text
git check-ignore -v validation/rc2/local-tests.log
# /Users/routerhealthchecker/.config/git/ignore:43:*.log
```

The full omitted-path list and hashes are recorded in [the inventory](2026-11-24-skill-builder-review-evidence/preservation-and-git-inventory.json). A reviewer exported only tracked files into a disposable tree and synchronized its root license with its runtime license solely to isolate this issue. The standard-library project check then exited **1**, with `local_document_links` as its sole failed check and six broken evidence links. That diagnostic edit occurred only in the disposable copy; it is not a fix or a passing result for this checkout.

**Impact:** a GitHub clone loses promised raw evidence, differs from the intended source payload, and fails the prepared CI project check after F-01 is corrected. Local untracked logs can hide the problem during filesystem-based builds.

**Recommended correction:** review the existing logs for appropriate disclosure and deliberately track the required exact evidence. Add scoped project unignore rules if useful, and ensure staging actually includes them despite global ignore settings. Verify a clean Git-tree export or clone against the declared release inventory. Preserve historical failures; removing evidence or its required links would hide the issue.

**Completion evidence:** every intended evidence path is in Git, hashes match preserved records, a clean checkout has no missing local references, and package construction from that checkout includes the same declared inputs. Relevant rules include EVAL-011/EVAL-014, LIFE-009, and OSS-001/OSS-007.

### F-03 — Audit and explanation can incorrectly report MIT selection as unresolved

**Priority: P2. Confidence: high for the source conflict. Evidence: static authoritative instruction comparison; native behavior not reproduced.**

Locations: [audit procedure](../../skills/skill-builder/commands/skill-builder-audit.md), line 120; [explanation procedure](../../skills/skill-builder/commands/skill-builder-explain.md), line 62. Compare [governance](../../skills/skill-builder/references/governance.md), line 198; [creation procedure](../../skills/skill-builder/commands/skill-builder-create.md), line 131; runtime license, lines 25–49; current license decision, lines 4–23.

The audit route foregrounds the frozen KB's unresolved original-material grant when directing publication blockers. The explanation route explicitly instructs the agent to describe this bundle's original-material choice as unresolved. Current governance and creation instructions recognize the subsequent MIT selection and correctly classify the archived pending status as historical.

**Impact:** the skill can give contradictory advice across modes or ask the owner to resolve a choice already made. The stale passage also undermines the user's intended MIT publication workflow. This is separate from the actual attribution mismatch in F-01.

**Recommended correction:** make audit and explanation consume the current outer license decision and retain the historical KB status in its proper context. Keep third-party exceptions and genuinely outstanding publication gates explicit. Add paired audit/Q&A cases for both an actually unselected new project's license and this already-selected bundle.

**Completion evidence:** the current-selection case reports MIT coverage plus retained third-party terms without falsely reopening the choice; the unselected case remains blocked appropriately. Include an independent source-backed check and a native task case. Relevant rules: INS-008 and OSS-005.

### F-04 — Failure cleanup can delete an in-place edit to generated output

**Priority: P2. Confidence: high. Evidence: reproduced inert failure-path probe.**

Locations: [helper](../../skills/skill-builder/scripts/skill_builder.py), lines 243–245 and 271–279; [CLI contract](../../skills/skill-builder/references/cli.md), line 187; [existing cleanup test](../../tests/test_skill_builder.py), lines 529–537.

`NewTree` remembers device/inode ownership and deletes owned files after a caught failure when those identifiers match. Its public contract also promises to retain concurrently changed files. An external in-place content edit normally preserves the inode, so the implementation does not meet that broader promise.

The probe created `owned.txt` using `NewTree.write`, modified its bytes in place, and raised a later exception. The recorded outcome was:

```json
{"same_device_inode": true, "modified_file_survived": false, "output_root_survived": false}
```

See [cleanup-probe.json](2026-11-24-skill-builder-review-evidence/cleanup-probe.json). The existing test protects a separate unrelated file; it does not cover an in-place modification of an owned file.

**Impact:** cleanup can discard work made to newly generated output while a later operation fails. This is a bounded preservation defect. It is not evidence of a general adversarial-filesystem sandbox escape; the documented point-in-time/concurrency limitations remain appropriate.

**Recommended correction:** retain a trustworthy post-write content/metadata identity and preserve files that have changed before cleanup, with explicit residual race limits. Alternatively, narrow the stated guarantee to exactly what is implemented and require coordination that prevents other writers during generation. Preserving modified bytes best matches the project's current contract.

**Completion evidence:** a new regression preserves an in-place edit during failure while still cleaning unchanged owned material and retaining unrelated/replaced material. Relevant rules: CMD-001, CMD-004, and CMD-008.

### F-05 — Release-test fixtures fail on macOS's default temporary-path aliases

**Priority: P2 for developer portability. Confidence: high. Evidence: default and controlled-environment runs.**

Locations: [release tests](../../tests/test_release.py), including lines 214–218, 228–239, 253–261, and 270–273; [builder path check](../../tools/build_release.py), lines 46–59.

The production builder deliberately rejects symlink ancestors. Release tests create unresolved `TemporaryDirectory` paths. In this macOS environment, default temporary paths begin under `/var/folders`, while `/var` is a symlink. Those fixtures encounter the symlink refusal before reaching the behavior they intend to test.

The default standard-library release run reported **19 methods, 10 failures and 5 errors**. Counts include failing subtests and should not be treated as distinct product defects. Repeating the same suite with a canonical, nonsymlink `TMPDIR` removed the path-related failures: **19 methods, 0 failures and 4 errors**, all four remaining errors from F-01.

**Impact:** the documented test command fails for avoidable fixture reasons on this workstation, obscuring actual regressions. Existing Linux evidence and untested OS disclosures should remain correctly scoped.

**Recommended correction:** canonicalize ordinary temporary fixture roots or choose an explicitly nonsymlink test root. Continue constructing deliberate symlinks in the tests that exercise rejection. Keep the production path checks intact. Add a macOS development/CI panel if macOS validation is an intended claim.

**Completion evidence:** the documented release-test command reaches and passes its intended assertions with the default macOS temporary configuration after F-01 is fixed, while explicit alias rejection tests remain meaningful. Relevant rules include EVAL-004/EVAL-010 and HOST-007.

## 6. Fresh validation results

The main interpreter was **Python 3.15.2 on macOS arm64**. Existing Python 3.10 and 3.12 interpreters also lacked the optional modules; the runtime reviewer checked additional installed interpreters with the same result. No environment was provisioned or modified to install them.

| Check | Fresh result | Interpretation |
| --- | --- | --- |
| External KB versus bundled manifest/member hashes | 182/182 match | Complete preservation of supplied substantive content. |
| `python3 -I -B …/skill_builder.py kb verify` | Exit 0, preservation passed | Archive identity and all indexed member identities. |
| `python3 -I -B tools/check_project.py` | Exit 2 | F-01 stops the check before later gates. |
| Project check with `--require-validators` | Exit 2 | Same earlier license defect; no completed full-validation result. |
| Full `unittest discover -s tests -v` | Exit 1; 65 methods; 18 failures, 8 errors | Mixed missing dependencies, F-01, and macOS fixture failures; counts include subtest failures. |
| Helper-only suite | 46 methods; 35 passed, 8 failures, 3 errors | All failing/error cases depend on unavailable PyYAML/jsonschema/referencing in this environment. |
| Standard-library release suite, default temp environment | Exit 1; 19 methods; 10 failures, 5 errors | F-01 plus F-05. |
| Same release suite, canonical nonsymlink `TMPDIR` | Exit 1; 19 methods; 0 failures, 4 errors | 15 passed; remaining four errors reproduce F-01. This diagnostic repeat is not a replacement for the default failure. |
| Builder `--identity` and archive-preparation attempt | Both exit 2 | F-01; no deliverable release archives generated. |
| Current rc.2 receipt schema check | Exit 2, blocked | Preservation passed; schema dependencies unavailable. |
| Cleanup modification probe | Modified output deleted | F-04 reproduced. |
| Clean tracked-tree project check after isolated license synchronization | Exit 1, six missing log links | F-02 isolated; temporary diagnostic copy only. |

The README explicitly says that the full helper suite requires the optional dependencies and deliberately fails if they are unavailable. Those dependency failures are **environmental blockers**, not eleven newly established implementation defects. Full format/schema validation remains unavailable here. The optional dependencies must be provisioned through an authorized reviewed setup before rerunning the full suite.

The recorded earlier rc.2 Linux run of 65 passing methods and preserved-validator run of 73 passing methods remain useful historical evidence. They do not supersede current failures, establish macOS behavior, or supply native host trials. This review did not rerun the frozen 73-test validator panel or remote GitHub Actions.

Raw current outputs, command arguments, exit statuses, durations, environment changes, and hashes are retained alongside this report. Repeated subsets are not added to the unique test denominator. Unknown model usage, costs, and statistical reliability remain unknown.

## 7. Portability, licensing, and publication readiness

### 7.1 Host design and current documentation

The portable directory/frontmatter design agrees with the [Agent Skills specification](https://agentskills.io/specification). The sampled host claims were checked against [OpenAI's skills guide](https://learn.chatgpt.com/docs/build-skills), [Claude Code's skills documentation](https://code.claude.com/docs/en/skills), and [Grok Build's skills documentation](https://docs.x.ai/build/features/skills-plugins-marketplaces) during this review. No concrete discrepancy surfaced in the sampled discovery, invocation, tool-grant lifetime, resource-root, or frontmatter-semantics claims.

The adapters correctly distinguish Codex metadata from Claude frontmatter, Claude tool preapproval from a security restriction, Grok's differing interpretation of shared fields, and Grok Build from Grok Bot/custom API hosts. The named modes share one parent entrypoint. Separate native `/skill-builder-create` registration is not promised.

These are documentation observations. The separate axes for format, discovery, functional outcomes, safety/continuation, and maintained support in [compatibility.md](../../docs/compatibility.md) are appropriate. A current source URL is not an immutable documentation revision; retain bounded dated evidence when updating important host claims.

### 7.2 Native evidence remains the largest uncompleted behavioral step

The original KB retains **22 evaluation designs**; the repository adds **19 candidate-specific designs**. Their `not_run` status is honest. Three earlier development trials provide bounded feedback, with development-snapshot identity and grading limits recorded. They do not establish native discovery, final-candidate end-to-end quality, or a clean comparative benefit.

Run the exact packaged candidate on **Codex first**, then Claude Code and Grok Build to the intended advertised tiers. The minimum panel should cover explicit invocation; positive/paraphrase/negative/opt-out requests; completed creation; defect detection and target preservation during audit; source-accurate Q&A; a different working directory including spaces; unavailable capabilities; permitted and denied actions; interruption and continuation; re-invocation/source changes; same-name collisions; actual selected artifact identity; output verification; and cleanup.

Use independent expected artifacts/checkers, frozen fixtures, reset conditions, budgets, and retry/exclusion rules. Record every attempt. For benefit claims, add clean no-skill and relevant previous-version conditions without inherited candidate instructions. Native trials are required for stronger host/task claims, even after all local checks pass.

### 7.3 MIT scope and remaining publication work

The current outer declaration selects MIT for original builder material and original material in the precisely identified KB snapshot. It retains third-party exceptions, provenance, Apache/MIT texts, and source attribution. That treatment is appropriate as an engineering packaging contract. This review did not adjudicate ownership of every retained external passage. F-01 and F-03 concern consistency in applying the existing decision.

[SECURITY.md](../../SECURITY.md), line 3, still leaves the actual private reporting route unconfigured. The project itself requires this before public release. Configure a real channel and publish the intended supported-version/response process without inventing a commitment. Choose honest host support tiers and retain unrun rows.

CI uses read-only permissions, immutable checkout references, separate standard-library/optional-validator jobs, and no privileged publication path. These are good choices. Remote execution remains unrun, and a clean GitHub checkout currently has F-02. Exact dependency versions are pinned; artifact hashes are not locked, as the README discloses. Hash locking is a useful further supply-chain improvement when preparing the validation environment.

## 8. Prioritized improvement plan

| Order | Work and owner | Completion evidence | Relative effort |
| --- | --- | --- | --- |
| 1 | Maintainer/release tooling: fix F-01 attribution consistency; append fresh evidence and regenerate manifests. | Current required checks and affected release tests pass; matching source/runtime grants and deterministic package identities. | Small scoped change. |
| 2 | Maintainer/repository packaging: fix F-02 tracked evidence inventory. | Required logs retained in Git; clean checkout passes links and contains declared release inputs. | Small change plus careful evidence review. |
| 3 | Runtime instruction owner: fix F-03 in audit/explanation. | Current-selection and truly-unselected licensing cases produce correct distinct advice. | Small edit plus semantic cases. |
| 4 | Helper owner: fix F-04 at the cleanup contract. | In-place edit survives failure; unchanged owned cleanup and unrelated/replaced preservation still work. | Moderate, focused recovery change. |
| 5 | Test owner: fix F-05 ordinary temporary fixtures. | Default macOS suite reaches intended gates; deliberate alias tests remain effective. | Small fixture change. |
| 6 | Validation owner: provision reviewed pinned optional dependencies, then rerun the full local panel on the changed identity. | Nonempty tests, required format/schema checks, exact input identities, retained failures/limitations. | Environment-dependent. |
| 7 | Host/evaluation owner: exercise the final candidate on native Codex; add secondary-host panels to the promised tier. | Artifact-bound discovery/create/audit/Q&A/denied-path/continuation receipts. | Largest evidence task. |
| 8 | Maintainer: configure private reporting and final release/support policy; run clean remote CI and reproducible packaging. | Actual configured route, passing clean-checkout CI, inspected notices/host limits, final detached hashes. | Small setup plus validation. |

Useful subsequent improvements are measured context loading and more executable semantic regressions. The audit route's named initial KB sources plus entrypoint/audit/governance/coverage/CLI documents total about **275,098 bytes** before target content or effect-specific branches, by a source-byte calculation. This is not a token count or demonstrated performance defect. Measure actual activated context, truncation/continuation behavior, and end-to-end task outcomes on the primary host. Preserve all source knowledge while using reliable navigation, staged full-file reads, and durable checkpoints.

Add regression cases for contradictions across authoritative consumers and for clean Git-tree/source-package agreement. These two boundaries escaped the existing strong local helper tests. Such checks offer more value than increasing counts with tests that repeat implementation text.

## 9. Review deliverables and remaining uncertainty

The report is accompanied by the all-99 procedural comparison, machine-readable findings, a pre-report source identity/depth inventory, preservation/Git inventory, fresh command observations and raw outputs, and the cleanup probe. [evidence-index.json](2026-11-24-skill-builder-review-evidence/evidence-index.json) identifies the supporting files and hashes without a self-hash cycle.

The assessment is complete within its stated source/semantic/execution coverage. The skill's public-release readiness remains blocked by F-01 and F-02. F-03 through F-05 need correction or an explicitly justified, accurately scoped disposition. Required-validator execution, native host outcomes, maintained support, clean comparative benefit, remote CI, and the public reporting channel remain separate outstanding evidence or release decisions.

No runtime repair, license change, archive rewrite, dependency installation, commit, push, or publication was performed as part of this review.
