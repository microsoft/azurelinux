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
#Source0:       https://github.com/coredns/coredns/archive/v%%{version}.tar.gz
Source0:        aad-pod-identity-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         modify-go-build-option.patch

BuildRequires:  golang >= 1.15

%description
NMI is the resource that is used when your pods look to use their identity.

%prep
%setup -q -c -n aad-pod-identity-%{version}
cd aad-pod-identity-1.7.0
%patch0 -p1

%build
cd aad-pod-identity-%{version}
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner

make build-nmi

%install
cd aad-pod-identity-1.7.0
install -m 755 -d %{buildroot}/bin
install -m 755 ./bin/aad-pod-identity/nmi %{buildroot}/bin
cp LICENSE ..

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE
/bin/%{name}

%changelog
* Thu Jun 24 2021 Henry Li <lihl@microsoft.com> - 1.7.0-1
- Original version for CBL-Mariner.
