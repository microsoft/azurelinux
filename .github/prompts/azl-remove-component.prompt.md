---
description: "Remove component(s) from Azure Linux"
---

# Remove Component: `${input:component_names:component name(s), comma-separated}`

Remove the component(s) **${input:component_names}** from the **${input:project:base}** project.

Follow the workflow in the [skill-remove-component skill](../skills/skill-remove-component/SKILL.md).

## Workflow

1. Parse the component list from `${input:component_names}` (comma-separated)
2. For each component, verify it exists: `azldev comp list -p <name> -q -O json`
3. Find all artifacts: component definition, publish-channel references (component name in `[component-groups.base-packages]` and per-binary `# srpm: <name>` entries under `[package-groups.exceptions-packages]` in `base/comps/components-publish-channels.toml`), lock file, rendered specs
4. Remove the component entry from `components.toml` (or delete dedicated `base/comps/<name>/` directory)
5. Remove the component from `[component-groups.base-packages].components` (if present) and any matching `# srpm: <name>` lines from `[package-groups.exceptions-packages].packages` in `base/comps/components-publish-channels.toml`
6. Delete `locks/<name>.lock` and `specs/<first-char>/<name>/`
7. Check for references in kiwi image files (`*.kiwi`) and other config (`base/images/`, `comps.xml`)
8. Verify no references remain: `azldev comp list -p <name> -q -O json` should fail, `grep` of `components-publish-channels.toml` and kiwi files should return nothing
