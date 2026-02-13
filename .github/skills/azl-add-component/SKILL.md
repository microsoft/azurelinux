---
name: azl-add-component
description: |
  Add a new component to Azure Linux. Use when importing packages from Fedora,
  creating comp.toml files, choosing inline vs dedicated definitions, or setting
  up a new component with overlays. Triggers: "add component", "new package",
  "import from fedora", "create my-comp.toml", etc.
---

# Add a Component

> **TODO:** This skill is a placeholder. Full instructions will cover:
>
> - Checking if a component already exists (`azldev comp query -p <name>`)
> - Choosing inline (in `components.toml`) vs dedicated (`<name>/<name>.comp.toml`)
> - Sourcing specs from upstream Fedora
> - Adding overlays when customizations are needed
> - Validating with `azldev comp prep-sources` and test builds
