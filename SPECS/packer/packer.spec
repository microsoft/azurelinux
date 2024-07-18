%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Tool for creating identical machine images for multiple platforms from a single source configuration.
Name:           packer
Epoch:          1
Version:        1.9.5
Release:        2%{?dist}
License:        MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/hashicorp/packer
Source0:        https://github.com/hashicorp/packer/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/hashicorp/packer/archive/v%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. Apply all patches affecting "go.mod" and "go.sum" files. Example: CVE-2023-49569.patch.
#   5. go mod vendor
#   6. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         CVE-2023-45288.patch
Patch1:         CVE-2022-3064.patch
Patch2:         CVE-2023-49569.patch
BuildRequires:  golang >= 1.17.1
BuildRequires:  kernel-headers
BuildRequires:  glibc-devel

%description
Packer is a tool for building identical machine images for multiple platforms from a single source configuration.

%prep
%autosetup -N
# Apply vendor before patching
tar --no-same-owner -xf %{SOURCE1}
%autopatch -p1

%build
export GOPATH=%{our_gopath}
LD_FLAGS="-X github.com/hashicorp/packer/version.Version=%{version} -X github.com/hashicorp/packer/version.VersionPrerelease="
go build -mod=vendor -v -a -o packer -ldflags="$LD_FLAGS"

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./packer/packer

%check
go test -mod=vendor
./packer/packer -help

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/packer

%changelog
* Mon July 8 2024 Bhagyashri Pathak <bhapathak@microsoft.com> - 1.9.5-2
- Bump release to rebuild with go 1.22.4

* Mon Jul 01 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:1.9.5-1
- Revert to version 1.9.5.
- Added patches for CVE-2022-3064 and CVE-2023-49569.

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.10.1-3
- Bump release to rebuild with go 1.21.11

* Thu Apr 18 2024 Chris Gunn <chrisgun@microsoft.com> - 1.10.1-2
- Fix for CVE-2023-45288

* Wed Apr 10 2024 Sumedh Sharma <sumsharma@microsoft.com> - 1.10.1-1
- Bump version to address CVE-2023-49569

* Fri Feb 02 2024 Daniel McIlvaney <damcilva@microsoft.com> - 1.8.7-2
- Address CVE-2023-44487 by patching vendored golang.org/x/net

* Wed Dec 20 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-1
- Auto-upgrade to 1.8.7 - CVE-2023-45286

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-15
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.8.1-14
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.8.1-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.1-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.1-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.8.1-2
- Bump release to rebuild with golang 1.18.3

* Tue Jun 07 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.8.1-1
- Original version for CBL-Mariner.
- License verified.
