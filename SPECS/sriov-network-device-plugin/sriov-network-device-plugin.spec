Summary:        Plugin for discovering and advertising networking resources
Name:           sriov-network-device-plugin
Version:        3.4.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/k8snetworkplumbingwg/sriov-network-device-plugin
Source0:        https://github.com/k8snetworkplumbingwg/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  golang

%description
sriov-network-device-plugin is Kubernetes device plugin for discovering and advertising networking
resources in the form of SR-IOV virtual functions and PCI physical functions

%prep
%autosetup -p1

%build
go build -mod vendor -o ./build/sriovdp ./cmd/sriovdp/

%install
install -D -m0755 build/sriovdp %{buildroot}%{_bindir}/sriovdp
install -D -m0755 images/entrypoint.sh %{buildroot}%{_bindir}/entrypoint.sh
install -D -m0755 images/ddptool-1.0.1.12.tar.gz %{buildroot}/usr/share/%{name}/ddptool-1.0.1.12.tar.gz

%files
%license LICENSE
%doc README.md
%{_bindir}/sriovdp
%{_bindir}/entrypoint.sh
/usr/share/%{name}/ddptool-1.0.1.12.tar.gz

%changelog
* Fri Sep 23 2022 Aditya Dubey <adityadubey@microsoft.com> - 3.4.0-1
- Original version for CBL-Mariner
- License Verified
