## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name torch

# Where the src comes from
%global forgeurl https://github.com/pytorch/pytorch

# So pre releases can be tried
%bcond_with gitcommit
%if %{with gitcommit}
# v2.8.0-rc8
%global commit0 a1cb3cc05d46d198467bebbb6e8fba50a325d4e7
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20250723
%global pypi_version 2.8.0
%global flatbuffers_version 24.12.23
%global miniz_version 3.0.2
%global pybind11_version 2.13.6
%else
%global pypi_version 2.8.0
%global flatbuffers_version 24.12.23
%global miniz_version 3.0.2
%global pybind11_version 2.13.6
%endif

# For -test subpackage
# suitable only for local testing
# Install and do something like
#   export LD_LIBRARY_PATH=/usr/lib64/python3.12/site-packages/torch/lib
#   /usr/lib64/python3.12/site-packages/torch/bin/test_api, test_lazy
%bcond_with test

%ifarch x86_64
%bcond_without rocm
%endif

# For testing distributed+rccl etc.
%bcond_without rccl
%bcond_with gloo
%bcond_without mpi
%bcond_without tensorpipe

# Disable dwz with rocm because memory can be exhausted
%if %{with rocm}
%define _find_debuginfo_dwz_opts %{nil}
%endif

# These came in 2.4 and not yet in Fedora
%bcond_with opentelemetry
%bcond_with httplib
%bcond_with kineto

%if 0%{?fedora}
%bcond_without onnx
%else
%bcond_with onnx
%endif

Name:           python-%{pypi_name}
%if %{with gitcommit}
Version:        %{pypi_version}^git%{date0}.%{shortcommit0}
%else
Version:        %{pypi_version}
%endif
Release:        %autorelease
Summary:        PyTorch AI/ML framework
# See license.txt for license details
License:        BSD-3-Clause AND BSD-2-Clause AND 0BSD AND Apache-2.0 AND MIT AND BSL-1.0 AND GPL-3.0-or-later AND Zlib

URL:            https://pytorch.org/
%if %{with gitcommit}
Source0:        %{forgeurl}/archive/%{commit0}/pytorch-%{shortcommit0}.tar.gz
Source1000:     pyproject.toml
%else
Source0:        %{forgeurl}/releases/download/v%{version}/pytorch-v%{version}.tar.gz
%endif
Source1:        https://github.com/google/flatbuffers/archive/refs/tags/v%{flatbuffers_version}.tar.gz
Source2:        https://github.com/pybind/pybind11/archive/refs/tags/v%{pybind11_version}.tar.gz

# Developement on tensorpipe has stopped, repo made read only July 1, 2023, this is the last commit
%global tp_commit 52791a2fd214b2a9dc5759d36725909c1daa7f2e
%global tp_scommit %(c=%{tp_commit}; echo ${c:0:7})
Source20:       https://github.com/pytorch/tensorpipe/archive/%{tp_commit}/tensorpipe-%{tp_scommit}.tar.gz
# The old libuv tensorpipe uses
Source21:       https://github.com/libuv/libuv/archive/refs/tags/v1.41.0.tar.gz
# Developement afaik on libnop has stopped, this is the last commit
%global nop_commit 910b55815be16109f04f4180e9adee14fb4ce281
%global nop_scommit %(c=%{nop_commit}; echo ${c:0:7})
Source22:       https://github.com/google/libnop/archive/%{nop_commit}/libnop-%{nop_scommit}.tar.gz

%if %{without opentelemetry}
%global ot_ver 1.14.2
Source60:       https://github.com/open-telemetry/opentelemetry-cpp/archive/refs/tags/v%{ot_ver}.tar.gz
%endif

%if %{without httplib}
%global hl_commit 3b6597bba913d51161383657829b7e644e59c006
%global hl_scommit %(c=%{hl_commit}; echo ${c:0:7})
Source70:       https://github.com/yhirose/cpp-httplib/archive/%{hl_commit}/cpp-httplib-%{hl_scommit}.tar.gz
%endif

%if %{without kineto}
%global ki_commit 5e7501833f1021ce6f618572d3baf657b6319658
%global ki_scommit %(c=%{ki_commit}; echo ${c:0:7})
Source80:       https://github.com/pytorch/kineto/archive/%{ki_commit}/kineto-%{ki_scommit}.tar.gz
%endif

%if %{without onnx}
%global ox_ver 1.18.0
Source90:       https://github.com/onnx/onnx/archive/refs/tags/v%{ox_ver}.tar.gz
%endif

# https://github.com/pytorch/pytorch/issues/150187
Patch11:       0001-Add-cmake-variable-USE_ROCM_CK.patch
# https://github.com/pytorch/pytorch/issues/156595
# Patch12:       0001-Use-horrible-dynamo-stub.patch
Patch12:       0001-Fix-compilation-and-import-torch-issues-for-cpython-.patch

