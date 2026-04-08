# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global glibcsrcdir glibc-2.42-55-gebd45473f5
%global glibcversion 2.42
# Pre-release tarballs are pulled in from git using a command that is
# effectively:
#
# git archive HEAD --format=tar --prefix=$(git describe --match 'glibc-*')/ \
#	> $(git describe --match 'glibc-*').tar
# gzip -9 $(git describe --match 'glibc-*').tar
#
# glibc_release_url is only defined when we have a release tarball.
# Conversly, glibc_autorequires is set for development snapshots, where
# dependencies based on symbol versions are inaccurate.
%{lua: if string.match(rpm.expand("%glibcsrcdir"), "^glibc%-[0-9.]+$") then
    rpm.define("glibc_release_url https://ftp.gnu.org/gnu/glibc/")
  end
  local major, minor = string.match(rpm.expand("%glibcversion"),
                                    "^([0-9]+)%.([0-9]+)%.9000$")
  if major and minor then
    rpm.define("glibc_autorequires 1")
    -- The minor version in a .9000 development version lags the actual
    -- symbol version by one.
    local symver = "GLIBC_" .. major .. "." .. (minor + 1)
    rpm.define("glibc_autorequires_symver " .. symver)
  else
    rpm.define("glibc_autorequires 0")
  end}
##############################################################################
# We support the following options:
# --with/--without,
# * testsuite - Running the testsuite.
# * benchtests - Running and building benchmark subpackage.
# * bootstrap - Bootstrapping the package.
# * werror - Build with -Werror
# * docs - Build with documentation and the required dependencies.
# * valgrind - Run smoke tests with valgrind to verify dynamic loader.
#
# You must always run the testsuite for production builds.
# Default: Always run the testsuite.
%bcond_without testsuite
# Default: Always build the benchtests.
%bcond_without benchtests
# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Enable using -Werror
%bcond_without werror
# Default: Always build documentation.
%bcond_without docs

# Default: Always run valgrind tests if there is architecture support.
%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif
# Restrict %%{valgrind_arches} further in case there are problems with
# the smoke test.
%if %{with valgrind}
%ifarch ppc64 ppc64p7
# The valgrind smoke test does not work on ppc64, ppc64p7 (bug 1273103).
%undefine with_valgrind
%endif
%endif

# Build the POWER10 multilib.
%ifarch ppc64le
%define buildpower10 1
%else
%define buildpower10 0
%endif

%if %{with bootstrap}
# Disable benchtests, -Werror, docs, and valgrind if we're bootstrapping
%undefine with_benchtests
%undefine with_werror
%undefine with_docs
%undefine with_valgrind
%endif

# We do our own build flags management.  In particular, see
# glibc_shell_* below.
%undefine _auto_set_build_flags

##############################################################################
# Utility functions for pre/post scripts.  Stick them at the beginning of
# any lua %pre, %post, %postun, etc. sections to have them expand into
# those scripts.  It only works in lua sections and not anywhere else.
%global glibc_post_funcs %{expand:
-- We use lua because there may be no shell that we can run during
-- glibc upgrade. We used to implement much of %%post as a C program,
-- but from an overall maintenance perspective the lua in the spec
-- file was simpler and safer given the operations required.
-- All lua code will be ignored by rpm-ostree; see:
-- https://github.com/projectatomic/rpm-ostree/pull/1869
-- If we add new lua actions to the %%post code we should coordinate
-- with rpm-ostree and ensure that their glibc install is functional.
-- We must not use rpm.execute because this is a RPM 4.15 features and
-- we must still support downstream bootstrap with RPM 4.14 and missing
-- containerized boostrap.

-- Open-code rpm.execute with error message handling.
function post_exec (msg, program, ...)
  if rpm.spawn ~= nil then
    local status = rpm.spawn ({program, ...})
    if status == nil then
      io.stdout:write (msg)
      assert (nil)
    end
  else
    local pid = posix.fork ()
    if pid == 0 then
      posix.exec (program, ...)
      io.stdout:write (msg)
      assert (nil)
    elseif pid > 0 then
      posix.wait (pid)
    end
  end
end

function call_ldconfig ()
  post_exec("Error: call to ldconfig failed.\\n",
	    "ldconfig")
end

function update_gconv_modules_cache ()
  local iconv_dir = "%{_libdir}/gconv"
  local iconv_cache = iconv_dir .. "/gconv-modules.cache"
  local iconv_modules = iconv_dir .. "/gconv-modules"
  if posix.utime(iconv_modules) == 0 then
    if posix.utime (iconv_cache) == 0 then
      post_exec ("Error: call to %{_prefix}/sbin/iconvconfig failed.\\n",
		 "%{_prefix}/sbin/iconvconfig",
		 "-o", iconv_cache,
		 "--nostdlib",
		 iconv_dir)
    else
      io.stdout:write ("Error: Missing " .. iconv_cache .. " file.\\n")
    end
  end
end}

##############################################################################
# %%package glibc - The GNU C Library (glibc) core package.
##############################################################################
Summary: The GNU libc libraries
Name: glibc
Version: %{glibcversion}

# We'll use baserelease here for two reasons:
# - It is known to rpmdev-bumpspec, so it will be properly handled for mass-
#   rebuilds
# - It allows using the Release number without the %%dist tag in the dependency
#   generator to make the generated requires interchangeable between Rawhide
#   and ELN (.elnYY < .fcXX).
%global baserelease 10
Release: %{baserelease}%{?dist}

# Licenses:
#
# High level license status of the glibc source tree:
#
# * In general, GPLv2+ is used by programs, LGPLv2+ is used for
#   libraries.
#
# * LGPLv2+ with exceptions is used for things that are linked directly
#   into dynamically linked programs and shared libraries (e.g. crt
#   files, lib*_nonshared.a).  Historically, this exception also applies
#   to parts of libio.
#
# * GPLv2+ with exceptions is used for parts of the Arm unwinder.
#
# * GFDL is used for the documentation.
#
# * UNICODE v3 is used for the Unicode data files.
#
# * Some other licenses are used in various places (BSD, Inner-Net,
#   ISC, Public Domain, etc.).
#
# Licenses that make an appearance in the source tree but are not used:
#
# * HSRL and FSFAP are only used in test cases, which currently do not
#   ship in binary RPMs, so they are not listed here.
#
# * GPLv3+ is used by manual/texinfo.tex, which we do not use and a test and
#   some scripts that we do not ship, and so it is not listed here.
#
# * LGPLv3+ is used by some Hurd code, which we do not build.
#
# * A copyleft license is used in posix/runtests.c, but it is only a test
#   case and so the license is not listed here.
#
# * A "PCRE License" is used by PCRE.tests, but it is only a test case and
#   so the license is not listed here.
#
# * BSL-1.0 is only used by a test from boost and so the license is not
#   listed here.
#
# * Unlicense is used in an OpenRISC 1000 file which we don't support.
#
# SPDX references:
# https://spdx.org/licenses
# https://docs.fedoraproject.org/en-US/legal/allowed-licenses
# https://gitlab.com/fedora/legal/fedora-license-data
#
# SPDX license string based on evaluation of glibc-2.39 sources by
# ScanCode toolkit (https://github.com/nexB/scancode-toolkit),
# and accounting for exceptions listed above:
License: LGPL-2.1-or-later AND SunPro AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND BSD-3-Clause AND GPL-2.0-or-later AND LGPL-2.1-or-later WITH GNU-compiler-exception AND GPL-2.0-only AND ISC AND LicenseRef-Fedora-Public-Domain AND HPND AND CMU-Mach AND LGPL-2.0-or-later AND Unicode-3.0 AND GFDL-1.1-or-later AND GPL-1.0-or-later AND FSFUL AND MIT AND Inner-Net-2.0 AND X11 AND GPL-2.0-or-later WITH GCC-exception-2.0 AND GFDL-1.3-only AND GFDL-1.1-only

URL: http://www.gnu.org/software/glibc/
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.xz
Source1: bench.mk
Source2: glibc-bench-compare
Source3: glibc.req.in
Source4: glibc.attr
Source10: wrap-find-debuginfo.sh
Source11: parse-SUPPORTED.py
# Include in the source RPM for reference.
Source12: ChangeLog.old

# glibc_ldso: ABI-specific program interpreter name.  Used for debuginfo
# extraction (wrap-find-debuginfo.sh) and smoke testing ($run_ldso below).
#
# glibc_has_libnldbl: -lnldbl is supported for long double as double.
#
# glibc_has_libmvec: libmvec is available.
#
# glibc_rtld_early_cflags: The ABI baseline for architectures with
# potentially a later baseline.  The --with-rtld-early-cflags=
# configure option is passed to the main glibc build if this macro is
# defined.
%ifarch %{ix86}
%global glibc_ldso /lib/ld-linux.so.2
%global glibc_has_libnldbl 0
%global glibc_has_libmvec 0
%endif
%ifarch aarch64
%global glibc_ldso /lib/ld-linux-aarch64.so.1
%global glibc_has_libnldbl 0
%global glibc_has_libmvec 1
%endif
%ifarch ppc
%global glibc_ldso /lib/ld.so.1
%global glibc_has_libnldbl 1
%global glibc_has_libmvec 0
%endif
%ifarch ppc64
%global glibc_ldso /lib64/ld64.so.1
%global glibc_has_libnldbl 1
%global glibc_has_libmvec 0
%endif
%ifarch ppc64le
%global glibc_ldso /lib64/ld64.so.2
%global glibc_has_libnldbl 1
%global glibc_has_libmvec 0
%define glibc_rtld_early_cflags -mcpu=power8
%endif
%ifarch riscv64
%global glibc_ldso /lib/ld-linux-riscv64-lp64d.so.1
%global glibc_has_libnldbl 0
%global glibc_has_libmvec 0
%endif
%ifarch s390
%global glibc_ldso /lib/ld.so.1
%global glibc_has_libnldbl 1
%global glibc_has_libmvec 0
%define glibc_rtld_early_cflags -march=z13
%endif
%ifarch s390x
%global glibc_ldso /lib/ld64.so.1
%global glibc_has_libnldbl 1
%global glibc_has_libmvec 0
%define glibc_rtld_early_cflags -march=z13
%endif
%ifarch x86_64 x86_64_v2 x86_64_v3 x86_64_v4
%global glibc_ldso /lib64/ld-linux-x86-64.so.2
%global glibc_has_libnldbl 0
%global glibc_has_libmvec 1
%define glibc_rtld_early_cflags -march=x86-64
%endif

# This is necessary to enable source RPM building under noarch, as
# used by some build environments.
%ifarch noarch
%global glibc_ldso /lib/ld.so
%global glibc_has_libnldbl 0
%global glibc_has_libmvec 0
%endif

######################################################################
# Activate the wrapper script for debuginfo generation, by rewriting
# the definition of __debug_install_post.
%{lua:
local wrapper = rpm.expand("%{SOURCE10}")
local sysroot = rpm.expand("%{glibc_sysroot}")
local original = rpm.expand("%{macrobody:__debug_install_post}")
-- Strip leading newline.  It confuses the macro redefinition.
-- Avoid embedded newlines that confuse the macro definition.
original = original:match("^%s*(.-)%s*$"):gsub("\\\n", "")
rpm.define("__debug_install_post bash " .. wrapper
  .. " " .. sysroot .. " %{_prefix}%{glibc_ldso} " .. original)
}

# sysroot package support.  These contain arch-specific packages, so
# turn off the rpmbuild check.
%global _binaries_in_noarch_packages_terminate_build 0
# Variant of %%dist that contains just the distribution release, no affixes.
%{?fedora:%global sysroot_dist fc%{fedora}}
%{?rhel:%global sysroot_dist el%{rhel}}
%{?!sysroot_dist:%global sysroot_dist root}
# The name of the sysroot package.
%global sysroot_package_arch sysroot-%{_arch}-%{sysroot_dist}-%{name}
# Installed path for the sysroot tree.  Must contain /sys-root/, which
# triggers filtering.
%global sysroot_prefix /usr/%{_arch}-redhat-linux/sys-root/%{sysroot_dist}

# The wrapper script relies on the fact that debugedit does not change
# build IDs.
%global _no_recompute_build_ids 1
%undefine _unique_build_ids

%ifarch %{ix86}
# The memory tracing tools (like mtrace, memusage) in glibc-utils only work
# when the corresponding memory tracing libraries are preloaded.  So we ship
# memory allocation tracing/checking libraries in glibc-utils, except on
# i686 where we need to ship them in glibc.i686.  This is because
# glibc-utils.x86_64 will contain only the 64-bit version of these
# libraries.
%global glibc_ship_tracelibs_in_utils 0
%else
%global glibc_ship_tracelibs_in_utils 1
%endif

##############################################################################
# Patches:
# - See each individual patch file for origin and upstream status.
# - For new patches follow template.patch format.
##############################################################################
Patch13: glibc-fedora-localedata-rh61908.patch
Patch17: glibc-cs-path.patch
Patch23: glibc-python3.patch
Patch24: glibc-rh2432405.patch
# https://bugs.winehq.org/show_bug.cgi?id=58523
# revert 3d3572f59059e2b19b8541ea648a6172136ec42e to fix wine build
# applied with PP powers as we really need to build wine to fix scriptlet problems

##############################################################################
# Continued list of core "glibc" package information:
##############################################################################
Obsoletes: glibc-profile < 2.4
Obsoletes: nscd < 2.35
Provides: ldconfig
%if "%{_sbindir}" == "%{_bindir}"
# We rely on filesystem to create the compat symlinks for us
Requires: filesystem(unmerged-sbin-symlinks)
%endif
Provides: /sbin/ldconfig
Provides: /usr/sbin/ldconfig
# Historic file paths provided for backwards compatibility.
Provides: %{glibc_ldso}

# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)

# We need libgcc for cancellation support in POSIX threads.
Requires: libgcc%{_isa}
# Preserve the historic installation order.
Requires(pre): libgcc%{_isa}

Requires: glibc-common = %{version}-%{release}

# Various components (regex, glob) have been imported from gnulib.
Provides: bundled(gnulib)

Requires(pre): filesystem
Requires: filesystem

%ifarch %{ix86}
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# after nss_*.x86_64.  (See below for the other ordering.)
Recommends: (nss_db(x86-32) if nss_db(x86-64))
Recommends: (nss_hesiod(x86-32) if nss_hesiod(x86-64))
# Deinstall the glibc32 package if present.  This helps tests that do
# not run against the compose.
Conflicts: glibc32 <= %{version}-%{release}
Obsoletes: glibc32 <= %{version}-%{release}
%endif

# This is for building auxiliary programs like memusage
# For initial glibc bootstraps it can be commented out
%if %{without bootstrap}
BuildRequires: gd-devel libpng-devel zlib-devel
%endif
%if %{with docs}
%endif
%if %{without bootstrap}
BuildRequires: libselinux-devel >= 1.33.4-3
%endif
BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext
# We need procps-ng (/bin/ps), util-linux (/bin/kill), and gawk (/bin/awk),
# but it is more flexible to require the actual programs and let rpm infer
# the packages. However, until bug 1259054 is widely fixed we avoid the
# following:
# BuildRequires: /bin/ps, /bin/kill, /bin/awk
# And use instead (which should be reverted some time in the future):
BuildRequires: procps-ng, util-linux, gawk
BuildRequires: systemtap-sdt-devel

%if %{with valgrind}
# Require valgrind for smoke testing the dynamic loader to make sure we
# have not broken valgrind.
BuildRequires: valgrind
%endif

# We use python for the microbenchmarks and locale data regeneration
# from unicode sources (carried out manually). We choose python3
# explicitly because it supports both use cases.  On some
# distributions, python3 does not actually install /usr/bin/python3,
# so we also depend on python3-devel.
BuildRequires: python3 python3-devel

# This GCC version is needed for -fstack-clash-protection support.
BuildRequires: gcc >= 7.2.1-6
%global enablekernel 3.2
Conflicts: kernel < %{enablekernel}
%define target %{_target_cpu}-redhat-linux
%ifarch ppc64le
%global target ppc64le-redhat-linux
%endif

# GNU make 4.0 introduced the -O option.
BuildRequires: make >= 4.0

# The intl subsystem generates a parser using bison.
BuildRequires: bison >= 2.7

# binutils 2.30-17 is needed for --generate-missing-build-notes.
BuildRequires: binutils >= 2.30-17

# Earlier releases have broken support for IRELATIVE relocations
Conflicts: prelink < 0.4.2

%if %{without bootstrap}
%if %{with testsuite}
BuildRequires: diffutils
# The testsuite builds static C++ binaries that require a C++ compiler,
# static C++ runtime from libstdc++-static, and lastly static glibc.
BuildRequires: gcc-c++
BuildRequires: libstdc++-static
# A configure check tests for the ability to create static C++ binaries
# before glibc is built and therefore we need a glibc-static for that
# check to pass even if we aren't going to use any of those objects to
# build the tests.
BuildRequires: glibc-static

# libidn2 (but not libidn2-devel) is needed for testing AI_IDN/NI_IDN.
BuildRequires: libidn2

# The testsuite runs mtrace, which is a perl script
BuildRequires: perl-interpreter
%endif
%endif

# The compressed character maps and info files both require gzip for
# building.
#
# We support using gzip (gzip) or bzip (bzip2) at runtime to decompress
# the character maps, but we don't require them with Requires: to be
# able to use the 'locale' program with the installed compressed maps
# since this is a rare activity for most deployments.
BuildRequires: gzip

# Filter out all GLIBC_PRIVATE symbols since they are internal to
# the package and should not be examined by any other tool.
%global __filter_GLIBC_PRIVATE 1
%global __provides_exclude ^libc_malloc_debug\\.so.*$

# For language packs we have glibc require a virtual dependency
# "glibc-langpack" wich gives us at least one installed langpack.
# If no langpack providing 'glibc-langpack' was installed you'd
# get language-neutral support e.g. C, POSIX, and C.UTF-8 locales.
# In the past we used to install the glibc-all-langpacks by default
# but we no longer do this to minimize container and VM sizes.
# Today you must actively use the language packs infrastructure to
# install language support.
Requires: glibc-langpack = %{version}-%{release}
Suggests: glibc-minimal-langpack = %{version}-%{release}

# Suggest extra gconv modules so that they are installed by default but can be
# removed if needed to build a minimal OS image.
Recommends: glibc-gconv-extra%{_isa} = %{version}-%{release}
# Use redhat-rpm-config as a marker for a buildroot configuration, and
# unconditionally pull in glibc-gconv-extra in that case.
Requires: (glibc-gconv-extra%{_isa} = %{version}-%{release} if redhat-rpm-config)

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

######################################################################
# libnsl subpackage
######################################################################

%package -n libnsl
Summary: Legacy support library for NIS
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n libnsl
This package provides the legacy version of libnsl library, for
accessing NIS services.

This library is provided for backwards compatibility only;
applications should use libnsl2 instead to gain IPv6 support.

##############################################################################
# glibc "devel" sub-package
##############################################################################
%package devel
Summary: Object files for development using standard C libraries.
Requires: %{name} = %{version}-%{release}
Requires: libxcrypt-devel%{_isa} >= 4.0.0
Requires: kernel-headers >= 3.2
BuildRequires: kernel-headers >= 3.2
# For backwards compatibility, when the glibc-headers package existed.
Provides: glibc-headers = %{version}-%{release}
Provides: glibc-headers(%{_target_cpu})
Obsoletes: glibc-headers < %{version}-%{release}
# For backwards compatibility with alternative Fedora approach to
# work around multilib issue in composes.
%if 0%{?fedora}
%ifarch x86_64
Provides: glibc-headers-x86 = %{version}-%{release}
Obsoletes: glibc-headers-x86 < %{version}-%{release}
%endif
%ifarch s390x
Provides: glibc-headers-s390 = %{version}-%{release}
Obsoletes: glibc-headers-s390 < %{version}-%{release}
%endif
%endif

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc "doc" sub-package
##############################################################################
%if %{with docs}
%package doc
Summary: Documentation for GNU libc
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

# Removing texinfo will cause check-safety.sh test to fail because it seems to
# trigger documentation generation based on dependencies.  We need to fix this
# upstream in some way that doesn't depend on generating docs to validate the
# texinfo.  I expect it's simply the wrong dependency for that target.
BuildRequires: texinfo >= 5.0

%description doc
The glibc-doc package contains The GNU C Library Reference Manual in info
format.  Additional package documentation is also provided.
%endif

##############################################################################
# glibc "static" sub-package
##############################################################################
%package static
Summary: C library static libraries for -static linking.
Requires: %{name}-devel = %{version}-%{release}
Requires: libxcrypt-static%{?_isa} >= 4.0.0

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

##############################################################################
# glibc "common" sub-package
##############################################################################
%package common
Summary: Common binaries and locale data for glibc
Requires: %{name} = %{version}-%{release}
Recommends: tzdata >= 2003a

%if "%{_sbindir}" == "%{_bindir}"
# We rely on filesystem to create the compat symlinks for us
Requires: filesystem(unmerged-sbin-symlinks)
%endif

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

######################################################################
# File triggers to do ldconfig calls automatically (see rhbz#1380878)
######################################################################

# File triggers for when libraries are added or removed in standard
# paths.
%transfiletriggerin common -P 2000000 -p <lua> -- /lib /usr/lib /lib64 /usr/lib64
%glibc_post_funcs
call_ldconfig()
%end

%transfiletriggerpostun common -P 2000000 -p <lua> -- /lib /usr/lib /lib64 /usr/lib64
%glibc_post_funcs
call_ldconfig()
%end

# We need to run ldconfig manually because __brp_ldconfig assumes that
# glibc itself is always installed in $RPM_BUILD_ROOT, but with sysroots
# we may be installed into a subdirectory of that path.  Therefore we
# unset __brp_ldconfig and run ldconfig by hand with the sysroots path
# passed to -r.
%undefine __brp_ldconfig

######################################################################

%package locale-source
Summary: The sources for the locales
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description locale-source
The sources for all locales provided in the language packs.
If you are building custom locales you will most likely use
these sources as the basis for your new locale.

# We define a global regular expression to capture all of the locale
# sources. We use it later when constructing the various packages.
%global locale_rx eo syr tok *_*

