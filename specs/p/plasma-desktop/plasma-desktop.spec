# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global scim 1
%if 0%{?rhel} && 0%{?rhel} > 7
%undefine scim
%endif

Name:    plasma-desktop
Summary: Plasma Desktop shell
Version: 6.6.0
Release: 2%{?dist}

License: BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND LGPL-3.0-only AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only)
URL:     https://invent.kde.org/plasma/%{name}

Source0: https://download.kde.org/%{stable_kf6}/plasma/%{maj_ver_kf6}.%{min_ver_kf6}.%{bug_ver_kf6}/%{name}-%{version}.tar.xz
Source1: https://download.kde.org/%{stable_kf6}/plasma/%{maj_ver_kf6}.%{min_ver_kf6}.%{bug_ver_kf6}/%{name}-%{version}.tar.xz.sig

# breeze fedora sddm theme components
# includes f40-based preview (better than breeze or nothing at least)
Source20:       breeze-fedora-0.3.tar.gz

## upstream patches

## downstream patches
# default kickoff/kicker favorites: +kwrite +konsole
# Patch100: plasma-desktop-5.90.0-default_favorites.patch

# Hide virtual keyboard indicator on sddm.
# Do not remove this as it breaks Fedora's QA policy
Patch101:       hide-virtual-keyboard-indicator-on-sddm.patch

## upstreamable patches

BuildRequires:  pkgconfig(libusb)
BuildRequires:  fontconfig-devel
BuildRequires:  libX11-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  pkgconfig(xkeyboard-config)

BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(Phonon4Qt6)
BuildRequires:  wayland-protocols-devel

BuildRequires:  ibus-devel
%if 0%{?scim}
BuildRequires:  scim-devel
%endif

BuildRequires:  kf6-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  cmake(KF6DocTools)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6GlobalAccel)
BuildRequires:  cmake(KF6NewStuff)
BuildRequires:  cmake(KF6NotifyConfig)
BuildRequires:  cmake(KF6Su)
BuildRequires:  cmake(KF6Attica)
BuildRequires:  cmake(KF6Wallet)
BuildRequires:  cmake(KF6Runner)
BuildRequires:  cmake(KF6Baloo)
BuildRequires:  cmake(KF6Declarative)
BuildRequires:  cmake(KF6People)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6Sonnet)
BuildRequires:  cmake(KF6Svg)
BuildRequires:  cmake(KF6ItemModels)
BuildRequires:  cmake(KF6KDED)
BuildRequires:  cmake(KF6KIO)

BuildRequires:  cmake(KSysGuard)
BuildRequires:  cmake(Plasma5Support)
BuildRequires:  kscreenlocker-devel
BuildRequires:  kwin-devel
BuildRequires:  plasma-breeze-qt6
BuildRequires:  plasma-workspace-devel

BuildRequires:  cmake(PlasmaActivities)
BuildRequires:  cmake(PlasmaActivitiesStats)
BuildRequires:  cmake(Plasma)

# For theming info
# /usr/share/backgrounds/default.{jxl,png}
BuildRequires:  desktop-backgrounds-compat


# Optional
%if 0%{?fedora}
BuildRequires:  cmake(AppStreamQt)
%endif
BuildRequires:  intltool
BuildRequires:  cmake(KAccounts6)
BuildRequires:  PackageKit-Qt6-devel
BuildRequires:  libcanberra-devel
BuildRequires:  boost-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  SDL2-devel
BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(libwacom)

BuildRequires:  xdg-user-dirs

# xorg-x11 doesn't have hw_server and disable for s390/s390x
%ifnarch s390 s390x
# KCM touchpad has been merged to plasma-desktop in 5.3
Provides:       kcm_touchpad = %{version}-%{release}
Obsoletes:      kcm_touchpad < 5.3.0
# for xserver-properties
BuildRequires:  xorg-x11-server-devel
Requires:       kf6-kded

# for kcm_keyboard
BuildRequires:  pkgconfig(libudev)
Requires:       iso-codes

# for kcm_input, kcm_touchpad
BuildRequires:  pkgconfig(xorg-evdev)
BuildRequires:  pkgconfig(xorg-libinput)

%endif

# kcm_users
Requires:       accountsservice
# kcm_clock
Requires:       qt6-qtlocation%{?_isa}

# Desktop
Requires:       plasma-workspace

# xdg-utils integration
Requires:       xdg-utils >= 1.2.0~
Requires:       kde-cli-tools

# Qt Integration (brings in Breeze)
Requires:       plasma-integration

# Install systemsettings, full set of KIO slaves and write() notifications
Requires:       plasma-systemsettings
Requires:       kio-extras
Requires:       kwrited

# Install KWin
Requires:       kwin

# kickoff -> edit applications (#1229393)
Requires:       kmenuedit

BuildRequires:  cmake(KF6Kirigami)
Requires:       kf6-kirigami%{?_isa}
BuildRequires:  cmake(KF6KirigamiAddons)
Requires:       kf6-kirigami-addons%{?_isa}
BuildRequires:  kf6-qqc2-desktop-style
Requires:       kf6-qqc2-desktop-style%{?_isa}
BuildRequires:  kpipewire
Requires:       kpipewire%{?_isa}
BuildRequires:  signon-plugin-oauth2-devel
Requires:       signon-plugin-oauth2%{?_isa}

