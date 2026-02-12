%global debug_package %{nil}
Summary:        Application Gateway Ingress Controller
Name:           application-gateway-kubernetes-ingress
Version:        1.7.7
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Networking
URL:            https://github.com/Azure/application-gateway-kubernetes-ingress
Source0:        https://github.com/Azure/application-gateway-kubernetes-ingress/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Leverage the `generate_source_tarball.sh` to create the vendor sources
# NOTE: govendor-v1 format is for inplace CVE updates so that we do not have to overwrite in the blob-store.
# After fixing any possible CVE for the vendored source, we must bump v1 -> v2
Source1:        %{name}-%{version}-govendor-v1.tar.gz
Patch0:         CVE-2025-30204.patch
Patch1:         CVE-2025-47911.patch
Patch2:         CVE-2025-58190.patch

BuildRequires:  golang >= 1.23

%description
This is an ingress controller that can be run on Azure Kubernetes Service (AKS) to allow an Azure Application Gateway
to act as the ingress for an AKS cluster.

%prep
%autosetup -N

rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner
%autopatch -p1

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
* Thu Feb 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.7.7-3
- Patch for CVE-2025-58190, CVE-2025-47911

* Sat Mar 29 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.7.7-2
- Patch CVE-2025-30204

* Tue Feb 04 2025 Gary Swalling <gaswal@microsoft.com> - 1.7.7-1
- Upgrade to v1.7.7 with golang.org/x/net v0.33.0 for CVE-2023-39325, CVE-2023-44487,
- CVE-2023-45288, CVE-2024-51744, CVE-2024-35255, CVE-2023-3978
- Remove patches which are no longer needed

* Tue Dec 31 2024 Rohit Rawat <rohitrawat@microsoft.com> - 1.7.2-3
- Add patch for CVE-2024-45338

* Thu Jul 11 2024 Thien Trung Vuong <tvuong@microsoft.com> - 1.7.2-2
- Add patch for CVE-2022-21698, CVE-2022-41273
- Move vendored tarball extraction into %prep and %changed from %autosetup to %setup

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.2-1
- Auto-upgrade to 1.7.2 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.0-16
- Bump release to rebuild with go 1.20.10

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

* Tue Jan 24 2023 Adit Jha <aditjha@microsoft.com> - 1.4.0-7
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
