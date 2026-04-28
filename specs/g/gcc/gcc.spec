# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global DATE 20260123
%global gitrev 226e8310eed1ce10784f98f199e1aa4b12ca86b7
%global gcc_version 15.2.1
%global gcc_major 15
# Note, gcc_release must be integer, if you want to add suffixes to
# %%{release}, append them after %%{gcc_release} on Release: line.
%global gcc_release 7
%global nvptx_tools_gitrev a0c1fff6534a4df9fb17937c3c4a4b1071212029
%global newlib_cygwin_gitrev d35cc82b5ec15bb8a5fe0fe11e183d1887992e99
%global _unpackaged_files_terminate_build 0
%if 0%{?fedora:1}
%global _performance_build 1
# Hardening slows the compiler way too much.
%undefine _hardened_build
%endif
%undefine _auto_set_build_flags
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
# Until annobin is fixed (#1519165).
%undefine _annotated_build
%endif
# Strip will fail on nvptx-none *.a archives and the brp-* scripts will
# fail randomly depending on what is stripped last.
%if 0%{?__brp_strip_static_archive:1}
%global __brp_strip_static_archive %{__brp_strip_static_archive} || :
%endif
%if 0%{?__brp_strip_lto:1}
%global __brp_strip_lto %{__brp_strip_lto} || :
%endif
%if 0%{?rhel} > 0
%define bugurl https://issues.redhat.com
%else
%define bugurl https://bugzilla.redhat.com/bugzilla
%endif
%{!?dist_bug_report_url: %global dist_bug_report_url %bugurl}

%if 0%{?fedora} < 32 && 0%{?rhel} < 8
%global multilib_64_archs sparc64 ppc64 ppc64p7 s390x x86_64
%else
%global multilib_64_archs sparc64 ppc64 ppc64p7 x86_64
%endif
%if 0%{?rhel} > 7
%global build_ada 0
%global build_objc 0
%global build_go 0
%global build_d 0
%global build_m2 0
%global build_cobol 0
%else
%ifarch %{ix86} x86_64 ia64 ppc %{power64} alpha s390x %{arm} aarch64 riscv64
%global build_ada 0
%else
%global build_ada 0
%endif
%global build_objc 0
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_go 0
%else
%global build_go 0
%endif
%ifarch %{ix86} x86_64 %{arm} aarch64 %{mips} s390 s390x riscv64
%global build_d 0
%else
%global build_d 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_m2 0
%else
%global build_m2 0
%endif
%ifarch x86_64 aarch64
%global build_cobol 0
%else
%global build_cobol 0
%endif
%endif
%ifarch %{ix86} x86_64 ia64 ppc64le
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 riscv64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64 aarch64
%global build_libhwasan 1
%else
%global build_libhwasan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64 s390x riscv64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch x86_64 ppc64 ppc64le aarch64 s390x riscv64
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 riscv64
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64 riscv64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%if 0%{?rhel} > 8
%global build_isl 0
%else
%global build_isl 1
%endif
%global build_libstdcxx_docs 1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips} riscv64
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
%ifarch x86_64 ppc64le
%global build_offload_nvptx 0
%else
%global build_offload_nvptx 0
%endif
%ifarch x86_64
%global build_offload_amdgcn 0
%else
%global build_offload_amdgcn 0
%endif
%if 0%{?fedora} < 32 && 0%{?rhel} < 8
%ifarch s390x
%global multilib_32_arch s390
%endif
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64 ppc64p7
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif
%if 0%{?fedora} >= 36 || 0%{?rhel} >= 10
%global build_annobin_plugin 1
%else
%global build_annobin_plugin 0
%endif
Summary: Various compilers (C, C++, Objective-C, ...)
Name: gcc
Version: %{gcc_version}
Release: %{gcc_release}%{?dist}
# License notes for some of the less obvious ones:
#   gcc/doc/cppinternals.texi: Linux-man-pages-copyleft-2-para
#   isl: MIT, BSD-2-Clause
#   libcody: Apache-2.0
#   libphobos/src/etc/c/curl.d: curl
# All of the remaining license soup is in newlib.
License: GPL-3.0-or-later AND LGPL-3.0-or-later AND (GPL-3.0-or-later WITH GCC-exception-3.1) AND (GPL-3.0-or-later WITH Texinfo-exception) AND (LGPL-2.1-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH GNU-compiler-exception) AND BSL-1.0 AND GFDL-1.3-or-later AND Linux-man-pages-copyleft-2-para AND SunPro AND BSD-1-Clause AND BSD-2-Clause AND BSD-2-Clause-Views AND BSD-3-Clause AND BSD-4-Clause AND BSD-Source-Code AND Zlib AND MIT AND Apache-2.0 AND (Apache-2.0 WITH LLVM-Exception) AND ZPL-2.1 AND ISC AND LicenseRef-Fedora-Public-Domain AND HP-1986 AND curl AND Martin-Birgmeier AND HPND-Markus-Kuhn AND dtoa AND SMLNJ AND AMD-newlib AND OAR AND HPND-merchantability-variant AND HPND-Intel
# The source for this package was pulled from upstream's vcs.
# %%{gitrev} is some commit from the
# https://gcc.gnu.org/git/?p=gcc.git;h=refs/vendors/redhat/heads/gcc-%%{gcc_major}-branch
# branch.  Use the following command to generate the tarball:
# ./update-gcc.sh %%{gitrev}
# optionally if say /usr/src/gcc/.git/ is an existing gcc git clone
# ./update-gcc.sh %%{gitrev} /usr/src/gcc/.git/
# to speed up the clone operations.  Note, %%{gitrev} macro in
# gcc.spec shouldn't be updated before running the script, the script
# will update it, fill in some %%changelog details etc.
Source0: gcc-%{version}-%{DATE}.tar.xz
# The source for nvptx-tools package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone --depth 1 https://github.com/MentorEmbedded/nvptx-tools.git nvptx-tools-dir.tmp
# git --git-dir=nvptx-tools-dir.tmp/.git fetch --depth 1 origin %%{nvptx_tools_gitrev}
# git --git-dir=nvptx-tools-dir.tmp/.git archive --prefix=nvptx-tools-%%{nvptx_tools_gitrev}/ %%{nvptx_tools_gitrev} | xz -9e > nvptx-tools-%%{nvptx_tools_gitrev}.tar.xz
# rm -rf nvptx-tools-dir.tmp
Source1: nvptx-tools-%{nvptx_tools_gitrev}.tar.xz
# The source for nvptx-newlib package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone https://sourceware.org/git/newlib-cygwin.git newlib-cygwin-dir.tmp
# git --git-dir=newlib-cygwin-dir.tmp/.git archive --prefix=newlib-cygwin-%%{newlib_cygwin_gitrev}/ %%{newlib_cygwin_gitrev} ":(exclude)newlib/libc/sys/linux/include/rpc/*.[hx]" | xz -9e > newlib-cygwin-%%{newlib_cygwin_gitrev}.tar.xz
# rm -rf newlib-cygwin-dir.tmp
Source2: newlib-cygwin-%{newlib_cygwin_gitrev}.tar.xz
%global isl_version 0.24
Source3: https://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
URL: http://gcc.gnu.org
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %%gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
# Need binutils which support .loc view >= 2.30
# Need binutils which support --generate-missing-build-notes=yes >= 2.31
# Need binutils which support .base64 >= 2.43
BuildRequires: binutils >= 2.43
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, sharutils
BuildRequires: texinfo, texinfo-tex, /usr/bin/pod2man
BuildRequires: systemtap-sdt-devel >= 1.3
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1
BuildRequires: python3-devel, /usr/bin/python
BuildRequires: gcc, gcc-c++, make
%if %{build_go}
BuildRequires: hostname, procps
%endif
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
BuildRequires: libzstd-devel
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs}
BuildRequires: (glibc32 or glibc-devel(%{__isa_name}-32))
%endif
%ifarch sparcv9 ppc
BuildRequires: (glibc64 or glibc-devel(%{__isa_name}-64))
%endif
%if %{build_ada}
# Ada requires Ada to build
BuildRequires: gcc-gnat >= 3.1, libgnat >= 3.1
%endif
%if %{build_d}
# D requires D to build
BuildRequires: gcc-gdc >= 11.0.0, libgphobos-static >= 11.0.0
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
%if %{build_libstdcxx_docs}
BuildRequires: doxygen >= 1.7.1
BuildRequires: graphviz, dblatex, texlive-collection-latex, docbook5-style-xsl
%endif
%if %{build_offload_amdgcn}
BuildRequires: llvm >= 15, lld >= 15
%endif
Requires: cpp = %{version}-%{release}
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %%gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
# Need binutils that support .loc view >= 2.30
# Need binutils which support --generate-missing-build-notes=yes >= 2.31
# Need binutils that support .base64 >= 2.43
Requires: binutils >= 2.43
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
%ifarch %{arm}
Requires: glibc >= 2.16
%endif
%endif
Requires: libgcc >= %{version}-%{release}
Requires: libgomp = %{version}-%{release}
# lto-wrapper invokes make
Requires: make
%if !%{build_ada}
Obsoletes: gcc-gnat < %{version}-%{release}
%endif
Obsoletes: gcc-java < %{version}-%{release}
AutoReq: true
Provides: bundled(libiberty)
Provides: bundled(libbacktrace)
Provides: bundled(libffi)
Provides: gcc(major) = %{gcc_major}

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
Patch13: gcc15-pr123273.patch
Patch14: gcc15-pr123667.patch
Patch15: gcc15-pr123737.patch

Patch50: isl-rh2155127.patch

Patch100: gcc15-fortran-fdec-duplicates.patch

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%global _gnu %{nil}
%else
%global _gnu -gnueabi
%endif
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}
%endif
%ifarch ppc ppc64p7
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}
%endif
%ifnarch sparcv9 ppc ppc64p7
%global gcc_target_platform %{_target_platform}
%endif

%if %{build_go}
# Avoid stripping these libraries and binaries.
%global __os_install_post \
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.24.* \
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json \
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet \
%__os_install_post \
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgo.so.24.* \
chmod 755 %{buildroot}%{_prefix}/bin/go.gcc \
chmod 755 %{buildroot}%{_prefix}/bin/gofmt.gcc \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json \
chmod 755 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet \
%{nil}
%endif

%description
The gcc package contains the GNU Compiler Collection version %{gcc_major}.
You'll need this package in order to compile C code.

%package -n libgcc
Summary: GCC version %{gcc_major} shared support library
Autoreq: false
%if !%{build_ada}
Obsoletes: libgnat < %{version}-%{release}
%endif
Obsoletes: libmudflap < %{version}-%{release}
Obsoletes: libmudflap-devel < %{version}-%{release}
Obsoletes: libmudflap-static < %{version}-%{release}
Obsoletes: libgcj < %{version}-%{release}
Obsoletes: libgcj-devel < %{version}-%{release}
Obsoletes: libgcj-src < %{version}-%{release}
%ifarch %{ix86} x86_64
Obsoletes: libcilkrts < %{version}-%{release}
Obsoletes: libcilkrts-static < %{version}-%{release}
Obsoletes: libmpx < %{version}-%{release}
Obsoletes: libmpx-static < %{version}-%{release}
%endif

%description -n libgcc
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package c++
Summary: C++ support for GCC
Requires: gcc = %{version}-%{release}
Requires: libstdc++ = %{version}-%{release}
Requires: libstdc++-devel = %{version}-%{release}
Provides: gcc-g++ = %{version}-%{release}
Provides: g++ = %{version}-%{release}
Autoreq: true

%description c++
This package adds C++ support to the GNU Compiler Collection.
It includes support for most of the current C++ specification,
including templates and exception handling.

%package -n libstdc++
Summary: GNU Standard C++ Library
Autoreq: true
Requires: glibc >= 2.10.90-7
BuildRequires: tzdata >= 2017c
%if 0%{?fedora} > 38 || 0%{?rhel} > 9
Recommends: tzdata >= 2017c
%else
Requires: tzdata >= 2017c
%endif

%description -n libstdc++
The libstdc++ package contains a rewritten standard compliant GCC Standard
C++ Library.

%package -n libstdc++-devel
Summary: Header files and libraries for C++ development
Requires: libstdc++%{?_isa} = %{version}-%{release}
Autoreq: true

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n libstdc++-static
Summary: Static libraries for the GNU standard C++ library
Requires: libstdc++-devel = %{version}-%{release}
Autoreq: true

%description -n libstdc++-static
Static libraries for the GNU standard C++ library.

%package -n libstdc++-docs
Summary: Documentation for the GNU standard C++ library
Autoreq: true

%description -n libstdc++-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package objc
Summary: Objective-C support for GCC
Requires: gcc = %{version}-%{release}
Requires: libobjc = %{version}-%{release}
Autoreq: true

%description objc
gcc-objc provides Objective-C support for the GCC.
Mainly used on systems running NeXTSTEP, Objective-C is an
object-oriented derivative of the C language.

%package objc++
Summary: Objective-C++ support for GCC
Requires: gcc-c++ = %{version}-%{release}, gcc-objc = %{version}-%{release}
Autoreq: true

%description objc++
gcc-objc++ package provides Objective-C++ support for the GCC.

%package -n libobjc
Summary: Objective-C runtime
Autoreq: true

%description -n libobjc
This package contains Objective-C shared library which is needed to run
Objective-C dynamically linked programs.

%package gfortran
Summary: Fortran support
Requires: gcc = %{version}-%{release}
Requires: libgfortran = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
Requires: libquadmath-devel = %{version}-%{release}
%endif
Provides: gcc-fortran = %{version}-%{release}
Provides: gfortran = %{version}-%{release}
Autoreq: true

%description gfortran
The gcc-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package -n libgfortran
Summary: Fortran runtime
Autoreq: true
%if 0%{?fedora} < 28 && 0%{?rhel} < 8
%if %{build_libquadmath}
Requires: libquadmath = %{version}-%{release}
%endif
%endif

%description -n libgfortran
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%package -n libgfortran-static
Summary: Static Fortran libraries
Requires: libgfortran = %{version}-%{release}
Requires: gcc = %{version}-%{release}
%if %{build_libquadmath}
Requires: libquadmath-static = %{version}-%{release}
%endif

%description -n libgfortran-static
This package contains static Fortran libraries.

%package gdc
Summary: D support
Requires: gcc = %{version}-%{release}
Requires: libgphobos = %{version}-%{release}
Provides: gcc-d = %{version}-%{release}
Provides: gdc = %{version}-%{release}
Autoreq: true

%description gdc
The gcc-gdc package provides support for compiling D
programs with the GNU Compiler Collection.

%package -n libgphobos
Summary: D runtime
Autoreq: true

%description -n libgphobos
This package contains D shared library which is needed to run
D dynamically linked programs.

%package -n libgphobos-static
Summary: Static D libraries
Requires: libgphobos = %{version}-%{release}
Requires: gcc-gdc = %{version}-%{release}

%description -n libgphobos-static
This package contains static D libraries.

%package gm2
Summary: Modula-2 support
Requires: gcc = %{version}-%{release}
Requires: libgm2 = %{version}-%{release}
Provides: gcc-m2 = %{version}-%{release}
Provides: gm2 = %{version}-%{release}
Autoreq: true

