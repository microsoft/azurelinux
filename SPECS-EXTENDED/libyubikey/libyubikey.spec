Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libyubikey
Version:        1.13
Release:        14%{?dist}
Summary:        C library for decrypting and parsing Yubikey One-time passwords

License:        BSD
URL:            https://opensource.yubico.com/yubico-c
Source0:        https://opensource.yubico.com/yubico-c/releases/%{name}-%{version}.tar.gz
BuildRequires:  gcc

%description
This package holds a low-level C software development kit for the Yubico
authentication device, the Yubikey.

%package devel
Summary:        Development files for libyubikey
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header file needed to develop applications that use
libyubikey.

%prep
%setup -q

%build
%configure --disable-static --disable-silent-rules
# --disable-rpath doesn't work for the configure script
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

%check
export LD_LIBRARY_PATH=${RPM_BUILD_DIR}/%{name}-%{version}/.libs
make check

%install
%make_install INSTALL="install -p"

%ldconfig_scriptlets

%files
%doc AUTHORS NEWS ChangeLog README
%license COPYING
%{_bindir}/modhex
%{_bindir}/ykparse
%{_bindir}/ykgenerate
%{_libdir}/libyubikey.so.0
%{_libdir}/libyubikey.so.0.1.7
%{_mandir}/man1/ykgenerate.1*
%{_mandir}/man1/ykparse.1*
%{_mandir}/man1/modhex.1*

%files devel
%{_includedir}/yubikey.h
%{_libdir}/libyubikey.so
%exclude %{_libdir}/libyubikey.la

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.13-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 13 2019 Maxim Burgerhout <maxim@wzzrd.com> - 1.13-12
- Merge pull request from zlopez around manpages for flatpak builds

* Thu Aug 1 2019 Orion Poplawski <orion@nwra.com> - 1.13-11
- Modernize spec

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Nick Bebout <nb@fedoraproject.org> - 1.13-8
- Add BuildRequires gcc

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Nick Bebout <nb@fedoraproject.org> - 1.13-1
- Update to 1.13

* Fri Jun 19 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.12-4
- Reflect SONAME bump (Fix FTFBS).
- Add %%license.
- Append --disable-silent-rules to %%configure.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.12-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Nov 26 2014 Nick Bebout <nb@fedoraproject.org - 1.12-1
- Update to 1.12

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 28 2013 - Maxim Burgerhout <wzzrd@fedoraproject.org> - 1.11-1
- New upstream release 1.11; adds man pages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 - Maxim Burgerhout <wzzrd@fedoraproject.org> - 1.10-1
- New upstream release 1.10; enables build warnings

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 1 2012 - Maxim Burgerhout <wzzrd@fedoraproject.org> - 1.9-1
- New upstream release 1.9 with memory leak and rpath fixes, gnulib update

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 8 2012 - Maxim Burgerhout <maxim@wzzrd.com> - 1.7-2
- Rebuild for gcc 4.7

* Sun Feb 6 2011 - Maxim Burgerhout <maxim@wzzrd.com> - 1.7-1
- New upstream version 1.7; new features in 1.6 and 1.7 listed below
- yubikey.h: Possible to use from C++ using extern namespace scoping.
- New API to generate OTPs.
- ykgenerate: New tool to generate OTPs.
- ykdebug/ykparse: The old tool "ykdebug" has been renamed to "ykparse"

* Sun Jan 24 2010 - Maxim Burgerhout <maxim@wzzrd.com> - 1.5-4
- Reverted inserting compilerflags
- Put README, modhex and ykdebug back into main package
- Adapted defattr to (-,root,root,-)
- Set INSTALL variable in make install line

* Sun Jan 24 2010 - Maxim Burgerhout <maxim@wzzrd.com> - 1.5-3
- Took out the dep on libusb1-devel
- Moved README doc to -devel: it's mostly about ykdebug and modhex

* Sun Jan 24 2010 - Maxim Burgerhout <maxim@wzzrd.com> - 1.5-2
- Used macros in Source0
- URL no longer point to redirect
- Removed INSTALL from documentation
- Moved modhex and ykdebug to -devel
- Inserted compilerflags 
- Inserted INSTALLFLAGS to keep timestamps
- Some more macros for make and sed

* Wed Jan 20 2010 - Maxim Burgerhout <maxim@wzzrd.com> - 1.5-1
- First packaged release
