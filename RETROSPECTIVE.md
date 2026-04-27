# Session Retrospective

> **Historical Note (2026-04-27):** This retrospective documents a COSMIC-focused research session. The active desktop decision for ProtagonistOS is KDE, recorded in `docs/decisions/ADR-0003-desktop-environment.md`.

**Project:** Custom Linux Distro Feasibility — Azure Linux Base  
**Date:** April 22, 2026  
**Scope:** Full research session from initial repo exploration through COSMIC desktop implementation planning  

---

## Table of Contents

1. [What We Set Out to Do](#1-what-we-set-out-to-do)
2. [How the Exploration Unfolded](#2-how-the-exploration-unfolded)
3. [Key Technical Discoveries](#3-key-technical-discoveries)
4. [How Thinking Evolved](#4-how-thinking-evolved)
5. [Decisions Made](#5-decisions-made)
6. [What We Produced](#6-what-we-produced)
7. [Open Questions](#7-open-questions)
8. [Recommended Next Steps](#8-recommended-next-steps)
9. [Lessons for Future Sessions](#9-lessons-for-future-sessions)

---

## 1. What We Set Out to Do

The session began with a single broad request:

> *"Research this code base and report back the high level architecture. I am interested in using this project as a base for a Custom Linux Distro. Output a full technical feasibility report at project root."*

The implied goals were:

- Understand how Azure Linux is structured and how it builds
- Determine whether it is a practical base for a custom distribution
- Produce a document that another engineer or stakeholder could use to evaluate the project

As the session continued, the scope deepened twice:

1. When the question of desktop environments was raised, the work became a desktop feasibility analysis layered on top of the server analysis.
2. When COSMIC was named specifically, the work became a concrete implementation planning exercise.

---

## 2. How the Exploration Unfolded

### Phase 1 — Repository Orientation

The first pass was purely structural. The top-level layout was mapped and four major regions of the repo identified:

- `SPECS/` and `SPECS-EXTENDED/` — the package library
- `SPECS-SIGNED/` — Secure Boot and kernel signing wrappers
- `toolkit/` — the entire build system

The toolkit's internal structure was the first surprise: this is not a simple shell-script build system. It is a purpose-built Go-based build orchestration platform with:

- ~15 custom Go tools (`specreader`, `grapher`, `graphpkgfetcher`, `srpmpacker`, `scheduler`, `pkgworker`, `imager`, `roast`, `isomaker`, `imagecustomizer`, and more)
- A Makefile-driven orchestration layer split across multiple `.mk` fragments
- Hermetic chroot build environments derived from the toolchain RPMs
- Declarative JSON/YAML image composition (no scripting required to define what goes in an image)

The documentation in `toolkit/docs/how_it_works/` was notably thorough, including Mermaid flowcharts of the full pipeline.

### Phase 2 — Build System Deep Dive

The three-stage build pipeline was documented in detail:

```
Toolchain (631 RPMs) → Packages (SPEC → SRPM → RPM) → Image (imager + roast)
```

Key design decisions identified:

- **Hermetic builds**: packages are built inside chroot snapshots, not on the live host
- **Reproducibility**: every source file has a SHA hash in a `.signature.json` sidecar
- **Seeded or from-scratch**: the toolchain can be downloaded (fast) or fully bootstrapped from host tools in Docker (supply-chain-independent)
- **Go 1.23 toolchain** for all custom tooling, with no scripting languages in the critical path

### Phase 3 — Package Ecosystem

The scale was verified:

- `SPECS/` — 1,531 packages
- `SPECS-EXTENDED/` — 1,523 packages
- `SPECS-SIGNED/` — 24 signed wrappers
- **Total: ~3,078 unique package specs**

Kernel version: **Linux 6.6.130.1 (LTS)**, with five variants (standard, HWE, 64K ARM, MSHV, UKI).

The SPEC conventions match Fedora origins — many Azure Linux specs trace directly back to the Fedora Project, which means RPM-experienced engineers will find the codebase familiar.

### Phase 4 — Image Configuration System

The image config format (JSON/YAML) turned out to be one of the most important findings for the custom distro case. The entire composition of a distro image is declarative:

- Disk layout, partition table, partition sizes, filesystem types
- Package lists (composable JSON files)
- Kernel selection
- Boot type (EFI/legacy)
- Additional files to inject
- Post-install scripts
- SELinux mode
- Hostname, locale, timezone

A custom derivative can define its entire OS composition in a handful of JSON files without touching any Go code or Makefile internals.

### Phase 5 — Security Analysis

Azure Linux has a notably hardened security baseline:

- All packages compiled with PIE, stack protector strong, fortify source, RELRO, format security
- SELinux enforcing by default
- Secure Boot via signed shim/grub/kernel chain
- FIPS 140-2/3 dedicated image config
- GPG-signed packages with build-time enforcement option
- Kernel lockdown in integrity mode

This was a positive finding for the custom distro case — hardening is inherited for free.

### Phase 6 — Desktop Feasibility Investigation

This phase was triggered by:

> *"What about a full on distro with a desktop environment? As I understand it this project is specifically designed as a server only distro."*

The investigation involved grepping the spec trees for:

- GNOME components (gnome-shell, mutter, gnome-session, gdm, gjs, cogl)
- KDE/Plasma components (kwin, plasmashell, KF6 frameworks, sddm)
- Xfce, MATE, LXDE, Sway, Hyprland
- Display managers
- Mesa hardware drivers
- Audio components

**The central finding was the Mesa driver situation.** Azure Linux's `mesa` (24.0.1) spec revealed:

```
-Dgallium-drivers=swrast,virgl
```

Only software rendering and VM rendering. All hardware Gallium drivers (Intel `iris`/`crocus`, AMD `radeonsi`/`r600`, Nouveau) are compiled out. This makes bare-metal hardware-accelerated desktop rendering impossible without recompiling Mesa.

Combined with the absence of any desktop shell, compositor, or display manager, the verdict was:

> **LOW FEASIBILITY for generic desktop use without ~150–250 new SPECs.**

### Phase 7 — COSMIC DE Pivot

The desktop conversation changed direction when COSMIC was named:

> *"I am thinking Cosmic DE. What would I have to do?"*

This required a different investigation:

- Mapped the COSMIC component set from the `pop-os/cosmic-epoch` upstream repository
- Verified which Azure Linux packages already satisfy COSMIC's build/runtime dependencies
- Identified specific missing packages
- Assessed Mesa GPU enablement as a mandatory separate workstream
- Estimated a realistic packaging scope

The COSMIC finding was significantly more encouraging than the generic desktop finding:

- COSMIC does not require importing GNOME Shell, Mutter, GJS, or the KDE Frameworks stack
- It is Rust-based, and Azure Linux already has Rust 1.90.0
- The full Wayland base (wayland, mesa, libdrm, libglvnd, libinput, libxkbcommon) is already present
- System services (systemd, pam, polkit, dbus, accountsservice, pipewire) are already present
- The missing pieces are a bounded set, not a complete missing desktop framework

**Revised estimate: ~35–60 new SPECs plus several major existing spec modifications**, compared to 150–250 for GNOME.

---

## 3. Key Technical Discoveries

### Discovery 1: The Toolkit Is a First-Class Build Platform

Azure Linux's `toolkit/` is not configuration glue for an existing build system. It is a custom-engineered build platform with its own dependency graph engine, parallel scheduler, chroot worker management, and image composition tooling. The investment in this infrastructure is significant and reflects Microsoft's intent to use this as a production-grade foundation. For a custom distro, this is an asset — you inherit production-quality build infrastructure at no additional engineering cost.

### Discovery 2: Customization Was Designed In, Not Bolted On

Microsoft maintains a separate tutorials repository dedicated to building custom derivatives. The image config system is explicitly designed for composition. The branding packages (`azurelinux-release`, `azurelinux-repos`, `azurelinux-rpm-macros`) are standard RPMs that can be forked and replaced without touching any build tooling.

### Discovery 3: Mesa Is the Critical Desktop Enablement Gate

The `mesa` spec's Gallium driver configuration is the single most important thing to fix before any desktop use case is viable. The fix itself is a known quantity (add the appropriate driver names to the `-Dgallium-drivers` list), but it requires validating hardware behavior, which is a non-trivial testing workload. Everything else in the desktop stack can be added as new packages. Mesa has to be *recompiled*.

### Discovery 4: COSMIC Avoids the GNOME/KDE Dependency Explosion

Where GNOME would require ~40–60 SPECs just for the shell and compositor layer alone, COSMIC's core is `cosmic-comp` + `cosmic-session` + `cosmic-greeter`. The entire toolkit is `libcosmic`. No foreign compositor, no JavaScript runtime, no GTK4 monolith.

### Discovery 5: COSMIC's Component Model Maps Well to Azure Linux's Package Model

COSMIC is organized as discrete, namespaced components (`cosmic-comp`, `cosmic-session`, `cosmic-panel`, etc.). Each translates cleanly to a separate Azure Linux RPM spec. There are no tightly-coupled monolithic components that would force awkward package splits.

### Discovery 6: Build Host Constraint

The entire build system requires Linux. macOS cannot host native builds. This is a concrete operational constraint for anyone working on this project from a Mac and needs to be resolved before any actual build validation can occur.

---

## 4. How Thinking Evolved

### Initial framing: Is Azure Linux a good base?

The initial answer was unambiguously yes for server, cloud, container, and edge use cases. High confidence, backed by documentation quality, customization architecture, and security posture.

### First pivot: Desktop is harder than expected

The initial desktop assessment reached for GNOME and KDE as the obvious candidates. The verdict (too much missing infrastructure) was correct, but GNOME and KDE turned out to be the wrong comparators for someone thinking about a modern desktop product in 2025.

### Second pivot: COSMIC changes the calculus

When COSMIC was named, the right response was to return to first principles: what does COSMIC actually require, and what does Azure Linux already have? That investigation produced a materially different answer than the GNOME/KDE analysis.

The key insight: COSMIC is not a desktop skin — it is a new compositor + session layer + app set built on the same low-level Wayland/DRM infrastructure that Azure Linux already packages for its cloud and VM use cases. The gap is not "port the entire GNOME stack." The gap is "enable desktop GPU drivers, package libseat and a few missing system libs, then package ~30–50 COSMIC components."

### Final framing: Azure Linux + COSMIC is a real distro engineering program

The conversation converged on a position that is neither dismissive nor naive:

- Azure Linux + COSMIC is technically plausible
- It requires treating this as a dedicated multi-quarter desktop program
- The foundations are stronger than they first appeared
- The most important early technical work is Mesa enablement, not COSMIC packaging

---

## 5. Decisions Made

| Decision | Rationale |
|----------|-----------|
| Use Azure Linux 3.0 as the base | Active Microsoft maintenance, purpose-built for derivation, strong security defaults, RPM ecosystem |
| Target COSMIC DE | Avoids GNOME/KDE framework import; Rust-native; Wayland-native; maps to Azure Linux's existing low-level stack |
| x86\_64 first | Reduces initial complexity; widest hardware base |
| Intel + AMD GPU support first | Largest combined desktop hardware base; both covered by open Mesa drivers |
| Pin a COSMIC Epoch release, not git tip | Stability over novelty; reproducibility |
| Mesa must be rebuilt for desktop GPU | Non-negotiable for hardware rendering |
| Flatpak for app breadth | Avoids needing to natively package a full desktop app catalog immediately |
| Separate desktop compose from server compose | Keeps server image quality unchanged; allows a distinct QA matrix |

---

## 6. What We Produced

### CUSTOM_DISTRO_FEASIBILITY_REPORT.md

Location: [CUSTOM_DISTRO_FEASIBILITY_REPORT.md](CUSTOM_DISTRO_FEASIBILITY_REPORT.md)

A full technical feasibility report covering:

- Repository architecture overview
- Three-stage build pipeline documentation
- Complete Go tool inventory
- Package ecosystem statistics
- Image configuration schema and examples
- Security architecture table
- Seven customization levels (from package composition to full toolchain bootstrap)
- Desktop environment assessment (Section 8a) — what exists, what is missing, GNOME/KDE porting estimate
- COSMIC desktop implementation path (Section 8b) — component map, prerequisites analysis, missing packages, Mesa blocker, packaging scope (~35–60 SPECs), phased strategy, integration checklist, release model, trademark notes
- Feasibility assessment table
- Risk register with mitigations
- Five-phase customization strategy
- Conclusion and recommendations

### RETROSPECTIVE.md

Location: [RETROSPECTIVE.md](RETROSPECTIVE.md) (this file)

A summary of the session: what was explored, found, decided, and what comes next.

---

## 7. Open Questions

### Technical

1. **Mesa GPU scope**: Which specific Gallium/Vulkan drivers go into the initial desktop Mesa build? Intel `iris` + AMD `radeonsi` is the obvious starting point. Does `crocus` (older Intel) matter? Does `nouveau` (NVIDIA open driver) go in scope?

2. **NVIDIA desktop**: Azure Linux has container-oriented NVIDIA tooling already. Does this distro target NVIDIA GPU support for desktop rendering — and if so, via the Nouveau open driver in Mesa or via a separate packaging effort for the proprietary driver?

3. **libseat vs. pure logind**: COSMIC can seat via `libseat` → `seatd` or via `libseat` → `systemd-logind`. The logind path avoids packaging `seatd` separately. Which path does the distro prefer?

4. **Flatpak first or native apps first**: Does the initial COSMIC app catalog strategy rely on Flatpak for third-party apps and only native RPMs for COSMIC components? Or is native packaging of common apps (Firefox, etc.) in scope from the start?

5. **ARM64 desktop**: Is `aarch64` desktop support in scope, or is this strictly x86\_64 initially? Azure Linux has full aarch64 support and COSMIC works on aarch64, but the hardware QA matrix for ARM desktop is more niche.

6. **Secure Boot for desktop**: The SPECS-SIGNED packages use Microsoft-controlled keys. For a real desktop distro shipping to users, Secure Boot support is expected. Does this distro establish its own UEFI signing infrastructure, or is Secure Boot out of scope initially?

7. **GStreamer codec coverage**: COSMIC's media player depends on GStreamer with codec plugins. Azure Linux has `gstreamer1` (1.20.0) — `gstreamer1-plugins-base`, `gstreamer1-plugins-good`, and codec coverage need to be verified against what COSMIC actually needs.

### Program and Process

8. **Maintenance cadence**: Does this distro track upstream COSMIC Epoch releases at a regular cadence, or is COSMIC treated as a slow-moving system component updated infrequently?

9. **Update delivery model**: Does this distro ship its own hosted RPM repository? What is the update delivery mechanism for end users?

10. **System76 relationship**: COSMIC has a trademark policy. Reaching out to System76 proactively before naming the desktop in any release materials is worth doing early.

11. **Installer story**: Azure Linux has a Calamares-based installer for ISOs. Does the desktop distro use that, adapt it, or use a custom installer? COSMIC has `cosmic-initial-setup` for first-boot configuration — the interaction between install-time and first-boot setup needs to be designed.

---

## 8. Recommended Next Steps

Ordered by logical dependency:

### Immediate (no code yet)

1. **Provision a Linux build host.** Nothing else can happen without this. An Ubuntu 22.04 or Azure Linux 3.0 VM with 16+ cores, 200 GB disk, and good network access to `packages.microsoft.com` is the practical minimum. Run `sudo make -C toolkit install-prereqs-and-configure` to install build prerequisites.

2. **Validate a first clean build.** Run `make image CONFIG_FILE=toolkit/imageconfigs/core-efi.json` to confirm the build toolchain works end-to-end in your environment before touching anything else.

3. **Make an architectural decision on GPU scope.** Decide the initial GPU support matrix before any Mesa work starts. This decision gates everything downstream.

### Foundation (weeks 1–6)

4. **Fork and re-brand the identity packages.** Fork `azurelinux-release`, `azurelinux-repos`, `azurelinux-rpm-macros`, `azurelinux-sysinfo`. Set your distro's `%{dist}` tag. Establish a clean branding separation from Microsoft.

5. **Rework the Mesa spec for desktop GPU.** Enable at minimum Intel `iris` and AMD `radeonsi` in the Gallium driver list. Validate rendering on at least one Intel and one AMD system before proceeding.

6. **Package the missing low-level desktop prerequisites.**
   - `libseat` + `seatd`
   - `libdisplay-info`
   - `just` (build tool)
   - `mold` (linker, optional but recommended)
   - `xdg-desktop-portal` base
   - `flatpak` (if app delivery strategy requires it)

7. **Create a skeleton desktop image config.** A `cosmic-desktop.json` and matching package list stub establishes the compose target even before COSMIC packages exist.

### COSMIC Bootstrap (weeks 6–12)

8. **Package COSMIC support libraries first.**
   - `libcosmic`
   - `cosmic-protocols`
   - `cosmic-text`
   - `cosmic-theme`
   - `cosmic-time`

9. **Package and boot the COSMIC core session.**
   - `cosmic-comp`
   - `cosmic-session`
   - `cosmic-greeter`
   
   Success criterion: log in to a COSMIC session in a VM.

10. **Package the COSMIC shell components.**
    - `cosmic-panel`
    - `cosmic-launcher`
    - `cosmic-notifications`
    - `cosmic-settings-daemon`
    - `cosmic-settings`
    - `xdg-desktop-portal-cosmic`

### Desktop Usability (weeks 12–20)

11. **Package core apps.**
    - `cosmic-files`, `cosmic-term`, `cosmic-screenshot`, `cosmic-randr`
    - `cosmic-bg`, `cosmic-applets`, `cosmic-icons`

12. **Validate the hardware loop.**
    - Intel laptop: suspend/resume, brightness, external display, touchpad
    - AMD desktop: GPU rendering, display hotplug
    - VM path: continues to work in Hyper-V / QEMU

13. **Test and harden integration.**
    - PipeWire audio session
    - Screenshot/screencast portal
    - File chooser portal
    - XWayland compatibility
    - Font coverage (add Noto fonts for broader Unicode/CJK coverage)
    - Locale defaults

### Optional Follow-Up Work Identified During This Session

These were offered but not started:

- **Package-by-package porting matrix** — a table of every COSMIC component, its upstream source URL, required Azure Linux RPM name, build dependency list, and packaging priority
- **Draft desktop image configuration** — a complete `cosmic-desktop.json` and associated package list stubs ready to fill in as packages are built
- **Fedora/openSUSE import analysis** — how Fedora 41 (which fully packages COSMIC) and openSUSE (X11:COSMIC:Factory) package COSMIC, and what spec adaptations would be needed for Azure Linux's RPM macro conventions

---

## 9. Lessons for Future Sessions

### What worked well

- **Incremental document building**: Starting with a broad feasibility report, then adding targeted sections as scope clarified, produced a report that evolved naturally with the conversation rather than needing to be fully rewritten.

- **Going to primary sources**: Checking actual SPEC files rather than assuming what was packaged produced more accurate findings. The Mesa driver situation in particular would have been easy to miss without reading the actual spec.

- **Respecting the user's scope decision**: When the user indicated they wanted to pursue desktop despite the feasibility concerns, the right response was to shift from advising against to planning how. Feasibility concerns can be stated once and then moved past.

### What could have been better

- **The initial desktop section assumed GNOME/KDE** without first asking what desktop the user had in mind. This produced a section that needed significant revision once COSMIC was named. A brief clarifying question earlier would have saved rework.

- **Package version spot-checks could be more systematic.** The session verified key package versions (rust 1.90.0, mesa 24.0.1, libinput 1.25.0, etc.) individually. A more systematic pass through COSMIC's stated build requirements against Azure Linux's package list would produce a more complete gap analysis.

### Mental models that helped

- **COSMIC = "a desktop that avoids importing another desktop"**: framing COSMIC not as a light GNOME variant but as a clean-room Wayland desktop built on the same substrate Azure Linux already uses for VMs and cloud helped clarify why the feasibility assessment changed.

- **Mesa as the real gate**: everything else in the desktop stack can be added as new packages. Mesa cannot be trivially added — it has to be recompiled with different flags, and the result has to be tested on real hardware. Making this the first major technical decision item focuses the program on the right constraint.

---

*Retrospective generated from full session history as of April 22, 2026.*
