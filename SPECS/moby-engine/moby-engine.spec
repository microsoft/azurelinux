%define commit_hash f417435e5f6216828dec57958c490c4f8bae4f98

Summary: The open-source application container engine
Name:    moby-engine
Version: 25.0.3
Release: 15%{?dist}
License: ASL 2.0
Group:   Tools/Container
URL: https://mobyproject.org
Vendor: Microsoft Corporation
Distribution: Azure Linux

Source0: https://github.com/moby/moby/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: docker.service
Source2: docker.socket

Patch0:  CVE-2022-2879.patch
Patch1:  enable-docker-proxy-libexec-search.patch
Patch2:  CVE-2024-41110.patch
Patch3:  CVE-2024-29018.patch
Patch4:  CVE-2024-24786.patch
Patch5:  CVE-2024-36621.patch
Patch6:  CVE-2024-36620.patch
Patch7:  CVE-2024-36623.patch
Patch8:  CVE-2024-45337.patch
Patch9:  CVE-2023-45288.patch
Patch10: CVE-2025-22868.patch
Patch11: CVE-2025-22869.patch
Patch12: CVE-2025-30204.patch
Patch13: CVE-2024-51744.patch
Patch14: CVE-2025-58183.patch
#This can be removed when upgraded to v28.2.0
Patch15: fix-multiarch-image-push-tag.patch

%{?systemd_requires}

BuildRequires: bash
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
Requires: device-mapper-libs
Requires: docker-init
Requires: iptables
Requires: libcgroup
Requires: libseccomp
Requires: containerd
Requires: tar
Requires: xz

Conflicts: docker
Conflicts: docker-io
Conflicts: docker-engine-cs
Conflicts: docker-ee

Obsoletes: docker-ce < %{version}-%{release}
Obsoletes: docker-engine < %{version}-%{release}
Obsoletes: docker < %{version}-%{release}
Obsoletes: docker-io < %{version}-%{release}

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
DOCKER_GITCOMMIT=${GIT_COMMIT:0:7} DOCKER_BUILDTAGS='seccomp' hack/make.sh dynbinary

%install
mkdir -p %{buildroot}%{_bindir}
install -p -m 755 ./bundles/dynbinary-daemon/dockerd %{buildroot}%{_bindir}/dockerd

mkdir -p %{buildroot}%{_libexecdir}
install -p -m 755 ./bundles/dynbinary-daemon/docker-proxy %{buildroot}%{_libexecdir}/docker-proxy

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

%files
%license LICENSE NOTICE
%{_bindir}/dockerd
%{_libexecdir}/docker-proxy
%{_sysconfdir}/*
%{_unitdir}/*

%changelog
* Wed Jan 21 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 25.0.3-15
- Fix multiarch image push tag

* Sat Nov 15 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 25.0.3-14
- Patch for CVE-2025-58183

* Fri May 23 2025 Akhila Guruju <v-guakhila@microsoft.com> - 25.0.3-13
- Patch CVE-2024-51744

* Mon Apr 21 2025 Dallas Delaney <dadelan@microsoft.com> - 25.0.3-12
- Patch CVE-2025-30204

* Mon Mar 17 2025 Dallas Delaney <dadelan@microsoft.com> - 25.0.3-11
- Patch CVE-2025-22868 & CVE-2025-22869

* Fri Feb 14 2025 Kanishk Bansal <kanbansal@microsoft.com> - 25.0.3-10
- Address CVE-2023-45288

* Fri Dec 20 2024 Aurelien Bombo <abombo@microsoft.com> - 25.0.3-9
- Add patch for CVE-2024-45337

* Wed Dec 04 2024 Adit Jha <aditjha@microsoft.com> - 25.0.3-8
- Fix CVE-2024-36620, CVE-2024-36621, and CVE-2024-36623 with patches

* Mon Nov 25 2024 Bala <balakumaran.kannan@microsoft.com> - 25.0.3-7
- Fix CVE-2024-24786 by patching

* Mon Aug 19 2024 Suresh Thelkar <sthelkar@microsoft.com> - 25.0.3-6
- Patch CVE-2024-29018

* Tue Aug 13 2024 Rohit Rawat <rohitrawat@microsoft.com> - 25.0.3-5
- Address CVE-2024-41110

* Fri Aug 09 2024 Henry Beberman <henry.beberman@microsoft.com> - 25.0.3-4
- Backport upstream change to search /usr/libexec for docker-proxy without daemon.json

* Tue Jun 25 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 25.0.3-3
- Address CVE-2022-2879

* Thu Mar 21 2024 Henry Beberman <henry.beberman@microsoft.com> - 25.0.3-2
- Add the in-tree version of docker proxy built from cmd/docker-proxy into /usr/libexec
- Set userland-proxy-path explicitly by introducing /etc/docker/daemon.json

* Mon Feb 26 2024 Henry Beberman <henry.beberman@microsoft.com> - 25.0.3-1
- Upgrade to version 25.0.3 and clean up spec
- Remove docker-proxy as it's no longer used (2050e085f95bb796e9ff3a325b9985e319c193cf)

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20.10.25-3
- Bump release to rebuild with go 1.20.10

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
