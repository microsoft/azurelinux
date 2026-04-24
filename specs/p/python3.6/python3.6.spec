# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# ==================
# Top-level metadata
# ==================

%global pybasever 3.6

# pybasever without the dot:
%global pyshortver 36

Name: python%{pybasever}
Summary: Version %{pybasever} of the Python interpreter
URL: https://www.python.org/

#  WARNING  When rebasing to a new Python version,
#           remember to update the python3-docs package as well
%global general_version %{pybasever}.15
#global prerel ...
%global upstream_version %{general_version}%{?prerel}
Version: %{general_version}%{?prerel:~%{prerel}}
Release: 53%{?dist}
# Python is Python
# pip MIT is and bundles:
#   appdirs: MIT
#   distlib: Python
#   distro: ASL 2.0
#   html5lib: MIT
#   six: MIT
#   colorama: BSD
#   cachecontrol: ASL 2.0
#   msgpack-python: ASL 2.0
#   lockfile: MIT
#   progress: ISC
#   ipaddress: Python
#   packaging: ASL 2.0 or BSD
#   pep517: MIT
#   pyparsing: MIT
#   pytoml: MIT
#   retrying: ASL 2.0
#   requests: ASL 2.0
#   chardet: LGPLv2
#   idna: BSD
#   urllib3: MIT
#   certifi: MPLv2.0
#   setuptools: MIT
#   webencodings: BSD
# setuptools is MIT and bundles:
#   packaging: ASL 2.0 or BSD
#   pyparsing: MIT
#   six: MIT
#   appdirs: MIT
# Automatically converted from old format: Python and MIT and ASL 2.0 and BSD and ISC and LGPLv2 and MPLv2.0 and (ASL 2.0 or BSD) - review is highly recommended.
License: LicenseRef-Callaway-Python AND LicenseRef-Callaway-MIT AND Apache-2.0 AND LicenseRef-Callaway-BSD AND ISC AND LicenseRef-Callaway-LGPLv2 AND MPL-2.0 AND (Apache-2.0 OR LicenseRef-Callaway-BSD)


# ==================================
# Conditionals controlling the build
# ==================================

# Note that the bcond macros are named for the CLI option they create.
# "%%bcond_without" means "ENABLE by default and create a --without option"

# Main Python, i.e. whether this is the main Python version in the distribution
# that owns /usr/bin/python3 and other unique paths
# This also means the built subpackages are called python3 rather than python3X
# WARNING: This also influences the flatpackage bcond below.
# By default, this is disabled.
%bcond_with main_python

# Flat package, i.e. python36, python37, python38 for tox etc.
# Default (in Fedora >= 44): disabled
# Default (in Fedora < 44): enabled when this is not the main Python
# Not supported: Combination of flatpackage enabled and main_python enabled
%if %{with main_python} || 0%{?fedora} >= 44
%bcond_with flatpackage
%else
%bcond_without flatpackage
%endif

# Whether to use RPM build wheels from the python-{pip,setuptools}-wheel package
# Uses upstream bundled prebuilt wheels otherwise
# pip 22 no longer supports Python 3.6
%bcond_with rpmwheels

# Expensive optimizations (mainly, profile-guided optimizations)
%ifarch %{ix86} x86_64
%bcond_without optimizations
%else
# On some architectures, the optimized build takes tens of hours, possibly
# longer than Koji's 24-hour timeout. Disable optimizations here.
%bcond_with optimizations
%endif

# Run the test suite in %%check
%bcond_without tests

# Extra build for debugging the interpreter or C-API extensions
# (the -debug subpackages)
%if %{with flatpackage}
%bcond_with debug_build
%else
%bcond_without debug_build
%endif

# Support for the GDB debugger
%bcond_without gdb_hooks

# The dbm.gnu module (key-value database)
%bcond_without gdbm

# Main interpreter loop optimization
%bcond_without computed_gotos

# Support for the Valgrind debugger/profiler
%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

# https://fedoraproject.org/wiki/Changes/Python_Upstream_Architecture_Names
# For a very long time we have converted "upstream architecture names" to "Fedora names".
# This made sense at the time, see https://github.com/pypa/manylinux/issues/687#issuecomment-666362947
# However, with manylinux wheels popularity growth, this is now a problem.
# Wheels built on a Linux that doesn't do this were not compatible with ours and vice versa.
# We now have a compatibility layer to workaround a problem,
# but we also no longer use the legacy arch names in Fedora 34+.
# This bcond controls the behavior. The defaults should be good for anybody.
%if 0%{?fedora} >= 34 || 0%{?rhel} >= 9
%bcond_with legacy_archnames
%else
%bcond_without legacy_archnames
%endif

# ==================================
# Notes from bootstraping Python 3.6
# ==================================
#
# New Python major version (3.X) break ABI and bytecode compatibility,
# so all packages depending on it need to be rebuilt.
#
# Due to a dependency cycle between Python, gdb, rpm, pip, setuptools, wheel,
# and other packages, this isn't straightforward.
# Build in the following order:
#
# 1. At the same time:
#     - gdb without python support (add %%global _without_python 1 on top of
#       gdb's SPEC file)
#     - python-rpm-generators
#       (this can be done also during step 2., but should be done before 3.)
# 2. python3 without rewheel (use %%bcond_with rewheel instead of
#     %%bcond_without)
# 3. gdb with python support (remove %%global _without_python 1 on top of
#    gdb's SPEC file)
# 4. rpm
# 5. python-setuptools with bootstrap set to 1
# 6. python-pip with build_wheel set to 0
# 7. python-wheel with %%bcond_without bootstrap
# 8. python-setuptools with bootstrap set to 0 and also with_check set to 0
# 9. python-pip with build_wheel set to 1
# 10. pyparsing
# 11. python3 with rewheel
#
# Then the most important packages have to be built, in dependency order.
# These were:
#   python-sphinx, pytest, python-requests, cloud-init, dnf, anaconda, abrt
#
# After these have been built, a targeted rebuild should be done for the rest.


# =====================
# General global macros
# =====================

%global pkgname python%{pybasever}

%global pylibdir %{_libdir}/python%{pybasever}
%global dynload_dir %{pylibdir}/lib-dynload

# ABIFLAGS, LDVERSION and SOABI are in the upstream configure.ac
# See PEP 3149 for some background: http://www.python.org/dev/peps/pep-3149/
%global ABIFLAGS_optimized m
%global ABIFLAGS_debug     dm

%global LDVERSION_optimized %{pybasever}%{ABIFLAGS_optimized}
%global LDVERSION_debug     %{pybasever}%{ABIFLAGS_debug}

# When we use the upstream arch triplets, we convert them from the legacy ones
# This is reversed in prep when %%with legacy_archnames, so we keep both macros
%global platform_triplet_legacy %{_arch}-linux%{_gnu}
%global platform_triplet_upstream %{expand:%(echo %{platform_triplet_legacy} | sed -E \\
    -e 's/^arm(eb)?-linux-gnueabi$/arm\\1-linux-gnueabihf/' \\
    -e 's/^mips64(el)?-linux-gnu$/mips64\\1-linux-gnuabi64/' \\
    -e 's/^ppc(64)?(le)?-linux-gnu$/powerpc\\1\\2-linux-gnu/')}
%if %{with legacy_archnames}
%global platform_triplet %{platform_triplet_legacy}
%else
%global platform_triplet %{platform_triplet_upstream}
%endif

%global SOABI_optimized cpython-%{pyshortver}%{ABIFLAGS_optimized}-%{platform_triplet}
%global SOABI_debug     cpython-%{pyshortver}%{ABIFLAGS_debug}-%{platform_triplet}

# All bytecode files are in a __pycache__ subdirectory, with a name
# reflecting the version of the bytecode.
# See PEP 3147: http://www.python.org/dev/peps/pep-3147/
# For example,
#   foo/bar.py
# has bytecode at:
#   foo/__pycache__/bar.cpython-%%{pyshortver}.pyc
#   foo/__pycache__/bar.cpython-%%{pyshortver}.opt-1.pyc
#   foo/__pycache__/bar.cpython-%%{pyshortver}.opt-2.pyc
%global bytecode_suffixes .cpython-%{pyshortver}*.pyc

# libmpdec (mpdecimal package in Fedora) is tightly coupled with the
# decimal module. We keep it bundled as to avoid incompatibilities
# with the packaged version.
# The version information can be found at Modules/_decimal/libmpdec/mpdecimal.h
# defined as MPD_VERSION.
%global libmpdec_version 2.4.2

# Python's configure script defines SOVERSION, and this is used in the Makefile
# to determine INSTSONAME, the name of the libpython DSO:
#   LDLIBRARY='libpython$(VERSION).so'
#   INSTSONAME="$LDLIBRARY".$SOVERSION
# We mirror this here in order to make it easier to add the -gdb.py hooks.
# (if these get out of sync, the payload of the libs subpackage will fail
# and halt the build)
%global py_SOVERSION 1.0
%global py_INSTSONAME_optimized libpython%{LDVERSION_optimized}.so.%{py_SOVERSION}
%global py_INSTSONAME_debug     libpython%{LDVERSION_debug}.so.%{py_SOVERSION}

# Disable automatic bytecompilation. The python3 binary is not yet be
# available in /usr/bin when Python is built. Also, the bytecompilation fails
# on files that test invalid syntax.
%undefine py_auto_byte_compile

# For multilib support, files that are different between 32- and 64-bit arches
# need different filenames. Use "64" or "32" according to the word size.
# Currently, the best way to determine an architecture's word size happens to
# be checking %%{_lib}.
%if "%{_lib}" == "lib64"
%global wordsize 64
%else
%global wordsize 32
%endif

# Opt-out from https://fedoraproject.org/wiki/Changes/fno-omit-frame-pointer
# Python is slower with frame pointers, but we expect to remove this in Python 3.12+
# See https://lists.fedoraproject.org/archives/list/python-devel@lists.fedoraproject.org/thread/6TQYCHMX4FZLF27U5BCEC7IFV6XNBKJP/
# Tracking bugzilla: https://bugzilla.redhat.com/2158729
%undefine _include_frame_pointers

# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized)

BuildRequires: autoconf
BuildRequires: bluez-libs-devel
BuildRequires: bzip2
BuildRequires: bzip2-devel
BuildRequires: desktop-file-utils
BuildRequires: expat-devel

BuildRequires: findutils
BuildRequires: gcc-c++
%if %{with gdbm}
BuildRequires: gdbm-devel
%endif
BuildRequires: git-core
BuildRequires: glibc-all-langpacks
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: gnupg2
BuildRequires: libappstream-glib
BuildRequires: libffi-devel
BuildRequires: libnsl2-devel
BuildRequires: libtirpc-devel
BuildRequires: libGL-devel
BuildRequires: libxcrypt-devel
BuildRequires: libX11-devel
BuildRequires: make
BuildRequires: ncurses-devel

BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: redhat-rpm-config >= 127
BuildRequires: sqlite-devel
BuildRequires: gdb

BuildRequires: openssl-devel

BuildRequires: tar
BuildRequires: tcl-devel < 1:9
BuildRequires: tix-devel
BuildRequires: tk-devel < 1:9

%if %{with valgrind}
BuildRequires: valgrind-devel
%endif

BuildRequires: xz-devel
BuildRequires: zlib-devel

BuildRequires: systemtap-sdt-devel
BuildRequires: /usr/bin/dtrace

# workaround http://bugs.python.org/issue19804 (test_uuid requires ifconfig)
BuildRequires: /usr/sbin/ifconfig

%if %{with rpmwheels}
BuildRequires: python-setuptools-wheel
BuildRequires: python-pip-wheel
%else
# For %%python_wheel_inject_sbom
BuildRequires: python-rpm-macros
%endif


# =======================
# Source code and patches
# =======================

Source0: %{url}ftp/python/%{general_version}/Python-%{upstream_version}.tar.xz
Source1: %{url}ftp/python/%{general_version}/Python-%{upstream_version}.tar.xz.asc
Source2: %{url}static/files/pubkeys.txt

# A simple script to check timestamps of bytecode files
# Run in check section with Python that is currently being built
# Originally written by bkabrda
Source8: check-pyc-timestamps.py

