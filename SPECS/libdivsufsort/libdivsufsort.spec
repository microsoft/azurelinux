Summary:        A software library that implements a lightweight suffix array construction algorithm.
Name:           libdivsufsort
Version:        2.0.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/y-256/libdivsufsort
# Source0:      https://github.com/y-256/libdivsufsort/archive/refs/tags/%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
A software library that implements a lightweight suffix array construction algorithm.

%prep
%autosetup

%build
mkdir build
cd build
%cmake -DCMAKE_BUILD_TYPE="Release" -DCMAKE_INSTALL_PREFIX="%{_prefix}" ..
%make_build

%install
cd build
%make_install

%files
%{_includedir}/divsufsort.h
%{_libdir}/libdivsufsort.so
%{_libdir}/libdivsufsort.so.3*
%{_libdir}/pkgconfig/libdivsufsort.pc

%changelog
* Tue Mar 30 2021 Nicolas Ontiveros <niontive@microsoft.com> - 2.0.1-1
- Original version for CBL-Mariner. License verified.
