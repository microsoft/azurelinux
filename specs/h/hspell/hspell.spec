# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A Hebrew spell checker
Name: hspell
Version: 1.4
Release: 25%{?dist}
License: AGPL-3.0-only
URL: http://hspell.ivrix.org.il/
Source: http://hspell.ivrix.org.il/%{name}-%{version}.tar.gz
Patch0: 0001-require-local-module-explicitly.patch

BuildRequires:  gcc, make, hunspell-devel
BuildRequires:  perl-generators, perl-interpreter, zlib-devel
BuildRequires:  perl(Carp), perl(FileHandle)

%description
Hspell is a Hebrew SPELLer and morphological analyzer. It provides a mostly
spell-like interface (gives the list of wrong words in the input text), but can
also suggest corrections (-c). It also provides a true morphological analyzer
(-l), that prints all known meanings of a Hebrew string.
Hspell 1.4 still follows the old (pre June 2017) spelling standard of the
Academy of the Hebrew Language.

%description -l he
Hspell הוא מאיית ומנתח צורני עברי, המספק מנשק דמוי-spell - פולט רשימה של המילים
השגויות המופיעות בקלט. Hspell מקפיד מאוד כללי האקדמיה העברית לכתיב חסר ניקוד
("כתיב מלא").  כמו כן, Hspell מספק (-l) מנתח מורפולוגי אשר מדפיס את כל
המשמעויות האפשריות של מחרוזת אותיות עברית.
גרסה 1.4 תואמת עדיין לכללי האיות הישנים (טרם יוני 2017) של האקדמיה.

%package devel
Summary: Library and include files for Hspell, the Hebrew spell checker
Requires: %{name} = %{version}-%{release}

%description devel
Library and include files for applications that want to use Hspell.

%description -l he devel
ספרייה וקובצי כותרת עבור יישומים שרוצים להשתמש ב-Hspell.

%package -n hunspell-he
Summary: Hebrew hunspell dictionaries
Requires: hunspell

%description -n hunspell-he
Hebrew hunspell dictionaries.

%prep
%setup -q
%patch -P 0 -p1 -b .localreq
/usr/bin/iconv -f hebrew -t utf8 -o WHATSNEW WHATSNEW

%build
%configure --enable-fatverb --enable-linginfo --enable-shared
make
make hunspell

%install
make DESTDIR=$RPM_BUILD_ROOT STRIP=: install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libhspell.a

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hunspell
cp -p he.dic $RPM_BUILD_ROOT/%{_datadir}/hunspell/he_IL.dic
cp -p he.aff $RPM_BUILD_ROOT/%{_datadir}/hunspell/he_IL.aff

%check
# there are three known failures
! make test | grep FAILED | grep -E -v '1/aspell/[489]'

%files
%doc LICENSE README WHATSNEW COPYING
%{_bindir}/hspell
%{_bindir}/hspell-i
%{_bindir}/multispell
%{_libdir}/libhspell.so.0
%{_mandir}/man1/hspell.1*
%{_datadir}/hspell/

%files devel
%{_includedir}/*.h
%{_libdir}/libhspell.so
%{_mandir}/man3/hspell.3*

%files -n hunspell-he
%doc LICENSE
%{_datadir}/hunspell/*

%ldconfig_scriptlets

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Parag Nemade <pnemade AT redhat DOT com> - 1.4-18
- Migrate to SPDX license expression

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 29 2022 Parag Nemade <pnemade AT redhat DOT com> - 1.4-15
- Update hunspell dictionary directory path
  https://fedoraproject.org/wiki/Changes/Hunspell_dictionary_dir_change

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 26 2020 Jitka Plesnikova <jplesnik@redhat.com> - 1.4-10
- Add perl dependencies needed for build

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.4-1
- Sync with upstream hspell-1.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.3-1
- Sync with upstream hspell-1.3

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Peter Schiffer <pschiffe@redhat.com> - 1.2-8
- cleaned build section:
  STRIP variable is used in make install
  CFLAGS are picked up already by configure script
  fixed bogus dates in changelog

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.2-5
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Peter Schiffer <pschiffe@redhat.com> - 1.2-3
- .spec file cleanup

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 29 2012 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.2-1
- Sync with upstream hspell-1.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan  9 2010 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.1-3
- Rebuild with proper hunspell-devel dependency

* Fri Jan  1 2010 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.1-2
- Rebase to upstream version 1.1 and fix spec typos.

* Thu Dec 31 2009 Dan Kenigsberg <danken@cs.technion.ac.il> - 1.1-1
- Rebase to upstream version 1.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.0-11
- Fix Patch0:/%%patch mismatch.

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-10
- fix license tag

* Wed May 14 2008 Caolan McNamara <caolanm@redhat.com> - 1.0-9
- Resolves: rhbz#313231 build hspell.so instead of a .a

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0-8
- Autorebuild for GCC 4.3

* Tue May 22 2007 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-7
- Move the hunspell-he dictionaries into hspell package (Bug #240696).
  Mostly applying Caolan McNamara's patch #155078.
* Sun Feb 11 2007 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-6
- Use gzip -n to exclude MTIME from compressed data and resolve bug #228171
* Tue Sep 12 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-5
- Rebuild for Fedora Extras 6
* Sun Jul  9 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-4
- bump version to mend upgrade path. Bug #197125
* Sat May 20 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-3
- do not strip the binary, create useful defuginfo package (Bug #192437).
* Mon May 15 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 1.0-2
- new upstream release.
- Hebrew description converted to utf8.
* Tue Feb 28 2006 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-7
- Rebuild for Fedora Extras 5
* Mon Sep 26 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-6
- Add the text of the GPL to the binary package. It seems that I'll do anything
  to make my sponsor Tom happy.
* Thu Sep 22 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-5
- According to Tom's request, distribute the fat version.
- Add short Hebrew description to the devel package.
* Tue Sep 20 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-4
- Distribute the "slim" flavor, as I suspect it is better suited for the casual
  user (even though I personally enjoy the chubby morphological analizer).
* Mon Sep 19 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-3
- minor spec file cleanups, eliminate "fat" variant
* Thu Sep 15 2005 Dan Kenigsberg <danken@cs.technion.ac.il> 0.9-2
- version 0.9, some magic to silence rpmlint
* Fri Jun  4 2004 Dan Kenigsberg <danken@cs.technion.ac.il> 0.8-1
- Some cleanups, and a devel package
* Fri Dec 19 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.7-1
- Changes for version 0.7
* Tue Jul 29 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.6-1
- Tiny changes for the C frontend
* Fri May  2 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.5-1
- create the "fat" variant
* Mon Feb 17 2003 Dan Kenigsberg <danken@cs.technion.ac.il> 0.3-2
- The release includes only the compressed database.
- Added signature, and some other minor changes.
* Sun Jan  5 2003 Tzafrir Cohen <tzafrir@technion.ac.il> 0.2-1
- Initial build.