# Desktop menu entry for idle3
Source10: idle3.desktop

# AppData file for idle3
Source11: idle3.appdata.xml

# Patches for bundled wheels

# Patch for the bundled pip wheel for CVE-2007-4559
Source101: pip-CVE-2007-4559.patch

# Patch for the bundled setuptools wheel for CVE-2024-6345
# Remote code execution via download functions in the package_index module
# Tracking bug: https://bugzilla.redhat.com/show_bug.cgi?id=2297771
# Upstream solution: https://github.com/pypa/setuptools/pull/4332
# Patch simplified because upstream doesn't support SVN anymore.
Source102: setuptools-CVE-2024-6345.patch

# (Patches taken from github.com/fedora-python/cpython)

# 00001 # d06a8853cf4bae9e115f45e1d531d2dc152c5cc8
# Fixup distutils/unixccompiler.py to remove standard library path from rpath
#
# Was Patch0 in ivazquez' python3000 specfile
Patch1: 00001-rpath.patch

# 00102 # 4a773a6f1c51615333cbae27982904a312777223
# Change the various install paths to use /usr/lib64/ instead or /usr/lib/
#
# Only used when "%%{_lib}" == "lib64".
Patch102: 00102-lib64.patch

# 00111 # f07cfb42e1868a3bba0890edf4a72beaeeae370c
# Don't try to build a libpythonMAJOR.MINOR.a
#
# Downstream only: not appropriate for upstream.
#
# See https://bugzilla.redhat.com/show_bug.cgi?id=556092
Patch111: 00111-no-static-lib.patch

# 00132 # 75c270b8641ddff06c0edf7be7cc444e6debb6d7
# Add rpmbuild hooks to unittest
#
# Add non-standard hooks to unittest for use in the "check" phase, when
# running selftests within the build:
#   @unittest._skipInRpmBuild(reason)
# for tests that hang or fail intermittently within the build environment, and:
#   @unittest._expectedFailureInRpmBuild
# for tests that always fail within the build environment
#
# The hooks only take effect if WITHIN_PYTHON_RPM_BUILD is set in the
# environment, which we set manually in the appropriate portion of the "check"
# phase below (and which potentially other python-* rpms could set, to reuse
# these unittest hooks in their own "check" phases)
Patch132: 00132-add-rpmbuild-hooks-to-unittest.patch

# 00155 # 0ef7ae83073c1bbe610d4678ed56ae775fd6e174
# avoid allocating thunks in ctypes unless absolutely necessary
#
# Avoid allocating thunks in ctypes unless absolutely necessary, to avoid
# generating SELinux denials on "import ctypes" and "import uuid" when
# embedding Python within httpd
# See https://bugzilla.redhat.com/show_bug.cgi?id=814391
Patch155: 00155-avoid-ctypes-thunks.patch

# 00160 # f69288aba24c43c506c3e90e2aa658e436e76e72
# Disable test_fs_holes in RPM build
#
# Python 3.3 added os.SEEK_DATA and os.SEEK_HOLE, which may be present in the
# header files in the build chroot, but may not be supported in the running
# kernel, hence we disable this test in an rpm build.
# Adding these was upstream issue http://bugs.python.org/issue10142
Patch160: 00160-disable-test_fs_holes-in-rpm-build.patch

# 00163 # 88e26259f7da12e17adb936815aa421d84c69f09
# Disable parts of test_socket in RPM build
#
# Some tests within test_socket fail intermittently when run inside Koji;
# disable them using unittest._skipInRpmBuild
Patch163: 00163-disable-parts-of-test_socket-in-rpm-build.patch

# 00170 # 5a71e038b7511727657466d7796cf9c11c67334a
# In debug builds, try to print repr() when a C-level assert fails
#
# In debug builds, try to print repr() when a C-level assert fails in the
# garbage collector (typically indicating a reference-counting error
# somewhere else e.g in an extension module)
# The new macros/functions within gcmodule.c are hidden to avoid exposing
# them within the extension API.
# Sent upstream: http://bugs.python.org/issue9263
# See https://bugzilla.redhat.com/show_bug.cgi?id=614680
Patch170: 00170-gc-assertions.patch

# 00189 # dd3bacdeb7a9c0c99ab78229d3f1aa4c9761efb4
# Instead of bundled wheels, use our RPM packaged wheels
#
# We keep them in /usr/share/python-wheels
Patch189: 00189-use-rpm-wheels.patch
# The following versions of setuptools/pip are bundled when this patch is not applied.
# The versions are written in Lib/ensurepip/__init__.py, this patch removes them.
# When the bundled setuptools/pip wheel is updated, the patch no longer applies cleanly.
# In such cases, the patch needs to be amended and the versions updated here:
%global pip_version 18.1
%global setuptools_version 40.6.2

# 00251 # 2eabd04356402d488060bc8fe316ad13fc8a3356
# Change user install location
#
# Set values of prefix and exec_prefix in distutils install command
# to /usr/local if executable is /usr/bin/python* and RPM build
# is not detected to make pip and distutils install into separate location.
#
# Fedora Change: https://fedoraproject.org/wiki/Changes/Making_sudo_pip_safe
Patch251: 00251-change-user-install-location.patch

# 00262 # eb17e4d0defe4a58be25df5128fda6eab53acbbb
# PEP538 - Coerce legacy C locale
#
# Backport of PEP 538: Coercing the legacy C locale to a UTF-8 based locale
# https://www.python.org/dev/peps/pep-0538/
# Fedora Change: https://fedoraproject.org/wiki/Changes/python3_c.utf-8_locale
# Original proposal: https://bugzilla.redhat.com/show_bug.cgi?id=1404918
Patch262: 00262-pep538_coerce_legacy_c_locale.patch

# 00292 # 7bee9c57be78ac9bb512ddc08b1f73271c494e4d
# Restore PyExc_RecursionErrorInst symbol
#
# Restore the public PyExc_RecursionErrorInst symbol that was removed
# from the 3.6.4 release upstream.
# Reported upstream: https://bugs.python.org/issue30697
Patch292: 00292-restore-PyExc_RecursionErrorInst-symbol.patch

# 00294 # dddeb1c65cb86057d5c44be91e7965e5681c87e0
# Define TLS cipher suite on build time
#
# Define TLS cipher suite on build time depending
# on the OpenSSL default cipher suite selection.
# Fixed upstream on CPython's 3.7 branch:
# https://bugs.python.org/issue31429
# See also: https://bugzilla.redhat.com/show_bug.cgi?id=1489816
Patch294: 00294-define-TLS-cipher-suite-on-build-time.patch

# 00319 # 137b120c34cd92a9694edc0196f0d78311071dba
# test_tarfile_ppc64
#
# Fix sparse file tests of test_tarfile on ppc64le with the tmpfs
# filesystem.
#
# Upstream: https://bugs.python.org/issue35772
Patch319: 00319-test_tarfile_ppc64.patch

# 00343 # c758d1d3051b80314a533a8a42244beb4670141e
# Fix test_faulthandler on GCC 10
#
# bpo-21131: Fix faulthandler.register(chain=True) stack (GH-15276)
# https://bugs.python.org/issue21131
# https://github.com/python/cpython/commit/ac827edc493d3ac3f5b9b0cc353df1d4b418a9aa
Patch343: 00343-faulthandler-gcc10.patch

# 00353 # ab4cc97b643cfe99f567e3a03e5617b507183771
# Original names for architectures with different names downstream
#
# https://fedoraproject.org/wiki/Changes/Python_Upstream_Architecture_Names
#
# Pythons in RHEL/Fedora used different names for some architectures
# than upstream and other distros (for example ppc64 vs. powerpc64).
# This was patched in patch 274, now it is sedded if %%with legacy_archnames.
#
# That meant that an extension built with the default upstream settings
# (on other distro or as an manylinux wheel) could not been found by Python
# on RHEL/Fedora because it had a different suffix.
# This patch adds the legacy names to importlib so Python is able
# to import extensions with a legacy architecture name in its
# file name.
# It work both ways, so it support both %%with and %%without legacy_archnames.
#
# WARNING: This patch has no effect on Python built with bootstrap
# enabled because Python/importlib_external.h is not regenerated
# and therefore Python during bootstrap contains importlib from
# upstream without this feature. It's possible to include
# Python/importlib_external.h to this patch but it'd make rebasing
# a nightmare because it's basically a binary file.
Patch353: 00353-architecture-names-upstream-downstream.patch

# 00358 # cd155152db2f3f64831ecc5bd174a72c3bac401f
# align allocations and PyGC_Head to 16 bytes on 64-bit platforms
#
# Upstream bug: https://bugs.python.org/issue27987
# Fixes: https://bugzilla.redhat.com/show_bug.cgi?id=1923658
#
# Combination of two upstream commits:
# - 1b85f4ec45a5d63188ee3866bd55eb29fdec7fbf
# - 8766cb74e186d3820db0a855ccd780d6d84461f7
Patch358: 00358-align-allocations-and-pygc_head-to-16-bytes-on-64-bit-platforms.patch

# 00361 # b3dd949b7947b1b44b358e0c30d080e5b16ca8bc
# openssl-3-compatibility
#
# Backported from Python 3.8
#
# Based on https://github.com/stratakis/cpython/tree/fedora-3.6_openssl3_compat
Patch361: 00361-openssl-3-compatibility.patch

# 00375 # 5488ab84d2447aa8df8b3502e76f151ac2488947
# Fix test_distance to enable build on i686
#
# Fix precision in test_distance (test.test_turtle.TestVec2D).
# See: https://bugzilla.redhat.com/show_bug.cgi?id=2038843
Patch375: 00375-fix-test_distance-to-enable-build-on-i686.patch

# 00378 # b0c3e36a85f7eec22d64222176ea5139c0bc097d
# Support expat 2.4.5
#
# Curly brackets were never allowed in namespace URIs
# according to RFC 3986, and so-called namespace-validating
# XML parsers have the right to reject them a invalid URIs.
#
# libexpat >=2.4.5 has become strcter in that regard due to
# related security issues; with ET.XML instantiating a
# namespace-aware parser under the hood, this test has no
# future in CPython.
#
# References:
# - https://datatracker.ietf.org/doc/html/rfc3968
# - https://www.w3.org/TR/xml-names/
#
# Also, test_minidom.py: Support Expat >=2.4.5
#
# Upstream: https://bugs.python.org/issue46811
Patch378: 00378-support-expat-2-4-5.patch

# 00382 # 9e275dcdf3934b827994ecc3247d583d5bab7985
# CVE-2015-20107
#
# Make mailcap refuse to match unsafe filenames/types/params (GH-91993)
#
# Upstream: https://github.com/python/cpython/issues/68966
#
# Tracker bug: https://bugzilla.redhat.com/show_bug.cgi?id=2075390
Patch382: 00382-cve-2015-20107.patch

# 00386 # 0e4bced7d3cd0f94ebfbcc209e10dbf81607b073
# CVE-2021-28861
#
# Fix an open redirection vulnerability in the `http.server` module when
# an URI path starts with `//` that could produce a 301 Location header
# with a misleading target.  Vulnerability discovered, and logic fix
# proposed, by Hamza Avvan (@hamzaavvan).
#
# Test and comments authored by Gregory P. Smith [Google].
#
# Upstream: https://github.com/python/cpython/pull/93879
# Tracking bugzilla: https://bugzilla.redhat.com/show_bug.cgi?id=2120642
Patch386: 00386-cve-2021-28861.patch

