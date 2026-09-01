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
%bcond_with gitcommit
%if %{with gitcommit}
%global commit0 de5c1aebb641af098d9310a9fcca5591a7c066c8
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20251015
%endif

%global upstreamname rocblas
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
%global rocblas_name librocblas5%{pkg_suffix}
%else
%global rocblas_name rocblas%{pkg_suffix}
%endif

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-mtls-dialect=gnu2//')

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

%bcond_without compress
%if %{with compress}
%global build_compress ON
%else
%global build_compress OFF
%endif

%if 0%{?fedora}
%bcond_without test
%else
%bcond_with test
%endif
%if %{with test}
%global build_test ON
%else
%global build_test OFF
%endif

# Option to test suite for testing on real HW:
# May have to set gpu under test with
# export HIP_VISIBLE_DEVICES=<num> - 0, 1 etc.
%bcond_with check

%bcond_without tensile
%if %{with tensile}
%global build_tensile ON
%else
%global build_tensile OFF
%endif

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

# SUSE/OSB times out because -O is added to the make args
# This accumulates all the output from the long running tensile
# jobs.
%global _make_output_sync %{nil}

# OracleLinux 9 has a problem with it's strip not recognizing *.co's
%global __strip %rocmllvm_bindir/llvm-strip

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

%global cmake_config \\\
  -DBLAS_INCLUDE_DIR=%{_includedir}/%{blaslib} \\\
  -DBLAS_LIBRARY=%{blaslib} \\\
  -DBUILD_CLIENTS_BENCHMARKS=%{build_test} \\\
  -DBUILD_CLIENTS_TESTS=%{build_test} \\\
  -DBUILD_CLIENTS_TESTS_OPENMP=OFF \\\
  -DBUILD_FORTRAN_CLIENTS=OFF \\\
  -DBUILD_OFFLOAD_COMPRESS=%{build_compress} \\\
  -DBUILD_WITH_PIP=OFF \\\
  -DBUILD_WITH_TENSILE=%{build_tensile} \\\
  -DBUILD_WITH_HIPBLASLT=OFF \\\
  -DCMAKE_AR=%rocmllvm_bindir/llvm-ar \\\
  -DCMAKE_BUILD_TYPE=%{build_type} \\\
  -DCMAKE_C_COMPILER=%rocmllvm_bindir/amdclang \\\
  -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/amdclang++ \\\
  -DCMAKE_INSTALL_LIBDIR=%{pkg_libdir} \\\
  -DCMAKE_INSTALL_PREFIX=%{pkg_prefix} \\\
  -DCMAKE_LINKER=%rocmllvm_bindir/ld.lld \\\
  -DCMAKE_RANLIB=%rocmllvm_bindir/llvm-ranlib \\\
  -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \\\
  -DCMAKE_SKIP_RPATH=ON \\\
  -DCMAKE_VERBOSE_MAKEFILE=ON \\\
  -DGPU_TARGETS=%{gpu_list} \\\
  -DROCM_SYMLINK_LIBS=OFF \\\
  -DHIP_PLATFORM=amd \\\
  -DTensile_CPU_THREADS=${CORES} \\\
  -DTensile_DIR=${TP}/cmake \\\
  -DTensile_LIBRARY_FORMAT=%{tensile_library_format} \\\
  -DTensile_ROOT=${TP} \\\
  -DTensile_VERBOSE=%{tensile_verbose}

%global gpu_list %{rocm_gpu_list_default}
%global _gpu_list gfx1100

%if %{with compat}
%bcond_without bundled_tensile
%else
%if 0%{?suse_version}
%bcond_without bundled_tensile
%else
%bcond_with bundled_tensile
%endif
%endif

Name:           rocblas%{pkg_suffix}
Summary:        BLAS implementation for ROCm
License:        MIT AND BSD-3-Clause
URL:            https://github.com/ROCm/rocm-libraries

%if %{with gitcommit}
Version:        git%{date0}.%{shortcommit0}
Release:        3%{?dist}
Source0:        %{url}/archive/%{commit0}/rocm-libraries-%{shortcommit0}.tar.gz
%else
Version:        %{rocm_version}
Release:        7%{?dist}
Source0:        %{url}/releases/download/rocm-%{version}/%{upstreamname}.tar.gz#/%{upstreamname}-%{version}.tar.gz
%endif

Patch1:         0001-fixup-install-of-tensile-output.patch

