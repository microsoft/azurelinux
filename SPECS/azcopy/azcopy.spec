Summary:        The new Azure Storage data transfer utility - AzCopy v10
Name:           azcopy
Version:        10.22.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/Azure/azure-storage-azcopy
Source0:        https://github.com/Azure/azure-storage-azcopy/archive/refs/tags/v%{version}.tar.gz#/azure-storage-%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/Azure/azure-storage-azcopy/archive/refs/tags/v%{version}.tar.gz -O azure-storage-%{name}-%{version}.tar.gz
#   2. tar -xf azure-storage-%{name}-%{version}.tar.gz
#   3. cd azure-storage-%{name}-%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf azure-storage-%{name}-%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        azure-storage-%{name}-%{version}-vendor.tar.gz

BuildRequires:  golang >= 1.17.9
BuildRequires:  git
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
AzCopy v10 is a command-line utility that you can use to copy data to
and from containers and file shares in Azure Storage accounts.
AzCopy V10 presents easy-to-use commands that are optimized for high
performance and throughput.

%prep
%setup -q -n azure-storage-%{name}-%{version}

%build
tar --no-same-owner -xf %{SOURCE1}
export GOPATH=%{our_gopath}
go build -buildmode=pie -mod=vendor

%install
install -D -m 0755 ./azure-storage-azcopy %{buildroot}%{_bindir}/azcopy

%check
go test -mod=vendor
./azure-storage-azcopy --version

%files
%defattr(-,root,root)
%license LICENSE
%doc NOTICE.txt README.md
%{_bindir}/azcopy

%changelog
* Thu Jan 04 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.22.1-1
- Auto-upgrade to 10.22.1 - 3.0 upgrade

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-14
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 10.15.0-13
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-12
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-11
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-10
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-9
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-8
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-7
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.15.0-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 10.15.0-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 10.15.0-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 10.15.0-2
- Bump release to rebuild against Go 1.18.5

* Fri Jul 01 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 10.15.0-1
- Original version for CBL-Mariner.
- License verified.
