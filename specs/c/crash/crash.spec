# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# crash core analysis suite
#
Summary: Kernel analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles
Name: crash
Version: 9.0.1
Release: 3%{?dist}
License: GPL-3.0-only
Source0: https://github.com/crash-utility/crash/archive/crash-%{version}.tar.gz
Source1: http://ftp.gnu.org/gnu/gdb/gdb-16.2.tar.gz
URL: https://crash-utility.github.io
ExclusiveOS: Linux
ExclusiveArch: %{ix86} ia64 x86_64 ppc ppc64 s390 s390x %{arm} aarch64 ppc64le riscv64
BuildRequires: ncurses-devel zlib-devel lzo-devel snappy-devel bison wget patch texinfo libzstd-devel
BuildRequires: make gcc gcc-c++
BuildRequires: gmp-devel mpfr-devel
Requires: binutils
Provides: bundled(libiberty)
Provides: bundled(gdb) = 16.2
Patch0: lzo_snappy_zstd.patch
Patch1: crash-9.0.1_build.patch

%description
The core analysis suite is a self-contained tool that can be used to
investigate either live systems, kernel core dumps created from the
netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch
offered by Mission Critical Linux, or the LKCD kernel patch.

%package devel
Requires: %{name} = %{version}, zlib-devel
Summary: kernel crash analysis utility for live systems, netdump, diskdump, kdump, LKCD or mcore dumpfiles

%description devel
The core analysis suite is a self-contained tool that can be used to
investigate either live systems, kernel core dumps created from the
netdump, diskdump and kdump packages from Red Hat Linux, the mcore kernel patch
offered by Mission Critical Linux, or the LKCD kernel patch.

%prep
%setup -n %{name}-%{version} -q
%patch -P 0 -p1 -b lzo_snappy_zstd.patch
%patch -P 1 -p1

%build

cp %{SOURCE1} .
make -j`nproc` RPMPKG="%{version}-%{release}" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" LDFLAGS="%{build_ldflags}"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
%make_install
mkdir -p %{buildroot}%{_mandir}/man8
cp -p crash.8 %{buildroot}%{_mandir}/man8/crash.8
mkdir -p %{buildroot}%{_includedir}/crash
chmod 0644 defs.h
cp -p defs.h %{buildroot}%{_includedir}/crash

%files
%{_bindir}/crash
%{_mandir}/man8/crash.8*
%doc README COPYING3

