# Evaluation receipt reviewer

The portable, instruction-only skill is in [skills/evaluation-receipt-reviewer](skills/evaluation-receipt-reviewer/SKILL.md). It accepts explicitly supplied evaluation receipts and associated evidence, and returns a read-only review. The skill directory is the complete runtime source. Examples are relative to its entry point. No runtime dependency, script, host adapter, or permission grant is required by the source.

[Independent acceptance tests](tests/acceptance.md) are maintained outside the runtime directory. Give the reviewer only the case request and inputs. Keep expected judgments with the grader.

## Evidence scope

The supplied contract and synthetic unknown-activation example informed the skill. Source review can establish what the written workflow requests. Native discovery, automatic routing, actual activation, task execution, and comparative benefit are untested. Independent cases are authored and unrun. No previous reviewer release or observed baseline was supplied. The recorded keyword and field-name grader failures are synthetic counterexamples.

The [rule ledger](rule-traceability.json) carries 99 canonical identifiers with
provisional scope decisions and unverified outcomes. The original schema
validator and native runner were not run.

## Independent evaluation plan

Use R1–R4 as fixed execution cases and the routing controls as a separate
discovery check. Explicit loading can test task execution independently of
automatic routing. For a comparative claim, use fresh sessions with identical
inputs, tool policy and run settings for the candidate and clean no-skill
control. Include a prior version only when its exact bytes and attributable run
evidence are available. Freeze case bytes and the grader assertions before
the run. Hold new paraphrases and schema mutations out of description tuning.

Record every attempt and its output, action trace, candidate identity, actual
activation evidence or reason unavailable, and recorded usage or reason
unknown. Use the written assertions as the grading contract. A missing
observation remains inconclusive, and a forbidden effect fails its case
regardless of the quality of the answer. Keep retries as distinct observations.
No performance, routing or comparative claim is supported by this source delivery.
