# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           hidapi
Version:        0.15.0
Release: 3%{?dist}
Summary:        Library for communicating with USB and Bluetooth HID devices

License:        GPL-3.0-only OR BSD-3-Clause
URL:            https://github.com/libusb/hidapi

Source0:        %{url}/archive/%{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: libudev-devel
BuildRequires: libusb1-devel

BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc
BuildRequires: mingw32-binutils

BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc
BuildRequires: mingw64-binutils

%global _description %{expand:
HIDAPI is a multi-platform library which allows an application to interface
with USB and Bluetooth HID-class devices on Windows, Linux, FreeBSD and Mac OS
X.  On Linux, either the hidraw or the libusb back-end can be used. There are
trade-offs and the functionality supported is slightly different.}

%description %_description

%package devel
Summary: Development files for hidapi
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n hidapi-devel
This package contains development files for hidapi which provides access to
USB and Bluetooth HID-class devices.

%package -n mingw32-hidapi
Summary:        %{summary}
Obsoletes:      mingw32-hidapi-static < 0.11.2-6

%description -n mingw32-hidapi %_description

%package -n mingw64-hidapi
Summary:        %{summary}
Obsoletes:      mingw64-hidapi-static < 0.11.2-6

%description -n mingw64-hidapi %_description

%{?mingw_debug_package}


%prep
%autosetup -n %{name}-%{name}-%{version}


%build
%cmake
%cmake_build

%mingw_cmake
%mingw_make_build


%install
%cmake_install

%mingw_make_install
%mingw_debug_install_post


%files
%doc AUTHORS.txt README.md LICENSE*.txt
%{_libdir}/libhidapi-*.so.*

%files devel
%{_includedir}/hidapi
%{_libdir}/cmake/hidapi
%{_libdir}/libhidapi-hidraw.so
%{_libdir}/libhidapi-libusb.so
%{_libdir}/pkgconfig/hidapi-hidraw.pc
%{_libdir}/pkgconfig/hidapi-libusb.pc

%files -n mingw32-hidapi
%doc AUTHORS.txt README.md LICENSE*.txt
%{mingw32_libdir}/cmake/hidapi
%{mingw32_bindir}/libhidapi.dll
%{mingw32_libdir}/libhidapi.dll.a
%{mingw32_libdir}/pkgconfig/hidapi.pc
%{mingw32_includedir}/hidapi

%files -n mingw64-hidapi
%doc AUTHORS.txt README.md LICENSE*.txt
%{mingw64_libdir}/cmake/hidapi
%{mingw64_bindir}/libhidapi.dll
%{mingw64_libdir}/libhidapi.dll.a
%{mingw64_libdir}/pkgconfig/hidapi.pc
%{mingw64_includedir}/hidapi

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May 21 2025 Scott Talbert <swt@techie.net> - 0.15.0-1
- Update to new upstream release 0.15.0 (#2367105)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 31 2024 Scott Talbert <swt@techie.net> - 0.14.0-6
- Update License tag to use SPDX identifiers

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 23 2023 Scott Talbert <swt@techie.net> - 0.14.0-1
- Update to new upstream release 0.14.0 (#2209190)

* Thu Feb 02 2023 Scott Talbert <swt@techie.net> - 0.13.1-1
- Update to new upstream release 0.13.1 (#2159139)

* Wed Feb 01 2023 Scott Talbert <swt@techie.net> - 0.12.0-4
- Add mingw subpackages

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Scott Talbert <swt@techie.net> - 0.12.0-1
- Update to new upstream release 0.12.0 (#2081598)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Scott Talbert <swt@techie.net> - 0.11.2-1
- Update to new upstream release 0.11.2 (#2036738)

* Mon Oct 04 2021 Scott Talbert <swt@techie.net> - 0.11.0-1
- Update to new upstream release 0.11.0 (#2008570)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 19:56:21 EST 2020 Scott Talbert <swt@techie.net> - 0.10.1-2
- Fix FTBFS with autoconf 2.70

* Tue Nov 24 21:26:02 EST 2020 Scott Talbert <swt@techie.net> - 0.10.1-1
- Update to new upstream release 0.10.1 (#1901388)
- Remove BR on gcc-c++ (no longer needed)

* Mon Oct 26 2020 Scott Talbert <swt@techie.net> - 0.10.0-1
- Update to new upstream release 0.10.0 (#1891375)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Scott Talbert <swt@techie.net> - 0.9.0-1
- Switch to new upstream at libusb organization

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-0.11.d17db57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jul 15 2018 Scott Talbert <swt@techie.net> - 0.8.0-0.10.d17db57
- Add missing BR for gcc-c++, fixes mass rebuild FTBFS

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-0.9.d17db57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Scott Talbert <swt@techie.net> - 0.8.0-0.8.d17db57
- Add missing BR for gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-0.7.d17db57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.0-0.6.d17db57
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-0.5.d17db57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-0.4.d17db57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-0.3.d17db57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-0.2.d17db57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 01 2015 Scott Talbert <swt@techie.net> - 0.8.0-0.1.d17db57
- Update to latest upstream commit d17db57

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-5.a88c724
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-4.a88c724
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3.a88c724
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct 29 2013 Scott Talbert <swt@techie.net> - 0.7.0-2.a88c724
- Incorporate review comments

* Wed Oct 23 2013 Scott Talbert <swt@techie.net> - 0.7.0-1.a88c724
- Initial packaging of hidapi library
