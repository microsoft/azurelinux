# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Garbage collector for C and C++
Name:    gc
Version: 8.2.6
Release: 5%{?dist}

# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD
URL:     https://www.hboehm.info/gc/
Source0: https://github.com/ivmai/bdwgc/releases/download/v%{version}/gc-%{version}%{?pre}.tar.gz

## upstreamable patches

## downstream patches

BuildRequires: automake libtool
BuildRequires: gcc-c++
## https://www.hboehm.info/gc/ says: "Starting with 8.0, libatomic_ops is only required if the compiler does not understand C atomics."
#BuildRequires: pkgconfig(atomic_ops) >= 7.4
BuildRequires: pkgconfig
BuildRequires: make

# rpmforge compatibility
Obsoletes: libgc < %{version}-%{release}
Provides:  libgc = %{version}-%{release}

%description
The Boehm-Demers-Weiser conservative garbage collector can be
used as a garbage collecting replacement for C malloc or C++ new.

%package devel
Summary: Libraries and header files for %{name} development
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: libgc-devel < %{version}-%{release}
Provides:  libgc-devel = %{version}-%{release}
%description devel
%{summary}.


%prep
%autosetup -n gc-%{version}%{?pre} -p1


%build
# refresh auto*/libtool to purge rpaths
rm -f libtool libtool.m4
autoreconf -i -f

# see https://bugzilla.redhat.com/689877
CPPFLAGS="-DUSE_GET_STACKBASE_FOR_MAIN $CPPFLAGS"
# https://github.com/ivmai/bdwgc/commit/3ea130ae326d02e224921017d3ee9c287fd4e670
# WAS https://bugzilla.redhat.com/show_bug.cgi?id=1551671
CPPFLAGS="-DDONT_UNDEF_EXCEPTIONS $CPPFLAGS"
export CPPFLAGS

%configure \
  --disable-docs \
  --enable-cplusplus \
  --enable-large-config \
  --enable-threads=posix

%make_build


%install
%make_install

install -p -D -m644 doc/gc.man  %{buildroot}%{_mandir}/man3/gc.3

## Unpackaged files
rm -rfv %{buildroot}%{_datadir}/gc/
rm -fv  %{buildroot}%{_libdir}/lib*.la


%check
%ifarch %{arm}
## cordtest segfaults
%global arch_ignore ||:
%endif
## cordtest segfaults or hangs on ix86
## gctest sometimes(?) hangs on armv7hl, aarch64, ppc64le
%ifnarch %{arm} aarch64 %{ix86} ppc64le
make check %{?arch_ignore}
%endif


%ldconfig_scriptlets

%files
%{_libdir}/libcord.so.1*
%{_libdir}/libgc.so.1*
%{_libdir}/libgccpp.so.1*
%{_libdir}/libgctba.so.1*

