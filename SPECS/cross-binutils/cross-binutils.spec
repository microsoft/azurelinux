# Globals which should be in a macro file.
# These should be set programatically in the future.
%global _host_arch      x86_64
%global _target_arch    aarch64
%global _tuple          %{_target_arch}-%{_vendor}-linux-gnu
%global _cross_name     %{_target_arch}-%{_vendor}-linux-gnu

# Folders which should be in our macro file
%global _opt                /opt/
%global _crossdir           /opt/cross/

# Generally we include '/usr' in most paths.
# Can we also use '/usr' for our paths? This will bring us in line with the
# %%configure macro which sets these.
%global _bindir            /bin
%global _sbindir           /sbin
%global _libdir            /lib
%global _lib64dir          /lib64
%global _libexecdir        /libexec
%global _datadir           /share
%global _docdir            /share/doc
%global _includedir        /include
%global _infodir           /share/info
%global _mandir            /share/man
%global _oldincludedir     /include


# Why is this wrong? We get "x86_64-pc-linux-gnu" when eval'd, but our 
# tools select "aarch64-linux-gnu"
%global _host_vendor        %{nil}

# If we want our cross compile aware packges to also support native, we
# need logic to switch modes something like this:
%if "%{_target_arch}" != "%{_host_arch}"
%global _cross_prefix       %{_crossdir}%{_tuple}/
%global _cross_sysroot      %{_crossdir}%{_tuple}/sysroot/
%global _cross_includedir   /usr/%{_host}/%{_tuple}/include/
%global _cross_infodir      %{_crossdir}%{_tuple}/share/info
%global _cross_bindir       %{_tuple}/bin
%global _cross_libdir       %{_tuple}/lib
%global _tuple_name         %{_tuple}-
%else
%global _cross_prefix       %{nil}
%global _cross_sysroot      %{nil}
%global _cross_includedir   %{_includedir}
%global _cross_infodir      %{_infodir}
%global _cross_bindir       %{_bindir}
%global _cross_libdir       %{_libdir}
%global _tuple_name         %{nil}
%endif

Summary:        Contains a linker, an assembler, and other tools
Name:           %{_cross_name}-binutils
Version:        2.37
Release:        8%{?dist}
License:        GPLv2+
URL:            http://www.gnu.org/software/binutils
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
ExclusiveArch:  x86_64
Source0:        http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz
# Patch was derived from source: https://src.fedoraproject.org/rpms/binutils/blob/f34/f/binutils-export-demangle.h.patch
Patch0:         export-demangle-header.patch
# Patch1 Source https://sourceware.org/git/?p=binutils-gdb.git;a=commit;h=6b86da53d5ee2022b9065f445d23356190380746
Patch1:         linker-script-readonly-keyword-support.patch
Patch2:         thin_archive_descriptor.patch

%description
The Binutils package contains a linker, an assembler,
and other tools for handling object files.

%prep
%autosetup -p1 -n binutils-%{version}

%build
# Ideally we would like to model this after the %%configure macro in the future.
./configure \
            --prefix=%{_cross_prefix} \
            --target=%{_tuple} \
            --disable-multilib \
            --with-sysroot=%{_cross_sysroot}

make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=%{buildroot} install

find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}/%{_cross_infodir}
%find_lang %{name} --all-name

%files -f %{name}.lang
%defattr(-,root,root)
%license COPYING
#%%{_cross_prefix}%%{_cross_bindir}/dwp
#%%{_cross_prefix}%%{_cross_bindir}/gprof
%{_cross_prefix}%{_cross_bindir}/ld.bfd
#%%{_cross_prefix}%%{_cross_bindir}/ld.gold
#%%{_cross_prefix}%%{_cross_bindir}/c++filt
%{_cross_prefix}%{_cross_bindir}/objdump
%{_cross_prefix}%{_cross_bindir}/as
%{_cross_prefix}%{_cross_bindir}/ar
%{_cross_prefix}%{_cross_bindir}/objcopy
#%%{_cross_prefix}%%{_cross_bindir}/strings
#%%{_cross_prefix}%%{_cross_bindir}/addr2line
%{_cross_prefix}%{_cross_bindir}/nm
#%%{_cross_prefix}%%{_cross_bindir}/size
%{_cross_prefix}%{_cross_bindir}/ld
#%%{_cross_prefix}%%{_cross_bindir}/elfedit
%{_cross_prefix}%{_cross_bindir}/ranlib
%{_cross_prefix}%{_cross_bindir}/readelf
%{_cross_prefix}%{_cross_bindir}/strip

# These duplicates are not found in the normal binutils
#%%{_cross_prefix}%%{_bindir}/%%{_tuple_name}dwp
%{_cross_prefix}%{_bindir}/%{_tuple_name}gprof
%{_cross_prefix}%{_bindir}/%{_tuple_name}ld.bfd
#%%{_cross_prefix}%%{_bindir}/%%{_tuple_name}ld.gold
%{_cross_prefix}%{_bindir}/%{_tuple_name}c++filt
%{_cross_prefix}%{_bindir}/%{_tuple_name}objdump
%{_cross_prefix}%{_bindir}/%{_tuple_name}as
%{_cross_prefix}%{_bindir}/%{_tuple_name}ar
%{_cross_prefix}%{_bindir}/%{_tuple_name}objcopy
%{_cross_prefix}%{_bindir}/%{_tuple_name}strings
%{_cross_prefix}%{_bindir}/%{_tuple_name}addr2line
%{_cross_prefix}%{_bindir}/%{_tuple_name}nm
%{_cross_prefix}%{_bindir}/%{_tuple_name}size
%{_cross_prefix}%{_bindir}/%{_tuple_name}ld
%{_cross_prefix}%{_bindir}/%{_tuple_name}elfedit
%{_cross_prefix}%{_bindir}/%{_tuple_name}ranlib
%{_cross_prefix}%{_bindir}/%{_tuple_name}readelf
%{_cross_prefix}%{_bindir}/%{_tuple_name}strip

