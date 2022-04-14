Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:   Writes audio CD-Rs in disk-at-once (DAO) mode
Name:      cdrdao
Version:   1.2.4
Release:   6%{?dist}
License:   GPLv2+
URL:       http://cdrdao.sourceforge.net/
Source0:   http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2

BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  libsigc++30
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  libao-devel
BuildRequires:  libmad-devel
BuildRequires:  lame-devel
#requirements to rebuild autotools
BuildRequires:  autoconf GConf2-devel

# We have removed gcdmaster sub-package in 1.2.3-10
Obsoletes: gcdmaster < 1.2.3-10

# Only exclude s390
ExcludeArch: s390 s390x

# Missing includes causes failure build
# Patches 1 to 5 upstreamed, remove in a future release
#Patch1: cdrdao-1.2.3-stat.patch
#Patch2: cdrdao-1.2.3-helpmansync.patch
#Patch3: cdrdao-1.2.3-format_security.patch
#Patch4: cdrdao-1.2.3-narrowing.patch
#Patch5: cdrdao-1.2.3-lame-3.100.patch
# Patches 6 and 7 grabbed from gentoo
Patch6: cdrdao-1.2.4-wformat-security.patch
Patch7: cdrdao-1.2.4-ax_pthread.patch

%description
Cdrdao records audio CD-Rs in disk-at-once (DAO) mode, based on a
textual description of the CD contents. Recording in DAO mode writes
the complete disc (lead-in, one or more tracks, and lead-out) in a
single step. DAO allows full control over the length and the contents
of pre-gaps, the pause areas between tracks.


%prep
%autosetup -p 1

%build
#run autoreconf to support aarch64
#not needed when upstream moves to  new automake
autoreconf -v -f -i -I.
%configure \
        --without-xdao \
        --without-scglib \
        --with-ogg-support \
        --with-mp3-support \
        --with-lame

%make_build


