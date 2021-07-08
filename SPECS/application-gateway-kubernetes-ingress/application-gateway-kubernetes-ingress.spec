Summary:        Application Gateway Ingress Controller
Name:           application-gateway-kubernetes-ingress
Version:        1.4.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Networking
URL:            https://github.com/Azure/application-gateway-kubernetes-ingress
#Source0:       https://github.com/Azure/application-gateway-kubernetes-ingress/archive/refs/tags/1.4.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
Patch0:         Use-mariner-container.patch

#BuildRequires:  golang >= 1.13
#BuildRequires:  helm
#BuildRequires:  ca-certificates
#BuildRequires:  openssl
#BuildRequires:  cmake

%description
This is an ingress controller that can be run on Azure Kubernetes Service (AKS) to allow an Azure Application Gateway 
to act as the ingress for an AKS cluster. 

%prep
%autosetup -p1

%build
chmod u+x ./scripts/build.sh
mkdir build && cd build
cmake ..
cmake --build . --target appgw-ingress

%install
mkdir -p %{buildroot}%{_bindir}
cp bin/appgw-ingress %{buildroot}%{_bindir}/

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/appgw-ingress

%changelog
* Fri Jul 02 2021 Henry Li <lihl@microsoft.com> - 1.4.0-1
- Original version for CBL-Mariner.
