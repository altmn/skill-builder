# Release and publication

The public repository is `altmn/skill-builder`, maintained by Alex Allen, with default branch `master`. Changes use new feature branches and pull requests. Never merge or mirror the private preparation repository's Git history into this repository.

For a request to "get to production", follow [project instructions](../AGENTS.md#getting-to-production): publish a new versioned release, including for documentation-only changes, and update and verify existing installed copies without another confirmation. The validation, preservation, and package checks below still apply. Source-only work and local package preparation alone do not request production.

## First publication history

Export reviewed source without `.git`, initialize an independent Git database, and create one signed commit with no parents. Upload no original branches, tags, reflogs, bundles, object alternates or preparation commits. Rename the bootstrap feature branch to `master` without creating another commit. Existing reviews, failures, changelog entries and attribution stay as files. This hides earlier Git history, not the historical evidence intentionally retained in the snapshot.

Future fixes use public pull requests. Do not amend or force-push the public initial commit. Verify a fresh clone's refs and ancestry; old commit identifiers appearing in retained evidence do not mean their Git objects were uploaded.

## Verify and build

Use the reviewed pinned validation environment, or provision `requirements-validation.txt` only when authorized. Run:

```sh
python3 -I -B tools/check_project.py --require-validators
python3 -I -B -m unittest discover -s tests -v
python3 -I -B tools/check_git_inventory.py
python3 -I -B tools/check_workflow_impact.py
git diff --check
python3 -I -B tools/build_release.py --output ../skill-builder-build-1.0.0
```

Choose a new output directory with an existing parent outside selected source trees. The builder refuses existing output and never installs or publishes. It emits standalone, source and plugin archives, per-package manifests, SHA256SUMS and a detached build receipt. Inspect each archive's inventory and bytes. Only `-plugin.zip` is the OpenAI upload; keep archive hashes outside the archives they identify.

Review retained third-party terms and disclosure risks, and verify the frozen KB hash. Preserve failed evidence. If a frozen source cannot safely or legally be distributed, stop publication and resolve the issue without rewriting it.

## GitHub launch

Require successful `standard-library` and `optional-validators` CI, including a complete initial-snapshot impact record. Enable private vulnerability reporting and check its form. Verify the public website, support, privacy and terms pages. Protect `master` with PRs, signed commits, linear history, resolved conversations and required CI; protect `v*` tags against modification/deletion. No separate reviewer approval is required for solo maintenance.

Create a signed `v1.0.0` tag on the reviewed public commit and a stable release attaching the three archives, SHA256SUMS and build receipt. Record actual commit, tag, URLs and checks in a detached publication receipt. Do not rebuild archives to insert their own final hashes or relabel historical evidence as current passes.

Native acceptance of the exact archives remains unestablished without fresh evidence. This release performs no live skill installation, paid evaluation, portal upload or directory publication. Follow [OpenAI preparation](chatgpt-submission.md).
