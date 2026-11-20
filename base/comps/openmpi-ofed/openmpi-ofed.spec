#
# Copyright (c) 2004-2005 The Trustees of Indiana University and Indiana
#                         University Research and Technology
#                         Corporation.  All rights reserved.
# Copyright (c) 2004-2005 The University of Tennessee and The University
#                         of Tennessee Research Foundation.  All rights
#                         reserved.
# Copyright (c) 2004-2005 High Performance Computing Center Stuttgart,
#                         University of Stuttgart.  All rights reserved.
# Copyright (c) 2004-2005 The Regents of the University of California.
#                         All rights reserved.
# Copyright (c) 2006-2022 Cisco Systems, Inc.  All rights reserved.
# Copyright (c) 2013      Mellanox Technologies, Inc.
#                         All rights reserved.
# Copyright (c) 2015      Research Organization for Information Science
#                         and Technology (RIST). All rights reserved.
# $COPYRIGHT$
#
# Additional copyrights may follow
#
# $HEADER$
#
############################################################################
#
# Copyright (c) 2003, The Regents of the University of California, through
# Lawrence Berkeley National Laboratory (subject to receipt of any
# required approvals from the U.S. Dept. of Energy).  All rights reserved.
#
# Initially written by:
#       Greg Kurtzer, <gmkurtzer@lbl.gov>
#
############################################################################


#############################################################################
#
# Configuration Options
#
# Options that can be passed in via rpmbuild's --define option.  Note
# that --define takes *1* argument: a multi-token string where the first
# token is the name of the variable to define, and all remaining tokens
# are the value.  For example:
#
# shell$ rpmbuild ... --define 'install_in_opt 1' ...
#
#############################################################################

# Define this if you want to make this SRPM build in
# /opt/NAME/VERSION-RELEASE instead of the default /usr/.  Note that
# Open MPI will be *entirely* installed in /opt.  One possible
# exception is the modulefile -- see the description of
# modulefile_path, below.
# type: bool (0/1)
%{!?install_in_opt: %define install_in_opt 0}

# Mellanox/HPC-X fork: install OpenMPI under
# /usr/mpi/gcc/<name>-<version>/ -- the long-standing MLNX_OFED / DOCA
# packaging convention.  DOCA 3.3.0 (openmpi 4.1.9a1) shipped at
# /usr/mpi/gcc/openmpi-4.1.9a1/, which kept all bundled libraries in a
# unique versioned subdir and never collided with system packages.
#
# Why the prefix change is required: OMPI 5.x bundles openpmix and
# prrte and, with the upstream default --prefix=/usr, drops
# libpmix.so.2 and libprrte.so.3 into /usr/lib64/ plus help texts
# under /usr/share/{pmix,prte}/.  Those collide with the system pmix
# and prrte-libs packages on RHEL 10 / ctyunos / SLES (SW#5008199,
# SW#5010922).  Moving --prefix to /usr/mpi/gcc/openmpi-<ver>/ keeps
# the bundled libs in a versioned subdir and removes the collision.
#
# The Ubuntu 24.04 libevent-dev / evdns.h collision (SW#5009387) is a
# separate symptom of the same upstream --prefix=/usr default, but it
# only manifests when libevent is bundled (--with-libevent=internal).
# With all_external_3rd_party=1 (this spec's default) libevent is
# never bundled, so SW#5009387 is fixed independently of mofed_prefix.
#
# install_in_opt takes priority if also set (=> /opt/<name>/<version>).
# Set mofed_prefix=0 (and install_in_opt=0) to fall back to the
# upstream default of --prefix=/usr -- but that path causes the
# pmix/prrte file collisions described above.
# type: bool (0/1)
%{!?mofed_prefix: %define mofed_prefix 1}

# This specfile expects to find all required 3rd party packages
# (Libevent, Hwloc, PMIx, PRRTE) externally, and will not use the
# internal/embedded copies of these packages.  This behavior is
# strongly recommended for packagers.  However, if you want to override
# this behavior, change the definition below to 0.
#
# NOTE: This option will cause "--with-libevent=external
# --with-hwloc=external --with-pmix=external --with-prrte=external" to
# be added to the arguments to configure. If you wish to use different
# CLI options, set this value to 0 and set configure_options to the
# CLI options you want.
%{!?all_external_3rd_party: %define all_external_3rd_party 1}

# Define this if you want this RPM to install environment setup
# shell scripts.
# Mellanox/HPC-X fork: default flipped from upstream 0 -> 1, because
# with mofed_prefix=1 (this fork's default) the OMPI binaries live
# under /usr/mpi/gcc/openmpi-<version>/bin/ which is not on $PATH by
# default; mpivars.{sh,csh} let users `source` them to set up the
# environment.  Still overridable via rpmbuild --define.
# type: bool (0/1)
%{!?install_shell_scripts: %define install_shell_scripts 1}
# type: string (root path to install shell scripts)
%{!?shell_scripts_path: %define shell_scripts_path %{_bindir}}
# type: string (base name of the shell scripts)
%{!?shell_scripts_basename: %define shell_scripts_basename mpivars}

