# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global pkgname hunspell

Name:          mingw-%{pkgname}
Version:       1.7.2
Release: 11%{?dist}
Summary:       MinGW Windows spell checker and morphological analyzer library

URL:           http://hunspell.github.io/
License:       LGPL-2.1-or-later OR GPL-2.0-or-later OR MPL-1.1
Source0:       https://github.com/hunspell/%{pkgname}/archive/v%{version}/%{pkgname}-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: make
BuildRequires: libtool automake autoconf
BuildRequires: bison
BuildRequires: gettext-devel

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-binutils
BuildRequires: mingw32-gettext
BuildRequires: mingw32-readline

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-binutils
BuildRequires: mingw64-gettext
BuildRequires: mingw64-readline


%description
Hunspell is a spell checker and morphological analyzer library and program
designed for languages with rich morphology and complex word compounding or
character encoding. Hunspell interfaces: Ispell-like terminal interface using
Curses library, Ispell pipe interface, OpenOffice.org UNO module.

This is the MinGW build of Hunspell.


# Win32
%package -n mingw32-%{pkgname}
Summary:       MinGW Windows spell checker and morphological analyzer library

%description -n mingw32-%{pkgname}
Hunspell is a spell checker and morphological analyzer library and program
designed for languages with rich morphology and complex word compounding or
character encoding. Hunspell interfaces: Ispell-like terminal interface using
Curses library, Ispell pipe interface, OpenOffice.org UNO module.

This is the MinGW build of Hunspell.


%package -n mingw32-%{pkgname}-static
Summary:        Static version of the MinGW Windows hunspell library
Requires:       mingw32-%{pkgname} = %{version}-%{release}

%description -n mingw32-%{pkgname}-static
Static version of the MinGW Windows hunspell spell checking library.


%package -n mingw32-%{pkgname}-tools
Summary:        MinGW Windows hunspell library tools
Requires:       mingw32-%{pkgname} = %{version}-%{release}

%description -n mingw32-%{pkgname}-tools
MinGW Windows hunspell library tools.


# Win64
%package -n mingw64-%{pkgname}
Summary:       MinGW Windows spell checker and morphological analyzer library

%description -n mingw64-%{pkgname}
Hunspell is a spell checker and morphological analyzer library and program
designed for languages with rich morphology and complex word compounding or
character encoding. Hunspell interfaces: Ispell-like terminal interface using
Curses library, Ispell pipe interface, OpenOffice.org UNO module.

This is the MinGW build of Hunspell


%package -n mingw64-%{pkgname}-static
Summary:        Static version of the MinGW Windows hunspell library
Requires:       mingw64-%{pkgname} = %{version}-%{release}

%description -n mingw64-%{pkgname}-static
Static version of the MinGW Windows hunspell spell checking library.


%package -n mingw64-%{pkgname}-tools
Summary:        MinGW Windows hunspell library tools
Requires:       mingw64-%{pkgname} = %{version}-%{release}

%description -n mingw64-%{pkgname}-tools
MinGW Windows hunspell library tools.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{pkgname}-%{version}


%build
autoreconf -ifv
%mingw_configure --enable-static --enable-shared --with-ui --with-readline --enable-threads=win32
%mingw_make_build


%install
%mingw_make_install

