---
applyTo: "base/comps/**"
description: "Packaging idioms for component changes. Read when writing or changing a spec, overlay, build option or patch under base/comps."
---

# Packaging idioms: required check

You MUST do this check before declaring any change under `base/comps/` done, ready to push or reviewed: a new or
changed spec, an overlay, a `build` define/with/without, a patch, a source or version bump. "Small" changes
are not exempt; one-line overlays and version bumps break the most things.

1. Open `.agents/skills/rpm-packaging-idioms/SKILL.md` and follow it.
2. Changing an existing component? Go through **every row** of `references/overlay-hazards.md`.
3. Open every ecosystem card whose signals appear in the spec, overlay or patch, and go through **every row**.

Do not stop after the first few problems. Finish the rows.