%install
%make_install

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%files
%doc AUTHORS README CREDITS ChangeLog
%license COPYING
%{_bindir}/cdrdao
%{_bindir}/*toc*
%{_datadir}/cdrdao
%{_mandir}/*/cdrdao*
%{_mandir}/*/cue2toc*
%{_mandir}/*/toc2cue*
%{_mandir}/*/toc2cddb*


%changelog
* Fri Feb 04 2022 Cameron Baird <cameronbaird@microsoft.com> - 1.12.4-6
- Upgrade to to libsigc++30
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 06 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.2.4-1
- update to 1.2.4 fixes rhbz #1579090

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 Filipe Rosset <rosset.filipe@gmail.com> - 1.2.3-33
- fix FTBFS on rawhide
- spec cleanup + silent rpmlint

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Bastien Nocera <bnocera@redhat.com> - 1.2.3-29
+ cdrdao-1.2.3-29
- Add MP3 encoding and decoding support

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 16 2016 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2.3-27
- FTBFS when 255 assigned to a char fixed (narrowing), added cdrdao-1.2.3-narrowing.patch

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.2.3-24
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Dec 05 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2.3-21
- fixed -Werror=format-security violations

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2.3-19
- rerun autotools to support aarch64

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.2.3-17
- Deleted unused patch files

* Tue Oct 09 2012 Honza Horak <hhorak@redhat.com> - 1.2.3-16
- Add missing options to man page

* Mon Aug 27 2012 Honza Horak <hhorak@redhat.com> - 1.2.3-15
- Spec file clean up

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-13
- Rebuilt for c++ ABI breakage

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Honza Horak <hhorak@redhat.com> - 1.2.3-11
- obsolete gcdmaster

* Mon Aug 08 2011 Honza Horak <hhorak@redhat.com> - 1.2.3-10
- removing a sub-package gcdmaster (xdao) due to missing dependencies 
  on libgnomeuimm26

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 20 2011 Honza Horak <hhorak@redhat.com> - 1.2.3-8
- Fixed warning while erasing this package
- https://bugzilla.redhat.com/show_bug.cgi?id=665656

* Thu Sep 02 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 1.2.3-7
- Bump for libao

* Wed Jan 20 2010 Roman Rakus <rrakus@redhat.com>  1.2.3-6
- typo in %%patch

* Wed Jan 20 2010 Roman Rakus rrakus@redhat.com 1.2.3-5
- Some missing includes cause failure build

* Wed Jan 13 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 1.2.3-4
- Merge review #225639
- no need option --with-mp3-support. it needs libmad(don't ship)
- change license to GPLv2+

* Mon Jan 11 2010 rrakus@redhat.com 1.2.3-3
- Fixed typo

* Mon Jan 11 2010 Roman Rakus rrakus@redhat.com 1.2.3-2
- Fixed URL tag
- some cleanup

* Mon Nov 30 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 1.2.3-1
- new upstream

* Wed Sep 23 2009 Orcan Ogetbil <oget[DOT]fedora[AT]gmail[DOT]com> - 1.2.3-0.rc2.4
- Update desktop file according to F-12 FedoraStudio feature

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-0.rc2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 16 2009 Denis Leroy <denis@poolshark.org> - 1.2.3-0.rc2.2
- Make sure version is printed with usage, to fix k3b

* Tue Apr  7 2009 Denis Leroy <denis@poolshark.org> - 1.2.3-0.rc2.1
- Update to latest 1.2.3 release candidate
- Merged with gcdmaster spec file
- Added scripts to manage gcdmaster new schemas file
- Moved desktop file fix into patch
- Added patch to fix gcc 4.4 compile

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.2-5
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 harald@redhat.com 1.2.2-4
- added string.h includes to make it compile again

* Fri Aug 17 2007 Harald Hoyer <harald@redhat.com> - 1.2.2-3
- changed license to GPLv2

* Tue Feb 27 2007 Harald Hoyer <harald@redhat.com> - 1.2.2-2
- fixed specfile issues (bug #225639)

* Wed Jan 24 2007 Harald Hoyer <harald@redhat.com> - 1.2.2-1
- version 1.2.2
- built without cdrecord-devel now

* Mon Aug 21 2006 Harald Hoyer <harald@redhat.com> - 1.2.1-2
- rebuild with new/old cdrtools

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.1-1.1
- rebuild

* Wed Mar 08 2006 Harald Hoyer <harald@redhat.com> - 1.2.1-1
- version 1.2.1 (1.2.0 was not functional)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-1.2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-1.2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Harald Hoyer <harald@redhat.com>
- rebuilt

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Jul 18 2005 Harald Hoyer <harald@redhat.com> 1.2.0-1
- version 1.2.0

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Tue Feb 22 2005 Karsten Hopp <karsten@redhat.de> 1.1.9-8 
- cdrdao builds just fine without the pccts package and uses 
  its own pccts copy.

* Wed Feb 09 2005 Harald Hoyer <harald@redhat.com>
- rebuilt

* Wed Oct 13 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-6
- build requires newer cdrecord-devel

* Tue Sep 21 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-5
- removed INSTALL from doc (bug 132908)

* Wed Sep 08 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-4
- build requires newer cdrecord-devel

* Tue Sep 07 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-3
- build requires newer cdrecord-devel

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Harald Hoyer <harald@redhat.com> - 1.1.9-1
- version 1.1.9

* Wed Apr 14 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-4
- fixed BuildRequires

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-3
- fixed ISO C++ issues

* Fri Feb 20 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-2
- fixed ambigous operator cast

* Wed Feb 18 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-1
- use scsilib from cdrecord-devel

* Mon Feb 16 2004 Harald Hoyer <harald@redhat.com> - 1.1.8-1
- version 1.1.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Harald Hoyer <harald@redhat.de> 1.1.7-8.atapi.1
- added ATAPI: support

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 13 2003 Harald Hoyer <harald@redhat.de> 1.1.7-6
- refined O_EXCL patch, nonroot sg handling

* Mon May 12 2003 Harald Hoyer <harald@redhat.de> 1.1.7-5
- refined O_EXCL patch, nonroot sg handling

* Wed Feb 26 2003 Harald Hoyer <harald@redhat.de> 1.1.7-4
- refined O_EXCL patch

* Tue Feb 25 2003 Harald Hoyer <harald@redhat.de> 1.1.7-3
- readded O_EXCL patch

* Tue Feb 04 2003 Phil Knirsch <pknirsch@redhat.com> 1.1.7-2
- Added s390x again as newer models will have SCSI.

* Wed Jan 29 2003 Harald Hoyer <harald@redhat.de> 1.1.7-1
- updated to 1.1.7

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Nov 28 2002 Harald Hoyer <harald@redhat.de> 1.1.5-11
- added cdrdao-1.1.5-EXCL.patch to lock the CDROM device
- more archs for scsilib (cdrtools)

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Mike A. Harris <mharris@redhat.com> 1.1.5-9
- Rebuilt in new environment with gcc 3.2

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Mike A. Harris <mharris@redhat.com> 1.1.5-6
- Bumped release, and rebuilt against new toolchain.

* Fri Feb 22 2002 Mike A. Harris <mharris@redhat.com> 1.1.5-5
- Bumped release, and rebuilt against new toolchain.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.1.5-4
- automated rebuild

* Sun Dec 23 2001 Mike A. Harris <mharris@redhat.com> 1.1.5-3
- Added missing /usr/share/cdrdao/drivers file (#57785)
- Also built 1.1.5-1.72.0 package for 7.x

* Sat Dec 22 2001 Mike A. Harris <mharris@redhat.com> 1.1.5-2
- Bumped release and rebuilt so rawhide package doesn't release number
  conflict with previous 1.1.5-1 package built against 7.2

* Fri Dec 21 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix non-standard C++ code

* Tue Dec 18 2001 Mike A. Harris <mharris@redhat.com> 1.1.5-1
- Updated to 1.1.5
- Updated endianness patch for ia64
- s/Copyright/License/ in specfile
- Changed to bz2 compression for smaller sources
- Fixed BuildRoot line (was hard coded)

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Tue Jun 26 2001 Bill Nottingham <notting@redhat.com>
- include on ia64

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add excludearch for s390 s390x

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- rebuilt for the distro

* Fri Sep 8 2000 Tim Powers <timp@redhat.com>
- removed all references to xcdrdao, we don't ship it. So no applnk, no gtkmm
  requirements either.

* Thu Sep 7 2000 Tim Powers <timp@redhat.com>
- fixed bad Requires line, was still requiring gtk--, when the package changed
  to gtkmm

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jun 5 2000 Tim Powers <timp@redhat.com>
- man pages in correct location
- use %%makeinstall

* Mon May 8 2000 Tim Powers <timp@redhat.com>
- use applnk for dirs
- use %%configure
- remove redundant defines
- rebuilt for 7.0

* Tue Nov 2 1999 Tim Powers <timp@redhat.com>
- updated to 1.1.3
- we now have xcdrdao
- added gnome menu stuff

* Sat Aug 21 1999 Tim Powers <timp@redhat.com>
- removed wmconfig stuff. Nosuch file names xcdrdao

* Wed Aug 18 1999 Dale Lovelace <dale@redhat.com>
- add cdrdao.wmconfig

* Sat Jul 10 1999 Tim Powers <timp@redhat.com>
- updated to 1.1.1 
- built for 6.1

* Mon May 10 1999 Cristian Gafton <gafton@redhat.com>
- gtk-- does not wokr on the alpha, so we have no xcdrdao for it.
- cheesy workaround for the broken tar archive

* Tue Apr 13 1999 Michael Maher <mike@redhat.com>
- built package 
