# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# workaround LTO related issue when stripping the target files (#1863378)
%global __brp_strip_lto %{nil}

%global cross cross
%global rpmprefix %{nil}

%global build_all		1
%global build_aarch64		%{build_all}
%global build_alpha		%{build_all}
%global build_arm		%{build_all}
%global build_arc		%{build_all}
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
%global build_m68k		%{build_all}
%global build_microblaze	%{build_all}
%global build_mips64		%{build_all}
%global build_mn10300		%{build_all}
%global build_openrisc		%{build_all}
%global build_powerpc64		%{build_all}
%global build_powerpc64le	%{build_all}
%global build_riscv32		%{build_all}
%global build_riscv64		%{build_all}
%global build_s390x		%{build_all}
%global build_sh		%{build_all}
%global build_sparc64		%{build_all}
%global build_x86_64		%{build_all}
%global build_xtensa		%{build_all}

# built compiler generates lots of ICEs
# - none at this time

# gcc considers obsolete
%global build_cris		0
%global build_m32r		0
%global build_score		0
%global build_sh		0
%global build_sh64		0

# gcc doesn't build
# - none at this time

# 32-bit packages we don't build as we can use the 64-bit package instead
%global build_i386		0
%global build_mips		0
%global build_powerpc		0
%global build_s390		0
%global build_sh4		0
%global build_sparc		0

# gcc doesn't support
%global build_metag		0

# not available in binutils-2.22
%global build_unicore32		0

%global multilib_64_archs sparc64 ppc64 s390x x86_64

# we won't build libgcc for these as it depends on C library or kernel headers
# % global no_libgcc_targets	nios2*
%global no_libgcc_targets	none

###############################################################################
#
# The gcc versioning information.  In a sed command below, the specfile winds
# pre-release version numbers in BASE-VER back to the last actually-released
# number.
%global DATE 20250808
%global gitrev f833458d29b4fa40ffce6cf3b37ab9a30a864901
%global gcc_version 15.2.1
%global gcc_major 15

# Note, cross_gcc_release must be integer, if you want to add suffixes
# to %%{release}, append them after %%{cross_gcc_release} on Release:
# line.  gcc_release is the Fedora gcc release that the patches were
# taken from.
%global gcc_release 2
%global cross_gcc_release 1
%global cross_binutils_version 2.43.1-1
%global isl_version 0.16.1
%global isl_libmajor 15

%global _performance_build 1
# Hardening slows the compiler way too much.
%undefine _hardened_build

Summary: Cross C compiler
Name: %{cross}-gcc
Version: %{gcc_version}
Release: %{cross_gcc_release}%{?dist}
# License tag value taken from the gcc package except the values related
# to newlib which isn't present here
License: GPL-3.0-or-later AND LGPL-3.0-or-later AND (GPL-3.0-or-later WITH GCC-exception-3.1) AND (GPL-3.0-or-later WITH Texinfo-exception) AND (LGPL-2.1-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH GNU-compiler-exception) AND BSL-1.0 AND GFDL-1.3-or-later AND Linux-man-pages-copyleft-2-para AND SunPro AND BSD-1-Clause AND BSD-2-Clause AND BSD-2-Clause-Views AND BSD-3-Clause AND BSD-4-Clause AND BSD-Source-Code AND Zlib AND MIT AND Apache-2.0 AND (Apache-2.0 WITH LLVM-Exception) AND ZPL-2.1 AND ISC AND LicenseRef-Fedora-Public-Domain AND HP-1986 AND curl
URL: http://gcc.gnu.org
BuildRequires: gcc-c++
BuildRequires: isl-devel >= %{isl_version}

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone --depth 1 git://gcc.gnu.org/git/gcc.git gcc-dir.tmp
# git --git-dir=gcc-dir.tmp/.git fetch --depth 1 origin %%{gitrev}
# git --git-dir=gcc-dir.tmp/.git archive --prefix=%%{name}-%%{version}-%%{DATE}/ %%{gitrev} | xz -9e > %%{name}-%%{version}-%%{DATE}.tar.xz
# rm -rf gcc-dir.tmp
%global srcdir gcc-%{version}-%{DATE}
Source0: %{srcdir}.tar.xz

