# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel}
%bcond_with liq
%bcond_with raqm
%bcond_with avif
%else
# Enabled by default
%bcond_without liq
%bcond_without avif
%endif
# disabled as breaks vertical text
# See https://bugzilla.redhat.com/2022957
%bcond_with    raqm
# Not available in Fedora, only in rpmfusion
# Also see https://github.com/libgd/libgd/issues/678 segfault
%bcond_with    heif


Summary:       A graphics library for quick creation of PNG or JPEG images
Name:          gd
Version:       2.3.3
Release: 20%{?prever}%{?short}%{?dist}
License:       GD
URL:           http://libgd.github.io/
%if 0%{?commit:1}
# git clone https://github.com/libgd/libgd.git; cd gd-libgd
# git archive  --format=tgz --output=libgd-%{version}-%{commit}.tgz --prefix=libgd-%{version}/  master
Source0:       libgd-%{version}-%{commit}.tgz
%else
Source0:       https://github.com/libgd/libgd/releases/download/gd-%{version}/libgd-%{version}.tar.xz
%endif

# Needed by PHP see https://github.com/libgd/libgd/pull/766
Patch0:        libgd-flip.patch
# Missing header see https://github.com/libgd/libgd/pull/766
Patch1:        libgd-iostream.patch

BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: gettext-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libwebp-devel
%if %{with liq}
BuildRequires: libimagequant-devel
%endif
%if %{with raqm}
BuildRequires: libraqm-devel
%endif
%if %{with avif}
BuildRequires: libavif-devel
%endif
%if %{with heif}
BuildRequires: libheif-devel
%endif
BuildRequires: libX11-devel
BuildRequires: libXpm-devel
BuildRequires: zlib-devel
BuildRequires: pkgconfig
BuildRequires: libtool
BuildRequires: perl-interpreter
BuildRequires: perl-generators
BuildRequires: perl(FindBin)
# for fontconfig/basic test
BuildRequires: liberation-sans-fonts
BuildRequires: make


%description
The gd graphics library allows your code to quickly draw images
complete with lines, arcs, text, multiple colors, cut and paste from
other images, and flood fills, and to write out the result as a PNG or
JPEG file. This is particularly useful in Web applications, where PNG
and JPEG are two of the formats accepted for inline images by most
browsers. Note that gd is not a paint program.


%package progs
Requires:       %{name}%{?_isa} = %{version}-%{release}
Summary:        Utility programs that use libgd

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images.


%package devel
Summary:  The development libraries and header files for gd
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: freetype-devel%{?_isa}
Requires: fontconfig-devel%{?_isa}
Requires: libjpeg-devel%{?_isa}
Requires: libpng-devel%{?_isa}
Requires: libtiff-devel%{?_isa}
Requires: libwebp-devel%{?_isa}
Requires: libX11-devel%{?_isa}
Requires: libXpm-devel%{?_isa}
Requires: zlib-devel%{?_isa}
%if %{with liq}
Requires: libimagequant-devel%{?_isa}
%endif
%if %{with raqm}
Requires: libraqm-devel
%endif
%if %{with avif}
Requires: libavif-devel
%endif
%if %{with heif}
Requires: libheif-devel
%endif


%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.


%prep
%setup -q -n libgd-%{version}%{?prever:-%{prever}}
%patch -P0 -p1
%patch -P1 -p1

: $(perl config/getver.pl)

: regenerate autotool stuff
if [ -f configure ]; then
   libtoolize --copy --force
   autoreconf -vif
else
   ./bootstrap.sh
fi


%build
# Provide a correct default font search path
CFLAGS="-std=gnu17 $RPM_OPT_FLAGS -DDEFAULT_FONTPATH='\"\
/usr/share/fonts/bitstream-vera:\
/usr/share/fonts/dejavu:\
/usr/share/fonts/default/Type1:\
/usr/share/X11/fonts/Type1:\
/usr/share/fonts/liberation\"'"

%ifarch %{ix86}
# see https://github.com/libgd/libgd/issues/242
CFLAGS="$CFLAGS -msse -mfpmath=sse"
%endif

