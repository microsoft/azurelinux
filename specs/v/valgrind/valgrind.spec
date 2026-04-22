# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?scl:%scl_package valgrind}

Summary: Dynamic analysis tools to detect memory or thread bugs and profile
Name: %{?scl_prefix}valgrind
Version: 3.26.0
Release: 6%{?dist}
Epoch: 1

# This ignores licenses that are only found in the test or perf sources
# we only care about those license statements found in sources that end
# up in the binary packages. One piece of code for which we don't have
# a license specifier is in coregrind/m_main.c for some Hacker's Delight
# public domain code, which is only compiled into Darwin binaries, which
# we don't create. Also some subpackages have their own license tags.
License: GPL-3.0-or-later AND bzip2-1.0.6 AND (GPL-3.0-or-later AND LGPL-2.0-or-later) AND (GPL-3.0-or-later AND ISC) AND (GPL-3.0-or-later AND Unlicense) AND (GPL-3.0-or-later AND Zlib) AND (GPL-3.0-or-later WITH GCC-exception-2.0) AND (LGPL-2.0-or-later WITH GCC-exception-2.0) AND (GPL-3.0-or-later AND BSD-3-Clause) AND (GPL-3.0-or-later AND (MIT OR NCSA)) AND CMU-Mach AND (GPL-3.0-or-later AND X11 AND BSD-3-Clause) AND X11 AND (GPL-3.0-or-later AND LGPL-2.0-or-later) AND (GPL-2.0-or-later WITH Autoconf-exception-generic) AND (GPL-3.0-or-later WITH Autoconf-exception-generic-3.0) AND FSFULLR AND FSFAP AND FSFUL AND FSFULLRWD
URL: https://www.valgrind.org/

# Are we building for a Software Collection?
%{?scl:%global is_scl 1}
%{!?scl:%global is_scl 0}

# We never want the openmpi subpackage when building a software collecton.
# We always want it for fedora.
# We only want it for older rhel.
# And on fedora > 39 i386 dropped openmpi.
%if %{is_scl}
  %global build_openmpi 0
%else
  %if 0%{?fedora}
    %ifarch %{ix86}
      %global build_openmpi (%{?fedora} < 40)
    %else
      %global build_openmpi 1
    %endif
  %endif
  %if 0%{?rhel}
    %if 0%{?rhel} > 7
      %global build_openmpi 0
    %else
      %global build_openmpi 1
    %endif
  %endif
%endif

# We only want to build the valgrind-tools-devel package for Fedora proper
# as convenience. But not for DTS or RHEL.
%if %{is_scl}
  %global build_tools_devel 0
%else
  %if 0%{?rhel}
    %global build_tools_devel 0
  %else
    %global build_tools_devel 1
  %endif
%endif

# Whether to run the full regtest or only a limited set
# The full regtest includes gdb_server integration tests
# and experimental tools.
# Don't run them when creating scl, the gdb_server tests might hang.
%if %{is_scl}
  %global run_full_regtest 0
%else
  %global run_full_regtest 1
%endif

# Generating minisymtabs doesn't really work for the staticly linked
# tools. Note (below) that we don't strip the vgpreload libraries at all
# because valgrind might read and need the debuginfo in those (client)
# libraries for better error reporting and sometimes correctly unwinding.
# So those will already have their full symbol table.
%undefine _include_minidebuginfo

Source0: https://sourceware.org/pub/valgrind/valgrind-%{version}.tar.bz2

# Needs investigation and pushing upstream
Patch1: valgrind-3.9.0-cachegrind-improvements.patch

# Make ld.so supressions slightly less specific.
Patch2: valgrind-3.9.0-ldso-supp.patch

# Add some stack-protector
Patch3: valgrind-3.26.0-some-stack-protector.patch

# Add some -Wl,z,now.
Patch4: valgrind-3.26.0-some-Wl-z-now.patch

# VALGRIND_3_26_BRANCH patches
Patch5: 0001-Prepare-NEWS-for-branch-3.26-fixes.patch
Patch6: 0002-Bug-511972-valgrind-3.26.0-tests-fail-to-build-on-up.patch
Patch7: 0003-readlink-proc-self-exe-overwrites-buffer-beyond-its-.patch
Patch8: 0004-Linux-DRD-suppression-add-an-entry-for-__is_decorate.patch
Patch9: 0005-Linux-Helgrind-add-a-suppression-for-_dl_allocate_tl.patch
Patch10: 0006-Disable-linux-madvise-MADV_GUARD_INSTALL.patch
Patch11: 0007-Bug-514613-Unclosed-leak_summary-still_reachable-tag.patch
Patch12: 0008-Bug-514206-Assertion-sr_isError-sr-failed-mmap-fd-po.patch

# Refix for https://bugs.kde.org/show_bug.cgi?id=514613
Patch100: 0001-Refix-still_reachable-xml-closing-tag-and-add-testca.patch

BuildRequires: make
BuildRequires: glibc-devel

%if %{build_openmpi}
BuildRequires: openmpi-devel
%endif

%if %{run_full_regtest}
BuildRequires: gdb
%endif

# gdbserver_tests/filter_make_empty uses ps in test
BuildRequires: procps

# Some testcases require g++ to build
BuildRequires: gcc-c++

# check_headers_and_includes uses Getopt::Long
%if 0%{?fedora}
BuildRequires: perl-generators
%endif
BuildRequires: perl(Getopt::Long)

# We always autoreconf
BuildRequires: automake
BuildRequires: autoconf

# For make check validating the documentation
BuildRequires: docbook-dtds

# For testing debuginfod-find
%if 0%{?fedora} > 29 || 0%{?rhel} > 7
BuildRequires: elfutils-debuginfod
BuildRequires: elfutils-debuginfod-client
# For using debuginfod at runtime
Recommends: elfutils-debuginfod-client
%endif

# Optional subpackages
Recommends: %{?scl_prefix}valgrind-docs = %{epoch}:%{version}-%{release}
Recommends: %{?scl_prefix}valgrind-scripts = %{epoch}:%{version}-%{release}
Recommends: %{?scl_prefix}valgrind-gdb = %{epoch}:%{version}-%{release}

# For running the testsuite.
# Some of the python scripts require python 3.9+
BuildRequires: python3-devel

%{?scl:Requires:%scl_runtime}

# We could use %%valgrind_arches as defined in redhat-rpm-config
# But that is really for programs using valgrind, it defines the
# set of architectures that valgrind works correctly on.
ExclusiveArch: %{ix86} x86_64 ppc ppc64 ppc64le s390x armv7hl aarch64 riscv64

# Define valarch, the architecture name that valgrind uses
# And only_arch, the configure option to only build for that arch.
%ifarch %{ix86}
%define valarch x86
%define only_arch --enable-only32bit
%endif
%ifarch x86_64
%define valarch amd64
%define only_arch --enable-only64bit
%endif
%ifarch ppc
%define valarch ppc32
%define only_arch --enable-only32bit
%endif
%ifarch ppc64
%define valarch ppc64be
%define only_arch --enable-only64bit
%endif
%ifarch ppc64le
%define valarch ppc64le
%define only_arch --enable-only64bit
%endif
%ifarch s390x
%define valarch s390x
%define only_arch --enable-only64bit
%endif
%ifarch armv7hl
%define valarch arm
%define only_arch --enable-only32bit
%endif
%ifarch aarch64
%define valarch arm64
%define only_arch --enable-only64bit
%endif
%ifarch riscv64
%define valarch riscv64
%define only_arch --enable-only64bit
%endif

%description
Valgrind is an instrumentation framework for building dynamic analysis
tools. There are Valgrind tools that can automatically detect many
memory management and threading bugs, and profile your programs in
detail. You can also use Valgrind to build new tools. The Valgrind
distribution currently includes six production-quality tools: a memory
error detector (memcheck, the default tool), two thread error
detectors (helgrind and drd), a cache and branch-prediction profiler
(cachegrind), a call-graph generating cache and branch-prediction
profiler (callgrind), and a heap profiler (massif).

%package devel
Summary: Development files for valgrind aware programs
# This is really Hybrid-BSD
# https://fedoraproject.org/wiki/Licensing:BSD#Hybrid_BSD_(half_BSD,_half_zlib)
# But that doesnt have a SPDX identifier yet
# https://gitlab.com/fedora/legal/fedora-license-data/-/issues/422
License: bzip2-1.0.6
# These are just the header files, so strictly speaking you don't
# need valgrind itself unless you are testing your builds. This used
# to be a Requires, so people might depend on the package pulling in
# the core valgrind package, so make it at least a weak dependency.
Recommends: %{?scl_prefix}valgrind = %{epoch}:%{version}-%{release}

%description devel
Header files and libraries for development of valgrind aware programs.

%package docs
Summary: Documentation for valgrind tools, scripts and gdb integration
License: GFDL-1.2-or-later

%description docs
Documentation in html and pdf, plus man pages for valgrind tools and scripts.

%package scripts
Summary: Scripts for post-processing valgrind tool output
License: GPL-3.0-or-later AND (GPL-3.0-or-later OR MPL-2.0)
# Most scripts can be used as is for post-processing a valgrind tool run.
# But callgrind_control uses vgdb.
Recommends: %{?scl_prefix}valgrind-gdb = %{epoch}:%{version}-%{release}

%description scripts
Perl and Python scripts for post-processing valgrind tool output.

%package gdb
Summary: Tools for integrating valgrind and gdb
License: GPL-3.0-or-later
Requires: %{?scl_prefix}valgrind = %{epoch}:%{version}-%{release}
# vgdb can be used without gdb, just to control valgrind.
# But normally you use it together with both valgrind and gdb.
Recommends: gdb

%description gdb
Tools and support files for integrating valgrind and gdb.

%if %{build_tools_devel}
%package tools-devel
Summary: Development files for building valgrind tools.
Requires: %{?scl_prefix}valgrind-devel = %{epoch}:%{version}-%{release}
Provides: %{name}-static = %{epoch}:%{version}-%{release}

%description tools-devel
Header files and libraries for development of valgrind tools.
%endif

%if %{build_openmpi}
%package openmpi
Summary: OpenMPI support for valgrind
# See above, Hybrid-BSD like.
License: bzip2-1.0.6
Requires: %{?scl_prefix}valgrind = %{epoch}:%{version}-%{release}

%description openmpi
A wrapper library for debugging OpenMPI parallel programs with valgrind.
See the section on Debugging MPI Parallel Programs with Valgrind in the
Valgrind User Manual for details.
%endif

%prep
%setup -q -n %{?scl:%{pkg_name}}%{!?scl:%{name}}-%{version}

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
%patch -P12 -p1

%patch -P100 -p1

%build
# LTO triggers undefined symbols in valgrind.  But valgrind has a
# --enable-lto configure time option that we will use instead.
%define _lto_cflags %{nil}

# Some patches (might) touch Makefile.am or configure.ac files.
# Just always autoreconf so we don't need patches to prebuild files.
./autogen.sh

%if %{build_openmpi}
%define mpiccpath %{!?scl:%{_libdir}}%{?scl:%{_root_libdir}}/openmpi/bin/mpicc
%else
# We explicitly don't want the libmpi wrapper. So make sure that configure
# doesn't pick some random mpi compiler that happens to be installed.
%define mpiccpath /bin/false
%endif

# Filter out "hardening" flags that don't make sense for valgrind.
# -fstack-protector just cannot work (valgrind would have to implement
# its own version since it doesn't link with glibc and handles stack
# setup itself). We patch some flags back in just for those helper
# programs where it does make sense.
#
# -Wl,-z,now doesn't make sense for static linked tools
# and would prevent using the vgpreload libraries on binaries that
# don't link themselves against libraries (like pthread) which symbols
# are needed (but only if the inferior itself would use them).
#
# -O2 doesn't work for the vgpreload libraries either. They are meant
# to not be optimized to show precisely what happened. valgrind adds
# -O2 itself wherever suitable.
#
# On ppc64[be] -fexceptions is troublesome.
# It might cause an undefined reference to `_Unwind_Resume'
# in libcoregrind-ppc64be-linux.a(libcoregrind_ppc64be_linux_a-readelf.o):
# In function `read_elf_symtab__ppc64be_linux.
#
# Also disable strict symbol checks because the vg_preload library
# will use hidden/undefined symbols from glibc like __libc_freeres.
%undefine _strict_symbol_defs_build

%ifarch ppc64
CFLAGS="`echo " %{optflags} " | sed 's/ -fstack-protector\([-a-z]*\) / / g;s/ -O2 / /g;s/ -fexceptions / /g;'`"
%else
CFLAGS="`echo " %{optflags} " | sed 's/ -fstack-protector\([-a-z]*\) / / g;s/ -O2 / /g;'`"
%endif
export CFLAGS

