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
%global commit0 2584e35062ad9c2edb68d93c464cf157bc57e3b0
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20250926
%endif

%global upstreamname hipSOLVER
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
%if 0%{?suse_version}
%global hipsolver_name libhipsolver1%{pkg_suffix}
%else
%global hipsolver_name hipsolver%{pkg_suffix}
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

# FTBFS, turn off testing
%bcond_with test
%if %{with test}
%global build_test ON
%else
%global build_test OFF
%endif

# gfortran and clang rpm macros do not mix
%global build_fflags %{nil}

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

Name:           %{hipsolver_name}
%if %{with gitcommit}
Version:        git%{date0}.%{shortcommit0}
Release:        3%{?dist}
%else
Version:        %{rocm_version}
Release:        6%{?dist}
%endif
Summary:        ROCm SOLVER marshalling library
License:        MIT

%if %{with gitcommit}
Url:            https://github.com/ROCm/rocm-libraries
Source0:        %{url}/archive/%{commit0}/rocm-libraries-%{shortcommit0}.tar.gz
%else
Url:            https://github.com/ROCm/%{upstreamname}
Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz
%endif

Patch1:         0001-hipsolver-so-version-fortran-bindings.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  rocblas%{pkg_suffix}-devel
BuildRequires:  rocm-cmake%{pkg_suffix}
BuildRequires:  rocm-comgr%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-runtime%{pkg_suffix}-devel
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocsolver%{pkg_suffix}-devel
BuildRequires:  rocsparse%{pkg_suffix}-devel
%if 0%{?fedora}
BuildRequires:  suitesparse-devel
%endif

%if %{with test}
BuildRequires:  gtest-devel
BuildRequires:  hipsparse%{pkg_suffix}-devel
%if 0%{?suse_version}
BuildRequires:  blas-devel
BuildRequires:  cblas-devel
BuildRequires:  lapack-devel
%else
BuildRequires:  blas-static
BuildRequires:  lapack-static
%endif
%endif

Provides:       hipsolver%{pkg_suffix} = %{version}-%{release}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
hipSOLVER is a LAPACK marshalling library, with multiple supported
backends. It sits between the application and a 'worker'
LAPACK library, marshalling inputs into the backend library and
marshalling results back to the application. hipSOLVER exports an
interface that does not require the client to change, regardless
of the chosen backend. Currently, hipSOLVER supports rocSOLVER
and cuSOLVER as backends.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       hipsolver%{pkg_suffix}-devel = %{version}-%{release}

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
cd projects/hipsolver
%patch -P1 -p1
%else
%autosetup -p1 -n %{upstreamname}-rocm-%{version}
%endif

%build
%if %{with gitcommit}
cd projects/hipsolver
%endif

%cmake \
    -DCMAKE_C_COMPILER=%rocmllvm_bindir/amdclang \
    -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/amdclang++ \
    -DCMAKE_INSTALL_LIBDIR=%{pkg_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{pkg_prefix} \
    -DCMAKE_LINKER=%rocmllvm_bindir/ld.lld \
    -DCMAKE_AR=%rocmllvm_bindir/llvm-ar \
    -DCMAKE_RANLIB=%rocmllvm_bindir/llvm-ranlib \
    -DCMAKE_BUILD_TYPE=%{build_type} \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DCMAKE_SKIP_RPATH=ON \
    -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
    -DROCM_SYMLINK_LIBS=OFF \
    -DHIP_PLATFORM=amd \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DBUILD_CLIENTS_TESTS=%{build_test}

%cmake_build

%install
%if %{with gitcommit}
cd projects/hipsolver
%endif

%cmake_install

# Extra license
rm -f %{buildroot}%{pkg_prefix}/share/doc/hipsolver/LICENSE.md

%files
%if %{with gitcommit}
%doc projects/hipsolver/README.md
%license projects/hipsolver/LICENSE.md
%else
%doc README.md
%license LICENSE.md
%endif

%{pkg_prefix}/%{pkg_libdir}/libhipsolver.so.1{,.*}
%{pkg_prefix}/%{pkg_libdir}/libhipsolver_fortran.so.1{,.*}

%files devel
%{pkg_prefix}/include/hipsolver/
%{pkg_prefix}/%{pkg_libdir}/libhipsolver.so
%{pkg_prefix}/%{pkg_libdir}/libhipsolver_fortran.so
%{pkg_prefix}/%{pkg_libdir}/cmake/hipsolver/

%if %{with test}
%files test
%{pkg_prefix}/share/hipsolver/
%{pkg_prefix}/bin/hipsolver*
%endif

%changelog
* Tue Jul 28 2026 Tom Rix <Tom.Rix@amd.com> - 7.1.0-6
- FTBFS fixed

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Dec 23 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-4
- Add --with compat

* Thu Nov 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-3
- Remove dir tags

* Mon Nov 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 7.1.0-2
- Rebuilt for gtest 1.17.0

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.0.1

* Mon Oct 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-2
- Turn on -test for fedora

* Sun Sep 21 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-1
- Update to 7.0.1

* Wed Aug 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-4
- Add Fedora copyright

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Simplify file removal

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-2
- Remove -mtls-dialect cflag

* Thu Jul 24 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Remove suse check of ldconfig

* Wed May 14 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Cleanup module build

* Sun Apr 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Sat Apr 5 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-6
- suitesparse-devel is optional

* Fri Feb 14 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-5
- remove multi build
- Fix SLE 15.6

* Thu Jan 23 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- multithread compress

* Fri Jan 17 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-3
- build requires gcc-c++

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed
