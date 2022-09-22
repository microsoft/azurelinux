Summary:        Container storage interface for logical volume management
Name:           csi-driver-lvm
Version:        0.5.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/metal-stack/csi-driver-lvm
Source0:        https://github.com/metal-stack/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated GO dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/metal-stack/%{name}/archive/refs/tags/v%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. go mod edit -go=1.17
#   6. go mod tidy
#   7. tar  --sort=name \
#           --mtime="2022-09-18 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-gocached.tar.gz .
Source1: %{name}-%{version}-gocached.tar.gz
BuildRequires: golang

%description
csi-driver-lvm utilizes local storage of Kubernetes nodes to provide persistent storage for pods

%prep
%setup -q
tar -xvf %{SOURCE1}

%build
%make_build

%install
install -d %{buildroot}%{_bindir}
install csi-driver-lvm %{buildroot}%{_bindir}/csi-driver-lvm

%files
%license LICENSE
%doc README.md
%{_bindir}/csi-driver-lvm

%changelog
* Thu Sep 22 2022 Lanze Liu <lanzeliu@microsoft.com> - 0.5.0-1
- Original version for CBL-Mariner
- License Verified
