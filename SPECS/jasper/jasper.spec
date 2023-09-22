Summary:        Implementation of the JPEG-2000 standard, Part 1
Name:           jasper
Version:        2.0.32
Release:        3%{?dist}
License:        JasPer
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.ece.uvic.ca/~frodo/jasper/
Source0:        https://github.com/jasper-software/jasper/archive/version-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# skip hard-coded prefix/lib rpath
Patch2:         jasper-2.0.14-rpath.patch
# architecture related patches
Patch100:       jasper-2.0.2-test-ppc64-disable.patch
Patch101:       jasper-2.0.2-test-ppc64le-disable.patch
# autoreconf
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libGLU-devel
BuildRequires:  libXi-devel
BuildRequires:  libXmu-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  make
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
This package contains an implementation of the image compression
standard JPEG-2000, Part 1. It consists of tools for conversion to and
from the JP2 and JPC formats.

%package devel
Summary:        Header files, libraries and developer documentation
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       libjpeg-turbo-devel
Requires:       pkgconfig
Provides:       libjasper-devel = %{version}-%{release}

%description devel
%{summary}.

%package libs
Summary:        Runtime libraries for %{name}
Conflicts:      jasper < 1.900.1-4

%description libs
%{summary}.

%package utils
Summary:        Nonessential utilities for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description utils
%{summary}, including jiv and tmrdemo.

%prep
%setup -q -n %{name}-version-%{version}

%patch2 -p1 -b .rpath
# Need to disable one test to be able to build it on ppc64 arch
# At ppc64 this test just stuck (nothing happend - no exception or error)
# %patch3 -p1 -b .freeglut

%if "%{_arch}" == "ppc64"
%patch100 -p1 -b .test-ppc64-disable
%endif

# Need to disable two tests to be able to build it on ppc64le arch
# At ppc64le this tests just stuck (nothing happend - no exception or error)

%if "%{_arch}" == "ppc64le"
%patch101 -p1 -b .test-ppc64le-disable
%endif

%build
mkdir builder
%cmake \
  -DJAS_ENABLE_DOC:BOOL=OFF \
  -B builder

%make_build -C builder

%install
make install/fast DESTDIR=%{buildroot} -C builder

# Unpackaged files
rm -f doc/README
find %{buildroot} -type f -name "*.la" -delete -print

%check
make test -C builder

