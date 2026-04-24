# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A utility for displaying and/or setting hard disk parameters
Name: hdparm
Version: 9.65
Release: 10%{?dist}
License: hdparm
URL:    https://sourceforge.net/projects/%{name}/
Source: https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0: %{name}-9.60-ditch_dead_code.patch
Patch1: %{name}-9.43-close_fd.patch
Patch2: %{name}-9.43-get_geom.patch
Patch3: %{name}-9.54-resourceleak-fixes.patch
Patch4: %{name}-9.54-resourceleak-fixes-2.patch
Patch5: %{name}-9.60-sysfs-fclose.patch

BuildRequires: gcc
BuildRequires: make

Provides: /sbin/hdparm

%if "%{_sbindir}" == "%{_bindir}"
# We rely on filesystem to create the compat symlinks for us
Requires: filesystem(unmerged-sbin-symlinks)
Provides: /usr/sbin/hdparm
%endif

%description
Hdparm is a useful system utility for setting (E)IDE hard drive
parameters.  For example, hdparm can be used to tweak hard drive
performance and to spin down hard drives for power conservation.

%prep
%autosetup -p1

%build
CFLAGS="$RPM_OPT_FLAGS" %make_build STRIP=/bin/true LDFLAGS="$RPM_LD_FLAGS"

%install
install -c -m 755 -Dt $RPM_BUILD_ROOT%{_sbindir}/ hdparm
install -c -m 644 -Dt $RPM_BUILD_ROOT%{_mandir}/man8/ hdparm.8

%files
%doc hdparm.lsm Changelog README.acoustic TODO
%license LICENSE.TXT
%{_sbindir}/hdparm
%{_mandir}/man8/hdparm.8*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.65-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.65-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 9.65-7
- Rebuilt for the bin-sbin merge (2nd attempt)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.65-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 9.65-5
- Rebuilt for the bin-sbin merge

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.65-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.65-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 21 2023 Vojtech Trefny <vtrefny@redhat.com> - 9.65-1
- New upstream version 9.65

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Vojtech Trefny <vtrefny@redhat.com> - 9.63-1
- New upstream version 9.63

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.62-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 19 2021 Tomas Bzatek <tbzatek@redhat.com> - 9.62-1
- New upstream version 9.62

* Tue May 04 2021 Tomas Bzatek <tbzatek@redhat.com> - 9.61-1
- New upstream version 9.61

* Fri Apr 16 2021 Tomas Bzatek <tbzatek@redhat.com> - 9.60-3
- Fix fclose() on sysfs file write

* Thu Apr 15 2021 Tomas Bzatek <tbzatek@redhat.com> - 9.60-2
- Move hdparm binary to /usr/sbin

* Wed Apr 07 2021 Tomas Bzatek <tbzatek@redhat.com> - 9.60-1
- New upstream version 9.60

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.58-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.58-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 20 2019 Michal Minář <miminar@redhat.com> - 9.58-1
- New upstream version 9.58

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Michal Minář <miminar@redhat.com> - 9.56-1
- New upstream version.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Michal Minář <miminar@redhat.com> - 9.54-1
- New upstream version 9.54

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 9.52-3
- Use LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 11 2017 Michal Minar <miminar@redhat.com> - 9.52-1
- New upstream version.

* Sun Sep 10 2017 Vasiliy N. Glazov <vascom2@gmail.com> - 9.51-4
- Cleanup spec

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.51-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 23 2017 Michal Minar <miminar@redhat.com> 9.51-1
- New upstream version.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 9.48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 24 2015 Michal Minar <miminar@redhat.com> 9.48-1
- New upstream version.

* Tue Jun 16 2015 Michal Minar <miminar@redhat.com> 9.47-1
- New upstream version.

* Thu May 21 2015 Jaromir Capik <jcapik@redhat.com> - 9.45-2
- Removing ExcludeArch for s390 & s390x (it works)

