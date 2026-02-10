# Component Management — Agent Guide

## Rules

- Non-trivial components (overlays, build config) SHOULD have their own `<name>/<name>.comp.toml`. Simple imports stay inline in `components.toml`.
- `components.toml` uses `includes` to pull in all `**/*.comp.toml` — no manual wiring needed.
- Canonical complex example: [`azurelinux-rpm-config/azurelinux-rpm-config.comp.toml`](azurelinux-rpm-config/azurelinux-rpm-config.comp.toml)
- Schema: [`azldev.schema.json`](../../external/schemas/azldev.schema.json)

## Skills

- Adding a new component → [`azl-add-component`](../../.github/skills/azl-add-component/SKILL.md)
- Fixing overlay issues → [`azl-fix-overlay`](../../.github/skills/azl-fix-overlay/SKILL.md)
- Building and debugging → [`azl-build-component`](../../.github/skills/azl-build-component/SKILL.md)