# Define this to 1 if you want this RPM to install a modulefile.
# type: bool (0/1)
%{!?install_modulefile: %define install_modulefile 0}

# Root path to install modulefiles.  If the value modulefile_path is
# set, that directory is the root path for where the modulefile will
# be installed there (assuming install_modulefile==1), even if
# install_in_opt==1.  type: string (root path to install modulefile)
#
# NOTE: modulefile_path is not actually defined here, because we have
#       to check/process install_in_opt first.

# type: string (subdir to install modulefile)
%{!?modulefile_subdir: %define modulefile_subdir %{name}}
# type: string (name of modulefile)
# AZL: NVIDIA's version string; used for the tarball, the install prefix
# (/usr/mpi/gcc/openmpi-<upstream_version>) and module/selector names.
%global upstream_version 5.0.10rc2.2605121430
%global vendor_release 1.b99be7132e
%{!?modulefile_name: %define modulefile_name %{upstream_version}}

# The name of the modules RPM.  Can vary from system to system.
# RHEL6 calls it "environment-modules".
# type: string (name of modules RPM)
%{!?modules_rpm_name: %define modules_rpm_name environment-modules}

# Should we use the mpi-selector functionality?
# type: bool (0/1)
%{!?use_mpi_selector: %define use_mpi_selector 0}
# The name of the mpi-selector RPM.  Can vary from system to system.
# type: string (name of mpi-selector RPM)
%{!?mpi_selector_rpm_name: %define mpi_selector_rpm_name mpi-selector}
# The location of the mpi-selector executable (can be a relative path
# name if "mpi-selector" can be found in the path)
# type: string (path to mpi-selector executable)
%{!?mpi_selector: %define mpi_selector mpi-selector}

# Should we build a debuginfo RPM or not?
# type: bool (0/1)
# AZL: generate debuginfo like other distro packages (vendor default is 0).
%{!?build_debuginfo_rpm: %define build_debuginfo_rpm 1}

# Should we build an all-in-one RPM, or several sub-package RPMs?
# type: bool (0/1)
%{!?build_all_in_one_rpm: %define build_all_in_one_rpm 1}

# Should we use the default "check_files" RPM step (i.e., check for
# unpackaged files)?  It is discouraged to disable this, but some
# installers need it (e.g., older versions of OFED, because they
# installed lots of other stuff in the BUILD_ROOT before Open MPI/SHMEM).
# type: bool (0/1)
%{!?use_check_files: %define use_check_files 1}

# By default, RPM supplies a bunch of optimization flags, some of
# which may not work with non-gcc compilers.  We attempt to weed some
# of these out (below), but sometimes it's better to just ignore them
# altogether (e.g., PGI 6.2 will warn about unknown compiler flags,
# but PGI 7.0 will error -- and RPM_OPT_FLAGS contains a lot of flags
# that PGI 7.0 does not understand).  The default is to use the flags,
# but you can set this variable to 0, indicating that RPM_OPT_FLAGS
# should be erased (in which case you probabl want to supply your own
# optimization flags!).
# type: bool (0/1)
%{!?use_default_rpm_opt_flags: %define use_default_rpm_opt_flags 1}

# Some compilers can be installed via tarball or RPM (e.g., Intel,
# PGI).  If they're installed via RPM, then rpmbuild's auto-dependency
# generation stuff will work fine.  But if they're installed via
# tarball, then rpmbuild's auto-dependency generation stuff will
# break; complaining that it can't find a bunch of compiler .so files.
# So provide an option to turn this stuff off.
# type: bool (0/1)
%{!?disable_auto_requires: %define disable_auto_requires 0}

# On some platforms, Open MPI/SHMEM just flat-out doesn't work with
# -D_FORTIFY_SOURCE (e.g., some users have reported that there are
# problems on ia64 platforms).  In this case, just turn it off
# (meaning: this specfile will strip out that flag from the
# OS-provided compiler flags).  We already strip out _FORTIFY_SOURCE
# for non-GCC compilers; setting this option to 0 will *always* strip
# it out, even if you're using GCC.
# type: bool (0/1)
%{!?allow_fortify_source: %define allow_fortify_source 1}

# Define this to 1 if you want to keep libtool archive files
# Default is 0 (remove *.la files)
# type: bool (0/1)
%{!?install_libtool_archive: %define install_libtool_archive 0}

#############################################################################
#
# Configuration Logic
#
#############################################################################

