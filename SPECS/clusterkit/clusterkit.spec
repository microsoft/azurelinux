#############################################################################
#
# Configuration Options
#
#############################################################################
%{!?configure_options: %global configure_options --with-mpi=%{_libdir}/openmpi}
%global with_mpi 1
# mpi, cuda and nccl require setting parameters in configure_opts.
# Without them they will fail to work:
%define grep_in_configure_optios() %(echo -- %{configure_options} \\\
  | grep -q -- '--with-%1='; echo $?)
%if %{grep_in_configure_optios mpi} == 0
  %global with_mpi 1
%endif
%if %{grep_in_configure_optios cuda} == 0
  %global with_cuda 1
  %global gdr_param --enable-gdr
%endif
%if %{grep_in_configure_optios nccl} == 0
  %global with_nccl 1
%endif

# Some compilers can be installed via tarball or RPM (e.g., Intel,
# PGI).  If they're installed via RPM, then rpmbuild's auto-dependency
# generation stuff will work fine.  But if they're installed via
# tarball, then rpmbuild's auto-dependency generation stuff will
# break; complaining that it can't find a bunch of compiler .so files.
# So provide an option to turn this stuff off.
# type: bool (0/1)
%{!?disable_auto_requires: %define disable_auto_requires 0}

#############################################################################
#
# Preamble Section
#
#############################################################################

Summary: ClusterKit validation tool
Name:           clusterkit
Version: 1.15.472
Release:        1%{?dist}
License: BSD
Group: Applications
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.2.2/SOURCES/mlnx_ofed/OFED-internal-25.10-2.4.1.tgz
Source0:         %{_distro_sources_url}/clusterkit-1.15.472.tar.gz
Packager: %{?_packager:%{_packager}}%{!?_packager:%{_vendor}}
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
Prefix: %{_prefix}
Provides: clusterkit
BuildRoot:       /var/tmp/%{name}-%{version}-build
%if 0%{?suse_version}
BuildRequires: gcc-fortran gcc autoconf automake libtool
%else
BuildRequires: gcc-gfortran gcc autoconf automake libtool
BuildRequires: openmpi-devel
%endif

%if %{disable_auto_requires}
AutoReq: no
%endif

%if %{with cuda} || %{with nccl}
# Don't generate automatic dependencies from cuda wrappers and nccl:
# they are being loaded with dlopen().
%global __requires_exclude ^(libcudart\\.so\\.)|(libnccl\\.so\\.)|(libcublas\\.so\\.)|(libcublasLt\\.so\\.)
%endif

%description
ClusterKit validation tool

#############################################################################
#
# Prepatory Section
#
#############################################################################
%prep
%setup -q -n clusterkit-%{version}

%build
export PATH=%{_libdir}/openmpi/bin:$PATH
export LD_LIBRARY_PATH=%{_libdir}/openmpi/lib:${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
%define _with_arg()   %{expand:%%{?with_%{1}:--with-%{2}}%%{!?with_%{1}:--without-%{2}}}
%define _enable_arg() %{expand:%%{?with_%{1}:--enable-%{2}}%%{!?with_%{1}:--disable-%{2}}}

%configure %_with_arg mpi mpi \
	   %_with_arg cuda cuda \
           %{?gdr_param} \
           %{?configure_options}
%{__make} %{?_smp_mflags} V=1

#############################################################################
#
# Install Section
#
#############################################################################
%install
%{__make} DESTDIR=%{buildroot} install

#############################################################################
#
# CLEAN Section
#
#############################################################################
%clean
# We should leave build root for IBED installation
# test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT
cd /tmp

test "x$RPM_BUILD_ROOT" != "x" && rm -rf $RPM_BUILD_ROOT

%if %{with cuda} || %{with nccl}
%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%endif

#############################################################################
#
# Files Section
#
#############################################################################


%files
%define outdir %{_bindir}/output
%define scopesdir %{_bindir}/scopes
%defattr(-, root, root)
%doc README
%_bindir/analysis.py
%_bindir/bwResultAnalyzer.py
%_bindir/clusterkit
%_bindir/clusterkit.sh
%_bindir/core_to_hca_dgx.sh
%_bindir/core_to_hca_dgx_gpu.sh
%_bindir/core_to_hca_dgx100.sh
%_bindir/hca_to_core_dgx100.sh
%_bindir/run_clusterkit.sh
%dir %{outdir}
%outdir/generate_output.py
%outdir/output_config.ini
%outdir/latency_calc_config.csv
%outdir/requirements.txt
%outdir/run.sh
%dir %{scopesdir}
%scopesdir/scopes.py
%scopesdir/run_scopes.sh
%scopesdir/requirements.txt
%scopesdir/README.md
%if %{with cuda}
%_libdir/libcuda_wrapper.*
%_libdir/libstress_gpu_ops.*
%endif
%if %{with nccl}
%_libdir/libnccl_wrapper.*
%endif
%_datadir/clusterkit/doc/README


#############################################################################
#
# Changelog
#
#############################################################################
%changelog
* Thu Apr 17 2026 Azure Linux Team - 1.15.472-1
- Initial Azure Linux import from NVIDIA (license: BSD)
- License verified
