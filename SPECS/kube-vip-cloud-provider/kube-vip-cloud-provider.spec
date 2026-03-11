Summary:        The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups
Name:           kube-vip-cloud-provider
Version:        0.0.10
Release:        5%{?dist}
License:        ASL 2.0
URL:            https://github.com/kube-vip/kube-vip-cloud-provider
Group:          Applications/Text
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/kube-vip/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Note that the source file should be renamed to the format {name}-%{version}.tar.gz

# Steps to manually create the vendor tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# Adding the vendor folder and creating a tarball
# How to re-build this file:
# 1. wget https://github.com/kube-vip/%%{name}/archive/refs/tags/v%%{version}tar.gz -O %%{name}-%%{version}.tar.gz
# 2. <repo-root>/toolkit/scripts/build_go_vendor_cache.sh %%{name}-%%{version}.tar.gz

Source1: %{name}-%{version}-vendor.tar.gz

Patch1:        CVE-2023-47108.patch
Patch2:        CVE-2024-45338.patch
# CVE-2025-22872 is fixed in go net version .38.0 by https://github.com/golang/net/commit/e1fcd82abba34df74614020343be8eb1fe85f0d9
Patch3:        CVE-2025-22872.patch
Patch4:        CVE-2025-47911.patch
Patch5:        CVE-2025-58190.patch

BuildRequires: golang >= 1.22

%description
The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups.

%prep
%autosetup -a 1 -p1

%build 
go build -mod=vendor

%install
install -d %{buildroot}%{_bindir}
install kube-vip-cloud-provider %{buildroot}%{_bindir}/kube-vip-cloud-provider

%files
%{_bindir}/kube-vip-cloud-provider

%changelog
* Wed Feb 18 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.10-5
- Patch for CVE-2025-58190, CVE-2025-47911

* Mon Apr 21 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 0.0.10-4
- Add patch for CVE-2025-22872

* Tue Dec 31 2024 Rohit Rawat <rohitrawat@microsoft.com> - 0.0.10-3
- Add patch for CVE-2024-45338

* Tue Sep 03 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.10-2
- Release bump to fix package information.

* Mon Jul 08 2024 Tobias Brick <tobiasb@microsoft.com> - 0.0.10-1
- Upgrade to 0.0.10
- Patch CVE-2023-47108

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.7-1
- Auto-upgrade to 0.0.7 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.2-13
- Bump release to rebuild with go 1.20.10

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
