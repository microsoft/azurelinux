%global debug_package %{nil}
%define upstream_name containerd

# Source: official upstream containerd v2.2.4 release tarball
# build-rpm.sh reads these globals and downloads:
#   https://github.com/<github_owner>/<github_repo>/archive/<branch_name>.tar.gz
# saving it as ${spec_name}-${Version}.tar.gz next to this spec.
# GitHub returns an immutable archive for a tag ref, giving us reproducible
# source between rebuilds.
%global github_owner containerd
%global github_repo  containerd
%global branch_name  v%{version}
# GitHub tag archives extract to: <repo>-<version>
%global extracted_dir %{github_repo}-%{version}

# REVISION metadata embedded in `containerd --version`. v2.2.4 commit pin from
# https://github.com/containerd/containerd/releases/tag/v2.2.4.
%define commit_hash 193637f7ee8ae5f5aa5248f49e7baa3e6164966e

Summary: Industry-standard container runtime
Name: %{upstream_name}2
# Tracks the AzureLinux 3.0-dev containerd2 baseline at Version 2.2.4.
Version: 2.2.4
# Release "6000.verity" distinguishes this dadelan fork build from any
# future official AzureLinux containerd2-2.2.4-N release (which start at
# Release: 1, 2, ...). The 6xxx range succeeds the prior 5xxx steamboat
# RPM stream and the 4xxx 2.2.0-patch-based / 3xxx fork-tarball builds.
# The ".verity" suffix marks the dm-verity erofs snapshotter patch set
# (Patch8-9 of PATCHES.md). No .commit_hash tag since the upstream is an
# immutable release tag.
# IMPORTANT: any future official AzureLinux containerd2-2.2.4-N release
# will be considered OLDER than this; bump Epoch or pin to a higher Version
# if you ever need to deprecate this stream.
Release: 6000.verity%{?dist}
License: ASL 2.0
Group: Tools/Container
URL: https://www.containerd.io
Vendor: Microsoft Corporation
Distribution: Azure Linux

# AzureLinux toolkit downloads from GitHub using github_owner/repo/branch_name
# above and stores it as ${upstream_name}-${Version}.tar.gz in the toolchain
# cache; the SHA in containerd2.signatures.json gates the download.
Source0: https://github.com/%{github_owner}/%{github_repo}/archive/%{branch_name}.tar.gz#/%{upstream_name}-%{version}.tar.gz
Source1: containerd.service
# dm-verity-aware containerd config (enables erofs snapshotter + differ).
Source2: containerd-config-dmverity.toml
# systemd-modules-load.d entry: erofs + dm_verity must be loaded before
# containerd.service starts (differ asserts dm_verity at init).
Source3: aks-dmverity-modules.conf
# containerd.service.d drop-in: ExecStartPre re-overlays Source2 onto
# /etc/containerd/config.toml on every start, so AKS CSE's bootstrap-time
# clobber gets undone before containerd reads the config.
Source4: containerd-dmverity-overlay.conf
# Registry mirror: mcr.microsoft.com -> notaryaksegistry.azurecr.io, where
# the dm-verity notation referrers live.
Source5: mcr-mirror-hosts.toml

# ============================================================================
# Patches
# ============================================================================
# Patch0-7: AzureLinux 3.0-dev containerd2 baseline patches, copied verbatim
#           from microsoft/azurelinux@origin/3.0-dev:SPECS/containerd2 at
#           commit 5a4864f9 (Release: 2). Includes:
#             - multi-snapshotters-support / tardev-support carry-patches
#             - 5 CVE backports (CVE-2026-{39882,33814,39821,42506,27136})
#             - fix-TestCgroupNamespace-cgroupv1 test fix
# Patch8-9: dm-verity fork work, ported from 4001 against v2.2.4 + AZL stack.
#           See PATCHES.md for the squash provenance back to the original
#           10 fork commits.
# ============================================================================

Patch0:  multi-snapshotters-support.patch
Patch1:  tardev-support.patch
Patch2:  CVE-2026-39882.patch
Patch3:  CVE-2026-33814.patch
Patch4:  fix-TestCgroupNamespace-cgroupv1.patch
Patch5:  CVE-2026-39821.patch
Patch6:  CVE-2026-42506.patch
Patch7:  CVE-2026-27136.patch
# dm-verity series — see PATCHES.md for provenance.
Patch8:  0004-snapshotters-erofs-add-dm-verity-formatting-and-sign.patch
Patch9:  0005-snapshotters-erofs-add-require_signatures-policy-com.patch

%{?systemd_requires}

BuildRequires: golang < 1.25
BuildRequires: go-md2man
BuildRequires: make
BuildRequires: systemd-rpm-macros

Requires: runc >= 1.2.2
# Runtime dependencies for the dm-verity erofs differ:
#   erofs-utils  - provides mkfs.erofs, called by the differ to convert tar
#                  layers into erofs filesystems before verity hashing.
#   veritysetup  - standalone on Azure Linux (NOT bundled with cryptsetup);
#                  formats each erofs layer with a dm-verity hash tree.
# Both are in the azurelinux-official-base repo so dependency resolution
# works during VHD build and on customer-provisioned nodes.
Requires: erofs-utils
Requires: veritysetup

# This package replaces the old name of containerd
Provides: containerd = %{version}-%{release}
Obsoletes: containerd < %{version}-%{release}

# This package replaces the old name of moby-containerd
Provides: moby-containerd = %{version}-%{release}
Obsoletes: moby-containerd < %{version}-%{release}

# This package replaces moby-containerd-cc
Provides: moby-containerd-cc = %{version}-%{release}
Obsoletes: moby-containerd-cc < %{version}-%{release}

