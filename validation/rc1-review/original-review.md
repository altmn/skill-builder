# Skill Builder 1.0.0-rc.1: independent implementation review

**Prepared for Alex | November 23, 2026 | Review of the supplied knowledge base and source release**

## 1. Overall assessment

**Skill Builder substantially implements the intended design. It preserves the knowledge base in full, supplies substantive procedures for every one of its 99 rules, implements both requested subcommands, and provides a separate best-practice question-answering workflow. It needs several concrete corrections before a stable public release. The current artifact also does not contain the MIT license grant you have selected.**

This is a strong foundation that should be improved through focused changes. There is no evidence that the knowledge base must be rebuilt or that the skill needs a new architecture. The most serious executable defect is in release packaging: a symlink used as a selected source-directory root can cause files outside the project to enter a release archive. Four further reproducible defects affect numeric validation, metadata serialization, repeated packaging, and batch error handling.

The favorable preservation result and the defects are compatible. Every original byte can be retained while a helper still mishandles an input. Similarly, a procedure can accurately describe a requirement without proving that an agent or host performs it on every task. This report keeps those questions separate.

| Question | Assessment |
| --- | --- |
| Is the complete attached knowledge base preserved? | Yes. The embedded ZIP is byte-identical, and every substantive member matches its recorded identity. |
| Are all 99 requirements operationally represented? | Yes, at the instruction/procedure level. No substantive procedural omission was identified in the reviewed scope. |
| Are create and audit implemented? | Yes: parent-skill modes and real Python CLI subcommands, with clear division between helper preparation and completed agent work. |
| Can users ask best-practice questions? | Yes. A dedicated explanation workflow and a fresh question task support that conclusion. |
| Do the supplied regression suites pass? | Yes: 47 source tests and 73 preserved-validator tests passed in fresh local runs. Additional tests exposed gaps outside those panels. |
| Are the supplied release bytes reproducible? | Yes. Rebuilding unchanged source reproduced the exact source ZIP and recorded runtime ZIP hashes. |
| Is the artifact currently MIT licensed as requested? | No. Its license files explicitly say selection is pending. |
| Is native Codex, Claude Code, or Grok Build operation verified? | No. The project correctly labels those panels unrun. This review's manually supplied task exercises do not establish native discovery. |
| Is it ready for the intended release? | Not unchanged. Correct the confirmed defects and MIT status, configure reporting, and complete the host evidence needed for the support claims you intend to make. |

The distinction between an experimental release and a tested stable release matters. Missing comparative benefit measurements do not prevent an accurately described experimental release. Missing native-host evidence does prevent claiming that native behavior has been verified. The current missing MIT grant prevents describing this artifact as the selected MIT-licensed release. [S: README.md, line 5; S: LICENSE.md, line 3; S: validation/README.md, line 7; E: preservation, baseline checks, and package identities.]

## 2. Scope, method, and evidence limits

### 2.1 Inputs and identities

The review used only the attached source material, disposable local copies, synthetic test inputs, and current primary documentation for host/specification/licensing claims. The original attachments and extracted review source were not edited, installed, or published.

| Input | Bytes | SHA-256 |
| --- | ---: | --- |
| Attached knowledge-base ZIP | 11,572,664 | `9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204` |
| Attached Skill Builder source ZIP | 12,685,526 | `624d313a45a15749c75a5251b53c40408808ba1ee3c7149e2d4697635bd06588` |
| Supplied detached-checksum text | 102 | `7166dc443764c65c4bb91e8a3903151e85822ba1ac3ab01b319866edab31696c` |

The source ZIP digest matches the value in the supplied checksum text. The `(1)` and `-copy` suffixes on the uploaded filenames do not affect that byte-identity result. The checksum establishes consistency with the supplied digest; it is not independent publisher authentication. [E: input identities and package reproduction.]

### 2.2 Work performed

Three independent reviewers divided the initial work into requirements/preservation, executable code/packaging, and workflows/portability/release readiness. The integrating reviewer read the principal source and test evidence, reconciled their findings, and independently reproduced the selected-root symlink, exponent-overflow, description-serialization, and malformed-record cases. A separate inspection confirmed that the second nested build contained the first build's archives and receipts. Fresh-context agents then exercised Q&A, audit, and creation without receiving the expected answers or defect list; another fresh agent used the generated skill on three independently chosen input sets.

The requirements pass read all 13 handbook chapters, every canonical rule and implementation-map entry, all three operational workflows, shared governance, profile guidance, creation/audit instructions, relevant templates, schema guidance, and all 22 original evaluation designs. It checked all 297 rule-owner references. The code pass reviewed the current helpers, package/check scripts, tests, public CLI contract, and the archived validators they invoke before executing them. The host/release pass checked entry-point behavior, adapters, evaluation records, licensing, notices, and maintenance material.

The complete knowledge archive received byte-level comparison. Its large historical file and instruction catalogs received structural verification and targeted semantic reading. This review did not repeat the original upstream project's entire source audit, manually reread every historical ledger row, or execute the historical project's setup, hooks, services, or authenticated flows. Preserving those records does not independently verify every historical assertion in them.

### 2.3 Terminology used in this report

| Term | Meaning |
| --- | --- |
| Preserved | Original bytes and identities match. |
| Procedure present | The skill contains substantive actions, applicability conditions, and evidence expectations for a requirement. |
| Reproduced defect | A local case produced the stated unwanted result using the reviewed code. |
| Evidence gap | A result needed for a stronger claim has not been established; this is not an observed failure. |
| Improvement | A useful change whose absence is not a demonstrated violation or failure. |
| Native host test | Actual loading/invocation on the named product and surface, with evidence of the loaded artifact when observable. |

Priorities are contextual. **P1/high** findings should be resolved before the intended public release. **P2/medium** defects should be corrected before a stable release because they violate an advertised contract or undermine repeatable operation. **P3/low** is a smaller robustness issue. No critical exploit, real-secret disclosure, or successful hostile-host compromise is asserted.

## 3. Knowledge preservation and requirements coverage

### 3.1 Preservation meets the full-content requirement

The design retains the exact original ZIP at `skills/skill-builder/references/knowledge-base.zip`. Independent comparison established:

- 454 original ZIP entries retained, including directories and packaging metadata.
- 182 substantive files, totaling 76,965,199 uncompressed bytes.
- Zero missing substantive paths, size mismatches, or SHA-256 mismatches.
- The same 99 canonical rules, unchanged authority/strength classifications, and matching JSON Pointers in the operational implementation map.
- 297 owner file/heading references checked, with no missing or ambiguous owner section.

