Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Maintains identical copies of files on multiple machines
Name: rdist
Version: 6.1.5
Release: 73%{?dist}
# On Feb 17, 2011, Michael A. Cooper gave permission via email for all of his
# copyrighted work in rdist to be relicensed to the same BSD as the rest of
# rdist. This is done in Patch15. Documentation of this is in Source3.
License: BSD
Source0: https://www.MagniComp.com/download/rdist/rdist-%{version}.tar.gz
Source1: https://people.redhat.com/pknirsch/src/rdist-v1.1.tar.bz2
# https://www.magnicomp.com/rdist/rdist-eu-license.shtml
Source2: rdist-eu-license.txt
Source3: rdist-licensing-email.txt
Patch0: rdist-6.1.5-linux.patch
Patch1: rdist-6.1.5-links.patch
Patch2: rdist-6.1.5-oldpath.patch
Patch3: rdist-6.1.5-hardlink.patch
Patch4: rdist-6.1.5-bison.patch
Patch5: rdist-6.1.5-varargs.patch
Patch6: rdist-6.1.5-maxargs.patch
Patch7: rdist-6.1.5-lfs.patch
Patch8: rdist-6.1.5-cleanup.patch
Patch9: rdist-6.1.5-svr4.patch
Patch10: rdist-6.1.5-ssh.patch
Patch11: rdist-6.1.5-mkstemp.patch
Patch12: rdist-6.1.5-stat64.patch
Patch13: rdist-6.1.5-re_args.patch
Patch14: rdist-6.1.5-fix-msgsndnotify-loop.patch
Patch15: rdist-6.1.5-license-fix.patch
URL: https://www.MagniComp.com/rdist
BuildRequires: byacc bison gcc

%description
The RDist program maintains identical copies of files on multiple
hosts.  If possible, RDist will preserve the owner, group, mode and
mtime of files and it can update programs that are executing.

Install rdist if you need to maintain identical copies of files on
multiple hosts.

%prep
%setup -q
%setup -q -T -D -a 1

cp %{SOURCE2} .
cp %{SOURCE3} .

# apply patch15 first due to #840419
%patch 15 -p1 -b .license-fix
%patch 0 -p1 -b .linux
%patch 1 -p1 -b .links
%patch 2 -p1 -b .oldpath
%patch 3 -p1 -b .hardlink
%patch 4 -p1 -b .bison
%patch 5 -p1 -b .varargs
%patch 6 -p1 -b .maxargs
%patch 7 -p1 -b .lfs
%patch 8 -p1 -b .cleanup
%patch 9 -p1 -b .svr4
%patch 10 -p1 -b .ssh
%patch 11 -p1 -b .mkstemp
%patch 12 -p1 -b .stat64
%patch 13 -p1 -b .re_args
%patch 14 -p1 -b .fix-msgsndnotify-loop

%build
make
make -C rdist

%install
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,8}

install -m755 src/rdist ${RPM_BUILD_ROOT}%{_bindir}
install -m755 rdist/rdist ${RPM_BUILD_ROOT}%{_bindir}/oldrdist
install -m755 src/rdistd ${RPM_BUILD_ROOT}%{_sbindir}
ln -sf ../sbin/rdistd ${RPM_BUILD_ROOT}%{_bindir}/rdistd

install -m644 doc/rdist.man ${RPM_BUILD_ROOT}%{_mandir}/man1/rdist.1
install -m644 doc/rdistd.man ${RPM_BUILD_ROOT}%{_mandir}/man8/rdistd.8

%files
%doc README rdist-eu-license.txt rdist-licensing-email.txt
%{_bindir}/rdist
%{_bindir}/oldrdist
%{_bindir}/rdistd
%{_sbindir}/rdistd
%{_mandir}/man1/rdist.1*
%{_mandir}/man8/rdistd.8*

