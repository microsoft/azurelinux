#
# spec file for package gd
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define prjname libgd
%define lname libgd3
Name:           gd
Version:        2.3.3
Release:        4%{?dist}
Summary:        A Drawing Library for Programs That Use PNG and JPEG Output
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://libgd.github.io/
Source:         https://github.com/libgd/libgd/releases/download/%{name}-%{version}/%{prjname}-%{version}.tar.xz
Source1:        baselibs.conf
# might be upstreamed, but could be suse specific also (/usr/share/fonts/Type1 font dir)
Patch1:         gd-fontpath.patch
# could be upstreamed, but not in this form (need ac check for attribute format printf, etc.)
Patch2:         gd-format.patch
# could be upstreamed
Patch3:         gd-aliasing.patch
BuildRequires:  fontconfig-devel
# needed for tests
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
%if %{with_check}
BuildRequires:  fontawesome-fonts
%endif
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(libwebp)
Provides:       gdlib = %{version}
Obsoletes:      gdlib < %{version}

%description
Gd allows your code to quickly draw images complete with lines, arcs,
text, and multiple colors. It supports cut and paste from other images
and flood fills. It outputs PNG, JPEG, and WBMP (for wireless devices)
and is supported by PHP.

%package -n %{lname}
Summary:        A Drawing Library for Programs That Use PNG and JPEG Output
Conflicts:      gd < 2.2.3
# change order while installing a split library
Obsoletes:      gd < 2.2.3

%description -n %{lname}
Gd allows your code to quickly draw images complete with lines, arcs,
text, and multiple colors. It supports cut and paste from other images
and flood fills. It outputs PNG, JPEG, and WBMP (for wireless devices)
and is supported by PHP.

%package devel
Summary:        Drawing Library for Programs with PNG and JPEG Output
Requires:       %{lname} = %{version}
Requires:       glibc-devel

%description devel
gd allows code to quickly draw images complete with lines, arcs, text,
multiple colors, cut and paste from other images, and flood fills. gd
writes out the result as a PNG or JPEG file. This is particularly
useful in World Wide Web applications, where PNG and JPEG are two of
the formats accepted for inline images by most browsers.

%prep
%setup -q -n %{prjname}-%{version}
%patch1
%patch2
%patch3
chmod 644 COPYING

%build
# ADDITIONAL CFLAGS ARE NEEDED TO FIX TEST FAILURES IN CASE OF i586, BUT HARMLESS TO APPLY GENERALLY FOR ALL ix86
%ifarch %{ix86}
export CFLAGS="%{optflags} -msse -mfpmath=sse"
%else
%ifnarch x86_64
export CFLAGS="%{optflags} -ffp-contract=off"
%endif
%endif

# without-x -- useless switch which just mangles cflags
%configure \
	--disable-silent-rules \
	--disable-werror \
	--without-liq \
	--without-x \
	--with-fontconfig \
	--with-freetype \
	--with-jpeg \
	--with-png \
	--with-webp \
	--with-zlib \
	--disable-static
%make_build

%check
%if !0%{?sle_version} || 0%{?sle_version} < 150000
# on SLE15 we have --with-arch-32=x86_64 so the test actually
# passes boo#1053825
%ifarch %{ix86}
# See https://github.com/libgd/libgd/issues/359
XFAIL_TESTS="gdimagegrayscale/basic $XFAIL_TESTS"
%endif
%endif
export XFAIL_TESTS
export TMPDIR=${TMPDIR:/tmp}
%make_build check

%install
%make_install

find %{buildroot} -type f -name "*.la" -delete -print

%post -n %{lname} -p /sbin/ldconfig
%postun -n %{lname} -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/annotate
%{_bindir}/bdftogd
%{_bindir}/gd2copypal
%{_bindir}/gd2togif
%{_bindir}/gd2topng
%{_bindir}/gdcmpgif
%{_bindir}/gdparttopng
%{_bindir}/gdtopng
%{_bindir}/giftogd2
%{_bindir}/pngtogd
%{_bindir}/pngtogd2
%{_bindir}/webpng