The runtime exposes substantive files through verified read/search/extract operations. Excluding macOS sidecars from a working extraction does not remove them from the retained archive. Archived examples contain their own `SKILL.md` files; leaving the KB closed inside the installed skill is a sensible way to prevent those research fixtures from becoming accidentally discoverable skills. This storage choice meets the requested full preservation without loading the entire historical corpus into every prompt. [S: SKILL.md, line 33; S: references/knowledge-base-manifest.json; S: scripts/skill_builder.py, line 112; E: preservation-and-map checks.]

### 3.2 All rules are represented, but they are not 99 universal mandates

The catalog contains **five specification-based rules and 94 project-policy rules**. Separately, the strengths are **43 required, 34 conditional, and 22 recommended**. A locally required control does not become an industry specification because it is important to this project. Conversely, a conditional rule can become essential when the relevant effect exists. [K: catalogs/requirements.json; S: references/requirement-coverage.md, line 19.]

Applying the knowledge in full means considering all 99 IDs, keeping their original meaning, selecting applicability from actual capabilities and effects, and recording evidence and release consequences. It does not require adding an installer, daemon, browser, state database, or paid evaluation service to an instruction-only writing skill. Historical counterexamples should inform decisions; undesirable practices found in the benchmark should not be copied into new skills.

The skill handles this distinction well. It preserves canonical authority and strength, requires every rule to receive a disposition, distinguishes `adopted` from `passed`, requires reasons for exclusions, and says that a profile cannot waive real effects. The operational map has genuine procedures behind its links, rather than only 99 labels pointing at generic prose. [S: SKILL.md, line 66; S: references/requirement-coverage.md, line 31; S: references/governance.md, section g-authority.]

| Requirement family | Rules | Procedural coverage found |
| --- | ---: | --- |
| Format | 10 | Distributed metadata, resource boundaries, optional fields, packaging contents, checker scope. |
| Instructions | 12 | Task contracts, triggers, authority, questions, examples, ownership, failure and partial results. |
| Architecture | 8 | Proportionate design, mode/subskill boundaries, adapters, generation, handoffs, workers. |
| Host portability | 7 | Named products, capability records, invocation/permission differences, roots, shared cases. |
| Commands | 10 | Interfaces, result states, argument handling, writes, reviewed execution chains, recovery. |
| Security | 12 | Trust levels, controls, data flows, secrets, opt-outs, budgets, graders, CI boundaries. |
| Evaluation | 14 | Independent criteria, adverse cases, controls, attempts, identities, graders, zero-test handling. |
| Performance | 6 | Whole-task work, measurements, cold/warm conditions, caches, process justification. |
| Lifecycle | 12 | Scope, ownership, updates, migration, rollback, removal, release identity, publication. |
| Open-source maintenance | 8 | README, evidence, contributions, licenses, reporting, workflow pins, maintenance. |
| **Total** | **99** | **No substantive procedural omission identified.** |

The full rule-by-rule procedure review is in Appendix A and the evidence JSON. That result must not be read as 99 passing execution tests. For example, the filesystem-boundary procedure is present, while finding F-02 shows that one package-building implementation does not fully satisfy it.

### 3.3 Guidance beyond the numbered rules also survives

The review specifically checked details that can be lost in a simple rule checklist: separate lifetimes for loaded instructions, invocation permissions, and durable state; actual versus intended loaded artifact identity; duplicate skill names and namespaces; response-size versus live-capture limits; confirmation that timed-out readers stop; every lifecycle writer; malformed versus missing settings; preservation of local and untracked work; numeric source ranges versus search selectors; unknown measurements; and dated resolution events that do not rewrite old receipts.

These subjects remain in governance, workflow phases, explicit supplemental-contract routing, and mandatory original-source reading. The skill does not need to duplicate every original sentence in each workflow to preserve and apply its meaning. Its own operational layer is an addition to the complete source, not a replacement for it. [S: references/requirement-coverage.md, section Supplemental contracts; S: references/governance.md, sections g-host, g-command, g-lifecycle, g-evidence, and g-continuation.]

## 4. Workflow and architecture assessment

### 4.1 Creation

`skill-builder-create` has a real agent workflow covering context, task contract, architecture/profile, implementation, hosts, evaluation, packaging, delivery, recovery, and required output. It asks for meaningful examples and independent acceptance conditions, separates portable logic from adapters, and requires completing the domain skill after scaffolding.

The Python subcommand intentionally creates an incomplete project, evidence templates, and all-rule records. It explicitly returns `semantic_implementation: not_run` and `release_ready: false`. This is appropriate helper design. A review that calls the whole skill incomplete solely because the CLI produces a draft would overlook the agent procedure. The serialization defect in F-04 is separate: accepted input should still produce valid, faithful metadata in a draft. [S: commands/skill-builder-create.md; S: scripts/skill_builder.py, line 318.]

### 4.2 Audit

`skill-builder-audit` has a detailed source-review workflow rather than a promise that a structural checker is a complete audit. It requires identity, inventory, semantic instruction review, effects and failure paths, validation, claims, prioritized findings, optional scoped repairs, recovery, and explicit outputs.

The helper inventories and hashes regular files, records omitted content and coverage limits, avoids executing the target, checks recognized skill metadata/resources, and creates a separate assessment workspace. It does not invent a Git commit identity or a full semantic pass. The agent is instructed to continue. Those are strong design choices for reviewing untrusted repositories. [S: commands/skill-builder-audit.md; S: scripts/skill_builder.py, lines 351 and 463.]

### 4.3 Questions and explanations

`skill-builder-explain` is a dedicated route for focused questions. It selects complete relevant source, separates specification, documented behavior, observations, results, and recommendations, checks changing facts when material, and avoids unwanted scaffolding. Users do not need a separate `explain` CLI command: the agent owns the answer and the CLI supplies retrieval. The fresh Q&A task described in Section 8 confirmed this distinction for one representative question. [S: commands/skill-builder-explain.md; S: SKILL.md, line 16.]

### 4.4 Subcommand semantics are correctly represented

The requested names exist as modes of one skill and as Python CLI subcommands. The documented examples use `$skill-builder skill-builder-create` where Codex dollar invocation is available, and `/skill-builder skill-builder-audit` on a corresponding slash-command host. The project expressly says it does not register separate `/skill-builder-create` commands. That is not a missing requirement: the user asked for subcommands, and this design supplies them.

