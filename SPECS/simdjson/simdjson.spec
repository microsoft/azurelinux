%global lib_version 24.0.0
%global lib_soversion 24
Distribution:   Azure Linux
Name:		simdjson
Vendor:         Microsoft Corporation
Version:	3.11.6
Release:	%autorelease
Summary:	Parsing gigabytes of JSON per second

License:	Apache-2.0 AND MIT
URL:		https://simdjson.org
Source0:	https://github.com/simdjson/simdjson/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	cmake >= 3.1
BuildRequires:	gcc-c++

%description
JSON is everywhere on the Internet. Servers spend a *lot* of time parsing it.
We need a fresh approach. The simdjson library uses commonly available 
SIMD instructions and microparallel algorithms to parse JSON 4x faster than
RapidJSON and 25x faster than JSON for Modern C++.

%package devel
Summary: Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Provides:   cmake(simdjson)

%description devel
The package contains libraries and header files for developing applications
that use %{name}.

%package doc
Summary: Documents for %{name}

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
%autochangelog
