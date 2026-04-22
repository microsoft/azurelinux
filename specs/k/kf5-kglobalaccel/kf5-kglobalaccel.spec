# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond kf6_compat %[0%{?fedora} >= 40 || 0%{?rhel} >= 10]

%global framework kglobalaccel

Name:    kf5-%{framework}
Version: 5.116.0
Release: 5%{?dist}
Summary: KDE Frameworks 5 Tier 3 integration module for global shortcuts

License: CC0-1.0 AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-3.0-only AND (LGPL-2.1-only OR LGPL-3.0-only)
URL:     https://invent.kde.org/frameworks/%{framework}

%global majmin %majmin_ver_kf5
%global stable %stable_kf5
Source0:        http://download.kde.org/%{stable}/frameworks/%{majmin}/%{framework}-%{version}.tar.xz

## upstream fixes

BuildRequires:  extra-cmake-modules >= %{majmin}
BuildRequires:  kf5-rpm-macros
BuildRequires:  kf5-kconfig-devel >= %{majmin}
BuildRequires:  kf5-kcoreaddons-devel >= %{majmin}
BuildRequires:  kf5-kcrash-devel >= %{majmin}
BuildRequires:  kf5-kdbusaddons-devel >= %{majmin}
BuildRequires:  kf5-kwindowsystem-devel >= %{majmin}

# for systemd-related macros
BuildRequires:  systemd

BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5X11Extras)

BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%if %{without kf6_compat}
Conflicts:      kglobalacceld
%endif

%description
%{summary}.

%package        libs
Summary:        Runtime libraries for %{name}
Requires:       %{name} = %{version}-%{release}
%description    libs
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{framework}-%{version}


%build
%cmake_kf5 %{?with_kf6_compat:-DBUILD_RUNTIME=OFF}
%cmake_build


%install
%cmake_install

# unpackaged files
%if 0%{?flatpak:1}
rm -fv %{buildroot}%{_prefix}/lib/systemd/user/plasma-kglobalaccel.service
%endif


%find_lang_kf5 kglobalaccel5_qt


