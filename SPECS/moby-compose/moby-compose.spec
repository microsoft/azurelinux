Summary:        Define and run multi-container applications with Docker
Name:           moby-compose
Version:        2.17.3
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Tools/Container
URL:            https://github.com/docker/compose
Source0:        https://github.com/docker/compose/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         CVE-2023-44487.patch
# Patch can be removed when grpc go module is updated to version v1.62.0, patches backported to v1.50.0
# These are the patches backported in order to get access to the security fix
# https://github.com/grpc/grpc-go/commit/6eabd7e1834e47b20f55cbe9d473fc607c693358
# https://github.com/grpc/grpc-go/commit/8eb4ac4c1514c190ee0b5d01a91c63218dac93c0
# https://github.com/grpc/grpc-go/commit/f2180b4d5403d2210b30b93098eb7da31c05c721
Patch1:         patch-server.go-to-support-single-serverWorkerChannel.patch
Patch2:         Change-server-stream-context-handling.patch
Patch3:         prohibit-more-than-MaxConcurrentStreams-handlers.patch

# Leverage the `generate_source_tarball.sh` to create the vendor sources
# NOTE: govendor-v1 format is for inplace CVE updates so that we do not have to overwrite in the blob-store.
# After fixing any possible CVE for the vendored source, we must bump v1 -> v2
Source1:        %{name}-%{version}-govendor-v1.tar.gz
BuildRequires:  golang
Requires:       moby-cli


%description
Compose is a tool for defining and running multi-container Docker applications.
With Compose, you use a YAML file to configure your application’s services.
Then, with a single command, you create and start all the services from your
configuration.

%prep
%autosetup -N -n compose-%{version}
# Apply vendor before patching
%setup -q -n compose-%{version} -T -D -a 1
%autopatch -p1

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
* Wed Mar 20 2024 Henry Beberman <henry.beberman@microsoft.com> - 2.17.3-2
- Correct license to ASL 2.0

* Wed Feb 21 2024 Sam Meluch <sammeluch@microsoft.com> - 2.17.3-1
- Upgrade to version 2.17.3
- Add patch for vendored golang.org/grpc

* Fri Feb 02 2024 Daniel McIlvaney <damcilva@microsoft.com> - 2.17.2-7
- Address CVE-2023-44487 by patching vendored golang.org/x/net

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.17.2-6
- Bump release to rebuild with go 1.20.9

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
