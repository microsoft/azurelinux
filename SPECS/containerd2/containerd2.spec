%global debug_package %{nil}
%define upstream_name containerd
%define commit_hash 207ad711eabd375a01713109a8a197d197ff6542

Summary: Industry-standard container runtime
Name: %{upstream_name}2
Version: 2.0.0
Release: 17%{?dist}
License: ASL 2.0
Group: Tools/Container
URL: https://www.containerd.io
Vendor: Microsoft Corporation
Distribution: Azure Linux

Source0: https://github.com/containerd/containerd/archive/v%{version}.tar.gz#/%{upstream_name}-%{version}.tar.gz
Source1: containerd.service
Source2: containerd.toml

Patch0:	CVE-2024-45338.patch
Patch1:	CVE-2025-27144.patch
Patch2:	CVE-2024-40635.patch
Patch3:	CVE-2025-22872.patch
Patch4:	CVE-2025-47291.patch
Patch5:	multi-snapshotters-support.patch
Patch6:	tardev-support.patch
Patch7: CVE-2024-25621.patch
Patch8: CVE-2025-64329.patch
Patch9: fix-credential-leak-in-cri-errors.patch
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
