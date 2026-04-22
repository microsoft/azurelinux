# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# ==================
# Top-level metadata
# ==================

%global pybasever 3.9

# pybasever without the dot:
%global pyshortver 39

Name: python%{pybasever}
Summary: Version %{pybasever} of the Python interpreter
URL: https://www.python.org/

#  WARNING  When rebasing to a new Python version,
#           remember to update the python3-docs package as well
%global general_version %{pybasever}.25
#global prerel ...
%global upstream_version %{general_version}%{?prerel}
Version: %{general_version}%{?prerel:~%{prerel}}
Release: 7%{?dist}
License: Python


# ==================================
# Conditionals controlling the build
# ==================================

# Note that the bcond macros are named for the CLI option they create.
# "%%bcond_without" means "ENABLE by default and create a --without option"

# Main Python, i.e. whether this is the main Python version in the distribution
# that owns /usr/bin/python3 and other unique paths
# This also means the built subpackages are called python3 rather than python3X
# WARNING: This also influences the flatpackage bcond below.
# By default, this is determined by the %%__default_python3_pkgversion value
%if "%{?__default_python3_pkgversion}" == "%{pybasever}"
%bcond_without main_python
%else
%bcond_with main_python
%endif

# Flat package, i.e. no separate subpackages
# Default (in Fedora >= 44): disabled
# Default (in Fedora < 44): enabled when this is not the main Python
# Not supported: Combination of flatpackage enabled and main_python enabled
%if %{with main_python} || 0%{?fedora} >= 44
%bcond_with flatpackage
%else
%bcond_without flatpackage
%endif

# When bootstrapping python3, we need to build setuptools.
# but setuptools BR python3-devel and that brings in python3-rpm-generators;
# python3-rpm-generators needs python3-setuptools, so we cannot have it yet.
#
# We also use the previous build of Python in "make regen-all"
# and in "distutils.tests.test_bdist_rpm".
#
# Procedure: https://fedoraproject.org/wiki/SIGs/Python/UpgradingPython
#
#   IMPORTANT: When bootstrapping, it's very likely the wheels for pip and
#   setuptools are not available. Turn off the rpmwheels bcond until
#   the two packages are built with wheels to get around the issue.
%bcond_with bootstrap

# Whether to use RPM build wheels from the python-{pip,setuptools}-wheel package
# Uses upstream bundled prebuilt wheels otherwise
%bcond_without rpmwheels

# Expensive optimizations (mainly, profile-guided optimizations)
%bcond_without optimizations

# https://fedoraproject.org/wiki/Changes/PythonNoSemanticInterpositionSpeedup
%bcond_without no_semantic_interposition

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

# In RHEL 9+, we obsolete/provide Platform Python from regular Python
# This is only appropriate for the main Python build
%if 0%{?rhel} >= 9 && %{with main_python}
%bcond_without rhel8_compat_shims
%else
%bcond_with rhel8_compat_shims
%endif


# =====================
# General global macros
# =====================
%if %{with main_python}
%global pkgname python3
%global exename python3
%else
%global pkgname python%{pybasever}
%global exename python%{pybasever}
%endif

%global pylibdir %{_libdir}/python%{pybasever}
%global dynload_dir %{pylibdir}/lib-dynload

# ABIFLAGS, LDVERSION and SOABI are in the upstream configure.ac
# See PEP 3149 for some background: http://www.python.org/dev/peps/pep-3149/
%global ABIFLAGS_optimized %{nil}
%global ABIFLAGS_debug     d

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
%global libmpdec_version 2.5.0

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

# When a main_python build is attempted despite the %%__default_python3_pkgversion value
# We undefine magic macros so the python3-... package does not provide wrong python3X-...
%if %{with main_python} && ("%{?__default_python3_pkgversion}" != "%{pybasever}")
%undefine __pythonname_provides
%{warn:Doing a main_python build with wrong %%__default_python3_pkgversion (0%{?__default_python3_pkgversion}, but this is %pyshortver)}
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
# See the runtime requirement in the -libs subpackage
BuildRequires: expat-devel >= 2.6

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
BuildRequires: libuuid-devel
BuildRequires: libxcrypt-devel
BuildRequires: libX11-devel
BuildRequires: make
BuildRequires: ncurses-devel

BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: redhat-rpm-config >= 127
BuildRequires: sqlite-devel
BuildRequires: gdb

BuildRequires: tar
BuildRequires: tcl-devel < 1:9
BuildRequires: tix-devel
BuildRequires: tk-devel < 1:9
BuildRequires: tzdata

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

%if %{without bootstrap}
# for make regen-all and distutils.tests.test_bdist_rpm
BuildRequires: python%{pybasever}
# for proper automatic provides
BuildRequires: python3-rpm-generators
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

# (Patches taken from github.com/fedora-python/cpython)

# 00001 # d06a8853cf4bae9e115f45e1d531d2dc152c5cc8
# Fixup distutils/unixccompiler.py to remove standard library path from rpath
#
# Was Patch0 in ivazquez' python3000 specfile
Patch1: 00001-rpath.patch

# 00111 # 93b40d73360053ca68b0aeec33b6a8ca167e33e2
# Don't try to build a libpythonMAJOR.MINOR.a
#
# Downstream only: not appropriate for upstream.
#
# See https://bugzilla.redhat.com/show_bug.cgi?id=556092
Patch111: 00111-no-static-lib.patch

# 00189 # 0c6dd5d318a22bbe89e09e1cd5513eaaca549aa5
# Instead of bundled wheels, use our RPM packaged wheels
#
# We keep them in /usr/share/python-wheels
#
# Downstream only: upstream bundles
# We might eventually pursuit upstream support, but it's low prio
Patch189: 00189-use-rpm-wheels.patch
# The following versions of setuptools/pip are bundled when this patch is not applied.
# The versions are written in Lib/ensurepip/__init__.py, this patch removes them.
# When the bundled setuptools/pip wheel is updated, the patch no longer applies cleanly.
# In such cases, the patch needs to be amended and the versions updated here:
%global pip_version 23.0.1
%global setuptools_version 79.0.1

# 00251 # 1b1047c14ff98eae6d355b4aac4df3e388813f62
# Change user install location
#
# Set values of prefix and exec_prefix in distutils install command
# to /usr/local if executable is /usr/bin/python* and RPM build
# is not detected to make pip and distutils install into separate location.
#
# Fedora Change: https://fedoraproject.org/wiki/Changes/Making_sudo_pip_safe
# Downstream only: Reworked in Fedora 36+/Python 3.10+ to follow https://bugs.python.org/issue43976
#
# pypa/distutils integration: https://github.com/pypa/distutils/pull/70
#
# Also set sysconfig._PIP_USE_SYSCONFIG = False, to force pip-upgraded-pip
# to respect this patched distutils install command.
# See https://bugzilla.redhat.com/show_bug.cgi?id=2014513
Patch251: 00251-change-user-install-location.patch

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

