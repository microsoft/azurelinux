---
applyTo: "scripts/overlay-classifier/**"
---

# Overlay Classification Taxonomy

This document defines the classification labels used by the overlay classifier scripts. It serves as the authoritative reference for both humans reviewing classifications and agents performing LLM refinement.

## Context

Azure Linux imports RPM specs from upstream Fedora and customizes them via overlays. Each overlay represents a deviation from upstream. The goal of classification is to **inventory and justify every deviation**, enabling the team to:

- Track which deviations are temporary (backports) vs permanent (customizations)
- Identify fixes that should be upstreamed to Fedora
- Understand the role each customization plays in the AZL distro
- Minimize unnecessary deviation from upstream

## Classification Labels

All labels are flat (no sub-categories). Labels with the `AZL-` prefix are AZL-specific customizations; the Sankey diagram groups them under a virtual "AZL-customization" node for visual clarity.

### Backport-dist-git

A patch or fix that is **already available in the upstream dist-git** (any Fedora branch/version or the upstream project repo), backported or cherry-picked into AZL because AZL pins an older version or snapshot, or because the fix hasn't been picked up by Fedora yet. These are **self-resolving** — they will be removed when AZL bumps its upstream pin or Fedora branch to include the fix. Should be accompanied by upstream commit URLs, CVE references, or an indication of which Fedora version/release contains the fix.

**Indicators:**
- TOML comments or commit body contain `src.fedoraproject.org/rpms/*/c/` URLs
- Description or commit message mentions "backport", "cherry-pick", "backported"
- Description says "Temporary: ... Remove when snapshot includes ..."
- Description mentions "fixed upstream in f4x", "fixed in fedora", "landed in rawhide"
- The actual upstream fix is applied as a patch (not a workaround)
- CVE reference (e.g., `CVE-2024-12345`)
- Upstream bug tracker or commit URL (github.com, bugzilla)
- `patch-add` or `file-add` overlay adding a `.patch`/`.diff` file authored by an upstream contributor (not AZL/Microsoft)
- Patch filename contains an upstream bug tracker ID (e.g., `IVY-1652`, `bz#NNNN`, `GH-NNN`)
- Patch fixes compatibility with a newer toolchain/runtime (Java 14+, GCC 15, Python 3.13, etc.)
- Commit header starts with `fix(` without AZL-specific keywords

### AZL-dependency-pruning

Removes a BuildRequires or Requires because the dependency package isn't available or isn't shipped in AZL.

**Examples:** Removing `yasm`, `libavif-devel`, `ffmpeg` dependencies.

### AZL-feature-disablement

Disables a build feature, subpackage, or optional capability that AZL doesn't need or can't support.

**Examples:** `--without mingw`, disabling Xen in grub2, disabling crash reporter in Firefox, `%global with_X 0`.

### AZL-branding-policy

Changes Fedora-specific names, paths, identities, or vendor strings to Azure Linux equivalents. Also includes alignment with RHEL/enterprise conventions where AZL deliberately follows RHEL rather than Fedora.

**Examples:** Replacing "Fedora" with "AzureLinux" in boot entries, setting `distro = azurelinux`, EFI vendor paths, `--with-distro=redhat` for RHEL-aligned defaults, `build.defines = { rhel = "11" }`.

### AZL-build

Adjusts for differences in AZL's build toolchain, mock environment, or CI infrastructure compared to Fedora's.

**Examples:** `-std=gnu89` for older C code, compiler triple fixes, `%autosetup` additions, mock/container workarounds, Koji builder adjustments.

### AZL-test-disablement

Skips or disables tests that fail in AZL's build or CI environment. Includes both bulk check-skip (component-check-disablement.toml) and per-overlay test skipping.

**Examples:** `check.skip = true`, skipping inotify tests in containers, removing test-only BuildRequires.

### AZL-security

Changes related to FIPS, cryptographic policy, or security hardening specific to AZL's compliance requirements.

**Examples:** Removing `fips.so`, FIPS provider changes, crypto policy adjustments, debuginfo suppression for malware scan.

### AZL-release-management

Overlays that manage Release tag values, changelog behavior, or version pinning mechanics required by azldev's rendering pipeline.

**Examples:** `spec-set-tag Release`, handling `%autorelease` conditional logic, `pkgrelease`/`specrelease` macros.

### AZL-missing-dependency-workaround

Adds a dependency or patches around a package not yet imported into AZL. Expected to be **temporary** — should be resolved when the missing package is imported.

**Examples:** "WORKAROUND: Remove virt-firmware-rs BuildRequires — not yet in AZL4", adding missing transitive deps during bootstrap.

### AZL-platform-adaptation

Adjusts for AZL's supported architectures or platform-specific behavior not covered by Fedora's defaults.

**Examples:** ARM64/aarch64 SVE fixes, architecture-conditional patches, ExcludeArch/ExclusiveArch changes.

## Upstreamability Tag

Orthogonal to the category label. Records whether the overlay's change can or should be pushed upstream. Values: `yes`, `no`, `unknown`.

### yes — Upstreamable

The overlay addresses something that could benefit from upstream action:

1. **Self-created fix, no upstream PR yet** — A fix authored by AZL/Microsoft that should be contributed upstream (e.g., a Makefile fix in openpace). Once accepted upstream and included in Fedora, the overlay can be removed.

2. **Workaround for a missing upstream fix** — The overlay works around a problem (e.g., disabling flaky tests) that needs an upstream fix. The overlay is temporary until the upstream fix is available.

3. **Related to an upstream gap** — The upstream project lacks a feature or macro that could be added (e.g., qemu's audio backend build flags lack disable macros in Fedora). An upstream change is possible, but the overlay may still be needed even after the upstream change lands.

### no — Not upstreamable

The change is inherently AZL-specific:
- Branding/vendor changes (Fedora → AzureLinux)
- Release tag management (azldev pipeline mechanics)
- AZL-only build infrastructure adjustments
- Backport-dist-git entries (fix already exists upstream)

### unknown

Insufficient information to determine upstreamability. Requires manual or LLM review.
