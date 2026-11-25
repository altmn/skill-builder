# Five-finding correction record

Date: **2026-11-24, America/Los_Angeles**. Branch:
`codex/fix-five-review-findings`. Baseline commit:
`6b80b706d891baed8dde3b8323e383f0072390b9`.

This records repairs to the [independent implementation review](../../docs/reviews/2026-11-24-skill-builder-review.md).
The original report and its evidence remain unchanged. This unpublished rc.2
correction snapshot has its own payload identity; prior package receipts are
historical and have not been rewritten.

| Finding | Correction | Verification boundary |
| --- | --- | --- |
| F-01 | Matching full Alex Allen attribution in source/runtime grants, decision metadata, exact builder expectation and regression tests. | Release contracts inspect actual packaged grants and reject shortened or matching-prefix alternative attributions. |
| F-02 | Retained 23 exact historical logs, added them to the local Git index, scoped validation-log ignore override, and Git release-input inventory gate. | Git fixtures exercise global-ignore omissions, project override and missing indexed evidence; clean index export is verified separately. No commit/publication is implied. |
| F-03 | Audit/explanation use the current outer MIT decision; archived pending status remains historical; other projects retain their own license requirements. | Paired source-backed interpretation check; full native audit/Q&A designs remain unrun. |
| F-04 | Cleanup checks successful write bytes and observed file/directory metadata, preserving edits/replacements/uncertain states and checking parent identities. | Inert before/after regressions cover in-place edits, replaced files/parents, metadata, unchanged/partial writes and unrelated material. These are point-in-time controls, not a filesystem sandbox. |
| F-05 | Ordinary release fixtures resolve the OS temporary root before creating paths. | Default macOS release panel plus synthetic system-temp alias and deliberate rejection cases. |

The bundled KB archive remains SHA-256
`9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204`;
its unchanged manifest remains SHA-256
`c7efadcddfb5dbf427ae16851b490728b5a2a932140923b99e705688cbc9f101`.
All 182 substantive member identities and all 99 original rule mappings are
preserved. None of these repairs modifies the archive or its historical text.

## Executed checks

| Panel | Result and evidence |
| --- | --- |
| Integrated default Python 3.15 suite | 79 methods: 8 failures and 3 errors, all from unavailable optional validators. No newly reproduced product failures. [Exact commands/results](available-environment/available-validation-results.json), [raw output](available-environment/integrated-default-tests.stderr.txt). |
| Standard-library release suite | 21 passed, zero failures/errors/skips, under default macOS temporary settings. [Raw output](available-environment/stdlib-release-tests.stderr.txt). |
| Git inventory regressions | Four passed: ignored evidence, project override, missing indexed files, and no-Git scope. Git fixtures include spaces in their paths. |
| Cleanup regressions | Nine passed on Python 3.15 and nine on Python 3.10; these are the same cases repeated on two runtimes. [Commands and source hashes](cleanup/results.json), [Python 3.15 output](cleanup/focused-python315.stderr.txt), [Python 3.10 output](cleanup/focused-python310.stderr.txt). |
| Before-fix cleanup observation | Original helper loses edits/metadata and follows a replaced root during cleanup in the selected regression panel. [Retained failing output](cleanup/before-regression-panel.stderr.txt). |
| Core project check | Passed with optional portable-format validation explicitly blocked under default Python. [Output](available-environment/core-project-check.stdout.txt). |
| Existing YAML-capable environment | Portable format and project checks passed using preexisting Python 3.14 / PyYAML 6.0.3. No packages installed. [Output](available-environment/available-yaml-project-check.stdout.txt). |
| Required-validator check | Failed because default Python lacks PyYAML/jsonschema/referencing. This is a blocked prerequisite, not a passing full-validation result. [Output](available-environment/required-project-check.stdout.txt). |
| Knowledge preservation | Exact archive and 182 member identities passed. [Output](available-environment/knowledge-preservation.stdout.txt). |
| F-03 source interpretation | Fresh-context read-only reviewer correctly distinguished the selected builder from a separate unselected project for audit and Q&A. Frozen fixture hashes unchanged. [Observation](license-source-check.json). This is not native discovery or full host evaluation. |
| Historical preservation | 130 protected archive/map/prior-evidence inputs unchanged, including all 23 retained logs. [Comparison](preservation.json). |
| Clean Git index export | Core and available-format project checks passed on an export containing all 23 original logs with matching hashes; no diagnostic source edits were needed. [Named staged snapshot, commands and results](git-export/clean-export-results.json). |
| Local package reproduction | Two source/runtime build pairs matched, written member bytes were verified, and actual grants contained Alex Allen. [Observation](package-reproduction.json). This local packaging check does not clear unavailable schema or native-host gates. |

The integrated nonpasses are the documented missing-dependency behavior, with
raw results retained. The user subsequently authorized temporary pinned dependency setup. All seven
requirements were installed at their exact recorded versions in a temporary
environment. The full 79-method suite then passed with zero failures, errors or
skips, as did required-validator project checks, canonical receipt validation,
the 21-method standard-library release subset and pip dependency consistency.
See [the pinned run record](pinned-environment/results.json) and
[full raw test output](pinned-environment/full-tests.stderr.txt). Earlier missing-
dependency attempts remain unchanged. Repeated subsets are not added to the
79-method denominator.

The [current runtime identity](runtime-payload-identity.json) identifies the
corrected runtime independently of source-only evidence additions. The original
root source-package manifest is retained as
[baseline-source-package-manifest.json](baseline-source-package-manifest.json).
Current source manifests are generated by the release builder; enclosing ZIP
checksums stay detached to avoid a receipt/archive self-hash cycle.

Native Codex/Claude/Grok discovery, clean comparative outcomes, remote CI,
installation and publication remain unrun. The private-security-reporting setup
decision remains separate. Local fixes do not promote those claims to passed.
