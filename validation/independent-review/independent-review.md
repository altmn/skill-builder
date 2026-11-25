# Independent review of Skill Builder

Review date: 2026-11-23 UTC. Scope: the candidate source project at `/workspace/scratch/1e5ab00a904f/skill-builder-project`. This was one substantive review, with focused verification of fixes made during it. The candidate was still being assembled; this is not the final release gate or a claim that all 99 rule decisions received an independent semantic audit.

## Current disposition

No unresolved code blocker was identified in the reviewed implementation after the focused fixes below. One contributor-command mismatch remained at the last documentation check. The final project check, complete local test run, all-rule mapping validation, final archive inspection, and exact final-package receipts remain the integrating agent's release work. Native host behavior was not exercised by this review.

### R-05 — Correct the contributor validation command

**Status: open at the last read; required documentation correction, not a reason to withhold a corrected download.**

- Location: `AGENTS.md:11`; enforcing code: `tools/check_project.py:158–159`.
- Observation: AGENTS tells contributors to run `python3 -B tools/check_project.py`, but the checker refuses non-isolated execution. The audit workflow's equivalent mismatch was corrected to use `python3 -I -B` before this review closed.
- Consequence: the repository's stated required validation command fails before performing its checks.
- Action: use `python3 -I -B tools/check_project.py` in AGENTS and keep README/CI/CONTRIBUTING examples consistent with the new launch contract. The root agent has been notified.

## Defects found and resolved during this review

### R-01 — Generated evidence reported the wrong builder version

**Status: resolved and verified.**

- Original location: `skills/skill-builder/scripts/skill_builder.py:28`, propagated by `source_identity()` and `--version`.
- Observation: the helper initially reported `1.0.0`; both VERSION files reported `1.0.0-rc.1`.
- Consequence: generated evidence did not identify the declared candidate version accurately.
- Resolution: the helper now reports `1.0.0-rc.1`; both VERSION files match. `tools/check_project.py:96–98` now checks all three values together.
- Evidence: `independent-resolution-verification.json`.

### R-02 — An inert deep directory tree escaped the audit traversal limits

**Status: resolved and verified.**

- Original location: `skills/skill-builder/scripts/skill_builder.py:347–374` in the initial reviewed helper.
- Observation: a 1,030-level empty-directory fixture triggered `RecursionError` even with `max_files=1`. Directories did not consume the file budget, and recursion had no depth limit. This was reproduced without executing any target code.
- Consequence: ordinary adversarial filesystem data could crash the supposedly bounded audit before a usable report was produced.
- Resolution: traversal now has an explicit directory-depth boundary of 128 and a separate global entry budget. A 140-level fixture returns incomplete coverage with an explicit `maximum_directory_depth_128` omission.
- Evidence: original reproduction in `independent-reproduction.json`; fixed-depth result in `independent-reproduction-followup.json`.

### R-03 — The first global entry-budget implementation undercounted prefetched names

**Status: resolved and verified.**

- Initial fix location: `skills/skill-builder/scripts/skill_builder.py:361–381` at helper SHA-256 `b98bd560973b989757349d75ec6659904a0f93ad6a82527217c198d7f395bc4c`.
- Observation: the helper collected directory entries before charging them to `entries_seen`, then recursed before charging prefetched siblings. An inert six-level fixture configured with `max_entries=6` caused 27 actual entries to be obtained from `os.scandir`, while the report said six.
- Consequence: the claimed enumeration/storage budget did not bound actual enumeration; wide nested directories could multiply retained work.
- Resolution: the global counter now advances when a name is obtained, before recursive processing, and no lookahead occurs after exhaustion. The same independent counting fixture now observes exactly six names, reports six, and marks incomplete coverage.
- Current location: `skills/skill-builder/scripts/skill_builder.py:361–380`.
- Evidence: before result in `independent-reproduction-followup.json`; after result in `independent-resolution-verification.json`.

### R-04 — A stale generated manifest could produce a successful package with an invalid payload manifest

**Status: resolved and verified; the original clean candidate did not contain the triggering reserved filename.**

- Original location: `tools/build_release.py:104–107`.
- Observation: if the input dictionary already contained `PACKAGE-MANIFEST.json`, its old bytes were hashed as payload and then replaced by the new generated manifest. `make_zip()` returned success even though the corresponding declared file hash did not match the written archive. A two-file inert fixture reproduced this.
- Consequence: rebuilding from extracted package material could create a misleading identity record and reintroduce the manifest self-reference problem that the documented identity design excludes.
- Resolution: `make_zip()` rejects this reserved input name before creating an output archive. Independent verification observed `ValueError` and no output file. A regression was also added at `tests/test_release.py:41–46`.
- Current location: `tools/build_release.py:104–106`.
- Evidence: before result in `independent-package-reproduction.json`; after result in `independent-resolution-verification.json`.

## Optional improvement

### E-01 — Narrow or enforce the environment-file exclusion claim

**Priority: nonblocking documentation/build-policy improvement.**

- Locations: `docs/architecture.md`, paragraph under “Repository and distributed skill”; `tools/build_release.py:23–29,60–74,133–142`.
- Observation: architecture documentation says build outputs exclude environment files. The packager excludes selected virtual-environment/cache directory names and top-level files through its allowlist, but recursively includes arbitrary regular files inside selected source directories. For example, a future `tools/.env` or `skills/skill-builder/.env` would be included. No such sensitive file was observed in the reviewed candidate, and this review did not place one in it.
- Action: either describe the existing narrower exclusion accurately, or add an explicit, reviewed deny policy for environment/credential files and a corresponding package inspection check. A policy should preserve any intentionally declared inert test fixtures.

## Preservation result relevant to the review

The uploaded source ZIP and the packaged knowledge-base ZIP were compared directly and were byte-for-byte identical, SHA-256 `9666202020c7a0c2b8fd66e6e738db2695572e79225bb565aebc687ddaabb204`. Independent `zipfile` inspection found 454 original members, 182 unique substantive-file manifest rows, an exact match between indexed and actual substantive members, 76,965,199 uncompressed substantive bytes, and no individual size/hash mismatches. This establishes source preservation, not instruction quality or live-host functionality.

The archived representation keeps original example/probe `SKILL.md` files out of the live runtime directory. No additional live runtime entrypoint was identified in the reviewed layout. The preserved source was read as data; no original target scripts, hooks, installers, or test suites were executed for this review.

## Final focused verification identity and limits

The final focused checks in `independent-resolution-verification.json` identify:

- Helper SHA-256: `71f7dc8ae9a67b3d0b19f5fdaaafe99441468653efab12147f54a4c24fcba31c`.
- Release builder SHA-256: `5cc98f10bbc7f9777a88b18374df6ca1d072f4a613f0bf2b791c2c5d2be9b9be`.

Reviewed material included the parent skill, creation/audit workflows, governance, host adapters, CLI contract, release-status/architecture/compatibility/security material, the helper, package builder, and the newly arrived project checker. The original validators and schemas were inspected for their trust and evidence boundaries. The implementation map and final evaluation/validation records arrived late in the assembly and were not independently assessed rule by rule here. No claim is made that a documentation URL proves current host behavior or that this review establishes native discovery, permission enforcement, a clean no-skill comparison, distribution rights, or final archive readiness.

Only the reviewed local helper/build functions were executed against reviewer-owned inert fixtures in unique analysis directories. Candidate files were not edited by this reviewer. Reproduction data remains outside the candidate. Later edits require the integrating agent's affected checks against the final identities.
