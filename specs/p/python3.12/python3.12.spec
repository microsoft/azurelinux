# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# ==================
# Top-level metadata
# ==================

%global pybasever 3.12

# pybasever without the dot:
%global pyshortver 312

Name: python%{pybasever}
Summary: Version %{pybasever} of the Python interpreter
URL: https://www.python.org/

#  WARNING  When rebasing to a new Python version,
#           remember to update the python3-docs package as well
%global general_version %{pybasever}.12
#global prerel ...
%global upstream_version %{general_version}%{?prerel}
Version: %{general_version}%{?prerel:~%{prerel}}
Release: 4%{?dist}
License: Python-2.0.1


# ==================================
# Conditionals controlling the build
# ==================================

# Note that the bcond macros are named for the CLI option they create.
# "%%bcond_without" means "ENABLE by default and create a --without option"

# Main Python, i.e. whether this is the main Python version in the distribution
# that owns /usr/bin/python3 and other unique paths
# This also means the built subpackages are called python3 rather than python3X
# By default, this is determined by the %%__default_python3_pkgversion value
%if "%{?__default_python3_pkgversion}" == "%{pybasever}"
%bcond_without main_python
%else
%bcond_with main_python
%endif

# If this is *not* Main Python, should it contain `Provides: python(abi) ...`?
# In Fedora no package shall depend on an alternative Python via this tag, so we do not provide it.
# In ELN/RHEL/CentOS we want to allow building against alternative stacks, so the Provide is enabled.
%if 0%{?fedora}
%bcond_with python_abi_provides_for_alt_pythons
%else
%bcond_without python_abi_provides_for_alt_pythons
%endif

# When bootstrapping python3, we need to build setuptools.
# but setuptools BR python3-devel and that brings in python3-rpm-generators;
# python3-rpm-generators needs python3-setuptools, so we cannot have it yet.
#
# We also use the previous build of Python in "make regen-all".
#
# Procedure: https://fedoraproject.org/wiki/SIGs/Python/UpgradingPython
#
#   IMPORTANT: When bootstrapping, it's very likely python-pip-wheel is
#   not available. Turn off the rpmwheels bcond until
#   python-pip is built with a wheel to get around the issue.
%bcond_with bootstrap

# Whether to use RPM build wheels from the python-{pip,setuptools,wheel}-wheel packages
# Uses upstream bundled prebuilt wheels otherwise
# Only F39+ has a pip new enough to work with Python 3.12
%if 0%{?fedora} >= 39 || 0%{?rhel} >= 10
%bcond_without rpmwheels
%else
%bcond_with rpmwheels
%endif
# If the rpmwheels condition is disabled, we use the bundled wheel packages
# from Python with the versions below.
# This needs to be manually updated when we update Python.
%global pip_version 25.0.1
%global setuptools_version 79.0.1
%global wheel_version 0.40.0
# All of those also include a list of indirect bundled libs:
# pip
#  $ %%{_rpmconfigdir}/pythonbundles.py <(unzip -p Lib/ensurepip/_bundled/pip-*.whl pip/_vendor/vendor.txt)
%global pip_bundled_provides %{expand:
Provides: bundled(python3dist(cachecontrol)) = 0.14.1
Provides: bundled(python3dist(certifi)) = 2024.8.30
Provides: bundled(python3dist(distlib)) = 0.3.9
Provides: bundled(python3dist(distro)) = 1.9
Provides: bundled(python3dist(idna)) = 3.10
Provides: bundled(python3dist(msgpack)) = 1.1
Provides: bundled(python3dist(packaging)) = 24.2
Provides: bundled(python3dist(platformdirs)) = 4.3.6
Provides: bundled(python3dist(pygments)) = 2.18
Provides: bundled(python3dist(pyproject-hooks)) = 1.2
Provides: bundled(python3dist(requests)) = 2.32.3
Provides: bundled(python3dist(resolvelib)) = 1.0.1
Provides: bundled(python3dist(rich)) = 13.9.4
Provides: bundled(python3dist(setuptools)) = 70.3
Provides: bundled(python3dist(tomli)) = 2.2.1
Provides: bundled(python3dist(truststore)) = 0.10
Provides: bundled(python3dist(typing-extensions)) = 4.12.2
Provides: bundled(python3dist(urllib3)) = 1.26.20
}
# setuptools
# vendor.txt not in .whl
# %%{_rpmconfigdir}/pythonbundles.py <(unzip -l Lib/test/wheeldata/setuptools-*.whl | grep -E '_vendor/.+dist-info/RECORD' | sed -E 's@^.*/([^-]+)-([^-]+)\.dist-info/.*$@\1==\2@')
%global setuptools_bundled_provides %{expand:
Provides: bundled(python3dist(autocommand)) = 2.2.2
Provides: bundled(python3dist(backports-tarfile)) = 1.2
Provides: bundled(python3dist(importlib-metadata)) = 8
Provides: bundled(python3dist(inflect)) = 7.3.1
Provides: bundled(python3dist(jaraco-collections)) = 5.1
Provides: bundled(python3dist(jaraco-context)) = 5.3
Provides: bundled(python3dist(jaraco-functools)) = 4.0.1
Provides: bundled(python3dist(jaraco-text)) = 3.12.1
Provides: bundled(python3dist(more-itertools)) = 10.3
Provides: bundled(python3dist(packaging)) = 24.2
Provides: bundled(python3dist(platformdirs)) = 4.2.2
Provides: bundled(python3dist(tomli)) = 2.0.1
Provides: bundled(python3dist(typeguard)) = 4.3
Provides: bundled(python3dist(typing-extensions)) = 4.12.2
Provides: bundled(python3dist(wheel)) = 0.45.1
Provides: bundled(python3dist(zipp)) = 3.19.2
}
# wheel
#  $ %%{_rpmconfigdir}/pythonbundles.py <(unzip -p Lib/test/wheeldata/wheel-*.whl wheel/vendored/vendor.txt)
%global wheel_bundled_provides %{expand:
Provides: bundled(python3dist(packaging)) = 23
}

