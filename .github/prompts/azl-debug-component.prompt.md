---
description: "Debug a component build failure or overlay error"
---

# Debug Component: `${input:component_name:package name}`

Debug issues with **${input:component_name}**.

Error context: ${input:error_context:paste error or describe issue}

Use the [skill-fix-overlay skill](../skills/skill-fix-overlay/SKILL.md) for overlay failures, the [skill-build-component skill](../skills/skill-build-component/SKILL.md) for build debugging, and the [skill-mock skill](../skills/skill-mock/SKILL.md) for runtime/packaging inspection.

## Triage

First, determine the error category:

1. **Overlay failure** — errors during `prep-sources` or early in build mentioning overlay application, pattern matching, or section/tag not found:
   - Follow the `skill-fix-overlay` workflow: diff pre/post overlay output, diagnose pattern failures, suggest fixes
   - Common causes: upstream spec changed, section renamed/removed, wrong overlay type

2. **Build failure** — compilation errors, missing dependencies, test failures during `comp build`:
   - Follow the `skill-build-component` inner loop: check build logs in `base/build/logs/`, use `--preserve-buildenv on-failure`, inspect mock chroot
   - Common causes: missing BuildRequires, incompatible compiler flags, test failures
   - **`%check` failures:** Always attempt to fix failing tests first. Disabling `%check` (via `build.without = ["check"]`) is an **absolute last resort** — only after exhausting other options. If you must disable it, the `skip_reason` must clearly explain why the tests cannot be fixed.

3. **Runtime/packaging issue** — wrong file permissions, missing files, dependency conflicts in built RPMs:
   - Follow the `skill-mock` workflow: install RPMs in a mock chroot, verify contents, check dependencies
   - Common causes: missing Requires, wrong file paths, permission issues

**When in doubt**, start with a `prep-sources` pre/post diff to determine if the issue is overlay-related:

```bash
azldev comp prep-sources -p ${input:component_name} --skip-overlays -o base/build/work/scratch/${input:component_name}-pre --force
azldev comp prep-sources -p ${input:component_name} -o base/build/work/scratch/${input:component_name}-post --force
diff -r base/build/work/scratch/${input:component_name}-pre base/build/work/scratch/${input:component_name}-post
```

If `prep-sources` itself fails, the issue is overlay-related (category 1). If it succeeds but `comp build` fails, it's a build issue (category 2).

## Fix

**IF** a request has been made to fix the issue, attempt a fix. Before declaring success, ensure the fix actually resolves the issue by running tests. Also, queue a sub-agent and tell it to use the `skill-review-component` skill to review the fix and confirm it follows best practices and won't cause future maintenance issues. If the review agent raises concerns, address them, and then re-run the review (repeat as needed).