ExclusiveArch:  x86_64 aarch64
%global toolchain gcc
%global _lto_cflags %nil

BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  flexiblas-devel
BuildRequires:  fmt-devel
BuildRequires:  foxi-devel
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran

%if %{with gloo}
BuildRequires:  gloo-devel
%endif
BuildRequires:  json-devel

BuildRequires:  libomp-devel
BuildRequires:  numactl-devel
BuildRequires:  ninja-build
%if %{with onnx}
BuildRequires:  onnx-devel
%endif
%if %{with mpi}
BuildRequires:  openmpi-devel
%endif
BuildRequires:  protobuf-devel
BuildRequires:  sleef-devel
BuildRequires:  valgrind-devel
BuildRequires:  pocketfft-devel
BuildRequires:  pthreadpool-devel

BuildRequires:  cpuinfo-devel
BuildRequires:  FP16-devel
BuildRequires:  fxdiv-devel
BuildRequires:  psimd-devel
BuildRequires:  xnnpack-devel = 0.0^git20240814.312eb7e

BuildRequires:  python3-devel
BuildRequires:  python3dist(filelock)
BuildRequires:  python3dist(jinja2)
BuildRequires:  python3dist(networkx)
BuildRequires:  python3dist(numpy)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(pyyaml)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(typing-extensions)

%if 0%{?fedora}
BuildRequires:  python3-pybind11
BuildRequires:  python3dist(fsspec)
BuildRequires:  python3dist(sympy)
%endif

%if %{with rocm}
BuildRequires:  hipblas-devel
BuildRequires:  hipblaslt-devel
BuildRequires:  hipcub-devel
BuildRequires:  hipfft-devel
BuildRequires:  hiprand-devel
BuildRequires:  hipsparse-devel
BuildRequires:  hipsparselt-devel
BuildRequires:  hipsolver-devel
BuildRequires:  magma-devel
BuildRequires:  miopen-devel
BuildRequires:  rocblas-devel
BuildRequires:  rocrand-devel
BuildRequires:  rocfft-devel
%if %{with rccl}
BuildRequires:  rccl-devel
%endif
BuildRequires:  rocprim-devel
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-core-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocsolver-devel
BuildRequires:  rocm-smi-devel
BuildRequires:  rocthrust-devel
BuildRequires:  roctracer-devel

Requires:       amdsmi

%endif

%if %{with test}
BuildRequires:  google-benchmark-devel
%endif

Requires:       python3dist(dill)
Requires:       python3dist(yaml)

Obsoletes:      caffe  = 1.0^git20200212.9b89154

%description
PyTorch is a Python package that provides two high-level features:

 * Tensor computation (like NumPy) with strong GPU acceleration
 * Deep neural networks built on a tape-based autograd system

You can reuse your favorite Python packages such as NumPy, SciPy,
and Cython to extend PyTorch when needed.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

# For convience
Provides:       pytorch

# Apache-2.0
Provides:       bundled(flatbuffers) = %{flatbuffers_version}
# MIT
Provides:       bundled(miniz) = %{miniz_version}
Provides:       bundled(pybind11) = %{pybind11_version}

%if %{with tensorpipe}
# BSD-3-Clause
Provides:       bundled(tensorpipe)
# Apache-2.0
Provides:       bundled(libnop)
# MIT AND CC-BY-4.0 AND ISC AND BSD-2-Clause
Provides:       bundled(libuv) = 1.41.0
%endif

%description -n python3-%{pypi_name}
PyTorch is a Python package that provides two high-level features:

 * Tensor computation (like NumPy) with strong GPU acceleration
 * Deep neural networks built on a tape-based autograd system

You can reuse your favorite Python packages such as NumPy, SciPy,
and Cython to extend PyTorch when needed.

%if %{with test}
%package -n python3-%{pypi_name}-test
Summary:        Tests for %{name}
Requires:       python3-%{pypi_name}%{?_isa} = %{version}-%{release}

%description -n python3-%{pypi_name}-test
%{summary}
%endif


%prep

%if %{with gitcommit}
%autosetup -p1 -n pytorch-%{commit0}
# Overwrite with a git checkout of the pyproject.toml
cp %{SOURCE1000} .

%else
%autosetup -p1 -n pytorch-v%{version}
%endif

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

