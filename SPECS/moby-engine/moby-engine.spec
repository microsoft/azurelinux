Summary: The open-source application container engine
Name:    moby-engine
Version: 19.03.15+azure
Release: 8%{?dist}
License: ASL 2.0
Group:   Tools/Container

# Git clone is a standard practice of producing source files for moby.
# Please look at ./generate-sources.sh for generating source tar ball.
# ENGINE_REPO=https://github.com/moby/moby.git
%define MOBY_GITCOMMIT 420b1d36250f9cfdc561f086f25a213ecb669b6f

# docker-proxy binary comes from libnetwork
# The proxy code rarely sees any changes
# The default value for the commit is taken from the engine repo
#   see "hack/dockerfile/install/proxy.installer" in that repo
# PROXY_REPO=https://github.com/docker/libnetwork.git
# PROXY_COMMIT=153d0769a1181bf591a9637fd487a541ec7db1e6

# Tini is a tiny container init, it's used as the binary for "docker-init"
# TINI_REPO=https://github.com/krallin/tini.git
# TINI_COMMIT=fec3683b971d9c3ef73f284f176672c44b448662

#Source0: https://github.com/moby/moby/archive/v19.03.15.tar.gz
Source0: moby-engine-%{version}.tar.gz
Source2: docker.service
Source3: docker.socket
Source4: LICENSE
Source5: NOTICE
Patch0:  CVE-2021-41091.patch
Patch1:  CVE-2021-41089.patch
URL: https://mobyproject.org
Vendor: Microsoft Corporation
Distribution: Mariner

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
%autosetup -p1 -c
mkdir -p %{OUR_GOPATH}/src/github.com/docker
ln -sfT %{_topdir}/BUILD/%{name}-%{version}/libnetwork %{OUR_GOPATH}/src/github.com/docker/libnetwork
mkdir -p '%{OUR_GOPATH}/src/github.com/docker'
ln -sfT %{_topdir}/BUILD/%{name}-%{version} %{OUR_GOPATH}/src/github.com/docker/docker

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache
export GOPROXY=off
export GO111MODULE=off
#export GOFLAGS=-trimpath
export GOGC=off
export VERSION=%{version}

GIT_COMMIT=%{MOBY_GITCOMMIT}
GIT_COMMIT_SHORT=${GIT_COMMIT:0:7}
DOCKER_GITCOMMIT=${GIT_COMMIT_SHORT} DOCKER_BUILDTAGS='apparmor seccomp' hack/make.sh dynbinary

mkdir -p tini/build
cd tini/build
cmake ..
make tini-static

cd ../../
go build \
    -o libnetwork/docker-proxy \
    github.com/docker/libnetwork/cmd/proxy

%install
mkdir -p %{buildroot}/%{_bindir}
cp -aLT ./bundles/dynbinary-daemon/dockerd %{buildroot}/%{_bindir}/dockerd
echo %{_bindir}/dockerd >> files

cp -aT libnetwork/docker-proxy %{buildroot}/%{_bindir}/docker-proxy
echo %{_bindir}/docker-proxy >> ./files

cp -aT tini/build/tini-static %{buildroot}/%{_bindir}/docker-init
echo %{_bindir}/docker-init >> ./files

# install udev rules
mkdir -p %{buildroot}/%{_sysconfdir}/udev/rules.d
install -p -m 644 contrib/udev/80-docker.rules %{buildroot}/%{_sysconfdir}/udev/rules.d/80-docker.rules
echo %config %{_sysconfdir}/udev/rules.d/80-docker.rules >> ./files
# add init scripts
mkdir -p %{buildroot}/%{_unitdir}
install -p -m 644 %{SOURCE2} %{buildroot}/%{_unitdir}/docker.service
install -p -m 644 %{SOURCE3} %{buildroot}/%{_unitdir}/docker.socket
echo %config %{_unitdir}/docker.service >> ./files
echo %config %{_unitdir}/docker.socket >> ./files

# copy legal files
mkdir -p %{buildroot}/usr/share/doc/%{name}-%{version}
cp %{SOURCE4} %{buildroot}/usr/share/doc/%{name}-%{version}/LICENSE
cp %{SOURCE5} %{buildroot}/usr/share/doc/%{name}-%{version}/NOTICE

%post
if ! grep -q "^docker:" /etc/group; then
	groupadd --system docker
fi

%preun
%systemd_preun docker.service

%postun
%systemd_postun_with_restart docker.service

# list files owned by the package here
%files -f ./files
%license LICENSE
/usr/share/doc/%{name}-%{version}/*

%changelog
* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 19.03.15+azure-8
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 19.03.15+azure-7
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 19.03.15+azure-6
- Increment release for force republishing using golang 1.16.12

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 19.03.15+azure-5
- Increment release for force republishing using golang 1.16.9

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
