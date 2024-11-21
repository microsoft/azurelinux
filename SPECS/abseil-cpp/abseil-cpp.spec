# Installed library version
%global lib_version 2401.0.0
%define lib_ver_min %(echo %{lib_version} | cut -d. -f1-2)

Summary:        C++ Common Libraries
Name:           abseil-cpp
Version:        20240116.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://abseil.io
Source0:        https://github.com/abseil/abseil-cpp/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 3.20.0
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  gmock-devel
BuildRequires:  gtest
BuildRequires:  gtest-devel

%if 0%{?with_check}
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  gmock
%endif

%description
Abseil is an open-source collection of C++ library code designed to augment
the C++ standard library. The Abseil library code is collected from
Google's own C++ code base, has been extensively tested and used in
production, and is the same code we depend on in our daily coding lives.

In some cases, Abseil provides pieces missing from the C++ standard; in
others, Abseil provides alternatives to the standard for special needs we've
found through usage in the Google code base. We denote those cases clearly
within the library code we provide you.

Abseil is not meant to be a competitor to the standard library; we've just
found that many of these utilities serve a purpose within our code base,
and we now want to provide those resources to the C++ community as a whole.

%package testing
Summary:        Libraries needed for running tests on the installed %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description testing
%{summary}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers for %{name}

%prep
%autosetup -p1 -S gendiff

%build
%cmake \
%if 0%{?with_check}
  -GNinja \
%endif
  -DABSL_USE_EXTERNAL_GOOGLETEST:BOOL=ON \
  -DABSL_FIND_GOOGLETEST:BOOL=ON \
  -DABSL_ENABLE_INSTALL:BOOL=ON \
  -DABSL_BUILD_TESTING:BOOL=ON \
  -DABSL_BUILD_TEST_HELPERS:BOOL=ON \
  -DCMAKE_BUILD_TYPE:STRING=None \
  -DCMAKE_CXX_STANDARD:STRING=17
%cmake_build

%install
%cmake_install

%check
%ctest --output-on-failure

%files
%license LICENSE
%doc FAQ.md README.md UPGRADES.md
%{_libdir}/libabsl_*.so.%{lib_ver_min}.*

%files devel
%{_includedir}/absl
%{_libdir}/cmake/absl
%{_libdir}/libabsl_*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Mar 19 2024 Betty Lakes <bettylakes@microsoft.com> - 20240116.0-1
- Upgrade version to 20240116.0

* Sun Dec 17 2023 Muhammad Falak <mwani@microsoft.com> - 20230802.1-1
- Bump version to 20230802.1

* Thu Jun 30 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 20220623.0-1
- Updating to 20220623.0 to remove workaround patches for GTest.

* Mon Nov 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20211102.0-1
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- License verified.
- Updating to version 20211102.0.
- Removing redundant type fix patch.
- Adding patches removing use of unpublished GTest macros and matchers from the test code.

* Mon Mar 08 2021 Rich Mattes <richmattes@gmail.com> - 20200923.3-1
- Update to release 20200923.3

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200923.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 2020 Rich Mattes <richmattes@gmail.com> - 20200923.2-1
- Update to release 20200923.2
- Rebuild to fix tagging in koji (rhbz#1885561)

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200225.2-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200225.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 27 2020 Rich Mattes <richmattes@gmail.com> - 20200225.2-2
- Don't remove buildroot in install

* Sun May 24 2020 Rich Mattes <richmattes@gmail.com> - 20200225.2-1
- Initial package.
