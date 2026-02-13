---
name: azl-review-component
description: "Review an Azure Linux component definition for hygiene and best practices. Use when reviewing comp.toml files, checking overlay quality, validating file organization, or auditing component definitions. Triggers: review component, check hygiene, audit component, validate comp.toml, component review. NOTE: This skill is a work-in-progress — the checklist below covers basics but the full review workflow is still being refined."
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
