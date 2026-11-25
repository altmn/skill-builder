# Independent integration review of Skill Builder 1.0.0-rc.2

Review date: 2026-11-23. Reviewer: independent integration agent. The review used the actual changed source at `work/skill-builder-1.0.0-rc.1` and the supplied rc.1 source ZIP. The source directory name retains rc.1; the edited project identifies itself as rc.2.

## Result

**No unresolved defect was identified within this review's scope after the focused correction described below.** The independent review found one adjacent batch-error defect, reported it to the integrating reviewer, and then confirmed its narrow fix. The initial failure and all initial observations remain unchanged in the evidence files. This result does not establish that the project has no defects outside the inspected and exercised paths.

### Finding I-01 — unresolvable user shorthand discarded the evidence batch

Priority: P3 / low. Status: **fixed and independently rechecked**.

With a valid record, the literal path `~skill_builder_integration_no_such_user_9a4255/evidence.json`, and another valid record, `Path.expanduser()` raised `RuntimeError`. The initial helper emitted a traceback on stderr, no JSON on stdout, and no per-record outcomes. The process returned 1 because the exception was uncaught; this was not the documented completed-check failure envelope. It contradicted the current CLI reference's promise that an unreadable/malformed record gets an individual failure while later records continue.

The correction confines the new catch to path expansion, converts that error into the stable message `Record path could not be expanded.`, and lets the existing per-record `BuilderError` handling continue the batch. It does not broadly suppress errors from the trusted validator.

The focused rerun returned exit 1, empty stderr, a valid JSON aggregate with `outcome: failed`, and all three per-record outcomes in input order: `passed`, `failed`, `passed`. Both valid record paths and the failing path were retained accurately. Evidence: [original failed stderr](unknown-user-record.stderr), [original empty stdout](unknown-user-record.stdout), [corrected stdout](unknown-user-record-fixed.stdout), and [focused recheck](focused-recheck.json).

## Identity binding

| Input | SHA-256 |
| --- | --- |
| Initial helper used for independent probes | `babea39afbd891f25c993d472aab0c9391468e94cc10a4d3be27003661b769c3` |
| Helper after the focused path-expansion fix | `02d059365b37ee12c03283bb406ea87d74305525ff1c7b554675f28d170d20d0` |
| Release builder inspected in the initial pass | `079847a2f686b8466ca1c7e82d4b7c3e4c67efb63871cba49b3f0db3db9f5a4f` |
| Project checker inspected in the initial pass | `2e6497050385277b9b26a8e91d3ac7c5c48689b0be4e907eb55e5f2df9d6b9f2` |
| Supplied rc.1 source ZIP | `624d313a45a15749c75a5251b53c40408808ba1ee3c7149e2d4697635bd06588` |
| Preserved KB ZIP | `9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204` |

The first independent harness also checked that its three reviewed Python files were unchanged when that harness finished. The post-fix recheck verified the expected new helper hash immediately before execution. Earlier checks are evidence for their recorded earlier bytes; they are not silently relabeled as a full execution panel on the final helper.

## Work performed and observed results

The reviewer read `AGENTS.md`, README and contributor instructions; inspected the edited helper, release builder, project checker, relevant tests, CLI contract, license declarations and current license decision; and inspected the preserved validation execution paths before invoking them. The custom probe source is [probe_review.py](probe_review.py), and its recorded output is [probe-run.log](probe-run.log). Complete structured observations are in [observations.json](observations.json).

