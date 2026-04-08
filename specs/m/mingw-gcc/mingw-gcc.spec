# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global mingw_build_ucrt64 1
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

# Causes build failures
%undefine _auto_set_build_flags

# NOTE See mingw-filesystem/README.md for the build steps!
%global bootstrap 0

%global build_isl 0

%global isl_version 0.16.1

# Run the testsuite
%global enable_tests 0

%global DATE 20250808
%global gitrev f833458d29b4fa40ffce6cf3b37ab9a30a864901
%global gcc_version 15.2.1
%global gcc_major 15

Name:           mingw-gcc
Version:        %{gcc_version}
Release:        2%{?dist}
Summary:        MinGW Windows cross-compiler (GCC) for C

# Sync with native 'gcc' package
License: GPL-3.0-or-later AND LGPL-3.0-or-later AND (GPL-3.0-or-later WITH GCC-exception-3.1) AND (GPL-3.0-or-later WITH Texinfo-exception) AND (LGPL-2.1-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH GNU-compiler-exception) AND BSL-1.0 AND GFDL-1.3-or-later AND Linux-man-pages-copyleft-2-para AND SunPro AND BSD-1-Clause AND BSD-2-Clause AND BSD-2-Clause-Views AND BSD-3-Clause AND BSD-4-Clause AND BSD-Source-Code AND Zlib AND MIT AND Apache-2.0 AND (Apache-2.0 WITH LLVM-Exception) AND ZPL-2.1 AND ISC AND LicenseRef-Fedora-Public-Domain AND HP-1986 AND curl AND Martin-Birgmeier AND HPND-Markus-Kuhn AND dtoa AND SMLNJ AND AMD-newlib AND OAR AND HPND-merchantability-variant AND HPND-Intel
URL:            http://gcc.gnu.org

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone --depth 1 git://gcc.gnu.org/git/gcc.git gcc-dir.tmp
# git --git-dir=gcc-dir.tmp/.git fetch --depth 1 origin %%{gitrev}
# git --git-dir=gcc-dir.tmp/.git archive --prefix=%%{name}-%%{version}-%%{DATE}/ %%{gitrev} | xz -9e > %%{name}-%%{version}-%%{DATE}.tar.xz
# rm -rf gcc-dir.tmp
%global srcdir gcc-%{version}-%{DATE}
Source0:        %{srcdir}.tar.xz

# See https://sourceforge.net/p/mingw-w64/mailman/mingw-w64-public/thread/8fd2fb03-9b8a-07e1-e162-0bb48bcc3984%40gmail.com/#msg37200751
Patch0:         0020-libgomp-Don-t-hard-code-MS-printf-attributes.patch
# Add missing stdlib.h include
Patch1:         mingw-gcc_include-stdlib.patch

BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  texinfo
BuildRequires:  mingw32-filesystem >= 133
BuildRequires:  mingw64-filesystem >= 133
BuildRequires:  ucrt64-filesystem >= 133
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils
BuildRequires:  ucrt64-binutils
BuildRequires:  mingw32-headers
BuildRequires:  mingw64-headers
BuildRequires:  ucrt64-headers
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  libmpc-devel
BuildRequires:  libgomp
BuildRequires:  flex
BuildRequires:  zlib-devel
%if %{build_isl}
BuildRequires: isl = %{isl_version}
BuildRequires: isl-devel = %{isl_version}
%endif
%if 0%{bootstrap} == 0
BuildRequires:  mingw32-crt
BuildRequires:  mingw64-crt
BuildRequires:  ucrt64-crt
BuildRequires:  mingw32-winpthreads
BuildRequires:  mingw64-winpthreads
BuildRequires:  ucrt64-winpthreads
%if 0%{enable_tests}
BuildRequires:  wine
BuildRequires:  autogen
BuildRequires:  dejagnu
BuildRequires:  sharutils
%endif
%endif
Provides: bundled(libiberty)

%description
MinGW Windows cross-compiler (GCC) for C.

###############################################################################
# Mingw32
###############################################################################
%package -n mingw32-gcc
Summary:        MinGW Windows cross-compiler (GCC) for C for the win32 target
Requires:       mingw32-binutils
Requires:       mingw32-headers
Requires:       mingw32-cpp
%if 0%{bootstrap} == 0
Requires:       mingw32-crt
Requires:       mingw32-libgcc
Requires:       mingw32-winpthreads-static
%endif

%description -n mingw32-gcc
MinGW Windows cross-compiler (GCC) for C for the win32 target.


%package -n mingw32-gcc-plugin-devel
Summary:	Support for compiling plugins for MinGW GCC for the win32 target
Requires:	mingw32-gcc = %{version}-%{release}
Requires:	gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1

%description -n mingw32-gcc-plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.


%if 0%{bootstrap} == 0
%package -n mingw32-libgcc
Summary:        MinGW Windows GCC runtime libraries for C for the win32 target

%description -n mingw32-libgcc
MinGW Windows GCC runtime libraries for C for the win32 target.


%package -n mingw32-libstdc++
Summary:        MinGW Windows GCC runtime libraries for C++ for the win32 target

%description -n mingw32-libstdc++
MinGW Windows GCC runtime libraries for C++ for the win32 target.


%package -n mingw32-libgomp
Summary:        GCC OpenMP v3.0 shared support library for the win32 target
Requires:       mingw32-gcc = %{version}-%{release}

%description -n mingw32-libgomp
This package contains GCC shared support library which is
needed for OpenMP v3.0 support for the win32 target.
%endif


%package -n mingw32-cpp
Summary:        MinGW Windows cross-C Preprocessor for the win32 target
# NB: Explicit mingw32-filesystem dependency is REQUIRED here.
Requires:       mingw32-filesystem >= 133

%description -n mingw32-cpp
MinGW Windows cross-C Preprocessor for the win32 target.


%package -n mingw32-gcc-c++
Summary:        MinGW Windows cross-compiler for C++ for the win32 target
Requires:       mingw32-gcc = %{version}-%{release}

%description -n mingw32-gcc-c++
MinGW Windows cross-compiler for C++ for the win32 target.


%package -n mingw32-gcc-objc
Summary:        MinGW Windows cross-compiler support for Objective C for the win32 target
Requires:       mingw32-gcc = %{version}-%{release}

%description -n mingw32-gcc-objc
MinGW Windows cross-compiler support for Objective C for the win32 target.


%package -n mingw32-gcc-objc++
Summary:        MinGW Windows cross-compiler support for Objective C++ for the win32 target
Requires:       mingw32-gcc-c++ = %{version}-%{release}
Requires:       mingw32-gcc-objc = %{version}-%{release}

%description -n mingw32-gcc-objc++
MinGW Windows cross-compiler support for Objective C++ for the win32 target.


%package -n mingw32-gcc-gfortran
Summary:        MinGW Windows cross-compiler for FORTRAN for the win32 target
Requires:       mingw32-gcc = %{version}-%{release}

%description -n mingw32-gcc-gfortran
MinGW Windows cross-compiler for FORTRAN for the win32 target.


###############################################################################
# Mingw64
###############################################################################
%package -n mingw64-gcc
Summary:        MinGW Windows cross-compiler (GCC) for C for the win64 target
Requires:       mingw64-binutils
Requires:       mingw64-headers
Requires:       mingw64-cpp
%if 0%{bootstrap} == 0
Requires:       mingw64-crt
Requires:       mingw64-libgcc
Requires:       mingw64-winpthreads-static
%endif

