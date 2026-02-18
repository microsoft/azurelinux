Summary:        Command line tool for working with Jenkins X.
Name:           jx
Version:        3.2.236
Release:        25%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/jenkins-x/jx
Source0:        https://github.com/jenkins-x/jx/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/jenkins-x/jx/archive/v%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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
Patch1:         CVE-2021-44716.patch
Patch2:         CVE-2023-45288.patch
Patch3:         CVE-2024-51744.patch
Patch4:         CVE-2025-58058.patch
Patch5:         CVE-2025-65637.patch
Patch6:         CVE-2025-30204.patch
BuildRequires:  golang
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
Command line tool for working with Jenkins X.

%prep
%autosetup -p1 -a1

%build
export GOPATH=%{our_gopath}
# No download use vednor cache locally
sed -i 's/go mod download/# go mod download/' ./Makefile
sed -i 's/CGO_ENABLED=$(CGO_ENABLED) $(GO) $(BUILD_TARGET)/CGO_ENABLED=$(CGO_ENABLED) $(GO) $(BUILD_TARGET) -mod=vendor/' ./Makefile
make build

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./build/jx

%check
# jenkins is not available for aarch64, can only run unit tests for x86_64.
%ifarch x86_64
sed -i 's/TEST_BUILDFLAGS :=  -ldflags "$(BUILD_TIME_CONFIG_FLAGS)"/TEST_BUILDFLAGS :=  -mod=vendor -ldflags "$(BUILD_TIME_CONFIG_FLAGS)"/' ./Makefile
make test && \
./build/jx --help
%else
./build/jx --help
%endif

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/jx

%changelog
* Tue Feb 17 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.2.236-25
- Patch for CVE-2025-30204

* Mon Dec 08 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.2.236-24
- Patch for CVE-2025-65637

* Wed Sep 03 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.2.236-23
- Patch for CVE-2025-58058

* Tue Sep 02 2025 Akhila Guruju <v-guakhila@microsoft.com> - 3.2.236-22
- Bump release to rebuild with golang

* Thu Mar 20 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 3.2.236-21
- Fix CVE-2024-51744

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-20
- Bump release to rebuild with go 1.22.7

* Thu Aug 22 2024 Sumedh Sharma <sumsharma@microsoft.com> - 3.2.236-19
- Add patch to resolve CVE-2023-45288

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 3.2.236-18
- Drop requirement on a specific version of golang

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-17
- Bump release to rebuild with go 1.21.11

* Mon Feb 05 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 3.2.236-16
- Patch CVE-2021-44716

* Thu Feb 01 2024 Daniel McIlvaney <damcilva@microsoft.com> -3.2.236-15
- Address CVE-2023-44487 by patching vendored golang.org/x/net
- Add unit tests to check section

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-14
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 3.2.236-13
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-12
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-11
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-10
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-9
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-8
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-7
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.236-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.2.236-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.2.236-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.2.236-2
- Bump release to rebuild against Go 1.18.5

* Wed Jun 22 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 3.2.236-1
- Original version for CBL-Mariner.
- License verified.