# Older Fedora/RHEL only had __global_ldflags.
# Even older didn't even have that (so we don't need to scrub them).
%if 0%{?build_ldflags:1}
LDFLAGS="`echo " %{build_ldflags} "    | sed 's/ -Wl,-z,now / / g;'`"
%else
%if 0%{?__global_ldflags:1}
LDFLAGS="`echo " %{__global_ldflags} " | sed 's/ -Wl,-z,now / / g;'`"
%endif
%endif
export LDFLAGS

%configure \
  --with-mpicc=%{mpiccpath} \
  %{only_arch} \
  GDB=%{_bindir}/gdb \
  --with-gdbscripts-dir=%{_datadir}/gdb/auto-load \
  --enable-lto

%make_build

%install
rm -rf $RPM_BUILD_ROOT
%make_install
mkdir docs/installed
mv $RPM_BUILD_ROOT%{_datadir}/doc/valgrind/* docs/installed/
rm -f docs/installed/*.ps

# We want the MPI wrapper installed under the openmpi libdir so the script
# generating the MPI library requires picks them up and sets up the right
# openmpi libmpi.so requires. Install symlinks in the original/upstream
# location for backwards compatibility.
%if %{build_openmpi}
pushd $RPM_BUILD_ROOT%{_libdir}
mkdir -p openmpi/valgrind
cd valgrind
mv libmpiwrap-%{valarch}-linux.so ../openmpi/valgrind/
ln -s ../openmpi/valgrind/libmpiwrap-%{valarch}-linux.so
popd
%endif

%if %{build_tools_devel}
%ifarch %{ix86} x86_64
# To avoid multilib clashes in between i?86 and x86_64,
# tweak installed <valgrind/config.h> a little bit.
for i in HAVE_PTHREAD_CREATE_GLIBC_2_0 HAVE_PTRACE_GETREGS HAVE_AS_AMD64_FXSAVE64; do
  sed -i -e 's,^\(#define '$i' 1\|/\* #undef '$i' \*/\)$,#ifdef __x86_64__\n# define '$i' 1\n#endif,' \
    $RPM_BUILD_ROOT%{_includedir}/valgrind/config.h