%description -n mingw64-gcc
MinGW Windows cross-compiler (GCC) for C for the win64 target.


%package -n mingw64-gcc-plugin-devel
Summary:	Support for compiling plugins for MinGW GCC for the win64 target
Requires:	mingw64-gcc = %{version}-%{release}
Requires:	gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1

%description -n mingw64-gcc-plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.


%if 0%{bootstrap} == 0
%package -n mingw64-libgcc
Summary:        MinGW Windows GCC runtime libraries for C for the win64 target

%description -n mingw64-libgcc
MinGW Windows GCC runtime libraries for C for the win64 target.


%package -n mingw64-libstdc++
Summary:        MinGW Windows GCC runtime libraries for C++ for the win64 target

%description -n mingw64-libstdc++
MinGW Windows GCC runtime libraries for C++ for the win64 target.


%package -n mingw64-libgomp
Summary:        GCC OpenMP v3.0 shared support library for the win64 target
Requires:       mingw64-gcc = %{version}-%{release}

%description -n mingw64-libgomp
This package contains GCC shared support library which is
needed for OpenMP v3.0 support for the win32 target.
%endif


%package -n mingw64-cpp
Summary:        MinGW Windows cross-C Preprocessor for the win64 target.
# NB: Explicit mingw64-filesystem dependency is REQUIRED here.
Requires:       mingw64-filesystem >= 133

%description -n mingw64-cpp
MinGW Windows cross-C Preprocessor for the win64 target


%package -n mingw64-gcc-c++
Summary:        MinGW Windows cross-compiler for C++ for the win64 target
Requires:       mingw64-gcc = %{version}-%{release}

%description -n mingw64-gcc-c++
MinGW Windows cross-compiler for C++ for the win64 target.


%package -n mingw64-gcc-objc
Summary:        MinGW Windows cross-compiler support for Objective C for the win64 target
Requires:       mingw64-gcc = %{version}-%{release}

%description -n mingw64-gcc-objc
MinGW Windows cross-compiler support for Objective C for the win64 target.


%package -n mingw64-gcc-objc++
Summary:        MinGW Windows cross-compiler support for Objective C++ for the win64 target
Requires:       mingw64-gcc-c++ = %{version}-%{release}
Requires:       mingw64-gcc-objc = %{version}-%{release}

%description -n mingw64-gcc-objc++
MinGW Windows cross-compiler support for Objective C++ for the win64 target.


%package -n mingw64-gcc-gfortran
Summary:        MinGW Windows cross-compiler for FORTRAN for the win64 target
Requires:       mingw64-gcc = %{version}-%{release}

%description -n mingw64-gcc-gfortran
MinGW Windows cross-compiler for FORTRAN for the win64 target.


###############################################################################
# UCRT64
###############################################################################
%package -n ucrt64-gcc
Summary:        MinGW Windows cross-compiler (GCC) for C for the win64 target
Requires:       ucrt64-binutils
Requires:       ucrt64-headers
Requires:       ucrt64-cpp
%if 0%{bootstrap} == 0
Requires:       ucrt64-crt
Requires:       ucrt64-libgcc
Requires:       ucrt64-winpthreads-static
%endif


%description -n ucrt64-gcc
MinGW Windows cross-compiler (GCC) for C for the win64 target.


%package -n ucrt64-gcc-plugin-devel
Summary:	Support for compiling plugins for MinGW GCC for the win64 target
Requires:	ucrt64-gcc = %{version}-%{release}
Requires:	gmp-devel >= 4.1.2-8, mpfr-devel >= 3.1.0, libmpc-devel >= 0.8.1

%description -n ucrt64-gcc-plugin-devel
This package contains header files and other support files
for compiling GCC plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.


%if 0%{bootstrap} == 0
%package -n ucrt64-libgcc
Summary:        MinGW Windows GCC runtime libraries for C for the win64 target

%description -n ucrt64-libgcc
MinGW Windows GCC runtime libraries for C for the win64 target.


%package -n ucrt64-libstdc++
Summary:        MinGW Windows GCC runtime libraries for C++ for the win64 target

%description -n ucrt64-libstdc++
MinGW Windows GCC runtime libraries for C++ for the win64 target.


%package -n ucrt64-libgomp
Summary:        GCC OpenMP v3.0 shared support library for the win64 target
Requires:       ucrt64-gcc = %{version}-%{release}

%description -n ucrt64-libgomp
This package contains GCC shared support library which is
needed for OpenMP v3.0 support for the win32 target.
%endif


%package -n ucrt64-cpp
Summary:        MinGW Windows cross-C Preprocessor for the win64 target.
# NB: Explicit ucrt64-filesystem dependency is REQUIRED here.
Requires:       ucrt64-filesystem >= 133

%description -n ucrt64-cpp
MinGW Windows cross-C Preprocessor for the win64 target


%package -n ucrt64-gcc-c++
Summary:        MinGW Windows cross-compiler for C++ for the win64 target
Requires:       ucrt64-gcc = %{version}-%{release}

%description -n ucrt64-gcc-c++
MinGW Windows cross-compiler for C++ for the win64 target.


%package -n ucrt64-gcc-objc
Summary:        MinGW Windows cross-compiler support for Objective C for the win64 target
Requires:       ucrt64-gcc = %{version}-%{release}

%description -n ucrt64-gcc-objc
MinGW Windows cross-compiler support for Objective C for the win64 target.


%package -n ucrt64-gcc-objc++
Summary:        MinGW Windows cross-compiler support for Objective C++ for the win64 target
Requires:       ucrt64-gcc-c++ = %{version}-%{release}
Requires:       ucrt64-gcc-objc = %{version}-%{release}

%description -n ucrt64-gcc-objc++
MinGW Windows cross-compiler support for Objective C++ for the win64 target.


%package -n ucrt64-gcc-gfortran
Summary:        MinGW Windows cross-compiler for FORTRAN for the win64 target
Requires:       ucrt64-gcc = %{version}-%{release}

%description -n ucrt64-gcc-gfortran
MinGW Windows cross-compiler for FORTRAN for the win64 target.


%prep
%autosetup -p1 -n %{srcdir}
echo 'Fedora MinGW %{version}-%{release}' > gcc/DEV-PHASE

%build
# Default configure arguments
configure_args="\
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --includedir=%{_includedir} \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --datadir=%{_datadir} \
    --build=%_build --host=%_host \
    --with-gnu-as --with-gnu-ld --verbose \
    --without-newlib \
    --disable-multilib \
    --disable-libcc1 \
    --with-system-zlib \
    --disable-nls --without-included-gettext \
    --disable-win32-registry \
    --enable-languages="c,c++,objc,obj-c++,fortran" \
    --with-bugurl=http://bugzilla.redhat.com/bugzilla \
    --enable-threads=posix"

# PPL/CLOOG optimalisations are only available on Fedora
%if %{build_isl}
configure_args="$configure_args --with-isl"
%else
configure_args="$configure_args --without-isl"
%endif

# When bootstrapping, disable LTO support as it causes errors while building any binary
# $ i686-w64-mingw32-gcc -o conftest    conftest.c  >&5
# i686-w64-mingw32-gcc: fatal error: -fuse-linker-plugin, but liblto_plugin.so not found
%if 0%{bootstrap}
configure_args="$configure_args --disable-lto"
%else
configure_args="$configure_args --enable-libgomp"
%endif

