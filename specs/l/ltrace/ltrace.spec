# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Tracks runtime library calls from dynamically linked executables
Name: ltrace
Version: 0.7.91
Release: 53%{?dist}
# In coordination with Juan Céspedes, upstream is now officially on gitlab.
# We are going to being sending all of our Fedora patches upstream to gitlab.
URL: https://gitlab.com/cespedes/ltrace
License: GPL-2.0-or-later

BuildRequires: elfutils-devel dejagnu
BuildRequires: libselinux-devel
BuildRequires: autoconf automake libtool
BuildRequires: gcc-c++
BuildRequires: make

# Note: this URL needs to be updated for each release, as the file
# number changes for each file.  Full list of released files is at:
#  https://alioth.debian.org/frs/?group_id=30892
Source: ltrace-%{version}.tar.bz2

# Merge of several upstream commits that fixes compilation on ARM.
Patch0: ltrace-0.7.91-arm.patch

# Upstream patch that fixes accounting of exec, __libc_start_main and
# others in -c output.
Patch1: ltrace-0.7.91-account_execl.patch

# Upstream patch that fixes interpretation of PLT on x86_64 when
# IRELATIVE slots are present.
Patch2: ltrace-0.7.91-x86_64-irelative.patch

# Upstream patch that fixes fetching of system call arguments on s390.
Patch3: ltrace-0.7.91-s390-fetch-syscall.patch

# Upstream patch that enables tracing of IRELATIVE PLT slots on s390.
Patch4: ltrace-0.7.91-s390-irelative.patch

# Fix for a regression in tracing across fork.  Upstream patch.
Patch5: ltrace-0.7.91-ppc64-fork.patch

# Fix crashing a prelinked PPC64 binary which makes PLT calls through
# slots that ltrace doesn't trace.
# https://bugzilla.redhat.com/show_bug.cgi?id=1051221
Patch6: ltrace-0.7.91-breakpoint-on_install.patch
Patch7: ltrace-0.7.91-ppc64-unprelink.patch

# Man page nits.  Backport of an upstream patch.
Patch8: ltrace-0.7.91-man.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1044766
Patch9: ltrace-0.7.91-cant_open.patch

# Support Aarch64 architecture.
Patch10: ltrace-0.7.91-aarch64.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1064406
Patch11: ltrace-0.7.2-e_machine.patch

# Support for ppc64le, backported from upstream.
# http://anonscm.debian.org/gitweb/?p=collab-maint/ltrace.git;a=commit;h=eea4ad2cce289753aaa35b4e0258a76d8f8f367c
# https://bugzilla.redhat.com/show_bug.cgi?id=1131956
Patch13: ltrace-0.7.91-ppc64le-support.patch
# 35a9677dc9dcb7909ebd28f30200474d7e8b660f,
# 437d2377119036346f4dbd93039c847b4cc9d0be,
# eb3993420734f091cde9a6053ca6b4edcf9ae334
Patch14: ltrace-0.7.91-ppc64le-fixes.patch

# http://anonscm.debian.org/gitweb/?p=collab-maint/ltrace.git;a=commit;h=2e9f9f1f5d0fb223b109429b9c904504b7f638e2
# http://anonscm.debian.org/gitweb/?p=collab-maint/ltrace.git;a=commit;h=f96635a03b3868057db5c2d7972d5533e2068345
Patch15: ltrace-0.7.91-parser-ws_after_id.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1171165
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=d8f1287b85e2c2b2ae0235809e956f4365e53c45
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=d80c5371454383e3f9978622e5578cf02af8c44c
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=bf82100966deda9c7d26ad085d97c08126a8ae88
Patch16: ltrace-0.7.91-ppc-bias.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1158714
Patch17: ltrace-0.7.91-x86-plt_map.patch
Patch18: ltrace-0.7.91-x86-unused_label.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1170315
Patch19: ltrace-0.7.91-unwind-elfutils.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1208351
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=4724bd5a4a19db117a1d280b9d1a3508fd4e03fa
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=72ee29639c55b5942bc07c8ed0013005f8fc5a97
Patch20: ltrace-0.7.91-multithread-no-f-1.patch
Patch21: ltrace-0.7.91-multithread-no-f-2.patch

