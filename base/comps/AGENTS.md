# Component Management — Agent Guide

## Rules

- Non-trivial components (overlays, build config) SHOULD have their own `<name>/<name>.comp.toml`. Simple imports stay inline in `components.toml`.
- `components.toml` uses `includes` to pull in all `**/*.comp.toml` — no manual wiring needed.
- **When moving a component out of inline `components.toml` into a dedicated `<name>/<name>.comp.toml`, DELETE the inline entry.** Do **not** leave a "moved to X" pointer or any other tombstone comment behind. Discovery is automatic via the `**/*.comp.toml` include glob.
- **When removing a component outright, DELETE the inline entry.** Don't leave a TODO/removed-from-here comment — git history is the record.
- Canonical example: [`rpm/rpm.comp.toml`](rpm/rpm.comp.toml) — uses modern `[[...overlays]]` syntax with `description` fields. For a larger overlay example (legacy inline syntax, not to be copied for new work), see [`azurelinux-rpm-config/azurelinux-rpm-config.comp.toml`](azurelinux-rpm-config/azurelinux-rpm-config.comp.toml).
- Schema: [`azldev.schema.json`](../../external/schemas/azldev.schema.json)

## Skills

- Adding a new component → [`skill-add-component`](../../.github/skills/skill-add-component/SKILL.md)
- Removing component(s) → [`skill-remove-component`](../../.github/skills/skill-remove-component/SKILL.md)
- Fixing overlay issues → [`skill-fix-overlay`](../../.github/skills/skill-fix-overlay/SKILL.md)
- Byte-deterministic Source0 repack (`modify_source.sh` + `replace-upstream`) → [`skill-modify-source`](../../.github/skills/skill-modify-source/SKILL.md)
- Remediating component-level signing/scan failures → [`skill-signing-failure-remediation`](../../.github/skills/skill-signing-failure-remediation/SKILL.md)
- Building and debugging → [`skill-build-component`](../../.github/skills/skill-build-component/SKILL.md)
- Testing in mock chroot → [`skill-mock`](../../.github/skills/skill-mock/SKILL.md)
