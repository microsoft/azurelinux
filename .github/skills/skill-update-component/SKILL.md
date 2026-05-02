---
name: skill-update-component
description: "[Skill] Refresh component lock files with `azldev comp update`. Use when finalizing a component change for PR, bumping an upstream commit pin, or investigating lock-drift CI failures. Triggers: comp update, refresh lock, bump pin, lock drift, version bump, finalize component change."
---

# Update Component Lock Files

`azldev comp update` refreshes one or more component lock files in `locks/`. A lock file pins the upstream commit + an input fingerprint computed from the component's TOML config; if either changes, the lock is stale and the `Update Locks` CI check fails.

## When to run it

| Situation | Run `update`? |
|-----------|---------------|
| Finalizing any component change for PR | **Yes** — once at the end |
| Bumping an upstream commit pin | **Yes** — also mid-workflow (see below) |
| Iterative overlay/build-config/metadata edits | No — `render` alone is enough during iteration *See section on changelog/release quirks in the pin-bump workflow below* |
| Just reading or building existing components | No |

> **Always re-run `update` before opening a PR**, even if all you did was tweak an overlay description. The fingerprint is computed from the full component config, so any TOML change may invalidate the lock.

## End-of-work refresh (the common case)

For most component edits — overlays, build flags, metadata, descriptions — just run `update` once at the end then re-render.

```bash
azldev comp update -p <name>
git add locks/<name>.lock specs/<first-char>/<name>/<name>.spec
git commit -m "fix(pkg): Fix <name> bug"
azldev comp render -p <name>
git add specs/<first-char>/<name>/
git commit --amend --no-edit
```

**NOTE:** The rendered spec is updated immediately after `update` runs, but the `%changelog` and `Release:` fields in the spec are only updated once the new lock is committed. This is the same HEAD-vs-working-tree quirk that trips agents up during pin bumps — see the section below for details. This is only a concern when finalizing edits for a PR; during iterative overlay/build-config/metadata edits the changelog/release fields are not expected to track the working-tree lock.

## Bumping an upstream commit pin

When the goal is to move a component to a new upstream commit, `update` also runs **at the start** to bump the pin. There's a quirk that catches agents out: the rendered spec body and the rendered changelog/release are derived from different sources.

> **Automatic changelog and release calculations are derived from the lock as committed in `HEAD`, not the working tree.** Commit pinning works fine off the working-tree lock, so the spec body tracks the new pin immediately after `update` + `render`. But the changelog entry and release number won't update until the new lock is committed. Don't panic if a freshly-bumped pin's changelog still shows the old version, iterate as needed, then commit the updated lock to see the final changelog and release reflected in the rendered spec.

### Inner loop for a pin bump

```
update → render → iterate → commit lock → render → amend
```

1. **Bump the pin**

  Update a pinned commit, or a snapshot time, then update:

   ```bash
   azldev comp update -p <name>
   git diff locks/<name>.lock   # sanity check the new upstream commit
   ```

2. **Render**

   ```bash
   azldev comp render -p <name>
   ```

   Spec body tracks the new pin. `%changelog` / `Release:` still reflect the previous lock — this is the quirk. Don't panic.

3. **Iterate**
  Adjust overlays/patches/build config as the new upstream version requires. Re-render after each change.

  Re-running update is likely unnecessary during this iteration phase — the working-tree lock already reflects the new upstream commit, and `render` will show the spec body changes immediately. Only re-run `update` if you make changes that would affect the pinned commit itself (for example, changing the upstream commit hash or snapshot time) — otherwise `render` alone is sufficient to see the spec body changes.

4. **Commit the lock**

   ```bash
   azldev comp update -p <name>
   git add locks/<name>.lock
   git commit -m "chore(pkg): update <name> to <ver>"
   ```

5. **Re-render** — now `%changelog` / `Release:` reflect the new lock.

   ```bash
   azldev comp render -p <name>
   ```

6. **Amend** so the lock bump and rendered spec land in a single commit. Stage the whole component directory — render can touch nested sidecars (`.fmf`, `.azl.macros`, etc.) alongside `<name>.spec`:

   ```bash
   git add specs/<first-char>/<name>/
   git commit --amend --no-edit
   ```

## CI gotcha

`Check Rendered Specs` and `Update Locks` both run against the **PR's committed state**, not the working tree. The end-of-work refresh (or the amend in step 6 of a pin bump) is what keeps both checks green together — without it, render check would flag a stale changelog or lock check would flag a stale fingerprint.

## When to use `-a`

Wholesale lock refresh is slow. Use it only when:

- Doing a coordinated mass-bump (e.g., refreshing everything against a new Fedora snapshot).
- Investigating CI lock-drift failures that span many components.

For day-to-day work, always use `-p <name>`.

## Lock Debugging

The update command supports `-O json` for easier reading of the output.

## Related

- [`skill-build-component`](../skill-build-component/SKILL.md) — the standard `edit → render → build → test` loop. `update` is the finalizing step on top of that loop.
- [`skill-fix-overlay`](../skill-fix-overlay/SKILL.md) — when bumping a pin breaks an existing overlay.
- [`skill-mock`](../skill-mock/SKILL.md) — smoke-testing built RPMs after a pin bump.
