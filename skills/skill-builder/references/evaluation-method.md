# Routing and incremental-value evaluation

Load for description optimization or claims about quality, context, latency or
cost. This supplements the frozen KB's chapters 02, 06 and 08, its 99-rule ledger
and original evidence schemas. Installed `scripts/evaluate.py` prepares panels
from the subject's explicit case files and fixture root and accounts for
observations offline; it does not run agents or graders. The source-repository
`tools/evaluate.py` is an adapter over that same engine and defaults to builder
development cases only when no target cases were supplied.

## Separate the questions

| Condition | Question |
| --- | --- |
| No target skill available | What can the baseline agent do? |
| Candidate explicitly activated | Do the instructions improve execution? |
| Candidate automatically selected | Does the complete system improve the task? |
| Previous revision explicitly activated | Has execution regressed? |

Use matched prompts, fixtures, tools, model/settings, policy and budgets. The
treatment's skill resources are an intentional difference. Keep a realistic
distractor catalog fixed, excluding only the target from the control. Check
hidden copies, ancestors, hooks, memory and inherited context. Unverified clean
controls stay unscored. Mark the previous condition unavailable if none exists.

## Routing

Freeze realistic positives, near-miss negatives, label rationales and a
stratified development/held-out split before description edits. The source
repository starts with 20 prompts in a fixed 12/8 split; these are engineering
defaults, not format constraints. Use fresh sessions and repeated trials.

Require actual successful activation or a verified full read of the exact
revision. An answer claiming skill use is insufficient. Normalize target-skill
events only; unrelated skills do not count. Activation errors, incomplete traces
and mismatched revisions are unknown, never successful non-activation.

Report TP/FN/FP/TN, precision, recall, false activation rate and F1. Keep trial
metrics separate from query majority; require every scheduled trial and leave
even-trial ties unscored. Undefined ratios remain null. Separate development
from held-out scores. Repeated selection on validation needs a fresh test set.

## Execution and resources

Predeclare artifacts, independent checks, forbidden effects, identity, reset,
trials, budget and retries. Keep graders outside target control. Grade actual
outputs and effects, using code for mechanical facts and an independent rubric
for meaning. Require evidence. A safety invariant failure fails the run regardless
of other scores. A changed grader requires a new panel and retained old results.

Compare matched case/trial outcomes across conditions. Include every attempt's
resource usage, including failed and contaminated runs. Unknown tokens/cost stay
null. Separate warm/cold and cache conditions. Measure actual loaded references
and tokenizer counts before pruning; bytes and line counts are not tokens.

Report task success alongside assertion scores when useful so numerous trivial
checks cannot hide a failed task. Repeated trials are clustered by prompt, not
new intent coverage. Use prompt-clustered uncertainty estimates for larger
studies; a small pilot's descriptive differences do not establish broad benefit.

## Provenance

For observable trajectory grading, incident-derived cases, clean environments,
requirement/check traceability, blinded named-variant comparisons and local
failure feedback, apply [the Uber workflow supplement](uber-workflows.md).
Both create and audit emit its companion worksheets. These extend the existing
method without changing the frozen source or transferring builder results to subjects.

Adapted from the user-supplied **Engineering Agent Skills** (2026-11-24), sections
2, 6–7, 9–10 and 13. Its engineering recommendations and synthetic examples are
not format requirements. The source repository records the guide's digest and
adoption decisions outside the immutable KB. Its upstream `main` observations
were not a pinned checkout.

Primary references, checked 2026-11-24: [format](https://agentskills.io/specification),
[description evaluation](https://agentskills.io/skill-creation/optimizing-descriptions),
[output evaluation](https://agentskills.io/skill-creation/evaluating-skills).
Host permissions and isolation remain host responsibilities. Evidence hashes
establish byte identity, not truth of a normalized trace or semantic grade.
