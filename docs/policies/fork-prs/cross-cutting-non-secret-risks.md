# Cross-cutting: non-secret pipelines on fork PRs

> ↩ [Fork-PR options index](README.md) · [Threat model](README.md#threat-model)

This policy restricts **ADO pipelines with secrets access**. A pipeline that
has *no* service connection, *no* secret-bearing variable group, *no* secure
file, and *no* secret-bearing environment is out of scope and may be configured
to build fork PRs. Such a pipeline still poses residual risks that its author
should weigh before opting in — a secrets-free pipeline is not a risk-free one.

## Residual risks of non-secret ADO pipelines on fork PRs

1. **Parallelism abuse / queue starvation.** A fork PR can trigger arbitrary
   builds in the project's hosted-pool quota. Sustained fork-PR traffic can
   delay legitimate builds — a low-grade denial of service against CI.
2. **Internal-network probing.** ADO hosted pools (including 1ES Hosted Pools)
   often run on Microsoft-internal network classes with reachability to
   internal services not exposed publicly. A fork PR running arbitrary code on
   such an agent can probe and fingerprint that network with no credentials of
   its own.
3. **Internal package-feed and registry abuse.** Hosted agents are typically
   pre-authenticated to internal Go proxies, pip indexes, MCR, and similar
   feeds. A fork PR can issue arbitrary queries/downloads against these as the
   agent identity, logged as legitimate corporate traffic and hard to
   attribute.
4. **Cross-pipeline reads via the Build Service identity.** The pipeline runs
   as the project's Build Service account. Anything that identity can read in
   the project (other repos, feeds, wikis, work items, other pipelines'
   artifacts) is reachable by a fork build that adds the appropriate tasks.
5. **Log disclosure of internal metadata.** Build logs frequently include
   internal hostnames, IP ranges, agent image versions, and MCR tags that an
   attacker would otherwise have to guess. Fork PR build logs are visible to
   the PR author.
6. **Shared self-hosted pool poisoning.** *Not applicable when the hosted-pool
   rule is followed*, but documented for completeness: a fork PR on a shared
   self-hosted pool can leave poisoned caches, modified dotfiles, or planted
   binaries that the next trusted pipeline on that pool picks up.

These risks apply regardless of whether the pipeline holds secrets. The default
recommendation for any new non-secret ADO pipeline is to run fork PRs only
after the author has consciously assessed the items above and decided the value
of pre-merge fork feedback is worth them; when in doubt, default to
upstream-only.
