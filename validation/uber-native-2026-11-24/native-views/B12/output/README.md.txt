# Meeting notes extractor

The [skill](skills/meeting-notes-extractor/SKILL.md) turns pasted meeting notes
or explicitly named local Markdown notes into JSON decisions, action items,
and open questions. The [example notes](examples/notes.md) and
[expected JSON](examples/expected.json) show an action owned by Alex and due
Friday, plus an action with both fields set to null.

## Use

Supply the skill to a host that accepts Markdown skill instructions, then ask
it to extract outcomes from a paste or a specific local Markdown file. For
file input the host needs a local reader that can report complete access.
For paste input the skill needs only the supplied text. The runtime payload
is the single skill directory under `skills/`. It has no executable resource
or host-specific configuration.

The expected runtime effects are reading the named files when applicable and
replying in the current conversation. The host controls permissions and any
retention of conversation data. The skill does not request additional access.

## Review and check

Use the independent [runner cases](checks/cases.md). With a complete captured
reply, run `python3 -I -B output/checks/check_reply.py example REPLY.txt` from
the parent of this project. Python 3.10+ and its standard library suffice for
the checker. Other case IDs are listed in the case table. The checker uses
fixture-specific wording anchors. Manually assess semantically equivalent
paraphrases, extra claims, and observed tool effects separately.

Update the skill, example, and independent cases together when the output
contract changes. The skill is instruction-only. The checker is development
source and stays outside the runtime payload.

## Evidence

The supplied contract defines the desired outcome and known failure modes.
There are no observed baseline or candidate host runs. Discovery, routing,
runtime behavior, native enforcement, timing, and token use remain unverified.
See [evaluation review](EVALUATION-REVIEW.md) for the evidence boundary.
