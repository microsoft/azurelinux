Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Czech man pages from the Linux Documentation Project
Name: man-pages-cs
Version: 0.18.20090209
Release: 31%{?dist}
# GPLv3 .. coreutils/
# BSD and MIT and Public Domain  .. openssh/
License: BSD and GPLv2 and GPLv3 and MIT and Public Domain
URL: http://tropikhajma.sweb.cz/man-pages-cs/
Source: http://tropikhajma.sweb.cz/%{name}/%{name}-%{version}.tar.lzma

Patch1:  man-pages-cs-01.patch
Patch2:  man-pages-cs-02.patch
Patch3:  man-pages-cs-03.patch
Patch4:  man-pages-cs-04.patch
Patch5:  man-pages-cs-05.patch
Patch6:  man-pages-cs-06.patch
Patch7:  man-pages-cs-07.patch
Patch8:  man-pages-cs-08.patch
Patch9:  man-pages-cs-09.patch
Patch10: man-pages-cs-10.patch
Patch11: man-pages-cs-11.patch
Patch12: man-pages-cs-0.18.20090209-socket.patch
Patch13: man-pages-cs-0.18.20090209-test.patch

Requires: man-pages-reader
Supplements: (man-pages and langpacks-cs)
BuildArch: noarch

%description
Manual pages from the Linux Documentation Project, translated into
Czech.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

%build
# coreutils directory contains newer version
rm ./procps/kill.1
rm ./procps/uptime.1
rm ./man-pages/man1/du.1
# links to ls - better version in coreutils directory
rm ./man-pages/man1/dir.1
rm ./man-pages/man1/vdir.1

# add deprecation warning to all man pages
warning="\
UPOZORNĚNÍ: Projekt českých manuálových stránek není nadále udržován.\n\
Tato manuálová stránka je zastaralá a informace zde uvedené mohou být\n\
neaktuální.\n\
Aktuální informace naleznete v nápovědě příkazu\n\
nebo anglické verzi manuálových stránek.\n\
"
for sec in 1 2 3 4 5 6 7 8; do
    find . -name "*.$sec" -not -path "*.pc*" -print | xargs sed -i "/^\.SH POPIS$/Ia $warning"
done

%install
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}/cs

%files
%license at/COPYING binutils/COPYING wget/COPYING grep/COPYING procps/COPYING coreutils/COPYING lynx/COPYING openssh/LICENCE procmain/COPYING cdp/COPYING gnu-ghostscript/COPYING bzip2/LICENSE gnu-ghostscript/LICENSE
%doc CONTRIB README README.Czech Changelog
%{_mandir}/cs/man*/*

%changelog
* Wed Jan 12 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.18.20090209-31
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.18.20090209-30
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.20090209-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.20090209-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.20090209-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.20090209-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.20090209-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.20090209-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.20090209-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Nikola Forró <nforro@redhat.com> - 0.18.20090209-22
- resolves: #1324481
  add deprecation warning to all man pages

* Sat Feb 27 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.18.20090209-21
- Add Supplements: for https://fedoraproject.org/wiki/Packaging:Langpacks guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.20090209-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.20090209-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.20090209-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.20090209-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.20090209-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 29 2012 Peter Schiffer <pschiffe@redhat.com> - 0.18.20090209-15
- .spec file cleanup

* Thu Jul 26 2012 Peter Schiffer <pschiffe@redhat.com> - 0.18.20090209-14
- resolves: #821661
  fixed typo in the test.1 man page

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.20090209-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.20090209-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.20090209-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.18.20090209-10
- Resolves: #650369
  fix socket.2 man-page

* Fri Apr 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.18.20090209-9
- add man-pages-reader dependence

* Wed Mar 17 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.18.20090209-8
- remove directories from the package

* Thu Feb 11 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.18.20090209-7
- add another patches created by Ludek Dolihal

* Mon Nov  3 2009 Ivana Varekova <varekova@redhat.com> - 0.18.20090209-6
- fix release tag

* Mon Nov  3 2009 Ivana Varekova <varekova@redhat.com> - 0.18.20090209-5
- add another patches created by Ludek Dolihal

* Mon Oct 12 2009 Ivana Varekova <varekova@redhat.com> - 0.18.20090209-4
- add another patches created by Ludek Dolihal

* Tue Sep 28 2009 Ivana Varekova <varekova@redhat.com> - 0.18.20090209-3
- add another patches created by Ludek Dolihal

* Tue Sep 15 2009 Ivana Varekova <varekova@redhat.com> - 0.18.20090209-2
- fix instalation part
- remove duplicate files
- add patches created by Ludek Dolihal

* Tue Sep 15 2009 Ivana Varekova <varekova@redhat.com> - 0.18.20090209-1
- update to 0.18.20090209

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.20080113-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.20080113-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Ivana Varekova <varekova@redhat.com> - 0.17.20080113-6
- update another part of coreutils man-pages (patches are from Kamil Dudka)

* Thu Dec  8 2008 Ivana Varekova <varekova@redhat.com> - 0.17.20080113-5
- update another part of coreutils man-pages (patches are from Kamil Dudka)

* Thu Dec  4 2008 Ivana Varekova <varekova@redhat.com> - 0.17.20080113-4
- update another part of coreutils man-pages (patches are from Kamil Dudka)

* Mon Dec  1 2008 Ivana Varekova <varekova@redhat.com> - 0.17.20080113-3
- update part of coreutils man-pages (patches are from Kamil Dudka)

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.17.20080113-2
- fix license tag

* Tue Jan 15 2008 Ivana Varekova <varekova@redhat.com> - 0.17.20080113-1
- update to 0.17.20080113

* Thu Nov 22 2007 Ivana Varekova <varekova@redhat.com> - 0.17.20070905-1
- update to 0.17.20070905
- patch to build in RPM_BUILD_ROOT (thanks Milan Kerslager)

* Fri Mar  2 2007 Ivana Varekova <varekova@redhat.com> - 0.16-7
- Resolves: 226121
  incorporate the package review feedback

* Fri Aug 11 2006 Ivana Varekova <varekova@redhat.com> - 0.16-6
- remove at.1 man page to right directory (#202049)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.16-5.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Aug  5 2005 Ivana Varekova <varekova@redhat.com> 0.16-5
- remove lastlog man page (man page is removed to shadow-utils)

* Wed Sep 29 2004 Adrian Havill <havill@redhat.com> 0.16-4
- rebuilt, n-v-r

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Akira TAGOH <tagoh@redhat.com> 0.16-2
- removed man.1 because the latest man contains it.

* Thu Feb 06 2003 Adrian Havill <havill@redhat.com>
- make iconv use UTF8 (#78717)
- update to 0.16

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 25 2002 Tim Powers <timp@redhat.com>
- remove the shadow manpage since it conflicts with shadow-utils now

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Aug 14 2001 Tim Powers <timp@redhat.com>
- rebuilt to hopefully fix the rpm verify problem

* Thu Aug  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- Own %%{_mandir}/cs

* Tue Apr  3 2001 Trond Eivind Glomsrød <teg@redhat.com>
- make pdf2dsc(1) use hyphen.cs, not hyphens.cs (#34181)

* Tue Dec 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 0.14
- new location

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 20 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Sun Jun 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- first build
