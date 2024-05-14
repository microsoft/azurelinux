Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global checkout 20130902svn

Summary: Driver for QPDL/SPL2 printers (Samsung and several Xerox printers)
Name: splix
Version: 2.0.1
Release: 3%{?dist}
License: GPLv2
URL: https://splix.sourceforge.net/

# This is a SVN snapshot downloaded via 'Download Snapshot' from
# https://sourceforge.net/p/splix/code/315/tree/
# and renamed to follow naming guidelines
Source0: %{_distro_sources_url}/%{name}-%{version}.%{checkout}.tar.bz2

# IEEE 1284 Device IDs
Patch0:  splix-deviceID.patch
# rules.mk misses LDFLAGS
Patch1:  splix-ldflags.patch

Requires: cups

# gcc-c++ is no longer in buildroot by default
BuildRequires: gcc-c++

# _cups_serverbin macro
BuildRequires: cups-devel

# postscriptdriver tags
BuildRequires: python3-cups, cups

# JBIG1 lossless image compression
BuildRequires: jbigkit-devel

%description
This driver is usable by all printer devices which understand the QPDL
(Quick Page Description Language) also known as SPL2 (Samsung Printer Language)
language. It covers several Samsung, Xerox and Dell printers.
Splix doesn't support old SPL(1) printers.

%prep
%setup -q -n splix

# remove old PPDs (not sure why some PPDs are outside ppd/)
rm -f *.ppd

pushd ppd
# remove old PPDs
make distclean
popd

%patch 0 -p1 -b .deviceID
%patch 1 -p1 -b .ldflags

%build
%set_build_flags
# *.drv.in -> *.drv
make drv

CXXFLAGS="%{optflags} -fno-strict-aliasing" \
make all V=1 DRV_ONLY=1 %{?_smp_mflags}

%install
make install DRV_ONLY=1 CUPSDRV=%{_datadir}/cups/drv/splix DESTDIR=%{buildroot}

%files
%license COPYING
%doc AUTHORS ChangeLog THANKS
%{_cups_serverbin}/filter/pstoqpdl
%{_cups_serverbin}/filter/rastertoqpdl
%{_datadir}/cups/drv/splix

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-3
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 2.0.1-2
- Update Source0
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.1-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.40.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.39.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.38.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.37.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-0.36.20130902svn
- 1550554 - splix: Partial Fedora build flags injection

* Mon Feb 19 2018 Zdenek Dohnal <zdohnal@redhat.com> - 2.0.1-0.35.20130902svn
- gcc-c++ is no longer in buildroot by default

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.34.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.0.1-0.33.20130902svn
- Rebuilt for switch to libxcrypt

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.32.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.31.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.30.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-0.29.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.28.20130902svn
- Add Device ID for Xerox WorkCentre 3119 Series (#1294214)

* Thu Nov 26 2015 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.27.20130902svn
- BuildRequires: python3-cups

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-0.26.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0.1-0.25.20130902svn
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-0.24.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.23.20130902svn
- Rebuilt against jbigkit-2.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-0.22.20130902svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.21.20130902svn
- Add Device ID for Samsung ML-2160

* Mon Mar 17 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.20.20130902svn
- Add Device ID for Samsung ML-1640

* Mon Sep 02 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.19.20130902svn
- Latest upstream snapshot.

* Sat Jul 27 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.18.20121128svn
- Add Device ID for Samsung CLP-310 (#988926)

* Mon Apr 08 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.17.20121128svn
- Add Device IDs for Samsung SCX-4200 Series (#949063)

* Wed Mar 06 2013 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.16.20121128svn
- Add Device IDs for Samsung ML-2250/2510, Xerox Phaser 3117/3120/3130

* Tue Mar  5 2013 Tim Waugh <twaugh@redhat.com> - 2.0.1-0.15.20121128svn
- Build requires cups for postscriptdriver tags (bug #917333).

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-0.14.20121128svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.13.20121128svn
- latest svn snapshot

* Wed Oct 17 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.12.20120419svn
- Add Device ID for Xerox Phaser 3124 (#867392).

* Tue Sep 25 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.11.20120419svn
- Add Device ID for Samsung ML-2525 (#859669).

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-0.10.20120419svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 19 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.9.20120419svn
- Latest upstream snapshot: all patches and changes merged upstream !
- Build splix with JBIG1 support and install DRV files instead of PPD files.
- Add Device ID for Samsung ML-2010 (#807308).

* Wed Jan 18 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.7.20111121svn
- Add Device ID for Samsung ML-1660.

* Wed Nov 30 2011 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.6.20111121svn
- Install splix PPDs into separate directory.
- Added patch for compiling/installing DRVs instead of PPDs.
  However we still ship only selected PPDs instead of DRVs as some printers
  require JBIG1 support.

* Tue Nov 29 2011 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.5.20111121svn
- Re-compile PPD files.

* Mon Nov 28 2011 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.4.20111121svn
- Add Device ID for Samsung ML-1610.

* Tue Nov 22 2011 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.3.20111121svn
- Include more files into documentation (#755069).

* Mon Nov 21 2011 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.2.20111121svn
- Download only trunk from upstream SVN repository.

* Fri Nov 18 2011 Jiri Popelka <jpopelka@redhat.com> - 2.0.1-0.1.20111118svn
- Initial spec file.
