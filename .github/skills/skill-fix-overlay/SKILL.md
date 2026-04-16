---
name: skill-fix-overlay
description: "[Skill] Diagnose and fix overlay issues in Azure Linux components. Use when overlays fail to apply, produce unexpected results, or need debugging. Triggers: overlay error, fix overlay, overlay not applying, spec-search-replace failed, overlay debug."
---

# Fix an Overlay

## Diagnosis Workflow

### 1. Render and inspect

The fastest way to check if overlays apply cleanly:

```bash
azldev comp render -p <name>
# Inspect the result
cat specs/<first-char>/<name>/<name>.spec
```

If `render` fails, the error message will identify which overlay failed and why.

### 2. Diff pre/post overlay (deep debug)

When you need to understand exactly what upstream provides vs. what overlays change:

> Use a temp dir for `prep-sources` output. Use `--force` to overwrite an existing output dir.

`prep-sources -o <dir>` writes to a user-specified directory (NOT `base/out/` — that's for `comp build` output).

```bash
azldev comp prep-sources -p <name> --skip-overlays --force -o base/build/work/scratch/<name>-pre -q
azldev comp prep-sources -p <name> --force -o base/build/work/scratch/<name>-post -q
diff -r base/build/work/scratch/<name>-pre base/build/work/scratch/<name>-post
```

### 3. Inspect the upstream spec/sources

Look at the pre-overlay output dir — this is what the overlay is trying to modify. Common root cause: upstream changed and the overlay's assumptions no longer hold.

## Common Failures

### `spec-add-tag`: "tag already exists"

The tag is already in the upstream spec. Fix: use `spec-set-tag` (replaces value if exists, adds if not) or `spec-update-tag` (replaces value, but fails if tag doesn't exist — use when you want to guarantee the tag was already present) instead.

### `spec-search-replace`: no match

The regex doesn't match anything in the spec. Causes:
- Upstream changed the line (check `<pre-dir>/<name>.spec`)
- Regex escaping issues — TOML basic strings need `\\` for literal backslash
- Use TOML literal strings (`'...'`) to avoid escaping: `regex = 'RPM_VENDOR=redhat'`
- **No multi-line regex** — `(?s)`/DOTALL is not supported. Use multiple targeted single-line replacements instead.

### `spec-*-lines`: section not found

The spec section (`%prep`, `%build`, `%install`, etc.) doesn't exist or has different casing. Check the actual section names in `<pre-dir>/<name>.spec`.

### `file-*`: file not found

The file doesn't exist in the upstream sources. Check `ls <pre-dir>/` for actual filenames. Globs (`**/*`) are supported for `file-search-replace`.

### Overlay applies but build still fails

The overlay applied cleanly but the *result* is wrong. Compare `<post-dir>/<name>.spec` against what you expect. Common issues:
- Regex matched more/fewer lines than intended (try to avoid regex, they are brittle)
- Replacement introduced syntax errors in the spec
- Missing dependency that the overlay was supposed to add

For overlay type reference (all 12 types with key fields), see [`comp-toml.instructions.md`](../../instructions/comp-toml.instructions.md#overlay-types). Full schema: [`azldev.schema.json`](../../../external/schemas/azldev.schema.json).

## Tips

- **Test incrementally.** Apply one overlay at a time and verify with `prep-sources`. Debugging 10 overlays at once is painful.
- **Minimize overlays.** Each is a potential failure point. Prefer the smallest delta from upstream.
- **Verify in chroot.** If overlays apply but the build still fails, use [`skill-mock`](../skill-mock/SKILL.md) to inspect the build environment.
- **Follow the inner loop.** The full cycle is: investigate → modify → render → build → test → inspect. See [`skill-build-component`](../skill-build-component/SKILL.md) for details.
- **Smoke-test after fixing overlays.** A clean apply and successful build don't guarantee working RPMs. See [`skill-mock`](../skill-mock/SKILL.md).
