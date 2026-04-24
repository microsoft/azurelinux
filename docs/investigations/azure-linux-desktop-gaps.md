---
title: Azure Linux Desktop Gaps
status: active
source_of_truth: github
branch: sandbox
last_reviewed: 2026-04-24
drive_copy: none
source_inputs:
  - AGENTS.md
  - docs/desktop-performance-reality.md
  - docs/current-state/azure-linux-baseline.md
  - docs/current-state/desktop-performance-reality.md
---

# Azure Linux Desktop Gaps

## Purpose

This investigation identifies the concrete gaps between upstream Azure Linux 3.0 and a credible ProtagonistOS desktop build.

This is not a vision document. It exists to turn the Azure Linux desktop problem into engineering tasks.

## Current Verdict

Azure Linux is not desktop-ready for ProtagonistOS by default.

The gap is not one missing package. The gap is a full desktop enablement chain:

1. Hardware graphics support
2. Desktop session prerequisites
3. Desktop environment packaging
4. SELinux policy behavior
5. Image composition
6. Hardware validation
7. Branding and defaults

The first hard blocker is Mesa hardware acceleration. Until that is solved, higher-level desktop work is premature.

## Gap 1: Mesa Hardware Acceleration

### Problem

The current desktop path depends on Mesa being rebuilt with hardware drivers suitable for target workstations.

The immediate required Gallium drivers are:

- `iris` for modern Intel integrated graphics
- `radeonsi` for AMD graphics

If the system falls back to `swrast`, desktop performance is not acceptable.

### Why this matters

Software rendering invalidates most desktop performance conclusions. It makes the system slow for the wrong reason and hides the performance profile of the actual target system.

### Required work

- Inspect `SPECS/mesa/`.
- Identify the current Mesa build options.
- Add required Gallium drivers.
- Rebuild Mesa successfully in the Azure Linux build system.
- Confirm generated RPMs include the expected DRI drivers.
- Validate on real Intel and AMD hardware.

### Acceptance criteria

- `glxinfo` reports a hardware renderer, not `llvmpipe` or `swrast`.
- Intel target hardware uses the expected Intel path.
- AMD target hardware uses the expected AMD path.
- A basic Wayland session can run without software rendering.

## Gap 2: Desktop Prerequisite Packages

### Problem

Azure Linux is server/cloud-first. Several desktop-session dependencies may be absent, incomplete, or not configured for a full graphical workstation.

Known or likely prerequisites include:

- `libseat`
- `libdisplay-info`
- `xdg-desktop-portal`
- Wayland protocol packages
- PipeWire session components
- desktop portal backends
- display manager dependencies
- input stack dependencies

### Required work

- Build a package inventory for the target desktop stack.
- Compare required packages against `SPECS/` and `SPECS-EXTENDED/`.
- Mark each package as present, missing, outdated, or requiring rebuild.
- Create or import missing RPM specs following the existing Azure Linux conventions.

### Acceptance criteria

- A package gap matrix exists.
- Every required desktop prerequisite has an owner status:
  - present
  - missing
  - needs rebuild
  - blocked by dependency
  - rejected
- Missing prerequisites are represented by issues or build tasks.

## Gap 3: Desktop Environment Packaging

### Problem

The repository guidance currently references COSMIC as the intended desktop path, but recent project direction may have shifted toward KDE and Wayland.

This must be resolved before package work goes too far.

### Required decision

Choose one first graphical target for the Azure Linux path:

- COSMIC on Wayland
- KDE Plasma on Wayland
- minimal Wayland compositor target for build validation only

### Why this matters

COSMIC and KDE imply different dependency trees, packaging workload, SELinux policy work, default apps, and validation targets.

### Acceptance criteria

- A decision record exists for the first desktop target.
- The documentation no longer contradicts itself between COSMIC and KDE.
- The package gap matrix follows the chosen desktop target.

## Gap 4: SELinux Desktop Policy

### Problem

Azure Linux's security posture is useful, but a desktop stack needs a policy that understands desktop behavior.

An untuned policy can create:

- excessive AVC denials
- audit log noise
- startup overhead
- confusing false blockers during package bring-up

### Required work

- Boot a permissive development image once a graphical session exists.
- Capture AVC denials during:
  - login
  - app launch
  - file manager use
  - terminal use
  - browser use, once available
  - settings panel use
- Separate expected access from actual policy errors.
- Decide whether ProtagonistOS will ship enforcing SELinux at first graphical release or stage enforcement later.

