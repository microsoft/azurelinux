# Component Management — Agent Guide

## Rules

- Non-trivial components (overlays, build config) SHOULD have their own `<name>/<name>.comp.toml`. Simple imports stay inline in `components.toml`.
- `components.toml` uses `includes` to pull in all `**/*.comp.toml` — no manual wiring needed.
- Canonical example: [`rpm/rpm.comp.toml`](rpm/rpm.comp.toml) — uses modern `[[...overlays]]` syntax with `description` fields. For a larger overlay example (legacy inline syntax, not to be copied for new work), see [`azurelinux-rpm-config/azurelinux-rpm-config.comp.toml`](azurelinux-rpm-config/azurelinux-rpm-config.comp.toml).
- Schema: [`azldev.schema.json`](../../external/schemas/azldev.schema.json)

## Skills

- Adding a new component → [`skill-add-component`](../../.github/skills/skill-add-component/SKILL.md)
- Fixing overlay issues → [`skill-fix-overlay`](../../.github/skills/skill-fix-overlay/SKILL.md)
- Building and debugging → [`skill-build-component`](../../.github/skills/skill-build-component/SKILL.md)
- Testing in mock chroot → [`skill-mock`](../../.github/skills/skill-mock/SKILL.md)
