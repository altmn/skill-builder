# Incident-derived create and audit cases

Later [native comparisons](../../validation/uber-native-2026-11-24/README.md)
execute these four tasks under clean no-skill, previous and improved conditions.
The original case definitions and preparation-only records remain unchanged;
the later record retains failures, resource observations and scope limits.

This optional corpus broadens the builder's development evidence with two
creation and two audit tasks adapted from retained integration artifacts and
reviewer failures. It contains **case designs, not new passing runs**. The
prompts are newly authored adaptations, not transcripts of user requests. Case
provenance names the actual source artifact and the independent annotation.
The original routing/execution corpus and its historical schedule are unchanged.

The fixed split is two development and two validation routing queries, and two
development and two validation execution tasks. Each routing split has one
positive and one negative. Do not tune using validation results. All these files
and their historical sources are public development material: a validation label
does not prove that a model or future reviewer has never seen the task. A stronger
generalization claim needs separately owned, genuinely unseen field tasks.

## Prepare the panel

After freezing real candidate/environment identities, run from the source root:

```sh
python3 -I -B skills/skill-builder/scripts/evaluate.py prepare \
  --candidate /approved/candidate/skill-builder \
  --routing-cases evals/field/routing.json \
  --execution-cases evals/field/execution.json \
  --fixtures-root evals/field \
  --environment /approved/environment.json --trials 1 \
  --output /existing/parent/new-field-panel
```

With no previous revision or named variants, one trial schedules 16 slots:
four routing and twelve execution slots. Preparation freezes inputs and invokes
no agent, installs nothing and executes no subject. Use the
[shared protocol](../protocol.md) for matching controls, real activation,
independent artifact/effect checks, preserved attempts and usage accounting.

## Runner and independent grader

Supply only the case prompt and its declared input fixtures to the subject.
Keep this README, annotations and expected checks outside subject authority.
For an audit case, the trusted runner materializes the case's `materialization`
mapping in a disposable target outside live discovery roots; each destination
contains the exact declared fixture bytes. The runner records source hashes,
materialized target hashes and before/after state. The evaluator does not perform
this step. The setup fixture is intentionally inert text and must never execute.

For creation cases independently inspect actual delivered files, positive and
missing/ambiguous-input behavior, requirement/check mapping and source identity.
For audits independently confirm evidence locations, preserved unknowns and no
target writes/execution. A returned claim of preservation is insufficient.
Trajectory action IDs denote observed operations verified by the trusted adapter;
they are not tool-name requirements or text the subject must recite. Permit
equivalent valid paths, and grade outcome and trajectory separately.

Use an authorized disposable environment to expose hidden tools, cached files,
space/Unicode paths and undeclared dependencies. Record exact runtime/tool
identity, reset, credentials policy and absent capabilities. A temporary path
alone does not establish isolation. Native/model trials and comparative benefit
remain unrun until independent receipts for these exact cases exist.
