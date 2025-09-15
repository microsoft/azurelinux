%global lib_version 24.0.0
%global lib_soversion 24
Summary:	    Parsing gigabytes of JSON per second
Name:		    simdjson
Version:	    3.11.6
Release:	    2%{?dist}
License:	    Apache-2.0 AND MIT
URL:		    https://simdjson.org
Source0:	    https://github.com/simdjson/simdjson/archive/v%{version}/%{name}-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildRequires:	cmake >= 3.1
BuildRequires:	gcc-c++

%description
JSON is everywhere on the Internet. Servers spend a *lot* of time parsing it.
We need a fresh approach. The simdjson library uses commonly available 
SIMD instructions and microparallel algorithms to parse JSON 4x faster than
RapidJSON and 25x faster than JSON for Modern C++.

%package devel
Summary:        Development files for %{name}
Requires:	    %{name} = %{version}-%{release}
Provides:       cmake(simdjson)

%description devel
The package contains libraries and header files for developing applications
that use %{name}.

%package doc
Summary:        Documents for %{name}

%description doc 
%{summary}

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%cmake -DSIMDJSON_TESTS=ON
%cmake_build

%install
%cmake_install

%check
%ctest

%files
%license LICENSE
%doc CONTRIBUTING.md README.md
%{_libdir}/lib%{name}*.so.%{lib_soversion}
%{_libdir}/lib%{name}*.so.%{lib_version}

%files devel
%license LICENSE
%{_includedir}/%{name}.h
%{_libdir}/cmake/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files doc
%license LICENSE
%doc doc

%changelog
* Fri April 11 2025 Riken Maharjan <rmaharjan@microsoft.com> - 3.11.6-2
- Initial Azure Linux import from Fedora 43 (license: MIT)
- License Verified

* Thu Jan 16 2025 Ali Erdinc Koroglu <aekoroglu@linux.intel.com> - 3.11.6-1
- Update to 3.11.6 (rhbz#2330725)

* Wed Nov 06 2024 Ali Erdinc Koroglu <aekoroglu@linux.intel.com> - 3.10.1-1
- Update to 3.10.1 (rhbz#2173069)

* Fri Aug 02 2024 Ali Erdinc Koroglu <aekoroglu@linux.intel.com> - 3.10.0-1
- Update to 3.10.0

* Mon Feb 26 2024 Ali Erdinc Koroglu <aekoroglu@linux.intel.com> - 3.7.0-1
- Update to 3.7.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 11 2023 Ali Erdinc Koroglu <aekoroglu@linux.intel.com> - 3.6.3-1
- Update to 3.6.3

* Wed Nov 01 2023 Ali Erdinc Koroglu <aekoroglu@linux.intel.com> - 3.6.0-1
- Update to 3.6.0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 25 2023 aekoroglu <aekoroglu@linux.intel.com> - 3.1.0-1
- update to 3.1.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 aekoroglu <aekoroglu@linux.intel.com> - 3.0.1-1
- update to 3.0.1

* Tue Aug 09 2022 aekoroglu <ali.erdinc.koroglu@intel.com> - 2.2.2-1
- initial package
