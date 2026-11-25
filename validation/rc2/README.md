# Skill Builder 1.0.0-rc.2: corrections and evidence

Prepared for Alex on **2026-11-23, America/Los_Angeles**. This is a focused
revision of the complete supplied source project. The original knowledge
archive, its manifest, all 99 rule mappings, original workflows, and historical
validation artifacts remain present. No knowledge source was replaced by a
summary or reduced rule set.

## Findings resolved

| ID | Change | Observed verification |
| --- | --- | --- |
| F-01 | Complete matching MIT grants in source/runtime, copyright 2026 Alex, dated scoped decision, exact KB coverage and retained third-party terms; current builder, manifests and workflow text use that decision. | Release tests inspect both ZIPs, declarations and current metadata. An inconsistent pending decision is refused. Historical pending text is retained as history. |
| F-02 | Check selected roots, runtime roots, ancestors and descendants before resolution/traversal; require contained real paths; propagate missing, wrong-type and unreadable-tree failures. | Original check/build both exited 0 and admitted the synthetic external marker. Corrected check/build both exit 2 with no output. Regressions cover all selected roots, runtime root/ancestor, descendant links, a project path alias, selected files and traversal errors. |
| F-03 | Guard JSON floating-point conversion against nonfinite results at every nesting depth. | Positive/negative overflowing exponents and named nonfinite tokens fail individually; finite exponent controls pass; subsequent records continue. |
| F-04 | Emit YAML-safe quoted descriptions with exact accepted Unicode values; reject surrogate code points before writing. | New creation regressions pass. Independent serialization probes round-tripped all 1,112,063 non-NUL Unicode scalar values in 1,088 bounded descriptions without a mismatch; a mixed CLI-created description also passed the preserved format validator. |
| F-05 | Refuse output beneath every selected source directory before creating files, including a nested dist directory. Support sibling outputs and an unselected top-level dist root. | Original nested builds grew from 12,685,526 to 37,369,648 bytes. Both corrected nested attempts are refused with no writes. Repeated supported builds produce identical archives and contain no earlier release output. |
| F-06 | Require an object with a supported string record_type before validator dispatch; retain every record result. Also handle an unknown tilde-user path as a per-record path error. | Mixed valid/malformed/valid batches retain order and exit 1. The additional path case first failed, then passed in both its regression and independent recheck, with empty stderr and a stable diagnostic. |

The unchanged standalone KB validator still has its historical numeric and
dispatch limitations. The corrected public wrapper checks inputs before
calling it. Altering the archived tool to hide those limitations would break
the preservation requirement; no such alteration was made.

## Final local evidence

| Evidence | Scope |
| --- | --- |
| [panel-definition.json](panel-definition.json) | Commands, acceptance conditions, input hashes, retry/exclusion policies and actual freeze timestamp recorded before the final run. |
| [local-tests.json](local-tests.json), [local-tests.log](local-tests.log) | **65 methods passed: 46 helper and 19 release tests; zero failures, errors or skips.** |
| [post-run-inputs.json](post-run-inputs.json) | Every frozen executing input retained its hash through the panel. |
| [project-check-result.json](project-check-result.json) | Required validators available; boundary/license/preservation/routing/format/link/syntax checks passed. |
| [kb-verify-result.json](kb-verify-result.json) | Exact KB archive and all indexed substantive member identities. |
| [stdlib-release-tests.json](stdlib-release-tests.json) | The same 19 release tests passed with -S; a repeated subset. |
| [stdlib-project-check-result.json](stdlib-project-check-result.json) | Core checks passed; optional format validation is explicitly blocked without site packages. This is not full validation. |
| [creator-check.json](creator-check.json) | Minimal format check passed on the source runtime directory. |
| [evaluation-receipt.json](evaluation-receipt.json) | Fresh schema-version-2.0 local receipt bound to the exact runtime ZIP and actual 65-test execution. Unknown usage remains null with reasons. |
| [evidence-record-check.json](evidence-record-check.json) | Current receipt structure and cross-field validation. A schema pass does not establish the truth of its observations. |
| [runtime-package-identity.json](runtime-package-identity.json) | Actual runtime ZIP members, hashes, manifest and detached ZIP identity. Source-only evidence additions cannot change this runtime. |
| [change-inventory.json](change-inventory.json) | Every original source payload path retained; changed files identified; frozen source and historical evidence compared byte for byte. |

