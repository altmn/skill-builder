# Meeting notes extractor

Extract decisions, actions with owners and deadlines, and unresolved questions from user-supplied meeting notes. The portable payload is [skills/meeting-notes-extractor/SKILL.md](skills/meeting-notes-extractor/SKILL.md).

In a host that loads agent skill instructions, ask “Extract decisions, actions and open questions from these notes as JSON,” then paste the notes or name each accessible local Markdown file. The [weekly release example](examples/weekly-release.md) produces the [example JSON](examples/weekly-release.json). Missing or incomplete notes produce a request for accessible input.

## Runtime and support

The instructions use the current conversation and, when required, the host's local file reader. Pasted input works without a file reader. A file request requires a complete read, including any continuation pages. The skill emits a chat response and has no runtime scripts, dependencies, installer, application state, or external destinations. File scope and tool restrictions are instructions for the host agent. Host enforcement remains a capability of the host. The skill targets portable Markdown instructions with Codex as the primary intended host. Native discovery, invocation, and containment are unverified.

## Independent checks

See [the evaluation guide](evals/README.md). The runner owns the fixtures, response capture, and trace. Keep the oracle and grader out of the candidate's context.

## Maintenance

Edit the runtime contract in the skill and update affected examples and cases together. Keep prior observations tied to the bytes and conditions actually exercised. This delivery contains source for runner evaluation. Public reuse terms were not assigned.
