---
description: "Review an Azure Linux component for hygiene and best practices"
argument-hint: "Component to review. Indicate if the review should be a full review or only on changes."
---

# Review Component: `${input:component_name:package name}`

Review **${input:component_name}** for hygiene and best practices.

Follow the component structure and review guidance in the [azldev-comp-toml skill](../../.agents/skills/azldev-comp-toml/SKILL.md), overlay guidance in the [azldev-overlays skill](../../.agents/skills/azldev-overlays/SKILL.md), and repository-specific rules in [base/comps/AGENTS.md](../../base/comps/AGENTS.md).

## Steps

1. Query the component: `azldev comp query -p ${input:component_name}`
2. Read the component's `.comp.toml` file (or inline definition in `components.toml`)
3. Run through the `azldev-comp-toml` skill's **Review checklist**, using the
	`azldev-overlays` skill for the overlay-specific checks
4. Produce a structured report grouped by severity: **Errors** (must-fix), **Warnings** (should-fix), **Info** (suggestions)
