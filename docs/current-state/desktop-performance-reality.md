---
title: Desktop Performance Reality
status: active
source_of_truth: github
branch: dev
last_reviewed: 2026-04-27
drive_copy: none
original_path: docs/desktop-performance-reality.md
---

# Desktop Performance Reality

## Purpose

This document tracks the current performance reality for using Azure Linux as the base for a ProtagonistOS desktop system.

The original report is preserved at:

`docs/desktop-performance-reality.md`

This normalized version is the current-state working document. It keeps the findings actionable and organized around the engineering consequences for ProtagonistOS.

## Current Verdict

Azure Linux's hardened baseline is not the primary desktop performance blocker by itself.

The major blocker is hardware graphics enablement. If Azure Linux is limited to software rendering paths such as `swrast`, desktop performance will be unacceptable regardless of whether the hardened compiler/security defaults are individually tolerable.

Once hardware Mesa drivers are enabled and validated, the remaining hardening overhead appears manageable for a developer workstation, but it must be measured on target hardware rather than assumed.

## Key Findings

### 1. Hardware Mesa drivers are the gating dependency

The original report states that Azure Linux Mesa currently only ships `swrast` and `virgl`, and that enabling `iris` and `radeonsi` is the first meaningful performance improvement for a desktop workload.

Implication for ProtagonistOS:

- Intel integrated graphics support must be validated through `iris`.
- AMD graphics support must be validated through `radeonsi`.
- Software rendering is not an acceptable fallback for the target user experience.
- GPU driver enablement should be treated as a release blocker for any graphical ISO.

### 2. Security hardening overhead is real but probably secondary

The report evaluates overhead from:

- VDSO ASLR
- Full RELRO
- PIE and ASLR
- Stack canaries
- `_FORTIFY_SOURCE=2`
- SELinux runtime checks
- Audit logging
- Mesa shader compilation effects

The practical conclusion is that most individual hardening costs are small in steady-state desktop use, but they can compound during startup, app launch, shader compilation, and untuned SELinux policy development.

Implication for ProtagonistOS:

- Do not weaken the hardening baseline prematurely.
- First fix hardware acceleration.
- Then measure startup latency, app launch latency, and compositor frame timing.
- Only consider mitigation after measurement shows a user-visible problem.

### 3. SELinux policy quality matters

The report distinguishes between tuned policy, untuned policy, permissive development mode, AVC cache behavior, and audit daemon I/O.

Implication for ProtagonistOS:

- Running a desktop stack under an untuned SELinux policy can create audit noise and avoidable I/O overhead.
- Policy work is not optional if Azure Linux remains the base.
- Development images may tolerate permissive mode, but production images need a coherent policy strategy.
- Audit logging needs to be watched during desktop bring-up.

### 4. Compositor and login startup should be measured, not guessed

Full RELRO and Mesa `dlopen()` behavior can affect cold-start and login-to-desktop timing.

Implication for ProtagonistOS:

- Login-to-usable-desktop latency should become a tracked benchmark.
- First boot and warm boot should be measured separately.
- Greeter/compositor startup order may matter.
- Library page cache effects need to be accounted for when testing.

### 5. Shader cache strategy may be needed later

The original report suggests pre-compiling or pre-warming compositor shader paths to avoid first-use jank.

Implication for ProtagonistOS:

- This is not the first engineering task.
- It becomes relevant only after hardware acceleration works.
- A seeded Mesa shader cache may be useful for polish, but it should not distract from base graphics enablement.

## Engineering Priority Order

1. Confirm Azure Linux package/build path for Mesa changes.
2. Enable and build Mesa hardware drivers needed for realistic desktop use.
3. Validate Intel and AMD graphics on physical hardware.
4. Establish baseline benchmarks against Fedora or another working desktop distribution.
5. Measure compositor frame timing, app launch latency, login latency, memory use, and SELinux audit behavior.
6. Tune SELinux policy and audit behavior.
7. Investigate shader-cache prewarming only after the core graphics path is acceptable.

## Minimum Benchmark Set

Use this as the first practical benchmark checklist:

```bash
# Confirm renderer
glxinfo | grep -E "OpenGL renderer|OpenGL version"

# Basic GPU/compositor sanity
weston-info || true
vulkaninfo --summary || true

# Boot timing
systemd-analyze
systemd-analyze blame

# App launch timing
hyperfine 'konsole --version'
hyperfine 'dolphin --version'

# CPU and cache behavior during a focused workload
perf stat -e instructions,cycles,cache-misses,branch-misses <command>

# SELinux denials
ausearch -m avc --start recent

# Audit volume
sudo tail -f /var/log/audit/audit.log
```

Adjust the application commands once the actual desktop package set is finalized.

## Release Blockers Identified

A graphical ProtagonistOS ISO should not be considered technically credible until these are resolved:

- Hardware-accelerated Mesa driver path works.
- Login reaches a usable desktop reliably.
- The compositor is not running through software rendering.
- SELinux policy behavior is understood, even if not fully final.
- App launch latency is measured on target-class refurbished hardware.
- At least one Intel iGPU and one AMD GPU path have been tested.

## Open Questions

- What is the exact Azure Linux packaging change required to enable `iris` and `radeonsi`?
- Does Azure Linux's current kernel configuration support the target graphics stack cleanly?
- Which display manager and greeter path will ProtagonistOS use?
- Which KDE session path should define benchmark baselines first (minimal session bring-up or full Plasma desktop)?
- What physical hardware should define the minimum supported target tier?
- How much SELinux policy work is required before the desktop can run without excessive AVC noise?

## Relationship to Original Report

The original document remains valuable because it contains detailed mechanism-level analysis and estimates.

This normalized version should be used for project planning and current-state tracking. If the original report changes materially, update this file so the current-state conclusions remain coherent.
