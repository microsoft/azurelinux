# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%?mingw_package_header

Name:           mingw-pdcurses
Version:        3.8
Release:        15%{?dist}
Summary:        Curses library for MinGW

License:        LicenseRef-Fedora-Public-Domain
URL:            http://pdcurses.sourceforge.net/
Source0:        http://downloads.sourceforge.net/pdcurses/PDCurses-%{version}.tar.gz

BuildArch:      noarch

Patch0001:      0001-build-sys-add-WINDRES-variable.patch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils

# For applying patches.
BuildRequires:  git

%?mingw_debug_package

%description
PDCurses is a public domain curses library for DOS, OS/2, Win32, X11
and SDL, implementing most of the functions available in X/Open and
System V R4 curses. It supports many compilers for these
platforms. The X11 port lets you recompile existing text-mode curses
programs to produce native X11 applications.

Note that ncurses is not available for MinGW / Windows.  Applications
which need curses functionality can use this package, provided they
don't use any of the extensions specific to ncurses.


%package -n mingw32-pdcurses
Summary:        Curses library for MinGW32

%description -n mingw32-pdcurses
PDCurses is a public domain curses library for DOS, OS/2, Win32, X11
and SDL, implementing most of the functions available in X/Open and
System V R4 curses. It supports many compilers for these
platforms. The X11 port lets you recompile existing text-mode curses
programs to produce native X11 applications.

Note that ncurses is not available for MinGW / Windows.  Applications
which need curses functionality can use this package, provided they
don't use any of the extensions specific to ncurses.

%package -n mingw64-pdcurses
Summary:        Curses library for MinGW64

%description -n mingw64-pdcurses
PDCurses is a public domain curses library for DOS, OS/2, Win32, X11
and SDL, implementing most of the functions available in X/Open and
System V R4 curses. It supports many compilers for these
platforms. The X11 port lets you recompile existing text-mode curses
programs to produce native X11 applications.

Note that ncurses is not available for MinGW / Windows.  Applications
which need curses functionality can use this package, provided they
don't use any of the extensions specific to ncurses.


%prep
%autosetup -S git_am -n PDCurses-%{version}

cp -a wincon win32
cp -a wincon win64

%build
pushd win32
make \
  CC=%{mingw32_cc} \
  LINK=%{mingw32_cc} \
  STRIP=%{mingw32_strip} \
  WINDRES=%{mingw32_windres} \
  WIDE=Y UTF8=Y DLL=Y
popd

pushd win64
make \
  CC=%{mingw64_cc} \
  LINK=%{mingw64_cc} \
  STRIP=%{mingw64_strip} \
  WINDRES=%{mingw64_windres} \
  WIDE=Y UTF8=Y DLL=Y
popd

%install
mkdir -p $RPM_BUILD_ROOT%{mingw32_bindir}
mkdir -p $RPM_BUILD_ROOT%{mingw32_libdir}
mkdir -p $RPM_BUILD_ROOT%{mingw32_includedir}

install win32/pdcurses.dll $RPM_BUILD_ROOT%{mingw32_bindir}/pdcurses.dll
install win32/pdcurses.a $RPM_BUILD_ROOT%{mingw32_libdir}/libpdcurses.dll.a
install -m 0644 curses.h panel.h $RPM_BUILD_ROOT%{mingw32_includedir}


mkdir -p $RPM_BUILD_ROOT%{mingw64_bindir}
mkdir -p $RPM_BUILD_ROOT%{mingw64_libdir}
mkdir -p $RPM_BUILD_ROOT%{mingw64_includedir}

install win64/pdcurses.dll $RPM_BUILD_ROOT%{mingw64_bindir}/pdcurses.dll
install win64/pdcurses.a $RPM_BUILD_ROOT%{mingw64_libdir}/libpdcurses.dll.a
install -m 0644 curses.h panel.h $RPM_BUILD_ROOT%{mingw64_includedir}


%files -n mingw32-pdcurses
%{mingw32_bindir}/pdcurses.dll
%{mingw32_libdir}/libpdcurses.dll.a
%{mingw32_includedir}/curses.h
%{mingw32_includedir}/panel.h

%files -n mingw64-pdcurses
%{mingw64_bindir}/pdcurses.dll
%{mingw64_libdir}/libpdcurses.dll.a
%{mingw64_includedir}/curses.h
%{mingw64_includedir}/panel.h


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.8-7
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 3.8-1
- New upstream release 3.8
- Removed demos and term.h

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 21 2012 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.4-12
- Add mingw64.
- Rework patch.
- Rename mingw32-pdcurses-3.4-build.patch into mingw-pdcurses-3.4-build.patch.

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 3.4-11
- Renamed the source package to mingw-pdcurses (#801012)
- Modernize the spec file
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.4-10
- Rebuild against the mingw-w64 toolchain
- Use the correct toolchain tools in the patch

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 3.4-7
- Fix Source0 URL.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 3.4-4
- Rebuild for mingw32-gcc 4.4

* Fri Jan 16 2009 Richard Jones <rjones@redhat.com> - 3.4-3
- Remove +x permissions on the header files.

* Sat Nov 22 2008 Richard Jones <rjones@redhat.com> - 3.4-2
- Rename implib to libpdcurses.dll.a so that libtool can use it.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 3.4-1
- Initial RPM release.
