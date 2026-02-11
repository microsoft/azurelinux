---
description: "Debug a component build failure or overlay error"
---

# Debug Component: `${input:component_name:package name}`

Debug issues with **${input:component_name}**.

Error context: ${input:error_context:paste error or describe issue}

Use the [azl-fix-overlay skill](../skills/azl-fix-overlay/SKILL.md) for overlay failures, the [azl-build-component skill](../skills/azl-build-component/SKILL.md) for build debugging, and the [azl-mock skill](../skills/azl-mock/SKILL.md) for runtime/packaging inspection.

## Triage

First, determine the error category:

1. **Overlay failure** — errors during `prep-sources` or early in build mentioning overlay application, pattern matching, or section/tag not found:
   - Follow the `azl-fix-overlay` workflow: diff pre/post overlay output, diagnose pattern failures, suggest fixes
   - Common causes: upstream spec changed, section renamed/removed, wrong overlay type

2. **Build failure** — compilation errors, missing dependencies, test failures during `comp build`:
   - Follow the `azl-build-component` inner loop: check build logs in `base/build/logs/`, use `--preserve-buildenv on-failure`, inspect mock chroot
   - Common causes: missing BuildRequires, incompatible compiler flags, test failures

3. **Runtime/packaging issue** — wrong file permissions, missing files, dependency conflicts in built RPMs:
   - Follow the `azl-mock` workflow: install RPMs in a mock chroot, verify contents, check dependencies
   - Common causes: missing Requires, wrong file paths, permission issues

**When in doubt**, start with a `prep-sources` pre/post diff to determine if the issue is overlay-related:

```bash
pre=$(mktemp -d) && azldev comp prep-sources -p ${input:component_name} --skip-overlays -o "$pre"
post=$(mktemp -d) && azldev comp prep-sources -p ${input:component_name} -o "$post"
diff -r "$pre" "$post"
```

If `prep-sources` itself fails, the issue is overlay-related (category 1). If it succeeds but `comp build` fails, it's a build issue (category 2).
