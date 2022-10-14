Summary:        Plugin for discovering and advertising networking resources 
Name:           sriov-network-device-plugin
Version:        3.4.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/k8snetworkplumbingwg/sriov-network-device-plugin
Source0:        https://github.com/k8snetworkplumbingwg/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

# Below is a manually created tarball, no download link.
# We're using pre-populated GO dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/k8snetworkplumbingwg/%{name}/archive/refs/tags/v%{version}.tar.gz -O %{name}-%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2022-10-10 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-govendor.tar.gz vendor

Source1:       %{name}-%{version}-govendor.tar.gz
Patch0:         sriovdp.patch
BuildRequires:  golang

%description
sriov-network-device-plugin is Kubernetes device plugin for discovering and advertising networking 
resources in the form of SR-IOV virtual functions and PCI physical functions 

%prep
%autosetup -p1
%setup -q -T -D -a 1

%build
make build

%install
install -D -m0755 build/sriovdp %{buildroot}%{_bindir}/sriovdp
install -D -m0755 images/entrypoint.sh %{buildroot}%{_bindir}/entrypoint.sh

%files
%license LICENSE
%doc README.md
%{_bindir}/sriovdp
%{_bindir}/entrypoint.sh

%changelog
* Thu Sep 23 2022 Aditya Dubey <adityadubey@microsoft.com> - 3.4.0-1
- Original version for CBL-Mariner
- License Verified
