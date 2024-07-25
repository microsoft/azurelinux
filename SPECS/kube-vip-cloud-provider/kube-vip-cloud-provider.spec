Summary:        The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups
Name:           kube-vip-cloud-provider
Version:        0.0.2
Release:        18%{?dist}
License:        ASL 2.0
URL:            https://github.com/kube-vip/kube-vip-cloud-provider
Group:          Applications/Text
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://github.com/kube-vip/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Note that the source file should be renamed to the format {name}-%{version}.tar.gz

# Steps to manually create the vendor tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# Adding the vendor folder and creating a tarball
# How to re-build this file:
# 1. wget https://github.com/kube-vip/%%{name}/archive/refs/tags/v%%{version}tar.gz -O %%{name}-%%{version}.tar.gz
# 2. tar -xf %%{name}-%%{version}.tar.gz
# 3. cd %%{name}-%%{version}
# 4. go mod vendor
# 5. tar -cf %%{name}-%%{version}-vendor.tar.gz vendor

Source1: %{name}-%{version}-vendor.tar.gz
Patch0:         CVE-2022-21698.patch
Patch1:         CVE-2021-44716.patch
Patch2:         CVE-2023-44487.patch
BuildRequires: golang

%description
The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups.

%prep
%autosetup -N
# Apply vendor before patching
tar -xvf %{SOURCE1}
%autopatch -p1

%build
go build -mod=vendor

%install
install -d %{buildroot}%{_bindir}
install kube-vip-cloud-provider %{buildroot}%{_bindir}/kube-vip-cloud-provider

%check
go test -mod=vendor ./...

%files
%{_bindir}/kube-vip-cloud-provider

%changelog
* Thu Jul 25 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-18
- Bump release to rebuild with go 1.22.5

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-17
- Bump release to rebuild with go 1.21.11

* Wed Feb 07 2024 Daniel McIlvaney <damcilva@microsoft.com> - 0.0.2-16
- Address CVE-2023-44487 by patching vendored golang.org/x/net
- Rework CVE-2023-21698.patch to apply without directory change
- Add check section

* Mon Feb 05 2024 Osama Esmail <osamaesmail@microsoft.com> - 0.0.2-15
- Fix CVE-2021-44716

* Tue Jan 31 2024 Tobias Brick <tobiasb@microsoft.com> - 0.0.2-14
- Fix CVE-2022-21698

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-13
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.0.2-12
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-11
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-10
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-9
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-8
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-7
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-6
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-5
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-4
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.0.2-3
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.0.2-2
- Bump release to rebuild with go 1.18.8

* Tue Sep 06 2022 Vinayak Gupta <guptavinayak@microsoft.com> - 0.0.2-1
- Original version for CBL-Mariner
- License Verified
