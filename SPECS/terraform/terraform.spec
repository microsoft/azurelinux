Summary:        Infrastructure as code deployment management tool
Name:           terraform
Version:        1.3.2
Release:        28%{?dist}
License:        MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://www.terraform.io/
Source0:        https://github.com/hashicorp/terraform/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/hashicorp/terraform/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
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
Patch0:         CVE-2023-44487.patch
Patch1:         CVE-2024-3817.patch
Patch2:         CVE-2024-6257.patch
Patch3:         CVE-2024-6104.patch
Patch4:         CVE-2022-32149.patch
Patch5:         CVE-2023-4782.patch
Patch6:         CVE-2024-24786.patch
Patch7:         CVE-2024-45338.patch
Patch8:         CVE-2023-0475.patch
Patch9:         CVE-2025-22869.patch
Patch10:        CVE-2025-30204.patch
Patch11:        CVE-2023-48795.patch
Patch12:        CVE-2025-58058.patch
Patch13:        CVE-2025-11065.patch

%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
BuildRequires:  golang

%description
Terraform is an infrastructure as code deployment management tool

%prep
%autosetup -p1 -n %{name}-%{version} -a1

%build
export GOPATH=%{our_gopath}
go build -mod=vendor -v -a -o terraform

%check
go test -mod=vendor
./terraform -help

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./terraform

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/terraform

%changelog
* Wed Feb 04 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.3.2-28
- Patch for CVE-2025-11065

* Wed Sep 03 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.3.2-27
- Patch for CVE-2025-58058

* Thu Sep 04 2025 Akhila Guruju <v-guakhila@microsoft.com> - 1.3.2-26
- Bump release to rebuild with golang

* Fri Apr 04 2025 Sumedh Sharma <sumsharma@microsoft.com> - 1.3.2-25
- Add patch to resolve CVE-2023-48795

* Sat Mar 29 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.3.2-24
- Patch CVE-2025-30204

* Mon Mar 10 2025 Sudipta Pandit <sudpandit@microsoft.com> - 1.3.2-23
- Add patch for CVE-2025-22869

* Tue Jan 21 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 1.3.2-22
- Add Patch for CVE-2023-0475

* Mon Jan 06 2025 Sumedh Sharma <sumsharma@microsoft.com> - 1.3.2-21
- Add patch for CVE-2024-45338

* Wed Dec 04 2024 bhapathak <bhapathak@microsoft.com> - 1.3.2-20
- Patch CVE-2024-24786

* Thu Oct 10 2024 Sumedh Sharma <sumsharma@microsoft.com> - 1.3.2-19
- Add patch to resolve CVE-2023-4782 & CVE-2022-32149

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-18
- Bump release to rebuild with go 1.22.7

* Thu Jul 25 2024 Sumedh Sharma <sumsharma@microsoft.com> - 1.3.2-17
- Patch CVE-2024-6257 in vendored hashicorp/go-getter

* Mon Jul 29 2024 Sumedh Sharma <sumsharma@microsoft.com> - 1.3.2-16
- Patch CVE-2024-6104

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-15
- Bump release to rebuild with go 1.21.11

* Mon Apr 22 2024 Daniel McIlvaney <damcilva@microsoft.com> - 1.3.2-14
- Patch CVE-2024-3817 in vendored hashicorp/go-getter

* Thu Feb 01 2024 Daniel McIlvaney <damcilva@microsoft.com> - 1.3.2-13
- Address CVE-2023-44487 by patching vendored golang.org/x/net

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-12
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.3.2-11
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-10
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-9
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-8
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-7
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-6
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-5
- Bump release to rebuild with go 1.19.6

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-4
- Set golang <= 1.18.8 build requires

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.3.2-3
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.3.2-2
- Bump release to rebuild with go 1.18.8

* Mon Oct 10 2022 Henry Li <lihl@microsoft.com> - 1.3.2-1
- Upgrade to version 1.3.2 to resolve CVE-2021-36230

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.2.2-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.2.2-2
- Bump release to rebuild with golang 1.18.3

* Tue Jun 07 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.2.2-1
- Upgrade version to 1.2.2.

* Tue Mar 29 2022 Andrew Phelps <anphel@microsoft.com> - 1.1.7-2
- Build with golang >= 1.17.1

* Wed Mar 23 2022 Matthew Torr <matthewtorr@microsoft.com> - 1.1.7-1
- Original version for CBL-Mariner.
- License verified.
