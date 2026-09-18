# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: dosfstools
Version: 4.2
Release: 16%{?dist}
Summary: Utilities for making and checking MS-DOS FAT filesystems on Linux
License: GPL-3.0-or-later
Source0: https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
URL: https://github.com/dosfstools/dosfstools

BuildRequires: gcc
BuildRequires: make
# For tests
BuildRequires: xxd
# rhbz#2021638
Recommends: glibc-gconv-extra

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/mkfs.vfat
%endif

%description
The dosfstools package includes the mkdosfs and dosfsck utilities,
which respectively make and check MS-DOS FAT filesystems on hard
drives or on floppies.

%prep
%autosetup -p1

%build
%configure --enable-compat-symlinks
%make_build CFLAGS="%{optflags} -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -fno-strict-aliasing"

%install
%make_install PREFIX=%{_prefix}

# license file is in the licenses dir, drop ancient/duplicate docs
rm -f %{buildroot}%{_docdir}/%{name}/*

%check
make check

%files
%license COPYING
%doc NEWS README
%{_sbindir}/*
%{_mandir}/man8/*


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.2-14
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.2-12
- Rebuilt for the bin-sbin merge

* Mon Feb 19 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 4.2-11
- Don't ship ancient docs, run tests

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 4.2-8
- Converted license to SPDX

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 15 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 4.2-5
- Added weak dependency on glibc-gconv-extra
  Resolves: rhbz#2021638

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb  1 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 4.2-1
- New version
  Resolves: rhbz#1922767

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 4.1-11
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan  9 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.1-7
- Fixed mkfs.fat cluster size calculation for disks with 4k sectors

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 4.1-1
- New version
  Resolves: rhbz#1416392

* Fri May  6 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 4.0-1
- New version
  Resolves: rhbz#1333781
- Switched to autotools
- Various spec file cosmetic fixes (e.g. used optflags)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Sep 18 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.28-1
- New version
  Resolves: rhbz#1263818

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.27-1
- New version
  Resolves: rhbz#1078057
  Resolves: rhbz#1158101
- Updated URL to point to new upstream
- Removed RPM artefacts from SPEC

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.26-1
- New version
  Resolves: rhbz#1074172

* Mon Feb 17 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.25-1
- New version
  Resolves: rhbz#1055259

* Mon Nov 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.24-1
- New version
  Resolves: rhbz#1034058
- Dropped fix-big-endian patch (upstreamed)

* Fri Nov 22 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.23-3
- Used /usr/sbin directory instead of /sbin

* Fri Nov 22 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.23-2
- Fixed dosfsck on big endian platforms
  Resolves: rhbz#1029695

* Tue Oct 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.23-1
- New version
  Resolves: rhbz#1019081
- Fixed bogus dates in changelog (best effort)

* Thu Aug  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.22-4
- Fixed sources URL

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.22-2
- Fixed ownership of man directories
  Resolves: rhbz#987735

* Tue Jul 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.22-1
- New version
  Resolves: rhbz#987337

* Wed Jul 17 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.21-1
- New version
  Resolves: rhbz#985279
- Dropped manpage-fix patch (upstreamed)

* Tue Jun 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.20-3
- Fixed fsck.vfat manpage to be consistent with the tool options

* Fri Jun 14 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.20-2
- Installed compatibility symlinks

* Thu Jun 13 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.20-1
- New version
  Resolves: rhbz#973937

* Wed Jun 12 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.19-1
- New version
  Resolves: rhbz#971686

* Tue Jun  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.17-1
- New version
  Resolves: rhbz#968400
- Dropped fix-label patch (upstreamed)

* Thu May  2 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.16-3
- Fixed dosfslabel (by fix-label patch)
  Resolves: rhbz#948055

* Mon Mar 11 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.16-2
- Source0 URL synced with upstream

* Wed Mar  6 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.16-1
- New version
  Resolves: rhbz#916913

* Fri Feb 22 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.15-1
- New version
  Resolves: rhbz#913884
- Dropped patches: fix-alloc-rootdir-entry, dev-detect-fix (all upstreamed)

* Thu Jan 24 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.14-1
- New version
  Resolves: rhbz#903581
- Switched to xz compressed sources
- Dropped dosfslabel-fat32 patch (upstreamed)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 29 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.12-1
- New version, all patches were rebased
  Resolves: rhbz#749969

* Fri Jun 03 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.11-5
- Fixed device partitions detection
  Resolves: rhbz#710480

* Tue Apr 05 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.11-4
- Fixed dosfslabel on FAT32 (#693662)

* Mon Feb 14 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.11-3
- Fixed buffer overflow in alloc_rootdir_entry (#674095)
- Dropped fix-reclaim-file patch, obsoleted by fix-alloc-rootdir-entry patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.11-1
- New version
- Fixed buffer overflow in reclaim file (#660154)

* Fri Oct 08 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.10-2
- Fixed dosfsck and dosfslabel on s390x (#624596)

* Wed Oct 06 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.10-1
- Bump to newer release

* Mon May 31 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.9-3
- Rebuilt with -fno-strict-aliasing

* Fri Feb 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.9-2
- Used bz2 compresed sources

* Fri Feb 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 3.0.9-1
- Bump to newer release
- Removed mkdosfs-ygg from Obsoletes/Provides tag as it looks really deprecated
- Drop bounds patch - fixed upstream

* Sun Dec 06 2009 Lubomir Rintel <lkundrak@v3.sk> - 3.0.6-1
- Bump to newer release
- Fix numerous out-of-bound writes

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.0.1-6
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Stepan Kasal <skasal@redhat.com> - 3.0.1-3
- fix the previous commit
- omit the most obsolete documents
- after writing the label, exit with exit code 0 (#468050)

* Fri Jan 30 2009 Stepan Kasal <skasal@redhat.com> - 3.0.1-2
- install all the documentation to the usual docdir (#225707)

* Mon Jan 19 2009 Peter Vrabec <pvrabec@redhat.com> - 3.0.1-1
- upgrade
- include ChangeLog and COPYING (#225707)

* Mon Nov 17 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.0-2
- apply vfat timing fix (bz 448247)

* Tue Sep 30 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.0-1
- update to 3.0.0

* Wed Jul 16 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.11-10
- fix license tag
- fix patch to apply with fuzz=0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.11-9
- Autorebuild for GCC 4.3

* Tue Apr  3 2007 Jeremy Katz <katzj@redhat.com> - 2.11-8
- add dosfslabel (originally by Peter Jones)

* Wed Feb 21 2007 Peter Vrabec <pvrabec@redhat.com> 2.11-7
- fix debuginfo package (#225707)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.11-6.1
- rebuild

* Fri Jun 30 2006 Peter Vrabec <pvrabec@redhat.com> 2.11-6
- fix upgrade path (#197231)

* Thu May 11 2006 Peter Vrabec <pvrabec@redhat.com> 2.11-5
- fix work with disk image files > 4GB (#191198)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.11-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.11-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 16 2005 Jakub Jelinek <jakub@redhat.com> 2.11-4
- rebuilt with GCC 4.1
- make it build with -D_FORTIFY_SOURCE=2

* Sun Nov 06 2005 Peter Vrabec <pvrabec@redhat.com> 2.11-3
- fix LFS (#172369)

* Fri Nov 04 2005 Peter Vrabec <pvrabec@redhat.com> 2.11-2
- fix LFS

* Wed Oct 12 2005 Peter Vrabec <pvrabec@redhat.com> 2.11-1
- upgrade

* Thu Apr 28 2005 Peter Vrabec <pvrabec@redhat.com> 2.10-3
- if HDIO_GETGEO fails, print a warning and default to H=255,S=63 (#155950)

* Thu Mar 17 2005 Peter Vrabec <pvrabec@redhat.com> 2.10-2
- rebuild

* Thu Dec 09 2004 Peter Vrabec <pvrabec@redhat.com>  2.10-1
- updated to 2.10

* Wed Nov 10 2004 Martin Stransky <stransky@redhat.com> 2.8-16
- add check for minimum count of clusters in FAT16 and FAT32

* Wed Oct 13 2004 Peter Vrabec <pvrabec@redhat.com> 2.8-15
- fix fat_length type in boot.c. (same problem like in RHEL bug #135293)

* Wed Oct  6 2004 Jeremy Katz <katzj@redhat.com> - 2.8-14
- fix rebuilding (#134834)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Sep  3 2003 Bill Nottingham <notting@redhat.com> 2.8-11
- rebuild

* Wed Sep  3 2003 Bill Nottingham <notting@redhat.com> 2.8-10
- don't rely on <linux/msdos_fs.h> including <asm/byteorder.h>

* Tue Jun 24 2003 Jeremy Katz <katzj@redhat.com> 2.8-9
- rebuild

* Tue Jun 24 2003 Jeremy Katz <katzj@redhat.com> 2.8-8
- add patch from Vince Busam (http://www.sixpak.org/dosfstools/) to do auto 
  creation of FAT32 on large devices (#97308)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 19 2003 Jeremy Katz <katzj@redhat.com> 2.8-6
- handle getting the size of loop devices properly (part of #84351)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 2.8-4
- Patch2 for errno

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to version 2.8

* Fri Jul  6 2001 Preston Brown <pbrown@redhat.com>
- major upgrade to v2.7.
- forward port old ia64 patch (now incorporated) s390 additions

* Tue Mar 20 2001 Oliver Paukstadt <oliver.paukstadt@millenux.com>
- ported to zSeries (64 bit)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- hard link mkdosfs

* Thu Jun 15 2000 Matt Wilson <msw@redhat.com>
- FHS
- patch to build against 2.4 kernel headers (patch3)

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix for ia64

* Thu Feb  3 2000 Matt Wilson <msw@redhat.com>
- remove mkdosfs.8 symlink, symlink mkdosfs.8.gz to mkfs.msdos.8.gz

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions and summary
- man pages are compressed

* Thu Dec 16 1999 Cristian Gafton <gafton@redhat.com>
- fix the 2.88MB drives (patch from hjl)

* Mon Aug 16 1999 Matt Wilson <msw@redhat.com>
- updated to 2.2

* Sun Jun 27 1999 Matt Wilson <msw@redhat.com>
- changed to new maintainer, renamed to dosfstools

* Sat Apr 17 1999 Jeff Johnson <jbj@redhat.com>
- fix mkdosfs on sparc (#1746)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Thu Jan 21 1999 Bill Nottingham <notting@redhat.com>
- build for RH 6.0

* Tue Oct 13 1998 Cristian Gafton <gafton@redhat.com>
- avoid using unsinged long on alphas 

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