%ifarch aarch64 ppc64 ppc64le s390 s390x x86_64 riscv64
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1359680
export CFLAGS="$CFLAGS -ffp-contract=off"
%endif

%configure \
    --enable-gd-formats \
    --with-tiff=%{_prefix} \
    --disable-rpath
make %{?_smp_mflags}


%install
make install INSTALL='install -p' DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.a


%check
# Workaround to https://github.com/libgd/libgd/issues/763
export TMPDIR=/tmp

: Upstream test suite
make check

: Check content of pkgconfig
grep %{version} $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gdlib.pc


%ldconfig_scriptlets


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/*.so.*

%files progs
%{_bindir}/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gdlib.pc


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 06 2024 Richard W.M. Jones <rjones@redhat.com> - 2.3.3-16
- Bump and rebuild package (for riscv64)

* Wed Jan 31 2024 František Zatloukal <fzatlouk@redhat.com> - 2.3.3-15
- Rebuilt for libavif 1.0.3

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Mar 04 2023 Sandro Mani <manisandro@gmail.com> - 2.3.3-11
- Rebuild (libimagequant)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Kalev Lember <klember@redhat.com> - 2.3.3-9
- Rebuild for new libavif

* Sun Oct 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 2.3.3-8
- Rebuild for new libavif

* Sun Oct 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 2.3.3-7
- Rebuild for new libavif

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Robert-André Mauchin <zebob.m@gmail.com> - 2.3.3-4
- Rebuild for libavif soname bump

* Fri Nov 19 2021 Remi Collet <remi@remirepo.net> - 2.3.3-3
- disable libraqm usage, see #2022957

* Mon Sep 20 2021 Paul Howarth <paul@city-fan.org> - 2.3.3-2
- Explicitly enable gd/gd2 formats, wanted by perl bindings (#2005916)

* Mon Sep 13 2021 Remi Collet <remi@remirepo.net> - 2.3.3-1
- update to 2.3.3
- open https://github.com/libgd/libgd/pull/766 missing macros
- open https://github.com/libgd/libgd/pull/767 missing headers

* Tue Jul 27 2021 Florian Weimer <fweimer@redhat.com> - 2.3.2-9
- Rebuild again for libavif soname bump

* Thu Jul 22 2021 Robert-André Mauchin <zebob.m@gmail.com> - 2.3.2-8
- Rebuild for libavif soname bump

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Robert-André Mauchin <zebob.m@gmail.com> - 2.3.2-6
- Rebuild for libavif soname bump

* Sun May 23 2021 Robert-André Mauchin <zebob.m@gmail.com> - 2.3.2-5
- Rebuild for libavif soname bump

* Mon Mar 29 2021 Robert-André Mauchin <zebob.m@gmail.com> - 2.3.2-4
- Rebuild for libavif soname bump

* Wed Mar 17 2021 Filip Januš <fjanus@redhat.com> - 2.3.2-3
- Add condition if fedora for packages not available in RHEL

* Mon Mar  8 2021 Remi Collet <remi@remirepo.net> - 2.3.2-2
- enable avif support
- use bcond

* Mon Mar 08 2021 Ondrej Dubaj <odubaj@redhat.com> - 2.3.2-1
- rebase to version 2.3.2

* Wed Feb 3 2021 Filip Januš <fjanus@redhat.com> - 2.3.1-1
- Upstream released new version 2.3.1
- patch bug615 is no more needed - fixed by upstream in release
- gdimagestring16/gdimagestring16 gdimagestringup16/gdimagestringup16 passed on
  x390s - XFAIL_TEST definition for x390s is no more necessary

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Remi Collet <remi@remirepo.net> - 2.3.0-2
- fix gdImageStringFT() fails for empty strings
  https://github.com/libgd/libgd/issues/615

* Tue Mar 24 2020 Remi Collet <remi@remirepo.net> - 2.3.0-1
- update to 2.3.0
- add dependency on libraqm
- remove gdlib-config

* Fri Jan 31 2020 Filip Januš <fjanus@redhat.com> - 2.2.5-12
- Add patch(gd-2.2.5-null-pointer.patch) - fix Null pointer reference in gdImageClone (gdImagePtr src)
- Resolves: #1599032

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 odubaj@redhat.com - 2.2.5-10
- Fixed heap based buffer overflow in gd_color_match.c:gdImageColorMatch() in libgd as used in imagecolormatch()
- Resolves: RHBZ#1678104 (CVE-2019-6977)
- Fixed potential double-free in gdImage*Ptr()
- Resolves: RHBZ#1671391 (CVE-2019-6978)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 07 2018 mskalick@redhat.com - 2.2.5-7
- Add missing requires to libimagequent-devel

* Thu Aug 30 2018 mskalick@redhat.com - 2.2.5-6
- Use libimagequant library (RHBZ#1468338)

* Thu Aug 30 2018 mskalick@redhat.com - 2.2.5-5
- Check return value in gdImageBmpPtr to avoid double free (CVE-2018-1000222)
- Don't mark gdimagegrayscale/basic test as failing

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 26 2018 Marek Skalický <mskalick@redhat.com> - 2.2.5-3
- Fix CVE-2018-5711 - Potential infinite loop in gdImageCreateFromGifCtx

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 30 2017 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Update to 2.2.5
- fix double-free in gdImagePngPtr(). CVE-2017-6362
- fix buffer over-read into uninitialized memory. CVE-2017-7890

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 2.2.4-2
- Rebuild (libwebp)

* Wed Jan 18 2017 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4

* Tue Dec 06 2016 Marek Skalický <mskalick@redhat.com> - 2.2.3-5
- Fix invalid read in gdImageCreateFromTiffPtr() ( CVE-2016-6911)
- Disable tests using freetype in Fedora 26 (freetype > 2.6)

* Mon Dec 05 2016 Marek Skalický <mskalick@redhat.com> - 2.2.3-4
- Fix stack based buffer overflow when passing negative `rlen` as size to
  memcpy() (CVE-2016-8670)

* Mon Dec 05 2016 Marek Skalický <mskalick@redhat.com> - 2.2.3-3
- Fix possible overflow in gdImageWebpCtx (CVE-2016-7568)

* Tue Jul 26 2016 Dan Horák <dan[at]danny.cz> - 2.2.3-2
- apply workaround for rhbz#1359680

* Fri Jul 22 2016 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3
- use -msse -mfpmath=sse build options (x86-32)

* Fri Jun 24 2016 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Sat May 28 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-2
- remove unneeded sources

* Fri May 27 2016 Marek Skalicky <mskalick@redhat.com> - 2.2.1-1
- Upgrade to 2.2.1 release
- Upstream moved to github.com

* Thu Apr 28 2016 Marek Skalicky <mskalick@redhat.com> - 2.1.1-7
- Fixed heap overflow (CVE-2016-3074)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec  1 2015 Tom Callaway <spot@fedoraproject.org> - 2.1.1-5
- rebuild for libvpx 1.5.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 2.1.1-3
- rebuild for libvpx 1.4.0

* Mon Mar 23 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-2
- fix version in gdlib.pc
- fix license handling

* Wed Jan 14 2015 Jozef Mlich <jmlich@redhat.com> - 2.1.1-1
- Update to 2.1.1 final
  Resolves: #1181972

* Thu Jan 08 2015 Jozef Mlich <jmlich@redhat.com> - 2.1.0-8
- Resolves: #1076676 CVE-2014-2497
  Previous patch indroduced memory leak. Using upstream version.
  https://bitbucket.org/libgd/gd-libgd/commits/463c3bd09bfe8e924e19acad7a2a6af16953a704

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 16 2014 Jozef Mlich <jmlich@redhat.com> - 2.1.0-6
- Resolves: #1076676 CVE-2014-2497
  NULL pointer dereference in gdImageCreateFromXpm()

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 23 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.0-4
- Fix FTBFS

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.1.0-2
- Perl 5.18 rebuild

* Tue Jun 25 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- update to 2.1.0 final

* Tue Jun 25 2013 Remi Collet <rcollet@redhat.com> - 2.1.0-0.2.725ba9d
- rebuild for linpng 1.6

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 2.1.0-0.1.725ba9d
- update to 2.1.0 (post RC2 git snapshot)

* Tue Apr 23 2013 Remi Collet <rcollet@redhat.com> - 2.0.35-25
- drop uneeded patch
- really set default font search path

* Mon Mar 25 2013 Honza Horak <hhorak@redhat.com> - 2.0.35-24
- Fix build on aarch64

* Mon Mar 25 2013 Honza Horak <hhorak@redhat.com> - 2.0.35-23
- Fix issues found by Coverity

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.0.35-21
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.0.35-20
- rebuild against new libjpeg

* Tue Aug 28 2012 Honza Horak <hhorak@redhat.com> - 2.0.35-19
- Spec file cleanup
- Compile and run test suite during build
- Using chrpath to get rid of --rpath in gd-progs

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Honza Horak <hhorak@redhat.com> - 2.0.35-17
- fixed CVE-2009-3546 gd: insufficient input validation in _gdGetColors()
  Resolves: #830745

* Tue Feb 28 2012 Honza Horak <hhorak@redhat.com> - 2.0.35-16
- Fixed AALineThick.patch to display vertical lines correctly
  Resolves: #798255

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> 2.0.35-14
- Rebuild for libpng 1.5

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-13
- Rebuilt for glibc bug#747377

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  6 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.35-11
- more spec file fixes

* Wed Jan  6 2010 Jiri Moskovcak <jmoskovc@redhat.com> - 2.0.35-10
- spec file fixes based on merge review

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.35-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan  6 2009 Ivana Varekova <varekova@redhat.com> - 2.0.35-7
- do minor spec file cleanup 

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.35-6
- fix license tag (nothing in this is GPL)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.35-5
- Autorebuild for GCC 4.3

* Tue Nov 20 2007 Ivana Varekova <varekova@redhat.com> 2.0.35-4
- remove static library

* Mon Nov 19 2007 Ivana Varekova <varekova@redhat.com> 2.0.35-3
- spec file cleanup

* Mon Nov 19 2007 Ivana Varekova <varekova@redhat.com> 2.0.35-2
- fix gdlib.pc file

* Tue Sep 18 2007 Ivana Varekova <varekova@redhat.com> 2.0.35-1
- update to 2.0.35

* Tue Sep  4 2007 Ivana Varekova <varekova@redhat.com> 2.0.34-3
- fix font paths (#225786#5)
- fix pkgconfig Libs flag (#225786#4)

* Thu Feb 22 2007 Ivana Varekova <varekova@redhat.com> 2.0.34-2
- incorporate package review feedback

* Thu Feb  8 2007 Ivana Varekova <varekova@redhat.com> 2.0.34-1
- update to 2.0.34

* Mon Jan 29 2007 Ivana Varekova <varekova@redhat.com> 2.0.33-12
- Resolves: #224610
  CVE-2007-0455 gd buffer overrun

* Tue Nov 21 2006 Ivana Varekova <varekova@redhat.com> 2.0.33-11
- Fix problem with to large box boundaries
  Resolves: #197747

* Thu Nov 16 2006 Ivana Varekova <varekova@redhat.com> 2.0.33-10
- added 'thick' - variable support for AA line (#198042)

* Tue Oct 31 2006 Adam Tkac <atkac@redhat.com> 2.0.33-9.4
- patched some additionals overflows in gd (#175414)

* Wed Sep 13 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 2.0.33 - 9.3
- gd-devel now requires fontconfig-devel (#205834)

* Wed Jul 19 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 2.0.33 - 9.2
- use CFLAGS on sparc64 (#199363)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.33 - 9.1
- rebuild

* Mon Jul 10 2006 Jitka Kudrnacova <jkudrnac@redhat.com> 2.0.33-9
- prevent from an infinite loop when decoding bad GIF images (#194520)
 
* Thu May 25 2006 Ivana Varekova <varekova@redhat.com> - 2.0.33-7
- fix multilib problem (add pkgconfig)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.33-6.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.33-6.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 20 2006 Phil Knirsch <pknirsch@redhat.com> 2.0.33-6
- Included a few more overflow checks (#177907)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 02 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.33-5
- Switched BuildPreReqs and Requires to modular xorg-x11 style

* Mon Oct 10 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.33-4
- Fixed possible gd crash when drawing AA line near image borders (#167843)

* Wed Sep 07 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.33-3
- Fixed broken freetype-config --libs flags in configure (#165875)

* Sun Apr 17 2005 Warren Togami <wtogami@redhat.com> 2.0.33-2
- devel reqs (#155183 thias)

* Tue Mar 22 2005 Than Ngo <than@redhat.com> 2.0.33-1
- 2.0.33 #150717
- apply the patch from Jose Pedro Oliveira
  - Added the release macro to the subpackages requirements versioning
  - Handled the gdlib-config movement to gd-devel in a differment manner
  - Added fontconfig-devel to the build requirements
  - Added xorg-x11-devel to the build requirements (Xpm)
  - Removed explicit /sbin/ldconfig requirement (gd rpm)
  - Removed explicit perl requirement (gd-progs rpm)
  - Added several missing documentation files (including the license file)
  - Replaced %%makeinstall by make install DESTDIR=...

* Thu Mar 10 2005 Than Ngo <than@redhat.com> 2.0.32-3
- move gdlib-config in devel

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 2.0.32-2
- bump release and rebuild with gcc 4

* Wed Nov 03 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.32-1
- Update to 2.0.32 which includes all the security fixes

* Wed Oct 27 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.28-2
- Fixed several buffer overflows for gdMalloc() calls

* Tue Jul 27 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.28-1
- Update to 2.0.28

* Fri Jul 02 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.27-1
- Updated to 2.0.27 due to:
  o Potential memory overruns in gdImageFilledPolygon. Thanks to John Ellson.
  o The sign of Y-axis values returned in the bounding box by gdImageStringFT
    was incorrect. Thanks to John Ellson and Riccardo Cohen.

* Wed Jun 30 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.26-1
- Update to 2.0.26

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 21 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.21-3
- Disable rpath usage.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 02 2004 Phil Knirsch <pknirsch@redhat.com> 2.0.21-1
- Updated to 2.0.21

* Tue Aug 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.0.15

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 06 2003 Phil Knirsch <pknirsch@redhat.com> 2.0.12-1
- Update to 2.0.12

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.8.4-11
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.8.4-10
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 24 2002 Phil Knirsch <pknirsch@redhat.com>
- Specfile update to add URL for homepage (#54608)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Oct 31 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.8.4-5
- Rebuild with current libpng

* Mon Aug 13 2001 Philipp Knirsch <pknirsch@redhat.de> 1.8.4-4
- Fixed a wrong double ownership of libgd.so (#51599).

* Fri Jul 20 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.8.4-3
- There's really no reason to link against both freetype 1.x and 2.x,
  especially when gd is configured to use just freetype 2.x. ;)

* Mon Jun 25 2001 Philipp Knirsch <pknirsch@redhat.de>
- Forgot to include the freetype library in the shared library linking. Fixed.

* Thu Jun 21 2001 Philipp Knirsch <pknirsch@redhat.de>
- Update to 1.8.4

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- Updates the descriptions to get rid of al references to gif

* Tue Dec 12 2000 Philipp Knirsch <Philipp.Knirsch@redhat.de>
- Fixed bug #22001 where during installation the .so.1 and the so.1.8 links
  didn't get installed and therefore updates had problems.

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- define HAVE_LIBTTF to actually enable ttf support (oops, #18299)
- remove explicit dependencies on libpng, libjpeg, et. al.
- add BuildPrereq: freetype-devel

* Wed Aug  2 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new libpng

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add %%postun run of ldconfig (#14915)

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com> 
- update to 1.8.3

* Sun Jun  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Mon May 22 2000 Nalin Dahyabhai <nalin@redhat.com> 
- break out a -progs subpackage
- disable freetype support

* Fri May 19 2000 Nalin Dahyabhai <nalin@redhat.com> 
- update to latest version (1.8.2)
- disable xpm support

* Thu Feb 03 2000 Nalin Dahyabhai <nalin@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- buiuld for glibc 2.1

* Fri Sep 11 1998 Cristian Gafton <gafton@redhat.com>
- built for 5.2
