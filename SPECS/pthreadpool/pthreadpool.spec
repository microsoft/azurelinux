# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 4fe0e1e183925bf8cfa6aae24237e724a96479b8
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20230829

Summary:        Portable thread pool
Name:           pthreadpool
License:        BSD-2-Clause
Version:        0.0^git%{date0}.%{shortcommit0}
Release:        7%{?dist}

URL:            https://github.com/Maratyszcza/%{name}
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

Patch0:        0001-pthreadpool-fedora-cmake-changes.patch

BuildRequires: cmake
BuildRequires: fxdiv-devel
BuildRequires: gcc-c++
BuildRequires: gtest-devel

%description
pthreadpool is a portable and efficient thread pool
implementation. It provides similar functionality
to #pragma omp parallel for, but with additional features.

Features:
* C interface (C++-compatible).
* 1D-6D loops with step parameters.
* Run on user-specified or auto-detected number of threads.
* Work-stealing scheduling for efficient work balancing.
* Wait-free synchronization of work items.
* Compatible with Linux (including Android), macOS,
  iOS, Windows, Emscripten environments.
* 100% unit tests coverage.
* Throughput and latency microbenchmarks.

%package devel

Summary:        Portable thread pool
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
pthreadpool is a portable and efficient thread pool
implementation. It provides similar functionality
to #pragma omp parallel for, but with additional features.

Features:
* C interface (C++-compatible).
* 1D-6D loops with step parameters.
* Run on user-specified or auto-detected number of threads.
* Work-stealing scheduling for efficient work balancing.
* Wait-free synchronization of work items.
* Compatible with Linux (including Android), macOS,
  iOS, Windows, Emscripten environments.
* 100% unit tests coverage.
* Throughput and latency microbenchmarks.

%prep
%autosetup -p1 -n %{name}-%{commit0}

%build

%cmake \
       -DPTHREADPOOL_USE_SYSTEM_LIBS=ON \
       -DPTHREADPOOL_BUILD_BENCHMARKS=OFF \
       
%cmake_build

%check
%ctest

%install
%cmake_install

%files
%license LICENSE
%{_libdir}/lib%{name}.so.*

%files devel
%doc README.md
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0^git20230829.4fe0e1e-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0^git20230829.4fe0e1e-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0^git20230829.4fe0e1e-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0^git20230829.4fe0e1e-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0^git20230829.4fe0e1e-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 2 2023 Tom Rix <trix@redhat.com> - 0.0^git20230829.4fe0e1e-2
- Address review comments

* Sat Sep 16 2023 Tom Rix <trix@redhat.com> - 1.0^git20230829.4fe0e1e-1
- Initial package
