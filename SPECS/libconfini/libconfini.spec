Name:           libconfini
Summary:        libconfini
Version:        1.16.0
Release:        1%{?dist}
License:        GPLv3
URL:            https://madmurphy.github.io/libconfini/html/index.html
#Source0:       https://github.com/madmurphy/libconfini/archive/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
libconfini is the ultimate and most consistent INI file parser library written in C.
Originally designed for parsing configuration files written by other programs, it 
focuses on standardization and parsing exactness and is at ease with almost every 
type of file containing key/value pairs.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}

%description devel
Development files for %{name}

%prep
%setup -q

%build
./bootstrap -z
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%license COPYING
%doc %{_docdir}/%{name}
%{_mandir}/*
%{_includedir}/*.h
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
*   Fri Dec 11 2020 Jonathan Chiu <jochi@microsoft.com> 1.16.0-1
-   Original version for CBL-Mariner.