tar xf %{SOURCE1}
rm -rf third_party/flatbuffers/*
cp -r flatbuffers-%{flatbuffers_version}/* third_party/flatbuffers/

tar xf %{SOURCE2}
rm -rf third_party/pybind11/*
cp -r pybind11-%{pybind11_version}/* third_party/pybind11/

%if %{with tensorpipe}
tar xf %{SOURCE20}
rm -rf third_party/tensorpipe/*
cp -r tensorpipe-*/* third_party/tensorpipe/
tar xf %{SOURCE21}
rm -rf third_party/tensorpipe/third_party/libuv/*
cp -r libuv-*/* third_party/tensorpipe/third_party/libuv/
tar xf %{SOURCE22}
rm -rf third_party/tensorpipe/third_party/libnop/*
cp -r libnop-*/* third_party/tensorpipe/third_party/libnop/

# gcc 15 include cstdint
sed -i '/#include <tensorpipe.*/a#include <cstdint>' third_party/tensorpipe/tensorpipe/common/allocator.h
sed -i '/#include <tensorpipe.*/a#include <cstdint>' third_party/tensorpipe/tensorpipe/common/memory.h
%endif

%if %{without opentelemtry}
tar xf %{SOURCE60}
rm -rf third_party/opentelemetry-cpp/*
cp -r opentelemetry-cpp-*/* third_party/opentelemetry-cpp/
%endif

%if %{without httplib}
tar xf %{SOURCE70}
rm -rf third_party/cpp-httplib/*
cp -r cpp-httplib-*/* third_party/cpp-httplib/
%endif

%if %{without kineto}
tar xf %{SOURCE80}
rm -rf third_party/kineto/*
cp -r kineto-*/* third_party/kineto/
%endif

%if %{without onnx}
tar xf %{SOURCE90}
rm -rf third_party/onnx/*
cp -r onnx-*/* third_party/onnx/
%endif

# Adjust for the hipblaslt's we build
sed -i -e 's@"gfx90a", "gfx940", "gfx941", "gfx942"@"gfx90a", "gfx1103", "gfx1150", "gfx1151", "gfx1100", "gfx1101", "gfx1200", "gfx1201"@' aten/src/ATen/native/cuda/Blas.cpp

%if 0%{?rhel}
# In RHEL but too old
sed -i -e '/typing-extensions/d' setup.py
# Need to pip these
sed -i -e '/sympy/d' setup.py
sed -i -e '/fsspec/d' setup.py
%else
# for 2.5.0
sed -i -e 's@sympy==1.13.1@sympy>=1.13.1@' setup.py
%endif

# A new dependency
# Connected to USE_FLASH_ATTENTION, since this is off, do not need it
sed -i -e '/aotriton.cmake/d' cmake/Dependencies.cmake
# Compress hip
sed -i -e 's@HIP_CLANG_FLAGS -fno-gpu-rdc@HIP_CLANG_FLAGS -fno-gpu-rdc --offload-compress@' cmake/Dependencies.cmake
# Silence noisy warning
sed -i -e 's@HIP_CLANG_FLAGS -fno-gpu-rdc@HIP_CLANG_FLAGS -fno-gpu-rdc -Wno-pass-failed@' cmake/Dependencies.cmake
sed -i -e 's@HIP_CLANG_FLAGS -fno-gpu-rdc@HIP_CLANG_FLAGS -fno-gpu-rdc -Wno-unused-command-line-argument@' cmake/Dependencies.cmake
sed -i -e 's@HIP_CLANG_FLAGS -fno-gpu-rdc@HIP_CLANG_FLAGS -fno-gpu-rdc -Wno-unused-result@' cmake/Dependencies.cmake
sed -i -e 's@HIP_CLANG_FLAGS -fno-gpu-rdc@HIP_CLANG_FLAGS -fno-gpu-rdc -Wno-deprecated-declarations@' cmake/Dependencies.cmake
# Use parallel jobs
sed -i -e 's@HIP_CLANG_FLAGS -fno-gpu-rdc@HIP_CLANG_FLAGS -fno-gpu-rdc -parallel-jobs=4@' cmake/Dependencies.cmake
# Need to link with librocm_smi64
sed -i -e 's@hiprtc::hiprtc@hiprtc::hiprtc rocm_smi64@' cmake/Dependencies.cmake

# No third_party fmt, use system
sed -i -e 's@fmt::fmt-header-only@fmt@' CMakeLists.txt
sed -i -e 's@fmt::fmt-header-only@fmt@' aten/src/ATen/CMakeLists.txt
sed -i -e 's@list(APPEND ATen_HIP_INCLUDE $<TARGET_PROPERTY:fmt,INTERFACE_INCLUDE_DIRECTORIES>)@@' aten/src/ATen/CMakeLists.txt

