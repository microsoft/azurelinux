# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Important for %%{ix86}:
# This rpm has to be build on a CPU with sse2 support like Pentium 4 !
#

Summary: GNU arbitrary precision library
Name: gmp
Version: 6.3.0
Release: 5%{?dist}
Epoch: 1
URL: https://gmplib.org/
Source0: https://gmplib.org/download/gmp/gmp-%{version}.tar.xz
Source2: gmp.h
Source3: gmp-mparam.h
Patch2: gmp-6.0.0-debuginfo.patch
Patch3: gmp-intel-cet.patch
# https://gmplib.org/repo/gmp/rev/8e7bb4ae7a18
Patch4: gmp-6.3.0-c23.patch
# https://gmplib.org/list-archives/gmp-devel/2023-August/006198.html
# https://gmplib.org/repo/gmp/rev/372acfd0c33e
Patch5: gmp-6.3.0-s390x-popcount.patch

# * Main sources are dual licensed under LGPL-3.0-or-later and GPL-2.0-or-later
#   Either only one may be active or both simultaneously.
# * Some docs are under GFDL-1.3-invariants-or-later.
# * demos are under GPL-3.0-or-later but they are NOT shipped.
# * tests are under GPL-3.0-or-later but they are NOT shipped.
License: (LGPL-3.0-or-later OR GPL-2.0-or-later OR (LGPL-3.0-or-later AND GPL-2.0-or-later)) AND GFDL-1.3-invariants-or-later

BuildRequires: autoconf automake libtool
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: git
# Generate the .hmac checksum unless --without fips is used
%bcond_without fips
%if %{with fips}
BuildRequires: fipscheck
%endif
BuildRequires: make

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

%package c++
Summary: C++ bindings for the GNU MP arbitrary precision library
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description c++
Bindings for using the GNU MP arbitrary precision library in C++ applications.

%package devel
Summary: Development tools for the GNU MP arbitrary precision library
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: %{name}-c++%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
The libraries, header files and documentation for using the GNU MP 
arbitrary precision library in applications.

If you want to develop applications which will use the GNU MP library,
you'll need to install the gmp-devel package.  You'll also need to
install the gmp package.

%package static
Summary: Development tools for the GNU MP arbitrary precision library
Requires: %{name}-devel = %{epoch}:%{version}-%{release}

%description static
The static libraries for using the GNU MP arbitrary precision library 
in applications.

%prep
%autosetup -S git

%build
autoreconf -ifv
if as --help | grep -q execstack; then
  # the object files do not require an executable stack
  export CCAS="gcc -c -Wa,--noexecstack"
fi

%ifarch %{ix86}
  export CFLAGS=$(echo %{optflags} | sed -e "s/-mtune=[^ ]*//g" | sed -e "s/-march=[^ ]*/-march=i686/g")
  export CXXFLAGS=$(echo %{optflags} | sed -e "s/-mtune=[^ ]*//g" | sed -e "s/-march=[^ ]*/-march=i686/g")
%endif

# set baseline to z13
%ifarch s390x
  export MPN_PATH="s390_64/z13 s390_64 generic"
%endif

%configure --enable-cxx --enable-fat

sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -e 's|-lstdc++ -lm|-lstdc++|' \
    -i libtool
export LD_LIBRARY_PATH=`pwd`/.libs
%make_build

%if %{with fips}
%define __spec_install_post \
    %{?__debug_package:%{__debug_install_post}} \
    %{__arch_install_post} \
    %{__os_install_post} \
    fipshmac -d $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_libdir}/libgmp.so.10.* \
    file=`basename $RPM_BUILD_ROOT%{_libdir}/libgmp.so.10.*.hmac` && \
        mv $RPM_BUILD_ROOT%{_libdir}/$file $RPM_BUILD_ROOT%{_libdir}/.$file && \
        ln -s .$file $RPM_BUILD_ROOT%{_libdir}/.libgmp.so.10.hmac
%{nil}
%endif

%install
export LD_LIBRARY_PATH=`pwd`/.libs
%make_install 
install -m 644 gmp-mparam.h ${RPM_BUILD_ROOT}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/lib{gmp,mp,gmpxx}.la
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}
ln -sf libgmpxx.so.4 $RPM_BUILD_ROOT%{_libdir}/libgmpxx.so

