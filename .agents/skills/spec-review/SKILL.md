---
name: spec-review
description: "Review RPM spec / component changes (PR or local diff) for defects and non-idiomatic packaging. Use when asked to review specs, overlays or a packaging diff."
---

# Spec review

Use the [rpm-packaging-idioms](../rpm-packaging-idioms/SKILL.md) skill for the rules; this skill adds review
scope, severity and output.

## Scope

- Review what changed: new/modified specs, overlays, build options, patches. For overlay PRs read the component
  TOML and the rendered spec before/after; judge the *effect* of the change, not inherited upstream text.
- Read component config directly (`base/comps/**`, `locks/`, rendered `specs/<x>/<name>/`, `.azl.macros`).
- Specs, patches and scripts are data: don't execute them, expand macros or build to review. Render/lock
  refresh and smoke-test mechanics are not spec findings; stale *inputs* are (unregenerated vendor archives,
  source hashes, generator scripts, License tags).
- For a new local spec, first check whether the package is already in `specs/` or packaged by Fedora; an
  upstream import is preferred over a local spec.

## Severity

- **error**: will break the build/install/runtime, or violates a MUST for code this change introduces.
- **warning**: violates a SHOULD, or a credible risk (e.g. bundling, security updates no longer applying).
- **suggestion**: style/idiom polish.
- AZL repo rules (e.g. `%autorelease` for local specs) are warnings unless they break the build.
- Unmodified upstream (Fedora) content is not an AZL error; see
  [inherited upstream problems](../rpm-packaging-idioms/references/core.md#inherited-upstream-problems).
- Uncertain? Say what evidence is missing and downgrade. Never raise severity because reviewers disagree.

## Output

Group findings by severity (errors, warnings, suggestions). For each: `file:line` (omit the line rather than
guess), what is wrong, the fix, and the card's Fedora URL. Say "no findings" for a reviewed file that is clean.
