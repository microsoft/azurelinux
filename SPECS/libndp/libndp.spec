Summary:        Library for Neighbor Discovery Protocol
Name:           libndp
Version:        1.8
Release:        1%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            http://www.libndp.org/
Source:         http://www.libndp.org/files/%{name}-%{version}.tar.gz

%description
This package contains a library which provides a wrapper
for IPv6 Neighbor Discovery Protocol.  It also provides a tool
named ndptool for sending and receiving NDP messages.

%package devel
Summary:        Libraries and header files for libndp
Requires:       libndp

%description devel
Headers and libraries for the libndp.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_bindir}/ndptool
%{_libdir}/*.so.*
%{_mandir}/man8/ndptool.8*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Jan 11 2022 Henry Li <lihl@microsoft.com> - 1.8-1
- Upgrade to version 1.8
- Remove calling autogen, which does not exist in latest version
- Verified License
- Remove sha1 macro

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.7-3
- Remove libtool archive files from final packaging

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.7-2
-   Added %%license line automatically
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Thu Sep 13 2018 Bo Gan <ganb@vmware.com> 1.7-1
-   Update to 1.7

*   Mon Nov 28 2016 Alexey Makhalov <amakhalov@vmware.com> 1.6-1
-   Update to 1.6 to fix CVE-2016-3698

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-2
-   GA - Bump release of all rpms

*   Tue Jun 23 2015 Divya Thaluru <dthaluru@vmware.com> 1.5-1
-   Initial build.
