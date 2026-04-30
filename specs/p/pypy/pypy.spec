## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 12;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Note: When this is updated to 7.4,
# the installation layout will change in a backwards-incompatible way.
# That'll be a good time to rename this to pypy2.7 and adapt %%pypyprefix to be
# %%{_libdir}/pypy%%{pyversion} (see e.g. pypy3.7 or pypy3.8 for inspiration).
%global basever 7.3
Name:           pypy
Version:        %{basever}.20
%global pyversion 2.7
Release:        %autorelease
Summary:        Python implementation with a Just-In-Time compiler

# LGPL and another free license we'd need to ask spot about are present in some
# java jars that we're not building with atm (in fact, we're deleting them
# before building).  If we restore those we'll have to work out the new
# licensing terms
# PyPy is MIT
# Python standard library is Python-2.0.1
# pyrepl is MIT-CMU
# pypy/module/unicodedata is Unicode-3.0
# Bundled cffi is is MIT
# Bundled pycparser is is BSD-3-Clause
# Bundled pycparser.ply is BSD-3-Clause
# Bundled bits from cryptography are Apache-2.0 OR BSD-3-Clause
License:        MIT AND MIT-CMU AND Python-2.0.1 AND Unicode-3.0 AND BSD-3-Clause AND (Apache-2.0 OR BSD-3-Clause)
URL:            https://www.pypy.org/

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

# High-level configuration of the build:

# Whether to use RPM build wheels from the python-{pip,setuptools}-wheel package
# Uses upstream bundled prebuilt wheels otherwise
# setuptools >= 45.0 no longer support Python 2.7, hence disabled
%bcond rpmwheels 0

# PyPy consists of an implementation of an interpreter (with JIT compilation)
# for the full Python language  written in a high-level language, leaving many
# of the implementation details as "pluggable" policies.
#
# The implementation language is then compiled down to .c code, from which we
# obtain a binary.
#
# This allows us to build a near-arbitrary collection of different
# implementations of Python with differing tradeoffs
#
# (As it happens, the implementation language is itself Python, albeit a
# restricted subset "RPython", chosen to making it amenable to being compiled.
# The result implements the full Python language though)

# We could build many different implementations of Python.
# For now, let's focus on the implementation that appears to be receiving the
# most attention upstream: the JIT-enabled build, with all standard
# optimizations

# Building a configuration can take significant time:

# A build of pypy (with jit) on i686 took 77 mins:
#  [Timer] Timings:
#  [Timer] annotate                       ---  583.3 s
#  [Timer] rtype_lltype                   ---  760.9 s
#  [Timer] pyjitpl_lltype                 ---  567.3 s
#  [Timer] backendopt_lltype              ---  375.6 s
#  [Timer] stackcheckinsertion_lltype     ---   54.1 s
#  [Timer] database_c                     ---  852.2 s
#  [Timer] source_c                       --- 1007.3 s
#  [Timer] compile_c                      ---  419.9 s
#  [Timer] ===========================================
#  [Timer] Total:                         --- 4620.5 s
#
# A build of pypy (nojit) on x86_64 took about an hour:
#  [Timer] Timings:
#  [Timer] annotate                       ---  537.5 s
#  [Timer] rtype_lltype                   ---  667.3 s
#  [Timer] backendopt_lltype              ---  385.4 s
#  [Timer] stackcheckinsertion_lltype     ---   42.5 s
#  [Timer] database_c                     ---  625.3 s
#  [Timer] source_c                       --- 1040.2 s
#  [Timer] compile_c                      ---  273.9 s
#  [Timer] ===========================================
#  [Timer] Total:                         --- 3572.0 s
#
#
# A build of pypy-stackless on i686 took about 87 mins:
#  [Timer] Timings:
#  [Timer] annotate                       ---  584.2 s
#  [Timer] rtype_lltype                   ---  777.3 s
#  [Timer] backendopt_lltype              ---  365.9 s
#  [Timer] stackcheckinsertion_lltype     ---   39.3 s
#  [Timer] database_c                     --- 1089.6 s
#  [Timer] source_c                       --- 1868.6 s
#  [Timer] compile_c                      ---  490.4 s
#  [Timer] ===========================================
#  [Timer] Total:                         --- 5215.3 s


# We will build a "pypy" binary.
#
# Unfortunately, the JIT support is only available on some architectures.
#
# rpython/jit/backend/detect_cpu.py:getcpuclassname currently supports the
# following options:
#  'i386', 'x86'
#  'x86-without-sse2':
#  'x86_64'
#  'armv6', 'armv7' (versions 6 and 7, hard- and soft-float ABI)
#  'cli'
#  'llvm'
#
# We will only build with JIT support on those architectures, and build without
# it on the other archs.  The resulting binary will typically be slower than
# CPython for the latter case.

%global src_name %{ver_name}-v%{version}-src

%ifarch %{ix86} x86_64 %{arm} s390x %{power64} aarch64 riscv64
%global with_jit 1
%else
%global with_jit 0
%endif

# Should we build a "pypy-stackless" binary?
%global with_stackless 0

# Should we build the emacs JIT-viewing mode?
%if 0%{?rhel} == 6
%global with_emacs 0
%else
%global with_emacs 1
%endif

# Easy way to enable/disable verbose logging:
%global verbose_logs 0

# Easy way to turn off the selftests:
%global run_selftests 1

%global pypy_include_dir  %{pypyprefix}/include
%global pypyprefix %{_libdir}/%{name}-%{basever}
%global pylibver 2.7
%global pymajorlibver 2
%global ver_name  %{name}%{pymajorlibver}

# We refer to this subdir of the source tree in a few places during the build:
%global goal_dir pypy/goal

%ifarch %{ix86} x86_64 %{arm}
%global _package_note_linker gold
%endif

# Source and patches:
Source0: https://downloads.python.org/pypy/pypy%{pyversion}-v%{version}-src.tar.bz2

# Supply various useful RPM macros for building python modules against pypy:
#  __pypy, pypy_sitelib, pypy_sitearch
Source1: macros.%{name}
#  __pypy2, pypy2_sitelib, pypy2_sitearch
Source2: macros.%{name}%{pymajorlibver}

# Patch for the bundled pip wheel for CVE-2023-5752
# https://github.com/pypa/pip/pull/12119
# https://github.com/pypa/pip/pull/12306
# https://github.com/pypa/pip/pull/12373
Source3: pip-CVE-2023-5752.patch

# Patch for the bundled setuptools wheel for CVE-2024-6345
# Remote code execution via download functions in the package_index module
# Tracking bug: https://bugzilla.redhat.com/show_bug.cgi?id=2297771
# Upstream solution: https://github.com/pypa/setuptools/pull/4332
# Patch simplified because upstream doesn't support SVN anymore.
Source4: setuptools-CVE-2024-6345.patch

# Patch for the bundled setuptools wheel for CVE-2025-47273
# Path traversal in PackageIndex.download leads to Arbitrary File Write
# Tracking bug: https://bugzilla.redhat.com/show_bug.cgi?id=2366982
# Upstream solution: https://github.com/pypa/setuptools/commit/250a6d17978f9f6ac3ac887091f2d32886fbbb0b
# Patch modified for Python 2
Source5: setuptools-CVE-2025-47273.patch