sed -i -e 's@fmt::fmt-header-only@fmt@' third_party/kineto/libkineto/CMakeLists.txt
sed -i -e 's@fmt::fmt-header-only@fmt@' c10/CMakeLists.txt
sed -i -e 's@fmt::fmt-header-only@fmt@' torch/CMakeLists.txt
sed -i -e 's@fmt::fmt-header-only@fmt@' cmake/Dependencies.cmake
sed -i -e 's@fmt::fmt-header-only@fmt@' caffe2/CMakeLists.txt

sed -i -e 's@add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/fmt)@#add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/fmt)@' cmake/Dependencies.cmake
sed -i -e 's@set_target_properties(fmt-header-only PROPERTIES INTERFACE_COMPILE_FEATURES "")@#set_target_properties(fmt-header-only PROPERTIES INTERFACE_COMPILE_FEATURES "")@' cmake/Dependencies.cmake
sed -i -e 's@list(APPEND Caffe2_DEPENDENCY_LIBS fmt::fmt-header-only)@#list(APPEND Caffe2_DEPENDENCY_LIBS fmt::fmt-header-only)@' cmake/Dependencies.cmake

# No third_party FXdiv
sed -i -e 's@if(NOT TARGET fxdiv)@if(MSVC AND USE_XNNPACK)@' caffe2/CMakeLists.txt
sed -i -e 's@TARGET_LINK_LIBRARIES(torch_cpu PRIVATE fxdiv)@#TARGET_LINK_LIBRARIES(torch_cpu PRIVATE fxdiv)@' caffe2/CMakeLists.txt

# https://github.com/pytorch/pytorch/issues/149803
# Tries to checkout nccl
sed -i -e 's@    checkout_nccl()@    True@' tools/build_pytorch_libs.py

# Disable the use of check_submodule's in the setup.py, we are a tarball, not a git repo
sed -i -e 's@check_submodules()$@#check_submodules()@' setup.py

# Release comes fully loaded with third party src
# Remove what we can
#
# For 2.1 this is all but miniz-2.1.0
# Instead of building as a library, caffe2 reaches into
# the third_party dir to compile the file.
# mimiz is licensed MIT
# https://github.com/richgel999/miniz/blob/master/LICENSE
mv third_party/miniz-%{miniz_version} .
#
# setup.py depends on this script
mv third_party/build_bundled.py .

# Need the just untarred flatbuffers/flatbuffers.h
mv third_party/flatbuffers .

mv third_party/pybind11 .

%if %{with tensorpipe}
mv third_party/tensorpipe .
%endif

%if %{without opentelemetry}
mv third_party/opentelemetry-cpp .
%endif

%if %{without httplib}
mv third_party/cpp-httplib .
%endif

%if %{without kineto}
mv third_party/kineto .
%endif

%if %{without onnx}
mv third_party/onnx .
%endif

%if %{with test}
mv third_party/googletest .
%endif

# Remove everything
rm -rf third_party/*
# Put stuff back
mv build_bundled.py third_party
mv miniz-%{miniz_version} third_party
mv flatbuffers third_party
mv pybind11 third_party

%if %{with tensorpipe}
mv tensorpipe third_party
%endif

%if %{without opentelemetry}
mv opentelemetry-cpp third_party
%endif

%if %{without httplib}
mv cpp-httplib third_party
%endif

%if %{without kineto}
mv kineto third_party
%endif

%if %{without onnx}
mv onnx third_party
%endif

%if %{with test}
mv googletest third_party
%endif

#
# Fake out pocketfft, and system header will be used
mkdir third_party/pocketfft
cp /usr/include/pocketfft_hdronly.h third_party/pocketfft/

#
# Use the system valgrind headers
mkdir third_party/valgrind-headers
cp %{_includedir}/valgrind/* third_party/valgrind-headers

# Fix installing to /usr/lib64
sed -i -e 's@DESTINATION ${PYTHON_LIB_REL_PATH}@DESTINATION ${CMAKE_INSTALL_PREFIX}/${PYTHON_LIB_REL_PATH}@' caffe2/CMakeLists.txt

# reenable foxi linking
sed -i -e 's@list(APPEND Caffe2_DEPENDENCY_LIBS foxi_loader)@#list(APPEND Caffe2_DEPENDENCY_LIBS foxi_loader)@' cmake/Dependencies.cmake

# cmake version changed
sed -i -e 's@cmake_minimum_required(VERSION 3.4)@cmake_minimum_required(VERSION 3.5)@' third_party/tensorpipe/third_party/libuv/CMakeLists.txt
sed -i -e 's@cmake_minimum_required(VERSION 3.4)@cmake_minimum_required(VERSION 3.5)@' libuv*/CMakeLists.txt
%if %{without opentelemtry}
sed -i -e 's@cmake_minimum_required(VERSION 3.1)@cmake_minimum_required(VERSION 3.5)@' third_party/opentelemetry-cpp/CMakeLists.txt
%endif

