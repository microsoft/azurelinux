Summary:        Open Container Image manipulation tool
Name:           umoci
Version:        0.4.7
Release:        13%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/opencontainers/umoci
Source0:        https://github.com/opencontainers/umoci/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
BuildRequires:  golang >= 1.17.9

%description
umoci modifies Open Container images.
umoci is a manipulation tool for OCI images. In particular, it is an
alternative to oci-image-tools provided by the OCI.

%prep
%setup -q

%build
tar --no-same-owner -xf %{SOURCE0}
export GOPATH=%{our_gopath}
make BUILD_FLAGS="-mod=vendor" VERSION="%{version}" umoci

%install
install -D -m 0755 ./umoci %{buildroot}%{_bindir}/umoci

%check
go test -mod=vendor
./umoci --version

%files
%defattr(-,root,root)
%license COPYING
%doc README.md
%{_bindir}/umoci

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-13
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.4.7-12
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-11
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-10
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-9
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-8
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-7
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-6
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-5
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.4.7-4
- Bump release to rebuild with go 1.19.4

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.4.7-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.4.7-2
- Bump release to rebuild against Go 1.18.5

* Mon Jul 25 2022 Tom Fay <tomfay@microsoft.com> - 0.4.7-1
- Original version for CBL-Mariner.
- License verified.
