 
%global qt_module qt5compat
 
%global examples 1
 
#global unstable 1
%if 0%{?unstable}
%global prerelease rc2
%endif
 
Summary: Qt6 - Qt 5 Compatibility Libraries
Name:    %{qt_module}
Version: 6.6.1
Release: 1%{?dist}
 
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)
 
%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif
 
# Upstream patches
 
# Upstreamable patches
 
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: qtbase-devel >= %{version}
BuildRequires: qtbase-private-devel
# qt6-qtdeclarative is required for QtGraphicalEffects
BuildRequires: qtdeclarative-devel
BuildRequires: qtshadertools-devel
BuildRequires: pkgconfig(xkbcommon)
%{?_qt:Requires: %{_qt}%{?_isa} = %{_qt_version}}
BuildRequires: libicu-devel
 
%description
%{summary}.
 
%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
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
%cmake_qt6 -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF}
 
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
%{_qt_libdir}/libQt6Core5Compat.so.6*
%{_qt_libdir}/qt6/qml/Qt5Compat/GraphicalEffects/*
 
%files devel
%dir %{_qt_libdir}/cmake/Qt6Core5Compat/
%{_qt_archdatadir}/mkspecs/modules/*.pri
%{_qt_headerdir}/QtCore5Compat/
%{_qt_libdir}/cmake/Qt6/FindWrapIconv.cmake
%{_qt_libdir}/cmake/Qt6BuildInternals/StandaloneTests/Qt5CompatTestsConfig.cmake
%{_qt_libdir}/cmake/Qt6Core5Compat/*.cmake
%{_qt_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt_libdir}/libQt6Core5Compat.prl
%{_qt_libdir}/libQt6Core5Compat.so
%{_qt_libdir}/pkgconfig/*.pc
%{_qt_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt_libdir}/qt6/modules/*.json
 
%if 0%{?examples}
%files examples
%{_qt_examplesdir}/
%endif
 
%changelog
* Tue Jan 02 2024 Sam Meluch <sammeluch@microsoft.com> - 6.6.1-1
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- License Verified

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
 
* Thu Jul 13 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-5
- Rebuilt for ICU 73.2
 
* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-4
- Rebuild for qtbase private API version change
 
* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Rebuild for qtbase private API version change
 
* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-2
- Rebuilt for ICU 73.2
 
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
 
* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 6.4.1-2
- Rebuild for ICU 72
 
* Wed Nov 23 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.1-1
- 6.4.1
 
* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0
 
* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 6.3.1-3
- Rebuilt for ICU 71.1
 
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
 
* Mon Jan 31 2022 Uwe Klotz <uwe.klotz@gmail.com> - 6.2.2-3
- Add missing unpackaged files for QtGraphicalEffects
 
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
 
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1
 
* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 6.1.0-2
- Rebuild for ICU 69
 
* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0
 
* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3
 
* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1
 
* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Wed Jan 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0
- 6.0.0
