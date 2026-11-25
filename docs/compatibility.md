# Compatibility and support evidence

Documentation review date: **2026-11-22, America/Los_Angeles**.

Skill Builder has one portable parent entrypoint, two named workflow modes, and a reference/Q&A route. A mode name is not a separately registered native skill. The Python command-line helper is a local resource used by the workflows; its scaffold and static audit output do not replace the agent's semantic work.

## Invocation contract

| Surface | Create | Audit | Reference question |
| --- | --- | --- | --- |
| Codex CLI/IDE | `$skill-builder skill-builder-create …` | `$skill-builder skill-builder-audit …` | `$skill-builder Explain …` |
| ChatGPT with this skill available | Select `@skill-builder`, then request `skill-builder-create` | Select `@skill-builder`, then request `skill-builder-audit` | Select `@skill-builder`, then ask the question |
| Claude Code | `/skill-builder skill-builder-create …` | `/skill-builder skill-builder-audit …` | `/skill-builder Explain …` |
| Grok Build | `/skill-builder skill-builder-create …` | `/skill-builder skill-builder-audit …` | `/skill-builder Explain …` |
| Other host | Map the mode to the [custom host contract](../skills/skill-builder/references/hosts/custom-host.md) | Same contract | Provide trusted reference access |

These are documented target interfaces, not evidence that the package was installed on those products. Exact names may be qualified by a host's plugin namespace or selector. Verify the selected artifact rather than relying on its display name.

## Evidence matrix

| Target | Format and local resources | Native discovery | Representative host tasks | Host enforcement/continuation | Maintenance commitment |
| --- | --- | --- | --- | --- | --- |
| Codex CLI 0.170.0 | Local checks and exact candidate identity recorded | Bounded explicit/implicit discovery exercised | Create, audit and Q&A exercised | Read-only denial and native resume exercised; compaction and other families unrun; duplicate activation inconclusive | No unqualified supported-version promise |
| Claude Code | Shared portable artifact; local checks do not prove host parity | Not run | Not run | Not run | No supported-version promise |
| Grok Build | Shared portable artifact; dedicated adapter required | Not run | Not run | Not run | No supported-version promise |
| Grok Bot | No tested filesystem-package import | Not run | Not run | Not run | Not supported by a tested integration |
| Custom model/API host | Loader design supplied; application implementation required | Not run | Not run | Not run | Integration owner's responsibility |

An agent-assisted development trial is useful feedback, but is not a clean native discovery test, a measured improvement over baseline, or proof of an OS sandbox. A local test receipt must identify the code/artifact it tested. Do not copy historical KB passes into the current matrix. Unknown or missing usage is not zero cost.

## Detailed adapters

- [Codex](../skills/skill-builder/references/hosts/codex.md): native entrypoint, resource identity, selected installation scope and host evaluation recipe.
- [Claude Code](../skills/skill-builder/references/hosts/claude-code.md): explicit mode arguments, tool-grant lifetime, continuation and collision cases.
- [Grok](../skills/skill-builder/references/hosts/grok.md): product identification and distinct Build/Bot/API routes.
- [Custom host](../skills/skill-builder/references/hosts/custom-host.md): trusted loading, scoped execution, missing capabilities and acceptance evidence.

The adapters preserve the KB's distinction between task semantics and host behavior. They add no automatic account changes, tools, permissions, hooks or paid requests. Optional metadata never substitutes for actual enforcement.

## Read the complete preserved knowledge base

The original uploaded ZIP is retained at `skills/skill-builder/references/knowledge-base.zip`. It contains the entire source collection, including historical fixtures and their `SKILL.md` files. Keep it archived in an installed skill. Extract only into a new explicit directory outside every active skill-discovery root; otherwise a host might discover research fixtures as skills.

Resolve the actual skill root first. With an absolute script path, these commands are independent of the current working directory:

```sh
python3 -I -B /absolute/skill-builder/scripts/skill_builder.py kb read handbook/04-portability.md
python3 -I -B /absolute/skill-builder/scripts/skill_builder.py kb search 'permission' --path handbook/
```

