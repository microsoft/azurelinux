# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global framework qqc2-desktop-style

Name:    kf5-%{framework}
Version: 5.116.1
Release: 4%{?dist}
Summary: QtQuickControls2 style for consistency between QWidget and QML apps
License: LGPL-2.0-or-later AND (LGPL-3.0-only OR GPL-2.0-or-later) AND (LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only)
URL:     https://invent.kde.org/frameworks/%{framework}
Source:  https://download.kde.org/%{stable_kf5}/frameworks/%{majmin_ver_kf5}/%{framework}-%{version}.tar.xz

## upstream patches

BuildRequires: extra-cmake-modules >= %{majmin_ver_kf5}
BuildRequires: gcc-c++
BuildRequires: kf5-rpm-macros

BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Gui)
BuildRequires: cmake(Qt5Quick)
BuildRequires: cmake(Qt5QuickControls2)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5X11Extras)
BuildRequires: cmake(Qt5LinguistTools)

BuildRequires: cmake(KF5Config) >= %{majmin_ver_kf5}
BuildRequires: cmake(KF5ConfigWidgets) >= %{majmin_ver_kf5}
BuildRequires: cmake(KF5Kirigami2) >= %{majmin_ver_kf5}
BuildRequires: cmake(KF5IconThemes) >= %{majmin_ver_kf5}

Requires: kf5-kirigami2%{?_isa} >= %{majmin_ver_kf5}
Requires: kf5-sonnet%{?_isa} >= %{majmin_ver_kf5}
Requires: qt5-qtquickcontrols2%{?_isa}

# renamed
Provides:  %{framework} = %{version}-%{release}
Provides:  %{framework}%{?_isa} = %{version}-%{release}
Obsoletes: %{framework} < %{version}-%{release}

%description
This is a style for QtQuickControls 2 that uses QWidget's QStyle for
painting, making possible to achieve an higher degree of consistency
between QWidget-based and QML-based apps.


%prep
%autosetup -n %{framework}-%{version} -p1


%build
%cmake_kf5
%cmake_build


%install
%cmake_install
%find_lang_kf5 qqc2desktopstyle5_qt


