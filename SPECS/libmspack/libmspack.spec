Summary:        A library that provides compression and decompression of file formats used by Microsoft
Name:           libmspack
Version:        0.10.1alpha
Release:        2%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.cabextract.org.uk/libmspack/
Source0:        http://www.cabextract.org.uk/libmspack/%{name}-%{version}.tar.gz

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
find %{buildroot} -type f -name "*.la" -delete -print

%check
make -k check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README TODO ChangeLog AUTHORS
%license COPYING.LIB
%{_libdir}/*.so.*

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so

%changelog
* Thu Feb 10 2022 Muhammad Falak <mwani@microsfot.com> - 0.10.1alpha-2
- Use `make -k check` to enable ptest

* Tue Jan 11 2022 Henry Li <lihl@microsoft.com> - 0.10.1alpha-1
- Upgrade to version 0.10.1alpha
- Remove binaries under /usr/bin
- Add README, TODO, ChangeLog, AUTHORS to the main package
- License Verified
- Remove the sha1 macro
- Fix URL field

* Fri Sep 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.7.1alpha-4
- Remove libtool archive files from final packaging

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
