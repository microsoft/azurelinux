---
title: Azure Linux Baseline
status: active
source_of_truth: github
branch: dev
last_reviewed: 2026-04-27
drive_copy: none
source_inputs:
  - AGENTS.md
---

# Azure Linux Baseline

## Purpose

This document captures the current technical baseline for using Azure Linux 3.0 as the foundation for ProtagonistOS.

It is derived from the repository project guidelines in `AGENTS.md` and should be treated as the concise current-state reference for the base system.

## Current Verdict

Azure Linux 3.0 is a plausible but difficult base for ProtagonistOS.

Its strengths are RPM packaging, a disciplined build pipeline, reproducible source/signature handling, and a hardened enterprise-style baseline.

Its weakness is that it is server/cloud-first. A desktop distribution must add or rebuild a substantial graphical stack before it can be treated as a credible workstation base.

## Repository Role

This repository is a downstream fork of `microsoft/azurelinux`, branch `3.0`.

The fork is not a passive mirror. It is intended to diverge deliberately to support a custom desktop distribution.

## Target Architecture

The intended build-up path is:

```text
Azure Linux 3.0
  -> Mesa rebuild with Intel iris and AMD radeonsi Gallium drivers
  -> Desktop prerequisites
  -> COSMIC core session components
  -> COSMIC shell and applications
  -> ProtagonistOS branding, defaults, and developer-focused system policy
```

## Current Development Phase

The project is in planning / pre-build phase as of April 2026.

No desktop package layer is considered complete yet.

The current engineering priority is not branding, installer polish, or default applications. The first priority is making the graphical stack technically viable.

## Key Baseline Facts

### Build system

Azure Linux uses a three-stage build process:

1. Toolchain bootstrap or download
2. Package build from RPM specs into SRPM/RPM artifacts
3. Image assembly through declarative image configuration

The build tooling is Go-based and orchestrated through `make`.

A Linux build host is required. macOS is not a supported build host for validation.

### Package structure

The important repository areas are:

- `SPECS/` for primary RPM specs
- `SPECS-EXTENDED/` for extended package specs
- `SPECS-SIGNED/` for signed boot/kernel/EFI wrappers
- `toolkit/` for the build system
- `toolkit/imageconfigs/` for image composition definitions
- `toolkit/docs/` for build-system documentation

### Desktop enablement path

The first desktop-enablement sequence is:

1. Rebuild Mesa with required hardware drivers.
2. Add missing desktop prerequisites.
3. Add COSMIC support libraries.
4. Add COSMIC session core packages.
5. Add shell and application packages.
6. Only then work on final image composition and polish.

## First Engineering Dependency: Mesa

Mesa must be rebuilt for hardware desktop support.

The immediate requirement is to update the Mesa spec so the build includes the Gallium drivers required for realistic workstation graphics support.

Minimum required targets:

- `iris` for modern Intel integrated graphics
- `radeonsi` for AMD graphics

Without this, the desktop stack risks falling back to software rendering or incomplete virtualized rendering paths, which is not acceptable for ProtagonistOS.

## Constraints

### Do not casually modify upstream build tooling

The toolkit Go source should be treated as upstream-maintained infrastructure. Changes to the toolkit should be avoided unless there is a specific, measured reason.

### Preserve upstream package library assumptions

The Azure Linux package library should be treated as the base inventory. Desktop work should primarily add or extend packages, not randomly replace upstream structure.

### Validate on Linux

All serious build validation must happen on a Linux host.

A Mac or VM can be useful for reading, editing, or early inspection, but it is not the proving ground for the distribution.

## Practical Consequences for ProtagonistOS

- The project should remain build-system-first until the ISO path is understood.
- Desktop package work should begin with Mesa, not COSMIC shell packages.
- Hardware acceleration is a credibility gate.
- The fork must maintain a clear distinction between upstream Azure Linux and downstream ProtagonistOS changes.
- Documentation must record where the fork intentionally diverges.

## Open Questions

- What exact Mesa spec changes are required for `iris` and `radeonsi`?
- Are all required Mesa dependencies already present in Azure Linux 3.0?
- Which desktop prerequisites are missing from `SPECS/` and `SPECS-EXTENDED/`?
- Is COSMIC still the intended desktop target for the Azure Linux path, or should the documentation be revised for KDE if the project direction has changed?
- What is the first minimal image target: command-line ISO, graphical ISO, or staged build artifact?
- Which physical machine should be the first validation target?

## Current Recommendation

Treat Azure Linux as an engineering research base until a minimal hardware-accelerated graphical image can be produced.

Do not assume that the distribution vision is validated just because the repository builds. For ProtagonistOS, the first meaningful proof is a minimal ISO that boots on target-class hardware and reaches a hardware-accelerated desktop or well-defined graphical session path.