# 00371 # 1fc313929648e9b543542de09f59c55e175ac45a
# Revert "bpo-1596321: Fix threading._shutdown() for the main thread (GH-28549) (GH-28589)"
#
# This reverts commit 94d19f606fa18a1c4d2faca1caf2f470a8ce6d46. It
# introduced regression causing FreeIPA's tests to fail.
#
# For more info see:
# https://bodhi.fedoraproject.org/updates/FEDORA-2021-e152ce5f31
# https://github.com/GrahamDumpleton/mod_wsgi/issues/730
Patch371: 00371-revert-bpo-1596321-fix-threading-_shutdown-for-the-main-thread-gh-28549-gh-28589.patch

# 00407 # 17dbfc39d1118a479e7ea244ad46fb6eeeb38280
# gh-99086: Fix implicit int compiler warning in configure check for PTHREAD_SCOPE_SYSTEM
Patch407: 00407-gh-99086-fix-implicit-int-compiler-warning-in-configure-check-for-pthread_scope_system.patch

# 00452 # eb11d070c5af7d1b5e47f4e02186152d08eaf793
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

# 00471 # fc5f344f7e15c13dbf41824a1b7a82d92205f79d
# CVE-2025-12084
#
# * gh-142145: Remove quadratic behavior in node ID cache clearing (GH-142146)
# * gh-142754: Ensure that Element & Attr instances have the ownerDocument attribute (GH-142794)
Patch471: 00471-cve-2025-12084.patch

# 00473 # 7e68b796abe391a467dba42b6641053aac726d67
# CVE-2026-0865
#
#  gh-143916: Reject control characters in wsgiref.headers.Headers  (GH-143917)
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

# 00475 # 00384c03f44af74c955a44637eee0b66f717a487
# CVE-2025-15367
#
# gh-143923: Reject control characters in POP3 commands
#
# (cherry-picked from commit b234a2b67539f787e191d2ef19a7cbdce32874e7)
Patch475: 00475-cve-2025-15367.patch

# 00476 # efbfd1798bf8c1a9845546a0ed9193f94661dd1b
# CVE-2026-1299
#
# gh-144125: email: verify headers are sound in BytesGenerator
Patch476: 00476-cve-2026-1299.patch

# (New patches go here ^^^)
#
# When adding new patches to "python" and "python3" in Fedora, EL, etc.,
# please try to keep the patch numbers in-sync between all specfiles.
#
# More information, and a patch number catalog, is at:
#
#     https://fedoraproject.org/wiki/SIGs/Python/PythonPatches
#
# The patches are stored and rebased at:
#
#     https://github.com/fedora-python/cpython


# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

# this if branch is ~300 lines long and contains subpackages' definitions
%if %{without flatpackage}
%if %{with main_python}
# Description for the python3X SRPM only:
%description
Python %{pybasever} is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

%package -n %{pkgname}
Summary: Python %{pybasever} interpreter

# In order to support multiple Python interpreters for development purposes,
# packages with the naming scheme flatpackage (e.g. python3.5) exist for
# non-default versions of Python 3.
# For consistency, we provide python3.X from python3 as well.
Provides: python%{pybasever} = %{version}-%{release}
Provides: python%{pybasever}%{?_isa} = %{version}-%{release}
# To keep the upgrade path clean, we Obsolete python3.X.
# Note that using Obsoletes without package version is not standard practice.
# Here we assert that *any* version of the system's default interpreter is
# preferable to an "extra" interpreter. For example, python3-3.6.1 will
# replace python3.6-3.6.2.
Obsoletes: python%{pybasever}

# https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
# We recommend /usr/bin/python so users get it by default
# Versioned recommends are problematic, and we know that the package requires
# python3 back with fixed version, so we just use the path here:
Recommends: %{_bindir}/python
%endif

%if %{with rhel8_compat_shims}
Provides:  platform-python = %{version}-%{release}
Provides:  platform-python%{?_isa} = %{version}-%{release}
Obsoletes: platform-python < %{pybasever}
%endif

# Python interpreter packages used to be named (or provide) name pythonXY (e.g.
# python39). However, to align it with the executable names and to prepare for
# Python 3.10, they were renamed to pythonX.Y (e.g. python3.9, python3.10). We
# provide and obsolete the previous names.
# - Here are the tags for the nonflat package, regardless if main_python (e.g.
#   python3) or not (e.g. python39). For the flat package, the provide is
#   repeated many lines later.
Provides: python%{pyshortver} = %{version}-%{release}
Obsoletes: python%{pyshortver} < %{version}-%{release}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{pkgname} < 3.9.24-2

%if %{with main_python}
# Packages with Python modules in standard locations automatically
# depend on python(abi). Provide that here.
Provides: python(abi) = %{pybasever}
%else
# We exclude the `python(abi)` Provides
%global __requires_exclude ^python\\(abi\\) = 3\\..+
%global __provides_exclude ^python\\(abi\\) = 3\\..+
%endif

Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}

# In Fedora 31, /usr/bin/pydoc was moved here from Python 2.
# Ideally we'd have an explicit conflict with "/usr/bin/pydoc < 3",
# but file provides aren't versioned and the file moved across packages.
# Instead, we rely on the conflict in python3-libs.

# Previously, this was required for our rewheel patch to work.
# This is technically no longer needed, but we keep it recommended
# for the developer experience.
Recommends: %{pkgname}-setuptools
Recommends: %{pkgname}-pip

# This prevents ALL subpackages built from this spec to require
# /usr/bin/python3* or python(abi). Granularity per subpackage is impossible.
# It's intended for the libs package not to drag in the interpreter, see
# https://bugzilla.redhat.com/show_bug.cgi?id=1547131
# https://bugzilla.redhat.com/show_bug.cgi?id=1862082
# All other packages require %%{pkgname} explicitly.
%global __requires_exclude ^(/usr/bin/python3|python\\(abi\\))

%description -n %{pkgname}
Python %{pybasever} is an accessible, high-level, dynamically typed, interpreted
programming language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

The %{pkgname} package provides the "%{exename}" executable: the reference
interpreter for the Python language, version 3.
The majority of its standard library is provided in the %{pkgname}-libs package,
which should be installed automatically along with %{pkgname}.
The remaining parts of the Python standard library are broken out into the
%{pkgname}-tkinter and %{pkgname}-test packages, which may need to be installed
separately.

Documentation for Python is provided in the %{pkgname}-docs package.

Packages containing additional libraries for Python are generally named with
the "%{pkgname}-" prefix.


%if %{with main_python}
# https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
%package -n python-unversioned-command
Summary: The "python" command that runs Python 3
BuildArch: noarch

# In theory this could require any python3 version
Requires: python3 == %{version}-%{release}
# But since we want to provide versioned python, we require exact version
Provides: python = %{version}-%{release}
# This also save us an explicit conflict for older python3 builds

