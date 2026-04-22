# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-expat
Version:        2.7.4
Release: 2%{?dist}
Summary:        MinGW Windows port of expat XML parser library

License:        MIT
URL:            http://www.libexpat.org/
Source0:        http://downloads.sourceforge.net/expat/expat-%{version}.tar.bz2

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils


%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

# Win32
%package -n mingw32-expat
Summary:        MinGW Windows port of expat XML parser library

%description -n mingw32-expat
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package -n mingw32-expat-static
Summary:        Static version of the MinGW Windows expat XML parser library
Requires:       mingw32-expat = %{version}-%{release}

%description -n mingw32-expat-static
Static version of the MinGW Windows expat XML parser library.

# Win64
%package -n mingw64-expat
Summary:        MinGW Windows port of expat XML parser library

%description -n mingw64-expat
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package -n mingw64-expat-static
Summary:        Static version of the MinGW Windows expat XML parser library
Requires:       mingw64-expat = %{version}-%{release}

%description -n mingw64-expat-static
Static version of the MinGW Windows expat XML parser library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n expat-%{version}


%build
%mingw_configure
%mingw_make_build


%install
%mingw_make_install

# Remove .la files
find %{buildroot} -name "*.la" -delete

# Remove documentation which duplicates that found in the native package.
rm -r %{buildroot}%{mingw32_docdir}
rm -r %{buildroot}%{mingw64_docdir}
rm -r %{buildroot}%{mingw32_mandir}
rm -r %{buildroot}%{mingw64_mandir}


# Win32
%files -n mingw32-expat
%license COPYING
%{mingw32_bindir}/libexpat-1.dll
%{mingw32_bindir}/xmlwf.exe
%{mingw32_libdir}/libexpat.dll.a
%{mingw32_libdir}/pkgconfig/expat.pc
%{mingw32_libdir}/cmake/expat-%{version}/
%{mingw32_includedir}/expat.h
%{mingw32_includedir}/expat_config.h
%{mingw32_includedir}/expat_external.h

%files -n mingw32-expat-static
%{mingw32_libdir}/libexpat.a

# Win64
%files -n mingw64-expat
%license COPYING
%{mingw64_bindir}/libexpat-1.dll
%{mingw64_bindir}/xmlwf.exe
%{mingw64_libdir}/libexpat.dll.a
%{mingw64_libdir}/pkgconfig/expat.pc
%{mingw64_libdir}/cmake/expat-%{version}/
%{mingw64_includedir}/expat.h
%{mingw64_includedir}/expat_config.h
%{mingw64_includedir}/expat_external.h

%files -n mingw64-expat-static
%{mingw64_libdir}/libexpat.a


%changelog
* Fri Feb 06 2026 Sandro Mani <manisandro@gmail.com> - 2.7.4-1
- Update to 2.7.4

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Dec 03 2025 Sandro Mani <manisandro@gmail.com> - 2.7.3-1
- Update to 2.7.3

* Wed Sep 17 2025 Sandro Mani <manisandro@gmail.com> - 2.7.2-1
- Update to 2.7.2

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Apr 02 2025 Sandro Mani <manisandro@gmail.com> - 2.7.1-1
- Update to 2.7.1

* Sat Mar 15 2025 Sandro Mani <manisandro@gmail.com> - 2.7.0-1
- Update to 2.7.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 09 2024 Sandro Mani <manisandro@gmail.com> - 2.6.4-1
- Update to 2.6.4

* Tue Nov 05 2024 Sandro Mani <manisandro@gmail.com> - 2.6.3-2
- Backport patch for CVE-2024-50602

* Thu Sep 05 2024 Sandro Mani <manisandro@gmail.com> - 2.6.3-1
- Update to 2.6.3

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 22 2024 Sandro Mani <manisandro@gmail.com> - 2.6.2-1
- Update to 2.6.2

* Sun Mar 10 2024 Sandro Mani <manisandro@gmail.com> - 2.6.1-1
- Update to 2.6.1

* Fri Feb 16 2024 Sandro Mani <manisandro@gmail.com> - 2.6.0-1
- Update to 2.6.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Sandro Mani <manisandro@gmail.com> - 2.5.0-1
- Update to 2.5.0

* Fri Oct 21 2022 Sandro Mani <manisandro@gmail.com> - 2.4.9-1
- Update to 2.4.9

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 14 2022 Sandro Mani <manisandro@gmail.com> - 2.4.8-1
- Update to 2.4.8

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 2.4.7-2
- Rebuild with mingw-gcc-12

* Mon Mar 14 2022 Sandro Mani <manisandro@gmail.com> - 2.4.7-1
- Update to 2.4.7

* Mon Feb 21 2022 Sandro Mani <manisandro@gmail.com> - 2.4.6-1
- Update to 2.4.6

* Tue Feb 01 2022 Sandro Mani <manisandro@gmail.com> - 2.4.4-1
- Update to 2.4.4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Sandro Mani <manisandro@gmail.com> - 2.4.3-1
- Update to 2.4.3

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Sandro Mani <manisandro@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Sat Apr 17 2021 Sandro Mani <manisandro@gmail.com> - 2.3.0-1
- Update to 2.3.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 13 2020 Sandro Mani <manisandro@gmail.com> - 2.2.10-1
- Update to 2.2.10

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Sandro Mani <manisandro@gmail.com> - 2.2.8-1
- Update to 2.2.8

* Wed Aug 28 2019 Sandro Mani <manisandro@gmail.com> - 2.2.7-1
- Update to 2.2.7

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Oct 15 2017 Kalev Lember <klember@redhat.com> - 2.2.4-1
- Update to 2.2.4

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 24 2016 Kalev Lember <klember@redhat.com> - 2.2.0-1
- Update to 2.2.0
- Don't set group tags
- Use license macro for COPYING

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.1.0-3
- Added static subpackages

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- Dropped the autoconf/libtool regeneration pieces

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-12
- Added win64 support
- Dropped unneeded RPM tags

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 2.0.1-11
- Remove .la files

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-10
- Renamed the source package to mingw-expat (RHBZ #800377)
- Use mingw macros without leading underscore
- Use the RPM magic to automatically generate provides/requires tags
- Automatically generate a debuginfo subpackage

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-9
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-6
- Fix Source0 URL.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  9 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-4
- Remove +x permissions on COPYING file.

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-3
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-2
- Include license.

* Fri Oct 31 2008 Richard W.M. Jones <rjones@redhat.com> - 2.0.1-1
- Initial RPM release.
