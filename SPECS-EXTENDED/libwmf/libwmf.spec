Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Windows MetaFile Library
Name: libwmf
Version: 0.2.12
Release: 4%{?dist}
#libwmf is under the LGPLv2+, however...
#1. The tarball contains an old version of the urw-fonts under GPL+.
#   Those fonts are not installed
#2. The header of the command-line wmf2plot utility places it under the GPLv2+.
#   wmf2plot is neither built or install
License: LGPLv2+ and GPLv2+ and GPL+
Source: https://github.com/caolanm/libwmf/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
URL: https://github.com/caolanm/libwmf

Requires: urw-fonts
Requires: %{name}-lite = %{version}-%{release}

# for file triggers
Requires: gdk-pixbuf2%{?_isa} >= 2.31.5-2.fc24

BuildRequires: gtk2-devel, libtool, libxml2-devel, libpng-devel
BuildRequires: libjpeg-devel, libXt-devel, libX11-devel, dos2unix, libtool

%description
A library for reading and converting Windows MetaFile vector graphics (WMF).

%package lite
Summary: Windows Metafile parser library

%description lite
A library for parsing Windows MetaFile vector graphics (WMF).

%package devel
Summary: Support files necessary to compile applications with libwmf
Requires: libwmf = %{version}-%{release}
Requires: gtk2-devel, libxml2-devel, libjpeg-devel

%description devel
Libraries, headers, and support files necessary to compile applications 
using libwmf.

%prep
%setup -q
f=README ; iconv -f iso-8859-2 -t utf-8 $f > $f.utf8 ; mv $f.utf8 $f

%build
autoreconf -i -f -Ipatches
%configure --with-libxml2 --disable-static --disable-dependency-tracking --with-gsfontdir=/usr/share/fonts/urw-base35
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

rm -rf $RPM_BUILD_ROOT%{_includedir}/libwmf/gd
find doc -name "Makefile*" -exec rm {} \;