# 00387 # c687b2d407c9ec9ddf30a14f7151aa2064a8b0eb
# CVE-2020-10735: Prevent DoS by very large int()
#
# gh-95778: CVE-2020-10735: Prevent DoS by very large int() (GH-96504)
#
# Converting between `int` and `str` in bases other than 2
# (binary), 4, 8 (octal), 16 (hexadecimal), or 32 such as base 10 (decimal) now
# raises a `ValueError` if the number of digits in string form is above a
# limit to avoid potential denial of service attacks due to the algorithmic
# complexity. This is a mitigation for CVE-2020-10735
# (https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-10735).
#
# This new limit can be configured or disabled by environment variable, command
# line flag, or :mod:`sys` APIs. See the `Integer String Conversion Length
# Limitation` documentation.  The default limit is 4300
# digits in string form.
#
# Patch by Gregory P. Smith [Google] and Christian Heimes [Red Hat] with feedback
# from Victor Stinner, Thomas Wouters, Steve Dower, Ned Deily, and Mark Dickinson.
#
# Notes on the backport to Python 3.6:
#
# * Use "Python 3.6.15-13" version in the documentation, whereas this
#   version will never be released
# * Only add _Py_global_config_int_max_str_digits global variable:
#   Python 3.6 doesn't have PyConfig API (PEP 597) nor _PyRuntime.
# * sys.flags.int_max_str_digits cannot be -1 on Python 3.6: it is
#   set to the default limit. Adapt test_int_max_str_digits() for that.
# * Declare _PY_LONG_DEFAULT_MAX_STR_DIGITS and
#   _PY_LONG_MAX_STR_DIGITS_THRESHOLD macros in longobject.h but only
#   if the Py_BUILD_CORE macro is defined.
# * Declare _Py_global_config_int_max_str_digits in pydebug.h.
#
#
# gh-95778: Mention sys.set_int_max_str_digits() in error message (#96874)
#
# When ValueError is raised if an integer is larger than the limit,
# mention sys.set_int_max_str_digits() in the error message.
#
#
# gh-96848: Fix -X int_max_str_digits option parsing (#96988)
#
# Fix command line parsing: reject "-X int_max_str_digits" option with
# no value (invalid) when the PYTHONINTMAXSTRDIGITS environment
# variable is set to a valid limit.
Patch387: 00387-cve-2020-10735-prevent-dos-by-very-large-int.patch

# 00392 # 033f82b975577a72218ce385b5333dcc5c88dfd5
# CVE-2022-37454: Fix buffer overflows in _sha3 module
#
# This is a port of the applicable part of XKCP's fix [1] for
# CVE-2022-37454 and avoids the segmentation fault and the infinite
# loop in the test cases published in [2].
#
# [1]: https://github.com/XKCP/XKCP/commit/fdc6fef075f4e81d6b1bc38364248975e08e340a
# [2]: https://mouha.be/sha-3-buffer-overflow/
Patch392: 00392-cve-2022-37454-fix-buffer-overflows-in-_sha3-module.patch

# 00394 # 377cbc015f738fdea510969d0dbe266748b6bb09
# CVE-2022-45061: CPU denial of service via inefficient IDNA decoder
#
# gh-98433: Fix quadratic time idna decoding.
#
# There was an unnecessary quadratic loop in idna decoding. This restores
# the behavior to linear.
Patch394: 00394-cve-2022-45061-cpu-denial-of-service-via-inefficient-idna-decoder.patch

# 00397 # e867e27272cd259b76133784ef3f2811e671f3db
# PEP 706, CVE-2007-4559: Filter API for tarfile.extractall
#
# Add API for allowing checks on the content of tar files, allowing callers to mitigate
# directory traversal (CVE-2007-4559) and related issues.
#
# Python 3.12 will warn if this API is not used.
# Python 3.14 will fail if it's not used.
#
# Backport from https://github.com/python/cpython/issues/102950
#
# Change document: https://peps.python.org/pep-0706/
Patch397: 00397-pep-706-cve-2007-4559-filter-api-for-tarfile-extractall.patch

# 00399 # dc0a803eea47d3b4f0657816b112b5a33491500f
# CVE-2023-24329
#
# gh-102153: Start stripping C0 control and space chars in `urlsplit` (GH-102508)
#
# `urllib.parse.urlsplit` has already been respecting the WHATWG spec a bit GH-25595.
#
# This adds more sanitizing to respect the "Remove any leading C0 control or space from input" [rule](https://url.spec.whatwg.org/GH-url-parsing:~:text=Remove%%20any%%20leading%%20and%%20trailing%%20C0%%20control%%20or%%20space%%20from%%20input.) in response to [CVE-2023-24329](https://nvd.nist.gov/vuln/detail/CVE-2023-24329).
#
# Backported from Python 3.12
Patch399: 00399-cve-2023-24329.patch

# 00407 # f562db9763f424318fd311e3267d2aed0afadbbe
# gh-99086: Fix implicit int compiler warning in configure check for PTHREAD_SCOPE_SYSTEM
Patch407: 00407-gh-99086-fix-implicit-int-compiler-warning-in-configure-check-for-pthread_scope_system.patch

# 00409 # e9d6272416d44decf99497e4eca478e44be6a8e2
# bpo-13497: Fix `broken nice` configure test
#
# Per POSIX, `nice(3)` requires `unistd.h` and `exit(3)` requires `stdlib.h`.
#
# Fixing the test will prevent false positives with pedantic compilers like clang.
Patch409: 00409-bpo-13497-fix-broken-nice-configure-test.patch

# 00410 # ea9f02d63dc0f772362f520967bce90e4f4d3abd
# bpo-42598: Fix implicit function declarations in configure
#
# This is invalid in C99 and later and is an error with some compilers
# (e.g. clang in Xcode 12), and can thus cause configure checks to
# produce incorrect results.
Patch410: 00410-bpo-42598-fix-implicit-function-declarations-in-configure.patch

# 00415 # b2fcdad7812f48865b2186b08c1ae28e9af65975
# [CVE-2023-27043] gh-102988: Reject malformed addresses in email.parseaddr() (#111116)
#
# Detect email address parsing errors and return empty tuple to
# indicate the parsing error (old API). Add an optional 'strict'
# parameter to getaddresses() and parseaddr() functions. Patch by
# Thomas Dwyer.
Patch415: 00415-cve-2023-27043-gh-102988-reject-malformed-addresses-in-email-parseaddr-111116.patch

# 00419 # f13682530cc7e4daec2e40acd56508846fdd3aad
# gh-112769: test_zlib: Fix comparison of ZLIB_RUNTIME_VERSION with non-int suffix (GH-112771) (GH-112774)
#
# zlib-ng defines the version as "1.3.0.zlib-ng".
Patch419: 00419-gh-112769-test_zlib-fix-comparison-of-zlib_runtime_version-with-non-int-suffix-gh-112771-gh-112774.patch

# 00422 # fefea32e0c70109a5c88e3d22ec9ff554fcbc6ab
# gh-115133: Fix tests for XMLPullParser with Expat 2.6.0
#
# Feeding the parser by too small chunks defers parsing to prevent
# CVE-2023-52425. Future versions of Expat may be more reactive.
Patch422: 00422-gh-115133-fix-tests-for-xmlpullparser-with-expat-2-6-0.patch

# 00423 # 81584d3af3b307c2aeede3ba8ae95c7efc81f5f7
# bpo-33377: Add triplets for mips-r6 and riscv
Patch423: 00423-bpo-33377-add-triplets-for-mips-r6-and-riscv.patch

# 00426 # 05ddec93394a09199c3bbb2d71a4a2566fd50332
# CVE-2023-6597
#
# Combines Two fixes for tempfile.TemporaryDirectory:
# https://github.com/python/cpython/commit/e9b51c0ad81da1da11ae65840ac8b50a8521373c
# https://github.com/python/cpython/commit/02a9259c717738dfe6b463c44d7e17f2b6d2cb3a
Patch426: 00426-cve-2023-6597.patch

# 00427 # 37c3b42b8931ed4eca0272bf53086eb28ca8544e
# ZipExtFile tell and seek, CVE-2024-0450
#
# Backport of seek and tell methods for ZipExtFile makes it
# possible to backport the fix for CVE-2024-0450.
#
# Combines:
# https://github.com/python/cpython/commit/066df4fd454d6ff9be66e80b2a65995b10af174f
# https://github.com/python/cpython/commit/66363b9a7b9fe7c99eba3a185b74c5fdbf842eba
Patch427: 00427-zipextfile-tell-and-seek-cve-2024-0450.patch

# 00431 # ee1b513c52ab7663f7d58b07a1df123ea551e7c4
# CVE-2024-4032: incorrect IPv4 and IPv6 private ranges
#
# Upstream issue: https://github.com/python/cpython/issues/113171
#
# Backported from 3.8.
Patch431: 00431-cve-2024-4032.patch

# 00435 # f80b87e6a67eebe0693b895261bad2e9a58a4825
# gh-121650: Encode newlines in headers, and verify headers are sound (GH-122233)
#
# Per RFC 2047:
#
# > [...] these encoding schemes allow the
# > encoding of arbitrary octet values, mail readers that implement this
# > decoding should also ensure that display of the decoded data on the
# > recipient's terminal will not cause unwanted side-effects
#
# It seems that the "quoted-word" scheme is a valid way to include
# a newline character in a header value, just like we already allow
# undecodable bytes or control characters.
# They do need to be properly quoted when serialized to text, though.
#
# This should fail for custom fold() implementations that aren't careful
# about newlines.
#
#
# This patch also contains modified commit cherry picked from
# c5bba853d5e7836f6d4340e18721d3fb3a6ee0f7.
#
# This commit was backported to simplify the backport of the other commit
# fixing CVE. The only modification is a removal of one test case which
# tests multiple changes in Python 3.7 and it wasn't working properly
# with Python 3.6 where we backported only one change.
Patch435: 00435-gh-121650-encode-newlines-in-headers-and-verify.patch

# 00437 # c1618bd3b415d9df1a2d050332220300d394ac5f
# CVE-2024-6232 Remove backtracking when parsing tarfile headers
#
# * Remove backtracking when parsing tarfile headers
# * Rewrite PAX header parsing to be stricter
# * Optimize parsing of GNU extended sparse headers v0.0
Patch437: 00437-cve-2024-6232-remove-backtracking-when-parsing-tarfile-headers.patch

# 00443 # 49e939f29e3551ec4e7bdb2cc8b8745e3d1fca35
# gh-124651: Quote template strings in `venv` activation scripts
#
# (cherry picked from 3.9)
Patch443: 00443-gh-124651-quote-template-strings-in-venv-activation-scripts.patch

# 00444 # fed0071c8c86599091f93967a5fa2cce42ceb840
# Security fix for CVE-2024-11168
#
# gh-103848: Adds checks to ensure that bracketed hosts found by urlsplit are of IPv6 or IPvFuture format (GH-103849)
#
# Tests are adjusted because Python <3.9 don't support scoped IPv6 addresses.
Patch444: 00444-security-fix-for-cve-2024-11168.patch

# 00446 # f5cc2c3be4273be70cdcdf9eb95abf425808f752
# Resolve sinpi name clash with libm
#
# bpo-36106: Resolve sinpi name clash with libm (IEEE-754 violation). (GH-12027)
#
# The standard math library (libm) may follow IEEE-754 recommendation to
# include an implementation of sinPi(), i.e. sinPi(x):=sin(pi*x).
# And this triggers a name clash, found by FreeBSD developer
# Steve Kargl, who worken on putting sinpi into libm used on FreeBSD
# (it has to be named "sinpi", not "sinPi", cf. e.g.
# https://en.cppreference.com/w/c/experimental/fpext4).
Patch446: 00446-Resolve-sinpi-name-clash-with-libm.patch

# 00450 # 31aa7c11975e890489e31d8b293c3f92d3ea1180
# CVE-2025-0938: Disallow square brackets ([ and ]) in domain names for parsed URLs
Patch450: 00450-cve-2025-0938-disallow-square-brackets-and-in-domain-names-for-parsed-urls.patch

# 00452 # dab1c136301f0beac6ec132a8e5b08206b698bc8
# Properly apply exported CFLAGS for dtrace/systemtap builds
#
# When using --with-dtrace the resulting object file could be missing
# specific CFLAGS exported by the build system due to the systemtap
# script using specific defaults.
#
# Exporting the CC and CFLAGS variables before the dtrace invocation
# allows us to properly apply CFLAGS exported by the build system
# even when cross-compiling.
Patch452: 00452-properly-apply-exported-cflags-for-dtrace-systemtap-builds.patch

# 00457 # da99203f07d380d50ec780323bbebda00f227797
# ssl: Raise OSError for ERR_LIB_SYS
#
# The patch resolves the flakiness of test_ftplib
#
# Backported from upstream 3.10+:
# https://github.com/python/cpython/pull/127361
Patch457: 00457-ssl-raise-oserror-for-err_lib_sys.patch

