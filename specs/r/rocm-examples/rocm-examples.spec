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
%global upstreamname rocm-examples
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

%global toolchain rocm

# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-mtls-dialect=gnu2//')

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

# To test install the rocm-examples on a machine with an AMD gpu and run them manually

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"         xz level 7 using %%{getncpus} threads
# Multithreading the compress reduces the build time.
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

# some example cmake's do not like :xnack suffix
# reduce the default list
%global gpu_list %rocm_gpu_list_test
%global _gpu_list gfx1100

Name:           rocm-examples%{pkg_suffix}
Version:        %{rocm_version}
Release:        3%{?dist}
Summary:        A collection of examples for the ROCm software stack
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT AND Apache-2.0
# The main license is MIT
# A couple of assembly/llvm ir files that are Apache-2.0
# HIP-Basic/assembly_to_executable/hip_obj_gen.mcin
# HIP-Basic/assembly_to_executable/hip_obj_gen_win.mcin
# HIP-Basic/llvm_ir_to_executable/hip_obj_gen.mcin
# HIP-Basic/llvm_ir_to_executable/hip_obj_gen_win.mcin
Source0:        %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  hipblas%{pkg_suffix}-devel
BuildRequires:  hipcub%{pkg_suffix}-devel
BuildRequires:  hipfft%{pkg_suffix}-devel
BuildRequires:  hipify%{pkg_suffix}
BuildRequires:  hiprand%{pkg_suffix}-devel
BuildRequires:  hipsolver%{pkg_suffix}-devel
BuildRequires:  rocm-comgr%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-runtime%{pkg_suffix}-devel
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocblas%{pkg_suffix}-devel
BuildRequires:  rocfft%{pkg_suffix}-devel
BuildRequires:  rocsolver%{pkg_suffix}-devel
BuildRequires:  rocsparse%{pkg_suffix}-devel
BuildRequires:  rocthrust%{pkg_suffix}-devel

%if 0%{?suse_version}
BuildRequires:  benchmark-devel
BuildRequires:  gtest
%else
BuildRequires:  google-benchmark-devel
BuildRequires:  gtest-devel
%endif

# Only x86_64 works right now:
ExclusiveArch:  x86_64

BuildRequires: libpfm-devel
%description
This repository is a collection of examples to enable new users
to start using ROCm, as well as provide more advanced examples
for experienced users.

The examples are structured in several categories:
* HIP-Basic showcases some basic functionality without
  any additional dependencies

* Libraries contains examples for ROCm-libraries, that
  provide higher-level functionality

* Applications showcases some common applications, using
  HIP to accelerate them

* AI contains instructions on how to use ROCm for AI

* Tutorials contains the code accompanying the HIP Tutorials
  that can be found in the HIP documentation.

* For a full overview over the examples see the section
  repository contents.

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

# No External, not going to bundle things outside of this project.
# Not having glfw-devel turns off building examples that use External/glad
#
# Need to keep CmdParser
rm -rf External/{glad,KHR}

# https://github.com/ROCm/rocm-examples/issues/217
for f in `find . -name 'CMakeLists.txt'`; do
    sed -i -e 's@/opt/rocm@%{pkg_prefix}@' $f
done
for f in `find . -name 'Makefile'`; do
    sed -i -e 's@/opt/rocm@%{pkg_prefix}@' $f
done

# On SLE 15.6
# libstdc++ is too old and there are several compiling problems like this ..
# .../Tutorials/reduction/include/Reduction/v0.hpp:31:10: fatal error: 'execution' file not found
%if 0%{?suse_version}
%if %{suse_version} <= 1500
sed -i -e 's@add_subdirectory(Tutorials)@#add_subdirectory(Tutorials)@' CMakeLists.txt
sed -i -e 's@add_subdirectory(module_api)@message("no module_api")@'    HIP-Basic/CMakeLists.txt
%endif
%endif

# Some custom commands need to use hip_flags
sed -i -e 's@${CMAKE_HIP_COMPILER}@${CMAKE_HIP_COMPILER} -I%{pkg_prefix}/include@' HIP-Basic/llvm_ir_to_executable/CMakeLists.txt

%build

export ROCM_ROOT=%{pkg_prefix}

%cmake \
    -DCMAKE_C_COMPILER=%rocmllvm_bindir/amdclang \
    -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/amdclang++ \
    -DCMAKE_CXX_FLAGS="-I %{pkg_prefix}/include" \
    -DCMAKE_INSTALL_LIBDIR=%{pkg_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{pkg_prefix} \
    -DCMAKE_HIP_ARCHITECTURES=%{gpu_list} \
    -DCMAKE_HIP_COMPILER=%rocmllvm_bindir/amdclang++ \
    -DCMAKE_HIP_COMPILER_ROCM_ROOT=%{pkg_prefix} \
    -DCMAKE_HIP_FLAGS="-I %{pkg_prefix}/include" \
    -DGPU_TARGETS=%{gpu_list} \
    -DCMAKE_BUILD_TYPE=%{build_type} \
    -DHIP_PLATFORM=amd

%cmake_build

%install
%cmake_install

%files
%license LICENSE.md
%doc README.md
%{pkg_prefix}/bin/*

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Dec 24 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Add --with compat

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Sat Oct 11 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.2-1
- Update to 7.0.2

* Sun Sep 21 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-1
- Update to 7.0.1

* Thu Aug 28 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Add Fedora copyright

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-2
- Remove -mtls-dialect cflag

* Fri Jul 25 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 1 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-1
- Update to 6.4.1

* Fri May 2 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Disable building tutorial on sle 15.6

* Thu Apr 24 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Build on suse

* Sun Apr 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Fri Mar 21 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.3-1
- Initial package