Separate discoverable skills could be added later for convenience if actual host usage warrants them. They would add discovery and maintenance surface, so they should not be introduced only to imitate command naming. Current official documentation supports the underlying parent-skill invocation patterns. [S: SKILL.md, line 18; S: README.md, line 29; W2, W3, W4.]

## 5. Confirmed defects and release mismatch

| ID | Priority | Finding | Result observed |
| --- | --- | --- | --- |
| F-01 | P1 / high | MIT selection is absent from the artifact | Source/runtime licenses and current release metadata still say selection pending. |
| F-02 | P1 / high | Selected-root symlink bypasses release containment | External synthetic file entered the source ZIP; project check and build exited 0. |
| F-03 | P2 / medium | Exponent overflow passes evidence validation | `elapsed.value: 1e999` became infinity and received a passing record result. |
| F-04 | P2 / medium | Some accepted descriptions yield invalid or changed YAML | U+007F failed YAML parsing; U+0085 changed to a space; creation exited 0. |
| F-05 | P2 / medium | Previous release outputs enter later source packages | Second nested build included the first build and grew from 12.69 MB to 37.37 MB. |
| F-06 | P3 / low | Wrong-type record dispatch aborts the batch | A list/dict `record_type` caused exit 2 and discarded per-record results. |

### 5.1 F-01: incorporate the already selected MIT license

**Evidence.** The repository `LICENSE.md` begins with a pending-selection heading and expressly states that no public license has been selected for new code, instructions, documentation, or original KB material. The installed runtime has a corresponding status file. README, NOTICE, compatibility, task brief, governance, workflow text, release status, manifests, and the builder repeat that state. The release builder also hardcodes `blocked_pending_rights_holder_license_selection` and a license blocker; editing a README alone would not update newly built artifacts. [S: LICENSE.md, line 3; S: skills/skill-builder/LICENSE.md, line 1; S: references/governance.md, section g-oss; S: tools/build_release.py, lines 92 and 175.]

**Why it matters.** Your present instruction selects MIT. The delivered artifact has not incorporated that choice. A GitHub project containing a pending-license status file does not provide the intended grant. This is an artifact/requirement mismatch; it is not evidence that the earlier builder was wrong to preserve an unresolved decision when preparing that snapshot. GitHub's guidance recommends an actual license file, and its MIT reference includes the grant, attribution, and notice requirements. [W5, W6.]

**Recommended change.** Put the full MIT license and intended copyright attribution in both source and runtime distributions for the original work you are licensing. Add a clear component-coverage declaration that identifies the original KB snapshot by hash and explains the relationship between the current grant and its historical pending-status text. Preserve all applicable third-party notices and terms. Keep the original ZIP byte-identical; its historic status can remain intact while the current outer declaration records the new decision.

Update the current status owner, builder fields, relevant workflow instructions, and public documentation to consult that declaration. Preserve old receipts as historical and append a new release decision. Do not leave a permanent instruction that every future generated project is blocked because this old KB snapshot originally lacked a license choice. Equally, a new MIT declaration should not claim to relicense underlying third-party material indiscriminately. This review does not adjudicate ownership of every source excerpt.

**Acceptance.** Both packages contain complete MIT terms and component coverage; current generated manifests/status accurately reflect the selection; third-party notices remain; the frozen KB hash is unchanged; package identities and affected evidence are regenerated. Add a case where the user has already selected a license. No renewed permission to select MIT is needed: you have already supplied that decision. No license edit was made during this review-only task. The fresh creation exercise did honor an explicit MIT choice for new original work, so this finding concerns the builder's own delivered license state and current release records, not an inability to create licensed skills.

### 5.2 F-02: reject symlinks at selected release-input roots

**Evidence and cause.** `walk_files(base)` uses `os.walk(base, followlinks=False)` and rejects symlinks among child directories. It does not reject a symlink supplied as `base`. `source_files()` calls it separately for selected roots such as `docs`. `regular_bytes()` checks the final file component, but not symlink ancestors or resolved containment within the project. [S: tools/build_release.py, lines 42, 60, and 138.]

**Reproduction.** In a disposable source copy, move `docs/` to a sibling directory outside the project, add a synthetic marker file, and replace `docs` with a symlink to that sibling. Run the required-validator project check and release build. Both returned 0. The source ZIP contained the external marker under `skill-builder-1.0.0-rc.1/docs/`. The integrating reviewer reproduced this independently with a different marker. [E: F-02 reviewer and integrating-reviewer reproductions.]

**Impact and boundary.** The release can include unrelated local files from outside its intended source tree. A filename denylist will not catch ordinary sensitive filenames. This test involved only synthetic content; no real secrets were read or disclosed. It requires no race, so the project's documented limitation against hostile concurrent replacement does not explain it. The supplied unchanged archive itself was not shown to contain such unintended files.

**Recommended change.** Before enumerating any selected root, check its actual type and all relevant ancestors. Require resolved containment in the intended project/skill root, retain descendant/leaf symlink checks, and fail explicitly for an unreadable or invalid required source tree. Apply the same policy to runtime identity generation, source collection, and the project check where appropriate. An intentional external dependency should need a separate explicit manifest/policy instead of entering through an unnoticed path alias.

**Acceptance.** A symlink at a selected source root, a symlinked runtime root/ancestor, and a descendant symlink are rejected before their contents are packaged. No external marker enters an archive. Normal unchanged input still produces the expected deterministic output. This is the first executable fix to prioritize. Relevant KB rules include SEC-004, FMT-009, and LIFE-009.

### 5.3 F-03: reject finite-syntax numbers that overflow the parser

**Evidence and cause.** The JSON parser rejects `NaN` and `Infinity` through `parse_constant`, but ordinary exponent notation is handled by the default float parser. `1e999` is syntactically a JSON number; converting it to a Python float yields infinity. A supplied valid evaluation receipt was changed only at top-level `elapsed.value` to that token. The wrapper returned exit 0, `outcome: passed`, and a passing record with zero errors. The preserved KB's standalone record checker accepted it too. The integrating reviewer independently reproduced the wrapper result. [S: scripts/skill_builder.py, lines 76 and 544; K: tools/validate_records.py, line 30; E: F-03.]

**Impact and boundary.** This violates the stated nonfinite-value rejection contract before any question about the truth of the measurement arises. An infinite elapsed-time, cost, or similar measurement can contaminate subsequent arithmetic or fail later serialization. The issue is not that JSON Schema should establish whether a measurement really happened; it is that the parser/schema pipeline accepts a nonfinite in-memory representation that the public contract promises to reject. [S: references/cli.md, line 177.]