# Expensive optimizations (mainly, profile-guided optimizations)
%bcond_without optimizations

# Run the test suite in %%check
%bcond_without tests

# Extra build for debugging the interpreter or C-API extensions
# (the -debug subpackages)
%bcond_without debug_build

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

# We use the upstream arch triplets, we convert them from %%{_arch}-linux%%{_gnu}
%global platform_triplet %{expand:%(echo %{_arch}-linux%{_gnu} | sed -E \\
    -e 's/^arm(eb)?-linux-gnueabi$/arm\\1-linux-gnueabihf/' \\
    -e 's/^mips64(el)?-linux-gnu$/mips64\\1-linux-gnuabi64/' \\
    -e 's/^ppc(64)?(le)?-linux-gnu$/powerpc\\1\\2-linux-gnu/')}

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

%if %{with main_python}
# To keep the upgrade path clean, we Obsolete python3.X from the python3
# package and python3.X-foo from individual subpackages.
# Note that using Obsoletes without package version is not standard practice.
# Here we assert that *any* version of the system's default interpreter is
# preferable to an "extra" interpreter. For example, python3-3.6.1 will
# replace python3.6-3.6.2.
%define unversioned_obsoletes_of_python3_X_if_main() %{expand:\
Obsoletes: python%{pybasever}%{?1:-%{1}}\
}
%else
%define unversioned_obsoletes_of_python3_X_if_main() %{nil}
%endif

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
%if %{undefined rhel}
BuildRequires: libb2-devel
%endif
BuildRequires: libffi-devel
BuildRequires: libnsl2-devel
BuildRequires: libtirpc-devel
BuildRequires: libGL-devel
BuildRequires: libuuid-devel
BuildRequires: libxcrypt-devel
BuildRequires: libX11-devel
BuildRequires: make
BuildRequires: mpdecimal-devel
BuildRequires: ncurses-devel

BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: python-rpm-macros
BuildRequires: readline-devel
BuildRequires: redhat-rpm-config >= 127
BuildRequires: sqlite-devel
BuildRequires: gdb

BuildRequires: tar
BuildRequires: tcl-devel < 1:9
BuildRequires: tix-devel
BuildRequires: tk-devel < 1:9
BuildRequires: tzdata

# Perf support is only available on x86_64 and aarch64 right now
%ifarch x86_64 aarch64
BuildRequires: perf
%endif

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
# Python 3.12 removed the deprecated imp module,
# the first compatible version of pip is 23.1.2.
BuildRequires: %{python_wheel_pkg_prefix}-pip-wheel >= 23.1.2
%if %{with tests}
BuildRequires: %{python_wheel_pkg_prefix}-setuptools-wheel
BuildRequires: (%{python_wheel_pkg_prefix}-wheel-wheel if %{python_wheel_pkg_prefix}-setuptools-wheel < 71)
%endif
%endif

%if %{without bootstrap}
# for make regen-all
# Note that we're not using the %%{pkgname} macro here on purpose, because when
# upgrading the main python3 to a new Python version, this would pull in the
# old version instead.
BuildRequires: python%{pybasever}
%endif

%if %{without bootstrap} || %{without main_python}
# for proper automatic provides
BuildRequires: python3-rpm-generators
%endif

# =======================
# Source code and patches
# =======================

Source0: %{url}ftp/python/%{general_version}/Python-%{upstream_version}.tar.xz
Source1: %{url}ftp/python/%{general_version}/Python-%{upstream_version}.tar.xz.asc
# The release manager for Python 3.12 is Thomas Wouters
Source2: https://github.com/Yhg1s.gpg

# A simple script to check timestamps of bytecode files
# Run in check section with Python that is currently being built
# Originally written by bkabrda
Source8: check-pyc-timestamps.py

# Desktop menu entry for idle3
Source10: idle3.desktop

# AppData file for idle3
Source11: idle3.appdata.xml

