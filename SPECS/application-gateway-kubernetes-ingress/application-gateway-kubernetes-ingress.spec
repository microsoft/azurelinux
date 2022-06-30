%global debug_package %{nil}
Summary:        Application Gateway Ingress Controller
Name:           application-gateway-kubernetes-ingress
Version:        1.4.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Networking
URL:            https://github.com/Azure/application-gateway-kubernetes-ingress
#Source0:       https://github.com/Azure/application-gateway-kubernetes-ingress/archive/refs/tags/1.4.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using vendored Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/Azure/%%{name}/archive/refs/tags/%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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

BuildRequires:  golang >= 1.13

%description
This is an ingress controller that can be run on Azure Kubernetes Service (AKS) to allow an Azure Application Gateway 
to act as the ingress for an AKS cluster. 

%prep
%autosetup

%build
rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner

export VERSION=%{version}
export VERSION_PATH=github.com/Azure/application-gateway-kubernetes-ingress/pkg/version

go build -ldflags "-s -X $VERSION_PATH.Version=$VERSION" -mod=vendor -v -o appgw-ingress ./cmd/appgw-ingress

%install
mkdir -p %{buildroot}%{_bindir}
cp appgw-ingress %{buildroot}%{_bindir}/


%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/appgw-ingress

%changelog
* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.4.0-2
- Bump release to rebuild with golang 1.18.3

* Mon Jul 12 2021 Henry Li <lihl@microsoft.com> - 1.4.0-1
- Original version for CBL-Mariner.
- License Verified.
