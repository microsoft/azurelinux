Name:           tinyxml2
Summary:        Simple, small, efficient, C++ XML parser that can be easily integrated into other programs. 
Version:        7.1.0
Release:        1%{?dist}
License:        zlib
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/leethomason/tinyxml2/

#Source0:       https://github.com/leethomason/%{name}/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  build-essential

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
/usr/lib64/*.so.*

%files devel
%{_includedir}/*
/usr/lib64/cmake/tinyxml2
/usr/lib64/*.so
/usr/lib64/pkgconfig/tinyxml2.pc

%changelog
*   Wed Oct 14 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 7.1.0-1
-   Updated to version 7.1.0.
-   Enabled building *-debuginfo package.
-   Added 'Vendor' and 'Distribution' tags.
-   Added teh %%license macro.
-   Updated 'URL' and 'Source0' tags.
-   License verified.
*   Thu Apr 09 2020 Jonathan Chiu <jochi@microsoft.com> 7.0.1-1
-   Original version for CBL-Mariner.
