# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Copyright Fedora Project Authors.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
%if 0%{!?suse_version:1}
%define python_exec python3
%define python_expand python3
%endif

%bcond_with gitcommit
%if %{with gitcommit}
%global commit0 2584e35062ad9c2edb68d93c464cf157bc57e3b0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20250926
%endif

%global upstreamname hipblaslt
%global rocm_release 7.1
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

%bcond_with compat
%if %{with compat}
%global pkg_libdir lib
%global pkg_prefix %{_prefix}/lib64/rocm/rocm-%{rocm_release}
%global pkg_suffix -%{rocm_release}
%global pkg_module rocm%{pkg_suffix}
%else
%global pkg_libdir %{_lib}
%global pkg_prefix %{_prefix}
%global pkg_suffix %{nil}
%global pkg_module default
%endif
%if 0%{?suse_version}
%global hipblaslt_name libhipblaslt0%{pkg_suffix}
%else
%global hipblaslt_name hipblaslt%{pkg_suffix}
%endif

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-mtls-dialect=gnu2//')

# Fortran is only used in testing
# clang and gfortran fedora toolchain args do not mix
%global build_fflags %{nil}

# Reduce link memory pressure
%global _lto_cflags %{nil}

# may run out of memory for both compile and link
# Calculate a good -j number below
%global _smp_mflags %{nil}

# gfx90a: 10343 pass, 152 fail
%bcond_with test
# Disable rpatch checks for a local build
%if %{with test}
%global __brp_check_rpaths %{nil}
%global build_test ON
%else
%global build_test OFF
%endif

%global tensile_version 4.33.0
# The upstream hipBLASTLt project has a hard fork of the python-tensile package
# The rocBLAS uses.  The two versions are incompatible.  It appears that the
# fork happened around version 4.33.0.  Unfortunately hipBLASLt can no longer be
# build without using this fork.
# https://github.com/ROCm/hipBLASLt/issues/535
# The problem with the fork has been raised here.
# https://github.com/ROCm/hipBLASLt/issues/908

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

# hipblaslt does not support our default set
%global gpu_list %{rocm_gpu_list_hipblaslt}
# For testing
%global _gpu_list "gfx1100"

# Use ninja if it is available
# Ninja is available on suse but obs times out with ninja build, make doesn't
%if 0%{?fedora}
%bcond_without ninja
%else
%bcond_with ninja
%endif

%if %{with ninja}
%global cmake_generator -G Ninja
%else
%global cmake_generator %{nil}
%endif

# Request for python-nanobind on EPEL
# https://bugzilla.redhat.com/show_bug.cgi?id=2402409
%if 0%{?fedora}
%bcond_without nanobind
%else
%bcond_with nanobind
%endif

Name:           %{hipblaslt_name}
%if %{with gitcommit}
Version:        git%{date0}.%{shortcommit0}
Release:        2%{?dist}
%else
Version:        %{rocm_version}
Release:        7%{?dist}
%endif
Summary:        ROCm general matrix operations beyond BLAS
License:        MIT AND BSD-3-Clause
URL:            https://github.com/ROCm/rocm-libraries

%if %{with gitcommit}
Source0:        %{url}/archive/%{commit0}/rocm-libraries-%{shortcommit0}.tar.gz
%else
Source0:        %{url}/releases/download/rocm-%{version}/%{upstreamname}.tar.gz#/%{upstreamname}-%{version}.tar.gz
%endif

%global nanobind_version 2.9.2
%global nanobind_giturl https://github.com/wjakob/nanobind
Source1:        %{nanobind_giturl}/archive/v%{nanobind_version}/nanobind-%{nanobind_version}.tar.gz
%global robinmap_version 1.3.0
%global robinmap_giturl https://github.com/Tessil/robin-map
Source2:        %{robinmap_giturl}/archive/v%{robinmap_version}/robin-map-%{robinmap_version}.tar.gz

# yappi was removed from fedora
# yappi is used in tensilelite to generate profiling data, we are not using that in the build
Patch1:         0001-hipblaslt-tensilelite-remove-yappi-dependency.patch
# change hard coded vendor paths to fedoras
Patch2:         0001-hipblaslt-tensilelite-use-fedora-paths.patch
# https://github.com/ROCm/rocm-libraries/issues/2422
Patch3:         0001-hipblaslt-find-origami-package.patch
# do not try to fetch, point to the nanobind tarball
Patch4:         0001-hipblaslt-tensilelite-use-nanobind-tarball.patch
# compile and link jobpools
Patch5:         0001-hipblaslt-cmake-compile-and-link-pools.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  hipblas%{pkg_suffix}-devel
BuildRequires:  hipcc%{pkg_suffix}
BuildRequires:  libzstd-devel
BuildRequires:  rocblas%{pkg_suffix}-devel
BuildRequires:  rocminfo%{pkg_suffix}
BuildRequires:  rocm-cmake%{pkg_suffix}
BuildRequires:  rocm-comgr%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-llvm%{pkg_suffix}-devel
BuildRequires:  rocm-origami%{pkg_suffix}-devel
BuildRequires:  rocm-runtime%{pkg_suffix}-devel
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocm-smi%{pkg_suffix}-devel
BuildRequires:  zlib-devel

