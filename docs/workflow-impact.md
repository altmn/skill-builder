# Review the effect of every improvement on create and audit

The repository's AGENTS.md requires this review at planning and delivery. The
failure to prevent is improving the builder itself while overlooking what it
teaches, generates or assesses for another skill. This is repository governance,
not a new skill-format requirement or an addition to the frozen 99-rule catalog.

For each workflow, decide `updated` or `no_change_needed` independently. Identify
the failure addressed, concrete downstream owners, and verification. Examine
the command procedure, helper output, templates, shared resources, target-case
evaluation, host adapters, documentation and packaged runtime. A shared helper
may propagate an improvement without edits to both command files. Conversely,
an index link or a passing builder test does not prove either subject workflow.

When behavior changes, verify relevant outcomes on other skills and test the
runtime package when distribution matters. Include allowed/denied cases where
effects change. Use proportionate checks: documentation-only work need not run
a costly native panel. Preserve unavailable/failed/unrun evidence and state the
claim it blocks. This policy authorizes no additional installation, network,
model spend, publication or other effects beyond the current task.

## Required append-only record

Copy [the template](templates/workflow-impact.json.template) to a new named file
under `docs/change-impact/`. Replace placeholders and list exact repository paths
in `reviewed_paths`, including additions/deletions and retained evidence. Cover
all intended changes; multiple fresh records may divide the scope. Keep both
create and audit entries even if neither needs a functional change.

Each decision needs a concrete reason (at least 20 characters, no placeholders),
existing downstream owner paths and actual verification status. `updated` needs
an owner in the reviewed paths. A `passed` verification needs commands and
existing evidence files. Other statuses require a reason and consequence; they
do not become passes or waive release gates. The template is a companion review
format, not one of the original version-2 evidence schemas.

Stage files and run:

```sh
python3 -I -B tools/check_workflow_impact.py
```

This reads **staged bytes**, including the new record. Untracked and unstaged
edits are not reviewed as part of the commit. Run the separate Git inventory
check when preparing source releases. After committing, review the branch with
`python3 -I -B tools/check_workflow_impact.py --base master`.

The checker requires a newly added record covering each changed file; an old
record cannot silently carry forward. Modifying or deleting an old impact
record is refused; add a dated follow-up instead. It reads only Git objects and
never executes owners, commands or evidence. Records are bounded to 1 MiB.
Exit 0 means review structure/coverage is complete, 1 means uncovered paths,
and 2 means invalid records or unavailable Git inputs. Inspect the returned
unresolved verification separately; structural success is not release approval.

## CI and review responsibilities

CI uses the PR merge base or push's before revision. New-branch pushes and manual
runs check the latest commit; root commits compare against the empty tree.
The PR check covers the complete branch range. The local staged check remains
mandatory for each commit. Full history is checked out; missing required objects
block rather than trigger a fetch from this checker.

The PR template makes the record visible to reviewers. Automation establishes
record freshness, exact path coverage and required decisions/references. It
cannot prove that a no-change reason is correct, that tests really ran, or that
a language model follows an instruction. Review those claims against evidence.
No branch protection, account setting or Git hook is installed by this policy;
required remote status enforcement remains a repository-owner setting.

## Dependency update pull requests

Dependabot proposals need the same reasoned create/audit review as other changes. A missing record is a review-policy failure, even when the dependency test job passes; rerunning unchanged proposals cannot supply the assessment. Review the exact upstream version and execution changes, test the candidate dependency set, and add a fresh record before merging. Do not generate a blanket passing review for every future dependency version or exempt bot-authored changes.

When related proposals affect the same CI or dependency files, a maintainer may apply their exact version bumps together in a reviewed companion PR. Identify the original proposals and retain their failed evidence. After the companion passes required CI and merges, close the superseded proposals as implemented, rather than describing their original runs as successful.

CI runs for every pull request, on master pushes, and on manual dispatch. Feature branch pushes and tag pushes do not start a duplicate run of the same source. Dependabot groups future proposals by ecosystem; grouping does not waive this review or required tests. Published release archives retain their recorded identities until a separately versioned release is prepared.
