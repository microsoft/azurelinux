# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?suse_version}
%global hipblaslt_name libhipblaslt0
%else
%global hipblaslt_name hipblaslt
%endif

%if 0%{?suse_version}
%{?sle15_python_module_pythons}
%{?!python_module:%define python_module() python3-%{**}}
%else
%define python_exec python3
%define python_expand python3
%endif

%global upstreamname hipBLASLt
%global rocm_release 6.4
%global rocm_patch 3
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/')

# Fortran is only used in testing
# clang and gfortran fedora toolchain args do not mix
%global build_fflags %{nil}

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

# hipblaslt does not support our default set
#
# build is timing out, remove some of the ISA targets
# gfx942;gfx1102
%global amdgpu_targets "gfx90a:xnack+;gfx90a:xnack-;gfx1100;gfx1101;gfx1103;gfx1150;gfx1151;gfx1200;gfx1201"

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

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

Name:           %{hipblaslt_name}
Version:        %{rocm_version}
Release:        1%{?dist}
Summary:        ROCm general matrix operations beyond BLAS
Url:            https://github.com/ROCmSoftwarePlatform/%{upstreamname}
License:        MIT

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz
# https://github.com/ROCm/hipBLASLt/issues/1959
Patch0:         0001-hipblaslt-find-toolchain.patch
# https://github.com/ROCm/hipBLASLt/issues/1960
Patch1:         0001-hipblaslt-handle-missing-joblib.patch
# https://github.com/ROCm/hipBLASLt/issues/2060
# https://github.com/AngryLoki/gentoo/blob/b211598514d2876dcbc75ae86d1dd24898f61cab/sci-libs/hipBLASLt/files/hipBLASLt-6.4.1-upstream-clang.patch
Patch2:         hipBLASLt-6.4.1-upstream-clang.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  hipblas-devel
BuildRequires:  hipcc
BuildRequires:  libzstd-devel
BuildRequires:  rocblas-devel
BuildRequires:  rocminfo
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-llvm-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-smi-devel
BuildRequires:  roctracer-devel
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
%else
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(pyyaml)
%if 0%{?rhel}
%global tensile_verbose 2
%else
%global tensile_verbose 1
BuildRequires:  python3dist(joblib)
%endif
# https://github.com/ROCm/hipBLASLt/issues/1734
BuildRequires:  python3dist(msgpack)
BuildRequires:  msgpack-devel
%endif

%if %{with test}
BuildRequires:  blas-static
BuildRequires:  gcc-gfortran
BuildRequires:  gtest-devel
BuildRequires:  gmock-devel
BuildRequires:  lapack-static
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

Provides:       hipblaslt = %{version}-%{release}
Provides:       bundled(python-tensile) = %{tensile_version}

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
Provides:       hipblaslt-devel = %{version}-%{release}

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
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

# Suse obs times out
# print out command in scripts
%if 0%{?suse_version}
sed -i '2i set -x'                                                             tensilelite/Tensile/Ops/gen_assembly.sh
sed -i '2i set -x'                                                             library/src/amd_detail/rocblaslt/src/kernels/compile_code_object.sh
%endif

# Remove venv
sed -i -e 's@. ${venv}/bin/activate@@'                                         tensilelite/Tensile/Ops/gen_assembly.sh
sed -i -e 's@deactivate@@'                                                     tensilelite/Tensile/Ops/gen_assembly.sh
# Change some paths in Common.py
# change rocm path from /opt/rocm to /usr
# need to be able to find hipcc, rocm-smi, extractkernel, rocm_agent_enumerator
sed -i -e 's@opt/rocm@usr@'                                                    tensilelite/Tensile/Common.py
# Use PATH to find where TensileGetPath and other tensile bins are
sed -i -e 's@${Tensile_PREFIX}/bin/TensileGetPath@TensileGetPath@g'            tensilelite/Tensile/cmake/TensileConfig.cmake

# defer to cmdline
sed -i -e 's@set(CMAKE_INSTALL_LIBDIR@#set(CMAKE_INSTALL_LIBDIR@' CMakeLists.txt
# Do not use virtualenv_install
sed -i -e 's@virtualenv_install@#virtualenv_install@'                          CMakeLists.txt
# do not mess with prefix path
sed -i -e 's@APPEND CMAKE_PREFIX_PATH@APPEND NO_CMAKE_PREFIX_PATH@'            CMakeLists.txt

