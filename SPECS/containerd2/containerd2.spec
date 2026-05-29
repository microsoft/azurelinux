%global debug_package %{nil}
%define upstream_name containerd
%define commit_hash 193637f7ee8ae5f5aa5248f49e7baa3e6164966e

Summary: Industry-standard container runtime
Name: %{upstream_name}2
Version: 2.2.4
Release: 1%{?dist}
License: ASL 2.0
Group: Tools/Container
URL: https://www.containerd.io
Vendor: Microsoft Corporation
Distribution: Azure Linux

Source0: https://github.com/containerd/containerd/archive/v%{version}.tar.gz#/%{upstream_name}-%{version}.tar.gz
Source1: containerd.service
Source2: containerd.toml

Patch0:	multi-snapshotters-support.patch
Patch1:	tardev-support.patch
Patch2:	CVE-2026-39882.patch
Patch3:	CVE-2026-33814.patch
Patch4:	fix-TestCgroupNamespace-cgroupv1.patch
Patch5:	CVE-2026-39821.patch
Patch6:	CVE-2026-42506.patch
Patch7:	CVE-2026-27136.patch

%{?systemd_requires}

BuildRequires: golang < 1.25
BuildRequires: go-md2man
BuildRequires: make
BuildRequires: systemd-rpm-macros

Requires: runc >= 1.2.2

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
%autosetup -p1 -n %{upstream_name}-%{version}

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
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/containerd/config.toml
install -vdm 755 %{buildroot}/opt/containerd/{bin,lib}

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
%dir /opt/containerd
%dir /opt/containerd/bin
%dir /opt/containerd/lib

%changelog
* Thu May 28 2026 Aadhar Agarwal <aadagarwal@microsoft.com> - 2.2.4-1
- Upgrade to 2.2.4
- Pulls in CVE-2026-46680 fix (PR #13448 / 0a8f65bef)
- Remove CVE-2026-34986.patch (in v2.2.4: go-jose/v4 v4.1.4, PR #13292 / 4413816ce)
- Remove CVE-2026-35469.patch (in v2.2.3: spdystream v0.5.1 / 31bd34a06)
- Remove fix-credential-leak-in-cri-errors.patch (in v2.2.2: PR #12491 / cb3ae2119)
- Retain CVE-2026-39882.patch (otel v1.35.0 lacks PR #8108)
- Retain CVE-2026-33814.patch (x/net v0.47.0 lacks 1e71bd86e)
- Add fix-TestCgroupNamespace-cgroupv1.patch (PR #13240; allows %check on cgroup-v1 build hosts)
- Regenerate multi-snapshotters-support.patch against v2.2.4 (upstream absorbed runtimeHandler plumbing in v2.2.3)

* Wed May 28 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.1.6-5
- Patch for CVE-2026-33814

* Mon May 28 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.1.6-4
- Patch for CVE-2026-39882

* Wed May 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.1.6-3
- Patch for CVE-2026-42506, CVE-2026-39821, CVE-2026-27136

* Fri Apr 24 2026 Jyoti Kanase <v-jykanase@microsoft.com> - 2.1.6-2
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

* Wed Jan 21 2026 Aadhar Agarwal <aadagarwal@microsoft.com> - 2.0.0-17
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