%if %{with rocm}
# hipify
./tools/amd_build/build_amd.py
# Fedora installs to /usr/include, not /usr/include/rocm-core
sed -i -e 's@rocm-core/rocm_version.h@rocm_version.h@' aten/src/ATen/hip/tunable/TunableGemm.h
# https://github.com/pytorch/pytorch/issues/149805
sed -i -e 's@rocm-core/rocm_version.h@rocm_version.h@' cmake/public/LoadHIP.cmake
# Fedora installs to /usr/include, not /usr/include/rocm-core
sed -i -e 's@rocm-core/rocm_version.h@rocm_version.h@' aten/src/ATen/hip/tunable/Tunable.cpp
sed -i -e 's@rocm-core/rocm_version.h@rocm_version.h@' aten/src/ATen/cuda/tunable/Tunable.cpp
# use any hip, correct CMAKE_MODULE_PATH
sed -i -e 's@lib/cmake/hip@lib64/cmake/hip@' cmake/public/LoadHIP.cmake
sed -i -e 's@HIP 1.0@HIP MODULE@'            cmake/public/LoadHIP.cmake
# silence an assert
# sed -i -e '/qvalue = std::clamp(qvalue, qmin, qmax);/d' aten/src/ATen/native/cuda/IndexKernel.cu

%endif

%build

#
# Control the number of jobs
#
# The build can fail if too many threads exceed the physical memory
# So count core and and memory and increase the build memory util the build succeeds
#
# Real cores, No hyperthreading
COMPILE_JOBS=`cat /proc/cpuinfo | grep -m 1 'cpu cores' | awk '{ print $4 }'`
if [ ${COMPILE_JOBS}x = x ]; then
    COMPILE_JOBS=1
fi
# Take into account memmory usage per core, do not thrash real memory
BUILD_MEM=2
MEM_KB=0
MEM_KB=`cat /proc/meminfo | grep MemTotal | awk '{ print $2 }'`
MEM_MB=`eval "expr ${MEM_KB} / 1024"`
MEM_GB=`eval "expr ${MEM_MB} / 1024"`
COMPILE_JOBS_MEM=`eval "expr 1 + ${MEM_GB} / ${BUILD_MEM}"`
if [ "$COMPILE_JOBS_MEM" -lt "$COMPILE_JOBS" ]; then
    COMPILE_JOBS=$COMPILE_JOBS_MEM
fi
export MAX_JOBS=$COMPILE_JOBS

# For debugging setup.py
# export SETUPTOOLS_SCM_DEBUG=1

# For verbose cmake output
# export VERBOSE=ON
# For verbose linking
# export CMAKE_SHARED_LINKER_FLAGS=-Wl,--verbose

# Manually set this hardening flag
export CMAKE_EXE_LINKER_FLAGS=-pie

export BUILD_CUSTOM_PROTOBUF=OFF
export BUILD_NVFUSER=OFF
export BUILD_SHARED_LIBS=ON
export BUILD_TEST=OFF
export CMAKE_BUILD_TYPE=RelWithDebInfo
export CMAKE_FIND_PACKAGE_PREFER_CONFIG=ON
export CAFFE2_LINK_LOCAL_PROTOBUF=OFF
export INTERN_BUILD_MOBILE=OFF
export USE_DISTRIBUTED=OFF
export USE_CUDA=OFF
export USE_FAKELOWP=OFF
export USE_FBGEMM=OFF
export USE_FLASH_ATTENTION=OFF
export USE_GLOO=OFF
export USE_ITT=OFF
export USE_KINETO=OFF
export USE_KLEIDIAI=OFF
export USE_LITE_INTERPRETER_PROFILER=OFF
export USE_LITE_PROTO=OFF
export USE_MAGMA=OFF
export USE_MEM_EFF_ATTENTION=OFF
export USE_MKLDNN=OFF
export USE_MPI=OFF
export USE_NCCL=OFF
export USE_NNPACK=OFF
export USE_NUMPY=ON
export USE_OPENMP=ON
export USE_PYTORCH_QNNPACK=OFF
export USE_ROCM=OFF
export USE_SYSTEM_SLEEF=ON
export USE_SYSTEM_EIGEN_INSTALL=ON
%if %{with onnx}
export USE_SYSTEM_ONNX=ON
%endif
export USE_SYSTEM_PYBIND11=OFF
export USE_SYSTEM_LIBS=OFF
export USE_SYSTEM_NCCL=OFF
export USE_TENSORPIPE=OFF
export USE_XNNPACK=OFF
export USE_XPU=OFF
export USE_SYSTEM_PTHREADPOOL=ON
export USE_SYSTEM_CPUINFO=ON
export USE_SYSTEM_FP16=ON
export USE_SYSTEM_FXDIV=ON
export USE_SYSTEM_PSIMD=ON
export USE_SYSTEM_XNNPACK=OFF

