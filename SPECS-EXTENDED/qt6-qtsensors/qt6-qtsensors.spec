Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global qt_module qtsensors

Summary:       Qt6 - Sensors component
Name:          qt6-%{qt_module}
Version:       6.5.7
Release:       1%{?dist}
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License:       LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:           http://www.qt.io/
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-opensource-src-%{version}.tar.xz#/%{qt_module}-everywhere-src-%{version}.tar.xz

# filter qml/plugin provides
%global __provides_exclude_from ^(%{_qt_archdatadir}/qml/.*\\.so|%{_qt_plugindir}/.*\\.so)$

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: qt-rpm-macros
BuildRequires: qtbase-devel >= %{version}
BuildRequires: qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qtdeclarative-devel >= %{version}
BuildRequires: qtsvg-devel >= %{version}

BuildRequires: pkgconfig(xkbcommon) >= 0.5.0
BuildRequires: openssl-devel

# provides a plugin that can use iio-sensor-proxy
Recommends:    iio-sensor-proxy

%description
The Qt Sensors API provides access to sensor hardware via QML and C++
interfaces.  The Qt Sensors API also provides a motion gesture recognition
API for devices.

%package devel
Summary:       Development files for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      qtbase-devel%{?_isa}
%description devel
%{summary}.

%if 0%{?examples}
%package examples
Summary:       Programming examples for %{name}
Requires:      %{name}%{?_isa} = %{version}-%{release}
# BuildRequires: qt6-qtsensors-devel >= %{version}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1


%build
%cmake_qt -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%ldconfig_scriptlets

%files
%license LICENSES/*
%{_qt_libdir}/libQt6Sensors.so.6*
%{_qt_plugindir}/sensors/

%files devel
%{_qt_headerdir}/QtSensors/
%{_qt_libdir}/libQt6Sensors.so
%{_qt_libdir}/libQt6Sensors.prl
%{_qt_libdir}/cmake/Qt6/FindSensorfw.cmake
%{_qt_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtSensorsTestsConfig.cmake
%dir %{_qt_libdir}/cmake/Qt6Sensors/
%{_qt_libdir}/cmake/Qt6Sensors/*.cmake
%{_qt_archdatadir}/mkspecs/modules/qt_lib_sensors*.pri
/usr/modules/*.json
%{_qt_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt_libdir}/pkgconfig/*.pc

%if 0%{?examples}
%files examples
%{_qt_examplesdir}/
%endif


%changelog
* Tue Dec 02 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 6.5.7-1
- Initial Azure Linux import from Fedora 37 (license: MIT)
- Upgrade to 6.5.7
- License Verified

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

* Wed May 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-2
- Enable examples

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

* Thu Sep 16 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc
