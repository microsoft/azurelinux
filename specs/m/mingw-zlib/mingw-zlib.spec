# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global mingw_build_ucrt64 1
%{?mingw_package_header}

Name:           mingw-zlib
Version:        1.3.1
Release: 7%{?dist}
Summary:        MinGW Windows zlib compression library

License:        Zlib
URL:            https://www.zlib.net/
Source0:        https://www.zlib.net/zlib-%{version}.tar.xz
# Use UNIX naming convention for libraries
Patch0:         mingw-zlib-cmake.patch

BuildArch:      noarch

BuildRequires:  cmake
BuildRequires:  make

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc

BuildRequires:  ucrt64-filesystem >= 95
BuildRequires:  ucrt64-gcc


%description
MinGW Windows zlib compression library.


# Win32
%package -n mingw32-zlib
Summary:        MinGW Windows zlib compression library for the win32 target

%description -n mingw32-zlib
MinGW Windows zlib compression library for the win32 target.


%package -n mingw32-zlib-static
Summary:        Static libraries for mingw32-zlib development.
Requires:       mingw32-zlib = %{version}-%{release}

%description -n mingw32-zlib-static
The mingw32-zlib-static package contains static library for mingw32-zlib development.


# Win64
%package -n mingw64-zlib
Summary:        MinGW Windows zlib compression library for the win64 target

%description -n mingw64-zlib
MinGW Windows zlib compression library for the win64 target.

%package -n mingw64-zlib-static
Summary:        Static libraries for mingw64-zlib development
Requires:       mingw64-zlib = %{version}-%{release}

%description -n mingw64-zlib-static
The mingw64-zlib-static package contains static library for mingw64-zlib development.


# UCRT64
%package -n ucrt64-zlib
Summary:        MinGW Windows zlib compression library for the ucrt64 target

%description -n ucrt64-zlib
MinGW Windows zlib compression library for the ucrt64 target.

%package -n ucrt64-zlib-static
Summary:        Static libraries for ucrt64-zlib development
Requires:       ucrt64-zlib = %{version}-%{release}

%description -n ucrt64-zlib-static
The ucrt64-zlib-static package contains static library for ucrt64-zlib development.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n zlib-%{version}


%build
MINGW32_CMAKE_ARGS=-DINSTALL_PKGCONFIG_DIR=%{mingw32_libdir}/pkgconfig \
MINGW64_CMAKE_ARGS=-DINSTALL_PKGCONFIG_DIR=%{mingw64_libdir}/pkgconfig \
UCRT64_CMAKE_ARGS=-DINSTALL_PKGCONFIG_DIR=%{ucrt64_libdir}/pkgconfig \
%mingw_cmake
%mingw_make_build
%mingw_make_build


%install
%mingw_make_install

# Drop the man pages
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}
rm -rf %{buildroot}%{ucrt64_mandir}


# Win32
%files -n mingw32-zlib
%{mingw32_includedir}/zconf.h
%{mingw32_includedir}/zlib.h
%{mingw32_libdir}/libz.dll.a
%{mingw32_bindir}/zlib1.dll
%{mingw32_libdir}/pkgconfig/zlib.pc

%files -n mingw32-zlib-static
%{mingw32_libdir}/libz.a

# Win64
%files -n mingw64-zlib
%{mingw64_includedir}/zconf.h
%{mingw64_includedir}/zlib.h
%{mingw64_libdir}/libz.dll.a
%{mingw64_bindir}/zlib1.dll
%{mingw64_libdir}/pkgconfig/zlib.pc

%files -n mingw64-zlib-static
%{mingw64_libdir}/libz.a

# UCRT64
%files -n ucrt64-zlib
%{ucrt64_includedir}/zconf.h
%{ucrt64_includedir}/zlib.h
%{ucrt64_libdir}/libz.dll.a
%{ucrt64_bindir}/zlib1.dll
%{ucrt64_libdir}/pkgconfig/zlib.pc

%files -n ucrt64-zlib-static
%{ucrt64_libdir}/libz.a


%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 29 2024 Jonathan Schleifer <js@nil.im> - 1.3.1-2
- Build UCRT64 package

* Wed Jan 31 2024 Sandro Mani <manisandro@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Sandro Mani <manisandro@gmail.com> - 1.2.13-1
- Update to 1.2.13

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Sandro Mani <manisandro@gmail.com> - 1.2.12-1
- Update to 1.2.12

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.2.11-8
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Sandro Mani <manisandro@gmail.com> - 1.2.11-4
- Drop minizip subpackages, it's a separate package now

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.2.11-1
- Update to 1.2.11

* Tue Aug 06 2019 Thomas Sailer <t.sailer@alumni.ethz.ch> - 1.2.8-12
- update pkgconf file version to 1.2.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.8-1
- Update to 1.2.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.7-1
- Update to 1.2.7

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.5-10
- Added win64 support
- Simplified the build process by using autotools and a hacked version of libtool
- Made the package compliant with the new MinGW packaging guidelines

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.2.5-9
- Renamed the source package to mingw-zlib (#800415)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Kalev Lember <kalevlember@gmail.com> - 1.2.5-8
- Remove the .la files
- Spec clean up

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.5-7
- Rebuild against the mingw-w64 toolchain
- Use the correct RPM macros
- Fix FTBFS against the latest binutils caused by the use of an invalid .def file

* Fri Feb 17 2012 David Tardon <dtardon@redhat.com> - 1.2.5-6
- fix dlname in libz.la

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May 10 2011 Kalev Lember <kalev@smartlink.ee> - 1.2.5-4
- Use the built .pc file instead of manually generating it

* Tue Apr 26 2011 Kalev Lember <kalev@smartlink.ee> - 1.2.5-3
- Install zlib pkgconfig file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.5-1
- Update to 1.2.5
- Use %%global instead of %%define
- Automatically generate debuginfo subpackage
- Use correct %%defattr tag
- Merged the changes from the native Fedora package

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-18
- Cannot copy current directory into itself, so fix the copy command
  which creates 'x' subdirectory.

* Fri May  1 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 1.2.3-17
- BR autoconf, automake, libtool

* Thu Apr 30 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 1.2.3-16
- use autotools build system from native package

* Tue Mar  3 2009 W. Pilorz <wpilorz at gmail.com> - 1.2.3-15
- Add static subpackage.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-13
- Rebuild for mingw32-gcc 4.4

* Mon Jan 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-12
- Force rebuild to test maintenance account.

* Thu Dec 18 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-11
- Pass correct CFLAGS to build.

* Thu Oct 16 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-10
- Consider native patches.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-9
- Rename mingw -> mingw32.

* Sun Sep 21 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-8
- Remove manpage.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-7
- Remove static library.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-5
- Fix misnamed file: zlibdll.a -> zlib.dll.a
- Explicitly provide mingw(zlib1.dll).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-3
- Initial RPM release, largely based on earlier work from several sources.
