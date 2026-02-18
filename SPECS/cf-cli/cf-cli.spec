Summary:        The official command line client for Cloud Foundry.
Name:           cf-cli
Version:        8.4.0
Release:        27%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/cloudfoundry/cli
Source0:        https://github.com/cloudfoundry/cli/archive/refs/tags/v%{version}.tar.gz#/cli-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/cloudfoundry/cli/archive/refs/tags/v%{version}.tar.gz -O cli-%%{version}.tar.gz
#   2. tar -xf cli-%%{version}.tar.gz
#   3. cd cli-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf cli-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        cli-%{version}-vendor.tar.gz
Patch0:         CVE-2023-44487.patch
Patch1:         CVE-2021-44716.patch
Patch2:         CVE-2021-43565.patch
# Produced by git clone https://github.com/golang/text && cd text && 
# git checkout 434eadcdbc3b0256971992e8c70027278364c72c && git format-patch -1 HEAD
Patch3:         CVE-2022-32149.patch
Patch4:         CVE-2024-24786.patch
Patch5:         CVE-2024-45338.patch
Patch6:         CVE-2024-51744.patch
Patch7:         CVE-2025-65637.patch
Patch8:         CVE-2025-30204.patch
Patch9:         CVE-2025-47911.patch

BuildRequires:  golang
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
The official command line client for Cloud Foundry.

%prep
%autosetup -p1 -n cli-%{version} -a1

%build
export GOPATH=%{our_gopath}
# No mod download use vednor cache locally
sed -i 's/GOFLAGS := -mod=mod/GOFLAGS := -mod=vendor/' ./Makefile
make build

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./out/cf

%check
./out/cf --version

%files
%defattr(-,root,root)
%license LICENSE NOTICE
%doc README.md
%{_bindir}/cf

%changelog
* Wed Feb 18 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 8.4.0-27
- Patch for CVE-2025-47911, CVE-2025-30204

* Mon Dec 08 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 8.4.0-26
- Patch for CVE-2025-65637

* Thu Sep 04 2025 Akhila Guruju <v-guakhila@microsoft.com> - 8.4.0-25
- Bump release to rebuild with golang

* Tue Mar 25 2025 Archana Shettigar <v-shettigara@microsoft.com> - 8.4.0-24
- Add patch for CVE-2024-51744

* Fri Jan 03 2025 Sumedh Sharma <sumsharma@microsoft.com> - 8.4.0-23
- Add patch for CVE-2024-45338

* Wed Dec 04 2024 bhapathak <bhapathak@microsoft.com> - 8.4.0-22
- Patch CVE-2024-24786

* Tue Sep 17 2024 Jiri Appl <jiria@microsoft.com> - 8.4.0-21
- Patch CVE-2022-32149 bringing upstream patch over the vendored golang.org/x/text module

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-20
- Bump release to rebuild with go 1.22.7

* Mon Jul 22 2024 Archana Choudhary <archana1@microsoft.com> - 8.4.0-19.cm2
- Patch CVE-2021-43565

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 8.4.0-18
- Drop requirement on a specific version of golang


* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-17
- Bump release to rebuild with go 1.21.11

* Mon Feb 05 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 8.4.0-16
- Patch CVE-2021-44716

* Thu Feb 01 2024 Daniel McIlvaney <damcilva@microsoft.com> - 8.4.0-15
- Address CVE-2023-44487 by patching vendored golang.org/x/net

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-14
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 8.4.0-13
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-12
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-11
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-10
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-9
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-8
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-7
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 8.4.0-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 8.4.0-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 8.4.0-2
- Bump release to rebuild against Go 1.18.5

* Fri Jun 24 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.4.0-1
- Original version for CBL-Mariner.
- License verified.