%description gm2
The gcc-gm2 package provides support for compiling Modula-2
programs with the GNU Compiler Collection.

%package -n libgm2
Summary: Modula-2 runtime
Autoreq: true

%description -n libgm2
This package contains Modula-2 shared libraries which are needed to run
Modula-2 dynamically linked programs.

%package -n libgm2-static
Summary: Static Modula-2 libraries
Requires: libgm2 = %{version}-%{release}
Requires: gcc-gm2 = %{version}-%{release}

%description -n libgm2-static
This package contains static Modula-2 libraries.

%package gcobol
Summary: COBOL support
Requires: gcc = %{version}-%{release}
Requires: gcc-c++ = %{version}-%{release}
Requires: libgcobol = %{version}-%{release}
Autoreq: true

%description gcobol
The gcc-gcobol package provides support for compiling COBOL
programs with the GNU Compiler Collection.

%package -n libgcobol
Summary: COBOL runtime
Autoreq: true

%description -n libgcobol
This package contains COBOL shared libraries which are needed to run
COBOL dynamically linked programs.

%package -n libgcobol-static
Summary: Static COBOL libraries
Requires: libgcobol = %{version}-%{release}
Requires: gcc-gcobol = %{version}-%{release}

%description -n libgcobol-static
This package contains static COBOL libraries.

%package -n libgomp
Summary: GCC OpenMP v4.5 shared support library

%description -n libgomp
This package contains GCC shared support library which is needed
for OpenMP v4.5 support.

%package -n libgomp-offload-nvptx
Summary: GCC OpenMP v4.5 plugin for offloading to NVPTX
Requires: libgomp = %{version}-%{release}

%description -n libgomp-offload-nvptx
This package contains libgomp plugin for offloading to NVidia
PTX.  The plugin needs libcuda.so.1 shared library that has to be
installed separately.

%package -n libgomp-offload-amdgcn
Summary: GCC OpenMP v4.5 plugin for offloading to AMD GCN
Requires: libgomp = %{version}-%{release}
%if 0%{?fedora:1}
Requires: rocm-runtime >= 6.0.0
%endif

%description -n libgomp-offload-amdgcn
This package contains libgomp plugin for offloading to AMD ROCm capable
devices.

%package gdb-plugin
Summary: GCC plugin for GDB
Requires: gcc = %{version}-%{release}

%description gdb-plugin
This package contains GCC plugin for GDB C expression evaluation.

%package -n libgccjit
Summary: Library for embedding GCC inside programs and libraries
Requires: gcc = %{version}-%{release}

%description -n libgccjit
This package contains shared library with GCC JIT front-end.

%package -n libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
%if 0%{?fedora} > 27 || 0%{?rhel} > 7
BuildRequires: python3-sphinx
%else
BuildRequires: python-sphinx
%endif
Requires: libgccjit = %{version}-%{release}

%description -n libgccjit-devel
This package contains header files and documentation for GCC JIT front-end.

%package -n libgdiagnostics
Summary: Library for emitting diagnostics

%description -n libgdiagnostics
This package contains libgdiagnostics shared library and sarif-replay program.

%package -n libgdiagnostics-devel
Summary: Support for emitting diagnostics
Requires: libgdiagnostics = %{version}-%{release}

%description -n libgdiagnostics-devel
This package contains header files and documentation for the libgdiagnostics
library.

%package -n libquadmath
Summary: GCC __float128 shared support library

%description -n libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n libquadmath-devel
Summary: GCC __float128 support
Requires: libquadmath = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libquadmath-static
Summary: Static libraries for __float128 support
Requires: libquadmath-devel = %{version}-%{release}

%description -n libquadmath-static
This package contains static libraries for building Fortran programs
using REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libitm-devel
Summary: The GNU Transactional Memory support
Requires: libitm = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package -n libitm-static
Summary: The GNU Transactional Memory static library
Requires: libitm-devel = %{version}-%{release}

%description -n libitm-static
This package contains GNU Transactional Memory static libraries.

%package -n libatomic
Summary: The GNU Atomic library

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libatomic-static
Summary: The GNU Atomic static library
Requires: libatomic = %{version}-%{release}

%description -n libatomic-static
This package contains GNU Atomic static libraries.

%package -n libasan
Summary: The Address Sanitizer runtime library

%description -n libasan
This package contains the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%package -n libasan-static
Summary: The Address Sanitizer static library
Requires: libasan = %{version}-%{release}

%description -n libasan-static
This package contains Address Sanitizer static runtime library.

%package -n libhwasan
Summary: The Hardware-assisted Address Sanitizer runtime library

%description -n libhwasan
This package contains the Hardware-assisted Address Sanitizer library
which is used for -fsanitize=hwaddress instrumented programs.

%package -n libhwasan-static
Summary: The Hardware-assisted Address Sanitizer static library
Requires: libhwasan = %{version}-%{release}

%description -n libhwasan-static
This package contains Hardware-assisted Address Sanitizer static runtime
library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n libtsan-static
Summary: The Thread Sanitizer static library
Requires: libtsan = %{version}-%{release}

%description -n libtsan-static
This package contains Thread Sanitizer static runtime library.

%package -n libubsan
Summary: The Undefined Behavior Sanitizer runtime library

%description -n libubsan
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n libubsan-static
Summary: The Undefined Behavior Sanitizer static library
Requires: libubsan = %{version}-%{release}

%description -n libubsan-static
This package contains Undefined Behavior Sanitizer static runtime library.

%package -n liblsan
Summary: The Leak Sanitizer runtime library

%description -n liblsan
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n liblsan-static
Summary: The Leak Sanitizer static library
Requires: liblsan = %{version}-%{release}

%description -n liblsan-static
This package contains Leak Sanitizer static runtime library.

%package -n cpp
Summary: The C Preprocessor
Requires: filesystem >= 3
Provides: /lib/cpp
Autoreq: true

%description -n cpp
Cpp is the GNU C-Compatible Compiler Preprocessor.
Cpp is a macro processor which is used automatically
by the C compiler to transform your program before actual
compilation. It is called a macro processor because it allows
you to define macros, abbreviations for longer
constructs.

The C preprocessor provides four separate functionalities: the
inclusion of header files (files of declarations that can be
substituted into your program); macro expansion (you can define macros,
and the C preprocessor will replace the macros with their definitions
throughout the program); conditional compilation (using special
preprocessing directives, you can include or exclude parts of the
program according to various conditions); and line control (if you use
a program to combine or rearrange source files into an intermediate
file which is then compiled, you can use line control to inform the
compiler about where each source line originated).

You should install this package if you are a C programmer and you use
macros.

%package gnat
Summary: Ada 83, 95, 2005 and 2012 support for GCC
Requires: gcc = %{version}-%{release}
Requires: libgnat = %{version}-%{release}, libgnat-devel = %{version}-%{release}
Autoreq: true

%description gnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
development tools, the documents and Ada compiler.

%package -n libgnat
Summary: GNU Ada 83, 95, 2005 and 2012 runtime shared libraries
Autoreq: true

%description -n libgnat
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
shared libraries, which are required to run programs compiled with the GNAT.

%package -n libgnat-devel
Summary: GNU Ada 83, 95, 2005 and 2012 libraries
Autoreq: true

%description -n libgnat-devel
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
libraries, which are required to compile with the GNAT.

%package -n libgnat-static
Summary: GNU Ada 83, 95, 2005 and 2012 static libraries
Requires: libgnat-devel = %{version}-%{release}
Autoreq: true

%description -n libgnat-static
GNAT is a GNU Ada 83, 95, 2005 and 2012 front-end to GCC. This package includes
static libraries.

%package go
Summary: Go support
Requires: gcc = %{version}-%{release}
Requires: libgo = %{version}-%{release}
Requires: libgo-devel = %{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Provides: gccgo = %{version}-%{release}
Autoreq: true

%description go
The gcc-go package provides support for compiling Go programs
with the GNU Compiler Collection.

%package -n libgo
Summary: Go runtime
Autoreq: true

%description -n libgo
This package contains Go shared library which is needed to run
Go dynamically linked programs.

%package -n libgo-devel
Summary: Go development libraries
Requires: libgo = %{version}-%{release}
Autoreq: true

%description -n libgo-devel
This package includes libraries and support files for compiling
Go programs.

%package -n libgo-static
Summary: Static Go libraries
Requires: libgo = %{version}-%{release}
Requires: gcc = %{version}-%{release}

%description -n libgo-static
This package contains static Go libraries.

%package plugin-devel
Summary: Support for compiling GCC plugins
Requires: gcc = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1

%description plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%package offload-nvptx
Summary: Offloading compiler to NVPTX
Requires: gcc = %{version}-%{release}
Requires: libgomp-offload-nvptx = %{version}-%{release}

%description offload-nvptx
The gcc-offload-nvptx package provides offloading support for
NVidia PTX.  OpenMP and OpenACC programs linked with -fopenmp will
by default add PTX code into the binaries, which can be offloaded
to NVidia PTX capable devices if available.

%package offload-amdgcn
Summary: Offloading compiler to AMD GCN
Requires: gcc = %{version}-%{release}
Requires: libgomp-offload-amdgcn = %{version}-%{release}
Requires: llvm >= 15, lld >= 15

%description offload-amdgcn
The gcc-offload-amdgcn package provides offloading support for
AMD GCN.  OpenMP and OpenACC programs linked with -fopenmp will
by default add GCN code into the binaries, which can be offloaded
to AMD ROCm capable devices if available.

%package plugin-annobin
Summary: The annobin plugin for gcc, built by the installed version of gcc
Requires: gcc = %{version}-%{release}
%if %{build_annobin_plugin}
BuildRequires: annobin-plugin-gcc >= 10.62, rpm-devel, binutils-devel, xz
%endif

%description plugin-annobin
This package adds a version of the annobin plugin for gcc.  This version
of the plugin is explicitly built by the same version of gcc that is installed
so that there cannot be any synchronization problems.

%prep
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2 -a 3
%autopatch -p0 -m 0 -M 4
%if %{build_isl}
%autopatch -p0 -m 5 -M 6
%endif
%if %{build_libstdcxx_docs}
%autopatch -p0 7
%endif
%autopatch -p0 -m 8 -M 9
%if 0%{?fedora} >= 29 || 0%{?rhel} > 7
%autopatch -p0 10
%endif
%autopatch -p0 -m 11 -M 99
touch -r isl-0.24/m4/ax_prog_cxx_for_build.m4 isl-0.24/m4/ax_prog_cc_for_build.m4

%if 0%{?rhel} >= 9
%autopatch -p1 100
%endif

%ifarch %{arm}
rm -f gcc/testsuite/go.test/test/fixedbugs/issue19182.go
%endif
rm -f libphobos/testsuite/libphobos.gc/forkgc2.d
#rm -rf libphobos/testsuite/libphobos.gc

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt
sed -i -e 's/m_report_bug = false;/m_report_bug = true;/' gcc/diagnostic.cc

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

%build

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
      libgcc/Makefile.in
    ;;
esac

%if %{build_offload_nvptx}
mkdir obji
IROOT=`pwd`/obji
cd nvptx-tools-%{nvptx_tools_gitrev}
rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}
CC="$CC" CXX="$CXX" CFLAGS="%{optflags}" CXXFLAGS="%{optflags}" \
../configure --prefix=%{_prefix}
make %{?_smp_mflags}
make install prefix=${IROOT}%{_prefix}
cd ../..

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
rm -rf obj-offload-nvptx-none
mkdir obj-offload-nvptx-none

cd obj-offload-nvptx-none
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --disable-bootstrap --disable-sjlj-exceptions \
	--enable-newlib-io-long-long --with-build-time-tools=${IROOT}%{_prefix}/nvptx-none/bin \
	--target nvptx-none --enable-as-accelerator-for=%{gcc_target_platform} \
	--enable-languages=c,c++,fortran,lto \
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=%dist_bug_report_url \
	--enable-checking=release --with-system-zlib \
	--with-gcc-major-version-only --without-isl
make %{?_smp_mflags}
cd ..
rm -f newlib
%endif

%if %{build_offload_amdgcn}
mkdir -p objia%{_prefix}/bin objia%{_prefix}/amdgcn-amdhsa/bin
IAROOT=`pwd`/objia
ln -sf %{_prefix}/bin/llvm-ar ${IAROOT}%{_prefix}/bin/amdgcn-amdhsa-ar
ln -sf %{_prefix}/bin/llvm-ar ${IAROOT}%{_prefix}/bin/amdgcn-amdhsa-ranlib
ln -sf %{_prefix}/bin/llvm-mc ${IAROOT}%{_prefix}/bin/amdgcn-amdhsa-as
ln -sf %{_prefix}/bin/llvm-nm ${IAROOT}%{_prefix}/bin/amdgcn-amdhsa-nm
ln -sf %{_prefix}/bin/lld ${IAROOT}%{_prefix}/bin/amdgcn-amdhsa-ld
ln -sf ../../bin/amdgcn-amdhsa-ar ${IAROOT}%{_prefix}/amdgcn-amdhsa/bin/ar
ln -sf ../../bin/amdgcn-amdhsa-ranlib ${IAROOT}%{_prefix}/amdgcn-amdhsa/bin/ranlib
ln -sf ../../bin/amdgcn-amdhsa-as ${IAROOT}%{_prefix}/amdgcn-amdhsa/bin/as
ln -sf ../../bin/amdgcn-amdhsa-nm ${IAROOT}%{_prefix}/amdgcn-amdhsa/bin/nm
ln -sf ../../bin/amdgcn-amdhsa-ld ${IAROOT}%{_prefix}/amdgcn-amdhsa/bin/ld

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
rm -rf obj-offload-amdgcn-amdhsa
mkdir obj-offload-amdgcn-amdhsa

cd obj-offload-amdgcn-amdhsa
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --disable-bootstrap --disable-sjlj-exceptions \
	--with-build-time-tools=${IAROOT}%{_prefix}/amdgcn-amdhsa/bin \
	--target amdgcn-amdhsa --enable-as-accelerator-for=%{gcc_target_platform} \
	--enable-languages=c,c++,fortran,lto \
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=%dist_bug_report_url \
	--enable-checking=release --with-system-zlib \
	--with-gcc-major-version-only --without-isl --disable-libquadmath
make %{?_smp_mflags}
cd ..
rm -f newlib
%endif

rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_isl}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
cd isl-build

%ifarch riscv64
# Update config.{sub,guess} scripts for riscv64 (the original ones are too old)
cp -f -v /usr/lib/rpm/%{_vendor}/config.guess ../../isl-%{isl_version}/config.guess
cp -f -v /usr/lib/rpm/%{_vendor}/config.sub ../../isl-%{isl_version}/config.sub
%endif

sed -i 's|libisl\([^-]\)|libgcc%{gcc_major}privateisl\1|g' \
  ../../isl-%{isl_version}/Makefile.{am,in}
../../isl-%{isl_version}/configure \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags} CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC"
make install
cd ../isl-install/lib
rm libgcc%{gcc_major}privateisl.so{,.23}
mv libgcc%{gcc_major}privateisl.so.23.1.0 libisl.so.23
ln -sf libisl.so.23 libisl.so
cd ../..
%endif

