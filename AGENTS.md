# Project Guidelines

## Purpose

This repository is a **downstream fork of [microsoft/azurelinux](https://github.com/microsoft/azurelinux) (branch `3.0`)**.

The goal is to build a custom Linux desktop distribution on top of Azure Linux 3.0, targeting the **COSMIC desktop environment** (`pop-os/cosmic-epoch`). This is an active engineering project, not a mirror. Changes made here diverge intentionally from upstream.

See [README.md](README.md) for the project overview, [docs/README.md](docs/README.md) for the documentation index, [docs/reports/protagonistos-technical-status.md](docs/reports/protagonistos-technical-status.md) for the current project status, [CUSTOM_DISTRO_FEASIBILITY_REPORT.md](CUSTOM_DISTRO_FEASIBILITY_REPORT.md) for the original technical analysis, and [RETROSPECTIVE.md](RETROSPECTIVE.md) for session history and open questions.

## Operating Workflow

The **Git repository is the source of truth** for ProtagonistOS technical state.

Use the project surfaces this way:

| Surface | Role |
|---|---|
| Git repository | Authoritative technical documentation, source code, specs, image configs, ADRs, reports |
| GitHub Issues | Active workflow: tasks, blockers, investigations, acceptance criteria, follow-up work |
| Google Calendar | Time allocation: focus blocks, build windows, review sessions, hardware testing |
| Google Drive | Archive/reference only: readable copies, historical notes, planning drafts, exported summaries |
| Codex sessions | Execution, reconciliation, drafting, implementation, summarization |
| Codex automations | Future workflow automation after the manual repo/issues/calendar model is stable |

If Google Drive and the repository disagree, the repository wins. Drive-originated technical material must be promoted into Markdown in this repository before it is treated as current truth.

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
| `docs/README.md` | Documentation index and repo/Drive synchronization policy |
| `docs/current-state/` | Current technical reality documents |
| `docs/decisions/` | Architecture Decision Records and durable workflow decisions |
| `docs/investigations/` | Research notes, gap analyses, exploratory reports |
| `docs/reports/` | Synthesized project status and planning reports |
| `CUSTOM_DISTRO_FEASIBILITY_REPORT.md` | Full technical feasibility report |
| `RETROSPECTIVE.md` | Project history, decisions, open questions, next steps |

## Current Documentation Map

Current state:
- [Azure Linux baseline](docs/current-state/azure-linux-baseline.md)
- [Desktop performance reality](docs/current-state/desktop-performance-reality.md)
- [Environment setup](docs/current-state/environment-setup.md)

Decisions:
- [ADR-0001: Project workflow and source of truth](docs/decisions/ADR-0001-project-workflow-source-of-truth.md)

Investigations:
- [Azure Linux desktop gaps](docs/investigations/azure-linux-desktop-gaps.md)
- [Personal human-AI workflow surface](docs/investigations/personal-ai-workflow-surface.md)

Reports:
- [ProtagonistOS technical status](docs/reports/protagonistos-technical-status.md)

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

Immediate workflow tasks should become GitHub Issues:
1. Inspect `SPECS/mesa/` and document current Gallium driver build flags
2. Patch Mesa spec to enable `iris` and `radeonsi`
3. Define the first Linux build host
4. Create a package gap matrix for desktop prerequisites
5. Decide whether COSMIC remains the first desktop target or whether KDE/minimal Wayland should be reconsidered
6. Define the first hardware validation matrix
7. Create the first minimal image target and acceptance criteria

## Key Constraints

- **Do not modify upstream toolkit Go source** unless specifically asked — the build system is upstream-maintained
- **Upstream Azure Linux content is intentionally preserved** — treat `SPECS/` and `SPECS-EXTENDED/` as the upstream package library; new desktop specs are additions, not replacements
- **Mesa must be recompiled** for desktop GPU support — it cannot be added as a separate package
- **Linux build host required** — all build validation must happen on a Linux machine
