Summary:        A WPE backend designed for Linux desktop systems
Name:           wpebackend-fdo
Version:        1.12.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/Igalia/%{name}
Source0:        https://github.com/Igalia/WPEBackend-fdo/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  glib2-devel
BuildRequires:  libepoxy-devel
BuildRequires:  libwpe-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  meson
BuildRequires:  wayland-devel

%description
A WPE backend designed for Linux desktop systems.

%package       devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description   devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%prep
%autosetup -p1 -n WPEBackend-fdo-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
meson --prefix=%{_prefix} --buildtype=release .. && \
ninja
popd

%install
cd %{_target_platform}
DESTDIR=%{buildroot}/ ninja install

%files
%license COPYING
%doc NEWS
%{_libdir}/libWPEBackend-fdo-1.0.so.1
%{_libdir}/libWPEBackend-fdo-1.0.so.1.*
%{_libdir}/libWPEBackend-fdo-1.0.so

%files devel
%{_includedir}/wpe-fdo-1.0
%{_libdir}/pkgconfig/wpebackend-fdo-1.0.pc

%changelog
* Sat May 14 2022 Sriram Nambakam <snambakam@microsoft.com> - 1.12.0-1
- Update to 1.12.0
- License verified
- Use meson and ninja instead of cmake

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Mar 12 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Tue Mar 03 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 1.5.90-2
- Rebuild against updated libwpe

* Tue Mar 03 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 1.5.90-1
- Update to 1.5.90

* Mon Feb 24 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Chris King <bunnyapocalypse@protonmail.com> - 1.4.0-2
- Change location of libWPEBackend-fdo.so to allow for WPE backend

* Wed Sep 18 2019 Chris King <bunnyapocalypse@protonmail.com> - 1.4.0-1
- New version

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 17 2019 Chris King <bunnyapocalypse@protonmail.com> - 1.3.1-1
- New version

* Sat May 11 2019 Chris King <bunnyapocalypse@protonmail.com> - 1.3.0-1
- New version

* Mon Mar 25 2019 Chris King <bunnyapocalypse@protonmail.com> - 1.2.0-1
- New version

* Thu Feb 28 2019 Pete Walter <pwalter@fedoraproject.org> - 1.1.90-2
- Update wayland deps

* Tue Feb 26 2019 Chris King <bunnyapocalypse@protonmail.com> - 1.1.90-1
- New version with soname bump

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 26 2018 Chris King <bunnyapocalypse@protonmail.com> - 1.0.0-1
- Soname bump

* Mon Jul 16 2018 Chris King <bunnyapocalypse@fedoraproject.org> - 0.1-1
- Initial RPM package