%{lua:
-- To make lua-mode happy: '

-- List of supported locales.  This is used to generate the langpack
-- subpackages below.  This table needs adjustments if the set of
-- glibc locales changes.  "code" is the glibc code for the language
-- (before the "_".  "name" is the English translation of the language
-- name (for use in subpackage descriptions).  "regions" is a table of
-- variant specifiers (after the "_", excluding "@" and "."
-- variants/charset specifiers).  The table must be sorted by the code
-- field, and the regions table must be sorted as well.
--
-- English translations of language names can be obtained using (for
-- the "aa" language in this example):
--
-- python3 -c 'import langtable; print(langtable.language_name("aa", languageIdQuery="en"))'

local locales =  {
  { code="aa", name="Afar", regions={ "DJ", "ER", "ET" } },
  { code="af", name="Afrikaans", regions={ "ZA" } },
  { code="agr", name="Aguaruna", regions={ "PE" } },
  { code="ak", name="Akan", regions={ "GH" } },
  { code="am", name="Amharic", regions={ "ET" } },
  { code="an", name="Aragonese", regions={ "ES" } },
  { code="anp", name="Angika", regions={ "IN" } },
  {
    code="ar",
    name="Arabic",
    regions={
      "AE",
      "BH",
      "DZ",
      "EG",
      "IN",
      "IQ",
      "JO",
      "KW",
      "LB",
      "LY",
      "MA",
      "OM",
      "QA",
      "SA",
      "SD",
      "SS",
      "SY",
      "TN",
      "YE" 
    } 
  },
  { code="as", name="Assamese", regions={ "IN" } },
  { code="ast", name="Asturian", regions={ "ES" } },
  { code="ayc", name="Southern Aymara", regions={ "PE" } },
  { code="az", name="Azerbaijani", regions={ "AZ", "IR" } },
  { code="be", name="Belarusian", regions={ "BY" } },
  { code="bem", name="Bemba", regions={ "ZM" } },
  { code="ber", name="Berber", regions={ "DZ", "MA" } },
  { code="bg", name="Bulgarian", regions={ "BG" } },
  { code="bhb", name="Bhili", regions={ "IN" } },
  { code="bho", name="Bhojpuri", regions={ "IN", "NP" } },
  { code="bi", name="Bislama", regions={ "VU" } },
  { code="bn", name="Bangla", regions={ "BD", "IN" } },
  { code="bo", name="Tibetan", regions={ "CN", "IN" } },
  { code="br", name="Breton", regions={ "FR" } },
  { code="brx", name="Bodo", regions={ "IN" } },
  { code="bs", name="Bosnian", regions={ "BA" } },
  { code="byn", name="Blin", regions={ "ER" } },
  { code="ca", name="Catalan", regions={ "AD", "ES", "FR", "IT" } },
  { code="ce", name="Chechen", regions={ "RU" } },
  { code="chr", name="Cherokee", regions={ "US" } },
  { code="ckb", name="Central Kurdish", regions={ "IQ" } },
  { code="cmn", name="Mandarin Chinese", regions={ "TW" } },
  { code="crh", name="Crimean Turkish", regions={ "RU", "UA" } },
  { code="cs", name="Czech", regions={ "CZ" } },
  { code="csb", name="Kashubian", regions={ "PL" } },
  { code="cv", name="Chuvash", regions={ "RU" } },
  { code="cy", name="Welsh", regions={ "GB" } },
  { code="da", name="Danish", regions={ "DK" } },
  {
    code="de",
    name="German",
    regions={ "AT", "BE", "CH", "DE", "IT", "LI", "LU" } 
  },
  { code="doi", name="Dogri", regions={ "IN" } },
  { code="dsb", name="Lower Sorbian", regions={ "DE" } },
  { code="dv", name="Divehi", regions={ "MV" } },
  { code="dz", name="Dzongkha", regions={ "BT" } },
  { code="el", name="Greek", regions={ "CY", "GR" } },
  {
    code="en",
    name="English",
    regions={
      "AG",
      "AU",
      "BW",
      "CA",
      "DK",
      "GB",
      "HK",
      "IE",
      "IL",
      "IN",
      "NG",
      "NZ",
      "PH",
      "SC",
      "SG",
      "US",
      "ZA",
      "ZM",
      "ZW" 
    } 
  },
  { code="eo", name="Esperanto", regions={} },
  {
    code="es",
    name="Spanish",
    regions={
      "AR",
      "BO",
      "CL",
      "CO",
      "CR",
      "CU",
      "DO",
      "EC",
      "ES",
      "GT",
      "HN",
      "MX",
      "NI",
      "PA",
      "PE",
      "PR",
      "PY",
      "SV",
      "US",
      "UY",
      "VE" 
    } 
  },
  { code="et", name="Estonian", regions={ "EE" } },
  { code="eu", name="Basque", regions={ "ES" } },
  { code="fa", name="Persian", regions={ "IR" } },
  { code="ff", name="Fulah", regions={ "SN" } },
  { code="fi", name="Finnish", regions={ "FI" } },
  { code="fil", name="Filipino", regions={ "PH" } },
  { code="fo", name="Faroese", regions={ "FO" } },
  { code="fr", name="French", regions={ "BE", "CA", "CH", "FR", "LU" } },
  { code="fur", name="Friulian", regions={ "IT" } },
  { code="fy", name="Western Frisian", regions={ "DE", "NL" } },
  { code="ga", name="Irish", regions={ "IE" } },
  { code="gbm", name="Garhwali", regions={ "IN" } },
  { code="gd", name="Scottish Gaelic", regions={ "GB" } },
  { code="gez", name="Geez", regions={ "ER", "ET" } },
  { code="gl", name="Galician", regions={ "ES" } },
  { code="gu", name="Gujarati", regions={ "IN" } },
  { code="gv", name="Manx", regions={ "GB" } },
  { code="ha", name="Hausa", regions={ "NG" } },
  { code="hak", name="Hakka Chinese", regions={ "TW" } },
  { code="he", name="Hebrew", regions={ "IL" } },
  { code="hi", name="Hindi", regions={ "IN" } },
  { code="hif", name="Fiji Hindi", regions={ "FJ" } },
  { code="hne", name="Chhattisgarhi", regions={ "IN" } },
  { code="hr", name="Croatian", regions={ "HR" } },
  { code="hsb", name="Upper Sorbian", regions={ "DE" } },
  { code="ht", name="Haitian Creole", regions={ "HT" } },
  { code="hu", name="Hungarian", regions={ "HU" } },
  { code="hy", name="Armenian", regions={ "AM" } },
  { code="ia", name="Interlingua", regions={ "FR" } },
  { code="id", name="Indonesian", regions={ "ID" } },
  { code="ig", name="Igbo", regions={ "NG" } },
  { code="ik", name="Inupiaq", regions={ "CA" } },
  { code="is", name="Icelandic", regions={ "IS" } },
  { code="it", name="Italian", regions={ "CH", "IT" } },
  { code="iu", name="Inuktitut", regions={ "CA" } },
  { code="ja", name="Japanese", regions={ "JP" } },
  { code="ka", name="Georgian", regions={ "GE" } },
  { code="kab", name="Kabyle", regions={ "DZ" } },
  { code="kk", name="Kazakh", regions={ "KZ" } },
  { code="kl", name="Kalaallisut", regions={ "GL" } },
  { code="km", name="Khmer", regions={ "KH" } },
  { code="kn", name="Kannada", regions={ "IN" } },
  { code="ko", name="Korean", regions={ "KR" } },
  { code="kok", name="Konkani", regions={ "IN" } },
  { code="ks", name="Kashmiri", regions={ "IN" } },
  { code="ku", name="Kurdish", regions={ "TR" } },
  { code="kv", name="Komi", regions={ "RU" } },
  { code="kw", name="Cornish", regions={ "GB" } },
  { code="ky", name="Kyrgyz", regions={ "KG" } },
  { code="lb", name="Luxembourgish", regions={ "LU" } },
  { code="lg", name="Ganda", regions={ "UG" } },
  { code="li", name="Limburgish", regions={ "BE", "NL" } },
  { code="lij", name="Ligurian", regions={ "IT" } },
  { code="ln", name="Lingala", regions={ "CD" } },
  { code="lo", name="Lao", regions={ "LA" } },
  { code="lt", name="Lithuanian", regions={ "LT" } },
  { code="ltg", name="Latgalian", regions={ "LV" } },
  { code="lv", name="Latvian", regions={ "LV" } },
  { code="lzh", name="Literary Chinese", regions={ "TW" } },
  { code="mag", name="Magahi", regions={ "IN" } },
  { code="mai", name="Maithili", regions={ "IN", "NP" } },
  { code="mdf", name="Moksha", regions={ "RU" } },
  { code="mfe", name="Morisyen", regions={ "MU" } },
  { code="mg", name="Malagasy", regions={ "MG" } },
  { code="mhr", name="Meadow Mari", regions={ "RU" } },
  { code="mi", name="Maori", regions={ "NZ" } },
  { code="miq", name="Miskito", regions={ "NI" } },
  { code="mjw", name="Karbi", regions={ "IN" } },
  { code="mk", name="Macedonian", regions={ "MK" } },
  { code="ml", name="Malayalam", regions={ "IN" } },
  { code="mn", name="Mongolian", regions={ "MN" } },
  { code="mni", name="Manipuri", regions={ "IN" } },
  { code="mnw", name="Mon", regions={ "MM" } },
  { code="mr", name="Marathi", regions={ "IN" } },
  { code="ms", name="Malay", regions={ "MY" } },
  { code="mt", name="Maltese", regions={ "MT" } },
  { code="my", name="Burmese", regions={ "MM" } },
  { code="nan", name="Min Nan Chinese", regions={ "TW" } },
  { code="nb", name="Norwegian Bokmål", regions={ "NO" } },
  { code="nds", name="Low German", regions={ "DE", "NL" } },
  { code="ne", name="Nepali", regions={ "NP" } },
  { code="nhn", name="Tlaxcala-Puebla Nahuatl", regions={ "MX" } },
  { code="niu", name="Niuean", regions={ "NU", "NZ" } },
  { code="nl", name="Dutch", regions={ "AW", "BE", "NL" } },
  { code="nn", name="Norwegian Nynorsk", regions={ "NO" } },
  { code="nr", name="South Ndebele", regions={ "ZA" } },
  { code="nso", name="Northern Sotho", regions={ "ZA" } },
  { code="oc", name="Occitan", regions={ "FR" } },
  { code="om", name="Oromo", regions={ "ET", "KE" } },
  { code="or", name="Odia", regions={ "IN" } },
  { code="os", name="Ossetic", regions={ "RU" } },
  { code="pa", name="Punjabi", regions={ "IN", "PK" } },
  { code="pap", name="Papiamento", regions={ "AW", "CW" } },
  { code="pl", name="Polish", regions={ "PL" } },
  { code="ps", name="Pashto", regions={ "AF" } },
  { code="pt", name="Portuguese", regions={ "BR", "PT" } },
  { code="quz", name="Cusco Quechua", regions={ "PE" } },
  { code="raj", name="Rajasthani", regions={ "IN" } },
  { code="rif", name="Tarifit", regions={ "MA" } },
  { code="ro", name="Romanian", regions={ "RO" } },
  { code="ru", name="Russian", regions={ "RU", "UA" } },
  { code="rw", name="Kinyarwanda", regions={ "RW" } },
  { code="sa", name="Sanskrit", regions={ "IN" } },
  { code="sah", name="Sakha", regions={ "RU" } },
  { code="sat", name="Santali", regions={ "IN" } },
  { code="sc", name="Sardinian", regions={ "IT" } },
  { code="scn", name="Sicilian", regions={ "IT" } },
  { code="sd", name="Sindhi", regions={ "IN" } },
  { code="se", name="Northern Sami", regions={ "NO" } },
  { code="sgs", name="Samogitian", regions={ "LT" } },
  { code="shn", name="Shan", regions={ "MM" } },
  { code="shs", name="Shuswap", regions={ "CA" } },
  { code="si", name="Sinhala", regions={ "LK" } },
  { code="sid", name="Sidamo", regions={ "ET" } },
  { code="sk", name="Slovak", regions={ "SK" } },
  { code="sl", name="Slovenian", regions={ "SI" } },
  { code="sm", name="Samoan", regions={ "WS" } },
  { code="so", name="Somali", regions={ "DJ", "ET", "KE", "SO" } },
  { code="sq", name="Albanian", regions={ "AL", "MK" } },
  { code="sr", name="Serbian", regions={ "ME", "RS" } },
  { code="ss", name="Swati", regions={ "ZA" } },
  { code="ssy", name="Saho", regions={ "ER" } },
  { code="st", name="Southern Sotho", regions={ "ZA" } },
  { code="su", name="Sudanese", regions={ "ID" } },
  { code="sv", name="Swedish", regions={ "FI", "SE" } },
  { code="sw", name="Swahili", regions={ "KE", "TZ" } },
  { code="syr", name="Syriac", regions={} },
  { code="szl", name="Silesian", regions={ "PL" } },
  { code="ta", name="Tamil", regions={ "IN", "LK" } },
  { code="tcy", name="Tulu", regions={ "IN" } },
  { code="te", name="Telugu", regions={ "IN" } },
  { code="tg", name="Tajik", regions={ "TJ" } },
  { code="th", name="Thai", regions={ "TH" } },
  { code="the", name="Chitwania Tharu", regions={ "NP" } },
  { code="ti", name="Tigrinya", regions={ "ER", "ET" } },
  { code="tig", name="Tigre", regions={ "ER" } },
  { code="tk", name="Turkmen", regions={ "TM" } },
  { code="tl", name="Tagalog", regions={ "PH" } },
  { code="tn", name="Tswana", regions={ "ZA" } },
  { code="to", name="Tongan", regions={ "TO" } },
  { code="tok", name="Toki Pona", regions={} },
  { code="tpi", name="Tok Pisin", regions={ "PG" } },
  { code="tr", name="Turkish", regions={ "CY", "TR" } },
  { code="ts", name="Tsonga", regions={ "ZA" } },
  { code="tt", name="Tatar", regions={ "RU" } },
  { code="ug", name="Uyghur", regions={ "CN" } },
  { code="uk", name="Ukrainian", regions={ "UA" } },
  { code="unm", name="Unami language", regions={ "US" } },
  { code="ur", name="Urdu", regions={ "IN", "PK" } },
  { code="uz", name="Uzbek", regions={ "UZ" } },
  { code="ve", name="Venda", regions={ "ZA" } },
  { code="vi", name="Vietnamese", regions={ "VN" } },
  { code="wa", name="Walloon", regions={ "BE" } },
  { code="wae", name="Walser", regions={ "CH" } },
  { code="wal", name="Wolaytta", regions={ "ET" } },
  { code="wo", name="Wolof", regions={ "SN" } },
  { code="xh", name="Xhosa", regions={ "ZA" } },
  { code="yi", name="Yiddish", regions={ "US" } },
  { code="yo", name="Yoruba", regions={ "NG" } },
  { code="yue", name="Cantonese", regions={ "HK" } },
  { code="yuw", name="Yau", regions={ "PG" } },
  { code="zgh", name="Tamazight", regions={ "MA" } },
  { code="zh", name="Mandarin Chinese", regions={ "CN", "HK", "SG", "TW" } },
  { code="zu", name="Zulu", regions={ "ZA" } } 
}

-- Prints a list of LANGUAGE "_" REGION pairs.  The output is expected
-- to be identical to parse-SUPPORTED.py.  Called from the %%prep section.
function print_locale_pairs()
   for i = 1, #locales do
      local locale = locales[i]
      if #locale.regions == 0 then
	 print(locale.code .. "\n")
      else
	 for j = 1, #locale.regions do
	    print(locale.code .. "_" .. locale.regions[j] .. "\n")
	 end
      end
   end
end

local function compute_supplements(locale)
   local lang = locale.code
   local regions = locale.regions
   result = "langpacks-core-" .. lang
   for i = 1, #regions do
      result = result .. " or langpacks-core-" .. lang .. "_" .. regions[i]
   end
   return result
end

-- Emit the definition of a language pack package.
local function lang_package(locale)
   local lang = locale.code
   local langname = locale.name
   local suppl = compute_supplements(locale)
   print(rpm.expand([[

%package langpack-]]..lang..[[

Summary: Locale data for ]]..langname..[[

Provides: glibc-langpack = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Supplements: ((glibc and (]]..suppl..[[)) unless glibc-all-langpacks)
%description langpack-]]..lang..[[

The glibc-langpack-]]..lang..[[ package includes the basic information required
to support the ]]..langname..[[ language in your applications.
%files -f langpack-]]..lang..[[.filelist langpack-]]..lang..[[
]]))
end

for i = 1, #locales do
   lang_package(locales[i])
end
}

# The glibc-all-langpacks provides the virtual glibc-langpack,
# and thus satisfies glibc's requirement for installed locales.
# Users can add one more other langauge packs and then eventually
# uninstall all-langpacks to save space.
%package all-langpacks
Summary: All language packs for %{name}.
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Provides: %{name}-langpack = %{version}-%{release}
%description all-langpacks

# No %files, this is an empty package. The C/POSIX and
# C.UTF-8 files are already installed by glibc. We create
# minimal-langpack because the virtual provide of
# glibc-langpack needs at least one package installed
# to satisfy it. Given that no-locales installed is a valid
# use case we support it here with this package.
%package minimal-langpack
Summary: Minimal language packs for %{name}.
Provides: glibc-langpack = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
%description minimal-langpack
This is a Meta package that is used to install minimal language packs.
This package ensures you can use C, POSIX, or C.UTF-8 locales, but
nothing else. It is designed for assembling a minimal system.
%files minimal-langpack

# Infrequently used iconv converter modules.
%package gconv-extra
Summary: All iconv converter modules for %{name}.
Requires: %{name}%{_isa} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description gconv-extra
This package contains all iconv converter modules built in %{name}.

##############################################################################
# Subpackages for NSS modules except nss_files, nss_compat, nss_dns
##############################################################################

# This should remain it's own subpackage or "Provides: nss_db" to allow easy
# migration from old systems that previously had the old nss_db package
# installed. Note that this doesn't make the migration that smooth, the
# databases still need rebuilding because the formats were different.
# The nss_db package was deprecated in F16 and onwards:
# https://lists.fedoraproject.org/pipermail/devel/2011-July/153665.html
# The different database format does cause some issues for users:
# https://lists.fedoraproject.org/pipermail/devel/2011-December/160497.html
%package -n nss_db
Summary: Name Service Switch (NSS) module using hash-indexed files
Requires: %{name}%{_isa} = %{version}-%{release}
%ifarch x86_64
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# before nss_db.x86_64.  (See above for the other ordering.)
Recommends: (nss_db(x86-32) if glibc(x86-32))
%endif

%description -n nss_db
The nss_db Name Service Switch module uses hash-indexed files in /var/db
to speed up user, group, service, host name, and other NSS-based lookups.

%package -n nss_hesiod
Summary: Name Service Switch (NSS) module using Hesiod
Requires: %{name}%{_isa} = %{version}-%{release}
%ifarch x86_64
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# before nss_hesiod.x86_64.  (See above for the other ordering.)
Recommends: (nss_hesiod(x86-32) if glibc(x86-32))
%endif

%description -n nss_hesiod
The nss_hesiod Name Service Switch module uses the Domain Name System
(DNS) as a source for user, group, and service information, following
the Hesiod convention of Project Athena.

%package nss-devel
Summary: Development files for directly linking NSS service modules
Requires: %{name}%{_isa} = %{version}-%{release}
Requires: nss_db%{_isa} = %{version}-%{release}
Requires: nss_hesiod%{_isa} = %{version}-%{release}

%description nss-devel
The glibc-nss-devel package contains the object files necessary to
compile applications and libraries which directly link against NSS
modules supplied by glibc.

This is a rare and special use case; regular development has to use
the glibc-devel package instead.

##############################################################################
# glibc "utils" sub-package
##############################################################################
%package utils
Summary: Development utilities from GNU C library
Requires: %{name} = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

%if %{with benchtests}
%package benchtests
Summary: Benchmarking binaries and scripts for %{name}
%description benchtests
This package provides built benchmark binaries and scripts to run
microbenchmark tests on the system.
%endif

##############################################################################
# compat-libpthread-nonshared
# See: https://sourceware.org/bugzilla/show_bug.cgi?id=23500
##############################################################################
%package -n compat-libpthread-nonshared
Summary: Compatibility support for linking against libpthread_nonshared.a.

%description -n compat-libpthread-nonshared
This package provides compatibility support for applications that expect
libpthread_nonshared.a to exist. The support provided is in the form of
an empty libpthread_nonshared.a that allows dynamic links to succeed.
Such applications should be adjusted to avoid linking against
libpthread_nonshared.a which is no longer used. The static library
libpthread_nonshared.a is an internal implementation detail of the C
runtime and should not be expected to exist.

%if %{without bootstrap}
%package -n %sysroot_package_arch
Summary: Sysroot package for glibc, %{_arch} architecture
BuildArch: noarch
Provides: sysroot-%{_arch}-%{name}
# The files are not usable for execution, so do not provide nor
# require anything.
AutoReqProv: no

%description -n %sysroot_package_arch
This package contains development files for the glibc package
that can be installed across architectures.
%dnl %%{without bootstrap}
%endif

##############################################################################
# glibc32 (only for use in building GCC, not shipped)
##############################################################################
%ifarch x86_64
%package -n glibc32
Summary: The GNU libc libraries (32-bit)
Conflicts: glibc(x86-32)
%dnl The gcc package does not use ELF dependencies to install glibc32:
%dnl BuildRequires: (glibc32 or glibc-devel(%{__isa_name}-32))
%dnl Not generating the ELF dependencies for glibc32 makes it less likely
%dnl that the package is selected by accident over glibc.i686.
AutoReqProv: no

%description -n glibc32
This package is only used for internal building of multilib aware
packages, like gcc, due to a technical limitation in the distribution
build environment. Any package which needs both 32-bit and 64-bit
runtimes at the same time must install glibc32 (marked as a 64-bit
package) to access the 32-bit development files during a 64-bit build.

This package is not supported or intended for use outside of the
distribution build enviroment. Regular users can install both 32-bit and
64-bit runtimes and development files without any problems.

%endif

##############################################################################
# Prepare for the build.
##############################################################################
%prep
%autosetup -n %{glibcsrcdir} -p1

##############################################################################
# %%prep - Additional prep required...
##############################################################################
# Make benchmark scripts executable
chmod +x benchtests/scripts/*.py scripts/pylint

# Remove all files generated from patching.
find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

# Ensure timestamps on configure files are current to prevent
# regenerating them.
touch `find . -name configure`

# Ensure *-kw.h files are current to prevent regenerating them.
touch locale/programs/*-kw.h

# Verify that our locales table is compatible with the locales table
# in the spec file.
set +x
echo '%{lua: print_locale_pairs()}' > localedata/SUPPORTED.spec
set -x
python3 %{SOURCE11} localedata/SUPPORTED > localedata/SUPPORTED.glibc
diff -u \
  --label "spec file" localedata/SUPPORTED.spec \
  --label "glibc localedata/SUPPORTED" localedata/SUPPORTED.glibc
rm localedata/SUPPORTED.spec localedata/SUPPORTED.glibc

##############################################################################
# Build glibc...
##############################################################################
%build
# Log osystem information
uname -a
LD_SHOW_AUXV=1 /bin/true
ld.so --list-diagnostics || true
ld.so --list-tunables || true
cat /proc/cpuinfo
cat /proc/sysinfo 2>/dev/null || true
cat /proc/meminfo
df

# Propgate select compiler flags from redhat-rpm-config.  These flags
# are target-dependent, so we use only those which are specified in
# redhat-rpm-config.  We keep the -m32/-m32/-m64 flags to support
# multilib builds.

%{lua:
-- Split the string argument into keys of an associate array.
-- The values are set to true.
local function string_to_array(s)
    local result = {}
    for e in string.gmatch(s, "%S+") do
        result[e] = true
    end
    return result
end

local inherit_flags = {}

-- These flags are put into the CC and CXX arguments to configure.
-- Alternate builds do not use the flags listed here, only the main build does.
inherit_flags.cc_main = string_to_array [[
-march=armv8-a+lse
-march=armv8.1-a
-march=haswell
-march=i686
-march=x86-64
-march=x86-64-v2
-march=x86-64-v3
-march=x86-64-v4
-march=z13
-march=z14
-march=z15
-march=zEC12
-mcpu=power10
-mcpu=power8
-mcpu=power9
-mtune=generic
-mtune=power10
-mtune=power8
-mtune=power9
-mtune=z13
-mtune=z14
-mtune=z15
-mtune=zEC12
]]

-- Like inherit_flags_cc_main, but also used for alternate builds.
inherit_flags.cc = string_to_array [[
-m31
-m32
-m64
]]

-- These flags are passed through CFLAGS and CXXFLAGS.
inherit_flags.cflags = string_to_array [[
-O2
-O3
-Wall
-Wp,-D_GLIBCXX_ASSERTIONS
-fasynchronous-unwind-tables
-fno-omit-frame-pointer
-fstack-clash-protection
-funwind-tables
-g
-mbackchain
-mbranch-protection=standard
-mfpmath=sse
-mno-omit-leaf-frame-pointer
-msse2
-mstackrealign
-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1
]]

-- Iterate over the build_cflags RPM variable and emit a shell
-- variable that contains the inherited flags of the indicated variant.
local function shell_build_flags(variant)
    local result = {}
    local inherit = assert(inherit_flags[variant])
    for f in string.gmatch(rpm.expand("%build_cflags"), "%S+") do
        if inherit[f] then
	    result[#result + 1] = f
	end
    end
    print("glibc_flags_" .. variant .. "=\"" .. table.concat(result, " ")
          .. "\"\n")
end

shell_build_flags('cc_main') -- Set $glibc_flags_cc_main.
shell_build_flags('cc') -- Set $glibc_flags_cc.
shell_build_flags('cflags') -- Set $glibc_flags_cflags.
}

%if 0%{?_annotated_build} > 0
# libc_nonshared.a cannot be built with the default hardening flags
# because the glibc build system is incompatible with
# -D_FORTIFY_SOURCE.  The object files need to be marked as to be
# skipped in annobin annotations.  (The -specs= variant of activating
# annobin does not work here because of flag ordering issues.)
# See <https://bugzilla.redhat.com/show_bug.cgi?id=1668822>.
BuildFlagsNonshared="-fplugin=annobin -fplugin-arg-annobin-disable -Wa,--generate-missing-build-notes=yes"
%endif

# Special flag to enable annobin annotations for statically linked
# assembler code.  Needs to be passed to make; not preserved by
# configure.
%global glibc_make_flags_as ASFLAGS="-g -Wa,--generate-missing-build-notes=yes"
%global glibc_make_flags %{glibc_make_flags_as}

##############################################################################
# %%build - Generic options.
##############################################################################
EnableKernel="--enable-kernel=%{enablekernel}"

##############################################################################
# build()
#	Build glibc in the directory $1, passing the rest of the arguments
#	as additional configure arguments.  Several
#	global values are used to determine build flags, kernel version,
#	system tap support, etc.
##############################################################################
build()
{
	local builddir=$1
	shift
	rm -rf $builddir
	mkdir $builddir
	pushd $builddir
	../configure "$@" \
		--prefix=%{_prefix} \
		--with-headers=%{_prefix}/include $EnableKernel \
		--with-nonshared-cflags="$BuildFlagsNonshared" \
		--enable-bind-now \
		--build=%{target} \
		--enable-stack-protector=strong \
		--enable-systemtap \
%ifarch %{ix86}
		--disable-multi-arch \
%endif
%if %{without werror}
		--disable-werror \
%endif
		--disable-profile \
%if %{with bootstrap}
		--without-selinux \
%endif
%ifarch aarch64
		--enable-memory-tagging \
%endif
		--disable-crypt \
	        --disable-build-nscd \
	        --disable-nscd \
		--enable-fortify-source \
		--disable-sframe \
		|| { cat config.log; false; }

	# We enable DT_GNU_HASH and DT_HASH for ld.so and DSOs to improve
	# compatibility with applications that expect DT_HASH e.g. Epic Games
	# Easy Anti-Cheat.  This is temporary as applications move to
	# supporting only DT_GNU_HASH.  This was initially enabled in Fedora
	# 37.  We must use 'env' because it is the only way to pass, via the
	# environment, two variables that set the initial Makefile values for
	# LDFLAGS used to build shared objects and the dynamic loader.
	env LDFLAGS.so="-Wl,--hash-style=both" \
		LDFLAGS-rtld="-Wl,--hash-style=both" \
		%make_build -r %{glibc_make_flags}
	popd
}

%ifarch x86_64
# Build for the glibc32 package.
build build-%{target}-32 \
  CC="gcc -m32" \
  CXX="g++ -m32" \
  CFLAGS="${glibc_flags_cflags/-m64/-m32}" \
  --host=i686-linux-gnu \
%dnl There is no libgcc_s.so.1, but building support/ requires it.
  --disable-libsupport \
#
%endif

# Default set of compiler options.
build build-%{target} \
  CC="gcc $glibc_flags_cc $glibc_flags_cc_main" \
  CXX="g++ $glibc_flags_cc $glibc_flags_cc_main" \
  CFLAGS="$glibc_flags_cflags" \
  %{?glibc_rtld_early_cflags:--with-rtld-early-cflags=%glibc_rtld_early_cflags} \
%ifarch x86_64
  --enable-cet \
%endif
#

# POWER10 build variant.
%if %{buildpower10}
build build-%{target}-power10 \
  CC="gcc $glibc_flags_cc" \
  CXX="g++ $glibc_flags_cc" \
  CFLAGS="$glibc_flags_cflags" \
  --with-cpu=power10 \
#
%endif


##############################################################################
# Install glibc...
##############################################################################
%install

# The built glibc is installed into a subdirectory of $RPM_BUILD_ROOT.
# For a system glibc that subdirectory is "/" (the root of the filesystem).
# This is called a sysroot (system root) and can be changed if we have a
# distribution that supports multiple installed glibc versions.
%global glibc_sysroot $RPM_BUILD_ROOT

# Create symbolic links for Features/UsrMove (aka UsrMerge, MoveToUsr).
# See below: Remove UsrMove symbolic links.
usrmove_file_names="bin lib lib64 sbin"
for d in $usrmove_file_names ; do
    mkdir -p "%{glibc_sysroot}/usr/$d"
    ln -s "usr/$d" "%{glibc_sysroot}/$d"
done

%ifarch x86_64
# Install for the glibc32 package.
pushd build-%{target}-32
%make_build install_root=%{glibc_sysroot} install
popd
pushd %{glibc_sysroot}
rm -rf etc var usr/bin usr/lib/gconv usr/libexec usr/sbin usr/share
rm -f lib/libnss_db* lib/libnss_hesiod* lib/libnsl* usr/lib/libnsl* usr/lib/libnss*
rm usr/lib/libc_malloc_debug.so
strip -g usr/lib/*.o
popd
mkdir glibc32-headers
cp -a %{glibc_sysroot}%{_includedir} glibc32-headers
%endif

# Build and install:
pushd build-%{target}
%make_build install_root=%{glibc_sysroot} install
%make_build install_root=%{glibc_sysroot} \
	install-locale-files -C ../localedata objdir=`pwd`
popd
# Locale creation via install-locale-files does not group identical files
# via hardlinks, so we must group them ourselves.
hardlink -c %{glibc_sysroot}/usr/lib/locale

%ifarch x86_64
# Verify that there are no unexpected differences in the header files common
# between i386 and x86_64.
diff -ur %{glibc_sysroot}%{_includedir} glibc32-headers/include \
     > glibc-32-64.diff || true
if test -s  glibc-32-64.diff ; then
    if test $(grep -v '^Only in ' glibc-32-64.diff | wc -l) -ne 0; then
	: Unexpected header file differences
	exit 1
    fi
else
    : Missing additional stubs header files.
fi
rm glibc-32-64.diff
rm -rf glibc32-headers
%endif

%if %{glibc_autorequires}
mkdir -p %{glibc_sysroot}/%{_rpmconfigdir} %{glibc_sysroot}/%{_fileattrsdir}
sed < %{SOURCE3} \
    -e s/@VERSION@/%{version}/ \
    -e s/@RELEASE@/%{baserelease}/ \
    -e s/@SYMVER@/%{glibc_autorequires_symver}/ \
    > %{glibc_sysroot}/%{_rpmconfigdir}/glibc.req
cp %{SOURCE4} %{glibc_sysroot}/%{_fileattrsdir}/glibc.attr
%endif

# Implement Changes/Unify_bin_and_sbin.
%if "%{_sbindir}" == "%{_bindir}"
mv %{glibc_sysroot}/usr/sbin/{iconvconfig,zic} %{glibc_sysroot}/%{_bindir}/
%endif

# install_different:
#	Install all core libraries into DESTDIR/SUBDIR. Either the file is
#	installed as a copy or a symlink to the default install (if it is the
#	same). The path SUBDIR_UP is the prefix used to go from
#	DESTDIR/SUBDIR to the default installed libraries e.g.
#	ln -s SUBDIR_UP/foo.so DESTDIR/SUBDIR/foo.so.
#	When you call this function it is expected that you are in the root
#	of the build directory, and that the default build directory is:
#	"../build-%{target}" (relatively).
#	The primary use of this function is to install alternate runtimes
#	into the build directory and avoid duplicating this code for each
#	runtime.
install_different()
{
	local lib libbase libbaseso dlib
	local destdir="$1"
	local subdir="$2"
	local subdir_up="$3"
	local libdestdir="$destdir/$subdir"
	# All three arguments must be non-zero paths.
	if ! [ "$destdir" \
	       -a "$subdir" \
	       -a "$subdir_up" ]; then
		echo "One of the arguments to install_different was emtpy."
		exit 1
	fi
	# Create the destination directory and the multilib directory.
	mkdir -p "$destdir"
	mkdir -p "$libdestdir"
	# Walk all of the libraries we installed...
	for lib in libc math/libm
	do
		libbase=${lib#*/}
		# Take care that `libbaseso' has a * that needs expanding so
		# take care with quoting.
		libbaseso=$(basename %{glibc_sysroot}/%{_libdir}/${libbase}.so.*)
		# Only install if different from default build library.
		if cmp -s ${lib}.so ../build-%{target}/${lib}.so; then
			ln -sf "$subdir_up"/$libbaseso $libdestdir/$libbaseso
		else
			cp -a ${lib}.so $libdestdir/$libbaseso
		fi
	done
}

