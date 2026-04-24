# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstreamname rpp
%global rocm_release 6.4
%global rocm_patch 0
%global rocm_version %{rocm_release}.%{rocm_patch}

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-mtls-dialect=gnu2//')

# The default list in the project does not cover our expected targets
%global all_rocm_gpus "gfx900;gfx906:xnack-;gfx908:xnack-;gfx90a:xnack+;gfx90a:xnack-;gfx942;gfx950;gfx1010;gfx1012;gfx1030;gfx1100;gfx1101;gfx1102;gfx1103;gfx1150;gfx1151;gfx1152;gfx1153;gfx1200;gfx1201"

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

# Testing does not work well, it requires local hw.
%bcond_with test

Name:           rocm-rpp
Version:        %{rocm_version}
Release: 6%{?dist}
Summary:        ROCm Performace Primatives for computer vision
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT AND Apache-2.0 AND LicenseRef-Fedora-Public-Domain
# The main license is MIT
# A couple of files have Apache-2.0
#   src/include/common/rpp/kernel_cache.hpp
#   src/modules/kernel_cache.cpp
# A Public Domain
#   src/modules/md5.cpp

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  chrpath
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  half-devel
BuildRequires:  ninja-build
%if 0%{?fedora}
BuildRequires:  opencv-devel
%endif
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-omp-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
AMD ROCm Performance Primitives (RPP) library is a comprehensive,
high-performance computer vision library for AMD processors that
have HIP, OpenCL, or CPU backends.

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

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

# hip compiler
sed -i -e 's@set(COMPILER_FOR_HIP ${ROCM_PATH}/llvm/bin/clang++)@set(COMPILER_FOR_HIP hipcc)@' CMakeLists.txt
# remove clang++
sed -i -e '/set(CMAKE_CXX_COMPILER clang++)/d' CMakeLists.txt

# #include <half/half.hpp> -> <half.hpp>
for f in `find . -type f -name '*.hpp' -o -name '*.cpp' -o -name '*.h' `; do
    sed -i -e 's@#include <half/half.hpp>@#include <half.hpp>@' $f
done

# Remove search for HALF, ours is installed in the usual place
sed -i -e '/HALF/d' CMakeLists.txt

%if %{without test}
# Some things that are not used
sed -i -e '/COMPONENT test/d' CMakeLists.txt
%endif

# Remove third_party libs
# https://github.com/ROCm/rpp/issues/602
rm -rf libs/third_party

%build

%cmake -G Ninja \
       -DAMDGPU_TARGETS=%{all_rocm_gpus} \
       -DBACKEND=HIP \
       -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
       -DCMAKE_BUILD_TYPE=%{build_type} \
       -DHIP_PLATFORM=amd \
       -DROCM_SYMLINK_LIBS=OFF \
       -DRPP_AUDIO_SUPPORT=OFF \
       -DROCM_PATH=%{_prefix} \
       -DHIP_PATH=%{_prefix} \
       -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%cmake_build

%install
%cmake_install

# ERROR   0020: file '/usr/lib64/librpp.so.1.9.1' contains a runpath referencing '..' of an absolute path [/usr/lib64/rocm/llvm/bin/../lib]
chrpath -r %{rocmllvm_libdir} %{buildroot}%{_libdir}/librpp.so.1.*.*

%files
%license LICENSE
%exclude %{_docdir}/rpp/LICENSE
%exclude %{_docdir}/rpp-asan/LICENSE
%{_libdir}/librpp.so.1{,.*}

%files devel
%doc README.md
%{_includedir}/rpp
%{_libdir}/librpp.so

%if %{with test}
%files test
%dir %{_datadir}/rpp
%{_datadir}/rpp/*

%endif

%changelog
* Thu Aug 21 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-5
- Remove prebuild libffts.a library

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-4
- Remove -mtls-dialect cflag
- Add gfx950,gfx1150,gfx1151,gfx1152,gfx1153

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Add --with test

* Sun Apr 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Tue Feb 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-3
- Remove opencv for RHEL

* Sun Jan 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.1-2
- build requires gcc-c++
- Add gfx12

* Sun Dec 29 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.1-1
- Update to 6.3.1