# Drop .la files
rm -f %{buildroot}%{mingw32_libdir}/*.la
rm -f %{buildroot}%{mingw64_libdir}/*.la

# Drop the man pages
rm -rf %{buildroot}%{mingw32_datadir}/man
rm -rf %{buildroot}%{mingw64_datadir}/man


# Win32
%files -n mingw32-%{pkgname}
%license COPYING COPYING.LESSER COPYING.MPL license.hunspell license.myspell
%{mingw32_bindir}/libhunspell-1.7-0.dll
%{mingw32_includedir}/hunspell/
%{mingw32_libdir}/libhunspell-1.7.dll.a
%{mingw32_libdir}/pkgconfig/hunspell.pc

%files -n mingw32-%{pkgname}-static
%{mingw32_libdir}/libhunspell-1.7.a

%files -n mingw32-%{pkgname}-tools
%{mingw32_bindir}/affixcompress
%{mingw32_bindir}/analyze.exe
%{mingw32_bindir}/chmorph.exe
%{mingw32_bindir}/hunspell.exe
%{mingw32_bindir}/hunzip.exe
%{mingw32_bindir}/hzip.exe
%{mingw32_bindir}/ispellaff2myspell
%{mingw32_bindir}/makealias
%{mingw32_bindir}/munch.exe
%{mingw32_bindir}/unmunch.exe
%{mingw32_bindir}/wordforms
%{mingw32_bindir}/wordlist2hunspell


# Win64
%files -n mingw64-%{pkgname}
%license COPYING COPYING.LESSER COPYING.MPL license.hunspell license.myspell
%{mingw64_bindir}/libhunspell-1.7-0.dll
%{mingw64_includedir}/hunspell/
%{mingw64_libdir}/libhunspell-1.7.dll.a
%{mingw64_libdir}/pkgconfig/hunspell.pc

%files -n mingw64-%{pkgname}-static
%{mingw64_libdir}/libhunspell-1.7.a

%files -n mingw64-%{pkgname}-tools
%{mingw64_bindir}/affixcompress
%{mingw64_bindir}/analyze.exe
%{mingw64_bindir}/chmorph.exe
%{mingw64_bindir}/hunspell.exe
%{mingw64_bindir}/hunzip.exe
%{mingw64_bindir}/hzip.exe
%{mingw64_bindir}/ispellaff2myspell
%{mingw64_bindir}/makealias
%{mingw64_bindir}/munch.exe
%{mingw64_bindir}/unmunch.exe
%{mingw64_bindir}/wordforms
%{mingw64_bindir}/wordlist2hunspell


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Sandro Mani <manisandro@gmail.com> - 1.7.2-8
- Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.7.2-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Sandro Mani <manisandro@gmail.com> - 1.7.2-1
- Update to 1.7.2

* Tue Aug 30 2022 Sandro Mani <manisandro@gmail.com> - 1.7.1-1
- Update to 1.7.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.7.0-14
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 12 13:41:09 GMT 2020 Sandro Mani <manisandro@gmail.com> - 1.7.0-10
- Rebuild (mingw-gettext)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Sandro Mani <manisandro@gmail.com> - 1.7.0-8
- Rebuild (gettext)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 13 2019 Sandro Mani <manisandro@gmail.com> - 1.7.0-6
- Backport fix for CVE-2019-16707

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 1.7.0-5
- Rebuild (Changes/Mingw32GccDwarf2)

* Wed Aug 28 2019 Sandro Mani <manisandro@gmail.com> - 1.7.0-4
- Rebuild (readline)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 14 2018 Sandro Mani <manisandro@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Sandro Mani <manisandro@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Sandro Mani <manisandro@gmail.com> - 1.5.4-1
- Update to 1.5.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jan 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.3.2-9
- Rebuild against mingw-gcc 4.8 (win64 uses SEH exceptions now)

* Thu Nov 22 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.3.2-8
- Rebuild against latest mingw-readline

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 18 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.3.2-6
- Added win64 support

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 1.3.2-5
- Drop .la files

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.3.2-4
- Renamed the source package to mingw-hunspell (#800425)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.3.2-3
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep 04 2011 Kalev Lember <kalevlember@gmail.com> - 1.3.2-1
- Update to 1.3.2

* Wed Jul  6 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.12-4
- Rebuild against win-iconv
- Force the use of the Win32 threads API instead of pthreads

* Thu Apr 28 2011 Kalev Lember <kalev@smartlink.ee> - 1.2.12-3
- Rebuilt for proxy-libintl removal

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.12-1
- Update to 1.2.12 (RHBZ #587589)
- Dropped all the patches and post-install hacks
- Rebuild in order to have soft dependency on libintl

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.8-11
- Rebuild because of broken mingw32-gcc/mingw32-binutils

* Sun Aug 30 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.8-10
- Automatically generate debuginfo subpackage

* Thu Aug 13 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.8-9
- Fixed invalid source URL

* Thu Jul 30 2009 Jesse Keating <jkeating@redhat.com> - 1.2.8-8
- Bump for F12 rebuild
- Fill in a date for the previous commit

* Thu Jul 30 2009 Erik van Pienbroek <epienbro@fedoraproject.org> 1.2.8-7
- Updated description

* Wed May 20 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.2.8-6
- Ported the native Fedora package to build a MinGW library

* Fri May 01 2009 Caolan McNamara <caolanm@redhat.com> - 1.2.8-5
- Resolves: rhbz#498556 fix default language detection

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.8-3
- tweak summary

* Wed Nov 19 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.8-2
- Resolves: rhbz#471085 in ispell compatible mode (-a), ignore
  -m option which means something different to ispell

* Sun Nov 02 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.8-1
- latest version

* Sat Oct 18 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.7-5
- sort as per "C" locale

* Fri Oct 17 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.7-4
- make wordlist2hunspell remove blank lines 

* Mon Sep 15 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.7-3
- Workaround rhbz#462184 uniq/sort problems with viramas

* Tue Sep 09 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.7-2
- add wordlist2hunspell

* Sat Aug 23 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.7-1
- latest version

* Tue Jul 29 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.6-1
- latest version

* Sun Jul 27 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.5-1
- latest version

* Tue Jul 22 2008 Kristian Høgsberg <krh@redhat.com> - 1.2.4.2-2
- Drop ABI breaking hunspell-1.2.2-xulrunner.pita.patch and fix the
  hunspell include in xulrunner.

* Fri Jul 18 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.4.2-1
- latest version

* Thu Jul 17 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.4-1
- latest version

* Fri May 16 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.2-3
- Resolves: rhbz#446821 fix crash

* Wed May 14 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.2-2
- give xulrunner what it needs so we can get on with it

* Fri Apr 18 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.2-1
- latest version
- drop integrated hunspell-1.2.1-1863239.badstructs.patch

* Wed Mar 05 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.1-6
- add ispellaff2myspell to devel

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.1-5
- Autorebuild for GCC 4.3

* Thu Jan 03 2008 Caolan McNamara <caolanm@redhat.com> - 1.2.1-4
- add hunspell-1.2.1-1863239.badstructs.patch

* Fri Nov 09 2007 Caolan McNamara <caolanm@redhat.com> - 1.2.1-2
- pkg-config cockup

* Mon Nov 05 2007 Caolan McNamara <caolanm@redhat.com> - 1.2.1-1
- latest version

* Mon Oct 08 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.12.2-2
- lang fix for man pages from Ville Skyttä

* Wed Sep 05 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.12.2-1
- next version

* Tue Aug 28 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.11.2-1
- next version

* Fri Aug 24 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.10-1
- next version

* Thu Aug 02 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.9-2
- clarify license

* Wed Jul 25 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.9-1
- latest version

* Wed Jul 18 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.8.2-1
- latest version

* Tue Jul 17 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.8-1
- latest version

* Sat Jul 07 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.7-1
- latest version
- drop integrated hunspell-1.1.5.freem.patch

* Fri Jun 29 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.6-1
- latest version
- drop integrated hunspell-1.1.4-defaultdictfromlang.patch
- drop integrated hunspell-1.1.5-badheader.patch
- drop integrated hunspell-1.1.5.encoding.patch

* Fri Jun 29 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.5.3-5
- fix memory leak
  http://sourceforge.net/tracker/index.php?func=detail&aid=1745263&group_id=143754&atid=756395

* Wed Jun 06 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.5.3-4
- Resolves: rhbz#212984 discovered problem with missing wordchars

* Tue May 22 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.5.3-3
- Resolves: rhbz#240696 extend encoding patch to promote and add
  dictionary 8bit WORDCHARS to the ucs-2 word char list

* Mon May 21 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.5.3-2
- Resolves: rhbz#240696 add hunspell-1.1.5.encoding.patch

* Mon May 21 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.5.3-1
- patchlevel release

* Tue Mar 20 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.5-2
- some junk in delivered headers

* Tue Mar 20 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.5-1
- next version

* Fri Feb 09 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.4-6
- some spec cleanups

* Fri Jan 19 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.4-5
- .pc

* Thu Jan 11 2007 Caolan McNamara <caolanm@redhat.com> - 1.1.4-4
- fix out of range

* Fri Dec 15 2006 Caolan McNamara <caolanm@redhat.com> - 1.1.4-3
- hunspell#1616353 simple c api for hunspell

* Wed Nov 29 2006 Caolan McNamara <caolanm@redhat.com> - 1.1.4-2
- add hunspell-1.1.4-defaultdictfromlang.patch to take locale as default
  dictionary

* Wed Oct 25 2006 Caolan McNamara <caolanm@redhat.com> - 1.1.4-1
- initial version