done
%endif
%else
# Remove files we aren't going to package.
# See tools-devel files.
rm $RPM_BUILD_ROOT%{_includedir}/valgrind/config.h
rm $RPM_BUILD_ROOT%{_includedir}/valgrind/libvex*h
rm $RPM_BUILD_ROOT%{_includedir}/valgrind/pub_tool_*h
rm -rf $RPM_BUILD_ROOT%{_includedir}/valgrind/vki
rm $RPM_BUILD_ROOT%{_libdir}/valgrind/*.a
%endif

# We don't want debuginfo generated for the vgpreload libraries.
# Turn off execute bit so they aren't included in the debuginfo.list.
# We'll turn the execute bit on again in %%files.
chmod 644 $RPM_BUILD_ROOT%{_libexecdir}/valgrind/vgpreload*-%{valarch}-*so

%check
# Make sure some info about the system is in the build.log
# Add || true because rpm on copr EPEL6 acts weirdly and we don't want
# to break the build.
uname -a
rpm -q glibc gcc binutils || true
%if %{run_full_regtest}
rpm -q gdb || true
%endif

LD_SHOW_AUXV=1 /bin/true
cat /proc/cpuinfo

# Make sure a basic binary runs. There should be no errors.
./vg-in-place --error-exitcode=1 /bin/true --help

# Build the test files with the software collection compiler if available.
%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}
# Make sure no extra CFLAGS, CXXFLAGS or LDFLAGS leak through,
# the testsuite sets all flags necessary. See also configure above.
%make_build CFLAGS="" CXXFLAGS="" LDFLAGS="" check

# Workaround https://bugzilla.redhat.com/show_bug.cgi?id=1434601
# for gdbserver tests.
export PYTHONCOERCECLOCALE=0

echo ===============TESTING===================
%if %{run_full_regtest}
  make regtest || :
%else
  make nonexp-regtest || :
%endif

# Make sure test failures show up in build.log
# Gather up the diffs (at most the first 20 lines for each one)
MAX_LINES=20
diff_files=`find gdbserver_tests */tests -name '*.diff*' | sort`
if [ z"$diff_files" = z ] ; then
   echo "Congratulations, all tests passed!" >> diffs
else
   for i in $diff_files ; do
      echo "=================================================" >> diffs
      echo $i                                                  >> diffs
      echo "=================================================" >> diffs
      if [ `wc -l < $i` -le $MAX_LINES ] ; then
         cat $i                                                >> diffs
      else
         head -n $MAX_LINES $i                                 >> diffs
         echo "<truncated beyond $MAX_LINES lines>"            >> diffs
      fi
   done
fi
cat diffs
echo ===============END TESTING===============

%{!?_licensedir:%global license %%doc}

%files
%license COPYING
%{_bindir}/valgrind
%dir %{_libexecdir}/valgrind
# Install just the core tools, default suppression and vgpreload libraries.
%{_libexecdir}/valgrind/default.supp
%{_libexecdir}/valgrind/*-*-linux
# Turn on executable bit again for vgpreload libraries.
# Was disabled in %%install to prevent debuginfo stripping.
%attr(0755,root,root) %{_libexecdir}/valgrind/vgpreload_*-%{valarch}-linux.so

%files docs
%license COPYING.DOCS
%doc NEWS README_*
%doc docs/installed/html docs/installed/*.pdf
%{_mandir}/man1/*

%files scripts
%license COPYING
%{_bindir}/callgrind_annotate
%{_bindir}/callgrind_control
%{_bindir}/cg_annotate
%{_bindir}/cg_diff
%{_bindir}/cg_merge
%{_bindir}/ms_print
%{_libexecdir}/valgrind/dh_view.css
%{_libexecdir}/valgrind/dh_view.html
%{_libexecdir}/valgrind/dh_view.js

%files gdb
%license COPYING
%{_bindir}/valgrind-di-server
%{_bindir}/valgrind-listener
%{_bindir}/vgdb
%{_bindir}/vgstack
# gdb register descriptions
%{_libexecdir}/valgrind/*.xml
%{_datadir}/gdb/auto-load/valgrind-monitor.py
%{_datadir}/gdb/auto-load/valgrind-monitor-def.py

%files devel
%dir %{_includedir}/valgrind
%{_includedir}/valgrind/valgrind.h
%{_includedir}/valgrind/cachegrind.h
%{_includedir}/valgrind/callgrind.h
%{_includedir}/valgrind/drd.h
%{_includedir}/valgrind/helgrind.h
%{_includedir}/valgrind/memcheck.h
%{_includedir}/valgrind/dhat.h
%{_libdir}/pkgconfig/valgrind.pc

%if %{build_tools_devel}
%files tools-devel
%license COPYING
%{_includedir}/valgrind/config.h
%{_includedir}/valgrind/libvex*h
%{_includedir}/valgrind/pub_tool_*h
%{_includedir}/valgrind/vki
%dir %{_libdir}/valgrind
%{_libdir}/valgrind/*.a
%endif

%if %{build_openmpi}
%files openmpi
%dir %{_libdir}/valgrind
%{_libdir}/openmpi/valgrind/libmpiwrap*.so
%{_libdir}/valgrind/libmpiwrap*.so
%endif

%changelog
* Thu Jan 29 2026 Mark Wielaard <mjw@fedoraproject.org> - 3.26.0-5
  - Add 0001-Refix-still_reachable-xml-closing-tag-and-add-testca.patch

* Mon Jan 26 2026 Mark Wielaard <mjw@fedoraproject.org> - 3.26.0-4
  - Add more VALGRIND_3_26_BRANCH patches
    - 0007-Bug-514613-Unclosed-leak_summary-still_reachable-tag.patch
    - 0008-Bug-514206-Assertion-sr_isError-sr-failed-mmap-fd-po.patch

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jan  8 2026 Mark Wielaard <mjw@fedoraproject.org> - 3.26.0-2
  - Add VALGRIND_3_26_BRANCH patches
    - 0001-Prepare-NEWS-for-branch-3.26-fixes.patch
    - 0002-Bug-511972-valgrind-3.26.0-tests-fail-to-build-on-up.patch
    - 0003-readlink-proc-self-exe-overwrites-buffer-beyond-its-.patch
    - 0004-Linux-DRD-suppression-add-an-entry-for-__is_decorate.patch
    - 0005-Linux-Helgrind-add-a-suppression-for-_dl_allocate_tl.patch
    - 0006-Disable-linux-madvise-MADV_GUARD_INSTALL.patch

* Fri Oct 24 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.26.0-1
- Valgrind 3.26.0 final
- Clarify License of valgrind-scripts.

* Sat Oct 18 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.26.0-0.1.RC1
- Upstream 3.26.0-RC1
- Remove all VALGRIND_3_25_BRANCH and proposed upstream patches
- Refresh some-stack-protector and some-Wl-z-now patches.
- Add vgstack to valgrind-gdb.
- Update License to GPL-3.0-or-later

* Mon Aug 11 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.25.1-4
- Add ppc64-strcmp-ld.patch
- Add 0003-Add-several-missing-syscall-hooks-to-ppc64-linux.patch

* Tue Aug  5 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.25.1-3
- Add VALGRIND_3_25_BRANCH patches
  - 0001-Prepare-NEWS-for-branch-3.25.x-fixes.patch
  - 0002-Bug-503241-s390x-Support-z17-changes-to-the-NNPA-ins.patch

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue May 20 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.25.1-1
- Valgrind 3.25.1 final

* Fri May 16 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.25.0-3
- Add 2 more VALGRIND_3_25_BRANCH patches

* Fri May  9 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.25.0-2
- Add VALGRIND_3_25_BRANCH patches

* Fri Apr 25 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.25.0-1
- Valgrind 3.25.0 final

* Wed Apr 23 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.25.0-0.1.RC2
- Upstream 3.25.0-RC2

* Fri Apr 18 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.25.0-0.1.RC1
- Upstream 3.25.0-RC1
- Remove all VALGRIND_3_24_BRANCH patches
- Enable riscv64 arch support

* Sun Mar 30 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.24.0-8
- Add new VALGRIND_3_24_BRANCH patches
  - 0019-filter_gdb.in-__syscall_cancel_arch-is-just-in-a-sys.patch
  - 0020-Bug-501893-Missing-suppression-for-__wcscat_avx2-str.patch
  - 0021-filter_gdb.in-filter-out-__libc_do_syscall.patch
  - 0022-Handle-top-__syscall_cancel-frames-when-getting-stac.patch
- Remove valgrind-3.24.0-syscall-cancel.patch (replaced by 0022).

* Fri Mar 28 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.24.0-7
- Add valgrind-3.24.0-syscall-cancel.patch

* Wed Mar 12 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.24.0-6
- More VALGRIND_3_24_BRANCH patches
  0016-syswrap-generic-Emit-pp_ExeContext-after-the-file-de.patch
  0017-add_hardwired_spec-for-ld-linux-x86-64.so.2-memcmp.patch
  0018-gdbserver_tests-filter-out-new-Missing-rpms-message.patch

* Fri Jan 17 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.24.0-5
- valgrind-devel now Recommends, instead of Requires, valgrind.
- valgrind-gdb now Requires valgrind, instead of valgrind-devel.
- valgrind-scripts now Recommends valgrind-gdb
- valgrind-gdb now Recommends gdb

* Wed Jan 15 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.24.0-4
- Add 0015-ppc-test_dfp2-build-fix-for-GCC-15.patch

* Tue Jan 14 2025 Mark Wielaard <mjw@fedoraproject.org> - 3.24.0-3
- Add more VALGRIND_3_24_BRANCH patches
  0012-Recognize-new-DWARF5-DW_LANG-constants.patch
  0013-Bug-498317-FdBadUse-is-not-a-valid-CoreError-type-in.patch
  0014-linux-support-EVIOCGRAB-ioctl.patch
- Split main valgrind package into several subpackages:
  - valgrind now contains just the core tools.
  - valgrind-scripts contains the post-processing scripts for callgrind,
    cachegrind, massif and dhat which depend on perl and python.
  - valgrind-gdb contains the debuginfo client/server and (v)gdb support.
  - valgrind-docs contains the man pages, html and pdf manual.
* Tue Nov 26 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.24.0-2
- Add VALGRIND_3_24_BRANCH patches
  0001-Prepare-NEWS-for-branch-3.24-fixes.patch
  0002-vgdb.c-fork_and_exec_valgrind-Fix-off-by-one-error-w.patch
  0003-vgdb.c-fork_and_exec_valgrind-Fix-another-off-by-one.patch
  0004-regtest-add-a-fdleak-filter-for-write-on-write-on-li.patch
  0005-Add-exp-and-supp-patterns-for-missing-main-frame-for.patch
  0006-Add-additional-exp-ppc64le-files-to-EXTRA_DIST.patch
  0007-Add-support-for-landlock_create_ruleset-444-landlock.patch
  0008-helgrind-tests-tc17_sembar.c-Remove-bool-typedef.patch
  0009-drd-tests-swapcontext.c-Rename-typedef-struct-thread.patch
  0010-none-tests-bug234814.c-sa_handler-take-an-int-as-arg.patch
  0011-Add-open_tree-move_mount-fsopen-fsconfig-fsmount-fsp.patch

* Mon Nov  4 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.24.0-1
- Upstream 3.24.0 final

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.23.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul  6 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.23.0-4
- Add more upstream VALGRIND_3_23_BRANCH patches
  0016-mips-skip-using-shared-syscall-numbers-for-mips64.patch
  0017-gdbserver_tests-filters-remove-python-rpm-module-loa.patch
  0018-Implement-VMOVQ-xmm1-xmm2-m64.patch
  0019-arm64-Fix-fcvtas-instruction.patch
  0020-gdbserver_tests-filters-remove-more-verbose-python-r.patch
  0021-Avoid-dev-inode-check-on-btrfs-with-sanity-level-3.patch

* Sun Jun 23 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.23.0-3
- Add more upstream VALGRIND_3_23_BRANCH patches
  0012-Bug-487439-SIGILL-in-JDK11-JDK17.patch
  0013-Don-t-leave-fds-created-with-log-file-xml-file-or-lo.patch
  0014-Close-both-internal-pipe-fds-after-VG_-fork-in-paren.patch
  0015-Don-t-allow-programs-calling-fnctl-on-valgrind-s-own.patch

* Mon Jun 10 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.23.0-2
- Add upstream VALGRIND_3_23_BRANCH patches

* Fri Apr 26 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.23.0-1
- Upstream 3.23.0 final

* Thu Apr 25 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.23.0-0.2.RC2
- configure --enable-lto

* Wed Apr 24 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.23.0-0.1.RC2
- Upstream 3.23.0-RC2

* Sat Apr 20 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.23.0-0.1.RC1
+- Upstream 3.23.0-RC1
+- Remove all upstreamed patches

* Sat Apr 13 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-8
- Add BuildRequires: python3-devel for running testsuite.
- Add valgrind-3.22.0-gdb-thread-exited.patch
- Add valgrind-3.22.0-set_vma_name-supp.patch
- Add valgrind-3.22.0-pth_mempcpy_false_races.patch
- Add valgrind-3.22.0-amd64-VFMADD213.patch
- Add valgrind-3.22.0-amd64-redir-strcmp.patch

* Mon Mar 11 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-7
- Add valgrind-3.22.0-gcc-builtin_strcmp-128-256-bit-vector.patch

* Mon Mar  4 2024 Mark Wielaard <mjw@fedoraproject.org>
- Update Fedora license tags to spdx license tags

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.22.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-5
- Add valgrind-3.22.0-x86-nop.patch

* Sat Dec  9 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-4
- Add valgrind-3.22.0-fchmodat2.patch
- Prep for migration to SPDX identifiers

* Tue Dec  5 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-3
- Add valgrind-3.22.0-rodata.patch

* Fri Nov 17 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-2
- Add valgrind-3.22.0-valgrind-monitor-python-re.patch
- Drop support for rhel6

* Tue Oct 31 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-1
- Upstream 3.22.0 final
- BuildRequires elfutils-debuginfod for testing

* Mon Oct 30 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-0.2.RC2
- Update valgrind-3.21.0-no-memcpy-replace-check.patch
- Fedora 40 dropped openmpi support on i386

* Thu Oct 26 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-0.1.RC2
- Upstream 3.22.0-RC2

* Tue Oct 17 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.22.0-0.1.RC1
- Upstream 3.22.0-RC1
- Remove all upstreamed patches
- Adjust valgrind-3.16.0-some-stack-protector.patch
- Adjust valgrind-3.16.0-some-Wl-z-now.patch
- Add cachegrind.h to valgrind-devel package

* Mon Aug 21 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-10
- Add valgrind-3.21.0-lazy-debuginfo.patch
- Add valgrind-3.21.0-cleanup-read_elf_object.patch

* Thu Aug 17 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-9
- Add valgrind-3.21.0-gdb-multi-mode-stdout-redirecting-to-stderr.patch
- Use %%patch -Pn instead of deprecated %%patchn

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.21.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-7
- Add valgrind-3.21.0-vgm.patch and valgrind-3.21.0-vgm-tests.patch
- Add valgrind-3.21.0-pgste.patch

* Thu Jun  1 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-6
- Add valgrind-3.21.0-callgrind_control-no-strict.patch
- Add valgrind-3.21.0-realloc-again.patch

* Tue May 30 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-5
- Update valgrind-3.21.0-no-memcpy-replace-check.patch (memcpy_chk)

* Wed May 17 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-4
- Add valgrind-3.21.0-epoll_pwait2.patch

* Tue May 16 2023 Alexandra Hájková <ahajkova@redhat.com> - 3.21.0-3
- Add valgrind-3.21.0-Add-with-gdbscripts-dir.patch

* Fri May  5 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-2
- Add valgrind-3.21.0-no-memcpy-replace-check.patch

* Fri Apr 28 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-1
- Upstream 3.21.0 final

* Sat Apr 22 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-0.1.RC2
- Upstream 3.21.0-RC2

* Fri Apr 21 2023 Mark Wielaard <mjw@fedoraproject.org> - 3.21.0-0.1.RC1
- Upstream 3.21.0-RC1
- Remove upstreamed valgrind-faultstatus-implicit-int.patch
- Adjust valgrind-3.16.0-some-{Wl-z-now,stack-protector}.patch
  cg_merge is now a pything script.

* Fri Nov 18 2022 Florian Weimer <fweimer@redhat.com> - 1:3.20.0-2
- Avoid using implicit int C89 feature

* Mon Oct 24 2022 Mark Wielaard <mjw@fedoraproject.org> - 3.20.0-1
- Upgrade to valgrind 3.20.0. Drop old patches.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 25 2022 Mark Wielaard <mjw@fedoraproject.org> - 3.19.0-3
- Add valgrind-3.19.0-s390x-memmem.patch

* Fri May 13 2022 Mark Wielaard <mjw@fedoraproject.org> - 3.19.0-2
- Add valgrind-3.19.0-ld-so-strncmp.patch

* Tue Apr 12 2022 Mark Wielaard <mjw@fedoraproject.org> - 3.19.0-1
- Upgrade to valgrind 3.19.0. Drop old patches.

* Tue Feb  8 2022 Mark Wielaard <mjw@fedoraproject.org>
- Add valgrind-3.18.1-ppc64-cmov.patch
- Add valgrind-3.18.1-arm64-atomics-rdm.patch
- Add valgrind-3.18.1-rust-demangle-suffix.patch

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.18.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Mark Wielaard <mjw@fedoraproject.org> - 3.18.1-8
- Add valgrind-3.18.1-ppc-hwcaps.patch
- Add valgrind-3.18.1-s390x-wflrx.patch

* Sat Dec 11 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.18.1-7
-Add valgrind-3.18.1-s390x-vdso.patch

* Fri Dec 10 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.18.1-6
- Add valgrind-3.18.1-rseq-enosys.patch

* Mon Nov 22 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.18.1-5
- Add valgrind-3.18.1-demangle-namespace.patch

* Fri Nov 19 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.18.1-4
- Add valgrind-3.18.1-condvar.patch

* Wed Nov 17 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.18.1-3
- Add valgrind-3.18.1-ppc-pstq.patch
- Add valgrind-3.18.1-ppc-pstq-tests.patch
- Add valgrind-3.18.1-gdbserver_tests-hwcap.patch
- Add valgrind-3.18.1-rust-v0-demangle.patch
- Add valgrind-3.18.1-arm64-doubleword-cas.patch
- Add valgrind-3.18.1-arm64-ldaxp-stlxp.patch
- Add valgrind-3.18.1-arm64-atomic-align.patch
- Add valgrind-3.18.1-amd64-more-spec-rules.patch

* Mon Nov  1 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.18.1-2
- Add valgrind-3.18.1-dhat-tests-copy.patch
- Add valgrind-3.18.1-s390x-EXRL.patch
- Add valgrind-3.18.1-ppc64-lxsibzx-lxsihzx.patch

* Fri Oct 15 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.18.0-1
- Update to upstream 3.18.1 final

* Wed Oct 13 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.18.0-0.1.RC1
- Update to upstream 3.18.0-RC1
- Drop all upstreamed patches

* Mon Sep 20 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-13
- Add valgrind-3.17.0-dwarf-atomic_type.patch
- Add valgrind-3.17.0-faster-readdwarf3.patch

* Wed Sep  8 2021 Mark Wielaard <mjw@fedoraproject.org>
- Add valgrind-3.17.0-ppc64-test_isa_3_1_VRT.patch

* Wed Aug 25 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-12
- Add valgrind-3.17.0-vgdb-queued-signals.patch
- Add valgrind-3.17.0-ppc64-test-isa-3-1.patch
- Add valgrind-3.17.0-ppc64-pstxvp.patch

* Fri Aug  6 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-11
- Add valgrind-3.17.0-ppc64-statfs64.patch

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.17.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Mark Wielaard <mjw@fedoraproject.org>
- Add valgrind-3.17.0_start.patch

* Wed Jul 21 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-9
- Add valgrind-3.17.0-clone3.patch

* Sat Jul 17 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-8
- Update drd suppression for native ld.so names.

* Sat Jul 17 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-7
- Add gdbserver_tests-update-filters-for-newer-glibc-gdb.patch
- Add helgrind-and-drd-suppression-libc-and-libpthread.patch
- Remove valgrind-3.9.0-helgrind-race-supp.patch

* Fri Jul  9 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-6
- Update to include fixed CI gating tests.

* Fri Jun 18 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-5
- Add valgrind-3.17.0-s390-prep.patch
- Add valgrind-3.17.0-s390-z15.patch
- Add valgrind-3.17.0-s390-z13-vec-fix.patch

* Thu Jun  3 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-4
- Add valgrind-3.17.0-s390_insn_as_string.patch
- Add valgrind-3.17.0-debuginfod.patch
- Add valgrind-3.17.0-clone-parent-res.patch

* Tue May  4 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-3
- Add valgrind-3.17.0-ppc64-isa-3.1{,tests}.patch

* Fri Apr 16 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-2
- Add CI gating

* Mon Mar 22 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-1
- Update to upstream 3.17.0 final.

* Wed Mar 17 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-0.1.RC2
- Update to upstream 3.17.0-RC2

* Mon Mar 15 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.17.0-0.1.RC1
- Update to upstream 3.17.0-RC1
- Drop all upstreamed patches

* Wed Mar  3 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-20
- Add valgrind-3.16.1-arm64_sp_lr_fp_DwReg.patch

* Sun Feb 21 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-19
- Add valgrind-3.16.1-readdwarf-line.patch

* Sat Feb  6 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-18
- Update valgrind-3.16.1-open-proc-self-exe.patch to handle openat

* Sat Feb  6 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-17
- Add valgrind-3.16.1-open-proc-self-exe.patch

* Wed Feb  3 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-16
- Add valgrind-3.16.0-shmctl.patch

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.16.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-14
- Add valgrind-3.16.1-dwarf5.patch

* Fri Jan  8 2021 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-13
- Add valgrind-3.16.1-ppc64-scv-hwcap.patch

* Sun Dec 20 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-12
- Add valgrind-3.16.1-ficlone.patch
- Add valgrind-3.16.1-arm64-expensive-cmp.patch

* Thu Dec 17 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-11
- Update valgrind-3.16.1-arm64-fma.patch

* Tue Dec 15 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-10
- Add valgrind-3.16.1-arm64-fma.patch

* Sun Dec 13 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-9
- Add valgrind-3.16.1-stxsibx-stxsihx.patch

* Thu Dec  3 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-8
- Update valgrind-3.16.1-s390x-z14-vector.patch

* Thu Dec  3 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-7
- Add valgrind-3.16.1-pthread-intercept.patch
- Add valgrind-3.16.1-s390_emit_load_mem.patch
- Add valgrind-3.16.1-s390x-z14-vector.patch

* Mon Nov  9 2020 Mark Wielaard <mjw@fedoraproject.org>
- Add BuildRequires which (#1895773)

* Fri Oct 16 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-6
- Add valgrind-3.16.1-faccessat2.patch
- Add valgrind-3.16.1-gdbserver_nlcontrolc.patch
- Add valgrind-3.16.1-PPC64BE-lsw.patch

* Tue Aug 18 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-5
- Update valgrind-3.16.1-epoll.patch

* Mon Jul 27 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-4
- Add valgrind-3.16.1-REX-prefix-JMP.patch
- Add valgrind-3.16.1-epoll.patch
- Add valgrind-3.16.1-sched_getsetattr.patch
- Add valgrind-3.16.1-dl_runtime_resolve.patch

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 3.16.1-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jul  8 2020 Jeff Law <law@redhat.org> - 3.16.1-2
- Disable LTO

* Tue Jun 23 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.1-1
- Update to upstream valgrind 3.16.1.

* Fri Jun 19 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.0-3
- Add valgrind-3.16.0-ppc-L-field.patch

* Wed May 27 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.0-2
- Apply stack-protector and -Wl,z,now patches.

* Wed May 27 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.0-1
- Update to upstream valgrind 3.16.0 final.

* Tue May 19 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.0-0.4.RC2
- Add docbook-dtds to BuildRequires.

* Tue May 19 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.0-0.3.RC2
- Update to upstream 3.16.0 RC2

* Fri May  1 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.0-0.2.GIT
- Update to upstream 3.16.0 branch point (commit 55cdb7c4e)

* Fri Apr 17 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.16.0-0.1.GIT
- Update to upstream 3.16.0-GIT (commit 52d02fe23)
  - Drop all streamed patches.

* Wed Mar  4 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-20
- Add valgrind-3.15.0-z15.patch

* Fri Feb 28 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-19
- Add valgrind-3.15.0-time64.patch
- Add valgrind-3.15.0-arm-preadv2-pwritev2.patch
- Add valgrind-3.15.0-avx_estimate_insn-test.patch
- Add valgrind-3.15.0-gcc-10-x86-amd64-asm-test.patch

* Fri Feb 14 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-18
- Add valgrind-3.15.0-ppc64-sigframe.patch

* Thu Feb 13 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-17
- Add valgrind-3.15.0-glibc-dtv-supp.patch

* Wed Jan 29 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-16
- Add valgrind-3.15.0-s390x-HRcVec128.patch

* Wed Jan 29 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-15
- Don't use valgrind-3.15.0-ptrace-siginfo.patch on ppc64[le]
- Add valgrind-3.15.0-s390x-compare-and-signal.patch

* Fri Jan 24 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-14
- Add valgrind-3.15.0-gcc-10-i686-asm-test.patch
- Add valgrind-3.15.0-gcc10-ppc64-asm-constraints.patch

* Thu Jan 23 2020 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-13
- Add valgrind-3.15.0-gcc-10-typedef-enum.patch

* Mon Sep 23 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-12
- Add valgrind-3.15.0-ptrace-siginfo.patch

* Mon Aug  5 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-11
- Add valgrind-3.15.0-preadv2-pwritev2.patch
- Add valgrind-3.15.0-arm-membarrier.patch
- Add valgrind-3.15.0-z14-misc.patch

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.15.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-9
- Add valgrind-3.15.0-pkey.patch

* Tue May 28 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-8
- Update valgrind-3.15.0-copy_file_range.patch.
- Add valgrind-3.15.0-avx-rdrand-f16c.patch.

* Fri May 24 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-7
- Update valgrind-3.15.0-some-stack-protector.patch to include getoff.
- Add valgrind-3.15.0-some-Wl-z-now.patch

* Fri May 24 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-6
- Add valgrind-3.15.0-s390x-wrap-drd.patch

* Mon May 20 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-5
- Add valgrind-3.15.0-exp-sgcheck-no-aarch64.patch
- Add valgrind-3.15.0-scalar-arm64.patch
- Add valgrind-3.15.0-scalar-x86.patch

* Tue May  7 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-4
- Add valgrind-3.15.0-arm64-ld-stpcpy.patch

* Sun May  5 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-3
- Add valgrind-3.15.0-copy_file_range.patch

* Thu Apr 25 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-2
- gdb has been fixed on fedora, run full regtests again.
- Add valgrind-3.15.0-ppc64-filter_gdb.patch

* Tue Apr 16 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-1
- On ppc64[be] -fexceptions is troublesome.
- valgrind-3.15.0 final
  Remove upstreamed patches
  - valgrind-3.15.0-arm64-Ity_F16.patch
  - valgrind-3.15.0-filter-libc-futex.patch
  - valgrind-3.15.0-mmap-32bit.patch

* Sun Apr 14 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-0.8.RC2
- Adding of stack-protector flag should only be done with newer gcc.
- Older rpm macros didn't provide build_ldflags.
- Add valgrind-3.15.0-arm64-Ity_F16.patch

* Sun Apr 14 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-0.7.RC2
- Add valgrind-3.15.0-some-stack-protector.patch

* Sat Apr 13 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-0.6.RC2
- Pass through most (hardening) flags, except -O2, -fstack-protector
  and -Wl,-z,now.

* Fri Apr 12 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-0.5.RC2
- No openmpi support on old s390x rhel.
- Disable s390x z13 support on rhel6 (too old binutils).
- Use an explicit ExclusiveArch, don't rely on %%valgrind_arches.
- Drop close_fds, it is no longer needed.
- Include any gdbserver_tests diffs for failing regtest.

* Thu Apr 11 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-0.4.RC2
- Update to 3.15.0.RC2.
- Drop upstreamed patches:
  - valgrind-3.15.0-s390x-get-startregs-constraint.patch
  - valgrind-3.15.0-missing-a-c.patch
  - valgrind-3.15.0-libstdc++-supp.patch
  - valgrind-3.15.0-dhat-x86.patch
  - valgrind-3.15.0-gdb-output1.patch
  - valgrind-3.15.0-gdb-output2.patch
- Update valgrind-3.15.0-mmap-32bit.patch to upstream version.
- gdb on f30 and rawhide is currently broken, don't run_full_regtest.
- Any glibc-devel version is.
- Drop rhel5 special case for tools-devel.
- Use /bin/true --help as sanity test.

* Wed Apr 10 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-0.3.RC1
- Enable full regtest on all fedora arches.
- Make sure that patched a.c is not newer than cgout-test.
- Update valgrind-3.15.0-gdb-output1.patch to upstream version.
- Add valgrind-3.15.0-filter-libc-futex.patch.
- Add valgrind-3.15.0-mmap-32bit.patch.

* Tue Apr  9 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-0.2.RC1
- Add valgrind-3.15.0-s390x-get-startregs-constraint.patch
- Add valgrind-3.15.0-missing-a-c.patch
- Add valgrind-3.15.0-libstdc++-supp.patch
- Add valgrind-3.15.0-dhat-x86.patch
- Add valgrind-3.15.0-gdb-output1.patch
- Add valgrind-3.15.0-gdb-output2.patch

* Mon Apr  8 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.15.0-0.1.RC1
- Remove patches to prebuild files and always ./autogen.sh.
- Only ever build primary arch. Put tools under libexec.
- Update to upstream 3.15.0-RC1.
- Drop all upstreamed patches.

* Mon Mar  4 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-16
- Add valgrind-3.14.0-gettid.patch

* Mon Mar  4 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-15
- Add valgrind-3.14.0-ppc64-quotactl.patch

* Thu Feb 21 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-14
- Add valgrind-3.14.0-ppc-subfe.patch

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 1:3.14.0-13
- Rebuild for openmpi 3.1.3

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.14.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-11
- Add valgrind-3.14.0-s390x-vec-facility-bit.patch.

* Wed Jan  9 2019 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-10
- Add valgrind-3.14.0-rsp-clobber.patch
- Add valgrind-3.14.0-subrange_type-count.patch

* Mon Dec 31 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-9
- Add valgrind-3.14.0-vbit-test-sec.patch
- Add valgrind-3.14.0-x86-Iop_Sar64.patch
- Add valgrind-3.14.0-power9-addex.patch

* Thu Dec 20 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-8
- Update valgrind-3.14.0-jm-vmx-constraints.patch for ppc64.
- Show all diff files in check, not just the main/default one.

* Fri Dec 14 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-7
- Add valgrind-3.14.0-arm64-ptrace-traceme.patch
- Add valgrind-3.14.0-mc_translate-vecret.patch

* Wed Dec 12 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-6
- Add valgrind-3.14.0-final_tidyup.patch
- Add valgrind-3.14.0-ppc64-ldbrx.patch
- Add valgrind-3.14.0-ppc64-unaligned-words.patch
- Add valgrind-3.14.0-ppc64-lxvd2x.patch
- Add valgrind-3.14.0-ppc64-unaligned-vecs.patch
- Add valgrind-3.14.0-ppc64-lxvb16x.patch
- Add valgrind-3.14.0-set_AV_CR6.patch
- Add valgrind-3.14.0-undef_malloc_args.patch
- Add valgrind-3.14.0-jm-vmx-constraints.patch
- Add valgrind-3.14.0-sigkill.patch
- Add valgrind-3.14.0-ppc64-ptrace.patch

* Sat Dec  1 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.14.0-5
- Add valgrind-3.14.0-wcsncmp.patch (#1645971)
- Replace valgrind-3.14.0-s390x-vec-float-point-{code,test}.patch
  with upstream versions.

* Fri Nov 23 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.14.0-4
- Add valgrind-3.14.0-get_otrack_shadow_offset_wrk-ppc.patch,
  valgrind-3.14.0-new-strlen-IROps.patch,
  valgrind-3.14.0-ppc-instr-new-IROps.patch,
  valgrind-3.14.0-memcheck-new-IROps.patch,
  valgrind-3.14.0-ppc-frontend-new-IROps.patch,
  valgrind-3.14.0-transform-popcount64-ctznat64.patch and
  valgrind-3.14.0-enable-ppc-Iop_Sar_Shr8.patch (#1652926)

* Wed Nov 21 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.14.0-3
- Add valgrind-3.14.0-s390z-more-z13-fixes.patch.

* Tue Nov 20 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.14.0-2
- Add valgrind-3.14.0-s390x-fix-reg-alloc-vr-vs-fpr.patch.
- Add valgrind-3.14.0-s390x-sign-extend-lochi.patch.
- Add valgrind-3.14.0-s390x-vec-reg-vgdb.patch.
- Add valgrind-3.14.0-s390x-vec-float-point-code.patch
  and valgrind-3.14.0-s390x-vec-float-point-tests.patch
- Disable full regtests on fedora everywhere.

* Tue Oct  9 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.14.0-1
- valgrind 3.14.0 final.

* Thu Oct  4 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.14.0-0.2.RC2
- Upgrade to RC2.
- Drop valgrind-3.14.0-add-vector-h.patch.

* Fri Sep 14 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.14.0-0.1.GIT
- New upstream (pre-)release.
- Add valgrind-3.14.0-add-vector-h.patch.

* Fri Aug 10 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.13.0-28
- Add valgrind-3.13.0-utime.patch

* Fri Aug  3 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.13.0-27
- Add valgrind-3.13.0-ppc64-xsmaxcdp.patch

* Fri Aug  3 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.13.0-26
- Use valgrind_arches for ExclusiveArch when defined.
- Use restorecon for scl on rhel6 to work around rpm bug (#1610676).

* Tue Jul 31 2018 Mark Wielaard  <mjw@fedoraproject.org> - 3.13.0-25
- Add valgrind-3.13.0-x86-arch_prctl.patch (#1610304)

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 3.13.0-24
- Rebuild with fixed binutils

* Fri Jul 27 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-23
- Remove valgrind-3.13.0-arm-disable-vfp-test.patch

* Thu Jul 26 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-22
- Add valgrind-3.13.0-arch_prctl.patch (#1608824)

* Thu Jul 12 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-21
- Add valgrind-3.13.0-separate-code.patch (#1600034)
- Add valgrind-3.13.0-arm-disable-vfp-test.patch

* Thu Jul  5 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-20
- Don't try a full_regtest under scl, also don't adjust PATH.

* Thu Apr 12 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-19
- Improved valgrind-3.13.0-arm64-hwcap.patch
- Add valgrind-3.13.0-arm64-ptrace.patch

* Thu Apr 12 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-18
- Add valgrind-3.13.0-build-id-phdrs.patch (#1566639)

* Tue Feb 27 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-17
- Add valgrind-3.13.0-ppc64-mtfprwa-constraint.patch.

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.13.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-15
- Split valgrind-tools-devel from valgrind-devel.
- Make building of libmpi wrapper explicit.

* Mon Jan 22 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-14
- undefine _strict_symbol_defs_build.

* Tue Jan  2 2018 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-13
- Add additional fix to valgrind-3.13.0-debug-alt-file.patch.

* Tue Dec 12 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-12
- Add valgrind-3.13.0-s390-cgijnl.patch.
- Use upstream version of valgrind-3.13.0-debug-alt-file.patch.

* Sun Dec 10 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-11
- Add valgrind-3.13.0-debug-alt-file.patch.

* Thu Nov  2 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-10
- Add valgrind-3.13.0-ppc64-timebase.patch.

* Tue Oct 17 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-9
- Add valgrind-3.13.0-amd64-eflags-tests.patch
- Add valgrind-3.13.0-suppress-dl-trampoline-sse-avx.patch
- Add valgrind-3.13.0-static-tls.patch

* Mon Oct 16 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-8
- Add valgrind-3.13.0-ppc64-vex-fixes.patch

* Thu Aug 17 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-7
- Add valgrind-3.13.0-xml-socket.patch

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul  7 2017 Mark Wielaard <mjw@fedoraproject.org>
- Add --error-exitcode=1 to /bin/true check.

* Thu Jun 29 2017 Mark Wielaard <mjw@fedoraproject.org> 3.13.0-4
- Add valgrind-3.13.0-arm-index-hardwire.patch (#1466017)
- Add valgrind-3.13.0-ucontext_t.patch
- Add valgrind-3.13.0-gdb-8-testfix.patch
- Add valgrind-3.13.0-disable-vgdb-child.patch

* Fri Jun 23 2017 Mark Wielaard <mjw@fedoraproject.org> 3.13.0-3
- Add valgrind-3.13.0-arm64-hwcap.patch (#1464211)

* Sat Jun 17 2017 Mark Wielaard <mjw@fedoraproject.org> 3.13.0-2
- Add valgrind-3.13.0-ppc64-check-no-vsx.patch
- Add valgrind-3.13.0-epoll_pwait.patch (#1462258)
- Add valgrind-3.13.0-ppc64-diag.patch

* Thu Jun 15 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-1
- valgrind 3.13.0 final.
- Drop all upstreamed patches.

* Tue Jun  6 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-0.2.RC1
- Add valgrind-3.13.0-arm-dcache.patch
- Add valgrind-3.13.0-g++-4.4.patch
- Add valgrind-3.13.0-s390x-GI-strcspn.patch
- Add valgrind-3.13.0-xtree-callgrind.patch

* Fri Jun  2 2017 Mark Wielaard <mjw@fedoraproject.org> - 3.13.0-0.1.RC1
- Update description as suggested by Ivo Raisr.
- Workaround gdb/python bug in testsuite (#1434601)
- Update to upstream 3.13.0-RC1.
- Drop all upstreamed patches.

* Tue Mar 28 2017 Mark Wielaard <mjw@redhat.com> - 3.12.0-8
- Add valgrind-3.12.0-powerpc-register-pair.patch
- Add valgrind-3.12.0-ppc64-isa-3_00.patch

* Sat Feb 18 2017 Mark Wielaard <mjw@redhat.com> - 3.12.0-7
- Add valgrind-3.12.0-aarch64-syscalls.patch

* Sat Feb 18 2017 Mark Wielaard <mjw@redhat.com> - 3.12.0-6
- Add valgrind-3.12.0-arm64-ppc64-prlimit64.patch
- Add valgrind-3.12.0-arm64-hint.patch
- Add valgrind-3.12.0-clone-spawn.patch
- Add valgrind-3.12.0-quick-fatal-sigs.patch
- Add valgrind-3.12.0-exit_group.patch
- Add valgrind-3.12.0-deregister-stack.patch
- Add valgrind-3.12.0-x86-gdt-and-ss.patch
- Add valgrind-3.12.0-cd-dvd-ioctl.patch
- Add valgrind-3.12.0-tests-cxx11_abi_0.patch
- Add valgrind-3.12.0-helgrind-dl_allocate_tls-supp.patch
- Add valgrind-3.12.0-ppc-xxsel.patch

* Fri Feb 17 2017 Mark Wielaard <mjw@redhat.com> - 3.12.0-5
- Add valgrind-3.12.0-ppc64-r2.patch (#1424367)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 12 2016 Mark Wielaard <mjw@redhat.com> - 3.12.0-3
- Add valgrind-3.12.0-nocwd-cleanup.patch (#1390282)

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1:3.12.0-2
- Rebuild for openmpi 2.0

* Fri Oct 21 2016 Mark Wielaard <mjw@redhat.com> - 3.12.0-1
- Update to valgrind 3.12.0 release.

* Thu Oct 20 2016 Mark Wielaard <mjw@redhat.com> - 3.12.0-0.4-RC2
- Update to 3.12.0-RC1. Drop integrated patches.
- Add valgrind-3.12.0-skip-cond-var.patch

* Fri Sep 30 2016 Mark Wielaard <mjw@redhat.com> - 3.12.0-0.3-BETA1
- Clear CFLAGS, CXXFLAGS and LDFLAGS during make check.

* Thu Sep 29 2016 Mark Wielaard <mjw@redhat.com> - 3.12.0-0.2-BETA1
- Add valgrind-3.12-beta1-ppc64be.patch.
- Enable gdb_server tests again.

* Tue Sep 20 2016 Mark Wielaard <mjw@redhat.com> - 3.12.0-0.1-BETA1
- Update to valgrind 3.12.0 pre-release.
  - Drop upstreamed patches.
  - Disable exp-tests in %%check. GDB crashes on gdb_server tests.

* Fri Jul 22 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-26
- Only build valgrind-openmpi when not creating a software collection.
- No support for multilib on secondary arches when creating scl.
- Touch up empty .exp files.

* Thu Jul 21 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-24
- Mandatory Perl build-requires added
- Add valgrind-3.11.0-shr.patch
- Add valgrind-3.11.0-pcmpxstrx-0x70-0x19.patch
- Update valgrind-3.11.0-wrapmalloc.patch
- Add valgrind-3.11.0-sighandler-stack.patch

* Tue Jun 21 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-23
- Update valgrind-3.11.0-ppoll-mask.patch (#1344082)

* Mon May 30 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-22
- Add valgrind-3.11.0-arm64-handle_at.patch
- Add valgrind-3.11.0-ppc64-syscalls.patch

* Fri Apr 29 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-21
- Add valgrind-3.11.0-deduppoolalloc.patch
- Add valgrind-3.11.0-ppc-bcd-addsub.patch
- Add valgrind-3.11.0-ppc64-vgdb-vr-regs.patch

* Fri Apr 15 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-20
- Update valgrind-3.11.0-cxx-freeres.patch (x86 final_tidyup fix)
- Add valgrind-3.11.0-s390x-risbgn.patch

* Sun Apr 03 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-19
- Add valgrind-3.11.0-cxx-freeres.patch (#1312647)
- Add valgrind-3.11.0-ppc64-separate-socketcalls.patch
- Add valgrind-3.11.0-isZeroU.patch
- Replace valgrind-3.11.0-arm64-ldpsw.patch with upstream version
- Add valgrind-3.11.0-ppc64-128bit-mod-carry.patch
- Add valgrind-3.11.0-amd64-fcom.patch
- Add valgrind-3.11.0-z13s.patch
- Add valgrind-3.11.0-gdb-test-filters.patch

* Mon Mar 14 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-18
- Update valgrind-3.11.0-libstdc++-supp.patch.
- Add valgrind-3.11.0-arm64-ldr-literal-test.patch.
- Add valgrind-3.11.0-arm64-ldpsw.patch

* Thu Mar 10 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-17
- Update valgrind-3.11.0-arm64-more-syscalls.patch
- Add valgrind-3.11.0-libstdc++-supp.patch (#1312647)

* Wed Mar 09 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-16
- Add valgrind-3.11.0-ppoll-mask.patch
- Add valgrind-3.11.0-arm64-more-syscalls.patch

* Wed Feb 24 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-15
- Add valgrind-3.11.0-s390-separate-socketcalls.patch
- Add valgrind-3.11.0-amd64-ld-index.patch

* Thu Feb 18 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-14
- Update valgrind-3.11.0-futex.patch (fix helgrind/drd regression).
- Update valgrind-3.11.0-x86_unwind.patch (include amd64 fix).

* Wed Feb 17 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-13
- Remove valgrind-3.11.0-no-stv.patch (gcc6 has been fixed).
- Add valgrind-3.11.0-futex.patch
- Add valgrind-3.11.0-s390x-popcnt.patch

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.11.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-11
- Add valgrind-3.11.0-no-stv.patch (GCC6 workaround).

* Mon Jan 25 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-10
- Add valgrind-3.11.0-drd_std_thread.patch GCC6 build fix.

* Fri Jan 22 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-9
- Fix valgrind-3.11.0-pthread_barrier.patch to apply with older patch.
- Fix multilib issue in config.h with HAVE_AS_AMD64_FXSAVE64.

* Thu Jan 21 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-8
- Add valgrind-3.11.0-rlimit_data.patch
- Add valgrind-3.11.0-fclose.patch
- Add valgrind-3.11.0-pthread_spin_destroy.patch
- Add valgrind-3.11.0-socketcall-x86-linux.patch
- Don't strip debuginfo from vgpreload libaries.
  Enable dwz for everything else again.
- Add valgrind-3.11.0-is_stmt.patch
- Add valgrind-3.11.0-x86_unwind.patch

* Tue Jan 19 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-7
- Add valgrind-3.11.0-pthread_barrier.patch

* Sat Jan 16 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-6
- Add valgrind-3.11.0-aspacemgr.patch (#1283774)

* Sun Nov 15 2015 Mark Wielaard <mjw@redhat.com> - 3.11.0-5
- Add valgrind-3.11.0-wrapmalloc.patch

* Mon Oct 12 2015 Mark Wielaard <mjw@redhat.com> - 3.11.0-4
- Fix parenthesis in valgrind-3.11.0-rexw-cvtps2pd.patch.
- Add valgrind-3.11.0-s390-hwcap.patch

* Mon Oct 12 2015 Mark Wielaard <mjw@redhat.com> - 3.11.0-3
- Add valgrind-3.11.0-rexw-cvtps2pd.patch.

* Thu Oct 01 2015 Mark Wielaard <mjw@redhat.com> - 3.11.0-2
- Add valgrind-3.11.0-no-rdrand.patch

* Wed Sep 23 2015 Mark Wielaard <mjw@redhat.com> - 3.11.0-1
- Upgrade to valgrind 3.11.0 final
- Drop patches included upstream
  - valgrind-3.11.0-ppc-dfp-guard.patch
  - valgrind-3.11.0-ppc-ppr.patch
  - valgrind-3.11.0-ppc-mbar.patch
  - valgrind-3.11.0-glibc-futex-message.patch
  - valgrind-3.11.0-arm64-libvex_test.patch
  - valgrind-3.11.0-arm-warnings.patch
  - valgrind-3.11.0-arm-no-cast-align.patch
  - valgrind-3.11.0-ppc-vbit-test.patch
- Add arm64 syscall patches
  - valgrind-3.11.0-arm64-xattr.patch
  - valgrind-3.11.0-arm64-sigpending.patch

* Sat Sep 19 2015 Mark Wielaard <mjw@redhat.com> - 3.11.0-0.4.TEST1
- Add valgrind-3.11.0-ppc-dfp-guard.patch
- Add valgrind-3.11.0-ppc-ppr.patch
- Add valgrind-3.11.0-ppc-mbar.patch

* Fri Sep 18 2015 Mark Wielaard <mjw@redhat.com> - 3.11.0-0.3.TEST1
- Make sure some info about the system is in the build.log before check.
- Add valgrind-3.11.0-glibc-futex-message.patch
- Add valgrind-3.11.0-arm64-libvex_test.patch
- Add valgrind-3.11.0-arm-warnings.patch
- Add valgrind-3.11.0-arm-no-cast-align.patch
- Add valgrind-3.11.0-ppc-vbit-test.patch

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 1:3.11.0-0.2.TEST1
- Rebuild for openmpi 1.10.0

* Thu Sep 10 2015 Mark Wielaard <mjw@redhat.com> - 3.11.0-0.1.TEST1
- Add BuildRequires perl(Getopt::Long)
- Upgrade to valgrind 3.11.0.TEST1
- Remove upstreamed valgrind-3.10.1-gdb-file-warning.patch

* Tue Aug 25 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-22.svn20150825r15589
- Drop valgrind-3.9.0-stat_h.patch.
- Add BuildRequires gcc-c++.
- Update to current valgrind svn (svn20150825r15589)
- Add valgrind-3.10.1-gdb-file-warning.patch

* Mon Aug 17 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-21.svn20150817r15561
- Update to current valgrind svn. Drop patches now upstream.

* Mon Aug 17 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-20
- Don't try to move around libmpiwrap when not building for openmpi (s390x)

* Fri Aug 14 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-19
- Install libmpiwrap library under {_libdir}/openmpi/valgrind (#1238428)

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> - 1:3.10.1-18
- Rebuild for RPM MPI Requires Provides Change

* Mon Aug 10 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-17
- Add setuid and setresgid to valgrind-3.10.1-aarch64-syscalls.patch.

* Mon Aug 03 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-16
- Add valgrind-3.10.1-ppc64-hwcap2.patch

* Wed Jul 08 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-15
- Update valgrind-3.10.1-s390x-fiebra.patch

* Wed Jul 08 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-14
- Add valgrind-3.10.1-s390x-fiebra.patch

* Tue Jul 07 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-13
- Add valgrind-3.10.1-di_notify_mmap.patch
- Add valgrind-3.10.1-memmove-ld_so-ppc64.patch

* Fri Jun 19 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-12
- Add valgrind-3.10.1-kernel-4.0.patch.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.10.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 07 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-10
- Add valgrind-3.10.1-cfi-redzone.patch.

* Wed Jun 03 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-9
- Add valgrind-3.10.1-memfd_create.patch.
- Add valgrind-3.10.1-syncfs.patch.
- Add valgrind-3.10.1-arm-process_vm_readv_writev.patch.
- Add valgrind-3.10.1-fno-ipa-icf.patch.
- Add valgrind-3.10.1-demangle-q.patch

* Fri May 22 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-8
- Disable extended regtest on arm. The gdb tests hang for unknown reasons.
  The reason is a glibc bug #1196181 which causes:
  "GDB fails with Cannot parse expression `.L1055 4@r4'."

