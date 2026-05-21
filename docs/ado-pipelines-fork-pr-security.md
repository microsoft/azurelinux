# Securing ADO PR-check pipelines against fork PRs

This document is the long-form rationale for the project's fork-PR policy
(see [`ado-pr-check-fork-policy.instructions.md`](../.github/instructions/ado-pr-check-fork-policy.instructions.md)).
It explains how an ADO pipeline under [`.github/workflows/ado/`](../.github/workflows/ado/) that has
**secrets access** (any service connection, secret-bearing variable group,
secure file, or environment with secrets) could be made safe to run as a
GitHub PR check / merge queue workload **when the PR may originate from an
attacker-controlled fork** — and why the project today defaults to *not*
running fork PRs against such pipelines at all.

The doc focuses on a single architectural option — the **internal-template
pattern** — and compares two deployment variants of it (shared vs. isolated
ADO project). It then describes the much simpler alternative of **not
running fork PRs at all** (the path the policy currently codifies) and the
residual risks that fork PRs still pose to ADO pipelines *without* secrets
access (which the policy does **not** restrict today).

---

## Threat model (one paragraph)

A fork PR can rewrite any file under the PR's HEAD, including pipeline YAML,
shell snippets, `requirements.txt`, and helper scripts. If any of that code
runs in a job that is bound to a real Service Connection (SC) or has a
secret-bearing variable group attached, the attacker gets **arbitrary code
execution under the WIF identity of the SC** and can call any API that
identity is allowed to call. The goal is to make it structurally impossible
for attacker-controlled YAML/scripts to ever execute in the same job that
holds the SC token.

---

## The internal-template pattern (mandatory baseline)

The trust boundary is moved out of the public GitHub repo and into ADO
configuration + a private ADO-hosted git repo that the attacker cannot
submit PRs against.

### Required pieces

1. **Private template repo in ADO** (in whichever ADO project hosts the
   pipeline). Contains the *entire* logic of the pipeline's raw stages
   template plus any helper scripts it invokes.

   - Branch-protected: no force-push, required reviewers from a small,
     trusted owner group.
   - Pinned ref (a protected branch or a tag) referenced by the SC's
     "Required template" check.

2. **Wrapper pipeline in the GitHub repo** (the `<wrapper>.yml` under
   [`.github/workflows/ado/`](../.github/workflows/ado/)) is reduced to:

   - `trigger: none` / `pr: none` (PR firing is configured in ADO).
   - `resources.repositories` for OneBranch governed templates **and** for
     the private template repo.
   - `extends:` the private template (no parameters, or only ADO-controlled
     parameters such as predefined `Build.*` variables).
   - No `stages:`, `jobs:`, `steps:`, no `script:`, no `parameters:` that
     pass attacker-controlled data into the template.

3. **Service Connection hardening** (Project Settings → Service Connections
   → the relevant SC → "Approvals and checks"):

   - **Required template check** pinned to the private repo + path + ref.
     This is evaluated against the *compiled* pipeline YAML at token-issue
     time. A fork PR that rewrites the wrapper to extend a different
     template will fail the check and never receive a WIF token.
   - **Branch control** restricted to the protected base branches of the
     GitHub repo (`3.0`, `main`, etc.). Fork PR runs use
     `refs/pull/N/merge` — they are rejected before the SC issues a token.
   - **Pipeline permissions**: granted only to this one pipeline.
     "Open access" must be off.

4. **Variable group(s)** consumed by the pipeline: same scoping —
   pipeline-permissions limited to this one pipeline; "Open access" off.

5. **Federated credential subject** on the Entra app set exactly to
   `sc://<org>/<project>/<sc-name>` (no wildcards), so a leaked SC config
   cannot be reused elsewhere.

