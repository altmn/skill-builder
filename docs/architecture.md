# Architecture and source ownership

## Portable runtime

`skills/skill-builder/SKILL.md` selects create, audit, or explanation. `commands/` owns ordered work and outputs. `references/governance.md` owns rule/evidence semantics. `references/hosts/` owns discovery, invocation, resource resolution, permission differences, continuation, and support boundaries. The helper owns repeatable file/archive/profile mechanics. It does not finish the agent's substantive creation or semantic audit.

The exact original ZIP is the knowledge owner. All 454 original archive entries remain present, including directories and operating-system metadata. A separate manifest identifies 182 substantive files, totaling 76,965,199 uncompressed bytes. The complete handbook, 99 canonical rules, large file/instruction catalogs, schemas, templates, tools, examples, source register, notices, offline readers, and historical successes/failures are retained. Nothing has been replaced by a shorter retelling.

The archived representation prevents nested example `SKILL.md` files from becoming discoverable entry points and avoids loading a large corpus into every prompt. It is storage packaging, not removal of knowledge. `kb read` returns a complete original text file; search returns locators with explicit paging; extraction restores original substantive files to an explicitly chosen separate workspace.

## Repository and distributed skill

The source archive includes maintenance documentation, tests, evaluation designs, validation evidence, and the runtime skill. The installable archive contains the skill root and its required references/scripts/assets/notices. Development artifacts stay outside the runtime. Both include the same complete original KB ZIP. Build selection uses the top-level files and directories declared in `tools/build_release.py`; selected trees omit `.git`, `.venv`, Python caches, and directories literally named `dist`. Output must be a new directory outside **every selected source directory**, even a nested `dist` directory. A sibling of the project or a child of a top-level, unselected `dist/` directory is supported. Two builds to supported locations therefore cannot collect the preceding build's archives or receipts. Arbitrary older artifacts already placed in selected inputs remain input content and require explicit review; the builder does not silently delete or rewrite them.

Every required selected root, runtime root, leaf, and relevant ancestor must be a real nonsymlink path, and each resolved input must remain inside its project or runtime boundary. Missing or unreadable selected roots and traversal errors fail explicitly. `check_project.py` runs the same selection preflight before reading project payloads, and runtime identity generation applies the runtime boundary checks. These are point-in-time checks of a stable tree, not an operating-system sandbox against adversarial concurrent replacement. The builder also refuses common local environment/credential filenames, including `.env` variants, `.netrc`, `.pypirc`, and SSH private-key names. This filename check is not a secret scanner: inspect all selected contents before public distribution. The immutable supplied KB archive is retained as source evidence without rewriting its internal metadata.

## Evidence identity

Root `plugin.json` is canonical for the portable OpenAI plugin. The development marketplace points to this root. The plugin archive contains only this manifest, root notices/licenses, the two explicit icon assets and the complete runtime; tests, validation logs, repository automation and development catalogs stay in the source distribution. The standalone skill archive remains separate.

Local plugin checks validate this project's identity/version, listing fields, URL syntax, PNG headers/dimensions, inventory and preserved KB hash. They are not full vendor-schema validation, image decoding, URL access checks, skill scans or native activation evidence. The plugin declares `requires_local_executor: true`. Build receipts remain preparation records; publication is recorded separately without putting an archive's own hash inside it.

The [Uber supplement](../skills/skill-builder/references/uber-workflows.md) uses
the existing runtime evaluator for trajectories and named variants. Separate
offline companions own blinded artifact accounting (`scripts/ablate.py`) and
bounded specification/incident/lint checks (`scripts/review.py`). Both reuse
evaluation path/evidence contracts; none executes a subject or calls a model.
Create/audit export visibly unfinished worksheets through their shared helper.
The [adoption record](uber-adoption.json) assesses propagation independently for
both workflows. Existing packaging selection includes these runtime resources;
there is no new discovery entrypoint, installer, hook or external data flow.

Supplemental research is recorded in [the engineering-guide adoption record](engineering-guide-adoption.json) and a conditional runtime evaluation reference. It adds current procedures outside the frozen archive; the original 99-rule catalog, manifest and historical evidence retain their identities. Evaluation corpora, graders and offline reporting tools remain source-repository maintenance material.

The source archive's SHA-256 and every substantive KB file hash establish preservation. The runtime payload identity is the SHA-256 of a canonical sorted file manifest, excluding that generated manifest itself. Build receipts and archive checksums live outside the runtime they identify. Source packaging can include validation records that refer to runtime identity, while the final source archive hash remains detached. There is no recursive self-hash requirement.

An original source blob/hash inside the KB identifies its historical upstream source. It must not be substituted with the hash of an adapted display excerpt. A runtime manifest identifies this candidate. An actual-host activation receipt identifies what a host loaded, when observable. These identities have different purposes.

## Why these resources exist

`scripts/evaluate.py` in the runtime skill owns generic panel preparation and
accounting. It uses the installed helper for bounded data reads/inventory and
requires explicit subject case files and fixture roots. `tools/evaluate.py` is
only the repository adapter selecting the builder's development cases by default.
Supplemental templates under `assets/evaluation/` feed both create and audit
workspaces; their source knowledge and procedures remain outside the frozen KB.

Exact archive preservation, safe path handling, all-rule ledger generation, and reproducible packaging are recurring mechanical tasks. They are implemented in code and checked by independent outcomes. Domain decisions, instruction quality, applicability, severity, source interpretation, and consequential authorization still require agent/human judgment. More code would not make those decisions mechanically true.

There is no daemon, database, telemetry, browser driver, custom model router, or automatic installer. Network research is an explicit agent step when current external facts are needed. Capability-dependent procedures remain fully available in the KB and workflow, without forcing every generated project to acquire those capabilities.
