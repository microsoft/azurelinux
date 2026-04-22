# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond kf6_pim 1

Name:    plasma-workspace
Summary: Plasma workspace, applications and applets
Version: 6.6.0
Release: 2%{?dist}

# Automatically converted from old format: BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND LGPL-3.0-only AND LGPL-3.0-or-later AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only) AND MIT - review is highly recommended.
License: BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND LGPL-3.0-only AND LGPL-3.0-or-later AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only) AND MIT
URL:     https://invent.kde.org/plasma/%{name}

Source0: https://download.kde.org/%{stable_kf6}/plasma/%{maj_ver_kf6}.%{min_ver_kf6}.%{bug_ver_kf6}/%{name}-%{version}.tar.xz
Source1: https://download.kde.org/%{stable_kf6}/plasma/%{maj_ver_kf6}.%{min_ver_kf6}.%{bug_ver_kf6}/%{name}-%{version}.tar.xz.sig

Source11:       startkderc
Source15:       fedora-lookandfeel.json
Source16:       fedoradark-lookandfeel.json
Source17:       fedoralight-lookandfeel.json

Source100:      kde
Source101:      kde-fingerprint
Source102:      kde-smartcard


## systemd user service dependencies
## (debating whether these be owned here or somewhere better...
## in the repective pkgs themselves? -- rdieter)
Source40:       ssh-agent.conf
## To be dropped when EL10 and F42 is no longer supported
## Or if spice-vd-agent >= 0.23.0 is shipped in any existing release
Source41:       spice-vdagent.conf

## upstream patches

## upstreamable Patches

## downstream Patches
# default to enable open terminal action
Patch106:       plasma-workspace-5.27.80-enable-open-terminal-action.patch
# default to enable the lock/logout actions
Patch107:       plasma-workspace-5.27.80-enable-lock-logout-action.patch

# udev
BuildRequires:  zlib-devel
BuildRequires:  libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXau-devel
BuildRequires:  libXdmcp-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXtst-devel
BuildRequires:  libXft-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-devel
BuildRequires:  glib2-devel
BuildRequires:  fontconfig-devel
BuildRequires:  boost-devel
BuildRequires:  pkgconfig(libusb)
BuildRequires:  libbsd-devel
BuildRequires:  pam-devel
BuildRequires:  libxcrypt-devel
BuildRequires:  lm_sensors-devel
BuildRequires:  pciutils-devel
BuildRequires:  pipewire-devel
BuildRequires:  unity-gtk3-module
Requires:       unity-gtk3-module
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
%endif
BuildRequires:  libqalculate-devel
BuildRequires:  libicu-devel

BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel

BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  cmake(Qt6Location)
BuildRequires:  cmake(Qt6Positioning)
BuildRequires:  cmake(Qt6ShaderTools)
BuildRequires:  polkit-qt6-1-devel
BuildRequires:  libcanberra-devel
BuildRequires:  kf6-rpm-macros
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(libudev)
BuildRequires:  systemd

BuildRequires:  extra-cmake-modules
BuildRequires:  cmake(KF6Baloo)
BuildRequires:  cmake(KF6Archive)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6Declarative)
BuildRequires:  cmake(KF6Su)
BuildRequires:  cmake(KF6DocTools)
BuildRequires:  cmake(KF6GlobalAccel)
BuildRequires:  cmake(KF6GuiAddons)
BuildRequires:  cmake(KF6IdleTime)
BuildRequires:  cmake(KF6ItemModels)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  cmake(KF6NewStuff)
BuildRequires:  cmake(KF6Notifications)
BuildRequires:  cmake(KF6NotifyConfig)
BuildRequires:  cmake(KF6People)
BuildRequires:  cmake(KF6Runner)
BuildRequires:  cmake(KF6TextEditor)
BuildRequires:  cmake(KF6TextWidgets)
BuildRequires:  cmake(KF6UnitConversion)
BuildRequires:  cmake(KF6Wallet)
BuildRequires:  cmake(KF6ThreadWeaver)
BuildRequires:  cmake(KF6Kirigami)
BuildRequires:  cmake(KF6KirigamiAddons)
BuildRequires:  cmake(KF6QuickCharts)
BuildRequires:  cmake(KF6StatusNotifierItem)
BuildRequires:  cmake(KF6Svg)
BuildRequires:  cmake(KF6KDED)
BuildRequires:  cmake(KF6NetworkManagerQt)
BuildRequires:  cmake(KF6Screen)
BuildRequires:  cmake(KF6Holidays)
BuildRequires:  cmake(KF6Prison)
BuildRequires:  cmake(KF6UserFeedback)
BuildRequires:  cmake(KNightTime)
BuildRequires:  cmake(Plasma5Support)

BuildRequires:  wayland-devel >= 1.3.0
BuildRequires:  libksysguard-devel
BuildRequires:  kscreenlocker-devel
BuildRequires:  kwin-devel
BuildRequires:  layer-shell-qt-devel
BuildRequires:  cmake(Phonon4Qt6)
BuildRequires:  PackageKit-Qt6-devel
BuildRequires:  cmake(KExiv2Qt6)

BuildRequires:  cmake(Plasma)
BuildRequires:  cmake(KWayland)
BuildRequires:  cmake(PlasmaActivities)
BuildRequires:  cmake(PlasmaActivitiesStats)

# workaround for
#   The imported target "Qt6::XkbCommonSupport" references the file
#     "/usr/lib64/libQt6XkbCommonSupport.a"
#  but this file does not exist.
BuildRequires:  qt6-qtbase-static
BuildRequires:  cmake(Qt6Core5Compat)
BuildRequires:  cmake(QCoro6)
BuildRequires:  pkgconfig(libxcrypt)

BuildRequires:  wayland-protocols-devel
BuildRequires:  plasma-wayland-protocols-devel
BuildRequires:  plasma-breeze-devel >= %{majmin_ver_kf6}

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils

BuildRequires:  cmake(AppStreamQt) >= 1.0.0

# when kded_desktopnotifier.so moved here
Conflicts:      kio-extras < 5.4.0

Recommends:     plasma-welcome

Recommends:     %{name}-geolocation = %{version}-%{release}
Suggests:       imsettings-qt

Requires:       %{name}-common = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       libkworkspace6%{?_isa} = %{version}-%{release}
# for selinux settings
Requires:       (policycoreutils if selinux-policy)

Requires:       kactivitymanagerd%{?_isa}
Requires:       ksystemstats%{?_isa}
Requires:       kf6-baloo
Requires:       kf6-kded
Requires:       kf6-kdoctools
Requires:       kf6-kglobalaccel
Requires:       kf6-kquickcharts
Requires:       kf6-kirigami
Requires:       kf6-kirigami-addons
BuildRequires:  kf6-kirigami-addons
Requires:       kio-extras
BuildRequires:  kio-extras
Requires:       kio-fuse
BuildRequires:  kio-fuse

# The new volume control for PulseAudio
Recommends:       plasma-pa

# Without the platformtheme plugins we get broken fonts
Requires:       kf6-frameworkintegration

# For krunner
Recommends:       plasma-milou

# https://pagure.io/fedora-kde/SIG/issue/303
Recommends: kde-inotify-survey

# https://pagure.io/fedora-kde/SIG/issue/354
Recommends: audiocd-kio

# For a11y
Recommends: orca

# powerdevil has a versioned dep on libkworkspace6, so (may?)
# need to avoid this dep when bootstrapping
%if ! 0%{?bootstrap}
# Power management
Requires:       powerdevil
%endif

Requires:       dbus
# dbus-update-activation-environment
Requires:       dbus-tools

# Required for applications to show in kickoff and on task manager
Requires:       redhat-menus

# startkde (TODO: review, this is no longer a shell script)
Requires:       coreutils
Requires:       socat
Requires:       xmessage
Requires:       qt6-qttools

# kconf_update
Requires:       /usr/bin/qtpaths-qt6

Requires:       xrdb xprop

Requires:       kde-settings-plasma

# Default look-and-feel theme
Requires:       plasma-lookandfeel-fedora = %{version}-%{release}

Requires:       systemd

# Default sound theme
Requires:       ocean-sound-theme

# PolicyKit authentication agent
Requires:        polkit-kde

# onscreen keyboard
Requires:        plasma-keyboard%{?_isa}

# lockscreen look-and-feel imports qml: QtQuick.VirtualKeyboard
Requires:        qt6-qtvirtualkeyboard

Requires:        (uresourced if systemd-oomd-defaults)

# needed for task manager thumbnails under wayland and for things like
# screenshare portal
BuildRequires:  kpipewire-devel

# Require any plasmashell (plasma-desktop provides plasmashell(desktop))
%if 0%{?bootstrap}
Provides:       plasmashell = %{version}
%else
# Note: We should require >= %%{version}, but that creates a circular dependency
# at build time of plasma-desktop, because it provides the needed dependency, but
# also needs plasma-workspace to build. So for now the dependency is unversioned.
Requires:       plasmashell
%endif

# plasmashell provides dbus service org.freedesktop.Notifications
Provides: desktop-notification-daemon

# digitalclock applet
%if ! 0%{?bootstrap}
BuildRequires: pkgconfig(iso-codes)
%endif
Requires: iso-codes

# Split of Xorg session into subpackage
Obsoletes: plasma-workspace < 5.19.5-2

# khotkeys was dropped
Obsoletes: khotkeys < 6

