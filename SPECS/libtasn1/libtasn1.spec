Summary:        ASN.1 library
Name:           libtasn1
Version:        4.19.0
Release:        1%{?dist}
License:        GPLv3+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.gnu.org/software/libtasn1/
Source0:        https://ftp.gnu.org/gnu/libtasn1/%{name}-%{version}.tar.gz
Provides:       libtasn1-tools = %{version}-%{release}

%description
Libtasn1 library provides Abstract Syntax Notation One (ASN.1, as specified by the X.680 ITU-T recommendation) parsing and structures management,
and Distinguished Encoding Rules (DER, as per X.690) encoding and decoding functions.

%package devel
Summary:        Development libraries and header files for libtasn1
Requires:       libtasn1

%description devel
The package contains libraries and header files for
developing applications that use libtasn1.

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_infodir}/*
find %{buildroot} -type f -name "*.la" -delete -print

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING doc/COPYING*
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.a
%{_mandir}/man3/*

%changelog
* Tue Oct 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.19.0-1
- Updating to version 4.19.0 to fix CVE-2021-46848.

* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.18.0-2
- Remove manual pkgconfig(*) provides in toolchain specs

* Tue Jan 25 2022 Henry Li <lihl@microsoft.com> - 4.18.0-1
- Upgrade to version 4.18.0
- Fix license files

* Tue Jul 20 2021 Muhammad Falak Wani <mwani@microsoft.com> - 4.14-3
- Add an explicit provides for `libtasn1-tools`.
- Add version-release to pkgconfig(libtans1)

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.14-2
- Added %%license line automatically

* Wed Apr 22 2020 Nicolas Ontiveros <niontive@microsoft.com> 4.14-1
- Upgrade to version 4.14.
- Fixed CVE-2018-1000654.
- Remove sha1 macro.
- Update URL.
- Update Source0.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.13-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 4.13-1
- Update to version 4.13 fix CVE-2018-6003.

* Tue Oct 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.12-1
- update to 4.12 and apply patch for CVE-2017-10790

* Tue Apr 04 2017 Kumar Kaushik <kaushikk@vmware.com> 4.10-1
- Upgrading version to 4.10

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 4.7-4
- Moved man3 to devel subpackage.

* Wed Nov 30 2016 Dheeraj Shetty <dheerajs@vmware.com> 4.7-3
- Added patch for CVE-2016-4008

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 4.7-2
- GA - Bump release of all rpms

* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 4.7-1
- Updated to version 4.7

* Mon Oct 12 2015 Xiaolin Li <xiaolinl@vmware.com> 4.5-3
- Moving static lib files to devel package.

* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> 4.5-2
- Removing la files from packages.

* Fri Jun 19 2015 Divya Thaluru <dthaluru@vmware.com> 4.5-1
- Initial build. First version
