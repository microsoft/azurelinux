# Fork-PR checks for secret-bearing ADO pipelines

## Problem

We want pull requests from **forks** of this repository to run a pre-merge
check that scans the contributed sources and builds the changed packages in
Koji. That check is an Azure DevOps (ADO) pipeline that holds a **service
connection (SC)** to Control Tower — the service that drives the scan and the
package build — and the build runs in **production Koji**.

A fork PR can rewrite any file under the PR HEAD: pipeline YAML, shell
snippets, `requirements.txt`, helper scripts, and the package spec files. So
"run the check on fork PRs" means "run attacker-influenceable content against a
secret-bearing pipeline whose build executes in production." This document
states the options and their security trade-offs so the team can decide which
to adopt. No option is adopted yet — these are candidates for that decision.

## Threat model

Two distinct threats, both in scope:

- **Token exfiltration.** If fork-controlled code runs in a job that holds the
  SC token, the attacker gets arbitrary calls under that identity. That job can
  also attempt to reach other secrets in the pipeline's ADO project and
  enumerate other builds and artifacts there. The defense is to make it
  structurally impossible for fork-controlled YAML/scripts to execute in the
  same job that holds the token.
- **Production Koji code execution.** The check builds the PR's package in
  production Koji, which executes the PR's spec scriptlets (`%prep`, `%build`,
  `%install`, …) in production as the check's intended function. This is a
  property of *what the check does*, not of how it authenticates.

## How to read the comparison

> None of the authentication patterns below mitigates execution of untrusted
> spec code in production Koji. That risk is cross-cutting and must be contained
> on the Koji side (isolated/disposable build target, no prod inheritance, no
> signing) — a separate problem to solve with the Koji team, out of scope for
> this document. Until it is contained, the human who approves a run (or the
> merge) by reviewing the exact commit is the only gatekeeper against malicious
> spec execution.

Every option that builds runs the PR's spec in production Koji, so the row
entries below note only the token/isolation trade-off; the Koji risk above
applies to all of them equally.

The internal-template and notifier options can additionally require a reviewer
to approve each run through an ADO Environment check. That approval happens
**outside GitHub**, via an ADO email notification; surfacing the approval prompt
in the PR itself would take extra work.

| Option | Security | Maintainer convenience | Implementation | Pre-merge fork feedback |
| --- | --- | --- | --- | --- |
| [Comment-triggered `/azp run`](option-comment-trigger.md) | The SC token is present in a job that runs PR-HEAD YAML and scripts; safety depends on the commenter reviewing that exact commit | A GitHub **Write+** collaborator must comment `/azp run` for each commit they want checked | Single pipeline; PR status reported natively. **~2–3 days** | Yes, gated on the comment |
| [Internal-template pattern](option-internal-template.md) | SC token is issued only against a template the fork cannot modify; the trust boundary is enforced by ADO at token-issue time | Runs automatically on fork PRs once configured | Private ADO template repo + SC checks; the isolated-project variant adds a dedicated project to own (the shared-project variant is cheaper but widens blast radius). **~2 weeks** | Yes |
| [Notifier → trusted-internal split](option-notifier-split.md) | The SC token never enters a fork-controlled job; the privileged stage runs trusted-branch code only | Runs automatically if the completion trigger fires for fork runs (verify — see the option); posting status onto the PR requires a GitHub App | Two pipelines + a completion trigger, plus a GitHub App to report status. **2–3 weeks** | Yes |
| [GitHub Actions + OIDC](option-github-actions-oidc.md) *(not available)* | Disallowed for this scenario: OIDC into a production Entra tenant is [blocked by default, exception-only, and not usable from pull requests](https://eng.ms/docs/more/github-inside-microsoft/troubleshoot/oidc) ([Open Source Security policy](https://docs.opensource.microsoft.com/security/azure)) | — | N/A | No |
| [No fork PRs](option-no-fork-prs.md) | No SC token is ever issued to a fork build; no automatic prod-Koji build on fork code (the build still runs the PR's spec at merge-queue time, gated by maintainer merge approval) | Fork PRs get no check; a maintainer pushes the branch upstream or relies on the merge-queue run | No new ADO or GitHub infrastructure. N/A | No |

## Reference material

Related (this repo):

- ADO pipeline conventions:
  [`ado-pipeline.instructions.md`](../../../.github/instructions/ado-pipeline.instructions.md)
- Fork-PR policy (operative rule):
  [`ado-pr-check-fork-policy.instructions.md`](../../../.github/instructions/ado-pr-check-fork-policy.instructions.md)
- Adjacent scope — residual risks for pipelines **without** secrets access
  (out of scope of this policy):
  [cross-cutting-non-secret-risks.md](cross-cutting-non-secret-risks.md)

External references:

- Microsoft Open Source Security — Actions & Azure:
  <https://docs.opensource.microsoft.com/security/azure>
- Microsoft Open Source Security TSG — Securing and Evaluating GitHub Actions:
  <https://docs.opensource.microsoft.com/security/tsg/actions>
- GitHub inside Microsoft — OIDC workload identity federation:
  <https://eng.ms/docs/more/github-inside-microsoft/troubleshoot/oidc>
- GitHub — Security hardening / secure use reference:
  <https://docs.github.com/en/actions/reference/security/secure-use>
