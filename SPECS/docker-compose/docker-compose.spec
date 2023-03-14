Summary:        Define and run multi-container applications with Docker
Name:           docker-compose
Version:        2.16.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Tools/Container
URL:            https://github.com/docker/compose
Source0:        https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated GO dependencies from this tarball, since network is disabled during build time.
#   1. wget https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz -o %{name}-%{version}.tar.gz
#   2. tar -xf %{name}-%{version}.tar.gz
#   3. cd %{name}-%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2023-03-17 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %{name}-%{version}-govendor-vX.tar.gz vendor
# NOTE: govendor-v1 format is for inplace CVE updates so that we do not have to overwrite in the blob-store.
# After fixing any possible CVE for the vendored source, we must bump v1 -> v2
Source1:        %{name}-%{version}-govendor-v1.tar.gz
BuildRequires:  golang

%description
Compose is a tool for defining and running multi-container Docker applications.
With Compose, you use a YAML file to configure your application’s services.
Then, with a single command, you create and start all the services from your
configuration.

%prep
%autosetup -n compose-%{version}
%setup -q -n compose-%{version} -T -D -a 1

%build
go build \
	   -mod=vendor \
	   -trimpath \
	   -tags e2e \
	   -ldflags "-w -X github.com/docker/compose/v2/internal.Version=%{version}" \
	   -o ./bin/build/%{name} ./cmd

%install
mkdir -p %{buildroot}%{_bindir}
install -D -m0755 bin/build/docker-compose %{buildroot}%{_bindir}/

%files
%license LICENSE
%{_bindir}/docker-compose

%changelog
* Tue Mar 14 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 2.16.0-1
- Original version for CBL-Mariner
- License Verified