* Wed Apr 22 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-7
- Add valgrind-3.10-1-ppc64-sigpending.patch
- Filter out -fstack-protector-strong and disable _hardened_build.

* Wed Feb 18 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-6
- Add valgrind-3.10.1-send-recv-mmsg.patch
- Add mount and umount2 to valgrind-3.10.1-aarch64-syscalls.patch.
- Add valgrind-3.10.1-glibc-version-check.patch

* Tue Feb 10 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-5
- Add accept4 to valgrind-3.10.1-aarch64-syscalls.patch.
- Add valgrind-3.10.1-ppc64-accept4.patch.

* Sun Feb 08 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-4
- Add valgrind-3.10.1-aarch64-syscalls.patch.

* Thu Feb 05 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-3
- Add valgrind-3.10-s390-spechelper.patch.

* Tue Jan 13 2015 Mark Wielaard <mjw@redhat.com> - 3.10.1-2
- Add valgrind-3.10.1-mempcpy.patch.

* Wed Nov 26 2014 Mark Wielaard <mjw@redhat.com> - 3.10.1-1
- Upgrade to 3.10.1 final.

* Mon Nov 24 2014 Mark Wielaard <mjw@redhat.com> - 3.10.1-0.1.TEST1
- Upgrade to valgrind 3.10.1.TEST1
- Remove patches that are now upstream:
  - valgrind-3.10.0-old-ppc32-instr-magic.patch
  - valgrind-3.10.0-aarch64-syscalls.patch
  - valgrind-3.10.0-aarch64-dmb-sy.patch
  - valgrind-3.10.0-aarch64-frint.patch
  - valgrind-3.10.0-fcvtmu.patch
  - valgrind-3.10.0-aarch64-fcvta.patch

