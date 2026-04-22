# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           tini
Version:        0.19.0
Release: 12%{?dist}
Summary:        A tiny but valid init for containers

License:        MIT
URL:            https://github.com/krallin/tini
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

%if 0%{?el7}
BuildRequires:  cmake3
%else
BuildRequires:  cmake
%endif
BuildRequires:  gcc
BuildRequires:  glibc-static
BuildRequires:  sed

%description
Tini is the simplest init you could think of.

All Tini does is spawn a single child (Tini is meant to be run in a container),
and wait for it to exit all the while reaping zombies and performing signal
forwarding.

%package        static
Summary:        Standalone static build of %{name}
%description    static
This package contains a standalone static build of %{name}, meant to be used
inside a container.

%prep
%autosetup
# Do not strip binaries
sed -i CMakeLists.txt -e 's/ -Wl,-s//'

%build
%if 0%{?el7}
%cmake3
%cmake3_build
%else
%cmake
%cmake_build
%endif

%install
%if 0%{?el7}
%cmake3_install
%else
%cmake_install
%endif

%files
%license LICENSE
%doc README.md
%{_bindir}/tini

%files static
%license LICENSE
%doc README.md
%{_bindir}/tini-static

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.19.0-2
- Use cmake3 on el7

* Sun Jun 13 2021 Davide Cavalca <dcavalca@fedoraproject.org> - 0.19.0-1
- Initial package
