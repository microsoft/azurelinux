Summary:        A tiny but valid init for containers
Name:           tini
Version:        0.19.0
Release:        11%{?dist}
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
BuildRequires:  glibc-static >= 2.35-6%{?dist}
BuildRequires:  kernel-headers
BuildRequires:  make
BuildRequires:  sed

%description
Tini is the simplest init you could think of.

All Tini does is spawn a single child (Tini is meant to be run in a container),
and wait for it to exit all the while reaping zombies and performing signal
forwarding.

%package static
Summary:        Standalone static build of tini
# `docker-init` used to be provided by `tini` it's now provided by `tini-static`
# `tini` and `tini-static` are co-installable so long as both are newer than
# that change.
Conflicts:      %{name} <= 0.19.0-6
Provides:       docker-init = %{version}-%{release}

%description static
This package contains a standalone static build of tini, meant to be used
inside a container.

%prep
%autosetup
# Do not strip binaries
sed -i CMakeLists.txt -e 's/ -Wl,-s//'
# Enable static-pie (ASLR) support for tini-static
sed -i CMakeLists.txt -e 's/ -static/ -static-pie/'

%build
mkdir build && cd build
%cmake ..
%make_build

%install
%make_install -C build
# Ensure we're providing a static `docker-init`
ln -s %{_bindir}/tini-static %{buildroot}%{_bindir}/docker-init

%files
%license LICENSE
%doc README.md
%{_bindir}/tini

%files static
%license LICENSE
%doc README.md
%{_bindir}/tini-static
%{_bindir}/docker-init

%changelog
* Wed Oct 04 2023 Minghe Ren <mingheren@microsoft.com> - 0.19.0-11
- Bump release to rebuild against glibc 2.35-6

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.19.0-10
- Bump release to rebuild against glibc 2.35-5

* Wed Jul 05 2023 Andrew Phelps <anphel@microsoft.com> - 0.19.0-9
- Bump release to rebuild against glibc 2.35-4

* Tue Sep 13 2022 Andy Caldwell <andycaldwell@microsoft.com> - 0.19.0-8
- Rebuilt for glibc-static 2.35-3

* Mon Feb 21 2022 Andy Caldwell <andycaldwell@microsoft.com> - 0.19.0-7
- Re-enable `tini-static` package
- Enable binary hardening flag (`-static-pie`)

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
