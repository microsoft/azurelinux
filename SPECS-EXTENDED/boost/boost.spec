# Support for documentation installation As the %%doc macro erases the
# target directory ($RPM_BUILD_ROOT%%{_docdir}/%%{name}), manually
# installed documentation must be saved into a temporary dedicated
# directory.
# XXX note that as of rpm 4.9.1, this shouldn't be necessary anymore.
# We should be able to install directly.
%global boost_docdir __tmp_docdir
%global boost_examplesdir __tmp_examplesdir

%if 0%{?flatpak}
# For bundling in Flatpak, currently build without mpich and openmpi,
# which aren't needed and cause prefix=/app errors.
%bcond_with mpich
%bcond_with openmpi
%else
# All arches have mpich
%bcond_without mpich

%ifarch s390
  # No OpenMPI support on these arches
  %bcond_with openmpi
%else
  %bcond_without openmpi
%endif
%endif

%ifnarch %{ix86} x86_64 %{arm} ppc64 ppc64le aarch64
  %bcond_with context
%else
  %bcond_without context
%endif

%bcond_without python3

%ifnarch %{ix86} x86_64
  %bcond_with quadmath
%else
  %bcond_without quadmath
%endif

Name: boost
%global real_name boost
Summary: The free peer-reviewed portable C++ source libraries
Version: 1.69.0
%global version_enc 1_69_0
%global version_suffix 169
Release: 21%{?dist}
License: Boost and MIT and Python
%global obsver %{version}-%{release}

%global toplev_dirname %{real_name}_%{version_enc}
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: http://www.boost.org

Source0: https://sourceforge.net/projects/%{name}/files/%{name}/%{version}/%{toplev_dirname}.tar.bz2
#Source0: https://dl.bintray.com/boostorg/master/%%{name}_%%{version_enc}-snapshot.tar.gz
Source1: libboost_thread.so

# Since Fedora 13, the Boost libraries are delivered with sonames
# equal to the Boost version (e.g., 1.41.0).
%global sonamever %{version}

# boost is an "umbrella" package that pulls in all boost shared library
# components, except for MPI and Python sub-packages.  Those are special
# in that there are alternative implementations to choose from
# (Open MPI and MPICH, and Python 2 and 3), and it's not a big burden
# to have interested parties install them explicitly.
# The subpackages that don't install shared libraries are also not pulled in
# (doc, doctools, examples, jam, static).
Requires: %{name}-atomic%{?_isa} = %{version}-%{release}
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-container%{?_isa} = %{version}-%{release}
Requires: %{name}-contract%{?_isa} = %{version}-%{release}
%if %{with context}
Requires: %{name}-context%{?_isa} = %{version}-%{release}
Requires: %{name}-coroutine%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-date-time%{?_isa} = %{version}-%{release}
%if %{with context}
Requires: %{name}-fiber%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-filesystem%{?_isa} = %{version}-%{release}
Requires: %{name}-graph%{?_isa} = %{version}-%{release}
Requires: %{name}-iostreams%{?_isa} = %{version}-%{release}
Requires: %{name}-locale%{?_isa} = %{version}-%{release}
Requires: %{name}-log%{?_isa} = %{version}-%{release}
Requires: %{name}-math%{?_isa} = %{version}-%{release}
Requires: %{name}-program-options%{?_isa} = %{version}-%{release}
Requires: %{name}-random%{?_isa} = %{version}-%{release}
Requires: %{name}-regex%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Requires: %{name}-stacktrace%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Requires: %{name}-test%{?_isa} = %{version}-%{release}
Requires: %{name}-thread%{?_isa} = %{version}-%{release}
Requires: %{name}-timer%{?_isa} = %{version}-%{release}
Requires: %{name}-type_erasure%{?_isa} = %{version}-%{release}
Requires: %{name}-wave%{?_isa} = %{version}-%{release}

BuildRequires: gcc-c++
BuildRequires: m4
BuildRequires: libstdc++-devel
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
%if %{with python3}
BuildRequires: python3-devel
BuildRequires: python3-numpy
%endif
BuildRequires: libicu-devel
%if %{with quadmath}
BuildRequires: libquadmath-devel
%endif

# https://svn.boost.org/trac/boost/ticket/6150
Patch4: boost-1.50.0-fix-non-utf8-files.patch

# Add a manual page for bjam, based on the on-line documentation:
# http://www.boost.org/boost-build2/doc/html/bbv2/overview.html
Patch5: boost-1.48.0-add-bjam-man-page.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=828856
# https://bugzilla.redhat.com/show_bug.cgi?id=828857
# https://svn.boost.org/trac/boost/ticket/6701
Patch15: boost-1.58.0-pool.patch

# https://svn.boost.org/trac/boost/ticket/5637
Patch25: boost-1.57.0-mpl-print.patch

# https://svn.boost.org/trac/boost/ticket/9038
Patch51: boost-1.58.0-pool-test_linking.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1102667
Patch61: boost-1.57.0-python-libpython_dep.patch
Patch62: boost-1.66.0-python-abi_letters.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1190039
Patch65: boost-1.66.0-build-optflags.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1318383
Patch82: boost-1.66.0-no-rpath.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1541035
Patch83: boost-1.66.0-bjam-build-flags.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1673669
Patch84: boost-1.69-random.patch

# https://github.com/boostorg/mpi/pull/81
Patch85: boost-1.69-mpi-c_data.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1818723
Patch86: boost-1.69-format-allocator.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1832639
Patch87: boost-1.69.0-test-cxx20.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1834764
Patch88: auto_buffer-C-20-compatibility.patch

%bcond_with tests
%bcond_with docs_generated

%description
Boost provides free peer-reviewed portable C++ source libraries.  The
emphasis is on libraries which work well with the C++ Standard
Library, in the hopes of establishing "existing practice" for
extensions and providing reference implementations so that the Boost
libraries are suitable for eventual standardization. (Some of the
libraries have already been included in the C++ 2011 standard and
others have been proposed to the C++ Standards Committee for inclusion
in future standards.)

%package atomic
Summary: Run-time component of boost atomic library
Provides:  boost169-atomic = %{obsver}
Obsoletes: boost169-atomic < %{obsver}

%description atomic

Run-time support for Boost.Atomic, a library that provides atomic data
types and operations on these data types, as well as memory ordering
constraints required for coordinating multiple threads through atomic
variables.

%package chrono
Summary: Run-time component of boost chrono library
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Provides:  boost169-chrono = %{obsver}
Obsoletes: boost169-chrono < %{obsver}

%description chrono

Run-time support for Boost.Chrono, a set of useful time utilities.

%package container
Summary: Run-time component of boost container library
Provides:  boost169-container = %{obsver}
Obsoletes: boost169-container < %{obsver}

%description container

Boost.Container library implements several well-known containers,
including STL containers. The aim of the library is to offer advanced
features not present in standard containers or to offer the latest
standard draft features for compilers that comply with C++03.

%package contract
Summary: Run-time component of boost contract library
Provides:  boost169-contract = %{obsver}
Obsoletes: boost169-contract < %{obsver}

%description contract

Run-time support for boost contract library.
Contract programming for C++. All contract programming features are supported:
Subcontracting, class invariants, postconditions (with old and return values),
preconditions, customizable actions on assertion failure (e.g., terminate
or throw), optional compilation and checking of assertions, etc,
from Lorenzo Caminiti.

%if %{with context}
%package context
Summary: Run-time component of boost context switching library
Provides:  boost169-context = %{obsver}
Obsoletes: boost169-context < %{obsver}

%description context

Run-time support for Boost.Context, a foundational library that
provides a sort of cooperative multitasking on a single thread.

%package coroutine
Summary: Run-time component of boost coroutine library
Provides:  boost169-coroutine = %{obsver}
Obsoletes: boost169-coroutine < %{obsver}

%description coroutine
Run-time support for Boost.Coroutine, a library that provides
generalized subroutines which allow multiple entry points for
suspending and resuming execution.

%endif

%package date-time
Summary: Run-time component of boost date-time library
Provides:  boost169-date-time = %{obsver}
Obsoletes: boost169-date-time < %{obsver}

%description date-time

Run-time support for Boost Date Time, a set of date-time libraries based
on generic programming concepts.

%if %{with context}
%package fiber
Summary: Run-time component of boost fiber library
Provides:  boost169-fiber = %{obsver}
Obsoletes: boost169-fiber < %{obsver}

%description fiber

Run-time support for the Boost Fiber library, a framework for
micro-/userland-threads (fibers) scheduled cooperatively.
%endif

%package filesystem
Summary: Run-time component of boost filesystem library
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Provides:  boost169-filesystem = %{obsver}
Obsoletes: boost169-filesystem < %{obsver}

%description filesystem

Run-time support for the Boost Filesystem Library, which provides
portable facilities to query and manipulate paths, files, and
directories.

%package graph
Summary: Run-time component of boost graph library
Requires: %{name}-regex%{?_isa} = %{version}-%{release}
Provides:  boost169-graph = %{obsver}
Obsoletes: boost169-graph < %{obsver}

%description graph

Run-time support for the BGL graph library.  BGL interface and graph
components are generic, in the same sense as the Standard Template
Library (STL).

%package iostreams
Summary: Run-time component of boost iostreams library
Provides:  boost169-iostreams = %{obsver}
Obsoletes: boost169-iostreams < %{obsver}

%description iostreams

Run-time support for Boost.Iostreams, a framework for defining streams,
stream buffers and i/o filters.

%package locale
Summary: Run-time component of boost locale library
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Requires: %{name}-thread%{?_isa} = %{version}-%{release}
Provides:  boost169-locale = %{obsver}
Obsoletes: boost169-locale < %{obsver}

%description locale

Run-time support for Boost.Locale, a set of localization and Unicode
handling tools.

%package log
Summary: Run-time component of boost logging library
Provides:  boost169-log = %{obsver}
Obsoletes: boost169-log < %{obsver}

%description log

Boost.Log library aims to make logging significantly easier for the
application developer.  It provides a wide range of out-of-the-box
tools along with public interfaces for extending the library.

%package math
Summary: Math functions for boost TR1 library
Provides:  boost169-math = %{obsver}
Obsoletes: boost169-math < %{obsver}

%description math

Run-time support for C99 and C++ TR1 C-style Functions from the math
portion of Boost.TR1.

%if %{with python3}

%package numpy3
Summary: Run-time component of boost numpy library for Python 3
Requires: %{name}-python3%{?_isa} = %{version}-%{release}
Requires: python3-numpy
Provides:  boost169-numpy3 = %{obsver}
Obsoletes: boost169-numpy3 < %{obsver}

%description numpy3

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes,
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for the NumPy extension of the Boost Python Library for Python 3.

%endif

%package program-options
Summary:  Run-time component of boost program_options library
Provides:  boost169-program_options = %{obsver}
Obsoletes: boost169-program_options < %{obsver}

%description program-options

Run-time support of boost program options library, which allows program
developers to obtain (name, value) pairs from the user, via
conventional methods such as command-line and configuration file.

%if %{with python3}

%package python3
Summary: Run-time component of boost python library for Python 3
Provides:  boost169-python3 = %{obsver}
Provides:  boost-python = %{obsver}
Obsoletes: boost169-python3 < %{obsver}

%description python3

The Boost Python Library is a framework for interfacing Python and
C++. It allows you to quickly and seamlessly expose C++ classes,
functions and objects to Python, and vice versa, using no special
tools -- just your C++ compiler.  This package contains run-time
support for the Boost Python Library compiled for Python 3.

