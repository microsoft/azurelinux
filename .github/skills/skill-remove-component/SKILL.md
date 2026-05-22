---
name: skill-remove-component
description: "[Skill] Remove components from Azure Linux. Use when deleting packages, cleaning up unused dependencies, or pruning the distro. Triggers: remove component, delete package, drop component, prune dependency."
---

# Remove a Component

## Before You Start

Verify the component exists and understand what it produces:

```bash
azldev comp list -p <name> -q -O json
```

Then check for all artifacts that need to be removed:

1. Component definition — `base/comps/components.toml` (inline) or `base/comps/<name>/<name>.comp.toml` (dedicated)
2. Publish-channel references — `base/comps/components-publish-channels.toml` (component name in `component-groups.base-packages.components`, plus any per-binary entries in `package-groups.exceptions-packages.packages`)
3. Lock file — `locks/<name>.lock`
4. Rendered specs — `specs/<first-char>/<name>/`
5. Other references — image definitions (`base/images/`), `comps.xml`, etc.

## Removal Steps

### 1. Remove the component definition

- **Inline entry**: remove `[components.<name>]` from `base/comps/components.toml`
- **Dedicated directory**: delete `base/comps/<name>/` (contains `<name>.comp.toml` and possibly local spec/sources)

### 2. Remove publish-channel references

Publishing is configured per *component* (not per binary subpackage) in `base/comps/components-publish-channels.toml`. For each component being removed:

- Remove its entry from the `components = [...]` array in `[component-groups.base-packages]` if present (otherwise it inherits the project-wide `sdk` default and needs no edit there).
- Remove any per-binary carve-outs for its subpackages from `[package-groups.exceptions-packages].packages`. Exception lines carry a `# srpm: <name>` trailing comment — grep that to find them all:

```bash
grep "srpm: <name>" base/comps/components-publish-channels.toml
```

Remove every matching line. When removing many components at once, editing by hand is error-prone — prefer using your editor's multi-cursor or find-and-replace to remove all lines matching the SRPM name.

### 3. Remove the lock file

```bash
rm locks/<name>.lock
```

There is no `azldev` command for this — manual deletion is the only way.

### 4. Remove rendered specs

The preferred approach is to let `azldev` handle cleanup after removing the component definition:

```bash
azldev comp render -a --clean-stale
```

This re-renders all components and removes spec directories for components that no longer exist. It's slow (renders everything), but is the most reliable method.

For targeted removal when you don't want to re-render everything:

```bash
rm -rf specs/<first-char>/<name>/
```

### 5. Check for other references

Search for the component name in image definitions, kiwi files, and other config:

```bash
grep -rn "<name>" base/images/ base/comps/comps.xml
grep -rn "<name>" --include="*.kiwi" .
```

Kiwi files (`*.kiwi`) define image package lists — if any subpackage produced by the component is referenced there, it must be removed or replaced before the component can be dropped.

## Verify

After removal, confirm nothing was missed:

```bash
azldev comp list -p <name> -q -O json                              # should fail with "component not found"
grep -n "\"<name>\"\|srpm: <name>" base/comps/components-publish-channels.toml  # should return nothing
ls locks/<name>.lock specs/*/<name>/ 2>/dev/null                   # should return nothing
grep -rn "<name>" --include="*.kiwi" .                  # should return nothing
```

## Notes

- **Check for reverse dependencies** before removing a component. If other components depend on it (via `BuildRequires` or `Requires`), removing it will break their builds.
- **When modifying dependants, check their release calculation.** If you disable a feature or remove a `BuildRequires` from a dependant component that uses `release = { calculation = "manual" }`, you must also bump its release counter (e.g., increment the `azl_release` define). Components with automatic release calculation (`auto`, `static`, `autorelease`) handle this via the commit-render-amend cycle, but manual-release components do not.
- **Publishing is component-scoped, exceptions are binary-scoped.** The `base-packages` group lists *component* names; the `exceptions-packages` group lists *binary RPM* names with `# srpm: <name>` comments. Always search by `# srpm:` comment rather than guessing suffix patterns.
- **This is a metadata-only change.** No builds or tests are needed — the component is simply being dropped from the distro definition.
- **When removing a component and its exclusive dependencies** (packages only needed by the component being removed), remove them all in the same change to keep the tree consistent.
