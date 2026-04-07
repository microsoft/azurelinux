# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global qt_module qt3d

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

Summary: Qt6 - Qt3D QML bindings and C++ APIs
Name:    qt6-%{qt_module}
Version: 6.10.2
Release: 1%{?dist}

%global examples 1

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif
Source1: qt3dcore-config-multilib_p.h

Patch0:  qt3d-assimp-fix-build.patch

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: qt6-rpm-macros >= %{version}
BuildRequires: qt6-qtbase-static >= %{version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtshadertools-devel
BuildRequires: qt6-qtimageformats
%if 0%{?fedora} && 0%{?fedora} >= 40
%global bundled_assimp 0
BuildRequires: pkgconfig(assimp) >= 3.3.1
%else
%global bundled_assimp 1
%endif
Requires: qt6-qtimageformats%{?_isa} >= %{version}

%description
Qt 3D provides functionality for near-realtime simulation systems with
support for 2D and 3D rendering in both Qt C++ and Qt Quick applications).

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
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
%define _lto_cflags %{nil}

%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF} \
  -DFEATURE_qt3d_system_assimp=%{?bundled_assimp:OFF}%{!?bundled_assimp:ON}

%cmake_build


%install
%cmake_install

%ifarch %{multilib_archs}
# multilib: qt3dcore-config_p.h
  mv %{buildroot}%{_qt6_headerdir}/Qt3DCore/%{version}/Qt3DCore/private/qt3dcore-config_p.h %{buildroot}%{_qt6_headerdir}/Qt3DCore/%{version}/Qt3DCore/private/qt3dcore-config-%{__isa_bits}_p.h
  install -p -m644 -D %{SOURCE1} %{buildroot}%{_qt6_headerdir}/Qt3DCore/%{version}/Qt3DCore/private/qt3dcore-config_p.h
%endif

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


%ldconfig_scriptlets

%files
%license LICENSES/GPL* LICENSES/LGPL*
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%{_qt6_libdir}/libQt63DAnimation.so.6*
%{_qt6_libdir}/libQt63DCore.so.6*
%{_qt6_libdir}/libQt63DExtras.so.6*
%{_qt6_libdir}/libQt63DInput.so.6*
%{_qt6_libdir}/libQt63DLogic.so.6*
%{_qt6_libdir}/libQt63DQuick.so.6*
%{_qt6_libdir}/libQt63DQuickAnimation.so.6*
%{_qt6_libdir}/libQt63DQuickExtras.so.6*
%{_qt6_libdir}/libQt63DQuickInput.so.6*
%{_qt6_libdir}/libQt63DQuickLogic.so.6*
%{_qt6_libdir}/libQt63DQuickRender.so.6*
%{_qt6_libdir}/libQt63DQuickScene2D.so.6*
%{_qt6_libdir}/libQt63DQuickScene3D.so.6*
%{_qt6_libdir}/libQt63DRender.so.6*
%{_qt6_plugindir}/geometryloaders/
%{_qt6_plugindir}/renderers/
%{_qt6_plugindir}/renderplugins/
%{_qt6_plugindir}/sceneparsers/
%{_qt6_qmldir}/Qt3D/
%{_qt6_qmldir}/QtQuick/Scene2D/
%{_qt6_qmldir}/QtQuick/Scene3D/

%files devel
%dir %{_qt6_libdir}/cmake/Qt63DAnimation
%dir %{_qt6_libdir}/cmake/Qt63DAnimationPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DCore/
%dir %{_qt6_libdir}/cmake/Qt63DCorePrivate/
%dir %{_qt6_libdir}/cmake/Qt63DExtras
%dir %{_qt6_libdir}/cmake/Qt63DExtrasPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DInput
%dir %{_qt6_libdir}/cmake/Qt63DInputPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DLogic
%dir %{_qt6_libdir}/cmake/Qt63DLogicPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DQuick
%dir %{_qt6_libdir}/cmake/Qt63DQuickAnimation
%dir %{_qt6_libdir}/cmake/Qt63DQuickAnimationPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DQuickExtras
%dir %{_qt6_libdir}/cmake/Qt63DQuickExtrasPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DQuickInput
%dir %{_qt6_libdir}/cmake/Qt63DQuickInputPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DQuickLogic/
%dir %{_qt6_libdir}/cmake/Qt63DQuickLogicPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DQuickPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DQuickRender/
%dir %{_qt6_libdir}/cmake/Qt63DQuickRenderPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DQuickScene2D
%dir %{_qt6_libdir}/cmake/Qt63DQuickScene2DPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DQuickScene3D
%dir %{_qt6_libdir}/cmake/Qt63DQuickScene3DPrivate/
%dir %{_qt6_libdir}/cmake/Qt63DRender/
%dir %{_qt6_libdir}/cmake/Qt63DRenderPrivate/
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_includedir}/Qt3DAnimation
%{_qt6_includedir}/Qt3DCore/
%{_qt6_includedir}/Qt3DExtras
%{_qt6_includedir}/Qt3DInput/
%{_qt6_includedir}/Qt3DLogic/
%{_qt6_includedir}/Qt3DQuick
%{_qt6_includedir}/Qt3DQuickAnimation
%{_qt6_includedir}/Qt3DQuickExtras
%{_qt6_includedir}/Qt3DQuickInput/
%{_qt6_includedir}/Qt3DQuickLogic
%{_qt6_includedir}/Qt3DQuickRender/
%{_qt6_includedir}/Qt3DQuickScene2D
%{_qt6_includedir}/Qt3DQuickScene3D
%{_qt6_includedir}/Qt3DRender/
%{_qt6_libdir}/cmake/Qt6/FindWrapQt3DAssimp.cmake
%{_qt6_libdir}/cmake/Qt63DAnimation/*.cmake
%{_qt6_libdir}/cmake/Qt63DAnimationPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DCore/*.cmake
%{_qt6_libdir}/cmake/Qt63DCorePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DExtras/*.cmake
%{_qt6_libdir}/cmake/Qt63DExtrasPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DInput/*.cmake
%{_qt6_libdir}/cmake/Qt63DInputPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DLogic/*.cmake
%{_qt6_libdir}/cmake/Qt63DLogicPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuick/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickAnimation/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickAnimationPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickExtras/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickExtrasPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickInput/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickInputPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickLogic/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickLogicPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickRender/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickRenderPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickScene2D/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickScene2DPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickScene3D/*.cmake
%{_qt6_libdir}/cmake/Qt63DQuickScene3DPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt63DRender/*.cmake
%{_qt6_libdir}/cmake/Qt63DRenderPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/Qt3DTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/libQt63DAnimation.prl
%{_qt6_libdir}/libQt63DAnimation.so
%{_qt6_libdir}/libQt63DCore.prl
%{_qt6_libdir}/libQt63DCore.so
%{_qt6_libdir}/libQt63DExtras.prl
%{_qt6_libdir}/libQt63DExtras.so
%{_qt6_libdir}/libQt63DInput.prl
%{_qt6_libdir}/libQt63DInput.so
%{_qt6_libdir}/libQt63DLogic.prl
%{_qt6_libdir}/libQt63DLogic.so
%{_qt6_libdir}/libQt63DQuick.prl
%{_qt6_libdir}/libQt63DQuick.so
%{_qt6_libdir}/libQt63DQuickAnimation.prl
%{_qt6_libdir}/libQt63DQuickAnimation.so
%{_qt6_libdir}/libQt63DQuickExtras.prl
%{_qt6_libdir}/libQt63DQuickExtras.so
%{_qt6_libdir}/libQt63DQuickInput.prl
%{_qt6_libdir}/libQt63DQuickInput.so
%{_qt6_libdir}/libQt63DQuickLogic.prl
%{_qt6_libdir}/libQt63DQuickLogic.so
%{_qt6_libdir}/libQt63DQuickRender.prl
%{_qt6_libdir}/libQt63DQuickRender.so
%{_qt6_libdir}/libQt63DQuickScene2D.prl
%{_qt6_libdir}/libQt63DQuickScene2D.so
%{_qt6_libdir}/libQt63DQuickScene3D.prl
%{_qt6_libdir}/libQt63DQuickScene3D.so
%{_qt6_libdir}/libQt63DRender.prl
%{_qt6_libdir}/libQt63DRender.so
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
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

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.1-2
- Use system assimp

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

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-1
- 6.0.0