# Bundled tensile
Source1:        https://github.com/ROCmSoftwarePlatform/Tensile/archive/rocm-%{version}.tar.gz#/Tensile-%{version}.tar.gz
Patch101:       0001-tensile-fedora-gpus.patch
Patch102:       0001-tensile-gfx1153.patch
Patch103:       0001-tensile-set-default-paths.patch
Patch104:       0001-tensile-ignore-cache-check.patch
Patch105:       0001-tensile-add-cmake-arches.patch
Patch106:       0001-tensile-gfx1036.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocminfo%{pkg_suffix}
BuildRequires:  rocm-cmake%{pkg_suffix}
BuildRequires:  rocm-comgr%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-runtime%{pkg_suffix}-devel
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocm-rpm-macros%{pkg_suffix}-modules

%if %{with tensile}
%if 0%{?suse_version}
%if 0%{?suse_version} <= 1600
%global tensile_library_format yaml
%else
%global tensile_library_format msgpack
%endif
# OBS vm times out without console output
%global tensile_verbose 2
%else
%global tensile_verbose 1
%global tensile_library_format msgpack
# suse_version
%endif 
%else
%global tensile_verbose %{nil}
%global tensile_library_format %{nil}
# tensile
%endif

%if %{with tensile}
%if %{with bundled_tensile}
%if 0%{?suse_version}
BuildRequires:  python-rpm-macros
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module joblib}
BuildRequires:  %{python_module msgpack}
BuildRequires:  %{python_module PyYAML}
BuildRequires:  %{python_module setuptools}
%if 0%{?suse_version} <= 1600
%else
BuildRequires:  msgpack-cxx-devel
# suse version <= 1600
%endif
%else
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  msgpack-devel
%if 0%{?fedora} || 0%{?rhel} > 9
BuildRequires:  python3dist(joblib)
%endif
BuildRequires:  python3dist(msgpack)
BuildRequires:  python3dist(pyyaml)
# suse version
%endif
%else
%if 0%{?suse_version}
%if 0%{?suse_version} <= 1600
%else
BuildRequires:  msgpack-cxx-devel
# suse version <= 1600
%endif
BuildRequires: %{python_module tensile-devel}
BuildRequires: %{python_module joblib}
%else
BuildRequires:  python3dist(tensile)
BuildRequires:  msgpack-devel
# suse_version
%endif
# bundled_tensile
%endif
# tensile
%endif

%if %{with compress}
BuildRequires:  pkgconfig(libzstd)
%endif

%if %{with test}

BuildRequires:  libomp-devel
BuildRequires:  rocminfo%{pkg_suffix}
BuildRequires:  rocm-smi%{pkg_suffix}-devel

%if 0%{?suse_version}
BuildRequires:  openblas-devel
BuildRequires:  gtest
BuildRequires:  gcc-fortran
BuildRequires: %{python_module PyYAML}
%global blaslib openblas
%else
BuildRequires:  gcc-gfortran
BuildRequires:  gtest-devel
BuildRequires:  python3dist(pyyaml)
%if 0%{?rhel}
BuildRequires:  flexiblas-devel
%global blaslib flexiblas
%else
BuildRequires:  blas-devel
%global blaslib cblas
%endif
%endif
%endif

%if %{with ninja}
%if 0%{?fedora} || 0%{?rhel}
BuildRequires:  ninja-build
%endif
%if 0%{?suse_version}
BuildRequires:  ninja
%define __builder ninja
%endif
%endif

Provides:       rocblas%{pkg_suffix} = %{version}-%{release}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
rocBLAS is the AMD library for Basic Linear Algebra Subprograms
(BLAS) on the ROCm platform. It is implemented in the HIP
programming language and optimized for AMD GPUs.

%if 0%{?suse_version}
%package -n %{rocblas_name}
Summary:        Shared libraries for %{name}

%description -n %{rocblas_name}
%{summary}

%ldconfig_scriptlets -n %{rocblas_name}
%endif

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{rocblas_name}%{?_isa} = %{version}-%{release}
%if %{without compat}
Requires:       cmake(hip)
%endif

%description devel
%{summary}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{rocblas_name}%{?_isa} = %{version}-%{release}
Requires:       diffutils

%description test
%{summary}
%endif

%prep
%if %{with gitcommit}
%setup -q -n rocm-libraries-%{commit0}
cd projects/rocblas
%patch -P1 -p1 
%else
%setup -q -n %{upstreamname}
%patch -P1 -p1
%endif

tar xf %{SOURCE1}
mv Tensile-* Tensile
cd Tensile
%patch -P101 -p1
%patch -P102 -p1
%patch -P103 -p1
%patch -P104 -p1
%patch -P105 -p1
%patch -P106 -p1

#Fix a few things:
chmod 755 Tensile/Configs/miopen/convert_cfg.py
sed -i -e 's@bin/python@bin/python3@' Tensile/Configs/miopen/convert_cfg.py
sed -i -e 's@bin/python@bin/python3@' Tensile/Tests/create_tests.py
sed -i -e 's@bin/env python3@bin/python3@' Tensile/bin/Tensile
sed -i -e 's@bin/env python3@bin/python3@' Tensile/bin/TensileCreateLibrary

