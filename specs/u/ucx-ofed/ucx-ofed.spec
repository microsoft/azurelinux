# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?configure_options: %global configure_options %{nil}}
%bcond_without cma
%bcond_with    cuda
%bcond_with    gdrcopy
%bcond_without ib
%bcond_with    knem
%bcond_without rdmacm
%bcond_with    rocm
%bcond_with    ugni
%bcond_without xpmem
%bcond_with    vfs
%bcond_with    mad
%bcond_with    ze
%bcond_without mlx5
%bcond_with    gda
%bcond_with    efa

%global upstream_name ucx

Name: ucx-ofed
Version: 1.21.0.20260504
Release: 1.65a1a71af%{?dist}%{?debug:.debug}.2604085
Summary: UCX is a communication library implementing high-performance messaging
Group: System Environment/Libraries

License: BSD
URL: http://www.openucx.org
Source6000: MLNX_OFED_SRC-26.04-0.8.5.0.tgz

BuildRoot: %(mktemp -ud %{_tmppath}/%{upstream_name}-%{version}-%{release}-XXXXXX)
Prefix: %{_prefix}

# UCX currently supports only the following architectures
ExclusiveArch: aarch64 ppc64le x86_64

%if %{defined extra_deps}
Requires: %{?extra_deps}
%endif

# Legacy package cleanup
Conflicts: ucx-knem < %{version}-%{release}
Obsoletes: ucx-knem < %{version}-%{release}

BuildRequires: automake autoconf libtool gcc-c++
%if %{with cma}
BuildRequires: glibc-devel >= 2.15
%endif
%if %{with gdrcopy}
BuildRequires: gdrcopy
%endif
%if %{with ib}
BuildRequires: rdma-core-ofed-devel
%endif
%if %{with mlx5}
BuildRequires: rdma-core-ofed-devel
%endif
%if %{with efa}
BuildRequires: rdma-core-ofed-devel
%endif
%if %{with knem}
BuildRequires: knem
%endif
%if %{with rdmacm}
BuildRequires: rdma-core-ofed-devel
%endif
%if %{with rocm}
BuildRequires: hsa-rocr-dev
%endif
%if %{with xpmem}
BuildRequires: pkgconfig(cray-xpmem)
%endif
%if %{with vfs}
BuildRequires: fuse3-devel
%endif
%if %{with ze}
BuildRequires: level-zero-devel
%endif
%if "%{debug}" == "1"
BuildRequires: valgrind-devel
%endif
%if %{with mad}
BuildRequires: rdma-core-ofed-devel
%endif

%description
UCX is an optimized communication framework for high-performance distributed
applications. UCX utilizes high-speed networks, such as RDMA (InfiniBand, RoCE,
etc), Cray Gemini or Aries, for inter-node communication. If no such network is
available, TCP is used instead. UCX supports efficient transfer of data in
either main memory (RAM) or GPU memory (through CUDA and ROCm libraries). In
addition, UCX provides efficient intra-node communication, by leveraging the
following shared memory mechanisms: posix, sysv, cma, knem, and xpmem.
The acronym UCX stands for "Unified Communication X".

This package was built from '' branch, commit 65a1a71.

%if "%{_vendor}" == "suse" && 0%{?suse_version} < 1600
%debug_package
%endif

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Header files required for developing with UCX
Group: Development/Libraries

%description devel
Provides header files and examples for developing with UCX.

%prep
tar -xf %{SOURCE6000}
_ucx_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/ucx-%{version}-*.src.rpm' -print -quit)
if [ -z "$_ucx_srpm" ]; then
    echo "ERROR: ucx source RPM not found inside %{SOURCE6000}" >&2
    exit 1
fi
rpm2cpio "$_ucx_srpm" | cpio -idm './ucx-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf ucx-%{version}.tar.gz
%setup -q -T -D -n %{upstream_name}-%{version}

