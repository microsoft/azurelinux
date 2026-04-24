# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-dbus
Version:        1.16.0
Release: 4%{?dist}
Summary:        MinGW Windows port of D-Bus

# The effective license of the majority of the package, including the shared
# library, is "GPL-2+ or AFL-2.1". Certain utilities are "GPL-2+" only.
License: (AFL-2.1 OR GPL-2.0-or-later) AND GPL-2.0-or-later
URL:            http://www.freedesktop.org/wiki/Software/dbus
Source0:        http://dbus.freedesktop.org/releases/dbus/dbus-%{version}.tar.xz

# Restore support for static libs
Patch0:         dbus-static-libs.patch

BuildArch:      noarch

BuildRequires:  cmake

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-glib2
BuildRequires:  mingw32-expat

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-glib2
BuildRequires:  mingw64-expat


%description
D-BUS is a system for sending messages between applications. It is
used both for the system wide message bus service, and as a
per-user-login-session messaging facility.


# Win32
%package -n mingw32-dbus
Summary:        MinGW Windows port of D-Bus
Requires:       pkgconfig

%description -n mingw32-dbus
D-BUS is a system for sending messages between applications. It is
used both for the system wide message bus service, and as a
per-user-login-session messaging facility.


%package -n mingw32-dbus-static
Summary:        Static version of MinGW Windows port of DBus library
Requires:       mingw32-dbus = %{version}-%{release}

%description -n mingw32-dbus-static
D-BUS is a system for sending messages between applications. It is
used both for the system wide message bus service, and as a
per-user-login-session messaging facility.

Static version of MinGW Windows port of DBus library


# Win64
%package -n mingw64-dbus
Summary:        MinGW Windows port of D-Bus
Requires:       pkgconfig

%description -n mingw64-dbus
D-BUS is a system for sending messages between applications. It is
used both for the system wide message bus service, and as a
per-user-login-session messaging facility.


%package -n mingw64-dbus-static
Summary:        Static version of MinGW Windows port of DBus library
Requires:       mingw64-dbus = %{version}-%{release}

%description -n mingw64-dbus-static
D-BUS is a system for sending messages between applications. It is
used both for the system wide message bus service, and as a
per-user-login-session messaging facility.

Static version of MinGW Windows port of DBus library


%{?mingw_debug_package}


%prep
%autosetup -p1 -n dbus-%{version}


%build
MINGW_BUILDDIR_SUFFIX=static %mingw_cmake -DDBUS_ENABLE_DOXYGEN_DOCS=OFF -DENABLE_QT_HELP=OFF -DBUILD_SHARED_LIBS=OFF
MINGW_BUILDDIR_SUFFIX=static %mingw_make_build

MINGW_BUILDDIR_SUFFIX=shared %mingw_cmake -DDBUS_ENABLE_DOXYGEN_DOCS=OFF -DENABLE_QT_HELP=OFF
MINGW_BUILDDIR_SUFFIX=shared %mingw_make_build


%install
MINGW_BUILDDIR_SUFFIX=static %mingw_make_install
MINGW_BUILDDIR_SUFFIX=shared %mingw_make_install

# Remove manpages because they duplicate what's in the
# Fedora native package already.
rm -rf %{buildroot}%{mingw32_datadir}/doc
rm -rf %{buildroot}%{mingw64_datadir}/doc
rm -rf %{buildroot}%{mingw32_datadir}/xml
rm -rf %{buildroot}%{mingw64_datadir}/xml


# Win32
%files -n mingw32-dbus
%license COPYING
%{mingw32_bindir}/dbus-daemon.exe
%{mingw32_bindir}/dbus-env.bat
%{mingw32_bindir}/dbus-launch.exe
%{mingw32_bindir}/dbus-monitor.exe
%{mingw32_bindir}/dbus-run-session.exe
%{mingw32_bindir}/dbus-send.exe
%{mingw32_bindir}/dbus-test-tool.exe
%{mingw32_bindir}/dbus-update-activation-environment.exe
%{mingw32_bindir}/libdbus-1-3.dll
%{mingw32_libdir}/dbus-1.0/
%{mingw32_libdir}/libdbus-1.dll.a
%{mingw32_libdir}/cmake/DBus1/
%{mingw32_libdir}/pkgconfig/dbus-1.pc
%{mingw32_sysconfdir}/dbus-1/
%{mingw32_includedir}/dbus-1.0/
%{mingw32_datadir}/dbus-1/

