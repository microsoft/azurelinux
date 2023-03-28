Summary:        Kubernetes Custom, Resource, and External Metric APIs implemented to work with Prometheus.
Name:           prometheus-adapter
Version:        0.10.0
Release:        3%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/kubernetes-sigs/prometheus-adapter
Source0:        https://github.com/kubernetes-sigs/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  golang
BuildRequires:  prometheus

%description
Implementation of Prometheus via Kubernetes Custom, Resource, and External Metric API.

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
%doc docs CONTRIBUTING.md OWNERS SECURITY.md SECURITY_CONTACTS VERSION code-of-conduct.md
%doc README.md RELEASE.md
%{_bindir}/*

%changelog
* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-3
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-2
- Bump release to rebuild with go 1.19.6

* Wed Feb 15 2023 Osama Esmail <osamaesmail@microsoft.com> - 0.10.0-1
- Original version for CBL-Mariner
- License verified.