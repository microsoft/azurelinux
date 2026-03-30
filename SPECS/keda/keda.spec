Summary:        Kubernetes-based Event Driven Autoscaling
Name:           keda
Version:        2.14.1
Release:        11%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/kedacore/keda
#Source0:       https://github.com/kedacore/%%{name}/archive/refs/tags/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/kedacore/%%{name}/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         CVE-2024-6104.patch
Patch1:         CVE-2024-45338.patch
Patch2:         CVE-2025-27144.patch
Patch3:         CVE-2025-22868.patch
Patch4:         CVE-2025-29786.patch
Patch5:         CVE-2025-30204.patch
Patch6:         CVE-2025-29923.patch
Patch7:         CVE-2025-22870.patch
Patch8:         CVE-2024-51744.patch
Patch9:         CVE-2025-22872.patch
Patch10:        CVE-2025-68156.patch
Patch11:        CVE-2025-68476.patch
Patch12:        CVE-2025-11065.patch
Patch13:        CVE-2025-47911.patch
Patch14:        CVE-2025-58190.patch
Patch15:        CVE-2026-2303.patch
BuildRequires:  golang >= 1.15

%description
KEDA is a Kubernetes-based Event Driven Autoscaling component. 
It provides event driven scale for any container running in Kubernetes 

%prep
%autosetup -p1 -a1

%build
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
* Thu Feb 19 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.14.1-11
- Patch for CVE-2026-2303, CVE-2025-58190, CVE-2025-47911

* Tue Feb 03 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.14.1-10
- Patch for CVE-2025-11065

* Fri Jan 02 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.14.1-9
- Patch for CVE-2025-68476

* Fri Dec 19 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.14.1-8
- Patch for CVE-2025-68156

* Fri Apr 25 2025 Kanishk Bansal <kanbansal@microsoft.com> - 2.14.1-7
- Patch CVE-2025-22872

* Thu Apr 17 2025 Sudipta Pandit <sudpandit@microsoft.com> - 2.14.1-6
- Fixes an incorrect patch introduced with the patch for CVE-2025-29923
- Fixes patches being overridden during the build step
- Fixes CVE-2025-22870 and CVE-2024-51744

* Sun Mar 30 2025 Kanishk Bansal <kanbansal@microsoft.com> - 2.14.1-5
- Patch CVE-2025-30204, CVE-2025-29923

* Mon Mar 24 2025 Kshitiz Godara <kgodara@microsoft.com> - 2.14.1-4
- Fix CVE-2025-29786 with an upstream patch

* Mon Mar 03 2025 Kanishk Bansal <kanbansal@microsoft.com> - 2.14.1-3
- Fix CVE-2025-27144, CVE-2025-22868 with an upstream patch

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
