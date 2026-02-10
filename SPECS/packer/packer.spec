%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Tool for creating identical machine images for multiple platforms from a single source configuration.
Name:           packer
Version:        1.9.5
Release:        12%{?dist}
License:        MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
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
Patch6:         CVE-2025-22869.patch
Patch7:         CVE-2025-22868.patch
Patch8:         CVE-2025-30204.patch
Patch9:         CVE-2025-22870.patch
Patch10:        CVE-2024-51744.patch
Patch11:        CVE-2025-22872.patch
Patch12:        CVE-2025-58058.patch
Patch13:        CVE-2025-47913.patch
Patch14:        CVE-2025-11065.patch

BuildRequires:  golang >= 1.21
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
* Tue Feb 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.9.5-12
- Patch for CVE-2025-11065

* Tue Nov 18 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.9.5-11
- Patch CVE-2025-47913

* Wed Sep 03 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.9.5-10
- Patch for CVE-2025-58058

* Tue Apr 22 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.9.5-9
- Patch CVE-2025-22872

* Tue Apr 15 2025 Sreeniavsulu Malavathula <v-smalavathu@microsoft.com> - 1.9.5-8
- Fix CVE-2025-22870, CVE-2024-51744 with upstream patches

* Sat Mar 29 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.9.5-7
- Patch CVE-2025-30204

* Fri Feb 28 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.9.5-6
- Fix CVE-2024-28180, CVE-2025-27144, CVE-2025-22869, CVE-2025-22868 with an upstream patch

* Thu Jan 09 2025 Sudipta Pandit <sudpandit@microsoft.com> - 1.9.5-5
- Add patch for CVE-2025-21613 and CVE-2025-21614
- Remove patch for CVE-2023-45288, CVE-2023-49569, CVE-2024-45337

* Fri Dec 20 2024 Aurelien Bombo <abombo@microsoft.com> - 1.9.5-4
- Add patch for CVE-2024-45337

* Mon Nov 25 2024 Bala <balakumaran.kannan@microsoft.com> - 1.9.5-3
- Patched CVE-2024-24786

* Mon Aug 05 2024 Bala <balakumaran.kannan@microsoft.com> - 1.9.5-2
- Patched CVE-2024-6104.

* Mon Jul 01 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.5-1
- Bump to version 1.9.5.
- Patched CVE-2022-3064.
- Ported patches from 2.0: CVE-2023-45288 and CVE-2023-49569.

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.4-1
- Auto-upgrade to 1.9.4 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.1-15
- Bump release to rebuild with go 1.20.10

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
