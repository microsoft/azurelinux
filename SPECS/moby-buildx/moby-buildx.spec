%define         upstream_name buildx
%define         commit_hash 05846896d149da05f3d6fd1e7770da187b52a247

Summary:        A Docker CLI plugin for extended build capabilities with BuildKit
Name:           moby-%{upstream_name}
# update "commit_hash" above when upgrading version
Version:        0.7.1
Release:        16%{?dist}
License:        ASL 2.0
Group:          Tools/Container
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.github.com/docker/buildx
Source0:        https://github.com/docker/buildx/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Fixed in upstream v0.8.0. Can remove when we upgrade to that version.
Patch0:         CVE-2022-21698.patch

BuildRequires: bash
BuildRequires: golang >= 1.17

# conflicting packages
Conflicts: docker-ce
Conflicts: docker-ee

%description
A Docker CLI plugin for extended build capabilities with BuildKit

%prep
%setup -q -n %{upstream_name}-%{version}
%patch 0 -p1 -d vendor/github.com/prometheus/client_golang

%build
export CGO_ENABLED=0
go build -mod=vendor \
    -ldflags "-X version.Version=%{version} -X version.Revision=%{commit_hash} -X version.Package=github.com/docker/buildx" \
    -o buildx \
    ./cmd/buildx

%install
mkdir -p "%{buildroot}/%{_libexecdir}/docker/cli-plugins"
cp -aT buildx "%{buildroot}/%{_libexecdir}/docker/cli-plugins/docker-buildx"

%files
%license LICENSE
%{_libexecdir}/docker/cli-plugins/docker-buildx

%changelog
* Thu Feb 01 2024 Tobias Brick <tobiasb@microsoft.com> - 0.7.1-16
- Fix CVE-2022-21698

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.7.1-15
- Bump release to rebuild with go 1.20.9

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
