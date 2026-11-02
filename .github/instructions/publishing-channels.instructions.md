---
applyTo: "base/comps/components-publish-channels.toml"
description: "Publishing channel edits route future builds; Base additions must also trigger a component build."
---

# Publishing channel changes

- Membership in `[component-groups.base-packages].components` routes the next
  component build to Base. It does not republish old RPMs or change the build
  fingerprint. A configuration-only promotion can otherwise merge without
  publishing anything to production Base.
- Every newly listed component must be `added` or `changed` in
  `azldev comp changed --from <base-ref> --to HEAD -p <name> -q -O json`.
  Touched specs, touched locks, and `sourcesChange` alone are not sufficient.
- If no genuine component input change already selects a rebuild, use
  `azldev comp update -p <name> --bump`. This preserves the upstream pin;
  plain `update` may be a no-op. For `release.calculation = "manual"`, also
  advance the release in the component's source/config and verify the final
  rendered release. Render, commit, re-render, and stage the
  final specs for an amend following the
  [update-component skill](../../.agents/skills/azldev-update-component/SKILL.md).
- Check runtime dependency closure and explicit package exceptions. Listing a
  component does not automatically add its dependencies, and package overrides
  can keep individual subpackages in SDK.
- Do not claim publication from a green submission check. Verify the completed
  official build and the resulting artifacts in the intended production channel.

See [Package publishing channels](../../DEVELOPING.md#package-publishing-channels)
for the human-facing workflow.
