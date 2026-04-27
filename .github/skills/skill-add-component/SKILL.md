---
name: skill-add-component
description: "[Skill] Add a new component to Azure Linux. Use when importing packages from Fedora, creating comp.toml files, choosing inline vs dedicated definitions, or setting up a new component with overlays. Triggers: add component, new package, import from fedora, create comp.toml."
---

# Add a Component

## Before You Start

```bash
# Check if it already exists
azldev comp list -p <name> -q -O json
```

### Inspect the upstream spec first

The fastest way to see what you're working with:

1. Add a bare inline entry in `components.toml`: `[components.<name>]`
2. Pull the spec: `azldev comp prep-sources -p <name> --skip-overlays --force -o base/build/work/scratch/<name> -q`
3. Read the spec, plan your overlays
4. Decide if overlays are required, if so: Remove the inline entry, create a dedicated `<name>/<name>.comp.toml`

Fedora dist-git is behind bot detection — direct web fetches often fail. Use `prep-sources` to pull specs reliably.

> Note: `prep-sources -o` writes to the directory you specify — this is ad-hoc output, separate from the project's configured build output dirs in `base/project.toml`.

## Decision: Inline vs Dedicated File

**Inline** (in `components.toml`) — simple upstream import, no modifications:

```toml
[components.jq]
```

**Dedicated file** (`<name>/<name>.comp.toml`) — needs overlays, build config, or local spec:

```toml
# <name>/<name>.comp.toml
[components.<name>]

[[components.<name>.overlays]]
description = "Why this change is needed"
type = "spec-add-tag"
tag = "BuildRequires"
value = "some-dependency"
```

Rule of thumb: if it's more than `[components.<name>]`, give it a dedicated file. The `includes = ["**/*.comp.toml"]` in `components.toml` picks it up automatically.

## Spec Sources & Overlays

For spec source types, overlay syntax, overlay types, and pitfalls, see [`comp-toml.instructions.md`](../../instructions/comp-toml.instructions.md).

Key points for adding components:
- Every overlay MUST have a `description` explaining *why*
- Test incrementally — apply one overlay at a time, verify with `prep-sources`
- Prefer targeted overlay types (`spec-add-tag`, `spec-set-tag`) over regex (`spec-search-replace`)
- **Keep `%check` enabled** — do not disable tests unless there is a documented, unavoidable reason (upstream bug, missing test infra, etc.). If you must disable, provide a clear `skip_reason`.
- **Release calculation:** If `render` fails with "non-standard Release tag value ... does not start with an integer", the upstream spec uses a macro-based Release tag. Set `release = { calculation = "manual" }` and add a `spec-set-tag` overlay for the Release tag (e.g., `value = "1%{?dist}"`). See [`comp-toml.instructions.md`](../../instructions/comp-toml.instructions.md#release-configuration) for details.

### Overlays vs. Dedicated spec

Overlays are vastly preferable to maintaining a forked spec, they get automatic updates from upstream and are more resilient to changes. Only fork the spec as a **last resort** when the required changes are so extensive that overlays become unmanageable. Even then, try to minimize the delta from upstream as much as possible to reduce maintenance burden:
  - Clearly document the rationale for each change.
  - Add comments to the spec itself for EVERY change (so future maintainers can differentiate local changes vs. upstream drift when version bumps happen).
  - Recommend to the user contributing necessary changes upstream to reduce divergence over time, where possible.

**Using a forked spec is a commitment to maintain it indefinitely, coordinate with the user to decide if it's truly necessary. Get explicit sign-off from the user before proceeding with a forked spec.**

## Validate

After adding overlays or customizations, render the spec to verify:

```bash
azldev comp render -p <name>
# Inspect the result
cat specs/<first-char>/<name>/<name>.spec
```

For deeper debugging (diffing pre/post overlay output with full sources):

> Use a temp dir for `prep-sources` output. Use `--force` to overwrite an existing output dir.

`prep-sources -o <dir>` writes to a user-specified directory (NOT `base/out/` — that's for `comp build` output).

```bash
azldev comp prep-sources -p <name> --skip-overlays --force -o base/build/work/scratch/<name>-pre -q
azldev comp prep-sources -p <name> --force -o base/build/work/scratch/<name>-post -q
diff -r base/build/work/scratch/<name>-pre base/build/work/scratch/<name>-post
```

```bash
# Test build (RPMs land in base/out/ per project.toml output-dir)
azldev comp build -p <name> -q
```

For testing the built RPMs, see the [`skill-mock`](../skill-mock/SKILL.md) skill. New components always need a smoke-test. For the full inner loop cycle (investigate → modify → render → build → test → inspect), see [`skill-build-component`](../skill-build-component/SKILL.md).