enablelgo=
enablelada=
enablelobjc=
enableld=
enablelm2=
enablelcob=
%if %{build_objc}
enablelobjc=,objc,obj-c++
%endif
%if %{build_ada}
enablelada=,ada
%endif
%if %{build_go}
enablelgo=,go
%endif
%if %{build_d}
enableld=,d
%endif
%if %{build_m2}
enablelm2=,m2
%endif
%if %{build_cobol}
enablelcob=,cobol
%endif
offloadtgts=
%if %{build_offload_nvptx}
offloadtgts=nvptx-none
%endif
%if %{build_offload_amdgcn}
offloadtgts=${offloadtgts:+${offloadtgts},}amdgcn-amdhsa
%endif
CONFIGURE_OPTS="\
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=%dist_bug_report_url \
	--enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
	--enable-targets=powerpcle-linux \
%endif
%ifarch ppc64le %{mips} s390x
%ifarch s390x
%if 0%{?fedora} < 32 && 0%{?rhel} < 8
	--enable-multilib \
%else
	--disable-multilib \
%endif
%else
	--disable-multilib \
%endif
%else
	--enable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only \
	--enable-libstdcxx-backtrace --with-libstdcxx-zoneinfo=%{_datadir}/zoneinfo \
%ifnarch %{mips}
	--with-linker-hash-style=gnu \
%endif
	--enable-plugin --enable-initfini-array \
%if %{build_isl}
	--with-isl=`pwd`/isl-install \
%else
	--without-isl \
%endif
%if %{build_offload_nvptx} || %{build_offload_amdgcn}
	--enable-offload-targets=$offloadtgts --enable-offload-defaulted \
%endif
%if %{build_offload_nvptx}
	--without-cuda-driver \
%endif
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%if %{attr_ifunc}
	--enable-gnu-indirect-function \
%endif
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 ppc64le ppc64p7 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch ppc64le
	--with-long-double-format=ieee \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc ppc64 ppc64p7
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%endif
%if 0%{?rhel} == 6
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc64le
%if 0%{?rhel} >= 9
%if 0%{?rhel} >= 10
	--with-cpu-32=power9 --with-tune-32=power10 --with-cpu-64=power9 --with-tune-64=power10 \
%else
	--with-cpu-32=power9 --with-tune-32=power9 --with-cpu-64=power9 --with-tune-64=power9 \
%endif
%else
	--with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--enable-cet \
	--with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch x86_64
%if 0%{?rhel} > 8
%if 0%{?rhel} > 9
	--with-arch_64=x86-64-v3 \
%else
	--with-arch_64=x86-64-v2 \
%endif
%endif
	--with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%endif
%ifarch s390 s390x
%if 0%{?rhel} >= 7
%if 0%{?rhel} > 7
%if 0%{?rhel} > 8
%if 0%{?rhel} >= 9
	--with-arch=z14 --with-tune=z15 \
%else
	--with-arch=z13 --with-tune=arch13 \
%endif
%else
	--with-arch=z13 --with-tune=z14 \
%endif
%else
	--with-arch=z196 --with-tune=zEC12 \
%endif
%else
%if 0%{?fedora} >= 38
	--with-arch=z13 --with-tune=z14 \
%else
%if 0%{?fedora} >= 26
	--with-arch=zEC12 --with-tune=z13 \
%else
	--with-arch=z9-109 --with-tune=z10 \
%endif
%endif
%endif
	--enable-decimal-float \
%endif
%ifarch armv7hl
	--with-tune=generic-armv7-a --with-arch=armv7-a \
	--with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
%ifarch mips mipsel
	--with-arch=mips32r2 --with-fp-32=xx \
%endif
%ifarch mips64 mips64el
	--with-arch=mips64r2 --with-abi=64 \
%endif
%ifarch riscv64
	--with-arch=rv64gc --with-abi=lp64d --with-multilib-list=lp64d \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform} \
%endif
%if 0%{?fedora} >= 35 || 0%{?rhel} >= 9
%ifnarch %{arm}
	--with-build-config=bootstrap-lto --enable-link-serialization=1 \
%endif
%endif
%if 0%{?rhel:1}
	--enable-host-pie --enable-host-bind-now \
%endif
	--disable-libssp \
%if %{build_libquadmath} == 0
	--disable-libquadmath \
%endif
%if %{build_libatomic} == 0
	--disable-libatomic \
%endif
%if %{build_libitm} == 0
	--disable-libitm \
%endif
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
	--enable-languages=c,c++,fortran${enablelobjc}${enablelada}${enablelgo}${enableld}${enablelm2}${enablelcob},lto \
	$CONFIGURE_OPTS

%ifarch sparc sparcv9 sparc64
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" LDFLAGS_FOR_TARGET=-Wl,-z,relro,-z,now bootstrap
%else
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" LDFLAGS_FOR_TARGET=-Wl,-z,relro,-z,now profiledbootstrap
%endif

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
		  | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../../configure --disable-bootstrap --enable-host-shared \
	--enable-languages=jit --enable-libgdiagnostics $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{gcc_major}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
make jit.sphinx.html
make jit.sphinx.install-html jit_htmldir=`pwd`/../../rpm.doc/libgccjit-devel/html
cd ..

%if %{build_isl}
cp -a isl-install/lib/libisl.so.23 gcc/
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/{gfortran,objc,gdc,libphobos,gm2,libgm2,libgdiagnostics-devel,gcobol,libgcobol}
mkdir -p rpm.doc/go rpm.doc/libgo rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer}

for i in {gcc,gcc/cp,gcc/ada,gcc/jit,libstdc++-v3,libobjc,libgomp,libcc1,libatomic,libsanitizer}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%if %{build_objc}
(cd libobjc; for i in README*; do
	cp -p $i ../rpm.doc/objc/$i.libobjc
done)
%endif
%if %{build_d}
(cd gcc/d; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gdc/$i.gdc
done)
(cd libphobos; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libphobos/$i.libphobos
done
cp -a src/LICENSE*.txt libdruntime/LICENSE.txt ../rpm.doc/libphobos/)
%endif
%if %{build_m2}
(cd gcc/m2; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gm2/$i.gm2
done)
(cd libgm2; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libgm2/$i.libgm2
done)
%endif
%if %{build_cobol}
(cd gcc/cobol; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gcobol/$i.gcobol
done)
(cd libgcobol; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libgcobol/$i.libgcobol
done)
%endif
%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done;
sed -n '/==========/,/==========/{/==========/d;s/^ \* *//p}' math/cosq.c \
  > ../rpm.doc/libquadmath/LICENSE.SunPro)
%endif
%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif
%if %{build_go}
(cd gcc/go; for i in README* ChangeLog*; do
	cp -p $i ../../rpm.doc/go/$i
done)
(cd libgo; for i in LICENSE* PATENTS* README; do
	cp -p $i ../rpm.doc/libgo/$i.libgo
done)
%endif
(cd gcc/doc/libgdiagnostics; make html; \
mv _build/html ../../../rpm.doc/libgdiagnostics-devel/html )

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%if %{build_annobin_plugin}
mkdir annobin-plugin
cd annobin-plugin
tar xf %{_usrsrc}/annobin/latest-annobin.tar.xz
cd annobin*
touch aclocal.m4 configure Makefile.in */configure */config.h.in */Makefile.in
ANNOBIN_FLAGS=../../obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags
ANNOBIN_CFLAGS1="%build_cflags -I %{_builddir}/gcc-%{version}-%{DATE}/gcc"
ANNOBIN_CFLAGS1="$ANNOBIN_CFLAGS1 -I %{_builddir}/gcc-%{version}-%{DATE}/obj-%{gcc_target_platform}/gcc"
ANNOBIN_CFLAGS2="-I %{_builddir}/gcc-%{version}-%{DATE}/include -I %{_builddir}/gcc-%{version}-%{DATE}/libcpp/include"
ANNOBIN_LDFLAGS="%build_ldflags -L%{_builddir}/gcc-%{version}-%{DATE}/obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/src/.libs"
CC="`$ANNOBIN_FLAGS --build-cc`" CXX="`$ANNOBIN_FLAGS --build-cxx`" \
  CFLAGS="$ANNOBIN_CFLAGS1 $ANNOBIN_CFLAGS2 $ANNOBIN_LDFLAGS" \
  CXXFLAGS="$ANNOBIN_CFLAGS1 `$ANNOBIN_FLAGS --build-includes` $ANNOBIN_CFLAGS2 $ANNOBIN_LDFLAGS" \
  ./configure --with-gcc-plugin-dir=%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin \
	      --without-annocheck --without-tests --without-docs --disable-rpath --without-debuginfod \
	      --without-clang-plugin --without-llvm-plugin
make
cd ../..
%endif

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}

# RISC-V ABI wants to install everything in /lib64/lp64d or /usr/lib64/lp64d.
# Make these be symlinks to /lib64 or /usr/lib64 respectively. See:
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/DRHT5YTPK4WWVGL3GIN5BF2IKX2ODHZ3/
%ifarch riscv64
for d in %{buildroot}%{_libdir} %{buildroot}/%{_lib} \
	  %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib} \
	  %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/%{_lib}; do
  mkdir -p $d
  (cd $d && ln -sf . lp64d)
done
%endif

%if %{build_offload_nvptx}
cd nvptx-tools-%{nvptx_tools_gitrev}
cd obj-%{gcc_target_platform}
make install prefix=%{buildroot}%{_prefix}
cd ../..

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
cd obj-offload-nvptx-none
make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
rm -rf %{buildroot}%{_prefix}/libexec/gcc/nvptx-none/%{gcc_major}/install-tools
rm -rf %{buildroot}%{_prefix}/libexec/gcc/nvptx-none/%{gcc_major}/g++-mapper-server
rm -rf %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/{install-tools,plugin,cc1,cc1plus,f951}
rm -rf %{buildroot}%{_infodir} %{buildroot}%{_mandir}/man7 %{buildroot}%{_prefix}/share/locale
rm -rf %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/{install-tools,plugin}
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/{install-tools,plugin,include-fixed}
rm -rf %{buildroot}%{_prefix}/%{_lib}/libc[cp]1*
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/nvptx-none/lib/mgomp/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/mgomp/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/
mv -f %{buildroot}%{_prefix}/lib/gcc/nvptx-none/%{gcc_major}/mgomp/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none/mgomp/
find %{buildroot}%{_prefix}/lib/gcc/nvptx-none %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none \
     %{buildroot}%{_prefix}/nvptx-none/lib -name \*.la | xargs rm
cd ..
rm -f newlib
%endif

%if %{build_offload_amdgcn}
mkdir -p %{buildroot}%{_prefix}/bin %{buildroot}%{_prefix}/amdgcn-amdhsa/bin
ln -sf llvm-ar %{buildroot}%{_prefix}/bin/amdgcn-amdhsa-ar
ln -sf llvm-ar %{buildroot}%{_prefix}/bin/amdgcn-amdhsa-ranlib
ln -sf llvm-mc %{buildroot}%{_prefix}/bin/amdgcn-amdhsa-as
ln -sf llvm-nm %{buildroot}%{_prefix}/bin/amdgcn-amdhsa-nm
ln -sf lld %{buildroot}%{_prefix}/bin/amdgcn-amdhsa-ld
ln -sf ../../bin/amdgcn-amdhsa-ar %{buildroot}%{_prefix}/amdgcn-amdhsa/bin/ar
ln -sf ../../bin/amdgcn-amdhsa-ranlib %{buildroot}%{_prefix}/amdgcn-amdhsa/bin/ranlib
ln -sf ../../bin/amdgcn-amdhsa-as %{buildroot}%{_prefix}/amdgcn-amdhsa/bin/as
ln -sf ../../bin/amdgcn-amdhsa-nm %{buildroot}%{_prefix}/amdgcn-amdhsa/bin/nm
ln -sf ../../bin/amdgcn-amdhsa-ld %{buildroot}%{_prefix}/amdgcn-amdhsa/bin/ld

