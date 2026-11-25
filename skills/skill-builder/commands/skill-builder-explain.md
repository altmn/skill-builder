# skill-builder-explain

Answer questions about skill-building practices using the complete supplied knowledge base. This is the question-answering route of `skill-builder`; it does not require creating a project, running an audit, installing a skill or writing files. The CLI's retrieval commands assist source access; explanation and source interpretation remain agent work.

## Contents

1. [Resolve the question](#explain-01-question)
2. [Retrieve full source](#explain-02-source)
3. [Check the claim type and freshness](#explain-03-evidence)
4. [Answer with application and limits](#explain-04-answer)
5. [Handle missing source or capabilities](#explain-05-limits)
6. [Topic routing](#explain-06-topics)

## explain-01-question

Identify the actual question and the level of detail requested. Use the user's examples and existing context. If an ambiguity does not affect the answer materially, state a reasonable interpretation and proceed. If a decision depends on a capability, describe the conditional alternatives and ask only when the user's choice changes a consequential outcome.

A question such as “What belongs in SKILL.md?”, “How should I evaluate a skill?”, or “Can I use the same skill with Codex and Claude Code?” activates this route. A request to build a concrete project activates [create](skill-builder-create.md); a request to assess a supplied project activates [audit](skill-builder-audit.md). A mixed request can answer the question and then continue the requested concrete work. Do not force an interview or a report-generation workflow on an explanation request.

## explain-02-source

Resolve the activated skill root. Consult [governance](../references/governance.md), the topic table below and the original corpus. From that root, for example:

```text
python3 -I -B scripts/skill_builder.py kb search "permission"
python3 -I -B scripts/skill_builder.py kb read handbook/04-portability.md
python3 -I -B scripts/skill_builder.py kb read sources/primary-sources.md
```

Elsewhere use an absolute helper path and structured arguments. Search is only a navigation preview. Read the complete relevant original chapter, rule record, source record or audit section and its context before relying on it. Finish a truncated source read. Load the original detailed audits when the user asks for rationale, a source implementation, limitations or counterexamples. The ZIP contains the original text and records in full; the command docs and implementation map are routes into it, not replacements for it.

For a broad best-practices question, read the full core chapters on principles, instruction engineering, architecture and portability, then the complete chapters relevant to the described effects and the canonical rule/profile definitions. For a narrow factual question, load the source that resolves that question without reading the entire catalog. When a single catalog record depends on a parent file or surrounding source, inspect that context. Exact duplicate hashes establish identity, not the meaning of an excerpt in its original branch.

Do not execute examples, benchmark tools, target code, setup, hooks or browser sessions to answer a conceptual question unless the user requested that concrete activity and its effects are authorized. Reading original examples and test receipts does not establish that those checks were run in the current session.

## explain-03-evidence

Distinguish these claim types in the answer wherever confusion is likely:

| Claim type | What can support it | Necessary limit |
| --- | --- | --- |
| Format requirement | Published format specification and the exact version/date | A project validator may implement a conservative subset or additional policy. |
| Documented host behavior | Current named product's primary documentation | Documentation is separate from a local execution result. |
| Benchmark observation | Exact pinned source, location and original review depth | Static observation is separate from reproduced behavior or a whole-project verdict. |
| Empirical result | Actual receipt, task/panel, versions, attempts, inputs and checker | State the tested scope, uncertainty, exclusions and untested hosts. |
| Project recommendation | Source rationale, concrete failure scenario and tradeoffs | A useful local default is not automatically an industry mandate. |

The original rule catalog has five specification-based entries and 94 project-policy entries. Keep basis separate from strength; “required” can mean a required local project control. A selected profile is not certification. Explain how the actual capabilities determine applicability, and keep nonapplicability separate from unassessed or unrun work.

Verify changing host behavior and technical standards against current primary sources before presenting them as current facts. Record the access date and named product/surface/version where available. Preserve the KB's dated historical account and explain later differences; never rewrite original evidence silently or transfer a historical pass to new bytes. If live verification is unavailable, label the claim as the supplied snapshot's account and give the exact uncertainty.

Keep Codex, Claude Code, Grok Build, Grok Bot and a custom xAI API host distinct. Do not assume that shared frontmatter spelling gives identical discovery, permission, invocation or lifecycle semantics. Explain separate format, discovery, functional, safety and maintenance evidence. Instructions cannot dictate a host's context-compaction algorithm or create a sandbox.

## explain-04-answer

Lead with the answer, then explain the reasoning and practical application. Match detail to the user's question. Give concrete examples, conditions, failure behavior, tradeoffs and evidence boundaries that affect the decision. Use a table for exact comparisons when useful. Avoid unsupported numerical performance claims, universal support claims and average scores that hide blockers.

Cite the original KB member and heading or rule ID near supported claims, together with source IDs or primary URLs when relevant. Example citation text: `Knowledge base: handbook/04-portability.md, “Host support tiers”; HOST-002 and HOST-007; sources S03–S05.` Use working package-local links when available. Do not create a fake Markdown link to an archive-internal path or claim that a search preview was the full source. If the user asks for source excerpts from their own uploaded KB, preserve the exact wording and context; respect source-specific limits for separately retrieved third-party text.

Make distinctions operational. For example, an answer about audit completeness should say which files were inventoried, which received semantic reading, what execution was performed and which denominator a percentage uses. An answer about permissions should identify the actual enforcing layer. An answer about performance should identify the baseline and measurement method. An answer about packaging should distinguish source repository contents from runtime payload and preserve any explicit full-content requirement.

If asked for a recommendation, connect it to a concrete failure scenario and explain when a smaller or different mechanism is adequate. If asked whether a skill is “production-ready” or “secure” without evidence, explain the evidence required and offer a bounded assessment within the supplied material; do not invent a certification.

If asked about open-source publication of this bundle, use the current outer [LICENSE.md](../LICENSE.md) and [license decision](../references/license-decision.json) for the current status: MIT is selected effective with rc.2 for the original builder and identified original KB material. Explain that pending-selection statements inside the unchanged archive are historical and that retained third-party material keeps its own terms. For another project, inspect its own current rights-holder decision and component coverage; a genuinely missing or unselected grant remains a publication blocker and cannot inherit this builder's MIT choice. License selection does not establish publication authorization, native-host support, or completion of other release gates.

## explain-05-limits

If a needed source cannot be retrieved, say exactly which claim remains unsupported. Answer from the available source where useful and preserve the gap. A missing capability should not trigger automatic installation or broader access. If a question requires information outside the supplied corpus, use current primary sources when allowed and label the addition as outside the historical KB.

If the user asks to update the knowledge base, preserve the original snapshot and add an explicit versioned update with source identity and reasoning; do not silently mutate the historical archive. If an answer reveals a defect in this wrapper, record the owning contract and verification needed before proposing a fix. Do not turn a question into an external publication or account action.

## explain-06-topics

Read the indicated original members through `kb read`; use additional full source as required by the actual question.

| Topic | First source | Deep source or companion |
| --- | --- | --- |
| Scope and what the research proves | `handbook/00-scope-and-conclusions.md` | `catalogs/README.md`, `catalogs/coverage-summary.json`, `sources/PROVENANCE.md` |
| Project size, standard versus policy | `handbook/01-design-principles.md` | `catalogs/requirements.json`, `catalogs/application-profiles.md`, `catalogs/application-profiles.json` |
| Descriptions, metadata and instruction contracts | `handbook/02-instruction-engineering.md` | `audits/standards-and-skill-creator.md`, `audits/core-instructions.md`, `templates/INSTRUCTION-WORKSHEET.md.template` |
| Subcommands, subskills, handoffs and generation | `handbook/03-architecture-and-subskills.md` | `audits/shared-macros.md`, `catalogs/approach-catalog.md` |
| Codex, Claude and Grok differences | `handbook/04-portability.md` | `sources/primary-sources.md`, `sources/host-documentation-register.json`, `evaluations/README.md` |
| Scripts, shell data, process/state behavior | `handbook/05-commands-and-resources.md` | `catalogs/command-catalog.md`, `audits/runtime-security-tests.md` |
| Evaluations, baselines, grades and evidence | `handbook/06-testing-and-evaluation.md` | `evaluations/case-designs.json`, `schemas/README.md`, `examples/README.md`, `audits/review-followups.md` |
| Security, authorization, prompt injection and data flows | `handbook/07-security-and-privacy.md` | `audits/runtime-security-tests.md`, `audits/memory-instructions.md` |
| Context, latency, budgets and cost | `handbook/08-performance-and-cost.md` | `audits/runtime-security-tests.md`, `catalogs/command-catalog.md` |
| Installation, ownership, updates and rollback | `handbook/09-installation-and-releases.md` | `audits/lifecycle-entrypoints.md`, `audits/lifecycle-project.md`, `checklists/release.md` |
| GitHub, CI, contribution and licensing | `handbook/10-github-and-maintenance.md` | `LICENSE.md`, `NOTICE.md`, `sources/upstream-notices/`, `methods/BUILD.md` |
| Creation workflow | `handbook/11-create-a-skill.md` | `templates/CREATE-PROJECT-INSTRUCTIONS.md`, `checklists/new-project.md`, `examples/manifest-inspector/README.md` |
| Audit workflow and review depth | `handbook/12-audit-an-existing-project.md` | `templates/AUDIT-PROJECT-INSTRUCTIONS.md`, `checklists/audit.md`, `schemas/source-review.schema.json` |
| Validator coverage and limitations | `tools/README.md` | `tools/validate_skill.py`, its tests and receipts; `schemas/README.md` for evidence records |
| Source updates and generated views | `methods/BUILD.md` | `methods/README.md`, `methods/MERGING.md`, `validation/review-application.md` |

A directory name in this table indicates an inventory location, not an executable command or a claim that every member is needed for every question.