# (Patches taken from github.com/fedora-python/cpython)

# 00251 # 6a4ec74157aa01f1ada9f29f30a371cd9e5369e8
# Change user install location
#
# Set values of base and platbase in sysconfig from /usr
# to /usr/local when RPM build is not detected
# to make pip and similar tools install into separate location.
#
# Fedora Change: https://fedoraproject.org/wiki/Changes/Making_sudo_pip_safe
# Downstream only.
#
# We've tried to rework in Fedora 36/Python 3.10 to follow https://bugs.python.org/issue43976
# but we have identified serious problems with that approach,
# see https://bugzilla.redhat.com/2026979 or https://bugzilla.redhat.com/2097183
#
# pypa/distutils integration: https://github.com/pypa/distutils/pull/70
Patch251: 00251-change-user-install-location.patch

# 00371 # 0e580d52dd79a1973e9b363ad7487e7b9334f2a2
# Revert "bpo-1596321: Fix threading._shutdown() for the main thread (GH-28549) (GH-28589)"
#
# This reverts commit 38c67738c64304928c68d5c2bd78bbb01d979b94. It
# introduced regression causing FreeIPA's tests to fail.
#
# For more info see:
# https://bodhi.fedoraproject.org/updates/FEDORA-2021-e152ce5f31
# https://github.com/GrahamDumpleton/mod_wsgi/issues/730
Patch371: 00371-revert-bpo-1596321-fix-threading-_shutdown-for-the-main-thread-gh-28549-gh-28589.patch

# 00460 # 1da89114f7ee7e7f392128a9861d9c2b41c0ddeb
# gh-132415: Update vendored setuptools in ``Lib/test/wheeldata``
#
# (actual changes in .whl files removed to make this patch smaller)
#
# gh-127906: Add missing sys import to test_cppext
Patch460: 00460-gh-132415-update-vendored-setuptools-in-lib-test-wheeldata.patch

# 00461 # f7bc103c7bcc6e48789b225e06daf835793e1086
# Downstream only: Install wheel in test venvs when setuptools < 71
Patch461: 00461-downstream-only-install-wheel-in-test-venvs-when-setuptools-71.patch

# 00462 # 5324dc5f57e0068f7e4f7b2f20006e88ff5f4e47
# Fix PySSL_SetError handling SSL_ERROR_SYSCALL
#
# Python 3.10 changed from using SSL_write() and SSL_read() to SSL_write_ex() and
# SSL_read_ex(), but did not update handling of the return value.
#
# Change error handling so that the return value is not examined.
# OSError (not EOF) is now returned when retval is 0.
#
# This resolves the issue of failing tests when a system is
# stressed on OpenSSL 3.5.
Patch462: 00462-fix-pyssl_seterror-handling-ssl_error_syscall.patch

# 00464 # 1c713e02a26bf8865bb6421749d19d0766cac178
# Enable PAC and BTI protections for aarch64
#
# Apply protection against ROP/JOP attacks for aarch64 on asm_trampoline.S
#
# The BTI flag must be applied in the assembler sources for this class
# of attacks to be mitigated on newer aarch64 processors.
#
# Upstream PR: https://github.com/python/cpython/pull/130864/files
#
# The upstream patch is incomplete but only for the case where
# frame pointers are not used on 3.13+.
#
# Since on Fedora we always compile with frame pointers the BTI/PAC
# hardware protections can be enabled without losing Perf unwinding.
Patch464: 00464-enable-pac-and-bti-protections-for-aarch64.patch

# 00471 # 37c05f26d11e8e24f2a760167015a267996b1d69
# CVE-2025-12084
#
# * gh-142145: Remove quadratic behavior in node ID cache clearing (GH-142146)
# * gh-142754: Ensure that Element & Attr instances have the ownerDocument attribute (GH-142794)
Patch471: 00471-cve-2025-12084.patch

# 00472 # 2ba215eaba508b2cdd7c3acfdf3b9a6e32872274
# CVE-2025-13836
#
# [3.12] gh-119451: Fix a potential denial of service in http.client (GH-119454) (#142140)
#
# gh-119451: Fix a potential denial of service in http.client (GH-119454)
#
# Reading the whole body of the HTTP response could cause OOM if
# the Content-Length value is too large even if the server does not send
# a large amount of data. Now the HTTP client reads large data by chunks,
# therefore the amount of consumed memory is proportional to the amount
# of sent data.
Patch472: 00472-cve-2025-13836.patch

# 00473 # dd705786aa0c1ccfde913858598e34e1f196be2e
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

# 00475 # 3748209a316662d4e85981ca1a7418547a1d25c6
# CVE-2025-15367
#
# gh-143923: Reject control characters in POP3 commands
#
# (cherry-picked from commit b234a2b67539f787e191d2ef19a7cbdce32874e7)
Patch475: 00475-cve-2025-15367.patch

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
# packages with fully versioned naming scheme (e.g. python3.9*) exist for
# non-default versions of Python 3.
# For consistency, we provide python3.X from python3 as well.
Provides: python%{pybasever} = %{version}-%{release}
Provides: python%{pybasever}%{?_isa} = %{version}-%{release}

