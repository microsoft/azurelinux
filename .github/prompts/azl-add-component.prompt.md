---
description: "Add a new component to Azure Linux"
---

# Add Component: `${input:component_name:package name}`

Add the component **${input:component_name}** to the **${input:project:base}** project, sourcing from **${input:source_distro:fedora}**.

Follow the full workflow in the [skill-add-component skill](../skills/skill-add-component/SKILL.md) — it is the source of truth for the add-component procedure, including tenet reviews, validation, building, and testing. Use the structural patterns from [comp-toml.instructions.md](../instructions/comp-toml.instructions.md) for TOML syntax and overlay guidance.

## Quick Reference

- **Component name:** `${input:component_name}`
- **Check existence:** `azldev comp list -p ${input:component_name} -q -O json`
- **Prep sources:** `azldev comp prep-sources -p ${input:component_name} --skip-overlays --force -o base/build/work/scratch/${input:component_name} -q`
- **Build:** `azldev comp build -p ${input:component_name} -q`
