# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?configure_options: %global configure_options %{nil}}
%bcond_without cma
%bcond_with    cuda
%bcond_with    gdrcopy
%bcond_without ib
%bcond_with    knem
%bcond_without rdmacm
%bcond_with    ugni
%bcond_with    xpmem
%bcond_with    vfs
%bcond_with    mad
%bcond_without mlx5

%ifarch x86_64
%if 0%{?fedora} <= 42
%bcond_with rocm
%else
%bcond_without rocm
%endif
%else
%bcond_with rocm
%endif

Name: ucx
Version: 1.18.1
Release: 3%{?dist}
Summary: UCX is a communication library implementing high-performance messaging

License: BSD-3-Clause AND MIT AND CC-PDDC AND (BSD-3-Clause OR Apache-2.0)
# CC-PDDC
# src/ucm/ptmalloc286/malloc-2.8.6.h
# src/ucm/ptmalloc286/malloc.c
# MIT
# src/ucs/datastruct/khash.h
# BSD-3-Clause or Apache-2.0
# src/ucs/arch/aarch64/memcpy_thunderx2.S
# BSD-3-Clause
# All other files

URL: http://www.openucx.org
Source: https://github.com/openucx/%{name}/releases/download/v%{version}/ucx-%{version}.tar.gz
# TOOLS/PERF: Include omp.h outside of extern C declarations
Patch0: https://github.com/openucx/%{name}/pull/10664.patch


BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Prefix: %{_prefix}

# UCX currently supports only the following architectures
ExclusiveArch: aarch64 ppc64le x86_64 riscv64

%if %{defined extra_deps}
Requires: %{?extra_deps}
%endif

BuildRequires: automake autoconf libtool gcc-c++
%if "%{_vendor}" == "suse"
BuildRequires: libnuma-devel
%else
BuildRequires: numactl-devel
%endif
%if %{with cma}
BuildRequires: glibc-devel >= 2.15
%endif
%if %{with gdrcopy}
BuildRequires: gdrcopy
%endif
%if %{with ib}
BuildRequires: libibverbs-devel
%endif
%if %{with mlx5}
BuildRequires: rdma-core-devel
%endif
%if %{with knem}
BuildRequires: knem
%endif
%if %{with rdmacm}
BuildRequires: librdmacm-devel
%endif
%if %{with rocm}
BuildRequires: rocm-hip-devel
BuildRequires: chrpath
%endif
%if %{with xpmem}
BuildRequires: xpmem-devel
%endif
%if %{with vfs}
BuildRequires: fuse3-devel
%endif
%if %{with mad}
BuildRequires: libibmad-devel libibumad-devel
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


%if "%{_vendor}" == "suse"
%debug_package
%endif

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Header files required for developing with UCX

%description devel
Provides header files and examples for developing with UCX.

%prep
%setup -q
%patch -P0 -p1
# https://github.com/openucx/ucx/issues/10542
# With ROCm 6.3+ libhsakmt is bundled with libhsa-runtime64
# Remove this nonexistent library
sed -i 's@-lhsakmt@@' config/m4/rocm.m4

autoreconf -fiv
# https://github.com/openucx/ucx/commit/b0a275a5492125a13020cd095fe9934e0b5e7c6a
# can be removed on release after 1.17.0
sed -i '/#include <limits.h>/a #include <math.h>' src/ucs/time/time.h

%build
# may be fixed in 1.19.0
%set_build_flags
export CFLAGS="$CFLAGS -std=gnu17"

%define _with_arg()   %{expand:%%{?with_%{1}:--with-%{2}}%%{!?with_%{1}:--without-%{2}}}
%define _enable_arg() %{expand:%%{?with_%{1}:--enable-%{2}}%%{!?with_%{1}:--disable-%{2}}}
%configure --disable-optimizations \
           --disable-logging \
           --disable-debug \
           --disable-assertions \
           --disable-params-check \
           --without-java \
%if %{with rocm}
           --with-rocm=%{_prefix} \
%endif
           %_enable_arg cma cma \
           %_with_arg cuda cuda \
           %_with_arg gdrcopy gdrcopy \
           %_with_arg ib verbs \
           %_with_arg mlx5 mlx5 \
           %_with_arg knem knem \
           %_with_arg rdmacm rdmacm \
           %_with_arg xpmem xpmem \
           %_with_arg vfs fuse3 \
           %_with_arg ugni ugni \
           %_with_arg mad mad \
           %{?configure_options}
