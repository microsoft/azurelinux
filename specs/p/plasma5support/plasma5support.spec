# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:    plasma5support
Summary: Support components for porting from KF5/Qt5 to KF6/Qt6
Version: 6.6.0
Release: 1%{?dist}

License: CC0-1.0 AND GPL-2.0-or-later AND LGPL-2.0-or-later
URL:     https://invent.kde.org/plasma/%{name}

Source0:  https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{name}-%{version}.tar.xz
Source1:  https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{name}-%{version}.tar.xz.sig

BuildRequires:  extra-cmake-modules
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  kf6-rpm-macros
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6Sql)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6Service)
BuildRequires:  cmake(KF6Solid)
BuildRequires:  cmake(KF6IdleTime)
BuildRequires:  cmake(KF6NetworkManagerQt)
BuildRequires:  cmake(KF6UnitConversion)
BuildRequires:  cmake(KF6Holidays)
BuildRequires:  cmake(PlasmaActivities)
BuildRequires:  cmake(KSysGuard)
BuildRequires:  cmake(Plasma)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(libgps)
Requires:  kf6-filesystem

# Renamed from kf6-plasma5support
Obsoletes:      kf6-plasma5support < 1:%{version}-%{release}
Provides:       kf6-plasma5support = 1:%{version}-%{release}
# Geolocation libs got split off from plasma-workspace
Obsoletes: plasma-workspace-geolocation < 6.2.90-1
Provides:  plasma-workspace-geolocation = %{version}-%{release}
Obsoletes: plasma-workspace-geolocation-libs < 6.2.90-1
Provides:  plasma-workspace-geolocation-libs = %{version}-%{release}

%description
%{summary}.

%package devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt6-qtbase-devel
Obsoletes:      kf6-plasma5support-devel < 1:%{version}-%{release}
Provides:       kf6-plasma5support-devel = 1:%{version}-%{release}
# Geolocation devel components were part of plasma-workspace-devel
Conflicts: plasma-workspace-devel < 6.2.90-1
%description    devel
%{summary}.

%package        doc
Summary:        Developer Documentation files for %{name}
BuildArch:      noarch
%description    doc
Developer Documentation files for %{name} for use with KDevelop or QtCreator.

%prep
%autosetup -p1

%build
%cmake_kf6
%cmake_build

%install
%cmake_install
%find_lang libplasma5support --with-qt --with-kde --all-name

