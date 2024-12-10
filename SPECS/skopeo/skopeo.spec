Summary:        Inspect container images and repositories on registries
Name:           skopeo
Version:        1.14.2
Release:        9%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/containers/skopeo
Source0:        https://github.com/containers/skopeo/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2023-45288.patch
Patch1:         CVE-2024-3727.patch
Patch2:         CVE-2024-6104.patch
Patch3:         CVE-2024-9676.patch
Patch4:         CVE-2024-28180.patch
Patch5:         CVE-2024-24786.patch
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
BuildRequires:  btrfs-progs-devel
BuildRequires:  device-mapper-devel
BuildRequires:  go-md2man
BuildRequires:  golang
BuildRequires:  gpgme-devel
BuildRequires:  libassuan-devel
BuildRequires:  pkgconfig
Requires:       libcontainers-common

%description
Command line utility to inspect images and repositories directly on Docker
registries without the need to pull them.

%prep
%autosetup -p1

%build
export GOPATH=%{our_gopath}
make

%install
make PREFIX=%{buildroot}%{_prefix} install-binary install-docs

%check
make test-unit-local
./bin/skopeo --version

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%%{name}*

%changelog
* Mon Nov 11 2024 Rohit Rawat <rohitrawat@microsoft.com> - 1.14.2-9
- Fix CVE-2024-9676, CVE-2024-28180 and CVE-2024-24786

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.14.2-8
- Bump release to rebuild with go 1.22.7

* Wed Jul 17 2024 Sindhu Karri <lakarri@microsoft.com> - 1.14.2-7
- Fix CVE-2024-6104 in github.com/hashicorp/go-retryablehttp

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 1.14.2-6
- Drop requirement on a specific version of golang

* Wed Jun 26 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.14.2-5
- Bump release to rebuild with go 1.21.11

* Thu Jun 20 2024 Rohit Rawat <rohitrawat@microsoft.com> - 1.14.2-4
- Fix CVE-2024-3727 in github.com/containers/image

* Thu Apr 18 2024 Chris Gunn <chrisgun@microsoft.com> - 1.14.2-3
- Fix for CVE-2023-45288

* Tue Feb 13 2024 David Steele <davidsteele@microsoft.com> - 1.14.2-2
- Bump version to 1.14.2 to address Docker Daemon version issue.

* Fri Feb 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.14.1-2
- Bump release to rebuild with go 1.21.6

* Fri Jan 19 2024 Muhammad Falak <mwani@microsoft.com> - 1.14.1-1
- Bump version to 1.14.1 to address https://github.com/advisories/GHSA-jq35-85cj-fj4p

* Tue Oct 17 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.3-1
- Update to v1.13.3 to fix CVE-2023-33199 in rekor.

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.12.0-5
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.12.0-4
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.12.0-3
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.12.0-2
- Bump release to rebuild with go 1.19.11

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.12.0-1
- Bump skopeo version to 1.12.0 - upgrade to latest

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-5
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-4
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-3
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-2
- Bump release to rebuild with go 1.19.6

* Wed Feb 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-1
- Auto-upgrade to 1.11.0 - upgrade to latest

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.9.1-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.1-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.1-2
- Bump release to rebuild against Go 1.18.5

* Tue Jul 26 2022 Tom Fay <tomfay@microsoft.com> - 1.9.1-1
- Original version for CBL-Mariner.
- License verified.
