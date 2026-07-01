# Option: GitHub Actions + OIDC — disallowed for this scenario

> ↩ [Fork-PR options index](README.md) · [Threat model](README.md#threat-model)

A natural-looking design is to do the untrusted work in a GitHub Actions
`pull_request` workflow (no secrets) and the privileged Control Tower call in a
`pull_request_target` / `workflow_run` workflow that federates to an Azure
identity via OIDC — no stored secret, native GitHub check status.

**This option is disallowed for our scenario.** It is documented here so the
comparison is complete and the reasoning is on record.

## Why it is disallowed

Our privileged identity lives in a **production Entra tenant**. Microsoft
policy governs connecting GitHub to such tenants:

- **OIDC into production Entra tenants (AME/PME/Torus) is blocked by default**
  and is exception-only. Teams are directed to use Azure Pipelines instead.
- **Even with an approved exception, OIDC cannot be used from pull requests.**
  The only supported federated-credential scenario is via GitHub Environments
  restricted to protected branches; PR-triggered federation is not permitted.
- Federated credentials to privileged tenants are rejected outright when they
  originate from the Microsoft open source enterprise.

Because the entire goal is **pre-merge validation of fork pull requests**, and
OIDC to the production tenant is unavailable from pull requests even under an
exception, this design cannot meet the requirement. Connecting a repository to
a privileged principal in a production tenant is, separately, strongly
discouraged.

This is a restriction on **connecting to a production tenant from pull-request
GitHub Actions** — not a statement that OIDC is bad in general.

## References

- GitHub inside Microsoft — Configure OIDC Workload Identity Federation for
  GitHub (blocked-by-default policy, exception path, protected-environments-only
  requirement):
  <https://eng.ms/docs/more/github-inside-microsoft/troubleshoot/oidc>
- Microsoft Open Source Security — Actions & Azure (connecting repositories to
  privileged production tenants; use Azure Pipelines for production builds):
  <https://docs.opensource.microsoft.com/security/azure>
- Microsoft Open Source Security TSG — Securing and Evaluating GitHub Actions:
  <https://docs.opensource.microsoft.com/security/tsg/actions>
- GitHub — secure use reference (`pull_request_target` untrusted-checkout
  risks):
  <https://docs.github.com/en/actions/reference/security/secure-use>
