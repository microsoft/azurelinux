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

%global upstreamname hipRAND
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
%global hiprand_name libhiprand1%{pkg_suffix}
%else
%global hiprand_name hiprand%{pkg_suffix}
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

%if 0%{?fedora}
%bcond_without test
%else
%bcond_with test
%endif
%if %{with test}
%global build_test ON
%else
%global build_test OFF
%endif

# Option to test suite for testing on real HW:
%bcond_with check
# For docs
%bcond_with doc

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

Name:           %{hiprand_name}
%if %{with gitcommit}
Version:        git%{date0}.%{shortcommit0}
Release:        3%{?dist}
%else
Version:        %{rocm_version}
Release:        6%{?dist}
%endif
Summary:        HIP random number generator
License:        MIT AND BSD-3-Clause
%if %{with gitcommit}
Url:            https://github.com/ROCm/rocm-libraries
Source0:        %{url}/archive/%{commit0}/rocm-libraries-%{shortcommit0}.tar.gz
%else
Url:            https://github.com/ROCm/%{upstreamname}
Source0:        %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-%{version}.tar.gz
%endif

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocm-cmake%{pkg_suffix}
BuildRequires:  rocm-comgr%{pkg_suffix}-devel
BuildRequires:  rocm-compilersupport%{pkg_suffix}-macros
BuildRequires:  rocm-hip%{pkg_suffix}-devel
BuildRequires:  rocm-rpm-macros%{pkg_suffix}
BuildRequires:  rocm-runtime%{pkg_suffix}-devel
BuildRequires:  rocrand%{pkg_suffix}-devel

%if %{with test}
%if 0%{?suse_version}
BuildRequires:  gtest
%else
BuildRequires:  gtest-devel
%endif
%endif

%if %{with doc}
BuildRequires:  doxygen
%endif

Provides:       hiprand%{pkg_suffix} = %{version}-%{release}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
hipRAND is a RAND marshalling library, with multiple supported backends. It
sits between the application and the backend RAND library, marshalling inputs
into the backend and results back to the application. hipRAND exports an
interface that does not require the client to change, regardless of the chosen
backend. Currently, hipRAND supports either rocRAND or cuRAND.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary:        The hipRAND development package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       rocrand%{pkg_suffix}-devel
Provides:       hiprand%{pkg_suffix}-devel = %{version}-%{release}

%description devel
The hipRAND development package.

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
cd projects/hiprand
%else
%autosetup -p1 -n %{upstreamname}-rocm-%{version}
%endif

#Remove RPATH:
sed -i '/INSTALL_RPATH/d' CMakeLists.txt

# On Tumbleweed Q2,2025
# /usr/include/gtest/internal/gtest-port.h:279:2: error: C++ versions less than C++14 are not supported.
#   279 | #error C++ versions less than C++14 are not supported.
# https://github.com/ROCm/hipRAND/issues/222
# Convert the c++11's to c++14
sed -i -e 's@set(CMAKE_CXX_STANDARD 11)@set(CMAKE_CXX_STANDARD 14)@' {,test/package/}CMakeLists.txt

%build
%if %{with gitcommit}
cd projects/hiprand
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
    -DBUILD_TEST=%{build_test} \
    -DROCM_SYMLINK_LIBS=OFF

%cmake_build

%install
%if %{with gitcommit}
cd projects/hiprand
%endif
%cmake_install

rm -f %{buildroot}%{pkg_prefix}/share/doc/hiprand/LICENSE.md
rm -f %{buildroot}%{pkg_prefix}/bin/hipRAND/CTestTestfile.cmake

%check
%if %{with test}
%if %{with check}
%if 0%{?suse_version}
export LD_LIBRARY_PATH=$PWD/build/library:$LD_LIBRARY_PATH
%endif

%ctest
%endif
%endif

%files
%if %{with gitcommit}
%doc projects/hiprand/README.md
%license projects/hiprand/LICENSE.md
%else
%doc README.md
%license LICENSE.md
%endif
%if %{with debug}
%{pkg_prefix}/%{pkg_libdir}/libhiprand-d.so.1{,.*}
%else
%{pkg_prefix}/%{pkg_libdir}/libhiprand.so.1{,.*}
%endif

%files devel
%{pkg_prefix}/include/hiprand/
%if %{with debug}
%{pkg_prefix}/%{pkg_libdir}/libhiprand-d.so
%else
%{pkg_prefix}/%{pkg_libdir}/libhiprand.so
%endif
%{pkg_prefix}/%{pkg_libdir}/cmake/hiprand/

%if %{with test}
%files test
%{pkg_prefix}/bin/test*
%endif

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 22 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-5
- Add --with compat

* Wed Dec 10 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-4
- Fix debug install

* Thu Nov 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-3
- Remove dir tags

* Mon Nov 17 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 7.1.0-2
- Rebuilt for gtest 1.17.0

* Fri Oct 31 2025 Tom Rix <Tom.Rix@amd.com> - 7.1.0-1
- Update to 7.1.0

* Mon Oct 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-2
- Turn on -test for fedora

* Sat Sep 20 2025 Tom Rix <Tom.Rix@amd.com> - 7.0.1-1
- Update to 7.0.1

* Wed Aug 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-6
- Add Fedora copyright

* Mon Aug 25 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-5
- Simplify file removal

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-4
- Remove -mtls-dialect cflag

* Mon Jul 28 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-3
- Remove debian dir

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Mon Jun 16 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-4
- Remove suse check of ldconfig

* Mon May 12 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Cleanup module build

* Sun Apr 27 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Improve testing on suse

* Sat Apr 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Fri Apr 4 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-6
- Use correct spdx license
- cleanup

* Tue Feb 11 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-5
- Remove split building
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


