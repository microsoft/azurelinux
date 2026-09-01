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

%global upstreamname aqlprofile
%global rocm_release 7.1
%global rocm_patch 0
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

# Testing is broken
%bcond_with test
%if %{with test}
%global build_test ON
%else
%global build_test OFF
%endif

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

%global gpu_list %{rocm_gpu_list_test}
%global _gpu_list gfx1100

# Test building needs our compiler
%global toolchain clang

Name:           aqlprofile%{pkg_suffix}
Version:        %{rocm_version}
Release:        5%{?dist}
Summary:        Architected Queuing Language Profiling Library
License:        MIT

# Only x86_64 works right now:
ExclusiveArch:  x86_64

Url:            https://github.com/ROCm/%{upstreamname}
Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocm-clang%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-llvm%{pkg_suffix}-static
BuildRequires:  rocm-runtime%{pkg_suffix}-devel
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocm-runtime%{pkg_suffix}-devel

%if %{with test}
%if 0%{?suse_version}
BuildRequires:  gmock
BuildRequires:  gtest
%else
BuildRequires:  gmock-devel
BuildRequires:  gtest-devel
%endif
%endif

%description
AQLprofile is an open source library that enables advanced GPU
profiling and tracing on AMD platforms. It works in conjunction
with rocprofiler-sdk to support profiling methods such as
performance counters (PMC) and SQ thread trace (SQTT).
AQLprofile provides the foundational mechanisms for constructing
AQL packets and managing profiling operations across multiple
AMD GPU architecture families.

%package devel
Summary:        The development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%if %{with test}
%package test
Summary:        The test package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description test
%{summary}
%endif

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

# Do not hardcode CMAKE_BUILD_TYPE
# https://github.com/ROCm/aqlprofile/issues/12
sed -i -e 's@CMAKE_BUILD_TYPE@DO_NO_HARDCODE_CMAKE_BUILD_TYPE@' cmake_modules/env.cmake

%build
%cmake \
    -DAQLPROFILE_BUILD_TESTS=%{build_test} \
    -DCMAKE_INSTALL_LIBDIR=%{pkg_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{pkg_prefix} \
    -DCMAKE_BUILD_TYPE=%{build_type} \
    -DCMAKE_C_COMPILER=%rocmllvm_bindir/amdclang \
    -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/amdclang++ \
    -DCMAKE_HIP_ARCHITECTURES=%{gpu_list} \
    -DCMAKE_HIP_COMPILER_ROCM_ROOT=%{pkg_prefix} \
    -DCMAKE_HIP_COMPILER=%{rocmllvm_bindir}/amdclang++ \
    -DCMAKE_HIP_FLAGS="-I %{pkg_prefix}/include" \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DGPU_TARGETS=%{gpu_list}
    
%cmake_build

%install
%cmake_install

%files
%license LICENSE.md
%{pkg_prefix}/%{pkg_libdir}/libhsa-amd-aqlprofile64.so.1{,.*}

%files devel
%doc README.md
%{pkg_prefix}/include/aqlprofile-sdk/
%{pkg_prefix}/%{pkg_libdir}/libhsa-amd-aqlprofile64.so

%if %{with test}
%files test
%{pkg_prefix}/share/hsa-amd-aqlprofile/
%endif

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Dec 28 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-3
- Fix --with test

* Tue Dec 23 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Add --with compat

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Fri Sep 26 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-1
- Update to 7.0.1

* Thu Aug 28 2025 Tom Rix <Tom.Rix@amd.com> - 0.0^git20250526.eebb229-3
- Add Fedora copyright

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0^git20250526.eebb229-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 1 2025 Tom Rix <Tom.Rix@amd.com> - 0.0^git20250526.eebb229-1
- Initial package