# For debugging
# set threads to 1
# sed -i -e 's@default=-1@default=1@'                                          tensilelite/Tensile/TensileCreateLibrary.py
# sed -i -e 's@return cpu_count@return 1@'                                     tensilelite/Tensile/Parallel.py
# Print things
# sed -i -e 's@if globalParameters["PrintCodeCommands"]:@if True:@'            tensilelite/Tensile/TensileCreateLibrary.py
# sed -i -e 's@#print@print@'                                                  tensilelite/Tensile/Parallel.py

%if %{with test}
# Remove problem libraries, why are we linking gfortran AND flang ?
sed -i -e 's@-lgfortran -lflang -lflangrti@-lgfortran@'                        clients/gtest/CMakeLists.txt
%endif

%if 0%{?suse_version} >= 1600
sed -i -e 's@msgpack REQUIRED@msgpack-cxx REQUIRED@' tensilelite/Tensile/Source/lib/CMakeLists.txt
%endif

%if 0%{?sle_version} == 150600
sed -i 's@#!/usr/bin/env python3@#!/usr/bin/python3.11@' tensilelite/Tensile/bin/Tensile*
sed -i 's@python3@python3.11@'  clients/common/hipblaslt_gentest.py cmake/virtualenv.cmake tensilelite/Tensile/Ops/gen_assembly.sh 
%endif

sed -i 's@find_package(LLVM REQUIRED CONFIG)@find_package(LLVM REQUIRED CONFIG PATHS "%{rocmllvm_cmakedir}")@' tensilelite/Tensile/Source/lib/CMakeLists.txt

# Reduce requirements
sed -i -e '/joblib/d' tensilelite/requirements.*

# As of 6.4, there is a long poll
# compile_code_object.sh gfx90a,gfx1100,gfx1101,gfx1151,gfx1200,gfx1201 RelWithDebInfo sha1 hipblasltTransform.hsaco
# This compiles a large file with multiple gpus.
GPUS=`echo %{amdgpu_targets} | grep -o 'gfx' | wc -l`

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
sed -i -e "s@--offload-arch@-parallel-jobs=${HIP_JOBS} --offload-arch@" library/src/amd_detail/rocblaslt/src/kernels/compile_code_object.sh

%build

# Do a manual install instead of cmake's virtualenv
cd tensilelite
TL=$PWD

%python_exec setup.py install --root $TL
cd ..

# Should not have to do this
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

# Use ld.lld to work around a problem with ld
%cmake %{cmake_generator} \
       -DAMDGPU_TARGETS=%{amdgpu_targets} \
       -DBUILD_CLIENTS_TESTS=%{build_test} \
       -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
       -DBUILD_VERBOSE=ON \
       -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DCMAKE_INSTALL_LIBDIR=%{_lib} \
       -DCMAKE_C_COMPILER=%{rocmllvm_bindir}/clang \
       -DCMAKE_CXX_COMPILER=%{rocmllvm_bindir}/clang++ \
       -DCMAKE_CXX_FLAGS="-fuse-ld=%{rocmllvm_bindir}/ld.lld" \
       -DCMAKE_VERBOSE_MAKEFILE=ON \
       -DHIP_PLATFORM=amd \
       -DROCM_SYMLINK_LIBS=OFF \
       -DBUILD_WITH_TENSILE=ON \
       -DTensile_COMPILER=%{rocmllvm_bindir}/clang++ \
       -DTensile_LIBRARY_FORMAT=msgpack \
       -DTensile_VERBOSE=%{tensile_verbose} \
       -DVIRTUALENV_BIN_DIR=%{_bindir} \
%if 0%{?sle_version} == 150600
       -DPYTHON_EXECUTABLE:FILEPATH=python3.11 \
%endif
       %{nil}

%cmake_build

%install
%cmake_install

if [ -f %{buildroot}%{_prefix}/share/doc/hipblaslt/LICENSE.md ]; then
    rm %{buildroot}%{_prefix}/share/doc/hipblaslt/LICENSE.md
fi

%post  -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%dir %{_libdir}/cmake/hipblaslt/
%dir %{_libdir}/hipblaslt/
%dir %{_libdir}/hipblaslt/library/
%license LICENSE.md
%{_libdir}/libhipblaslt.so.*
%{_libdir}/hipblaslt/library/*

%files devel
%doc README.md
%{_includedir}/hipblaslt
%{_libdir}/cmake/hipblaslt/
%{_libdir}/libhipblaslt.so

%if %{with test}
%files test
%{_bindir}/hipblaslt*
%endif

%changelog
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

