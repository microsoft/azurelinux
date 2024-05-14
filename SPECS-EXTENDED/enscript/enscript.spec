Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: A plain ASCII to PostScript converter
Name: enscript
Version: 1.6.6
Release: 25%{?dist}
License: GPLv3+
URL: https://www.gnu.org/software/enscript
# Tarball exists nowhere. You have to obtain it via:
# $ git clone git://git.savannah.gnu.org/enscript.git
# $ git archive --format=tar --prefix=%%{name}-%%{version}/ v%%{version} | gzip > %%{name}-%%{version}.tar.gz
Source0: %{_distro_sources_url}/%{name}-%{version}.tar.gz
#https://neugierig.org/software/ruby/ruby-enscript.tar.gz
Source1: %{_distro_sources_url}/%{name}-ruby-1.6.4.tar.gz
#https://home.raxnet.net/downloads/viewcvs/php.st
Source2: enscript-php-1.6.4.st

# RH #61294
Patch3: enscript-1.6.1-locale.patch

# RH #224548
Patch8: enscript-wrap_header.patch

Patch10:enscript-1.6.4-rh457720.patch
Patch12:enscript-rh477382.patch
Patch13:enscript-build.patch
Patch14:enscript-manfixes.patch
Patch15: enscript-bufpos-crash.patch
# 1664367 - adding support for 2 other encodings, enscript cannot print f.e. euro symbol
# without it
# rhbz: https://bugzilla.redhat.com/show_bug.cgi?id=1664367
# upstream patch: https://lists.gnu.org/archive/html/bug-enscript/2018-04/msg00008.html
Patch16: 0001-enscript-newencodings.patch
# enscript bundles some gnulib source files, so some issues or CVEs in gnulib can be
# present in enscript
# gnulib CVE: https://bugzilla.redhat.com/show_bug.cgi?id=1635896
Patch17: enscript-CVE-vasnprintf.patch

# gcc is no longer in buildroot by default
BuildRequires: gcc
BuildRequires: autoconf, automake, gettext
BuildRequires: gettext-devel

# our downstreamed gnulib bundles some gnulib files, so we need to provide
# this one. I'm not sure why we have gnulib files there, because upstream
# does not have these files. The correct way would be to extract these files,
# fix Makefiles to link correct gnulib and requires gnulib-'something' in spec
# file, but enscript is lowly used+low maintenance+mostly dead upstream package,
# so there is a little merit of doing it...
Provides: bundled(gnulib)

%description
GNU enscript is a free replacement for Adobe's Enscript
program. Enscript converts ASCII files to PostScript(TM) and spools
generated PostScript output to the specified printer or saves it to a
file. Enscript can be extended to handle different output media and
includes many options for customizing printouts

%prep
%setup -q
%patch 3 -p1 -b .locale
%patch 8 -p1 -b .wrap_header
%patch 10 -p1 -b .rh457720
%patch 12 -p1 -b .rh477382
%patch 13 -p1 -b .build
%patch 14 -p1 -b .manfixes
%patch 15 -p1 -b .bufpos-crash
# 1664367 - [RFE] Add support for 885915 encoding in enscript
%patch 16 -p1 -b .newencodings
# CVE in gnulib
%patch 17 -p1 -b .vasnprintf

%{__tar} -C states/hl -zxf %{SOURCE1} ruby.st
install -pm 644 %{SOURCE2} states/hl/php.st

%build
autoreconf -fiv
export CPPFLAGS='-DPROTOTYPES'
%configure --with-media=Letter
make %{?_smp_mflags}


%install
mkdir -p %{buildroot}%{_datadir}/locale/{de,es,fi,fr,nl,sl}/LC_MESSAGES
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_datadir}/info/dir

%find_lang %name

