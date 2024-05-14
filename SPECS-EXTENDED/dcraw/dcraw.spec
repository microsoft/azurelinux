Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Tool for decoding raw image data from digital cameras
Name: dcraw
Version: 9.28.0
Release: 10%{?dist}
License: GPLv2+
URL: https://www.dechifro.org/dcraw/
Source0: https://www.dechifro.org/dcraw/archive/dcraw-%{version}.tar.gz
Patch0: dcraw-9.21-lcms2-error-reporting.patch
Patch1: dcraw-CVE-2018-5801.patch
Patch2: dcraw-CVE-2017-13735.patch
Patch3: dcraw-CVE-2017-14608.patch
Patch4: dcraw-CVE-2018-19655.patch
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: libjpeg-devel
BuildRequires: lcms2-devel
BuildRequires: jasper-devel
Provides: bundled(dcraw)

%description
This package contains dcraw, a command line tool to decode raw image data
downloaded from digital cameras.

%prep
%autosetup -n dcraw

%build
%{__cc} %optflags $RPM_LD_FLAGS \
    -Wl,--no-as-needed \
    -lm -ljpeg -llcms2 -ljasper \
    -DLOCALEDIR="\"%{_datadir}/locale\"" \
    -o dcraw dcraw.c
# build language catalogs
for catsrc in dcraw_*.po; do
    lang="${catsrc%.po}"
    lang="${lang#dcraw_}"
    msgfmt -o "dcraw_${lang}.mo" "$catsrc"
done

%install
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 dcraw %{buildroot}%{_bindir}

# install language catalogs
for catalog in dcraw_*.mo; do
    lang="${catalog%.mo}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES"
    install -m 0644 "$catalog" "%{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/dcraw.mo"
done

install -d -m 0755 %{buildroot}%{_bindir} %{buildroot}%{_mandir}/man1
install -m 0644 dcraw.1 %{buildroot}%{_mandir}/man1/dcraw.1
# localized manpages
rm -f %{name}-man-files
touch %{name}-man-files
for manpage in dcraw_*.1; do
    lang="${manpage%.1}"
    lang="${lang#dcraw_}"
    install -d -m 0755 "%{buildroot}%{_mandir}/${lang}/man1"
    install -m 0644 "${manpage}" "%{buildroot}%{_mandir}/${lang}/man1/dcraw.1"
    echo "%%lang($lang) %%{_mandir}/${lang}/man1/*" >> %{name}-man-files
done

%find_lang %{name}

%files -f %{name}.lang -f %{name}-man-files
%{_bindir}/dcraw
%{_mandir}/man1/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.28.0-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Mar 20 2020 Josef Ridky <jridky@redhat.com> - 9.28.0-9
- Fix CVE-2018-19655

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.28.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Tom Stellard <tstellar@redhat.com> - 9.28.0-7
- Use __cc macro instead of hard-coding gcc

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.28.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Josef Ridky <jridky@redhat.com> - 9.28.0-5
- set new upstream url

