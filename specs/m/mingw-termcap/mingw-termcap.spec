# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Note: Termcap was deprecated and removed from Fedora after F-8.  It
# has been replaced by ncurses.  However ncurses cannot be compiled on
# Windows so we have to supply termcap.  In addition, the last stand-
# alone Fedora termcap package was actually just /etc/termcap from
# ncurses.  So here we are using the GNU termcap library which is
# regretably GPL'd.

%?mingw_package_header

%global mingw_build_win32 1
%global mingw_build_win64 1

Name:           mingw-termcap
Version:        1.3.1
Release: 40%{?dist}
Summary:        MinGW terminal feature database

License:        GPL-2.0-or-later
URL:            ftp://ftp.gnu.org/gnu/termcap/
Source0:        ftp://ftp.gnu.org/gnu/termcap/termcap-%{version}.tar.gz
# Fix implicit function declarations
Patch0:         termcap-1.3.1-implicit.patch

BuildArch:      noarch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils

BuildRequires:  autoconf


%description
This is the GNU termcap library -- a library of C functions that
enable programs to send control strings to terminals in a way
independent of the terminal type.  The GNU termcap library does not
place an arbitrary limit on the size of termcap entries, unlike most
other termcap libraries.

This package contains libraries and development tools for the MinGW
cross-compiled version.


# Win32
%package -n mingw32-termcap
Summary:        MinGW terminal feature database

%description -n mingw32-termcap
This is the GNU termcap library -- a library of C functions that
enable programs to send control strings to terminals in a way
independent of the terminal type.  The GNU termcap library does not
place an arbitrary limit on the size of termcap entries, unlike most
other termcap libraries.

This package contains libraries and development tools for the MinGW
cross-compiled version.

%package -n mingw32-termcap-static
Summary:        Static version of the cross compiled termcap library
Requires:       mingw32-termcap = %{version}-%{release}

%description -n mingw32-termcap-static
Static version of the cross compiled termcap library.

# Win64
%package -n mingw64-termcap
Summary:        MinGW terminal feature database

%description -n mingw64-termcap
This is the GNU termcap library -- a library of C functions that
enable programs to send control strings to terminals in a way
independent of the terminal type.  The GNU termcap library does not
place an arbitrary limit on the size of termcap entries, unlike most
other termcap libraries.

This package contains libraries and development tools for the MinGW
cross-compiled version.

%package -n mingw64-termcap-static
Summary:        Static version of the cross compiled termcap library
Requires:       mingw64-termcap = %{version}-%{release}

%description -n mingw64-termcap-static
Static version of the cross compiled termcap library.


%?mingw_debug_package


%prep
%setup -q -n termcap-%{version}
%patch -P0 -p1

# Packaged script doesn't understand --bindir, so rebuild:
autoconf


%build
%mingw_configure
%mingw_make %{?_smp_mflags} CFLAGS="$CFLAGS -std=gnu89"

# Build a shared library.  No need for -fPIC on Windows.
pushd build_win32
%{mingw32_cc} -shared \
  -Wl,--out-implib,libtermcap.dll.a \
  -o libtermcap-0.dll \
  termcap.o tparam.o version.o
popd
pushd build_win64
%{mingw64_cc} -shared \
  -Wl,--out-implib,libtermcap.dll.a \
  -o libtermcap-0.dll \
  termcap.o tparam.o version.o
popd


%install
# We can't use the %%mingw_make_install macro here as
# the Makefile doesn't support the DESTDIR=... flag
make install -C build_win32 \
  prefix=$RPM_BUILD_ROOT%{mingw32_prefix} \
  exec_prefix=$RPM_BUILD_ROOT%{mingw32_prefix} \
  oldincludedir=
make install -C build_win64 \
  prefix=$RPM_BUILD_ROOT%{mingw64_prefix} \
  exec_prefix=$RPM_BUILD_ROOT%{mingw64_prefix} \
  oldincludedir=

# Move the shared library to the correct locations.
mkdir -p $RPM_BUILD_ROOT%{mingw32_bindir}
install -m 0755 build_win32/libtermcap-0.dll $RPM_BUILD_ROOT%{mingw32_bindir}
install -m 0755 build_win32/libtermcap.dll.a $RPM_BUILD_ROOT%{mingw32_libdir}

mkdir -p $RPM_BUILD_ROOT%{mingw64_bindir}
install -m 0755 build_win64/libtermcap-0.dll $RPM_BUILD_ROOT%{mingw64_bindir}
install -m 0755 build_win64/libtermcap.dll.a $RPM_BUILD_ROOT%{mingw64_libdir}

# Move the info files to the correct location.
mkdir -p $RPM_BUILD_ROOT%{mingw32_infodir}
mv $RPM_BUILD_ROOT%{mingw32_prefix}/info/* $RPM_BUILD_ROOT%{mingw32_infodir}

mkdir -p $RPM_BUILD_ROOT%{mingw64_infodir}
mv $RPM_BUILD_ROOT%{mingw64_prefix}/info/* $RPM_BUILD_ROOT%{mingw64_infodir}



%files -n mingw32-termcap
%doc COPYING
%{mingw32_bindir}/libtermcap-0.dll
%{mingw32_libdir}/libtermcap.dll.a
%{mingw32_includedir}/termcap.h
# Note that we want the info files in this package because
# there is no equivalent native Fedora package.
%{mingw32_infodir}/*

%files -n mingw32-termcap-static
%{mingw32_libdir}/libtermcap.a

%files -n mingw64-termcap
%doc COPYING
%{mingw64_bindir}/libtermcap-0.dll
%{mingw64_libdir}/libtermcap.dll.a
%{mingw64_includedir}/termcap.h
%{mingw64_infodir}/*

%files -n mingw64-termcap-static
%{mingw64_libdir}/libtermcap.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.3.1-31
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.3.1-13
- Added win64 support
- Automatically generate debuginfo subpackage
- Added static subpackage

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.3.1-12
- Renamed the source package to mingw-termcap (#801034)
- Modernize the spec file
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.3.1-11
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-6
- Rebuild for mingw32-gcc 4.4

* Fri Dec 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-5
- Added license file to doc section.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-4
- Rerun autoconf because the standard configure doesn't know --bindir.
- Set exec_prefix during make install step.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-3
- Fix so it builds a working DLL.

* Thu Sep 25 2008 Richard W.M. Jones <rjones@redhat.com> - 1.3.1-1
- Initial RPM release.