%unversioned_obsoletes_of_python3_X_if_main

# https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package
# https://fedoraproject.org/wiki/Changes/Python_means_Python3
# We recommend /usr/bin/python so users get it by default
# Versioned recommends are problematic, and we know that the package requires
# python3 back with fixed version, so we just use the path here:
Recommends: %{_bindir}/python
%endif

# Python interpreter packages used to be named (or provide) name pythonXY (e.g.
# python39). However, to align it with the executable names and to prepare for
# Python 3.10, they were renamed to pythonX.Y (e.g. python3.9, python3.10). We
# provide the previous names.
Provides: python%{pyshortver} = %{version}-%{release}

%if %{with main_python} || %{with python_abi_provides_for_alt_pythons}
# Packages with Python modules in standard locations automatically
# depend on python(abi). Provide that here.
Provides: python(abi) = %{pybasever}
%else
# We exclude the `python(abi)` Provides
%global __requires_exclude ^python\\(abi\\) = 3\\..+
%global __provides_exclude ^python\\(abi\\) = 3\\..+
%endif

Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}

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
Requires: %{python_wheel_pkg_prefix}-pip-wheel >= 23.1.2
# Bundled libb2 is CC0, covered by grandfathering exception
License: Python-2.0.1 AND CC0-1.0
%else
Provides: bundled(python3dist(pip)) = %{pip_version}
%pip_bundled_provides
# License manually combined form Python + pip
License: Python-2.0.1 AND CC0-1.0 AND MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND ISC AND LGPL-2.1-only AND MPL-2.0 AND (Apache-2.0 OR BSD-2-Clause)
%endif

%unversioned_obsoletes_of_python3_X_if_main libs

# Bundled internal headers are used even when building with system libb2
# last updated by https://github.com/python/cpython/pull/6286
Provides: bundled(libb2) = 0.98.1

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
# When built with a specific expat version, but installed with an older one,
# we sometimes get:
#   ImportError: /usr/lib64/python3.X/lib-dynload/pyexpat.cpython-....so:
#   undefined symbol: XML_...
# The pyexpat module has build-time checks for expat version to only use the
# available symbols. However, there is no runtime protection, so when the module
# is later installed with an older expat, it may error due to undefined symbols.
# This breaks many things, including python -m venv.
# We avoid this problem by requiring at least the same version of expat that
# was used during the build time.
# Other subpackages (like -debug) also need this, but they all depend on -libs.
%global expat_version %(LANG=C rpm -q --qf '%%{version}' expat.%{_target_cpu} | sed 's/.*not installed/0/')
Requires: expat%{?_isa} >= %{expat_version}


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
# We omit this dependency on RHEL to avoid pulling the macros to AppStream:
# RHEL users can use the minimal implementation of %%pyproject_buildrequires
# from pyproject-srpm-macros instead.
# On Fedora, we keep this to avoid one additional round of %%generate_buildrequires.
%{!?rhel:Requires: (pyproject-rpm-macros if rpm-build)}

%unversioned_obsoletes_of_python3_X_if_main devel

%if %{with main_python}
# Python developers are very likely to need pip
Recommends: %{pkgname}-pip
%endif

# tox users are likely to need the devel subpackage
Supplements: tox

%if %{without bootstrap} || %{without main_python}
# Generators run on the main Python 3 so we cannot require them when bootstrapping it
Requires: (python3-rpm-generators if rpm-build)
%endif

Provides: %{pkgname}-2to3 = %{version}-%{release}

%if %{with main_python}
Provides: 2to3 = %{version}-%{release}
%endif

Conflicts: %{pkgname} < %{version}-%{release}

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

%unversioned_obsoletes_of_python3_X_if_main idle

%if %{with main_python}
Provides: idle3 = %{version}-%{release}
Provides: idle = %{version}-%{release}
%endif

Provides: %{pkgname}-tools = %{version}-%{release}
Provides: %{pkgname}-tools%{?_isa} = %{version}-%{release}

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

%unversioned_obsoletes_of_python3_X_if_main tkinter

# The importable module "turtle" is here, so provide python3-turtle.
# (We don't provide python3-turtledemo, that's not too useful when imported.)
%py_provides %{pkgname}-turtle

%description -n %{pkgname}-tkinter
The Tkinter (Tk interface) library is a graphical user interface toolkit for
the Python programming language.


%package -n %{pkgname}-test
Summary: The self-test suite for the main python3 package
Requires: %{pkgname} = %{version}-%{release}
Requires: %{pkgname}-libs%{?_isa} = %{version}-%{release}

%if %{with rpmwheels}
Requires: %{python_wheel_pkg_prefix}-setuptools-wheel
Requires: (%{python_wheel_pkg_prefix}-wheel-wheel if %{python_wheel_pkg_prefix}-setuptools-wheel < 71)
%else
Provides: bundled(python3dist(setuptools)) = %{setuptools_version}
%setuptools_bundled_provides
Provides: bundled(python3dist(wheel)) = %{wheel_version}
%wheel_bundled_provides
# License manually combined from Python + setuptools + wheel
License: Python-2.0.1 AND MIT AND Apache-2.0 AND (Apache-2.0 OR BSD-2-Clause)
%endif

%unversioned_obsoletes_of_python3_X_if_main test

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

%unversioned_obsoletes_of_python3_X_if_main debug

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


# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%gpgverify -k2 -s1 -d0
%autosetup -S git_am -n Python-%{upstream_version}

# Verify the second level of bundled provides is up to date
# Arguably this should be done in %%check, but %%prep has a faster feedback loop
# setuptools.whl does not contain the vendored.txt files
if [ -f %{_rpmconfigdir}/pythonbundles.py ]; then
  %{_rpmconfigdir}/pythonbundles.py <(unzip -p Lib/ensurepip/_bundled/pip-*.whl pip/_vendor/vendor.txt) --compare-with '%pip_bundled_provides'
  %{_rpmconfigdir}/pythonbundles.py <(unzip -p Lib/test/wheeldata/wheel-*.whl wheel/vendored/vendor.txt) --compare-with '%wheel_bundled_provides'
  %{_rpmconfigdir}/pythonbundles.py <(unzip -l Lib/test/wheeldata/setuptools-*.whl | grep -E '_vendor/.+dist-info/RECORD' | sed -E 's@^.*/([^-]+)-([^-]+)\.dist-info/.*$@\1==\2@') --compare-with '%setuptools_bundled_provides'
fi

%if %{with rpmwheels}
rm Lib/ensurepip/_bundled/pip-%{pip_version}-py3-none-any.whl
rm Lib/test/wheeldata/setuptools-%{setuptools_version}-py3-none-any.whl
rm Lib/test/wheeldata/wheel-%{wheel_version}-py3-none-any.whl
%endif

# Remove all exe files to ensure we are not shipping prebuilt binaries
# note that those are only used to create Microsoft Windows installers
# and that functionality is broken on Linux anyway
find -name '*.exe' -print -delete

# Remove bundled libraries to ensure that we're using the system copy.
rm -r Modules/expat
rm -r Modules/_decimal/libmpdec

# Remove files that should be generated by the build
# (This is after patching, so that we can use patches directly from upstream)
rm configure pyconfig.h.in


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

  # A workaround for https://bugs.python.org/issue39761
  export DFLAGS=" "

%configure \
  --with-platlibdir=%{_lib} \
  --enable-ipv6 \
  --enable-shared \
  --with-computed-gotos=%{computed_gotos_flag} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --with-system-expat \
  --with-system-libmpdec \
  --enable-loadable-sqlite-extensions \
  --with-dtrace \
  --with-lto \
  --with-ssl-default-suites=openssl \
  --without-static-libpython \
%if %{with rpmwheels}
  --with-wheel-pkg-dir=%{python_wheel_dir} \
%endif
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

# When the actual %%{dynload_dir} exists (it does when python3.X is installed for regen-all)
# %%{buildroot}%%{dynload_dir} is not created by make install and the extension modules are missing
# Reported upstream as https://github.com/python/cpython/issues/98782
# A workaround is to create the directory before running make install
mkdir -p %{buildroot}%{dynload_dir}

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

# Make sure sysconfig looks at the right pyconfig-32.h/pyconfig-64.h file instead of pyconfig.h
# See https://bugzilla.redhat.com/show_bug.cgi?id=201434
# and https://bugzilla.redhat.com/show_bug.cgi?id=653058
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/sysconfig.py

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
  %{_rpmconfigdir}/redhat/pathfix.py \
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
-x 'bad_coding|badsyntax|site-packages|test/test_lib2to3/data'

# Turn this BRP off, it is done by compileall2 --hardlink-dupes above
%global __brp_python_hardlink %{nil}

# Since we have *.py files in bindir, this is created, but we don't want it
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
rm %{buildroot}%{_mandir}/man1/python3.1
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
%if %{with debug_build}
ln -s ./python3-debug %{buildroot}%{_bindir}/python-debug
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
  # --timeout=2700: kill test running for longer than 45 minutes
  # test_freeze_simple_script is skipped, because it fails without bundled libs.
  #  the freeze tool is only usable from the source checkout anyway,
  #  we don't ship it in the RPM package.
  # test_check_probes is failing since it was introduced in 3.12.0rc1,
  # the test is skipped until it is fixed in upstream.
  # see: https://github.com/python/cpython/issues/104280#issuecomment-1669249980
  # test_gdb is skipped due to https://bugzilla.redhat.com/2275274#c11

  LD_LIBRARY_PATH=$ConfDir $ConfDir/python -m test.regrtest \
    -wW --slowest %{_smp_mflags} --timeout=2700 \
    -i test_freeze_simple_script \
    -i test_check_probes \
    -x test_gdb \
    %ifarch %{mips64}
    -x test_ctypes \
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