%files devel
%doc doc/README.environment doc/README.linux
%doc doc/*.md
%{_includedir}/gc.h
%{_includedir}/gc_cpp.h
%{_includedir}/gc/
%{_libdir}/libcord.so
%{_libdir}/libgc.so
%{_libdir}/libgccpp.so
%{_libdir}/libgctba.so
%{_libdir}/pkgconfig/bdw-gc.pc
%{_mandir}/man3/gc.3*


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 8.2.6-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar 08 2024 Jens Petersen <petersen@redhat.com> - 8.2.6-1
- update to https://github.com/ivmai/bdwgc/releases/tag/v8.2.6 release

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Timm Bäder <tbaeder@redhat.com> - 8.2.2-2
- Fix undefined pthread_setname_np
- https://fedoraproject.org/wiki/Toolchain/PortingToModernC

* Tue Sep 20 2022 Rex Dieter <rdieter@fedoraproject.org> 8.2.2-1
- 8.2.2 (#2124760)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Alexandra Hájková <ahajkova@redhat.com> - 8.0.6-3
- backport upstream "Do not probe to find main data root start if
  dl_iterate_phdr exists"
- https://bugzilla.redhat.com/show_bug.cgi?id=2063942

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 7 2021 Ivan Maidanski <ivmai@mail.ru> - 8.0.6-1
- 8.0.6
- Source0: Switch URL to Github releases
- %%build: remove --disable-static (default one since 8.0.0)
- %%build: remove --enable-parallel-mark (default one since 8.0.0)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Rex Dieter <rdieter@fedoraproject.org> - 8.0.4-2
- drop libatomic_ops dep

* Wed Jan 15 2020 Rex Dieter <rdieter@fedoraproject.org> - 8.0.4-1
- 8.0.4
- %%build: --with-libatomic-ops=yes

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 14 2018 Rex Dieter <rdieter@fedoraproject.org> - 7.6.4-3
- gc: Effectively overrides -fexceptions flag  (#1551671)
- move autoreconf to %%build

* Tue Feb 27 2018 Richard W.M. Jones <rjones@redhat.com> - 7.6.4-2
- Add upstream patches for RISC-V support.

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 7.6.4-1
- 7.6.4, reverts abi bump, compat-gc no longer needed

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 7.6.2-4
- BR: gcc-c++
- add (temporary) compat-gc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7.6.2-2
- Switch to %%ldconfig_scriptlets

* Thu Jan 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 7.6.2-1
- 7.6.2 (#1531008)
- libgc soname bump
- -devel: include all docs here (ie, remove README's from main too)

* Fri Dec 29 2017 Rex Dieter <rdieter@fedoraproject.org> - 7.6.0-8
- rebuild (libatomic_ops)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 03 2017 Petr Šabata <contyk@redhat.com> - 7.6.0-5
- Turns out our tests hang on armv7hl too, let's skip them (#1431866)

* Wed Mar 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 7.6.0-4
- skip tests on ppcle64 (#1431866)

* Tue Mar 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 7.6.0-3
- skip tests on aarch64 (#1431866)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 7.6.0-1
- gc-7.6.0 (#1365135)

* Fri Jun 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 7.4.4-1
- gc-7.4.4 (#1346538)

* Sat Feb 27 2016 Dan Horák <dan[at]danny.cz> - 7.4.2-6
- install also cord_pos.h

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7.4.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Rex Dieter <rdieter@fedoraproject.org> 7.4.2-1
- gc-7.4.2

* Wed Jun 11 2014 Pavel Raiskup <praiskup@redhat.com> - 7.4.0-4
- backport upstream fix for disclaim_test fail on ppc (#1101996)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Pavel Raiskup <praiskup@redhat.com> - 7.4.0-2
- ignore test results on ppc-like arches for now (#1101996)

* Tue May 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.4.0-1
- gc-7.4.0

* Mon May 12 2014 Rex Dieter <rdieter@fedoraproject.org> 7.2e-3
- 'make check' non-fatal on ppc64le too (#1096574)

* Fri Feb 21 2014 Rex Dieter <rdieter@fedoraproject.org> 7.2e-2
- update Urls to match upstream project move

* Fri Nov 15 2013 Rex Dieter <rdieter@fedoraproject.org> 7.2e-1
- gc-7.2e (#892559)

* Wed Oct 30 2013 Pavel Raiskup <praiskup@redhat.com> - 7.2d-4
- add support for aarch64 (#969817)
- ignore testsuite results only for powerpc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2d-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 07 2013 Rex Dieter <rdieter@fedoraproject.org> 7.2d-1
- gc-7.2d

* Mon Oct 29 2012 Pavel Raiskup <praiskup@redhat.com> - 7.2c-5
- fix possible infinite loop in test suite (#871067)

* Mon Oct 29 2012 Pavel Raiskup <praiskup@redhat.com> - 7.2c-4
- trim lines, s/[tabs]/[spaces]/

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 24 2012 Rex Dieter <rdieter@fedoraproject.org> 7.2c-2
- rebuild

* Tue Jun 26 2012 Rex Dieter <rdieter@fedoraproject.org> 7.2c-1
- 7.2c

* Fri Jun 15 2012 Rex Dieter <rdieter@fedoraproject.org>
- 7.2b-2
- backport patches from gc-7_2-hotfix-2 branch in lieu of 7.2c release
- gc 7.2 final abi broken when changing several symbols to hidden (#825473)
- CVE-2012-2673 gc: malloc() and calloc() overflows (#828878)

* Wed May 30 2012 Rex Dieter <rdieter@fedoraproject.org> 7.2b-1
- gc-7.2b

* Mon May 14 2012 Rex Dieter <rdieter@fedoraproject.org>
- 7.2-1
- gc-7.2 (final)

* Fri Mar 02 2012 Rex Dieter <rdieter@fedoraproject.org> 7.2-0.7.alpha6
- libatomic_ops: use -DAO_USE_PTHREAD_DEFS on ARMv5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-0.6.alpha6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-0.5.alpha6
- Rebuilt for glibc bug#747377

* Mon Jun 20 2011 Rex Dieter <rdieter@fedoraproject.rog> 7.2-0.4.alpha6.20110107
- gc-7.2alpha6
- build with -DUSE_GET_STACKBASE_FOR_MAIN (#689877)

* Wed Feb 09 2011 Rex Dieter <rdieter@fedoraproject.org> 7.2-0.3.alpha5.20110107
- bdwgc-7.2alpha4 20110107 snapshot

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2-0.2.alpha4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 7.2-0.1.alpha4
- gc-7.2alpha4
- use/package internal libatomic_ops

* Tue Dec  8 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 7.1-10
- Explicitly BR libatomic_ops-static in accordance with the Packaging
  Guidelines (libatomic_ops-devel is still static-only).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 19 2009 Rex Dieter <rdieter@fedoraproject.org. - 7.1-8
- FTBFS gc-7.1-7.fc11 (#511365)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-6
- rebuild for pkgconfig deps

* Wed Oct 15 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-5
- forward-port patches (gcinit, sparc)

* Fri Oct 03 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-4
- BR: libatomic_ops-devel

* Mon Sep 08 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-3
- upstream DONT_ADD_BYTE_AT_END patch
- spec cosmetics

* Sat Jul 12 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-2
- --enable-large-config (#453972)

* Sun May 04 2008 Rex Dieter <rdieter@fedoraproject.org> 7.1-1
- gc-7.1
- purge rpaths

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 7.0-7
- respin (gcc43)

* Wed Aug 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-6
- BR: gawk
- fixup compat_header patch to avoid needing auto* tools

* Wed Aug 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-5
- compat_header patch (supercedes previous pkgconfig patch)

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-4
- pkgconfig patch (cflags += -I%%_includedir/gc)

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-3
- respin (ppc32)

* Tue Jul 24 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-2
- gcinit patch, ABI compatibility (#248700)

* Mon Jul 09 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 7.0-1
- gc-7.0

* Mon Dec 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-3
- Obsoletes/Provides: libgc(-devel) (rpmforge compatibility)

* Mon Aug 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-2
- fc6 respin

* Thu Jul 13 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.8-1
- 6.8

* Fri Mar 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.7-1
- 6.7

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-5
- gcc(4.1) patch

* Thu Dec 01 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-4
- Provides: libgc(-devel)

* Wed Sep 14 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-3
- no-undefined patch, libtool madness (#166344)

* Mon Sep 12 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-2
- drop opendl patch (doesn't appear to be needed anymore)

* Fri Sep 09 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.6-1
- 6.6

* Wed May 25 2005 Rex Dieter <rexdieter[AT]users.sf.net> 6.5-1
- 6.5

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jan 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:6.4-2
- --enable-threads unconditionally
- --enable-parallel-mark only on %%ix86 (#144681)

* Mon Jan 10 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:6.4-1
- 6.4
- update opendl patch

* Fri Jul 09 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.1
- 6.3(final)

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.4.alpha6
- dlopen patch

* Wed May 26 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.3.alpha6
- explictly --enable-threads ('n friends)

* Tue May 25 2004 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.2.alpha6
- 6.3alpha6
- --disable-static
- --enable-parallel-mark

* Wed Dec 17 2003 Rex Dieter <rexdieter at sf.net> 0:6.3-0.fdr.0.1.alpha2
- 6.3alpha2

* Thu Oct 02 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.3
- OK, put manpage in man3.

* Thu Oct 02 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.2
- drop manpage pending feedback from developer.

* Tue Sep 30 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.1
- fix manpage location
- remove .la file (it appears unnecessary after all, thanks to opendl patch)
- remove cvs tag from description
- touchup -devel desc/summary.
- macro update to support Fedora Core

* Thu Sep 11 2003 Rex Dieter <rexdieter at sf.net> 0:6.2-0.fdr.0
- 6.2 release.
- update license (BSD)
- Consider building with: --enable-parallel-mark
  (for now, no).
