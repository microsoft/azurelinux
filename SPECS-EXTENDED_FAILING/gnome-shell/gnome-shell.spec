Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           gnome-shell
Version:        3.36.9
Release:        5%{?dist}
Summary:        Window management and application launching for GNOME

License:        GPLv2+
Provides:       desktop-notification-daemon
URL:            https://wiki.gnome.org/Projects/GnomeShell
#VCS:           git:git://git.gnome.org/gnome-shell
Source0:        http://download.gnome.org/sources/gnome-shell/3.36/%{name}-%{version}.tar.xz

# Replace Epiphany with Firefox in the default favourite apps list
Patch1: gnome-shell-favourite-apps-firefox.patch

# Implement https://wiki.gnome.org/Design/OS/BootOptions
# This should go upstream once systemd has a generic interface for this
Patch2: 0001-endSessionDialog-Immediately-add-buttons-to-the-dial.patch
Patch3: 0002-endSessionDialog-Support-rebooting-into-the-bootload.patch

%define eds_version 3.33.1
%define gnome_desktop_version 3.35.91
%define glib2_version 2.56.0
%define gobject_introspection_version 1.49.1
%define gjs_version 1.57.3
%define gtk3_version 3.15.0
%define mutter_version 3.36.0
%define polkit_version 0.100
%define gsettings_desktop_schemas_version 3.33.1
%define ibus_version 1.5.2
%define gnome_bluetooth_version 3.9.0
%define gstreamer_version 1.4.5

BuildRequires:  asciidoc
BuildRequires:  bash-completion
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  git
BuildRequires:  ibus-devel >= %{ibus_version}
BuildRequires:  chrpath
BuildRequires:  desktop-file-utils
BuildRequires:  evolution-data-server-devel >= %{eds_version}
BuildRequires:  gcr-devel
BuildRequires:  gjs-devel >= %{gjs_version}
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gnome-autoar-devel
BuildRequires:  pkgconfig(gnome-desktop-3.0)
BuildRequires:  gobject-introspection >= %{gobject_introspection_version}
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  polkit-devel >= %{polkit_version}
BuildRequires:  startup-notification-devel
BuildRequires:  systemd-devel
# for theme generation
BuildRequires:  sassc
# for screencast recorder functionality
BuildRequires:  gstreamer1-devel >= %{gstreamer_version}
BuildRequires:  gtk3-devel >= %{gtk3_version}
BuildRequires:  gettext >= 0.19.6
BuildRequires:  libcanberra-devel
BuildRequires:  python3

# for barriers
BuildRequires:  libXfixes-devel >= 5.0
# used in unused BigThemeImage
BuildRequires:  librsvg2-devel
BuildRequires:  mutter-devel >= %{mutter_version}
BuildRequires:  pulseaudio-libs-devel
%ifnarch s390 s390x ppc ppc64 ppc64p7
BuildRequires:  gnome-bluetooth-libs-devel >= %{gnome_bluetooth_version}
%endif
# Bootstrap requirements
BuildRequires: gtk-doc
%ifnarch s390 s390x
Requires:       gnome-bluetooth%{?_isa} >= %{gnome_bluetooth_version}
%endif
Requires:       gnome-desktop3%{?_isa} >= %{gnome_desktop_version}
%if 0%{?rhel} != 7
# Disabled on RHEL 7 to allow logging into KDE session by default
Requires:       gnome-session-xsession
%endif
# wrapper script uses to restart old GNOME session if run --replace
# from the command line
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}
Requires:       gjs%{?_isa} >= %{gjs_version}
Requires:       gtk3%{?_isa} >= %{gtk3_version}
# needed for loading SVG's via gdk-pixbuf
Requires:       librsvg2%{?_isa}
Requires:       mutter%{?_isa} >= %{mutter_version}
Requires:       upower%{?_isa}
Requires:       polkit%{?_isa} >= %{polkit_version}
Requires:       gnome-desktop3%{?_isa} >= %{gnome_desktop_version}
Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires:       gstreamer1%{?_isa} >= %{gstreamer_version}
# needed for schemas
Requires:       at-spi2-atk%{?_isa}
# needed for on-screen keyboard
Requires:       ibus%{?_isa} >= %{ibus_version}
# needed for the user menu
Requires:       accountsservice-libs%{?_isa}
Requires:       gdm-libs%{?_isa}
# needed for settings items in menus
Requires:       control-center
# needed by some utilities
Requires:       python3%{_isa}
# needed for the dual-GPU launch menu
Requires:       switcheroo-control
# needed for clocks/weather integration
Requires:       geoclue2-libs%{?_isa}
Requires:       libgweather%{?_isa}
# Needed for launching flatpak apps etc
Requires:       xdg-desktop-portal-gtk

%if 0%{?rhel}
# In Fedora, fedora-obsolete-packages obsoletes caribou
Obsoletes:      caribou < 0.4.21-10
Obsoletes:      caribou-antler < 0.4.21-10
Obsoletes:      caribou-devel < 0.4.21-10
Obsoletes:      caribou-gtk2-module < 0.4.21-10
Obsoletes:      caribou-gtk3-module < 0.4.21-10
Obsoletes:      python-caribou < 0.4.21-10
Obsoletes:      python2-caribou < 0.4.21-10
Obsoletes:      python3-caribou < 0.4.21-10
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1740897
Conflicts:      gnome-shell-extension-background-logo < 3.34.0

%description
GNOME Shell provides core user interface functions for the GNOME 3 desktop,
like switching to windows and launching applications. GNOME Shell takes
advantage of the capabilities of modern graphics hardware and introduces
innovative user interface concepts to provide a visually attractive and
easy to use experience.