%package python3-devel
Summary: Shared object symbolic links for Boost.Python 3
Requires: %{name}-numpy3%{?_isa} = %{version}-%{release}
Requires: %{name}-python3%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Provides:  boost169-python3-devel = %{obsver}
Obsoletes: boost169-python3-devel < %{obsver}

%description python3-devel

Shared object symbolic links for Python 3 variant of Boost.Python.

%endif

%package random
Summary: Run-time component of boost random library
Provides:  boost169-random = %{obsver}
Obsoletes: boost169-random < %{obsver}

%description random

Run-time support for boost random library.

%package regex
Summary: Run-time component of boost regular expression library
Provides:  boost169-regex = %{obsver}
Obsoletes: boost169-regex < %{obsver}

%description regex

Run-time support for boost regular expression library.

%package serialization
Summary: Run-time component of boost serialization library
Provides:  boost169-serialization = %{obsver}
Obsoletes: boost169-serialization < %{obsver}

%description serialization

Run-time support for serialization for persistence and marshaling.

%package stacktrace
Summary: Run-time component of boost stacktrace library
Provides:  boost169-stacktrace = %{obsver}
Obsoletes: boost169-stacktrace < %{obsver}

%description stacktrace

Run-time component of the Boost stacktrace library.

%package system
Summary: Run-time component of boost system support library
Provides:  boost169-system = %{obsver}
Obsoletes: boost169-system < %{obsver}

%description system

Run-time component of Boost operating system support library, including
the diagnostics support that is part of the C++11 standard library.

%package test
Summary: Run-time component of boost test library
Provides:  boost169-test = %{obsver}
Obsoletes: boost169-test < %{obsver}

%description test

Run-time support for simple program testing, full unit testing, and for
program execution monitoring.

%package thread
Summary: Run-time component of boost thread library
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Provides:  boost169-thread = %{obsver}
Obsoletes: boost169-thread < %{obsver}

%description thread

Run-time component Boost.Thread library, which provides classes and
functions for managing multiple threads of execution, and for
synchronizing data between the threads or providing separate copies of
data specific to individual threads.

%package timer
Summary: Run-time component of boost timer library
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Provides:  boost169-timer = %{obsver}
Obsoletes: boost169-timer < %{obsver}

%description timer

"How long does my C++ code take to run?"
The Boost Timer library answers that question and does so portably,
with as little as one #include and one additional line of code.

%package type_erasure
Summary: Run-time component of boost type erasure library
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Provides:  boost169-type_erasure = %{obsver}
Obsoletes: boost169-type_erasure < %{obsver}

%description type_erasure

The Boost.TypeErasure library provides runtime polymorphism in C++
that is more flexible than that provided by the core language.

%package wave
Summary: Run-time component of boost C99/C++ preprocessing library
Requires: %{name}-chrono%{?_isa} = %{version}-%{release}
Requires: %{name}-date-time%{?_isa} = %{version}-%{release}
Requires: %{name}-filesystem%{?_isa} = %{version}-%{release}
Requires: %{name}-system%{?_isa} = %{version}-%{release}
Requires: %{name}-thread%{?_isa} = %{version}-%{release}
Provides:  boost169-wave = %{obsver}
Obsoletes: boost169-wave < %{obsver}

%description wave

Run-time support for the Boost.Wave library, a Standards conforming,
and highly configurable implementation of the mandated C99/C++
preprocessor functionality.

%package devel
Summary: The Boost C++ headers and shared development libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libicu-devel
%if %{with quadmath}
Requires: libquadmath-devel%{?_isa}
%endif
Provides:  boost169-devel = %{obsver}
Obsoletes: boost169-devel < %{obsver}

%description devel
Headers and shared object symbolic links for the Boost C++ libraries.

%package static
Summary: The Boost C++ static development libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Provides:  boost169-static = %{obsver}
Obsoletes: boost169-static < %{obsver}

%description static
Static Boost C++ libraries.

%package doc
Summary: HTML documentation for the Boost C++ libraries
%if 0%{?rhel} >= 6
BuildArch: noarch
%endif
Provides:  boost169-doc = %{obsver}
Obsoletes: boost169-doc < %{obsver}