# Fix problems with building a number of test cases.
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=694d19ff14017926454771cbb63a22355b72f1bf
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=a3a03622fb4ca9772dca13eae724a94ba1e728f4
Patch22: ltrace-0.7.91-testsuite-includes.patch
Patch23: ltrace-0.7.91-testsuite-includes-2.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1210653
# http://anonscm.debian.org/cgit/collab-maint/ltrace.git/commit/?id=eea6091f8672b01f7f022b0fc367e0f568225ffc
Patch24: ltrace-0.7.91-ppc64le-configure.patch

Patch25: ltrace-rh1307754.patch

# GCC now warns (errors) on "tautological compares", and readdir_r is deprecated.
Patch26: ltrace-0.7.91-tautology.patch

# ARM code has unreachable code after switch statement, move initialization
Patch27: ltrace-rh1423913.patch

# AARCH64 large parameters and syscall testsuite fixes.
Patch28: ltrace-0.7.91-aarch64-params.patch

# gcc-9 fix.  Avoid passing NULL as argument to %s
Patch29: ltrace-0.7.91-null.patch

# Adds support for CET PLTs via second-plt lookups.
Patch30: ltrace-0.7.91-cet.patch

# Extra #includes for gcc 9
Patch31: ltrace-0.7.91-aarch64-headers.patch
# Testsuite: AARCH64 ifuncs not supported yet yet.
Patch32: ltrace-rh1225568.patch

# testsuite fixes for pre-installed config files
Patch33: ltrace-0.7.91-testsuite-system_call_params.patch

# Ignore bogus files from the environment
Patch34: ltrace-0.7.91-XDG_CONFIG_DIRS.patch

# GCC erroneously warns about uninitialized values
Patch35: ltrace-0.7.91-rh1799619.patch

# Support for both SC and SCV sycall insns
Patch36: ltrace-0.7.91-ppc64le-scv.patch

Patch37: ltrace-0.7.91-W-use-after-free.patch

%description
Ltrace is a debugging program which runs a specified command until the
command exits.  While the command is executing, ltrace intercepts and
records both the dynamic library calls called by the executed process
and the signals received by the executed process.  Ltrace can also
intercept and print system calls executed by the process.

You should install ltrace if you need a sysadmin tool for tracking the
execution of processes.

%prep
%setup -q -n %{name}-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1
%patch -P11 -p1
%patch -P13 -p1
%patch -P14 -p1
%patch -P15 -p1
%patch -P16 -p1
%patch -P17 -p1
%patch -P18 -p1
%patch -P19 -p1
%patch -P20 -p1
%patch -P21 -p1
%patch -P22 -p1
%patch -P23 -p1
%patch -P24 -p1
%patch -P25 -p1
%patch -P26 -p1
%patch -P27 -p1
%patch -P28 -p1
%patch -P29 -p1
%patch -P30 -p1
%patch -P31 -p1
%patch -P32 -p1
%patch -P33 -p1
%patch -P34 -p1
%patch -P35 -p1
%patch -P36 -p1
%patch -P37 -p1

%build
autoreconf -i
%configure --docdir=%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
%make_build

%install
%make_install bindir=%{_bindir}

# The testsuite is useful for development in real world, but fails in
# koji for some reason.  Disable it, but have it handy.
%check
echo ====================TESTING=========================
# The ppc64 testsuite hangs rpmbuild hard in koji, disable until fixed.
%ifnarch ppc64le
timeout 180 make check ||:
%endif
echo ====================TESTING END=====================

