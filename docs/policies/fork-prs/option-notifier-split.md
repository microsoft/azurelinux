# Option: notifier → trusted-internal split

> ↩ [Fork-PR options index](README.md) · [Threat model](README.md#threat-model)

Split the work across two pipelines with a hard trust boundary between them.
A thin **notifier** runs on the fork PR, holds no secrets, executes no PR code,
and emits only metadata. A separate **internal** pipeline — triggered by the
notifier's completion, running its own trusted-branch code — holds the SC and
makes the privileged Control Tower call. The job that holds the token never
executes code the PR author can modify. This isolates the *token*; it does not
change the fact that the resulting build runs the PR's spec in production Koji
(see Security posture).

## When to choose

- You want fork PRs to run automatically and you want the SC fully isolated
  from fork-controlled code (stronger than review discipline), **and**
- you can stand up a GitHub App to report the result back onto the PR.

## How it works

```text
fork PR ──(branch policy check)──▶ Notifier  [checkout: none, no secrets]
                                     • emits pr-context (head SHA, repo, PR #)
                                     • tags the run
                                            │ completion trigger (tag filter)
                                            ▼
                       Internal pipeline  [trusted branch, holds the SC]
                         • validates the metadata as untrusted data
                         • runs its own scripts → Control Tower
                         • posts a check-run/status to the PR head SHA
```

- The **notifier** sets `checkout: none`, so it runs no PR code, and emits only
  ADO-provided metadata (`Build.SourceVersion`, `System.PullRequest.*`). Fork
  builds receive only a restricted-scope `System.AccessToken`, so the notifier
  cannot queue the internal pipeline directly — the completion trigger
  indirection is required.
- The **internal pipeline** is reached via the pipeline-completion resource
  trigger, runs on the trusted target branch, and therefore receives secrets
  normally without enabling fork secrets. It consumes the metadata as **data
  only** (validate the head SHA against `^[0-9a-f]{40}$` and the repo URI
  against an allow-list; never `source`/exec the artifact) and runs only its
  own checked-out scripts. It never checks out PR code; the PR's package is
  built by Control Tower / Koji from the validated SHA, so **production Koji
  still executes the PR's spec** — the isolation is of the SC token, not of the
  build.
- A maintainer-gated ADO **Environment** on the internal pipeline provides the
  approval boundary if maintainer authorization per run is required.

## Security posture

- The SC token never enters a fork-controlled job — this is a structural
  isolation, not a review-dependent one.
- The privileged stage executes only trusted-branch code; PR-derived values
  cross the boundary as validated data, not as executable content.
- **Production Koji is not addressed by this option.** The build it triggers
  still runs the PR's spec in prod Koji; this option isolates the token, not
  the build. Koji-side containment is tracked separately (see the
  [threat model](README.md#threat-model)).
- Use a small safe tag to filter the trigger; keep attacker-controlled values
  (e.g. fork branch names) out of tags and inside the validated metadata.

See GitHub's guidance on the equivalent `pull_request` → `workflow_run`
pattern and untrusted-checkout risks in the
[secure use reference](https://docs.github.com/en/actions/reference/security/secure-use).

## Trade-offs

- The PR's required check is the **notifier**, which goes green as soon as it
  tags — so the internal pipeline's pass/fail is not automatically on the PR.
  Reporting status back requires the internal pipeline to post a GitHub
  check-run/commit-status to the PR head SHA, which needs a **GitHub App**
  (its secret stored in Key Vault (KV), reached via an SC). That is the main
  cost of this option.
- Two pipeline definitions plus a completion trigger to maintain; confirm the
  completion trigger fires for fork-PR notifier runs in your configuration.
- Every fork PR (and push to it) can drive an internal run that pauses on
  maintainer approval — watch for approval fatigue on busy repos.

## Open questions

- Is a GitHub App available (or can one be provisioned with KV-stored secrets)
  to post PR status?
- Does the pipeline-completion trigger reliably fire for `refs/pull/*/merge`
  notifier runs originating from forks?
- Should the internal run require maintainer approval per run, or only branch
  policy?