%if %{with main_python}
%files -n python-unversioned-command
%{_bindir}/python
%{_mandir}/*/python.1*
%endif

%files -n %{pkgname}-libs
%doc README.rst

%dir %{pylibdir}
%dir %{dynload_dir}

%license %{pylibdir}/LICENSE.txt

%{pylibdir}/lib2to3

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
%{pylibdir}/ensurepip/_bundled/pip-%{pip_version}-py3-none-any.whl
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
%{dynload_dir}/_sha2.%{SOABI_optimized}.so
%{dynload_dir}/_sha3.%{SOABI_optimized}.so

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
%{dynload_dir}/zlib.%{SOABI_optimized}.so
%{dynload_dir}/_zoneinfo.%{SOABI_optimized}.so

%dir %{pylibdir}/site-packages/
%dir %{pylibdir}/site-packages/__pycache__/
%{pylibdir}/site-packages/README.txt

%if %{with debug_build}
%exclude %{pylibdir}/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}.py
%exclude %{pylibdir}/__pycache__/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}%{bytecode_suffixes}
%endif

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

%dir %{pylibdir}/importlib/metadata/
%dir %{pylibdir}/importlib/metadata/__pycache__/
%{pylibdir}/importlib/metadata/*.py
%{pylibdir}/importlib/metadata/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/importlib/resources/
%dir %{pylibdir}/importlib/resources/__pycache__/
%{pylibdir}/importlib/resources/*.py
%{pylibdir}/importlib/resources/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/json/
%dir %{pylibdir}/json/__pycache__/
%{pylibdir}/json/*.py
%{pylibdir}/json/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/logging
%{pylibdir}/multiprocessing

%dir %{pylibdir}/re/
%dir %{pylibdir}/re/__pycache__/
%{pylibdir}/re/*.py
%{pylibdir}/re/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/sqlite3/
%dir %{pylibdir}/sqlite3/__pycache__/
%{pylibdir}/sqlite3/*.py
%{pylibdir}/sqlite3/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/tomllib/
%dir %{pylibdir}/tomllib/__pycache__/
%{pylibdir}/tomllib/*.py
%{pylibdir}/tomllib/__pycache__/*%{bytecode_suffixes}
%exclude %{pylibdir}/turtle.py
%exclude %{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}

%{pylibdir}/urllib
%{pylibdir}/xml

%dir %{pylibdir}/zipfile/
%dir %{pylibdir}/zipfile/__pycache__/
%{pylibdir}/zipfile/*.py
%{pylibdir}/zipfile/__pycache__/*%{bytecode_suffixes}
%dir %{pylibdir}/zipfile/_path/
%dir %{pylibdir}/zipfile/_path/__pycache__/
%{pylibdir}/zipfile/_path/*.py
%{pylibdir}/zipfile/_path/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/zoneinfo

%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages/__pycache__/
%endif

# "Makefile" and the config-32/64.h file are needed by
# sysconfig.py:get_config_vars(), so we include them in the core
# package, along with their parent directories (bug 531901):
%dir %{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/
%{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/Makefile
%dir %{_includedir}/python%{LDVERSION_optimized}/
%{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}

%{_libdir}/%{py_INSTSONAME_optimized}
%if %{with main_python}
%{_libdir}/libpython3.so
%endif


%files -n %{pkgname}-devel
%{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/*
%exclude %{pylibdir}/config-%{LDVERSION_optimized}-%{platform_triplet}/Makefile
%exclude %{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}
%{_includedir}/python%{LDVERSION_optimized}/*.h
%{_includedir}/python%{LDVERSION_optimized}/internal/
%{_includedir}/python%{LDVERSION_optimized}/cpython/
%doc Misc/README.valgrind Misc/valgrind-python.supp

%if %{with main_python}
%{_bindir}/2to3
%{_bindir}/python3-config
%{_bindir}/python-config
%{_libdir}/pkgconfig/python3.pc
%{_libdir}/pkgconfig/python.pc
%{_libdir}/pkgconfig/python3-embed.pc
%{_bindir}/pygettext3.py
%{_bindir}/pygettext.py
%{_bindir}/msgfmt3.py
%{_bindir}/msgfmt.py
%endif

%{_bindir}/2to3-%{pybasever}
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


%files -n %{pkgname}-idle
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

%files -n %{pkgname}-tkinter
%{pylibdir}/tkinter
%{dynload_dir}/_tkinter.%{SOABI_optimized}.so
%{pylibdir}/turtle.py
%{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}
%dir %{pylibdir}/turtledemo
%{pylibdir}/turtledemo/*.py
%{pylibdir}/turtledemo/*.cfg
%dir %{pylibdir}/turtledemo/__pycache__/
%{pylibdir}/turtledemo/__pycache__/*%{bytecode_suffixes}


%files -n %{pkgname}-test
%{pylibdir}/test
%{dynload_dir}/_ctypes_test.%{SOABI_optimized}.so
%{dynload_dir}/_testbuffer.%{SOABI_optimized}.so
%{dynload_dir}/_testcapi.%{SOABI_optimized}.so
%{dynload_dir}/_testclinic.%{SOABI_optimized}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_optimized}.so
%{dynload_dir}/_testinternalcapi.%{SOABI_optimized}.so
%{dynload_dir}/_testmultiphase.%{SOABI_optimized}.so
%{dynload_dir}/_testsinglephase.%{SOABI_optimized}.so
%{dynload_dir}/_xxinterpchannels.%{SOABI_optimized}.so
%{dynload_dir}/_xxsubinterpreters.%{SOABI_optimized}.so
%{dynload_dir}/_xxtestfuzz.%{SOABI_optimized}.so
%{dynload_dir}/xxlimited.%{SOABI_optimized}.so
%{dynload_dir}/xxlimited_35.%{SOABI_optimized}.so
%{dynload_dir}/xxsubtype.%{SOABI_optimized}.so

%dir %{pylibdir}/__phello__/
%dir %{pylibdir}/__phello__/__pycache__/
%{pylibdir}/__phello__/__init__.py
%{pylibdir}/__phello__/spam.py
%{pylibdir}/__phello__/__pycache__/*%{bytecode_suffixes}

# We don't bother splitting the debug build out into further subpackages:
# if you need it, you're probably a developer.

# Hence the manifest is the combination of analogous files in the manifests of
# all of the other subpackages

%if %{with debug_build}
%files -n %{pkgname}-debug
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
%{dynload_dir}/_sha2.%{SOABI_debug}.so
%{dynload_dir}/_sha3.%{SOABI_debug}.so

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

# Analog of the -tools subpackage's files:
#  None for now; we could build precanned versions that have the appropriate
# shebang if needed

# Analog  of the tkinter subpackage's files:
%{dynload_dir}/_tkinter.%{SOABI_debug}.so

# Analog  of the -test subpackage's files:
%{dynload_dir}/_ctypes_test.%{SOABI_debug}.so
%{dynload_dir}/_testbuffer.%{SOABI_debug}.so
%{dynload_dir}/_testcapi.%{SOABI_debug}.so
%{dynload_dir}/_testclinic.%{SOABI_debug}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_debug}.so
%{dynload_dir}/_testinternalcapi.%{SOABI_debug}.so
%{dynload_dir}/_testmultiphase.%{SOABI_debug}.so
%{dynload_dir}/_testsinglephase.%{SOABI_debug}.so
%{dynload_dir}/_xxinterpchannels.%{SOABI_debug}.so
%{dynload_dir}/_xxsubinterpreters.%{SOABI_debug}.so
%{dynload_dir}/_xxtestfuzz.%{SOABI_debug}.so
%{dynload_dir}/xxlimited.%{SOABI_debug}.so
%{dynload_dir}/xxlimited_35.%{SOABI_debug}.so
%{dynload_dir}/xxsubtype.%{SOABI_debug}.so

%{pylibdir}/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}.py
%{pylibdir}/__pycache__/_sysconfigdata_%{ABIFLAGS_debug}_linux_%{platform_triplet}%{bytecode_suffixes}

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
* Fri Feb 06 2026 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.12-4
- Security fixes for CVE-2026-0865, CVE-2025-15366 and CVE-2025-15367

* Fri Jan 16 2026 Lumír Balhar <lbalhar@redhat.com> - 3.12.12-3
- Security fix for CVE-2025-13836

* Tue Jan 06 2026 Lumír Balhar <lbalhar@redhat.com> - 3.12.12-2
- Security fix for CVE-2025-12084
- Require at least the same expat version as used during the build time

* Fri Oct 10 2025 Karolina Surma <ksurma@redhat.com> - 3.12.12-1
- Update to 3.12.12

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 12 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.12.11-2
- Enable PAC and BTI hardware protections for aarch64

* Wed Jun 04 2025 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.11-1
- Update to 3.12.11

* Fri May 09 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.12.10-4
- Fix PySSL_SetError handling SSL_ERROR_SYSCALL
- This fixes random flakiness of test_ssl on stressed machines

* Tue May 06 2025 Miro Hrončok <mhroncok@redhat.com> - 3.12.10-3
- Drop requirement on python-wheel-wheel with setuptools >= 71

* Tue Apr 22 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.12.10-2
- Apply Intel's CET for mitigation against control-flow hijacking attacks

* Wed Apr 09 2025 Miro Hrončok <mhroncok@redhat.com> - 3.12.10-1
- Update to 3.12.10

* Mon Mar 31 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.12.9-3
- Properly apply exported CFLAGS for dtrace/systemtap builds
- Fixes: rhbz#2356301

* Thu Feb 06 2025 Miro Hrončok <mhroncok@redhat.com> - 3.12.9-2
- Rebuilt with mpdecimal 4.0.0

* Tue Feb 04 2025 Charalampos Stratakis <cstratak@redhat.com> - 3.12.9-1
- Update to 3.12.9
- Security fix for CVE-2025-0938
- Fixes: rhbz#2343275

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 3.12.8-4
- Add explicit BR: libxcrypt-devel

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.12.8-2
- Security fix for CVE-2024-12254
- Fixes: rhbz#2330926

* Tue Dec 03 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.12.8-1
- Update to 3.12.8
- Security fix for CVE-2024-9287
- Fixes: rhbz#2321656

* Tue Oct 01 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.7-1
- Update to 3.12.7

* Mon Sep 09 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.6-1
- Update to 3.12.6
- Fixes: rhbz#2310090

* Fri Aug 23 2024 Charalampos Stratakis <cstratak@redhat.com> - 3.12.5-2
- Security fix for CVE-2024-8088
- Fixes: rhbz#2307461

* Wed Aug 07 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.5-1
- Update to 3.12.5
- Fixes: rhbz#2303159 (email header injection)

* Tue Jul 23 2024 Lumír Balhar <lbalhar@redhat.com> - 3.12.4-3
- Require systemtap-sdt-devel for sys/sdt.h

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.4-1
- Update to 3.12.4

* Thu Jun 06 2024 Python Maint <python-maint@redhat.com> - 3.12.3-3
- Build as non-main Python

* Wed Apr 17 2024 Miro Hrončok <mhroncok@redhat.com> - 3.12.3-2
- Require expat >= 2.6 to prevent errors when creating venvs with older expat

* Wed Apr 10 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.3-1
- Update to 3.12.3

* Thu Mar 21 2024 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-3
- Move all test modules to the python3-test package, namely:
   - __phello__
   - _xxsubinterpreters
   - xxlimited
   - xxlimited_35
   - xxsubtype

* Wed Feb 21 2024 Miro Hrončok <mhroncok@redhat.com> - 3.12.2-2
- Fix tests for XMLPullParser with Expat 2.6.0

* Wed Feb 07 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.2-1
- Update to 3.12.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Lumír Balhar <lbalhar@redhat.com> - 3.12.1-2
- Security fix for CVE-2023-27043 (rhbz#2196190)

* Fri Dec 08 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.1-1
- Update to 3.12.1
- Own stray directories in /usr/lib64/python3.12
- Fixes: rhbz#2252143

* Thu Oct 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.12.0-2
- Use bundled libb2 in RHEL builds

* Mon Oct 02 2023 Miro Hrončok <mhroncok@redhat.com> - 3.12.0-1
- Update to 3.12.0 final

* Tue Sep 19 2023 Miro Hrončok <mhroncok@redhat.com> - 3.12.0~rc3-1
- Update to 3.12.0rc3

* Wed Sep 06 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~rc2-1
- Update to 3.12.0rc2

* Mon Aug 07 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~rc1-1
- Update to 3.12.0rc1

* Wed Aug 02 2023 Charalampos Stratakis <cstratak@redhat.com> - 3.12.0~b4-3
- Remove extra distro-applied CFLAGS passed to user built C extensions
- https://fedoraproject.org/wiki/Changes/Python_Extension_Flags_Reduction

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0~b4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Miro Hrončok <mhroncok@redhat.com> - 3.12.0~b4-1
- Update to 3.12.0b4

* Wed Jun 21 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~b3-2
- Backport upstream patch to add PyType_GetDict() function

* Tue Jun 20 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~b3-1
- Update to 3.12.0b3

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.12.0~b2-3
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.12.0~b2-2
- Bootstrap for Python 3.12

* Wed Jun 07 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~b2-1
- Update to 3.12.0b2

* Mon May 29 2023 Miro Hrončok <mhroncok@redhat.com> - 3.12.0~b1-2
- Use wheels from RPMs, at least on Fedora 39+
- On older Fedora releases, declare bundled() provides and a complex License tag

* Tue May 23 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~b1-1
- Update to 3.12.0b1

* Wed Apr 05 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~a7-1
- Update to 3.12.0a7

* Thu Mar 23 2023 Miro Hrončok <mhroncok@redhat.com> - 3.12.0~a6-2
- Increase the test timeout during package build

* Wed Mar 08 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~a6-1
- Update to 3.12.0a6

* Wed Feb 08 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~a5-1
- Update to 3.12.0a5

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.0~a4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~a4-1
- Update to 3.12.0a4

* Mon Dec 19 2022 Miro Hrončok <mhroncok@redhat.com> - 3.12.0~a3-2
- No longer patch the default bytecode cache invalidation policy

* Wed Dec 07 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~a3-1
- Update to 3.12.0a3

* Tue Nov 15 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~a2-1
- Update to 3.12.0a2
- Fixes: rhbz#2133847

* Thu Oct 27 2022 Miro Hrončok <mhroncok@redhat.com> - 3.12.0~a1-2
- Finish initial bootstrap of Python 3.12.0a1

* Wed Oct 26 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 3.12.0~a1-1
- Initial Python 3.12 package forked from Python 3.11