The read command emits the complete selected source. Search returns navigation evidence and must be followed by complete reading of applicable material. Consult the helper's `--help` for exact current flags. There is no need to install the KB's historical example skills.

## Installation, updates and removal

Before installation, choose host, user/project scope, exact destination and source version. Inspect destination ownership and existing modifications, validate the staged runtime and record copied files with hashes. Copy only the complete runtime `skill-builder` directory into the selected host's supported skill location. A managed import mechanism may require a different route; use that host's contract. This repository itself performs no automatic installation.

Preserve existing user files and local edits. Updates should stage and validate replacement bytes before activation and retain a recovery path. Removal should follow the ownership record and leave unrelated configuration, outputs and modified files intact. A successful copy is not proof of discovery; verify the native selector and an explicit invocation separately. Plugin publication, host-specific ZIP upload and direct folder loading are distinct distribution paths.

## Minimum native evaluation before stronger claims

Freeze tasks, fixtures, expected effects, forbidden effects, reset, budget, retry policy and grading before comparing candidate and no-skill conditions. Use fresh contexts; a no-skill control must not inherit the candidate through AGENTS files, hooks, conversation history or preloaded memory.

Exercise explicit invocation, positive/paraphrase/ambiguous/negative triggers, opt-out, create, audit, Q&A, resources read from another working directory, unavailable capability, denied action, malformed result, interruption, artifact verification and cleanup. Use the full KB's 22 designs and apply HOST-03 through HOST-06 for temporal and identity behavior. Preserve all attempts and explain exclusions. A design without execution stays not run.

Record host product/surface/version, model or unknown, runtime/OS, policy, input/output identity, selected artifact, activated bytes when exposed, permissions, durable state, grader/checker and outcome. Keep the intended source hash distinct from activated identity. Run both allowed and denied actions at the actual claimed enforcement boundary. Recheck the exact distributed package after generation or packaging changes.

## Sources and update policy

The following official documentation was retrieved for this adapter review. Detailed facts are attached to their respective adapter, while the complete original KB keeps its own dated documentation evidence:

- [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Grok Build skills, plugins and marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces)
- [Grok Bot skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations)
- [xAI function calling](https://docs.x.ai/developers/tools/function-calling)
- [Agent Skills specification](https://agentskills.io/specification)

All access dates are 2026-11-22, America/Los_Angeles. Retrieval establishes documented behavior only. No immutable vendor documentation revision or full page snapshot was supplied by the reader; do not pretend a source URL is permanently versioned. Recheck relevant primary documentation before shipping changed adapters, and retain a dated update event rather than rewriting historical claims.

The original-material MIT selection is now recorded in [LICENSE.md](../LICENSE.md), with third-party exceptions in [NOTICE.md](../NOTICE.md). This dated license resolution does not change the historical documentation review above, establish native host support, configure a reporting route, or establish GitHub publication.

Dated update: [native CLI observations and public-payload review](../validation/public-native-2026-11-24/README.md), 2026-11-24. This sampled panel does not establish comprehensive or maintained support.

## 1.0.0 publication update — 2026-11-24

The standalone skill and OpenAI plugin are separate archives. The plugin declares `requires_local_executor: true`: its local-program workflow is desktop-only under [OpenAI's guidance](https://developers.openai.com/plugins/deploy/desktop-only), accessed 2026-11-24. It needs local file access, process execution and Python 3.10+; optional validators remain separately provisioned. No MCP server, hooks, installer or execution permission is bundled.

The development marketplace needs a client supporting portable root `plugin.json`; no legacy overlay is supplied. A valid catalog does not prove native installation. Earlier Codex observations concern prior bytes. Intended-host acceptance of the exact 1.0.0 artifacts, Claude Code/Grok execution and maintained version commitments remain unestablished. Stable versioning and GitHub publication do not change these limits. See [submission preparation](chatgpt-submission.md).