# The %%configure macro can't be used for out of source builds
# without overriding other variables and causes unwanted side
# effects so make sure the right compiler flags are used
export CC="%{__cc} ${RPM_OPT_FLAGS}"

# Win32
mkdir build_win32
pushd build_win32
    ../configure $configure_args --target=%{mingw32_target} --with-sysroot=%{mingw32_sysroot} --with-gxx-include-dir=%{mingw32_includedir}/c++ --disable-sjlj-exceptions --with-dwarf2
popd

# Win64
mkdir build_win64
pushd build_win64
    ../configure $configure_args --target=%{mingw64_target} --with-sysroot=%{mingw64_sysroot} --with-gxx-include-dir=%{mingw64_includedir}/c++
popd

# ucrt64
mkdir build_ucrt64
pushd build_ucrt64
    ../configure $configure_args --target=%{ucrt64_target} --with-sysroot=%{ucrt64_sysroot} --with-gxx-include-dir=%{ucrt64_includedir}/c++
popd

# If we're bootstrapping, only build the GCC core
%if 0%{bootstrap}
%mingw_make_build all-gcc
%else
%mingw_make_build all
%endif


%if 0%{enable_tests}
%check
# Win32
# Create a seperate wine prefix
export WINEPREFIX=/tmp/.wine_gcc_testsuite
rm -rf $WINEPREFIX
mkdir $WINEPREFIX

# The command below will fail, but that's intentional
# We only have to call a wine binary which triggers
# the generation and population of a wine prefix
winecfg || :

# Copy the GCC DLL's inside the wine prefix
SYSTEM32_DIR=$WINEPREFIX/drive_c/windows/syswow64
if [ ! -d $SYSTEM32_DIR ] ; then
    SYSTEM32_DIR=$WINEPREFIX/drive_c/windows/system32
fi
cp build_win32/i686-w64-mingw32/libquadmath/.libs/libquadmath-0.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libgfortran/.libs/libgfortran-5.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libobjc/.libs/libobjc-4.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libssp/.libs/libssp-0.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libstdc++-v3/src/.libs/libstdc++-6.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libgcc/shlib/libgcc_s_dw2-1.dll $SYSTEM32_DIR
%if 0%{bootstrap} == 0
cp %{mingw32_bindir}/libwinpthread-1.dll $SYSTEM32_DIR
cp build_win32/i686-w64-mingw32/libgomp/.libs/libgomp-1.dll $SYSTEM32_DIR
%endif

SYSTEM64_DIR=$WINEPREFIX/drive_c/windows/system32
cp build_win64/x86_64-w64-mingw32/libquadmath/.libs/libquadmath-0.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libgfortran/.libs/libgfortran-5.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libobjc/.libs/libobjc-4.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libssp/.libs/libssp-0.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libstdc++-v3/src/.libs/libstdc++-6.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libgcc/shlib/libgcc_s_seh-1.dll $SYSTEM64_DIR
%if 0%{bootstrap} == 0
cp %{mingw64_bindir}/libwinpthread-1.dll $SYSTEM64_DIR
cp build_win64/x86_64-w64-mingw32/libgomp/.libs/libgomp-1.dll $SYSTEM64_DIR
%endif

# According to Kai Tietz (of the mingw-w64 project) it's recommended
# to set the environment variable GCOV_PREFIX_STRIP
export GCOV_PREFIX_STRIP=1000

