%{!?configure_options: %global configure_options %{nil}}
%bcond_without cma
%bcond_with    cuda
%bcond_with    gdrcopy
%bcond_without ib
%bcond_without rdmacm
%bcond_with    rocm
%bcond_with    ugni
%bcond_with    xpmem
%bcond_with    vfs

Summary:        UCX is a communication library implementing high-performance messaging
Name:           ucx
Version:        1.15.0
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            http://www.openucx.org
Source0:        https://github.com/openucx/%{name}/releases/download/v1.15.0/ucx-1.15.0.tar.gz


# UCX currently supports only the following architectures
ExclusiveArch: aarch64 ppc64le x86_64

%if %{defined extra_deps}
Requires: %{?extra_deps}
%endif

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gcc-c++

%if %{with cma}
BuildRequires: glibc-devel >= 2.15
%endif
%if %{with gdrcopy}
BuildRequires: gdrcopy
%endif
%if %{with ib}
BuildRequires: libibverbs-devel
%endif
%if %{with rdmacm}
BuildRequires: librdmacm-devel
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
%if "%{debug}" == "1"
BuildRequires: valgrind-devel
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

This package was built from '' branch, commit c334359.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Header files required for developing with UCX

%description devel
Provides header files and examples for developing with UCX.

%prep
%setup -q

%build
%define _with_arg()   %{expand:%%{?with_%{1}:--with-%{2}}%%{!?with_%{1}:--without-%{2}}}
%define _enable_arg() %{expand:%%{?with_%{1}:--enable-%{2}}%%{!?with_%{1}:--disable-%{2}}}
%configure --disable-optimizations \
           %{!?debug:--disable-logging} \
           %{!?debug:--disable-debug} \
           %{!?debug:--disable-assertions} \
           %{!?debug:--disable-params-check} \
           %{?debug:--with-valgrind} \
           %{?debug:--enable-profiling} \
           %{?debug:--enable-frame-pointer} \
           %{?debug:--enable-stats} \
           %{?debug:--enable-debug-data} \
           %{?debug:--enable-mt} \
           --without-go \
           --without-java \
           %_enable_arg cma cma \
           %_with_arg cuda cuda \
           %_with_arg gdrcopy gdrcopy \
           %_with_arg ib verbs \
           %_with_arg rdmacm rdmacm \
           %_with_arg rocm rocm \
           %_with_arg xpmem xpmem \
           %_with_arg vfs fuse3 \
           %_with_arg ugni ugni \
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
%{_datadir}/ucx
%exclude %{_datadir}/ucx/examples
%doc README AUTHORS NEWS
%{!?_licensedir:%global license %%doc}
%license LICENSE

%files devel
%{_includedir}/uc*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/ucx.pc
%{_libdir}/pkgconfig/ucx-uct.pc
%{_libdir}/pkgconfig/ucx-ucs.pc
%{_libdir}/cmake/ucx/*.cmake
%{_datadir}/ucx/examples

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%if %{with cma}
%package cma
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: UCX CMA support

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

%description ib
Provides support for IBTA-compliant transports for UCX. This includes RoCE,
InfiniBand, OmniPath, and any other transport supported by IB Verbs API.
Typically these transports provide RDMA support, which enables a fast and
hardware-offloaded data transfer.

%files ib
%{_libdir}/ucx/libuct_ib.so.*
%endif

%if %{with rdmacm}
%package rdmacm
Requires: %{name}-ib%{?_isa} = %{version}-%{release}
Summary: UCX RDMA connection manager support

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

%description rocm
Provides Radeon Open Compute (ROCm) Runtime support for UCX.

%files rocm
%{_libdir}/ucx/libuct_rocm.so.*
%{_libdir}/ucx/libucm_rocm.so.*

%if %{with gdrcopy}
%package rocmgdr
Requires: %{name}-rocm%{?_isa} = %{version}-%{release}
Summary: UCX GDRCopy support for ROCM

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

%description ugni
Provides Gemini/Aries transport for UCX.

%files ugni
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

%changelog
* Wed Jan 24 2024 Juan Camposeco <juanarturoc@microsoft.com> - 1.15.0-5
- Update version to 1.15.0 and remove knem dependency

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.11.0-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue Jul 26 2022 Rachel Menge <rachelmenge@microsoft.com> - 1.11.0-3
- Move from SPECS-EXTENDED to SPECS
- License verified

* Thu Aug 26 2021 Thomas Crain <thcrain@microsoft.com> - 1.11.0-2
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Remove option to build with libibcm

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
