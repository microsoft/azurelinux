# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global boost_version 1.69.0
%global rapidjson_version 1.1.0
%global geometry_version 1.0.0

%global testcommit a623c19a91947a9d29f9ec5625ce620ab42325dc

%global debug_package %{nil}

Name:           wagyu
Version:        0.5.0
Release: 13%{?dist}
Summary:        A general library for geometry operations of union, intersections, difference, and xor

License:        BSL-1.0 AND BSD-3-Clause
URL:            https://github.com/mapbox/wagyu
Source0:        https://github.com/mapbox/wagyu/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/mapnik/geometry-test-data/archive/%{testcommit}/geometry-test-data-%{testcommit}.tar.gz
# Remove benchmarking support to avoid libbenchmark dependency
Patch0:         wagyu-benchmark.patch
# Rip out mason stuff - we use our own packages
Patch1:         wagyu-mason.patch
# https://github.com/mapbox/wagyu/pull/109
Patch2:         wagyu-cxx14.patch

BuildRequires:  cmake make
BuildRequires:  gcc-c++
BuildRequires:  catch1-devel
BuildRequires:  boost-devel >= %{boost_version}
BuildRequires:  boost-static >= %{boost_version}
BuildRequires:  rapidjson-devel >= %{rapidjson_version}
BuildRequires:  rapidjson-static >= %{rapidjson_version}
BuildRequires:  geometry-hpp-devel >= %{geometry_version}
BuildRequires:  geometry-hpp-static >= %{geometry_version}

%description
Wagyu is a general library for the following basic geometric operations:

    Union
    Intersection
    Difference
    XOR

The output geometry from each of these operations is guaranteed to
be valid and simple as per the OGC.


%package        devel
Summary:        Development files for %{name}
Provides:       %{name}-static = %{version}-%{release}

Requires:       geometry-hpp-devel >= %{geometry_version}

%description    devel
Wagyu is a general library for the following basic geometric operations:

    Union
    Intersection
    Difference
    XOR

The output geometry from each of these operations is guaranteed to
be valid and simple as per the OGC.


%prep
%autosetup -p 1 -n wagyu-%{version}
tar --directory=tests/geometry-test-data --strip-components=1 --gunzip --extract --file=%{SOURCE1}
rm -f tests/catch.hpp


%build
%make_build release CXXFLAGS="-I$PWD/include %{optflags}" WERROR=False


%install
mkdir -p %{buildroot}%{_includedir}
cp -pr include/mapbox %{buildroot}%{_includedir}


%check
%make_build test CXXFLAGS="-I$PWD/include %{optflags}" WERROR=False


%files devel
%doc README.md
%license LICENSE
%{_includedir}/mapbox


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar  4 2020 Tom Hughes <tom@compton.nu> - 0.5.0-1
- Update to 0.5.0 upstream release

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Tom Hughes <tom@compton.nu> - 0.4.3-2
- Build using catch1

* Mon Nov 20 2017 Tom Hughes <tom@compton.nu> - 0.4.3-1
- Update to 0.4.3 upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr  9 2017 Tom Hughes <tom@compton.nu> - 0.4.2-1
- Initial build of 0.4.2