# applets/kickoff/KickoffSingleton.qml unconditionally imports org.kde.plasma.plasma5support
Requires:       qt6qml(org.kde.plasma.plasma5support)

# for kimpanel-ibus-panel and kimpanel-ibus-panel-launcher
Recommends: ibus

# for drawing tablet support
Recommends: udev-hid-bpf-stable

# Virtual provides for plasma-workspace
Provides:       plasmashell(desktop) = %{version}-%{release}
Provides:       plasmashell = %{version}-%{release}

Obsoletes:      kde-workspace < 5.0.0-1

Obsoletes:      kactivities-workspace < 5.6.0
Provides:       kactivities-workspace = %{version}-%{release}

Obsoletes:      plasma-user-manager < 5.19.50
Provides:       plasma-user-manager = %{version}-%{release}

# kimpanel moved here from kdeplasma-addons-5.5.x
Conflicts:      kdeplasma-addons < 5.6.0

# kcm_activities.mo moved here (#1325724)
Conflicts:      kde-l10n < 15.12.3-4

# See https://pagure.io/fedora-kde/SIG/issue/455 for more information
Conflicts:      kde-settings < 39.1-7

%description
%{summary}.

%package        kimpanel-scim
Summary:        SCIM backend for kimpanel
Requires:       %{name} = %{version}-%{release}
%description    kimpanel-scim
A backend for the kimpanel panel icon for input methods using the SCIM input
method framework.

%package        doc
Summary:        Documentation and user manuals for %{name}
# when conflicting HTML docs were removed
Conflicts:      kcm_colors < 1:4.11.16-10
# when conflicting HTML docs were removed
Conflicts:      kde-runtime-docs < 17.08.3-6
# when made noarch
Obsoletes: plasma-desktop-doc < 5.3.1-2
BuildArch: noarch
%description    doc
%{summary}.


%package -n sddm-breeze
Summary:        SDDM breeze theme
Requires:       kde-settings-sddm
# upgrade path, when sddm-breeze was split out
Obsoletes: plasma-workspace < 5.3.2-8
# theme files from breeze plasma
Requires:       libplasma
# QML imports:
# QtQuick.VirtualKeyboard
Requires:       qt6-qtvirtualkeyboard
# QML imports:
# org.kde.plasma.breeze.components
# org.kde.plasma.*
# The dependency is with 3 version numbers due to upstream occasional respins containing an etra number (i.e: 6.0.5.1)
Requires:       plasma-workspace >= %{maj_ver_kf6}.%{min_ver_kf6}
# /usr/share/backgrounds/default.{jxl,png}
Requires:       desktop-backgrounds-compat
# for jxl support
Requires:       kf6-kimageformats
BuildArch: noarch

%description -n sddm-breeze
%{summary}.


%prep
%autosetup -a 20 -p1


%build
%cmake_kf6 \
%ifarch s390 s390x
    -DBUILD_KCM_MOUSE_X11=OFF \
    -DBUILD_KCM_TOUCHPAD_X11=OFF
%endif

%cmake_build


%install
%cmake_install
%find_lang %{name} --with-html --all-name

grep "%{_kf6_docdir}" %{name}.lang > %{name}-doc.lang
cat  %{name}.lang %{name}-doc.lang | sort | uniq -u > plasmadesktop6.lang

# make fedora-breeze sddm theme variant.
cp -alf %{buildroot}%{_datadir}/sddm/themes/breeze/ \
        %{buildroot}%{_datadir}/sddm/themes/01-breeze-fedora
