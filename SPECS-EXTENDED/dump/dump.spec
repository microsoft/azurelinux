Vendor:         Microsoft Corporation
Distribution:   Mariner
%define PREVER b46
%define DUMP_VERSION 0.4%{PREVER}

%define _legacy_common_support 1

Summary:       Programs for backing up and restoring ext2/ext3/ext4 filesystems
Name:          dump
Version:       0.4
Release:       2%{?dist}
License:       BSD
URL:           http://dump.sourceforge.net/
Source:        http://downloads.sourceforge.net/dump/dump-%{DUMP_VERSION}.tar.gz
BuildRequires: e2fsprogs-devel >= 1.18, readline-devel >= 4.2
BuildRequires: zlib-devel, bzip2-devel, automake
BuildRequires: device-mapper-devel, libselinux-devel
BuildRequires: lzo-minilzo
BuildRequires: lzo-devel, libtool
# This Requires is now mandatory because we need to ensure the "disk"
# group is created before installation (#60461)
Requires:      setup
Requires:      rmt
Obsoletes:     dump-static
Provides:      dump-static

Patch0:        dump-buildfix.patch
Patch1:        dump-remove-lzo.patch
Patch2:        dump-glibc_xattr.patch

%description
The dump package contains both dump and restore. Dump examines files
in a filesystem, determines which ones need to be backed up, and
copies those files to a specified disk, tape, or other storage medium.
The restore command performs the inverse function of dump; it can
restore a full backup of a filesystem. Subsequent incremental backups
can then be layered on top of the full backup. Single files and
directory subtrees may also be restored from full or partial backups.

Install dump if you need a system for both backing up filesystems and
restoring filesystems after backups.

%prep
%setup -q -n dump-%{DUMP_VERSION}

%patch0 -p1 -b .buildfix
%patch1 -p1 -b .remove-lzo
%patch2 -p1 -b .glibc_xattr

for i in MAINTAINERS COPYING ChangeLog; do
    iconv -f iso-8859-1 -t utf-8  $i -o $i.new
    touch -r $i $i.new
    mv $i.new $i
done

%build
autoreconf -fiv

export CFLAGS="$RPM_OPT_FLAGS -Wall -Wpointer-arith -Wstrict-prototypes \
-Wmissing-prototypes -Wno-char-subscripts -fno-strict-aliasing"

# XXX --enable-kerberos needs krcmd
%configure --disable-static \
    --enable-transselinux \
    --enable-largefile \
    --disable-rmt \
    --disable-ssl \
    --enable-qfa \
    --enable-readline \
    --with-binmode=0755 \
    --with-manowner=root \
    --with-mangrp=root \
    --with-manmode=0644 

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8

%makeinstall INSTALL="install -p" \
    SBINDIR=%{buildroot}%{_sbindir} \
    BINDIR=%{buildroot}%{_sbindir} \
    MANDIR=%{buildroot}%{_mandir}/man8 \
    BINOWNER=$(id -un) \
    BINGRP=$(id -gn) \
    MANOWNER=$(id -un) \
    MANGRP=$(id -gn)

pushd %{buildroot}
    ln -sf dump .%{_sbindir}/rdump
    ln -sf restore .%{_sbindir}/rrestore
    mkdir -p .%{_sysconfdir}
    > .%{_sysconfdir}/dumpdates
popd

%files
%doc AUTHORS COPYING INSTALL KNOWNBUGS MAINTAINERS NEWS README REPORTING-BUGS TODO
%doc dump.lsm
%attr(0664,root,disk) %config(noreplace) %{_sysconfdir}/dumpdates
%{_sbindir}/dump
%{_sbindir}/rdump
%{_sbindir}/restore
%{_sbindir}/rrestore
%{_mandir}/man8/dump.8*
%{_mandir}/man8/rdump.8*
%{_mandir}/man8/restore.8*
%{_mandir}/man8/rrestore.8*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.4-2
- Remove epoch

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.4-1
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Mon Jun 07 2021 Thomas Crain <thcrain@microsoft.com> - 1:0.4-0.44.b46
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable SSL support

