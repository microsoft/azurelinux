# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# depends on downloading googletest src directory, use mock --enable-network
%bcond_with check

# So pre releases can be tried
%bcond_with gitcommit

%if %{with gitcommit}
# PyTorch 2.4+ has this error
# .../pytorch/aten/src/ATen/cpu/Utils.cpp:38:34: error: ‘cpuinfo_has_x86_amx_tile’ was not declared in this scope; did you mean ‘cpuinfo_has_x86_mmx_plus’?
#   38 |   return cpuinfo_initialize() && cpuinfo_has_x86_amx_tile();
#      |                                  ^~~~~~~~~~~~~~~~~~~~~~~~
#      |                                  cpuinfo_has_x86_mmx_plus
#
# Pick a more recent cpuinfo
%global commit0 1e83a2fdd3102f65c6f1fb602c1b320486218a99
Version:        24.09.26
%define patch_level 0

%else

# For PyTorch 2.5
%global commit0 1e83a2fdd3102f65c6f1fb602c1b320486218a99
Version:        24.09.26
%define patch_level 2

%endif

%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Summary:        A library to detect information about host CPU
Name:           cpuinfo
License:        BSD-2-Clause
Release:        %{patch_level}.git%{?shortcommit0}%{?dist}.2


URL:            https://github.com/pytorch/%{name}
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
# so version YY.M.D
Patch0:         0001-cpuinfo-fedora-cmake-changes.patch

ExclusiveArch:  x86_64 aarch64

BuildRequires:  cmake
BuildRequires:  gcc-c++
%if %{with check}
BuildRequires:  gtest-devel
%endif
BuildRequires:  make

%description
cpuinfo is a library to detect essential for performance
optimization information about host CPU.

Features
* Cross-platform availability:
  * Linux, Windows, macOS, Android, and iOS operating systems
  * x86, x86-64, ARM, and ARM64 architectures
* Modern C/C++ interface
  * Thread-safe
  * No memory allocation after initialization
  * No exceptions thrown
* Detection of supported instruction sets, up to AVX512 (x86)
  and ARMv8.3 extensions
* Detection of SoC and core information:
  * Processor (SoC) name
  * Vendor and microarchitecture for each CPU core
  * ID (MIDR on ARM, CPUID leaf 1 EAX value on x86) for each CPU core
* Detection of cache information:
  * Cache type (instruction/data/unified), size and line size
  * Cache associativity
  * Cores and logical processors (hyper-threads) sharing the cache
* Detection of topology information (relative between logical
  processors, cores, and processor packages)
* Well-tested production-quality code:
  * 60+ mock tests based on data from real devices
  * Includes work-arounds for common bugs in hardware and OS kernels
  * Supports systems with heterogenous cores, such as big.LITTLE and Max.Med.Min
* Permissive open-source license (Simplified BSD)

%package devel
Summary:        Headers and libraries for cpuinfo
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the developement libraries and headers
for cpuinfo.

%prep
%autosetup -p1 -n %{name}-%{commit0}

# Patch the version patch
sed -i -e 's@cpuinfo_VERSION 23.11.04@cpuinfo_VERSION %{version}@' CMakeLists.txt

%build
%cmake \
%if %{with check}
    -DCPUINFO_BUILD_UNIT_TESTS=ON \
%else
    -DCPUINFO_BUILD_UNIT_TESTS=OFF \
%endif
    -DCPUINFO_BUILD_MOCK_TESTS=OFF \
    -DCPUINFO_BUILD_BENCHMARKS=OFF

%cmake_build

%install
%cmake_install

%if %{with check}
rm -rf %{buildroot}/%{_includedir}/gmock
rm -rf %{buildroot}/%{_includedir}/gtest
rm -rf %{buildroot}/%{_libdir}/cmake/GTest
rm -rf %{buildroot}/%{_libdir}/libgmock*
rm -rf %{buildroot}/%{_libdir}/libgtest*
rm -rf %{buildroot}/%{_libdir}/pkgconfig/gmock*
rm -rf %{buildroot}/%{_libdir}/pkgconfig/gtest*
%endif

%check
%if %{with check}
%ctest
%endif

%files
%license LICENSE
%{_bindir}/isa-info
%{_bindir}/cpu-info
%{_bindir}/cache-info
%ifarch x86_64
%{_bindir}/cpuid-dump
%endif
%{_libdir}/lib%{name}.so.*

%files devel
%doc README.md
%dir %{_datadir}/%{name}
%{_includedir}/%{name}.h
%{_datadir}/%{name}/%{name}-*.cmake
%{_libdir}/lib%{name}*.so
%{_libdir}/pkgconfig/lib%{name}.pc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.09.26-2.git1e83a2f.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat May 3 2025 Tom Rix <Tom.Rix@amd.com> - 24.09.26-2.git1e83a2f.1
- Move license to main package

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.09.26-1.git1e83a2f.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.11.04-0.gitd6860c4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 10 2024 Tom Rix <trix@redhat.com> - 23.11.04-0.gitd6860c4
- Update for pytorch 2.3

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2.14-3.giteb4a667.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 23.2.14-3.giteb4a667.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Tom Rix <trix@redhat.com> - 23.2.14-3.giteb4a667
- Add aarch64 to exclusive arch
- Make files more explicit
- Add opional check
- Fix license

* Wed Mar 29 2023 Tom Rix <trix@redhat.com> - 23.2.14-2.giteb4a667
- Simplify devel description
- Use dir tag for cpuinfo datadir

* Sun Mar 12 2023 Tom Rix <trix@redhat.com> - 23.2.14-1.giteb4a667
- Initial package

