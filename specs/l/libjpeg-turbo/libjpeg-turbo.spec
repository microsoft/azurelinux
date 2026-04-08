# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libjpeg-turbo
Version:        3.1.2
Release:        2%{?dist}
Summary:        A MMX/SSE2/SIMD accelerated library for manipulating JPEG image files
License:        Zlib AND BSD-3-Clause AND MIT AND IJG
URL:            https://github.com/%{name}/%{name}

Source0:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:         libjpeg-turbo-cmake.patch

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  libtool
BuildRequires:  nasm

Obsoletes:      libjpeg < 6b-47
# add provides (even if it not needed) to workaround bad packages, like
# java-1.6.0-openjdk (#rh607554) -- atkac
Provides:       libjpeg = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:       libjpeg%{_isa} = 6b-47%{?dist}
%endif

%description
The libjpeg-turbo package contains a library of functions for manipulating JPEG
images.

%package devel
Summary:        Headers for the libjpeg-turbo library
Obsoletes:      libjpeg-devel < 6b-47
Provides:       libjpeg-devel = 6b-47%{?dist}
%if "%{?_isa}" != ""
Provides:       libjpeg-devel%{_isa} = 6b-47%{?dist}
%endif
Requires:       libjpeg-turbo%{?_isa} = %{version}-%{release}
Obsoletes:      libjpeg-turbo-static < 1.3.1
Provides:       libjpeg-turbo-static = 1.3.1%{?dist}

%description devel
This package contains header files necessary for developing programs which will
manipulate JPEG files using the libjpeg-turbo library.

%package utils
Summary:        Utilities for manipulating JPEG images
Requires:       libjpeg-turbo%{?_isa} = %{version}-%{release}

%description utils
The libjpeg-turbo-utils package contains simple client programs for accessing
the libjpeg functions. It contains cjpeg, djpeg, jpegtran, rdjpgcom and
wrjpgcom. Cjpeg compresses an image file into JPEG format. Djpeg decompresses a
JPEG file into a regular image file. Jpegtran can perform various useful
transformations on JPEG files. Rdjpgcom displays any text comments included in a
JPEG file. Wrjpgcom inserts text comments into a JPEG file.

%package -n turbojpeg
Summary:        TurboJPEG library

%description -n turbojpeg
The turbojpeg package contains the TurboJPEG shared library.

%package -n turbojpeg-devel
Summary:        Headers for the TurboJPEG library
Requires:       turbojpeg%{?_isa} = %{version}-%{release}

%description -n turbojpeg-devel
This package contains header files necessary for developing programs which will
manipulate JPEG files using the TurboJPEG library.

%prep
%autosetup -p1 -S gendiff

#rm -rf doc

%build
# NASM object files are missing GNU Property note for Intel CET,
# force it on the resulting library
%ifarch %{ix86} x86_64
export LDFLAGS="$RPM_LD_FLAGS -Wl,-z,ibt -Wl,-z,shstk"
%endif

%{cmake} -DCMAKE_SKIP_RPATH:BOOL=YES \
         -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
%ifarch s390x riscv64
         -DFLOATTEST:STRING="fp-contract" \
%endif
         -DENABLE_STATIC:BOOL=NO

%cmake_build

%install
%cmake_install
find %{buildroot} -name "*.la" -delete

# Remove tjbench
rm -f %{buildroot}/%{_bindir}/tjbench

# Fix perms
chmod -x README.md

# multilib header hack
# we only apply this to known Red Hat multilib arches, per bug #1264675
case `uname -i` in
  i386 | ppc | s390 | sparc )
    wordsize="32"
    ;;
  x86_64 | ppc64 | s390x | sparc64 )
    wordsize="64"
    ;;
  *)
    wordsize=""
    ;;
esac

if test -n "$wordsize"
then
  mv $RPM_BUILD_ROOT%{_includedir}/jconfig.h \
     $RPM_BUILD_ROOT%{_includedir}/jconfig-$wordsize.h

  cat >$RPM_BUILD_ROOT%{_includedir}/jconfig.h <<EOF
#ifndef JCONFIG_H_MULTILIB
#define JCONFIG_H_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "jconfig-32.h"
#elif __WORDSIZE == 64
# include "jconfig-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

fi

%check
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
%ctest

