# Technical Feasibility Report: Custom Linux Distro Based on Azure Linux

> **Historical Note (2026-04-27):** This report captures an earlier COSMIC-first exploration phase. The canonical desktop direction is now KDE, as defined in `docs/decisions/ADR-0003-desktop-environment.md`. Keep this document for historical technical context.

**Date:** April 22, 2026  
**Repository:** microsoft/azurelinux (branch: 3.0)  
**Purpose:** Evaluate the technical feasibility of using Azure Linux as a base for a custom Linux distribution

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Repository Architecture Overview](#2-repository-architecture-overview)
3. [Build System Deep Dive](#3-build-system-deep-dive)
4. [Package Ecosystem](#4-package-ecosystem)
5. [Image Configuration & Output Formats](#5-image-configuration--output-formats)
6. [Security Architecture](#6-security-architecture)
7. [Customization Surfaces](#7-customization-surfaces)
8. [Build Prerequisites & Host Requirements](#8-build-prerequisites--host-requirements)
   - [8a. Desktop Environment Assessment](#8a-desktop-environment-assessment)
  - [8b. COSMIC Desktop Implementation Path](#8b-cosmic-desktop-implementation-path)
9. [Feasibility Assessment](#9-feasibility-assessment)
10. [Risks & Mitigations](#10-risks--mitigations)
11. [Recommended Customization Strategy](#11-recommended-customization-strategy)
12. [Conclusion](#12-conclusion)

---

## 1. Executive Summary

Azure Linux 3.0 is a production-grade, open-source, RPM-based Linux distribution developed by Microsoft for its cloud and edge infrastructure. The codebase is well-documented, modularly designed, and explicitly architected to support custom image derivation. Microsoft themselves provide a separate [tutorials repository](https://github.com/microsoft/azurelinux-tutorials) dedicated to building custom derivatives.

**Verdict: HIGH FEASIBILITY — for server, cloud, container, and edge appliance use cases.** The project is technically sound as a custom distro base for those workloads. The build system is purpose-built for layering, customization is achieved through declarative JSON configuration files and spec overrides, and the full build pipeline is reproducible from source.

**Verdict: LOW FEASIBILITY — for a full desktop distribution.** Azure Linux is explicitly a server/cloud-first distro. Critical desktop components (GNOME Shell, KDE Plasma, display managers, hardware GPU drivers) are absent from the spec tree and would require hundreds of new SPECs to port. See [Section 8a: Desktop Environment Assessment](#8a-desktop-environment-assessment) for a full breakdown.

**Desktop refinement:** among modern desktop environments, **COSMIC is the most plausible path** on top of Azure Linux because it avoids importing the full GNOME Shell or KDE Plasma stack. It is still a large multi-quarter engineering effort that requires desktop GPU enablement, session integration, and packaging a substantial COSMIC-specific component set. See [Section 8b: COSMIC Desktop Implementation Path](#8b-cosmic-desktop-implementation-path).

---

## 2. Repository Architecture Overview

### Top-Level Structure

```
azurelinux/
├── SPECS/              # ~1,531 primary package specs (core + base packages)
├── SPECS-EXTENDED/     # ~1,523 extended package specs (community-facing)
├── SPECS-SIGNED/       # 24 signed package wrappers (kernel, grub, EFI shim)
├── toolkit/            # The entire build system
│   ├── Makefile        # Top-level orchestrator
│   ├── docs/           # Build system documentation
│   ├── imageconfigs/   # Declarative image definitions (JSON/YAML)
│   ├── resources/      # Toolchain manifests, repo configs, assets
│   ├── scripts/        # Makefile fragments (.mk files)
│   └── tools/          # Go-based build tools (source)
├── LICENSES-AND-NOTICES/
├── cgmanifest.json     # Component governance manifest
└── README.md
```

### Design Philosophy

Azure Linux is designed around the principle that a **small common core** can address universal cloud/edge needs, with teams layering additional packages on top. This maps directly onto the needs of a custom distribution. Key design decisions:

- **RPM-based packaging** — all packages are defined by `.spec` files and built into RPMs
- **Reproducible builds** — every artifact can be traced back to a specific SRPM and toolchain version
- **Hermetic chroot builds** — packages are built inside isolated chroot environments derived from the toolchain RPMs, preventing host contamination
- **Declarative image composition** — images are defined entirely by JSON/YAML config files; no custom scripting is required to define what goes into a system image

---

## 3. Build System Deep Dive

### Three-Stage Pipeline

The build pipeline is strictly ordered into three stages, each of which can be seeded from pre-built artifacts or rebuilt from scratch:

```
Stage 1: TOOLCHAIN
  ↓  (631 RPMs defining the hermetic build environment)
Stage 2: PACKAGES
  ↓  (Build RPMs from SPEC files inside chroot)
Stage 3: IMAGE
     (Compose final image artifacts from RPMs)
```

#### Stage 1 — Toolchain

The toolchain is a controlled set of ~631 RPMs (per architecture) that define the build environment. It serves as the foundation for all subsequent package builds. The toolchain can be:

- **Downloaded** from `packages.microsoft.com` (default, fastest)
- **Extracted** from a local `toolchain.tar.gz` archive (`TOOLCHAIN_ARCHIVE=...`)
- **Fully rebuilt from scratch** (`REBUILD_TOOLCHAIN=y`), bootstrapped inside a Docker container from host tools, then rebuilt clean using the intermediate outputs

The toolchain produces a `chroot` worker archive — a snapshot of the full build environment that is used for all subsequent builds, ensuring reproducibility.

#### Stage 2 — Package Generation

The package build stage operates as follows:

1. **`specreader`** — scans all `*.spec` files, extracts dependency metadata to `specs.json`
2. **`grapher`** — builds a directed dependency graph (`graph.dot`) from the spec metadata
3. **`graphpkgfetcher`** — resolves unmet nodes against locally cached RPMs or remote repos, producing a `cached_graph.dot`
4. **`srpmpacker`** — packages SPEC files + verified sources (by SHA hash) into SRPMs
5. **`scheduler`** — determines optimal parallel build order respecting the dependency graph
6. **`pkgworker`** — builds individual packages inside dedicated chroot environments

Each package source is verified against a `*.signature.json` hash file before being accepted, preventing supply chain substitution.

#### Stage 3 — Image Generation

Image generation is driven entirely by a JSON/YAML configuration file:

1. **`imageconfigvalidator`** — validates the config file schema
2. **`imager`** — creates a filesystem (raw disk image or directory tree) and installs packages via `tdnf` inside a chroot
3. **`roast`** — converts the raw disk image into the final output format

### Go Build Tools

All custom tooling is written in Go 1.23 and lives in `toolkit/tools/`. The full tool suite includes:

| Tool | Purpose |
|------|---------|
| `specreader` | Parse spec files into dependency JSON |
| `grapher` | Build dependency graph from spec JSON |
| `graphpkgfetcher` | Resolve graph nodes against local/remote RPM caches |
| `srpmpacker` | Pack SPEC + sources into SRPMs |
| `scheduler` | Order builds for parallel execution |
| `pkgworker` | Build a single package in a chroot |
| `imager` | Install packages into a filesystem |
| `roast` | Convert raw image to final format (vhd, vhdx, ext4, etc.) |
| `isomaker` | Assemble bootable ISO with initrd installer |
| `imageconfigvalidator` | Validate image config JSON/YAML |
| `imagepkgfetcher` | Resolve packages needed for an image |
| `imagecustomizer` | Post-build image customization tool |
| `depsearch` | Query dependency graphs |
| `liveinstaller` | ISO-embedded terminal installer |
| `licensecheck` | Validate RPM license compliance |
| `versionsprocessor` | Manage version consistency |

---

## 4. Package Ecosystem

### Spec Repositories

| Repository | Count | Description |
|------------|-------|-------------|
| `SPECS/` | ~1,531 | Core packages maintained by Microsoft |
| `SPECS-EXTENDED/` | ~1,523 | Extended/community packages (many borrowed from Fedora/Photon) |
| `SPECS-SIGNED/` | 24 | Signed wrappers for kernel, grub, EFI, and RDMA modules |

Total: **~3,078 unique package specs** available for inclusion.

### Kernel

The primary kernel is **Linux 6.6.x LTS** (currently `6.6.130.1`). Additional kernel variants are available:

- `kernel` — standard kernel
- `kernel-hwe` — Hardware Enablement kernel (newer drivers for recent hardware)
- `kernel-64k` — 64K page-size kernel (ARM64 specific)
- `kernel-mshv` — Microsoft Hypervisor kernel
- `kernel-uki` — Unified Kernel Image (UKI) for Confidential VMs

### Package Manager

**`tdnf`** (Tiny Dandified YUM) is the primary package manager — a lightweight, fast, DNF-compatible package manager written in C. Standard `dnf` is also available. Both support signed RPM repositories.

### Upstream Acknowledgements

Azure Linux's SPEC files draw from multiple upstream distributions:
- **Fedora Project** — DNF, Qt, and many `SPECS-EXTENDED` packages
- **Photon OS** — Additional SPEC files
- **Linux from Scratch** — Core userspace patterns

This means the spec authoring conventions will be familiar to any RPM-experienced developer.

---

## 5. Image Configuration & Output Formats

### Supported Output Formats

Images are composed by `roast` from a raw disk image into the following formats:

| Format | Description |
|--------|-------------|
| `.vhd` | Hyper-V Gen 1 virtual disk |
| `.vhdx` | Hyper-V Gen 2 virtual disk |
| `.ext4` | Raw ext4 partition image |
| `.tar.gz` | Rootfs tarball (no partition table) |
| Container image | OCI-compatible container rootfs |
| ISO | Bootable installer with Calamares GUI or terminal installer |
| OVA | VMware-compatible appliance format |

### Architecture Support

| Architecture | Status |
|---|---|
| `x86_64` (AMD64) | Fully supported |
| `aarch64` (ARM64) | Fully supported |
| `arm64` (64K page) | Kernel variant available |

### Pre-Built Image Configs

The toolkit ships `~30+` ready-to-use image configurations including:

- `core-efi.json` — Standard EFI VM image (VHDX, Gen2 Hyper-V)
- `core-legacy.json` — Legacy BIOS VM image
- `core-fips.json` — FIPS 140-2/140-3 compliant image
- `core-container.json` — Minimal OCI container image
- `distroless-*.json` — Distroless variants (base, debug, minimal)
- `marketplace-gen2-*.json` — Azure Marketplace images
- `minimal-os.json` — Minimal 500MB VM image
- `full.json` — Developer image with full toolset
- `baremetal-*.yaml` — Bare-metal install configurations
- `core-efi-selinux.json` — SELinux enforcing image

### Image Config Schema (JSON)

Image configs are fully declarative. Key sections:

```json
{
  "Disks": [{
    "PartitionTableType": "gpt",
    "MaxSize": 4096,
    "Artifacts": [{ "Name": "my-distro", "Type": "vhdx" }],
    "Partitions": [...]
  }],
  "SystemConfigs": [{
    "Name": "My Custom Distro",
    "BootType": "efi",
    "PackageLists": ["packagelists/my-packages.json"],
    "KernelOptions": { "default": "kernel" },
    "Hostname": "my-distro",
    "AdditionalFiles": { "myconfig.conf": "/etc/myconfig.conf" },
    "PostInstallScripts": [{ "Path": "scripts/myscript.sh" }],
    "KernelCommandLine": { "SELinux": "enforcing" }
  }]
}
```

---

## 6. Security Architecture

Azure Linux ships with a hardened security baseline enabled by default:

### Compiler Hardening (All Packages)

| Feature | Status |
|---------|--------|
| Position Independent Executable (`-fPIE -pie`) | Default |
| Stack Protector Strong (`-fstack-protector-strong`) | Default |
| Format Security (`-Wformat-security`) | Default |
| Fortify Source (`_FORTIFY_SOURCE`) | Default |
| Full RELRO (`--enable-bind-now`) | Default |
| RELRO (Read-Only Relocations) | Default |

### Kernel Hardening (Default)

- ASLR (stack, libs, exec, brk, VDSO)
- `/dev/mem` and `/dev/kmem` protection
- Strict module RO/NX
- Kernel `.rodata` write protection
- Stack Protector in kernel
- Kernel Address Display Restriction (`kptr_restrict`)
- Symlink and hardlink restrictions

### System Security

- **SELinux** — Mandatory Access Control, enforcing by default (configurable)
- **Secure Boot** — Supported via signed shim + signed GRUB + signed kernel (SPECS-SIGNED)
- **FIPS 140-2/140-3** — Dedicated `core-fips.json` image configuration
- **Confidential VMs** — Dedicated CVM image configs with DRTM support
- **GPG Signed Packages** — All published packages signed; `VALIDATE_IMAGE_GPG=y` enforces validation at build time
- **SHA-verified Sources** — Each SPEC source file has a `*.signature.json` hash requirement

---

## 7. Customization Surfaces

Azure Linux exposes multiple well-defined customization surfaces, ordered from least to most invasive:

### Level 1 — Package Composition (No Code Changes)

Create custom `packagelists/*.json` files referencing existing package names, then reference them from a new image config JSON. This is sufficient for most use cases: adding, removing, or substituting packages without any rebuild.

```json
// packagelists/my-custom-packages.json
{
  "packages": [
    "core-packages-base-image",
    "my-app",
    "custom-daemon"
  ]
}
```

### Level 2 — Additional Files & Post-Install Scripts

Image configs support injecting arbitrary files and running post-install scripts inside the assembled image:

```json
"AdditionalFiles": {
  "myfiles/my.conf": "/etc/my.conf"
},
"PostInstallScripts": [
  { "Path": "scripts/configure-my-distro.sh" }
]
```

### Level 3 — Custom SPEC Files (New Packages)

Drop a new `SPECS/mypackage/mypackage.spec` with a corresponding `mypackage.signatures.json`, and the build system will automatically include it in dependency resolution. The build system docs include a full walkthrough (see `toolkit/docs/building/add-package.md`).

### Level 4 — Forking Existing SPECs

Copy and modify any existing SPEC file in `SPECS/` to change compiler flags, patch sets, build options, or version. Existing patches live alongside the SPEC in the package subdirectory.

### Level 5 — Custom Kernel Configuration

The `SPECS/kernel/` directory contains the full kernel SPEC. Custom kernel configs can be applied by modifying or adding Kconfig fragments. ARM64 `64K` and `HWE` kernel variants demonstrate this pattern.

### Level 6 — Image Customizer (Post-Build)

The `toolkit/tools/imagecustomizer` tool supports post-build modifications to assembled images without requiring a full rebuild — useful for CI/CD workflows that stamp builds with final configuration.

### Level 7 — Full Toolchain Bootstrap

Set `REBUILD_TOOLCHAIN=y` to build the entire toolchain from scratch using only the host system's tools in a Docker container. This enables complete supply-chain independence from Microsoft's package servers.

---

## 8a. Desktop Environment Assessment

Azure Linux is explicitly a **server and cloud-first distribution**. This section documents the state of graphical/desktop components in the spec tree for teams evaluating a desktop use case.

### What IS Present (Lower-Layer Building Blocks)

| Layer | Package(s) | Notes |
|-------|-----------|-------|
| Display protocol | `wayland`, `wayland-protocols`, `xorg-x11-server-Xwayland` | Wayland client libs present |
| X.Org server | `xorg-x11-server` (SPECS-EXTENDED, v1.20.10) | EOL upstream; Fedora 40+ has fully dropped it |
| GPU / OpenGL | `mesa` (v24.0.1), `vulkan-loader`, `vulkan-headers` | Mesa present but severely restricted (see below) |
| UI toolkit | `gtk2`, `gtk3`, `qt5`/`qt6` base, `cairo`, `pango`, `gdk-pixbuf2` | Toolkit libs present, no desktop shell |
| Audio | `pulseaudio` (v16.1), `pipewire` | Both in SPECS-EXTENDED |
| Input | `xorg-x11-drv-libinput` | |
| Input methods | `ibus` + multiple backends | CJK input support present |
| Fonts | `dejavu-fonts`, `fontawesome-fonts`, `google-roboto-slab-fonts`, `freefont` | Limited set |
| Icons/themes | `adwaita-icon-theme` (v3.36.1), `gsettings-desktop-schemas` | GNOME schema stubs only |

### Critical Missing Components (Desktop Deal-Breakers)

| Component | What's Missing | Impact |
|-----------|---------------|--------|
| **Desktop shell** | No GNOME Shell (`mutter`, `gnome-shell`, `gnome-session`, `gnome-control-center`, `gjs`, `cogl`, `clutter`), no KDE Plasma (`kwin`, `plasmashell`, KF6 frameworks), no Xfce, no MATE, no LXDE, no Sway, no Hyprland | No usable desktop environment at all |
| **Display manager** | No `gdm`, `lightdm`, or `sddm` | No graphical login |
| **Hardware GPU drivers** | Mesa is compiled with **only `swrast` (CPU software rendering) and `virgl` (VM passthrough)** — Intel `iris`/`crocus`, AMD `radeonsi`/`r600`, and Nouveau are conditionally disabled in the spec | No hardware acceleration on bare metal |
| **Proprietary GPU drivers** | Only `libnvidia-container` and `nvidia-container-toolkit` (for containerized GPU workloads) — no display/Wayland/X11 NVIDIA drivers | No NVIDIA desktop rendering |
| **Compositor** | No `mutter`, `kwin`, `weston`, `sway`, or any Wayland compositor | |
| **App ecosystem** | No file manager, settings app, terminal (beyond server tools), browser, or office suite | |

### Mesa GPU Driver Detail

The `mesa` (v24.0.1) SPEC reveals that hardware Gallium drivers are conditionally compiled out for the standard build:

```
# Actual build line used:
-Dgallium-drivers=swrast,virgl

# Full driver list (available but disabled by default):
# iris, crocus (Intel), radeonsi, r600, r300 (AMD),
# nouveau (NVIDIA), freedreno, etnaviv, panfrost (ARM), etc.
```

This means even if you added a shell and display manager, bare-metal hardware-accelerated rendering would require recompiling Mesa with the appropriate driver flags enabled.

### Estimated Desktop Porting Effort

To build a functional GNOME desktop on top of Azure Linux from scratch:

| Task | Estimated New SPECs |
|------|-------------------|
| GNOME core shell stack (`mutter`, `gnome-shell`, `gnome-session`, `gjs`, `cogl`, etc.) | ~40–60 |
| GNOME Settings, Control Center, and system utilities | ~30–50 |
| GNOME applications (Files, Terminal, Text Editor, etc.) | ~20–40 |
| Display manager (`gdm`) and login infrastructure | ~5–10 |
| Mesa recompile with hardware driver flags | ~1 (modify existing) |
| Missing font packages (Noto full set, etc.) | ~10–15 |
| Missing GNOME library dependencies | ~50–80 |
| **Total estimate** | **~150–250 new/modified SPECs** |

A minimal KDE Plasma desktop would require a similar or larger effort due to the KDE Frameworks (KF6) dependency tree.

### Recommendation for Desktop Use Cases

If the goal is a **desktop distribution**, Azure Linux is the wrong starting point. Better-suited alternatives:

| Project | Why It's Better for Desktop |
|---------|----------------------------|
| **Fedora** | Most Azure Linux SPECs trace back to Fedora; full GNOME stack maintained; RPM-based (same tooling familiarity) |
| **RHEL / AlmaLinux / Rocky Linux** | Enterprise-grade RPM base with full desktop option |
| **openSUSE Leap / Tumbleweed** | Excellent RPM base, full KDE and GNOME support, `obs` build system |
| **Debian / Ubuntu** | Largest desktop package ecosystem; `debootstrap` enables easy custom derivatives |
| **NixOS** | Highly reproducible declarative builds (philosophically similar to Azure Linux) with full desktop support |
| **Arch Linux** | Minimal RPM-free base; easy desktop layering via AUR; rolling release |

**Azure Linux remains an excellent base for server, container, cloud appliance, edge, and embedded use cases.** The feasibility verdict for those workloads is unchanged.

## 8b. COSMIC Desktop Implementation Path

If the goal is to build a **real desktop distribution** on top of Azure Linux despite its server-first orientation, **COSMIC is the strongest candidate** among modern desktop environments. Unlike GNOME Shell or KDE Plasma, COSMIC does not require importing an entire legacy desktop stack. It is a newer, Wayland-native, Rust-heavy environment with a more self-contained component model.

That changes the problem from "port all of GNOME/KDE" to "build a first-class desktop product on top of Azure Linux's existing low-level graphics, system, and RPM infrastructure." The latter is still difficult, but materially more tractable.

### Why COSMIC Is a Better Fit Than GNOME or KDE

COSMIC reduces the dependency blast radius in several ways:

- It avoids a hard dependency on **GNOME Shell + Mutter + gnome-session + gjs + the broader GNOME control stack**.
- It avoids a hard dependency on **KWin + Plasma Workspace + the KDE Frameworks stack**.
- It is **Wayland-native**, which fits a modern desktop strategy and reduces the need to invest deeply in legacy X11 desktop architecture beyond compatibility support through XWayland.
- It is primarily **Rust-based**, and Azure Linux already ships a current Rust toolchain (`rust` 1.90.0), which is a major prerequisite already satisfied.

The practical implication is that Azure Linux does not need to become a GNOME distribution or a KDE distribution. It needs to become a **desktop-capable Wayland distribution with a COSMIC packaging and integration layer**.

### COSMIC Component Set

Upstream COSMIC is not a single monolithic package. It is a collection of related components that must be packaged and integrated together. The critical components are:

#### Core desktop/session

- `cosmic-comp` — compositor
- `cosmic-session` — session startup and orchestration
- `cosmic-greeter` — greeter/login experience
- `cosmic-panel` — desktop panel
- `cosmic-launcher` — application launcher
- `cosmic-settings` — control/settings UI
- `cosmic-settings-daemon` — background settings/session services
- `cosmic-notifications` — notification service/UI
- `cosmic-osd` — on-screen display service
- `xdg-desktop-portal-cosmic` — Wayland desktop portal integration

#### Core user-facing utilities

- `cosmic-files`
- `cosmic-term`
- `cosmic-edit`
- `cosmic-store`
- `cosmic-screenshot`
- `cosmic-randr`
- `cosmic-bg`
- `cosmic-applets`
- `cosmic-icons`
- `cosmic-initial-setup`
- `cosmic-player`
- `pop-launcher`
- `cosmic-workspaces-epoch`

#### Core libraries/toolkit

- `libcosmic`
- `cosmic-protocols`
- `cosmic-text`
- `cosmic-theme`
- `cosmic-time`

In practice, a usable Azure Linux COSMIC edition would need to package the **core desktop/session layer first**, then the **core apps/utilities**, and only then expand into the full app surface.

### Azure Linux Prerequisites Already Present

Azure Linux already has a stronger COSMIC foundation than it has for GNOME or KDE. The following verified packages exist in the current spec trees:

#### Graphics and display base

- `wayland`
- `wayland-protocols`
- `mesa` 24.0.1
- `libdrm` 2.4.120
- `libglvnd` 1.7.0
- `vulkan-loader` 1.3.275.0
- `xorg-x11-server-Xwayland`

#### Input/session/system services

- `libinput` 1.25.0
- `libxkbcommon` 1.6.0
- `pam` 1.5.3
- `polkit` 123
- `systemd` 255
- `accountsservice`
- `libei`

#### Desktop runtime/build dependencies

- `pipewire`
- `dbus`
- `fontconfig` 2.14.2
- `freetype` 2.13.2
- `expat` 2.6.4
- `gstreamer1` 1.20.0
- `clang` 18.1.8
- `lld` 18.1.8
- `rust` 1.90.0

That means Azure Linux already covers much of the **kernel, graphics, input, session, audio, and compiler substrate** needed for COSMIC packaging.

### Key Gaps That Must Be Closed

The main blockers are no longer a complete missing desktop framework. They are a set of concrete platform and packaging gaps.

#### 1. Seat/session management

Verified missing:

- `libseat`
- `seatd`

These are important because a modern Wayland compositor typically needs a clean seat/session handoff strategy. Depending on how COSMIC is configured, `systemd-logind` may handle some of the session model, but packaging `libseat` and `seatd` cleanly is still the safer desktop baseline.

#### 2. Display topology support

Verified missing:

- `libdisplay-info`

This matters for monitor enumeration, display metadata handling, and robust multi-monitor behavior.

#### 3. Portal integration

Not present in the Azure Linux spec tree during this analysis:

- `xdg-desktop-portal`
- `xdg-desktop-portal-gtk`
- `xdg-desktop-portal-cosmic`

These are required for modern sandboxed app behavior, file pickers, screenshots, screencasting, and desktop integration under Wayland.

#### 4. Build helpers and developer tooling

Verified missing:

- `just`
- `mold`

COSMIC upstream documents these as part of the expected build environment. They are not strictly impossible to work around, but packaging them removes friction and makes builds reproducible in the Azure Linux ecosystem.

#### 5. Application ecosystem integration

Verified missing:

- `flatpak`

Flatpak is not strictly required to boot COSMIC, but it is important for a modern desktop distro strategy, especially if the base distro initially has a thinner native desktop app catalog than Fedora, Debian, or openSUSE.

### Mesa and GPU Enablement Are Mandatory Workstreams

The existing Azure Linux Mesa packaging is the single largest technical blocker to turning COSMIC into a real desktop product.

The current `mesa` build path effectively resolves to:

```text
-Dgallium-drivers=swrast,virgl
```

This is appropriate for:

- software rendering
- virtualized rendering paths
- cloud and VM use cases

It is not appropriate for a general-purpose desktop distribution.

For a COSMIC desktop product, Mesa needs to be rebuilt with hardware drivers enabled for the initial support matrix. At minimum, that likely means:

- Intel: `iris`, likely `crocus`
- AMD: `radeonsi`, optionally `r600`
- optionally ARM drivers if ARM desktop targets matter

NVIDIA is a separate policy and engineering decision. Azure Linux currently contains **container-oriented NVIDIA packages** (`libnvidia-container`, `nvidia-container-toolkit`) but not a desktop GPU driver stack. The safest initial product scope is:

- Tier 1: Intel + AMD graphics
- Tier 2: VM/virt paths
- Deferred: NVIDIA desktop support

Without Mesa rework, COSMIC may build and even start in some environments, but the distro would not be credible as a bare-metal desktop OS.

### Estimated Packaging Scope for a COSMIC Port

Compared to the GNOME estimate of ~150–250 new or modified SPECs, COSMIC has a meaningfully smaller but still substantial packaging surface.

#### Rough-order estimate

| Workstream | Estimated New/Modified SPECs |
|-----------|------------------------------|
| Missing low-level dependencies (`libseat`, `seatd`, `libdisplay-info`, portals, helper tools) | ~8–15 |
| COSMIC libraries/toolkit (`libcosmic`, `cosmic-*` shared libs/protocol crates) | ~5–10 |
| Core desktop/session components (`cosmic-comp`, `cosmic-session`, `cosmic-greeter`, `cosmic-panel`, `cosmic-settings`, `cosmic-settings-daemon`, portal integration) | ~10–15 |
| Core user-facing apps (`cosmic-files`, `cosmic-term`, `cosmic-edit`, `cosmic-store`, `cosmic-screenshot`, etc.) | ~10–20 |
| Base distro desktop polish (fonts, themes, icons, defaults, desktop package groups) | ~5–10 |
| Mesa desktop enablement | ~1 major existing SPEC rework |
| **Total estimate** | **~35–60 new SPECs plus several major existing spec modifications** |

This is a realistic order-of-magnitude estimate for getting to a **first credible COSMIC-based Azure Linux desktop**, not a fully mature consumer desktop distribution.

### Packaging Strategy

The recommended packaging strategy is to avoid importing COSMIC as a single opaque blob. Instead, package it as first-class Azure Linux RPMs in layered phases.

#### Phase A — Base enablement

Add the missing platform prerequisites:

- `libseat`
- `seatd`
- `libdisplay-info`
- `xdg-desktop-portal`
- `xdg-desktop-portal-cosmic`
- `xdg-desktop-portal-gtk` or another fallback portal backend as needed
- `just`
- `mold`
- `flatpak`

At the same time, fork or patch Mesa for desktop GPU enablement.

#### Phase B — Bootable COSMIC session

Package the minimum viable desktop shell:

- `libcosmic`
- COSMIC support libraries
- `cosmic-comp`
- `cosmic-session`
- `cosmic-greeter`
- `cosmic-panel`
- `cosmic-launcher`
- `cosmic-settings-daemon`
- `xdg-desktop-portal-cosmic`

Success criterion:

- a user can log into a COSMIC session from a graphical greeter in a VM and on at least one bare-metal test system

#### Phase C — Daily-driver desktop

Add the applications and desktop utilities that make the environment usable:

- `cosmic-files`
- `cosmic-term`
- `cosmic-settings`
- `cosmic-notifications`
- `cosmic-osd`
- `cosmic-screenshot`
- `cosmic-randr`
- `cosmic-bg`
- `cosmic-applets`
- `cosmic-icons`

Success criterion:

- common daily tasks are usable without dropping to TTY or manually editing config files

#### Phase D — Product polish

Add:

- installer/session defaults
- branding and theme integration
- Flatpak-first app delivery if desired
- QA matrix for Intel and AMD laptops/desktops
- optional additional COSMIC apps (`cosmic-store`, `cosmic-edit`, `cosmic-player`)

### Image and Compose Changes Required

The current Azure Linux image definitions are server-oriented. A COSMIC edition would require at minimum:

- a new desktop image config under `toolkit/imageconfigs/`
- one or more desktop package lists under `toolkit/imageconfigs/packagelists/`
- display manager and session defaults
- desktop-specific `AdditionalFiles` and `PostInstallScripts`
- likely a dedicated installer or ISO path for graphical installation

A plausible image layering model would be:

1. **Base desktop platform list**
  Includes graphics stack, audio stack, input stack, session services, fonts, portals.
2. **COSMIC core list**
  Includes compositor, session, greeter, panel, launcher, settings daemon.
3. **COSMIC apps list**
  Includes files, terminal, settings UI, screenshot tool, applets, store.

That separation matches Azure Linux's existing layering philosophy and will make it easier to test and ship server and desktop editions in parallel.

### Integration Work Beyond RPM Packaging

Packaging COSMIC is necessary, but not sufficient. To make Azure Linux into a reliable COSMIC distro, the following integrations must be engineered and tested:

- PAM stack for local graphical login
- `systemd --user` unit behavior
- `polkit` agent flow
- account creation / first-boot provisioning
- monitor hotplug and multi-display behavior
- audio session bring-up with PipeWire
- power management, suspend/resume, lid handling
- input device defaults (touchpad, keyboard layout, hotkeys)
- screenshot / screencast portals
- file chooser integration under Wayland
- XWayland compatibility for non-native apps
- desktop MIME defaults and file associations
- font fallback, locale coverage, and emoji/CJK coverage

This integration workload is why the overall project remains a **distro engineering program**, not just a package port.

### Build and Release Model Recommendation

For a COSMIC-based Azure Linux derivative, the recommended release model is:

- **x86_64 first**
- **Intel and AMD GPU support first**
- **VM support first, laptops second, broader hardware matrix third**
- **pinned COSMIC Epoch releases**, not random tip-of-tree snapshots
- **separate desktop compose** from server/cloud compose
- **Flatpak for breadth of apps**, native RPMs for core desktop components

This keeps the scope bounded and aligns with how upstream COSMIC is actually consumed by other distributions.

### Trademark and Naming Considerations

System76's published COSMIC trademark policy allows Linux distributions to refer to the COSMIC desktop environment so long as usage is not misleading and does not imply endorsement. However:

- avoid presenting your distro as an official System76 or Pop!_OS product
- keep your distro branding distinct from COSMIC's branding
- use COSMIC to describe the desktop environment, not the distro identity

This is a manageable legal/branding issue, but it should be handled explicitly during product naming and release planning.

### Final COSMIC-Specific Assessment

For Azure Linux specifically:

- **GNOME/KDE path:** low feasibility without a very large package import effort
- **COSMIC path:** moderate feasibility if the project is resourced as a dedicated desktop program

In practical terms, a COSMIC-based Azure Linux distro is feasible if you are willing to commit to:

- ~35–60 new SPECs
- several major existing spec changes, especially Mesa
- a dedicated desktop QA matrix
- sustained integration work around login, audio, graphics, portals, and power management

The strongest reading is:

**Azure Linux is not ready-made for desktop use, but it is capable of becoming a COSMIC-based desktop distro if you deliberately turn it into one.**

---

## 8. Build Prerequisites & Host Requirements

### Supported Build Hosts

| OS | Status |
|----|--------|
| Azure Linux (any version) | Fully supported |
| Ubuntu 22.04 | Validated |
| macOS | **Not supported** (Linux-only due to chroot/loopback requirements) |
| Windows (native) | **Not supported** |
| WSL2 on Windows | Possible with caveats (loopback device support required) |

> **Important for this repo:** This workspace is on macOS. Building requires a Linux VM or a remote Linux host (e.g., an Azure VM, a local VM, or a CI runner).

### Required Tools (Ubuntu 22.04)

- **Go 1.23.1+** (`golang-1.23-go` package)
- **Docker** — for toolchain bootstrap and chroot environments
- **make**, **rpm**, **tdnf**, **createrepo_c**
- Standard Linux development tools (`gcc`, `binutils`, `gawk`, etc.)

Install via:
```bash
sudo make -C toolkit install-prereqs-and-configure
```

### Resource Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| Disk | 50 GB | 200 GB+ |
| RAM | 8 GB | 32 GB |
| CPU | 4 cores | 16+ cores (parallel package builds) |
| Network | Required for source/RPM download | High bandwidth for initial seed |

---

## 9. Feasibility Assessment

### Strengths

| Factor | Assessment |
|--------|-----------|
| **Customization Architecture** | ✅ Excellent — explicitly designed for custom derivatives |
| **Documentation Quality** | ✅ Excellent — full how-it-works docs, quickstart, tutorials |
| **Package Coverage** | ✅ Excellent — ~3,000+ specs across base, extended, and signed |
| **Security Baseline** | ✅ Excellent — hardened by default, FIPS/Secure Boot/SELinux ready |
| **Output Format Flexibility** | ✅ Excellent — VHD, VHDX, container, ISO, raw, OVA, tar.gz |
| **Architecture Support** | ✅ Good — x86_64 and aarch64 |
| **Desktop Use Case** | ❌ Not viable without ~150–250 new SPECs — see [Section 8a](#8a-desktop-environment-assessment) |
| **COSMIC Desktop Path** | ⚠️ Plausible with a dedicated engineering effort — roughly ~35–60 new SPECs, Mesa desktop enablement, and session integration work |
| **Reproducibility** | ✅ Excellent — hermetic chroot builds, source hash verification |
| **Community & Upstream** | ✅ Good — active Microsoft-maintained, public community calls |
| **License** | ✅ MIT (toolkit) + per-package licenses (packages) |

### Challenges

| Factor | Assessment |
|--------|-----------|
| **Build Host Constraint** | ⚠️ Linux-only — macOS/Windows require a Linux VM or remote build |
| **Initial Build Time** | ⚠️ Full from-scratch builds take many hours; pre-built seed recommended |
| **Branding Divergence** | ⚠️ `azurelinux-release`, `azurelinux-repos`, `azurelinux-rpm-macros` contain Microsoft branding; must be forked for a true custom distro identity |
| **Package Signing** | ⚠️ `SPECS-SIGNED/` packages use Microsoft-controlled signing keys; custom distro needs its own signing infrastructure |
| **Toolchain Dependency** | ⚠️ Default workflow downloads toolchain from `packages.microsoft.com`; full independence requires `REBUILD_TOOLCHAIN=y` |
| **Go Tooling Version** | ℹ️ Go 1.23 required; must be managed on build host |
| **Rich Dependency Syntax** | ℹ️ Some RPM rich dependencies (`or`, `with`) are not fully supported — workarounds exist |

---

## 10. Risks & Mitigations

### Risk 1: Microsoft Branding in Base Packages

**Packages affected:** `azurelinux-release`, `azurelinux-repos`, `azurelinux-rpm-macros`, `azurelinux-sysinfo`

**Mitigation:** Fork these packages in your own `SPECS/` tree and replace with your distro's branding. This is the standard approach (analogous to how Fedora-derived distros fork `fedora-release`). The `%{dist}` RPM macro (`.azl3` tag) is defined in `azurelinux-rpm-macros` and should be replaced with your own distro tag.

### Risk 2: Supply Chain Dependency on packages.microsoft.com

**Mitigation:** Use `DISABLE_UPSTREAM_REPOS=y` combined with a local RPM mirror, or perform a full `REBUILD_TOOLCHAIN=y` bootstrap to achieve complete independence. The build system is designed to support both modes.

### Risk 3: Secure Boot / Signed Kernel

**Packages affected:** All entries in `SPECS-SIGNED/`

**Mitigation:** For Secure Boot support, you will need your own UEFI signing certificate. The `SPECS-SIGNED/` packages are wrappers that sign pre-built binaries — replace the signing keys with your own. Alternatively, disable Secure Boot for non-production/internal use.

### Risk 4: Linux Build Host Requirement

**Mitigation:** Provision a Linux build environment. Recommended options:
- An Azure VM (Ubuntu 22.04 or Azure Linux 3.0)
- A local Linux VM (Hyper-V, VMware, VirtualBox)
- A GitHub Actions or Azure DevOps runner with Ubuntu 22.04

### Risk 5: Full Rebuild Time

**Mitigation:** Seed the build from pre-built Microsoft packages by leaving `REBUILD_TOOLCHAIN=n` and `REBUILD_PACKAGES=n` for the initial pass. Only locally modified packages will be rebuilt. The `DELTA_BUILD=y` option further limits rebuilds to changed packages and their dependents.

---

## 11. Recommended Customization Strategy

For a new custom distro based on Azure Linux, the following phased approach is recommended:

### Phase 1 — Fork & Brand (Week 1)

1. Fork this repository into your own GitHub organization
2. Fork and rename the following SPECS: `azurelinux-release`, `azurelinux-repos`, `azurelinux-rpm-macros`, `azurelinux-sysinfo`
3. Update the `%{dist}` tag in your `rpm-macros` package to your distro identifier (e.g., `.mydistro1`)
4. Create a custom `imageconfigs/my-distro.json` based on `core-efi.json`
5. Create `imageconfigs/packagelists/my-distro-base.json` with your package selection

### Phase 2 — Core Build Validation (Week 2)

1. Provision a Linux build host (Ubuntu 22.04 minimum, 16 cores, 200GB disk recommended)
2. Install prerequisites: `sudo make -C toolkit install-prereqs-and-configure`
3. Seed toolchain from Microsoft's servers (fastest first build): `make toolchain`
4. Build only your modified packages: `make build-packages PACKAGE_REBUILD_LIST="my-release my-repos my-rpm-macros"`
5. Build your custom image: `make image CONFIG_FILE=imageconfigs/my-distro.json`

### Phase 3 — Custom Packages (Ongoing)

1. Add new packages by creating `SPECS/<pkgname>/<pkgname>.spec` + `<pkgname>.signatures.json`
2. Modify existing package SPECs as needed (patches, compile flags, version bumps)
3. Add post-install configuration scripts under `imageconfigs/scripts/`
4. Use `toolkit/tools/imagecustomizer` for post-build image manipulation in CI/CD

### Phase 4 — Security & Signing Infrastructure (Pre-Production)

1. Generate your own GPG signing key pair for package signing
2. Replace Secure Boot signing keys if Secure Boot is required
3. Enable `VALIDATE_IMAGE_GPG=y` in production image builds
4. Consider `DISABLE_UPSTREAM_REPOS=y` and a private RPM mirror for supply chain control

### Phase 5 — Reproducible Release Builds

1. Use `REPO_SNAPSHOT_TIME=<posix_time>` to pin remote repo snapshots
2. Capture build summaries for reproducibility (`make build-summary`)
3. Archive toolchain with `TOOLCHAIN_ARCHIVE` for fully offline rebuilds

---

## 12. Conclusion

Azure Linux 3.0 is an excellent foundation for a custom Linux distribution. Its architecture was designed from the ground up with derivation in mind — the toolkit explicitly supports custom SPEC trees, declarative image composition, and flexible build modes ranging from fully seeded (fast) to fully self-hosted (independent).

The main operational requirement is a **Linux build host**, which rules out native macOS or Windows builds but is easily addressed with a VM or CI environment. The branding and signing infrastructure require one-time setup work to establish a distro-independent identity, but the mechanisms for doing so are well-understood and supported by the build system.

The project is backed by active Microsoft engineering, maintains public community calls, and is already in production as the foundation of Microsoft's cloud and edge products — providing high confidence in long-term maintenance and security patch velocity.

**Recommendation: Proceed. Begin with Phase 1 (fork & brand) and Phase 2 (core build validation) to establish a working build pipeline before committing to deeper customization work.**

For a desktop-oriented fork, the recommendation is narrower: **proceed only with a COSMIC-first strategy, not a GNOME-first or KDE-first strategy.** If desktop is a hard requirement, the most defensible path is to keep Azure Linux as the base OS, add the missing Wayland/session/portal substrate, rework Mesa for real desktop hardware, and package COSMIC as a dedicated edition with its own compose, QA matrix, and release cadence.

---

*Report generated from repository analysis of `microsoft/azurelinux` branch `3.0` as of April 22, 2026.*
