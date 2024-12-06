%define commit_hash fca702de7f71362c8d103073c7e4a1d0a467fadd

Summary: The open-source application container engine
Name:    moby-engine
Version: 24.0.9
Release: 11%{?dist}
License: ASL 2.0
Group:   Tools/Container
URL: https://mobyproject.org
Vendor: Microsoft Corporation
Distribution: Mariner

Source0: https://github.com/moby/moby/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: docker.service
Source2: docker.socket
# Backport of vendored "buildkit" v0.12.5 https://github.com/moby/buildkit/pull/4604 to 0.8.4-0.20221020190723-eeb7b65ab7d6 in this package.
# Remove once we upgrade this package at least to version 25.0+.
Patch1:  CVE-2024-23651.patch
# Backport of vendored "buildkit" v0.12.5 https://github.com/moby/buildkit/pull/4603 to 0.8.4-0.20221020190723-eeb7b65ab7d6 in this package.
# Remove once we upgrade this package at least to version 25.0+.
Patch2:  CVE-2024-23652.patch
Patch3:  CVE-2023-45288.patch
Patch4:  CVE-2023-44487.patch
Patch5:  enable-docker-proxy-libexec-search.patch
Patch6:  CVE-2024-41110.patch
Patch7:  CVE-2024-29018.patch
Patch8:  CVE-2024-36621.patch
Patch9:  CVE-2024-36623.patch

%{?systemd_requires}

BuildRequires: bash
BuildRequires: btrfs-progs-devel
BuildRequires: cmake
BuildRequires: device-mapper-devel
BuildRequires: gcc
BuildRequires: glibc-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: libtool
BuildRequires: libltdl-devel
BuildRequires: make
BuildRequires: pkg-config
BuildRequires: systemd-devel
BuildRequires: tar
BuildRequires: golang
BuildRequires: git

Requires: audit
Requires: /bin/sh
Requires: device-mapper-libs >= 1.02.90-1
Requires: docker-init
Requires: iptables
Requires: libcgroup
Requires: libseccomp >= 2.3
Requires: moby-containerd >= 1.2
Requires: tar
Requires: xz

Conflicts: docker
Conflicts: docker-io
Conflicts: docker-engine-cs
Conflicts: docker-ee

Obsoletes: docker-ce
Obsoletes: docker-engine
Obsoletes: docker
Obsoletes: docker-io

%description
Moby is an open-source project created by Docker to enable and accelerate software containerization.

%define OUR_GOPATH %{_topdir}/.gopath

%prep
%autosetup -p1 -n moby-%{version}

mkdir -p %{OUR_GOPATH}/src/github.com/docker
ln -sfT %{_builddir}/moby-%{version} %{OUR_GOPATH}/src/github.com/docker/docker

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache
export GOPROXY=off
export GO111MODULE=off
export GOGC=off
export VERSION=%{version}

GIT_COMMIT=%{commit_hash}
DOCKER_GITCOMMIT=${GIT_COMMIT:0:7} DOCKER_BUILDTAGS='apparmor seccomp' hack/make.sh dynbinary

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 ./bundles/dynbinary-daemon/dockerd %{buildroot}%{_bindir}/dockerd

mkdir -p %{buildroot}%{_libexecdir}
install -p -m 755 ./bundles/dynbinary-daemon/docker-proxy %{buildroot}%{_libexecdir}/docker-proxy
ln -s %{_libexecdir}/docker-proxy %{buildroot}/%{_bindir}/docker-proxy

mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
install -p -m 644 contrib/udev/80-docker.rules %{buildroot}%{_sysconfdir}/udev/rules.d/80-docker.rules

mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/docker.service
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/docker.socket

%post
if ! grep -q "^docker:" /etc/group; then
    groupadd --system docker
fi

%preun
%systemd_preun docker.service

%postun
%systemd_postun_with_restart docker.service

