---
applyTo: "scripts/overlay-classifier/**"
---

# Overlay Classification Taxonomy

This document defines the classification labels and sub-categories used by the overlay classifier scripts. It serves as the authoritative reference for both humans reviewing classifications and agents performing LLM refinement.

## Context

Azure Linux imports RPM specs from upstream Fedora and customizes them via overlays. Each overlay represents a deviation from upstream. The goal of classification is to **inventory and justify every deviation**, enabling the team to:

- Track which deviations are temporary (backports) vs permanent (customizations)
- Identify fixes that should be upstreamed to Fedora
- Understand the role each customization plays in the AZL distro
- Minimize unnecessary deviation from upstream

## Top-Level Labels

### Backport-fedora

A patch or config change that already exists in a newer Fedora branch or commit, cherry-picked into AZL's current pinned snapshot. These are **self-resolving** — they will be removed automatically when AZL's upstream snapshot advances past the commit that includes the fix.

**Indicators:**
- TOML comments or commit body contain `src.fedoraproject.org/rpms/*/c/` URLs
- Description or commit message mentions "backport", "cherry-pick", "backported"
- Description says "Temporary: ... Remove when snapshot includes ..."
- Description mentions "fixed upstream in f4x", "fixed in fedora", "landed in rawhide"

### Upstream-fix

A fix for a real bug (build failure, CVE, runtime issue) that upstream Fedora hasn't merged yet. These are **candidates for upstreaming** — the team should track whether the fix has been submitted to Fedora.

**Indicators:**
- CVE reference (e.g., `CVE-2024-12345`)
- Upstream bug tracker or commit URL (github.com, bugzilla)
- `patch-add` or `file-add` overlay adding a `.patch`/`.diff` file authored by an upstream contributor (not AZL/Microsoft)
- Patch filename contains an upstream bug tracker ID (e.g., `IVY-1652`, `bz#NNNN`, `GH-NNN`)
- Patch fixes compatibility with a newer toolchain/runtime (Java 14+, GCC 15, Python 3.13, etc.)
- Commit header starts with `fix(` without AZL-specific keywords

### AZL-customization

An intentional deviation from Fedora specific to Azure Linux's requirements. These are **not expected to be upstreamed** and represent the AZL-specific value-add or necessary adaptation.

## AZL-customization Sub-Categories

### Dependency-pruning

Removes a BuildRequires or Requires because the dependency package isn't available or isn't shipped in AZL.

**Examples:** Removing `yasm`, `libavif-devel`, `ffmpeg` dependencies.

### Feature-disablement

Disables a build feature, subpackage, or optional capability that AZL doesn't need or can't support.

**Examples:** `--without mingw`, disabling Xen in grub2, disabling crash reporter in Firefox, `%global with_X 0`.

### Branding

Changes Fedora-specific names, paths, identities, or vendor strings to Azure Linux equivalents.

**Examples:** Replacing "Fedora" with "AzureLinux" in boot entries, setting `distro = azurelinux`, EFI vendor paths.

### Build-environment

Adjusts for differences in AZL's build toolchain, mock environment, or CI infrastructure compared to Fedora's.

**Examples:** `-std=gnu89` for older C code, compiler triple fixes, `%autosetup` additions, mock/container workarounds, Koji builder adjustments.

### Test-disablement

Skips or disables tests that fail in AZL's build or CI environment. Includes both bulk check-skip (component-check-disablement.toml) and per-overlay test skipping.

**Examples:** `check.skip = true`, skipping inotify tests in containers, removing test-only BuildRequires.

### Security/compliance

Changes related to FIPS, cryptographic policy, or security hardening specific to AZL's compliance requirements.

**Examples:** Removing `fips.so`, FIPS provider changes, crypto policy adjustments, debuginfo suppression for malware scan.

### Release-management

Overlays that manage Release tag values, changelog behavior, or version pinning mechanics required by azldev's rendering pipeline.

**Examples:** `spec-set-tag Release`, handling `%autorelease` conditional logic, `pkgrelease`/`specrelease` macros.

### Missing-dependency-workaround

Adds a dependency or patches around a package not yet imported into AZL. Expected to be **temporary** — should be resolved when the missing package is imported.

**Examples:** "WORKAROUND: Remove virt-firmware-rs BuildRequires — not yet in AZL4", adding missing transitive deps during bootstrap.

### Platform-adaptation

Adjusts for AZL's supported architectures or platform-specific behavior not covered by Fedora's defaults.

**Examples:** ARM64/aarch64 SVE fixes, architecture-conditional patches, ExcludeArch/ExclusiveArch changes.

### Distro-policy-alignment

Aligns with RHEL/enterprise conventions where AZL deliberately follows RHEL rather than Fedora.

**Examples:** Setting `--with-distro=redhat` for RHEL-aligned defaults, `build.defines = { rhel = "11" }`, enterprise-focused configuration.
