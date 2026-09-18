# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:      zint
Version:   2.15.0
Release:   2%{?dist}
Summary:   Barcode generator library
License:   BSD-3-Clause AND GPL-3.0-or-later
URL:       http://www.zint.org.uk
Source:    http://downloads.sourceforge.net/%{name}/%{name}-%{version}-src.tar.gz

# create shared libQZint instead of static one
Patch0:    %{name}-shared.patch

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: mesa-libGL-devel
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: qt5-qttools-devel
BuildRequires: qt5-qttools-static
BuildRequires: desktop-file-utils

%description
Zint is a C library for encoding data in several barcode variants. The
bundled command-line utility provides a simple interface to the library.
Features of the library:
- Over 50 symbologies including all ISO/IEC standards, like QR codes.
- Unicode translation for symbologies which support Latin-1 and 
  Kanji character sets.
- Full GS1 support including data verification and automated insertion of 
  FNC1 characters.
- Support for encoding binary data including NULL (ASCII 0) characters.
- Health Industry Barcode (HIBC) encoding capabilities.
- Output in PNG, EPS and SVG formats with user adjustable sizes and colors.
- Verification stage for SBN, ISBN and ISBN-13 data.


%package devel
Summary:       Library and header files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      cmake

%description devel 
C library and header files needed to develop applications that use 
the Zint library. The API documentation can be found on the project website:
http://www.zint.org.uk/zintSite/Manual.aspx


%package qt
Summary:       Zint Barcode Studio

%description qt
Zint Barcode Studio is a Qt-based GUI which allows desktop users to generate 
barcodes which can then be embedded in documents or HTML pages.


%package qt-devel
Summary:       Library and header files for %{name}-qt
Requires:      %{name}-devel%{?_isa} = %{version}-%{release}

%description qt-devel 
C library and header files needed to develop applications that use libQZint.


%prep
%autosetup -p1 -n %{name}-%{version}-src

# fix line endings
sed -i "s|\r||g" docs/manual.txt

# remove BSD-licensed file required for Windows only (just to ensure that this package is plain GPLv3+)
rm -f backend/ms_stdint.h

# remove bundled getopt sources (we use the corresponding Fedora package instead)
rm -f frontend/getopt*.*

find -type f -exec chmod 644 {} \;

%build
%cmake
%cmake_build


%install
%cmake_install
rm -rf %{buildroot}/%{_datadir}/apps
install -D -p -m 644 docs/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -D -p -m 644 cmake/modules/FindZint.cmake %{buildroot}%{_datadir}/cmake/Modules/FindZint.cmake
install -D -p -m 644 %{name}-qt.png %{buildroot}/usr/share/pixmaps/%{name}-qt.png
install -D -p -m 644 %{name}-qt.desktop %{buildroot}%{_datadir}/applications/%{name}-qt.desktop
mv %{buildroot}%{_datadir}/%{name} %{buildroot}%{_datadir}/cmake/%{name}
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-qt.desktop


%ldconfig_scriptlets
%ldconfig_scriptlets qt


%files
%doc docs/manual.txt README TODO
%license LICENSE frontend/COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_libdir}/libzint.so.*

%files devel
%{_includedir}/%{name}.h
%{_libdir}/libzint.so
%{_datadir}/cmake/%{name}/
%{_datadir}/cmake/Modules/*.cmake

%files qt
%{_bindir}/%{name}-qt
%{_libdir}/libQZint.so.*
%{_datadir}/applications/%{name}-qt.desktop
%{_datadir}/pixmaps/%{name}-qt.png

%files qt-devel
%{_includedir}/qzint.h
%{_libdir}/libQZint.so


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun May 18 2025 Martin Gieseking <martin.gieseking@uos.de> - 2.15.0-1
- Update to 2.15.0
- Dropped rpath patch which is no longer required
- Updated license (libzint is now licensed under BSD-3-Clause)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 2.13.0-4
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Martin Gieseking <martin.gieseking@uos.de> - 2.13.0-1
- Update to 2.13.0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Martin Gieseking <martin.gieseking@uos.de> - 2.12.0-1
- Update to 2.12.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 25 2022 Martin Gieseking <martin.gieseking@uos.de> - 2.11.0-1
- Update to 2.11.0.

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Aug 14 2021 Martin Gieseking <martin.gieseking@uos.de> - 2.10.0-1
- Update to 2.10.0.
- Mark license file properly.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 01 2021 Martin Gieseking <martin.gieseking@uos.de> - 2.9.1-1
- Update to 2.9.1.
- Use cmake macros.

* Wed Sep 25 2019 Martin Gieseking <martin.gieseking@uos.de> - 2.6.6-1
- Update to release 2.6.6

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 01 2017 Martin Gieseking <martin.gieseking@uos.de> - 2.6.2-1
- Update to release 2.6.2

* Mon Sep 11 2017 Martin Gieseking <martin.gieseking@uos.de> - 2.6.1-1
- Update to release 2.6.1
- Added zint manpage

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 16 2017 Martin Gieseking <martin.gieseking@uos.de> - 2.6.0-1
- Update to release 2.6.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.4.3-10
- Rebuilt for GCC 5 C++11 ABI change

* Thu Dec 18 2014 Martin Gieseking <martin.gieseking@uos.de> 2.4.3-9
- Fixed https://bugzilla.redhat.com/show_bug.cgi?id=1174324

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.4.3-2
- Rebuild for new libpng

* Tue May 17 2011 Martin Gieseking <martin.gieseking@uos.de> 2.4.3-1
- updated to release 2.4.3

* Thu May 05 2011 Martin Gieseking <martin.gieseking@uos.de> 2.4.2-1
- updated to release 2.4.2

* Fri Jan 14 2011 Martin Gieseking <martin.gieseking@uos.de> 2.4.1-2
- fixed filename in Source URL

* Fri Jan 14 2011 Martin Gieseking <martin.gieseking@uos.de> 2.4.1-1
- updated to release 2.4.1

* Tue Oct 05 2010 jkeating - 2.4.0-1.1
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.4.0-1
- updated to version 2.4.0

* Tue Sep 07 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.3.2-4
- replaced BR: qt-devel with qt4-devel

* Mon Jun 14 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.3.2-3
- merged zint command-line utility and zint-qt back together with their libraries

* Fri Jun 11 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.3.2-2
- changed Group of base and -qt package to Applications/Text
- removed redundant Requires

* Sun May 30 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.3.2-1
- updated to release 2.3.2
- added patch to reolve rpath issue
- fixed Source0
- dropped locale patch and .desktop file (added upstream)
- split the libraries into separate subpackages

* Sat May 22 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.3.1-2
- Added patch to fix export issue

* Fri May 21 2010 Martin Gieseking <martin.gieseking@uos.de> - 2.3.1-1
- initial package
