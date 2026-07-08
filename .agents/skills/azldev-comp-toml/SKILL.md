---
name: azldev-comp-toml
description: "Read this before authoring, editing, or reviewing a *.comp.toml file; do not work from memory. Explains the azldev component definition format and review workflow, covering component structure, spec sources, build config, release calculation, render options, file organization, overlay hygiene, stale files, disabled tests, and testing verification. Triggers include comp.toml, component config, review component, component hygiene, spec source, upstream-distro, build defines, release calculation, includes."
---

# Component definition files (`*.comp.toml`)

A component definition tells azldev where a package's spec comes from and how to
customize it for your distro. Every component lives under `[components.<name>]`.

Get the authoritative, always-current field list from the schema:

```sh
azldev config generate-schema
```

## Structure

A bare entry inherits everything from your distro's defaults — most upstream packages
need nothing more:

```toml
[components.curl]
```

Add sub-tables only for what you change. The fields you will reach for most:

| Field | Purpose |
| --- | --- |
| `spec` | where the spec comes from (see below) |
| `overlays` / `overlay-files` | targeted spec/source edits (see the `azldev-overlays` skill) |
| `build.defines` / `build.with` / `build.without` | RPM macro and bcond build tweaks |
| `release.calculation` | how the `Release` tag is managed |
| `render.skip-file-filter` | rendering edge-case escape hatch |

## Spec source

The `spec` field selects where the spec is fetched from. When omitted, the component
inherits the distro default (normally an upstream import).

```toml
# Upstream import (the usual case) — inherits the distro's upstream version
[components.curl]

# Upstream, but pinned to a specific upstream distro/version
[components.curl]
spec = { type = "upstream", upstream-distro = { name = "fedora", version = "rawhide" } }

# Upstream package whose name differs from the component name
[components.mydistro-rpm-config]
spec = { type = "upstream", upstream-name = "redhat-rpm-config" }

# Local spec that lives in your repo (not imported from an upstream distro)
[components.mydistro-release]
spec = { type = "local", path = "mydistro-release.spec" }
```

## Build configuration

```toml
[components.mypackage.build]
defines = { rhel = "11" }      # override RPM macros
with = ["feature_x"]            # enable %bcond_with conditionals
without = ["plugin_rhsm"]       # disable %bcond_with conditionals
```

## Release calculation

`release.calculation` controls the `Release:` tag. There are four modes:

- `auto` (default) — auto-detect whether the spec uses `%autorelease` or a static
  release and handle it accordingly. Correct for most packages.
- `autorelease` — force `%autorelease` handling (use when auto-detection misreads a
  spec that wraps `%autorelease` in a conditional).
- `static` — force static-integer handling and bump the integer on render (the
  inverse of `autorelease`).
- `manual` — you own the `Release:` value. Use this only when render fails with a
  "non-standard Release tag" error. **A `manual` component is not bumped by the
  render/commit/amend cycle, so increment its release yourself in the same change**
  (see the `azldev-update-component` skill).

```toml
[components.mypackage.release]
calculation = "manual"
```

## Render configuration

`render.skip-file-filter = true` keeps all source and patch files during render.
azldev normally prunes files not referenced by the rendered spec; set this only for
the rare spec whose `Source`/`Patch` filenames use macros the filter cannot expand.

## File organization

- **Inline** — put simple, customization-free components directly in a shared config
  file (e.g. `[components.jq]`).
- **Dedicated** — give a component its own `<name>/<name>.comp.toml` once it needs
  overlays, build config, or a local spec. Rule of thumb: anything more than
  `[components.<name>]` earns a dedicated file.
- A parent config picks up dedicated files through an `includes` glob, for example
  `includes = ["**/*.comp.toml"]`.

## Review checklist

Start with `azldev comp list -p <name> -q -O json`, then use
`azldev comp query -p <name> -q -O json` when the review needs parsed spec details.
For a change review, focus on the diff while checking enough surrounding context to
ensure it fits the component and repository conventions.

- **Organization:** The component follows the repository's inline-versus-dedicated-file
  convention; its name matches upstream or sets `spec.upstream-name`; no stale or
  orphaned component files remain.
- **Spec source:** The default upstream source is preferred. Pins explain why they are
  needed, and local specs are used only when overlays cannot express the change.
- **Overlays:** Every overlay explains why it exists. Prefer structured overlay types
  over regex; scope unavoidable `spec-search-replace` expressions by section and, when
  applicable, package, and use TOML literal strings. `spec-search-replace` cannot span
  lines. Remove overlays that upstream has made unnecessary. See the `azldev-overlays` skill.
- **Build config:** Defines and bcond overrides are necessary and correspond to the
  spec. If `build.check.skip = true`, require a specific `build.check.skip_reason` and
  verify that fixing the tests is impractical; skipped `%check` is a last resort.
- **Release mode:** `auto` is the default. Force `autorelease` or `static` only when
  auto-detection is wrong. Use `manual` only for a non-standard release tag, and verify
  the component increments its release itself.
- **Generated state:** The lock matches the final component inputs, and rendered output
  contains the intended changes without unrelated drift.
- **Testing:** Changes that can affect RPM output were built and smoke-tested in a mock
  chroot. Organization, comment, or documentation-only metadata edits do not require a
  rebuild when the resolved component inputs are unchanged.

Report findings by severity: errors for correctness or required-policy violations,
warnings for maintainability risks, and info for optional improvements. Prefer small,
actionable fixes over unrelated cleanup.

## Documenting changes

Add a TOML comment explaining *why* a non-obvious field is set (a version pin, a
workaround), and link the upstream commit or bug when the change is based on one. For
overlays, use the overlay `metadata` table instead (see the `azldev-overlays` skill).

Generated by `azldev docs agent`; do not hand-edit. Generated for azldev version `v0.1.0`.
