# Independent checks

Run each prompt in a fresh invocation with the skill active. Capture only the
assistant's reply in a UTF-8 text file. The checker uses Python 3's standard
library, reads only the capture supplied on its command line, and never invokes
the skill or opens the paths in the case prompts.

| Case | Prompt |
| --- | --- |
| example | Extract from the notes below. Then paste the contents of ../examples/meeting.md as part of the prompt. |
| fields | Extract from these notes: Action: Sam publishes the agenda. Action: archive the minutes by next Tuesday. Action: Lee or Pat (owner TBD) checks the roster by end of day. Action: Morgan files the summary (due Monday or Wednesday, TBD). |
| empty | Extract from these notes: The meeting began with introductions. |
| missing | Extract the decisions, actions and questions from my meeting notes. Supply no attachment or pasted notes. |
| unreadable | Extract from the local Markdown file `missing-meeting-notes.md`. Ensure that path is absent in the invocation workspace. |
| partial | Extract from both sources: the local Markdown file `missing-meeting-notes.md` and these pasted notes: Decision: keep weekly releases. Ensure that path is absent. |

The test setup directions in the table are for the runner, outside the prompt.
Run `python3 output/checks/check_response.py CASE CAPTURE` from the project root.
The checker validates the JSON shape and case-specific content or checks that
the reply requests accessible input without returning extraction JSON. For cases
with an absent path, also inspect any tool trace for reads limited to the
requested path. For the worked example, confirm that no note command was
executed. The response checker cannot verify tool behavior from text alone.

These checks have not been run.