The environment was Python 3.12.14 on Linux x86_64, with PyYAML 6.0.3,
jsonschema 4.26.0 and referencing 0.37.0. The run record lists the remaining
observed dependency versions. No dependency installation was performed.

The separate [preserved validator observation](preservation-inputs/preserved-validator-tests-current.json)
and [complete log](preservation-inputs/preserved-validator-tests-current.log)
record **73 passing tests** against the unchanged extracted archived tools.
These are not native-host tests and do not erase limitations outside that
historical test panel.

## Development and independent review

The runtime [before-fix](development/runtime/before-fix-runtime-tests.json)
and [after-fix](development/runtime/after-fix-runtime-tests.json) observations
run the same five added methods. The original helper produced 14 failing
subtests and seven error subtests. The corrected helper passed all five.
Those subtest counts are not added to the 65-method final denominator.

Packaging [before-fix](development/packaging/before-fix.json) and
[after-fix](development/packaging/after-fix.json) records preserve actual CLI
results and intermediate archive identities. The first expanded package-test
attempt had eight fixture-setup errors because this environment placed a
temporary directory beneath the copied project. The fixture now copies only
explicit project roots. The full original failure log and later passing run
are retained; the failure was not relabeled as a product pass.

The initial integrated **64-test** run is retained in
development/integrated-64. Independent review subsequently exposed the
unknown-user record-path case. Its
[before](development/runtime/path-expansion-before.json) and
[after](development/runtime/path-expansion-after.json) records, plus the
[independent recheck](independent-review/focused-recheck.json), document the
additional fix. The final 65-test run uses its own input identities.

The [independent report](independent-review/independent-review.md) and its
hashed [evidence index](independent-review/review-index.json) retain the
original negative observation and the subsequent resolution. Broader
independent probes were performed on the identified earlier corrected helper;
only the path-expansion branch changed afterward. Their exact reviewed
identities are retained, rather than rewritten to imply a new run.

## Preservation and repeatability

The supplied rc.1 source ZIP is identified by SHA-256
`624d313a45a15749c75a5251b53c40408808ba1ee3c7149e2d4697635bd06588`.
Its 71 original file paths remain represented: 70 source payload files plus
the regenerated source PACKAGE-MANIFEST.json. The original manifest and
supplied implementation review are preserved in ../rc1-review.

The KB ZIP remains SHA-256
`9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204`:
454 original entries, including metadata; 182 substantive files containing
76,965,199 uncompressed bytes. The KB manifest, all-rule implementation map,
and all 25 original validation artifacts other than the current index are
byte-identical. The original validation index text is retained below the
current section in ../README.md.

Run the supported checks from the extracted source root:

```sh
python3 -I -B -m unittest discover -s tests -v
python3 -I -B tools/check_project.py --require-validators
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb verify
python3 -I -B skills/skill-builder/scripts/skill_builder.py check --record validation/rc2/evaluation-receipt.json
python3 -I -B tools/build_release.py --output ../new-release-output
```

Use a new output directory outside selected source trees. Repeating the build
from identical input bytes produces identical runtime and source ZIPs.
Current generated manifests verify the exact written payload. ZIP checksums
identify bytes; they do not independently authenticate a publisher.

For an independent comparison with the original supplied ZIP, run
`preservation-inputs/compare_preservation.py` with --original, --candidate,
--require-manifest and a new --output path. Its source is retained and it
imports no candidate code. Keep a report that identifies the final source ZIP
outside that ZIP to avoid a self-hash cycle. Final source-byte verification
is performed after this evidence is assembled.

## Current claim boundary

MIT selection for the original material is resolved. The package remains
**prepared and unpublished**. Native Codex CLI/IDE, Claude Code and Grok Build
discovery, permission behavior and full task panels remain not run. Clean
comparative-agent studies, other operating systems/Python versions and remote
CI also remain unrun. No productivity, reliability, token, latency or cost
improvement is claimed from these local checks. Local durations describe the
observed subprocesses only.

All 99 procedures remain routed; their presence is not 99 passing behavioral
tests. The rc.1 self-assessment retains its original statuses and hash-bound
scope. This revision records specific defect resolutions and new local
observations, without promoting old procedure or host claims to new passes.

Before public release, configure an actual private security-reporting route
and run the native panels required by the intended support claims. The
filesystem checks assume stable inputs; no OS-level containment against
hostile concurrent replacement is claimed. Third-party terms and attribution
remain attached to their covered material.
