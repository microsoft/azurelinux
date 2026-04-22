# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global qt_module qtlocation

Summary: Qt5 - Location component
Name:    qt5-%{qt_module}
Version: 5.15.18
Release: 2%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: (LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0) AND ISC AND BSL-1.0 AND MIT
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-opensource-src-%{version}.tar.xz

## upstream patches
## repo: https://invent.kde.org/qt/qt/qtlocation
## branch: kde/5.15
## git format-patch v5.15.16-lts-lgpl
Patch1:   0001-Fix-appendChildNode-call.patch
Patch5:   0005-Fix-build-of-Qt.labs.location-QML-plugin.patch
Patch6:   0006-Fix-HereMap-plugin-not-supporting-authentication-via.patch

Patch100: 0100-Add-some-missing-cstdint-inclusions-872.patch
Patch101: 0101-Add-missing-include.patch
Patch102: 0102-Removed-non-compiling-assignment-operator.-Fixed-718.patch
Patch103: 0103-Explicitly-disable-copy-assignment-operator.patch
Patch104: 0104-Fix-build-with-ICU-75.patch

Patch200: 0200-Bump-mapbox-gl-native-deps.patch
Patch201: 0201-mapbox-gl-fix-smart-ptr.patch

# filter plugin/qml provides
%global __provides_exclude_from ^(%{_qt5_archdatadir}/qml/.*\\.so|%{_qt5_plugindir}/.*\\.so)$

BuildRequires: make
BuildRequires: qt5-qtbase-devel >= 5.9.0
# QtPositioning core-private
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: qt5-qtdeclarative-devel >= 5.9.0

BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libcrypto)

BuildRequires: boost-devel >= 1.65.1
BuildRequires: earcut-hpp-devel >= 0.12.4
BuildRequires: geometry-hpp-devel >= 0.9.3
BuildRequires: polylabel-devel >= 1.0.3
BuildRequires: protozero-devel >= 1.5.2
BuildRequires: rapidjson-devel >= 1.1.0
BuildRequires: mapbox-variant-devel >= 1.1.4
BuildRequires: wagyu-devel >= 0.4.3

# TODO: use upstream tarballs or unbundle
# geojson-cpp: https://github.com/mapbox/geojson-cpp, ISC
# geojson-vt-cpp: https://github.com/mapbox/geojson-vt-cpp, ISC
# kdbush-hpp: https://github.com/mourner/kdbush.hpp, ISC
# shelf-pack-cpp: https://github.com/mapbox/shelf-pack-cpp, ISC
# supercluster-hpp: https://github.com/mapbox/supercluster.hpp, ISC
# unique-resource: https://github.com/okdshin/unique_resource, BSL-1.0
# vector-tile: https://github.com/mapbox/vector-tile, ISC
# nunicode: https://bitbucket.org/alekseyt/nunicode, MIT
Provides: bundled(geojson-cpp) = 0.5.1
Provides: bundled(geojson-vt-cpp) = 6.6.5
Provides: bundled(kdbush-hpp) = 0.1.3
Provides: bundled(shelf-pack-cpp) = 2.1.1
Provides: bundled(supercluster-hpp) = 0.5.0
Provides: bundled(unique-resource) = 0~gcba309e
Provides: bundled(vector-tile) = 1.0.4
Provides: bundled(nunicode) = 1.11

%description
The Qt Location and Qt Positioning APIs gives developers the ability to
determine a position by using a variety of possible sources, including
satellite, or wifi, or text file, and so on.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%autosetup -n %{qt_module}-everywhere-src-%{version} -p1
rm -rf src/3rdparty/mapbox-gl-native/deps/{boost,earcut,geometry,optional,polylabel,protozero,rapidjson,wagyu,tao_tuple,variant}

%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}

# no shadow builds until fixed: https://bugreports.qt.io/browse/QTBUG-37417
%{qmake_qt5}

%make_build

%install
make install INSTALL_ROOT=%{buildroot}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%ldconfig_scriptlets

