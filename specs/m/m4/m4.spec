# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: GNU macro processor
Name: m4
Version: 1.4.21
Release: 1%{?dist}
License: GPL-3.0-or-later AND GFDL-1.3-or-later AND FSFULLR AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND GPL-3.0-or-later WITH Texinfo-exception AND GPL-2.0-or-later WITH Autoconf-exception-generic AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND MIT
Source0: https://ftp.gnu.org/gnu/m4/m4-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/m4/m4-%{version}.tar.xz.sig
URL: https://www.gnu.org/software/m4/
BuildRequires: make
BuildRequires: gcc autoconf automake
BuildRequires: gettext
%ifarch ppc ppc64
BuildRequires: texinfo
%endif
# Gnulib bundled - the library has been granted an exception, see https://fedorahosted.org/fpc/ticket/174
# Gnulib is not versioned, see m4 ChangeLog for approximate date of Gnulib copy
Provides: bundled(gnulib)

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%prep
%setup -q
chmod 644 COPYING

%build
%configure
%make_build

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%find_lang %{name}

%check
make %{?_smp_mflags} check

%files -f %{name}.lang
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{_bindir}/m4
%{_infodir}/*
%{_mandir}/man1/m4.1*

%changelog
* Mon Feb 09 2026 Frédéric Bérat <fberat@redhat.com> - 1.4.21-1
- Update to m4-1.4.21 (#2437444)

* Fri Nov 14 2025 Florian Weimer  <fweimer@redhat.com> - 1.4.20-3
- Update License tag with build system licenses

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 12 2025 Frédéric Bérat <fberat@redhat.com> - 1.4.20-1
- Update to m4-1.4.20 (#2365446)

* Tue Feb 04 2025 Frédéric Bérat <fberat@redhat.com> - 1.4.19-12
- Add -std=gnu17 to CFLAGS to fix FTBFS until new m4 release gets out (#2340807)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Aug 08 2023 Frederic Berat <fberat@redhat.com> - 1.4.19-7
- Migrate to SPDX licenses (#2222092).

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 31 2021 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.19-1
- Update to m4-1.4.19
  Resolves: #1965719

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 13 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.18-16
- Drop workaround introduced in previous release
  Resolves: #1864107

* Thu Aug 06 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.18-15
- Disable %%check on ppc64le (workaround for FTBFS)
  Resolves: #1864107

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-14
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 02 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.18-8
- Work around change in glibc
  Resolves: #1573342

* Thu Feb 22 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.18-7
- Add BuildRequires gcc
- Remove Group tag

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Stephen Gallagher <sgallagh@redhat.com> - 1.4.18-2
- Add missing %%license macro
  Resolves: #1418521

* Mon Jan 02 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.18-1
- Update to m4-1.4.18
  Resolves: #1409340

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.17-8
- Fix m4 FTBFS in rawhide
  Resolves: #1239665

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 10 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.17-4
- Fix ppc64le test fails
  Resolves: #1083434

* Mon Dec 09 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.17-3
- Buildrequire texinfo for ppc architecture
  Resolves: #1038230

* Tue Nov 12 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.17-2
- Fix installation of info documentation
  Resolves: #1020194

* Tue Nov 05 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.17-1
- Update to m4-1.4.17
  Resolves: #1010895
- Fix bogus date in the %%changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 04 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-8
- Rerun autoreconf
  Resolves: #926109

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-6
- Fix issues found by fedora-review utility in the spec file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-4
- Fix handling of bundled gnulib in the spec file
  Resolves: #821777

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 20 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-2
- Temporarily fix readlink test to accept EINVAL also
  Resolves: #739189

* Wed Mar 02 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.16-1
- Update to m4-1.4.16

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep  7 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.15-1
- Update to m4-1.4.15 (removed include patch, already applied in upstream source)
  Resolves: #630709

* Mon Mar  1 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.14-1
- Update to m4-1.4.14
  Resolves: #568339

* Thu Sep  3 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.13-4
- Fix errors installing m4 with --excludedocs
  Resolves: #516013

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.4.13-3
- Use xz compressed upstream tarball.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 27 2009 Stepan Kasal <skasal@redhat.com> - 1.4.13-1
- new upstream release
- drop the ununsed Source1: %%{SOURCE0}.sig
- enable %%check again

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov  5 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.12-1
- Update to m4-1.4.12
  Resolves: #469944
- Merge review
  Resolves: #226115

* Wed Apr 23 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.11-1
- Update to m4-1.4.11 (removed vasnprintf patch, it's included in
  upstream source)
  Resolves: #443589

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.10-3
- Fix Buildroot

* Mon Dec 17 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.10-2
- Fix vasnprintf puts %%n into a writeable format string in all cases
  Resolves: #345651

* Wed Aug 22 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.10-1
- Update to m4-1.4.10
- Fix license to GPL version 3 or later

* Tue Jun  5 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-1
- Update to m4-1.4.9

* Thu Apr 19 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.8-2
- Rebuild

* Sun Nov 26 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.8-1
- Update to m4-1.4.8

* Wed Oct 25 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.7-2
- Drop %%check again.  SIGPIPE is set to SIG_IGN in mock, which breaks the
  sysval test.

* Tue Oct 24 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.7-1
- Update to m4-1.4.7
- Add %%check
- Fix a rpmlint warning about Summary:

* Mon Jul 17 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.5-3
- Use the install-info scriptlets recommended in the Fedora Extras wiki
- Move $RPM_BUILD_ROOT cleaning from %%prep to %%install

* Mon Jul 17 2006 Tomas Mraz <tmraz@redhat.com> - 1.4.5-2
- remove infodir/dir so it isn't included in the package

* Mon Jul 17 2006 Miloslav Trmac <mitr@redhat.com> - 1.4.5-1
- Update to m4-1.4.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.4.4-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 22 2005 Miloslav Trmac <mitr@redhat.com> - 1.4.4-1
- Update to m4-1.4.4

* Sun Sep 18 2005 Miloslav Trmac <mitr@redhat.com> - 1.4.3-2
- Ship COPYING and ChangeLog

* Fri Apr  1 2005 Miloslav Trmac <mitr@redhat.com> - 1.4.3-1
- Update to m4-1.4.3

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.4.2-3
- build with gcc-4

* Sun Feb 27 2005 Florian La Roche <laroche@redhat.com>
- rebuild

* Sun Dec 12 2004 Miloslav Trmac <mitr@redhat.com> - 1.4.2-1
- Update to m4-1.4.2

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add french translation file

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- do not strip apps

* Fri Jun 14 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- use _infodir on popular request #47465

* Sat Jan 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add URL tag
- improved spec file
- add hack to update config.guess config.sub
- fix to build with newer autoconf versions

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Feb 13 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- signal patch is not necessary anymore
- fix printf buffer overflow problem

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Matt Wilson <msw@redhat.com>
- added defattr

* Mon Jun  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHS compliance
- 1.4.1
- some fixes to spec file

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- Manhattan build

* Tue Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- added info file handling and BuildRoot

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