%files -n mingw32-dbus-static
%{mingw32_libdir}/libdbus-1.a

# Win64
%files -n mingw64-dbus
%license COPYING
%{mingw64_bindir}/dbus-daemon.exe
%{mingw64_bindir}/dbus-env.bat
%{mingw64_bindir}/dbus-launch.exe
%{mingw64_bindir}/dbus-monitor.exe
%{mingw64_bindir}/dbus-run-session.exe
%{mingw64_bindir}/dbus-send.exe
%{mingw64_bindir}/dbus-test-tool.exe
%{mingw64_bindir}/dbus-update-activation-environment.exe
%{mingw64_bindir}/libdbus-1-3.dll
%{mingw64_libdir}/dbus-1.0/
%{mingw64_libdir}/libdbus-1.dll.a
%{mingw64_libdir}/cmake/DBus1/
%{mingw64_libdir}/pkgconfig/dbus-1.pc
%{mingw64_sysconfdir}/dbus-1/
%{mingw64_includedir}/dbus-1.0/
%{mingw64_datadir}/dbus-1/

%files -n mingw64-dbus-static
%{mingw64_libdir}/libdbus-1.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 18 2024 Sandro Mani <manisandro@gmail.com> - 1.16.0-1
- Update to 1.16.0

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.14.10-5
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 12 2023 Sandro Mani <manisandro@gmail.com> - 1.14.10-1
- Update to 1.14.10

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Sandro Mani <manisandro@gmail.com> - 1.14.8-1
- Update to 1.14.8

* Sat Feb 11 2023 Sandro Mani <manisandro@gmail.com> - 1.14.6-1
- Update to 1.14.6

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 05 2022 Sandro Mani <manisandro@gmail.com> - 1.14.4-1
- Update to 1.14.4

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.8.16-16
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 1.8.16-10
- Rebuild (Changes/Mingw32GccDwarf2)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.8.16-1
- Update to 1.8.16

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.8.12-1
- Update to 1.8.12

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.28-1
- Update to 1.6.28
- Fixes CVE-2014-7824 (RHBZ #1173557)
- Fixes CVE-2014-3638 CVE-2014-3639 CVE-2014-3636
  CVE-2014-3637 and CVE-2014-3635 (RHBZ #1142582)
- Fixes CVE-2014-3477 (RHBZ #1117395)
- Fixes CVE-2014-3533 CVE-2014-3532 (RHBZ #1115637)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 03 2013 Ivan Romanov <drizt@land.ru> - 1.6.12-1
- A new upstream version

* Thu Aug 29 2013 Ivan Romanov <drizt@land.ru> - 1.6.8-4
- Added patch to rename interface argument name (RHBZ #980278)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.8-1
- Update to 1.6.8

* Sun Sep 23 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.6.4-1
- Update to 1.6.4
- Fixes compatibility issue with c++11 support

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.4.16-1
- Update to 1.4.16
- Added win64 support
- Link against libxml2 instead of expat
- Dropped upstreamed patches

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.6-5
- Remove .la files

* Wed Mar 07 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.4.6-4
- Renamed the source package to mingw-dbus (RHBZ #800858)
- Use mingw macros without leading underscore
- Dropped unneeded RPM tags

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.4.6-3
- Rebuild against the mingw-w64 toolchain
- Added patch to prevent redeclaration of the symbol ELEMENT_TYPE

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 28 2011 Ivan Romanov <drizt@land.ru> - 1.4.6-1
- New upstream version
- Removed clean stage
- Added dbus-1.4.6-path-is-absolute.patch patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-0.2.20101008git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 8 2010 Ivan Romanov <drizt@land.ru> - 1.4.1-0.1.20101008git
- Updated to 1.4.1 version from git
- windbus is now part of freedesktop dbus
- Removed mingw32-dbus-c++ package (c++ bindings it's not part of dbus)
- Removed mingw32-dbus-1.2.4-20081031-mingw32.patch
- Removed unusual dependencies
- Removed init.d script
- Changed define tags on the top to global tags
- Added static subpackage with static library
- Added debuginfo

* Fri Feb 6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-0.3.20081031svn
- Include license.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-0.2.20081031svn
- Requires pkgconfig.

* Mon Nov 3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-0.1.20081031svn
- Initial RPM release.
