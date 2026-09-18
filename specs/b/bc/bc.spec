# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: GNU's bc (a numeric processing language) and dc (a calculator)
Name: bc
Version: 1.08.2
Release: 2%{?dist}
License: GPL-3.0-or-later
URL: https://www.gnu.org/software/bc/
Source0: https://ftp.gnu.org/gnu/bc/bc-%{version}.tar.gz
Source1: https://ftp.gnu.org/gnu/bc/bc-%{version}.tar.gz.sig
Source2: kevin_pizzini.asc
Patch1: bc-1.06-dc_ibase.patch
Patch2: bc-1.06.95-doc.patch
Patch3: bc-1.07.1-readline-echo-empty.diff
BuildRequires: bison
BuildRequires: ed
BuildRequires: flex
BuildRequires: gcc
BuildRequires: make
BuildRequires: readline-devel
BuildRequires: texinfo
# for gpg verification
BuildRequires: gnupg2

%description
The bc package includes bc and dc. Bc is an arbitrary precision
numeric processing arithmetic language. Dc is an interactive
arbitrary precision stack based calculator, which can be used as a
text mode calculator.

Install the bc package if you need its number handling capabilities or
if you would like to use its text mode calculator.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

%build
%configure --with-readline
%make_build

%install
%make_install
rm -f %{buildroot}/%{_infodir}/dir

%files
%license COPYING COPYING.LIB
%doc FAQ AUTHORS NEWS README Examples/
%{_bindir}/dc
%{_bindir}/bc
%{_mandir}/man1/bc.1*
%{_mandir}/man1/dc.1*
%{_infodir}/bc.info*
%{_infodir}/dc.info*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.08.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 1.08.2-1
- Update to 1.08.2 - rhbz#2368486

