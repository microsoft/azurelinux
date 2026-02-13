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
| `spec-add-tag` | Add a new tag to spec | `tag`, `value` |
| `spec-set-tag` | Replace existing tag value | `tag`, `value` |
| `spec-update-tag` | Append to existing tag | `tag`, `value` |
| `spec-remove-tag` | Remove a tag | `tag` |
| `spec-prepend-lines` | Insert at start of section body | `section`, `lines` |
| `spec-append-lines` | Insert at end of section body | `section`, `lines` |
| `spec-search-replace` | Regex replace in spec | `regex`, `replacement` |
| `file-add` | Add a file to sources root | `file`, `source` |
| `file-remove` | Remove a file from sources | `file` |
| `file-rename` | Rename a source file | `file`, `replacement` |
| `file-prepend-lines` | Prepend lines to a file | `file`, `lines` |
| `file-search-replace` | Regex replace in source files | `file`, `regex`, `replacement` |

Optional fields that apply to multiple types: `section` (target spec section), `package` (target sub-package).

### Overlay pitfalls

- **Do NOT use inline array syntax for overlays.** Write each overlay as a separate `[[components.<name>.overlays]]` block (array-of-tables), not as `overlays = [{ ... }, { ... }]`. The inline form is valid TOML but harder to read and review. Some older components in the repo use the inline style — don't copy it.
- **No `$schema` in TOML.** `$` is invalid at the start of a bare TOML key.
- **No multi-line regex.** `spec-search-replace` doesn't support `(?s)`/DOTALL. Use multiple single-line replacements.
- **No backreferences in `spec-search-replace`.** `${1}` or `$1` in `replacement` is literal text, not a capture group backreference. Repeat the matched text in the replacement instead.
- **`lines` must be an array of strings.** Use `lines = ["single line"]` or a multi-line array `lines = ["line1", "line2"]`, not a bare string like `lines = "..."`.
- **`file-add` places files at the sources root**, alongside the tarball and other Source files — NOT inside the extracted source tree. To install the added file, also add a `spec-add-tag` for the corresponding `Source` tag and a `spec-append-lines` in `%install` to install it. To modify files inside the extracted tree, use `file-search-replace` or add a `sed` command in `%prep` via `spec-append-lines`.
- **Use TOML literal strings for regex.** `regex = 'RPM_VENDOR=redhat'` avoids double-escaping backslashes.
- **Prefer targeted types over regex.** `spec-add-tag`, `spec-set-tag`, `spec-prepend-lines`, etc. are more robust to upstream changes. Use `spec-search-replace` as a last resort.
- **`spec-prepend-lines` and `spec-append-lines` operate *within* a section body.** `spec-prepend-lines` inserts right after the section header (start of body); `spec-append-lines` inserts at the end of the section body (before the next section). Neither inserts outside the section boundary. For example, to add install commands at the end of `%install`, use `spec-append-lines` with `section = "%install"` — do NOT use `spec-prepend-lines` with `section = "%files"` (that would put the lines inside `%files`).
- **Don't rename `Name:`.** Changing the spec `Name:` tag causes cascading breakage (`%{name}` in Source0, `%setup`, paths, `%files`).
- **`file-search-replace` supports globs.** Use `file = "**/*"` to replace across all source files.

## File Organization

- **Inline** (in `components.toml`): for simple imports with no customization (`[components.jq]`)
- **Dedicated** (`<name>/<name>.comp.toml`): when overlays, build config, or local spec are needed
- Rule of thumb: if it's more than `[components.<name>]`, give it a dedicated file
- `components.toml` has `includes = ["**/*.comp.toml"]` — dedicated files are picked up automatically

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

## Validation

Verify overlays apply cleanly with `azldev comp prep-sources` before committing. See skills `azl-build-component` and `azl-fix-overlay` for step-by-step workflows.
