%global debug_package %{nil}

Name:          helm
Version:       3.13.1
Release:       1%{?dist}
Summary:       The Kubernetes Package Manager
Group:         Applications/Networking
License:       Apache 2.0
Vendor:        Microsoft Corporation
Distribution:  Mariner
Url:           https://github.com/helm/helm
#Source0:      https://github.com/%{name}/%{name}/archive/v%{version}.tar.gz
Source0:       %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/helm/helm/archive/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:       %{name}-%{version}-vendor.tar.gz
BuildRequires: golang <= 1.18.8

%description
Helm is a tool that streamlines installing and managing Kubernetes applications. Think of it like apt/yum/homebrew for Kubernetes.

%prep
%autosetup -p1

%build
tar -xf %{SOURCE1} --no-same-owner
export VERSION=%{version}
for cmd in cmd/* ; do
    go build -tags '' -ldflags '-w -s -X helm.sh/helm/v3/internal/version.version=v%{version} -X helm.sh/helm/v3/internal/version.metadata= -X helm.sh/helm/v3/internal/version.gitCommit= -X helm.sh/helm/v3/internal/version.gitTreeState=clean ' \
    -mod=vendor -v -o $(basename $cmd) ./$cmd
done

%install
install -d -m 755 %{buildroot}%{_bindir}
install -m 755 ./helm %{buildroot}%{_bindir}

%files
%license LICENSE
%doc ADOPTERS.md SECURITY.md code-of-conduct.md CONTRIBUTING.md README.md
%{_bindir}/helm


%check
go test -v ./cmd/helm

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.13.1-1
- Auto-upgrade to 3.13.1 - Azure Linux 3.0 - package upgrades

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-11
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 3.10.3-10
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-9
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-8
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-7
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-6
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-5
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-4
- Bump release to rebuild with go 1.19.6

* Thu Feb 16 2023 Suresh Thelkar <sthelkar@microsoft.com> - 3.10.3-3
- Patch CVE-2023-25165
- License verified.

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-2
- - Set golang <= 1.18.8 build requires

* Wed Jan 04 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.10.3-1
- Auto-upgrade to 3.10.3 - to fix CVE-2022-23524

* Thu Dec 22 2022 Nan Liu <liunan@microsoft.com> - 3.9.4-5
- Enable the check tests

* Wed Dec 21 2022 Nan Liu <liunan@microsoft.com> - 3.9.4-4
- Patch CVE-2022-23525, CVE-2022-23526

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.9.4-3
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.9.4-2
- Bump release to rebuild with go 1.18.8

* Mon Oct 24 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.9.4-1
- Upgrade to 3.9.4

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.9.3-2
- Bump release to rebuild against Go 1.18.5

* Mon Aug 22 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> 3.9.3-1
- Update helm version to 3.9.3
- Fix version info not displaying correct version.

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 3.4.1-5
- Bump release to rebuild with golang 1.18.3
- License verified

* Mon Sep 20 2021 Henry Beberman <henry.beberman@microsoft.com> - 3.4.1-4
- Patch CVE-2021-32690

* Mon Sep 20 2021 Henry Beberman <henry.beberman@microsoft.com> - 3.4.1-3
- Patch CVE-2021-21303

* Tue Aug 17 2021 Henry Li <lihl@microsoft.com> 3.4.1-2
- Update and rename vendor source tarball
- Use go to build the project from vendor source
- Remove glide and ca-certificates from BR
- Modify file section to add license and document files

* Wed Nov 25 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 3.4.1-1
- Update helm version 3

* Tue Jun 02 2020 Paul Monson <paulmon@microsoft.com> 2.14.3-2
- Rename go to golang
- Add ca-certificates temporarily

* Thu Oct 17 2019 Andrew Phelps <anphel@microsoft.com> 2.14.3-1
- Original version for CBL-Mariner
