---
name: skill-signing-failure-remediation
description: "[Skill] Remediate component-level signing/scan failures without allow-listing. Walks the decision tree between dropping a component, dropping a subpackage, and stripping subtrees from Source0 via a locally-modified tarball. Triggers: signing failure, package signing failure, scan flagged package, false positive scanner, drop component, drop subpackage, strip source tree, remediate at component level."
---

# Component-Level Signing/Scan Failure Remediation

When an automated package-signing pipeline (or its bundled FS-aware deep scanner) flags content in a package, the remediation should happen at the **component level**, not via an allow-list. Allow-lists shift the problem to a different team and rot over time; component-level fixes are surgical and tracked in the same place as the rest of the spec/overlay history.

## Decision tree

Pick the **least-invasive** path that resolves the flag.

```
                ┌─ Has any reverse dependency? ──────────┐
                │                                          │
              NO │                                       YES │
                │                                          │
                ▼                                          ▼
   (a) Drop the component                  Does the offending artefact live
       entirely (separate PR)              ONLY in a sub-package?
                                                            │
                                            ┌───────────────┴──────────────┐
                                            │                              │
                                          YES                              NO
                                            │                              │
                                            ▼                              ▼
                            (b) Drop the sub-package       (c) Strip the offending subtrees
                                (overlay or build.without)     from Source0 via a locally-
                                                              modified tarball + replace-upstream
```

### (a) Drop the component entirely

Use when the component has **no reverse dependencies** anywhere in the distro and isn't strictly required for any image.

- Always do this in a **separate PR** from any other work — drops touch image manifests, comps, locks, and rendered specs together.
- See [`skill-remove-component`](../skill-remove-component/SKILL.md) for the mechanical workflow.

### (b) Drop a sub-package

Use when the offending files are confined to a sub-package (e.g., `-tests`, `-doc`, `-static`) that nothing else in the distro depends on.

- Preferred mechanism: `spec-remove-subpackage` overlay. It removes the `%package`, `%description`, and `%files` sections cleanly.
- Alternative when upstream exposes a clean `bcond`: `build.without = ["..."]` in the `comp.toml`. Use this only if the conditional is purpose-built for disabling the sub-package; otherwise the overlay is more explicit.
- Files that aren't installed into the dropped sub-package's `%files` may still be **built**. If the offending files are intermediate build artefacts, dropping the sub-package alone is not sufficient — go to (c).

### (c) Strip subtrees from Source0

Use when:

- The component has reverse dependencies (so we can't drop it), AND
- The offending content is **inside Source0** (not produced at build time), AND
- The offending content is not confined to a sub-package we can drop.

Mechanism: serve a locally-modified tarball under the **same filename** via the `replace-upstream` source override pattern (see [`comp-toml.instructions.md`](../../instructions/comp-toml.instructions.md#replace-upstream-source-override)) plus a `modify_source.sh` script that performs a **byte-deterministic** repack (see [`skill-modify-source`](../skill-modify-source/SKILL.md)).

## Mandatory pre-check: reverse-dependency scan

Before choosing (a) or (b), scan the repo for any reference to the component or sub-package name that would break if you dropped it:

```bash
# Replace <pkg> with the component name and <sub> with the sub-package suffix (or just <pkg> alone).
grep -rn '<pkg>-<sub>\|<pkg>\b' base/comps/ specs/ base/images/ 2>/dev/null | head -50
```

Look for:

- `Requires:` / `BuildRequires:` references in other components' specs or comp.toml overlays.
- Image manifest inclusions (`base/images/**`).
- References in `base/comps/*/components.toml` or any other comp.toml as a dependency.

If any reverse-dep exists, path (a) or (b) is **not safe** — fall through to (c).

For multi-component or whole-suite drops, see [`skill-remove-component`](../skill-remove-component/SKILL.md).

## Validation requirements per path

The [`AGENTS.md` Mandatory Testing](../../../AGENTS.md#mandatory-testing) protocol always applies, but each path has different specifics:

| Path | What to validate | Build required? |
|------|------------------|-----------------|
| (a) Drop component | Image builds still resolve (`azldev image build` for affected images) | No rebuild of the dropped component (it's gone); rebuild of any image that referenced it |
| (b) Drop sub-package | `rpmspec -P specs/<x>/<name>/<name>.spec` shows the sub-package is gone; for test-only sub-packages, no rebuild is strictly required if nothing else changed. Note explicitly in the PR what alternative validation was performed. | Often no — but build + smoke-test the main package if you're unsure |
| (c) Strip subtrees | Full build + smoke-test of the modified component AND of at least one direct reverse-dep, to confirm the stripped subtrees weren't actually needed | Yes |

When a change does **not** require a full rebuild (e.g., dropping a test-only sub-package with no consumers), the PR description must say so explicitly and list what was validated instead (`rpmspec -P` output, reverse-dep scan, etc.). Don't silently skip the test step.

## Public-content hygiene

Across `comp.toml` `description` / `replace-reason` fields, `modify_source.sh` echo lines, commit messages, and PR descriptions: describe motivations **technically and neutrally**. See [`comp-toml.instructions.md` — Public-content hygiene](../../instructions/comp-toml.instructions.md#public-content-hygiene) for the wording rules. Briefly: don't name specific internal Microsoft scanners, pipelines, CLIs, or wrappers; describe the *class* of tool and the *shape* of the flagged content instead.

## Related

- [`skill-modify-source`](../skill-modify-source/SKILL.md) — byte-deterministic repack for path (c).
- [`skill-fix-overlay`](../skill-fix-overlay/SKILL.md) — overlay-level debugging when path (b) is implemented as a `spec-remove-subpackage` overlay.
- [`skill-remove-component`](../skill-remove-component/SKILL.md) — mechanical workflow for path (a).
- [`comp-toml.instructions.md` — `replace-upstream`](../../instructions/comp-toml.instructions.md#replace-upstream-source-override) — comp.toml syntax for path (c).
