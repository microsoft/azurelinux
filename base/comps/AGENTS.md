# Component Management — Agent Guide

## Rules

- Non-trivial components (overlays, build config) SHOULD have their own `<name>/<name>.comp.toml`. Simple imports stay inline in `components.toml`.
- `components.toml` uses `includes` to pull in all `**/*.comp.toml` — no manual wiring needed.
- Canonical example: [`rpm/rpm.comp.toml`](rpm/rpm.comp.toml) — uses modern `[[...overlays]]` syntax with `description` fields. For a larger overlay example (legacy inline syntax, not to be copied for new work), see [`azurelinux-rpm-config/azurelinux-rpm-config.comp.toml`](azurelinux-rpm-config/azurelinux-rpm-config.comp.toml).
- Schema: [`azldev.schema.json`](../../external/schemas/azldev.schema.json)

## Skills

- Adding a new component → [`azl-add-component`](../../.github/skills/azl-add-component/SKILL.md)
- Fixing overlay issues → [`azl-fix-overlay`](../../.github/skills/azl-fix-overlay/SKILL.md)
- Building and debugging → [`azl-build-component`](../../.github/skills/azl-build-component/SKILL.md)
- Testing in mock chroot → [`azl-mock`](../../.github/skills/azl-mock/SKILL.md)
