---
applyTo: ".github/workflows/ado/*.yml,.github/workflows/ado/templates/**/*.yml,scripts/ci/**"
description: "Policy: how ADO pipelines under .github/workflows/ado/ handle GitHub fork pull requests — what is allowed, what is forbidden, and how it is enforced."
---

# Policy: GitHub PR fork builds for ADO pipelines

The operative rule for how ADO pipelines under `.github/workflows/ado/` run
against GitHub pull requests from **forks** of this repository.

> If anything in this policy conflicts with what the user is asking for,
> **stop and ask** rather than guessing.

## Scope

- **In scope:** ADO YAML pipelines under `.github/workflows/ado/` (wrappers and
  raw stages templates) and their helper scripts under
  `scripts/ci/`.
- **Out of scope:** GitHub Actions workflows under `.github/workflows/*.yml`
  (different security model).

## Definitions

- **Fork PR** — a pull request whose source branch lives in a fork, not in a
  branch of the upstream repository.
- **Merge-queue commit** — a commit on a `gh-readonly-queue/<base>/pr-<n>-<sha>`
  branch produced by the GitHub merge queue.
- **Privileged check** — a pipeline with **secrets access**: it uses a service
  connection (e.g. `azureSubscription:` / `serviceConnection:`), binds a
  secret-bearing variable group, downloads a secure file, or runs in a
  secret-bearing ADO Environment — i.e. a credential or token reaches the job.
  Currently the source-upload + package-build check is the privileged one.

## Rules

Contributions — including from internal developers — arrive as **fork PRs**.

1. **Non-privileged checks** build fork PRs automatically.
2. **Privileged checks MUST NOT build fork PRs automatically.** A privileged
   check builds a fork PR only when an authorized reviewer triggers it **per
   commit** with an Azure Pipelines `/azp run` comment. This applies to **every**
   fork PR, including those opened by team members.
   - On the privileged pipeline, "Make secrets available to builds of forks" is
     ON **and** "Require a team member's comment before building a pull request"
     is ON, so no fork build receives secrets without an explicit per-commit
     comment.
   - Authorization is currently any **Write+** collaborator; the project is
     narrowing Write+ to maintainers so this becomes maintainer-only.
3. **Hosted agents only** — Microsoft-hosted agents or **1ES Hosted Pools**.
   Self-hosted agent pools are forbidden.
4. **CODEOWNERS** MUST cover `.github/workflows/ado/**` and
   `scripts/ci/**`, requiring maintainer review.
5. **PR-derived input** (branch names, commit SHAs, PR numbers, `git diff`
   filenames) MUST be regex-validated before use in shell, file paths, or HTTP
   calls.
6. **Secrets** are passed via the task `env:` block, never inline `$(...)`.
7. **Network class** — prefer the lowest-trust `LinuxHostVersion.Network` the
   workload allows; a higher-trust class MUST be justified by the wrapper author.
8. **YAML triggers** stay `trigger: none` / `pr: none`; PR firing is configured
   in ADO, per the [ADO pipeline instructions](ado-pipeline.instructions.md).

## Reviewer checklist (every change to an ADO pipeline)

- [ ] Runs on a hosted pool (no self-hosted pool introduced).
- [ ] No privileged check builds fork PRs automatically — it is comment-gated
      per commit (verify in the ADO UI; YAML cannot guarantee this).
- [ ] "Make secrets available to builds of forks" is enabled **only** on the
      privileged pipeline, with the comment requirement ON.
- [ ] PR-derived strings are sanitized / regex-validated.
- [ ] CODEOWNERS covers the modified files.
- [ ] Secrets pass via `env:`; network class is no higher-trust than required.
