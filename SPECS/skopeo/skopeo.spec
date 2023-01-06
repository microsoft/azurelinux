Summary:        Inspect container images and repositories on registries
Name:           skopeo
Version:        1.9.1
Release:        5%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/containers/skopeo
Source0:        https://github.com/containers/skopeo/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
BuildRequires:  btrfs-progs-devel
BuildRequires:  device-mapper-devel
BuildRequires:  go-md2man
BuildRequires:  golang >= 1.17.9
BuildRequires:  gpgme-devel
BuildRequires:  libassuan-devel
BuildRequires:  pkgconfig
Requires:       libcontainers-common

%description
Command line utility to inspect images and repositories directly on Docker
registries without the need to pull them.

%prep
%setup -q

%build
tar --no-same-owner -xf %{SOURCE0}
export GOPATH=%{our_gopath}
make

%install
make PREFIX=%{buildroot}%{_prefix} install-binary install-docs

%check
make test-unit-local
./bin/skopeo --version

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%%{name}*

%changelog
* Fri Jan 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.1-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.9.1-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.1-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.1-2
- Bump release to rebuild against Go 1.18.5

* Tue Jul 26 2022 Tom Fay <tomfay@microsoft.com> - 1.9.1-1
- Original version for CBL-Mariner.
- License verified.
