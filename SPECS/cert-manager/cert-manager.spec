Summary:        Automatically provision and manage TLS certificates in Kubernetes
Name:           cert-manager
Version:        1.11.2
Release:        6%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/jetstack/cert-manager
Source0:        https://github.com/jetstack/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated GO dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/jetstack/%%{name}/archive/refs/tags/v%%{version}.tar.gz -o %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-govendor.tar.gz vendor
Source1:        %{name}-%{version}-govendor.tar.gz
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
%autosetup -p1
%setup -q -T -D -a 1

%build
go build -o bin/acmesolver cmd/acmesolver/main.go
go build -o bin/cainjector cmd/cainjector/main.go
go build -o bin/controller cmd/controller/main.go
go build -o bin/cmctl cmd/ctl/main.go
go build -o bin/webhook cmd/webhook/main.go

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
