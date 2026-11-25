# Workflow-impact review validation: 2026-11-24

Repository maintenance policy now requires separate create/audit propagation
decisions at planning and delivery. AGENTS.md, contributor guidance and the PR
template route authors to append-only records and the staged/CI checker. No
runtime skill files, frozen KB bytes or target behavior changed in this policy.

[Actual commands/results](results.json) and both streams are retained. The full
pinned suite passed **118 tests**. The new Git-aware gate passed 11 tests without
site packages and, separately, 11 under Python 3.10; these are repeated subsets,
not extra distinct tests. Core and required-validator project checks passed.
The core invocation keeps missing optional YAML checks blocked; the pinned
invocation executed them. Logs are sanitized derived views with original stream
hashes retained in results.json. No new native panel was necessary for this
repository-only change; prior runtime observations retain their exact identities.

Regressions exercise missing, stale, incomplete and placeholder reviews; both
workflow decisions; justified no-change outcomes; evidence references; staged
versus unstaged bytes; append-only record history; committed/CI ranges; and
preserved verification limits. Temporary Git repositories use fixture identities
and no hooks, network or external accounts. No live Git hook is installed.

The checker proves record freshness, schema-like contracts and path coverage,
not the truth of reasoning or test claims. Remote CI execution and branch
protection changes are not claimed. Reviewers still assess whether an improvement
needs downstream changes and whether the evidence is sufficient.
