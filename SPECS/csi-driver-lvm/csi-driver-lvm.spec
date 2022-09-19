Summary:        Container storage interface for logical volume management
Name:           csi-driver-lvm
Version:        0.4.1
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/metal-stack/csi-driver-lvm
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/metal-stack/%{name}/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}-govendorcached.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated GO dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/metal-stack/%{name}/archive/refs/tags/v%{version}.tar.gz -o %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2022-09-18 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-govendorcached.tar.gz .
BuildRequires:  golang

%description
csi-driver-lvm utilizes local storage of Kubernetes nodes to provide persistent storage for pods

%prep
%setup -q

%build
make %{?_smp_mflags}
%files
%license LICENSE
%doc README.md

%changelog
* Thu Sep 08 2022 Lanze Liu <lanzeliu@microsoft.com> 0.4.1.1
- Initial version of package csi-driver-lvm
- License Verified
