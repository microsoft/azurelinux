---
description: "Review an Azure Linux component for hygiene and best practices"
---

# Review Component: `${input:component_name:package name}`

Review **${input:component_name}** for hygiene and best practices.

Follow the review checklist in the [azl-review-component skill](../skills/azl-review-component/SKILL.md). Reference [comp-toml.instructions.md](../instructions/comp-toml.instructions.md) for structural patterns and [base/comps/AGENTS.md](../../base/comps/AGENTS.md) for file organization rules.

## Steps

1. Query the component: `azldev comp query -p ${input:component_name}`
2. Read the component's `.comp.toml` file (or inline definition in `components.toml`)
3. Run through the review checklist from the skill
4. Produce a structured report grouped by severity: **Errors** (must-fix), **Warnings** (should-fix), **Info** (suggestions)