#we're carrying around duplicate fonts
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*afm
rm -rf $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/*t1
sed -i $RPM_BUILD_ROOT%{_datadir}/libwmf/fonts/fontmap -e 's#libwmf/fonts#fonts/urw-base35#g'

%ldconfig_scriptlets
%ldconfig_scriptlets lite

%files
%{_libdir}/libwmf-0.2.so.7*
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so
%{_bindir}/wmf2svg
%{_bindir}/wmf2gd
%{_bindir}/wmf2eps
%{_bindir}/wmf2fig
%{_bindir}/wmf2x
%{_bindir}/libwmf-fontmap
%{_datadir}/libwmf/

%files lite
%doc AUTHORS README
%license COPYING
%{_libdir}/libwmflite-0.2.so.7*

%files devel
%doc doc/*.html
%doc doc/*.png
%doc doc/*.gif
%doc doc/html
%doc doc/caolan
%{_libdir}/libwmf*.so
%{_libdir}/pkgconfig/libwmf.pc
%{_includedir}/libwmf/
%{_bindir}/libwmf-config


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.12-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Caolán McNamara <caolanm@redhat.com> - 0.2.12-1
- Related: rhbz#1671392/rhbz#1671621 unwanted soname bump

* Fri Feb 01 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.2.11-2
- track library sonames so bumps aren't a surprise
- use %%make_build %%make_install macros

* Thu Jan 31 2019 Caolán McNamara <caolanm@redhat.com> - 0.2.11-1
- Resolves: rhbz#1671392 CVE-2019-6978 latest version

* Fri Aug 10 2018 Caolán McNamara <caolanm@redhat.com> - 0.2.10-1
- latest version

* Fri Aug 10 2018 Caolán McNamara <caolanm@redhat.com> - 0.2.9-5
- Related: rhbz#1602602 fix more clang warnings

* Fri Aug 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.9-4
- Switch to %%ldconfig_scriptlets

* Fri Aug 10 2018 Caolán McNamara <caolanm@redhat.com> - 0.2.9-3
- Related: rhbz#1602602 fix more clang warnings

* Fri Aug 10 2018 Caolán McNamara <caolanm@redhat.com> - 0.2.9-2
- Related: rhbz#1602602 fix clang warnings

* Wed Aug 08 2018 Caolán McNamara <caolanm@redhat.com> - 0.2.9-1
- Resolves: rhbz#1602602 new version with covscan warnings fixed
- all cve fixes merged to that new upstream

* Wed Aug 08 2018 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-56
- Resolves: rhbz#1595490 make libwmf work again with recent urw-fonts

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8.4-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8.4-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Sep 12 2017 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-53
- Resolves: rhbz#1489844 CVE-2017-6362 remove afflicted but unused function

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8.4-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8.4-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 08 2017 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-50
- CVE-2016-9317, CVE-2016-10167, CVE-2016-10168

* Wed Oct 26 2016 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-49
- Resolves: rhbz#1388451 (CVE-2016-9011) check max claimed record len
            against max seekable position

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8.4-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 02 2015 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-47
- Related: rhbz#1227244 CVE-2015-4696 fix patch context

* Fri Aug 14 2015 Matthias Clasen <mclasen@redhat.com> - 0.2.8.4-46
- Rely on gdk-pixbuf2 file triggers

* Tue Jun 23 2015 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-45
- Related: rhbz#1227244 CVE-2015-4695 meta_pen_create heap buffer overflow
- Related: rhbz#1227244 CVE-2015-4696 wmf2gd/wmf2eps use after free

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-43
- Resolves: rhbz#1227244 CVE-2015-0848 heap overflow when decoding BMP images

* Tue Jun 02 2015 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-42
- Resolves: rhbz#1227244 CVE-2015-0848 heap overflow when decoding BMP images

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.2.8.4-41
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 04 2013 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-37
- Resolves: rhbz#925929 support aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.2.8.4-35
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.2.8.4-34
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 0.2.8.4-31
- Rebuild for new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 07 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-29
- drop bogus buildrequires

* Mon Dec 06 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-28
- Resolves: rhbz#660161 security issues

* Mon Oct 18 2010 Parag Nemade <paragn AT fedoraproject.org> - 0.2.8.4-27
- Merge-review cleanup (#226058)

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-26
- Move docs into -lite subpackage that all the rest require to
  fulfil subpackage licencing rules

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.2.8.4-25
- Remove explicit file deps

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.2.8.4-23
- Adapt to standalone gdk-pixbuf

* Fri Apr 16 2010 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-22
- Clarify licences

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Caolán McNamara <caolanm@redhat.com> - 0.2.8.4-20
- Resolves: CVE-2009-1364

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.8.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 13 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.2.8.4-18
- Split libwmflite (WMF parser) into -lite subpackage (#432651).
- Build with dependency tracking disabled.
- Convert docs to UTF-8.

* Wed Aug 29 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-17
- rebuild

* Thu Aug 02 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-16
- I wrote it and still had to check the headers to see if I had
  cut and pasted "and later" into then

* Thu May 24 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-15
- drop duplicate font metrics

* Thu Feb 15 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-14
- remove use of archaic autotools

* Fri Feb 09 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-13
- Resolves: rhbz#222734 no need for Makefiles in doc dirs

* Tue Jan 16 2007 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-12
- Resolves: rhbz#222734 no need for Makefiles in doc dirs

* Thu Nov 16 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-11
- Resolves: rhbz#215925 reduce exported symbols

* Fri Jul 14 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-10
- retweak for 64bit

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-9.1
- rebuild

* Wed Jul 12 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-9
- CVE-2006-3376 libwmf integer overflow

* Tue May 16 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-8
- rh#191971# BuildRequires

* Fri May  5 2006 Matthias Clasen <mclasen@redhat.com> 0.2.8.4-7
- Rebuild against the new GTK+
- Require GTK+ 2.9.0

* Tue May 02 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-6
- add a .pc and base libwmf-devel on pkg-config output

* Tue Feb 28 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-5
- rh#143096# extra deps according to libwmf-config

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2.8.4-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 19 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-4
- rh#178275# match srvg gtk2 _host usage for pixbuf loaders

* Tue Jan 03 2006 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-3
- add libwmf-0.2.8.4-fallbackfont.patch for rh#176620#

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 0.2.8.4-2.1
- rebuilt

* Wed Nov 23 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-2
- rh#173299# modify pre/post requires

* Thu Jul 28 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.4-1
- get patches merged upstream
- drop integrated libwmf-0.2.8.3-warnings.patch
- drop integrated libwmf-0.2.8.3-noextras.patch
- drop integrated libwmf-0.2.8.3-rh154813.patch

* Tue Jul 26 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-9
- rh#154813# wmf upsidedown, spec (what of is there is) says that
  this shouldn't happen, but...

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-8
- rebuild with gcc4

* Thu Dec 16 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-7
- RH#143096# No need for extra X libs to be linked against

* Tue Nov  2 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-6
- #rh137878# Extra BuildRequires

* Thu Oct  7 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-5
- #rh134945# Extra BuildRequires

* Wed Sep  1 2004 Caolan McNamara <caolanm@redhat.com> 0.2.8.3-4
- #131373# cleanup compiletime warnings

* Thu Jul  8 2004 Matthias Clasen <mclasen@redhat.com> - 0.2.8.3-3
- Update to use the new update-gdk-pixbuf-loaders script in gtk2-2.4.1-2

* Thu May 20 2004 Caolan McNamara <caolanm@redhat.com>
- Initial version
