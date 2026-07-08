---
name: azldev-overlays
description: "Read this before adding, changing, or diagnosing any overlay; never edit a spec or rendered file from memory. Explains how to modify a component's RPM spec or loose source files with azldev overlays (semantic patches applied at render time) instead of forking the spec, covering overlay types, the render-and-inspect loop, common failures, pitfalls, and metadata. Triggers include overlay, overlay failed, no match, spec-add-tag, spec-remove-tag, patch-add, fix spec, backport, disable test, prune subpackage, edit spec."
---

# Working with overlays

Overlays are **semantic patches** applied to a component's RPM spec and loose
source files at render time. They let you make targeted changes to an upstream
spec without forking it. Prefer an overlay over hand-editing a rendered spec:
overlays are re-applied on every render, so a manual edit to a rendered spec is
overwritten.

## The inner loop

Overlays live in the component's TOML config — inline `[[components.<name>.overlays]]`
entries, or per-file overlay documents referenced by the component's `overlay-files`
glob. They apply **in order** and are **non-atomic**: if one fails part-way, the
overlays before it stay applied.

1. Add or edit the overlay in the component config.
2. Re-render and inspect the result:

   ```sh
   azldev comp render -p <name>
   ```

   Read the rendered spec (under `specs/`) to confirm the change
   landed where you intended, and iterate until it is correct.
3. Finalize the lock and changelog with the normal end-of-work refresh (see the
   `azldev-update-component` skill): update the lock, commit, then re-render and amend.

Config errors reference the offending overlay by its `description`, so give every
overlay a short, specific `description`.

## Diagnose common failures

Start with `azldev comp diff-sources -p <name>` to see the exact overlay effect.
Use separate pre/post `prep-sources` directories only when you need persistent trees
for deeper inspection.

| Symptom | Likely cause and fix |
| --- | --- |
| `spec-add-tag`: tag already exists | Upstream already has the tag. Use `spec-set-tag`, or `spec-update-tag` when its prior existence is an invariant. |
| `spec-search-replace`: no match | Inspect the current upstream line, check TOML regex quoting, and narrow the expression to the actual section/package. |
| Section or file not found | Inspect the upstream spec/source names; upstream may have renamed or removed the target. |
| Overlay applies but output/build is wrong | Inspect `diff-sources` for an over-broad match, malformed replacement, or a dependency/file change the overlay omitted. |

## Choosing an overlay type

Match the change to the narrowest overlay type. Required fields are enforced when
the config loads, so a missing field fails fast rather than at apply time.

### Spec overlays (structured `.spec` edits)

| Type | Use for | Required |
| --- | --- | --- |
| `spec-add-tag` | add a tag; fails if it already exists | `tag`, `value` |
| `spec-insert-tag` | add a tag next to its family (e.g. after the last `Source*`) | `tag`, `value` |
| `spec-set-tag` | set a tag, replacing it if present or adding it if not | `tag`, `value` |
| `spec-update-tag` | change an existing tag; fails if it is missing | `tag`, `value` |
| `spec-remove-tag` | delete tag instances; without `value`, deletes every instance | `tag` |
| `spec-prepend-lines` | insert lines at the top of a section (or the whole file) | `lines` |
| `spec-append-lines` | insert lines at the end of a section (or the whole file) | `lines` |
| `spec-search-replace` | regex replace within a section (or the whole spec) | `regex` |
| `spec-remove-section` | delete a whole section | `section` |
| `spec-remove-subpackage` | delete every section of a sub-package | `package` |
| `patch-add` | add a `.patch` file and register it in the spec | `source` |
| `patch-remove` | remove a patch and its spec references | `file` |

### File overlays (loose non-spec files; never `.spec`)

| Type | Use for | Required |
| --- | --- | --- |
| `file-prepend-lines` | prepend lines to a file | `file`, `lines` |
| `file-search-replace` | regex replace in a file | `file`, `regex` |
| `file-add` | copy in a new file; fails if it already exists | `file`, `source` |
| `file-remove` | delete a file | `file` |
| `file-rename` | rename a file in place | `file`, `replacement` |

## Rules that trip people up

- **`spec-remove-tag` without `value` removes every instance** of the named tag.
  To remove one dependency, set both `tag` and the exact `value` to match:

  ```toml
  [[components.mypackage.overlays]]
  description = "Remove an unavailable build dependency"
  type = "spec-remove-tag"
  tag = "BuildRequires"
  value = "unwanted-package"
  ```
