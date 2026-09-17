Summary:        Kubernetes Custom, Resource, and External Metric APIs implemented to work with Prometheus.
Name:           prometheus-adapter
Version:        0.12.0
Release:        11%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/kubernetes-sigs/prometheus-adapter
Source0:        https://github.com/kubernetes-sigs/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/kubernetes-sigs/%%{name}/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod edit -go=1.26.0
#   5. go mod edit -require=google.golang.org/grpc@v1.83.2 \
#                  -require=github.com/google/cel-go@v0.31.0 \
#                  -require=golang.org/x/crypto@v0.57.0
#   6. go mod tidy
#   7. rm -rf vendor && go mod vendor
#   8. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -czf %%{name}-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - Source0 already ships a "vendor" tree; %prep replaces it with this one so that the
#         module bump does not require regenerating Source0 itself, whose checksum is shared
#         with the 3.0-dev branch.
#       - Steps 2-8 are also automated by generate_source_tarball.sh:
#           ./generate_source_tarball.sh --srcTarball %%{name}-%%{version}.tar.gz \
#               --outFolder /tmp --pkgVersion %%{version}
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         CVE-2026-73500.patch
Patch1:         CVE-2026-37236.patch
Patch2:         CVE-2026-84304.patch
Patch3:         fix-cel-go-api-migration.patch
BuildRequires:  golang >= 1.26

%description
Implementation of Prometheus via Kubernetes Custom, Resource, and External Metric API.

%package docs
Summary:        prometheus-adapter docs
Requires:       %{name} = %{version}-%{release}

%description docs
Documentation for prometheus-adapter

%prep
%autosetup -N
# Source0 ships a vendor tree pinned to the old module set; replace it wholesale.
rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner
%autopatch -p1

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
* Fri Sep 18 2026 Sumit Jena <v-sumitjena@microsoft.com> - 0.12.0-11
- Patch for CVE-2026-84304, CVE-2026-84445, CVE-2026-83530
- Removed patches CVE-2024-45338, CVE-2025-22872, CVE-2025-47911, CVE-2025-58190,
  CVE-2026-25680, CVE-2026-25681, CVE-2026-27136, CVE-2026-33186, CVE-2026-39821,
  CVE-2026-42502, CVE-2026-42506, CVE-2026-56852

* Tue Sep 08 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.12.0-10
- Patch for CVE-2026-37236

* Fri Aug 14 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.12.0-9
- Patch for CVE-2026-73500

* Tue Aug 11 2026 Akhila Guruju <v-guakhila@microsoft.com> - 0.12.0-8
- Patch CVE-2026-33186

* Mon Jul 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.12.0-7
- Patch for CVE-2026-56852

* Wed May 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.12.0-6
- Patch for CVE-2026-42506, CVE-2026-39821, CVE-2026-27136, CVE-2026-42502, CVE-2026-25681, CVE-2026-25680

* Thu Feb 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.12.0-5
- Patch for CVE-2025-47911, CVE-2025-58190

* Sun Aug 31 2025 Andrew Phelps <anphel@microsoft.com> - 0.12.0-4
- Set BR for golang to < 1.25

* Tue Apr 22 2025 Archana Shettigar <v-shettigara@microsoft.com> - 0.12.0-3
- Patch CVE-2025-22872

* Tue Dec 31 2024 Rohit Rawat <rohitrawat@microsoft.com> - 0.12.0-2
- Patch CVE-2024-45338

* Fri Jul 12 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.12.0-1
- Auto-upgrade to 0.12.0 - Fix CVE-2023-39325, CVE-2023-3978, CVE-2023-45142, CVE-2023-45288, and CVE-2024-24786

* Tue Dec 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.11.2-1
- Auto-upgrade to 0.11.2 - Package Upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.10.0-10
- Bump release to rebuild with go 1.20.10

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