%build
%define _with_arg()   %{expand:%%{?with_%{1}:--with-%{2}}%%{!?with_%{1}:--without-%{2}}}
%define _enable_arg() %{expand:%%{?with_%{1}:--enable-%{2}}%%{!?with_%{1}:--disable-%{2}}}
%configure --disable-optimizations \
           %{!?debug:--disable-logging} \
           %{!?debug:--disable-debug} \
           %{!?debug:--disable-assertions --enable-mt} \
           %{!?debug:--disable-params-check} \
           %{?debug:--with-valgrind} \
           %{?debug:--enable-profiling} \
           %{?debug:--enable-frame-pointer} \
           %{?debug:--enable-stats} \
           %{?debug:--enable-debug-data} \
           %{?debug:--enable-mt} \
           --without-go \
           --without-java --without-gda \
           %_enable_arg cma cma \
           %_with_arg cuda cuda \
           %_with_arg gdrcopy gdrcopy \
           %_with_arg ib verbs \
           %_with_arg mlx5 mlx5 \
           %_with_arg efa efa \
           %_with_arg knem knem \
           %_with_arg rdmacm rdmacm \
           %_with_arg rocm rocm \
           %_with_arg xpmem xpmem \
           %_with_arg vfs fuse3 \
           %_with_arg ugni ugni \
           %_with_arg mad mad \
           %_with_arg ze ze \
           %{?configure_options}
