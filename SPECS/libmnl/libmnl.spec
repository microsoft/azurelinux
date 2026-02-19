Summary:    A minimalistic user-space library oriented to Netlink developers.
Name:       libmnl
Version:    1.0.5
Release:        2%{?dist}
License:    LGPLv2+
URL:        http://netfilter.org/projects/libmnl
Group:      System Environment/libraries
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:     http://netfilter.org/projects/libmnl/files/%{name}-%{version}.tar.bz2
Obsoletes:  libmnl-static

%description
libmnl is a minimalistic user-space library oriented to Netlink developers. There are a lot of common tasks in parsing, validating, constructing of both the Netlink header and TLVs that are repetitive and easy to get wrong. This library aims to provide simple helpers that allows you to re-use code and to avoid re-inventing the wheel.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       libmnl >= 1.0.4
%description devel
Libraries and header files for libnml library.

%prep
%setup -q

%build
%configure --enable-static=no
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
make %{?_smp_mflags} -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libmnl.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libmnl.so
%{_libdir}/libmnl.la
%{_libdir}/pkgconfig/*

%changelog
* Thu Mar 27 2025 Andrew Phelps <anphel@microsoft.com> - 1.0.5-2
- Remove dependency on bash from post/postun phases

* Fri Feb 23 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.5-1
- Auto-upgrade to 1.0.5 - Azure Linux 3.0 Upgrades

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.4-6
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.0.4-5
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.0.4-4
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 17 2018 Bo Gan <ganb@vmware.com> 1.0.4-3
-   Cleanup spec file
*   Wed Jul 5 2017 Divya Thaluru <dthaluru@vmware.com> 1.0.4-2
-   Added obsoletes for libmnl-static package which is deprecated
*   Wed Aug 3 2016 Xiaolin Li <xiaolinl@vmware.com> 1.0.4-1
-   Initial build.	First version
