# Install and manage Skill Builder

For AI-assisted setup, use the [README prompts](../README.md#get-started). These are the direct steps. The current OpenAI plugin requires local execution, so its full workflow needs a compatible desktop environment.

## Choose a package

The [1.0.0 release](https://github.com/altmn/skill-builder/releases/tag/v1.0.0) publishes three separate packages and detached `SHA256SUMS`:

| File | Purpose |
| --- | --- |
| `skill-builder-1.0.0.zip` | Installable `skill-builder/` folder, with `SKILL.md` and the complete knowledge base |
| `skill-builder-1.0.0-plugin.zip` | OpenAI plugin metadata, icons, notices, and runtime for a compatible desktop plugin import |
| `skill-builder-1.0.0-source.zip` | Development checkout with tests, maintenance tools, docs, and evidence |

Check the downloaded filename/version and checksum. Do not upload the source ZIP as a plugin or copy the entire source tree into skill discovery. Source changes after the release do not alter the published assets or their recorded identities.

The plugin declares `requires_local_executor: true`. A browser conversation can guide setup, but cannot make this desktop-only package run on the web. An approved directory listing and a universal personal ZIP-import route are not claimed. Use your host/account's supported import mechanism. [OpenAI's desktop-only guidance](https://developers.openai.com/plugins/deploy/desktop-only) explains this restriction.

## Install a standalone skill folder

1. Choose the exact host and personal/project scope. Check existing destination ownership and local edits first.
2. Inspect the standalone package, then copy only the complete `skill-builder/` runtime folder into the host's documented skills location. Keep the knowledge base archived; expanding it in discovery roots could expose research fixtures as skills.
3. Record installed files and hashes. A copy is not proof of discovery; check the host's native selector in a fresh session.
4. Try a small [Create, Audit, or Explain request](../README.md#try-it) with explicit inputs and a new output directory.

The helpers use Python 3.10+; the optional full validation dependency set needs Python 3.11+. Installation does not supply missing tools. See the [host adapters](compatibility.md) for the supported discovery layout and current evidence limits.

## Local Codex plugin testing from source

With Git and a Codex client supporting portable root manifests:

```sh
git clone https://github.com/altmn/skill-builder.git
cd skill-builder
codex plugin marketplace add "$PWD"
codex plugin add skill-builder@skill-builder-dev
```

The development marketplace points to the portable plugin root. Root `plugin.json` is canonical. These commands install a cached plugin; they are separate from building archives, and native installation of the exact release is not claimed. Choose your installation scope through supported host controls.

Start a new session if discovery has not refreshed. In Codex, use `$skill-builder` or the skill picker (`/skills` in the CLI). In the ChatGPT tab of a compatible desktop app, type `@` and select the matching installed entry before sending a task without the Codex prefix. These are modes of one parent skill:

```text
$skill-builder skill-builder-create Create a skill that turns meeting notes
into decisions, action items, owners, and open questions.
```

```text
$skill-builder skill-builder-audit Review the skill in [skill directory]
and prioritize the findings without repairing it.
```

```text
$skill-builder Explain when a task should use a script instead of more
prompt instructions, with relevant knowledge-base sources.
```

Discovery, correct task routing, completed semantic work, and acceptance of a release are separate checks. Current local and historical results are recorded in [compatibility](compatibility.md) and [validation](../validation/README.md).

## Update, disable, or remove

Compare your installed version and source identity with the [published releases](https://github.com/altmn/skill-builder/releases). Choose the same distribution form and host scope. Preserve local modifications and generated work, stage/validate the replacement, and retain a recovery path. Refresh a cached plugin through the host's supported installation process; do not edit caches directly.

For temporary disablement, use the host's plugin/skill controls. For removal, identify the installed copy and its ownership record, then remove only recorded owned material. Leave unrelated configuration, user outputs, and modified files intact. Managed plugins may require an administrator. Verify availability in a fresh session afterward; that does not erase instructions from an existing conversation.

There is no automatic installer or updater in this repository. See the [compatibility guide](compatibility.md#installation-updates-and-removal) and [maintenance prompts](../README.md#update-or-remove).

## Use the helpers directly

For source development and optional direct CLI work, see the [retained technical quick start](technical-guide.md#prerequisites-and-local-quick-start). Run from the source root, with isolated imports:

```sh
python3 -I -B skills/skill-builder/scripts/skill_builder.py --help
python3 -I -B skills/skill-builder/scripts/skill_builder.py kb verify
```

The create helper prepares intake and a scaffold; the audit helper prepares inventory and structural evidence. Continue the corresponding agent procedure for semantic completion. Optional dependency setup is separate and never automatic. Full checks and reproducible archive steps remain in the [technical guide](technical-guide.md#validation-and-evidence).
