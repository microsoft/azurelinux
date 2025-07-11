%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
Summary:        Simple and easy way to configure a layer 3 network fabric designed for Kubernetes
Name:           flannel
Version:        0.24.2
Release:        15%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Libraries
URL:            https://github.com/flannel-io/flannel
Source0:        https://github.com/flannel-io/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         CVE-2024-24786.patch
Patch1:         CVE-2023-44487.patch
Patch2:         CVE-2023-45288.patch
Patch3:         CVE-2025-30204.patch
Patch4:         CVE-2024-51744.patch
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  glibc-static >= 2.38-11%{?dist}
BuildRequires:  golang >= 1.20
BuildRequires:  kernel-headers

%description
Flannel is a simple and easy way to configure a layer 3 network fabric designed for Kubernetes.

%prep
%autosetup -p1 -a 1

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
%doc README.md CONTRIBUTING.md DCO
%license LICENSE
%{_bindir}/flanneld

%changelog
* Thu May 22 2025 Kanishk Bansal <kanbansal@microsoft.com> - 0.24.2-15
- Bump to rebuild with updated glibc

* Mon May 12 2025 Andrew Phelps <anphel@microsoft.com> - 0.24.2-14
- Bump to rebuild with updated glibc

* Wed Mar 31 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 0.24.2-13
- patch for CVE-2024-51744

* Sun Mar 30 2025 Kanishk Bansal <kanbansal@microsoft.com> - 0.24.2-12
- Patch CVE-2025-30204

* Tue Feb 25 2025 Chris Co <chrco@microsoft.com> - 0.24.2-11
- Bump to rebuild with updated glibc

* Fri Feb 14 2025 Kanishk Bansal <kanbansal@microsoft.com> - 0.24.2-10
- Patch CVE-2023-45288

* Wed Feb 05 2025 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 0.24.2-9
- Patch CVE-2023-44487

* Fri Dec 06 2024 sthelkar <sthelkar@microsoft.com> - 0.24.2-8
- Patch CVE-2024-24786

* Mon Aug 26 2024 Rachel Menge <rachelmenge@microsoft.com> - 0.24.2-7
- Update to build dep latest glibc-static version

* Wed Aug 21 2024 Chris Co <chrco@microsoft.com> - 0.24.2-6
- Bump to rebuild with updated glibc

* Wed May 22 2024 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.24.2-5
- update to build dep latest glibc-static version

* Mon May 13 2024 Chris Co <chrco@microsoft.com> - 0.24.2-4
- Update to build dep latest glibc-static version

* Mon Mar 11 2024 Dan Streetman <ddstreet@microsoft.com> - 0.24.2-3
- update to build dep latest glibc-static version

* Tue Feb 27 2024 Dan Streetman <ddstreet@microsoft.com> - 0.24.2-2
- updated glibc-static buildrequires release

* Tue Feb 20 2024 Sumedh Sharma <sumsharma@microsoft.com> - 0.24.2-1
- Upgrade to version 0.24.2

* Tue Nov 07 2023 Andrew Phelps <anphel@microsoft.com> - 0.14.0-21
- Bump release to rebuild against glibc 2.38-1

* Wed Oct 18 2023 Minghe Ren <mingheren@microsoft.com> - 0.14.0-20
- Bump release to rebuild against glibc 2.35-6

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-19
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.14.0-18
- Bump release to rebuild with updated version of Go.

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.14.0-17
- Bump release to rebuild against glibc 2.35-5

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-16
- Bump release to rebuild with go 1.19.12

* Fri Jul 14 2023 Andrew Phelps <anphel@microsoft.com> - 0.14.0-15
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
