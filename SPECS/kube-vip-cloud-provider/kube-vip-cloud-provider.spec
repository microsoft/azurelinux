Summary:        The Kube-Vip cloud provider functions as a general-purpose cloud provider for on-premises bare-metal or virtualized setups
Name:           kube-vip-cloud-provider
Version:        0.0.10
Release:        14%{?dist}
License:        ASL 2.0
URL:            https://github.com/kube-vip/kube-vip-cloud-provider
Group:          Applications/Text
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/kube-vip/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Note that the source file should be renamed to the format %%{name}-%%{version}.tar.gz

# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/kube-vip/%%{name}/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod edit -modfile=go.mod -require=github.com/google/cel-go@v0.31.0 \
#                                  -require=k8s.io/apiserver@v0.34.0 \
#                                  -require=google.golang.org/grpc@v1.83.2 \
#                                  -require=go.opentelemetry.io/otel@v1.47.0 \
#                                  -require=go.opentelemetry.io/otel/sdk@v1.47.0
#   5. go mod tidy
#   6. go mod vendor
#   7. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -czf %%{name}-%%{version}-vendor-v4.tar.gz vendor
#
# Alternatively, run the helper from this spec directory:
#   bash generate_source_tarball.sh \
#       --srcTarball "$(pwd)/%%{name}-%%{version}.tar.gz" \
#       --outFolder "$(pwd)" \
#       --pkgVersion %%{version} --vendorVersion 4
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - You require Go 1.26+ for OpenTelemetry v1.47.0.
#       - cel-go, apiserver and grpc are the upgrades from CVE-2026-84445.patch; otel and otel/sdk are for
#         CVE-2026-128085 and CVE-2026-128086. The resulting go.mod/go.sum changes are carried in Patch2 and Patch11.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.

Source1: %{name}-%{version}-vendor-v4.tar.gz

Patch0:       CVE-2026-73500.patch
Patch1:       CVE-2026-37236.patch
Patch2:       CVE-2026-84445.patch
Patch3:       CVE-2026-78659.patch
Patch4:       CVE-2026-78660.patch
Patch5:       CVE-2026-78663.patch
Patch6:       CVE-2026-78669.patch
Patch7:       CVE-2026-81870.patch
Patch8:       CVE-2026-97032.patch
Patch9:       CVE-2026-78661.patch
Patch10:      CVE-2026-97045.patch
Patch11:      CVE-2026-128085.patch

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

%files
%{_bindir}/kube-vip-cloud-provider

%changelog
* Fri Nov 27 2026 Swapnil Sahu <v-swapsahu@microsoft.com> - 0.0.10-14
- Patch for CVE-2026-128085, CVE-2026-128086
- Upgrade vendored go.opentelemetry.io/otel to v1.47.0
- Drop SDK hunks from CVE-2026-81870 patch, already included in otel SDK v1.47.0

* Tue Nov 24 2026 Muhammad Falak R Wani <mwani@microsoft.com> - 0.0.10-13
- Remove 'BuildRequires: golang >= 1.25' pin; the default Go toolchain satisfies it.

* Tue Nov 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.10-12
- Patch for CVE-2026-97045, CVE-2026-78661

* Mon Oct 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.10-11
- Patch for CVE-2026-97032, CVE-2026-81870, CVE-2026-78669, CVE-2026-78663, CVE-2026-78660, CVE-2026-78659

* Wed Sep 16 2026 Aditya Singh <v-aditysing@microsoft.com> - 0.0.10-10
- Patch for CVE-2026-84445, CVE-2026-84304, CVE-2026-83530
- Removed patch for CVE-2024-45338, CVE-2025-22872, CVE-2025-47911, CVE-2025-58190, CVE-2026-39821,
  CVE-2026-42506, CVE-2026-27136, CVE-2026-25680, CVE-2026-25681, CVE-2026-42502, CVE-2026-56852
- Pinned golang >= v1.25

* Tue Sep 08 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.10-9
- Patch for CVE-2026-37236

* Fri Aug 14 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.10-8
- Patch for CVE-2026-73500

* Mon Jul 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.10-7
- Patch for CVE-2026-56852

* Wed May 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.0.10-6
- Patch for CVE-2026-42506, CVE-2026-39821, CVE-2026-27136, CVE-2026-42502, CVE-2026-25681, CVE-2026-25680

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