%if %{buildpower10}
pushd build-%{target}-power10
install_different "$RPM_BUILD_ROOT/%{_libdir}/glibc-hwcaps" power10 ..
popd
%endif


##############################################################################
# Move files to the expected location
##############################################################################

# On riscv64 libraries end up installed into the lp64d/ subdirectory
# by default, but in Fedora that's a compatibility symlink (owned by
# the filesystem package) that we don't want to show up in paths.
# Let's move everything out.
%ifarch riscv64
mv %{glibc_sysroot}%{_libdir}/lp64d/* %{glibc_sysroot}/%{_libdir}/
rm -rf %{glibc_sysroot}%{_libdir}/lp64d/
%endif

##############################################################################
# Remove the files we don't want to distribute
##############################################################################

# Remove the libNoVersion files.
# XXX: This looks like a bug in glibc that accidentally installed these
#      wrong files. We probably don't need this today.
rm -f %{glibc_sysroot}/%{_libdir}/libNoVersion*

# Remove the old nss modules.
rm -f %{glibc_sysroot}%{_libdir}/libnss1-*
rm -f %{glibc_sysroot}%{_libdir}/libnss-*.so.1

# This statically linked binary is no longer necessary in a world where
# the default Fedora install uses an initramfs, and further we have rpm-ostree
# which captures the whole userspace FS tree.
# Further, see https://github.com/projectatomic/rpm-ostree/pull/1173#issuecomment-355014583
rm -f %{glibc_sysroot}/{usr/,}sbin/sln

##############################################################################
# Remove separate sbin directory
##############################################################################

# 'make install' insists on creating a separate /usr/sbin directory,
# Instead of fighting with this, just move things to the right location.
%if "%{_sbindir}" == "%{_bindir}"
mv "%{glibc_sysroot}/usr/sbin/"* "%{glibc_sysroot}/usr/bin/"
rmdir "%{glibc_sysroot}/usr/sbin"
%endif

######################################################################
# Run ldconfig to create all the symbolic links we need
######################################################################

# Note: This has to happen before creating /etc/ld.so.conf.

mkdir -p %{glibc_sysroot}/var/cache/ldconfig
truncate -s 0 %{glibc_sysroot}/var/cache/ldconfig/aux-cache

# ldconfig is statically linked, so we can use the new version.
%{glibc_sysroot}/%{_sbindir}/ldconfig -N -r %{glibc_sysroot}

##############################################################################
# Install info files
##############################################################################

%if %{with docs}
# Move the info files if glibc installed them into the wrong location.
if [ -d %{glibc_sysroot}%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p %{glibc_sysroot}%{_infodir}
  mv -f %{glibc_sysroot}%{_prefix}/info/* %{glibc_sysroot}%{_infodir}
  rm -rf %{glibc_sysroot}%{_prefix}/info
fi

# Compress all of the info files.
gzip -9nvf %{glibc_sysroot}%{_infodir}/libc*

# Copy the debugger interface documentation over to the right location
mkdir -p %{glibc_sysroot}%{_docdir}/glibc
cp elf/rtld-debugger-interface.txt %{glibc_sysroot}%{_docdir}/glibc
cp posix/gai.conf %{glibc_sysroot}%{_docdir}/glibc
%else
rm -f %{glibc_sysroot}%{_infodir}/dir
rm -f %{glibc_sysroot}%{_infodir}/libc.info*
%endif

##############################################################################
# Create locale sub-package file lists
##############################################################################

olddir=`pwd`
pushd %{glibc_sysroot}%{_prefix}/lib/locale
rm -f locale-archive
$olddir/build-%{target}/elf/ld.so \
        --library-path $olddir/build-%{target}/ \
        $olddir/build-%{target}/locale/localedef \
	--alias-file=$olddir/intl/locale.alias \
        --prefix %{glibc_sysroot} --add-to-archive \
        %locale_rx
# Historically, glibc-all-langpacks deleted the file on updates (sic),
# so we need to restore it in the posttrans scriptlet (like the old
# glibc-all-langpacks versions)
ln locale-archive locale-archive.real

# Almost half the LC_CTYPE files in langpacks are identical to the C.utf8
# variant which is installed by default.  When we keep them as hardlinks,
# each langpack ends up retaining a copy.  If we convert these to symbolic
# links instead, we save ~350K each when they get installed that way.
#
# To simplify testing, do this for LC_NAME and LC_NUMERIC as well,
# although the savings are minimal.  (It is not clear what is smaller:
# multiple short symbolic links, or one file hard linked into multiple
# directories.)
pushd %{glibc_sysroot}/usr/lib/locale
for k in CTYPE NAME NUMERIC; do
  for f in $(find %locale_rx -samefile C.utf8/LC_$k); do
    rm $f && ln -s ../C.utf8/LC_$k $f
  done
done
popd

# Create the file lists for the language specific sub-packages:
for i in %locale_rx 
do
    lang=${i%%_*}
    if [ ! -e langpack-${lang}.filelist ]; then
        echo "%dir %{_prefix}/lib/locale" >> langpack-${lang}.filelist
    fi
    echo "%dir  %{_prefix}/lib/locale/$i" >> langpack-${lang}.filelist
    echo "%{_prefix}/lib/locale/$i/*" >> langpack-${lang}.filelist
done
popd
pushd %{glibc_sysroot}%{_prefix}/share/locale
for i in */LC_MESSAGES/libc.mo
do
    locale=${i%%%%/*}
    lang=${locale%%%%_*}
    echo "%lang($lang) %{_prefix}/share/locale/${i}" \
         >> %{glibc_sysroot}%{_prefix}/lib/locale/langpack-${lang}.filelist
done
popd
mv  %{glibc_sysroot}%{_prefix}/lib/locale/*.filelist .

##############################################################################
# Install configuration files for services
##############################################################################

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > %{glibc_sysroot}/etc/ld.so.conf
truncate -s 0 %{glibc_sysroot}/etc/ld.so.cache
chmod 644 %{glibc_sysroot}/etc/ld.so.conf
mkdir -p %{glibc_sysroot}/etc/ld.so.conf.d
truncate -s 0 %{glibc_sysroot}/etc/gai.conf

# Include %{_libdir}/gconv/gconv-modules.cache
truncate -s 0 %{glibc_sysroot}%{_libdir}/gconv/gconv-modules.cache
chmod 644 %{glibc_sysroot}%{_libdir}/gconv/gconv-modules.cache

# Remove any zoneinfo files; they are maintained by tzdata.
rm -rf %{glibc_sysroot}%{_prefix}/share/zoneinfo

# Make sure %config files have the same timestamp across multilib packages.
#
# XXX: Ideally ld.so.conf should have the timestamp of the spec file, but there
# doesn't seem to be any macro to give us that.  So we do the next best thing,
# which is to at least keep the timestamp consistent. The choice of using
# SOURCE0 is arbitrary.
touch -r %{SOURCE0} %{glibc_sysroot}/etc/ld.so.conf
touch -r inet/etc.rpc %{glibc_sysroot}/etc/rpc

%if %{with benchtests}
# Build benchmark binaries.  Ignore the output of the benchmark runs.
pushd build-%{target}
make BENCH_DURATION=1 bench-build
popd

# Copy over benchmark binaries.
mkdir -p %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests
cp $(find build-%{target}/benchtests -type f -executable) %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
# ... and the makefile.
for b in %{SOURCE1} %{SOURCE2}; do
	cp $b %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
done
# .. and finally, the comparison scripts.
cp benchtests/scripts/benchout.schema.json %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/compare_bench.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/import_bench.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/validate_benchout.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
%endif

# The #line directives gperf generates do not give the proper
# file name relative to the build directory.
pushd locale
ln -sf programs/*.gperf .
popd
pushd iconv
ln -sf ../locale/programs/charmap-kw.gperf .
popd

%if %{with docs}
# Remove the `dir' info-heirarchy file which will be maintained
# by the system as it adds info files to the install.
rm -f %{glibc_sysroot}%{_infodir}/dir
%endif

# Disallow linking against libc_malloc_debug.
rm %{glibc_sysroot}%{_libdir}/libc_malloc_debug.so

# Strip all of the installed object files.
strip -g %{glibc_sysroot}%{_libdir}/*.o

# The xtrace and memusage scripts have hard-coded paths that need to be
# translated to a correct set of paths using the $LIB token which is
# dynamically translated by ld.so as the default lib directory.
for i in %{glibc_sysroot}%{_prefix}/bin/{xtrace,memusage}; do
%if %{with bootstrap}
  test -w $i || continue
%endif
  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_libdir}/libpcprofile.so~' \
      -e 's~=/%{_lib}/libmemusage.so~=%{_libdir}/libmemusage.so~' \
      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
      -i $i
done

##############################################################################
# Build an empty libpthread_nonshared.a for compatiliby with applications
# that have old linker scripts that reference this file. We ship this only
# in compat-libpthread-nonshared sub-package.
##############################################################################
ar cr %{glibc_sysroot}%{_libdir}/libpthread_nonshared.a

# Remove UsrMove symbolic links.
# These should not end in the packaged contents.
# They are part of the filesystem package.
for d in $usrmove_file_names ; do
    rm "%{glibc_sysroot}/$d"
done

###############################################################################
# Sysroot package creation.
###############################################################################

%if %{without bootstrap}
mkdir -p %{glibc_sysroot}/%{sysroot_prefix}
pushd %{glibc_sysroot}/%{sysroot_prefix}
mkdir -p usr/lib usr/lib64

cp -a %{glibc_sysroot}/%{_prefix}/include usr/.
%ifarch x86_64
# 32-bit headers for glibc32 don't go in the sysroot.
rm usr/include/gnu/*-32.h
%endif
for lib in lib lib64;  do
%ifarch x86_64
    if [ "$lib" = "lib" ]; then
	# 32-bit libraries built for glibc32 don't go in the sysroot.
	continue
    fi
%endif
    for pfx in "" %{_prefix}/; do
	if test -d %{glibc_sysroot}/$pfx$lib ; then
	    # Implement UsrMove: everything goes into usr/$lib.  Only
	    # copy files directly in $lib.
	    find %{glibc_sysroot}/$pfx$lib -maxdepth 1 -type f \
		| xargs -I '{}' cp  '{}' usr/$lib/.
	    # Symbolic links need to be adjusted for UsrMove: They
	    # need to stay within the same directory.
	    for sl in `find %{glibc_sysroot}/$pfx$lib -maxdepth 1 -type l`; do
		set +x
		slbase=$(basename $sl)
		sltarget=$(basename $(readlink $sl))
		if ! test -r usr/$lib/$sltarget; then
		    echo "$sl: inferred $sltarget ($(readlink $sl)) missing"
		    exit 1
		fi
		set -x
		ln -sf $sltarget usr/$lib/$slbase
	    done
	fi
    done
done

# Workaround for the lack of a kernel sysroot package.  Copy the
# kernel headers into the sysroot.
rpm -ql kernel-headers | grep "^/usr/include" | while read f ; do
    if test -f "$f" ; then
        install -D "$f" "./$f"
    fi
done

# Remove the executable bit from files in the sysroot.  This prevents
# debuginfo extraction.
find -type f | xargs chmod a-x

# Use sysroot-relative paths in linker script.  Ignore symbolic links.
sed -e 's,\([^0-9a-zA-Z=*]/lib\),/usr/lib,g' \
    -e 's,\([^0-9a-zA-Z=*]\)/,\1/,g' \
    -i $(find -type f -name 'lib[cm].so')

popd
%dnl %%{without bootstrap}
%endif

##############################################################################
# Beyond this point in the install process we no longer modify the set of
# installed files.
##############################################################################

# Placement of files in subpackages is mostly controlled by the
# %%files section below.  There are some exceptions where a subset of
# files are put in one package and need to be elided from another
# package, and it's not possible to do this easily using explicit file
# lists or directory matching.  For these exceptions. .filelist file
# are created.

# Make the sorting below more consistent.
export LC_ALL=C

# `make_sysroot_filelist PATH FIND-ARGS LIST` writes %%files section
# lines for files and directories in the sysroot under PATH to the
# file LIST, with FIND-ARGS passed to the find command.  The output is
# passed through sort.
make_sysroot_filelist () {
  (
    find "%{glibc_sysroot}$1" \( -type f -o -type l \) $2 \
      -printf "$1/%%P\n" || true
    find "%{glibc_sysroot}$1" -type d $2 -printf "%%%%dir $1/%%P\n" || true
  ) | sort > "$3"
}

# `remove_from_filelist FILE1 FILE2` removes the lines from FILE1
# which are also in FILE2.  The lines must not contain tabs, and the
# file is sorted as a side effect.  The input files must be sorted
# according to the sort command.
remove_from_filelist () {
    comm -23 "$1" "$2" > "$1.tmp"
    mv "$1.tmp" "$1"
}

# `split_sysroot_file_list DIR FIND-ARGS REGEXP MAIN-LIST EXCEPTIONS-LIST`
# creates a list of files in the sysroot subdirectory # DIR.
# Files and directories are enumerated with the find command,
# passing FIND-ARGS as an extra argument.  Those output paths that
# match REGEXP (an POSIX extended regular expression; all whitespace
# in it is removed before matching) are put into EXCEPTIONS-LIST.  The
# remaining files are put into MAIN-LIST.
split_sysroot_file_list () {
  make_sysroot_filelist "$1" "$2" "$4"
  grep -E -e "$(printf %%s "$3" | tr -d '[:space:]')" < "$4" > "$5"
  remove_from_filelist "$4" "$5"
}

# The primary gconv converters are in the glibc package, the rest goes
# into glibc-gconv-extra.  The Z9 and Z900 subpatterns are for
# s390x-specific converters.  The -name clause skips over files
# that are not loadable gconv modules.
split_sysroot_file_list \
  %{_libdir}/gconv '-name *.so' \
  'gconv/
   (CP1252
   |ISO8859-15?
   |UNICODE
   |UTF-[0-9]+
   |ISO-8859-1_CP037_Z900
   |UTF(8|16)_UTF(16|32)_Z9
   )\.so$' \
  gconv-extra.filelist glibc.filelist

##############################################################################
# Run the glibc testsuite
##############################################################################
%check
%if %{with testsuite}

# Run the glibc tests. If any tests fail to build we exit %check with
# an error, otherwise we print the test failure list and the failed
# test output and continue.  Write to standard error to avoid
# synchronization issues with make and shell tracing output if
# standard output and standard error are different pipes.
run_tests () {
  # This hides a test suite build failure, which should be fatal.  We
  # check "Summary of test results:" below to verify that all tests
  # were built and run.
  %make_build check |& tee rpmbuild.check.log >&2
  test -n tests.sum
  if ! grep -Eq '^\s+=== Summary of results ===$' rpmbuild.check.log ; then
    echo "FAIL: test suite build of target: $(basename "$(pwd)")" >& 2
    exit 1
  fi
  set +x
  grep -v ^PASS: tests.sum > rpmbuild.tests.sum.not-passing || true
  if test -n rpmbuild.tests.sum.not-passing ; then
    echo ===================FAILED TESTS===================== >&2
    echo "Target: $(basename "$(pwd)")" >& 2
    cat rpmbuild.tests.sum.not-passing >&2
    while read failed_code failed_test ; do
      for suffix in out test-result ; do
        if test -e "$failed_test.$suffix"; then
	  echo >&2
          echo "=====$failed_code $failed_test.$suffix=====" >&2
          cat -- "$failed_test.$suffix" >&2
	  echo >&2
        fi
      done
    done <rpmbuild.tests.sum.not-passing
  fi

  # Unconditonally dump differences in the system call list.
  echo "* System call consistency checks:" >&2
  cat misc/tst-syscall-list.out >&2
  set -x
}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================

# Default libraries.
pushd build-%{target}
run_tests
popd

%if %{buildpower10}
# Run this test only if the server supports Power10 instructions.
if LD_SHOW_AUXV=1 /bin/true | grep -E "AT_HWCAP2:[^$]*arch_3_1" > /dev/null; then
  echo ====================TESTING -mcpu=power10=============
  pushd build-%{target}-power10
  run_tests
  popd
fi
%endif

echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr %{glibc_sysroot}%{_libdir}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr %{glibc_sysroot}%{_libdir}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

run_ldso="%{glibc_sysroot}/%{_prefix}%{glibc_ldso} --library-path %{glibc_sysroot}/%{_libdir}"

# Show the auxiliary vector as seen by the new library
# (even if we do not perform the valgrind test).
LD_SHOW_AUXV=1 $run_ldso /bin/true

%if 0%{?_enable_debug_packages}
# Finally, check if valgrind runs with the new glibc.
# We want to fail building if valgrind is not able to run with this glibc so
# that we can then coordinate with valgrind to get it fixed before we update
# glibc.
%if %{with valgrind}
$run_ldso /usr/bin/valgrind --error-exitcode=1 \
	$run_ldso /usr/bin/true
# true --help performs some memory allocations.
$run_ldso /usr/bin/valgrind --error-exitcode=1 \
	$run_ldso /usr/bin/true --help >/dev/null
%endif
%endif

%endif


%pre -p <lua>
-- Check that the running kernel is new enough
required = '%{enablekernel}'
rel = posix.uname("%r")
if rpm.vercmp(rel, required) < 0 then
  error("FATAL: kernel too old", 0)
end

-- (1) Remove multilib libraries from previous installs.
-- In order to support in-place upgrades, we must immediately remove
-- all platform directories before installing a new glibc
-- version.  RPM only deletes files removed by updates near the end
-- of the transaction.  If we did not remove all platform
-- directories here, they may be preferred by the dynamic linker
-- during the execution of subsequent RPM scriptlets, likely
-- resulting in process startup failures.

-- Full set of libraries glibc may install.
install_libs = { "anl", "BrokenLocale", "c", "dl", "m", "mvec",
		 "nss_compat", "nss_db", "nss_dns", "nss_files",
		 "nss_hesiod", "pthread", "resolv", "rt", "SegFault",
		 "thread_db", "util" }

-- We are going to remove these libraries. Generally speaking we remove
-- all core libraries in the multilib directory.
-- For the versioned install names, the version are [2.0,9.9*], so we
-- match "libc-2.0.so" and so on up to "libc-9.9*".
-- For the unversioned install names, we match the library plus ".so."
-- followed by digests.
remove_regexps = {}
for i = 1, #install_libs do
  -- Versioned install name.
  remove_regexps[#remove_regexps + 1] = ("lib" .. install_libs[i]
                                         .. "%%-[2-9]%%.[0-9]+%%.so$")
  -- Unversioned install name.
  remove_regexps[#remove_regexps + 1] = ("lib" .. install_libs[i]
                                         .. "%%.so%%.[0-9]+$")
end

-- Two exceptions:
remove_regexps[#install_libs + 1] = "libthread_db%%-1%%.0%%.so"
remove_regexps[#install_libs + 2] = "libSegFault%%.so"

-- We are going to search these directories.
local remove_dirs = { "%{_libdir}/i686",
		      "%{_libdir}/i686/nosegneg",
		      "%{_libdir}/power6",
		      "%{_libdir}/power7",
		      "%{_libdir}/power8",
		      "%{_libdir}/power9",
		    }

-- Add all the subdirectories of the glibc-hwcaps subdirectory.
repeat
  local iter = posix.files("%{_libdir}/glibc-hwcaps")
  if iter ~= nil then
    for entry in iter do
      if entry ~= "." and entry ~= ".." then
        local path = "%{_libdir}/glibc-hwcaps/" .. entry
        if posix.access(path .. "/.", "x") then
          remove_dirs[#remove_dirs + 1] = path
        end
      end
    end
  end
until true

-- Walk all the directories with files we need to remove...
for _, rdir in ipairs (remove_dirs) do
  if posix.access (rdir) then
    -- If the directory exists we look at all the files...
    local remove_files = posix.files (rdir)
    for rfile in remove_files do
      for _, rregexp in ipairs (remove_regexps) do
	-- Does it match the regexp?
	local dso = string.match (rfile, rregexp)
        if (dso ~= nil) then
	  -- Removing file...
	  os.remove (rdir .. '/' .. rfile)
	end
      end
    end
  end
end

%post -p <lua>
%glibc_post_funcs
-- (1) Update /etc/ld.so.conf
-- Next we update /etc/ld.so.conf to ensure that it starts with
-- a literal "include ld.so.conf.d/*.conf".

local ldsoconf = "/etc/ld.so.conf"
local ldsoconf_tmp = "/etc/glibc_post_upgrade.ld.so.conf"

if posix.access (ldsoconf) then

  -- We must have a "include ld.so.conf.d/*.conf" line.
  local have_include = false
  for line in io.lines (ldsoconf) do
    -- This must match, and we don't ignore whitespace.
    if string.match (line, "^include ld.so.conf.d/%%*%%.conf$") ~= nil then
      have_include = true
    end
  end

  if not have_include then
    -- Insert "include ld.so.conf.d/*.conf" line at the start of the
    -- file. We only support one of these post upgrades running at
    -- a time (temporary file name is fixed).
    local tmp_fd = io.open (ldsoconf_tmp, "w")
    if tmp_fd ~= nil then
      tmp_fd:write ("include ld.so.conf.d/*.conf\n")
      for line in io.lines (ldsoconf) do
        tmp_fd:write (line .. "\n")
      end
      tmp_fd:close ()
      local res = os.rename (ldsoconf_tmp, ldsoconf)
      if res == nil then
        io.stdout:write ("Error: Unable to update configuration file (rename).\n")
      end
    else
      io.stdout:write ("Error: Unable to update configuration file (open).\n")
    end
  end
end

-- (2) Rebuild ld.so.cache early.
-- If the format of the cache changes then we need to rebuild
-- the cache early to avoid any problems running binaries with
-- the new glibc.

call_ldconfig()

-- (3) Update gconv modules cache.
-- If the /usr/lib/gconv/gconv-modules.cache exists, then update it
-- with the latest set of modules that were just installed.
-- We assume that the cache is in _libdir/gconv and called
-- "gconv-modules.cache".

update_gconv_modules_cache()

-- (4) On upgrades, restart systemd if installed.  "systemctl -q" does
-- not suppress the error message (which is common in chroots), so
-- open-code rpm.execute with standard error suppressed.
if tonumber(arg[2]) >= 2
   and posix.access("%{_prefix}/bin/systemctl", "x")
then
  if rpm.spawn ~= nil then
    rpm.spawn ({"%{_prefix}/bin/systemctl", "daemon-reexec"},
               {stderr="/dev/null"})
  else
    local pid = posix.fork()
    if pid == 0 then
      posix.redirect2null(2)
      posix.exec("%{_prefix}/bin/systemctl", "daemon-reexec")
    elseif pid > 0 then
      posix.wait(pid)
    end
  end
end

%posttrans all-langpacks -e -p <lua>
-- The old glibc-all-langpacks postun scriptlet deleted the locale-archive
-- file, so we may have to resurrect it on upgrades.
local archive_path = "%{_prefix}/lib/locale/locale-archive"
local real_path = "%{_prefix}/lib/locale/locale-archive.real"
local stat_archive = posix.stat(archive_path)
local stat_real = posix.stat(real_path)
-- If the hard link was removed, restore it.
if stat_archive ~= nil and stat_real ~= nil
    and (stat_archive.ino ~= stat_real.ino
         or stat_archive.dev ~= stat_real.dev) then
  posix.unlink(archive_path)
  stat_archive = nil
end
-- If the file is gone, restore it.
if stat_archive == nil then
  posix.link(real_path, archive_path)
end
-- Remove .rpmsave file potentially created due to config file change.
local save_path = archive_path .. ".rpmsave"
if posix.access(save_path) then
  posix.unlink(save_path)
end

%post gconv-extra -p <lua>
%glibc_post_funcs
update_gconv_modules_cache ()

%postun gconv-extra -p <lua>
%glibc_post_funcs
update_gconv_modules_cache ()

%files -f glibc.filelist
%{_sbindir}/ldconfig
%{_sbindir}/iconvconfig
%{_libexecdir}/getconf
%{_prefix}%{glibc_ldso}
%{_libdir}/libBrokenLocale.so.1
%{_libdir}/libanl.so.1
%{_libdir}/libc.so.6
%{_libdir}/libdl.so.2
%{_libdir}/libm.so.6
%{_libdir}/libnss_compat.so.2
%{_libdir}/libnss_dns.so.2
%{_libdir}/libnss_files.so.2
%{_libdir}/libpthread.so.0
%{_libdir}/libresolv.so.2
%{_libdir}/librt.so.1
%{_libdir}/libthread_db.so.1
%{_libdir}/libutil.so.1
%{_libdir}/libpcprofile.so
%{_libdir}/audit
%if %{glibc_has_libmvec}
%{_libdir}/libmvec.so.1
%endif
%ifarch %{ix86}
# Needs to be in glibc.i686 so that glibc-utils.x86_64 can use it.
%{_libdir}/libmemusage.so
%{_libdir}/libc_malloc_debug.so.0
%endif
%if %{buildpower10}
%{_libdir}/glibc-hwcaps
%endif
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%verify(not md5 size mtime) %config(noreplace) /etc/rpc
%dir /etc/ld.so.conf.d
%dir %{_libdir}/gconv
%dir %{_libdir}/gconv/gconv-modules.d
%verify(not md5 size mtime) %config(noreplace) %{_libdir}/gconv/gconv-modules
%verify(not md5 size mtime) %{_libdir}/gconv/gconv-modules.cache
%ifarch s390x
%verify(not md5 size mtime) %config(noreplace) %{_libdir}/gconv/gconv-modules.d/gconv-modules-s390.conf
%endif
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/gai.conf
# If rpm doesn't support %license, then use %doc instead.
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB LICENSES

%files common
%{_bindir}/gencat
%{_bindir}/getconf
%{_bindir}/getent
%{_bindir}/iconv
%{_bindir}/ld.so
%{_bindir}/ldd
%{_bindir}/locale
%{_bindir}/localedef
%{_bindir}/pldd
%{_bindir}/sotruss
%{_bindir}/sprof
%{_bindir}/tzselect
%{_bindir}/zdump
%{_sbindir}/zic
%dir %{_datarootdir}/i18n
%dir %{_datarootdir}/i18n/locales
%dir %{_datarootdir}/i18n/charmaps
%dir %{_prefix}/lib/locale
%{_datarootdir}/locale/locale.alias
%{_prefix}/lib/locale/C.utf8

%files all-langpacks
%{_prefix}/lib/locale/locale-archive
%{_prefix}/lib/locale/locale-archive.real
%{_prefix}/share/locale/*/LC_MESSAGES/libc.mo

%files locale-source
%{_datarootdir}/i18n/locales
%{_datarootdir}/i18n/charmaps

%files devel
%{_includedir}/*
%if %{glibc_autorequires}
%attr(0755,root,root) %{_rpmconfigdir}/glibc.req
%{_fileattrsdir}/glibc.attr
%endif
%{_libdir}/*.o
%{_libdir}/libBrokenLocale.so
%{_libdir}/libanl.a
%{_libdir}/libanl.so
%{_libdir}/libc.so
%{_libdir}/libc_nonshared.a
%{_libdir}/libdl.a
%{_libdir}/libg.a
%{_libdir}/libm.so
%{_libdir}/libmcheck.a
%{_libdir}/libpthread.a
%{_libdir}/libresolv.so
%{_libdir}/librt.a
%{_libdir}/libthread_db.so
%{_libdir}/libutil.a
%if %{glibc_has_libnldbl}
%{_libdir}/libnldbl_nonshared.a
%endif
%if %{glibc_has_libmvec}
%{_libdir}/libmvec.so
%endif
%ifarch x86_64
# This files are included in the buildroot for glibc32 below.
%exclude %{_includedir}/gnu/lib-names-32.h
%exclude %{_includedir}/gnu/stubs-32.h
%endif

%if %{with docs}
%files doc
%{_datarootdir}/doc
%{_infodir}/*.info*
%endif

%files static
%{_libdir}/libBrokenLocale.a
%{_libdir}/libc.a
%{_libdir}/libm.a
%{_libdir}/libresolv.a
%if %{glibc_has_libmvec}
%{_libdir}/libm-%{version}.a
%{_libdir}/libmvec.a
%endif

%files utils
%if %{without bootstrap}
%{_bindir}/memusage
%{_bindir}/memusagestat
%endif
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/xtrace
%ifnarch %{ix86}
# Needs to be in glibc.i686 so that glibc-utils.x86_64 can use it.
%{_libdir}/libmemusage.so
%{_libdir}/libc_malloc_debug.so.0
%endif

%files -f gconv-extra.filelist gconv-extra
%verify(not md5 size mtime) %config(noreplace) %{_libdir}/gconv/gconv-modules.d/gconv-modules-extra.conf

%files -n nss_db
%{_bindir}/makedb
%{_libdir}/libnss_db.so.2
/var/db/Makefile
%files -n nss_hesiod
%{_libdir}/libnss_hesiod.so.2
%doc hesiod/README.hesiod
%files nss-devel
%{_libdir}/libnss_compat.so
%{_libdir}/libnss_db.so
%{_libdir}/libnss_hesiod.so

%files -n libnsl
%{_libdir}/libnsl.so.1

%if %{with benchtests}
%files benchtests
%{_libexecdir}/glibc-benchtests
%endif

%files -n compat-libpthread-nonshared
%{_libdir}/libpthread_nonshared.a

%if %{without bootstrap}
%files -n sysroot-%{_arch}-%{sysroot_dist}-glibc
%{sysroot_prefix}
%endif

%ifarch x86_64
%files -n glibc32
%{_includedir}/gnu/lib-names-32.h
%{_includedir}/gnu/stubs-32.h
%{_prefix}/lib/*.a
%{_prefix}/lib/*.o
%{_prefix}/lib/*.so*
%{_prefix}/lib/audit/*
%endif

%changelog
* Wed Feb 18 2026 Frédéric Bérat <fberat@redhat.com> - 2.42-10
- Auto-sync with upstream branch release/2.42/master,
  commit ebd45473f5421e0fced5ba2cde0f1aaa36e79b61:
- nss: Missing checks in __nss_configure_lookup, __nss_database_get (bug 28940) (Florian Weimer)
- Linux: In getlogin_r, use utmp fallback only for specific errors (Florian Weimer)
- nss: Introduce dedicated struct nss_database_for_fork type (Florian Weimer)
- Switch currency symbol for the bg_BG locale to euro (Florian Weimer)
- Remove patches already applied upstream:
  - glibc-rh2429016.patch

* Fri Jan 23 2026 Florian Weimer  <fweimer@redhat.com> - 2.42-9
- Ignore LD_PROFILE if LD_PROFILE_OUTPUT is not set (#2432405)

* Fri Jan 23 2026 Florian Weimer <fweimer@redhat.com> - 2.42-8
- Auto-sync with upstream branch release/2.42/master,
  commit cbf39c26b25801e9bc88499b4fd361ac172d4125:
- posix: Reset wordexp_t fields with WRDE_REUSE (CVE-2025-15281)
- resolv: Fix NSS DNS backend for getnetbyaddr (CVE-2026-0915)
- memalign: reinstate alignment overflow check (CVE-2026-0861)

* Tue Jan 13 2026 Florian Weimer  <fweimer@redhat.com> - 2.42-7
- Switch currency symbol for the bg_BG locale to euro (#2429016)

* Mon Jan 12 2026 Frédéric Bérat <fberat@redhat.com> - 2.42-6
- Auto-sync with upstream branch master,
  commit f122d0b4d145814869bf10c56db1d971bcba55c5:
- nptl: Optimize trylock for high cache contention workloads (BZ #33704) (Sunil K Pandey)
- support: Exit on consistency check failure in resolv_response_add_name (Florian Weimer)
- support: Fix FILE * leak in check_for_unshare_hints in test-container (Florian Weimer)
- sprof: fix -Wformat warnings on 32-bit hosts (Collin Funk)
- sprof: check pread size and offset for overflow (DJ Delorie)

* Mon Dec 15 2025 Frédéric Bérat <fberat@redhat.com> - 2.42-5
- Auto-sync with upstream branch master,
  commit b11411fe2ee7a8f3c3a2c1ee99c1729adb9a0efe:
- posix: Fix invalid flags test for p{write,read}v2 (Yury Khrustalev)
- ppc64le: Power 10 rawmemchr clobbers v20 (bug #33091) (Sachin Monga)
- ppc64le: Restore optimized strncmp for power10 (Sachin Monga)
- ppc64le: Restore optimized strcmp for power10 (Sachin Monga)
- AArch64: Fix and improve SVE pow(f) special cases (Pierre Blanchard)
- AArch64: fix SVE tanpi(f) [BZ #33642] (Pierre Blanchard)
- AArch64: Fix instability in AdvSIMD sinh (Joe Ramsay)
- AArch64: Fix instability in AdvSIMD tan (Joe Ramsay)
- AArch64: Optimise SVE scalar callbacks (Joe Ramsay)
- aarch64: fix includes in SME tests (Yury Khrustalev)
- aarch64: fix cfi directives around __libc_arm_za_disable (Yury Khrustalev)
- x86: fix wmemset ifunc stray '!' (bug 33542) (Jiamei Xie)
- aarch64: tests for SME (Yury Khrustalev)
- aarch64: clear ZA state of SME before clone and clone3 syscalls (Yury Khrustalev)
- aarch64: define macro for calling __libc_arm_za_disable (Yury Khrustalev)
- x86: Detect Intel Nova Lake Processor (Sunil K Pandey)
- x86: Detect Intel Wildcat Lake Processor (Sunil K Pandey)
- nptl: Fix MADV_GUARD_INSTALL logic for thread without guard page (BZ 33356) (Adhemerval Zanella)
- nss: Group merge does not react to ERANGE during merge (bug 33361) (Florian Weimer)
- libio: Define AT_RENAME_* with the same tokens as Linux (Florian Weimer)
- AArch64: Fix SVE powf routine [BZ #33299] (Pierre Blanchard)
- i386: Also add GLIBC_ABI_GNU2_TLS version [BZ #33129] (H.J. Lu)

* Tue Aug 19 2025 Florian Weimer <fweimer@redhat.com> - 2.42-4
- Add marker symbol versions GLIBC_ABI_DT_X86_64_PLT, GLIBC_ABI_GNU2_TLS,
  GLIBC_ABI_GNU_TLS, following upstream.
- Auto-sync with upstream branch release/2.42/master,
  commit 7a8f3c6ee4b565a02da4ba0dad9aaeaeed4639ce:
- x86-64: Add GLIBC_ABI_DT_X86_64_PLT [BZ #33212]
- x86-64: Add GLIBC_ABI_GNU2_TLS version [BZ #33129]
- i386: Add GLIBC_ABI_GNU_TLS version [BZ #33221]
- Use TLS initial-exec model for __libc_tsd_CTYPE_* thread variables [BZ #33234]
- malloc: Fix checking for small negative values of tcache_key
- malloc: Make sure tcache_key is odd enough
- malloc: Fix MAX_TCACHE_SMALL_SIZE
- malloc: Remove redundant NULL check

* Fri Aug 08 2025 Frédéric Bérat <fberat@redhat.com> - 2.42-3
- Auto-sync with upstream branch release/2.42/master,
  commit c5476b7907d01207ede6bf57b26cef151b601f35:
- hurd: support: Fix running SGID tests
- Revert "tst-freopen4-main.c: Call support_capture_subprocess with chroot"
- tst-env-setuid: Delete LD_DEBUG_OUTPUT output
- tst-freopen4-main.c: Call support_capture_subprocess with chroot
- tst-fopen-threaded.c: Delete temporary file
- Delete temporary files in support_subprocess
- nptl: Fix SYSCALL_CANCEL for return values larger than INT_MAX (BZ 33245)

* Fri Aug 01 2025 Florian Weimer <fweimer@redhat.com> - 2.42-2
- Auto-sync with upstream branch release/2.42/master,
  commit 5e298d2d937b6da06500478be956abeb24357e05:
- elf: Handle ld.so with LOAD segment gaps in _dl_find_object (bug 31943)
- elf: Extract rtld_setup_phdr function from dl_main
- stdlib: resolve a double lock init issue after fork [BZ #32994]

* Wed Jul 30 2025 Florian Weimer <fweimer@redhat.com> - 2.42-1
- Drop 0001-Revert-Linux-Keep-termios-ioctl-constants-strictly-i.patch,
  merged upstream.
- Auto-sync with upstream branch release/2.42/master,
  commit bc13db73937730401d592b33092db6df806d193e:
- inet-fortified: fix namespace violation (bug 33227)
- Bump version number to 2.42
- math: Update auto-libm-tests-in with ldbl-128ibm compoundn/pown failures
- INSTALL: Update newest tested binutils version
- elf: Compile _dl_debug_state separately (bug 33224)
- sframe: Add support for SFRAME_F_FDE_FUNC_START_PCREL flag
- Disable SFrame support by default
- math: xfail some pown and compoundn tests for ibm128-libgcc
- posix: Fix double-free after allocation failure in regcomp (bug 33185)
- Revert "Linux: Keep termios ioctl constants strictly internal"
- termios: manual: document the SPEED_MAX and BAUD_MAX constants
- termios: SPEED_MAX and BAUD_MAX constants
- termios: move the baud_t interface from __USE_MISC to __USE_GNU
- termios: manual: improve the explanation of various tty concepts
- termios: manual: remove duplicate cfgetospeed() definition
- termios: manual: fix typo: tcsettattr -> tcsetattr
- elf: Initialize GLRO (dl_read_only_area) after static dlopen (bug 33139)
- x86-64: Properly compile ISA optimized modf and modff
- x86-64: Compile ISA versions of modf/modff with -fno-stack-protector
- iconv: iconv -o should not create executable files (bug 33164)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.9000-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Adam Williamson <awilliam@redhat.com> - 2.41.9000-23
- Revert "Linux: Keep termios ioctl constants strictly internal" to fix wine build

* Fri Jul 18 2025 Arjun Shankar <arjun@redhat.com> - 2.41.9000-22
- Build without SFrame stack trace format information

* Thu Jul 17 2025 Arjun Shankar <arjun@redhat.com> - 2.41.9000-21
- Auto-sync with upstream branch master,
  commit 0263528f8dd60cf58976e2d516b7c9edb16ae6f8:
- malloc: fix definition for MAX_TCACHE_SMALL_SIZE
- SFrame: Add tests that uses DWARF backtracer
- configure: Add --enable-sframe option
- elf: Add SFrame stack tracing
- aarch64: Add SFrame support for aarch64 architecture
- x86: Add SFrame support for x86 architecture
- elf: Add SFrame support to _dl_find_object function
- x86_64: Optimize modf/modff for x86_64-v2
- Linux: Keep termios ioctl constants strictly internal
- termios: Move isatty, __isatty_nostatus from io
- termios: Reflow and sort Makefile
- Remove termios2 ioctl defintions from public headers
- elf: Remove now pointless empty ld.so.conf files in single tests
- support: Always run ldconfig in containered tests
- Makefile: Add ld.so.conf with libgcc dir to testroot.pristine
- Makeconfig: Add libgcc directory to rtld-prefix search path
- Mark support for lock elision as deprecated.
- x86: Avoid vector/r16-r31 registers and memcpy/memset in mcount_internal
- fstat: add test and documentation for an edge case.
- fstatat: extend tests and documentation
- elf: Restore support for _r_debug interpositions and copy relocations
- elf: Introduce _dl_debug_change_state
- elf: Introduce separate _r_debug_array variable
- manual: Remove '.info' suffix in manual names passed to @ref [BZ #32962].
- elf: Add DL_ADDRESS_WITHOUT_RELOC [BZ #33088]
- stdlib: Fix __libc_message_impl iovec size (BZ 32947)
- AArch64: Avoid memset ifunc in cpu-features.c [BZ #33112]
- malloc: Cleanup tcache_init()
- malloc: replace instances of __builtin_expect with __glibc_unlikely
- malloc: refactored aligned_OK and misaligned_chunk
- elf: Add missing DSO dependencies for tst-rtld-no-malloc-{audit,preload}
- powerpc: Remove modf optimization
- powerpc: Remove modff optimization
- manual: Add missing free to open_memstream example [BZ #27866]
- Linux: Convert '__close_nocancel_nostatus' to a standalone handler
- Linux: Fix '__close_nocancel_nostatus' clobbering 'errno' [BZ #33035]
- inet: Implement inet_ntoa on top of inet_ntop
- resolv: Optimize inet_ntop
- resolve: Proper indent resolv/inet_ntop.c
- benchtests: Add IPv6 inet_ntop benchmark
- benchtests: Add IPv4 inet_ntop benchmark
- posix: Fix fnmatch build with gcc-16
- powerpc: use .machine power10 in POWER10 assembler sources

* Sun Jun 22 2025 Florian Weimer  <fweimer@redhat.com> - 2.41.9000-20
- Remove glibc-rh2368545.patch, applied upstream.
- Auto-sync with upstream branch master,
  commit b3b0d0308c95d213f019b19c33abf1b06911f528:
- i386: Update ___tls_get_addr to preserve vector registers
- manual: Clarify renameat documentation
- posix: Add nonnull attribute to glob_pattern_p.
- math: Simplify and optimize modf implementation
- math: Simplify and optimize modff implementation
- AArch64: Improve codegen SVE log1p helper
- AArch64: Optimise SVE FP64 Hyperbolics
- AArch64: Optimize SVE exp functions
- Fix termios related targets
- malloc: Cleanup _mid_memalign
- aarch64: simplify calls to __libc_arm_za_disable in assembly
- aarch64: GCS: use internal struct in __alloc_gcs
- powerpc: Remove assembler workarounds
- malloc: Fix tests-malloc-largetcache tests
- Add TCPI_OPT_USEC_TS from Linux 6.14 and TCPI_OPT_TFO_CHILD from 6.15 to netinet/tcp.h.
- linux/termios: regression test for termios speed functions
- include/array_length.h: add array_foreach[_const] macros
- termios: unify the naming of the termios speed fields
- termios: add new baud_t interface, defined to be explicitly numeric
- manual: document all the termios Bxxx constants in the manual
- termios: merge the termios baud definitions
- hurd+generic/termios: make speed_t an unsigned int
- termios: change the generic cfsetspeed() to support arbitrary speeds
- hurd/termios: remove USE_OLD_TTY
- linux: implement arbitrary and split speeds in termios
- linux/termios/powerpc: deal with powerpc-unique ioctl emulation
- linux/ioctls: use <linux/sockios.h> for sockios ioctls
- io: replace local_isatty() with a proper function __isatty_nostatus()
- termios: make __tcsetattr() the internal interface

* Fri Jun 20 2025 Florian Weimer  <fweimer@redhat.com> - 2.41.9000-19
- Remove glibc-fedora-manual-dircategory.patch (#2252409)

* Fri Jun 20 2025 Florian Weimer  <fweimer@redhat.com> - 2.41.9000-18
- Remove glibc-fedora-linux-tcsetattr.patch (#2252406)

* Thu Jun 19 2025 Florian Weimer  <fweimer@redhat.com> - 2.41.9000-17
- langpacks: Use symlinks for LC_NAME, LC_NUMERIC files if possible (RHEL-97433)

* Tue Jun 17 2025 Florian Weimer  <fweimer@redhat.com> - 2.41.9000-16
- Replace glibc-rh2368545.patch with upstream fix under review.
- Auto-sync with upstream branch master,
  commit d1b27eeda3d92f33314e93537437cab11ddf4777:
- malloc: Sort tests-exclude-largetcache in Makefile
- ppc64le: Revert "powerpc: Optimized strcmp for power10" (CVE-2025-5702)
- ppc64le: Revert "powerpc : Add optimized memchr for POWER10" (Bug 33059)
- ppc64le: Revert "powerpc: Fix performance issues of strcmp power10" (CVE-2025-5702)
- ppc64le: Revert "powerpc: Optimized strncmp for power10" (CVE-2025-5745)
- malloc: add testing for large tcache support
- malloc: add tcache support for large chunk caching
- Always check lockf64 return value
- elf: Add optimization barrier for __ehdr_start and _end
- htl: move pthread_key_*, pthread_get/setspecific
- elf: Remove the unused _etext declaration
- io: Mark lockf() __wur [BZ #32800]
- benchtests: Improve modf benchtest
- benchtests: Add modff benchtest
- riscv: Correct __riscv_hwprobe function prototype [BZ #32932]
- resolv: Add test for getaddrinfo returning FQDN in ai_canonname
- aarch64: fix typo in sysdeps/aarch64/Makefile
- Advisory text for CVE-2025-5745
- Advisory text for CVE-2025-5702
- hurd: Make __getrandom_early_init call __mach_init
- x86: Avoid GLRO(dl_x86_cpu_features)
- manual: Add a comparative example of 'clock_nanosleep' use
- AArch64: Fix builderror with GCC 12.1/12.2
- Linux: Drop obsolete kernel support with `if_nameindex' and `if_nametoindex'
- aarch64: add __ifunc_hwcap function to be used in ifunc resolvers
- aarch64: add support for hwcap3,4
- manual: Document futimens and utimensat
- manual: Document unlinkat
- manual: Document renameat
- manual: Document mkdirat
- manual: Document faccessat
- manual: Expand Descriptor-Relative Access section
- Makefile: Avoid $(objpfx)/ in makefiles
- manual: Document error codes missing for 'inet_pton'
- manual: Document error codes missing for 'if_nametoindex'
- manual: Document error codes missing for 'if_indextoname'
- posix: fix building regex when _LIBC isn't defined
- localedata: Use the name North Macedonia.
- malloc: Count tcache entries downwards
- sparc: Fix argument passing to __libc_start_main (BZ 32981)
- localedata: Refer to Eswatini instead of Swaziland.
- sigaction: don't sign-extend sa_flags
- stdio-common: Add nonnull attribute to stdio_ext.h functions.
- elf: Fix UB on _dl_map_object_from_fd
- argp: Fix shift bug
- math: Remove i386 ilogb/ilogbf/llogb/llogbf
- math: Optimize float ilogb/llogb
- math: Remove UB and optimize double ilogbf
- math: Optimize double ilogb/llogb
- math: Remove UB and optimize double ilogb
- manual: Correct return value description of 'clock_nanosleep'
- nss: free dynarray buffer after parsing nsswitch.conf
- manual: Document clock_nanosleep
- manual: Fix invalid 'illegal' usage with 'nanosleep'
- manual: Fix duplicate 'consult' erratum
- localedata: Correct Persian collation rules description
- stdio-common: Correct 'sscanf' test feature wrapper description
- manual: Document error codes missing for 'inet_ntop'
- manual: Document error codes missing for 'socket'
- stdio-common: Consistently use 'num_digits_len' in 'vfscanf'
- Update syscall lists for Linux 6.15
- AArch64: Improve enabling of SVE for libmvec
- AArch64: Improve codegen in SVE log1p
- Use Linux 6.15 in build-many-glibcs.py
- manual: mention PKEY_UNRESTRICTED macro in the manual
- linux: use PKEY_UNRESTRICTED macro in tst-pkey
- misc: add PKEY_UNRESTRICTED macro
- generic: Add missing parameter name to __getrandom_early_init
- hurd: Avoid -Wfree-labels warning in _hurd_intr_rpc_mach_msg
- Update RISC-V relocations
- malloc: Fix malloc init order
- Move C warning flags from +gccwarn to +gccwarn-c
- doc: Add missing space in documentation of __TIMESIZE
- doc: Fix typos in documentation of _TIME_BITS
- Fix comment typo in libc-symbols.h
- Turn on -Wmissing-parameter-name by default if available
- manual: Document getopt_long_only with single letter options (bug 32980)

* Fri May 30 2025 Florian Weimer  <fweimer@redhat.com> - 2.41.9000-15
- malloc: Revert to the glibc-2.41.9000-6.fc43 version (#2368545)

* Mon May 26 2025 Florian Weimer <fweimer@redhat.com> - 2.41.9000-14
- Remove glibc-configure-disable-libsupport.patch, solved with
  upstream commit be61b9493d38032519e596f282f9695667402c8d
  ("support: Use unwinder in links-dso-program-c only with libgcc_s").
- Fix regression malloc initialization (#2368545)
- Auto-sync with upstream branch master,
  commit 4f4c4fcde76aedc1f5362a51d98ebb57a28fbce9:
- Turn on -Wfree-labels by default if available
- S390: Use cfi_val_offset instead of cfi_escape. 31bit part
- libmvec: Add inputs for asinpi(f), acospi(f), atanpi(f) and atan2pi(f)
- INSTALL: Regenerate with texinfo 7.2
- Fix error reporting (false negatives) in SGID tests
- manual: Use more inclusive language in comments.
- Makerules: Use 'original' instead of 'master' in source.
- gen-libm-test: Use 'original source' instead of 'master' in code.
- nss_test1: Use 'parametrized template' instead of 'master' in comment.
- linknamespace: Use 'ALLOWLIST' instead of 'WHITELIST' in code.
- posix: Use more inclusive language in test data.
- pylintrc: Remove obsolete ignore section and comments.
- support: Pick group in support_capture_subprogram_self_sgid if UID == 0
- ldbl-128: also disable lgammaf128_r builtin when building lgammal_r
- elf: Fix subprocess status handling for tst-dlopen-sgid (bug 32987)
- x86_64: Fix typo in ifunc-impl-list.c.
- elf: Test case for bug 32976 (CVE-2025-4802)
- support: Use const char * argument in support_capture_subprogram_self_sgid
- AArch64: Fix typo in math-vector.h
- Fix typos in ldbl-opt makefile
- AArch64: Cleanup SVE config and defines
- AArch64: Cleanup PAC and BTI
- AArch64: Implement AdvSIMD and SVE atan2pi/f
- AArch64: Implement AdvSIMD and SVE atanpi/f
- AArch64: Implement AdvSIMD and SVE asinpi/f
- AArch64: Implement AdvSIMD and SVE acospi/f
- AArch64: Optimize inverse trig functions
- Document CVE-2025-4802.
- ctype: Fallback initialization of TLS using relocations (bug 19341, bug 32483)
- Use proper extern declaration for _nl_C_LC_CTYPE_{class,toupper,tolower}
- Optimize __libc_tsd_* thread variable access
- Remove <libc-tsd.h>
- manual: add sched_getcpu()
- manual: Clarifications for listing directories
- manual: add remaining CPU_* macros
- powerpc: Remove check for -mabi=ibmlongdouble
- aarch64: update tests for SME
- aarch64: Disable ZA state of SME in setjmp and sigsetjmp
- benchtest: malloc tcache hotpath benchtest
- Implement C23 rootn.
- malloc: Improve performance of __libc_calloc
- S390: Use cfi_val_offset instead of cfi_escape.
- powerpc64le: Remove configure check for objcopy >= 2.26.
- Raise the minimum binutils version to 2.39

* Tue May 13 2025 DJ Delorie <dj@redhat.com> - 2.41.9000-13
- Auto-sync with upstream branch master,
  commit ad966bc4efd9e69cbbda2073121cc68f1deb9588.
- added benchtest inputs for log2l
- added benchtest inputs for expl
- aarch64: fix unwinding in longjmp
- added benchtest inputs for powl
- added benchtest inputs for fmal
- manual: fix typo for sched_[sg]etattr
- malloc: Improve malloc initialization
- Document all CLOCK_* values
- malloc: Improved double free detection in the tcache
- Correct spelling mistake in test file
- hurd: Make rename refuse trailing slashes [BZ #32570]
- Implement C23 compoundn
- hurd: Fix tst-stack2 test build on Hurd
- nss: remove undefined behavior and optimize getaddrinfo
- powerpc: Remove POWER7 strncasecmp optimization
- manual: add more pthread functions
- S390: Add new s390 platform z17.
- Correct test descriptors in libm-test-pown.inc
- malloc: Inline tcache_try_malloc

* Thu May 01 2025 Patsy Griffin <patsy@redhat.com> - 2.41.9000-12
- Auto-sync with upstream branch master,
  commit 84977600dace5a7cfcb0918e6757939fd4969839:
- math: Fix UB on sinpif (BZ 32925)
- math: Fix UB on erfcf (BZ 32924)
- math: Fix UB on cospif (BZ 32923)
- math: Fix UB on cbrtf (BZ 32922)
- math: Fix UB on sinhf (BZ 32921)
- math: Fix UB on logf (BZ 32920)
- math: Fix UB on coshf (BZ 32919)
- math: Fix UB on atanhf (BZ 32918)
- nptl: Fix pthread_getattr_np when modules with execstack are allowed (BZ 32897)
- RISC-V: Use builtin for ffs and ffsll while supported extension available
- stdio: Remove UB on printf_fp
- benchtest: Correct shell script related to bench-malloc-thread

* Fri Apr 25 2025 Florian Weimer <fweimer@redhat.com> - 2.41.9000-11
- Auto-sync with upstream branch master,
  commit e04afb71771710cdc6025fe95908f5f17de7b72d:
- linux/termio: remove <termio.h> and struct termio
- elf: tst-audit10: split AVX512F code into dedicated functions [BZ #32882]
- Add NT_ARM_GCS and NT_RISCV_TAGGED_ADDR_CTRL from Linux 6.13 to elf.h
- Add AT_* constants from Linux 6.12
- malloc: move tcache_init out of hot tcache paths
- aarch64: Add back non-temporal load/stores from oryon-1's memset
- aarch64: Add back non-temporal load/stores from oryon-1's memcpy
- malloc: Use tailcalls in __libc_free
- malloc: Inline tcache_free
- malloc: Improve free checks
- malloc: Inline _int_free_check
- malloc: Inline _int_free
- malloc: Move mmap code out of __libc_free hotpath
- manual/tunables: fix a trivial typo
- Fix spelling mistake "trucate" -> "truncate"
- Fix spelling mistake "suports" -> "supports"
- Fix spelling mistake "succsefully" -> "successfully"
- manual: Mention POSIX-1.2024 requires time_t to be 64 bit or wider.
- manual: Update standardization of getline and getdelim [BZ #32830]
- libio: Add test case for fflush

* Mon Apr 14 2025 Florian Weimer <fweimer@redhat.com> - 2.41.9000-10
- Auto-sync with upstream branch master,
  commit 7b47b3dd214c8ff2c699f13efe5533941be53635:
- libio: Synthesize ESPIPE error if lseek returns 0 after reading bytes
- x86: Detect Intel Diamond Rapids
- x86: Handle unknown Intel processor with default tuning
- conform: Add initial support for C23.
- x86: Add ARL/PTL/CWF model detection support
- timezone: Enhance tst-bz28707 diagnostics
- powerpc: Remove relocation cache flush code for power64

* Wed Apr 09 2025 Carlos O'Donell <carlos@redhat.com> - 2.41.9000-9
- Auto-sync with upstream branch master,
  commit 63c99cd50bc9c10f0692f7cb31f4c5f02ff526df:
- math: Fix up THREEp96 constant in expf128 [BZ #32411]
- elf: Extend glibc.rtld.execstack tunable to force executable stack (BZ 32653)
- stdlib: Implement C2Y uabs, ulabs, ullabs and uimaxabs
- stdio-common: In tst-setvbuf2, close helper thread descriptor only if opened
- Remove duplicates from binaries-shared-tests when creating make rules
- x86: Optimize xstate size calculation
- NEWS: update for GCC 12.1 requirement [BZ #32539]

* Thu Apr 03 2025 Arjun Shankar <arjun@redhat.com> - 2.41.9000-8
- Auto-sync with upstream branch master,
  aaf94ec804830e0e273cfb45d54f4a04ab778fe5:
- stdio: fix hurd link for tst-setvbuf2
- stdlib: Fix qsort memory leak if callback throws (BZ 32058)
- sysdeps: powerpc: restore -mlong-double-128 check
- stdio: Add more setvbuf tests
- add ptmx support to test-container
- Update syscall lists for Linux 6.14
- x86: Link tst-gnu2-tls2-x86-noxsave{,c,xsavec} with libpthread
- elf: Fix tst-origin build when toolchain defaults to --as-needed (BZ 32823)
- Raise the minimum GCC version to 12.1 [BZ #32539]
- Fix typo in comment
- manual: tidy the longopt.c example
- manual: Document functions adopted by POSIX.1-2024.
- aarch64: Fix _dl_tlsdesc_dynamic unwind for pac-ret (BZ 32612)
- x86: Use separate variable for TLSDESC XSAVE/XSAVEC state size (bug 32810)
- x86: Skip XSAVE state size reset if ISA level requires XSAVE
- malloc: Improve performance of __libc_malloc
- stdio-common: Reject real data w/o exponent digits in scanf [BZ #12701]
- stdio-common: Reject significand prefixes in scanf [BZ #12701]
- stdio-common: Reject integer prefixes in scanf [BZ #12701]
- stdio-common: Also reject exp char w/o significand in i18n scanf [BZ #13988]
- stdio-common: Add tests for formatted vsscanf input specifiers
- stdio-common: Add tests for formatted vfscanf input specifiers
- stdio-common: Add tests for formatted vscanf input specifiers
- stdio-common: Add tests for formatted sscanf input specifiers
- stdio-common: Add tests for formatted fscanf input specifiers
- stdio-common: Add scanf long double data for Intel/Motorola 80-bit format
- Implement C23 pown
- support: Use unwinder in links-dso-program-c only with libgcc_s
- malloc: Use __always_inline for simple functions
- linux: Fix integer overflow warnings when including <sys/mount.h> [BZ #32708]
- malloc: Use _int_free_chunk for remainders
- Use MPFR 4.2.2 and Linux 6.14 in build-many-glibcs.py
- stdio-common: Add scanf long double data for IBM 128-bit format
- stdio-common: Add scanf long double data for IEEE 754 binary64 format
- stdio-common: Add scanf long double data for IEEE 754 binary128 format
- stdio-common: Add scanf double data for IEEE 754 binary64 format
- stdio-common: Add scanf float data for IEEE 754 binary32 format
- stdio-common: Add scanf integer data for LP64 targets
- stdio-common: Add scanf integer data for ILP32 targets
- stdio-common: Add tests for formatted scanf input specifiers

* Tue Apr 01 2025 Andrea Bolognani <abologna@redhat.com> - 2.41.9000-7
- Update riscv64 handling (thanks David Abdurachmanov)

* Tue Mar 25 2025 Florian Weimer <fweimer@redhat.com> - 2.41.9000-6
- Add glibc-configure-disable-libsupport.patch and --disable-support
  to work around missing libgcc_s.so.1 in glibc32 build.
- Auto-sync with upstream branch master,
  commit 0544df4f4a9c6ce72de589e95f5bdadce8f103d0:
- mach: Use the host_get_time64 to replace the deprecated host_get_time for CLOCK_REALTIME when it's available
- aio_suspend64: Fix clock discrepancy [BZ #32795]
- Add _FORTIFY_SOURCE support for inet_pton
- Prepare inet_pton to be fortified
- Update kernel version to 6.13 in header constant tests
- support: Link links-dso-program-c with libgcc_s only if available
- elf: Use +nolink-deps to add make-only dependency for tst-origin
- Makeconfig: Support $(+nolink-deps) in link flags
- debug: Improve '%n' fortify detection (BZ 30932)
- Remove eloop-threshold.h
- malloc: missing initialization of tcache in _mid_memalign
- support: Link links-dso-program-c against libgcc_s
- Add _FORTIFY_SOURCE support for inet_ntop
- Add missing guards in include/arpa/inet.h
- Prepare inet_ntop to be fortified

* Thu Mar 20 2025 Florian Weimer <fweimer@redhat.com> - 2.41.9000-5
- Auto-sync with upstream branch master,
  commit c5113a838b28a8894da19794ca7a69c5ace959a3:
- add inputs giving large errors for rsqrt
- malloc: Improve csize2tidx
- elf: Fix tst-origin make rules
- AArch64: Optimize algorithm in users of SVE expf helper
- malloc: Improve arena_for_chunk()
- benchtests: Increase iterations of bench-malloc-simple
- elf: Fix tst-origin make rules
- htl: Make pthread_setcanceltype / state a cancellation point

* Fri Mar 14 2025 Florian Weimer <fweimer@redhat.com> - 2.41.9000-4
- Auto-sync with upstream branch master,
  commit 10af00f7a135c85796a9c4c75228358b8898da5c:
- tst-fopen-threaded: Only check EOF for failing read
- Implement C23 powr
- x86_64: Add atanh with FMA
- elf: Canonicalize $ORIGIN in an explicit ld.so invocation [BZ 25263]
- x86_64: Add sinh with FMA
- benchtests: Remove wrong snippet from 360cce0b06
- x86_64: Add tanh with FMA
- nptl: Check if thread is already terminated in sigcancel_handler (BZ 32782)
- nptl: PTHREAD_COND_INITIALIZER compatibility with pre-2.41 versions (bug 32786)
- getaddrinfo.c: support MPTCP (BZ #29609)
- math: Refactor how to use libm-test-ulps
- Update syscall lists for Linux 6.13
- Makefile: Clean up pthread_atfork integration
- nptl: Include <stdbool.h> in tst-pthread_gettid_np.c
- Linux: Add new test misc/tst-sched_setattr-thread
- Linux: Remove attribute access from sched_getattr (bug 32781)
- Linux: Add the pthread_gettid_np function (bug 27880)
- elf: Test dlopen (NULL, RTLD_LAZY) from an ELF constructor
- s390x: Regenerate ULPs.
- math: Remove an extra semicolon in math function declarations
- nptl: extend test coverage for sched_yield
- posix: Move environ helper variables next to environ definition (bug 32541)
- Implement C23 rsqrt

* Fri Mar 07 2025 Carlos O'Donell <carlos@redhat.com> - 2.41.9000-3
- Auto-sync with upstream branch master,
  commit ee3b1d15da412be19583085f81c220653b270c1f:
- Use binutils 2.44 branch and Linux 6.13 in build-many-glibcs.py
- elf: Fix handling of symbol versions which hash to zero (bug 29190)
- configure: Fix spelling of -Wl,--no-error-execstack option
- manual: Mark perror as MT-unsafe and update check-safety.sh
- elf: Check if __attribute__ ((aligned (65536))) is supported
- htl: Make __pthread_create_internal directly call __pthread_sigmask
- htl: Make __pthread_sigmask directly call __sigthreadmask
- hurd: Consolidate signal mask change
- static-pie: Skip the empty PT_LOAD segment at offset 0 [BZ #32763]
- sysdeps: linux: Add BTRFS_SUPER_MAGIC to pathconf
- linux: Prefix AT_HWCAP with 0x on LD_SHOW_AUXV
- Remove dl-procinfo.h
- powerpc: Remove unused dl-procinfo.h
- powerpc: Move cache geometry information to ld diagnostics
- powerpc: Move AT_HWCAP descriptions to ld diagnostics
- benchtests: Add random strlen benchmark
- benchtests: Improve large memcpy/memset benchmarks
- manual: Explain sched_yield semantics with different schedulers
- Pass -Wl,--no-error-execstack for tests where -Wl,-z,execstack is used [PR32717]
- malloc: Add integrity check to largebin nextsizes
- libio: Clean up fputc/putc comments
- htl: move pthread_once into libc
- Remove unused dl-procinfo.h
- LoongArch: Optimize f{max,min}imum_mag_num{,f}
- LoongArch: Optimize f{max,min}imum_num{,f}
- LoongArch: Optimize f{max,min}imum_mag{,f}
- LoongArch: Optimize f{max,min}imum{,f}
- AArch64: Use prefer_sve_ifuncs for SVE memset
- sysdeps/ieee754: Fix remainder sign of zero for FE_DOWNWARD (BZ #32711)
- math: Add optimization barrier to ensure a1 + u.d is not reused [BZ #30664]
- RISC-V: Fix IFUNC resolver cannot access gp pointer

* Tue Feb 25 2025 Arjun Shankar <arjun@redhat.com> - 2.41.9000-2
- Auto-sync with upstream branch master,
  commit 935563754bb5e1f16b9edb392d6c80c6827ddfca:
- AArch64: Remove LP64 and ILP32 ifdefs
- AArch64: Simplify lrint
- AArch64: Remove AARCH64_R macro
- AArch64: Cleanup pointer mangling
- AArch64: Remove PTR_REG defines
- AArch64: Remove PTR_ARG/SIZE_ARG defines
- stdlib: Add single-threaded fast path to rand()
- Increase the amount of data tested in stdio-common/tst-fwrite-pipe.c
- posix: Rewrite cpuset tests
- support: Add support_next_to_fault_before support function
- math: Fix `unknown type name '__float128'` for clang 3.4 to 3.8.1 (bug 32694)
- nptl: clear the whole rseq area before registration
- aarch64: Add GCS test with signal handler
- aarch64: Add GCS tests for dlopen
- aarch64: Add GCS tests for transitive dependencies
- aarch64: Add tests for Guarded Control Stack
- aarch64: Add configure checks for GCS support

* Thu Feb 20 2025 Carlos O'Donell <carlos@redhat.com> - 2.41.9000-1
- Auto-sync with upstream branch master,
  commit 6d24313e4a4098f7c469e119784bfbbfdb1ec749.
- manual: Mark setlogmask as AS-unsafe and AC-unsafe.
- AArch64: Add SVE memset
- x86 (__HAVE_FLOAT128): Defined to 0 for Intel SYCL compiler [BZ #32723]
- manual: Document setlogmask as MT-safe.
- math: Consolidate acosf and asinf internal tables
- math: Consolidate acospif and asinpif internal tables
- math: Consolidate cospif and sinpif internal tables
- htl: don't export __pthread_default_rwlockattr anymore.
- htl: move pthread_rwlock_init into libc.
- htl: move pthread_rwlock_destroy into libc.
- htl: move pthread_rwlock_{rdlock, timedrdlock, timedwrlock, wrlock, clockrdlock, clockwrlock} into libc.
- htl: move pthread_rwlock_unlock into libc.
- htl: move pthread_rwlock_tryrdlock, pthread_rwlock_trywrlock into libc.
- htl: move pthread_rwlockattr_getpshared, pthread_rwlockattr_setpshared into libc.
- htl: move pthread_rwlockattr_destroy into libc.
- htl: move pthread_rwlockattr_init into libc.
- htl: move __pthread_default_rwlockattr into libc.
- Fix tst-aarch64-pkey to handle ENOSPC as not supported
- Increase the amount of data tested in stdio-common/tst-fwrite-bz29459.c
- elf: Keep using minimal malloc after early DTV resize (bug 32412)
- libio: Initialize _total_written for all kinds of streams
- malloc: Add size check when moving fastbin->tcache
- nss: Improve network number parsers (bz 32573, 32575)
- nptl: Remove unused __g_refs comment.
- advisories: Fix up GLIBC-SA-2025-0001
- AArch64: Improve codegen for SVE powf
- AArch64: Improve codegen for SVE pow
- AArch64: Improve codegen for SVE erfcf
- Aarch64: Improve codegen in SVE exp and users, and update expf_inline
- Aarch64: Improve codegen in SVE asinh
- math: Improve layout of exp/exp10 data
- assert: Add test for CVE-2025-0395
- math: Consolidate coshf and sinhf internal tables
- math: Consolidate acoshf and asinhf internal tables
- math: Use tanpif from CORE-MATH
- math: Use sinpif from CORE-MATH
- math: Use cospif from CORE-MATH
- math: Use atanpif from CORE-MATH
- math: Use atan2pif from CORE-MATH
- math: Use asinpif from CORE-MATH
- math: Use acospif from CORE-MATH
- benchtests: Add tanpif
- benchtests: Add sinpif
- benchtests: Add cospif
- benchtests: Add atanpif
- benchtests: Add atan2pif
- benchtests: Add asinpif
- benchtests: Add acospif
- hurd: Replace char foo[1024] with string_t
- hurd: Drop useless buffer initialization in ttyname*
- mig_strncpy: ensure destination string is null terminated
- htl: stop exporting __pthread_default_barrierattr.
- htl: move pthread_barrier_wait into libc.
- htl: move pthread_barrier_init into libc.
- htl: move pthread_barrier_destroy into libc.
- htl: move pthread_barrierattr_getpshared, pthread_barrierattr_setpshared into libc.
- htl: move pthread_barrierattr_init into libc.
- htl: move pthread_barrierattr_destroy into libc.
- htl: move __pthread_default_barrierattr into libc.
- manual: Update signal descriptions
- libio: Replace __LP64__ with __WORDSIZE
- powerpc64le: Also avoid IFUNC for __mempcpy
- elf: Build dl-tls.o with early startup symbol redirections
- manual: make @manpageurl more specific to each output
- math: Fix tanf for some inputs (BZ 32630)
- elf: Use _dl_find_object instead of _dl_find_dso_for_object in dlopen
- elf: Add fast path to dlopen for fully-opened maps
- elf: Determine the caller link map in _dl_open
- elf: Merge __dl_libc_freemem into __rtld_libc_freeres
- elf: Add l_soname accessor function for DT_SONAME values
- elf: Split _dl_lookup_map, _dl_map_new_object from _dl_map_object
- hurd: Use the new __proc_reauthenticate_complete protocol
- elf: Do not add a copy of _dl_find_object to libc.so
- htl: move pthread_setcancelstate into libc.
- math: Fix sinhf for some inputs (BZ 32627)
- math: Fix log10p1f internal table value (BZ 32626)
- manual: Safety annotations for timespec_get and timespec_getres
- sh: Fix tst-guard1 build
- manual: Add links to POSIX Semaphores man-pages documentation
- manual: Consolidate POSIX Semaphores docs in Threads chapter
- ld.so: Decorate BSS mappings
- nptl: Add support for setup guard pages with MADV_GUARD_INSTALL
- nptl: Correct stack size attribute when stack grows up [BZ #32574]
- manual: Update compatibility note on flushing of line-oriented files
- htl: move pthread_setcanceltype into libc.
- htl: move pthread_mutex_consistent, pthread_mutex_consistent_np into libc.
- htl: move pthread_mutex_destroy into libc.
- htl: move pthread_mutex_getprioceiling, pthread_mutex_setprioceiling into libc
- htl: move pthread_mutex_{lock, unlock, trylock, timedlock, clocklock}
- htl: move pthread_mutex_init into libc.
- htl: remove leftover for pthread_mutexattr_settype
- Add test of input file flushing / offset issues
- Fix fflush handling for mmap files after ungetc (bug 32535)
- Fix fseek handling for mmap files after ungetc or fflush (bug 32529)
- Make fflush (NULL) flush input files (bug 32369)
- Make fclose seek input file to right offset (bug 12724)
- Fix fflush after ungetc on input file (bug 5994)
- libio: Add a new fwrite test that evaluates partial writes
- libio: Start to return errors when flushing fwrite's buffer [BZ #29459]
- Add new tests for fopen
- Increase version to 2.41.9000, add new section to NEWS
- Create ChangeLog.old/ChangeLog.30
- Bump version to 2.41