# XXX note doubled %% in sed script below.
(cd %{buildroot};find .%{_datadir}/enscript/* \! -type d) | \
	sed -e 's,^\.,,' | sed -e 's,*font.map,%%config &,' > share.list
(cd %{buildroot};find .%{_datadir}/enscript/* -type d) | \
	sed -e 's,^\.,,' | sed -e 's,^,%dir ,' >> share.list

( cd %{buildroot}
  ln .%{_prefix}/bin/enscript .%{_prefix}/bin/nenscript
)

%find_lang %{name} %{name}.lang

for all in README THANKS; do
	iconv -f ISO88591 -t UTF8 < $all > $all.new
	touch -r $all $all.new
	mv $all.new $all
done

%files -f %{name}.lang -f share.list
%license COPYING
%doc AUTHORS ChangeLog docs/FAQ.html NEWS README README.ESCAPES THANKS TODO
%{_bindir}/*
%{_mandir}/man1/*
%dir %{_datadir}/enscript
%{_infodir}/%{name}*
%config(noreplace) %{_sysconfdir}/enscript.cfg

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.6-25
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.6-24
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.6-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Zdenek Dohnal <zdohnal@redhat.com> - 1.6.6-19
- 1664367 - [RFE] Add support for 885915 encoding in enscript
- remove old Obsoletes/Provides
- fix gnulib CVE

* Tue Jul 24 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.6.6-18
- correcting license

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.6.6-16
- remove install-info, info package does it now automatically when any package puts a file into %%_infodir

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.6.6-15
- gcc is no longer in buildroot by default

* Thu Feb 08 2018 Zdenek Dohnal <zdohnal@redhat.com> - 1.6.6-14
- remove old stuff https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/MRWOMRZ6KPCV25EFHJ2O67BCCP3L4Y6N/

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Tim Waugh <twaugh@redhat.com> - 1.6.6-4

- Fixed word-wrapping crash in tokenizer (bug #870639).
* Thu Apr 04 2013 Adam Tkac <atkac redhat com> - 1.6.6-3
- some manpage fixes

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 26 2012 Adam Tkac <atkac redhat com> - 1.6.6-1
- update to 1.6.6
- paches merged
  - enscript-1.6.4-hilight.patch
  - enscript-1.6.4-rh457719.patch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 08 2010 Adam Tkac <atkac redhat com> - 1.6.5.2-3
- BR: s/gettext-autopoint/gettext-devel (#631147)

* Sat Jul 17 2010 Dan Horák <dan[at]danny.cz> - 1.6.5.2-2
- add gettext-autopoint to BuildRequires

* Wed Jun 02 2010 Adam Tkac <atkac redhat com> - 1.6.5.2-1
- update to 1.6.5.2

* Thu May 20 2010 Adam Tkac <atkac redhat com> - 1.6.5.1-1
- update to 1.6.5.1
- patches merged
  - enscript-1.6.1-config.patch
  - enscript-doublefree.patch
  - enscript-1.6.1-CAN-2004-1185.patch
  - enscript-1.6.1-CAN-2004-1186.patch
  - enscript-CVE-2008-3863+CVE-2008-4306.patch
- license changed to GPLv3+
- add gettext to BuildRequires

* Mon Dec 14 2009 Adam Tkac <atkac redhat com> - 1.6.4-16
- merge review related fixes (#225729)

* Mon Nov 30 2009 Adam Tkac <atkac redhat com> - 1.6.4-15
- ship postscript files with .eps extension (#505775)
- merge review fixes (#225729)
- improve enscript-1.6.1-config.patch

* Mon Aug 10 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.6.4-14
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 03 2008 Adam Tkac <atkac redhat com> 1.6.4-11
- fixed various buffer overflows (CVE-2008-3863, CVE-2008-4306)

* Fri Aug 08 2008 Adam Tkac <atkac redhat com> 1.6.4-10
- updated patches due rpm 4.6
- enscript -w is handled well (#457719)
- mkafmmap -V is handled well (#457720)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.6.4-9
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Adam Tkac <atkac redhat com> 1.6.4-8
- rebuild (BuildID feature)
- change license to GPLv2

* Mon Feb 12 2007 Adam Tkac <atkac redhat com> 1.6.4-7
- wrap_header patch had problems with around 70 characters long headers

* Fri Jan 26 2007 Adam Tkac <atkac redhat com> 1.6.4-6
- wrap_header patch has been improved

* Tue Dec 19 2006 Adam Tkac <atkac redhat com> 1.6.4-5
- fixed long-header patch

* Fri Sep 01 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 1.6.4-4
- enscript now wrapes long header instead of truncating

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.6.4-3.1
- rebuild

* Tue Jun 27 2006 Florian La Roche <laroche@redhat.com> - 1.6.4-3
- /sbin/install-info is required for scripts

* Fri Feb 17 2006 Jitka Kudrnacova <jkudrnac@redhat.com> 1.6.4-2
- added new highlighters (#177336)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.6.4-1.1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.6.4-1.1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Jitka Kudrnacova <jkudrnac@redhat.com> 1.6.4-1.1
- fixed URL in the description (bug #178444)

* Fri Dec 23 2005 Tim Waugh <twaugh@redhat.com> 1.6.4-1
- 1.6.4 (bug #176349).  No longer need tmp, CAN-2004-1184, demunge patches.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  8 2005 Tim Waugh <twaugh@redhat.com> 1.6.1-31
- Fixed po files (bug #149859).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 1.6.1-30
- Rebuild for new GCC.

* Sat Jan 29 2005 Tim Waugh <twaugh@redhat.com> 1.6.1-29
- Applied patch to fix CAN-2004-1186 (bug #144684).
- Applied patch to fix CAN-2004-1185 (bug #144684).
- Backported patch to fix CAN-2004-1184 (bug #144684).

* Mon Sep 27 2004 Tim Waugh <twaugh@redhat.com> 1.6.1-28
- Fixed double-free problem (bug #132964).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Nov  3 2003 Tim Waugh <twaugh@redhat.com>
- Removed mail patch.  It was included to be more compatible with an
  lpr we no longer ship.  Fixes bug #108762.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Tim Waugh <twaugh@redhat.com> 1.6.1-20
- Fix URL (bug #65278).

* Wed Apr  3 2002 Tim Waugh <twaugh@redhat.com> 1.6.1-19
- Fix license (bug #62573).

* Mon Mar 18 2002 Tim Waugh <twaugh@redhat.com> 1.6.1-18
- Fix locale issues (bug #61294).

* Mon Feb 04 2002 Tim Waugh <twaugh@redhat.com> 1.6.1-17
- Rebuild in new environment.

* Mon Jan 14 2002 Tim Waugh <twaugh@redhat.com> 1.6.1-16.2
- Use tmpfile instead of tmpnam or tempnam (bug #57704).
- Built for Red Hat Linux 7.x.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.6.1-16
- automated rebuild

* Wed Dec 19 2001 Tim Waugh <twaugh@redhat.com> 1.6.1-15
- Own %%{_datadir}/enscript directory (bug #56974).

* Mon Jun 25 2001 Crutcher Dunnavant <crutcher@redhat.com> 1.6.1-14
- add optional mail paramater, closing bug #17750
- patch from marques@cs.cornell.edu

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Feb 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- langify

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- rebuild to gzip man pages

* Wed Mar 24 1999 Erik Troan <ewt@redhat.com>
- marked /usr/share/enscript/font.map as a config file

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- added documentation to the RPM

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.
- include i18n locales.

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Wed Nov 11 1998 Preston Brown <pbrown@redhat.com>
- translations ripped out, slight cleanup to build section.

* Mon Nov 09 1998 Preston Brown <pbrown@redhat.com>
- initial build of GNU enscript to replace nenscript.
