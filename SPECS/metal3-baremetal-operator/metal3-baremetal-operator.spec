Name:           metal3-baremetal-operator
Version:        0.4.0
Release:        1%{?dist}
Summary:        Bare Metal Operator implements a Kubernetes API for managing bare metal hosts
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/metal3-io/baremetal-operator

# Created using ./generate-sources.sh
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  golang >= 1.14

%description
The Bare Metal Operator implements a Kubernetes API for managing bare metal
hosts.  It maintains an inventory of available hosts as instances of the
BareMetalHost Custom Resource Definition. The Bare Metal Operator knows how to
inspect the host's hardware details and report them on the corresponding
BareMetalHost, provision hosts with a desired image, and clean a host's disk
contents before or after provisioning.

%prep
%autosetup

%build
export GO111MODULE=on
export GOFLAGS=
go build -mod=vendor -v -ldflags '-extldflags "-static" -X "github.com/metal3-io/baremetal-operator/pkg/version.Raw=capm3-v%{version}"' -o %{name} cmd/manager/main.go

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
