Summary:        The official command line client for Cloud Foundry.
Name:           cf-cli
Version:        8.4.0
Release:        15%{?dist}
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

# patches for vendored code >= 1000
Patch1000: CVE-2021-44716.patch

BuildRequires:  golang >= 1.18.3
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
The official command line client for Cloud Foundry.

%prep
%autosetup -N -n cli-%{version}

# Apply vendor before patching
tar --no-same-owner -xf %{SOURCE1}

%autopatch -p1

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
%license LICENSE
%doc NOTICE README.md
%{_bindir}/cf

%changelog
* Tue Feb 5 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 20.10.27-3
- Patch CVE-2021-44716

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