**Recommended change.** Add a `parse_float` conversion that verifies finiteness, or a complete recursive finite-number check before validation. Define the supported numeric representation explicitly. Test positive and negative overflow, named nonfinite tokens, and a finite scientific-notation control. Preserve the original archive; place the immediate guard in current wrapper code and record the inherited validator limitation. A future KB revision can correct its canonical tool under a new source identity.

**Acceptance.** `1e999`, `-1e999`, `NaN`, `Infinity`, and `-Infinity` receive explicit record failures. A normal finite exponent remains accepted. Failure does not expose input contents, abort unrelated records, or produce a passing aggregate. Relevant KB rules include CMD-001, CMD-002, EVAL-004, EVAL-012, and EVAL-014.

### 5.4 F-04: make description serialization faithful for all accepted characters

**Evidence and cause.** Creation accepts a nonblank, NUL-free description up to 1,024 characters, then inserts `json.dumps(description, ensure_ascii=False)` into a YAML double-quoted field. Raw JSON and YAML character handling differ. A description containing U+007F was accepted with exit 0 but the generated YAML failed the project's own parser. U+0085 was accepted and parsed, but changed from a next-line character to a space. Both were independently reproduced. [S: scripts/skill_builder.py, lines 318 and 327; S: references/cli.md, line 49; E: F-04.]

| Input | Create result | YAML result |
| --- | --- | --- |
| `Before` + U+007F + `After` | `scaffold_created`, exit 0 | Rejected by PyYAML. |
| `Before` + U+0085 + `After` | `scaffold_created`, exit 0 | Parsed as `Before After`; input changed. |

**Impact and boundary.** A draft can be incomplete in its task content and still need structurally valid, accurate metadata. These unusual characters expose a real serialization gap; they do not show that ordinary non-ASCII descriptions are generally broken.

**Recommended change.** Use a YAML-safe scalar emitter or selectively escape characters that cannot safely appear raw, while preserving valid Unicode scalar values. A blanket switch to JSON's ASCII-only escaping is insufficient: non-BMP characters can become JSON surrogate pairs that a YAML reader does not recombine. If an ASCII-only YAML representation is needed, emit the appropriate YAML Unicode escape for the full code point. Reject invalid lone surrogates and any clearly documented unsupported input before writing; do not silently strip or normalize accepted input. Test code-point round trips for ordinary Unicode, quotes, line breaks, U+007F, U+0085, U+2028, U+2029, and non-BMP characters such as U+1F600 and U+20000.

**Acceptance.** Every accepted description produces parseable YAML with the original value; unsupported input fails before output creation with a stable reason. The draft's normal missing domain implementation remains correctly labeled. Relevant rules include FMT-001, FMT-004, FMT-006, and EVAL-012.

### 5.5 F-05: keep release output outside selected source inputs

**Evidence and cause.** The build accepts a new output directory under a selected source tree. Collection later includes that tree recursively. Its omit policy recognizes a directory literally named `dist`, but not arbitrary prior output locations. Documentation says the build directory is omitted, which is too broad for the actual implementation. [S: tools/build_release.py, lines 26, 60, 138, and 150; S: docs/architecture.md, line 13.]

In a disposable unchanged source copy, build once to `docs/build-1`, then again to `docs/build-2`. Both builds returned 0. The first source ZIP was **12,685,526 bytes**; the second was **37,369,648 bytes**. The latter contained the first runtime ZIP, source ZIP, checksums, and receipt. The integrating reviewer separately inspected these entries in the produced archive. [E: F-05.]

**Impact and boundary.** An otherwise reasonable output choice pollutes later package inputs and can cause repeated growth. This is distinct from deterministic ZIP construction: the tool has changed the input set through its own previous output. The documented example using a sibling output directory avoids the problem, and the supplied unchanged artifact rebuilt exactly.

**Recommended change.** Enforce output outside selected source trees, or support one explicit excluded build root and reject other nested locations. Document the enforced policy. Excluding only the current output is insufficient because older outputs remain eligible.

**Acceptance.** Nested output is rejected before writing, or is placed in an explicitly excluded root. Two supported builds reproduce identical source ZIPs with no prior release archive/receipt nested inside. Relevant rules include ARC-004, FMT-009, and LIFE-009.

### 5.6 F-06: preserve per-record results for malformed dispatch fields

**Evidence and cause.** A record such as `{"record_type": []}` reaches a dictionary-membership dispatch before its type is checked. That raises `TypeError`. The wrapper's per-record handler catches `BuilderError` and `OSError`, so its top-level handler returns `blocked`, exit 2, discarding already collected results and skipping later records. A valid/malformed/valid batch reproduced this behavior. [S: scripts/skill_builder.py, lines 561 and 676; K: tools/validate_records.py, line 98; E: F-06.]

**Impact.** This is a smaller API consistency issue. It does not produce a false pass, but callers receive a global capability-style blockage for an ordinary bad record, and other requested records are not reported. The archived standalone checker's main loop catches such record exceptions; the wrapper does not preserve that protection.

**Recommended change and acceptance.** Check that the dispatch field is a supported string before calling the validator, or convert expected record-validation exceptions into individual failures. Mixed batches should report every requested record in order and return exit 1 for invalid records. Reserve exit 2 for unavailable dependencies, integrity/environment problems, and invocation failures. Keep raw input values out of errors. Relevant rules include CMD-001, CMD-002, and EVAL-004.

## 6. Native-host evidence and release preparation

### 6.1 The host adapters are sound; native support remains unverified

Current primary documentation supports the main adapter distinctions reviewed here. Codex has its own discovery roots and explicit invocation; Claude Code has its own slash-command, argument, and permission behavior; Grok Build documents materially different effects for some similarly named fields. The project correctly keeps Grok Build, Grok Bot, and custom xAI/API hosts distinct. [S: references/hosts/; W2, W3, W4.]

Two examples justify this separation. Claude Code's `allowed-tools` is a preapproval mechanism with a particular lifetime, not a blanket tool-exclusion mechanism. Grok Build's documentation says its field does not grant or restrict tools. Claude's documentation also states that arguments are appended when no placeholder receives them, so absence of `$ARGUMENTS` in the shared core is not by itself an argument-loss bug. These are documentation checks, not observations of this release running on those hosts. [W3, W4.]

The source openly says native Codex, Claude Code, and Grok Build discovery/task panels are unrun. Its 18 candidate-specific evaluation designs remain designs; three earlier development tasks used development snapshots and did not establish native loaded identity or a clean no-skill comparison. Those statements are appropriately conservative. [S: docs/compatibility.md, line 19; S: evals/cases.json; S: validation/development-trials.json, line 5.]

