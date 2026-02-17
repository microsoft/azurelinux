%define debug_package %{nil}
%ifarch aarch64
%global gohostarch      arm64
%elifarch x86_64
%global gohostarch      amd64
%endif
Summary:        CRI tools
Name:           cri-tools
Version:        1.29.0
Release:        9%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/kubernetes-sigs/cri-tools
Source0:        https://github.com/kubernetes-sigs/cri-tools/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2024-21626.patch
Patch1:         CVE-2023-45288.patch
Patch2:         CVE-2024-24786.patch
Patch3:         CVE-2024-45338.patch
Patch4:         CVE-2025-22872.patch
Patch5:         CVE-2025-47911.patch
Patch6:         CVE-2025-58190.patch
BuildRequires:  glib-devel
BuildRequires:  glibc-devel
BuildRequires:  golang

%description
cri-tools aims to provide a series of debugging and validation tools for Kubelet CRI, which includes:
crictl: CLI for kubelet CRI.
critest: validation test suites for kubelet CRI.

%prep
%autosetup -p1

%build
export VERSION="%{version}"
%make_build

%install
export BUILD_FOLDER="./build/bin/linux/%{gohostarch}"
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} "${BUILD_FOLDER}/crictl"
install -p -m 755 -t %{buildroot}%{_bindir} "${BUILD_FOLDER}/critest"

%files
%license LICENSE
%doc CHANGELOG.md CONTRIBUTING.md OWNERS README.md code-of-conduct.md
%doc docs/validation.md docs/roadmap.md docs/crictl.md
%{_bindir}/crictl
%{_bindir}/critest

%changelog
* Thu Feb 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.29.0-9
- Patch for CVE-2025-58190, CVE-2025-47911

* Thu Sep 04 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.29.0-8
- Bump release to rebuild with golang

* Thu May 22 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.29.0-7
- Patch CVE-2025-22872

* Mon Jan 06 2025 Sumedh Sharma <sumsharma@microsoft.com> - 1.29.0-6
- Add patch for CVE-2024-45338

* Wed Dec 04 2024 Suresh Thelkar <sthelkar@microsoft.com> - 1.29.0-5
- Patch CVE-2024-24786

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.29.0-4
- Bump release to rebuild with go 1.22.7

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.29.0-3
- Bump release to rebuild with go 1.21.11

* Thu Apr 18 2024 Chris Gunn <chrisgun@microsoft.com> - 1.29.0-2
- Fix for CVE-2023-45288

* Mon Apr 29 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.29.0-1
- Auto-upgrade to 1.29.0 - CVE-2023-45142

* Thu Feb 15 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.28.0-5
- Bump release to rebuild with go 1.21.6

* Wed Feb 14 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.28.0-4
- Patch runc for CVE-2024-21626

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.28.0-3
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.28.0-2
- Bump release to rebuild with updated version of Go.

* Wed Sep 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.28.0-1
- Auto-upgrade to 1.28.0 to fix vendored vulns CVE-2021-38561, CVE-2021-44716,
  CVE-2022-32149, CVE-2022-27664, CVE-2022-29526, CVE-2022-28948
- Use SPDX license expression in license tag
- Use %%doc macro to install docs
- Remove obsolete patch to remove git usage in makefile

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.23.0-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.0-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.0-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.23.0-2
- Bump release to rebuild with golang 1.18.3

* Tue Feb 08 2022 Henry Li <lihl@microsoft.com> - 1.23.0-1
- Update to version 1.23.0

*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.22.0-2
-   Removing the explicit %%clean stage.

*   Thu Sep 16 2021 Andrew Phelps <anphel@microsoft.com> 1.22.0-1
-   Update version to 1.22.0

*   Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.11.1-8
-   Increment release to force republishing using golang 1.15.13.

*   Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.11.1-7
-   Increment release to force republishing using golang 1.15.11.

*   Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.11.1-6
-   Increment release to force republishing using golang 1.15.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.11.1-5
-   Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 1.11.1-4
-   Renaming go to golang

*   Thu Apr 09 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.11.1-3
-   Fixed "Source0" and "URL" tags.
-   License verified.
-   Removed "%%define sha1".

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.11.1-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Jul 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.1-1
-   Initial build added for Photon.