ln -sf newlib-cygwin-%{newlib_cygwin_gitrev}/newlib newlib
cd obj-offload-amdgcn-amdhsa
make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
rm -rf %{buildroot}%{_prefix}/libexec/gcc/amdgcn-amdhsa/%{gcc_major}/install-tools
rm -rf %{buildroot}%{_prefix}/libexec/gcc/amdgcn-amdhsa/%{gcc_major}/g++-mapper-server
rm -rf %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa/{install-tools,plugin,cc1,cc1plus,f951}
rm -rf %{buildroot}%{_infodir} %{buildroot}%{_mandir}/man7 %{buildroot}%{_prefix}/share/locale
rm -rf %{buildroot}%{_prefix}/lib/gcc/amdgcn-amdhsa/%{gcc_major}/{install-tools,plugin}
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa/{install-tools,plugin,include-fixed}
rm -rf %{buildroot}%{_prefix}/%{_lib}/libc[cp]1*
mv -f %{buildroot}%{_prefix}/amdgcn-amdhsa/lib/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa/
mv -f %{buildroot}%{_prefix}/lib/gcc/amdgcn-amdhsa/%{gcc_major}/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa/
pushd %{buildroot}%{_prefix}/amdgcn-amdhsa/lib
for i in gfx*; do
mv -f %{buildroot}%{_prefix}/amdgcn-amdhsa/lib/$i/*.{a,spec} %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa/$i/
mv -f %{buildroot}%{_prefix}/lib/gcc/amdgcn-amdhsa/%{gcc_major}/$i/*.a %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa/$i/
done
popd
find %{buildroot}%{_prefix}/lib/gcc/amdgcn-amdhsa %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa \
     %{buildroot}%{_prefix}/amdgcn-amdhsa/lib -name \*.la | xargs rm
cd ..
rm -f newlib
%endif

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install
%if %{build_ada}
chmod 644 %{buildroot}%{_infodir}/gnat*
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}

%if %{build_isl}
cp -a isl-install/lib/libisl.so.23 $FULLPATH/
%endif

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
rm -f %{buildroot}%{_prefix}/lib/cpp
ln -sf ../bin/cpp %{buildroot}/%{_prefix}/lib/cpp
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
%if %{build_ada}
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc
%endif
mkdir -p %{buildroot}%{_fmoddir}

%if %{build_go}
mv %{buildroot}%{_prefix}/bin/go{,.gcc}
mv %{buildroot}%{_prefix}/bin/gofmt{,.gcc}
ln -sf /etc/alternatives/go %{buildroot}%{_prefix}/bin/go
ln -sf /etc/alternatives/gofmt %{buildroot}%{_prefix}/bin/gofmt
%endif

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
done

# Nuke bits/*.h.gch dirs
# 1) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 2) there are multilib issues, conflicts etc. with this
# 3) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_major}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ -o -name \*.orig | xargs rm -f
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc ppc64 ppc64p7
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif

FULLLSUBDIR=
%ifarch sparcv9 ppc
FULLLSUBDIR=lib32
%endif
%ifarch sparc64 ppc64 ppc64p7
FULLLSUBDIR=lib64
%endif
if [ -n "$FULLLSUBDIR" ]; then
  FULLLPATH=$FULLPATH/$FULLLSUBDIR
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

mv %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/
%if %{build_d}
mv %{buildroot}%{_prefix}/%{_lib}/libgphobos.spec $FULLPATH/
%endif
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif
%if %{build_cobol}
mv %{buildroot}%{_prefix}/%{_lib}/libgcobol.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_major}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
%ifarch %{ix86} x86_64 ppc ppc64 ppc64p7 ppc64le %{arm} aarch64 riscv64
rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%else
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%endif
%ifarch sparcv9 ppc
%ifarch ppc
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -m64 -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /lib64/libgcc_s.so.1 libgcc.a )' > $FULLPATH/64/libgcc_s.so
%else
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%endif
%ifarch %{multilib_64_archs}
%ifarch x86_64 ppc64 ppc64p7
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
OUTPUT_FORMAT('`gcc -m32 -Wl,--print-output-format -nostdlib -r -o /dev/null`')
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%else
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/

%if %{build_ada}
mv -f $FULLPATH/adalib/libgnarl-*.so %{buildroot}%{_prefix}/%{_lib}/
mv -f $FULLPATH/adalib/libgnat-*.so %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/adalib/libgnarl.so* $FULLPATH/adalib/libgnat.so*
%endif

mkdir -p %{buildroot}%{_prefix}/libexec/getconf
if gcc/xgcc -B gcc/ -E -P -dD -xc /dev/null | grep '__LONG_MAX__.*\(2147483647\|0x7fffffff\($\|[LU]\)\)'; then
  ln -sf POSIX_V6_ILP32_OFF32 %{buildroot}%{_prefix}/libexec/getconf/default
else
  ln -sf POSIX_V6_LP64_OFF64 %{buildroot}%{_prefix}/libexec/getconf/default
fi

mkdir -p %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++*gdb.py* \
      %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
%py_byte_compile %{python3} %{buildroot}%{_prefix}/share/gcc-%{gcc_major}/python/
%py_byte_compile %{python3} %{buildroot}%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/

rm -f $FULLEPATH/libgccjit.so
cp -a objlibgccjit/gcc/libgccjit.so* %{buildroot}%{_prefix}/%{_lib}/
cp -a ../gcc/jit/libgccjit*.h %{buildroot}%{_prefix}/include/
/usr/bin/install -c -m 644 objlibgccjit/gcc/doc/libgccjit.info %{buildroot}/%{_infodir}/
gzip -9 %{buildroot}/%{_infodir}/libgccjit.info

rm -f $FULLEPATH/libgdiagnostics.so
cp -a objlibgccjit/gcc/libgdiagnostics.so* %{buildroot}%{_prefix}/%{_lib}/
cp -a ../gcc/libgdiagnostics*.h %{buildroot}%{_prefix}/include/
cp -a objlibgccjit/gcc/sarif-replay %{buildroot}%{_prefix}/bin/

sed -e 's,\.\./include/,../../../../include/,' \
  %{buildroot}%{_prefix}/%{_lib}/libstdc++.modules.json \
  > $FULLPATH/libstdc++.modules.json

pushd $FULLPATH
if [ "%{_lib}" = "lib" ]; then
%if %{build_objc}
ln -sf ../../../libobjc.so.4 libobjc.so
%endif
ln -sf ../../../libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../libgfortran.so.5.* libgfortran.so
ln -sf ../../../libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../libgo.so.24.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../libquadmath.so.0.* libquadmath.so
%endif
%if %{build_d}
ln -sf ../../../libgdruntime.so.6.* libgdruntime.so
ln -sf ../../../libgphobos.so.6.* libgphobos.so
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf ../../../libm2$i.so.20.* libm2$i.so
done
%endif
%if %{build_cobol}
ln -sf ../../../libgcobol.so.1.* libgcobol.so
%endif
%if %{build_libitm}
ln -sf ../../../libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../libasan.so.8.* libasan.so
mv ../../../libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../libubsan.so.1.* libubsan.so
%endif
else
%if %{build_objc}
ln -sf ../../../../%{_lib}/libobjc.so.4 libobjc.so
%endif
ln -sf ../../../../%{_lib}/libstdc++.so.6.*[0-9] libstdc++.so
ln -sf ../../../../%{_lib}/libgfortran.so.5.* libgfortran.so
ln -sf ../../../../%{_lib}/libgomp.so.1.* libgomp.so
%if %{build_go}
ln -sf ../../../../%{_lib}/libgo.so.24.* libgo.so
%endif
%if %{build_libquadmath}
ln -sf ../../../../%{_lib}/libquadmath.so.0.* libquadmath.so
%endif
%if %{build_d}
ln -sf ../../../../%{_lib}/libgdruntime.so.6.* libgdruntime.so
ln -sf ../../../../%{_lib}/libgphobos.so.6.* libgphobos.so
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf ../../../../%{_lib}/libm2$i.so.20.* libm2$i.so
done
%endif
%if %{build_cobol}
ln -sf ../../../../%{_lib}/libgcobol.so.1.* libgcobol.so
%endif
%if %{build_libitm}
ln -sf ../../../../%{_lib}/libitm.so.1.* libitm.so
%endif
%if %{build_libatomic}
ln -sf ../../../../%{_lib}/libatomic.so.1.* libatomic.so
%endif
%if %{build_libasan}
ln -sf ../../../../%{_lib}/libasan.so.8.* libasan.so
mv ../../../../%{_lib}/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../../%{_lib}/libubsan.so.1.* libubsan.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libtsan.so.2.* | sed 's,^.*libt,libt,'`' )' > libtsan.so
mv ../../../../%{_lib}/libtsan_preinit.o libtsan_preinit.o
%endif
%if %{build_libhwasan}
rm -f libhwasan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/libhwasan.so.0.* | sed 's,^.*libh,libh,'`' )' > libhwasan.so
mv ../../../../%{_lib}/libhwasan_preinit.o libhwasan_preinit.o
%endif
%if %{build_liblsan}
rm -f liblsan.so
echo 'INPUT ( %{_prefix}/%{_lib}/'`echo ../../../../%{_lib}/liblsan.so.0.* | sed 's,^.*libl,libl,'`' )' > liblsan.so
mv ../../../../%{_lib}/liblsan_preinit.o liblsan_preinit.o
%endif
fi
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++exp.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a $FULLLPATH/
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/%{_lib}/libobjc.*a .
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_d}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgdruntime.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgphobos.*a $FULLLPATH/
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  mv -f %{buildroot}%{_prefix}/%{_lib}/libm2$i.*a $FULLLPATH/
  rm -f m2/m2$i/*.{a,la}
  ln -sf ../../libm2$i.so m2/m2$i/
  ln -sf ../../libm2$i.a m2/m2$i/
done
%endif
%if %{build_cobol}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcobol.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
%endif
%if %{build_libubsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libubsan.*a $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLPATH/
%endif
%if %{build_libhwasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libhwasan.*a $FULLPATH/
%endif
%if %{build_liblsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLPATH/
%endif
%if %{build_go}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgo.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgobegin.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libgolibbegin.*a $FULLLPATH/
%endif

%if %{build_ada}
%ifarch sparcv9 ppc
rm -rf $FULLPATH/64/ada{include,lib}
%endif
%ifarch %{multilib_64_archs}
rm -rf $FULLPATH/32/ada{include,lib}
%endif
if [ "$FULLPATH" != "$FULLLPATH" ]; then
mv -f $FULLPATH/ada{include,lib} $FULLLPATH/
pushd $FULLLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../../libgnarl-*.so libgnarl-%{gcc_major}.so
ln -sf ../../../../../libgnat-*.so libgnat.so
ln -sf ../../../../../libgnat-*.so libgnat-%{gcc_major}.so
else
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../../%{_lib}/libgnarl-*.so libgnarl-%{gcc_major}.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../../%{_lib}/libgnat-*.so libgnat-%{gcc_major}.so
fi
popd
else
pushd $FULLPATH/adalib
if [ "%{_lib}" = "lib" ]; then
ln -sf ../../../../libgnarl-*.so libgnarl.so
ln -sf ../../../../libgnarl-*.so libgnarl-%{gcc_major}.so
ln -sf ../../../../libgnat-*.so libgnat.so
ln -sf ../../../../libgnat-*.so libgnat-%{gcc_major}.so
else
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl.so
ln -sf ../../../../../%{_lib}/libgnarl-*.so libgnarl-%{gcc_major}.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat.so
ln -sf ../../../../../%{_lib}/libgnat-*.so libgnat-%{gcc_major}.so
fi
popd
fi
%endif

%ifarch sparcv9 ppc
%if %{build_objc}
ln -sf ../../../../../lib64/libobjc.so.4 64/libobjc.so
%endif
ln -sf ../`echo ../../../../lib/libstdc++.so.6.*[0-9] | sed s~/lib/~/lib64/~` 64/libstdc++.so
ln -sf ../`echo ../../../../lib/libgfortran.so.5.* | sed s~/lib/~/lib64/~` 64/libgfortran.so
ln -sf ../`echo ../../../../lib/libgomp.so.1.* | sed s~/lib/~/lib64/~` 64/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgo.so.24.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgo.so.24.* | sed 's,^.*libg,libg,'`' )' > 64/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 64/libquadmath.so
%endif
%if %{build_d}
rm -f libgdruntime.so libgphobos.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgdruntime.so.6.* | sed 's,^.*libg,libg,'`' )' > libgdruntime.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgdruntime.so.6.* | sed 's,^.*libg,libg,'`' )' > 64/libgdruntime.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgphobos.so.6.* | sed 's,^.*libg,libg,'`' )' > libgphobos.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgphobos.so.6.* | sed 's,^.*libg,libg,'`' )' > 64/libgphobos.so
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  rm -f libm2$i.so
  echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libm2$i.so.20.* | sed 's,^.*libm,libm,'`' )' > libm2$i.so
  echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libm2$i.so.20.* | sed 's,^.*libm,libm,'`' )' > 64/libm2$i.so
  rm -f 64/m2/m2$i/*.{a,la}
  ln -sf ../../libm2$i.so 64/m2/m2$i/
  ln -sf ../../libm2$i.a 64/m2/m2$i/
done
%endif
%if %{build_cobol}
rm -f libgcobol.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libgcobol.so.1.* | sed 's,^.*libg,libg,'`' )' > libgcobol.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libgcobol.so.1.* | sed 's,^.*libg,libg,'`' )' > 64/libgcobol.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 64/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libasan.so.8.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libasan.so.8.* | sed 's,^.*liba,liba,'`' )' > 64/libasan.so
mv ../../../../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > 64/libubsan.so
%endif
ln -sf lib32/libgfortran.a libgfortran.a
ln -sf ../lib64/libgfortran.a 64/libgfortran.a
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/lib64/libobjc.*a 64/
%endif
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++fs.a libstdc++fs.a
ln -sf ../lib64/libstdc++fs.a 64/libstdc++fs.a
ln -sf lib32/libstdc++exp.a libstdc++exp.a
ln -sf ../lib64/libstdc++exp.a 64/libstdc++exp.a
ln -sf lib32/libsupc++.a libsupc++.a
ln -sf ../lib64/libsupc++.a 64/libsupc++.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_d}
ln -sf lib32/libgdruntime.a libgdruntime.a
ln -sf ../lib64/libgdruntime.a 64/libgdruntime.a
ln -sf lib32/libgphobos.a libgphobos.a
ln -sf ../lib64/libgphobos.a 64/libgphobos.a
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf lib32/libm2$i.a libm2$i.a
  ln -sf ../lib64/libm2$i.a 64/libm2$i.a
done
%endif
%if %{build_cobol}
ln -sf lib32/libgcobol.a libgcobol.a
ln -sf ../lib64/libgcobol.a 64/libgcobol.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libasan}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
%endif
%if %{build_libubsan}
ln -sf lib32/libubsan.a libubsan.a
ln -sf ../lib64/libubsan.a 64/libubsan.a
%endif
%if %{build_go}
ln -sf lib32/libgo.a libgo.a
ln -sf ../lib64/libgo.a 64/libgo.a
ln -sf lib32/libgobegin.a libgobegin.a
ln -sf ../lib64/libgobegin.a 64/libgobegin.a
ln -sf lib32/libgolibbegin.a libgolibbegin.a
ln -sf ../lib64/libgolibbegin.a 64/libgolibbegin.a
%endif
%if %{build_ada}
ln -sf lib32/adainclude adainclude
ln -sf ../lib64/adainclude 64/adainclude
ln -sf lib32/adalib adalib
ln -sf ../lib64/adalib 64/adalib
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
%if %{build_objc}
ln -sf ../../../../libobjc.so.4 32/libobjc.so
%endif
ln -sf ../`echo ../../../../lib64/libstdc++.so.6.*[0-9] | sed s~/../lib64/~/~` 32/libstdc++.so
ln -sf ../`echo ../../../../lib64/libgfortran.so.5.* | sed s~/../lib64/~/~` 32/libgfortran.so
ln -sf ../`echo ../../../../lib64/libgomp.so.1.* | sed s~/../lib64/~/~` 32/libgomp.so
%if %{build_go}
rm -f libgo.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgo.so.24.* | sed 's,^.*libg,libg,'`' )' > libgo.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgo.so.24.* | sed 's,^.*libg,libg,'`' )' > 32/libgo.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > libquadmath.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libquadmath.so.0.* | sed 's,^.*libq,libq,'`' )' > 32/libquadmath.so
%endif
%if %{build_d}
rm -f libgdruntime.so libgphobos.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgdruntime.so.6.* | sed 's,^.*libg,libg,'`' )' > libgdruntime.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgdruntime.so.6.* | sed 's,^.*libg,libg,'`' )' > 32/libgdruntime.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgphobos.so.6.* | sed 's,^.*libg,libg,'`' )' > libgphobos.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgphobos.so.6.* | sed 's,^.*libg,libg,'`' )' > 32/libgphobos.so
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  rm -f libm2$i.so
  echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libm2$i.so.20.* | sed 's,^.*libm,libm,'`' )' > libm2$i.so
  echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libm2$i.so.20.* | sed 's,^.*libm,libm,'`' )' > 32/libm2$i.so
  rm -f 32/m2/m2$i/*.{a,la}
  ln -sf ../../libm2$i.so 32/m2/m2$i/
  ln -sf ../../libm2$i.a 32/m2/m2$i/
done
%endif
%if %{build_cobol}
rm -f libgcobol.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libgcobol.so.1.* | sed 's,^.*libg,libg,'`' )' > libgcobol.so
#echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libgcobol.so.1.* | sed 's,^.*libg,libg,'`' )' > 32/libgcobol.so
%endif
%if %{build_libitm}
rm -f libitm.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > libitm.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libitm.so.1.* | sed 's,^.*libi,libi,'`' )' > 32/libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > libatomic.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libatomic.so.1.* | sed 's,^.*liba,liba,'`' )' > 32/libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libasan.so.8.* | sed 's,^.*liba,liba,'`' )' > libasan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libasan.so.8.* | sed 's,^.*liba,liba,'`' )' > 32/libasan.so
mv ../../../../lib/libasan_preinit.o 32/libasan_preinit.o
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo 'INPUT ( %{_prefix}/lib64/'`echo ../../../../lib64/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > libubsan.so
echo 'INPUT ( %{_prefix}/lib/'`echo ../../../../lib64/libubsan.so.1.* | sed 's,^.*libu,libu,'`' )' > 32/libubsan.so
%endif
%if %{build_objc}
mv -f %{buildroot}%{_prefix}/lib/libobjc.*a 32/
%endif
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%endif
%ifarch sparc64 ppc64 ppc64p7
ln -sf ../lib32/libgfortran.a 32/libgfortran.a
ln -sf lib64/libgfortran.a libgfortran.a
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++fs.a 32/libstdc++fs.a
ln -sf lib64/libstdc++fs.a libstdc++fs.a
ln -sf ../lib32/libstdc++exp.a 32/libstdc++exp.a
ln -sf lib64/libstdc++exp.a libstdc++exp.a
ln -sf ../lib32/libsupc++.a 32/libsupc++.a
ln -sf lib64/libsupc++.a libsupc++.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_d}
ln -sf ../lib32/libgdruntime.a 32/libgdruntime.a
ln -sf lib64/libgdruntime.a libgdruntime.a
ln -sf ../lib32/libgphobos.a 32/libgphobos.a
ln -sf lib64/libgphobos.a libgphobos.a
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf ../lib32/libm2$i.a 32/libm2$i.a
  ln -sf lib64/libm2$i.a libm2$i.a
done
%endif
%if %{build_cobol}
ln -sf ../lib32/libgcobol.a 32/libgcobol.a
ln -sf lib64/libgcobol.a libgcobol.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libasan}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
%endif
%if %{build_libubsan}
ln -sf ../lib32/libubsan.a 32/libubsan.a
ln -sf lib64/libubsan.a libubsan.a
%endif
%if %{build_go}
ln -sf ../lib32/libgo.a 32/libgo.a
ln -sf lib64/libgo.a libgo.a
ln -sf ../lib32/libgobegin.a 32/libgobegin.a
ln -sf lib64/libgobegin.a libgobegin.a
ln -sf ../lib32/libgolibbegin.a 32/libgolibbegin.a
ln -sf lib64/libgolibbegin.a libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../lib32/adainclude 32/adainclude
ln -sf lib64/adainclude adainclude
ln -sf ../lib32/adalib 32/adalib
ln -sf lib64/adalib adalib
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgfortran.a 32/libgfortran.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++fs.a 32/libstdc++fs.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libstdc++exp.a 32/libstdc++exp.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libsupc++.a 32/libsupc++.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_d}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgdruntime.a 32/libgdruntime.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgphobos.a 32/libgphobos.a
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libm2$i.a 32/libm2$i.a
done
%endif
%if %{build_cobol}
#ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgcobol.a 32/libgcobol.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libasan.a 32/libasan.a
%endif
%if %{build_libubsan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libubsan.a 32/libubsan.a
%endif
%if %{build_go}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgo.a 32/libgo.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgobegin.a 32/libgobegin.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/libgolibbegin.a 32/libgolibbegin.a
%endif
%if %{build_ada}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adainclude 32/adainclude
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}/%{gcc_major}/adalib 32/adalib
%endif
%endif
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
# if 0%{?_enable_debug_packages}
%if 0
for d in . $FULLLSUBDIR; do
  mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d
  for f in `find $d -maxdepth 1 -a \
		\( -name libasan.a -o -name libatomic.a \
		-o -name libcaf_single.a \
		-o -name libgcc.a -o -name libgcc_eh.a \
		-o -name libgcov.a -o -name libgfortran.a \
		-o -name libgo.a -o -name libgobegin.a \
		-o -name libgolibbegin.a -o -name libgomp.a \
		-o -name libitm.a -o -name liblsan.a \
		-o -name libobjc.a -o -name libgdruntime.a -o -name libgphobos.a \
		-o -name libm2\*.a -o -name libquadmath.a -o -name libstdc++.a \
		-o -name libstdc++fs.a -o -name libstdc++exp.a \
		-o -name libsupc++.a -o -name libgcobol.a \
		-o -name libtsan.a -o -name libubsan.a \) -a -type f`; do
    cp -a $f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/$d/
  done
done
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a -o -name libobjc.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a -o -name libquadmath.a \
		    -o -name libgdruntime.a -o -name libgphobos.a -o -name libm2\*.a \
		    -o -name libitm.a -o -name libgo.a -o -name libcaf\*.a \
		    -o -name libatomic.a -o -name libasan.a -o -name libtsan.a \
		    -o -name libubsan.a -o -name liblsan.a -o -name libcc1.a \
		    -o -name libgcobol.a \) \
		 -a -type f`
popd
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.5.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
%if %{build_libquadmath}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%if %{build_d}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgdruntime.so.6.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgphobos.so.6.*
%endif
%if %{build_m2}
for i in cor iso log min pim; do
  chmod 755 %{buildroot}%{_prefix}/%{_lib}/libm2$i.so.20.*
done
%endif
%if %{build_cobol}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgcobol.so.1.*
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.8.*
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.1.*
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.2.*
%endif
%if %{build_libhwasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libhwasan.so.0.*
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%endif
%if %{build_go}
# Avoid stripping these libraries and binaries.
chmod 644 %{buildroot}%{_prefix}/%{_lib}/libgo.so.24.*
chmod 644 %{buildroot}%{_prefix}/bin/go.gcc
chmod 644 %{buildroot}%{_prefix}/bin/gofmt.gcc
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json
chmod 644 %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet
%endif
%if %{build_objc}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libobjc.so.4.*
%endif

%if %{build_ada}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnarl*so*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgnat*so*
%endif

for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cat > %{buildroot}%{_prefix}/bin/c89 <<"EOF"
#!/bin/sh
fl="-std=c89"
for opt; do
  case "$opt" in
    -ansi|-std=c89|-std=iso9899:1990) fl="";;
    -std=*) echo "`basename $0` called with non ANSI/ISO C option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
cat > %{buildroot}%{_prefix}/bin/c99 <<"EOF"
#!/bin/sh
fl="-std=c99"
for opt; do
  case "$opt" in
    -std=c99|-std=iso9899:1999) fl="";;
    -std=*) echo "`basename $0` called with non ISO C99 option $opt" >&2
	    exit 1;;
  esac
done
exec gcc $fl ${1+"$@"}
EOF
chmod 755 %{buildroot}%{_prefix}/bin/c?9

cd ..
%find_lang %{name}
%find_lang cpplib

# Remove binaries we will not be including, so that they don't end up in
# gcc-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a} || :
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gccgo || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcj || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ar || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-nm || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcc-ranlib || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gdc || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gm2 || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcobc || :
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gcobol || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%ifnarch sparc64 ppc64 ppc64p7
ln -sf %{multilib_32_arch}-%{_vendor}-%{_target_os} %{buildroot}%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%if %{build_go}
rm -rf %{buildroot}%{_prefix}/lib64/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%endif

rm -f %{buildroot}%{_prefix}/lib*/lib*.spec || :
rm -f %{buildroot}%{_prefix}/lib*/libstdc++.modules.json || :
rm -f %{buildroot}%{_prefix}/%{_lib}/lib{asan,atomic,gcc_s,gcobol,gdruntime,gfortran,go,gomp-plugin-*,gomp,gphobos,hwasan}.so || :
rm -f %{buildroot}%{_prefix}/%{_lib}/lib{itm,lsan,m2{cor,iso,log,min,pim},objc,quadmath,stdc++,tsan,ubsan}.so || :
rm -f %{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/install-tools/{fixinc.sh,mkinstalldirs} || :
rm -f %{buildroot}%{_prefix}/share/locale/*/LC_MESSAGES/libstdc++.mo || :
rm -f %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include-fixed/README || :
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ssp || :
rm -rf %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/install-tools || :
%ifarch ppc ppc64 ppc64le ppc64p7
rm -f %{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/{e,n}crt{i,n}.o || :
%endif

%if %{build_offload_nvptx}
rm -f %{buildroot}%{_mandir}/man1/*-accel-*nvptx*
find %{buildroot}%{_prefix}/nvptx-none/lib -name libstdc++.a-gdb.py | xargs rm -f || :
find %{buildroot}%{_prefix}/nvptx-none/lib -name libstdc++.modules.json | xargs rm -f || :
%endif
%if %{build_offload_amdgcn}
rm -f %{buildroot}%{_mandir}/man1/*-accel-*amdgcn*
find %{buildroot}%{_prefix}/amdgcn-amdhsa/lib -name libstdc++.a-gdb.py | xargs rm -f || :
find %{buildroot}%{_prefix}/amdgcn-amdhsa/lib -name libstdc++.modules.json | xargs rm -f || :
%endif
rm -f %{buildroot}%{_mandir}/man7/{gpl,gfdl,fsf-funding}.7*

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{_arch} > $FULLPATH/rpmver

# Add symlink to lto plugin in the binutils plugin directory.
%{__mkdir_p} %{buildroot}%{_libdir}/bfd-plugins/
ln -s ../../libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so \
  %{buildroot}%{_libdir}/bfd-plugins/

%if %{build_annobin_plugin}
mkdir -p $FULLPATH/plugin
rm -f $FULLPATH/plugin/gcc-annobin*
cp -a %{_builddir}/gcc-%{version}-%{DATE}/annobin-plugin/annobin*/gcc-plugin/.libs/annobin.so.0.0.0 \
  $FULLPATH/plugin/gcc-annobin.so.0.0.0
ln -sf gcc-annobin.so.0.0.0 $FULLPATH/plugin/gcc-annobin.so.0
ln -sf gcc-annobin.so.0.0.0 $FULLPATH/plugin/gcc-annobin.so
%endif

%check
cd obj-%{gcc_target_platform}

# run the tests.
LC_ALL=C make %{?_smp_mflags} -k check ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ \
%if 0%{?fedora} >= 20 || 0%{?rhel} > 7
     RUNTESTFLAGS="--target_board=unix/'{-foffload=disable,-fstack-protector-strong/-foffload=disable}'" || :
%else
     RUNTESTFLAGS="--target_board=unix/'{-foffload=disable,-fstack-protector/-foffload=disable}'" || :
%endif
%if !%{build_annobin_plugin}
if [ -f %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so ]; then
  # Test whether current annobin plugin won't fail miserably with the newly built gcc.
  echo -e '#include <stdio.h>\nint main () { printf ("Hello, world!\\n"); return 0; }' > annobin-test.c
  echo -e '#include <iostream>\nint main () { std::cout << "Hello, world!" << std::endl; return 0; }' > annobin-test.C
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc` \
  -O2 -g -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS \
  -fexceptions -fstack-protector-strong -grecord-gcc-switches -o annobin-test{c,.c} \
  -Wl,-rpath,%{gcc_target_platform}/libgcc/ \
  -fplugin=%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so \
  2> ANNOBINOUT1 || echo Annobin test 1 FAIL > ANNOBINOUT2;
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` \
  `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes` \
  -O2 -g -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS \
  -fexceptions -fstack-protector-strong -grecord-gcc-switches -o annobin-test{C,.C} \
  -Wl,-rpath,%{gcc_target_platform}/libgcc/:%{gcc_target_platform}/libstdc++-v3/src/.libs/ \
  -fplugin=%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/annobin.so \
  -B %{gcc_target_platform}/libstdc++-v3/src/.libs/ \
  2> ANNOBINOUT3 || echo Annobin test 2 FAIL > ANNOBINOUT4;
  [ -f ./annobin-testc ] || echo Annobin test 1 MISSING > ANNOBINOUT5;
  [ -f ./annobin-testc ] && \
  ( ./annobin-testc > ANNOBINRES1 2>&1 || echo Annobin test 1 RUNFAIL > ANNOBINOUT6 );
  [ -f ./annobin-testC ] || echo Annobin test 2 MISSING > ANNOBINOUT7;
  [ -f ./annobin-testC ] && \
  ( ./annobin-testC > ANNOBINRES2 2>&1 || echo Annobin test 2 RUNFAIL > ANNOBINOUT8 );
  cat ANNOBINOUT[1-8] > ANNOBINOUT
  touch ANNOBINRES1 ANNOBINRES2
  [ -s ANNOBINOUT ] && echo Annobin testing FAILed > ANNOBINRES
  cat ANNOBINOUT ANNOBINRES[12] >> ANNOBINRES
  rm -f ANNOBINOUT* ANNOBINRES[12] annobin-test{c,C}
fi
%endif
echo ====================TESTING=========================
( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
%if !%{build_annobin_plugin}
[ -f ANNOBINRES ] && cat ANNOBINRES
%endif
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | xz -9e \
  | uuencode testlogs-%{_target_platform}.tar.xz || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%post go
%{_sbindir}/update-alternatives --install \
  %{_prefix}/bin/go go %{_prefix}/bin/go.gcc 92 \
  --slave %{_prefix}/bin/gofmt gofmt %{_prefix}/bin/gofmt.gcc

%preun go
if [ $1 = 0 ]; then
  %{_sbindir}/update-alternatives --remove go %{_prefix}/bin/go.gcc
fi

%{?ldconfig:
# Because glibc Prereq's libgcc and /sbin/ldconfig
# comes from glibc, it might not exist yet when
# libgcc is installed
%post -n libgcc -p <lua>
if posix.access ("%ldconfig", "x") then
  rpm.execute ("%ldconfig")
end

%postun -n libgcc -p <lua>
if posix.access ("%ldconfig", "x") then
  rpm.execute ("%ldconfig")
end
}

%ldconfig_scriptlets -n libstdc++

%ldconfig_scriptlets -n libobjc

%ldconfig_scriptlets -n libgfortran

%ldconfig_scriptlets -n libgphobos

%ldconfig_scriptlets -n libgm2

%ldconfig_scriptlets -n libgnat

%ldconfig_scriptlets -n libgomp

%ldconfig_scriptlets gdb-plugin

%ldconfig_scriptlets -n libgccjit

%ldconfig_scriptlets -n libgdiagnostics

%ldconfig_scriptlets -n libquadmath

%ldconfig_scriptlets -n libitm

%ldconfig_scriptlets -n libatomic

%ldconfig_scriptlets -n libasan

%ldconfig_scriptlets -n libubsan

%ldconfig_scriptlets -n libtsan

%ldconfig_scriptlets -n liblsan

%ldconfig_scriptlets -n libhwasan

%ldconfig_scriptlets -n libgo

%files -f %{name}.lang
%{_prefix}/bin/cc
%{_prefix}/bin/c89
%{_prefix}/bin/c99
%{_prefix}/bin/gcc
%{_prefix}/bin/gcov
%{_prefix}/bin/gcov-tool
%{_prefix}/bin/gcov-dump
%{_prefix}/bin/gcc-ar
%{_prefix}/bin/gcc-nm
%{_prefix}/bin/gcc-ranlib
%{_prefix}/bin/lto-dump
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}-gcc
%endif
%ifarch ppc64 ppc64p7
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}-gcc
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{gcc_major}
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/gcov-tool.1*
%{_mandir}/man1/gcov-dump.1*
%{_mandir}/man1/lto-dump.1*
%{_infodir}/gcc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/liblto_plugin.so*
%{_libdir}/bfd-plugins/liblto_plugin.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/openacc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/acc_prof.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdatomic.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gcov.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/stdckdint.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pkuintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sgxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/gfniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cetintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cet.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vbmi2vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vnnivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vaesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vpclmulqdqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vpopcntdqvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bitalgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pconfigintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/wbnoinvdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/movdirintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/waitpkgintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cldemoteintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bf16vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/enqcmdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vp2intersectintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512vp2intersectvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/serializeintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tsxldtrkintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxtileintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxint8intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxbf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86gprintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/uintrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/hresetintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/keylockerintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxvnniintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mwaitintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fp16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512fp16vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxvnniint8intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxneconvertintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/cmpccxaddintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxfp16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/prfchiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/raointintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxcomplexintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx512bitalgvlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avxvnniint16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sha512intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sm3intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sm4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/usermsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxavx512intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxfp8intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxmovrsintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxtf32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amxtransposeintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2-512bf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2-512convertintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2-512mediaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2-512minmaxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2-512satcvtintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2bf16intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2convertintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2copyintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2mediaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2minmaxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/avx10_2satcvtintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/movrsintrin.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/amo.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/x86gprintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/rs6000-vecdefines.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_cmse.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_bf16.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_acle.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_fp16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_bf16.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_sve.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_sme.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_neon_sve_bridge.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_private_fp8.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/arm_private_neon_types.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/vecintrin.h
%endif
%ifarch riscv64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/riscv_vector.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/riscv_crypto.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/riscv_bitmanip.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/riscv_th_vector.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sifive_vector.h
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/sanitizer
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/collect2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsanitizer.spec
%endif
%if %{build_isl}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libisl.so.*
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libubsan.so
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgomp.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libubsan.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%endif
%else
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.so
%endif
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan_preinit.o
%endif
%if %{build_libhwasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libhwasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libhwasan_preinit.o
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan_preinit.o
%endif
%{_prefix}/libexec/getconf/default
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files -n cpp -f cpplib.lang
%{_prefix}/lib/cpp
%{_prefix}/bin/cpp
%{_mandir}/man1/cpp.1*
%{_infodir}/cpp*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1

%files -n libgcc
/%{_lib}/libgcc_s-%{gcc_major}-%{DATE}.so.1
/%{_lib}/libgcc_s.so.1
%{!?_licensedir:%global license %%doc}
%license gcc/COPYING* COPYING.RUNTIME

%files c++
%{_prefix}/bin/%{gcc_target_platform}-*++
%{_prefix}/bin/g++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1plus
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/g++-mapper-server
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++exp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n libstdc++
%{_prefix}/%{_lib}/libstdc++.so.6*
%dir %{_datadir}/gdb
%dir %{_datadir}/gdb/auto-load
%dir %{_datadir}/gdb/auto-load/%{_prefix}
%dir %{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/
# Package symlink to keep compatibility
%ifarch riscv64
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/lp64d
%endif
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/libstdc*gdb.py*
%{_datadir}/gdb/auto-load/%{_prefix}/%{_lib}/__pycache__
%dir %{_prefix}/share/gcc-%{gcc_major}
%dir %{_prefix}/share/gcc-%{gcc_major}/python
%{_prefix}/share/gcc-%{gcc_major}/python/libstdcxx

%files -n libstdc++-devel
%dir %{_prefix}/include/c++
%{_prefix}/include/c++/%{gcc_major}
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.modules.json
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++exp.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++exp.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++exp.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%files -n libstdc++-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libsupc++.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libsupc++.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libsupc++.a
%endif

%if %{build_libstdcxx_docs}
%files -n libstdc++-docs
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_objc}
%files objc
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/objc
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1obj
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libobjc.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libobjc.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libobjc.so
%endif
%doc rpm.doc/objc/*
%doc libobjc/THREADS* rpm.doc/changelogs/libobjc/ChangeLog*

%files objc++
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1objplus

%files -n libobjc
%{_prefix}/%{_lib}/libobjc.so.4*
%endif

%files gfortran
%{_prefix}/bin/gfortran
%{_prefix}/bin/f95
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/ISO_Fortran_binding.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libcaf_single.a
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/finclude
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/finclude
%endif
%dir %{_fmoddir}
%doc rpm.doc/gfortran/*

%files -n libgfortran
%{_prefix}/%{_lib}/libgfortran.so.5*

%files -n libgfortran-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgfortran.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgfortran.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgfortran.a
%endif

%if %{build_d}
%files gdc
%{_prefix}/bin/gdc
%{_mandir}/man1/gdc.1*
%{_infodir}/gdc*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/d
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/d21
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.spec
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgphobos.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgphobos.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgphobos.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgdruntime.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgphobos.so
%endif
%doc rpm.doc/gdc/*

%files -n libgphobos
%{_prefix}/%{_lib}/libgdruntime.so.6*
%{_prefix}/%{_lib}/libgphobos.so.6*
%doc rpm.doc/libphobos/*

%files -n libgphobos-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgphobos.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgphobos.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgdruntime.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgphobos.a
%endif
%endif

%if %{build_m2}
%files gm2
%{_prefix}/bin/gm2
%{_mandir}/man1/gm2.1*
%{_infodir}/m2*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/m2
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cc1gm2
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libm2*.a
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libm2*.so
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/m2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libm2*.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libm2*.so
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/m2
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libm2*.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libm2*.so
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/m2rte.so
%doc rpm.doc/gm2/*

%files -n libgm2
%{_prefix}/%{_lib}/libm2*.so.20*
%doc rpm.doc/libgm2/*

%files -n libgm2-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libm2*.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libm2*.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libm2*.a
%endif
%endif

%if %{build_cobol}
%files gcobol
%{_prefix}/bin/gcobol
%{_prefix}/bin/gcobc
%{_mandir}/man1/gcobol.1*
%{_mandir}/man3/gcobol-io.3*
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cobol1
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcobol.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcobol.so
%{_datadir}/gcobol
%doc rpm.doc/gcobol/*

%files -n libgcobol
%{_prefix}/%{_lib}/libgcobol.so.1*
%doc rpm.doc/libgcobol/*

%files -n libgcobol-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgcobol.a
%endif

%if %{build_ada}
%files gnat
%{_prefix}/bin/gnat
%{_prefix}/bin/gnat[^i]*
%{_infodir}/gnat*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/ada_target_properties
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/ada_target_properties
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/ada_target_properties
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/gnat1
%doc rpm.doc/changelogs/gcc/ada/ChangeLog*

%files -n libgnat
%{_prefix}/%{_lib}/libgnat-*.so
%{_prefix}/%{_lib}/libgnarl-*.so

%files -n libgnat-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adainclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnat.a
%exclude %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnarl.a
%endif

%files -n libgnat-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/adalib/libgnarl.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/adalib/libgnarl.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnat.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/adalib/libgnarl.a
%endif
%endif

%files -n libgomp
%{_prefix}/%{_lib}/libgomp.so.1*
%{_infodir}/libgomp.info*
%doc rpm.doc/changelogs/libgomp/ChangeLog*

%if %{build_libquadmath}
%files -n libquadmath
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%{!?_licensedir:%global license %%doc}
%license rpm.doc/libquadmath/COPYING*

%files -n libquadmath-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include/quadmath_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*

%files -n libquadmath-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libquadmath.a
%endif
%endif

%if %{build_libitm}
%files -n libitm
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%files -n libitm-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/include
#%%{_prefix}/lib/gcc/%%{gcc_target_platform}/%%{gcc_major}/include/itm.h
#%%{_prefix}/lib/gcc/%%{gcc_target_platform}/%%{gcc_major}/include/itm_weak.h
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.so
%endif
%doc rpm.doc/libitm/ChangeLog*

%files -n libitm-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libitm.a
%endif
%endif

%if %{build_libatomic}
%files -n libatomic
%{_prefix}/%{_lib}/libatomic.so.1*

%files -n libatomic-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan
%{_prefix}/%{_lib}/libasan.so.8*

%files -n libasan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libasan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libasan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libasan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libubsan}
%files -n libubsan
%{_prefix}/%{_lib}/libubsan.so.1*

%files -n libubsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libubsan.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libubsan.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libubsan.a
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%{_prefix}/%{_lib}/libtsan.so.2*

%files -n libtsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_libhwasan}
%files -n libhwasan
%{_prefix}/%{_lib}/libhwasan.so.0*

%files -n libhwasan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libhwasan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_liblsan}
%files -n liblsan
%{_prefix}/%{_lib}/liblsan.so.0*

%files -n liblsan-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/liblsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog*
%{!?_licensedir:%global license %%doc}
%license libsanitizer/LICENSE.TXT
%endif

%if %{build_go}
%files go
%ghost %{_prefix}/bin/go
%attr(755,root,root) %{_prefix}/bin/go.gcc
%{_prefix}/bin/gccgo
%ghost %{_prefix}/bin/gofmt
%attr(755,root,root) %{_prefix}/bin/gofmt.gcc
%{_mandir}/man1/gccgo.1*
%{_mandir}/man1/go.1*
%{_mandir}/man1/gofmt.1*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/go1
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/cgo
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/buildid
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/test2json
%attr(755,root,root) %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/vet
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/64/libgolibbegin.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgo.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/32/libgolibbegin.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%endif
%ifarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%endif
%doc rpm.doc/go/*

%files -n libgo
%{_prefix}/%{_lib}/libgo.so.24
%attr(755,root,root) %{_prefix}/%{_lib}/libgo.so.24.*
%doc rpm.doc/libgo/*

%files -n libgo-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/%{_lib}/go
%dir %{_prefix}/%{_lib}/go/%{gcc_major}
%{_prefix}/%{_lib}/go/%{gcc_major}/%{gcc_target_platform}
%ifarch %{multilib_64_archs}
%ifnarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/go
%dir %{_prefix}/lib/go/%{gcc_major}
%{_prefix}/lib/go/%{gcc_major}/%{gcc_target_platform}
%endif
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgolibbegin.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgolibbegin.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgobegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgolibbegin.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.so
%endif

%files -n libgo-static
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib32/libgo.a
%endif
%ifarch sparc64 ppc64 ppc64p7
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/lib64/libgo.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64 ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgo.a
%endif
%endif

%files -n libgccjit
%{_prefix}/%{_lib}/libgccjit.so.*
%doc rpm.doc/changelogs/gcc/jit/ChangeLog*

%files -n libgccjit-devel
%{_prefix}/%{_lib}/libgccjit.so
%{_prefix}/include/libgccjit*.h
%{_infodir}/libgccjit.info*
%doc rpm.doc/libgccjit-devel/*
%doc gcc/jit/docs/examples

%files -n libgdiagnostics
%{_prefix}/bin/sarif-replay
%{_prefix}/%{_lib}/libgdiagnostics.so.*

%files -n libgdiagnostics-devel
%{_prefix}/%{_lib}/libgdiagnostics.so
%{_prefix}/include/libgdiagnostics*.h
%doc rpm.doc/libgdiagnostics-devel/*

%files plugin-devel
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/plugin

%files gdb-plugin
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcc1plugin.so*
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/libcp1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*

%if %{build_offload_nvptx}
%files offload-nvptx
%{_prefix}/bin/nvptx-none-*
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-gcc
%{_prefix}/bin/%{gcc_target_platform}-accel-nvptx-none-lto-dump
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%{_prefix}/lib/gcc/nvptx-none
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/nvptx-none
%dir %{_prefix}/nvptx-none
%{_prefix}/nvptx-none/bin
%{_prefix}/nvptx-none/include

%files -n libgomp-offload-nvptx
%{_prefix}/%{_lib}/libgomp-plugin-nvptx.so.*
%endif

%if %{build_offload_amdgcn}
%files offload-amdgcn
%{_prefix}/bin/amdgcn-amdhsa-*
%{_prefix}/bin/%{gcc_target_platform}-accel-amdgcn-amdhsa-gcc
%{_prefix}/bin/%{gcc_target_platform}-accel-amdgcn-amdhsa-lto-dump
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel
%{_prefix}/lib/gcc/amdgcn-amdhsa
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_major}/accel/amdgcn-amdhsa
%dir %{_prefix}/amdgcn-amdhsa
%{_prefix}/amdgcn-amdhsa/bin
%{_prefix}/amdgcn-amdhsa/include

%files -n libgomp-offload-amdgcn
%{_prefix}/%{_lib}/libgomp-plugin-gcn.so.*
%endif

%if %{build_annobin_plugin}
%files plugin-annobin
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gcc-annobin.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gcc-annobin.so.0
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/plugin/gcc-annobin.so.0.0.0
%endif

%changelog
* Fri Jan 23 2026 Jakub Jelinek <jakub@redhat.com> 15.2.1-7
- update from releases/gcc-15 branch
  - PRs c++/122070, c++/122550, c++/123597, libstdc++/123147,
	middle-end/123107, middle-end/123703, target/119130, target/123742,
	tree-optimization/122793, tree-optimization/123602,
	tree-optimization/123736, tree-optimization/123741

* Tue Jan 20 2026 Jakub Jelinek <jakub@redhat.com> 15.2.1-6
- update from releases/gcc-15 branch
  - PRs ada/68179, ada/123060, ada/123088, ada/123096, ada/123138, ada/123185,
	ada/123289, ada/123302, ada/123306, ada/123371, ada/123589,
	analyzer/122975, analyzer/123085, c/123156, c++/91388, c++/114764,
	c++/116952, c++/120446, c++/121854, c++/121966, c++/122048,
	c++/122668, c++/122752, c++/122772, c++/122834, c++/122922,
	c++/123331, debug/121964, diagnostics/120063, fortran/107406,
	libfortran/122936, libstdc++/120446, libstdc++/122812,
	libstdc++/122907, middle-end/111817, middle-end/123392,
	rtl-optimization/121773, rtl-optimization/122215,
	rtl-optimization/123121, rtl-optimization/123523, target/117575,
	target/120250, target/121192, target/121485, target/123022,
	target/123092, target/123155, target/123217, target/123460,
	target/123484, target/123489, target/123521, target/123607,
	testsuite/123353, tree-optimization/122868, tree-optimization/123040,
	tree-optimization/123300, tree-optimization/123351,
	tree-optimization/123372, tree-optimization/123431,
	tree-optimization/123513

* Thu Dec 11 2025 Jakub Jelinek <jakub@redhat.com> 15.2.1-5
- update from releases/gcc-15 branch
  - PRs ada/111433, ada/115305, ada/122640, ada/123037, c/121506, c/123018,
	c++/119580, c++/120529, c++/120876, c++/121325, c++/121445,
	c++/122625, c++/122658, c++/122677, c++/122789, fortran/122709,
	fortran/122977, libstdc++/122661, libstdc++/122726, libstdc++/122743,
	libstdc++/122842, libstdc++/122921, lto/122515, middle-end/120052,
	middle-end/120564, middle-end/121581, middle-end/122624,
	rtl-optimization/122627, target/110796, target/118446, target/119275,
	target/121853, target/122175, target/122189, target/122216,
	target/122446, target/122539, target/122652, target/122656,
	target/122692, target/122695, target/122858, target/122867,
	target/122991, tree-optimization/121776, tree-optimization/122126,
	tree-optimization/122225, tree-optimization/122943
- create gnatgcc symlink only when building Ada
- avoid building libssp and disabled libraries
- remove various unpackaged files from the buildroot

* Tue Nov 11 2025 Jakub Jelinek <jakub@redhat.com> 15.2.1-4
- update from releases/gcc-15 branch
  - PRs ada/81087, ada/118208, ada/118782, c++/122192, c++/122253, c++/122310,
	c++/122381, c++/122421, fortran/107968, fortran/114023,
	fortran/122206, fortran/122386, rtl-optimization/122321,
	target/99930, target/118460, target/119079, target/120674,
	target/121604, target/122097, target/122270, target/122323,
	target/122516, target/122527, tree-optimization/122012,
	tree-optimization/122394, tree-optimization/122408,
	tree-optimization/122505
  - fix ICE while building firefox with LTO+PGO (#2395476, PR lto/122620)

* Wed Oct 22 2025 Jakub Jelinek <jakub@redhat.com> 15.2.1-3
- update from releases/gcc-15 branch
  - PRs ada/107536, ada/113536, ada/117517, ada/118343, c/122188, c++/120757,
	c++/121981, c++/122302, fortran/108581, fortran/121616,
	fortran/121939, go/104290, libstdc++/122062, libstdc++/122322,
	middle-end/121922, middle-end/122133, target/110812, target/121599,
	target/121652, target/121742, target/121780, target/121781,
	target/121845, target/121875, target/122119, target/122177,
	target/122187, target/122210, target/122220, target/122222,
	target/122223, tree-optimization/121772, tree-optimization/122104,
	tree-optimization/122213
- package libgcobol.spec (#2401679)

* Wed Sep 24 2025 Jakub Jelinek <jakub@redhat.com> 15.2.1-2
- update from releases/gcc-15 branch
  - PRs ada/121968, bootstrap/118009, bootstrap/119089, c++/97740, c++/119859,
	c++/120499, c++/120620, c++/121351, c++/121396, c++/121524,
	c++/121724, c++/121795, c++/121801, c++/121977, c++/122015,
	c++/122019, fortran/89092, fortran/121263, libfortran/121234,
	libgcc/117600, libstdc++/110853, libstdc++/117276, libstdc++/119861,
	libstdc++/120390, libstdc++/120698, libstdc++/121097,
	libstdc++/121313, libstdc++/121374, libstdc++/121496,
	libstdc++/121745, libstdc++/121827, middle-end/121453,
	middle-end/121828, middle-end/121831, rtl-optimization/87600,
	rtl-optimization/120718, rtl-optimization/120983,
	rtl-optimization/121253, rtl-optimization/121757, target/49857,
	target/81540, target/116445, target/118280, target/118885,
	target/119830, target/120476, target/120691, target/120986,
	target/121007, target/121118, target/121208, target/121294,
	target/121414, target/121449, target/121464, target/121510,
	target/121534, target/121542, target/121548, target/121602,
	target/121608, target/121634, target/121749, target/121794,
	target/121906, testsuite/118567, tree-optimization/107997,
	tree-optimization/121370, tree-optimization/121527,
	tree-optimization/121659, tree-optimization/121844,
	tree-optimization/121870, tree-optimization/122016

* Fri Aug  8 2025 Jakub Jelinek <jakub@redhat.com> 15.2.1-1
- update from releases/gcc-15 branch
  - GCC 15.2 release
  - PRs ada/120440, ada/121184, c/119950, c/120055, c/120353, c/120354,
	c++/95615, c++/108080, c++/109283, c++/115605, c++/115908, c++/116775,
	c++/118074, c++/118903, c++/119916, c++/120224, c++/120243,
	c++/120273, c++/120412, c++/120453, c++/120495, c++/120577,
	c++/120756, c++/120800, c++/120845, c++/121055, c++/121133,
	c++/121219, c++/121238, cobol/119231, cobol/119323, cobol/119335,
	cobol/119337, cobol/119377, cobol/119524, cobol/119632, cobol/119695,
	cobol/119770, cobol/119771, cobol/119772, cobol/119790, cobol/119810,
	cobol/119885, cobol/119975, cobol/120251, cobol/120328, cobol/120402,
	cobol/120621, cobol/120765, cobol/120772, cobol/120779, cobol/120790,
	cobol/120791, cobol/120794, fortran/119106, fortran/121145,
	fortran/121203, ipa/114790, libstdc++/119962, libstdc++/121373,
	lto/120308, middle-end/119835, middle-end/121095, middle-end/121159,
	middle-end/121322, middle-end/121389, rtl-optimization/121340,
	target/118891, target/119692, target/119737, target/119853,
	target/119854, target/120119, target/120351, target/120427,
	target/120530, target/120645, target/120714, target/121027,
	target/121028, target/121064, target/121121, target/121274,
	target/121277, testsuite/121286, testsuite/121288,
	tree-optimization/117423, tree-optimization/118891,
	tree-optimization/119085, tree-optimization/121127,
	tree-optimization/121130, tree-optimization/121190,
	tree-optimization/121202, tree-optimization/121256,
	tree-optimization/121264, tree-optimization/121320,
	tree-optimization/121323, tree-optimization/121413

* Sat Jul 19 2025 Jakub Jelinek <jakub@redhat.com> 15.1.1-5
- update from releases/gcc-15 branch
  - PRs cobol/119818, middle-end/120935, modula2/121164, testsuite/119508

* Fri Jul 18 2025 Jakub Jelinek <jakub@redhat.com> 15.1.1-4
- update from releases/gcc-15 branch
  - PRs ada/121056, c++/87097, c++/120569, c++/120628, c++/120954,
	fortran/104428, fortran/120637, fortran/120843, fortran/120847,
	fortran/121060, ipa/121023, libstdc++/118681, libstdc++/119754,
	libstdc++/120997, middle-end/120709, modula2/117203, modula2/119650,
	modula2/120253, modula2/120389, modula2/120474, modula2/120497,
	modula2/120542, modula2/120606, modula2/120673, modula2/120731,
	modula2/120912, rtl-optimization/120242, rtl-optimization/120627,
	rtl-optimization/120736, rtl-optimization/120813, target/118241,
	target/120356, target/120807, target/120908, target/120995,
	target/120999, tree-optimization/118669, tree-optimization/120358,
	tree-optimization/120780, tree-optimization/120817,
	tree-optimization/120924, tree-optimization/120944,
	tree-optimization/121035, tree-optimization/121049,
	tree-optimization/121059, tree-optimization/121131

* Mon Jul  7 2025 Jakub Jelinek <jakub@redhat.com> 15.1.1-3
- update from releases/gcc-15 branch
  - PRs ada/120665, ada/120705, ada/120854, c/120180, c++/116064, c++/120123,
	c++/120363, c++/120413, c++/120414, c++/120471, c++/120502,
	c++/120555, c++/120575, c++/120684, c++/120940, fortran/51961,
	fortran/85750, fortran/99838, fortran/101735, fortran/102599,
	fortran/114022, fortran/119856, fortran/119948, fortran/120193,
	fortran/120355, fortran/120483, fortran/120711, fortran/120784,
	ipa/120295, libfortran/119856, libstdc++/99832, libstdc++/120367,
	libstdc++/120432, libstdc++/120465, libstdc++/120548,
	libstdc++/120625, libstdc++/120648, libstdc++/120650,
	libstdc++/120931, libstdc++/120934, middle-end/118694,
	middle-end/120369, middle-end/120547, middle-end/120608,
	middle-end/120631, rtl-optimization/116389, rtl-optimization/120050,
	rtl-optimization/120182, rtl-optimization/120347,
	rtl-optimization/120423, rtl-optimization/120550,
	rtl-optimization/120795, target/86772, target/119971, target/120042,
	target/120441, target/120442, target/120480, target/120624,
	testsuite/52641, testsuite/120082, testsuite/120919,
	tree-optimization/116352, tree-optimization/119960,
	tree-optimization/120003, tree-optimization/120341,
	tree-optimization/120357, tree-optimization/120638,
	tree-optimization/120654, tree-optimization/120677,
	tree-optimization/120729, tree-optimization/120927
- fix up FE lowering of pointer arith (PR c/120837)
- perform %%check with -foffload=disable flag

* Wed May 21 2025 Jakub Jelinek <jakub@redhat.com> 15.1.1-2
- update from releases/gcc-15 branch
  - PRs ada/112958, ada/120104, c/120057, c++/119863, c++/119864, c++/119938,
	c++/119939, c++/119981, c++/119996, c++/120012, c++/120013,
	c++/120023, c++/120125, c++/120161, c++/120350, fortran/102891,
	fortran/102900, fortran/119928, fortran/119986, fortran/120049,
	fortran/120107, fortran/120139, fortran/120163, fortran/120179,
	fortran/120191, ipa/119852, ipa/119973, ipa/120006, ipa/120146,
	libfortran/120152, libfortran/120153, libfortran/120158,
	libfortran/120196, libstdc++/118260, libstdc++/119427,
	libstdc++/119714, libstdc++/120029, libstdc++/120114,
	libstdc++/120159, libstdc++/120187, libstdc++/120190,
	libstdc++/120198, libstdc++/120293, modula2/115276, modula2/119914,
	modula2/119915, modula2/120117, modula2/120188, preprocessor/116047,
	preprocessor/120061, target/119610, testsuite/119909,
	tree-optimization/111873, tree-optimization/119712,
	tree-optimization/120043, tree-optimization/120048,
	tree-optimization/120074, tree-optimization/120089,
	tree-optimization/120143, tree-optimization/120211

* Fri Apr 25 2025 Jakub Jelinek <jakub@redhat.com> 15.1.1-1
- update from releases/gcc-15 branch
  - GCC 15.1 release
  - PRs fortran/119836, target/119327, target/119873, tree-optimization/118407

* Fri Apr 18 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.14
- update from releases/gcc-14 branch
  - GCC 15.1.0-rc1
  - PRs tree-optimization/119858

* Thu Apr 17 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.13
- update from trunk and releases/gcc-14 branch
  - PRs ada/119643, c/88382, c/119717, c++/99214, c++/101180, c++/106618,
	c++/111075, c++/112288, c++/113360, c++/113835, c++/114772,
	c++/114970, c++/115639, c++/116416, c++/116954, c++/119175,
	c++/119345, c++/119687, c++/119692, c++/119755, c++/119807,
	cobol/119217, cobol/119302, cobol/119694, cobol/119759, cobol/119776,
	cobol/119777, d/109023, d/119758, d/119761, d/119799, d/119817,
	d/119826, driver/90465, driver/119727, fortran/106948, fortran/119669,
	ipa/113203, ipa/119318, ipa/119803, libfortran/119502, libgcc/101075,
	libgcc/119796, libgomp/119849, libstdc++/21334, libstdc++/119725,
	libstdc++/119748, libstdc++/119840, lto/119792, middle-end/14708,
	middle-end/105548, middle-end/119706, middle-end/119808,
	modula2/119735, modula2/119779, rtl-optimization/118502,
	rtl-optimization/119785, rust/119341, rust/119342, sanitizer/119801,
	target/42683, target/97106, target/97585, target/106445,
	target/108134, target/113633, target/116827, target/118794,
	target/119298, target/119386, target/119533, target/119547,
	target/119673, target/119784, target/119834, testsuite/117706,
	translation/119684, tree-optimization/71094, tree-optimization/87909,
	tree-optimization/112822, tree-optimization/116093,
	tree-optimization/118476, tree-optimization/119351,
	tree-optimization/119399, tree-optimization/119706,
	tree-optimization/119707, tree-optimization/119718,
	tree-optimization/119722, tree-optimization/119757,
	tree-optimization/119778

* Thu Apr 10 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.12
- update from trunk
  - PRs ada/119571, analyzer/113253, bootstrap/119680, c/78008, c/81831,
	c/101440, c/114957, c/117689, c/118118, c/119173, c/119582, c/119612,
	c++/60972, c++/64500, c++/90468, c++/99546, c++/106976, c++/109961,
	c++/113925, c++/116285, c++/116960, c++/117336, c++/117530,
	c++/117849, c++/118249, c++/118626, c++/118629, c++/118698,
	c++/118982, c++/119303, c++/119383, c++/119387, c++/119401,
	c++/119462, c++/119518, c++/119551, c++/119563, c++/119564,
	c++/119574, c++/119608, c++/119652, cobol/119283, cobol/119295,
	cobol/119364, cobol/119414, cobol/119521, cobol/119682, d/117002,
	d/117832, d/118309, driver/58973, fortran/101602, fortran/119460,
	fortran/119656, gcov-profile/119535, gcov-profile/119553,
	gcov-profile/119618, ipa/119599, libfortran/119460, libstdc++/109162,
	libstdc++/110498, libstdc++/114758, libstdc++/114945,
	libstdc++/115046, libstdc++/119517, libstdc++/119545,
	libstdc++/119550, libstdc++/119593, libstdc++/119620,
	libstdc++/119642, libstdc++/119671, middle-end/78874,
	middle-end/101018, middle-end/112589, middle-end/116595,
	middle-end/118965, middle-end/119442, middle-end/119482,
	middle-end/119537, middle-end/119541, middle-end/119559,
	middle-end/119613, middle-end/119662, preprocessor/118674,
	preprocessor/119391, rtl-optimization/119291, rtl-optimization/119594,
	rtl-optimization/119672, rtl-optimization/119689, target/117759,
	target/119308, target/119369, target/119473, target/119539,
	target/119549, target/119556, target/119572, target/119573,
	target/119645, target/119664, target/119678, testsuite/116398,
	testsuite/118597, tree-optimization/80331, tree-optimization/87502,
	tree-optimization/103827, tree-optimization/113281,
	tree-optimization/118924, tree-optimization/119491,
	tree-optimization/119493, tree-optimization/119532,
	tree-optimization/119534, tree-optimization/119586,
	tree-optimization/119614, tree-optimization/119616,
	tree-optimization/119640, web/119227
  - fix up LTO opts handling (##2356219, PR lto/119625)

* Sat Mar 29 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.11
- update from trunk
  - PRs ada/119265, ada/119440, analyzer/119278, bootstrap/119513, c/116545,
	c/118061, c/118765, c/119311, c/119350, c/119366, c++/101881,
	c++/114525, c++/114992, c++/118104, c++/118920, c++/118961,
	c++/119194, c++/119233, c++/119316, c++/119344, c++/119370,
	c++/119378, c++/119379, cobol/119213, cobol/119214, cobol/119241,
	cobol/119242, cobol/119244, cobol/119290, cobol/119301, cobol/119390,
	d/117621, d/118545, debug/101533, driver/101544, fortran/60560,
	fortran/85836, fortran/116706, fortran/118796, fortran/119272,
	fortran/119338, fortran/119349, fortran/119380, fortran/119403,
	fortran/119406, fortran/119419, gcov-profile/118442, ipa/98265,
	ipa/116572, ipa/119147, ipa/119376, ipa/119484, libfortran/85836,
	libgomp/96835, libitm/88319, libstdc++/101527, libstdc++/101587,
	libstdc++/108487, libstdc++/111055, libstdc++/111138,
	libstdc++/116440, libstdc++/117214, libstdc++/117983,
	libstdc++/118699, libstdc++/119135, libstdc++/119282,
	libstdc++/119358, libstdc++/119415, libstdc++/119429,
	libstdc++/119469, libstdc++/119488, middle-end/93437,
	middle-end/112938, middle-end/113546, middle-end/117811,
	middle-end/118627, middle-end/118795, middle-end/119325,
	modula2/115111, modula2/118045, modula2/118600, modula2/119449,
	modula2/119504, other/42270, other/119218, other/119250, other/119510,
	preprocessor/108900, rtl-optimization/118615, rtl-optimization/118914,
	rtl-optimization/119285, rtl-optimization/119307, rust/119333,
	target/55583, target/91614, target/92713, target/96226, target/98743,
	target/101544, target/112980, target/117069, target/117092,
	target/117452, target/118068, target/119010, target/119114,
	target/119120, target/119172, target/119224, target/119235,
	target/119270, target/119286, target/119355, target/119357,
	target/119408, target/119421, target/119425, target/119428,
	target/119450, target/119465, testsuite/113634, testsuite/113965,
	testsuite/116163, testsuite/119220, testsuite/119382,
	testsuite/119489, tree-optimization/37143, tree-optimization/105820,
	tree-optimization/118616, tree-optimization/119155,
	tree-optimization/119274, tree-optimization/119287,
	tree-optimization/119389, tree-optimization/119417,
	tree-optimization/119483
- package gcc-gcobol on x86_64 and aarch64 so far
- turn unversioned obsoletes into versioned ones

* Thu Mar 13 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.10
- update from trunk
  - PRs analyzer/117262, c/60440, c/67301, c/112960, c/113515, c/117029,
	c/117178, c/118579, c/119183, c++/98533, c++/100589, c++/109431,
	c++/110584, c++/114795, c++/115580, c++/116740, c++/117364,
	c++/117504, c++/117512, c++/118775, c++/118787, c++/118799,
	c++/118874, c++/119073, c++/119076, c++/119102, c++/119123,
	c++/119134, c++/119138, c++/119150, c++/119154, c++/119162,
	cobol/119216, cobol/119229, d/119139, debug/119190, fortran/47928,
	fortran/77872, fortran/98903, fortran/101577, fortran/103391,
	fortran/104684, fortran/104826, fortran/107143, fortran/118747,
	fortran/119049, fortran/119054, fortran/119074, fortran/119078,
	fortran/119118, fortran/119157, fortran/119199, ipa/118318,
	ipa/118785, ipa/119067, libgcc/119151, libstdc++/108053,
	libstdc++/113310, libstdc++/115215, libstdc++/115218,
	libstdc++/119081, libstdc++/119110, libstdc++/119121,
	libstdc++/119144, lto/114501, middle-end/97323, middle-end/118457,
	middle-end/118801, middle-end/119119, middle-end/119204,
	middle-end/119219, middle-end/119226, modula2/118998, modula2/119088,
	modula2/119192, other/38768, other/119052, preprocessor/119202,
	rtl-optimization/114492, rtl-optimization/116564,
	rtl-optimization/117477, rtl-optimization/118739,
	rtl-optimization/119046, rtl-optimization/119071,
	rtl-optimization/119099, sanitizer/56682, target/114222,
	target/114991, target/115258, target/115439, target/115485,
	target/115835, target/116708, target/116901, target/117931,
	target/117955, target/118351, target/118892, target/118906,
	target/118934, target/118942, target/118956, target/119084,
	target/119115, target/119127, target/119131, target/119133,
	target/119171, target/119238, testsuite/115248,
	tree-optimization/116125, tree-optimization/116901,
	tree-optimization/117919, tree-optimization/118922,
	tree-optimization/118976, tree-optimization/119057,
	tree-optimization/119096, tree-optimization/119145,
	tree-optimization/119166
- use %%autopatch in the spec file

* Sat Mar  1 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.9
- update from trunk
  - PRs c/114870, c/119001, c++/110822, c++/114913, c++/118516, c++/118928,
	c++/118986, c++/119038, c++/119045, d/116961, d/118654,
	fortran/108233, fortran/108369, fortran/118730, fortran/118789,
	ipa/111245, ipa/118243, jit/117047, libstdc++/93059, libstdc++/104606,
	libstdc++/105609, libstdc++/106612, libstdc++/112490,
	libstdc++/112803, libstdc++/118083, lto/91299, middle-end/66279,
	middle-end/115871, middle-end/118819, middle-end/118860,
	middle-end/119021, rtl-optimization/116336, rtl-optimization/117712,
	rtl-optimization/119002, target/107635, target/109189, target/115458,
	target/118931, target/118940, testsuite/115028, testsuite/116143,
	translation/118991, tree-optimization/87984, tree-optimization/116855,
	tree-optimization/118464, tree-optimization/119030
- fix ranger related miscompilation (PR tree-optimization/118953)
- fix miscompilation of floating point comparisons if NaNs can appear
  (#2346233, PR rtl-optimization/119002)
- fix ICF related miscompilation (PR ipa/119006)

* Tue Feb 25 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.8
- update from trunk
  - PRs analyzer/118300, c/117023, c/119000, c++/66519, c++/66878, c++/70037,
	c++/70536, c++/82794, c++/82936, c++/83144, c++/86769, c++/86933,
	c++/94100, c++/96364, c++/101740, c++/102455, c++/107637, c++/110345,
	c++/113800, c++/115586, c++/116379, c++/117106, c++/117324,
	c++/118053, c++/118190, c++/118282, c++/118304, c++/118306,
	c++/118319, c++/118574, c++/118661, c++/118763, c++/118773,
	c++/118807, c++/118822, c++/118833, c++/118846, c++/118849,
	c++/118856, c++/118876, c++/118923, c++/118981, c++/188574, d/111628,
	debug/118790, driver/117739, fortran/24878, fortran/47485,
	fortran/48958, fortran/56423, fortran/59252, fortran/107635,
	fortran/115271, fortran/116829, fortran/117430, fortran/118080,
	fortran/118159, fortran/118740, fortran/118745, fortran/118750,
	fortran/118845, fortran/118862, go/118746, ipa/118097, jit/118780,
	libfortran/114618, libstdc++/100612, libstdc++/111050,
	libstdc++/115209, libstdc++/118160, libstdc++/118559,
	libstdc++/118701, libstdc++/118811, libstdc++/118855,
	libstdc++/118865, lto/118125, middle-end/107067, middle-end/113525,
	middle-end/116351, middle-end/117263, middle-end/118288,
	middle-end/118950, middle-end/118993, modula2/115112, modula2/118761,
	modula2/118978, other/116613, other/118919, rtl-optimization/102150,
	rtl-optimization/108840, rtl-optimization/115568,
	rtl-optimization/115932, rtl-optimization/116028,
	rtl-optimization/116244, rtl-optimization/117081,
	rtl-optimization/117082, rtl-optimization/117239,
	rtl-optimization/117506, rtl-optimization/117922,
	rtl-optimization/118497, sarif-replay/118792, sarif-replay/118881,
	target/69374, target/86660, target/94282, target/109093,
	target/109780, target/113331, target/114516, target/114522,
	target/115123, target/115478, target/115703, target/117674,
	target/117991, target/118089, target/118146, target/118248,
	target/118540, target/118561, target/118601, target/118623,
	target/118685, target/118764, target/118768, target/118771,
	target/118772, target/118776, target/118806, target/118813,
	target/118815, target/118825, target/118828, target/118832,
	target/118835, target/118843, target/118844, target/118872,
	target/118878, target/118936, testsuite/116604, testsuite/116986,
	testsuite/118754, tree-optimization/82142, tree-optimization/86270,
	tree-optimization/90579, tree-optimization/98028,
	tree-optimization/98845, tree-optimization/108357,
	tree-optimization/110449, tree-optimization/115538,
	tree-optimization/117790, tree-optimization/118521,
	tree-optimization/118706, tree-optimization/118727,
	tree-optimization/118749, tree-optimization/118756,
	tree-optimization/118805, tree-optimization/118817,
	tree-optimization/118852, tree-optimization/118895,
	tree-optimization/118915, tree-optimization/118954,
	tree-optimization/118973
- drop on riscv riscv_cmo.h header from file list, add sifive_vector.h

* Tue Feb  4 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.7
- update from trunk
  - PRs ada/118712, ada/118731, c/118742, c++/79786, c++/98893, c++/108205,
	c++/109918, c++/114619, c++/116506, c++/116880, c++/116914,
	c++/117114, c++/117778, c++/118265, c++/118470, c++/118491,
	c++/118718, c++/118719, fortran/93289, lto/113207, middle-end/115913,
	middle-end/116926, modula2/117411, modula2/118703,
	rtl-optimization/111673, rtl-optimization/117248,
	rtl-optimization/117611, target/116010, target/118713,
	testsuite/116845, tree-optimization/117113, tree-optimization/118717

* Sat Feb  1 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.6
- update from trunk
  - PRs c++/117501, c++/117516, debug/100530, fortran/108454, fortran/118714,
	ipa/117432, libstdc++/118156, middle-end/117498, modula2/115032,
	rtl-optimization/116234, target/113689, target/115673,
	tree-optimization/114277
- use rpm.execute instead of posix.fork, posix.exec and posix.wait in libgcc
  scriptlets; guard them on ldconfig macro existence and use that macro instead
  of explicit /sbin/ldconfig (#2291927)

* Thu Jan 30 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.5
- update from trunk
  - PRs c/116357, c++/57533, c++/114292, c++/116524, c++/117855, c++/118239,
	c++/118285, c++/118632, c++/118655, c++/118673, d/118477,
	fortran/58857, fortran/110993, fortran/118640, fortran/118683,
	libstdc++/98749, libstdc++/118413, libstdc++/118563,
	middle-end/118643, middle-end/118684, middle-end/118692,
	middle-end/118695, modula2/116073, modula2/117737, modula2/118183,
	other/118675, preprocessor/118168, rtl-optimization/118320,
	rtl-optimization/118429, rtl-optimization/118638,
	rtl-optimization/118662, target/114085, target/116860, target/117173,
	target/117688, target/118103, target/118490, target/118642,
	target/118646, target/118663, target/118696, testsuite/118127,
	tree-optimization/112859, tree-optimization/114052,
	tree-optimization/115347, tree-optimization/117270,
	tree-optimization/117424, tree-optimization/117892,
	tree-optimization/118505, tree-optimization/118637,
	tree-optimization/118653
- fix up C++ list conversion for #embed or large series of comma
  separated small constants (PR c++/118671)
- punt in niters clz/ctz creation if internal function can't be used
  and frontend didn't build __builtin_c{l,t}z{,l,ll} builtins
  (PR tree-optimization/118689)

* Sat Jan 25 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.4
- update from trunk
  - PRs c/118639, c++/105440, c++/107522, c++/107741, c++/115769, c++/116417,
	c++/116568, c++/116756, c++/117153, c++/117397, c++/117602,
	c++/117775, c++/117827, c++/118047, c++/118049, c++/118101,
	c++/118124, c++/118139, c++/118147, c++/118199, c++/118214,
	c++/118225, c++/118245, c++/118255, c++/118278, c++/118355,
	c++/118390, c++/118396, c++/118454, c++/118486, c++/118509,
	c++/118513, c++/118523, c++/118525, c++/118528, c++/118532,
	c++/118534, c++/118582, c++/118590, c++/118604, d/114434, d/115249,
	d/116373, d/117115, d/118438, d/118448, d/118449, d/118584,
	fortran/71884, fortran/81978, fortran/96087, fortran/107122,
	fortran/118321, fortran/118359, fortran/118441, fortran/118613,
	gcov-profile/116743, ipa/116068, ipa/118400, jit/117886,
	libfortran/118406, libfortran/118536, libfortran/118571,
	libstdc++/99995, libstdc++/100249, libstdc++/109849, libstdc++/118158,
	libstdc++/118185, lto/118238, middle-end/112779, middle-end/113904,
	middle-end/114596, middle-end/114877, middle-end/118140,
	middle-end/118273, middle-end/118472, modula2/118010, modula2/118589,
	objc++/118586, rtl-optimization/109592, rtl-optimization/113994,
	rtl-optimization/117868, rtl-optimization/118067,
	rtl-optimization/118562, rtl-optimization/118591,
	rtl-optimization/1180167, sarif-replay/117670, target/80813,
	target/110901, target/113257, target/113560, target/114442,
	target/116256, target/116308, target/116593, target/117079,
	target/117726, target/118154, target/118170, target/118182,
	target/118270, target/118329, target/118357, target/118489,
	target/118497, target/118501, target/118510, target/118511,
	target/118512, target/118531, target/118560, target/118609,
	testsuite/116448, testsuite/117958, testsuite/118451,
	tree-optimization/92539, tree-optimization/102705,
	tree-optimization/115494, tree-optimization/115777,
	tree-optimization/115895, tree-optimization/116010,
	tree-optimization/117668, tree-optimization/117875,
	tree-optimization/118012, tree-optimization/118077,
	tree-optimization/118224, tree-optimization/118348,
	tree-optimization/118360, tree-optimization/118384,
	tree-optimization/118430, tree-optimization/118456,
	tree-optimization/118483, tree-optimization/118487,
	tree-optimization/118514, tree-optimization/118522,
	tree-optimization/118529, tree-optimization/118552,
	tree-optimization/118558, tree-optimization/118569,
	tree-optimization/118572, tree-optimization/118605,
	tree-optimization/118628, tree-optimization/118634
- fix libstdc++.modules.json content after relocation

* Tue Jan 14 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.3
- temporary fix for coroutine range for handling (PR c++/117231)

* Tue Jan 14 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.2
- update from trunk
  - PRs ada/118459, c/116871, c++/118445, modula2/116557, target/116030,
	target/117682, tree-optimization/118405

* Mon Jan 13 2025 Jakub Jelinek <jakub@redhat.com> 15.0.1-0.1
- update from trunk
  - PRs c/118112, c++/114630, d/117701, fortran/115788, fortran/118432,
	lto/118181, middle-end/64242, middle-end/118303, middle-end/118411,
	middle-end/118415, modula2/118453, rtl-optimization/107455,
	target/115910, target/115921, target/118418, tree-optimization/117119,
	tree-optimization/117997, tree-optimization/118409

* Sat Jan 11 2025 Jakub Jelinek <jakub@redhat.com> 15.0.0-0.4
- update from trunk
  - PRs ada/18765, ada/118274, c/116060, c/117866, c/118376, c++/117792,
	c++/117887, c++/117925, c++/117937, c++/117993, c++/118060,
	c++/118277, c++/118387, c++/118391, fortran/108434, fortran/118337,
	ipa/118138, rtl-optimization/117186, rtl-optimization/117467,
	rtl-optimization/117934, rtl-optimization/118266, target/65181,
	target/118017, target/118131, target/118188, target/118332,
	target/118362, testsuite/118025, tree-optimization/88575,
	tree-optimization/116126, tree-optimization/117927,
	tree-optimization/118206, tree-optimization/118211,
	tree-optimization/118344

* Thu Jan  9 2025 Jakub Jelinek <jakub@redhat.com> 15.0.0-0.3
- new package
