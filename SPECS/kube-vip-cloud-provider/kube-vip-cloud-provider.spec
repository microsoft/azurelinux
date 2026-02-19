Summary:        The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups
Name:           kube-vip-cloud-provider
Version:        0.0.2
Release:        26%{?dist}
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
Patch3:         CVE-2024-28180.patch
Patch4:         CVE-2025-27144.patch
Patch5:         CVE-2022-3162.patch
Patch6:         CVE-2024-51744.patch
Patch7:         CVE-2025-65637.patch
Patch8:         CVE-2025-11065.patch
Patch9:         CVE-2025-30204.patch
BuildRequires: golang

%description
The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups.

%prep
%autosetup -a 1 -p1

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
* Wed Feb 18 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.2-26
- Patch for CVE-2025-30204

* Wed Feb 04 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.2-25
- Patch for CVE-2025-11065

* Mon Dec 08 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.2-24
- Patch for CVE-2025-65637

* Thu Sep 04 2025 Akhila Guruju <v-guakhila@microsoft.com> - 0.0.2-23
- Bump release to rebuild with golang

* Fri Mar 28 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 0.0.2-22
- Fix CVE-2024-51744

* Fri Feb 28 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 0.0.2-21
- Add patch for CVE-2022-3162

* Fri Feb 28 2025 Kanishk Bansal <kanbansal@microsoft.com> - 0.0.2-20
- Apply security fix for CVE-2025-27144 with an upstream patch

* Mon Oct 07 2024 Ahmed Badawi <ahmedbadawi@microsoft.com> - 0.0.2-19
- Apply security fix for CVE-2024-28180 by patching vendored go-jose

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-18
- Bump release to rebuild with go 1.22.7

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-17
- Bump release to rebuild with go 1.21.11

* Wed Feb 07 2024 Daniel McIlvaney <damcilva@microsoft.com> - 0.0.2-16
- Address CVE-2023-44487 by patching vendored golang.org/x/net
- Rework CVE-2023-21698.patch to apply without directory change
- Add check section

* Mon Feb 05 2024 Osama Esmail <osamaesmail@microsoft.com> - 0.0.2-15
- Fix CVE-2021-44716

* Wed Jan 31 2024 Tobias Brick <tobiasb@microsoft.com> - 0.0.2-14
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
