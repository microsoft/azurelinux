# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel} < 9
# Needed for EPEL8
%undefine __cmake_in_source_build
%endif

# For ROCm
%if 0%{?fedora}
%ifarch x86_64
%bcond_without rocm
%endif
%endif

%if %{with rocm}
# Kokkos only builds one gpu at a time, so need to loop over them
# $gpu will be evaluated in the loops below
%global _vpath_builddir %{_vendor}-%{_target_os}-build-${gpu:-normal}

# For testing gpus, depends on having a gpu
%bcond_with rocm_test
%if %{with rocm_test}
# Only build the for the gpu you are testing
%global gpu_test gfx1100
%global kokkos_gpu_list %{gpu_test}
%global build_rocm_test ON
%else
# kokkos only supports some GPUs, of these pick the important ones
%global kokkos_gpu_list gfx942 gfx90a gfx1100
%global build_rocm_test OFF
%endif

# hippc is clang based, the toolchain is gcc, remove the gcc options that are not supported on clang
%global rocm_cxxflags %(echo %{optflags} | sed -E 's/-specs=[^ ]+//g; s/-Wno-complain-wrong-lang//g; s/-fexceptions//g; s/-fstack-clash-protection//g; s/-fcf-protection//g; s/-ffat-lto-objects//g; s/-Xarch_host//g; s/-mtls-dialect=[^ ]+//g; s/-flto=auto//g; s/-grecord-gcc-switches/-frecord-command-line/g; s/-Wp,-U_FORTIFY_SOURCE,-D_FORTIFY_SOURCE=3//g; s/-Wp,-D_GLIBCXX_ASSERTIONS//g; s/-mno-omit-leaf-frame-pointer//g; s/[[:space:]]+/ /g')
%endif

Name:           kokkos
Version:        4.7.02
%global         sover 4.7
Release:        1%{?dist}
Summary:        Kokkos C++ Performance Portability Programming
# no support for 32-bit archs https://github.com/kokkos/kokkos/issues/2312
ExcludeArch: i686 armv7hl

License:        Apache-2.0 WITH LLVM-exception
URL:            https://github.com/kokkos/kokkos
Source0:        %{url}/releases/download/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.16
BuildRequires:  hwloc-devel
%if 0%{?rhel} == 9
%global gts_version 13
BuildRequires: gcc-toolset-%{gts_version}
%endif
%if %{with rocm}
BuildRequires:  rocm-cmake
BuildRequires:  rocm-comgr-devel
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-hip-devel
BuildRequires:  rocm-rpm-macros
BuildRequires:  rocm-rpm-macros-modules
BuildRequires:  rocm-runtime-devel
BuildRequires:  rocprim-devel
BuildRequires:  rocthrust-devel
Requires:       rocm-rpm-macros-modules
%endif


%global kokkos_desc \
Kokkos Core implements a programming model in C++ for writing performance \
portable applications targeting all major HPC platforms. For that purpose \
it provides abstractions for both parallel execution of code and data \
management.  Kokkos is designed to target complex node architectures with \
N-level memory hierarchies and multiple types of execution resources. It \
currently can use OpenMP, Pthreads and CUDA as backend programming models.

%description
%{kokkos_desc}

%package devel
Summary:        Development package for  %{name} packages
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       hwloc-devel
%description devel
%{kokkos_desc}

This package contains the development files of %{name}.

%package -n %{name}-rocm
Summary:        %{name} ROCm package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n %{name}-rocm
%{summary}

%package -n %{name}-rocm-devel
Summary:        %{name} ROCm development package
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description -n %{name}-rocm-devel
%{summary}

%prep
%autosetup -p1

%build

%{?el9:. /opt/rh/gcc-toolset-%{gts_version}/enable}
%cmake \
  -DKokkos_ENABLE_TESTS=On \
%ifarch ppc64le
  -DKokkos_ARCH_POWER8=ON \
%endif
  -DCMAKE_INSTALL_INCLUDEDIR=include/kokkos \
  -DKokkos_ENABLE_AGGRESSIVE_VECTORIZATION=ON \
  -DKokkos_ENABLE_DEPRECATED_CODE=ON \
  -DKokkos_ENABLE_OPENMP=ON \
  -DKokkos_ENABLE_SERIAL=ON \
  -DKokkos_ENABLE_HWLOC=ON \
  -DKokkos_ENABLE_HIP=OFF \
  %{nil}