# Rename gmp.h to gmp-<arch>.h and gmp-mparam.h to gmp-mparam-<arch>.h to 
# avoid file conflicts on multilib systems and install wrapper include files
# gmp.h and gmp-mparam-<arch>.h
basearch=%{_arch}
# always use i386 for iX86
%ifarch %{ix86}
basearch=i386
%endif
# Rename files and install wrappers

mv %{buildroot}/%{_includedir}/gmp.h %{buildroot}/%{_includedir}/gmp-${basearch}.h
install -m644 %{SOURCE2} %{buildroot}/%{_includedir}/gmp.h
mv %{buildroot}/%{_includedir}/gmp-mparam.h %{buildroot}/%{_includedir}/gmp-mparam-${basearch}.h
install -m644 %{SOURCE3} %{buildroot}/%{_includedir}/gmp-mparam.h


%check
export LD_LIBRARY_PATH=`pwd`/.libs
%make_build check

%ldconfig_scriptlets

%ldconfig_scriptlets c++

%files
%license COPYING COPYING.LESSERv3 COPYINGv2 COPYINGv3
%doc NEWS README
%{_libdir}/libgmp.so.*
%if %{with fips}
%{_libdir}/.libgmp.so.*.hmac
%endif

%files c++
%{_libdir}/libgmpxx.so.*