Before advertising tested native support, freeze the corrected final package and run a small shared panel: explicit create/audit/Q&A, relevant implicit activation, a near miss and opt-out, resources from another directory with spaces, missing or denied capability, hostile audit data, interruption/continuation, and actual output/effect checks. Prioritize Codex as the default target, then extend the same applicable panel to Claude Code and Grok Build. Record version, surface, policy, package identity, actual activation identity where exposed, all attempts, and unavailable cases.

A comparison against a clean no-skill control is needed for claims of better quality, speed, or cost. It need not delay a release that makes no such claim. Likewise, format/documentation compatibility can be stated without pretending it is demonstrated native behavior. Relevant rules include HOST-002, HOST-006, HOST-007, and EVAL-001 through EVAL-007.

### 6.2 Configure a real reporting route

`SECURITY.md` explicitly says there is no published repository or private reporting endpoint. That is understandable before launch, but a public project needs an actual destination for sensitive findings and a support policy the maintainer can sustain. Configure the chosen repository's reporting mechanism and update the document with real information. No invented email address, GitHub URL, response-time promise, or indefinite support commitment is needed. Verify that a prospective reporter can find the route. [S: SECURITY.md, line 3; K: handbook/10-github-and-maintenance.md; OSS-006.]

### 6.3 Apply the evidence formats to this project itself

The create workflow requires per-target host-capability records, while Skill Builder principally supplies a prose compatibility matrix and adapters for its own host status. Add schema-valid own-project records that honestly retain untested/unrun states and unknown-version reasons. Validate them and their file references in the project check.

Also separate procedure coverage from operational results in the public self-assessment summary. Its 58 scoped passes are not fabricated host passes: the detailed records qualify them, and other entries remain inconclusive, unrun, excluded, or blocked. Nevertheless, a downstream reader can easily detach a pass count from its scope. A companion matrix should keep `procedure_present`, local resource result, native-host result, and supported release claim separate. Do not alter frozen schemas merely to add these fields. [S: validation/self-assessment-context.json; S: commands/skill-builder-create.md, line 98; S: references/governance.md, section g-evidence.]

## 7. Improvements that preserve the full knowledge

### 7.1 Measure the actual reading burden

A conservative inventory of the ordinary Codex creation route names **22 distinct wrapper/core/example files totaling 273,136 UTF-8 bytes, 32,993 whitespace-separated words, and 3,563 lines**, counted once each. It excludes later conditional chapters, full applicable schemas/templates, filled records, and repeated reads. These are file-size observations, not measured model tokens, latency, cost, or a demonstrated context failure. [E: reading-burden inventory.]

The main `SKILL.md` is 101 lines, but its shortness does not describe the full activated workload. The KB itself warns that a small entry point that always loads long references can still be costly. The wrapper already supports staged reading; the improvement is to measure and sharpen it. [K: handbook/08-performance-and-cost.md; S: commands/skill-builder-create.md, line 35.]

Preserve every original byte and all 99 decisions. Use an identity-bound reading ledger, complete-source loading at the relevant decision point, stable paths, optional range/record retrieval for large files, and fewer repeated operational statements. Measure a small writing task and a resource-assisted task before and after changes, including continuation and actual output quality. Do not reduce a metric by deleting source material, replacing it with summaries, or silently skipping applicable rules. The public skill specification also recommends progressive resource loading, consistent with this approach. [W1.]

### 7.2 Make provisional exclusions harder to mistake for final decisions

The profile selector gives some unselected rules a default `not_applicable` decision with a generic warning to verify the declared scope. The workflows correctly require that review, so this is not missing procedural coverage. A generated completion flag or capability inventory would make it harder to carry a default exclusion into a final report unchanged.

For example, local file writes can occur without a publication, installer, or persistent-state modifier. The agent must still assess destination/ownership controls. Consider storing provisional selection separately from final applicability evidence and refusing a final release verdict while exclusions remain unreviewed. Keep this as a wrapper/companion improvement rather than rewriting the original canonical profile data. [S: scripts/skill_builder.py, line 263; S: references/requirement-coverage.md, line 43; CMD-004.]

### 7.3 Add narrowly useful maintenance checks

After the defects are corrected, add regressions for their observable outcomes. Expand CI to the minimum supported Python version and any OS you intend to claim, with path/encoding cases appropriate to that scope. Current local verification used Python 3.12.14 on Linux; it did not validate every Python 3.10+ or OS combination. The README already acknowledges that limit. [S: README.md, line 57; S: .github/workflows/ci.yml; E: environment.]

The current CI setup has useful protections: read-only repository permissions, pinned checkout code, no persisted checkout credentials, no privileged PR publishing path, and separate standard-library and optional-validator jobs. Exact dependency versions are pinned but distribution hashes are not. Hash-locking is a possible later supply-chain improvement if that is the maintained policy; it is not necessary to invent a claim that the existing pins already provide it. Remote GitHub CI execution was not performed in this review.

## 8. Fresh verification and task exercises

### 8.1 Local regression and packaging results

| Verification | Fresh result | What it establishes |
| --- | --- | --- |
| Source helper/package suite | 47 passed; zero skips | Existing local contract cases. |
| Preserved KB tools suite | 73 passed; zero skips | 53 format, 14 record, and 6 profile cases. |
| Release-only suite without site packages | 7 passed; zero skips | A repeated subset of the 47 under the standard-library path. |
| Project check with required validators | Passed, exit 0 | Implemented preservation, map, metadata, links, syntax, and dependency checks. |
| Project check without site packages | Core checks passed; optional validator explicitly blocked | Honest distinction between available and unavailable checking. |
| Three version-2.0 source evidence records | Schema checks passed | Record structure, not truth of every claim. |
| Rebuild of unchanged source | Exact source/runtime ZIP identities reproduced | Deterministic packaging for those input bytes and environment. |
| Additional boundary cases | Five executable defect families reproduced | Gaps beyond the supplied passing tests. |

Do not add the seven repeated release tests to the 47 as if they were new distinct tests. The three formal records checked were the final and earlier local evaluation receipts and self-rule traceability. Their structural validity does not negate the new defects or supply unrun host evidence.

The environment was Python 3.12.14 on Linux x86_64. Available validation versions exactly matched the pins: PyYAML 6.0.3; jsonschema 4.26.0; referencing 0.37.0; attrs 26.1.0; jsonschema-specifications 2025.9.1; rpds-py 2026.6.3; typing_extensions 4.16.0. No dependency installation was needed. Tests and builds used disposable copies, and execution chains were inspected first. [E: baseline results and test logs.]

### 8.2 Reproduced artifact identities

| Artifact | Bytes | Identity |
| --- | ---: | --- |
| Source ZIP | 12,685,526 | SHA-256 `624d313a45a15749c75a5251b53c40408808ba1ee3c7149e2d4697635bd06588` |
| Runtime ZIP | 11,996,105 | SHA-256 `28083dd9c2f0593d1562b9a8ef2b9c6c76c9076b1d188eca2b10b7a4ce7f35e2` |
| Runtime payload | 23 files, excluding its generated manifest | Manifest-array SHA-256 `abb578cb1358a7843198ef811eb97d9fb4178be4cb08742771c824eebb7c3138` |
| Source payload | 70 files, excluding its generated manifest | Manifest-array SHA-256 `96a109e5f0a4180a276ff62a6a61b188a868e18793c21e3c3a6c47a9ef657f51` |

The runtime digest matches the shipped final runtime receipt, and the source digest matches the upload. Fixed timestamps/modes, sorted entries, exact member checks, and detached archive checksums are well implemented for the current input set. The defects concern input selection and edge contracts, not a failure to reproduce this supplied package. [S: tools/build_release.py; S: validation/final-runtime-package-identity.json; E: rebuilt identities.]

### 8.3 Fresh-context task exercises

| Exercise | Observation | Scope limit |
| --- | --- | --- |
| Focused Q&A | Correctly distinguished five specification-based and 94 project-policy rules, chose a proportionate instruction profile, explained exclusions, and answered with source references without creating a project. | One source-based answer, manually reviewed; no statistical or native-trigger result. |
| Audit of an inert flawed target | Reviewed all 3 files / 1,208 bytes / 28 lines; reported 10 findings covering all seven predeclared issue families; retained all 99 dispositions and 18 schema-valid records. | A source audit; no target script or native host was executed. |
| Creation of an instruction-only skill | Produced a complete acceptance-criteria reviewer with a two-file runtime (`SKILL.md` and MIT `LICENSE`), 16 development cases, all 99 dispositions, and four schema-valid evidence records. | Local source/artifact creation; authored worked examples were correctly labeled illustrations, not independent trials. |
| Independent use of the generated skill | A fresh agent reviewed three input sets. It left precise criteria unflagged, asked about two ambiguous terms without inventing thresholds, and identified opposing button-state requirements under the same condition. Exact passages and requested columns were preserved. | One manually supplied invocation with three input sets; no native discovery, clean control, or reliability estimate. |

The integrating reviewer independently confirmed that every audit-target file retained its original hash and that no execution marker appeared. The generated skill's canonical and delivered runtime copies were byte-identical; the runtime contained no scripts or external resources. Its 12 portable checks and four evidence-record checks passed, while native support, independent author-time behavior, and comparative claims remained unrun in the original creation receipt. The later three-input exercise is a separate observation recorded by this review; the earlier receipt was not rewritten to claim it.

These exercises provide direct evidence that the builder can complete useful agent work beyond CLI preparation. They do not close the release defects or the native-host gaps. The full prompts, retained observations, target identities, and relevant verification records are included or identified in the evidence appendix. No claim is made that all private reasoning or tool traces were retained.

These are bounded development observations. The agents received the actual skill path and ordinary tasks, without expected answers or the independent reviewers' findings. They were manually directed to the source artifact; no native host selector or activation path was exercised. No clean no-skill control, repeated reliability estimate, calibrated model grading, or measured token/cost advantage is claimed. Unknown usage remains unknown.

## 9. Recommended correction sequence

### Phase 1: correct the current artifact

1. Fix selected-root/ancestor symlink handling and add a package-boundary regression.
2. Incorporate your MIT choice in both distributions, component coverage, current status, and builder output while retaining the original KB hash and third-party material.
3. Add finite-number validation, faithful description serialization, and stable per-record error handling.
4. Enforce a build-output policy that prevents prior releases entering later source inputs.
5. Configure the actual security-reporting route for the chosen public repository.

### Phase 2: regenerate truthful evidence

Run the affected negative and positive cases, then the existing local suite once against the corrected candidate. Validate the formal records, build twice in a supported location, and inspect the exact archive member set and notices. Record new payload/archive identities and append a dated resolution event for each finding. Keep this report and earlier receipts as evidence of their original versions; do not relabel old passes as results for new bytes.

Add own-project host-capability records and a clearly separated procedure/local/native support summary. Keep the complete KB unchanged and record any supplemental validator fix outside it. If a new KB version is later produced, give it a new identity and preserve the earlier source history.

### Phase 3: establish the claims you want to publish

Run the final-package native Codex panel first. Then run relevant shared cases on Claude Code and Grok Build before calling those integrations tested. If releasing experimentally before those runs, use explicit untested/documentation-only labels. Run clean comparative panels only when you intend to claim benefits over an unassisted baseline or a previous version.

Measure the real reading burden before simplifying operational loading. Improvements should retain source completeness, applicability reasoning, and task/safety acceptance conditions. The source already has the correct architectural separation for this work; focused corrections and stronger evidence are the appropriate next step.

## 10. Proposed acceptance checklist for the next candidate

| Gate | Required evidence |
| --- | --- |
| Preservation | Original KB ZIP and all 182 substantive identities unchanged. |
| Procedure coverage | All 99 canonical IDs, classifications, pointers, and owners retained; relevant changes reviewed semantically. |
| Packaging boundary | Selected-root, ancestor, descendant, and leaf symlink cases rejected; no external markers packaged. |
| Numeric input | Overflow/nonfinite cases fail per record; finite controls pass. |
| Metadata | Accepted descriptions round-trip exactly and pass the portable checker; rejected input leaves no output tree. |
| Build isolation | Supported repeated builds contain no prior release output and produce equal archive bytes. |
| Batch behavior | Valid/invalid/valid input returns all three per-record outcomes in order with the correct aggregate exit. |
| MIT distribution | Full terms, attribution, component coverage, and retained notices in both packages; generated current status agrees. |
| Current evidence | New checks bind to exact corrected payload; historical receipts remain historical. |
| Reporting | Actual private reporting destination and realistic supported-version policy documented. |
| Codex default claim | Native final-package discovery and representative tasks recorded, or experimental limits stated clearly. |
| Secondary hosts | Claims match separately recorded documentation, format, task, safety, and maintenance evidence. |