%files -n %{lname}
%license COPYING
%{_libdir}/*.so.*

%files devel
%license COPYING
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gdlib.pc

%changelog
* Wed May 17 2023 Olivia Crain <oliviacrain@microsoft.com> - 2.3.3-4
- Bumping release to re-build with newer 'libtiff' libraries.

* Fri Mar 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.3-3
- Bumping release to re-build with newer 'libtiff' libraries.

* Tue Jun 28 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.3.3-2
- Added temporary directory variable to check section to fix failing tests
- See https://github.com/libgd/libgd/issues/763 for details

* Tue May 31 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.3.3-1
- Upgrade to 2.3.3 to address CVE-2021-38115 and CVE-2021-40812

* Tue Apr 12 2022 Muhammad Falak <mwani@microsoft.com> - 2.3.0-5
- Backport patch from upstream to address CVE-2021-40145

* Fri Feb 04 2022 Muhammad Falak <mwani@microsoft.com> - 2.3.0-4
- Add an explicit BR on 'fontawesome-fonts' to enable ptest

* Wed Jan 26 2022 Henry Li <lihl@microsoft.com> - 2.3.0-3
- License Verified
- Fix linting

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Dec 17 2020 Joe Schmitt <joschmit@microsoft.com> - 2.3.0-2.2
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Remove X11 dependencies

* Sun Aug  9 2020 Matthias Eliasson <elimat@opensuse.org>
- Version update to 2.3.0:
  [#]## Security
  - Potential double-free in gdImage*Ptr(). (CVE-2019-6978)
  - gdImageColorMatch() out of bounds write on heap. (CVE-2019-6977)
  - Uninitialized read in gdImageCreateFromXbm(). (CVE-2019-11038)
  - Double-free in gdImageBmp. (CVE-2018-1000222)
  - Potential NULL pointer dereference in gdImageClone(). (CVE-2018-14553)
  - Potential infinite loop in gdImageCreateFromGifCtx(). (CVE-2018-5711)
  [#]## Fixed
  - Fix #597: add codecov support
  - Fix #596: gdTransformAffineCopy run error
  - Fix #589: Install dependencies move to .travis.yml
  - Fix #586: gdTransformAffineCopy() segfaults on palette images
  - Fix #585: gdTransformAffineCopy() changes interpolation method
  - Fix #584: gdImageSetInterpolationMethod(im, GD_DEFAULT) inconsistent
  - Fix #583: gdTransformAffineCopy() may use unitialized values
  - Fix #533: Remove cmake modules
  - Fix #539: Add RAQM support for cmake
  - Fix #499: gdImageGifAnimAddPtr: heap corruption with 2 identical images
  - Fix #486: gdImageCropAuto(�, GD_CROP_SIDES) crops left but not right
  - Fix #485: auto cropping has insufficient precision
  - Fix #479: Provide a suitable malloc function to liq
  - Fix #474: libtiff link returns 404 HTTP code
  - Fix #450: Failed to open 1 bit per pixel bitmap
  - Fix #440: new_width & new_height exception handling
  - Fix #432: gdImageCrop neglecting transparency
  - Fix #420: Potential infinite loop in gdImageCreateFromGifCtx
  - Fix #411: gd_gd.c format documentation appears to be incorrect
  - Fix #369: Fix new_a init error in gdImageConvolution()
  - Fix #351: gdImageFilledArc() doesn't properly draw pies
  - Fix #338: Fatal and normal libjpeg/libpng errors not distinguishable
  - Fix #169: Update var type to hold bigger w&h for ellipse
  - Fix #164: update doc files install directory in CMakeLists.txt
  - Correct some test depend errors
  - Update cmake min version to 3.7
  - Delete libimagequant source code download action in CMakeLists.txt
  - Improve msys support
  - Fix some logic error in CMakeLists.txt
  - Remove the following macro: HAVE_STDLIB_H, HAVE_STRING_H, HAVE_STDDEF_H,
    HAVE_LIMITS_H, HAVE_ERRNO_H, AC_C_CONST
  [#]## Added
  - test cases for following API: gdImageCopyResized(), gdImageWebpEx(),
    gdImageCreateFromGd2PartPtr(),  gdImageCloneMatch(),
    gdImageColorClosestHWB(), gdImageColorMatch(), gdImageStringUp(),
    gdImageStringUp16(), gdImageString(), gdImageString16(),
    gdImageCopyMergeGray(), gdImageCopyMerge()
- Drop CVE patches now fixed upstream:
  - gd-CVE-2018-1000222.patch
  - gd-CVE-2018-14553.patch
  - gd-CVE-2018-5711.patch
  - gd-CVE-2019-11038.patch
  - gd-CVE-2019-6977.patch
  - gd-CVE-2019-6978.patch
- Drop patch: libgd-config.patch since upstream have dropped libgd-config binary
- Run spec-cleaner
  + Remove package groups
  + use license macro
  + use make macros
* Wed Mar  4 2020 pgajdos@suse.com
- security update
- added patches
  fix CVE-2018-14553 [bsc#1165471], null pointer dereference in gdImageClone()
  + gd-CVE-2018-14553.patch
* Tue Jul 16 2019 pgajdos@suse.com
- security update
- added patches
  CVE-2019-11038 [bsc#1140120]
  + gd-CVE-2019-11038.patch
* Thu May 30 2019 pgajdos@suse.com
- change order while installing splitted library [bsc#1136574]
* Thu Jan 31 2019 Petr Gajdos <pgajdos@suse.com>
- security update
  * CVE-2019-6978 [bsc#1123522]
    + gd-CVE-2019-6978.patch
  * CVE-2019-6977 [bsc#1123361]
    + gd-CVE-2019-6977.patch
* Thu Dec 13 2018 meissner@suse.com
- add gd-devel as baselibs, for building 32bit libaries on 64bit
* Mon Aug 27 2018 pgajdos@suse.com
- security update:
  * CVE-2018-1000222 [bsc#1105434]
    + gd-CVE-2018-1000222.patch
* Tue Mar 13 2018 crrodriguez@opensuse.org
- libgd-config.patch: do not inject false dependencies into
  packages, GD does not need extra libs to be used.
  this also allows us to clean up -devel package dependencies.
* Mon Jan 22 2018 pgajdos@suse.com
- security update:
  * CVE-2018-5711 [bsc#1076391]
    + gd-CVE-2018-5711.patch
* Tue Sep  5 2017 pgajdos@suse.com
- Version update to 2.2.5:
  [#]## Security
  - Double-free in gdImagePngPtr(). (CVE-2017-6362)
  - Buffer over-read into uninitialized memory. (CVE-2017-7890)
  [#]## Fixed
  - Fix #109: XBM reading fails with printed error
  - Fix #338: Fatal and normal libjpeg/ibpng errors not distinguishable
  - Fix #357: 2.2.4: Segfault in test suite
  - Fix #386: gdImageGrayScale() may produce colors
  - Fix #406: webpng -i removes the transparent color
  - Fix Coverity #155475: Failure to restore alphaBlendingFlag
  - Fix Coverity #155476: potential resource leak
  - Fix several build issues and test failures
  - Fix and reenable optimized support for reading 1 bps TIFFs
  [#]## Added
  - The native MSVC buildchain now supports libtiff and most executables
- removed patches (upstreamed):
  . gd-freetype.patch
  . gd-rounding.patch
* Tue Aug 15 2017 lnussel@suse.de
- Don't fail gdimagegrayscale/basic on SLE15 (boo#1053825)
* Fri Jul 21 2017 tchvatal@suse.com
- Add patch gd-rounding.patch
- Set again the cflags so other archs do not fail testsuite
* Fri Jul  7 2017 tchvatal@suse.com
- Version update to 2.2.4:
  * gdImageCreate() doesn't check for oversized images and as such is prone
    to DoS vulnerabilities. (CVE-2016-9317) bsc#1022283
  * double-free in gdImageWebPtr() (CVE-2016-6912) bsc#1022284
  * potential unsigned underflow in gd_interpolation.c (CVE-2016-10166)
    bsc#1022263
  * DOS vulnerability in gdImageCreateFromGd2Ctx() (CVE-2016-10167)
    bsc#1022264
  * Signed Integer Overflow gd_io.c (CVE-2016-10168) bsc#1022265
- Remove patches merged/obsoleted by upstream:
  * gd-config.patch
  * gd-disable-freetype27-failed-tests.patch
  * gd-test-unintialized-var.patch
- Add patch gd-freetype.patch taking patch from upstream for
  freetype 2.7
* Fri Dec  9 2016 pgajdos@suse.com
- devel package also require libwebp-devel
* Thu Dec  8 2016 crrodriguez@opensuse.org
- Support webp format, BuildRequires libwebp-devel
* Thu Dec  8 2016 crrodriguez@opensuse.org
- Honour %%optflags correctly.
* Fri Sep 30 2016 badshah400@gmail.com
- Update to version 2.2.3:
  + Security fixes:
  - Php bug#72339, Integer Overflow in _gd2GetHeader
    (CVE-2016-5766)
  - Issue gh/libgd/libgd#247: A read out-of-bands was found in
    the parsing of TGA files (CVE-2016-6132)
  - Issue gh/libgd/libgd#247: Buffer over-read issue when
    parsing crafted TGA file (CVE-2016-6214)
  - Issue gh/libgd/libgd#248: fix Out-Of-Bounds Read in
    read_image_tga
  - Integer overflow error within _gdContributionsAlloc()
    (CVE-2016-6207)
  - Fix php bug#72494, invalid color index not handled, can lead
    to crash (CVE-2016-6128)
  + Improve color check for CropThreshold
  + gdImageCopyResampled has been improved. Better handling of
    images with alpha channel, also brings libgd in sync with
    php's bundled gd.
- Drop patches:
  + gd-CVE-2016-5116.patch: upstreamed
  + gd-CVE-2016-6132.patch: upstreamed
  + gd-CVE-2016-6214.patch: upstreamed
  + gd-CVE-2016-6905.patch: upstreamed
  + gd-libvpx.patch: vpx support dropped.
- Add BuildRequires for automake and autoconf since
  gd-disable-freetype27-failed-tests.patch touches makefiles.
- Drop getver.pl from source: included in upstream tarball.
- Add "-msse -mfpmath=sse" to CFLAGS to fix tests on ix86
  architectures.
- Add "-ffp-contract=off" to CFLAGS for non-ix86 arch (ppc, arm)
  to fix a test: see gh#libgd/libgd#278.
- Add gd-test-unintialized-var.patch to fix an uninitialised
  variable in tests/gd2/gd2_read.c to prevent it from compiling
  with -Werror (only causes problems in no ix86 arch
  surprisingly); patch sent upstream.
- Rebase gd-disable-freetype27-failed-tests.patch for updated
  version.
- Update URL and Source to project's new github URL's.
* Thu Sep 29 2016 badshah400@gmail.com
- Add gd-disable-freetype27-failed-tests.patch: Disable for now
  tests failing against freetype >= 2.7 for being too exact
  (gh#libgd/libgd#302). The failures have been understood by
  upstream to be due to minor differences between test images and
  those generated when freeetype >= 2.7 is used to build gd.
* Tue Aug 23 2016 pgajdos@suse.com
- security update:
  * CVE-2016-6132 [bsc#987577]
    + gd-CVE-2016-6132.patch
  * CVE-2016-6214 [bsc#991436]
    + gd-CVE-2016-6214.patch
  * CVE-2016-6905 [bsc#995034]
    + gd-CVE-2016-6905.patch
* Mon May 30 2016 pgajdos@suse.com
- security update:
  * CVE-2016-5116 [bsc#982176]
    + gd-CVE-2016-5116.patch
* Tue Mar  1 2016 pgajdos@suse.com
- add missing config/getver.pl [bsc#965190]
* Tue May 12 2015 joerg.lorenzen@ki.tng.de
- Added patch gd-libvpx.patch to enable build against libvpx >= 1.4,
  new VPX_ prefixed namespaces are available since libvpx = 0.9.1.
* Sat Feb 28 2015 mpluskal@suse.com
- Cleanup spec file with spec-cleaner
- No longer needed patches
  * gd-2.1.0-CVE-2014-2497.patch
  * gd-autoconf.patch
- Update to 2.1.1
  * changelog provided only as commit log (see Changelog)
  * fix for CVE-2014-2497
* Tue Aug 26 2014 jengelh@inai.de
- Resolve build failure with automake-1.14
* Fri Jun 27 2014 meissner@suse.com
- split out libgd3, so libgd2 could be installed in parallel.
* Thu Apr 17 2014 tchvatal@suse.com
- Add tiff and vpx to the devel deps as it is in .pc file.
* Thu Apr 10 2014 pgajdos@suse.com
- build against libtiff and libvpx
* Fri Apr  4 2014 pgajdos@suse.com
- fixed NULL ptr deref in GD XPM decoder [bnc#868624]
  * CVE-2014-2497.patch
* Fri Dec 27 2013 tchvatal@suse.com
- Cleanup here&there to parallelize everything
- Remove bogus cmake dependency
* Tue Dec 17 2013 pgajdos@suse.com
- updated to 2.1.0
- removed warn.patch (not needed)
- removed ppc64.patch (upstreamed)
- removed gd-png_check_sig.patch (upstreamed)
* Sun Feb  3 2013 crrodriguez@opensuse.org
- gd-autoconf.patch fix up compile file so gd can handle
  large files on 32 bit
* Sun Feb  5 2012 jengelh@medozas.de
- Remove redundant tags/sections
- Parallel build with %%_smp_mflags
- Remove pointless INSTALL file from rpm package
  (it's just the default autotools INSTALL blurb)
* Wed Oct  5 2011 uli@suse.com
- cross-build fix: use libpng from sysroot
* Sat Oct  1 2011 coolo@suse.com
- add libtool as buildrequire to make the spec file more reliable
* Tue Jun 14 2011 aj@suse.de
- Devel package needs zlib-devel and libpng-devel.
* Tue Apr  6 2010 ro@suse.de
- add baselibs.conf (for libpghoto2)
* Sun Apr  4 2010 ro@suse.de
- replace png_check_sig by negated png_sig_cmp for libpng14
* Wed Nov 12 2008 crrodriguez@suse.de
- QA Results: Regression on PPC64 only, detected by PHP test suite,
  the system libgd part, fix by IBM
* Mon Mar 10 2008 crrodriguez@suse.de
- fix rpm version number, otherwise it wont upgrade later.
* Fri Jan 18 2008 anosek@suse.cz
- updated to version 2.0.36RC1
  * Fixed gdImageCopy with true color image, the transparent color was ignored
  * Fixed support of PNG grayscale image with alpha channel
  * Added Netware builds script
  * ease the creation of regexp to match symbols/functions in the sources
  * _gdCreateFromFile() can crash if gdImageCreate fails
  * gdImageCreateFrom*Ptr() can crash if gdNewDynamicCtxEx() fails
  * gdImageRectangle draws 1x1 rectangles as 1x3 rectangles
  * Possible integer overflow in gdImageFill()
  * Optimization for single pixel line not in correct order
  * gdImageColorDeallocate can write outside buffer
  * gdImageColorTransparent can write outside buffer
  * gdImageWBMPCtx can crash when createwbmp fails
  * Fixed decoding of the html entity &thetasym;
  * Fixed configure script ignoring --with-png=DIR option
- dropped obsoleted security.patch
* Thu Dec 20 2007 crrodriguez@suse.de
- remove static libraries and "la" files
- devel package dependency cleanup
* Mon Jul  9 2007 anosek@suse.cz
- updated to version 2.0.35
  * Fix valgrind error in gdImageFillTiled (Nuno Lopes)
  * Add missing custom cmake macros (required for the tests suite)
  * Avoid signature buffer copy  in gd_gif_c (Nuno Lopes)
  * Race condition in gdImageStringFTEx (Antony Dogval, Pierre
    Scott MacVicar)
  * Reading GIF images is not thread safe (static usage in private
    functions) (Roman Nemecek, Nuno Lopes, Pierre)
  * GIF Local palette is read twice
  * GIF, Use local frame dimension when possible instead of the
    logical screen size (Pierre)
  * GIF, do not try to use the global colmap if it does not exist
    (Nuno Lopes, Pierre)
  * gdImageAALine draws axis lines with two pixels width (Pierre)
  * gdImageArc CPU usage with large angles (Pierre)
  * gdImageFilledRectangle regression fixed when used with reversed
    edges (Pierre)
  * Possible infinite loop in libgd/gd_png.c, flaw found by Xavier
    Roche (Pierre)
  * Fixed segfault when an invalid color index is present in a GIF
    image data, reported by Elliot <wccode at gmail dot com> (Pierre)
  * Possible integer overflow in gdImageCreateTrueColor (Pierre)
    gdImageCreateXbm can crash if gdImageCreate fails (Pierre)
- dropped obsolete patches (png-loop-CVE-2007-2756.patch)
* Tue May 29 2007 nadvornik@suse.cz
- fixed infinite loop on truncated png images
  CVE-2007-2756 [#276525]
* Thu May  3 2007 prusnak@suse.cz
- changed expat to libexpat-devel in Requires of devel subpackage
* Tue Feb 20 2007 nadvornik@suse.cz
- updated to 2.0.34:
  * security fixes merged upstream
  * various other bugfixes
* Wed Aug 16 2006 aj@suse.de
- Reduce BuildRequires.
* Wed Aug 16 2006 aj@suse.de
- Remove unneeded BuildRequire xorg-x11.
* Wed Aug 16 2006 aj@suse.de
- Do not use fonts to build package.
* Wed Aug 16 2006 sndirsch@suse.de
- gd-fontpath.diff: fixes new fontpath for Type1 fonts
* Mon Aug  7 2006 nadvornik@suse.cz
- adjusted ttf fonts path for gdtestft
* Fri Jun 23 2006 nadvornik@suse.cz
- fixed another check for return value on error [#186953]
- gdlib-config is moved to devel package [#168628]
* Thu Jun  8 2006 nadvornik@suse.cz
- fixed check for EOF in gd_gif_in.c [#182334]
* Wed Mar  8 2006 sbrabec@suse.cz
- Fixed devel dependencies.
* Wed Jan 25 2006 mls@suse.de
- converted neededforbuild to BuildRequires
* Thu Jan 12 2006 nadvornik@suse.cz
- compile with -fstack-protector
* Thu Jan  5 2006 nadvornik@suse.cz
- fixed another integer overflow [#138007]
* Thu Nov 24 2005 meissner@suse.de
- fixed 1 aliasing issue.
* Sat Feb  5 2005 meissner@suse.de
- added 1 missign format attribute
* Mon Nov 22 2004 nadvornik@suse.cz
- run test programs during build [#48382]
* Mon Nov 15 2004 nadvornik@suse.cz
- fixed more overflows - CAN-2004-0941 [#47666]
* Tue Nov  2 2004 nadvornik@suse.cz
- updated to 2.0.32:
  * fixed several integer overflows [#47666]
  * animated gif support
* Tue Aug 24 2004 nadvornik@suse.cz
- updated to 2.0.28:
  restored support for reading and writing GIF images
* Fri Feb 20 2004 schwab@suse.de
- Fix missing return value.
* Thu Feb  5 2004 nadvornik@suse.cz
- updated to 2.0.22
- fixed dangerous compiler warnings
* Sat Jan 10 2004 adrian@suse.de
- add %%defattr and %%run_ldconfig
* Tue Jan  6 2004 nadvornik@suse.cz
- updated to 2.0.17
- fixed to build with new freetype
* Thu Jul 24 2003 mjancar@suse.cz
- update to 2.0.15
* Thu Feb 13 2003 nadvornik@suse.cz
- updated to 2.0.11: speed improvements, bugfixes
* Fri Dec 13 2002 prehak@suse.cz
- added gdImageCreateFromXpm() function prototype to gd.h
* Thu Nov 28 2002 nadvornik@suse.cz
- updated to 2.0.8
* Tue Sep 17 2002 ro@suse.de
- removed bogus self-provides
* Tue May 28 2002 bk@suse.de
- gd-devel requires gd and use prefix, bindir and includedir macros
* Wed Feb 13 2002 nadvornik@suse.cz
- used macro %%{_libdir}
* Thu Jan 31 2002 ro@suse.de
- changed neededforbuild <libpng> to <libpng-devel-packages>
* Mon Nov  5 2001 ro@suse.de
- fix Makefile.am for automake 1.5 (removed duplicated line)
* Fri May 25 2001 pblaha@suse.cz
- fix include on ia64
* Thu Mar 29 2001 ro@suse.de
- use aclocal
* Wed Mar 21 2001 ro@suse.de
- update to 1.8.4
- use freetype2
* Mon Dec  4 2000 pblaha@suse.cz
- move simbolick link libgd.so -> gd-devel
* Thu Nov 30 2000 aj@suse.de
- Add suse_update_config.
* Wed Nov 15 2000 pblaha@suse.cz
- aplied patch from perl-GD and split to gd & gd-devel
* Mon Jun  5 2000 bubnikv@suse.cz
- updated to 1.8.3
* Fri May 12 2000 nadvornik@suse.cz
- update to 1.8.1
- added BuildRoot
* Mon Oct 11 1999 ro@suse.de
- added xpm and ttf support
* Sun Oct 10 1999 ro@suse.de
- added libpng to neededforbuild
* Thu Oct  7 1999 schwab@suse.de
- update to 1.7.3
* Mon Sep 13 1999 bs@suse.de
- ran old prepare_spec on spec file to switch to new prepare_spec.
* Thu Sep  9 1999 bs@suse.de
- fixed call of Check at the end of %%install section
* Tue Jun 15 1999 ro@suse.de
- fixed doc installation
* Tue Jun 15 1999 ro@suse.de
- update to 1.3
* Thu Feb  5 1998 ro@suse.de
- ready for autobuild
