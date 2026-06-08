%define         commit_hash 30feaa1a915b869ebc2eea6328624b49facd4bfb

Summary:        A Docker CLI plugin for extended build capabilities with BuildKit
Release:        15%{?dist}
Distribution:   Azure Linux
URL:            https://www.github.com/docker/buildx
Source0:        https://github.com/docker/buildx/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2024-45337.patch
Patch1:         CVE-2024-45338.patch
Patch2:         CVE-2025-22869.patch
Patch3:         CVE-2025-0495.patch
Patch4:         CVE-2025-22872.patch
Patch5:         CVE-2025-47913.patch
Patch6:         CVE-2025-11065.patch
Patch7:         CVE-2025-47911.patch
Patch8:         CVE-2025-58190.patch
Patch9:         CVE-2026-39882.patch
Patch10:        CVE-2026-35469.patch
Patch11:        CVE-2026-39821.patch
Patch12:        CVE-2026-39829.patch
Patch13:        CVE-2026-39830.patch
Patch14:        CVE-2026-39832.patch
Patch15:        CVE-2026-39834.patch
Patch16:        CVE-2026-42506.patch
Patch17:        CVE-2026-46597.patch
Patch18:        CVE-2026-27136.patch
Patch19:        CVE-2026-25680.patch
Patch20:        CVE-2026-25681.patch
Patch21:        CVE-2026-39827.patch
Patch22:        CVE-2026-39835.patch
Patch23:        CVE-2026-42502.patch
Patch24:        CVE-2026-46598.patch
Patch25:        CVE-2026-39833.patch

# conflicting packages
Conflicts: docker-ce
Conflicts: docker-ee

Obsoletes: moby-buildx < %{version}-%{release}
Provides:  moby-buildx = %{version}-%{release}

%description
A Docker CLI plugin for extended build capabilities with BuildKit

%prep
%autosetup -p1 -n buildx-%{version}

%build
export CGO_ENABLED=0
go build -mod=vendor \
    -ldflags "-X version.Version=%{version} -X version.Revision=%{commit_hash} -X version.Package=github.com/docker/buildx" \
    -o buildx \
    ./cmd/buildx

%install
mkdir -p "%{buildroot}%{_libexecdir}/docker/cli-plugins"
install -m 755 buildx "%{buildroot}%{_libexecdir}/docker/cli-plugins/docker-buildx"

%files
%license LICENSE
%{_libexecdir}/docker/cli-plugins/docker-buildx

%changelog
* Mon Jun 01 2026 Akhila Guruju <v-guakhila@microsoft.com> - 0.14.0-15
- Patch CVE-2026-39833 and fix patch for CVE-2026-39832

* Mon Jun 01 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.14.0-14
- Patch for CVE-2026-46598, CVE-2026-42502, CVE-2026-39835, CVE-2026-39827, CVE-2026-25681, CVE-2026-25680

* Mon Apr 20 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.14.0-11
- Patch for CVE-2026-39882
* Wed May 27 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.14.0-13
- Patch for CVE-2026-46597, CVE-2026-42506, CVE-2026-39834, CVE-2026-39832, CVE-2026-39830, CVE-2026-39829, CVE-2026-39821, CVE-2026-27136

* Thu May 07 2026 Akhila Guruju <v-guakhila@microsoft.com> - 0.14.0-12
- Patch CVE-2026-35469

* Mon Apr 20 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.14.0-11
- Patch for CVE-2026-39882

* Thu Feb 19 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.14.0-10
- Patch for CVE-2025-58190, CVE-2025-47911

* Tue Feb 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.14.0-9
- Patch for CVE-2025-11065

* Tue Nov 18 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.14.0-8
- Patch for CVE-2025-47913

* Sun Aug 31 2025 Andrew Phelps <anphel@microsoft.com> - 0.14.0-7
- Set BR for golang to < 1.25

* Wed May 21 2025 Sreeniavsulu Malavathula <v-smalavathu@microsoft.com> - 0.14-0-6
- Patch CVE-2025-22872

* Tue May 13 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 0.14.0-5
- Fix CVE-2025-0495 with upstream patch modified to apply for azurelinux package

* Mon Mar 03 2025 Kanishk Bansal <kanbansal@microsoft.com> - 0.14.0-4
- Fix CVE-2025-22869 with an upstream patch

* Tue Dec 31 2024 Rohit Rawat <rohitrawat@microsoft.com> - 0.14.0-3
- Add patch for CVE-2024-45338

* Fri Dec 20 2024 Aurelien Bombo <abombo@microsoft.com> - 0.14.0-2
- Add patch for CVE-2024-45337

* Thu May 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.14.0-1
- Auto-upgrade to 0.14.0 - address CVE-2024-23653

* Tue Feb 27 2024 Henry Beberman <henry.beberman@microsoft.com> - 0.12.1-1
- Rename package from moby-buildx to docker-buildx
- Upgrade to version 0.12.1

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.11.2-1
- Auto-upgrade to 0.11.2 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-15
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 0.7.1-14
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.7.1-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.7.1-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.7.1-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 0.7.1-2
- Bump release to rebuild with golang 1.18.3

* Fri Jan 28 2022 Nicolas Guibourge <nicolasg@microsoft.com> 0.7.1-1
- Upgrade to 0.7.1.
- Use code from upstream instead of Azure fork.
* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 0.4.1+azure-3
- Increment release to force republishing using golang 1.15.13.
* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 0.4.1+azure-2
- Increment release to force republishing using golang 1.15.
* Thu Jun 11 2020 Andrew Phelps <anphel@microsoft.com> 0.4.1+azure-1
- Update to version 0.4.1+azure
* Wed May 20 2020 Joe Schmitt <joschmit@microsoft.com> 0.3.1+azure-5
- Remove reliance on existing GOPATH environment variable.
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.3.1+azure-4
- Added %%license line automatically
* Mon May 04 2020 Eric Li <eli@microsoft.com> 0.3.1+azure-3
- Add #Source0: and license verified
* Fri May 01 2020 Emre Girgin <mrgirgin@microsoft.com> 0.3.1+azure-2
- Renaming go to golang
* Fri Apr 03 2020 Mohan Datla <mdatla@microsoft.com> 0.3.1+azure-1
- Initial CBL-Mariner import from Azure.
* Tue Mar 24 2020 Brian Goff <brgoff@microsoft.com>
- Initial version
