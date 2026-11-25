# Behavioral evaluation plan

This directory contains **designs**, not native-host passing results. The complete original KB includes 22 detailed evaluation designs; read `evaluations/README.md` and `evaluations/case-designs.json` through the helper. Keep them intact. The candidate-specific panel in `cases.json` instantiates additional concrete skill-builder outcomes without replacing the original panel.

## Conditions and independence

Use the [repeatable panel protocol](protocol.md), [routing corpus](routing.json)
and [task corpus](execution.json) for concrete routing/benefit measurements.
`tools/evaluate.py` freezes identities and computes evidence-bound summaries
offline. It does not run agents, call models, install skills or grade semantics.
The existing [bounded native observations](../validation/public-native-2026-11-24/README.md)
remain historical evidence for their exact bytes; they contain no clean comparison.

Freeze fixtures, expected artifacts, forbidden effects, budgets, retry policy and grading before running a comparison. Use a fresh candidate session, a separate clean no-skill session, and a prior-version session for later revisions. The control must not inherit this skill, its workflow, an AGENTS file containing it, a preloaded conversation, or an active candidate plugin. Record contamination if isolation fails; do not silently call that a clean control.

Use deterministic graders for paths, hashes, JSON schemas, exact outputs and forbidden side effects. Use a separately instructed reviewer for semantic instruction quality and source interpretation. Do not place a grader or expected answers in the target's authority. Keep all failed, blocked, inconclusive and excluded attempts with reasons. Report denominators and variation; a few development trials do not yield a universal success rate.

## Required records

Use the original versioned evaluation-receipt schema for formal host runs. Record case ID, source/package and input identities, actual loaded artifact or reason unknown, host product/surface/version, model/version or unknown, OS/runtime, permissions, reset procedure, budget, timings, attempts, usage/cost source, checker version, artifacts, outcome, omissions and redaction. Do not use intended source bytes as proof of activated bytes. Unknown usage is not zero.

For instruction continuation, source changes, removal, duplicate names and namespaces, use the actual host behavior described by HOST-03 through HOST-06. A textual simulation is useful but must be labeled simulation. Tool-approval lifetime, instruction lifetime and persistent state are separate.

## Scope of development checks

Local unit/contract tests establish helper behavior; structural validation establishes format and direct-resource properties; agent-assisted trials establish only the observed task in the supplied environment. Native discovery has bounded historical observations linked above. Clean baseline benefit, repeated outcome rates, latency/cost claims and secondary-host enforcement require their own concrete receipts; the new corpora are designs, not passing results.

Keep independent trial artifacts outside the candidate runtime so a future run cannot discover its expected answer. Retain a redacted receipt in the source project, bound to the exact candidate identity. Re-run affected checks after substantive changes and preserve the earlier attempt record.

## Incident-derived extension

The optional [field corpus](field/README.md) adds annotated creation and audit
tasks adapted from retained integration evidence and verifier failures. Its
inert fixtures, provenance and fixed split are separate from the default corpus;
preparing it makes no model calls and creates no new passing result. Supply its
explicit case files and fixture root to the installed evaluator. Public historical
adaptations do not establish unseen generalization or subject benefit.
