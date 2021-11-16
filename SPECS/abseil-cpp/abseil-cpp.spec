Summary:        C++ Common Libraries
Name:           abseil-cpp
Version:        20211102.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://abseil.io
Source0:        https://github.com/abseil/abseil-cpp/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         abseil-cpp-20211102.0-typematch.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%if %{with_check}
BuildRequires:  gtest-devel
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

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers for %{name}

%prep
%autosetup -p1

%build
mkdir build
pushd build
%cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
%if %{with_check}
  -DBUILD_TESTING=ON \
  -DABSL_USE_GOOGLETEST_HEAD=OFF \
%else
  -DBUILD_TESTING=OFF \
%endif
  ..
%make_build

%install
pushd build
%make_install

%check
pushd build
ctest --output-on-failure

%files
%license LICENSE
%doc FAQ.md LTS.md README.md UPGRADES.md
%{_libdir}/libabsl_*.so

%files devel
%{_includedir}/absl
%{_libdir}/cmake/absl

%changelog
* Mon Nov 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20211102.0-1
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- License verified.
- Updating to version 20211102.0.

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
