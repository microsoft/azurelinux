# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global cross cross
%global rpmprefix %{nil}

%global build_all		1
%global build_aarch64		%{build_all}
%global build_alpha		%{build_all}
%global build_arc		%{build_all}
%global build_arm		%{build_all}
%global build_avr32		%{build_all}
%global build_blackfin		%{build_all}
%global build_bpf		%{build_all}
%global build_c6x		%{build_all}
%global build_cris		%{build_all}
%global build_frv		%{build_all}
%global build_h8300		%{build_all}
%global build_hppa		%{build_all}
%global build_hppa64		%{build_all}
%global build_ia64		%{build_all}
%global build_loongarch64	%{build_all}
%global build_m32r		%{build_all}
%global build_m68k		%{build_all}
%global build_metag		%{build_all}
%global build_microblaze	%{build_all}
%global build_mips64		%{build_all}
%global build_mn10300		%{build_all}
%global build_openrisc		%{build_all}
%global build_powerpc64		%{build_all}
%global build_powerpc64le	%{build_all}
%global build_riscv32		%{build_all}
%global build_riscv64		%{build_all}
%global build_s390x		%{build_all}
%global build_score		%{build_all}
%global build_sh		%{build_all}
%global build_sparc64		%{build_all}
%global build_tile		%{build_all}
%global build_x86_64		%{build_all}
%global build_xtensa		%{build_all}

# 32-bit packages we don't build as we can use the 64-bit package instead
%global build_i386		0
%global build_mips		0
%global build_powerpc		0
%global build_s390		0
%global build_sparc		0
%global build_sh4		0

# not available in binutils-2.27
%global build_hexagon		0
%global build_unicore32		0

# Do not create deterministic archives by default  (cf: BZ 1195883)
%global enable_deterministic_archives 0

# Disable the default generation of compressed debug sections.
%define default_compress_debug 0

# Default to read-only-relocations (relro) in shared binaries.
%define default_relro 1

# Disable the default generation of GNU Build notes by the assembler.
# This has turned out to be problematic for the i686 architecture.
# although the exact reason has not been determined.  (See BZ 1572485)
# It also breaks building EFI binaries on AArch64, as these cannot have
# relocations against absolute symbols.
%define default_generate_notes 0

Name: %{cross}-binutils
Version: 2.45
Release: 2%{?dist}
Summary: A GNU collection of cross-compilation binary utilities
License: GPL-3.0-or-later AND (GPL-3.0-or-later WITH Bison-exception-2.2) AND (LGPL-2.0-or-later WITH GCC-exception-2.0) AND BSD-3-Clause AND GFDL-1.3-or-later AND GPL-2.0-or-later AND LGPL-2.1-or-later AND LGPL-2.0-or-later
URL: https://sourceware.org/binutils

# Note - the Linux Kernel binutils releases are too unstable and contain too
# many controversial patches so we stick with the official FSF version
# instead.

Source: http://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.xz

Source2: binutils-2.19.50.0.1-output-format.sed

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

# Purpose:  Allow the binutils to be configured with any (recent) version of
#            autoconf.
# Lifetime: Fixed in 2.44 (maybe ?)
Patch11: binutils-autoconf-version.patch

# Purpose:  Stop libtool from inserting useless runpaths into binaries.
# Lifetime: Who knows.
Patch12: binutils-libtool-no-rpath.patch

# Purpose:  Fix binutils testsuite failures.
# Lifetime: Permanent, but varies with each rebase.
Patch14: binutils-testsuite-fixes.patch

# Purpose:  Fix binutils testsuite failures for the RISCV-64 target.
# Lifetime: Permanent, but varies with each rebase.
Patch15: binutils-riscv-testsuite-fixes.patch

# Purpose:  Fix the ar test of non-deterministic archives.
# Lifetime: Fixed in 2.44
Patch18: binutils-fix-ar-test.patch