%prep
%autosetup -S git

%build
%meson -Dextensions_app=false
%meson_build

%install
%meson_install

# Create empty directories where other packages can drop extensions
mkdir -p %{buildroot}%{_datadir}/gnome-shell/extensions
mkdir -p %{buildroot}%{_datadir}/gnome-shell/search-providers

%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Shell.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/evolution-calendar.desktop

%files -f %{name}.lang
%license COPYING
%doc README.md
%caps(cap_sys_nice+ep) %{_bindir}/gnome-shell
%{_bindir}/gnome-extensions
%{_bindir}/gnome-shell-extension-prefs
%{_bindir}/gnome-shell-extension-tool
%{_bindir}/gnome-shell-perf-tool
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/glib-2.0/schemas/00_org.gnome.shell.gschema.override
%{_datadir}/applications/org.gnome.Shell.desktop
%{_datadir}/applications/evolution-calendar.desktop
%{_datadir}/applications/org.gnome.Shell.Extensions.desktop
%{_datadir}/applications/org.gnome.Shell.PortalHelper.desktop
%{_datadir}/bash-completion/completions/gnome-extensions
%{_datadir}/gnome-control-center/keybindings/50-gnome-shell-system.xml
%{_datadir}/gnome-shell/
%{_datadir}/dbus-1/services/org.gnome.Shell.CalendarServer.service
%{_datadir}/dbus-1/services/org.gnome.Shell.Extensions.service
%{_datadir}/dbus-1/services/org.gnome.Shell.HotplugSniffer.service
%{_datadir}/dbus-1/services/org.gnome.Shell.Notifications.service
%{_datadir}/dbus-1/services/org.gnome.Shell.PortalHelper.service
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Extensions.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Introspect.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.PadOsd.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Screencast.xml
%{_datadir}/dbus-1/interfaces/org.gnome.Shell.Screenshot.xml
%{_datadir}/dbus-1/interfaces/org.gnome.ShellSearchProvider.xml
%{_datadir}/dbus-1/interfaces/org.gnome.ShellSearchProvider2.xml
%{_datadir}/icons/hicolor/scalable/apps/org.gnome.Shell.Extensions.svg
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Shell.Extensions-symbolic.svg
%{_userunitdir}/gnome-shell-disable-extensions.service
%{_userunitdir}/gnome-shell-wayland.service
%{_userunitdir}/gnome-shell-wayland.target
%{_userunitdir}/gnome-shell-x11.service
%{_userunitdir}/gnome-shell-x11.target
%{_sysconfdir}/xdg/autostart/gnome-shell-overrides-migration.desktop
# Co own directory instead of pulling in xdg-desktop-portal - we
# are providing a backend to the portal, not depending on it
%dir %{_datadir}/xdg-desktop-portal/portals/
%{_datadir}/xdg-desktop-portal/portals/gnome-shell.portal
%{_libdir}/gnome-shell/
%{_libexecdir}/gnome-shell-calendar-server
%{_libexecdir}/gnome-shell-perf-helper
%{_libexecdir}/gnome-shell-hotplug-sniffer
%{_libexecdir}/gnome-shell-portal-helper
%{_libexecdir}/gnome-shell-overrides-migration.sh
# Co own these directories instead of pulling in GConf
# after all, we are trying to get rid of GConf with these files
%dir %{_datadir}/GConf
%dir %{_datadir}/GConf/gsettings
%{_datadir}/GConf/gsettings/gnome-shell-overrides.convert
%{_mandir}/man1/gnome-extensions.1*
%{_mandir}/man1/gnome-shell.1*

%changelog
* Thu Feb 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.36.9-5
- Removing dependency on 'bolt'.

* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.36.9-4
- Removing epoch.

* Fri Jan 28 2022 Thomas Crain <thcrain@microsoft.com> - 3.36.9-3
- Remove NetworkManger-libnm-devel BR because CBL-Mariner is not providing NetworkManager
- License verified

* Sat Jul 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.36.9-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing run-time dependency on 'libnma' (GUI library for 'NetworkManager')
  because CBL-Mariner is not providing 'NetworkManager'.

* Mon Mar 15 2021 Florian Müllner <fmuellner@redhat.com> - 3.36.9-1
- Update to 3.36.9

* Thu Jan 14 2021 Florian Müllner <fmuellner@redhat.com> - 3.36.8-1
- Update to 3.36.8

* Wed Oct 07 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.7-1
- Update to 3.36.7

* Mon Sep 07 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.6-1
- Update to 3.36.6

* Tue Aug 11 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.5-1
- Update to 3.36.5

* Tue Jul 07 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.4-1
- Update to 3.36.4

* Wed Jun 03 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.3-1
- Update to 3.36.3

* Wed May 20 2020 Stephen Gallagher <sgallagh@redhat.com> - 3.36.2-3
- Fix crashes when locking the screen while certain extensions are active
- Resolves: rhbz#1817082

* Fri May 01 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.2-2
- Fix a crash

* Thu Apr 30 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.2-1
- Update to 3.36.2

* Mon Apr 13 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.1-4
- Fix translated folder names
  Resolves: #1822336

* Tue Apr 07 2020 Florian Müllner <fmuellner@redhat.com - 3.36.1-3
- Remove obsolete libcroco require
- Update files section

* Tue Apr 07 2020 Jonas Ådahl <jadahl@redhat.com> - 3.36.1-3
- Backport fixes from gnome-3-36

* Tue Mar 31 2020 Jonas Ådahl <jadahl@redhat.com> - 3.36.1-2
- Backport fixup for spring animation fix

