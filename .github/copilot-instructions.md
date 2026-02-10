# Azure Linux — Copilot Instructions

Azure Linux is a TOML-defined Linux distribution that imports RPM specs from upstream distros (primarily Fedora) and customizes them via an **overlay system** — no spec forking required. The `azldev` CLI tool drives all component and image workflows.

## Repository Layout

```
azldev.toml                          # Root config — includes distro/ and base/
├── base/                            # The "base" project
│   ├── project.toml                 # Project metadata, output dirs, default distro ref
│   └── comps/                       # Component definitions
│       ├── components.toml          # Main component list (includes **/*.comp.toml)
│       ├── <name>/<name>.comp.toml  # Dedicated component files (when overlays/config needed)
│       └── <name>/                  # May also contain local spec files and overlay sources
├── distro/                          # Distro definitions (shared across projects)
│   ├── azurelinux.distro.toml       # Azure Linux 4.0: default distro, mock configs, build defines
│   ├── distro.toml                  # Includes all *.distro.toml
│   ├── fedora.distro.toml           # Fedora: dist-git URIs, lookaside, version branches
│   └── mock/                        # Mock build environment configs
└── external/schemas/
    └── azldev.schema.json           # Authoritative schema for all TOML config files
```

## Key Concepts

**Components** = unit of packaging (→ one or more RPMs). Spec sources:
- Upstream (default): `[components.curl]` — pulls from Fedora dist-git
- Local: `spec = { type = "local", path = "mypackage.spec" }`
- Pinned upstream: `spec = { type = "upstream", upstream-distro = { name = "fedora", version = "rawhide" } }`

**Overlays** modify upstream specs/sources without forking. Types: `spec-add-tag`, `spec-set-tag`, `spec-update-tag`, `spec-remove-tag`, `spec-prepend-lines`, `spec-append-lines`, `spec-search-replace`, `file-add`, `file-remove`, `file-rename`, `file-prepend-lines`, `file-search-replace`. Schema: [`azldev.schema.json`](../external/schemas/azldev.schema.json).

**TOML include hierarchy**: `azldev.toml` → `distro/distro.toml` + `base/project.toml` → `base/comps/components.toml` → `**/*.comp.toml` (stitched into single namespace).

## azldev CLI Reference

Run all commands from the repo root (where `azldev.toml` lives). Use `azldev --help` and `azldev <command> --help` for current syntax — the tool is under active development.

| Task | Command |
|------|---------|
| List all components | `azldev comp list -a` |
| Query a component | `azldev comp query -p <name>` |
| Add a component | `azldev comp add` |
| Build a component | `azldev comp build -p <name>` |
| Build with local repo | `azldev comp build -p <name> --local-repo ./base/out` |
| Prepare sources (apply overlays) | `azldev comp prep-sources -p <name>` |
| Prepare sources (skip overlays) | `azldev comp prep-sources -p <name> --skip-overlays` |
| Build, keep env on failure | `azldev comp build -p <name> --preserve-buildenv on-failure` |
| List images | `azldev image list` |
| Build an image | `azldev image build` |
| Dump resolved config | `azldev config dump` |

## Repository Hygiene Rules

1. **Overlay descriptions**: Every overlay MUST include a `description` field explaining *why* the change is needed.
2. **Naming**: Component names should match the upstream package name. Use `upstream-name` when the upstream name differs (e.g., `upstream-name = "redhat-rpm-config"` for `azurelinux-rpm-config`).
3. **Schema validation**: The authoritative schema is `external/schemas/azldev.schema.json`. TOML files reference it via `$schema` for editor validation.
4. **Don't edit generated output**: Build artifacts in `build/` and `out/` are generated — never edit them directly.