%files
%{_bindir}/imgcmp
%{_bindir}/imginfo
%{_bindir}/jasper
%{_mandir}/man1/img*
%{_mandir}/man1/jasper.1*
%{_docdir}/JasPer/*

%files devel
%doc doc/*
%{_includedir}/jasper/
%{_libdir}/libjasper.so
%{_libdir}/pkgconfig/jasper.pc

%ldconfig_scriptlets libs

%files libs
%doc README
%license COPYRIGHT LICENSE
%{_libdir}/libjasper.so.4*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.0.32-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Jul 20 2021 Vinicius Jarina <vinja@microsoft.com> - 2.0.32-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified.

* Wed Jun 02 2021 Josef Ridky <jridky@redhat.com> - 2.0.32-1
- New upstream release 2.0.32 (#1950621)

* Tue Mar 30 2021 Josef Ridky <jridky@redhat.com> - 2.0.28-1
- New upstream release 2.0.28 (#1944481)

* Wed Mar 24 2021 Josef Ridky <jridky@redhat.com> - 2.0.27-1
- New upstream release 2.0.27 (#1940455)

* Tue Mar 16 2021 Josef Ridky <jridky@redhat.com> - 2.0.26-2
- Fix CVE-2021-3443 (#1939233)

* Wed Mar 10 2021 Josef Ridky <jridky@redhat.com> - 2.0.26-1
- New upstream release 2.0.26 (#1935900)

* Tue Feb 09 2021 Josef Ridky <jridky@redhat.com> - 2.0.25-1
- New upstream release 2.0.25 (#1925996)

* Thu Jan 28 2021 Josef Ridky <jridky@redhat.com> - 2.0.24-3
- fix CVE-2021-3272 (#1921328)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Josef Ridky <jridky@redhat.com> - 2.0.24-1
- New upstream release 2.0.24 (#1905690)

* Wed Oct 07 2020 Josef Ridky <jridky@redhat.com> - 2.0.22-1
- New upstream release 2.0.22 (#1876161)

* Thu Aug 27 2020 Than Ngo <than@redhat.com> - 2.0.17-3
- add correct version

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Josef Ridky <jridky@redhat.com> - 2.0.17-1
- new upstream release (2.0.17)
- change of source URL to GitHub of Jasper

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 17 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.0.16-1
- New version, rebuilt for new freeglut

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.0.14-7
- cleanup cmake usage, move to %%build
- %%build: explicitly disable doc generation
- kill hard-coded rpath
- -libs: explicit soname so bumps aren't a surprise
- use %%license, %%make_build, 'make install/fast'

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 30 2018 Josef Ridky <jridky@redhat.com> - 2.0.14-5
- Fix CVE-2016-9396 (#1396986)

* Thu Mar 08 2018 Josef Ridky <jridky@redhat.com> - 2.0.14-4
- Fix gcc dependency

* Mon Feb 26 2018 Josef Ridky <jridky@redhat.com> - 2.0.14-3
- Clean spec file
- Remove unused Group tag
- Add gcc requirement
- Use ldconfig scriptlet

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 15 2017 rebase-helper <rebase-helper@localhost.local> - 2.0.14-1
- New upstream release 2.0.14 (#1491888)

* Fri Aug 25 2017 Josef Ridky <jridky@redhat.com> - 2.0.12-4
- CVE-2017-1000050 jasper: NULL pointer exception in jp2_encode() (#1472888)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Mar 03 2017 Josef Ridky <jridky@redhat.com> - 2.0.12-1
- New upstream release 2.0.12 (#1428622)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Josef Ridky <jridky@redhat.com> - 2.0.10-1
- New upstream release 2.0.10 (#1403401)

* Thu Dec  1 2016 Josef Ridky <jridky@redhat.com> - 2.0.2-1
- New upstream release 2.0.2 (#1395929)
- CVE-2016-9262 jasper: Multiple overflow vulnerabilities leading to use after free (#1393883)
- CVE-2016-8654 jasper: Heap-based buffer overflow in QMFB code in JPC codec (#1399168)
- CVE-2016-9388 jasper: Reachable assertion in RAS encoder/decoder
- CVE-2016-9389 jasper: Improper equality testing of component domains via assertion
- CVE-2016-9390 jasper: Assertion failure when tiles lie outside of the image area
- CVE-2016-9391 jasper: reachable assertions in the JPC bitstream code
- CVE-2016-9392 jasper: Missing sanity checks on the date in SIZ marker segment
- CVE-2016-9393 jasper: Missing sanity checks on the date in SIZ marker segment
- CVE-2016-9394 jasper: Missing sanity checks on the data in a SIZ marker segment
- CVE-2016-9395 jasper: Assertion failure in jas_seq2d_create
- CVE-2016-9557 jasper: Signed integer overflow in jas_image.c
- CVE-2016-9560 jasper: Stack-based buffer overflow in jpc_tsfb.c
- Upgrade libjasper.so.1* to libjasper.so.4*

* Mon Oct 24 2016 Josef Ridky <jridky@redhat.com> - 1.900.13-1
- New upstream release 1.900.13 (#1385637)
- Release contains security fix for CVE-2016-8690, CVE-2016-8691, CVE-2016-8692, CVE-2016-8693 (#1385516)

* Thu Oct 13 2016 Josef Ridky <jridky@redhat.com> - 1.900.3-1
- New upstream release 1.900.3

* Tue Oct 11 2016 Josef Ridky <jridky@redhat.com> - 1.900.2-2
- CVE-2016-2089 - matrix rows_ NULL pointer dereference in jas_matrix_clip() (#1302636)

* Mon Oct 10 2016 Josef Ridky <jridky@redhat.com> - 1.900.2-1
- New upstream release 1.900.2 (#1382188)

* Thu Sep 15 2016 Dave Airlie <airlied@redhat.com> - 1.900.1-34
- patch 14 is an ABI break, this breaks gnome-software and steam
- this would require a new revision of the .so to fix properly
- as sizeof (int) != sizeof (size_t)

* Fri Aug 12 2016 Josef Ridky <jridky@redhat.com> - 1.900.1-33
- CVE-2015-5203 - double free in jasper_image_stop_load() (#1254244)
- CVE-2015-5221 - Use-after-free and double-free flaws (#1255714)
- CVE-2016-1867 - out-of-bounds read in the jpc_pi_nextcprl() function (#1298138)
- CVE-2016-1577 - double free vulnerability in jas_iccattrval_destroy (#1314468)
- CVE-2016-2116 - memory leak in jas_iccprof_createfrombuf causing 
		  memory consumption (#1314473)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.900.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 22 2015 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-30
- CVE-2014-8157 - dec->numtiles off-by-one check in jpc_dec_process_sot() (#1184750)
- CVE-2014-8158 - unrestricted stack memory use in jpc_qmfb.c (#1184750)

* Thu Dec 18 2014 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-29
- CVE-2014-8137 - double-free in jas_iccattrval_destroy() (oCERT-2014-012) (#1175761)
- CVE-2014-8138 - heap overflow in jp2_decode() (oCERT-2014-012) (#1175761)

* Thu Dec 04 2014 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-28
- CVE-2014-9029 - incorrect component number check in COC, RGN and QCC
                  marker segment decoders (#1170650)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 25 2013 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-24
- added --force option to autoreconf (#925604)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.900.1-22
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 06 2012 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-21
- build with -fno-strict-overflow

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 09 2011 Jiri Popelka <jpopelka@redhat.com> - 1.900.1-18
- CVE-2011-4516, CVE-2011-4517 jasper: heap buffer overflow flaws
  lead to arbitrary code execution (CERT VU#887409) (#765660)
- Fixed problems found by static analysis of code (#761440)
- spec file modernized

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-16
- rebuild

* Sun Feb 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-15
- FTBFS jasper-1.900.1-14.fc12: ImplicitDSOLinking (#564794)

* Thu Oct 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-14
- add pkgconfig support

* Tue Oct 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-13
- CVE-2008-3520 jasper: multiple integer overflows in jas_alloc calls (#461476)
- CVE-2008-3522 jasper: possible buffer overflow in 
  jas_stream_printf() (#461478)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.900.1-11
- FTBFS jasper-1.900.1-10.fc11 (#511743)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.900.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 25 2009 Rex Dieter <rdieter@fedoraproject.org> 1.900.1-9
- patch for "jpc_dec_tiledecode: Assertion `dec->numcomps == 3' failed)
  (#481284, #481291)

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.900.1-8
- respin (gcc43)

* Mon Oct 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-7
- -libs: %%post/%%postun -p /sbin/ldconfig

* Mon Sep 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-6
- -libs: -Requires: %%name
- -devel: +Provides: libjasper-devel
- drop (unused) geojasper bits

* Wed Aug 22 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-4
- -libs subpkg to be multilib friendlier
- -utils subpkg for non-essential binaries jiv, tmrdemo (#244153)

* Fri Aug 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-3
- License: JasPer

* Wed May 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-2
- CVE-2007-2721 (#240397)

* Thu Mar 29 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.900.1-1
- jasper-1.900.1

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.900.0-3
- omit deprecated memleak patch

* Fri Dec 08 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.900.0-2
- jasper-1.900.0 (#218947)

* Mon Sep 18 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-15
- memory leak (#207006)

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-13
- fc6 respin

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-12
- fixup build issues introduced by geojasper integration

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-10
- support/use geojasper (optional, default no)
- fc5: gcc/glibc respin

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Tue Jan 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-9
- workaround "freeglut-devel should Requires: libGL-devel, libGLU-devel"
  (#179464)

* Tue Jan 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-8
- revert jasper to jaspertool rename (#176773)
- actually use/apply GL patch

* Tue Oct 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-7
- GL patch to remove libGL dependancy (using only freeglut)

* Tue Oct 18 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-6
- token %%check section
- --enable-shared 

* Mon Oct 17 2005 Rex Dieter <rexdieter[AT]users.sf.net> 1.701.0-5
- use %%{?dist}
- BR: libGL-devel 

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Oct 23 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.3
- Capitalize summary
- remove 0-length ChangeLog

* Fri Jun 04 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.2
- nuke .la file
- BR: glut-devel -> freeglut-devel

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:1.701.0-0.fdr.1
- 1.701.0

* Tue Jun 01 2004 Rex Dieter <rexdieter at sf.net> 0:1.700.5-0.fdr.2
- avoid conflicts with fc'2 tomcat by renaming /usr/bin/jasper -> jaspertool

* Mon Mar 08 2004 Rex Dieter <rexdieter at sf.net> 0:1.700.5-0.fdr.1
- use Epochs.
- -devel: Requires: %%name = %%epoch:%%version

* Thu Jan 22 2004 Rex Dieter <rexdieter at sf.net> 1.700.5-0.fdr.0
- first try