# For tensilelite
%if 0%{?suse_version}
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module joblib}
BuildRequires:  %{python_module msgpack}
BuildRequires:  %{python_module PyYAML}
BuildRequires:  %{python_module setuptools}
BuildRequires:  msgpack-cxx-devel
%global tensile_verbose 2
BuildRequires:  %{python_module dataclasses if %python-base < 3.11}
BuildRequires:  %{python_module ujson}
BuildRequires:  %{python_module distro}
BuildRequires:  %{python_module simplejson}
%else
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pyyaml)
%if %{with nanobind}
BuildRequires:  python3dist(nanobind)
%endif
%global tensile_verbose 1
BuildRequires:  python3dist(joblib)
# https://github.com/ROCm/hipBLASLt/issues/1734
BuildRequires:  python3dist(msgpack)
BuildRequires:  msgpack-devel
%endif

%if %{with test}
BuildRequires:  blis-devel
BuildRequires:  lapack-devel
%if 0%{?suse_version}
BuildRequires:  gmock
BuildRequires:  gtest
%else
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
%endif
%endif

%if %{with ninja}
%if 0%{?fedora}
BuildRequires:  ninja-build
%endif
%if 0%{?suse_version}
BuildRequires:  ninja
%define __builder ninja
%endif
%endif

Provides:       hipblaslt%{pkg_suffix} = %{version}-%{release}
Provides:       bundled(python-tensile) = %{tensile_version}

%if %{without nanobind}
# BSD-3-Clause
Provides:       bundled(nanobind) = %{nanobind_version}
Provides:       bundled(robin-map) = %{robinmap_version}
%endif

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
hipBLASLt is a library that provides general matrix-matrix
operations. It has a flexible API that extends functionalities
beyond a traditional BLAS library, such as adding flexibility
to matrix data layouts, input types, compute types, and
algorithmic implementations and heuristics.

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       hipblaslt%{pkg_suffix}-devel = %{version}-%{release}

%description devel
%{summary}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%if %{with gitcommit}
%setup -q -n rocm-libraries-%{commit0}
cd projects/hipblaslt
%patch -P1 -p1
%patch -P2 -p1
%else
%autosetup -p1 -n %{upstreamname}
%endif

# Use PATH to find where TensileGetPath and other tensile bins are
sed -i -e 's@${Tensile_PREFIX}/bin/TensileGetPath@TensileGetPath@g'            tensilelite/Tensile/cmake/TensileConfig.cmake

# defer to cmdline
sed -i -e 's@set(CMAKE_INSTALL_LIBDIR@#set(CMAKE_INSTALL_LIBDIR@' CMakeLists.txt

# Do not use virtualenv_install
sed -i -e 's@virtualenv_install@#virtualenv_install@'                          CMakeLists.txt

# Disable trying to download rocm-cmake
sed -i -e 's@if(NOT ROCmCMakeBuildTools_FOUND)@if(FALSE)@' cmake/dependencies.cmake

