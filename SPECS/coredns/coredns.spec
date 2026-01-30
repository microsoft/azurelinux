%global debug_package %{nil}

# set commit number that corresponds to the github tag for the version
%global coredns_gitcommit "6e11ebddfc13bfca683fcbcae72cc4af6de47dd2"

Summary:        Fast and flexible DNS server
Name:           coredns
Version:        1.11.4
Release:        14%{?dist}
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Libraries
URL:            https://github.com/coredns/coredns
#Source0:       https://github.com/coredns/coredns/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/coredns/coredns/archive/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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
Patch0:         CVE-2025-22868.patch
# Patch to fix the package test suite due to external akamai update
# https://github.com/coredns/coredns/commit/d8ecde1080e7cbbeb98257ba4e03a271f16b4cd9
Patch1:         coredns-example-net-test.patch
Patch2:         CVE-2025-29786.patch
Patch3:         CVE-2025-30204.patch
Patch4:         CVE-2024-53259.patch
Patch5:         CVE-2025-47950.patch
Patch6:         CVE-2025-58063.patch
Patch7:         CVE-2025-59530.patch
Patch8:         CVE-2025-68156.patch
Patch9:         CVE-2025-68151.patch
Patch10:        CVE-2025-11065.patch

BuildRequires:  golang < 1.25

%description
CoreDNS is a fast and flexible DNS server.

%prep
%autosetup -a1 -p1

%build
export BUILDOPTS="-mod=vendor -v"
export GITCOMMIT=%{coredns_gitcommit}

# use go provided by host
go_version_host=`go version | { read _ _ v _; echo ${v#go}; }`
go_version_min=$(cat %{_builddir}/%{name}-%{version}/.go-version)
echo "+++ using go version ${go_version_host} (minimum ${go_version_min})"
echo "${go_version_host}" > %{_builddir}/%{name}-%{version}/.go-version

make

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} %{name}

%check
# From go.test.yml
go install github.com/fatih/faillint@latest && \
(cd request && go test -v -race ./...) && \
(cd core && go test -v -race ./...) && \
(cd coremain && go test -v -race ./...) && \
(cd plugin && go test -v -race ./...) && \
(cd test && go test -v -race ./...) && \
./coredns -version

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}

%changelog
* Fri Jan 30 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.11.4-14
- Patch for CVE-2025-11065

* Thu Jan 15 2026 Aditya Singh <v-aditysingh@microsoft.com> - 1.11.4-13
- Patch for CVE-2025-68151

* Fri Dec 19 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.11.4-12
- Patch for CVE-2025-68156

* Mon Oct 27 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.11.4-11
- Patch for CVE-2025-59530

* Thu Sep 18 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.4-10
- Changed patch order to resolve 'make' race condition.

* Thu Sep 11 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.11.4-9
- Patch for CVE-2025-58063

* Sun Aug 31 2025 Andrew Phelps <anphel@microsoft.com> - 1.11.4-8
- Set BR for golang to < 1.25

* Tue Jun 17 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.11.4-7
- Fix CVE-2025-47950 with an upstream patch

* Tue Apr 01 2025 Ankita Pareek <ankitapareek@microsoft.com> - 1.11.4-6
- Add patch for CVE-2024-53259

* Sat Mar 29 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.11.4-5
- Patch CVE-2025-30204

* Mon Mar 24 2025 Kshitiz Godara <kgodara@microsoft.com> - 1.11.4-4
- Fix CVE-2025-29786 with an upstream patch

* Mon Mar 03 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.11.4-3
- Fix CVE-2025-22868 with an upstream patch

* Mon Feb 17 2025 Sam Meluch <sammeluch@microsoft.com> - 1.11.4-2
- readd check section from 2.0

* Fri Feb 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.4-1
- Auto-upgrade to 1.11.4 to fix CVE-2023-44487

* Mon Nov 25 2024 Bala <balakumaran.kannan@microsoft.com> - 1.11.1-3
- Fix CVE-2024-24786

* Mon Jun 24 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 1.11.1-2
- Address CVE-2023-44487, CVE-2023-45288, CVE-2023-49295, CVE-2024-0874, CVE-2024-22189

* Wed Oct 18 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 1.11.1-1
- Upgrade to 1.11.1 to match version required by kubernetes

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-10
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.9.3-9
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-8
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-7
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-6
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-5
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-4
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-3
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-2
- Bump release to rebuild with go 1.19.5

* Thu Jan 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-1
- Auto-upgrade to 1.9.3 - version required by Kubernetes

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.6-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.8.6-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.6-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.6-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.8.6-2
- Bump release to rebuild with golang 1.18.3

* Fri Apr 22 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.8.6-1
- Update to version  "1.8.6".
- Remove clean section
- License verified

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.8.4-4
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 1.8.4-3
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 1.8.4-2
- Increment release for force republishing using golang 1.16.12

* Tue Dec 28 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.8.4-1
- Update to version  "1.8.4".

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.8.0-2
- Increment release for force republishing using golang 1.16.9

* Fri Aug 20 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.8.0-1
- Update to version  "1.8.0".

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.7.0-3
- Increment release to force republishing using golang 1.15.13.
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.7.0-2
- Increment release to force republishing using golang 1.15.11.
* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.7.0-1
- Original version for CBL-Mariner.
