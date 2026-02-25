---
description: "Update an existing Azure Linux component (version bump, dependency change, overlay edit)"
---

# Update Component: `${input:component_name:package name}`

Update **${input:component_name}** — target version: **${input:new_version:target version}**, update type: **${input:update_type:version|dependency|overlay|config}**.

Use structural patterns from [comp-toml.instructions.md](../instructions/comp-toml.instructions.md). If overlays break, follow the [skill-fix-overlay skill](../skills/skill-fix-overlay/SKILL.md). Test changes using the [skill-build-component skill](../skills/skill-build-component/SKILL.md).

## Workflow

1. **Query current state:** `azldev comp query -p ${input:component_name}`
2. **Identify scope** of the update based on the update type:
   - `version` — version bump (see risk assessment below)
   - `dependency` — adding/removing/changing BuildRequires or Requires
   - `overlay` — modifying or adding overlays
   - `config` — build config changes (`build.defines`, `build.without`)
3. **Apply changes** to the `.comp.toml` file
4. **Verify overlays still apply:**
   ```bash
   azldev comp prep-sources -p ${input:component_name} --skip-overlays -o base/build/work/scratch/${input:component_name}-pre --force
   azldev comp prep-sources -p ${input:component_name} -o base/build/work/scratch/${input:component_name}-post --force
   diff -r base/build/work/scratch/${input:component_name}-pre base/build/work/scratch/${input:component_name}-post
   ```
   If overlays fail, follow the [skill-fix-overlay skill](../skills/skill-fix-overlay/SKILL.md).
5. **Migrate to dedicated file** if the component is still inline and now needs customization (use `/azl-migrate-component`)
6. **Build and test:** `azldev comp build -p ${input:component_name}`
7. **Smoke-test** the built RPMs in a mock chroot

## Versioning Risk Assessment

When bumping versions, assess risk before proceeding:

| Bump Type | Risk | Action |
|-----------|------|--------|
| **Major** (1.x → 2.x) | High — may break API/ABI | Require explicit user approval. Check upstream release notes for breaking changes. |
| **Minor** (1.2 → 1.3) | Medium — generally safe | Check for new dependencies, deprecations, soname changes. |
| **Patch** (1.2.3 → 1.2.4) | Low — usually safe | Typically security fixes and bug fixes. |

**Always:**
- Check upstream release notes for breaking changes
- Flag soname changes (may break dependent packages)
- Note new dependencies (new BuildRequires or Requires)
- Examine existing overlays — ensure they still apply cleanly; if an overlay is no longer needed, recommend removal
- Warn about feature removal upstream
- Summarize risks and changes for the user

When in doubt, recommend the user review the upstream changelog before proceeding.