%if %{with nanobind}
# Disable download of nanobind
sed -i -e 's@FetchContent_MakeAvailable(nanobind)@find_package(nanobind)@' tensilelite/rocisa/CMakeLists.txt
%else
# Use bundled nanobind
tar xf %{SOURCE1}
mv nanobind-* nanobind
cd nanobind
tar xf %{SOURCE2}
cp -r robin-map-*/* ext/robin_map/
cd ..
tar czf nanobind.tar.gz nanobind
%endif

# As of 6.4, there is a long poll
# compile_code_object.sh gfx90a,gfx1100,gfx1101,gfx1151,gfx1200,gfx1201 RelWithDebInfo sha1 hipblasltTransform.hsaco
# This compiles a large file with multiple gpus.
GPUS=`echo %{gpu_list} | grep -o 'gfx' | wc -l`

HIP_JOBS=`lscpu | grep 'Core(s)' | awk '{ print $4 }'`
if [ ${HIP_JOBS}x = x ]; then
    HIP_JOBS=1
fi
# Try again..
if [ ${HIP_JOBS} = 1 ]; then
    HIP_JOBS=`lscpu | grep '^CPU(s)' | awk '{ print $2 }'`
    if [ ${HIP_JOBS}x = x ]; then
        HIP_JOBS=4
    fi
fi
if [ "$GPUS" -lt "$HIP_JOBS" ]; then
    HIP_JOBS=$GPUS
fi

# HIPBLASLT_ENABLE_OPENMP is OFF yet it is still being used
# https://github.com/ROCm/rocm-libraries/issues/3201
sed -i -e '/OpenMP::OpenMP_CXX/d' clients/CMakeLists.txt
sed -i -e '/omp/d'                clients/common/src/blis_interface.cpp
sed -i -e '/#include <omp.h>/d'   clients/common/include/testing_matmul.hpp
sed -i -e '/#include <omp.h>/d'   clients/common/include/hipblaslt_init.hpp
sed -i -e '/#include <omp.h>/d'   clients/common/src/cblas_interface.cpp

# We are building from a tarball, not a git repo
sed -i -e 's@find_package(Git REQUIRED)@#find_package(Git REQUIRED)@' cmake/dependencies.cmake

%build
%if %{with gitcommit}
cd projects/hipblaslt
%endif

# Do a manual install instead of cmake's virtualenv
cd tensilelite
TL=$PWD

%python_exec setup.py install --root $TL
cd ..

# Should not have to do this
export PATH=%{pkg_prefix}/bin:$PATH
CLANG_PATH=`hipconfig --hipclangpath`
ROCM_CLANG=${CLANG_PATH}/clang
RESOURCE_DIR=`${ROCM_CLANG} -print-resource-dir`
export DEVICE_LIB_PATH=${RESOURCE_DIR}/amdgcn/bitcode
export TENSILE_ROCM_ASSEMBLER_PATH=${CLANG_PATH}/clang++
export TENSILE_ROCM_OFFLOAD_BUNDLER_PATH=${CLANG_PATH}/clang-offload-bundler

# Look for the just built tensilelite
export PATH=${TL}/%{_bindir}:$PATH
%if 0%{?suse_version}
%{python_expand} export PYTHONPATH=${TL}%{python_sitelib}:$PYTHONPATH
%{python_expand} export Tensile_DIR=${TL}%{python_sitelib}/Tensile
%else
export PYTHONPATH=${TL}%{python3_sitelib}:$PYTHONPATH
export Tensile_DIR=${TL}%{python3_sitelib}/Tensile
%endif
# Uncomment and see if the path is sane
# TensileGetPath

cat /proc/cpuinfo
cat /proc/meminfo
lscpu

# Real cores, No hyperthreading
COMPILE_JOBS=`lscpu | grep 'Core(s)' | awk '{ print $4 }'`
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
BUILD_MEM=8
MEM_KB=0
MEM_KB=`cat /proc/meminfo | grep MemTotal | awk '{ print $2 }'`
MEM_MB=`eval "expr ${MEM_KB} / 1024"`
MEM_GB=`eval "expr ${MEM_MB} / 1024"`
COMPILE_JOBS_MEM=`eval "expr 1 + ${MEM_GB} / ${BUILD_MEM}"`
if [ "$COMPILE_JOBS_MEM" -lt "$COMPILE_JOBS" ]; then
    COMPILE_JOBS=$COMPILE_JOBS_MEM
fi
LINK_MEM=32
LINK_JOBS=`eval "expr 1 + ${MEM_GB} / ${LINK_MEM}"`
JOBS=${COMPILE_JOBS}
if [ "$LINK_JOBS" -lt "$JOBS" ]; then
    JOBS=$LINK_JOBS
fi

%cmake %{cmake_generator} \
       -DGPU_TARGETS=%{gpu_list} \
       -DBLIS_INCLUDE_DIR=%{_includedir}/blis \
       -DBLIS_LIB=%{_libdir}/libblis.so \
       -DBUILD_CLIENTS_TESTS=%{build_test} \
       -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
       -DBUILD_VERBOSE=ON \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_C_COMPILER=%{rocmllvm_bindir}/amdclang \
       -DCMAKE_CXX_COMPILER=%{rocmllvm_bindir}/amdclang++ \
       -DCMAKE_INSTALL_LIBDIR=%{pkg_libdir} \
       -DCMAKE_INSTALL_PREFIX=%{pkg_prefix} \
       -DCMAKE_PREFIX_PATH=%{python3_sitelib}/nanobind \
       -DCMAKE_VERBOSE_MAKEFILE=ON \
       -DHIP_PLATFORM=amd \
       -DHIPBLASLT_ENABLE_CLIENT=%{build_test} \
       -DHIPBLASLT_ENABLE_MARKER=OFF \
       -DHIPBLASLT_ENABLE_OPENMP=OFF \
       -DHIPBLASLT_ENABLE_ROCROLLER=OFF \
       -DHIPBLASLT_ENABLE_SAMPLES=OFF \
       -DROCM_SYMLINK_LIBS=OFF \
       -DTensile_LIBRARY_FORMAT=msgpack \
       -DTensile_VERBOSE=%{tensile_verbose} \
       -DVIRTUALENV_BIN_DIR=%{_bindir} \
       -DHIPBLASLT_PARALLEL_COMPILE_JOBS=${COMPILE_JOBS} \
       -DHIPBLASLT_PARALLEL_LINK_JOBS=${LINK_JOBS} \
       %{nil}

%cmake_build

%install
%if %{with gitcommit}
cd projects/hipblaslt
%endif

%cmake_install

# Extra license
rm -f %{buildroot}%{pkg_prefix}/share/doc/hipblaslt/LICENSE.md

%post  -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%if %{with gitcommit}
%doc projects/hipblaslt/README.md
%license projects/hipblaslt/LICENSE.md
%else
%doc README.md
%license LICENSE.md
%endif

%{pkg_prefix}/%{pkg_libdir}/libhipblaslt.so.*
%{pkg_prefix}/%{pkg_libdir}/hipblaslt/

%files devel
%{pkg_prefix}/include/hipblaslt/
%{pkg_prefix}/include/hipblaslt-export.h
%{pkg_prefix}/include/hipblaslt-version.h
%{pkg_prefix}/%{pkg_libdir}/cmake/hipblaslt/
%{pkg_prefix}/%{pkg_libdir}/libhipblaslt.so

%if %{with test}
%files test
%{pkg_prefix}/bin/hipblaslt*
%{pkg_prefix}/bin/sequence.yaml
%endif

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Dec 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-6
- Remove build requires git

* Thu Dec 25 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-5
- Add --with compat

* Sat Dec 13 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-4
- Fix fortran buildrequires on SUSE

* Sun Dec 7 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-3
- Add compile and link job pools

* Sat Dec 6 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-2
- Use blis-devel for testing
- Use GPU_TARGETS

* Thu Nov 27 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-1
- Update to 7.1.1

* Sun Nov 23 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-3
- Bundle nanobind for EPEL

* Thu Nov 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Remove dir tags

* Sat Nov 1 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Sat Oct 11 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.2-1
- Update to 7.0.2

* Wed Oct 8 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-2
- Use joblib on RHEL

* Thu Sep 25 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-1
- Update to 7.0.1

* Thu Aug 28 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.3-5
- Add Fedora copyright

* Sun Aug 24 2025 Egbert Eich <eich@suse.com> - 6.4.3-4
- On SUSE use code from python-tensile to check for msgpack.

* Wed Aug 20 2025 Egbert Eich <eich@suse.com> - 6.4.3-3
- On SLE-15 exclusively use python 3.6.
  This is since joblib is not even available on PackageHub.
- On SUSE check for msgpack-cxx instead of msgpack.

* Wed Aug 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.3-2
- Remove roctracer
- Build on EPEL

* Thu Aug 7 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.3-1
- Update to 6.4.3
- Add gfx1103,gfx1150,gfx1151 targets

* Thu Jul 24 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 17 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-4
- Use Gentoo fix for gfx12*

* Sun Jun 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-3
- Remove suse check of ldconfig

* Mon Jun 9 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-2
- Fix fedora build dependencies

* Thu May 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.1-1
- Update to 6.4.1

* Fri May 9 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-4
- Document gfx1201 failure

* Wed May 7 2025 Tim Flink <tflink@fedoraproject.org> - 6.4.0-3
- put gfx1100;gfx1101 back into build target list

* Thu May 1 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Reduce gpu set to 6.3
- mitigate suse build timeout

* Sat Apr 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Thu Apr 10 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-12
- Reenable ninja

* Fri Mar 7 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-11
- msgpack is manditory

* Mon Mar 3 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-10
- Add tensile format and verbose args similar to roblas

* Sun Mar 2 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-9
- format consistent with other rocm packages

* Sun Mar 2 2025 Christian Goll <cgoll@suse.de> - 6.3.1-8
- Fix all builds

* Thu Feb 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-7
- Fix fedora

* Tue Feb 25 2025 Christian Goll <cgoll@suse.com> - 6.3.1-6
- use python3.11 for 15.6 builds

* Mon Feb 17 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-5
- Fix for TW

* Thu Jan 23 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-4
- Add gfx1200,gfx1201
- multithread compress

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-2
- build requires gcc-c++

* Mon Dec 23 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.1-1
- Update to 6.3.1

* Wed Dec 11 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

