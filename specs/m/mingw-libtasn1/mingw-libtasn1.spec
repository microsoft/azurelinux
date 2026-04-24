# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-libtasn1
Version:        4.21.0
Release: 2%{?dist}
Summary:        MinGW Windows libtasn1 library

# The libtasn1 library is LGPLv2+, utilities are GPLv3+;
# we are only packaging the library.
License:        LGPL-2.1-or-later
URL:            http://www.gnu.org/software/libtasn1/
Source0:        http://ftp.gnu.org/gnu/libtasn1/libtasn1-%{version}.tar.gz
Source1:        http://ftp.gnu.org/gnu/libtasn1/libtasn1-%{version}.tar.gz.sig

BuildArch:      noarch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 98
BuildRequires:  mingw32-gcc

BuildRequires:  mingw64-filesystem >= 98
BuildRequires:  mingw64-gcc

BuildRequires:  bison


%description
libtasn1 is the ASN.1 library used in GNUTLS.

This package contains the MinGW Windows cross compiled libtasn1 library.


%package -n mingw32-libtasn1
Summary:        MinGW Windows libtasn1 library
Requires:       pkgconfig

%description -n mingw32-libtasn1
A library that provides Abstract Syntax Notation One (ASN.1, as specified
by the X.680 ITU-T recommendation) parsing and structures management, and
Distinguished Encoding Rules (DER, as per X.690) encoding and decoding functions.

This package contains the MinGW Windows cross compiled libtasn1 library.


%package -n mingw64-libtasn1
Summary:        MinGW Windows libtasn1 library
Requires:       pkgconfig

%description -n mingw64-libtasn1
A library that provides Abstract Syntax Notation One (ASN.1, as specified
by the X.680 ITU-T recommendation) parsing and structures management, and
Distinguished Encoding Rules (DER, as per X.690) encoding and decoding functions.

This package contains the MinGW Windows cross compiled libtasn1 library.


%?mingw_debug_package


%prep
%setup -q -n libtasn1-%{version}


%build
%mingw_configure --disable-static --disable-gcc-warnings
%mingw_make_build


%install
%mingw_make_install

# Remove documentation
rm -rf %{buildroot}%{mingw32_datadir}/info/
rm -rf %{buildroot}%{mingw64_datadir}/info/
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}
# Remove .la and .def files
rm -f %{buildroot}%{mingw32_libdir}/{*.la,*.def}
rm -f %{buildroot}%{mingw64_libdir}/{*.la,*.def}
# Remove utilities
rm -f %{buildroot}%{mingw32_bindir}/*.exe
rm -f %{buildroot}%{mingw64_bindir}/*.exe


%files -n mingw32-libtasn1
%license COPYING COPYING.LESSERv2
%{mingw32_bindir}/libtasn1-6.dll
%{mingw32_includedir}/libtasn1.h
%{mingw32_libdir}/libtasn1.dll.a
%{mingw32_libdir}/pkgconfig/libtasn1.pc

%files -n mingw64-libtasn1
%license COPYING COPYING.LESSERv2
%{mingw64_bindir}/libtasn1-6.dll
%{mingw64_includedir}/libtasn1.h
%{mingw64_libdir}/libtasn1.dll.a
%{mingw64_libdir}/pkgconfig/libtasn1.pc


%changelog
* Tue Jan 13 2026 Sandro Mani <manisandro@gmail.com> - 4.21.0-1
- Update to 4.21.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 12 2025 Sandro Mani <manisandro@gmail.com> - 4.20.0-1
- Update to 4.20.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 4.19.0-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 04 2022 Sandro Mani <manisandro@gmail.com> - 4.19.0-1
- Update to 4.19.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 4.18.0-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 10 2021 Sandro Mani <manisandro@gmail.com> - 4.18.0-1
- Update to 4.18.0

* Thu Nov 04 2021 Sandro Mani <manisandro@gmail.com> - 4.17.0-1
- Update to 4.17.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.16.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Feb 02 2020 Sandro Mani <manisandro@gmail.com> - 4.16.0-1
- Update to 4.16.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 21 2019 Sandro Mani <manisandro@gmail.com> - 4.15.0-1
- Update to 4.15.0

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 4.14-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Wed Aug 14 2019 Fabiano Fidêncio <fidencio@redhat.com> - 4.14-1
- Update the sources accordingly to its native counter part, rhbz#1740747

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Michael Cronenworth <mike@cchtml.com> - 4.13-1
- Update to 4.13

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 30 2017 Michael Cronenworth <mike@cchtml.com> - 4.12-1
- Update to 4.12

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 29 2016 Michael Cronenworth <mike@cchtml.com> - 4.9-1
- Update to 4.9

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 27 2015 Michael Cronenworth <mike@cchtml.com> - 4.5-1
- Update to 4.5

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 31 2015 Kalev Lember <kalevlember@gmail.com> - 4.4-1
- Update to 4.4 (CVE-2015-2806)

* Sat Sep 20 2014 Michael Cronenworth <mike@cchtml.com> - 4.2-1
- Update to 4.2

* Thu Sep 11 2014 Michael Cronenworth <mike@cchtml.com> - 4.1-1
- Update to 4.1

* Tue Jul 01 2014 Michael Cronenworth <mike@cchtml.com> - 4.0-1
- Update to 4.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Michael Cronenworth <mike@cchtml.com> - 3.6-1
- Update to 3.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.3-3
- Fix FTBFS against latest mingw-w64 (already resolved in upstream gnulib)

* Thu May 30 2013 Michael Cronenworth <mike@cchtml.com> - 3.3-2
- Rebuild for mingw-filesystem changes

* Thu May 09 2013 Michael Cronenworth <mike@cchtml.com> - 3.3-1
- Update to 3.3

* Thu Feb 07 2013 Michael Cronenworth <mike@cchtml.com> - 3.2-1
- Update to 3.2

* Sat Nov 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.14-1
- Update to 2.14

* Sun Oct 07 2012 Kalev Lember <kalevlember@gmail.com> - 2.13-1
- Update to 2.13

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.12-1
- Update to 2.12 (#804920)
- Build 64 bit Windows binaries

* Tue Feb 28 2012 Kalev Lember <kalevlember@gmail.com> - 2.9-4
- Remove .la files

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.9-3
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Jul 10 2011 Kalev Lember <kalevlember@gmail.com> - 2.9-1
- Update to 2.9
- Renamed the base package to mingw-libtasn1
- Use the automatic dep extraction available in mingw32-filesystem 68

* Mon May 09 2011 Kalev Lember <kalev@smartlink.ee> - 2.7-1
- Initial RPM release
