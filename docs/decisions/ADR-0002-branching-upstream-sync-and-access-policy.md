---
title: "ADR-0002: Branching, Upstream Sync, Contribution, and Access Policy"
status: active
source_of_truth: github
branch: dev
last_reviewed: 2026-04-27
drive_copy: none
source_inputs:
  - GitHub Issue #7
  - docs/decisions/ADR-0001-project-workflow-source-of-truth.md
---

# ADR-0002: Branching, Upstream Sync, Contribution, and Access Policy

## Status

Accepted.

## Context

ProtagonistOS is a downstream fork of Azure Linux 3.0, not a mirror. The project needs a branch model that keeps Microsoft Azure Linux history distinct from downstream ProtagonistOS work, supports clean contribution-back branches, and prevents exploratory work from becoming confused with stable project state.

Before this decision, `sandbox` was used as the project integration branch. That was acceptable during early exploration, but it is too loose for ongoing downstream distro engineering.

## Decision

Use this branch model:

```text
upstream/3.0          Microsoft Azure Linux upstream branch, fetch-only reference
origin/3.0            pristine Azure Linux 3.0 mirror, no ProtagonistOS commits
origin/main           stable ProtagonistOS branch
origin/dev            active ProtagonistOS integration branch
codex/<task>          Codex-authored feature or work branches
feature/<task>        human-authored feature or work branches
sync/upstream-<date>  temporary upstream synchronization branches
upstream-contrib/<x>  clean contribution branches based on upstream/3.0
release/<version>     optional future release stabilization branches
```

Branch rules:

- `origin/3.0` must remain pristine and must not contain ProtagonistOS commits.
- `origin/dev` is the integration branch for active ProtagonistOS work.
- `origin/main` is stable project state and should advance from reviewed `dev` changes.
- New ProtagonistOS work branches must branch from `dev`, not from `main` or `3.0`.
- Temporary upstream sync branches must merge from `3.0` into `dev` through a reviewable pull request.
- Long-lived ProtagonistOS branches must not be rebased after publication; use merge commits for upstream sync auditability.
- `sandbox` is legacy and should not receive new project work.

## Upstream Sync Workflow

Use this process to pull Microsoft Azure Linux changes into ProtagonistOS:

```bash
git fetch upstream
git checkout 3.0
git merge --ff-only upstream/3.0
git push origin 3.0

git checkout dev
git checkout -b sync/upstream-3.0-YYYY-MM-DD
git merge --no-ff 3.0
# resolve conflicts
# run relevant validation
# open PR: sync/upstream-3.0-YYYY-MM-DD -> dev
```

Sync requirements:

- Keep upstream Microsoft changes separate from downstream ProtagonistOS changes.
- Capture conflict resolution notes in the sync PR.
- Call out any sync changes under `SPECS/`, `SPECS-EXTENDED/`, `SPECS-SIGNED/`, or `toolkit/`.
- Do not mix upstream syncs into feature PRs.
- Treat conflicts in intentionally changed downstream areas as project decisions, especially Mesa, branding packages, image configs, and docs.

Operator checklist for each sync:

- Fetch `upstream`.
- Fast-forward local and remote `3.0`.
- Create a dated `sync/upstream-3.0-YYYY-MM-DD` branch from `dev`.
- Merge `3.0` into the sync branch with a merge commit.
- Resolve conflicts and document them in the PR.
- Run validation appropriate to the files touched.
- Merge the sync PR into `dev`.

## Contribution-Back Workflow

Never open upstream Azure Linux PRs from `dev`, `main`, `sandbox`, or ProtagonistOS feature branches.

For upstream-appropriate fixes:

```bash
git fetch upstream
git checkout -b upstream-contrib/<topic> upstream/3.0
# cherry-pick or recreate only the upstream-relevant fix
# open PR to microsoft/azurelinux:3.0
```

Good upstream candidates include generic Azure Linux fixes, packaging correctness fixes, build reproducibility fixes, security fixes, and toolkit fixes that are not downstream-specific.

Do not include ProtagonistOS branding, dashboard work, COSMIC product decisions, downstream image composition, or private workflow documentation in upstream contribution branches.

Track upstream PR links from the originating ProtagonistOS issue or PR. When an upstream PR is accepted, bring it back through the normal upstream sync workflow instead of manually duplicating history.

## Repository Access Policy

Protect `main`, `dev`, and `3.0` once the branches exist.

Required defaults:

- Require pull requests for protected branches.
- Disallow force pushes on protected branches.
- Disallow deletion of protected branches.
- Require status checks before merge once checks are stable enough to be meaningful.
- Require branches to be up to date before merge where practical.
- Keep direct write/admin access limited to trusted users and apps.
- Keep `GITHUB_TOKEN` read-only by default unless a workflow needs write access.
- Ensure Pages deployment can publish only reviewed branch content.
- Do not expose secrets to pull requests from forks.
- Use protected environments for publishing when dashboard deployment needs approval.
- Treat `upstream` as fetch-only operationally.

Signed commits may be required later if the workflow supports them without blocking Codex-authored work.

## Consequences

The project now has distinct places for upstream baseline, active integration, stable downstream state, task branches, upstream sync branches, and upstream contribution branches.

This adds process overhead, but it prevents downstream ProtagonistOS engineering from contaminating the Azure Linux mirror branch and gives future syncs and contribution-back work a clear audit trail.