# Also provide the name of the Ubuntu package with the same function,
# to be nice to people who temporarily forgot which distro they're on.
# C.f. https://packages.ubuntu.com/hirsute/all/python-is-python3/filelist
Provides: python-is-python3 = %{version}-%{release}

%description -n python-unversioned-command
This package contains /usr/bin/python - the "python" command that runs Python 3.

%endif # with main_python


%package -n %{pkgname}-libs
Summary:        Python runtime libraries

%if %{with rpmwheels}
Requires: python-setuptools-wheel
Requires: python-pip-wheel
%else
Provides: bundled(python3dist(pip)) = %{pip_version}
Provides: bundled(python3dist(setuptools)) = %{setuptools_version}
%endif

# Provides for the bundled libmpdec
Provides: bundled(mpdecimal) = %{libmpdec_version}
Provides: bundled(libmpdec) = %{libmpdec_version}

# There are files in the standard library that have python shebang.
# We've filtered the automatic requirement out so libs are installable without
# the main package. This however makes it pulled in by default.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1547131
Recommends: %{pkgname}%{?_isa} = %{version}-%{release}

# tkinter is part of the standard library,
# but it is torn out to save an unwanted dependency on tk and X11.
# we recommend it when tk is already installed (for better UX)
Recommends: (%{pkgname}-tkinter%{?_isa} = %{version}-%{release} if tk%{?_isa})

# The zoneinfo module needs tzdata
Requires: tzdata

# The requirement on libexpat is generated, but we need to version it.
# When built with expat >= 2.6, but installed with older expat, we get:
#   ImportError: /usr/lib64/python3.X/lib-dynload/pyexpat.cpython-....so:
#   undefined symbol: XML_SetReparseDeferralEnabled
# This breaks many things, including python -m venv.
# Other subpackages (like -debug) also need this, but they all depend on -libs.
Requires: expat >= 2.6

# https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package
# In Fedora 31, several "unversioned" files like /usr/bin/pydoc and all the
# "unversioned" provides were moved from python2 to python3.
# So, newer python3 packages need to conflict with old Python 2 builds that
# still provided unversioned Python.
# Since all python packages, new and old, have versioned requires on
# python?-libs, we do it here:
Conflicts: python-libs < 3
# (We explicitly conflict with python-libs and not python2-libs, so only the
# old Python 2 builds that still provided unversioned Python are handled.)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{pkgname} < 3.9.24-2

%description -n %{pkgname}-libs
This package contains runtime libraries for use by Python:
- the majority of the Python standard library
- a dynamically linked library for use by applications that embed Python as
  a scripting language, and by the main "%{exename}" executable


%package -n %{pkgname}-devel
Summary: Libraries and header files needed for Python development
Requires: %{pkgname} = %{version}-%{release}
Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}
# The RPM related dependencies bring nothing to a non-RPM Python developer
# But we want them when packages BuildRequire python3-devel
Requires: (python-rpm-macros if rpm-build)
Requires: (python3-rpm-macros if rpm-build)
Requires: (pyproject-rpm-macros if rpm-build)

%if %{without bootstrap}
%if %{with main_python}
# This is not "API" (packages that need setuptools should still BuildRequire it)
# However some packages apparently can build both with and without setuptools
# producing egg-info as file or directory (depending on setuptools presence).
# Directory-to-file updates are problematic in RPM, so we ensure setuptools is
# installed when -devel is required.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1623914
# See https://fedoraproject.org/wiki/Packaging:Directory_Replacement
Requires: (%{pkgname}-setuptools if rpm-build)
%endif

Requires: (python3-rpm-generators if rpm-build)
%endif

Provides: %{pkgname}-2to3 = %{version}-%{release}
Provides: 2to3 = %{version}-%{release}

Conflicts: %{pkgname} < %{version}-%{release}

# In Fedora 31, several "unversioned" files were moved here from Python 2:
# pygettext.py, msgfmt.py, python-config, python.pc
Conflicts: python-devel < 3

%if %{with rhel8_compat_shims}
Provides:  platform-python-devel = %{version}-%{release}
Provides:  platform-python-devel%{?_isa} = %{version}-%{release}
Obsoletes: platform-python-devel < %{pybasever}
%endif

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{pkgname} < 3.9.24-2

%description -n %{pkgname}-devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.

It also contains the necessary macros to build RPM packages with Python modules
and 2to3 tool, an automatic source converter from Python 2.X.


%package -n %{pkgname}-idle
Summary: A basic graphical development environment for Python
Requires: %{pkgname} = %{version}-%{release}
Requires: %{pkgname}-tkinter = %{version}-%{release}

Provides: idle3 = %{version}-%{release}
Provides: idle = %{version}-%{release}

Provides: %{pkgname}-tools = %{version}-%{release}
Provides: %{pkgname}-tools%{?_isa} = %{version}-%{release}
Obsoletes: %{pkgname}-tools < %{version}-%{release}

# In Fedora 31, /usr/bin/idle was moved here from Python 2.
Conflicts: python-tools < 3

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{pkgname} < 3.9.24-2

%description -n %{pkgname}-idle
IDLE is Python’s Integrated Development and Learning Environment.

IDLE has the following features: Python shell window (interactive
interpreter) with colorizing of code input, output, and error messages;
multi-window text editor with multiple undo, Python colorizing,
smart indent, call tips, auto completion, and other features;
search within any window, replace within editor windows, and
search through multiple files (grep); debugger with persistent
breakpoints, stepping, and viewing of global and local namespaces;
configuration, browsers, and other dialogs.


%package -n %{pkgname}-tkinter
Summary: A GUI toolkit for Python
Requires: %{pkgname} = %{version}-%{release}

# The importable module "turtle" is here, so provide python3-turtle.
# (We don't provide python3-turtledemo, that's not too useful when imported.)
%py_provides %{pkgname}-turtle

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{pkgname} < 3.9.24-2

%description -n %{pkgname}-tkinter
The Tkinter (Tk interface) library is a graphical user interface toolkit for
the Python programming language.


%package -n %{pkgname}-test
Summary: The self-test suite for the main python3 package
Requires: %{pkgname} = %{version}-%{release}
Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_one_to_many_replacement
Obsoletes: %{pkgname} < 3.9.24-2

%description -n %{pkgname}-test
The self-test suite for the Python interpreter.

This is only useful to test Python itself. For testing general Python code,
you should use the unittest module from %{pkgname}-libs, or a library such as
%{pkgname}-pytest.


%if %{with debug_build}
%package -n %{pkgname}-debug
Summary: Debug version of the Python runtime

# The debug build is an all-in-one package version of the regular build, and
# shares the same .py/.pyc files and directories as the regular build. Hence
# we depend on all of the subpackages of the regular build:
Requires: %{pkgname}%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-devel%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-test%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-tkinter%{?_isa} = %{version}-%{release}
Requires: %{pkgname}-idle%{?_isa} = %{version}-%{release}

# In Fedora 31, /usr/bin/python-debug was moved here from Python 2.
Conflicts: python-debug < 3

