# Workflow evidence, ablation and field feedback

This supplement adapts the user-supplied **How Uber Evals 1 Million Agent Skill
Invocations a Month** (2026-11-24), especially Skill Workshop, Evals, Ablation and
Continuous Improvement. [Original article](https://www.uber.com/us/en/blog/optimizing-ubers-agent-skills/).
Repository `docs/uber-adoption.json` records the supplied document's digest and
create/audit decisions. The original ZIP, manifest, 99 rules and historical
records remain unchanged. These are engineering recommendations, not format
requirements or evidence of benefit in another skill.

## 1. Specify observable behavior

Use `workflow-contract.json.template` alongside the task brief. Give consequential
outputs, required actions and forbidden actions stable IDs, concrete statements,
owner paths/SHA-256 and case/check mappings. Do not invent requirements to fill
a template. `scripts/review.py contract --record CONTRACT --target SUBJECT_ROOT
--execution-cases CASES` checks source drift, unique IDs and real check links;
forbidden actions must map to invariants. It cannot prove coverage, meaning,
authority or enforcement. Review changes before updating an owner digest.

## 2. Grade outcomes and trajectories independently

Execution cases may add meaningful action requirements:

```json
{"trajectory": {"required": ["read_inputs", "verify_output"],
 "forbidden": ["execute_untrusted_setup"],
 "before": [["read_inputs", "verify_output"]]}}
```

The trusted host adapter normalizes observable events in the identity-bound trace:

```json
{"complete": true, "events": [
 {"kind": "action", "name": "read_inputs", "outcome": "succeeded"},
 {"kind": "action", "name": "verify_output", "outcome": "succeeded"}]}
```

Outcomes are succeeded, failed or denied. Required actions need success;
forbidden actions fail on any observed attempt, including denial. A successful
predecessor must precede the first successful successor; an absent optional
successor imposes no order. Allow equivalent paths. Apply the same domain
requirements to no-skill controls; do not require a target helper to favor it.
Activation retains its existing separate meaning. Normalize returned results
and artifacts, not answer claims, intention or hidden reasoning. Retain raw
evidence digests, adapter version and redaction/coverage limits. Incomplete
traces stay inconclusive, but observed forbidden actions still fail even on
unscored runs. No trace collector, hook or new permission is installed here.

## 3. Use field failures and independent annotations

Record case provenance: actual field incident, adaptation of historical evidence,
author case or fixed golden fixture. Include redacted source identity and human
annotations for material correctness, allowed variation and forbidden effects.
Calibrate subjective graders against examples and retain disagreements. Freeze
held-out ownership; inspected public examples are development evidence, not
proof of unseen tasks. No fixed percentage mix or target failure rate is imposed.

Clean-room trials need an authorized disposable environment with explicit
runtime/image identity, tool inventory, absent caches/documents, path variants,
credential policy, reset and hidden-skill checks. Test the distributed runtime
from an unrelated directory including spaces/non-ASCII paths. A fresh directory
or isolated Python is not OS containment or native discovery. Leave unavailable
host/model/remote trials unrun and identify the claim they block.

## 4. Test variants before pruning

Use `ABLATION-PLAN.md`. `scripts/evaluate.py prepare --variants FILE` accepts one
to four named explicit variants with absolute runtime roots. Names begin with a
lowercase letter and contain lowercase letters/digits/underscores (32 characters
maximum); built-in conditions are reserved. Each gets exact payload/entrypoint
identity, execution slots and matched differences against explicit candidate.
Use identical candidate bytes in a repeat variant for A/A variation. Share the
frozen corpus/settings/budgets and randomize/interleave the runner's order.

`scripts/ablate.py blind` verifies observations and copies matched artifacts to
randomized neutral left/right paths, with a private key. It refuses empty pairs,
existing output, more than 512 pairs/4,096 artifact copies or 128 MiB total copied
artifact bytes. Budgets are checked before output creation. Keep the key outside judging; inspect
identifying prose in artifacts. Give the independent judge only pairs.json,
copied artifacts and the frozen rubric/calibration. A separate collector binds
annotations to the key and calibration evidence. `score` retains missing/unknown
preferences, ties, losing results and the underlying failed/incomplete panel.
Counts are descriptive, not confidence intervals or automatic release approval.
By default pairs compare each named variant to explicit candidate. Repeat
`blind --condition NAME` to select frozen comparisons, including `no_skill` for
whole-skill removal or `previous` when a prior revision exists. In preference
counts, `variant_wins` denotes the selected alternative, including no-skill.

Measure actual context, tool errors/calls, latency, caches and all attempts'
usage. Optional integer counters `tool_calls`, `tool_errors` and
`activated_context_tokens` require `metric_sources` naming their measurement
method. Missing values remain unknown. Do not infer tokens from bytes or causal
skill cost from overlapping session windows. Choose pruning, maintenance or
retirement from sufficient task-specific evidence. Preserve required knowledge
access and authority conditions during instruction experiments.

## 5. Convert friction into a local regression

`papercut.json.template` is opt-in local evidence. Record attempted, expected and
observed behavior, affected identity, owner, deduplication category, workaround
and redacted evidence. Triage and fix the owning code, adapter, instruction or
evaluation layer. Preserve failures. Resolution needs an actual regression case
and hashed receipt containing `case_id`, `outcome: passed`, exact
`subject_version` and `independent_checker`. Retain the original affected
identity in incident evidence when recording a fixed version.
`scripts/review.py papercut --record RECORD --evidence-root ROOT
--execution-cases CASES` validates structure without executing anything. Record
validity does not prove truth or a production fix. No external report is sent.

## 6. Use lints as review locators

`scripts/review.py lint FILE` reads one explicit UTF-8 Markdown file (1 MiB cap)
and reports numbered-step completion, command-result and vague-retry diagnostics
with line numbers and a source digest. Review one objective per step, observable
completion and a failure/remediation/stop table where useful. Judgment tasks
need not invent shell commands. Diagnostics are advisory and exit 0; zero
warnings is not semantic, quality or safety approval.

All companions are offline/standard-library. Exit 1 means detected contract drift
or failed experiment, 2 invalid/inaccessible/mismatched input, and 3 incomplete
ablation accounting. They do not run models, enforce runner budgets, install
anything or certify quality. Use original version-2 receipts for host claims.
