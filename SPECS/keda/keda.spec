Summary:        Kubernetes-based Event Driven Autoscaling
Name:           keda
Version:        2.4.0
Release:        24%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/kedacore/keda
#Source0:       https://github.com/kedacore/%%{name}/archive/refs/tags/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# A couple of notes:
#   A: The -v2 suffix just increases as we make more vendored tarballs.
#   B: Make sure to apply the appropriate patches before creating the tarball.
#
# How to re-build this file.
#   1. wget https://github.com/kedacore/%%{name}/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. Apply appropriate patches
#   5. go mod vendor
#   6. tar  --sort=name \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor-v2.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor-v2.tar.gz
# Patches the version of client_golang used in the vendored source. Should be applied before creating the vendored tarball.
# Can be removed if we upgrade keda to 2.6.0 or later.
Patch0:         CVE-2022-21698.patch
Patch1:         CVE-2023-44487.patch
Patch2:         CVE-2021-44716.patch
Patch3:         CVE-2022-32149.patch
Patch4:         CVE-2024-6104.patch


BuildRequires:  golang

%description
KEDA is a Kubernetes-based Event Driven Autoscaling component.
It provides event driven scale for any container running in Kubernetes

%prep
%autosetup -N
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner
%autopatch -p1

%build
export LDFLAGS="-X=github.com/kedacore/keda/v2/version.GitCommit= -X=github.com/kedacore/keda/v2/version.Version=main"

go build -ldflags "$LDFLAGS" -mod=vendor -v -o bin/keda main.go

gofmt -l -w -s .
go vet ./...

go build -ldflags "$LDFLAGS" -mod=vendor -v -o bin/keda-adapter adapter/main.go

%install
mkdir -p %{buildroot}%{_bindir}
cp ./bin/keda %{buildroot}%{_bindir}
cp ./bin/keda-adapter %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-adapter

%changelog
* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-24
- Bump release to rebuild with go 1.22.7

* Fri Aug 30 2024 Sindhu Karri <lakarri@microsoft.com> - 2.4.0-23
- Fix CVE-2022-32149 with a patch

* Thu Aug 01 2024 Bala <balakumaran.kannan@microsoft.com> - 2.4.0-22
- Patch CVE-2024-6104

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 2.4.0-21
- Drop requirement on a specific version of golang

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-20
- Bump release to rebuild with go 1.21.11

* Fri Feb 09 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.0-19
- Bump release to rebuild with go 1.21.6.

* Mon Feb 05 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 2.4.0-18
- Patch CVE-2021-44716

* Mon Feb 05 2024 Daniel McIlvaney <damcilva@microsoft.com> - 2.4.0-17
- Address CVE-2023-44487 by patching vendored golang.org/x/net/http2

* Tue Jan 01 2024 Tobias Brick <tobiasb@microsoft.com> - 2.4.0-16
- Patch CVE-2022-21698
- Update vendored tarball
- Move tarball expansion to %prep

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-15
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 2.4.0-14
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.4.0-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.4.0-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.4.0-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 2.4.0-2
- Bump release to rebuild with golang 1.18.3
- License verified

* Wed Aug 25 2021 Henry Li <lihl@microsoft.com> - 2.4.0-1
- Original version for CBL-Mariner
