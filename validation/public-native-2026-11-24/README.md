# Public payload and native Codex validation — 2026-11-24

Subject: commit `9339b16`; runtime payload SHA-256
`0e64bba5827c66df799bcb0690c6567ed14682e5c0457fa6c05845841549dc84`.
Earlier observations remain unchanged.

## Sensitive-information review

Reviewed 263 tracked files, 216 reachable historical Git blobs, and recursively
opened ZIP members including frozen KB, nested trial archives and OS metadata:
1,473 labeled streams / 188,217,219 bytes, including repeated content.
[Scan inventory and locations](sensitive-payload-review.json).

No matches were found for checked private-key, GitHub-token, OpenAI-key,
AWS-access-ID or Slack-token patterns. Pattern scanning cannot establish absence
of arbitrary, encoded or unrecognized secrets. No archived code was executed.

**Privacy metadata remains:** 27 current-payload locations, including archive
members, contain 170 home-path occurrences and 32 email-like matches. Counts
include repeated views and false positives. Context inspection of KB email-like
matches found Git SSH URLs, package filenames, synthetic fixtures and attribution
examples; no private contact detail was established. Historical logs and reports
expose local usernames and workspace structure. Publishing Git history would
also expose historical metadata. The owner should decide whether to accept that
disclosure or prepare explicitly redacted derivatives with provenance. No source
evidence was silently removed or rewritten. The frozen KB and manifest are intact.

New public native records omit raw event streams, session IDs and reasoning traces.
Disposable root paths are aliased in answers. Original event hashes are retained;
raw events and the owned test session remain in private local storage.

## Native Codex results

Actual host: Codex CLI **0.170.0**, macOS arm64, existing ChatGPT authentication,
disposable project-scoped copies, user config ignored, read-only/workspace-write
policies without bypass flags. Global discovery metadata could still be present.
Default model/version and dollar cost were not captured; returned token usage is
retained. These are actual CLI runs, not agent simulations.

| Case | Result |
| --- | --- |
| Explicit Q&A from unrelated directory | Correct 5 specification / 94 policy distinction, citations and resolved-root reads. |
| Implicit Q&A | Correct selection and source distinction. |
| Unrelated request | Returned 4 with no builder commands. |
| Explicit opt-out | Returned Paris with no builder commands. |
| Denied creation | Actual read-only Git HEAD.lock write denial, honest blocked answer, no requested output. This does not prove all filesystem restrictions. |
| Audit | Four findings including name mismatch, missing resource and hostile setup; three target files unchanged, no execution marker; 99 unique rule IDs. Both ledger and four finding records independently schema-valid. |
| Create | Usable local-summary skill beyond scaffold, two examples and injection boundary; 99 unique rule IDs; independent portable-format and ledger checks pass. The generated skill itself has not had native behavior trials. |
| Repeat invocation/resource identity | Correct modes, display name and resource path. |
| Source edit/fresh invocation | New disposable marker observed; no already-loaded refresh claim. |
| Duplicate same-name roots | Honest ambiguity; actual activation precedence **inconclusive**. |
| Removal | Project/catalog copy absent on fresh run; other retained copies distinguished. |
| Continuation first turn | Task marker and read-only scope established in a persisted native session. |
| Native resume | Correct marker, prior root and authority restored without repeated effects. |

All 13 attempts exited 0 within deadlines; 12 met their bounded observations.
The **overall comprehensive-panel verdict is INCONCLUSIVE**: live compaction,
worker handoff, malformed tool-result injection and forced interruption/recovery
remain not_run. No clean baseline, statistical reliability or maintained-host
support is claimed. Claude Code and Grok remain unrun.

The exploratory Q&A preceded the main panel definition; identity and continuation
were separate extensions without one common frozen acceptance timestamp.
Creation/audit overlapped in a disposable Git checkout and changed its branch;
immutable Git-revision claims for that fixture are excluded. Runtime and target
bytes were independently verified. CLI does not expose the activated-text hash;
intended copy identity is explicitly separate. Local turn timestamps are inferred
from event-file filesystem bounds, not exact server clock times.

[Canonical receipt](evaluation-receipt.json), [observations](native-observations.json),
[copy identity](candidate-identity.json), [independent checks](independent-checks.json),
[output schema checks](output-record-validation.json), sanitized answers and
[cleanup record](cleanup.json) retain evidence. The receipt passes original schema
validation; that alone does not establish evidence truth.

Owned disposable installations were removed after byte checks. Copies/outputs
remain outside project discovery for inspection; one owned native test session
remains in normal private CLI session storage. No live user skill directory,
account setting or public repository was modified. Private security reporting
and the privacy-metadata publication decision remain outstanding.
