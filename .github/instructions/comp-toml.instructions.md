---
applyTo: "**/*.comp.toml"
---

# Component Definition Files (`*.comp.toml`)

Component definitions tell `azldev` where to find a spec and how to customize it. Schema: [`azldev.schema.json`](../../external/schemas/azldev.schema.json) (or `azldev config generate-schema` for latest).

## Structure

Every component lives under `[components.<name>]`. A bare entry inherits defaults from the distro config:

```toml
[components.curl]
```

### Key fields

| Field | Purpose | Example |
|-------|---------|---------|
| `spec` | Where to find the spec | `{ type = "upstream" }`, `{ type = "local", path = "mypackage.spec" }` |
| `spec.upstream-name` | Upstream package name (if different) | `"redhat-rpm-config"` |
| `spec.upstream-distro` | Pin to a specific distro/version | `{ name = "fedora", version = "rawhide" }` |
| `overlays` | List of spec/source modifications | See Overlays section |
| `release.calculation` | Release tag handling (`"auto"`, `"autorelease"`, `"static"`, or `"manual"`) | `"manual"` |
| `render.skip-file-filter` | Keep all source files during render (edge case) | `true` |
| `build.defines` | RPM macro overrides | `{ rhel = "11" }` |
| `build.with` | Enable build conditionals | `["feature_x"]` |
| `build.without` | Disable build conditionals | `["plugin_rhsm"]` |

## Spec Source Types

```toml
# Upstream (default) — inherits distro's Fedora version
[components.curl]

# Upstream — pinned version
[components.curl]
spec = { type = "upstream", upstream-distro = { name = "fedora", version = "rawhide" } }

# Upstream — different package name
[components.azurelinux-rpm-config]
spec = { type = "upstream", upstream-name = "redhat-rpm-config" }

# Local spec (Azure Linux-originating package)
[components.azurelinux-release]
spec = { type = "local", path = "azurelinux-release.spec" }
```

## Overlays

Overlays modify upstream specs/sources without forking. Every overlay **MUST** have a `description` field explaining *why* the change is needed.

### TOML syntax

Use **array-of-tables** (multi-line) for overlays — one `[[...overlays]]` block per overlay:

```toml
# Targeted type (preferred) — more robust to upstream changes
[[components.curl.overlays]]
description = "Add missing build dependency for Azure Linux"
type = "spec-add-tag"
tag = "BuildRequires"
value = "golang >= 1.21"

# Regex type (last resort) — brittle if upstream changes the line
[[components.rpm.overlays]]
description = "Customize RPM vendor"
type = "spec-search-replace"
regex = "RPM_VENDOR=redhat"
replacement = "RPM_VENDOR=azurelinux"
```

### Overlay types

| Type | Does | Key fields |
|------|------|------------|
| `spec-add-tag` | Add a new tag; **fails if already exists** | `tag`, `value` |
| `spec-insert-tag` | Insert tag after the last tag of the same family (e.g., `Source9999` after last `Source*`); falls back to after last tag of any kind | `tag`, `value` |
| `spec-set-tag` | Set tag value; replaces entire value if exists, adds if not | `tag`, `value` |
| `spec-update-tag` | Replace value of existing tag; **fails if tag doesn't exist** | `tag`, `value` |
| `spec-remove-tag` | Remove a tag; **fails if tag doesn't exist** | `tag`, optionally `value` to match |
| `spec-prepend-lines` | Insert at start of section body | `section`, `lines` |
| `spec-append-lines` | Insert at end of section body | `section`, `lines` |
| `spec-search-replace` | Regex replace in spec (**last resort**) | `regex`, `replacement` |
| `patch-add` | Copy a patch file into sources and register it in the spec (`PatchN` or `%patchlist`) | `source`, optionally `file` |
| `patch-remove` | Remove patch files and their spec references matching a glob | `file` |
| `file-add` | Add a file to sources root | `file`, `source` |
| `file-remove` | Remove a file from sources | `file` |
| `file-rename` | Rename a source file | `file`, `replacement` |
| `file-prepend-lines` | Prepend lines to a file | `file`, `lines` |
| `file-search-replace` | Regex replace in source files | `file`, `regex`, `replacement` |

Optional fields that apply to multiple types: `section` (target spec section), `package` (target sub-package).

**Up-to-date details can be found from the azldev schema command, or by inspecting [azldev.schema.json](../../external/schemas/azldev.schema.json)**.

### Choosing the right overlay type (avoiding regex)

