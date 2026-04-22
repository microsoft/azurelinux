# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%?mingw_package_header

Summary:        MinGW Windows port of the LibTIFF library
Name:           mingw-libtiff
Version:        4.4.0
Release: 9%{?dist}
License:        libtiff
URL:            http://www.simplesystems.org/libtiff/
Source:         https://download.osgeo.org/libtiff/tiff-%{version}.tar.xz

BuildArch:      noarch

BuildRequires: make
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-libjpeg-turbo
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-zlib
BuildRequires:  mingw64-libjpeg-turbo
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils


%description
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.


# Win32
%package -n mingw32-libtiff
Summary:        MinGW Windows port of the LibTIFF library

%description -n mingw32-libtiff
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package -n mingw32-libtiff-static
Summary:        Static version of the MinGW Windows LibTIFF library
Requires:       mingw32-libtiff = %{version}-%{release}

%description -n mingw32-libtiff-static
Static version of the MinGW Windows LibTIFF library.

# Win64
%package -n mingw64-libtiff
Summary:        MinGW Windows port of the LibTIFF library

%description -n mingw64-libtiff
The libtiff package contains a library of functions for manipulating
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package -n mingw64-libtiff-static
Summary:        Static version of the MinGW Windows LibTIFF library
Requires:       mingw64-libtiff = %{version}-%{release}

%description -n mingw64-libtiff-static
Static version of the MinGW Windows LibTIFF library.


%?mingw_debug_package


%prep
%setup -q -n tiff-%{version}


%build
export MINGW32_CFLAGS="%{mingw32_cflags} -fno-strict-aliasing"
export MINGW64_CFLAGS="%{mingw64_cflags} -fno-strict-aliasing"
%mingw_configure --enable-static --enable-shared --enable-ld-version-script
%mingw_make %{?_smp_mflags}


%install
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

# remove docs
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/doc
rm -rf $RPM_BUILD_ROOT%{mingw32_mandir}
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/doc
rm -rf $RPM_BUILD_ROOT%{mingw64_mandir}

