# Dependabot CI correction — 2026-11-24

Four dependency proposals each passed the full optional-validator job but failed the required propagation-review gate because no fresh impact record covered their one changed file. These are deterministic policy failures, not flaky tests. Original failed logs and exact run identifiers remain alongside this record.

The companion change applies all four proposals together: checkout 7.0.1 and setup-python 7.1.0 at immutable commits, PyYAML 6.0.4 and rpds-py 2026.9.1 at exact versions. Release notes, execution entrypoints, package Python requirements, wheel metadata/licenses and selected wheel hashes were reviewed. This review does not certify all upstream code.

Updated Python dependencies are tested in a fresh isolated environment provisioned from the reviewed binary wheels. Runtime procedures, original KB, templates and subject grading contracts remain unchanged; full-suite subject and packaged-runtime regressions verify the affected validation integration. No native host or general target-quality claim is added.

Future proposals are grouped by ecosystem, and PR checks run once without duplicate feature-branch push runs. They still require a reasoned impact record and successful tests. The published v1.0.0 archives retain their original identities; this maintenance change is unreleased source.
