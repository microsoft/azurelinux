Summary:        FUSE adapter - Azure Storage
Name:           blobfuse2
Version:        2.0.0.preview.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/Azure/azure-storage-fuse/
Source0:        https://github.com/Azure/azure-storage-fuse/archive/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/Azure/azure-storage-fuse/archive/%{name}-%{version}.tar.gz -O %{name}-%{version}.tar.gz
#   2. tar -xf %{name}-%{version}.tar.gz
#   3. cd azure-storage-fuse-%{name}-%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %{name}-%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz

BuildRequires:  golang >= 1.16
BuildRequires:  fuse3-devel
Requires:       fuse3
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
Blobfuse2 provides a virtual filesystem backed by the Azure Storage. 
It uses the libfuse open source library (fuse3) to communicate with the 
Linux FUSE kernel module, and implements the filesystem operations using 
the Azure Storage REST APIs.

%prep
%setup -q -n %{name}-%{version}

%build
tar --no-same-owner -xf %{SOURCE1}
export GOPATH=%{our_gopath}
go build -buildmode=pie -mod=vendor

%install
install -D -m 0755 ./blobfuse2 %{buildroot}%{_bindir}/blobfuse2

%files
%defattr(-,root,root,-)
%license LICENSE
%doc NOTICE README.md
%{_bindir}/blobfuse2

%changelog
* Tue Sep 27 2022 Gauri Prasad <gapra@microsoft.com> - 2.0.0.preview.3-1
- Original version for CBL-Mariner.