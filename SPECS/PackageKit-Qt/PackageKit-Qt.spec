# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gitcommit 42902ed51e02e78f13a002c5e81c240601b7445a
%global gitdate 20250914.113000
%global shortcommit %(c=%{gitcommit}; echo ${c:0:7})

Summary:   Qt support library for PackageKit
Name:      PackageKit-Qt
Version:   1.1.4
Release:   2%{?dist}

License:   LGPL-2.1-only
URL:       http://www.packagekit.org/

Source0:   https://github.com/hughsie/PackageKit-Qt/archive/v%{version}.tar.gz
# Source0:   https://github.com/PackageKit/%%{name}/archive/%%{gitcommit}.tar.gz

# Upstream patches

BuildRequires: cmake
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Sql)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Sql)
BuildRequires: gcc-c++
# required for /usr/share/dbus-1/interfaces/*.xml
BuildRequires: PackageKit >= 0.9.1

Recommends: PackageKit

## FIXME/TODO:
# Qt4-based PackageKit-Qt no longer supported or built since 0.10.0 release, add Obsoletes somewhere?
# consider renaming PackageKit-Qt5 -> PackageKit-Qt ? -- rex

%description
PackageKit-Qt is a Qt support library for PackageKit

%package -n PackageKit-Qt6
Summary: Qt6 support library for PackageKit
Recommends: PackageKit
%description -n PackageKit-Qt6
%{summary}.

%package -n PackageKit-Qt6-devel
Summary: Development files for PackageKit-Qt6
Requires: PackageKit-Qt6%{?_isa} = %{version}-%{release}
%description -n PackageKit-Qt6-devel
%{summary}.


%prep
%autosetup -p1 -n %{name}-%{version}


%build
%cmake -DBUILD_WITH_QT6=ON
%cmake_build


%install
%cmake_install

%files -n PackageKit-Qt6
%doc AUTHORS NEWS
%license COPYING
%{_libdir}/libpackagekitqt6.so.%{version}
%{_libdir}/libpackagekitqt6.so.2

%files -n PackageKit-Qt6-devel
%{_libdir}/libpackagekitqt6.so
%{_libdir}/pkgconfig/packagekitqt6.pc
%{_includedir}/PackageKitQt/
%{_libdir}/cmake/packagekitqt6/


%changelog
* Thu Oct 30 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.1.4-2
- Drop unneeded Conflicts on PackageKit-Qt5

* Sat Oct 04 2025 Steve Cossette <farchord@gmail.com> - 1.1.4-1
- Update to 1.1.4

* Thu Sep 25 2025 Steve Cossette <farchord@gmail.com> - 1.1.4~20250914.113000.42902ed-1
- Git build for Plasma 6.4.90

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Feb 09 2025 Steve Cossette <farchord@gmail.com> - 1.1.2-1
- 1.1.2

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.1.1-7
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.1.1-3
- Add PackageKit-Qt6 build

* Sat Jul 22 2023 Alessandro Astone <ales.astone@gmail.com> - 1.1.1-2
- Backport fixes for Discover distro upgrade

* Sat Jul 22 2023 Alessandro Astone <ales.astone@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 11 2020 Rex Dieter <rdieter@fedoraproject.org> - 1.0.2-1
- 1.0.2

* Fri Oct 02 2020 Rex Dieter <rdieter@fedoraproject.org> - 1.0.1-8
- use new cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.0.1-1
- BR: gcc-c++, use %%ldconfig_scriptlets
- 1.0.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Jan Grulich <jgrulich@redhat.com> - 1.0.0-1
- Fix build against PackageKit::Offline

* Tue Jan 16 2018 Jan Grulich <jgrulich@redhat.com> - 1.0.0-1
- 1.0.0

* Fri Jan 12 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.10.0-1
- 0.10.0

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.9.5-5
- drop old Provides: PackageKit-qt
- -Requires/+Recommends: PackageKit

* Tue Oct 27 2015 Rex Dieter <rdieter@fedoraproject.org> 0.9.5-4
- .spec cosmetics

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.5-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Oct 13 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.5-1
- 0.9.5

* Fri Oct 03 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-7
- cleanup, pull in latest upstream fixes, -Qt5 support

* Thu Sep 04 2014 Adam Williamson <awilliam@redhat.com> - 0.9.2-6
- require PackageKit (#1003122)

* Wed Aug 27 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-5
- drop Properly-export-cmake-targets.patch, breaks apper build

* Tue Aug 26 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-4
- pull in some upstream fixes

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.2-1
- 0.9.2 release

* Sat Apr 26 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-0.3.20140424git
- 20140424 snapshot

* Tue Apr 22 2014 Rex Dieter <rdieter@fedoraproject.org> 0.9.0-0.1.20140421git
- fresh git snapshot

* Tue Apr 08 2014 Daniel Vrátil <dvratil@redhat.com> - 0.9.0-0.1
- Update to 0.9.0 git snapshot, 0.8.x does not build against PackageKit 0.9.0 which is in rawhide

* Tue Apr 08 2014 Daniel Vrátil <dvratil@redhat.com> - 0.8.9-1
- Update to latest upstream release

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 09 2013 Richard Hughes <richard@hughsie.com> 0.8.8-1
- New upstream release
- Adding Provides property to Daemon
- Adding some Meta information
- Add missing declare enums
- Adds the transactionFlags to the Transaction class
- Add TransactionFlags registration
- Fix searchGroups() be iterating over the flaged values
- Ignore Interface isValid() check
- Implement connectNotify and disconnectNotify
- Improve error handling and make it easier for QML use it
- Make sure we set an error if we fail to contact PackageKit

* Thu Mar 07 2013 Rex Dieter <rdieter@fedoraproject.org> 0.8.7-3
- pickup/test upstream crash fix (kde#315009)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Richard Hughes <richard@hughsie.com> 0.8.7-1
- New upstream release
- Add back the destroy() signal
- Make our package spliters static
- Make sure we waitForFinishe() when getting the TransactionList
- Only call Cancel() if the transaction proxy exist
- The full namespace is needed for a slot to be called
- Workaround Qt bug not contructing default values when the call fails

* Mon Nov 26 2012 Rex Dieter <rdieter@fedoraproject.org> 0.8.6-3
- fixup dir ownership
- use pkgconfig-style deps
- tighten subpkg dep via %%?_isa

* Mon Nov 26 2012 Richard Hughes <richard@hughsie.com> 0.8.6-2
- Added obsoletes/provides as required for the Fedora package review

* Mon Nov 26 2012 Richard Hughes <richard@hughsie.com> 0.8.6-1
- Initial version for Fedora package review
