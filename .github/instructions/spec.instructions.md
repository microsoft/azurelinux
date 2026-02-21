---
applyTo: "**/*.spec"
---

# RPM Spec Files (`*.spec`)

## When are hand-coded specs appropriate?

Most components import specs from upstream (Fedora) via `*.comp.toml` — hand-coded specs are only for **Azure Linux-originating packages** that don't exist upstream (e.g., `azurelinux-release`, `azurelinux-repos`).

If the package exists upstream, **prefer overlays** over maintaining a forked spec. Overlays get automatic upstream updates and are more resilient to changes. See the `azl-add-component` skill for the decision tree.

## Relationship to `.comp.toml`

A hand-coded spec is referenced from its component definition:

```toml
[components.azurelinux-release]
spec = { type = "local", path = "azurelinux-release.spec" }
```

The spec file lives alongside the `.comp.toml` in the component's directory (`base/comps/<name>/`).

## When you see a spec in `prep-sources` output

Specs in `prep-sources` output directories are **generated output** — they may have overlays applied. Don't edit them directly. To change an upstream spec, modify the overlays in the `.comp.toml` instead.

To see the upstream spec before overlays: `azldev comp prep-sources -p <name> --skip-overlays --force -o my/build/dir/<name> -q`

## Azure Linux conventions

- **Dist tag**: `.azl4` (set via `dist` macro in `azurelinux.distro.toml` build defaults)
- **Vendor**: `Microsoft Corporation` (set via `vendor` macro)
- **`%autorelease`**: preferred for Release tag when appropriate
- **BuildRequires on `azurelinux-rpm-config`**: provides Azure Linux-specific RPM macros
- **License**: use SPDX identifiers

## Debugging a spec

If overlays produce an incorrect spec, use `prep-sources` to compare before/after. See skills `azl-fix-overlay` and `azl-build-component` for step-by-step workflows.
