Summary:        The command line for DC/OS
Name:           dcos-cli
Version:        1.2.0
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/dcos/dcos-cli
Source0:        https://github.com/dcos/dcos-cli/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  golang >= 1.17.1
BuildRequires:  git
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
The command line for DC/OS.

%prep
%autosetup -p1

%build
export GOPATH=%{our_gopath}
export NO_DOCKER=1
# No mod download append -mod=vebdor to use vednor cache locally
sed -i 's/CGO_ENABLED=0 go build/CGO_ENABLED=0 go build -mod=vendor/' ./Makefile
# Use correct version
sed -i 's/VERSION?=$(shell git rev-parse HEAD)/VERSION?=%{version}/' ./Makefile
make

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} ./build/linux/dcos

%check
export NO_DOCKER=1
go test -mod=vendor
./build/linux/dcos --version

%files
%defattr(-,root,root)
%license LICENSE
%doc NOTICE README.md
%{_bindir}/dcos

%changelog
* Fri Jul 01 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.2.0-1
- Original version for CBL-Mariner.
- License verified.
