Summary:        Tool for creating identical machine images for multiple platforms from a single source configuration.
Name:           packer
Version:        1.8.7
Release:        1%{?dist}
License:        MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/hashicorp/packer
Source0:        https://github.com/hashicorp/packer/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/hashicorp/packer/archive/v%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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

BuildRequires:  golang >= 1.17.1
BuildRequires:  kernel-headers
BuildRequires:  glibc-devel
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
Packer is a tool for building identical machine images for multiple platforms from a single source configuration.

%prep
%autosetup -p1

%build
tar --no-same-owner -xf %{SOURCE1}
export GOPATH=%{our_gopath}
LD_FLAGS="-X github.com/hashicorp/packer/version.Version=%{version} -X github.com/hashicorp/packer/version.VersionPrerelease="
go build -mod=vendor -v -a -o packer --ldflags="$LD_FLAGS"

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
