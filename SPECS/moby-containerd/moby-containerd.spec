%global debug_package %{nil}
%define upstream_name containerd
%define commit_hash 10c12954828e7c7c9b6e0ea9b0c02b01407d3ae1
Summary:        Industry-standard container runtime
Name:           moby-%{upstream_name}
Version:        1.6.6+azure
Release:        9%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Tools/Container
URL:            https://www.containerd.io
# Git clone is a standard practice of producing source files for moby-* packages.
# Please look at ./generate-sources.sh for generating source tar ball.
Source0:        https://github.com/containerd/containerd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        containerd.service
Source2:        containerd.toml
Source3:        NOTICE
Source4:        LICENSE
Patch0:         Makefile.patch
Patch1:         CVE-2022-23471.patch
Patch2:         add_ptrace_readby_tracedby_to_apparmor.patch
Patch3:         CVE-2023-25173.patch
Patch4:         CVE-2023-25153.patch

%{?systemd_requires}

BuildRequires:  bash
BuildRequires:  btrfs-progs-devel
BuildRequires:  cmake
BuildRequires:  device-mapper-devel
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  go-md2man
BuildRequires:  golang
BuildRequires:  libltdl-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libselinux-devel
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  systemd-devel
BuildRequires:  tar
BuildRequires:  which
Requires:       bash
Requires:       device-mapper-libs >= 1.02.90-1
Requires:       libcgroup
Requires:       libseccomp >= 2.3
Requires:       moby-runc >= 1.0.0~rc10~
Requires:       apparmor-parser
Requires:       libapparmor
Conflicts:      containerd
Conflicts:      containerd-io
Conflicts:      moby-engine <= 3.0.10
Obsoletes:      containerd
Obsoletes:      containerd-io

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
export BUILDTAGS="-mod=vendor"
make VERSION="%{version}" REVISION="%{commit_hash}" DESTDIR="%{buildroot}" PREFIX="%{_prefix}" install install-man

mkdir -p %{buildroot}/%{_unitdir}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/containerd.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/containerd/config.toml

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

%changelog
* Wed Mar 01 2023 Mitch Zhu <mitchzhu@microsoft.com> - 1.6.6+azure-9
- Add patch to fix CVE-2023-25153

* Tue Feb 28 2023 Mitch Zhu <mitchzhu@microsoft.com> - 1.6.6+azure-8
- Add patch to fix CVE-2023-25173

* Tue Dec 27 2022 Aadhar Agarwal <aadagarwal@microsoft.com> - 1.6.6+azure-7
- Backport upstream fix in containerd to add ptrace readby and tracedby to default AppArmor profile (add_ptrace_readby_tracedby_to_apparmor.patch)

* Tue Dec 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.6.6+azure-6
- Bump release to rebuild with go 1.18.8-2

* Tue Dec 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.6.6+azure-5
- Add patch for CVE-2022-23471

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.6.6+azure-4
- Bump release to rebuild with go 1.18.8

* Wed Aug 17 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.6.6+azure-3
- Bump to rebuild with golang 1.18.5-1

* Tue Jun 28 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.6.6+azure-2
- Add dependency on apparmor-parser, libapparmor
* Mon Jun 20 2022 Andrew Phelps <anphel@microsoft.com> - 1.6.6+azure-1
- Upgrade to version 1.6.6 to fix CVE-2022-31030
- Lint spec
* Tue Jun 07 2022 Andrew Phelps <anphel@microsoft.com> - 1.5.9+azure-7
- Bumping release to rebuild with golang 1.18.3
* Fri Apr 29 2022 chalamalasetty <chalamalasetty@live.com> - 1.5.9+azure-6
- Bumping 'Release' to rebuild with updated Golang version 1.16.15-2.
* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.5.9+azure-5
- Bump release to force rebuild with golang 1.16.15
* Thu Mar 03 2022 Anirudh Gopal <angop@microsoft.com> - 1.5.9+azure-4
- Enable containerd service restart
* Wed Mar 02 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.5.9+azure-3
- Fix CVE-2022-23648
* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 1.5.9+azure-2
- Bump release to force rebuild with golang 1.16.14
* Wed Jan 19 2022 Henry Beberman <henry.beberman@microsoft.com> - 1.5.9+azure-1
- Update to version 1.5.9+azure
* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 1.4.4+azure-6
- Increment release for force republishing using golang 1.16.12
* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.4.4+azure-5
- Increment release for force republishing using golang 1.16.9
* Mon Oct 04 2021 Henry Beberman <henry.beberman@microsoft.com> 1.4.4+azure-4
- Patch CVE-2021-41103
- Change config to noreplace
- Refactor how files is specified
* Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.4.4+azure-3
- Increment release to force republishing using golang 1.16.7.
* Mon Jul 19 2021 Neha Agarwal <nehaagarwal@microsoft.com> 1.4.4+azure-2
- CVE-2021-32760 fix
* Mon Jul 12 2021 Andrew Phelps <anphel@microsoft.com> 1.4.4+azure-1
- Update to version 1.4.4+azure
* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.3.4+azure-3
- Increment release to force republishing using golang 1.15.13.
* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.3.4+azure-2
- Increment release to force republishing using golang 1.15.
* Thu Jun 11 2020 Andrew Phelps <anphel@microsoft.com> 1.3.4+azure-1
- Update to version 1.3.4+azure
* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 1.3.3+azure-6
- Remove reliance on existing GOPATH environment variable.
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.3.3+azure-5
- Added %%license line automatically
* Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.3.3+azure-4
- Removing *Requires for "ca-certificates".
* Tue May 05 2020 Eric Li <eli@microsoft.com> 1.3.3+azure-3
- Add #Source0: and license verified
* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 1.3.3+azure-2
- Renaming go to golang
* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 1.3.3+azure-1
- Initial CBL-Mariner import from Azure.
* Thu Jan 23 2020 Brian Goff <brgoff@microsoft.com>
- Initial version
