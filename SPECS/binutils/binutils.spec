Summary:        Contains a linker, an assembler, and other tools
Name:           binutils
Version:        2.41
Release:        1%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://www.gnu.org/software/binutils
Source0:        https://ftp.gnu.org/gnu/binutils/%{name}-%{version}.tar.xz
# Patch was derived from source: https://src.fedoraproject.org/rpms/binutils/blob/f34/f/binutils-export-demangle.h.patch
Patch0:         export-demangle-header.patch
Provides:       bundled(libiberty)

%description
The Binutils package contains a linker, an assembler,
and other tools for handling object files.

%package        devel
Summary:        Header and development files for binutils
Requires:       %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications
for handling compiled objects.

%prep
%autosetup -p1

%build
%configure \
    --disable-silent-rules \
    --disable-werror    \
    --enable-gold       \
    --enable-ld=default \
    --enable-plugins    \
    --enable-shared     \
    --enable-64-bit-bfd \
    --with-system-zlib

%make_build tooldir=%{_prefix}

%install
%make_install tooldir=%{_prefix}
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}%{_infodir}
%find_lang %{name} --all-name

install -m 644 libiberty/pic/libiberty.a %{buildroot}%{_libdir}
install -m 644 include/libiberty.h %{buildroot}%{_includedir}

%check
sed -i 's/testsuite/ /g' gold/Makefile
%make_build check

