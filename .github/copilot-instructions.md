# Azure Linux — Copilot Instructions

Azure Linux is a TOML-defined Linux distribution that imports RPM specs from upstream distros (primarily Fedora) and customizes them via an **overlay system** — no spec forking required. The `azldev` CLI tool drives all component and image workflows.

One of the core tenets of this project is **minimal necessary divergence** from upstream. Overlays should be surgical and only change what's needed to meet Azure Linux requirements. Upstream packages should be preferred over bespoke components, and local specs should be a last resort. This keeps maintenance overhead low and makes it easier to pull in new versions and security updates from upstream.

## Repository Layout

```
azldev.toml                          # Root config — includes distro/ and base/
├── base/                            # The "base" project
│   ├── project.toml                 # Project metadata, output dirs, default distro ref
│   ├── out/                         # Built RPMs/SRPMs (configured by output-dir in project.toml)
│   ├── build/                       # Build artifacts (configured by log-dir, work-dir)
│   │   ├── logs/                    # Build logs
│   │   └── work/<name>/             # Per-component working directories
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

**Components** = unit of packaging (→ one or more RPMs). Spec sources: upstream (default, from Fedora dist-git), local, or pinned upstream. See [`comp-toml.instructions.md`](instructions/comp-toml.instructions.md#spec-source-types) for syntax.

**Overlays** modify upstream specs/sources without forking. See [`comp-toml.instructions.md`](instructions/comp-toml.instructions.md#overlays) for types, syntax, and pitfalls. Schema: [`azldev.schema.json`](../external/schemas/azldev.schema.json).

**TOML include hierarchy**: `azldev.toml` → `distro/distro.toml` + `base/project.toml` → `base/comps/components.toml` → `**/*.comp.toml` (stitched into single namespace).

## azldev CLI Reference

Run all commands from the repo root (where `azldev.toml` lives). If the terminal's cwd has drifted, use `azldev -C /path/to/repo <command>`. Use `azldev --help` and `azldev <command> --help` for current syntax — the tool is under active development.

**Agent-friendly flags:** Use `-q` (quiet) to reduce noise and `-O json` for machine-parseable output. These are global flags and work on all commands.

| Task | Command |
|------|---------|
| List all components | `azldev comp list -a -q -O json` |
| List a specific component | `azldev comp list -p <name> -q -O json` |
| List with wildcard | `azldev comp list -p "azurelinux*" -q -O json` |
| Query a component (parsed spec, slow) | `azldev comp query -p <name> -q -O json` |
| Add a component | `azldev comp add` |
| Build a component | `azldev comp build -p <name> -q` |
| Build chain (auto-publish to local repo) | `azldev comp build --local-repo-with-publish ./base/out -p <a> -p <b> -q` |
| Prepare sources (apply overlays) | `azldev comp prep-sources -p <name> -o <dir> -q` |
| Prepare sources (skip overlays) | `azldev comp prep-sources -p <name> --skip-overlays -o <dir> -q` |
| Build, keep env on failure | `azldev comp build -p <name> --preserve-buildenv on-failure -q` |
| List images | `azldev image list` |
| Build an image | `azldev image build` |
| Boot an image in QEMU | `azldev image boot` |
| Dump resolved config | `azldev config dump -q -O json` |
| Advanced commands (like mock shell) | `azldev adv --help` (hidden from normal help) |

## Repository Hygiene Rules

1. **Overlay descriptions**: Every overlay MUST include a `description` field explaining *why* the change is needed.
2. **Naming**: Component names should match the upstream package name. Use `upstream-name` when the upstream name differs (e.g., `upstream-name = "redhat-rpm-config"` for `azurelinux-rpm-config`).
3. **Schema validation**: The authoritative schema is `external/schemas/azldev.schema.json`. Do NOT add `$schema` keys to TOML files — `$` is invalid at the start of a bare TOML key.
4. **Don't edit generated output**: Build artifacts in `base/out/` and `base/build/` are generated (configured by `output-dir`, `log-dir`, `work-dir` in `base/project.toml`) — never edit them directly. Note: `prep-sources -o <dir>` writes to a user-specified directory, separate from these project output dirs.
5. **Mandatory testing**: Any change that affects a component's output (overlays, build config, spec edits, version bumps, new components) MUST be validated by building AND testing the resulting RPMs. A successful build alone is not sufficient — smoke-test in a mock chroot. Pure organizational changes (moving definitions between files, editing descriptions/comments) do not require rebuild. See `AGENTS.md` for the full testing protocol.