# Purpose:  Fix a seg fault in the AArch64 linker when building u-boot.
# Lifetime: Fixed in 2.45
Patch19: binutils-aarch64-small-plt0.patch

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

BuildRequires: texinfo >= 4.0, gettext, flex, bison, zlib-devel
# BZ 920545: We need pod2man in order to build the manual pages.
BuildRequires: /usr/bin/pod2man
# Perl, sed and touch are all used in the %prep section of this spec file.
BuildRequires: gcc, gcc-c++, perl-interpreter, sed, coreutils
BuildRequires: findutils
BuildRequires: autoconf automake
BuildRequires: make
 
Provides: bundled(libiberty)

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

%package -n %{cross}-binutils-common
Summary: Cross-build binary utility documentation and translation files
BuildArch: noarch
%description -n %{cross}-binutils-common
Documentation, manual pages and translation files for cross-build binary image
generation, manipulation and query tools.

%global do_package() \
%if %2 \
%package -n %{rpmprefix}binutils-%1 \
Summary: Cross-build binary utilities for %1 \
Requires: %{cross}-binutils-common == %{version}-%{release} \
%description -n %{rpmprefix}binutils-%1 \
Cross-build binary image generation, manipulation and query tools. \
%endif

%global do_symlink() \
%if %2 \
%package -n %{rpmprefix}binutils-%1 \
Summary: Cross-build binary utilities for %1 \
Requires: binutils-%3 == %{version}-%{release} \
%description -n %{rpmprefix}binutils-%1 \
Cross-build binary image generation, manipulation and query tools. \
%endif

%do_package aarch64-linux-gnu	%{build_aarch64}
%do_package alpha-linux-gnu	%{build_alpha}
%do_package arc-linux-gnu	%{build_arc}
%do_package arm-linux-gnu	%{build_arm}
%do_package avr32-linux-gnu	%{build_avr32}
%do_package bfin-linux-gnu	%{build_blackfin}
%do_package bpf-unknown-none	%{build_bpf}
%do_package c6x-linux-gnu	%{build_c6x}
%do_package cris-linux-gnu	%{build_cris}
%do_package frv-linux-gnu	%{build_frv}
%do_package h8300-linux-gnu	%{build_h8300}
%do_package hexagon-linux-gnu	%{build_hexagon}
%do_package hppa-linux-gnu	%{build_hppa}
%do_package hppa64-linux-gnu	%{build_hppa64}
%do_package i386-linux-gnu	%{build_i386}
%do_package ia64-linux-gnu	%{build_ia64}
%do_package loongarch64-linux-gnu %{build_loongarch64}
%do_package m32r-linux-gnu	%{build_m32r}
%do_package m68k-linux-gnu	%{build_m68k}
%do_package metag-linux-gnu	%{build_metag}
%do_package microblaze-linux-gnu %{build_microblaze}
%do_package mips-linux-gnu	%{build_mips}
%do_package mips64-linux-gnu	%{build_mips64}
%do_package mn10300-linux-gnu	%{build_mn10300}
%do_package openrisc-linux-gnu	%{build_openrisc}	or1k-linux-gnu
%do_package powerpc-linux-gnu	%{build_powerpc}
%do_package powerpc64-linux-gnu	%{build_powerpc64}
%do_package powerpc64le-linux-gnu %{build_powerpc64le}
%do_symlink ppc-linux-gnu	%{build_powerpc}	powerpc-linux-gnu
%do_symlink ppc64-linux-gnu	%{build_powerpc64}	powerpc64-linux-gnu
%do_symlink ppc64le-linux-gnu	%{build_powerpc64le}	powerpc64le-linux-gnu
%do_package riscv32-linux-gnu	%{build_riscv32}
%do_package riscv64-linux-gnu	%{build_riscv64}
%do_package s390-linux-gnu	%{build_s390}
%do_package s390x-linux-gnu	%{build_s390x}
%do_package score-linux-gnu	%{build_score}
%do_package sh-linux-gnu	%{build_sh}
%do_package sh4-linux-gnu	%{build_sh4}
%do_package sparc-linux-gnu	%{build_sparc}
%do_package sparc64-linux-gnu	%{build_sparc64}
%do_package tile-linux-gnu	%{build_tile}
%do_package unicore32-linux-gnu	%{build_unicore32}
%do_package x86_64-linux-gnu	%{build_x86_64}
%do_package xtensa-linux-gnu	%{build_xtensa}

# Where the binaries aimed at gcc will live (ie. /usr/<target>/bin/)
%global auxbin_prefix %{_exec_prefix}

###############################################################################
#
# Preparation
#
###############################################################################
%prep
%global srcdir binutils-%{version}
%setup -q -n %{srcdir} -c
cd %{srcdir}
%patch -P01 -p1
%patch -P02 -p1
%patch -P03 -p1
%patch -P04 -p1
%patch -P05 -p1
%patch -P06 -p1
%patch -P07 -p1
%patch -P11 -p1
%patch -P12 -p1
%patch -P14 -p1
%patch -P15 -p1
%patch -P18 -p1
%patch -P19 -p1
%patch -P99 -p1
%patch -P100 -p1
%patch -P101 -p1

# We cannot run autotools as there is an exact requirement of autoconf-2.59.

# On ppc64 and aarch64, we might use 64KiB pages
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*ppc.c
sed -i -e '/#define.*ELF_COMMONPAGESIZE/s/0x1000$/0x10000/' bfd/elf*aarch64.c
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
sed -i -e 's/^ PACKAGE=/ PACKAGE=%{cross}-/' */configure
# Undo the name change to run the testsuite.
for tool in binutils gas ld
do
  sed -i -e "2aDEJATOOL = $tool" $tool/Makefile.am
  sed -i -e "s/^DEJATOOL = .*/DEJATOOL = $tool/" $tool/Makefile.in
done
touch */configure

function prep_target () {
    target=$1
    cond=$2

    if [ $cond != 0 ]
    then
	echo $1 >&5
    fi
}

cd ..
(
    prep_target aarch64-linux-gnu	%{build_aarch64}
    prep_target alpha-linux-gnu		%{build_alpha}
    prep_target arc-linux-gnu		%{build_arc}
    prep_target arm-linux-gnu		%{build_arm}
    prep_target avr32-linux-gnu		%{build_avr32}
    prep_target bfin-linux-gnu		%{build_blackfin}
    prep_target bpf-unknown-none	%{build_bpf}
    prep_target c6x-linux-gnu		%{build_c6x}
    prep_target cris-linux-gnu		%{build_cris}
    prep_target frv-linux-gnu		%{build_frv}
    prep_target h8300-linux-gnu		%{build_h8300}
    prep_target hexagon-linux-gnu	%{build_hexagon}
    prep_target hppa-linux-gnu		%{build_hppa}
    prep_target hppa64-linux-gnu	%{build_hppa64}
    prep_target i386-linux-gnu		%{build_i386}
    prep_target ia64-linux-gnu		%{build_ia64}
    prep_target loongarch64-linux-gnu	%{build_loongarch64}
    prep_target m32r-linux-gnu		%{build_m32r}
    prep_target m68k-linux-gnu		%{build_m68k}
    prep_target metag-linux-gnu		%{build_metag}
    prep_target microblaze-linux-gnu	%{build_microblaze}
    prep_target mips-linux-gnu		%{build_mips}
    prep_target mips64-linux-gnu	%{build_mips64}
    prep_target mn10300-linux-gnu	%{build_mn10300}
    prep_target openrisc-linux-gnu	%{build_openrisc}
    prep_target powerpc-linux-gnu	%{build_powerpc}
    prep_target powerpc64-linux-gnu	%{build_powerpc64}
    prep_target powerpc64le-linux-gnu	%{build_powerpc64le}
    prep_target riscv32-linux-gnu	%{build_riscv32}
    prep_target riscv64-linux-gnu	%{build_riscv64}
    prep_target s390-linux-gnu		%{build_s390}
    prep_target s390x-linux-gnu		%{build_s390x}
    prep_target score-linux-gnu		%{build_score}
    prep_target sh-linux-gnu		%{build_sh}
    prep_target sh4-linux-gnu		%{build_sh4}
    prep_target sparc-linux-gnu		%{build_sparc}
    prep_target sparc64-linux-gnu	%{build_sparc64}
    prep_target tile-linux-gnu		%{build_tile}
    prep_target unicore32-linux-gnu	%{build_unicore32}
    prep_target x86_64-linux-gnu	%{build_x86_64}
    prep_target xtensa-linux-gnu	%{build_xtensa}
) 5>target.list

n=0
for target in `cat target.list`
do
    n=1
    break
done
if [ $n = 0 ]
then
    echo "No targets selected" >&2
    exit 8
fi

###############################################################################
#
# Build
#
###############################################################################
%build

function config_target () {
    arch=$1
    prefix=$arch-
    build_dir=${1%%%%-*}

    case $arch in
	aarch64-*)	target=aarch64-linux-gnu;;
	arc-*)		target=arc-linux-gnu;;
	arm-*)		target=arm-linux-gnueabi;;
	avr32-*)	target=avr-linux;;
	bfin-*)		target=bfin-uclinux;;
	bpf-*)		target=bpf-unknown-none;;
	c6x-*)		target=c6x-uclinux;;
	h8300-*)	target=h8300-elf;;
	m32r-*)		target=m32r-elf;;
	mn10300-*)	target=am33_2.0-linux;;
	m68knommu-*)	target=m68k-linux;;
	openrisc-*)	target=or1k-linux-gnu;;
	parisc-*)	target=hppa-linux;;
	score-*)	target=score-elf;;
	tile-*)		target=tilegx-linux;;
	v850-*)		target=v850e-linux;;
	x86-*)		target=x86_64-linux;;
	*)		target=$arch;;
    esac

    echo $arch: target is $target
    export CFLAGS="$RPM_OPT_FLAGS -Wno-unused-const-variable -std=gnu11"
    CARGS=

    case $target in i?86*|sparc*|ppc*|s390*|sh*|arm*|aarch64*|riscv*)
	    CARGS="$CARGS --enable-64-bit-bfd"
	    ;;
    esac

    case $target in ia64*)
	    CARGS="$CARGS --enable-targets=i386-linux"
	    ;;
    esac

    case $target in ppc*|ppc64*)
	    CARGS="$CARGS --enable-targets=spu"
	    ;;
    esac

    case $target in ppc64-*)
	    CARGS="$CARGS --enable-targets=powerpc64le-linux"
	    ;;
    esac

    case $target in sh-*)
	    CARGS="$CARGS --enable-targets=sh-linux,sh4-linux"
	    # sh-elf is dropped for now as it makes for ambiguity in format recognition
	    ;;
    esac

    case $target in x86_64*|i?86*|arm*|aarch64*|riscv*)
	    CARGS="$CARGS --enable-targets=x86_64-pep"
	    ;;
    esac

%if %{default_relro}
  CARGS="$CARGS --enable-relro=yes"
%else
  CARGS="$CARGS --enable-relro=no"
%endif

    mkdir $build_dir
    cd $build_dir

    # We could optimize the cross builds size by --enable-shared but the produced
    # binaries may be less convenient in the embedded environment.
    echo LDFLAGS: $RPM_LD_FLAGS
    LDFLAGS="$RPM_LD_FLAGS " \
    ../%{srcdir}/configure \
	--disable-dependency-tracking \
	--disable-silent-rules \
	--enable-checking \
	--prefix=%{_prefix} \
	--exec-prefix=%{auxbin_prefix} \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir} \
	--sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--build=%{_target_platform} \
	--host=%{_target_platform} \
	--target=$target \
	--program-prefix=$prefix \
	--disable-shared \
	--disable-install_libbfd \
	--with-sysroot=%{_prefix}/$arch/sys-root \
%if %{enable_deterministic_archives}
	--enable-deterministic-archives \
%else    
	--enable-deterministic-archives=no \
%endif
%if %{default_compress_debug}
	--enable-compressed-debug-sections=all \
%else
	--enable-compressed-debug-sections=none \
%endif
%if %{default_generate_notes}
	--enable-generate-build-notes=yes \
%else
	--enable-generate-build-notes=no \
%endif
	--enable-lto \
	$CARGS \
	--enable-gprofng=no \
	--enable-plugins \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla/
    cd ..
}

for target in `cat target.list`
do
    config_target $target
done

function build_target () {
    build_dir=${1%%%%-*}
    %make_build -C $build_dir tooldir=%{_prefix} all
}

for target in `cat target.list`
do
    build_target $target
done

# for documentation purposes only
mkdir %{cross}-binutils
cd %{cross}-binutils
../%{srcdir}/configure \
    --disable-dependency-tracking \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --exec-prefix=%{auxbin_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir} \
    --sharedstatedir=%{_sharedstatedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --program-prefix=%{cross}- \
    --disable-shared \
    --enable-gprofng=no \
    --with-bugurl=http://bugzilla.redhat.com/bugzilla/
%make_build tooldir=%{_prefix} all
cd ..

###############################################################################
#
# Installation
#
###############################################################################
%install
function install_bin () {
    cpu=${1%%%%-*}
    build_dir=$cpu
    %make_install -C $build_dir DESTDIR=%{buildroot}

    # We want links for ppc and ppc64 also if we make powerpc or powerpc64
    case $cpu in
	powerpc*)
	    cd %{buildroot}/usr/bin
	    for i in $cpu-*
	    do
		ln -s $i ppc${i#powerpc}
	    done
	    cd -
	    cd %{buildroot}/usr/
	    for i in $cpu-*
	    do
		ln -s $i ppc${i#powerpc}
	    done
	    cd -
	    cd %{buildroot}/usr/share/man/man1
	    for i in $cpu-*
	    do
		ln -s $i ppc${i#powerpc}
	    done
	    cd -
	    ;;
    esac
}

for target in `cat target.list`
do
    echo "=== INSTALL target $target ==="
    mkdir -p %{buildroot}%{_prefix}/$target/sys-root
    install_bin $target

done

echo "=== INSTALL man targets ==="
make install-man1 -C %{cross}-binutils/binutils DESTDIR=%{buildroot}
make install-man1 -C %{cross}-binutils/gas DESTDIR=%{buildroot}
make install-man1 -C %{cross}-binutils/ld DESTDIR=%{buildroot}
make install-man1 -C %{cross}-binutils/gprof DESTDIR=%{buildroot}

echo "=== INSTALL po targets ==="
%make_install -C %{cross}-binutils/binutils/po DESTDIR=%{buildroot}
%make_install -C %{cross}-binutils/gas/po DESTDIR=%{buildroot}
%make_install -C %{cross}-binutils/ld/po DESTDIR=%{buildroot}
%make_install -C %{cross}-binutils/gprof/po DESTDIR=%{buildroot}
%make_install -C %{cross}-binutils/bfd/po DESTDIR=%{buildroot}
%make_install -C %{cross}-binutils/opcodes/po DESTDIR=%{buildroot}

# Add the additional symlink-only targets
grep ^powerpc target.list | sed -e s/powerpc/ppc/ >symlink-target.list
cat symlink-target.list >>target.list

# For cross-binutils we drop the documentation.
echo "=== REMOVE documentation ==="
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_infodir}/dir

echo "=== REMOVE libraries and scripts ==="
find %{buildroot} -type f -name "*.a" -delete
rm -rf %{buildroot}%{auxbin_prefix}/*/lib/ldscripts
rmdir %{buildroot}%{auxbin_prefix}/*/lib || :

echo "=== REMOVE include and dev files ==="
if [ -d %{buildroot}/usr/include ]; then
    find %{buildroot}/usr/include -type f -name "*.h" -delete
fi
rm -rf %{buildroot}/etc/gprofng.rc

echo "=== BUILD file lists ==="
function build_file_list () {
    arch=$1
    cpu=${arch%%%%-*}

    case $cpu in
	avr32)		target_cpu=avr;;
	bfin)		target_cpu=bfin;;
	h8300)		target_cpu=h8300;;
	mn10300)	target_cpu=am33_2.0;;
	openrisc)	target_cpu=or1k;;
	score)		target_cpu=score;;
	tile)		target_cpu=tilegx;;
	v850)		target_cpu=v850e;;
	*)		target_cpu=$cpu;;
    esac

    (
	echo %{_bindir}/$arch-[!l]\*
	echo %{_bindir}/$arch-ld\*
	echo %{_mandir}/man1/$arch-\*
	echo %{auxbin_prefix}/$target_cpu-\*
    ) >files.$arch
}

