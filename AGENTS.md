# Project Guidelines

## Purpose

This repository is a **downstream fork of [microsoft/azurelinux](https://github.com/microsoft/azurelinux) (branch `3.0`)**.

The goal is to build a custom Linux desktop distribution on top of Azure Linux 3.0, targeting the **COSMIC desktop environment** (`pop-os/cosmic-epoch`). This is an active engineering project, not a mirror. Changes made here diverge intentionally from upstream.

See [README.md](README.md) for the project overview, [CUSTOM_DISTRO_FEASIBILITY_REPORT.md](CUSTOM_DISTRO_FEASIBILITY_REPORT.md) for the full technical analysis, and [RETROSPECTIVE.md](RETROSPECTIVE.md) for session history and open questions.

## Architecture

```
Azure Linux 3.0 (RPM-based, server/cloud-first base)
  └── Mesa rebuild  — enable Intel iris + AMD radeonsi Gallium drivers
       └── Desktop prerequisites  — libseat, libdisplay-info, xdg-desktop-portal
            └── COSMIC core  — cosmic-comp, cosmic-session, cosmic-greeter
                 └── COSMIC shell + apps  — cosmic-panel, cosmic-settings, cosmic-files, ...
```

## Repository Layout

| Path | Contents |
|---|---|
| `SPECS/` | ~1,531 primary RPM specs (core + base packages) |
| `SPECS-EXTENDED/` | ~1,523 extended RPM specs (community-facing) |
| `SPECS-SIGNED/` | 24 signed package wrappers (kernel, grub, EFI shim) |
| `toolkit/` | The entire build system — Go tools, Makefiles, image configs, docs |
| `toolkit/imageconfigs/` | Declarative JSON image definitions (the compose layer) |
| `toolkit/docs/` | Build system documentation including pipeline flowcharts |
| `CUSTOM_DISTRO_FEASIBILITY_REPORT.md` | Full technical feasibility report |
| `RETROSPECTIVE.md` | Project history, decisions, open questions, next steps |

## Build System

Azure Linux uses a **three-stage hermetic build pipeline**:

1. **Toolchain** (631 RPMs) — downloaded or bootstrapped from Docker; defines the chroot environment
2. **Packages** (SPEC → SRPM → RPM) — built inside isolated chroot snapshots
3. **Image** (`imager` + `roast`) — assembled from RPMs via declarative JSON config

All build tooling is written in Go (1.23). Orchestration is via `make`. Build targets require a **Linux host** — macOS is not supported.

Quick-start build command:
```bash
make image CONFIG_FILE=toolkit/imageconfigs/core-efi.json
```

Full documentation: [`toolkit/README.md`](toolkit/README.md) and [`toolkit/docs/`](toolkit/docs/).

## Package Conventions

- All packages follow **Fedora RPM spec conventions** — many specs trace directly to Fedora
- Source files have a `.signatures.json` sidecar with SHA hashes for reproducibility
- Every new package for the desktop layer belongs in `SPECS/` and follows existing spec patterns
- The identity packages to fork for branding: `azurelinux-release`, `azurelinux-repos`, `azurelinux-rpm-macros`, `azurelinux-sysinfo`

## Current Development Phase

**Planning / Pre-build** (April 2026). No desktop packages exist yet.

Priority order for the first engineering work:
1. Mesa spec (`SPECS/mesa/`) — add `iris` and `radeonsi` to `-Dgallium-drivers`
2. Missing prerequisites — `libseat`, `libdisplay-info`, `xdg-desktop-portal` base
3. COSMIC support libraries — `libcosmic`, `cosmic-protocols`
4. COSMIC session core — `cosmic-comp`, `cosmic-session`, `cosmic-greeter`

## Key Constraints

- **Do not modify upstream toolkit Go source** unless specifically asked — the build system is upstream-maintained
- **Upstream Azure Linux content is intentionally preserved** — treat `SPECS/` and `SPECS-EXTENDED/` as the upstream package library; new desktop specs are additions, not replacements
- **Mesa must be recompiled** for desktop GPU support — it cannot be added as a separate package
- **Linux build host required** — all build validation must happen on a Linux machine
