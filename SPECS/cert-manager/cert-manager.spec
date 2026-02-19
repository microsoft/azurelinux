Summary:        Automatically provision and manage TLS certificates in Kubernetes
Name:           cert-manager
Version:        1.12.15
Release:        6%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/jetstack/cert-manager
Source0:        https://github.com/jetstack/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated GO dependencies from this tarball, since network is disabled during build time.
# How to re-build this file:
# 1. wget https://github.com/jetstack/%%{name}/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
# 2. <repo-root>/SPECS/cert-manager/generate_source_tarball.sh --srcTarball %%{name}-%%{version}.tar.gz --pkgVersion %%{version}
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         CVE-2024-45338.patch
Patch1:         CVE-2025-27144.patch
Patch2:         CVE-2025-22868.patch
Patch3:         CVE-2025-22869.patch
Patch4:         CVE-2025-30204.patch
Patch5:         CVE-2025-32386.patch
Patch6:         CVE-2025-22872.patch
Patch7:         CVE-2025-11065.patch
Patch8:         CVE-2025-47911.patch
Patch9:         CVE-2025-58190.patch

BuildRequires:  golang
Requires:       %{name}-acmesolver
Requires:       %{name}-cainjector
Requires:       %{name}-cmctl
Requires:       %{name}-controller
Requires:       %{name}-webhook

%description
cert-manager is a Kubernetes add-on to automate the management and issuance
of TLS certificates from various issuing sources.

%package acmesolver
Summary:        cert-manager's acmesolver binary

%description acmesolver
HTTP server used to solve ACME challenges.

%package cainjector
Summary:        cert-manager's cainjector binary

%description cainjector
cert-manager CA injector is a Kubernetes addon to automate the injection of CA data into
webhooks and APIServices from cert-manager certificates.

%package controller
Summary:        cert-manager's controller binary

%description controller
cert-manager is a Kubernetes addon to automate the management and issuance of
TLS certificates from various issuing sources.

%package cmctl
Summary:        cert-manager's cmctl binary

%description cmctl
cmctl is a CLI tool manage and configure cert-manager resources for Kubernetes

%package webhook
Summary:        cert-manager's webhook binary

%description webhook
Webhook component providing API validation, mutation and conversion functionality for cert-manager.

%prep
%autosetup -a 1 -p1

%build

LOCAL_BIN_DIR=$(realpath bin)
go -C cmd/acmesolver build -mod=vendor -o "${LOCAL_BIN_DIR}"/acmesolver main.go
go -C cmd/controller build -mod=vendor -o "${LOCAL_BIN_DIR}"/controller main.go
go -C cmd/cainjector build -mod=vendor -o "${LOCAL_BIN_DIR}"/cainjector main.go
go -C cmd/ctl build -mod=vendor -o "${LOCAL_BIN_DIR}"/cmctl main.go
go -C cmd/webhook build -mod=vendor -o "${LOCAL_BIN_DIR}"/webhook main.go

%install
mkdir -p %{buildroot}%{_bindir}
install -D -m0755 bin/acmesolver %{buildroot}%{_bindir}/
install -D -m0755 bin/cainjector %{buildroot}%{_bindir}/
install -D -m0755 bin/controller %{buildroot}%{_bindir}/
install -D -m0755 bin/cmctl %{buildroot}%{_bindir}/
install -D -m0755 bin/webhook %{buildroot}%{_bindir}/
%files

%files acmesolver
%license LICENSE LICENSES
%doc README.md
%{_bindir}/acmesolver

%files cainjector
%license LICENSE LICENSES
%doc README.md
%{_bindir}/cainjector

%files controller
%license LICENSE LICENSES
%doc README.md
%{_bindir}/controller

%files cmctl
%license LICENSE LICENSES
%doc README.md
%{_bindir}/cmctl

%files webhook
%license LICENSE LICENSES
%doc README.md
%{_bindir}/webhook

%changelog
* Thu Feb 19 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.12.15-6
- Patch for CVE-2025-58190, CVE-2025-47911

* Tue Feb 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.12.15-5
- Patch for CVE-2025-11065

* Wed Apr 16 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 1.12.15-4
- Patch CVE-2025-32386 (also fixes CVE-2025-32387)
- Patch CVE-2025-22872

* Fri Mar 28 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.12.15-3
- Patch CVE-2025-30204

* Mon Mar 03 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.12.15-2
- Fix CVE-2025-22868, CVE-2025-22869 & CVE-2025-27144 with an upstream patch

* Mon Jan 27 2025 Rohit Rawat <rohitrawat@microsoft.com> - 1.12.15-1
- Upgrade to 1.12.15 - to fix CVE-2024-12401
- Remove CVE-2024-45337.patch as it is fixed in 1.12.15

* Tue Dec 31 2024 Rohit Rawat <rohitrawat@microsoft.com> - 1.12.13-3
- Add patch for CVE-2024-45338

* Wed Jan 08 2025 Muhammad Falak <mwani@microsoft.com> - 1.12.13-2
- Patch CVE-2024-45337

* Mon Sep 16 2024 Jiri Appl <jiria@microsoft.com> - 1.12.13-1
- Upgrade to 1.12.13 which carries helm 3.14.2 to fix CVE-2024-26147 and CVE-2024-25620

* Wed Aug 07 2024 Bhagyashri Pathak <bhapathak@microsoft.com> - 1.12.12-2
- Patch for CVE-2024-25620

* Wed Jul 10 2024 Tobias Brick <tobiasb@microsoft.com> - 1.12.12-1
- Upgrade to 1.12.12 to fix CVE-2024-26147 and CVE-2023-45142

* Wed May 29 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 1.11.2-8
- Bump release to build with new helm to fix CVE-2024-25620

* Wed May 22 2024 Neha Agarwal <nehaagarwal@microsoft.com> - 1.11.2-7
- Bump release to build with new helm to fix CVE-2024-26147

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.2-6
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.11.2-5
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.2-4
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.2-3
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.2-2
- Bump release to rebuild with go 1.19.10

* Mon May 15 2023 Aditya Dubey <adityadubey@microsoft.com> - 1.11.0-1
- Upgrade to v1.11.2
- Removed patch for CVE-2023-25165
- This version uses helm v3.11.1, which fixes CVE-2023-25165 and thus we do not need the patch file anymore

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.3-10
- Bump release to rebuild with go 1.19.8

* Wed Mar 29 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.3-9
- Add patch for CVE-2023-25165

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.3-8
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.3-7
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.3-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.3-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.7.3-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.7.3-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.7.3-2
- Bump release to rebuild against Go 1.18.5

* Fri Aug 05 2022 Chris Gunn <chrisgun@microsoft.com> - 1.7.3-1
- Update to v1.7.3
- Split binaries into separate packages.

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.5.3-2
- Add a hard BR on golang <= 1.17.10
- Bump release to rebuild with golang 1.17.10

* Fri Sep 10 2021 Henry Li <lihl@microsoft.com> - 1.5.3-1
- Original version for CBL-Mariner
- License Verified
