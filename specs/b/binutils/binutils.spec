# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


Summary: A GNU collection of binary utilities
Name: binutils%{?_with_debug:-debug}
# Note - a version number of X.XX is an offical upstream GNU Binutils release.
# A version number of X.XX.50 is a snapshot of the upstream development sources.
# A version number of X.XX.90 is a pre-release snapshot.
# The variable %%{source} (see below) should be set to indicate which of these
# origins is being used.
Version: 2.45.1
Release: 4%{?dist}
License: GPL-3.0-or-later AND (GPL-3.0-or-later WITH Bison-exception-2.2) AND (LGPL-2.0-or-later WITH GCC-exception-2.0) AND BSD-3-Clause AND GFDL-1.3-or-later AND GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-or-later
URL: https://sourceware.org/binutils

#---Start of Configure Options-----------------------------------------------

# The binutils can be built with the following parameters to change
#  the default behaviour:

# --with    bootstrap    Build with minimal dependencies.
# --with    clang        Force building with CLANG instead of GCC.
# --with    crossbuilds  Build cross targeted versions of the binutils as well as natives.
# --with    debug        Build without optimizations and without splitting the debuginfo into a separate file.
# --without debuginfod   Disable support for debuginfod.
# --without docs         Skip building documentation.  Default is with docs, except when building a cross binutils.
# --without gold         Disable building of the GOLD linker.
# --without gprofng      Do not build the GprofNG profiler.
# --without systemzlib   Use the binutils version of zlib.  Default is to use the system version.
# --without testsuite    Do not run the testsuite.  Default is to run it.
# --without xxhash       Do not link against the xxhash library.

# Other configuration options can be set by modifying the following defines.

# Create shared libraries.
%define enable_shared 1

# Create deterministic archives (ie ones without timestamps).
# Default is off because of BZ 1195883.
%define enable_deterministic_archives 0

# Generate a warning when linking creates an executable stack
%define warn_for_executable_stacks 1

# Generate a warning when linking creates a segment with read, write and execute permissions
%define warn_for_rwx_segments 1

# Turn the above warnings into errors.
# Only effective if the warnings are enabled.
# Disabled by default because this is now handled by a macro in redhat-rpm-config.
%define error_for_executable_stacks 0
%define error_for_rwx_segments 0

# Enable support for GCC LTO compilation.
# Disable if it is necessary to work around bugs in LTO.
%define enable_lto 1

# Enable support for generating new dtags in the linker
# Disable if it is necessary to use RPATH instead.
# Currently enabled for Fedora, disabled for RHEL.
%if 0%{?fedora} != 0
%define enable_new_dtags 1
%else
%define enable_new_dtags 0
%endif

# Enable the compression of debug sections as default behaviour of the
# assembler and linker.  This option is disabled for now.  The assembler and
# linker have command line options to override the default behaviour.
%define default_compress_debug 0

# Default to read-only-relocations (relro) in shared binaries.
# This is enabled as a security feature.
%define default_relro 1

# Enable the default generation of GNU Build notes by the assembler.
# This option is disabled as it has turned out to be problematic for the i686
# architecture, although the exact reason has not been determined.  (See
# BZ 1572485).  It also breaks building EFI binaries on AArch64, as these
# cannot have relocations against absolute symbols.
%define default_generate_notes 0

# Enable thread support in the GOLD linker (if it is being built).  This is
# particularly important if plugins to the linker intend to use threads
# themselves.  See BZ 1636479 for more details.  This option is made
# configurable in case there is ever a need to disable thread support.
%define enable_threading 1

# Enable the use of separate code and data segments.  Whilst potentially
# useful from a security point of view, it is problematic from a file
# size point of view.  So for now, only enable it for the i686, x86_64
# and riscv64 architectures as these are the ones that have the most
# potential vulnerability.
%ifarch %{ix86} x86_64 riscv64
%define enable_separate_code 1
%else
%define enable_separate_code 0
%endif

# Indicate where the sources come from.
#
# Official releases come from:  https://ftp.gnu.org/gnu/binutils
# Pre releases come from:       https://sourceware.org/pub/binutils/snapshots/
# Snapshots come from:          https://snapshots.sourceware.org/binutils/trunk/
# Tarballs are made by hand following a process outlined in this document:
#                               https://fedoraproject.org/wiki/BinutilsRawhideSync
#
# Note - the Linux Kernel binutils releases are too unstable and contain
# too many controversial patches so we stick with the official GNU version
# instead.
#
# Note - there is a confusing misnomer in the URL for the pre-release tarballs.
# They are a "snapshot" of the about to be released branch sources, rather than
# a snapshot of the mainline development sources.

%define source official-release
# %%define source pre-release
# %%define source snapshot
# %%define source tarball

# For snapshots and tarballs an extension is used to indicate the commit ID.
# We need to know that so that the source extraction process will work
# correctly.  Note %%(echo) is used because you cannot directly set a
# spec variable to a hexadecimal string value.

%define commit_id %(echo "21e608528c3")

#----End of Configure Options------------------------------------------------

# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Not debug
%bcond_with debug
# Default: support debuginfod.
%bcond_without debuginfod
# Default: Always build documentation.
%bcond_without docs
# Default: build binutils-gprofng package.
%bcond_without gprofng
# Default: Use the system supplied version of the zlib compression library.
%bcond_without systemzlib
# Default: Always run the testsuite.
%bcond_without testsuite
# Default: Use the xxhash-devel library.
%bcond_without xxhash

# Note - in the future the gold linker may become deprecated.
%ifnarch riscv64
%bcond_without gold
%else
# RISC-V does not have ld.gold thus disable by default.
%bcond_with gold
%endif

# Allow the user to override the compiler used to build the binutils.
# The default build compiler is gcc if %%toolchain is not clang.
%if "%toolchain" == "clang"
%bcond_without clang
%else
%bcond_with clang
%endif

%if %{with clang}
%global toolchain clang
%else
%global toolchain gcc
%endif

# (Do not) create cross targeted versions of the binutils.
%bcond_with crossbuilds
# %%bcond_without crossbuilds

%if %{with bootstrap}
%undefine with_docs
%undefine with_testsuite
%undefine with_gprofng
%endif

%if %{with debug}
%undefine with_testsuite
%define enable_shared 0
%endif

# GprofNG currenly only supports the x86 and AArch64 architectures.
%ifnarch x86_64 aarch64
%undefine with_gprofng
%endif

# The opcodes library needs a few functions defined in the bfd
# library, but these symbols are not defined in the stub bfd .so
# that is available at link time.  (They are present in the real
# .so that is used at run time).
%undefine _strict_symbol_defs_build

# BZ 1924068.  Since applications that use the BFD library are
# required to link against the static version, ensure that it retains
# its debug informnation.
%undefine __brp_strip_static_archive

# ODD numbered upstream GNU Binutils releases do not include the sources
# for the GOLD linker, so we use a snapshot from the mainline development
# sources instead - but only for GOLD, not for the rest of the binutils.
#
# FIXME: Delete this once the gold linker is fully deprecated.
# %%define use_separate_gold_tarball 0
%define gold_tarball %(echo "binutils-with-gold-2.44.50-21e608528c3")

#----------------------------------------------------------------------------

%if "%{source}" == "official-release"
# Source0: https://ftp.gnu.org/gnu/binutils/binutils-with-gold-%%{version}.tar.xz
Source0: https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz
%endif
%if "%{source}" == "pre-release"
Source0: binutils-%{version}.tar.xz
%endif
%if "%{source}" == "snapshot"
Source0: binutils-with-gold-%{version}-%{commit_id}.tar.xz
%endif
%if "%{source}" == "tarball"
Source0: binutils-%{version}-%{commit_id}.tar.xz
%endif

Source1: binutils-2.19.50.0.1-output-format.sed
%if "%{gold_tarball}" != ""
Source2: %{gold_tarball}.tar.xz
%endif

#----------------------------------------------------------------------------

# Purpose:  Use /lib64 and /usr/lib64 instead of /lib and /usr/lib in the
#           default library search path of 64-bit targets.
# Lifetime: Permanent, but it should not be.  This is a bug in the libtool
#           sources used in both binutils and gcc, (specifically the
#           libtool.m4 file).  These are based on a version released in 2009
#           (2.2.6?) rather than the latest version.  (Definitely fixed in
#           libtool version 2.4.6).
Patch01: binutils-libtool-lib64.patch

# Purpose:  Appends a RHEL or Fedora release string to the generic binutils
#           version string.
# Lifetime: Permanent.  This is a RHEL/Fedora specific patch.
Patch02: binutils-version.patch

# Purpose:  Exports the demangle.h header file (associated with the libiberty
#           sources) with the binutils-devel rpm.
# Lifetime: Permanent.  This is a RHEL/Fedora specific patch.
Patch03: binutils-export-demangle.h.patch

# Purpose:  Disables the check in the BFD library's bfd.h header file that
#           config.h has been included before the bfd.h header.  See BZ
#           #845084 for more details.
# Lifetime: Permanent - but it should not be.  The bfd.h header defines
#           various types that are dependent upon configuration options, so
#           the order of inclusion is important.
# FIXME:    It would be better if the packages using the bfd.h header were
#           fixed so that they do include the header files in the correct
#           order.
Patch04: binutils-no-config-h-check.patch

# Purpose:  Disable an x86/x86_64 optimization that moves functions from the
#           PLT into the GOTPLT for faster access.  This optimization is
#           problematic for tools that want to intercept PLT entries, such
#           as ltrace and LD_AUDIT.  See BZs 1452111 and 1333481.
# Lifetime: Permanent.  But it should not be.
# FIXME:    Replace with a configure time option.
Patch05: binutils-revert-PLT-elision.patch

# Purpose:  Do not create PLT entries for AARCH64 IFUNC symbols referenced in
#           debug sections.
# Lifetime: Permanent.
# FIXME:    Find related bug.  Decide on permanency.
Patch06: binutils-2.27-aarch64-ifunc.patch

# Purpose:  Stop the binutils from statically linking with libstdc++.
# Lifetime: Permanent.
Patch07: binutils-do-not-link-with-static-libstdc++.patch

# Purpose:  Stop gold from aborting when input sections with the same name
#            have different flags.
# Lifetime: Fixed in 2.43 (maybe)
Patch08: binutils-gold-mismatched-section-flags.patch

# Purpose:  Change the gold configuration script to only warn about
#            unsupported targets.  This allows the binutils to be built with
#            BPF support enabled.
# Lifetime: Permanent.
Patch09: binutils-gold-warn-unsupported.patch

# Purpose:  Enable the creation of .note.gnu.property sections by the GOLD
#            linker for x86 binaries.
# Lifetime: Permanent.
Patch10: binutils-gold-i386-gnu-property-notes.patch

# Purpose:  Allow the binutils to be configured with any (recent) version of
#            autoconf.
# Lifetime: Fixed in 2.44 (maybe ?)
Patch11: binutils-autoconf-version.patch

# Purpose:  Stop libtool from inserting useless runpaths into binaries.
# Lifetime: Who knows.
Patch12: binutils-libtool-no-rpath.patch

# Purpose:  Stop an abort when using dwp to process a file with no dwo links.
# Lifetime: Fixed in 2.44 (maybe)
Patch13: binutils-gold-empty-dwp.patch

# Purpose:  Fix binutils testsuite failures.
# Lifetime: Permanent, but varies with each rebase.
Patch14: binutils-testsuite-fixes.patch

# Purpose:  Fix binutils testsuite failures for the RISCV-64 target.
# Lifetime: Permanent, but varies with each rebase.
Patch15: binutils-riscv-testsuite-fixes.patch

# Purpose:  Make the GOLD linker ignore the "-z pack-relative-relocs" command line option.
# Lifetime: Fixed in 2.44 (maybe)
Patch16: binutils-gold-pack-relative-relocs.patch

# Purpose:  Let the gold linker ignore --error-execstack and --error-rwx-segments.
# Lifetime: Fixed in 2.44 (maybe)
Patch17: binutils-gold-ignore-execstack-error.patch

# Purpose:  Fix the ar test of non-deterministic archives.
# Lifetime: Fixed in 2.44
Patch18: binutils-fix-ar-test.patch

# Purpose:  Fix a seg fault in the AArch64 linker when building u-boot.
# Lifetime: Fixed in 2.45
Patch19: binutils-aarch64-small-plt0.patch

# Purpose:  Stops a potential illegal memory access when linking a corrupt
#            input file.  PR 33457
# Lifetime: Fixed in 2.46
Patch20: binutils-CVE-2025-11083.patch

# Purpose:  Stops a potential illegal memory access when linking a corrupt
#            input file.  PR 33464
# Lifetime: Fixed in 2.46
Patch21: binutils-CVE-2025-11082.patch

#----------------------------------------------------------------------------

# Purpose:  Suppress the x86 linker's p_align-1 tests due to kernel bug on CentOS-10
# Lifetime: TEMPORARY
Patch99: binutils-suppress-ld-align-tests.patch

# Purpose: Disable GCS warnings when shared dependencies are not built with GCS
# support
# Lifetime: TEMPORARY
Patch100: binutils-disable-gcs-report-dynamic.patch
Patch101: binutils-disable-gcs-report-dynamic-tests.patch

#----------------------------------------------------------------------------

Provides: bundled(libiberty)

%if %{with debug}
# Define this if you want to skip the strip step and preserve debug info.
# Useful for testing.
%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}
%endif

# Perl, sed and touch are all used in the %%prep section of this spec file.
BuildRequires: autoconf, automake, perl, sed, coreutils, make

# bison is used to generate either gold/yyscript.c or ld/ldgram.c depending
# on the build architecture.
BuildRequires: bison

%if %{with clang}
BuildRequires: clang compiler-rt
%else
BuildRequires: gcc
%endif

%if %{with gold}
# The GOLD testsuite needs a static libc++
BuildRequires: libstdc++-static

%if ! %{with clang}
BuildRequires: gcc-c++
Conflicts: gcc-c++ < 4.0.0
%endif
%endif

%if %{without bootstrap}
BuildRequires: gettext, flex, jansson-devel
%if %{with systemzlib}
BuildRequires: zlib-devel
%endif
%endif

%if %{with docs}
BuildRequires: texinfo >= 4.0
# BZ 920545: We need pod2man in order to build the manual pages.
BuildRequires: /usr/bin/pod2man
%else
BuildRequires: findutils
%endif

# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
%if %{with testsuite}
# relro_test.sh uses dc which is part of the bc rpm, hence its inclusion here.
# sharutils is needed so that we can uuencode the testsuite results.
BuildRequires: dejagnu, glibc-static, sharutils, bc, libstdc++
%if %{with systemzlib}
BuildRequires: zlib-devel
%endif
%endif

%if %{with debuginfod}
BuildRequires: elfutils-debuginfod-client-devel
%endif

%if %{with xxhash}
BuildRequires: xxhash-devel
%endif

Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
# We also need rm.
Requires(post): coreutils

# %%if %%{with gold}
# # For now we make the binutils package require the gold sub-package.
# # That way other packages that have a requirement on "binutils" but
# # actually want gold will not have to be changed.  In the future, if
# # we decide to deprecate gold, we can remove this requirement, and
# # then update other packages as necessary.
# Requires: binutils-gold >= %%{version}
# %%endif

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%define _gnu %{nil}
%endif

#----------------------------------------------------------------------------

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).

#----------------------------------------------------------------------------

%package devel
Summary: BFD and opcodes static and dynamic libraries and header files
Provides: binutils-static = %{version}-%{release}
%if %{with systemzlib}
Requires: zlib-devel
%endif
Requires: binutils = %{version}-%{release}
# BZ 1215242: We need touch...
Requires: coreutils

%description devel
This package contains BFD and opcodes static and dynamic libraries.

The dynamic libraries are in this package, rather than a separate
base package because they are actually linker scripts that force
the use of the static libraries.  This is because the API of the
BFD library is too unstable to be used dynamically.

The static libraries are here because they are now needed by the
dynamic libraries.

Developers starting new projects are strongly encouraged to consider
using libelf instead of BFD.

# BZ 1924068.  Since applications that use the BFD library are
# required to link against the static version, ensure that it retains
# its debug informnation.
# FIXME: Yes - this is being done twice.  I have no idea why this
# second invocation is necessary but if both are not present the
# static archives will be stripped.
%undefine __brp_strip_static_archive

#----------------------------------------------------------------------------

%if %{with gold}

%package gold
Summary: The GOLD linker, a faster alternative to the BFD linker
# The GOLD linker is now deprecated as it is not being developed upstream.
# For more details see: https://fedoraproject.org/wiki/Changes/DeprecateGoldLinker
Provides: deprecated()
Requires: binutils >= %{version}

%description gold
This package provides the GOLD linker, which can be used as an alternative to
the default binutils linker (ld.bfd).  The GOLD is generally faster than the
BFD linker, and it supports features such as Identical Code Folding and
Incremental linking.  Unfortunately it is not as well maintained as the BFD
linker, and it may become deprecated in the future.

# The higher of these two numbers determines the default linker.
%{!?ld_gold_priority:%global ld_gold_priority   30}

%endif

%{!?ld_bfd_priority: %global ld_bfd_priority    50}

#----------------------------------------------------------------------------

%if %{with gprofng}

%package gprofng
Summary: Next Generating code profiling tool
Provides: gprofng = %{version}-%{release}
Requires: binutils = %{version}-%{release}

%description gprofng
GprofNG is the GNU Next Generation Profiler for analyzing the performance 
of Linux applications.

%endif

#----------------------------------------------------------------------------

%if %{with crossbuilds}

# Uncomment this when testing changes to the spec file, especially the cross building support.
# Remember to comment it out again once the testing is complete.
# %%undefine with_testsuite

# The list of cross targets to build.
%global system         redhat-linux
%global cross_targets  aarch64-%{system} ppc64le-%{system} s390x-%{system} x86_64-%{system}

%package -n cross-binutils-aarch64
Summary: Cross targeted AArch64 binutils for developer use.  Not intended for production.
Provides: cross-binutils-aarch64 = %{version}-%{release}
Requires: coreutils
%if %{with systemzlib}
Requires: zlib-devel
%endif
BuildRequires: autoconf automake perl sed coreutils make gcc findutils gcc-c++
ExcludeArch: aarch64-linux-gnu aarch64-redhat-linux

%description -n cross-binutils-aarch64
This package contains an AArch64 cross targeted version of the binutils for
use by developers.  It is NOT INTENDED FOR PRODUCTION use.


%package -n cross-binutils-ppc64le
Summary: Cross targeted PPC64LE binutils for developer use.  Not intended for production.
Provides: cross-binutils-ppc64le = %{version}-%{release}
Requires: coreutils
%if %{with systemzlib}
Requires: zlib-devel
%endif
BuildRequires: autoconf automake perl sed coreutils make gcc findutils gcc-c++
ExcludeArch: ppc64le-linux-gnu ppc64le-redhat-linux

%description -n cross-binutils-ppc64le
This package contains a PPC64LE cross targeted version of the binutils for
use by developers.  It is NOT INTENDED FOR PRODUCTION use.


%package -n cross-binutils-s390x
Summary: Cross targeted S390X binutils for developer use.  Not intended for production.
Provides: cross-binutils-s390x = %{version}-%{release}
Requires: coreutils
%if %{with systemzlib}
Requires: zlib-devel
%endif
BuildRequires: autoconf automake perl sed coreutils make gcc findutils gcc-c++
ExcludeArch: s390x-linux-gnu s390x-redhat-linux

%description -n cross-binutils-s390x
This package contains a S390X cross targeted version of the binutils for
use by developers.  It is NOT INTENDED FOR PRODUCTION use.


%package -n cross-binutils-x86_64
Summary: Cross targeted X86_64 binutils for developer use.  Not intended for production.
Provides: cross-binutils-x86_64 = %{version}-%{release}
Requires: coreutils
%if %{with systemzlib}
Requires: zlib-devel
%endif
BuildRequires: autoconf automake perl sed coreutils make gcc findutils gcc-c++
ExcludeArch: x86_64-linux-gnu x86_64-redhat-linux i686-linux-gnu i686-redhat-linux

%description -n cross-binutils-x86_64
This package contains a X86_64 cross targeted version of the binutils for
use by developers.  It is NOT INTENDED FOR PRODUCTION use.

%endif

#----------------------------------------------------------------------------

%prep

%if "%{gold_tarball}" != ""

%setup -q -n binutils-%{version} -a 0
%setup -q -n binutils-%{version} -D -b 2 

mv ../%{gold_tarball}/gold .
mv ../%{gold_tarball}/elfcpp .

%autopatch -p1 

%else

%if "%{source}" == "snapshot"
%autosetup -p1 -n binutils-with-gold-%{version}-%{commit_id}
%elif "%{source}" == "official-release"
%autosetup -p1 -n binutils-with-gold-%{version}
%else
%autosetup -p1 -n binutils-%{version} 
%endif

%endif

# On ppc64 and aarch64, we might use 64KiB pages
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*ppc.c
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*aarch64.c
sed -i -e '/common_pagesize/s/4 /64 /' gold/powerpc.cc
sed -i -e '/pagesize/s/0x1000,/0x10000,/' gold/aarch64.cc

# LTP sucks
perl -pi -e 's/i\[3-7\]86/i[34567]86/g' */conf*
sed -i -e 's/%''{release}/%{release}/g' bfd/Makefile{.am,.in}
sed -i -e '/^libopcodes_la_\(DEPENDENCIES\|LIBADD\)/s,$, ../bfd/libbfd.la,' opcodes/Makefile.{am,in}

# Build libbfd.so and libopcodes.so with -Bsymbolic-functions if possible.
if gcc %{optflags} -v --help 2>&1 | grep -q -- -Bsymbolic-functions; then
sed -i -e 's/^libbfd_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' bfd/Makefile.{am,in}
sed -i -e 's/^libopcodes_la_LDFLAGS = /&-Wl,-Bsymbolic-functions /' opcodes/Makefile.{am,in}
fi

# $PACKAGE is used for the gettext catalog name.
sed -i -e 's/^ PACKAGE=/ PACKAGE=%{?cross}/' */configure

# Undo the name change to run the testsuite.
for tool in binutils gas ld
do
  sed -i -e "2aDEJATOOL = $tool" $tool/Makefile.am
  sed -i -e "s/^DEJATOOL = .*/DEJATOOL = $tool/" $tool/Makefile.in
done

# Touch the .info files so that they are newer then the .texi files and
# hence do not need to be rebuilt.  This eliminates the need for makeinfo.
# The -print is there just to confirm that the command is working.
%if %{without docs}
  find . -name *.info -print -exec touch {} \;
%else
# If we are creating the docs, touch the texi files so that the info and
# man pages will be rebuilt.
  find . -name *.texi -print -exec touch {} \;
%endif

%ifarch %{power64}
%define _target_platform %{_arch}-%{_vendor}-%{_host_os}
%endif

#----------------------------------------------------------------------------

%build

# Building is now handled by functions which allow for both native and cross
# builds.  Builds are created in their own sub-directory of the sources, which
# allows for both native and cross builds to be created at the same time.