%files -f qqc2desktopstyle5_qt.lang
%doc README.md
%license LICENSES/*.txt
%dir %{_kf5_plugindir}/kirigami/
%{_kf5_plugindir}/kirigami/org.kde.desktop.so
%{_kf5_qmldir}/QtQuick/Controls.2/org.kde.desktop/
%{_kf5_qmldir}/org/kde/qqc2desktopstyle/
%{_kf5_libdir}/cmake/KF5QQC2DeskopStyle/
%{_kf5_libdir}/cmake/KF5QQC2DesktopStyle/


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.116.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.116.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.116.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 22 2024 Alessandro Astone <ales.astone@gmail.com> - 5.116.1-1
- Fix translations coinstallability with KF6

* Sun May 19 2024 Alessandro Astone <ales.astone@gmail.com> - 5.116.0-1
- 5.116.0
- Require kf5-sonnet for QML

* Wed Mar 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5.115.0-2
- Renamed with kf5- prefix

* Sat Feb 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.115.0-1
- 5.115.0

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.113.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.113.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.113.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 08 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.113.0-1
- 5.113.0

* Tue Oct 10 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.111.0-1
- 5.111.0

* Tue Sep 05 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.110.0-1
- 5.110.0

* Sat Aug 05 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.109.0-1
- 5.109.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.108.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 02 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.108.0-1
- 5.108.0

* Sat Jun 03 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.107.0-1
- 5.107.0

* Mon May 15 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.106.0-1
- 5.106.0

* Sun Apr 02 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.105.0-1
- 5.105.0

* Sat Mar 04 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.104.0-1
- 5.104.0

* Sun Feb 05 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.103.0-1
- 5.103.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.102.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jan 14 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.102.0-1
- 5.102.0

* Mon Dec 12 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.101.0-1
- 5.101.0
- use new macros to simplify code

* Sun Nov 06 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.100.0-1
- 5.100.0

* Fri Oct 14 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.99.0-1
- 5.99.0

* Thu Sep 15 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.98.0-1
- 5.98.0

* Sat Aug 13 2022 Justin Zobel <justin@1707.io> - 5.97.0-1
- Update to 5.97.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.96.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.96.0-1
- 5.96.0

* Fri May 13 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.94.0-1
- 5.94.0

* Sun Apr 10 2022 Justin Zobel <justin@1707.io> - 5.93-1
- Update to 5.93

* Thu Mar 10 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.92.0-1
- 5.92.0

* Fri Feb 11 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.91.0-1
- 5.91.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.90.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Marc Deop i Argemí (Private) <marc@marcdeop.com> - 5.90.0-1
- 5.90.0

* Wed Dec 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.89.0-1
- 5.89.0

* Mon Nov 08 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.88.0-1
- 5.88.0

* Tue Oct 05 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.87.0-1
- 5.87.0

* Tue Sep 14 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.86.0-1
- 5.86.0

* Thu Aug 12 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.85.0-1
- 5.85.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.83.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.83.0-1
- 5.83.0

* Mon May 03 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.82.0-1
- 5.82.0

* Tue Apr 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.81.0-1
- 5.81.0

* Tue Mar 09 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.80.0-1
- 5.80.0

* Sat Feb 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.79.0-2
- respin

* Sat Feb 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.79.0-1
- 5.79.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.78.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan  4 09:00:58 CST 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.78.0-1
- 5.78.0

* Sun Dec 13 14:26:50 CST 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.77.0-1
- 5.77.0

* Thu Nov 19 09:21:50 CST 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.76.0-1
- 5.76.0

* Wed Oct 14 10:16:43 CDT 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.75.0-1
- 5.75.0

* Fri Sep 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.74.0-1
- 5.74.0

* Mon Aug 03 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.73.0-1
- 5.73.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.72.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.72.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.72.0-1
- 5.72.0

* Tue Jun 16 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.71.0-1
- 5.71.0

* Mon May 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.70.0-1
- 5.70.0

* Tue Apr 21 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.69.0-1
- 5.69.0

* Fri Mar 20 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.68.0-1
- 5.68.0

* Tue Feb 11 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.67.1-1
- 5.67.1

* Mon Feb 03 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.67.0-1
- 5.67.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.66.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.66.0-1
- 5.66.0

* Tue Dec 17 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.65.0-1
- 5.65.0

* Fri Nov 08 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.64.0-1
- 5.64.0

* Tue Oct 22 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.63.0-1
- 5.63.0

* Mon Sep 16 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.62.0-1
- 5.62.0

* Wed Aug 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.61.0-1
- 5.61.0

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.60.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.60.0-1
- 5.60.0

* Thu Jun 06 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.59.0-1
- 5.59.0

* Tue May 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.58.0-1
- 5.58.0

* Tue Apr 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.57.0-1
- 5.57.0

* Tue Mar 05 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.56.0-1
- 5.56.0

* Mon Feb 04 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.55.0-1
- 5.55.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.54.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 18 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.54.0-2
- add versioned runtime dep for kf5-kirigami2

* Wed Jan 09 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.54.0-1
- 5.54.0

* Sun Dec 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.53.0-1
- 5.53.0

* Sun Nov 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.52.0-1
- 5.52.0

* Wed Oct 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.51.0-1
- 5.51.0

* Tue Sep 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.50.0-1
- 5.50.0

* Tue Aug 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.49.0-1
- 5.49.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.48.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.48.0-1
- 5.48.0

* Sat Jun 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-1
- 5.47.0

* Thu May 17 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.46.2-1
- 5.46.2

* Wed May 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.46.1-1
- 5.46.1

* Wed May 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.46.0-2
- pull in upstream fixes, use %%make_build

* Sat May 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.46.0-1
- 5.46.0

* Sun Apr 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.45.0-1
- 5.45.0

* Sat Mar 03 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.44.0-1
- 5.44.0

* Wed Feb 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.43.0-1
- 5.43.0

* Mon Jan 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.42.0-1
- 5.42.0

* Mon Dec 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.41.0-1
- 5.41.0

* Wed Nov 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.40.0-1
- 5.40.0

* Wed Oct 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.39.0-1
- qqc2-desktop-style

