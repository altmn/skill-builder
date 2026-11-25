# Engineering-guide improvements: 2026-11-24

The branch adds strict YAML reuse, identity-bound paged KB reads, a fixed routing
corpus, and offline preparation/accounting for four task-comparison conditions.
The frozen archive and its manifest remain byte-identical to the prior commit.
The [implementation identity](implementation-identity.json) records exact runtime
and code/test/corpus bytes; no all-99-rules-pass or release certification is made.

## Local checks

The [final checks](final/checks.json) retain commands, status and both streams:
100 tests passed in the full pinned environment; 21 release tests passed without
site packages; 15 evaluation tests passed under Python 3.10 and, separately,
without site packages. Core and required-validator project checks passed.
The core check explicitly retains unavailable PyYAML checks as blocked; the
pinned check ran those checks successfully. Diff whitespace checks passed.
The repeated subsets are not additional distinct tests.

The [earlier development run](development/checks.json) retains the 99-test panel
and its other checks before the final safety-accounting regression was added.
Its pass is not substituted for the final 100-test run. Logs are sanitized
derived views; original stream hashes remain in each check index.

## Native pilot

The frozen [plan](pilot/plan.json) predeclared six native CLI sessions: two routing
queries and one explanation task under automatic, explicit, no-skill and prior
conditions, one trial each. CLI used fresh ephemeral projects, ignored user
configuration, read-only sandboxing and no bypass flags. No live user skill
directory, account setting or public repository was changed. Known user/shared/
plugin roots were checked for target copies; fresh project roots excluded
repository ancestry. Raw events remain private; only normalized evidence,
digests and sanitized final answers are retained here.

All six attempts completed within the declared 180-second deadlines. Both
routing cases met their labels. Candidate explicit, candidate automatic and
the no-skill baseline all met the frozen explanation checks: observed task
quality difference was zero on this one question. The prior answer also met
semantic checks, but native explicit invocation exposed no verifiable full
entrypoint read or activated digest. That comparison stays unscored.

The [summary](pilot/summary.json) is therefore **incomplete**, with five scored
observations and one retained identity gap. The [independent observations](pilot/independent-observations.json)
record full-read detection, output/tree checks and original trace digests.
The [observations](pilot/observations.json) preserve all six attempts and usage.
Dollar cost and exact default model version are unknown. Provider caching was
uncontrolled, and two sessions overlapped; timings are observations, not a speed
comparison. There are no held-out trials or statistical benefit claims. This
pilot is not a formal maintained-host support receipt; original host receipts
and their support limits remain unchanged.

Recompute the report with `python3 -I -B tools/evaluate.py summarize --plan
validation/engineering-guide-2026-11-24/pilot/plan.json --observations
validation/engineering-guide-2026-11-24/pilot/observations.json`. Exit 3 is expected
for the deliberately retained prior-activation gap, not a passing full panel.
