---
applyTo: ".github/workflows/ado/*.yml,.github/workflows/ado/templates/*.yml,.github/workflows/scripts/**"
description: "Policy: GitHub PR fork builds for ADO pipelines under .github/workflows/ado/. Defines what is allowed, what is forbidden, and how to enforce it. Long-form rationale lives in docs/ado-pipelines-fork-pr-security.md."
---

# Policy: GitHub PR fork builds for ADO pipelines

This policy governs how ADO pipelines under `.github/workflows/ado/` may
be configured with respect to GitHub pull requests originating from
**forks** of this repository. It is the operative rule. Long-form
rationale, threat analysis, and design alternatives live in
[`docs/ado-pipelines-fork-pr-security.md`](../../docs/ado-pipelines-fork-pr-security.md).

> If anything in this policy conflicts with what the user is asking for,
> **stop and ask** rather than guessing.

## Scope

- **In scope:** ADO YAML pipelines under `.github/workflows/ado/`
  (wrappers and raw stages templates) and their helper scripts under
  `.github/workflows/scripts/`.
- **Out of scope (today):**
  - GitHub Actions workflows under `.github/workflows/*.yml`. They have
    a different security model and are not addressed here.
  - ADO pipelines **without secrets access** (see definition below).
    Authors of such pipelines should still read the residual-risk
    section in
    [`docs/ado-pipelines-fork-pr-security.md`](../../docs/ado-pipelines-fork-pr-security.md#residual-risks-of-non-secret-ado-pipelines-on-fork-prs)
    before opting in to fork PR builds.

## Definitions

- **Fork PR** -- a GitHub pull request whose source branch lives in a
  fork of this repository (i.e. not pushed to a branch of the upstream
  repository).
- **Upstream PR** -- a pull request whose source branch lives in the
  upstream repository itself.
- **Merge queue commit** -- a commit produced by the GitHub merge queue
  on a `gh-readonly-queue/<base>/pr-<n>-<sha>` branch.
- **Secrets access** -- an ADO pipeline has secrets access if **any**
  of the following are true:
  - It uses a service connection (e.g. `azureSubscription:`,
    `serviceConnection:` inputs on tasks such as `AzureCLI@2`).
  - It binds a variable group via `variables: - group: <name>`.
  - It downloads a secure file via `DownloadSecureFile@1` (or similar).
  - It runs in an ADO Environment that has approvals or secret-bearing
    resources attached.
  - It otherwise has any pipeline-level mechanism through which a
    credential, token, or sensitive value reaches the running job.

## Normative rule

ADO pipelines with secrets access **MUST NOT** be configured to build
fork PRs.

**Why (brief):** a fork PR can rewrite any file in the PR HEAD,
including pipeline YAML, shell snippets, and helper scripts. If that
code runs in a job bound to a service connection or a secret-bearing
variable group, the attacker gets arbitrary code execution under the
pipeline's identity and can call any API that identity is permitted to
call. The full threat model and the design options that *could*
mitigate it (internal-template pattern in shared vs. isolated ADO
projects) are documented in
[`docs/ado-pipelines-fork-pr-security.md`](../../docs/ado-pipelines-fork-pr-security.md).

## Hosted agents only

All ADO pipelines under `.github/workflows/ado/` **MUST** run on
hosted agent pools -- either Microsoft-hosted agents or **1ES Hosted
Pools** (the internal Microsoft hosted-pool offering defined in Azure).
Self-hosted agent pools are forbidden.

**Why:** hosted pools guarantee a clean worker for each build. This
eliminates the risk of one workload leaking state to another via
caches, modified dotfiles, planted binaries on `PATH`, or modified
language-toolchain caches. The self-hosted-pool poisoning class of
attack documented in
[`docs/ado-pipelines-fork-pr-security.md`](../../docs/ado-pipelines-fork-pr-security.md) does not
apply when this rule is followed.

## Network class (R0 vs R1)

When a pipeline executes any PR-derived content (which includes
upstream PRs and merge-queue commits), prefer the **lowest-trust
network class** the workload can run on (e.g. `R0` over `R1`). The
chosen `LinuxHostVersion.Network` value in the wrapper's OneBranch
`featureFlags` is a security-relevant decision and should be
explicitly justified by the wrapper author. Higher-trust network
classes increase the surface available to attacker-controlled code if
any of the other rules are ever bypassed.

## CODEOWNERS coverage

`.github/workflows/ado/**` and `.github/workflows/scripts/**` **MUST**
have CODEOWNERS entries that require maintainer review on any change.

**Why:** the wrapper, the raw stages template, and the helper scripts
are all part of the trust boundary. A merged malicious change to any
of them can weaken every other control in this policy.

## Enforcement

To comply with the normative rule, configure the ADO pipeline as
follows:

1. **GitHub PR trigger settings** (ADO pipeline UI -> Triggers -> Pull
   request validation, **not** YAML):
   - "Build pull requests from forks of this repository" -> **OFF**.
   - "Make secrets available to builds of forks" -> **OFF** (defense
     in depth: this must be off even if the previous toggle is also
     off, in case the previous toggle is ever flipped by mistake).
2. **GitHub branch policy / merge queue** (GitHub repo settings):
   - The pipeline's check is required only on PRs from upstream
     branches and on merge-queue commits.
3. **YAML triggers** stay as `trigger: none` / `pr: none` per the
   existing [ADO pipeline instructions](ado-pipeline.instructions.md);
   PR firing is configured in ADO, not in YAML.

## Reviewer checklist (apply on every change to an ADO pipeline)

Tick these off before approving:

- [ ] Pipeline still runs on a hosted pool (Microsoft-hosted or 1ES
      Hosted Pool). No self-hosted pool introduced.
- [ ] The ADO pipeline's GitHub PR trigger does **not** enable fork PR
      builds (verify in the ADO UI; YAML cannot guarantee this).
- [ ] If the change adds or modifies a service connection, variable
      group, secure file, or secret-bearing environment, the policy
      author confirms the pipeline is still upstream-PR-only.
- [ ] PR-derived strings (branch names, commit SHAs, PR numbers,
      filenames produced by `git diff`, etc.) are sanitized /
      regex-validated before being used in shell, file paths, or HTTP
      calls.
- [ ] CODEOWNERS still covers the modified files.
- [ ] Network class (`LinuxHostVersion.Network`) is no higher-trust
      than the workload requires.

## Exceptions

There are **no standing exceptions** to the normative rule today. A
future exception (i.e. allowing a specific secret-bearing ADO pipeline
to build fork PRs) requires:

1. Implementations of at minimum the **internal-template
   pattern in an isolated ADO project** (Variant B in
   [`docs/ado-pipelines-fork-pr-security.md`](../../docs/ado-pipelines-fork-pr-security.md#variant-b--isolated-ado-project)).
2. Discussion and explicit approval by project maintainers.
3. Documentation of the approved exception in this file (or a
   sibling).

Until such an exception is approved and documented, the rule is
absolute.
