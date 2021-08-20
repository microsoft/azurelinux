Summary:        A library that provides compression and decompression of file formats used by Microsoft
Name:           libmspack
Version:        0.7.1alpha
Release:        3%{?dist}
License:        LGPLv2+
URL:            http://www.cabextract.org.uk/libmspack/libmspack-0.5alpha.tar.gz
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://www.cabextract.org.uk/libmspack/%{name}-%{version}.tar.gz
%define sha1    libmspack=073348180586d7b0f61fd7f971162ffb5c1f6621
%description
A library that provides compression and decompression of file formats used by Microsoft

%package        devel
Summary:        Header and development files for libmspack
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q

%build
%configure
#Package does not support parallel make
make

%install
make DESTDIR=%{buildroot} install

%check
cd test
./cabd_test

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING.LIB
%{_bindir}/cabrip
%{_bindir}/chmextract
%{_bindir}/msexpand
%{_bindir}/oabextract
%{_libdir}/*.so.*

%files  devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.7.1alpha-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.7.1alpha-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 0.7.1alpha-1
-   Update to 0.7.1alpha
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5alpha-3
-   Add devel package.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5alpha-2
-   GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 0.5-1
-   Updated to version 0.5
*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 0.4-1
    Initial version