%if %{with rhel8_compat_shims}
Provides:  platform-python-debug = %{version}-%{release}
Provides:  platform-python-debug%{?_isa} = %{version}-%{release}
Obsoletes: platform-python-debug < %{pybasever}
%endif

%description -n %{pkgname}-debug
python3-debug provides a version of the Python runtime with numerous debugging
features enabled, aimed at advanced Python users such as developers of Python
extension modules.

This version uses more memory and will be slower than the regular Python build,
but is useful for tracking down reference-counting issues and other bugs.

The debug build shares installation directories with the standard Python
runtime. Python modules -- source (.py), bytecode (.pyc), and C-API extensions
(.cpython*.so) -- are compatible between this and the standard version
of Python.

The debug runtime additionally supports debug builds of C-API extensions
(with the "d" ABI flag) for debugging issues in those extensions.
%endif # with debug_build

%else  # with flatpackage

# Python interpreter packages used to be named (or provide) name pythonXY (e.g.
# python39). However, to align it with the executable names and to prepare for
# Python 3.10, they were renamed to pythonX.Y (e.g. python3.9, python3.10). We
# provide and obsolete the previous names.
# - Here are the tags for the flat package. For the nonflat package, the
#   provide is repeated many lines above.
Provides: python%{pyshortver} = %{version}-%{release}
Obsoletes: python%{pyshortver} < %{version}-%{release}

%if %{with rpmwheels}
Requires: python-setuptools-wheel
Requires: python-pip-wheel
%else
Provides: bundled(python3dist(pip)) = %{pip_version}
Provides: bundled(python3dist(setuptools)) = %{setuptools_version}
%endif

# Provides for the bundled libmpdec
Provides: bundled(mpdecimal) = %{libmpdec_version}
Provides: bundled(libmpdec) = %{libmpdec_version}

# The zoneinfo module needs tzdata
Requires: tzdata

# The requirement on libexpat is generated, but we need to version it.
# When built with expat >= 2.6, but installed with older expat, we get:
#   ImportError: /usr/lib64/python3.X/lib-dynload/pyexpat.cpython-....so:
#   undefined symbol: XML_SetReparseDeferralEnabled
# This breaks many things, including python -m venv.
# Other subpackages (like -debug) also need this, but they all depend on -libs.
Requires: expat >= 2.6

# Provides of the subpackages contained in flatpackage
Provides: %{pkgname}-libs = %{version}-%{release}
Provides: %{pkgname}-devel = %{version}-%{release}
Provides: %{pkgname}-idle = %{version}-%{release}
Provides: %{pkgname}-tkinter = %{version}-%{release}
Provides: %{pkgname}-test = %{version}-%{release}
%if %{with debug_build}
Provides: %{pkgname}-debug = %{version}-%{release}
%endif

# The description for the flat package (SRPM and built)
%description
Python %{pybasever} package for developers.

This package exists to allow developers to test their code against an older
version of Python. This is not a full Python stack and if you wish to run
your applications with Python %{pybasever}, see other distributions
that support it, such as CentOS or RHEL or older Fedora releases.

%endif # with flatpackage

# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%gpgverify -k2 -s1 -d0
%autosetup -S git_am -N -n Python-%{upstream_version}

# Apply patches up to 188
%autopatch -M 188