`spec-search-replace` is fragile — it breaks when upstream changes the matched text. Before reaching for regex, check if a targeted type can do the job:

| Task | Use this | NOT this |
|------|----------|----------|
| Add a `BuildRequires` or `Requires` | `spec-add-tag` | regex to insert a line |
| Add a `Source` tag alongside existing ones | `spec-insert-tag` (e.g., `tag = "Source9999"`) | regex to find the last Source line |
| Change `Version`, `Release`, or `Summary` | `spec-set-tag` | regex `s/old/new/` |
| Remove a specific dependency | `spec-remove-tag` with `tag` + `value` | regex to delete the line |
| Add commands at end of `%install` | `spec-append-lines` with `section = "%install"` | regex to find and insert after a line |
| Add entries to `%files` | `spec-append-lines` with `section = "%files"` | regex to append after existing entries |
| Add env/export at start of `%build` | `spec-prepend-lines` with `section = "%build"` | regex to insert before existing content |
| Add a patch | `patch-add` (auto-registers `PatchN` or `%patchlist`) | manual `spec-add-tag` for PatchN + `file-add` |
| Remove a patch | `patch-remove` with glob (e.g., `file = "CVE-*.patch"`) | regex to delete PatchN line + `file-remove` |
| Target a sub-package's `%files` | `spec-append-lines` with `section = "%files"`, `package = "devel"` | regex scoped to a section |

**When regex IS appropriate:** modifying arbitrary text mid-section (e.g., changing a configure flag, replacing a variable value, removing a conditional block). Even then, always scope with `section` and `package` to limit the blast radius.

### Overlay pitfalls

- **Do NOT use inline array syntax for overlays.** Write each overlay as a separate `[[components.<name>.overlays]]` block (array-of-tables), not as `overlays = [{ ... }, { ... }]`. The inline form is valid TOML but harder to read and review. Some older components in the repo use the inline style — don't copy it.
- **No `$schema` in TOML.** `$` is invalid at the start of a bare TOML key.
- **Scope regex overlays with `section` and `package`.** When using `spec-search-replace`, always set `section` (e.g. `"%files"`, `"%install"`) and `package` (e.g. `"foo"` for a `%files foo` section) to limit where the regex matches if possible. The `package` value is the **short sub-package suffix** as it appears after the section tag in the spec (e.g. `%files foo` → `package = "foo"`, not `package = "mypkg-foo"`). Unscoped regex overlays risk matching unintended lines elsewhere in the spec, especially after upstream updates. If the overlay targets a specific sub-package's `%files` section, both fields should be set.
- **No multi-line regex.** `spec-search-replace` doesn't support `(?s)`/DOTALL. Use multiple single-line replacements.
- **No backreferences in `spec-search-replace`.** `${1}` or `$1` in `replacement` is literal text, not a capture group backreference. Repeat the matched text in the replacement instead.
- **`lines` must be an array of strings.** Use `lines = ["single line"]` for single-element lists, or a multi-line array for multiple elements (not a bare string like `lines = "..."`).
    ```toml
    lines = [
        "line 1",
        "line 2",
    ]
    ```
- **`file-add` places files at the sources root**, alongside the tarball and other Source files — NOT inside the extracted source tree. To install the added file, also add a `spec-add-tag` for the corresponding `Source` tag and a `spec-append-lines` in `%install` to install it. To modify files inside the extracted tree, use `file-search-replace` or add a `sed` command in `%prep` via `spec-append-lines`.
- **Use TOML literal strings for regex.** `regex = 'RPM_VENDOR=redhat'` avoids double-escaping backslashes.
- **Prefer multi-line format for TOML arrays.** When a list field (`lines`, `with`, `without`, etc.) has 2+ elements, split it across multiple lines with a trailing comma for readability:
    ```toml
    lines = [
        "# Comment explaining the change",
        "rm -f broken_test",
    ]
    ```
- **Prefer targeted types over regex.** `spec-add-tag`, `spec-set-tag`, `spec-prepend-lines`, etc. are more robust to upstream changes. Use `spec-search-replace` as a last resort.
- **`spec-prepend-lines` and `spec-append-lines` operate *within* a section body.** `spec-prepend-lines` inserts right after the section header (start of body); `spec-append-lines` inserts at the end of the section body (before the next section). Neither inserts outside the section boundary. For example, to add install commands at the end of `%install`, use `spec-append-lines` with `section = "%install"` — do NOT use `spec-prepend-lines` with `section = "%files"` (that would put the lines inside `%files`).
- **Don't rename `Name:`.** Changing the spec `Name:` tag causes cascading breakage (`%{name}` in Source0, `%setup`, paths, `%files`).
- **`file-search-replace` supports globs.** Use `file = "**/*"` to replace across all source files.

