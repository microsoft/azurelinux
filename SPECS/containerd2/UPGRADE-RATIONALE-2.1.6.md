# containerd2 Upgrade Rationale: 2.0.0 → 2.1.6

## Summary
Upgrade containerd2 from v2.0.0 (release 17) to v2.1.6.
Branch: aadagarwal/upgrade-containerd-2.1.6
Date: 2026-02-05

## Decision Log

### 1. Target Version: 2.1.6
**Decision:** Upgrade to 2.1.6 (latest 2.1.x patch) rather than 2.0.x or 2.2.x.
**Rationale:** 2.1.6 is the latest stable patch release of the 2.1 series (released Dec 17, 2025). It includes all security fixes from 2.0.x plus new features and stability improvements. 2.2.x is not yet released. The 2.0.x branch is a dead-end that will stop receiving updates.

### 2. Config Version: Upgrade to Version 3
**Decision:** Update containerd.toml from config version 2 to version 3.
**Rationale:** Version 3 is the recommended config format for containerd 2.x (introduced in 2.0). Plugin paths changed from `io.containerd.grpc.v1.cri` to `io.containerd.cri.v1.runtime` / `io.containerd.cri.v1.images`. While version 2 is still auto-converted, it is deprecated with removal postponed to v2.3 (per upstream PRs #11684, #12431). Updating now avoids future churn and aligns with upstream documentation.

### 3. runc Dependency: Bump to >= 1.3.0
**Decision:** Change `Requires: runc >= 1.2.2` to `Requires: runc >= 1.3.0`.
**Rationale:** containerd 2.1.6 bundles runc v1.3.4 as its reference runtime (PR #12618). Azure Linux 3.0 currently has runc 1.3.3 packaged. Setting >= 1.3.0 ensures we get the 1.3.x series which includes security fixes (GHSA-qw9x-cqr3-wc7r, GHSA-cgrx-mc8f-2prm, GHSA-9493-h29p-rfm2) listed in the 2.1.5 release notes, while remaining compatible with the available runc version.

### 4. Go Version Constraint: Remove upper bound
**Decision:** Change `BuildRequires: golang < 1.25` to `BuildRequires: golang` (no version constraint).
**Rationale:** containerd 2.1.6's go.mod declares `go 1.24.2`. Azure Linux 3.0 currently has Go 1.25.6 available. The old `< 1.25` constraint would block builds. Go 1.25 is fully backward-compatible with code requiring Go 1.24, so removing the upper bound is safe.

### 5. CVE Patches: Drop 7, Verify Each; Credential-leak Patch Also Upstreamed
**Decision:** Remove all 7 CVE patches and the credential-leak patch (8 total dropped) after upstream verification.
**Rationale for each:**

| Patch | CVE | Drop Reason |
|---|---|---|
| CVE-2024-25621.patch | CVE-2024-25621 | Core fix by Akihiro Suda upstreamed Oct 2025; included in 2.1.x. Verification: check `cmd/containerd/server/server.go` for `0o700` permissions. |
| CVE-2024-40635.patch | CVE-2024-40635 | Core OCI spec fix cherry-picked from upstream Mar 2025. Verification: check `pkg/oci/spec_opts.go` for `math.MaxInt32` bounds check. |
| CVE-2024-45338.patch | CVE-2024-45338 | `golang.org/x/net` bumped from v0.30.0 to v0.47.0 in 2.1.6. Verification: check `vendor/golang.org/x/net/html/foreign.go` for `strings.EqualFold`. |
| CVE-2025-22872.patch | CVE-2025-22872 | Same `golang.org/x/net` bump covers this fix. Verification: check `vendor/golang.org/x/net/html/token.go` for self-closing tag fix. |
| CVE-2025-27144.patch | CVE-2025-27144 | `go-jose/go-jose/v4` bumped from v4.0.4 to v4.0.5 in 2.1.0. Verification: check `vendor/github.com/go-jose/go-jose/v4/jwe.go` for `strings.SplitN`. |
| CVE-2025-47291.patch | CVE-2025-47291 | Core fix upstream (PR #11568). Verification: check `client/task.go` for `getRuncOptions()` method. |
| CVE-2025-64329.patch | CVE-2025-64329 | Core fix authored Aug 2024, before 2.1.0. Verification: check `internal/cri/io/container_io.go` for `ctx.Done()` in Attach. |

### 6. Microsoft Patches: Retain and Rebase 2, Carry 1 New (Partially Upstreamed)
**Decision:** Keep multi-snapshotters-support and tardev-support patches. Drop fix-credential-leak-in-cri-errors.patch (superseded). Add fix-credential-leak-in-grpc-errors.patch (follow-up not yet in 2.1.6).
**Rationale:**
- **multi-snapshotters-support**: Enables per-runtime-handler snapshotter selection needed for Kata/Confidential Containers. Author: Mitch Zhu (Microsoft). Required rebase due to CRI Transfer Service refactoring in 2.1 — one hunk conflicted in `image_pull.go` (duplicate `snapshotterFromPodSandboxConfig` call) and was manually resolved.
- **tardev-support**: Adds snapshot labels for tardev-snapshotter (Azure Linux Kata CC). Author: Mitch Zhu (Microsoft). Applied cleanly with no changes needed.
- **fix-credential-leak-in-cri-errors.patch**: DROPPED — superseded. The original patch contained two upstream commits:
  - **Commit 1** (`3e2cee2`, PR #12491, merged Nov 19 2025): Adds `SanitizeError()` in `internal/cri/util/sanitize.go` and calls it inside `defer` blocks in `instrumented_service.go` to redact query parameters in CRI error logs. **This IS included in 2.1.6.** ✅
  - **Commit 2** (`7b11d6c`, PR #12801, merged ~Jan 2026): Follow-up that **moves** `SanitizeError()` from the `defer` block to BEFORE `errgrpc.ToGRPC(err)` return, preventing credential leak in gRPC errors returned to kubelet (visible via `kubectl describe pod`). **This is NOT in 2.1.6** (merged after Dec 17 release). ❌
- **fix-credential-leak-in-grpc-errors.patch**: NEW — carries only the Commit 2 changes (moving `SanitizeError` before return in 4 functions: `PullImage`, `ListImages`, `ImageStatus`, `RemoveImage`). This patch should be dropped once containerd is upgraded to a version containing commit `7b11d6c`.

### 7. Breaking Changes Accepted
**Decision:** Accept all upstream breaking changes in 2.1.x.
**Rationale:**
- **Schema 1 image removal**: Docker v2 Schema 1 has been deprecated since 2015. No Azure Linux images use this format.
- **Dynamic library plugins removed**: Azure Linux does not use `.so`-based containerd plugins.
- **Transfer Service default for CRI image pull**: Containerd auto-detects config conflicts and falls back to local pull. No manual intervention needed for existing setups.
- **FreeBSD defaults reorganized**: Not applicable to Azure Linux.

### 8. Downstream Dependencies: No Changes Needed
**Decision:** Keep existing Provides/Obsoletes directives unchanged.
**Rationale:** `containerd2` already provides `containerd`, `moby-containerd`, and `moby-containerd-cc`. Downstream packages (kubernetes, moby-engine, kata-containers, kata-containers-cc) resolve to containerd2 via these aliases. Version bump is transparent to dependents.

## Verification Checklist
- [ ] Go 1.24.x available in build environment
- [ ] runc >= 1.3.4 available in Azure Linux 3.0
- [ ] Each CVE patch verified as fixed in 2.1.6 source
- [ ] 3 Microsoft patches apply cleanly onto 2.1.6 (multi-snapshotters, tardev, credential-leak-grpc)
- [ ] RPM builds successfully
- [ ] containerd starts with new config
- [ ] Image pull works (Transfer Service path)
- [ ] Container lifecycle works (create, start, stop, remove)
- [ ] Downstream packages install without dependency conflicts