%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_qt5_libdir}/libQt5Location.so.5*
%{_qt5_archdatadir}/qml/QtLocation/
%{_qt5_libdir}/qt5/qml/Qt/labs/location/*
%{_qt5_plugindir}/geoservices/
%{_qt5_libdir}/libQt5Positioning.so.5*
%dir %{_qt5_archdatadir}/qml/QtPositioning
%{_qt5_archdatadir}/qml/QtPositioning/*
%{_qt5_plugindir}/position/
%{_qt5_libdir}/libQt5PositioningQuick.so.5*

%files devel
%{_qt5_headerdir}/QtLocation/
%{_qt5_libdir}/libQt5Location.so
%{_qt5_libdir}/libQt5Location.prl
%{_qt5_headerdir}/QtPositioning/
%{_qt5_libdir}/libQt5Positioning.so
%{_qt5_libdir}/libQt5Positioning.prl
%{_qt5_headerdir}/QtPositioningQuick/
%{_qt5_libdir}/libQt5PositioningQuick.so
%{_qt5_libdir}/libQt5PositioningQuick.prl
%{_qt5_libdir}/pkgconfig/Qt5Location.pc
%dir %{_qt5_libdir}/cmake/Qt5Location
%{_qt5_libdir}/cmake/Qt5Location/Qt5Location*.cmake
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_location*.pri
%{_qt5_libdir}/pkgconfig/Qt5Positioning.pc
%dir %{_qt5_libdir}/cmake/Qt5Positioning
%{_qt5_libdir}/cmake/Qt5Positioning/Qt5Positioning*.cmake
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri
%{_qt5_libdir}/pkgconfig/Qt5PositioningQuick.pc
%dir %{_qt5_libdir}/cmake/Qt5PositioningQuick/
%{_qt5_libdir}/cmake/Qt5PositioningQuick/Qt5PositioningQuick*.cmake
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_positioning*.pri

%files examples
%{_qt5_examplesdir}/


%changelog
* Tue Nov 04 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.18-1
- 5.15.18

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 5.15.17-3
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 26 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.17-1
- 5.15.17

* Wed Jan 22 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.16-3
- Rebuild (qt-5.15.16)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Zephyr Lykos <fedora@mochaa.ws> - 5.15.16-1
- 5.15.16
- Unbundle deps

* Wed Sep 04 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.15-1
- 5.15.15

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 29 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.14-1
- 5.15.14

* Thu Mar 14 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.13-1
- 5.15.13

* Thu Feb 01 2024 Pete Walter <pwalter@fedoraproject.org> - 5.15.12-5
- Rebuild for ICU 74

* Tue Jan 30 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.12-4
- Fix build of bundled rapidjson

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.12-1
- 5.15.12

* Fri Oct 06 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.11-1
- 5.15.11

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 5.15.10-2
- Rebuilt for ICU 73.2

* Mon Jun 12 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.10-1
- 5.15.10

* Tue Apr 11 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.9-1
- 5.15.9

* Mon Feb 20 2023 Than Ngo <than@redhat.com> - 5.15.8-4
- Fixed FTBFS

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.8-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.8-1
- 5.15.8

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 5.15.7-2
- Rebuild for ICU 72

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.7-1
- 5.15.7

* Tue Sep 20 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-1
- 5.15.6

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.15.5-3
- Rebuilt for ICU 71.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.5-1
- 5.15.5

* Mon May 16 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.4-1
- 5.15.4

* Fri Mar 04 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.3-1
- 5.15.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 5.15.2-6
- Rebuild for ICU 69

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 5.15.2-5
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 15 15:15:20 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-3
- Bump for eln build

* Tue Nov 24 07:54:14 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-2
- Rebuild for qtbase with -no-reduce-relocations option

* Fri Nov 20 09:30:46 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2

* Thu Sep 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-1
- 5.15.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Jeff Law <law@redhat.com> - 5.14.2-3
- Disable LTO

* Sat May 16 2020 Pete Walter <pwalter@fedoraproject.org> - 5.14.2-2
- Rebuild for ICU 67

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-1
- 5.13.2

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 5.12.5-3
- Rebuild for ICU 65

* Wed Sep 25 2019 Than Ngo <than@redhat.com> - 5.12.5-2
- fixed build failures with gcc10

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-1
- 5.12.4

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-1
- 5.12.3

* Fri Feb 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 5.11.3-2
- Rebuild for ICU 63

* Fri Dec 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.2-1
- 5.11.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 5.11.1-2
- Rebuild for ICU 62

* Tue Jun 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Sun May 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0
- drop old G_INIT_VALUE patch (el6 too old anyway)

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 5.10.1-4
- Rebuild for ICU 61.1

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 5.10.1-3
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-2
- rebuild (gcc)
- use %%make_build %%ldconfig_scriptlets

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 5.10.1-1
- 5.10.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 5.9.3-2
- Rebuild for ICU 60.1

* Thu Nov 23 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Mon Oct 09 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.2-1
- 5.9.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Fri Jun 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- drop shadow/out-of-tree builds (#1456211,QTBUG-37417)
- directly reference other qt5-related build deps

* Wed May 31 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Upstream official release

* Fri May 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Upstream Release Candidate retagged

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.0-0.beta.3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue May 09 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Upstream beta 3

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-2
- build docs on all archs

* Mon Jan 30 2017 Helio Chissini de Castro <helio@kde.org> - 5.8.0-1
- New upstream version

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-4
- filter plugins too

* Mon Jan 02 2017 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-3
- filter qml provides, BR: qt5-qtdeclarative explicitly

* Sat Dec 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- drop BR: cmake (handled by qt5-rpm-macros now)
- 5.7.1 dec5 snapshot

* Wed Nov 09 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Compiled with gcc

* Tue Jun 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release

* Thu Jun 09 2016 Jan Grulich <jgrulich@redhat.com> - 5.6.1-1
- Update to 5.6.1

* Thu Apr 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-4
- BR: qt5-qtbase-private-devel

* Sun Mar 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-3
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-2
- rebuild

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.10.rc
- Update to final RC

* Sun Feb 21 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.9.rc
- rebuild

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.8
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.7.beta
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.6.beta
- update source URL, use %%license, BR: cmake

* Mon Dec 21 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.5
- Update to final beta release

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-0.4
- (re) add bootstrap macro support
- drop geoclue(1) dep (unused at build time anyway (#1286886)
- drop (deprecated) gypsy support (#1069225)

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.3
- Official beta release

* Sun Dec 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.2
- (re)add bootstrap macro support

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 beta

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- -docs: BuildRequires: qt5-qhelpgenerator, standardize bootstrapping

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- tighten qtbase dep (#1233829), .spec cosmetics, (re)enable docs

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Wed Jun 24 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Mon Jun 15 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Mon Feb 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-3
- rebuild (gcc5)

* Wed Dec 31 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-2
- BR: pkgconfig(Qt5Qml) > 5.4.0 (#1177986)

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.3.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.2.beta
- out-of-tree build, use %%qmake_qt5

* Sun Oct 19 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.beta
- 5.4.0-beta

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Mon May 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- sanitize .prl file(s)

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- build -examples only when supported

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -examples subpkg

* Thu Jan 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- first try
