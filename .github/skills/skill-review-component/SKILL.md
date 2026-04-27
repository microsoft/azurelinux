---
name: skill-review-component
description: "[Skill] Review an Azure Linux component definition for hygiene and best practices. Use when reviewing comp.toml files, checking overlay quality, validating file organization, or auditing component definitions. Triggers: review component, check hygiene, audit component, validate comp.toml, component review. NOTE: This skill is a work-in-progress — the checklist below covers basics but the full review workflow is still being refined."
---

# Review a Component

## Review Checklist

### 1. Query the component

```bash
azldev comp list -p <name> -q -O json
```

Review the resolved output for correctness, then dig deeper with query (it's slow since it parses the spec in mock):

```bash
azldev comp query -p <name> -q -O json
```

### 2. File organization

- Components with overlays or any customization SHOULD have a dedicated `<name>/<name>.comp.toml` file
- Component names should match the upstream package name; use `upstream-name` when they differ
- No stale or orphaned files in the component directory

### 3. Overlay quality

- Every overlay MUST have a `description` field explaining *why* the change is needed
- Prefer targeted overlay types (`spec-set-tag`, `spec-add-tag`) over regex (`spec-search-replace`) where possible
  - Regex overlays should be a last resort and must be carefully reviewed for correctness and potential unintended matches. Almost always prefer more specific overlay types that target the exact change needed, rather than broad regex patterns that could match multiple unintended places in the spec on future updates etc.
- When `spec-search-replace` is unavoidable, **make every effort to always scope it** with `section` and/or `package` fields to limit where the regex can match. For example, a replacement targeting a `%files` entry in a sub-package should set `section = "%files"` and `package = "<suffix>"` (the short sub-package suffix as it appears in the spec header, e.g. `"foo"` for `%files foo`, not `"mypkg-foo"`). Unscoped regex overlays are fragile and may silently match unintended lines after upstream updates.
- No multi-line regex patterns (unsupported)
- Use TOML literal strings (`'...'`) for regex to avoid escaping issues
- No unnecessary overlays — if upstream already provides what's needed, don't overlay it

### 4. Naming conventions

- Component name matches upstream package name
- `upstream-name` is set when the component name differs from upstream (e.g., `azurelinux-rpm-config` with `upstream-name = "redhat-rpm-config"`)

### 5. Build configuration

- `build.defines` and `build.without` are used appropriately
- No unnecessary build overrides
- Conditional builds (`build.without`) match available spec conditionals
- **`%check` disabled?** If `build.without` includes `"check"`, flag as a **Warning** — disabling tests is an absolute last resort. Verify that a `skip_reason` is present and clearly explains why the tests cannot be fixed. If the justification is missing or weak, recommend re-enabling `%check` and fixing the underlying test failures instead.
- **`release.calculation = "manual"`?** Verify it's actually needed — the upstream Release tag should use a non-standard macro (e.g., `%{baserelease}`, `%{pkg_release}`) that azldev can't auto-calculate. If the Release tag is a plain integer, `manual` is unnecessary. When `manual` is set, verify there's a corresponding `spec-set-tag` overlay for the Release tag.

### 6. Source configuration

- Spec source type is appropriate (upstream default vs pinned version vs local spec)
- Pinned versions have a reason (comment or overlay description)
- Local specs are a last resort and clearly justified

### 7. Testing verification

- If the change could affect built RPMs, verify they were tested — not just built
- Pure organizational changes (moving definitions, editing comments) don't need a rebuild

## Output

Produce a structured report grouped by severity:

- **Errors:** Must-fix issues (missing overlay descriptions, broken patterns)
- **Warnings:** Should-fix issues (suboptimal overlay types, naming mismatches)
- **Info:** Suggestions and best practices

## Scope of Changes

If the review includes a subset of the file (i.e., git diff), focus on that subset but also consider the overall context to ensure changes fit well with the existing structure and conventions. Offer actionable recommendations for any issues with the changes, but also consider if there are broader improvements that could be made to the component definition as a whole. The goal should be to minimize changes while maximizing maintainability and adherence to best practices. This is a balance - if the proposed change aligns with the existing structure and conventions, it's likely better to keep it as-is even if it's not perfect, rather than suggesting a large refactor that may introduce new issues or require additional testing. However, if the fix would be fairly small and would improve the overall quality and maintainability of the component, it's worth suggesting. Use your judgement to weigh the benefits of the change against the potential risks and effort involved in both making the changes, testing them, and getting final review sign-off from the maintainers (who will likely prefer smaller, incremental improvements over large refactors, especially if the current structure is already reasonably good and the proposed change is more of a "nice to have" than a "must have").