# Patch for the bundled requests within the bundled pip for CVE-2024-47081
# .netrc credentials leaked with malicious URLs
# Tracking bug: https://bugzilla.redhat.com/show_bug.cgi?id=2371272
# Upstream fix: https://github.com/psf/requests/pull/6965
Source6: pip-requests-CVE-2024-47081.patch

# Patch for the bundled urllib3 within the bundled pip for CVE-2025-50181
# Redirects are not disabled when retries are disabled on PoolManager instantiation
# Tracking bug: https://bugzilla.redhat.com/show_bug.cgi?id=2373799
# Upstream fix: https://github.com/urllib3/urllib3/commit/f05b1329126d5be6de501f9d1e3e36738bc08857
Source7: pip-urllib3-CVE-2025-50181.patch

# Patch pypy.translator.platform so that stdout from "make" etc gets logged,
# rather than just stderr, so that the command-line invocations of the compiler
# and linker are captured:
Patch0: 006-always-log-stdout.patch

# Disable the printing of a quote from IRC on startup (these are stored in
# ROT13 form in lib_pypy/_pypy_irc_topic.py).  Some are cute, but some could
# cause confusion for end-users (and many are in-jokes within the PyPy
# community that won't make sense outside of it).  [Sorry to be a killjoy]
Patch1: 007-remove-startup-message.patch

# Glibc's libcrypt was replaced with libxcrypt in f28, crypt.h header has
# to be added to privent compilation error.
# https://fedoraproject.org/wiki/Changes/Replace_glibc_libcrypt_with_libxcrypt
Patch2: 009-add-libxcrypt-support.patch

# Instead of bundled wheels, use our RPM packaged wheels from
# /usr/share/python-wheels
# We conditionally apply this, but we use autosetup, so we use Source here
Source189: 189-use-rpm-wheels.patch

# 00382 #
# Make mailcap refuse to match unsafe filenames/types/params (GH-91993)
#
# Upstream: https://github.com/python/cpython/issues/68966
#
# Tracker bug: https://bugzilla.redhat.com/show_bug.cgi?id=2075390
#
# Backported from python3.
Patch382: 382-cve-2015-20107.patch

# 00394 #
# gh-98433: Fix quadratic time idna decoding.
#
# There was an unnecessary quadratic loop in idna decoding. This restores
# the behavior to linear.
#
# Backported from python3.
Patch394: 394-cve-2022-45061-cpu-denial-of-service-via-inefficient-idna-decoder.patch

# 00399 #
# CVE-2023-24329
#
# gh-102153: Start stripping C0 control and space chars in `urlsplit` (GH-102508)
#
# `urllib.parse.urlsplit` has already been respecting the WHATWG spec a bit GH-25595.
#
# This adds more sanitizing to respect the "Remove any leading C0 control or space from input" [rule](https://url.spec.whatwg.org/GH-url-parsing:~:text=Remove%%20any%%20leading%%20and%%20trailing%%20C0%%20control%%20or%%20space%%20from%%20input.) in response to [CVE-2023-24329](https://nvd.nist.gov/vuln/detail/CVE-2023-24329).
#
# Backported from Python 3.12
Patch399: 399-cve-2023-24329.patch

# Build-time requirements:

# pypy's can be rebuilt using itself, rather than with CPython; doing so
# halves the build time.
#
# Turn it off with this boolean, to revert back to rebuilding using CPython
# and avoid a cycle in the build-time dependency graph:

%global use_self_when_building 1
%if 0%{use_self_when_building}
BuildRequires: pypy2
%global bootstrap_python_interp pypy2
%else
# exception to use Python 2: https://pagure.io/fesco/issue/2130
BuildRequires: python27
%global bootstrap_python_interp python2
%endif

BuildRequires:  gcc

BuildRequires:  libffi-devel
BuildRequires:  tcl-devel < 1:9
BuildRequires:  tk-devel < 1:9

BuildRequires:  sqlite-devel

BuildRequires:  zlib-devel
BuildRequires:  bzip2-devel
BuildRequires:  ncurses-devel
BuildRequires:  expat-devel
BuildRequires:  openssl-devel
%if 0%{?fedora} >= 41
BuildRequires:  openssl-devel-engine
%endif
BuildRequires:  gdbm-devel
BuildRequires:  chrpath

BuildRequires:  python-rpm-macros

%ifarch %{valgrind_arches}
BuildRequires:  valgrind-devel
%endif

%if %{run_selftests}
# Used by the selftests, though not by the build:
BuildRequires:  gc-devel

# For use in the selftests, for recording stats:
BuildRequires:  time

# For use in the selftests, for imposing a per-test timeout:
BuildRequires:  perl-interpreter
%endif

# All arches have execstack
BuildRequires:  execstack

# For byte-compiling the JIT-viewing mode:
%if %{with_emacs}
BuildRequires:  emacs
%endif

# For %%autosetup -S git
BuildRequires:  %{_bindir}/git

%if %{with rpmwheels}
BuildRequires: python-setuptools-wheel < 45
BuildRequires: python-pip-wheel
%endif

# Metadata for the core package (the JIT build):
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{ver_name} = %{version}-%{release}
Provides: %{ver_name}%{_isa} = %{version}-%{release}
Provides: pypy%{pyversion} = %{version}-%{release}
Provides: pypy%{pyversion}%{_isa} = %{version}-%{release}
Provides: %{ver_name}(abi) = %{basever}

%description
PyPy's implementation of Python, featuring a Just-In-Time compiler on some CPU
architectures, and various optimized implementations of the standard types
(strings, dictionaries, etc)

%if 0%{with_jit}
This build of PyPy has JIT-compilation enabled.
%else
This build of PyPy has JIT-compilation disabled, as it is not supported on this
CPU architecture.
%endif


%package libs
Summary:  Run-time libraries used by PyPy implementations of Python

%if %{without rpmwheels}
# PyPy is MIT AND MIT-CMU AND Python-2.0.1 AND Unicode-3.0 AND BSD-3-Clause AND (Apache-2.0 OR BSD-3-Clause) (see the main package license)
# setuptools is MIT and bundles:
#   packaging: BSD-2-Clause OR Apache-2.0
#   pyparsing: MIT
#   six: MIT
# pip is MIT and bundles:
#   appdirs: MIT
#   distlib: Python-2.0.1
#   distro: Apache-2.0
#   html5lib: MIT
#   six: MIT
#   colorama: BSD-3-Clause
#   CacheControl: Apache-2.0
#   msgpack-python: Apache-2.0
#   lockfile: MIT
#   progress: ISC
#   ipaddress: Python-2.0.1
#   packaging: BSD-2-Clause OR Apache-2.0
#   pep517: MIT
#   pyparsing: MIT
#   pytoml: MIT
#   retrying: Apache-2.0
#   requests: Apache-2.0
#   chardet: LGPL-2.0-or-later
#   idna: BSD-3-Clause
#   urllib3: MIT
#   certifi: MPL-2.0
#   setuptools: MIT
#   webencodings: BSD-3-Clause
License: MIT AND MIT-CMU AND Python-2.0.1 AND Unicode-3.0 AND BSD-3-Clause AND (Apache-2.0 OR BSD-3-Clause) AND (BSD-2-Clause OR Apache-2.0) AND Apache-2.0 AND ISC AND LGPL-2.0-or-later AND MPL-2.0
%endif

