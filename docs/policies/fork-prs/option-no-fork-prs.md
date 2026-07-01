# Option: do not run fork PRs

> ↩ [Fork-PR options index](README.md) · [Threat model](README.md#threat-model)

The secret-bearing pipeline never builds fork PRs. Fork contributors get no
pre-merge run of this check; the check runs only on PRs from upstream branches
and on merge-queue commits.

## When to choose

- Fork PRs are rare or not a primary contribution path, **or**
- the engineering cost of the isolating designs is not justified by the value
  of pre-merge feedback on fork PRs, **or**
- the SC's permissions are sensitive enough that any residual risk from running
  fork content is unacceptable.

## How it works

Two layers, both required:

1. **ADO PR trigger settings** (configured on the pipeline, not in YAML):
   - "Build pull requests from forks of this repository" → **OFF**.
   - "Make secrets available to builds of forks" → **OFF** as defense in depth,
     so a later accidental flip of the first toggle does not expose secrets.
2. **GitHub branch policy / merge queue**: the check is required only on PRs
   from upstream branches and on merge-queue commits. Fork PRs do not block
   merge.

No isolated project, private template repo, or SC "Required template" check is
needed (branch control on the SC is still worthwhile as defense in depth). The
standard wrapper + raw-stages structure under
[`.github/workflows/ado/`](../../../.github/workflows/ado/) applies, with the
hardening from
[`ado-pipeline.instructions.md`](../../../.github/instructions/ado-pipeline.instructions.md).

## Security posture

- The entire fork-PR threat model is removed: PR HEAD is never executed against
  the SC, so pipeline injection through a fork is not possible.
- Merge-queue commits are derived from PR HEAD and are trusted only because a
  maintainer approved the merge; CODEOWNERS + branch protection + required
  reviews on the ADO pipeline and script paths are what keep that trust honest.
- **Production Koji is not fully avoided.** The check is required on
  merge-queue commits, which contain the PR's spec files, so prod Koji executes
  the PR author's scriptlets at merge-queue time — after, and gated by, a
  maintainer's merge approval rather than automatically on the fork PR.
- Standard supply-chain hardening (pinned tool versions, internal feeds,
  PR-derived strings used only as validated data) still applies, because
  merge-queue commits include the PR's contents.

## Trade-offs

- Fork contributors cannot get pre-merge feedback from this check. A maintainer
  must either push the fork's branch to the upstream repo to run it, or rely on
  the merge-queue run as the gate.
- Smallest attack surface: the PR HEAD never runs against the SC, and prod Koji
  runs fork code only after a maintainer merge approval.

## Open questions

- Is merge-queue-time feedback acceptable, or do contributors need a result
  before the maintainer acts?
- Who owns pushing fork branches upstream when a pre-merge run is needed?
