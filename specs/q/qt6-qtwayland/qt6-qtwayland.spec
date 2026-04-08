# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global qt_module qtwayland

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

%global examples 1

Summary: Qt6 - Wayland platform support and QtCompositor module
Name:    qt6-%{qt_module}
Version: 6.10.2
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

# filter qml provides
%global __provides_exclude_from ^%{_qt6_archdatadir}/qml/.*\\.so$

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtbase-static
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
# For Adwaita decorations
BuildRequires: qt6-qtsvg-devel

BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-egl)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(libinput)
BuildRequires: pkgconfig(libdrm)

BuildRequires: libXext-devel

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
Requires: wayland-devel%{?_isa}
%description devel
%{summary}.

%package adwaita-decoration
Summary: Qt decoration plugin implementing Adwaita-like client-side decorations
Requires: %{name}%{?_isa} = %{version}-%{release}
Supplements: (qt6-qtbase and gnome-shell)
%description adwaita-decoration
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# BuildRequires: qt6-qtwayland-devel >= %{version}
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
%doc README
%license LICENSES/*
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%{_qt6_libdir}/libQt6WaylandCompositor.so.6*
%{_qt6_libdir}/libQt6WaylandCompositor.so.6*
%{_qt6_libdir}/libQt6WaylandCompositorIviapplication.so.6*
%{_qt6_libdir}/libQt6WaylandCompositorPresentationTime.so.6*
%{_qt6_libdir}/libQt6WaylandCompositorWLShell.so.6*
%{_qt6_libdir}/libQt6WaylandCompositorXdgShell.so.6*
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.so.6*
%{_qt6_plugindir}/wayland-graphics-integration-server
%{_qt6_plugindir}/wayland-shell-integration
%{_qt6_qmldir}/QtWayland/

%files devel
%{_qt6_headerdir}/QtWaylandCompositor/
%{_qt6_headerdir}/QtWaylandCompositorIviapplication/
%{_qt6_headerdir}/QtWaylandCompositorPresentationTime/
%{_qt6_headerdir}/QtWaylandCompositorWLShell/
%{_qt6_headerdir}/QtWaylandCompositorXdgShell/
%{_qt6_headerdir}/QtWaylandEglCompositorHwIntegration/
%{_qt6_libdir}/libQt6WaylandCompositor.so
%{_qt6_libdir}/libQt6WaylandCompositorIviapplication.prl
%{_qt6_libdir}/libQt6WaylandCompositorIviapplication.so
%{_qt6_libdir}/libQt6WaylandCompositorPresentationTime.prl
%{_qt6_libdir}/libQt6WaylandCompositorPresentationTime.so
%{_qt6_libdir}/libQt6WaylandCompositorWLShell.prl
%{_qt6_libdir}/libQt6WaylandCompositorWLShell.so
%{_qt6_libdir}/libQt6WaylandCompositorXdgShell.prl
%{_qt6_libdir}/libQt6WaylandCompositorXdgShell.so
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.so
%{_qt6_libdir}/libQt6WaylandCompositor.prl
%{_qt6_libdir}/libQt6WaylandEglCompositorHwIntegration.prl
%{_qt6_libdir}/cmake/Qt6WaylandCompositor/Qt6WaylandCompositorConfig*.cmake
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%dir %{_qt6_libdir}/cmake/Qt6WaylandClientFeaturesPrivate/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositor/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorIviapplication/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorIviapplicationPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorPresentationTime/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorPresentationTimePrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorWLShell/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorWLShellPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorXdgShell/
%dir %{_qt6_libdir}/cmake/Qt6WaylandCompositorXdgShellPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate/
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWaylandTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandClient/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandClientFeaturesPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositor/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorIviapplication/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorIviapplicationPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositorPresentationTime/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorPresentationTimePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositorPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositorWLShell/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorWLShellPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandCompositorXdgShell/
%{_qt6_libdir}/cmake/Qt6WaylandCompositorXdgShellPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate/
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc
%exclude %{_qt6_libdir}/cmake/Qt6WaylandClient/Qt6QWaylandAdwaitaDecoration*.cmake

%files adwaita-decoration
%{_qt6_plugindir}/wayland-decoration-client/libadwaita.so
%{_qt6_libdir}/cmake/Qt6WaylandClient/Qt6QWaylandAdwaitaDecoration*.cmake

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/wayland/
%endif

%changelog
* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Fri Oct 10 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-2
- Move Qt6WaylandAdwaitaDecoration cmake fiels to its subpackage

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Thu Aug 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-3
- Disable pointer warp support for now

* Thu Jun 26 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-2
- Add pointer warp support

* Mon Jun 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Tue Apr 22 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-3
- Backport upstream fix broken popups

* Mon Apr 14 2025 Pavel Solovev <daron439@gmail.com> - 6.9.0-2
- Require wayland-devel in the devel package

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

* Thu Nov 28 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-3
- Backport upstream fix for crash when unplugging graphics tablets

* Tue Oct 22 2024 Alessandro Astone <ales.astone@gmail.com> - 6.8.0-2
- Backport fix for rhbz#2318535

* Fri Oct 11 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Tue Aug 06 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-4
- Backport upstream fixes to avoid crashes on Plasma 6

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-2
- Backport - Client: Ensure that guessed popup parent has shell surface

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

* Thu Feb 08 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.1-5
- Backport upstream fix: Fix Qt::KeypadModifier for key events

* Wed Feb 07 2024 Jan Grulich <jgrulich@redhat.com>
- Backport upstream fix: disable threaded GL on desktop NVIDIA

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Wed Oct 11 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Wed Aug 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-3
- Use QAdwaitaDecorations by default

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

* Fri Jul 29 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-4
- Do not take decoration shadows into account when placing popups

* Tue Jul 26 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-3
- Keep toplevel windows in the top left corner of the screen

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

* Wed Jan 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0
- 6.0.0
