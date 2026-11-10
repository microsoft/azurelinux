---
applyTo: "**"
excludeAgent: "cloud-agent"
---

# Code review guidance

## Publication channels

- Flag any addition or removal of publication channels as requiring maintainer
  review. This includes changes to channel definitions, component channel
  assignments, and effective assignments through defaults or group membership
  (for example, adding or removing entries in `base-packages` in
  `base/comps/components-publish-channels.toml`).
- Treat a channel reassignment as both a removal from the old channel and an
  addition to the new channel. Identify the affected components and channels
  in the finding, even when the change appears intentional.