- **`section` is optional only** for `spec-prepend-lines`, `spec-append-lines`, and
  `spec-search-replace` (omit it to target the whole spec). It is **required** for
  `spec-remove-section`.
- **`package` needs `section`** on the whole-file-capable overlays — a sub-package is
  a sub-qualifier of a section. `spec-remove-subpackage` is the exception: it takes
  `package` and rejects `section`.
- **`replacement` is literal** — `$1`-style capture-group references are not expanded;
  omit it to delete matched text.
- **Quote `regex` as a TOML literal string** — write `regex = '\.so$'`, not
  `regex = "\.so$"`. A basic (double-quoted) TOML string interprets backslash escapes, so
  `\s`, `\.`, `\d` and friends are mangled before the regex engine ever sees them; single
  quotes keep the pattern verbatim.
- **Anchor regex overlays to whole lines, and prefer macro toggles.** When
  `spec-search-replace` is unavoidable, anchor the full line (for example,
  `regex = '^%setup -q$'`) instead of matching a fragment, and combine several
  near-identical patterns into one rather than stacking brittle overlays. If the
  upstream spec already exposes a conditional such as `%if 0%{?rhel}` /
  `%if 0%{?fedora}` or a definable macro, set that macro instead of rewriting the
  line with regex; the explicit toggle survives upstream changes more reliably.
- **`spec-search-replace` matches one line at a time** — the pattern is applied to each
  spec line independently, so it can never span a newline and `(?s)`/DOTALL does nothing.
  For a multi-line change use a structured spec overlay (`spec-remove-section`,
  `spec-prepend-lines`/`spec-append-lines`, etc.). `file-search-replace` is different: it
  matches against the whole file, so multi-line patterns (and `(?s)`) work there.
- **`file` is a glob** (`**` supported) for the multi-file file overlays; for `file-add`
  and `file-rename` it is a single name, and `file-rename`'s `replacement` is a
  filename only (not a path).
- **`source` paths are relative** to the config that declares the overlay — the overlay
  file when loaded via `overlay-files`, otherwise the component config.
- **`file-add` lands beside the spec**, in the dist-git sources root — not inside the
  extracted upstream tree. Adding a file there does not make the build use it; wire it in
  with a `SourceN` tag plus `%prep`/`%install` steps, or use `patch-add` to change tracked
  sources.
- **Don't rename the `Name:` tag** with `spec-update-tag`/`spec-set-tag`. `%{name}` feeds
  `Source*` URLs, `%setup -n`, and `%files` paths, so renaming it silently breaks those
  references. Keep the spec `Name` aligned with the component instead.
- To add a real `.patch` file (rather than an inline edit), use `patch-add`; it copies
  the `source` into the component sources and registers a `PatchN` tag or `%patchlist`
  entry.

## Document intent with `metadata`

Give non-trivial overlays a `metadata` table. It is documentation only — excluded from
the component fingerprint, so editing it never invalidates the build cache — but it
records *why* the overlay exists and *when* it can be dropped. Every metadata block
requires `category`; pick the narrowest of:

`upstream-backport`, `azl-pruning`, `azl-compatibility`, `azl-temp-workaround`,
`azl-branding-policy`, `azl-disable-flaky-tests`, `azl-disable-unsupported-tests`,
`azl-security-compliance`, `azl-release-management`, `azl-platform-adaptation`.

It also requires `upstream-status`: `upstreamed`, `upstreamable`,
`needs-upstream-hook`, `inapplicable`, or `unknown`. Add `commits` and `bugs` as
`{ url = "https://..." }` entries where they apply. `commits` is required for
`upstream-backport`, whose status must be `upstreamed` or `upstreamable`. When several
overlays share one provenance, put them in a per-file overlay document (`overlay-files`)
with a single file-level `[metadata]`.

## Full reference

The tables above are the working subset. For the exhaustive field rules, metadata
constraints, and the per-file overlay format, generate the machine-readable schema
with `azldev config generate-schema` (see the `ComponentOverlay` definition), or read
azldev's overlays configuration reference.

Generated by `azldev docs agent`; do not hand-edit. Generated for azldev version `v0.1.0`.
