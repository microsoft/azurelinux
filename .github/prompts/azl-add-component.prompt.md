---
description: "Add a new component to Azure Linux"
---

# Add Component: `${input:component_name:package name}`

Add the component **${input:component_name}** to the **${input:project:base}** project, sourcing from **${input:source_distro:fedora}**.

Follow the workflow in the [azl-add-component skill](../skills/azl-add-component/SKILL.md) and use the structural patterns from [comp-toml.instructions.md](../instructions/comp-toml.instructions.md).

## Workflow

1. Check if `${input:component_name}` already exists: `azldev comp list -p ${input:component_name} -q -O json`
2. If it doesn't exist, add a bare inline entry to inspect the upstream spec first
3. Use `azldev comp prep-sources -p ${input:component_name} --skip-overlays -o <dir> -q` to pull the upstream spec
4. Review the spec and determine what customizations are needed (if any)
5. **Decision:**
   - No changes needed → leave as inline entry in `components.toml`
   - Needs overlays or customizations → create `${input:component_name}/${input:component_name}.comp.toml`
   - Needs extensive changes overlays can't handle → forked local spec (**last resort**, requires explicit user sign-off)
6. Add overlays with meaningful `description` fields explaining *why* each change is needed
7. Validate: `azldev comp prep-sources -p ${input:component_name} -o <dir> -q` (with overlays) and diff against the skip-overlays output
8. Build: `azldev comp build -p ${input:component_name} -q`
9. Smoke-test the built RPMs in a mock chroot