%cmake_build

%if %{with rocm}
rocm_clang=`hipconfig -l`/clang++
for gpu in %{kokkos_gpu_list}
do
    module load rocm/$gpu
    ugpu=${gpu^^}
    %cmake \
	   -DCMAKE_CXX_COMPILER=${rocm_clang} \
	   -DCMAKE_CXX_FLAGS="%{rocm_cxxflags}" \
	   -DCMAKE_CXX_STANDARD=17 \
	   -DCMAKE_INSTALL_BINDIR=$ROCM_BIN \
	   -DCMAKE_INSTALL_INCLUDEDIR=%{_libdir}/rocm/${gpu}/include/kokkos \
	   -DCMAKE_INSTALL_LIBDIR=$ROCM_LIB \
	   -DKokkos_ARCH_AMD_${ugpu}=ON \
	   -DKokkos_ENABLE_AGGRESSIVE_VECTORIZATION=ON \
	   -DKokkos_ENABLE_DEPRECATED_CODE=ON \
	   -DKokkos_ENABLE_HIP=ON \
	   -DKokkos_ENABLE_HWLOC=ON \
	   -DKokkos_ENABLE_OPENMP=OFF \
	   -DKokkos_ENABLE_SERIAL=ON \
	   -DKokkos_ENABLE_TESTS=%{build_rocm_test}

    %cmake_build
    module purge
done
%endif

%install

%cmake_install

%if %{with rocm}
for gpu in %{kokkos_gpu_list}
do
    %cmake_install
done
%endif

%check
# https://github.com/kokkos/kokkos/issues/2959 - unstable test
%ifarch s390x
%global testargs --exclude-regex KokkosCore_UnitTest_StackTraceTest
%endif
%ctest %{?testargs} --timeout 6000

%if %{with rocm_test}
gpu=%{gpu_test}
module load rocm/$gpu
%ctest %{?testargs} --timeout 6000
module purge
%endif

%files
%doc README.md
%license LICENSE
%{_libdir}/libkokkos*.so.%{sover}*

%files devel
%{_includedir}/kokkos
%{_libdir}/libkokkos*.so
%{_libdir}/cmake/Kokkos
%{_bindir}/nvcc_wrapper
%{_bindir}/hpcbind
%{_bindir}/kokkos_launch_compiler

%if %{with rocm}
%files -n %{name}-rocm
%{_libdir}/rocm/gfx*/lib/libkokkos*.so.%{sover}*

%files -n %{name}-rocm-devel
%{_libdir}/rocm/gfx*/lib/libkokkos*.so
%{_libdir}/rocm/gfx*/lib/cmake/Kokkos
%{_libdir}/rocm/gfx*/bin/nvcc_wrapper
%{_libdir}/rocm/gfx*/bin/hpcbind
%{_libdir}/rocm/gfx*/bin/kokkos_launch_compiler
%{_libdir}/rocm/gfx*/include/kokkos
%endif


%changelog
* Sat Feb 21 2026 Richard Berger <richard.berger@outlook.com> - 4.7.02-1
- Version bump to v4.7.02

* Sat Aug 2 2025 Richard Berger <richard.berger@outlook.com> - 4.6.02-1
- Version bump to v4.6.02

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 20 2025 Richard Berger <richard.berger@outlook.com> - 4.6.00-1
- Version bump to v4.6.00

* Sat Feb 15 2025 Richard Berger <richard.berger@outlook.com> - 4.5.01-2
- update license to Apache-2.0 WITH LLVM-exception