| Area | Independent observation | Practical limit |
| --- | --- | --- |
| Full source preservation | The current KB ZIP and its content manifest are byte-identical to the corresponding members in the supplied rc.1 source ZIP. `KnowledgeBase.verify()` checked every indexed member: 182 substantive files and 76,965,199 uncompressed bytes. The original ZIP still contains all 454 entries. | Byte preservation does not independently establish every historical statement in the archive. |
| Full canonical rule content | Profile selection retained all original fields and values in all 99 canonical rule objects. No abbreviated rule text was substituted in the selected records. | This check does not establish that every workflow or host enforces every selected rule. |
| Description serialization | Every non-NUL Unicode scalar value—1,112,063 code points—round-tripped through the new serializer and PyYAML in 1,088 descriptions, each at most 1,024 scalars. A leading ordinary character kept every test description nonblank. No mismatches occurred. | This is exhaustive code-point coverage for this local serializer/parser pair, not exhaustive string-combination testing or a native host parser panel. NUL and surrogate code points are outside the advertised accepted input contract. |
| Full CLI description path | One mixed description containing quotes, a backslash, C0/DEL/NEL controls, Unicode line separators, BMP noncharacters, ordinary multilingual text, emoji and the maximum scalar value was created through the CLI. Its parsed value matched exactly, and its generated `SKILL.md` passed the preserved portable format validator. | Scaffolding remains visibly incomplete; the check does not establish a completed task skill. |
| JSON and batch failures | A 21-record batch preserved order and all results. It rejected positive/negative exponent overflow, named nonfinite tokens, unsupported dispatch types, a nested duplicate key, invalid UTF-8, a 5,000-digit integer exceeding the current interpreter's parsing limit, and overly deep JSON. Finite controls and valid records passed. A synthetic private-content marker was absent from stdout. | These are local synthetic inputs; they do not validate the truth of the historical example record used as the schema-valid base. |
| Current license consistency | The source and runtime license declarations were identical. The build's license metadata check accepted the current MIT choice, explicit original-material scope, retained exceptions, release version and exact KB identity. | This is consistency of the supplied declaration and artifact, not an adjudication of third-party ownership or distribution rights. |
| Project check | `python3 -I -B tools/check_project.py --require-validators` exited 0. All 18 reported checks passed, with no failed checks and empty stderr. | This run preceded the focused path-expansion patch. The integrating reviewer owns the final full-suite and final-package verification. |

The public JSON wrapper rejected the tested record values with stable per-record diagnostics. The unknown-user case above was the sole failure in the eight initial independent observations, and it has its own separate successful recheck. The initial observation set was not rewritten to remove that failure.

## Package boundaries and output placement: inspection findings

The inspected builder validates requested path components before resolving them, so a selected root or ancestor symlink is not hidden by `resolve()`. `source_paths()` checks all required source files and selected directory trees before the release preparation reads version/runtime/source payload bytes. Traversal errors propagate, selected files must be regular, and descendant aliases are refused. The project checker obtains its selected file set from that same boundary check.

`prepare()` requires a new output directory and an existing nonsymlink parent. It rejects an output located inside any selected source directory, including a nested `dist` under such a directory. Root-level `dist` and a sibling output are supported by the current selection policy. The builder resolves payload bytes before creating its staging directory, writes manifests and detached hashes, and reopens its written archives to compare the actual members with the source bytes.

The new package tests cover these contracts in synthetic copies, including selected-root and ancestor symlinks, selected-file links, traversal errors, forbidden nested outputs, allowed repeated builds, and license/manifest agreement. This reviewer inspected those tests but did not independently rerun the package test suite or produce final release ZIPs. Those executions are deliberately left to the integrating/package reviewer to avoid duplicating an already active panel.

The code and CLI documentation explicitly describe a point-in-time filesystem boundary. They do not claim OS-level containment against another process replacing directories concurrently. No race-resistance result is asserted here.

## Environment and limits

The independent probes used isolated Python 3.12.14 on Linux x86-64, with PyYAML 6.0.3, jsonschema 4.26.0 and referencing 0.37.0 already available. No dependencies were installed. The temporary validation material and probe outputs were confined to this evidence directory; no project files were edited by this reviewer.

No native Codex, Claude Code, Grok Build, Windows, macOS, remote CI, installation, update/removal lifecycle, external service, account or publication operation was exercised. No comparative agent task-benefit, permission enforcement, hostile-process containment or legal-rights assurance is claimed. The final distributed archives and their detached identities require the integrating reviewer's final verification.

## Evidence retention and integration

Preserve all top-level files in this directory if incorporating this review into the source evidence record. The original stderr, empty stdout, initial observations and initial probe log are part of the record even though the defect is now resolved. The record fixtures and generated Unicode scaffold are disposable synthetic working inputs and can be excluded from the release evidence bundle.