# remove binaries
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/*.exe
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/*.exe

# Drop all .la files
find $RPM_BUILD_ROOT -name "*.la" -delete


# Win32
%files -n mingw32-libtiff
%doc COPYRIGHT README.md RELEASE-DATE VERSION TODO ChangeLog
%{mingw32_bindir}/libtiff-5.dll
%{mingw32_bindir}/libtiffxx-5.dll
%{mingw32_includedir}/*
%{mingw32_libdir}/libtiff.dll.a
%{mingw32_libdir}/libtiffxx.dll.a
%{mingw32_libdir}/pkgconfig/libtiff-4.pc

%files -n mingw32-libtiff-static
%{mingw32_libdir}/libtiff.a
%{mingw32_libdir}/libtiffxx.a

# Win64
%files -n mingw64-libtiff
%doc COPYRIGHT README.md RELEASE-DATE VERSION TODO ChangeLog
%{mingw64_bindir}/libtiff-5.dll
%{mingw64_bindir}/libtiffxx-5.dll
%{mingw64_includedir}/*
%{mingw64_libdir}/libtiff.dll.a
%{mingw64_libdir}/libtiffxx.dll.a
%{mingw64_libdir}/pkgconfig/libtiff-4.pc

%files -n mingw64-libtiff-static
%{mingw64_libdir}/libtiff.a
%{mingw64_libdir}/libtiffxx.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Orion Poplawski <orion@nwra.com> - 4.4.0-1
- Update to 4.4.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Michael Cronenworth <mike@cchtml.com> - 4.3.0-1
- Update to 4.3.0

* Wed Jun 01 2022 Michael Cronenworth <mike@cchtml.com> - 4.2.0-1
- Update to 4.2.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 4.0.9-11
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 4.0.9-5
- Rebuild (Changes/Mingw32GccDwarf2)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 11 2018 Michael Cronenworth <mike@cchtml.com> - 4.0.9-1
- Update to 4.0.9

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Michael Cronenworth <mike@cchtml.com> - 4.0.8-1
- Update to 4.0.8

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Michael Cronenworth <mike@cchtml.com> - 4.0.7-1
- Update to 4.0.7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.3-6
- Fix CVE-2014-9655 and CVE-2015-1547 (RHBZ #1190712)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.3-4
- Fix CVE-2013-4231, CVE-2013-4232, CVE-2013-4243, CVE-2013-4244 (RHBZ #996833)
- Fix CVE-2012-4447, CVE-2012-4564, CVE-2013-1960.patch, CVE-2013-1961

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.3-1
- Update to 4.0.3

* Sat Aug 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2 (RHBZ #850919)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.5-7
- Added win64 support

* Fri Mar 09 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.5-6
- Dropped .la files

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.9.5-5
- Renamed the source package to mingw-libtiff (#800437)
- Spec clean up
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.5-4
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 03 2011 Kalev Lember <kalev@smartlink.ee> - 3.9.5-2
- Rebuilt with mingw32-libjpeg-turbo, dropped jpeg_boolean patch (#604702)

* Mon Apr 25 2011 Kalev Lember <kalev@smartlink.ee> - 3.9.5-1
- Update to 3.9.5
- Fixes CVE-2011-1167 (#689575)
- Dropped the patches from Fedora native libtiff package which are all now
  incorporated in 3.9.5

* Fri Jun 25 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.4-1
- Update to 3.9.4
- Merged the native Fedora package changes up to 3.9.4-1
- Fixes CVE-2010-1411 (RHBZ #592361) and various other CVE's

* Fri Sep 18 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.8.2-20
- Rebuild because of broken mingw32-gcc/mingw32-binutils

* Thu Aug 27 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.8.2-19
- Rebuild for minw32-libjpeg 7
- Automatically generate debuginfo subpackage
- Added -static subpackage

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Michael Ploujnikov <ploujj@gmail.com> - 3.8.2-17
- update upstream URL
- Fix some more LZW decoding vulnerabilities (CVE-2009-2285)
Related: #511015

* Mon Jun 8 2009 Michael Ploujnikov <ploujj@gmail.com> - 3.8.2-16
- add mingw32-gcc-c++ to the BuildRequirements

* Fri Jun 5 2009 Michael Ploujnikov <ploujj@gmail.com> - 3.8.2-15
- replace %%define with %%global as per Fedora packaging guidelines

* Wed Jun 3 2009 Michael Ploujnikov <ploujj@gmail.com> - 3.8.2-14
- cleanup based on initial review and help from Adam Goode:
- removed LIBVER define
- exported proper mingw32 cflags
- removed make check
- removed executables
- removed multilib stuff (irrelevant for mingw32)
- fixed defattr
- added .la files back in

* Sun Mar 22 2009 Michael Ploujnikov <ploujj@gmail.com> - 3.8.2-13
- Initial mingw32 build

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 26 2008 Tom Lane <tgl@redhat.com> 3.8.2-11
- Fix LZW decoding vulnerabilities (CVE-2008-2327)
Related: #458674
- Use -fno-strict-aliasing per rpmdiff recommendation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.8.2-10
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 Tom Lane <tgl@redhat.com> 3.8.2-9
- Update License tag
- Rebuild to fix Fedora toolchain issues

* Thu Jul 19 2007 Tom Lane <tgl@redhat.com> 3.8.2-8
- Restore static library to distribution, in a separate -static subpackage
Resolves: #219905
- Don't apply multilib header hack to unrecognized architectures
Resolves: #233091
- Remove documentation for programs we don't ship
Resolves: #205079
Related: #185145

* Tue Jan 16 2007 Tom Lane <tgl@redhat.com> 3.8.2-7
- Remove Makefiles from the shipped /usr/share/doc/html directories
Resolves: bz #222729

* Tue Sep  5 2006 Jindrich Novy <jnovy@redhat.com> - 3.8.2-6
- fix CVE-2006-2193, tiff2pdf buffer overflow (#194362)
- fix typo in man page for tiffset (#186297)
- use %%{?dist}

* Mon Jul 24 2006 Matthias Clasen <mclasen@redhat.com>
- Fix several vulnerabilities (CVE-2006-3460 CVE-2006-3461
  CVE-2006-3462 CVE-2006-3463 CVE-2006-3464 CVE-2006-3465)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.8.2-4.1
- rebuild

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> - 3.8.2-3
- Fix multilib conflict

* Thu May 25 2006 Matthias Clasen <mclasen@redhat.com> - 3.8.2-3
- Fix overflows in tiffsplit

* Wed Apr 26 2006 Matthias Clasen <mclasen@redhat.com> - 3.8.2-2
- Drop tiffgt to get rid of the libGL dependency (#190768)

* Wed Apr 26 2006 Matthias Clasen <mclasen@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.7.4-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.7.4-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 16 2005 Matthias Clasen <mclasen@redhat.com> 3.7.4-3
- Don't ship static libs

* Fri Nov 11 2005 Matthias Saou <http://freshrpms.net/> 3.7.4-2
- Remove useless explicit dependencies.
- Minor spec file cleanups.
- Move make check to %%check.
- Add _smp_mflags.

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4
- Drop upstreamed patches

* Wed Jun 29 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.2-1
- Update to 3.7.2
- Drop upstreamed patches

* Fri May  6 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.1-6
- Fix a stack overflow

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.1-5
- Don't use mktemp

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.1-4
- Rebuild with gcc4

* Wed Jan  5 2005 Matthias Clasen <mclasen@redhat.com> - 3.7.1-3
- Drop the largefile patch again
- Fix a problem with the handling of alpha channels
- Fix an integer overflow in tiffdump (#143576)

* Wed Dec 22 2004 Matthias Clasen <mclasen@redhat.com> - 3.7.1-2
- Readd the largefile patch (#143560)

* Wed Dec 22 2004 Matthias Clasen <mclasen@redhat.com> - 3.7.1-1
- Upgrade to 3.7.1
- Remove upstreamed patches
- Remove specfile cruft
- make check

* Thu Oct 14 2004 Matthias Clasen <mclasen@redhat.com> 3.6.1-7
- fix some integer and buffer overflows (#134853, #134848)

* Tue Oct 12 2004 Matthias Clasen <mclasen@redhat.com> 3.6.1-6
- fix http://bugzilla.remotesensing.org/show_bug.cgi?id=483

* Mon Sep 27 2004 Rik van Riel <riel@redhat.com> 3.6.1-4
- compile using RPM_OPT_FLAGS (bz #133650)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 20 2004 Matthias Clasen <mclasen@redhat.com> 3.6.1-2
- Fix and use the makeflags patch

* Wed May 19 2004 Matthias Clasen <mclasen@redhat.com> 3.6.1-1
- Upgrade to 3.6.1
- Adjust patches
- Don't install tiffgt man page  (#104864)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- really add symlink to shared lib by running ldconfig at compile time

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Oct 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- link shared lib against -lm (Jakub Jelinek)

* Thu Sep 25 2003 Jeremy Katz <katzj@redhat.com> 3.5.7-13
- rebuild to fix gzipped file md5sum (#91281)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 11 2003 Phil Knirsch <pknirsch@redhat.com> 3.5.7-11
- Fixed rebuild problems.

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlink to shared lib

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 3.5.7-8
- rebuild on all arches

* Mon Aug 19 2002 Phil Knirsch <pknirsch@redhat.com> 3.5.7-7
- Added LFS support (#71593)

* Tue Jun 25 2002 Phil Knirsch <pknirsch@redhat.com> 3.5.7-6
- Fixed wrong exit code of tiffcp app (#67240)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 15 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed segfault in fax2tiff tool (#64708).

* Mon Feb 25 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed problem with newer bash versions setting CDPATH (#59741)

* Tue Feb 19 2002 Phil Knirsch <pknirsch@redhat.com>
- Update to current release 3.5.7

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Aug 28 2001 Phil Knirsch <phil@redhat.de>
- Fixed ia64 problem with tiffinfo. Was general 64 bit arch problem where s390x
  and ia64 were missing (#52129).

* Tue Jun 26 2001 Philipp Knirsch <pknirsch@redhat.de>
- Hopefully final symlink fix

* Thu Jun 21 2001 Than Ngo <than@redhat.com>
- add missing libtiff symlink

* Fri Mar 16 2001 Crutcher Dunnavant <crutcher@redhat.com>
- killed tiff-to-ps.fpi filter

* Wed Feb 28 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed missing devel version dependancy.

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- rebuild

* Mon Aug  7 2000 Crutcher Dunnavant <crutcher@redhat.com>
- added a tiff-to-ps.fpi filter for printing

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply Peter Skarpetis's fix for the 32-bit conversion

* Mon Jul  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- make man pages non-executable (#12811)

* Mon Jun 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove CVS repo info from data directories

* Thu May 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix build rooting
- fix syntax error in configure script
- move man pages to {_mandir}

* Wed May 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild for an errata release

* Wed Mar 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.5.5, which integrates our fax2ps fixes and the glibc fix

* Tue Mar 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix fax2ps swapping height and width in the bounding box

* Mon Mar 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- move man pages from devel package to the regular one
- integrate Frank Warmerdam's fixed .fax handling code (keep until next release
  of libtiff)
- fix fax2ps breakage (bug #8345)

* Sat Feb 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- set MANDIR=man3 to make multifunction man pages friendlier

* Mon Jan 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix URLs

* Fri Jan 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- link shared library against libjpeg and libz

* Tue Jan 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable zip and jpeg codecs
- change defattr in normal package to 0755
- add defattr to -devel package

* Wed Dec 22 1999 Bill Nottingham <notting@redhat.com>
- update to 3.5.4

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 6)

* Wed Jan 13 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed Jun 10 1998 Michael Fulbright <msf@redhat.com>
- rebuilt against fixed jpeg libs (libjpeg-6b)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 13 1997 Donnie Barnes <djb@redhat.com>
- new version to replace the one from libgr
- patched for glibc
- added shlib support
