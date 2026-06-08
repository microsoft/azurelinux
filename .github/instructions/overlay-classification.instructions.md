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

A patch or fix that is **already available in Fedora** (any Fedora branch/version), backported or cherry-picked into AZL because AZL pins an older version or snapshot. These are **self-resolving** — they will be removed when AZL bumps its upstream pin or Fedora branch to include the fix. Should be accompanied by upstream commit URLs or an indication of which Fedora version/release contains the fix.

**Indicators:**
- TOML comments or commit body contain `src.fedoraproject.org/rpms/*/c/` URLs
- Description or commit message mentions "backport", "cherry-pick", "backported"
- Description says "Temporary: ... Remove when snapshot includes ..."
- Description mentions "fixed upstream in f4x", "fixed in fedora", "landed in rawhide"
- The actual upstream fix is applied as a patch (not a workaround)

### Upstream-fix

A fix for a real bug (build failure, CVE, runtime issue) that **is not yet in any Fedora branch**. These are **candidates for upstreaming** — the team should track whether the fix has been submitted upstream or to Fedora. Should indicate relevant links to bugs or in-progress PRs if upstreaming is underway. If a fix was rejected upstream, note that in the rationale.

**Note:** If a fix exists in the upstream project repo but Fedora hasn't picked it up in any branch, it's still Upstream-fix. It only becomes Backport-fedora once Fedora ships it.

#### Upstream-fix Sub-Categories

| Sub-category | Description |
|---|---|
| **Upstreamable** | Self-created fix that should be pushed upstream. No upstream PR/bug link exists yet (e.g., openpace Makefile fix with "TODO: push to upstream"). |
| **Waiting-for-fedora** | Fix is merged or in-progress upstream (has PR URLs, bug IDs, commit links, or CVE refs). Waiting for upstream to release and/or Fedora to pick up the new version (e.g., vamp-plugin-sdk with merged commit not yet in a release). |

**Indicators:**
- CVE reference (e.g., `CVE-2024-12345`)
- Upstream bug tracker or commit URL (github.com, bugzilla)
- `patch-add` or `file-add` overlay adding a `.patch`/`.diff` file authored by an upstream contributor (not AZL/Microsoft)
- Patch filename contains an upstream bug tracker ID (e.g., `IVY-1652`, `bz#NNNN`, `GH-NNN`)
- Patch fixes compatibility with a newer toolchain/runtime (Java 14+, GCC 15, Python 3.13, etc.)
- Commit header starts with `fix(` without AZL-specific keywords

### AZL-customization

An intentional deviation from Fedora specific to Azure Linux's requirements. These are **not expected to be upstreamed** and represent AZL-specific adaptation. This includes workarounds for missing dependencies or version gaps in AZL's tracked Fedora branch — if the overlay works around a problem (e.g., disables a feature) rather than applying the actual fix, it's a customization even if the fix exists in Fedora.

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