6. **Template content rules** (these matter as much as the SC config):

   - The template MUST NOT execute any code from the PR HEAD checkout —
     no `pip install -r` from a PR-controlled `requirements.txt`, no
     `python3 <pr-path>`, no `bash <pr-path>`, no `go install ...@$(...)`
     where the version comes from PR data.
   - Helper scripts invoked by the template live in the private template
     repo, not in the GitHub repo.
   - PR-supplied data enters the job only via ADO predefined variables
     (`Build.SourceBranch`, `Build.SourceVersion`,
     `System.PullRequest.TargetBranch`) and is **regex-validated** before
     being used in shell, paths, or HTTP calls:
     - SHAs: `^[0-9a-f]{40}$`
     - Branch names: `^[A-Za-z0-9._/-]{1,255}$`
     - Component names derived from `git diff` filenames:
       `^[a-z0-9._+-]{1,128}$` (reject the run on any failure).
   - Any non-trivial logic is a Python script in the template repo (per the
     [ADO pipeline instructions](../.github/instructions/ado-pipeline.instructions.md)),
     not inline bash.
   - All tool versions pinned (container image by digest, not floating tag;
     package-manager installs pinned; Go / Python / etc. pinned by commit
     or version). Only `GovernedTemplates@refs/heads/main` is exempt.
   - The `OneBranch.Official.CrossPlat.yml` vs `NonOfficial` choice in the
     wrapper must match the SC's environment (production SC → `Official`;
     dev/staging SC → `NonOfficial`).

7. **GitHub-side hygiene** (does not affect SC security but prevents the
   wrapper itself from being silently weakened):

   - CODEOWNERS over `.github/workflows/ado/**` and
     `.github/workflows/scripts/**` requiring maintainer review.
   - Branch protection on the base branches with required reviews.

### Why this is the strongest option

The trust boundary is enforced by **ADO at token-issuance time**, against a
template that lives in a repo the attacker has no PR access to. No amount
of YAML rewriting in a fork PR can move that boundary.

---

## Variant A — shared ADO project

Put the private template repo, the pipeline, the SC, and the variable
group into an existing ADO project that also hosts other pipelines, repos,
SCs, and resources.

### What is *not* automatically exposed

With the SC scoped to this pipeline only and "Required template" + branch
control configured, the **direct path** to the Control Tower SC is
identical to the isolated-project case. Other SCs, variable groups, secure
files, and environments in the project are not automatically reachable —
they each have their own pipeline-permissions list.

### Security flaws / residual exposure

1. **Project Build Service identity is broadly scoped.**
   The pipeline runs as `<Project> Build Service (<org>)`. In a shared
   project this identity often has Read (sometimes Contribute) on many
   repos, ADO Artifacts feeds, wikis, and work items. A fork PR that
   modifies the wrapper to add `checkout:` of another project repo, or a
   `DownloadPipelineArtifact@2` of another pipeline's output, can read
   anything that identity can read. The "Required template" check stops
   the SC token from being issued, but it does NOT stop other tasks in
   the wrapper from running under the build identity.
2. **Self-hosted agent pool poisoning.** If the project uses a shared
   self-hosted pool, a fork PR build can leave behind poisoned caches,
   modified `~/.gitconfig`, planted binaries on `PATH`, or modified Go
   module cache, which the next trusted pipeline on that pool will pick
   up. This is the single biggest realistic risk in a shared project.
3. **Cross-pipeline artifact access.** Fork build can pull artifacts
   produced by other pipelines in the same project (signed binaries,
   internal reports, etc.) using the build identity.
4. **Configuration drift.** Pipeline-permissions on SCs and VGs in a busy
   shared project drift toward "Open access" through one-click mistakes
   over time. More admins = more chances of a misconfigured neighbor that
   weakens the posture indirectly (e.g., a neighbor SC compromise that
   then targets your pool).
5. **Larger administrative blast radius.** Anyone with Project
   Administrator on the shared project can modify SC checks, grant
   pipeline permissions, add federated credentials, or change branch
   protections on the template repo. The set of people who can weaken
   your security equals the (typically much larger) set of project admins.
6. **Audit/forensics noise.** Distinguishing fork-PR build activity from
   normal project activity in audit logs is harder.

### Acceptability conditions

A shared project is acceptable **only if all** of these hold:

- The pipeline runs on **Microsoft-hosted agents** (or a self-hosted pool
  dedicated to this pipeline only).
- The project Build Service identity has been audited and does not have
  access to anything you would mind a fork PR reading.
- Project Administrator membership is small, reviewed, and trusted.
- No SC/VG in the project is set to "Open access".

If any of these are shaky, prefer Variant B.

---

## Variant B — isolated ADO project

Create a new ADO project whose **only** purpose is to host this pipeline,
its private template repo, the Control Tower SC, the variable group, and
nothing else.

### Security flaws / residual exposure

1. **Wrapper supply chain in the GitHub repo.** The wrapper still lives in
   the public repo and can be modified through a merged malicious PR.
   CODEOWNERS + branch protection + reviewer discipline are still
   required. (This flaw is identical in both variants — it is a property
   of the wrapper-in-public-repo design, not of project topology.)