* Wed Feb 12 2020 Václav Doležal <vdolezal@redhat.com> - 1:0.4-0.43.b46
- Use library functions for manipulating xattrs (#1795953)

* Tue Feb 04 2020 Václav Doležal <vdolezal@redhat.com> - 1:0.4-0.42.b46
- Fix FTBFS by enabling '-fcommon'

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.41.b46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.40.b46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:0.4-0.39.b46
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.38.b46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.37.b46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.36.b46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 09 2017 Troy Dawson <tdawson@redhat.com> - 1:0.4-0.35.b46
- Fix VERSION / version issue causing FTBFS on F27+

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.34.b46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.33.b46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.32.b46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:0.4-0.31.b46
- Rebuild for readline 7.x

* Thu Sep 15 2016 Josef Ridky <jridky@redhat.com> - 1:0.4-0.30.b46
- New upstream release 0.4b46 (#1376411)

* Thu Aug 11 2016 Josef Ridky <jridky@redhat.com> - 1:0.4-0.29.b45
- Fix issue with ignoring -Q flag (#1366133)
- Fix issue with SIGSEGV alert (#1365124)

* Sat Jul 30 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1:0.4-0.28.b45
- Restore higher Release so upgrade path works for pre-release

* Fri Jul 29 2016 Josef Ridky <jridky@redhat.com> - 1:0.4-0.1.b45
- New upstream release 0.4b45 (#1361495)
- Fix issue with bad UUID error message (#1048548)
- Spec file has been updated

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4-0.27.b44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 25 2015 Petr Hracek <phracek@redhat.com> - 1:0.4-0.26.b44
- Fix hang restoring incrementals which remove directories (#972370)
- Thanks to Jason Tibbitts

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.25.b44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 17 2014 Petr Hracek <phracek@redhat.com> - 1:0.4-0.24.b44
- Do not ship lzo in dump package (#1132282)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.23.b44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.22.b44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.21.b44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Petr Hracek <phracek@redhat.com> - 1:0.4-0.20.b44
- Move rmt into star package (#968995)
- Remove dependency to star (#968995)

* Wed Apr 17 2013 Petr Hracek <phracek@redhat.com> - 1:0.4-0.19.b44
- Support aarch64 (#925282)

* Tue Mar 05 2013 Adam Tkac <atkac redhat com> - 1:0.4-0.18.b44
- build with -fno-strict-aliasing

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.17.b44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Adam Tkac <atkac redhat com> 1:0.4-0.16.b44
- remove hardcoded _sbindir path

* Thu Jan 17 2013 Adam Tkac <atkac redhat com> 1:0.4-0.15.b44
- apply the patch for #664616

* Thu Jan 17 2013 Adam Tkac <atkac redhat com> 1:0.4-0.14.b44
- minor manpage fixes (#664616)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.13.b44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.12.b44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 14 2011 Adam Tkac <atkac redhat com> 0.4-0.11.b44
- update to 0.4b44
- patches merged
  - dump-rh507948.patch
  - dump-0.4b42-ext4.patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.10.b43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 2 2010 Jan Görig <jgorig redhat com> 0.4-0.9.b42
- fix dump -w does not work on ext4 fielsystems (#658890)

* Mon Jul 12 2010 Adam Tkac <atkac redhat com> 0.4-0.8.b43
- move COPYRIGHT to the rmt package

* Fri Jun 11 2010 Adam Tkac <atkac redhat com> 0.4-0.7.b43
- update to 0.4b43
- patches merged
  - dump-rh568457.patch
  - dump-rh576525.patch

* Mon Apr 26 2010 Adam Tkac <atkac redhat com> 0.4-0.6.b42
- fix invalid EA metainformation in dump, add workaround to restore (#576525)

* Thu Mar 4 2010 Jan Görig <jgorig redhat com> 0.4-0.5.b42
- don't set extended attributes when in read only mode (#568457)

* Wed Feb 10 2010 Adam Tkac <atkac redhat com> 0.4-0.4.b42
- improve patch for multivol backup issues

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4-0.3.b42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Tkac <atkac redhat com> 0.4-0.2.b42
- restore multivol backups correctly

* Mon Jun 22 2009 Adam Tkac <atkac redhat com> 0.4-0.1.b42
- update to 0.4b42
- patches merged
  - dump-selinux.patch
  - dump-dmfix.patch
  - dump-immutable.patch
  - dump-0.4b41-libtinfo.patch
  - dump-rh356121.patch
  - dump-rh493635.patch
  - dump-rh490627.patch
  - dump-rh489853.patch
- fix NVR to conform to Fedora policies

* Sat Apr 04 2009 Adam Tkac <atkac redhat com> 0.4b41-13
- display dump level correctly in all cases (#493635)
- -A option is not valid when -P is specified, correct manual page (#490627)
- fix typos in manual pages (#489853)

* Mon Mar 09 2009 Adam Tkac <atkac redhat com> 0.4b41-12
- correct manual page (dump level is 0 by default, #356121)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4b41-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 lonely wolf <wolfy@fedoraproject.org> 0.4b41-10
- spec cleanup

* Fri Oct 03 2008 Adam Tkac <atkac redhat com> 0.4b41-9
- dump-0.4b37-2TB.patch is no longer needed
- rebuild (#464989)

* Mon Jun 23 2008 Adam Tkac <atkac redhat com> 0.4b41-8
- removed compat static -> non-static symlinks (#452425)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 0.4b41-7.1
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Adam Tkac <atkac redhat com> 0.4b41-6.1
- use libtinfo instead libncurses
- use autoreconf (=> add BuildRequires: automake - for aclocal)

* Wed Aug 22 2007 Adam Tkac <atkac redhat com> 0.4b41-6
- rebuild (BuildID feature)
- use device-mapper-devel instead device-mapper in BuildRequires

* Tue Jan 30 2007 Adam Tkac <atkac redhat com> 0.4b41-5
- fixed dumping of 2TB systems

* Mon Jan 29 2007 Adam Tkac <atkac redhat com> 0.4b41-4
- added Andrew Kroeger's patch. Immutable files are restored correctly

* Thu Jan 18 2007 Adam Tkac <atkac redhat com> 0.4b41-3
- dump is now linked dynamically
- removed termcap dependency

* Mon Aug  7 2006 Jindrich Novy <jnovy@redhat.com> 0.4b41-2
- fix miscompares detected by restore -C caused by SELinux (#189845)
- link properly against device-mapper and selinux libraries
- add autoconf BuildRequires
- use %%{?dist}

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.4b41-1.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.4b41-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.4b41-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 11 2006 Jindrich Novy <jnovy@redhat.com> 0.4b41-1
- update to 0.4b41
- drop .fixacl patch, now applied in the new upstream release
- link against device-mapper

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Jindrich Novy <jnovy@redhat.com> 0.4b40-5
- spec file cleanup - thanks to Matthias Saou (#172961)
- convert spec to UTF-8

* Wed Jul 06 2005 Karsten Hopp <karsten@redhat.de> 0.4b40-4
- BuildRequires ncurses-devel

* Thu Jun  9 2005 Jindrich Novy <jnovy@redhat.com> 0.4b40-3
- fix restoration of ext3 ACL's (#159617) - Stelian Pop

* Wed May 11 2005 Jindrich Novy <jnovy@redhat.com> 0.4b40-2
- Don't strip binaries to get valid debuginfo

* Tue May  3 2005 Jindrich Novy <jnvoy@redhat.com> 0.4b40-1
- Updated to dump 0.4b40
- Dropped .ea and .asize patches (applied upstream)

* Wed Mar  2 2005 Jindrich Novy <jnovy@redhat.com> 0.4b39-3
- Added patch to fix negative size problem with -s/-d 
  options (#147710) - from Stelian Pop

* Mon Feb 28 2005 Jindrich Novy <jnovy@redhat.com> 0.4b39-2
- Updated the EA patch with support for in-inode EAs, big
  inodes and fixes 'error in EA block' displayed for
  every single inode (#149299) - patch from Stelian Pop

* Mon Jan 24 2005 Jindrich Novy <jnovy@redhat.com. 0.4b39-1
- Updated to dump 0.4b39
- Updated the experimental patch.

* Wed Jan 12 2005 Jindrich Novy <jnovy@redhat.com> 0.4b38-1
- Updated to dump 0.4b38 (#144840)
- Updated the experimental dump patch.
- Dropped the cvs patch, applied in the upstream release.

* Mon Dec 20 2004 Dan Walsh <dwalsh@redhat.com> 0.4b37-3
- Updated experimental dump patch from upstream to allow dump/restore of xattr.

* Thu Dec 9 2004 Dan Walsh <dwalsh@redhat.com> 0.4b37-2
- Added experimental dump patch from upstream to allow dump/restore of xattr.

* Thu Jul 29 2004 Warren Togami <wtogami@redhat.com>
- 0.4b37

* Fri Jul 02 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 0.4b36

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 17 2003 Mike A. Harris <mharris@redhat.com> 0.4b33-1
- Updated to dump 0.4b33, fixes (#89835)

* Fri Jan 24 2003 Mike A. Harris <mharris@redhat.com> 0.4b28-7
- Added --enable-qfa to configure macro for RFE: (#77608)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.4b28-6
- rebuilt

* Mon Oct  7 2002 Mike A. Harris <mharris@redhat.com> 0.4b28-5
- All-arch rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Mike A. Harris <mharris@redhat.com> 0.4b28-2
- Updated to dump 0.4b28
- Removed atomic_read/write patch, not needed anymore

* Fri Mar  1 2002 Mike A. Harris <mharris@redhat.com> 0.4b27-3
- BuildRequires readline-devel >= 4.2 for the rl_completion_matches function
- Added dump-0.4b27-dump-atomic-read-write.patch to avoid namespace conflict
  with included kernel headers.  atomic_read is a function on s390 and as
  such, cannot be #undef'd

* Thu Feb 28 2002 Mike A. Harris <mharris@redhat.com> 0.4b27-2
- Added prereq on "setup" to ensure disk group is created prior to this
  package being installed
- Somehow the dump package changelog got hosed, and part of the spec file
  regressed.  I believe it is fixed now.

* Tue Feb 26 2002 Mike A. Harris <mharris@redhat.com> 0.4b27-1
- Updated to dump 0.4b27-1

* Fri Feb 22 2002 Mike A. Harris <mharris@redhat.com> 0.4b25-5
- Bumped release up a couple notches to rebuild in rawhide
 
* Thu Feb 21 2002 Mike A. Harris <mharris@redhat.com> 0.4b25-1.72.0
- Rebuilt 0.4b25 for erratum release.  Fixes various bugs that have been
  reported in bugzilla which are logged below.  Also fixes a bug caused by
  linking statically to a faulty system library.
- Added Provides dump-static line
 
* Mon Feb 11 2002 Mike A. Harris <mharris@redhat.com> 0.4b25-3
- Added missing zlib buildprereq
- Rebuild in new environment

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Nov 21 2001 Mike A. Harris <mharris@redhat.com> 0.4b25-1
- Updated to version 0.4b25-1
- Added homepage URL for RFE (#54601)
- Also fixed in this release are (#21272, #52663, #56616)
- Dropped time.h patch as it is unneeded now

* Tue Nov  6 2001 Mike A. Harris <mharris@redhat.com> 0.4b22-7
- Updated BuildPreReq to e2fsprogs-devel >= 1.18, readline-devel >= 4.1 to
  explicitly state the minimum required deps and fix (#51900)

* Sat Sep  8 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.4b22-6
- Kill the static subpackage - the standard binaries are now static
  This removes /usb/sbin/*. The static versions are now in /sbin 
  (#53433)
- Obsolete dump-static

* Tue Aug 14 2001 Trond Eivind Glomsrød <teg@redhat.com> 0.4b22-5
- Move non-static binaries to /usr/sbin (#49520)

* Fri Jun 29 2001 Mike A. Harris <mharris@redhat.com> 0.4b22-4
- Added BuildPrereq: readline-devel (#44734 - which was reopened and changed)

* Sat Jun 16 2001 Mike A. Harris <mharris@redhat.com> 0.4b22-3
- Added BuildPrereq: libtermcap-devel (#44734)

* Tue Jun 12 2001 Mike A. Harris <mharris@redhat.com> 0.4b22-2
- Removed release tag from buildroot dirname - messy.
- Broke all lines over multiple lines for readability in specfile.
- Added --enable-largefile configure flags

* Mon Jun 11 2001 Florian La Roche <Florian.LaRoche@redhat.de> 0.4b22-1
- 0.4b22

* Mon May  7 2001 Mike A. Harris <mharris@redhat.com> 0.4b21-5
- Added BuildPrereq: e2fsprogs-devel (#27428)

* Mon Apr  9 2001 Bill Nottingham <notting@redhat.com>
- fix ia64

* Wed Feb 14 2001 Bill Nottingham <notting@redhat.com>
- fix build with current glibc

* Mon Jan 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- change copyright: UCB to License: BSD

* Fri Jan 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.4b21.

* Sun Nov 26 2000 Jeff Johnson <jbj@redhat.com>
- update to 0.4b20.

* Fri Nov 10 2000 Stelian Pop <pop@cybercable.fr>
- dump 0.4b20 released, first packaging.

* Tue Oct 31 2000 Jeff Johnson <jbj@redhat.com>
- remove setuid bits for Red Hat 5.x errata.

* Wed Aug 30 2000 Matt Wilson <msw@redhat.com>
- rebuild to cope with glibc locale binary incompatibility, again

* Wed Aug 30 2000 Preston Brown <pbrown@redhat.com>
- fix for dumping files between 2 and 4 gigs (#16466)

* Mon Aug 21 2000 Matt Wilson <msw@redhat.com>
- don't use -O2 on alpha because of compiler ICE

* Sun Aug 20 2000 Jeff Johnson <jbj@redhat.com>
- update to 0.4b19.

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Wed Aug 16 2000 Erik Troan <ewt@redhat.com>
- support LABEL= in fstab

* Sat Jul 22 2000 Bill Nottingham <notting@redhat.com>
- if dump/restore aren't set(u|g)id, they don't need group tty (#12670)

* Wed Jul 19 2000 Jakub Jelinek <jakub@redhat.com>
- rebuild to cope with glibc locale binary incompatibility

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Preston Brown <pbrown@redhat.com>
- whoops I had dump commented out of the file list.  fixed.
- dropped suid bits on the static binaries.
- fix char buffer size issue (#11880)

* Mon Jun 19 2000 Preston Brown <pbrown@redhat.com>
- dropped SUID bits

* Tue Jun  6 2000 Jeff Johnson <jbj@redhat.com>
- update to 0.4b17.
- FHS packaging.

* Thu Jun  1 2000 Stelian Pop <pop@cybercable.fr>
- dump 0.4b17 released, first packaging.

* Sat Mar 11 2000 Stelian Pop <pop@cybercable.fr>
- dump 0.4b16 released, first packaging.

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- use posix signal handling to preserve dump functionality with libc5.

* Thu Mar  2 2000 Bill Nottingham <notting@redhat.com>
- update to 0.4b15

* Thu Feb 10 2000 Jeff Johnson <jbj@redhat.com>
- dump -0ufB /dev/ftape 1638000 /mnt2 fails to use /mnt2 as tape device (#8036)

* Thu Feb 10 2000 Stelian Pop <pop@cybercable.fr>
- dump 0.4b14 released, first packaging.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Thu Jan 27 2000 Jeff Johnson <jbj@redhat.com>
- update to 0.4b13.

* Fri Jan 21 2000 Stelian Pop <pop@cybercable.fr>
- dump 0.4b13 released, first packaging.

* Mon Jan 10 2000 Jeff Johnson <jbj@redhat.com.
- update to 0.4b12.

* Sat Jan 8 2000 Stelian Pop <pop@cybercable.fr>
- dump 0.4b12 released, first packaging.

* Sun Dec 5 1999 Stelian Pop <pop@cybercable.fr>
- dump 0.4b11 released, first packaging.

* Sat Nov 27 1999 Jeff Johnson <jbj@redhat.com>
- intergrate Stelian's fixes (Thanks!).

* Sun Nov 21 1999 Stelian Pop <pop@cybercable.fr>
- dump 0.4b10 released, first packaging.

* Thu Nov 11 1999 Stelian Pop <pop@cybercable.fr>
- make static versions also for rescue purposes.

* Fri Nov 5 1999 Stelian Pop <pop@cybercable.fr>
- dump 0.4b9 released, first packaging.

* Wed Nov 3 1999 Stelian Pop <pop@cybercable.fr>
- dump 0.4b8 released, first packaging.

* Fri Oct 8 1999 Stelian Pop <pop@cybercable.fr>
- dump 0.4b7 released, first packaging.

* Thu Sep 30 1999 Stelian Pop <pop@cybercable.fr>
- dump 0.4b6 released, first packaging.

* Fri Sep 10 1999 Jeff Johnson <jbj@redhat.com>
- recompile with e2fsprogs = 1.15 (#4962).

* Sat Jul 31 1999 Jeff Johnson <jbj@redhat.com>
- workaround egcs bug (#4281) that caused dump problems (#2989).
- use sigjmp_buf, not jmp_buf (#3260).
- invoke /etc/rmt (instead of rmt) like other unices. (#3272).
- use glibc21 err/glob rather than the internal compatibility routines.
- wire $(OPT) throughout Makefile's.
- fix many printf problems, mostly lint clean.
- merge SuSE, Debian and many OpenBSD fixes.

* Thu Mar 25 1999 Jeff Johnson <jbj@redhat.com>
- remove setuid/setgid bits from /sbin/rmt (dump/restore are OK).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- strip binaries.

* Thu Mar 18 1999 Jeff Johnson <jbj@redhat.com>
- Fix dangling symlinks (#1551).

* Wed Mar 17 1999 Michael Maher <mike@redhat.com>
- Top O' the morning, build root's fixed for man pages.  

* Fri Feb 19 1999 Preston Brown <pbrown@redhat.com>
- upgraded to dump 0.4b4, massaged patches.

* Tue Feb 02 1999 Ian A Cameron <I.A.Cameron@open.ac.uk>
- added patch from Derrick J Brashear for traverse.c to stop bread errors

* Wed Jan 20 1999 Jeff Johnson <jbj@redhat.com>
- restore original 6755 root.tty to dump/restore, defattr did tty->root (#684).
- mark /etc/dumpdates as noreplace.

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- add build root.

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- added a patch for resolving linux/types.h and sys/types.h conflicts

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- added prototype of llseek() so dump would work on large partitions

* Thu Oct 30 1997 Donnie Barnes <djb@redhat.com>
- made all symlinks relative instead of absolute

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Mar 06 1997 Michael K. Johnson <johnsonm@redhat.com>
- Moved rmt to its own package.

* Tue Feb 11 1997 Michael Fulbright <msf@redhat.com>
- Added endian cleanups for SPARC

* Fri Feb 07 1997 Michael K. Johnson <johnsonm@redhat.com> 
- Made /etc/dumpdates writeable by group disk.
