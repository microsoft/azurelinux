%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Tool for creating identical machine images for multiple platforms from a single source configuration.
Name:           packer
Epoch:          1
Version:        1.9.5
Release:        17%{?dist}
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
#   4. Apply all patches affecting "go.mod" and "go.sum" files. Example: CVE-2025-21613.patch.
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
Source1:        %{name}-%{version}-vendor-v2.tar.gz
Patch0:         CVE-2022-3064.patch
Patch1:         CVE-2024-6104.patch
Patch2:         CVE-2024-24786.patch
Patch3:         CVE-2025-21613.patch
Patch4:         CVE-2024-28180.patch
Patch5:         CVE-2025-27144.patch
Patch6:         CVE-2025-22868.patch
Patch7:         CVE-2025-22869.patch
Patch8:         CVE-2025-22870.patch
Patch9:         CVE-2024-51744.patch
Patch10:        CVE-2025-30204.patch
Patch11:        CVE-2025-22872.patch
Patch12:        CVE-2025-58058.patch
Patch13:        CVE-2025-47913.patch
Patch14:        CVE-2025-11065.patch
BuildRequires:  golang
BuildRequires:  kernel-headers
BuildRequires:  glibc-devel

%description
Packer is a tool for building identical machine images for multiple platforms from a single source configuration.

%prep
%autosetup -p1 -a1

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
* Tue Feb 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.9.5-17
- Patch for CVE-2025-11065

* Tue Nov 18 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.9.5-16
- Patch for CVE-2025-47913

* Wed Sep 03 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.9.5-15
- Patch for CVE-2025-58058

* Tue Sep 02 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.9.5-14
- Bump release to rebuild with golang

* Tue Apr 22 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.9.5-13
- Patch CVE-2025-22872

* Sat Mar 29 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.9.5-12
- Patch CVE-2025-30204
- Fix previous changelog

* Fri Mar 14 2025 Sreeniavsulu Malavathula <v-smalavathu@microsoft.com> - 1.9.5-11
- Patch to fix CVE-2025-22870, CVE-2024-51744 with an upstream patch

* Sun Mar 02 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.9.5-10
- Fix CVE-2025-22868, CVE-2025-22869 with an upstream patch

* Fri Feb 28 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.9.5-9
- Fix CVE-2025-27144 with an upstream patch

* Fri Jan 31 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.9.5-8
- Fix CVE-2024-28180 with an upstream patch

* Mon Jan 13 2025 Sudipta Pandit <sudpandit@microsoft.com> - 1.9.5-7
- Add patch for CVE-2025-21613 and CVE-2025-21614
- Remove patch for CVE-2023-45288, CVE-2023-49569, CVE-2024-45337, CVE-2024-45338

* Thu Jan 02 2025 Sumedh Sharma <sumsharma@microsoft.com> - 1.9.5-6
- Add patch for CVE-2024-45338.

* Tue Dec 17 2024 Andrew Phelps <anphel@microsoft.com> - 1.9.5-5
- Add patch for CVE-2024-45337

* Mon Dec 09 2024 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 1.9.5-4
- Patch for CVE-2024-24786

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.5-3
- Bump release to rebuild with go 1.22.7

* Thu Aug 01 2024 Bala <balakumaran.kannan@microsoft.com> - 1:1.9.5-2
- Patch for CVE-2024-6104

* Mon Jul 01 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:1.9.5-1
- Revert to version 1.9.5.
- Added patches for CVE-2022-3064 and CVE-2023-49569.

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 1.10.1-4
- Drop requirement on a specific version of golang

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
