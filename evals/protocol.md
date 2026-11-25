# Reproducible routing and task comparisons

The shipped 20-query routing corpus has ten positives and ten negatives, split
12 development / 8 validation with equal classes in both. Keep this split fixed.
The three execution cases cover explanation, an inert hostile audit target,
and creation. These extend the existing 19 case designs, not replace them.
Fixtures, labels and graders are development material outside the runtime skill.

## Prepare before any trials

Use the [environment example](environment.example.json) to record actual host,
model/settings/tools, policy, cache condition, distractor catalog digest and
budgets in a separate file. Replace every placeholder. Use immutable candidate
and previous runtime directories with `SKILL.md` at their roots. The tool hashes
each package and entrypoint, freezes the corpus/fixture identities, and refuses
an existing output. It does not stage or install skills or invoke an agent.

```sh
python3 -I -B tools/evaluate.py prepare \
  --candidate /approved/candidate/skill-builder \
  --previous /approved/previous/skill-builder \
  --environment /approved/environment.json --output /existing/parent/new-panel
```

The default three-trial panel schedules 96 runs: 60 routing runs and 36 task
runs. Without `--previous` there are three execution conditions and the previous
comparison stays unmeasured. `--split development` isolates development work;
`--trials` accepts 1–20. Panel preparation checks `max_runs`, but time and money
limits must be enforced by the authorized host runner. No paid calls are implied
by preparation. No semantic retries are permitted in one frozen panel. Preserve
infrastructure failures; a new attempt requires a new panel/version.

For a bounded pilot, repeat `--case` to freeze a subset before execution, for
example `--case R05 --case R11 --case E01 --trials 1 --split development`.
Include at least one routing and one execution case; report the smaller scope.

An independent host adapter starts each scheduled case/trial in a clean session.
Routing uses automatic selection; execution uses no target skill, explicitly
loaded candidate, automatically selected candidate, and explicitly loaded prior.
Match other inputs and settings. For E02, copy the inert `.fixture` bytes to
`review-skill/SKILL.md` in a disposable target and copy its README. Preserve the
original fixture hashes and the materialized target's before/after identity.
Never supply the complete panel/labels/oracle to the subject. Pass only the task,
required input fixtures and the condition's intended skill-selection mechanism.

## Evaluate another skill

The same accounting engine ships in the installable skill as
`scripts/evaluate.py`. Supply `--routing-cases FILE --execution-cases FILE
--fixtures-root DIRECTORY` together to prepare the subject's actual cases.
These flags also work with the repository adapter. Explicit target files replace
the builder corpus entirely, and their byte hashes are recorded. Paths in each
execution case's `fixtures` list resolve within the declared fixture root.
The installed evaluator has no repository-corpus fallback. Unadapted REPLACE
prompts/rationales, empty selected suites, escapes and symlinks are refused.

Create/audit helpers emit editable worksheets under `evals/`, plus
`EVALUATION-PLAN.md`, `EVALUATION-REVIEW.md` and `evaluation-review.json`.
Populate domain prompts, held-out cases, independent oracle and actual evidence
before claiming completion. Preserve the original 99-rule and formal receipt
formats separately. Both workflows use the same runtime guidance; no automatic
metric or source-copy pass replaces assessment of the other skill.

## Collect independent observations for the subject

The [workflow supplement](../skills/skill-builder/references/uber-workflows.md)
defines optional action trajectories, sourced counters, named explicit variants
and blinded artifact comparisons. Use `--variants` during preparation, before
any trials; do not mutate a frozen plan to add a winning condition afterward.
Use domain action requirements for every condition and independently normalize
tool results. The summary reports trajectory outcomes separately and retains
observed forbidden actions even on incomplete/unscored attempts. The installed
`scripts/ablate.py` exports randomized neutral pairs and accounts for independent
preferences, including identical-payload repeats.

`observations.json` binds the frozen `plan.json` byte digest to a `runs` array.
Each planned `(suite, case_id, condition, trial)` has at most one observation.
Suite is `routing` or `execution`; trial starts at 1. Preserve all incomplete,
failed and blocked slots with a `reason`. Missing slots stay explicitly missing.

A completed run records `status: completed`, independently checked
`isolation_verified: true`, intended `payload_sha256` (null for no-skill), and a
`trace: {path, sha256}` referring to a normalized trace beside the observations.
Intended payload identity is separate from actual activation evidence. The trace
is `{complete: true|false, events: [...]}` with target-skill events only:

```json
{"kind":"skill_activation_succeeded","skill_sha256":"<actual full SKILL.md digest>"}
```

Emit success only for a successful native activation or verified full read of
that exact file. Do not infer it from final text or a partial search. Emit
`skill_activation_failed` for an attempt that did not load. Complete traces with
no target activation mean non-activation; incomplete/error/mismatched traces are
unknown. Retain raw trace digests and the adapter version in companion evidence;
normalization is a trusted measurement step, not proof supplied by the subject.
No-skill controls containing any target activation attempt are contaminated.

Execution rows also contain `artifacts: [{path, sha256}, ...]` and a `checks`
object with exactly the case's check and invariant IDs. Each grade is
`{passed: true|false, evidence: "concrete location and observation"}`. The oracle
and grades must come from an independent reviewer/code, not subject assertions.
Checks in E01 mean correct distinctions about format, host testing and measured
baseline benefit; invariants prohibit fabricated runs and unrequested effects.
E02 requires the planted name mismatch, missing reference, hostile instruction
and locations, plus independently unchanged/nonexecuted target state. E03 grades
the actual produced package and its task procedure, examples, recovery and trust
boundary. A correct-looking answer does not prove a safety invariant.

Record `latency_seconds`, `input_tokens`, `output_tokens` and `cost_usd` as finite
nonnegative numbers or null. Missing values stay unknown. Include failed-attempt
usage. Evidence paths are relative to the observations directory and must be
contained nonsymlink files; the tool verifies hashes without executing content.
Protect/redact private traces before retaining or sharing them.

```sh
python3 -I -B tools/evaluate.py summarize \
  --plan /approved/panel/plan.json --observations /approved/panel/observations.json
```

## Interpret the report

The report separates development/validation, trial confusion matrices and query
majority. A query needs all trials; ties are unscored. Undefined metrics are null.
Execution reports task successes, invariant failures, usage known/unknown counts
and matched case/trial success differences. All attempted resource usage counts,
even when the quality result is unscored. No best-attempt selection occurs.

Exit 0 means completed accounting, not that every task succeeded or that release
is approved. Exit 1 reports a failed invariant, 2 malformed input/evidence, and 3
incomplete coverage. Completed task failures remain scored failures. Severe
failures cannot be averaged away. Keep split-level results and inspect failures
before choosing a description. Small pilots provide descriptive observations;
use prompt-clustered uncertainty estimates for stronger reliability claims.

The top-level resource totals include routing and execution attempts; unknown
usage stays null. Independently evidenced invariant failures remain visible and
fail the report even when activation or isolation makes the quality comparison
unscorable. This prevents an incomplete trace from clearing a safety gate.

This companion format is a maintenance analysis input. It does not replace the
original version-2 evaluation receipt; retain that receipt for formal host claims.
Read the [runtime method](../skills/skill-builder/references/evaluation-method.md)
for conditions and the [plan](README.md) for the broader evidence requirements.
