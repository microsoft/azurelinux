Summary:        MessagePack implementation for C and C++
Name:           msgpack
Version:        3.3.0
Release:        1%{?dist}
License:        Boost
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://msgpack.org
#Source0:       https://github.com/%{name}/%{name}-c/archive/cpp-%{version}.tar.gz
Source0:        %{name}-c-cpp-%{version}.tar.gz
%define _build_id_links none
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  gcc

%description
MessagePack is an efficient binary serialization format,
which lets you exchange data among multiple languages like JSON,
except that it's faster and smaller.

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
* Thu Mar 03 2022 Minghe Ren <mingheren@microsoft.com> - 3.3.0-1
- Upgrade to version 3.3.0

* Mon Oct 12 2020 Olivia Crain <oliviacrain@microsoft.com> - 3.2.1-2
- License verified and %%license added
- Update Source0

* Mon Mar 30 2020 Jonathan Chiu <jochi@microsoft.com> - 3.2.1-1
- Original version for CBL-Mariner