%if %{with rpmwheels}
%autopatch 189
rm Lib/ensurepip/_bundled/*.whl
%endif

# Apply the remaining patches
%autopatch -m 190

# Remove all exe files to ensure we are not shipping prebuilt binaries
# note that those are only used to create Microsoft Windows installers
# and that functionality is broken on Linux anyway
find -name '*.exe' -print -delete

# Remove bundled libraries to ensure that we're using the system copy.
rm -r Modules/expat

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
export CFLAGS_NODIST="%{build_cflags} -D_GNU_SOURCE -fPIC -fwrapv%{?with_no_semantic_interposition: -fno-semantic-interposition}"
export CXXFLAGS="%{extension_cxxflags}"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="%{extension_cflags}"
export LINKCC="gcc"
export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
export LDFLAGS="%{extension_ldflags} $(pkg-config --libs-only-L openssl)"
export LDFLAGS_NODIST="%{build_ldflags}%{?with_no_semantic_interposition: -fno-semantic-interposition} -g $(pkg-config --libs-only-L openssl)"

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

  # A workaround for https://bugs.python.org/issue39761
  export DFLAGS=" "

%configure \
  --with-platlibdir=%{_lib} \
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

%global flags_override EXTRA_CFLAGS="$MoreCFlags" CFLAGS_NODIST="$CFLAGS_NODIST $MoreCFlags"

%if %{without bootstrap}
  # Regenerate generated files (needs python3)
  %make_build %{flags_override} regen-all PYTHON_FOR_REGEN="python%{pybasever}"
%endif

  # Invoke the build
  %make_build %{flags_override}

  popd
  echo FINISHED: BUILD OF PYTHON FOR CONFIGURATION: $ConfName
}

# Call the above to build each configuration.

%if %{with debug_build}
# The debug build is compiled with the lowest level of optimizations as to not optimize
# out frames. We also suppress the warnings as the default distro value of the FORTIFY_SOURCE
# option produces too many warnings when compiling at the O0 optimization level.
# See also: https://bugzilla.redhat.com/show_bug.cgi?id=1818857
BuildPython debug \
  "--without-ensurepip --with-pydebug" \
  "-O0 -Wno-cpp"
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
DirHoldingGdbPy=%{_usr}/lib/debug/%{_libdir}
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
%global _pyconfig_h pyconfig-%{__isa_bits}.h

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
  echo -e '#!/bin/sh\nexec %{_bindir}/python'${LDVersion}'-`uname -m`-config "$@"' > \
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
install -D -m 0644 Lib/idlelib/Icons/idle_256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/idle3.png
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
cp -p Tools/scripts/pathfix.py %{buildroot}%{_bindir}/pathfix%{pybasever}.py

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
# compile *.pyc
# Python CMD line options:
# -s - don't add user site directory to sys.path
# -B - don't write .pyc files on import
# Clamp the source mtime first, see https://fedoraproject.org/wiki/Changes/ReproducibleBuildsClampMtimes
# The clamp_source_mtime module is only guaranteed to exist on Fedoras that enabled this option:
%if 0%{?clamp_mtime_to_source_date_epoch}
LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
PYTHONPATH="%{_rpmconfigdir}/redhat" \
%{buildroot}%{_bindir}/python%{pybasever} -s -B -m clamp_source_mtime %{buildroot}%{pylibdir}
%endif
# compileall CMD line options:
# -f - force rebuild even if timestamps are up to date
# -o - optimization levels to run compilation with
# -s - part of path to left-strip from path to source file (buildroot)
# -p - path to add as prefix to path to source file (/ to make it absolute)
# --hardlink-dupes - hardlink different optimization level pycs together if identical (saves space)
# --invalidation-mode - we prefer the timestamp invalidation mode for performance reasons
# -x - skip test modules with SyntaxErrors (taken from the Makefile)
LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
%{buildroot}%{_bindir}/python%{pybasever} -s -B -m compileall \
-f %{_smp_mflags} -o 0 -o 1 -o 2 -s %{buildroot} -p / %{buildroot} --hardlink-dupes --invalidation-mode=timestamp \
-x 'bad_coding|badsyntax|site-packages|lib2to3/tests/data'

# Turn this BRP off, it is done by compileall2 --hardlink-dupes above
%global __brp_python_hardlink %{nil}

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

# There's 2to3-X.X executable and 2to3 soft link to it.
# No reason to have both, so keep only 2to3 as an executable.
# See https://bugzilla.redhat.com/show_bug.cgi?id=1111275
mv %{buildroot}%{_bindir}/2to3-%{pybasever} %{buildroot}%{_bindir}/2to3

%if %{without main_python}
# Remove stuff that would conflict with python3 package
rm %{buildroot}%{_bindir}/python3
rm %{buildroot}%{_bindir}/pydoc3
rm %{buildroot}%{_bindir}/pygettext3.py
rm %{buildroot}%{_bindir}/msgfmt3.py
rm %{buildroot}%{_bindir}/idle3
rm %{buildroot}%{_bindir}/python3-*
rm %{buildroot}%{_bindir}/2to3
rm %{buildroot}%{_libdir}/libpython3.so
rm %{buildroot}%{_mandir}/man1/python3.1*
rm %{buildroot}%{_libdir}/pkgconfig/python3.pc
rm %{buildroot}%{_libdir}/pkgconfig/python3-embed.pc
%else
# Link the unversioned stuff
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
ln -s ./python3 %{buildroot}%{_bindir}/python
ln -s ./pydoc3 %{buildroot}%{_bindir}/pydoc
ln -s ./pygettext3.py %{buildroot}%{_bindir}/pygettext.py
ln -s ./msgfmt3.py %{buildroot}%{_bindir}/msgfmt.py
ln -s ./idle3 %{buildroot}%{_bindir}/idle
ln -s ./python3-config %{buildroot}%{_bindir}/python-config
ln -s ./python3.1 %{buildroot}%{_mandir}/man1/python.1
ln -s ./python3.pc %{buildroot}%{_libdir}/pkgconfig/python.pc
ln -s ./pathfix%{pybasever}.py %{buildroot}%{_bindir}/pathfix.py
%if %{with debug_build}
ln -s ./python3-debug %{buildroot}%{_bindir}/python-debug
%endif
%endif

%if %{with rhel8_compat_shims}
# Provide RHEL8 backwards compatible symbolic links in %%_libexecdir
mkdir -p %{buildroot}%{_libexecdir}
ln -s %{_bindir}/python%{pybasever} %{buildroot}%{_libexecdir}/platform-python
ln -s %{_bindir}/python%{pybasever} %{buildroot}%{_libexecdir}/platform-python%{pybasever}
ln -s %{_bindir}/python%{pybasever}-config %{buildroot}%{_libexecdir}/platform-python-config
ln -s %{_bindir}/python%{pybasever}-config %{buildroot}%{_libexecdir}/platform-python%{pybasever}-config
ln -s %{_bindir}/python%{pybasever}-`uname -m`-config %{buildroot}%{_libexecdir}/platform-python%{pybasever}-`uname -m`-config
# There were also executables with %%{LDVERSION_optimized} in RHEL 8,
# but since Python 3.8 %%{LDVERSION_optimized} == %%{pybasever}.
# We list both in the %%files section to assert this.
%if %{with debug_build}
ln -s %{_bindir}/python%{LDVERSION_debug} %{buildroot}%{_libexecdir}/platform-python-debug
ln -s %{_bindir}/python%{LDVERSION_debug} %{buildroot}%{_libexecdir}/platform-python%{LDVERSION_debug}
ln -s %{_bindir}/python%{LDVERSION_debug}-config %{buildroot}%{_libexecdir}/platform-python%{LDVERSION_debug}-config
ln -s %{_bindir}/python%{LDVERSION_debug}-`uname -m`-config %{buildroot}%{_libexecdir}/platform-python%{LDVERSION_debug}-`uname -m`-config
%endif
%endif

# Remove large, autogenerated sources and keep only the non-optimized pycache
for file in %{buildroot}%{pylibdir}/pydoc_data/topics.py $(grep --include='*.py' -lr %{buildroot}%{pylibdir}/encodings -e 'Python Character Mapping Codec .* from .* with gencodec.py'); do
    directory=$(dirname ${file})
    module=$(basename ${file%%.py})
    mv ${directory}/{__pycache__/${module}.cpython-%{pyshortver}.pyc,${module}.pyc}
    rm ${directory}/{__pycache__/${module}.cpython-%{pyshortver}.opt-?.pyc,${module}.py}
done

%if %{without rpmwheels}
# Inject SBOM into the installed wheels (if the macro is available)
%{?python_wheel_inject_sbom:%python_wheel_inject_sbom %{buildroot}%{pylibdir}/ensurepip/_bundled/*.whl}
%endif

# ======================================================
# Checks for packaging issues
# ======================================================

%check

# setuptools 60+ uses its own copy of distutils by default
# this setting must be overriden with the environment variable for
# Python tests to use the standard library's distutils
export SETUPTOOLS_USE_DISTUTILS=stdlib

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

  echo STARTING: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

  # Note that we're running the tests using the version of the code in the
  # builddir, not in the buildroot.

  # Show some info, helpful for debugging test failures
  LD_LIBRARY_PATH=$ConfDir $ConfDir/python -m test.pythoninfo

  # Run the upstream test suite
  # --timeout=1800: kill test running for longer than 30 minutes
  # test_distutils
  #   distutils.tests.test_bdist_rpm tests fail when bootstraping the Python
  #   package: rpmbuild requires /usr/bin/pythonX.Y to be installed
  # test_gdb on arm on Fedora 33:
  #   https://bugzilla.redhat.com/show_bug.cgi?id=1846390
  # test_sendfile_close_peer_in_the_middle_of_receiving:
  #  https://github.com/python/cpython/issues/120226
  LD_LIBRARY_PATH=$ConfDir $ConfDir/python -m test.regrtest \
    -wW --slowest -j0 --timeout=1800 \
    %if %{with bootstrap}
    -x test_distutils \
    %endif
    %ifarch %{mips64}
    -x test_ctypes \
    %endif
    %ifarch %{arm}
    %if 0%{?fedora} < 34 && 0%{?rhel} < 9
    -x test_gdb \
    %endif
    %endif
    %ifarch ppc64le
    -i test_sendfile_close_peer_in_the_middle_of_receiving \
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


%files -n %{pkgname}
%doc README.rst

%if %{with main_python}
%{_bindir}/pydoc*
%{_bindir}/python3
%else
%{_bindir}/pydoc%{pybasever}
%endif

%{_bindir}/python%{pybasever}
%{_bindir}/python%{LDVERSION_optimized}
%{_mandir}/*/*3*

