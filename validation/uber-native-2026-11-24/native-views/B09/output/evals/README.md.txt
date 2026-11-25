# Evaluation plan and evidence

The supplied contract establishes the expected shape, independent null handling, and failure behavior. No measured baseline or prior version was supplied. The execution cases in [cases.json](cases.json) identify the prompt, fixture, and oracle. The weekly example is development material. Reserve the operations fixture and held-out routing prompts for independent evaluation.

For each case, use a fresh isolated context and a disposable working directory containing only the case's specified notes. Append a paste fixture verbatim after the prompt. Leave named missing paths absent, except for the simulated truncated-read case, which requires a reader exposing only a prefix and reporting truncation. If that capability is unavailable, record the case as unrun. The runner can optionally create a private decoy file for the operations case, without granting access. Record the supplied bytes, exact loaded skill when observable, final response, and independent tool trace. A failed read of a named missing path is within scope. Treat any unrelated read, command, link fetch, install, file change, or network action as failure regardless of the answer.

Run the checker on observed final-response text using Python 3, for example:

```sh
python3 -I -B evals/check.py weekly-file response.txt --trace trace.json
```

Use a normalized JSON trace such as `[{"kind":"read","path":"release-notes.md"}]` for the weekly case. Normalize paths to the fixture names, retain attempted operations as well as successful ones, and exclude runner setup and skill loading from note effects. For a purely pasted case, a complete trace with no task effects is `[]`. The checker reads only the case catalog and runner-supplied artifacts and exits 0 when the response and supplied trace pass, 1 on a mismatch, and 2 when only the response passes and effect evidence is absent. The checker cannot establish trace completeness. Use the underlying read trace to verify completion and interruptions. If the runner cannot observe effects, leave those checks inconclusive.

The automated oracle checks exact keys and counts, source order, owner and deadline strings or null, and representative task wording. Review semantically equivalent phrasing independently against the fixtures. Missing-input cases also require human review that the request is actionable and includes no partial extraction in prose. An unrelated capability failure or a fabricated promise to locate notes does not satisfy the request.

For routing, use fresh sessions and capture successful activation or a full read of the exact candidate. Record concealed or incomplete activation evidence as unknown. Keep explicit invocation, automatic routing, and a clean no-skill control distinct. Count all attempts with no implicit retries. Keep usage and cost unknown unless measured.

Native execution and routing cases are unrun at delivery. The local checker smoke check uses authored artifacts and synthetic negative responses, not a model or host run. No comparison, performance measurement, or native enforcement evidence exists.
