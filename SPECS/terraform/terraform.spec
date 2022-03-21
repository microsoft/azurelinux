%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

Summary:        Infrastructure as code deployment management tool
Name:           terraform
Version:        1.1.7
Release:        1%{?dist}
License:        MPL-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://www.terraform.io/
#Source0:       https://github.com/hashicorp/terraform/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
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

BuildRequires:  golang >= 1.17.2

%description
Terraform is an infrastructure as code deployment management tool

%prep
%autosetup -p1

%build
tar --no-same-owner -xf %{SOURCE1}
export GOPATH=%{our_gopath}
go build -mod=vendor -v -a -o terraform

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./terraform

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/terraform

%changelog
* Wed Mar 23 2022 Matthew Torr <matthewtorr@microsoft.com> - 1.1.7-1
- Initial release of terraform RPM for Mariner 2.