%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 6.1.5-73
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:6.1.5-72
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-71
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-70
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-69
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Michal Ruprich <mruprich@redhat.com> - 1:6.1.5-68
- Resolves: #1606088 - rdist: FTBFS in Fedora rawhide 

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-67
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-66
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-64
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-63
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.5-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1:6.1.5-60
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-59
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-58
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Michal Luscon <mluscon@redhat.com> - 1:6.1.5-57
- Fixed #840419: rdist-6.1.5-license-fix.patch modifies patch backup files

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 1:6.1.5-52
- Fix several rpmlint warnings/errors, clean spec file (#226359)

* Thu Feb 17 2011 Tom Callaway <spot@fedoraproject.org> - 1:6.1.5-51
- resolve non-free licensing, thanks to Michael A. Cooper

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 19 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 1:6.1.5-49
- added dist macro

* Mon Apr 19 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 1:6.1.5-48
- fixed rdistd manpage
- Resolves: #526175

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.1.5-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:6.1.5-45
- Autorebuild for GCC 4.3

* Wed Aug 02 2006 Phil Knirsch <pknirsch@redhat.com> 1:6.1.5-44
- Fixed problem with memory leak (#192229)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:6.1.5-43.1
- rebuild

* Wed Jun 07 2006 Phil Knirsch <pknirsch@redhat.com> - 1:6.1.5-43
- Added missing bison buildprereq (#194158)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:6.1.5-42.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:6.1.5-42.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 28 2005 Phil Knirsch <pknirsch@redhat.com> 6.1.5-42
- Fixed build problem on latest FC-devel tree

* Wed May 04 2005 Phil Knirsch <pknirsch@redhat.com> 6.1.5-41
- Fixed incorrect use of statfs return values (#147481)

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 6.1.5-40
- bump release and rebuild with gcc 4

* Fri Feb 18 2005 Phil Knirsch <pknirsch@redhat.com> 6.1.5-39
- rebuilt

* Fri Jul 02 2004 Phil Knirsch <pknirsch@redhat.com> 6.1.5-38
- Added byacc to BuildPreReq (#124939)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Phil Knirsch <pknirsch@redhat.com> 6.1.5-36
- rebuilt

* Tue May 25 2004 Phil Knirsch <pknirsch@redhat.com> 6.1.5-35.30.1
- Built packages for RHEL3.

* Tue May 25 2004 Phil Knirsch <pknirsch@redhat.com> 6.1.5-35.21.1
- Fixed missing unlink() for mkstemp() created file (#123833).
- Built packages for AS2.1

* Wed Feb 18 2004 Phil Knirsch <pknirsch@redhat.com> 6.1.5-34.30.1
- Built errata package for RHEL3.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 6.1.5-33
- rebuilt

* Mon Jan 12 2004 Phil Knirsch <pknirsch@redhat.com> 6.1.5-32
- Included missing dir patch for mkstemp change (#106728).

* Wed Dec 17 2003 Phil Knirsch <pknirsch@redhat.com> 6.1.5-31
- Fixed wrong SvR4 system detection on Linux (#110426).
- Fixed unitialized use of struct (#111189).
- Make rsh work correctly with password authentification and ssh (#111778).

* Tue Dec 16 2003 Phil Knirsch <pknirsch@redhat.com>
- Finished LFS support for rdist on 32bit archs (#79580).
- Lots of code cleanup.
- Switched from mktemp to mkstemp usage.

* Thu Sep 25 2003 Phil Knirsch <pknirsch@redhat.com> 6.1.5-30.1
- rebuilt

* Thu Sep 04 2003 Phil Knirsch <pknirsch@redhat.com> 6.1.5-30
- Fixed max. # of args (#85634).

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com>
- rebuilt

* Tue Jun 17 2003 Phil Knirsch <pknirsch@redhat.com> 1:6.1.5-29
- use stdarg.h instead of varargs.h.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Phil Knirsch <pknirsch@redhat.com> 1:6.1.5-27.1
- Bumped release and rebuilt

* Wed Jun 04 2003 Phil Knirsch <pknirsch@redhat.com> 1:6.1.5-27
- Fixed new bison build problems.
- Changed Copyright to License.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1:6.1.5-26
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1:6.1.5-25
- rebuild on all arches

* Mon Aug 12 2002 Phil Knirsch <pknirsch@redhat.com> 6.1.5-24
- Fixed small typo in URL: field.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 6.1.5-23
- automated rebuild

* Thu Jun 20 2002 Phil Knirsch <pknirsch@redhat.com> 6.1.5-22
- Bumped release and rebuilt.

* Thu Jun 20 2002 Phil Knirsch <pknirsch@redhat.com> 6.1.5-21
- Include ia64 again.

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 6.1.5-20
- Don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 31 2002 Phil Knirsch <pknirsch@redhat.com>
- Added my 4.3BSD port of the v1 protocol rdist code and provide a oldrdist
  binary (#55761 and several others).
- Fixed a small manpage problem (#55489)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- exclude ia64 for now.

* Sat Feb 05 2000 Cristian Gafton <gafton@redhat.com>
- include new license package
- man pages are compressed
- fix description

* Tue Jul 20 1999 Jeff Johnson <jbj@redhat.com>
- re-release latest rdist package.

* Thu Jun  3 1999 Jeff Johnson <jbj@redhat.com>
- permit rdist to distribute hard links (#3228)

* Tue Apr 13 1999 Jeff Johnson <jbj@redhat.com>
- add /usr/bin/rdistd symlink (#2154)
- update docs to reflect /usr/bin/oldrdist change.

* Mon Apr 12 1999 Jeff Johnson <jbj@redhat.com>
- use /usr/bin/oldrdist for old rdist compatibility path (#2044).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Wed Feb 17 1999 Jeff Johnson <jbj@redhat.com>
- dynamic allocation for link info (#1046)

* Thu Nov 12 1998 Jeff Johnson <jbj@redhat.com>
- update to 6.1.5

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 20 1997 Otto Hammersmith <otto@redhat.com>
- fixed the url to the source
- fixed the copyright field

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