%if %{install_in_opt}
%define _prefix /opt/%{name}/%{upstream_version}
%define _sysconfdir /opt/%{name}/%{upstream_version}/etc
%define _libdir /opt/%{name}/%{upstream_version}/lib
%define _includedir /opt/%{name}/%{upstream_version}/include
%define _mandir /opt/%{name}/%{upstream_version}/man

# Note that the name "openmpi" is hard-coded in
# opal/mca/installdirs/config for pkgdatadir; there is currently no
# easy way to have OMPI change this directory name internally.  So we
# just hard-code that name here as well (regardless of the value of
# %{name} or %{_name}).
%define _pkgdatadir /opt/%{name}/%{upstream_version}/share/openmpi

# Per advice from Doug Ledford at Red Hat, docdir is supposed to be in
# a fixed location.  But if you're installing a package in /opt, all
# bets are off.  So feel free to install it anywhere in your tree.  He
# suggests $prefix/doc, but the GNU Autotools these days default to
# $prefix/share/doc.
%define _defaultdocdir /opt/%{name}/%{upstream_version}/share/doc

# Also put the modulefile in /opt (unless the user already specified
# where they want it to go -- the modulefile is a bit different in
# that the user may want it outside of /opt).
%{!?modulefile_path: %define modulefile_path /opt/%{name}/%{upstream_version}/share/openmpi/modulefiles}
%endif

# Mellanox/HPC-X fork: when mofed_prefix=1 (the default in this fork)
# and install_in_opt is not also set, install everything under
# /usr/mpi/gcc/<name>-<version>/ (the MLNX_OFED / DOCA convention).
%if %{mofed_prefix}
%if !%{install_in_opt}
# AZL: use NVIDIA's MLNX OFED install layout (install.pl builds with
# _prefix /usr/mpi/gcc/openmpi-<version>, _datadir <prefix>/share and
# _defaultdocdir <prefix>/doc), independent of the renamed package.
%define _prefix /usr/mpi/gcc/openmpi-%{upstream_version}
%define _sysconfdir %{_prefix}/etc
%define _libdir %{_prefix}/lib
%define _includedir %{_prefix}/include
%define _datadir %{_prefix}/share
%define _mandir %{_prefix}/share/man
%define _pkgdatadir %{_prefix}/share/openmpi
%define _defaultdocdir %{_prefix}/doc
%{!?modulefile_path: %define modulefile_path %{_prefix}/share/openmpi/modulefiles}
%endif
%endif

# AZL: libraries and pkg-config files under the private prefix must not be
# advertised system-wide (the distro openmpi uses MPI-suffixed sonames, and a
# plain pkgconfig(ompi) here could satisfy openmpi-devel BuildRequires).
# Filter them, and the matching internal requirements.
%global __provides_exclude_from ^/usr/mpi/gcc/openmpi-%{upstream_version}/
# AZL: keep %%license files in the standard location despite the _datadir
# override above.
%global _defaultlicensedir /usr/share/licenses
%global __requires_exclude ^(libmpi(_mpifh|_usempif08|_usempi_ignore_tkr)?|libopen-pal|liboshmem|libompi_dbg_msgq)\\.so.*$

%if %{all_external_3rd_party}
# AZL: the distro prrte installs prterun under /usr/%%{_lib}/openmpi/bin, which
# mpirun does not search; record its path at configure time (configure fails
# if prterun is not there).
%define _configure_3rd_party --with-libevent=external --with-hwloc=external --with-pmix=external --with-prrte=external --with-prrte-bindir=/usr/%{_lib}/openmpi/bin
%else
%define _configure_3rd_party %{nil}
%endif

# Now that we have processed install_in_opt, we can see if
# modulefile_path was not set.  If it was not, then set it to a
# default value.
%{!?modulefile_path: %define modulefile_path /usr/share/Modules/modulefiles}

%if !%{build_debuginfo_rpm}
%define debug_package %{nil}
%endif

%if %(test "%{_prefix}" = "/usr" && echo 1 || echo 0)
%global _sysconfdir /etc
%else
%global _sysconfdir %{_prefix}/etc
%endif

# Is the sysconfdir under the prefix directory?  This affects
# whether we list the sysconfdir separately in the files sections,
# below.
%define sysconfdir_in_prefix %(test "`echo %{_sysconfdir} | grep %{_prefix}`" = "" && echo 0 || echo 1)

%{!?_pkgdatadir: %define _pkgdatadir %{_datadir}/openmpi}

%if !%{use_check_files}
%define __check_files %{nil}
%endif

# Set this to any options you want to pass in to configure.
# AZL: default to the configure options NVIDIA's install.pl passes for
# openmpi (the Mellanox optimized platform file, which builds pml/osc ucx as
# DSOs and enables OpenSHMEM). UCX, HCOLL and UCC are pinned explicitly
# instead of the installer's build-environment autodetection.
%{!?configure_options: %define configure_options --with-platform=contrib/platform/mellanox/optimized --with-ucx=/usr --without-hcoll --without-ucc}