export USE_DISTRIBUTED=ON
%if %{with tensorpipe}
export USE_TENSORPIPE=ON
export TP_BUILD_LIBUV=OFF
%endif

%if %{with gloo}
export USE_GLOO=ON
export USE_SYSTEM_GLOO=ON
%endif
%if %{with mpi}
export USE_MPI=ON
%endif

%if %{with test}
export BUILD_TEST=ON
%endif

# Why we are using py3_ vs pyproject_
#
# current pyproject problem with mock
# + /usr/bin/python3 -Bs /usr/lib/rpm/redhat/pyproject_wheel.py /builddir/build/BUILD/pytorch-v2.1.0/pyproject-wheeldir
# /usr/bin/python3: No module named pip
# Adding pip to build requires does not fix
#
# See BZ 2244862

%if %{with rocm}

export USE_ROCM=ON
export USE_ROCM_CK=OFF
export USE_MAGMA=ON
export HIP_PATH=`hipconfig -p`
export ROCM_PATH=`hipconfig -R`
RESOURCE_DIR=`%{rocmllvm_bindir}/clang -print-resource-dir`
export DEVICE_LIB_PATH=${RESOURCE_DIR}/amdgcn/bitcode

# pytorch uses clang, not hipcc
export HIP_CLANG_PATH=%{rocmllvm_bindir}
export PYTORCH_ROCM_ARCH=%{rocm_gpu_list_default}

%endif

%if 0%{?fedora}
%pyproject_wheel
%else
%py3_build
%endif


%install

%if %{with rocm}
export USE_ROCM=ON
export USE_ROCM_CK=OFF
export HIP_PATH=`hipconfig -p`
export ROCM_PATH=`hipconfig -R`
RESOURCE_DIR=`%{rocmllvm_bindir}/clang -print-resource-dir`
export DEVICE_LIB_PATH=${RESOURCE_DIR}/amdgcn/bitcode

# pytorch uses clang, not hipcc
export HIP_CLANG_PATH=%{rocmllvm_bindir}
export PYTORCH_ROCM_ARCH=%{rocm_gpu_list_default}

%endif

%if 0%{?fedora}
%pyproject_install
%pyproject_save_files '*torch*'
%else
%py3_install
%endif


%check
# Not working yet
# pyproject_check_import torch

# Do not remote the empty files

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.md 
%{_bindir}/torchrun
%{_bindir}/torchfrtrace
%{python3_sitearch}/%{pypi_name}*
%{python3_sitearch}/functorch

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.8.0-7
- Latest state for python-torch

* Thu Oct 23 2025 Jeremy Newton <Jeremy.Newton@amd.com> - 2.8.0-6
- Rebuild due to python change

* Wed Oct 01 2025 Jeremy Newton <Jeremy.Newton@amd.com> - 2.8.0-5
- Rebuild for rocprim 6.4.4

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.8.0-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.8.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Aug 14 2025 Tom Rix <Tom.Rix@amd.com> - 2.8.0-2
- Build on EPEL

* Fri Aug 08 2025 Tom Rix <Tom.Rix@amd.com> - 2.8.0-1
- Update to 2.8.0

* Mon Aug 04 2025 Tom Rix <Tom.Rix@amd.com> - 2.8.0.rc8-2
- Change a couple cmake mins

* Thu Jul 31 2025 Tom Rix <Tom.Rix@amd.com> - 2.8.0.rc8-1
- Update to 2.8.0-rc8

* Sun Jul 27 2025 Tom Rix <Tom.Rix@amd.com> - 2.7.0-9
- Fix some issues with switching to pyproject macros

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 24 2025 Tom Rix <Tom.Rix@amd.com> - 2.7.0-7
- Update gitcommit to 2.8.0-rc8

* Sun Jul 20 2025 Tom Rix <Tom.Rix@amd.com> - 2.7.0-6
- Update the next gitcommit to v2.8.0-rc6

* Fri Jun 27 2025 Tom Rix <Tom.Rix@amd.com> - 2.7.0-5
- update gitcommit to 2.8-rc3

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 2.7.0-4
- Rebuilt for Python 3.14

* Sun May 04 2025 Tom Rix <Tom.Rix@amd.com> - 2.7.0-3
- Rebuild for magma

* Thu May 01 2025 Tom Rix <Tom.Rix@amd.com> - 2.7.0-2
- Turn off kleidai

* Fri Apr 25 2025 Tom Rix <Tom.Rix@amd.com> - 2.7.0-1
- Update to 2.7.0

* Sat Apr 19 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-19
- Update gitcommit to 2.7.0-rc10

