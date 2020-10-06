Summary:        RELP Library
Name:           librelp
Version:        1.2.17
Release:        7%{?dist}
License:        GPLv3+
URL:            https://github.com/rsyslog/librelp
#Source0:        https://github.com/rsyslog/librelp/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
%define sha1 librelp=701d69e7723fe614b96750af8cba5ee9a54085fe
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  gnutls-devel
BuildRequires:  autogen
Requires:       gnutls

%if %{with_check}
BuildRequires:  valgrind
%endif

%description
Librelp is an easy to use library for the RELP protocol. RELP (stands
for Reliable Event Logging Protocol) is a general-purpose, extensible
logging protocol.

%package devel
Summary:	Development libraries and header files for librelp
Requires:	librelp

%description devel
The package contains libraries and header files for
developing applications that use librelp.

%prep
%setup -q
autoreconf -fiv

%build
%configure
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%check
make check

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig
%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_libdir}/*.la
%{_libdir}/*.a
%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%changelog
*   Mon Sep 05 2020 Emre Girgin <mrgirgin@microsoft.com> 1.2.17-7
-   Remove the Valgrind workaround in the check section.
*   Sat May 09 00:21:40 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.2.17-6
-   Added %%license line automatically
*   Wed Mar 11 2020 Christopher Co <chrco@microsoft.com> 1.2.17-5
-   Updated Source location
*   Mon Mar 09 2020 Jon Slobodzian <joslobo@microsoft.com> 1.2.17-4
-   Fixed URL. Verified license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.2.17-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Nov 20 2018 Ashwin H <ashwinh@vmware.com> 1.2.17-2
-   Fix librelp %check
*   Tue Sep 11 2018 Keerthana K <keerthanak@vmware.com> 1.2.17-1
-   Updated to version 1.2.17
*	Tue Apr 11 2017 Harish Udaiy Kumar <hudaiyakumar@vmware.com> 1.2.13-1
-	Updated to version 1.2.13
*	Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.2.9-2
-	GA - Bump release of all rpms
* 	Thu Feb 25 2016 Anish Swaminathan <anishs@vmware.com>  1.2.9-1
- 	Upgrade to 1.2.9
*	Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 1.2.7-1
-	Initial build. First version
