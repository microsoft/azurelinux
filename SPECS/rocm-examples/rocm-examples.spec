# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstreamname rocm-examples
%global rocm_release 6.4
%global rocm_patch 2
%global rocm_version %{rocm_release}.%{rocm_patch}

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

Name:           rocm-examples
Version:        %{rocm_version}
Release:        2%{?dist}
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
BuildRequires:  hipblas-devel
BuildRequires:  hipcub-devel
BuildRequires:  hipfft-devel
BuildRequires:  hipify
BuildRequires:  hiprand-devel
BuildRequires:  hipsolver-devel
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocblas-devel
BuildRequires:  rocfft-devel
BuildRequires:  rocsolver-devel
BuildRequires:  rocsparse-devel
BuildRequires:  rocthrust-devel

%if 0%{?suse_version}
BuildRequires:  benchmark-devel
BuildRequires:  gtest
%else
BuildRequires:  google-benchmark-devel
BuildRequires:  gtest-devel
%endif

# Only x86_64 works right now:
ExclusiveArch:  x86_64

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
rm -rf External/

# https://github.com/ROCm/rocm-examples/issues/217
for f in `find . -name 'CMakeLists.txt'`; do
    sed -i -e 's@opt/rocm@usr@' $f
done
for f in `find . -name 'Makefile'`; do
    sed -i -e 's@opt/rocm@usr@' $f
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

%build
%cmake \
    -DCMAKE_CXX_COMPILER=hipcc \
    -DCMAKE_HIP_ARCHITECTURES=%{rocm_gpu_list_default} \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DCMAKE_BUILD_TYPE=%{build_type} \
    -DHIP_PLATFORM=amd

%cmake_build

%install
%cmake_install

%files
%license LICENSE.md
%doc README.md
%{_bindir}/*

%changelog
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