* Sun Apr 13 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-18
- Update gitcommit to 2.7.0-rc9

* Thu Apr 10 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-17
- Update gitcomit to 2.7.0-rc8

* Sat Apr 05 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-16
- Update gitcommit to v2.7.0-rc6

* Sat Mar 29 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-15
- Update gitcommit to 2.7-rc3

* Sat Mar 22 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-14
- Update gitcommit to v2.7.0-rc2

* Thu Mar 13 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-13
- Update gitcommit

* Wed Mar 12 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-12
- Remove papering over c++ assert problem.

* Sat Mar 01 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-11
- cmake version changed

* Wed Feb 26 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-10
- Remove gold linker

* Mon Feb 17 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-9
- Remove rocm loop

* Fri Jan 31 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-8
- Rebuild

* Fri Jan 24 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-7
- Document the issue for c++ asserts in upstream

* Thu Jan 23 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-6
- triage build break

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 02 2025 Tom Rix <Tom.Rix@amd.com> - 2.5.1-4
- Rebuild for onnx

* Tue Dec 24 2024 Tom Rix <Tom.Rix@amd.com> - 2.5.1-3
- Remove many options

* Mon Dec 23 2024 Tom Rix <Tom.Rix@amd.com> - 2.5.1-2
- Obsolete caffe

* Sat Dec 21 2024 Tom Rix <Tom.Rix@amd.com> - 2.5.1-1
- Update to 2.5.1

* Tue Nov 26 2024 Tom Rix <Tom.Rix@amd.com> - 2.5.0-1
- Update for 2.5.0

* Thu Nov 14 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-12
- Use rocmllvm_bindir

* Thu Oct 31 2024 Peter Robinson <pbrobinson@gmail.com> - 2.4.1-11
- drop old versions of pytorch from sources

* Thu Oct 31 2024 Peter Robinson <pbrobinson@gmail.com> - 2.4.1-10
- Add binutils-gold build dep

* Thu Oct 31 2024 Peter Robinson <pbrobinson@gmail.com> - 2.4.1-9
- Fix various Provides including the pytotch provides

* Tue Oct 29 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-8
- Use the new xnnpack

* Fri Oct 11 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-7
- Update gitcommit to v2.5.0-rc9

* Thu Oct 10 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-6
- Update for llvm18

* Mon Oct 07 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-5
- Some help finding llvm18

* Mon Sep 30 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-4
- Update gitcommit

* Sun Sep 15 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-3
- Simplify cuda versions

* Sun Sep 15 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-2
- Update gitcommit

* Mon Sep 09 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.1-1
- Update to 2.4.1

* Tue Sep 03 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.0-10
- amdsmi is a runtime dependency for ROCm

* Fri Aug 30 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.0-9
- Update the gitcommit

* Thu Aug 15 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.0-8
- Start tracking 2.5

* Wed Aug 07 2024 Tom Rix <Tom.Rix@amd.com> - 2.4.0-7
- Disable fbgemm with rocm

* Mon Aug 05 2024 Tom Rix <trix@redhat.com> - 2.4.0-6
- Enable hipblaslt

* Sun Aug 04 2024 Tom Rix <trix@redhat.com> - 2.4.0-5
- Remove the packages

* Sun Aug 04 2024 Tom Rix <trix@redhat.com> - 2.4.0-4
- Simplify ROCm gpu list

* Sat Jul 27 2024 Tom Rix <trix@redhat.com> - 2.4.0-3
- Fbgemm not available on aarch64

* Thu Jul 25 2024 Sérgio M. Basto <sergio@serjux.com> - 2.4.0-2
- Rebuild for opencv 4.10.0

* Thu Jul 25 2024 Tom Rix <trix@redhat.com> - 2.4.0-1
- PyTorch 2.4

* Sat Jul 20 2024 Tom Rix <trix@redhat.com> - 2.3.1-23
- Fix USE_NUMA

* Sat Jul 20 2024 Tom Rix <trix@redhat.com> - 2.3.1-22
- Use fbgemm on 2.4

* Tue Jul 16 2024 Kefu Chai <tchaikov@gmail.com> - 2.3.1-20
- Rebuilt for fmt 11

* Wed Jul 10 2024 Tom Rix <trix@redhat.com> - 2.3.1-19
- Update to 2.4-rc8

