Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Polish man pages from the Linux Documentation Project
Name: man-pages-pl
Version: 0.7
Release: 11%{?dist}
# Multiple man pages are distributed under different licenses.
License: GPL+ and BSD and MIT and GFDL
URL: https://sourceforge.net/projects/manpages-pl/
Source: https://sourceforge.net/projects/manpages-pl/files/manpages-pl-%{version}.tar.bz2

Requires: man-pages-reader
Supplements: (man-pages and langpacks-pl)

BuildArch: noarch

BuildRequires: perl-interpreter

%description
Manual pages from the Linux Documentation Project, translated into
Polish.

%prep
%setup -q -n manpages-pl-%{version}

%build
# nothing to build

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# these man pages are provided by procps-ng package
%{__rm} -f $RPM_BUILD_ROOT%{_mandir}/pl/man1/kill.1*
%{__rm} -f $RPM_BUILD_ROOT%{_mandir}/pl/man1/uptime.1*
%{__rm} -f $RPM_BUILD_ROOT%{_mandir}/pl/man8/pidof.8*

%files
%doc AUTHORS CHANGELOG COPYRIGHT README VERSION
%license licenses
%{_mandir}/pl/man*/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.7-11
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.7-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 27 2018 Nikola Forró <nforro@redhat.com> - 1:0.7-5
- really remove man pages provided by procps-ng package

* Tue Mar 27 2018 Nikola Forró <nforro@redhat.com> - 1:0.7-4
- remove man pages provided by procps-ng package
  resolves: #1560738

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 14 2017 Nikola Forró <nforro@redhat.com> - 1:0.7-1
- update to 0.7
  resolves: #1422065

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jun 13 2016 Tom Callaway <spot@fedoraproject.org> - 1:0.6-5
- remove non-free man pages (bz1334291)

* Sat Feb 27 2016 Parag Nemade <pnemade AT redhat DOT com> - 1:0.6-4
- Add Supplements: for https://fedoraproject.org/wiki/Packaging:Langpacks guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Nov 13 2014 jchaloup <jchaloup@redhat.com> - 1:0.6-1
- updated to 0.6
  resolves: #1163168

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 16 2013 Peter Schiffer <pschiffe@redhat.com> - 1:0.5-1
- resolves: #1013307
  updated to 0.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun  7 2013 Peter Schiffer <pschiffe@redhat.com> - 1:0.4-1
- resolves: #967817
  updated to 0.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 03 2012 Peter Schiffer <pschiffe@redhat.com> - 1:0.3-2
- minor .spec file cleanup

* Mon Jul 30 2012 Peter Schiffer <pschiffe@redhat.com> - 1:0.3-1
- resolves: #844054
  update to 0.3

* Mon Jul 23 2012 Peter Schiffer <pschiffe@redhat.com> - 1:0.2-1
- resolves: #823199
  updated tarball from the new upstream project
- resolves: #842284
  file conflict fixed with update to the new tarball

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun  8 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 0.24-12
- Resolves: #701467
  update sigaction.2 manual page
  the patch was created by Mira Bielecka, thanks

* Mon Aug 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.24-11
- remove links to nothing

* Fri Apr 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.24-10
- add man-pages-reader dependence

* Wed Mar 17 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.24-9
- remove directories from the package

* Fri Oct  9 2009 Ivana Varekova <varekova@redhat.com> - 0.24-8
- fix source tag

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.24-5
- fix license tag

* Mon Dec 17 2007 Ivana Varekova <varekova@redhat.com> - 0.24-4
- remove groupmems.8 (#425778)

* Fri Mar  2 2007 Ivana Varekova <varekova@redhat.com> - 0.24-3
- Resolves: 226128
  incorporate package review feedback

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.24-2.1
- rebuild

* Thu Apr 06 2006 Karsten Hopp <karsten@redhat.de> 0.24-2
- remove some vim man pages provided by current vim

* Mon Jan  9 2006 Ivana Varekova <varekova@redat.com> 0.24-1
- update source
- add pidof patch (created by Marcin Garski)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 26 2005 Ivana Varekova <varekova@redhat.com> 0.23-7
- login.defs man page removed (bug 169181), will be provided 
  by shadow-utils

* Thu Apr 07 2005 Peter Vrabec <pvrabec@redhat.com> 0.23-6
- newgrp man page removed, will be provided by shadow-utils

* Thu Nov 18 2004 Adrian Havill <havill@redhat.com> 0.23-4
- remove mc.1 (#138865)

* Wed Sep 29 2004 Adrian Havill <havill@redhat.com> 0.23-2
- bump n-v-r, rebuild

* Wed Apr 07 2004 Karsten Hopp <karsten@redhat.com>
- use new tarball from ptm.linux.pl (#112253)
- disable rofffix patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Akira TAGOH <tagoh@redhat.com> 0.22-14
- removed apropos.1, man.1, whatis.1, and man.config.5, because the latest man contains those manpages.

* Tue Feb 11 2003 Phil Knirsch <pknirsch@redhat.com> 0.22-13
- Convert all manpages to utf-8.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 25 2002 Tim Powers <timp@redhat.com>
- remove man pages which conflict with shadow-utils

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Aug  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- Own %%{_mandir}/pl

* Wed Apr  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- fix roff errors in various man pages (#34189)
- remove lisp-tut.5 - it's beyond repair and needs rewriting

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 20 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Mon Jun 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't include rpm manpage, it's included with rpm

* Sun Jun 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed typo in description
* Sun Jun 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- first build