# 00465 # 2224c823bcc1b62b85f516883151459ae51cdb7d
# tarfile cves
#
# Security fixes for CVE-2025-4517, CVE-2025-4330, CVE-2025-4138, CVE-2024-12718, CVE-2025-4435 on tarfile
#
# The backported fixes do not contain changes for ntpath.py and related tests,
# because the support for symlinks and junctions were added later in Python 3.9,
# and it does not make sense to backport them to 3.6 here.
#
# The patch is contains the following changes:
# - https://github.com/python/cpython/commit/42deeab5b2efc2930d4eb73416e1dde9cf790dd2
#   fixes symlink handling for tarfile.data_filter
# - https://github.com/python/cpython/commit/9d2c2a8e3b8fe18ee1568bfa4a419847b3e78575
#   fixes handling of existing files/symlinks in tarfile
# - https://github.com/python/cpython/commit/00af9794dd118f7b835dd844b2b609a503ad951e
#   adds a new "strict" argument to realpath()
# - https://github.com/python/cpython/commit/dd8f187d0746da151e0025c51680979ac5b4cfb1
#   fixes mulriple CVE fixes in the tarfile module
# - downstream only fixes that makes the changes work and compatible with Python 3.6
Patch465: 00465-tarfile-cves.patch

# 00467 # f0b2819ec35fe1f732f661aea68863a5e4dd829f
# tarfile CVE-2025-8194
#
# tarfile now validates archives to ensure member offsets are non-negative (GH-137027)
Patch467: 00467-tarfile-cve-2025-8194.patch

# 00473 # e05f1f3d8ad066ef84e8353328bff5fa9403a241
# CVE-2026-0865
#
# gh-143916: Reject control characters in wsgiref.headers.Headers  (GH-143917)
#
# * Add 'test.support' fixture for C0 control characters
# * gh-143916: Reject control characters in wsgiref.headers.Headers
Patch473: 00473-cve-2026-0865.patch

# 00474 # 837ddca0372fa87ff9cee47142200caa21e77def
# CVE-2025-15366
#
# gh-143921: Reject control characters in IMAP commands
#
# (cherry-picked from commit 6262704b134db2a4ba12e85ecfbd968534f28b45)
Patch474: 00474-cve-2025-15366.patch

# 00475 # 2dc1bd28c0d5e9af4336a10bd64b895bd84bd946
# CVE-2025-15367
#
# gh-143923: Reject control characters in POP3 commands
#
# (cherry-picked from commit b234a2b67539f787e191d2ef19a7cbdce32874e7)
Patch475: 00475-cve-2025-15367.patch

# 00476 # 7caaa0b2486d0f5a1bdf12bb9b9f1393560ee303
# CVE-2026-1299
#
# gh-144125: email: verify headers are sound in BytesGenerator
#
#
#
# The fix for the CVE uncovered a known issue in handling
# policy.linesep lengths fixed by:
#
# bpo-34424: Handle different policy.linesep lengths correctly. (#8803)
#
# (cherry-picked from commit 45b2f8893c1b7ab3b3981a966f82e42beea82106)
Patch476: 00476-cve-2026-1299.patch

# (New patches go here ^^^)
#
# When adding new patches to "python" and "python3" in Fedora, EL, etc.,
# please try to keep the patch numbers in-sync between all specfiles.
#
# More information, and a patch number catalog, is at:
#
#     https://fedoraproject.org/wiki/SIGs/Python/PythonPatches


# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

# Provide and obsolete the old python3X name
Provides:  python%{pyshortver} = %{version}-%{release}
Obsoletes: python%{pyshortver} < %{version}-%{release}

# Packages with Python modules in standard locations automatically
# depend on python(abi). Provide that here only for the main Python.
%if %{with main_python}
Provides: python(abi) = %{pybasever}
%else
%global __requires_exclude ^python\\(abi\\) = 3\\..+
%global __provides_exclude ^python\\(abi\\) = 3\\..+
%endif

%if %{without flatpackage}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

# In order to support multiple Python interpreters for development purposes,
# packages with the naming scheme flatpackage (e.g. python35) exist for
# non-default versions of Python 3.
# For consistency, and to keep the upgrade path clean, we Provide/Obsolete
# these names here.
Provides: python%{pyshortver} = %{version}-%{release}
# Note that using Obsoletes without package version is not standard practice.
# Here we assert that *any* version of the system's default interpreter is
# preferable to an "extra" interpreter. For example, python3-3.6.1 will
# replace python36-3.6.2.
Obsoletes: python%{pyshortver}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{name} < 3.6.15-50

%if %{with main_python}
# Previously, this was required for our rewheel patch to work.
# This is technically no longer needed, but we keep it recommended
# for the developer experience.
Recommends: python3-setuptools
Recommends: python3-pip
%endif

# This prevents ALL subpackages built from this spec to require
# /usr/bin/python3*. Granularity per subpackage is impossible.
# It's intended for the libs package not to drag in the interpreter, see
# https://bugzilla.redhat.com/show_bug.cgi?id=1547131
# All others require %%{name} anyway.
%global __requires_exclude ^/usr/bin/python3


# The description used both for the SRPM and the main `python3` subpackage:
%description
Python is an accessible, high-level, dynamically typed, interpreted programming
language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

The %{name} package provides the "python3" executable: the reference
interpreter for the Python language, version 3.
The majority of its standard library is provided in the %{name}-libs package,
which should be installed automatically along with %{name}.
The remaining parts of the Python standard library are broken out into the
%{name}-tkinter and %{name}-test packages, which may need to be installed
separately.

Documentation for Python is provided in the %{name}-docs package.

Packages containing additional libraries for Python are generally named with
the "%{name}-" prefix.


%package libs
Summary:        Python runtime libraries

%if %{with rpmwheels}
Requires: python-setuptools-wheel
Requires: python-pip-wheel
%else
# Versions of bundled libs are based on:
# https://github.com/pypa/pip/blob/18.1/src/pip/_vendor/vendor.txt and
# https://github.com/pypa/setuptools/blob/v40.6.2/pkg_resources/_vendor/vendored.txt
Provides: bundled(python3dist(pip)) = 18.1
Provides: bundled(python3dist(appdirs)) = 1.4.3
Provides: bundled(python3dist(distlib)) = 0.2.7
Provides: bundled(python3dist(distro)) = 1.3
Provides: bundled(python3dist(html5lib)) = 1.0.1
Provides: bundled(python3dist(six)) = 1.11
Provides: bundled(python3dist(colorama)) = 0.3.9
Provides: bundled(python3dist(cachecontrol)) = 0.12.5
Provides: bundled(python3dist(msgpack-python)) = 0.5.6
Provides: bundled(python3dist(lockfile)) = 0.12.2
Provides: bundled(python3dist(progress)) = 1.4
Provides: bundled(python3dist(ipaddress)) = 1.0.22
Provides: bundled(python3dist(packaging)) = 18
Provides: bundled(python3dist(pep517)) = 0.2
Provides: bundled(python3dist(pyparsing)) = 2.2.1
Provides: bundled(python3dist(pytoml)) = 0.1.19
Provides: bundled(python3dist(retrying)) = 1.3.3
Provides: bundled(python3dist(requests)) = 2.19.1
Provides: bundled(python3dist(chardet)) = 3.0.4
Provides: bundled(python3dist(idna)) = 2.7
Provides: bundled(python3dist(urllib3)) = 1.23
Provides: bundled(python3dist(certifi)) = 2018.8.24
Provides: bundled(python3dist(setuptools)) = 40.4.3
Provides: bundled(python3dist(webencodings)) = 0.5.1

Provides: bundled(python3dist(setuptools)) = 40.6.2
Provides: bundled(python3dist(packaging)) = 16.8
Provides: bundled(python3dist(pyparsing)) = 2.2.1
Provides: bundled(python3dist(six)) = 1.10
Provides: bundled(python3dist(appdirs)) = 1.4.3
%endif

# Provides for the bundled libmpdec
Provides: bundled(mpdecimal) = %{libmpdec_version}
Provides: bundled(libmpdec) = %{libmpdec_version}

# There are files in the standard library that have python shebang.
# We've filtered the automatic requirement out so libs are installable without
# the main package. This however makes it pulled in by default.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1547131
Recommends: %{name}%{?_isa} = %{version}-%{release}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{name} < 3.6.15-50

%description libs
This package contains runtime libraries for use by Python:
- the majority of the Python standard library
- a dynamically linked library for use by applications that embed Python as
  a scripting language, and by the main "python3" executable


%package devel
Summary: Libraries and header files needed for Python development
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires: python-rpm-macros
# The RPM related dependencies bring nothing to a non-RPM Python developer
# But we want them when packages BuildRequire python3-devel
Requires: (python-rpm-macros if rpm-build)
Requires: (python3-rpm-macros if rpm-build)
Requires: (python3-rpm-generators if rpm-build)

Provides: %{name}-2to3 = %{version}-%{release}
%if %{with main_python}
Provides: 2to3 = %{version}-%{release}
%endif

Conflicts: %{name} < %{version}-%{release}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{name} < 3.6.15-50

%description devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.

It also contains the necessary macros to build RPM packages with Python modules
and 2to3 tool, an automatic source converter from Python 2.X.


%package idle
Summary: A basic graphical development environment for Python
Requires: %{name} = %{version}-%{release}
Requires: %{name}-tkinter = %{version}-%{release}

%if %{with main_python}
Provides: idle3 = %{version}-%{release}
%endif

Provides: %{name}-tools = %{version}-%{release}
Provides: %{name}-tools%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-tools < %{version}-%{release}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{name} < 3.6.15-50

%description idle
IDLE is Python’s Integrated Development and Learning Environment.

IDLE has the following features: Python shell window (interactive
interpreter) with colorizing of code input, output, and error messages;
multi-window text editor with multiple undo, Python colorizing,
smart indent, call tips, auto completion, and other features;
search within any window, replace within editor windows, and
search through multiple files (grep); debugger with persistent
breakpoints, stepping, and viewing of global and local namespaces;
configuration, browsers, and other dialogs.


%package tkinter
Summary: A GUI toolkit for Python
Requires: %{name} = %{version}-%{release}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{name} < 3.6.15-50

%description tkinter
The Tkinter (Tk interface) library is a graphical user interface toolkit for
the Python programming language.


%package test
Summary: The self-test suite for the main python3 package
Requires: %{name} = %{version}-%{release}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{name} < 3.6.15-50

%description test
The self-test suite for the Python interpreter.

This is only useful to test Python itself. For testing general Python code,
you should use the unittest module from %{name}-libs, or a library such as
%{name}-pytest or %{name}-nose.


%if %{with debug_build}
%package debug
Summary: Debug version of the Python runtime

# The debug build is an all-in-one package version of the regular build, and
# shares the same .py/.pyc files and directories as the regular build. Hence
# we depend on all of the subpackages of the regular build:
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-test%{?_isa} = %{version}-%{release}
Requires: %{name}-tkinter%{?_isa} = %{version}-%{release}
Requires: %{name}-idle%{?_isa} = %{version}-%{release}

%description debug
python3-debug provides a version of the Python runtime with numerous debugging
features enabled, aimed at advanced Python users such as developers of Python
extension modules.

This version uses more memory and will be slower than the regular Python build,
but is useful for tracking down reference-counting issues and other bugs.

The bytecode format is unchanged, so that .pyc files are compatible between
this and the standard version of Python, but the debugging features mean that
C/C++ extension modules are ABI-incompatible and must be built for each version
separately.

The debug build shares installation directories with the standard Python
runtime, so that .py and .pyc files can be shared.
Compiled extension modules use a special ABI flag ("d") in the filename,
so extensions for both versions can co-exist in the same directory.
%endif # with debug_build

%else  # with flatpackage

