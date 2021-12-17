Summary:    Atomic memory update operations portable implementation
Name:       libatomic_ops
Version:    7.6.6
Release:        4%{?dist}
License:    GPLv2 and MIT
URL:        https://github.com/ivmai/libatomic_ops
Group:      Development/Libraries
Source0:    http://www.ivmaisoft.com/_bin/atomic_ops/libatomic_ops-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner

%description
This package provides semi-portable access to hardware-provided atomic memory update operations on a number of architectures.

%package devel
Summary:    Development files for the libatomic_ops library
Group:      Development/Libraries
Requires:   libatomic_ops
Provides:   libatomic_ops-devel
Provides:   libatomic_ops-devel(x86-64)

%description devel
Libraries and header files for libatomic_ops library.


%prep
%setup -q
%build
./configure --prefix=%{_prefix}      \
            --bindir=%{_sbindir}     \
            --enable-shared \
            --disable-silent-rules

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
make check

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_docdir}/libatomic_ops/COPYING
%{_docdir}/libatomic_ops/LICENSING.txt
%{_libdir}/libatomic_ops.so.*
%{_libdir}/libatomic_ops_gpl.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_docdir}/libatomic_ops/README*
%{_libdir}/libatomic_ops.a
%{_libdir}/libatomic_ops_gpl.a
%{_libdir}/libatomic_ops.so
%{_libdir}/libatomic_ops_gpl.so
%{_libdir}/pkgconfig/atomic_ops.pc

%changelog
* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.6.6-4
- Removing the explicit %%clean stage.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 7.6.6-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 7.6.6-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 13 2018 Siju Maliakkal <smaliakkal@vmware.com> 7.6.6-1
-   Updated to latest version
*   Tue Jul 26 2016 Xiaolin Li <xiaolinl@vmware.com> 7.4.4-1
-   Initial build. First version