## 11. Sources and how to use the evidence appendix

Local citations use **S** for the extracted `skill-builder-1.0.0-rc.1` source project and **K** for the attached `agent-skill-project-knowledge-base_final` root. For readability, an S citation beginning with `SKILL.md`, `commands/`, `references/`, or `scripts/` is relative to `skills/skill-builder/`; other S paths are relative to the project root. Single line numbers are entry locations, and named sections/functions identify the full relevant contract. **E** refers to `skill-builder-review-evidence.json` accompanying this report.

The evidence appendix includes input hashes, independent preservation checks, the complete 99-row procedure review, environment and regression results, exact package identities, synthetic reproduction outputs, reading-load inventory, and fresh task observations. It deliberately distinguishes saved observation records from complete private tool traces. It is an audit record, not an automatic certification artifact.

### Current primary documentation

All URLs below were checked on November 23, 2026. Their role is to verify the stated external format/host/licensing facts, not to establish native execution of this package.

- **W1:** [Agent Skills specification](https://agentskills.io/specification). Portable structure and metadata, optional fields, and progressive loading guidance.
- **W2:** [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills). Codex discovery/invocation and skill packaging guidance; the previous developers.openai.com/codex/skills path redirects here.
- **W3:** [Claude Code: Extend Claude with skills](https://code.claude.com/docs/en/skills). Invocation, arguments, resource paths, and permission/instruction lifetime differences.
- **W4:** [Grok Build: Skills, Plugins & Marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces). Discovery and host-specific metadata semantics.
- **W5:** [GitHub: Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository). Repository licensing and placement guidance.
- **W6:** [Choose a License: MIT](https://choosealicense.com/licenses/mit/). Full MIT text and attribution/notice requirements.

## Appendix A. Complete rule-by-rule procedural coverage

Every row below retains the original canonical rule statement. **Present** means a substantive procedure was found, with three concrete owner routes recorded in the evidence JSON. It does not mean the implementation, a generated target, or every host passed the rule. See the findings above for actual defects and the separate native-evidence limitations. Basis abbreviations are **Spec** for specification and **Policy** for project policy; strength abbreviations are **Req**, **Cond**, and **Rec**.

| Rule | Basis / strength | Original canonical statement | Procedure |
| --- | --- | --- | --- |
| FMT-001 | Spec / Req | A skill has SKILL.md with YAML frontmatter and a Markdown body. | Present |
| FMT-002 | Spec / Req | name is a nonempty string, at most 64 characters, and matches its directory. | Present |
| FMT-003 | Spec / Req | name follows the published lowercase alphanumeric/hyphen rules without boundary or consecutive hyphens. | Present |
| FMT-004 | Spec / Req | description is a nonempty string of at most 1024 characters. | Present |
| FMT-005 | Spec / Req | Optional standard fields obey their documented types and limits, including compatibility and metadata. | Present |
| FMT-006 | Policy / Rec | Reject duplicate YAML keys, unsafe tags and ambiguous coercion in distributed metadata. | Present |
| FMT-007 | Policy / Req | Portable metadata contains no undeclared host extension or unresolved template variable. | Present |
| FMT-008 | Policy / Req | Runtime resource references resolve within the declared package or an explicitly allowed dependency. | Present |
| FMT-009 | Policy / Rec | The package contains only needed runtime resources and applicable notices. | Present |
| FMT-010 | Policy / Req | Format-validation claims list their checked and unchecked properties. | Present |
| INS-001 | Policy / Req | Define a concrete outcome, inputs, scope and output contract. | Present |
| INS-002 | Policy / Rec | Discovery text states triggers and relevant boundaries early. | Present |
| INS-003 | Policy / Req | Consequential instructions identify condition, action, evidence, failure behavior and authority. | Present |
| INS-004 | Policy / Req | Respect existing user authorization and higher-level execution policy. | Present |
| INS-005 | Policy / Rec | Ask only for missing information that materially changes the task or effect. | Present |
| INS-006 | Policy / Rec | Put branch-specific detail in references with explicit load conditions. | Present |
| INS-007 | Policy / Rec | Fix deterministic failures in resources before adding repeated prompt warnings. | Present |
| INS-008 | Policy / Req | One authoritative owner defines each policy or command contract. | Present |
| INS-009 | Policy / Req | Unavailable checks and partial completion remain visible. | Present |
| INS-010 | Policy / Rec | Examples teach decisions without requiring exact prose when meaning is the contract. | Present |
| INS-011 | Policy / Req | Keep observed facts, estimates, hypotheses and recommendations distinct. | Present |
| INS-012 | Policy / Rec | Remove task-irrelevant promotion, profiling and repeated ceremony from the core path. | Present |
| ARC-001 | Policy / Rec | Choose instruction-only, resource-assisted or suite/runtime according to actual needs. | Present |
| ARC-002 | Policy / Rec | Split discoverable skills by user intent, capability or materially different effects. | Present |
| ARC-003 | Policy / Req | Keep portable task logic separate from host integration. | Present |
| ARC-004 | Policy / Cond | Generated artifacts have deterministic sources, provenance and drift checks. | Present |
| ARC-005 | Policy / Cond | Handoffs contain identity, scope, decisions, outputs, status and pending effects. | Present |
| ARC-006 | Policy / Cond | Parallel workers have disjoint writes or an explicit integration owner. | Present |
| ARC-007 | Policy / Cond | Readers finish or are confirmed stopped before a shared snapshot changes. | Present |
| ARC-008 | Policy / Rec | Repository contribution documents are distinct from installed task instructions. | Present |
| HOST-001 | Policy / Req | Advertise named hosts and products rather than model brands alone. | Present |
| HOST-002 | Policy / Req | Record host version, platform, capability and tested status. | Present |
| HOST-003 | Policy / Req | Translate permission and invocation semantics explicitly. | Present |
| HOST-004 | Policy / Req | Unsupported and unknown capabilities do not silently become supported. | Present |
| HOST-005 | Policy / Cond | Resource paths work independently of the caller working directory. | Present |
| HOST-006 | Policy / Cond | For each secondary host claimed as functionally exercised, safety exercised or supported, run the applicable shared outcome and denied-action cases. Format-only targets remain explicitly untested for behavior. | Present |
| HOST-007 | Policy / Req | Format compatibility is not presented as functional or security support. | Present |
| CMD-001 | Policy / Cond | Public commands document inputs, outputs, effects, errors, limits and cleanup. | Present |
| CMD-002 | Policy / Cond | Machine output uses a versioned schema and explicit result states. | Present |
| CMD-003 | Policy / Req | Untrusted text is passed as data, not interpolated into shell source. | Present |
| CMD-004 | Policy / Req | Writes and deletions validate destination scope and ownership. | Present |
| CMD-005 | Policy / Cond | Validators and tests are inspected for hooks, plugins, downloads and side effects before execution. | Present |
| CMD-006 | Policy / Cond | Timeout, cancellation and retry behavior are bounded and observable. | Present |
| CMD-007 | Policy / Cond | Uncertain remote outcomes are reconciled before retry. | Present |
| CMD-008 | Policy / Cond | Temporary paths are unique and private; cleanup removes only owned state. | Present |
| CMD-009 | Policy / Cond | Durable writes survive interruption without false completion. | Present |
| CMD-010 | Policy / Cond | Reused results bind to exact relevant inputs and configuration. | Present |
| SEC-001 | Policy / Req | Treat lower-trust retrieved content, repository task data and tool results as data rather than new authority. Apply host-designated instruction sources only at their actual trust level, without expanding user authorization or overriding higher-level policy. | Present |
| SEC-002 | Policy / Req | List protected resources, trust boundaries and enforcement mechanisms. | Present |
| SEC-003 | Policy / Req | A control failure does not silently broaden access or weaken isolation. | Present |
| SEC-004 | Policy / Cond | Filesystem and network limits protect actual operations, including redirects and path resolution. | Present |
| SEC-005 | Policy / Cond | Browser profile/session reuse is explicit and scoped. | Present |
| SEC-006 | Policy / Req | Credentials are excluded from logs, arguments, URLs and exported artifacts where avoidable. | Present |
| SEC-007 | Policy / Req | Each external data flow has destination, content, default, authority and retention documented. | Present |
| SEC-008 | Policy / Req | Opt-outs persist across setup, upgrade and endpoint changes. | Present |
| SEC-009 | Policy / Cond | Classifier and redaction limits are documented and tested. | Present |
| SEC-010 | Policy / Cond | Paid operations have enforced bounds across parent and workers. | Present |
| SEC-011 | Policy / Cond | Hostile repositories cannot control the grader or authoritative expected result. | Present |
| SEC-012 | Policy / Cond | CI and distribution isolate untrusted input from privileged execution. | Present |
| EVAL-001 | Policy / Req | Separate structure, resource correctness and full agent outcomes. | Present |
| EVAL-002 | Policy / Req | Task cases have independent acceptance conditions and real artifact/state checks. | Present |
| EVAL-003 | Policy / Rec | Discovery has positive, negative, ambiguous and opt-out cases. | Present |
| EVAL-004 | Policy / Req | Include missing prerequisite, denied action, malformed output and interruption cases. | Present |
| EVAL-005 | Policy / Rec | Compare candidate, previous version and a clean no-skill control where applicable. | Present |
| EVAL-006 | Policy / Req | Freeze acceptance, retry and exclusion policies before a comparison. | Present |
| EVAL-007 | Policy / Rec | Use held-out tasks and repeated trials for stochastic claims. | Present |
| EVAL-008 | Policy / Cond | Subjective graders are calibrated and versioned. | Present |
| EVAL-009 | Policy / Req | Critical safety failures cannot be hidden by an average score. | Present |
| EVAL-010 | Policy / Req | A zero-test or unavailable-provider result cannot count as a passing check. | Present |
| EVAL-011 | Policy / Req | Verification binds to the exact package or input revision. | Present |
| EVAL-012 | Policy / Rec | Tests protect observable contracts and credible regressions. | Present |
| EVAL-013 | Policy / Cond | Regression claims include before-fix failure evidence or an explicit limit. | Present |
| EVAL-014 | Policy / Req | Evaluation receipts include versions, inputs, attempts, outcomes, artifacts and missing data. | Present |
| PERF-001 | Policy / Rec | Measure total activated context and end-to-end work. | Present |
| PERF-002 | Policy / Rec | Report cold and warm conditions separately. | Present |
| PERF-003 | Policy / Req | Token, latency and cost claims identify their measurement method. | Present |
| PERF-004 | Policy / Cond | Caches have keys, invalidation, retention and sensitive-data policies. | Present |
| PERF-005 | Policy / Cond | Persistent processes justify their lifecycle/security cost with measurements. | Present |
| PERF-006 | Policy / Rec | Performance changes preserve task and safety acceptance conditions. | Present |
| LIFE-001 | Policy / Cond | Installation targets one declared host/scope and inspectable version. | Present |
| LIFE-002 | Policy / Cond | Ownership records distinguish project files from existing user data. | Present |
| LIFE-003 | Policy / Cond | Locked dependency failure is explicit rather than silently refreshing the lockfile. | Present |
| LIFE-004 | Policy / Cond | Updates stage and validate before activation when the runtime requires it. | Present |
| LIFE-005 | Policy / Cond | Stable/development channels resolve to explicit intended revisions. | Present |
| LIFE-006 | Policy / Cond | One deterministic owner runs bounded versioned migrations. | Present |
| LIFE-007 | Policy / Cond | Rollback claims cover package, dependencies and state compatibility. | Present |
| LIFE-008 | Policy / Cond | Uninstall removes only owned integrations and preserves chosen user data. | Present |
| LIFE-009 | Policy / Req | Release checks inspect the exact distributed artifact. | Present |
| LIFE-010 | Policy / Cond | Provenance/checksum verification uses an explicit trust model. | Present |
| LIFE-011 | Policy / Cond | Lifecycle support is tested on claimed platforms. | Present |
| LIFE-012 | Policy / Req | External publication is covered by current authorization. | Present |
| OSS-001 | Policy / Req | README describes task, example, support, install effects, data use, limits and removal. | Present |
| OSS-002 | Policy / Req | Public claims link to reproducible evidence and retain negative results. | Present |
| OSS-003 | Policy / Rec | Contribution instructions name canonical files and valid commands. | Present |
| OSS-004 | Policy / Rec | PR requirements are proportional to changed behavior. | Present |
| OSS-005 | Policy / Req | Licenses and third-party notices accompany redistributed material. | Present |
| OSS-006 | Policy / Rec | Security reporting and supported versions are visible. | Present |
| OSS-007 | Policy / Req | Actions and reusable workflow references follow a reviewed immutable dependency policy. | Present |
| OSS-008 | Policy / Rec | Maintenance rechecks host semantics, examples, dependencies and data flows. | Present |