* Wed Nov 19 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-6
- Add getgroups/setgroups to valgrind-3.10.0-aarch64-syscalls.patch

* Tue Nov  4 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-5
- Merge valgrind-3.10.0-aarch64-times.patch
  and valgrind-3.10.0-aarch64-getsetsid.patch
  into valgrind-3.10.0-aarch64-syscalls.patch
  add fdatasync, msync, pread64, setreuid, setregid,
  mknodat, fchdir, chroot, fchownat, fchmod and fchown.
- Add valgrind-3.10.0-aarch64-frint.patch
- Add valgrind-3.10.0-fcvtmu.patch
- Add valgrind-3.10.0-aarch64-fcvta.patch

* Sat Oct 11 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-4
- Add valgrind-3.10.0-aarch64-times.patch
- Add valgrind-3.10.0-aarch64-getsetsid.patch
- Add valgrind-3.10.0-aarch64-dmb-sy.patch

* Mon Sep 15 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-3
- Add valgrind-3.10.0-old-ppc32-instr-magic.patch.

* Fri Sep 12 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-2
- Fix ppc32 multilib handling on ppc64[be].
- Drop ppc64 secondary for ppc32 primary support.
- Except for armv7hl we don't support any other arm[32] arch.

* Thu Sep 11 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-1
- Update to 3.10.0 final.
- Remove valgrind-3.10-configure-glibc-2.20.patch fixed upstream.

