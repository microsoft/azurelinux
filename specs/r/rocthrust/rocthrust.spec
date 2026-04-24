# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global upstreamname rocThrust

%global rocm_release 6.4
%global rocm_patch 4
%global rocm_version %{rocm_release}.%{rocm_patch}

# Compiler is hipcc, which is clang based:
%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-mtls-dialect=gnu2//')
# there is no debug package
%global debug_package %{nil}

# Option to test suite for testing on real HW:
%bcond_with check
%if %{with check}
%global build_test ON
%else
%global build_test OFF
%endif

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
# Threaded compression reduces the build time.
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

Name:           rocthrust
Version:        %{rocm_version}
Release: 2%{?dist}
Summary:        ROCm Thrust libary

Url:            https://github.com/ROCm/%{upstreamname}
%if 0%{?suse_version}
# https://en.opensuse.org/openSUSE:Accepted_licences
# Uses 'Public Domain' but this is not a spdx tag and hangs up the SLE 15.7 autochecker
# The license should also include Public Domain
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT
%else
# https://docs.fedoraproject.org/en-US/legal/allowed-licenses/
# Uses 'LicenseRef-Fedora-Public-Domain'
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND MIT AND LicenseRef-Fedora-Public-Domain
%endif
# All files are Apache 2.0 with some exceptions:
# ./cmake contains only files under MIT
# ./internal/benchmark/*.py are dual licensed Apache 2.0 and Boost 1.0
# ./thrust/ contain some headers files that are Boost 1.0 licensed
# ./thrust/ contain some headers that are dual Apache 2.0 and Boost 1.0
# ./thrust/cmake/FindTBB.cmake is public domain
# ./thrust/detail/allocator/allocator_traits.h is dual Apache 2.0 and MIT
# ./thrust/detail/complex contains BSD 2 clause licensed headers

Source0:        %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel
BuildRequires:  rocprim-static
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros

%if %{with check}
%if 0%{?suse_version}
BuildRequires:  gtest
%else
BuildRequires:  gtest-devel
%endif
BuildRequires:  rocminfo
%endif

# Only headers, cmake infra, noarch confuses libdir
# BuildArch: noarch
# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
Thrust is a parallel algorithm library. This library has been
ported to HIP/ROCm platform, which uses the rocPRIM library.

%package devel
Summary:        The %{upstreamname} development package
Provides:       %{name}-static = %{version}-%{release}

%description devel
The %{upstreamname} development package.

%prep
%autosetup -p1 -n %{upstreamname}-rocm-%{version}

#
# The ROCMExportTargetsHeaderOnly.cmake file
# generates a files that reference the install location of other files
# Make this change so they match
sed -i -e 's/ROCM_INSTALL_LIBDIR lib/ROCM_INSTALL_LIBDIR lib64/' cmake/ROCMExportTargetsHeaderOnly.cmake

%build

%if %{with check}
# Building all the gpu's does not make sense
# Build only the first one, this only works well with rpmbuild.
gpu=`rocm_agent_enumerator | head -n 1`
%endif

%cmake \
	-DCMAKE_CXX_COMPILER=hipcc \
	-DCMAKE_C_COMPILER=hipcc \
	-DCMAKE_LINKER=%rocmllvm_bindir/ld.lld \
	-DCMAKE_AR=%rocmllvm_bindir/llvm-ar \
	-DCMAKE_RANLIB=%rocmllvm_bindir/llvm-ranlib \
    -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
    -DBUILD_TEST=%{build_test} \
%if %{with check}
    -DAMDGPU_TARGETS=${gpu} \
%endif
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DROCM_SYMLINK_LIBS=OFF
%cmake_build

%install
%cmake_install

if [ -f %{buildroot}%{_prefix}/share/doc/rocthrust/LICENSE ]; then
    rm %{buildroot}%{_prefix}/share/doc/rocthrust/LICENSE
fi

%check
%if %{with check}
%ctest
%endif

%files devel
%doc README.md
%license LICENSE
%license NOTICES.txt
%{_includedir}/thrust
%{_libdir}/cmake/%{name}

%changelog
* Tue Sep 30 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.4-1
- Update to 6.4.4

* Tue Jul 29 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Remove -mtls-dialect cflag

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Tue Jun 3 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Improve testing on suse

* Fri Apr 18 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Fri Apr 4 2025 Tom Rix <Tom.Rix@amd.com> 6.3.0-6
- correct spdx license for suse

* Fri Apr 4 2025 Tom Rix <Tom.Rix@amd.com> 6.3.0-5
- correct spdx license usage

* Mon Jan 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- multithread compress

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- build requires gcc-c++

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed


