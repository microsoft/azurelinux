# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 072586a71b55b7f8c584153d223e95687148a900
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20200517
# there is no debug package
%global debug_package %{nil}

Summary:        P(ortable) SIMD
Name:           psimd
License:        MIT
Version:        %{date0}.%{shortcommit0}
Release: 9%{?dist}

URL:            https://github.com/Maratyszcza
Source0:        %{url}/%{name}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc

%description
Portable 128-bit SIMD intrinsics

%package devel
Summary: P(ortable) SIMD
BuildArch:      noarch
Provides:       %{name}-static = %{version}-%{release}

%description devel
Portable 128-bit SIMD intrinsics

%prep
%autosetup -p1 -n %{name}-%{commit0}

# For CMake 4
sed -i -e 's@CMAKE_MINIMUM_REQUIRED(VERSION 2.8.12 FATAL_ERROR@CMAKE_MINIMUM_REQUIRED(VERSION 3.5@' CMakeLists.txt

%build
%cmake 
%cmake_build

%install
%cmake_install

%files devel
%doc README.md
%license LICENSE
%{_includedir}/psimd.h

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20200517.072586a-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Tom Rix <Tom.Rix@amd.com> - 20200517.072586a-7
- change minimal cmake version

* Sun Mar 16 2025 Tom Rix <Tom.Rix@amd.com> - 20200517.072586a-6
- Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20200517.072586a-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20200517.072586a-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20200517.072586a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20200517.072586a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 17 2023 Tom Rix <trix@redhat.com> - 20200517.072586a-1
- Initial release
