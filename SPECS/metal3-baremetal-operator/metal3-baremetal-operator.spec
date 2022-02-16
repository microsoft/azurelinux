Summary:        Bare Metal Operator implements a Kubernetes API for managing bare metal hosts
Name:           metal3-baremetal-operator
Version:        0.5.4
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/metal3-io/baremetal-operator
Source0:        https://github.com/metal3-io/baremetal-operator/archive/refs/tags/capm3-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# The source is the upstream tarball with the vendor dir (created using
# "go mod vendor") included for offline builds and its top-level directory
# renamed to %%{name}-%%{version}. It is then repackaged as a tar using the
# following command:
#
#   tar \
#     --mtime="1970-01-01 00:00Z" \
#     --sort=name \
#     --owner=0 \
#     --group=0 \
#     --numeric-owner \
#     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#     -cf %%{name}-%%{version}.tar.gz \
#     %%{name}-%%{version}
#
# This command creates a tar with the same cryptographic hash regardless of time
# or environment. See https://reproducible-builds.org/docs/archives/. It can be
# recreated using ./generate-sources.sh.

BuildRequires:  golang >= 1.17

%description
The Bare Metal Operator implements a Kubernetes API for managing bare metal
hosts. It maintains an inventory of available hosts as instances of the
BareMetalHost Custom Resource Definition. The Bare Metal Operator knows how to
inspect the host's hardware details and report them on the corresponding
BareMetalHost, provision hosts with a desired image, and clean a host's disk
contents before or after provisioning.

%prep
%autosetup

%build
export CGO_ENABLED=0
go build -mod=vendor -v -a -ldflags '-extldflags "-static"' -o %{name} .

%install
install -p -m 755 -t %{buildroot} %{name}

%files
%defattr(-,root,root)
%license LICENSE
/%{name}

%changelog
* Thu Feb 09 2022 Vince Perri <viperri@microsoft.com> - 0.5.4-1
- Original version for CBL-Mariner.
- License verified
