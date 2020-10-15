Summary:        MessagePack implementation for C and C++
Name:           msgpack
Version:        3.2.1
Release:        2%{?dist}
License:        Boost
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://msgpack.org
#Source0:       https://github.com/%{name}/%{name}-c/archive/cpp-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define _build_id_links none
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gcc

%description
Fluent Bit is a fast Log Processor and Forwarder for Linux, Embedded Linux, MacOS and BSD
family operating systems. It's part of the Fluentd Ecosystem and a CNCF sub-project.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%setup -q -n %{name}-c-cpp-%{version}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} ..
make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

%files
%license COPYING LICENSE_1_0.txt NOTICE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/msgpack.pc
%{_libdir}/*.so
%{_libdir}/*.a

%changelog
* Mon Oct 12 2020 Thomas Crain <thcrain@microsoft.com> - 3.2.1-2
- License verified and %%license added
- Update Source0

* Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> - 3.2.1-1
- Original version for CBL-Mariner