Patch0: gcc15-hack.patch
Patch2: gcc15-sparc-config-detection.patch
Patch3: gcc15-libgomp-omp_h-multilib.patch
Patch4: gcc15-libtool-no-rpath.patch
Patch5: gcc15-isl-dl.patch
Patch6: gcc15-isl-dl2.patch
Patch7: gcc15-libstdc++-docs.patch
Patch8: gcc15-no-add-needed.patch
Patch9: gcc15-Wno-format-security.patch
Patch10: gcc15-rh1574936.patch
Patch11: gcc15-d-shared-libphobos.patch
Patch12: gcc15-pr119006.patch

Patch900: cross-gcc-intl-filename.patch
Patch901: cross-gcc-format-config.patch

%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
BuildRequires: binutils >= 2.31
%else
BuildRequires: binutils >= 2.24
%endif
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo
BuildRequires: %{cross}-binutils-common >= %{cross_binutils_version}

# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, libmpc-devel >= 0.8.1
Provides: bundled(libiberty)

%description
Cross-build GNU C compiler collection.

%package -n %{cross}-gcc-common
Summary: Cross-build GNU C compiler documentation and translation files
BuildArch: noarch

%description -n %{cross}-gcc-common
Documentation, manual pages and translation files for cross-build GNU C
compiler.

This is the common part of a set of cross-build GNU C compiler packages for
building kernels for other architectures.  No support for cross-building
user space programs is currently supplied as that would massively multiply the
number of packages.

###############################################################################
#
# Conditional arch package definition
#
###############################################################################
%global do_package() \
%if %2 \
%package -n %{rpmprefix}gcc-%1 \
Summary: Cross-build binary utilities for %1 \
Requires: %{cross}-gcc-common == %{version}-%{release} \
BuildRequires: %{rpmprefix}binutils-%1 >= %{cross_binutils_version} \
Requires: %{rpmprefix}binutils-%1 >= %{cross_binutils_version} \
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1 \
%if 0%{?__isa_bits} == 64 \
Requires: libisl.so.%{isl_libmajor}()(64bit) \
%else \
Requires: libisl.so.%{isl_libmajor} \
%endif \
%description -n %{rpmprefix}gcc-%1 \
Cross-build GNU C compiler. \
\
Only building kernels is currently supported.  Support for cross-building \
user space programs is not currently provided as that would massively multiply \
the number of packages. \
\
%package -n %{rpmprefix}gcc-c++-%1 \
Summary: Cross-build binary utilities for %1 \
Requires: %{rpmprefix}gcc-%1 == %{version}-%{release} \
%description -n %{rpmprefix}gcc-c++-%1 \
Cross-build GNU C++ compiler. \
\
Only the compiler is provided; not libstdc++.  Support for cross-building \
user space programs is not currently provided as that would massively multiply \
the number of packages. \
%endif

%global do_symlink() \
%if %2 \
%package -n gcc-%1 \
Summary: Cross-build binary utilities for %1 \
Requires: gcc-%3 == %{version}-%{release} \
%description -n gcc-%1 \
Cross-build GNU C++ compiler. \
\
Only building kernels is currently supported.  Support for cross-building \
user space programs is not currently provided as that would massively multiply \
the number of packages. \
\
%package -n gcc-c++-%1 \
Summary: Cross-build binary utilities for %1 \
Requires: gcc-%1 == %{version}-%{release} \
Requires: gcc-c++-%3 == %{version}-%{release} \
%description -n gcc-c++-%1 \
Cross-build GNU C++ compiler. \
\
Only the compiler is provided; not libstdc++.  Support for cross-building \
user space programs is not currently provided as that would massively multiply \
the number of packages. \
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
%do_package openrisc-linux-gnu	%{build_openrisc}
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
%do_package sh64-linux-gnu	%{build_sh64}
%do_package sparc-linux-gnu	%{build_sparc}
%do_package sparc64-linux-gnu	%{build_sparc64}
%do_package unicore32-linux-gnu	%{build_unicore32}
%do_package x86_64-linux-gnu	%{build_x86_64}
%do_package xtensa-linux-gnu	%{build_xtensa}

###############################################################################
#
# Preparation
#
###############################################################################
%prep

