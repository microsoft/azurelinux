# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?suse_version}
%global rccl_name librccl1
%else
%global rccl_name rccl
%endif

%global upstreamname RCCL
%global rocm_release 6.4
%global rocm_patch 2
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-flto=thin//' -e 's/-mtls-dialect=gnu2//')

%global _lto_cflags %{nil}

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

# downloads tests, use mock --enable-network
%bcond_with test
%if %{with test}
%global build_test ON
%global __brp_check_rpaths %{nil}
%else
%global build_test OFF
%endif

%bcond_with export
%if %{with export}
%global build_compile_db ON
%else
%global build_compile_db OFF
%endif

# rccl is not supported on gfx1103
# On 6.1.1
# lld: error: ld-temp.o <inline asm>:1:25: specified hardware register is not supported on this GPU
#        s_getreg_b32 s1, hwreg(HW_REG_HW_ID)
#
# On 6.2
# Problems reported with gfx10, removing gfx10 and default (gfx10 and gfx11) from build list
#

Name:           %{rccl_name}
Version:        %{rocm_version}
Release:        5%{?dist}
Summary:        ROCm Communication Collectives Library

Url:            https://github.com/ROCm/rccl
License:        BSD-3-Clause AND MIT AND Apache-2.0
# From License.txt the main license is BSD 3
# Modifications from Microsoft is MIT
# The NVIDIA based header files below are Apache-2.0
#  src/include/nvtx3/nv*.h and similar
# The URL for NVIDIA in the License.txt https://github.com/NVIDIA/NVTX is Apache-2.0

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  hipify
BuildRequires:  gcc-c++
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-core-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-smi-devel

%if %{with test}
%if 0%{?suse_version}
BuildRequires:  gtest
%else
BuildRequires:  gtest-devel
%endif
%endif

Requires:       %{name}-data = %{version}-%{release}
Provides:       rccl = %{version}-%{release}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
RCCL (pronounced "Rickle") is a stand-alone library of standard
collective communication routines for GPUs, implementing all-reduce,
all-gather, reduce, broadcast, reduce-scatter, gather, scatter, and
all-to-all. There is also initial support for direct GPU-to-GPU
send and receive operations. It has been optimized to achieve high
bandwidth on platforms using PCIe, xGMI as well as networking using
InfiniBand Verbs or TCP/IP sockets. RCCL supports an arbitrary
number of GPUs installed in a single node or multiple nodes, and
can be used in either single- or multi-process (e.g., MPI)
applications.

The collective operations are implemented using ring and tree
algorithms and have been optimized for throughput and latency. For
best performance, small operations can be either batched into
larger operations or aggregated through the API.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary:        Headers and libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       rccl-devel = %{version}-%{release}

%description devel
Headers and libraries for %{name}

%package data
Summary:        Data for %{name}
BuildArch:      noarch

%description data
Data for %{name}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%autosetup -p1 -n rccl-rocm-%{version}

# Allow user to set AMDGPU_TARGETS
sed -i -e '/AMD GPU targets to compile for/d' CMakeLists.txt

# No /opt/rocm/.info/version
sed -i -e 's@cat ${ROCM_PATH}/.info/version@echo %{rocm_version}@' CMakeLists.txt

# wrong path
# https://github.com/ROCm/rccl/issues/1649
sed -i -e 's@rocm-core/rocm_version.h@rocm_version.h@' src/include/hip_rocm_version_info.h

# Problems building on SUSE
# ENABLE_MSCCLPP=OFF
sed -i -e 's@if (ENABLE_MSCCLPP AND NOT(${HOST_OS_ID} STREQUAL "ubuntu" OR ${HOST_OS_ID} STREQUAL "centos"))@if (ENABLE_MSCCLPP)@' CMakeLists.txt

# Building --with test
# .../test/common/TestBed.cpp:607:16: error: no member named 'setfill' in namespace 'std'
#   607 |     ss << std::setfill(' ') << std::setw(20) << ncclFuncNames[funcType] << " ";
# https://github.com/ROCm/rccl/issues/1749
sed -i '/#include <map.*/a#include <iomanip>' test/common/TestBed.hpp

# On Tumbleweed Q3,2025
# /usr/include/gtest/internal/gtest-port.h:273:2: error: C++ versions less than C++17 are not supported.
# Convert the c++14 to c++17
sed -i -e 's@set(CMAKE_CXX_STANDARD   14)@set(CMAKE_CXX_STANDARD 17)@' CMakeLists.txt

