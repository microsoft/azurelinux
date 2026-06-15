%global qt_module qtconnectivity
 
#global unstable 1
%if 0%{?unstable}
%global prerelease rc2
%endif
 
%global examples 1
 
Summary:       Qt6 - Connectivity components
Name:          qt6-%{qt_module}
Version:       6.5.7
Vendor:        Microsoft Corporation
Distribution:  Azure Linux

%global majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

Release:       1%{?dist}
 
# See LICENSE.GPL3, respectively, for exception details
License:       LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:           http://qt.io
 
%if 0%{?unstable}
Source0:       https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0:       https://download.qt.io/official_releases/qt/%{majmin}/%{version}/src/submodules/%{qt_module}-everywhere-opensource-src-%{version}.tar.xz#/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

Patch0:        build_fix_quint128.patch
Patch1:        CVE-2025-23050-qtconnectivity-6.5.diff
 
# filter qml provides
%global __provides_exclude_from ^%{_qt_archdatadir}/qml/.*\\.so$
 
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: qt-rpm-macros
BuildRequires: qtbase-devel >= %{version}
BuildRequires: qtbase-private-devel >= %{version}
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qtdeclarative-devel >= %{version}
BuildRequires: pkgconfig(bluez)
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: openssl-devel
 
%description
%{summary}.
 
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
%license LICENSES/GPL* LICENSES/LGPL*
%{_qt_libexecdir}/sdpscanner
%{_qt_libdir}/libQt6Bluetooth.so.6*
%{_qt_libdir}/libQt6Nfc.so.6*
 
%files devel
%{_qt_headerdir}/QtBluetooth/
%{_qt_libdir}/libQt6Bluetooth.so
%{_qt_libdir}/libQt6Bluetooth.prl
%{_qt_headerdir}/QtNfc/
%{_qt_libdir}/libQt6Nfc.so
%{_qt_libdir}/libQt6Nfc.prl
%dir %{_qt_libdir}/cmake/Qt6Bluetooth/
%dir %{_qt_libdir}/cmake/Qt6Nfc/
%{_qt_libdir}/cmake/Qt6/FindBlueZ.cmake
%{_qt_libdir}/cmake/Qt6/FindPCSCLITE.cmake
%{_qt_libdir}/cmake/Qt6BuildInternals/StandaloneTests/*.cmake
%{_qt_libdir}/cmake/Qt6Bluetooth/*.cmake
%{_qt_libdir}/cmake/Qt6Nfc/*.cmake
%{_qt_archdatadir}/mkspecs/modules/qt_lib_bluetooth*.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_nfc*.pri
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