* Wed Mar 05 2025 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 1.08.1-3
- Verify gpg signature
- Change to https links
- Misc changes

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.08.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 06 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.08.1-1
- Update to 1.08.1 (#2335123)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 25 2023 Sérgio Basto <sergio@serjux.com> - 1.07.1-18
- Migrate to SPDX license format

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Aug 14 2021 Pádraig Brady <P@draigBrady.com> - 1.07.1-14
- Echo empty lines, useful for delimiting work

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.07.1-8
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Sep 13 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 1.07.1-4
- Cleanup spec

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.07.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Kevin Fenzi <kevin@scrye.com> - 1.07.1-1https://bugs.archlinux.org/task/53546
- Update to 1.07.1
- Fixes a bug that breaks kernel builds ( https://bugs.archlinux.org/task/53546 )

* Mon May 15 2017 Ondrej Vasik <ovasik@redhat.com> - 1.07-2
- build seems to be racy now, removing parallel build for now
- add build dep on "ed"

* Wed May 10 2017 Ondrej Vasik <ovasik@redhat.com> - 1.07-1
- new upstream version 1.07, dropped patches already appllied
  in usptream version

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.06.95-18
- Install COPYING[.*] using the %%license macro

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.06.95-17
- Rebuild for readline 7.x

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.06.95-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.06.95-14
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 02 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.06.95-11
- man and info patched - clarified scale after multiplication

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-8
- Minor spec cleanup

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-5
- Rebuilt for glibc bug#747377

* Thu Sep 08 2011 Ondrej Vasik <ovasik@redhat.com> 1.06.95-4
- do not mask SIGINT in dc when reading from stdin (#697340)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Ondrej Vasik <ovasik@redhat.com> 1.06.95-2
- fix possible segfault in arrays handling(debbug #586969)
- initialize f_void to work with math lib again(#664080)

* Thu Sep 24 2009 Ondrej Vasik <ovasik@redhat.com> 1.06.95-1
- update to upstream alpha 1.06.95 (in use in Gentoo, Slackware
  for quite a long time, marked stable there)
- removed already applied patches, fix small memory leak
  (gentoo patch)
- add missing BR for bison and texinfo

* Thu Aug 20 2009 Zdenek Prikryl <zprikryl@redhat.com> 1.06-36
- Don't complain if installing with --excludedocs (#515934)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.06-33
- Autorebuild for GCC 4.3

* Fri Jan 04 2008 Zdenek Prikryl <zprikryl@redhat.com> 1.06-32
- Added Examples directory into doc
- Added bc info file

* Fri Dec 14 2007 Stepan Kasal <skasal@redhat.com> 1.06-31
- Remove bc-1.06-flex.patch
- do not run autofoo
- fix the Licence tag

* Fri Dec 07 2007 Zdenek Prikryl <zprikryl@redhat.com> 1.06-30
- Package review (#225611)

* Tue Sep 18 2007 Zdenek Prikryl <zprikryl@redhat.com> 1.06-29
- update of source URI

* Wed Aug 22 2007 Zdenek Prikryl <zprikryl@redhat.com> 1.06-28
- fixed incorrect processing of decimal separator
- Resolves: #253729

* Thu Jul 26 2007 Zdenek Prikryl <zprikryl@redhat.com> 1.06-27
- dc accepts the input which contains wrong symbols of radix in same way like bc
- Resolves: #151844
- Added library string.h to remove warnings.

* Mon Feb 26 2007 Thomas Woerner <twoerner@redhat.com> 1.06-26
- removed grep and mktemp usage from post script, also the requires

* Mon Feb 26 2007 Karsten Hopp <karsten@redhat.com> 1.06-25
- flex supports -8 now (pmachata)

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 1.06-24
- fix buildroot
- remove trailing dot from summary
- fix post/preun requirements
- use make install DESTDIR=...
- convert changelog to utf-8
- use smp flags
- use 'flex -I' instead 'flex -I8' (not supported anymore)
- run autofoo stuff to update files for current automake

* Tue Jan 23 2007 Florian La Roche <laroche@redhat.com>
- scripts should never fail: rhbz#223677

* Mon Jan 22 2007 Thomas Woerner <twoerner@redhat.com> 1.06-22
- rebuild for ncurses

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.06-21
- rebuild
- add missing br automake

* Tue Jun  6 2006 Thomas Woerner <twoerner@redhat.com> 1.06-20
- added missing flex build require

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.06-19.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.06-19.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Thomas Woerner <twoerner@redhat.com> 1.06-19
- fixed rpm macro usage in chengelog (#137800)

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 1.06-18
- Rebuilt for new readline.

* Fri Oct  8 2004 Thomas Woerner <twoerner@redhat.com> 1.06-17.1
- added BuildRequires for readline-devel (#134699)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Aug 14 2003 Thomas Woerner <twoerner@redhat.com> 1.06-15
- fixed incorrect capitalization in bc info page (#89851)

* Tue Jun 17 2003 Thomas Woerner <twoerner@redhat.com> 1.06-14
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.06-11
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.06-8
- Rebuild

* Mon Feb  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.06-7
- s/Copyright/License/
- The %%doc file AUTHOR should be AUTHORS

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Sep  9 2001 Phil Knirsch <phil@redhat.de> 1.06-5
- Fixed a variable initialization problem in load.c which broke badly on S390.

* Fri May 11 2001 Preston Brown <pbrown@redhat.com> 1.06-4
- use mktemp, not the pid shell variable, in rpm scriptlets

* Fri May 11 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.06-3
- rebuild with new readline
- Add patch to fix compilation with recent readline versions

* Fri Dec 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Add COPYING, COPYING.LIB, FAQ, AUTHORS, NEWS, README

* Sun Nov 19 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to bc 1.06

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rebuild

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%makeinstall, %%configure, %%{_mandir}, %%{_infodir}
  and %%{_tmppath}  

* Wed May 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- added URL
- let build system handle man page gzipping

* Thu Apr 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- fixed bug 7145 (long commands -> coredump) 
- removed explicit stripping, it does this by itself anyway
- gzipped man-pages

* Thu Mar 30 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild with new readline (4.1)

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Rebuild with new readline (4.0)
- fix Source URL
- some spec file cleanups

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Jan 21 1999 Jeff Johnson <jbj@redhat.com>
- use %%configure

* Fri Sep 11 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.05a.

* Sun Jun 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Thu Jun 04 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.05 with build root.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 21 1998 Erik Troan <ewt@redhat.com>
- got upgrades of info entry working (I hope)

* Sun Apr 05 1998 Erik Troan <ewt@redhat.com>
- fixed incorrect info entry

* Wed Oct 15 1997 Donnie Barnes <djb@redhat.com>
- added install-info support

* Thu Sep 11 1997 Donald Barnes <djb@redhat.com>
- upgraded from 1.03 to 1.04

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
