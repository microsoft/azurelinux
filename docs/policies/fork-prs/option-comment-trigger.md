# Option: comment-triggered `/azp run`

> ↩ [Fork-PR options index](README.md) · [Threat model](README.md#threat-model)

A single secret-bearing pipeline is wired as the PR check, but fork PRs do not
build automatically. A repository collaborator with **Write or higher**
permission must comment `/azp run` (or `/AzurePipelines run`) to authorize the
build of the current head commit; each new commit needs a fresh comment.

## When to choose

- You want the simplest wiring and native PR status, **and**
- you accept that the trust boundary is the commenter's review of the exact
  commit they authorize, rather than structural isolation, **and**
- the SC's blast radius is acceptable under that assumption.

## How it works

- One ADO pipeline (YAML in GitHub), wired as a PR build-validation check, with
  "Make secrets available to builds of forks" = ON and "Require a team member's
  comment before building a pull request" = ON.
- A **Write+** collaborator comments `/azp run` to authorize the build of the
  current head commit. The build *is* the check, so the Azure Pipelines GitHub App
  posts pass/fail to the PR natively — no separate GitHub App is needed.
- Internal PRs can skip the comment: set the comment requirement to **"Only on
  pull requests from non-team members."** Write+ authors build automatically;
  fork/non-member PRs require `/azp run`.

## Security posture

- The SC token is present in a job that runs the PR HEAD's YAML and `scripts/**`.
  There is **no structural isolation**: safety collapses to "the `/azp run`
  commenter actually reviewed that exact head commit."
- **Production Koji is not addressed by this option.** The authorized build
  still runs the PR's spec in prod Koji; the comment gate controls *who
  authorizes* the run, not what the build executes. Koji-side containment is
  tracked separately (see the [threat model](README.md#threat-model)).
- **Trust assumption — state it plainly:** authorization is GitHub **Write+
  collaborator** permission typing the comment. It is *not* maintainer-only and
  *not* enforced by ADO permissioning. Any Write+ member can authorize a
  secret-bearing run of fork code. To require maintainer-only authorization,
  layer an SC **Approval check** — but that check also gates internal PRs,
  reducing the convenience that motivates this option.
- Even with secrets enabled, fork builds receive a *restricted* access token
  unless the "same permissions as regular builds" toggle is also flipped (more
  risk). Leave it off.
- This option depends on the org-level "Limit building pull requests from
  forked repositories" control permitting secrets for fork PRs. If that control
  is set to "Securely build," secrets cannot be made available to fork PRs at
  all and this option is blocked until an admin changes it (a security-posture
  decision). Verify the org setting before choosing this option.

See the
[secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
for hardening the workflow that runs under these conditions.

## Trade-offs

- Low implementation cost and native PR status (no custom GitHub App).
- The trust boundary is human review discipline, not isolation — unlike the
  [internal-template](option-internal-template.md) and
  [notifier-split](option-notifier-split.md) options.
- Per-commit friction: every new fork commit needs a fresh `/azp run`.

## Open questions

- Is the org-level fork-build control set to allow secrets for fork PRs?
- Is Write+ review discipline an acceptable trust boundary for this SC, or is
  maintainer-only authorization (and the resulting internal-PR friction)
  required?
