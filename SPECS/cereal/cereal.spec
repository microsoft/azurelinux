# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Debuginfo packages are disabled to prevent rpmbuild from generating an empty
# debuginfo package for the empty main package.
%global debug_package %{nil}
%bcond mingw %[%{undefined rhel} || %{defined epel}]

Name:           cereal
Version:        1.3.2
Release:        11%{?dist}
Summary:        A header-only C++11 serialization library
# include/cereal/details/polymorphic_impl.hpp is BSL-1.0
# include/cereal/external/base64.hpp is Zlib
# include/cereal/external/rapidjson/ is MIT
# include/cereal/external/rapidxml/license.txt is MIT OR BSL-1.0
License:        BSD-3-Clause AND BSL-1.0 AND Zlib AND MIT AND (MIT OR BSL-1.0)
Url:            http://uscilab.github.io/cereal/
Source0:        https://github.com/USCiLab/cereal/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  boost-devel
BuildRequires:  cmake >= 3.0

%if %{with mingw}
BuildRequires:  mingw32-filesystem >= 95  
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-boost

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-boost
%endif

%description
cereal is a header-only C++11 serialization library. cereal takes arbitrary
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast,
light-weight, and easy to extend - it has no external dependencies and can be
easily bundled with other code or used standalone.

%package devel
Summary:        Development headers and libraries for %{name}
Provides:       %{name}-static = %{version}-%{release}

%description devel
cereal is a header-only C++11 serialization library. cereal takes arbitrary
data types and reversibly turns them into different representations, such as
compact binary encodings, XML, or JSON. cereal was designed to be fast,
light-weight, and easy to extend - it has no external dependencies and can be
easily bundled with other code or used standalone.

This package contains development headers and libraries for the cereal library


%if %{with mingw}
%package -n mingw32-%{name}
Summary:       MinGW Windows %{name} library

%description -n mingw32-%{name}
MinGW Windows %{name} library.

%package -n mingw64-%{name}
Summary:       MinGW Windows %{name} library

%description -n mingw64-%{name}
MinGW Windows %{name} library.
%endif

%prep
%setup -q

%build
%{cmake} -DSKIP_PORTABILITY_TEST=ON -DWITH_WERROR=OFF
%cmake_build

%if %{with mingw}
# MinGW build
%mingw_cmake -DSKIP_PORTABILITY_TEST=ON -DBUILD_SANDBOX=OFF -DWITH_WERROR=OFF
%mingw_make_build
%endif

%install
%cmake_install
%if %{with mingw}
%mingw_make_install
%mingw_debug_install_post
%endif

%check
# https://github.com/USCiLab/cereal/issues/744
%ifarch ppc64le
%global testargs --exclude-regex '\(test_complex\|test_pod\)'
%endif
%ctest  --output-on-failure %{?testargs}

%files devel
%doc README.md
%license LICENSE
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}

%if %{with mingw}
%files -n mingw32-%{name}
%doc README.md
%license LICENSE
%{mingw32_includedir}/%{name}
%{mingw32_libdir}/cmake/%{name}
%files -n mingw64-%{name}
%doc README.md
%license LICENSE
%{mingw64_includedir}/%{name}
%{mingw64_libdir}/cmake/%{name}
%endif

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.3.2-9
- Disable mingw in RHEL builds

* Tue Oct 01 2024 Jean THOMAS <virgule@jeanthomas.me> - 1.3.2-8
- Add mingw32/mingw64 packages

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 01 2022 Christoph Junghans <junghans@votca.org> - 1.3.2-1
- Version bump v1.3.2 (bug #2059217)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Christoph Junghans <junghans@votca.org> - 1.3.1-1
- Version bump to v1.3.1 (bug #2041347)

* Fri Sep 17 2021 Christoph Junghans <junghans@votca.org> - 1.3.0-9
- fix build on rawhide (bug #1987402) by updating bundled doctest.h

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 17 2020 Christoph Junghans <junghans@votca.org> - 1.3.0-6
- Make package not noarch (bug #1888969)

* Mon Aug 03 2020 Christoph Junghans <junghans@votca.org> - 1.3.0-5
- Fix out-of-source build on F33 (bug #1863317)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 26 2019 Christoph Junghans <junghans@votca.org> - 1.3.0-1
- Version bump (bug #1765568)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 15 2017 Christoph Junghans <junghans@votca.org> - 1.2.2-1
- Update to v1.2.2 (bug #1422474) 

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Sep 03 2016 Christoph Junghans <junghans@votca.org> - 1.2.1-2
- Minor changes from review (bug #1372403)

* Thu Sep 01 2016 Christoph Junghans <junghans@votca.org> - 1.2.1-1
- First release.
