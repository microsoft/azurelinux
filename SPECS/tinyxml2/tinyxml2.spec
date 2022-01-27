Summary:        Simple, small, efficient, C++ XML parser that can be easily integrated into other programs.
Name:           tinyxml2
Version:        9.0.0
Release:        1%{?dist}
License:        zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/leethomason/tinyxml2/
Source0:        https://github.com/leethomason/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  build-essential
BuildRequires:  cmake

%description
TinyXML2 is a simple, small, efficient, C++ XML parser that can be easily integrated into other programs.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%setup -q

%build
mkdir build
cd build
cmake \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DBUILD_SHARED_LIBS=ON \
    ..
make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

%files
%doc readme.md
%license LICENSE.txt
%{_lib64dir}/*.so.*

%files devel
%{_includedir}/*
%{_lib64dir}/cmake/tinyxml2
%{_lib64dir}/*.so
%{_lib64dir}/pkgconfig/tinyxml2.pc

%changelog
* Wed Jan 05 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 9.0.0-1
- Update to version 9.0.0.

* Wed Oct 14 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 7.1.0-1
- Updated to version 7.1.0.
- Enabled building *-debuginfo package.
- Added 'Vendor' and 'Distribution' tags.
- Added teh %%license macro.
- Updated 'URL' and 'Source0' tags.
- License verified.

* Thu Apr 09 2020 Jonathan Chiu <jochi@microsoft.com> 7.0.1-1
- Original version for CBL-Mariner.
