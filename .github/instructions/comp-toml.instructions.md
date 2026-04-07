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
| `spec-add-tag` | Add a new tag; **fails if already exists** | `tag`, `value` |
| `spec-insert-tag` | Insert tag after the last tag of the same family (e.g., `Source9999` after last `Source*`); falls back to after last tag of any kind | `tag`, `value` |
| `spec-set-tag` | Set tag value; replaces entire value if exists, adds if not | `tag`, `value` |
| `spec-update-tag` | Replace value of existing tag; **fails if tag doesn't exist** | `tag`, `value` |
| `spec-remove-tag` | Remove a tag; **fails if tag doesn't exist** | `tag`, optionally `value` to match |
| `spec-prepend-lines` | Insert at start of section body | `section`, `lines` |
| `spec-append-lines` | Insert at end of section body | `section`, `lines` |
| `spec-search-replace` | Regex replace in spec (**last resort**) | `regex`, `replacement` |
| `spec-remove-section` | Remove an entire section (header + body); **fails if section doesn't exist** | `section`, optionally `package` |
| `patch-add` | Copy a patch file into sources and register it in the spec (`PatchN` or `%patchlist`) | `source`, optionally `file` |
| `patch-remove` | Remove patch files and their spec references matching a glob | `file` |
| `file-add` | Add a file to sources root | `file`, `source` |
| `file-remove` | Remove a file from sources | `file` |
| `file-rename` | Rename a source file | `file`, `replacement` |
| `file-prepend-lines` | Prepend lines to a file | `file`, `lines` |
| `file-search-replace` | Regex replace in source files | `file`, `regex`, `replacement` |

Optional fields that apply to multiple types: `section` (target spec section), `package` (target sub-package).

This table is a **quick reference, not exhaustive**. The canonical overlay documentation is upstream: https://github.com/microsoft/azure-linux-dev-tools/blob/main/docs/user/reference/config/overlays.md

The schema can also be inspected locally via `azldev config generate-schema` or [azldev.schema.json](../../external/schemas/azldev.schema.json).

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
| Disable a build feature with bcond toggle | `build.without = ["feature"]` | regex to modify conditional |
| Remove an entire subpackage | `spec-remove-section` (×3: `%package`, `%description`, `%files`) | commenting out or `%if 0` wrapping |
| Disable a feature in a source config file | `file-search-replace` on the config file | `spec-search-replace` |

**When regex IS appropriate:** modifying arbitrary text mid-section (e.g., changing a configure flag, replacing a variable value, removing a conditional block). Even then, always scope with `section` and `package` to limit the blast radius.

### Overlay pitfalls

- **Do NOT use inline array syntax for overlays.** Write each overlay as a separate `[[components.<name>.overlays]]` block (array-of-tables), not as `overlays = [{ ... }, { ... }]`. The inline form is valid TOML but harder to read and review. Some older components in the repo use the inline style — don't copy it.
- **No `$schema` in TOML.** `$` is invalid at the start of a bare TOML key.
- **`spec-search-replace` cannot match section tags.** `%package`, `%description`, `%files`, and other section headers are structural elements parsed by the spec engine, not matchable text. To remove an entire subpackage, use `spec-remove-section` with `section` and `package` fields — one overlay per section type (`%package`, `%description`, `%files`).
- **`file-search-replace` targets source files, not the spec.** It operates on files alongside the spec (Source0, Source1, etc. and loose files like build configs) — NOT on the `.spec` file itself. Use `spec-search-replace` for spec modifications.
- **Scope regex overlays with `section` and `package`.** When using `spec-search-replace`, always set `section` (e.g. `"%files"`, `"%install"`) and `package` (e.g. `"foo"` for a `%files foo` section) to limit where the regex matches if possible. The `package` value is the **short sub-package suffix** as it appears after the section tag in the spec (e.g. `%files foo` → `package = "foo"`, not `package = "mypkg-foo"`). For specs using `-n` naming (e.g. `%package -n %{name}+foo`), use the **unexpanded macro form**: `package = "%{name}+foo"`. Unscoped regex overlays risk matching unintended lines elsewhere in the spec, especially after upstream updates. If the overlay targets a specific sub-package's `%files` section, both fields should be set.
- **No multi-line regex.** `spec-search-replace` doesn't support `(?s)`/DOTALL. Use multiple single-line replacements.
- **Blank lines from empty replacements break continuations.** Replacing a line's content with `''` leaves a blank line. In RPM macro heredocs with `\` continuation, this breaks the chain. Either replace with the next entry's text or use a different overlay type.
- **Replacement string escaping differs from regex.** In TOML literal strings, regex `'\\'` matches `\` in the spec, but `'\\'` in `replacement` produces `\\` in output. Use `'\'` in replacement to get `\`.
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

## Adding Description Comments

When adding or modifying fields in a `.comp.toml` file, check the schema (`external/schemas/azldev.schema.json`) for a `description` on that field. If the schema field **does not** have a `description` key (or equivalent, i.e. `skip_reason` for check skip), add a TOML comment above the field explaining what it does and why it's set to that value. This helps future readers (human and agent) understand fields that aren't self-documenting via the schema.

**BUT**... don't add pointless noise - if the change is self-explanatory and requires no additional context, a comment may not be necessary. Use your judgement, but when in doubt, add a comment.

DO:

```toml
# Pin to Fedora rawhide since we need feature 'x' that is not in stable releases yet.
# Re-align to a stable release once the feature is backported or a new release is available.
spec = { type = "upstream", upstream-distro = { name = "fedora", version = "rawhide" } }
```

Offers important context about *why* the component is pinned to rawhide, which is not obvious from the TOML field alone. Future readers will understand the rationale and know to check for backports or new releases to remove the rawhide pin.

DO NOT:

```toml
# Need new stuff.
spec = { type = "upstream", upstream-distro = { name = "fedora", version = "rawhide" } }
```

This offers no real information beyond what the TOML field already says, and doesn't explain *why* the new stuff is needed, or what that new stuff is. It's just noise.

### References

When making changes based on external information (e.g. a bug report, an upstream commit, a changelog entry, etc.), include a link to the relevant source in a comment (prefer full URL for ease of use). This provides valuable context for future readers to understand the reasoning behind the change and investigate further if needed. It also makes it easier to determine if the change is still relevant or if there have been updates since.

```toml
# ...
# Fixed upstream in my-package-1.2.3 (rawhide): https://src.fedoraproject.org/rpms/my-package/c/abcdef123456 (rhbz#1234567)
[[components.mypackage.overlays]]
description = "Fix build failure due to missing dependency that was added in my-package-1.2.3"
...
```

## Validation

Verify overlays apply cleanly with `azldev comp prep-sources` before committing. See skills `skill-build-component` and `skill-fix-overlay` for step-by-step workflows.