## File Organization

- **Inline** (in `components.toml`): for simple imports with no customization (`[components.jq]`)
- **Dedicated** (`<name>/<name>.comp.toml`): when overlays, build config, or local spec are needed
- Rule of thumb: if it's more than `[components.<name>]`, give it a dedicated file
- `components.toml` has `includes = ["**/*.comp.toml"]` — dedicated files are picked up automatically
- **When moving a component out of inline `components.toml` into a dedicated `<name>.comp.toml` file, DELETE the inline entry.** Don't leave a "moved to X" pointer comment. Discovery is automatic via the `**/*.comp.toml` include glob.
- **When removing a component outright, DELETE the inline entry.** No tombstone comments.

## `replace-upstream` Source Override

When a component must serve a **locally-modified** Source0 (or any other source) under the **same filename** as the upstream sources manifest declares, use a `[[components.<name>.source-files]]` block with `replace-upstream = true`. This swaps the same-named entry in the Fedora `sources` manifest **in place** during render — there is **no** separate `file-remove` overlay needed against the `sources` file, and no need to invent a new filename.

```toml
[[components.examplepkg.source-files]]
filename = "examplepkg-1.2.3.tar.xz"
hash = "<sha512 of LOCALLY-MODIFIED tarball>"
hash-type = "SHA512"
replace-upstream = true
replace-reason = "Upstream tarball ships a vendored copy of a third-party library plus a 'tests/network' tree that trip an automated package-signing pipeline's deep scanner. Repacked under the same filename with those subtrees stripped via base/comps/examplepkg/modify_source.sh; the surviving bits are byte-identical to upstream so the build is unaffected."

[components.examplepkg.source-files.origin]
uri = "https://azltempstaginglookaside.blob.core.windows.net/repo/pkgs_modified/examplepkg/examplepkg-1.2.3.tar.xz/sha512/<same-sha512-as-hash-field>/examplepkg-1.2.3.tar.xz"
```

### Required field semantics

| Field | Notes |
|-------|-------|
| `filename` | Must match the upstream Source0/N filename exactly. That's how the override is keyed. |
| `hash` | SHA-512 of the **locally-modified** tarball. Lowercase hex. |
| `hash-type` | `"SHA512"`. |
| `replace-upstream` | `true`. Tells render to swap the same-named entry in the upstream manifest instead of appending a new one. |
| `replace-reason` | Single TOML string (basic or literal, not triple-quoted/multi-line). Must self-contain the full WHY so no TOML comment is needed in addition. See "`replace-reason` style" below. |
| `origin.uri` | Lookaside URL. The `$hash` path segment MUST be the **same SHA-512** as the `hash` field. |

### Lookaside URL pattern

```
https://azltempstaginglookaside.blob.core.windows.net/repo/pkgs_modified/$pkg/$filename/$hashtype/$hash/$filename
```

- `$pkg` = component name (e.g., `examplepkg`)
- `$filename` = upstream Source0 filename (appears twice)
- `$hashtype` = `sha512` (lowercase in the URL even though the TOML field is `"SHA512"`)
- `$hash` = same SHA-512 as `hash`. If they ever diverge, the upload at one URL won't be findable from the other.

### `replace-reason` style

- A **single-line TOML string** (basic `"..."` or literal `'...'`). No triple-quoted / multi-line strings.
- Self-contained: must include *what* was changed and *why* clearly enough that no separate TOML comment is needed.
- Use **neutral, public-safe wording** for the motivation. Phrases like "automated package-signing pipeline", "FS-aware deep scanner", "automated malware scan" are fine. Do **not** name specific internal Microsoft scanners, pipelines, CLIs, tenants, or wrappers. Describe the *shape* of the bad content (what subtrees / what scanner class flagged it), not the brand of the tool.
- One short banner-style line at the very top of the `*.comp.toml` summarizing the override is fine. **Multi-paragraph header comments are not** — keep the explanation inside `replace-reason`.

### What render emits

Render emits an audit `WARN`-level log entry naming the override and the from/to SHA-512 pair. That is **expected and desired** — it makes overrides discoverable in render output.

### How the modified tarball is produced

Use a `modify_source.sh` script alongside the `*.comp.toml`. The script MUST be byte-deterministic (same input → same hash, across machines and re-runs), or the lookaside URL and the `hash` field will drift on every re-pack. The canonical pattern is documented in [`skill-modify-source`](../skills/skill-modify-source/SKILL.md).

