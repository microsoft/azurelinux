%global debug_package %{nil}
Summary:        Node Managed Identity
Name:           nmi
Version:        1.8.7
Release:        15%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/Azure/aad-pod-identity
#Source0:       https://github.com/Azure/aad-pod-identity/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/Azure/aad-pod-identity/archive/refs/tags/v%%{version}.tar.gz -O aad-pod-identity-%%{version}.tar.gz
#   2. tar -xf aad-pod-identity-%%{version}.tar.gz
#   3. cd aad-pod-identity-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         modify-go-build-option.patch
BuildRequires:  golang >= 1.15

%description
NMI is the resource that is used when your pods look to use their identity.

%prep
%autosetup -c -N -n %{name}-%{version}
pushd aad-pod-identity-%{version}
%patch0 -p1
popd

%build
pushd aad-pod-identity-%{version}

# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner

make build-nmi
popd

%install
mkdir -p %{buildroot}%{_bindir}
pushd aad-pod-identity-%{version}
cp ./bin/aad-pod-identity/nmi %{buildroot}%{_bindir}
cp LICENSE ..
popd

%check
pushd aad-pod-identity-%{version}
make unit-test
popd

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-15
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.8.7-14
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-13
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-12
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-11
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.7-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.8.7-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.7-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.7-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.8.7-2
- Bump release to rebuild with golang 1.18.3

* Thu Feb 10 2022 Henry Li <lihl@microsoft.com> - 1.8.7-1
- Upgrade to version 1.8.7
- Update modify-go-build-option.patch
- License Verified

* Thu Jun 24 2021 Henry Li <lihl@microsoft.com> - 1.7.0-1
- Original version for CBL-Mariner