%files -f kglobalaccel5_qt.lang
%doc README.md
%license LICENSES/*.txt
%{_kf5_datadir}/qlogging-categories5/%{framework}*
%if %{without kf6_compat}
%{_kf5_bindir}/kglobalaccel5
%{_kf5_datadir}/kservices5/kglobalaccel5.desktop
%{_datadir}/dbus-1/services/org.kde.kglobalaccel.service
%if ! 0%{?flatpak:1}
%{_userunitdir}/plasma-kglobalaccel.service
%endif
%endif

%files libs
%{_kf5_libdir}/libKF5GlobalAccel.so.*
%if %{without kf6_compat}
%{_kf5_libdir}/libKF5GlobalAccelPrivate.so.*
%{_kf5_qtplugindir}/org.kde.kglobalaccel5.platforms/
%endif

%files devel
%{_kf5_includedir}/KGlobalAccel/
%{_kf5_libdir}/libKF5GlobalAccel.so
%{_kf5_libdir}/cmake/KF5GlobalAccel/
%{_kf5_archdatadir}/mkspecs/modules/qt_KGlobalAccel.pri
%{_kf5_datadir}/dbus-1/interfaces/*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.116.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.116.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.116.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun May 19 2024 Alessandro Astone <ales.astone@gmail.com> - 5.116.0-1
- 5.116.0

* Sat Feb 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.115.0-1
- 5.115.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.113.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.113.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 08 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.113.0-1
- 5.113.0

* Sun Dec 03 2023 Alessandro Astone <ales.astone@gmail.com> - 5.111.0-10
- Don't require kglobalacceld

* Mon Nov 20 2023 Steve Cossette <farchord@gmail.com> - 5.111.0-9
- Preparation for Plasma 6

* Mon Nov 20 2023 Alessandro Astone <ales.astone@gmail.com> - 5.111.0-8
- Conflicts kglobalacceld

* Mon Nov 20 2023 Alessandro Astone <ales.astone@gmail.com> - 5.111.0-7
- Remove Obsoletes kglobalacceld

* Tue Oct 24 2023 Alessandro Astone <ales.astone@gmail.com> - 5.111.0-6
- Add Obsoletes: to upgrade from the compat build

* Tue Oct 24 2023 Alessandro Astone <ales.astone@gmail.com> - 5.111.0-5
- Re-enable the daemon until Plasma 6

* Wed Oct 18 2023 Alessandro Astone <ales.astone@gmail.com> - 5.111.0-4
- Require the new kglobalacceld if compat build

* Mon Oct 16 2023 Alessandro Astone <ales.astone@gmail.com> - 5.111.0-3
- Require kf6-kglobalaccel if compat build

* Thu Oct 12 2023 Alessandro Astone <ales.astone@gmail.com> - 5.111.0-2
- Backport patch for KF6 coinstallability

* Tue Oct 10 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.111.0-1
- 5.111.0

* Mon Oct 09 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.110.0-4
- Re-enable building kglobalaccel runtime code

* Sun Oct 08 2023 Steve Cossette <farchord@gmail.com> - 5.110.0-3
- Added logic and build flag for co-installation with KF6

* Tue Sep 05 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.110.0-1
- 5.110.0

* Sat Aug 05 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.109.0-1
- 5.109.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.108.0-2
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

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.102.0-2
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

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.96.0-2
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

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.90.0-2
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

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.83.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.83.0-1
- 5.83.0

* Mon May 03 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.82.0-1
- 5.82.0

* Mon Apr 12 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.81.0-2
- upstream fix: avoid service restarts

* Tue Apr 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.81.0-1
- 5.81.0

* Sat Apr 03 2021 Onuralp SEZER <thunderbirdtr@fedoraproject.org> - 5.80.0-3
- remove service for flatpak build fix

* Fri Mar 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.80.0-2
- pull in upstream uid fix

* Tue Mar 09 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.80.0-1
- 5.80.0

* Sat Feb 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.79.0-2
- respin

* Sat Feb 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.79.0-1
- 5.79.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.78.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan  4 08:46:23 CST 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.78.0-1
- 5.78.0

* Sun Dec 13 14:13:12 CST 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.77.0-1
- 5.77.0

* Thu Nov 19 09:02:11 CST 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.76.0-1
- 5.76.0
- .spec cleanup, update URL
- use upstream kglobalaccel.service implementation

* Wed Oct 14 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.75.0-2
- systemd kglobalaccel.service (#1861700)

* Wed Oct 14 09:54:23 CDT 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.75.0-1
- 5.75.0

* Fri Sep 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.74.0-1
- 5.74.0

* Mon Aug 03 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.73.0-1
- 5.73.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.72.0-2
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

* Sun Feb 02 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.67.0-1
- 5.67.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.66.0-2
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

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.60.0-2
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

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.54.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.54.0-1
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

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.48.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.48.0-1
- 5.48.0

* Fri Jun 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-3
- -devel: drop extraneous cmake(Qt5...) deps

* Thu Jun 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-2
- cleanup, use %%make_build %%ldconfig_scriptlets

* Sat Jun 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.47.0-1
- 5.47.0

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

* Fri Nov 10 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.40.0-1
- 5.40.0

* Sun Oct 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.39.0-1
- 5.39.0

* Thu Sep 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.38.1-1
- 5.38.1, fix %%description (sync w/summary), cosmetics

* Mon Sep 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.38.0-1
- 5.38.0

* Fri Aug 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.37.0-1
- 5.37.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.36.0-1
- 5.36.0

* Sun Jun 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.35.0-1
- 5.35.0

* Mon May 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.34.0-1
- 5.34.0

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.33.0-1
- 5.33.0

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.32.0-1
- 5.32.0

* Mon Feb 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.31.0-1
- 5.31.0

* Fri Dec 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.29.0-1
- 5.29.0

* Tue Oct 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Wed Sep 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.26.0-1
- KDE Frameworks 5.26.0

* Mon Aug 08 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.25.0-1
- KDE Frameworks 5.25.0

* Wed Jul 06 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.24.0-1
- KDE Frameworks 5.24.0

* Tue Jun 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.23.0-1
- KDE Frameworks 5.23.0

* Tue Jun 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-2
- update URL, use autosetup

* Mon May 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.22.0-1
- KDE Frameworks 5.22.0

* Mon Apr 04 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.21.0-1
- KDE Frameworks 5.21.0

* Mon Mar 14 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.20.0-1
- KDE Frameworks 5.20.0

* Thu Feb 11 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.19.0-1
- KDE Frameworks 5.19.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Rex Dieter <rdieter@fedoraproject.org> 5.18.0-2
- cosmetics, update URL, use %%license, move plugins to -libs

* Sun Jan 03 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.18.0-1
- KDE Frameworks 5.18.0

* Tue Dec 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.17.0-1
- KDE Frameworks 5.17.0

* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.16.0-1
- KDE Frameworks 5.16.0

* Thu Oct 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.15.0-1
- KDE Frameworks 5.15.0

* Wed Sep 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.14.0-1
- KDE Frameworks 5.14.0

* Wed Aug 19 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-1
- KDE Frameworks 5.13.0

* Wed Aug 19 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-1
- KDE Frameworks 5.13.0

* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13

* Thu Jul 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.12.0-1
- 5.12.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-1
- KDE Frameworks 5.10.0

* Wed Apr 22 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- backport logging fix (kde#346429)
- -libs: add dep on main pkg
- bump minimal build deps

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- KDE Frameworks 5.9.0

* Mon Mar 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.8.0-1
- KDE Frameworks 5.8.0

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- Rebuild (GCC 5)

* Fri Feb 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.7.0-2
- Conflicts: plasma-workspace < 5.2.0-8

* Mon Feb 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Thu Jan 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0

* Mon Dec 08 2014 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-1
- KDE Frameworks 5.5.0

* Mon Nov 03 2014 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- KDE Frameworks 5.4.0

* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- KDE Frameworks 5.3.0

* Thu Sep 11 2014 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- KDE Frameworks 5.2.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.100.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Tue May 06 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-2
- Rebuild against updated kf5-rpm-macros

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-1
- KDE Frameworks 4.99.0

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-release snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