%description
containerd is an industry-standard container runtime with an emphasis on
simplicity, robustness and portability. It is available as a daemon for Linux
and Windows, which can manage the complete container lifecycle of its host
system: image transfer and storage, container execution and supervision,
low-level storage and network attachments, etc.

containerd is designed to be embedded into a larger system, rather than being
used directly by developers or end-users.

%prep
%autosetup -p1 -n %{extracted_dir}

%build
export BUILDTAGS="-mod=vendor"
make VERSION="%{version}" REVISION="%{commit_hash}" binaries man

%check
export BUILDTAGS="-mod=vendor"
make VERSION="%{version}" REVISION="%{commit_hash}" test

%install
make VERSION="%{version}" REVISION="%{commit_hash}" DESTDIR="%{buildroot}" PREFIX="/usr" install install-man

mkdir -p %{buildroot}/%{_unitdir}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/containerd.service
install -vdm 755 %{buildroot}/opt/containerd/{bin,lib}

# dm-verity-aware containerd config, dropped at the canonical path.
# %config(noreplace) preserves operator edits across RPM upgrades.
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/containerd/config.toml

# Stash the same config under /usr/share/containerd2 so the systemd drop-in
# (Source4) can re-overlay it after AKS CSE rewrites /etc/containerd/config.toml
# at bootstrap. Single source of truth — any change to Source2 propagates to
# both standalone and AKS consumers.
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_datadir}/containerd2/config.toml

install -D -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/modules-load.d/aks-dmverity.conf
install -D -p -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/systemd/system/containerd.service.d/dmverity-overlay.conf
install -D -p -m 0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/containerd/certs.d/mcr.microsoft.com/hosts.toml

%post
%systemd_post containerd.service

if [ $1 -eq 1 ]; then # Package install
	systemctl enable containerd.service > /dev/null 2>&1 || :
	systemctl start containerd.service > /dev/null 2>&1 || :
fi

%preun
%systemd_preun containerd.service

%postun
%systemd_postun_with_restart containerd.service

%files
%license LICENSE NOTICE
%{_bindir}/*
%{_mandir}/*
%config(noreplace) %{_unitdir}/containerd.service
%config(noreplace) %{_sysconfdir}/containerd/config.toml
%{_datadir}/containerd2/config.toml
%{_sysconfdir}/modules-load.d/aks-dmverity.conf
%{_sysconfdir}/systemd/system/containerd.service.d/dmverity-overlay.conf
%config(noreplace) %{_sysconfdir}/containerd/certs.d/mcr.microsoft.com/hosts.toml
%dir %{_sysconfdir}/containerd
%dir %{_sysconfdir}/containerd/certs.d
%dir %{_sysconfdir}/containerd/certs.d/mcr.microsoft.com
%dir %{_sysconfdir}/systemd/system/containerd.service.d
%dir %{_datadir}/containerd2
%dir /opt/containerd
%dir /opt/containerd/bin
%dir /opt/containerd/lib

%changelog
* Tue Jun 02 2026 Dallas Delaney <dadelan@microsoft.com> - 2.2.4-5000
- Port to upstream containerd v2.2.4 + AzureLinux 3.0-dev baseline.
- Drop 0001 (diff-walking mount-manager): merged upstream in v2.2.2
  (PR #13186 / commit 409f75be8), ancestor of v2.2.4.
- Drop 0002 (tardev-support): now provided by AzureLinux baseline as
  tardev-support.patch (Patch1).
- Drop 0003 (cri credential leak): merged upstream in v2.2.2 (PR #12491 /
  commit cb3ae2119), ancestor of v2.2.4.
- Adopt AzureLinux 3.0-dev's 8-patch baseline verbatim (Patch0-7):
  multi-snapshotters-support, tardev-support, 5 CVE backports
  (CVE-2026-{39882,33814,39821,42506,27136}), fix-TestCgroupNamespace-cgroupv1.
- Regenerate 0004 + 0005 against v2.2.4 tree (5 context-only conflicts in
  0004 hand-fixed: docs/snapshotters/erofs.md trailing TODO, go.mod, go.sum,
  plugins/snapshots/erofs/erofs.go, plugins/snapshots/erofs/plugin/plugin.go;
  0005 applied cleanly with offsets). Preserves boltdb label-cap fix
  (containerd.io/dmverity/* keys).
- Switch Source0 from per-commit GitHub archive to v%{version} release tag.
- Switch %autosetup target dir from %{extracted_dir}=<repo>-<sha> to
  %{extracted_dir}=<repo>-<version> to match release-tarball layout.

* Tue Jun 02 2026 Dallas Delaney <dadelan@microsoft.com> - 2.2.0-4001.cb15e731a
- 0004 patch fix: rename TargetLayer{Signature,RootHash}Label prefix from
  containerd.io/snapshot/ to containerd.io/dmverity/. The old prefix matched
  snapshots.FilterInheritedLabels and auto-promoted the base64 PKCS#7 sig
  into a boltdb snapshot label, which exceeded the 4096-byte label cap
  for enterprise ESRP signatures (RSA-4096 leaf + intermediates + RFC3161
  timestamp = ~5.7KB). Pull failed with InvalidArgument. Sidecar-file
  flow into veritysetup is unchanged; label persistence was unread fallout.

* Sun Jun 01 2026 Dallas Delaney <dadelan@microsoft.com> - 2.2.0-4000.cb15e731a
- Patch-based spec. Source pinned to upstream containerd@cb15e731a (immutable)
  with 5 patches (see PATCHES.md). Enables ADO builds without committing
  binary tarballs. Behaviorally equivalent to steamboat 3012.
