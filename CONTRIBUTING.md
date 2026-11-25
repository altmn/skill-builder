# Contributing

Start with the task contract, a real failure or useful capability, and the affected rule IDs. Keep one owner for each instruction or deterministic behavior. Do not edit the embedded knowledge-base ZIP or its manifest to make a check pass. A source update needs a new immutable archive, full preservation/source-change record, license review, and fresh relevant evidence.

Edit portable instructions in `skills/skill-builder/`, host behavior in its `references/hosts/`, helper mechanics in `scripts/skill_builder.py`, and independent tests in `tests/`. Keep public examples and CLI help synchronized. Add tests for real observable contracts; avoid tests that only repeat an implementation detail.

Run the documented local checks from README.md. Preserve failed attempts and distinguish tested local behavior from native agent-host discovery. A recorded historical receipt is not a current CI run. When adding a permission, executor, storage, network, lifecycle, or publication boundary, include both permitted and denied cases and describe the actual enforcement layer.

Before preparing a source release from Git, review and add every intended input,
then run `python3 -I -B tools/check_git_inventory.py`. This read-only check catches
local evidence that would be lost from a checkout because it is absent from the
index, including globally ignored logs. Index membership is not a commit or a
byte-equality check; validate a clean index export as well. A source ZIP without
Git metadata uses its generated package manifest instead. Retain required raw
and failed evidence rather than removing its links to clear the gate.

Before submitting a change, inspect its effects, dependencies, generated package, license status, and support claims. The maintainer is Alex Allen (@altmn); use the repository support and private security reporting routes. Do not invent publisher attestations or host acceptance.

## Review record

Every change needs a fresh [workflow-impact review](docs/workflow-impact.md),
including maintenance-only changes whose create/audit disposition is a reasoned
`no_change_needed`. Start the assessment before editing, revisit it before
delivery, and include its path in the PR. Stage the intended changes and new
record, then run `python3 -I -B tools/check_workflow_impact.py`. CI checks record
coverage for committed changes; a reviewer still checks the reasoning and
whether the independent verification actually supports it.

Target-specific evaluation mechanics belong to
`skills/skill-builder/scripts/evaluate.py`; `tools/evaluate.py` is a repository
adapter, not a second implementation. Keep the create/audit procedures and
`assets/evaluation/` worksheets synchronized with the CLI contract, and test
other subjects through both workflows and a runtime-only copy.

Include the problem and impact, changed behavior, scope/effects, applicable rule IDs, exact commands/results, candidate identity, coverage and limitations, and any required maintainer decision. Attribute sources. Do not include secrets or private user traces.

## Public development

The default branch is `master`. Work on a new feature branch and open a pull request against `master`; never reuse a merged branch. Required CI, signed commits, linear history and resolved review conversations protect the default branch. No additional reviewer approval is required for this solo-maintained project.

By contributing, you confirm your right to submit the contribution under the project's MIT license while retaining applicable third-party notices. No separate CLA or DCO is required. Use synthetic fixtures rather than private user material. Follow [community expectations](CODE_OF_CONDUCT.md), [support](SUPPORT.md), and [security reporting](SECURITY.md).
