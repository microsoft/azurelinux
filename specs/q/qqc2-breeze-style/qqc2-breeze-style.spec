# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:    qqc2-breeze-style
Version: 6.6.0
Release: 2%{?dist}
Summary: QtQuickControls2 breeze style

License: CC0-1.0 and GPL-2.0-or-later AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-3.0-only AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only)
URL:     https://invent.kde.org/plasma/%{name}

Source0: https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{name}-%{version}.tar.xz
Source1: https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{name}-%{version}.tar.xz.sig

## upstream patches

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: extra-cmake-modules
BuildRequires: kf6-rpm-macros

BuildRequires: cmake(KF6ColorScheme)
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6GuiAddons)
BuildRequires: cmake(KF6IconThemes)
BuildRequires: cmake(KF6KirigamiPlatform)
BuildRequires: cmake(KF6QuickCharts)

BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel

Requires:       kf6-kquickcharts


%description
This is a pure Qt Quick/Kirigami Qt Quick Controls style.

%prep
%autosetup -n %{name}-%{version} -p1


%build
%cmake_kf6
%cmake_build


%install
%cmake_install


%files 
%doc README.md
%license LICENSES/*.txt
%{_kf6_plugindir}/kirigami/platform/org.kde.breeze.so
%{_qt6_qmldir}/org/kde/breeze/
%{_kf6_libdir}/cmake/QQC2BreezeStyle/

%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Tue Jan 27 2026 Steve Cossette <farchord@gmail.com> - 6.5.91-1
- 6.5.91

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 farchord@gmail.com - 6.5.90-1
- 6.5.90

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

* Thu May 15 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.90-1
- 6.3.90

* Tue May 06 2025 Steve Cossette <farchord@gmail.com> - 6.3.5-1
- 6.3.5

* Wed Apr 02 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.4-1
- 6.3.4

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

* Tue Mar 26 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.3-1
- 6.0.3

* Tue Mar 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.2-1
- 6.0.2

* Wed Mar 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.1-1
- 6.0.1

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.93.0-1
- 5.93.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.92.0-1
- 5.92.0

* Thu Dec 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.91.0-1
- 5.91.0

* Sun Dec 03 2023 Justin Zobel <justin.zobel@gmail.com> - 5.90.0-1
- Update to 5.90.0

* Fri Nov 24 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-1
- 5.27.80

* Tue Oct 24 2023 Steve Cossette <farchord@gmail.com> - 5.27.9-1
- 5.27.9

* Tue Sep 12 2023 justin.zobel@gmail.com - 5.27.8-1
- 5.27.8

* Tue Aug 01 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.7-1
- 5.27.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.27.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 25 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.6-1
- 5.27.6

* Wed May 10 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.5-1
- 5.27.5

* Tue Apr 04 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.4-1
- 5.27.4

* Tue Mar 14 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.3-1
- 5.27.3

* Tue Feb 28 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.2-1
- 5.27.2

* Tue Feb 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.1-1
- 5.27.1

* Thu Feb 09 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.26.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 19 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.26.90-1
- 5.26.90

* Thu Jan 05 2023 Justin Zobel <justin@1707.io> - 5.26.5-1
- Update to 5.26.5

* Tue Nov 29 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.4-1
- 5.26.4

* Wed Nov 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.3-1
- 5.26.3

* Wed Oct 26 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.2-1
- 5.26.2

* Tue Oct 18 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.1-1
- 5.26.1

* Thu Oct 06 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.0-1
- 5.26.0

* Sat Sep 17 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.90-1
- 5.25.90

* Wed Sep 07 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.5-1
- 5.25.5

* Wed Aug 03 2022 Justin Zobel <justin@1707.io> - 5.25.4-1
- Update to 5.25.4

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.25.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.3-1
- 5.25.3

* Tue Jun 28 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.2-1
- 5.25.2

* Tue Jun 21 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.1-1
- 5.25.1

* Thu Jun 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.0-1
- 5.25.0

* Fri May 20 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.90-1
- 5.24.90

* Tue May 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.5-1
- 5.24.5

* Thu Mar 31 2022 Justin Zobel <justin@1707.io> - 5.24.4-1
- Update to 5.24.4

* Tue Mar 08 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.3-1
- 5.24.3

* Tue Feb 22 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.24.2-1
- 5.24.2

* Tue Feb 15 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.1-1
- 5.24.1

* Thu Feb 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.0-1
- 5.24.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.23.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.90-1
- 5.23.90

* Tue Jan 04 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.5-1
- 5.23.5

* Tue Dec 14 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.4-1
- 5.23.4

* Wed Nov 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.3-1
- 5.23.3

* Tue Oct 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.2-1
- 5.23.2

* Sat Oct 23 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.1-1
- 5.23.1

* Fri Oct 08 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.0-1
- 5.23.0

* Fri Sep 17 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-1
- 5.22.90

* Tue Aug 31 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.5-1
- 5.22.5

* Tue Jul 27 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.4-1
- 5.22.4

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.3-1
- 5.22.3

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2.1-1
- 5.22.2.1

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2-1
- 5.22.2

* Tue Jun 15 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.1-1
- 5.22.1

* Sun Jun 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.0-1
- 5.22.0

* Tue May 04 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.5-1
- 5.21.5

* Tue Apr 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.4-1
- 5.21.4

* Tue Mar 16 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.3-1
- 5.21.3

* Tue Mar 02 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.2-1
- 5.21.2

* Tue Feb 23 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.1-1
- 5.21.1

* Thu Feb 11 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.0-1
- 5.21.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.20.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.90-1
- 5.20.90 (beta)
