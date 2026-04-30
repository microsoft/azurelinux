# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# rpmbuild parameters:
# --with testsuite: Run the testsuite (biarch if possible).  Default is without.
# --with buildisa: Use %%{?_isa} for BuildRequires
# --with asan: gcc -fsanitize=address
# --without python: No python support.
# --with profile: gcc -fprofile-generate / -fprofile-use: Before better
#                 workload gets run it decreases the general performance now.
# --define 'scl somepkgname': Independent packages by scl-utils-build.
# --define 'tests "TEST1 ... TESTN": Limit testing to specified tests.

# Turn off the brp-python-bytecompile automagic
%global _python_bytecompile_extra 0

# Disable LTO until upstream fixes GDB's ODR woes.
%define _lto_cflags %{nil}

%{?scl:%scl_package gdb}
%{!?scl:
 %global pkg_name %{name}
 %global _root_prefix %{_prefix}
 %global _root_datadir %{_datadir}
 %global _root_libdir %{_libdir}
}

# If we're on Fedora or RHEL 9+, we will build the gdb-minimal package.
# Never build the -minimal package on SCLs, since it's unneeded there.
%if 0%{?fedora} || (0%{?rhel} > 8 && 0%{!?scl:1})
  %global _build_minimal 1
%endif

# Include support for Guile? This is enabled on RHEL 8 and
# Fedora < 38.
%if (0%{?fedora:1} && 0%{?fedora} < 38) || (0%{?rhel:1} && 0%{?rhel} == 8)
  %define use_guile 1
%endif

Name: %{?scl_prefix}gdb

# Freeze it when GDB gets branched
%global snapsrc    20220501
# See timestamp of source gnulib installed into gnulib/ .
%global snapgnulib 20220501
%global tarname gdb-%{version}
Version: 17.1

# The release always contains a leading reserved number, start it at 1.
# `upstream' is not a part of `name' to stay fully rpm dependencies compatible for the testing.
Release: 4%{?dist}

License: GPL-3.0-or-later AND BSD-3-Clause AND FSFAP AND LGPL-2.1-or-later AND GPL-2.0-or-later AND LGPL-2.0-or-later AND LicenseRef-Fedora-Public-Domain AND GFDL-1.3-or-later AND LGPL-2.0-or-later WITH GCC-exception-2.0 AND GPL-3.0-or-later WITH GCC-exception-3.1 AND GPL-2.0-or-later WITH GNU-compiler-exception AND MIT
# Do not provide URL for snapshots as the file lasts there only for 2 days.
# ftp://sourceware.org/pub/gdb/releases/FIXME{tarname}.tar.xz
Source: ftp://sourceware.org/pub/gdb/releases/%{tarname}.tar.xz
URL: https://gnu.org/software/gdb/

# For our convenience
%global gdb_src %{tarname}
%global gdb_build build-%{_target_platform}
%if 0%{?_build_minimal}
  %global gdb_build_minimal %{gdb_build}-minimal
%endif

# error: Installed (but unpackaged) file(s) found: /usr/lib/debug/usr/bin/gdb-gdb.py
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/PBOJDOFMWTRV3ZOKNV5HN7IBX5EPHDHF/
%undefine _debuginfo_subpackages

# For DTS RHEL<=7 GDB it is better to use none than a Requires dependency.
%if 0%{!?rhel:1}
Recommends: dnf-command(debuginfo-install)
%endif

%if 0%{!?scl:1}
Summary: A GNU source-level debugger for C, C++, Fortran, Go and other languages
Requires: gdb-headless%{?_isa} = %{version}-%{release}

%description
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Fortran, Go, and other languages, by executing them in a controlled
fashion and printing their data.

If you want to use GDB for development purposes, you should install
the 'gdb' package which will install 'gdb-headless' and possibly other
useful packages too.

%package headless

# gdb-add-index also uses 'readelf' and 'objcopy', both of which are
# in the binutils package.  (BZ 2275274)
Requires: binutils
%endif
# endif !scl

Summary: A GNU source-level debugger for C, C++, Fortran, Go and other languages

%ifarch %{arm} riscv64
  %global have_inproctrace 0
%else
  %global have_inproctrace 1
%endif

# https://fedorahosted.org/fpc/ticket/43 https://fedorahosted.org/fpc/ticket/109
Provides: bundled(libiberty) = %{snapsrc}
Provides: bundled(gnulib) = %{snapgnulib}
# The libraries in the top-level directory (libbfd, libopcodes,
# libctf) are covered by the "bundled(binutils)" below.  See ticket
# #109, as mentioned above.
Provides: bundled(binutils) = %{snapsrc}
# https://fedorahosted.org/fpc/ticket/130
Provides: bundled(md5-gcc) = %{snapsrc}

# https://fedoraproject.org/wiki/Packaging:Guidelines#BuildRequires_and_.25.7B_isa.7D
%if 0%{?_with_buildisa:1} || 0%{?_with_testsuite:1}
  %global buildisa %{?_isa}
%else
  %global buildisa %{nil}
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1209492

# rpm-suggestions.py needs to import rpm which is found in python3-rpm.
Recommends: python3-rpm

BuildRequires: gcc-c++

# GDB patches have the format `gdb-<version>-bz<red-hat-bz-#>-<desc>.patch'.
# They should be created using patch level 1: diff -up ./gdb (or gdb-6.3/gdb).

#=
#push=Should be pushed upstream.
#fedora=Should stay as a Fedora patch.
#fedoratest=Keep it in Fedora only as a regression test safety.

# Cleanup any leftover testsuite processes as it may stuck mock(1) builds.
#=push+jan
Source2: gdb-orphanripper.c

# /etc/gdbinit (from Debian but with Fedora compliant location).
#=fedora
Source4: gdbinit

# Include the auto-generated file containing the "Patch:" directives.
# See README.local-patches for more details.
Source9998: _gdb.spec.Patch.include
Source9999: _gdb.spec.patch.include
%include %{SOURCE9998}

BuildRequires: readline-devel%{buildisa} >= 7.0
BuildRequires: ncurses-devel%{buildisa} texinfo gettext flex bison
BuildRequires: expat-devel%{buildisa}
# gdb/minidebug.c uses the xz library to handle compressed debuginfo.
BuildRequires: xz-devel%{buildisa}
# dlopen() no longer makes rpm-libsFIXME{?_isa} (it's .so) a mandatory dependency.
BuildRequires: rpm-devel%{buildisa}
BuildRequires: zlib-devel%{buildisa} libselinux-devel%{buildisa}
%if 0%{!?_without_python:1}
  %global __python %{__python3}
BuildRequires: python3-devel%{buildisa}
%endif
# gdb-doc in PDF, see: https://bugzilla.redhat.com/show_bug.cgi?id=919891#c10
BuildRequires: texinfo-tex
BuildRequires: texlive-collection-latexrecommended
# Permit rebuilding *.[0-9] files even if they are distributed in gdb-*.tar:
BuildRequires: /usr/bin/pod2man
BuildRequires: libbabeltrace-devel%{buildisa}
%if %{defined use_guile}
    %if 0%{!?rhel:1}
BuildRequires: guile22-devel%{buildisa}
    %endif
    # Guile is only supported prior to RHEL9, where it was called "guile".
    %if 0%{?rhel:1} && 0%{?rhel} < 9
BuildRequires: guile-devel%{buildisa}
    %endif
%endif

# Add support for Intel Processor Trace on eligible architectures.
%global have_libipt 0
%ifarch %{ix86} x86_64
%global have_libipt 1
BuildRequires: libipt-devel%{buildisa}
%endif

# See https://bugzilla.redhat.com/show_bug.cgi?id=1593280
# DTS RHEL-6 has mpfr-2 while GDB requires mpfr-3 on RHEL-7, RHEL-8, and
# Fedora < 32, and mpfr-4 on Fedora 32+ and RHEL-9+.
BuildRequires: mpfr-devel%{buildisa}
BuildRequires: source-highlight-devel
%if 0%{!?rhel:1}
BuildRequires: xxhash-devel
%endif

# Include debuginfod support.
BuildRequires: elfutils-debuginfod-client-devel

# Workaround for missing boost-devel dependency (rhbz 1718480)
BuildRequires: boost-devel

%if 0%{?_with_testsuite:1}

# Ensure the devel libraries are installed for both multilib arches.
%global bits_local %{?_isa}
%global bits_other %{?_isa}
%ifarch ppc
  %global bits_other (%{__isa_name}-64)
%endif

%ifarch x86_64
  %if 0%{?fedora:1} || 0%{?rhel} < 10
    %global bits_other (%{__isa_name}-32)
  %endif
%endif

BuildRequires: sharutils dejagnu

# Test supported SCL toolchain components.
BuildRequires: %{?scl_testing_prefix}gcc %{?scl_testing_prefix}gcc-c++ %{?scl_testing_prefix}gcc-gfortran

# Fedora supports Objective C.
%if 0%{!?rhel:1}
BuildRequires: gcc-objc
%endif

# We don't support gcc-gdb-plugin on RHEL anymore.
# Note: kevinb disabled this entirely, but we should probably just get rid of it.
%if 0
%if 0%{!?rhel:1}
BuildRequires: gcc-gdb-plugin%{?_isa}
%endif
%endif

BuildRequires: systemtap-sdt-devel
BuildRequires: opencl-headers ocl-icd-devel%{bits_local} ocl-icd-devel%{bits_other}

%if 0%{!?rhel:1}
BuildRequires: gcc-go
BuildRequires: libgo-devel%{bits_local} libgo-devel%{bits_other}
%endif

%if 0%{!?rhel:1}
  %ifnarch s390x
# Fedora s390x does not support fpc.
BuildRequires: fpc
  %endif
%endif

%if 0%{!?rhel:1}
BuildRequires: gcc-gnat
BuildRequires: libgnat%{bits_local} libgnat%{bits_other}
%endif
BuildRequires: glibc-devel%{bits_local} glibc-devel%{bits_other}
BuildRequires: libgcc%{bits_local} libgcc%{bits_other}
BuildRequires: libgfortran%{bits_local} libgfortran%{bits_other}
# libstdc++-devel of matching bits is required only for g++ -static.
BuildRequires: libstdc++%{bits_local} libstdc++%{bits_other}
%ifarch %{ix86} x86_64
BuildRequires: libquadmath%{bits_local} libquadmath%{bits_other}
%endif
# multilib glibc-static is open Bug 488472:
%if 0%{?rhel:1}
BuildRequires: glibc-static%{bits_other}
%endif
BuildRequires: valgrind%{bits_local} valgrind%{bits_other}
BuildRequires: xz
BuildRequires: rust
BuildRequires: elfutils-debuginfod
%endif
# endif _with_testsuite
BuildRequires: make gmp-devel

%{?scl:Requires:%scl_runtime}

# FIXME: The text needs to be duplicated to prevent 2 empty heading lines.
%if 0%{!?scl:1}
%description headless
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.
%else
%description
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.
%endif

%if 0%{?_build_minimal}
%package minimal
Summary: A GNU source-level debugger for C, C++, Fortran, Go and other languages (minimal version)
# gdb-add-index is shared with gdb-headless and it must be from same version
Conflicts: %{name}-headless < %{version}-%{release}
Conflicts: %{name}-headless > %{version}-%{release}

%description minimal
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Fortran, Go, and other languages, by executing them in a controlled
fashion and printing their data.

This package provides a minimal version of GDB, tailored to be used by
the Fedora buildroot.  It should probably not be used by end users.
%endif
# endif _build_minimal

%package gdbserver
Summary: A standalone server for GDB (the GNU source-level debugger)

%description gdbserver
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Fortran, Go, and other languages, by executing them in a controlled
fashion and printing their data.

This package provides a program that allows you to run GDB on a different
machine than the one which is running the program being debugged.

%package doc
Summary: Documentation for GDB (the GNU source-level debugger)
License: GFDL
BuildArch: noarch
%if 0%{?scl:1}
# As of F-28, packages won't need to call /sbin/install-info by hand
# anymore.  We make an exception for DTS here.
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/MP2QVJZBOJZEOQO2G7UB2HLXKXYPF2G5/
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
%endif

%description doc
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

This package provides INFO, HTML and PDF user manual for GDB.

%prep
%setup -q -n %{gdb_src}

# Files have `# <number> <file>' statements breaking VPATH / find-debuginfo.sh .
(cd gdb;rm -fv $(perl -pe 's/\\\n/ /' <Makefile.in|sed -n 's/^YYFILES = //p'))

# *.info* is needlessly split in the distro tar; also it would not get used as
# we build in GDB_BUILD, just to be sure.
find -name "*.info*"|xargs rm -f

# Apply patches defined on _gdb.spec.Patch.include

# Include the auto-generated patch directives.
# See README.local-patches for more details.
%include %{SOURCE9999}

find -name "*.orig" | xargs rm -f
! find -name "*.rej" # Should not happen.

# In the past a distro name prefix was added to the version string in
# version.in.
#
# However, placing text at the start of version.in can cause problems;
# GDB will have a version string that starts with text rather than a
# number as is the case with upstream GDB, and for most (all?) other
# distros.
#
# GDB's version string is exposed to users as part of the Python API,
# and it is not uncommon for users to try and grok the version number
# from this string.  Having Fedora/RHEL GDB not start with the major
# version number can be unexpected, and might cause tools/script that
# work for other builds of GDB to fail with Fedora/RHEL GDB.
#
# So, we switched to use the more standard --with-pkgversion configure
# option.  This ensures the distro name is still included in the 'gdb
# --version' output, but the text is no longer part of the string
# exposed in the Python API.
#
# Unfortunately, for RHEL the dist_name macro is not defined.  At
# least not on RHEL 9 or earlier.  So, if dist_name is not defined,
# but the rhel macro is, then we use a hard-coded RHEL appropriate
# string.
#
# FIXME: It would be nice to rewrite this using elif, but this is not
# supported on older (pre 9) RHEL systems.

%if 0%{?dist_name:1}
  %global pkgversion_configure_flag --with-pkgversion=%{dist_name}
%else
  %if 0%{?fedora:1}
    %global pkgversion_configure_flag --with-pkgversion=Fedora Linux
  %endif

  %if 0%{?rhel:1}
    %global pkgversion_configure_flag --with-pkgversion=Red Hat Enterprise Linux
  %endif
%endif

# Change the version that gets printed by GDB.  The 'version' here is
# usually the same as the original upstream version on which we are
# based.  The 'release' is new information we're adding and identifies
# the modifications we've made to upstream.
cat > gdb/version.in << _FOO
%{?version_prefix:%version_prefix }%{version}-%{release}
_FOO

# Remove the info and other generated files added by the FSF release
# process.
rm -f libdecnumber/gstdint.h
rm -f bfd/doc/*.info
rm -f bfd/doc/*.info-*
rm -f gdb/doc/*.info
rm -f gdb/doc/*.info-*

mv -f readline/readline/doc readline-doc
rm -rf readline/readline/*
mv -f readline-doc readline/readline/doc

rm -rf zlib texinfo

%build

# A set of common GDB configure flags, which are used for both minimal
# and non-minimal compilations.
COMMON_GDB_CONFIGURE_FLAGS="\
        --prefix=%{_prefix}                                     \
        --libdir=%{_libdir}                                     \
        --sysconfdir=%{_sysconfdir}                             \
        --mandir=%{_mandir}                                     \
        --infodir=%{_infodir}                                   \
        --with-gdb-datadir=%{_datadir}/gdb                      \
        --enable-gdb-build-warnings=,-Wno-unused,-Wno-deprecated-declarations,-Wno-unused-function,-Wno-stringop-overflow\
%ifarch %{ix86}
,-Wno-format-overflow\
%endif
        --enable-build-with-cxx                                 \
%ifnarch %{ix86} alpha ppc s390 s390x x86_64 ppc64 ppc64le %{arm} aarch64 riscv64
        --disable-werror                                        \
%else
        --enable-werror                                         \
%endif
        --with-separate-debug-dir=/usr/lib/debug                \
        --disable-sim                                           \
        --disable-rpath                                         \
        --without-stage1-ldflags                                \
        --disable-libmcheck                                     \
        --with-system-readline                                  \
        --without-libunwind                                     \
        --enable-64-bit-bfd                                     \
        --with-system-zlib                                      \
        --with-lzma                                             \
        --with-debuginfod                                       \
%if 0%{?rhel:1}
        --disable-libctf                                        \
%endif
        --disable-gdb-compile
"

# The base set of targets that Fedora and RHEL support.  These are the
# targets that every GDB build, regardless of host architecture,
# supports debugging.  This means that these targets can be used as
# remote debug targets.
ENABLED_TARGETS="aarch64-linux-gnu,powerpc-linux-gnu,riscv64-linux-gnu,s390-linux-gnu,x86_64-redhat-linux-gnu"

# Fedora, and older RHEL also have 32-bit ARM support.
%if 0%{?fedora:1} || (0%{?rhel:1} && 0%{?rhel} < 10)
ENABLED_TARGETS="$ENABLED_TARGETS,arm-linux-gnu"
%endif

# Identify the build directory with the version of gdb as well as the
# architecture, to allow for mutliple versions to be installed and
# built.
# Initially we're in the GDB_SRC directory.

for fprofile in %{?_with_profile:-fprofile} ""
do

# We will first build the minimal version of GDB.
%if 0%{?_build_minimal}
mkdir %{gdb_build_minimal}$fprofile
cd %{gdb_build_minimal}$fprofile

# The configure flags we will use when building gdb-minimal.
GDB_MINIMAL_CONFIGURE_FLAGS="\
    --without-babeltrace \
    --without-expat \
    --disable-tui \
    --without-python \
    --without-guile \
    --disable-inprocess-agent \
    --without-intel-pt \
    --disable-unit-tests \
    --disable-source-highlight"

# Populate CFLAGS, LDFLAGS, CC, CXX, etc.
%set_build_flags
CFLAGS="$CFLAGS %{?_with_asan:-fsanitize=address}"
LDFLAGS="$LDFLAGS %{?_with_asan:-fsanitize=address}"
CXXFLAGS="$CXXFLAGS %{?_with_asan:-fsanitize=address}"

# --htmldir and --pdfdir are not used as they are used from GDB_BUILD.
../configure                                                    \
        ${COMMON_GDB_CONFIGURE_FLAGS}                           \
        ${GDB_MINIMAL_CONFIGURE_FLAGS}                          \
%if 0%{?pkgversion_configure_flag:1}
        "%{pkgversion_configure_flag}"                          \
%endif
        --with-auto-load-dir='$debugdir:$datadir/auto-load%{?scl::%{_root_datadir}/gdb/auto-load}'      \
        --with-auto-load-safe-path='$debugdir:$datadir/auto-load%{?scl::%{_root_datadir}/gdb/auto-load}'        \
        --enable-targets=${ENABLED_TARGETS}     \
        %{_target_platform}

# Prepare gdb/config.h first.
%make_build CFLAGS="$CFLAGS $FPROFILE_CFLAGS" LDFLAGS="$LDFLAGS $FPROFILE_CFLAGS" V=1 maybe-configure-gdb
perl -i.relocatable -pe 's/^(D\[".*_RELOCATABLE"\]=" )1(")$/${1}0$2/' gdb/config.status

%make_build CFLAGS="$CFLAGS $FPROFILE_CFLAGS" LDFLAGS="$LDFLAGS $FPROFILE_CFLAGS" V=1

cd ..
%endif
# endif _build_minimal

# Now we build the full GDB.
mkdir %{gdb_build}$fprofile
cd %{gdb_build}$fprofile

export CFLAGS="$RPM_OPT_FLAGS %{?_with_asan:-fsanitize=address} -DDNF_DEBUGINFO_INSTALL"
export LDFLAGS="%{?__global_ldflags} %{?_with_asan:-fsanitize=address}"
export CXXFLAGS="$CFLAGS"

# The configure flags we will use when building the full GDB.
GDB_FULL_CONFIGURE_FLAGS="\
        --with-system-gdbinit=%{_sysconfdir}/gdbinit            \
        --with-babeltrace                                       \
        --with-expat                                            \
$(: ppc64 host build crashes on ppc variant of libexpat.so )    \
        --without-libexpat-prefix                               \
        --enable-tui                                            \
%if 0%{!?_without_python:1}
        --with-python=%{__python}                               \
%else
        --without-python                                        \
%endif
%if %{defined use_guile}
        --with-guile                                            \
%else
        --without-guile                                         \
%endif
%if %{have_inproctrace}
        --enable-inprocess-agent                                \
%else
        --disable-inprocess-agent                               \
%endif
%if %{have_libipt}
        --with-intel-pt                                         \
%else
        --without-intel-pt                                      \
%endif
%if 0%{!?rhel:1}
        --with-xxhash                                           \
%endif
        --enable-unit-tests"

# --htmldir and --pdfdir are not used as they are used from GDB_BUILD.
../configure                                                    \
        ${COMMON_GDB_CONFIGURE_FLAGS}                           \
        ${GDB_FULL_CONFIGURE_FLAGS}                             \
%if 0%{?pkgversion_configure_flag:1}
        "%{pkgversion_configure_flag}"                          \
%endif
        --with-auto-load-dir='$debugdir:$datadir/auto-load%{?scl::%{_root_datadir}/gdb/auto-load}'      \
        --with-auto-load-safe-path='$debugdir:$datadir/auto-load%{?scl::%{_root_datadir}/gdb/auto-load}'        \
        --enable-targets=${ENABLED_TARGETS}     \
        %{_target_platform}

if [ -z "%{!?_with_profile:no}" ]
then
  # Run all the configure tests being incompatible with $FPROFILE_CFLAGS.
  %make_build configure-host configure-target
  %make_build clean

  # Workaround -fprofile-use:
  # linux-x86-low.c:2225: Error: symbol `start_i386_goto' is already defined
  %make_build -C gdb/gdbserver linux-x86-low.o
fi

# Global CFLAGS would fail on:
# conftest.c:1:1: error: coverage mismatch for function 'main' while reading counter 'arcs'
if [ "$fprofile" = "-fprofile" ]
then
  FPROFILE_CFLAGS='-fprofile-generate'
elif [ -z "%{!?_with_profile:no}" ]
then
  FPROFILE_CFLAGS='-fprofile-use'
  # We cannot use -fprofile-dir as the bare filenames clash.
  (cd ../${builddir}-fprofile;
   # It was 333 on x86_64.
   test $(find -name "*.gcda"|wc -l) -gt 300
   find -name "*.gcda" | while read -r i
   do
     ln $i ../${builddir}/$i
   done
  )
else
  FPROFILE_CFLAGS=""
fi

# Prepare gdb/config.h first.
%make_build CFLAGS="$CFLAGS $FPROFILE_CFLAGS" LDFLAGS="$LDFLAGS $FPROFILE_CFLAGS" V=1 maybe-configure-gdb
perl -i.relocatable -pe 's/^(D\[".*_RELOCATABLE"\]=" )1(")$/${1}0$2/' gdb/config.status

%make_build CFLAGS="$CFLAGS $FPROFILE_CFLAGS" LDFLAGS="$LDFLAGS $FPROFILE_CFLAGS" V=1

! grep '_RELOCATABLE.*1' gdb/config.h

if [ "$fprofile" = "-fprofile" ]
then
  cd gdb
  cp -p gdb gdb-withindex
  PATH="$PWD:$PATH" sh ../../gdb/gdb-add-index $PWD/gdb-withindex
  ./gdb -nx -ex q ./gdb-withindex
  ./gdb -nx -readnow -ex q ./gdb-withindex
  cd ..
fi

cd ..

done  # fprofile

cd %{gdb_build}

%make_build \
     -C gdb/doc {gdb,annotate}{.info,/index.html,.pdf} MAKEHTMLFLAGS=--no-split MAKEINFOFLAGS=--no-split V=1

# Copy the <sourcetree>/gdb/NEWS file to the directory above it.
cp $RPM_BUILD_DIR/%{gdb_src}/gdb/NEWS $RPM_BUILD_DIR/%{gdb_src}

%check
# Initially we're in the GDB_SRC directory.
cd %{gdb_build}

# We always run the unittests.
(cd gdb; make run GDBFLAGS='-batch -ex "maintenance selftest"')

%if 0%{!?_with_testsuite:1}
echo ====================TESTSUITE DISABLED=========================
%else
echo ====================TESTING=========================
cd gdb
gcc -o ./orphanripper %{SOURCE2} -Wall -lutil -ggdb2
# Need to use a single --ignore option, second use overrides first.
# No `%{?_smp_mflags}' here as it may race.
# WARNING: can't generate a core file - core tests suppressed - check ulimit
# "readline-overflow.exp" - Testcase is broken, functionality is OK.
(
  # ULIMIT required for `gdb.base/auxv.exp'.
  ulimit -H -c
  ulimit -c unlimited || :

  # Setup $CHECK as `check//unix/' or `check//unix/-m64' for explicit bitsize.
  # Never use two different bitsizes as it fails on ppc64.
  echo 'int main (void) { return 0; }' >biarch.c
  CHECK=""
  for BI in -m64 -m32 -m31 ""
  do
    # Do not use size-less options if any of the sizes works.
    # On ia64 there is no -m64 flag while we must not leave a bare `check' here
    # as it would switch over some testing scripts to the backward compatibility
    # mode: when `make check' was executed from inside the testsuite/ directory.
    if [ -z "$BI" -a -n "$CHECK" ];then
      continue
    fi
    # Do not use $RPM_OPT_FLAGS as the other non-size options will not be used
    # in the real run of the testsuite.
    if ! gcc $BI -o biarch biarch.c
    then
      continue
    fi
    CHECK="$CHECK check//unix/$BI check//native-gdbserver/$BI check//native-extended-gdbserver/$BI"
  done
  # Do not try -m64 inferiors for -m32 GDB as it cannot handle inferiors larger
  # than itself.
  # s390 -m31 still uses the standard ELF32 binary format.
  gcc $RPM_OPT_FLAGS -o biarch biarch.c
  RPM_SIZE="$(file ./biarch|sed -n 's/^.*: ELF \(32\|64\)-bit .*$/\1/p')"
  if [ "$RPM_SIZE" != "64" ]
  then
    CHECK="$(echo " $CHECK "|sed 's#check//unix/-m64 check//native-gdbserver/-m64 check//native-extended-gdbserver/-m64# #')"
  fi

  # Disable some problematic testcases.
  # RUNTESTFLAGS='--ignore ...' is not used below as it gets separated by the
  # `check//...' target spawn and too much escaping there would be dense.
  for test in                           \
    gdb.base/readline-overflow.exp      \
    gdb.base/bigcore.exp                \
%if 0%{?rhel} < 7 
    gdb.base/gnu-debugdata.exp          \
    gdb.base/access-mem-running.exp     \
    gdb.threads/access-mem-running-thread-exit.exp \
%endif
  ; do
    mv -f ../../gdb/testsuite/$test ../gdb/testsuite/$test-DISABLED || :
  done

  # Run all the scheduled testsuite runs also in the PIE mode.
  # See also: gdb-runtest-pie-override.exp
  ###CHECK="$(echo $CHECK|sed 's#check//unix/[^ ]*#& &/-fPIC/-pie#g')"

TESTS=""
%if 0%{?tests:1}
  for test in %{tests}; do
    TESTS="${TESTS:+$TESTS }$test"
  done
%endif
  ./orphanripper make %{?_smp_mflags} -k $CHECK TESTS="$TESTS" || :
)
for t in sum log
do
  for file in testsuite*/gdb.$t
  do
    suffix="${file#testsuite}"
    suffix="${suffix%/gdb.$t}"
    ln $file gdb-%{_target_platform}$suffix.$t || :
  done
done
# `tar | bzip2 | uuencode' may have some piping problems in Brew.
tar cjf gdb-%{_target_platform}.tar.bz2 gdb-%{_target_platform}*.{sum,log}
uuencode gdb-%{_target_platform}.tar.bz2 gdb-%{_target_platform}.tar.bz2
cd ../..
echo ====================TESTING END=====================
%endif
# endif _testsuite

%install
# Initially we're in the GDB_SRC directory.
%if 0%{?_build_minimal}
cd %{gdb_build_minimal}
rm -rf $RPM_BUILD_ROOT

%make_install %{?_smp_mflags}

# Delete everything except the 'gdb' binary, and then rename it to
# 'gdb.minimal'.
rm -rfv $RPM_BUILD_ROOT%{_prefix}/{include,lib*,share}
rm -fv $RPM_BUILD_ROOT%{_bindir}/{gcore,gdbserver,gstack,gdb-add-index}
mv $RPM_BUILD_ROOT%{_bindir}/gdb $RPM_BUILD_ROOT%{_bindir}/gdb.minimal

cd ..
%endif
# endif _build_minimal

# Install the full build.

cd %{gdb_build}

# We must remove the $RPM_BUILD_ROOT directory ourselves if we're not
# building gdb-minimal.
%if 0%{!?_build_minimal}
rm -rf $RPM_BUILD_ROOT
%endif

%make_install %{?_smp_mflags}

%if 0%{!?scl:1}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/libexec
mv -f $RPM_BUILD_ROOT%{_bindir}/gdb $RPM_BUILD_ROOT%{_prefix}/libexec/gdb
ln -s -r $RPM_BUILD_ROOT%{_prefix}/libexec/gdb  $RPM_BUILD_ROOT%{_bindir}/gdb
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
touch -r %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit.d
sed 's#%%{_sysconfdir}#%{_sysconfdir}#g' <%{SOURCE4} >$RPM_BUILD_ROOT%{_sysconfdir}/gdbinit
touch -r %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/gdbinit

for i in `find $RPM_BUILD_ROOT%{_datadir}/gdb/python/gdb -name "*.py"`
do
  # Files could be also patched getting the current time.
  touch -r $RPM_BUILD_DIR/%{gdb_src}/gdb/version.in $i
done

%if 0%{?_enable_debug_packages:1} && 0%{!?_without_python:1}
mkdir -p $RPM_BUILD_ROOT/usr/lib/debug%{_bindir}
cp -p ./gdb/gdb-gdb.py $RPM_BUILD_ROOT/usr/lib/debug%{_bindir}/
for pyo in "" "-O";do
  # RHEL-5: AttributeError: 'module' object has no attribute 'compile_file'
  %{__python} $pyo -c 'import compileall, re, sys; sys.exit (not compileall.compile_dir("'"$RPM_BUILD_ROOT/usr/lib/debug%{_bindir}"'", 1, "'"/usr/lib/debug%{_bindir}"'"))'
done
%endif

# Compile python files
%if 0%{!?_without_python:1}
%py_byte_compile %{__python3} %{buildroot}%{_datadir}/gdb/python/gdb

# BZ 999645: /usr/share/gdb/auto-load/ needs filesystem symlinks
for i in $(echo bin lib $(basename %{_libdir}) sbin|tr ' ' '\n'|sort -u);do
  # mkdir to satisfy dangling symlinks build check.
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/gdb/auto-load/%{_root_prefix}/$i
  ln -s $(echo %{_root_prefix}|sed 's#^/*##')/$i \
        $RPM_BUILD_ROOT%{_datadir}/gdb/auto-load/$i
done
for i in `find $RPM_BUILD_ROOT%{_datadir}/gdb -name "*.py"`; do
  # Files are installed by install(1) not preserving the timestamps.
  touch -r $RPM_BUILD_DIR/%{gdb_src}/gdb/version.in $i
done
%endif

# Create the folder where GDB expects to find custom JIT readers.
mkdir -p %{buildroot}%{_libdir}/gdb

# Remove the files that are part of a gdb build but that are owned and
# provided by other packages.
# These are part of binutils

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/
rm -f $RPM_BUILD_ROOT%{_infodir}/bfd*
rm -f $RPM_BUILD_ROOT%{_infodir}/standard*
rm -f $RPM_BUILD_ROOT%{_infodir}/configure*
rm -f $RPM_BUILD_ROOT%{_infodir}/sframe-spec*
# Just exclude the header files in the top directory, and don't exclude
# the gdb/ directory, as it contains jit-reader.h.
rm -rf $RPM_BUILD_ROOT%{_includedir}/*.h
rm -rf $RPM_BUILD_ROOT/%{_libdir}/lib{bfd*,opcodes*,iberty*,ctf*,sframe*}

# pstack obsoletion

ln -s gstack.1 $RPM_BUILD_ROOT%{_mandir}/man1/pstack.1
ln -s gstack $RPM_BUILD_ROOT%{_bindir}/pstack

# Packaged GDB is not a cross-target one.
(cd $RPM_BUILD_ROOT%{_datadir}/gdb/syscalls
 rm -f mips*.xml
 rm -f sparc*.xml
%ifnarch x86_64
 rm -f amd64-linux.xml
%endif
%ifnarch %{ix86} x86_64
 rm -f i386-linux.xml
%endif
)

# Documentation only for development.
rm -f $RPM_BUILD_ROOT%{_infodir}/gdbint*
rm -f $RPM_BUILD_ROOT%{_infodir}/stabs*
rm -f $RPM_BUILD_ROOT%{_infodir}/ctf-spec*

# Delete this too because the dir file will be updated at rpm install time.
# We don't want a gdb specific one overwriting the system wide one.

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# These files are unrelated to Fedora Linux.
rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit/elinos.py
rm -f $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit/wrs-linux.py
rmdir $RPM_BUILD_ROOT%{_datadir}/gdb/system-gdbinit

%files
# File must begin with "/": {GFDL,COPYING3,COPYING,COPYING.LIB,COPYING3.LIB}
%license COPYING3 COPYING COPYING.LIB COPYING3.LIB
%doc README NEWS
%{_bindir}/gdb
%{_bindir}/gcore
%{_mandir}/*/gcore.1*
%{_bindir}/gstack
%{_mandir}/*/gstack.1*
%{_bindir}/pstack
%{_mandir}/*/pstack.1*
# Provide gdb/jit-reader.h so that users are able to write their own GDB JIT
# plugins.
%{_includedir}/gdb
# Export the folder where JIT readers should be placed.
%dir %{_libdir}/gdb
%if 0%{!?scl:1}
%files headless
%{_prefix}/libexec/gdb
%endif
%config(noreplace) %{_sysconfdir}/gdbinit
%{_mandir}/*/gdb.1*
%{_sysconfdir}/gdbinit.d
%{_mandir}/*/gdbinit.5*
%{_bindir}/gdb-add-index
%{_mandir}/*/gdb-add-index.1*
%{_datadir}/gdb

# don't include the files in include, they are part of binutils

%if 0%{?_build_minimal}
%files minimal
%{_bindir}/gdb.minimal
%{_bindir}/gdb-add-index
%endif

%files gdbserver
%{_bindir}/gdbserver
%{_mandir}/*/gdbserver.1*
%if %{have_inproctrace}
%{_libdir}/libinproctrace.so
%endif

