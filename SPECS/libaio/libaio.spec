Summary:        Linux-native asynchronous I/O access library
Name:           libaio
Version:        0.3.113
Release:        1%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pagure.io/libaio
Source0:        https://releases.pagure.org/%{name}/%{name}-%{version}.tar.gz
Patch0:         libaio-install-to-destdir-slash-usr.patch

%if %{with_check}
BuildRequires:  e2fsprogs-devel
%endif

%description
The Linux-native asynchronous I/O facility ("async I/O", or "aio") has a
richer API and capability set than the simple POSIX async I/O facility.
This library, libaio, provides the Linux-native API for async I/O.
The POSIX async I/O facility requires this library in order to provide
kernel-accelerated async I/O capabilities, as do applications which
require the Linux-native async I/O API.

%package    devel
Summary:    Development files for Linux-native asynchronous I/O access
Group:      Development/System
Requires:   libaio

%description devel
This package provides header files to include and libraries to link with
for the Linux-native asynchronous I/O facility ("async I/O", or "aio").

%prep
%autosetup -p1 -a 0


%build
# A library with a soname of 1.0.0 was inadvertantly released.  This
# build process builds a version of the library with the broken soname in
# the libaio-0.3.103 directory, and then builds the library again
# with the correct soname.
cd %{name}-%{version}
make soname='libaio.so.1.0.0' libname='libaio.so.1.0.0'
cd ..
make

%install
cd %{name}-%{version}
install -D -m 755 src/libaio.so.1.0.0 %{buildroot}/%{_libdir}/libaio.so.1.0.0
cd ..
make destdir=%{buildroot} prefix=%{_prefix} libdir=/lib usrlibdir=%{_libdir} includedir=%{_includedir} install

%check
# The check generates a lot of load on CPU & is flaky when run parallely. Avoid using `-j $(nproc)
make -k check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%attr(0755,root,root) %{_libdir}/libaio.so.*
%license COPYING
%doc COPYING TODO

%files devel
%attr(0644,root,root) %{_includedir}/*
%attr(0755,root,root) %{_libdir}/libaio.so
%attr(0755,root,root) %{_libdir}/libaio.a

%changelog
* Tue Dec 19 2023 Brian Fjeldstad <bfjelds@microsoft.com> 0.3-113-1
- Upgrade to 0.3.113
- Remove gcc-11 patch that was added to libaio 0.3.113

* Mon Feb 21 2022 Muhammad Falak <mwani@microsoft.com> 0.3-112-4
- Switch to `%autosetup` instead of `%setup`
- Introduce patch to fix gcc-11 ptest bug & parity with upstream

* Thu Dec 17 2020 Andrew Phelps <anphel@microsoft.com> 0.3-112-3
- Add e2fsprogs-devel to fix check test.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.3.112-2
- Added %%license line automatically

* Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 0.3.112-1
- Update to 0.3.112. Fix Source0 URL. Fix URL. Update Patch0. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.3.110-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.3.110-2
- GA - Bump release of all rpms

* Tue Mar 3 2015 Divya Thaluru <dthaluru@vmware.com> 0.3.110-1
- Initial version