%files
%doc NEWS COPYING CREDITS INSTALL README TODO
%{_bindir}/ltrace
%{_mandir}/man1/ltrace.1*
%{_mandir}/man5/ltrace.conf.5*
%{_datadir}/ltrace

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 03 2022 Carlos O'Donell <carlos@redhat.com> - 0.7.91-45
- Rebuild ltrace for rawhide (#2046722)

* Thu Jan 27 2022 DJ Delorie <dj@redhat.com> - 0.7.91-44
- Fix use-after-free cases.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb  8 2021 DJ Delorie <dj@redhat.com> - 0.7.91-41
- Add support for SCV syscall insn for ppc64le

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 0.7.91-38
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Feb  6 2020 DJ Delorie <dj@redhat.com> - 0.7.91-37
- Initialize some variables to avoid gcc warning (#1799619)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jul 23 2019 DJ Delorie <dj@redhat.com> - 0.7.91-35
- Skip ppc64 testsuite until the hangs in koji can be fixed.

* Wed Jul 17 2019 DJ Delorie <dj@redhat.com> - 0.7.91-34
- Add fixes in handling of bogus paths that come from XDG_CONFIG_DIRS.
- Testsuite fixes for pre-installed config files.
- Extra AARCH64 includes for gcc 9.
- Testsuite: AARCH64 ifuncs not supported yet yet.

* Thu Apr 4 2019 DJ Delorie <dj@redhat.com> - 0.7.91-33
- Add Intel CET support.

* Tue Mar 12 2019 DJ Delorie <dj@redhat.com> - 0.7.91-32
- Revert previous patch, redundant

* Tue Mar 5 2019 Eugene Syromiatnikov <esyr@redhat.com> - 0.7.91-31
- Fix "Too many return value classes" assert

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Jeff Law <law@redhat.com> - 0.7.91-29
- Avoid passing NULL as argument to %s in printf call

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 DJ Delorie <dj@redhat.com> - 0.7.91-27
- Fix aarch64 long parameters (via $r8) support.
- Make system_call_params test compare more exactly.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.91-26
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 Jeff Law <law@redhat.com.org> - 0.7.91-22
- Fix FTBFS due to invalid code in ARM support (#1423913).

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 20 2016 DJ Delorie <dj@redhat.com> - 0.7.91-20
- Fix FTBFS due to new gcc 6 warnings, deprecated readdir_r, and bogus chunk in unwind-elf patch.

* Fri Feb 19 2016 Jeff Law <law@redhat.com.org> - 0.7.91-19
- Fix FTBFS due to testsuite failure (#1307754) .  Add missing files to %%doc

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.91-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.91-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 13 2015 Petr Machata <pmachata@redhat.com> - 0.7.91-16
- Add upstream fix to map of powerpc64le architecture to ppc backend.
  (ltrace-0.7.91-ppc64le-configure.patch)

* Wed Apr  8 2015 Petr Machata <pmachata@redhat.com> - 0.7.91-15
- Add upstream fixes for compilation of test cases
  (ltrace-0.7.91-testsuite-includes.patch,
  ltrace-0.7.91-testsuite-includes-2.patch)

* Wed Apr  8 2015 Petr Machata <pmachata@redhat.com> - 0.7.91-14
- Add upstream fixes for tracing multi-threaded processes without -f
  (ltrace-0.7.91-multithread-no-f-1.patch,
  ltrace-0.7.91-multithread-no-f-2.patch)

* Fri Jan  9 2015 Petr Machata <pmachata@redhat.com> - 0.7.91-13
- Add upstream fix for support of elfutils unwinder
  (ltrace-0.7.91-unwind-elfutils.patch)

* Wed Jan  7 2015 Petr Machata <pmachata@redhat.com> - 0.7.91-12
- Add upstream fix for a bug in labeling PLT slots
  (ltrace-0.7.91-x86-plt_map.patch)

* Tue Dec  9 2014 Petr Machata <pmachata@redhat.com> - 0.7.91-11
- Fix bias handling in PPC backend
- Fix cloning of unresolved breakpoints in PPC backend
  (ltrace-0.7.91-ppc-bias.patch)

* Wed Aug 20 2014 Petr Machata <pmachata@redhat.com> - 0.7.91-10
- Backported PowerPC64 ELFv2 support.
  (ltrace-0.7.91-ppc64le-support.patch,
  ltrace-0.7.91-ppc64le-fixes.patch)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.91-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.91-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 13 2014 Petr Machata <pmachata@redhat.com> - 0.7.91-7
- Add an upstream patch that fixes missed initialization of some
  fields in struct process after atteching to a multi-threaded
  process.  (ltrace-0.7.2-e_machine.patch)
- Add upstream patch-set that implements support for the new aarch64
  architecture.  (ltrace-0.7.91-aarch64.patch)

* Tue Jan 14 2014 Petr Machata <pmachata@redhat.com> - 0.7.91-6
- Fix a problem when an invalid command has been found
  (ltrace-0.7.91-cant_open.patch)

* Tue Jan 14 2014 Petr Machata <pmachata@redhat.com> - 0.7.91-5
- Fix interpretation of x86_64 PLT with IRELATIVE slots.
  (ltrace-0.7.91-x86_64-irelative.patch)
- Fix fetching of system call arguments on s390.
  (ltrace-0.7.91-s390-fetch-syscall.patch)
- Enable tracing of IRELATIVE PLT slots on s390.
  (ltrace-0.7.91-s390-irelative.patch)
- Fix a couple nits in ltrace.1 (ltrace-0.7.91-man.patch)

* Fri Jan 10 2014 Petr Machata <pmachata@redhat.com> - 0.7.91-4
- Fix crashing a prelinked PPC64 binary which makes PLT calls through
  slots that ltrace doesn't trace.
  (ltrace-0.7.91-breakpoint-on_install.patch,
  ltrace-0.7.91-ppc64-unprelink.patch)

* Thu Jan  9 2014 Petr Machata <pmachata@redhat.com> - 0.7.91-3
- Fix a problem in tracing across fork on PPC64
  (ltrace-0.7.91-ppc64-fork.patch)

* Thu Nov 21 2013 Petr Machata <pmachata@redhat.com> - 0.7.91-2
- Fix a problem in including in summary (-c) function calls that don't
  finish before exec or exit (ltrace-0.7.91-account_execl.patch)

* Tue Nov  5 2013 Petr Machata <pmachata@redhat.com> - 0.7.91-1
- Rebase to a pre-release 0.8
- Drop BR on autoconf and friends

* Wed Aug  7 2013 Ville Skyttä <ville.skytta@iki.fi> - 0.7.2-7
- Install docs to %%{_pkgdocdir} where available (#992149).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Petr Machata <pmachata@redhat.com> - 0.7.2-5
- On s390, the highest bit in PC address is used to distinguish
  between 24-bit and 31-bit addressing modes.  Linux used to do this
  for us, but not anymore.
  (ltrace-0.7.2-s390-set_instruction_pointer.patch)

* Wed Feb  6 2013 Petr Machata <pmachata@redhat.com> - 0.7.2-4
- Update the ARM patch (ltrace-0.7.2-arm.patch) with support for
  parameter passing conventions.

* Thu Jan 31 2013 Petr Machata <pmachata@redhat.com> - 0.7.2-3
- Bring small fixes from master branch
  (ltrace-0.7.2-bits.patch; drop ltrace-0.7.2-man.patch)
- Add a patch that implements ARM sofware singlestepping.  This mostly
  fixes test suite on ARM, though parameter passing conventions are
  still not implemented.  (ltrace-0.7.2-arm.patch)
- Work around a new GCC warning (ltrace-0.7.2-unused-typedef.patch)

* Fri Jan 11 2013 Petr Machata <pmachata@redhat.com> - 0.7.2-2
- Improve documentation: better correlation between ltrace(1) and
  --help, other minor improvements in ltrace(1).
  (ltrace-0.7.2-man.patch)

* Mon Dec 10 2012 Petr Machata <pmachata@redhat.com> - 0.7.2-1
- Upstream 0.7.2
  - Drop all the patches

* Sat Nov 10 2012 Petr Machata <pmachata@redhat.com> - 0.7.0-1
- Upstream 0.7.0
  - Drop all the patches
  - Upstream patch for missing sysdeps/linux-gnu/ppc/insn.h
    (ltrace-0.7.0-ppc-insn.h.patch)
  - Upstream patch for installing ltrace.conf.5 to man5
    (ltrace-0.7.0-man5.patch)

* Mon Oct  1 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-19
- Upstream patch for ia64 parameter passing
  (ltrace-0.6.0-abi-ia64.patch)
- Upstream fix for a bug in computation of time spent in a syscall
  (ltrace-0.6.0-syscall-time.patch)
- Upstream fix for a bug in passing struct(float,struct(float,float))
  on x86_64 (ltrace-0.6.0-x86_64-flatten.patch)
- Upstream patch for support of -l option (ltrace-0.6.0-dash-l.patch)
- Several more upstream patches with random cleanups.  Those were
  brought to Fedora to make porting of other patches easier.
  (ltrace-0.6.0-cleanups.patch)

* Thu Aug 30 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-18
- PPC64 passes floating point equivalent structures in registers

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun  1 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-16
- Look for __cxa_demangle in libstdc++ as well
- Demangle test case should report it's unsupported if demangling
  support isn't compiled in (ltrace-0.6.0-demangle.patch)
- Resolves: #827422

* Thu May 31 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-15
- Add upstream patches for parameter passing.  Apart from a couple of
  fixes, this brings in s390 support (ltrace-0.6.0-abi-s390.patch)

* Fri May 18 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-14
- Add upstream patch that improves parameter passing support (the
  upstream "revamp" branch) (ltrace-0.6.0-abi.patch)

* Thu May  3 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-13
- Check -n argument for validity (ltrace-0.6.0-dash-n.patch)
- Resolves: #818529
- ltrace-0.6.0-libs-fixes-1.patch
  - Fix double free when process initialization fails for some reason
  - Don't indent first level of calls

* Mon Apr 30 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-12
- Fix 32-bit builds

* Mon Apr 30 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-11
- Fix detach from sleeping process
- Add limited support for return from tail call
- Fix singlestep over atomic instruction sequence on PPC
- Add extensive upstream patch that implements
  - tracing calls done from DSOs
  - better tools for filtering symbol tables
  - support for tracing PLT calls on PPC64 (not entry points read from .plt)
  - support for PPC32 old-style (BSS) PLT table
- Drop ppc-shift patch that was superseded by the above
- Drop demangle patch that hasn't been applied for some time now

* Wed Apr 11 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.0-10
- Drop ExclusiveArch as all current Primary/Secondary Arches are supported

* Wed Apr 11 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-9
- And patch configure and config.h, not just configure.ac
- Resolves: #810973

* Wed Apr 11 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-7
- Add libselinux-devel BR
- Resolves: #810973

* Tue Apr 10 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-6
- If we fail to attach to traced process, check whether deny_ptrace
  isn't enabled.  If yes, warn about it.
- Resolves: #810973

* Tue Feb  7 2012 Petr Machata <pmachata@redhat.com> - 0.6.0-5
- Add upstream patches for initial breakpoint insertion.  This mostly
  fixes tracing on PPC.
- Resolves: #773050

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Petr Machata <pmachata@redhat.com> - 0.6.0-3
- Add several upstream patches that fix various races in tracing
  multi-threaded processes
- Add upstream patches for support of tracing across vfork
- Add upstream patches for ppc: excessive shift, and fetching
  function arguments

* Fri Sep  2 2011 Petr Machata <pmachata@redhat.com> - 0.6.0-2
- Add upstream patches for tracing multi-threaded processes, endian
  fixes, and a test suite fixlet

* Tue Feb 15 2011 Petr Machata <pmachata@redhat.com> - 0.6.0-1
- Update to 0.6.0
  - Drop most patches
  - Port exec-stripped patch
  - Add return-string-n patch
  - Leave just the testsuite part in ia64-sigill patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-19.45svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  9 2010 Petr Machata <pmachata@redhat.com> - 0.5-18.45svn
- Add memmove to /etc/ltrace.conf
- Resolves: #658311

* Wed Sep  8 2010 Petr Machata <pmachata@redhat.com> - 0.5-17.45svn
- Fix demangler resolution.  Libiberty is not in the default install
  anymore, and the fallback configure check for __cxa_demangle doesn't
  take into account the possibility that the symbol might be in
  libstdc++ instead.
- Resolves: #631069 FTBFS

* Wed May 19 2010 Petr Machata <pmachata@redhat.com> - 0.5-16.45svn.1
- When the value of undefined symbol in PPC 32-bit binary is 0, use
  PPC-specific magic to compute the PLT slots.
- Fix a problem with tracing stripped binary after execl on
  architectures that need PLT reinitalisation breakpoint.
- Support tracing of 31-bit binaries with 64-bit ltrace
- Fix handling of the case where forked child is reported before
  parent's fork event
- Patch from Supriya Kannery implements fetching 5th and further
  function arguments on s390

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-14.45svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-13.45svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct  7 2008 Petr Machata <pmachata@redhat.com> - 0.5-12.45svn
- Fix fork & exec patches to apply cleanly under --fuzz=0
- Resolves: #465036

* Fri May 23 2008 Petr Machata <pmachata@redhat.com> - 0.5-11.45svn
- Patch from James M. Leddy, fixes interaction of -c and -o
- Fix compilation by using -D_LARGEFILE64_SOURCE
- related: #447404

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.5-10.45svn
- Autorebuild for GCC 4.3

* Wed Sep 12 2007 Petr Machata <pmachata@redhat.com> - 0.5-9.45svn
- Cleanup spec.
- Fix parallel make bug in Makefile.
- resolves: #226109

* Thu Aug 16 2007 Petr Machata <pmachata@redhat.com> - 0.5-8.45svn
- Fix licensing tag.

* Fri May  4 2007 Petr Machata <pmachata@redhat.com> - 0.5-7.45svn
- added fork/exec patches, mostly IBM's work
- added trace-exec tests into suite
- added ia64 sigill patch

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 0.5-6.45svn
- tidy up the specfile per rpmlint comments
- fix man page

* Mon Sep  4 2006 Petr Machata <pmachata@redhat.com> - 0.5-5.45svn
- fix plt handling on ppc32 (symval patch)
- fix attaching to process (attach patch)
- add fork & exec patches from IBM
- adjust weak symbol handling (ppc32fc5 patch)

* Wed Aug 23 2006 Petr Machata <pmachata@redhat.com> - 0.5-3.45svn
- use "{X}.{release}svn" release string per naming guidelines

* Tue Aug 22 2006 Petr Machata <pmachata@redhat.com> - 0.5-1.1.45svn
- using dist tag

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 0.5-1.0.45svn.6
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Fri Jul 14 2006 Petr Machata <pmachata@redhat.com> - 0.5-1.0.45svn.5
- adding .gnu.hash patch to support new ELF hash table section
- adding testsuite patch to silent some bogus failures

* Fri Jul 14 2006 Petr Machata <pmachata@redhat.com> - 0.5-1.0.45svn
- adding upstream (svn) version.  It contains most of patches that we
  already use, and has support for secure PLTs.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.4-1.7.1
- rebuild

* Wed Jun 14 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.7
- drop broken ppc support

* Thu Jun  1 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.6
- e_entry patch: use elf's e_entry field instead of looking up _start
  symbol, which failed on stripped binaries.

* Wed May  3 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.5
- Correct a typo that prevented the inclusion of "demangle.h"
- Adding -Wl,-z,relro

* Mon Apr 24 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.4
- turn off opd translation on ia64, GElf already gives us function
  address.
- turn on main-internal test, it should pass now.

* Wed Apr 12 2006 Petr Machata <pmachata@redhat.com> - 0.4-1.2
- svn fix for opt_x patch
- patches for testsuite for s390{,x}
- turning off main-internal test. Fails on ia64, needs investigation.

* Fri Apr  7 2006 Petr Machata <pmachata@redhat.com> - 0.4-1
- Upstream 0.4
- opt_x patch: New structure for opt_x list elements, now with
  'found'.  Using it in options.c, elf.c.
- testsuite patch: Automated testsuite for ltrace.

* Wed Mar  1 2006 Petr Machata  <pmachata@redhat.com> - 0.3.36-4.3
- include %%{ix86} to ExclusiveArch, instead of mere i386

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.3.36-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.3.36-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan  9 2006 Jakub Jelinek <jakub@redhat.com> 0.3.36-4
- added ppc64 and s390x support (IBM)
- added ia64 support (Ian Wienand)

* Sat Mar  5 2005 Jakub Jelinek <jakub@redhat.com> 0.3.36-3
- rebuilt with GCC 4

* Tue Dec 14 2004 Jakub Jelinek <jakub@redhat.com> 0.3.36-2
- make x86_64 ltrace trace both 32-bit and 64-bit binaries (#141955,
  IT#55600)
- fix tracing across execve
- fix printf-style format handling on 64-bit arches

* Thu Nov 18 2004 Jakub Jelinek <jakub@redhat.com> 0.3.36-1
- update to 0.3.36

* Mon Oct 11 2004 Jakub Jelinek <jakub@redhat.com> 0.3.35-1
- update to 0.3.35
- update syscall tables from latest kernel source

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  8 2004 Jakub Jelinek <jakub@redhat.com> 0.3.32-3
- buildreq elfutils-libelf-devel (#124921)

* Thu Apr 22 2004 Jakub Jelinek <jakub@redhat.com> 0.3.32-2
- fix demangling

* Thu Apr 22 2004 Jakub Jelinek <jakub@redhat.com> 0.3.32-1
- update to 0.3.32
  - fix dict.c assertion (#114359)
  - x86_64 support
- rewrite elf.[ch] using libelf
- don't rely on st_value of SHN_UNDEF symbols in binaries,
  instead walk .rel{,a}.plt and compute the addresses (#115299)
- fix x86-64 support
- some ltrace.conf additions
- some format string printing fixes

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb  3 2003 Jakub Jelinek <jakub@redhat.com> 0.3.29-1
- update to 0.3.29

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Sep  1 2002 Jakub Jelinek <jakub@redhat.com> 0.3.10-12
- add a bunch of missing functions to ltrace.conf
  (like strlen, ugh)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 28 2002 Phil Knirsch <pknirsch@redhat.com>
- Added the 'official' s390 patch.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jul 20 2001 Jakub Jelinek <jakub@redhat.com>
- fix stale symlink in documentation directory (#47749)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Aug  2 2000 Tim Waugh <twaugh@redhat.com>
- fix off-by-one problem in checking syscall number

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Matt Wilson <msw@redhat.com>
- rebuilt for next release
- patched Makefile.in to take a hint on mandir (patch2)
- use %%{_mandir} and %%makeinstall

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Fri Jan  7 2000 Jeff Johnson <jbj@redhat.com>
- update to 0.3.10.
- include (but don't apply) sparc patch from Jakub Jellinek.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Fri Mar 12 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.3.6.

* Mon Sep 21 1998 Preston Brown <pbrown@redhat.com>
- upgraded to 0.3.4
