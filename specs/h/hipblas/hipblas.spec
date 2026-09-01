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

%global upstreamname hipBLAS
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
%global hipblas_name libhipblas3%{pkg_suffix}
%else
%global hipblas_name hipblas%{pkg_suffix}
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

%bcond_with test
%if %{with test}
%global build_test ON
%global __brp_check_rpaths %{nil}
# test parallel building broken
%global _smp_mflags -j1
%else
%global build_test OFF
%endif

# gfortran and clang rpm macros do not mix
%global build_fflags %{nil}

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

Name:           hipblas%{pkg_suffix}
%if %{with gitcommit}
Version:        git%{date0}.%{shortcommit0}
Release:        2%{?dist}
%else
Version:        %{rocm_version}
Release:        6%{?dist}
%endif
Summary:        ROCm BLAS marshalling library
License:        MIT

%if %{with gitcommit}
Url:            https://github.com/ROCm/rocm-libraries
Source0:        %{url}/archive/%{commit0}/rocm-libraries-%{shortcommit0}.tar.gz
%else
Url:            https://github.com/ROCmSoftwarePlatform/%{upstreamname}
Source0:        %{url}/archive/refs/tags/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  hipblas-common%{pkg_suffix}-devel
BuildRequires:  rocblas%{pkg_suffix}-devel
BuildRequires:  rocm-cmake%{pkg_suffix}
BuildRequires:  rocm-comgr%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-runtime%{pkg_suffix}-devel
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocsolver%{pkg_suffix}-devel

%if %{with test}
BuildRequires:  gtest-devel
%if 0%{?suse_version}
BuildRequires:  blas-devel
BuildRequires:  cblas-devel
BuildRequires:  lapack-devel
%else
BuildRequires:  blas-static
BuildRequires:  lapack-static
BuildRequires:  python3-pyyaml
%endif
%endif

Provides:       hipblas%{pkg_suffix} = %{version}-%{release}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
hipBLAS is a Basic Linear Algebra Subprograms (BLAS) marshalling
library, with multiple supported backends. It sits between the
application and a 'worker' BLAS library, marshalling inputs into
the backend library and marshalling results back to the
application. hipBLAS exports an interface that does not require
the client to change, regardless of the chosen backend. Currently,
hipBLAS supports rocBLAS and cuBLAS as backends.

%if 0%{?suse_version}
%package -n %{hipblas_name}
Summary:        Shared libraries for %{name}

%description -n %{hipblas_name}
%{summary}

%ldconfig_scriptlets -n %{hipblas_name}
%endif

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{hipblas_name}%{?_isa} = %{version}-%{release}
Requires:       hipblas-common%{pkg_suffix}-devel

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
cd projects/hipblas
%else
%autosetup -p1 -n %{upstreamname}-rocm-%{version}
%endif

# This is a tarball, no .git to query
sed -i -e 's@find_package(Git REQUIRED)@#find_package(Git REQUIRED)@' library/CMakeLists.txt

%build
%if %{with gitcommit}
cd projects/hipblas
%endif

%cmake \
    -DCMAKE_C_COMPILER=%rocmllvm_bindir/amdclang \
    -DCMAKE_CXX_COMPILER=%rocmllvm_bindir/amdclang++ \
    -DCMAKE_INSTALL_LIBDIR=%{pkg_libdir} \
    -DCMAKE_INSTALL_PREFIX=%{pkg_prefix} \
    -DCMAKE_LINKER=%rocmllvm_bindir/ld.lld \
    -DCMAKE_AR=%rocmllvm_bindir/llvm-ar \
    -DCMAKE_RANLIB=%rocmllvm_bindir/llvm-ranlib \
    -DCMAKE_BUILD_TYPE=%build_type \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DCMAKE_SKIP_RPATH=ON \
    -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
    -DROCM_SYMLINK_LIBS=OFF \
    -DHIP_PLATFORM=amd \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DBUILD_CLIENTS_BENCHMARKS=%{build_test} \
    -DBUILD_CLIENTS_TESTS=%{build_test} \
    -DBUILD_CLIENTS_TESTS_OPENMP=OFF \
    -DBUILD_FORTRAN_CLIENTS=OFF \
    -DBLAS_LIBRARY=cblas

%cmake_build

%install
%if %{with gitcommit}
cd projects/hipblas
%endif
%cmake_install

rm -f %{buildroot}%{pkg_prefix}/share/doc/hipblas/LICENSE.md

%files  -n %{hipblas_name}
%if %{with gitcommit}
%license projects/hipblas/LICENSE.md
%doc projects/hipblas/README.md
%else
%license LICENSE.md
%doc README.md
%endif
%{pkg_prefix}/%{pkg_libdir}/libhipblas.so.3{,.*}

%files devel
%{pkg_prefix}/include/hipblas/
%{pkg_prefix}/%{pkg_libdir}/libhipblas.so
%{pkg_prefix}/%{pkg_libdir}/cmake/hipblas/

%if %{with test}
%files test
%{pkg_prefix}/bin/hipblas*
%endif

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 22 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-5
- Add --with compat

* Thu Nov 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-4
- Remove dir tags

* Wed Nov 19 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-3
- hipblas cmake looks for hipblas-common

* Thu Nov 13 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Better handling of shared library on opensuse

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Sat Oct 11 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.2-1
- Update to 7.0.2

* Sat Sep 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-1
- Update to 7.0.1

* Wed Aug 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-6
- Add Fedora copyright

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-5
- Simplify file removal

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-4
- Remove -mtls-dialect cflag

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.1-2
- Remove suse check of ldconfig

* Thu May 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.1-1
- Update to 6.4.1

* Tue May 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Cleanup module build

* Tue Apr 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.0-2
- Rebuild against newer hipblas-common

* Sat Apr 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Fri Feb 14 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-5
- remove multi build
- Fix SLE 15.6

* Mon Jan 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- multhread compress

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- build requires gcc-c++

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed

