Summary:        Cluster API Provider Metal3 enables users to deploy a Cluster API based cluster on top of bare metal infrastructure using Metal3.
Name:           metal3-cluster-api-provider-metal3
Version:        0.4.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/metal3-io/cluster-api-provider-metal3
#Source0:       https://github.com/metal3-io/cluster-api-provider-metal3/archive/refs/tags/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
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

BuildRequires:  golang >= 1.13

%description
The Cluster API brings declarative, Kubernetes-style APIs to cluster creation,
configuration and management. The API itself is shared across multiple cloud
providers. Cluster API Provider Metal3 is one of the providers for Cluster API
and enables users to deploy a Cluster API based cluster on top of bare metal
infrastructure using Metal3.

%prep
%autosetup

%check
source ./hack/fetch_ext_bins.sh
fetch_tools
setup_envs
go test -v ./api/... ./controllers/... ./baremetal/...

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
* Thu Feb 09 2022 Vince Perri <viperri@microsoft.com> - 0.4.0-1
- Original version for CBL-Mariner.
- License verified