# I'm assuming we don't need these:
rm -r Tensile/Configs/miopen/archives

# hack where TensileGetPath is located
sed -i -e 's@${Tensile_PREFIX}/bin/TensileGetPath@TensileGetPath@g' Tensile/cmake/TensileConfig.cmake

# Use /usr instead of /opt/rocm for prefix
# Is this needed with bundled?
sed -i -e 's@/opt/rocm@%{pkg_prefix}@g' Tensile/Common.py
sed -i -e 's@/opt/rocm@%{pkg_prefix}@g' Tensile/Tests/yaml_only/test_config.py

# Ignora asm cap
sed -i -e 's@globalParameters["IgnoreAsmCapCache"] = False@globalParameters["IgnoreAsmCapCache"] = True@' Tensile/Common.py
sed -i -e 's@arguments["IgnoreAsmCapCache"] = args.IgnoreAsmCapCache@arguments["IgnoreAsmCapCache"] = True@' Tensile/TensileCreateLibrary.py
sed -i -e 's@if not ignoreCacheCheck and derivedAsmCaps@if False and derivedAsmCaps@' Tensile/Common.py

# Reduce requirements
sed -i -e '/joblib/d' requirements.*
sed -i -e '/rich/d' requirements.*
sed -i -e '/msgpack/d' requirements.*

# Generalize prefix
sed -i -e 's@/usr/bin@%{pkg_prefix}/bin@' Tensile/Utilities/Toolchain.py
sed -i -e 's@/usr/lib64/rocm/llvm/bin@%{rocmllvm_bindir}@' Tensile/Utilities/Toolchain.py

# Make sure hip/hip_runtime.h is found
sed -i -e 's@"-D__HIP_HCC_COMPAT_MODE__=1"@"-D__HIP_HCC_COMPAT_MODE__=1","-I%{pkg_prefix}/include"@' Tensile/BuildCommands/SourceCommands.py

cd ..

sed -i -e 's@pkg_search_module(PKGBLAS cblas)@pkg_search_module(PKGBLAS %blaslib)@' clients/CMakeLists.txt
sed -i -e 's@target_link_libraries( rocblas-test PRIVATE ${BLAS_LIBRARY} ${GTEST_BOTH_LIBRARIES} roc::rocblas )@target_link_libraries( rocblas-test PRIVATE %blaslib ${GTEST_BOTH_LIBRARIES} roc::rocblas )@' clients/gtest/CMakeLists.txt

# no git in this build
sed -i -e 's@find_package(Git REQUIRED)@find_package(Git)@' library/CMakeLists.txt

# On Tumbleweed Q2,2025
# /usr/include/gtest/internal/gtest-port.h:279:2: error: C++ versions less than C++14 are not supported.
#   279 | #error C++ versions less than C++14 are not supported.
# Convert the c++11's to c++14
sed -i -e 's@CXX_STANDARD 11@CXX_STANDARD 14@' clients/samples/CMakeLists.txt

%if 0%{?suse_version}
# Suse's libgfortran.so for gcc 14 is here
# /usr/lib64/gcc/x86_64-suse-linux/14/libgfortran.so
# Without adding this path with -L, it isn't found, but thankfully it isn't really needed
sed -i -e 's@list( APPEND COMMON_LINK_LIBS "-lgfortran")@#list( APPEND COMMON_LINK_LIBS "-lgfortran")@' clients/{benchmarks,gtest}/CMakeLists.txt
%endif

%build

%if %{with tensile}
%if %{with bundled_tensile}
cd Tensile
TL=$PWD
python3 setup.py install --root $TL
TP=${TL}/usr/lib/python%{python3_version}/site-packages/Tensile/
cd ..
%else
TP=`/usr/bin/TensileGetPath`
%endif
%endif

%if %{with gitcommit}
cd projects/rocblas
%endif

CORES=`lscpu | grep 'Core(s)' | awk '{ print $4 }'`
if [ ${CORES}x = x ]; then
    CORES=1
fi
# Try again..
if [ ${CORES} = 1 ]; then
    CORES=`lscpu | grep '^CPU(s)' | awk '{ print $2 }'`
    if [ ${CORES}x = x ]; then
        CORES=4
    fi
fi

export CLANG_PATH=%{rocmllvm_bindir}
export TENSILE_ROCM_ASSEMBLER_PATH=${CLANG_PATH}/clang++
export TENSILE_ROCM_OFFLOAD_BUNDLER_PATH=${CLANG_PATH}/clang-offload-bundler
# Work around problem with koji's ld
export HIPCC_LINK_FLAGS_APPEND=-fuse-ld=lld

%cmake %{cmake_generator} %{cmake_config}

%cmake_build

