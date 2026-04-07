# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 63058eff77e11aa15bf531df5dd34395ec3017c8
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20201208
%global upstream_name FXdiv

Summary:        Header for division via fixed-point math
Name:           fxdiv
License:        MIT
Version:        1.0^git%{date0}.%{shortcommit0}
Release:        7%{?dist}

# Only a header
BuildArch:      noarch

URL:            https://github.com/Maratyszcza/%{name}
Source0:        %{url}/archive/%{commit0}/%{upstream_name}-%{shortcommit0}.tar.gz

Patch0:        0001-Prep-fxdiv-cmake-for-fedora-packaging.patch

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: gtest-devel

%description
Header-only library for division via fixed-point multiplication by inverse

On modern CPUs and GPUs integer division is several times slower
than multiplication. FXdiv implements an algorithm to replace an
integer division with a multiplication and two shifts. This
algorithm improves performance when an application performs repeated
divisions by the same divisor.

Features
  * Integer division for uint32_t, uint64_t, and size_t
  * Header-only library, no installation or build required
  * Compatible with C99, C++, OpenCL, and CUDA
  * Uses platform-specific compiler intrinsics for optimal performance
  * Covered with unit tests and microbenchmarks

%package devel

Summary:        Header for division via fixed-point math
Provides:       %{name}-static = %{version}-%{release}

%description devel
Header-only library for division via fixed-point multiplication by inverse

On modern CPUs and GPUs integer division is several times slower
than multiplication. FXdiv implements an algorithm to replace an
integer division with a multiplication and two shifts. This
algorithm improves performance when an application performs repeated
divisions by the same divisor.

Features
  * Integer division for uint32_t, uint64_t, and size_t
  * Header-only library, no installation or build required
  * Compatible with C99, C++, OpenCL, and CUDA
  * Uses platform-specific compiler intrinsics for optimal performance
  * Covered with unit tests and microbenchmarks

%prep
%autosetup -p1 -n %{upstream_name}-%{commit0}

%build

%cmake \
       -DFXDIV_USE_SYSTEM_LIBS=ON \
       -DFXDIV_BUILD_TESTS=ON \
       -DFXDIV_BUILD_BENCHMARKS=OFF \
       
%cmake_build

%check
%ctest

%install
%cmake_install

%files devel
%license LICENSE
%doc README.md
%{_includedir}/fxdiv.h

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20201208.63058ef-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20201208.63058ef-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20201208.63058ef-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20201208.63058ef-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0^git20201208.63058ef-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 23 2023 Tom Rix <trix@redhat.com> - 1.0^git20201208.63058ef-2
- Address review comments

* Fri Sep 15 2023 Tom Rix <trix@redhat.com> - 1.0^git20201208.63058ef-1
- Initial package