%ldconfig_scriptlets

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
%{_bindir}/dwp
%{_bindir}/gprof
%{_bindir}/ld.bfd
%{_bindir}/ld.gold
%{_bindir}/c++filt
%{_bindir}/objdump
%{_bindir}/as
%{_bindir}/ar
%{_bindir}/objcopy
%{_bindir}/strings
%{_bindir}/addr2line
%{_bindir}/nm
%{_bindir}/size
%{_bindir}/ld
%{_bindir}/elfedit
%{_bindir}/ranlib
%{_bindir}/readelf
%{_bindir}/strip
%{_sysconfdir}/gprofng.rc
%{_bindir}/gp-archive
%{_bindir}/gp-collect-app
%{_bindir}/gp-display-html
%{_bindir}/gp-display-src
%{_bindir}/gp-display-text
%{_bindir}/gprofng
%{_libdir}/ldscripts/*
%{_mandir}/man1/readelf.1.gz
%{_mandir}/man1/windmc.1.gz
%{_mandir}/man1/ranlib.1.gz
%{_mandir}/man1/gprof.1.gz
%{_mandir}/man1/strip.1.gz
%{_mandir}/man1/c++filt.1.gz
%{_mandir}/man1/as.1.gz
%{_mandir}/man1/objcopy.1.gz
%{_mandir}/man1/elfedit.1.gz
%{_mandir}/man1/strings.1.gz
%{_mandir}/man1/nm.1.gz
%{_mandir}/man1/ar.1.gz
%{_mandir}/man1/ld.1.gz
%{_mandir}/man1/dlltool.1.gz
%{_mandir}/man1/addr2line.1.gz
%{_mandir}/man1/windres.1.gz
%{_mandir}/man1/size.1.gz
%{_mandir}/man1/objdump.1.gz
%{_mandir}/man1/gp-archive.1.gz
%{_mandir}/man1/gp-collect-app.1.gz
%{_mandir}/man1/gp-display-html.1.gz
%{_mandir}/man1/gp-display-src.1.gz
%{_mandir}/man1/gp-display-text.1.gz
%{_mandir}/man1/gprofng.1.gz

%{_libdir}/libbfd-%{version}.so
%{_libdir}/libopcodes-%{version}.so

%files devel
%{_includedir}/ansidecl.h
%{_includedir}/bfd.h
%{_includedir}/bfdlink.h
%{_includedir}/ctf-api.h
%{_includedir}/ctf.h
%{_includedir}/demangle.h
%{_includedir}/diagnostics.h
%{_includedir}/dis-asm.h
%{_includedir}/libiberty.h
%{_includedir}/plugin-api.h
%{_includedir}/symcat.h
%{_libdir}/bfd-plugins/libdep.so
%{_libdir}/libbfd.a
%{_libdir}/libbfd.so
%{_libdir}/libctf-nobfd.a
%{_libdir}/libctf-nobfd.so
%{_libdir}/libctf-nobfd.so.0
%{_libdir}/libctf-nobfd.so.0.*
%{_libdir}/libctf.a
%{_libdir}/libctf.so
%{_libdir}/libctf.so.0
%{_libdir}/libctf.so.0.*
%{_libdir}/libiberty.a
%{_libdir}/libopcodes.a
%{_libdir}/libopcodes.so
%{_includedir}/collectorAPI.h
%{_includedir}/libcollector.h
%{_includedir}/libfcollector.h
%{_includedir}/sframe-api.h
%{_includedir}/sframe.h
%{_libdir}/gprofng/libgp-collector.so
%{_libdir}/gprofng/libgp-collectorAPI.a
%{_libdir}/gprofng/libgp-collectorAPI.so
%{_libdir}/gprofng/libgp-heap.so
%{_libdir}/gprofng/libgp-iotrace.so
%{_libdir}/gprofng/libgp-sync.so
%{_libdir}/libgprofng.a
%{_libdir}/libgprofng.so
%{_libdir}/libgprofng.so.0
%{_libdir}/libgprofng.so.0.0.0
%{_libdir}/libsframe.a
%{_libdir}/libsframe.so
%{_libdir}/libsframe.so.1
%{_libdir}/libsframe.so.1.0.0

%changelog
* Wed Nov 08 2023 Andrew Phelps <anphel@microsoft.com> - 2.41-1
- Upgrade to version 2.41

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.37-7
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Aug 29 2023 Andy Zaugg <azaugg@linkedin.com> - 2.37-6
- Use the pic'ed libiberty.a version

* Wed Feb 08 2023 Rachel Menge <rachelmenge@microsoft.com> - 2.37-5
- Backport upstream patch to fix CVE-2022-4285

* Thu Sep 01 2022 Henry Beberman <henry.beberman@microsoft.com> - 2.37-4
- Backport upstream patch to fix CVE-2022-38533

* Wed Apr 20 2022 Andrew Phelps <anphel@microsoft.com> - 2.37-3
- Add patch to fix CVE-2021-45078

* Fri Dec 03 2021 Andrew Phelps <anphel@microsoft.com> - 2.37-2
- Add thin_archive_descriptor.patch to fix nodejs build issue

* Thu Nov 04 2021 Andrew Phelps <anphel@microsoft.com> - 2.37-1
- Update version to 2.37
- Update export-demangle-header.patch

* Fri Oct 15 2021 Ismail Kose <iskose@microsoft.com> - 2.36.1-4
- Adding READONLY keyword support in linker script
- Verified license

* Tue Sep 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.36.1-3
- Adding 'libiberty' lib and header.

* Tue Aug 24 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.36.1-2
- Add patch from Fedora 34 (license: MIT) to export demangle.h from libiberty sources
- Lint spec

* Tue May 11 2021 Andrew Phelps <anphel@microsoft.com> - 2.36.1-1
- Update to version 2.36.1

* Mon Jan 11 2021 Emre Girgin <mrgirgin@microsoft.com> - 2.32-5
- Update URL and Source0 to use https.
- Fix CVE-2020-35493.
- Fix CVE-2020-35494.
- Fix CVE-2020-35495.
- Fix CVE-2020-35496.
- Fix CVE-2020-35507.

* Thu Oct 22 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.32-4
- Use autosetup
- Fix CVE-2019-12972.
- Fix CVE-2019-14250.
- Fix CVE-2019-14444.
- Fix CVE-2019-9071.
- No patch CVE-2019-9072.
- Fix CVE-2019-9073.
- Fix CVE-2019-9074.
- No patch CVE-2019-9076.
- Fix CVE-2019-17450.
- Fix CVE-2019-17451.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.32-3
- Added %%license line automatically

* Wed May 06 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.32-2
- Fix CVE-2019-9077.
- Fix CVE-2019-9075.
- Fix CVE-2019-9070.
- Remove sha1 macro.

* Thu Feb 06 2020 Andrew Phelps <anphel@microsoft.com> - 2.32-1
- Update to version 2.32

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.31.1-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Mar 14 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.31.1-4
- Fix CVE-2019-9075 and CVE-2019-9077

* Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> - 2.31.1-3
- fix CVE-2018-1000876

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.31.1-2
- Fix CVE-2018-17358, CVE-2018-17359 and CVE-2018-17360

* Fri Sep 21 2018 Keerthana K <keerthanak@vmware.com> - 2.31.1-1
- Update to version 2.31.1

* Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> - 2.31-1
- Update to version 2.31.

* Thu Jun 7 2018 Keerthana K <keerthanak@vmware.com> - 2.30-4
- Fix CVE-2018-10373

* Mon Mar 19 2018 Alexey Makhalov <amakhalov@vmware.com> - 2.30-3
- Add libiberty to the -devel package

* Wed Feb 28 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.30-2
- Fix CVE-2018-6543.

* Mon Jan 29 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.30-1
- Update to version 2.30

* Mon Dec 18 2017 Anish Swaminathan <anishs@vmware.com> - 2.29.1-5
- Fix CVEs CVE-2017-17121, CVE-2017-17122, CVE-2017-17123,
- CVE-2017-17124, CVE-2017-17125

* Mon Dec 4 2017 Anish Swaminathan <anishs@vmware.com> - 2.29.1-4
- Fix CVEs CVE-2017-16826, CVE-2017-16827, CVE-2017-16828, CVE-2017-16829,
- CVE-2017-16830, CVE-2017-16831, CVE-2017-16832

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.29.1-3
- Aarch64 support
- Parallel build

* Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> - 2.29.1-2
- Add patch to fix CVE-2017-15020

* Mon Oct 2 2017 Anish Swaminathan <anishs@vmware.com> - 2.29.1-1
- Version update to 2.29.1, fix CVEs CVE-2017-12799, CVE-2017-14729,CVE-2017-14745

* Fri Aug 11 2017 Anish Swaminathan <anishs@vmware.com> - 2.29-3
- Apply patches for CVE-2017-12448,CVE-2017-12449,CVE-2017-12450,CVE-2017-12451,
- CVE-2017-12452,CVE-2017-12453,CVE-2017-12454,CVE-2017-12455,CVE-2017-12456,
- CVE-2017-12457,CVE-2017-12458,CVE-2017-12459

* Tue Aug 8 2017 Rongrong Qiu <rqiu@vmware.com> - 2.29-2
- fix for make check for bug 1900247

* Wed Aug 2 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.29-1
- Version update

* Tue May 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.28-2
- Patch for CVE-2017-8421

* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> - 2.28-1
- Upgraded to version 2.28
- Apply patch for CVE-2017-6969

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.25.1-2
- GA - Bump release of all rpms

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.25.1-1
- Updated to version 2.25.1

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 2.25-2
- Handled locale files with macro find_lang

* Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.25-1
- Updated to 2.25

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 2.24-1
- Initial build. First version
