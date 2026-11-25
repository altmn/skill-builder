# meeting-decisions

Extract agreed decisions, action items and unresolved questions from supplied Markdown meeting notes. For example, “Action: rotate the on-call guide.” yields:

```json
{"decisions":[],"actions":[{"task":"Rotate the on-call guide.","owner":null,"due":null}],"questions":[]}
```

The complete runtime source is [skills/meeting-decisions/SKILL.md](skills/meeting-decisions/SKILL.md). The intended host is Codex with access to the explicitly named local files, or with notes pasted into the request. A typical prompt is “Extract decisions, action items and open questions from ./minutes.md as JSON.” With missing notes, the skill requests the Markdown. The runtime is instruction-only and has no package dependencies, installer, host configuration or persisted state.

Local source is ready for independent trials. Native discovery, execution, isolation and host version support remain unverified. File access and conversation retention depend on the host. The payload requests no external transfers, workspace writes or command execution.

[TASK-BRIEF.md](TASK-BRIEF.md) covers scope and trust. [EVALUATION-PLAN.md](EVALUATION-PLAN.md) defines independent grading. [EVALUATION-REVIEW.md](EVALUATION-REVIEW.md) records observations and gates. [LICENSE-DECISION.md](LICENSE-DECISION.md) records the public reuse gate.

For maintenance, edit the canonical runtime entry point and update affected independent cases and the oracle. Recheck exact payload identity, scope of reads, JSON shape and the affected fixtures before a new trial panel. Preserve old results with their original hashes. Report defects to the project owner with sanitized input and expected/observed outcomes. No native host versions are currently listed as supported.
