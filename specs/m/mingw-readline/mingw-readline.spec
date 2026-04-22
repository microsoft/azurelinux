# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-readline
Version:        8.3
Release: 3%{?dist}
Summary:        MinGW port of readline for editing typed command lines

License:        GPL-2.0-or-later
URL:            https://tiswww.case.edu/php/chet/readline/rltop.html
Source0:        https://git.savannah.gnu.org/cgit/readline.git/snapshot/readline-%{version}.tar.gz

# Remove RPATH, use CFLAGS
Patch1:         readline-8.0-shlib.patch
# Fix mingw build
Patch2:         readline_mingw.patch

BuildArch:      noarch

BuildRequires:  make

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-termcap

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-termcap


%description
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

This is a port of the library and development tools to Windows.


# Win32
%package -n mingw32-readline
Summary:        MinGW port of readline for editing typed command lines

%description -n mingw32-readline
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

This is a port of the library and development tools to Windows.

%package -n mingw32-readline-static
Summary:        Static version of the cross compiled readline library
Requires:       mingw32-readline = %{version}-%{release}

%description -n mingw32-readline-static
Static version of the cross compiled readline library.

# Win64
%package -n mingw64-readline
Summary:        MinGW port of readline for editing typed command lines

%description -n mingw64-readline
The Readline library provides a set of functions that allow users to
edit command lines. Both Emacs and vi editing modes are available. The
Readline library includes additional functions for maintaining a list
of previously-entered command lines for recalling or editing those
lines, and for performing csh-like history expansion on previous
commands.

This is a port of the library and development tools to Windows.

%package -n mingw64-readline-static
Summary:        Static version of the cross compiled readline library
Requires:       mingw64-readline = %{version}-%{release}

%description -n mingw64-readline-static
Static version of the cross compiled readline library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n readline-%{version}


%build
export MINGW32_CFLAGS="%{mingw32_cflags} -D_POSIX -D__USE_MINGW_ALARM=1"
export MINGW64_CFLAGS="%{mingw64_cflags} -D_POSIX -D__USE_MINGW_ALARM=1"
%mingw_configure --enable-shared
%mingw_make SHLIB_LIBS=-ltermcap


%install
%mingw_make_install

# Don't want the info files or manpages which duplicate the native package.
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw32_infodir}

rm -rf %{buildroot}%{mingw64_mandir}
rm -rf %{buildroot}%{mingw64_infodir}

rm -rf %{buildroot}%{mingw32_docdir}
rm -rf %{buildroot}%{mingw64_docdir}

# The examples also duplicate the native package so they can be removed as well
rm -f %{buildroot}%{mingw32_datadir}/readline/*.c
rm -f %{buildroot}%{mingw64_datadir}/readline/*.c


# Win32
%files -n mingw32-readline
%license COPYING
%{mingw32_bindir}/libreadline8.dll
%{mingw32_bindir}/libhistory8.dll
%{mingw32_libdir}/libreadline.dll.a
%{mingw32_libdir}/libhistory.dll.a
%{mingw32_libdir}/pkgconfig/history.pc
%{mingw32_libdir}/pkgconfig/readline.pc
%{mingw32_includedir}/readline/

%files -n mingw32-readline-static
%{mingw32_libdir}/libhistory.a
%{mingw32_libdir}/libreadline.a

# Win64
%files -n mingw64-readline
%license COPYING
%{mingw64_bindir}/libreadline8.dll
%{mingw64_bindir}/libhistory8.dll
%{mingw64_libdir}/libreadline.dll.a
%{mingw64_libdir}/libhistory.dll.a
%{mingw64_libdir}/pkgconfig/history.pc
%{mingw64_libdir}/pkgconfig/readline.pc
%{mingw64_includedir}/readline/

%files -n mingw64-readline-static
%{mingw64_libdir}/libhistory.a
%{mingw64_libdir}/libreadline.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Sandro Mani <manisandro@gmail.com> - 8.3-1
- Update to 8.3

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 07 2022 Sandro Mani <manisandro@gmail.com> - 8.2-1
- Update to 8.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 8.1-5
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 09 2021 Sandro Mani <manisandro@gmail.com> - 8.1-1
- Update to 8.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 14 2019 Fabiano Fidêncio <fidencio@redhat.com> - 8.0-1
- Update the sources accordingly to its native counter part, rhbz#1740751

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 6.2-4
- Fix CVE-2014-2524 (RHBZ #1077035)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 6.2-1
- Update to 6.2
- Cleaned up old patches and obsolete hacks

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2-12
- Added win64 support
- Automatically generate debuginfo subpackage
- Added -static subpackage

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 5.2-11
- Renamed the source package to mingw-readline (#801022)
- Modernize the spec file
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2-10
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 5.2-5
- Rebuild for mingw32-gcc 4.4

* Sat Nov 22 2008 Richard W.M. Jones <rjones@redhat.com> - 5.2-4
- Rename *.dll.a to lib*.dll.a so that libtool can use these libraries.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 5.2-3
- Fix paths to mandir, infodir.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 5.2-2
- Rebuild against latest termcap.

* Thu Sep 25 2008 Richard W.M. Jones <rjones@redhat.com> - 5.2-1
- Initial RPM release.