# Require Wayland session dependencies appropriately
Requires:   kwin
Requires:   xorg-x11-server-Xwayland
Requires:   qt6-qtwayland%{?_isa}
# startplasmacompositor deps
Requires:   qt6-qttools
Requires:   xdg-desktop-portal-kde
# Enables X11 apps to screenshare a Wayland environment
Recommends: xwaylandvideobridge
# Replace the old -wayland subpackage
Obsoletes:  %{name}-wayland < 6.4.1-2
Conflicts:  %{name}-wayland < 6.4.1-2
Provides:   %{name}-wayland = %{version}-%{release}
Provides:   %{name}-wayland%{?_isa} = %{version}-%{release}

%description
Plasma 6 libraries and runtime components

%package common
Summary: Common files for %{name}
%description common
%{name}.

%package -n libkworkspace6
Summary: Runtime libkworkspace6 library
# when spilt occurred
Obsoletes: plasma-workspace < 5.4.2-2
Obsoletes: libkworkspace5 < %{version}-%{release}
Requires:  %{name}-common = %{version}-%{release}
%description -n libkworkspace6
%{summary}.

%package libs
Summary: Runtime libraries for %{name}
# when split out
Obsoletes: plasma-workspace < 5.4.2-2
## omit dep on main pkg for now, means we can avoid pulling in a
## huge amount of deps (including kde4) into buildroot -- rex
#Requires:  %%{name}%%{?_isa} = %%{version}-%%{release}
Requires:  %{name}-common = %{version}-%{release}
# consider splitting out plasma_packagestructure content later
Provides: plasma-packagestructure = %{version}-%{release}
%description libs
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       libkworkspace6%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation and user manuals for %{name}
# Automatically converted from old format: GFDL - review is highly recommended.
License:        LicenseRef-Callaway-GFDL
# switch to noarch
Obsoletes:      plasma-workspace-doc < 5.3.1-2
Requires:       %{name}-common = %{version}-%{release}
BuildArch: noarch
%description    doc
Documentation and user manuals for %{name}.


%package -n sddm-wayland-plasma
Summary:        Plasma Wayland SDDM greeter configuration
Provides:       sddm-greeter-displayserver
Conflicts:      sddm-greeter-displayserver
Requires:       kwin-wayland
Requires:       layer-shell-qt
Requires:       plasma-keyboard
Supplements:    (sddm and plasma-workspace)
%if ! (0%{?fedora} && 0%{?fedora} < 38)
# Replace sddm-x11 with sddm-wayland-plasma
## N.B.: If sddm gets updated in F36/F37, this will need to be bumped
Obsoletes:      sddm-x11 < 0.19.0^git20230404.e652433-2
%endif
BuildArch:      noarch

%description -n sddm-wayland-plasma
This package contains configuration and dependencies for SDDM
to use KWin for the Wayland compositor for the greeter.

%package -n plasma-lookandfeel-fedora
Summary:  Fedora look-and-feel for Plasma
Requires: %{name} = %{version}-%{release}
# lockscreen look-and-feel imports qml: QtQuick.VirtualKeyboard
Requires: qt6-qtvirtualkeyboard
# when switched to noarch
Obsoletes: plasma-lookandfeel-fedora < 5.8.0-5
# https://bugzilla.redhat.com/show_bug.cgi?id=1356890
Obsoletes: f22-kde-theme < 22.4
Obsoletes: f23-kde-theme < 23.1
Obsoletes: f24-kde-theme < 24.6
Obsoletes: f24-kde-theme-core < 5.10.5-2
BuildArch: noarch
%description -n plasma-lookandfeel-fedora
%{summary}.


%prep
%autosetup -p1

# Populate initial lookandfeel package
cp -a lookandfeel/org.kde.breeze lookandfeel/org.fedoraproject.fedora
cp -a lookandfeel/org.kde.breeze lookandfeel/org.fedoraproject.fedoradark
cp -a lookandfeel/org.kde.breeze lookandfeel/org.fedoraproject.fedoralight
# Overwrite settings to configure twilight mode
cp -a lookandfeel/org.kde.breezetwilight/* lookandfeel/org.fedoraproject.fedora
# Overwrite settings to configure dark mode
cp -a lookandfeel/org.kde.breezedark/* lookandfeel/org.fedoraproject.fedoradark
# Write the correct lookandfeel package names
install -m 0644 %{SOURCE15} lookandfeel/org.fedoraproject.fedora/metadata.json
install -m 0644 %{SOURCE16} lookandfeel/org.fedoraproject.fedoradark/metadata.json
install -m 0644 %{SOURCE17} lookandfeel/org.fedoraproject.fedoralight/metadata.json
cat >> lookandfeel/CMakeLists.txt <<EOL
plasma_install_package(org.fedoraproject.fedora org.fedoraproject.fedora.desktop look-and-feel lookandfeel)
plasma_install_package(org.fedoraproject.fedoradark org.fedoraproject.fedoradark.desktop look-and-feel lookandfeel)
plasma_install_package(org.fedoraproject.fedoralight org.fedoraproject.fedoralight.desktop look-and-feel lookandfeel)
EOL


%build
%cmake_kf6 \
  -DINSTALL_SDDM_WAYLAND_SESSION:BOOL=ON \
  -DWITH_X11_SESSION:BOOL=OFF \
  -DGLIBC_LOCALE_GEN:BOOL=OFF \
  -DGLIBC_LOCALE_PREGENERATED:BOOL=ON
%cmake_build


%install
%cmake_install

#chrpath --delete %{buildroot}%{_kf6_qtplugindir}/phonon_platform/kde.so

# General startplasma symlink
ln -sr %{buildroot}%{_kf6_bindir}/startplasma-wayland %{buildroot}%{_kf6_bindir}/startplasma

# Drop (Wayland) qualifier from plasma.desktop
sed -E 's| \(.*\)||g' -i %{buildroot}%{_datadir}/wayland-sessions/plasma.desktop

# move sddm configuration snippet to the right place
mkdir -p %{buildroot}%{_prefix}/lib/sddm
mv %{buildroot}%{_sysconfdir}/sddm.conf.d %{buildroot}%{_prefix}/lib/sddm

## customize plasma-lookandfeel-fedora defaults
# from [Wallpaper] Image=Next to Image=Fedora
sed -i -e 's|^Image=.*$|Image=Fedora|g' \
  %{buildroot}%{_kf6_datadir}/plasma/look-and-feel/org.fedoraproject.fedora*.desktop/contents/defaults

# PAM
# https://invent.kde.org/plasma/kscreenlocker/-/merge_requests/163#less-simple-method-for-redhat-and-redhat-adjacent-fedora-opensuse-etc-systems
install -m644 -p -D %{SOURCE100} %{buildroot}%{_sysconfdir}/pam.d/kde
install -m644 -p -D %{SOURCE101} %{buildroot}%{_sysconfdir}/pam.d/kde-fingerprint
install -m644 -p -D %{SOURCE102} %{buildroot}%{_sysconfdir}/pam.d/kde-smartcard

# Make kdestart use systemd
install -m644 -p -D %{SOURCE11} %{buildroot}%{_sysconfdir}/xdg/startkderc

# systemd user service deps
mkdir -p %{buildroot}%{_userunitdir}/plasma-core.target.d/
mkdir -p %{buildroot}%{_userunitdir}/plasma-workspace@.target.d/

install -m644 -p -D %{SOURCE40} %{buildroot}%{_userunitdir}/plasma-core.target.d/ssh-agent.conf
%if ! (0%{?rhel} >= 11 || 0%{?fedora} >= 43)
install -m644 -p -D %{SOURCE41} %{buildroot}%{_userunitdir}/plasma-core.target.d/spice-vdagent.conf
%endif

%find_lang all --with-html --all-name

grep "%{_kf6_docdir}" all.lang > %{name}-doc.lang
grep libkworkspace.mo all.lang > libkworkspace6.lang
# any translations not used elsewhere, include in main pkg
cat *.lang | sort | uniq -u > %{name}.lang


%check
desktop-file-validate %{buildroot}%{_kf6_datadir}/applications/org.kde.{plasmashell,kcolorschemeeditor,kfontview,plasmawindowed,klipper,plasma-interactiveconsole,baloorunner,secretprompter}.desktop

%post
if [ -s /usr/sbin/setsebool ] ; then
  setsebool -P selinuxuser_execmod 1 ||:
fi

%files common
%license LICENSES

%files -f %{name}.lang
%{_libexecdir}/ksecretprompter
%{_kf6_datadir}/applications/org.kde.baloorunner.desktop
%{_kf6_datadir}/applications/org.kde.secretprompter.desktop
%{_kf6_datadir}/xdg-desktop-portal/kde-portals.conf
%{_sysconfdir}/xdg/menus/plasma-applications.menu
%{_kf6_bindir}/gmenudbusmenuproxy
%{_kf6_bindir}/kcminit
%{_kf6_bindir}/kcminit_startup
%{_kf6_bindir}/krunner
%{_kf6_bindir}/ksmserver
%{_kf6_bindir}/ksplashqml
%{_kf6_bindir}/plasmashell
%{_kf6_bindir}/plasmawindowed
%{_kf6_bindir}/plasma_session
%{_kf6_bindir}/plasma-apply-*
%{_kf6_bindir}/plasma-interactiveconsole
%{_kf6_bindir}/plasma-shutdown
%{_kf6_bindir}/plasma_waitforname
%{_kf6_bindir}/xembedsniproxy
%{_kf6_bindir}/kcolorschemeeditor
%{_kf6_bindir}/kde-systemd-start-condition
%{_kf6_bindir}/kfontinst
%{_kf6_bindir}/kfontview
%{_kf6_bindir}/lookandfeeltool
%{_kf6_qmldir}/org/kde/*
%{_libexecdir}/baloorunner
%{_libexecdir}/ksmserver-logout-greeter
%{_libexecdir}/kf6/kauth/fontinst*
%{_libexecdir}/kfontprint
%{_libexecdir}/plasma-changeicons
%{_libexecdir}/plasma-dbus-run-session-if-needed
%{_libexecdir}/plasma-fallback-session-*
%{_kf6_datadir}/plasma/avatars/
%{_kf6_datadir}/plasma/plasmoids/
%{_kf6_datadir}/plasma/wallpapers/
%dir %{_kf6_datadir}/plasma/look-and-feel/
%{_kf6_datadir}/plasma/look-and-feel/org.kde.breeze.desktop/
%{_kf6_datadir}/plasma/look-and-feel/org.kde.breezedark.desktop/
%{_kf6_datadir}/plasma/look-and-feel/org.kde.breezetwilight.desktop/
%{_kf6_datadir}/solid/
%{_kf6_datadir}/kstyle/
%{_sysconfdir}/xdg/startkderc
%{_sysconfdir}/xdg/autostart/*.desktop
%{_datadir}/zsh/site-functions/_krunner
%{_datadir}/zsh/site-functions/_plasmashell
%{_datadir}/icons/hicolor/*/*/*font*.png
%{_datadir}/icons/hicolor/scalable/apps/preferences-desktop-font-installer.svgz
%{_datadir}/desktop-directories/*.directory
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/org.kde.fontinst.service
%{_datadir}/dbus-1/system.d/org.kde.fontinst.conf
%{_datadir}/knsrcfiles/*.knsrc
%{_datadir}/kfontinst/icons/hicolor/*/actions/*font*.png
%{_datadir}/konqsidebartng/virtual_folders/services/fonts.desktop
%{_datadir}/krunner/dbusplugins/plasma-runner-baloosearch.desktop
%{_datadir}/kxmlgui5/kfontviewpart/kfontviewpart.rc
%{_datadir}/kxmlgui5/kfontview/kfontviewui.rc
%{_kf6_datadir}/knotifications6/*.notifyrc
%{_kf6_datadir}/config.kcfg/*
%{_kf6_datadir}/kio_desktop/
%{_kf6_datadir}/applications/kcm_*
%{_kf6_datadir}/applications/org.kde.plasmashell.desktop
%{_kf6_datadir}/applications/org.kde.kcolorschemeeditor.desktop
%{_kf6_datadir}/applications/org.kde.kfontview.desktop
%{_kf6_datadir}/applications/org.kde.kfontinst.desktop
%{_kf6_datadir}/applications/org.kde.plasmawindowed.desktop
%{_kf6_datadir}/applications/org.kde.plasma-fallback-session-save.desktop
%{_kf6_datadir}/applications/org.kde.klipper.desktop
%{_kf6_datadir}/kio/servicemenus/installfont.desktop
%{_kf6_datadir}/qlogging-categories6/*.categories
%{_sysconfdir}/xdg/plasmanotifyrc
%{_kf6_datadir}/polkit-1/actions/org.kde.fontinst.policy
%{_userunitdir}/*.service
%{_userunitdir}/plasma-core.target
%dir %{_userunitdir}/plasma-core.target.d/
%{_userunitdir}/plasma-core.target.d/ssh-agent.conf
%if ! (0%{?rhel} >= 11 || 0%{?fedora} >= 43)
%{_userunitdir}/plasma-core.target.d/spice-vdagent.conf
%endif
%{_userunitdir}/plasma-workspace.target
%{_userunitdir}/plasma-workspace-wayland.target
%{_userunitdir}/plasma-workspace-x11.target
%dir %{_userunitdir}/plasma-workspace@.target.d/
%{_libdir}/kconf_update_bin/plasma6.3-update-clipboard-database-2-to-3
%{_datadir}/kconf_update/plasma6.3-update-clipboard-database-2-to-3.upd
%{_libdir}/kconf_update_bin/plasmashell-6.5-remove-stop-activity-shortcut
%{_datadir}/kconf_update/plasmashell-6.5-remove-stop-activity-shortcut.upd
%{_kf6_datadir}/timezonefiles/timezones.json
%{_kf6_datadir}/applications/org.kde.plasma-interactiveconsole.desktop
# PAM
%config(noreplace) %{_sysconfdir}/pam.d/kde
%config(noreplace) %{_sysconfdir}/pam.d/kde-fingerprint
%config(noreplace) %{_sysconfdir}/pam.d/kde-smartcard
# Plasma Wayland
%{_kf6_bindir}/startplasma
%{_kf6_bindir}/startplasma-wayland
%{_datadir}/wayland-sessions/plasma.desktop

%files doc -f %{name}-doc.lang

%files -n libkworkspace6 -f libkworkspace6.lang
%{_libdir}/libkworkspace6.so.*

%files libs
%{_libdir}/libbatterycontrol.so.*
%{_libdir}/libtaskmanager.so.*
%{_libdir}/libklipper.so.*
%{_libdir}/libkrdb.so
%{_libdir}/libnotificationmanager.*
%{_libdir}/libkfontinst*
%{_libdir}/libkmpris.so.*
# multilib'able plugins
%{_kf6_qtplugindir}/plasma/applets/
%if %{with kf6_pim}
%{_kf6_qtplugindir}/plasmacalendarplugins/
%endif
%{_kf6_plugindir}/kio/*.so
%{_kf6_plugindir}/kded/*.so
%{_libdir}/libklookandfeel.so.6
%{_libdir}/libklookandfeel.so.%{version}
%{_kf6_plugindir}/krunner/*
%{_qt6_plugindir}/plasma/kcms/systemsettings/kcm_*.so
%{_kf6_qtplugindir}/kf6/parts/kfontviewpart.so
%{_kf6_qtplugindir}/kf6/thumbcreator/fontthumbnail.so
%{_kf6_qtplugindir}/kf6/kfileitemaction/wallpaperfileitemaction.so
%{_kf6_qtplugindir}/kf6/packagestructure/plasma_layouttemplate.so
%{_kf6_qtplugindir}/kf6/packagestructure/plasma_lookandfeel.so
%{_kf6_qtplugindir}/kf6/packagestructure/wallpaper_images.so
%{_kf6_qtplugindir}/plasma/containmentactions/org.kde.applauncher.so
%{_kf6_qtplugindir}/plasma/containmentactions/org.kde.contextmenu.so
%{_kf6_qtplugindir}/plasma/containmentactions/org.kde.paste.so
%{_kf6_qtplugindir}/plasma/containmentactions/org.kde.switchdesktop.so
%{_kf6_qtplugindir}/plasma/containmentactions/switchwindow.so
%{_kf6_qtplugindir}/plasma/containmentactions/switchactivity.so
%{_kf6_qtplugindir}/plasma/kcminit/kcm_fonts_init.so
%{_kf6_qtplugindir}/plasma/kcminit/kcm_style_init.so
%{_kf6_qtplugindir}/plasma/kcms/systemsettings_qwidgets/kcm_fontinst.so
%{_libexecdir}/plasma-sourceenv.sh
%{_kf6_datadir}/kconf_update/plasma6.0-remove-dpi-settings.upd
%{_kf6_datadir}/kconf_update/plasmashell-6.0-keep-default-floating-setting-for-plasma-5-panels.upd
%{_kf6_datadir}/kconf_update/plasma6.0-remove-old-shortcuts.upd
%{_kf6_datadir}/kconf_update/migrate-calendar-to-plugin-id.upd
%{_kf6_datadir}/kconf_update/migrate-calendar-to-plugin-id.py
%{_kf6_datadir}/kconf_update/plasmashell-6.0-keep-custom-position-of-panels.upd
%{_kf6_datadir}/kconf_update/plasma6.4-migrate-fullscreen-notifications-to-dnd.upd
%{_libdir}/kconf_update_bin/plasma6.0-remove-old-shortcuts
%{_libdir}/kconf_update_bin/plasmashell-6.0-keep-default-floating-setting-for-plasma-5-panels
%{_libdir}/kconf_update_bin/plasma6.0-remove-dpi-settings
%{_libdir}/kconf_update_bin/plasmashell-6.0-keep-custom-position-of-panels
%{_libdir}/kconf_update_bin/plasma6.4-migrate-fullscreen-notifications-to-dnd
%{_kf6_datadir}/kglobalaccel/org.kde.krunner.desktop

%files devel
%{_libdir}/libbatterycontrol.so
%{_libdir}/libklipper.so
%{_libdir}/libtaskmanager.so
%{_libdir}/libkworkspace6.so
%{_includedir}/kworkspace6/
%{_includedir}/taskmanager/
%{_includedir}/notificationmanager/
%{_libdir}/cmake/KRunnerAppDBusInterface/
%{_libdir}/cmake/KSMServerDBusInterface/
%{_libdir}/cmake/LibKLookAndFeel/
%{_libdir}/cmake/LibKWorkspace/
%{_libdir}/cmake/LibTaskManager/
%{_libdir}/cmake/LibNotificationManager/
%{_datadir}/dbus-1/interfaces/*.xml
%{_includedir}/krdb/krdb.h
%{_includedir}/krdb/krdb_export.h
%{_includedir}/klookandfeel/
%{_libdir}/cmake/Krdb/*.cmake
%{_libdir}/libklookandfeel.so

%files -n sddm-wayland-plasma
%{_prefix}/lib/sddm/sddm.conf.d/plasma-wayland.conf

%files -n plasma-lookandfeel-fedora
%{_kf6_datadir}/plasma/look-and-feel/org.fedoraproject.fedora*.desktop/


%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Sun Feb 08 2026 Neal Gompa <ngompa@fedoraproject.org> - 6.5.91-2
- Unconditionally require plasma-keyboard

* Tue Jan 27 2026 Steve Cossette <farchord@gmail.com> - 6.5.91-1
- 6.5.91

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 farchord@gmail.com - 6.5.90-1
- 6.5.90

* Tue Jan 13 2026 farchord@gmail.com - 6.5.5-1
- 6.5.5

* Sun Dec 14 2025 Alessandro Astone <ales.astone@gmail.com> - 6.5.4-2
- Default to plasma-keyboard in sddm for f44

* Tue Dec 09 2025 Steve Cossette <farchord@gmail.com> - 6.5.4-1
- 6.5.4

* Fri Dec 05 2025 Neal Gompa <ngompa@fedoraproject.org> - 6.5.3-3
- Install light/dark variants of Fedora look and feel theme

* Sun Nov 23 2025 Steve Cossette <farchord@gmail.com> - 6.5.3-2
- Rebuild

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

* Tue Sep 30 2025 Jan Grulich <jgrulich@redhat.com> - 6.4.5-4
- Rebuild (qt6)

* Fri Sep 26 2025 Neal Gompa <ngompa@fedoraproject.org> - 6.4.5-3
- Drop spice-vdagent snippet for F43+ / EL11+ (RHBZ#2399742)

* Thu Sep 25 2025 Steve Cossette <farchord@gmail.com> - 6.4.90-1
- 6.4.90

* Wed Sep 24 2025 Steve Cossette <farchord@gmail.com> - 6.4.5-2
- Fix for Qt 6.9.2-related crash

* Tue Sep 16 2025 farchord@gmail.com - 6.4.5-1
- 6.4.5

* Tue Aug 26 2025 Steve Cossette <farchord@gmail.com> - 6.4.4-3
- Adding plasma-keyboard as a runtime dependancy

* Thu Aug 07 2025 František Zatloukal <fzatlouk@redhat.com> - 6.4.4-2
- Rebuilt for icu 77.1

* Wed Aug 06 2025 Steve Cossette <farchord@gmail.com> - 6.4.4-1
- 6.4.4

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 6.4.3-3
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Steve Cossette <farchord@gmail.com> - 6.4.3-1
- 6.4.3

* Thu Jul 03 2025 Steve Cossette <farchord@gmail.com> - 6.4.2-1
- 6.4.2

* Wed Jun 25 2025 Neal Gompa <ngompa@fedoraproject.org> - 6.4.1-2
- Merge plasma-workspace-wayland subpackage into main package

* Tue Jun 24 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.1-1
- 6.4.1

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

* Mon Apr 14 2025 Jan Grulich <jgrulich@redhat.com> - 6.3.4-3
- Rebuild (qt6)

* Thu Apr 03 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.4-2
- Backport upstream patch

* Wed Apr 02 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.4-1
- 6.3.4

* Tue Mar 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.3.3-2
- Rebuild (qt6)

* Tue Mar 11 2025 Steve Cossette <farchord@gmail.com> - 6.3.3-1
- 6.3.3

* Tue Feb 25 2025 Steve Cossette <farchord@gmail.com> - 6.3.2-1
- 6.3.2

* Tue Feb 18 2025 Steve Cossette <farchord@gmail.com> - 6.3.1-1
- 6.3.1

* Thu Feb 06 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.0-1
- 6.3.0

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 6.2.91-2
- Add explicit BR: libxcrypt-devel

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

* Wed Nov 13 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.2.3-2
- Backport patch to drop xsetroot dependency
- Drop unused iceauth dependency

* Tue Nov 05 2024 Steve Cossette <farchord@gmail.com> - 6.2.3-1
- 6.2.3

* Tue Oct 22 2024 Steve Cossette <farchord@gmail.com> - 6.2.2-1
- 6.2.2

* Wed Oct 16 2024 Steve Cossette <farchord@gmail.com> - 6.2.1.1-1
- 6.2.1.1

* Tue Oct 15 2024 Steve Cossette <farchord@gmail.com> - 6.2.1-1
- 6.2.1

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 6.2.0-3
- Rebuild (qt6)

* Sun Oct 06 2024 Steve Cossette <farchord@gmail.com> - 6.2.0-2
- 6.2.0 Respin

* Thu Oct 03 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Sun Sep 15 2024 Alessandro Astone <ales.astone@gmail.com> - 6.1.90-2
- Add missing dependency on xsetroot.
  Fixes cursor in some XWayland apps.
  (https://pagure.io/fedora-kde/SIG/issue/562)

* Thu Sep 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.90-1
- 6.1.90

* Tue Sep 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.5-1
- 6.1.5
- Add missing dependency on xsetroot.
  Fixes cursor in some XWayland apps.
  (https://pagure.io/fedora-kde/SIG/issue/562)

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 6.1.4-3
- convert license to SPDX

* Thu Aug 15 2024 Alessandro Astone <ales.astone@gmail.com> - 6.1.4-2
- Set pre-generated locales (rhbz#2300192)

* Fri Aug 09 2024 Steve Cossette <farchord@gmail.com> - 6.1.4-1
- 6.1.4

* Thu Jul 25 2024 Timothée Ravier <tim@siosm.fr> - 6.1.3-4
- Backport patch for https://pagure.io/fedora-kde/SIG/issue/539

* Wed Jul 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.3-3
- rebuilt

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.3-1
- 6.1.3

* Sat Jul 06 2024 Mukundan Ragavan <nonamedotc@gmail.com> - 6.1.2-2
- rebuild for libqalculate soname update

* Wed Jul 03 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.2-1
- 6.1.2

* Tue Jun 25 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.1-1
- 6.1.1

* Tue Jun 18 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-3
- Rebuild to sort dependencies with plasma-desktop

* Tue Jun 18 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-2
- Rebuild due to upstream re-spin

* Thu Jun 13 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-1
- 6.1.0

* Fri May 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.90-1
- 6.0.90

* Wed May 22 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.5-1
- 6.0.5

* Tue Apr 16 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.4-1
- 6.0.4

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.0.3-3
- Rebuild (qt6)

* Tue Apr 02 2024 Alessandro Astone <ales.astone@gmail.com> - 6.0.3-2
- Backport systray icon color bugfix

* Tue Mar 26 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.3-1
- 6.0.3

* Fri Mar 15 2024 Marie Loise Nolden <loise@kde.org> - 6.0.2-2
- fix startup sound by adding upstream patches

* Tue Mar 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.2-1
- 6.0.2

* Mon Mar 11 2024 Alessandro Astone <ales.astone@gmail.com> - 6.0.1-2
- Patch qtpaths binary name, avoids abort on first login

* Wed Mar 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.1-1
- 6.0.1

* Fri Mar 01 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.0.0-4
- Add Recommends on xwaylandvideobridge for -wayland

* Wed Feb 28 2024 Steve Cossette <farchord@gmail.com> - 6.0.0-3
- Updated package's build/runtime requirements

* Mon Feb 26 2024 Alessandro Astone <ales.astone@gmail.com> - 6.0.0-2
- Respin 6.0.0

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Tue Feb 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 5.93.0-6
- Backport rudimentary auto-launch apps on reboot from 6.1

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 5.93.0-5
- Rebuild (qt6)

* Thu Feb 15 2024 Alessandro Astone <ales.astone@gmail.com> - 5.93.0-4
- Stricter x11 obsoletes version

* Tue Feb 13 2024 Neal Gompa <ngompa@fedoraproject.org> - 5.93.0-3
- Drop qualifier from plasma.desktop

* Mon Feb 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.93.0-2
- Backport security patch

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.93.0-1
- 5.93.0

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 5.92.0-7
- Rebuild for ICU 74

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Steve Cossette <farchord@gmail.com> - 5.92.0-4
- Added patch for bug: app activation/minimize problems in taskbar

* Mon Jan 15 2024 Alessandro Astone <ales.astone@gmail.com> - 5.92.0-3
- Rebuild for plasma-breeze

* Thu Jan 11 2024 Alessandro Astone <ales.astone@gmail.com> - 5.92.0-2
- Re-enable audiocd-kio recommends

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.92.0-1
- 5.92.0

* Sat Dec 23 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.91.0-2
- Clean up uneeded conditionals in packaging

* Thu Dec 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.91.0-1
- 5.91.0

* Mon Dec 04 2023 Alessandro Astone <ales.astone@gmail.com> - 5.90.0-2
- Update breeze-fedora sddm theme

* Sun Dec 03 2023 Justin Zobel <justin.zobel@gmail.com> - 5.90.0-1
- Update to 5.90.0

* Wed Nov 29 2023 Jan Grulich <jgrulich@redhat.com> - 5.27.80-15
- Rebuild (qt6)

* Sat Nov 25 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-14
- Re-enable downstream patches

* Fri Nov 24 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-13
- Add missing QML dependency for lockscreen

* Fri Nov 24 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-12
- Add missing QML dependency for sddm-breeze

* Fri Nov 24 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-11
- Switch default sound theme

* Tue Nov 21 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-10
- Convert look-and-feel metadata to json to enable the theme again
- Re-enable the fedora background

* Mon Nov 20 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-9
- Rebuild for kf6-kquickcharts versioning
- Redo PAM to support upstream changes for multiple concurrent pam sessions

* Sun Nov 19 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-8
- Re-enable 01-breeze-fedora

* Sun Nov 19 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-7
- sddm-wayland-plasma requries layer-shell-qt

* Sat Nov 18 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-6
- Fix Plasma 6 runtime requirements

* Sat Nov 18 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.27.80-5
- Drop -x11 subpackage and have -wayland subpackage obsolete it
- Remove all legacy conditionals from Plasma 5

* Sat Nov 18 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-4
- libkworkspace6 subpackage
- Require kf6-kirigami2-addons at runtime

* Sat Nov 18 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-3
- Remove runtime dependency on deprecated khotkeys

* Sat Nov 18 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-2
- Rebuild against rawhide kuserfeedback

* Wed Nov 15 2023 Steve Cossette <farchord@gmail.com> - 5.27.80-1
- 5.27.80

* Fri Nov 03 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.27.9.1-2
- Mark plasma-workspace-x11 as deprecated

* Wed Oct 25 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.9.1-1
- 5.27.9.1
- Replace old %%stable macro

* Tue Oct 24 2023 Steve Cossette <farchord@gmail.com> - 5.27.9-1
- 5.27.9

* Fri Sep 22 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.27.8-2
- Recommend orca for a11y and require xdg-desktop-portal-kde for wayland

* Tue Sep 12 2023 justin.zobel@gmail.com - 5.27.8-1
- 5.27.8

* Sat Aug 12 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.7-2
- Add upstream patch

* Tue Aug 01 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.7-1
- 5.27.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.27.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 5.27.6-2
- Rebuilt for ICU 73.2

* Sun Jun 25 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.6-1
- 5.27.6

* Mon Jun 12 2023 Timothée Ravier <tim@siosm.fr> - 5.27.5-2
- Recommend kde-inotify-survey & kf5-audiocd-kio

* Wed May 10 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.5-1
- 5.27.5

* Wed Apr 05 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.27.4.1-2
- Bump sddm Obsoletes for F38+

* Tue Apr 04 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.4.1-1
- 5.27.4.1

* Tue Apr 04 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.4-1
- 5.27.4

* Mon Apr 03 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.27.3-4
- Add Obsoletes sddm-x11 for sddm-wayland transition in F38+

* Mon Mar 27 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.3-3
- Add patch to hide the virtual keyboard indicator from sddm

* Wed Mar 22 2023 Adam Williamson <awilliam@redhat.com> - 5.27.3-2
- Backport MR #2767 to fix slow startup issue (#2179998)

* Tue Mar 14 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.3-1
- 5.27.3

* Mon Mar 13 2023 Adam Williamson <awilliam@redhat.com> - 5.27.2-3
- Rebuild with no changes for F38 Bodhi purposes

* Mon Mar 13 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.2-2
- Add Requires: kde-settings-sddm to sddm-breeze subpackage

* Tue Feb 28 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.2-1
- 5.27.2

* Tue Feb 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.1-1
- 5.27.1
- Recommends plasma-welcome on Fedora

* Mon Feb 20 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.27.0-4
- Add patch to disable global shortcuts at login (#2171332)

* Wed Feb 15 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.27.0-3
- Add wayland-protocols-devel BR
- Add kf5-libkexiv2-devel BR

* Tue Feb 14 2023 Marc Deop marcdeop@fedoraproject.org - 5.27.0-2
- Rebuild against new sources

* Thu Feb 09 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.26.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 19 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.26.90-1
- 5.26.90

* Thu Jan 05 2023 Justin Zobel <justin@1707.io> - 5.26.5-1
- Update to 5.26.5

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 5.26.4.1-2
- Rebuild for ICU 72

* Tue Nov 29 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.4.1-1
- 5.26.4.1

* Tue Nov 29 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.4-1
- 5.26.4

* Wed Nov 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.3-1
- 5.26.3

* Mon Nov 07 2022 Marc Deop marcdeop@fedoraproject.org - 5.26.2-3
- BuildRequires for kpipewire-devel

* Sat Nov 05 2022 Marc Deop marcdeop@fedoraproject.org - 5.26.2-2
- Require kpipewire

* Wed Oct 26 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.2-1
- 5.26.2

* Tue Oct 18 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.1-1
- 5.26.1

* Thu Oct 06 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.0-1
- 5.26.0

* Sun Sep 25 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.25.90-2
- Add Fedora patches to change default desktop context menu configuration
  + Enable "Open Terminal" action
  + Enable "Lock" and "Logout" actions

* Sat Sep 17 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.90-1
- 5.25.90

* Wed Sep 07 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.5-1
- 5.25.5

* Fri Aug 26 2022 Adam Williamson <awilliam@redhat.com> - 5.25.4-2
- Disable sddm-on-wayland for F37 (#2110801)

* Wed Aug 03 2022 Justin Zobel <justin@1707.io> - 5.25.4-1
- Update to 5.25.4

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.25.3.1-8
- Rebuilt for ICU 71.1

* Wed Jul 27 2022 Troy Dawson <tdawson@redhat.com> - 5.25.3.1-7
- Add BuildRequires libicu-devel - enables this code
  https://invent.kde.org/plasma/plasma-workspace/-/merge_requests/1725

* Mon Jul 25 2022 Jan Grulich <jgrulich@redhat.com> - 5.25.3.1-6
- Rebuild (qt5)

* Sun Jul 24 2022 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.25.3.1-5
- Added patch to fix #457019

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.25.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jan Grulich <jgrulich@redhat.com> - 5.25.3.1-3
- Disable toplevel fixed positions on Wayland

* Thu Jul 14 2022 Jan Grulich <jgrulich@redhat.com> - 5.25.3.1-2
- Rebuild (qt5)

* Tue Jul 12 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.3.1-1
- 5.25.3.1

* Tue Jul 12 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.3-1
- 5.25.3

* Tue Jun 28 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.2-1
- 5.25.2

* Tue Jun 21 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.1-1
- 5.25.1

* Tue Jun 14 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.25.0-2
- Remove broken mechanism for setting default look and feel
- Always ship Fedora look and feel theme
- Drop unneeded sddm theme snapshot and patches

* Thu Jun 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.0-1
- 5.25.0

* Fri May 20 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.90-1
- 5.24.90

* Tue May 17 2022 Jan Grulich <jgrulich@redhat.com> - 5.24.5-3
- Rebuild (qt5)

* Fri May 06 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.24.5-2
- Rebuild for new gpsd

* Tue May 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.5-1
- 5.24.5

* Thu Mar 31 2022 Justin Zobel <justin@1707.io> - 5.24.4-1
- Update to 5.24.4

* Mon Mar 14 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.24.3-2
- Do not use the SDDM Wayland greeter by default for F36

* Tue Mar 08 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.3-1
- 5.24.3

* Tue Mar 08 2022 Jan Grulich <jgrulich@redhat.com> - 5.24.2-4
- Rebuild (qt5)

* Sun Mar 06 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.24.2-3
- Backport sddm theme improvements to fix visual bugs (#2054016, #2058468)
- Correctly set distro logo for fedora breeze sddm theme

* Mon Feb 28 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.24.2-2
- Refresh default look-and-feel patch to fix for Plasma 5.24

* Tue Feb 22 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.24.2-1
- 5.24.2

* Tue Feb 15 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.1-1
- 5.24.1

* Fri Feb 11 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.0-2
- Rebuild due to tarball re-spin

* Thu Feb 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.0-1
- 5.24.0
- Add sddm-wayland-plasma subpackage to ship Wayland greeter configuration

* Wed Jan 19 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.23.90-2
- rebase konsole-in-contextmenu.patch (#2026789)

* Thu Jan 13 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.90-1
- 5.23.90

* Tue Jan 04 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.5-1
- 5.23.5

* Wed Dec 29 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.4-2
- -wayland: Recommends: xdg-desktop-portal-kde

* Tue Dec 14 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.4-1
- 5.23.4

* Wed Nov 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.3-1
- 5.23.3

* Tue Oct 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.2-1
- 5.23.2

* Sat Oct 23 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.1-1
- 5.23.1

* Fri Oct 08 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.0-1
- 5.23.0
- Add BuildRequires: systemd-rpm-macros

* Wed Sep 22 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.22.90-4
- Fix setup of Fedora Breeze look and feel

* Mon Sep 20 2021 Neal Gompa <ngompa@fedoraproject.org> - 5.22.90-3
- Drop forked Breeze Twilight theme in favor of in-tree one

* Mon Sep 20 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-2
- Remove patch(180) already applied upstream
- Remove patch(181) already applied upstream
- Comment out patch(100) as it does not apply cleanly
- Adjust files sections

* Fri Sep 17 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-1
- 5.22.90

* Sun Sep 12 2021 Alexey Kurov <nucleo@fedoraproject.org> - 5.22.5-2
- fix removable devices list in devicenotifier (#1975017)

* Tue Aug 31 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.5-1
- 5.22.5

* Wed Aug 11 2021 Björn Esser <besser82@fedoraproject.org> - 5.22.4-6
- Rebuild (gpsd)

* Sun Aug 08 2021 Mukundan Ragavan <nonamedotc@gmail.com> - 5.22.4-5
- rebuild for libqalculate

* Mon Aug 02 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.22.4-4
- Requires: maliit-keyboard

* Mon Aug 02 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.22.4-3
- conditionalize systemdBoot support
- Requires: uresourced (when systemdBoot is enabled)

* Fri Jul 30 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.22.4-2
- pull in upstream fix to add dependency on kwallet-pam user service

* Tue Jul 27 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.4-1
- 5.22.4

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.22.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.22.3-2
- add (modularized) user service dependencies for ssh-agent, spice-vdagent
- drop BR: kf5-kdelibs4support

* Mon Jul 12 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.3-1
- 5.22.3

* Thu Jul 01 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.22.2.1-2
- backport upstream fixes

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2.1-1
- 5.22.2.1

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2-1
- 5.22.2

* Tue Jun 15 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.1-1
- 5.22.1

* Sun Jun 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.0-1
- 5.22.0

* Fri May 28 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-4
- .konsole-in-contextmenu.patch rebased

* Tue May 18 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-3
- Requires: ksystemstats
- make other plasma-related runtime deps arch'd

* Sun May 16 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-2
- drop Requires: ksysguardd (#1960934)
- s/kf5-ksysguard/libksysguard/

* Fri May 14 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-1
- 5.21.90

* Thu May 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.5-4
- Reset systemd failed units on login (master/ branch backport)
- actually apply buffer types patch from -3

* Wed May 05 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.5-3
- Announce which buffer types are available on thumbnails elements

* Wed May 05 2021 Yaroslav Sidlovsky <zawertun@gmail.com> - 5.21.5-2
- xsetroot added as required for plasma-workspace-x11

* Tue May 04 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.5-1
- 5.21.5

* Fri Apr 30 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.4-2
- startkde: make compat symlink unconditionally use startplasma-x11
- startkde: drop compat symlink in future releases (f35+)

* Tue Apr 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.4-1
- 5.21.4

* Tue Mar 16 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.3-1
- 5.21.3

* Tue Mar 02 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.2-1
- 5.21.2

* Mon Mar 01 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.1-4
- plasma-core.target: +Before=ssh-agent.service

* Thu Feb 25 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.1-3
- plasma-workspace@.target: Wants += ssh-agent.service (#1761817)

* Wed Feb 24 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.1-2
- .spec cosmetics

* Tue Feb 23 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.1-1
- 5.21.1

* Thu Feb 11 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.0-1
- 5.21.0

* Fri Jan 29 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.90-9
- pull in upstream fix for lockscreen detection (kde#432251)

* Thu Jan 28 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.90-7
- pull in upstream wayland session fix (kde#432189)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.20.90-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Neal Gompa <ngompa13@gmail.com> - 5.20.90-5
- Switch over to systemd user sessions

* Mon Jan 25 2021 Neal Gompa <ngompa13@gmail.com> - 5.20.90-4
- Fix setup for default wallpaper in Fedora Breeze Twilight theme

* Sat Jan 23 2021 Neal Gompa <ngompa13@gmail.com> - 5.20.90-3
- Fix configuration of Fedora Breeze Twilight theme

* Fri Jan 22 2021 Neal Gompa <ngompa13@gmail.com> - 5.20.90-2
- Switch to new Breeze Twilight-based theme (pagureio#fedora-kde/SIG#12)
- Adapt Wayland by default to new upstream settings

* Thu Jan 21 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.90-1
- 5.20.90 (beta)

* Thu Jan 14 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.5-4
- rebuild (gpsd)
- update URL

* Thu Jan 14 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.5-3
- pull in upstream fix for sanitized user environment (#1754395)

* Thu Jan 14 10:43:00 CET 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.5-2
- Rebuild (gpsd)

* Tue Jan  5 16:03:33 CET 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.5-1
- 5.20.5

* Tue Dec 22 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.20.4-2
- runtime dep cleanup, mostly -dbus-x11, +dbus +dbus-tools

* Tue Dec  1 09:43:00 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.4-1
- 5.20.4

* Wed Nov 25 08:17:45 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.3-3
- rebuild (qt5)

* Sun Nov 15 15:23:57 CET 2020 Vitaly Zaitsev <vitaly@easycoding.org> - 5.20.3-2
- Backported patch with crash fix on logout (#1861700).

* Wed Nov 11 08:22:42 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.3-1
- 5.20.3

* Tue Oct 27 14:24:55 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.2-1
- 5.20.2

* Tue Oct 20 15:30:42 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.1.1-1
- 5.20.1

* Sun Oct 11 19:50:04 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.0-1
- 5.20.0

* Sat Oct 03 2020 Neal Gompa <ngompa13@gmail.com> - 5.19.90-2
- Use Wayland by default for F34+
  https://fedoraproject.org/wiki/Changes/WaylandByDefaultForPlasma

* Fri Sep 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.90-1
- 5.19.90

* Thu Sep 17 2020 Neal Gompa <ngompa13@gmail.com> - 5.19.5-2
- Split out Xorg session and set up conditional for Wayland by default

* Tue Sep 01 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.5-1
- 5.19.5

* Tue Jul 28 2020 Adam Jackson <ajax@redhat.com> - 5.19.4-2
- Require iceuth xrgb xprop, not xorg-x11-{server-,}utils

* Tue Jul 28 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.4-1
- 5.19.4

* Tue Jul 07 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.3-1
- 5.19.3

* Wed Jul 01 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.19.2-2
- Recommends: plasma-pa, plasma-milou

* Tue Jun 23 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.2-1
- 5.19.2

* Thu Jun 18 2020 Björn Esser <besser82@fedoraproject.org> - 5.19.1-2
- Rebuild (gpsd)

* Wed Jun 17 2020 Martin Kyral <martin.kyral@gmail.com> - 5.19.1-1
- 5.19.1

* Thu Jun 11 2020 Marie Loise Nolden <loise@kde.org> - 5.19.0-2
- drop qtwebkit build dependencies

* Tue Jun 9 2020 Martin Kyral <martin.kyral@gmail.com> - 5.19.0-1
- 5.19.0

* Fri May 15 2020 Martin Kyral <martin.kyral@gmail.com> - 5.18.90-1
- 5.18.90

* Tue May 05 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.5-1
- 5.18.5

* Thu Apr 09 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.4.1-2
- update patch "Qt applications lose system theme if launched via dbus activation" (#1754395)

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.4.1-1
- 5.18.4.1

* Fri Apr 03 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.4-2
- patch to workaround "Qt applications lose system theme if launched via dbus activation" (#1754395)

* Tue Mar 31 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.4-1
- 5.18.4

* Thu Mar 19 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.3-2
- f31+ plasma-lookandfeel-fedora: default to 'Fedora' wallpaper (#1812293)

* Tue Mar 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.3-1
- 5.18.3

* Sun Mar 08 2020 Mukundan Ragavan <nonamedotc@gmail.com> - 5.18.2-2
- rebuild for libqalculate

* Tue Feb 25 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.2-1
- 5.18.2

* Tue Feb 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.1-1
- 5.18.1

* Tue Feb 11 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.0-1
- 5.18.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.17.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Jan Grulich <jgrulich@redhat.com> - 5.17.90-1
- 5.17.90

* Wed Jan 08 2020 Jan Grulich <jgrulich@redhat.com> - 5.17.5-1
- 5.17.5

* Mon Dec 23 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.17.4-2
- provide compat /usr/bin/startkde symlink (#1785826, #1785973)

* Thu Dec 05 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.4-1
- 5.17.4

* Fri Nov 29 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 5.17.3-2
- rebuild for libqalculate

* Wed Nov 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.17.3-1
- 5.17.3

* Wed Oct 30 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.2-1
- 5.17.2

* Wed Oct 23 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.1-1
- 5.17.1

* Thu Oct 10 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.0-1
- 5.17.0

* Fri Sep 20 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.90-1
- 5.16.90

* Fri Sep 06 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.5-1
- 5.16.5

* Tue Aug 27 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 5.16.4-2
- rebuild for libqalculate

* Tue Jul 30 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.4-1
- 5.16.4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.3-1
- 5.16.3

* Wed Jul 03 2019 Björn Esser <besser82@fedoraproject.org> - 5.16.2-2
- Rebuild (gpsd)

* Wed Jun 26 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.2-1
- 5.16.2

* Tue Jun 18 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.16.1-1
- 5.16.1

* Tue Jun 11 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.0-1
- 5.16.0

* Sun May 19 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.90-3
- de-bootstrap

* Sun May 19 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.90-2
- bootstrap build

* Thu May 16 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.90-1
- 5.15.90

* Thu May 09 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.5-1
- 5.15.5

* Sun Apr 21 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 5.15.4-2
- rebuild for libqalculate

* Wed Apr 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.4-1
- 5.15.4

* Sat Mar 23 2019 Mukundan Ragavan <nonamedotc@gmail.com> - 5.15.3-2
- rebuild for libqalculate

* Tue Mar 12 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.3-1
- 5.15.3

* Thu Feb 28 2019 Pete Walter <pwalter@fedoraproject.org> - 5.15.2-2
- Update wayland deps

* Tue Feb 26 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.2-1
- 5.15.2

* Tue Feb 19 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.1-1
- 5.15.1

* Wed Feb 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.0-1
- 5.15.0

* Tue Feb 05 2019 Martin Kyral <martin.kyral@gmail.com> - 5.14.90-5
- fix startkde.patch

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.14.90-3
- de-bootstrap

* Sun Jan 20 2019 Martin Kyral <martin.kyral@gmail.com> - 5.14.90-1
- 5.14.90
- enable boostrap

* Tue Nov 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.4-1
- 5.14.4

* Thu Nov 08 2018 Martin Kyral <martin.kyral@gmail.com> - 5.14.3-1
- 5.14.3

* Wed Oct 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-2
- move systemmonitor.desktop to main, bump kf5 dep

* Wed Oct 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Tue Oct 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.1-1
- 5.14.1

* Thu Oct 11 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.0-3
- rebuild (gpsd)

* Wed Oct 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.0-2
- Fix build with gpsd 3.18 (#1638110)

* Sat Oct 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.0-1
- 5.14.0

* Tue Oct 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.90-2
- Provides: desktop-notification-daemon (#1628758)

* Fri Sep 14 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.90-1
- 5.13.90

* Tue Sep 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.5-1
- 5.13.5

* Tue Aug 21 2018 Mukundan Ragavan <nonamedotc@gmail.com> - 5.13.4-2
- rebuild for libqalculate.so.19()

* Thu Aug 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.4-1
- 5.13.4

* Wed Jul 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.3-4
- avoid versioned runtime powerdevil dep when bootstrapping

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.3-1
- 5.13.3

* Mon Jul 09 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.2-1
- 5.13.2

* Fri Jun 22 2018 Mukundan Ragavan <nonamedotc@gmail.com> - 5.13.1-2
- rebuild for libqalculate.so.18()

* Tue Jun 19 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.1-1
- 5.13.1

* Tue Jun 12 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.0-1
- 5.13.0

* Fri May 18 2018 Martin Kyral <martin.kyral@gmail.com> - 5.12.90-1
- 5.12.90

* Fri May 18 2018 Mukundan Ragavan <nonamedotc@gmail.com> - 5.12.5-4
- rebuild for libqalculate.so.17()

* Wed May 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-3
- sddm-breeze: Recommends: qt5-qtvirtualkeyboard

* Sun May 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-2
- refresh startkde.patch
- .spec cleanup

* Tue May 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-1
- 5.12.5

* Wed Apr 11 2018 Mukundan Ragavan <nonamedotc@gmail.com> - 5.12.4-2
- rebuild for libqalculate.so.16()

* Fri Mar 30 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-1
- 5.12.4

* Sat Mar 10 2018 Mukundan Ragavan <nonamedotc@gmail.com> - 5.12.3-2
- rebuild for libqalculate.so.14()

* Tue Mar 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-1
- 5.13.3
- plasmawayland session: drop explcitly running dbus_launch
- use %%make_build %%ldconfig_scriptlets

* Wed Feb 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.2-1
- 5.12.2

* Tue Feb 13 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.1-1
- 5.12.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.0-2
- respin

* Fri Feb 02 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.0-1
- 5.12.0

* Mon Jan 15 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.95-1
- 5.11.95

* Mon Jan 15 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.4-4
- use upstreamed version of previous commit/patch

* Mon Jan 15 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.4-3
- include candidate crash fix for xembedsniproxy (#1497829,kde#359664)

* Tue Dec 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.4-2
- refresh/fix startkde.patch

* Thu Nov 30 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.4-1
- 5.11.4

* Tue Nov 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-2
- .spec cruft, BR: kf5-prison, bump min qt5/kf5 deps

* Wed Nov 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Wed Oct 25 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.2-1
- 5.11.2

* Tue Oct 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Wed Oct 11 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.0-1
- 5.11.0

* Mon Oct 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.5-5
- Requires: ksysguardd (#1497831)

* Wed Sep 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.5-4
- rebuild (libqalculate)

* Tue Aug 29 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.5-3
- Restore: Requires: plasma-lookandfeel-fedora

* Thu Aug 24 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.5-2
- drop old stuff
- RPM Bundling Fedora look and feel themes (#1356890)
- BR: cmake(AppstreamQt)

* Thu Aug 24 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.5-1
- 5.10.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.4-1
- 5.10.4

* Tue Jun 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.3-1
- 5.10.3

* Thu Jun 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.2-1
- 5.10.2

* Tue Jun 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1

* Wed May 31 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-2
- Disable bootstrap

* Wed May 31 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Apr 28 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.5.1-1
- 5.9.5.1

* Thu Apr 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.5-3
- pull in upstream 5.9 branch fixes

* Wed Apr 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.5-2
- -doc: use %%find_lang --with-html

* Wed Apr 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.5-1
- 5.9.5

* Thu Mar 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.3-3
- rebuild

* Fri Mar 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.3-2
- fix sddm-breeze (01-breeze-fedora theme)
- bump kf5 dep

* Wed Mar 01 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Sat Feb 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-3
- Requires: kf5-plasma >= %%_kf5_version

* Thu Feb 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-2
- avoid fedora theme crasher (kde#376847)

* Tue Feb 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-1
- 5.8.6

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Mukundan Ragavan <nonamedotc@gmail.com> - 5.8.5-5
- rebuild for libqalculate.so.6

* Mon Jan 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-4
- Obsoletes: kde-runtime-drkonqi (#1415360)

* Thu Jan 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-3
- pull in 5.8 branch fixes

* Mon Jan 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-2
- filter qml/plugin provides

* Wed Dec 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-1
- 5.8.5

* Wed Dec 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.4-2
- rebuild (libqalculate)

* Tue Nov 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.4-1
- 5.8.4

* Tue Nov 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.3-1
- 5.8.3

* Sun Oct 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-4
- sddm-breeze: Requires: qt5-qtquickcontrols instead (kde#371493)

* Sat Oct 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-3
- sddm-breeze: Requires: qt5-qtgraphicaleffects (kde#371493)

* Fri Oct 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-2
- backport candidate systray-icon cpu fix from master (kde#356479)

* Tue Oct 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-1
- 5.8.2

* Tue Oct 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-1
- 5.8.1

* Mon Oct 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-5
- f24-kde-theme/plasma-lookandfeel-fedora noarch
- continue to produce f24-kde-theme on f25+ builds

* Sat Oct 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-4
- plasma-lookandfeel-fedora (f25+)

* Fri Oct 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-3
- sddm-breeze: make 01-breeze-fedora theme use backgrounds/default.png

* Fri Oct 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-2
- pull in upstream branch fixes
- re-order patches so upstream applied first, then downstream

* Thu Sep 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-1
- 5.8.0

* Fri Sep 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.95-2
- -libs: Provides: plasma-packagestructure

* Thu Sep 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.95-1
- 5.7.95

* Fri Sep 16 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.5-2
- restore fedora.twenty.two theme support (#1376102)

* Tue Sep 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.5-1
- 5.7.5

* Fri Sep 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.4-2
- drop support for f22 (plasma theme)

* Tue Aug 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.4-1
- 5.7.4

* Tue Aug 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.3-2
- adapt to upstream looknfeel/default-layout changes
- BR: iso-codes (technically only runtime dep, but can't hurt)

* Tue Aug 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.3-1
- 5.7.3

* Sat Jul 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.2-3
- klipper autostart: OnlyShowIn=KDE (#1361765,kde#366277)

* Mon Jul 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.2-2
- -drkonqi: -Requires: kdialog
- remove BR: qt5-qtbase-private-devel until we can properly document why it is needed

* Tue Jul 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.2-1
- 5.7.2

* Tue Jul 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-3
- BR: qt5-qtbase-private-devel

* Thu Jul 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- BR: kf5-kholidays-devel
- revert recent upstream systray icon resize (kde#365570)

* Tue Jul 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-1
- 5.7.1

* Thu Jun 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-1
- 5.7.0

* Mon Jun 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.95-3
- kwaylad-integration is part of plasma, not kf5

* Sun Jun 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.95-2
- bump Qt5 dep

* Sat Jun 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.95-1
- 5.6.95

* Fri Jun 24 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.5-2
- Suggests: imsettings-qt (#1349743)

* Tue Jun 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.5-1
- 5.6.5

* Sun Jun 05 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-3
- -drkonqi: support 'dnf debuginfo-install' (f24+)
- -drkonqi: Requires: kdialog konsole5 dnf-command(debuginfo-install) (f24+)

* Thu May 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-2
- backport 5.6 branch fixes

* Sat May 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-1
- 5.6.4

* Thu May 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-5
- /etc/pam.d/kde is executable (#1335500)

* Sun May 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-4
- -libs: omit geolocation plugins

* Sat Apr 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-3
- own phonon_platform plugin dir
- -libs: move multilib'able plugins here

* Wed Apr 27 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-2
- Some processes (kuiserver) are left running after exiting KDE (#348123)

* Tue Apr 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-1
- 5.6.3

* Sat Apr 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-1
- 5.6.2

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-2
- de-bootstrap

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-1
- Plasma-5.6.1 (bootstrap)

* Wed Mar 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.5-10
- f24-kde-theme-core: fix conflict with f24-kde-theme
- f24-kde-theme-core: add dep to/from plasma-workspace
- -wayland: s/plasma-workspace/%%name/

* Wed Mar 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.5-9
- enable f24-kde-theme default looknfeel (f24+)

* Mon Mar 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.5-8
- f24-kde-theme-core subpkg (readying for f24-kde-theme)

* Mon Mar 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.5-7
- Provides: f23-kde-theme-core

* Mon Mar 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.5-6
- generic theming for f24+

* Mon Mar 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.5-5
- drop Requires: sddm-breeze for f23+ (workaround for bug #1261034)

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.5-4
- f23+: -Requires: sni-qt kde-platform-plugin (use rich/soft deps elsewhere)

* Mon Mar 07 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.5-3
- backport "Avoid blocking DBus calls in SNI startup" (kde#359611)

* Thu Mar 03 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-2
- Upstream respun tarball

* Wed Mar 02 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Mon Feb 29 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-6
- Requires: iso-codes (digitalclock applet)

* Mon Feb 29 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-5
- pull in some 5.5 branch fixes

* Mon Feb 22 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-4
- -wayland: Requires: xorg-x11-server-Xwayland

* Tue Feb 09 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-3
- backport xembedsniproxy fixes

* Thu Feb 04 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-2
- backport systray applets not shown workaround (kde#352055)

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Mon Jan 25 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.3-6
- pull in upstream fixes (notifications/xembedsniproxy)

* Mon Jan 11 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.3-5
- -wayland: Requires: qt5-qtools (for qdbus-qt5)

* Mon Jan 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.3-4
- startplasmacompositor.patch (#1297418)
- disable bootstrap

* Sun Jan 10 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.3-3
- drop hacked klipper/prison support (until we have kf5-prison available properly)

* Sat Jan 09 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.3-2
- pull in upstream fixes (notifications,xembedsniproxy)

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-2
- use %%majmin_ver_kf5 for most plasma-related deps
- tighten plugin deps using %%_isa
- update URL

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Tue Dec 15 2015 Than Ngo <than@redhat.com> - 5.5.0-5
- enable bootstrap for secondary arch

* Mon Dec 14 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-4
- proper upstream fix for #356415 (review #126331)

* Sun Dec 13 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.0-3
- latest upstream fixes (#1291100)
- revert commit causing regression'ish kde #356415
- drop kwayland-integration from main pkg (only in -wayland subpkg)

* Sat Dec 05 2015 Daniel Vrátil <dvraitl@fedoraproject.org> - 5.5.0-2
- remove version dependency on oxygen-fonts, because it's not being released anymore

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Tue Nov 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.3-4
- Unhelpful summary/description for drkonqi packages (#1282810)

* Mon Nov 16 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.3-3
- Fix changing of visibility for system tray entries
  Resolves: kdebz#355404

* Wed Nov 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.3-2
- refresh xembedsniproxy support (#1280457)

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Tue Nov 03 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-8
- make klipper/prison support f24+ only (for now)
- backport xembed-sni-proxy

* Tue Oct 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-7
- klipper: prison (qrcode) support

* Wed Oct 14 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-6
- rev startkde.patch drop dbus launch (kde#352251)

* Mon Oct 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-5
- Obsoletes: kde-runtime-kuiserver (#1249157), Provides: kuiserver

* Mon Oct 05 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-4
- startkde: don't try to source things in a subshell, don't munge XDG_DATA_DIRS needlessly

* Sun Oct 04 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-3
- consistently use %%{majmin_ver_kf5} macro for other plasma5-related deps

* Sat Oct 03 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-2
- .spec cosmetics, use %%license
- -common, -drkonqi, -libs, libkworkspace5 subpkgs
- -geolocation subpkg (#1222097)
- -drkonqi: include installdbgsymbols.sh

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-6
- try tightened plasmashell dep (loosened in plasma-desktop)

* Fri Sep 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-5
- relax kf5-kxmlrpcclient dep (and drop related hacks), tighten khotkeys

* Tue Sep 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-4
- Requires: sddm-breeze unconditionally (#1260394)

* Sat Sep 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-3
- tighten build deps

* Sat Sep 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- Requires: sddm-breeze, (hopefully) temporary workaround for dnf Obsoletes bug (#1260394, f22)

* Fri Sep 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-1
- de-bootstrap

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-0.1
- 5.4.1, enable bootstrap

* Fri Sep 04 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-7
- Conflicts: kio-extras < 5.4.0

* Wed Sep 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-6.1
- make plasma-pa f23+ only

* Tue Sep 01 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-6
- Try rebuilding against new baloo

* Wed Aug 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-5
- versioned kf5-related build deps

* Tue Aug 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-4
- Disable bootstrap

* Tue Aug 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-3
- Re-enable plasma-pa and kwayland-integration dependencies

* Sat Aug 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-2
- Temporarily disable plasma-pa and kwayland-integration until the packages are reviewed

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-4
- use patch for startkde.cmake, remove redundant prison dependency

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Tue Aug 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-11
- Provides: f23-kde-theme-core (and f22-kde-theme-core)
- default_lookandfeel org.fedoraproject.fedora.twenty.three (f23+)

* Thu Aug 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-10
- prep fedora.twenty.three plasma theme

* Thu Aug 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-9
- make sddm-breeze noarch (#1250204)

* Thu Aug 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-8
- sddm-breeze subpkg, userlist variant for bz #1250204

* Wed Aug 05 2015 Jonathan Wakely <jwakely@redhat.com> 5.3.2-7
- Rebuilt for Boost 1.58

* Fri Jul 31 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-6
- Requires: kde-platform-plugin

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 5.3.2-4
- rebuild for Boost 1.58

* Thu Jul 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-3
- .spec cosmetics
- port selinux/drkonqi scriptlet (from kde-runtime)
- own /usr/share/drkonqi/
- %%config(noreplace) pam

* Fri Jun 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-2
- Make the Requires: plasmashell unversioned to break circular dependency during update

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Sat Jun 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-5
- shutdown scripts are not executed (#1234059)

* Thu Jun 18 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-4
- startkde.cmake: sync ScaleFactor changes, drop QT_PLUGIN_PATH munging (#1233298)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.1-2
- use %%{?kf5_kinit_requires}
- Requires: kf5-kactivities
- doc: make noarch, %%lang'ify

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Wed May 20 2015 Jan Grulich <jgrulich@redhat.com> - 5.3.0-8
- apply the new patch for update scripts execution

* Wed May 20 2015 Jan Grulich <jgrulich@redhat.com> - 5.3.0-7
- process update scripts after first initialization

* Tue May 19 2015 Jan Grulich <jgrulich@redhat.com> - 5.3.0-6
- copy Breeze look-and-feel package also as Fedora Twenty Two look-and-feel package

* Mon May 18 2015 Jan Grulich <jgrulich@redhat.com> - 5.3.0-5
- set default look and feel theme to Fedora Twenty Two

* Tue May 05 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-4
- backport patch form kde-workspace to add Konsole into shell context menu
- re-enable fix-update-scripts.patch

* Wed Apr 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-3
- Disable bootstrap

* Wed Apr 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-2
- Requires plasmashell (virtual provides for packages that provide Plasma shells, like plasma-desktop)

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Wed Apr 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-6
- Requires: kde-settings-plasma (#1197709)

* Sat Apr 04 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-5
- conflicts with kf5-kxmlrpcclient (#1208947)

* Tue Mar 31 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-4
- Requires: khotkeys (#1207079)

* Mon Mar 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-3
- backport fix for update scripts

* Wed Mar 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-2
- Lockscreen: Password field does not have focus (kde#344823)

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Mon Mar 16 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-6
- revert Requires: plasma-desktop (dep should be the other way around)
- drop Obsoletes: kde-workspace (leave for plasma-desktop)
- Requires: polkit-kde

* Sun Mar 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-5
- Requires: -sddm (#1201034), +plasma-desktop

* Fri Mar 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-4
- rebuild (gpsd)

* Tue Mar 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- use our own startkde.cmake

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-8
- (Build)Requires: kf5-kglobalaccel(-devel) >= 5.7
- drop ksyncdbusenv.patch workaround
- .spec cosmetics

* Wed Feb 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-7
- "Could not sync environment to dbus." (startkde) (#1191171)

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-6
- Revert the previous change

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-5
- Provides/Obsoletes: kdeclassic-cursor-theme

* Sun Feb 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-4
- Requires: powerdevil, oxygen-sound-theme

* Thu Jan 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-3
- Requires: plasma-milou (for krunner)

* Thu Jan 29 2015 Dan Horák <dan[at]danny.cz> - 5.2.0-2
- no FireWire on s390(x)

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-3.beta
- Requires: kf5-frameworkintegration (provides platformtheme plugin)

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- BR: kf5-kscreen-devel (renamed)

* Tue Jan 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-5
- Add upstream patch to make ksyncdbusenv work with dbus-1.8.14

* Fri Jan 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-4
- Requires: qt5-qttools (for dbus-qt5)

* Wed Jan 07 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.2-3
- Omit "5" from pkg summary
  Drop config macro for files installed to /etc/xdg
  Move /usr/share/dbus-1/interfaces/*.xml stuff to main package
  Validate .desktop files
  look for qdbus-qt5 in startkde instead of qdbus

* Mon Jan 05 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- add upstream patch to fix black screen on start

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-1
- Plasma 5.1.2

* Fri Nov 28 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-2
- Apply upstream patch to build against new version of KScreen

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Tue Sep 02 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-3
- Make sure we get oxygen-icon-theme and oxyge-icons installed

* Fri Aug 29 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-2
- Add upstream patch to fix generated path in plasma.desktop

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-7
- Add more Obsoletes to make upgrade from KDE 4 smooth
- Add sni-qt to Requires so that Qt 4 apps are working with Plasma 5 systray
- Requires kde-settings

* Thu Jul 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-4
- Add patch to fix build-time generated paths

* Thu Jul 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-3
- Use relative BIN_INSTALL_DIR so that built-in paths are correctly generated

* Thu Jul 24 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Fix /usr//usr/ in generated files

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Tue May 20 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-6.20140519gita85f5bc
- Add LIBEXEC_PATH to kde5 profile to fix drkonqi lookup
- Fix install

* Mon May 19 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-3.20140519gita85f5bc
- Update to latest git snapshot
- Add PAM file
- Add profile.d entry

* Fri Apr 25 2014 Daniel Vrátil <dvratil@redhat.com> - 4.95.0-1.20140425git7c97c92
- Initial version of kde5-plasma-workspace
