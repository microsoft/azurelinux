Summary:	String handling essentials library
Name:		libestr
Version:	0.1.10
Release:        4%{?dist}
License:	LGPLv2+
URL:		http://libestr.adiscon.com/
Source0:	http://libestr.adiscon.com/files/download/%{name}-%{version}.tar.gz
%define sha1 libestr=35cc717f5ae737a28140dd1472e13ce2ec317c6c
Group:		System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner
%description
This package compiles the string handling essentials library
used by the Rsyslog daemon.

%package devel
Summary:	Development libraries for string handling
Requires:	libestr

%description devel
The package contains libraries and header files for
developing applications that use libestr.

%prep
%setup -q
%build
./configure \
	--prefix=%{_prefix}
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_libdir}/*.a
%{_libdir}/*.la
%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
* Sat May 09 00:21:00 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.1.10-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.1.10-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.1.10-2
-	GA - Bump release of all rpms
*	Wed Jun 17 2015 Divya Thaluru <dthaluru@vmware.com> 0.1.10-1
-	Initial build. First version
