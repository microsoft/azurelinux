---
description: "Migrate an inline component definition to a dedicated file"
---

# Migrate Component: `${input:component_name:package name}`

Migrate **${input:component_name}** from an inline definition to a dedicated `.comp.toml` file.

Use structural patterns from [comp-toml.instructions.md](../instructions/comp-toml.instructions.md) and file organization rules from [base/comps/AGENTS.md](../../base/comps/AGENTS.md).

## When to use

- Adding first customization (overlays, build config) to a simple inline import
- The inline definition is getting complex (multiple fields beyond just the name)
- Adding overlays to an inline component

## Workflow

1. **Query the current definition:** `azldev comp query -p ${input:component_name}`
2. **Find the inline entry** in `components.toml` (or whichever file contains it)
3. **Create the dedicated file:** `base/comps/${input:component_name}/${input:component_name}.comp.toml`
   - Move the component definition from the inline entry to the new file
   - Follow the dedicated file patterns from `comp-toml.instructions.md`
4. **Remove the inline entry** — the dedicated file is auto-discovered via the `**/*.comp.toml` glob in `components.toml`
5. **Validate:** `azldev comp query -p ${input:component_name} -q -O json` — output should be identical to before migration
6. **Optionally:** add the overlays or customizations that triggered the migration
