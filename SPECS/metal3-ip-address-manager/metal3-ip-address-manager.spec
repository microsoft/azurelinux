Name:           metal3-ip-address-manager
Version:        0.0.4
Release:        1%{?dist}
Summary:        IP Address Manager is a Kubernetes Controller that provides IP addresses and manages the allocations of IP subnets for the Cluster API Provider for Metal3.
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/metal3-io/ip-address-manager

# Created using ./generate-sources.sh
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  golang >= 1.13

%description
The IP Address Manager is a Kubernetes Controller that provides IP addresses and
manages the allocations of IP subnets for the Cluster API Provider for Metal3.

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
* Thu Feb 09 2022 Vince Perri <viperri@microsoft.com> - 0.0.4-1
- Original version for CBL-Mariner.
