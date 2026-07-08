---
description: "Add a new component to Azure Linux"
---

# Add Component: `${input:component_name:package name}`

Add the component **${input:component_name}** to the **${input:project:base}** project, sourcing from **${input:source_distro:fedora}**.

Follow the workflow in the [azldev-add-component skill](../../.agents/skills/azldev-add-component/SKILL.md) and the structural guidance in the [azldev-comp-toml skill](../../.agents/skills/azldev-comp-toml/SKILL.md).

## Workflow

1. Check if `${input:component_name}` already exists: `azldev comp list -p ${input:component_name} -q -O json`
2. If it doesn't exist, add a bare inline entry to inspect the upstream spec first
3. Create the initial lock: `azldev comp update -p ${input:component_name}`
4. Use `azldev comp prep-sources -p ${input:component_name} --skip-overlays --force -o base/build/work/scratch/${input:component_name} -q` to pull the upstream spec
5. Review the spec and determine what customizations are needed (if any)
6. **Decision:**
   - No changes needed → leave as inline entry in `components.toml`
   - Needs overlays or customizations → create `${input:component_name}/${input:component_name}.comp.toml`
   - Needs extensive changes overlays can't handle → forked local spec (**last resort**, requires explicit user sign-off)
7. Add overlays with meaningful `description` fields explaining *why* each change is needed
8. Refresh the lock, render, and verify: `azldev comp update -p ${input:component_name}`, then `azldev comp render -p ${input:component_name}` and inspect `specs/` (as specified by `rendered-specs-dir` config) output. For deeper debugging, use `azldev comp diff-sources -p ${input:component_name}`.
9. Build: `azldev comp build -p ${input:component_name} -q`
10. Smoke-test the built RPMs in a mock chroot