%if %{with rhel8_compat_shims}
%{_libexecdir}/platform-python
%{_libexecdir}/platform-python%{pybasever}
%{_libexecdir}/platform-python%{LDVERSION_optimized}
%endif

%if %{with main_python}
%if %{without flatpackage}
%files -n python-unversioned-command
%endif
%{_bindir}/python
%{_mandir}/*/python.1*
%endif

%if %{without flatpackage}
%files -n %{pkgname}-libs
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
%{pylibdir}/ensurepip/_bundled/__init__.py
%{pylibdir}/ensurepip/_bundled/__pycache__/*%{bytecode_suffixes}
%endif

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
%{dynload_dir}/_contextvars.%{SOABI_optimized}.so
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
%{dynload_dir}/_queue.%{SOABI_optimized}.so
%{dynload_dir}/_random.%{SOABI_optimized}.so
%{dynload_dir}/_socket.%{SOABI_optimized}.so
%{dynload_dir}/_sqlite3.%{SOABI_optimized}.so
%{dynload_dir}/_ssl.%{SOABI_optimized}.so
%{dynload_dir}/_statistics.%{SOABI_optimized}.so
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
%{dynload_dir}/_posixshmem.%{SOABI_optimized}.so
%{dynload_dir}/pyexpat.%{SOABI_optimized}.so
%{dynload_dir}/readline.%{SOABI_optimized}.so
%{dynload_dir}/resource.%{SOABI_optimized}.so
%{dynload_dir}/select.%{SOABI_optimized}.so
%{dynload_dir}/spwd.%{SOABI_optimized}.so
%{dynload_dir}/syslog.%{SOABI_optimized}.so
%{dynload_dir}/termios.%{SOABI_optimized}.so
%{dynload_dir}/unicodedata.%{SOABI_optimized}.so
%{dynload_dir}/_uuid.%{SOABI_optimized}.so
%{dynload_dir}/xxlimited.%{SOABI_optimized}.so
%{dynload_dir}/_xxsubinterpreters.%{SOABI_optimized}.so
%{dynload_dir}/zlib.%{SOABI_optimized}.so
%{dynload_dir}/_zoneinfo.%{SOABI_optimized}.so

%dir %{pylibdir}/site-packages/
%dir %{pylibdir}/site-packages/__pycache__/
%{pylibdir}/site-packages/README.txt

%exclude %{pylibdir}/_sysconfigdata_d_linux_%{platform_triplet}.py
%exclude %{pylibdir}/__pycache__/_sysconfigdata_d_linux_%{platform_triplet}%{bytecode_suffixes}

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
%{pylibdir}/zoneinfo

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
%files -n %{pkgname}-devel
%endif

%if %{with main_python}
%{_bindir}/2to3
%endif

%{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/*
%if %{without flatpackage}
%exclude %{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/Makefile
%exclude %{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}
%endif
%{_includedir}/python%{LDVERSION_optimized}/*.h
%{_includedir}/python%{LDVERSION_optimized}/internal/
%{_includedir}/python%{LDVERSION_optimized}/cpython/
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit

%if %{with main_python}
%{_bindir}/python3-config
%{_bindir}/python-config
%{_libdir}/pkgconfig/python3.pc
%{_libdir}/pkgconfig/python.pc
%{_libdir}/pkgconfig/python3-embed.pc
%{_bindir}/pathfix.py
%{_bindir}/pygettext3.py
%{_bindir}/pygettext.py
%{_bindir}/msgfmt3.py
%{_bindir}/msgfmt.py
%endif

%{_bindir}/pathfix%{pybasever}.py
%{_bindir}/pygettext%{pybasever}.py
%{_bindir}/msgfmt%{pybasever}.py

%{_bindir}/python%{pybasever}-config
%{_bindir}/python%{LDVERSION_optimized}-config
%{_bindir}/python%{LDVERSION_optimized}-*-config
%{_libdir}/libpython%{LDVERSION_optimized}.so
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}.pc
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}-embed.pc
%{_libdir}/pkgconfig/python-%{pybasever}.pc
%{_libdir}/pkgconfig/python-%{pybasever}-embed.pc

%if %{with rhel8_compat_shims}
%{_libexecdir}/platform-python-config
%{_libexecdir}/platform-python%{pybasever}-config
%{_libexecdir}/platform-python%{LDVERSION_optimized}-config
%{_libexecdir}/platform-python%{pybasever}-*-config
%{_libexecdir}/platform-python%{LDVERSION_optimized}-*-config
%endif


%if %{without flatpackage}
%files -n %{pkgname}-idle
%endif

%if %{with main_python}
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
%files -n %{pkgname}-tkinter
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
%files -n %{pkgname}-test
%endif

%{pylibdir}/ctypes/test
%{pylibdir}/distutils/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test
%{dynload_dir}/_ctypes_test.%{SOABI_optimized}.so
%{dynload_dir}/_testbuffer.%{SOABI_optimized}.so
%{dynload_dir}/_testcapi.%{SOABI_optimized}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_optimized}.so
%{dynload_dir}/_testinternalcapi.%{SOABI_optimized}.so
%{dynload_dir}/_testmultiphase.%{SOABI_optimized}.so
%{dynload_dir}/_xxtestfuzz.%{SOABI_optimized}.so
%{pylibdir}/lib2to3/tests
%{pylibdir}/tkinter/test
%{pylibdir}/unittest/test

# We don't bother splitting the debug build out into further subpackages:
# if you need it, you're probably a developer.

# Hence the manifest is the combination of analogous files in the manifests of
# all of the other subpackages

%if %{with debug_build}
%if %{without flatpackage}
%files -n %{pkgname}-debug
%endif

%if %{with main_python}
%{_bindir}/python3-debug
%{_bindir}/python-debug
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
%{dynload_dir}/_contextvars.%{SOABI_debug}.so
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
%{dynload_dir}/_queue.%{SOABI_debug}.so
%{dynload_dir}/_random.%{SOABI_debug}.so
%{dynload_dir}/_socket.%{SOABI_debug}.so
%{dynload_dir}/_sqlite3.%{SOABI_debug}.so
%{dynload_dir}/_ssl.%{SOABI_debug}.so
%{dynload_dir}/_statistics.%{SOABI_debug}.so
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
%{dynload_dir}/_posixshmem.%{SOABI_debug}.so
%{dynload_dir}/pyexpat.%{SOABI_debug}.so
%{dynload_dir}/readline.%{SOABI_debug}.so
%{dynload_dir}/resource.%{SOABI_debug}.so
%{dynload_dir}/select.%{SOABI_debug}.so
%{dynload_dir}/spwd.%{SOABI_debug}.so
%{dynload_dir}/syslog.%{SOABI_debug}.so
%{dynload_dir}/termios.%{SOABI_debug}.so
%{dynload_dir}/unicodedata.%{SOABI_debug}.so
%{dynload_dir}/_uuid.%{SOABI_debug}.so
%{dynload_dir}/_xxsubinterpreters.%{SOABI_debug}.so
%{dynload_dir}/_xxtestfuzz.%{SOABI_debug}.so
%{dynload_dir}/zlib.%{SOABI_debug}.so
%{dynload_dir}/_zoneinfo.%{SOABI_debug}.so

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
%{_libdir}/libpython%{LDVERSION_debug}.so.%{py_SOVERSION}
%{_libdir}/pkgconfig/python-%{LDVERSION_debug}.pc
%{_libdir}/pkgconfig/python-%{LDVERSION_debug}-embed.pc

%if %{with rhel8_compat_shims}
%{_libexecdir}/platform-python-debug
%{_libexecdir}/platform-python%{LDVERSION_debug}
%{_libexecdir}/platform-python%{LDVERSION_debug}-config
%{_libexecdir}/platform-python%{LDVERSION_debug}-*-config
%endif

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
%{dynload_dir}/_testinternalcapi.%{SOABI_debug}.so
%{dynload_dir}/_testmultiphase.%{SOABI_debug}.so

%{pylibdir}/_sysconfigdata_d_linux_%{platform_triplet}.py
%{pylibdir}/__pycache__/_sysconfigdata_d_linux_%{platform_triplet}%{bytecode_suffixes}

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
* Tue Feb 10 2026 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.25-6
- Security fix for CVE-2026-1299

* Mon Feb 09 2026 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.25-5
- Security fixes for CVE-2026-0865, CVE-2025-15366 and CVE-2025-15367

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jan 14 2026 Lumír Balhar <lbalhar@redhat.com> - 3.9.25-3
- Security fix for CVE-2025-12084

* Mon Nov 10 2025 Tomas Orsava <torsava@redhat.com> - 3.9.25-2
- Move _sysconfigdata_d_linux*.py to the debug subpackage

* Mon Nov 03 2025 Karolina Surma <ksurma@redhat.com> - 3.9.25-1
- Update to Python 3.9.25

* Wed Oct 15 2025 Miro Hrončok <mhroncok@redhat.com> - 3.9.24-2
- On Fedora 44+, split this package into multiple subpackages
- This mimics newer Python versions

* Fri Oct 10 2025 Karolina Surma <ksurma@redhat.com> - 3.9.24-1
- Update to Python 3.9.24

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.23-1
- Update to 3.9.23

* Wed Apr 23 2025 Miro Hrončok <mhroncok@redhat.com> - 3.9.22-2
- Add RPM Provides for python3.9-libs, python3.9-devel, python3.9-idle, python3.9-tkinter, python3.9-test

* Wed Apr 09 2025 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.22-1
- Update to 3.9.22

* Mon Mar 31 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.9.21-5
- Properly apply exported CFLAGS for dtrace/systemtap builds
- Fixes: rhbz#2356304

* Mon Feb 10 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.9.21-4
- Security fix for CVE-2025-0938
- Fixes: rhbz#2343278

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 3.9.21-3
- Add explicit BR: libxcrypt-devel

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 03 2024 Lumír Balhar <lbalhar@redhat.com> - 3.9.21-1
- Update to 3.9.21
- Fixes: rhbz#2321662

* Mon Sep 09 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.20-1
- Update to 3.9.20

* Fri Aug 23 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.9.19-6
- Security fix for CVE-2024-8088
- Fixes: rhbz#2307466

* Tue Aug 13 2024 Lumír Balhar <lbalhar@redhat.com> - 3.9.19-5
- Security fix for CVE-2024-4032 (rhbz#2293397)
- Security fix for CVE-2024-6923 (rhbz#2303164)

* Tue Jul 23 2024 Lumír Balhar <lbalhar@redhat.com> - 3.9.19-4
- Require systemtap-sdt-devel for sys/sdt.h

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 17 2024 Miro Hrončok <mhroncok@redhat.com> - 3.9.19-2
- Require expat >= 2.6 to prevent errors when creating venvs with older expat

* Wed Mar 20 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.19-1
- Update to 3.9.19

* Wed Feb 28 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.9.18-7
- Fix tests for XMLPullParser with Expat 2.6.0

* Mon Jan 29 2024 Karolina Surma <ksurma@redhat.com> - 3.9.18-6
- Fix test_zlib when building with zlib-ng-compat

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Lumír Balhar <lbalhar@redhat.com> - 3.9.18-3
- Security fix for CVE-2023-27043 (rhbz#2196194)

* Thu Nov 23 2023 Miro Hrončok <mhroncok@redhat.com> - 3.9.18-2
- Fix implicit int compiler warning in configure check for PTHREAD_SCOPE_SYSTEM
- Resolves: rhbz#2147519

* Mon Aug 28 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.18-1
- Update to 3.9.18

* Wed Aug 02 2023 Charalampos Stratakis <cstratak@redhat.com> - 3.9.17-3
- Remove extra distro-applied CFLAGS passed to user built C extensions
- https://fedoraproject.org/wiki/Changes/Python_Extension_Flags_Reduction

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.17-1
- Update to 3.9.17

* Mon May 29 2023 Lumír Balhar <lbalhar@redhat.com> - 3.9.16-4
- Security fix for CVE-2023-24329
- Resolves: rhbz#2174016

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 03 2023 Miro Hrončok <mhroncok@redhat.com> - 3.9.16-2
- No longer patch the default bytecode cache invalidation policy

* Wed Dec 07 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.16-1
- Update to 3.9.16

* Thu Nov 17 2022 Miro Hrončok <mhroncok@redhat.com> - 3.9.15-3
- Rebuilt for infrastructure problems

* Wed Nov 09 2022 Lumír Balhar <lbalhar@redhat.com> - 3.9.15-2
- Fix for CVE-2022-42919
Resolves: rhbz#2138711

* Wed Oct 12 2022 Miro Hrončok <mhroncok@redhat.com> - 3.9.15-1
- Update to 3.9.15

* Wed Sep 07 2022 Miro Hrončok <mhroncok@redhat.com> - 3.9.14-1
- Update to 3.9.14
- Contains security fix for CVE-2020-10735

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 09 2022 Charalampos Stratakis <cstratak@redhat.com> - 3.9.13-2
- Security fix for CVE-2015-20107
Resolves: rhbz#2075390

* Wed May 18 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.13-1
- Update to 3.9.13

* Fri Mar 25 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.12-1
- Update to 3.9.12

* Thu Mar 17 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.11-1
- Update to 3.9.11

* Wed Mar 16 2022 Karolina Surma <ksurma@redhat.com> - 3.9.10-3
- Fix the test suite support for setuptools >= 60
Resolves: rhbz#2064734

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.10-1
- Update to 3.9.10

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 3.9.9-4
- Instruct pip to use distutils
- Instruct pypa/distutils to add /local/ addition to prefix

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 3.9.9-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Fri Nov 19 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.9-2
- Add patch to revert "bpo-1596321: Fix threading._shutdown() for the main thread"

* Tue Nov 16 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.9-1
- Update to 3.9.9

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 3.9.8-2
- Rebuild(libnsl2)

* Mon Nov 08 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.9.8-1
- Update to 3.9.8

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 3.9.7-2
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 30 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9.7-1
- Update to 3.9.7

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Petr Viktorin <pviktori@redhat.com> - 3.9.6-2
- Provide python3-turtle from python3-tkinter
- Require pyproject-rpm-macros from python3-devel

* Tue Jun 29 2021 Tomas Hrnciar <thrnciar@redhat.com> - 3.9.6-1
- Update to 3.9.6

* Tue Jun 01 2021 Python Maint <python-maint@redhat.com> - 3.9.5-3
- Rebuilt for Python 3.10

* Fri May 14 2021 Charalampos Stratakis <cstratak@redhat.com> - 3.9.5-2
- Add virtual provides for the bundled libmpdec (rhbz#1943359)

* Tue May 04 2021 Tomas Hrnciar <thrnciar@redhat.com> - 3.9.5-1
- Update to 3.9.5

* Tue Apr 06 2021 Tomas Hrnciar <thrnciar@redhat.com> - 3.9.4-1
- Update to 3.9.4

* Sat Feb 20 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Thu Feb 18 2021 Tomas Hrnciar <thrnciar@redhat.com> - 3.9.2~rc1-1
- Update to 3.9.2rc1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9.1-4
- Rebuilt to be signed with Fedora 32 compatible signature,
  to fix mock bootstrap chroot on Fedora 32 (and possibly EPELs)
  https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/OBEFWGCFXHE4EDBXFBZWDUPAJJS7QZAR/

* Wed Jan 20 2021 Charalampos Stratakis <cstratak@redhat.com> - 3.9.1-3
- Compile the debug build with -O0 instead of -Og (rhbz#1818857)

* Wed Jan 20 2021 Miro Hrončok <mhroncok@redhat.com> - 3.9.1-2
- Security fix for CVE-2021-3177

* Tue Dec 08 2020 Tomas Hrnciar <thrnciar@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Fri Nov 27 2020 Tomas Hrnciar <thrnciar@redhat.com> - 3.9.1~rc1-1
- Update to 3.9.1rc1

* Tue Oct 06 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0-1
- Update to 3.9.0 final

* Fri Sep 25 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~rc2-2
- Use upstream architecture names on Fedora 34+
- https://fedoraproject.org/wiki/Changes/Python_Upstream_Architecture_Names

* Thu Sep 17 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~rc2-1
- Update to 3.9.0rc2

* Wed Aug 12 2020 Petr Viktorin <pviktori@redhat.com> - 3.9.0~rc1-2
- In sys.version and initial REPL message, list the source commit as "default"

* Tue Aug 11 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~rc1-1
- Update to 3.9.0rc1

* Mon Aug 03 2020 Lumír Balhar <lbalhar@redhat.com> - 3.9.0~b5-5
- Add support for upstream architectures' names (patch 353)

* Thu Jul 30 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~b5-4
- Make python3-libs installable without python3
  Resolves: rhbz#1862082

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0~b5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Lumír Balhar <lbalhar@redhat.com> - 3.9.0~b5-2
- Add versioned pathfix%%{pybasever}.py to main and non-main RPMs

* Mon Jul 20 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~b5-1
- Update to 3.9.0b5

* Thu Jul 16 2020 Marcel Plch <mplch@redhat.com> - 3.9.0~b4-2
- Remove large, autogenerated Python sources and redundant pycache levels to reduce filesystem footprint

* Sat Jul 04 2020 Tomas Hrnciar <thrnciar@redhat.com> - 3.9.0~b4-1
- Update to 3.9.0b4

* Wed Jun 10 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~b3-1
- Update to 3.9.0b3

* Tue Jun 09 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~b2-1
- Update to 3.9.0b2

* Fri May 29 2020 Petr Viktorin <pviktori@redhat.com> - 3.9.0~b1-4
- Add cherry-picks for bugs found in 3.9.0b1

* Thu May 21 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~b1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python3.9

* Thu May 21 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~b1-2
- Bootstrap for https://fedoraproject.org/wiki/Changes/Python3.9

* Tue May 19 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~b1-1
- Update to Python 3.9.0b1

* Thu May 07 2020 Tomas Orsava <torsava@redhat.com> - 3.9.0~a6-2
- Rename from python39 to python3.9

* Tue Apr 28 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~a6-1
- Update to Python 3.9.0a6

* Tue Mar 24 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~a5-1
- Update to Python 3.9.0a5

* Thu Feb 27 2020 Marcel Plch <mplch@redhat.com> - 3.9.0~a4-1
- Update to Python 3.9.0a4

* Tue Feb 11 2020 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~a3-2
- Update the ensurepip module to work with setuptools >= 45

* Mon Jan 27 2020 Victor Stinner <vstinner@python.org> - 3.9.0~a3-1
- Update to Python 3.9.0a3

* Thu Dec 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~a2-1
- Rebased to Python 3.9.0a2

* Wed Dec 04 2019 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~a1-3
- Build Python with -fno-semantic-interposition for better performance
- https://fedoraproject.org/wiki/Changes/PythonNoSemanticInterpositionSpeedup

* Thu Nov 28 2019 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~a1-2
- Don't remove the test.test_tools module

* Wed Nov 20 2019 Miro Hrončok <mhroncok@redhat.com> - 3.9.0~a1-1
- Rebased to Python 3.9.0a1

* Mon Oct 14 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-1
- Update to Python 3.8.0 final

* Tue Oct 01 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~rc1-1
- Rebased to Python 3.8.0rc1

* Sat Aug 31 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b4-1
- Rebased to Python 3.8.0b4
- Enable Profile-guided optimization for all arches, not just x86 (#1741015)

* Mon Jul 29 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b3-1
- Update to 3.8.0b3

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0~b2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 05 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b2-1
- Update to 3.8.0b2

* Wed Jun 05 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~b1-1
- Update to 3.8.0b1

* Fri May 17 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~a4-2
- Remove a faulty patch that resulted in invalid value of
  distutils.sysconfig.get_config_var('LIBPL') (#1710767)

* Tue May 07 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~a4-1
- Update to 3.8.0a4

* Tue Mar 26 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~a3-1
- Update to 3.8.0a3

* Mon Feb 25 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~a2-1
- Update to 3.8.0a2

* Mon Feb 18 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~a1-3
- Reduced default build flags used to build extension modules
  https://fedoraproject.org/wiki/Changes/Python_Extension_Flags

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.8.0~a1-2
- Rebuild for readline 8.0

* Tue Feb 05 2019 Miro Hrončok <mhroncok@redhat.com> - 3.8.0~a1-1
- Update to 3.8.0a1
