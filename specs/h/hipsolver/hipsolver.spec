# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?suse_version}
%global hipsolver_name libhipsolver0
%else
%global hipsolver_name hipsolver
%endif

%global upstreamname hipSOLVER
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

Name:           %{hipsolver_name}
Version:        %{rocm_version}
Release: 3%{?dist}
Summary:        ROCm SOLVER marshalling library
Url:            https://github.com/ROCm/%{upstreamname}
License:        MIT

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  rocblas-devel
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocsolver-devel
BuildRequires:  rocsparse-devel
%if 0%{?fedora}
BuildRequires:  suitesparse-devel
%endif

%if %{with test}
BuildRequires:  gtest-devel
BuildRequires:  hipsparse-devel
%if 0%{?suse_version}
BuildRequires:  blas-devel
BuildRequires:  cblas-devel
BuildRequires:  lapack-devel
%else
BuildRequires:  blas-static
BuildRequires:  lapack-static
%endif
%endif

Provides:       hipsolver = %{version}-%{release}

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
Provides:       hipsolver-devel = %{version}-%{release}

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
    -DROCM_SYMLINK_LIBS=OFF \
    -DHIP_PLATFORM=amd \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DCMAKE_INSTALL_LIBDIR=%_libdir \
    -DBUILD_CLIENTS_TESTS=%{build_test}

%cmake_build

%install
%cmake_install

if [ -f %{buildroot}%{_prefix}/share/doc/hipsolver/LICENSE.md ]; then
    rm %{buildroot}%{_prefix}/share/doc/hipsolver/LICENSE.md
fi

%files
%license LICENSE.md
%{_libdir}/libhipsolver.so.0{,.*}

%files devel
%doc README.md
%dir %{_libdir}/cmake/hipsolver
%dir %{_includedir}/hipsolver
%{_includedir}/hipsolver/*
%{_libdir}/libhipsolver.so
%{_libdir}/cmake/hipsolver/*.cmake

%if %{with test}
%files test
%dir %{_datadir}/hipsolver
%{_datadir}/hipsolver/test/*
%{_bindir}/hipsolver*
%endif

%changelog
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