%if 0%{!?_without_python:1}
# [rhel] Do not migrate /usr/share/gdb/auto-load/ with symlinks on RHELs.
%if 0%{!?rhel:1}
%pre
for i in $(echo bin lib $(basename %{_libdir}) sbin|tr ' ' '\n'|sort -u);do
  src="%{_datadir}/gdb/auto-load/$i"
  dst="%{_datadir}/gdb/auto-load/%{_root_prefix}/$i"
  if test -d $src -a ! -L $src;then
    if ! rmdir 2>/dev/null $src;then
      mv -n $src/* $dst/
      rmdir $src
    fi
  fi
done
%endif
%endif

%files doc
%doc %{gdb_build}/gdb/doc/{gdb,annotate}.{html,pdf}
%{_infodir}/annotate.info*
%{_infodir}/gdb.info*

%if 0%{?scl:1}
# As of F-28, packages won't need to call /sbin/install-info by hand
# anymore.  We make an exception for DTS here.
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/MP2QVJZBOJZEOQO2G7UB2HLXKXYPF2G5/

%post doc
# This step is part of the installation of the RPM. Not to be confused
# with the 'make install ' of the build (rpmbuild) process.

# For --excludedocs:
if [ -e %{_infodir}/gdb.info.gz ]
then
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/annotate.info.gz || :
  /sbin/install-info --info-dir=%{_infodir} %{_infodir}/gdb.info.gz || :
fi

%preun doc
if [ $1 = 0 ]
then
  # For --excludedocs:
  if [ -e %{_infodir}/gdb.info.gz ]
  then
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/annotate.info.gz || :
    /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/gdb.info.gz || :
  fi
fi
%endif
# endif scl

%changelog
* Wed Feb 11 2026 Guinevere Larsen <guinevere@redhat.com>
- Backport upstream commit f08ffbbf269 to fix RHBZ 2435950
  This reverts a new feature that was never properly approved
  for merging in upstream GDB.

* Wed Feb 4 2026 Andrew Burgess <aburgess@redhat.com>
- Backport upstream commit 70b66cf338b14336 to fix RH BZ 2402580.
  This backport will not be needed once we rebase to GDB 18.

* Wed Jan 14 2026 Kevin Buettner <kevinb@redhat.com> - 17.1-1
- Rebase to FSF GDB 17.1.
  Deleted: gdb-fix-bg-execution-repeat.patch
- Backport upstream commit ce106639c20 from Tom de Vries, fixing a
  a gdb.threads/thread-specific-bp.exp failure.
- Made spec file change to build gdb with --disable-gdb-compile due to
  this feature's brokenness.  With it disabled, failing tests skip
  cleanly without timeouts.  Also reduces binary size and attack
  surface.

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com>
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com>
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Andrew Burgess <aburgess@redhat.com>
- Rename 'gdb-add-rpm-suggestion-script.patch' to
  'gdb-rpm-suggestion-script.patch' and
  'gdb-6.3-rh-testversion-20041202.patch' to
  'gdb-test-show-version.patch'.  The new names better reflect the
  patch contents.

* Tue Jun 03 2025 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-archer-next-over-throw-cxx-exec.patch, we now have
  upstream commit d462550c91c.

* Tue Jun 03 2025 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-6.3-mapping-zero-inode-test.patch, we now have upstream
  commit fcfd8a4f239.

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com>
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 16.3-2
- Bootstrap for Python 3.14

* Wed May 28 2025 Andrew Burgess <aburgess@redhat.com>
- Remove 32-bit ARM support for RHEL 10+.  This is not a RHEL
  supported target, so lets drop this target.  Retain for older RHEL
  versions, as well as Fedora.

* Mon May 12 2025 Keith Seitz <keiths@redhat.com>
- Remove gdb-rhbz1149205-catch-syscall-after-fork-test.patch
  in favor of upstream commit.

* Wed May 07 2025 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-6.8-bz466901-backtrace-full-prelinked.patch.  Prelinking
  is no longer supported, there seems little point keeping this test.

* Fri Apr 25 2025 Alexandra Hájková <ahajkova@redhat.com>
- Backport "Fix another timeout in gdb.base/bg-execution-repeat.exp"
  (Tom de Vries)

* Wed Apr 23 2025 Alexandra Hájková <ahajkova@redhat.com> - 16.3-1
- Rebase to FSF GDB 16.3.
  Deleted: core-target-open-segfault.patch
           gdb-rhbz2354997-gstack-drop-readnever.patch
           tui-wrefresh-issue.patch

* Wed Apr 02 2025 Alexandra Hájková <ahajkova@redhat.com>
- Remove upstreamed gdb-rhbz-818343-set-solib-absolute-prefix-testcase.patch.

* Fri Mar 28 2025 Keith Seitz <keiths@redhat.com> - 16.2-3
- Backport "Fix gstack issues" from upstream.
  (Keith Seitz, RH BZ 2354997)

* Thu Mar 06 2025 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-rhbz1084404-ppc64-s390x-wrong-prologue-skip-O2-g-3of3.patch.
  The upstream test 'gdb.arch/amd64-prologue-skip.exp' should be
  sufficient for testing an upstream fix which was pushed in 2015.

* Wed Mar 05 2025 Guinevere Larsen <guinevere@redhat.com>
- Remove gdb-6.5-gcore-buffer-limit-test.patch. A similar test has been
  added upstream, which will trickle down soon.

* Thu Feb 27 2025 Keith Seitz <keiths@redhat.com>
- Remove gdb-6.6-bz237572-ppc-atomic-sequence-test.patch. This is covered
  by gdb.arch/ppc64-isa207-atomic-inst.exp.

* Mon Feb 10 2025 Andrew Burgess <aburgess@redhat.com>
- Add core-target-open-segfault.patch and tui-wrefresh-issue.patch,
  these backport upstream commits 2fc56106422 and 2b646bb8767
  respectively, both fix regressiosn in GDB 16 vs GDB 15.

* Fri Feb 07 2025 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-6.5-bz218379-ppc-solib-trampoline-test.patch.  There must
  be upstream tests that 'next' over a libc call.  Additionally, it is
  not clear to me exactly what bug is being tested for here.

* Fri Feb 07 2025 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-gstack.man file.  This is no longer used.  There is an
  upstream version of gstack which provides its own man page.

* Tue Feb 04 2025 Alexandra Hájková <ahajkova@redhat.com> - 16.2-1
- Rebase to FSF GDB 16.2.
  Modified: gdb-add-rpm-suggestion-script.patch

* Thu Jan 23 2025 Alexandra Hájková <ahajkova@redhat.com> - 16.1-1
- Rebase to FSF GDB 16.1.
  Dropped:
  gdb-backport-buildid-related-changes.patch
  gdb-catchpoint-re-set.patch
  gdb-remove-qnx-neutrino-support.patch

* Thu Jan 23 2025 Alexandra Hájková <ahajkova@redhat.com>
- Remove upstreamed gdb-6.3-gstack-20050411.patch.

* Fri Jan 17 2025 Guinevere Larsen <guinevere@redhat.com>
- remove gdb-test-bt-cfi-without-die.patch.  This test has been
  accepted upstream and will make its way back to testing with
  the GDB 17 release.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-rhbz1261564-aarch64-hw-watchpoint-test.patch.  This test
  should be covered by gdb.base/watchpoint-unaligned.exp which was
  added upstream in commit a3b60e4588606354b93508a0008a5.

* Thu Jan 02 2025 Guinevere Larsen <glarsen@redhat.com>
- Remove gdb-rhbz1156192-recursive-dlopen-test.patch.

* Thu Jan 02 2025 Andrew Burgess <aburgess@redhat.com>
- Update generate-patches-from-git-repo.sh script, and regenerate
  patches.  This changed gdb-add-rpm-suggestion-script.patch,
  gdb-backport-buildid-related-changes.patch, and
  gdb-remove-qnx-neutrino-support.patch.  In each case, there is no
  significant change, only the diff header itself changed.

* Wed Dec 11 2024 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-6.6-buildid-locate-tests.patch patch, merge the tests
  from this patch into gdb-add-rpm-suggestion-script.patch.  The tests
  from the removed patch all relate to RPM suggestion, and so should
  live with the rpm suggestion script.

* Wed Dec 11 2024 Andrew Burgess <aburgess@redhat.com>
- This REMOVES the 'set/show build-id-verbose' command.  Users should
  instead use 'set/show rpm-suggestion enabled'.  The old
  build-id-verbose setting took an integer, but only 0 or 1 had
  meaning.  The new setting is a boolean, and takes 'on' or 'off'.
  The old setting was undocumented, while the new setting has a manual
  entry.

* Wed Dec 11 2024 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-add-deprecated-settings-py-script.patch.  This REMOVES
  the 'set/show build-id-core-load' setting from GDB.  This setting
  has had no effect on GDB since commit a5d2c85367e544d446 back in
  2020.  Lets finally drop this setting.

* Tue Dec 10 2024 Andrew Burgess <aburgess@redhat.com>
- Remove
  gdb-6.6-buildid-locate-misleading-warning-missing-debuginfo-rhbz981154.patch,
  gdb-6.6-buildid-locate.patch,
  gdb-6.6-buildid-locate-solib-missing-ids.patch, and
  gdb-remove-use-of-py-isascii.  Add new patches
  gdb-add-deprecated-settings-py-script.patch,
  gdb-backport-buildid-related-changes.patch,
  gdb-remove-qnx-neutrino-support.patch, and
  gdb-6.6-buildid-locate-tests.patch.  Update
  gdb-add-rpm-suggestion-script.patch and
  gdb-rhbz1156192-recursive-dlopen-test.patch.  All of the RPM
  suggestion feature is now provided via a Python extension.  I
  believe that the existing functionality should be covered by the new
  implementation, but with no real tests for the existing code, we
  cannot be certain.  There are new GDB commands added as part of this
  change related to controlling the RPM suggestion feature.  These are
  documented within the gdb-add-rpm-suggestion-script.patch patch by
  changes to the GDB manual.

* Thu Nov 14 2024 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-6.5-bz243845-stale-testing-zombie-test.patch.  This was a
  test for a fix to a function that was named linux_test_for_tracefork,
  which was removed in 2022 in upstream commit a288518611d.

* Wed Nov 13 2024 Alexandra Hájková <ahajkova@redhat.com>
- Remove upstreamed (21dc8b8d287) gdb-test-dw2-aranges.patch.

* Wed Nov 13 2024 Andrew Burgess <aburgess@redhat.com>
- Add x86_64-redhat-linux-gnu to --enable-targets for full GDB build
  in gdb.spec, this ensures we can remote debug x86-64 targets from
  non-x86-64 hosts.  This fixes rhbz 2308522.

* Tue Nov 12 2024 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-6.6-testsuite-timeouts.patch.  I updated the upstream
  tests in commit 06b8b0ad976 so this patch is no longer useful.

* Wed Nov  6 2024 Mark Wielaard <mjw@fedoraproject.org> - 15.2-2
- Resolves: rhbz#2323513
  - gdb-add-index.patch: Replace which with command -v
  - Remove which Requires which was only there for gdb-add-index

* Tue Nov  5 2024 Guinevere Larsen <guinevere@redhat.com>
- Remove gdb-simultaneous-step-resume-breakpoint.patch
  This test is covered by a combination of upstream tests already.

* Thu Oct 24 2024 Guinevere Larsen <guinevere@redhat.com>
- Make the GDB package provide the libdir/gdb folder, so that packages
  that provide a JIT reader don't need to create it on their own.

* Fri Oct 4 2024 Alexandra Hájková <ahajkova@redhat.com> - 15.2-2
- Rebase to FSF GDB 15.2.

* Thu Sep 26 2024 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-rhbz1007614-memleak-infpy_read_memory-test.patch.  An
  equivalent test was pushed upstream in commit f4b29c2f610.

* Wed Sep 11 2024 Kevin Buettner <kevinb@redhat.com>
- Remove local patch gdb-6.5-section-num-fixup-test.patch.  This
  patch contained a test case which should be covered by upstream
  test gdb.base/ctxobj.exp.

* Mon Sep  9 2024 Andrew Burgess <aburgess@redhat.com>
- Backport upstream commit a92e943014f to fix rhbz2304296.

* Wed Aug 21 2024 Alexandra Hájková <ahajkova@redhat.com> - 15.1-22
- Add x86_64-redhat-linux-gnu to --enable-targets= in gdb.spec.
  This enables to connect to gdbserver running on x86 using the x86 binary
  running GDB from a different architecture. (RHBZ 2308522)

* Wed Aug 21 2024 Alexandra Hájková <ahajkova@redhat.com>
- Remove gdb-6.6-bz229517-gcore-without-terminal.patch
    This test was upstreamed.

* Thu Aug  8 2024 Guinevere Larsen <blarsen@redhat.com>
- Remove gdb-6.7-ppc-clobbered-registers-O2-test.patch
    This test is already upstreamed in gdb.opt
- Remove gdb-rhbz947564-findvar-assertion-frame-failed-testcase.patch
    This is already covered by gdb.thread/tls.exp

* Wed Jul 24 2024 Alexandra Hájková <ahajkova@redhat.com> - 15.1-1
- Rebase to FSF GDB 15.1.
- Update local patches:
    gdb-6.3-gstack-20050411.patch
    gdb-6.6-buildid-locate-solib-missing-ids.patch
    gdb-6.6-buildid-locate.patch
    gdb-add-missing-debug-ext-lang-hook.patch
    gdb-add-rpm-suggestion-script.patch
    gdb-merge-debug-symbol-lookup.patch
- Dropped:
    gdb-add-missing-debug-ext-lang-hook.patch
    gdb-add-missing-debug-info-python-hook.patch
    gdb-do-not-import-py-curses-ascii-module.patch
    gdb-ftbs-swapped-calloc-args.patch
    gdb-handle-no-python-gdb-module.patch
    gdb-refactor-find-and-add-separate-symbol-file.patch
    gdb-reformat-missing-debug-py-file.patch
    gdb-remove-path-in-test-name.patch
    gdb-remove-use-of-py-isascii
    gdb-rhbz-2232086-cpp-ify-mapped-symtab.patch
    gdb-rhbz-2232086-generate-dwarf-5-index-consistently.patch
    gdb-rhbz-2232086-generate-gdb-index-consistently.patch
    gdb-rhbz-2232086-reduce-size-of-gdb-index.patch
    gdb-rhbz2232086-refactor-selftest-support.patch
    gdb-rhbz2250652-avoid-PyOS_ReadlineTState.patch
    gdb-rhbz2250652-gdbpy_gil.patch
    gdb-rhbz2261580-intrusive_list-assertion-fix.patch
    gdb-rhbz2277160-apx-disasm.patch
    gdb-rhel2295897-pre-read-DWZ-file-in-DWARF-reader.patch
    gdb-sync-coffread-with-elfread.patch

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul  5 2024 Guinevere Larsen <blarsen@redhat.com> - 14.2-14
- backport commit 91874afabcd to solve RHEL-2295897
  This fixes a double free when debugging mysql-workbench

* Thu Jun 27 2024 Kevin Buettner <kevinb@redhat.com> - 14.2-13
- Revise rpm-suggestions.py script so that message regarding
  a not-found 'rpm' module is deferred until just prior to
  printing the GDB prompt.  (RHBZ 2275274)

* Wed Jun 19 2024 Guinevere Larsen <blarsen@redhat.com>
- Drop gdb-glibc-strstr-workaround.patch

* Tue Jun 18 2024 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-core-open-vdso-warning.patch.  This tests added by this
  patch are similar to those of upstream test gdb.base/vdso-warning.exp.

* Tue Jun 18 2024 Kevin Buettner <kevinb@redhat.com> - 14.2-12
- Revise rpm-suggestions.py script so that message regarding
  a not-found 'rpm' module is output to stderr.  (RHBZ 2275274)

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com>
- Rebuilt for Python 3.13

* Thu Jun 06 2024 Python Maint <python-maint@redhat.com> - 14.2-10
- Bootstrap for Python 3.13

* Thu May 23 2024 Kevin Buettner <kevinb@redhat.com> - 14.2-9
- Revise rpm-suggestions.py script so that a message is printed when
  the 'rpm' module (found in the python3-rpm package) isn't found.
  In particular, the ModuleNotFoundError will be caught, avoiding
  a potential python import error.  (RHBZ 2275274)

* Wed May 22 2024 Guinevere Larsen <blarsen@redhat.com>
- Remove gdb-fedora-libncursesw.patch, this workaround isn't needed
  anymore.

* Wed May 15 2024 Keith Seitz <keiths@redhat.com> - 14.2-8
- Sync x86 disassembler with (proposed) gdb-15.1 release.
  (many authors, RHBZ 2277160)

* Tue Apr 30 2024 Keith Seitz <keiths@redhat.com> - 14.2-7
- Remove bundled copy of libipt.
- Remove bundled copy of libstdc++ pretty-printers.
- Always include debuginfod support.
- Purge RHEL < 8.

* Thu Apr 25 2024 Kevin Buettner <kevinb@redhat.com> - 14.2-6
- Further changes for fixing RHBZ 2275274:  Add a
  'Requires: binutils' which is needed because gdb-add-index uses
  readelf and objcopy.  Also, delete librpm related stuff since
  gdb/build-id.c no longer attempts to dlopen a librpm library.  Add
  'Recommends python3-rpm' so that rpm-suggestions.py will find the
  required python module.

* Tue Apr 23 2024 Kevin Buettner <kevinb@redhat.com> - 14.2-5
- Add "Requires: which" for RHBZ 2275274.

* Mon Apr 22 2024 Keith Seitz <keiths@redhat.com>
- Remove gdb-linux_perf-bundle.patch.

* Thu Mar 28 2024 Kevin Buettner <kevinb@redhat.com>
- Drop gdb-6.5-bz185337-resolve-tls-without-debuginfo-v2.patch.  I've
  rewritten and expanded the test case and have submitted it for
  upstream consideration.  The hack which rewrote 'errno' into a
  dereference of a call to '__errno_location' does still fix a problem
  with printing errno in statically linked binaries.  But it will fail
  when attempting to debug a core file.  The original test case
  associated with this bug now works correctly due changes to glibc.

* Tue Mar 19 2024 Andrew Burgess <aburgess@redhat.com>
- Drop gdb-bz634108-solib_address.patch.  This is a test only patch.
  I've pushed upstream commit 52ca06e807b which covers this test case,
  we'll pick up the upstream test next time Fedora is rebased.

* Tue Mar 19 2024 Andrew Burgess <aburgess@redhat.com>
- Drop gdb-container-rh-pkg.patch.  This patch gave a warning when
  connecting to very old gdbserver.  The warning mentioned specific
  RHEL versions, all of which are no longer supported.  As such the
  warning seems pointless.

* Mon Mar 18 2024 Andrew Burgess <aburgess@redhat.com>
- Drop gdb-6.3-attach-see-vdso-test.patch, this is a test only patch.
  Upstream commit 93eb6c64ec4a6ea includes a similar test, and will be
  picked up as part of the next rebase.

* Wed Mar 13 2024 Andrew Burgess <aburgess@redhat.com>
- Remove the use of librpm from GDB's C++ code, and instead provide
  similar RPM suggestion feature using a Python extension.  The Python
  extension feature that supports this is an upstream feature which
  has been back-ported (along with several dependencies and related
  fixes).  The actual RPM suggestion is now provided as a Python
  script which is auto-loaded by GDB.  Removing the use of librpm from
  the C++ code allows some cleanup of the configure scripts.

* Fri Mar  8 2024 Andrew Burgess <aburgess@redhat.com>
- Reduce gdb-6.6-buildid-locate.patch by removing some unnecessary
  casts added to bfd/ source files.

* Fri Mar  8 2024 Andrew Burgess <aburgess@redhat.com>
- Reduce gdb-6.6-buildid-locate.patch by removing the build_id_bfd_get
  to build_id_bfd_shdr_get change.  This was only changing the name of
  a function, so seems pointless.

* Wed Mar 6 2024 Alexandra Hájková <ahajkova@redhat.com> - 14.2-1
- Rebase to FSF GDB 14.2.

* Mon Mar 4 2024 Alexandra Hájková <ahajkova@redhat.com> - 14.1-10
- Replace zlib to zlib-ng package in a debug-toolset-binary Fedora CI
  test (RHBZ 2266910).

* Wed Feb 21 2024 Richard W.M. Jones <rjones@redhat.com>
- Bump and rebuild for riscv64

* Mon Jan 29 2024 Kevin Buettner <kevinb@redhat.com> - 14.1-8
- Backport upstream workaround for GCC 14 problem which is causing
  GDB internal errors (RHBZ 261580, Tom de Vries).

* Thu Jan 25 2024 Guinevere Larsen <blarsen@redhat.com>
- Remove gdb-6.5-BEA-testsuite.patch, as it was upstreamed and
  will make its way back with the next rebase.

* Thu Jan 25 2024 Guinevere Larsen <blarsen@redhat.com> - 14.1-7
- Backport "gdb: fix list . related crash"

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Kevin Buettner <kevinb@redhat.com> - 14.1-4
- Backport upstream commit bc23ea51f8a83e9524dfb553baa8baacb29e68a9,
  potentially fixing RHBZ 2257562.

* Thu Jan 11 2024 Alexandra Hájková <ahajkova@redhat.com> - 14.1-3
- Fix typo in gdb.spec.

* Mon Jan 8 2024 Alexandra Hájková <ahajkova@redhat.com> - 14.1-2
- Backport upstream commits 7ae9ecfd801 and 8170efad364 to avoid
  using _PyOS_ReadlineTState  (RHBZ 2250652).

* Fri Dec 8 2023 Kevin Buettner <kevinb@redhat.com> - 14.1-1
- Rebase to FSF GDB 14.1.
- Update local patches:
    gdb-6.5-bz185337-resolve-tls-without-debuginfo-v2.patch
    gdb-6.6-buildid-locate-rpm.patch
    gdb-6.6-buildid-locate.patch
    gdb-container-rh-pkg.patch
    gdb-core-open-vdso-warning.patch
    gdb-fedora-libncursesw.patch
    gdb-linux_perf-bundle.patch
- Update backported patches which didn't make it into 14.1:
    gdb-rhbz-2232086-cpp-ify-mapped-symtab.patch
    gdb-rhbz-2232086-generate-gdb-index-consistently.patch
- Drop upstreamed local patches:
    gdb-6.5-sharedlibrary-path.patch
- Drop gdb-13.2 backports (which are now in gdb-14.1):
    gdb-binutils29988-read_indexed_address.patch
    gdb-bz2196395-debuginfod-legacy-openssl-crash.patch
    gdb-bz2237392-dwarf-obstack-allocation.patch
    gdb-bz2237515-debuginfod-double-free.patch
    gdb-rhbz2192105-ftbs-dangling-pointer
    gdb-rhbz2233961-CVE-2022-4806.patch
    gdb-rhbz2233965-memory-leak.patch
- Adjust gdb.spec so that --with-mpfr is no longer passed to
  configure; doing so, combined with some configury changes triggered
  a latent build problem.

* Mon Dec 4 2023 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-6.5-missed-trap-on-step-test.patch.  Testing what happens
  when stepping over/through a statement which triggers a watchpoint
  is being added, upstream, to gdb.base/watchpoint.exp.

* Tue Nov 28 2023 Andrew Burgess <aburgess@redhat.com>
- Backport upstream commits 1f0fab7ff86, aa19bc1d259, acc117b57f7,
  aff250145af, and 3644f41dc80.  These commits reduce the size of the
  generated gdb-index file, and also ensure that the gdb-index and
  dwarf-5 index are generated consistently even as the number of
  worker threads that GDB uses changes (RHBZ 2232086).

* Thu Oct 19 2023 Alexandra Hájková <ahajkova@redhat.com>
- Remove gdb-6.5-ia64-libunwind-leak-test.patch.
  The patch doesn't include any actual fixes, the architecture
  is end of life and the kernel is planning to drop IA64 support.

* Wed Oct 11 2023 Guinevere Larsen <blarsen@redhat.com>
- Remove gdb-rhbz1186476-internal-error-unqualified-name-re-set-test.patch
  as it was upstreamed back in 2010 with a different test name.

* Mon Oct 2 2023 Kevin Buettner <kevinb@redhat.com> - 13.2-11
- Backport upstream commit which prevents internal error when
  generating an overly large gdb-index file.  (RHBZ 1773651, Kevin
  Buettner.)

* Sun Oct 1 2023 Alexandra Hájková <ahajkova@redhat.com> - 13.2-10
- Backport upstream commit d28fbc7197b which fixes RHBZ 2233965 (
  CVE-2022-48065).

* Thu Sep 28 2023 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-6.5-sharedlibrary-path.patch, which was upstreamed in
  commit 3ec033fab4a.

* Tue Sep 19 2023 Keith Seitz <keiths@redhat.com>
- Remove gdb-rhbz1553104-s390x-arch12-test.patch, which is more thoroughly tested
  by binutils.

* Mon Sep 18 2023 Alexandra Hájková <ahajkova@redhat.com> - 13.2-8
- Bump release to 13.2-9.

* Sun Sep 17 2023 Alexandra Hájková <ahajkova@redhat.com> - 13.2-8
- Backport upstream commit 8f2c64de86b which fixes RHBZ 2233961,
  CVE-2022-48064, (Alan Modra).

* Fri Sep 15 2023 Keith Seitz <keiths@redhat.com> - 13.2-8
- migrated to SPDX license

* Fri Sep 15 2023 Andrew Burgess <aburgess@redhat.com>
- Bump release to 13.2-8.

* Thu Sep 14 2023 Andrew Burgess <aburgess@redhat.com>
- Backport upstream commit 54392c4df604f20, which fixes RHBZ 2237392.

* Wed Sep 13 2023 Andrew Burgess <aburgess@redhat.com>
- Backport upstream commit f96328accde1e63, which fixes RHBZ 2237515.

* Wed Aug  9 2023 Guinevere Larsen <blarsen@redhat.com>
- Remove gdb-6.7-testsuite-stable-results.patch, it only made the test
  fail more.

* Mon Aug  7 2023 Kevin Buettner <kevinb@redhat.com> - 13.2-7
- Bump release.

* Thu Aug  3 2023 Andrew Burgess <aburgess@redhat.com>
- Backport upstream commit f3eee586174, which fixes RHBZ 2196395.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Python Maint <python-maint@redhat.com>
- Rebuilt for Python 3.12

* Tue Jul  4 2023 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-test-pid0-core.patch.  This work has been upstreamed in
  commit 8bcead69665.

* Sat Jul  1 2023 Mark Wielaard <mjw@fedoraproject.org> - 13.2-4
- Adjust gdb-add-index.patch to be silent about which gdb.

* Fri Jun 30 2023 Kevin Buettner <kevinb@redhat.com> - 13.2-3
- Backport upstream changes which prevent repeated warnings from being
  printed when loading a core file  (RHBZ 2160211, Lancelot SIX).

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 13.2-2
- Rebuilt for Python 3.12

* Sun Jun 25 2023 Alexandra Hájková <ahajkova@redhat.com> - 13.2-1
- Rebase to FSF GDB 13.22.
- Remove gdb-rhbz2177655-aarch64-pauth-valid-regcache.patch.
- Remove gdb-rhbz2183595-rustc-inside_main.patch.

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com>
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com>
- Bootstrap for Python 3.12

* Sat May 20 2023 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-lineno-makeup-test.patch.  An equivalent test has now
  been merged to upstream binutils-gdb in commit ef56b006501.

* Tue May 16 2023 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-ccache-workaround.patch.  This patch works around
  problems when using older versions of ccache, however, upstream GDB
  now disables ccache during testing, see upstream commit 49b4de64242d.

* Tue May 16 2023 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-ppc-power7-test.patch, this patch is already covered by
  upstream tests gdb.arch/powerpc-*.exp.

* Sat May 6 2023 Alexandra Hájková <ahajkova@redhat.com>
- Remove gdb-rhel5.9-testcase-xlf-var-inside-mod.patch, the patch adds
  gdb.fortran/xlf-variable.exp test, the test can only be run on
  PPC64 machines which are not supported anymore.

* Thu May 4 2023 Kevin Buettner <kevinb@redhat.com>
- Fix C89-isms in gdb-6.6-buildid-locate-rpm.patch.  (Florian Weimer,
  RHBZ 2143992)'.  This change merely restores changes introduced by
  Keith's Nov 30 2022 commit, but which were inadvertently lost during
  the GDB 13.1 backport.

* Thu May 4 2023 Andrew Burgess <aburgess@redhat.com>
- Rewrite the changes to gdb-add-index.sh.  If the user has set the
  GDB environment variable then use that value, otherwise find a
  suitable GDB executable by looking in various places.

* Wed May 3 2023 Kevin Buettner <kevinb@redhat.com> 13.1-5
- Backport "Pass const frame_info_ptr reference for
  skip_[language_]trampoline". (Mark Wielaard, RHBZ 2192105, build/30413)

* Tue May 2 2023 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-opcodes-clflushopt-test.patch.  This patch tests that GDB
  can disassemble the clflushopt instruction correctly.  Such
  disassembly is a feature of libopcode and is covered by the gas
  tests i386/x86-64-clflushopt.s and i386/clflushopt.s.  Lets remove
  this test from GDB and just rely on the gas tests instead.

* Sat Apr 29 2023 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-6.7-charsign-test.patch. This patch originally contained
  some changes to GDB which were rejected by upstream maintainers.  All
  that remained was a testcase which had a number of failures due to
  the rest of the work not being present in GDB.

* Tue Apr 25 2023 Bruno Larsen <blarsen@redhat.com>
- Remove gdb-6.5-bz109921-DW_AT_decl_file-test.patch. That patch was
  only a test for basic DWARF-2 support, ensuring that GDB found a
  variable in a .h file; tests such as gdb.linespec/linespec.exp already
  tests for it.

* Mon Apr 24 2023 Bruno Larsen <blarsen@redhat.com>
- Remove gdb-6.5-last-address-space-byte-test.patch. It was used to
  test for a regression in target_xfer_memory, a function that has
  been removed from upstream back in 2006.

* Thu Apr 13 2023 Alexandra Hájková <ahajkova@redhat.com>
- Remove gdb-6.3-bz140532-ppc-unwinding-test.patch, it adds
  powerpc-bcl-prologue.exp test which seems to be a subset of
  upstream powerpc-prologue.exp

* Tue Apr 11 2023 Keith Seitz
- Backport "Fix a potential illegal memory access in the BFD library..."
  (Nick Clifton, binutils/29988)

* Fri Mar 31 2023 Keith Seitz <keiths@redhat.com> - 13.1-4
- Backport "Fix crash in inside_main_func"
  (Tom Tromey, RHBZ 2183595)

* Thu Mar 30 2023 Alexandra Hájková <ahajkova@redhat.com> - 12.1-3
- Update gdb-6.6-buildid-locate.patch to fix RHBZ 2181221.

* Wed Mar 29 2023 Andrew Burgess <aburgess@redhat.com>
- Used --with-pkgversion to place the distribution name in the version
  string rather than placing the string directly into the version.in
  file.

* Fri Mar 24 2023 Kevin Buettner <kevinb@redhat.com> - 13.1-2
- Backport fix for RHBZ 2177655.  (Luis Machado)

* Mon Mar 20 2023 Bruno Larsen <blarsen@redhat.com>
- Remove gdb-rhbz1350436-type-printers-error.patch since it is upstreamed.

* Wed Mar 8 2023 Kevin Buettner <kevinb@redhat.com> - 13.1-1
- Rebase to FSF GDB 13.1.
- Update gdb-6.3-rh-testversion-20041202.patch.
- Update gdb-6.3-bz140532-ppc-unwinding-test.patch.
- Update gdb-6.6-buildid-locate.patch.
- Update gdb-6.6-buildid-locate-rpm.patch.
- Remove 'Recommends: ' line for gcc-gdb-plugin for BZ2149246.
- Define _lto_cflags to nil to avoid ODR violations.
- Add -Wno-stringop-overflow to --enable-gdb-build-warnings to work around
  gcc problem.

* Fri Jan 27 2023 Kevin Buettner <kevinb@redhat.com> - 12.1-16
- Tweak gdb-6.3-rh-testversion-20041202.patch so that $_gdb_major
  and $_gdb_minor will be obtained correctly.

* Thu Jan 26 2023 Bruno Larsen <blarsen@redhat.com>
- Remove gdb-rhbz1398387-tab-crash-test.patch as that test didn't
  work anymore.

* Tue Jan 24 2023 Keith Seitz <keiths@redhat.com> - 12.1-15
- NVR bump for failed build.

* Mon Jan 23 2023 Kevin Buettner <kevinb@redhat.com>
- More tweaks to gdb-6.6-buildid-locate-rpm.patch, in which rpmTag
  is replaced with rpmDbiTagVal.

* Mon Jan 23 2023 Keith Seitz <keiths@redhat.com> - 12.1-14
  From Sergey Mende:
- Backport upstream patch "gdb: call check_typedef at beginning of
  dwarf_expr_context::fetch_result". (Simon Marchi)


* Fri Jan 20 2023 Kevin Buettner <kevinb@redhat.com> - 12.1-13
- Backport fix for problems associated with GCC 13's self-move warning.
  (Jan-Benedict Glaw)
- Tweak gdb-6.6-buildid-locate-rpm.patch so that running GDB's configure
  script will not error out due to GCC 13's warnings.

* Thu Jan 19 2023 Alexandra Hájková <ahajkova@redhat.com> - 12.1-12
- Backport replace deprecated distutils.sysconfig in python-config.
  (Lancelot SIX)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Andrew Burgess <aburgess@redhat.com>
- Backport upstream commits 38665d717a3 and c3efaf0afd9 to fix RHBZ
  2152431.

* Fri Dec 16 2022 Keith Seitz <keiths@redhat.com>
- Remove gdb-6.6-buildid-locate-rpm-scl.patch and
  gdb-bz601887-dwarf4-rh-test.patch.

* Fri Dec 9 2022 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-fortran-frame-string.patch, a version of this test has
  now been upstreamed.

* Fri Dec 9 2022 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-bfd-aliasing.patch.

* Fri Dec 9 2022 Andrew Burgess <aburgess@redhat.com>
- Remove gdb-entryval-crash-1of3.patch, gdb-entryval-crash-2of3.patch,
  and gdb-entryval-crash-3of3.patch.

* Wed Dec 7 2022 Keith Seitz <keiths@redhat.com> - 12.1-10
- Disable Guile support for F38+, RHBZ 2151328.

* Mon Dec 5 2022 Keith Seitz <keiths@redhat.com>
- Remove gdb-physname-pr11734-test.patch,
  gdb-physname-pr12273-test.patch, gdb-runtest-pie-override.patch,
  gdb-test-expr-cumulative-archer.patch.

* Thu Dec 1 2022 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-6.3-threaded-watchpoints2-20050225.patch.  The test in this
  patch is a tweaked version of upstream test gdb.threads/watchthreads.exp
  from 2004.  It doesn't actually test anything new.

* Thu Dec 1  2022 Bruno Larsen <blarsen@redhat.com>
- Remove gdb-rhbz1325795-framefilters-test.patch.  This test doesn't
  pass in the curret state, and the code that introduced the original
  problem has been changed beyong recognition at this point.

* Wed Nov 30 2022 Keith Seitz <keiths@redhat.com>
- Backport "libiberty: Fix C89-isms in configure tests" and do likewise in
  gdb-6.6-buildid-locate-rpm.patch.
  (Florian Weimer, RHBZ 2143992)

* Wed Nov 23 2022 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-6.3-inheritancetest-20050726.patch.  Upstream testcase
  gdb.cp/impl-this.exp tests the printing of an instance variable from
  an inherited class in the "print c" test. 

* Fri Nov 18 2022 Kevin Buettner <kevinb@redhat.com>
- Remove gdb-6.3-test-movedir-20050125.patch.  Upstream test
  gdb.base/fullname.exp provides coverage for this case and more.

* Thu Nov  3 2022 Keith Seitz <keiths@redhat.com> - 12.1-9
- Add patch to fix ODR violations on powerpc and
  enable LTO builds. (Keith Seitz, sw build/23395)

* Tue Oct 18 2022 Bruno Larsen - 12.1-8
- Backport fix to gdb.base/break-main-file-remove-fail.exp
  (Tom de Vries)

* Tue Oct 18 2022 Bruno Larsen - 12.1-7
- Remove patch gdb-6.3-test-dtorfix.
  Was upstreamed, will be back in the next rebase.

* Thu Oct 13 2022 Alexandra Hájková - 12.1-7
- Bump the release number.

* Tue Oct 11 2022 Alexandra Hájková - 12.1-6
- Backport upstream patch "Add support for readline 8.2". (Andreas Schwab)

* Fri Oct 7 2022 Alexandra Hájková - 12.1-6
- Update gdb-6.6-buildid-locate.patch to fix RHBZ 2122947.

* Thu Jul 28 2022 Amit Shah <amitshah@fedoraproject.org> 
- Use the dist_name macro to identify the distribution

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com>
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 12.1-2
- Bootstrap for Python 3.11

* Thu May 12 2022 Kevin Buettner - 12.1-1
- Rebase to FSF GDB 12.1.
- Update gdb-6.6-buildid-locate.patch.
- Update gdb-6.6-buildid-locate-rpm.patch.
- Dropped backported patches from GDB 11.1 and 11.2.

* Wed Mar 30 2022 Kevin Buettner - 11.2-3
- Backport upstream patch which removes sizes from debuginfod download
  messages when the size is not available (RHBZ 2068280, Aaron Merey).

* Wed Feb 9 2022 Kevin Buettner - 11.2-2
- On ix86, add -Wno-format-overflow to --enable-gdb-build-warnings. 
  (This is a workaround for the bogus warning/error that we now see
  on i686 regarding a "may write a terminating nul past the end of
  the destination" message for the sprintf() call in
  global_symbol_searcher::search() in gdb/symtab.c.)

* Wed Feb 9 2022 Kevin Buettner - 11.2-1
- Rebase to FSF GDB 11.2.

* Mon Jan 31 2022 Kevin Buettner <kevinb@redhat.com> - 11.1-12
- Fix "sect_index_data not initialized" internal error. (RHBZ 2042664,
  Kevin Buettner).

* Mon Jan 31 2022 Keith Seitz <keiths@redhat.com> - 11.1-11
- Fix buld issues. (RHBZ 2042257, Keith Seitz, Andrew Burgess)
- Update libipt to 2.0.5.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Alexandra Hájková - 11.1-9
- Remove gdb-6.3-inferior-notification-20050721.patch
  which adds problematic attach-32 test.

* Tue Jan 11 2022 Alexandra Hájková - 11.1-8
- Backport upstream patch "[PR gdb/27026] CTRL-C is ignored
  when debug info is downloaded" (RHBZ 2024875, Aaron Merey).

* Tue Jan 11 2022 Alexandra Hájková - 11.1-8
- Backport upstream patch "rework "set debuginfod" commands"
  (RHBZ 2024875, Simon Marchi).

* Tue Jan 11 2022 Alexandra Hájková - 11.1-8
- Backport upstream patch "Fix unittest.exp failure due to 'set debuginfod' addition"
  (RHBZ 2024875, Tom Tromey).

* Mon Jan 10 2022 Alexandra Hájková - 11.1-8
- Add -Wno-unused-function to --enable-gdb-build-warnings to prevent the build failure:
  "../../gdb/c-exp.y:3455:1: error: 'void c_print_token(FILE*, int, YYSTYPE)'
  defined but not used [-Werror=unused-function]"

* Mon Jan 10 2022 Alexandra Hájková - 11.1-8
- Backport upstream patch "gdb: add set/show commands for managing debuginfod"
  (RHBZ 2024875, Aaron Merey).

* Mon Jan 10 2022 Alexandra Hájková - 11.1-8
- Backport upstream patch "gdb.texinfo: Expand documentation for debuginfod"
  (RHBZ 2024875, Aaron Merey).

* Mon Dec 6 2021 Kevin Buettner - 11.1-7
- Add -Wno-deprecated-declarations to --enable-gdb-build-warnings to work
  around the python 3.11 deprecation of Py_SetProgramName.

* Fri Nov 12 2021 Timm Bäder <tbaeder@redhat.com> - 11.1-6
- Use %%set_build_flags to populate all relevant build flags

* Wed Nov 10 2021 Kevin Buettner - 11.1-5
- Backport upstream fix and test case for a dprintf bug (RHBZ 2022177, Kevin
  Buettner).

* Tue Nov 9 2021 Bruno Larsen - 11.1-4
- Backport manpage update to be closer to -help (RHBZ 853071)

* Wed Nov 3 2021 Kevin Buettner - 11.1-3
- Make adjustments to gdb-6.6-buildid-locate.patch, provided by Tom de Vries.

* Mon Oct 11 2021 Kevin Buettner - 11.1-2
- Backport upstream patch which papers over Fortran lexical analyzer
  bug (RHBZ 2012976, Tom de Vries).

* Mon Oct 04 2021 Kevin Buettner - 11.1-1
- Rebase to FSF GDB 11.1.
- Adjust build-id related patches.
- Drop backported patches which are no longer relevant.
- Bump 'snapgnulib' date.

* Thu Sep 30 2021 Alexandra Hájková <ahajkova@redhat.com> - 10.2-9
- Backport test for RHBZ 1976887 (Kevin Buettner).

* Thu Sep 30 2021 Alexandra Hájková <ahajkova@redhat.com> - 10.2-9
- Backport upstream patch which fixes internal-error: Unexpected
  type field location kind (RHBZ 1976887, Alexandra Hájková).

* Wed Sep 22 2021 Bruno Larsen <blarsen@redhat.com> - 10.2-8
- Backport "[gdb] Improve early exits for env var in debuginfod-support.c"
  (Tom de Vries)

* Wed Sep 22 2021 Bruno Larsen <blarsen@redhat.com> - 10.2-8
- Backport "[gdb/cli] Don't assert on empty string for core-file"
  (Tom de Vries)

* Tue Sep 21 2021 Peter Robinson <pbrobinson@fedoraproject.org> 10.2-7
- Use guile 2.2 (rhbz #1901353)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> 10.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Kevin Buettner <kevinb@redhat.com> - 10.2-5
- Remove autoconf invocations from spec file.
- Remove BuildRequires: autoconf.

* Mon Jun 14 2021 Kevin Buettner <kevinb@redhat.com> - 10.2-4
- Backport upstream patches which fix multi-threaded debugging for
  glibc-2.34 (RHBZ 1971096, Simon Marchi, Kevin Buettner).

* Fri Jun 11 2021 Keith Seitz <keiths@redhat.com> - 10.2-3
- Backport "Exclude debuginfo files from 'outside ELF segments' warning".
  (Keith Seitz, RH BZ 1898252)
- Backport "Fix crash when expanding partial symtab..."
  (Tom Tromey. gdb/27743)
- Backport "[gdb/server] Don't overwrite fs/gs_base with -m32"
- (Tom de Vries)

* Sun Jun 06 2021 Python Maint <python-maint@redhat.com>
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Kevin Buettner <kevinb@redhat.com> - 10.2-1
- Rebase to FSF GDB 10.2.
- Drop gdb-6.3-test-pie-20050107.patch.
- Drop gdb-6.3-test-self-20050110.patch.
- Drop gdb-6.5-bz218379-ppc-solib-trampoline-test.patch.
- Drop gdb-6.6-buildid-locate-core-as-arg.patch.
- Drop gdb-6.8-quit-never-aborts.patch.
- Drop gdb-archer-pie-addons-keep-disabled.patch.
- Drop gdb-archer-pie-addons.patch.
- Drop gdb-archer-vla-tests.patch.
- Drop gdb-archer.patch.
- Drop gdb-attach-fail-reasons-5of5.patch.
- Drop gdb-btrobust.patch.
- Drop gdb-bz1219747-attach-kills.patch.
- Drop gdb-bz533176-fortran-omp-step.patch.
- Drop gdb-dts-rhel6-python-compat.patch.
- Drop gdb-gnat-dwarf-crash-3of3.patch.
- Drop gdb-jit-reader-multilib.patch.
- Drop gdb-moribund-utrace-workaround.patch.
- Drop gdb-rhbz1930528-fix-gnulib-build-error.patch.
- Drop gdb-rhbz1932645-aarch64-ptrace-header-order.patch.
- Drop gdb-vla-intel-fix-print-char-array.patch.
- Drop gdb-vla-intel-fortran-strides.patch.
- Drop gdb-vla-intel-stringbt-fix.patch.
- Drop gdb-vla-intel-tests.patch.
- Drop process_psymtab_comp_unit-type-unit.patch.
- Drop gdb-testsuite-readline63-sigint-revert.patch.
- Drop gdb-config.patch.
- Add following upstream patches for Fortran stride / slice support:
  gdb-rhbz1964167-convert-enum-range_type.patch
  gdb-rhbz1964167-fortran-array-slices-at-prompt.patch
  gdb-rhbz1964167-fortran-array-strides-in-expressions.patch
  gdb-rhbz1964167-fortran-clean-up-array-expression-evaluation.patch
  gdb-rhbz1964167-fortran-range_type-to-range_flag.patch
  gdb-rhbz1964167-fortran-whitespace_array.patch
  gdb-rhbz1964167-move-fortran-expr-handling.patch

* Tue Jun 01 2021 Python Maint <python-maint@redhat.com>
- Bootstrap for Python 3.10

* Wed Mar 31 2021 Keith Seitz <keiths@redhat.com> - 10.1-18
- Backport "Save/restore file offset while reading notes in core file"
  (Keith Seitz, RHBZ 1931344)

* Wed Mar 31 2021 Jonathan Wakely <jwakely@redhat.com> - 10.1-17
- Rebuilt for removed libstdc++ symbols (#1937698)

* Tue Mar 23 2021 Kevin Buettner <kevinb@redhat.com>
-  Remove spec file workaround for RHBZ 1912913.

* Fri Mar 19 2021 Kevin Buettner <kevinb@redhat.com> - 10.1-16
- Fix potential hang during gdbserver testing (RHBZ 1941080, Kevin Buettner).

* Thu Mar 18 2021 Keith Seitz <keiths@redhat.com>
- Disable libctf on RHEL (RHBZ 1935517).

* Thu Mar 11 2021 Kevin Buettner <kevinb@redhat.com> - 10.1-15
- Update libipt to version 2.0.4.

* Fri Mar 05 2021 Kevin Buettner <kevinb@redhat.com> - 10.1-14
- Backport patches which fix frame_id_p assertion failure (RHBZ 1909902,
  Pedro Alves).

* Fri Mar  5 2021 Jan Kratochvil <jan.kratochvil@redhat.com> - 10.1-13
- Drop gdb-vla-intel-fortran-vla-strings.patch as it was still regressing the
  testsuite.

* Thu Mar  4 2021 Jan Kratochvil <jan.kratochvil@redhat.com> - 10.1-12
- Fix gdb-vla-intel-fortran-vla-strings.patch to no longer modify cached
  inferior types.

* Thu Mar  4 2021 Jan Kratochvil <jan.kratochvil@redhat.com> - 10.1-11
- Align gdb-vla-intel-fortran-vla-strings.patch more to upstream
  fixing whitespaces in Fortran types printing.

* Thu Mar  4 2021 Jan Kratochvil <jan.kratochvil@redhat.com> - 10.1-10
- Reapply 10.1-8 after it has been accidentally reverted by 10.1-9.

* Wed Feb 24 2021 Kevin Buettner <kevinb@redhat.com> - 10.1-9
- Fix aarch64 build problem (RHBZ 1932645, Kevin Buettner).

* Fri Feb 19 2021 Jan Kratochvil <jan.kratochvil@redhat.com> - 10.1-8
- Fix gdb-vla-intel-fortran-vla-strings.patch for compatiblity with GraalVM.

* Thu Feb 18 2021 Kevin Buettner <kevinb@redhat.com> - 10.1-7
- Fix gnulib related build problem (RHBZ 1930528, Kevin Buettner).

* Wed Feb 17 2021 Kevin Buettner <kevinb@redhat.com> - 10.1-6
- Fix libstdc++ assert when performing tab completion; build must be made
  with -D_GLIBCXX_DEBUG flag in order to trigger assert (RHBZ 1912985,
  Kevin Buettner).

* Thu Feb 11 2021 Keith Seitz
- Disable Guile support for RHEL9+.

* Tue Jan 26 2021 Stephen Gallagher <sgallagh@redhat.com> - 10.1-5
- Build gdb-minimal for ELN

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 2021 Kevin Buettner <kevinb@redhat.com>
- Add -Wno-stringop-overread to CFLAGS to work around gcc
  bug (RH BZ 1912913)

* Tue Jan 12 2021 Keith Seitz <keiths@redhat.com> - 10.1-3
- Disable xxhash support for RHEL.

* Wed Dec 09 2020 Kevin Buettner <kevinb@redhat.com> - 10.1-2
- Fix off-by-one error in ada_fold_name. (RHBZ 1905996, Kevin Buettner)

* Wed Nov 04 2020 Kevin Buettner <kevinb@redhat.com> - 10.1-1
- Rebase to FSF GDB 10.1.
- Bump 'snapgnulib' date.
- Drop gdb-rhbz1818011-bfd-gcc10-error.patch.
- Drop gdb-rhbz1822715-fix-python-deprecation.patch.
- Drop gdb-rhbz1829702-fix-python39.patch.
- Drop gdb-rhbz1838777-debuginfod.patch.
- Drop gdb-rhbz1844458-use-fputX_unfiltered.patch.
- Drop gdb-rhbz1869484-deleted-working-directory.
- Adjust build-id related patches.
- Ajust VLA patches.

* Mon Nov  2 2020 Kevin Buettner <kevinb@redhat.com> - 9.2-8
- Backport patches fixing abort when working directory is deleted.
  (RHBZ 1869484, Sergio Durigan Junior)

* Mon Nov  2  2020 Keith Seitz <keiths@redhat.com> - 9.2-7
- Fix missing debuginfo messages. (RH BZ 1887025)

* Mon Aug 10 2020 Keith Seitz <keiths@redhat.com>
- Disable LTO until upstream sorts out ODR problems.

* Tue Aug 04 2020 Keith Seitz <keiths@redhat.com>
- Update libipt to v2.0.2.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Tom Stellard <tstellar@redhat.com>
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Jul 20 2020 Jeff Law <lawb@redhat.com> - 9.2-3
- Fix broken configure tests compromised by LTO
- Add BuildRequires: autoconf

* Wed  Jun 17 2020 Keith Seitz <keiths@redhat.com> - 9.2-2
- Backport debuginfod support.

* Tue Jun  9 2020 Keith Seitz <keiths@redhat.com> - 9.2-1
- Rebase to FSF GDB 9.2.
- Add explicit python bytecode compilation.
- Change included files to patches to quell error from rpminspect.
- Fix attach-32.exp from gdb-6.3-inferior-notification-20050721.patch.

* Fri Jun  5 2020 Keith Seitz <keiths@redhat.com> - 9.1-8
- Add patch for Python 3.9 and re-enable python.
- Update generate-*.sh to include stgit support.

* Thu May 21 2020 Miro Hrončok <mhroncok@redhat.com> - 9.1-7
- Disable Python support to workaround problems with Python 3.9 (RHBZ 1829702)

* Thu Apr 16 2020 Kevin Buettner <kevinb@redhat.com> - 9.1-6
- Fix build breakage of gdb/python/python.c due to use of deprecated
  Python function (RHBZ 1822715, Kevin Buettner)

* Wed Apr 08 2020 Kevin Buettner <kevinb@redhat.com> - 9.1-5
- Fix build breakage when compiling bfd/elf.c with gcc 10. (RHBZ 1818011,
  H.J. Lu)

* Mon Mar  2 2020 Sergio Durigan Junior <sergiodj@redhat.com> - 9.1-4
- Add '--without-guile' to GDB_MINIMAL_CONFIGURE_FLAGS.

* Thu Feb 13 2020 Sergio Durigan Junior <sergiodj@redhat.com> - 9.1-3
- Fix 'Recursive call to 'missing_rpm_list_print' when pagination is
  on and missing RPM list is big' (RHBZ 1801974, Sergio Durigan
  Junior).

* Mon Feb 10 2020 Sergio Durigan Junior <sergiodj@redhat.com> - 9.1-2
- Enable libxxhash during build.

* Sat Feb  8 2020 Sergio Durigan Junior <sergiodj@redhat.com> - 9.1-1
- Rebase to FSF GDB 9.1.

* Tue Feb  4 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 9.0.90.20200203-5
- Re-enable guile support.

* Mon Feb  3 2020 Sergio Durigan Junior <sergiodj@redhat.com> - 9.0.90.20200203-4
- Rebase to FSF GDB 9.0.90.20200203 (9.1pre).
- Bump 'snapgnulib' date.
- Update URL to 'https'.
- Adjust build-id patchset.
- Adjust VLA patchset.
- Drop 'gdb-6.8-bz436037-reg-no-longer-active.patch'.
- Drop 'gdb-6.6-scheduler_locking-step-is-default.patch'.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 19 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 9.0.50.20191119-2
- Rebase to FSF GDB 9.0.50.20191119 (9.1pre).
- Drop 'gdb-readline62-ask-more-rh.patch'.
- Drop 'gdb-6.5-bz216711-clone-is-outermost.patch'.
- Adjust 'gdb-archer-pie-addons-keep-disabled.patch'.

* Fri Oct 18 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 9.0.50.20191018-1
- Rebase to FSF GDB 9.0.50.20191018 (9.1pre).
- Expand comment on "bundled(binutils)".
- Remove libctf's files from RPM_BUILD_ROOT.

* Wed Oct  9 2019 Jerry James <loganjerry@gmail.com> - 8.3.50.20190924-28
- Rebuild for mpfr 4

* Wed Sep 25 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190924-27
- Rebase to FSF GDB 8.3.50.20190924 (8.4pre).
- Update 'gdb-6.6-buildid-locate.patch'.

* Sat Aug 24 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190824-26
- Rebase to FSF GDB 8.3.50.20190824 (8.4pre).
- Update 'v1.5-libipt-static.patch'.

* Wed Aug 21 2019 Miro Hrončok <mhroncok@redhat.com>
- Rebuilt for Python 3.8

* Sun Aug 18 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190816-24
- Update bundled libipt copy to v2.0.1.

* Fri Aug 16 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190816-23
- Rebase to FSF GDB 8.3.50.20190816 (8.4pre).
- Drop 'gdb-testsuite-readline63-sigint.patch'.
- Cleanup 'gdb-archer.patch' and remove several things, like the '-P' feature.

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com>
- Rebuilt for Python 3.8

* Fri Aug  2 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190802-21
- Rebase to FSF GDB 8.3.50.20190802 (8.4pre).

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul  2 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190702-19
- Rebase to FSF GDB 8.3.50.20190702 (8.4pre).
- Remove gdb-bz568248-oom-is-error.patch.

* Tue Jun 25 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190625-18
- Rebase to FSF GDB 8.3.50.20190625 (8.4pre).

* Fri Jun 21 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190610-17
- Rebuild for librpm9 (RH BZ 1720305).

* Mon Jun 10 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190610-16
- Rebase to FSF GDB 8.3.50.20190610 (8.4pre).

* Sat Jun  1 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190601-15
- Rebase to FSF GDB 8.3.50.20190601 (8.4pre).

* Tue May 28 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190528-14
- Rebase to FSF GDB 8.3.50.20190528 (8.4pre).

* Fri May 17 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190517-13
- Rebase to FSF GDB 8.3.50.20190517 (8.4pre).

* Fri May 10 2019 Sergio Durigan Junior <sergiodj@fedoraproject.org> - 8.3.50.20190510-12
- Rebase to FSF GDB 8.3.50.20190510 (8.4pre).

* Wed May  1 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190501-11
- Rebase to FSF GDB 8.3.50.20190501 (8.4pre).
- Adjust VLA testcases.
- Fix "gcore does not support COREFILTER_ELF_HEADERS" (RH BZ 1371380,
  Sergio Durigan Junior).

* Mon Apr 29 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190425-10
- Share '/usr/bin/gdb-add-index' between gdb-minimal and gdb-headless
  (Igor Gnatenko, RHBZ 1695015).

* Mon Apr 29 2019 Sergio Durigan Junior <sergiodj@fedoraproject.org> - 8.3.50.20190425-9
- Provide 'gdb-minimal' package, specific for the buildroot (RHBZ 1695015).
- Adjust 'gdb-libexec-add-index.patch' for the gdb-minimal case.

* Thu Apr 25 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190425-8
- Rebase to FSF GDB 8.3.50.20190425 (8.4pre), and fix build breakage.

* Wed Apr 24 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190424-7
- Rebase to FSF GDB 8.3.50.20190424 (8.4pre).

* Fri Apr 12 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190412-6
- Remove 'gdb-x86_64-i386-syscall-restart.patch'.

* Fri Apr 12 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190412-5
- Rebase to FSF GDB 8.3.50.20190412 (8.4pre).
- Adjust 'gdb-6.3-rh-testversion-20041202.patch'.
- Remove 'gdb-follow-child-stale-parent.patch'.
- Remove 'gdb-rhbz795424-bitpos-20of25.patch'.
- Remove 'gdb-rhbz795424-bitpos-21of25.patch'.
- Remove 'gdb-rhbz795424-bitpos-22of25.patch'.
- Remove 'gdb-rhbz795424-bitpos-23of25.patch'.
- Remove 'gdb-rhbz795424-bitpos-25of25.patch'.
- Remove 'gdb-rhbz795424-bitpos-25of25-test.patch'.
- Remove 'gdb-rhbz795424-bitpos-arrayview.patch'.
- Remove 'gdb-rhbz795424-bitpos-lazyvalue.patch'.
- Remove 'gdb-bz541866-rwatch-before-run.patch'.

* Fri Mar 29 2019 Sergio Durigan Junior <sergiodj@fedoraproject.org> - 8.3.50.20190321-4
- Fix 'gdb-8.3.50.20190321-3.fc31.x86_64: crashing' (by fixing
  gdb-6.6-buildid-locate-rpm.patch) (RH BZ 1694091).

* Thu Mar 21 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190321-3
- Rebase to FSF GDB 8.3.50.20190321 (8.4pre).
- Remove gdb-temporary-fix-arm-build-error.patch.
- Fix "GDB crashes when using Python xmethods" (RH BZ 1690120).

* Tue Mar 19 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190319-2
- Rebase to FSF GDB 8.3.50.20190319 (8.4pre).
- Temporarily add gdb-temporary-fix-arm-build-error.patch.

* Mon Mar  4 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.3.50.20190304-1
- Rebase to FSF GDB 8.3.50.20190304 (8.4pre).
- Rewrite gdb-6.6-buildid-locate.patch.
- Remove gdb-python-gil.patch.

* Fri Feb 22 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20190222-19
- Rebase to FSF GDB 8.2.50.20190222 (8.3pre).

* Tue Feb 19 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20190219-18
- Rebase to FSF GDB 8.2.50.20190219 (8.3pre).
- BuildRequire on 'source-highlight-devel' and enable styled output.

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.2.50.20190120-17
- Disable temporarily guile support

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.2.50.20190120-16
- Rebuild for readline 8.0

* Tue Feb  5 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20190120-15
- Remove libmpx dependency when using '--with testsuite', since GCC9
  has dropped support for it.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20190120-13.fc30
- Rebase to FSF GDB 8.2.50.20190120 (8.3pre).
- Fix 'gdb does crash randomly on loading symbols or setting a breakpoint'
  (RHBZ 1638798, Keith Seitz).

* Thu Dec 20 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181220-12.fc30
- Rebase to FSF GDB 8.2.50.20181220 (8.3pre).

* Tue Dec 11 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181130-11.fc30
- Update gdb-6.3-gstack-20050411.patch (Pedro Alves).
- Update gdb-archer-next-over-throw-cxx-exec.patch (Pedro Alves).
- Update gdb-glibc-strstr-workaround.patch (Pedro Alves).

* Fri Nov 30 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181130-10.fc30
- Rebase to FSF GDB 8.2.50.20181130 (8.3pre).

* Tue Nov 20 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181114-9.fc30
- Declare _python_bytecompile_extra.
- Fix typo on gdb-x86_64-i386-syscall-restart.patch.

* Wed Nov 14 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181114-8.fc30
- Rebase to FSF GDB 8.2.50.20181114 (8.3pre).
- Drop gdb-6.3-ppc64syscall-20040622.patch.
- Drop gdb-6.3-ppc64displaysymbol-20041124.patch.
- Drop gdb-6.8-watchpoint-conditionals-test.patch.

* Thu Oct 18 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181016-7.fc30
- Use "--enable-unit-tests" flag when compiling GDB.

* Tue Oct 16 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181016-6.fc30
- Rebase to FSF GDB 8.2.50.20181016 (8.3pre).
- Enable and always run the unittests when building the package.

* Wed Oct 10 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181010-5.fc30
- Rebase to FSF GDB 8.2.50.20181010 (8.3pre).
- Remove 'gdb-6.8-sparc64-silence-memcpy-check.patch'.
- Remove 'gdb-7.2.50-sparc-add-workaround-to-broken-debug-files.patch'.

* Sat Oct  6 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20181006-4.fc30
- Rebase to FSF GDB 8.2.50.20181006 (8.3pre).

* Thu Oct  4 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.2.50.20180917-3.fc30
- Fix annobin complaints (RH BZ 1630564):
  --without-stage1-ldflags: Disable static libstdc++ and libgcc linking.
  --disable-libmcheck: That is a distro-level decision, not package decision.

* Wed Sep 19 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20180917-2.fc30
- Remove 'gdb-6.5-bz203661-emit-relocs.patch'.
- Update changelog entry for last release.

* Mon Sep 17 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.2.50.20180917-1.fc30
- Rebase to FSF GDB 8.2.50.20180917 (8.3pre).
- Add 'gdb-rhbz795424-bitpos-arrayview.patch'.
- Remove 'gdb-rhbz881849-ipv6-1of3.patch'.
- Remove 'gdb-rhbz881849-ipv6-2of3.patch'.
- Remove 'gdb-rhbz881849-ipv6-3of3.patch'.
- Remove 'gdb-rhbz1187581-power8-regs-1of7.patch'.
- Remove 'gdb-rhbz1187581-power8-regs-2of7.patch'.
- Remove 'gdb-rhbz1187581-power8-regs-3of7.patch'.
- Remove 'gdb-rhbz1187581-power8-regs-4of7.patch'.
- Remove 'gdb-rhbz1187581-power8-regs-5of7.patch'.
- Remove 'gdb-rhbz1187581-power8-regs-6of7.patch'.
- Remove 'gdb-rhbz1187581-power8-regs-7of7.patch'.

* Tue Aug 21 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180727-45.fc30
- Enable verbose output when running "make".

* Thu Aug  9 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1.90.20180727-44.fc29
- Add GDB support to access/display POWER8 registers (IBM, RH BZ 1187581).

* Thu Aug  9 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180727-43.fc29
- Reenable libipt.

* Wed Aug  8 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180727-42.fc29
- Again, temporarily disable libipt (needed to upgrade libipt to 2.0).

* Wed Aug  8 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180727-41.fc29
- Reenable libipt.
- Rebuild due to new libipt release.
- Adjust bundled libipt; remove unnecessary patch.
- Sync IPv6 patch with F-28 GDB.

* Wed Aug  8 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180727-40.fc29
- Temporarily disable libipt (needed to upgrade libipt to 2.0).

* Wed Aug  8 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1.90.20180727-39.fc29
- [dts] Fix build by removing a patch for already removed pahole.py .
- [dts rhel6] Fix build by updating gdb-gnat-dwarf-crash-3of3.patch .

* Mon Jul 30 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180727-38.fc29
- Recompile to fix RH BZ 1609504 (due to RH BZ 1609577).

* Sat Jul 28 2018 Sergio Durigan Junior <sergiodj@fedoraproject.org> - 8.1.90.20180727-37.fc29
- Rebase to FSF GDB 8.1.90.20180727 (8.2pre).

* Wed Jul 25 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180724-36.fc29
- Rebase to FSF GDB 8.1.90.20180724 (8.2pre).

* Sat Jul 14 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180714-35.fc29
- Rebase to FSF GDB 8.1.90.20180714 (8.2pre).
- Backport IPv6 patch (RH BZ 881849, Sergio Durigan Junior).

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1.90.20180708-33.fc29
- [dts] [rhel6] Do not use mpfr as rhel6 has mpfr-2 while GDB requires mpfr-3.

* Thu Jul 12 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1.90.20180708-32.fc29
- Remove as no longer needed:
  Workaround gcc-8.0: -Wno-error=cast-function-type,stringop-truncation

* Thu Jul 12 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1.90.20180708-31.fc29
- [dts] Upgrade libstdc++-v3-python to 8.1.1-20180626.

* Thu Jul 12 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180708-30.fc29
- Rebuild due to GCC ABI change.

* Sun Jul  8 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.90.20180708-29.fc29
- Rebase to FSF GDB 8.1.90.20180708 (8.2pre).

* Wed Jul  4 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180704-28.fc29
- Rebase to FSF GDB 8.1.50.20180704 (8.2pre).
- Remove defattr directives from specfile.

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com>
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180629-26.fc29
- Rebase to FSF GDB 8.1.50.20180629 (8.2pre).
- Remove pahole.py.
- Adjust handling of gdb-gdb.py.

* Sun Jun 24 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180624-25.fc29
- Rebase to FSF GDB 8.1.50.20180624 (8.2pre).

* Wed Jun 20 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180618-24.fc29
- Add BuildRequires: mpfr-devel (RH BZ 1593280).

* Mon Jun 18 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180618-23.fc29
- Rebase to FSF GDB 8.1.50.20180618 (8.2pre).

* Mon Jun 18 2018 Sergio Durigan Junior <sergiodj@fedoraproject.org> - 8.1.50.20180613-22.fc29
- Do not run /sbin/install-info when installing the documentation
  (except for DTS).

* Wed Jun 13 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180613-21.fc29
- Rebase to FSF GDB 8.1.50.20180613 (8.2pre).

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com>
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com>
- Bootstrap for Python 3.7

* Fri Jun  8 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180605-18.fc29
- Fix Python 3.7 breakage (RH BZ 1577396).

* Tue Jun  5 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180605-17.fc29
- Rebase to FSF GDB 8.1.50.20180605 (8.2pre).

* Sat Jun  2 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180522-16.fc29
- Rebase to FSF GDB 8.1.50.20180529 (8.2pre).

* Wed May 30 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1.50.20180522-15.fc28
- Rebase to FSF GDB 8.1.50.20180522 (8.2pre).

* Mon Apr  2 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1-14.fc28
- Revert 'Fix PDF build on Rawhide/F-29', rm -rf texinfo/ (from RH BZ 1562580).

* Sat Mar 31 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1-13.fc28
- Fix PDF build on Rawhide/F-29.

* Fri Mar 23 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1-12.fc28
- Add test: [s390x] Backport arch12 instructions decoding (RH BZ 1553104).

* Sat Mar  3 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1-11.fc28
- Add: BuildRequires: gcc-c++
  https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 8.1-10.fc28
- rebuild (guile)

* Sat Feb 17 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1-9.fc28
- [testsuite] Revert disable of BuildRequires: gcc-go (for RH BZ 1541639).

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.1-8.fc28
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.1-7.fc28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Feb  6 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1-6.fc28
- Fix .spec build compatibility with <=F-27 and <=RHEL-7.
- [testsuite] Temporarily disable BuildRequires: gcc-go (for RH BZ 1541639).

* Sun Feb  4 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1-5.fc28
- Workaround gcc-8.0: -Wno-error=cast-function-type,stringop-truncation
- Fix ppc64 stwux encoding as found by gcc-8.0 -Werror=tautological-compare.

* Sun Feb  4 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.1-4.fc28
- Fix -D_GLIBCXX_DEBUG gdb-add-index regression (RH BZ 1540559).

* Wed Jan 31 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.1-3.fc26
- Rebase to FSF GDB 8.1.

* Fri Jan 19 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.0.90.20180109-2.fc26
- Remove gdb-6.3-rh-dummykfail-20041202.patch (RH BZ 1535228).
- Remove gdb-glibc-vdso-workaround.patch (RH BZ 1535244).

* Wed Jan 10 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 8.0.90.20180109-1.fc26
- Rebase to pre-FSF GDB 8.1 (8.1.90.20180109).

* Sat Dec 16 2017 Sergio Durigan Junior <sergiodj@redhat.com> - 8.0.50.20171204-35.fc26
- Rebase to FSF GDB 8.0.50.20171213 (8.1pre).

* Sun Dec 10 2017 Sergio Durigan Junior <sergiodj@redhat.com> - 8.0.50.20171204-34.fc26
- chmod +x on the generate-*.sh script.s
- Remove references to gdb-8.0.1 from 'sources' and '.gitignore'.
- Regenerate first line of the patches (remove commit hash).
- Fix empty Source line.

* Thu Dec  7 2017 Sergio Durigan Junior <sergiodj@redhat.com> - 8.0.50.20171204-33.fc26
- Rebase to FSF GDB 8.0.50.20171204 (8.1pre).
- Implemented new method for dealing with local patches.

* Mon Dec  4 2017 Sergio Durigan Junior <sergiodj@redhat.com> - 8.0.1-32.fc26
- Convert all the patches to 'git-am' format.

* Sat Dec  2 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0.1-31.fc26
- [testsuite] Fix BuildRequires for non-x86* arches.

* Fri Oct 27 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0.1-30.fc26
- Use inlined func name for printing breakpoints (RH BZ 1228556, Keith Seitz).

* Sat Oct  7 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0.1-29.fc26
- [s390x] Backport arch14 guarded-storage register support (RH BZ 1498758).

* Thu Sep 28 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0.1-28.fc26
- Performance fix of gcore to use --readnever (for RH BZ 1493675).

* Tue Sep 26 2017 Troy Dawson <tdawson@redhat.com> - 8.0.1-27.fc26
- Cleanup spec file conditionals

* Tue Sep 12 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0.1-26.fc26
- Rebase to FSF GDB 8.0.1 (8.0 stable branch).

* Wed Aug 30 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-25.fc26
- [rhel6] Fix T-stopping of processes after their detachment (RH BZ 1486223).

* Thu Aug 24 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-24.fc26
- Backport DWARF-5 and breakpoint fixes from upstream stable branch 8.0.

* Sat Aug 19 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-23.fc26
- [s390x] Backport arch12 support and other s390x fixes (RH BZ 1420304).

* Fri Aug 18 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-22.fc26
- Backport a fix for clang && -gsplit-dwarf debuggees (RH BZ 1482892).

* Sun Aug 13 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-21.fc26
- Fix compatibility with F-27 debuginfo packaging.
- Fix compatibility with F-27 librpm version 8.

* Thu Aug  3 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-20.fc26
- Two fixes from upstream stable branch 8.0.

* Wed Aug  2 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-19.fc26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-18.fc26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-17.fc26
- [rhel6 dts] Use devtoolset gcc for GDB being now in C++11.

* Sat Jun 10 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-16.fc26
- [dts] Upgrade libstdc++-v3-python to 7.1.1-20170526.

* Fri Jun  9 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-15.fc26
- [rhel dts libipt] Fix#2 [-Werror=implicit-fallthrough=] with gcc-7.1.1.

* Fri Jun  9 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-14.fc26
- [rhel dts libipt] Fix [-Werror=implicit-fallthrough=] with gcc-7.1.1.

* Fri Jun  9 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 8.0-13.fc26
- Rebase to FSF GDB 8.0 final.
- [rhel7 dts] Rebase bundled libipt to 1.6.1.

* Sat May 20 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.99.90.20170420-12.fc26
- Move 'dnf-command(debuginfo-install)' gdb-headless -> gdb (RH BZ 1452335).

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.99.90.20170420-11.fc26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon May  8 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.99.90.20170420-10.fc26
- [.spec] Update patches categorization.

* Fri Apr 21 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.99.90.20170420-9.fc26
- [ppc*] Fix gdb.arch/powerpc-power7.exp testcase regression (RH BZ 1440044).

* Fri Apr 21 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.99.90.20170420-8.fc26
- Rebase to FSF GDB 7.99.90.20170420 (pre-8.0 stable branch).

* Wed Apr 19 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.50.20170309-7.fc26
- Fix reported gdb-vla-intel-stringbt-fix.patch regression (SuSE).
- Remove gcc-7 compilation compatibility hack.

* Fri Mar 10 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.50.20170309-6.fc26
- [testsuite] [ppc*,s390*] Do not FAIL rhbz1261564-aarch64-watchpoint.exp
  (RH BZ 1352563).

* Thu Mar  9 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.50.20170309-5.fc26
- Rebase to pre-7.13 FSF GDB trunk.

* Thu Mar  2 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.50.20170226-4.fc26
- Fix gdb-vla-intel-fortran-strides.patch rebase regression.

* Tue Feb 28 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.50.20170226-3.fc26
- Fix gdb.arch/amd64-entry-value-paramref.exp rebase regression.

* Tue Feb 28 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.50.20170226-2.fc26
- [testsuite] [rhel] Fix py-gil-mthread.exp for Python 2 compat (RH BZ 1427487).

* Mon Feb 27 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.50.20170226-1.fc26
- Rebase to pre-7.13 FSF GDB trunk.
- Dropped gdb-6.7-bz426600-DW_TAG_interface_type-test.patch as GCJ is no more.

* Fri Feb 24 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.1-47.fc26
- New testcase for: Fix <tab>-completion crash (Gary Benson, RH BZ 1398387).
- [testsuite] Use more standard_output_file.

* Wed Feb 15 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.1-46.fc26
- Fix <tab>-completion crash (Gary Benson, RH BZ 1398387).

* Tue Feb 14 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.1-45.fc26
- Release bump.

* Sun Feb 12 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.1-44.fc26
- [dts] Upgrade libstdc++-v3-python to 6.3.1-20170212.

* Wed Feb  8 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.1-43.fc26
- Fix build compatibility with gcc-7.

* Wed Feb  8 2017 Stephen Gallagher <sgallagh@redhat.com> - 7.12.1-42.fc26
- Add missing %%license macro

* Sat Jan 21 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12.1-41.fc26
- Rebase to released FSF GDB 7.12.1.

* Tue Jan 17 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-40.fc26
- Enable libinproctrace.so on all archs except arm32.

* Thu Jan 12 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-39.fc26
- Fix gdb-readline62-ask-more-rh.patch for Rawhide readline-7.0.

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 7.12-38.fc26
- Rebuild for readline 7.x

* Thu Jan 12 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-37.fc25
- [rhel6] Fix missing /usr/bin/realpath.

* Wed Jan 11 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-36.fc25
- Update from FSF GDB 7.12 stable branch to snapshot: gdb-7.12.0.20170111

* Sun Jan  8 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-35.fc25
- Fix Python backtraces for 32-bit inferiors (Tom Tromey, RH BZ 1411094).

* Fri Jan  6 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-34.fc25
- Fix gdb-add-index for 444 *.debug files.

* Mon Jan 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 7.12-33.fc25
- fix logic of prior Conflicts

* Mon Jan 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 7.12-32.fc25
- Conflicts: gdb-headless < 7.12-29 (#1402554)

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 7.12-31.fc25
- Python 3.6 rebuild: Rebuild with python3 support.

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 7.12-30.fc25
- Python 3.6 rebuild: Rebuild without python3 support.

* Mon Oct 31 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-29.fc25
- Fix gdb-headless /usr/bin/ executables (BZ 1390251).

* Mon Oct 24 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-28.fc25
- Fix testcase: gdb.base/gdb-rhbz1156192-recursive-dlopen.exp

* Sun Oct 23 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-27.fc25
- More work on missing testcases present in rhel6 GDB; some still FAIL.

* Thu Oct 20 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-26.fc25
- Add missing testcases present in rhel6 GDB; some still FAIL.

* Fri Oct 14 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-25.fc25
- [rhel6] Fix .spec without devtoolset-6-build installed (RH BZ 1384947).

* Wed Oct 12 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-24.fc25
- Fix TLS (such as 'errno') regression.

* Wed Oct 12 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-23.fc25
- [testsuite] Various testsuite fixes.
- [aarch64] Fix gdb.cp/nextoverthrow.exp regression (Yao Qi).

* Fri Oct  7 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-22.fc25
- Fix .spec build: error: Macro %%buildisa has empty body

* Fri Oct  7 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-21.fc25
- Rebase to FSF GDB 7.12.

* Thu Oct  6 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.20.20161006.fc25
- Rebase to FSF GDB 7.11.90.20161006 (pre-7.12 branch snapshot).

* Thu Sep 29 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.19.20160929.fc25
- Rebase to FSF GDB 7.11.90.20160929 (pre-7.12 branch snapshot).
 - Fixes GDB crashes on inf. function call scripts (RH BZ 1378147, Pedro Alves).

* Wed Sep 28 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.18.20160928.fc25
- Fix attachment of JIT-debug-enabled inf. (7.11.1 regression, RH BZ 1375553).
- Rebase to FSF GDB 7.11.90.20160928 (pre-7.12 branch snapshot).

* Wed Sep 14 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.17.20160907.fc25
- Fix description empty lines.

* Wed Sep 14 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.16.20160907.fc25
- Provide gdb-headless package (RH BZ 1195005).

* Mon Sep 12 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.15.20160907.fc25
- [testsuite] More testsuite fixes.

* Mon Sep 12 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.14.20160907.fc25
- Various mostly testsuite compatibility and regression fixes.

* Wed Sep  7 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.13.20160907.fc25
- Rebase to FSF GDB 7.11.90.20160907 (pre-7.12 branch snapshot).
- Rebase Intel VLA patchset.

* Wed Sep  7 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.12.20160904.fc25
- [rhel6+7] Fix compatibility of bison <3.1 and gcc >=6.

* Sun Sep  4 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.11.20160904.fc25
- Release bump for a mistaken build.

* Sun Sep  4 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.10.20160904.fc25
- Fix libipt bundling in 7.12.

* Sun Sep  4 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.12-0.9.20160904.fc25
- Rebase to FSF GDB 7.11.90.20160904 (pre-7.12 branch snapshot).
- Make Version tag 7.12; but it is still a pre-release.

* Mon Aug 29 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.90.20160829-8.fc25
- Rebase to FSF GDB 7.11.90.20160829 (pre-7.12 branch snapshot).

* Fri Aug 26 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.90.20160807-7.fc25
- Fix Intel VLA patchset regression: dynamic.exp: p varw filled

* Tue Aug 23 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.90.20160807-6.fc25
- Merge Fedora packaging changes from Fedora 24 gdb-7.11.1-83.fc24:

* Tue Aug 23 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.1-83.fc24
- [dts+el7] [x86*] Bundle libipt - fix#3 its initialization (RH BZ 1256513).

* Tue Aug 23 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.1-82.fc24
- [dts+el7] [x86*] Bundle libipt - fix#2 its initialization (RH BZ 1256513).

* Tue Aug 23 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.1-81.fc24
- [dts+el7] [x86*] Bundle libipt - fix its initialization (RH BZ 1256513).

* Mon Aug 22 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.1-80.fc24
- [dts] Upgrade libstdc++-v3-python to 6.1.1-20160817.

* Fri Aug 19 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.1-79.fc24
- [dts+el7] [x86*] Bundle linux_perf.h for libipt (RH BZ 1256513).

* Wed Aug 17 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.1-78.fc24
- [dts+el7] [x86*] Bundle libipt (RH BZ 1256513).

* Sun Aug  7 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.90.20160807-5.fc25
- Rebase to FSF GDB 7.11.90.20160807 (pre-7.12 branch snapshot).

* Sun Jul 31 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.50.20160721-4.fc25
- Testcase for: Load strictly build-id-checked core files only if no executable
  is specified (Jan Kratochvil, RH BZ 1339862).

* Thu Jul 28 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.50.20160721-3.fc25
- Do not apply RHEL-6 patches on non-RHEL-6 even for testsuite.

* Thu Jul 21 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.50.20160721-2.fc25
- Rebase to FSF GDB 7.11.50.20160721 (pre-7.12 trunk snapshot).

* Sun Jul 17 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.50.20160716-1.fc25
- Rebase to FSF GDB 7.11.50.20160716 (pre-7.12 trunk snapshot).

* Mon Jun 27 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.1-76.fc24
- Test 'info type-printers' Python error (RH BZ 1350436).

* Mon Jun  6 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11.1-75.fc24
- Rebase to released FSF GDB 7.11.1.

* Mon May 30 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-74.fc24
- Import bare DW_TAG_lexical_block (RH BZ 1325396).

* Tue May  3 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-73.fc24
- Fix compilation error by upstream symfile.c fix.

* Tue May  3 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-72.fc24
- Fix messages suggesting more recent RHEL gdbserver (RH BZ 1321114).

* Wed Apr 27 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-71.fc24
- Import upstream 7.11 branch stable fixes.

* Sat Apr 23 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-70.fc24
- New test for Python "Cannot locate object file for block" (for RH BZ 1325795).

* Tue Apr 12 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-69.fc24
- Never kill PID on: gdb exec PID (Jan Kratochvil, RH BZ 1219747).

* Fri Apr  8 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-68.fc24
- [--with testsuite] Add two more BuildRequires.

* Fri Apr  8 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-67.fc24
- [testsuite] Fix several false FAILs.

* Wed Apr  6 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-66.fc24
- Import upstream 7.11 branch stable fixes.

* Wed Apr  6 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-65.fc24
- Add messages suggesting more recent RHEL gdbserver (RH BZ 1321114).

* Wed Apr  6 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-64.fc24
- Fix non-stop gdb -p <container>: internal error (Pedro Alves, RH BZ 1318049).

* Sat Mar 19 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-63.fc24
- .spec cleanup: Drop strict-aliasing GCC bug workaround (from RH BZ 1315191).

* Fri Mar 18 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-62.fc24
- .spec cleanup: Drop SCL obsoletes of devtoolset-1.1*: *-1.0*

* Thu Mar 17 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-61.fc24
- Add message suggesting gdbserver for non-matching PID namespaces.

* Tue Mar 15 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-60.fc24
- New Fedora GDB testfile: rhbz1261564-aarch64-watchpoint.exp
- Backport gdb-7.11 stable branch PR gdb/19676 fix (Pedro Alves).

* Tue Mar  8 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-59.fc24
- Fix strict-aliasing rules compilation error (RH BZ 1315191).

* Fri Feb 26 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-58.fc24
- Rebase VLA (Fortran dynamic arrays) strides (multi-dim. subarrays) from Intel.

* Thu Feb 25 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-57.fc24
- Release bump only.

* Wed Feb 24 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-56.fc24
- Release bump only.

* Wed Feb 24 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.11-55.fc24
- Rebase to released FSF GDB 7.11.

* Tue Feb 16 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.90.20160216-54.fc24
- Rebase to FSF GDB 7.10.90.20160216 (pre-7.11 branch snapshot).

* Tue Feb 16 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.90.20160211-53.fc24
- Drop gdb-testsuite-subdirs-revert.patch.

* Sat Feb 13 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.90.20160211-52.fc24
- Rebase to FSF GDB 7.10.90.20160211 (pre-7.11 branch snapshot).

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.10.50.20160131-51.fc24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 31 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160131-50.fc24
- Rebase to FSF GDB 7.10.50.20160131 (trunk snapshot).

* Sun Jan 31 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160121-49.fc24
- Fix another false gcc6 compilation warning (Mark Wielaard).

* Sun Jan 31 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160121-48.fc24
- Fix false gcc6 compilation warning for: bfd/elf64-s390.c

* Sun Jan 31 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160121-47.fc24
- [testsuite] Fix false selftest.exp FAIL from system readline-6.3+ (Patrick Palka).

* Fri Jan 22 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160121-46.fc24
- Fix gdb.gdb/selftest.exp false FAIL.

* Fri Jan 22 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160121-45.fc24
- Rebase to FSF GDB 7.10.50.20160121 (trunk snapshot).

* Wed Jan 20 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-44.fc24
- Suppress librpm non-absolute filename warnings for /^remote:/ filenames.

* Sat Jan 16 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-43.fc24
- Test clflushopt instruction decode (for RH BZ 1262471).

* Sat Jan  9 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-42.fc24
- Simplify .spec: Remove conditional revert of: gdb-pahole-python2.patch

* Sat Jan  9 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-41.fc24
- Simplify .spec: Remove conditional revert of: gdb-6.8-attach-signalled-detach-stopped.patch
- Simplify .spec: Remove conditional revert of: gdb-6.8-quit-never-aborts.patch

* Sat Jan  9 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-40.fc24
- Merge gdb-rhel5-compat.patch into: gdb-6.8-attach-signalled-detach-stopped.patch

* Sat Jan  9 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-39.fc24
- Simplify .spec: Remove conditional revert of: gdb-readline62-ask-more-rh.patch

* Sat Jan  9 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-38.fc24
- Simplify .spec: Remove conditional revert of: gdb-6.6-buildid-locate-rpm-scl.patch

* Sat Jan  9 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-37.fc24
- Simplify .spec: Remove conditional revert of: gdb-dts-rhel6-python-compat.patch

* Sat Jan  9 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-36.fc24
- VLA (Fortran dynamic arrays) strides (multi-dimensional subarrays) from Intel.

* Fri Jan  8 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-35.fc24
- Fix false FAILs on too long base directory.

* Fri Jan  8 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20160106-34.fc24
- Rebase to FSF GDB 7.10.50.20160106 (trunk snapshot).

* Sat Nov 14 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20151113-33.fc24
- Rebase to FSF GDB 7.10.50.20151113 (trunk snapshot).
- [testsuite] BuildRequire libmpx for --with testsuite.
- Force libncursesw over libncurses to match the includes (RH BZ 1270534).

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.10.50.20151027-32.fc24
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sun Nov  8 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20151027-31.fc24
- [aarch64] Fix build regression (RH BZ 1278902, bugreport by Peter Robinson).

* Tue Nov  3 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10.50.20151027-30.fc24
- Rebase to FSF GDB 7.10.50.20151027 (trunk snapshot).

* Mon Oct 12 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-29.fc23
- Fix internal error on DW_OP_bregx(-1) (RH BZ 1270564).

* Mon Sep 28 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-28.fc23
- Add --with buildisa, remove %%{?_isa} from BuildRequires by default:
  https://github.com/msimacek/koschei/issues/54

* Thu Sep 24 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-27.fc23
- [rhel6,rhel7] Keep pahole.py and make it Python2 compatible.

* Wed Sep 23 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-26.fc23
- [rhel7] Provide libstdc++-v3-python with C++11 even on RHEL-7 (RH BZ 1239290).
- Do not provide libstdc++-v3-python lib64 files on 32-bit archs.
- [rhel6,rhel7] Delete pahole.py on Python2 systems.

* Wed Sep 23 2015 Robert Kuska <rkuska@redhat.com> - 7.10-25.fc23
- Python3.5 Rebuild: Rebuild wit python3 support 

* Wed Sep 23 2015 Robert Kuska <rkuska@redhat.com> - 7.10-24.fc23
- Python3.5 Rebuild: Rebuild without python3 support 

* Fri Sep 18 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-23.fc23
- Fix the pahole command breakage due to its Python3 port (RH BZ 1264532).

* Sun Sep 13 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-22.fc23
- Fix gstack to use gdb from $PATH (bugreport by Frank Hirtz, RH BZ 1262589).

* Fri Sep 11 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-21.fc23
- [testsuite] Fix gcc-gdb-plugin and gcc-go BuildRequires for --with testsuite.

* Thu Sep 10 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-20.fc23
- [ppc64le] Use skip_entrypoint for skip_trampoline_code (RH BZ 1260558).

* Thu Sep 10 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-19.fc23
- Add changelog entry and fix librpm dependency broken by Peter Robinson.

* Thu Sep  3 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-18.fc23
- Enable libipt (Intel Processor Trace Decoder Library).

* Wed Sep  2 2015 Sergio Durigan Junior <sergiodj@redhat.com> - 7.10-17.fc23
- Fix 'Make the probes-based dynamic linker interface more robust to
  errors' (Sergio Durigan Junior, RH BZ 1259132).

* Tue Sep  1 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-16.fc23
- [RHEL] Fix librpm Recommends compatibility.

* Sat Aug 29 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-15.fc23
- Rebase to FSF GDB 7.10 final.

* Sat Aug 22 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-14.fc23
- Re-enable --with testsuite BuildRequires: prelink for RHELs.

* Sat Aug 22 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.10-13.fc23
- Rebase to FSF GDB 7.9.90.20150822 (7.10 branch snapshot).
- Remove --with testsuite BuildRequires: prelink (prelink is orphaned in F-23+).

* Thu Aug  6 2015 Sergio Durigan Junior <sergiodj@redhat.com> - 7.9.90.20150717-12.fc23
- Add "Recommends: default-yama-scope" (for RH BZ 1209492).

* Thu Aug  6 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.90.20150717-11.fc23
- Fix librpm version for f23.

* Sun Aug  2 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.90.20150717-10.fc23
- Fix unpackaged d-exp.c source for the debuginfo rpm.
- Fix librpm version dependency Koji build failure (for RH BZ 1249325).

* Sun Aug  2 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.90.20150717-9.fc23
- Fix librpm version dependency (for RH BZ 1249325, from Igor Gnatenko).

* Sat Aug  1 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.90.20150717-8.fc23
- Fix librpm version 3->7 for Rawhide
  (RH BZ 1249325, bugreport by Zbigniew Jędrzejewski-Szmek).
- Fix yum vs. dnf message suggestion for Rawhide
  (RH BZ 1249326, bugreport by Zbigniew Jędrzejewski-Szmek).

* Fri Jul 17 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.90.20150717-7.fc23
- Rebase to FSF GDB 7.9.90.20150717 (7.10 branch snapshot).

* Fri Jul 10 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.90.20150709-6.fc23
- Rebase to FSF GDB 7.9.90.20150709 (7.10 branch snapshot).

* Tue Jul  7 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.50.20150531-5.fc23
- Upgrade libstdc++-v3-python to r225521 (RH BZ 1239290).

* Thu Jul  2 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.50.20150531-4.fc23
- [RHEL] Use Python2, disable Guile.

* Fri Jun 26 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.50.20150531-3.fc23
- Fix 'info type-printers' Python error (Clem Dickey, RH BZ 1085576).

* Tue Jun 16 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.50.20150531-2.fc23
- Fix enum e e 'Attempt to use a type name as an expr.' (Keith Seitz, PR 16253).

* Sun May 31 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.50.20150531-1.fc23
- Rebase to FSF GDB 7.9.50.20150531 (pre-7.10 trunk snapshot).

* Fri May 15 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.1-14.fc22
- Fix ignored Requires for gdb-doc (RH BZ 1221814).

* Thu May 14 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.1-13.fc22
- Change 'Recommends: dnf-plugins-core' to 'dnf-command(debuginfo-install)'.

* Wed May 13 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9.1-12.fc22
- Rebase to FSF GDB 7.9.1 (7.9 stable branch).
- Add 'Recommends: dnf-plugins-core' for 'dnf debuginfo-install'.

* Thu Apr  2 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9-11.fc22
- Suggest s/debuginfo-install/dnf debuginfo-install/ (BZ 1208650, Omair Majid).

* Sun Feb 22 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.9-10.fc22
- Rebase to the final 7.9 release.

* Sun Feb 22 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.90.20150202-9.fc22
- Change Require->Recommends for gcc-gdb-plugin (RH BZ 1195005).

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 7.8.90.20150214-8
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Feb 16 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.90.20150214-7.fc22
- Switch Python 2->3 (RH BZ 1014549).

* Sat Feb 14 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.90.20150214-6.fc22
- Rebase to 7.9-branch snapshot 7.8.90.20150214.

* Wed Feb 11 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.90.20150202-5.fc22
- Enable guile support.

* Wed Feb 11 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.90.20150202-4.fc22
- Fix gcc5 compilation errors (RH BZ 1190649).

* Mon Feb  9 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.90.20150202-3.fc22
- Require gcc-gdb-plugin.

* Mon Feb  2 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.90.20150202-2.fc22
- Rebase to 7.9-branch snapshot 7.8.90.20150202.
- Temporarily disable dg-extract-results.py to fix gdb.sum sorting.

* Thu Jan  8 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.50.20150108-1.fc22
- Rebase to pre-7.9 snapshot 7.8.50.20150108.
- Fix jit-reader.h for multi-lib.

* Sun Dec 28 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.1-36.fc21
- Rebase to 7.8.1.20141228 for a performance fix (PR binutils/17677).

* Sat Dec 13 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.1-35.fc21
- Fix resolve_dynamic_struct: Assertion `TYPE_NFIELDS (type) > 0' (PR 17642).

* Sat Nov 22 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.1-34.fc21
- [ppc64] Fix compatibility of Fedora errno workaround (for RH BZ 1166549).

* Fri Nov 21 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.1-33.fc21
- Fix regression accessing errno from a core file (RH BZ 1166549).

* Thu Nov 20 2014 Sergio Durigan Junior <sergiodj@redhat.com> - 7.8.1-32.fc21
- Fix 'Unowned dir /usr/include/gdb/' (RH BZ 1164991).

* Sat Nov 15 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.1-31.fc21
- Fix '[RFE] please add add-auto-load-scripts-directory command' (RH
  BZ 1163339, Jan Kratochvil).

* Thu Oct 30 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8.1-30.fc21
- Rebase to FSF GDB 7.8.1.

* Mon Oct 27 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-29.fc21
- Backport vDSO regression.
- Revert the makeinfo workaround from 7.8-27.fc21.
- Further 1.75x improvement of the interactive symbols lookup (Doug Evans).

* Mon Oct 20 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-28.fc21
- Accelerate interactive symbols lookup 15x.

* Sun Oct 19 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-27.fc21
- Workaround makeinfo F-22 Bug 1154436.

* Sun Oct 19 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-26.fc21
- Import 5 upstream gdb-7.8 branch fixes (async fix by Pedro Alves).

* Fri Oct 03 2014 Sergio Durigan Junior <sergiodj@redhat.com> - 7.8-25.fc21
- Fix 'Slow gstack performance' (RH BZ 1103894, Jan Kratochvil).

* Fri Oct  3 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-24.fc21
- Fix "save breakpoints" for signal catchpoints and disabled breakpoints
  (BZ 1146170, Miroslav Franc).

* Mon Sep 15 2014 Sergio Durigan Junior <sergiodj@redhat.com> - 7.8-23.fc21
- Install gdb/jit-reader.h on include directory (BZ 1141968).

* Sun Sep 14 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-22.fc21
- [testsuite] Fix runaway gdb.base/attach processes.

* Sun Sep  7 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-21.fc21
- Fix GDB SIGTT* Stopped when using the PID argument (BZ 1136704, Pedro Alves).

* Wed Aug 20 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-20.fc21
- Fix babeltrace errors (Yao Qi).
- Fix crash on Python frame filters with unreadable arg (BZ 1126177).

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-18.fc21
- [rhel] Adjust the previous patch for compilation on older GCCs.

* Wed Aug 13 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-17.fc21
- Fix Python GIL with gdb.execute("continue") (Phil Muldoon, BZ 1116957).

* Mon Aug  4 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-16.fc21
- Enable babeltrace compile-time feature.

* Sat Aug  2 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-15.fc21
- Rebase to FSF GDB 7.8.
- Display Fortran strings in backtraces.

* Thu Jul 24 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-14.fc21
- Rebase to FSF GDB 7.7.91.20140724 (pre-7.8 snapshot).
- Import TUI regression fix (Pedro Alves, BZ 1123003).

* Tue Jul 22 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.8-13.fc21
- Bump the package version number to final 7.8; still using 7.7.91.20140721.tar.

* Tue Jul 22 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.91.20140721-12.fc21
- Rebase to FSF GDB 7.7.91.20140721 (pre-7.8 snapshot).
- Rebase the Intel VLA patchset.
- New fix of the optimized-out entry data values crash (BZ 1111910).
- [testsuite] Fix paginate-*.exp race for "read1".

* Fri Jul 11 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140711-11.fc21
- Fix regression#2 of the optimized-out entry data values fix (of BZ 1111910).
- Rebase to FSF GDB 7.7.90.20140711 (pre-7.8 snapshot).
- [testsuite] Disable --with testsuite PIE testing, it has too many false FAILs.

* Wed Jul  9 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140627-10.fc21
- Fix regression of the optimized-out entry data values fix (of BZ 1111910).

* Tue Jul  8 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140627-9.fc21
- Rebase the Intel VLA patchset.
- Python completion w/overriden completer (Sergio Durigan Junior, BZ 1075199).
- Remove %%{_bindir}/mono-gdb.py workaround of mono BZ 815501.

* Tue Jul  1 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140627-8.fc21
- Do not remove %%{_datadir}/gdb/syscalls/ppc*.xml as it is secondary target.
- Remove: %%{_datadir}/gdb/guile
- Remove: %%{_datadir}/gdb/system-gdbinit

* Mon Jun 30 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140627-7.fc21
- Fix crash on optimized-out entry data values (BZ 1111910).

* Fri Jun 27 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140627-6.fc21
- Rebase to FSF GDB 7.7.90.20140627 (pre-7.8 snapshot).

* Fri Jun 27 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140613-5.fc21
- Continue backtrace even if a frame filter throws an exception (Phil Muldoon).

* Tue Jun 24 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140613-4.fc21
- [aarch64] Fix compilation error.

* Fri Jun 20 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140613-3.fc21
- Fix --with-system-readline with readline-6.3 patch 5.
  - Use --enable-werror again.

* Thu Jun 19 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140613-2.fc21
- Temporarily use --disable-werror for readline-6.3's deprecated 'VFunction'.

* Thu Jun 19 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.90.20140613-1.fc21
- Rebase to FSF GDB 7.7.90.20140613 (pre-7.8 snapshot).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.7.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun  3 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-20.fc21
- Fix#2 /usr/share/gdb/system-gdbinit/ timestamps causing non-matching *.py[oc].

* Tue Jun  3 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-19.fc21
- Fix /usr/share/gdb/auto-load/ (safely) dangling symlinks.
- Fix /usr/share/gdb/system-gdbinit/ timestamps causing non-matching *.py[oc].

* Tue Jun  3 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-18.fc21
- [ppc64le testsuite] Add comments about prelink+valgrind not yet ported.

* Fri May 30 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-17.fc21
- [arm*,aarch64] Turn on --enable-werror, fix aarch64 for it.

* Fri May 30 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-16.fc21
- [aarch64] Fix signal frame unwinding (BZ 1086894, upstream).

* Mon May 26 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-15.fc21
- [testsuite] Drop BuildRequires: gcc-java+libgcj on Fedora (no longer in F21+).

* Fri May 16 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-14.fc21
- [rhel5] Drop the RHEL-5 support - simplify this .spec file.

* Wed May 14 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-13.fc21
- [s390*] Import upstream fix for 64->32 debugging.

* Mon May 12 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-12.fc21
- [s390*] Fix compilation error.

* Fri May  9 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-11.fc21
- [ppc*] Import ppc64le support (BZ 1096303, Ulrich Weigand).

* Tue May  6 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7.1-10.fc21
- Rebase to FSF GDB 7.7.1.

* Mon May  5 2014 Sergio Durigan Junior <sergiodj@redhat.com> - 7.7-9.fc21
- Improve testcase message for RH BZ 981154.

* Mon May  5 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7-8.fc21
- Fix TLS access for -static -pthread (BZ 1080660).

* Mon May  5 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7-7.fc21
- Add GFDL License to the main package (man pages are generated from .texinfo).

* Thu Apr 24 2014 Sergio Durigan Junior <sergiodj@redhat.com> - 7.7-6.fc21
- Fix build failures for GCC 4.9 (Nick Clifton).

* Thu Apr 24 2014 Sergio Durigan Junior <sergiodj@redhat.com> - 7.7-5.fc21
- Fix 'gdb gives highly misleading error when debuginfo pkg is present,
  but not corresponding binary pkg' (RH BZ 981154).

* Mon Feb 24 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7-4.fc21
- Fix crash of -readnow /usr/lib/debug/usr/bin/gnatbind.debug (BZ 1069211).

* Sun Feb 23 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7-3.fc21
- [rhel6] DTS backward Python compatibility API (BZ 1020004, Phil Muldoon).
- [rhel6] Do not install its man page if gdb-add-index is not installed.
- [rhel] Do not migrate /usr/share/gdb/auto-load/ with symlinks on RHELs.
- Fix gdb-7.7 auto-load from /usr/share/gdb/auto-load/ regression.

* Sun Feb  9 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7-2.fc21
- [rhel] Fix rebase build regression on RHEL systems (Tobias Burnus).

* Fri Feb  7 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.7-1.fc21
- Rebase to FSF GDB 7.7.
- New rpmbuild option: --with asan

* Thu Jan 23 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20140119-20.fc20
- [s390*,ppc*] Enable secondary targets s390* and ppc* (BZ 1056259).

* Sun Jan 19 2014 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20140119-19.fc20
- Backport several gdb-7.6.x stable branch fixes (BZ 1055155).

* Wed Dec 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-18.fc20
- [aarch64] Backport two breakpoint/watchpoint fixes.

* Mon Nov 18 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-17.fc20
- [rhel7] [--with testsuite] Remove gcc-java&co. BuildRequires.

* Sat Nov  9 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-16.fc20
- Fix explicit Class:: inside class scope (BZ 874817, Keith Seitz).

* Tue Nov  5 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-15.fc20
- [aarch64] Backport two fixes (BZ 1026484).

* Sun Nov  3 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-14.fc20
- Fix %%{_bindir}gdb-add-index to also use -iex 'set auto-load no'.

* Wed Oct 30 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-13.fc20
- [rhel5] Fix /etc/gdbinit compatibility with python-2.4.

* Mon Sep 30 2013 Sergio Durigan Junior <sergiodj@redhat.com> - 7.6.50.20130731-12.fc20
- Fix the case when GDB leaks memory because value_struct_elt does not call
  check_typedef.  (Doug Evans, BZ 15695, filed as RH BZ 1013453).

* Wed Sep 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-11.fc20
- Enable arm-linux-gnu and aarch64-linux-gnu targets on all archs (BZ 1011647).

* Mon Sep  9 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-10.fc20
- Fix the version string to be GNU standards compliant (BZ 1004949).

* Fri Aug 30 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-9.fc20
- Load /etc/gdbinit.d/*.{gdb,py} files automatically (BZ 981520).

* Fri Aug 30 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-8.fc20
- New %%pre to fix failed upgrade of the previous commit (BZ 999645).
- Fix false warnings of new %%pre during future upgrades (BZ 999645).

* Wed Aug 28 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-7.fc20
- Fix /usr/share/gdb/auto-load/ need of filesystem symlinks (BZ 999645).
  It needs: yum remove gdb-heap; yum reinstall gdb; yum install gdb-heap

* Thu Aug  8 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-6.fc20
- [rhel5] tps-srpmtest does not set %%{rhel} (BZ 1002198, Miroslav Franc).

* Thu Aug  8 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-5.fc20
- Simplify BuildRequires by texlive-collection-latexrecommended (see BZ 919891).

* Tue Aug  6 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-4.fc20
- Revert the texlive-collection-latexrecommended change (see BZ 919891).

* Tue Aug  6 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-3.fc20
- Simplify BuildRequires by texlive-collection-latexrecommended (see BZ 919891).
- Fix crash on 'enable count' (Simon Marchi, BZ 993118).

* Fri Aug  2 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-2.fc20
- Drop ia64 patches and .spec support.

* Fri Aug  2 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6.50.20130731-1.fc20
- Rebase to FSF GDB 7.6.50.20130731 (snapshot between 7.6 and future 7.7).

* Mon Jul 29 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-36.fc20
- Remove %%{gdb_docdir}, rebuild for unversioned docdirs (for BZ 986871).

* Wed Jul 24 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-35.fc20
- [ppc] Support Power8 CPU (IBM, BZ 731875).

* Wed Jul 17 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-34.fc20
- Remove --disablerepo='*' from BZ 554152 as it conflicts with BZ 981154.

* Wed Jul 17 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-33.fc20
- Fix yum install command output when the binary RPM is missing (BZ 981154).
- Fix the changlog entry formatting for 6.3.0.0-0.1.

* Mon Jun 10 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-32.fc19
- [scl] Disable Python frame filters on scl.
- Update libraries opening performance fix from upstream.
- Fix C++ lookups performance regression (Doug Evans, BZ 972677).

* Tue May 28 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-31.fc19
- [ppc] Backport hardware watchpoints fix (Edjunior Machado, BZ 967915).

* Tue May 21 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-30.fc19
- Backported Python frame filters (Phil Muldoon).
- Backported breakpoint conditions crash fix (Sergio Durigan Junior).

* Sun May 19 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-29.fc19
- Fix performance regression opening many libraries (Gary Benson, BZ 965106).

* Thu May  9 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-28.fc19
- Fix needless expansion of non-gdbindex symtabs (Doug Evans).

* Mon May  6 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-27.fc19
- [testsuite] [RHEL-5] Fix gdb-orphanripper.c runtime error.

* Fri May  3 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-26.fc19
- Fix gcore for vDSO (on ppc64).

* Sat Apr 27 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-25.fc19
- Fix false "Unknown error 512" on x32 (H.J. Lu, BZ 956883).

* Fri Apr 26 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.6-24.fc19
- Rebase to FSF GDB 7.6.

* Wed Apr 24 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130423-23.fc19
- Fix man page BuildRequires (for BZ 881892).

* Tue Apr 23 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130423-22.fc19
- [spec] Fix virtual bundles after GDB has been branched.

* Tue Apr 23 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130423-21.fc19
- Rebase to FSF GDB 7.5.91.20130423 (pre-7.6 snapshot).

* Mon Apr 22 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130407-20.fc19
- [SCL] Skip deprecated .gdb_index warning for Red Hat built files (BZ 953585).

* Mon Apr 22 2013 Sergio Durigan Junior <sergiodj@redhat.com> - 7.5.91.20130407-19.fc19
- [RHEL-6] Regression test for RH BZ 947564.

* Thu Apr 11 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130407-18.fc19
- Provide man page for gcore.1 and gdb-add-index.1 (BZ 881892).

* Sun Apr  7 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130407-17.fc19
- [RHEL-5] Fix noarch doc build.

* Sun Apr  7 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130407-16.fc19
- Rebase to FSF GDB 7.5.91.20130407 (pre-7.6 snapshot).
- [SCL] Remove BuildRequires of gcc-go on SCL (Miroslav Franc, BZ 948982).
- Provide man page for gdbinit.5 (BZ 881892), document gdb -p in man (BZ 659000).

* Tue Apr  2 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130402-15.fc19
- Rebase to FSF GDB 7.5.91.20130402 (pre-7.6 snapshot).

* Sat Mar 23 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.91.20130323-14.fc19
- Rebase to FSF GDB 7.5.91.20130310 (pre-7.6 snapshot).
- Fix crash regression from the dlopen of libpthread.so fix (BZ 911712).

* Mon Mar 11 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130310-13.fc19
- [RHEL-5] Import build regression fix.

* Sun Mar 10 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130310-12.fc19
- Add workaround of PDF gdb-doc build (filed as RH BZ 919891).

* Sun Mar 10 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130310-11.fc19
- Re-enable (again) PDF in gdb-doc after texinfo RH BZ 876710 has been fixed.

* Sun Mar 10 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130310-10.fc19
- Rebase to FSF GDB 7.5.50.20130310 (pre-7.6 snapshot).
- Fix various entry-values sub-optimal results.

* Mon Feb 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130215-9.fc19
- testsuite: Fix gdb.arch/powerpc-power6.exp testcase (IBM, RH BZ 890900).

* Tue Feb 19 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130215-8.fc19
- Temporarily disable PDF in gdb-doc for still unavailable texinfo RH BZ 876710.

* Mon Feb 18 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130215-7.fc19
- Rebase to FSF GDB 7.5.50.20130215 (pre-7.6 snapshot).

* Fri Feb  8 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130118-6.fc19
- Re-enable PDF in gdb-doc after texinfo RH BZ 876710 has been fixed.

* Mon Feb  4 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130118-5.fc19
- Release bump only.

* Fri Feb  1 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130118-4.fc19
- Fix assert crashes with minidebuginfo (BZ 903522).

* Fri Jan 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130118-3.fc19
- Release bump only.

* Mon Jan 21 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130118-2.fc19
- [RHEL] Reintroduce gdb-6.8-quit-never-aborts.patch.

* Sat Jan 19 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.50.20130118-1.fc19
- Rebase to FSF GDB 7.5.50.20130118 (pre-7.6 snapshot).

* Sun Jan 13 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-35.fc18
- [testsuite] Fix gdb-orphanripper.c lockup on F-17 (/dev/pts/* glibc chown).

* Tue Jan  8 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-34.fc18
- Update dlopen to support map_failed probe of glibc (Gary Benson, BZ 886516).

* Thu Jan  3 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-33.fc18
- [ppc*] Fix PowerPC disassembly regression (Alan Modra, Edjunior Machado).

* Thu Dec 13 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-32.fc18
- 'dwz -m' parsing fix (Tom Tromey).

* Mon Dec  3 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-31.fc18
- Fix DW_OP_GNU_implicit_pointer offset bug (Tom Tromey).

* Sun Dec  2 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-30.fc18
- Temporarily disable PDF in gdb-doc before texinfo RH BZ 876710 gets fixed.

* Thu Nov 29 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-29.fc18
- Provide Source URL when it is a release.

* Thu Nov 29 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-28.fc18
- Fix (unsplit) split info doc.

* Thu Nov 29 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.1-27.fc18
- Rebase to FSF GDB 7.5.1 (7.5 stable branch).

* Fri Nov  9 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.0.20120926-26.fc18
- Fix `GDB cannot access struct member whose offset is larger than 256MB'
  (RH BZ 871066).

* Fri Oct  5 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.0.20120926-25.fc18
- entry values: Fix resolving in inlined frames.

* Thu Sep 27 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.0.20120926-24.fc18
- Permit passing pointers as address number even for C++ methods (Keith Seitz).

* Thu Sep 27 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.0.20120926-23.fc18
- Fix crash printing classes (BZ 849357, Tom Tromey).

* Wed Sep 26 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.0.20120926-22.fc18
- Fix .spec 'bundled' Provides for the stable branch rebase.

* Wed Sep 26 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5.0.20120926-21.fc18
- [ppc32] Fix stepping over symbol-less code crash regression (BZ 860696).
- Rebase to FSF GDB 7.5.0.20120926 (7.5 stable branch).
  - Remove the .spec Source keyword URL as not valid now.

* Fri Sep 14 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5-20.fc18
- [RHEL-6] Disable no longer valid workaround of man pages .gz suffix.

* Sat Aug 18 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.5-19.fc18
- Rebase to FSF GDB 7.5.
- Update dlopen to support two variants of glibc (Gary Benson, BZ 669432).

* Fri Aug 17 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.91.20120801-18.fc18
- Drop Source URL for snapshots.
- Separate %%{snapgnulib} from %%{snap}.
- Fix %%{libstdcxxpython} to be %%{name}-prefixed.
- Fix debug info for go-exp.y and go-exp.c.
- Include RHEL-5 compatible %%{buildroot} cleanup.
- Use %%__global_ldflags.

* Wed Aug  1 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.91.20120801-17.fc18
- Rebase to FSF GDB 7.4.91.20120801.
- [dwz] Rebase it from FSF GDB HEAD.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.50.20120714-16.fc18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120714-15.fc18
- [devtoolset] Include Obsoletes of devtoolset-1.0-* by devtoolset-1.1-*.

* Sun Jul 15 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120714-14.fc18
- Rebase to FSF GDB 7.4.50.20120714.
  - Fix entryval feature crash on some .debug files optimized by dwz (BZ 839596).
- Fix another stale frame_info * (PR 11914, like PR 13866).

* Fri Jul  6 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120703-13.fc18
- [RHEL] Disable MiniDebugInfo F-18 feature on RHEL <= 6 (BZ 834068).

* Fri Jul  6 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120703-12.fc18
- Fix .spec metadata for the MiniDebugInfo F-18 feature (BZ 834068).

* Fri Jul  6 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120703-11.fc18
- [archer-tromey-dwz-multifile-rebase] Fix DWARF files reading (Tom Tromey).

* Fri Jul  6 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120703-10.fc18
- Fix build-id-core-loads internal error (BZ 837870).

* Thu Jul  5 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120703-9.fc18
- Implement MiniDebugInfo F-18 Feature consumer (Alexander Larsson, BZ 834068).

* Tue Jul  3 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120703-8.fc18
- Rebase to FSF GDB 7.4.50.20120703.
- [archer-tromey-dwz-multifile-rebase] Merge new branch (Tom Tromey).
- [arm] <--with testsuite>: Disable fpc BuildRequires as it is not yet built.
- Revert function returning pointer fix (PR 9514) regressing Fedora errno patch.

* Thu Jun 21 2012 Sergio Durigan Junior <sergiodj@redhat.com> - 7.4.50.20120603-7.fc18
- Include testcase for BZ 818343.

* Tue Jun 19 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120603-6.fc18
- Fix regression of undisplayed missing shared libraries caused by a fix for:
  GNU/Linux core open: Can't read pathname for load map: Input/output error.

* Sun Jun 17 2012 Sergio Durigan Junior <sergiodj@redhat.com> - 7.4.50.20120603-5.fc18
- Include testcase for BZ 823789.

* Thu Jun 14 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120603-4.fc18
- Support DW_OP_GNU_parameter_ref for -O2 -g inferiors (BZ 827375).

* Wed Jun  6 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120603-3.fc18
- Disable -lmcheck in the development builds.
- Fix assertion on some files as glibc-2.15.90-8.fc18 (Doug Evans).

* Sun Jun  3 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120603-2.fc18
- Fix Release.
- Make yum --enablerepo compatible with at least mock-1.1.21-1.fc16 Rawhide cfg.

* Sun Jun  3 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120602-1.fc18
- Rebase to FSF GDB 7.4.50.20120602.
- [testsuite] BuildRequire gcc-go.
- Drop printing 2D C++ vectors as matrices which no longer worked (BZ 562763).
- Fix dejagnu-1.5-4.fc17 compatibility for Go (for BZ 635651).
- Use librpm.so.3 for rpm-4.10.0 in Fedora 18.
- Revert recent breakage of UNIX objfiles order for symbols lookup.

* Sat Jun  2 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-48.fc17
- [ppc] Fix hardware watchpoints on PowerPC (BZ 827600, Edjunior Machado).

* Mon May 28 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-47.fc17
- Workaround PR libc/14166 for inferior calls of strstr.

* Mon May 14 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-46.fc17
- [RHEL5] Workaround doc build race.

* Mon May 14 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-45.fc17
- Rename "set auto-load" patchset variable $ddir to $datadir.

* Wed May  9 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-44.fc17
- Fix in "set auto-load" patchset for SCL scripts inheritance (BZ 815910).

* Wed Apr 25 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-43.fc17
- [RHEL5] Workaround kernel for detaching SIGSTOPped processes (BZ 809382).

* Tue Apr 24 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-42.fc17
- Update "set auto-load" patchset and the --with-auto-load-safe-path setting.
- [RHEL] Disable gdb-add-index even on RHEL-6 as RHEL-6.0 had too old elfutils.

* Wed Apr 18 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-41.fc17
- [RHEL] Fix --with-auto-load-safe-path systems prior to /usr move.

* Wed Apr 18 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-40.fc17
- Security fix for loading untrusted inferiors, see "set auto-load" (BZ 756117).

* Fri Apr 13 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-39.fc17
- [RHEL7] Fix/remove readline-devel BuildRequires redundant distro suffic .fc17.

* Wed Apr  4 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-38.fc17
- Workaround crashes from stale frame_info pointer (BZ 804256).

* Wed Apr  4 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-37.fc17
- testsuite: Fix break-interp.exp expections for updated glibc (BZ 752834).

* Wed Apr  4 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-36.fc17
- [RHEL5,RHEL6] Reintroduce fix attaching to stopped processes.

* Fri Mar 30 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-35.fc17
- Fix performance regressions with .gdb_index (Tom Tromey, BZ 805274).

* Fri Mar 30 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-34.fc17
- Fixup %%{_datadir}/gdb timestamps for multilib conflicts on RHELs.

* Mon Mar 26 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-33.fc17
- [vla] Fix regression on no type for subrange from IBM XLF Fortran (BZ 806920).

* Sat Mar 17 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-32.fc17
- Fix loading of core files without build-ids but with build-ids in executables.

* Fri Mar  9 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-31.fc17
- Fix an implied regression by the inferior calls fix below (BZ 799531).

* Fri Mar  9 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-30.fc17
- Fix SELinux deny_ptrace .spec build rules (BZ 786878).

* Tue Mar  6 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-29.fc17
- Fix inferior calls, particularly uncaught thrown exceptions (BZ 799531).
- Fix DWARF DIEs CU vs. section relative offsets (Joel Brobecker, me).

* Tue Mar  6 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-28.fc17
- Print reasons for failed attach/spawn incl. SELinux deny_ptrace (BZ 786878).

* Sun Mar  4 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-27.fc17
- [rhel5] Fix up the previous commit (BZ 799318).

* Sun Mar  4 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-26.fc17
- [rhel5] Fix up the previous commit (BZ 799318).

* Sun Mar  4 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-25.fc17
- [rhel5] Workaround rpmbuild to make the doc subpkg noarch again (BZ 799318).

* Fri Mar  2 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-24.fc17
- [vla] Fix crash for dynamic.exp with gcc-gfortran-4.1.2-51.el5.x86_64.
- Reintroduce RHEL-5 glibc workaround for bt-clone-stop.exp.
- testsuite: Update/fix rh634108-solib_address.exp for the upstreamed API.

* Wed Feb 29 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-23.fc17
- Add kernel vDSO workaround (`no loadable ...') on RHEL-5 (kernel BZ 765875).
- Fix skipping of prologues on RHEL-5 gcc-4.1 -O2 -g code (BZ 797889).
- Fix breakpoint warning during 'next' over exit() (Tom Tromey, BZ 797892).

* Tue Feb 28 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-22.fc17
- testsuite: Fix gdb.base/macscp.exp ccache workaround in SCL mode.
- Adjust the RHEL/F version string automatically (BZ 797651, BZ 797646).
- Provide gdbtui for RHEL-5 and RHEL-6 as it is removed upstream (BZ 797664).

* Fri Feb 24 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-21.fc17
- testsuite: Do not use gcc44/gfortran44 on RHEL-5 if in SCL mode.

* Wed Feb 22 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-20.fc17
- Fix libinproctrace.so build on RHEL-5 i386 (disable it on RHEL-5).

* Wed Feb 22 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-19.fc17
- Implement SCL (scl-utils-build) macros.

* Tue Feb 21 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-18.fc17
- Fix debuginfo gdb-gdb.py build without redhat-rpm-config and on RHEL-5.
- Provide precompiled variants of gdb-gdb.py.

* Mon Feb 13 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-17.fc17
- gstack: Turn off --readnever (suggested by Oliver Henshaw).

* Fri Feb 10 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-16.fc17
- [RHELs] Drop simulation of legacy behavior - new GDB should behave as new GDB.

* Fri Feb 10 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-15.fc17
- Simplify %%setup .spec rule.

* Fri Feb 10 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-14.fc17
- Drop --with upstream .spec rules.

* Fri Feb 10 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-13.fc17
- Drop --with debug .spec rules.

* Thu Feb  9 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-12.fc17
- Improve performance for C++ symbols expansion (Tom Tromey, BZ 787487).
- Install also gdb-gdb.py pretty printers.

* Thu Feb  9 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-11.fc17
- Fix possible NULL crash in find_charset_names (Tom Tromey, BZ 786091).
- [ppc*] Fix build failure due to GCC aliasing warning (BZ 786504).

* Sat Jan 21 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120120-10.fc17
- Rebase to FSF GDB 7.4.50.20120120.
- Drop the g77 .spec provisioning as it has been fixed in FSF GDB.

* Thu Jan 19 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-9.fc17
- Enable smaller %%{_bindir}/gdb in future by no longer using -rdynamic.
- Make --enablerepo to use '*-debug*' for RHEL compatibility (BZ 781571).
- On older RHELs make readline bundled again (BZ 701131).
- Fix build compatibility with RHEL-5 due to false noarch build.

* Wed Jan 11 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-8.fc17
- Disable unexpected GDB directories relocatability.

* Wed Jan 11 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-7.fc17
- Fix BuildRequires for RHEL compatibility (BZ 701131).

* Wed Jan 11 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-6.fc17
- Provide %%snap timestamp for: Provides: bundled(librarypackage)
- Replace %%define by %%global.
- Replace Java in Summary with Fortran (only GCC-compiled Java is supported).
- Unbundle readline-6.2 with a workaround of skipped "ask" (BZ 701131).
- Work around readline-6.2 incompatibility not asking for --more-- (BZ 701131).

* Sat Jan  7 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-5.fc17
- Mark %%{_sysconfdir}/gdbinit as %%config(noreplace).
- Add appropriate: Provides: bundled(librarypackage).
- Remove excessive explicit Requires: librarypackage.

* Thu Jan  5 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-4.fc17
- Fix linking on non-x86* (such as s390*) after libgdb.a removal.

* Wed Jan  4 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-3.fc17
- Reinclude gdb-dlopen-stap-probe.patch (missing in Fedora glibc - BZ 752476).

* Tue Jan  3 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-2.fc17
- Fix SystemTap support regression on i686 (Sergio Durigan Junior).

* Tue Jan  3 2012 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.4.50.20120103-1.fc17
- Rebase to FSF GDB 7.4.50.20120103.

* Mon Nov 28 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-11.fc17
- No longer build bundled libstdc++ pretty printers on RHELs >= 7.

* Sat Nov 5 2011 Sergio Durigan Junior <sergiodj@redhat.com> - 7.3.50.20110722-10.fc16
- Backport fix for crash in cp_scan_for_anonymous_namespace
  (Aleksandar Ristovski, BZ 750341).

* Fri Oct 14 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-9.fc16
- Backport `info os processes' crash fix - for Eclipse (Pedro Alves, BZ 746294).

* Tue Oct 11 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-8.fc16
- Fix PIE testsuite run; new lib/future.exp hack and use -fPIC instead of -fPIE.

* Mon Sep 26 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-7.fc16
- [vla] Fix VLA arrays displayed in `bt full' (BZ 738482).
- Fix DW_OP_GNU_implicit_pointer for DWARF32 v3+ on 64-bit arches.
- Fix internal error on some optimized-out values.

* Tue Aug 16 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-6.fc16
- Python command/function auto-loading (Phil Muldoon, BZ 730976).
- Work around PR libc/13097 "linux-vdso.so.1" warning message.
- [TUI] Fix stepi on stripped code.
- Add BuildRequires: systemtap-sdt-devel for archer-sergiodj-stap-patch-split.

* Wed Aug 10 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-5.fc16
- Fix dlopen of libpthread.so, patched glibc required (Gary Benson, BZ 669432).

* Tue Aug  9 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-4.fc16
- Improve GDB performance on inferior dlopen calls (Gary Benson, BZ 698001).
- [python] Fix crash when pretty printer fails (Phil Muldoon, BZ 712715).
- Fix crash on invalid C++ mangled names (BZ 729283).

* Fri Jul 29 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-3.fc16
- Fix regression from VLA merge affecting -O0 -g watchpoints.

* Fri Jul 29 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-2.fc16
- Include gcc -g3 .debug_macro implementation by Tom Tromey.

* Sat Jul 23 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.3.50.20110722-1.fc16
- Rebase to FSF GDB 7.3.50.20110722.
- Improve gcc-4.6 stdarg false prologue end workaround (GDB PR 12435 + GCC PR 47471).

* Sun Jul  3 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.90.20110703-40.fc15
- Rebase to FSF GDB 7.2.90.20110703 (which is a 7.3 pre-release).
  - Adjust the `print errno' patch due to the DW_AT_linkage_name following again.

* Fri Jun 24 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.90.20110525-39.fc15
- Fix install-info for the gdb-doc subpackage (BZ 715228).

* Wed May 25 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.90.20110525-38.fc15
- Rebase to FSF GDB 7.2.90.20110525 (which is a 7.3 pre-release).
- [stap] Fix double free (Sergio Durigan Junior).

* Tue May  3 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.90.20110429-37.fc15
- Search also for .<seqno> files in /usr/lib/debug/.build-id (BZ 641377).

* Mon May  2 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.90.20110429-36.fc15
- Bundle readline-6.2 with a workaround of skipped "ask" (BZ 701131).
  - Use --without-system-readline, disable Requires and BuildRequires of readline.
  - Drop gdb-6.5-readline-long-line-crash.patch and gdb-readline-6.0-signal.patch.

* Fri Apr 29 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.90.20110429-35.fc15
- Rebase to FSF GDB 7.2.90.20110429 (which is a 7.3 pre-release).
- Fix -O2 -g breakpoints internal error + prologue skipping (BZ 612253).
- Fix case insensitive symbols for Fortran by iFort (BZ 645773).
- Fix physname-related CU expansion issue for C++ (PR 12708).
- Fix Python access to inlined frames (BZ 694824).

* Mon Apr 11 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.90.20110411-34.fc15
- Rebase to FSF GDB 7.2.90.20110411 (which is a 7.3 pre-release).
- Include the proper fix for anonymous struct typedefs (Tom Tromey, BZ 672230).

* Wed Mar 30 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 7.2.50.20110328-33.fc15
- Cleanup spec file to add sparc|sparcv9|sparc64.
- Add sparc specific workarounds to toolchain badness:
  - disable mmap in bdf/ via --without-mmap configure option.
  - add patch to not build mmap support on sparc for gdb/.
  - gdb code is NOT at fault, but we need a working gdb while we sort out
    the toolchain and rebuild all packages. this workaround is NOT for upstream.

* Tue Mar 29 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110328-32.fc15
- Fix occasional crash on `print errno' with no -pthread and no -g3 (BZ 690908).

* Mon Mar 28 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110328-31.fc15
- Rebase to FSF GDB 7.2.50.20110328 (which is a 7.3 pre-release).
- Bundle %%{libstdcxxpython}.tar.bz2 unconditionally - for rebulds on RHELs.

* Sun Mar 20 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110320-30.fc15
- Fix threading internal error on corrupted memory (BZ 677654).
- Fix i386 rwatch+awatch before run (BZ 688788, on top of BZ 541866).

* Sun Mar 20 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110320-29.fc15
- Rebase to FSF GDB 7.2.50.20110320 (which is a 7.3 pre-release).
- Merge archer-sergiodj-stap, the SystemTap probes breakpoints feature.
  - [stap] Fix -O2 warnings.
- Fix Ada support crash on uninitialized gdbarch.

* Sat Mar  5 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110305-28.fc15
- Rebase to FSF GDB 7.2.50.20110305 (which is a 7.3 pre-release).

* Fri Feb 25 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110222-27.fc15
- Include doc also in the PDF form; new BuildRequires: texinfo-tex.

* Wed Feb 23 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110222-26.fc15
- Rebase to FSF GDB 7.2.50.20110222 (which is a 7.3 pre-release).
- Fix attach/core-load of {,un}prelinked i386 libs (bugreport by Michal Toman).

* Mon Feb 21 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110218-25.fc15
- Drop %%{_datadir}/gdb/syscalls/* for unsupported arches.

* Fri Feb 18 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110218-24.fc15
- Rebase to FSF GDB 7.2.50.20110218 (which is a 7.3 pre-release).
- [vla] Fox Fortran vector slices for allocated arrays (for BZ 609782).

* Tue Feb 15 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110213-23.fc15
- Move the GFDL License to gdb-doc.

* Tue Feb 15 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110213-22.fc15
- Fix gdb-doc Group to be Documentation, also provide it as noarch.

* Tue Feb 15 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110213-21.fc15
- Drop non-user (gdbint) and obsolete (stabs) documentation.
- Install also HTML files besides the INFO file.
- Create new subpackage gdb-doc for both INFO and HTML files.

* Sun Feb 13 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110213-20.fc15
- Rebase to FSF GDB 7.2.50.20110213 (which is a 7.3 pre-release).
- Fix occasionall unfound source lines (affecting at least glibc debugging).
- Fix const/volatile qualifiers of C++ types (PR c++/12328).
- Be backward compatible for --rebuild with <=fc14 librpm.so.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2.50.20110206-19.fc15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb  6 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110206-18.fc15
- Fix regressions on C++ names resolving (PR 11734, PR 12273, Keith Seitz).

* Sun Feb  6 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110206-17.fc15
- Rebase to FSF GDB 7.2.50.20110206 (which is a 7.3 pre-release).

* Thu Jan 27 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110125-16.fc15
- Fix Python new-backtrace command (BZ 672235, Phil Muldoon).

* Wed Jan 26 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110125-15.fc15
- Temporary fix of F15 gcc-4.6 child DIEs of DW_TAG_typedef (BZ 672230).
- Workaround gcc-4.6 stdarg false prologue end (GDB PR 12435 + GCC PR 47471).

* Tue Jan 25 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110125-14.fc15
- Rebase to FSF GDB 7.2.50.20110125 (which is a 7.3 pre-release).
- Fix discontiguous address ranges in .gdb_index - v3->v4 (BZ 672281).
- Fix DWARF-3+ DW_AT_accessibility default assumption for F15 gcc-4.6.

* Thu Jan 20 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110117-13.fc15
- Use librpm.so.2 for rpm-4.9.0 in Fedora 15.

* Mon Jan 17 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110117-12.fc15
- Use %%{?dist} for sanity checking tools compliance (suggested by Petr Muller).

* Mon Jan 17 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110117-11.fc15
- Rebase to FSF GDB 7.2.50.20110117 (which is a 7.3 pre-release).
- Fix callback-mode readline-6.0 regression for CTRL-C (for RHEL-6.0).
  - Fix occasional NULL dereference of the readline-6.0 workaround (BZ 575516).

* Sat Jan 15 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110107-10.fc15
- [delayed-symfile] Test a backtrace regression on CFIs without DIE (BZ 614604).
- [archer-tromey-delayed-symfile] New test gdb.dwarf2/dw2-aranges.exp.
- [archer-keiths-expr-cumulative+upstream] Import C++ testcases.
  - testsuite: Fix gdb-test-expr-cumulative-archer.patch compatibility.

* Fri Jan  7 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110107-9.fc15
- Remove --with-pythondir as no longer valid.
- Provide %%{_bindir}gdb-add-index even on RHEL-5.
- Provide again libstdc++ pretty printers for any RHEL.

* Fri Jan  7 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110107-8.fc15
- Rebase to FSF GDB 7.2.50.20110107 (which is a 7.3 pre-release).
- Import archer-tromey-python (BZ 666177, branch update by Phil Muldoon).

* Tue Jan  4 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20110104-7.fc15
- Rebase to FSF GDB 7.2.50.20110104 (which is a 7.3 pre-release).
- New testcase py-prettyprint.exp:print hint_error (for BZ 611569, BZ 629236).
- New test gdb.arch/x86_64-pid0-core.exp for kernel PID 0 cores (BZ 611435).

* Sat Jan  1 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20101231-6.fc15
- Fix --with-system-readline doc build upstream regression.

* Sat Jan  1 2011 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20101231-5.fc15
- Rebase to FSF GDB 7.2.50.20101231 (which is a 7.3 pre-release).
- Remove gdb-6.3-bt-past-zero-20051201.patch, gdb-archer-ada.patch and
  gdb-6.3-framepczero-20040927.patch already removed from .spec before.
- Remove gdb-6.5-dwarf-stack-overflow.patch, upstreamed (Tom Tromey).
- Remove gdb-6.6-bz225783-gdb-debuginfo-paths.patch, upstreamed (Tom Tromey).
- Remove gdb-6.6-readline-system.patch, reimplemented upstream (Tom Tromey).
- Remove gdb-bz642879-elfread-sigint-stale.patch, upstreamed (Jan Kratochvil).
- Remove gdb-next-over-throw.patch, upstreamed (Tom Tromey).

* Mon Dec 27 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20101117-4.fc15
- Provide stub %%{_sysconfdir}/gdbinit (BZ 651232).

* Mon Dec 27 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20101117-3.fc15
- Fix ppc* compilation of PRPSINFO in the core files (BZ 662995, for BZ 254229).
- Fix (disable) non-x86* compilation of libinproctrace.so (for BZ 662995).

* Thu Nov 18 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20101117-2.fc15
- Drop gdb-6.8-glibc-headers-compat.patch: GNU/Linux irrelevant (Tom Tromey).
- Drop gdb-6.3-terminal-fix-20050214.patch: The bug is not reproducible.
- Drop gdb-6.7-kernel-headers-compat.patch: kernel-headers seem to be fixed.
- Drop gdb-archer-ada.patch: No longer needed for Ada (Keith Seitz).
- New PR backtrace/12237, drop gdb-6.3-framepczero-20040927.patch
  gdb-6.3-bt-past-zero-20051201.patch as they already had no effect.
- Drop gdb-6.8-gcc35998-ada-memory-trash.patch as a different fix is upstream.
- Drop gdb-6.3-inheritance-20050324.patch: the call is redundent (Tom Tromey).
- Drop gdb-6.3-large-core-20051206.patch: obsoleted by MAX_COPY_BYTES.

* Thu Nov 18 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2.50.20101117-1.fc15
- Rebase to FSF GDB 7.2.50.20101117 (which is a 7.3 pre-release).

* Sun Nov  7 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-25.fc14
- iFort compat. - case insensitive DWARF not in lowercase (BZ 645773).

* Thu Oct 14 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-24.fc14
- Add gdb.spec comments on the *.patch files upstream merge status.

* Thu Oct 14 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-23.fc14
- Workaround librpm BZ 643031 due to its unexpected exit() calls (BZ 642879).
- Fix crash on CTRL-C while reading an ELF symbol file (BZ 642879).

* Tue Oct 12 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-22.fc14
- testsuite: Provide missing lib/gdb-python.exp (for BZ 639089).

* Tue Oct 12 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-21.fc14
- Fix python stale error state, also fix its save/restore (BZ 639089).
- Fix inferior exec of new PIE x86_64 (BZ 638979).

* Tue Oct 12 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-20.fc14
- Fixup Release for 20.fc14.

* Tue Oct 12 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-19.fc14
- Use .gdb_index v3 to fix excessive resources rqmnts (BZ 640634, Tom Tromey).

* Wed Oct  6 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-18.fc14
- Fix false warning: non-absolute filename: <the main exec. file> (BZ 640648).

* Thu Sep 30 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-17.fc14
- New Conflicts: elfutils < 0.149 due to the .gdb_index .debug support.

* Wed Sep 29 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-16.fc14
- [ifunc] Fix crash on deleting watchpoint of an autovariable (BZ 637770).

* Mon Sep 27 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-15.fc14
- Revert the -O0 switch formerly to workaround GCC BZ 634757 (cmove bug).
- Remove no longer used BuildRequires: libstdc++.
- Remove commented out python libstdc++ .spec code.

* Sat Sep 25 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-14.fc14
- Fixup %%{_datadir}/gdb/python/gdb timestamps for multilib conflicts.

* Sat Sep 25 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-13.fc14
- Fix .gdb_index for big-endian hosts (Tom Tromey).

* Sat Sep 25 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-12.fc14
- Fix lost siginfo_t in linux-nat (BZ 592031).

* Sat Sep 25 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-11.fc14
- Fix infinite loop crash on self-referencing class (BZ 627432).

* Thu Sep 23 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-10.fc14
- gcore/-Wl,-z,relro: Always write out all the pages until kernel gets a fix.

* Wed Sep 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-9.fc14
- Fix gcore writer for -Wl,-z,relro (PR corefiles/11804).

* Wed Sep 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-8.fc14
- Enable python by default even in Brew and on all the arches (BZ 609157).

* Wed Sep 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-7.fc14
- python: load *-gdb.py for shlibs during attach (BZ 634660).
- Fix double free crash during overload resolution (PR 12028, Sami Wagiaalla).

* Sat Sep 18 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-6.fc14
- Fix python gdb.solib_address (BZ 634108, fix by Phil Muldoon).
- Temporarily build with -O0 to workaround GCC BZ 634757 (cmove bug).

* Tue Sep 14 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-5.fc14
- Fix Ada regression when any .gdb_index library is present.

* Sat Sep 11 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-4.fc14
- Fix symbol lookup misses methods of current class (BZ 631158, Sami Wagiaalla).
- Fix python gdb.execute-to_string redirection (BZ 627506, with Paul Bolle).

* Wed Sep  8 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-3.fc14
- Do not crash on broken separate debuginfo due to old elfutils (BZ 631575).

* Sat Sep 04 2010 Dennis Gilmore <dennis@ausil.us> - 7.2-2.fc14
- libinproctrace doesnt exist on sparc arches

* Fri Sep  3 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.2-1.fc14
- Formal update to the final FSF GDB release.

* Tue Aug 24 2010 Dan Horák <dan[at]danny.cz> - 7.1.90.20100806-12.fc14
- libinproctrace doesn't exist on s390(x)

* Thu Aug 19 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100806-11.fc14
- Fix crash on MI variable calling inferior function (BZ 610986).

* Tue Aug 10 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100806-10.fc14
- Fix /usr/bin/gdb-add-index missing -nx for gdb.
- New option --with profile (disabled by default - missing workload, BZ 615603).

* Sat Aug  7 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100806-9.fc14
- Fix python gdb.execute to_string pagination (BZ 620930).

* Fri Aug  6 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100806-8.fc14
- Out of memory is just an error, not fatal (uninitialized VLS vars, BZ 568248).

* Fri Aug  6 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100806-7.fc14
- Fix gcore from very small terminal windows (BZ 555076).
- Fix false `filesystem' debuginfo rpm request (BZ 599598).

* Wed Jul 28 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 7.1.90.20100721-6.fc14
- Rebuild against python 2.7

* Thu Jul 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100721-5.fc14
- Fix /usr/bin/gdb-add-index $d -> $dir typo.

* Thu Jul 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100721-4.fc14
- Import archer-tromey-python.
- Import archer-tromey-optional-psymtab (as present in FSF GDB post-7.2).
  - Provide /usr/bin/gdb-add-index for rpm-build (Tom Tromey).

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 7.1.90.20100721-3.fc14
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 21 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100721-2.fc14
- Fix prelinked executables with sepdebug and copy relocations (BZ 614659).

* Wed Jul 21 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1.90.20100721-1.fc14
- Rebase to FSF GDB 7.1.90.20100721 (which is 7.2 pre-release).

* Tue Jul 13 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-29.fc14
- Disable temporarily Python files before the new rebase is done (BZ 613710).

* Sun Jul 11 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-28.fc14
- Rebuild for Fedora 14.

* Wed Jun 30 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-28.fc13
- Print 2D C++ vectors as matrices (BZ 562763, sourceware10659, Chris Moller).

* Wed Jun 30 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-27.fc13
- Fix obstack corruptions on C++ (BZ 606185, Chris Moller, Jan Kratochvil).
- Improve support for typedefs in classes (BZ 602314).
- Fix `set print object on' for some non-dynamic classes (BZ 606660).

* Wed Jun  9 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-26.fc13
- Backport DWARF-4 support (BZ 601887, Tom Tromey).

* Wed Jun  9 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-25.fc13
- Fix ADL anonymous type crash (BZ 600746, Sami Wagiaalla).

* Tue Jun  1 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-24.fc13
- Fix crash on /proc/PID/stat race during inferior exit (BZ 596751).
- testsuite: gdb.threads/watchthreads-reorder.exp kernel-2.6.33 compat. fix.

* Sun May 30 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-23.fc13
- Fix and support DW_OP_*piece (Tom Tromey, BZ 589467).
- Fix follow-exec for C++ programs (bugreported by Martin Stransky).

* Mon May 24 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-22.fc13
- Remove core file when starting a process (BZ 594560).
- Fix lock up on loops in the solib chain (BZ 593926).
- Import fix of TUI layout internal error (BZ 595475).

* Sun May 16 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-21.fc13
- Make gdb-6.8-bz254229-gcore-prpsinfo.patch RHEL-5 /usr/bin/patch compatible
  (bugreported by Jonas Maebe).

* Thu May 13 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-20.fc13
- Fix crash on VLA bound referencing an optimized-out variable (BZ 591879).
- Re-enable the BZ 575292 and BZ 585445 C++ fix using an updated patch.

* Wed May 12 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-19.fc13
- Backport <tab>-completion bug on anonymous structure fields (BZ 590648).
- testsuite: Fix gdb.base/vla-overflow.exp FAILing on s390x (BZ 590635).
- Workaround non-stop moribund locations exploited by kernel utrace (BZ 590623).

* Thu Apr 29 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-18.fc13
- Make _Unwind_DebugHook independent from step-resume breakpoint (Tom Tromey).

* Tue Apr 27 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-17.fc13
- Fail gracefully if the _Unwind_DebugHook arg. is optimized out (Tom Tromey).

* Tue Apr 27 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-16.fc13
- Temporarily workaround the crash of BZ 575292 as there was now BZ 585445.

* Mon Apr 26 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-15.fc13
- Fix crash when using GNU IFUNC call from breakpoint condition.
- Avoid internal error by disabling the previous BZ 575292 fix (BZ 585445).

* Thu Apr 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-14.fc13
- Fix crash on C++ types in some debug info files (BZ 575292, Keith Seitz).
- Pretty printers not well documented (BZ 570635, Tom Tromey, Jan Kratochvil).

* Fri Apr 16 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-13.fc13
- archer-jankratochvil-fedora13 commit: 39998c496988faaa1509cc6ab76b5c4777659bf4
- [vla] Fix boundaries for arrays on -O2 -g (support bound-ref->var->loclist).
- [vla] Fix copy_type_recursive for unavailable variables (Joost van der Sluis).

* Sun Apr 11 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-12.fc13
- Fix crash on trying to load invalid executable (BZ 581215).

* Thu Apr  8 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-11.fc13
- testsuite: Fix gdb.base/gstack.exp also for ppc64 inferiors (for BZ 579793).

* Thu Apr  8 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-10.fc13
- Fix s390 --with testsuite Buildrequiers to be (s390-32) (BZ 580347, Cai Qian).

* Wed Apr  7 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-9.fc13
- Fix gstack to print even the frame #0.  New gdb.base/gstack.exp.  (BZ 579793)
- Merge gdb-6.3-gstack-without-path-20060414.p* into gdb-6.3-gstack-20050411.p*,
  no real code change.

* Mon Apr  5 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-8.fc13
- Fix breakpoint at *_start (BZ 162775, bugreport by John Reiser).

* Sat Apr  3 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-7.fc13
- Fix ppc build of the AVX registers support (for BZ 578250).

* Sat Apr  3 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-6.fc13
- Support AVX registers (BZ 578250).

* Sat Apr  3 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-5.fc13
- Fix dangling displays in separate debuginfo (BZ 574483).

* Wed Mar 31 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-4.fc13
- Remove gdb-readline-6.0-signal.patch with a bug causing crash while no longer
  required with F-13 readline-6.1 (BZ 575516)

* Mon Mar 29 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-3.fc13
- [expr-cumulative] using-directive: Fix memory leak (Sami Wagiaalla).

* Mon Mar 29 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-2.fc13
- Drop obsoleted `gdb-archer-pie-0315-breakpoint_address_match.patch'.
- Do not consider memory error on reading _r_debug->r_map as fatal (BZ 576742).
  - PIE: Attach binary even after re-prelinked underneath.
  - PIE: Attach binary even after ld.so re-prelinked underneath.
  - PIE: Fix occasional error attaching i686 binary (BZ 576742).
- testsuite: Fix unstable results of gdb.base/prelink.exp.

* Thu Mar 25 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.1-1.fc13
- Update to new FSF GDB release.

* Mon Mar 15 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.90.20100312-24.fc13
- Drop gdb-6.5-bz218379-ppc-solib-trampoline-fix.patch having false symbols
  resolving (related to BZ 573277).

* Fri Mar 12 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.90.20100312-23.fc13
- Update to new FSF GDB snapshot.
- Fix double-free on std::terminate handler (Tom Tromey, BZ 562975).

* Wed Mar 10 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.90.20100306-22.fc13
- Another License update.

* Wed Mar 10 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.90.20100306-21.fc13
- Update License for all the licenses contained in .src.rpm.

* Mon Mar  8 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.90.20100306-20.fc13
- Remove unapplied: gdb-6.8-inlining-addon.patch gdb-6.8-inlining-by-name.patch

* Mon Mar  8 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.90.20100306-19.fc13
- Include also %%doc COPYING3 (review by Petr Machata).
- Remove URL for Source (review by Matej Cepl).

* Sun Mar  7 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.90.20100306-18.fc13
- archer-jankratochvil-fedora13 commit: 59c35a31f0981a0f0b884b32c91ae6325b2126cd

* Sun Feb 28 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100203-17.fc13
- Fix false warning: section .gnu.liblist not found in ...
- Fix crash on stale addrinfo->sectindex (more sensitive due to the PIE patch).

* Fri Feb 26 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100203-16.fc13
- Fix ia64 part of the bt-clone-stop.exp fix.
- Fix gdb.ada/* regressions (Keith Seitz).
- Remove false gdb_assert on $sp underflow.

* Mon Feb  8 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100203-15.fc13
- Fix i386+x86_64 rwatch+awatch before run, regression against 6.8 (BZ 541866).

* Wed Feb  3 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100203-14.fc13
- Rediff gdb-6.8-bz254229-gcore-prpsinfo.patch for older patch(1) compatibility.

* Wed Feb  3 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100203-13.fc13
- archer-jankratochvil-fedora13 commit: 59c35a31f0981a0f0b884b32c91ae6325b2126cd
- Fortran: Fix regression on setting breakpoint at toplevel symbols (BZ 559291;
  David Moore, Intel).

* Mon Feb  1 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100128-12.fc13
- archer-jankratochvil-fedora13 commit: 5a573e8b26a2f0a6947d4c0249e43e5456610860
- Remove ExcludeArch on ia64 as it is now fixed up.

* Sun Jan 31 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100128-11.fc13
- Fix failed gdb_assert due to the PIE patchset (BZ 559414).

* Thu Jan 28 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100128-10.fc13
- Upgrade to the FSF GDB snapshot: 7.0.50.20100128
- archer-jankratochvil-fedora13 commit: 39c5a8b75fad3acd7204903db5dee025055a4594
  - Fix a regression on "AAA::ALPHA" test due to a merge from FSF GDB.
- Fix a regression of previous release due to false identification as core file.
- Move ifunc .patch into the GIT-managed archer-jankratochvil-fedora13 branch.
- Update gdb.pie/corefile.exp from 2007-01-26 FSF GDB commit by Andreas Schwab.

* Mon Jan 25 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-9.fc13
- Enable loading a core file just as a single argument to /usr/bin/gdb.

* Sun Jan 24 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-8.fc13
- testsuite: Fix gdb.arch/i386-bp_permanent.exp regression

* Sun Jan 24 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-7.fc13
- Update gdb.arch/powerpc-power7.exp for current binutils HEAD.

* Fri Jan 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-6.fc13
- Disable addon (finish) due to inline-cmds.exp: up from outer_inline2 assert.
- Fix gdb.arch/powerpc-power7.exp compatibility.

* Fri Jan 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-5.fc13
- Disable break-by-name on inlined functions due to a regression on parameters
  of inlined functions falsely <optimized out> (BZ 556975 Comment 8).

* Fri Jan 22 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-4.fc13
- Adjust BuildRequires for RHELs, add ExcludeArch on ia64.
- Disable one PIE-introduced assertion on RHELs.

* Thu Jan 21 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-3.fc13
- Revert FSF GDB gdbserver tracepoints as incomplete now.

* Thu Jan 21 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-2.fc13
- archer-jankratochvil-fedora13 commit: 21e418c04290aa5d2e75543d31fe3fe5d70d6d41
- [expr-cumulative] Fix "break expr if (cond)" regression.

* Thu Jan 21 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100121-1.fc13
- Upgrade to the FSF GDB snapshot: 7.0.50.20100121
- archer-jankratochvil-fedora13 commit: ccde1530479cc966374351038057b9dda90aa251
- [expr-cumulative] Archer branch is now included.

* Tue Jan 19 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100118-2.fc13
- Fix false PASS->FAIL of gdb.arch/i386-biarch-core.exp.

* Tue Jan 19 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100118-1.fc13
- Upgrade to the FSF GDB snapshot: 7.0.50.20100118
- Upgrade libstdc++-v3-python to r155978 (Phil Muldoon).

* Sat Jan 16 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.50.20100116-1.fc13
- Upgrade to the FSF GDB snapshot: 7.0.50.20100116
- archer-jankratochvil-fedora13 commit: 81810a20b2d2c3bf18e151de3cddfc96445b3c46
- [expr-cumulative] Archer branch is missing in this release.
- Update rpm.org#76 workaround for rpm-4.8 using librpm.so.1.
- Dissect archer-jankratochvil-misc into Patch403...Patch408.
- Some regressions exist in this release.

* Tue Jan 12 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-25.fc12
- non-librpm missing debuginfo yumcommand now prints also --disablerepo='*'
  to save some bandwidth by yum (Robin Green, BZ 554152).

* Sun Jan 10 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-24.fc12
- testsuite: BuildRequires also valgrind.

* Fri Jan  8 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-23.fc12
- Workaround missing libstdc++%%{bits_other} in Koji.

* Fri Jan  8 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-22.fc12
- Comply with new package review:
  - Fix .spec Source as this is not a snapshot now.
  - Convert all spaces to tabs.
  - Fix missing %%defattr at %%files for gdbserver.
  - Replace all hardcoded-library-path by variants of %%{_isa}.
- Include %%{_isa} for appropriate Requires and BuildRequires.

* Thu Jan  7 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-21.fc12
- [vla] Fix regression on fields of structs in internal vars (BZ 553338).
- archer-jankratochvil-fedora12 commit: 6e73988f653ba986e8742f208f17ec084292cbd5

* Thu Jan  7 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-20.fc12
- Fix crash reading broken stabs (it377671).

* Sun Jan  3 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-19.fc12
- testsuite: Fixup false FAILs for gdb.cp/constructortest.exp.

* Sat Jan  2 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-18.fc12
- Fix regression of gdb-7.0 (from 6.8) crashing on typedefed bitfields.
- Fix related_breakpoint stale ref crash.

* Fri Jan  1 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0.1-17.fc12
- Formal upgrade to the FSF GDB release gdb-7.0.1.
  - Fix regression of gdb-7.0.1 not preserving typedef of a field.

* Fri Jan  1 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-16.fc12
- More RHEL-5 compatibility updates.
  - Disable the build-id support by default.
  - Bundle back gdbserver to the base gdb package.
  - Remove bundled pstack.
  - Drop the BuildRequires of rpm-devel.

* Fri Jan  1 2010 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-15.fc12
- Fix error on a sw watchpoint active at function epilogue (hit on s390x).
- testsuite: Fix false MI "unknown output after running" regression.
- testsuite: Update ia64-sigtramp.exp for recent GDB.
- Implement bt-clone-stop.exp fix also for ia64.
- testsuite: Upstream condbreak.exp results stability fix (Daniel Jacobowitz).

* Thu Dec 24 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-14.fc12
- testsuite: Fix constructortest.exp and expand-sals.exp for gcc-4.4.2-20.fc12.

* Mon Dec 21 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-13.fc12
- [pie] Fix a race in testcase gdb.base/valgrind-db-attach.exp.
- Fix regression by python on ia64 due to stale current frame.
- Disable python iff RHEL-5 && (Brew || ppc64).

* Mon Dec 21 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-12.fc12
- Workaround build on native ppc64 host.
- More RHEL-5 compatibility updates.
  - Disable warning messages new for gdb-6.8+ for RHEL-5 backward compatibility.
  - Workaround RHEL-5 kernels for detaching SIGSTOPped processes (BZ 498595).
  - Serialize the testsuite output to keep the order for regression checks.
  - Re-enable python for all non-ppc* arches.
  - More gcc44 stack exceptions when running the testsuite on RHEL-5.
- Fix backward compatibility with G++ 4.1 namespaces "::".
- Fix regression on re-setting the single ppc watchpoint slot.
- Update snapshot of FSF gdb-7.0.x branch.
  - Backport fix of dcache invalidation locking up GDB on ppc64 targets.

* Fri Dec 18 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-11.fc12
- [pie] Fix general ppc64 regression due to a function descriptors bug.
- [pie] Fix also keeping breakpoints disabled in PIE mode.
- Import upstream <tab>-completion crash fix.
- Drop some unused patches from the repository.
- More RHEL-5 build compatibility updates.
  - Use gfortran44 when running the testsuite on RHEL-5.
  - Disable python there due to insufficient ppc multilib.
- Fix orphanripper hangs and thus enable it again.

* Mon Dec 14 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-10.fc12
- Make gdb-6.3-rh-testversion-20041202.patch to accept both RHEL and Fedora GDB.
- Adjust BuildRequires for Fedora-12, RHEL-6 and RHEL-5 builds.
- [vla] Fix compatibility of dynamic arrays with iFort (BZ 514287).
- Fix stepping through OMP parallel Fortran sections (BZ 533176).
- New fix of bp conditionals [bp_location-accel] regression (BZ 538626).

* Mon Dec  7 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-9.fc12
- Replace the PIE (Position Indepdent Executable) support patch by a new one.
- Drop gdb-6.3-nonthreaded-wp-20050117.patch as fuzzy + redundant.
- Fix callback-mode readline-6.0 regression for CTRL-C.
- Fix syscall restarts for amd64->i386 biarch.
- Various testsuite results stability fixes.
- Fix crash on reading stabs on 64bit (BZ 537837).
- archer-jankratochvil-fedora12 commit: 16276c1aad1366b92e687c72cab30192280e1906
- archer-jankratochvil-pie-fedora12 ct: 2ae60b5156d43aabfe5757940eaf7b4370fb05d2

* Thu Dec  3 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-8.fc12
- Fix slowness/hang when printing some variables (Sami Wagiaalla, BZ 541093).
- archer-jankratochvil-fedora12 commit: 6817a81cd411acc9579f04dcc105e9bce72859ff

* Wed Nov 25 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-7.fc12
- Support GNU IFUNCs - indirect functions (BZ 539590).
- Fix bp conditionals [bp_location-accel] regression (Phil Muldoon, BZ 538626).
- Fix missed breakpoint location [bp_location-accel] regression (upstream).

* Fri Oct 30 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-6
- Fix missing zlib-devel BuildRequires to support compressed DWARF sections.
- Include post-7.0 FSF GDB fixes.

* Fri Oct 23 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-5
- Make the package buildable on RHEL-5/CentOS-5 (without librpm there).
- archer-jankratochvil-fedora12 commit: 5b73ea6a0f74e63db3b504792fc1d37f548bdf5c

* Fri Oct 23 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-4
- Fix rpm --excludedocs (BZ 515998).

* Thu Oct 22 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-3
- Support multiple directories for `set debug-file-directory' (BZ 528668).

* Mon Oct 19 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-2
- Sync the .spec with RHEL/CentOS without EPEL, do not BuildRequires: fpc there.

* Wed Oct  7 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 7.0-1
- Formal upgrade to the final FSF GDB release gdb-7.0.
- Fix GNU/Linux core open: Can't read pathname for load map: Input/output error.
- archer-jankratochvil-fedora12 commit: ce4ead356654b951a49ca78d81ebfff95e758bf5

* Wed Sep 30 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.91.20090930-2
- Bump release.

* Wed Sep 30 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.91.20090930-1
- Fix broken python "help()" command "modules" (BZ 526552).
- Upgrade to the FSF GDB gdb-7.0 snapshot: 6.8.91.20090930
- archer-jankratochvil-fedora12 commit: 7cb860f03e2437c97239334ebe240d06f45723e0

* Sun Sep 27 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.91.20090925-3
- New test for step-resume breakpoint placed in multiple threads at once.

* Fri Sep 25 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.91.20090925-2
- Fix buildid-loading libs w/matching name but different build-id (BZ 524572).

* Fri Sep 25 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.91.20090925-1
- Upgrade to the FSF GDB gdb-7.0 snapshot: 6.8.91.20090925
- archer-jankratochvil-fedora12 commit: 4338ea85c798007c32594032f602db9fd230eba9
  - [python] Don't directly reference self.frame (Tom Tromey).
  - [expr] Updates from branch (Keith Seitz).

* Mon Sep 21 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.91.20090921-1
- Upgrade to the FSF GDB gdb-7.0 snapshot: 6.8.91.20090921
- archer-jankratochvil-fedora12 commit: 0d5c38dd89050c0ee1cf049656f177c170d675d4
  - [expr] Check has_stack_frames before calling find_pc_line (Sami Wagiaalla).

* Thu Sep 17 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.91.20090917-2
- Include bundled libstdc++ python; it will be in libstdc++-devel since gcc-4.5.

* Thu Sep 17 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.91.20090917-1
- Upgrade to the FSF GDB gdb-7.0 branch and snapshot: 6.8.91.20090917
- archer-jankratochvil-fedora12 commit: 16f3f01cc2cbc15283462eaabdfcde92cf42cdc6
- Drop the qsort_cmp workaround as resolved in FSF GDB now (BZ 515434).

* Thu Sep 10 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090910-1
- Upgrade to the FSF GDB gdb-6.8.50 snapshot: 6.8.50.20090910
- archer-jankratochvil-fedora12 commit: 941eb487a42933e442cb4d11344cda96ecb8a04d
  - [next-over-throw] Fix exceptions thrown during next (Tom Tromey).
  - [bp_location-accel] Do not (much) slow down on 500+ breakpoints (me).

* Thu Sep  3 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090818-8
- archer-jankratochvil-fedora12 commit: a081d2f12945e9468edd5f4341d3e945bd0fefe9
  - [expr] Fix too slow lookups in large C++ programs (Sami Wagiaalla).
  - [python] Fix varobj changed values reporting (GDB PR 10584, Tom Tromey).

* Tue Sep  1 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090818-7
- archer-jankratochvil-fedora12 commit: d25596676e8811b03f8c9aba6bbd04ebaa9ff5db
  - [call-frame-cfa] Fix parsing CFA-relative frames (BZ 516627, Tom Tromey).
  - [vla] variable length Fortran strings for -O -g code (part of BZ 508406, me).
  - [python] varobj + general fixes (Tom Tromey).

* Fri Aug 28 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090818-6
- Real upstream fixup of qsort_cmp (BZ 515434).
- Revert bitfields regression (BZ 520129).

* Tue Aug 25 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090818-5
- Temporarily disable assertion checks crashing in qsort_cmp (BZ 515434).

* Wed Aug 19 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090818-4
- Fixup "bad type" internal error, import from FSF GDB.
- archer-jankratochvil-fedora12 commit: 2ba2bc451eb832182ef84c3934115de7a329da7c

* Tue Aug 18 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090818-3
- archer-jankratochvil-fedora12 commit: 850e3cb38a25cb7fdfa4cef667626ffbde51bcac
- Fix the hardware watchpoints.

* Tue Aug 18 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090818-2
- Fix patch fuzz 0.

* Tue Aug 18 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090818-1
- Upgrade to the FSF GDB gdb-6.8.50 snapshot: 6.8.50.20090818
- archer-jankratochvil-fedora12 commit: 5e0d1cc74f119391a2c3ae25ef5749fc28674f06

* Wed Aug 12 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090811-4
- Fix minor regressions introduced by the rebase from F-11 (6.8.50.20090302).

* Tue Aug 11 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090811-3
- archer-jankratochvil-fedora12 commit: 2888fafe63889757c6fd27ccc2f25661d43fd1a4
- Drop archer-jankratochvil-vla VAROBJ invalidate/revalidate split to fix
  regressions against FSF GDB HEAD.

* Tue Aug 11 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090811-2
- archer-jankratochvil-fedora12 commit: 93f5e942bdcdcc376ece452c309bedabae71def9
- Fix "can't compute CFA for this frame" (by Tom Tromey, BZ 516627).

* Tue Aug 11 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090811-1
- Support constant DW_AT_data_member_location by GCC PR debug/40659 (BZ 515377).
- Fix .spec URL.
- archer-jankratochvil-fedora12 commit: 81de3c6abae4f7e3738aa9bcc0ab2f8725cce252

* Mon Aug 10 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090810-2
- Upgrade to the FSF GDB gdb-6.8.50 snapshot: 6.8.50.20090810
- archer-jankratochvil-fedora12 commit: 93ec16e6f5000dd64d433d86674e820ed0f35b72

* Tue Aug  4 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090803-2
- Drop the bundled libstdc++ python - it should be packaged on its own now.

* Tue Aug  4 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090803-1
- Upgrade to the FSF GDB gdb-6.8.50 snapshot: 6.8.50.20090803
- archer-jankratochvil-fedora12 commit: 0222cb1f4ddd1eda32965e464cb60b1e44e110b2

* Fri Jul 31 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-42
- Release bump only.

* Fri Jul 31 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-41
- Fix compatibility of --with-system-readline and readline-6.0+.
- Temporarily disabled orphanripper on Fedora 12.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.50.20090302-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-39
- testsuite: Fix multiple runs in parallel on a single host.
- testsuite: Remove the rpmbuild option: --with parallel
- testsuite: Run the testsuite with default rpm _smp_mflags.

* Mon Jul  6 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-38
- Archer update to the snapshot: 17bfc0488f54aeeb7a9e20ef3caa7e31e8e985fb
- Archer backport: de9c5190034b84b0a5fb4b98b05b304cda187700
  - [vla] Fix a crash regression on constant DW_AT_data_member_location.

* Mon Jun 29 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-37
- Replace the fix of cloned-TIDs with no pthread from upstream (BZ 471819).
- Fix a parallel testsuite runs incompatibility in gdb.base/gcore-shmid0.exp.

* Mon Jun 29 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-36
- Fix GDB crash on cloned-TIDs with no associated pthread (BZ 471819).
- Workaround rpm.org#76 rpm-devel requirement for debuginfo names (BZ 508193).

* Mon Jun 22 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-35
- Accelerate sorting blocks on reading a file (found on WebKit) (BZ 507267).

* Mon Jun 22 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-34
- Fix backtraces from core files with the executable found+loaded via build-id.
  - Due to F-11 GCC no longer needlessly duplicating .eh_frame as .debug_frame.

* Tue Jun 16 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-33
- Archer update to the snapshot: 05c402a02716177c4ddd272a6e312cbd2908ed68
- Archer backport: 05c402a02716177c4ddd272a6e312cbd2908ed68
  - Remove the [archer-pmuldoon-exception-rewind-master] branch.
  - Include this functionality as a FSF GDB accepted patchset.

* Mon Jun 15 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-32
- Fix crash on pending breakpoints with PIE (position-indep.-exec.) (BZ 505943).

* Fri Jun 12 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-31
- Fix an occasional crash during printing of missing debuginfo rpms (BZ 505401).

* Fri Jun 12 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-30
- Implement DW_OP_call_frame_cfa (for recent GCC).

* Thu Jun 11 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-29
- Archer update to the snapshot: 30c13da4efe18f43ee34aa4b29bc86e1a53de548
- Archer backport: 30c13da4efe18f43ee34aa4b29bc86e1a53de548
  - Fix dereferencing unbound C arrays (BZ 505163).

* Wed Jun 10 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-28
- Archer update to the snapshot: 000db8b7bfef8581ef099ccca8689cfddfea1be8
- Archer backport: b8d3bea36b137effc929e02c4dadf73716cb330b
  - Ignore explicit die representing global scope '::' (gcc 4.1 bug).
- Archer backport: c2d5c4a39b10994d86d8f2f90dfed769e8f216f3
  - Fix parsing DW_AT_const_value using DW_FORM_string
- Archer backport: 8d9ab68fc0955c9de6320bec2821a21e3244600d
                 + db41e11ae0a3aec7120ad6ce86450d838af74dd6
  - Fix Fortran modules/namespaces parsing (but no change was visible in F11).
- Archer backport: 000db8b7bfef8581ef099ccca8689cfddfea1be8
  - Fix "some Python error when displaying some C++ objects" (BZ 504356).
- testsuite: Support new rpmbuild option: --with parallel
- testsuite: gdb-orphanripper.c: Fix uninitialized `termios.c_line'.
- Fix crashes due to (missing) varobj revalidation, for VLA (for BZ 377541).
- Archer backport: 58dcda94ac5d6398f47382505e9d3d9d866d79bf
                 + f3de7bbd655337fe6705aeaafcc970deff3dd5d5
  - Implement Fortran modules namespaces (BZ 466118).
- Fix crash in the charset support.

* Thu Apr 30 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-27
- Fix race in the ia64 testcase `gdb-6.3-rh-testlibunwind-20041202.patch'.

* Mon Apr 27 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-26
- Support a new rpmbuild option: --without python

* Mon Apr 27 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-25
- The Koji build failures may have been by forgotten check-in of the Patch360.

* Mon Apr 27 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-24
- Another new Koji build fix attempt now by: BuildPreReq: python

* Mon Apr 27 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-23
- Fix BuildRequires for new Koji.

* Mon Apr 27 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-22
- Fix pstack/gstack cutting very long lines (BZ 497849).

* Sun Apr 19 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-21
- New test for parsing elf64-i386 files for kdump PAE vmcore dumps (BZ 457187).

* Thu Apr 16 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-20
- Fix crash in the charset support.

* Wed Apr 15 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-19
- Fix crash on pretty-printer reading uninitialized std::string (BZ 495781).

* Mon Apr 13 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-18
- Archer update to the snapshot: d1fee5066408a09423621d1ebc64e6d3e248ed08
- Archer backport: 4854339f75bdaf4b228fc35579bddbb2a1fecdc1
  - Fix Python FrameIterator.

* Mon Apr 13 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-17
- Archer update to the snapshot: 7c250ce99c90cf6097e2ec55ea0f205830979cee
- Archer backport: c14d9ab7eef43281b2052c885f89d2db96fb5f8e
  - Revert a change regressing: gdb.objc/basicclass.exp
- Archer backport: ebd649b96e61a1fb481801b65d827bca998c6633
                 + 1f080e897996d60ab7fde20423e2947512115667
                 + 1948198702b51b31d79793fc49434b529b4e245f
                 + e107fb9687bb1e7f74170aa3d19c4a8f6edbb10f
                 + 1e012c996e121cb35053d239a46bd5dc65b0ce60
  - Update the Python API from upstream.
- Archer backport: d3c83ad5ec9f7672b87af9ad29279f459e53da11
  - Fix a Python branch crash.

* Mon Apr 13 2009 Dennis Gilmore <dennis@ausil.us> - 6.8.50.20090302-16
- enable gdbserver package on sparc64

* Sun Apr  5 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-15
- Archer update to the snapshot: 7c7c77576669d17ad5072daa47ea3a4fd954483d
- Archer backport: 7c7c77576669d17ad5072daa47ea3a4fd954483d (Peter Bergner)
  - Disassemble Power7 instructions right in the default/only -Many GDB mode.

* Sun Apr  5 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-14
- Archer update to the snapshot: f6273d446ff87e50976600ba3f71b88d61043e20
- Archer backport: f6273d446ff87e50976600ba3f71b88d61043e20
  - Use pretty-printers to print base classes inside a derived class.

* Mon Mar 30 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-13
- Archer update to the snapshot: d144a3633454046aaeae3e2c369c271834431d36
- Archer backport: a2c49b7640ebe7ce1376902d48d5bbbee600996b
  - Fixup compilation older GCCs.
- Archer backport: fe48224ce1bd22f37a7fa6d111d54c1a340392bf
  - KFAIL 4 cases of: gdb.arch/powerpc-power7.exp
- Archer backport: d144a3633454046aaeae3e2c369c271834431d36
  - Fix C local extern variables (requires gcc-4.4.0-0.30).

* Fri Mar 27 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-12
- Archer update to the snapshot: 837d9879980148af05eae540d92caeb7200f1813
- Archer backport: 8340d06295c8db80c544503458305197891e0348
  - Fixes [master] regression for Eclipse CDT testsuite.
- Archer backport: 16328456d5740917ade0a49bcecc14c4564b9a99
  - Fixes #2 [expr] compatibility with gcc-4.4 on gdb.cp/namespace-using.exp.
- Rebase [expr] on the Keith Seitz's sync with FSF GDB fixing the former merge.

* Sun Mar 22 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-11
- Archer update to the snapshot: e734ed95d296a3342d4147873c4641cea6c4d7fe
- Archer backport: 1e1d73cda98b1adda884b80e07c7b4929c175628
  - Fixes [expr] compatibility with gcc-4.4 on gdb.cp/namespace-using.exp.

* Sun Mar 15 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-10
- Archer update to the snapshot: 935f217d3367a642374bc56c6b146d376fc3edab
- Archer backport: 281278326412f9d6a3fabb8adc1d419fd7ddc7d7
  - Fix [expr] crash reading invalid DWARF C++ symbol "" (BZ 490319).

* Thu Mar 12 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-9
- Archer backport: aafe933b497eee8cfab736a10bae1a90d4bceb18
  - [python] Remove duplicate target-wide-charset parameter

* Mon Mar  9 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-8
- Archer update to the snapshot: a99e30d08ade4a2df0f943b036cd653bcd12b04d
- Fixes internal error on breaking at a multi-locations C++ caller (BZ 488572).

* Mon Mar  9 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-7
- Archer update to the snapshot: ec29855686f2a78d90ebcc63765681249bbbe808
- Temporarily place libstdc++ pretty printers in this gdb.rpm.

* Sat Mar  7 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-6
- Archer update to the snapshot: 543fb2154d3bd551344b990b911be5c6cc703504
 - Fixes [delayed-symfile] excessive `(no debugging symbols found)' messages.

* Sat Mar  7 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-5
- Improve `gdb-6.6-buildid-locate-rpm.patch' by dlopen() (+pkg-config compat.).

* Sat Mar  7 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-4
- Split `gdb-6.6-buildid-locate.patch' to `gdb-6.6-buildid-locate-rpm.patch'.

* Sat Mar  7 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-3
- Archer update to the snapshot: 6cf16c0711e844094ab694b3d929f7bd30b49f61
- Fix crash on the inlined functions support.
- Fix crash from the PIE support, its varobj_refresh() was called only before
  varobj_invalidate() which is sufficient.
- Fix BuildRequires for the `--with testsuite' runs.
- Use the newly introduced `--with-pythondir' option.
- Remove libstdcxx [python] pretty printers (as included in libstdc++ rpm now).

* Fri Mar 06 2009 Jesse Keating <jkeating@redhat.com> - 6.8.50.20090302-2
- Rebuild for new rpm libs

* Mon Mar  2 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090302-1
- Include the Archer Project: http://sourceware.org/gdb/wiki/ProjectArcher
  snapshot: 8cc3753a9aad85bf53bef54c04334c60d16cb251
  * [python] Python scripting support: http://sourceware.org/gdb/wiki/PythonGdb
  * [catch-syscall] Trap and display syscalls.
  * [delayed-symfile] Improve startup performance by lazily read psymtabs.
  * [exception-rewind] Fix fatal C++ exceptions in an inferior function call.
  * [expr] Expressions, single-quote elimination, C++ input canonicalization.
  * [using-directive] C++ namespaces.
  * [vla] C variable length arrays / DW_FORM_block / Fortran dynamic arrays.
  * [misc] Fix debuginfoless `return' (BZ 365111), fix command-line macros for
    expected GCC (BZ 479914), new testcase for valgrind (for BZ 483262),
    implement `info common' for Fortran, fix Fortran logical-kind=8 (BZ 465310),
    fix static variable in C++ constructors (BZ 445912), fix power7 (BZ 485319).
- Upgrade to the FSF GDB gdb-6.8.50 snapshot.
- Fix parsing elf64-i386 files for kdump PAE vmcore dumps (BZ 457187).
  - Turn on 64-bit BFD support, globally enable AC_SYS_LARGEFILE.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8.50.20090210-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090210-1
- Upgrade to the FSF GDB gdb-6.8.50 snapshot.

* Wed Feb 11 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20090209-1
- Upgrade to the FSF GDB gdb-6.8.50 snapshot.

* Mon Feb  9 2009 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20081214-2
- Fix crash / implement `finish' into inlined functions (BZ 479781).
- Drop the gdb.threads/attach-into-signal.exp change as obsolete.

* Sun Dec 14 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8.50.20081214-1
- Upgrade to the upstream gdb-6.8.50 snapshot.

* Mon Dec  1 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-33
- Make `--with testsuite' BuildRequires properly conditional.

* Mon Dec  1 2008 Stepan Kasal <skasal@redhat.com> - 6.8-32
- Remove trivial BuildRequires, use rpm macros in a few remaining places.

* Tue Nov 18 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-31
- Enable ia64 hardware watchpoints if created before starting inferior.

* Sun Nov  9 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-30
- Fix a race in the testcase `gdb.threads/step-thread-exit.exp'.

* Sun Nov  9 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-29
- Fix more the variable-length-arrays support (BZ 468266, feature BZ 377541).
- Integrate the `bt full' protection (for BZ 466901) into the VLA patch.

* Thu Nov  6 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-28
- Fix the "never terminate `bt full'" patch false GCC warning / build error.

* Thu Nov  6 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-27
- Fix resolving of variables at locations lists in prelinked libs (BZ 466901),
  bugreported by Michal Babej.
- Never terminate `bt full' on a problem of variable resolving (for BZ 466901).

* Thu Nov  6 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-26
- Fix more the variable-length-arrays support (BZ 468266, feature BZ 377541).
- Fix the watchpoints conditionals.
- Fix on PPC spurious SIGTRAPs on active watchpoints.
- Fix occasional stepping lockup on many threads, seen on ia64.

* Mon Nov  3 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-25
- Fix the variable-length-arrays support (BZ 468266, feature BZ 377541).
- Fix the debuginfo-install suggestions for missing base packages (BZ 467901),
  also update the rpm/yum code to no longer require _RPM_4_4_COMPAT.

* Tue Sep  2 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-24
- Fix PIE patch regression for loading binaries from valgrind (BZ 460319).

* Thu Aug 28 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-23
- Fix attaching to stopped processes, based on the upstream version now.
  - Just kernel-2.6.25 neither upstream nor utrace work with it; 2.6.9 works.
- Fix occasional crash on a removed watchpoint.
- Fix false testcase FAILs for `gdb.pie/break.exp'.
- Fix a false warning (+a testcase FAIL) on s390x watchpoints.
- Fix a false FAIL on s390x `gdb.base/dump.exp'.

* Wed Aug 27 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-22
- Remove `gdb-6.3-nonthreaded-wp-20050117.patch' as obsoleted + regressing now.
- Make the GDB quit processing non-abortable to cleanup everything properly.
- Support DW_TAG_constant for Fortran in recent Fedora/RH GCCs.
- Fix crash on DW_TAG_module for Fortran in recent Fedora/RH GCCs.
- Readd resolving of bare names of constructors and destructors.
- Include various vendor testcases:
  - Leftover zombie process (BZ 243845).
  - Multithreaded watchpoints (`gdb.threads/watchthreads2.exp').
  - PIE testcases (`gdb.pie/*').
  - C++ contructors/destructors (`gdb.cp/constructortest.exp').

* Sat Aug 23 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-21
- Fix MI debuginfo print on reloaded exec, found by Denys Vlasenko (BZ 459414).
- Extend the Fortran dynamic variables patch also for dynamic Fortran strings.

* Wed Aug 13 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-20
- Temporarily disable attaching to a stopped process (BZ 453688)
  - To be reintroduced after a fix of the kernel BZ 454404.

* Mon Aug  4 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-19
- Fix `errno' printing on nonthreaded non-g3 inferiors (TLS minsym is absolute).

* Fri Aug  1 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-18
- Fix powerpc recent secure PLTs handling (shared library calls) (BZ 452960).
- Fix the testsuite .spec runner to run biarch also on ppc.
- Reenable testcases threadcrash.exp, chng-syms.exp, checkpoint.exp (BZ 207002).
- Fix PRPSINFO in the core files dumped by gcore (BZ 254229), reformatted patch
  from Denys Vlasenko.
- Fix register assignments with no GDB stack frames, Denys Vlasenko (BZ 436037).

* Mon Jul 14 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-17
- Refresh the patchset with fuzz 0 (for new rpmbuild).

* Mon Jul 14 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-16
- Rebuild with the new rpm-4.5.90 in the buildroot.

* Sat Jul 12 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-15
- Temporary rpm-4.5.90 compatibility workaround by Panu Matilainen.
- Fix a regression in the constant watchpoints fix, found by Daniel Jacobowitz.
- Fix the prelink testcase for false FAILs on i386.

* Tue Jul  8 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-14
- Fix crash due to calling an inferior function right after a watchpoint stop.

* Thu Jul  3 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-13
- Support transparent debugging of inlined functions for an optimized code.

* Fri Jun 20 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-12
- Remove the gdb/gdbtui binaries duplicity.

* Tue Jun 17 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-11
- Fix the testsuite run for ia64 (where no -m64 is present).
- Test a crash on libraries missing the .text section.
- Protect development in the build tree by automatic Makefile dependencies.
- Refuse creating watchpoints of an address value, suggested by Martin Stransky.
- Disable randomization (such as by setarch -R), suggested by Jakub Jelinek.
- Fix compatibility with recent glibc headers.

* Sun Jun  1 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-10
- Fix crash on a watchpoint update on an inferior stop.
- Fix the s390x part of the hardware watchpoints after a fork.

* Thu May 22 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-9
- Fix memory trashing on binaries from GNAT/Ada (workaround GCC PR 35998).

* Thu May 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.8-8
- Silence memcpy check which returns false positive (sparc64)

* Thu May 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.8-7
- patch from DaveM for sparc/sparc64
- touch up spec to enable sparcv9/sparc64

* Sat May  3 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-6
- Fix gdb.base/gcore-shmid0.exp to be unresolved on recent kernels.
- Make the testsuite results of dfp-test.exp more stable.

* Sun Apr 27 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-5
- Remove the kernel VDSO workaround (`no loadable ...') (kernel BZ 312011).

* Wed Apr 23 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-4
- Backport fix on various forms of threads tracking across exec() (BZ 442765).
- Testsuite: Include more biarch libraries on %%{multilib_64_archs}.
- Disable the build-id warnings for the testsuite run as they cause some FAILs.
- Fix PIE support for 32bit inferiors on 64bit debugger.
- Fix trashing memory on one ada/gnat testcase.
- Make the testsuite results on ada more stable.

* Wed Apr 16 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-3
- Fix ia64 compilation errors (Yi Zhan, BZ 442684).
- Fix build on non-standard rpm-devel includes (Robert Scheck, BZ 442449).
- Do not run the PIE mode for the testsuite during `--with upstream'.
- Fix test of the crash on a sw watchpoint condition getting out of the scope.

* Fri Apr 11 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-2
- Fix a regression due to PIE of reloading a changed exec file (BZ 433410).
- Include also biarch libgcc on %%{multilib_64_archs} for the testsuite.
- Cosmetic fix of a testcase sanity breakpoint setting (part of BZ 233852).
- New test of hiding unexpected breakpoints on intentional step commands.
- New test of GCORE for shmid 0 shared memory mappings.
- New test of a crash on `focus cmd', `focus prev' commands.
- Fix a minor test race of the hardware watchpoints after the fork call.
- Test crash on a sw watchpoint condition getting out of the scope.

* Fri Mar 28 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.8-1
- Upgrade to the latest upstream final release gdb-6.8.

* Mon Mar 10 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.50.20080227-3
- build-id warnings integrated more with rpm and the lists of the warnings got
  replaced usually by a single-line `debuginfo-install' advice.
  - FIXME: Testsuite needs an update for the new pre-prompt messages.
- Fix the `--with upstream' compilation - gstack/pstack are now omitted.

* Tue Mar  4 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.50.20080227-2
- Drop the unused `ChangeLog.RedHat' file stubs.
- New rpm option `--with upstream' to drop the Fedora patches for testing.
- Drop some no longer valid .spec file comments.
- Include the Fortran dynamic arrays entry for changelog of 6.7.50.20080227-1.

* Mon Mar  3 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.50.20080227-1
- Upgrade to the upstream gdb-6.8 prerelease.
- Cleanup the leftover `.orig' files during %%prep.
- Add expat-devel check by the configure script (for the other-arch builds).
- `--with testsuite' now also BuildRequires: fpc
- Backport fix of a segfault + PIE regression since 6.7.1 on PIE executables.
- Update the printed GDB version string to be Fedora specific.
- Fix/implement the Fortran dynamic arrays support (BZ 377541).

* Sat Mar  1 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-16
- Run the full testsuite also in the `-fPIE -pie' mode.

* Mon Feb 25 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-15
- New --with parameters `testsuite' and `debug'.
  - Testsuite is now run during the build only on explicit `--with testsuite'.
- Testsuite now possibly produces two outputs for the two GDB target arches.

* Thu Feb 21 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-14
- Rename `set debug build-id' as `set build-id-verbose', former level 1 moved
  to level 2, default value is now 1, use `set build-id-verbose 0' now to
  disable the missing separate debug filenames messages (BZ 432164).

* Wed Feb 20 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-13
- ia64 build fixes from Doug Chapman (BZ 428882).
- gdbserver separated into an extra package (BZ 405791).
- pstack obsoleted by included gstack (BZ 197020).
- Fix #include <asm/ptrace.h> on kernel-headers-2.6.25-0.40.rc1.git2.fc9.x86_64.
- Drop the PowerPC simulator as no longer being compatible with Fedora binaries.

* Thu Feb  7 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-12
- build-id debug messages print now the library names unconditionally.

* Thu Jan 24 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-11
- Improve the text UI messages for the build-id debug files locating.
  - Require now the rpm libraries.
- Fix false `(no debugging symbols found)' on `-readnever' runs.
- Extend the testcase `gdb.arch/powerpc-prologue.exp' for ppc64.

* Sat Jan 12 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-10
- Compilation fixup (-9 was never released).

* Sat Jan 12 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-9
- Fix also threaded inferiors for hardware watchpoints after the fork call.
- Test debugging statically linked threaded inferiors (BZ 239652).
  - It requires recent glibc to work in this case properly.
- Testcase cleanup fixup of the gcore memory and time requirements of 6.7.1-8.

* Thu Jan 10 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-8
- Fix detaching from a threaded formerly stopped process with non-primary
  thread currently active (general BZ 233852).
  - Enable back again the testcases named `attachstop.exp' (no such exist now).
  - Rename the testcase `gdb.threads/attachstop' to `gdb.threads/attachstop-mt'.
- Test ia64 memory leaks of the code using libunwind.
- Testcase delay increase (for BZ 247354).
- Test gcore memory and time requirements for large inferiors.

* Mon Jan  7 2008 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-7
- Backport the gcc-4.3 compatibility -Werror fixes.
- Fix documentation on hardware watchpoints wrt multiple threads.
- Rename the patch file for BZ 235197 from its former name 234468.
- Fix the vendora testcase `attach-32.exp' affecting the other tests results.
- Support DW_TAG_interface_type the same way as DW_TAG_class_type (BZ 426600).

* Mon Dec 10 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-6
- Testsuite fixes for more stable/comparable results.

* Sat Nov 24 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-5
- Reduce the excessive gcc-* packages dependencies outside of mock/koji.

* Fri Nov 16 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-4
- Fix `errno' resolving across separate debuginfo files.
- Fix segfault on no file loaded, `set debug solib 1', `info sharedlibrary'.
- Extend the testsuite run for all the languages if %%{dist} is defined.
- Support gdb.fortran/ tests by substituting the g77 compiler by gfortran.

* Sun Nov  4 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-3
- Fix `errno' resolving on recent glibc with broken DW_AT_MIPS_linkage_name.
- Imported new test for 6.7 PPC hiding of call-volatile parameter register.

* Sat Nov  3 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-2
- Backport `Breakpoints at multiple locations' patch primarily for C++.

* Thu Nov  1 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7.1-1
- Upgrade to GDB 6.7.1.  Drop redundant patches, forward-port remaining ones.

* Thu Nov  1 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.7-1
- Upgrade to GDB 6.7.  Drop redundant patches, forward-port remaining ones.
- Fix rereading of the main executable on its change.

* Fri Oct 19 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-37
- Fix hiding unexpected breakpoints on intentional step/next commands.
- Fix s390 compilation warning/failure due to a wrongly sized type-cast.

* Sun Oct 14 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-36
- Fix hardware watchpoints after inferior forks-off some process.

* Sat Oct 13 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-35
- Fix non-threaded watchpoints CTRL-C regression on `set follow child'.

* Fri Oct 12 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-34
- Fix gdbserver for threaded applications and recent glibc (BZ 328021).

* Tue Oct  9 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-33
- Fix debug load for sparse assembler files (such as vDSO32 for i386-on-x86_64).

* Mon Oct  8 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-32
- Set the breakpoints always to all the ctors/dtors variants (BZ 301701).
- Fix a TUI visual corruption due to the build-id warnings (BZ 320061).
- Fixed the kernel i386-on-x86_64 VDSO loading (producing `Lowest section in').

* Fri Oct  5 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-31
- Fix address changes of the ctors/dtors breakpoints w/multiple PCs (BZ 301701).
- Delete an info doc file on `rpmbuild -bp' later rebuilt during `rpmbuild -bc'.

* Tue Sep 25 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-30
- Fix re-setting of the ctors/dtors breakpoints with multiple PCs (BZ 301701).
- Avoid one useless user question in the core files locator (build-id).

* Sun Sep 23 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-29
- Fixed the kernel VDSO loading (`warning: no loadable sections found in ...').
- Fix the testcase for pending signals (from BZ 233852).

* Sat Sep 22 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-28
- Support also the `$allocate' and `$delete' ctor/dtor variants (BZ 301701).
- Fix the build compatibility with texinfo >= 4.10.
- Fix the testcase for pending signals (from BZ 233852).

* Sun Sep 16 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-27
- Fix attaching to stopped processes and/or pending signals.

* Tue Aug 28 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-26
- New fast verification whether the .debug file matches its peer (build-id).
- New locating of the matching binaries from the pure core file (build-id).

* Fri Aug 17 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-25
- Fixed excessive RPATH (related to BZ 228891).

* Wed Aug  8 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-24
- Fixed compatibility with the Rawhide glibc open(2) syscall sanity checking.
- Update the core_dump_elf_headers=1 compatibility code to the upstream variant.

* Mon Aug  6 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-23
- Update PPC unwinding patches to their upstream variants (BZ 140532).

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 6.6-22
- Rebuild for RH #249435

* Mon Jul 23 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-21
- Fixed compatibility with Rawhide kernel fs.binfmt_elf.core_dump_elf_headers=1.
- .spec file updates to mostly pass RPMLINT - Fedora merge review (BZ 225783).
- Fixed testcase of the exit of a thread group leader (of BZ 247354).
- Cleanup any leftover testsuite processes as it may stuck mock(1) builds.

* Sun Jul  8 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-20
- Do not hang on exit of a thread group leader (BZ 247354).
- New test for upstream fix of VDSO decoding while attaching to an i386 process.
- Fixed BZ # 232014 -> 232015.

* Thu Jul  5 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-19
- Link with libreadline provided by the operating system.

* Tue Jun 26 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-18
- Fix PPC software watchpoints active while stepping atomic instr. (BZ 237572).

* Thu Jun 21 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-17
- Support for stepping over PPC atomic instruction sequences (BZ 237572).
- `set scheduler-locking step' is no longer enforced but it is now default.

* Wed Jun 20 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-16
- Fix attaching a stopped process on expected + upstream kernels (BZ 233852).
 - Fix attaching during a pending signal being delivered.

* Thu Jun  7 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-15
- Testcase update to cover PPC Power6/DFP instructions disassembly (BZ 230000).
- Disable some known timeouting/failing testcases to reduce the build time.
- Fix crash on missing filenames debug info (BZ 242155).

* Sat Apr 28 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-14
- Fixup for the PPC Power6/DFP instructions disassembly (BZ 230000).
- New testcase for the GCORE buffer overflow (for BZ 238285, formerly 235753).

* Wed Apr 25 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-13
- Fix `gcore' command for 32bit PPC inferiors on 64bit PPC hosts (BZ 232015).

* Wed Apr 25 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-12
- Enable PowerPC to print 128-bit long double variables (BZ 237872).
- New testcase for gcore of 32bit inferiors on 64bit hosts.

* Tue Apr 24 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-11
- Package review, analysed by Ralf Corsepius (BZ 225783).
 - Fix prelink(8) testcase for non-root $PATH missing `/usr/sbin' (BZ 225783).
 - Fix debugging GDB itself - the compiled in source files paths (BZ 225783).
 - Fix harmless GCORE stack buffer overflow, by _FORTIFY_SOURCE=2 (BZ 238285).
 - Fix XML support - the build was missing `expat-devel'.
 - Updated the `info' files handling by the spec file.
 - Building now with the standard Fedora code protections - _FORTIFY_SOURCE=2.
 - Use multiple CPUs for the build (%%{?_smp_mflags}).
 - Separate testsuite run to its %%check section.
 - Fix (remove) non-ASCII spec file characters.
 - Remove system tools versions dumping - already present in mock build logs.

* Sun Apr 22 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-10
- Notify user of a child forked process being detached (BZ 235197).

* Sun Apr 22 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-9
- Allow running `/usr/bin/gcore' with provided but inaccessible tty (BZ 229517).
- Fix testcase for watchpoints in threads (for BZ 237096).
- BuildRequires now `libunwind-devel' instead of the former `libunwind'.
- Use the runtime libunwind .so.7, it requires now >= 0.99-0.1.frysk20070405cvs.

* Sat Mar 24 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-8
- Use definition of an empty structure as it is not an opaque type (BZ 233716).
- Fixed the gdb.base/attachstop.exp testcase false 2 FAILs.

* Thu Mar 15 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-7
- Suggest SELinux permissions problem; no assertion failure anymore (BZ 232371).

* Wed Mar 14 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-6
- Fix occasional dwarf2_read_address: Corrupted DWARF expression (BZ 232353).

* Mon Mar 12 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-5
- Temporary support for shared libraries >2GB on 64bit hosts. (BZ 231832)

* Sun Feb 25 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-4
- Backport + testcase for PPC Power6/DFP instructions disassembly (BZ 230000).

* Mon Feb  5 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-3
- Fix a race during attaching to dying threads; backport (BZ 209445).
- Testcase of unwinding has now marked its unsolvable cases (for BZ 140532).

* Fri Jan 26 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-2
- Backported post gdb-6.6 release PPC `show endian' fixup.
- Fix displaying of numeric char arrays as strings (BZ 224128).
- Simplified patches by merging upstream accepted ones into a single file.

* Sat Jan 20 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.6-1
- Upgrade to GDB 6.6.  Drop redundant patches, forward-port remaining ones.
- Backported post gdb-6.6 release ia64 unwinding fixups.
- Testcase for exec() from threaded program (BZ 202689).

* Mon Jan 15 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-27
- Fix the testsuite results broken in 6.5-26, stop invalid testsuite runs.

* Sat Jan 13 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-26
- Fix unwinding of non-debug (.eh_frame) PPC code, Andreas Schwab (BZ 140532).
- Fix unwinding of debug (.debug_frame) PPC code, workaround GCC (BZ 140532).
- Fix missing testsuite .log output of testcases using get_compiler_info().

* Fri Jan 12 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-25
- Fix unwinding of non-CFI (w/o debuginfo) PPC code by recent GCC (BZ 140532).

* Thu Jan 11 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-24
- Backport readline history for input mode commands like `command' (BZ 215816).

* Tue Jan  9 2007 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-23
- Find symbols properly at their original (included) file (BZ 109921).
- Remove the stuck mock(1) builds disfunctional workaround (-> mock BZ 221351).

* Sat Dec 30 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-22
- Fix unwinding crash on older gcj(1) code (extended CFI support) (BZ 165025).
- Include testcase for the readline history of input mode commands (BZ 215816).

* Sat Dec 23 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-21
- Try to reduce sideeffects of skipping ppc .so libs trampolines (BZ 218379).
- Fix lockup on trampoline vs. its function lookup; unreproducible (BZ 218379).

* Tue Dec 19 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-20
- Fix bogus 0x0 unwind of the thread's topmost function clone(3) (BZ 216711).
- Testcase for readline segfault on excessively long hand-typed lines.

* Tue Dec 12 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-19
- Fix attachment also to a threaded stopped process (BZ 219118).
- Cleanup any leftover testsuite processes as it may stuck mock(1) builds.

* Sat Nov 25 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-18
- Fix readline history for input mode commands like `command' (BZ 215816).

* Thu Nov 16 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-17
- Bugfix testcase typo of gdb-6.5-16.

* Thu Nov 16 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-16
- Provide testcase for accessing the last address space byte.

* Thu Nov  9 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-15
- Fix readline segfault on excessively long hand-typed lines.

* Thu Nov  2 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-14
- Fix "??" resolving of symbols from (non-prelinked) debuginfo packages.
- Fix "??" resolving of symbols from overlapping functions (nanosleep(3)).
- Also disable testcase "checkpoint.exp" for a possible kernel Bug 207002.
- Provided (disabled during build) threading testsuite from BEA.

* Sat Oct 14 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-13
- Fix deadlock accessing last address space byte; for corrupted backtraces.

* Sun Oct  8 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-12
- Disabled IPv6 until its user visible syntax gets stable upstream.

* Sun Oct  1 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-11
- No longer disassemble invalid i386 opcodes of movQ/movA (BZ 172034).
- Simplify the IPv6 patch for gdbserver (BZ 198365).
- Suggest fixing your target architecture for gdbserver(1) (BZ 190810).
- Fix dereferencing registers for 32bit inferiors on 64bit hosts (BZ 181390).
- Fix `gcore' command for 32bit inferiors on 64bit hosts.

* Wed Sep 27 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-10
- Support IPv6 for gdbserver (BZ 198365).
- Temporarily disable testcase "chng-syms.exp" for a possible kernel Bug 207002.

* Thu Sep 21 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-9
- Fix crash on C++ symbol failing to be demangled (BZ 206813).
- Fix attach to stopped process, supersede `gdb-6.3-attach-stop-20051011.patch'.
- Fix TLS symbols resolving for objects with separate .debug file (-debuginfo).
- Fix TLS symbols resolving for shared libraries with a relative pathname.
- Support TLS symbols (+`errno' suggestion if no pthread is found) (BZ 185337).

* Mon Sep 11 2006 Jan Kratochvil <jan.kratochvil@redhat.com> - 6.5-8
- Fix gdb printf command argument using "%%p" (BZ 205551).

* Mon Sep  4 2006 Alexandre Oliva <aoliva@redhat.com> - 6.5-7
- Fix bug in patch for CVE-2006-4146. (BZ 203873, BZ 203880)

* Thu Aug 24 2006 Alexandre Oliva <aoliva@redhat.com> - 6.5-6
- Avoid overflows and underflows in dwarf expression computation stack.
(BZ 203873)

* Thu Aug 24 2006 Alexandre Oliva <aoliva@redhat.com> - 6.5-5
- Backport support for i386 nop memory instructions.
- Fix debuginfo addresses resolving for --emit-relocs Linux kernels
(BZ 203661, from Jan Kratochvil, like the remaining changes).
- Bugfix segv on the source display by ^X 1 (fixes Patch130, BZ
200048).
- Do not step into the PPC solib trampolines (BZ 200533).
- Fix exec() from threaded program, partial CVS backport (BZ 182116).
- Fix occasional failure to load shared libraries (BZ 146810).
- Bugfix object names completion (fixes Patch116, BZ 193763).
- Avoid crash of 'info threads' if stale threads exist (BZ 195429).
- Handle corrupted or missing location list information (BZ 196439).

* Thu Jul 13 2006 Alexandre Oliva <aoliva@redhat.com> - 6.5-3
- Add missing definition of multilib_64_archs for glibc-devel buildreqs.
- Backport support for .gnu.hash sections.

* Wed Jul 12 2006 Alexandre Oliva <aoliva@redhat.com> - 6.5-2
- BuildReq sharutils, prelink and, on multilib systems, 32-bit glibc-devel.
- Drop obsolete attach-stop patch.
- Fix testcases in threaded-watchpoints2 and step-thread-exit patches.
- Re-enable attach-pie.exp, asm-source.exp and sigstep.exp tests.

* Tue Jul 11 2006 Alexandre Oliva <aoliva@redhat.com> - 6.5-1
- Upgrade to GDB 6.5.  Drop redundant patches, forward-port remaining
ones.  Re-enable ada and objc testsuites.

* Thu Jun 15 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.132
- Require flex and bison at build time.
- Additional patch for BZ 175083, to cope with waitpid setting status
even when returning zero.

* Wed May 31 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.131
- Require gettext at build time.  (BZ193366)

* Sat May 27 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.130
- Rewrite patch for BZ 175270, BZ 175083 so as to catch the exception
earlier.
- Remove too-fragile testcases from patches for CFA value and "S"
augmentation.

* Wed May 17 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.129
- Add not-automatically-generated file to fopen64 patch (BZ 191948).

* Fri Apr 14 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.128
- Avoid race conditions caused by exceptions messing with signal masks.
(BZ 175270, BZ 175083, maybe BZ 172938).
- Hardcode /bin and /usr/bin paths into gstack (BZ 179829, BZ 190548).
- Build in a subdir of the source tree instead of in a sibling directory.
- Switch to versioning scheme that uses the same base revision number
for all OSes, and uses a suffix to tell the builds apart and ensure
upgradability.

* Thu Apr 13 2006 Stepan Kasal <skasal@redhat.com> - 6.3.0.0-1.127
- Bump up release number.

* Thu Apr 13 2006 Stepan Kasal <skasal@redhat.com> - 6.3.0.0-1.123
- Use fopen64 where available.  Fixes BZ 178796, BZ 190547.
- Use bigger numbers than int.  Fixes BZ 171783, BZ 179096.

* Wed Mar  8 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.122
- Bump up release number.

* Wed Mar  8 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.119
- Fix regression in PIE debugging (BZ 133944) (re?)introduced by the
prelink fix (BZ 175075, BZ 190545).  Improve testcase for the prelink
fix.
- Revert dwarf2 frame identifier change.

* Tue Mar  7 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.118
- Bump up release number.

* Tue Mar  7 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.115
- Change dwarf2 frame identifiers to use the actual PC instead of the
function's entry point.
- Fix FSF and GDB contact addresses in new testcases.
- Do not try to compile x86_64-only CFA testcase on 32-bit x86.
- Change prelink test to issue untested instead of warning message if
system libraries are not prelinked.

* Fri Mar  3 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.114
- Bump up release number.

* Fri Mar  3 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.111
- Add support for "S" augmentation for signal stack frames.
- Add support for CFA value expressions and encodings.
- Various improvements to the prelink test.

* Thu Feb 23 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.110
- Bump up release number.

* Thu Feb 23 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.107
- Enable gdb to debug core files and executables with mismatched
prelink base addresses.  Fixes BZ 175075, BZ 190545.

* Tue Feb 14 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.106
- Bump up release number.

* Tue Feb 14 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.103
- Adjust type-punning patch to include fix not needed upstream.

* Tue Feb 14 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.102
- Bump up release number.

* Tue Feb 14 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.99
- Use type-punning warning fixes as accepted upstream.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 6.3.0.0-1.98.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 6.3.0.0-1.98.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 16 2006 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.98
- Bump up release number.

* Mon Dec 19 2005 Alexandre Oliva <aoliva@redhat.com> - 6.3.0.0-1.94
- Fix type-punning warnings issued by GCC 4.1.

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Thu Dec 01 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.93
- Bump up release number.

* Thu Dec 01 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.90
- Add option to allow backtracing past zero pc value.
- Bugzilla 170275

* Tue Nov 15 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.89
- Bump up release number.

* Tue Nov 15 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.86
- Fix ia64 user-specified SIGILL handling error.
- Bugzilla 165038.

* Tue Oct 18 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.85
- Bump up release number.

* Tue Oct 18 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.82
- Modify attach patch to add missing fclose.
- Bugzilla 166712

* Tue Oct 11 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.81
- Bump up release number.

* Tue Oct 11 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.78
- Support gdb attaching to a stopped process.

* Thu Sep 29 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.77
- Bump up release number.

* Thu Sep 29 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.74
- Fix up DSO read logic when process is attached.

* Mon Sep 26 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.73
- Bump up release number.

* Mon Sep 26 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.70
- Fix frame pointer calculation for ia64 sigtramp frame.

* Thu Sep 22 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.69
- Bump up release number.

* Thu Sep 22 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.66
- Remove extraneous xfree.

* Wed Sep 07 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.65
- Bump up release number.

* Wed Sep 07 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.62
- Readd readnever option

* Wed Jul 27 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.61
- Bump up release number.

* Tue Jul 26 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.57
- Bump up release number.

* Tue Jul 26 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.54
- Add testcase to verify printing of inherited members
- Bugzilla 146835

* Mon Jul 25 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.53
- Bump up release number.

* Mon Jul 25 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.50
- Fix bug with info frame and cursor address on ia64.
- Add testcase to verify pseudo-registers calculated for ia64 sigtramp.
- Bugzilla 160339

* Fri Jul 22 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.49
- Bump up release number.

* Fri Jul 22 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.46
- Fix attaching to 32-bit processes on 64-bit systems.
- Bugzilla 160254

* Thu Jul 14 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.45
- Bump up release number.

* Thu Jul 14 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.42
- Add work-around to make ia64 gcore work faster.
- Bugzilla 147436

* Thu Jul 14 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.41
- Bump up release number.

* Mon Jul 11 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.38
- Fix backtracing across sigaltstack for ia64
- Bugzilla 151741

* Fri Jul 08 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.37
- Bump up release number.

* Fri Jul 08 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.35
- Build pseudo-registers properly for sigtramp frame.
- Bugzilla 160339

* Fri Jul 08 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.34
- Bump up release number.

* Thu Jul 07 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.31
- Modify security errata to include additional bfd robustness updates
- Bugzilla 158680

* Fri Jun 10 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.30
- Bump up release number.

* Fri Jun 10 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.28
- Security errata for bfd and .gdbinit file usage
- Bugzilla 158680

* Wed May 18 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.24
- Bump up release number.

* Wed May 18 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.23
- Bump up release number.

* Wed May 18 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.22
- Specify SA_RESTART for linux-nat.c handlers and use my_waitpid
  which handles EINTR.

* Tue May 03 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.21
- Bump up release number.

* Tue May 03 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.20
- Bump up release number.

* Tue May 03 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.19
- Fix for partial die in cache error
- Bugzilla 137904

* Wed Apr 27 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.18
- Bump up release number.

* Wed Apr 27 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.17
- Bump up release number.

* Wed Apr 27 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.16
- Update ia64 sigtramp support to use libunwind and fix top-level
  rse register reads to also use libunwind.
- Bugzilla 151741

* Thu Apr 21 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.15
- Bump up release number.

* Thu Apr 21 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.14
- Bump up release number.

* Thu Apr 21 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.13
- Do not issue warning message for gcore under ia64
- Bugzilla 146416

* Mon Apr 11 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-1.12
- Update gstack patch, handle systems that lack /proc/<pid>/tasks.

* Fri Apr 8 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-1.11
- Replace patch warning about DW_OP_piece with a patch that implements
  the DW_OP_piece read path.

* Sat Apr 2 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-1.10
- Print a warning when the separate debug info's CRC doen't match;
  test.

* Wed Mar 30 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.9
- Bump up release number.

* Wed Mar 30 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.7
- Add proper vsyscall page support for ia64.

* Thu Mar 24 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.6
- Bump up release number.

* Thu Mar 24 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.4
- Fix printing of inherited members of C++ classes.
- Fix for Bugzilla 146835.

* Tue Mar 22 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.3
- Bump up release number.

* Thu Mar 17 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-1.1
- Remove warnings that cause errors when compiled with gcc4 and -Werror.

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 04 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.37
- Bump up release number.

* Thu Mar 03 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.35
- Add follow-fork fix from mainline sources.

* Thu Mar 03 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.34
- Bump up release number.

* Mon Feb 28 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.32
- Modify debug register handling for x86, x86-64 to be thread-specific.
- Modify threaded watchpoint code for x86, x86-64 to properly insert
  and remove watchpoints on all threads.

* Tue Feb 22 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.31
- Bump version number.

* Tue Feb 22 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.30
- Bump version number.

* Tue Feb 22 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.29
- Modify gdb-6.3-dwattype0-20050201.patch to check for a zero address
  and not zero unsnd.  Fix BE 32- vs 64-bit problem.

* Mon Feb 21 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.28
- Back port patch adding symfile-mem.o to all GNU/Linux builds.
  Fix BZ 146087.

* Wed Feb 16 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.27
- Bump up release number.

* Wed Feb 16 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.26
- Fix unload.exp testcase.

* Mon Feb 14 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.25
- Bump up release number.

* Mon Feb 14 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.24
- Fix gdb to always grab the terminal before a readline call.
- Bugzilla 147880

* Fri Feb 11 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.23
- Bump up release number.

* Fri Feb 11 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.21
- Fix gdb to handle stepping over the end of an exiting thread.
- Bugzilla 146848

* Thu Feb 10 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.20
- Bump up release number.

* Tue Feb 08 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.18
- Modify previous gcore patch to not use linux_proc_xfer_memory even
  for main thread.

* Mon Feb 07 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.17
- Modify previous gcore patch to only apply to ia64.

* Fri Feb 04 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.16
- Fix gcore to work properly for threaded applications
- Bugzilla 145309, 145092

* Fri Feb 04 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.15
- Tolerate DW_AT_type referencing <0> and instead of generating an
  error, treat as unknown type.
- Bugzilla 144852.

* Thu Feb  3 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.14
- Separate out test patches.

* Thu Jan 27 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.13
- Fix to allow ia64 gdb to backtrace from syscalls in a corefile.
- Bugzilla 145092.

* Wed Jan 26 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.12
- Fix to support examining files even when the executable moves
- Bugzilla 142122

* Wed Jan 26 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.11
- gdb-6.3-ppcdotsyms-20050126.patch: Backport BFD changes for reading
  synthetic symbols.  Rewrite code reading elf minimal symbols so that
  it includes synthetics.

* Fri Jan 21 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.10
- Fix to prevent resetting unwind kernel table size to invalid value
  when debugging a core file
- Bugzilla 145309

* Fri Jan 21 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.9
- When single stepping handle both back-to-back and nested signals.
- Disable .symbol patch, results in BFD errors.

* Fri Jan 21 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.8
- Support listing both in-charge and not-in-charge dtors when
  just the dtor name is given.
- Add new test case for newly added ctor/dtor functionality.

* Thu Jan 20 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.7
- Fix to allow breaking by line in both the in-charge and
  not-in-charge ctor/dtor.
- Bugzilla 117826

* Thu Jan 20 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.6
- Rebuild.

* Thu Jan 20 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.5
- Use bfd_get_synthetic_symtab to read in any synthetic symbols
  such as 64-bit PPC's ".symbol"s.

* Tue Jan 18 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.4
- Modify non-threaded watchpoint patch to use new observer.

* Mon Jan 17 2005 Jeff Johnston <jjohnstn@redhat.com> - 6.3.0.0-0.3
- Fix for non-threaded watchpoints.

* Mon Jan 17 2005 Andrew Cagney <cagney@redhat.com> - 6.3.0.0-0.2
- Enable PPC CFI, remove merged ppc patches.

* Wed Jan 12 2005 Elena Zannoni <ezannoni@redhat.com> - 6.3.0.0-0.1
- commit co-authors Andrew Cagney <cagney@redhat.com> and
  Jeff Johnston <jjohnstn@redhat.com>.
- Various fixes to complete the import and merge.

* Wed Dec 01 2004 Andrew Cagney <cagney@redhat.com> - 6.3.0.0
- Import GDB 6.3, get building, add all patches.

* Tue Nov 30 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.63
- When removing breakpoints, continue removing breakpoints even if an
  error occurs on the list.

* Sun Nov 28 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.62
- Bump version for RHEL4 build.

* Wed Nov 24 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.61
- For PPC-64, fix search for a symbol (wasn't specifying the section).

* Wed Nov 24 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.60
- For PPC-64, do not set malloc name to ".malloc"; no longer needed.
- For all, only define kfail when not already defined.

* Wed Nov 24 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.59
- Bump version.

* Wed Nov 24 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.58
- Add rs6000 reggroups; fixes problem of PS register being trashed
  causing mysterious branch breakpoints.

* Tue Nov 23 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.57
- Backport i386 prolog parser - better backtraces out of semop().
- Add option --readnever to suppress the reading of symbolic debug
  information.
- Add script gstack.sh, installed as gstack.
  Bugzilla 136584, 137121
- Add missing files gdb.pie/attach2.c, gdb.pie/break1.c and
  gdb.pie/Makefile.in along with testsuite/configure stuff for pie.

* Tue Nov 23 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.57
- Backport i386 prolog parser - better backtraces out of semop().
- Add option --readnever to suppress the reading of symbolic debug
  information.
- Add script gstack.sh, installed as gstack.
  Bugzilla 136584, 137121

* Mon Nov 22 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.56
- Bump up release number.

* Mon Nov 22 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.55
- Multiple ia64 backtrace fixes.  Bugzilla 125157

* Thu Nov 11 2004 Elena Zannoni <ezannoni@redhat.com> - 1.200400607.54
- Bump up release number

* Thu Nov 11 2004 Elena Zannoni <ezannoni@redhat.com> - 1.200400607.51
- Modify configure line to not use absolute paths. This was
  creating problems with makeinfo/texinfo.
- Get rid of makeinfo hack.
Bugzilla 135633

* Tue Nov 09 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.50
- Bump up release number

* Tue Nov 09 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.49
- Bump up release number

* Tue Nov 09 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.48
- Expose $base, $allocate constructors and $delete, $base destructors
  for breakpoints.

* Tue Nov 09 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.47
- Enable PPC CFI.

* Mon Nov 08 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.46
- Bump up release number

* Mon Nov 08 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.45
- Bump up release number

* Fri Nov 05 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.44
- Allow macros to continue past a backtrace error

* Tue Oct 26 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.43
- Hack around broken PT_FPSCR defined in headers.
- Import latest s390 fixes.
- Disable sigstep.exp - s390 has problems.
- Use PC's symtab when looking for a symbol.
- Work around DW_OP_piece.

* Fri Oct 22 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.42
- For 64-bit PPC, convert _dl_debug_state descriptor into a code address.
- Fix --ignore option.

* Sun Oct 10 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.40
- Disable attach-pie.exp test, hangs on amd64 without auxv.
- Move pie tests to pie.

* Sun Oct 10 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.39
- Fix comment bug in sigstep.exp.

* Thu Oct 07 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.38
- Do not invalidate cached thread info when resuming threads.
- Bump up release number.

* Fri Oct 01 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.35
- Fix S/390 watchpoint support to work better under threading.

* Fri Oct 01 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.34
- Fix thread_db_get_lwp to handle 2nd format ptids.

* Mon Sep 27 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.33
- Don't unwind past a zero PC (when normal frames).

* Mon Sep 27 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.32
- Add threaded watchpoint support for x86, x86-64, and ia64.

* Mon Sep 27 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.31
- Instead of deleting bigcore.exp, use runtest --ignore.

* Thu Sep 23 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.30
- Merge in mainline testsuite up to 2004-09-23, pick up sig*.exp tests.
  Merge in mainline infrun.c, pick up all infrun.c fixes.
  Generate bigcore's corefile from the running inferior.
  Limit bigcore's corefile to max file-size.

* Thu Sep 02 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.29
- Fix low-level lin-lwp code to wait specifically for any stepping
  LWP (bugzilla 130896)

* Tue Aug 31 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.28
- Add test case for bugzilla 128618 fix.

* Mon Aug 30 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.27
- Add support for breakpoints in manually loaded/unloaded shared libs.
  (bugzilla 128618)

* Mon Aug 30 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.26
- Add java inferior call support.

* Mon Aug 30 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.25
- Convert "main" the function descriptor, into an address.

* Mon Aug 30 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.24
- Fix single-stepping when a signal is pending, was exiting program.
  -- needs kernel fix so that ptrace(PT_STEP,SIG) doesn't do a PT_CONT.
  -- sigstep.exp tests pass with this fix applied.

* Mon Aug 30 2004 Elena Zannoni <ezannoni@redhat.com> - 1.200400607.23
- Delete some part of gdb-6.1post-test-rh.patch, to avoid confusing
  gdb when testing itself, and loading separate debug info.

* Fri Aug 13 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.22
- Check in gdb mainline fix for applications calling clone directly.

* Tue Aug 10 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.21
- Alter libunwind frame code to allow using libunwind 0.97 and up.

* Tue Aug 03 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.20
- Fix the ia64 libunwind test to match current output.

* Fri Jul 30 2004 Elena Zannoni <ezannoni@redhat.com> - 1.200400607.19
- Fix the tests where gdb debugs itself, as to not copy
  the executable to xgdb.

* Mon Jul 26 2004 Elena Zannoni <ezannoni@redhat.com> - 1.200400607.18
- Add Pie patches back in.

* Fri Jul 16 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.17
- Fix stepping over a no-debug shared-library function.
- Fix patch vsyscall patch name.

* Thu Jul 8 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.16
- Update thread code with fix from gdb HEAD

* Wed Jul 7 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.15
- disable vsyscall
- import Bob's crasher fix
- disable bigcore.exp

* Mon Jul 5 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.14
- Make large corefiles work on systems that require O_LARGEFILE.

* Tue Jun 29 2004 Elena Zannoni <ezannoni@redhat.com> - 1.200400607.13
- Fix BuildRequires for libunwind on ia64.

* Mon Jun 28 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.12
- Import wild frame ID patch.  Stops GDB incorrectly matching invalid
  frame IDs.
- Disable bigcore on ia64 and amd64.

* Fri Jun 25 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.11
- Fix testsuite to kill attach process (from corrinna/mainline).
- Fix build problems with vsyscall patch.

* Fri Jun 25 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.10
- Fix annotate test messages.
- Recognize VSYSCALL pages.

* Thu Jun 24 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.200400607.9
- Fix ia64 watchpoint support.

* Wed Jun 23 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.8
- Do not xfail signals on i387, convert KFAIL to FAIL and not XFAIL.

* Wed Jun 23 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.7
- Fix to ppc64 unwinder - handle glibcs function within syscall
  function hack.
- Update sigbpt.exp, ena-dis-br.exp observer.exp signull.exp,
  step-test.exp and sizeof.exp, so that test names are architecture
  clean.
- Disable bigcore.exp on PowerPC 64.

* Tue Jun 22 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.6
- Merge in mainline testsuite changes up to 2004-06-21.
- Re-implement 32 and 64-bit PPC signal trampolines.
- Check i386 and amd64 signal trampolines before dwarf2.
- Allow tramp-frame when there is a symbol.
- Test interaction between single-step, breakpoint and signal.
- ABI: Fix PPC64 function parameters, sizeof long-double, and enum
  return values.

* Mon Jun 21 2004 Elena Zannoni <ezannoni@redhat.com> - 1.200400607.5
- Fix sed line for gz info files.

* Mon Jun 21 2004 Andrew Cagney <cagney@redhat.com> - 1.200400607.4
- Tar/uuencode both the .sum and .log test results.

* Tue Jun 15 2004 Elena Zannoni <ezannoni@redhat.com> - 0.200400607.3
- Remove installation of mmalloc, and its info files.
- Add hack to deal with differring info files generated by makeinfo.
- Restore release number convention.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun 10 2004 Elena Zannoni <ezannoni@redhat.com> - 0.200400607.2
- Fix Requires and BuildRequires for libunwind dependencies.
- Add patch to silence gcc3.4 warnings.

* Wed Jun 09 2004 Elena Zannoni <ezannoni@redhat.com> - 0.200400607.1
- New import: revamp everything. Remove all patches for now.
- Update the Requires and BuildRequires sections.
- Removed stupid Ada testcases (there is no ada support in gdb yet).

* Mon May 10 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.20
- Disable PIE again.
- obsolete gdb64 only if on ppc64.

* Mon May 03 2004 Jeff Johnston <jjohnstn@redhat.com> - 0.20040223.19
- Add -u parameter to build ChangeLog patch.

* Mon May 03 2004 Jeff Johnston <jjohnstn@redhat.com> - 0.20040223.18
- Update thread fix made for .6 release to FSF version.

* Thu Apr 22 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.17
- Disable PIE again.

* Thu Apr 22 2004 Jeff Johnston <jjohnstn@redhat.com> - 0.20040223.16
- Bump version number.

* Wed Apr 21 2004 Jeff Johnston <jjohnstn@redhat.com> - 0.20040223.15
- fix ia64 info frame command
- also fix ia64 tdep file for which elf header file to include

* Tue Mar 30 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.14
- re-enable pie.

* Tue Mar 30 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.13
- Fix testsuite glitches.

* Wed Mar 24 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.12
- Fix typo.

* Wed Mar 24 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.11
- Make gdb compile w/o warnings with gcc-3.4.
- Reenable PIE support code.

* Tue Mar 23 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.10
- Bump version number

* Tue Mar 23 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.9
- temporarily disable PIE support.
- Add section to obsolete gdb64 package.

* Sun Mar 21 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.8
- Add support for debugging of PIE executables.

* Tue Mar 09 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.7
- Bump version number.

* Mon Mar 08 2004 Jeff Johnston <jjohnstn@redhat.com> - 0.20040223.6
- Fix thread support to recognize new threads even when they reuse
  tids of expired threads.  Also ensure that terminal is held by gdb
  while determining if a thread-create event has occurred.

* Mon Mar 08 2004 Andrew Cagney <cagney@redhat.com> - 0.20040223.5
- Sync with 6.1 branch; eliminate all amd64 patches;
  add more robust 32x64 PPC64 patches.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 2 2004 Andrew Cagney <cagney@redhat.com> - 0.20040223.4
- 32x64 fixes that work with threads, replaced old
  non-thread 32x64 patch, add nat patch.

* Wed Feb 25 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.3
- Add patch for x86_64 in 32 bit mode.

* Wed Feb 25 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.2
- Remove ppc64 hacks.
- Refresh some patches.

* Wed Feb 25 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20040223.1
- Import new gdb snapshot from mainline FSF.
- Update patch list.

* Tue Feb 17 2004 Jeff Johnston <jjohnstn@redhat.com> - 1.20031117.8
- Switch ia64-tdep.c to use new abi used by libunwind-0.95 and up.
- Fix gate area specification for ia64-linux-tdep.c.
- Fix long double support for ia64.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 08 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20031117.7
- Add fixes for ppc32 support on ppc64 platform, from Andrew Cagney.

* Tue Jan 06 2004 Elena Zannoni <ezannoni@redhat.com> - 0.20031117.6
- Add patch to have unique binary names in the testsuite.
- Disable s390/s390x pthread.exp test (FIXME)
- Don't install any info files for the ppc platform. Let's take them
  from the ppc64 one (or we get install conflicts).
- Remove generated info files from the source tree. They are generated
  as part of the FSF snapshot process.

* Mon Nov 24 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20031117.5
- Add patches from old rpm for i386 support on x86_64.
- Add build dependency on libunwind for ia64.

* Fri Nov 21 2003 Jeremy Katz <katzj@redhat.com> - 0.20031117.4
- more rpm tricks to get the gdb64 package happier

* Thu Nov 20 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20031117.3
- Add sick and twisted workaround for ppc64 architecture.

* Wed Nov 19 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20031117.2
- Fix typo in libunwind test.

* Tue Nov 18 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20031117.1
- Import new gdb snapshot from mainline FSF.
- Fix some testfiles.
- Add fixes for gcore, and patch for libunwind support on ia64.
- Add tests to see what versions of gcc, binutils, glibc and kernel we
  are running with.

* Wed Oct 15 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.41
- Bump up version number.

* Wed Sep 24 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.40
- Fix problem with gcore and single threaded programs. (bugzilla 103531)

* Mon Sep 22 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20030710.39
- Fix call to quit_target from quit_force.

* Sun Sep 21 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.38
- Fix PPC64 push dummy call.
- Re-fix PPC64 return value (had wrong / old patch).

* Sat Sep 20 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.37
- Fix PPC32 return values.

* Sat Sep 20 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.36
- Rewrite ppc64 retun value methods so that they (hopefully)
match the SysV spec.
- Enable ppc64 testsuite.

* Thu Sep 18 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.35
- Hack around problem "break main" vs "break .main" when there is
only a minimal ppc64 symbol table.  The former is a function descriptor
and not where you want the breakpoint to go.  Only convert descriptors
to pointers when the address is in the ".opd" section.

* Wed Sep 17 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.34
- Fix ppc32 push_dummy_call.

* Tue Sep 16 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.33
- Pack gdb.sum and gdb.log using uuencode and bzip.

* Tue Sep 16 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20030710.32
- Catch errors when quitting so exit of gdb still occurs.

* Mon Sep 15 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.31
- Fix ppc32 use_struct_convention.

* Thu Sep 11 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.30
- Mods to dwarf2-frame.c to work around a lack of GCC/CFI info.

* Thu Sep 11 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.29
- Bump up version number.

* Wed Sep 10 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.28
- Fix a core dump with MI.
- Add new ChangeLog patch for mi changes.

* Thu Sep 04 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.27
- Change the name of the package to gdb64 in ppc64 case.

* Tue Aug 26 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.26
- Add testcase for separate debug info.

* Tue Aug 26 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.25
- fix i386 on x86-64 TLS
- add "base-aug2003" suffix to older x86i386 patch

* Tue Aug 26 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.24
- skip the ppc64 and x86-64 frame redzone.

* Fri Aug 22 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.23
- Relax one testcase in selftest.exp a bit.
- Accept different output as well in thread bt (platform dependent).
- Enable testsuite run for ia64, ppc, s390 and s390x. They are in
  reasonably good shape.

* Thu Aug 21 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20030710.22
- Multiple ia64 fixes.
- Fix ia64 printing of function pointers.
- Fix ia64 prologue examination to ignore predicated insns if we
  haven't found the return address yet.
- Skip dump.exp testcase for ia64

* Thu Aug 21 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.21
- Bump release number.

* Wed Aug 20 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.20
- Relax pattern in annota2.exp test.

* Wed Aug 20 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.19
- rename gdb binary to gdb64 for ppc64 platform.

* Tue Aug 19 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20030710.18
- Fix ia64 pc unwinding to include psr slot.

* Mon Aug 18 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.17
- Fix info installation for annotate.texi. (Bugzilla 102521)

* Fri Aug 15 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.16
- revamp tls tests a bit.
- Handle new output from gdb in relocate.exp

* Wed Aug 13 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.15
- Fix problem for processing of separate debug info files.

* Wed Aug 13 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20030710.14
- add ia64.inc file for testing ia64 in gdb.asm testsuite

* Fri Aug 8 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.13
- print the libthread_db library path, print when threads are enabled

* Thu Aug 7 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.12
- "cat" the test log into the build log

* Wed Aug 06 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20030710.11
- modernize ia64 gdb to use new frame model
- remove/replace deprecated interfaces used by ia64 gdb

* Wed Aug 06 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.10
- Sync to gdb-5.3.90-sync-20030806.patch.

* Tue Jul 29 2003 Andrew Cagney <cagney@redhat.com> - 0.20030710.9
- add x86-64 i386 fixes

* Tue Jul 29 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.8
- Fix some tests by xfailing the correct target triplet for RedHat.
- Remove include of config.h from pthreads.c testcases.

* Mon Jul 28 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.7
- Fix some test failures, by escaping correctly.

* Thu Jul 24 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.6
- Remove one testcase that is redundant.

* Wed Jul 23 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.5
- Bump up release number.

* Wed Jul 23 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.4
- Bring in sync with current head of gdb-6 branch.
- Remove linespec patch, because included in the new sync patch.

* Fri Jul 18 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.3
- Add patch to avoid gdb segfault with bad debug info.
- Change location of build tree to avoid conflicts with older versions
  possibly installed.

* Thu Jul 17 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.2
- Add patch to synchronize the current snapshot with the gdb-6 branch head.
- Remove some patches that are includd in such diff.
- Enable tests on AMD64 as well.

* Fri Jul 11 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20030710.1
- Import new gdb snapshot.
- Revamp gdb.spec. Get rid of patches that apply to older versions.
- Add patches for ppc64 support, kfail and make gdb more robust in copingi
  with bad debug info.

* Wed Jul 02 2003 Jeff Johnston <jjohnstn@redhat.com> - 1.20021129.39
- Fix bug with ia64 checking of hardware breakpoints.

* Mon Jun 30 2003 Elena Zannoni <ezannoni@redhat.com> - 1.20021129.38
- Add necessary function for NPTL support on x86-64.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.37
* Tue Jun 03 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.36
- Enable warnings for x86_64, not x86-64.
- Fix warnings from infptrace.c and dwarfread.c.
- Print error message only when reading separate debug info really
  doesn't work (jimb@redhat.com).

* Fri May 23 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.35
- Fixes for fetching and storing access registers on s390x (jimb@redhat.com).
  Bugzilla 91455.

* Wed May 21 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20021129.34
- Do not generate error on detach failure.  Bugzilla 90900.

* Thu May 8 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.33
- New tests for asm on s390x (jimb@redhat.com). Bugzilla 90503.
- Fixes for prologue analysis on s390x (jimb@redhat.com). Bugzilla 90506.
- bfd fix for 64-bit platforms (jimb@redhat.com).
- Disable ppc64 builds until we have a port.

* Thu May 1 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20021129.32
- Add ia64 support to the float.exp testcase.

* Thu May 1 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.31
- Clean up the tls tests some more.
- Fix problem with non US-eng locale. Bugzilla bug 88823.

* Wed Apr 30 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20021129.30
- Fix ia64 prologue skipping.
- Fix ia64 line table.
- Fix setting of prev_pc in infrun.c.

* Mon Mar 31 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.29
- Include the gcore script, as gdb_gcore.sh and install it in
  /usr/bin as gcore.
- One more disassembly fix for core files. Added to
  gdb-5.3post-disasm-mar2003.patch. Bugzilla 87677.
- Enable build warnings for x86-64.

* Mon Mar 31 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.28
- Fix Java strings printing.
- Fix memory corruption in disassembly code. Bugzilla 85644.
- Testsuite fixes (jimb@redhat.com). Bugzilla 85457.
- Fixes for s390 stack handling (jimb@redhat.com). Bugzilla 85039.
- Fixes for s390 struct return (jimb@redhat.com).

* Wed Mar 26 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.27
- Fixes for disassembly of code in threaded applications. Bugzilla 87495.
- Fixes for s390 prologue analysis. (jimb@redhat.com).
  Bugzilla bugs 85251, 85214.

* Thu Mar 20 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.26
- Fix inferior function calls with void return on x86-64. Bugzilla bug 83197.
- Fix for upstream PR/699.
- Fix some problems with gdb-5.3post-thrtst-feb2003.patch.

* Wed Mar 19 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20021129.25
- Fix for thread-db.c: check_event() - Bugzilla bug 86231.

* Fri Mar 14 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.24
- Fix some problems with inferior function calls on x86-64.

* Fri Mar 07 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.23
- testsuite patches. Bugzilla 85215 85028 85335.

* Thu Mar 06 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.22
- Fix testsuite problems related to having '+' in the directory name.
  Bugzilla 85031.

* Mon Mar 03 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.21
- Fix a few inferior function call problems.

* Mon Mar 03 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.20
- Split the changelog patches in two. Cleanup messy patch section.

* Thu Feb 27 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20021129.19
- Perform run-time check for tkill syscall in lin-lwp.c.

* Mon Feb 24 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.18
- Update copyright year printed in version.

* Mon Feb 24 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.17
- Refresh build.

* Mon Feb 24 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.16
- Add some testsuite cleanups, to avoid spurious test failures.

* Fri Feb 21 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20021129.15
- Add patch to handle thread exiting when LD_ASSUME_KERNEL=2.4.1 which
  fixes Bugzilla bug 84217.

* Fri Feb 21 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.14
- New patch to fix disassembly on s390. Bugzilla bug 84286.
- New patch for attach/ptrace fix. Bugzilla bug 84220.
- Reenable tests for x86.

* Thu Feb 20 2003 Jeff Johnston <jjohnstn@redhat.com> - 0.20021129.13
- Add patch for mixed stabs with dwarf2 - bugzilla bug 84253.

* Wed Feb 12 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.12
- Disable tests also for x86.

* Tue Feb 11 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.11
- Add patch for mi threads tests.
- Add patch for dwarf2 debug_ranges section.
- Add patch for detach bug.

* Mon Feb 10 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.10
- Add patch for testsuite auto answering internal error queries.
- Add new TLS tests.
- Add cleanup patches for thread tests.

* Mon Feb 03 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.9
- Add new patch for thread support. Apply on all arches.
- Do not apply old patches, but leave them around for now.
- Add new patch for dwarf2 debug info reading.
- Add new patch for dwarf2 cfi engine cleanup.
- Add new patch for uiout problems.
- Add new patch for s390 build.
- Disable tests on all platforms but x86.

* Mon Jan 27 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.8
- Move all the changelog entries to a single patch.
- Add tests to the args patch.
- Add new patch for until command fix (bugzilla Bug 19890).
- s390 and s390x can be built with -Werror.
- Run make check for s390 and s390x too.
- Include an updated version of the thread nptl patch (still WIP).

* Wed Jan 15 2003 Phil Knirsch <pknirsch@redhat.com> - 0.20021129.7
- Apply the 2nd misc patch for s390 and s390x, too.

* Tue Jan 14 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.6
- Add patches for NPTL support, to be applied on i386 only.
  (this is still WIP)
- Split old misc patch in two parts.
- Temporarily disable testsuite run on alpha.

* Sun Jan 12 2003 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.5
- Add patch for --args with zero-length arguments. Fix for bug 79833.

* Tue Dec 17 2002 Elliot Lee <sopwith@redhat.com> - 0.20021129.4
- The define directive to rpm is significant even if the line it is
  in happens to start with a '#' character. Fixed.

* Fri Dec 13 2002 Elena Zannoni <ezannoni@redhat.com> - 0.20021129.3
- Merge previous patches for warnings into a single one.
- Add changelogs to patches.
- Add, but don't use, a macro to avoid stripping.

* Fri Dec  6 2002 Elena Zannoni <ezannoni@redhat.com>
- Add patch to allow debugging of executables with debug info stored
  in separate files.
- Add patch for Makefile dependencies and disable warnings for
  building thread-db.c.
- Re-enable building with -Werror for alpha, ia64, ppc.

* Mon Dec  2 2002 Elena Zannoni <ezannoni@redhat.com>
- Don't pass to gdb an empty build warnings flag, or that will disable warnings
  completely. We want to build using gdb's standard warnings instead.

* Mon Dec  2 2002 Elena Zannoni <ezannoni@redhat.com>
- Don't do testing for x86_64.

* Sun Dec  1 2002 Elena Zannoni <ezannoni@redhat.com>
- x86_64 doesn't build with Werror yet.
- Add patch for alpha.
- Alpha doesn't build with -Werror either.
- Add patch for ia64.
- Add patch for ppc.
- Drop ia64 from -Werror list.
- Drop ppc from -Werror list.

* Sun Dec  1 2002 Elena Zannoni <ezannoni@redhat.com>
- Add dejagnu to the build requirements.
- Enable make check.
- Add enable-gdb-build-warnings to the configure flags.

* Fri Nov 29 2002 Elena Zannoni <ezannoni@redhat.com>
- Import new upstream sources.
- Change version and release strings.
- Upgrade patches.
- Build gdb/gdbserver as well.
- Define and use 'cvsdate'.
- Do %%setup specifying the source directory name.
- Don't cd up one dir before removing tcl and friends.
- Change the configure command to allow for the new source tree name.
- Ditto for the copy of NEWS.
- Add some comments.

* Mon Nov 25 2002 Elena Zannoni <ezannoni@redhat.com> 5.2.1-5
General revamp.
- Add patch for gdb/doc/Makefile.in. Part of fix for bug 77615.
- Add patch for mmalloc/Makefile.in. Part of fix for bug 77615.
- Change string printed in version.in to <version>-<release>rh.
- Move the deletion of dejagnu, expect, tcl to the prep section,
  from the build section.
- Add build directory housekeeping to build section.
- Use macros for configure parameters.
- Do the build in a separate directory.
- Prepare for testing, but not enable it yet.
- Correctly copy the NEWS file to the top level directory, for the doc
  section to find it.
- Cd to build directory before doing install.
- Use makeinstall macro, w/o options.
- Remove workaround for broken gdb info files. Part of fix for bug 77615.
- Remove share/locale directory, it is in binutils.
- Remove info/dir file.
- Clarify meaning of post-install section.
- Add gdbint info files to post-install, pre-uninstall and files sections.
  Part of fix for bugs 77615, 76423.
- Add libmmalloc.a to package.

* Fri Aug 23 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- added mainframe patch from developerworks

* Wed Aug 21 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.2.1-3
- Add changelogs to the previous patch

* Wed Aug 14 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.2.1-2
- Add some patches from Elena Zannoni <ezannoni@redhat.com>

* Tue Jul 23 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.2.1-1
- 5.2.1

* Mon Jul 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- compile on mainframe

* Mon Jul  8 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.2-3
- Rebuild

* Tue May  7 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.2-2
- Rebuild

* Mon Apr 29 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.2-1
- 5.2

* Mon Apr 29 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.1.92-1
- 5.1.92. Hopefully identical to 5.2 final

* Mon Apr 22 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.1.91-1
- 5.1.91. 5.2 expected in a week

* Thu Mar 28 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.1.90CVS-5
- Update to current

* Thu Mar 28 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.1.90CVS-4
- Update to current

* Thu Mar 28 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.1.90CVS-3
- Update to current

* Wed Mar 20 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.1.90CVS-2
- Update to current

* Wed Mar 13 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.1.90CVS-1
- Update to current 5.2 branch

* Thu Jan 24 2002 Trond Eivind Glomsrod <teg@redhat.com> 5.1.1-1
- 5.1.1
- add URL

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Dec 10 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.1-2
- Fix some thread+fpu problems

* Mon Nov 26 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.1-1
- 5.1

* Mon Nov 19 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.0.94-0.71
- 5.0.94. Almost there....

* Mon Nov 12 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.0.93-2
- Add patch from jakub@redhat.com to improve handling of DWARF

* Mon Nov 12 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.0.93-1
- 5.0.93
- handle missing info pages in post/pre scripts

* Wed Oct 31 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.0.92-1
- 5.0.92

* Fri Oct 26 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.0.91rh-1
- New snapshot
- Use the 5.0.91 versioning from the snapshot

* Wed Oct 17 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.0rh-17
- New snapshot

* Thu Sep 27 2001 Trond Eivind Glomsrod <teg@redhat.com>
- New snapshot

* Wed Sep 12 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.0rh-16
- New snapshot

* Mon Aug 13 2001 Trond Eivind Glomsrod <teg@redhat.com> 5.0rh-15
- Don't buildrequire compat-glibc (#51690)

* Thu Aug  9 2001 Trond Eivind Glomsrod <teg@redhat.com>
- New snapshot, from the stable branch eventually leading to gdb 5.1

* Mon Jul 30 2001 Trond Eivind Glomsrod <teg@redhat.com>
- s/Copyright/License/
- Add texinfo to BuildRequires

* Mon Jun 25 2001 Trond Eivind Glomsrod <teg@redhat.com>
- New snapshot

* Fri Jun 15 2001 Trond Eivind Glomsrod <teg@redhat.com>
- New snapshot
- Add ncurses-devel to buildprereq
- Remove perl from buildprereq, as gdb changed the way
  version strings are generated

* Thu Jun 14 2001 Trond Eivind Glomsrod <teg@redhat.com>
- New snapshot

* Wed May 16 2001 Trond Eivind Glomsrod <teg@redhat.com>
- New snapshot - this had thread fixes for curing #39070
- New way of specifying version

* Tue May  1 2001 Trond Eivind Glomsrod <teg@redhat.com>
- New tarball
- Kevin's patch is now part of gdb

* Mon Apr  9 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Add patch from kevinb@redhat.com to fix floating point + thread
  problem (#24310)
- remove old workarounds
- new snapshot

* Thu Apr  5 2001 Trond Eivind Glomsrod <teg@redhat.com>
- New snapshot

* Sat Mar 17 2001 Bill Nottingham <notting@redhat.com>
- on ia64, there are no old headers :)

* Fri Mar 16 2001 Trond Eivind Glomsrod <teg@redhat.com>
- build with old headers, new compiler

* Fri Mar 16 2001 Trond Eivind Glomsrod <teg@redhat.com>
- new snapshot

* Mon Feb 26 2001 Trond Eivind Glomsrod <teg@redhat.com>
- new snapshot which should fix some more IA64 problems (#29151)
- remove IA64 patch, it's now integrated

* Wed Feb 21 2001 Trond Eivind Glomsrod <teg@redhat.com>
- add IA64 and Alpha patches from Kevin Buettner <kevinb@redhat.com>
- use perl instead of patch for fixing the version string

* Tue Feb 20 2001 Trond Eivind Glomsrod <teg@redhat.com>
- don't use kgcc anymore
- mark it as our own version
- new snapshot

* Mon Jan 22 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Link with ncurses 5.x even though we're using kgcc.
  No need to drag in requirements on ncurses4 (Bug #24445)

* Fri Jan 19 2001 Trond Eivind Glomsrod <teg@redhat.com>
- new snapshot

* Wed Dec 20 2000 Trond Eivind Glomsrod <teg@redhat.com>
- new snapshot

* Mon Dec 04 2000 Trond Eivind Glomsrod <teg@redhat.com>
- new snapshot
- new alpha patch - it now compiles everywhere. Finally.

* Fri Dec 01 2000 Trond Eivind Glomsrod <teg@redhat.com>
- new snapshot

* Mon Nov 20 2000 Trond Eivind Glomsrod <teg@redhat.com>
- new CVS snapshot
- disable the patches
- don't use %%configure, as it confuses the autoconf script
- enable SPARC, disable Alpha


* Wed Aug 09 2000 Trond Eivind Glomsrod <teg@redhat.com>
- added patch from GDB team for C++ symbol handling

* Tue Jul 25 2000 Trond Eivind Glomsrod <teg@redhat.com>
- upgrade to CVS snapshot
- excludearch SPARC, build on IA61

* Wed Jul 19 2000 Trond Eivind Glomsrod <teg@redhat.com>
- rebuild

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul 02 2000 Trond Eivind Glomsrod <teg@redhat.com>
- rebuild

* Thu Jun 08 2000 Trond Eivind Glomsrod <teg@redhat.com>
- use %%configure, %%makeinstall, %%{_infodir}, %%{_mandir},
  and %%{_tmppath}
- the install scripts  for info are broken(they don't care about
  you specify in the installstep), work around that.
- don't build for IA64

* Mon May 22 2000 Trond Eivind Glomsrod <teg@redhat.com>
- upgraded to 5.0 - dump all patches. Reapply later if needed.
- added the NEWS file to the %%doc files
- don't delete files which doesn't get installed (readline, texinfo)
- let build system handle stripping and gzipping
- don't delete libmmalloc
- apply patch from jakub@redhat.com to make it build on SPARC

* Fri Apr 28 2000 Matt Wilson <msw@redhat.com>
- rebuilt against new ncurses

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Tue Feb  8 2000 Jakub Jelinek <jakub@redhat.com>
- fix core file handling on i386 with glibc 2.1.3 headers

* Fri Jan 14 2000 Jakub Jelinek <jakub@redhat.com>
- fix reading registers from core on sparc.
- hack around build problems on i386 with glibc 2.1.3 headers

* Thu Oct 7 1999 Jim Kingdon
- List files to install in /usr/info specifically (so we don't pick up
things like info.info from GDB snapshots).

* Thu Oct 7 1999 Jim Kingdon
- Update GDB to 19991004 snapshot.  This eliminates the need for the
sigtramp, sparc, xref, and threads patches.  Update sparcmin patch.

* Mon Aug 23 1999 Jim Kingdon
- Omit readline manpage.

* Sat Aug  7 1999 Jim Kingdon
- Remove H.J. Lu's patches (they had been commented out).
- Add sigtramp patch (from gdb.cygnus.com) and threads patch (adapted
from code fusion CD-ROM).

* Wed Apr 14 1999 Jeff Johnson <jbj@redhat.com>
- merge H.J. Lu's patches into 4.18.

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- updated the kern22 patch with stuff from davem

* Thu Apr  1 1999 Jeff Johnson <jbj@redhat.com>
- sparc with 2.2 kernels no longer uses sunos ptrace (davem)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 3)

* Mon Mar  8 1999 Jeff Johnson <jbj@redhat.com>
- Sparc fiddles for Red Hat 6.0.
