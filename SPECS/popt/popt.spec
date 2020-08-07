Summary:	Programs to parse command-line options
Name:		popt
Version:	1.16
Release:        7%{?dist}
License:	MIT
URL:		http://rpm5.org/files/popt
Group:		Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	ftp://anduin.linuxfromscratch.org/BLFS/svn/p/%{name}-%{version}.tar.gz
%define sha1 popt=cfe94a15a2404db85858a81ff8de27c8ff3e235e
%description
The popt package contains the popt libraries which are used by
some programs to parse command-line options.

%package devel
Summary:	Libraries and header files for popt
Requires:	%{name} = %{version}

%description devel
Static libraries and header files for the support library for popt

%package lang
Summary: Additional language files for popt
Group:		Applications/System
Requires: %{name} = %{version}-%{release}
%description lang
These are the additional language files of popt.

%prep
%setup -q
%build
%configure \
	--disable-silent-rules
make %{?_smp_mflags}
%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete
%find_lang %{name}

%check
make %{?_smp_mflags} check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libpopt.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/popt.pc
%{_libdir}/libpopt.a
%{_libdir}/libpopt.so
%{_mandir}/man3/*

%files lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Sat May 09 00:21:02 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.16-7
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.16-6
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 1.16-5
-   Use standard configure macros
*   Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> 1.16-4
-   Added -lang subpackage
*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 1.16-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.16-2
-   GA - Bump release of all rpms
*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 1.16-1
-   Initial build. First version
