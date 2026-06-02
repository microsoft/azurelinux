%global debug_package %{nil}
%define upstream_name containerd

# Source pin: upstream containerd/containerd at commit cb15e731a (Jan 14 2026
# main, descendant of v2.2.0 tag). Chosen as the true branch point of the
# fork dadelan/snapshotter-dmverity-format so that all dm-verity fork
# commits apply as patches on top with ZERO conflicts. See PATCHES.md.
%global github_owner containerd
%global github_repo  containerd
%global branch_name  cb15e731a101d3cfdb94e4c905e43318929104aa
# GitHub commit archives extract to: <repo>-<full-sha>
%global extracted_dir %{github_repo}-%{branch_name}

%define commit_hash cb15e731a101d3cfdb94e4c905e43318929104aa

Summary: Industry-standard container runtime
Name: %{upstream_name}2
# Version pinned to v2.2.0 because cb15e731a is a post-v2.2.0 mainline commit
# (descendant of the v2.2.0 tag, predecessor of v2.3.0-beta.0). Vanilla v2.2.0
# is the closest stable upstream tag in this commit's ancestry; the actual
# tree content is "v2.2.0 + 238 upstream commits + 5 patches".
Version: 2.2.0
# Release range 4xxx distinguishes this patch-based ADO-friendly build from
# the prior steamboat 3xxx fork-tarball builds. The .cb15e731a tag carries
# the source commit so 'rpm -qi containerd2' shows what's installed.
Release: 4000.cb15e731a%{?dist}
License: ASL 2.0
Group: Tools/Container
URL: https://www.containerd.io
Vendor: Microsoft Corporation
Distribution: Azure Linux

# GitHub serves an immutable archive for any commit SHA; saved locally as
# containerd-2.2.0.tar.gz (signature pinned in containerd2.signatures.json).
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
# 0001-0003: AzureLinux-baseline carry-patches (see PATCHES.md for provenance).
# 0004-0005: dm-verity fork work, squashed for upstreaming readability. The
#            split is "core dm-verity (format + per-layer signature verify)"
#            then "require_signatures policy + commitBlock parity + logs".
#            See PATCHES.md for the mapping back to the original 10 commits.
# ============================================================================

Patch0001: 0001-diff-walking-enable-mount-manager.patch
Patch0002: 0002-tardev-support.patch
Patch0003: 0003-fix-credential-leak-in-cri-errors.patch
Patch0004: 0004-snapshotters-erofs-add-dm-verity-formatting-and-sign.patch
Patch0005: 0005-snapshotters-erofs-add-require_signatures-policy-com.patch

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

# dm-verity-aware containerd config at the canonical path.
# %config(noreplace) preserves operator edits across RPM upgrades.
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/containerd/config.toml

# Stash the same config under /usr/share/containerd2 so the systemd drop-in
# (Source4) can re-overlay it after AKS CSE rewrites /etc/containerd/config.toml
# at bootstrap. Single source of truth - any change to Source2 propagates to
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
* Sun Jun 01 2026 Dallas Delaney <dadelan@microsoft.com> - 2.2.0-4000.cb15e731a
- Bump to containerd 2.2.0 pinned at upstream commit cb15e731a.
- Add dm-verity erofs snapshotter signing/verification (patches 0004-0005).
- Add dm-verity-aware config + systemd drop-in + mcr-mirror hosts.toml.
- Drop CVE-2026-34986/CVE-2026-35469/multi-snapshotters-support: do not apply
  cleanly to 2.2.0 tree; rebase as separate work if Security still flags.

* Thu Apr 24 2026 Jyoti Kanase <v-jykanase@microsoft.com> - 2.1.6-2
- Modify CVE-2026-35469 patch for 2.1.6
- Patch for CVE-2026-34986

* Fri Apr 17 2026 Jyoti Kanase <v-jykanase@microsoft.com> - 2.1.6-1
- Upgrade to 2.1.6
- Remove CVE patches fixed in upstream: CVE-2024-25621, CVE-2024-40635,
  CVE-2024-45338, CVE-2025-22872, CVE-2025-27144, CVE-2025-47291,
  CVE-2025-47911, CVE-2025-58190, CVE-2025-64329
- Modify fix-credential-leak-in-cri-errors patch to keep only 2/2 not yet merged in upstream
- Rebase multi-snapshotters-support patch for 2.1.6

* Tue Apr 07 2026 Kanishk Bansal <kanbansal@microsoft.com> - 2.0.0-19
- Patch CVE-2026-35469

* Thu Feb 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.0.0-18
- Patch for CVE-2025-58190, CVE-2025-47911

* Tue Jan 21 2026 Aadhar Agarwal <aadagarwal@microsoft.com> - 2.0.0-17
- Backport fix for credential leak in CRI error logs

* Mon Nov 24 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.0.0-16
- Patch for CVE-2025-64329

* Tue Nov 11 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.0.0-15
- Patch for CVE-2024-25621

* Sun Aug 31 2025 Andrew Phelps <anphel@microsoft.com> - 2.0.0-14
- Set BR for golang to < 1.25

* Mon Jul 21 2025 Saul Paredes <saulparedes@microsoft.com> - 2.0.0-13
- Add "Provides/Obsoletes:" to shift all installs of moby-containerd-cc to containerd2

* Tue Jun 10 2025 Mitch Zhu <mitchzhu@microsoft.com> - 2.0.0-12
- Add updated tardev-snapshotter support patch

* Tue Jun 10 2025 Mitch Zhu <mitchzhu@microsoft.com> - 2.0.0-11
- Add updated multi-snapshotters-support patch

* Fri May 30 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.0.0-10
- Patch CVE-2025-47291

* Thu May 22 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.0.0-9
- Patch CVE-2025-22872

* Wed Apr 09 2025 Aadhar Agarwal <aadagarwal@microsoft.com> - 2.0.0-8
- Fix CVE-2024-40635

* Tue Apr 01 2025 Nan Liu <liunan@microsoft.com> - 2.0.0-7
- Remove the tardev-snapshotter patch for Kata CC support.

* Fri Mar 21 2025 Dallas Delaney <dadelan@microsoft.com> - 2.0.0-6
- Fix CVE-2025-27144

* Mon Mar 03 2025 Nan Liu <liunan@microsoft.com> - 2.0.0-5
- Add "Provides/Obsoletes:" to shift all installs of containerd and moby-containerd to containerd2

* Mon Feb 03 2025 Mitch Zhu <mitchzhu@microsoft.com> - 2.0.0-4
- Fix ptest in tardev-snapshotter support patch

* Sun Jan 26 2025 Mitch Zhu <mitchzhu@microsoft.com> - 2.0.0-3
- Added patch to support tardev-snapshotter for Kata CC.

* Thu Jan 23 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 2.0.0-2
- Fix CVE-2024-45338 by an unstream patch

* Wed Dec 11 2024 Nan Liu <liunan@microsoft.com> - 2.0.0-1
- Created a standalone package for containerd 2.0.0
- Initial CBL-Mariner import from Azure
- Initial version and License verified