make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/libucs_signal.a
rm -f %{buildroot}%{_libdir}/ucx/*.la
rm -f %{buildroot}%{_libdir}/ucx/lib*.so

%files
%{_libdir}/lib*.so.*
%{_bindir}/ucx_info
%{_bindir}/ucx_perftest
%{_bindir}/ucx_perftest_daemon
%{_bindir}/ucx_read_profile
%if "%{debug}" == "1"
%{_bindir}/ucs_stats_parser
%endif
%{_bindir}/io_demo
%{_datadir}/ucx
%exclude %{_datadir}/ucx/examples
%doc README AUTHORS NEWS
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_sysconfdir}/ucx/ucx.conf

%files devel
%{_includedir}/uc*
%exclude %{_includedir}/uct/ib/mlx5/gdaki*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/ucx.pc
%{_libdir}/pkgconfig/ucx-uct.pc
%{_libdir}/pkgconfig/ucx-ucs.pc
%{_libdir}/cmake/ucx/*.cmake
%{_datadir}/ucx/examples

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%package static
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Static libraries required for developing with UCX
Group: Development/Libraries

%description static
Provides static libraries required for developing with UCX.

%files static
%{_libdir}/lib*.a
%{_libdir}/ucx/lib*.a
%if %{with cma}
%{_libdir}/pkgconfig/ucx-cma.pc
%endif
%if %{with knem}
%{_libdir}/pkgconfig/ucx-knem.pc
%endif
%if %{with xpmem}
%{_libdir}/pkgconfig/ucx-xpmem.pc
%endif
%if %{with ib}
%{_libdir}/pkgconfig/ucx-ib.pc
%endif
%if %{with mlx5}
%{_libdir}/pkgconfig/ucx-ib-mlx5.pc
%endif
%if %{with efa}
%{_libdir}/pkgconfig/ucx-ib-efa.pc
%endif
%if %{with rdmacm}
%{_libdir}/pkgconfig/ucx-rdmacm.pc
%endif
%if %{with vfs}
%{_libdir}/pkgconfig/ucx-fuse.pc
%endif
%if %{with cuda} && %{with mlx5} && %{with gda}
%{_libdir}/pkgconfig/ucx-ib-mlx5-gda.pc
%endif

%if %{with cma}
%package cma
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX CMA support
Group: System Environment/Libraries

%description cma
Provides CMA (Linux cross-memory-attach) transport for UCX. It utilizes the
system calls process_vm_readv/writev() for one-shot memory copy from another
process.

%files cma
%{_libdir}/ucx/libuct_cma.so.*
%endif

%if %{with cuda}
%package cuda
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX CUDA support
Group: System Environment/Libraries

%description cuda
Provide CUDA (NVIDIA GPU) support for UCX. Enables passing GPU memory pointers
to UCX communication routines, and transports taking advantage of GPU-Direct
technology for direct data transfer between GPU and RDMA devices.

%files cuda
%{_libdir}/ucx/libucx_perftest_cuda.so.*
%{_libdir}/ucx/libucm_cuda.so.*
%{_libdir}/ucx/libuct_cuda.so.*
%endif

%if %{with gdrcopy}
%package gdrcopy
Requires: %{name}-cuda%{?_isa} = %{version}-%{release}
Summary: UCX GDRCopy support
Group: System Environment/Libraries

%description gdrcopy
Provide GDRCopy support for UCX. GDRCopy is a low-latency GPU memory copy
library, built on top of the NVIDIA GPUDirect RDMA technology.

%files gdrcopy
%{_libdir}/ucx/libuct_cuda_gdrcopy.so.*
%endif

%if %{with ib}
%package ib
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX RDMA support
Group: System Environment/Libraries

%description ib
Provides support for IBTA-compliant transports for UCX. This includes RoCE,
InfiniBand, OmniPath, and any other transport supported by IB Verbs API.
Typically these transports provide RDMA support, which enables a fast and
hardware-offloaded data transfer.

%files ib
%{_libdir}/ucx/libuct_ib.so.*
%endif

%if %{with mlx5}
%package ib-mlx5
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX IB MLX5 RDMA provider support
Group: System Environment/Libraries

%description ib-mlx5
Provides support for DevX, Direct Verbs and DC transports for Infiniband
devices.

%files ib-mlx5
%{_libdir}/ucx/libuct_ib_mlx5.so.*
%endif

%if %{with efa}
%package ib-efa
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX EFA device RDMA support
Group: System Environment/Libraries

%description ib-efa
Provides support for EFA device as an IBTA transport for UCX.

%files ib-efa
%{_libdir}/ucx/libuct_ib_efa.so.*
%endif

%if %{with mad}
%package mad
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX Infiniband MAD support
Group: System Environment/Libraries

%description mad
Provide Infiniband MAD support for UCX. Enables running perftest using
Infiniband datagrams for out-of-band communications.

%files mad
%{_libdir}/ucx/libucx_perftest_mad.so.*
%endif

%if %{with knem}
%package knem
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX KNEM transport support
Group: System Environment/Libraries

%description knem
Provides KNEM (fast inter-process copy) transport for UCX. KNEM is a Linux
kernel module that enables high-performance intra-node MPI communication
for large messages.

%files knem
%{_libdir}/ucx/libuct_knem.so.*
%endif

%if %{with rdmacm}
%package rdmacm
Requires: %{name}-ib%{?_isa} = %{version}-%{release}
Summary: UCX RDMA connection manager support
Group: System Environment/Libraries

%description rdmacm
Provides RDMA connection-manager support to UCX, which enables client/server
based connection establishment for RDMA-capable transports.

%files rdmacm
%{_libdir}/ucx/libuct_rdmacm.so.*
%endif

%if %{with rocm}
%package rocm
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX ROCm GPU support
Group: System Environment/Libraries

%description rocm
Provides Radeon Open Compute (ROCm) Runtime support for UCX.

%files rocm
%{_libdir}/ucx/libuct_rocm.so.*
%{_libdir}/ucx/libucm_rocm.so.*

%if %{with gdrcopy}
%package rocmgdr
Requires: %{name}-rocm%{?_isa} = %{version}-%{release}
Summary: UCX GDRCopy support for ROCM
Group: System Environment/Libraries

%description rocmgdr
Provide GDRCopy support for UCX ROCM. GDRCopy is a low-latency GPU memory copy
library, built on top of the NVIDIA GPUDirect RDMA technology.

%files rocmgdr
%{_libdir}/ucx/libuct_rocm_gdr.so.*
%endif
%endif

%if %{with ugni}
%package ugni
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX Gemini/Aries transport support.
Group: System Environment/Libraries

%description ugni
Provides Gemini/Aries transport for UCX.

%files ugni
%{_libdir}/ucx/libuct_ugni.so.*
%endif

%if %{with xpmem}
%package xpmem
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX XPMEM transport support.
Group: System Environment/Libraries

%description xpmem
Provides XPMEM transport for UCX. XPMEM is a Linux kernel module that enables a
process to map the memory of another process into its virtual address space.

%files xpmem
%{_libdir}/ucx/libuct_xpmem.so.*
%endif

%if %{with vfs}
%package vfs
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX Virtual Filesystem support.
Group: System Environment/Libraries

%description vfs
Provides a virtual filesystem over FUSE which allows real-time monitoring of UCX
library internals, protocol objects, transports status, and more.

%files vfs
%{_libdir}/ucx/libucs_fuse.so.*
%{_bindir}/ucx_vfs
%endif

%if %{with ze}
%package ze
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX ZE GPU support
Group: System Environment/Libraries

%description ze
Provides oneAPI Level Zero (ZE) Runtime support for UCX.

%files ze
%{_libdir}/ucx/libuct_ze.so.*
%{_libdir}/ucx/libucm_ze.so.*
%endif

%if %{with cuda} && %{with mlx5} && %{with gda}
%package ib-mlx5-gda
Requires: %{name}-cuda%{?_isa} = %{version}-%{release}
Requires: %{name}-ib%{?_isa} = %{version}-%{release}
Summary: UCX GPU Direct Async support
Group: System Environment/Libraries

%description ib-mlx5-gda
Provide GPU Direct Async support for UCX. GPU Direct Async allows GPU kernels
to initiate network communications directly without explicit synchronization
with the host CPU.

%files ib-mlx5-gda
%{_libdir}/ucx/libuct_ib_mlx5_gda.*
%{_includedir}/uct/ib/mlx5/gdaki/*
%endif

%changelog
* Mon Oct 20 2025 Leonid Genkin <lgenkin@nvidia.com> 1.21.0-1
- Bump version to 1.21.0
* Fri Apr 11 2025 Yossi Itigin <yosefe@nvidia.com> 1.20.0-1
- Bump version to 1.20.0
* Sat Oct 12 2024 Yossi Itigin <yosefe@nvidia.com> 1.19.0-1
- Bump version to 1.19.0
* Fri Apr 19 2024 Yossi Itigin <yosefe@nvidia.com> 1.18.0-1
- Bump version to 1.18.0
* Tue Oct 31 2023 Yossi Itigin <yosefe@nvidia.com> 1.17.0-1
- Bump version to 1.17.0
* Fri Apr 28 2023 Yossi Itigin <yosefe@nvidia.com> 1.16.0-1
- Bump version to 1.16.0
* Mon Oct 24 2022 Yossi Itigin <yosefe@mellanox.com> 1.15.0-1
- Bump version to 1.15.0
* Sat Apr 16 2022 Yossi Itigin <yosefe@mellanox.com> 1.14.0-1
- Bump version to 1.14.0
* Wed Nov 10 2021 Yossi Itigin <yosefe@mellanox.com> 1.13.0-1
- Bump version to 1.13.0
* Wed Jun 9 2021 Yossi Itigin <yosefe@mellanox.com> 1.12.0-1
- Bump version to 1.12.0
* Tue Apr 27 2021 Leonid Genkin <lgenkin@nvidia.com> 1.11.0-1
- Remove obsolete ib/cm code
* Wed Dec 16 2020 Yossi Itigin <yosefe@mellanox.com> 1.11.0-1
- Add VFS sub-package
* Wed Dec 16 2020 Yossi Itigin <yosefe@mellanox.com> 1.11.0-1
- Bump version to 1.11.0
* Wed Nov 11 2020 Yossi Itigin <yosefe@mellanox.com> 1.10.0-1
- Make the RPM relocatable
* Tue Jul 07 2020 Yossi Itigin <yosefe@mellanox.com> 1.10.0-1
- Bump version to 1.10.0
* Mon Feb 10 2020 Yossi Itigin <yosefe@mellanox.com> 1.9.0-1
- Bump version to 1.9.0
* Sun Sep 22 2019 Yossi Itigin <yosefe@mellanox.com> 1.8.0-1
- Bump version to 1.8.0
* Sun Mar 24 2019 Yossi Itigin <yosefe@mellanox.com> 1.7.0-1
- Bump version to 1.7.0
* Thu Jan 24 2019 Yossi Itigin <yosefe@mellanox.com> 1.6.0-1
- Add cma, knem, and xpmem sub-packages
* Tue Nov 20 2018 Yossi Itigin <yosefe@mellanox.com> 1.6.0-1
- Bump version to 1.6.0
* Tue Nov 6 2018 Andrey Maslennikov <andreyma@mellanox.com> 1.5.0-1
- Bump version to 1.5.0
- See NEWS for details
* Tue Oct 30 2018 Andrey Maslennikov <andreyma@mellanox.com> 1.4.0-1
- See NEWS for details
* Mon Aug 20 2018 Andrey Maslennikov <andreyma@mellanox.com> 1.3.1-1
- See NEWS for details
* Thu Aug 16 2018 Andrey Maslennikov <andreyma@mellanox.com> 1.3.0-1
- Explicitly set gcc-c++ as requirements
* Wed Mar 7 2018 Andrey Maslennikov <andreyma@mellanox.com> 1.3.0-1
- See NEWS for details
* Mon Aug 21 2017 Andrey Maslennikov <andreyma@mellanox.com> 1.2.1-1
- Spec file now complies with Fedora guidelines
* Mon Jul 3 2017 Andrey Maslennikov <andreyma@mellanox.com> 1.2.0-1
- Fedora package created