%setup -q -n %{srcdir} -c
cd %{srcdir}
%patch -P0 -p0 -b .hack~
%patch -P2 -p0 -b .sparc-config-detection~
%patch -P3 -p0 -b .libgomp-omp_h-multilib~
%patch -P4 -p0 -b .libtool-no-rpath~
%patch -P5 -p0 -b .isl-dl
%patch -P6 -p0 -b .isl-dl2
%patch -P7 -p0 -b .libc++docs
%patch -P8 -p0 -b .no-add-needed~
%patch -P9 -p0 -b .Wno-format-security~
%patch -P10 -p0 -b .rh1574936
%patch -P11 -p0 -b .shared-libphobos
%patch -P12 -p0 -b .pr119006

%patch -P900 -p0 -b .cross-intl~
%patch -P901 -p0 -b .format-config~

echo 'Red Hat Cross %{version}-%{cross_gcc_release}' > gcc/DEV-PHASE

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

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
    prep_target sh64-linux-gnu		%{build_sh64}
    prep_target sparc-linux-gnu		%{build_sparc}
    prep_target sparc64-linux-gnu	%{build_sparc64}
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

%global pkgbuilddir %{_builddir}/%{srcdir}

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

CC=gcc
CXX=g++
OPT_FLAGS="%{optflags}"
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=[123]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[123]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/\(-Wp,\)\?-U_FORTIFY_SOURCE//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-flto=auto//g;s/-flto//g;s/-ffat-lto-objects//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-fno-omit-frame-pointer//g;s/-mbackchain//g;s/-mno-omit-leaf-frame-pointer//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -g / -g1 /g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      %{srcdir}/libgcc/Makefile.in
    ;;
esac

#
# Configure the compiler
#
cd %{pkgbuilddir}
function config_target () {
    echo "=== CONFIGURING $1"

    arch=$1
    prefix=$arch-
    build_dir=$1

    case $arch in
	aarch64-*)	target=aarch64-linux-gnu;;
	arc-*)		target=arc-linux-gnu;;
	arm-*)		target=arm-linux-gnueabi;;
	avr32-*)	target=avr-linux;;
	bfin-*)		target=bfin-uclinux;;
	c6x-*)		target=c6x-uclinux;;
	h8300-*)	target=h8300-elf;;
	mn10300-*)	target=am33_2.0-linux;;
	m68knommu-*)	target=m68k-linux;;
	openrisc-*)	target=or1k-linux-gnu;;
	parisc-*)	target=hppa-linux;;
	score-*)	target=score-elf;;
	sh64-*)		target=sh64-linux-elf;;
	v850-*)		target=v850e-linux;;
	x86-*)		target=x86_64-linux;;
	*)		target=$arch;;
    esac

    echo $arch: target is $target
    #export CFLAGS="$RPM_OPT_FLAGS"

    CONFIG_FLAGS=
    case $arch in
	aarch64-*)
	    CONFIG_FLAGS="--enable-standard-branch-protection"
	    ;;
	arc-*)
	    CONFIG_FLAGS="--with-cpu=hs38"
	    ;;
	arm-*)
	    CONFIG_FLAGS="--with-tune=generic-armv7-a --with-arch=armv7-a \
		--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux"
	    ;;
	mips64-*)
	    CONFIG_FLAGS="--with-arch=mips64r2 --with-abi=64 --with-arch_32=mips32r2 --with-fp-32=xx"
	    ;;
	powerpc-*|powerpc64-*|ppc-*|ppc64-*)
	    CONFIG_FLAGS="--with-cpu-32=power7 --with-tune-32=power8 --with-cpu-64=power7 --with-tune-64=power8 --enable-secureplt"
	    ;;
	powerpc64le-*|ppc64le-*)
	    CONFIG_FLAGS="--with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 --enable-secureplt"
	    ;;
	s390*-*)
	    CONFIG_FLAGS="--with-arch=zEC12 --with-tune=z13 --enable-decimal-float"
	    ;;
	sh-*)
	    CONFIG_FLAGS=--with-multilib-list=m1,m2,m2e,m2a,m2a-single,m4,m4-single,m4-single-only,m4-nofpu
	    ;;
	sh4-*)
	    CONFIG_FLAGS=--with-multilib-list=m4,m4-single,m4-single-only,m4-nofpu
	    ;;
	sh64-*)
	    CONFIG_FLAGS=--with-multilib-list=m5-32media,m5-32media-nofpu,m5-compact,m5-compact-nofpu,m5-64media,m5-64media-nofpu
	    ;;
	sparc-*)
	    CONFIG_FLAGS="--disable-linux-futex --with-cpu=v7"
	    ;;
	sparc64-*)
	    CONFIG_FLAGS="--disable-linux-futex --with-cpu=ultrasparc"
	    ;;
	x86_64-*)
	    CONFIG_FLAGS="--with-arch_32=i686 --with-tune=generic --enable-cet"
	    ;;
    esac

    case $arch in
	alpha*|powerpc*|ppc*|s390*|sparc*)
	    CONFIG_FLAGS="$CONFIG_FLAGS --with-long-double-128" ;;
    esac

    case $arch in
	i[3456]86*|x86_64*|ppc*|ppc64*|s390*|arm*|aarch64*|mips*)
	    CONFIG_FLAGS="$CONFIG_FLAGS --enable-gnu-indirect-function" ;;
    esac

