Summary:        C library that provide processing for data in the UTF-8 encoding
Name:           utf8proc
Version:        2.9.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/JuliaStrings/utf8proc
# Source0:  https://github.com/JuliaStrings/utf8proc/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
%if %{with_check}
BuildRequires:  ruby
%endif

%description
utf8proc is a small, clean C library that provides Unicode normalization, case-folding, and other operations for data in the UTF-8 encoding.

%package        devel
Summary:        Development libraries and headers for utf8proc
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The utf8proc-devel package contains libraries, header files and documentation
for developing applications that use utf8proc.

%prep
%setup -q

%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DCMAKE_BUILD_TYPE=Release        \
      -DBUILD_SHARED_LIBS=ON            \
      ..
make %{?_smp_mflags}

%install
cd build
make DESTDIR=%{buildroot} install

%check
LANG=en_US.UTF-8 LANGUAGE=en_US.UTF-8 LC_ALL=en_US.UTF-8 make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license LICENSE.md
%doc lump.md NEWS.md README.md
%{_libdir}/libutf8proc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/utf8proc.h
%{_libdir}/libutf8proc.so

%changelog
* Fri Jan 12 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.9.0-1
- Auto-upgrade to 2.9.0 - none

* Tue Mar 01 2022 Bala <balakumaran.kannan@microsoft.com> - 2.6.1-2
- BR ruby for ptest
- Set Locale before running ptest

* Thu Jan 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.6.1-1
- Update to version 2.6.1.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.2.0-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 2.2.0-1
- Initial Version.
