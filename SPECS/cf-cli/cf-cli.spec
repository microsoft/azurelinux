# NOTE(mfrw): Modify the CF_BUILD_SHA by running: `git rev-parse --short HEAD` on the release
%global cf_build_sha b1b4068ff

Summary:        The official command line client for Cloud Foundry.
Name:           cf-cli
# Note: Upgrading the package also warrants an upgrade in the CF_BUILD_SHA
Version:        8.7.11
Release:        5%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Tools
URL:            https://github.com/cloudfoundry/cli
Source0:        https://github.com/cloudfoundry/cli/archive/refs/tags/v%{version}.tar.gz#/cli-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/cloudfoundry/cli/archive/refs/tags/v%%{version}.tar.gz -O cli-%%{version}.tar.gz
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

Patch0:         CVE-2024-45337.patch
Patch1:         CVE-2024-45338.patch
Patch2:         CVE-2025-22869.patch
Patch3:         CVE-2025-22872.patch
Patch4:         CVE-2025-47911.patch
Patch5:         CVE-2025-58190.patch

BuildRequires:  golang < 1.25
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
The official command line client for Cloud Foundry.

%prep
%autosetup -p1 -n cli-%{version} -a1

%build
export GOPATH=%{our_gopath}
# No mod download use vendor cache locally
sed -i 's/GOFLAGS := -mod=mod/GOFLAGS := -mod=vendor/' ./Makefile
make build CF_BUILD_SHA=%{cf_build_sha}

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
* Thu Feb 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 8.7.11-5
- Patch for CVE-2025-47911, CVE-2025-58190

* Sun Aug 31 2025 Andrew Phelps <anphel@microsoft.com> - 8.7.11-4
- Set BR for golang to < 1.25

* Tue Apr 22 2025 Archana Shettigar <v-shettigara@microsoft.com> - 8.7.11-3
- Fix CVE-2025-22872 with an upstream patch

* Mon Mar 03 2025 Kanishk Bansal <kanbansal@microsoft.com> - 8.7.11-2
- Fix CVE-2025-22869 with an upstream patch

* Wed Feb 26 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.7.11-1
- Auto-upgrade to 8.7.11 - address CVE-2023-44487

* Fri Feb 14 2025 Kanishk Bansal <kanbansal@microsoft.com> - 8.7.3-6
- Address CVE-2023-45288

* Tue Dec 31 2024 Rohit Rawat <rohitrawat@microsoft.com> - 8.7.3-5
- Add patch for CVE-2024-45338

* Fri Dec 20 2024 Aurelien Bombo <abombo@microsoft.com> - 8.7.3-4
- Add patch for CVE-2024-45337

* Mon Nov 25 2024 Bala <balakumaran.kannan@microsoft.com> - 8.7.3-3
- Fix CVE-2024-24786

* Mon Jul 29 2024 Muhammad Falak <mwani@microsoft.com> - 8.7.3-2
- Fix CF_BUILD_SHA to have correct build sha in the binary
- Move Source1 un-taring in prep section
- Address CVE-2023-39325

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.7.3-1
- Auto-upgrade to 8.7.3 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.4.0-14
- Bump release to rebuild with go 1.20.10

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