# list files owned by the package here
%files
%license LICENSE NOTICE
%{_bindir}/dockerd
# docker-proxy symlink in bindir to fix back-compat
%{_bindir}/docker-proxy
%{_libexecdir}/docker-proxy
%{_sysconfdir}/*
%{_unitdir}/*

%changelog
* Wed Dec 04 2024 Adit Jha <aditjha@microsoft.com> - 24.0.9-11
- Patch CVE-2024-36621 & CVE-2024-36623

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 24.0.9-10
- Bump release to rebuild with go 1.22.7

* Mon Aug 19 2024 Suresh Thelkar <sthelkar@microsoft.com> - 24.0.9-9
- Patch CVE-2024-29018

* Mon Aug 05 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 24.0.9-8
- Drop requirement on a specific version of golang

* Mon Jul 29 2024 Rohit Rawat <rohitrawat@microsoft.com> - 24.0.9-7
- Fix for CVE-2024-41110

* Tue Jun 25 2024 Henry Beberman <henry.beberman@microsoft.com> - 24.0.9-6
- Backport upstream change to search /usr/libexec for docker-proxy without daemon.json

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 24.0.9-5
- Bump release to rebuild with go 1.21.11

* Fri May 31 2024 Mitch Zhu <mitchzhu@microsoft.com> - 24.0.9-4
- Fix for CVE-2023-44487

* Fri May 03 2024 Chris Gunn <chrisgun@microsoft.com> - 24.0.9-3
- Fix for CVE-2023-45288

* Wed May 01 2024 Henry Beberman <henry.beberman@microsoft.com> - 24.0.9-2
- Symlink /usr/bin/docker-proxy to /usr/libexec/docker-proxy for back-compat

* Mon Mar 25 2024 Muhammad Falak <mwani@microsoft.com> - 24.0.9-1
- Bump version to 24.X
- Drop un-needed patches
- Remove docker-proxy as it's no longer used (2050e085f95bb796e9ff3a325b9985e319c193cf)
- Add the in-tree version of docker proxy built from cmd/docker-proxy into /usr/libexec
- Set userland-proxy-path explicitly by introducing /etc/docker/daemon.json

* Mon Feb 12 2024 Muhammad Falak <mwani@microsoft.com> - 20.10.27-4
- Bump release to rebuild with go 1.21.6

* Mon Feb 12 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 20.10.27-3
- Fixing CVEs: 2024-23651 and 2024-23652.

* Fri Feb 02 2024 Tobias Brick <tobiasb@microsoft.com> - 20.10.27-2
- Patch CVE-2022-21698

* Fri Dec 15 2023 Rohit Rawat <rohitrawat@microsoft.com> - 20.10.27-1
- Upgrade version to fix CVE-2020-8694, CVE-2020-8695 and CVE-2020-12912

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.25-3
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 20.10.25-2
- Bump release to rebuild with updated version of Go.

* Thu Aug 17 2023 Muhammad Falak <mwani@microsoft.com> - 20.10.25-1
- Bump version to 20.10.25

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.24-4
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.24-3
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.24-2
- Bump release to rebuild with go 1.19.10

* Fri May 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.24-1
- Auto-upgrade to 20.10.24 - since moby-cli was upgraded

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.14-9
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.14-8
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.14-7
- Bump release to rebuild with go 1.19.6

* Wed Mar 15 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 20.10.14-6
- Patch CVE-2023-25153

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.14-5
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.14-4
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 20.10.14-3
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 20.10.14-2
- Bump release to rebuild with go 1.18.8

* Fri Sep 30 2022 Adit Jha <aditjha@microsoft.com> - 20.10.14-1
- Upgrade to 20.10.14 to fix CVE-2022-24769

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 20.10.12-5
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 20.10.12-4
- Bump release to rebuild with golang 1.18.3

* Tue Mar 22 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 20.10.12-3
- Set 'systemd' as default cgroup driver

* Wed Mar 02 2022 Andy Caldwell <andycaldwell@microsoft.com> - 20.10.12-2
- Relax dependency from `tini` to `docker-init`

* Fri Feb 04 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 20.10.12-1
- Update to version 20.10.12
- Use code from upstream instead of Azure fork.

* Mon Oct 04 2021 Henry Beberman <henry.beberman@microsoft.com> 19.03.15+azure-4
- Patch CVE-2021-41091 and CVE-2021-41089
- Switch to autosetup

* Fri Aug 06 2021 Nicolas Guibourge <nicolasg@microsoft.com> 19.03.15+azure-3
- Increment release to force republishing using golang 1.16.7.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 19.03.15+azure-2
- Increment release to force republishing using golang 1.15.13.

* Thu Apr 15 2021 Andrew Phelps <anphel@microsoft.com> 19.03.15+azure-1
- Update to version 19.03.15+azure

* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 19.03.11+azure-4
- Increment release to force republishing using golang 1.15.

* Tue Jul 21 2020 Nicolas Ontiveros <niontive@microsoft.com> 19.03.11+azure-3
- Remove changes for CIS Docker Security Benchmark compliance.

* Fri Jul 03 2020 Chris Co <chrco@microsoft.com> 19.03.11+azure-2
- Remove default daemon configuration

* Thu Jun 11 2020 Andrew Phelps <anphel@microsoft.com> 19.03.11+azure-1
- Update to version 19.03.11+azure

* Thu May 28 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.0.12~rc.1+azure-8
- Make default configuration comply with CIS Docker Security Benchmark.

* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 3.0.12~rc.1+azure-7
- Remove reliance on existing GOPATH environment variable.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 3.0.12~rc.1+azure-6
- Added %%license line automatically

* Fri May 08 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 3.0.12~rc.1+azure-5
- Removing *Requires for "ca-certificates".
- Removing duplicate %%files directive.

* Fri May 08 2020 Eric Li <eli@microsoft.com> 3.0.12~rc.1+azure-4
- Add #Source0: and license verified

* Wed May 06 2020 Mohan Datla <mdatla@microsoft.com> 3.0.12~rc.1+azure-3
- Fixing the moby server version

* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0.12~rc.1+azure-2
- Renaming go to golang

* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 3.0.12~rc.1+azure-1
- Initial CBL-Mariner import from Azure.

* Mon Jan 27 2020 Brian Goffs <brgoff@microsoft.com>
- Use dynamic linking and issue build commands from rpm spec

* Tue Aug 7 2018 Robledo Pontes <rafilho@microsoft.com>
- Adding to moby build tools.

* Mon Mar 12 2018 Xing Wu <xingwu@microsoft.com>
- First draft