* Mon Sep  8 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-0.2.BETA2
- Update to 3.10.0.BETA2.
- Don't run dwz or generate minisymtab.
- Remove valgrind-3.9.0-s390x-ld-supp.patch fixed upstream.
- Add valgrind-3.10-configure-glibc-2.20.patch.

* Tue Sep  2 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-0.1.BETA1
- Update to official upstream 3.10.0 BETA1.
  - Enables inlined frames in stacktraces.

* Fri Aug 29 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-26.svn20140829r14384
- Update to upstream svn r14384
- Enable gdb_server tests again for arm and aarch64

* Wed Aug 27 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-25.svn20140827r14370
- Update to upstream svn r14370
- Remove ppc testfile copying (no longer patched in)

* Mon Aug 18 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-24.svn20140818r14303
- Update to upstream svn r14303
- Move fake libgcc into shared to not break post-regtest-checks.
- autogen.sh execution no longer needed in %%build.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.9.0-23.svn20140809r14250
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug  9 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-22.svn20140809r14250
- Update to upstream svn r14250
  - ppc64le support got integrated upstream. Remove patches:
    valgrind-3.9.0-ppc64le-initial.patch
    valgrind-3.9.0-ppc64le-functional.patch
    valgrind-3.9.0-ppc64le-test.patch
    valgrind-3.9.0-ppc64le-extra.patch

* Sat Jul 19 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-21.svn20140718r14176
- Disable full regtest on arm (gdb integration tests sometimes hang).

* Fri Jul 18 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-20.svn20140718r14176
- Update to upstream svn r14176
  Remove valgrind-3.9.0-arm64-user_regs.patch
- Add ppc64le support
  valgrind-3.9.0-ppc64le-initial.patch
  valgrind-3.9.0-ppc64le-functional.patch
  valgrind-3.9.0-ppc64le-test.patch
  valgrind-3.9.0-ppc64le-extra.patch

* Tue Jul 15 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-19.svn20140715r14165
- Add valgrind-3.9.0-arm64-user_regs.patch
- Disable full regtest on aarch64 (gdb integration tests sometimes hang).
- Enable openmpi support on aarch64.

* Tue Jul 15 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-18.svn20140715r14165
- Update to upstream svn r14165.
- Remove valgrind-3.9.0-ppc64-ifunc.patch.
- Remove valgrind-3.9.0-aarch64-glibc-2.19.90-gcc-4.9.patch
- Remove valgrind-3.9.0-format-security.patch
- Remove valgrind-3.9.0-msghdr.patch

