Summary:        C library that provide processing for data in the UTF-8 encoding
Name:           utf8proc
Version:        2.2.0
Release:        3%{?dist}
License:        MIT
Group:          System Environment/Libraries
Url:            https://github.com/JuliaStrings/utf8proc
# Source0:  https://github.com/JuliaStrings/utf8proc/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1 %{name}-%{version}=476efd08dbff38c63f01bb9176905edb09384e63
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cmake

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
make check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license LICENSE.md
%doc lump.md LICENSE.md NEWS.md README.md
%{_libdir}/libutf8proc.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/utf8proc.h
%{_libdir}/libutf8proc.so

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.2.0-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.2.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*       Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> 2.2.0-1
-       Initial Version.
