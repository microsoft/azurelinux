# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global        qt_module qtgraphs

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

%global examples 1

Summary: The Qt Graphs module enables you to visualize data in 3D
Name:    qt6-%{qt_module}
Version: 6.10.2
Release: 2%{?dist}

License: BSD-3-Clause AND GFDL-1.3-no-invariants-only AND GPL-3.0-only
URL:     https://doc.qt.io/qt-6/qtgraphs-index.html
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build

BuildRequires: cmake(Qt6BuildInternals)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6QuickTest)
BuildRequires: cmake(Qt6QuickWidgets)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6Quick3D)
BuildRequires: qt6-qtbase-private-devel

%description
The Qt Graphs module enables you to visualize data in 3D as bar,
scatter, and surface graphs. It's especially useful for visualizing
depth maps and large quantities of rapidly changing data, such as
data received from multiple sensors. The look and feel of graphs
can be customized by using themes or by adding custom items and labels.

Qt Graphs is built on Qt 6 and Qt Quick 3D to take advantage of
hardware acceleration and Qt Quick.

%package devel
Summary:       Development Files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary:       Programming examples for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}
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

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%files
%license LICENSES/BSD-3-Clause.txt LICENSES/GFDL*.txt LICENSES/GPL-*.txt
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%{_qt6_libdir}/libQt6Graphs.so.6*
%{_qt6_libdir}/libQt6GraphsWidgets.so.6*
%{_qt6_qmldir}/QtGraphs

%files devel
%{_qt6_headerdir}/QtGraphs
%{_qt6_headerdir}/QtGraphsWidgets
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtGraphsTestsConfig.cmake
%dir %{_qt6_libdir}/cmake/Qt6Graphs
%{_qt6_libdir}/cmake/Qt6Graphs/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6GraphsPrivate
%{_qt6_libdir}/cmake/Qt6GraphsPrivate/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6GraphsWidgets
%{_qt6_libdir}/cmake/Qt6GraphsWidgets/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6GraphsWidgetsPrivate
%{_qt6_libdir}/cmake/Qt6GraphsWidgetsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6Graphsplugin*.cmake
%{_qt6_libdir}/libQt6Graphs.so
%{_qt6_libdir}/pkgconfig/Qt6Graphs*.pc
%{_qt6_libdir}/libQt6Graphs.prl
%{_qt6_libdir}/libQt6GraphsWidgets.prl
%{_qt6_libdir}/libQt6GraphsWidgets.so
%{_qt6_libdir}/qt6/mkspecs/modules/qt_lib_graphs*.pri
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json


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

* Thu Nov 28 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
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

* Fri Jan 26 2024 Steve Cossette <farchord@gmail.com> - 6.6.1-1
- Initital release of qtgraphs