# We supply an emacs mode for the JIT viewer.
# (This doesn't bring in all of emacs, just the directory structure)
%if %{with_emacs}
Requires: emacs-filesystem%{?_emacs_version: >= %{_emacs_version}}
%endif

%if %{with rpmwheels}
Requires: python-setuptools-wheel < 45
Requires: python-pip-wheel
%else
Provides: bundled(python2dist(setuptools)) = 44.0.0
Provides: bundled(python2dist(packaging)) = 16.8
Provides: bundled(python2dist(pyparsing)) = 2.2.1
Provides: bundled(python2dist(six)) = 1.10.0

Provides: bundled(python2dist(pip)) = 20.0.2
Provides: bundled(python2dist(appdirs)) = 1.4.3
Provides: bundled(python2dist(CacheControl)) = 0.12.6
Provides: bundled(python2dist(contextlib2)) = 0.6.0
Provides: bundled(python2dist(certifi)) = 2019.11.28
Provides: bundled(python2dist(chardet)) = 3.0.4
Provides: bundled(python2dist(colorama)) = 0.4.3
Provides: bundled(python2dist(distlib)) = 0.3.0
Provides: bundled(python2dist(distro)) = 1.4.0
Provides: bundled(python2dist(html5lib)) = 1.0.1
Provides: bundled(python2dist(idna)) = 2.8
Provides: bundled(python2dist(ipaddress)) = 1.0.23
Provides: bundled(python2dist(lockfile)) = 0.12.2
Provides: bundled(python2dist(msgpack)) = 0.6.2
Provides: bundled(python2dist(packaging)) = 20.1
Provides: bundled(python2dist(pep517)) = 0.7.0
Provides: bundled(python2dist(progress)) = 1.5
Provides: bundled(python2dist(pyparsing)) = 2.4.6
Provides: bundled(python2dist(pytoml)) = 0.1.21
Provides: bundled(python2dist(requests)) = 2.22.0
Provides: bundled(python2dist(retrying)) = 1.3.3
Provides: bundled(python2dist(setuptools)) = 44.0.0
Provides: bundled(python2dist(six)) = 1.14.0
Provides: bundled(python2dist(urllib3)) = 1.25.7
Provides: bundled(python2dist(webencodings)) = 0.5.1
%endif

# Find the version in lib_pypy/cffi/_pycparser/__init__.py
Provides: bundled(python2dist(pycparser)) = 2.22

# Find the version in lib_pypy/cffi/_pycparser/ply/__init__.py
Provides: bundled(python2dist(ply)) = 3.9

# Find the version in lib_pypy/_cffi_ssl/cryptography/__about__.py
Provides: bundled(python2dist(cryptography)) = 2.7

Provides: %{ver_name}-libs = %{version}-%{release}
Provides: %{ver_name}-libs%{_isa} = %{version}-%{release}
Provides: pypy%{pyversion}-libs = %{version}-%{release}
Provides: pypy%{pyversion}-libs%{_isa} = %{version}-%{release}

%description libs
Libraries required by the various PyPy implementations of Python.


%package devel
Summary:  Development tools for working with PyPy
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: %{ver_name}-devel = %{version}-%{release}
Provides: %{ver_name}-devel%{_isa} = %{version}-%{release}
Provides: pypy%{pyversion}-devel = %{version}-%{release}
Provides: pypy%{pyversion}-devel%{_isa} = %{version}-%{release}

%description devel
Header files for building C extension modules against PyPy


%if 0%{with_stackless}
%package stackless
Summary:  Stackless Python interpreter built using PyPy
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Provides: %{ver_name}-stackless = %{version}-%{release}
Provides: %{ver_name}-stackless%{_isa} = %{version}-%{release}
Provides: pypy%{pyversion}-stackless = %{version}-%{release}
Provides: pypy%{pyversion}-stackless%{_isa} = %{version}-%{release}
%description stackless
Build of PyPy with support for micro-threads for massive concurrency
%endif


%prep
%autosetup -n pypy%{pyversion}-v%{version}-src -p1 -S git

# Temporary workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1954999
%{?!apply_patch:%define apply_patch(qp:m:) {%__apply_patch %**}}

%if %{with rpmwheels}
%apply_patch -m %(basename %{SOURCE189}) %{SOURCE189}
rm lib-python/2.7/ensurepip/_bundled/*.whl
rmdir lib-python/2.7/ensurepip/_bundled
%endif

%if %{without rpmwheels}
# Patch the bundled pip wheel for CVE-2023-5752, CVE-2024-47081, CVE-2025-50181
unzip -qq lib-python/2.7/ensurepip/_bundled/pip-20.0.2-py2.py3-none-any.whl
patch -p1 < %{SOURCE3}
patch -p1 < %{SOURCE6}
patch -p1 < %{SOURCE7}
zip -rq lib-python/2.7/ensurepip/_bundled/pip-20.0.2-py2.py3-none-any.whl pip pip-20.0.2.dist-info
rm -rf pip/ pip-20.0.2.dist-info/

# Patch the bundled setuptools wheel for CVE-2024-6345, CVE-2025-47273
unzip -qq lib-python/2.7/ensurepip/_bundled/setuptools-44.0.0-py2.py3-none-any.whl
patch -p1 < %{SOURCE4}
patch -p1 < %{SOURCE5}
zip -rq lib-python/2.7/ensurepip/_bundled/setuptools-44.0.0-py2.py3-none-any.whl easy_install.py pkg_resources setuptools setuptools-44.0.0.dist-info
rm -rf easy_install.py pkg_resources/ setuptools/ setuptools-44.0.0.dist-info/
%endif


# Replace /usr/local/bin/python or /usr/bin/env python shebangs with /usr/bin/python2 or pypy2:
find \( -name "*.py" -o -name "py.cleanup" \) -exec \
  sed \
    -i -r -e "s@/usr/(local/)?bin/(env )?python(2|3)?@/usr/bin/%{bootstrap_python_interp}@" \
    "{}" \
    \;

for f in rpython/translator/goal/bpnn.py ; do
   # Detect shebang lines && remove them:
   sed -e '/^#!/Q 0' -e 'Q 1' $f \
      && sed -i '1d' $f
   chmod a-x $f
done

rm -rf lib-python/3

# Replace all lib-python python shebangs with pypy
find lib-python/%{pylibver} -name "*.py" -exec \
  sed -r -i '1s|^#!\s*/usr/bin.*python.*|#!/usr/bin/%{name}|' \
    "{}" \
    \;

%if ! 0%{use_self_when_building}
  # use the pycparser from PyPy even on CPython
  ln -s lib_pypy/cffi/_pycparser pycparser
%endif

# Remove windows executable binaries
rm lib-python/2.7/distutils/command/*.exe

%build
%ifarch s390x
# pypy3 requires z10 at least
%global optflags %(echo %{optflags} | sed 's/-march=z9-109 /-march=z10 /')
%endif

BuildPyPy() {
  ExeName=$1
  Options=$2

  echo "--------------------------------------------------------------"
  echo "--------------------------------------------------------------"
  echo "--------------------------------------------------------------"
  echo "STARTING BUILD OF: $ExeName"
  echo "--------------------------------------------------------------"
  echo "--------------------------------------------------------------"
  echo "--------------------------------------------------------------"

  pushd %{goal_dir}

  # The build involves invoking a python script, passing in particular
  # arguments, environment variables, etc.
  # Some notes on those follow:

  # The generated binary embeds copies of the values of all environment
  # variables.  We need to unset "RPM_BUILD_ROOT" to avoid a fatal error from
  #  /usr/lib/rpm/check-buildroot
  # during the postprocessing of the rpmbuild, complaining about this
  # reference to the buildroot


  # By default, pypy's autogenerated C code is placed in
  #    /tmp/usession-N
  #  
  # and it appears that this stops rpm from extracting the source code to the
  # debuginfo package
  #
  # The logic in pypy-1.4/pypy/tool/udir.py indicates that it is generated in:
  #    $PYPY_USESSION_DIR/usession-$PYPY_USESSION_BASENAME-N    
  # and so we set PYPY_USESSION_DIR so that this tempdir is within the build
  # location, and set $PYPY_USESSION_BASENAME so that the tempdir is unique
  # for each invocation of BuildPyPy

  # Compilation flags for C code:
  #   pypy-1.4/pypy/translator/c/genc.py:gen_makefile
  # assembles a Makefile within
  #   THE_UDIR/testing_1/Makefile
  # calling out to platform.gen_makefile
  # For us, that's
  #   pypy-1.4/pypy/translator/platform/linux.py: class BaseLinux(BasePosix):
  # which by default has:
  #   CFLAGS = ['-O3', '-pthread', '-fomit-frame-pointer',
  #             '-Wall', '-Wno-unused']
  # plus all substrings from CFLAGS in the environment.
  # This is used to generate a value for CFLAGS that's written into the Makefile

  # How will we track garbage-collection roots in the generated code?
  #   http://pypy.readthedocs.org/en/latest/config/translation.gcrootfinder.html

  # This is the most portable option, and avoids a reliance on non-guaranteed
  # behaviors within GCC's code generator: use an explicitly-maintained stack
  # of root pointers:
  %global gcrootfinder_options --gcrootfinder=shadowstack

  export CFLAGS=$(echo "$RPM_OPT_FLAGS" | sed -e 's/-g//')

  # The generated C code leads to many thousands of warnings of the form:
  #   warning: variable 'l_v26003' set but not used [-Wunused-but-set-variable]
  # Suppress them:
  export CFLAGS=$(echo "$CFLAGS" -Wno-unused -fPIC)

  # If we're already built the JIT-enabled "pypy", then use it for subsequent
  # builds (of other configurations):
  if test -x './pypy' ; then
    INTERP='./pypy'
    %ifarch %{arm}
      # Reduce memory usage on arm during installation
      PYPY_GC_MAX_DELTA=200MB $INTERP --jit loop_longevity=300 ../../rpython/bin/rpython -Ojit targetpypystandalone
    %endif
  else
    # First pypy build within this rpm build?
    # Fall back to using the bootstrap python interpreter, which might be a
    # system copy of pypy from an earlier rpm, or be cpython's /usr/bin/python:
    INTERP='%{bootstrap_python_interp}'
  fi

  # Here's where we actually invoke the build:
  RPM_BUILD_ROOT= \
  PYPY_USESSION_DIR=$(pwd) \
  PYPY_USESSION_BASENAME=$ExeName \
  $INTERP ../../rpython/bin/rpython  \
  %{gcrootfinder_options} \
  $Options \
  targetpypystandalone \
%ifarch riscv64
  --withoutmod-_continuation \
%endif
;

  echo "--------------------------------------------------------------"
  echo "--------------------------------------------------------------"
  echo "--------------------------------------------------------------"
  echo "FINISHED BUILDING: $ExeName"
  echo "--------------------------------------------------------------"
  echo "--------------------------------------------------------------"
  echo "--------------------------------------------------------------"

  popd
}

BuildPyPy \
  %{name} \
%if 0%{with_jit}
  "-Ojit" \
%else
  "-O2" \
%endif
  %{nil}

%if 0%{with_stackless}
BuildPyPy \
  %{name}-stackless \
   "--stackless"
%endif

%if %{with_emacs}
%{_emacs_bytecompile} rpython/jit/tool/pypytrace-mode.el
%endif


%install

mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{pypyprefix}

#%if 0%{with_stackless}
#InstallPyPy %{name}-stackless
#%endif


# Run installing script,  archive-name  %{name}-%{basever} in %{buildroot}/%{_libdir} == %{pypyprefix}
%{bootstrap_python_interp} pypy/tool/release/package.py --archive-name %{name}-%{basever} --builddir %{buildroot}/%{_libdir} --no-embedded-dependencies

# Remove shebang lines from .py files that aren't executable, and
# remove executability from .py files that don't have a shebang line:
find \
  %{buildroot}                                                           \
  -name "*.py"                                                           \
    \(                                                                   \
       \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \;   \
             -print -exec sed -i '1d' {} \;                              \
          \)                                                             \
       -o                                                                \
       \(                                                                \
             -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \;         \
             -exec chmod a-x {} \;                                       \
        \)                                                               \
    \)


execstack --clear-execstack %{buildroot}/%{pypyprefix}/bin/pypy

# Bytecompile all of the .py files we ship, using our pypy binary, giving us
# .pyc files for pypy.
#
# Note that some of the test files deliberately contain syntax errors, so
# we are running it in subshell, to be able to ignore the failures and not to terminate the build.
(%{py_byte_compile %{buildroot}%{pypyprefix}/bin/pypy %{buildroot}%{pypyprefix}}) || :


%{buildroot}%{pypyprefix}/bin/%{name} -c 'import _tkinter'
%{buildroot}%{pypyprefix}/bin/%{name} -c 'import Tkinter'
%{buildroot}%{pypyprefix}/bin/%{name} -c 'import _sqlite3'
%{buildroot}%{pypyprefix}/bin/%{name} -c 'import _curses'
%{buildroot}%{pypyprefix}/bin/%{name} -c 'import curses'
%{buildroot}%{pypyprefix}/bin/%{name} -c 'import syslog'
%{buildroot}%{pypyprefix}/bin/%{name} -c 'from _sqlite3 import *'


# Header files for C extension modules.
# Upstream's packaging process (pypy/tool/release/package.py)
# creates an "include" subdir and copies all *.h/*.inl from "include" there
# (it also has an apparently out-of-date comment about copying them from
# pypy/_interfaces, but this directory doesn't seem to exist, and it doesn't
# seem to do this as of 2011-01-13)

# Capture the RPython source code files from the build within the debuginfo
# package (rhbz#666975)
%global pypy_debuginfo_dir /usr/src/debug/pypy-%{version}-src
mkdir -p %{buildroot}%{pypy_debuginfo_dir}

# copy over everything:
cp -a pypy %{buildroot}%{pypy_debuginfo_dir}

# ...then delete files that aren't:
#   - *.py files
#   - the Makefile
#   - typeids.txt
#   - dynamic-symbols-*
#find \
#  %{buildroot}%{pypy_debuginfo_dir}  \
#  \( -type f                         \
#     -a                              \
#     \! \( -name "*.py"              \
#           -o                        \
#           -name "Makefile"          \
#           -o                        \
#           -name "typeids.txt"       \
#           -o                        \
#           -name "dynamic-symbols-*" \
#        \)                           \
#  \)                                 \
#  -delete

# Alternatively, we could simply keep everything.  This leads to a ~350MB
# debuginfo package, but it makes it easy to hack on the Makefile and C build
# flags by rebuilding/linking the sources.
# To do so, remove the above "find" command.

# We don't need bytecode for these files; they are being included for reference
# purposes.
# There are some rpmlint warnings from these files:
#   non-executable-script
#   wrong-script-interpreter
#   zero-length
#   script-without-shebang
#   dangling-symlink
# but given that the objective is to preserve a copy of the source code, those
# are acceptable.

# Install the JIT trace mode for Emacs:
%if %{with_emacs}
mkdir -p %{buildroot}/%{_emacs_sitelispdir}
cp -a rpython/jit/tool/pypytrace-mode.el %{buildroot}/%{_emacs_sitelispdir}/%{name}trace-mode.el
cp -a rpython/jit/tool/pypytrace-mode.elc %{buildroot}/%{_emacs_sitelispdir}/%{name}trace-mode.elc
%endif

# Create executables pypy, pypy2 and pypy2.7
ln -sf %{pypyprefix}/bin/%{name} %{buildroot}%{_bindir}/%{name}%{pylibver}
ln -sf %{_bindir}/%{name}%{pylibver} %{buildroot}%{_bindir}/%{name}%{pymajorlibver}
ln -sf %{_bindir}/%{name}%{pymajorlibver} %{buildroot}%{_bindir}/%{name}

# Move files to the right places and remove unnecessary files
mv %{buildroot}/%{pypyprefix}/bin/libpypy-c.so %{buildroot}/%{_libdir}
rm -rf %{buildroot}/%{_libdir}/%{name}-%{basever}.tar.bz2
rm -rf %{buildroot}/%{pypyprefix}/README.rst
rm -rf %{buildroot}/%{pypyprefix}/README.rst
rm -rf %{buildroot}/%{pypy_include_dir}/README
chrpath --delete %{buildroot}/%{pypyprefix}/bin/%{name}

# Install macros for rpm:
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE1} %{buildroot}/%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE2} %{buildroot}/%{_rpmconfigdir}/macros.d

# Remove build script from the package
#rm %{buildroot}/%{pypyprefix}/lib_pypy/ctypes_config_cache/rebuild.py

# since 5.10.0, the debug binaries are built and shipped, making the
# pypy package ~350 MiB. let's remove them here for now and TODO figure out why
rm -f %{buildroot}%{pypyprefix}/bin/pypy.debug
rm -f %{buildroot}%{pypyprefix}/bin/libpypy-c.so.debug

%if %{without rpmwheels}
# Inject SBOM into the installed wheels
%{?python_wheel_inject_sbom:%python_wheel_inject_sbom %{buildroot}%{pypyprefix}/lib-python/%{pylibver}/ensurepip/_bundled/*.whl}
%endif

%check
topdir=$(pwd)

SkipTest() {
    TEST_NAME=$1
    sed -i -e"s|^$TEST_NAME$||g" testnames.txt
}

CheckPyPy() {
    # We'll be exercising one of the freshly-built binaries using the
    # test suite from the standard library (overridden in places by pypy's
    # modified version)
    ExeName=$1

    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
    echo "STARTING TEST OF: $ExeName"
    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"

    pushd %{goal_dir}

    # I'm seeing numerous cases where tests seem to hang, or fail unpredictably
    # So we'll run each test in its own process, with a timeout

    # Use regrtest to explicitly list all tests:
    ( ./$ExeName -c \
         "from test.regrtest import findtests; print('\n'.join(findtests()))"
    ) > testnames.txt

    # Skip some tests:
      # "audioop" doesn't exist for pypy yet:
      SkipTest test_audioop

      # The gdb CPython hooks haven't been ported to cpyext:
      SkipTest test_gdb

      # hotshot relies heavily on _hotshot, which doesn't exist:
      SkipTest test_hotshot

      # "strop" module doesn't exist for pypy yet:
      SkipTest test_strop

      # I'm seeing Koji builds hanging e.g.:
      #   http://koji.fedoraproject.org/koji/getfile?taskID=3386821&name=build.log
      # The only test that seems to have timed out in that log is
      # test_multiprocessing, so skip it for now:
      SkipTest test_multiprocessing

    echo "== Test names =="
    cat testnames.txt
    echo "================="

    echo "" > failed-tests.txt

    for TestName in $(cat testnames.txt) ; do

        echo "===================" $TestName "===================="

        # Use /usr/bin/time (rather than the shell "time" builtin) to gather
        # info on the process (time/CPU/memory).  This passes on the exit
        # status of the underlying command
        #
        # Use perl's alarm command to impose a timeout
        #   900 seconds is 15 minutes per test.
        # If a test hangs, that test should get terminated, allowing the build
        # to continue.
        #
        # Invoke pypy on test.regrtest to run the specific test suite
        # verbosely
        #
        # For now, || true, so that any failures don't halt the build:
        ( /usr/bin/time \
           perl -e 'alarm shift @ARGV; exec @ARGV' 900 \
             ./$ExeName -m test.regrtest -v $TestName ) \
        || (echo $TestName >> failed-tests.txt) \
        || true
    done

    echo "== Failed tests =="
    cat failed-tests.txt
    echo "================="

    popd

    # Doublecheck pypy's own test suite, using the built pypy binary:

    # Disabled for now:
    #   x86_64 shows various failures inside:
    #     jit/backend/x86/test
    #   followed by a segfault inside
    #     jit/backend/x86/test/test_runner.py
    #
    #   i686 shows various failures inside:
    #     jit/backend/x86/test
    #   with the x86_64 failure leading to cancellation of the i686 build

    # Here's the disabled code:
    #    pushd pypy
    #    time translator/goal/$ExeName test_all.py
    #    popd

    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
    echo "FINISHED TESTING: $ExeName"
    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
    echo "--------------------------------------------------------------"
}

#python testrunner/runner.py --logfile=pytest-A.log --config=pypy/pytest-A.cfg --config=pypy/pytest-A.py --root=pypy --timeout=3600
#python pypy/test_all.py --pypy=pypy/goal/pypy --timeout=3600 --resultlog=cpython.log lib-python
#python pypy/test_all.py --pypy=pypy/goal/pypy --resultlog=pypyjit.log pypy/module/pypyjit/test
#pypy/goal/pypy pypy/test_all.py --resultlog=pypyjit_new.log

%if %{run_selftests}
CheckPyPy %{name}-c

%if 0%{with_stackless}
CheckPyPy %{name}-c-stackless
%endif

%endif # run_selftests

# Because there's a bunch of binary subpackages and creating
# /usr/share/doc/pypy3-this and /usr/share/doc/pypy3-that
# is just confusing for the user.
%global _docdir_fmt %{name}

%files libs
%doc README.rst

%dir %{pypyprefix}
%dir %{pypyprefix}/lib-python
%license %{pypyprefix}/LICENSE
%{_libdir}/libpypy-c.so
%{pypyprefix}/lib-python/%{pylibver}/
%{pypyprefix}/lib_pypy/
%{pypyprefix}/site-packages/
%if %{with_emacs}
%{_emacs_sitelispdir}/%{name}trace-mode.el
%{_emacs_sitelispdir}/%{name}trace-mode.elc
%endif

%files
%doc README.rst
%{_bindir}/%{name}
%{_bindir}/%{name}%{pylibver}
%{_bindir}/%{name}%{pymajorlibver}
%{pypyprefix}/bin/

%files devel
%dir %{pypy_include_dir}
%{pypy_include_dir}/*.h
%{pypy_include_dir}/_numpypy
%{_rpmconfigdir}/macros.d/macros.%{name}
%{_rpmconfigdir}/macros.d/macros.%{name}%{pymajorlibver}

%if 0%{with_stackless}
%files stackless
%doc README.rst
%{_bindir}/%{name}-stackless
%endif


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 7.3.20-12
- test: add initial lock files

* Fri Jan 30 2026 Miroslav Suchý <msuchy@redhat.com> - 7.3.20-11
- migrate license to SPDX

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.20-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jan 07 2026 Miro Hrončok <miro@hroncok.cz> - 7.3.20-9
- Enable JIT on riscv64

* Wed Sep 24 2025 Miro Hrončok <miro@hroncok.cz> - 7.3.20-6
- Inject SBOM into the installed wheels

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Charalampos Stratakis <cstratak@redhat.com> - 7.3.20-1
- Update to 7.3.20
- Fixes: rhbz#2376234

* Thu Jul 10 2025 Charalampos Stratakis <cstratak@redhat.com> - 7.3.19-2
- Security fixes for CVE-2025-47273, CVE-2024-47081 and CVE-2025-50181
- Fixes: rhbz#2367430, rhbz#2372476, rhbz#2373817

* Wed Feb 26 2025 Miro Hrončok <miro@hroncok.cz> - 7.3.19-1
- Update to 7.3.19
- Fixes: rhbz#2348403

* Tue Feb 25 2025 Miro Hrončok <miro@hroncok.cz> - 7.3.18-2
- Fix build with -Wincompatible-pointer-types

* Tue Feb 25 2025 Miro Hrončok <miro@hroncok.cz> - 7.3.18-1
- Update to 7.3.18
- Fixes: rhbz#2344159

* Tue Feb 25 2025 Miro Hrončok <miro@hroncok.cz> - 7.3.17-3
- Ensure this package is built with Tk 8
- Fixes: rhbz#2337753

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 03 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 7.3.17-1
- Update to 7.3.17

* Tue Aug 20 2024 Jason Montleon <jmontleo@redhat.com> - 7.3.16-3
- Add --withoutmod-_continuation target option for riscv64

* Thu Aug 01 2024 Miro Hrončok <miro@hroncok.cz> - 7.3.16-2
- Security fix for CVE-2024-6345 (in bundled setuptools wheel)
- Fixes: rhbz#2298675

* Mon Jul 29 2024 Miro Hrončok <miro@hroncok.cz> - 7.3.16-1
- Update to 7.3.16
- Fixes: rhbz#2276781

* Mon Jul 29 2024 Miro Hrončok <miro@hroncok.cz> - 7.3.15-5
- Fix build with
  https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 30 2024 Charalampos Stratakis <cstratak@redhat.com> - 7.3.15-3
- Security fix for CVE-2023-5752 for the bundled pip wheel
- Resolves: rhbz#2250771

* Wed Mar 20 2024 Charalampos Stratakis <cstratak@redhat.com> - 7.3.15-2
- Fix FTBFS with GCC 14 due to incompatible pointers
- Fixes: rhbz#2261538

* Wed Mar 20 2024 Charalampos Stratakis <cstratak@redhat.com> - 7.3.15-1
- Update to 7.3.15
- Fixes: rhbz#2255799

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 04 2023 Miro Hrončok <mhroncok@redhat.com> - 7.3.13-1
- Update to 7.3.13
- Fixes: rhbz#2241297

* Tue Aug 29 2023 Charalampos Stratakis <cstratak@redhat.com> - 7.3.12-3
- Security fix for CVE-2022-45061
- Fixes: rhbz#2144428

* Wed Jul 26 2023 Miro Hrončok <mhroncok@redhat.com> - 7.3.12-1
- Update to 7.3.12
- Fixes: rhbz#2203422

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 29 2023 Charalampos Stratakis <cstratak@redhat.com> - 7.3.11-3
- Security fix for CVE-2023-24329
Resolves: rhbz#2174018

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 30 2022 Miro Hrončok <mhroncok@redhat.com> - 7.3.11-1
- Update to 7.3.11
- Fixes: rhbz#2147521

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Miro Hrončok <mhroncok@redhat.com> - 7.3.9-3
- Use OpenSSL 3 on Fedora 36+
- https://fedoraproject.org/wiki/Changes/OpenSSL3.0
- https://fedoraproject.org/wiki/Changes/DeprecateOpensslCompat

* Tue Jun 28 2022 Charalampos Stratakis <cstratak@redhat.com> - 7.3.9-2
- Security fix for CVE-2015-20107
- Fixes: rhbz#2075390

* Wed Mar 30 2022 Miro Hrončok <mhroncok@redhat.com> - 7.3.9-1
- Update to 7.3.9
- Fixes: rhbz#2069872

* Tue Mar 01 2022 Miro Hrončok <mhroncok@redhat.com> - 7.3.8-1
- Update to 7.3.8
- Fixes: rhbz#2046555

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 7.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Tue Oct 26 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 7.3.6-1
- Update to 7.3.6
- Remove windows executable binaries
- Fixes: rhbz#2003681
- Fixes: rhbz#2005457

* Mon Sep 20 2021 Miro Hrončok <mhroncok@redhat.com> - 7.3.5-2
- Explicitly buildrequire OpenSSL 1.1, as Python 2 is not compatible with OpenSSL 3.0

* Mon Aug 16 2021 Miro Hrončok <mhroncok@redhat.com> - 7.3.5-1
- Update to 7.3.5
- Fixes: rhbz#1992600

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Tomas Hrnciar <thrnciar@redhat.com> - 7.3.4-2
- Replace removed /usr/lib/rpm/brp-python-bytecompile with %%py_byte_compile macros
- Fixes: rhbz#1976656

* Tue May 25 2021 Miro Hrončok <mhroncok@redhat.com> - 7.3.4-1
- Update to 7.3.4

* Tue May 25 2021 Miro Hrončok <mhroncok@redhat.com> - 7.3.1-4
- Provide missing bundled library information

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Tomas Hrnciar <thrnciar@redhat.com> - 7.3.1-1
- Update to 7.3.1

* Wed Feb 12 2020 Miro Hrončok <mhroncok@redhat.com> - 7.3.0-3
- Use bundled wheels, to allow updating setuptools in Fedora

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 28 2019 Miro Hrončok <mhroncok@redhat.com> - 7.3.0-1
- Update to 7.3.0

* Wed Oct 23 2019 Miro Hrončok <mhroncok@redhat.com> - 7.2.0-3
- Enable JIT on aarch64

* Wed Oct 16 2019 Miro Hrončok <mhroncok@redhat.com> - 7.2.0-2
- Enable JIT on power64

* Mon Oct 14 2019 Miro Hrončok <mhroncok@redhat.com> - 7.2.0-1
- Update to 7.2.0
- Enable aarch64

* Sat Jul 27 2019 Peter Robinson <pbrobinson@fedoraproject.org> 7.1.1-3
- Re-enable power64 builds

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Miro Hrončok <mhroncok@redhat.com> - 7.1.1-1
- Update to 7.1.1

* Thu Feb 28 2019 Miro Hrončok <mhroncok@redhat.com> - 7.0.0-1
- Update to 7.0.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 6.0.0-4
- Rebuilt for libcrypt.so.2 (#1666033)

* Tue Aug 21 2018 Miro Hrončok <mhroncok@redhat.com> - 6.0.0-3
- Use RPM packaged wheels

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 26 2018 Michal Cyprian <mcyprian@redhat.com> - 6.0.0-1
- Update to 6.0.0

* Wed Apr 11 2018 Miro Hrončok <mhroncok@redhat.com> - 5.10.0-4
- Provide pypy2(abi) = 5.10

* Tue Apr 10 2018 Miro Hrončok <mhroncok@redhat.com> - 5.10.0-3
- RPM macros improvements

* Tue Mar 27 2018 Michal Cyprian <mcyprian@redhat.com> - 5.10.0-2
- Remove the rightmost version number from the path
- rhbz#1516885: https://bugzilla.redhat.com/show_bug.cgi?id=1516885

* Wed Mar 21 2018 Michal Cyprian <mcyprian@redhat.com> - 5.10.0-1
- Update to 5.10.0

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.9.0-6
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 5.9.0-4
- Rebuilt for switch to libxcrypt

* Fri Dec 08 2017 Michal Cyprian <mcyprian@redhat.com> - 5.9.0-3
- Add pypy2 and pypy2.7 symlinks

* Thu Nov 30 2017 Miro Hrončok <mhroncok@redhat.com> - 5.9.0-2
- Make sure to bytecompile the files and ship .pyc files (#1519238)

* Mon Oct 23 2017 Michal Cyprian <mcyprian@redhat.com> - 5.9.0-1
- Update to 5.9.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Michal Cyprian <mcyprian@redhat.com> - 5.8.0-1
- Update to 5.8.0, add pypy2 provides

* Tue Mar 21 2017 Michal Cyprian <mcyprian@redhat.com> - 5.7.0-1
- Update to 5.7.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 29 2016 Peter Robinson <pbrobinson@fedoraproject.org> 5.6.0-3
- set z10 as the base CPU for s390x build

* Mon Nov 14 2016 Peter Robinson <pbrobinson@fedoraproject.org> 5.6.0-2
- Post boostrap build

* Mon Nov 14 2016 Peter Robinson <pbrobinson@fedoraproject.org> 5.6.0-1
- Update to 5.6.0
- Bootstrap mode for Power64 and s390x

* Thu Sep 01 2016 Michal Cyprian <mcyprian@redhat.com> - 5.4.0-1
- Update to 5.4.0

* Sun Aug 14 2016 Peter Robinson <pbrobinson@fedoraproject.org> 5.0.1-5
- Update supported architectures list

* Thu Jul 21 2016 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-4
- Build with gdbm support
- rhbz#1358482

* Thu Jun 30 2016 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-3
- Fix for: CVE-2016-0772 python: smtplib StartTLS stripping attack
- Raise an error when STARTTLS fails
- rhbz#1303647: https://bugzilla.redhat.com/show_bug.cgi?id=1303647
- rhbz#1351679: https://bugzilla.redhat.com/show_bug.cgi?id=1351679
- Fixed upstream: https://hg.python.org/cpython/rev/b3ce713fb9be

* Fri May 13 2016 Miro Hrončok <mhroncok@redhat.com> - 5.0.1-2
- Move header files back to %%{pypy_include_dir} (rhbz#1328025)

* Mon Mar 21 2016 Michal Cyprian <mcyprian@redhat.com> - 5.0.1-1
- Update to 5.0.1

* Mon Mar 14 2016 Michal Cyprian <mcyprian@redhat.com> - 5.0.0-1
- Update to 5.0.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Michal Cyprian <mcyprian@redhat.com> - 4.0.1-1
- Update to 4.0.1

* Tue Nov 24 2015 Peter Robinson <pbrobinson@fedoraproject.org> 4.0.0-3
- Post bootstrap build

* Tue Nov 24 2015 Peter Robinson <pbrobinson@fedoraproject.org> 4.0.0-2
- All arches have execstack
- Boostrap pypy on ppc64/ppc64le

* Tue Nov 17 2015 Matej Stuchlik <mstuchli@redhat.com> - 4.0.0-1
- Update to 4.0.0

* Mon Aug 31 2015 Michal Cyprian <mcyprian@redhat.com> - 2.6.1-1
- Upgrade to 2.6.1

* Wed Aug 26 2015 Michal Cyprian <mcyprian@redhat.com> - 2.6.0-5
- Use %%{bootstrap_python_interp} macro to run package.py

* Wed Aug 26 2015 Michal Cyprian <mcyprian@redhat.com> - 2.6.0-4
- Fix debuginfo missing sources
Resolves: rhbz#1256001

* Tue Aug 18 2015 Michal Cyprian <mcyprian@redhat.com> - 2.6.0-3
- Use script package.py in install section

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Matej Stuchlik <mstuchli@redhat.com> - 2.6.0-1
- Update to 2.6.0

* Wed Mar  4 2015 Ville Skyttä <ville.skytta@iki.fi> - 2.5.0-2
- Do not mark macros file as %%config (#1074266)

* Tue Feb 17 2015 Matej Stuchlik <mstuchli@redhat.com> - 2.5.0-1
- Update to 2.5.0

* Wed Sep 10 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Tue Sep 02 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.3.1-4
- Move devel subpackage requires so that it gets picked up by rpm

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul  7 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.1-2
- ARMv7 is supported for JIT
- no prelink on aarch64/ppc64le

* Sun Jun 08 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Dennis Gilmore <dennis@ausil.us> - 2.3-4
- valgrind is available everywhere except 31 bit s390

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Thu May 15 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.3-2
- Rebuilt (f21-python)

* Tue May 13 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.3-1
- Updated to 2.3

* Mon Mar 10 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.2.1-3
- Put RPM macros in proper location

* Thu Jan 16 2014 Matej Stuchlik <mstuchli@redhat.com> - 2.2.1-2
- Fixed errors due to missing __pycache__

* Thu Dec 05 2013 Matej Stuchlik <mstuchli@redhat.com> - 2.2.1-1
- Updated to 2.2.1
- Several bundled modules (tkinter, sqlite3, curses, syslog) were
  not bytecompiled properly during build, that is now fixed
- prepared new tests, not enabled yet

* Thu Nov 14 2013 Matej Stuchlik <mstuchli@redhat.com> - 2.2.0-1
- Updated to 2.2.0

* Thu Aug 15 2013 Matej Stuchlik <mstuchli@redhat.com> - 2.1-1
- Updated to 2.1.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Matej Stuchlik <mstuchli@redhat.com> - 2.0.2-4
- Patch1 fix

* Mon Jun 24 2013 Matej Stuchlik <mstuchli@redhat.com> - 2.0.2-3
- Yet another Sources fix

* Mon Jun 24 2013 Matej Stuchlik <mstuchli@redhat.com> - 2.0.2-2
- Fixed Source URL

* Mon Jun 24 2013 Matej Stuchlik <mstuchli@redhat.com> - 2.0.2-1
- 2.0.2, patch 8 does not seem necessary anymore

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-0.2.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 David Malcolm <dmalcolm@redhat.com> - 2.0-0.1.b1
- 2.0b1 (drop upstreamed patch 9)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 David Malcolm <dmalcolm@redhat.com> - 1.9-3
- log all output from "make" (patch 6)
- disable the MOTD at startup (patch 7)
- hide symbols from the dynamic linker (patch 8)
- add PyInt_AsUnsignedLongLongMask (patch 9)
- capture the Makefile, the typeids.txt, and the dynamic-symbols file within
the debuginfo package

* Mon Jun 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9-2
- Compile with PIC, fixes FTBFS on ARM

* Fri Jun  8 2012 David Malcolm <dmalcolm@redhat.com> - 1.9-1
- 1.9

* Fri Feb 10 2012 David Malcolm <dmalcolm@redhat.com> - 1.8-2
- disable C readability patch for now (patch 4)

* Thu Feb  9 2012 David Malcolm <dmalcolm@redhat.com> - 1.8-1
- 1.8; regenerate config patch (patch 0); drop selinux patch (patch 2);
regenerate patch 5

* Tue Jan 31 2012 David Malcolm <dmalcolm@redhat.com> - 1.7-4
- fix an incompatibility with virtualenv (rhbz#742641)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 David Malcolm <dmalcolm@redhat.com> - 1.7-2
- use --gcrootfinder=shadowstack, and use standard Fedora compilation flags,
with -Wno-unused (rhbz#666966 and rhbz#707707)

* Mon Nov 21 2011 David Malcolm <dmalcolm@redhat.com> - 1.7-1
- 1.7: refresh patch 0 (configuration) and patch 4 (readability of generated
code)

* Tue Oct  4 2011 David Malcolm <dmalcolm@redhat.com> - 1.6-7
- skip test_multiprocessing

* Tue Sep 13 2011 David Malcolm <dmalcolm@redhat.com> - 1.6-6
- don't ship the emacs JIT-viewer on el5 and el6 (missing emacs-filesystem;
missing _emacs_bytecompile macro on el5)

* Mon Sep 12 2011 David Malcolm <dmalcolm@redhat.com> - 1.6-5
- build using python26 on el5 (2.4 is too early)
* Thu Aug 25 2011 David Malcolm <dmalcolm@redhat.com> - 1.6-4
- fix SkipTest function to avoid corrupting the name of "test_gdbm"

* Thu Aug 25 2011 David Malcolm <dmalcolm@redhat.com> - 1.6-3
- add rpm macros file to the devel subpackage (source 2)
- skip some tests that can't pass yet

* Sat Aug 20 2011 David Malcolm <dmalcolm@redhat.com> - 1.6-2
- work around test_subprocess failure seen in koji (patch 5)

* Thu Aug 18 2011 David Malcolm <dmalcolm@redhat.com> - 1.6-1
- 1.6
- rewrite the %%check section, introducing per-test timeouts

* Tue Aug  2 2011 David Malcolm <dmalcolm@redhat.com> - 1.5-2
- add pypytrace-mode.el to the pypy-libs subpackage, for viewing JIT trace
logs in emacs

* Mon May  2 2011 David Malcolm <dmalcolm@redhat.com> - 1.5-1
- 1.5

* Wed Apr 20 2011 David Malcolm <dmalcolm@redhat.com> - 1.4.1-10
- build a /usr/bin/pypy (but without the JIT compiler) on architectures that
don't support the JIT, so that they do at least have something that runs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 David Malcolm <dmalcolm@redhat.com> - 1.4.1-8
- disable self-hosting for now, due to fatal error seen JIT-compiling the
translator

* Fri Jan 14 2011 David Malcolm <dmalcolm@redhat.com> - 1.4.1-7
- skip test_ioctl for now

* Thu Jan 13 2011 David Malcolm <dmalcolm@redhat.com> - 1.4.1-6
- add a "pypy-devel" subpackage, and install the header files there
- in %%check, re-run failed tests in verbose mode

* Fri Jan  7 2011 Dan Horák <dan[at]danny.cz> - 1.4.1-5
- valgrind available only on selected architectures

* Wed Jan  5 2011 David Malcolm <dmalcolm@redhat.com> - 1.4.1-4
- rebuild pypy using itself, for speed, with a boolean to break this cycle in
the build-requirement graph (falling back to using "python-devel" aka CPython)
- add work-in-progress patch to try to make generated c more readable
(rhbz#666963)
- capture the RPython source code files from the build within the debuginfo
package (rhbz#666975)

* Wed Dec 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-3
- try to respect the FHS by installing libraries below libdir, rather than
datadir; patch app_main.py to look in this installation location first when
scanning for the pypy library directories.
- clarifications and corrections to the comments in the specfile

* Wed Dec 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-2
- remove .svn directories
- disable verbose logging
- add a %%check section
- introduce %%goal_dir variable, to avoid repetition
- remove shebang line from demo/bpnn.py, as we're treating this as a
documentation file
- regenerate patch 2 to apply without generating a .orig file

* Tue Dec 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.1-1
- 1.4.1; fixup %%setup to reflect change in toplevel directory in upstream
source tarball
- apply SELinux fix to the bundled test_commands.py (patch 2)

* Wed Dec 15 2010 David Malcolm <dmalcolm@redhat.com> - 1.4-4
- rename the jit build and subpackge to just "pypy", and remove the nojit and
sandbox builds, as upstream now seems to be focussing on the JIT build (with
only stackless called out in the getting-started-python docs); disable
stackless for now
- add a verbose_logs specfile boolean; leave it enabled for now (whilst fixing
build issues)
- add more comments, and update others to reflect 1.2 -> 1.4 changes
- re-enable debuginfo within CFLAGS ("-g")
- add the LICENSE and README to all subpackages
- ensure the built binaries don't have the "I need an executable stack" flag
- remove DOS batch files during %%prep (idlelib.bat)
- remove shebang lines from .py files that aren't executable, and remove
executability from .py files that don't have a shebang line (taken from
our python3.spec)
- bytecompile the .py files into .pyc files in pypy's bytecode format

* Sun Nov 28 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-3
- BuildRequire valgrind-devel
- Install pypy library from the new directory
- Disable building with our CFLAGS for now because they are causing a build failure.
- Include site-packages directory

* Sat Nov 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-2
- Add patch to configure the build to use our CFLAGS and link libffi
  dynamically

* Sat Nov 27 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 1.4-1
- Update to 1.4
- Drop patch for py2.6 that's in this build
- Switch to building pypy with itself once pypy is built once as recommended by
  upstream
- Remove bundled, prebuilt java libraries
- Fix license tag
- Fix source url
- Version pypy-libs Req

* Tue May  4 2010 David Malcolm <dmalcolm@redhat.com> - 1.2-2
- cherrypick r72073 from upstream SVN in order to fix the build against
python 2.6.5 (patch 2)

* Wed Apr 28 2010 David Malcolm <dmalcolm@redhat.com> - 1.2-1
- initial packaging

## END: Generated by rpmautospec