%install
%if %{with gitcommit}
cd projects/rocblas
%endif

%cmake_install

rm -f %{buildroot}%{pkg_prefix}/share/doc/rocblas/LICENSE.md

%check
%if %{with test}
%if %{with check}
%if 0%{?suse_version}
export LD_LIBRARY_PATH=%{__builddir}/library/src:$LD_LIBRARY_PATH
%{__builddir}/clients/staging/rocblas-test --gtest_brief=1
%else
export LD_LIBRARY_PATH=%{_vpath_builddir}/library/src:$LD_LIBRARY_PATH
%{_vpath_builddir}/clients/staging/rocblas-test --gtest_brief=1
%endif
%endif
%endif

%files -n %{rocblas_name}
%if %{with gitcommit}
%license projects/rocblas/LICENSE.md
%doc projects/rocblas/README.md
%else
%license LICENSE.md
%doc README.md
%endif
%{pkg_prefix}/%{pkg_libdir}/librocblas.so.5{,.*}
%if %{with tensile}
%{pkg_prefix}/%{pkg_libdir}/rocblas/
%endif

%files devel
%{pkg_prefix}/include/rocblas/
%{pkg_prefix}/%{pkg_libdir}/cmake/rocblas/
%{pkg_prefix}/%{pkg_libdir}/librocblas.so

%if %{with test}
%files test
%{pkg_prefix}/bin/rocblas*
%endif

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 2 2026 Tom Rix <Tom.Rix@amd.com> - 7.1.1-6
- Fix SUSE

* Thu Jan 1 2026 Tom Rix <Tom.Rix@amd.com> - 7.1.1-5
- Fix --with bundled_tensile on RHEL

* Thu Dec 18 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-4
- Add --with compat
- Remove --with generic

* Wed Dec 17 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-3
- Add --with bundled_tensile

* Thu Dec 4 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-2
- Fix setting sw blas

* Thu Nov 27 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.1-1
- Update to 7.1.1

* Wed Nov 19 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-4
- Remove dir tags
- Fix build on SUSE 15.6

* Mon Nov 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 7.1.0-3
- Rebuilt for gtest 1.17.0

* Wed Nov 5 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Turn down verbose output on RHEL

* Thu Oct 30 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Mon Oct 27 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.2-2
- Better handling of shared library on opensuse

* Fri Oct 10 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.2-1
- Update to 7.0.2

* Mon Oct 6 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-2
- Remove setting __brp_check_rpaths to nil

* Sat Sep 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-1
- Update to 7.0.1
- Build -test on fedora

* Wed Aug 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-10
- Add Fedora copyright

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-9
- Simplify file removal

* Wed Aug 20 2025 Egbert Eich <eich@suse.com> - 6.4.2-8
- Consoldiate Python module BuildRequires for SUSE.

* Sat Aug 16 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-7
- set default build type to RelWithDebInfo

* Sat Aug 16 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-6
- Use msgpack on SUSE

* Wed Aug 13 2025 Egbert Eich <eich@suse.com> - 6.4.2-5
- Fix build and runtime dependencies of test package.
 
* Tue Aug 12 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-5
- remove roctracer
- Use distro appropriate blas libs

* Tue Jul 29 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-4
- Remove -mtls-dialect cflag

* Mon Jul 28 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Remove experimental gfx950
- Remove debian dir

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Wed Jun 11 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-8
- Remove suse check for using ldconfig

* Sun May 11 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-7
- Add experimental gfx950

* Tue May 6 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-6
- disable roctracer for everyone

* Tue Apr 29 2025 Tim Flink <tflink@fedoraproject.org> - 6.4.0-5
- add patch for option to disable roctracer logging
- disable roctracer logging for rhel builds
- allow for builds on rhel with ninja

* Tue Apr 29 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-4
- Improve testing for suse

* Sat Apr 26 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Add generic gpus

* Wed Apr 23 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Use joblib on sle 15.6 and 16.0

* Fri Apr 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Thu Apr 10 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-12
- Reenable ninja

* Fri Apr 4 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-11
- Use rocm-llvm strip

* Thu Feb 27 2025 Cristian Le <git@lecris.dev> - 6.3.0-10
- Add hip requirement to devel package

* Thu Feb 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-9
- Enable tensile for RHEL

* Wed Feb 26 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-8
- Enable tensile for SUSE

* Sun Feb 23 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-7
- Use tensile verbosity to avoid OSB timeout

* Wed Feb 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-6
- Use tensile cmake from the python location

* Tue Feb 11 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-5
- Remove multibuild
- Fix SLE 15.6

* Sat Jan 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- multithread rpm compress

* Tue Jan 14 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-3
- build requires gcc-c++

* Fri Dec 20 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- Build type should be release

* Fri Dec 6 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed


