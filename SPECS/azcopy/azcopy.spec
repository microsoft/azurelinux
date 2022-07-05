Summary:        The new Azure Storage data transfer utility - AzCopy v10
Name:           azcopy
Version:        10.15.0
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
* Fri Jul 01 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 10.15.0-1
- Original version for CBL-Mariner.
- License verified.