%files -f libplasma5support.lang
%doc README.md
%license LICENSES/*.txt
%{_qt6_qmldir}/org/kde/plasma/plasma5support/
%{_datadir}/plasma5support/
%{_datadir}/qlogging-categories6/plasma5support.categories
%{_datadir}/qlogging-categories6/plasma5support.renamecategories
%{_kf6_libdir}/libPlasma5Support.so.6
%{_kf6_libdir}/libPlasma5Support.so.%{version}
%{_kf6_qtplugindir}/plasma5support/
%{_libdir}/libplasma-geolocation-interface.so.6
%{_libdir}/libplasma-geolocation-interface.so.%{version}
%{_libdir}/libweather_ion.so.7
%{_libdir}/libweather_ion.so.7.0.0
%{_kf6_datadir}/plasma/weather_legacy/noaa_station_list.xml

%files devel
%{_includedir}/Plasma5Support/
%{_kf6_libdir}/cmake/Plasma5Support/
%{_qt6_docdir}/*.tags
%{_kf6_libdir}/libPlasma5Support.so
%{_libdir}/libweather_ion.so
%{_libdir}/libplasma-geolocation-interface.so
%{_includedir}/plasma/geolocation/
%{_includedir}/plasma5support/

%files doc
%{_qt6_docdir}/*.qch

%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Tue Jan 27 2026 Steve Cossette <farchord@gmail.com> - 6.5.91-1
- 6.5.91

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 farchord@gmail.com - 6.5.90-1
- 6.5.90

* Wed Jan 14 2026 Jitka Plesnikova <jplesnik@redhat.com> - 6.5.5-2
- Rebuild for new gpsd

* Tue Jan 13 2026 farchord@gmail.com - 6.5.5-1
- 6.5.5

* Tue Dec 09 2025 Steve Cossette <farchord@gmail.com> - 6.5.4-1
- 6.5.4

* Tue Nov 18 2025 Steve Cossette <farchord@gmail.com> - 6.5.3-1
- 6.5.3

* Tue Nov 04 2025 Steve Cossette <farchord@gmail.com> - 6.5.2-1
- 6.5.2

* Tue Oct 28 2025 Steve Cossette <farchord@gmail.com> - 6.5.1-1
- 6.5.1

* Fri Oct 17 2025 Steve Cossette <farchord@gmail.com> - 6.5.0-1
- 6.5.0

* Thu Oct 02 2025 Steve Cossette <farchord@gmail.com> - 6.4.91-1
- 6.4.91

* Tue Sep 30 2025 Jan Grulich <jgrulich@redhat.com> - 6.4.5-2
- Rebuild (qt6)

* Thu Sep 25 2025 Steve Cossette <farchord@gmail.com> - 6.4.90-1
- 6.4.90

* Tue Sep 16 2025 farchord@gmail.com - 6.4.5-1
- 6.4.5

* Wed Aug 06 2025 Steve Cossette <farchord@gmail.com> - 6.4.4-1
- 6.4.4

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Steve Cossette <farchord@gmail.com> - 6.4.3-1
- 6.4.3

* Thu Jul 03 2025 Steve Cossette <farchord@gmail.com> - 6.4.2-1
- 6.4.2

* Tue Jun 24 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.1-1
- 6.4.1

* Mon Jun 16 2025 Steve Cossette <farchord@gmail.com> - 6.4.0-1
- 6.4.0

* Sat May 31 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.91-2
- Add signature file

* Fri May 30 2025 Steve Cossette <farchord@gmail.com> - 6.3.91-1
- 6.3.91

* Tue May 27 2025 Remi Collet <remi@fedoraproject.org> - 6.3.90-2
- rebuild for new gpsd

* Thu May 15 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.90-1
- 6.3.90

* Tue May 06 2025 Steve Cossette <farchord@gmail.com> - 6.3.5-1
- 6.3.5

* Mon Apr 14 2025 Jan Grulich <jgrulich@redhat.com> - 6.3.4-2
- Rebuild (qt6)

* Wed Apr 02 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.4-1
- 6.3.4

* Tue Mar 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.3.3-2
- Rebuild (qt6)

* Tue Mar 11 2025 Steve Cossette <farchord@gmail.com> - 6.3.3-1
- 6.3.3

* Tue Feb 25 2025 Steve Cossette <farchord@gmail.com> - 6.3.2-1
- 6.3.2

* Tue Feb 18 2025 Steve Cossette <farchord@gmail.com> - 6.3.1-1
- 6.3.1

* Thu Feb 06 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.0-1
- 6.3.0

* Thu Jan 23 2025 Steve Cossette <farchord@gmail.com> - 6.2.91-1
- 6.2.91

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Steve Cossette <farchord@gmail.com> - 6.2.90-1
- Beta 6.2.90

* Tue Dec 31 2024 Steve Cossette <farchord@gmail.com> - 6.2.5-1
- 6.2.5

* Tue Nov 26 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.4-1
- 6.2.4

* Tue Nov 05 2024 Steve Cossette <farchord@gmail.com> - 6.2.3-1
- 6.2.3

* Tue Oct 22 2024 Steve Cossette <farchord@gmail.com> - 6.2.2-1
- 6.2.2

* Tue Oct 15 2024 Steve Cossette <farchord@gmail.com> - 6.2.1-1
- 6.2.1

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 6.2.0-2
- Rebuild (qt6)

* Thu Oct 03 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Thu Sep 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.90-1
- 6.1.90

* Tue Sep 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.5-1
- 6.1.5

* Fri Aug 09 2024 Steve Cossette <farchord@gmail.com> - 6.1.4-1
- 6.1.4

* Wed Jul 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.3-3
- rebuilt

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.3-1
- 6.1.3

* Wed Jul 03 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.2-1
- 6.1.2

* Tue Jun 25 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.1-1
- 6.1.1

* Thu Jun 13 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-1
- 6.1.0

* Fri May 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.90-1
- 6.0.90

* Wed May 22 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.5-1
- 6.0.5

* Tue Apr 16 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.4-1
- 6.0.4

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.0.3-3
- Rebuild (qt6)

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.0.3-2
- Rebuild (qt6)

* Tue Mar 26 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.3-1
- 6.0.3

* Tue Mar 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.2-1
- 6.0.2

* Sat Mar 09 2024 Marie Loise Nolden <loise@kde.org> - 6.0.1-2
- add missing BuildArch: noarch to -doc package

* Wed Mar 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.1-1
- 6.0.1

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 5.93.0-2
- Rebuild (qt6)

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.93.0-1
- 5.93.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 14 2024 Steve Cossette <farchord@gmail.com> - 5.92.0-2
- Fixed non-devel library in devel subpackage issue (rhbz# 2258332).

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.92.0-1
- 5.92.0

* Tue Jan 09 2024 Marie Loise Nolden <loise@kde.org> - 5.91.0-2
- add doc package for KF6 API

* Thu Dec 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.91.0-1
- 5.91.0

* Sun Dec 03 2023 Justin Zobel <justin.zobel@gmail.com> - 5.90.0-1
- Update to 5.90.0

* Wed Nov 29 2023 Jan Grulich <jgrulich@redhat.com> - 5.27.80-3
- Rebuild (qt6)

* Sun Nov 12 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-2
- Add Obsoletes/Provides to the devel subpackage

* Fri Nov 10 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-1
- Renamed from kf6-plasma5support
- 5.27.80

* Sat Sep 23 2023 Steve Cossette <farchord@gmail.com> - 5.240.0^20231011.222045.245b3dd-1
- Initial release
