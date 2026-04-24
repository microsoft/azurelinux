# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 eebb229d08057617f172968df68d145f614a8a09
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20250526

# Testing is broken
%bcond_with test
%if %{with test}
%global build_test ON
%else
%global build_test OFF
%endif

%bcond_with debug
%if %{with debug}
%global build_type DEBUG
%else
%global build_type RelWithDebInfo
%endif

Summary:        Architected Queuing Language Profiling Library
Name:           aqlprofile
License:        MIT
Version:        0.0^git%{date0}.%{shortcommit0}
Release: 3%{?dist}

# Only x86_64 works right now:
ExclusiveArch:  x86_64

Url:            https://github.com/ROCm/aqlprofile
Source0:        %{url}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  rocm-compilersupport-macros
BuildRequires:  rocm-runtime-devel

%description
AQLprofile is an open source library that enables advanced GPU
profiling and tracing on AMD platforms. It works in conjunction
with rocprofiler-sdk to support profiling methods such as
performance counters (PMC) and SQ thread trace (SQTT).
AQLprofile provides the foundational mechanisms for constructing
AQL packets and managing profiling operations across multiple
AMD GPU architecture families.

%package devel
Summary:        The development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -n %{name}-%{commit0}

# Do not hardcode CMAKE_BUILD_TYPE
# https://github.com/ROCm/aqlprofile/issues/12
sed -i -e 's@CMAKE_BUILD_TYPE@DO_NO_HARDCODE_CMAKE_BUILD_TYPE@' cmake_modules/env.cmake

%build
%cmake \
  -DCMAKE_BUILD_TYPE=%{build_type} \
  -DAQLPROFILE_BUILD_TESTS=%{build_test} \
  -DCMAKE_PREFIX_PATH=%{rocmllvm_cmakedir}/.. \
    
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%{_libdir}/libhsa-amd-aqlprofile64.so.1{,.*}

%files devel
%doc README.md
%dir %{_includedir}/aqlprofile-sdk
%{_includedir}/aqlprofile-sdk/*.h
%{_libdir}/libhsa-amd-aqlprofile64.so

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.0^git20250526.eebb229-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 1 2025 Tom Rix <Tom.Rix@amd.com> - 0.0^git20250526.eebb229-1
- Initial package