%if !%{use_default_rpm_opt_flags}
%define optflags ""
%endif

%if %{use_mpi_selector}
%define install_shell_scripts 1
%endif

#############################################################################
#
# Preamble Section
#
#############################################################################

Summary: A powerful implementation of MPI/SHMEM
Name: openmpi-ofed
# AZL: no Epoch; the vendor's Epoch 3 only orders against older MLNX OFED
# "openmpi" builds and this package name has no prior versions.
# AZL: "rc2" is a pre-release, so use "~" so that the final 5.0.10 sorts newer.
Version: 5.0.10~rc2.2605121430
URL: https://www.open-mpi.org
Release: %autorelease
# Same Open MPI code base and bundled components (ROMIO, treematch) as the
# distro openmpi; matches its license expression.
License: LicenseRef-Callaway-BSD AND LicenseRef-Callaway-MIT AND LicenseRef-Romio
Group: Development/Libraries
# AZL: NVIDIA's MLNX_OFED source bundle (origin URL and hash are pinned in
# openmpi-ofed.comp.toml); %%prep extracts the nested openmpi SRPM.
Source6000: MLNX_OFED_SRC-26.04-0.8.5.0.tgz
# AZL: missing from upstream spec; required by ./configure and make.
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: cpio
BuildRequires: pkgconfig
# AZL: Fortran bindings and UCX (pml/osc ucx) from the OFED stack, as in
# NVIDIA's install.pl. Open MPI 5 has no verbs/NUMA code of its own (RDMA goes
# through UCX), so the installer's rdma-core/numactl entries are not needed.
BuildRequires: gcc-gfortran
BuildRequires: ucx-ofed-devel
# AZL: configure locates the external PRRTE launcher at build time, and mpirun
# execs it at run time (as in the distro openmpi); ssh launches remote ranks.
BuildRequires: prrte >= 3.0.0
Requires: prrte%{?_isa} >= 3.0.0
Requires: openssh-clients
Provides: mpi
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root
%if %{disable_auto_requires}
AutoReq: no
%endif
%if %{all_external_3rd_party}
# If we require all external 3rd party packages, then assume the use
# of the OS Libevent and Hwloc packages.
# AZL: pmix-devel/prrte-devel also missing from upstream spec for
# --with-pmix=external --with-prrte=external.
BuildRequires: libevent-devel >= 2.0.21 hwloc-devel pmix-devel >= 4.2.0 prrte-devel >= 3.0.0
%endif
%if %{install_modulefile}
Requires: %{modules_rpm_name}
%endif
%if %{use_mpi_selector}
Requires: %{mpi_selector_rpm_name}
%endif
# AZL: the UCX transports are separate ucx-ofed subpackages; require the
# InfiniBand/mlx5 ones so pml ucx has RDMA, and recommend the rest.
Requires: ucx-ofed%{?_isa}
Requires: ucx-ofed-ib%{?_isa}
Requires: ucx-ofed-ib-mlx5%{?_isa}
Recommends: ucx-ofed-rdmacm%{?_isa}
Recommends: ucx-ofed-cma%{?_isa}

