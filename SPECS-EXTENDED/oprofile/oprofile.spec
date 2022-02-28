Summary:        System-Wide Profiler for Linux Systems
#
# spec file for package oprofile
#
# Copyright (c) 2021 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
Name:           oprofile
Version:        1.4.0
Release:        3%{?dist}
License:        GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools/Other
URL:            http://oprofile.sourceforge.net/
Source0:        http://prdownloads.sourceforge.net/oprofile/oprofile-%{version}.tar.gz
Source1:        baselibs.conf
Source2:        jvmpi.h
Patch0:         %{name}-no-libjvm-version.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  binutils-devel
BuildRequires:  docbook-utils
BuildRequires:  docbook-xsl-stylesheets
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  javapackages-local-bootstrap
BuildRequires:  libICE-devel
BuildRequires:  libtool
BuildRequires:  libxslt
BuildRequires:  pkgconf
BuildRequires:  popt-devel
BuildRequires:  zlib-devel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%description
OProfile is a system-wide profiler for Linux systems, capable of
profiling all running code at low overhead. OProfile is released under
the GNU GPL.

It consists of a kernel module and a daemon for collecting sample data,
and several post-profiling tools for turning data into information.

OProfile leverages the CPU hardware performance counters to enable
profiling of a wide variety of interesting statistics, which can also
be used for basic time-spent profiling. All code is profiled: hardware
and software interrupt handlers, kernel modules, the kernel, shared
libraries, and applications (the only exception being the oprofile
interrupt handler itself).

OProfile is currently in alpha status; however it has proven stable
over a large number of differing configurations. As always, there is no
warranty.

This is the package containing the userspace tools.

%package        devel
Summary:        Development files for oprofile, a system-wide profiler for Linux
Group:          Development/Libraries/C and C++
Requires:       binutils-devel
Requires:       libopagent1 = %{version}-%{release}

%description devel
OProfile is a system-wide profiler for Linux systems, capable of
profiling all running code at low overhead. OProfile is released under
the GNU GPL.

This package contains the files needed to develop JIT agents for other
virtual machines.

%package -n     libopagent1
Summary:        System-Wide Profiler for Linux Systems
Group:          System/Libraries

%description -n libopagent1
OProfile is a system-wide profiler for Linux systems, capable of
profiling all running code at low overhead. OProfile is released under
the GNU GPL.

This package contains the library needed at runtime when profiling JITed code
from supported virtual machines.

%prep
%autosetup -p1

mkdir -p java/include
# copy files necessary to build Java agent libraries
# libjvmpi_oprofile.so and libjvmti_oprofile.so
test -f %{java_home}/include/jvmpi.h || ln -s %{SOURCE2} %{java_home}/include

%build
./autogen.sh
%configure \
  --with-java=%{java_home}
%make_build

%install
%make_install htmldir=%{_docdir}/oprofile
rm -f %{buildroot}%{_libdir}/oprofile/libopagent.*a
# Hardlink duplicate files automatically (from package fdupes):
# It doesn't save much, but it keeps rpmlint from breaking the package build.
%fdupes %{buildroot}/%{_prefix}

%pre
getent group oprofile >/dev/null || \
	%{_sbindir}/groupadd -r oprofile
getent passwd oprofile >/dev/null || \
	%{_sbindir}/useradd -r -g oprofile -d %{_localstatedir}/lib/empty \
	-s /bin/false -c "Special user account to be used by OProfile" \
	oprofile

%ldconfig_scriptlets