%if %{with rpmwheels}
Requires: python-setuptools-wheel
Requires: python-pip-wheel
%else
# Versions of bundled libs are based on:
# https://github.com/pypa/pip/blob/18.1/src/pip/_vendor/vendor.txt and
# https://github.com/pypa/setuptools/blob/v40.6.2/pkg_resources/_vendor/vendored.txt
Provides: bundled(python3dist(pip)) = %{pip_version}
Provides: bundled(python3dist(appdirs)) = 1.4.3
Provides: bundled(python3dist(distlib)) = 0.2.7
Provides: bundled(python3dist(distro)) = 1.3
Provides: bundled(python3dist(html5lib)) = 1.0.1
Provides: bundled(python3dist(six)) = 1.11
Provides: bundled(python3dist(colorama)) = 0.3.9
Provides: bundled(python3dist(cachecontrol)) = 0.12.5
Provides: bundled(python3dist(msgpack-python)) = 0.5.6
Provides: bundled(python3dist(lockfile)) = 0.12.2
Provides: bundled(python3dist(progress)) = 1.4
Provides: bundled(python3dist(ipaddress)) = 1.0.22
Provides: bundled(python3dist(packaging)) = 18
Provides: bundled(python3dist(pep517)) = 0.2
Provides: bundled(python3dist(pyparsing)) = 2.2.1
Provides: bundled(python3dist(pytoml)) = 0.1.19
Provides: bundled(python3dist(retrying)) = 1.3.3
Provides: bundled(python3dist(requests)) = 2.19.1
Provides: bundled(python3dist(chardet)) = 3.0.4
Provides: bundled(python3dist(idna)) = 2.7
Provides: bundled(python3dist(urllib3)) = 1.23
Provides: bundled(python3dist(certifi)) = 2018.8.24
Provides: bundled(python3dist(setuptools)) = 40.4.3
Provides: bundled(python3dist(webencodings)) = 0.5.1

Provides: bundled(python3dist(setuptools)) = %{setuptools_version}
Provides: bundled(python3dist(packaging)) = 16.8
Provides: bundled(python3dist(pyparsing)) = 2.2.1
Provides: bundled(python3dist(six)) = 1.10
Provides: bundled(python3dist(appdirs)) = 1.4.3
%endif

# Provides for the bundled libmpdec
Provides: bundled(mpdecimal) = %{libmpdec_version}
Provides: bundled(libmpdec) = %{libmpdec_version}

# Provides of the subpackages contained in flatpackage
Provides: %{pkgname}-libs = %{version}-%{release}
Provides: %{pkgname}-devel = %{version}-%{release}
Provides: %{pkgname}-idle = %{version}-%{release}
Provides: %{pkgname}-tkinter = %{version}-%{release}
Provides: %{pkgname}-test = %{version}-%{release}
%if %{with debug_build}
Provides: %{pkgname}-debug = %{version}-%{release}
%endif

# The description for the flat package
%description
Python %{pybasever} package for developers.

This package exists to allow developers to test their code against an older
version of Python. This is not a full Python stack and if you wish to run
your applications with Python %{pybasever}, see other distributions
that support it, such as CentOS or RHEL with Software Collections
or older Fedora releases.

%endif # with flatpackage

# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%gpgverify -k2 -s1 -d0
%autosetup -S git_am -N -n Python-%{upstream_version}

# Apply initial patches manually
%autopatch 1

%if "%{_lib}" == "lib64"
%autopatch 102
%endif

%autopatch 111
%autopatch 132
%autopatch 155
%autopatch 160
%autopatch 163
%autopatch 170

%if %{with rpmwheels}
%autopatch 189
rm Lib/ensurepip/_bundled/*.whl
%else
# Patch the bundled pip wheel for CVE-2007-4559
unzip -qq Lib/ensurepip/_bundled/pip-%{pip_version}-py2.py3-none-any.whl
patch -p1 < %{SOURCE101}
zip -rq Lib/ensurepip/_bundled/pip-%{pip_version}-py2.py3-none-any.whl pip pip-%{pip_version}.dist-info
rm -rf pip/ pip-%{pip_version}.dist-info/

# Patch the bundled setuptools wheel for CVE-2024-6345
unzip -qq Lib/ensurepip/_bundled/setuptools-%{setuptools_version}-py2.py3-none-any.whl
patch -p1 < %{SOURCE102}
zip -rq Lib/ensurepip/_bundled/setuptools-%{setuptools_version}-py2.py3-none-any.whl easy_install.py pkg_resources setuptools setuptools-%{setuptools_version}.dist-info
rm -rf easy_install.py pkg_resources/ setuptools/ setuptools-%{setuptools_version}.dist-info/
%endif

# Apply the remaining patches
%autopatch -m 190

# Remove bundled libraries to ensure that we're using the system copy.
rm -r Modules/expat
rm -r Modules/zlib

# Remove files that should be generated by the build
# (This is after patching, so that we can use patches directly from upstream)
rm configure pyconfig.h.in

# When we use the legacy arch names, we need to change them in configure.ac
%if %{with legacy_archnames}
sed -i configure.ac \
    -e 's/\b%{platform_triplet_upstream}\b/%{platform_triplet_legacy}/'
%endif


# ======================================================
# Configuring and building the code:
# ======================================================

%build

# The build process embeds version info extracted from the Git repository
# into the Py_GetBuildInfo and sys.version strings.
# Our Git repository is artificial, so we don't want that.
# Tell configure to not use git.
export HAS_GIT=not-found

# Regenerate the configure script and pyconfig.h.in
autoconf
autoheader

# Remember the current directory (which has sources and the configure script),
# so we can refer to it after we "cd" elsewhere.
topdir=$(pwd)

# Get proper option names from bconds
%if %{with computed_gotos}
%global computed_gotos_flag yes
%else
%global computed_gotos_flag no
%endif

%if %{with optimizations}
%global optimizations_flag "--enable-optimizations"
%else
%global optimizations_flag "--disable-optimizations"
%endif

# Set common compiler/linker flags
# We utilize the %%extension_...flags macros here so users building C/C++
# extensions with our python won't get all the compiler/linker flags used
# in Fedora RPMs.
# Standard library built here will still use the %%build_...flags,
# Fedora packages utilizing %%py3_build will use them as well
# https://fedoraproject.org/wiki/Changes/Python_Extension_Flags
# https://fedoraproject.org/wiki/Changes/Python_Extension_Flags_Reduction
export CFLAGS="%{extension_cflags}"
export CFLAGS_NODIST="%{build_cflags} -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="%{extension_cxxflags}"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="%{extension_cflags}"
export LINKCC="gcc"
export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
export LDFLAGS="%{extension_ldflags} $(pkg-config --libs-only-L openssl)"
export LDFLAGS_NODIST="%{build_ldflags} -g $(pkg-config --libs-only-L openssl)"

# We can build several different configurations of Python: regular and debug.
# Define a common function that does one build:
BuildPython() {
  ConfName=$1
  ExtraConfigArgs=$2
  MoreCFlags=$3

  # Each build is done in its own directory
  ConfDir=build/$ConfName
  echo STARTING: BUILD OF PYTHON FOR CONFIGURATION: $ConfName
  mkdir -p $ConfDir
  pushd $ConfDir

  # Normally, %%configure looks for the "configure" script in the current
  # directory.
  # Since we changed directories, we need to tell %%configure where to look.
  %global _configure $topdir/configure

%configure \
  --enable-ipv6 \
  --enable-shared \
  --with-computed-gotos=%{computed_gotos_flag} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-ffi \
  --enable-loadable-sqlite-extensions \
  --with-dtrace \
  --with-lto \
  --with-ssl-default-suites=openssl \
%if %{with valgrind}
  --with-valgrind \
%endif
  $ExtraConfigArgs \
  %{nil}

  # Regenerate generated importlib frozen modules (see patch 353)
  %make_build EXTRA_CFLAGS="$CFLAGS $MoreCFlags" regen-importlib

  # Invoke the build
  %make_build EXTRA_CFLAGS="$CFLAGS $MoreCFlags"

  popd
  echo FINISHED: BUILD OF PYTHON FOR CONFIGURATION: $ConfName
}

# Call the above to build each configuration.

%if %{with debug_build}
BuildPython debug \
  "--without-ensurepip --with-pydebug" \
  "-O0"
%endif # with debug_build

BuildPython optimized \
  "--without-ensurepip %{optimizations_flag}" \
  ""

# ======================================================
# Installing the built code:
# ======================================================

%install

# As in %%build, remember the current directory
topdir=$(pwd)

# We install a collection of hooks for gdb that make it easier to debug
# executables linked against libpython3* (such as /usr/bin/python3 itself)
#
# These hooks are implemented in Python itself (though they are for the version
# of python that gdb is linked with)
#
# gdb-archer looks for them in the same path as the ELF file or its .debug
# file, with a -gdb.py suffix.
# We put them next to the debug file, because ldconfig would complain if
# it found non-library files directly in /usr/lib/
# (see https://bugzilla.redhat.com/show_bug.cgi?id=562980)
#
# We'll put these files in the debuginfo package by installing them to e.g.:
#  /usr/lib/debug/usr/lib/libpython3.2.so.1.0.debug-gdb.py
# (note that the debug path is /usr/lib/debug for both 32/64 bit)
#
# See https://fedoraproject.org/wiki/Features/EasierPythonDebugging for more
# information

%if %{with gdb_hooks}
DirHoldingGdbPy=%{_prefix}/lib/debug/%{_libdir}
mkdir -p %{buildroot}$DirHoldingGdbPy
%endif # with gdb_hooks

# Multilib support for pyconfig.h
# 32- and 64-bit versions of pyconfig.h are different. For multilib support
# (making it possible to install 32- and 64-bit versions simultaneously),
# we need to install them under different filenames, and to make the common
# "pyconfig.h" include the right file based on architecture.
# See https://bugzilla.redhat.com/show_bug.cgi?id=192747
# Filanames are defined here:
%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h
%global _pyconfig_h pyconfig-%{wordsize}.h

# Use a common function to do an install for all our configurations:
InstallPython() {

  ConfName=$1
  PyInstSoName=$2
  MoreCFlags=$3
  LDVersion=$4

  # Switch to the directory with this configuration's built files
  ConfDir=build/$ConfName
  echo STARTING: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
  mkdir -p $ConfDir
  pushd $ConfDir

  %make_install EXTRA_CFLAGS="$MoreCFlags"

  popd

%if %{with gdb_hooks}
  # See comment on $DirHoldingGdbPy above
  PathOfGdbPy=$DirHoldingGdbPy/$PyInstSoName-%{version}-%{release}.%{_arch}.debug-gdb.py
  cp Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy
%endif # with gdb_hooks

  # Rename the -devel script that differs on different arches to arch specific name
  mv %{buildroot}%{_bindir}/python${LDVersion}-{,`uname -m`-}config
  echo -e '#!/bin/sh\nexec `dirname $0`/python'${LDVersion}'-`uname -m`-config "$@"' > \
    %{buildroot}%{_bindir}/python${LDVersion}-config
  echo '[ $? -eq 127 ] && echo "Could not find python'${LDVersion}'-`uname -m`-config. Look around to see available arches." >&2' >> \
    %{buildroot}%{_bindir}/python${LDVersion}-config
    chmod +x %{buildroot}%{_bindir}/python${LDVersion}-config

  # Make python3-devel multilib-ready
  mv %{buildroot}%{_includedir}/python${LDVersion}/pyconfig.h \
     %{buildroot}%{_includedir}/python${LDVersion}/%{_pyconfig_h}
  cat > %{buildroot}%{_includedir}/python${LDVersion}/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF

  echo FINISHED: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
}

# Install the "debug" build first; any common files will be overridden with
# later builds
%if %{with debug_build}
InstallPython debug \
  %{py_INSTSONAME_debug} \
  -O0 \
  %{LDVERSION_debug}
%endif # with debug_build

# Now the optimized build:
InstallPython optimized \
  %{py_INSTSONAME_optimized} \
  "" \
  %{LDVERSION_optimized}

# Install directories for additional packages
install -d -m 0755 %{buildroot}%{pylibdir}/site-packages/__pycache__
%if "%{_lib}" == "lib64"
# The 64-bit version needs to create "site-packages" in /usr/lib/ (for
# pure-Python modules) as well as in /usr/lib64/ (for packages with extension
# modules).
# Note that rpmlint will complain about hardcoded library path;
# this is intentional.
install -d -m 0755 %{buildroot}%{_prefix}/lib/python%{pybasever}/site-packages/__pycache__
%endif

%if %{with main_python}
# add idle3 to menu
install -D -m 0644 Lib/idlelib/Icons/idle_16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/idle3.png
install -D -m 0644 Lib/idlelib/Icons/idle_32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/idle3.png
install -D -m 0644 Lib/idlelib/Icons/idle_48.png %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/idle3.png
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE10}

# Install and validate appdata file
mkdir -p %{buildroot}%{_metainfodir}
cp -a %{SOURCE11} %{buildroot}%{_metainfodir}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/idle3.appdata.xml
%endif

# Make sure distutils looks at the right pyconfig.h file
# See https://bugzilla.redhat.com/show_bug.cgi?id=201434
# Similar for sysconfig: sysconfig.get_config_h_filename tries to locate
# pyconfig.h so it can be parsed, and needs to do this at runtime in site.py
# when python starts up (see https://bugzilla.redhat.com/show_bug.cgi?id=653058)
#
# Split this out so it goes directly to the pyconfig-32.h/pyconfig-64.h
# variants:
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/distutils/sysconfig.py \
  %{buildroot}%{pylibdir}/sysconfig.py

# Install pathfix.py to bindir
# See https://github.com/fedora-python/python-rpm-porting/issues/24
cp -p Tools/scripts/pathfix.py %{buildroot}%{_bindir}/

# Install i18n tools to bindir
# They are also in python2, so we version them
# https://bugzilla.redhat.com/show_bug.cgi?id=1571474
for tool in pygettext msgfmt; do
  cp -p Tools/i18n/${tool}.py %{buildroot}%{_bindir}/${tool}%{pybasever}.py
  ln -s ${tool}%{pybasever}.py %{buildroot}%{_bindir}/${tool}3.py
done

# Switch all shebangs to refer to the specific Python version.
# This currently only covers files matching ^[a-zA-Z0-9_]+\.py$,
# so handle files named using other naming scheme separately.
LD_LIBRARY_PATH=./build/optimized ./build/optimized/python \
  Tools/scripts/pathfix.py \
  -i "%{_bindir}/python%{pybasever}" -pn \
  %{buildroot} \
  %{buildroot}%{_bindir}/*%{pybasever}.py \
  %{?with_gdb_hooks:%{buildroot}$DirHoldingGdbPy/*.py}

# Remove tests for python3-tools which was removed in
# https://bugzilla.redhat.com/show_bug.cgi?id=1312030
rm -rf %{buildroot}%{pylibdir}/test/test_tools

# Remove shebang lines from .py files that aren't executable, and
# remove executability from .py files that don't have a shebang line:
find %{buildroot} -name \*.py \
  \( \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \; \
  -print -exec sed -i '1d' {} \; \) -o \( \
  -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \; \
  -exec chmod a-x {} \; \) \)

# Get rid of DOS batch files:
find %{buildroot} -name \*.bat -exec rm {} \;

# Get rid of backup files:
find %{buildroot}/ -name "*~" -exec rm -f {} \;
find . -name "*~" -exec rm -f {} \;

# Do bytecompilation with the newly installed interpreter.
# This is similar to the script in macros.pybytecompile
# Clamp the source mtime first, see https://fedoraproject.org/wiki/Changes/ReproducibleBuildsClampMtimes
# The clamp_source_mtime module is only guaranteed to exist on Fedoras that enabled this option:
%if 0%{?clamp_mtime_to_source_date_epoch}
LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
PYTHONPATH="%{_rpmconfigdir}/redhat" \
%{buildroot}%{_bindir}/python%{pybasever} -s -B -m clamp_source_mtime %{buildroot}%{pylibdir}
%endif
# compile *.pyc
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} -O -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2], optimize=opt) for opt in range(3) for f in sys.argv[1:]]' || :

# Since we have pathfix.py in bindir, this is created, but we don't want it
rm -rf %{buildroot}%{_bindir}/__pycache__

# Fixup permissions for shared libraries from non-standard 555 to standard 755:
find %{buildroot} -perm 555 -exec chmod 755 {} \;

# Create "/usr/bin/python3-debug", a symlink to the python3 debug binary, to
# avoid the user having to know the precise version and ABI flags.
# See e.g. https://bugzilla.redhat.com/show_bug.cgi?id=676748
%if %{with debug_build} && %{with main_python}
ln -s \
  %{_bindir}/python%{LDVERSION_debug} \
  %{buildroot}%{_bindir}/python3-debug
%endif

%if %{without rpmwheels}
# Inject SBOM into the installed wheels (if the macro is available)
%{?python_wheel_inject_sbom:%python_wheel_inject_sbom %{buildroot}%{pylibdir}/ensurepip/_bundled/*.whl}
%endif

%if %{without main_python}
# Remove stuff that would conflict with python3 package
rm %{buildroot}%{_bindir}/python3
rm %{buildroot}%{_bindir}/pydoc3
rm %{buildroot}%{_bindir}/pathfix.py
rm %{buildroot}%{_bindir}/pygettext3.py
rm %{buildroot}%{_bindir}/msgfmt3.py
rm %{buildroot}%{_bindir}/idle3
rm %{buildroot}%{_bindir}/python3-*
rm %{buildroot}%{_bindir}/pyvenv
rm %{buildroot}%{_bindir}/2to3*
rm %{buildroot}%{_libdir}/libpython3.so
rm %{buildroot}%{_mandir}/man1/python3.1*
rm %{buildroot}%{_libdir}/pkgconfig/python3.pc
%endif

# ======================================================
# Checks for packaging issues
# ======================================================

%check

# first of all, check timestamps of bytecode files
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} %{SOURCE8}

# Ensure that the curses module was linked against libncursesw.so, rather than
# libncurses.so
# See https://bugzilla.redhat.com/show_bug.cgi?id=539917
ldd %{buildroot}/%{dynload_dir}/_curses*.so \
    | grep curses \
    | grep libncurses.so && (echo "_curses.so linked against libncurses.so" ; exit 1)

# Ensure that the debug modules are linked against the debug libpython, and
# likewise for the optimized modules and libpython:
for Module in %{buildroot}/%{dynload_dir}/*.so ; do
    case $Module in
    *.%{SOABI_debug})
        ldd $Module | grep %{py_INSTSONAME_optimized} &&
            (echo Debug module $Module linked against optimized %{py_INSTSONAME_optimized} ; exit 1)

        ;;
    *.%{SOABI_optimized})
        ldd $Module | grep %{py_INSTSONAME_debug} &&
            (echo Optimized module $Module linked against debug %{py_INSTSONAME_debug} ; exit 1)
        ;;
    esac
done

# Verify that the bundled libmpdec version python was compiled with, is the same version we have virtual
# provides for in the SPEC.
test "$(LD_LIBRARY_PATH=$(pwd)/build/optimized $(pwd)/build/optimized/python -c 'import decimal; print(decimal.__libmpdec_version__)')" = \
     "%{libmpdec_version}"

# ======================================================
# Running the upstream test suite
# ======================================================

topdir=$(pwd)
CheckPython() {
  ConfName=$1
  ConfDir=$(pwd)/build/$ConfName

  # The "modern" security policies are not handled gracefully by the test suite
  # of an older Python version. This is fixed upstream for 3.7+.
  # Instead of fixing the tests, we disable the system wide policy via:
  export OPENSSL_CONF=/non-existing-file
  # This is a compromise between skipping and fixing the ssl tests.

  echo STARTING: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

  # Note that we're running the tests using the version of the code in the
  # builddir, not in the buildroot.

  # Run the upstream test suite, setting "WITHIN_PYTHON_RPM_BUILD" so that the
  # our non-standard decorators take effect on the relevant tests:
  #   @unittest._skipInRpmBuild(reason)
  #   @unittest._expectedFailureInRpmBuild
  # test_faulthandler.test_register_chain currently fails on ppc64le and
  #   aarch64, see upstream bug http://bugs.python.org/issue21131
  WITHIN_PYTHON_RPM_BUILD= \
  LD_LIBRARY_PATH=$ConfDir $ConfDir/python -m test.regrtest \
    -wW --slowest --findleaks \
    -x test_distutils \
    -x test_bdist_rpm \
    -x test_gdb \
    %ifarch ppc64le aarch64
    -x test_faulthandler \
    %endif
    %ifarch %{mips64}
    -x test_ctypes \
    %endif
    %ifarch ppc64le
    -x test_buffer \
    %endif

  echo FINISHED: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

}

%if %{with tests}

# Check each of the configurations:
%if %{with debug_build}
CheckPython debug
%endif # with debug_build
CheckPython optimized

%endif # with tests


%files
%doc README.rst

%if %{without flatpackage}
%if %{with main_python}
%{_bindir}/pydoc*
%{_bindir}/python3
%{_bindir}/pyvenv
%{_mandir}/*/*
%else
%{_bindir}/pydoc%{pybasever}
%{_mandir}/*/python%{pybasever}*
%endif
%else
%{_bindir}/pydoc%{pybasever}
%{_mandir}/*/python%{pybasever}*
%endif
%{_bindir}/pyvenv-%{pybasever}
%{_bindir}/python%{pybasever}
%{_bindir}/python%{pybasever}m

%if %{without flatpackage}
%files libs
%doc README.rst
%endif

%dir %{pylibdir}
%dir %{dynload_dir}

%license %{pylibdir}/LICENSE.txt

%{pylibdir}/lib2to3
%if %{without flatpackage}
%exclude %{pylibdir}/lib2to3/tests
%endif

%dir %{pylibdir}/unittest/
%dir %{pylibdir}/unittest/__pycache__/
%{pylibdir}/unittest/*.py
%{pylibdir}/unittest/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/asyncio/
%dir %{pylibdir}/asyncio/__pycache__/
%{pylibdir}/asyncio/*.py
%{pylibdir}/asyncio/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/venv/
%dir %{pylibdir}/venv/__pycache__/
%{pylibdir}/venv/*.py
%{pylibdir}/venv/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/venv/scripts

%{pylibdir}/wsgiref
%{pylibdir}/xmlrpc

%dir %{pylibdir}/ensurepip/
%dir %{pylibdir}/ensurepip/__pycache__/
%{pylibdir}/ensurepip/*.py
%{pylibdir}/ensurepip/__pycache__/*%{bytecode_suffixes}

%if %{with rpmwheels}
%exclude %{pylibdir}/ensurepip/_bundled
%else
%dir %{pylibdir}/ensurepip/_bundled
%{pylibdir}/ensurepip/_bundled/*.whl
%endif

%dir %{pylibdir}/test/
%dir %{pylibdir}/test/__pycache__/
%dir %{pylibdir}/test/support/
%dir %{pylibdir}/test/support/__pycache__/
%{pylibdir}/test/__init__.py
%{pylibdir}/test/__pycache__/__init__%{bytecode_suffixes}
%{pylibdir}/test/support/__init__.py
%{pylibdir}/test/support/__pycache__/__init__%{bytecode_suffixes}

%dir %{pylibdir}/concurrent/
%dir %{pylibdir}/concurrent/__pycache__/
%{pylibdir}/concurrent/*.py
%{pylibdir}/concurrent/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/concurrent/futures/
%dir %{pylibdir}/concurrent/futures/__pycache__/
%{pylibdir}/concurrent/futures/*.py
%{pylibdir}/concurrent/futures/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/pydoc_data

%{dynload_dir}/_blake2.%{SOABI_optimized}.so
%{dynload_dir}/_md5.%{SOABI_optimized}.so
%{dynload_dir}/_sha1.%{SOABI_optimized}.so
%{dynload_dir}/_sha256.%{SOABI_optimized}.so
%{dynload_dir}/_sha3.%{SOABI_optimized}.so
%{dynload_dir}/_sha512.%{SOABI_optimized}.so

%{dynload_dir}/_asyncio.%{SOABI_optimized}.so
%{dynload_dir}/_bisect.%{SOABI_optimized}.so
%{dynload_dir}/_bz2.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_cn.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_hk.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_iso2022.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_jp.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_kr.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_tw.%{SOABI_optimized}.so
%{dynload_dir}/_crypt.%{SOABI_optimized}.so
%{dynload_dir}/_csv.%{SOABI_optimized}.so
%{dynload_dir}/_ctypes.%{SOABI_optimized}.so
%{dynload_dir}/_curses.%{SOABI_optimized}.so
%{dynload_dir}/_curses_panel.%{SOABI_optimized}.so
%{dynload_dir}/_dbm.%{SOABI_optimized}.so
%{dynload_dir}/_decimal.%{SOABI_optimized}.so
%{dynload_dir}/_elementtree.%{SOABI_optimized}.so
%if %{with gdbm}
%{dynload_dir}/_gdbm.%{SOABI_optimized}.so
%endif
%{dynload_dir}/_hashlib.%{SOABI_optimized}.so
%{dynload_dir}/_heapq.%{SOABI_optimized}.so
%{dynload_dir}/_json.%{SOABI_optimized}.so
%{dynload_dir}/_lsprof.%{SOABI_optimized}.so
%{dynload_dir}/_lzma.%{SOABI_optimized}.so
%{dynload_dir}/_multibytecodec.%{SOABI_optimized}.so
%{dynload_dir}/_multiprocessing.%{SOABI_optimized}.so
%{dynload_dir}/_opcode.%{SOABI_optimized}.so
%{dynload_dir}/_pickle.%{SOABI_optimized}.so
%{dynload_dir}/_posixsubprocess.%{SOABI_optimized}.so
%{dynload_dir}/_random.%{SOABI_optimized}.so
%{dynload_dir}/_socket.%{SOABI_optimized}.so
%{dynload_dir}/_sqlite3.%{SOABI_optimized}.so
%{dynload_dir}/_ssl.%{SOABI_optimized}.so
%{dynload_dir}/_struct.%{SOABI_optimized}.so
%{dynload_dir}/array.%{SOABI_optimized}.so
%{dynload_dir}/audioop.%{SOABI_optimized}.so
%{dynload_dir}/binascii.%{SOABI_optimized}.so
%{dynload_dir}/cmath.%{SOABI_optimized}.so
%{dynload_dir}/_datetime.%{SOABI_optimized}.so
%{dynload_dir}/fcntl.%{SOABI_optimized}.so
%{dynload_dir}/grp.%{SOABI_optimized}.so
%{dynload_dir}/math.%{SOABI_optimized}.so
%{dynload_dir}/mmap.%{SOABI_optimized}.so
%{dynload_dir}/nis.%{SOABI_optimized}.so
%{dynload_dir}/ossaudiodev.%{SOABI_optimized}.so
%{dynload_dir}/parser.%{SOABI_optimized}.so
%{dynload_dir}/pyexpat.%{SOABI_optimized}.so
%{dynload_dir}/readline.%{SOABI_optimized}.so
%{dynload_dir}/resource.%{SOABI_optimized}.so
%{dynload_dir}/select.%{SOABI_optimized}.so
%{dynload_dir}/spwd.%{SOABI_optimized}.so
%{dynload_dir}/syslog.%{SOABI_optimized}.so
%{dynload_dir}/termios.%{SOABI_optimized}.so
%{dynload_dir}/_testmultiphase.%{SOABI_optimized}.so
%{dynload_dir}/unicodedata.%{SOABI_optimized}.so
%{dynload_dir}/xxlimited.%{SOABI_optimized}.so
%{dynload_dir}/zlib.%{SOABI_optimized}.so

%dir %{pylibdir}/site-packages/
%dir %{pylibdir}/site-packages/__pycache__/
%{pylibdir}/site-packages/README.txt

%exclude %{pylibdir}/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}.py
%exclude %{pylibdir}/__pycache__/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}%{bytecode_suffixes}

%{pylibdir}/*.py
%dir %{pylibdir}/__pycache__/
%{pylibdir}/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/collections/
%dir %{pylibdir}/collections/__pycache__/
%{pylibdir}/collections/*.py
%{pylibdir}/collections/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/ctypes/
%dir %{pylibdir}/ctypes/__pycache__/
%{pylibdir}/ctypes/*.py
%{pylibdir}/ctypes/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/ctypes/macholib

%{pylibdir}/curses

%dir %{pylibdir}/dbm/
%dir %{pylibdir}/dbm/__pycache__/
%{pylibdir}/dbm/*.py
%{pylibdir}/dbm/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/distutils/
%dir %{pylibdir}/distutils/__pycache__/
%{pylibdir}/distutils/*.py
%{pylibdir}/distutils/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/distutils/README
%{pylibdir}/distutils/command
%exclude %{pylibdir}/distutils/command/wininst-*.exe

%dir %{pylibdir}/email/
%dir %{pylibdir}/email/__pycache__/
%{pylibdir}/email/*.py
%{pylibdir}/email/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/email/mime
%doc %{pylibdir}/email/architecture.rst

%{pylibdir}/encodings

%{pylibdir}/html
%{pylibdir}/http

%dir %{pylibdir}/importlib/
%dir %{pylibdir}/importlib/__pycache__/
%{pylibdir}/importlib/*.py
%{pylibdir}/importlib/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/json/
%dir %{pylibdir}/json/__pycache__/
%{pylibdir}/json/*.py
%{pylibdir}/json/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/logging
%{pylibdir}/multiprocessing

%dir %{pylibdir}/sqlite3/
%dir %{pylibdir}/sqlite3/__pycache__/
%{pylibdir}/sqlite3/*.py
%{pylibdir}/sqlite3/__pycache__/*%{bytecode_suffixes}

%if %{without flatpackage}
%exclude %{pylibdir}/turtle.py
%exclude %{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}
%endif

%{pylibdir}/urllib
%{pylibdir}/xml

%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages/__pycache__/
%endif

# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%dir %{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/
%{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/Makefile
%dir %{_includedir}/python%{LDVERSION_optimized}/
%{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}

%{_libdir}/%{py_INSTSONAME_optimized}
%if %{with main_python}
%{_libdir}/libpython3.so
%endif

%if %{without flatpackage}
%files devel
%if %{with main_python}
%{_bindir}/2to3
# TODO: Remove 2to3-3.7 once rebased to 3.7
%{_bindir}/2to3-%{pybasever}
%endif
%endif

%{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/*
%if %{without flatpackage}
%exclude %{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/Makefile
%exclude %{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}
%endif
%exclude %{pylibdir}/distutils/command/wininst-*.exe
%{_includedir}/python%{LDVERSION_optimized}/*.h
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit

%if %{with main_python}
%{_bindir}/python3-config
%{_libdir}/pkgconfig/python3.pc
%{_bindir}/pathfix.py
%{_bindir}/pygettext3.py
%{_bindir}/msgfmt3.py
%endif

%{_bindir}/pygettext%{pybasever}.py
%{_bindir}/msgfmt%{pybasever}.py

%{_bindir}/python%{pybasever}-config
%{_bindir}/python%{LDVERSION_optimized}-config
%{_bindir}/python%{LDVERSION_optimized}-*-config
%{_libdir}/libpython%{LDVERSION_optimized}.so
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}.pc
%{_libdir}/pkgconfig/python-%{pybasever}.pc

%if %{without flatpackage}
%files idle

%{_bindir}/idle*
%else
%{_bindir}/idle%{pybasever}
%endif

%{pylibdir}/idlelib

%if %{with main_python}
%{_metainfodir}/idle3.appdata.xml
%{_datadir}/applications/idle3.desktop
%{_datadir}/icons/hicolor/*/apps/idle3.*
%endif