%description
Open MPI is an open source implementation of the Message Passing
Interface specification (https://www.mpi-forum.org/) developed and
maintained by a consortium of research, academic, and industry
partners.

Open MPI also includes an implementation of the OpenSHMEM parallel
programming API (https://www.openshmem.org/).  OpenSHMEM is a
Partitioned Global Address Space (PGAS) abstraction layer, which
provides fast inter-process communication using one-sided
communication techniques.

This RPM contains all the tools necessary to compile, link, and run
Open MPI and OpenSHMEM jobs.

%if !%{build_all_in_one_rpm}

#############################################################################
#
# Preamble Section (runtime)
#
#############################################################################

%package runtime
Summary: Tools and plugin modules for running Open MPI/SHMEM jobs
Group: Development/Libraries
Provides: mpi
Provides: openmpi-ofed = %{version}
Provides: openmpi-ofed-runtime = %{version}
%if %{disable_auto_requires}
AutoReq: no
%endif
%if %{all_external_3rd_party}
# If we require all external 3rd party packages, then assume the use
# of the OS Libevent and Hwloc packages.
# AZL: pmix-devel/prrte-devel also missing from upstream spec for
# --with-pmix=external --with-prrte=external.
BuildRequires: libevent-devel >= 2.0.21 hwloc-devel pmix-devel >= 4.2.0 prrte-devel >= 3.0.0
%endif
%if %{install_modulefile}
Requires: %{modules_rpm_name}
%endif

%description runtime
Open MPI is an open source implementation of the Message Passing
Interface specification (https://www.mpi-forum.org/) developed and
maintained by a consortium of research, academic, and industry
partners.

Open MPI also includes an implementation of the OpenSHMEM parallel
programming API (https://www.openshmem.org/).  OpenSHMEM is a
Partitioned Global Address Space (PGAS) abstraction layer, which
provides fast inter-process communication using one-sided
communication techniques.

This subpackage provides general tools (mpirun, mpiexec, etc.) and the
Module Component Architecture (MCA) base and plugins necessary for
running Open MPI/OpenSHMEM jobs.

%endif

#############################################################################
#
# Preamble Section (devel)
#
#############################################################################

%package devel
Summary: Development tools and header files for Open MPI/SHMEM
Group: Development/Libraries
%if %{disable_auto_requires}
AutoReq: no
%endif
Provides: openmpi-ofed-devel = %{version}
Requires: %{name}-runtime

%description devel
Open MPI is an open source implementation of the Message Passing
Interface specification (https://www.mpi-forum.org/) developed and
maintained by a consortium of research, academic, and industry
partners.

Open MPI also includes an implementation of the OpenSHMEM parallel
programming API (https://www.openshmem.org/).  OpenSHMEM is a
Partitioned Global Address Space (PGAS) abstraction layer, which
provides fast inter-process communication using one-sided
communication techniques.

This subpackage provides the development files for Open MPI/OpenSHMEM,
such as wrapper compilers and header files for MPI/OpenSHMEM
development.

#############################################################################
#
# Preamble Section (docs)
#
#############################################################################

%package docs
Summary: Documentation for Open MPI/SHMEM
Group: Development/Documentation
%if %{disable_auto_requires}
AutoReq: no
%endif
Provides: openmpi-ofed-docs = %{version}
Requires: %{name}-runtime

%description docs
Open MPI is an open source implementation of the Message Passing
Interface specification (https://www.mpi-forum.org/) developed and
maintained by a consortium of research, academic, and industry
partners.

Open MPI also includes an implementation of the OpenSHMEM parallel
programming API (https://www.openshmem.org/).  OpenSHMEM is a
Partitioned Global Address Space (PGAS) abstraction layer, which
provides fast inter-process communication using one-sided
communication techniques.

This subpackage provides the documentation for Open MPI/OpenSHMEM.

#############################################################################
#
# Preparatory Section
#
#############################################################################
%prep
tar -xf %{SOURCE6000}
_openmpi_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/openmpi-%{upstream_version}-%{vendor_release}.src.rpm' -print -quit)
if [ -z "$_openmpi_srpm" ]; then
  echo "ERROR: openmpi source RPM not found inside %{SOURCE6000}" >&2
  exit 1
fi
rpm2cpio "$_openmpi_srpm" | cpio -idm './openmpi-%{upstream_version}-%{vendor_release}.tar.gz'
rm -rf MLNX_OFED_SRC-*
# Unbelievably, some versions of RPM do not first delete the previous
# installation root (e.g., it may have been left over from a prior
# failed build).  This can lead to Badness later if there's files in
# there that are not meant to be packaged.
rm -rf $RPM_BUILD_ROOT

tar -xf openmpi-%{upstream_version}-%{vendor_release}.tar.gz
%setup -q -T -D -n openmpi-%{upstream_version}
# AZL: the Mellanox platform file overrides C/CXX/FC/CCAS FLAGS with
# "-O3 -g", dropping the distro hardening compile flags while the hardened
# link flags stay (configure then cannot run test programs). Keep the distro
# flags instead of disabling hardened linking as install.pl does on RHEL10.
sed -i -E '/^ +(C|CXX|FC|CCAS)FLAGS="-O3 -g"$/d' contrib/platform/mellanox/optimized
if grep -qE '^ +(C|CXX|FC|CCAS)FLAGS="-O3' contrib/platform/mellanox/optimized; then exit 1; fi

#############################################################################
#
# Build Section
#
#############################################################################

%build

# rpmbuild processes seem to be geared towards the GNU compilers --
# they pass in some flags that will only work with gcc.  So if we're
# trying to build with some other compiler, the process will choke.
# This is *not* something the user can override with a well-placed
# --define on the rpmbuild command line, unless they find and override
# all "global" CFLAGS kinds of RPM macros (every distro names them
# differently).  For example, non-gcc compilers cannot use
# FORTIFY_SOURCE (at least, not as of 6 Oct 2006).  We can really only
# examine the basename of the compiler, so search for it in a few
# places.

%if %{allow_fortify_source}
using_gcc=1
if test "$CC" != ""; then
    # Do horrible things to get the basename of just the compiler,
    # particularly in the case of multword values for $CC
    eval "set $CC"
    if test "`basename $1`" != "gcc"; then
        using_gcc=0
    fi
fi

if test "$using_gcc" = "1"; then
    # Do wretched things to find a CC=* token
    eval "set -- %{configure_options}"
    compiler=
    while test "$1" != "" -a "$compiler" = ""; do
         case "$1" in
         CC=*)
                 compiler=`echo $1 | cut -d= -f2-`
                 ;;
         esac
         shift
    done

    # Now that we *might* have the compiler name, do a best-faith
    # effort to see if it's gcc.  Blah!
    if test "$compiler" != ""; then
        if test "`basename $compiler`" != "gcc"; then
            using_gcc=0
        fi
    fi
fi
%else
# If we're not allowing _FORTIFY_SOURCE, then just set using_gcc to 0 and
# the logic below will strip _FORTIFY_SOURCE out if it's present.
using_gcc=0
%endif

# If we're not using the default RPM_OPT_FLAGS, then wipe them clean
# (the "optflags" macro has already been wiped clean, above).

%if !%{use_default_rpm_opt_flags}
RPM_OPT_FLAGS=
export RPM_OPT_FLAGS
%endif

# If we're not GCC, strip out any GCC-specific arguments in the
# RPM_OPT_FLAGS before potentially propagating them everywhere.

if test "$using_gcc" = 0; then

    # Non-gcc compilers cannot handle FORTIFY_SOURCE (at least, not as
    # of Oct 2006)
    RPM_OPT_FLAGS="`echo $RPM_OPT_FLAGS | sed -e 's@-D_FORTIFY_SOURCE[=0-9]*@@'`"

    # Non-gcc compilers will generate warnings for several flags
    # placed in RPM_OPT_FLAGS by RHEL5, but -mtune=generic will cause
    # an error for icc 9.1.
    RPM_OPT_FLAGS="`echo $RPM_OPT_FLAGS | sed -e 's@-mtune=generic@@'`"
fi

CFLAGS="%{?cflags:%{cflags}}%{!?cflags:$RPM_OPT_FLAGS}"
CXXFLAGS="%{?cxxflags:%{cxxflags}}%{!?cxxflags:$RPM_OPT_FLAGS}"
FCFLAGS="%{?fcflags:%{fcflags}}%{!?fcflags:$RPM_OPT_FLAGS}"
export CFLAGS CXXFLAGS FCFLAGS
%configure %{configure_options} %{_configure_3rd_party}
%{__make} %{?mflags}%{!?mflags:%{?_smp_mflags}}


#############################################################################
#
# Install Section
#
#############################################################################

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}
# AZL: every internal shared library must be covered by the
# __requires_exclude filter above, or the package gets unresolvable Requires.
for lib in $RPM_BUILD_ROOT%{_libdir}/lib*.so.*; do
    case "$(basename "$lib")" in
        libmpi.so.*|libmpi_mpifh.so.*|libmpi_usempif08.so.*|libmpi_usempi_ignore_tkr.so.*|libopen-pal.so.*|liboshmem.so.*) ;;
        *) echo "ERROR: $lib is not in __requires_exclude" >&2; exit 1 ;;
    esac
done
# AZL: mpirun looks for prterun in its own bindir first. Point it at the
# distro PRRTE there, so prterun runs from this prefix and remote daemons and
# ranks get this prefix's PATH/LD_LIBRARY_PATH instead of the distro
# openmpi's (/usr/%%{_lib}/openmpi).
ln -s ../../../../%{_lib}/openmpi/bin/prterun $RPM_BUILD_ROOT%{_bindir}/prterun
ln -s ../../../../%{_lib}/openmpi/bin/prted $RPM_BUILD_ROOT%{_bindir}/prted
# AZL: pre-create the doc parent so it can be owned (%%doc populates it later).
install -d $RPM_BUILD_ROOT%{_defaultdocdir}

# We've had cases of config.log being left in the installation tree.
# We don't need that in an RPM.
find $RPM_BUILD_ROOT -name config.log -exec rm -f {} \;

%if !%{install_libtool_archive}
# Libtool archive files (.la files) create an unnecessary dependency
# between linked applications and the development versions of packages
# upon which Open MPI depends. For example, when building an application
# which uses Libtool, Open MPI would create a dependency not just on
# the HWLOC libs package, but the HWLOC devel package
# (to get the .so.1 -> .so symlink). Best practice in package builders
# appears to be to skip shipping .la files because of this issue.
find $RPM_BUILD_ROOT/%{_libdir} -name \*.la -exec rm -f {} \;
%endif
# End of libotool_archive if

# First, the [optional] modulefile

%if %{install_modulefile}
%{__mkdir_p} $RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/
cat <<EOF >$RPM_BUILD_ROOT/%{modulefile_path}/%{modulefile_subdir}/%{modulefile_name}
#%Module

# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI/SHMEM RPM).  Any changes made here will be lost a) if the RPM is
# uninstalled, or b) if the RPM is upgraded or uninstalled.

proc ModulesHelp { } {
   puts stderr "This module adds Open MPI/SHMEM v%{upstream_version} to various paths"
}

module-whatis   "Sets up Open MPI/SHMEM v%{upstream_version} in your environment"

prepend-path PATH "%{_prefix}/bin/"
prepend-path LD_LIBRARY_PATH %{_libdir}
prepend-path MANPATH %{_mandir}
EOF
%endif
# End of modulefile if

# Next, the [optional] shell scripts

%if %{install_shell_scripts}
%{__mkdir_p} $RPM_BUILD_ROOT/%{shell_scripts_path}
cat <<EOF > $RPM_BUILD_ROOT/%{shell_scripts_path}/%{shell_scripts_basename}.sh
# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI/SHMEM RPM).  Any changes made here will be lost if the RPM is
# uninstalled or upgraded.

# PATH
if test -z "\`echo \$PATH | grep %{_bindir}\`"; then
    PATH=%{_bindir}:\${PATH}
    export PATH
fi

# LD_LIBRARY_PATH
if test -z "\`echo \$LD_LIBRARY_PATH | grep %{_libdir}\`"; then
    LD_LIBRARY_PATH=%{_libdir}\${LD_LIBRARY_PATH:+:}\${LD_LIBRARY_PATH}
    export LD_LIBRARY_PATH
fi

# MANPATH
if test -z "\`echo \$MANPATH | grep %{_mandir}\`"; then
    MANPATH=%{_mandir}:\${MANPATH}
    export MANPATH
fi

# MPI_ROOT
MPI_ROOT=%{_prefix}
export MPI_ROOT
EOF
cat <<EOF > $RPM_BUILD_ROOT/%{shell_scripts_path}/%{shell_scripts_basename}.csh
# NOTE: This is an automatically-generated file!  (generated by the
# Open MPI/SHMEM RPM).  Any changes made here will be lost if the RPM is
# uninstalled or upgraded.

# path
if ("" == "\`echo \$path | grep %{_bindir}\`") then
    set path=(%{_bindir} \$path)
endif

# LD_LIBRARY_PATH
if ("1" == "\$?LD_LIBRARY_PATH") then
    if ("\$LD_LIBRARY_PATH" !~ *%{_libdir}*) then
        setenv LD_LIBRARY_PATH %{_libdir}:\${LD_LIBRARY_PATH}
    endif
else
    setenv LD_LIBRARY_PATH %{_libdir}
endif

# MANPATH
if ("1" == "\$?MANPATH") then
    if ("\$MANPATH" !~ *%{_mandir}*) then
        setenv MANPATH %{_mandir}:\${MANPATH}
    endif
else
    setenv MANPATH %{_mandir}:
endif

# MPI_ROOT
setenv MPI_ROOT %{_prefix}
EOF
%endif
# End of shell_scripts if

%if !%{build_all_in_one_rpm}

# Build lists of files that are specific to each package that are not
# easily identifiable by a single directory (e.g., the different
# libraries).  In a somewhat lame move, we can't just pipe everything
# together because if the user, for example, did --disable-shared
# --enable-static, the "grep" for .so files will not find anything and
# therefore return a non-zero exit status.  This will cause RPM to
# barf.  So be super lame and dump the egrep through /bin/true -- this
# always gives a 0 exit status.

# First, find all the files
rm -f all.files runtime.files remaining.files devel.files
find $RPM_BUILD_ROOT -type f -o -type l | \
   sed -e "s@$RPM_BUILD_ROOT@@" \
   > all.files | /bin/true

# Runtime files.  This should generally be library files and some
# executables (no man pages, no doc files, no header files).  Do *not*
# include wrapper compilers.
cat all.files | \
    egrep '/lib/|/lib64/|/lib32/|/bin/|/etc/|/help-' \
    > tmp.files | /bin/true
# Snip out a bunch of executables (e.g., wrapper compilers, pkgconfig
# files, .la and .a files) and docs
egrep -vi 'bin/mpic|bin/mpif|bin/mpif77|bin/mpif90|pkgconfig|wrapper|\.mod$|\.la$|\.a$' tmp.files > runtime.files | /bin/true

rm -f tmp.files

# Now take the runtime files out of all.files so that we don't get
# duplicates.
grep -v -f runtime.files all.files > remaining.files

# Devel files.  Basically -- just exclude the man pages and doc files.
cat remaining.files | \
   egrep -v '/man/|/doc/' \
   > devel.files | /bin/true

%endif
# End of !build_all_in_one_rpm

#############################################################################
#
# Clean Section
#
#############################################################################
%clean
# We may be in the directory that we're about to remove, so cd out of
# there before we remove it
cd /tmp

# Remove installed driver after rpm build finished
rm -rf $RPM_BUILD_DIR/%{name}-%{upstream_version}

test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT

#############################################################################
#
# Post Install Section
#
#############################################################################
%if %{use_mpi_selector}
%post
%{mpi_selector} \
	--register %{name}-%{upstream_version} \
	--source-dir %{shell_scripts_path} \
        --yes
%endif

#############################################################################
#
# Pre Uninstall Section
#
#############################################################################
%if %{use_mpi_selector}
%preun
%{mpi_selector} --unregister %{name}-%{upstream_version} --yes || \
      /bin/true > /dev/null 2> /dev/null
%endif

#############################################################################
#
# Files Section
#
#############################################################################

%if %{build_all_in_one_rpm}

#
# All in one RPM
#
# Easy; just list the prefix and then specifically call out the doc
# files.
#

%files
%defattr(-, root, root, -)
%if %(test "%{_prefix}" = "/usr" && echo 1 || echo 0)
%{_bindir}/*
%{_includedir}/*
%{_libdir}/*
%{_datadir}/*
%else
# AZL: list the prefix contents explicitly so the configuration files can be
# marked %%config.
%dir %{_prefix}
%{_bindir}
%{_includedir}
%{_libdir}
%{_datadir}
%dir %{_defaultdocdir}
%dir %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/openmpi-mca-params.conf
%{_sysconfdir}/openmpi-totalview.tcl
%endif
# If the sysconfdir is not under the prefix, then list it explicitly.
%if !%{sysconfdir_in_prefix}
%{_sysconfdir}
%endif
# If install_in_opt, then we're installing OMPI to
# /opt/openmpi/<version>.  But be sure to also explicitly mention
# /opt/openmpi so that it can be removed by RPM when everything under
# there is also removed.
%if %{install_in_opt}
%dir /opt/%{name}
%endif
# AZL: own the MLNX OFED MPI parent directories (co-owned with other MLNX
# OFED MPI packages).
%if %{mofed_prefix} && !%{install_in_opt}
%dir /usr/mpi
%dir /usr/mpi/gcc
%endif
# If we're installing the modulefile, get that, too
%if %{install_modulefile}
%{modulefile_path}
%endif
# If we're installing the shell scripts, get those, too
# AZL: only when they live outside %%{_prefix}, which is already listed.
%if %{install_shell_scripts}
%if %(echo "%{shell_scripts_path}" | grep -q "^%{_prefix}/" && echo 0 || echo 1)
%{shell_scripts_path}/%{shell_scripts_basename}.sh
%{shell_scripts_path}/%{shell_scripts_basename}.csh
%endif
%endif
%license LICENSE
%doc README.md

%else

#
# Sub-package RPMs
#
# Harder than all-in-one.  Explicitly list all the files we want by
# the various *.files we generated above.  Only list directories if
# they are not /usr (or assumedly any other location that does not
# already exist).

%files runtime -f runtime.files
%defattr(-, root, root, -)
%if %(test "%{_prefix}" != "/usr" && echo 1 || echo 0)
%dir %{_prefix}
%dir %{_pkgdatadir}
# If the sysconfdir is not under the prefix, then list it explicitly.
%if !%{sysconfdir_in_prefix}
%dir %{_sysconfdir}
%endif
%endif

# If install_in_opt, then we're installing OMPI to
# /opt/openmpi/<version>.  But be sure to also explicitly mention
# /opt/openmpi so that it can be removed by RPM when everything under
# there is also removed.  Also list /opt/openmpi/<version>/share so
# that it can be removed as well.
%if %{install_in_opt}
%dir /opt/%{name}
%dir /opt/%{name}/%{upstream_version}/share
%endif
# If we're installing the modulefile, get that, too
%if %{install_modulefile}
%{modulefile_path}
%endif
# If we're installing the shell scripts, get those, too
%if %{install_shell_scripts}
%{shell_scripts_path}/%{shell_scripts_basename}.sh
%{shell_scripts_path}/%{shell_scripts_basename}.csh
%endif
%doc README.md LICENSE

%files devel -f devel.files
%defattr(-, root, root, -)

%files docs
%defattr(-, root, root, -)
# Note that we list the mandir specifically here, because we want all
# files found in that tree, because rpmbuild may have compressed them
# after we installed them (e.g., foo.1.gz or foo.1.bz2), and we
# therefore don't know the exact filenames.
%{_mandir}

# Explicitly list the pkgdocdir so that it will be removed when the
# RPM is removed.
%{_pkgdocdir}

%endif


#############################################################################
#
# Changelog
#
#############################################################################
%changelog
%autochangelog
