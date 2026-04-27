---
title: ProtagonistOS Technical Status
status: active
source_of_truth: github
branch: dev
last_reviewed: 2026-04-27
drive_copy: none
source_inputs:
  - AGENTS.md
  - README.md
  - docs/current-state/azure-linux-baseline.md
  - docs/current-state/desktop-performance-reality.md
  - docs/investigations/azure-linux-desktop-gaps.md
  - docs/current-state/environment-setup.md
  - docs/decisions/ADR-0001-project-workflow-source-of-truth.md
  - docs/decisions/ADR-0002-branching-upstream-sync-and-access-policy.md
---

# ProtagonistOS Technical Status

## Current Phase

Planning / pre-build.

No ProtagonistOS desktop package layer is complete yet. The repository is currently a downstream Azure Linux 3.0 fork with project documentation and feasibility analysis layered on top.

## Source of Truth

The Git repository is authoritative.

Google Drive is archive/reference. GitHub Issues should become the active task board. Google Calendar should become the time-planning surface.

The active ProtagonistOS integration branch is `dev`. Stable project state lives on `main`. The `3.0` branch is reserved as a pristine Azure Linux upstream mirror. The previous `sandbox` branch is legacy and should not receive new project work.

## Current Technical Direction

The documented target remains:

```text
Azure Linux 3.0
  -> Mesa rebuild with Intel iris and AMD radeonsi
  -> desktop prerequisites
  -> COSMIC core
  -> COSMIC shell and applications
  -> ProtagonistOS branding and defaults
```

## Highest-Priority Engineering Gate

Mesa hardware acceleration is the first hard blocker.

Required first work:

- inspect `SPECS/mesa/`
- identify the current `-Dgallium-drivers` configuration
- enable `iris` and `radeonsi`
- rebuild Mesa on a Linux host
- confirm expected DRI artifacts are present
- validate hardware rendering on Intel and AMD systems

Until this is done, desktop performance conclusions are not meaningful.

## Current Constraints

- macOS is useful for editing and coordination, but not Azure Linux build validation
- serious package and image builds require a Linux host
- physical hardware validation is required for a credible desktop distro
- upstream Azure Linux toolkit Go source should not be modified casually
- desktop packages should be additions or measured rebuilds, not random replacement of upstream package structure

## Known Documentation State

Active current-state docs:

- `docs/current-state/azure-linux-baseline.md`
- `docs/current-state/desktop-performance-reality.md`
- `docs/current-state/environment-setup.md`

Active investigation docs:

- `docs/investigations/azure-linux-desktop-gaps.md`
- `docs/investigations/personal-ai-workflow-surface.md`

Active workflow decision:

- `docs/decisions/ADR-0001-project-workflow-source-of-truth.md`
- `docs/decisions/ADR-0002-branching-upstream-sync-and-access-policy.md`

Legacy detailed reports still present:

- `CUSTOM_DISTRO_FEASIBILITY_REPORT.md`
- `RETROSPECTIVE.md`
- `docs/desktop-performance-reality.md`
- `docs/desktop-security-posture.md`
- `docs/package-management.md`

## Immediate Next Issues to Create

Create GitHub Issues for:

1. Inspect `SPECS/mesa/` and document current Gallium driver build flags.
2. Patch Mesa spec to enable `iris` and `radeonsi`.
3. Define the first Linux build host.
4. Create a package gap matrix for desktop prerequisites.
5. Decide whether COSMIC remains the first desktop target or whether KDE/minimal Wayland should be reconsidered.
6. Define the first hardware validation matrix.
7. Create the first minimal image target and acceptance criteria.

## Open Decisions

- first official Linux build host
- first hardware validation targets
- first graphical target: COSMIC, KDE, or minimal Wayland compositor
- first image artifact: command-line ISO, graphical ISO, or staged package build
- SELinux enforcement strategy for early graphical builds