* Fri Jul  4 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-17.svn20140513r13961
- Remove ppc multilib support (#1116110)
- Add valgrind-3.9.0-ppc64-ifunc.patch

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.9.0-16.svn20140513r13961
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Mark Wielaard <mjw@redhat.com>
- Don't cleanup fake 32-bit libgcc created in %%build.
  make regtest might depend on it to build -m32 binaries.

* Fri May 16 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-15.svn20140513r13961
- Add SHL_d_d_#imm to valgrind-3.9.0-aarch64-glibc-2.19.90-gcc-4.9.patch

* Thu May 15 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-14.svn20140513r13961
- Add valgrind-3.9.0-aarch64-glibc-2.19.90-gcc-4.9.patch

* Tue May 13 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-13.svn20140513r13961
- Update to upstream svn r13961.
- Remove valgrind-3.9.0-mpx.patch integrated upstream now.
- Add valgrind-3.9.0-msghdr.patch
- Add valgrind-3.9.0-format-security.patch

* Thu May 8 2014 Mark Wielaard <mjw@redhat.com> 3.9.0-12.svn20140319r13879
- Add valgrind-3.9.0-mpx.patch (#1087933)

* Wed Mar 19 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-11.svn20140319r13879
- Update to upstream svn r13879. arm64 make check now builds.

* Tue Mar 18 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-10.svn20140318r13876
- Make sure basic binary (/bin/true) runs under valgrind.
  And fail the whole build if not. The regtests are not zero-fail.
- Update to upstream svn r13876.
- Introduce build_openmpi and build_multilib in spec file.

* Tue Mar 11 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-9.svn20140311r13869
- Enable aarch64 based on current upstream svn. Removed upstreamed patches.
  Thanks to Marcin Juszkiewicz <mjuszkiewicz@redhat.com>

* Mon Mar 10 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-8
- Add valgrind-3.9.0-ppc64-priority.patch

* Mon Feb 24 2014 Mark Wielaard <mjw@redhat.com>
- Add upstream fixes to valgrind-3.9.0-timer_create.patch

* Fri Feb 21 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-7
- Add valgrind-3.9.0-glibc-2.19.patch

* Fri Feb 21 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-6
- Add valgrind-3.9.0-s390-dup3.patch
- Add valgrind-3.9.0-timer_create.patch

* Thu Dec 12 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-5
- Add valgrind-3.9.0-manpage-memcheck-options.patch.
- Add valgrind-3.9.0-s390-fpr-pair.patch.

* Thu Nov 28 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-4
- Add valgrind-3.9.0-xabort.patch.

* Fri Nov 22 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-3
- Add valgrind-3.9.0-anon-typedef.patch.
- Add valgrind-3.9.0-s390x-ld-supp.patch

* Wed Nov 20 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-2
- Add valgrind-3.9.0-dwz-alt-buildid.patch.
- Add valgrind-3.9.0-s390-risbg.patch.

* Fri Nov  1 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-1
- Upgrade to valgrind 3.9.0 final.
- Remove support for really ancient GCCs (valgrind-3.9.0-config_h.patch).
- Add valgrind-3.9.0-amd64_gen_insn_test.patch.
- Remove and cleanup fake 32-bit libgcc package.

* Mon Oct 28 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-0.1.TEST1
- Upgrade to valgrind 3.9.0.TEST1
- Remove patches that are now upstream:
  - valgrind-3.8.1-abbrev-parsing.patch
  - valgrind-3.8.1-af-bluetooth.patch
  - valgrind-3.8.1-aspacemgr_VG_N_SEGs.patch
  - valgrind-3.8.1-avx2-bmi-fma.patch.gz
  - valgrind-3.8.1-avx2-prereq.patch
  - valgrind-3.8.1-bmi-conf-check.patch
  - valgrind-3.8.1-capget.patch
  - valgrind-3.8.1-cfi_dw_ops.patch
  - valgrind-3.8.1-dwarf-anon-enum.patch
  - valgrind-3.8.1-filter_gdb.patch
  - valgrind-3.8.1-find-buildid.patch
  - valgrind-3.8.1-gdbserver_exit.patch
  - valgrind-3.8.1-gdbserver_tests-syscall-template-source.patch
  - valgrind-3.8.1-glibc-2.17-18.patch
  - valgrind-3.8.1-index-supp.patch
  - valgrind-3.8.1-initial-power-isa-207.patch
  - valgrind-3.8.1-manpages.patch
  - valgrind-3.8.1-memcheck-mc_translate-Iop_8HLto16.patch
  - valgrind-3.8.1-mmxext.patch
  - valgrind-3.8.1-movntdqa.patch
  - valgrind-3.8.1-new-manpages.patch
  - valgrind-3.8.1-openat.patch
  - valgrind-3.8.1-overlap_memcpy_filter.patch
  - valgrind-3.8.1-pie.patch
  - valgrind-3.8.1-pkg-config.patch
  - valgrind-3.8.1-power-isa-205-deprecation.patch
  - valgrind-3.8.1-ppc-32-mode-64-bit-instr.patch
  - valgrind-3.8.1-ppc-setxattr.patch
  - valgrind-3.8.1-proc-auxv.patch
  - valgrind-3.8.1-ptrace-include-configure.patch
  - valgrind-3.8.1-ptrace-setgetregset.patch
  - valgrind-3.8.1-ptrace-thread-area.patch
  - valgrind-3.8.1-regtest-fixlets.patch
  - valgrind-3.8.1-s390-STFLE.patch
  - valgrind-3.8.1-s390_tsearch_supp.patch
  - valgrind-3.8.1-sendmsg-flags.patch
  - valgrind-3.8.1-sigill_diag.patch
  - valgrind-3.8.1-static-variables.patch
  - valgrind-3.8.1-stpncpy.patch
  - valgrind-3.8.1-text-segment.patch
  - valgrind-3.8.1-wcs.patch
  - valgrind-3.8.1-x86_amd64_features-avx.patch
  - valgrind-3.8.1-xaddb.patch
  - valgrind-3.8.1-zero-size-sections.patch
- Remove special case valgrind-3.8.1-enable-armv5.patch.
- Remove valgrind-3.8.1-x86-backtrace.patch, rely on new upstream fp/cfi
  try-cache mechanism.

* Mon Oct 14 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-31
- Fix multilib issue with HAVE_PTRACE_GETREGS in config.h.

* Thu Sep 26 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-30
- Add valgrind-3.8.1-index-supp.patch (#1011713)

* Wed Sep 25 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-29
- Filter out -mcpu= so tests are compiled with the right flags. (#996927).

* Mon Sep 23 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-28
- Implement SSE4 MOVNTDQA insn (valgrind-3.8.1-movntdqa.patch)
- Don't BuildRequire /bin/ps, just BuildRequire procps
  (procps-ng provides procps).

* Thu Sep 05 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-27
- Fix power_ISA2_05 testcase (valgrind-3.8.1-power-isa-205-deprecation.patch)
- Fix ppc32 make check build (valgrind-3.8.1-initial-power-isa-207.patch)
- Add valgrind-3.8.1-mmxext.patch

* Wed Aug 21 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-26
- Allow building against glibc 2.18. (#999169)

* Thu Aug 15 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-25
- Add valgrind-3.8.1-s390-STFLE.patch
  s390 message-security assist (MSA) instruction extension not implemented.

* Wed Aug 14 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-24
- Add valgrind-3.8.1-power-isa-205-deprecation.patch
  Deprecation of some ISA 2.05 POWER6 instructions.
- Fixup auto-foo generation of new manpage doc patch.

* Wed Aug 14 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-23
- tests/check_isa-2_07_cap should be executable.

* Tue Aug 13 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-22
- Add valgrind-3.8.1-initial-power-isa-207.patch
  Initial ISA 2.07 support for POWER8-tuned libc.

* Thu Aug 08 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-21
- Don't depend on docdir location and version in openmpi subpackage
  description (#993938).
- Enable openmpi subpackage also on arm.

* Thu Aug 08 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-20
- Add valgrind-3.8.1-ptrace-include-configure.patch (#992847)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.8.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1:3.8.1-18
- Perl 5.18 rebuild

* Mon Jul 08 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-17
- Add valgrind-3.8.1-dwarf-anon-enum.patch
- Cleanup valgrind-3.8.1-sigill_diag.patch .orig file changes (#949687).
- Add valgrind-3.8.1-ppc-setxattr.patch
- Add valgrind-3.8.1-new-manpages.patch
- Add valgrind-3.8.1-ptrace-thread-area.patch
- Add valgrind-3.8.1-af-bluetooth.patch

* Tue May 28 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1:3.8.1-16
- Provide virtual -static package in -devel subpackage (#609624).

* Thu Apr 25 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-15
- Add valgrind-3.8.1-zero-size-sections.patch. Resolves issues with zero
  sized .eh_frame sections on ppc64.

* Thu Apr 18 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-14
- fixup selinux file context when doing a scl build.
- Enable regtest suite on ARM.
- valgrind-3.8.1-abbrev-parsing.patch, drop workaround, enable real fix.
- Fix -Ttext-segment configure check. Enables s390x again.
- BuildRequire ps for testsuite.

* Tue Apr 02 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-13
- Fix quoting in valgrind valgrind-3.8.1-enable-armv5.patch and
  remove arm configure hunk from valgrind-3.8.1-text-segment.patch #947440
- Replace valgrind-3.8.1-text-segment.patch with upstream variant.
- Add valgrind-3.8.1-regtest-fixlets.patch.

* Wed Mar 20 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-12
- Add valgrind-3.8.1-text-segment.patch
- Don't undefine _missing_build_ids_terminate_build.

* Tue Mar 12 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-11
- Add valgrind-3.8.1-manpages.patch

* Fri Mar 01 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-10
- Don't disable -debuginfo package generation, but do undefine
  _missing_build_ids_terminate_build.

* Thu Feb 28 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-9
- Replace valgrind-3.8.1-sendmsg-flags.patch with upstream version.

* Tue Feb 19 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-8
- Add valgrind-3.8.1-sendmsg-flags.patch
- Add valgrind-3.8.1-ptrace-setgetregset.patch
- Add valgrind-3.8.1-static-variables.patch

* Thu Feb 07 2013 Jon Ciesla <limburgher@gmail.com> 1:3.8.1-7
- Merge review fixes, BZ 226522.

* Wed Jan 16 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-6
- Allow building against glibc-2.17.

* Sun Nov  4 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-5
- Add valgrind-3.8.1-stpncpy.patch (KDE#309427)
- Add valgrind-3.8.1-ppc-32-mode-64-bit-instr.patch (#810992, KDE#308573)
- Add valgrind-3.8.1-sigill_diag.patch (#810992, KDE#309425)

* Tue Oct 16 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-4
- Add valgrind-3.8.1-xaddb.patch (#866793, KDE#307106)

* Mon Oct 15 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-3
- Add valgrind-3.8.1-x86_amd64_features-avx.patch (KDE#307285)
- Add valgrind-3.8.1-gdbserver_tests-syscall-template-source.patch (KDE#307155)
- Add valgrind-3.8.1-overlap_memcpy_filter.patch (KDE#307290)
- Add valgrind-3.8.1-pkg-config.patch (#827219, KDE#307729)
- Add valgrind-3.8.1-proc-auxv.patch (KDE#253519)
- Add valgrind-3.8.1-wcs.patch (#755242, KDE#307828)
- Add valgrind-3.8.1-filter_gdb.patch (KDE#308321)
- Add valgrind-3.8.1-gdbserver_exit.patch (#862795, KDE#308341)
- Add valgrind-3.8.1-aspacemgr_VG_N_SEGs.patch (#730303, KDE#164485)
- Add valgrind-3.8.1-s390_tsearch_supp.patch (#816244, KDE#308427)

* Fri Sep 21 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-2
- Add valgrind-3.8.1-gdbserver_tests-mcinvoke-ppc64.patch
- Replace valgrind-3.8.1-cfi_dw_ops.patch with version as committed upstream.
- Remove erroneous printf change from valgrind-3.8.1-abbrev-parsing.patch.
- Add scalar testcase change to valgrind-3.8.1-capget.patch.

* Thu Sep 20 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-1
- Add partial backport of upstream revision 12884
  valgrind-3.8.0-memcheck-mc_translate-Iop_8HLto16.patch
  without it AVX2 VPBROADCASTB insn is broken under memcheck.
- Add valgrind-3.8.0-cfi_dw_ops.patch (KDE#307038)
  DWARF2 CFI reader: unhandled DW_OP_ opcode 0x8 (DW_OP_const1u and friends)
- Add valgrind-3.8.0-avx2-prereq.patch.
- Remove accidentially included diffs for gdbserver_tests and helgrind/tests
  Makefile.in from valgrind-3.8.0-avx2-bmi-fma.patch.gz
- Remove valgrind-3.8.0-tests.patch tests no longer hang.
- Added SCL macros to support building as part of a Software Collection.
- Upgrade to valgrind 3.8.1.

* Wed Sep 12 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-8
- Add configure fixup valgrind-3.8.0-bmi-conf-check.patch

* Wed Sep 12 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-7
- Add valgrind-3.8.0-avx2-bmi-fma.patch (KDE#305728)

* Tue Sep 11 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-6
- Add valgrind-3.8.0-lzcnt-tzcnt-bugfix.patch (KDE#295808)
- Add valgrind-3.8.0-avx-alignment-check.patch (KDE#305926)

* Mon Aug 27 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-5
- Add valgrind-3.8.0-abbrev-parsing.patch for #849783 (KDE#305513).

* Sun Aug 19 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-4
- Add valgrind-3.8.0-find-buildid.patch workaround bug #849435 (KDE#305431).

* Wed Aug 15 2012 Jakub Jelinek <jakub@redhat.com> 3.8.0-3
- fix up last change

* Wed Aug 15 2012 Jakub Jelinek <jakub@redhat.com> 3.8.0-2
- tweak up <valgrind/config.h> to allow simultaneous installation
  of valgrind-devel.{i686,x86_64} (#848146)

* Fri Aug 10 2012 Jakub Jelinek <jakub@redhat.com> 3.8.0-1
- update to 3.8.0 release
- from CFLAGS/CXXFLAGS filter just fortification flags, not arch
  specific flags
- on i?86 prefer to use CFI over %%ebp unwinding, as GCC 4.6+
  defaults to -fomit-frame-pointer

* Tue Aug 07 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-0.1.TEST1.svn12858
- Update to 3.8.0-TEST1
- Clear CFLAGS CXXFLAGS LDFLAGS.
- Fix \ line continuation in configure line.

* Fri Aug 03 2012 Mark Wielaard <mjw@redhat.com> 3.7.0-7
- Fixup shadowing warnings valgrind-3.7.0-dwz.patch
- Add valgrind-3.7.0-ref_addr.patch (#842659, KDE#298864)

* Wed Jul 25 2012 Mark Wielaard <mjw@redhat.com> 3.7.0-6
- handle dwz DWARF compressor output (#842659, KDE#302901)
- allow glibc 2.16.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May  7 2012 Jakub Jelinek <jakub@redhat.com> 3.7.0-4
- adjust suppressions so that it works even with ld-2.15.so (#806854)
- handle DW_TAG_unspecified_type and DW_TAG_rvalue_reference_type
  (#810284, KDE#278313)
- handle .debug_types sections (#810286, KDE#284124)

* Sun Mar  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> 3.7.0-2
- Fix building on ARM platform

* Fri Jan 27 2012 Jakub Jelinek <jakub@redhat.com> 3.7.0-1
- update to 3.7.0 (#769213, #782910, #772343)
- handle some further SCSI ioctls (#783936)
- handle fcntl F_SETOWN_EX and F_GETOWN_EX (#770746)

* Wed Aug 17 2011 Adam Jackson <ajax@redhat.com> 3.6.1-6
- rebuild for rpm 4.9.1 trailing / bug

* Thu Jul 21 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-5
- handle PLT unwind info (#723790, KDE#277045)

* Mon Jun 13 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-4
- fix memcpy/memmove redirection on x86_64 (#705790)

* Wed Jun  8 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-3
- fix testing against glibc 2.14

* Wed Jun  8 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-2
- fix build on ppc64 (#711608)
- don't fail if s390x support patch hasn't been applied,
  move testing into %%check (#708522)
- rebuilt against glibc 2.14

* Wed Feb 23 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-1
- update to 3.6.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Jakub Jelinek <jakub@redhat.com> 3.6.0-2
- rebuilt against glibc 2.13 (#673046)
- hook in pwrite64 syscall on ppc64 (#672858)
- fix PIE handling on ppc/ppc64 (#665289)

* Fri Nov 12 2010 Jakub Jelinek <jakub@redhat.com> 3.6.0-1
- update to 3.6.0
- add s390x support (#632354)
- provide a replacement for str{,n}casecmp{,_l} (#626470)

* Tue May 18 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-18
- rebuilt against glibc 2.12

* Mon Apr 12 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-16
- change pub_tool_basics.h not to include config.h (#579283)
- add valgrind-openmpi package for OpenMPI support (#565541)
- allow NULL second argument to capget (#450976)

* Wed Apr  7 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-15
- handle i686 nopw insns with more than one data16 prefix (#574889)
- DWARF4 support
- handle getcpu and splice syscalls

* Wed Jan 20 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-14
- fix build against latest glibc headers

* Wed Jan 20 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-13
- DW_OP_mod is unsigned modulus instead of signed
- fix up valgrind.pc (#551277)

* Mon Dec 21 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-12
- don't require offset field to be set in adjtimex's
  ADJ_OFFSET_SS_READ mode (#545866)

* Wed Dec  2 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-10
- add handling of a bunch of recent syscalls and fix some
  other syscall wrappers (Dodji Seketeli)
- handle prelink created split of .bss into .dynbss and .bss
  and similarly for .sbss and .sdynbss (#539874)

* Wed Nov  4 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-9
- rebuilt against glibc 2.11
- use upstream version of the ifunc support

* Wed Oct 28 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-8
- add preadv/pwritev syscall support

* Tue Oct 27 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-7
- add perf_counter_open syscall support (#531271)
- add handling of some sbb/adc insn forms on x86_64 (KDE#211410)

* Fri Oct 23 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-6
- ppc and ppc64 fixes

* Thu Oct 22 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-5
- add emulation of 0x67 prefixed loop* insns on x86_64 (#530165)

* Wed Oct 21 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-4
- handle reading of .debug_frame in addition to .eh_frame
- ignore unknown DWARF3 expressions in evaluate_trivial_GX
- suppress helgrind race errors in helgrind's own mythread_wrapper
- fix compilation of x86 tests on x86_64 and ppc tests

* Wed Oct 14 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-3
- handle many more DW_OP_* ops that GCC now uses
- handle the more compact form of DW_AT_data_member_location
- don't strip .debug_loc etc. from valgrind binaries

* Mon Oct 12 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-2
- add STT_GNU_IFUNC support (Dodji Seketeli, #518247)
- wrap inotify_init1 syscall (Dodji Seketeli, #527198)
- fix mmap/mprotect handling in memcheck (KDE#210268)

* Fri Aug 21 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-1
- update to 3.5.0

* Tue Jul 28 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-7
- handle futex ops newly added during last 4 years (#512121)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-5
- add support for DW_CFA_{remember,restore}_state

* Mon Jul 13 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-4
- handle version 3 .debug_frame, .eh_frame, .debug_info and
  .debug_line (#509197)

* Mon May 11 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-3
- rebuilt against glibc 2.10.1

* Wed Apr 22 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-2
- redirect x86_64 ld.so strlen early (#495645)

* Mon Mar  9 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-1
- update to 3.4.1

* Mon Feb  9 2009 Jakub Jelinek <jakub@redhat.com> 3.4.0-3
- update to 3.4.0

* Wed Apr 16 2008 Jakub Jelinek <jakub@redhat.com> 3.3.0-3
- add suppressions for glibc 2.8
- add a bunch of syscall wrappers (#441709)

* Mon Mar  3 2008 Jakub Jelinek <jakub@redhat.com> 3.3.0-2
- add _dl_start suppression for ppc/ppc64

* Mon Mar  3 2008 Jakub Jelinek <jakub@redhat.com> 3.3.0-1
- update to 3.3.0
- split off devel bits into valgrind-devel subpackage

* Thu Oct 18 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-7
- add suppressions for glibc >= 2.7

* Fri Aug 31 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-6
- handle new x86_64 nops (#256801, KDE#148447)
- add support for private futexes (KDE#146781)
- update License tag

* Fri Aug  3 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-5
- add ppc64-linux symlink in valgrind ppc.rpm, so that when
  rpm prefers 32-bit binaries over 64-bit ones 32-bit
  /usr/bin/valgrind can find 64-bit valgrind helper binaries
  (#249773)
- power5+ and power6 support (#240762)

* Thu Jun 28 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-4
- pass GDB=%%{_prefix}/gdb to configure to fix default
  --db-command (#220840)

* Wed Jun 27 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-3
- add suppressions for glibc >= 2.6
- avoid valgrind internal error if io_destroy syscall is
  passed a bogus argument

* Tue Feb 13 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-2
- fix valgrind.pc again

* Tue Feb 13 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-1
- update to 3.2.3

* Wed Nov  8 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-7
- some cachegrind improvements (Ulrich Drepper)

* Mon Nov  6 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-6
- fix valgrind.pc (#213149)
- handle Intel Core2 cache sizes in cachegrind (Ulrich Drepper)

* Wed Oct 25 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-5
- fix valgrind on ppc/ppc64 where PAGESIZE is 64K (#211598)

* Sun Oct  1 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-4
- adjust for glibc-2.5

* Wed Sep 27 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-3
- another DW_CFA_set_loc handling fix

* Tue Sep 26 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-2
- fix openat handling (#208097)
- fix DW_CFA_set_loc handling

* Tue Sep 19 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-1
- update to 3.2.1 bugfix release
  - SSE3 emulation fixes, reduce memcheck false positive rate,
    4 dozens of bugfixes

* Mon Aug 21 2006 Jakub Jelinek <jakub@redhat.com> 3.2.0-5
- handle the new i686/x86_64 nops (#203273)

* Fri Jul 28 2006 Jeremy Katz <katzj@redhat.com> - 1:3.2.0-4
- rebuild to bring ppc back

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.2.0-3.1
- rebuild

* Fri Jun 16 2006 Jakub Jelinek <jakub@redhat.com> 3.2.0-3
- handle [sg]et_robust_list syscall on ppc{32,64}

* Fri Jun 16 2006 Jakub Jelinek <jakub@redhat.com> 3.2.0-2
- fix ppc64 symlink to 32-bit valgrind libdir
- handle a few extra ppc64 syscalls

* Thu Jun 15 2006 Jakub Jelinek <jakub@redhat.com> 3.2.0-1
- update to 3.2.0
  - ppc64 support

* Fri May 26 2006 Jakub Jelinek <jakub@redhat.com> 3.1.1-3
- handle [sg]et_robust_list syscalls on i?86/x86_64
- handle *at syscalls on ppc
- ensure on x86_64 both 32-bit and 64-bit glibc{,-devel} are
  installed in the buildroot (#191820)

* Wed Apr 12 2006 Jakub Jelinek <jakub@redhat.com> 3.1.1-2
- handle many syscalls that were unhandled before, especially on ppc

* Mon Apr  3 2006 Jakub Jelinek <jakub@redhat.com> 3.1.1-1
- upgrade to 3.1.1
  - many bugfixes

* Mon Mar 13 2006 Jakub Jelinek <jakub@redhat.com> 3.1.0-2
- add support for DW_CFA_val_offset{,_sf}, DW_CFA_def_cfa_sf
  and skip over DW_CFA_val_expression quietly
- adjust libc/ld.so filenames in glibc-2.4.supp for glibc 2.4
  release

* Mon Jan  9 2006 Jakub Jelinek <jakub@redhat.com> 3.1.0-1
- upgrade to 3.1.0 (#174582)
  - many bugfixes, ppc32 support

* Thu Oct 13 2005 Jakub Jelinek <jakub@redhat.com> 3.0.1-2
- remove Obsoletes for valgrind-callgrind, as it has been
  ported to valgrind 3.0.x already

* Sun Sep 11 2005 Jakub Jelinek <jakub@redhat.com> 3.0.1-1
- upgrade to 3.0.1
  - many bugfixes
- handle xattr syscalls on x86-64 (Ulrich Drepper)

* Fri Aug 12 2005 Jakub Jelinek <jakub@redhat.com> 3.0.0-3
- fix amd64 handling of cwtd instruction
- fix amd64 handling of e.g. sarb $0x4,val(%%rip)
- speedup amd64 insn decoding

* Fri Aug 12 2005 Jakub Jelinek <jakub@redhat.com> 3.0.0-2
- lower x86_64 stage2 base from 112TB down to 450GB, so that
  valgrind works even on 2.4.x kernels.  Still way better than
  1.75GB that stock valgrind allows

* Fri Aug 12 2005 Jakub Jelinek <jakub@redhat.com> 3.0.0-1
- upgrade to 3.0.0
  - x86_64 support
- temporarily obsolete valgrind-callgrind, as it has not been
  ported yet

* Tue Jul 12 2005 Jakub Jelinek <jakub@redhat.com> 2.4.0-3
- build some insn tests with -mmmx, -msse or -msse2 (#161572)
- handle glibc-2.3.90 the same way as 2.3.[0-5]

* Wed Mar 30 2005 Jakub Jelinek <jakub@redhat.com> 2.4.0-2
- resurrect the non-upstreamed part of valgrind_h patch
- remove 2.1.2-4G patch, seems to be upstreamed
- resurrect passing -fno-builtin in memcheck tests

* Sun Mar 27 2005 Colin Walters <walters@redhat.com> 2.4.0-1
- New upstream version 
- Update valgrind-2.2.0-regtest.patch to 2.4.0; required minor
  massaging
- Disable valgrind-2.1.2-4G.patch for now; Not going to touch this,
  and Fedora does not ship 4G kernel by default anymore
- Remove upstreamed valgrind-2.2.0.ioctls.patch
- Remove obsolete valgrind-2.2.0-warnings.patch; Code is no longer
  present
- Remove upstreamed valgrind-2.2.0-valgrind_h.patch
- Remove obsolete valgrind-2.2.0-unnest.patch and
  valgrind-2.0.0-pthread-stacksize.patch; valgrind no longer
  includes its own pthread library

* Thu Mar 17 2005 Jakub Jelinek <jakub@redhat.com> 2.2.0-10
- rebuilt with GCC 4

* Tue Feb  8 2005 Jakub Jelinek <jakub@redhat.com> 2.2.0-8
- avoid unnecessary use of nested functions for pthread_once
  cleanup

* Mon Dec  6 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-7
- update URL (#141873)

* Tue Nov 16 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-6
- act as if NVALGRIND is defined when using <valgrind.h>
  in non-m32/i386 programs (#138923)
- remove weak from VALGRIND_PRINTF*, make it static and
  add unused attribute

* Mon Nov  8 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-4
- fix a printout and possible problem with local variable
  usage around setjmp (#138254)

* Tue Oct  5 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-3
- remove workaround for buggy old makes (#134563)

* Fri Oct  1 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-2
- handle some more ioctls (Peter Jones, #131967)

* Thu Sep  2 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-1
- update to 2.2.0

* Thu Jul 22 2004 Jakub Jelinek <jakub@redhat.com> 2.1.2-3
- fix packaging of documentation

* Tue Jul 20 2004 Jakub Jelinek <jakub@redhat.com> 2.1.2-2
- allow tracing of 32-bit binaries on x86-64

* Tue Jul 20 2004 Jakub Jelinek <jakub@redhat.com> 2.1.2-1
- update to 2.1.2
- run make regtest as part of package build
- use glibc-2.3 suppressions instead of glibc-2.2 suppressions

* Thu Apr 29 2004 Colin Walters <walters@redhat.com> 2.0.0-1
- update to 2.0.0

* Tue Feb 25 2003 Jeff Johnson <jbj@redhat.com> 1.9.4-0.20030228
- update to 1.9.4 from CVS.
- dwarf patch from Graydon Hoare.
- sysinfo patch from Graydon Hoare, take 1.

* Fri Feb 14 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-6.20030207
- add return codes to syscalls.
- fix: set errno after syscalls.

* Tue Feb 11 2003 Graydon Hoare <graydon@redhat.com> 1.9.3-5.20030207
- add handling for separate debug info (+fix).
- handle blocking readv/writev correctly.
- comment out 4 overly zealous pthread checks.

* Tue Feb 11 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-4.20030207
- move _pthread_desc to vg_include.h.
- implement pthread_mutex_timedlock().
- implement pthread_barrier_wait().

* Mon Feb 10 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-3.20030207
- import all(afaik) missing functionality from linuxthreads.

* Sun Feb  9 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-2.20030207
- import more missing functionality from linuxthreads in glibc-2.3.1.

* Sat Feb  8 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-1.20030207
- start fixing nptl test cases.

* Fri Feb  7 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-0.20030207
- build against current 1.9.3 with nptl hacks.

* Tue Oct 15 2002 Alexander Larsson <alexl@redhat.com>
- Update to 1.0.4

* Fri Aug  9 2002 Alexander Larsson <alexl@redhat.com>
- Update to 1.0.0

* Wed Jul  3 2002 Alexander Larsson <alexl@redhat.com>
- Update to pre4.

* Tue Jun 18 2002 Alexander Larsson <alla@lysator.liu.se>
- Add threadkeys and extra suppressions patches. Bump epoch.

* Mon Jun 17 2002 Alexander Larsson <alla@lysator.liu.se>
- Updated to 1.0pre1

* Tue May 28 2002 Alex Larsson <alexl@redhat.com>
- Updated to 20020524. Added GLIBC_PRIVATE patch

* Thu May  9 2002 Jonathan Blandford <jrb@redhat.com>
- add missing symbol __pthread_clock_settime

* Wed May  8 2002 Alex Larsson <alexl@redhat.com>
- Update to 20020508

* Mon May  6 2002 Alex Larsson <alexl@redhat.com>
- Update to 20020503b

* Thu May  2 2002 Alex Larsson <alexl@redhat.com>
- update to new snapshot

* Mon Apr 29 2002 Alex Larsson <alexl@redhat.com> 20020428-1
- update to new snapshot

* Fri Apr 26 2002 Jeremy Katz <katzj@redhat.com> 20020426-1
- update to new snapshot

* Thu Apr 25 2002 Alex Larsson <alexl@redhat.com> 20020424-5
- Added stack patch. Commented out other patches.

* Wed Apr 24 2002 Nalin Dahyabhai <nalin@redhat.com> 20020424-4
- filter out GLIBC_PRIVATE requires, add preload patch

* Wed Apr 24 2002 Alex Larsson <alexl@redhat.com> 20020424-3
- Make glibc 2.2 and XFree86 4 the default supressions

* Wed Apr 24 2002 Alex Larsson <alexl@redhat.com> 20020424-2
- Added patch that includes atomic.h

* Wed Apr 24 2002 Alex Larsson <alexl@redhat.com> 20020424-1
- Initial build
