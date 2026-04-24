# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstreamname rocAL

%global rocm_release 6.4
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

# mixing gcc and clang, some flags need to be removed
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong//' -e 's/-fcf-protection//' -e 's/-mtls-dialect=gnu2//')

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

# Need local gpu hw to test
# No good way to run tests from a subpackage, so need to run them as part of check
%bcond_with check
# Still need a test subpackage because tests depend on install of test data
%bcond_with test

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"        xz level 7 using %%{getncpus} threads
#
# This changes from the default compressor
#   $ gzip
# To
#   $ xz -7 -T cpus
#
# Multithreading the compress stage reduces the overall build time.
%global _source_payload         w7T0.xzdio
%global _binary_payload         w7T0.xzdio

Name:           rocal
Version:        %{rocm_version}
Release: 3%{?dist}
Summary:        ROCm Augmentation Library

Url:            https://github.com/ROCm/rocAL
License:        MIT AND BSD-3-Clause
# rocAL is MIT
# bundled rapidjson is MIT AND BSD-3-Clause
Source0:        %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz

#
# rapidjson bundling
# rocAL uses unreleased ToT rapidjson API, see rocAL-setup.py
%global rapidjson_date 20241218
%global rapidjson_commit 24b5e7a8b27f42fa16b96fc70aade9106cf7102f
%global short_rapidjson_commit %(c=%{rapidjson_commit}; echo ${c:0:7})
Source1:        https://github.com/Tencent/rapidjson/archive/%{rapidjson_commit}.tar.gz

BuildRequires:  cmake
# Problems with opional ffmpeg
# rocAL-rocm-6.3.3/rocAL/source/decoders/video/hardware_video_decoder.cpp:178:11: error: no matching function for call to 'av_find_best_stream'
#  178 |     ret = av_find_best_stream(_fmt_ctx, AVMEDIA_TYPE_VIDEO, -1, -1, &_decoder, 0);
#      |           ^~~~~~~~~~~~~~~~~~~
# So disable use
# BuildRequires:  ffmpeg-free-devel
BuildRequires:  gcc-c++
BuildRequires:  half-devel
BuildRequires:  lmdb-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libsndfile-devel
BuildRequires:  mivisionx-devel >= %{rocm_release}
BuildRequires:  protobuf-devel
BuildRequires:  pybind11-devel
BuildRequires:  rocdecode-devel >= %{rocm_release}
BuildRequires:  rocjpeg-devel >= %{rocm_release}
BuildRequires:  rocm-cmake >= %{rocm_release}
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel >= %{rocm_release}
BuildRequires:  rocm-omp-devel >= %{rocm_release}
BuildRequires:  rocm-rpp-devel >= %{rocm_release}
BuildRequires:  rocm-runtime-devel >= %{rocm_release}
BuildRequires:  rocm-rpm-macros >= %{rocm_release}
BuildRequires:  turbojpeg-devel

# License info copied from the rapidjson spec
# License: MIT AND BSD-3-Clause
Provides:       bundled(rapidjson) = %{rapidjson_date}.g%{short_rapidjson_commit}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
The AMD ROCm Augmentation Library (rocAL) is designed to efficiently
decode and process images and videos from a variety of storage formats
and modify them through a processing graph programmable by the user.
rocAL currently provides C API.

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       rocal-devel = %{version}-%{release}

%description devel
%{summary}

%if %{with test}
%package test
Summary:        Tests for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

# rapidjson ToT
tar xf %{SOURCE1}

# cmake 3.5 minimum
sed -i -e 's@cmake_minimum_required(VERSION 2.8)@cmake_minimum_required(VERSION 3.5)@' rapidjson-%{rapidjson_commit}/example/CMakeLists.txt

# #include <half/half.hpp> -> <half.hpp>
for f in `find . -type f -name '*.hpp' -o -name '*.h' -o -name '*.cpp' `; do
    sed -i -e 's@#include <half/half.hpp>@#include <half.hpp>@' $f