%ifnarch %{mips}
    case $arch in
	mips*) ;;
	*) CONFIG_FLAGS="$CONFIG_FLAGS --with-linker-hash-style=gnu" ;;
    esac
%endif

    mkdir $build_dir
    cd $build_dir

    # We could optimize the cross builds size by --enable-shared but the produced
    # binaries may be less convenient in the embedded environment.
    CC="$CC" \
    CXX="$CXX" \
    CFLAGS="$OPT_FLAGS" \
    CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
    CFLAGS_FOR_TARGET="-g -O2 -Wall -fexceptions" \
    AR_FOR_TARGET=%{_bindir}/$arch-ar \
    AS_FOR_TARGET=%{_bindir}/$arch-as \
    DLLTOOL_FOR_TARGET=%{_bindir}/$arch-dlltool \
    LD_FOR_TARGET=%{_bindir}/$arch-ld \
    NM_FOR_TARGET=%{_bindir}/$arch-nm \
    OBJDUMP_FOR_TARGET=%{_bindir}/$arch-objdump \
    RANLIB_FOR_TARGET=%{_bindir}/$arch-ranlib \
    READELF_FOR_TARGET=%{_bindir}/$arch-readelf \
    STRIP_FOR_TARGET=%{_bindir}/$arch-strip \
    WINDRES_FOR_TARGET=%{_bindir}/$arch-windres \
    WINDMC_FOR_TARGET=%{_bindir}/$arch-windmc \
    LDFLAGS='-Wl,-z,relro ' \
    ../%{srcdir}/configure \
	--bindir=%{_bindir} \
	--build=%{_target_platform} \
	--datadir=%{_datadir} \
	--disable-decimal-float \
	--disable-dependency-tracking \
	--disable-gold \
	--disable-libgcj \
	--disable-libgomp \
	--disable-libmpx \
	--disable-libquadmath \
	--disable-libssp \
	--disable-libunwind-exceptions \
	--disable-shared \
	--disable-silent-rules \
	--disable-sjlj-exceptions \
	--disable-threads \
	--with-ld=/usr/bin/$arch-ld \
	--enable-__cxa_atexit \
	--enable-checking=release \
	--enable-gnu-unique-object \
	--enable-initfini-array \
	--enable-languages=c,c++ \
	--enable-linker-build-id \
	--enable-lto \
	--enable-nls \
	--enable-obsolete \
	--enable-plugin \
%ifarch ppc ppc64 ppc64le ppc64p7
	--enable-secureplt \
%endif
	--enable-targets=all \
	--exec-prefix=%{_exec_prefix} \
	--host=%{_target_platform} \
	--includedir=%{_includedir} \
	--infodir=%{_infodir} \
	--libexecdir=%{_libexecdir} \
	--localstatedir=%{_localstatedir} \
	--mandir=%{_mandir} \
	--prefix=%{_prefix} \
	--program-prefix=$prefix \
	--sbindir=%{_sbindir} \
	--sharedstatedir=%{_sharedstatedir} \
	--sysconfdir=%{_sysconfdir} \
	--target=$target \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla/ \
	--with-gcc-major-version-only \
	--with-isl \
	--with-newlib \
	--with-plugin-ld=%{_bindir}/$arch-ld \
	--with-sysroot=%{_prefix}/$arch/sys-root \
	--with-system-libunwind \
	--with-system-zlib \
	--without-headers \
	$CONFIG_FLAGS
%if 0
	--libdir=%{_libdir} # we want stuff in /usr/lib/gcc/ not /usr/lib64/gcc
%endif

    cd ..
}

for target in `cat target.list`
do
    config_target $target
done

