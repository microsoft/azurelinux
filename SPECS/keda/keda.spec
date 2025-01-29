Summary:        Kubernetes-based Event Driven Autoscaling
Name:           keda
Version:        2.14.1
Release:        3%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/kedacore/keda
#Source0:       https://github.com/kedacore/%%{name}/archive/refs/tags/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-govendor-v1.tar.gz
Patch0:         CVE-2024-6104.patch
Patch1:         CVE-2024-45338.patch
BuildRequires:  golang >= 1.15

%description
KEDA is a Kubernetes-based Event Driven Autoscaling component. 
It provides event driven scale for any container running in Kubernetes 

%prep
%autosetup -p1 -a 1

%build
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner
export LDFLAGS="-X=github.com/kedacore/keda/v2/version.GitCommit= -X=github.com/kedacore/keda/v2/version.Version=main"

go build -ldflags "$LDFLAGS" -mod=vendor -v -o bin/keda cmd/operator/main.go

gofmt -l -w -s .
go vet ./...

go build -ldflags "$LDFLAGS" -mod=vendor -v -o bin/keda-adapter cmd/adapter/main.go

go build -ldflags "$LDFLAGS" -mod=vendor -v -o bin/keda-admission-webhooks cmd/webhooks/main.go

%install
mkdir -p %{buildroot}%{_bindir}
cp ./bin/keda %{buildroot}%{_bindir}
cp ./bin/keda-adapter %{buildroot}%{_bindir}
cp ./bin/keda-admission-webhooks %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-adapter
%{_bindir}/%{name}-admission-webhooks

%changelog
* Wed Jan 29 2025 <osamaesmail@microsoft.com> - 2.14.1-3
- Add "generate_source_tarball.sh"
- Change vendor naming scheme to %%{name}-%%{version}-govendor-v%%{vendorVersion}.tar.gz

* Wed Jan 08 2025 <rohitrawat@microsoft.com> - 2.14.1-2
- Add patch for CVE-2024-45338

* Fri Sep 27 2024 Archana Choudhary <archana1@microsoft.com> - 2.14.1-1
- Upgrade to 2.14.1
- Fix CVE-2024-35255 in github.com/Azure/azure-sdk-for-go/sdk/azidentity 

* Thu Aug 01 2024 Bala <balakumaran.kannan@microsoft.com> - 2.14.0-2
- Added CVE-2024-6104.patch

* Mon May 06 2024 Sean Dougherty <sdougherty@microsoft.com> - 2.14.0-1
- Upgrade to 2.14.0 for Azure Linux 3.0
- Added keda-admission-webhooks binary, added to KEDA in v2.10.0

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.0-15
- Bump release to rebuild with go 1.20.10

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