%description doc
This package contains the documentation in the HTML format of the Boost C++
libraries. The documentation provides the same content as that on the Boost
web page (http://www.boost.org/doc/libs/%{version_enc}).

%package examples
Summary: Source examples for the Boost C++ libraries
%if 0%{?rhel} >= 6
BuildArch: noarch
%endif
Requires: %{name}-devel = %{version}-%{release}
Provides:  boost169-examples = %{obsver}
Obsoletes: boost169-examples < %{obsver}

%description examples
This package contains example source files distributed with boost.


%if %{with openmpi}

%package openmpi
Summary: Run-time component of Boost.MPI library
BuildRequires: openmpi-devel
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Provides:  boost169-openmpi = %{obsver}
Obsoletes: boost169-openmpi < %{obsver}

%description openmpi

Run-time support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-devel
Summary: Shared library symbolic links for Boost.MPI
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: %{name}-graph-openmpi%{?_isa} = %{version}-%{release}
Provides:  boost169-openmpi-devel = %{obsver}
Obsoletes: boost169-openmpi-devel < %{obsver}

%description openmpi-devel

Devel package for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%if %{with python3}

%package openmpi-python3
Summary: Python 3 run-time component of Boost.MPI library
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: %{name}-python3%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Requires: python3-openmpi%{?_isa}
Provides:  boost169-openmpi-python3 = %{obsver}
Obsoletes: boost169-openmpi-python3 < %{obsver}

%description openmpi-python3

Python 3 support for Boost.MPI-OpenMPI, a library providing a clean C++
API over the OpenMPI implementation of MPI.

%package openmpi-python3-devel
Summary: Shared library symbolic links for Boost.MPI Python 3 component
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-python3-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-openmpi-python3%{?_isa} = %{version}-%{release}
Provides:  boost169-openmpi-python3-devel = %{obsver}
Obsoletes: boost169-openmpi-python3-devel < %{obsver}

%description openmpi-python3-devel

Devel package for the Python 3 interface of Boost.MPI-OpenMPI, a library
providing a clean C++ API over the OpenMPI implementation of MPI.

%endif

%package graph-openmpi
Summary: Run-time component of parallel boost graph library
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Provides:  boost169-graph-openmpi = %{obsver}
Obsoletes: boost169-graph-openmpi < %{obsver}

%description graph-openmpi

Run-time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the Standard
Template Library (STL).  This libraries in this package use OpenMPI
back-end to do the parallel work.

%endif


%if %{with mpich}

%package mpich
Summary: Run-time component of Boost.MPI library
BuildRequires: mpich-devel
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Provides:  boost169-mpich = %{obsver}
Obsoletes: boost169-mpich < %{obsver}

%description mpich

Run-time support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-devel
Summary: Shared library symbolic links for Boost.MPI
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: %{name}-graph-mpich%{?_isa} = %{version}-%{release}
Provides:  boost169-mpich-devel = %{obsver}
Obsoletes: boost169-mpich-devel < %{obsver}

%description mpich-devel

Devel package for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%if %{with python3}

%package mpich-python3
Summary: Python 3 run-time component of Boost.MPI library
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: %{name}-python3%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Requires: python3-mpich%{?_isa}
Provides:  boost169-mpich-python3 = %{obsver}
Obsoletes: boost169-mpich-python3 < %{obsver}

%description mpich-python3

Python 3 support for Boost.MPI-MPICH, a library providing a clean C++
API over the MPICH implementation of MPI.

%package mpich-python3-devel
Summary: Shared library symbolic links for Boost.MPI Python 3 component
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-python3-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-mpich-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-mpich-python3%{?_isa} = %{version}-%{release}
Provides:  boost169-mpich-python3-devel = %{obsver}
Obsoletes: boost169-mpich-python3-devel < %{obsver}

%description mpich-python3-devel

Devel package for the Python 3 interface of Boost.MPI-MPICH, a library
providing a clean C++ API over the MPICH implementation of MPI.

%endif

%package graph-mpich
Summary: Run-time component of parallel boost graph library
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Requires: %{name}-serialization%{?_isa} = %{version}-%{release}
Provides:  boost169-graph-mpich = %{obsver}
Obsoletes: boost169-graph-mpich < %{obsver}

%description graph-mpich

Run-time support for the Parallel BGL graph library.  The interface and
graph components are generic, in the same sense as the Standard
Template Library (STL).  This libraries in this package use MPICH
back-end to do the parallel work.

%endif

%package build
Summary: Cross platform build system for C++ projects
Requires: %{name}-jam
BuildArch: noarch
Provides:  boost169-build = %{obsver}
Obsoletes: boost169-build < %{obsver}

%description build
Boost.Build is an easy way to build C++ projects, everywhere. You name
your pieces of executable and libraries and list their sources.  Boost.Build
takes care about compiling your sources with the right options,
creating static and shared libraries, making pieces of executable, and other
chores -- whether you are using GCC, MSVC, or a dozen more supported
C++ compilers -- on Windows, OSX, Linux and commercial UNIX systems.

%package doctools
Summary: Tools for working with Boost documentation
Requires: docbook-dtds
Requires: docbook-style-xsl
Provides:  boost169-doctools = %{obsver}
Obsoletes: boost169-doctools < %{obsver}

%description doctools

Tools for working with Boost documentation in BoostBook or QuickBook format.

%package jam
Summary: A low-level build tool
Provides:  boost169-jam = %{obsver}
Obsoletes: boost169-jam < %{obsver}

%description jam
Boost.Jam (BJam) is the low-level build engine tool for Boost.Build.
Historically, Boost.Jam is based on on FTJam and on Perforce Jam but has grown
a number of significant features and is now developed independently.

%prep
%setup -q -n %{toplev_dirname}
find ./boost -name '*.hpp' -perm /111 | xargs chmod a-x

%patch4 -p1
%patch5 -p1
%patch15 -p0
%patch25 -p1
%patch51 -p1
%patch61 -p1
%patch62 -p1
%patch65 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p2
%patch85 -p2
%patch86 -p1
%patch87 -p2
%patch88 -p2

%build
# Dump the versions being used into the build logs.
%if %{with python3}
PYTHON3_ABIFLAGS=$(/usr/bin/python3-config --abiflags)
: PYTHON3_VERSION=%{python3_version}
: PYTHON3_ABIFLAGS=${PYTHON3_ABIFLAGS}
%endif

# There are many strict aliasing warnings, and it's not feasible to go
# through them all at this time.
# There are also lots of noisy but harmless unused local typedef warnings.
export RPM_OPT_FLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -Wno-unused-local-typedefs -Wno-deprecated-declarations"
export RPM_LD_FLAGS

cat > ./tools/build/src/user-config.jam << "EOF"
import os ;
local RPM_OPT_FLAGS = [ os.environ RPM_OPT_FLAGS ] ;
local RPM_LD_FLAGS = [ os.environ RPM_LD_FLAGS ] ;

using gcc : : : <compileflags>$(RPM_OPT_FLAGS) <linkflags>$(RPM_LD_FLAGS) ;
%if %{with openmpi} || %{with mpich}
using mpi ;
%endif
EOF

./bootstrap.sh --with-toolset=gcc --with-icu

# N.B. When we build the following with PCH, parts of boost (math
# library in particular) end up being built second time during
# installation.  Unsure why that is, but all sub-builds need to be
# built with pch=off to avoid this.

echo ============================= build serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
%if !%{with context}
	--without-context --without-coroutine \
	--without-fiber \
%endif
	variant=release threading=multi debug-symbols=on pch=off \
	stage

# See libs/thread/build/Jamfile.v2 for where this file comes from.
if [ $(find serial -type f -name has_atomic_flag_lockfree \
		-print -quit | wc -l) -ne 0 ]; then
	DEF=D
else
	DEF=U
fi

m4 -${DEF}HAS_ATOMIC_FLAG_LOCKFREE -DVERSION=%{version} \
	%{SOURCE1} > $(basename %{SOURCE1})

%if %{with python3}

# Previously, we built python 2.x and 3.x interfaces simultaneously.
# However, this does not work once trying to build other Python components
# such as libboost_numpy.  Therefore, we build for each separately, while
# minimizing duplicate compilation as much as possible.

cat > python3-config.jam << "EOF"
import os ;
local RPM_OPT_FLAGS = [ os.environ RPM_OPT_FLAGS ] ;
local RPM_LD_FLAGS = [ os.environ RPM_LD_FLAGS ] ;

using gcc : : : <compileflags>$(RPM_OPT_FLAGS) <linkflags>$(RPM_LD_FLAGS) ;
%if %{with openmpi} || %{with mpich}
using mpi ;
%endif
EOF

cat >> python3-config.jam << EOF
using python : %{python3_version} : /usr/bin/python3 : /usr/include/python%{python3_version}${PYTHON3_ABIFLAGS} : : : : ${PYTHON3_ABIFLAGS} ;
EOF

echo ============================= build serial-py3 ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-python --build-dir=serial-py3 \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

%endif

# Build MPI parts of Boost with OpenMPI support

%if %{with openmpi} || %{with mpich}
# First, purge all modules so that user environment does not conflict
# with the build.
module purge ||:
%endif

%if %{with openmpi}
%{_openmpi_load}

%if %{with python3}
echo ============================= build $MPI_COMPILER-py3 ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER-py3 \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage
%endif

%{_openmpi_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

# Build MPI parts of Boost with MPICH support
%if %{with mpich}
%{_mpich_load}

%if %{with python3}
echo ============================= build $MPI_COMPILER-py3 ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER-py3 \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage
%endif

%{_mpich_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

echo ============================= build Boost.Build ==================
(cd tools/build
 ./bootstrap.sh --with-toolset=gcc)

%check
:


%install
cd %{_builddir}/%{toplev_dirname}

%if %{with openmpi} || %{with mpich}
# First, purge all modules so that user environment does not conflict
# with the build.
module purge ||:
%endif

%if %{with openmpi}
%{_openmpi_load}
# XXX We want to extract this from RPM flags
# b2 instruction-set=i686 etc.

%if %{with python3}
echo ============================= install $MPI_COMPILER-py3 ==================
./b2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER-py3 \
	--stagedir=${RPM_BUILD_ROOT}${MPI_HOME} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

# Move Python module to proper location for automatic loading
mkdir -p ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost
touch ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost/__init__.py
mv ${RPM_BUILD_ROOT}${MPI_HOME}/lib/mpi.so \
   ${RPM_BUILD_ROOT}%{python3_sitearch}/openmpi/boost/
%endif

# Remove generic parts of boost that were built for dependencies.
rm -f ${RPM_BUILD_ROOT}${MPI_HOME}/lib/libboost_{python,{w,}serialization}*

%{_openmpi_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

%if %{with mpich}
%{_mpich_load}

%if %{with python3}
echo ============================= install $MPI_COMPILER-py3 ==================
./b2 -q %{?_smp_mflags} \
	--user-config=./python3-config.jam \
	--with-mpi --with-graph_parallel --build-dir=$MPI_COMPILER-py3 \
	--stagedir=${RPM_BUILD_ROOT}${MPI_HOME} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} stage

# Move Python module to proper location for automatic loading
mkdir -p ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost
touch ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost/__init__.py
mv ${RPM_BUILD_ROOT}${MPI_HOME}/lib/mpi.so \
   ${RPM_BUILD_ROOT}%{python3_sitearch}/mpich/boost/
%endif

# Remove generic parts of boost that were built for dependencies.
rm -f ${RPM_BUILD_ROOT}${MPI_HOME}/lib/libboost_{python,{w,}serialization}*

%{_mpich_unload}
export PATH=/bin${PATH:+:}$PATH
%endif

echo ============================= install serial ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--without-mpi --without-graph_parallel --build-dir=serial \
%if !%{with context}
	--without-context --without-coroutine \
	--without-fiber \
%endif
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--libdir=$RPM_BUILD_ROOT%{_libdir} \
	variant=release threading=multi debug-symbols=on pch=off \
	install

# Override DSO symlink with a linker script.  See the linker script
# itself for details of why we need to do this.
[ -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so ] # Must be present
rm -f $RPM_BUILD_ROOT%{_libdir}/libboost_thread.so
install -p -m 644 $(basename %{SOURCE1}) $RPM_BUILD_ROOT%{_libdir}/

%if %{with python3}
echo ============================= install serial-py3 ==================
./b2 -d+2 -q %{?_smp_mflags} \
	--user-config=python3-config.jam \
	--with-python --build-dir=serial-py3 \
	--prefix=$RPM_BUILD_ROOT%{_prefix} \
	--libdir=$RPM_BUILD_ROOT%{_libdir} \
	variant=release threading=multi debug-symbols=on pch=off \
	python=%{python3_version} install

%endif

echo ============================= install Boost.Build ==================
(cd tools/build
 ./b2 --prefix=$RPM_BUILD_ROOT%{_prefix} install
 # Fix some permissions
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/build/alias.py
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/kernel/boost-build.jam
 chmod -x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/options/help.jam
 chmod +x $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxproc.py
 # Fix shebang using unversioned python
 sed -i '1s@^#!/usr/bin.python$@&3@' $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxproc.py
 # We don't want to distribute this
 rm -f $RPM_BUILD_ROOT%{_bindir}/b2
 # Not a real file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/src/build/project.ann.py
 # Empty file
 rm -f $RPM_BUILD_ROOT%{_datadir}/boost-build/src/tools/doxygen/windows-paths-check.hpp
 # Install the manual page
 %{__install} -p -m 644 v2/doc/bjam.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/bjam.1
)

echo ============================= install Boost.QuickBook ==================
(cd tools/quickbook
 ../build/b2 --prefix=$RPM_BUILD_ROOT%{_prefix}
 %{__install} -p -m 755 ../../dist/bin/quickbook $RPM_BUILD_ROOT%{_bindir}/
 cd ../boostbook
 find dtd -type f -name '*.dtd' | while read tobeinstalledfiles; do
   install -p -m 644 $tobeinstalledfiles -D $RPM_BUILD_ROOT%{_datadir}/boostbook/$tobeinstalledfiles
 done
 find xsl -type f | while read tobeinstalledfiles; do
   install -p -m 644 $tobeinstalledfiles -D $RPM_BUILD_ROOT%{_datadir}/boostbook/$tobeinstalledfiles
 done
)

# Install documentation files (HTML pages) within the temporary place
echo ============================= install documentation ==================
# Prepare the place to temporarily store the generated documentation
rm -rf %{boost_docdir} && %{__mkdir_p} %{boost_docdir}/html
DOCPATH=%{boost_docdir}
DOCREGEX='.*\.\(html?\|css\|png\|gif\)'

find libs doc more -type f -regex $DOCREGEX \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories

sed "s:^:$DOCPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d

cat tmp-doc-directories | while read tobeinstalleddocdir; do
    find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -regex $DOCREGEX -print0 \
    | xargs -P 0 -0 %{__install} -p -m 644 -t $DOCPATH/$tobeinstalleddocdir
done
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $DOCPATH LICENSE_1_0.txt index.htm index.html boost.png rst.css boost.css

echo ============================= install examples ==================
# Fix a few non-standard issues (DOS and/or non-UTF8 files)
sed -i -e 's/\r//g' libs/geometry/example/ml02_distance_strategy.cpp
for tmp_doc_file in flyweight/example/Jamfile.v2 \
 format/example/sample_new_features.cpp multi_index/example/Jamfile.v2 \
 multi_index/example/hashed.cpp serialization/example/demo_output.txt
do
  mv libs/${tmp_doc_file} libs/${tmp_doc_file}.iso8859
  iconv -f ISO8859-1 -t UTF8 < libs/${tmp_doc_file}.iso8859 > libs/${tmp_doc_file}
  touch -r libs/${tmp_doc_file}.iso8859 libs/${tmp_doc_file}
  rm -f libs/${tmp_doc_file}.iso8859
done

# Prepare the place to temporarily store the examples
rm -rf %{boost_examplesdir} && mkdir -p %{boost_examplesdir}/html
EXAMPLESPATH=%{boost_examplesdir}
find libs -type d -name example -exec find {} -type f \; \
    | sed -n '/\//{s,/[^/]*$,,;p}' \
    | sort -u > tmp-doc-directories
sed "s:^:$EXAMPLESPATH/:" tmp-doc-directories \
    | xargs -P 0 --no-run-if-empty %{__install} -d
rm -f tmp-doc-files-to-be-installed && touch tmp-doc-files-to-be-installed
cat tmp-doc-directories | while read tobeinstalleddocdir
do
  find $tobeinstalleddocdir -mindepth 1 -maxdepth 1 -type f \
    >> tmp-doc-files-to-be-installed
done
cat tmp-doc-files-to-be-installed | while read tobeinstalledfiles
do
  if test -s $tobeinstalledfiles
  then
    tobeinstalleddocdir=`dirname $tobeinstalledfiles`
    %{__install} -p -m 644 -t $EXAMPLESPATH/$tobeinstalleddocdir $tobeinstalledfiles
  fi
done
rm -f tmp-doc-files-to-be-installed
rm -f tmp-doc-directories
%{__install} -p -m 644 -t $EXAMPLESPATH LICENSE_1_0.txt

rm -f %{buildroot}%{_libdir}/*python27*

%post doctools
CATALOG=%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://www.boost.org/tools/boostbook/dtd" \
 "file://%{_datadir}/boostbook/dtd" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://www.boost.org/tools/boostbook/dtd" \
 "file://%{_datadir}/boostbook/dtd" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
 "http://www.boost.org/tools/boostbook/xsl" \
 "file://%{_datadir}/boostbook/xsl" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
 "http://www.boost.org/tools/boostbook/xsl" \
 "file://%{_datadir}/boostbook/xsl" $CATALOG

%postun doctools
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  CATALOG=%{_sysconfdir}/xml/catalog
  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_datadir}/boostbook/dtd" $CATALOG
  %{_bindir}/xmlcatalog --noout --del \
    "file://%{_datadir}/boostbook/xsl" $CATALOG
fi


%files
%license LICENSE_1_0.txt

%files atomic
%license LICENSE_1_0.txt
%{_libdir}/libboost_atomic.so.%{sonamever}

%files chrono
%license LICENSE_1_0.txt
%{_libdir}/libboost_chrono.so.%{sonamever}

%files container
%license LICENSE_1_0.txt
%{_libdir}/libboost_container.so.%{sonamever}

%if %{with context}

%files context
%license LICENSE_1_0.txt
%{_libdir}/libboost_context.so.%{sonamever}

%files coroutine
%license LICENSE_1_0.txt
%{_libdir}/libboost_coroutine.so.%{sonamever}

%endif

%files date-time
%license LICENSE_1_0.txt
%{_libdir}/libboost_date_time.so.%{sonamever}

%if %{with context}
%files fiber
%license LICENSE_1_0.txt
%{_libdir}/libboost_fiber.so.%{sonamever}
%endif

%files filesystem
%license LICENSE_1_0.txt
%{_libdir}/libboost_filesystem.so.%{sonamever}

%files graph
%license LICENSE_1_0.txt
%{_libdir}/libboost_graph.so.%{sonamever}

%files iostreams
%license LICENSE_1_0.txt
%{_libdir}/libboost_iostreams.so.%{sonamever}

%files locale
%license LICENSE_1_0.txt
%{_libdir}/libboost_locale.so.%{sonamever}

%files log
%license LICENSE_1_0.txt
%{_libdir}/libboost_log.so.%{sonamever}
%{_libdir}/libboost_log_setup.so.%{sonamever}

%files math
%license LICENSE_1_0.txt
%{_libdir}/libboost_math_c99.so.%{sonamever}
%{_libdir}/libboost_math_c99f.so.%{sonamever}
%{_libdir}/libboost_math_c99l.so.%{sonamever}
%{_libdir}/libboost_math_tr1.so.%{sonamever}
%{_libdir}/libboost_math_tr1f.so.%{sonamever}
%{_libdir}/libboost_math_tr1l.so.%{sonamever}

%if %{with python3}
%files numpy3
%license LICENSE_1_0.txt
%{_libdir}/libboost_numpy%{python3_version_nodots}.so.%{sonamever}
%endif

%files test
%license LICENSE_1_0.txt
%{_libdir}/libboost_prg_exec_monitor.so.%{sonamever}
%{_libdir}/libboost_unit_test_framework.so.%{sonamever}

%files program-options
%license LICENSE_1_0.txt
%{_libdir}/libboost_program_options.so.%{sonamever}

%if %{with python3}
%files python3
%license LICENSE_1_0.txt
%{_libdir}/libboost_python%{python3_version_nodots}.so.%{sonamever}

%files python3-devel
%license LICENSE_1_0.txt
%{_libdir}/libboost_numpy%{python3_version_nodots}.so
%{_libdir}/libboost_python%{python3_version_nodots}.so
%endif

%files random
%license LICENSE_1_0.txt
%{_libdir}/libboost_random.so.%{sonamever}

%files regex
%license LICENSE_1_0.txt
%{_libdir}/libboost_regex.so.%{sonamever}

%files serialization
%license LICENSE_1_0.txt
%{_libdir}/libboost_serialization.so.%{sonamever}
%{_libdir}/libboost_wserialization.so.%{sonamever}

%files stacktrace
%license LICENSE_1_0.txt
%{_libdir}/libboost_stacktrace_addr2line.so.%{sonamever}
%{_libdir}/libboost_stacktrace_basic.so.%{sonamever}
%{_libdir}/libboost_stacktrace_noop.so.%{sonamever}

%files system
%license LICENSE_1_0.txt
%{_libdir}/libboost_system.so.%{sonamever}

%files thread
%license LICENSE_1_0.txt
%{_libdir}/libboost_thread.so.%{sonamever}

%files timer
%license LICENSE_1_0.txt
%{_libdir}/libboost_timer.so.%{sonamever}

%files type_erasure
%license LICENSE_1_0.txt
%{_libdir}/libboost_type_erasure.so.%{sonamever}

%files wave
%license LICENSE_1_0.txt
%{_libdir}/libboost_wave.so.%{sonamever}

%files contract
%license LICENSE_1_0.txt
%{_libdir}/libboost_contract.so.%{sonamever}

%files doc
%doc %{boost_docdir}/*

%files examples
%doc %{boost_examplesdir}/*

%files devel
%license LICENSE_1_0.txt
%{_includedir}/%{name}
%{_libdir}/libboost_atomic.so
%{_libdir}/libboost_chrono.so
%{_libdir}/libboost_container.so
%{_libdir}/libboost_contract.so
%if %{with context}
%{_libdir}/libboost_context.so
%{_libdir}/libboost_coroutine.so
%endif
%{_libdir}/libboost_date_time.so
%if %{with context}
%{_libdir}/libboost_fiber.so
%endif
%{_libdir}/libboost_filesystem.so
%{_libdir}/libboost_graph.so
%{_libdir}/libboost_iostreams.so
%{_libdir}/libboost_locale.so
%{_libdir}/libboost_log.so
%{_libdir}/libboost_log_setup.so
%{_libdir}/libboost_math_tr1.so
%{_libdir}/libboost_math_tr1f.so
%{_libdir}/libboost_math_tr1l.so
%{_libdir}/libboost_math_c99.so
%{_libdir}/libboost_math_c99f.so
%{_libdir}/libboost_math_c99l.so
%{_libdir}/libboost_prg_exec_monitor.so
%{_libdir}/libboost_unit_test_framework.so
%{_libdir}/libboost_program_options.so
%{_libdir}/libboost_random.so
%{_libdir}/libboost_regex.so
%{_libdir}/libboost_serialization.so
%{_libdir}/libboost_wserialization.so
%{_libdir}/libboost_stacktrace_addr2line.so
%{_libdir}/libboost_stacktrace_basic.so
%{_libdir}/libboost_stacktrace_noop.so
%{_libdir}/libboost_system.so
%{_libdir}/libboost_thread.so
%{_libdir}/libboost_timer.so
%{_libdir}/libboost_type_erasure.so
%{_libdir}/libboost_wave.so

%files static
%license LICENSE_1_0.txt
%{_libdir}/*.a
%if %{with mpich}
%{_libdir}/mpich/lib/*.a
%endif
%if %{with openmpi}
%{_libdir}/openmpi/lib/*.a
%endif

# OpenMPI packages
%if %{with openmpi}

%files openmpi
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi.so.%{sonamever}

%files openmpi-devel
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi.so
%{_libdir}/openmpi/lib/libboost_graph_parallel.so

%if %{with python3}

%files openmpi-python3
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi_python%{python3_version_nodots}.so.%{sonamever}
%{python3_sitearch}/openmpi/boost/

%files openmpi-python3-devel
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_mpi_python%{python3_version_nodots}.so

%endif

%files graph-openmpi
%license LICENSE_1_0.txt
%{_libdir}/openmpi/lib/libboost_graph_parallel.so.%{sonamever}

%endif

# MPICH packages
%if %{with mpich}

%files mpich
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi.so.%{sonamever}

%files mpich-devel
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi.so
%{_libdir}/mpich/lib/libboost_graph_parallel.so

%if %{with python3}

%files mpich-python3
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi_python%{python3_version_nodots}.so.%{sonamever}
%{python3_sitearch}/mpich/boost/

%files mpich-python3-devel
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_mpi_python%{python3_version_nodots}.so

%endif

%files graph-mpich
%license LICENSE_1_0.txt
%{_libdir}/mpich/lib/libboost_graph_parallel.so.%{sonamever}

%endif

%files build
%license LICENSE_1_0.txt
%{_datadir}/%{name}-build/

%files doctools
%license LICENSE_1_0.txt
%{_bindir}/quickbook
%{_datadir}/boostbook/

%files jam
%license LICENSE_1_0.txt
%{_bindir}/bjam
%{_mandir}/man1/bjam.1*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 1.69.0-21
- Remove epoch

* Wed Jul 14 2021 Muhammad Falak Wani <mwani@microsoft.com> - 1:1.69.0-20
- Fix obsver macro to reflect correct version-release
- Add explict provides 'boost-python'

* Fri Jan 08 2021 Ruying Chen <v-ruyche@microsoft.com> - 1:1.69.0-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Set epoch to 1
- Remove isa from libicu.
- Remove python2 shared objects

* Thu May 14 2020 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.69.0-18
- Obsoletes all sub-packages of boost169 (on F32) (#1835079)

* Tue May 12 2020 Avi Kivity <avi@scylladb.com> - 1.69.0-17
- Add patch for C++20 compatibility in Boost.Signals2 (#1834764)

* Mon May 11 2020 Jonathan Wakely <jwakely@redhat.com> - 1.69.0-16
- Add patch for C++20 compatibility in Boost.Test (#1832639)

* Mon Mar 30 2020 Jonathan Wakely <jwakely@redhat.com> - 1.69.0-15
- Patch Boost.Format for C++20 compatibility with GCC 10 (#1818723)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.69.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.69.0-13
- Removed the Python2 sub-packages

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 1.69.0-12
- Rebuild for ICU 65

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.69.0-11
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 1.69.0-10
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.69.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Jonathan Wakely <jwakely@redhat.com> - 1.69.0-8
- Fix Obsoletes tag to remove _isa (#1706079)

* Tue May 07 2019 Jonathan Wakely <jwakely@redhat.com> - 1.69.0-7
- Make main package obsolete old boost-signals subpackage (#1706079)

* Thu Feb 14 2019 Jonathan Wakely <jwakely@redhat.com> - 1.69.0-6
- Add patch for out-of-bounds vector access in Boost.MPI

* Thu Feb 14 2019 Orion Poplawski <orion@nwra.com> - 1.69.0-5
- Rebuild for openmpi 3.1.3

* Tue Feb 12 2019 Jonathan Wakely <jwakely@redhat.com> - 1.69.0-4
- Patch Boost.Random to fix warning (#1673669)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.69.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 1.69.0-2
- Rebuild for ICU 63

* Sat Dec 15 2018 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.69.0-1
- Rebase to 1.69.0
- Dropped library: Boost.Signals (now replaced by header-only Boost.Signals2)

* Sat Dec 01 2018 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.68.0-1
- Rebase to 1.68.0
- New library: Boost.Contract
- The Python-related shared libraries now carry the full Python version,
  eg _python27.so and _python37.so
- Drop patches:
    deleted: boost-1.66.0-address-model.patch
    deleted: boost-1.66.0-compute.patch
    deleted: boost-1.66.0-numpy3.patch
    deleted: boost-1.66.0-python37.patch
    deleted: boost-1.66.0-spirit-abs-overflow.patch

* Thu Sep 27 2018 Owen Taylor <otaylor@redhat.com> - 1.66.0-15
- Disable openmpi and mpich for Flatpak-bundled builds

* Thu Aug 23 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-14
- Fix permissions and python shebang of Boost.Build files

* Wed Jul 18 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-14
- Patch numpy for Python 3 (#1596468)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.66.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 1.66.0-12
- Rebuild for ICU 62

* Tue Jun 19 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-11
- Add patch to fix build with Python 3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.66.0-11
- Rebuilt for Python 3.7

* Mon Jun 04 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-10
- Add patch for Boost.Compute (#1585515)

* Tue May 01 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-9
- Fix Provides: and Obsoletes: tags for renamed python2 subpackages
- Remove old Provides: and Obsoletes: tags for odeint packages
- Remove old Provides: and Obsoletes: tags for mpich2 packages
- Remove old Provides: and Obsoletes: tags for boost-devel-static
- Make Requires: for boost-container unconditional

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 1.66.0-8
- Rebuild for ICU 61.1

* Fri Apr 27 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-7
- Remove Requires: boost-openmpi-python from boost-openmpi-devel

* Thu Apr 26 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-6
- Remove main package dependency on boost-python and boost-numpy (#1569483)
- Rename all subpackages using python2 from boost-xxx to boost-xxx2.
- Split new subpackage boost-python2-devel out of boost-devel.
- Split new subpackage boost-openmpi-python2-devel out of boost-openmpi-devel.
- Split new subpackage boost-mpich-python2-devel out of boost-mpich-devel.
- Enable conditional build for python2 packages.
- Drop ver.py source file and use python2_version and python3_version macros.
- Use shell variable for Python 3 ABI flags instead of global macro.

* Tue Feb 27 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-5
- Ensure boost metapackage installs boost-container and boost-stacktrace.

* Fri Feb 23 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-4
- Add patch to fix integer overflow in Boost.Spirit absolute_value (#1545092)

* Thu Feb 15 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-3
- Remove unnecessary Group tags and post/postun scriptlets running ldconfig

* Wed Feb 07 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-2
- Add RPM_OPT_FLAGS and RPM_LD_FLAGS to build flags for bjam (#1541035).

* Mon Feb 05 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-1
- Add RPM_LD_FLAGS to Jamfile and patch build.sh to use RPM flags (#1541035).

* Fri Jan 19 2018 Jonathan Wakely <jwakely@redhat.com> - 1.66.0-0.1
- Rebase to 1.66.0
  - Do not pass --without-coroutine2 to b2
  - Drop patches:
    boost-1.63.0-dual-python-build-v2.patch
    boost-1.64.0-mpi-get_data.patch
    boost-1.64.0-serialization-make_array.patch
    boost-1.64.0-icl-ttp-matching.patch
    boost-1.64.0-icl-undefined-shift.patch

* Wed Jan 17 2018 Jonathan Wakely <jwakely@redhat.com> - 1.64.0-7
- Restore "Provides: boost-python" for boost-python2

* Thu Dec 07 2017 Jonathan Wakely <jwakely@redhat.com> - 1.64.0-6
- Patch to fix #1516837

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 1.64.0-5
- Rebuild for ICU 60.1

* Mon Sep 25 2017 Jonathan Wakely <jwakely@redhat.com> - 1.64.0-4
- Fix some rpmlint issues
- Remove Requires for libquadmath (explicit-lib-dependency)
- Remove executable bits on header files (spurious-executable-perm)
- Adjust boost.wave %%description (spelling-error)

* Wed Sep 13 2017 Jonathan Wakely <jwakely@redhat.com> - 1.64.0-3
- Rename python2-boost to boost-python2

* Tue Sep 12 2017 Jonathan Wakely <jwakely@redhat.com> - 1.64.0-2
- Patch to fix #1485641

* Wed Sep 06 2017 Jonathan Wakely <jwakely@redhat.com> - 1.64.0-1
- Fix descriptions

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.64.0-0.8
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.64.0-0.7
- Python 2 binary package renamed to python2-boost
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.64.0-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.64.0-0.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Björn Esser <besser82@fedoraproject.org> - 1.64.0-0.4
- Drop obsolete patch for mpi serialization make_array
- Purge unused patches from repo

* Mon Jul 24 2017 Björn Esser <besser82@fedoraproject.org> - 1.64.0-0.3
- Add patch to fix make_array in serialization

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 1.64.0-0.2
- Rebuild for std::__once_functor linking issue on ppc64le (#1470692)

* Sat Jul 01 2017 Jonathan Wakely <jwakely@redhat.com> - 1.64.0-0.1
- Rebase to 1.64.0

* Sat Jul 01 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.63.0-9
- Add numpy and numpy3 packages (#1451982)
- Fix location of openmpi-python and mpich-python modules
- Add openmpi-python3 and mpich-python3 packages
- Add missing ldconfig post/postun for python3 package

* Sat Jul 01 2017 Jonathan Wakely <jwakely@redhat.com> - 1.63.0-8
- Remove patch for boost::function strict aliasing problem (#1422456)

* Tue Apr 25 2017 Jonathan Wakely <jwakely@redhat.com> - 1.63.0-7
- Rebuild for rpm-mpi-hooks fix (#1435690)

* Wed Apr 05 2017 Jonathan Wakely <jwakely@redhat.com> - 1.63.0-6
- Patch boost::function to fix strict aliasing problem (#1422456)
- Per packaging guidelines don't clean buildroot in %%install and %%clean.

* Sun Mar 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 1.63.0-5
- Enable OpenMPI/mpich on ppc64le and s390x now they have support

* Thu Feb 16 2017 Jonathan Wakely <jwakely@redhat.com> - 1.63.0-4
- Revert Boost.Build change that breaks building for two Python versions.

* Thu Feb 09 2017 Jonathan Wakely <jwakely@redhat.com> - 1.63.0-3
- Add --without-fiber when Boost.Context is not supported.

* Fri Jan 27 2017 Jonathan Wakely <jwakely@redhat.com> - 1.63.0-2
- Use correct sources for release, not a snapshot.
- Add -Wno-deprecated-declarations to build flags.

* Thu Jan 26 2017 Jonathan Wakely <jwakely@redhat.com> - 1.63.0-1
- Rebase to 1.63.0 (#1401431)

* Tue Dec 20 2016 Miro Hrončok <mhroncok@redhat.com> - 1.60.0-12
- Rebuild for Python 3.6

* Fri Dec 09 2016 Jonathan Wakely <jwakely@redhat.com> - 1.60.0-11
- Add patch for Boost.Asio to fix allocator usage (#1403165)

* Fri Oct 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1.60.0-10
- Rebuild for openmpi 2.0

* Mon Aug 01 2016 Jonathan Wakely <jwakely@redhat.com> - 1.60.0-9
- Add patch for Boost.Python to fix pointer registration (#1358725)

* Tue Jun 28 2016 Jonathan Wakely <jwakely@redhat.com> - 1.60.0-8
- Add patch for Boost.Multiprecision (#1349638)

* Mon Jun 06 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 1.60.0-7
- Drop rpath (#1318383)

* Tue May 03 2016 Jonathan Wakely <jwakely@redhat.com> - 1.60.0-6
- Rebuilt for GCC 6.1 (#1331983)

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 1.60.0-5
- rebuild for ICU 57.1

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.60.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Jonathan Wakely <jwakely@redhat.com> 1.60.0-3
- Remove redundant %%defattr statements

* Thu Jan 14 2016 Jonathan Wakely <jwakely@redhat.com> 1.60.0-2
- Make Requires: libquadmath-devel conditional

* Wed Jan 13 2016 Jonathan Wakely <jwakely@redhat.com> 1.60.0-1
- Rebase to 1.60.0

* Fri Dec 11 2015 Dan Horák <dan[at]danny.cz> - 1.59.0-10
- rebuilt for s390

* Tue Nov 24 2015 Jonathan Wakely <jwakely@redhat.com> 1.59.0-9
- do not use arch-specific BuildRequires (#1268267)

* Fri Nov 13 2015 Dan Horák <dan[at]danny.cz> - 1.59.0-8
- disable also the coroutine2 module when context is not available

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.59.0-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 1.59.0-6
- rebuild for ICU 56.1

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 1.59.0-5
- Rebuild for openmpi 1.10.0

* Mon Sep 14 2015 Jonathan Wakely <jwakely@redhat.com> 1.59.0-4
- Patch Boost.Test to fix #1262444

* Wed Sep 02 2015 Jonathan Wakely <jwakely@redhat.com> - 1.59.0-3
- Rebuilt for Boost 1.59

* Wed Sep 02 2015 Jonathan Wakely <jwakely@redhat.com> 1.59.0-2
- Add patch for Boost.Python bug.

* Wed Aug 26 2015 Jonathan Wakely <jwakely@redhat.com> 1.59.0-1
- Rebase to 1.59.0

* Tue Aug 25 2015 Jonathan Wakely <jwakely@redhat.com> 1.58.0-9
- Add boost-doctools subpackage (#1244268).

* Mon Aug 24 2015 Jonathan Wakely <jwakely@redhat.com> 1.58.0-8
- Use %%license for license files.

* Fri Aug 21 2015 Jonathan Wakely <jwakely@redhat.com> 1.58.0-7
- Bump release to match F23 update.

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> - 1.58.0-6
- Rebuild for RPM MPI Requires Provides Change

* Wed Aug 05 2015 Jonathan Wakely <jwakely@redhat.com> 1.58.0-5
- Patch incorrect placement of BOOST_UBLAS_INLINE macros.

* Tue Aug 04 2015 Jonathan Wakely <jwakely@redhat.com> 1.58.0-4
- Patch to prevent address model being set by Boost.Build.

* Mon Jul 27 2015 Jonathan Wakely <jwakely@redhat.com> 1.58.0-3
- Patch for missing include (boost-1.58.0-variant-includes.patch).

* Thu Jul 23 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.58.0-2
- Re-enable boost::context on AArch64.

* Fri Jul 17 2015 Jonathan Wakely <jwakely@redhat.com> - 1.58.0-1
- Rebase to 1.58.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.57.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 13 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.57.0-7
- Add AArch64 support for boost::context
  - Numbered patches are cherry-picked from upstream repository.
  - partial-revert-of-0002 removes some build definitions which are defined
    in coroutine/
  - last patch changes ABI names - taken from boost ML

* Sun Apr 12 2015 David Tardon <dtardon@redhat.com> - 1.57.0-6
- rebuild for yet another C++ ABI break

* Mon Mar 16 2015 Than Ngo <than@redhat.com> 1.57.0-5
- rebuild against new gcc

* Wed Feb 18 2015 Petr Machata <pmachata@redhat.com> - 1.57.0-4
- Fix template <class T> class boost::rv, which for union T's inherits
  off them.  (boost-1.57.0-move-is_class.patch)

* Mon Feb  9 2015 Petr Machata <pmachata@redhat.com> - 1.57.0-3
- Honor RPM_OPT_FLAGS (boost-1.57.0-build-optflags.patch)
  - And don't pass -ftemplate-depth at all.  The intention there was
    to increase the default instantiation depth above the default 17,
    but GCC defaults to 900 anyway, and requesting 128 actually lowers
    the limit.  (The same patch.)

- Add a patch to fix incorrect operator< in Boost.UUID
  (boost-1.57.0-uuid-comparison.patch)

* Thu Jan 29 2015 Petr Machata <pmachata@redhat.com> - 1.57.0-2
- Change Provides: and Obosoletes: back to not use %%{?_isa}
- Enable Boost.Context on PowerPC, it should now be supported
- Add a patch for Boost.Signal2 to include weak_ptr where it uses it
  (boost-1.57.0-signals2-weak_ptr.patch)

* Tue Jan 20 2015 Petr Machata <pmachata@redhat.com> - 1.57.0-1
- Rebase to 1.57.0
  - Drop patches:
    boost-1.54.0-bind-static_assert.patch
    boost-1.54.0-concept-unused_typedef.patch
    boost-1.54.0-static_warning-unused_typedef.patch
    boost-1.54.0-tuple-unused_typedef.patch
    boost-1.54.0-random-unused_typedef.patch
    boost-1.54.0-date_time-unused_typedef.patch
    boost-1.54.0-date_time-unused_typedef-2.patch
    boost-1.54.0-spirit-unused_typedef.patch
    boost-1.54.0-numeric-unused_typedef.patch
    boost-1.54.0-property_tree-unused_typedef.patch
    boost-1.55.0-program_options-class_attribute.patch
    boost-1.55.0-archive-init_order.patch
    boost-1.55.0-xpressive-unused_typedefs.patch
    boost-1.55.0-spirit-unused_typedefs.patch
    boost-1.54.0-smart_ptr-shared_ptr_at.patch
    boost-1.55.0-atomic-int128_1.patch
    boost-1.55.0-atomic-int128_2.patch

  - Rebase patches:
    boost-1.54.0-mpl-print.patch -> boost-1.57.0-mpl-print.patch
    boost-1.54.0-spirit-unused_typedef-2.patch -> boost-1.57.0-spirit-unused_typedef.patch
    boost-1.54.0-pool-test_linking.patch -> boost-1.57.0-pool-test_linking.patch

  - Add new subpackages boost-container

* Fri Jan  9 2015 Petr Machata <pmachata@redhat.com> - 1.55.0-8
- Build libboost_python and libboost_python3 such that they depend on
  their respective libpython's.
  (boost-1.55.0-python-libpython_dep.patch,
  boost-1.55.0-python-abi_letters.patch)
- Fix Boost.Python test suite so that PyImport_AppendInittab is called
  before PyInitialize, which broke the test suite with Python 3.
  (boost-1.55.0-python-test-PyImport_AppendInittab.patch)

* Thu Jan  8 2015 Petr Machata <pmachata@redhat.com> - 1.55.0-7
- Change Requires: and other package references to use %%{?_isa}, so
  that dependencies are arch-aware.
- Drop two obsolete conditions testing Fedora >= 10 (but leave RHEL >=
  6 for potential EPEL deployment).

* Fri Jan  2 2015 Petr Machata <pmachata@redhat.com> - 1.55.0-6
- Boost.Atomic: Fixed incorrect initialization of 128-bit values, when
  no native support for 128-bit integers is available.
  (boost-1.55.0-atomic-int128_1.patch,
  boost-1.55.0-atomic-int128_2.patch)

* Wed Nov 12 2014 Petr Machata <pmachata@redhat.com> - 1.55.0-5
- Fix boost::shared_ptr<T>::operator[], which was ill-formed for
  non-array T's.  (boost-1.54.0-smart_ptr-shared_ptr_at.patch)

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 1.55.0-4
- rebuild for ICU 53.1

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.55.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Petr Machata <pmachata@redhat.com> - 1.55.0-1
- Add a new sub-package boost-coroutine
- Annotate or drop some unused typedefs
  (boost-1.55.0-python-unused_typedefs.patch,
  boost-1.55.0-spirit-unused_typedefs.patch,
  boost-1.55.0-xpressive-unused_typedefs.patch)
- Add a patch for wrong initialization order
  (boost-1.55.0-archive-init_order.patch)
- Add a patch for misplaced attribute at class declaration
  (boost-1.55.0-program_options-class_attribute.patch)
- Drop 001-coroutine.patch, 002-date-time.patch, 003-log.patch,
  boost-1.53.0-attribute.patch,
  boost-1.54.0-__GLIBC_HAVE_LONG_LONG.patch,
  boost-1.54.0-algorithm-unused_typedef.patch,
  boost-1.54.0-context-execstack.patch,
  boost-1.54.0-graph-unused_typedef.patch,
  boost-1.54.0-interprocess-atomic_cas32-ppc.patch,
  boost-1.54.0-lexical_cast-int128.patch,
  boost-1.54.0-math-unused_typedef-2.patch,
  boost-1.54.0-math-unused_typedef.patch,
  boost-1.54.0-mpi-unused_typedef.patch,
  boost-1.54.0-multiprecision-unused_typedef.patch,
  boost-1.54.0-thread-cond_variable_shadow.patch,
  boost-1.54.0-thread-link_atomic.patch,
  boost-1.54.0-unordered-unused_typedef.patch,
  boost-1.54.0-xpressive-unused_typedef.patch,

* Tue Mar 18 2014 Petr Machata <pmachata@redhat.com> - 1.54.0-14
- Fix a noexecstack patch for ARM, enable Boost.Context on ARM.
  (boost-1.54.0-context-execstack.patch)

* Tue Mar 18 2014 Björn Esser <bjoern.esser@gmail.com> - 1.54.0-13
- rebuilt for mpich-3.1

* Mon Mar 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.54.0-12
- Enable MPICH and OpenMPI support on aarch64

* Wed Feb 12 2014 Petr Machata <pmachata@redhat.com> - 1.54.0-11
- Rebuild for ICU soname bump.

* Thu Jan  9 2014 Petr Machata <pmachata@redhat.com> - 1.54.0-10
- Add ppc64le to the list of arches that OpenMPI and MPICH don't
  support.

* Wed Dec 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.54.0-9
- Enable MPICH and OpenMPI support on ARM as it's long had them both

* Fri Dec 13 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-8
- Add aarch64 into the list of arches that OpenMPI does not support.

* Sun Dec  1 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-7
- Fix shameful blunders in implementation of the previous fix: don't
  hard-code path to has_atomic_flag_lockfree binary; use m4 instead of
  cpp, cpp in F19+ prefixes output with a bunch of comments.

* Wed Nov 27 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-6
- Add libboost_atomic.so.* to the libboost_thread.so linker script on
  architectures that need it.

* Thu Aug 29 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-5
- Fix atomic_cas32 (thanks Jaroslav Škarvada for figuring out where
  the problem is) (boost-1.54.0-interprocess-atomic_cas32-ppc.patch)

* Fri Aug 23 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-4
- Fix compilation of Boost.Pool test cases
  (boost-1.54.0-pool-test_linking.patch)
- Fix -Wshadow warnings in Boost.Pool
  (boost-1.54.0-pool-max_chunks_shadow.patch)
- -Wshadow warnings in Boost.Thread
  (boost-1.54.0-thread-cond_variable_shadow.patch)
- libboost_thread.so.* lacks DT_NEEDED on libboost_atomic.so.* on
  s390.  (boost-1.54.0-thread-link_atomic.patch)

* Mon Aug 19 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-3
- Bump odeint obsoletes and provides a notch to cover a build that
  sneaked into rawhide (bug 892850).

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-2
- Fix detection of availability of 128-bit integers in
  Boost.LexicalCast (boost-1.54.0-lexical_cast-int128.patch)

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 1.54.0-1
- Rebase to 1.54.0
  - Add new sub-package boost-log
  - Boost.Coroutine is only enabled if Boost.Context is
  - Drop boost-1.53-context.patch (interesting parts now upstream)
  - Drop boost-1.50.0-foreach.patch (#define foreach now discouraged)
  - Drop several unused typedef patches that are now upstream.
    (boost-1.53.0-static_assert-unused_typedef.patch,
    boost-1.53.0-fpclassify-unused_typedef.patch,
    boost-1.53.0-math-unused_typedef-3.patch,
    boost-1.53.0-lexical_cast-unused_typedef.patch,
    boost-1.53.0-regex-unused_typedef.patch,
    boost-1.53.0-thread-unused_typedef.patch)
  - Add release notes patches (001-coroutine.patch,
    002-date-time.patch, 003-log.patch)
  - Add additional unused typedefs in Boost.Math
    (boost-1.54.0-math-unused_typedef-2.patch)
- Drop symlinks from libboost_{thread,locale,atomic}.so -> *-mt.so,
  which we don't need anymore, as we ditched the tagged layout.

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-12
- There's no physical difference between single-threaded and
  multi-threaded builds, except some libraries are only built in
  multi-threaded mode.  So build everything in multi-threaded mode,
  and ditch tagged layout, which we don't need anymore.
  https://bugzilla.redhat.com/show_bug.cgi?id=971956

* Fri Jul 26 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-11
- Add Obsoletes for odeint (bug 892850)

* Thu Jul 25 2013 Deji Akingunola <dakingun@gmail.com> - 1.53.0-10
- Add Provides and Obsoletes for the mpich2->mpich renames

* Wed Jul 24 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-9
- Add explicit dependencies between some of the boost sub-packages

* Tue Jul 23 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-8
- MPICH2 became MPICH -- rename subpackages, dependencies and
  conditionals.
- Install supporting files (images etc.) for documentation
  (courtesy Marcel Metz, bug 985593)
- Add many patches for silencing unused local typedef warnings
  (boost-1.53.0-static_assert-unused_typedef.patch,
  boost-1.54.0-bind-static_assert.patch,
  boost-1.54.0-concept-unused_typedef.patch,
  boost-1.54.0-static_warning-unused_typedef.patch,
  boost-1.54.0-math-unused_typedef.patch,
  boost-1.54.0-math-unused_typedef-2.patch,
  boost-1.53.0-fpclassify-unused_typedef.patch,
  boost-1.54.0-math-unused_typedef-3.patch,
  boost-1.54.0-tuple-unused_typedef.patch,
  boost-1.54.0-random-unused_typedef.patch,
  boost-1.54.0-date_time-unused_typedef.patch,
  boost-1.54.0-date_time-unused_typedef-2.patch,
  boost-1.54.0-spirit-unused_typedef.patch,
  boost-1.54.0-spirit-unused_typedef-2.patch,
  boost-1.54.0-numeric-unused_typedef.patch,
  boost-1.54.0-multiprecision-unused_typedef.patch,
  boost-1.53.0-lexical_cast-unused_typedef.patch,
  boost-1.53.0-regex-unused_typedef.patch,
  boost-1.53.0-thread-unused_typedef.patch,
  boost-1.54.0-unordered-unused_typedef.patch,
  boost-1.54.0-algorithm-unused_typedef.patch,
  boost-1.53.0-graph-unused_typedef.patch,
  boost-1.54.0-locale-unused_typedef.patch,
  boost-1.54.0-property_tree-unused_typedef.patch,
  boost-1.54.0-xpressive-unused_typedef.patch,
  boost-1.54.0-mpi-unused_typedef.patch,
  boost-1.54.0-python-unused_typedef.patch)
- Add a patch to turn off execstack in Boost.Context
  (boost-1.54.0-context-execstack.patch)
- Fix boost::mpl::print on GCC (boost-1.54.0-mpl-print.patch)
- Add symlinks for /usr/lib/libboost_{thread,locale}.so -> *-mt.so

* Wed Jun 26 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-7
- Fix detection of availability of {,u}int64_t in glibc headers.
  (boost-1.53.0-__GLIBC_HAVE_LONG_LONG.patch)

* Wed Mar  6 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-6
- libboost_context.so must be guarded by conditional in the expanded
  filelist at boost-devel.

* Tue Mar  5 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-5
- Split off Python 3 DSO symlink to a separate subpackage
  boost-python3-devel.  This makes it possible to install
  boost-devel separately, without Python 3 support.
- Build with -fno-strict-aliasing

* Wed Feb 27 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-4
- Make Boost.Context support conditional

* Mon Feb 11 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-3
- Fix Boost.Context on ppc64
- Future-proof the linker script boost_thread-mt.so

* Sun Feb 10 2013 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.53.0-2
- Fixed the libboost_thread-mt.so script (which wrongly referred to Boost-1.50)

* Fri Feb  8 2013 Petr Machata <pmachata@redhat.com> - 1.53.0-1
- Upstream 1.53.0 beta1
  - Drop boost-1.50.0-signals-erase.patch
  - Port boost-1.50.0-attribute.patch
  - Drop boost-1.50.0-polygon.patch
  - New sub-packages boost-atomic and boost-context

* Sat Jan 26 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.50.0-7
- Rebuild for icu soname bump

* Sat Nov 03 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.50.0-6
- Rebuild for the new MPICH2 (and libmpich2 soname bump)

* Thu Aug 16 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-5
- Update %%description to reflect current state of C++
  standardization.  Courtesy of Jonathan Wakely.  (#837813)

* Wed Aug 15 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-4
- Override boost_thread-mt.so with a linker script that brings in
  Boost.System DSO as well.

* Wed Aug  8 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-3
- boost-python3 shouldn't be under the overall boost umbrella

* Tue Aug  7 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-2
- Enable Python 3 builds.  This is still disabled in Boost MPI, which
  does not seem to support Python 3

* Thu Jul 26 2012 Petr Machata <pmachata@redhat.com> - 1.50.0-1
- Upstream 1.50
  - boost-cmake-soname.patch drop, upstream handles soname well, and
    we haven't been doing manual numbering for several years now
  - boost-1.48.0-cmakeify-full.patch drop, not necessary for bjam
  - Rebase many patches, port others, courtesy of Denis Arnaud:
    - boost-1.48.0-exceptions.patch drop
    - boost-1.48.0-lexical_cast-incomplete.patch drop
    - boost-1.48.0-gcc47-pthreads.patch drop
    - boost-1.48.0-long-double.patch drop
    - boost-1.48.0-xtime.patch drop
    - boost-1.48.0-locale.patch drop
    - boost-1.48.0-signals-erase.patch port
    - boost-1.48.0-fix-non-utf8-files.patch port
    - boost-1.48.0-foreach.patch port
    - boost-1.48.0-attribute.patch port
    - boost-1.48.0-long-double-1.patch port
    - boost-1.48.0-polygon.patch port
    - boost-1.48.0-pool.patch port

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-16
- Build Boost.Locale backends
- Resolves: #832265

* Wed Jun  6 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-15
- In Boost.Pool, be careful not to overflow allocated chunk size.
- Resolves: #828857

* Thu May 24 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-14
- Don't attempt to install Python 3 portions of boost when given
  --without python3
- glibc newly defines a macro TIME_UTC, which collides with
  boost::TIME_UTC.  We can't avoid expanding that macro, but the value
  happens to be the same as that of boost::TIME_UTC.  So drop enum
  xtime_clock_types.  Update boost to use macro TIME_UTC instead of
  the scoped enum value.  External clients will have to do the same.
- Resolves: #824810
- BR on hwloc-devel shouldn't be required anymore (see #814798)

* Wed May  2 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-13
- Support building boost-python against Python 3
- Resolves: #807780

* Sun Apr 22 2012 Robert Scheck <robert@fedoraproject.org> - 1.48.0-12
- Included -math subpackage into umbrella package
- Added missing /sbin/ldconfig for -math subpackage

* Fri Apr 20 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-11
- Add hwloc-devel BR to work around a probable bug in openmpi-devel
  which fails to pull it in

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48.0-10
- Rebuilt for c++ ABI breakage

* Wed Jan 25 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-9
- Only build the long double math libraries on arches that support
  long double.
- ARM was considered unsupporting, because libc defines
  __NO_LONG_DOUBLE_MATH.  Ignore this setting, ARM has perfectly
  working long double that just happens to be only as long as double.
- Resolves: #783660
- Add a missing sort adaptor include to boost polygon
- Resolves: #784654

* Mon Jan 16 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-8
- Add underscores around several uses of __attribute__((X)) to prevent
  interactions with user-defined macro X
- Resolves: #781859

* Sat Jan 14 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-7
- Added source source files for mingw cross-compilation of Boost.Locale.
- Resolves: #781751

* Sat Jan  7 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-6
- Added the Boost.Timer sub-package. Resolves: #772397

* Wed Jan  4 2012 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-5
- Integrated into "upstream" (CMake-ified Boost) the Boost.TR1/Math patch.

* Wed Jan  4 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-4
- Build math portion of Boost.TR1, package DSOs in boost-math.
- Resolves: #771370

* Tue Jan  3 2012 Petr Machata <pmachata@redhat.com> - 1.48.0-3
- Add an upstream patch for BOOST_ENABLE_THREADS

* Tue Nov 29 2011 Petr Machata <pmachata@redhat.com> - 1.48.0-2
- Add an upstream patch for BOOST_FOREACH declaration issue #756005
- Add a proposed patch for error in boost lexical_cast #757385

* Sat Nov 19 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.48.0-1
- Upgrade to Boost-1.48.0, adding two new header-only components
  (Container and Move) and a new library (Locale).
- Resolves: #754865
- Added a patch with a manual page for the bjam executable.
- Added a patch to fix the non-UTF8-encoded example source file.
- Re-worked a little bit the example section, so as to fix the
  DOS-formatted and the ISO-8859-encoded files.

* Thu Nov  3 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-7
- Use <boost/tr1/tuple> instead of C++11 header <tuple> in boost math.
- Resolves: #751210

* Fri Sep  9 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-6
- Rebuild for libicu soname bump
- Hack /bin back to PATH after MPI module unload
- Resolves: #736890

* Tue Aug 30 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-4
- Drop BR bzip2-libs, which is brought it via bzip2-devel
- Source->Source0
- Drop unnecessary BuildRoot tag
- Update License tag to include all licenses that are found in
  sources.  Python license is at the main package, not to the python
  sub-package, because python22_fixed.h is in -devel.
  - Related: #673839
- Resolves: #225622

* Tue Jul 26 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-3
- Package examples
- Resolves: #722844

* Fri Jul 22 2011 Petr Machata <pmachata@redhat.com> - 1.47.0-2
- Convert two throws in boost/numeric/conversion to
  boost::throw_exception to allow compilation with -fno-exception
- Resolves: #724015

* Thu Jul 14 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.47.0-1
- Upgrade to Boost-1.47.0, adding three new header-only components
  (Geometry, Phoenix, Ratio) and a new library (Chrono).

* Sat Jun 18 2011 Peter Robinson <pbrobinson@gmail.com> - 1.46.1-4
- Fix compile on ARM platforms

* Mon Apr  4 2011 Petr Machata <pmachata@redhat.com> - 1.46.1-3
- Yet another way to pass -DBOOST_LIB_INSTALL_DIR to cmake.  Passing
  via CMAKE_CXX_FLAGS for some reason breaks when rpm re-quotes the
  expression as a result of %%{optflags} expansion.
- Related: #667294

* Wed Mar 30 2011 Deji Akingunola <dakingun@gmail.com> - 1.46.1-2
- Rebuild for mpich2 soname bump

* Sun Mar 13 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.46.1-1
- Merged the latest changes from the bug-fix release of Boost-1.46

* Mon Mar 07 2011 Caolán McNamara <caolanm@redhat.com> - 1.46.0-0.5
- rebuild for icu 4.6

* Thu Feb 24 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.46.0-0.4
- Merged the latest changes from the now final release of Boost-1.46

* Tue Feb  8 2011 Petr Machata <pmachata@redhat.com> - 1.46.0-0.3.beta1
- spirit.patch: Fix a problem in using boost::spirit with utf-8
  strings.  Thanks to Hicham HAOUARI for digging up the fix.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46.0-0.2.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Petr Machata <pmachata@redhat.com> - 1.46.0-0.1.beta1
- Package 1.46.0-beta1
- Reintroduce the soname patch
- unordered-cctor.patch: Add copy constructors and assignment
  operators when using rvalue references
- signals-erase.patch: Pass const_iterator to map::erase to avoid
  ambigous overload vs. templatized value_type ctor
- Related: #656410

* Mon Jan 10 2011 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-7
- Integrated Petr's work to fix missing Boost.Filesystem V3 issue
- Resolves: #667740

* Thu Jan  6 2011 Petr Machata <pmachata@redhat.com> - 1.44.0-6
- Don't override CXXFLAGS with -DBOOST_IOSTREAMS_USE_DEPRECATED
- Resolves: #667294

* Mon Jan  3 2011 Petr Machata <pmachata@redhat.com> - 1.44.0-5
- Add boost-random DSOs
- Resolves: #665679

* Wed Dec  8 2010 Petr Machata <pmachata@redhat.com> - 1.44.0-4
- Build with support for iostreams deprecated functions
- Resolves: #654480

* Fri Dec  3 2010 Tom "spot" Callaway <spot@fedoraproject.org> - 1.44.0-3
- also package build-system.jam in boost-build

* Tue Nov 30 2010 Tom "spot" Callaway <spot@fedoraproject.org> - 1.44.0-2
- add boost-build, boost-jam subpackages

* Sat Oct 23 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-1.1
- Rebuild.

* Sat Aug 21 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-1
- Split the CMake-buildable tar-ball into pristine upstream tar-ball
  and CMake framework patch

* Mon Aug 16 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-0.6
- Merged the latest changes from the now final release of Boost-1.44

* Fri Aug  6 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-0.5
- Patched header file in boost/random/detail. Resolves: #621631

* Sat Jul 31 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-0.4
- Added missing header files in boost/random/detail. Resolves: #619869

* Tue Jul 27 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.44.0-0.3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 27 2010 Benjamin Kosnik <bkoz@redhat.com> - 1.44.0-0.2
- Rebuild.

* Fri Jul 23 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.44.0-0.1
- Upstream update: Boost-1.44 with CMake enabled
- Resolves: #607615

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.41.0-13
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun  4 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-12
- Turn on mpich2 on s390.  Add arm to the list of arches that openmpi
  does not support.

* Fri Jun  4 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-12
- Don't distribute cmake support files.
- Related: #597020

* Wed Jun  2 2010 Dan Horák <dan[at]danny.cz> - 1.41.0-11
- don't build with mpich2/openmpi on s390/s390x

* Mon May 10 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-10
- Add an upstream patch that fixes computation of CRC in zlib streams.
- Resolves: #590205

* Wed May 05 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.41.0-9
- -devel: own %%{_datadir}/cmake/%%{name}/
- -devel: Requires: cmake (for %%{_datadir}/cmake ownership)

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 1.41.0-8
- rebuild for icu

* Mon Feb 22 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-7
- Add a patch for serialization of shared pointers to non polymorphic
  types

* Tue Feb  2 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-6
- More subpackage interdependency adjustments
  - boost does not bring in the MPI stuff.  Instead, $MPI-devel does.
    It needs to, so that the symbolic links don't dangle.
  - boost-graph-$MPI depends on boost-$MPI so that boost-mpich2
    does not satisfy the SONAME dependency of boost-graph-openmpi.
- Resolves: #559009

* Mon Feb  1 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.41.0-5
- Various fixes on the specification
- Resolves: #559009

* Fri Jan 29 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-5
- Introduce support for both OpenMPI and MPICH2
- Resolves: #559009

* Mon Jan 25 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-4
- Add a patch to build mapnik
- Resolves: #558383

* Tue Jan 19 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-3
- Generalize the soname selection

* Mon Jan 18 2010 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.41.0-2.2
- Further split the Boost.MPI sub-package into boost-mpi and
  boost-mpi-python
- Changed the description of Boost.MPI according to the actual
  dependency (MPICH2 rather than OpenMPI)
- Added a few details on the generation of the mpi.so library

* Thu Jan 14 2010 Petr Machata <pmachata@redhat.com> - 1.41.0-2
- Replace a boost-math subpackage with a stub
- Drop _cmake_lib_suffix and CMAKE_INSTALL_PREFIX magic, the rpm macro
  does that for us
- Drop LICENSE from the umbrella package
- Drop obsolete Obsoletes: boost-python and boost-doc <= 1.30.2

* Tue Jan 12 2010 Benjamin Kosnik <bkoz@redhat.com> - 1.41.0-1
- Don't package generated debug libs, even with 
  (-DCMAKE_BUILD_TYPE=RelWithDebInfo | Release).
- Update and include boost-cmake-soname.patch.
- Uncomment ctest.
- Fix up --with tests to run tests.

* Sat Dec 19 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.41.0-0.7
- Switched off the delivery into a versioned sub-directory

* Thu Dec 17 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.41.0-0.6
- Boost-CMake upstream integration

* Wed Dec 16 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.41.0-0.5
- Rebase to 1.41.0
- Set build type to RelWithDebInfo
- Resolves: #533922

* Mon Nov 16 2009 Denis Arnaud <denis.arnaud_fedora@m4x.org> - 1.40.0-1
- Add support for the Boost.MPI sub-package
- Build with CMake (https://svn.boost.org/trac/boost/wiki/CMake)
- Resolves: #529563

* Mon Nov 16 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-11
- Move comment in Patch13 out of line

* Mon Nov 16 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-10
- translate_exception.hpp misses a include
- Related: #537612

* Thu Oct 15 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-9
- Package index.html in the -doc subpackage
- Resolves: #529030

* Wed Oct 14 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-8
- Several fixes to support PySide
- Resolves: #520087
- GCC 4.4 name resolution fixes for GIL
- Resolves: #526834

* Sun Oct 11 2009 Jitesh Shah <jiteshs@marvell.com> 1.39.0-7
- Disable long double support for ARM

* Tue Sep 08 2009 Karsten Hopp <karsten@redhat.com> 1.39.0-6
- bump release and rebuild as the package was linked with an old libicu
  during the mass rebuild on s390x

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 1.39.0-5
- Make it to be usable with openssl-1.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-3
- Drop file list for main "boost" package, which was inadvertently left in.
- Add thread sub-package to capture omitted boost_thread.
- Add upstream patch to make boost_filesystem compatible with C++0x.
- Resolves: #496188
- Resolves: #509250

* Mon May 11 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.39.0-2
- Apply patch from Caolan McNamara
- Resolves: #500030 function_template bug is back...

* Thu May 07 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.39.0-1
- Update release.

* Wed May 06 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.39.0-0.3
- Fixes for rpmlint.

* Wed May 06 2009 Petr Machata <pmachata@redhat.com> - 1.39.0-0.2
- Split up boost package to sub-packages per library
- Resolves: #496188

* Wed May 06 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.39.0-0.1
- Rebase to 1.39.0.
- Add --with docs_generated.
- #225622: Substitute optflags at prep time instead of RPM_OPT_FLAGS.

* Mon May 04 2009 Benjamin Kosnik <bkoz@redhat.com> - 1.37.0-7
- Rebuild for libicu bump.

* Mon Mar 23 2009 Petr Machata <pmachata@redhat.com> - 1.37.0-6
- Apply a SMP patch from Stefan Ring
- Apply a workaround for "cannot appear in a constant-expression" in
  dynamic_bitset library.
- Resolves: #491537

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Petr Machata <pmachata@redhat.com> - 1.37.0-3
- Apply a unneccessary_iostreams patch from Caolan McNamara
- Fix soname patch so that it applies with fuzz=0.  Use fuzz=0 option
  in spec file just like ordinary patches do.
- Resolves: #479409

* Fri Dec 19 2008 Petr Machata <pmachata@redhat.com> - 1.37.0-2
- Apply a function_template patch from Caolan McNamara
- Resolves: #477131

* Tue Dec 16 2008 Benjamin Kosnik <bkoz@redhat.com> - 1.37.0-1
- Fix rpmlint rpath errors.
- Fix rpmlint warnings on tabs and spaces.
- Bump SONAME to 4

* Mon Nov 17 2008 Benjamin Kosnik <bkoz@redhat.com> - 1.37.0-0.1
- Rebase to 1.37.0.

* Tue Oct 21 2008 Benjamin Kosnik <bkoz@redhat.com> - 1.36.0-1
- Rebase to 1.36.0.

* Mon Oct  6 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-17
- Fix gcc43 patch to apply cleanly under --fuzz=0
- Resolves: #465003

* Mon Aug 11 2008 Petr Machata <pmachata@redhat.com> - 1.36.0-0.1.beta1
- Rebase to 1.36.0.beta1
  - Drop boost-regex.patch and portions of boost-gcc43.patch, port the rest
  - Automate SONAME tracking and bump SONAME to 4
  - Adjust boost-configure.patch to include threading=single,multi explicitly

* Thu Jun 12 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-16
- Fix "changes meaning of keywords" in boost date_time
- Related: #450718

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.34.1-15
- fix license tag

* Thu Mar 27 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-14
- Change devel-static back to static.
- Related: #225622

* Wed Mar 26 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-13
- Install library doc files
- Revamp %%install phase to speed up overall build time
- Some cleanups per merge review
- Resolves: #437032

* Thu Feb 14 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-12
- Fix "changes meaning of keywords" in boost python
- Resolves: #432694

* Wed Feb 13 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-11
- Fix "changes meaning of special_values_parser" in boost date_time
- Resolves: #432433

* Wed Feb  6 2008 Petr Machata <pmachata@redhat.com> - 1.34.1-10
- Fixes for GCC 4.3
- Resolves: #431609

* Mon Jan 14 2008 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-7
- Fixes for boost.regex (rev 42674).

* Wed Sep 19 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-5
- (#283771: Linking against boost libraries fails).

* Tue Aug 21 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-4
- Rebuild.

* Wed Aug 08 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-3
- Rebuild for icu 3.8 bump.

* Thu Aug 02 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-2
- SONAME to 3.

* Tue Jul 31 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1-1
- Update to boost_1_34_1.
- Source via http.
- Philipp Thomas <pth.suse.de> fix for RPM_OPT_FLAGS
- Philipp Thomas <pth.suse.de> fix for .so sym links.
- (#225622) Patrice Dumas review comments.

* Tue Jun 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.1.rc1-0.1
- Update to boost_1_34_1_RC1.

* Mon Apr 02 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-13
- (#225622: Merge Review: boost)
  Change static to devel-static.

* Mon Mar 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-12
- (#233523: libboost_python needs rebuild against python 2.5)
  Use patch.

* Mon Mar 26 2007 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-11
- (#225622: Merge Review: boost)
  Source to http.
  BuildRoot to preferred value.
  PreReq to post/postun -p
  Clarified BSL as GPL-Compatible, Free Software License.
  Remove Obsoletes.
  Add Provides boost-python.
  Remove mkdir -p $RPM_BUILD_ROOT%%{_docdir}
  Added periods for decription text.
  Fix Group field.
  Remove doc Requires boost.
  Preserve timestamps on install.
  Use %%defattr(-, root, root, -)
  Added static package for .a libs.
  Install static libs with 0644 permissions.
  Use %%doc for doc files.

* Mon Jan 22 2007 Benjamin Kosnik <bkoz@redhat.com> 1.34.0-0.5
- Update to boost.RC_1_34_0 snapshot as of 2007-01-19.
- Modify build procedures for boost build v2.
- Add *-mt variants for libraries, or at least variants that use
  threads (regex and thread).

* Thu Nov 23 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-10
- (#182414: boost: put tests in %%check section) via Rex Dieter
- Fix EVR with %%{?dist} tag via Gianluca Sforna

* Wed Nov 15 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-9
- (#154784: boost-debuginfo package is empty)

* Tue Nov 14 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-8
- (#205866: Revert scanner.hpp change.)

* Mon Nov 13 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-7
- (#205866: boost::spirit generates warnings with -Wshadow)
- (#205863: serialization lib generates warnings)
- (#204326: boost RPM missing dependencies)
- (#193465: [SIGNAL/BIND] Regressions with GCC 4.1)
- BUILD_FLAGS, add, to see actual compile line.
- REGEX_FLAGS, add, to compile regex with ICU support.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-6.1
- rebuild

* Tue May 16 2006 Karsten Hopp <karsten@redhat.de> 1.33.1-6
- buildrequire python-devel for Python.h

* Thu Feb 16 2006 Florian La Roche <laroche@redhat.com> - 1.33.1-5
- use the real version number to point to the shared libs

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.33.1-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 05 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-4
- Fix symbolic links.

* Wed Jan 04 2006 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-3
- Update to boost-1.33.1.
- (#176485: Missing BuildRequires)
- (#169271: /usr/lib/libboost*.so.? links missing in package)

* Thu Dec 22 2005 Jesse Keating <jkeating@redhat.com> 1.33.1-2
- rebuilt

* Mon Nov 14 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.1-1
- Update to boost-1.33.1 beta.
- Run testsuite, gather results.

* Tue Oct 11 2005 Nils Philippsen <nphilipp@redhat.com> 1.33.0-4
- build require bzip2-devel and zlib-devel

* Tue Aug 23 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.0-3
- Create doc package again.
- Parts of the above by Neal Becker <ndbecker2@gmail.com>.

* Fri Aug 12 2005 Benjamin Kosnik <bkoz@redhat.com> 1.33.0-1
- Update to boost-1.33.0, update SONAME to 2 due to ABI changes.
- Simplified PYTHON_VERSION by Philipp Thomas <pth@suse.de>

* Tue May 24 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-6
- (#153093: boost warns that gcc 4.0.0 is an unknown compiler)
- (#152205: development .so symbolic links should be in -devel subpackage)
- (#154783: linker .so symbolic links missing from boost-devel package)

* Fri Mar 18 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-5
- Revert boost-base.patch to old behavior.
- Use SONAMEVERSION instead of dllversion.

* Wed Mar 16 2005 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-4
- (#142612: Compiling Boost 1.32.0 Failed in RHEL 3.0 on Itanium2)
- (#150069: libboost_python.so is missing)
- (#141617: bad patch boost-base.patch)
- (#122817: libboost_*.so symbolic links missing)
- Re-add boost-thread.patch.
- Change boost-base.patch to show thread tags.
- Change boost-gcc-tools.patch to use SOTAG, compile with dllversion.
- Add symbolic links to files.
- Sanity check can compile with gcc-3.3.x, gcc-3.4.2, gcc-4.0.x., gcc-4.1.x.

* Thu Dec 02 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-3
- (#122817: libboost_*.so symbolic links missing)
- (#141574: half of the package is missing)
- (#141617: bad patch boost-base.patch)

* Wed Dec 01 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-2
- Remove bogus Obsoletes.

* Mon Nov 29 2004 Benjamin Kosnik <bkoz@redhat.com> 1.32.0-1
- Update to 1.32.0

* Wed Sep 22 2004 Than Ngo <than@redhat.com> 1.31.0-9
- cleanup specfile
- fix multiarch problem

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 05 2004 Warren Togami <wtogami@redhat.com> 1.31.0-7
- missing Obsoletes boost-python

* Mon May 03 2004 Benjamin Kosnik <bkoz@redhat.com>
- (#121630: gcc34 patch needed)

* Wed Apr 21 2004 Warren Togami <wtogami@redhat.com>
- #121415 FC2 BLOCKER: Obsoletes boost-python-devel, boost-doc
- other cleanups

* Tue Mar 30 2004 Benjamin Kosnik <bkoz@redhat.com>
- Remove bjam dependency. (via Graydon).
- Fix installed library names.
- Fix SONAMEs in shared libraries.
- Fix installed header location.
- Fix installed permissions.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 09 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0-2
- Update to boost-1.31.0

* Thu Jan 22 2004 Benjamin Kosnik <bkoz@redhat.com> 1.31.0-1
- Update to boost-1.31.0.rc2
- (#109307:  Compile Failure with boost libraries)
- (#104831:  Compile errors in apps using Boost.Python...)
- Unify into boost, boost-devel rpms.
- Simplify installation using bjam and prefix install.

* Tue Sep 09 2003 Nalin Dahyabhai <nalin@redhat.com> 1.30.2-2
- require boost-devel instead of devel in subpackages which require boost-devel
- remove stray Prefix: tag

* Mon Sep 08 2003 Benjamin Kosnik <bkoz@redhat.com> 1.30.2-1
- change license to Freely distributable
- verify installation of libboost_thread
- more boost-devel removals
- deal with lack of _REENTRANT on ia64/s390
- (#99458) rpm -e fixed via explict dir additions
- (#103293) update to 1.30.2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove packager, change to new Group:

* Tue May 06 2003 Tim Powers <timp@redhat.com> 1.30.0-3
- add deffattr's so we don't have unknown users owning files
