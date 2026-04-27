---
title: Environment Setup
status: active
source_of_truth: github
branch: dev
last_reviewed: 2026-04-27
drive_copy: none
source_inputs:
  - Google Drive: parallels-config-checklist.md
  - Google Drive: system-check.md
---

# Environment Setup

## Purpose

This document reconciles the environment notes that previously existed only in Google Drive.

It captures the current development-host context for ProtagonistOS and separates historical Fedora/Parallels notes from the actual Azure Linux build requirements.

## Current Verdict

The MacBook Pro plus Parallels setup is useful for editing, investigation, documentation, and lightweight Linux workstation experiments.

It is not the official validation environment for Azure Linux or ProtagonistOS builds.

Serious package and image validation requires a Linux build host.

## Historical Fedora/Parallels Setup

The April 12, 2026 Drive notes describe a Fedora Linux 42 Workstation VM on a MacBook Pro using Parallels.

Recommended VM allocation from that note:

| Resource | Value |
|---|---|
| CPU | 8 vCPU |
| Memory | 18 GB RAM |
| Disk | 300 GB dynamic disk |

Intent:

- keep macOS light
- run most Linux development work inside Fedora
- keep source trees, build directories, package caches, and toolchains inside the guest filesystem
- avoid heavy builds from Parallels shared folders such as `/media/psf`
- use shared folders only for light file exchange
- use snapshots sparingly and delete stale snapshots after confirming stability

## April 12, 2026 Fedora VM Health Check

The Drive system check recorded this state:

| Item | Value |
|---|---|
| Guest OS | Fedora Linux 42 Workstation |
| Architecture | aarch64 |
| Kernel | 6.19.11-100.fc42.aarch64 |
| Virtualization | Parallels |
| Root disk usage | 11 GB used of 63 GB |
| Memory | 3.8 GiB assigned |
| Swap | 3.8 GiB zram, about 1.5 GiB used |
| Network | working |
| Failed systemd units | none |
| Reboot required | no |

Healthy signals:

- `systemctl --failed` returned no failed units.
- `prltoolsd.service` was active.
- Parallels shared folders were mounted.
- `dnf needs-restarting -r` reported no reboot was needed.
- `upower` was installed and active.

Issues observed:

- memory pressure was visible with only 3.8 GiB assigned
- Parallels Tools logged `Module prl_tg not found`
- GUI and Flatpak graphics errors referenced `virgl (Apple M4 Pro (Compat))`
- unsupported `GL_EXT_shader_texture_lod` was observed
- KDE apps logged filesystem watch warnings, likely related to Parallels shared folders

## Engineering Consequence

The Fedora/Parallels setup is useful context, but it should be treated as an environment experiment, not the canonical build path.

For ProtagonistOS, the practical rule is:

- use macOS for editing, Codex sessions, Drive/Calendar/GitHub coordination, and repo maintenance
- use a real Linux host for Azure Linux package and image builds
- use physical Intel and AMD hardware for desktop validation
- avoid using VM graphics behavior as evidence for bare-metal desktop viability

## Open Questions

- What Linux host will be the first official build machine?
- Will the initial build host be bare metal, a Linux VM, or a remote machine?
- What filesystem and disk capacity should be required for repeatable image builds?
- Which physical Intel and AMD machines define the first hardware validation targets?