* Fri Feb 14 2025 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 4.5.01-1
- Version bump to v4.5.01 (bug #2264022)

* Wed Feb 05 2025 Christoph Junghans <junghans@votca.org> - 4.4.01-4
- Use ROCM_INCLUDE for install

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 3 2025 Tom Rix <Tom.Rix@amd.com> - 4.4.01-2
- Add ROCm support

* Sat Nov 30 2024 Richard Berger <richard.berger@outlook.com> - 4.4.01-1
- Version bump to v4.4.01

* Mon Sep 2 2024 Richard Berger <richard.berger@outlook.com> - 4.3.01-1
- Version bump to v4.3.01

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 4.2.00-5
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.00-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.00-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 4.2.00-1
- Version bump to v4.2.00 (bug #2250814)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 4.1.00-1
- Version bump to v4.1.00 (bug #2175429)

* Wed May 10 2023 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 4.0.01-1
- Version bump to v4.0.01 (bug #2175429)

* Mon Mar 06 2023 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 4.0.00-1
- Version bump to v4.0.00 (bug #2175429)

* Tue Feb 28 2023 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 3.7.01-3
- Fix missing include

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 3.7.01-1
- Version bump to v3.7.01 (bug #2151701)

* Thu Sep 22 2022 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 3.7.00-1
- Version bump to v3.7.00 (bug #2128805)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 06 2022 Cezary Skrzyński <cezary.skrzynski@ng-analytics.com> - 3.6.01-1
- Version bump to v3.6.01 (bug #2103824)

* Wed Apr 27 2022 Christoph Junghans <junghans@votca.org> - 3.6.00-1
- Version bump to v3.6.00 (bug #2026409)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 01 2021 Christoph Junghans <junghans@votca.org> - 3.5.00-1
- Version bump to v3.5.00 (bug #2026409)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Christoph Junghans <junghans@votca.org> - 3.4.01-2
- Rebuild for glibc (no libdl.so anymore)

* Fri May 28 2021 Christoph Junghans <junghans@votca.org> - 3.4.01-1
- Version bump to v3.4.01 (bug #1965296)

* Tue Apr 27 2021 Christoph Junghans <junghans@votca.org> - 3.4.00-1
- Version bump to v3.4.00 (bug #1953967)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 23 08:19:42 MST 2021 Christoph Junghans <junghans@lanl.gov> - 3.3.01-1
- Version bump to v3.3.01 (bug #1919508)

* Sat Dec 19 13:38:32 MST 2020 Christoph Junghans <junghans@votca.org> - 3.3.00-1
- Version bump to v3.3.00 (bug #1909362)

* Wed Nov 25 15:26:40 MST 2020 Christoph Junghans <junghans@votca.org> - 3.2.01-1
- Version bump to v3.2.01 (bug #1901667)

* Tue Aug 25 2020 Christoph Junghans <junghans@votca.org> - 3.2.00-2
- Fix cmake targets

* Tue Aug 25 2020 Christoph Junghans <junghans@votca.org> - 3.2.00-1
- Version bump to v3.2.00 (bug #1872456)

* Mon Aug 03 2020 Christoph Junghans <junghans@votca.org> - 3.1.01-4
- Fix out-of-source build on F33 (bug #1863948)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.01-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 06 2020 Christoph Junghans <junghans@votca.org> - 3.1.01-1
- Version bump to v3.1.01 (bug #1824998)
- drop 2961.patch - merge upstream

* Thu Apr 16 2020 Christoph Junghans <junghans@votca.org> - 3.1.00-1
- Version bump to v3.1.00 (bug #1824998)

* Thu Feb 27 2020 Christoph Junghans <junghans@votca.org> - 3.0.00-1
- Version bump to 3.0.00

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-0.3.20200107gite79d6b7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Christoph Junghans <junghans@votca.org> - 3.0.0-0.2.20200107gite79d6b7.1
- Added missing hwloc dep

* Sun Jan 12 2020 Christoph Junghans <junghans@votca.org> - 3.0.0-0.2.20200107gite79d6b7
- bump to latest release candidate snapshot

* Mon Dec 23 2019 Christoph Junghans <junghans@votca.org> - 3.0.0-0.2.20191219gitcb90e9
- bump to latest release candidate snapshot

* Fri Dec 20 2019 Christoph Junghans <junghans@votca.org> - 3.0.0-0.2.20191216git6619d83
- bump to latest snapshot and enable Kokkos_ENABLE_DEPRECATED_CODE
- disable StackTrace Unittests

* Sun Sep 29 2019 Christoph Junghans <junghans@votca.org> - 3.0.0-0.2.20190929git445c176
- bump to latest snapshot and enable AGGRESSIVE_VECTORIZATION

* Wed Sep 18 2019 Christoph Junghans <junghans@votca.org> - 3.0.0-0.1.190912gitd93e239
- initial commit (bug #1751409)
