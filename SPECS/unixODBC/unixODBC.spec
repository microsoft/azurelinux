Summary:    ODBC driver manager
Name:       unixODBC
Version:    2.3.7
Release:        3%{?dist}
License:    GPLv2+ and LGPLv2+
URL:        http://www.unixodbc.org/
Group:      System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:    ftp://ftp.unixodbc.org/pub/unixODBC/%{name}-%{version}.tar.gz
%define sha1 unixODBC=a066c4f3fcb19befbaf5a5801b830ec41b7318df

BuildRequires: automake autoconf libtool

%description
The unixODBC package is an Open Source ODBC (Open DataBase Connectivity) sub-system and an ODBC SDK for Linux, Mac OSX, and UNIX.
ODBC is an open specification for providing application developers with a predictable API with which to access data sources.

%package devel
Summary: Development files for unixODBC library
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
To develop programs that will access data through
ODBC, you need to install this package.

%prep

%setup -q

%build
./configure --prefix=/usr               \
            --sysconfdir=/etc/%{name}   \
            --enable-threads=yes        \
            --enable-drivers=yes        \
            --enable-driverc=yes
make

%install
make DESTDIR=%{buildroot} install
find doc -name "Makefile*" -delete
chmod 644 doc/{lst,ProgrammerManual/Tutorial}/*
install -v -m755 -d /usr/share/doc/%{name}-%{version}
cp -v -R doc/* /usr/share/doc/%{name}-%{version}
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_libdir}/libltdl.*
rm -rf %{buildroot}%{_datadir}/libtool

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc README COPYING AUTHORS ChangeLog NEWS doc
%config(noreplace) %{_sysconfdir}/%{name}/odbc*
%{_bindir}/odbcinst
%{_bindir}/isql
%{_bindir}/dltest
%{_bindir}/iusql
%{_bindir}/odbc_config
%{_bindir}/slencheck
%{_libdir}/*.so.*
%{_mandir}/man*/*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig

%changelog
* Sat May 09 00:20:58 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.3.7-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.3.7-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.3.7-1
-   Update version to 2.3.7.
*   Wed Oct 26 2016 Anish Swaminathan <anishs@vmware.com> 2.3.4-1
-   Initial build.  First version
