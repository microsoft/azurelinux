%global debug_package %{nil}
Summary:        Node Managed Identity
Name:           nmi
Version:        1.7.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/Azure/aad-pod-identity
#Source0:       https://github.com/Azure/aad-pod-identity/archive/refs/tags/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
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
make unit-test

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}

%changelog
* Thu Jun 24 2021 Henry Li <lihl@microsoft.com> -1.7.0-1
- Original version for CBL-Mariner