# Run the testsuite
# Code taken from the native Fedora GCC package to collect testsuite results
pushd build_win32
    make -k check %{?_smp_mflags} || :
    echo ====================TESTING WIN32=========================
    ( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
    echo ====================TESTING WIN32 END=====================
    mkdir testlogs-%{mingw32_target}-%{version}-%{release}
    for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
        ln $i testlogs-%{mingw32_target}-%{version}-%{release}/ || :
    done
    tar cf - testlogs-%{mingw32_target}-%{version}-%{release} | bzip2 -9c \
        | uuencode testlogs-%{mingw32_target}.tar.bz2 || :
    rm -rf testlogs-%{mingw32_target}-%{version}-%{release}
popd

pushd build_win64
    make -k check %{?_smp_mflags} || :
    echo ====================TESTING WIN64=========================
    ( LC_ALL=C ../contrib/test_summary || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}'
    echo ====================TESTING WIN64 END=====================
    mkdir testlogs-%{mingw64_target}-%{version}-%{release}
    for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
        ln $i testlogs-%{mingw64_target}-%{version}-%{release}/ || :
    done
    tar cf - testlogs-%{mingw64_target}-%{version}-%{release} | bzip2 -9c \
        | uuencode testlogs-%{mingw64_target}.tar.bz2 || :
    rm -rf testlogs-%{mingw64_target}-%{version}-%{release}
popd

%endif


%install
%if 0%{bootstrap}
%mingw_make DESTDIR=%{buildroot} install-gcc
%else
%mingw_make_install
%endif

# These files conflict with existing installed files.
rm -rf %{buildroot}%{_infodir}
rm -f %{buildroot}%{_libdir}/libiberty*
rm -f %{buildroot}%{_mandir}/man7/*
rm -rf %{buildroot}%{_datadir}/gcc-%{version}/python

%if 0%{bootstrap} == 0
# Move the DLL's manually to the correct location
mkdir -p %{buildroot}%{mingw32_bindir}
mv    %{buildroot}%{_prefix}/%{mingw32_target}/lib/libatomic-1.dll \
      %{buildroot}%{_prefix}/%{mingw32_target}/lib/libgcc_s_dw2-1.dll \
      %{buildroot}%{_prefix}/%{mingw32_target}/lib/libssp-0.dll \
      %{buildroot}%{_prefix}/%{mingw32_target}/lib/libstdc++-6.dll \
      %{buildroot}%{_prefix}/%{mingw32_target}/lib/libobjc-4.dll \
      %{buildroot}%{_prefix}/%{mingw32_target}/lib/libgfortran-5.dll \
      %{buildroot}%{_prefix}/%{mingw32_target}/lib/libquadmath-0.dll \
%if 0%{bootstrap} == 0
      %{buildroot}%{_prefix}/%{mingw32_target}/lib/libgomp-1.dll \
%endif
      %{buildroot}%{mingw32_bindir}

mkdir -p %{buildroot}%{mingw64_bindir}
mv    %{buildroot}%{_prefix}/%{mingw64_target}/lib/libatomic-1.dll \
      %{buildroot}%{_prefix}/%{mingw64_target}/lib/libgcc_s_seh-1.dll \
      %{buildroot}%{_prefix}/%{mingw64_target}/lib/libssp-0.dll \
      %{buildroot}%{_prefix}/%{mingw64_target}/lib/libstdc++-6.dll \
      %{buildroot}%{_prefix}/%{mingw64_target}/lib/libobjc-4.dll \
      %{buildroot}%{_prefix}/%{mingw64_target}/lib/libgfortran-5.dll \
      %{buildroot}%{_prefix}/%{mingw64_target}/lib/libquadmath-0.dll \
%if 0%{bootstrap} == 0
      %{buildroot}%{_prefix}/%{mingw64_target}/lib/libgomp-1.dll \
%endif
      %{buildroot}%{mingw64_bindir}

mkdir -p %{buildroot}%{ucrt64_bindir}
mv    %{buildroot}%{_prefix}/%{ucrt64_target}/lib/libatomic-1.dll \
      %{buildroot}%{_prefix}/%{ucrt64_target}/lib/libgcc_s_seh-1.dll \
      %{buildroot}%{_prefix}/%{ucrt64_target}/lib/libssp-0.dll \
      %{buildroot}%{_prefix}/%{ucrt64_target}/lib/libstdc++-6.dll \
      %{buildroot}%{_prefix}/%{ucrt64_target}/lib/libobjc-4.dll \
      %{buildroot}%{_prefix}/%{ucrt64_target}/lib/libgfortran-5.dll \
      %{buildroot}%{_prefix}/%{ucrt64_target}/lib/libquadmath-0.dll \
%if 0%{bootstrap} == 0
      %{buildroot}%{_prefix}/%{ucrt64_target}/lib/libgomp-1.dll \
%endif
      %{buildroot}%{ucrt64_bindir}


# Various import libraries are placed in the wrong folder
mkdir -p %{buildroot}%{mingw32_libdir}
mkdir -p %{buildroot}%{mingw64_libdir}
mkdir -p %{buildroot}%{ucrt64_libdir}
mv %{buildroot}%{_prefix}/%{mingw32_target}/lib/* %{buildroot}%{mingw32_libdir}
mv %{buildroot}%{_prefix}/%{mingw64_target}/lib/* %{buildroot}%{mingw64_libdir}
mv %{buildroot}%{_prefix}/%{ucrt64_target}/lib/* %{buildroot}%{ucrt64_libdir}

# Don't want the *.la files.
find %{buildroot} -name '*.la' -delete

%endif

# For some reason there are wrapper libraries created named $target-$target-gcc-$tool
# Drop those files for now as this looks like a bug in GCC
rm -f %{buildroot}%{_bindir}/%{mingw32_target}-%{mingw32_target}-*
rm -f %{buildroot}%{_bindir}/%{mingw64_target}-%{mingw64_target}-*
rm -f %{buildroot}%{_bindir}/%{ucrt64_target}-%{ucrt64_target}-*

%if 0%{bootstrap} == 0
# HACK symlink libssp dll over import lib, otherwise linking with -lssp failes for mysterious reasons
# Needed to build gdb and everything which adds -D_FORTIFY_SOURCES=... and -fstack-protector
ln -sf %{mingw32_bindir}/libssp-0.dll %{buildroot}%{mingw32_libdir}/libssp.dll.a
ln -sf %{mingw64_bindir}/libssp-0.dll %{buildroot}%{mingw64_libdir}/libssp.dll.a
ln -sf %{ucrt64_bindir}/libssp-0.dll %{buildroot}%{ucrt64_libdir}/libssp.dll.a
%endif


%files -n mingw32-gcc
%license gcc/COPYING* COPYING.RUNTIME
%{_bindir}/%{mingw32_target}-gcc
%{_bindir}/%{mingw32_target}-gcc-%{version}
%{_bindir}/%{mingw32_target}-gcc-ar
%{_bindir}/%{mingw32_target}-gcc-nm
%{_bindir}/%{mingw32_target}-gcc-ranlib
%{_bindir}/%{mingw32_target}-gcov
%{_bindir}/%{mingw32_target}-gcov-dump
%{_bindir}/%{mingw32_target}-gcov-tool
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include/
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include-fixed/
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/install-tools/
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/collect2
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/install-tools
%{_mandir}/man1/%{mingw32_target}-gcc.1*
%{_mandir}/man1/%{mingw32_target}-gcov.1*
%{_mandir}/man1/%{mingw32_target}-gcov-dump.1*
%{_mandir}/man1/%{mingw32_target}-gcov-tool.1*

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{_bindir}/%{mingw32_target}-lto-dump
%{mingw32_libdir}/libatomic.a
%{mingw32_libdir}/libatomic.dll.a
%{mingw32_libdir}/libgcc_s.a
%{mingw32_libdir}/libssp.a
%{mingw32_libdir}/libssp.dll.a
%{mingw32_libdir}/libssp_nonshared.a
%{mingw32_libdir}/libstdc++fs.a
%{mingw32_libdir}/libstdc++exp.a
%{mingw32_libdir}/libstdc++.modules.json
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/crtbegin.o
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/crtend.o
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/crtfastmath.o
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libgcov.a
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include/ssp
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include/ssp/*.h
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/g++-mapper-server
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/lto1
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/liblto_plugin.so*
%{_mandir}/man1/%{mingw32_target}-lto-dump.1*
%endif

%files -n mingw64-gcc
%license gcc/COPYING* COPYING.RUNTIME
%{_bindir}/%{mingw64_target}-gcc
%{_bindir}/%{mingw64_target}-gcc-%{version}
%{_bindir}/%{mingw64_target}-gcc-ar
%{_bindir}/%{mingw64_target}-gcc-nm
%{_bindir}/%{mingw64_target}-gcc-ranlib
%{_bindir}/%{mingw64_target}-gcov
%{_bindir}/%{mingw64_target}-gcov-dump
%{_bindir}/%{mingw64_target}-gcov-tool
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include/
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include-fixed/
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/install-tools/
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/collect2
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/install-tools
%{_mandir}/man1/%{mingw64_target}-gcc.1*
%{_mandir}/man1/%{mingw64_target}-gcov.1*
%{_mandir}/man1/%{mingw64_target}-gcov-dump.1*
%{_mandir}/man1/%{mingw64_target}-gcov-tool.1*

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{_bindir}/%{mingw64_target}-lto-dump
%{mingw64_libdir}/libatomic.a
%{mingw64_libdir}/libatomic.dll.a
%{mingw64_libdir}/libgcc_s.a
%{mingw64_libdir}/libssp.a
%{mingw64_libdir}/libssp.dll.a
%{mingw64_libdir}/libssp_nonshared.a
%{mingw64_libdir}/libstdc++fs.a
%{mingw64_libdir}/libstdc++exp.a
%{mingw64_libdir}/libstdc++.modules.json
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/crtbegin.o
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/crtend.o
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/crtfastmath.o
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libgcov.a
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include/ssp
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include/ssp/*.h
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/g++-mapper-server
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/lto1
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/liblto_plugin.so*
%{_mandir}/man1/%{mingw64_target}-lto-dump.1*
%endif

%files -n ucrt64-gcc
%license gcc/COPYING* COPYING.RUNTIME
%{_bindir}/%{ucrt64_target}-gcc
%{_bindir}/%{ucrt64_target}-gcc-%{version}
%{_bindir}/%{ucrt64_target}-gcc-ar
%{_bindir}/%{ucrt64_target}-gcc-nm
%{_bindir}/%{ucrt64_target}-gcc-ranlib
%{_bindir}/%{ucrt64_target}-gcov
%{_bindir}/%{ucrt64_target}-gcov-dump
%{_bindir}/%{ucrt64_target}-gcov-tool
%dir %{_prefix}/lib/gcc/%{ucrt64_target}/%{version}
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/include/
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/include-fixed/
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/install-tools/
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/collect2
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/lto-wrapper
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/install-tools
%{_mandir}/man1/%{ucrt64_target}-gcc.1*
%{_mandir}/man1/%{ucrt64_target}-gcov.1*
%{_mandir}/man1/%{ucrt64_target}-gcov-dump.1*
%{_mandir}/man1/%{ucrt64_target}-gcov-tool.1*

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{_bindir}/%{ucrt64_target}-lto-dump
%{ucrt64_libdir}/libatomic.a
%{ucrt64_libdir}/libatomic.dll.a
%{ucrt64_libdir}/libgcc_s.a
%{ucrt64_libdir}/libssp.a
%{ucrt64_libdir}/libssp.dll.a
%{ucrt64_libdir}/libssp_nonshared.a
%{ucrt64_libdir}/libstdc++fs.a
%{ucrt64_libdir}/libstdc++exp.a
%{ucrt64_libdir}/libstdc++.modules.json
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/crtbegin.o
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/crtend.o
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/crtfastmath.o
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/libgcc.a
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/libgcov.a
%dir %{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/include/ssp
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/include/ssp/*.h
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/g++-mapper-server
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/lto1
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/liblto_plugin.so*
%{_mandir}/man1/%{ucrt64_target}-lto-dump.1*
%endif

%files -n mingw32-gcc-plugin-devel
%dir %{_prefix}/lib/gcc/%{mingw32_target}
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}/plugin
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/plugin/gtype.state
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/plugin/include
%dir %{_libexecdir}/gcc/%{mingw32_target}
%dir %{_libexecdir}/gcc/%{mingw32_target}/%{version}
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/plugin

%files -n mingw64-gcc-plugin-devel
%dir %{_prefix}/lib/gcc/%{mingw64_target}
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}/plugin
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/plugin/gtype.state
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/plugin/include
%dir %{_libexecdir}/gcc/%{mingw64_target}
%dir %{_libexecdir}/gcc/%{mingw64_target}/%{version}
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/plugin

%files -n ucrt64-gcc-plugin-devel
%dir %{_prefix}/lib/gcc/%{ucrt64_target}
%dir %{_prefix}/lib/gcc/%{ucrt64_target}/%{version}
%dir %{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/plugin
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/plugin/gtype.state
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/plugin/include
%dir %{_libexecdir}/gcc/%{ucrt64_target}
%dir %{_libexecdir}/gcc/%{ucrt64_target}/%{version}
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/plugin

%if 0%{bootstrap} == 0
%files -n mingw32-libgcc
%license gcc/COPYING* COPYING.RUNTIME
%{mingw32_bindir}/libatomic-1.dll
%{mingw32_bindir}/libgcc_s_dw2-1.dll
%{mingw32_bindir}/libssp-0.dll

%files -n mingw64-libgcc
%license gcc/COPYING* COPYING.RUNTIME
%{mingw64_bindir}/libatomic-1.dll
%{mingw64_bindir}/libgcc_s_seh-1.dll
%{mingw64_bindir}/libssp-0.dll

%files -n ucrt64-libgcc
%license gcc/COPYING* COPYING.RUNTIME
%{ucrt64_bindir}/libatomic-1.dll
%{ucrt64_bindir}/libgcc_s_seh-1.dll
%{ucrt64_bindir}/libssp-0.dll

%files -n mingw32-libstdc++
%license gcc/COPYING* COPYING.RUNTIME
%{mingw32_bindir}/libstdc++-6.dll

%files -n mingw64-libstdc++
%license gcc/COPYING* COPYING.RUNTIME
%{mingw64_bindir}/libstdc++-6.dll

%files -n ucrt64-libstdc++
%license gcc/COPYING* COPYING.RUNTIME
%{ucrt64_bindir}/libstdc++-6.dll

%files -n mingw32-libgomp
%{mingw32_bindir}/libgomp-1.dll
%{mingw32_libdir}/libgomp.a
%{mingw32_libdir}/libgomp.dll.a
%{mingw32_libdir}/libgomp.spec

%files -n mingw64-libgomp
%{mingw64_bindir}/libgomp-1.dll
%{mingw64_libdir}/libgomp.a
%{mingw64_libdir}/libgomp.dll.a
%{mingw64_libdir}/libgomp.spec

%files -n ucrt64-libgomp
%{ucrt64_bindir}/libgomp-1.dll
%{ucrt64_libdir}/libgomp.a
%{ucrt64_libdir}/libgomp.dll.a
%{ucrt64_libdir}/libgomp.spec
%endif

%files -n mingw32-cpp
%{_bindir}/%{mingw32_target}-cpp
%{_mandir}/man1/%{mingw32_target}-cpp.1*
%dir %{_prefix}/lib/gcc/%{mingw32_target}
%dir %{_prefix}/lib/gcc/%{mingw32_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw32_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw32_target}
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1

%files -n mingw64-cpp
%{_bindir}/%{mingw64_target}-cpp
%{_mandir}/man1/%{mingw64_target}-cpp.1*
%dir %{_prefix}/lib/gcc/%{mingw64_target}
%dir %{_prefix}/lib/gcc/%{mingw64_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw64_target}/%{version}
%dir %{_libexecdir}/gcc/%{mingw64_target}
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1

%files -n ucrt64-cpp
%{_bindir}/%{ucrt64_target}-cpp
%{_mandir}/man1/%{ucrt64_target}-cpp.1*
%dir %{_prefix}/lib/gcc/%{ucrt64_target}
%dir %{_prefix}/lib/gcc/%{ucrt64_target}/%{version}
%dir %{_libexecdir}/gcc/%{ucrt64_target}/%{version}
%dir %{_libexecdir}/gcc/%{ucrt64_target}
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/cc1

%files -n mingw32-gcc-c++
%{_bindir}/%{mingw32_target}-g++
%{_bindir}/%{mingw32_target}-c++
%{_mandir}/man1/%{mingw32_target}-g++.1*
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1plus

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{mingw32_includedir}/c++/
%{mingw32_libdir}/libstdc++.a
%{mingw32_libdir}/libstdc++.dll.a
%{mingw32_libdir}/libstdc++.dll.a-gdb.py
%{mingw32_libdir}/libsupc++.a
%endif

%files -n mingw64-gcc-c++
%{_bindir}/%{mingw64_target}-g++
%{_bindir}/%{mingw64_target}-c++
%{_mandir}/man1/%{mingw64_target}-g++.1*
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1plus

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{mingw64_includedir}/c++/
%{mingw64_libdir}/libstdc++.a
%{mingw64_libdir}/libstdc++.dll.a
%{mingw64_libdir}/libstdc++.dll.a-gdb.py
%{mingw64_libdir}/libsupc++.a
%endif

%files -n ucrt64-gcc-c++
%{_bindir}/%{ucrt64_target}-g++
%{_bindir}/%{ucrt64_target}-c++
%{_mandir}/man1/%{ucrt64_target}-g++.1*
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/cc1plus

# Non-bootstrap files
%if 0%{bootstrap} == 0
%{ucrt64_includedir}/c++/
%{ucrt64_libdir}/libstdc++.a
%{ucrt64_libdir}/libstdc++.dll.a
%{ucrt64_libdir}/libstdc++.dll.a-gdb.py
%{ucrt64_libdir}/libsupc++.a
%endif

%files -n mingw32-gcc-objc
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1obj
%if 0%{bootstrap} == 0
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/include/objc/
%{mingw32_bindir}/libobjc-4.dll
%{mingw32_libdir}/libobjc.a
%{mingw32_libdir}/libobjc.dll.a
%endif

%files -n mingw64-gcc-objc
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1obj
%if 0%{bootstrap} == 0
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/include/objc/
%{mingw64_bindir}/libobjc-4.dll
%{mingw64_libdir}/libobjc.a
%{mingw64_libdir}/libobjc.dll.a
%endif

%files -n ucrt64-gcc-objc
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/cc1obj
%if 0%{bootstrap} == 0
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/include/objc/
%{ucrt64_bindir}/libobjc-4.dll
%{ucrt64_libdir}/libobjc.a
%{ucrt64_libdir}/libobjc.dll.a
%endif

%files -n mingw32-gcc-objc++
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/cc1objplus

%files -n mingw64-gcc-objc++
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/cc1objplus

%files -n ucrt64-gcc-objc++
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/cc1objplus

%files -n mingw32-gcc-gfortran
%{_bindir}/%{mingw32_target}-gfortran
%{_mandir}/man1/%{mingw32_target}-gfortran.1*
%{_libexecdir}/gcc/%{mingw32_target}/%{version}/f951
%if 0%{bootstrap} == 0
%{mingw32_bindir}/libgfortran-5.dll
%{mingw32_bindir}/libquadmath-0.dll
%{mingw32_libdir}/libgfortran.a
%{mingw32_libdir}/libgfortran.dll.a
%{mingw32_libdir}/libgfortran.spec
%{mingw32_libdir}/libquadmath.a
%{mingw32_libdir}/libquadmath.dll.a
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/libcaf_single.a
%{_prefix}/lib/gcc/%{mingw32_target}/%{version}/finclude
%endif

%files -n mingw64-gcc-gfortran
%{_bindir}/%{mingw64_target}-gfortran
%{_mandir}/man1/%{mingw64_target}-gfortran.1*
%{_libexecdir}/gcc/%{mingw64_target}/%{version}/f951
%if 0%{bootstrap} == 0
%{mingw64_bindir}/libgfortran-5.dll
%{mingw64_bindir}/libquadmath-0.dll
%{mingw64_libdir}/libgfortran.a
%{mingw64_libdir}/libgfortran.dll.a
%{mingw64_libdir}/libgfortran.spec
%{mingw64_libdir}/libquadmath.a
%{mingw64_libdir}/libquadmath.dll.a
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/libcaf_single.a
%{_prefix}/lib/gcc/%{mingw64_target}/%{version}/finclude
%endif

%files -n ucrt64-gcc-gfortran
%{_bindir}/%{ucrt64_target}-gfortran
%{_mandir}/man1/%{ucrt64_target}-gfortran.1*
%{_libexecdir}/gcc/%{ucrt64_target}/%{version}/f951
%if 0%{bootstrap} == 0
%{ucrt64_bindir}/libgfortran-5.dll
%{ucrt64_bindir}/libquadmath-0.dll
%{ucrt64_libdir}/libgfortran.a
%{ucrt64_libdir}/libgfortran.dll.a
%{ucrt64_libdir}/libgfortran.spec
%{ucrt64_libdir}/libquadmath.a
%{ucrt64_libdir}/libquadmath.dll.a
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/libcaf_single.a
%{_prefix}/lib/gcc/%{ucrt64_target}/%{version}/finclude
%endif


%changelog
* Fri Aug 15 2025 Sandro Mani <manisandro@gmail.com> - 15.2.1-1
- Update to 15.2.1 (20250808)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 15.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 16 2025 Sandro Mani <manisandro@gmail.com> - 15.1.1-1
- Update to 15.1.1 (20250521)

* Sun Feb 16 2025 Sandro Mani <manisandro@gmail.com> - 15.0.1-1
- Update to 15.0.1 (20250204)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 14.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Oct 06 2024 Neal Gompa <ngompa@fedoraproject.org> - 14.2.1-3
- Rebuild on fixed mingw-crt

* Mon Sep 30 2024 Sandro Mani <manisandro@gmail.com> - 14.2.1-2
- Rebuild for fixed default msvcrt in mingw-crt

* Tue Aug 27 2024 Sandro Mani <manisandro@gmail.com> - 14.2.1-1
- Update to 14.2.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 14.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Sandro Mani <manisandro@gmail.com> - 14.1.1-4
- Update to 20240701 snapshot

* Mon Jun 10 2024 Sandro Mani <manisandro@gmail.com> - 14.1.1-3
- Update to 20240607 snapshot

* Fri Jun 07 2024 Zephyr Lykos <fedora@mochaa.ws> - 14.1.1-2
- Build GCC with plugin support

* Sat May 11 2024 Sandro Mani <manisandro@gmail.com> - 14.1.1-1
- Update to 14.1.1

* Wed Feb 07 2024 Sandro Mani <manisandro@gmail.com> - 14.0.1-1
- Update to 14.0.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 13.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jul 30 2023 Sandro Mani <manisandro@gmail.com> - 13.2.1-1
- Update to 13.2.1 (20230728)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 13.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 26 2023 Sandro Mani <manisandro@gmail.com> - 13.1.1-4
- Update to gcc 20230426 snapshot

* Tue Mar 28 2023 Sandro Mani <manisandro@gmail.com> - 13.0.1-3
- Update to 20230324 snapshot

* Fri Mar 24 2023 Sandro Mani <manisandro@gmail.com> - 13.0.1-2
- Split out libstdc++ (#2181524)

* Thu Mar 09 2023 Sandro Mani <manisandro@gmail.com> - 13.0.1-1
- Update to 13.0.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Florian Weimer <fweimer@redhat.com> - 12.2.1-6
- Apply upstream patches to improve C99 compatibility of configure scripts

* Wed Jan 04 2023 Sandro Mani <manisandro@gmail.com> - 12.2.1-5
- Update to 20221121 snapshot

* Tue Nov 15 2022 Sandro Mani <manisandro@gmail.com> - 12.2.1-4
- Fix incorrect requires

* Fri Jul 22 2022 Sandro Mani <manisandro@gmail.com> - 12.1.1-3
- Update to 20220628 snapshot

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 09 2022 Sandro Mani <manisandro@gmail.com> - 12.1.1-1
- GCC 12.1 release

* Wed May 04 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-11
- Rebuild for standard dll provides move to mingw-crt (bootstrap=0)

* Tue May 03 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-10
- Rebuild for standard dll provides move to mingw-crt (bootstrap=1, enable_libgomp=0)

* Sun May 01 2022 Thierry Vignaud <tvignaud@redhat.com> 12.0.1-9
- Fix missing requires on *-libgcc whose split broke building packages
  linking with -lssp

* Wed Apr 27 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-8
- Bump

* Wed Apr 27 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-7
- Rebuild for mingw-w64-10.0.0 (bootstrap=0, enable_libgomp=1)

* Tue Apr 26 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-6
- Rebuild for mingw-w64-10.0.0 (bootstrap=0, enable_libgomp=0)

* Tue Apr 26 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-5
- Rebuild for mingw-w64-10.0.0 (bootstrap=1, enable_libgomp=0)

* Tue Apr 26 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-4
- Update to 20220413 snapshot
- Move runtime dlls to subpackage

* Wed Mar 30 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-3
- Re-add --enable-threads=posix

* Tue Mar 29 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-2
- Drop --enable-threads=posix, it hardcodes -lpthread in the link flags and
  breaks statically linking

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-1
- Update to 12.0.1 (with bootstrap=0, enable_libgomp=1)

* Thu Mar 24 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-0.2
- Update to 12.0.1 (with bootstrap=0, enable_libgomp=0)

* Thu Mar 24 2022 Sandro Mani <manisandro@gmail.com> - 12.0.1-0.1
- Update to 12.0.1 (with bootstrap=1, enable_libgomp=0)

* Wed Feb 23 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 11.2.1-7
- Add ucrt64 target (with bootstrap=0, enable_libgomp=1)

* Wed Feb 23 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 11.2.1-6
- Add ucrt64 target (with bootstrap=1, enable_libgomp=0)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 20 2021 Sandro Mani <manisandro@gmail.com> - 11.2.1-4
- Update to 11.2.1 20211019 snapshot

* Fri Jul 30 2021 Sandro Mani <manisandro@gmail.com> - 11.2.1-3
- Update to 11.2.1

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 09 2021 Sandro Mani <manisandro@gmail.com> - 11.1.1-1
- Update to 11.1.1 (full build)

* Thu Jul 08 2021 Sandro Mani <manisandro@gmail.com> - 11.1.1-0.2
- Update to 11.1.1 (bootstrap 2)

* Thu Jul 08 2021 Sandro Mani <manisandro@gmail.com> - 11.1.1-0.1
- Update to 11.1.1 (bootstrap)

* Mon Apr 26 2021 Sandro Mani <manisandro@gmail.com> - 10.3.1-1
- Update to 10.3.1

* Thu Jan 28 2021 Richard W.M. Jones <rjones@redhat.com> - 10.2.1-6
- Bump and rebuild for s390.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 12:33:56 CET 2021 Sandro Mani <manisandro@gmail.com> - 10.2.1-2
- Rebuild (mingw-w64)

* Thu Dec 10 2020 Paolo Bonzini <pbonzini@redhat.com> - 10.2.1-3
- Adjust ISL/CLOOG conditionals to look the same as native GCC

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 10.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Sandro Mani <manisandro@gmail.com> - 10.2.1-1
- Update to 10.2.1

* Mon Jul 20 2020 Jeff Law <law@redhat.com> - 10.1.1-4
- Fix broken configure tests compromised by LTO
- Add autoconf to BuildRequires

* Sun Jul 19 2020 Sandro Mani <manisandro@gmail.com> - 10.1.1-3
- Hack: symlink libssp-0.dll over libssp.dll.a

* Sat Jun 20 2020 Sandro Mani <manisandro@gmail.com> - 10.1.1-2
- Full build

* Sat Jun 20 2020 Sandro Mani <manisandro@gmail.com> - 10.1.1-1
- Update to 10.1.1 (bootstrap)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Sandro Mani <manisandro@gmail.com> - 9.2.1-5
- Bump

* Wed Oct  9 2019 Jerry James <loganjerry@gmail.com> - 9.2.1-4
- Rebuild for mpfr 4

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 9.2.1-3
- Switch to dwarf-2 exceptions for mingw32 (full build)

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 9.2.1-2
- Switch to dwarf-2 exceptions for mingw32 (bootstrap)

* Tue Aug 27 2019 Sandro Mani <manisandro@gmail.com> - 9.2.1-1
- Update to 9.2.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Sandro Mani <manisandro@gmail.com> - 9.1.1-1
- Update to 9.1.1

* Tue Apr 16 2019 Sandro Mani <manisandro@gmail.com> - 8.3.0-2
- Backport patch for gcc #88568

* Fri Feb 22 2019 Kalev Lember <klember@redhat.com> - 8.3.0-1
- Update to 8.3.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 05 2018 Sandro Mani <manisandro@gmail.com> - 8.2.0-3
- Backport patch for gcc#87137

* Wed Aug 08 2018 Sandro Mani <manisandro@gmail.com> - 8.2.0-2
- Cleanup snapshot handling
- Add patch for gcc #86593

* Fri Jul 27 2018 Kalev Lember <klember@redhat.com> - 8.2.0-1
- Update to 8.2.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Kalev Lember <klember@redhat.com> - 8.1.0-1
- Update to 8.1.0

* Sat Apr 07 2018 Rafael Kitover <rkitover@gmail.com> - 7.2.0-3
- Add patch to disable weakrefs in libstdc++

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 22 2017 Kalev Lember <klember@redhat.com> - 7.2.0-1
- Update to 7.2.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Kalev Lember <klember@redhat.com> - 7.1.0-1
- Update to 7.1.0

* Mon Feb 13 2017 Kalev Lember <klember@redhat.com> - 7.0.1-0.1.svn.20170212.r245378
- Update to gcc 7 20170212 snapshot (rev 245378)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Kalev Lember <klember@redhat.com> - 6.3.0-1
- Update to 6.3.0

* Tue Aug 23 2016 Kalev Lember <klember@redhat.com> - 6.2.0-1
- Update to 6.2.0

* Wed May 04 2016 Kalev Lember <klember@redhat.com> - 6.1.0-1
- Update to 6.1.0

* Sun Mar 27 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 6.0.0-0.2.svn.20160320.r234355
- Update to gcc 6 20160320 snapshot (rev 234355)

* Thu Feb  4 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 6.0.0-0.1.svn.20160131.r233023
- Update to gcc 6 20160131 snapshot (rev 233023)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 08 2015 Kalev Lember <klember@redhat.com> - 5.3.0-1
- Update to 5.3.0

* Wed Aug  5 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-2
- Export additional symbols needed to resolve boost build failure with GCC 5
- Resolves RHBZ #1218290, GCC #66030

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0

* Sat Apr 11 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.4.svn.20150405.r221873
- Switch back to the old libstdcxx c++98 ABI on Fedora 22 only
  (This was also done for the native Fedora GCC package)

* Fri Apr 10 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.3.svn.20150405.r221873
- Update to gcc 5 20150405 snapshot (rev 221873)

* Mon Mar 23 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.svn.20150322.r221575
- Update to gcc 5 20150322 snapshot (rev 221575)

* Sat Mar  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.svn.20150301.r221092
- Update to gcc 5 20150301 snapshot (rev 221092)

* Thu Jan 29 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.2-2
- The package cloog-ppl-devel was renamed to cloog-devel in rawhide

* Wed Dec  3 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.2-1
- Update to 4.9.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-3
- Use /usr/lib instead of %%{_libdir} (like also is done in
  the native gcc and cross-gcc packages)

* Mon Jul 28 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-2
- Really enable std::threads support

* Fri Jul 18 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-1
- Update to gcc 4.9.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.0-1
- Update to gcc 4.9.0

* Sun Apr 13 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.0-0.1.rc1
- Update to gcc 4.9.0 RC1

* Fri Jan 10 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.2-2
- Dropped xmmintrin patch as the issue is resolved in mingw-w64 3.1.0

* Sat Oct 19 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2
- Build with C++11 std::thread support (F21+ only)

* Fri Sep 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-4
- Rebuild against winpthreads

* Sat Aug  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-3
- Own the folders %%{_libexecdir}/gcc/%%{mingw32_target}/%%{version},
  %%{_libexecdir}/gcc/%%{mingw32_target}, %%{_libexecdir}/gcc/%%{mingw64_target}
  and %%{_libexecdir}/gcc/%%{mingw64_target}/%%{version}

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1

* Sat Jun  1 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-4
- Revised patch for GCC bug #56742

* Sun Apr 14 2013 Nicola Fontana <ntd@entidi.it> - 4.8.0-3
- Dropped dependency on PPL (#951914)

* Sun Apr 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-2
- Fix optimization bug which can lead to uncaught throw (SEH related) (GCC bug #56742)

* Sat Mar 23 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-1
- Update to gcc 4.8.0 final

* Mon Mar 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.6.svn.20130310.r196584
- Update to gcc 4.8 20130310 snapshot (rev 196584)

* Fri Feb  8 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.5.svn.20130203.r195703
- Update to gcc 4.8 20130203 snapshot (rev 195703)

* Sun Jan 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.4.svn.20130120.r195326
- Update to gcc 4.8 20130120 snapshot (rev 195326)

* Fri Jan 18 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.3.svn.20130113.r195137
- Make sure the header xmmintrin.h is C++ compatible. Fixes build
  failure in the mingw-qt5-qtbase package

* Wed Jan 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.2.svn.20130113.r195137
- Update to gcc 4.8 20130113 snapshot (rev 195137)

* Sat Jan 12 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-0.1.svn.20130106.r194954
- Update to gcc 4.8 20130106 snapshot (rev 194954)
- The win64 compiler now uses SEH by default

* Wed Jan  2 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.2-7
- Backported imported fix regarding virtual thunks as recommended
  by upstream mingw-w64 developers (gcc bug #55171)

* Tue Dec 04 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.2-6
- Re-enable libgomp support

* Mon Dec 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.2-5
- Temporary build without libgomp support because of the broken circular
  dependency between mingw-gcc and mingw-pthreads which was caused by the
  latest PPL update

* Mon Dec 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.2-4
- Made this package compatible with RHEL6 and RHEL7
- Build with --disable-ppl-version-check (fixes FTBFS against latest PPL)

* Fri Nov 30 2012 Tom Callaway <spot@fedoraproject.org> - 4.7.2-3
- rebuild for new ppl/cloog

* Mon Oct 15 2012 Jon Ciesla <limbugher@gmail.com> - 4.7.2-2
- Provides: bundled(libiberty)

* Fri Sep 21 2012 Kalev Lember <kalevlember@gmail.com> - 4.7.2-1
- Update to 4.7.2

* Sat Jul 21 2012 Kalev Lember <kalevlember@gmail.com> - 4.7.1-3
- Revert back to 4.7.1 final

* Wed Jul 18 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.1-2.20120718
- Update to gcc 4.7 20120718 snapshot

* Sun Jul 15 2012 Kalev Lember <kalevlember@gmail.com> - 4.7.1-1
- Update to 4.7.1

* Wed Apr 04 2012 Kalev Lember <kalevlember@gmail.com> - 4.7.0-2
- Fix the build
- Switch to the release tarball
- Disable the testsuite again to avoid breaking build on arches where
  wine is unavailable

* Wed Mar 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-1.20120322
- Update to gcc 4.7.0 final release (20120322 snapshot)
- Dropped upstreamed patches
- Enable the testsuite

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.9.20120224
- Re-enable libgomp support

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.8.20120224
- Perform a regular build

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.7.20120224
- Added support for both win32 and win64 targets
- Perform a bootstrap build
- Split out the OpenMP pieces to mingw{32,64}-libgomp packages to avoid
  forced dependency on mingw{32,64}-pthreads
- Added support for running the testsuite for both win32 and win64 targets
- Added a %%global called enable_winpthreads which can be used to enable
  C++11 threads support (requires winpthreads instead of pthreads-w32)

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.6.20120224
- Renamed the source package to mingw-gcc (RHBZ #673788)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.5.20120224
- Re-enable libgomp support

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.4.20120224
- Perform a regular build

* Sat Feb 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.3.20120224
- Update to gcc 4.7 20120224 snapshot
- Perform a bootstrap build using mingw-w64
- Dropped the /lib/i686-pc-mingw32-cpp symlink
- Dropped the float.h patch as it isn't needed anymore with mingw-w64
- Added some patches which upstream mingw-w64 recommends us to apply

* Fri Jan 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.2.20120126
- Update to gcc 4.7 20120126 snapshot (fixes mingw32-qt build failure)

* Tue Jan 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-0.1.20120106
- Update to gcc 4.7 20120106 snapshot

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.6.1-3.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 4.6.1-3.1
- rebuild with new gmp

* Fri Aug 26 2011 Kalev Lember <kalevlember@gmail.com> - 4.6.1-3
- Fix float.h inclusion when gcc's headers precede mingrt in include path

* Fri Aug 19 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.6.1-2
- Build against ppl and cloog

* Mon Jun 27 2011 Kalev Lember <kalev@smartlink.ee> - 4.6.1-1
- Update to 4.6.1

* Sat May 21 2011 Kalev Lember <kalev@smartlink.ee> - 4.5.3-3
- Rebuilt with automatic dep extraction and removed all manual
  mingw32(...) provides / requires
- Cleaned up the spec file from cruft not needed with latest rpm

* Tue May 10 2011 Kalev Lember <kalev@smartlink.ee> - 4.5.3-2
- Disable plugin support with a configure option, instead of deleting
  the files in the install section
- Use the %%{_mingw32_target} macro in files section

* Sat Apr 30 2011 Kalev Lember <kalev@smartlink.ee> - 4.5.3-1
- Update to 4.5.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Aug 05 2010 Kalev Lember <kalev@smartlink.ee> - 4.5.1-1
- Update to 4.5.1

* Thu May 13 2010 Kalev Lember <kalev@smartlink.ee> - 4.5.0-1
- Update to vanilla gcc 4.5.0
- Drop patches specific to Fedora native gcc.
- BuildRequires libmpc-devel and zlib-devel
- Added Provides for additional shared language runtime DLLs

* Thu Dec 17 2009 Chris Bagwell <chris@cnpbagwell.com> - 4.4.2-2
- Enable libgomp support.

* Sun Nov 22 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.2-1
- Update to gcc 4.4.2 20091114 svn 154179, which includes
  VTA backport from 4.5 branch.
- Patches taken from native Fedora gcc-4.4.2-10.

* Fri Sep 18 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-3
- Require mingw32-binutils >= 2.19.51.0.14 for %%gnu_unique_object support.

* Thu Sep 03 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-2
- Update to gcc 4.4.1 20090902 svn 151328.
- Patches taken from native Fedora gcc-4.4.1-8.
- Another license update to keep it in sync with native gcc package.

* Sun Aug 23 2009 Kalev Lember <kalev@smartlink.ee> - 4.4.1-1
- Update to gcc 4.4.1 20090818 svn 150873.
- Patches taken from native Fedora gcc-4.4.1-6.
- Replaced %%define with %%global and updated %%defattr.
- Changed license to match native Fedora gcc package.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.7
- New native Fedora version gcc 4.4.0 20090319 svn 144967.
- Enable _smp_mflags.

* Wed Mar  4 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.6
- Fix libobjc and consequently Objective C and Objective C++ compilers.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.0-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.4
- Rebuild for mingw32-gcc 4.4

* Thu Feb 19 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-0.2
- Move to upstream version 4.4.0-20090216 (same as Fedora native version).
- Added FORTRAN support.
- Added Objective C support.
- Added Objective C++ support.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-12
- Rebuild against latest filesystem package.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-11
- Remove obsoletes for a long dead package.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-10
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-9
- Rebuild against mingw32-filesystem 36

* Thu Oct 30 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-8
- Don't BR mpfr-devel for RHEL/EPEL-5 (Levente Farkas).

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-7
- Rename mingw -> mingw32.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-6
- Use RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.3.2-3
- Initial RPM release, largely based on earlier work from several sources.