%files
%license COPYING
%doc doc/oprofile.html doc/internals.html doc/opreport.xsd
%doc README TODO ChangeLog-*
%{_bindir}/ocount
%{_bindir}/ophelp
%{_bindir}/opimport
%{_bindir}/opannotate
%{_bindir}/opgprof
%{_bindir}/opreport
%{_bindir}/oparchive
%{_bindir}/opjitconv
%{_bindir}/op-check-perfevents
%{_bindir}/operf
%{_datadir}/oprofile
%{_mandir}/man1/*
%{_libdir}/oprofile/libjvm[tp]i_oprofile.so
%exclude %{_libdir}/oprofile/libjvm[tp]i_oprofile.*a
%{_docdir}/%{name}/ophelp.xsd

%files devel
%{_includedir}/*
%{_docdir}/%{name}/op-jit-devel.html
%dir %{_libdir}/oprofile
%{_libdir}/oprofile/libopagent.so

%files -n libopagent1
%license COPYING
%dir %{_libdir}/oprofile
%{_libdir}/oprofile/libopagent.so.1*

%changelog
* Fri Jan 21 2022 Thomas Crain <thcrain@microsoft.com> - 1.4.0-3
- Pull in javapackages-local-bootstrap as a BR for %%java_home macro definition
- Remove PPC-specific patches, BRs
- Lint spec
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.0-2
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Thu Sep 02 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.0-1.6
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- Replace BR 'docbook-utils-minimal' with 'docbook-utils'.
- Removed workaround for https://lists.opensuse.org/archives/list/factory@lists.opensuse.org/message/2577XBQ4V4PH4IJNYCEEKT4F4KSZ7M46/
  as it was incompatible with CBL-Mariner builds.
- Adjusted search Java home directory to CBL-Mariner.

* Sat Jan 16 2021 Dirk Müller <dmueller@suse.com>
- update to 1.4.0:
  * New/updated Processor Support
  * Marvell (Cavium) ThunderX2
  * Hygon Dhyana CPU
  * Bugfixes
  * Does not build with binutils-gdb master.
  * ocount leaves orphan process on error
- remove oprofile-handle-empty-event-name-spec-gracefully-for-ppc.patch,
  oprofile-handle-binutils-2_34.patch: upstream

* Tue Oct 13 2020 Jan Engelhardt <jengelh@inai.de>
- Do not suppress error text output from useradd.

* Wed Apr  8 2020 Christophe Giboudeaux <christophe@krop.fr>
- Add upstream patch:
  * oprofile-handle-binutils-2_34.patch
- Spec cleanup

* Thu Jan 23 2020 Stefan Brüns <stefan.bruens@rwth-aachen.de>
- Use docbook-utils-minimal for manpage generation, avoids
  texlive dependency.

* Mon Oct 29 2018 Tony Jones <tonyj@suse.com>
- Handle empty event name gracefully on ppc.
  New patch: oprofile-handle-empty-event-name-spec-gracefully-for-ppc.patch

* Thu Jul 26 2018 tonyj@suse.com
- Update to version 1.3.0
  - New/updated Processor Support for Intel Goldmont Plus
  - Minor bug fixes
  Release notes: http://oprofile.sourceforge.net/release-notes/oprofile-1.3.0

* Mon Oct  2 2017 jengelh@inai.de
- Rectify RPM groups. Update summary of -devel subpackage.
  Do not ignore errors from useradd/groupadd.
  Avoid running fdupes across partitions.

* Mon Sep 25 2017 fcrozat@suse.com
- Remove qt-devel from BuildRequires, it is no needed anymore.

* Mon Aug  7 2017 tonyj@suse.com
- Update to version 1.2.0
  - New/updated Processor Support
  * ARM Cortex A17
  * IBM Power 9
  * IBM Power 8NV and NVL variants
  * IBM z13
  * Intel Goldmont
  * Intel Kabylake
  * Intel Xeon Phi (Knights Landing)
  * Achitecture specific events for Applied Micro X-Gene
  - Bug fixes
  * #286 - Compilation error: left shift of negative value
  * #288 - oprofile fails to build with --enable-pch and gcc-6.2
  - Other fixes
  * Fixed compile warning and errors when using GCC 6 or GCC 7
  * Avoid using deprecated readdir_r function
  * Store samples in the archive and search the appropriate places
    for samples
  * Only start the application if the perf events setup was successful
  * Corrections in the code and i386 events so "make check" tests pass
- Drop local patch oprofile-1.1.0-gcc6.patch (upstream)

* Sat May 20 2017 tchvatal@suse.com
- Depend on java-devel instead of deprecated provide

* Sat Mar 11 2017 sfalken@opensuse.org
- Edited %%files to clear unpackaged files builderror in
  openSUSE:Factory

* Sat Jul  2 2016 i@marguerite.su
- add patch: oprofile-1.1.0-gcc6.patch, fixed boo#985359
  * cherry picked upstream commit 39d4d4, so please
    remember to drop it next release
  * GCC 6 is pickier about some of the type conversions
    avoid the intermediate bool type to make it happy

* Fri Dec 25 2015 mpluskal@suse.com
- Update to 1.1.0
  * New/updated Processor Support
    + Broadcom Brahmma-B15 CPU
    + Intel Skylake
    + Intel Airmont
    + Intel Xeon D
  * Bug fixes
    + Prevent dropping of samples when the JVM changes memory
    mappings
    + Better handling of IBM Power JVM generated zero-sized
    mappings
    + Correct handling of anon_hugepage mmap entries for Java
    + Improved oparchive documentation and man page
    + Fixed compile error when using compile fortification
    + Support IBM Power 8 event code larger than sizeof int
    + Avoid changing POSIXLY_CORRECT environment variable for
    processes monitored by operf and ocount
    + Ensure correct setting of the extra bits (edge, inv, cmask)
    for Intel processors
    + Fix default unit masks for Intel Haswell and Broadwell
    processors
    + Correctly initialize operf temporary file header information
- Cleanup spec file with spec-cleaner
- Use url for source
- Drop desktop file since binary it is calling is no longer
  present (at least since version 1.0.0)
- Update dependencies

* Fri Sep 19 2014 tonyj@suse.com
- Update to version 1.0.0. THIS IS A MAJOR OPROFILE RELEASE WITH SIGNIFICANT
  CHANGES FROM THE PREVIOUS 0.9.9 RELEASE.  See changelog below.
    Drop patch: oprofile-add-support-for-intel-silvermont-processor.patch
    Drop patch: oprofile-compressed-kernel.patch
    Drop patch: oprofile-configure-error-message-for-missing-libpfm-is-not-informative-enough.patch
    Drop patch: oprofile-enable-for-new-ppc64le-architecture.patch
    Drop patch: oprofile-fix-unable-to-open-cpu_type-file-for-reading-for-ibm-power7.patch
    Drop patch: oprofile-make-cpu-type-power8e-equivalent-to-power8.patch
  Changelog:
    Major changes:
  - The legacy opcontrol-based profiler has been removed. operf is now the
    only supported interface
  - GUI component (i.e., oprof_start) has been removed.
  - IBS events removed from AMD processors
  - Following architectures have been removed (Alpha [except for EV67 which
    is supported by operf/ocount], avr32, ia64,  IBM Cell,  P.A Semi PA64T)
  - RTV (real time clock) mode has been removed
    Other incompatibilities:
  - Sample data collected with previous releases of OProfile are incompatible
    with release 1.0.
  - ophelp schema: Major version changed for removal of unit mask 'extra'
    attribute and addition of unit mask 'name'.
    New features:
  - Enhance ocount to support millisecond time intervals
  - Obtain kernel symbols from /proc/kallsyms if no vmlinux file specified
  - New Processor Support (Freescale e6500, Freescale e500mc,
    Intel Silvermont, ARMv7 Krait, APM X-Gene (ARMv8),
    Intel Broadwell, ARMv8 Cortex A57, ARMv8 Cortex A53
  - Added little endian support for IBM POWER8
  - Update events for IBM POWER8
  - Added edge-detect events for IBM POWER7
  - Update events for Intel Haswell
  Bug Fixes:
  - opreport schema: Fix count field maxOccurs (changed to 'unbounded')
  - Fix compile error on ppc/uClibc platform: 'AT_BASE_PLATFORM' undeclared'
  - Duplicate event specs passed to ocount show up twice in output
  - Fix operf/ocount default unit mask selection
  - ocount: print the unit mask, kernel and user modes if specified for the
    event
  - ophelp schema is not included in installed files
  - Remove unused 'extra' attribute from ophelp schema
  - opreport from 'operf --callgraph' profile shows false recursive calls
  - Fix handling of default named unit masks longer than 11 chars
  - Print unit mask name where applicable in ophelp XML output
  - Fix profiling of multi-threaded apps when using "--pid" option
  - Fix operf/opreport kernel throttling detection
  - Fix sample attribution problem when using multiple events
  - exclude/include files option doesn't work for opannotate -a
  - Fix behavior and documentation for '--threshold' option
  - Remove hard-coded timeout for JIT dump conversion
  - Update Alpha EV67 CPU support and remove all other Alpha CPU support
  - operf main process improperly killing conversion process
  - Fix up S390 support to work with operf/ocount
  - Link ocount with librt for clock_gettime only when needed
  - Fix 'Invalid argument' running 'opcontrol --start --callgraph=<n>' in
    Timer mode
  - Allow root to remove old jitdump files from /tmp/.oprofile/jitdump
  - Remove opreport warnings for /no-vmlinux, [vdso], [hypervisor_bucket]
    not found
  - Fix event codes for marked architected events (IBM ppc64)
  - Make operf/ocount detect invalid timer mode from opcontrol
  - Reduce overhead of operf waiting for profiled app to end
  - Fix "Unable to open cpu_type file for reading" for IBM POWER7+
  - Allow all native events for IBM POWER8 in POWER7 compat mode
  - Fix spurious "backtraces skipped due to no file mapping" log entries
  - Fix the units for the reported CPU frequency

* Thu Aug 14 2014 tonyj@suse.com
- Add support for Intel Silvermont processor (bnc#891892)
  New patch: oprofile-add-support-for-intel-silvermont-processor.patch

* Thu Mar  6 2014 tonyj@suse.com
- Support ppc64le/power8e (bnc#867091)
  added patches:
  * oprofile-configure-error-message-for-missing-libpfm-is-not-informative-enough.patch
  * oprofile-enable-for-new-ppc64le-architecture.patch
  * oprofile-fix-unable-to-open-cpu_type-file-for-reading-for-ibm-power7.patch
  * oprofile-make-cpu-type-power8e-equivalent-to-power8.patch
  modified patches:
  * oprofile-pfm-ppc.patch

* Wed Aug  7 2013 tonyj@suse.com
- Update to version 0.9.9
  http://oprofile.sourceforge.net/release-notes/oprofile-0.9.9
- New 'ocount' program introduced for collecting raw event counts without
  post processing.
- New processor support for Haswell, zEC12, Power8
- New support for AMD Generic Performance Events and IBM Power ISA 2.07 Architected Events
- Numerous bug fixes.

* Thu Jan  3 2013 tonyj@suse.com
- Add dependancy on libpfm 4.3 for powerpc.
- Add patch 'oprofile-pfm-ppc.patch' (fix configure for 32bit powerpc)

* Mon Dec 10 2012 tonyj@suse.com
- Update to version 0.9.8.
- Support for pre-2.6 kernels has been removed
- The sample data format has changed (see bug #3309794 below for details)
- A new 'operf' program is now available that allows non-root users to profile
  single processes. 'operf' can also be used for system-wide profiling, but
  root authority is required.  This capability requires a kernel version of
  2.6.31 or greater.
- New Processors Support:
  Tilera (tile64 tilepro tile-gx)
  IBM (System z10 z196)
  Intel Ivy Bridge
  ARMv7 (Cortex-A5 Cortex-A15 Cortex-A7)
- Numerous bugfixes

* Fri Nov 25 2011 coolo@suse.com
- add libtool as buildrequire to avoid implicit dependency

* Sat Sep 24 2011 tonyj@suse.com
- Upgrade to version 0.9.7.
- Drop unneeded patches.
- Remove non-utf8 characters from changelog

* Tue May  3 2011 idoenmez@novell.com
- Add oprofile-0.9.6-gcc46.patch to fix compilation with gcc 4.6

* Thu Apr 28 2011 tonyj@novell.com
- Add support for building using qt4 (no bnc)

* Thu Apr 28 2011 tonyj@novell.com
- Add README-BEFORE-ADDING-PATCHES local file documenting required patch
  header

* Tue Jun 29 2010 coolo@novell.com
- fix baselibs.conf

* Thu Jun 24 2010 tonyj@novell.com
- Fix packaging of java agent libs bnc#576533
- Remove unnecessary verbage from %%desc for oprofile-devel and libopagent
- Make %%files of libopagent more specific to avoid future errors

* Wed Feb  3 2010 rguenther@suse.de
- Update to 0.9.6.  Fixes
  * opcontrol cannot start daemon in timer mode
  * Improper handling of separate debuginfo files
  * XML callgraph output has no symbol-level sample counts

* Mon Feb  1 2010 jengelh@medozas.de
- Package baselibs.conf

* Tue Aug  4 2009 tonyj@novell.com
- Update to 0.9.5 - i386/nehalem/events is the only difference from RC2

* Fri Jul 31 2009 jblunck@suse.de
- Remove libopagent static libary. It is used to inject information from a VM
  into the OProfile data and is therefore not suitable for being statically
  linked into the VM itself.

* Wed Jul 29 2009 jblunck@suse.de
- Move libopagent1 to its own package.

* Wed Jul 29 2009 jblunck@suse.de
- Update to version 0.9.5-rc2.

* Wed Jun 10 2009 tonyj@suse.de
- Fix definition clash for basename

* Sun Mar  1 2009 coolo@suse.de
- fix compilation with gcc 4.4

* Thu Nov 20 2008 schwab@suse.de
- Properly handle SPE overlays.

* Wed Nov 19 2008 schwab@suse.de
- Work around broken java support.

* Wed Oct 29 2008 schwab@suse.de
- Fix uninitialized variable.

* Thu Oct 23 2008 schwab@suse.de
- Ignore section symbols.

* Tue Oct 21 2008 schwab@suse.de
- Fix jvm agent libs.

* Fri Jul 18 2008 schwab@suse.de
- Update to oprofile 0.9.4.
  http://oprofile.sourceforge.net/release-notes/oprofile-0.9.4

* Fri Jul 11 2008 schwab@suse.de
- Update binutils check.

* Mon Nov 26 2007 schwab@suse.de
- Fix open call.

* Tue Oct 16 2007 schwab@suse.de
- Fix event mapping on 970MP [#333487].

* Thu Oct 11 2007 schwab@suse.de
- Fix missing includes.

* Tue Jul 17 2007 schwab@suse.de
- Update to oprofile 0.9.3.

* Wed Jul  4 2007 schwab@suse.de
- Update to oprofile 0.9.3-rc2.

* Mon Jun 18 2007 schwab@suse.de
- Update to oprofile 0.9.3-rc1.

* Thu Jan 11 2007 schwab@suse.de
- Add binutils-devel to BuildRequires.

* Mon Sep 18 2006 schwab@suse.de
- Update to oprofile 0.9.2 (no summary available).

* Fri Aug 18 2006 schwab@suse.de
- Avoid crash in find_nearest_line [#193622].

* Wed May 31 2006 schwab@suse.de
- Fix invalid string operation.

* Thu May  4 2006 schwab@suse.de
- Fix last change.

* Mon Feb 27 2006 schwab@suse.de
- Add events for Power5+ [#152494].

* Fri Jan 27 2006 mls@suse.de
- converted neededforbuild to BuildRequires

* Wed Jan 25 2006 schwab@suse.de
- Integrate fixes for ppc64 events and groups [#130910, #137665].

* Mon Dec 12 2005 schwab@suse.de
- Update to oprofile 0.9.1.

* Tue Nov  8 2005 dmueller@suse.de
- don't build as root

* Wed Sep 28 2005 schwab@suse.de
- Fix invalid C++.

* Wed Jul  6 2005 schwab@suse.de
- Unpack compressed vmlinux [#52767].
- Use RPM_OPT_FLAGS.

* Tue Jun  7 2005 schwab@suse.de
- Update to oprofile 0.9.

* Thu Mar 24 2005 schwab@suse.de
- Update to oprofile 0.8.2.

* Thu Nov  4 2004 schwab@suse.de
- Update to oprofile 0.8.1.

* Fri Sep  3 2004 schwab@suse.de
- Update to oprofile 0.8.

* Mon Jun 28 2004 skh@suse.de
- more fixes for #40468
  - fixed print statement in op_help.c
  - more power 4 events
  - fixed incorrect event counter settings for power 4

* Tue Jun  8 2004 skh@suse.de
- Update to fix for #40468: use correct event numbers for power5
  events.

* Wed May 26 2004 skh@suse.de
- Added default CYCLES event to the Power 4 and Power 5 event
  files. (#40468)

* Tue May 25 2004 skh@suse.de
- add user space support for ppc64 (#40468)

* Sun May  9 2004 ak@suse.de
- Increase minimum count on P4 to 5000 for all events
- Automatically add the module path of the current kernel to oprofpp
  (#36825)
- Fix 64bit uncleanness in symbol resolution (#36825)

* Sat Apr 10 2004 aj@suse.de
- Remove kernel-source requirement.

* Wed Feb  4 2004 skh@suse.de
- Updated to version 0.7.1
- Removed subpackage km_oprofile (it is part of the main kernel
  distribution as of kernel 2.6)
- Don't build as root.

* Mon Oct  6 2003 ak@suse.de
- Check if APIC is enabled instead of crashing (#31774)
  Needs updated kernel.

* Sat Aug 16 2003 adrian@suse.de
- add desktop file

* Thu Jul 31 2003 skh@suse.de
- Updated to 0.6

* Fri Jun 20 2003 mmj@suse.de
- Up to 0.5.4

* Fri Jun 13 2003 mmj@suse.de
- Package all dirs

* Wed Jun  4 2003 mmj@suse.de
- Make sure we get the right location for qt.

* Wed May 28 2003 mmj@suse.de
- Update to 0.5.3

* Tue May 13 2003 mmj@suse.de
- Use %%defattr
- Package forgotten files

* Mon Mar 31 2003 mmj@suse.de
- Update to 0.5.2 including:
  · Docu overhaul
  · Feature additions
- Bzip2'ed sources
- Folded both automake patches into one patch

* Tue Mar 11 2003 kukuk@suse.de
- Don't call depmod

* Mon Mar 10 2003 ro@suse.de
- remove k_deflt from neededforbuild (cycle)

* Mon Mar 10 2003 mmj@suse.de
- Fix typo

* Fri Mar  7 2003 mmj@suse.de
- A go at fixing km_oprofile

* Mon Mar  3 2003 duwe@suse.de
- split off km_oprofile
- tiny version update includes patches

* Mon Feb 24 2003 mmj@suse.de
- Add patch from davej to make it not crash the box

* Sat Feb 15 2003 adrian@suse.de
- minor dependency clean up

* Fri Feb  7 2003 mmj@suse.de
- Really fix build on x86_64

* Tue Feb  4 2003 mmj@suse.de
- Fix build on x86_64

* Tue Feb  4 2003 mmj@suse.de
- Update to oprofile 0.5:
  · Pentium IV support, including support for HyperThreading, is
    supported for 2.5 kernels (currently only in the -mm patchset).
  · Timer interrupt support for PA-RISC, ppc64, and sparc64 in 2.5
    kernels is available. Userspace Alpha support has been added.
  · HyperThreading support for Pentium IV on 2.4 kernels is not yet
    available. Note that PA-RISC and Alpha require kernel patches
    not yet available in a released kernel tree.
  · Support for the IA-64 architecture has been added for 2.4 kernels.
  · OProfile's userspace now works correctly on all 64-bit platforms.
  · A new script, opcontrol, has been added to unify control of the
    OProfile daemon and sample files. On 2.5, this allows separate
    daemon startup and starting/stopping profiling.
  · Fixed upstream to compile with gcc 3.3
  · Several bugfixes

* Wed Jan 29 2003 ro@suse.de
- fix build with gcc-3.3 (sluggish c++)

* Thu Nov  7 2002 mmj@suse.de
- Update to 0.4 which now has kernel 2.5 support

* Thu Sep 12 2002 mmj@suse.de
- Initial package, version 0.3 (x86 only for now)
