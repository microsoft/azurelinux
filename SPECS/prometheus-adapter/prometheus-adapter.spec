Summary:        Kubernetes Custom, Resource, and External Metric APIs implemented to work with Prometheus.
Name:           prometheus-adapter
Version:        0.10.0
Release:        15%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/kubernetes-sigs/prometheus-adapter
Source0:        https://github.com/kubernetes-sigs/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2024-24786.patch
Patch1:         CVE-2022-32149.patch
BuildRequires:  golang

%description
Implementation of Prometheus via Kubernetes Custom, Resource, and External Metric API.

%package docs
Summary:        prometheus-adapter docs
Requires:       %{name} = %{version}-%{release}

%description docs
Documentation for prometheus-adapter

%prep
%autosetup -p1

%build
make prometheus-adapter

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vp adapter             %{buildroot}%{_bindir}/

%check
make test

%files
%license LICENSE NOTICE
%{_bindir}/*

%files docs
%doc docs CONTRIBUTING.md OWNERS SECURITY.md SECURITY_CONTACTS VERSION code-of-conduct.md
%doc README.md RELEASE.md

%changelog
* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-15
- Bump release to rebuild with go 1.22.7

* Fri Aug 30 2024 Sindhu Karri <lakarri@microsoft.com> - 0.10.0-14
- Fix CVE-2022-32149 in golang.org/x/text

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-13
- Bump release to rebuild with go 1.21.11

* Thu May 16 2024 Rohit Rawat <rohitrawat@microsoft.com> - 0.10.0-12
- Fix CVE-2024-24786

* Fri Feb 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-11
- Bump release to rebuild with go 1.21.6

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-10
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.10.0-9
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-8
- Bump release to rebuild with go 1.19.12

* Wed Jul 26 2023 Osama Esmail <osamaesmail@mirosoft.com> - 0.10.0-7
- Removing `prometheus` from BuildRequires
- Making `docs` a separate package

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-6
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-5
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-4
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-3
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-2
- Bump release to rebuild with go 1.19.6

* Wed Feb 15 2023 Osama Esmail <osamaesmail@microsoft.com> - 0.10.0-1
- Original version for CBL-Mariner
- License verified.