# compute_global_configuration()
#   Build the CARGS variable which contains the global configuration arguments.
compute_global_configuration()
{
    CARGS="--quiet \
 --build=%{_target_platform} \
 --host=%{_target_platform} \
 --enable-ld \
 --enable-plugins \
 --enable-64-bit-bfd \
 --enable-default-hash-style=gnu \
 --with-bugurl=%{dist_bug_report_url}"

%if %{without bootstrap}
    CARGS="$CARGS --enable-jansson=yes"
%endif

%if %{with debuginfod}
    CARGS="$CARGS --with-debuginfod"
%endif

%if %{with gprofng}
    CARGS="$CARGS --enable-gprofng=yes"
%else
    CARGS="$CARGS --enable-gprofng=no"
%endif

%if %{with systemzlib}
    CARGS="$CARGS --with-system-zlib=yes"
%endif

%if %{with xxhash}
    CARGS="$CARGS --with-xxhash=yes"
%endif

%if %{default_compress_debug}
    CARGS="$CARGS --enable-compressed-debug-sections=all"
%else
    CARGS="$CARGS --enable-compressed-debug-sections=none"
%endif

%if %{default_generate_notes}
    CARGS="$CARGS --enable-generate-build-notes=yes"
%else
    CARGS="$CARGS --enable-generate-build-notes=no"
%endif

%if %{default_relro}
    CARGS="$CARGS --enable-relro=yes"
%else
    CARGS="$CARGS --enable-relro=no"
%endif

%if %{enable_deterministic_archives}
    CARGS="$CARGS --enable-deterministic-archives"
%else
    CARGS="$CARGS --enable-deterministic-archives=no"
%endif

%if %{warn_for_executable_stacks}
    CARGS="$CARGS --enable-warn-execstack=yes"
    CARGS="$CARGS --enable-default-execstack=no"
%if %{error_for_executable_stacks}
    CARGS="$CARGS --enable-error-execstack=yes"
%endif
%else
    CARGS="$CARGS --enable-warn-execstack=no"
%endif

%if %{warn_for_rwx_segments}
    CARGS="$CARGS --enable-warn-rwx-segments=yes"
%if %{error_for_rwx_segments}
    CARGS="$CARGS --enable-error-rwx-segments=yes"
%endif
%else
    CARGS="$CARGS --enable-warn-rwx-segments=no"
%endif

%if %{enable_lto}
    CARGS="$CARGS --enable-lto"
%endif

%if %{enable_new_dtags}
    CARGS="$CARGS --enable-new-dtags --disable-rpath"
%endif

%if %{enable_separate_code}
  CARGS="$CARGS --enable-separate-code=yes"
  CARGS="$CARGS --enable-rosegment=yes"
%else
  CARGS="$CARGS --enable-separate-code=no"
  CARGS="$CARGS --enable-rosegment=no"
%endif

%if %{enable_threading}
    CARGS="$CARGS --enable-threads=yes"
%else
    CARGS="$CARGS --enable-threads=no"
%endif

%if "%{source}" != "official-release"
# Since non official release tarballs are created directly from development
# sources they will have "development=true" set in the bfd/development.sh file.
# This enables -Werror by default, which is a problem because there is a
# known issue with the libiberty library:
#   libiberty/cp-demangle.c: In function 'd_demangle_callback.constprop':
#   libiberty/cp-demangle.c:6794:1: error: stack usage might be unbounded [-Werror=stack-usage=]
# So we explicitly disable werror for builds from these tarballs.
    CARGS="$CARGS --enable-werror=no"
%endif
}

# run_target_configuration()
#    Create and configure the build tree.
#        $1 is the target architecture
#        $2 is 1 if this is a native build
#        $3 is 1 if shared libraries should be built
#
run_target_configuration()
{
    local target="$1"
    local native="$2"
    local shared="$3"
    local builddir=build-$target

    # Create a build directory
    rm -rf $builddir
    mkdir $builddir
    pushd $builddir

    echo "BUILDING the Binutils for TARGET $target (native ? $native) (shared ? $shared)"

    %set_build_flags

    export CFLAGS="$RPM_OPT_FLAGS"

%ifarch %{power64}
    export CFLAGS="$CFLAGS -Wno-error"
%endif

%if %{with debug}
    %undefine _fortify_level
    export CFLAGS="$CFLAGS -O0 -ggdb2 -Wno-error"
%endif

    export CXXFLAGS="$CXXFLAGS $CFLAGS"

    # Some GNU extensions to the C11 standard are used.
    # Note set here as -std=gnu11 is not a valid G++ command line option.
    export CFLAGS="$CFLAGS -std=gnu11"

    # BZ 1541027 - include the linker flags from redhat-rpm-config as well.
    export LDFLAGS=$RPM_LD_FLAGS

%if %{enable_new_dtags}
    # Build the tools with new dtags, as well as supporting their generation by the linker.
    export LDFLAGS="$LDFLAGS -Wl,--enable-new-dtags"
%endif

    if test x$native == x1 ; then
        # Extra targets to build along with the native one.
        #
        # BZ 1920373: Enable PEP support for all targets as the PERF package's
        # testsuite expects to be able to read PE format files regardless of
        # the host's architecture.
        #
        # Also enable the BPF target so that strip will work on BPF files.
        case $target in
        s390*)
            # Note - The s390-linux target is there so that the GOLD linker will
            # build.  By default, if configured for just s390x-linux, the GOLD
            # configure system will only include support for 64-bit targets, but
            # the s390x gold backend uses both 32-bit and 64-bit templates.
            TARGS="--enable-targets=s390-linux,s390x-linux,x86_64-pep,bpf-unknown-none"
            ;;
        ia64*)
            TARGS="--enable-targets=ia64-linux,x86_64-pep,bpf-unknown-none"
            ;;
        ppc64-*)
            TARGS="--enable-targets=powerpc64le-linux,spu,x86_64-pep,bpf-unknown-none"
            ;;
        ppc64le*)
            TARGS="--enable-targets=powerpc-linux,spu,x86_64-pep,bpf-unknown-none"
            ;;
        *)
            TARGS="--enable-targets=x86_64-pep,bpf-unknown-none"
            ;;
        esac

        # Set up the sysroot and paths.
        SARGS="--with-sysroot=/ \
               --prefix=%{_prefix} \
               --libdir=%{_libdir} \
               --sysconfdir=%{_sysconfdir}"
%if %{with gold}
        SARGS="$SARGS --enable-gold=default"
%else
        SARGS="$SARGS --disable-gold"
%endif

    else # Cross builds

        # No extra targets are supported.
        TARGS=""

        # Disable the GOLD linker for cross builds because although it does
        # support sysroots specified on the command line, it does not support
        # them in linker scripts via the =/$SYSROOT prefix.
        SARGS="--with-sysroot=yes \
               --program-prefix=$target- \
               --prefix=%{_prefix}/$target \
               --libdir=%{_libdir} \
               --exec-prefix=%{_usr} \
               --sysconfdir=%{_sysconfdir} \
               --disable-gold"
    fi

    if test x$shared == x1 ; then
        RARGS="--enable-shared"
    else
        RARGS="--disable-shared"
    fi
    
    ../configure --target=$target $CARGS $SARGS $RARGS $TARGS  || cat config.log

    popd
}

# build_target ()
#   Builds a configured set of sources.
#        $1 is the target architecture
build_target()
{
    local target="$1"
    local builddir=build-$target

    pushd $builddir

    mkdir -p gas/doc
    
%if %{with docs}
    # Because of parallel building, info has to be made after all.
    # %%make_build %%{_smp_mflags} tooldir=%%{_prefix} all 
    # %%make_build %%{_smp_mflags} tooldir=%%{_prefix} info
    %make_build -j1 tooldir=%{_prefix} all 
    %make_build -j1 tooldir=%{_prefix} info
%else
    %make_build %{_smp_mflags} tooldir=%{_prefix} MAKEINFO=true all
%endif
    
    popd
}

# run_tests()
#       Test a built (but not installed) binutils.
#        $1 is the target architecture
#        $2 is 1 if this is a native build
#
run_tests()
{
    local target="$1"
    local native="$2"

    echo "TESTING the binutils FOR TARGET $target (native ? $native)"

    # Do not use %%check as it is run after %%install where libbfd.so is rebuilt
    # with -fvisibility=hidden no longer being usable in its shared form.
%if %{without testsuite}
    echo ================ $target == TESTSUITE DISABLED ====================
    return
%endif

    pushd build-$target

    # FIXME:  I have not been able to find a way to capture a "failed" return
    # value from "make check" without having it also stop the build.  So in
    # order to obtain the logs from the test runs if a check fails I have to
    # run the tests twice.  Once to generate the logs and then a second time
    # to generate the correct exit code.
    
    echo ================ $target == TEST RUN 1 =============================

    # Run the tests and accumulate the logs - but ignore failures...
    
    if test x$native == x1 ; then
        make -k check-gas check-binutils check-ld < /dev/null || :
%if %{with gold}
        # The GOLD testsuite always returns an error code, even if no tests fail.
        make -k check-gold < /dev/null || :
%endif
    else
        # Do not try running linking tests for the cross-binutils.
        make -k check-gas check-binutils < /dev/null || :
    fi
    
    for f in {gas/testsuite/gas,ld/ld,binutils/binutils}.sum
    do
        if [ -f $f ]; then
            cat $f
        fi
    done

%if %{with gold}
    if [ -f gold/test-suite.log ]; then
        cat gold/test-suite.log
    fi
    if [ -f gold/testsuite/test-suite.log ]; then
        cat gold/testsuite/*.log
    fi
%endif

    for file in {gas/testsuite/gas,ld/ld,binutils/binutils}.{sum,log}
    do
        if [ -f $file ]; then
            ln $file binutils-$target-$(basename $file) || :
        fi
    done

    tar cjf binutils-$target.tar.xz  binutils-$target-*.log
    uuencode binutils-$target.tar.xz binutils-$target.tar.xz
    rm -f binutils-$target.tar.xz    binutils-$target-*.log

%if %{with gold}
    if [ -f gold/testsuite/test-suite.log ]; then
        tar cjf  binutils-$target-gold.log.tar.xz gold/testsuite/*.log
        uuencode binutils-$target-gold.log.tar.xz binutils-$target-gold.log.tar.xz
        rm -f    binutils-$target-gold.log.tar.xz
    fi
%endif

    echo ================ $target == TEST RUN 2 =============================

    # Run the tests and this time fail if there are any errors.

    if test x$native == x1 ; then
        make -k check-gas check-binutils check-ld < /dev/null
        # Ignore the gold tests - they always fail
    else
        # Do not try running linking tests for the cross-binutils.
        make -k check-gas check-binutils < /dev/null
    fi

    popd
}

#----------------------------------------------------------------------------

# There is a problem with the clang+libtool+lto combination.
# The LDFLAGS containing -flto are not being passed when linking the
# libbfd.so, so the build fails.  Solution: disable LTO.
%if %{with clang}
%define enable_lto 0
%endif

%if %{with clang}
%define _with_cc_clang 1
%endif

# Disable LTO on arm due to:
# https://bugzilla.redhat.com/show_bug.cgi?id=1918924
%ifarch %{arm}
%define enable_lto 0
%endif

%if !0%{?enable_lto}
%global _lto_cflags %{nil}
%endif

compute_global_configuration

# Build the native configuration.
run_target_configuration  %{_target_platform} 1 %{enable_shared}
build_target              %{_target_platform}
run_tests                 %{_target_platform} 1 

%if %{with crossbuilds}

# Build the cross configurations.
for f in %{cross_targets}; do

    # Skip the native build.
    if test x$f != x%{_target_platform}; then
        # We could improve the cross build's size by enabling shared libraries but
        # the produced binaries may be less convenient in the embedded environment.
        run_target_configuration  $f 0 0
        build_target              $f 
        run_tests                 $f 0
    fi
done

%endif

#----------------------------------------------------------------------------

%install

# install_binutils()
#       Install the binutils.
#        $1 is the target architecture
#        $2 is 1 if this is a native build
#        $3 is 1 if shared libraries should be built
#
install_binutils()
{
    local target="$1"
    local native="$2"
    local shared="$3"

    local local_root=%{buildroot}/%{_prefix}
    local local_bindir=$local_root/bin
    local local_libdir=%{buildroot}%{_libdir}
    local local_mandir=$local_root/share/man/man1
    local local_incdir=$local_root/include
    local local_infodir=$local_root/share/info
    local local_libdir
    
    mkdir -p $local_libdir
    mkdir -p $local_incdir
    mkdir -p $local_mandir
    mkdir -p $local_infodir

    echo "INSTALLING the binutils FOR TARGET $target (native ? $native) (shared ? $shared)"

    pushd build-$target
    
    if test x$native == x1 ; then

%if %{with docs}
        %make_install DESTDIR=%{buildroot} 
        make prefix=%{buildroot}%{_prefix} infodir=$local_infodir install-info
%else
        %make_install DESTDIR=%{buildroot} MAKEINFO=true
%endif

        # Rebuild the static libraries with -fPIC.
        # It would be nice to build the static libraries with -fno-lto so that
        # they can be used by programs that are built with a different version
        # of GCC from the one used to build the libraries, but this will trigger
        # warnings from annocheck.

        # Future: Remove libiberty together with its header file, projects should bundle it.
        %make_build -s -C libiberty clean
        %set_build_flags
        %make_build -s CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C libiberty

        # Without the hidden visibility the 3rd party shared libraries would export
        # the bfd non-stable ABI.
        %make_build -s -C bfd clean
        %set_build_flags
        %make_build -s CFLAGS="-g -fPIC $RPM_OPT_FLAGS -fvisibility=hidden" -C bfd

        %make_build -s -C opcodes clean
        %set_build_flags
        %make_build -s CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C opcodes

        %make_build -s -C libsframe clean
        %set_build_flags
        %make_build -s CFLAGS="-g -fPIC $RPM_OPT_FLAGS" -C libsframe

        install -m 644 bfd/.libs/libbfd.a           $local_libdir
        install -m 644 libiberty/libiberty.a        $local_libdir
        install -m 644 ../include/libiberty.h       $local_incdir
        install -m 644 opcodes/.libs/libopcodes.a   $local_libdir
        install -m 644 libsframe/.libs/libsframe.a  $local_libdir

        # Remove Windows/Novell only man pages
        rm -f $local_mandir/{dlltool,nlmconv,windres,windmc}*
%if %{without docs}
	rm -f $local_mandir/{addr2line,ar,as,c++filt,elfedit,gp,ld,nm,objcopy,objdump,ranlib,readelf,size,strings,strip}*
	rm -f $local_infodir/{as,bfd,binutils,ctf,gprof,ld,sframe}*
%if %{with gprofng}
	rm -fr $local_infodir/../doc/gprofng
%endif
%endif

%if %{enable_shared}
        chmod +x $local_libdir/lib*.so*
%endif

        # Prevent programs from linking against libbfd and libopcodes
        # dynamically, as they are changed far too often.
        rm -f $local_libdir/lib{bfd,opcodes}.so

        # Remove libtool files, which reference the .so libs
        rm -f %local_libdir/lib{bfd,opcodes}.la

        # Sanity check --enable-64-bit-bfd really works.
        grep '^#define BFD_ARCH_SIZE 64$' $local_incdir/bfd.h
        # Fix multilib conflicts of generated values by __WORDSIZE-based expressions.
%ifarch %{ix86} x86_64 ppc %{power64} s390 s390x sh3 sh4 sparc sparc64 arm
        sed -i -e '/^#include "ansidecl.h"/{p;s~^.*$~#include <bits/wordsize.h>~;}' \
            -e 's/^#define BFD_DEFAULT_TARGET_SIZE \(32\|64\) *$/#define BFD_DEFAULT_TARGET_SIZE __WORDSIZE/' \
            -e 's/^#define BFD_HOST_64BIT_LONG [01] *$/#define BFD_HOST_64BIT_LONG (__WORDSIZE == 64)/' \
            -e 's/^#define BFD_HOST_64_BIT \(long \)\?long *$/#if __WORDSIZE == 32\
#define BFD_HOST_64_BIT long long\
#else\
#define BFD_HOST_64_BIT long\
#endif/' \
            -e 's/^#define BFD_HOST_U_64_BIT unsigned \(long \)\?long *$/#define BFD_HOST_U_64_BIT unsigned BFD_HOST_64_BIT/' \
            $local_incdir/bfd.h
%endif

        touch -r ../bfd/bfd-in2.h $local_incdir/bfd.h

        # Generate .so linker scripts for dependencies; imported from glibc/Makerules:

        # This fragment of linker script gives the OUTPUT_FORMAT statement
        # for the configuration we are building.
        OUTPUT_FORMAT="\
/* Ensure this .so library will not be used by a link for a different format
   on a multi-architecture system.  */
$(gcc $CFLAGS $LDFLAGS -shared -x c /dev/null -o /dev/null -Wl,--verbose -v 2>&1 | sed -n -f "%{SOURCE1}")"

        tee $local_libdir/libbfd.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

/* The libz & libsframe dependencies are unexpected by legacy build scripts.  */
/* The libdl dependency is for plugin support.  (BZ 889134)  */
INPUT ( %{_libdir}/libbfd.a %{_libdir}/libsframe.a -liberty -lz -ldl )
EOH

        tee $local_libdir/libopcodes.so <<EOH
/* GNU ld script */

$OUTPUT_FORMAT

INPUT ( %{_libdir}/libopcodes.a -lbfd )
EOH

        rm -fr $local_root/$target

    else # CROSS BUILDS

        local target_root=$local_root/$target
        
        %make_install DESTDIR=%{buildroot} MAKEINFO=true
    fi

    # This one comes from gcc
    rm -f $local_infodir/dir

    %find_lang binutils
    %find_lang opcodes
    %find_lang bfd
    %find_lang gas
    %find_lang gprof
    cat opcodes.lang >> binutils.lang
    cat bfd.lang     >> binutils.lang
    cat gas.lang     >> binutils.lang
    cat gprof.lang   >> binutils.lang

    if [ -x ld/ld-new ]; then
        %find_lang ld
        cat ld.lang >> binutils.lang
    fi

    if [ -x gold/ld-new ]; then
        %find_lang gold
        cat gold.lang >> binutils.lang
    fi

    popd
}

#----------------------------------------------------------------------------

install_binutils %{_target_platform} 1 %{enable_shared}

%if %{with crossbuilds}

for f in %{cross_targets}; do
    if test x$f != x%{_target_platform}; then
        install_binutils $f 0 0
    fi
done

%endif

# Stop check-rpaths from complaining about standard runpaths.
export QA_RPATHS=0x0003

#----------------------------------------------------------------------------

%if %{with gold}
%post gold

%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/ld.gold %{ld_gold_priority}
exit 0
%endif

%post

# Remove the /usr/bin/ld file so that the alternatives program
# can replace it with a symbolic link.
%__rm -f %{_bindir}/ld

%{_sbindir}/alternatives --install %{_bindir}/ld ld \
  %{_bindir}/ld.bfd %{ld_bfd_priority}

# Do not run "alternatives --auto ld" here.  Leave the setting to
# however the user previously had it set.  See BZ 1592069 for more details.

%ldconfig_post

exit 0

#----------------------------------------------------------------------------

# Note: $1 == 0 means that there is an uninstall in progress.
# $1 == 1 means that there is an upgrade in progress.

%if %{with gold}
%preun gold

if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove ld %{_bindir}/ld.gold
fi
exit 0
%endif

%preun
if [ $1 = 0 ]; then
  %{_sbindir}/alternatives --remove ld %{_bindir}/ld.bfd
fi

# Restore the /usr/bin/ld file so that the automatic file
# removal part of the uninstall process will work.
touch %{_bindir}/ld

exit 0

#----------------------------------------------------------------------------

%postun
%ldconfig_postun

#----------------------------------------------------------------------------

%files -f build-%{_target_platform}/binutils.lang