* Tue Oct 28 2014 Michal Minar <miminar@redhat.com> 9.45-7
- New upstream version 9.45.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.43-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.43-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Michal Minar <miminar@redhat.com> 9.43-5
- Fixed division by zero.
- Resolves: #986072

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.43-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Michal Minar <miminar@redhat.com> 9.43-3
- Added patches fixing covscan defects.

* Fri Apr 19 2013 Michal Minar <miminar@redhat.com> 9.43-2
- Fixed inconsistency between man page and program's help.

* Wed Mar 13 2013 Michal Minar <miminar@redhat.com> - 9.43-1
- hdparm-9.43

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 01 2012 Michal Minar <miminar@redhat.com> - 9.42-1
- hdparm-9.42

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Karsten Hopp <karsten@redhat.com> 9.39-1
- hdparm-9.39

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Karsten Hopp <karsten@redhat.com> 9.36-1
- update to hdparm-9.36 (#645048)

* Thu Oct 07 2010 Karsten Hopp <karsten@redhat.com> 9.33-1
- update to hdparm-9.33 (#592896)

* Fri Dec 11 2009 Karsten Hopp <karsten@redhat.com> 9.27-1
- update to 9.27
- enhance security-erase timeout to 12h (#536731)

* Thu Aug 20 2009 Ville Skyttä <ville.skytta@iki.fi> - 9.16-3
- Let rpmbuild strip the executable (#513025).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Karsten Hopp <karsten@redhat.com> 9.16-1
- update to 9.16, fixes disk spindowns

* Wed Mar 04 2009 Karsten Hopp <karsten@redhat.com> 9.12-1
- update to 9.12 to fix #488560

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Karsten Hopp <karsten@redhat.com> 9.8-1
- update

* Wed Mar 05 2008 Karsten Hopp <karsten@redhat.com> 8.6-1
- update to 8.6
- fix source URL

* Mon Feb 25 2008 Karsten Hopp <karsten@redhat.com> 8.5-1
- version 8.5, fixes u8->u16 bug in security commands

* Mon Feb 25 2008 Karsten Hopp <karsten@redhat.com> 8.4-2
- fix debuginfo package (#434644)

* Wed Feb 20 2008 Karsten Hopp <karsten@redhat.com> 8.4-1
- version 8.4

* Tue Feb 19 2008 Karsten Hopp <karsten@redhat.com> 8.1-3
- upload 8.1 sources and rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 8.1-2
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Karsten Hopp <karsten@redhat.com> 8.1-1
- update to 8.1

* Fri Aug 24 2007 Karsten Hopp <karsten@redhat.com> 7.7-1
- update to 7.7

* Tue Jul 10 2007 Karsten Hopp <karsten@redhat.com> 7.6-1
- update to version 7.6

* Fri Feb 09 2007 Karsten Hopp <karsten@redhat.com> 6.9-3
- more review cleanups (#225882)

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 6.9-2
- clean up spec file for merge review (#225882)

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 6.9-1
- update to 6.9

* Mon Jul 17 2006 Karsten Hopp <karsten@redhat.de> 6.6-2
- test builds on ia64, ppc, ppc64

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 6.6-1.1
- rebuild

* Mon May 22 2006 Karsten Hopp <karsten@redhat.de> 6.3-3
- remove obsolute include patch
- disable idestruct patch, rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.3-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.3-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 20 2005 Karsten Hopp <karsten@redhat.de> 6.3-2
- use ExcludeArch, this allows building on archs we don't
  ship such as Alpha (#175919)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Karsten Hopp <karsten@redhat.de> 6.3-1
- fix package URL

* Tue Oct 25 2005 Karsten Hopp <karsten@redhat.de> 6.3-1
- update to hdparm-6.3

* Wed Jun 08 2005 Karsten Hopp <karsten@redhat.de> 6.1-1
- update to 6.1 (BLKGETSIZE fixes)
- work around hdparm's usage of kernel headers, assume
  that we run it on little-endian machines only

* Wed May 18 2005 Karsten Hopp <karsten@redhat.de> 5.9-3
- remove /etc/sysconfig/harddisks (#157673)

* Tue May 10 2005 Karsten Hopp <karsten@redhat.de> 5.9-2
- enable debuginfo

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 5.9-1
- update to 5.9
- build with gcc-4

* Mon Jan 03 2005 Karsten Hopp <karsten@redhat.de> 5.8-2
- add --help option (#143916)

* Fri Nov 26 2004 Karsten Hopp <karsten@redhat.de> 5.8-1
- update

* Tue Sep 21 2004 Than Ngo <than@redhat.com> 5.7-2
- rebuilt

* Mon Sep 06 2004 Karsten Hopp <karsten@redhat.de> 5.7-1
- update to latest stable version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Karsten Hopp <karsten@redhat.de> 5.5-1
- update to latest stable version
- rename variable to avoid name clash with readahead function

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 5.4-2
- rebuild

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 5.4-1
- update
- #92057

* Wed Apr 23 2003 Karsten Hopp <karsten@redhat.de> 5.3-2
- rebuild

* Wed Apr 23 2003 Karsten Hopp <karsten@redhat.de> 5.3-1
- update to 5.3
- add comment to /etc/sysconfig/harddisks

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 5.2-3
- rebuild on all arches

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Wed Jun 26 2002 Karsten Hopp <karsten@redhat.de>
- update to 5.2 with the following fixes:
 - v5.2 compile fixes for 2.5.xx
 - v5.1 fixed segfault in "-i" on older drives
 - v5.0 lots of updates and new features
 - v4.9 fixed compile error with 2.5.xx kernels
 - v4.8 changed -Q to allow specifying queue depth
 - v4.7 added -z, -Q, -M flags; expanded parm range for -p

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- bump version for 8.0

* Fri Feb 22 2002 Karsten Hopp <karsten@redhat.de>
- rebuild in new environment

* Wed Jan 23 2002 Karsten Hopp <karsten@redhat.de> (4.6-1)
- Update to 4.6

* Mon Oct 01 2001 Karsten Hopp <karsten@redhat.de>
- fix name of doc file  (#54137)

* Fri Jul 20 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude s390,s390x

* Mon Jun 25 2001 Karsten Hopp <karsten@redhat.de>
- update to version 4.1
- update URL

* Wed Jul 19 2000 Bernhard Rosenkränzer <bero@redhat.com>
- disable readahead (#14268)
- add comment in /etc/sysconfig/harddisks about possible extra parameters

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jul 12 2000 Trond Eivind Glomsrød <teg@redhat.com>
- disable 32 bit interfacing (#13730)

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}
- add /etc/sysconfig/harddisks, a new file for hardisk
  optimization parameters

* Mon Jun 19 2000 Bernhard Rosenkränzer <bero@redhat.com>
- FHSify

* Sun Apr  9 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix compilation with kernel 2.3.*

* Thu Feb 17 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 3.9
- handle RPM_OPT_FLAGS

* Thu Feb 17 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Use O_NONBLOCK when opening devices so we can manipulate CD-ROM drives
  with no media inserted, even when running a current kernel (Bug #6457)

* Sat Feb  5 2000 Bill Nottingham <notting@redhat.com>
- build as non-root user (#6458)

* Fri Feb  4 2000 Bernhard Rosenkränzer <bero@redhat.com>
- deal with RPM compressing man pages

* Fri Nov 19 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.6

* Thu Aug 12 1999 Cristian Gafton <gafton@redhat.com>
- version 3.5

* Wed Mar 24 1999 Cristian Gafton <gafton@redhat.com>
- added patches from UP

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 3.3
- build rooted

* Fri Oct 31 1997 Donnie Barnes <djb@redhat.com>
- fixed spelling error in summary

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc

