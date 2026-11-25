# Custom host adapter contract

For outcome/trajectory evidence and clean-environment trials, follow the
[shared workflow supplement](../uber-workflows.md). A trusted adapter records
observable action results, raw evidence digests and its own version; do not infer
success from answer prose. Record unavailable isolation or activation evidence.
This guidance installs no hooks, grants no tools and adds no host support claim.

This is an implementation and acceptance contract for another agent host. It does not ship a model API integration, daemon, sandbox, credential manager or universal loader. Reuse the portable task procedure and the full preserved knowledge base; implement only the host facilities the chosen task requires.

## Required interface

Provide a trusted loader that resolves one exact `SKILL.md` and records its source identity. Validate portable metadata, expose bounded discovery text and load the instructions when selected. Keep target repositories, tool results, web content and the knowledge base's historical source excerpts as data. They must not replace the current user's authorization or higher-priority host policy.

Pass one of `skill-builder-create`, `skill-builder-audit` or a best-practices question to the parent skill as ordinary task input. The application may map these modes to native commands, but it must implement and test that mapping. A heading or string in Markdown is not executable command registration.

Bind logical capabilities explicitly:

| Capability | Required behavior | Missing capability behavior |
| --- | --- | --- |
| Read approved files | Read the chosen target and exact bundled resources with provenance | Stop source-dependent conclusions or obtain the missing approved input |
| Write owned outputs | Create within a declared new output tree; preserve conflicts and unrelated data | Return feasible read-only findings and mark artifact creation blocked |
| Run local processes | Structured arguments, reviewed program, bounded execution and truthful outcomes | Perform manual review; mark deterministic checks not run |
| Structured user input | Resolve genuinely blocking missing context | Use ordinary conversation without inventing answers |
| Parallel workers | Supply minimal task-local context and collect outcomes | Continue sequentially |
| Durable task records | Preserve identities, decisions, effects and evidence across turns | Explain the continuity limit and avoid repeating uncertain effects |
| Artifact export | Deliver exact inspected bytes through the chosen supported channel | State export blocked while preserving available outputs |
| Filesystem/network/tool enforcement | Enforce the actual declared restrictions and test allowed/denied paths | Stop operations requiring that control; do not call advisory text a sandbox |

Use supported, unsupported and untested statuses with evidence. Do not infer support from a function name or configuration key. Load the complete KB `templates/host-capabilities.json.template` and its schema, then fill it with observed implementations, versions, cases and failure behavior.

## Resource and identity contract

Resolve resources relative to the activated artifact, independent of the current working directory. Verify the ZIP identity against the shipped manifest before parsing or extracting. The helper may print complete KB files without extracting them. Extraction must remain inside a new explicit owned directory outside host discovery roots. Reject traversal, links or ambiguous entries according to the helper's contract.

Record intended source identity and activated identity separately. A host may expose a path, content hash or native artifact ID; use what it exposes and label unknowns. An intended-file hash must not be presented as proof of the model's actual loaded text.

When a context window is limited, retain the compact router and load complete relevant files in stages. Keep a coverage/read ledger so context management does not silently remove applicable requirements. Full knowledge preservation does not require loading all catalogs into every turn. Conversely, a shorter index is navigation only and cannot replace the source guidance.

## Execution and authorization contract

Let the application decide whether a proposed tool call is authorized and permitted. Validate structured arguments before dispatch. Use scoped tools or processes; never evaluate a model-supplied command through a shell by default. Protect actual file operations against escape and account for symlinks, races and platform differences where relevant.

Keep audits read-only against input. Do not import target modules or invoke its own skill/hook to assess it. Separate static inspection from isolated execution tests and document the exact effects of any authorized execution. Local creation must not auto-install, push, publish, contact maintainers or invoke paid model APIs.

For subprocesses define response and capture-storage bounds per stream, deadlines, descendant cleanup, retention and redaction. Preserve nonzero status, timeout, truncation and interruption as distinct outcomes. Structured validation or a successful process exit cannot prove semantic quality or security enforcement by itself.

Track each external flow separately, including telemetry, model requests, remote artifacts and messaging. Ordinary local use of this package needs no telemetry, secret credentials or network access. If the custom integration adds a flow, document destination, content, purpose, default, authorization, retention, opt-out, failure and cost.

## Continuation contract

Store task identity, mode, target/output roots, package identity, applicable-rule decisions, completed effects, outstanding gates and authorization scope in trusted records. Separate loaded instruction text, temporary tool grants and durable state. Recover state after compaction or worker handoff and recheck current capabilities before new effects.

Do not repeat an already-completed write because a message disappeared. If receipt validity or effect identity cannot be established, inspect the authorized state and report uncertainty. Preserve failed and interrupted attempts rather than overwriting them with the later successful retry.

## Acceptance and support claims

Instantiate the KB's interoperability and HOST-03 through HOST-06 designs. Freeze normal, boundary, malformed, hostile, denied and interrupted cases; compare clean baseline and candidate conditions using independent checks. Exercise discovery, create, audit, source-backed Q&A, resource root resolution, continuation, collisions and cleanup.

Report format, discovery, function, safety and maintenance as independent axes. A custom loader's test does not establish every product using the same model. Publish exact package/host/model/runtime/policy scope, cases, trials, attempts, exclusions and unknowns. An unimplemented loader is a design, not supported functionality.

Use the entire preserved KB for the full requirements, including `handbook/04-portability.md`, `handbook/05-commands-and-resources.md`, `handbook/06-testing-and-evaluation.md`, `handbook/07-security-and-privacy.md`, the 99-rule catalog and evidence schemas. [The Agent Skills specification](https://agentskills.io/specification), checked 2026-11-22, supplies the portable format; enforcement and runtime integration remain the host's responsibility.