# replace items
install -m644 -p breeze-fedora/* \
        %{buildroot}%{_datadir}/sddm/themes/01-breeze-fedora/
# Set Fedora background
bg_file_ext="jxl"
if [ -f "/usr/share/backgrounds/default.png" ]; then
bg_file_ext="png"
fi
sed -i -e "s|^background=.*$|background=/usr/share/backgrounds/default.${bg_file_ext}|g" %{buildroot}%{_datadir}/sddm/themes/01-breeze-fedora/theme.conf
# Set Fedora distro vendor logo
sed -i -e 's|^showlogo=.*$|showlogo=shown|g' %{buildroot}%{_datadir}/sddm/themes/01-breeze-fedora/theme.conf
sed -i -e 's|^logo=.*$|logo=%{_datadir}/pixmaps/fedora_whitelogo.svg|g' %{buildroot}%{_datadir}/sddm/themes/01-breeze-fedora/theme.conf


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/kcm_{keyboard,access,clock,splashscreen,landingpage,keys,smserver,desktoppaths,gamecontroller,activities,recentFiles,kded,krunnersettings,plasmasearch,qtquicksettings,tablet,touchscreen,workspace,baloofile,solid_actions,mouse,touchpad}.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/kcmspellchecking.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/org.kde.knetattach.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/org.kde.plasma.emojier.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/kaccess.desktop

%files -f plasmadesktop6.lang
%license LICENSES
%{_bindir}/kaccess
%{_bindir}/knetattach
%{_bindir}/solid-action-desktop-gen
%{_bindir}/plasma-emojier
%{_bindir}/tastenbrett
%{_bindir}/krunner-plugininstaller
%{_kf6_libexecdir}/kauth/kcmdatetimehelper
%{_libexecdir}/kimpanel-ibus-panel
%{_libexecdir}/kimpanel-ibus-panel-launcher
%{_kf6_qmldir}/org/kde/plasma/private
%{_kf6_qtplugindir}/attica_kde.so
%{_kf6_qtplugindir}/plasma/kcms/desktop/kcm_krunnersettings.so
%{_kf6_qtplugindir}/plasma/kcms/systemsettings/*.so
%{_kf6_qtplugindir}/plasma/kcms/systemsettings_qwidgets/*.so
%{_kf6_qtplugindir}/plasma/kcminit/kcm_touchpad_init.so
%{_kf6_plugindir}/kded/*.so
%{_kf6_plugindir}/krunner/krunner*.so
%{_kf6_qmldir}/org/kde/plasma/activityswitcher
%{_kf6_qmldir}/org/kde/plasma/emoji/
%{_kf6_qmldir}/org/kde/private/desktopcontainment/*
%{_kf6_datadir}/plasma/*
%{_kf6_datadir}/applications/kde-mimeapps.list
%ifnarch s390 s390x
# kcminput
%{_kf6_bindir}/kapplymousetheme
%{_kf6_bindir}/kcm-touchpad-list-devices
%endif
%{_kf6_datadir}/kcmmouse/
%{_kf6_qtplugindir}/plasma/kcminit/kcm_mouse_init.so
%{_datadir}/config.kcfg/*.kcfg
%{_datadir}/kglobalaccel/org.kde.plasma.emojier.desktop
%{_datadir}/kglobalaccel/org.kde.touchpadshortcuts.desktop
%{_datadir}/qlogging-categories6/*.categories
%{_kf6_datadir}/dbus-1/interfaces/org.kde.touchpad.xml
%{_kf6_datadir}/kcmkeys
%{_kf6_datadir}/knsrcfiles/
%{_kf6_datadir}/kcmsolidactions/
%{_kf6_datadir}/solid/devices/*.desktop
%{_kf6_datadir}/dbus-1/system.d/*.conf
%{_kf6_datadir}/knotifications6/*.notifyrc
%{_datadir}/icons/hicolor/*/*/*
%{_kf6_metainfodir}/*.xml
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmclock.policy
%{_sysconfdir}/xdg/autostart/*.desktop
%{_kf6_datadir}/accounts/providers/kde/*.provider
%{_kf6_datadir}/accounts/services/kde/*.service
%{_kf6_datadir}/kcm_recentFiles/workspace/settings/qml/recentFiles/ExcludedApplicationView.qml
# How to include these in the .lang file?
%{_kf6_datadir}/locale/sr/LC_SCRIPTS/kfontinst/kfontinst.js
%{_kf6_datadir}/locale/sr@ijekavian/LC_SCRIPTS/kfontinst/kfontinst.js
%{_kf6_datadir}/locale/sr@ijekavianlatin/LC_SCRIPTS/kfontinst/kfontinst.js
%{_kf6_datadir}/locale/sr@latin/LC_SCRIPTS/kfontinst/kfontinst.js
%{_userunitdir}/plasma-kaccess.service
%{_libdir}/libkglobalaccelmodel.so.6
%{_libdir}/libkglobalaccelmodel.so.%{version}
%{_kf6_qtplugindir}/plasma/applets/org.kde.*.so


%files -n sddm-breeze
%{_datadir}/sddm/themes/breeze/
%{_datadir}/sddm/themes/01-breeze-fedora/


%if 0%{?scim}
%files kimpanel-scim
%{_libexecdir}/kimpanel-scim-panel
%endif

%files doc -f %{name}-doc.lang


%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Mon Feb 09 2026 Adam Williamson <awilliam@redhat.com> - 6.5.91-2
- Require plasma5support (applets/kickoff/KickoffSingleton.qml needs it)

* Tue Jan 27 2026 Steve Cossette <farchord@gmail.com> - 6.5.91-1
- 6.5.91

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 farchord@gmail.com - 6.5.90-1
- 6.5.90

* Tue Jan 13 2026 farchord@gmail.com - 6.5.5-1
- 6.5.5

* Tue Dec 16 2025 Neal Gompa <ngompa@fedoraproject.org> - 6.5.4-2
- Add weak dependency on udev-hid-bpf-stable for tablet support

* Tue Dec 09 2025 Steve Cossette <farchord@gmail.com> - 6.5.4-1
- 6.5.4

* Thu Nov 27 2025 Steve Cossette <farchord@gmail.com> - 6.5.3-2
- Rebuild for possible issues with the Qt 6.10.1 update

* Tue Nov 18 2025 Steve Cossette <farchord@gmail.com> - 6.5.3-1
- 6.5.3

* Tue Nov 04 2025 Steve Cossette <farchord@gmail.com> - 6.5.2-1
- 6.5.2

* Tue Oct 28 2025 Steve Cossette <farchord@gmail.com> - 6.5.1-1
- 6.5.1

* Fri Oct 17 2025 Steve Cossette <farchord@gmail.com> - 6.5.0-1
- 6.5.0

* Sat Oct 04 2025 Steve Cossette <farchord@gmail.com> - 6.4.91-2
- Another rebuild for PackageKit-Qt Update

* Thu Oct 02 2025 Steve Cossette <farchord@gmail.com> - 6.4.91-1
- 6.4.91

* Tue Sep 30 2025 Jan Grulich <jgrulich@redhat.com> - 6.4.5-2
- Rebuild (qt6)

* Thu Sep 25 2025 Steve Cossette <farchord@gmail.com> - 6.4.90-1
- 6.4.90

* Tue Sep 16 2025 farchord@gmail.com - 6.4.5-1
- 6.4.5

* Wed Aug 06 2025 Steve Cossette <farchord@gmail.com> - 6.4.4-1
- 6.4.4

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Steve Cossette <farchord@gmail.com> - 6.4.3-1
- 6.4.3

* Sat Jul 05 2025 Timothée Ravier <tim@siosm.fr> - 6.4.2-2
- Require qt6-qtlocation for kcm_clock

* Thu Jul 03 2025 Steve Cossette <farchord@gmail.com> - 6.4.2-1
- 6.4.2

* Tue Jun 24 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.1-1
- 6.4.1

* Sun Jun 22 2025 Steve Cossette <farchord@gmail.com> - 6.4.0-2
- Fix an issue with icons not being clickable when specific alignment is set

* Mon Jun 16 2025 Steve Cossette <farchord@gmail.com> - 6.4.0-1
- 6.4.0

* Sat May 31 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.91-2
- Add signature file

* Fri May 30 2025 Steve Cossette <farchord@gmail.com> - 6.3.91-1
- 6.3.91

* Thu May 15 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.90-1
- 6.3.90

* Tue May 06 2025 Steve Cossette <farchord@gmail.com> - 6.3.5-1
- 6.3.5

* Mon Apr 14 2025 Jan Grulich <jgrulich@redhat.com> - 6.3.4-2
- Rebuild (qt6)

* Wed Apr 02 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.4-1
- 6.3.4

* Tue Mar 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.3.3-2
- Rebuild (qt6)

* Tue Mar 11 2025 Steve Cossette <farchord@gmail.com> - 6.3.3-1
- 6.3.3

* Tue Feb 25 2025 Steve Cossette <farchord@gmail.com> - 6.3.2-1
- 6.3.2

* Wed Feb 19 2025 Steve Cossette <farchord@gmail.com> - 6.3.1.1-1
- 6.3.1.1

* Tue Feb 18 2025 Steve Cossette <farchord@gmail.com> - 6.3.1-1
- 6.3.1

* Sat Feb 15 2025 Neal Gompa <ngompa@fedoraproject.org> - 6.3.0-2
- Adapt to backgrounds in JPEG-XL format

* Thu Feb 06 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.0-1
- 6.3.0

* Fri Jan 24 2025 Steve Cossette <farchord@gmail.com> - 6.2.91.1-1
- Update to 6.2.91.1

* Thu Jan 23 2025 Steve Cossette <farchord@gmail.com> - 6.2.91-1
- 6.2.91

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Steve Cossette <farchord@gmail.com> - 6.2.90-1
- Beta 6.2.90

* Tue Dec 31 2024 Steve Cossette <farchord@gmail.com> - 6.2.5-1
- 6.2.5

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 6.2.4-2
- Rebuild for ICU 76

* Tue Nov 26 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.4-1
- 6.2.4

* Tue Nov 05 2024 Steve Cossette <farchord@gmail.com> - 6.2.3-1
- 6.2.3

* Tue Oct 22 2024 Steve Cossette <farchord@gmail.com> - 6.2.2-1
- 6.2.2

* Tue Oct 15 2024 Steve Cossette <farchord@gmail.com> - 6.2.1-1
- 6.2.1

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 6.2.0-2
- Rebuild (qt6)

* Thu Oct 03 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Thu Sep 26 2024 Steve Cossette <farchord@gmail.com> - 6.1.90-2
- Fix kaccess crash on 6.1.90

* Thu Sep 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.90-1
- 6.1.90

* Tue Sep 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.5-1
- 6.1.5

* Fri Aug 09 2024 Steve Cossette <farchord@gmail.com> - 6.1.4-1
- 6.1.4

* Wed Jul 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.3-4
- rebuilt

* Wed Jul 24 2024 Steve Cossette <farchord@gmail.com> - 6.1.3-3
- Rebuild for change in plasma-workspace
- Experimental change to try to relax sddm-breeze version dependancy because of rebuild issues

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.3-1
- 6.1.3

* Wed Jul 03 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.2-1
- 6.1.2

* Tue Jun 25 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.1-1
- 6.1.1

* Tue Jun 18 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-3
- Rebuild to sort dependencies with plasma-workspace

* Tue Jun 18 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-2
- Soften dependency on plasma-workspace

* Thu Jun 13 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-1
- 6.1.0

* Fri May 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.90-1
- 6.0.90

* Wed May 22 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.5-1
- 6.0.5

* Tue Apr 16 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.4-1
- 6.0.4

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.0.3-2
- Rebuild (qt6)

* Tue Mar 26 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.3-1
- 6.0.3

* Tue Mar 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.2-1
- 6.0.2

* Wed Mar 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.1-1
- 6.0.1

* Tue Feb 27 2024 Marie Loise Nolden <loise@kde.org> - 6.0.0-2
- minor BR fixes

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 5.93.0-2
- Rebuild (qt6)

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.93.0-1
- 5.93.0

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 5.92.0-4
- Rebuild for ICU 74

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.92.0-1
- 5.92.0

* Tue Dec 26 2023 Alessandro Astone <ales.astone@gmail.com> - 5.91.0-2
- Re-enable optional dependency on KAccounts6
- Add missing QML dependency on org.kde.pipewire

* Thu Dec 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.91.0-1
- 5.91.0

* Tue Dec 19 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.90.0-2
- Refresh and apply default favorites patch

* Sun Dec 03 2023 Justin Zobel <justin.zobel@gmail.com> - 5.90.0-1
- Update to 5.90.0

* Wed Nov 29 2023 Jan Grulich <jgrulich@redhat.com> - 5.27.80-5
- Rebuild (qt6)

* Mon Nov 27 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-4
- Backport patch to fix desktop settings shortcut

* Sat Nov 25 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-3
- kio-extras is KF6

* Sat Nov 18 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-2
- Fix Plasma 6 runtime requirements

* Sat Nov 18 2023 Steve Cossette <farchord@gmail.com> - 5.27.80-1
- 5.27.80

* Tue Oct 24 2023 Steve Cossette <farchord@gmail.com> - 5.27.9-1
- 5.27.9

* Tue Sep 12 2023 justin.zobel@gmail.com - 5.27.8-1
- 5.27.8

* Tue Aug 01 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.7-1
- 5.27.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.27.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 25 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.6-1
- 5.27.6

* Wed May 10 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.5-1
- 5.27.5

* Tue Apr 04 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.4-1
- 5.27.4

* Tue Mar 14 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.3-1
- 5.27.3

* Tue Feb 28 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.2-1
- 5.27.2

* Tue Feb 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.1-1
- 5.27.1

* Tue Feb 14 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.27.0-2
- Rebuild against new sources

* Thu Feb 09 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Fri Jan 20 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.26.90-1
- 5.26.90

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.26.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Justin Zobel <justin@1707.io> - 5.26.5-1
- Update to 5.26.5

* Tue Nov 29 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.4-1
- 5.26.4

* Wed Nov 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.3-1
- 5.26.3

* Wed Oct 26 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.2-1
- 5.26.2

* Tue Oct 18 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.1-1
- 5.26.1

* Thu Oct 06 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.0-1
- 5.26.0

* Sat Sep 17 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.90-1
- 5.25.90

* Wed Sep 07 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.5-1
- 5.25.5

* Wed Aug 03 2022 Justin Zobel <justin@1707.io> - 5.25.4-1
- Update to 5.25.4

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.25.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.3-1
- 5.25.3

* Tue Jun 28 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.2-1
- 5.25.2

* Tue Jun 21 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.1-1
- 5.25.1

* Thu Jun 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.0-1
- 5.25.0

* Fri May 20 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.90-1
- 5.24.90

* Tue May 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.5-1
- 5.24.5

* Thu Mar 31 2022 Justin Zobel <justin@1707.io> - 5.24.4-1
- Update to 5.24.4

* Tue Mar 08 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.3-1
- 5.24.3

* Tue Feb 22 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.24.2-1
- 5.24.2

* Tue Feb 15 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.1-1
- 5.24.1

* Thu Feb 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.0-1
- 5.24.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.23.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.90-1
- 5.23.90

* Tue Jan 04 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.5-1
- 5.23.5

* Tue Dec 14 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.4-1
- 5.23.4

* Wed Nov 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.3-1
- 5.23.3

* Wed Oct 27 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.2.1-1
- 5.23.2.1

* Tue Oct 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.2-1
- 5.23.2

* Sat Oct 23 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.1-1
- 5.23.1

* Fri Oct 08 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.0-1
- 5.23.0

* Mon Sep 20 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-2
- Adjust license
- Adjust files section

* Fri Sep 17 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-1
- 5.22.90

* Tue Aug 31 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.5-1
- 5.22.5

* Tue Jul 27 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.4-1
- 5.22.4

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.22.3-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.3-1
- 5.22.3

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2.1-1
- 5.22.2.1

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2-1
- 5.22.2

* Tue Jun 15 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.1-1
- 5.22.1

* Sun Jun 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.0-1
- 5.22.0

* Thu May 20 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-3
- pull in some upstream fixes

* Sun May 16 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-2
- s/kf5-ksysguard/libksysguard/

* Fri May 14 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-1
- 5.21.90

* Tue May 04 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.5-1
- 5.21.5

* Tue Apr 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.4-1
- 5.21.4

* Tue Mar 16 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.3-1
- 5.21.3

* Tue Mar 02 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.2-1
- 5.21.2

* Tue Feb 23 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.1-1
- 5.21.1

* Mon Feb 15 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.0-2
- Tarball respin

* Thu Feb 11 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.0-1
- 5.21.0

* Thu Jan 28 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.90-3
- ibus-ui-emojier-plasma: +Recommends: ibus

* Tue Jan 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.90-2
- for ibus-ui-emojier-plasma: +Recommends: ibus-uniemoji
- fix URL

* Thu Jan 21 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.90-1
- 5.20.90 (beta)

* Tue Jan  5 16:03:32 CET 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.5-1
- 5.20.5

* Thu Dec 31 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.20.4-2
- Requires: accountsservice (kde#430916)

* Tue Dec  1 09:42:59 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.4-1
- 5.20.4

* Wed Nov 11 08:22:41 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.3-1
- 5.20.3

* Tue Oct 27 14:23:44 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.2-1
- 5.20.2

* Tue Oct 20 15:29:34 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.1-1
- 5.20.1

* Sun Oct 11 19:50:04 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.0-1
- 5.20.0

* Fri Sep 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.90-1
- 5.19.90

* Tue Sep 01 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.5-1
- 5.19.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.4-1
- 5.19.4

* Tue Jul 07 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.3-1
- 5.19.3

* Tue Jun 23 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.2-1
- 5.19.2

* Wed Jun 17 2020 Martin Kyral <martin.kyral@gmail.com> - 5.19.1-1
- 5.19.1

* Wed Jun 10 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.19.0-2
- adjust synaptics hacks (for rhel8), bump kf5 dep

* Tue Jun 9 2020 Martin Kyral <martin.kyral@gmail.com> - 5.19.0-1
- 5.19.0

* Fri May 15 2020 Martin Kyral <martin.kyral@gmail.com> - 5.18.90-1
- 5.18.90

* Tue May 05 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.5-1
- 5.18.5

* Sat May 02 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.4.1-2
- use bundled synaptics header, if needed
- fix feature macro logic (defined as 1 on, undefined off)
- minor cleanups

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.4.1-1
- 5.18.4.1

* Tue Mar 31 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.4-1
- 5.18.4

* Tue Mar 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.3-1
- 5.18.3

* Tue Feb 25 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.2-1
- 5.18.2

* Tue Feb 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.1-1
- 5.18.1

* Mon Feb 17 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.0-2
- pull in upstream kcm_fonts fix

* Tue Feb 11 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.0-1
- 5.18.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.17.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Jan Grulich <jgrulich@redhat.com> - 5.17.90-1
- 5.17.90

* Wed Jan 08 2020 Jan Grulich <jgrulich@redhat.com> - 5.17.5-1
- 5.17.5

* Fri Dec 27 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.17.4-2
- pull in upstream pager fix

* Thu Dec 05 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.4-1
- 5.17.4

* Wed Nov 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.17.3-1
- 5.17.3

* Wed Oct 30 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.2-1
- 5.17.2

* Wed Oct 23 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.1-1
- 5.17.1

* Wed Oct 16 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.0-2
- Updated tarball

* Thu Oct 10 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.0-1
- 5.17.0

* Fri Sep 20 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.90-1
- 5.16.90

* Fri Sep 06 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.5-1
- 5.16.5

* Tue Jul 30 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.4-1
- 5.16.4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.3-1
- 5.16.3

* Wed Jun 26 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.2-1
- 5.16.2

* Tue Jun 18 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.16.1-1
- 5.16.1

* Tue Jun 11 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.0-1
- 5.16.0

* Mon May 20 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.90.1-1
- 5.15.90.1

* Thu May 16 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.90-1
- 5.15.90

* Thu May 09 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.5-1
- 5.15.5

* Wed Apr 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.4-1
- 5.15.4

* Wed Mar 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.3.2-1
- 5.15.3.2
- tarball respun to remove docs causing build issues with KDocTools < 5.57

* Tue Mar 12 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.3-1
- 5.15.3

* Tue Feb 26 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.2-1
- 5.15.2

* Tue Feb 19 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.1-1
- 5.15.1

* Wed Feb 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.0-1
- 5.15.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 20 2019 Martin Kyral <martin.kyral@gmail.com> - 5.14.90-1
- 5.14.90

* Wed Nov 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.4-2
- pull in upstream taskmanager fix

* Tue Nov 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.4-1
- 5.14.4

* Thu Nov 08 2018 Martin Kyral <martin.kyral@gmail.com> - 5.14.3-1
- 5.14.3

* Wed Oct 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Tue Oct 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.1-1
- 5.14.1

* Fri Oct 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.0-1
- 5.14.0

* Fri Sep 14 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.90-1
- 5.13.90

* Tue Sep 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.5-1
- 5.13.5

* Thu Aug 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.4-1
- 5.13.4

* Thu Jul 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.3-4
- Requires: qqc2-desktop-style

* Fri Jul 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.3-3
- use %%_kf5_qmldir (more)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.3-1
- 5.13.3

* Mon Jul 09 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.2-1
- 5.13.2

* Wed Jun 20 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.1.1-1
- 5.13.1.1

* Tue Jun 19 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.1-1
- 5.13.1

* Sat Jun 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.0-1
- 5.13.0

* Thu May 31 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.90.1-1
- 5.12.90.1
- kickoff crashes when click on categories (#1584515)

* Fri May 18 2018 Martin Kyral <martin.kyral@gmail.com> - 5.12.90-1
- 5.12.90

* Tue May 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-1
- 5.12.5

* Tue Mar 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-1
- 5.12.4

* Fri Mar 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-2
- BR: AppStreamQt libudev xorg-input

* Tue Mar 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-1
- 5.12.3

* Fri Mar 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.2-2
- -doc: drop Obsoletes: kde-runtime-docs (#1550857,#1199720)
- bump min qt5/kf5 dep
- use %%make_build %%ldconfig_scriptlets
- drop konq4 support (last used f25)

* Wed Feb 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.2-1
- 5.12.2

* Tue Feb 13 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.1-1
- 5.12.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.0-1
- 5.12.0

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.11.95-2
- Remove obsolete scriptlets

* Mon Jan 15 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.95-1
- 5.11.95

* Tue Jan 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.5-1
- 5.11.5

* Thu Nov 30 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.4-1
- 5.11.4

* Wed Nov 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Wed Oct 25 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.2-1
- 5.11.2

* Tue Oct 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Wed Oct 11 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.0-1
- 5.11.0

* Thu Aug 24 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.5-1
- 5.10.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.4-1
- 5.10.4

* Tue Jun 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.3-1
- 5.10.3

* Thu Jun 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.2-1
- 5.10.2

* Tue Jun 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1

* Wed May 31 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Wed Apr 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.5-1
- 5.9.5, cleanup, BR: plasma-breeze, use %%find_lang more

* Fri Apr 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.4-2
- pull in upstream fixes, update URL

* Thu Mar 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.3-2
- rebuild

* Wed Mar 01 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Sat Feb 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-2
- Requires: kf5-plasma >= %%_kf5_version

* Tue Feb 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-1
- 5.8.6

* Mon Feb 13 2017 Than Ngo <than@redhat.com> - 5.8.5-4
- backport upstream to security issue
  honor the setting for prompting when executing executable files on the desktop
- fixed error: placeholders is not a namespace-name with gcc7

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-2
- filter qml/plugin provides, drop unused PK patch/support

* Wed Dec 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-1
- 5.8.5

* Tue Nov 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.4-1
- 5.8.4

* Thu Nov 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.3-2
- adjust default_favorites.patch for namespaced apper

* Tue Nov 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.3-1
- 5.8.3

* Tue Oct 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-1
- 5.8.2

* Tue Oct 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-1
- 5.8.1

* Fri Oct 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-4
- default_favorites.patch: use preferred://browser again

* Fri Oct 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-3
- drop re-enabling kicker PackageKit integration, it's racy (#1382360)

* Wed Oct 05 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-2
- move kimpanel-scim-panel to a -kimpanel-scim subpackage (#1381420)

* Thu Sep 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-1
- 5.8.0

* Thu Sep 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.95-1
- 5.7.95

* Tue Sep 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.5-1
- 5.7.5

* Tue Aug 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.4-1
- 5.7.4

* Tue Aug 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.3-1
- 5.7.3, drop f22 support

* Tue Jul 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.2-1
- 5.7.2

* Tue Jul 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-1
- 5.7.1

* Thu Jun 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-1
- 5.7.0

* Sat Jun 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.95-1
- 5.6.95

* Tue Jun 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.5-1
- 5.6.5

* Thu May 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-2
- fix kickoff kcm_useraccount => user_manager (kde#363528)
- backport 5.6 branch fixes

* Sat May 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-1
- 5.6.4

* Sat Apr 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-2
- kickoff applet still use KF5::ActivitiesExperimentalStats (kde#361952)

* Tue Apr 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-1
- 5.6.3

* Mon Apr 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-3
- muon-discover => plasma-discover (f24+)

* Mon Apr 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-2
- Conflicts: kde-l10n < 15.12.3-4 (#1325724)

* Sat Apr 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-1
- 5.6.2

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-2
- BR: ibus-devel scim-devel

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-1
- 5.6.1

* Mon Mar 28 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.5-5
- upstream fixes for: No 'favorites' in F24 KDE menu (#1320395,kde#357029)

* Fri Mar 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.5-4
- favorites: cleanup, no backups, f22+ fix firefox/konsole/discover, f22 fix konq/konsole/discover

* Wed Mar 23 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.5-3
- No 'favorites' in F24 KDE menu (#1320395,kde#357029)

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.5-2
- drop Requires: kde-style-breeze (f23+)

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Mon Feb 29 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-4
- (backport) wrong breeze icons used ... in taskmanager (#359387)

* Fri Feb 26 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-3
- fix kickoff "right click => remove app" packagekit integration (#359837)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Sat Jan 09 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.3-3
- pull in some upstream patches, simplify/consolidate s390 blocks

* Sat Jan 09 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.3-2
- Fix font preview (#1208229, kde#336089)

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.2-2
- update URL, old sources

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Wed Dec 16 2015 Than Ngo <than@redhat.com> - 5.5.0-6
- add workaround for "virtual memory exhausted: Cannot allocate memory" on s390
- exclude touchpad for s390/s390x

* Tue Dec 15 2015 Than Ngo <than@redhat.com> - 5.5.0-5
- fix build failure on s390/s390x

* Wed Dec 09 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-4
- omit env hack, rename plasma update script instead

* Tue Dec 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- force plasma's obsolete_kickoffrc.js to run again

* Tue Dec 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- backport favorites migration fix (#1289709)

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-5
- Recommends: muon-discover (#1224421)

* Mon Oct 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-4
- revert default_favorites.patch back to apper

* Fri Oct 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-3
- default_favorites.patch: -apper, +muon-discover

* Sun Oct 04 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-2
- Recommends: muon-discover
- consistently use %%{majmin_ver} macro for plasma5-related dependencies

* Fri Oct 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2, use %%license, .spec cosmetics

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-7
- relax some deps %%{version} => %%{majmin_ver} to ease bootstrapping

* Mon Sep 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-6
- re-fix font management, kauth_helper paths (#1208229, kde#353215)

* Mon Sep 21 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-5
- restore f22 default favorites

* Fri Sep 18 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-4
- conditionally apply C.UTF-8 workaround only for < f24 (#1250238)

* Sat Sep 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-3
- tighten build deps (simimlar to plasma-workspace)

* Fri Sep 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- make kio-extras unversioned (it's in kde-apps releases now)

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-4
- Wrong C.UTF-8 locale (#1250238)

* Fri Sep 04 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-3
- make plasma-related runtime deps versioned

* Tue Sep 01 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-2
- Try rebuild against new Baloo

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 5.3.2-5
- rebuild for Boost 1.58

* Tue Jul 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-4
- BR: pkgconfig(xkeyboard-config)

* Mon Jul 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-3
- Switch to Next Keyboard Layout shortcut restores after OS restarting (#1234082)

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-2
- pull in upstream fix for kcm_touchpad: No touchpad found (#1199825)

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Tue Jun 23 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-7
- kcm_touchpad: No touchpad found (#1199825)

* Wed Jun 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-6
- kcm_phonon does not display all HDMI audio ports (#1232903)

* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-5
- backport trashcan applet fix (#1231972,kde#349207)

* Mon Jun 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-4
- backport "Fix-dropping-files-onto-the-desktop-containment"
- BR: kf5-kglobalaccel-devel

* Mon Jun 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-3
- Requires: kmenuedit, instead of Recommends which doesn't seem to work reliably yet (#1229393)

* Tue Jun 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.1-2
- use %%{kf5_kinit_requires}
- -doc: noarch, %%lang'ify
- Provides: plasmashell

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Thu May 21 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-6
- default to folder containment (#1220862)

* Fri May 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-5
- Recommends: kmenuedit

* Sun May 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-4
- (re)fix fontinst service paths (#1208229)

* Wed Apr 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-3
- Provides plasmashell(desktop) (#1215691)

* Tue Apr 28 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-2
- Provides/Obsoletes kcm_touchpad (#1216897)

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Thu Apr 23 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Thu Apr 23 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.2-5
- fix fontinst service paths harder (#1208229)
- Konqueror "favorite" opens as a file manager (#1209169)

* Thu Apr 02 2015 Daniel Vrátil <dvratil@redhat.com> 5.2.2-4
- fix fontinst service paths (rhbz#1208229)

* Mon Mar 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-3
- own /usr/share/plasma/shells/org.kde.plasma.desktop/updates

* Fri Mar 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-2
- -doc: Conflicts: kcm_colors < 1:4.11.16-10 (drop conflicts in main pkg)

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Wed Mar 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-6
- adjust default kickoff favorites: +konsole +apper

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-5
- .spec cleanup
- pull in upstream fixes, particularly...
- Top level "tabs" disappears in Kickoff (kde#343524)

* Sat Mar 07 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-4
- -doc: Obsoletes: kde-runtime-docs (#1199720)
- %%find_lang: drop --with-kde, we want handbooks in -doc instead

* Fri Mar 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-3
- Does not obsolete kcm_colors anymore (KDE 4 version is co-installable now)

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-5
- Requires: iso-codes (for kcm_keyboard)

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-4
- Copy konqsidebartng to /usr/share/kde4/apps so that KDE4 Konqueror can find it

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-3
- Workaround broken DBus service file generated by CMake

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- Requires: breeze, systemsettings, kwin (for full Plasma experience)

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- Obsoletes/Provides kcm_colors

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Wed Jan 07 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.2-3
- Omit "5" from pkg summary
  Add icon cache scriptlets
  Validate application .desktop files
  Fixed license

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140515git532fc47
- Initial version of kde5-plasma-desktop
