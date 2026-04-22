# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-libepoxy
Version:        1.5.10
Release: 10%{?dist}
Summary:        MinGW Windows libepoxy library

License:        MIT
URL:            https://github.com/anholt/libepoxy
Source0:        https://github.com/anholt/libepoxy/releases/download/%{version}/libepoxy-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw64-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-angleproject
BuildRequires:  mingw64-angleproject

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  python3

%description
Epoxy is a library for handling OpenGL function pointer management.

This package contains the MinGW Windows cross compiled libepoxy library.


%package -n mingw32-libepoxy
Summary:        MinGW Windows libepoxy library
Requires:       mingw32-angleproject

%description -n mingw32-libepoxy
Epoxy is a library for handling OpenGL function pointer management.

This package contains the MinGW Windows cross compiled libepoxy library.


%package -n mingw64-libepoxy
Summary:        MinGW Windows libepoxy library
Requires:       mingw64-angleproject

%description -n mingw64-libepoxy
Epoxy is a library for handling OpenGL function pointer management.

This package contains the MinGW Windows cross compiled libepoxy library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n libepoxy-%{version}


%build
%mingw_meson -Degl=yes
%mingw_ninja


%install
%mingw_ninja_install


%files -n mingw32-libepoxy
%license COPYING
%{mingw32_bindir}/libepoxy-0.dll
%{mingw32_libdir}/libepoxy.dll.a
%{mingw32_libdir}/pkgconfig/epoxy.pc
%{mingw32_includedir}/epoxy/

%files -n mingw64-libepoxy
%license COPYING
%{mingw64_bindir}/libepoxy-0.dll
%{mingw64_libdir}/libepoxy.dll.a
%{mingw64_libdir}/pkgconfig/epoxy.pc
%{mingw64_includedir}/epoxy/

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Kalev Lember <klember@redhat.com> - 1.5.10-2
- Add missing runtime requires on mingw-angleproject

* Wed Jan 04 2023 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.5.10-1
- Update to 1.5.10
- Enable egl thanks to ANGLE

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.5.9-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Aug 15 2021 Sandro Mani <manisandro@gmail.com> - 1.5.9-1
- Update to 1.5.9

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Sandro Mani <manisandro@gmail.com> - 1.5.8-1
- Update to 1.5.8

* Sat May 01 2021 Sandro Mani <manisandro@gmail.com> - 1.5.7-1
- Update to 1.5.7

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Sandro Mani <manisandro@gmail.com> - 1.5.5-1
- Update to 1.5.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 26 2019 Sandro Mani <manisandro@gmail.com> - 1.5.4-1
- Update to 1.5.4

* Wed Aug 28 2019 Sandro Mani <manisandro@gmail.com> - 1.5.3-1
- Update to 1.5.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 23 2018 Christophe Fergeau <cfergeau@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.4.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Kalev Lember <klember@redhat.com> - 1.4.3-1
- Update to 1.4.3

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Kalev Lember <klember@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May 07 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.3.1-3
- Add BuildRequires: python to fix FTBFS

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 05 2015 Kalev Lember <klember@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 1.2-2
- Package review fixes (#1205194)
- Don't explicitly BR mingw{32,64}-binutils
- Fix the license tag

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 1.2-1
- Initial Fedora packaging