%files devel
%{_libdir}/libgmp.so
%{_libdir}/libgmpxx.so
%{_libdir}/pkgconfig/gmp.pc
%{_libdir}/pkgconfig/gmpxx.pc
%{_includedir}/*.h
%{_infodir}/gmp.info*

%files static
%{_libdir}/libgmp.a
%{_libdir}/libgmpxx.a

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 09 2024 Jakub Martisko <jamartis@redhat.com> - 1:6.3.0-1
- Rebase to gmp-6.3.0
- Refresh the cet patch

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 07 2023 Lukáš Zaoral <lzaoral@redhat.com> - 1:6.2.1-6
- migrate to SPDX license format

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 31 2021 Jakub Martisko <jamartis@redhat.com> - 1:6.2.1-1
- Rebase to gmp-6.2.1
- Minor update of the cet patch
Resolves: rhbz#1897831

* Tue Aug 31 2021 Jakub Martisko <jamartis@redhat.com> - 1:6.2.0-8
- Enable intel CET
- Fix based on the patches provided by H.J. Lu
Resolves: rhbz#1795709

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Kalev Lember <klember@redhat.com> - 1:6.2.0-5
- Move gmpxx.pc to -devel subpackage as well

* Fri Aug 07 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 1:6.2.0-4
- The pkgcfg file should be in devel

* Tue Jul 28 2020 Jakub Martisko <jamartis@redhat.com> - 1:6.2.0-3
- Use make macros

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 17 2020 Jakub Martisko <jamartis@redhat.com> - 1:6.2.0-1
- Rebase to 6.2.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Jakub Martisko <jamartis@redhat.com> - 1:6.1.2-12
- Reenable the fat binaries build option
Resolves: #1779060

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 15 2019 Anderson Toshiyuki Sasaki <ansasaki@redhat.com> - 1:6.1.2-10
- Create HMAC checksum for FIPS integrity self tests

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 13 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 1:6.1.2-4
- Fix the build process for ix89 family

* Fri Feb 17 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 1:6.1.2-3
- Build process updated to correctly build .debug_info for i386
  and to correctly use hardening flags

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 20 2016 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:6.1.2-1
- rebase

* Wed Jun 22 2016 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:6.1.1-1
- rebase

* Fri Apr 08 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1:6.1.0-3
- Split c++ subpackage (#1325439)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:6.1.0-1
- rebase to 6.1.0
- gmp-6.0.0-ppc64.patch already upstream, dropped

* Mon Sep 14 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:6.0.0-13
- do not package sse2 variant, use --enable-fat instead (a bit dangerous, some low level routines will be skipped in `make check`)

* Fri Sep 04 2015 Michal Toman <mtoman@fedoraproject.org> - 1:6.0.0-12
- Add support for MIPS architecture to gmp.h and gmp-mparam.h

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1:6.0.0-10
- Rebuilt for GCC 5 C++11 ABI change

* Thu Apr 02 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:6.0.0-9
- bug965318 - improve debuginfo of assembler sources

* Thu Sep 04 2014 Dan Horák <dan[at]danny.cz> - 1:6.0.0-8
- drop s390x patch, support is already in upstream

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 1:6.0.0-6
- fix license handling

* Thu Jul 10 2014 Brent Baude <baude@us.ibm.com> - 1:6.0.0-5
- Fix gmp headers for ppc64le (#1083429)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:6.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Karsten Hopp <karsten@redhat.com> 6.0.0-3
- set default for BMOD_1_TO_MOD_1_THRESHOLD on ppc64, patch by 
  Torbjorn Granlund:
  https://gmplib.org/repo/gmp/rev/4a6d258b467f

* Mon Apr 14 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:6.0.0-2
- rebase

* Wed Nov 06 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:5.1.3-2
- support for aarch64

* Wed Nov 06 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:5.1.3-1
- rebase to 5.1.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:5.1.2-1
- rebase to 5.1.2

* Thu Mar 28 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:5.1.1-3
- added build dependency needed to autoreconf on arm

* Thu Feb 14 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:5.1.1-2
- rebase to 5.1.1
- deleted unapplicable part of gmp-4.0.1-s390.patch

* Fri Jan 25 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:5.1.0-1
- rebase to 5.1.0, de-ansi patch no longer applicable
- upstream dropped libmp.so (bsdmp-like interface)
- silenced bogus date in changelog

* Tue Jan 22 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1:5.0.5-6
- Rebuild against new binutils to fix FTBFS on ARM

* Fri Nov 23 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1:5.0.5-5
- minor spec cleanup

* Fri Jul 20 2012 Peter Schiffer <pschiffe@redhat.com> 1:5.0.5-3
- fixed FTBFS

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Peter Schiffer <pschiffe@redhat.com> 1:5.0.5-1
- resolves: #820897
  update to 5.0.5

* Thu Apr 19 2012 Peter Schiffer <pschiffe@redhat.com> 1:5.0.4-1
- resolves: #785116
  update to 5.0.4

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.2-6
- Rebuilt for c++ ABI breakage

* Thu Jan 19 2012 Peter Schiffer <pschiffe@redhat.com> 1:5.0.2-5
- fixed FTBFS with gcc 4.7 on 32bit arch

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:5.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Peter Schiffer <pschiffe@redhat.com> 1:5.0.2-3
- removed old compatibility library

* Mon Sep 26 2011 Peter Schiffer <pschiffe@redhat.com> 1:5.0.2-2
- temporary build wild old compatibility library version

* Tue Sep 20 2011 Peter Schiffer <pschiffe@redhat.com> 1:5.0.2-1
- resolves: #702919
  update to 5.0.2
- resolves: #738091
  removed unused direct shlib dependency on libm
  updated license in gmp.h and gmp-mparam.h files

* Mon Jun 13 2011 Ivana Hutarova Varekova <varekova@redhat.com> 1:4.3.2-4
- Resolves: #706374
  fix sse2/libgmp.so.3.5.2 debuginfo data

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:4.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> 1:4.3.2-2
- fix Requires tag

* Wed Nov 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> 1:4.3.2-1
- downgrade from 5.0.1 to 4.3.2

* Mon May 24 2010 Ivana Hutarova Varekova <varekova@redhat.com> 5.0.1-1
- update to 5.0.1

* Tue Mar  2 2010 Ivana Hutarova Varekova <varekova@redhat.com> 4.3.1-7
- fix the license tag

* Fri Nov 27 2009 Ivana Hutarova Varekova <varekova@redhat.com> 4.3.1-6
- remove unnecessary dependences
  remove duplicated documentation

* Mon Aug 10 2009 Ivana Varekova <varekova@redhat.com> 4.3.1-5
- fix installation with --excludedocs option (#515947)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Ivana Varekova <varekova@redhat.com> 4.3.1-3
- rebuild

* Mon Jun 15 2009 Ivana Varekova <varekova@redhat.com> 4.3.1-2
- Resolves: #505592
  add RPM_OPT_FLAGS

* Thu May 28 2009 Ivana Varekova <varekova@redhat.com> 4.3.1-1
- update to 4.3.1
- remove configure macro (built problem)

* Thu Apr 09 2009 Dennis Gilmore <dennis@ausil.us> - 4.2.4-6
- no check that --host and --target are the same when building i586  or sparcv9 they are not

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 23 2008 Ivana Varekova <varekova@redhat.com> 4.2.4-4
- fix spec file

* Mon Dec  8 2008 Ivana Varekova <varekova@redhat.com> 4.2.4-3
- remove useless option (#475073)

* Wed Dec  3 2008 Stepan Kasal <skasal@redhat.com> 4.2.4-2
- Run full autoreconf, add automake to BuildRequires.

* Mon Nov 10 2008 Ivana Varekova <varekova@redhat.com> 4.2.4-1
- update to 4.2.4

* Fri Nov  7 2008 Ivana Varekova <varekova@redhat.com> 4.2.2-9
- remove useless patch (#470200)

* Thu Apr 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.2.2-8
- add sparc/sparc64 support

* Wed Mar 19 2008 Ivana Varekova <varekova@redhat.com> 4.2.2-7
- add superH support (#437688)

* Wed Feb 13 2008 Ivana varekova <varekova@redhat.com> 4.2.2-6
- fix gcc-4.3 problem - add <cstdio> (#432336)

* Fri Feb  8 2008 Ivana Varekova <varekova@redhat.com> 4.2.2-5
- split the devel subpackage to devel and static parts

* Thu Feb  7 2008 Ivana Varekova <varekova@redhat.com> 4.2.2-4
- change license tag

* Mon Sep 24 2007 Ivana Varekova <varekova@redhat.com> 4.2.2-3
- fix libgmpxx.so link

* Thu Sep 20 2007 Ivana Varekova <varekova@redhat.com> 4.2.2-2
- fix check tag

* Wed Sep 19 2007 Ivana Varekova <varekova@redhat.com> 4.2.2-1
- update to 4.2.2

* Mon Aug 20 2007 Ivana Varekova <varekova@redhat.com> 4.2.1-3
- spec file cleanup (#253439)

* Tue Aug  7 2007 Ivana Varekova <varekova@redhat.com> 4.2.1-2
- add arm support (#245456)
  thanks to Lennert Buytenhek

* Mon Aug  6 2007 Ivana Varekova <varekova@redhat.com> 4.2.1-1
- update to 4.2.1
- do some spec cleanups
- fix 238794 - gmp-devel depends on {version} but not on 
  {version}-{release}
- remove mpfr (moved to separate package)

* Thu Jul 05 2007 Florian La Roche <laroche@redhat.com> 4.1.4-13
- don't fail scripts to e.g. allow excludedocs installs

* Tue Apr 24 2007 Karsten Hopp <karsten@redhat.com> 4.1.4-12.3
- fix library permissions

* Wed Mar 14 2007 Karsten Hopp <karsten@redhat.com> 4.1.4-12.2
- fix typo

* Wed Mar 14 2007 Thomas Woerner <twoerner@redhat.com> 4.1.4-12.1
- added alpha support for gmp.h and gmp-mparam.h wrappers

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 4.1.4-12
- remove trailing dot from summary
- fix buildroot
- fix post/postun/... requirements
- use make install DESTDIR=...
- replace tabs with spaces
- convert changelog to utf-8

* Wed Jan 17 2007 Jakub Jelinek <jakub@redhat.com> 4.1.4-11
- make sure libmpfr.a doesn't contain SSE2 instructions on i?86 (#222371)
- rebase to mpfr 2.2.1 from 2.2.0 + cumulative fixes

* Thu Nov  2 2006 Thomas Woerner <twoerner@redhat.com> 4.1.4-10
- fixed arch order in gmp.h and gmp-mparam.h wrapper for all architectures

* Thu Nov  2 2006 Joe Orton <jorton@redhat.com> 4.1.4-10
- include ppc64 header on ppc64 not ppc header

* Fri Oct 27 2006 Thomas Woerner <twoerner@redhat.com> - 4.1.4-9
- fixed multilib devel conflicts for gmp (#212286)

* Thu Oct 26 2006 Jakub Jelinek <jakub@redhat.com> - 4.1.4-8
- upgrade mpfr to 2.2.0 (#211971)
- apply mpfr 2.2.0 cumulative patch

* Fri Jul 14 2006 Thomas Woerner <twoerner@redhat.com> - 4.1.4-7
- release bump

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.1.4-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.1.4-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Apr 18 2005 Thomas Woerner <twoerner@redhat.com> 4.1.4-6
- fixed __setfpucw call in mpfr-test.h

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 4.1.4-5
- build with gcc-4

* Wed Feb 09 2005 Karsten Hopp <karsten@redhat.de> 4.1.4-4
- rebuilt

* Sun Sep 26 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 4.1.4
- disable ppc64 patch, now fixed upstream

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 24 2004 Thomas Woerner <twoerner@redhat.com> 4.1.3-1
- new version 4.1.3

* Wed Mar 31 2004 Thomas Woerner <twoerner@redhat.com> 4.1.2-14
- dropped RPATH (#118506)

* Sat Mar 06 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- also build SSE2 DSOs, patch from Ulrich Drepper

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Thomas Woerner <twoerner@redhat.com> 4.1.2-11
- BuildRequires for automake16

* Mon Dec 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix symlink to libgmpxx.so.3  #111135
- add patch to factorize.c from gmp homepage

* Thu Oct 23 2003 Joe Orton <jorton@redhat.com> 4.1.2-9
- build with -Wa,--noexecstack

* Thu Oct 23 2003 Joe Orton <jorton@redhat.com> 4.1.2-8
- build assembly code with -Wa,--execstack
- use parallel make
- run tests, and fix C++ therein

* Thu Oct 02 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- enable mpfr  #104395
- enable cxx  #80195
- add COPYING.LIB
- add fixes from gmp web-site
- remove some cruft patches for older libtool releases

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- make configure.in work with newer autoconf

* Sun Jun 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not set extra_functions for s390x  #92001

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 4.1.2-3
- Add ppc64 patch, accompanied by running auto*

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.2

* Tue Dec 03 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.1.1
- remove un-necessary patches
- adjust s390/x86_64 patch

* Sun Oct 06 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add s390x patch
- disable current x86-64 support in longlong.h

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.1-4
- Add 4 patches, among them one for #67918
- Update URL
- s/Copyright/License/

* Mon Jul  8 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.1-3
- Redefine the configure macro, the included configure 
  script isn't happy about the rpm default one (#68190). Also, make
  sure the included libtool isn't replaced,

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat May 25 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to version 4.1
- patch s390 gmp-mparam.h to match other archs.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar 11 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.1-3
- Use standard %%configure macro and edit %%{_tmppath}

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.0.1-2
- Rebuild

* Tue Jan 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.1
- bzip2 src

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Feb 05 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed bugzilla bug #25515 where GMP wouldn't work on IA64 as IA64 is not
correctly identified as a 64 bit platform.

* Mon Dec 18 2000 Preston Brown <pbrown@redhat.com>
- include bsd mp library

* Tue Oct 17 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.1.1

* Sun Sep  3 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.1

* Sat Aug 19 2000 Preston Brown <pbrown@redhat.com>
- devel subpackage depends on main package so that .so symlink is OK.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- switch to the configure and makeinstall macros
- FHS-compliance fixing
- move docs to non-devel package

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- libtoolize for ia64

* Fri Apr 28 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.0.1

* Thu Apr 27 2000 Jakub Jelinek <jakub@redhat.com>
- sparc64 fixes for 3.0

* Wed Apr 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.0

* Mon Feb 14 2000 Matt Wilson <msw@redhat.com>
- #include <string.h> in files that use string functions

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary

* Mon Dec 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- s/GPL/LGPL/
- build as non-root (#7604)

* Mon Sep 06 1999 Jakub Jelinek <jj@ultra.linux.cz>
- merge in some debian gmp fixes
- Ulrich Drepper's __gmp_scale2 fix
- my mpf_set_q fix
- sparc64 fixes

* Wed Apr 28 1999 Cristian Gafton <gafton@redhat.com>
- add sparc patch for PIC handling

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 8)

* Thu Feb 11 1999 Michael Johnson <johnsonm@redhat.com>
- include the private header file gmp-mparam.h because several
  apps seem to assume that they are building against the gmp
  source tree and require it.  Sigh.

* Tue Jan 12 1999 Michael K. Johnson <johnsonm@redhat.com>
- libtoolize to work on arm

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- yet another touch of the spec file

* Wed Sep  2 1998 Michael Fulbright <msf@redhat.com>
- looked over before inclusion in RH 5.2

* Sun May 24 1998 Dick Porter <dick@cymru.net>
- Patch Makefile.in, not Makefile
- Don't specify i586, let configure decide the arch

* Sat Jan 24 1998 Marc Ewing <marc@redhat.com>
- started with package from Toshio Kuratomi <toshiok@cats.ucsc.edu>
- cleaned up file list
- fixed up install-info support

