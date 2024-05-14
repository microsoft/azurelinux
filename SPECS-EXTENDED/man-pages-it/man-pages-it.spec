Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Italian man (manual) pages from the Linux Documentation Project
Name: man-pages-it
Version: 4.08
Release: 11%{?dist}
# inherit the license tags from the man-pages package
License: GPL+ and GPLv2 and GPLv2+ and LGPLv2+ and GPLv3+ and BSD and MIT and Copyright only and IEEE
URL: https://www.pluto.linux.it/ildp/man/
%global extra_name %{name}-extra
%global extra_ver 0.5.0
# The tarball of the new 3.15 version has a slighly strange file name, not
# %%{name}-%%{version}.tar.gz anymore ...
Source0: ftp://ftp.pluto.it/pub/pluto/ildp/man/%{name}-%{version}.tar.xz
BuildArch: noarch
Obsoletes: %{extra_name} < 2.80
Provides: %{extra_name} = %{version}-%{release}
Summary(it): Pagine del manuale in italiano
Requires: man-pages-reader
Supplements: (man-pages and langpacks-it)

%description
Manual pages from the Linux Documentation Project, translated into Italian.

%description -l it
Questo pacchetto è la traduzione a cura dell'Italian Linux Documentation
Project (ILDP) del pacchetto man page ufficiale mantenuto e distribuito da
Michael Kerrisk. La versione di questo pacchetto garantisce che le man page
contenute sono state aggiornate alla versione corrispondente del pacchetto
ufficiale. 

%prep
%setup -q

for i in *; do
    if [ -f $i ]; then
        iconv -f ISO8859-15 -t UTF-8 $i -o $i.utf8
        mv $i.utf8 $i
    fi
done
for i in man*/*; do
    if [ -f $i ]; then
        iconv -f ISO8859-15 -t UTF-8 $i -o $i.utf8
        mv $i.utf8 $i
    fi
done

# https://bugzilla.redhat.com/show_bug.cgi?id=1334286
# https://savannah.nongnu.org/bugs/?42917
# Non-free because there is a (subjective) restriction on modification
rm ./man-pages/man2/sysinfo.2

%build
# nothing to build here

%install
make prefix=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/it
cp -R */man* $RPM_BUILD_ROOT/%{_mandir}/it
rm -rf $RPM_BUILD_ROOT/%{_mandir}/it/'man??'
rm -rf $RPM_BUILD_ROOT/share/man
rm -f $RPM_BUILD_ROOT/%{_mandir}/it/man1/man2html.1*
rm -f $RPM_BUILD_ROOT/%{_mandir}/it/man1/hman.1*

%files
%doc CHANGELOG LEGGIMI README description
%{_mandir}/it/man*/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.08-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Sep 11 2018 Mike FABIAN <mfabian@redhat.com> - 4.08-7
- Fix invalid license tag LGPLV2+ -> LGPLv2+

* Mon Sep 10 2018 Mike FABIAN <mfabian@redhat.com> - 4.08-6
- Resolves: rhbz#1626344 - Fix Supplements tag for langpacks-it

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Mike FABIAN <mfabian@redhat.com> - 4.08-1
- update to 4.08

* Fri Jun 03 2016 Mike FABIAN <mfabian@redhat.com> - 4.06-1
- update to 4.06

* Thu May 19 2016 Mike FABIAN <mfabian@redhat.com> - 4.03-1
- update to 4.03
- Resolves: rhbz#1337560 - file conflict between dpkg-dev package
  and man-pages-it package
- Resolves: rhbz#1334286 - man-pages-it included non-free docs.

* Sun Feb 28 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.56-6
- Add Supplements: for https://fedoraproject.org/wiki/Packaging:Langpacks guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.56-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.56-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 28 2014 Mike FABIAN <mfabian@redhat.com> - 3.56-2
- upstream tar ball man-pages-it-3.56.tar.xz has been changed, some files had been missing

* Mon Jan 27 2014 Mike FABIAN <mfabian@redhat.com> - 3.56-1
- update to 3.56.

* Wed Nov 13 2013 Mike FABIAN <mfabian@redhat.com> - 3.15-3
- Resolves: rhbz#1029225 Can't install lxc-templates due to conflict between dpkg and man-pages-it

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jan 30 2013 Mike FABIAN <mfabian@redhat.com> - 3.15-1
- Resolves: #906215 - man-pages-it package contains many man-pages
  which are not translated to Italian but are in English
- update to 3.15. The update contains:
- all the man pages from the sections man0p, man1p, and man3p are gone.
  But that is no problem, these were the untranslated English versions anyway!
- new manpages: abc2abc.1 abc2ly.1 abcqps.1 dselect.1 utmpx.5
- removed manpages: dselect.8

* Mon Nov 26 2012 Jens Petersen <petersen@redhat.com> - 2.80-13
- inherit the license tags of the man-pages package (#880076)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.80-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 31 2012 Ding-Yi Chen <dchen@redhat.com> - 2.80-11
- Remove hman.1 as well.

* Tue May 29 2012 Ding-Yi Chen <dchen@redhat.com> - 2.80-10
- Resolves: #825918 - man-pages-it : Conflicts with man2html

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.80-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.80-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 04 2010 Ding-Yi Chen <dchen@redhat.com> - 2.80-7
- Bug 582912 - man-pages-it: Change requires tag from man to man-pages-reader

* Wed Mar 03 2010 Ding-Yi Chen <dchen@redhat.com> - 2.80-6
- Resolves: #560507 [man-pages-it] Package wrangler fix

* Wed Mar 03 2010 Ding-Yi Chen <dchen@redhat.com> - 2.80-5
- Resolves: #560507 [man-pages-it] Package wrangler fix
- Fixed Fedora 569443 [man-pages-it] Wrong directory ownership

* Mon Feb 01 2010 Ding-Yi Chen <dchen@redhat.com> - 2.80-4
- Resolves: #560507
  [man-pages-it] Package wrangler fix
- Remove comments of extra subpackage, as upstream already merge them.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.80-3.1
- Rebuilt for RHEL 6

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jun 26 2008 Ding-Yi Chen <dchen@redhat.com> - 2.80-1
- [Bug 451982] New: RFE: New version of man-pages-it available
- Obsoletes man-pages-it-extra

* Thu Dec 06 2007 Ding-Yi Chen <dchen@redhat.com> - 2.65-7
- [Bug 226125] Merge Review: man-page-it (Comment 13)

* Thu Dec 06 2007 Ding-Yi Chen <dchen@redhat.com> - 2.65-6
- [Bug 226125] Merge Review: man-page-it (Comment 8)

* Thu Dec 06 2007 Ding-Yi Chen <dchen@redhat.com> - 2.65-5
- Fix improper format of SPEC

* Wed Dec 05 2007 Ding-Yi Chen <dchen@redhat.com> - 2.65-4
- Change the Licence from "Freely redistributable without restriction" to IEEE

* Tue Dec 04 2007 Ding-Yi Chen <dchen@redhat.com> - 2.65-3
- [Bug 226125] Merge Review: man-page-it

* Thu Oct 25 2007 Ding-Yi Chen <dchen@redhat.com> - 2.65-2
- [Bug 335931] man-pages-it package is 6 years old
- Add Italian summaries and descriptions

* Mon Oct 22 2007 Ding-Yi Chen <dchen@redhat.com> - 2.65-0
- [Bug 335931] man-pages-it package is 6 years old

* Wed Oct 10 2007 Ding-Yi Chen <dchen@redhat.com> - 0.3.0-18
- [Bug 236116] Unsupported programs in man-pages-it
- remove celibacy.1 and sex.6

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-17.1.gz
- rebuild

* Thu Mar 23 2006 Karsten Hopp <karsten@redhat.de> 0.3.0-17
- remove vim.1, provided by the vim-common package

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Apr 07 2005 Peter Vrabec <pvrabec@redhat.com> 0.3.0-16
- newgrp man page removed, will be provided by shadow-utils

* Tue Sep 28 2004 Leon Ho <llch@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Akira TAGOH <tagoh@redhat.com> 0.3.0-13
- removed apropos.1, man.1, whatis.1, man.config.5, and makewhatis.8, because the latest man contains those manpages.

* Tue Feb 11 2003 Phil Knirsch <pknirsch@redhat.com> 0.3.0-12
- Convert all manpages to utf-8.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.3.0-11
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 0.3.0-10
- remove unpackaged files from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.3.0-7
- Add URL

* Wed Apr  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add patch to fix roff errors in multiple man pages

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 20 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Mon Jun 19 2000 Matt Wilson <msw@redhat.com>
- defattr root

* Sun Jun 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_mandir}/it and %%{_tmppath} 

* Mon May 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- first build
