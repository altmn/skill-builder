<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/icon-dark.png">
    <img src="assets/icon.png" width="72" height="72" alt="">
  </picture>
</p>

# Skill Builder

Turn a repeatable task into an AI skill, or improve one you already use. Create a useful first version, review an existing skill, or ask a question about skill design.

[Try it](#try-it) · [Get started](#get-started) · [Get help](#get-help) · [Update or remove](#update-or-remove) · [Technical details](#technical-details)

> **Create:** a repeatable task → a skill to try
>
> **Audit:** an existing skill → prioritized improvements
>
> **Explain:** a question → a grounded answer

*Illustrative workflows, not measured results. Creation and audit include agent judgment; the bundled helpers prepare projects and evidence, not completed verdicts.*

<a id="start-with-a-task"></a>
<a id="what-it-does"></a>

## Try it

Choose the task you want to complete. **Create** and **Audit** are modes of the same Skill Builder skill, not separately installed skills.

| I want to… | Choose | What I receive |
| --- | --- | --- |
| Turn a recurring task into a reusable skill | Create | A candidate skill, examples, evaluation plan, and remaining decisions |
| Find worthwhile improvements in an existing skill | Audit | Evidence-linked findings, coverage limits, and a prioritized plan |
| Understand a design choice | Explain | An answer grounded in the preserved knowledge base and applicable sources |

**Paste into Codex after installation:**

```text
$skill-builder skill-builder-create
Create a skill that turns meeting notes into decisions, action items,
owners, and open questions. Ask about important missing requirements,
then build a small useful first version and an evaluation plan.
```

<details>
<summary>Prompts for auditing an existing skill or asking a question</summary>

**In Codex:**

```text
$skill-builder skill-builder-audit
Review the skill in [skill directory]. Prioritize the issues that affect
usefulness, activation, clarity, or reliability. Explain the evidence and
what still needs to be checked. Do not repair the skill.
```

```text
$skill-builder Explain when a task should become a reusable skill rather
than a one-off prompt. Use a meeting-notes workflow as the example and
help me choose the simplest useful approach.
```

</details>

**In the ChatGPT tab of a compatible desktop app:** type `@`, select the installed **Skill Builder** entry, and paste the task without `$skill-builder`. In the **Codex tab/app**, use `$skill-builder` or the skill picker (`/skills` in the CLI). The ChatGPT and Codex tabs use different selection syntax. Choose the actual entry; typing an unselected name is not installation or proof of activation. See [where it works](#where-it-works) for current limits.

<a id="prerequisites-and-local-quick-start"></a>
<a id="download-layout-and-installation-scope"></a>
<a id="github-and-openai-distribution"></a>

## Get started

The full workflow needs a desktop environment with local files and execution tools. You can still ask ChatGPT in a browser to help you choose the right setup and clarify your skill idea.

**Ask ChatGPT to guide you — paste into a chat at [chatgpt.com](https://chatgpt.com/):**

```text
I want to use Skill Builder to create an AI skill:
https://github.com/altmn/skill-builder

I'm using ChatGPT in my browser. Help me choose a supported desktop setup
for this project's full workflow and the right package for that tool.
Guide me through the next step without assuming I know command-line tools.
Help me clarify my skill idea here while I get set up.
```

**Ask a coding agent to set it up — paste into Codex or an agent with local tools:**

```text
Set up Skill Builder for this AI tool:
https://github.com/altmn/skill-builder

Read the current installation guidance, help me choose project or personal
scope, and use the correct installable package. Preserve local changes and
the complete bundled knowledge base. Verify the skill appears in a fresh
session, then help me try one small Create or Audit task.
```

Prefer direct instructions? Use the [installation guide](docs/getting-started.md). Choose the package by purpose:

| Package | Use it for |
| --- | --- |
| [Standalone skill ZIP](https://github.com/altmn/skill-builder/releases/download/v1.0.0/skill-builder-1.0.0.zip) | A host that loads a skill folder; copy only the complete runtime folder |
| [OpenAI plugin ZIP](https://github.com/altmn/skill-builder/releases/download/v1.0.0/skill-builder-1.0.0-plugin.zip) | A compatible desktop plugin import; local execution is required |
| [Source ZIP](https://github.com/altmn/skill-builder/releases/download/v1.0.0/skill-builder-1.0.0-source.zip) | Inspecting, developing, and testing this repository; not a plugin import |

These are the **1.0.0** published assets. [Checksums and release receipts](https://github.com/altmn/skill-builder/releases/tag/v1.0.0) identify them; subsequent source changes are separate. GitHub's automatic source archive is also distinct from an installable package. This project does not claim an approved OpenAI directory listing or a universal browser ZIP importer.

## Get help

If Skill Builder does not appear, check the chosen package, installation scope, and the selector for the AI tool you are using. If it appears but cannot complete a task, check local file and execution access.

**Paste into the AI tool where you are trying to use it:**

```text
Help me troubleshoot Skill Builder:
https://github.com/altmn/skill-builder

I'm using [AI tool and surface]. I installed [package or method].
When I try [task], I get [result or short error]. Check that I chose the
right package, the skill is available, and the tools needed for this task
are accessible. Guide me through the next useful step.
```

[Get support](SUPPORT.md) or [report a problem](https://github.com/altmn/skill-builder/issues/new/choose) using a small synthetic example and the relevant version. Keep private skill content out of public reports. Report vulnerabilities through the [security policy](SECURITY.md).

## Update or remove

**Ask the coding agent managing your installation:**

```text
Help me update my Skill Builder installation:
https://github.com/altmn/skill-builder

Compare the installed version with the latest published release and follow
the documented update process for this tool. Keep my generated projects,
local changes, and knowledge-base material intact. Verify Create, Audit,
and Explain are available afterward.
```

```text
Help me temporarily disable or uninstall Skill Builder from [AI tool].
Identify how this copy was installed and follow the project's instructions.
Keep my generated projects, audit outputs, modified files, and unrelated
settings. Help me confirm the result in a new chat or session.
```

See [direct update and removal guidance](docs/getting-started.md#update-disable-or-remove). There is no automatic updater; preserve owned-file records and local modifications.

<a id="validation-and-evidence"></a>

## Where it works

| Environment | Current position |
| --- | --- |
| Codex with local tools | Primary target. A bounded native CLI panel exercised earlier candidate bytes; comprehensive and exact-release acceptance remain incomplete. |
| ChatGPT desktop with local execution | The plugin declares desktop-only execution. Use a compatible installation route your account offers; native acceptance of the current package is not claimed. |
| ChatGPT in a browser | Setup guidance and planning are useful here; the current plugin's full local-file workflow does not run in an ordinary browser thread. |
| Claude Code, Grok Build, and custom hosts | Adapters are documented. Claude/Grok execution remains unrun; a documented adapter is not a tested support promise. |

Helpers use Python 3.10+. The optional full YAML/schema validation set needs Python 3.11+ and separately installed dependencies. See [compatibility and host guides](docs/compatibility.md), [current validation](validation/README.md), and the [preserved technical/evidence guide](docs/technical-guide.md).

<a id="full-knowledge-preservation"></a>
<a id="effects-trust-boundaries-and-data"></a>
<a id="build-reproducible-archives"></a>

## Technical details

Skill Builder retains its complete source knowledge base and all 99 rule IDs. The archive remains byte-for-byte preserved; applicability still requires judgment. The CLI assists with intake, source retrieval, scaffolds, and static evidence. Its output does not certify usefulness, safety, host support, or readiness to publish.

Ordinary CLI use is offline: it reads explicit local inputs and the bundled archive, and writes the requested output tree. It does not execute audited code, install dependencies, contact accounts, or publish. Share reports only with the intended audience. See [privacy](PRIVACY.md) and the [effects and threat model](docs/effects-and-threat-model.md).

| I want to… | Read this |
| --- | --- |
| Install, verify, update, or remove | [Getting started](docs/getting-started.md) |
| Use the helpers directly | [CLI contract](skills/skill-builder/references/cli.md) · [Technical guide](docs/technical-guide.md) |
| Understand the design and preservation boundary | [Architecture](docs/architecture.md) · [Knowledge-base preservation](docs/technical-guide.md#full-knowledge-preservation) |
| Inspect evaluations and historical evidence | [Evaluation plan](evals/README.md) · [Validation](validation/README.md) · [Technical/evidence guide](docs/technical-guide.md) |
| Build and release reproducible packages | [Technical build steps](docs/technical-guide.md#build-reproducible-archives) · [Release instructions](docs/releasing.md) |

<a id="maintenance-and-release-decisions"></a>

## Contribute

Documentation, examples, and focused improvements are welcome. Start with [CONTRIBUTING.md](CONTRIBUTING.md). Work on a feature branch and open a pull request against `master`; assess Create and Audit propagation separately using the [workflow-impact policy](docs/workflow-impact.md).

For maintainers: [presentation conventions](docs/presentation.md), [changelog](CHANGELOG.md), [submission preparation](docs/chatgpt-submission.md), and [community expectations](CODE_OF_CONDUCT.md). Existing source history, correction records, and failed/incomplete evidence remain linked in the [technical guide](docs/technical-guide.md).

Maintained by [Alex Allen (@altmn)](https://github.com/altmn). [MIT license](LICENSE.md) · [Retained notices](NOTICE.md) · [Terms](TERMS.md). This independent project is not an official OpenAI product.
