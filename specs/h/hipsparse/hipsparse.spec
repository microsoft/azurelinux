# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?suse_version}
%global hipsparse_name libhipsparse1
%else
%global hipsparse_name hipsparse
%endif

%global upstreamname hipSPARSE
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

# Assumes gpu hw
%bcond_with check

# downloads tests, use mock --enable-network
%bcond_with test
%if %{with test}
%global build_test ON
%global __brp_check_rpaths %{nil}
%else
%global build_test OFF
%endif

# gfortran and clang rpm macros do not mix
%global build_fflags %{nil}

# Compression type and level for source/binary package payloads.
#  "w7T0.xzdio"	xz level 7 using %%{getncpus} threads
%global _source_payload w7T0.xzdio
%global _binary_payload w7T0.xzdio

Name:           %{hipsparse_name}
Version:        %{rocm_version}
Release:        1%{?dist}
Summary:        ROCm SPARSE marshalling library
Url:            https://github.com/ROCmSoftwarePlatform/%{upstreamname}
License:        MIT

Source0:        %{url}/archive/rocm-%{rocm_version}.tar.gz#/%{upstreamname}-%{rocm_version}.tar.gz
Patch1:         0002-refactor-setting-matrices-download-dir.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if 0%{?suse_version}
BuildRequires:  gcc-fortran
%else
BuildRequires:  gcc-gfortran
%endif
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocprim-static
BuildRequires:  rocsparse-devel

%if %{with test}
BuildRequires:  gtest-devel
BuildRequires:  rocblas-devel
%if 0%{?suse_version}
BuildRequires:  rocm-libomp-devel
%else
BuildRequires:  libomp-devel
%endif
%endif

Provides:       hipsparse = %{version}-%{release}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

%description
hipSPARSE is a SPARSE marshalling library with multiple
supported backends. It sits between your application and
a 'worker' SPARSE library, where it marshals inputs to
the backend library and marshals results to your
application. hipSPARSE exports an interface that doesn't
require the client to change, regardless of the chosen
backend. Currently, hipSPARSE supports rocSPARSE and
cuSPARSE backends.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%package devel
Summary:        Libraries and headers for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       hipsparse-devel = %{version}-%{release}

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
    -DCMAKE_BUILD_TYPE=%build_type \
    -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    -DCMAKE_SKIP_RPATH=ON \
    -DBUILD_FILE_REORG_BACKWARD_COMPATIBILITY=OFF \
    -DROCM_SYMLINK_LIBS=OFF \
    -DHIP_PLATFORM=amd \
    -DAMDGPU_TARGETS=%{rocm_gpu_list_default} \
    -DCMAKE_INSTALL_LIBDIR=%_libdir \
    -DBUILD_CLIENTS_BENCHMARKS=%{build_test} \
    -DBUILD_CLIENTS_SAMPLES=OFF \
    -DBUILD_CLIENTS_TESTS=%{build_test} \
    -DBUILD_CLIENTS_TESTS_OPENMP=OFF \
%if %{with test}
    -DCMAKE_MATRICES_DIR=%{_builddir}/%{name}-test-matrices/ \
%endif
    -DBUILD_FORTRAN_CLIENTS=OFF

%cmake_build

%if %{with test}
%if %{with check}
%check
gpu=default
find . -name 'hipsparse-test' -exec {} \;
%endif
%endif

%install
%cmake_install

if [ -f %{buildroot}%{_prefix}/share/doc/hipsparse/LICENSE.md ]; then
    rm %{buildroot}%{_prefix}/share/doc/hipsparse/LICENSE.md
fi

%if %{with test}
mkdir -p %{buildroot}/%{_datadir}/%{name}/matrices
install -pm 644 %{_builddir}/%{name}-test-matrices/* %{buildroot}/%{_datadir}/%{name}/matrices
%endif

%files
%license LICENSE.md
%{_libdir}/libhipsparse.so.1{,.*}

%files devel
%doc README.md
%dir %{_libdir}/cmake/hipsparse
%dir %{_includedir}/hipsparse
%{_includedir}/hipsparse/*
%{_libdir}/libhipsparse.so
%{_libdir}/cmake/hipsparse/*.cmake

%if %{with test}
%files test
%dir %{_datadir}/hipsparse
%{_bindir}/hipsparse*
%{_datadir}/hipsparse/test/*
%{_datadir}/hipsparse/matrices/*
%endif

%changelog
* Tue Sep 30 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.4-1
- Update to 6.4.4

* Wed Jul 30 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.2-2
- Remove -mtls-dialect cflag

* Thu Jul 24 2025 Jeremy Newton <alexjnewt at hotmail dot com> - 6.4.2-1
- Update to 6.4.2

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 19 2025 Tim Flink <tflink@fedoraproject.org> - 6.4.0-4
- rework test subpackage to include test data in a predictable location

* Mon Jun 16 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-3
- Remove suse check of ldconfig

* Wed May 14 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-2
- Cleanup module build

* Sat Apr 19 2025 Tom Rix <Tom.Rix@amd.com> - 6.4.0-1
- Update to 6.4.0

* Thu Feb 13 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-5
- Remove multi build
- Fix SLE 15.6

* Tue Jan 21 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-4
- multithread compress

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 Tom Rix <Tom.Rix@amd.com> - 6.3.0-2
- build requires gcc-c++

* Tue Dec 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.3.0-1
- Update to 6.3

* Sun Nov 10 2024 Tom Rix <Tom.Rix@amd.com> - 6.2.1-1
- Stub for tumbleweed