function build_target () {
    echo "=== BUILDING $1"

    arch=$1
    build_dir=$1

    BUILD_FLAGS=
    case $arch in
	x86_64-*)
	    BUILD_FLAGS="gcc_cv_libc_provides_ssp=yes gcc_cv_as_ix86_tlsldm=yes"
	    ;;
    esac

    AR_FOR_TARGET=%{_bindir}/$arch-ar \
    AS_FOR_TARGET=%{_bindir}/$arch-as \
    DLLTOOL_FOR_TARGET=%{_bindir}/$arch-dlltool \
    LD_FOR_TARGET=%{_bindir}/$arch-ld \
    NM_FOR_TARGET=%{_bindir}/$arch-nm \
    OBJDUMP_FOR_TARGET=%{_bindir}/$arch-objdump \
    RANLIB_FOR_TARGET=%{_bindir}/$arch-ranlib \
    READELF_FOR_TARGET=%{_bindir}/$arch-readelf \
    STRIP_FOR_TARGET=%{_bindir}/$arch-strip \
    WINDRES_FOR_TARGET=%{_bindir}/$arch-windres \
    WINDMC_FOR_TARGET=%{_bindir}/$arch-windmc \
    make -C $build_dir %{_smp_mflags} tooldir=%{_prefix} $BUILD_FLAGS all-gcc

    echo "=== BUILDING LIBGCC $1"
    case $arch in
	%{no_libgcc_targets})
	    ;;
	*)
	    make -C $build_dir tooldir=%{_prefix} all-target-libgcc
	    ;;
    esac

}

for target in `cat target.list`
do
    build_target $target
done

###############################################################################
#
# Installation
#
###############################################################################
%install
rm -rf %{buildroot}

function install_bin () {
    echo "=== INSTALLING $1"

    arch=$1
    cpu=${1%%%%-*}

    case $arch in
	%{no_libgcc_targets})	with_libgcc="";;
	*)			with_libgcc="install-target-libgcc";;
    esac

    make -C $arch DESTDIR=%{buildroot} install-gcc ${with_libgcc}

    # We want links for ppc and ppc64 also if we make powerpc, powerpc64 or  powerpc64le
    case $cpu in
	powerpc*)
	    cd %{buildroot}/usr/bin
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
    mkdir -p %{buildroot}%{_prefix}/$target/sys-root
    install_bin $target
done

grep ^powerpc target.list | sed -e s/powerpc/ppc/ >symlink-target.list

# For cross-gcc we drop the documentation.
rm -rf %{buildroot}%{_infodir}

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_libdir}/{libffi*,libiberty.a}
rm -f %{buildroot}%{_libexecdir}/gcc/*/%{gcc_major}/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/bin/*-gcc-%{gcc_major} || :
rmdir  %{buildroot}%{_includedir}

find %{buildroot}%{_datadir} -name gcc.mo |
while read x
do
    y=`dirname $x`
    mv $x $y/%{cross}-gcc.mo
done

%find_lang %{cross}-gcc

gzip %{buildroot}%{_mandir}/man1/*.1
rm %{buildroot}%{_mandir}/man7/*.7
rmdir %{buildroot}%{_mandir}/man7

# All the installed manual pages and translation files for each program are the
# same, so symlink them to the common package
cd %{buildroot}%{_mandir}/man1
for i in %{cross}-cpp.1.gz %{cross}-gcc.1.gz %{cross}-g++.1.gz %{cross}-gcov.1.gz
do
    j=${i#%{cross}-}

    for k in *-$j
    do
	if [ $k != $i -a ! -L $k ]
	then
	    mv $k $i
	    ln -s $i $k
	fi
    done
done

# Add manpages the additional symlink-only targets
%if %{build_powerpc}%{build_powerpc64}%{build_powerpc64le}
for i in powerpc*
do
    ln -s $i ppc${i#powerpc}
done
%endif

cd -

function install_lang () {
    arch=$1
    cpu=${arch%%%%-*}

    case $cpu in
	avr32)		target_cpu=avr;;
	bfin)		target_cpu=bfin;;
	h8300)		target_cpu=h8300;;
	mn10300)	target_cpu=am33_2.0;;
	openrisc)	target_cpu=or1k;;
	parisc)		target_cpu=hppa;;
	score)		target_cpu=score;;
	v850)		target_cpu=v850e;;
	x86)		target_cpu=x86_64;;
	*)		target_cpu=$cpu;;
    esac

    (
	echo '%{_bindir}/'$arch'*-cpp'
	echo '%{_bindir}/'$arch'*-gcc'
	echo '%{_bindir}/'$arch'*-gcc-ar'
	echo '%{_bindir}/'$arch'*-gcc-nm'
	echo '%{_bindir}/'$arch'*-gcc-ranlib'
	case $cpu in
	    bpf*)
		rm -f %{buildroot}%{_mandir}/man1/${arch}*-gcov*
		;;
	    *)
		echo '%{_bindir}/'$arch'*-gcov*'
		echo '%{_mandir}/man1/'$arch'*-gcov*'
		;;
	esac
	echo '%{_bindir}/'$arch'*-lto-dump'
	echo '%{_mandir}/man1/'$arch'*-cpp*'
	echo '%{_mandir}/man1/'$arch'*-gcc*'
	echo '%{_mandir}/man1/'$arch'*-lto-dump*'
	case $cpu in
	    ppc*|ppc64*)
		;;
	    *)
		echo '/usr/lib/gcc/'$target_cpu'-*/'
		echo '%{_libexecdir}/gcc/'$target_cpu'-*/*/cc1'
		echo '%{_libexecdir}/gcc/'$target_cpu'-*/*/collect2'
		echo '%{_libexecdir}/gcc/'$target_cpu'-*/*/[abd-z]*'
		echo %{_prefix}/$arch/sys-root
		;;
	esac

    ) >files.$arch

    (
	echo '%{_bindir}/'$arch'*-c++'
	echo '%{_bindir}/'$arch'*-g++'
	echo '%{_mandir}/man1/'$arch'*-g++*'
	case $cpu in
	    ppc*|ppc64*)
		;;
	    *)
		echo '%{_libexecdir}/gcc/'$target_cpu'-*/*/cc1plus'
	esac
    ) >files-c++.$arch
}

