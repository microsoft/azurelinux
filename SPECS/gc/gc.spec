Summary:        A garbage collector for C and C++
Name:           gc
Version:        8.0.0
Release:        4%{?dist}
# Source1 is licensed under GPLv2+. Other licenses refer to Source0.
License:        GPLv2+ and GPLv3+ and MIT
Url:            https://www.hboehm.info/gc/
Source0:        https://www.hboehm.info/gc/gc_source/%{name}-%{version}.tar.gz
Source1:        http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-7.6.6.tar.gz
Group:          System Environment/Base
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
The Boehm-Demers-Weiser conservative garbage collector can be
used as a garbage collecting replacement for C malloc or C++ new.

%package devel
Summary:    Development libraries and header files for gc
Requires:   gc

%description devel
The package contains libraries and header files for
developing applications that use gc.

%prep
%setup -q
%setup -q -T -D -a 1
ln -sfv libatomic_ops-7.6.6 libatomic_ops

%build
./configure \
    --prefix=%{_prefix} \
    --datadir=%{_docdir} \
    --enable-cplusplus
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license README.QUICK libatomic_ops/COPYING
%{_libdir}/*.so.*
%{_docdir}/gc/*
%{_mandir}/man3/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_includedir}/gc/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 8.0.0-4
- Remove libtool archive files from final packaging

*   Wed May 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 8.0.0-3
-   Adding the "%%license" macro.
-   Removing "sha1" macros.
-   License verified.
-   Replacing tabs with spaces.
-   Updating "URL" and "Source0" tags (HTTP -> HTTPS switch).
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 8.0.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 17 2018 Sujay G <gsujay@vmware.com> 8.0.0-1
-   Bump to version 8.0.0
*   Wed Apr 05 2017 Danut Moraru <dmoraru@vmware.com> 7.6.0-1
-   Upgrade gc to 7.6.0, libatomic_ops to 7.4.4
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 7.4.2-2
-   GA - Bump release of all rpms
*   Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> 7.4.2-1
-   Initial build. First version