make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/ucx/*.la
rm -f %{buildroot}%{_libdir}/ucx/lib*.so
rm -f %{buildroot}%{_libdir}/ucx/lib*.a

%if %{with rocm}
# ERROR   0002: file '/usr/lib64/ucx/libucx_perftest_rocm.so.0.0.0' contains an
# invalid runpath '/usr/hip/lib' in [/usr/hip/lib:/usr/lib:/usr/lib64]
# Build is confused, assumes rocm is part of AMD's release to /opt/rocm/hip/lib
# We install ROCm to system locations, so rpath is not needed, delete them
chrpath -d %{buildroot}%{_libdir}/ucx/libucx_perftest_rocm.so.0.0.0
chrpath -d %{buildroot}%{_libdir}/ucx/libucm_rocm.so.0.0.0
chrpath -d %{buildroot}%{_libdir}/ucx/libuct_rocm.so.0.0.0
%endif

%files
%{_libdir}/lib*.so.*
%{_bindir}/ucx_info
%{_bindir}/ucx_perftest
%{_bindir}/ucx_perftest_daemon
%{_bindir}/ucx_read_profile
%{_bindir}/io_demo
%{_datadir}/ucx
%dir %{_sysconfdir}/ucx
%{_sysconfdir}/ucx/ucx.conf
%exclude %{_datadir}/ucx/examples
%doc README AUTHORS NEWS
%{!?_licensedir:%global license %%doc}
%license LICENSE

%files devel
%{_includedir}/uc*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/ucx*.pc
%dir %{_libdir}/cmake/ucx
%{_libdir}/cmake/ucx/*.cmake
%{_datadir}/ucx/examples


%if %{with cma}
%package cma
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX CMA support

%description cma
Provides CMA (Linux cross-memory-attach) transport for UCX. It utilizes the
system calls process_vm_readv/writev() for one-shot memory copy from another
process.

%files cma
%dir %{_libdir}/ucx
%{_libdir}/ucx/libuct_cma.so.*
%endif

%if %{with cuda}
%package cuda
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX CUDA support

%description cuda
Provide CUDA (NVIDIA GPU) support for UCX. Enables passing GPU memory pointers
to UCX communication routines, and transports taking advantage of GPU-Direct
technology for direct data transfer between GPU and RDMA devices.

%files cuda
%dir %{_libdir}/ucx
%{_libdir}/ucx/libucx_perftest_cuda.so.*
%{_libdir}/ucx/libucm_cuda.so.*
%{_libdir}/ucx/libuct_cuda.so.*
%endif

%if %{with gdrcopy}
%package gdrcopy
Requires: %{name}-cuda%{?_isa} = %{version}-%{release}
Summary: UCX GDRCopy support

%description gdrcopy
Provide GDRCopy support for UCX. GDRCopy is a low-latency GPU memory copy
library, built on top of the NVIDIA GPUDirect RDMA technology.

%files gdrcopy
%dir %{_libdir}/ucx
%{_libdir}/ucx/libuct_cuda_gdrcopy.so.*
%endif

%if %{with ib}
%package ib
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX RDMA support

%description ib
Provides support for IBTA-compliant transports for UCX. This includes RoCE,
InfiniBand, OmniPath, and any other transport supported by IB Verbs API.
Typically these transports provide RDMA support, which enables a fast and
hardware-offloaded data transfer.

%files ib
%dir %{_libdir}/ucx
%{_libdir}/ucx/libuct_ib.so.*
%endif

%if %{with knem}
%package knem
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX KNEM transport support

%description knem
Provides KNEM (fast inter-process copy) transport for UCX. KNEM is a Linux
kernel module that enables high-performance intra-node MPI communication
for large messages.

%files knem
%dir %{_libdir}/ucx
%{_libdir}/ucx/libuct_knem.so.*
%endif

%if %{with rdmacm}
%package rdmacm
Requires: %{name}-ib%{?_isa} = %{version}-%{release}
Requires: ucx-ib = %{version}-%{release}
Summary: UCX RDMA connection manager support

%description rdmacm
Provides RDMA connection-manager support to UCX, which enables client/server
based connection establishment for RDMA-capable transports.

%files rdmacm
%dir %{_libdir}/ucx
%{_libdir}/ucx/libuct_rdmacm.so.*
%endif

%if %{with rocm}
%package rocm
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX ROCm GPU support

%description rocm
Provides Radeon Open Compute (ROCm) Runtime support for UCX.

%files rocm
%dir %{_libdir}/ucx
%{_libdir}/ucx/libucm_rocm.so.*
%{_libdir}/ucx/libuct_rocm.so.*
%{_libdir}/ucx/libucx_perftest_rocm.so.*

%if %{with gdrcopy}
%package rocmgdr
Requires: %{name}-rocm%{?_isa} = %{version}-%{release}
Summary: UCX GDRCopy support for ROCM

%description rocmgdr
Provide GDRCopy support for UCX ROCM. GDRCopy is a low-latency GPU
memory copy library, built on top of the NVIDIA GPUDirect RDMA
technology.

%files rocmgdr
%dir %{_libdir}/ucx
%{_libdir}/ucx/libuct_rocm_gdr.so.*
%endif
%endif

%if %{with ugni}
%package ugni
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX Gemini/Aries transport support.

%description ugni
Provides Gemini/Aries transport for UCX.

%files ugni
%dir %{_libdir}/ucx
%{_libdir}/ucx/libuct_ugni.so.*
%endif

%if %{with xpmem}
%package xpmem
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX XPMEM transport support.

%description xpmem
Provides XPMEM transport for UCX. XPMEM is a Linux kernel module that enables a
process to map the memory of another process into its virtual address space.

%files xpmem
%dir %{_libdir}/ucx
%{_libdir}/ucx/libuct_xpmem.so.*
%endif

%if %{with vfs}
%package vfs
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX Virtual Filesystem support.

%description vfs
Provides a virtual filesystem over FUSE which allows real-time
monitoring of UCX library internals, protocol objects, transports
status, and more.

%files vfs
%dir %{_libdir}/ucx
%{_libdir}/ucx/libucs_fuse.so.*
%{_bindir}/ucx_vfs
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

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 25 2025 Kamal Heib <kheib@redhat.com> - 1.18.1-1
- Update to version 1.18.1
- Resolves: rhbz#2328935

* Sun Mar 9 2025 Tom Rix <Tom.Rix@amd.com> - 1.17.0-5
- ROCm is part of Fedora, so build it.

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 30 2024 David Abdurachmanov <davidlt@rivosinc.com> - 1.17.0-3
- Enable riscv64

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 27 2024 Benson Muite <benson_muite@emailplus.org> - 1.17.0-1
- Upgrade to new release bz2280815

* Sat Apr 27 2024 Benson Muite <benson_muite@emailplus.org> - 1.16.0-1
- Upgrade to new release bz2256073

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 24 2023 Benson Muite <benson_muite@emailplus.org> - 1.15.0-1
- Upgrade to new release

* Sun Dec 24 2023 Benson Muite <benson_muite@emailplus.org> - 1.14.1-5
- Add patch to separate C and C++ flags from yselkowitz

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Benson Muite <benson_muite@emailplus.org> - 1.14.1-3
- Apply fix to enable building with GCC13

* Fri Jun 02 2023 Benson Muite <benson_muite@emailplus.org> - 1.14.1-2
- Remove changes in patches that have been applied

* Fri Jun 02 2023 Kamal Heib <kheib@redhat.com> - 1.14.1-1
- Update to upstream release 1.14.1

* Sun Feb 19 2023 Benson Muite <benson_muite@emailplus.org> - 1.13.1-4
- List additional licenses used
- Remove unneeded ldconfig calls

* Sat Feb 18 2023 Benson Muite <benson_muite@emailplus.org> - 1.13.1-3
- Fix type declaration error
- Fix to enable use of GCC 13
- Use SPDX license identifier
- Fix build requires #RBZ2166925

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 24 2022 Benson Muite <benson_muite@emailplus.org> - 1.13.1-1
- Update to upstream release 1.13.0

* Wed Aug 03 2022 Michal Schmidt <mschmidt@redhat.com> - 1.13.0-3
- Update to upstream release 1.13.0
- Drop autogen.sh call. Upstream tarball does not have it anymore.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 13 2021 Honggang Li <honli@redhat.com> - 1.12.0-1
- Bump version to 1.12.0

* Mon Nov 01 2021 Honggang Li <honli@redhat.com> - 1.11.2-1
- Bump version to 1.11.2

* Mon Aug 09 2021 Yurii Shestakov <yuriis@nvidia.com> 1.11.0-1
- Bump version to 1.11.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Yurii Shestakov <yuriis@nvidia.com> 1.10.1-2
- Bump version to 1.10.1

* Mon Apr 26 2021 Yurii Shestakov <yuriis@nvidia.com> 1.10.1-rc1
- Bump version to 1.10.1-rc1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Yossi Itigin <yosefe@mellanox.com> 1.10.0-1
- Make the RPM relocatable

* Mon Nov  2 2020 Orion Poplawski <orion@nwra.com> - 1.9.0-1
- Update to 1.9.0

* Fri Oct 30 2020 Jeff Law <law@redhat.com> 1.8.1-5
- Adjust workaround for gcc-11 diagnostic to narrow its scope

* Thu Oct 29 2020 Jeff Law <law@redhat.com> 1.8.1-4
- Disable -Warray-bounds diagnostics for gcc-11

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Jeff Law <law@redhat.com> 1.8.1-2
- Fix broken configure files compromised by LTO

* Wed Jul 1 2020 Yossi Itigin <yosefe@mellanox.com> 1.8.1-1
- Bump version to 1.8.1

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
