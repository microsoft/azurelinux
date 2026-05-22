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

For most component edits — overlays, build flags, metadata, descriptions — run `update` once at the end, then re-render *after committing* so the changelog and release reflect your new commit.

```bash
azldev comp update -p <name>
azldev comp render -p <name>
git add base/comps/<name>/ locks/<name>.lock specs/<first-char>/<name>/
git commit -m "fix(pkg): Fix <name> bug"

# Now re-render and amend so %changelog / Release: track the new commit.
azldev comp render -p <name>
git add specs/<first-char>/<name>/
git commit --amend --no-edit
```

### Why the second render-and-amend?

> **`%changelog` and `Release:` are derived from `git log` for the component, not from the working tree.** rpmautospec walks the commit history every time it renders. The first render happens before your commit exists, so it produces a spec keyed off `HEAD`. The moment you `git commit`, the rendered output drifts — a fresh render will add a new `%changelog` entry for your commit and bump the `Release:` integer. Without the post-commit re-render and amend, the `Check Rendered Specs` CI check will fail with that exact diff.

This applies to **every** commit that touches a component or its lock -- pin bumps, overlay tweaks, build-config changes, metadata edits. There's nothing special about pin bumps.

During iterative work (before any commit) the changelog/release fields are not expected to track the working tree. Only worry about the post-commit re-render once you're finalizing for a PR.

> **Manual release components:** Keep the same post-commit re-render/amend workflow when finalizing, because rpmautospec-generated `%changelog` can still drift after you commit. The difference is that components with `release = { calculation = "manual" }` do **not** get their `Release:` value bumped automatically by that cycle. When modifying such a component, you must **manually increment** its release counter in the same change (for example via an `azl_release` define or a `spec-set-tag` overlay value). Check the component's `release.calculation` field before finalizing — if it's `manual`, do the re-render/amend step and bump the release counter yourself.

## Bumping an upstream commit pin

Pin bumps follow the same rule as every other change: the changelog/release fields are derived from `git log`, so you need a post-commit re-render. The pin-bump variant just splits the work across two commits (lock first, then iterate, then amend), and adds an *extra* up-front `update` to move the pin.

> **Recap:** automatic changelog and release calculations are derived from `git log` for the component. Commit pinning works fine off the working-tree lock, so the spec body tracks the new pin immediately after `update` + `render`. But the changelog entry and release number won't reflect your work until your commit lands on the branch and you re-render. Don't panic if a freshly-bumped pin's changelog still shows the old version mid-loop -- iterate as needed, commit the lock, then re-render to see the final changelog and release.

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

   Spec body tracks the new pin. `%changelog` / `Release:` still reflect the previous lock — that's expected, your bump isn't committed yet.

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