### Acceptance criteria

- AVC logs are captured for a repeatable session test.
- Known benign denials are documented.
- Required allow rules are tracked.
- Audit volume is measured, not guessed.

## Gap 5: Image Composition

### Problem

Azure Linux image creation is controlled through toolkit image configs. A ProtagonistOS image needs a minimal, reproducible image definition.

### Required work

- Identify the closest existing Azure Linux image config.
- Create a ProtagonistOS minimal image config.
- Add only the packages required to boot, log in, and validate the target graphical path.
- Keep branding and default app decisions out of the first image unless required for boot or identity.

### Acceptance criteria

- A minimal image config exists under `toolkit/imageconfigs/` or an equivalent project path.
- The image build command is documented.
- The image can be rebuilt from a clean Linux build host.
- The image boots in at least one VM or physical target.

## Gap 6: Build Host and Reproducibility

### Problem

The build system requires Linux. macOS is not a supported validation host.

### Required work

- Define the official build host environment.
- Record CPU, RAM, disk, filesystem, distro, and required tools.
- Document the exact build command for the first ISO target.
- Capture build logs and failure modes.

### Acceptance criteria

- A clean build host setup document exists.
- The first image build is reproducible from documented commands.
- Failed builds produce archived logs.

## Gap 7: Hardware Validation

### Problem

The target audience includes refurbished blue-collar/developer machines. VM success is not enough.

### Required work

Define a minimum hardware validation matrix.

At minimum:

- Intel integrated graphics laptop or desktop
- AMD graphics system
- low-RAM system
- older storage device class, if relevant
- Wi-Fi and Bluetooth validation target

### Acceptance criteria

- Hardware test matrix exists.
- Renderer, boot, login, suspend/resume, networking, audio, and input are tested.
- Failures are recorded as engineering issues, not informal notes.

## Gap 8: Project Identity and Branding Packages

### Problem

ProtagonistOS eventually needs identity packages, but this is not the first blocker.

Likely packages to fork or create later include:

- release package
- repository configuration package
- RPM macro package
- system information branding package
- default settings package
- artwork package

### Required work

- Identify Azure Linux identity packages.
- Decide the minimum identity change needed for an internal ProtagonistOS build.
- Defer visual polish until the graphical path works.

### Acceptance criteria

- Internal builds identify themselves clearly enough for debugging.
- Branding work does not block Mesa, package, or image work.

## Immediate Work Queue

### Task 1: Inspect Mesa spec

Path:

`SPECS/mesa/`

Goal:

Find the current build flags and determine the exact patch required to enable `iris` and `radeonsi`.

Output:

- spec notes
- required patch
- expected RPM output

### Task 2: Create desktop package gap matrix

Goal:

Produce a table of required packages for the selected desktop target.

Columns:

- package
- purpose
- required for minimal boot?
- present in Azure Linux?
- location
- status
- notes

### Task 3: Resolve desktop target contradiction

Goal:

Decide whether the Azure Linux path is targeting COSMIC, KDE, or a minimal Wayland validation target first.

Output:

`docs/decisions/ADR-0003-desktop-environment.md`

### Task 4: Define first image target

Goal:

Choose the first meaningful artifact:

- CLI ISO
- minimal Wayland ISO
- full graphical ISO

Output:

`docs/current-state/installer-and-iso-path.md`

## Risk Register

| Risk | Severity | Notes |
|---|---:|---|
| Mesa hardware acceleration cannot be enabled cleanly | High | Blocks credible desktop work |
| Desktop target remains ambiguous | High | Causes wasted packaging effort |
| Build host is not standardized | Medium | Causes non-reproducible failures |
| SELinux policy work is underestimated | Medium | May create noisy or fragile desktop builds |
| Image composition path is poorly understood | High | Blocks ISO creation |
| Work drifts into branding before bootable system exists | Medium | Consumes time without reducing core risk |

## Current Recommendation

Do not start with a polished desktop.

Start with the smallest image that proves the graphics and build pipeline:

1. Azure Linux base
2. rebuilt Mesa with hardware drivers
3. minimal Wayland-capable graphical session or selected desktop core
4. enough instrumentation to prove renderer, login, and frame path

Once that works, build upward.

## Definition of Done for This Investigation

This investigation is complete when every major gap has either:

- a linked decision record
- a package task
- a build task
- a validation task
- or a documented rejection

Until then, this document remains active.