# RCCL uses -parallel-jobs for both compiling and linking
# compiling is set to 12, which may be more than the cores on the build machine.
# linking is set by reserving 16GB pre thread, can be too little.
# Use our own heuristics here
# Real cores, No hyperthreading
COMPILE_JOBS=`cat /proc/cpuinfo | grep -m 1 'cpu cores' | awk '{ print $4 }'`
if [ ${COMPILE_JOBS}x = x ]; then
    COMPILE_JOBS=1
fi
# Try again..
if [ ${COMPILE_JOBS} = 1 ]; then
    COMPILE_JOBS=`lscpu | grep '^CPU(s)' | awk '{ print $2 }'`
    if [ ${COMPILE_JOBS}x = x ]; then
        COMPILE_JOBS=4
    fi
fi

# Take into account memmory usage per core, do not thrash real memory
# inflate this to prevent competing with normal compile jobs
BUILD_MEM=16
MEM_KB=0
MEM_KB=`cat /proc/meminfo | grep MemTotal | awk '{ print $2 }'`
MEM_MB=`eval "expr ${MEM_KB} / 1024"`
MEM_GB=`eval "expr ${MEM_MB} / 1024"`
COMPILE_JOBS_MEM=`eval "expr 1 + ${MEM_GB} / ${BUILD_MEM}"`
if [ "$COMPILE_JOBS_MEM" -lt "$COMPILE_JOBS" ]; then
    COMPILE_JOBS=$COMPILE_JOBS_MEM
fi
LINK_MEM=24
LINK_JOBS=`eval "expr 1 + ${MEM_GB} / ${LINK_MEM}"`

sed -i -e "s@rccl PRIVATE -parallel-jobs=12@rccl PRIVATE -parallel-jobs=${COMPILE_JOBS}@" CMakeLists.txt
sed -i -e "s@-parallel-jobs=\${num_linker_jobs}@-parallel-jobs=${LINK_JOBS}@" CMakeLists.txt

%build
%cmake \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_rccl} \
    -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
    -DBUILD_TESTS=%{build_test} \
    -DCMAKE_BUILD_TYPE=%{build_type} \
    -DCMAKE_C_COMPILER=/usr/bin/hipcc \
    -DCMAKE_CXX_COMPILER=/usr/bin/hipcc \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=%{build_compile_db} \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_SKIP_RPATH=ON \
    -DENABLE_MSCCLPP=OFF \
    -DHIP_PLATFORM=amd \
    -DRCCL_ROCPROFILER_REGISTER=OFF \
    -DROCM_PATH=%{_prefix} \
    -DROCM_SYMLINK_LIBS=OFF

%cmake_build

%install
%cmake_install

if [ -f %{buildroot}%{_prefix}/share/doc/rccl/LICENSE.txt ]; then
    rm %{buildroot}%{_prefix}/share/doc/rccl/LICENSE.txt
fi

%files
%license LICENSE.txt
%{_libdir}/librccl.so.*

%files data
%dir %{_datadir}/rccl
%dir %{_datadir}/rccl/msccl-algorithms
%dir %{_datadir}/rccl/msccl-unit-test-algorithms
%{_datadir}/rccl/msccl-algorithms/*.xml
%{_datadir}/rccl/msccl-unit-test-algorithms/*.xml

%files devel
%doc README.md
%dir %{_includedir}/rccl
%dir %{_libdir}/cmake/rccl
%{_includedir}/rccl/*
%{_libdir}/cmake/rccl/*.cmake
%{_libdir}/librccl.so

%if %{with test}
%files test
%{_bindir}/rccl-UnitTests
%endif

%changelog
* Mon Aug 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-5
- Fine tune parallel jobs

* Thu Aug 14 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-4
- build --with test on SUSE
- Remove multibuild file generation

* Tue Jul 29 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Remove -mtls-dialect cflag

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Tue Jun 17 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-3
- Fix builds test subpackage

* Sun Jun 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-2
- Remove suse check on ldconfig

* Thu May 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.1-1
- Update to 6.4.1

* Wed Apr 23 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Fix suse

* Fri Apr 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Thu Feb 13 2025 Tom Rix <Tom.Rix@amd.com> 6.3.2-3
- Use rpm macros gpu list
- Fix SLE 15.6

* Wed Feb 5 2025 Tom Rix <Tom.Rix@amd.com> 6.3.2-2
- Fix TW build

* Wed Jan 29 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.2-1
- Update to 6.3.2

* Sat Jan 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-3
- Add gfx1200,gfx1201

* Fri Dec 27 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- Add --with export
- Remove unneeded requires rocm-rpm-macros-modules

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3


