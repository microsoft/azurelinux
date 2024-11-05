%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Simple and easy way to configure a layer 3 network fabric designed for Kubernetes
Name:           flannel
Version:        0.14.0
Release:        25%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/flannel-io/flannel
#Source0:       https://github.com/flannel-io/flannel/archive/refs/tags/v0.14.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         CVE-2021-44716.patch

BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  glibc-static >= 2.35-7%{?dist}
BuildRequires:  golang
BuildRequires:  kernel-headers

%description
Flannel is a simple and easy way to configure a layer 3 network fabric designed for Kubernetes.

%prep
%autosetup -p1

%build
export GOPATH=%{our_gopath}
export TAG=v%{version}
%ifarch x86_64
export ARCH=amd64
%endif
%ifarch aarch64
export ARCH=arm64
%endif
export CGO_ENABLED=1

make dist/flanneld

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./dist/flanneld

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/flanneld

%changelog
* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-25
- Bump release to rebuild with go 1.22.7

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 0.14.0-24
- Drop requirement on a specific version of golang

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-23
- Bump release to rebuild with go 1.21.11

* Mon May 06 2024 Rachel Menge <rachelmenge@microsoft.com> - 0.10.0-22
- Bump release to rebuild against glibc 2.35-7

* Mon Feb 05 2024 Osama Esmail <osamaesmail@microsoft.com> - 0.14.0-21
- Patching CVE-2021-44716

* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> - 0.14.0-20
- Bump release to rebuild against glibc 2.35-6

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-19
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.14.0-18
- Bump release to rebuild with updated version of Go.

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.14.0-17
- Bump release to rebuild against glibc 2.35-5

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-16
- Bump release to rebuild with go 1.19.12

* Wed Jul 14 2023 Andrew Phelps <anphel@microsoft.com> - 0.14.0-15
- Bump release to rebuild against glibc 2.35-4

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-14
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-13
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-12
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-11
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-10
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-9
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-8
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.14.0-7
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.14.0-6
- Bump release to rebuild with go 1.18.8

* Wed Oct 05 2022 Andy Caldwell <andycaldwell@microsoft.com> - 0.14.0-5
- Bump release to rebuild against glibc 2.35-3

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.14.0-4
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 0.14.0-3
- Bump release to rebuild with golang 1.18.3

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.0-2
- Removing the explicit %%clean stage.
- License verified.

* Thu Sep 16 2021 Andrew Phelps <anphel@microsoft.com> 0.14.0-1
- Update to version 0.14.0
* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 0.12.0-3
- Increment release to force republishing using golang 1.15.13.
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 0.12.0-2
- Increment release to force republishing using golang 1.15.11.
* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 0.12.0-1
- Original version for CBL-Mariner.