done
sed -i -e 's@half/half.hpp@half.hpp@' cmake/FindHALF.cmake

# We set this below
sed -i -e 's@set(COMPILER_FOR_HIP@#set(COMPILER_FOR_HIP@' rocAL/rocAL_hip/CMakeLists.txt

# https://github.com/ROCm/rocAL/issues/287
# Several rpmlint warning about missing libjpeg syms
# rocal.x86_64: E: undefined-non-weak-symbol /usr/lib64/librocal.so.2.1.0 jpeg_mem_src (/usr/lib64/librocal.so.2.1.0)
sed -i -e 's@set(LINK_LIBRARY_LIST ${LINK_LIBRARY_LIST} ${TurboJpeg_LIBRARIES})@set(LINK_LIBRARY_LIST ${LINK_LIBRARY_LIST} ${LIBJPEG_LIBRARIES} ${TurboJpeg_LIBRARIES})@' rocAL/CMakeLists.txt

# Tests use the wrong ROCM_PATH
sed -i -e 's@set(ROCM_PATH /opt/rocm@set(ROCM_PATH /usr@' tests/cpp_api/CMakeLists.txt
sed -i -e 's@set(ROCM_PATH /opt/rocm@set(ROCM_PATH /usr@' tests/cpp_api/*/CMakeLists.txt

# tests have wrong include
for f in `find tests -type f -name '*.cpp' `; do
    sed -i -e 's@rocal_api.h@rocal/rocal_api.h@' $f
    sed -i -e 's@rocal_api_types.h@rocal/rocal_api_types.h@' $f
done

# Remove to make license simpler
# Apache License 2.0
# ------------------
# rocal-6.3.3-build/rocAL-rocm-6.3.3/docs/examples/tf/pets_training/create_pet_tf_record.py
rm -rf docs/examples/tf/pets_training

%build

cd rapidjson-%{rapidjson_commit}
p=$PWD
mkdir build
cd build
%__cmake \
       -DBUILD_SHARED_LIBS=OFF \
       -DCMAKE_BUILD_TYPE=RELEASE \
       -DRAPIDJSON_BUILD_CXX11:BOOL=OFF \
       -DCMAKE_INSTALL_PREFIX=$p/install \
       ..
%make_build
%make_build install
cd ../..

%cmake \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=%{build_type} \
    -DCMAKE_INSTALL_LIBDIR=%_libdir \
    -DCMAKE_PREFIX_PATH=$p/install/lib/cmake \
    -DCOMPILER_FOR_HIP=%rocmllvm_bindir/clang++ \
    -DHIP_PLATFORM=amd \
    -DROCM_PATH=%_prefix

%cmake_build

%if %{with check}
# Need to install rocal-test
# This issue in MiVisionX is causing test failures
# https://github.com/ROCm/MIVisionX/issues/1489
%check
%ctest
%endif

%install
%cmake_install

if [ -f %{buildroot}%{_prefix}/share/doc/rocal/LICENSE.txt ]; then
    rm %{buildroot}%{_prefix}/share/doc/rocal/LICENSE.txt
fi
if [ -f %{buildroot}%{_prefix}/share/doc/rocal-asan/LICENSE.txt ]; then
    rm %{buildroot}%{_prefix}/share/doc/rocal-asan/LICENSE.txt
fi

# No cmake knob to turn off testing, remove the install dir
%if %{without test}
rm -rf %{buildroot}%{_datadir}/rocal/test
%endif

%files
%doc README.md
%license LICENSE.txt
%{_libdir}/librocal.so.2{,.*}

%files devel
%{_libdir}/librocal.so
%{_includedir}/rocal/

%if %{with test}
%files test
%{_datadir}/rocal/test
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.0-1
- Update to 6.4.0

* Thu Feb 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.3-1
- Initial package
