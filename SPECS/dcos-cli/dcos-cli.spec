Summary:        The command line for DC/OS
Name:           dcos-cli
Version:        1.2.0
Release:        14%{?dist}
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
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-14
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.2.0-13
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-12
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-11
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-10
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-9
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-8
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-7
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.2.0-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.2.0-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.2.0-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.2.0-2
- Bump release to rebuild against Go 1.18.5

* Fri Jul 01 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.2.0-1
- Original version for CBL-Mariner.
- License verified.