2. **Template repo administration.** Whoever is admin on the isolated
   project can disable branch protection on the template repo and push
   malicious template content, then trigger a build. Keep the admin set
   tiny and audit it.
3. **Federated credential drift.** If someone adds a second federated
   credential subject to the Entra app pointing at a different SC, the
   isolation is broken. Audit federated credentials on the Entra app
   periodically.
4. **One-time cost.** Setup, ownership, and ongoing maintenance of a
   dedicated project are more work than reusing an existing one. Not a
   security flaw per se, but a real operational tradeoff.

### What this variant eliminates that the shared one does not

- Build Service identity has access to essentially nothing — lateral
  reads of other repos / feeds / artifacts are structurally impossible.
- No shared self-hosted pool to poison (use hosted agents; if a
  self-hosted pool is needed, it has a single consumer).
- Configuration drift on neighboring SCs/VGs cannot affect this
  pipeline because there are no neighbors.
- Administrative blast radius is limited to the isolated project's
  admin list.
- Audit trail is high-signal: every event in the project relates to
  this pipeline.

### Recommendation

Variant B is the strongest posture available for an ADO PR-check
pipeline that holds production-adjacent secrets and runs against fork
PRs. Variant A is acceptable only under the conditions listed above.

---

## Side-by-side comparison

| Risk surface | Shared project (A) | Isolated project (B) |
|---|---|---|
| Direct SC token theft from fork PR | Blocked by SC "Required template" + branch control | Blocked by SC "Required template" + branch control |
| Build identity reads other repos / feeds / artifacts | **Possible** — depends on identity's project-wide permissions | Near-zero — nothing else exists in the project |
| Self-hosted agent pool poisoning | **Possible** if pool is shared with other pipelines | Eliminated (single consumer; use hosted agents) |
| Misconfigured neighbor SC/VG weakens posture | **Possible** — drift, mistakes by other admins | Not applicable — no neighbors |
| Admin blast radius | Project Admins of shared project (often many) | Project Admins of isolated project (small) |
| Wrapper in GitHub repo can be replaced via merged malicious PR | Same risk in both — mitigated by CODEOWNERS + branch protection | Same risk in both — mitigated by CODEOWNERS + branch protection |
| Federated credential subject drift | Same risk in both — mitigated by periodic Entra audit | Same risk in both — mitigated by periodic Entra audit |
| Operational cost | Low (reuse existing project) | Higher one-time setup; small ongoing overhead |

---

## Alternative — do not run fork PRs at all

**This is the option the project's policy currently codifies for all ADO
pipelines with secrets access** (see
[`ado-pr-check-fork-policy.instructions.md`](../.github/instructions/ado-pr-check-fork-policy.instructions.md)).
If fork PRs are not built against secret-bearing pipelines, the design
simplifies dramatically.

### What changes

- No isolated project required.
- No private template repo required.
- No "Required template" check on the SC required (branch control still
  recommended as defense in depth).
- The standard wrapper + raw stages template structure under
  [`.github/workflows/ado/`](../.github/workflows/ado/) can be used directly, with the standard
  hardening from
  [`ado-pipeline.instructions.md`](../.github/instructions/ado-pipeline.instructions.md)
  (pinned versions, regex-validated PR inputs, secrets via `env:`,
  Python over shell, explicit `timeoutInMinutes`, etc.).
- The pipeline runs only for PRs from branches in the upstream repo and
  for the merge queue (which by definition operates on commits already
  approved into a `gh-readonly-queue/...` branch by maintainers).

### How to enforce "no fork PRs"

Two layers, both required:

1. **ADO pipeline trigger settings** (GitHub PR trigger configuration
   on the ADO pipeline, not in YAML):
   - Disable "Build pull requests from forks of this repository".
   - If forks must be allowed for some other reason, at minimum:
     "Make secrets available to builds of forks" = OFF and "Require a
     team member's comment before building a fork pull request" = ON.
     (Note: the comment gate is a human safeguard; treat it as weaker
     than full disabling.)
2. **Branch policy / merge queue configuration** on the GitHub side:
   - The check is required only on PRs from upstream branches and on
     merge-queue commits. Fork PRs simply do not block merge.

### Security implications

- **Eliminated risks:** the entire fork-PR threat model goes away.
  Pipeline-injection through PR HEAD is no longer possible because PR
  HEAD is never executed against the SC.
