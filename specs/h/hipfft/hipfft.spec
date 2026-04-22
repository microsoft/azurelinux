# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?suse_version}
%global hipfft_name libhipfft0
%else
%global hipfft_name hipfft
%endif

%global upstreamname hipFFT
%global rocm_release 6.4
%global rocm_patch 4
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
Version:        %{rocm_version}
Release: 2%{?dist}
Summary:        ROCm FFT marshalling library
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT

# Only x86_64 works right now
ExclusiveArch:  x86_64

Source0:        %{url}/archive/rocm-%{version}.tar.gz#/%{upstreamname}-rocm-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocprim-devel
BuildRequires:  rocfft-devel

%if %{with test}

BuildRequires:  boost-devel
BuildRequires:  fftw-devel
BuildRequires:  hiprand-devel
BuildRequires:  rocrand-devel

%if 0%{?suse_version}
BuildRequires:  gtest
BuildRequires:  libboost_program_options-devel
%else
BuildRequires:  gtest-devel
%endif

%endif

Provides:       hipfft = %{version}-%{release}

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
Provides:       hipfft-devel = %{version}-%{release}

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
%autosetup -n %{upstreamname}-rocm-%{version} -p 1

# CMake Error at clients/tests/CMakeLists.txt:87 (find_package):
#   No "FindHIP.cmake" found in CMAKE_MODULE_PATH.
# Remove MODULE
sed -i -e 's@find_package( HIP MODULE REQUIRED )@find_package( HIP REQUIRED )@' clients/tests/CMakeLists.txt

%build
%cmake \
    -DCMAKE_CXX_COMPILER=hipcc \
    -DCMAKE_C_COMPILER=hipcc \
    -DCMAKE_LINKER=%rocmllvm_bindir/ld.lld \
    -DCMAKE_AR=%rocmllvm_bindir/llvm-ar \
    -DCMAKE_RANLIB=%rocmllvm_bindir/llvm-ranlib \
    -DCMAKE_BUILD_TYPE=%{build_type} \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DCMAKE_SKIP_RPATH=ON \
    -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DCMAKE_INSTALL_LIBDIR=%_libdir \
    -DBUILD_CLIENTS_TESTS=%{build_test} \
    -DBUILD_CLIENTS_TESTS_OPENMP=OFF \
    -DROCM_SYMLINK_LIBS=OFF \
    -DHIP_PLATFORM=amd

%cmake_build


%install
%cmake_install

if [ -f %{buildroot}%{_prefix}/share/doc/hipfft/LICENSE.md ]; then
    rm %{buildroot}%{_prefix}/share/doc/hipfft/LICENSE.md
fi

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
%license LICENSE.md
%{_libdir}/libhipfft.so.0{,.*}

%files devel
%doc README.md
%dir %{_libdir}/cmake/hipfft
%dir %{_includedir}/hipfft
%{_includedir}/hipfft/*
%{_libdir}/libhipfft.so
%{_libdir}/cmake/hipfft/*.cmake

%if %{with test}
%files test
%{_bindir}/hipfft-test
%endif

%changelog
* Tue Sep 30 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.4-1
- Update to 6.4.4

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