for target in `cat target.list symlink-target.list`
do
    install_lang $target
done

%global __ar_no_strip $RPM_BUILD_DIR/%{srcdir}/ar-no-strip
cat >%{__ar_no_strip} <<EOF
#!/bin/bash
f=\$2
if [ \${f##*/} = libgcc.a -o \${f##*/} = libgcov.a ]
then
	:
else
	%{__strip} \$*
fi
EOF
chmod +x %{__ar_no_strip}
%undefine __strip
%global __strip %{__ar_no_strip}

###############################################################################
#
# Filesets
#
###############################################################################
%files -n %{cross}-gcc-common -f %{cross}-gcc.lang
%doc %{srcdir}/COPYING*
%doc %{srcdir}/README
%{_mandir}/man1/%{cross}-*

%global do_files() \
%if %2 \
%files -n %{rpmprefix}gcc-%1 -f files.%1 \
%files -n %{rpmprefix}gcc-c++-%1 -f files-c++.%1 \
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
%do_files riscv32-linux-gnu	%{build_riscv32}
%do_files riscv64-linux-gnu	%{build_riscv64}
%do_files s390-linux-gnu	%{build_s390}
%do_files s390x-linux-gnu	%{build_s390x}
%do_files score-linux-gnu	%{build_score}
%do_files sh-linux-gnu		%{build_sh}
%do_files sh4-linux-gnu		%{build_sh4}
%do_files sh64-linux-gnu	%{build_sh64}
%do_files sparc-linux-gnu	%{build_sparc}
%do_files sparc64-linux-gnu	%{build_sparc64}
%do_files unicore32-linux-gnu	%{build_unicore32}
%do_files x86_64-linux-gnu	%{build_x86_64}
%do_files xtensa-linux-gnu	%{build_xtensa}

%changelog
* Wed Aug 13 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 15.2.1-1
- Update to 15.2.1 GA

* Tue Jul 29 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 15.1.1-3
- Enable PAC/BTI/GCS in aarch64 CRT

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 15.1.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Apr 27 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 15.1.1-1
- Update to gcc 15.1 GA

* Wed Apr 02 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 15.0.1-0.2
- Update to latest gcc-15 snapshot

* Mon Mar 17 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 15.0.1-0.1
- Update to gcc-15 snapshot
- Drop NIOS2 support (retired upstream)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan 11 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 14.2.1-2
- Add support for riscv632 arch

* Sun Oct 27 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 14.2.1-1
- Update to 14.2.1

* Wed Aug 28 2024 Jose E. Marchesi <jose.marchesi@oracle.com> - 14.1.1-2
- Enable support for the BPF arch (rhbz#2281043).

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 14.1.1-1.2
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.1.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 13 2024 Peter Robinson <pbrobinson@fedoraproject.org> - 14.1.1-1
- Update to gcc 14.1.1

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.2.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.2.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jul 31 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 13.2.1-1
- Update to 13.2.1
- Re-enable PARISC (hppa/hppa64)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.1.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jun 10 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 13.1.1-2
- Fix libisl version issue

* Thu Jun 08 2023 Peter Robinson <pbrobinson@fedoraproject.org> - 13.1.1-1
- Update to gcc 13.1
- Drop tile/hppa support (dropped upstream)

* Tue Apr 18 2023 Arjun Shankar <arjun@redhat.com> - 12.2.1-6
- Backport upstream patches for improved C99 compatibility

* Tue Jan 24 2023 Michael Brown <mbrown@fensystems.co.uk> - 12.2.1-5
- Enable support for LoongArch64

* Sun Jan 22 2023 Michael Brown <mbrown@fensystems.co.uk> - 12.2.1-4
- Update to match gcc package's 12.2.1-4 release

* Sun Jan 22 2023 Michael Brown <mbrown@fensystems.co.uk> - 12.2.1-3
- Update to match gcc package's 12.2.1-3 release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.2.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 01 2023 Dan Horák <dan[at]danny.cz> - 12.2.1-2
- fix the openrisc toolchain triplet to match binutils (rhbz#2096361)

* Tue Aug 30 2022 Dan Horák <dan[at]danny.cz> - 12.2.1-1
- Update to 12.2.1 GA release
- Add Requires for plugin development (rhbz#2121894)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat May 07 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 12.1.1-1.2
- Update to 12.1.1 GA release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.2.1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jul 31 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 11.2.1-1
- Update to gcc 11.2.1

* Sat Jul 24 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 11.1.1-1
- Update to gcc 11.1.1
- Enable OpenRISC (or1k) support
- Disable sh/crui support

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.1-3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 11 2021 Dan Horák <dan[at]danny.cz> - 10.2.1-3.2
- reduce debuginfo verbosity

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 04 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 10.2.1-3
- GCC 10.2.0 release

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.1.1-2.2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.1.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Jeff Law <law@redhat.com> - 10.1.1-2
- Fix broken configure files compromised by LTO
- Add autoconf to BuildRequires

* Fri May 08 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 10.1.1-1
- GCC 10.1.0 release

* Thu Apr 30 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 10.0.1-0.13
- Update to gcc 10 snapshot 0.13

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 14 2019 Jeff Law <law@redhat.com> - 9.2.1-3
- Fix unprintable control character in PA backend caught by gcc-10

* Wed Oct  9 2019 Jerry James <loganjerry@gmail.com> - 9.2.1-2
- Rebuild for mpfr 4

* Tue Aug 27 2019 Peter Robinson <pbrobinson@fedoraproject.org> 9.2.1-1
- Sync with gcc-9.2.1-1

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 2019 Tom Callaway <spot@fedoraproject.org> - 9.1.1-2
- remove shared support from arm (glibc-arm-linux-gnu is dead)

* Sun May 26 2019 Peter Robinson <pbrobinson@fedoraproject.org> 9.1.1-1
- Sync with gcc-9.1.1-1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov  7 2018 Tom Callaway <spot@fedoraproject.org> - 8.2.1-1
- update to 8.2.1

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 David Howells <dhowells@redhat.com> - 8.1.1-3
- Change ARC to multilib (#1600183).
- Fix arc700 cpu type (#1600183).

* Wed Jul 11 2018 David Howells <dhowells@redhat.com> - 8.1.1-3
- Switch ARC to arc-linux-gnu and use hs38 not arc700 (#1600183).

* Tue Jul 10 2018 David Howells <dhowells@redhat.com> - 8.1.1-2
- Sync with gcc-8.1.1-4.
- Add support for the ARC arch (#1599744).

* Tue May 29 2018 David Howells <dhowells@redhat.com> - 8.1.1-1
- Sync with gcc-8.1.1-1.

* Fri Mar 30 2018 David Howells <dhowells@redhat.com> - 8.0.1-0.1
- Move to gcc-8 (#1580076).