- **Residual risks:**
  - Insider risk — a maintainer with push access to an upstream branch
    can still inject malicious YAML/scripts. Mitigated by CODEOWNERS,
    branch protection, and required reviews on
    `.github/workflows/ado/**` and `.github/workflows/scripts/**`.
  - Merge-queue commits are derived from PR HEAD; they are trusted only
    because a maintainer approved the merge. The same CODEOWNERS rule
    above is what keeps that trust honest.
  - Standard supply-chain hardening (pinned tool versions, internal
    feeds, sanitized PR-derived strings used only as data) still
    applies because merge-queue commits include the PR's contents.
- **Functional cost:** fork contributors cannot get pre-merge feedback
  from this specific check. Maintainers must either (a) push the fork's
  branch to the upstream repo to run the check, or (b) rely on the
  merge-queue run as the gate.

### When to choose this option

Choose "no fork PRs" when:

- Fork PRs to this repo are rare or not a primary contribution path,
  **or**
- The engineering cost of the isolated-project design is not justified
  by the value of pre-merge feedback on fork PRs, **or**
- The SC's permissions are sensitive enough that the residual risk of
  the internal-template design is still considered too high.

This is the simplest secure design. It trades contributor convenience
for a much smaller attack surface and lower operational burden, and is
the option the project policy mandates today.

---

## Residual risks of non-secret ADO pipelines on fork PRs

The project policy restricts only **ADO pipelines with secrets access**.
An ADO pipeline that has *no* service connection, *no* secret-bearing
variable group, *no* secure file, and *no* secret-bearing environment is
out of scope of the policy and may today be configured to build fork PRs.
Authors of such pipelines should still understand the residual risks a
fork PR build poses even without secrets, and weigh them before opting in:

1. **Parallelism abuse / queue starvation.** A fork PR can trigger
   arbitrary builds in the project's hosted-pool quota. A coordinated
   attacker can sustain enough fork-PR traffic to delay legitimate
   builds (effectively a low-grade denial-of-service against CI).
2. **Internal-network probing.** ADO hosted pools (including 1ES Hosted
   Pools) often run on Microsoft-internal network classes (e.g. `R1`)
   with reachability to internal services that are not exposed on the
   public internet. A fork PR running arbitrary code on such an agent
   can probe and fingerprint that internal network, even with no
   credentials of its own.
3. **Internal package-feed and registry abuse.** Hosted agents are
   typically pre-authenticated to internal Go module proxies, internal
   pip indexes, MCR, and similar feeds. A fork PR can issue arbitrary
   queries / downloads against these as the agent identity, which may
   be logged as legitimate corporate traffic and is hard to attribute.
4. **Cross-pipeline reads via the project Build Service identity.**
   The pipeline runs as the project's Build Service account. Anything
   that identity can read in the ADO project (other repos in the
   project, ADO Artifacts feeds, wikis, work items, downloadable
   artifacts of other pipelines) is reachable by a fork PR build that
   adds the appropriate tasks to the wrapper.
5. **Log disclosure of internal metadata.** Build logs frequently
   include internal hostnames, IP ranges, agent image versions, MCR
   tags, and other infrastructure details that an attacker would
   otherwise have to guess. Fork PR build logs are visible to the PR
   author.
6. **Shared self-hosted pool poisoning.** *Not applicable in this repo*
   because the policy mandates hosted pools only — but documented for
   completeness: a fork PR running on a shared self-hosted pool can
   leave behind poisoned caches, modified `~/.gitconfig`, planted
   binaries on `PATH`, or modified Go module cache, which the next
   trusted pipeline on that pool will pick up.

These risks apply *regardless* of whether the pipeline holds secrets.
The project does not policy-restrict non-secret pipelines today, but the
default recommendation for any new non-secret ADO pipeline is still to
run fork PRs only after the author has consciously assessed the items
above and decided the value of pre-merge fork feedback is worth them.

---

## Summary recommendation

1. **For ADO pipelines with secrets access:** the project policy
   mandates the "do not run fork PRs at all" option. See
   [`ado-pr-check-fork-policy.instructions.md`](../.github/instructions/ado-pr-check-fork-policy.instructions.md).
   Future exceptions, if approved by maintainers, must use the
   internal-template pattern in an **isolated ADO project** (Variant B);
   Variant A (shared project) is acceptable only under all of the
   conditions listed in its section above.
2. **For ADO pipelines without secrets access:** out of scope of the
   policy today. Authors should weigh the residual risks above before
   enabling fork PR builds; if in doubt, default to upstream-only.