## Public-content hygiene

In committed content — `*.comp.toml` files (overlay `description`, `replace-reason`, etc.), local `*.spec` files, `modify_source.sh` scripts, commit messages, PR descriptions — describe motivations **technically and neutrally**. Do not name specific Microsoft-internal infrastructure (signing services, scanner brand names, internal pipeline names, internal CLI wrappers, internal Azure tenants, etc.) by name.

Use neutral phrasing instead:

| Avoid | Prefer |
|-------|--------|
| Brand name of an internal signing service | "automated package-signing pipeline" |
| Brand name of an internal malware scanner | "FS-aware deep scanner", "automated malware scan" |
| Names of internal CI/CD pipelines or wrappers | "the build pipeline", or just `azldev` for tool references |

The technical *what* (the shape of the content that's being changed, the class of scanner that flagged it, the nature of the false positive) belongs in the description. The internal *brand* does not.

## Build Configuration

```toml
# Override RPM macros
[components.wget2.build]
defines = { rhel = "11" }

# Enable build conditionals
[components.mypackage.build]
with = ["feature_x"]

# Disable build conditionals
[components.dnf5.build]
without = ["plugin_rhsm"]
```

### Build-flag overrides: don't duplicate distro-level disablement

Several build flags are applied across many components via shared **disablement groups** rather than per-component `[components.<name>.build]` blocks. Before adding a `build.without` / `build.with` / `build.defines` override to a `*.comp.toml`, check whether the same flag is already applied at one of these layers — duplicating it in the per-component file is redundant and creates two sources of truth that can drift.

Check these layers, in order:

1. **`base/comps/component-mingw-disablement.toml`** — applies `build.without = ["mingw"]` to every component listed under `[component-groups.mingw-disabled]` via the group's `default-component-config.build` block. Azure Linux does not ship mingw cross-compilation toolchains; any component whose upstream spec has a `mingw` bcond should be added to that list, **not** carry its own `without = ["mingw"]`.
2. **`base/comps/component-check-disablement.toml`** — applies `build.check = { skip = true, ... }` to components listed under `[component-groups.check-skip-initial-failures]` (initial-bringup `%check` failures). Don't duplicate the check skip in a per-component file.
3. **Any other `component-*-disablement.toml`** under `base/comps/` — the pattern is `[component-groups.<group-name>.default-component-config.build]`.
4. **`distro/azurelinux.distro.toml`** — `[distros.azurelinux.versions.'<ver>'.default-component-config]` blocks set distro-wide defaults that every component inherits unless explicitly overridden.

If the desired build flag is already applied at any of those layers, **do not duplicate it in the per-component file**. If you're moving a component from an inline entry in `components.toml` into a dedicated `<name>.comp.toml` and the original inline entry had no `build` block, the dedicated file should also not have one — let the group / distro defaults apply.

Conversely, only add a per-component `[components.<name>.build]` block when the flag genuinely diverges from what the disablement groups and distro defaults already provide (e.g., a `with` that isn't shared by other components, a `defines` specific to this package).

## Release Configuration

By default (`release.calculation = "auto"`), `azldev` auto-calculates the `Release` tag during rendering. There are four modes:

### `auto` (default)

Auto-detects whether the spec uses `%autorelease` or a static release value and handles it accordingly. Works for most packages.

### `autorelease`

Forces `azldev` to treat the spec as using `%autorelease`, preserving the `%autorelease` macro in the rendered spec. Use this when auto-detection gets it wrong — typically when the spec wraps `%autorelease` in a conditional:

```spec
%if %{defined autorelease}
Release: %autorelease
%else
Release: 1
%endif
```

In this pattern, auto-detection may see the conditional and misidentify the release mode, expanding `%autorelease` to a hardcoded integer. Setting `calculation = "autorelease"` forces correct behavior:

```toml
[components.gvisor-tap-vsock]
# Upstream spec uses conditional %autorelease — auto-detection misidentifies it
[components.gvisor-tap-vsock.release]
calculation = "autorelease"
```

**When to use `autorelease`:** When `render` produces a hardcoded integer where `%autorelease` should be, or when the spec has conditional `%autorelease` logic that confuses auto-detection.

### `static`

Forces `azldev` to treat the spec as using a static (hardcoded) release value, even if auto-detection thinks it uses `%autorelease`. Uses a regex to match release patterns like `5.%{dist}` and bumps the integer component automatically during rendering. The inverse of `autorelease` — use when auto-detection incorrectly identifies a static release as `%autorelease`.

```toml
[components.mypackage.release]
calculation = "static"
```

**When to use `static`:** When auto-detection misidentifies a static release as `%autorelease` and produces incorrect rendering (e.g., inserts `%autorelease` where a hardcoded integer release should be).

### `manual`

Some upstream specs use non-standard Release tag values (e.g., `%{baserelease}%{?dist}`, `%{pkg_release}`) that the auto-calculator can't parse. These fail with:

```
non-standard Release tag value ... does not start with an integer
```

Fix: set `release.calculation = "manual"` and add a `spec-set-tag` overlay to set a concrete Release value:

```toml
[components.gcc]
release = { calculation = "manual" }

[[components.gcc.overlays]]
description = "Set explicit Release tag — upstream uses %{gcc_release} macro which azldev cannot auto-calculate"
type = "spec-set-tag"
tag = "Release"
value = "1%{?dist}"
```

**When to use `manual`:** Only when `render` fails with the "non-standard Release tag" error. Don't preemptively set it — most packages work fine with `auto`.

**When using `manual`:** You take ownership of bumping the Release value when needed (e.g., rebuild without a version change). The auto-calculator will not touch it.

## Render Configuration

The `render` section controls spec rendering behavior. Currently has one field:

```toml
[components.mypackage.render]
skip-file-filter = true
```

`skip-file-filter` disables post-render file filtering. During rendering, `azldev` normally prunes source/patch files not referenced by the rendered spec. If a spec uses unexpandable macros in `Source` or `Patch` tags (e.g., `Source0: %{name}-%{version}%{?prerelease}.tar.gz`), the filter can't resolve the filename and may incorrectly remove needed files. Setting `skip-file-filter = true` keeps all files. The tool auto-detects unexpandable macros and handles them correctly in the vast majority of cases - this is an edge case escape hatch that should almost never be needed in practice.

## Descriptions over comments

Several `.comp.toml` fields carry a free-form rationale string per the schema (`external/schemas/azldev.schema.json`): overlays take `description`, `replace-upstream` takes `replace-reason`, check skips take `skip_reason`, and so on. **Prefer those structured fields over TOML comments** — they're schema-validated, greppable, and surfaced in render diagnostics.

**Keep every rationale brief.** State *why* the change is needed in one short line. Do not narrate the implementation — the field body shows the *what*, the description supplies the *why*. A reviewer should be able to skim the description list and form a high-level picture of the divergence without reading code.

DO:

```toml
[[components.mypackage.overlays]]
type = "spec-remove-subpackage"
description = "Drop -doc subpackage; conflicts with system docs."
name = "doc"
```

DO NOT:

```toml
[[components.mypackage.overlays]]
type = "spec-remove-subpackage"
description = "Remove the -doc subpackage using spec-remove-subpackage, which deletes the matching %package, %description and %files blocks; this is needed because the docs conflict with the system-wide ones."
name = "doc"
```

### When TOML comments are appropriate

Avoid TOML comments by default. They aren't schema-validated, aren't surfaced anywhere except in the raw file, and drift over time. Reach for them only when no schema field can carry the rationale — e.g., justifying a non-default `upstream-distro` pin, or attaching a URL to a one-off block. Keep them as brief as a description: one short line, plus an optional URL.

DO:

```toml
# Pinned to rawhide — needs feature X (not yet in stable).
spec = { type = "upstream", upstream-distro = { name = "fedora", version = "rawhide" } }
```

DO NOT:

```toml
# This component depends on feature X from upstream which was added in rawhide
# but has not yet been backported to a stable Fedora release. Once the feature
# is available in a stable release (Fedora 42 or later expected), we should
# re-align this pin.
spec = { type = "upstream", upstream-distro = { name = "fedora", version = "rawhide" } }
```

### References

When a change is driven by an external source (upstream bug, commit, changelog entry), include the URL — inside the `description` if it fits, otherwise as a single-line comment above the field. Prefer full URLs for clickability.

```toml
# Fixed upstream in my-package-1.2.3 (rawhide): https://src.fedoraproject.org/rpms/my-package/c/abcdef123456 (rhbz#1234567)
[[components.mypackage.overlays]]
description = "Fix build failure from missing dep added in my-package-1.2.3."
...
```

## Validation

Verify overlays apply cleanly with `azldev comp prep-sources` before committing. See skills `skill-build-component` and `skill-fix-overlay` for step-by-step workflows.
