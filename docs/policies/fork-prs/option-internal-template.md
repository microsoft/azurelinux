# Option: internal-template pattern

> ↩ [Fork-PR options index](README.md) · [Threat model](README.md#threat-model)

Move the trust boundary out of the public GitHub repo and into ADO
configuration plus a private ADO-hosted git repo that the attacker cannot
submit PRs against. The SC issues a token only when the compiled pipeline
extends that private template, so no amount of YAML rewriting in a fork PR can
move the boundary.

## When to choose

- You want fork PRs to run automatically (no per-commit human action), **and**
- you can own a private ADO template repo and the SC hardening it requires.

Pick the **isolated-project** variant when the SC reaches production-adjacent
resources; pick the **shared-project** variant only under the acceptability
conditions listed below.

## How it works

This design requires **"Make secrets available to builds of forks" = ON** so
the SC token can be offered to a fork PR build at all. On its own that is
unsafe; the pieces below are what make it safe — the token is offered but
issued only against a template the fork cannot influence.

Required pieces:

1. **Private template repo in ADO** holding the entire raw-stages template and
   any helper scripts. Branch-protected (no force-push, required reviewers from
   a small trusted group); a pinned ref is referenced by the SC's "Required
   template" check.
2. **Wrapper pipeline in the GitHub repo** under
   [`.github/workflows/ado/`](../../../.github/workflows/ado/), reduced to:
   - `trigger: none` / `pr: none` (PR firing configured in ADO);
   - `resources.repositories` for the OneBranch governed templates **and** the
     private template repo;
   - `extends:` the private template with no attacker-controlled parameters;
   - no `stages:` / `jobs:` / `steps:` / `script:` of its own.
3. **Service Connection hardening** (Project Settings → Service Connections →
   the SC → Approvals and checks):
   - **Required template check** pinned to the private repo + path + ref,
     evaluated against the compiled YAML at token-issue time. A fork PR that
     extends a different template never receives a token.
   - **Branch control** restricted to the protected base branches. Fork PR runs
     use `refs/pull/N/merge` and are rejected before a token is issued.
   - **Pipeline permissions** granted to this one pipeline; "Open access" off.
4. **Variable group(s) (VG)** scoped the same way: pipeline-permissions limited
   to this pipeline; "Open access" off.
5. **Federated credential subject** on the Entra app set exactly to
   `sc://<org>/<project>/<sc-name>` (no wildcards).
6. **Template content rules** — as load-bearing as the SC config:
   - the template MUST NOT execute any code from the PR HEAD checkout (no
     `pip install -r` of a PR `requirements.txt`, no `python3 <pr-path>`, no
     `bash <pr-path>`, no `go install …@$(…)` with a PR-derived version);
   - helper scripts live in the private template repo, not the GitHub repo;
   - PR-supplied data enters only via ADO predefined variables and is
     regex-validated before use (SHAs `^[0-9a-f]{40}$`; branch names
     `^[A-Za-z0-9._/-]{1,255}$`; `git diff` component names
     `^[a-z0-9._+-]{1,128}$`); any validation failure rejects the run;
   - all tool versions pinned (container image by digest); only
     `GovernedTemplates@refs/heads/main` is exempt.
7. **GitHub-side hygiene**: CODEOWNERS over `.github/workflows/ado/**` and
   `.github/workflows/scripts/**`, plus branch protection with required
   reviews. This does not affect SC security but prevents the wrapper from
   being silently weakened through a merged PR.

## Security posture

Token isolation is strong: the "Required template" check binds the SC to a
template the fork cannot modify, so the token is never issued to a
fork-controlled compilation. **Production Koji is not addressed by this option**
— the build it authorizes still runs the PR's spec in prod Koji; Koji-side
containment is tracked separately (see the
[threat model](README.md#threat-model)). The remaining exposure is
project-topology-dependent and differs between the two variants below.

## Variant A — shared ADO project

Host the template repo, pipeline, SC, and variable group in an existing ADO
project that also holds other pipelines and resources.

With the SC scoped to this pipeline and "Required template" + branch control
configured, the **direct** path to the SC token is the same as in the isolated
case. The residual exposure is everything *else* the shared project grants:

- **Broadly-scoped Build Service identity.** The pipeline runs as
  `<Project> Build Service (<org>)`, which in a shared project often has read
  (sometimes contribute) on many repos, feeds, wikis, and work items. The
  "Required template" check stops the SC token from being issued but does not
  stop other tasks in the wrapper from running under the build identity — so a
  fork PR can add a `checkout:` or `DownloadPipelineArtifact@2` and read
  anything that identity can read.
- **Shared self-hosted pool poisoning.** Self-hosted pools are forbidden by
  policy (hosted pools only); noted for completeness, a fork build on a shared
  self-hosted pool could poison the next trusted pipeline — see
  [cross-cutting risks](cross-cutting-non-secret-risks.md#residual-risks-of-non-secret-ado-pipelines-on-fork-prs).
- **Cross-pipeline artifact reads**, **configuration drift** toward "Open
  access" by other admins, a **larger administrative blast radius** (every
  project admin can weaken the controls), and **noisier audit logs**.

Acceptable **only if all** hold: the pipeline runs on Microsoft-hosted agents
(or a pool dedicated to it alone); the Build Service identity has been audited
and can read nothing you would mind a fork reading; project-admin membership is
small and trusted; no SC/VG in the project is set to "Open access". If any of
these is shaky, use Variant B.

## Variant B — isolated ADO project

Create a new ADO project whose only purpose is to host this pipeline, its
private template repo, the SC, the variable group, and nothing else.

This eliminates what the shared variant cannot:

- the Build Service identity can read almost nothing — lateral reads of
  other repos / feeds / artifacts are structurally impossible;
- no shared self-hosted pool to poison (hosted agents only, per policy);
- neighboring SC/VG drift cannot affect this pipeline — there are no
  neighbors;
- administrative blast radius is limited to this project's small admin list;
- the audit trail is high-signal: every event relates to this pipeline.

Residual exposure that remains: the wrapper still lives in the public repo and
can be weakened via a merged malicious PR (CODEOWNERS + branch protection +
review discipline mitigate it); whoever administers the isolated project can
disable template-repo branch protection; a second federated-credential subject
on the Entra app would break isolation (audit periodically). Setting up and
owning a dedicated project is a real one-time and ongoing cost.

## Trade-offs

| Risk surface | Shared project (A) | Isolated project (B) |
| --- | --- | --- |
| Direct SC token theft from a fork PR | Blocked by "Required template" + branch control | Blocked by "Required template" + branch control |
| Build identity reads other repos / feeds / artifacts | Possible — depends on project-wide permissions | Near-zero — nothing else exists in the project |
| Self-hosted pool poisoning | Possible if the pool is shared | Eliminated (single consumer; hosted agents) |
| Misconfigured neighbor SC/VG | Possible via drift or other admins | Not applicable — no neighbors |
| Administrative blast radius | Shared-project admins (often many) | Isolated-project admins (small) |
| Wrapper replaced via merged malicious PR | Same in both — mitigated by CODEOWNERS + branch protection | Same in both — mitigated by CODEOWNERS + branch protection |
| Federated-credential subject drift | Same in both — mitigated by periodic Entra audit | Same in both — mitigated by periodic Entra audit |
| Operational cost | Low (reuse existing project) | Higher one-time setup; small ongoing overhead |

## Open questions

- Does an isolated project already exist for this workload, or is one to be
  stood up?
- Which group owns the private template repo and its branch protection?
- Does the Koji build step satisfy the template content rules (no execution of
  PR-checkout code outside the build itself)?