%{_cross_prefix}%{_cross_libdir}/ldscripts/*
#%%{_cross_prefix}%{_cross_libdir}/bfd-plugins/libdep.so
"/opt/cross/aarch64-mariner-linux-gnu/lib/bfd-plugins/libdep.so"

%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}readelf.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}windmc.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}ranlib.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}gprof.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}strip.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}c++filt.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}as.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}objcopy.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}elfedit.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}strings.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}nm.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}ar.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}ld.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}dlltool.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}addr2line.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}windres.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}size.1
%{_cross_prefix}%{_mandir}/man1/%{_tuple_name}objdump.1

# These are the -devel files, we are not generating them.
#%%{_cross_prefix}%%{_libdir}/libbfd-%%{version}.so
#%%{_cross_prefix}%%{_libdir}/libopcodes-%%{version}.so

#Headers are available in the debug folder only, or not at all.
#%%{_cross_prefix}%%{_cross_includedir}/plugin-api.h
#%%{_cross_prefix}%%{_cross_includedir}/symcat.h
#%%{_cross_prefix}%%{_cross_includedir}/bfd.h
#%%{_cross_prefix}%%{_cross_includedir}/ansidecl.h
#%%{_cross_prefix}%%{_cross_includedir}/bfdlink.h
#%%{_cross_prefix}%%{_cross_includedir}/dis-asm.h
#%%{_cross_prefix}%%{_cross_includedir}/diagnostics.h

#%%{_cross_prefix}%%{_libdir}/libbfd.a
#%%{_cross_prefix}%%{_libdir}/libopcodes.a
#%%{_cross_prefix}%%{_libdir}/libbfd.so
#%%{_cross_prefix}%%{_libdir}/libopcodes.so

%changelog
* Thu Dec 15 2022 Dallas Delaney <dadelan@microsoft.com> - 2.37-8
- Fork normal binutils package into cross compile aware package

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

* Tue Aug 24 2021 Thomas Crain <thcrain@microsoft.com> - 2.36.1-2
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

* Sat May 09 00:21:17 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.32-3
- Added %%license line automatically

* Wed May 06 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.32-2
- Fix CVE-2019-9077.
- Fix CVE-2019-9075.
- Fix CVE-2019-9070.
- Remove sha1 macro.

* Thu Feb 06 2020 Andrew Phelps <anphel@microsoft.com> 2.32-1
- Update to version 2.32

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.31.1-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Mar 14 2019 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.31.1-4
- Fix CVE-2019-9075 and CVE-2019-9077

* Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> 2.31.1-3
- fix CVE-2018-1000876

* Tue Jan 08 2019 Alexey Makhalov <amakhalov@vmware.com> 2.31.1-2
- Fix CVE-2018-17358, CVE-2018-17359 and CVE-2018-17360

* Fri Sep 21 2018 Keerthana K <keerthanak@vmware.com> 2.31.1-1
- Update to version 2.31.1

* Wed Aug 1 2018 Keerthana K <keerthanak@vmware.com> 2.31-1
- Update to version 2.31.

* Thu Jun 7 2018 Keerthana K <keerthanak@vmware.com> 2.30-4
- Fix CVE-2018-10373

* Mon Mar 19 2018 Alexey Makhalov <amakhalov@vmware.com> 2.30-3
- Add libiberty to the -devel package

* Wed Feb 28 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-2
- Fix CVE-2018-6543.

* Mon Jan 29 2018 Xiaolin Li <xiaolinl@vmware.com> 2.30-1
- Update to version 2.30

* Mon Dec 18 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-5
- Fix CVEs CVE-2017-17121, CVE-2017-17122, CVE-2017-17123,
- CVE-2017-17124, CVE-2017-17125

* Mon Dec 4 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-4
- Fix CVEs CVE-2017-16826, CVE-2017-16827, CVE-2017-16828, CVE-2017-16829,
- CVE-2017-16830, CVE-2017-16831, CVE-2017-16832

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29.1-3
- Aarch64 support
- Parallel build

* Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-2
- Add patch to fix CVE-2017-15020

* Mon Oct 2 2017 Anish Swaminathan <anishs@vmware.com> 2.29.1-1
- Version update to 2.29.1, fix CVEs CVE-2017-12799, CVE-2017-14729,CVE-2017-14745

* Fri Aug 11 2017 Anish Swaminathan <anishs@vmware.com> 2.29-3
- Apply patches for CVE-2017-12448,CVE-2017-12449,CVE-2017-12450,CVE-2017-12451,
- CVE-2017-12452,CVE-2017-12453,CVE-2017-12454,CVE-2017-12455,CVE-2017-12456,
- CVE-2017-12457,CVE-2017-12458,CVE-2017-12459

* Tue Aug 8 2017 Rongrong Qiu <rqiu@vmware.com> 2.29-2
- fix for make check for bug 1900247

* Wed Aug 2 2017 Alexey Makhalov <amakhalov@vmware.com> 2.29-1
- Version update

* Tue May 16 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.28-2
- Patch for CVE-2017-8421

* Thu Apr 06 2017 Anish Swaminathan <anishs@vmware.com> 2.28-1
- Upgraded to version 2.28
- Apply patch for CVE-2017-6969

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25.1-2
- GA - Bump release of all rpms

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> 2.25.1-1
- Updated to version 2.25.1

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> 2.25-2
- Handled locale files with macro find_lang

* Mon Apr 6 2015 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.25-1
- Updated to 2.25

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.24-1
- Initial build. First version
