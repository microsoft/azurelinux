# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

Name:           aurorae
Summary:        Aurorae is a themeable window decoration for KWin
Version:        6.6.0
Release:        1%{?dist}
License:        GPL-2.0-or-later AND MIT AND CC0-1.0
URL:            https://invent.kde.org/plasma/%{name}

Source0:        https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{name}-%{version}.tar.xz
Source1:        https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{name}-%{version}.tar.xz.sig

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: gcc
BuildRequires: kf6-rpm-macros
BuildRequires: extra-cmake-modules

BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Quick)
BuildRequires: cmake(Qt6UiTools)
BuildRequires: cmake(Qt6Widgets)

BuildRequires: cmake(KF6ColorScheme)
BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6NewStuff)
BuildRequires: cmake(KF6Package)
BuildRequires: cmake(KF6Svg)
BuildRequires: cmake(KF6WindowSystem)

BuildRequires: cmake(KDecoration3)

# Account for being split out of kwin
Conflicts:     kwin < 6.3.90
Supplements:   kwin%{?_isa} >= %{version}

%description
Aurorae is a themeable window decoration for KWin.
It supports theme files consisting of several SVG files for
decoration and buttons. Themes can be installed and selected
directly in the configuration module of KWin decorations.
Please have a look at theme-description on how to write a theme file.

%package devel
Summary: Development libraries for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%prep
%autosetup -p1

%build
%cmake_kf6
%cmake_build

%install
%cmake_install
%find_lang %{name}

%files -f %{name}.lang
%doc README AUTHORS TODO
%license LICENSES/*
%{_kf6_qtplugindir}/org.kde.kdecoration3.kcm/kcm_auroraedecoration.so
%{_kf6_qtplugindir}/org.kde.kdecoration3/org.kde.kwin.aurorae.so
%{_kf6_qmldir}/org/kde/kwin/decoration/AppMenuButton.qml
%{_kf6_qmldir}/org/kde/kwin/decoration/ButtonGroup.qml
%{_kf6_qmldir}/org/kde/kwin/decoration/Decoration.qml
%{_kf6_qmldir}/org/kde/kwin/decoration/DecorationButton.qml
%{_kf6_qmldir}/org/kde/kwin/decoration/MenuButton.qml
%{_kf6_qmldir}/org/kde/kwin/decoration/libdecorationplugin.so
%{_kf6_qmldir}/org/kde/kwin/decoration/qmldir
%{_kf6_qmldir}/org/kde/kwin/decorations/plastik/libplastikplugin.so
%{_kf6_qmldir}/org/kde/kwin/decorations/plastik/qmldir
%{_libexecdir}/plasma-apply-aurorae
%{_kf6_datadir}/knsrcfiles/aurorae.knsrc
%{_kf6_datadir}/kwin/aurorae/
%{_kf6_datadir}/kwin/decorations/kwin4_decoration_qml_plastik/
%{_kf6_qtplugindir}/org.kde.kdecoration3/org.kde.kwin.aurorae.v2.so

%files devel
%{_kf6_libdir}/cmake/Aurorae/

%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Tue Jan 27 2026 Steve Cossette <farchord@gmail.com> - 6.5.91-1
- 6.5.91

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 farchord@gmail.com - 6.5.90-1
- 6.5.90

* Tue Jan 13 2026 farchord@gmail.com - 6.5.5-1
- 6.5.5

* Tue Dec 09 2025 Steve Cossette <farchord@gmail.com> - 6.5.4-1
- 6.5.4

* Tue Nov 18 2025 Steve Cossette <farchord@gmail.com> - 6.5.3-1
- 6.5.3

* Tue Nov 04 2025 Steve Cossette <farchord@gmail.com> - 6.5.2-1
- 6.5.2

* Tue Oct 28 2025 Steve Cossette <farchord@gmail.com> - 6.5.1-1
- 6.5.1

* Fri Oct 17 2025 Steve Cossette <farchord@gmail.com> - 6.5.0-1
- 6.5.0

* Thu Oct 02 2025 Steve Cossette <farchord@gmail.com> - 6.4.91-1
- 6.4.91

* Thu Sep 25 2025 Steve Cossette <farchord@gmail.com> - 6.4.90-1
- 6.4.90

* Tue Sep 16 2025 farchord@gmail.com - 6.4.5-1
- 6.4.5

* Sat Aug 16 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.4-2
- Drop i686 support (leaf package)

* Wed Aug 06 2025 Steve Cossette <farchord@gmail.com> - 6.4.4-1
- 6.4.4

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Steve Cossette <farchord@gmail.com> - 6.4.3-1
- 6.4.3

* Thu Jul 03 2025 Steve Cossette <farchord@gmail.com> - 6.4.2-1
- 6.4.2

* Tue Jun 24 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.1-1
- 6.4.1

* Wed Jun 18 2025 Neal Gompa <ngompa@fedoraproject.org> - 6.4.0-2
- Add Supplements: kwin to account for the split from kwin
- Add Conflicts: kwin < 6.3.90 to account for the split on upgrade

* Mon Jun 16 2025 Steve Cossette <farchord@gmail.com> - 6.4.0-1
- 6.4.0

* Sat May 31 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.91-2
- Add signature file

* Fri May 30 2025 Steve Cossette <farchord@gmail.com> - 6.3.91-1
- 6.3.91

* Thu May 15 2025 Steve Cossette <farchord@gmail.com> - 6.3.90-1
- Initial release
