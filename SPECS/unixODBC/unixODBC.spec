Summary:        ODBC driver manager
Name:           unixODBC
Version:        2.3.12
Release:        1%{?dist}
License:        GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            http://www.unixodbc.org/
Source0:        http://www.unixodbc.org/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
Requires:       glibc-iconv

%description
The unixODBC package is an Open Source ODBC (Open DataBase Connectivity) sub-system and an ODBC SDK for Linux, Mac OSX, and UNIX.
ODBC is an open specification for providing application developers with a predictable API with which to access data sources.

%package devel
Summary:        Development files for unixODBC library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
To develop programs that will access data through
ODBC, you need to install this package.

%prep

%setup -q

%build
./configure --prefix=%{_prefix}               \
            --sysconfdir=%{_sysconfdir}/%{name}   \
            --enable-threads=yes        \
            --enable-drivers=yes        \
            --enable-driverc=yes
make

%install
make DESTDIR=%{buildroot} install
find doc -name "Makefile*" -delete
chmod 644 doc/{lst,ProgrammerManual/Tutorial}/*
install -v -m755 -d %{_docdir}/%{name}-%{version}
cp -v -R doc/* %{_docdir}/%{name}-%{version}
rm -f %{buildroot}%{_libdir}/*.a
find %{buildroot} -type f -name "*.la" -delete -print
rm -f %{buildroot}%{_libdir}/libltdl.*
rm -rf %{buildroot}%{_datadir}/libtool

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%doc README AUTHORS ChangeLog NEWS doc
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
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.3.12-1
- Auto-upgrade to 2.3.12 - Azure Linux 3.0 - package upgrades

* Thu May 26 2022 Evan Lee <evlee@microsoft.com> - 2.3.9-2
- Require glibc-iconv as a runtime dependency for unixODBC.

* Thu Jan 13 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 2.3.9-1
- Update to version 2.3.9.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.3.7-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.3.7-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 2.3.7-1
- Update version to 2.3.7.

* Wed Oct 26 2016 Anish Swaminathan <anishs@vmware.com> 2.3.4-1
- Initial build.  First version