* Thu Feb 21 2019 Josef Ridky <jridky@redhat.com> - 9.28.0-4
- Fix CVE-2017-13735 (#1488932)
- Fix CVE-2017-14608 (#1499687)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Josef Ridky <jridky@redhat.com> - 9.28.0-1
- New upstream release 9.28.0 (#1585348)
- Fix CVE-2018-5801 (#1557160)

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 9.27.0-8
- Use LDFLAGS from redhat-rpm-config

* Tue Feb 20 2018 Nils Philippsen <nils@tiptoe.de> - 9.27.0-7
- require gcc for building

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.27.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.27.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.27.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.27.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 05 2016 Than Ngo <than@redhat.com> - 9.27.0-2
- rebuild against new jasper-2.0.0

* Thu Jun 09 2016 Nils Philippsen <nils@redhat.com> - 9.27.0
- version 9.27.0
- use %%autosetup
- remove packaging cruft

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.25.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.25.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Nils Philippsen <nils@redhat.com> - 9.25.0-2
- add Provides: bundled(dcraw)
- don't manually specify, clean buildroot

* Wed May 20 2015 Nils Philippsen <nils@redhat.com> - 9.25.0-1
- version 9.25.0
- remove unnecessary check from CVE-2013-1438 patch
- avoid writing past array boundaries when reading certain raw formats
  (CVE-2015-3885)

* Wed Apr 08 2015 Nils Philippsen <nils@redhat.com> - 9.24.4-1
- version 9.24.4

* Sat Feb 14 2015 Nils Philippsen <nils@redhat.com> - 9.23.0-1
- version 9.23.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 30 2014 Nils Philippsen <nils@redhat.com> - 9.22-1
- version 9.22

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Nils Philippsen <nils@redhat.com> - 9.21-1
- report lcms2 errors

* Mon May 05 2014 Nils Philippsen <nils@redhat.com> - 9.21-1
- version 9.21

* Sat Apr 26 2014 Nils Philippsen <nils@redhat.com> - 9.20-2
- new upstream tarball with unchanged version number (RCS id 1.461 instead of
  1.458), obsoletes lcms2 patch

* Wed Jan 15 2014 Nils Philippsen <nils@redhat.com> - 9.20-1
- version 9.20

* Fri Dec 06 2013 Nils Philippsen <nils@redhat.com> - 9.19-4
- harden against corrupt input files (CVE-2013-1438)

* Fri Sep 13 2013 Nils Philippsen <nils@redhat.com> - 9.19-3
- build against the currently maintained version of lcms (2.x)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Nils Philippsen <nils@redhat.com> - 9.19-1
- version 9.19

* Mon Jun 03 2013 Nils Philippsen <nils@redhat.com> - 9.18-1
- version 9.18

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 9.17-2
- rebuild due to "jpeg8-ABI" feature drop

* Mon Jan 14 2013 Nils Philippsen <nils@redhat.com> - 9.17-1
- version 9.17

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 9.16-4
- rebuild against new libjpeg

* Thu Oct 18 2012 Nils Philippsen <nils@redhat.com> - 9.16-3
- upstream changed 9.16 tarball, adds support for Samsung NX1000, Sony
  DSC-RX100 models

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Nils Philippsen <nils@redhat.com> - 9.16-1
- version 9.16

* Tue Jun 19 2012 Nils Philippsen <nils@redhat.com> - 9.15-1
- version 9.15

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 9.12-2
- rebuild for gcc 4.7

* Thu Dec 22 2011 Nils Philippsen <nils@redhat.com> - 9.12-1
- version 9.12

* Wed Oct 12 2011 Nils Philippsen <nils@redhat.com> - 9.11-1
- version 9.11

* Mon Aug 01 2011 Nils Philippsen <nils@redhat.com> - 9.10-1
- version 9.10
- add BR: jasper-devel, link with jasper library

* Mon May 23 2011 Nils Philippsen <nils@redhat.com> - 9.08-1
- version 9.08

* Thu Apr 14 2011 Nils Philippsen <nils@redhat.com> - 9.07-1
- version 9.07

* Fri Mar 04 2011 Nils Philippsen <nils@redhat.com> - 9.06-1
- version 9.06

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 03 2010 Nils Philippsen <nils@redhat.com> - 9.04-1
- version 9.04

* Wed Jun 02 2010 Nils Philippsen <nils@redhat.com> - 9.01-1
- version 9.01
- color man page files with %%lang()

* Fri Feb 12 2010 Nils Philippsen <nils@redhat.com> - 8.99-1
- version 8.99

* Tue Aug 18 2009 Nils Philippsen <nils@redhat.com> - 8.96-1
- version 8.96

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 02 2009 Nils Philippsen <nils@redhat.com> - 8.91-1
- version 8.91

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.89-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 27 2008 Nils Philippsen <nphilipp@redhat.com> - 8.89-1
- version 8.89
- remove obsolete gps patch

* Mon Feb 25 2008 Nils Philippsen <nphilipp@redhat.com> - 8.82-1
- version 8.82

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 8.81-2
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Nils Philippsen <nphilipp@redhat.com> - 8.81-1
- version 8.81
- add support for GPS data (#428600, patch by Ulrich Drepper)

* Fri Nov 30 2007 Nils Philippsen <nphilipp@redhat.com> - 8.80-1
- version 8.80
- change license tag to GPLv2+

* Mon Feb 05 2007 Nils Philippsen <nphilipp@redhat.com> - 8.77-2
- rebuild with pristine source tarball

* Mon Feb 05 2007 Nils Philippsen <nphilipp@redhat.com> - 8.77-1
- version 8.77

* Mon Feb 05 2007 Nils Philippsen <nphilipp@redhat.com> - 8.53-2
- fix summary, use %%find_lang (#225678)

* Thu Feb 01 2007 Nils Philippsen <nphilipp@redhat.com> - 8.53-1
- upstream finally has a tarball, use that and its version (#209016)
- use dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.0.20060521-1.1
- rebuild

* Tue May 23 2006 Nils Philippsen <nphilipp@redhat.com> - 0.0.20060521-1
- program and manpage version of 2006-05-21
- use %%optflags
- change license tag to GPL
- use lcms

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.0.20051211-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.0.20051211-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 14 2005 Nils Philippsen <nphilipp@redhat.com>
- version of 2005-12-11
- manpage of 2005-09-29

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 02 2005 Nils Philippsen <nphilipp@redhat.com>
- version of 2005-02-27
- manpage of 2005-01-19

* Wed Dec 01 2004 Nils Philippsen <nphilipp@redhat.com>
- version of 2004-11-28
- initial build
