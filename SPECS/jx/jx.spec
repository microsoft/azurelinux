Summary:        Command line tool for working with Jenkins X.
Name:           jx
Version:        3.2.236
Release:        1%{?dist}
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

BuildRequires:  golang >= 1.17.1
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
Command line tool for working with Jenkins X.

%prep
%autosetup -p1

%build
tar --no-same-owner -xf %{SOURCE1}
export GOPATH=%{our_gopath}
# No download use vednor cache locally
sed -i 's/go mod download/# go mod download/' ./Makefile
sed -i 's/CGO_ENABLED=$(CGO_ENABLED) $(GO) $(BUILD_TARGET)/CGO_ENABLED=$(CGO_ENABLED) $(GO) $(BUILD_TARGET) -mod=vendor/' ./Makefile
make build

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./build/jx

%check
./build/jx --help

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/jx

%changelog
* Wed Jun 22 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 3.2.236-1
- Original version for CBL-Mariner.
- License verified.