%ldconfig_scriptlets
%ldconfig_scriptlets -n turbojpeg

%files
%license LICENSE.md
%doc README.md README.ijg ChangeLog.md
%{_libdir}/libjpeg.so.62*

%files devel
%doc doc/coderules.txt src/jconfig.txt doc/libjpeg.txt doc/structure.txt
%{_includedir}/jconfig*.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpegint.h
%{_includedir}/jpeglib.h
%{_libdir}/libjpeg.so
%{_libdir}/pkgconfig/libjpeg.pc
%{_libdir}/cmake/%{name}/%{name}*.cmake

%files utils
%doc doc/usage.txt doc/wizard.txt
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/rdjpgcom
%{_bindir}/wrjpgcom
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*

%files -n turbojpeg
%license LICENSE.md
%doc README.md README.ijg ChangeLog.md
%{_libdir}/libturbojpeg.so.0*

%files -n turbojpeg-devel
%{_includedir}/turbojpeg.h
%{_libdir}/libturbojpeg.so
%{_libdir}/pkgconfig/libturbojpeg.pc

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Sep 03 2025 Michal Hlavinka <mhlavink@redhat.com> - 3.1.2-1
- updated to 3.1.2 (#2392934)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Michal Hlavinka <mhlavink@redhat.com> - 3.1.1-1
- updated to 3.1.1 (#2367400)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 17 2024 Michal Hlavinka <mhlavink@redhat.com> - 3.1.0-1
- updated to 3.1.0 (#2332214)

* Wed Sep 18 2024 Michal Hlavinka <mhlavink@redhat.com> - 3.0.4-1
- updated to 3.0.4 (#2312472)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 06 2024 David Abdurachmanov <davidlt@rivosinc.com> - 3.0.2-2
- Set fp-contract for riscv64

* Mon Feb 05 2024 Frantisek Zatloukal <fzatlouk@redhat.com> - 3.0.2-1
- New upstream release 3.0.2 (Fixes RHBZ#2256228 and RHBZ#2166459 and RHBZ#2208448)

* Mon Jan 29 2024 Matej Mužila <mmuzila@redhat.com> - 2.1.4-6
- migrated to SPDX license

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 15 2022 Nikola Forró <nforro@redhat.com> - 2.1.4-1
- New upstream release 2.1.4 (#2118023)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Feb 27 2022 Nikola Forró <nforro@redhat.com> - 2.1.3-1
- New upstream release 2.1.3 (#2058898)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Matej Mužila <mmuzila@redhat.com> - 2.1.2-1
- New upstream release 2.1.2 (#2025141)

* Wed Aug 11 2021 Nikola Forró <nforro@redhat.com> - 2.1.1-1
- New upstream release 2.1.1 (#1991844)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 26 2021 Nikola Forró <nforro@redhat.com> - 2.1.0-1
- New upstream release 2.1.0 (#1953074)

* Thu Mar 25 2021 Nikola Forró <nforro@redhat.com> - 2.0.90-2
- Fix CVE-2021-20205 (#1937387)

* Thu Jan 28 2021 Nikola Forró <nforro@redhat.com> - 2.0.90-1
- New upstream release 2.0.90 (#1898427)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 04 2020 Nikola Forró <nforro@redhat.com> - 2.0.5-5
- Fix FTBFS (#1864007)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.0.5-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jul 03 2020 Nikola Forró <nforro@redhat.com> - 2.0.5-1
- New upstream release 2.0.5 (#1850293)

* Tue Jun 16 2020 Nikola Forró <nforro@redhat.com> - 2.0.4-3
- Fix CVE-2020-13790 (#1847159)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Nikola Forró <nforro@redhat.com> - 2.0.4-1
- New upstream release 2.0.4 (#1787793)

* Thu Sep 05 2019 Nikola Forró <nforro@redhat.com> - 2.0.3-1
- New upstream release 2.0.3 (#1749130)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Nikola Forró <nforro@redhat.com> - 2.0.2-3
- Fix LDFLAGS

* Mon Apr 29 2019 Nikola Forró <nforro@redhat.com> - 2.0.2-2
- Support running with Intel CET

* Wed Feb 27 2019 Nikola Forró <nforro@redhat.com> - 2.0.2-1
- New upstream release 2.0.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Nikola Forró <nforro@redhat.com> - 2.0.0-3
- Fix CVE-2018-19664 (#1656219)

* Fri Jan 11 2019 Nikola Forró <nforro@redhat.com> - 2.0.0-2
- Fix CVE-2018-20330 (#1665224)

* Mon Jul 30 2018 Nikola Forró <nforro@redhat.com> - 2.0.0-1
- New upstream release 2.0.0 (#1609439)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Nikola Forró <nforro@redhat.com> - 1.5.90-3
- Fix CVE-2018-1152 (#1593555)

* Fri Jun 15 2018 Nikola Forró <nforro@redhat.com> - 1.5.90-2
- Fix CVE-2018-11813 (#1588804)

* Wed Mar 28 2018 Nikola Forró <nforro@redhat.com> - 1.5.90-1
- New upstream release 1.5.90 (#1560219)

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 1.5.3-4
- Add missing gcc build dependency

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.5.3-2
- Switch to %%ldconfig_scriptlets

* Tue Dec 19 2017 Nikola Forró <nforro@redhat.com> - 1.5.3-1
- New upstream release 1.5.3 (#1468783)

* Tue Dec 19 2017 Nikola Forró <nforro@redhat.com> - 1.5.1-5
- re-enable check on ppc64(le)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 Karsten Hopp <karsten@redhat.com> - 1.5.1-2
- disable check on ppc64(le)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 06 2016 Petr Hracek <phracek@redhat.com> - 1.5.1-1
- New upstream relelase 1.5.1 (#1377903)

* Wed Sep 21 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.0-4
- Add upstream aarch64 NEON fix, re-enable SIMD on aarch64

* Mon Sep 19 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.0-3
- Temporarily disable SIMD on aarch64 until upstream #97 is fixed
- Add NEON fix for ARMv7

* Tue Sep 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.0-2
- Add upstream fix to fix SIMD crash on aarch64 (rhbz #1368569)

* Tue Jun 21 2016 Petr Hracek <phracek@redhat.com> - 1.5.0-1
- New upstream release 1.5.0 (#1343786)

* Thu Mar 10 2016 Petr Hracek <phracek@redhat.com> - 1.4.90-1
- New upstream release 1.4.90 (#1313111)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 07 2015 Petr Hracek <phracek@redhat.com> - 1.4.2-2
- Fix problem with multilibs like jconfig.h (#1264675)

* Wed Oct 07 2015 Petr Hracek <phracek@redhat.com> - 1.4.2-1
- New upstream release 1.4.2 (#1265034)

* Tue Jun 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.1-1
- new upstream version 1.4.1
- nasm available on all arches
- run tests with SMP

* Tue Jan 20 2015 Petr Hracek <phracek@redhat.com> - 1.4.0-1
- new upstream version 1.4.0 (#1180442)

* Wed Nov 26 2014 Petr Hracek <phracek@redhat.com> - 1.3.90-3
- libjpeg-turbo no longer defined macros like JPP (#1164815)

* Wed Nov 19 2014 Petr Hracek <phracek@redhat.com> - 1.3.90-2
- Resolves #1161585 Add suport for secondary arches

* Mon Oct 27 2014 Petr Hracek <phracek@redhat.com> - 1.3.90-1
- new upstream version 1.3.90
Resolves #1135375

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 17 2014 Simone Caronni <negativo17@gmail.com> - 1.3.1-2
- Re-add libjpeg-devel requirements for broken packages since Fedora 13.

* Wed Apr 16 2014 Petr Hracek <phracek@redhat.com> - 1.3.1-1
- New upstream version
- Remove upstreamed patches, add missing jpegint.h
- Clean up SPEC file
- Disable --static subpackage
- Remove libjpeg obsolency, removed in Fedora 13

* Thu Dec 19 2013 Petr Hracek <phracek@redhat.com> - 1.3.0-2
- Apply fixes CVE-2013-6629, CVE-2013-6630 (#20131737)

* Thu Jul 25 2013 Petr Hracek <phracek@redhat.com> - 1.3.0-1
- new upstream version
- no soname bump change

* Tue Mar 26 2013 Adam Tkac <atkac redhat com> - 1.2.90-2
- rebuild for ARM64 support

* Fri Feb 08 2013 Adam Tkac <atkac redhat com> 1.2.90-1
- update to 1.2.90

* Mon Feb 04 2013 Adam Tkac <atkac redhat com> 1.2.90-0.1.20130204svn922
- update to 1.2.80 snapshot (#854695)
- run `make test` during build

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> 1.2.1-6
- build with jpeg6 API/ABI (jpeg8-ABI feature was dropped)

* Tue Dec 04 2012 Adam Tkac <atkac redhat com> 1.2.1-5
- change license to IJG (#877517)

* Wed Oct 24 2012 Adam Tkac <atkac redhat com> 1.2.1-4
- build with jpeg8 API/ABI (#854695)

* Thu Oct 18 2012 Adam Tkac <atkac redhat com> 1.2.1-3
- minor provides tuning (#863231)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Adam Tkac <atkac redhat com> 1.2.1-1
- update to 1.2.1

* Thu Mar 08 2012 Adam Tkac <atkac redhat com> 1.2.0-1
- update to 1.2.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 21 2011 Orion Poplawski <orion cora nwra com> 1.1.1-3
- Make turobojpeg-devel depend on turbojpeg

* Fri Oct 7 2011 Orion Poplawski <orion cora nwra com> 1.1.1-2
- Ship the turbojpeg library (#744258)

* Mon Jul 11 2011 Adam Tkac <atkac redhat com> 1.1.1-1
- update to 1.1.1
  - ljt11-rh688712.patch merged

* Tue Mar 22 2011 Adam Tkac <atkac redhat com> 1.1.0-2
- handle broken JPEGs better (#688712)

* Tue Mar 01 2011 Adam Tkac <atkac redhat com> 1.1.0-1
- update to 1.1.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 17 2011 Adam Tkac <atkac redhat com> 1.0.90-1
- update to 1.0.90
- libjpeg-turbo10-rh639672.patch merged

* Fri Oct 29 2010 Adam Tkac <atkac redhat com> 1.0.1-3
- add support for arithmetic coded files into decoder (#639672)

* Wed Sep 29 2010 jkeating - 1.0.1-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Adam Tkac <atkac redhat com> 1.0.1-1
- update to 1.0.1
  - libjpeg-turbo10-rh617469.patch merged
- add -static subpkg (#632859)

* Wed Aug 04 2010 Adam Tkac <atkac redhat com> 1.0.0-3
- fix huffman decoder to handle broken JPEGs well (#617469)

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-2
- add libjpeg-devel%%{_isa} provides to -devel subpkg to satisfy imlib-devel
  deps

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 1.0.0-1
- update to 1.0.0
- patches merged
  - libjpeg-turbo-programs.patch
  - libjpeg-turbo-nosimd.patch
- add libjpeg provides to the main package to workaround problems with broken
  java-1.6.0-openjdk package

* Fri Jul 02 2010 Adam Tkac <atkac redhat com> 0.0.93-13
- remove libjpeg provides from -utils subpkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-12
- move Obsoletes: libjpeg to main pkg

* Wed Jun 30 2010 Rex Dieter <rdieter@fedoraproject.org> 0.0.93-11
- -utils: Requires: %%name ...

* Wed Jun 30 2010 Adam Tkac <atkac redhat com> 0.0.93-10
- add Provides = libjpeg to -utils subpackage

* Mon Jun 28 2010 Adam Tkac <atkac redhat com> 0.0.93-9
- merge review related fixes (#600243)

* Wed Jun 16 2010 Adam Tkac <atkac redhat com> 0.0.93-8
- merge review related fixes (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-7
- obsolete -static libjpeg subpackage (#600243)

* Mon Jun 14 2010 Adam Tkac <atkac redhat com> 0.0.93-6
- improve package description a little (#600243)
- include example.c as %%doc in the -devel subpackage

* Fri Jun 11 2010 Adam Tkac <atkac redhat com> 0.0.93-5
- don't use "fc12" disttag in obsoletes/provides (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-4
- fix compilation on platforms without MMX/SSE (#600243)

* Thu Jun 10 2010 Adam Tkac <atkac redhat com> 0.0.93-3
- package review related fixes (#600243)

* Wed Jun 09 2010 Adam Tkac <atkac redhat com> 0.0.93-2
- package review related fixes (#600243)

* Fri Jun 04 2010 Adam Tkac <atkac redhat com> 0.0.93-1
- initial package
