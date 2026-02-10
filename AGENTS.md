# Azure Linux — Agent Guide

For project context and architecture, see [`.github/copilot-instructions.md`](.github/copilot-instructions.md).

## Conventions

- Always run `azldev comp query -p <name>` before modifying a component.
- Prefer overlays over forking/local specs when customizing upstream packages.
- Use `azldev comp prep-sources -p <name>` to verify overlays apply cleanly before building.

## Skills

Detailed workflows live in skills (loaded on-demand when relevant):

| Task | Skill |
|------|-------|
| Build a component, debug build failures | [`azl-build-component`](.github/skills/azl-build-component/SKILL.md) |
| Add a new component to the distro | [`azl-add-component`](.github/skills/azl-add-component/SKILL.md) |
| Diagnose and fix overlay issues | [`azl-fix-overlay`](.github/skills/azl-fix-overlay/SKILL.md) |

## Directory Guidance

- **Components:** [`base/comps/AGENTS.md`](base/comps/AGENTS.md) — file organization rules
- **Distro config:** [`distro/AGENTS.md`](distro/AGENTS.md) — build defaults, shared config