%if %{without flatpackage}
%files tkinter
%endif

%{pylibdir}/tkinter
%if %{without flatpackage}
%exclude %{pylibdir}/tkinter/test
%endif
%{dynload_dir}/_tkinter.%{SOABI_optimized}.so
%{pylibdir}/turtle.py
%{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}
%dir %{pylibdir}/turtledemo
%{pylibdir}/turtledemo/*.py
%{pylibdir}/turtledemo/*.cfg
%dir %{pylibdir}/turtledemo/__pycache__/
%{pylibdir}/turtledemo/__pycache__/*%{bytecode_suffixes}

%if %{without flatpackage}
%files test
%endif
%{pylibdir}/ctypes/test
%{pylibdir}/distutils/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test
%{dynload_dir}/_ctypes_test.%{SOABI_optimized}.so
%{dynload_dir}/_testbuffer.%{SOABI_optimized}.so
%{dynload_dir}/_testcapi.%{SOABI_optimized}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_optimized}.so
%{pylibdir}/lib2to3/tests
%{pylibdir}/tkinter/test
%{pylibdir}/unittest/test


# We don't bother splitting the debug build out into further subpackages:
# if you need it, you're probably a developer.

# Hence the manifest is the combination of analogous files in the manifests of
# all of the other subpackages

%if %{with debug_build}
%if %{without flatpackage}
%files debug
%if %{with main_python}
%{_bindir}/python3-debug
%endif
%endif

# Analog of the core subpackage's files:
%{_bindir}/python%{LDVERSION_debug}

# Analog of the -libs subpackage's files:
# ...with debug builds of the built-in "extension" modules:

%{dynload_dir}/_blake2.%{SOABI_debug}.so
%{dynload_dir}/_md5.%{SOABI_debug}.so
%{dynload_dir}/_sha1.%{SOABI_debug}.so
%{dynload_dir}/_sha256.%{SOABI_debug}.so
%{dynload_dir}/_sha3.%{SOABI_debug}.so
%{dynload_dir}/_sha512.%{SOABI_debug}.so

%{dynload_dir}/_asyncio.%{SOABI_debug}.so
%{dynload_dir}/_bisect.%{SOABI_debug}.so
%{dynload_dir}/_bz2.%{SOABI_debug}.so
%{dynload_dir}/_codecs_cn.%{SOABI_debug}.so
%{dynload_dir}/_codecs_hk.%{SOABI_debug}.so
%{dynload_dir}/_codecs_iso2022.%{SOABI_debug}.so
%{dynload_dir}/_codecs_jp.%{SOABI_debug}.so
%{dynload_dir}/_codecs_kr.%{SOABI_debug}.so
%{dynload_dir}/_codecs_tw.%{SOABI_debug}.so
%{dynload_dir}/_crypt.%{SOABI_debug}.so
%{dynload_dir}/_csv.%{SOABI_debug}.so
%{dynload_dir}/_ctypes.%{SOABI_debug}.so
%{dynload_dir}/_curses.%{SOABI_debug}.so
%{dynload_dir}/_curses_panel.%{SOABI_debug}.so
%{dynload_dir}/_dbm.%{SOABI_debug}.so
%{dynload_dir}/_decimal.%{SOABI_debug}.so
%{dynload_dir}/_elementtree.%{SOABI_debug}.so
%if %{with gdbm}
%{dynload_dir}/_gdbm.%{SOABI_debug}.so
%endif
%{dynload_dir}/_hashlib.%{SOABI_debug}.so
%{dynload_dir}/_heapq.%{SOABI_debug}.so
%{dynload_dir}/_json.%{SOABI_debug}.so
%{dynload_dir}/_lsprof.%{SOABI_debug}.so
%{dynload_dir}/_lzma.%{SOABI_debug}.so
%{dynload_dir}/_multibytecodec.%{SOABI_debug}.so
%{dynload_dir}/_multiprocessing.%{SOABI_debug}.so
%{dynload_dir}/_opcode.%{SOABI_debug}.so
%{dynload_dir}/_pickle.%{SOABI_debug}.so
%{dynload_dir}/_posixsubprocess.%{SOABI_debug}.so
%{dynload_dir}/_random.%{SOABI_debug}.so
%{dynload_dir}/_socket.%{SOABI_debug}.so
%{dynload_dir}/_sqlite3.%{SOABI_debug}.so
%{dynload_dir}/_ssl.%{SOABI_debug}.so
%{dynload_dir}/_struct.%{SOABI_debug}.so
%{dynload_dir}/array.%{SOABI_debug}.so
%{dynload_dir}/audioop.%{SOABI_debug}.so
%{dynload_dir}/binascii.%{SOABI_debug}.so
%{dynload_dir}/cmath.%{SOABI_debug}.so
%{dynload_dir}/_datetime.%{SOABI_debug}.so
%{dynload_dir}/fcntl.%{SOABI_debug}.so
%{dynload_dir}/grp.%{SOABI_debug}.so
%{dynload_dir}/math.%{SOABI_debug}.so
%{dynload_dir}/mmap.%{SOABI_debug}.so
%{dynload_dir}/nis.%{SOABI_debug}.so
%{dynload_dir}/ossaudiodev.%{SOABI_debug}.so
%{dynload_dir}/parser.%{SOABI_debug}.so
%{dynload_dir}/pyexpat.%{SOABI_debug}.so
%{dynload_dir}/readline.%{SOABI_debug}.so
%{dynload_dir}/resource.%{SOABI_debug}.so
%{dynload_dir}/select.%{SOABI_debug}.so
%{dynload_dir}/spwd.%{SOABI_debug}.so
%{dynload_dir}/syslog.%{SOABI_debug}.so
%{dynload_dir}/termios.%{SOABI_debug}.so
%{dynload_dir}/_testmultiphase.%{SOABI_debug}.so
%{dynload_dir}/unicodedata.%{SOABI_debug}.so
%{dynload_dir}/zlib.%{SOABI_debug}.so

%{pylibdir}/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}.py
%{pylibdir}/__pycache__/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}%{bytecode_suffixes}

# No need to split things out the "Makefile" and the config-32/64.h file as we
# do for the regular build above (bug 531901), since they're all in one package
# now; they're listed below, under "-devel":

%{_libdir}/%{py_INSTSONAME_debug}

# Analog of the -devel subpackage's files:
%{pylibdir}/config-%{LDVERSION_debug}-%{platform_triplet}
%{_includedir}/python%{LDVERSION_debug}
%{_bindir}/python%{LDVERSION_debug}-config
%{_bindir}/python%{LDVERSION_debug}-*-config
%{_libdir}/libpython%{LDVERSION_debug}.so
%{_libdir}/libpython%{LDVERSION_debug}.so.1.0
%{_libdir}/pkgconfig/python-%{LDVERSION_debug}.pc

# Analog of the -tools subpackage's files:
#  None for now; we could build precanned versions that have the appropriate
# shebang if needed

# Analog  of the tkinter subpackage's files:
%{dynload_dir}/_tkinter.%{SOABI_debug}.so

# Analog  of the -test subpackage's files:
%{dynload_dir}/_ctypes_test.%{SOABI_debug}.so
%{dynload_dir}/_testbuffer.%{SOABI_debug}.so
%{dynload_dir}/_testcapi.%{SOABI_debug}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_debug}.so

%endif # with debug_build

# We put the debug-gdb.py file inside /usr/lib/debug to avoid noise from ldconfig
# See https://bugzilla.redhat.com/show_bug.cgi?id=562980
#
# The /usr/lib/rpm/redhat/macros defines %%__debug_package to use
# debugfiles.list, and it appears that everything below /usr/lib/debug and
# (/usr/src/debug) gets added to this file (via LISTFILES) in
# /usr/lib/rpm/find-debuginfo.sh
#
# Hence by installing it below /usr/lib/debug we ensure it is added to the
# -debuginfo subpackage
# (if it doesn't, then the rpmbuild ought to fail since the debug-gdb.py
# payload file would be unpackaged)

# Workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1476593
%undefine _debuginfo_subpackages

# ======================================================
# Finally, the changelog:
# ======================================================

%changelog
* Thu Jan 29 2026 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-52
- Security fixes for CVE-2026-0865, CVE-2025-15366, CVE-2025-15367, CVE-2026-1299

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 06 2025 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-50
- On Fedora 44+, split this package into multiple subpackages
- This mimics newer Python versions

* Mon Aug 11 2025 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-49
- Security fix for CVE-2025-8194

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 26 2025 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-47
- Security fixes for CVE-2025-4517, CVE-2025-4330, CVE-2025-4138, CVE-2024-12718, CVE-2025-4435

* Wed Apr 23 2025 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-46
- Add RPM Provides for python3.6-libs, python3.6-devel, python3.6-idle, python3.6-tkinter, python3.6-test

* Wed Apr 16 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-45
- Fix the flakiness of test_ftplib

* Tue Apr 01 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-44
- Properly apply exported CFLAGS for dtrace/systemtap builds
- Fixes: rhbz#2356306

* Fri Feb 14 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-43
- Security fix CVE-2025-0938
- Fixes: rhbz#2343277

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 3.6.15-42
- Add explicit BR: libxcrypt-devel

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 18 2024 Victor Stinner <vstinner@python.org> - 3.6.15-40
- Fix compatibility with glibc 2.41 (resolve sinpi name clash).

* Thu Nov 14 2024 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-39
- Security fix for CVE-2024-11168

* Mon Nov 04 2024 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-38
- Security fix for CVE-2024-9287 (rhbz#2321659)

* Thu Sep 05 2024 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-37
- Security fix for CVE-2024-6232 (rhbz#2310092)

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 3.6.15-36
- convert license to SPDX

* Fri Aug 16 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.6.15-35
- Security fix for CVE-2024-6923 (rhbz#2303161)

* Thu Aug 01 2024 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-34
- Security fix for CVE-2024-6345 (in bundled setuptools wheel)

* Tue Jul 23 2024 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-33
- Require systemtap-sdt-devel for sys/sdt.h

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-31
- Security fix for CVE-2024-4032 (rhbz#2293394)

* Wed Apr 24 2024 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-30
- Security fix for CVE-2024-0450 and CVE-2023-6597

* Mon Mar 11 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-29
- Support OpenSSL 3
- Fixes: rhbz#2254550

* Thu Mar 07 2024 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-28
- Fix build on riscv64

* Thu Feb 29 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-27
- Security fix for CVE-2007-4559
- Fixes: rhbz#2141080

* Wed Feb 28 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-26
- Fix tests for XMLPullParser with Expat 2.6.0

* Mon Jan 29 2024 Karolina Surma <ksurma@redhat.com> - 3.6.15-25
- Fix test_zlib when building with zlib-ng-compat

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-22
- Security fix for CVE-2023-27043 (rhbz#2196191)

* Tue Nov 28 2023 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-21
- Fix implicit-function-declarations in configure
- Fixes: rhbz#2147519

* Wed Aug 02 2023 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-20
- Remove extra distro-applied CFLAGS passed to user built C extensions
- https://fedoraproject.org/wiki/Changes/Python_Extension_Flags_Reduction

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 26 2023 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-18
- Security fix for CVE-2023-24329
- Resolves: rhbz#2174013

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-16
- Ensure the source mtime is clamped to $SOURCE_DATE_EPOCH before bytecompilation

* Mon Dec 19 2022 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-15
- Security fix for CVE-2022-45061: CPU denial of service via inefficient IDNA decoder
  Related: rhbz#2144072

* Thu Nov 10 2022 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-14
- CVE-2022-37454: Fix buffer overflows in _sha3 module
  Related: rhbz#2140200

* Wed Oct 05 2022 Victor Stinner <vstinner@python.org> - 3.6.15-13
- Prevent denial of service (DoS) by very large integers.
  Resolves: rhbz#1834423

* Wed Sep 14 2022 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-12
- Fix for CVE-2021-28861
Resolves: rhbz#2120785

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-10
- Fix test_tarfile on ppc64le
Resolves: rhbz#2109120

* Fri Jun 10 2022 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-9
- Security fix for CVE-2015-20107
Resolves: rhbz#2075390

* Thu Mar 03 2022 Charalampos Stratakis <cstratak@redhat.com> - 3.6.15-8
- Fix the test suite support for Expat >= 2.4.5
Resolves: rhbz#2056970

* Wed Feb 16 2022 Lumír Balhar <lbalhar@redhat.com> - 3.6.15-7
- Switch from system wheels to bundled ones

* Tue Jan 25 2022 Karolina Surma <ksurma@redhat.com> - 3.6.15-6
- Fix test to enable build with i686
Resolves: rhbz#2038843

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 3.6.15-3
- Rebuild(libnsl2)

* Mon Sep 20 2021 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-2
- Explicitly buildrequire OpenSSL 1.1, as Python 3.6 is not compatible with OpenSSL 3.0

* Sun Sep 05 2021 Miro Hrončok <mhroncok@redhat.com> - 3.6.15-1
- Update to 3.6.15

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Tomas Hrnciar <thrnciar@redhat.com> - 3.6.14-1
- Update to 3.6.14

* Fri May 14 2021 Charalampos Stratakis <cstratak@redhat.com> - 3.6.13-3
- Add virtual provides for the bundled libmpdec (rhbz#1943359)

* Thu Feb 25 2021 Petr Viktorin <pviktori@redhat.com> - 3.6.13-2
- Fix alignment issue causing failures on x86-64
  Resolves: https://bugzilla.redhat.com/show_bug.cgi?id=1923658

* Tue Feb 16 2021 Tomas Hrnciar <thrnciar@redhat.com> - 3.6.13-1
- Update to 3.6.13

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 05 2020 Miro Hrončok <mhroncok@redhat.com> - 3.6.12-3
- Use upstream architecture names on Fedora 34+
- https://fedoraproject.org/wiki/Changes/Python_Upstream_Architecture_Names

* Mon Sep 21 2020 Miro Hrončok <mhroncok@redhat.com> - 3.6.12-2
- Rebuilt for new %%extension flags
- Fixes: rhbz#1877652

* Wed Aug 19 2020 Tomas Hrnciar <thrnciar@redhat.com> - 3.6.12-1
- Update to 3.6.12

* Wed Aug 12 2020 Petr Viktorin <pviktori@redhat.com> - 3.6.11-5
- In sys.version and initial REPL message, list the source commit as "default"

* Mon Aug 03 2020 Lumír Balhar <lbalhar@redhat.com> - 3.6.11-4
- Add support for upstream architectures' names (patch 353)

* Fri Jul 31 2020 Charalampos Stratakis <cstratak@redhat.com> - 3.6.11-3
- Avoid infinite loop when reading specially crafted TAR files (CVE-2019-20907)
Resolves: rhbz#1856481
- Resolve hash collisions for Pv4Interface and IPv6Interface (CVE-2020-14422)
Resolves: rhbz#1854926

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Petr Viktorin <pviktori@redhat.com> - 3.6.11-1
- Update to 3.6.11 final

* Thu Jun 25 2020 Victor Stinner <vstinner@python.org> - 3.6.11~rc1-2
- Remove downstream 00178-dont-duplicate-flags-in-sysconfig.patch which
  introduced a bug on distutils.sysconfig.get_config_var('LIBPL')
  (rhbz#1851008).

* Fri Jun 19 2020 Petr Viktorin <pviktori@redhat.com> - 3.6.11-1
- Update to 3.6.11rc1

* Thu May 28 2020 Victor Stinner <vstinner@python.org> - 3.6.10-5
- Fix python3-config --configdir (rhbz#1772988).

* Wed May 06 2020 Miro Hrončok <mhroncok@redhat.com> - 3.6.10-4
- Rename from python36 to python3.6

* Wed Feb 12 2020 Miro Hrončok <mhroncok@redhat.com> - 3.6.10-3
- Update the ensurepip module to work with setuptools >= 45

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.10-1
- Update to 3.6.10

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.9-1
- Update to 3.6.9

* Mon Feb 18 2019 Miro Hrončok <mhroncok@redhat.com> - 3.6.8-6
- Reduced default build flags used to build extension modules
  https://fedoraproject.org/wiki/Changes/Python_Extension_Flags

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6.8-5
- Rebuild for readline 8.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Patrik Kopkan <pkopkan@redhat.com> - 3.6.8-3
- fix for CVE-2019-5010 (#1666519, #1666520)

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 3.6.8-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Dec 27 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.8-1
- Update to 3.6.8

* Mon Oct 22 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.7-1
- Update to 3.6.7

* Mon Sep 24 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.6-6
- Security fix for CVE-2018-14647 (#1631822)

* Fri Aug 17 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.6-5
- Add /usr/bin/pygettext3.py and msgfmt3.py to python3-devel
Resolves: rhbz#1571474

* Wed Aug 15 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.6-4
- Use RPM built wheels of pip and setuptools in ensurepip instead of our rewheel patch

* Fri Aug 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6.6-3
- Fix wrong requirement on gdbm

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Charalampos Stratakis <cstratak@redhat.com> - 3.6.6-1
- Update to Python 3.6.6

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 3.6.5-5
- Introduce python36 package
