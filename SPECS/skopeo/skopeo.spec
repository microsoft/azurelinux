Summary:        Inspect container images and repositories on registries
Name:           skopeo
Version:        1.14.4
Release:        18%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Tools
URL:            https://github.com/containers/skopeo
Source0:        https://github.com/containers/skopeo/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/containers/%%{name}/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod edit -modfile=go.mod -require=google.golang.org/grpc@v1.83.2
#      go mod edit -modfile=go.mod -require=go.opentelemetry.io/otel@v1.47.0
#   5. go mod tidy
#   6. go mod vendor
#   7. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -czf %%{name}-%%{version}-vendor-v2.tar.gz vendor
#
# Alternatively, run the helper from this spec directory:
#   bash generate_source_tarball.sh \
#       --srcTarball "$(pwd)/%%{name}-%%{version}.tar.gz" \
#       --outFolder "$(pwd)" \
#       --pkgVersion %%{version} --vendorVersion 2
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - You require Go 1.26+ for the updated Go modules.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor-v2.tar.gz
Patch0:         CVE-2022-2879.patch
Patch1:         CVE-2024-6104.patch
Patch2:         CVE-2024-9676.patch
Patch3:         CVE-2025-27144.patch
Patch4:         CVE-2025-58058.patch
Patch5:         CVE-2025-58183.patch
Patch6:         CVE-2025-11065.patch
Patch7:         CVE-2026-24117.patch
Patch8:         CVE-2026-32288.patch
Patch9:         CVE-2026-84445.patch
Patch10:        CVE-2026-107324.patch
Patch11:        CVE-2026-107325.patch
Patch12:        CVE-2026-61801.patch
Patch13:        CVE-2026-78659.patch
Patch14:        CVE-2026-78660.patch
Patch15:        CVE-2026-78669.patch
Patch16:        CVE-2026-97032.patch
Patch17:        CVE-2026-116585.patch
Patch18:        CVE-2026-116586.patch
Patch19:        CVE-2026-116587.patch
Patch20:        CVE-2026-116591.patch
Patch21:        CVE-2026-128085.patch

%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
BuildRequires:  btrfs-progs-devel
BuildRequires:  device-mapper-devel
BuildRequires:  go-md2man
BuildRequires:  golang
BuildRequires:  gpgme-devel
BuildRequires:  libassuan-devel
BuildRequires:  pkgconfig
Requires:       libcontainers-common

%description
Command line utility to inspect images and repositories directly on Docker
registries without the need to pull them.

%prep
%autosetup -N
rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner
%autopatch -p1

%build
export GOPATH=%{our_gopath}
make

%install
make PREFIX=%{buildroot}%{_prefix} install-binary install-docs

%check
make test-unit-local
./bin/skopeo --version

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%%{name}*

%changelog
* Fri Nov 27 2026 Sushil Sati <v-Sushil.sati@microsoft.com> - 1.14.4-18
- Patch for CVE-2026-128085 and CVE-2026-128086 by upgrading vendored go.opentelemetry.io/otel to v1.47.0

* Tue Nov 24 2026 Muhammad Falak R Wani <mwani@microsoft.com> - 1.14.4-17
- Remove 'BuildRequires: golang >= 1.25' pin; the default Go toolchain satisfies it.

* Tue Nov 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-16
- Patch for CVE-2026-116591, CVE-2026-116587, CVE-2026-116586, CVE-2026-116585

* Wed Oct 14 2026 jykanase <v-jykanase@microsoft.com> - 1.14.4-15
- Modified patch for CVE-2026-61801

* Tue Oct 13 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-14
- Patch for CVE-2026-97032, CVE-2026-78669, CVE-2026-78660, CVE-2026-78659, CVE-2026-61801, CVE-2026-107325, CVE-2026-107324

* Thu Sep 17 2026 Akhila Guruju <v-guakhila@microsoft.com> - 1.14.4-13
- Generate Source1 vendor tarball to fix CVE-2026-84445 and CVE-2026-84304
- Drop patches for CVE-2023-45288, CVE-2026-39821 and CVE-2026-56852, already fixed by the upgraded golang.org/x/net and golang.org/x/text modules

* Mon Jul 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-12
- Patch for CVE-2026-56852

* Wed May 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-11
- Patch for CVE-2026-39821

* Mon Apr 20 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-10
- Patch for CVE-2026-32288

* Wed Feb 18 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-9
- Patch for CVE-2026-24117

* Tue Feb 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-8
- Patch for CVE-2025-11065

* Sat Nov 15 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-7
- Patch for CVE-2025-58183

* Wed Sep 03 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 1.14.4-6
- Patch for CVE-2025-58058

* Thu Apr 10 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.14.4-5
- Remove extraction command from build

* Sat Mar 01 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.14.4-4
- Fix CVE-2025-27144 with an upstream patch

* Mon Nov 11 2024 Rohit Rawat <rohitrawat@microsoft.com> - 1.14.4-3
- Fix CVE-2023-45288 and CVE-2024-9676

* Fri Aug 02 2024 Sindhu Karri <lakarri@microsoft.com> - 1.14.4-2
- Fix CVE-2024-6104 in github.com/hashicorp/go-retryablehttp with a patch

* Thu Jun 27 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 1.14.4-1
- Upgrade to v1.14.4, address CVE-2022-2879

* Tue Jan 30 2024 Henry Li <lihl@microsoft.com> - 1.14.1-1
- Upgrade to v1.14.1

* Tue Oct 17 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.3-1
- Update to v1.13.3 to fix CVE-2023-33199 in rekor.

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.12.0-5
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.12.0-4
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.12.0-3
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.12.0-2
- Bump release to rebuild with go 1.19.11

* Thu Jun 22 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.12.0-1
- Bump skopeo version to 1.12.0 - upgrade to latest

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-5
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-4
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-3
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-2
- Bump release to rebuild with go 1.19.6

* Wed Feb 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.0-1
- Auto-upgrade to 1.11.0 - upgrade to latest

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.9.1-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.1-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.1-2
- Bump release to rebuild against Go 1.18.5

* Tue Jul 26 2022 Tom Fay <tomfay@microsoft.com> - 1.9.1-1
- Original version for CBL-Mariner.
- License verified.