%if %{with crossbuilds}
%if "%{_target_platform}" != "aarch64-%{system}"
%exclude /usr/aarch64-%{system}/*
%exclude /usr/bin/aarch64-%{system}-*
%endif

%if "%{_target_platform}" != "ppc64le-%{system}"
%exclude /usr/ppc64le-%{system}/*
%exclude /usr/bin/ppc64le-%{system}-*
%endif

%if "%{_target_platform}" != "s390x-%{system}"
%exclude /usr/s390x-%{system}/*
%exclude /usr/bin/s390x-%{system}-*
%endif

%if "%{_target_platform}" != "x86_64-%{system}"
%exclude /usr/x86_64-%{system}/*
%exclude /usr/bin/x86_64-%{system}-*
%endif
%endif

%license COPYING COPYING3 COPYING3.LIB COPYING.LIB
%doc README
%{_bindir}/[!l]*
# %%verify(symlink) does not work for some reason, so using "owner" instead.
%verify(owner) %{_bindir}/ld
# %%verify(mtime) does not work, probably because of the alternatives command in the %%post stage, so using "owner" instead.  (#2277349)
%verify(owner) %{_bindir}/ld.bfd

%if %{with gprofng}
%exclude %{_bindir}/gp-*
%exclude %{_bindir}/gprofng
%exclude %{_bindir}/gprofng-*
%endif

%exclude %dir %{_exec_prefix}/lib/debug

%if %{with docs}
%{_mandir}/man1/
%{_infodir}/as.info.*
%{_infodir}/binutils.info.*
%{_infodir}/ld.info.*
%{_infodir}/ldint.info.*
%{_infodir}/bfd.info.*
%{_infodir}/ctf-spec.info.*
%{_infodir}/gprof.info.*
%{_infodir}/sframe-spec.info.*

%if %{with gprofng}
%exclude %{_docdir}/gprofng/examples.tar.gz
%exclude %{_infodir}/gprofng*
%exclude %{_mandir}/man1/gprofng*
%endif

%endif

%if %{enable_shared}
%{_libdir}/lib*.so
%{_libdir}/lib*.so.*
%dir %{_libdir}/bfd-plugins
%{_libdir}/bfd-plugins/libdep.so

%exclude %{_libdir}/libbfd.so
%exclude %{_libdir}/libopcodes.so
%exclude %{_libdir}/libctf.a
%exclude %{_libdir}/libctf-nobfd.a

%if %{with gprofng}
%exclude %{_libdir}/libgprofng.*
%endif

%endif

#------------------------------------

%files devel
%{_prefix}/include/*
%{_libdir}/lib*.a
%{_libdir}/libbfd.so
%{_libdir}/libopcodes.so

%if %{enable_shared}
%exclude %{_libdir}/lib*.la
%endif

%if %{with debug}
%dir %{_libdir}/bfd-plugins
%{_libdir}/bfd-plugins/libdep.a
%endif

#------------------------------------

%if %{with gold}
%files gold
%{_bindir}/%{?cross}ld.gold
%endif

#------------------------------------

%if %{with gprofng}
%files gprofng
%{_bindir}/gp-*
%{_bindir}/gprofng
%{_bindir}/gprofng-*
%dir %{_libdir}/gprofng
%{_libdir}/gprofng/*
%{_sysconfdir}/gprofng.rc

%if %{enable_shared}
%{_libdir}/libgprofng.*
%endif

%if %{with docs}
%dir %{_docdir}/gprofng
%{_docdir}/gprofng/examples.tar.gz
%{_infodir}/gprofng*
%{_mandir}/man1/gprofng*
%endif

%endif

#------------------------------------

%if %{with crossbuilds}

%if "%{_target_platform}" != "aarch64-%{system}"
%files -n cross-binutils-aarch64 
/usr/aarch64-%{system}/
/usr/bin/aarch64-%{system}-*
%endif

%if "%{_target_platform}" != "ppc64le-%{system}"
%files -n cross-binutils-ppc64le
/usr/ppc64le-%{system}/
/usr/bin/ppc64le-%{system}-*
%endif

%if "%{_target_platform}" != "s390x-%{system}"
%files -n cross-binutils-s390x
/usr/s390x-%{system}/
/usr/bin/s390x-%{system}-*
%endif

%if "%{_target_platform}" != "x86_64-%{system}"
%files -n cross-binutils-x86_64
/usr/x86_64-%{system}/
/usr/bin/x86_64-%{system}-*
%endif

%endif

#----------------------------------------------------------------------------
%changelog
* Thu Jan 15 2026 Nick Clifton <nickc@redhat.com> - 2.45.1-4
- Remove experimental Risc-V patch added with -2 revision.

* Fri Jan 09 2026 Nick Clifton <nickc@redhat.com> - 2.45.1-3
- Fix Risc-V related test failures caused by previous patch. 

* Mon Jan 05 2026 Nick Clifton <nickc@redhat.com> - 2.45.1-2
- Change Risc-V assembler to default to disabling relaxation.

* Wed Nov 12 2025 Nick Clifton <nickc@redhat.com> - 2.45.1-1
- Rebase to the 2.45.1 release.

* Fri Oct 03 2025 Nick Clifton <nickc@redhat.com> - 2.45-4
- Stop a potential illegal memory access when linking a corrupt input file.  (CVE-2025-11082)

* Thu Oct 02 2025 Nick Clifton <nickc@redhat.com> - 2.45-3
- Stop a potential illegal memory access when linking a corrupt input file.  (CVE-2025-11083)

* Fri Sep 12 2025 Nick Clifton <nickc@redhat.com> - 2.45-2
- Enhance the riscv-64 zicfilp-unlabeled-plt test to cope with larger offsets.

* Mon Jul 28 2025 Nick Clifton <nickc@redhat.com> - 2.45-1
- Rebase to official GNU Binutils 2.45 release.

* Fri Jul 25 2025 Nick Clifton <nickc@redhat.com> - 2.44.90-4
- Properly handle LLVM IR bitcodes.  (#2382341) (PR 33198)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.44.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Nick Clifton <nickc@redhat.com> - 2.44.90-2
- Improve strip's handling of archives containing bitcodes.  (#2382341)

* Mon Jul 14 2025 Nick Clifton <nickc@redhat.com> - 2.44.90-1
- Rebase to 2.45 pre-release snapshot.

* Mon Jul 07 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-13
- Rebase to commit 21e608528c3

* Mon Jun 23 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-12
- Rebase to commit 28b75d9dcb8

* Mon Jun 09 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-11
- Rebase to commit a259da93f3c

* Tue May 27 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-10
- Rebase to commit d13aaae402f

* Mon May 12 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-9
- Rebase to commit 8dc4e62fc94

* Mon Apr 14 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-8
- Rebase to commit 6ef74a3985b

* Thu Apr 10 2025 Andrea Bolognani <abologna@redhat.com> - 2.44.50-7
- Fix BuildRequires on bison

* Wed Apr 02 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-6
- Deprecate the GOLD linker.

* Mon Mar 31 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-5
- Rebase to commit 7109ea04ac7

* Mon Mar 17 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-4
- Rebase to commit a07c8b3a73c

* Mon Mar 03 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-3
- Rebase to commit 56a0188548e

* Wed Feb 26 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-2
- Renumber patches.
- Add -std=gnu11 to CFLAGS to support the use of static_assert in the sources.

* Tue Feb 18 2025 Nick Clifton <nickc@redhat.com> - 2.44.50-1
- Rebase to commit 1256b9860f3

* Fri Feb 07 2025 Nick Clifton <nickc@redhat.com> - 2.44-3
- Fix seg fault in AArch64 linker when building u-boot.  (#2326190)

* Thu Feb 06 2025 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.44-2
- Default gcs-report-dynamic to NONE for Fedora.

* Mon Feb 03 2025 Nick Clifton <nickc@redhat.com> - 2.44-1
- Rebase to official GNU Binutils 2.44 release

* Mon Jan 27 2025 Nick Clifton <nickc@redhat.com> - 2.43.90-2
- Enable separate-code by default for the RISC-V target.

* Mon Jan 20 2025 Nick Clifton <nickc@redhat.com> - 2.43.90-1
- Rebased to 2.43.90 pre-release tarball.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.50-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 06 2025 Nick Clifton <nickc@redhat.com> - 2.43.50-11
- Rebase to commit f832531609d

* Mon Dec 09 2024 Nick Clifton <nickc@redhat.com> - 2.43.50-10
- Rebase to commit 3d75969bd0e

* Tue Nov 26 2024 Nick Clifton <nickc@redhat.com> - 2.43.50-9
- Rebase to commit 1686dc7079f

* Fri Nov 15 2024 Nick Clifton <nickc@redhat.com> - 2.43.50-8
- Spec File: Move all gprofng files into the binutils-gprofng sub-package.  (2326286)

* Mon Nov 04 2024 Nick Clifton <nickc@redhat.com> - 2.43.50-7
- Rebase to commit 55e32b3c682
- Revert commit 4f576180 which moves the .note.build-id section back to the start of the file.  (PR 2321588)

* Thu Oct 31 2024 Miro Hrončok <mhroncok@redhat.com> - 2.43.50-6
- Spec File: Do not install gprofng documentation when using --without docs

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 2.43.50-5
- Rebuild for Jansson 2.14
  (https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Mon Oct 14 2024 Nick Clifton <nickc@redhat.com> - 2.43.50-4
- Rebase to commit 22c62092858.

* Thu Oct 03 2024 Nick Clifton <nickc@redhat.com> - 2.43.50-3
- Add more fixes for linker testsuite failures for the RISC-V.

* Mon Sep 30 2024 Nick Clifton <nickc@redhat.com> - 2.43.50-2
- Rebase to commit 1f4aee70ed1.
- Configure the linker to support xxhash by default.

* Tue Sep 10 2024 Nick Clifton <nickc@redhat.com> - 2.43.50-1
- Rebase to commit c839a44c391.

* Mon Sep 09 2024 Nick Clifton <nickc@redhat.com> - 2.43.1-2
- Disable the default enablement of the linker's "-z separate-code" feature for non-x86 architectures.

* Sat Aug 17 2024 Nick Clifton <nickc@redhat.com> - 2.43.1-1
- Rebase to 2.43.1 release.  (#2305399)
- Retire: binutils-LTO-restore-wrapper-symbol.patch

* Mon Aug 05 2024 Nick Clifton <nickc@redhat.com> - 2.43-2
- Use correct fix for BZ 2301454.

* Mon Aug 05 2024 Nick Clifton <nickc@redhat.com> - 2.43-1
- Rebase to 2.43 release.

* Wed Jul 31 2024 Nick Clifton <nickc@redhat.com> - 2.42.90-2
- Revert commit eb7892c4019bd5d00175c0eb80eb0c5a47a42ca1 which was supposed to fix PR 31956 but also introduced new build failures.  (2301454).

* Mon Jul 22 2024 Nick Clifton <nickc@redhat.com> - 2.42.90-1
- Rebase to pre-release sources.
- Retire: binutils-update-linker-manual.patch

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.50-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-19
- Rebase to commit 49cc32b732a
- Retire: binutils-special-sections-in-groups.patch 

* Mon Jun 24 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-18
- Rebase to commit 18b13d11d37

* Mon Jun 24 2024 Nick Clifton  <nickc@redhat.com> - 2.42.50-17
- Fix building with documentation disabled.

* Fri Jun 14 2024 Nick Clifton <nickc@redhat.com>- 2.42.50-16
- Rebase to commit 6b19a26ee12.  (Which brings in --rosegment support).

* Mon Jun 10 2024 Nick Clifton <nickc@redhat.com>- 2.42.50-15
- Rebase to commit d1c2dd6f4de

* Fri May 31 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-14
- Rebase to commit cc80485f45c.  (Which brings in RELR support for the AArch64).

* Tue May 28 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-13
- Rebase to commit 73061b1e53a

* Tue May 14 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-12
- Remove "Requires: binutils-gold" from binutils sub-package.

* Mon May 13 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-11
- Rebase to commit 83b972fc272db31ab48aa5cde84f47c98868d7c8

* Mon Apr 29 2024 Nick Clifton  <nickc@redhat.com> - 2.42.50-10
- Spec File: Stop %%verify(mtime) for ld.bfd.  (#2277349)

* Mon Apr 29 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-9
- Rebase to commit 679ad6e126868c462d8339eb837efb5a91a091af

* Mon Apr 15 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-8
- Rebase to commit a73073dc7f23ab37ae33402fbb38c8314bcbea3e

* Tue Apr 02 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-7
- Rebase to commit 121a3f4b4f4aac216abe239f6f3bd491b63e5e34

* Mon Mar 18 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-6
- Rebase to commit 6549a232d25585800752007f699fb7db9fe70883

* Mon Mar 04 2024 Nick Clifton <nickc@redhat.com> - 2.42.50-5
- Rebase to commit 1485a3fb63619cced99dd7a4a043cf01a0f423d9

* Thu Feb 22 2024 Nick Clifton  <nickc@redhat.com> - 2.42.50-4
- Spec File: Change the NVR to reflect the fact that these binutils are based upon development sources, rather than release sources.

* Wed Feb 21 2024 Nick Clifton  <nickc@redhat.com> - 2.42-4
- Spec File: Add support for using source tarballs created after a specific commit.
- Rebase to commit 1b2c120daf9e2d935453f9051bbeafbac7f9f14d
- Retire: binutils-power-11.patch
- Retire: binutils-fatal-warnings.patch
- Retire: binutils-scfi-tests-fix.patch
- Retire: binutils-Intel-APX-part-1-fixes.patch 

* Wed Feb 14 2024 Nick Clifton  <nickc@redhat.com> - 2.42-2
- Add support for PowerPC v11 architecture extensions.

* Wed Feb 14 2024 Nick Clifton  <nickc@redhat.com> - 2.42-1
- Rebase to GNU Binutils 2.42.
- Retire: binutils-BPF-reloc-4.patch
- Retire: binutils-Intel-APX-part-1.patch
- Retire: binutils-aarch64-big-bti-programs.patch
- Retire: binutils-big-merge.patch
- Retire: binutils-demangler-updates.patch
- Retire: binutils-execstack-error.patch
- Retire: binutils-gold-powerpc.patch
- Retire: binutils-handle-corrupt-version-info.patch
- Retire: binutils-ppc-dt_relr-relocs.patch
- Retire: binutils-riscv-SUB_ULEB128.patch
- Retire: binutils-x86-64-v3.patch
- Retire: i686-AVX10.1-part-1.patch
- Retire: i686-AVX10.1-part-2.patch
- Retire: i686-AVX10.1-part-3.patch
- Retire: i686-AVX10.1-part-4.patch
- Retire: i686-AVX10.1-part-5.patch
- Retire: i686-AVX10.1-part-6.patch

* Mon Feb 12 2024 Nick Clifton  <nickc@redhat.com> - 2.41-34
- Backport commits 5a635f1f59ad and 41e115853eef to fix some APX issues.
- Add top-level multilib.am file.

* Mon Feb 12 2024 Nick Clifton  <nickc@redhat.com> - 2.41-33
- Backport commit 4199cf1e152d in order to add support for IBM's power-11 architecture extensions.

* Wed Jan 24 2024 Nick Clifton  <nickc@redhat.com> - 2.41-32
- Suppress the x86 linker's p_align-1 tests in order to cope with a CentOS-10 kernel bug.  (RHEL-22466)

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.41-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Nick Clifton  <nickc@redhat.com> - 2.41-30
- Import commits 4a54cb06585f568031dfd291d0fe45979ad75e98 and 00a17c6ad068c95019e1f37cfc2d1b8aaebd6ecb to add APX support to GOLD.

* Sat Jan 20 2024 Jakub Jelinek  <jakub@redhat.com> - 2.41-29
- Import commit eed38d8a02b2 to update APX support.  (#2259333)

* Fri Jan 19 2024 Nick Clifton  <nickc@redhat.com> - 2.41-28
- Import commits 5190fa38286a , 2519809009ed and eea4357967b6 to update APX support.

* Wed Jan 17 2024 Nick Clifton  <nickc@redhat.com> - 2.41-27
- Add support for Intel's APX (part 1) architecture extensions.

* Wed Jan 17 2024 Nick Clifton  <nickc@redhat.com> - 2.41-26
- Import libiberty demangling improvements in order to support gcc v14 mangling.

* Mon Jan 15 2024 Nick Clifton  <nickc@redhat.com> - 2.41-25
- Fix creation of DT_RELR relocs for PPC64LE.  (#2258061)

* Thu Jan 11 2024 Siddhesh Poyarekar  <siddhesh@redhat.com> - 2.41-24
- Use _fortify_level macro to control _FORTIFY_SOURCE.

* Thu Jan 11 2024 Amit Shah  <amitshah@fedoraproject.org>- 2.41-23
- Spec File: gprofng requires bison at build time

* Thu Jan 11 2024 Tulio Machado  <tuliom@redhat.com> - 2.41-22
- Remove dependency upon zlib-static.

* Thu Jan 04 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.41-21
- Fix location of gprofng.rc

* Thu Jan 04 2024 Nick Clifton  <nickc@redhat.com> - 2.41-20
- Fix SPDX annotation.

* Thu Jan 04 2024 Nick Clifton  <nickc@redhat.com> - 2.41-19
- Have the gold linker ignore the --error-execstack and --error-rwx-segments options.

* Tue Jan 02 2024 Nick Clifton  <nickc@redhat.com> - 2.41-18
- Fix handling of Risc-V SUB_LEB128 relocation.  (PR31179)

* Mon Dec 11 2023 Nick Clifton  <nickc@redhat.com> - 2.41-17
- Fix failure in binutils testsuite for RiscV architecture.

* Thu Dec 07 2023 Nick Clifton  <nickc@redhat.com> - 2.41-16
- Add support for Intel's AVX10.1 ISA.

* Tue Nov 28 2023 Nick Clifton  <nickc@redhat.com> - 2.41-15
- Disable errors for executable stacks (enabled too early by previous delta).

* Tue Nov 21 2023 Nick Clifton  <nickc@redhat.com> - 2.41-14
- Enable errors for executable stacks.

* Fri Nov 10 2023 Nick Clifton  <nickc@redhat.com> - 2.41-13
- Make the GOLD linker ignore the "-z pack-relative-relocs" option.  (#2248936)

* Tue Nov 07 2023 Nick Clifton  <nickc@redhat.com> - 2.41-12
- Fix the bfd linker's generation of call stubs for large AArch64 binaries with BTI enabled.  (#2241902)

* Tue Nov 07 2023 Nick Clifton  <nickc@redhat.com> - 2.41-11
- Fix merging strings when linking really big programs.

* Wed Nov 01 2023 Nick Clifton  <nickc@redhat.com> - 2.41-10
- Allow for x86_64 build environments that use a base ISA of x86-64-v3.  (#2247296)

* Mon Oct 30 2023 Nick Clifton  <nickc@redhat.com> - 2.41-9
- Accept and ignore R_BPF_64_NODYLD32 relocations.  (#2245296)

* Thu Oct 19 2023 Nick Clifton  <nickc@redhat.com> - 2.41-8
- Add ability to turn execstack warnings into errors.
- Enable warnings for rsx segments.

* Fri Oct 13 2023 Nick Clifton  <nickc@redhat.com> - 2.41-7
- Fix a potential NULL pointer derefence when parsing corrupt ELF symbol version information.  (#2243769)

* Thu Oct 12 2023 Nick Clifton  <nickc@redhat.com> - 2.41-6
- Enable warnings about executable stacks by default.

* Fri Aug 25 2023 Nick Clifton  <nickc@redhat.com> - 2.41-5
- Fix the GOLD linker's handling of 32-bit PowerPC binaries.  (#2234396)

* Wed Aug 23 2023 Nick Clifton  <nickc@redhat.com> - 2.41-4
- Add fixes for linker testsuite failures for the RISCV-64 target.

* Thu Aug 17 2023 Adam Williamson <awilliam@redhat.com> - 2.41-3
- More CI fixes.

* Thu Aug 17 2023 Adam Williamson <awilliam@redhat.com> - 2.41-2
- Tests: use uname -m instead of uname -i.

* Thu Aug 03 2023 Nick Clifton  <nickc@redhat.com> - 2.41-1
- Rebase to GNU Binutils 2.41
- Retire: binutils-filename-in-readelf-messages.patch
- Retire: binutils-readelf-other-sym-info.patch
- Retire: binutils-fix-testsuite-failures.patch
- Retire: binutils-objcopy-note-merge-speedup.patch
- Retire: binutils-testsuite-fixes.patch
- Retire: binutils-reloc-symtab.patch
- Retire: binutils-CVE-2023-1972.patch

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.40-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Nick Clifton  <nickc@redhat.com> - 2.40-12
- Spec File: migrated to SPDX license.  (#2222113)

* Mon Jul 17 2023 Nick Clifton  <nickc@redhat.com> - 2.40-11
- Spec File: Change License field to use SPDX notation.  (#2222113)

* Wed Jun 21 2023 Nick Clifton  <nickc@redhat.com> - 2.40-10
- Spec File: Add defines to enable rwx and execstack warnings.

* Wed May 31 2023 Nick Clifton  <nickc@redhat.com> - 2.40-9
- Spec File: Remove debug files from default package.  (#2208360)

* Tue May 02 2023 Nick Clifton  <nickc@redhat.com> - 2.40-8
- GOLD: Stop an abort triggered by running dwp on a file with no dwo links.  (#2192226)
- Spec File: Use _prefix.  (#2192118)

* Mon Apr 17 2023 Nick Clifton  <nickc@redhat.com> - 2.40-7
- Spec File: Fix typo.  (#2186396)
- BFD library: Fix illegal memory access when loading corrupt symbol version info.  (#2186579)

* Thu Mar 30 2023 Nick Clifton  <nickc@redhat.com> - 2.40-6
- Linker: Do not associate allocated reloc sections with the .symtab section.  (#2166419)

* Wed Mar 08 2023 Nick Clifton  <nickc@redhat.com> - 2.40-5
- Spec file: Rebuild libsframe.a with -fPIC enabled.  (#2174841)

* Mon Mar 06 2023 Nick Clifton  <nickc@redhat.com> - 2.40-4
- Spec file: Add libsframe.a to the (fake) libbfd.so.  (#2174841)

* Thu Feb 16 2023 Nick Clifton  <nickc@redhat.com> - 2.40-2
- Spec file: Remove duplicate gprofng debug file entries.
- Spec file: Fix testsuite failures for RiscV64.

* Mon Feb 13 2023 Nick Clifton  <nickc@redhat.com> - 2.40-1
- Rebase to 2.40.
- Retire: binutils-package-metadata.patch
- Retire: binutils-gas-dwarf-skip-empty-functions.patch
- Retire: binutils-CVE-38128-dwarf-abbrev-parsing.patch
- Retire: binutils-readelf-no-sections.patch
- Retire: binutils-libiberty-configure-compile-warnings.patch
- Retire: binutils-CVE-2022-4285.patch

* Tue Jan 31 2023 Nick Clifton  <nickc@redhat.com> - 2.39-10
- Spec File: Add (disabled by default) support for cross-builds of the binutils.

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.39-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Nick Clifton  <nickc@redhat.com> - 2.39-8
- Speed up objcopy's note merging algorithm.  (#29993)

* Tue Dec 13 2022 Nick Clifton  <nickc@redhat.com> - 2.39-7
- Fix a potential dereference of a NULL pointer.  (#2152946)

* Wed Nov 23 2022 Nick Clifton  <nickc@redhat.com> - 2.39-6
- Fix compile time warnings of the configure test files in the libiberty directory.  (#2144041)

* Wed Nov 02 2022 Nick Clifton  <nickc@redhat.com> - 2.39-5
- Fix configuration of s390x binutils so that it does not include support for extraneous targets.  (#2139143)

* Mon Oct 03 2022 Nick Clifton  <nickc@redhat.com> - 2.39-4
- Fix readelf's decoding of files with no sections.  (#2131609)

* Wed Aug 31 2022 Nick Clifton  <nickc@redhat.com> - 2.39-3
- Stop a potential infinite loop in the binutils DWARF parser.  (#2122675)

* Tue Aug 16 2022 Nick Clifton  <nickc@redhat.com> - 2.39-2
- Move gprofng related files into the gprofng sub-package.

* Thu Aug 11 2022 Nick Clifton  <nickc@redhat.com> - 2.39-1
- Rebase to GNU Binutils 2.39.
- Retire: binutils-CVE-2019-1010204.patch
- Retire: binutils-use-long-long.patch
- Retire: binutils-section-type.patch
- Retire: binutils-gas-loc-view.patch
- Retire: binutils-do-not-use-debuginfod.patch
- Retire: binutils-indirect-symbols.patch
- Retire: binutils-s390x-static-PIE.patch
- Retire: binutils-link-following.patch
- Retire: binutils-x86-non-canonical-references.patch
- Retire: binutils-ppc64-DT_RELR-relocs.patch
- Retire: binutils-ppc-gas-machine-directive.patch

* Wed Aug 10 2022 Luca Boccassi  <bluca@debian.org>  - 2.38-24
- Build with jansson when not bootstrapping.

* Thu Aug 04 2022 Nick Clifton  <nickc@redhat.com> - 2.38-23
- Add the --package-metadata option to the linkers.  (#2099999)

* Thu Jul 28 2022 Nick Clifton  <nickc@redhat.com> - 2.38-22
- Fix a couple of x86_64 linker testsuite failures.

* Tue Jul 26 2022 Nick Clifton  <nickc@redhat.com> - 2.38-21
- Tweak the PowerPC assembler's handling of the .machine directive.  (#2111082)

* Tue Jul 26 2022 Amit Shah  <amitshah@fedoraproject.org> - 2.38-20
- Check and enable 64-bit bfd on aarch64 and riscv64.

* Mon Jul 25 2022 Nick Clifton  <nickc@redhat.com> - 2.38-19
- Restore the use of --enable-64-bit-bfd for the AArch64 and riscv64 targets.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.38-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Nick Clifton  <nickc@redhat.com> - 2.38-16
- Fix a problem honouring readelf's -wE and -wN command line options.

* Mon Jun 13 2022 Nick Clifton  <nickc@redhat.com> - 2.38-15
- Fix a problem with PowerPC's handling of DT_RELR relocs.  (#2095622)
- Move annobin data into a separate debuginfo file.

* Wed Jun 08 2022 Nick Clifton  <nickc@redhat.com> - 2.38-14
- Fix bugs preventing the linker tests from running.

* Fri May 27 2022 Nick Clifton  <nickc@redhat.com> - 2.38-14
- Fix bug in binutils.spec file that was causing the wrong linker flags to be used.

* Fri May 27 2022 Nick Clifton  <nickc@redhat.com> - 2.38-13
- Change the ld man page so that it says that --enable-new-dtags is the default.  (#2090818)

* Tue May 24 2022 Nick Clifton  <nickc@redhat.com> - 2.38-12
- x86 linker: Disallow invalid relocations against protected symbols.  (#2089358)

* Fri May 20 2022 Nick Clifton  <nickc@redhat.com> - 2.38-11
- Stop readelf and objdump from unnecessarily following links.  (#2086863)

* Thu May 19 2022 Nick Clifton  <nickc@redhat.com> - 2.38-10
- Add support for generating static PIE binaries for s390x.  (#2088331)

* Thu May 12 2022 Nick Clifton  <nickc@redhat.com> - 2.38-9
- Fix description of gold subpackage so that it does not include the Requires fields.  (#2082919)

* Mon Apr 04 2022 Nick Clifton  <nickc@redhat.com> - 2.38-8
- Fix linker testsuite failures.

* Wed Mar 30 2022 Nick Clifton  <nickc@redhat.com> - 2.38-7
- Fix a bug handling indirect symbols.  (PR 28879) (#2068343)

* Thu Mar 10 2022 Nick Clifton  <nickc@redhat.com> - 2.38-6
- Simplify the assembler's evaluation of chained .loc view expressions.  [Second attempt]  (#2059646)

* Thu Mar 10 2022 Nick Clifton  <nickc@redhat.com> - 2.38-5
- Add an option to objdump/readelf to disable accessing debuginfod servers.  (#2051741)

* Wed Mar 09 2022 Nick Clifton  <nickc@redhat.com> - 2.38-4
- Simplify the assembler's evaluation of chained .loc view expressions.  (#2059646)

* Mon Feb 28 2022 Nick Clifton  <nickc@redhat.com> - 2.38-3
- Do not export any windows tools (if they were built).  (#2057636)

* Wed Feb 16 2022 Nick Clifton  <nickc@redhat.com> - 2.38-2
- Add support for specifying a section type in linker scripts.  (#2052801)

* Wed Feb 09 2022 Nick Clifton  <nickc@redhat.com> - 2.38-1
- Rebase on GNU Binutils 2.38.

* Thu Jan 27 2022 Nick Clifton  <nickc@redhat.com> - 2.37-25
- Borrow a patch from the GCC package to stop libtool from inserting needless runpaths into binaries.  (#2030667)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Nick Clifton  <nickc@redhat.com> - 2.37-23
- Fix a potential illegal memory access parsing a COFF format file.  (#2033716)

* Thu Dec 02 2021 Luca Boccassi  <luca.boccassi@microsoft.com> - 2.37-22
- Backport upstream patch to allow readelf to recognize packaging metadata note.

* Wed Dec 01 2021 Nick Clifton <nickc@redhat.com> - 2.37-21
- Add support for the EFI format to the AArch64 target.  (#2027515)

* Thu Nov 18 2021 Nick Clifton <nickc@redhat.com> - 2.37-20
- Add ability to warn about multibyte characters in the assembler.  (#2018848)

* Tue Nov 16 2021 Luca Boccassi <luca.boccassi@microsoft.com> - 2.37-19
- Allows linker scripts to set the SEC_READONLY flag.

* Tue Nov 09 2021 Nick Clifton <nickc@redhat.com> - 2.37-18
- Add ability to show unicode characters to display tools.

* Wed Oct 27 2021 Orion Poplawski <orion@nwra.com> - 2.37-17
- Add upstream patch to use the directory name in .file 0, fixes ccache FTBFS
  (bz#1996936)

* Tue Oct 26 2021 Timm Baeder  <tbaeder@redhat.com> - 2.27-16
- Remove leftover libtool files.

* Wed Oct 13 2021 Nick Clifton  <nickc@redhat.com> - 2.27-15
- Fix linker seg-fault compiling efivar libraries.  (#2012247)

* Wed Sep 29 2021 Nick Clifton  <nickc@redhat.com> - 2.27-14
- Fix linker testsuite failures triggered by 2.27-13 patch.  (#2008203)

* Fri Sep 17 2021 Nick Clifton  <nickc@redhat.com> - 2.27-13
- Default to an entry address of 0 for shared libraries.  (#2004952)

* Mon Sep 13 2021 Tom Stellard <tstellar@redhat.com> - 2.37-12
- Disable LTO on arm. (#1918924)

* Tue Aug 31 2021 Nick Clifton  <nickc@redhat.com> - 2.37-11
- Enable -separate-code for all architectures, not just x86/x86_64.

* Tue Aug 31 2021 Nick Clifton  <nickc@redhat.com> - 2.37-10
- Allow configuring with autonconf 2.71.  (#1999437)

* Wed Aug 18 2021 Nick Clifton  <nickc@redhat.com> - 2.37-9
- Fix a few testsuite failures.

* Wed Aug 11 2021 Stephen Gallagher <sgallagh@redhat.com> - 2.37-8
- Backport upstream patch to fix fd exhaustion
- Resolves: https://sourceware.org/bugzilla/show_bug.cgi?id=28138

* Tue Aug 10 2021 Nick Clifton  <nickc@redhat.com> - 2.37-6
- Ensure that the manual pages are generated.  (#1989836)

* Tue Aug 10 2021 Nick Clifton  <nickc@redhat.com> - 2.37-5
- Fix a local change to readelf which resulted in a success exit code for non-existant files.  (#1990817)

* Mon Aug 09 2021 Nick Clifton  <nickc@redhat.com> - 2.37-4
- Ensure that dir[0] contains pwd in gas generated DWARF-5 directory tables.  (#1966987)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Nick Clifton  <nickc@redhat.com> - 2.37-2
- Various fixes for testsuite failures.

* Mon Jul 19 2021 Nick Clifton  <nickc@redhat.com> - 2.37-1
- Rebase to GNU Binutils 2.37.
- Retire: binutils-2.36-branch-updates.patch
- Retire: binutils-CVE-2021-20197.patch
- Retire: binutils-CVE-2021-3530.patch
- Retire: binutils-plugin-file-descriptors.patch
- Retire: binutils-ppc-weak-undefined-plt-relocs.patch
- Retire: binutils-ppc64le-note-merge.patch
- Retire: binutils-s390-arch14-insns.patch

* Mon Jun 21 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-15
- Enable the creation of .note.gnu.property sections by the GOLD linker for x86 binaries.  (#1970961)

* Thu Jun 03 2021 Timm Bäder  <tabeder@redhat.com> - 2.36.1-14
- Set clang bconf default based on %%toolchain.
- Diable LTO when using clang.
- Disable check-rpath's test for standard runpaths.
- Make the existing tests have the gating effect.

* Tue May 18 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-13
- Increase number of file descriptors available to plugins.  (#1918924)
- Remove uses of RPATH.

* Tue May 18 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-12
- Generate PLT relocs for weak undefined PPC function symbols.  (#1960730)

* Fri May 14 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-11
- Enable file descriptor increase for plugin use.

* Thu May 13 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-10
- Enable use of new dtags.

* Fri May 07 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-9
- Fix stack exhaustion in the rust demangler.  (#1956424)

* Thu Mar 25 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-8
- Add an explicit dependency upon autoconf 2.69.  (#1942991)

* Thu Mar 11 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-7
- Extend vulnerability fix yet again.  (#1925779)

* Mon Feb 22 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-6
- Fix merging ppc64le notes (again).  (#1928936)

* Fri Feb 19 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-5
- Unretire the CVE 2021-20197 patch.

* Fri Feb 19 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-4
- Add support for the Z extensions to the s390x architecture.

* Thu Feb 18 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-3
- Fix merging ppc64le notes.  (#1928936)

* Fri Feb 12 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-2
- Fix testsuite failures triggered by locally applied patches.

* Thu Feb 11 2021 Nick Clifton  <nickc@redhat.com> - 2.36.1-1
- Rebase to GNU Binutils 2.36.1.
- Retire: binutils-2.35.1-update.patch
- Retire: binutils-CVE-2021-20197.patch
- Retire: binutils-DWARF-5-line-number-parsing.patch
- Retire: binutils-LTO-fix.patch
- Retire: binutils-Power10-fixes.patch
- Retire: binutils-SHF_LINK_ORDER.patch
- Retire: binutils-aarch64-condbranch-relocs.patch
- Retire: binutils-add-sym-cache-to-elf-link-hash.patch
- Retire: binutils-attach-to-group.patch
- Retire: binutils-config.patch
- Retire: binutils-duplicate-sections.patch
- Retire: binutils-dwarf-DW_FORM_ref8.patch
- Retire: binutils-dwarf-type-sign-2.patch
- Retire: binutils-dwarf-type-sign.patch
- Retire: binutils-elf-add-objects.patch
- Retire: binutils-gas-auto-dwarf-5.patch
- Retire: binutils-gold-gnu-properties.patch
- Retire: binutils-plugin-as-needed.patch
- Retire: binutils-ppc-annobin-disassembly.patch
- Retire: binutils-recursive-debuglink-following.patch
- Retire: binutils-s390-build.patch
- Retire: binutils-strip-merge.patch
- Retire: binutils-testsuite-failures.patch
- Retire: binutils-warnings.patch

* Mon Feb 08 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-34
- Extend vulnerability fix again.  (#1925779)

* Thu Feb 04 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-33
- Preserve debug information in libbfd.a and libopcodes.a.  (#1924068)

* Thu Feb 04 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-32
- Extend vulnerability fix again.  (#1913744)

* Wed Feb 03 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-31
- Enable PEP support for all targets.  (#1920373)

* Tue Feb 02 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-30
- Extend vulnerability fix.  (#1913744)

* Mon Feb 01 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-29
- Add support for DWARF-5 sections to the bfd linker's scripts.  (#1922707)

* Fri Jan 29 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-28
- Fix a vulnerability in the smart_rename function.  (#1913744)

* Thu Jan 28 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-27
- Fix failures is gas and ld testsuites.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.35.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-25
- Update the BFD library to handle DWARF-5 line number ranges.

* Thu Jan 21 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-24
- Update the GOLD linker to handle x86 .note.gnu.property sections.  (#1916925)

* Mon Jan 18 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-23
- Add a fix to gas to automatically enable DWARF-5 style file name tables.

* Fri Jan 15 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-22
- Add an option (currently disabled) to build a linker which generates new dtags.

* Tue Jan 12 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-21
- Ensure that bfd.h is the same for i686- and x86_64 versions of the devel rpm.  (#1915317)

* Fri Jan 08 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-20
- Fix bug running readelf on an empty file.  (#1903448)

* Thu Jan 07 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-19
- Fix bug running readelf on a file that cannot be read.  (#1913589)

* Mon Jan 04 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-18
- Fix linking with multiple same-name sections.  (PR 27100)

* Mon Jan 04 2021 Nick Clifton  <nickc@redhat.com> - 2.35.1-17
- Fix linking mixed SHF_LINK_ORDER and non-SHF_LINK_ORDER sections.  (#1907945)

* Thu Nov 26 2020 Florian Weimer <fweimer@redhat.com> - 2.35.1-16
- NVR bump for toolchain rebuild

* Wed Nov 25 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-15
- Import fixes added to the 2.35 branch after the 2.35.1 release.

* Tue Nov 10 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-14
- Add support for DW_FORM_ref8 when parsing DWARF types.  (#1893921)

* Tue Nov 03 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-13
- Extend fix for erroneous decoding of LEB128 values.

* Tue Nov 03 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-12
- Another correction for plugin as-needed patch.  (#1889763)

* Wed Oct 28 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-11
- Correction for plugin as-needed patch.  (#1889763)

* Tue Oct 27 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-8
- Really fix erroneous decoding of LEB128 values.  (#1891171)

* Wed Oct 21 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-7
- Fix erroneous decoding of LEB128 values.  (#188716)

* Thu Oct 15 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-6
- Make readelf and objdump recursively follow debug links.  (PR 26595)

* Fri Oct 09 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-5
- Allow plugin syms to mark as-needed shared libs needed

* Thu Oct 08 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-4
- Fix various problems with Power10 support.

* Tue Oct 06 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-3
- Fix strip when merging multiple same-named sections.  (#1885607)

* Mon Sep 21 2020 Nick Clifton  <nickc@redhat.com> - 2.35.1-1
- Rebase to GNU Binutils 2.35.1 release.
- Retire: binutils-gas-dwarf-level-4.patch
- Retire: binutils-aarch64-plt-sh_entsize.patch
- Retire: binutils-ppc-rename-xvcvbf16sp-to-xvcvbf16spn.patch
- Retire: binutils-dwarf-5-fixes.patch

* Fri Sep 11 2020 Nick Clifton  <nickc@redhat.com> - 2.35-14
- Fix the PowerPC disassembler so that it ignores annobin symbols.

* Thu Sep 10 2020 Nick Clifton  <nickc@redhat.com> - 2.35-13
- Fix the handling of relocations for AArch64 conditional branches.

* Tue Aug 25 2020 Nick Clifton  <nickc@redhat.com> - 2.35-12
- Import fixes from GNU binutils mainline for handling DWARF-5 debug information.

* Mon Aug 24 2020 Nick Clifton  <nickc@redhat.com> - 2.35-11
- Rename the PPC xvcvbf16sp instruction to xvcvbf16spn.

* Fri Jul 31 2020 Jeff Law  <nickc@redhat.com> - 2.35-10
- Re-enable LTO

* Fri Jul 31 2020 Jeff Law  <nickc@redhat.com> - 2.35-9
- Disable LTO for bootstrapping purposes

* Fri Jul 31 2020 Nick Clifton  <nickc@redhat.com> - 2.35-8
- Fix building with LTO enabled.

* Fri Jul 31 2020 Nick Clifton  <nickc@redhat.com> - 2.35-7
- Set the sh_entsize field of the AArch64's PLT section to 0.  (PR 26312)

* Thu Jul 30 2020 Richard W.M. Jones <rjones@redhat.com> - 2.35-6
- Disable LTO again, it causes "ar" to segfault.

* Thu Jul 30 2020 Nick Clifton  <nickc@redhat.com> - 2.35-5
- Default to DWARF level 3 in the assembler.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 26 2020 Jeff Law  <nickc@redhat.com> - 2.35-2
- Disable LTO for now

* Sun Jul 26 2020 Nick Clifton  <nickc@redhat.com> - 2.35-1
- Rebase to GNU Binutils 2.35.  (#1854613)

* Mon Jul 20 2020 Jeff Law  <law@redhat.com> - 2.34-9
- Fix more configure tests compromised by LTO.

* Sun Jul 19 2020 Jeff Law  <law@redhat.com> - 2.34-9
- Fix configure test compromised by LTO.  Add appropriate BuildRequires
  and force rebuliding the configure files in the appropriate dirs
- Fix various warnings exposed by LTO.

* Tue Jul 07 2020 Jeff Law  <law@redhat.com> - 2.34-8
- Switch to using %%autosetup.

* Tue Jun 16 2020 Nick Clifton  <nickc@redhat.com> - 2.34-7
- Add BPF support to the s390x target.  (#1825193)

* Tue May 26 2020 Nick Clifton  <nickc@redhat.com> - 2.34-6
- Enhance the error message displayed by the BFD library when it fails to load a plugin.  (#1836618)

* Fri May 22 2020 Nick Clifton  <nickc@redhat.com> - 2.34-5
- Rebase to tip of GNU Binutils 2.34 branch, brining in LTO fixes.
- Retire: binutils-nm-lto-plugin.patch

* Tue Apr 28 2020 Nick Clifton  <nickc@redhat.com> - 2.34-4
- Fix seg fault when loading plugins via symlinks.  (#1828587)

* Fri Apr 17 2020 Nick Clifton  <nickc@redhat.com> - 2.34-3
- Add support for the BPF target.  (#1825193)

* Sun Feb 16 2020 Nick Clifton  <nickc@redhat.com> - 2.34-2
- Fix the plugin support architecture to allow proper symbol info handling.  (PR 25355)

* Sun Feb 02 2020 Nick Clifton  <nickc@redhat.com> - 2.34-1
- Rebase to GNU Binutils 2.34.  (#1793098)
- Retire: binutils-improved-note-merging.patch
- Retire: binutils-CVE-2019-17451.patch
- Retire: binutils-CVE-2019-17450.patch
- Retire: binutils-addr2line-fixes.patch

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.33.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 David Abdurachmanov  <david.abdurachmanov@sifive.com> - 2.33.1-12
- Enable 64-bit BFD and PEP support for riscv.  (#1794343)

* Thu Jan 02 2020 Nick Clifton  <nickc@redhat.com> - 2.33.1-11
- Improve the accuracy of addr2line.  (#1760967)

* Mon Dec 02 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-10
- Re-enable strip merging build notes.  (#1777760)

* Mon Nov 25 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-9
- Remove spurious code left in gold-mimatched-section-flags patch.  (#1775750)

* Thu Nov 21 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-8
- Fix a buffer overrun in the note merging code.  (#1774507)

* Wed Nov 13 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-7
- Fix a potential seg-fault in the BFD library when parsing pathalogical debug_info sections.  (#1771669)
- Fix a potential memory exhaustion in the BFD library when parsing corrupt DWARF debug information.  (#1771678)

* Wed Nov 06 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-6
- Stop objcopy from creating null filled note sections when merging notes.

* Wed Nov 06 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-5
- Strip: Do not merge notes unless explicitly requested to do so.

* Tue Nov 05 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-4
- Objcopy: Do not generate a failure exit status if note merging fails.  (#1767937)

* Wed Oct 30 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-3
- Fix the verification of the installed linker symlink.  (#1767000)

* Mon Oct 28 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-2
- Improve objdump's ability to merge GNU build attribute notes.

* Mon Oct 14 2019 Nick Clifton  <nickc@redhat.com> - 2.33.1-1
- Rebase to GNU Binutils 2.33.1.
- Retire: binutils-CVE-2019-9073.patch
- Retire: binutils-CVE-2019-9074.patch
- Retire: binutils-CVE-2019-9075.patch
- Retire: binutils-CVE-2019-9077.patch
- Retire: binutils-disassembling-efi-files.patch
- Retire: binutils-CVE-2019-9071.patch
- Retire: binutils-gas-build-note-relocs.patch
- Retire: binutils-do-not-warn-about-debuginfo-files.patch
- Retire: binutils-do-not-merge-differing-SHF_EXCLUDE-groups.patch
- Retire: binutils-rh1736114.patch
- Retire: binutils-objcopy-gnu-build-version-notes.patch
- Retire: binutils-CVE-2019-14250.patch
- Retire: binutils-CVE-2019-14444.patch
- Retire: binutils-gcc-10-fixes.patch
- Retire: binutils-remove-old-formats.patch
- Retire: binutils-aarch64-gold-PLT-for-MOVW_ABS.patch

* Fri Oct 04 2019 Nick Clifton  <nickc@redhat.com> - 2.32-27
- Remove support for old file formats (ihex, tekhex, verilog) as they are a constant source of CVEs.

* Wed Sep 25 2019 Nick Clifton  <nickc@redhat.com> - 2.32-26
- Add an option to build using clang instead of gcc.

* Tue Sep 24 2019 Nick Clifton  <nickc@redhat.com> - 2.32-25
- Fix building with gcc-10.

* Tue Aug 13 2019 Nick Clifton  <nickc@redhat.com> - 2.32-24
- Fix potential integer overflow in readelf.  (#1740470)

* Fri Aug 09 2019 Nick Clifton  <nickc@redhat.com> - 2.32-23
- Fix potential integer overflow in GOLD.  (#1739491)

* Tue Aug 06 2019 Nick Clifton  <nickc@redhat.com> - 2.32-22
- Stop GOLD from seg-faulting on a corrupt input with a fuzzed section offset.  (#1735605)

* Mon Aug 05 2019 Nick Clifton  <nickc@redhat.com> - 2.32-21
- Stop strip from complaining if the first build note is not a version note.  (#1736114)

* Fri Aug  2 2019 Florian Weimer <fweimer@redhat.com> - 2.32-20
- Fix ld -Map not to produce corrupt ELF notes (#1736114)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.32-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Nick Clifton  <nickc@redhat.com> - 2.32-18
- Stops the linker from merging section groups with different SHF_EXCLUDE flags.  (#1730906)

* Tue Jul 02 2019 Nick Clifton  <nickc@redhat.com> - 2.32-17
- Stop the BFD library from complaining about sections found inside debuginfo files.  (PR 24717)

* Mon Jul 01 2019 Nick Clifton  <nickc@redhat.com> - 2.32-16
- Stop gas from triggering a seg-fault when creating relocs for build notes.  (PR 24748)

* Mon Jun 24 2019 Nick Clifton  <nickc@redhat.com> - 2.32-15
- Stop gold from aborting when it encounters input sections with the same name and different flags.  (#1722715)

* Tue May 21 2019 Nick Clifton  <nickc@redhat.com> - 2.32-14
- Import fix for PR 23870 in order to help building Go binaries.

* Mon Apr 29 2019 Nick Clifton  <nickc@redhat.com> - 2.32-13
- Do not include ld.gold in the base binutils package.  (#1703714)

* Wed Apr 24 2019 Björn Esser <besser82@fedoraproject.org> - 2.32-12
- Remove hardcoded gzip suffix from GNU info pages

* Wed Apr 10 2019 Nick Clifton  <nickc@redhat.com> - 2.32-11
- Fix a stack exhaustion problem in libiberty's name demangling code.  (#1680658)

* Mon Mar 18 2019 David Abdurachmanov  <david.abdurachmanov@gmail.com> - 2.32-10
- Disable ld.gold on RISC-V and fix file installation issues.

* Wed Mar 06 2019 Nick Clifton  <nickc@redhat.com> - 2.32-9
- Stop potential illegal memory access when disassembling an EFI binary.  (#1685727)

* Wed Feb 27 2019 Nick Clifton  <nickc@redhat.com> - 2.32-8
- Fix requirements and use of the alternatives mechanism.  (#1683408, #1683466)

* Tue Feb 26 2019 Nick Clifton  <nickc@redhat.com> - 2.32-7
- Move GOLD into a sub-package of BINUTILS.

* Tue Feb 26 2019 Nick Clifton  <nickc@redhat.com> - 2.32-6
- Stop potential illegal memory access when parsing a corrupt MIPS binary.  (#1680676)

* Tue Feb 26 2019 Nick Clifton  <nickc@redhat.com> - 2.32-5
- Stop potential illegal memory access when parsing corrupt archives.  (#1680670)

* Mon Feb 25 2019 Nick Clifton  <nickc@redhat.com> - 2.32-4
- Stop potential illegal memory access when parsing corrupt PE files.  (#1680682)

* Mon Feb 25 2019 Nick Clifton  <nickc@redhat.com> - 2.32-3
- Improve objdump's handling of corrupt input files.  (#1680663)

* Wed Feb 20 2019 Nick Clifton  <nickc@redhat.com> - 2.32-2
- Fix some bfd linker testsuite failures.

* Wed Feb 20 2019 Nick Clifton  <nickc@redhat.com> - 2.32-1
- Rebase to GNU Binutils 2.32
- Retire: binutils-s390-partial-relro.patch
- Retire: binutils-note-merge-improvements.patch
- Retire: Retire: binutils-merge-attribute-sections.patch
- Retire: binutils-gold-discard-version-info.patch
- Retire: binutils-gas-input-matches-output.patch
- Retire: binutils-fix-testsuite-failures.patch
- Retire: binutils-do-not-provide-shared-section-symbols.patch
- Retire: binutils-disable-readelf-gap-reports.patch
- Retire: binutils-detect-corrupt-sym-version-info.patch
- Retire: binutils-delay-ld-script-constant-eval.patch
- Retire: binutils-clear-version-info.patch
- Retire: binutils-CVE-2018-20002.patch
- Retire: binutils-CVE-2018-17358.patch
- Retire: binutils-2.31-export-demangle.h.patch
- Retire: binutils-2.28-ignore-gold-duplicates.patch
- Retire: binutils-2.26-lto.patch

* Mon Feb 18 2019 Nick Clifton  <nickc@redhat.com> - 2.31.1-23
- Ensure that decompressed sections have the correct alignment.  (#1678204)

* Thu Feb 14 2019 Nick Clifton  <nickc@redhat.com> - 2.31.1-22
- Rework the post uninstall stage to avoid mysterious error from ldconfig.  (#1673912)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.31.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Nick Clifton  <nickc@redhat.com> - 2.31.1-20
- Fix the assembler's check that the output file is not also one of the input files.  (#1660279)

* Thu Jan 03 2019 Nick Clifton  <nickc@redhat.com> - 2.31.1-19
- Fix a memory leak reading minisymbols.  (#1661535)

* Wed Jan 02 2019 Nick Clifton  <nickc@redhat.com> - 2.31.1-18
- Ensure that GOLD is linked with pthread library.  (#1636479)

* Wed Nov 28 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-17
- Stop gold from warning about discard version information unless explicitly requested.  (#1654153)

* Thu Nov 15 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-16
- Remove debugging fprintf statement accidentally left in patch.  (#1645828)

* Fri Oct 12 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-15
- Allow OS specific sections in section groups.  (#1639485)

* Fri Sep 28 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-14
- Fix a potential buffer overrun when parsing a corrupt ELF file.  (#1632912)
- Add a .attach_to_group pseuo-op to assembler (for use by annobin).  (#1630574)
- Stop the binutils from statically linking with libstdc++.  (#1630550)
- Include gold testsuite results in test logs.
- Disable readelf's reporting of gaps in build notes.  (#1623556)

* Tue Sep 04 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-13
- Delay the evaluation of linker script constants until after the configuration options have been set.  (#1624751)

* Tue Aug 28 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-12
- Detect and report corrupt symbol version information.  (#1599521)

* Tue Aug 14 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-11
- Remove the version information from a dynamic symbol that is being overridden.  (#1614920)

* Mon Aug 06 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-10
- Improve objcopy's --merge-notes option.  (#1608390)

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 2.31.1-9
- Rebuild with fixed binutils

* Mon Jul 30 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-8
- Move the .gnu.build.attributes section to after the .comment section.

* Fri Jul 27 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-7
- Fix a thinko in the merge patch.

* Fri Jul 27 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-6
- Fix a typo in the merge patch.

* Thu Jul 26 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-5
- Merge .gnu.build.attribute sections together.  (#1608390)

* Tue Jul 24 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-3
- Extend gold linker patch to cover subsections of .gnu.build.attributes.  (#1607054)

* Thu Jul 19 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-2
- Improve partial relro support for the s/390.

* Thu Jul 19 2018 Nick Clifton  <nickc@redhat.com> - 2.31.1-1
- Rebase to official 2.31.1 GNU Binutils release.
- Retire: binutils-2.22.52.0.1-export-demangle.h.patch
- Retire: binutils-2.30-allow_R_AARCH64-symbols.patch
- Retire: binutils-CVE-2018-10372.patch
- Retire: binutils-CVE-2018-10373.patch
- Retire: binutils-CVE-2018-10534.patch
- Retire: binutils-CVE-2018-10535.patch
- Retire: binutils-CVE-2018-6323.patch
- Retire: binutils-CVE-2018-6759.patch
- Retire: binutils-CVE-2018-7208.patch
- Retire: binutils-CVE-2018-7568.patch
- Retire: binutils-CVE-2018-7569.patch
- Retire: binutils-CVE-2018-7570.patch
- Retire: binutils-CVE-2018-7642.patch
- Retire: binutils-CVE-2018-7643.patch
- Retire: binutils-CVE-2018-8945.patch
- Retire: binutils-PowerPC-IEEE-long-double-warnings.patch
- Retire: binutils-debug-section-marking.patch
- Retire: binutils-gas-build-notes.patch
- Retire: binutils-gold-llvm-plugin.patch
- Retire: binutils-ifunc-relocs-in-notes.patch
- Retire: binutils-linkonce-notes.patch
- Retire: binutils-missing-notes.patch
- Retire: binutils-page-to-segment-assignment.patch
- Retire: binutils-revert-PowerPC-speculation-barriers.patch
- Retire: binutils-skip-dwo-search-if-not-needed.patch
- Retire: binutils-speed-up-objdump.patch
- Retire: binutils-strip-unknown-relocs.patch
- Retire: binutils-x86-local-relocs.patch
- Retire: binutils-x86-local-version.patch

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Nick Clifton  <nickc@redhat.com> 2.30.90-3
- Stop gold from complaining about annobin note relocs against symbols in sections which have been discarded.  (#1600431)

* Tue Jul 10 2018 Nick Clifton  <nickc@redhat.com> 2.30.90-2
- Revert fix for PR 23161 which was placing unversioned section symbols (_edata, _end, __bss_start) into shared libraries.  (#1599521)

* Mon Jul  9 2018 Nick Clifton  <nickc@redhat.com> 2.30.90-1
- Rebase to a snapshot of the soon-to-be-created 2.31 FSF release.

* Fri Jul  6 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.30-26
- Fix the generation of relocations for assembler created notes.  (#1598551)

* Wed Jul  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.30-25
- Minor spec cleanups and fixes.

* Mon Jun 18 2018 Nick Clifton  <nickc@redhat.com> 2.30-24
- When installing both ld.bfd and ld.gold, do not reset the current alternative if upgrading.  (#1592069)

* Tue Jun 12 2018 Nick Clifton  <nickc@redhat.com> 2.30-23
- Correct warning messages about incompatible PowerPC IEEE long double settings.

* Fri Jun 01 2018 Nick Clifton  <nickc@redhat.com> 2.30-22
- Fix handling of local versioned symbols by the x86 linker.  (PR 23194)
- Fix linker testsuite failures.

* Thu May 17 2018 Nick Clifton  <nickc@redhat.com> 2.30-21
- Fix a seg-fault parsing PE format binaries.  (#1560829)

* Mon May 14 2018 Nick Clifton  <nickc@redhat.com> 2.30-20
- Have the x86 linker resolve relocations against the _end, _edata and __bss_start symbols locally.  (#1576735)
- Do not generate GNU build notes for linkonce sections.  (#1576362)

* Thu May 10 2018 Nick Clifton  <nickc@redhat.com> 2.30-19
- Fix a seg-fault running objcopy on a corrupt PE format file.  (#1574702)
- Fix a seg-fault running objcopy on a corrupt ELF format file.  (#1574705)

* Tue May 01 2018 Nick Clifton  <nickc@redhat.com> 2.30-18
- Fix a seg-fault parsing corrupt DWARF information.  (#1573360)
- Fix another seg-fault parsing corrupt DWARF information.  (#1573367)
- Fix a seg-fault copying a corrupt ELF file.  (#1551788)
- Fix a seg-fault parsing a large ELF files on a 32-bit host.  (#1539891)
- Fix a seg-fault running nm on a corrupt ELF file.  (#15343247)
- Fix a seg-fault running nm on a file containing corrupt DWARF information.  (#1551781)
- Fix another seg-fault running nm on a file containing corrupt DWARF information.  (#1551763)

* Fri Apr 27 2018 Nick Clifton  <nickc@redhat.com> 2.30-17
- Disable the automatic generation of annobin notes.  (#1572485)

* Fri Apr 27 2018 Nick Clifton  <nickc@redhat.com> 2.30-16
- Fix for PR 22887 - crashing objdump by passing it a corrupt AOUT binary.  (#1553115)
- Fix for PR 22905 - crashing objdump by passing it a corrupt DWARF file.  (#1553122)
- Fix for PR 22741 - crashing objdump by passing it a corrupt COFF file.  (#1571918)

* Thu Apr 26 2018 Nick Clifton  <nickc@redhat.com> 2.30-15
- Enhance the assembler to automatically generate annobin notes if none are present in the input.

* Thu Mar 22 2018 Nick Clifton  <nickc@redhat.com> 2.30-14
- Fix the GOLD linker's processing of protected symbols created by the LLVM plugin.  (#1559234 and PR 22868)

* Wed Mar 14 2018 Nick Clifton  <nickc@redhat.com> 2.30-13
- Do not discard debugobj files created by GCC v8 LTO wrapper.  (#1543912 and RHBZ 84847 and PR 20882)

* Fri Mar 09 2018 Nick Clifton  <nickc@redhat.com> 2.30-12
- Treat relocs against s390x IFUNC symbols in note sections as relocs against the FUNC symbol instead.
- Combined previous patches into one which covers all ifunc supporting architectures.    (#1553705)
- Retire binutils-s390-ifunc-relocs-in-notes.patch
- Retire binutils-x86_64-ifunc-relocs-in-notes.patch

* Fri Mar 09 2018 Nick Clifton  <nickc@redhat.com> 2.30-11
- Treat relocs against s390x IFUNC symbols in note sections as relocs against the FUNC symbol instead.  (#1553705)

* Wed Mar 07 2018 Nick Clifton  <nickc@redhat.com> 2.30-10
- Ignore duplicate symbols generated by GOLD.  (#1458003)

* Wed Mar 07 2018 Nick Clifton  <nickc@redhat.com> 2.30-9
- Stop strip from replacing unknown relocs with null relocs.  (#1545386)

* Wed Mar 07 2018 Nick Clifton  <nickc@redhat.com> 2.30-8
- Ignore duplicate symbols generated by GOLD.  (#1458003)

* Mon Mar 05 2018 Nick Clifton  <nickc@redhat.com> 2.30-7
- Speed up objdump.  (#1551540)

* Thu Feb 22 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 2.30-6
- Fix R_AARCH64 symbols (PR 22764) (#1547781)

* Wed Feb 21 2018 Nick Clifton  <nickc@redhat.com> 2.30-5
- Fix assignment of pages to segments. (PR 22758)
- Inject RPM_LD_FLAGS into the build.  (#1541027)
- Fix slowdown in readelf when examining files with lots of debug information.  (PR 22802)
- Remove support for PowerPC speculation barrier insertion.
- Rebase on 2.30
- Retire binutils-2.22.52.0.1-relro-on-by-default.patch
- Retire binutils-2.28-dynamic-section-warning.patch
- Retire binutils-2.29-skip-rp14918-test-for-arm.patch
- Retire binutils-2.29.1-gold-start-stop.patch
- Retire binutils-2.29.1-readelf-use-dynamic.patch
- Retire binutils-aarch64-pie.patch
- Retire binutils-coverity.patch
- Retire binutils-ppc64-stub-creation.patch
- Retire binutils-strip-delete-relocs.patch
- Retire binutils-support-v3-build-notes.patch
- Retire binutils-z-undefs.patch

* Mon Feb 12 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-19
- Remove comment that explained how to disable annobin.  (#1541027)

* Thu Feb 08 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-18
- Inject RPM_LD_FLAGS into the build.  (#1541027)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.29.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Feb 01 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-16
- Use make_build and make_install macros.  (#1541027)

* Thu Jan 25 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-15
- Reenable binary annotations.

* Thu Jan 25 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-14
- Fix creation of PowerPC64 function call stubs.  (#1523457)
- Disable -z defs during build.
- Disable binary annotations.  (temporary ?)

* Mon Jan 22 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-13
- Fix bugs in AArch64 static PIE support.  (#1536645)

* Tue Jan 16 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-12
- Add "-z undefs" option to the linker.

* Thu Jan 11 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-11
- *Do* enable relro by default for the PowerPC64 architecture.  (#1523946)

* Wed Jan 03 2018 Nick Clifton  <nickc@redhat.com> 2.29.1-10
- Update readelf and objcopy to support v3 build notes.

* Tue Dec 12 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-9
- Have readelf display extra symbol information at the end of the line.  (#1479302)

* Mon Dec 11 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-8
- Do not enable relro by default for the PowerPC64 architecture.  (#1523946)

* Thu Dec 07 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-7
- Stop strip from crashing when deleteing relocs in a file with annobin notes.  (#1520805)

* Wed Dec 06 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-6
- Have readelf return an exit failure status when attempting to process an empty file. (#1522732)

* Tue Nov 28 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-5
- Disable PLT elision for x86/x86_64.  (#1452111 and #1333481)

* Wed Nov 01 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-4
- Have readelf suggest the use of --use-dynamic when there are dynamic relocs that could have been displayed.  (#1507694)

* Wed Oct 18 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-3
- Fix the GOLD linker's generation of relocations for start and stop symbols.  (#1500898)

* Thu Sep 28 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-2
- Enable GOLD for PPC64 and s390x. (#1173780)
- Retire: binutils-2.20.51.0.10-sec-merge-emit.patch.
  (It has been redundant for a long time now...)

* Tue Sep 26 2017 Nick Clifton  <nickc@redhat.com> 2.29.1-1
- Rebase on FSF binutils 2.29.1 release.
- Retire: binutils-2.29-ppc64-plt-localentry0-disable.patch
- Retire: binutils-2.29-non-elf-orphan-skip.patch

* Thu Sep 14 2017 Nick Clifton  <nickc@redhat.com> 2.29-10
- Extend fix for PR 21884.
  (#1491023)

* Thu Sep 14 2017 Nick Clifton  <nickc@redhat.com> 2.29-8
- Import fix for PR 21884 which stops a seg-fault in the linker when changing output format to binary during a final link.
  (#1491023)

* Sun Sep 10 2017 Nick Clifton  <nickc@redhat.com> - 2.29-7
- Annotate patches with reason and lifetime expectances.
- Retire: binutils-2.24-ldforcele.patch
- Retire: binutils-2.25-set-long-long.patch
- Retire: binutils-2.25.1-cleansweep.patch
- Retire: binutils-2.26-fix-compile-warnings.patch
- Retire: binutils-2.28-ignore-gold-duplicates.patch

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Nick Clifton  <nickc@redhat.com> 2.29-5
- Update ppc64 localentry0 patch with changes made by Alan Modra to the FSF binutils sources.
  (#1475636)

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.29-4
- Rebuild with binutils fix for ppc64le, bootstrapping (#1475636)

* Fri Jul 28 2017 Nick Clifton  <nickc@redhat.com> 2.29-3
- Do not enable the PPC64 plt-localentry0 linker optimization by default.
  (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Nick Clifton  <nickc@redhat.com> 2.29-1
- Rebase on FSF binutils 2.29.
- Retire: binutils-2.20.51.0.10-ppc64-pie.patch
- Retire: binutils-2.27-ld-buffer-overflow.patch
- Retire: binutils-2.28-libiberty-bugfixes.patch
- Retire: binutils-gnu-build-notes.patch
- Retire: binutils-2.28-gas-comp_dir.patch
- Retire: binutils-2.28-ppc-dynamic-relocs.patch
- Retire: binutils-2.28-dynamic-section-warning.patch
- Retire: binutils-2.28-aarch64-copy-relocs.patch
- Retire: binutils-2.28-DW_AT_export_symbols.patch

* Thu Jul 20 2017 Nick Clifton  <nickc@redhat.com> 2.28-14
- Remove -flto compile time option accidentally added to CFLAGS.

* Thu Jul 20 2017 Nick Clifton  <nickc@redhat.com> 2.28-13
- Add support for displaying new DWARF5 tags.
  (#1472966)

* Wed Jul 19 2017 Nick Clifton  <nickc@redhat.com> 2.28-12
- Correct snafu in previous delta that broke building s390 binaries.
  (#1472486)

* Mon Jul 17 2017 Nick Clifton  <nickc@redhat.com> 2.28-11
- Fix s390 assembler so that it remove fake local symbols from its output.
  (#1460254)

* Wed Jun 28 2017 Nick Clifton  <nickc@redhat.com> 2.28-10
- Update support for GNU Build Attribute notes to include version 2 notes.

* Thu Jun 15 2017 Nick Clifton  <nickc@redhat.com> 2.28-9
- Update patch to fix AArch64 copy reloc generation.
  (#1452170)

* Fri Jun 09 2017 Nick Clifton  <nickc@redhat.com> 2.28-8
- Ignore duplicate indirect symbols generated by the GOLD linker.
  (#1458003)

* Thu Jun 08 2017 Nick Clifton  <nickc@redhat.com> 2.28-7
- Eliminate the generation of incorrect dynamic copy relocations on AArch64.
  (#1452170)

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Mar 20 2017 Nick Clifton  <nickc@redhat.com> 2.28-5
- Update GNU BUILD NOTES patch.
- Import FSF binutils patch to fix running readelf on debug info binaries.
  (#1434050)

* Wed Mar 08 2017 Nick Clifton  <nickc@redhat.com> 2.28-4
- Update GNU BUILD NOTES patch.
- Import FSF binutils patch to fix an abort with PowerPC dynamic relocs.

* Mon Mar 06 2017 Mark Wielaard  <mjw@redhat.com> 2.28-3
- Backport patch to add support for putting name, comp_dir and
  producer strings into the .debug_str section. 
  (#1429389)

* Fri Mar 03 2017 Nick Clifton  <nickc@redhat.com> 2.28-2
- Add support for GNU BUILD NOTEs.

* Thu Mar 02 2017 Nick Clifton  <nickc@redhat.com> 2.28-1
- Rebase on FSF binutils v2.28.
- Retire: binutils-2.23.52.0.1-addr2line-dynsymtab.patch
- Retire: binutils-2.27-local-dynsym-count.patch
- Retire: binutils-2.27-monotonic-section-offsets.patch
- Retire: binutils-2.27-arm-aarch64-default-relro.patch
- Retire: binutils-2.28-gold.patch
- Retire: binutils-2.27-objdump-improvements.patch
- Retire: binutils-2.27-dwarf-parse-speedup.patch
- Retire: binutils-2.27-objdump-improvements.2.patch
- Retire: binutils-2.27-arm-binary-objects.patch
- Retire: binutils-2.27-ppc-fp-attributes.patch
- Add patch to sync libiberty with FSF GCC mainline.
  (#1428310)

* Fri Feb 17 2017 Nick Clifton  <nickc@redhat.com> 2.27-19
- Add support for PowerPC FP attributes.
  (#1422461)

* Wed Feb 15 2017 Nick Clifton  <nickc@redhat.com> 2.27-18
- Fix running the ARM port of the linker on BINARY objects.
  (#1422577)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.27-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Stephen Gallagher  <sgallagh@redhat.com> 2.27-16
- Install COPYING[*] files using the % license macro.
  (#1418430)

* Tue Jan 31 2017 Nick Clifton  <nickc@redhat.com> 2.27-15
- Fix buffer overflows when printing translated messages.
  (#1417411)

* Mon Jan 16 2017 Nick Clifton  <nickc@redhat.com> 2.27-14
- Include the filename concerned in readelf error messages.
  (#1412348)

* Mon Jan 09 2017 Nick Clifton  <nickc@redhat.com> 2.27-13
- Another speed up for objdump when displaying source code alognside disassembly.
  (#1397113)

* Tue Nov 22 2016 Nick Clifton  <nickc@redhat.com> 2.27-12
- Speed up objdump when displaying source code alognside disassembly.
  (#1397113)

* Tue Nov 08 2016 Nick Clifton  <nickc@redhat.com> 2.27-11
- Fix objdumps disassembly of dynamic executables.
  (#1370275)

* Fri Nov 04 2016 Nick Clifton  <nickc@redhat.com> 2.27-10
- Fix GOLD for ARM and AARCH64
  (#1386126)

* Mon Sep 26 2016 Mark Pryor  <pryorm09@gmail.com> 2.27-9
- Fix invocation of /sbin/ldconfig when reinstalling binutils
  in order to prevent warnings from rpm.
  (#1379030)
  (#1379117)

* Thu Sep 22 2016 Mark Pryor  <pryorm09@gmail.com> 2.27-8
- Add i386pep emulation for all EFI capable CPU types.
  (#1376870)

* Wed Sep 21 2016 Nick Clifton  <nickc@redhat.com> 2.27-7
- Use --with-sysroot=/ for native targets.  This prevents the default
  sysroot of /usr/local/<target>/sys-root from being used, which breaks 
  locating needed shared libaries, but still allows the --sysroot
  linker command line option to be effective.
  (#1374889)
  (#1377803)
  (#1377949)

* Tue Sep 20 2016 Nick Clifton  <nickc@redhat.com> 2.27-6
- Omit building GOLD when bootstrapping.
- Add a generic build requirement on gcc.
- Move bison and m4 build requirements to be conditional upon building GOLD.
- Add --with-sysroot configure option when building native targets.
- Skip PR14918 linker test for ARM native targets.
  (#1374889)

* Fri Sep 16 2016 Nick Clifton  <nickc@redhat.com> 2.27-5
- Add support for building the rpm with "--with bootstrap" enabled.
- Retire: binutils-2.20.51.0.2-ia64-lib64.patch

* Thu Sep 01 2016 Nick Clifton  <nickc@redhat.com> 2.27-4
- Properly disable the default generation of compressed debug sections.
  (#1366182)

* Fri Aug 19 2016 Nick Clifton  <nickc@redhat.com> 2.27-3
- Put sections in a monotonically increasing order of file offset.
- Allow ARM and AArch64 targets to have relro on by default.

* Mon Aug 15 2016 Nick Clifton  <nickc@redhat.com> 2.27-2
- Fix computation of sh_info field in the header of .dynsym sections.

* Wed Aug 03 2016 Nick Clifton  <nickc@redhat.com> 2.27-1
- Rebase on FSF binutils 2.27 release.
- Retire: binutils-2.26-formatting.patch
- Retire: binutils-2.26-Bsymbolic_PIE.patch
- Retire: binutils-rh1312151.patch
- Retire: binutils-2.26-fix-GOT-offset-calculation.patch
- Retire: binutils-2.26-common-definitions.patch
- Retire: binutils-2.26-x86-PIE-relocations.patch

* Mon Jun 13 2016 Nick Clifton  <nickc@redhat.com> 2.26-23
- Enable support for GCC's LTO.
  (#1342618)

* Thu Jun 02 2016 Nick Clifton  <nickc@redhat.com> 2.26-22
- Retire the copy-osabi patch.
  (#1252066)

* Mon May 09 2016 Nick Clifton  <nickc@redhat.com> 2.26-21
- Fix another compile time warning, this time in tc-arm.c.
  (#1333695)

* Fri Apr 22 2016 Nick Clifton  <nickc@redhat.com> 2.26-20
- Housekeeping: Delete retired patches.  Renumber patches.
- Increase version number past F24 because F24 update is blocked by a version number comparison.

* Fri Mar 18 2016 Nick Clifton  <nickc@redhat.com> 2.26-16
- Import patch to fix generation of x86 relocs in PIE mode.  (PR 19827)

* Mon Mar 14 2016 Nick Clifton  <nickc@redhat.com> 2.26-15
- Import patch to have common symbols in an executable override definitions in shared objects (PR 19579)
  (#1312507)

* Mon Feb 29 2016 Nick Clifton  <nickc@redhat.com> 2.26-14
- Import patch to fix x86 GOT offset calculation in 2.26 sources (PR 19601)
  (#1312489)

* Fri Feb 26 2016 Nick Clifton  <nickc@redhat.com> 2.26-13
- Import patch to fix symbol versioning bug in 2.26 sources (PR 19698)
  (#1312151)

* Fri Feb 19 2016 Nick Clifton  <nickc@redhat.com> 2.26-12
- Import H.J.Lu's kernel LTO patch.
  (#1302071)

* Tue Feb 16 2016 poma <poma@gmail.com> 2.26-11
- Enable -Bsymbolic and -Bsymbolic-functions to PIE.  Needed by Syslinux
  (#1308296)

* Wed Feb 10 2016 Nick Clifton <nickc@redhat.com> 2.26-10
- Retire: binutils-2.23.2-aarch64-em.patch
  (#1305179)

* Tue Feb 09 2016 Nick Clifton <nickc@redhat.com> 2.26-9
- Fix indentation in bfd/elf64-s390.c, gas/config/tc-ia64.c
  and bfd/pe-mips.c to avoid compile time warnings.

* Thu Feb 04 2016 Nick Clifton <nickc@redhat.com> 2.26-8
- Fix indentation in bfd/coff-[i386|x86_64].c to avoid compile time warning.
- Suppress GOLD's dir_caches destructor.
- Suppress GOLD's Reloc_stub::Key::name function.
- Suppress unused ARM architecture variations in GAS.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Nick Clifton <nickc@redhat.com> 2.26-4
- Drop the kernel patch entirely...
- Retire: binutils-2.25-kernel-ld-r.patch
- Retire: binutils-2.25.1-plugin-format-checking.patch

* Tue Jan 26 2016 Nick Clifton <nickc@redhat.com> 2.26-3
- Fix kernel patch for AVR targets.

* Mon Jan 25 2016 Nick Clifton <nickc@redhat.com> 2.26-2
- Fix kernel patch for PPC32 targets.

* Mon Jan 25 2016 Nick Clifton <nickc@redhat.com> 2.26-1
- Rebase on FSF binutils 2.26 release.
- Retire: binutils-2.25.1-ihex-parsing.patch
- Retire: binutils-2.25.1-dynamic_list.patch
- Retire: binutils-2.25.1-aarch64-pr18668.patch
- Retire: binutils-rh1247126.patch
  (#1271387)

* Thu Nov 05 2015 Nick Clifton <nickc@redhat.com> 2.25.1-9
- Prevent an infinite recursion when a plugin tries to claim a file in an unrecognised format.
  (#1174065)

* Wed Oct 28 2015 Nick Clifton <nickc@redhat.com> 2.25.1-8
- Enable little endian support when configuring for 64-bit PowerPC.
  (#1275709)

* Thu Sep 24 2015 Nick Clifton <nickc@redhat.com> 2.25.1-7
- Fix incorrectly generated binaries and DSOs on PPC platforms.
  (#1247126)

* Fri Sep 11 2015 Nick Clifton <nickc@redhat.com> 2.25.1-6
- Fix handling of AArch64 local GOT relocs.  (#1262091)

* Thu Sep 10 2015 Nick Clifton <nickc@redhat.com> 2.25.1-5
- Do not enable deterministic archives by default (#1195883)

* Thu Aug 06 2015 Rex Dieter <rdieter@fedoraproject.org> 2.25.1-4
- Qt linked with gold crash on startup (#1193044)

* Tue Aug 04 2015 Nick Clifton <nickc@redhat.com> - 2.25.1-3
- Fix the parsing of corrupt iHex files.
- Resovles: 1250141

* Tue Aug 04 2015 Nick Clifton <nickc@redhat.com> - 2.25.1-2
- Retire: binutils-2.25-aarch64-fPIC-error.patch
- Resovles: 1249969

* Thu Jul 23 2015 Nick Clifton <nickc@redhat.com> - 2.25.1-1
- Rebase on FSF binutils 2.25.1 release.
- Retire: binutils-2.25-x86_64-pie-relocs.patch

* Thu Jul 02 2015 Nick Clifton <nickc@redhat.com> - 2.25-12
- For AArch64 issue an error message when attempting to resolve a
  PC-relative dynamic reloc in a non-PIC object file.
- Related: 1232499

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Nick Clifton <nickc@redhat.com> - 2.25-10
- Make the AArch64 GOLD port use 64K pages.
- Resolves: BZ #1225156 and BZ #1215546

* Mon Apr 27 2015 Nick Clifton <nickc@redhat.com> - 2.25-8
- Require the coreutils so that touch is available.
- Resolves: BZ #1215242

* Tue Apr 21 2015 Nick Clifton <nickc@redhat.com> - 2.25-7
- Enable building GOLD for the AArch64.
- Resolves: BZ #1203057

* Thu Mar 19 2015 Nick Clifton <nickc@redhat.com> - 2.25-6
- Remove the windmc manual page, so that it is not installed.
- Resolves: BZ #1203606

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.25-6
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Feb 02 2015 Nick Clifton <nickc@redhat.com> - 2.25-5
- Fix scanning for object symbols in binutils-2.25-kernel-ld-r.patch
- Resolves: BZ #1149660

* Tue Jan 20 2015 Nick Clifton <nickc@redhat.com> - 2.25-4
- Import the fix for PR ld/17827 from FSF mainline.
- Resolves: BZ #1182511

* Mon Jan 12 2015 Nick Clifton <nickc@redhat.com> - 2.25-3
- Suppress building of GOLD for PPC, for now...
- Resolves: BZ #1173780

* Sat Dec 27 2014 Ralf Corsépius <corsepiu@fedoraproject.org> -  2.25-2
- Reflect configure.info/standards.info having been dropped (RHBZ#1177359).

* Wed Dec 24 2014 Nick Clifton <nickc@redhat.com> - 2.25-1
- Rebase on FSF binutils 2.25 release.
- Retire: binutils-2.24-s390-mkopc.patch
- Retire: binutils-2.24-elfnn-aarch64.patch
- Retire: binutils-2.24-DW_FORM_ref_addr.patch
- Retire: binutils-2.24-set-section-macros.patch
- Retire: binutils-2.24-fake-zlib-sections.patch
- Retire: binutils-2.24-arm-static-tls.patch
- Retire: binutils-2.24-fat-lto-objects.patch
- Retire: binutils-2.24-symbol-warning.patch
- Retire: binutils-2.24-aarch64-ld-shared-non-PIC-xfail.patch
- Retire: binutils-2.24-weak-sym-merge.patch
- Retire: binutils-2.24-indirect-chain.patch
- Retire: binutils-2.24-aarch64-fix-final_link_relocate.patch
- Retire: binutils-2.24-aarch64-fix-gotplt-offset-ifunc.patch
- Retire: binutils-2.24-aarch64-fix-static-ifunc.patch
- Retire: binutils-2.24-aarch64-fix-ie-relax.patch
- Retire: binutils-HEAD-change-ld-notice-interface.patch
- Retire: binutils-2.24-corrupt-binaries.patch
- Retire: binutils-2.24-strings-default-all.patch
- Retire: binutils-2.24-corrupt-ar.patch

* Thu Nov 13 2014 Nick Clifton <nickc@redhat.com> - 2.24-29
- Fix problems with the ar program reported in FSF PR 17533.
  Resolves: BZ #1162666, #1162655

* Fri Oct 31 2014 Nick Clifton <nickc@redhat.com> - 2.24-28
- Fix buffer overrun in ihex parser.
- Fix memory corruption in previous patch.
- Consoldiate corrupt handling patches into just one patch.
- Default strings command to using -a.

* Wed Oct 29 2014 Nick Clifton <nickc@redhat.com> - 2.24-27
- Fix memory corruption bug introduced by the previous patch.

* Tue Oct 28 2014 Nick Clifton <nickc@redhat.com> - 2.24-26
- Import patches for PR/17510 and PR/17512 to fix reading corrupt ELF binaries.
  Resolves: BZ #1157276, #1157277

* Mon Oct 27 2014 Nick Clifton <nickc@redhat.com> - 2.24-25
- Import patch from mainline to fix seg-fault when reading corrupt group headers.
  Resolves: BZ #1157276

* Fri Oct 24 2014 Nick Clifton <nickc@redhat.com> - 2.24-24
- Import patch from mainline to fix seg-fault when reading corrupt srec fields.
  Resolves: BZ #1156272

* Mon Aug 25 2014 Kyle McMartin <kmcmarti@redhat.com> - 2.24-23
- aarch64: increase common page size to 64KB
- binutils-HEAD-change-ld-notice-interface.patch: backport fix from HEAD
  that fixes LTO + ifunc when using ld.bfd instead of gold.
- binutils-2.24-aarch64-fix-gotplt-offset-ifunc.patch
  binutils-2.24-aarch64-fix-static-ifunc.patch, split elfnn-aarch64 patches
  into upstream git commits, to make it easier to figure out what's
  backported already
- binutils-2.24-aarch64-fix-ie-relax.patch: add fix for gd to ie relaxation
  when target register is >16 (pretty unlikely, but...)

* Thu Aug 21 2014 Kyle McMartin <kmcmarti@redhat.com> - 2.24-22
- bfd/elfnn-aarch64.c: use correct offsets in final_link_relocate
  Resolves: BZ #1126199

* Thu Aug 21 2014 Nick Clifton <nickc@redhat.com> - 2.24-21
- Import patch from mainline to fix indirect symbol resolution.
  Resolves: BZ #1123714

* Tue Aug 19 2014 Nick Clifton <nickc@redhat.com> - 2.24-20
- Enable deterministic archives by default.
  Resolves: BZ #1124342

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Nick Clifton <nickc@redhat.com> - 2.24-18
- Correct elf_merge_st_other arguments for weak symbols.
  Resolves: #1126436

* Tue Aug 12 2014 Jeff Law <law@redhat.com> - 2.24-17
- Enable gold for PPC.

* Tue Jun 24 2014 Kyle McMartin <kyle@redhat.com> - 2.24-16
- Backport a couple LTO testsuite fixes from HEAD.
  Default to -ffat-lto-objects for some ld tests, which was the default in
  gcc 4.8, but changed in 4.9, and resulted in some failures.
- Add STATIC_TLS flag on ARM when IE relocs are emitted in a shared
  library. Also fix up offsets in the testsuite resulting from the
  addition of the flags.
- XFail some ld tests on AArch64 to cut some of the spurious testsuite
  failures down.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.24-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Nick Clifton <nickc@redhat.com> - 2.24-14
- Fix detection of little endian PPC64 binaries.  (#1095885)

* Mon Apr 28 2014 Nick Clifton <nickc@redhat.com> - 2.24-13
- Fix detection of uncompressed .debug_str sections.  (#1082370)

* Tue Apr 22 2014 Nick Clifton <nickc@redhat.com> - 2.24-12
- Fix compiling using gcc 4.9  (#1087374)

* Thu Mar 27 2014 Nick Clifton <nickc@redhat.com> - 2.24-11
- Use {version} in Source string.  Delete unused patches.

* Tue Jan 28 2014 Nick Clifton <nickc@redhat.com> - 2.24-10
- Fix decoding of abbrevs using a DW_FORM_ref_addr attribute.  (#1056797)

* Tue Dec 17 2013 Nick Clifton <nickc@redhat.com> - 2.24-9
- Import fixes on 2.24 branch that affect AArch64 IFUNC and PLT handling.

* Thu Dec 05 2013 Nick Clifton <nickc@redhat.com> - 2.24-8
- Fix building opcodes library with -Werror=format-security.  (#1037026)

* Wed Dec 04 2013 Jeff Law <law@redhat.com> - 2.24-7
- Update to official binutils 2.24 release.

* Thu Nov 21 2013 Nick Clifton <nickc@redhat.com> - 2.24-6
- Update binutils 2.24 snapshot.

* Mon Nov 11 2013 Nick Clifton <nickc@redhat.com> - 2.24-5
- Update binutils 2.24 snapshot.
- Switch to using GIT instead of CVS to access the FSF repository.
- Retire binutils-2.24-nm-dynsym.patch

* Fri Oct 25 2013 Nick Clifton <nickc@redhat.com> - 2.24-4
- Update binutils 2.24 snapshot.
- Stop NM from halting if it encounters a file with no symbols when displaying dynamic symbols in multiple files.  (#1022845)

* Fri Oct 18 2013 Nick Clifton <nickc@redhat.com> - 2.24-3
- Update binutils 2.24 snapshot.

* Fri Oct 11 2013 Nick Clifton <nickc@redhat.com> - 2.24-2
- Update binutils 2.24 snapshot.

* Fri Oct 04 2013 Nick Clifton <nickc@redhat.com> - 2.24-1
- Rebase on binutils 2.24 snapshot.
- Retire: binutils-2.23.52.0.1-64-bit-thin-archives.patch,
-         binutils-2.23.52.0.1-as-doc-texinfo-fixes.patch,
-         binutils-2.23.52.0.1-check-regular-ifunc-refs.patch,
-         binutils-2.23.2-ld-texinfo-fixes.patch,
-         binutils-2.23.2-bfd-texinfo-fixes.patch,
-         binutils-2.23.2-dwz-alt-debuginfo.patch
-         binutils-2.23.2-s390-gas-machinemode.patch
-         binutils-2.23.2-xtensa.memset.patch
-         binutils-2.23.2-s390-zEC12.patch
-         binutils-2.23.2-arm-add-float-abi-to-e_flags.patch
-         binutils-2.23.51.0.1-readelf-flush-stdout.patch

* Mon Sep 09 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-14
- Make readelf flush stdout before emitting an error or warning message.  (#1005182)

* Fri Aug 30 2013 Kyle McMartin <kyle@redhat.com> 2.23.88.0.1-13
- Add the hard-float/soft-float ABI flag as appropriate for
  ET_DYN/ET_EXEC in EABI_VER5.
- Fix last changelog entry, it was release 12, not 14.

* Wed Aug 14 2013 Nick Clifton <nickc@redhat.com> 2.23.88.0.1-12
- Add support for the s/390 zEC12 architecture to gas.  (#996395)

* Mon Aug 12 2013 Nick Clifton <nickc@redhat.com> 2.23.88.0.1-11
- Fix typos in invocations of memset in elf32-xtensa.c

* Wed Aug 07 2013 Karsten Hopp <karsten@redhat.com> 2.23.88.0.1-10
- disable -Werror on ppc64p7 for #918189

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.88.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-8
- Add support for the S/390 .machinemode pseudo-op to GAS.  (#986031)

* Fri Jul 05 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-7
- Add a requirement for libstdc++-static when running the GOLD testsuite.

* Wed Jun 05 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-6
- Fix building of aarch64 targets after applying the patch for kernel ld -r modules.
- Fix building when "--with debug" is specified.

* Wed May 29 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-5
- Add support for the alternative debuging files generated by the DWZ program.  (#965255)

* Fri May 17 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-4
- Import H.J.'s patch to add support for kernel ld -r modules.
- Fix errors reported by version 5.0 of texinfo when parsing bfd documentation.

* Fri Apr 26 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-3
- Fix errors reported by version 5.0 of texinfo when parsing assembler documentation.

* Thu Apr 25 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-2
- Fix errors reported by version 5.0 of texinfo when parsing linker documentation.

* Wed Apr 24 2013 Nick Clifton <nickc@redhat.com> - 2.23.88.0.1-1
- Switch over to basing sources on the official FSF binutils releases.
- Retire binutils-2.23.52.0.1-revert-pr15149.patch.
- Update binutils-2.22.52.0.1-relro-on-by-default.patch and binutils-2.23.52.0.1-as-doc-texinfo-fixes.patch.

* Wed Apr 17 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-10
- Import patch for FSF mainline PR 15371 to fix ifunc references in shared libraries.  (#927818)

* Thu Mar 14 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-9
- Enhance opncls.c:find_separate_debug_file() to look in Fedora specific locations.
- Enhance dwarf2.c:find_line() to work with shared libraries.  (#920542)

* Wed Mar 13 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-8
- Fix addr2line to use dynamic symbols if it failed to canonicalize ordinary symbols.  (#920542)

* Wed Mar 13 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-7
- Change requirement to explicitly depend upon /usr/bin/pod2man.  (#920545)

* Wed Mar 13 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-6
- Require perl for pod2man for building man pages.  (#920545)

* Fri Mar 08 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-5
- Reverts patch for PR15149 - prevents report weak DT_NEEDED symbols.  (#918003)

* Wed Mar 06 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-4
- Enable building of GOLD for the ARM.  (#908966)

* Mon Mar 04 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-3
- Fix errors reported by version 5.0 of texinfo when parsing assembler documentaion.

* Fri Mar 01 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-2
- Fix the creation of index tables in 64-bit thin archives.  (#915411)

* Thu Feb 28 2013 Nick Clifton <nickc@redhat.com> - 2.23.52.0.1-1
- Rebase on 2.23.51.0.1 release.  (#916516)

* Fri Feb 08 2013 Nick Clifton <nickc@redhat.com> - 2.23.51.0.9-2
- Enable 64-bit BFD for aarch64.  (#908904)

* Mon Feb 04 2013 Nick Clifton <nickc@redhat.com> - 2.23.51.0.9-1
- Rebase on 2.23.51.0.9 release.  (#907089)
- Retire binutils-2.23.51.0.8-arm-whitespace.patch.

* Mon Jan 21 2013 Nick Clifton <nickc@redhat.com> - 2.23.51.0.8-4
- Allow more whitespace in ARM instructions.  (#892261)

* Tue Jan 15 2013 Patsy Franklin <pfrankli@redhat.com> - 2.23.51.0.8-3
- Add bc to BuildRequires when running the testsuite.  (#895321)

* Wed Jan 02 2013 Nick Clifton <nickc@redhat.com> - 2.23.51.0.8-2
- Add runtime link with libdl.  (#889134)

* Wed Jan 02 2013 Nick Clifton <nickc@redhat.com> - 2.23.51.0.8-1
- Rebase on 2.23.51.0.8 release.  (#890382)

* Fri Dec 21 2012 Nick Clifton <nickc@redhat.com> - 2.23.51.0.7-1
- Rebase on 2.23.51.0.7 release.  (#889432)

* Tue Nov 27 2012 Nick Clifton <nickc@redhat.com> - 2.23.51.0.6-1
- Rebase on 2.23.51.0.6 release.  (#880508)

* Tue Nov 13 2012 Nick Clifton <nickc@redhat.com> - 2.23.51.0.5-1
- Rebase on 2.23.51.0.5 release.  (#876141)
- Retire binutils-2.23.51.0.3-arm-ldralt.patch

* Tue Oct 23 2012 Nick Clifton <nickc@redhat.com> - 2.23.51.0.3-3
- Rename ARM LDRALT instruction to LDALT.  (#869025) PR/14575

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> - 2.23.51.0.3-2
- Provides: bundled(libiberty)

* Tue Oct 02 2012 Nick Clifton <nickc@redhat.com> - 2.23.51.0.3-1
- Rebase on 2.23.51.0.3 release.  (#858560)

* Tue Sep 11 2012 Nick Clifton <nickc@redhat.com> - 2.23.51.0.2-1
- Rebase on 2.23.51.0.2 release.  (#856119)
- Retire binutils-2.23.51.0.1-gold-keep.patch and binutils-rh805974.patch.

* Tue Sep 4 2012 Jeff Law <law@redhat.com> 2.23.51.0.1-4
- Correctly handle PLTOFF relocs for s390 IFUNCs.

* Tue Aug 14 2012 Karsten Hopp <karsten@redhat.com> 2.23.51.0.1-3
- apply F17 commit cd2fda5 to honour {powerpc64} macro (#834651)

* Tue Aug 14 2012 Nick Clifton <nickc@redhat.com> - 2.23.51.0.1-2
- Make GOLD honour KEEP directives in linker scripts  (#8333355)

* Wed Aug 08 2012 Nick Clifton <nickc@redhat.com> - 2.23.51.0.1-1
- Rebase on 2.23.51.0.1 release.  (#846433)
- Retire binutils-2.22.52.0.4-dwz.patch, binutils-2.22.52.0.4-ar-4Gb.patch, binutils-2.22.52.0.4-arm-plt-refcount.patch, binutils-2.22.52.0.4-s390-64bit-archive.patch.

* Thu Aug 02 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.4-8
- Make the binutils-devel package depend upon the binutils package. (#845082)

* Thu Aug 02 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.4-7
- Disable checks that config.h is included before system headers.  (#845084)

* Tue Jul 17 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.4-6
- Use 64bit indicies in archives for s390 binaries.  (#835957)

* Thu Jul 05 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.4-5
- Catch attempts to create a broken symbol index with archives > 4Gb in size.  (#835957)

* Fri Jun 29 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.4-4
- Import fix for ld/14189.  (#829311)

* Fri Jun 29 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.4-3
- Fix handling of archives > 4Gb in size by importing patch for PR binutils/14302.  (#835957)

* Tue Jun 19 2012 Jakub Jelinek <jakub@redhat.com> - 2.22.52.0.4-2
- Add minimal dwz -m support.

* Wed Jun 06 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.4-1
- Rebase on 2.22.52.0.4 release.  (#829027)

* Tue May 08 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.3-1
- Rebase on 2.22.52.0.3 release.  (#819823)

* Mon Apr 30 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.2-1
- Rebase on 2.22.52.0.2 release.  (#816514)
- Retire binutils-2.22.52.0.1-weakdef.patch, binutils-2.22.52.0.1-ld-13621.patch, binutils-rh797752.patch, binutils-2.22.52.0.1-x86_64-hidden-ifunc.patch, binutils-2.22.52.0.1-tsx.patch and binutils-2.22.52.0.1-hidden-ifunc.patch.
- Update binutils-2.22.52.0.1-reloc-on-by-default.patch.

* Fri Apr 27 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.1-12
- Include demangle.h in the devel rpm.

* Tue Apr 03 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.1-11
- Enable -zrelro by default for RHEL 7+. (#807831)

* Fri Mar 16 2012 Jakub Jelinek <jakub@redhat.com> - 2.22.52.0.1-10
- Fix up handling of hidden ifunc relocs on i?86

* Wed Mar 14 2012 Jeff Law <law@redhat.com> - 2.22.52.0.1-9
- Fix c++filt docs (2nd instance) (#797752)

* Wed Mar 07 2012 Jakub Jelinek <jakub@redhat.com> - 2.22.52.0.1-8
- Fix up handling of hidden ifunc relocs on x86_64
- Add Intel TSX support

* Tue Mar 06 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.1-7
- Enable -zrelro by default. (#621983 #807831)

* Mon Feb 27 2012 Jeff Law <law@redhat.com> - 2.22.52.0.1-6
- Fix c++filt docs (#797752)

* Wed Feb 15 2012 Mark Wielaard <mjw@redhat.com> - 2.22.52.0.1-5
- Add upstream ld/13621 'dangling global hidden symbol in symtab' patch.

* Wed Feb 08 2012 Adam Williamson <awilliam@redhat.com> - 2.22.52.0.1-4
- Actually apply the patch

* Wed Feb 08 2012 Adam Williamson <awilliam@redhat.com> - 2.22.52.0.1-3
- Add upstream weakdef.patch to fix RH #788107

* Wed Feb 01 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.1-2
- Drat - forgot to upload the new tarball.  Now done.

* Wed Feb 01 2012 Nick Clifton <nickc@redhat.com> - 2.22.52.0.1-1
- Rebase on 2.22.52 release.
- Remove build-id.patch and gold-casts.patch as they are included in the 2.22.52 sources.

* Fri Jan 13 2012 Nick Clifton <nickc@redhat.com> - 2.22-4
- Fix bug in GOLD sources parsing signed integers in command line options. 

* Fri Jan 13 2012 Nick Clifton <nickc@redhat.com> - 2.22-3
- Add casts for building gold with 4.7 version of gcc.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  22 2011 Nick Clifton <nickc@redhat.com> - 2.22-1
- Rebase on 2.22 release.

* Fri Sep  30 2011 Ricky Zhou <ricky@fedoraproject.org> - 2.21.53.0.2-2
- Rebuild libopcodes.a with -fPIC.

* Tue Aug  09 2011 Nick Clifton <nickc@redhat.com> - 2.21.53.0.2-1
- Rebase on 2.21.53.0.2 tarball.  Delete unneeded patches.  (BZ 728677)

* Tue Aug  02 2011 Nick Clifton <nickc@redhat.com> - 2.21.53.0.1-3
- Update libiberty demangling.  (BZ 727453)

* Wed Jul  27 2011 Nick Clifton <nickc@redhat.com> - 2.21.53.0.1-2
- Import Jakub Jelinek's patch to add support for displaying the contents of .debug_macro sections.

* Tue Jul  19 2011 Nick Clifton <nickc@redhat.com> - 2.21.53.0.1-1
- Rebase on 2.21.53.0.1 tarball.  Delete unneeded patches.  (BZ 712668)

* Fri Jun  24 2011 Nick Clifton <nickc@redhat.com> - 2.21.52.0.1-5
- Import fix for PR ld/12921.

* Fri Jun  24 2011 Nick Clifton <nickc@redhat.com> - 2.21.52.0.1-4
- Run "alternatives --auto" to restore ld symbolic link if it was manually configured.  (BZ 661247)

* Thu Jun  16 2011 Nick Clifton <nickc@redhat.com> - 2.21.52.0.1-3
- Fix seg-fault attempting to find a function name without a symbol table.  (BZ 713471)

* Fri Jun  10 2011 Nick Clifton <nickc@redhat.com> - 2.21.52.0.1-2
- Import fix for PR ld/12851 (BZ 711268)

* Thu Jun  09 2011 Nick Clifton <nickc@redhat.com> - 2.21.52.0.1-1
- Rebase on 2.21.52.0.1 tarball.  (BZ 712025)

* Tue May  17 2011 Nick Clifton <nickc@redhat.com> - 2.21.51.0.9-1
- Rebase on 2.21.51.0.9 tarball.  (BZ 703105)

* Mon May   2 2011 Peter Robinson <pbrobinson@gmail.com> - 2.21.51.0.8-3
- Add ARM to BFD checks

* Mon Apr  11 2011 Nick Clifton <nickc@redhat.com> - 2.21.51.0.8-2
- Delete plugins patch - enable plugins via configure option.

* Mon Apr  11 2011 Nick Clifton <nickc@redhat.com> - 2.21.51.0.8-1
- Rebase on 2.21.51.0.8 tarball.

* Thu Mar  17 2011 Nick Clifton <nickc@redhat.com> - 2.21.51.0.7-1
- Rebase on 2.21.51.0.7 tarball.

* Tue Mar  08 2011 Nick Clifton <nickc@redhat.com> - 2.21.51.0.6-2
- Enable gold plugins.  (BZ 682852)

* Thu Feb  10 2011 Nick Clifton <nickc@redhat.com> - 2.21.51.0.6-1
- Rebase on 2.21.51.0.6 tarball.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.21.51.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan  28 2011 Jakub Jelinek <jakub@redhat.com> - 2.21.51.0.5-3
- Readd --build-id fix patch.  (PR ld/12451)

* Thu Jan   6 2011 Dan Horák <dan[at]danny.cz> - 2.21.51.0.5-2
- fix build on non-gold arches like s390(x) where both ld and ld.bfd is installed

* Wed Jan   5 2011 Nick Clifton <nickc@redhat.com> - 2.21.51.0.5-1
- Rebase on 2.21.51.0.5 tarball.
- Delete redundant patches.
- Fix gold+ld configure command line option.

* Fri Nov   5 2010 Dan Horák <dan[at]danny.cz> - 2.20.51.0.12-2
- "no" is not valid option for --enable-gold

* Thu Oct  28 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.12-1
- Rebase on 2.20.51.0.12 tarball.  (BZ 582160)

* Fri Sep  10 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.11-1
- Rebase on 2.20.51.0.11 tarball.  (BZ 631771)

* Fri Aug  20 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.10-3
- Allow ^ and ! characters in linker script wildcard patterns.  (BZ 621742)

* Fri Aug  20 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.10-2
- Fix seg fault in sec_merge_emit().  (BZ 623687)

* Tue Aug  10 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.10-1
- Rebase on 2.20.51.0.10 tarball.
- Import GOLD sources from binutils mainline as of 10 Aug 2010. 

* Wed Jun  30 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.7-5
- Rename the binutils-static package to binutils-devel in line with the Fedora packaging guidelines.

* Wed Jun   9 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.7-4
- Allow GOLD linker to parse "-l<name>" directives inside INPUT statements in linker scripts. (BZ 600553)

* Tue May   4 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.7-3
- Allow unique symbols in archive maps.

* Tue Apr  20 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.7-2
- Merge binutils-devel package into binutils-static package.  (BZ 576300)

* Thu Apr   8 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.7-1
- Rebase on 2.20.51.0.7 tarball.
- Delete redundant patches:
  binutils-2.20.51.0.2-add-needed.patch,
  binutils-2.20.51.0.2-do-not-set-ifunc.patch,
  binutils-2.20.51.0.2-enable-gold.patch,
  binutils-2.20.51.0.2-gas-expr.patch,
  binutils-2.20.51.0.2-ifunc-ld-s.patch,
  binutils-2.20.51.0.2-lwp.patch,
  binutils-2.20.51.0.2-ppc-hidden-plt-relocs.patch,
  binutils-2.20.51.0.2-x86-hash-table.patch,
- Do not allow unique symbols to be bound locally.  (PR ld/11434)
- Add support for DWARF4 debug information.

* Thu Mar   4 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-17
- Do not set ELFOSABI_LINUX on binaries which just link to IFUNC using DSOs.  (BZ 568941)

* Tue Mar   2 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-16
- Copy the OSABI field in ELF headers, if set.  (BZ 568921)

* Fri Feb  12 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-15
- Create separate static and devel sub-packages.  (BZ 556040)

* Tue Feb   2 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-14
- Fix seg-fault when linking mixed x86 and x86_64 binaries.  (BZ 487472)

* Fri Jan  22 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-13
- Add a requirement for the coreutils.  (BZ 557006)

* Wed Jan  20 2010 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-12
- Fix --no-copy-dt-needed so that it will not complain about weak references.

* Fri Dec  18 2009 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-11
- Add missing part of PR 11088 patch.

* Thu Dec  17 2009 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-10
- Apply patch for PR 11088.  (BZ 544149)

* Wed Dec  9 2009 Nick Clifton <nickc@redhat.com> - 2.20.51.0.2-9
- Apply patch for PR 10856.  (BZ 544358)

* Tue Dec  1 2009 Roland McGrath <roland@redhat.com> - 2.20.51.0.2-8
- Build gold only for x86 flavors until others are tested.

* Tue Nov 24 2009 Roland McGrath <roland@redhat.com> - 2.20.51.0.2-7
- Add support for building gold.

* Mon Nov  9 2009 Jakub Jelinek <jakub@redhat.com> 2.20.51.0.2-5
- Fix up --copy-dt-needed-entries default.  (Nick Clifton)

* Mon Nov  9 2009 Jakub Jelinek <jakub@redhat.com> 2.20.51.0.2-4
- Fix ld -s with IRELATIVE relocations.  (BZ 533321, PR ld/10911)
- Add AMD Orochi LWP support, fix FMA4 support.

* Thu Nov 05 2009 Nick CLifton <nickc@redhat.com> 2.20.51.0.2-3
- Rename --add-needed to --copy-dt-needed-entries and improve error message about unresolved symbols in DT_NEEDED DSOs.

* Tue Oct 27 2009 Jan Kratochvil <jan.kratochvil@redhat.com> 2.20.51.0.2-2
- Fix rpm --excludedocs (BZ 515922).
- Fix spurious scriplet errors by `exit 0'. (BZ 517979, Nick Clifton)

* Mon Oct 12 2009 Nick Clifton <nickc@redhat.com> 2.20.51.0.2-1
- Rebase on 2.20 tarball.
- Remove redundant moxie patch.
- Remove redundant unique is global patch.
- Remove redundant cxxfilt java doc patch.

* Tue Sep 29 2009 Jan Kratochvil <jan.kratochvil@redhat.com> 2.19.51.0.14-32
- Remove spurious description of nonexistent --java switch for cxxfilt.

* Thu Aug  6 2009 Jakub Jelinek <jakub@redhat.com> 2.19.51.0.14-31
- Fix strip on objects with STB_GNU_UNIQUE symbols. (BZ 515700, PR binutils/10492)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.51.0.14-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.11-28
- Rebase sources on 2.19.51.0.14 tarball.  Gain fixes for PRs 10429 and 10433.

* Wed Jul 22 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.11-28
- Rebase sources on 2.19.51.0.13 tarball.  Remove redundant orphan section placement patch. (BZ 512937)

* Tue Jul 14 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.11-27
- Add patch to allow moxie target to build, and hence --enable-targets=all to work.

* Tue Jul 14 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.11-26
- Import orphan section placement patch from mainline.  (BZ 510384)

* Tue Jul 14 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.11-25
- Fix build-id patch to avoid memory corruption.  (BZ 501582)

* Sat Jul 11 2009 Jan Kratochvil <jan.kratochvil@redhat.com> 2.19.51.0.11-24
- Provide uuencode output of the testsuite results.

* Tue Jun 30 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.11-23
- Rebase sources on the 2.19.51.0.11 tarball.

* Mon Jun 22 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.10-22
- Rebase sources on the 2.19.51.0.10 tarball.

* Thu Jun 11 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.2-21
- Do not attempt to set execute permission on non-regular files.  (BZ 503426)

* Tue Jun  9 2009 Jakub Jelinek <jakub@redhat.com> 2.19.51.0.2-20
- Fix .cfi_* skip over >= 64KB of code.  (PR gas/10255)

* Wed May 27 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.2-19
- Import fix for binutils PR #9938.  (BZ 500295)

* Wed Apr 15 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.2-18
- Update IBM Power 7 support patch to fix tlbilx opcode.  (BZ 494718)

* Tue Mar 17 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.2-17
- Add glibc-static to BuildRequires when running the testsuite.

* Thu Mar 05 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.2-16
- Add IBM Power7 support.  (BZ 487887)

* Mon Mar 02 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.2-15
- Add IFUNC support.  (BZ 465302)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.19.51.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Jan Kratochvil <jan.kratochvil@redhat.com> 2.19.50.0.2-13
- Rediff the symbolic-envvar-revert patch to comply with rpm patch --fuzz=0.

* Thu Feb  5 2009 Nick Clifton <nickc@redhat.com> 2.19.51.0.2-12
- Rebase sources on 2.19.51.0.2 tarball.  Remove linkonce-r-discard and
  gcc-expect-table patches.

* Mon Feb  2 2009 Jan Kratochvil <jan.kratochvil@redhat.com> 2.19.50.0.1-11
- Fix .eh_frame_hdr build also for .gcc_except_table LSDA refs (BZ 461675).

* Fri Jan 23 2009 Nick Clifton <nickc@redhat.com> 2.19.50.0.1-10
- Only require dejagnu if the testsuites are going to be run.  (BZ 481169)

* Sat Nov 29 2008 Nick Clifton <nickc@redhat.com> 2.19.50.0.1-8
- Add build-id patch to ensure that section contents are incorporated
  into a build id.  (BZ 472152)

* Fri Nov 21 2008 Nick Clifton <nickc@redhat.com> 2.19.50.0.1
- Rebase sources on 2.19.50.0.1 tarball.  Update all patches, trimming
  those that are no longer needed.

* Thu Oct 30 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.9-7
- Fix %%{_prefix}/include/bfd.h on 32-bit hosts due the 64-bit BFD target
  support from 2.18.50.0.8-2 (BZ 468495).

* Thu Oct 30 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.9-6
- binutils-devel now requires zlib-devel (BZ 463101 comment 5).
- Fix complains on .gnu.linkonce.r relocations to their discarded
  .gnu.linkonce.t counterparts.

* Mon Sep 22 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.9-5
- Remove %%makeinstall to comply with the spu-binutils review (BZ 452211).

* Mon Sep 22 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.9-4
- Fix *.so scripts for multilib linking (BZ 463101, suggested by Jakub Jelinek).

* Sun Sep 21 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.9-3
- Provide libbfd.so and libopcodes.so for automatic dependencies (BZ 463101).
- Fix .eh_frame_hdr build on C++ files with discarded common groups (BZ 458950).
- Provide --build and --host to fix `rpmbuild --target' biarch builds.
- Include %%{binutils_target}- filename prefix for binaries for cross builds.
- Fix multilib conflict on %%{_prefix}/include/bfd.h's BFD_HOST_64BIT_LONG_LONG.

* Mon Sep 15 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.9-2
- Package review, analysed by Jon Ciesla and Patrice Dumas (BZ 225615).
 - build back in the sourcedir without problems as gasp is no longer included.
 - Fix the install-info requirement.
 - Drop the needless gzipping of the info files.
 - Provide Obsoletes versions.
 - Use the %%configure macro.

* Sat Aug 30 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.9-1
- Update to 2.18.50.0.9.
  - Drop the ppc-only spu target pre-build stage (BZ 455242).
  - Drop parsing elf64-i386 files for kdump PAE vmcore dumps (BZ 457189).
- New .spec BuildRequires zlib-devel (/-static) for compressed sections.
- Update .spec Buildroot to be more unique.

* Fri Aug  1 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.8-2
- Fix parsing elf64-i386 files for kdump PAE vmcore dumps (BZ 457189).
- Turn on 64-bit BFD support for i386, globally enable AC_SYS_LARGEFILE.
- `--with debug' builds now with --disable-shared.
- Removed a forgotten unused ld/eelf32_spu.c workaround from 2.18.50.0.8-1.

* Thu Jul 31 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.8-1
- Update to 2.18.50.0.8.
  - Drop the .clmul -> .pclmul renaming backport.
- Add %%{binutils_target} macro to support building cross-binutils.
  (David Woodhouse)
- Support `--without testsuite' to suppress the testsuite run.
- Support `--with debug' to build without optimizations.
- Refresh the patchset with fuzz 0 (for new rpmbuild).
- Enable the spu target on ppc/ppc64 (BZ 455242).

* Wed Jul 16 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.6-4
- include the `dist' tag in the Release number
- libbfd.a symbols visibility is now hidden (for #447426, suggested by Jakub)

* Wed Jul 16 2008 Jan Kratochvil <jan.kratochvil@redhat.com> 2.18.50.0.6-3
- rebuild libbfd.a with -fPIC for inclusion into shared libraries (#447426)

* Tue Apr  8 2008 Jakub Jelinek <jakub@redhat.com> 2.18.50.0.6-2
- backport .clmul -> .pclmul renaming

* Fri Apr  4 2008 Jakub Jelinek <jakub@redhat.com> 2.18.50.0.6-1
- update to 2.18.50.0.6
  - Intel AES, CLMUL, AVX/FMA support

* Mon Mar  3 2008 Jakub Jelinek <jakub@redhat.com> 2.18.50.0.4-2
- revert aranges optimization (Alan Modra, BZ#5303, BZ#5755)
- fix ld-shared testcase for GCC 4.3 (H.J. Lu)

* Fri Feb 29 2008 Jakub Jelinek <jakub@redhat.com> 2.18.50.0.4-1
- update to 2.18.50.0.4

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> 2.18.50.0.3-2
- Autorebuild for GCC 4.3

* Wed Dec 12 2007 Jakub Jelinek <jakub@redhat.com> 2.18.50.0.3-1
- update to 2.18.50.0.3
  - fix build with recent makeinfo (#415271)

* Thu Aug 16 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.18-1
- update to 2.17.50.0.18
  - GPLv3+
  - preserve .note.gnu.build-id in objcopy --only-keep-debug (#251935)
  - fix sparc64/alpha broken by --build-id patch (#252936)
- update License tag
- fix ld crash with --build-id and non-ELF output format (Alan Modra, BZ#4923)

* Tue Jul 31 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.17-7
- fix ppc32 secure PLT detection (Alan Modra)

* Wed Jul 25 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.17-6
- rebuilt to make sure even libbfd.so and libopcodes.so aren't
  broken by #249435

* Tue Jul 24 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.17-5
- add .note.gnu.build-id into default linker script (#249435)

* Tue Jul 24 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.17-4
- don't kill the %%{_gnu} part of target name on arm
  (Lennert Buytenhek, #243516)
- create just one PT_NOTE segment header for all consecutive SHT_NOTE
  sections

* Wed Jul 18 2007 Roland McGrath <roland@redhat.com> 2.17.50.0.17-3
- fix for ld --build-id

* Sun Jul 15 2007 Roland McGrath <roland@redhat.com> 2.17.50.0.17-2
- ld --build-id support

* Wed Jun 27 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.17-1
- update to 2.17.50.0.17

* Tue Jun 12 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.16-1
- update to 2.17.50.0.16

* Sat Apr 14 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.12-4
- fix linking non-ELF input objects into ELF output (#235747)

* Wed Mar 14 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.12-3
- don't require matching ELF_OSABI for target vecs with ELFOSABI_NONE,
  only prefer specific osabi target vecs over the generic ones
  (H.J.Lu, #230964, BZ#3826)
- build libbfd.so and libopcodes.so with -Bsymbolic-functions

* Fri Mar  2 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.12-2
- ignore install-info errors from scriptlets (#223678)

* Thu Mar  1 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.12-1
- update to 2.17.50.0.12
- revert the misdesigned LD_SYMBOLIC{,_FUNCTIONS} env var support,
  only support -Bsymbolic/-Bsymbolic-functions/--dynamic-list*

* Mon Jan  8 2007 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.9-1
- update to 2.17.50.0.9
- fix tekhex reader

* Sat Dec 23 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.8-2
- fix --as-needed on ppc64 (#219629)

* Sun Dec  3 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.8-1
- update to 2.17.50.0.8
- initialize frch_cfi_data (BZ#3607)

* Fri Dec  1 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.7-1
- update to 2.17.50.0.7
  - .cfi_personality and .cfi_lsda directives, per subsection .cfi_*
    directives, better .eh_frame CIE merging

* Thu Nov  9 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.6-3
- fix popcnt instruction assembly and disassembly on amd64 (#214767)

* Mon Oct 23 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.6-2
- update to 2.17.50.0.6
  - fix for section relative linker script defined symbols in
    empty sections (#207598, BZ#3267)
  - fix handling of DW_CFA_set_loc in .eh_frame optimizations
  - fix R_PPC_{PLT,GOT{,_TLSGD,_TLSLD,_TPREL,_DTPREL}}16_HA relocation
    handling with weak undefined symbols (Alan Modra, #211094)

* Tue Sep 12 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.3-6
- fix multilib conflict in %%{_prefix}/include/bfd.h

* Tue Sep 12 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.3-5
- fix efi-app-ia64 magic number (#206002, BZ#3171)

* Tue Sep  5 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.3-4
- link libopcodes*.so against libbfd*.so (#202327)
- split *.a and header files into binutils-devel

* Fri Aug 18 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.3-3
- on ppc and ppc64 increase default -z commonpagesize to 64K (#203001)

* Fri Jul 28 2006 Alexandre Oliva <aoliva@redhat.com> 2.17.50.0.3-2
- do not infer x86 arch implicitly based on instruction in the input
  (#200330)

* Mon Jul 17 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.3-1
- update to 2.17.50.0.3

* Fri Jul 14 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.2-8
- add support for new AMDFAM10 instructions (#198281, IT#97662)
- add -march=/-mtune= gas support on x86/x86-64
- x86/x86-64 nop insn improvements
- fix DT_GNU_HASH shift count value computation

* Tue Jul 11 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.2-7
- add DT_GNU_HASH support (--hash-style=gnu and --hash-style=both
  ld options)

* Thu Jun 29 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.2-4
- fix i?86 TLS GD->IE transition in executables (#196157, BZ#2513)

* Mon Jun 19 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.2-3
- fix two places in ld that misbehaved with MALLOC_PERTURB_=N
- fix .tls_common handling in relocatable linking

* Mon Jun  5 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.2-2
- fix --as-needed (Alan Modra, #193689, BZ#2721)

* Thu Jun  1 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.2-1
- update to 2.17.50.0.2
- update from CVS to 20060601
- speed up the ELF linker by caching the result of kept section check
  (H.J. Lu)

* Tue May  9 2006 Jakub Jelinek <jakub@redhat.com> 2.17.50.0.1-1
- update to 2.17.50.0.1

* Fri Mar 31 2006 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.6-6
- fix ld error message formatting, so that collect2 parser can
  parse it again for g++ -frepo (#187142)

* Thu Mar  9 2006 Alexandre Oliva <aoliva@redhat.com> 2.16.91.0.6-4
- fix relaxation of TLS GD to LE on PPC (#184590)

* Fri Mar  3 2006 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.6-3
- support DW_CFA_val_{offset,offset_sf,expression} in readelf/objdump

* Tue Feb 28 2006 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.6-2
- add MNI support on i?86/x86_64 (#183080)
- support S signal frame augmentation flag in .eh_frame,
  add .cfi_signal_frame support (#175951, PR other/26208, BZ#300)

* Tue Feb 14 2006 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.6-1
- update to 2.16.91.0.6
  - fix ppc64 --gc-sections
  - disassembler fixes for x86_64 cr/debug regs
  - fix linker search order for DT_NEEDED libs

* Mon Jan 02 2006 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.5-1
- update to 2.16.91.0.5
- don't error about .toc1 references to discarded sectiosn on ppc64
  (#175944)

* Wed Dec 14 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.3-2
- put .gnu.linkonce.d.rel.ro.* sections into relro region

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.3-1
- update to 2.16.91.0.3
- add .weakref support (Alexandre Oliva, #115157, #165728)

* Thu Aug 18 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.2-4
- install-info also configure.info
- update standards.texi from gnulib (#165530)

* Tue Aug 16 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.2-3
- update to 20050816 CVS
- better fix for ld-cdtest
- fix symbol version script parsing

* Fri Jul 29 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.2-2
- don't complain about relocs to discarded sections in ppc32
  .got2 sections (Alan Modra, PR target/17828)

* Fri Jul 22 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.2-1
- update to 2.16.91.0.2

* Thu Jul 21 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.1-3
- fix buffer overflow in readelf ia64 unwind printing code
- use vsnprintf rather than vsprintf in gas diagnostics (Tavis Ormandy)
- fix ld-cdtest when CFLAGS contains -fexceptions

* Wed Jul 20 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.1-2
- update to 20050720 CVS

* Mon Jul 11 2005 Jakub Jelinek <jakub@redhat.com> 2.16.91.0.1-1
- update to 2.16.91.0.1 plus 20050708 CVS

* Wed Jun 15 2005 Jakub Jelinek <jakub@redhat.com> 2.16.90.0.3-1
- update to 2.16.90.0.3
- update to 20050615 CVS
  - ppc32 secure PLT support (Alan Modra)
- further bfd/readelf robustification

* Sat Jun 11 2005 Jakub Jelinek <jakub@redhat.com> 2.15.94.0.2.2-4
- further bfd robustification (CAN-2005-1704, #158680)

* Fri Jun 10 2005 Jakub Jelinek <jakub@redhat.com> 2.15.94.0.2.2-3
- further objdump and readelf robustification (CAN-2005-1704, #158680)

* Wed May 25 2005 Jakub Jelinek <jakub@redhat.com> 2.15.94.0.2.2-2
- bfd and readelf robustification (CAN-2005-1704, #158680)

* Tue Mar 29 2005 Jakub Jelinek <jakub@redhat.com> 2.15.94.0.2.2-1
- update to 2.15.94.0.2.2
- speed up walk_wild_section (Robert O'Callahan)

* Mon Mar  7 2005 Jakub Jelinek <jakub@redhat.com> 2.15.94.0.2-4
- rebuilt with GCC 4

* Mon Feb 28 2005 Jakub Jelinek <jakub@redhat.com> 2.15.94.0.2-3
- fix buffer overflows in readelf (#149506)
- move c++filt to binutils from gcc-c++, conflict with gcc-c++ < 4.0 (#86333)

* Thu Feb 10 2005 Jakub Jelinek <jakub@redhat.com> 2.15.94.0.2-1
- update to 2.15.94.0.2
- fix .note.GNU-stack/PT_GNU_STACK computation in linker on ppc64 (#147296)
- fix stripping of binaries/libraries that have empty sections right before
  .dynamic section (with the same starting address; #144038)
- handle AS_NEEDED (...) in linker script INPUT/GROUP

* Tue Dec 14 2004 Jakub Jelinek <jakub@redhat.com> 2.15.92.0.2-11
- fix a longstanding -z relro bug

* Mon Dec 13 2004 Jakub Jelinek <jakub@redhat.com> 2.15.92.0.2-10
- avoid unnecessary gap with -z relro showing on i686 libc.so
- ppc64 --emit-relocs fix (Alan Modra)
- don't crash if STT_SECTION symbol has incorrect st_shndx (e.g. SHN_ABS,
  as created by nasm; #142181)
- don't try to make absptr LSDAs relative if they don't have relocations
  against them (Alan Modra, #141162)

* Wed Oct 27 2004 Jakub Jelinek <jakub@redhat.com> 2.15.92.0.2-5.EL4
- fix ar xo (#104344)

* Wed Oct 20 2004 Jakub Jelinek <jakub@redhat.com> 2.15.92.0.2-5
- fix --just-symbols on ppc64 (Alan Modra, #135498)

* Fri Oct 15 2004 Jakub Jelinek <jakub@redhat.com> 2.15.92.0.2-4
- fix code detecting matching linkonce and single member comdat
  group sections (#133078)

* Mon Oct 11 2004 Jakub Jelinek <jakub@redhat.com> 2.15.92.0.2-3
- revert Sep 09 change to make ppc L second argument e.g. for tlbie
  non-optional
- fix stripping of prelinked binaries and libraries (#133734)
- allow strings(1) on 32-bit arches to be used again with > 2GB
  files (#133555)

* Mon Oct  4 2004 Jakub Jelinek <jakub@redhat.com> 2.15.92.0.2-2
- update to 2.15.92.0.2
- change ld's ld.so.conf parser to match ldconfig's (#129340)

* Mon Sep 20 2004 Jakub Jelinek <jakub@redhat.com> 2.15.91.0.2-9
- avoid almost 1MB (sparse) gaps in the middle of -z relro
  libraries on x86-64 (Andreas Schwab)
- fix -z relro to make sure end of PT_GNU_RELRO segment is always
  COMMONPAGESIZE aligned

* Wed Aug 18 2004 Jakub Jelinek <jakub@redhat.com> 2.15.91.0.2-8
- fix linker segfaults on input objects with SHF_LINK_ORDER with
  incorrect sh_link (H.J.Lu, Nick Clifton, #130198, BZ #290)

* Wed Aug 18 2004 Jakub Jelinek <jakub@redhat.com> 2.15.91.0.2-7
- resolve all undefined ppc64 .* syms to the function bodies through
  .opd, not just those used in brach instructions (Alan Modra)

* Tue Aug 17 2004 Jakub Jelinek <jakub@redhat.com> 2.15.91.0.2-6
- fix ppc64 ld --dotsyms (Alan Modra)

* Tue Aug 17 2004 Jakub Jelinek <jakub@redhat.com> 2.15.91.0.2-5
- various ppc64 make check fixes when using non-dot-syms gcc (Alan Modra)
- fix --gc-sections
- on ia64 create empty .gnu.linkonce.ia64unw*.* sections for
  .gnu.linkonce.t.* function doesn't need unwind info

* Mon Aug 16 2004 Jakub Jelinek <jakub@redhat.com> 2.15.91.0.2-4
- kill ppc64 dot symbols (Alan Modra)
- objdump -d support for objects without dot symbols
- support for overlapping ppc64 .opd entries

* Mon Aug 9 2004 Jakub Jelinek <jakub@redhat.com> 2.15.91.0.2-3
- fix a newly introduced linker crash on x86-64

* Sun Aug 8 2004 Alan Cox <alan@redhat.com> 2.15.91.0.2-2
- BuildRequire bison and macroise buildroot - from Steve Grubb

* Fri Jul 30 2004 Jakub Jelinek <jakub@redhat.com> 2.15.91.0.2-1
- update to 2.15.91.0.2
- BuildRequire flex (#117763)

* Wed May 19 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.3-7
- use lib64 instead of lib directories on ia64 if %%{_lib} is
  set to lib64 by rpm

* Sat May 15 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.3-6
- fix a bug introduced in the ++/-- rejection patch
  from 2.15.90.0.3 (Alan Modra)

* Tue May  4 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.3-5
- fix s390{,x} .{,b,p2}align handling
- ppc/ppc64 testsuite fix

* Mon May  3 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.3-4
- -z relro ppc/ppc64/ia64 fixes
- change x86-64 .plt symbol st_size handling to match ia32
- prettify objdump -d output

* Tue Apr 20 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.3-3
- several SPARC fixes

* Sun Apr 18 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.3-2
- yet another fix for .tbss handling

* Fri Apr 16 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.3-1
- update to 2.15.90.0.3

* Fri Mar 26 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.1.1-2
- update to 20040326 CVS
  - fix ppc64 weak .opd symbol handling (Alan Modra, #119086)
- fix .tbss handling bug introduced

* Fri Mar 26 2004 Jakub Jelinek <jakub@redhat.com> 2.15.90.0.1.1-1
- update to 2.15.90.0.1.1

* Sat Feb 21 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.8-8
- with -z now without --enable-new-dtags create DT_BIND_NOW
  dynamic entry in addition to DT_FLAGS_1 with DF_1_NOW bit set

* Fri Feb 20 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.8-7
- fix -pie on ppc32

* Fri Feb 20 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.8-6
- clear .plt sh_entsize on sparc32
- put whole .got into relro area with -z now -z relro

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 22 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.8-4
- fix -pie on IA64

* Mon Jan 19 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.8-3
- fix testcases on s390 and s390x

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.8-2
- fix testcases on AMD64
- fix .got's sh_entsize on IA32/AMD64
- set COMMONPAGESIZE on s390/s390x
- set COMMONPAGESIZE on ppc32 (Alan Modra)

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.8-1
- update to 2.14.90.0.8

* Tue Jan 13 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.7-4
- fix -z relro on 64-bit arches

* Mon Jan 12 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.7-3
- fix some bugs in -z relro support

* Fri Jan  9 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.7-2
- -z relro support, reordering of RW sections

* Fri Jan  9 2004 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.7-1
- update to 2.14.90.0.7

* Mon Nov 24 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.6-4
- fix assembly parsing of foo=(.-bar)/4 (Alan Modra)
- fix IA-64 assembly parsing of (p7) hint @pause

* Tue Sep 30 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.6-3
- don't abort on some linker warnings/errors on IA-64

* Sat Sep 20 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.6-2
- fix up merge2.s to use .p2align instead of .align

* Sat Sep 20 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.6-1
- update to 2.14.90.0.6
- speed up string merging (Lars Knoll, Michael Matz, Alan Modra)
- speed up IA-64 local symbol handling during linking

* Fri Sep  5 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.5-7
- avoid ld -s segfaults introduced in 2.14.90.0.5-5 (Dmitry V. Levin,
  #103180)

* Fri Aug 29 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.5-6
- build old demangler into libiberty.a (#102268)
- SPARC .cfi* support

* Tue Aug  5 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.5-5
- fix orphan section placement

* Tue Jul 29 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.5-4
- fix ppc64 elfvsb linker tests
- some more 64-bit cleanliness fixes, give ppc64 fdesc symbols
  type and size (Alan Modra)

* Tue Jul 29 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.5-3
- fix 64-bit unclean code in ppc-opc.c

* Mon Jul 28 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.5-2
- fix 64-bit unclean code in tc-ppc.c

* Mon Jul 28 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.5-1
- update to 2.14.90.0.5
- fix ld -r on ppc64 (Alan Modra)

* Fri Jul 18 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-23
- rebuilt

* Thu Jul 17 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-22
- fix elfNN_ia64_dynamic_symbol_p (Richard Henderson, #86661)
- don't access memory beyond what was allocated in readelf
  (Richard Henderson)

* Thu Jul 10 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-21
- add .cfi_* support on ppc{,64} and s390{,x}

* Tue Jul  8 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-20
- remove lib{bfd,opcodes}.la (#98190)

* Mon Jul  7 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-19
- fix -pie support on amd64, s390, s390x and ppc64
- issue relocation overflow errors for s390/s390x -fpic code when
  accessing .got slots above 4096 bytes from .got start

* Thu Jul  3 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-18
- rebuilt

* Thu Jul  3 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-17
- fix ia64 -pie support
- require no undefined non-weak symbols in PIEs like required for normal
  binaries

* Wed Jul  2 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-16
- fix readelf -d on IA-64
- build libiberty.a with -fPIC, so that it can be lined into shared
  libraries

* Wed Jun 25 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-15
- rebuilt

* Wed Jun 25 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-14
- added support for Intel Prescott instructions
- fix hint@pause for ia64
- add workaround for LTP sillyness (#97934)

* Wed Jun 18 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-13
- update CFI stuff to 2003-06-18
- make sure .eh_frame is aligned to 8 bytes on 64-bit arches,
  remove padding within one .eh_frame section

* Tue Jun 17 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-12
- rebuilt

* Tue Jun 17 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-11
- one more fix for the same patch

* Tue Jun 17 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-10
- fix previous patch

* Mon Jun 16 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-9
- ensure R_PPC64_{RELATIVE,ADDR64} have *r_offset == r_addend
  and the other relocs have *r_offset == 0

* Tue Jun 10 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-8
- remove some unnecessary provides in ppc64 linker script
  which were causing e.g. empty .ctors/.dtors section creation

* Fri Jun  6 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-7
- some CFI updates/fixes
- don't create dynamic relocations against symbols defined in PIE
  exported from its .dynsym

* Wed Jun  4 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-6
- update gas to 20030604
- PT_GNU_STACK support

* Mon Jun  2 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-5
- buildrequire gettext (#91838)

* Sat May 31 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-4
- fix shared libraries with >= 8192 .plt slots on ppc32

* Thu May 29 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-3
- rebuilt

* Thu May 29 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-2
- rename ld --dynamic option to --pic-executable or --pie
- fix ld --help output
- document --pie/--pic-executable in ld.info and ld.1

* Wed May 28 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.4-1
- update to 2.14.90.0.4-1
- gas CFI updates (Richard Henderson)
- dynamic executables (Ulrich Drepper)

* Tue May 20 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.2-2
- fix ELF visibility handling
- tidy plt entries on IA-32, ppc and ppc64

* Mon May 19 2003 Jakub Jelinek <jakub@redhat.com> 2.14.90.0.2-1
- update to 2.14.90.0.2-1

* Tue May 13 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.20-8
- fix bfd_elf_hash on 64-bit arches (Andrew Haley)

* Wed Apr 30 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.20-7
- rebuilt

* Mon Apr 14 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.20-6
- optimize DW_CFA_advance_loc4 in gas even if there is 'z' augmentation
  with size 0 in FDE

* Fri Apr 11 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.20-5
- fix SPARC build

* Thu Apr  3 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.20-4
- fix ppc32 plt reference counting
- don't include %%{_prefix}/%%{_lib}/debug in the non-debuginfo package
  (#87729)

* Mon Mar 31 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.20-3
- make elf64ppc target native extra on ppc and elf32ppc native extra
  on ppc64.

* Fri Mar 28 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.20-2
- fix TLS on IA-64 with ld relaxation

* Sat Mar 22 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.20-1
- update to 2.13.90.0.20

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-9
- rebuilt

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-8
- don't strip binaries in %%install, so that there is non-empty
  debuginfo

* Mon Feb 24 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-7
- don't optimize .eh_frame during ld -r

* Thu Feb 13 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-6
- don't clear elf_link_hash_flags in the .symver patch
- only use TC_FORCE_RELOCATION in s390's TC_FORCE_RELOCATION_SUB_SAME
  (Alan Modra)

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-5
- fix the previous .symver change
- remove libbfd.so and libopcodes.so symlinks, so that other packages
  link statically, not dynamically against libbfd and libopcodes
  whose ABI is everything but stable

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-4
- do .symver x, x@FOO handling earlier
- support .file and .loc on s390*

* Mon Feb 10 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-3
- handle .symver x, x@FOO in ld such that relocs against x become
  dynamic relocations against x@FOO (#83325)
- two PPC64 TLS patches (Alan Modra)

* Sun Feb 09 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-2
- fix SEARCH_DIR on x86_64/s390x
- fix Alpha --relax
- create DT_RELA{,SZ,ENT} on s390 even if there is just .rela.plt
  and no .rela.dyn section
- support IA-32 on IA-64 (#83752)
- .eh_frame_hdr fix (Andreas Schwab)

* Thu Feb 06 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.18-1
- update to 2.13.90.0.18 + 20030121->20030206 CVS diff

* Tue Feb 04 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-8
- alpha TLS fixes
- use .debug_line directory table to make the section tiny bit smaller
- libtool fix from Jens Petersen

* Sun Feb 02 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-7
- sparc32 TLS

* Fri Jan 24 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-6
- s390{,x} TLS and two other mainframe patches

* Fri Jan 17 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-5
- fix IA-64 TLS IE in shared libs
- .{preinit,init,fini}_array compat hack from Alexandre Oliva

* Thu Jan 16 2003 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-4
- IA-64 TLS fixes
- fix .plt sh_entsize on Alpha
- build with %%_smp_mflags

* Sat Nov 30 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-3
- fix strip on TLS binaries and libraries

* Fri Nov 29 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-2
- fix IA-64 ld bootstrap

* Thu Nov 28 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.16-1
- update to 2.13.90.0.16
- STT_TLS SHN_UNDEF fix

* Wed Nov 27 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.10-4
- pad .rodata.cstNN sections at the end if they aren't sized to multiple
  of sh_entsize
- temporary patch to make .eh_frame and .gcc_except_table sections
  readonly if possible (should be removed when AUTO_PLACE is implemented)
- fix .PPC.EMB.apuinfo section flags

* Wed Oct 23 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.10-3
- fix names and content of alpha non-alloced .rela.* sections (#76583)
- delete unpackaged files from the buildroot

* Tue Oct 15 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.10-2
- enable s390x resp. s390 emulation in linker too

* Mon Oct 14 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.10-1
- update to 2.13.90.0.10
- add a bi-arch patch for sparc/s390/x86_64
- add --enable-64-bit-bfd on sparc, s390 and ppc

* Thu Oct 10 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.4-3
- fix combreloc testcase

* Thu Oct 10 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.4-2
- fix orphan .rel and .rela section placement with -z combreloc (Alan Modra)
- skip incompatible linker scripts when searching for libraries

* Tue Oct  1 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.4-1
- update to 2.13.90.0.4
- x86-64 TLS support
- some IA-32 TLS fixes
- some backported patches from trunk
- include opcodes, ld, gas and bfd l10n too

* Thu Sep 19 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.2-3
- allow addends for IA-32 TLS @tpoff, @ntpoff and @dtpoff
- clear memory at *r_offset of dynamic relocs on PPC
- avoid ld crash if accessing non-local symbols through LE relocs
- new IA-32 TLS relocs, bugfixes and testcases
- use brl insn on IA-64 (Richard Henderson)
- fix R_IA64_PCREL21{M,F} handling (Richard Henderson)
- build in separate builddir, so that gasp tests don't fail
- include localization

* Thu Aug  8 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.2-2
- fix R_386_TPOFF32 addends (#70824)

* Sat Aug  3 2002 Jakub Jelinek <jakub@redhat.com> 2.13.90.0.2-1
- update to 2.13.90.0.2
  - fix ld TLS assertion failure (#70084)
  - fix readelf --debug-dump= handling to match man page and --help
    (#68997)
- fix _GLOBAL_OFFSET_TABLE gas handling (#70241)

* Wed Jul 24 2002 Jakub Jelinek <jakub@redhat.com> 2.12.90.0.15-1
- update to 2.12.90.0.15
- TLS .tbss fix
- don't use rpm %%configure macro, it is broken too often (#69366)

* Thu May 30 2002 Jakub Jelinek <jakub@redhat.com> 2.12.90.0.9-1
- update to 2.12.90.0.9
  - TLS support
- remove gasp.info from %%post/%%preun (#65400)

* Mon Apr 29 2002 Jakub Jelinek <jakub@redhat.com> 2.12.90.0.7-1
- update to 2.12.90.0.7
- run make check

* Mon Apr 29 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-12
- fix .hidden handling on SPARC (Richard Henderson)
- don't crash when linking -shared non-pic code with SHF_MERGE
- fix .eh_frame_hdr for DW_EH_PE_aligned
- correctly adjust DW_EH_PE_pcrel encoded personalities in CIEs

* Fri Apr  5 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-11
- don't emit dynamic R_SPARC_DISP* relocs against STV_HIDDEN symbols
  into shared libraries

* Thu Mar 21 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-10
- don't merge IA-64 unwind info sections together during ld -r

* Mon Mar 11 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-9
- fix DATA_SEGMENT_ALIGN on ia64/alpha/sparc/sparc64

* Fri Mar  8 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-8
- don't crash on SHN_UNDEF local dynsyms (Andrew MacLeod)

* Thu Mar  7 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-7
- fix bfd configury bug (Alan Modra)

* Tue Mar  5 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-6
- don't copy visibility when equating symbols
- fix alpha .text/.data with .previous directive bug

* Tue Mar  5 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-5
- fix SHF_MERGE crash with --gc-sections (#60369)
- C++ symbol versioning patch

* Fri Feb 22 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-4
- add DW_EH_PE_absptr -> DW_EH_PE_pcrel optimization for shared libs,
  if DW_EH_PE_absptr cannot be converted that way, don't build the
  .eh_frame_hdr search table

* Fri Feb 15 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-3
- fix ld -N broken by last patch

* Tue Feb 12 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-2
- trade one saved runtime page for data segment (=almost always not shared)
  for up to one page of disk space where possible

* Fri Feb  8 2002 Jakub Jelinek <jakub@redhat.com> 2.11.93.0.2-1
- update to 2.11.93.0.2
- use %%{ix86} instead of i386 for -z combreloc default (#59086)

* Thu Jan 31 2002 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-10
- don't create SHN_UNDEF STB_WEAK symbols unless there are any relocations
  against them

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com> 2.11.92.0.12-9.1
- rebuild (fix ia64 miscompilation)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 28 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-8
- two further .eh_frame patch fixes

* Wed Dec 19 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-7
- as ld is currently not able to shrink input sections to zero size
  during discard_info, build a fake minimal CIE in that case
- update elf-strtab patch to what was commited

* Mon Dec 17 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-6
- one more .eh_frame patch fix
- fix alpha .eh_frame handling
- optimize elf-strtab finalize

* Sat Dec 15 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-5
- yet another fix for the .eh_frame patch

* Fri Dec 14 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-4
- Alan Modra's patch to avoid crash if there is no dynobj

* Thu Dec 13 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-3
- H.J.'s patch to avoid crash if input files are not ELF
- don't crash if a SHF_MERGE for some reason could not be merged
- fix objcopy/strip to preserve SHF_MERGE sh_entsize
- optimize .eh_frame sections, add PT_GNU_EH_FRAME support
- support anonymous version tags in version script

* Tue Nov 27 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-2
- fix IA-64 SHF_MERGE handling

* Tue Nov 27 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.12-1
- update to 2.11.92.0.12
  - optimize .dynstr and .shstrtab sections (#55524)
  - fix ld.1 glitch (#55459)
- turn relocs against SHF_MERGE local symbols with zero addend
  into STT_SECTION + addend
- remove man pages for programs not included (nlmconv, windres, dlltool;
  #55456, #55461)
- add BuildRequires for texinfo

* Thu Oct 25 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.7-2
- duh, fix strings on bfd objects (#55084)

* Sat Oct 20 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.7-1
- update to 2.11.92.0.7
- remove .rel{,a}.dyn from output if it is empty

* Thu Oct 11 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.5-2
- fix strings patch
- use getc_unlocked in strings to speed it up by 50% on large files

* Wed Oct 10 2001 Jakub Jelinek <jakub@redhat.com> 2.11.92.0.5-1
- update to 2.11.92.0.5
  - binutils localization (#45148)
  - fix typo in REPORT_BUGS_TO (#54325)
- support files bigger than 2GB in strings (#54406)

* Wed Sep 26 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-12
- on IA-64, don't mix R_IA64_IPLTLSB relocs with non-PLT relocs in
  .rela.dyn section.

* Tue Sep 25 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-11
- add iplt support for IA-64 (Richard Henderson)
- switch to new section flags for SHF_MERGE and SHF_STRINGS, put
  in compatibility code
- "s" section flag for small data sections on IA-64 and Alpha
  (Richard Henderson)
- fix sparc64 .plt[32768+] handling
- don't emit .rela.stab on sparc

* Mon Sep 10 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-10
- fix SHF_MERGE on Sparc

* Fri Aug 31 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-9
- on Alpha, copy *r_offset to R_ALPHA_RELATIVE's r_addend

* Thu Aug 30 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-8
- on IA-64, put crtend{,S}.o's .IA_64.unwind section last in
  .IA_64.unwind output section (for compatibility with 7.1 eh)

* Fri Aug 24 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-7
- put RELATIVE relocs first, not last
- enable -z combreloc by default on IA-{32,64}, Alpha, Sparc*

* Thu Aug 23 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-6
- support for -z combreloc
- remove .dynamic patch, -z combreloc patch does this better
- set STT_FUNC default symbol sizes in .endp directive on IA-64

* Mon Jul 16 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-5
- fix last patch (H.J.Lu)

* Fri Jul 13 2001 Jakub Jelinek <jakub@redhat.com> 2.11.90.0.8-4
- fix placing of orphan sections

* Sat Jun 23 2001 Jakub Jelinek <jakub@redhat.com>
- fix SHF_MERGE support on Alpha

* Fri Jun  8 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.8
  - some SHF_MERGE suport fixes
- don't build with tooldir /usrusr instead of /usr (#40937)
- reserve few .dynamic entries for prelinking

* Mon Apr 16 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.5
  - SHF_MERGE support

* Tue Apr  3 2001 Jakub Jelinek <jakub@redhat.com>
- 2.11.90.0.4
  - fix uleb128 support, so that CVS gcc bootstraps
  - some ia64 fixes

* Mon Mar 19 2001 Jakub Jelinek <jakub@redhat.com>
- add -Bgroup support from Ulrich Drepper

* Fri Mar  9 2001 Jakub Jelinek <jakub@redhat.com>
- hack - add elf_i386_glibc21 emulation

* Fri Feb 16 2001 Jakub Jelinek <jakub@redhat.com>
- 2.10.91.0.2

* Fri Feb  9 2001 Jakub Jelinek <jakub@redhat.com>
- 2.10.1.0.7
- remove ExcludeArch ia64
- back out the -oformat, -omagic and -output change for now

* Fri Dec 15 2000 Jakub Jelinek <jakub@redhat.com>
- Prereq /sbin/install-info

* Tue Nov 21 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.1.0.2

* Tue Nov 21 2000 Jakub Jelinek <jakub@redhat.com>
- add one more alpha patch

* Wed Nov 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix alpha visibility as problem
- add support for Ultra-III

* Fri Sep 15 2000 Jakub Jelinek <jakub@redhat.com>
- and one more alpha patch

* Fri Sep 15 2000 Jakub Jelinek <jakub@redhat.com>
- two sparc patches

* Mon Jul 24 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.18

* Mon Jul 10 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.12

* Mon Jun 26 2000 Jakub Jelinek <jakub@redhat.com>
- 2.10.0.9

* Thu Jun 15 2000 Jakub Jelinek <jakub@redhat.com>
- fix ld -r

* Mon Jun  5 2000 Jakub Jelinek <jakub@redhat.com>
- 2.9.5.0.46
- use _mandir/_infodir/_lib

* Mon May  8 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.41

* Wed Apr 12 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.34

* Wed Mar 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.31

* Fri Feb 04 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- apply kingdon's patch from #5031

* Wed Jan 19 2000 Jeff Johnson <jbj@redhat.com>
- Permit package to be built with a prefix other than /usr.

* Thu Jan 13 2000 Cristian Gafton <gafton@redhat.com>
- add pacth from hjl to fix the versioning problems in ld

* Tue Jan 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add sparc patches from Jakub Jelinek <jakub@redhat.com>
- Add URL:

* Tue Dec 14 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.22

* Wed Nov 24 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.19

* Sun Oct 24 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- 2.9.5.0.16

* Mon Sep 06 1999 Jakub Jelinek <jj@ultra.linux.cz>
- make shared non-pic libraries work on sparc with glibc 2.1.

* Fri Aug 27 1999 Jim Kingdon
- No source/spec changes, just rebuilding with egcs-1.1.2-18 because
  the older egcs was miscompling gprof.

* Mon Apr 26 1999 Cristian Gafton <gafton@redhat.com>
- back out very *stupid* sparc patch done by HJLu. People, keep out of
  things you don't understand.
- add alpha relax patch from rth

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- version  2.9.1.0.23
- patch to make texinfo documentation compile
- auto rebuild in the new build environment (release 2)

* Tue Feb 23 1999 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.21
- merged with UltraPenguin

* Mon Jan 04 1999 Cristian Gafton <gafton@redhat.com>
- added ARM patch from philb
- version 2.9.1.0.19a
- added a patch to allow arm* arch to be identified as an ARM

* Thu Oct 01 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.14.

* Sat Sep 19 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.13.

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.1.0.12

* Thu Jul  2 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.7.

* Wed Jun 03 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.6.

* Tue Jun 02 1998 Erik Troan <ewt@redhat.com>
- added patch from rth to get right offsets for sections in relocateable
  objects on sparc32

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue May 05 1998 Cristian Gafton <gafton@redhat.com>
- version 2.9.1.0.4 is out; even more, it is public !

* Tue May 05 1998 Jeff Johnson <jbj@redhat.com>
- updated to 2.9.1.0.3.

* Mon Apr 20 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.9.0.3

* Tue Apr 14 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.9.0.2

* Sun Apr 05 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.8.1.0.29 (HJ warned me that this thing is a moving target...
  :-)
- "fixed" the damn make install command so that all tools get installed

* Thu Apr 02 1998 Cristian Gafton <gafton@redhat.com>
- upgraded again to 2.8.1.0.28 (at least on alpha now egcs will compile)
- added info packages handling

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.8.1.0.23

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.8.1.0.15 (required to compile the newer glibc)
- all patches are obsoleted now

* Wed Oct 22 1997 Erik Troan <ewt@redhat.com>
- added 2.8.1.0.1 patch from hj
- added patch for alpha palcode form rth
