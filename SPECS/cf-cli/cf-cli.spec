Summary:        The official command line client for Cloud Foundry.
Name:           cf-cli
Version:        8.4.0
Release:        1%{?dist}
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

BuildRequires:  golang >= 1.18.3
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
The official command line client for Cloud Foundry.

%prep
%setup -q -n cli-%{version}

%build
tar --no-same-owner -xf %{SOURCE1}
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
* Fri Jun 24 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 8.4.0-1
- Original version for CBL-Mariner.
- License verified.
