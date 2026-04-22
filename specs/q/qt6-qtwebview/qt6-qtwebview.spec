# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global qt_module qtwebview

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

%global examples 1

Summary: Qt6 - WebView component
Name:    qt6-%{qt_module}
Version: 6.10.2
Release: 2%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

%{?qt6_qtwebengine_arches:ExclusiveArch: %{qt6_qtwebengine_arches}}

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel >= %{version}
BuildRequires: qt6-qtwebengine-devel
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1

%description
Qt WebView provides a way to display web content in a QML application
without necessarily including a full web browser stack by using native
APIs where it makes sense.

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
%license LICENSES/GPL* LICENSES/LGPL*
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%{_qt6_libdir}/libQt6WebView.so.6{,.*}
%{_qt6_libdir}/libQt6WebViewQuick.so.6{,.*}
%{_qt6_qmldir}/QtWebView/
%dir %{_qt6_plugindir}/webview/
%{_qt6_plugindir}/webview/libqtwebview_webengine.so

%files devel
%dir %{_qt6_headerdir}/QtWebView
%{_qt6_headerdir}/QtWebView/*
%dir %{_qt6_headerdir}/QtWebViewQuick
%{_qt6_headerdir}/QtWebViewQuick/*
%dir %{_qt6_libdir}/cmake/Qt6WebView
%dir %{_qt6_libdir}/cmake/Qt6WebViewPrivate
%dir %{_qt6_libdir}/cmake/Qt6WebViewQuick
%dir %{_qt6_libdir}/cmake/Qt6WebViewQuickPrivate
%{_qt6_libdir}/cmake/Qt6/FindWebView2.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWebViewTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/cmake/Qt6WebView/*.cmake
%{_qt6_libdir}/cmake/Qt6WebViewPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WebViewQuick/*.cmake
%{_qt6_libdir}/cmake/Qt6WebViewQuickPrivate/*.cmake
%{_qt6_libdir}/libQt6WebView.so
%{_qt6_libdir}/libQt6WebView.prl
%{_qt6_libdir}/libQt6WebViewQuick.so
%{_qt6_libdir}/libQt6WebViewQuick.prl
%{_qt6_libdir}/pkgconfig/Qt6WebView.pc
%{_qt6_libdir}/pkgconfig/Qt6WebViewQuick.pc
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_libdir}/qt6/metatypes/*.json
%{_qt6_libdir}/qt6/modules/*.json

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif


%changelog
* Tue Feb 10 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Mon Sep 29 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Fri Aug 29 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 05 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Wed Mar 26 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0~rc-1
- 6.9.0 RC

* Tue Feb 18 2025 Steve Cossette <farchord@gmail.com> - 6.8.2-2
- Fix package to use qtwebengine arches

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-2
- Install Software Bill of Materials

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
- 6.8.1

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Wed May 22 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Fri Oct 13 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Mon Jul 24 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-3
- Rebuilt for ICU 73.2

* Thu Jul 13 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-2
- Bump build for private API version change

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Wed Apr 05 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Mon Mar 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Wed Jan 25 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- 6.4.2
