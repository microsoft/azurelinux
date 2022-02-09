Name:           metal3-cluster-api-provider-metal3
Version:        0.4.0
Release:        1%{?dist}
Summary:        Cluster API Provider Metal3 enables users to deploy a Cluster API based cluster on top of bare metal infrastructure using Metal3.
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/metal3-io/cluster-api-provider-metal3

# Created using ./generate-sources.sh
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  golang >= 1.13

%description
The Cluster API brings declarative, Kubernetes-style APIs to cluster creation,
configuration and management. The API itself is shared across multiple cloud
providers. Cluster API Provider Metal3 is one of the providers for Cluster API
and enables users to deploy a Cluster API based cluster on top of bare metal
infrastructure using Metal3.

%prep
%autosetup

%build
export CGO_ENABLED=0
go build -mod=vendor -v -a -ldflags '-extldflags "-static"' -o %{name} .

%install
install -p -m 755 -t %{buildroot} %{name}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE
/%{name}

%changelog
* Thu Feb 09 2022 Vince Perri <viperri@microsoft.com> - 0.4.0-1
- Original version for CBL-Mariner.
