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

%global upstreamname hipFFT
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
%global hipfft_name libhipfft0%{pkg_suffix}
%else
%global hipfft_name hipfft%{pkg_suffix}
%endif

%global toolchain rocm
# hipcc does not support some clang flags
%global build_cxxflags %(echo %{optflags} | sed -e 's/-fstack-protector-strong/-Xarch_host -fstack-protector-strong/' -e 's/-fcf-protection/-Xarch_host -fcf-protection/' -e 's/-mtls-dialect=gnu2//' -e 's/-flto=thin//' )

%global _lto_cflags %{nil}

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
%else
%global build_test OFF
%endif

# Option to test suite for testing on real HW:
# May have to set gpu under test with
# export HIP_VISIBLE_DEVICES=<num> - 0, 1 etc.
%bcond_with check

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio" xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

Name:           %{hipfft_name}
%if %{with gitcommit}
Version:        git%{date0}.%{shortcommit0}
Release:        2%{?dist}
%else
Version:        %{rocm_version}
Release:        5%{?dist}
%endif
Summary:        ROCm FFT marshalling library
License:        MIT

%if %{with gitcommit}
Url:            https://github.com/ROCm/rocm-libraries
Source0:        %{url}/archive/%{commit0}/rocm-libraries-%{shortcommit0}.tar.gz
%else
Url:            https://github.com/ROCm/%{upstreamname}
Source0:        %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-rocm-%{version}.tar.gz
%endif

# https://github.com/ROCm/rocm-libraries/issues/2400
Patch1:         0001-hipfft-hipfftw-soversion.patch

# Only x86_64 works right now
ExclusiveArch:  x86_64

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocm-cmake%{pkg_suffix}
BuildRequires:  rocm-comgr%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-runtime%{pkg_suffix}-devel >= %{rocm_release}
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocprim%{pkg_suffix}-static
BuildRequires:  rocfft%{pkg_suffix}-devel

%if %{with test}

BuildRequires:  boost-devel
BuildRequires:  fftw-devel
BuildRequires:  hiprand%{pkg_suffix}-devel
BuildRequires:  rocrand%{pkg_suffix}-devel

%if 0%{?suse_version}
BuildRequires:  gtest
BuildRequires:  libboost_program_options-devel
%else
BuildRequires:  gtest-devel
%endif

%endif

Provides:       hipfft%{pkg_suffix} = %{version}-%{release}

%description
hipFFT is an FFT marshalling library. Currently, hipFFT supports
the rocFFT backends

hipFFT exports an interface that does not require the client to
change, regardless of the chosen backend. It sits between the
application and the backend FFT library, marshalling inputs into
the backend and results back to the application.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       hipfft%{pkg_suffix}-devel = %{version}-%{release}

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
cd projects/hipfft
%else
%autosetup -n %{upstreamname}-rocm-%{version} -p 1
%endif

# CMake Error at clients/tests/CMakeLists.txt:87 (find_package):
#   No "FindHIP.cmake" found in CMAKE_MODULE_PATH.
# Remove MODULE
sed -i -e 's@find_package( HIP MODULE REQUIRED )@find_package( HIP REQUIRED )@' clients/tests/CMakeLists.txt

%build
%if %{with gitcommit}
cd projects/hipfft
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
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DBUILD_CLIENTS_TESTS=%{build_test} \
    -DBUILD_CLIENTS_TESTS_OPENMP=OFF \
    -DROCM_SYMLINK_LIBS=OFF \
    -DHIP_PLATFORM=amd

%cmake_build


%install
%if %{with gitcommit}
cd projects/hipfft
%endif
%cmake_install

rm -f %{buildroot}%{pkg_prefix}/share/doc/hipfft/LICENSE.md

%check
%if %{with test}
%if %{with check}
%if 0%{?suse_version}
export LD_LIBRARY_PATH=%{__builddir}/library:$LD_LIBRARY_PATH
%{__builddir}/clients/staging/hipfft-test
%else
export LD_LIBRARY_PATH=%{_vpath_builddir}/library:$LD_LIBRARY_PATH
%{_vpath_builddir}/clients/staging/hipfft-test
%endif
%endif
%endif

%files
%if %{with gitcommit}
%license projects/hipfft/LICENSE.md
%doc projects/hipfft/README.md
%else
%license LICENSE.md
%doc README.md
%endif

%{pkg_prefix}/%{pkg_libdir}/libhipfft.so.0{,.*}
%{pkg_prefix}/%{pkg_libdir}/libhipfftw.so.0{,.*}

%files devel
%{pkg_prefix}/include/hipfft/
%{pkg_prefix}/%{pkg_libdir}/libhipfft.so
%{pkg_prefix}/%{pkg_libdir}/libhipfftw.so
%{pkg_prefix}/%{pkg_libdir}/cmake/hipfft/

%if %{with test}
%files test
%{pkg_prefix}/bin/hipfft-test
%endif

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 22 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-4
- Add --with compat

* Thu Dec 11 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-3
- Fix building -test, disable lto

* Thu Nov 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-2
- Remove dir tags

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Sat Oct 11 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.2-1
- Update to 7.0.2

* Thu Sep 25 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-2
- Require a new rocm runtime

* Sat Sep 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.0-1
- Update to 7.0.1

* Wed Aug 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-4
- Add Fedora copyright

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Simplify file removal

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-2
- Remove -mtls-dialect cflag

* Thu Jul 24 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2
- Fix spurious tab in spec file

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-4
- Remove suse check of ldconfig

* Tue May 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Cleanup module build

* Mon Apr 28 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Improve testing for suse

* Sat Apr 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Wed Feb 12 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-5
- Remove multibuild
- Fix SLE 15.6

* Mon Jan 20 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- multithread compress

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- build requires gcc-c++

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed


