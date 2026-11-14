---
applyTo: "**"
excludeAgent: "cloud-agent"
---

# Code review guidance

## Component version changes

- Compare each affected component's effective upstream version before and after
  the PR, including changes caused indirectly by upstream pins, lock files,
  overlays, or shared defaults. Use rendered specs and component configuration
  as evidence; do not rely solely on the PR title or a literal version edit.
- A change to a new **major version** (for example, `1.9.4` to `2.0.0`) requires
  a **high-severity** review comment stating that maintainer approval is required
  before merging.
- A change to a new **minor version** within the same major version (for example,
  `1.9.4` to `1.10.0`) requires a **medium-severity** review comment stating that
  maintainer approval is required before merging.
- Start the finding's title with "Maintainer approval required:" and identify
  the component and old/new versions. Report only the major-version finding
  when both major and minor numbers change.
- Report each version-change approval requirement as an inline review comment
  on the changed line responsible for the update, not solely in the review
  summary. Include the component and old/new versions.
- Apply these checkpoints even when the version change is intentional. They
  request maintainer sign-off, not a revert or a claim that the update is broken.
  Report independently demonstrated defects separately.
- Patch-only updates (for example, `1.9.4` to `1.9.5`) and RPM release-only
  changes do not trigger this rule. Follow the upstream project's versioning
  scheme; do not invent major/minor classifications for ambiguous versions.

## Publication channels

- Flag any addition or removal of publication channels as requiring maintainer
  approval. This includes changes to channel definitions, component channel
  assignments, and effective assignments through defaults or group membership
  (for example, adding or removing entries in `base-packages` in
  `base/comps/components-publish-channels.toml`).
- Treat a channel reassignment as both a removal from the old channel and an
  addition to the new channel. Identify the affected components and channels
  in the finding, even when the change appears intentional.
- A channel change alone is a maintainer sign-off checkpoint, not a correctness
  error. Start each approval-only finding's title with "Maintainer approval
  required:" followed by the affected component or group and routing change.
  Do not shorten this to "Approve ..."; the title must identify the maintainer
  as the required approver.
- Low severity is appropriate for approval-only findings; it does not make
  maintainer approval optional. State that maintainer sign-off is required
  before merging the routing change.
- Do not describe the change as broken or recommend reverting it solely
  because it changes publication channels.
- Report independently demonstrated defects (such as broken dependency closure
  or a missing required rebuild) separately, with their own evidence and
  defect-focused titles. Do not conflate those defects with the sign-off request.
