# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global qt_module qtdatavis3d

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

%global examples 1

Summary: Qt6 - Qt Data Visualization component
Name:    qt6-%{qt_module}
Version: 6.10.2
Release: 1%{?dist}

License: GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel >= %{version}
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: openssl-devel

%description
Qt Data Visualization module provides multiple graph types to visualize data in
3D space both with C++ and Qt Quick 2.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1


%build
%cmake_qt6 \
    -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
    -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build

%install
%cmake_install

%files
%license LICENSES/GPL*
%{_qt6_archdatadir}/sbom/qtdatavisualization-%{qt_version}.spdx
%{_qt6_libdir}/libQt6DataVisualization.so.6*
%{_qt6_libdir}/libQt6DataVisualizationQml.so.6*
%{_qt6_qmldir}/QtDataVisualization/

%files devel
%dir %{_qt6_libdir}/cmake/Qt6DataVisualization
%dir %{_qt6_libdir}/cmake/Qt6DataVisualizationPrivate
%dir %{_qt6_libdir}/cmake/Qt6DataVisualizationQml
%dir %{_qt6_libdir}/cmake/Qt6DataVisualizationQmlPrivate
%{_qt6_headerdir}/QtDataVisualization/
%{_qt6_headerdir}/QtDataVisualizationQml/
%{_qt6_libdir}/libQt6DataVisualization.so
%{_qt6_libdir}/libQt6DataVisualization.prl
%{_qt6_libdir}/libQt6DataVisualizationQml.prl
%{_qt6_libdir}/libQt6DataVisualizationQml.so
%{_qt6_libdir}/cmake/Qt6DataVisualization/*.cmake
%{_qt6_libdir}/cmake/Qt6DataVisualizationPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6DataVisualizationQml/*.cmake
%{_qt6_libdir}/cmake/Qt6DataVisualizationQmlPrivate/*.cmake
%{_qt6_archdatadir}/mkspecs/modules/*
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtDataVisualizationTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/pkgconfig/*.pc

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif


%changelog
* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Thu Aug 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Mon Mar 24 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0~rc-1
- 6.9.0 RC

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-2
- Move Software Bill of Materials from -devel

* Mon Dec 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
- 6.8.1

* Fri Oct 11 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Tue Oct 10 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-2
- Rebuild for qtbase private API version change

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Tue Apr 04 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- 6.4.2

* Wed Nov 23 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.1-1
- 6.4.1

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-1
- 6.3.1

* Wed Apr 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-1
- 6.3.0

* Fri Feb 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-2
- Enable s390x builds

* Mon Jan 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-1
- 6.2.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.2-1
- 6.2.2

* Fri Oct 29 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.1-1
- 6.2.1

* Thu Sep 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-1
- 6.2.0

* Mon Sep 27 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc2-1
- 6.2.0 - rc2

* Sat Sep 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-2
- Bump build for additional dependencies

* Fri Jun 11 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1
- 6.1.1