* Fri Jul 05 2024 Tom Rix <trix@redhat.com> - 2.3.1-18
- Switch from openblas to flexiblas (rhbz#2295953)

* Thu Jul 04 2024 Tom Rix <trix@redhat.com> - 2.3.1-17
- Show use of hipblaslt package

* Thu Jul 04 2024 Tom Rix <trix@redhat.com> - 2.3.1-16
- Revisions of patches for 2.4

* Wed Jun 26 2024 Tom Rix <trix@redhat.com> - 2.3.1-15
- Add a CUDA subpackage

* Wed Jun 26 2024 Tom Rix <trix@redhat.com> - 2.3.1-14
- Update gitcommit to v2.4.0-rc6

* Tue Jun 25 2024 Tom Rix <trix@redhat.com> - 2.3.1-13
- Add CUDA BuildRequires

* Mon Jun 24 2024 Tom Rix <trix@redhat.com> - 2.3.1-12
- Update gitcommit to 2.4.0-rc5

* Fri Jun 21 2024 Tom Rix <trix@redhat.com> - 2.3.1-11
- Update gitcommit to 2.4.0-rc3

* Tue Jun 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 2.3.1-10
- Patch for sleef 3.6

* Fri Jun 14 2024 Python Maint <python-maint@redhat.com> - 2.3.1-9
- Rebuilt for Python 3.13

* Thu Jun 13 2024 Tom Rix <trix@redhat.com> - 2.3.1-8
- Update gitcommit

* Thu Jun 13 2024 Tom Rix <trix@redhat.com> - 2.3.1-7
- Use specific version of CUDA base on disto release

* Tue Jun 11 2024 Tom Rix <trix@redhat.com> - 2.3.1-6
- Fix broken cpuinfo for aarch64

* Tue Jun 11 2024 Tom Rix <trix@redhat.com> - 2.3.1-5
- Reduce amd gpu list on F40

* Mon Jun 10 2024 Tom Rix <trix@redhat.com> - 2.3.1-4
- Start a readme for NVIDIA

* Mon Jun 10 2024 Tom Rix <trix@redhat.com> - 2.3.1-3
- Fix the normal build.

* Sun Jun 09 2024 Tom Rix <trix@redhat.com> - 2.3.1-2
- Update gitcommit

* Sun Jun 09 2024 Tom Rix <trix@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Sat Jun 08 2024 Tom Rix <trix@redhat.com> - 2.3.0-15
- Add --with compat_gcc

* Sat Jun 08 2024 Tom Rix <trix@redhat.com> - 2.3.0-14
- Do not apply ROCm patches with CUDA build

* Fri Jun 07 2024 Tom Rix <trix@redhat.com> - 2.3.0-13
- Do not conditionally patch

* Thu Jun 06 2024 Tom Rix <trix@redhat.com> - 2.3.0-12
- Update for ROCm 6.1.1

* Wed Jun 05 2024 Tom Rix <trix@redhat.com> - 2.3.0-11
- Update the ToT git commit

* Tue May 21 2024 Tom Rix <trix@redhat.com> - 2.3.0-10
- Start tracking upstream 2.4

* Sat May 18 2024 Tom Rix <trix@redhat.com> - 2.3.0-9
- Roll ROCm support claim back to f40

* Thu May 16 2024 Tom Rix <trix@redhat.com> - 2.3.0-8
- Add cuda arches to build for

* Tue May 07 2024 Tom Rix <trix@redhat.com> - 2.3.0-7
- Fill in missing packages on F40 and F39 with third_party.

* Sun May 05 2024 Tom Rix <trix@redhat.com> - 2.3.0-6
- Collect the buildrequires that depend on F40 together.

* Sun May 05 2024 Tom Rix <trix@redhat.com> - 2.3.0-5
- Improve fedora conditional use versions.

* Fri May 03 2024 Tom Rix <trix@redhat.com> - 2.3.0-4
- Enable dynamo on 3.12

* Thu May 02 2024 Tom Rix <trix@redhat.com> - 2.3.0-3
- Disable dwz with ROCm

* Tue Apr 30 2024 Tom Rix <trix@redhat.com> - 2.3.0-2
- Update sources

* Tue Apr 30 2024 Tom Rix <trix@redhat.com> - 2.3.0-1
- Initial 2.3 release

* Mon Apr 15 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20240408.97ff6cf-2
- Use the system gloo

* Thu Apr 11 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20240408.97ff6cf-1
- v2.3.0-rc12

* Sat Apr 06 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20240402.4bb5cb5-1
- Update to 2.3-rc7

* Sun Mar 31 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20242213.74832f1-2
- Provide pytorch as a convience

* Wed Mar 27 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20242213.74832f1-1
- Update to 2.3-rc6

* Fri Mar 22 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20240313.6a89a75-8
- Remove conditional around the rocm patches

* Fri Mar 22 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20240313.6a89a75-7
- Split the ROCm gpu families out into subpackages.

* Thu Mar 21 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20240313.6a89a75-6
- Update the source to 2.3-rc2

* Thu Mar 21 2024 Tom Rix <trix@redhat.com> - 2.3.0^git20240313.6a89a75-5
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
