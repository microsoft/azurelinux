Summary:        Define and run multi-container applications with Docker
Name:           docker-compose
Version:        2.27.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Tools/Container
URL:            https://github.com/docker/compose
Source0:        https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Leverage the `generate_source_tarball.sh` to create the vendor sources
# NOTE: govendor-v1 format is for inplace CVE updates so that we do not have to overwrite in the blob-store.
# After fixing any possible CVE for the vendored source, we must bump v1 -> v2
Source1:        %{name}-%{version}-govendor-v1.tar.gz
BuildRequires:  golang
Requires:       docker-cli
Obsoletes:      moby-compose < %{version}-%{release}
Provides:       moby-compose = %{version}-%{release}


%description
Compose is a tool for defining and running multi-container Docker applications.
With Compose, you use a YAML file to configure your application’s services.
Then, with a single command, you create and start all the services from your
configuration.

%prep
%autosetup -p1 -n compose-%{version} -a 1

%build
go build \
	   -mod=vendor \
	   -trimpath \
	   -tags e2e \
	   -ldflags "-w -X github.com/docker/compose/v2/internal.Version=%{version}" \
	   -o ./bin/build/docker-compose ./cmd

%install
mkdir -p "%{buildroot}/%{_libexecdir}/docker/cli-plugins"
install -D -m0755 bin/build/docker-compose %{buildroot}/%{_libexecdir}/docker/cli-plugins

%files
%license LICENSE
%{_libexecdir}/docker/cli-plugins/docker-compose

%changelog
* Thu May 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.27.0-1
- Auto-upgrade to 2.27.0 - address CVE-2024-23653

* Wed Mar 20 2024 Henry Beberman <henry.beberman@microsoft.com> - 2.24.6-2
- Correct license to ASL 2.0

* Mon Feb 26 2024 Henry Beberman <henry.beberman@microsoft.com> - 2.24.6-1
- Rename spec from moby-compose to docker-compose
- Bump version to 2.24.6

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.17.2-6
- Bump release to rebuild with go 1.20.10

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 2.17.2-5
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.17.2-4
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.17.2-3
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.17.2-2
- Bump release to rebuild with go 1.19.10

* Tue Mar 14 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 2.17.2-1
- Original version for CBL-Mariner
- License Verified
