# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?suse_version}
# 15.6
# rocm-runtime.x86_64: E: shlib-policy-name-error (Badness: 10000) libhsa-runtime64-1
# Your package contains a single shared library but is not named after its SONAME.
%global runtime_name libhsa-runtime64-1
%else
%global runtime_name rocm-runtime
%endif
%global forge_name rocm-runtime

#Image support is x86 only
%ifarch x86_64
%global enableimage 1
%endif
%global rocm_release 6.4
%global rocm_patch 2
%global rocm_version %{rocm_release}.%{rocm_patch}

%bcond_without kfdtest

%bcond_with compat_gcc
%if %{with compat_gcc}
%global compat_gcc_major 13
%global gcc_major_str -13
%else
%global compat_gcc_major %{nil}
%global gcc_major_str %{nil}
%endif

Name:       %{runtime_name}
Version:    %{rocm_version}
Release: 4%{?dist}
Summary:    ROCm Runtime Library

License:    NCSA
URL:        https://github.com/ROCm/ROCR-Runtime
Source0:    %{url}/archive/rocm-%{version}.tar.gz#/%{forge_name}-%{version}.tar.gz

# Depends on
# https://github.com/torvalds/linux/commit/15bd4958fe38e763bc17b607ba55155254a01f55
# Look for 'queue cwsr size 0x%x not sufficient for node cwsr size' in
# drivers/gpu/drm/amd/amdkfd/kfd_queue.c
Patch:      0001-hsakmt-bump-vgpr-count-for-gfx1151-1807-1986.patch

ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  gcc%{compat_gcc_major}-c++
BuildRequires:  libdrm-devel
BuildRequires:  libffi-devel
BuildRequires:  rocm-llvm-static
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-device-libs
BuildRequires:  libzstd-devel

%if 0%{?suse_version}
BuildRequires:  libelf-devel
BuildRequires:  libnuma-devel
BuildRequires:  zlib-devel
%if %{suse_version} > 1500
BuildRequires:  xxd
%else
BuildRequires:  vim
%endif
%else
BuildRequires:  elfutils-libelf-devel
BuildRequires:  numactl-devel
BuildRequires:  vim-common
%endif

Provides:   rocm-runtime = %{version}-%{release}
Obsoletes:  hsakmt < 6.3
Provides:   hsakmt = %{version}-%{release}

%description
The ROCm Runtime Library is a thin, user-mode API that exposes the necessary
interfaces to access and interact with graphics hardware driven by the AMDGPU
driver set and the AMDKFD kernel driver. Together they enable programmers to
directly harness the power of AMD discrete graphics devices by allowing host
applications to launch compute kernels directly to the graphics hardware.

%package devel
Summary: ROCm Runtime development files
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides:  hsakmt-devel = %{version}-%{release}
Obsoletes: hsakmt-devel < 6.3
Provides:  rocm-runtime-devel = %{version}-%{release}

%description devel
ROCm Runtime development files

%if %{with kfdtest}
%package -n kfdtest
Summary: Test suite for ROCm's KFD kernel module
Requires: rocm-smi

%description -n kfdtest
This package includes ROCm's KFD kernel module test suite (kfdtest), the list of
excluded tests for each ASIC, and a convenience script to run the test suite.
%endif

%prep
%autosetup -n ROCR-Runtime-rocm-%{version} -p3

# Use llvm's static libs kfdtest
sed -i -e 's@LLVM_LINK_LLVM_DYLIB@0@' libhsakmt/tests/kfdtest/CMakeLists.txt

# gcc 15 include cstdint
sed -i '/#include <memory>.*/a#include <cstdint>' runtime/hsa-runtime/core/inc/amd_elf_image.hpp

%build

export PATH=%{rocmllvm_bindir}:$PATH

export CC=/usr/bin/gcc%{gcc_major_str}
export CXX=/usr/bin/g++%{gcc_major_str}

%cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DCMAKE_INSTALL_LIBDIR=%{_lib} \
    -DCMAKE_SHARED_LINKER_FLAGS=-ldrm_amdgpu \
    -DINCLUDE_PATH_COMPATIBILITY=OFF \
    %{?!enableimage:-DIMAGE_SUPPORT=OFF}
%cmake_build

%if %{with kfdtest}
%if 0%{?suse_version}
cd ..
export LIBHSAKMT_PATH=$(pwd)/build/libhsakmt/archive
%else
export LIBHSAKMT_PATH=$(pwd)/%__cmake_builddir/libhsakmt/archive
%endif
cd libhsakmt/tests/kfdtest
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_SKIP_RPATH=ON -DLLVM_DIR=%{rocmllvm_cmakedir}
%cmake_build

%endif

%install
%cmake_install

%if %{with kfdtest}
cd libhsakmt/tests/kfdtest
%cmake_install
%endif

if [ -f %{buildroot}%{_prefix}/share/doc/hsa-runtime64/LICENSE.md ]; then
    rm %{buildroot}%{_prefix}/share/doc/hsa-runtime64/LICENSE.md
elif [ -f %{buildroot}%{_prefix}/share/doc/packages/%{name}/LICENSE.md ]; then
    rm %{buildroot}%{_prefix}/share/doc/packages/%{name}/LICENSE.md
fi

if [ -f %{buildroot}%{_libdir}/libhsakmt.a ]; then
    rm %{buildroot}%{_libdir}/libhsakmt.a
fi
if [ -f %{buildroot}%{_libdir}/libhsakmt.so ]; then
    rm %{buildroot}%{_libdir}/libhsakmt.*
fi
if [ -d %{buildroot}%{_includedir}/hsakmt ]; then
    rm -rf %{buildroot}%{_includedir}/hsakmt
fi
if [ -d %{buildroot}%{_libdir}/cmake/hsakmt ]; then
    rm -rf %{buildroot}%{_libdir}/cmake/hsakmt
fi
if [ -f %{buildroot}%{_libdir}/pkgconfig/libhsakmt.pc ]; then
    rm %{buildroot}%{_libdir}/pkgconfig/libhsakmt.pc
fi

%ldconfig_scriptlets

%files
%doc README.md
%license LICENSE.txt
%{_libdir}/libhsa-runtime64.so.1{,.*}

%files devel
%{_includedir}/hsa/
%{_libdir}/libhsa-runtime64.so
%{_libdir}/cmake/hsa-runtime64/

%if %{with kfdtest}
%files -n kfdtest
%doc libhsakmt/tests/kfdtest/README.txt
%license libhsakmt/tests/kfdtest/LICENSE.kfdtest
%{_bindir}/kfdtest
%{_bindir}/run_kfdtest.sh
%{_datadir}/kfdtest
%endif

%changelog
* Mon Dec 8 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Fix misreported gfx1151 memory size

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Thu May 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.1-1
- Update to 6.4.1

* Wed Apr 16 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.0-1
- Update to 6.4.0

* Thu Mar 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.2-5
- Build kfdtest for SUSE

* Thu Mar 13 2025 Christian Goll <cgoll@suse.com> - 6.3.2-4
- Explicit require zlib-devel for SLE 15.6

* Tue Mar 04 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 6.3.2-3
- Fix the upgrade path for hsakmt-devel

* Sun Feb 9 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.2-2
- Fix SLE 15.6

* Sun Feb 2 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.2-1
- Update to 6.3.2

* Sat Jan 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-3
- gcc 15 include cstdint

* Thu Jan 9 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-2
- Use compat gcc

* Sun Dec 22 2024 Tom Rix <Tom.Rix@amc.com> - 6.3.1-1
- Update to 6.3.1

* Fri Dec 20 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- Link kfdtest with static llvm libs

* Sat Dec 7 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 3 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed

