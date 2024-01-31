Summary:        Provides a way for the Kubernetes users to utilize the local storage in each node
Name:           local-path-provisioner
Version:        0.0.21
Release:        14%{?dist}
License:        ASL 2.0
URL:            https://github.com/rancher/local-path-provisioner
Group:          Applications/Text
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://github.com/rancher/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Note that the source file should be renamed to the format {name}-%{version}.tar.gz
# Fixed in upstream 0.0.24, so we can remove this patch when we upgrade to that version
Patch0:         CVE-2022-21698.patch

BuildRequires: golang

%description
Provides a way for the Kubernetes users to utilize the local storage in each node. 

%prep
%setup -q
%patch 0 -p1 -d vendor/github.com/prometheus/client_golang

%build
export CGO_ENABLED=0
go build -mod=vendor 

%install
install -d %{buildroot}%{_bindir}
install local-path-provisioner %{buildroot}%{_bindir}/local-path-provisioner

%files
%{_bindir}/local-path-provisioner

%changelog
* Mon Jan 31 2024 Tobias Brick <tobiasb@microsoft.com> - 0.0.21-14
- Fix CVE-2022-21698

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-13
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.0.21-12
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-11
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-10
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-9
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-8
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-7
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-6
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-5
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.21-4
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.0.21-3
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.0.21-2
- Bump release to rebuild with go 1.18.8

* Thu Jun 23 2022 Lior Lustgarten <lilustga@microsoft.com> 0.0.21-1
- Original version for CBL-Mariner
- License Verified
