# Component Management — Agent Guide

## Rules

- Non-trivial components (overlays, build config) SHOULD have their own `<name>/<name>.comp.toml`. Simple imports stay inline in `components.toml`.
- `components.toml` uses `includes` to pull in all `**/*.comp.toml` — no manual wiring needed.
- Canonical example: [`rpm/rpm.comp.toml`](rpm/rpm.comp.toml) — uses modern `[[...overlays]]` syntax with `description` fields. For a larger overlay example (legacy inline syntax, not to be copied for new work), see [`azurelinux-rpm-config/azurelinux-rpm-config.comp.toml`](azurelinux-rpm-config/azurelinux-rpm-config.comp.toml).
- Schema: [`azldev.schema.json`](../../external/schemas/azldev.schema.json)
- Before a version or source-pin update, review upstream release notes, new dependencies, feature removals, ABI/soname changes, and whether existing overlays are still needed. Major version updates require explicit user approval.
- When removing a component, also remove it from `[component-groups.base-packages].components` and remove matching `# srpm: <name>` package exceptions in `components-publish-channels.toml`; then check image definitions, `comps.xml`, and dependants.

## Skills

- Adding a new component → [`azldev-add-component`](../../.agents/skills/azldev-add-component/SKILL.md)
- Updating or finalizing a component → [`azldev-update-component`](../../.agents/skills/azldev-update-component/SKILL.md)
- Removing component(s) → [`azldev-remove-component`](../../.agents/skills/azldev-remove-component/SKILL.md)
- Fixing overlay issues → [`azldev-overlays`](../../.agents/skills/azldev-overlays/SKILL.md)
- Building and debugging → [`azldev-build-component`](../../.agents/skills/azldev-build-component/SKILL.md)
- Testing in mock chroot → [`azldev-mock`](../../.agents/skills/azldev-mock/SKILL.md)