%files devel
%{_includedir}/*

%changelog
* Fri Dec 19 2025 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 9.0.1-2
- enable RISC-V 64-bit architecture

* Fri Nov 21 2025 Lianbo Jiang <lijiang@redhat.com> - 9.0.1-1
- Rebase to upstream crash 9.0.1

* Mon Oct 20 2025 Lianbo Jiang <lijiang@redhat.com> - 9.0.0-5
- Add blk_mq shared tags support for dev -d/-D
- Support running on X86_64 with RISCV target
- RISCV64: Add 'PAGE DIRECTORY' property to the 'vtop' command
- vmware_vmss: support segment registers
- vmware_guestdump: support segment registers
- Fix the segfault issue caused by "dis -s" command
- Add a rustfilt command to demangle a mangled Rust symbol
- Enable demangling a mangled Rust support
- Enable resolving mangled Rust symbol in lockless ring buffer
- Fix a compilation error on the old gcc version 8.5.0
- Fix for log command printed a couple of empty lines
- Optimize extensions's compiler from gcc to $(CC)
- Fix get_pathname() not handling stacked mounts
- Fix "mount <address>" fail when "super_block.s_files" unavaliable
- Fix "mount" MNT_CURSOR entries (kernels 5.8-6.7)


* Fri Jul 25 2025 Lianbo Jiang <lijiang@redhat.com> - 9.0.0-4
- x86_64: filter unwanted warning message for "bt -T" cmd
- doc: Update requirements for building on Fedora
- gdb: Fix a regression for eppic extension on gdb-16.2
- Fix crash initialization failure on LoongArch with recent GDB versions
- gdb: Disable DT_DEBUG lookup by GDB inside the vmcore

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Lianbo Jiang <lijiang@redhat.com> - 9.0.0-2
- vmware_guestdump: Version 7 support
- Fix incorrect task state during exit
- Add multi-threads support in crash target
- Call cmd_bt silently after "set pid"
- x86_64: Add gdb multi-stack unwind support
- arm64: Add gdb multi-stack unwind support
- ppc64: Add gdb multi-stack unwind support
- Fix the issue of "page excluded" messages flooding
- Fix "kmem -p" option on Linux 6.16-rc1 and later kernels

* Fri Apr 25 2025 Lianbo Jiang <lijiang@redhat.com> - 9.0.0-1
- Rebase to upstream crash 9.0.0

* Wed Feb 5 2025 Lianbo Jiang <lijiang@redhat.com> - 8.0.6-4
- Doc: add compilation requirements note in README
- Fix "net -a" option on Linux 6.13 and later kernels
- kmem: fix the determination of slab page due to invalid page_type
- Enhance "kmem -i[=shared]" to display(or not) shared pages
- Fix misleading CPU count in display_sys_stats()
- arm64: add pac mask to better support gdb stack unwind
- x86_64: Fix 'bt -S/-I' segfault issue
- Fix build failure in readline lib
- tools.c: do not use keywords 'nullptr' as a variable in code
- Fix build failure on 32bit machine(i686)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Lianbo Jiang <lijiang@redhat.com> - 8.0.6-2
- Fix infinite loop during module symbols initialization
- Fix for "help -r" segfault in case of ramdump
- arm64: add cpu context registers to better support gdb stack unwind
- x86_64: Mark #VC stack unavailable when CONFIG_AMD_MEM_ENCRYPT is not set
- Fix incorrect 'bt -v' output suggesting overflow

* Tue Nov 12 2024 Lianbo Jiang <lijiang@redhat.com> - 8.0.6-1
- Rebase to upstream crash 8.0.6

* Thu Aug 22 2024 Lianbo Jiang <lijiang@redhat.com> - 8.0.5-5
- arm64: Fix a segfault issue due to the incorrect irq_stack_size on ARM64
- s390x: Fix "bt -f/-F" command fail with seek error
- arm64: Introduction of support for 16K page with 2-level table support
- Fix a "Bus error" issue caused by 'crash --osrelease' or crash loading

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Lianbo Jiang <lijiang@redhat.com> - 8.0.5-3
- x86_64: fix for adding kernel stack padding issue
- Fix "kmem -v" option on Linux 6.9 and later kernels
- X86 64: fix for crash session loading failure
- Fix for failing to load kernel module

* Tue May 28 2024 Lianbo Jiang <lijiang@redhat.com> - 8.0.5-2
- Adding the zram decompression algorithm "lzo-rle"
- arm64: section_size_bits compatible with macro definitions
- Reflect __{start,end}_init_task kernel symbols rename

* Mon Apr 29 2024 Lianbo Jiang <lijiang@redhat.com> - 8.0.5-1
- Rebase to upstream crash 8.0.5

* Tue Apr 02 2024 Lianbo Jiang <lijiang@redhat.com> - 8.0.4-5
- Update to the latest upstream commit: ce47cb8dabb5

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 28 2023 Lianbo Jiang <lijiang@redhat.com> - 8.0.4-2
- Update to the latest upstream commit: 53d2577cef98

* Thu Nov 16 2023 Lianbo Jiang <lijiang@redhat.com> - 8.0.4-1
- Rebase to upstream crash 8.0.4

* Tue Jul 25 2023 Lianbo Jiang <lijiang@redhat.com> - 8.0.3-5
- Fix warning about kernel version inconsistency during crash startup

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Lianbo Jiang <lijiang@redhat.com> - 8.0.3-3
- Support module memory layout change on Linux 6.4

* Sun Jun 25 2023 Sérgio Basto <sergio@serjux.com> - 8.0.3-2
- Migrate to SPDX license format

* Fri Apr 28 2023 Lianbo Jiang <lijiang@redhat.com> - 8.0.3-1
- Rebase to upstream crash 8.0.3

* Fri Mar 10 2023 Lianbo Jiang <lijiang@redhat.com> - 8.0.2-4
- Fix "kmem -n" option to display memory blocks on Linux 6.3-rc1 and later
- gdb: Fix an assertion failure in dw2_find_pc_sect_compunit_symtab()
- Fix for "net -n" option to properly deal with an invalid argument
- Fix C99 compatibility issues in embedded copy of GDB
- Enhance "net" command to display IPv6 address of network interface
- Fix for "search -u" option failing in maple tree kernel
- x86_64: Fix "bt" command on kernels with random_kstack_offset=on
- Fix for "dis" command to correctly display the offset of disassembly code
- Fix for "bt" command unnecessarily printing an exception frame
- Fix for "kmem -i" option to not print invalid values for CACHED
- Fix for "net -s" option to show IPv6 addresses on Linux 3.13 and later
- Fix "kmem -s|-S" not working properly on RHEL8.6 and later
- Fix for "bt" command printing "bogus exception frame" warning

* Tue Feb 07 2023 Lianbo Jiang <lijiang@redhat.com> - 8.0.2-3
- Update to the latest upstream commit <46344aa2f92b>

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Lianbo Jiang <lijiang@redhat.com> - 8.0.2-1
- Rebase to upstream crash 8.0.2

* Thu Sep 22 2022 Lianbo Jiang <lijiang@redhat.com> - 8.0.1-4
- Update to the latest upstream commit <3b5e3e1583a1>

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 10 2022 Lianbo Jiang <lijiang@redhat.com> - 8.0.1-2
- Update to the latest upstream commit <c07068266b41>

* Sun May 01 2022 Lianbo Jiang <lijiang@redhat.com> - 8.0.1-1
- Rebase to upstream crash 8.0.1

* Wed Feb 09 2022 Lianbo Jiang <lijiang@redhat.com> - 8.0.0-6
- Update to the latest upstream commit <5f390ed811b0>
- Fix for cdefs issue on ppc64le

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Lianbo Jiang <lijiang@redhat.com> - 8.0.0-4
- Fix segmentation fault caused by crash extension modules
- Support the overflow stack exception handling on aarch64

* Mon Dec 06 2021 Lianbo Jiang <lijiang@redhat.com> - 8.0.0-3
- Enable ZSTD feature

* Fri Nov 26 2021 Lianbo Jiang <lijiang@redhat.com> - 8.0.0-2
- Enable LTO and Hardened package

* Wed Nov 24 2021 Lianbo Jiang <lijiang@redhat.com> - 8.0.0-1
- Rebase to upstream 8.0.0

* Sat Nov 06 2021 Lianbo Jiang <lijiang@redhat.com> - 7.3.0-5
- Update to the latest upstream: commit <68870c83d299>

* Tue Oct 12 2021 Lianbo Jiang <lijiang@redhat.com> - 7.3.0-4
- Update to gdb-10.2

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Lianbo Jiang <lijiang@redhat.com> - 7.3.0-2
- Update to the latest upstream <f53b73e8380b>

* Fri May 07 2021 Lianbo Jiang <lijiang@redhat.com> - 7.3.0-1
- Rebase to upstream 7.3.0

* Mon Mar 08 2021 Lianbo Jiang <lijiang@redhat.com> - 7.2.9-5
- Fix Segmentation fault
- Update to the latest upstream: commit <9c0c6c1b3750>

* Fri Feb 05 2021 Lianbo Jiang <lijiang@redhat.com> - 7.2.9-4
- Update to the latest upstream: commit <fdb41f0b6fa4>

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Lianbo Jiang <lijiang@redhat.com> - 7.2.9-2
- Add support for lockless ringbuffer

* Wed Nov 25 2020 Lianbo Jiang <lijiang@redhat.com> - 7.2.9-1
- Update to latest upstream release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 7.2.8-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 7.2.8-3
- Disable LTO

* Fri Jan 31 2020 Dave Anderson <anderson@redhat.com> - 7.2.8-2
- Update to latest upstream release
- Fix aarch64 build for gcc-10 -fno-common

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 23 2019 Dave Anderson <anderson@redhat.com> - 7.2.7-1
- Update to latest upstream release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May  6 2019 Dave Anderson <anderson@redhat.com> - 7.2.6-1
- Update to latest upstream release

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7.2.5-3
- Rebuild for readline 8.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Dave Anderson <anderson@redhat.com> - 7.2.5-1
- Update to latest upstream release

* Mon Sep 24 2018 Dave Anderson <anderson@redhat.com> - 7.2.4-1
- Update to latest upstream release

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 18 2018 Dave Anderson <anderson@redhat.com> - 7.2.3-1
- Update to latest upstream release

* Fri Feb 23 2018 Dave Anderson <anderson@redhat.com> - 7.2.1-2
- Use RPM build flags for LDFLAGS

* Fri Feb 16 2018 Dave Anderson <anderson@redhat.com> - 7.2.1-1
- Update to latest upstream release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct  2 2017 Dave Anderson <anderson@redhat.com> - 7.2.0-1
- Update to latest upstream release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 24 2017 Dave Anderson <anderson@redhat.com> - 7.1.9-1
- Update to latest upstream release

* Thu Feb 23 2017 Dave Anderson <anderson@redhat.com> - 7.1.8-1
- Update to latest upstream release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 7.1.7-2
- Rebuild for readline 7.x

* Tue Dec  6 2016 Dave Anderson <anderson@redhat.com> - 7.1.7-1
- Update to latest upstream release

* Fri Oct 14 2016 Dave Anderson <anderson@redhat.com> - 7.1.6-1
- Update to latest upstream release
- Fix for RHBZ#1044119 - crash bundles gdb

* Thu May  5 2016 Dave Anderson <anderson@redhat.com> - 7.1.5-2
- BZ #1333295 - FTBFS due compiler warnings in elf64-s390.c

* Thu Apr 28 2016 Dave Anderson <anderson@redhat.com> - 7.1.5-1
- Update to latest upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Dave Anderson <anderson@redhat.com> - 7.1.4-1
- Update to latest upstream release

* Thu Sep  3 2015 Dave Anderson <anderson@redhat.com> - 7.1.3-1
- Update to latest upstream release

* Mon Jul 13 2015 Dave Anderson <anderson@redhat.com> - 7.1.2-1
- Update to latest upstream release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Dave Anderson <anderson@redhat.com> - 7.1.1-1
- Update to latest upstream release

* Mon Mar  2 2015 Dave Anderson <anderson@redhat.com> - 7.1.0-3
- Support increment of Linux version from 3 to 4

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 7.1.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb 10 2015 Dave Anderson <anderson@redhat.com> - 7.1.0-1
- Update to latest upstream release

* Fri Nov 15 2014 Dave Anderson <anderson@redhat.com> - 7.0.9-1
- Update to latest upstream release

* Mon Sep 15 2014 Dave Anderson <anderson@redhat.com> - 7.0.8-1
- Update to latest upstream release
- Add ppc64le as supported architecture for crash package (BZ #1136050)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 02 2014 Dave Anderson <anderson@redhat.com> - 7.0.7-2
- Fix FTBS for aarch64 (BZ #1114588)

* Wed Jun 11 2014 Dave Anderson <anderson@redhat.com> - 7.0.7-1
- Update to latest upstream release
- Fix Fedora_21_Mass_Rebuild FTBFS (BZ #1106090)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 28 2014 Dave Anderson <anderson@redhat.com> - 7.0.5-1
- Update to latest upstream release
- Use system readline library
- Fix "crash --log vmcore" command for 3.11 and later kernels.

* Tue Dec 17 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 7.0.4-2
- crash bundles gdb which bundles libiberty.  Add virtual Provides for
  libiberty tracking.  Open a bug for unbundling gdb RHBZ#1044119

* Mon Dec 16 2013 Dave Anderson <anderson@redhat.com> - 7.0.4-1
- Update to latest upstream release

* Tue Oct 29 2013 Dave Anderson <anderson@redhat.com> - 7.0.3-1
- Update to latest upstream release

* Wed Sep 04 2013 Dave Anderson <anderson@redhat.com> - 7.0.2-1
- Update to latest upstream release
- Build with lzo and snappy compression capability

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Dave Anderson <anderson@redhat.com> - 7.0.1-1
- Update to latest upstream release
- Add aarch64 as an exclusive arch

* Tue Apr  9 2013 Dave Anderson <anderson@redhat.com> - 6.1.6-1
- Update to latest upstream release

* Tue Feb 19 2013 Dave Anderson <anderson@redhat.com> - 6.1.4-1
- Update to latest upstream release

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  9 2013 Dave Anderson <anderson@redhat.com> - 6.1.2-1
- Update to latest upstream release

* Tue Nov 27 2012 Dave Anderson <anderson@redhat.com> - 6.1.1-1
- Update to latest upstream release

* Mon Sep  1 2012 Dave Anderson <anderson@redhat.com> - 6.1.0-1
- Add ppc to ExclusiveArch list
- Update to latest upstream release

* Tue Aug 21 2012 Dave Anderson <anderson@redhat.com> - 6.0.9-1
- Update to latest upstream release

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  1 2012 Dave Anderson <anderson@redhat.com> - 6.0.8-1
- Update to latest upstream release.
- Replace usage of "struct siginfo" with "siginfo_t".

* Mon Apr 30 2012 Dave Anderson <anderson@redhat.com> - 6.0.6-1
- Update to latest upstream release

* Mon Mar 26 2012 Dave Anderson <anderson@redhat.com> - 6.0.5-1
- Update to latest upstream release

* Wed Jan  4 2012 Dave Anderson <anderson@redhat.com> - 6.0.2-1
- Update to latest upstream release

* Wed Oct 26 2011 Dave Anderson <anderson@redhat.com> - 6.0.0-1
- Update to latest upstream release

* Tue Sep 20 2011 Dave Anderson <anderson@redhat.com> - 5.1.8-1
- Update to latest upstream release
- Additional fixes for gcc-4.6 -Werror compile failures for ARM architecture.

* Thu Sep  1 2011 Dave Anderson <anderson@redhat.com> - 5.1.7-2
- Fixes for gcc-4.6 -Werror compile failures for ARM architecture.

* Wed Aug 17 2011 Dave Anderson <anderson@redhat.com> - 5.1.7-1
- Update to latest upstream release
- Fixes for gcc-4.6 -Werror compile failures for ppc64/ppc.

* Tue May 31 2011 Peter Robinson <pbrobinson@gmail.com> - 5.1.5-1
- Update to latest upstream release
- Add ARM to the Exclusive arch

* Wed Feb 25 2011 Dave Anderson <anderson@redhat.com> - 5.1.2-2
- Fixes for gcc-4.6 -Werror compile failures in gdb module.  

* Wed Feb 23 2011 Dave Anderson <anderson@redhat.com> - 5.1.2-1
- Upstream version.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 20 2010 Dave Anderson <anderson@redhat.com> - 5.0.6-2
- Bump version.

* Tue Jul 20 2010 Dave Anderson <anderson@redhat.com> - 5.0.6-1
- Update to upstream version.

* Fri Sep 11 2009 Dave Anderson <anderson@redhat.com> - 4.0.9-2
  Bump version.

* Fri Sep 11 2009 Dave Anderson <anderson@redhat.com> - 4.0.9-1
- Update to upstream release, which allows the removal of the 
  Revision tag workaround, the crash-4.0-8.11-dwarf3.patch and 
  the crash-4.0-8.11-optflags.patch

* Sun Aug 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 4.0.8.11-2
- Fix reading of dwarf 3 DW_AT_data_member_location
- Use proper compiler flags

* Wed Aug 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 4.0.8.11-1
- Update to later upstream release
- Fix abuse of Revision tag

- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-9.7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0-8.7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Dave Anderson <anderson@redhat.com> - 4.0-7.7.2
- Replace exclusive arch i386 with ix86.

* Thu Feb 19 2009 Dave Anderson <anderson@redhat.com> - 4.0-7.7.1
- Updates to this file per crash merge review
- Update to upstream version 4.0-7.7.  Full changelog viewable in:
    http://people.redhat.com/anderson/crash.changelog.html

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.0-7
- fix license tag

* Tue Apr 29 2008 Dave Anderson <anderson@redhat.com> - 4.0-6.3
- Added crash-devel subpackage
- Updated crash.patch to match upstream version 4.0-6.3

* Wed Feb 20 2008 Dave Anderson <anderson@redhat.com> - 4.0-6.0.5
- Second attempt at addressing the GCC 4.3 build, which failed due
  to additional ptrace.h includes in the lkcd vmdump header files.

* Wed Feb 20 2008 Dave Anderson <anderson@redhat.com> - 4.0-6.0.4
- First attempt at addressing the GCC 4.3 build, which failed on x86_64
  because ptrace-abi.h (included by ptrace.h) uses the "u32" typedef,
  which relies on <asm/types.h>, and include/asm-x86_64/types.h
  does not not typedef u32 as done in include/asm-x86/types.h.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.0-6.0.3
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Dave Anderson <anderson@redhat.com> - 4.0-5.0.3
- Updated crash.patch to match upstream version 4.0-5.0.

* Wed Aug 29 2007 Dave Anderson <anderson@redhat.com> - 4.0-4.6.2
- Updated crash.patch to match upstream version 4.0-4.6.

* Wed Sep 13 2006 Dave Anderson <anderson@redhat.com> - 4.0-3.3
- Updated crash.patch to match upstream version 4.0-3.3.
- Support for x86_64 relocatable kernels.  BZ #204557

* Mon Aug  7 2006 Dave Anderson <anderson@redhat.com> - 4.0-3.1
- Updated crash.patch to match upstream version 4.0-3.1.
- Added kdump reference to description.
- Added s390 and s390x to ExclusiveArch list.  BZ #199125
- Removed LKCD v1 pt_regs references for s390/s390x build.
- Removed LKCD v2_v3 pt_regs references for for s390/s390x build.

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 4.0-3
- rebuild

* Mon May 15 2006 Dave Anderson <anderson@redhat.com> - 4.0-2.26.4
- Updated crash.patch such that <asm/page.h> is not #include'd
  by s390_dump.c; IBM did not make the file s390[s] only; BZ #192719

* Mon May 15 2006 Dave Anderson <anderson@redhat.com> - 4.0-2.26.3
- Updated crash.patch such that <asm/page.h> is not #include'd
  by vas_crash.h; only ia64 build complained; BZ #191719

* Mon May 15 2006 Dave Anderson <anderson@redhat.com> - 4.0-2.26.2
- Updated crash.patch such that <asm/segment.h> is not #include'd
  by lkcd_x86_trace.c; also for BZ #191719

* Mon May 15 2006 Dave Anderson <anderson@redhat.com> - 4.0-2.26.1
- Updated crash.patch to bring it up to 4.0-2.26, which should 
  address BZ #191719 - "crash fails to build in mock"

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.0-2.18.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 04 2006 Dave Anderson <anderson@redhat.com> 4.0-2.18
- Updated source package to crash-4.0.tar.gz, and crash.patch
  to bring it up to 4.0-2.18.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Mar 03 2005 Dave Anderson <anderson@redhat.com> 3.10-13
- Compiler error- and warning-related fixes for gcc 4 build.
- Update to enhance x86 and x86_64 gdb disassembly output so as to
  symbolically display call targets from kernel module text without
  requiring module debuginfo data.
- Fix hole where an ia64 vmcore could be mistakenly accepted as a
  usable dumpfile on an x86_64 machine, leading eventually to a
  non-related error message.
* Wed Mar 02 2005 Dave Anderson <anderson@redhat.com> 3.10-12
- rebuild (gcc 4)
* Thu Feb 10 2005 Dave Anderson <anderson@redhat.com> 3.10-9
- Updated source package to crash-3.10.tar.gz, containing
  IBM's final ppc64 processor support for RHEL4
- Fixes potential "bt -a" hang on dumpfile where netdump IPI interrupted
  an x86 process while executing the instructions just after it had entered
  the kernel for a syscall, but before calling the handler.  BZ #139437
- Update to handle backtraces in dumpfiles generated on IA64 with the
  INIT switch (functionality intro'd in RHEL3-U5 kernel).  BZ #139429
- Fix for handling ia64 and x86_64 machines booted with maxcpus=1 on
  an SMP kernel.  BZ #139435
- Update to handle backtraces in dumpfiles generated on x86_64 from the
  NMI exception stack (functionality intro'd in RHEL3-U5 kernel).
- "kmem -[sS]" beefed up to more accurately verify slab cache chains
  and report errors found.
- Fix for ia64 INIT switch-generated backtrace handling when
  init_handler_platform() is inlined into ia64_init_handler();
  properly handles both RHEL3 and RHEL4 kernel patches.
  BZ #138350
- Update to enhance ia64 gdb disassembly output so as to
  symbolically display call targets from kernel module
  text without requiring module debuginfo data.

* Wed Jul 14 2004 Dave Anderson <anderson@redhat.com> 3.8-5
- bump release for fc3

* Tue Jul 13 2004 Dave Anderson <anderson@redhat.com> 3.8-4
- Fix for gcc 3.4.x/gdb issue where vmlinux was mistakenly presumed non-debug 

* Fri Jun 25 2004 Dave Anderson <anderson@redhat.com> 3.8-3
- remove (harmless) error message during ia64 diskdump invocation when
  an SMP system gets booted with maxcpus=1
- several 2.6 kernel specific updates

* Thu Jun 17 2004 Dave Anderson <anderson@redhat.com> 3.8-2
- updated source package to crash-3.8.tar.gz 
- diskdump support
- x86_64 processor support 

* Mon Sep 22 2003 Dave Anderson <anderson@redhat.com> 3.7-5
- make bt recovery code start fix-up only upon reaching first faulting frame

* Fri Sep 19 2003 Dave Anderson <anderson@redhat.com> 3.7-4
- fix "bt -e" and bt recovery code to recognize new __KERNEL_CS and DS

* Wed Sep 10 2003 Dave Anderson <anderson@redhat.com> 3.7-3
- patch to recognize per-cpu GDT changes that redefine __KERNEL_CS and DS

* Wed Sep 10 2003 Dave Anderson <anderson@redhat.com> 3.7-2
- patches for netdump active_set determination and slab info gathering 

* Wed Aug 20 2003 Dave Anderson <anderson@redhat.com> 3.7-1
- updated source package to crash-3.7.tar.gz

* Wed Jul 23 2003 Dave Anderson <anderson@redhat.com> 3.6-1
- removed Packager, Distribution, and Vendor tags
- updated source package to crash-3.6.tar.gz 

* Fri Jul 18 2003 Jay Fenlason <fenlason@redhat.com> 3.5-2
- remove ppc from arch list, since it doesn't work with ppc64 kernels
- remove alpha from the arch list since we don't build it any more

* Fri Jul 18 2003 Matt Wilson <msw@redhat.com> 3.5-1
- use %%defattr(-,root,root)

* Tue Jul 15 2003 Jay Fenlason <fenlason@redhat.com>
- Updated spec file as first step in turning this into a real RPM for taroon.
- Wrote man page.
