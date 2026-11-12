---
applyTo: "**"
excludeAgent: "cloud-agent"
---

# Code review guidance

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
