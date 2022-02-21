Summary:        A tiny but valid init for containers
Name:           tini
Version:        0.19.0
Release:        7%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/krallin/tini
Source0:        https://github.com/krallin/tini/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  binutils
BuildRequires:  cmake
BuildRequires:  diffutils
BuildRequires:  file
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers
BuildRequires:  make
BuildRequires:  sed
Provides:       docker-init = %{version}-%{release}

%description
Tini is the simplest init you could think of.

All Tini does is spawn a single child (Tini is meant to be run in a container),
and wait for it to exit all the while reaping zombies and performing signal
forwarding.

%package static
Summary:        Standalone static build of tini

%description static
This package contains a standalone static build of tini, meant to be used
inside a container.

%prep
%autosetup
# Do not strip binaries
sed -i CMakeLists.txt -e 's/ -Wl,-s//'
# Enable static-pie (ASLR) support for tini-static
# TODO:  glibc-devel does not contain rcrt1.o so -static-pie linkage fails
# sed -i CMakeLists.txt -e 's/ -static/ -static-pie/'
# Enable RELRO NOW for all binaries
sed -i CMakeLists.txt -e 's/ -Wl,-z,relro/ -Wl,-z,relro,-z,now/'

%build
mkdir build && cd build
%cmake ..
%make_build

%install
%make_install -C build
# Ensure we're providing docker-init
ln -s %{_bindir}/tini %{buildroot}%{_bindir}/docker-init

%files
%license LICENSE
%doc README.md
%{_bindir}/tini
%{_bindir}/docker-init

%files static
%license LICENSE
%doc README.md
%{_bindir}/tini-static

%changelog
* Mon Feb 21 2022 Andy Caldwell <andycaldwell@microsoft.com> - 0.19.0-7
- Re-enable `tini-static` package
- Enable binary hardening flags (`-z relro -z now`)

* Mon Feb 07 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 0.19.0-6
- Makes moby-engine spec relying on tini to provide docker-init

* Thu Nov 04 2021 Max Brodeur-Urbas <maxbr@microsoft.com> - 0.19.0-5
- Removed static tini package

* Wed Aug 18 2021 Tom Fay <tomfay@microsoft.com> - 0.19.0-4
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- License verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.19.0-2
- Use cmake3 on el7

* Sun Jun 13 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.19.0-1
- Initial package
