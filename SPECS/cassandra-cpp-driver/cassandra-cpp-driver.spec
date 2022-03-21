Summary:        DataStax C/C++ Driver for Apache Cassandra and DataStax Products
Name:           cassandra-cpp-driver
Version:        2.16.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/datastax/cpp-driver
Source0:        https://github.com/datastax/cpp-driver/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  libuv-devel
BuildRequires:  openssl-devel
Requires:       libuv

%description
A modern, feature-rich, and highly tunable C/C++ client library for Apache
Cassandra and DataStax Products using Cassandra's native protocol and Cassandra
Query Language along with extensions for DataStax Products.

%package devel
Summary:        Development libraries for ${name}
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       libuv-devel

%description devel
Development libraries for %{name}

%prep
%setup -q -n cpp-driver-%{version}

%build
mkdir -p build
cd build
%cmake ..\
    -DCMAKE_BUILD_TYPE=RELEASE
%make_build

%install
cd build
%make_install

%ldconfig_scriptlets

%files
%license LICENSE.txt
%{_libdir}/*.so.2
%{_libdir}/*.so.2.*

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Sep 01 2021 Andy Caldwell <andycaldwell@microsoft.com> - 2.16.0-1
- Original version for CBL-Mariner
- License verified
