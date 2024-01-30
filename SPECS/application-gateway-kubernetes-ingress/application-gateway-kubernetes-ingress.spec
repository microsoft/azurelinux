%global debug_package %{nil}
Summary:        Application Gateway Ingress Controller
Name:           application-gateway-kubernetes-ingress
Version:        1.4.0
Release:        17%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Networking
URL:            https://github.com/Azure/application-gateway-kubernetes-ingress
#Source0:       https://github.com/Azure/application-gateway-kubernetes-ingress/archive/refs/tags/1.4.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using vendored Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/Azure/%%{name}/archive/refs/tags/%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
# If upstream ever upgrades client_goland to 1.11.1, we can get rid of this patch.
Patch0:         CVE-2022-21698.patch
BuildRequires:  golang >= 1.13

%description
This is an ingress controller that can be run on Azure Kubernetes Service (AKS) to allow an Azure Application Gateway 
to act as the ingress for an AKS cluster. 

%prep
%setup
rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner
%patch -P 0 -p 1 -d vendor/github.com/prometheus/client_golang

%build
export VERSION=%{version}
export VERSION_PATH=github.com/Azure/application-gateway-kubernetes-ingress/pkg/version

go build -ldflags "-s -X $VERSION_PATH.Version=$VERSION" -mod=vendor -v -o appgw-ingress ./cmd/appgw-ingress

%install
mkdir -p %{buildroot}%{_bindir}
cp appgw-ingress %{buildroot}%{_bindir}/


%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/appgw-ingress

%changelog
* Mon Jan 01 2024 Tobias Brick <tobiasb@microsoft.com> - 1.4.0-17
- Patch for CVE-2022-21698
- Moved vendored tarball extraction into %prep and changed from %autosetup to %setup

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-16
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.4.0-15
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-14
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-13
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-12
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-11
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-10
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-9
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-8
- Bump release to rebuild with go 1.19.5

* Tues Jan 24 2023 Adit Jha <aditjha@microsoft.com> - 1.4.0-7
- Bump release to rebuild vendor repoistory which contain patch fix for CVE-2021-4235, CVE-2022-3064

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.4.0-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.4.0-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.4.0-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.4.0-2
- Bump release to rebuild with golang 1.18.3

* Mon Jul 12 2021 Henry Li <lihl@microsoft.com> - 1.4.0-1
- Original version for CBL-Mariner.
- License Verified.