* Tue Mar 31 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.1-1
- Update to 3.36.1
- Remove gnome-extensions-app subpackage (will move to a separate .spec)

* Wed Mar 25 2020 Ray Strode <rstrode@redhat.com> - 3.36.0-4
- Clear environment on logout
  Fixes log in to Xorg right after log out from wayland
  Resolves: #1815487

* Wed Mar 11 2020 Adam Williamson <awilliam@redhat.com> - 3.36.0-3
- Backport fix for input method preedit issue (MR #1084)

* Tue Mar 10 2020 Adam Williamson <awilliam@redhat.com> - 3.36.0-2
- Backport fix for ibus failing to start automatically (MR #1080)

* Sat Mar 07 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Sun Mar 01 2020 Florian Müllner <fmuellner@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Tue Feb 18 2020 Florian Müllner <fmuellner@redhat.com> - 3.35.91-1
- Update to 3.35.91

* Fri Feb 07 2020 Kalev Lember <klember@redhat.com> - 3.35.90-2
- Adjust the favorites patch to include the apps we install by default

* Thu Feb 06 2020 Florian Müllner <fmuellner@redhat.com> - 3.35.90-1
- Update to 3.35.90

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Kalev Lember <klember@redhat.com> - 3.35.3-2
- Rebuilt for libgnome-desktop soname bump

* Sun Jan 05 2020 Florian Müllner <fmuellner@redhat.com> - 3.35.3-2
- Update to 3.35.3

* Wed Dec 11 2019 Florian Müllner <fmuellner@redhat.com> - 3.35.2-1
- Udpate to 3.35.2

* Sat Oct 12 2019 Florian Müllner <fmuellner@redhat.com> - 3.35.1-1
- Update to 3.35.1

* Sat Oct 12 2019 Adam Williamson <awilliam@redhat.com> - 3.34.1-2
- Backport MR #754 to fix #1749433

* Wed Oct 09 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Tue Sep 24 2019 Debarshi Ray <rishi@fedorapeople.org> - 3.34.0-3
- Stop NOTIFY_SOCKET from leaking into the GNOME environment

* Fri Sep 20 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.0-2
- Fix disappearing icons in frequent view

* Mon Sep 09 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Thu Sep 05 2019 Kalev Lember <klember@redhat.com> - 3.33.92-1
- Update to 3.33.92

* Mon Aug 26 2019 Kalev Lember <klember@redhat.com> - 3.33.91-1
- Update to 3.33.91

* Fri Aug 23 2019 Adam Williamson <awilliam@redhat.com> - 3.33.90-2
- Revert commit that causes #1740897 (overview type-to-search bug)
  Resolves: #1740897

* Sat Aug 10 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.4-1
- Update to 3.33.4

* Mon Jun 24 2019 Florian Mülllner <fmuellner@redhat.com> - 3.33.3-1
- Update to 3.33.3

* Wed May 22 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.2-1
- Update to 3.33.2

* Wed May 22 2019 Kalev Lember <klember@redhat.com> - 3.33.1-2
- Rebuild for libecal-2.0

* Tue May 14 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.1-1
- Update to 3.33.1

* Wed Apr 17 2019 Florian Müllner <fmuellner@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Wed Apr 17 2019 Adam Williamson <awilliam@redhat.com> - 3.32.0-3
- Backport MR #463 and MR #494 to fix a couple of bugs
  Resolves: #1696270
  Resolves: #1690429

* Sat Mar 23 2019 Phil Wyett <philwyett@kathenas.org> - 3.32.0-2
- Update source URL
- Add gcc BuildRequires
- Update versions required for gjs and mutter

* Tue Mar 12 2019 Florian Müllner <fmuellner@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Tue Mar 05 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Thu Feb 21 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.91-1
- Update to 3.31.91

* Mon Feb 11 2019 Adam Williamson <awilliam@redhat.com> - 3.31.90-2
- Backport MR #402 to fix missing logo on login screen

* Thu Feb 07 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.4-1
- Update to 3.31.4

* Fri Dec 14 2018 Adam Williamson <awilliam@redhat.com> - 3.31.2-3
- Backport several bugfix commits from current git master

* Fri Nov 30 2018 Adam Williamson <awilliam@redhat.com> - 3.31.2-2
- Backport PR #293 to fix 'empty input method indicator' bug

* Wed Nov 14 2018 Florian Müllner <fmuellner@redhat.com> - 3.31.2-1
- Update to 3.31.2

* Mon Nov 12 2018 Mohan Boddu <mboddu@bhujji.com> - 3.30.1-3
- Rebuilt for evolution-data-server soname bump

* Tue Oct 23 2018 Jonas Ådahl <jadahl@redhat.com> - 3.30.1-2
- Backport keyboard layout change fixes (rhbz#1637418)

* Mon Oct 08 2018 Florian Müllner <fmuellner@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Thu Sep 27 2018 Hans de Goede <hdegoede@redhat.com> - 3.30.0-9
- Add downstream patches implementing the "Boot Options" menu from:
  https://wiki.gnome.org/Design/OS/BootOptions

* Sat Sep 22 2018 Adam Williamson <awilliam@redhat.com> - 3.30.0-8
- Backport fix for IBus type issue (GGO MR #228)

* Wed Sep 19 2018 Adam Williamson <awilliam@redhat.com> - 3.30.0-7
- Replace dnd fix from -5 with upstream version (GGO MR #209)
- Fix a window destroy crash which can occur with new gjs (GGO #539)
- Fix a window menu issue on multi-monitor systems (GGO MR #227)
- Fix hover and active states for some buttons (GGO #523)

* Wed Sep 19 2018 Adam Williamson <awilliam@redhat.com> - 3.30.0-6
- Fix missing key description in ssh key unlock prompt (GGO #574)

* Wed Sep 19 2018 Ray Strode <rstrode@redhat.com> - 3.30.0-5
- Fix lock up when dropping icon on dash
  Resolves: #1630134

* Tue Sep 18 2018 Adam Williamson <awilliam@redhat.com> - 3.30.0-4
- Fix connecting to wifi from user menu (RHBZ #1628263)

* Sat Sep 15 2018 Adam Williamson <awilliam@redhat.com> - 3.30.0-3
- Backport fix for GGO #140 from upstream master

* Thu Sep 13 2018 Kalev Lember <klember@redhat.com> - 3.30.0-2
- Require xdg-desktop-portal-gtk

* Tue Sep 04 2018 Florian Müllner <fmuellner@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Wed Aug 29 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.92-1
- Update to 3.29.92

* Mon Aug 20 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.91-1
- Update to 3.29.91

* Thu Aug 09 2018 Debarshi Ray <rishi@fedoraproject.org> - 3.29.90-2
- Remove telepathy-logger and telepathy-glib runtime dependencies

* Wed Aug 01 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.90-1
- Update to 3.29.90

* Wed Jul 18 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.4-1
- Update to 3.29.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.29.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 24 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.2-1
- Update to 3.29.2

* Wed May 09 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.1-3
- Fix automatic connection to wireless networks without stored secrets

* Sun Apr 29 2018 Adam Williamson <awilliam@redhat.com> - 3.29.1-2
- Backport fix for password entry modifier key issues (#1569211)

* Wed Apr 25 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.1-1
- Update to 3.29.1

* Tue Apr 24 2018 Ray Strode <rstrode@redhat.com> - 3.28.1-2
- pull polkit cancel lock up from upstream
  Resolves: #1568213

* Fri Apr 13 2018 Florian Müllner <fmuellner@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Mon Mar 12 2018 Florian Müllner <fmuellner@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Florian Müllner <fmuellner@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Thu Feb 22 2018 Lubomir Rintel <lkundrak@v3.sk> - 3.27.91-2
- Replace libnm-gtk with libnma

* Wed Feb 21 2018 Florian Müllner <fmuellner@redhat.com> - 3.27.91-1
- Update to 3.27.91

* Wed Feb 07 2018 Kalev Lember <klember@redhat.com> - 3.27.1-5
- Rebuilt for evolution-data-server soname bump

* Mon Jan 22 2018 Adam Williamson <awilliam@redhat.com> - 3.27.1-4
- Backport fix for crasher bug BGO #788931 (#1469129)

* Tue Dec 19 2017 Kalev Lember <klember@redhat.com> - 3.27.1-3
- Explicitly require libnm-gtk (#1509496)

* Wed Nov 08 2017 Milan Crha <mcrha@redhat.com> - 3.27.1-2
- Rebuild for newer libical

* Tue Oct 17 2017 Florian Müllner <fmuellner@redhat.com> - 3.27.1-1
- Update to 3.27.1

* Wed Oct 04 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Thu Sep 21 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-2
- Fix crash on fast status icon remapping

* Tue Sep 12 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Tue Aug 22 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Fri Aug 11 2017 Kevin Fenzi <kevin@scrye.com> - 3.25.90-2
- Rebuild with older working rpm

* Thu Aug 10 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Wed Jun 21 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.3-1
- Update to 3.25.3

* Thu May 25 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.2-1
- Update to 3.25.2

* Thu Apr 27 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.1-1
- Update to 3.25.1

* Tue Apr 11 2017 Florian Müllner <fmuellner@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Mon Mar 20 2017 Florian Müllner <fmuellner@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.23.92-2
- Fix wrong runtime requirements

* Tue Mar 14 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Wed Mar 01 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Thu Feb 16 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Tue Feb 14 2017 Richard Hughes <rhughes@redhat.com> - 3.23.3-1
- Update to 3.23.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.23.2-3
- Rebuild for Python 3.6

* Tue Dec  6 2016 Rui Matos <rmatos@redhat.com> - 3.23.2-2
- Tighten mutter version dependency for plugin API changes
  Resolves: #1401886

* Wed Nov 23 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Sun Oct 30 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.1-1
- Update to 3.23.1

* Fri Oct 21 2016 Bastien Nocera <bnocera@redhat.com> - 3.22.1-2
- Add patches to allow launching on discrete GPU when available

* Tue Oct 11 2016 Florian Müllner <fmuellner@redhat.com> - 3.22.1
- Update to 3.22.1

* Mon Sep 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.22.0
- Update to 3.22.0

* Tue Sep 13 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.92
- Update to 3.21.92

* Fri Sep 09 2016 Kalev Lember <klember@redhat.com> - 3.21.91-2
- Drop libgsystem dependency

* Tue Aug 30 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.91
- Update to 3.21.91

* Sat Aug 20 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.90.1-1
- Update to 3.21.90.1
  (Fixes a corrupt .desktop file that made it from the build directory into
   the 3.21.90 tarball)

* Fri Aug 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Wed Jul 20 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Mon Jul 18 2016 Milan Crha <mcrha@redhat.com> - 3.21.3-2
- Rebuild for newer evolution-data-server

* Tue Jun 21 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Tue Jun 21 2016 Milan Crha <mcrha@redhat.com> - 3.21.2-2
- Rebuild for newer evolution-data-server

* Thu May 26 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Fri Apr 29 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 3.20.1-2
- rebuild for ICU 57.1

* Wed Apr 13 2016 Florian Müllner <fmuellner@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Florian Müllner <fmuellner@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Wed Mar 16 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Thu Mar 03 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Fri Feb 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Tue Feb 16 2016 Milan Crha <mcrha@redhat.com> - 3.19.4-3
- Rebuild for newer evolution-data-server

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Mon Jan 18 2016 David Tardon <dtardon@redhat.com> - 3.19.3-2
- rebuild for libical 2.0.0

* Thu Dec 17 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Tue Dec 01 2015 Kalev Lember <klember@redhat.com> - 3.19.2-2
- Bump gsettings-desktop-schemas dep to 3.19.2

* Wed Nov 25 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Tue Nov 10 2015 Ray Strode <rstrode@redhat.com> 3.19.1-3.20151110
- Update to git snapshot

* Sun Nov 01 2015 Kalev Lember <klember@redhat.com> - 3.19.1-2
- Fix gnome-shell crashing in gdm mode (#1276833)

* Thu Oct 29 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.1-1
- Update to 3.19.1

* Thu Oct 15 2015 Florian Müllner <fmuellner@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Florian Müllner <fmuellner@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Wed Sep 16 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Thu Sep 03 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Thu Aug 20 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 3.17.4-2
- Create empty directories for extensions and search providers
- Move desktop file validation to %%check section
- Use make_install macro

* Thu Jul 23 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.4-1
- Update to 3.17.4

* Wed Jul 22 2015 Milan Crha <mcrha@redhat.com> - 3.17.3-3
- Rebuild for newer evolution-data-server

* Sat Jul 04 2015 Kalev Lember <klember@redhat.com> - 3.17.3-2
- Require gobject-introspection 1.45.3

* Thu Jul 02 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.2-1
- Update to 3.17.2

* Thu Apr 30 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.1-1
- Update to 3.17.1

* Tue Apr 28 2015 Milan Crha <mcrha@redhat.com> - 3.16.1-2
- Rebuild for newer evolution-data-server

* Tue Apr 14 2015 Florian Müllner <fmuellner@redhat.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Florian Müllner <fmuellner@redhat.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-2
- Update minimum dep versions
- Use license macro for the COPYING file

* Tue Mar 17 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.92-1
- Update to 3.15.92

* Tue Mar 17 2015 Ray Strode <rstrode@redhat.com> 3.15.91-2
- Drop dep on NetworkManager-config-connectivity-fedora
  It's already required by fedora-release-workstation

* Wed Mar 04 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.91-1
- Update to 3.15.91

* Fri Feb 20 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Tue Feb 17 2015 Milan Crha <mcrha@redhat.com> - 3.15.4-2
- Rebuild against newer evolution-data-server

* Wed Jan 21 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Fri Dec 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.3-1
- Update to 3.15.3

* Thu Nov 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.2-1
- Update to 3.15.2

* Thu Oct 30 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.1-1
- Update to 3.15.1

* Tue Oct 14 2014 Florian Müllner <fmuellner@redhat.com> - 3.14.1-1
- Update to 3.14.1

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Drop unused gnome-menus dependency

* Mon Sep 22 2014 Florian Müllner <fmuellner@redhat.com> - 3.14.0-1
- Update to 3.14.0

* Wed Sep 17 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.92-1
- Update to 3.13.92

* Wed Sep 03 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.91-1
- Update to 3.13.91

* Wed Aug 20 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 31 2014 Milan Crha <mcrha@redhat.com> - 3.13.4-3
- Rebuild against newer evolution-data-server

* Mon Jul 28 2014 Adel Gadllah <adel.gadllah@gmail.com> - 3.13.4-2
- Require NetworkManager-config-connectivity-fedora

* Wed Jul 23 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.4-1
- Update to 3.13.4

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-2
- Rebuilt for gobject-introspection 1.41.4

* Fri Jun 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- New gobject-introspection has been built, drop the last patch again

* Wed Jun 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- Revert annotation updates until we get a new gobject-introspection build

* Wed Jun 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.2-1
- Update to 3.13.2

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Pull in libgsystem

* Wed Apr 30 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.1-1
- Update to 3.13.1

* Tue Apr 15 2014 Florian Müllner <fmuellner@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Update dep versions

* Tue Mar 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Wed Mar 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Wed Mar 12 2014 Adam Williamson <awilliam@redhat.com> - 3.11.91-2
- update to final revision of background bug fix from upstream (BGO #722149)

* Thu Mar 06 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Mon Mar 03 2014 Adam Williamson <awilliam@redhat.com> - 3.11.90-5
- backport fixes to fix drag-and-drop workspace creation (BGO #724686)

* Wed Feb 26 2014 Adam Williamson <awilliam@redhat.com> - 3.11.90-4
- backport a couple of bugfixes from BGO for things that annoy me

* Sat Feb 22 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.90-3
- Add dependency on gnome-control-center - several panels are referenced
  by a number of menu items

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.90-2
- Rebuilt for cogl soname bump

* Thu Feb 20 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 3.11.5-3
- Rebuild for libevdev soname bump

* Wed Feb 05 2014 Adam Williamson <awilliam@redhat.com> - 3.11.5-2
- build against new gjs (and hence mozjs24)

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Mon Feb 03 2014 Milan Crha <mcrha@redhat.com> - 3.11.4-2
- Rebuild against newer evolution-data-server

* Thu Jan 16 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Jan 14 2014 Milan Crha <mcrha@redhat.com> - 3.11.3-2
- Rebuild against newer evolution-data-server

* Fri Dec 20 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Thu Nov 21 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-3
- Rebuild for new libical (RH bug #1023020)

* Tue Nov 19 2013 Milan Crha <mcrha@redhat.com> - 3.11.2-2
- Rebuild against newer evolution-data-server

* Wed Nov 13 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Wed Oct 30 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Fri Oct 25 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.1-2
- Rebuild for new e-d-s

* Tue Oct 15 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0.1-1
- Update to 3.10.0.1

* Tue Sep 24 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.92-3
- Build against mutter-wayland

* Tue Sep 17 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.90-1
- Update to 3.9.90

* Mon Aug 19 2013 Adam Williamson <awilliam@redhat.com> - 3.9.5-3
- Rebuild for new e-d-s

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-2
- Drop the bluez revert patch as we now have new enough gnome-bluetooth

* Tue Jul 30 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.5
- Update to 3.9.5

* Mon Jul 29 2013 Adam Williamson <awilliam@redhat.com> - 3.9.4-2
- rebuild against updated evolution-data-server

* Wed Jul 10 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.4-1
- Update to 3.9.4

* Wed Jul 10 2013 Milan Crha <mcrha@redhat.com> - 3.9.3-3
- Rebuild against newer evolution-data-server

* Wed Jul 10 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.3-2
- Add a downstream patch to revert back to bluez 4

* Tue Jun 18 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.3-1
- Update to 3.9.3

* Tue May 28 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Sat May 25 2013 Rex Dieter <rdieter@fedoraproject.org> 3.9.1-3
- rebuild (libical)

* Wed May 01 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-2
- Add missing telepathy-logger runtime dep
- Depend on gnome-session-xsession so that it gets pulled in for
  typical GNOME installs

* Wed May 01 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Tue Apr 16 2013 Florian Müllner <fmuellner@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Thu Mar 28 2013 Adel Gadllah <adel.gadllah@gmail.com> - 3.8.0.1-2
- Ship the perf tool

* Wed Mar 27 2013 Ray Strode <rstrode@redhat.com> - 3.8.0.1-1
- Update to 3.8.0.1

* Tue Mar 26 2013 Florian Müllner <fmuellner@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Tue Mar 05 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 20 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-2
- Rebuilt for libgcr soname bump

* Wed Feb 06 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.7.4.1-2
- Rebuild for new cogl

* Thu Jan 17 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.4.1-1
- Update to 3.7.4.1

* Tue Jan 15 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Wed Jan 09 2013 Richard Hughes <hughsient@gmail.com> - 3.7.3.1-1
- Update to 3.7.3.1

* Tue Dec 18 2012 Florian Müllner <fmuellner@redhat.com> 3.7.3-1
- Update to 3.7.3

* Mon Dec 17 2012 Adam Jackson <ajax@redhat.com> 3.7.2-3
- Also don't mangle rpath on power

* Mon Dec 10 2012 Adam Jackson <ajax@redhat.com> 3.7.2-2
- Disable bluetooth on power

* Mon Nov 19 2012 Florian Müllner <fmuellner@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Tue Nov 13 2012 Dan Horák <dan[at]danny.cz> - 3.7.1-2
- don't Require: gnome-bluetooth on s390(x)

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Wed Oct 31 2012 Brian Pepple <bpepple@fedoraproject.org> - 3.6.1-5
- Rebuild against latest telepathy-logger

* Thu Oct 25 2012 Milan Crha <mcrha@redhat.com> - 3.6.1-4
- Rebuild against newer evolution-data-server

* Sat Oct 20 2012 Dan Horák <dan[at]danny.cz> - 3.6.1-3
- explicit BR: control-center as it isn't brought in indirectly on s390(x)

* Thu Oct 18 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.1-2
- Remove avoid-redhat-menus patch

  The standard way of supporting a desktop-specific menu layout is
  to set XDG_MENU_PREFIX (which we made gnome-session do now).

* Mon Oct 15 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Florian Müllner <fmuellner@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 11 2012 Florian Müllner <fmuellner@redhat.com> - 3.5.91-1
- Update dependencies

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 28 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.90-3
- Rebuild against new cogl/clutter

* Mon Aug 27 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.90-2
- Rebuild for new libcamel and synchronize gnome-bluetooth Requires with
  BuildRequires.

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 14 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.5-2
- Add Requires: gnome-bluetooth >= 3.5.5

* Mon Aug 13 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.4-4
- Tighten runtime requires

* Thu Jul 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.4-3
- Add a gdm-libs dependency

* Wed Jul 18 2012 Colin Walters <walters@verbum.org> - 3.5.4-2
- Bump release

* Wed Jul 18 2012 Ray Strode <rstrode@redhat.com> 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.3-2
- Rebuild against new e-d-s

* Tue Jun 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-2
- Remove upstreamed patch

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Mon May 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.4.1-6
- Cherry pick F17 changes, bump build for new evo soname

* Wed May 16 2012 Owen Taylor <otaylor@redhat.com> - 3.4.1-5
- New version of unmount notification

* Tue May 15 2012 Owen Taylor <otaylor@redhat.com> - 3.4.1-4
- Add a patch to display a notification until it's safe to remove a drive (#819492)

* Fri Apr 20 2012 Owen Taylor <otaylor@redhat.com> - 3.4.1-3
- Add a patch from upstream to avoid a crash when Evolution is not installed (#814401)

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence glib-compile-schemas scriplets

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Thu Apr  5 2012 Owen Taylor <otaylor@redhat.com> - 3.4.0-2
- Change gnome-shell-favourite-apps-firefox.patch to also patch the JS code
  to handle the transition from mozilla-firefox.desktop to firefox.desktop.
  (#808894, reported by Jonathan Kamens)

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.92-1
- Update to 3.3.92

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-2
- Rebuild for new cogl

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Thu Feb  9 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-2
- Depend on accountsservice-libs (#755112)

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-2
- Rebuild for new cogl

* Thu Jan  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Sun Nov 27 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 3.3.2-2
- Rebuild for new clutter and e-d-s

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Nov 09 2011 Kalev Lember <kalevlember@gmail.com> - 3.2.1-6
- Adapt to firefox desktop file name change in F17

* Thu Nov 03 2011 Adam Jackson <ajax@redhat.com> 3.2.1-5
- Build with -Wno-error=disabled-declarations for the moment

* Wed Nov 02 2011 Brian Pepple <bpepple@fedoraproject.org> - 3.2.1-4
- Rebuld against tp-logger.

* Sun Oct 30 2011 Bruno Wolff III <bruno@wolff.to> - 3.2.1-3
- Rebuild for new evolution-data-server

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Sep 28 2011 Ray Strode <rstrode@redhat.com> 3.2.0-2
- rebuild

* Mon Sep 26 2011 Owen Taylor <otaylor@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Fri Sep 16 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.91.1-2
- Tighten dependencies by specifying the required arch (#739130)

* Wed Sep 14 2011 Owen Taylor <otaylor@redhat.com> - 3.1.91.1-1
- Update to 3.1.91.1 (adds browser plugin)
  Update Requires

* Thu Sep 08 2011 Dan Horák <dan[at]danny.cz> - 3.1.91-3
- workaround a chrpath issue on s390(x)

* Wed Sep 07 2011 Kalev Lember <kalevlember@gmail.com> - 3.1.91-2
- Replace Epiphany with Firefox in the default favourite apps

* Wed Sep  7 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Thu Sep  1 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90.1-2
- Require caribou

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90.1-1
- Update to 3.1.90.1

* Wed Aug 31 2011 Adam Williamson <awilliam@redhat.com> - 3.1.4-3.gite7b9933
- rebuild against e-d-s

* Fri Aug 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-2.gite7b9933
- git snapshot that builds against gnome-menus 3.1.5

* Thu Aug 18 2011 Matthew Barnes <mbarnes@redhat.com> - 3.1.5-1
- Rebuild against newer eds libraries.

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3-4
- Rebuild

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3-3
- Add necessary requires

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3-2
- Rebuild

* Tue Jul  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 3.1.3-1
- Upstream 3.1.3 dev release

* Mon Jun 27 2011 Adam Williamson <awilliam@redhat.com> - 3.0.2-4
- add fixes from f15 branch (gjs dep and rpath)

* Wed Jun 22 2011 Owen Taylor <otaylor@redhat.com> - 3.0.2-3
- Add a patch from upstream to avoid g_file_get_contents()

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.0.2-2
- Rebuilt for new gtk3 and gnome-desktop3

* Wed May 25 2011 Owen Taylor <otaylor@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Tue May 10 2011 Dan Williams <dcbw@redhat.com> - 3.0.1-4
- Fix initial connections to WPA Enterprise access points (#699014)
- Fix initial connections to mobile broadband networks

* Thu Apr 28 2011 Dan Horák <dan[at]danny.cz> - 3.0.1-3
- no bluetooth on s390(x)

* Wed Apr 27 2011 Owen Taylor <otaylor@redhat.com> - 3.0.1-2
- Add a patch from upstream to fix duplicate applications in application display

* Mon Apr 25 2011 Owen Taylor <otaylor@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr 11 2011 Colin Walters <walters@verbum.org> - 3.0.0.2-2
- We want to use the GNOME menus which has the designed categories,
  not the legacy redhat-menus.

* Fri Apr 08 2011 Nils Philippsen <nils@redhat.com> - 3.0.0.2-1
- Update to 3.0.0.2 (fixes missing import that was preventing extensions from
  loading.)
- Update source URL

* Tue Apr  5 2011 Owen Taylor <otaylor@redhat.com> - 3.0.0.1-1
- Update to 3.0.0.1 (fixes bug where network menu could leave
  Clutter event handling stuck.)

* Mon Apr  4 2011 Owen Taylor <otaylor@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Tue Mar 29 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.93-3
- Bump

* Tue Mar 29 2011 Brian Pepple <bpepple@fedoraproject.org> - 2.91.93-2
- Rebuild for new tp-logger

* Mon Mar 28 2011 Owen Taylor <otaylor@redhat.com> - 2.91.93-1
- Update to 2.91.93.

* Fri Mar 25 2011 Ray Strode <rstrode@redhat.com> 2.91.92-3
- Adjustments for More nm-client api changes.
- Fix VPN indicator

* Thu Mar 24 2011 Christopher Aillon <caillon@redhat.com> - 2.91.92-2
- Make activating vpn connections work from the shell indicator

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Wed Mar 16 2011 Michel Salim <salimma@fedoraproject.org> - 2.91.91-2
- Fix alt-tab behavior on when primary display is not leftmost (# 683932)

* Tue Mar  8 2011 Owen Taylor <otaylor@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-2
- Require upower and polkit at runtime

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-6
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Bill Nottingham <notting@redhat.com> - 2.91.6-4
- buildrequire gnome-bluetooth to fix bluetooth status icon (#674874)

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-3
- Rebuild against newer gtk

* Tue Feb  1 2011 Owen Taylor <otaylor@redhat.com> - 2.91.6-2
- Build-requires evolution-data-server-devel

* Tue Feb  1 2011 Owen Taylor <otaylor@redhat.com> - 2.91.6-1
- Update to 2.91.6

* Thu Jan 13 2011 Mattihas Clasen <mclasen@redhat.com> - 2.91.5-3
- Drop desktop-effects dependency

* Wed Jan 12 2011 Colin Walters <walters@verbum.org> - 2.91.5-2
- BR latest g-i, handles flags as arguments better

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-1
- Update to 2.91.5

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-1
- Update to 2.91.4
- Rebuild against new gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.3-2
- Rebuild aginst new gtk

* Mon Nov 29 2010 Owen Taylor <otaylor@redhat.com> - 2.91.2-1
- Update to 2.91.3

* Thu Nov 18 2010 Owen Taylor <otaylor@redhat.com> - 2.91.2-3
- Add another memory-management crasher fix from upstream

* Mon Nov 15 2010 Owen Taylor <otaylor@redhat.com> - 2.91.2-2
- Add a patch from upstream fixing a memory-management crasher

* Tue Nov  9 2010 Owen Taylor <otaylor@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Mon Nov  1 2010 Owen Taylor <otaylor@redhat.com> - 2.91.1-1
- Update to 2.91.1
- Add libcroco-devel to BuildRequires, apparently it was getting
  pulled in indirectly before
- Add libcanberra-devel and pulseaudio-libs-devel BuildRequires

* Mon Oct  4 2010 Owen Taylor <otaylor@redhat.com> - 2.91.0-1
- Update to 2.91.0
- Remove patch to disable VBlank syncing

* Thu Aug 12 2010 Colin Walters <walters@verbum.org> - 2.31.5-7
- Add patch to disable vblank syncing

* Tue Jul 13 2010 Colin Walters <walters@verbum.org> - 2.31.5-5
- Run glib-compile-schemas

* Tue Jul 13 2010 Colin Walters <walters@megatron> - 2.31.5-4
- Bless stuff in files section

* Tue Jul 13 2010 Colin Walters <walters@verbum.org> - 2.31.5-3
- Axe gnome-desktop-devel

* Tue Jul 13 2010 Adel Gadllah <adel.gadllah@gmail.com> - 2.31.5-2
- BuildRequire gnome-desktop3-devel, gtk3

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 2.31.5-1
- New upstream version
- Drop rpath goop, shouldn't be necessary any more

* Fri Jun 25 2010 Colin Walters <walters@megatron> - 2.31.2-3
- Drop gir-repository-devel build dependency

* Fri May 28 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.31.2-2
- Added new version requirements for dependencies based on upstream releases
- Added new file listings for gnome-shell-clock-preferences binary and .desktop
- Added gnome-shell man page file listing

* Wed May 26 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.31.2-1
- New upstream release

* Fri Mar 26 2010 Colin Walters <walters@verbum.org> - 2.29.1-3
- Specify V=1 for build, readd smp_mflags since parallel is fixed upstream

* Thu Mar 25 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.29.1-2
- Bumped for new version of mutter and clutter
- Added version requirement to gjs-devel because of dependency of build

* Wed Mar 24 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.29.1-1
- Update to latest version 2.29.1

* Sun Feb 21 2010 Bastien Nocera <bnocera@redhat.com> 2.28.1-0.2.20100128git
- Require json-glib
- Rebuild for new clutter with json split out
- Fix deprecation in COGL

* Thu Jan 28 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.28.1-0.1.20100128git
- New git snapshot
- Fixed Version for alphatag use

* Fri Jan 15 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20101015git-1
- Added dependency on a git build of gobject-introspect to solve some breakage
- Also went ahead and made a new git tarball

* Tue Jan 12 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20100112git-1
- New git snapshot

* Mon Dec 07 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-5
- Added libtool, glib-gettext for the libtoolize dep of git snapshot

* Mon Dec 07 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-4
- Added gnome-common needed by autogen.sh in git snapshot build

* Sun Dec 06 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-3
- Added the autotools needed to build the git snapshot to the build requires

* Sun Dec 06 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-2
- Fixed the setup naming issue with the git snapshot directory naming

* Sun Dec 06 2009 Adam Miller <maxamillion@fedoraproject.org> - 2.28.0.20091206git-1
- Update to git snapshot on 20091206

* Wed Oct  7 2009 Owen Taylor <otaylor@redhat.com> - 2.28.0-2
- Update to 2.28.0

* Tue Sep 15 2009 Owen Taylor <otaylor@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Fri Sep  4 2009 Owen Taylor <otaylor@redhat.com> - 2.27.2-2
- Test for gobject-introspection version should be >= not >

* Fri Sep  4 2009 Owen Taylor <otaylor@redhat.com> - 2.27.2-1
- Update to 2.27.2
- Add an explicit dep on gobject-introspection 0.6.5 which is required 
  for the new version

* Sat Aug 29 2009 Owen Taylor <otaylor@redhat.com> - 2.27.1-4
- Fix GConf %%preun script to properly be for package removal

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.1-3
- Replace libgnomeui with gnome-desktop in BuildRequires

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.1-2
- BuildRequire intltool
- Add find_lang

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.1-1
- Update to 2.27.1
- Update Requires, add desktop-effects

* Wed Aug 12 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-4
- Add an explicit dependency on GConf2 for pre/post

* Tue Aug 11 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-3
- Add missing BuildRequires on gir-repository-devel

* Tue Aug 11 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-2
- Temporarily use a non-parallel-build until gnome-shell is fixed

* Mon Aug 10 2009 Owen Taylor <otaylor@redhat.com> - 2.27.0-1
- Initial version