for target in `cat target.list`
do
    build_file_list $target
done

# All the installed manual pages and translation files for each program are the
# same, so symlink them to the core package
echo "=== CROSSLINK man pages ==="
cd %{buildroot}%{_mandir}/man1
for i in %{cross}-*.1*
do
    j=${i#%{cross}-}

    for k in *-$j
    do
	if [ $k != $i ]
	then
	    ln -sf $i $k
	fi
    done
done


# Add ld.bfd manual pages
find * -name "*ld.1*" -a ! -name "%{cross}-ld.1*" -print |
while read x
do
    y=`echo $x | sed -e s/ld[.]1/ld.bfd.1/`
    ln -s $x $y
done

cd -

# Find the language files which only exist in the common package
(
    %find_lang %{cross}-binutils
    %find_lang %{cross}-opcodes
    %find_lang %{cross}-bfd
    %find_lang %{cross}-gas
    %find_lang %{cross}-ld
    %find_lang %{cross}-gprof
    cat %{cross}-binutils.lang
    cat %{cross}-opcodes.lang
    cat %{cross}-bfd.lang
    cat %{cross}-gas.lang
    cat %{cross}-ld.lang
    cat %{cross}-gprof.lang
) >files.cross



###############################################################################
#
# Cleanup
#
###############################################################################
###############################################################################
#
# Filesets
#
###############################################################################
%files -n %{cross}-binutils-common -f files.cross
%license %{srcdir}/COPYING*
%doc %{srcdir}/README
%{_mandir}/man1/%{cross}-*

%global do_files() \
%if %2 \
%files -n %{rpmprefix}binutils-%1 -f files.%1 \
%endif

%do_files aarch64-linux-gnu	%{build_aarch64}
%do_files alpha-linux-gnu	%{build_alpha}
%do_files arc-linux-gnu		%{build_arc}
%do_files arm-linux-gnu		%{build_arm}
%do_files avr32-linux-gnu	%{build_avr32}
%do_files bfin-linux-gnu	%{build_blackfin}
%do_files bpf-unknown-none	%{build_bpf}
%do_files c6x-linux-gnu		%{build_c6x}
%do_files cris-linux-gnu	%{build_cris}
%do_files frv-linux-gnu		%{build_frv}
%do_files h8300-linux-gnu	%{build_h8300}
%do_files hexagon-linux-gnu	%{build_hexagon}
%do_files hppa-linux-gnu	%{build_hppa}
%do_files hppa64-linux-gnu	%{build_hppa64}
%do_files i386-linux-gnu	%{build_i386}
%do_files ia64-linux-gnu	%{build_ia64}
%do_files loongarch64-linux-gnu	%{build_loongarch64}
%do_files m32r-linux-gnu	%{build_m32r}
%do_files m68k-linux-gnu	%{build_m68k}
%do_files metag-linux-gnu	%{build_metag}
%do_files microblaze-linux-gnu	%{build_microblaze}
%do_files mips-linux-gnu	%{build_mips}
%do_files mips64-linux-gnu	%{build_mips64}
%do_files mn10300-linux-gnu	%{build_mn10300}
%do_files openrisc-linux-gnu	%{build_openrisc}
%do_files powerpc-linux-gnu	%{build_powerpc}
%do_files powerpc64-linux-gnu	%{build_powerpc64}
%do_files powerpc64le-linux-gnu	%{build_powerpc64le}
%do_files ppc-linux-gnu		%{build_powerpc}
%do_files ppc64-linux-gnu	%{build_powerpc64}
%do_files ppc64le-linux-gnu	%{build_powerpc64le}
%do_files riscv64-linux-gnu	%{build_riscv64}
%do_files riscv32-linux-gnu	%{build_riscv32}
%do_files s390-linux-gnu	%{build_s390}
%do_files s390x-linux-gnu	%{build_s390x}
%do_files score-linux-gnu	%{build_score}
%do_files sh-linux-gnu		%{build_sh}
%do_files sh4-linux-gnu		%{build_sh4}
%do_files sparc-linux-gnu	%{build_sparc}
%do_files sparc64-linux-gnu	%{build_sparc64}
%do_files tile-linux-gnu	%{build_tile}
%do_files unicore32-linux-gnu	%{build_unicore32}
%do_files x86_64-linux-gnu	%{build_x86_64}
%do_files xtensa-linux-gnu	%{build_xtensa}

%changelog
* Sun Sep 28 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 2.45-1
- Update to 2.45

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Mar 16 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 2.44-1
- Update to 2.44
- Drop NIOS2 support (removed upstream)

* Wed Feb 26 2025 Nick Clifton <nickc@redhat.com> - 2.43.1-5
- Fix seg fault in AArch64 linker when building u-boot.  (#2326190)

* Wed Feb 26 2025 Nick Clifton <nickc@redhat.com> - 2.43.1-4
- Add -std=gnu11 to CFLAGS to support the use of static_assert in the sources.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan 11 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 2.43.1-2
- Add support for riscv632 arch

* Tue Aug 20 2024 Jose E. Marchesi <jose.marchesi@oracle.com> - 2.43.1-1
- Update to binutils 2.43.1-1
- Add: binutils-fix-ar-test.patch
- Update: binutils-riscv-testsuite-fixes.patch
- Update: binutils-testsuite-fixes.patch
- Retire: binutils-special-sections-in-groups.patch
- Retire: binutils-gold-powerpc.patch
- Retire: binutils-handle-corrupt-version-info.patch
- Retire: binutils-execstack-error.patch
- Retire: binutils-BPF-reloc-4.patch
- Retire: binutils-x86-64-v3.patch
- Retire: binutils-big-merge.patch
- Retire: binutils-aarch64-urcbig-bti-programs.patch
- Retire: i686-AVX10.1-part-1.patch
- Retire: i686-AVX10.1-part-2.patch
- Retire: i686-AVX10.1-part-3.patch
- Retire: i686-AVX10.1-part-4.patch
- Retire: i686-AVX10.1-part-5.patch
- Retire: i686-AVX10.1-part-6.patch
- Retire: binutils-riscv-SUB_ULEB128.patch
- Retire: binutils-ppc-dt_relr-relocs.patch
- Retire: binutils-demangler-updates.patch
- Retire: binutils-Intel-APX-part-1.patch
- Retire: binutils-power-11.patch
- Retire: binutils-Intel-APX-part-1-fixes.patch
- Retire: binutils-multilib.am.patch
- Retire: binutils-Intel-APX-CODE_6_GOTTPOFF.patch
- Retire: binutils-archive-DT_SYMTAB.patch

* Mon Jul 29 2024 Jose E. Marchesi <jose.marchesi@oracle.com> - 2.41-3
- Enable support for the BPF arch (rhbz#2281056)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 13 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 2.41-1
- Update to binutils 2.41-37

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.40-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
