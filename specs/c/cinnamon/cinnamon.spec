# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 66ad76e3d5ad00f5768bd6340c614fb2e2bafaa1
%global date 20241127
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

%global __requires_exclude ^lib%{name}.so|^lib%{name}-js.so

%global cjs_version 6.4.0
%global cinnamon_desktop_version 6.4.0
%global cinnamon_translations_version 6.4.0
%global gobject_introspection_version 1.38.0
%global muffin_version 6.4.0
%global json_glib_version 0.13.2

%global __python %{__python3}

Name:           cinnamon
Version:        6.4.12
Release: 4%{?dist}
Summary:        Window management and application launching for GNOME
# Automatically converted from old format: GPLv2+ and LGPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+
URL:            https://github.com/linuxmint/%{name}
%if 0%{?tag:1}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0:        %{url}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif
Source1:        10_cinnamon-common.gschema.override
Source2:        10_cinnamon-apps.gschema.override.in
Source3:        22_fedora.styles

Patch0:         set_wheel.patch
#Patch1:         revert_25aef37.patch
Patch2:         default_panal_launcher.patch
Patch3:         remove_crap_from_menu.patch
Patch4:         Add_nightlight_applet.patch
Patch5:         %{url}/pull/13091.patch#/Use_DesktopAppInfo_from_GioUnix.patch
Patch6:         %{url}/commit/9ed70641a1f63d2b2b44e08a84033cbf912e0c2b.patch#/fix_mount_applet.patch

ExcludeArch:    %{ix86}


BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  desktop-file-utils
BuildRequires:  python3-libsass
BuildRequires:  python3-rpm-macros
BuildRequires:  pkgconfig(cjs-1.0) >= %{cjs_version}
BuildRequires:  pkgconfig(dbus-glib-1)
BuildRequires:  pkgconfig(gcr-base-3)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(libgnome-menu-3.0)
BuildRequires:  pkgconfig(lib%{name}-menu-3.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(%{name}-desktop) >= %{cinnamon_desktop_version}
BuildRequires:  gobject-introspection >= %{gobject_introspection_version}
BuildRequires:  pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(polkit-agent-1)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(xapp)

# for screencast recorder functionality
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  intltool
BuildRequires:  pkgconfig(libcanberra)

# used in unused BigThemeImage
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libmuffin-0) >= %{muffin_version}
BuildRequires:  pkgconfig(libpulse)

# Bootstrap requirements
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  gnome-common

# media keys
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(colord)
%ifnarch s390 s390x
BuildRequires:  pkgconfig(libwacom)
BuildRequires:  pkgconfig(xorg-wacom)
%endif
BuildRequires:  pkgconfig(xtst)


Requires:       %{name}-desktop%{?_isa} >= %{cinnamon_desktop_version}
Requires:       muffin%{?_isa} >= %{muffin_version}
Requires:       cjs%{?_isa} >= %{cjs_version}
Requires:       gnome-menus%{?_isa} >= 3.0.0-2

# wrapper script used to restart old GNOME session if run --replace
# from the command line
Requires:       gobject-introspection%{?_isa} >= %{gobject_introspection_version}

# needed for loading SVG's via gdk-pixbuf
Requires:       librsvg2%{?_isa}

# needed as it is now split from Clutter
Requires:       json-glib%{?_isa} >= %{json_glib_version}
Requires:       upower%{?_isa}
Requires:       polkit%{?_isa} >= 0.100

# needed for session files
Requires:       %{name}-session%{?_isa}

# needed for schemas
Requires:       at-spi2-atk%{?_isa}

# needed for on-screen keyboard
Requires:       caribou%{?_isa}

# needed for the user menu
Requires:       accountsservice-libs%{?_isa}

# needed for settings
Requires:       gsound
Requires:       libtimezonemap%{?_isa}
Requires:       python3-distro
Requires:       python3-pytz
Requires:       python3-pexpect
Requires:       python3-gobject%{?_isa}
Requires:       python3-dbus%{?_isa}
Requires:       python3-lxml%{?_isa}
Requires:       python3-pillow%{?_isa}
Requires:       python3-pam
Requires:       python3-tinycss2
Requires:       python3-requests
Requires:       python3-setproctitle%{?_isa}
Requires:       python3-xapp
Requires:       mintlocale
Recommends:     %{name}-control-center%{?_isa}
Recommends:     gnome-online-accounts-gtk
Recommends:     %{name}-translations >= %{cinnamon_translations_version}

# needed for theme overrides
Requires:       desktop-backgrounds-basic
Requires:       desktop-backgrounds-gnome
Requires:       gnome-backgrounds
Recommends:     paper-icon-theme
Requires:       system-logos

# Theming
Requires:       google-noto-sans-fonts
Requires:       google-noto-sans-mono-fonts
Requires:       %{name}-themes >= 1:1.7.4-0.2.20181112gitb94b890

# RequiredComponents in the session files
Requires:       nemo%{?_isa}
Requires:       %{name}-screensaver%{?_isa}

# metacity and mate-panel are needed for fallback
Recommends:     metacity%{?_isa}
Recommends:     mate-panel%{?_isa}

# required for keyboard applet
Requires:       gucharmap%{?_isa}
Requires:       xapps%{?_isa}
Requires:       python3-xapps-overrides%{?_isa}

# required for calendar applet events
Recommends:     %{name}-calendar-server%{?_isa} = %{version}-%{release}

# required for network applet
Requires:       nm-connection-editor%{?_isa}
Requires:       network-manager-applet%{?_isa}

Requires:       python3-inotify


# required for cinnamon-killer-daemon
Requires:       keybinder3%{?_isa}

# required for sound applet
Requires:       wget%{?_isa}

# required for power applet
Recommends:     tuned-ppd

# required for printer applet
Requires:       cups-client%{?_isa}

# required for spice
Requires:       gettext

# required for gesture support
Recommends:     touchegg

# required for flatpak support
Recommends:     xdg-desktop-portal-xapp

Requires:       libsoup3

Provides:       desktop-notification-daemon
Provides:       bundled(libcroco) = 0.6.12
Provides:       PolicyKit-authentication-agent = %{version}-%{release}

%description
Cinnamon is a Linux desktop which provides advanced
innovative features and a traditional user experience.

The desktop layout is similar to Gnome 2.
The underlying technology is forked from Gnome Shell.
The emphasis is put on making users feel at home and providing
them with an easy to use and comfortable desktop experience.

%package calendar-server
Summary:        Calendar server for Cinnamon
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       evolution-data-server%{?_isa}
Requires:       gnome-calendar%{?_isa}

%description calendar-server
Calendar server for Cinnamon.

%if 0%{?fedora} && 0%{?fedora} < 40
%package devel-doc
Summary:        Development Documentation files for Cinnamon
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description devel-doc
This package contains the code documentation for various Cinnamon components.
%endif

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

%{__sed} -i -e 's@gksu@pkexec@g' files%{_bindir}/%{name}-settings-users
%{__sed} -i -e 's@gnome-orca@orca@g' files%{_datadir}/%{name}/%{name}-settings/modules/cs_accessibility.py
# remove mintlocale im from settings
%{__sed} -i -e 's@mintlocale im@mintlocale_im_removed@g' files%{_datadir}/%{name}/%{name}-settings/%{name}-settings.py

# Fix rpmlint errors
for file in files%{_datadir}/%{name}/applets/{printers,settings-example}@cinnamon.org/*.py \
  files%{_datadir}/%{name}/%{name}-settings/bin/*.py \
  files%{_datadir}/%{name}/%{name}-looking-glass/*.py \
  files%{_datadir}/%{name}/%{name}-settings/modules/cs_{actions,applets,desklets,display,gestures}.py \
  python3/cinnamon/*.py; do
  chmod a+x $file
done
chmod a-x files%{_datadir}/%{name}/%{name}-settings/bin/__init__.py

%build
%meson \
 --libexecdir=%{_libexecdir}/cinnamon/ \
 -Ddeprecated_warnings=false \
 -Dpy3modules_dir=%{python3_sitelib} \
%if 0%{?fedora} && 0%{?fedora} < 40
 -Ddocs=true
%else
 -Ddocs=false
%endif

%meson_build


%install
%meson_install

# install common gschema override
%{__install} --target-directory=%{buildroot}%{_datadir}/glib-2.0/schemas \
    -Dpm 0644 %{SOURCE1}

# install gschema-override for apps
%{__sed} -e 's!@pkg_manager@!org.mageia.dnfdragora.desktop!g' \
    < %{SOURCE2} > %{buildroot}%{_datadir}/glib-2.0/schemas/10_%{name}-apps.gschema.override

# install gschema-override for wallpaper
%{__cat} >> %{buildroot}%{_datadir}/glib-2.0/schemas/10_%{name}-wallpaper.gschema.override << EOF
[org.cinnamon.desktop.background]
picture-uri='file:///usr/share/backgrounds/tiles/default_blue.jpg'
EOF

# install style file for mint-x and mint-y
%{__install} --target-directory=%{buildroot}%{_datadir}/%{name}/styles.d/ \
    -Dpm 0644 %{SOURCE3}

# Provide symlink for the background-propeties.
%{__ln_s} %{_datadir}/gnome-background-properties %{buildroot}%{_datadir}/%{name}-background-properties
# Delete useless gir files
%{__rm} -rf %{buildroot}%{_datadir}/%{name}/*.gir

%check
%{_bindir}/desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%doc README.rst AUTHORS
%license COPYING
%{_bindir}/cinnamon
%{_bindir}/cinnamon-dbus-command
%{_bindir}/cinnamon-desktop-editor
%{_bindir}/cinnamon-file-dialog
%{_bindir}/cinnamon-hover-click
%{_bindir}/cinnamon-install-spice
%{_bindir}/cinnamon-json-makepot
%{_bindir}/cinnamon-killer-daemon
%{_bindir}/cinnamon-launcher
%{_bindir}/cinnamon-looking-glass
%{_bindir}/cinnamon-menu-editor
%{_bindir}/cinnamon-preview-gtk-theme
%{_bindir}/cinnamon-screensaver-lock-dialog
%{_bindir}/cinnamon-session-cinnamon
%{_bindir}/cinnamon-session-cinnamon2d
%{_bindir}/cinnamon-settings
%{_bindir}/cinnamon-settings-users
%{_bindir}/cinnamon-slideshow
%{_bindir}/cinnamon-spice-updater
%{_bindir}/cinnamon-subprocess-wrapper
%{_bindir}/cinnamon-xlet-makepot
%{_bindir}/cinnamon2d
%{_bindir}/xlet-about-dialog
%{_bindir}/xlet-settings
%config(noreplace) %{_sysconfdir}/xdg/menus/*
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/org.Cinnamon.HotplugSniffer.service
%{_datadir}/dbus-1/services/org.Cinnamon.Melange.service
%{_datadir}/dbus-1/services/org.Cinnamon.Slideshow.service
%{_datadir}/desktop-directories/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/%{name}-session/sessions/*
%{_datadir}/icons/hicolor/*/*/*
%{_datadir}/polkit-1/actions/org.%{name}.settings-users.policy
%{_datadir}/xdg-desktop-portal/x-cinnamon-portals.conf
%{_datadir}/xsessions/*
%{_datadir}/wayland-sessions/*
%{_datadir}/%{name}/
%{_datadir}/%{name}-background-properties
%{_libdir}/%{name}/
%dir %{_libexecdir}/%{name}/
%{_libexecdir}/cinnamon/cinnamon-hotplug-sniffer
%{_libexecdir}/cinnamon/cinnamon-perf-helper
%{_mandir}/man1/*
%{python3_sitelib}/%{name}/

%files calendar-server
%{_bindir}/%{name}-calendar-server
%{_libexecdir}/%{name}/%{name}-calendar-server.py
%{_datadir}/dbus-1/services/org.%{name}.CalendarServer.service

%if 0%{?fedora} && 0%{?fedora} < 40
%files devel-doc
%doc %{_datadir}/gtk-doc/html/*/
%endif

%changelog
* Sun Sep 21 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.12-3
- Fix mount applet

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.4.12-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 15 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.12-1
- Update to 6.4.12

* Fri Sep 12 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.9-4
- Rebuild for glib2-2.86 changes

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 6.4.9-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Apr 26 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.9-1
- Update to 6.4.9

* Thu Mar 27 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.8-2
- Rebuild for new cjs

* Wed Feb 26 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.8-1
- Update to 6.4.8

* Sat Feb 08 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.7-1
- Update to 6.4.7

* Mon Jan 20 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.6-3
- Add recommends tuned-ppd for power applet power levels

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.6-1
- Update to 6.4.6

* Sat Jan 04 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.4-1
- Update to 6.4.4

* Thu Dec 19 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.3-1
- Update to 6.4.3

* Wed Dec 11 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.2-2
- Add a nightlight applet to ease disabling

* Fri Dec 06 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.2-1
- Update to 6.4.2

* Mon Dec 02 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.1-1
- Update t0 6.4.1

* Thu Nov 28 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.0-1
- Update to 6.4.0

* Wed Nov 27 2024 Leigh Scott <leigh123linux@gmail.com> - 6.3.0^20241127git66ad76e-2
- Update git snapshot

* Thu Nov 14 2024 Leigh Scott <leigh123linux@gmail.com> - 6.3.0^20241114git8525e74-1
- Update to git snapshot

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 6.2.9-2
- convert license to SPDX

* Tue Aug 20 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.9-1
- Update to 6.2.9

* Mon Aug 05 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.8-1
- Update to 6.2.8

* Sat Jul 20 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.7-1
- Update to 6.2.7

* Sat Jul 20 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.6-1
- Update to 6.2.6

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.4-1
- Update to 6.2.4

* Sat Jun 22 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.2-1
- Update to 6.2.2

* Tue Jun 18 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.1-1
- Update to 6.2.1

* Sun Jun 16 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-1
-  Update to 6.2.0

* Thu Jun 13 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-0.4.20240613git3aed68c
- Update snapshot

* Wed Jun 12 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-0.3.20240604git0d2a1ed
- Enable internal polkit agent for xorg and wayland

* Wed Jun 12 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-0.2.20240604git0d2a1ed
- Remove polkit autostart

* Wed Jun 12 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-0.1.20240604git0d2a1ed
- Update to git snapshot

* Fri May 17 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.4-7
- Add recommends gnome-online-accounts-gtk

* Sun Apr 21 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.4-6
- Add patch to remove old goa desktop file

* Fri Mar 08 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.4-5
- Add requires google-noto-sans-mono-fonts, needed for override

* Mon Feb 19 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.4-4
- Use paper cursor theme as adwaita is broken

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.4-1
- Update to 6.0.4 release

* Fri Dec 29 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.3-1
- Update to 6.0.3 release

* Tue Dec 19 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.2-1
- Update to 6.0.2 release

* Wed Nov 29 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.0-1
- Update to 6.0.0 release

* Fri Nov 10 2023 Leigh Scott <leigh123linux@gmail.com> - 5.9.0-2.20231107git5a73d40
- Rebuild against correct muffin

* Thu Nov 09 2023 Leigh Scott <leigh123linux@gmail.com> - 5.9.0-1.20231107git5a73d40
- Update to git snapshot

* Fri Oct 27 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.4-5
- Use libsoup3 for applets

* Sun Sep 24 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.4-4
- Add xdg-portal conf file

* Wed Jul 19 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.4-3
- Add fedora styles file

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 09 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.4-1
- Update to 5.8.4 release

* Thu Jul 06 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.3-1
- Update to 5.8.3 release
- Revert 'Default disable desktop effects

* Wed Jul 05 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.2-2
- Rebuilt for Python 3.12

* Fri Jun 23 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.2-1
- Update to 5.8.2 release

* Thu Jun 08 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.1-2
- Drop requires libsoup

* Thu Jun 08 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.1-1
- Update to 5.8.1 release

* Thu Jun 08 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.0-2
- Default disable desktop effects

* Wed Jun 07 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.0-1
- Update to 5.8.0 release

* Wed Jun 07 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.0-0.2.20230606git77e26ae
- Update to git master snapshot

* Fri Jun 02 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.0-0.1.20230601git93135ed
- Update to git master snapshot

* Tue May 09 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.8-3
- Rebuild for cjs-5.7.0

* Thu Apr 13 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.8-2
- Fix settings on aarch64

* Mon Mar 20 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.8-1
- Update to 5.6.8 release

* Thu Feb 16 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.7-1
- Update to 5.6.7 release

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 15 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.5-1
- Update to 5.6.5 release

* Wed Nov 30 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.4-1
- Update to 5.6.4 release

* Mon Nov 28 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.3-1
- Readd lost window placement modes

* Fri Nov 18 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.1-1
- Update to 5.6.1 release

* Tue Sep 06 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.12-1
- Update to 5.4.12 release

* Sun Aug 21 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.11-1
- Update to 5.4.11 release

* Sat Aug 13 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.10-2
- Fix soup version issue for applets

* Sat Aug 13 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.10-1
- Update to 5.4.10 release

* Mon Aug 01 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.9-1
- Update to 5.4.9 release

* Mon Jul 25 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.8-1
- Update to 5.4.8 release

* Sun Jul 24 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.7-1
- Update to 5.4.7 release

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.5-1
- Update to 5.4.5 release

* Fri Jul 15 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.4-1
- Update to 5.4.4 release

* Wed Jul 13 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.2-2.20220712git1fe1f52
- Update to latest snapshot

* Mon Jun 27 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.2-1
- Update to 5.4.2 release

* Mon Jun 20 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.1-1
- Update to 5.4.1 release

* Sat Jun 11 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-2
- Add requires gsound

* Sat Jun 11 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-1
- Update to 5.4.0 release

* Sun May 22 2022 Leigh Scott <leigh123linux@gmail.com> - 5.2.7-4
- The calendar-server sub-package isn't noarch due to search paths

* Mon May 16 2022 Leigh Scott <leigh123linux@gmail.com> - 5.2.7-3
- Fix calendar-server sub-package

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 01 2022 Leigh Scott <leigh123linux@gmail.com> - 5.2.7-1
- Update to 5.2.7 release

* Thu Dec 16 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.6-1
- Update to 5.2.6 release

* Tue Dec 14 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.5-3
- Tweak schema override for theme changes

* Mon Dec 13 2021 Peter Hutterer <peter.hutterer@redhat.com> - 5.2.5-2
- Rebuild for libwacom soname bump

* Thu Dec 09 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.5-1
- Update to 5.2.5 release

* Mon Dec 06 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.3-1
- Update to 5.2.3 release

* Mon Nov 29 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.1-1
- Update to 5.2.1 release

* Sat Nov 20 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.0-1
- Update to 5.2.0 release

* Thu Nov 04 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.7-1
- Update to 5.0.7 release

* Fri Oct 15 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.6-1
- Update to 5.0.6 release

* Tue Oct 05 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.5-5
- Fix python-3.10 menu-editor

* Mon Sep 27 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.5-4
- Drop fallback patches

* Mon Sep 06 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.5-3
- Add upstream fixes

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.5-1
- Update to 5.0.5 release

* Thu Jul 08 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.4-1
- Update to 5.0.4 release

* Fri Jun 25 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.3-1
- Update to 5.0.3 release

* Mon Jun 07 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.2-2
- Add python install directory patch

* Fri Jun 04 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.2-1
- Update to 5.0.2 release

* Wed Jun 02 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.1-2
- Switch fallback to metacity

* Tue Jun 01 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.1-1
- Update to 5.0.1 release

* Tue Jun 01 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.0-2
- Fix session

* Tue Jun 01 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.0-1
- Update to 5.0.0 release

* Tue Mar 23 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.6-5
- Add gnome-system-monitor to settings

* Thu Mar 04 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.6-4
- More GWL fixes

* Thu Mar 04 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.6-3
- Add upstream GWL fixes

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.6-1
- Update to 4.8.6 release

* Sat Jan  2 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.5-1
- Update to 4.8.5 release

* Tue Dec 29 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.4-1
- Update to 4.8.4 release

* Sun Dec 13 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.3-1
- Update to 4.8.3 release

* Tue Dec  8 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.2-1
- Update to 4.8.2 release

* Tue Dec  8 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.1-1
- Update to 4.8.1 release

* Thu Nov 26 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.0-1
- Update to 4.8.0 release

* Mon Oct 19 2020 Leigh Scott <leigh123linux@gmail.com> - 4.7.0-0.1.20201019gitd077210
- Update to git master snapshot

* Sat Sep 19 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.7-2
- Switch to gjs f34+

* Tue Aug 11 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.7-1
- Update to 4.6.7 release

* Mon Aug 10 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.6-4
- Enable LTO

* Fri Jul 31 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.6-3
- Drop libcroco requirement

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.6-1
- Update to 4.6.6 release

* Sun Jun 21 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.5-1
- Update to 4.6.5 release

* Wed Jun 17 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.4-1
- Update to 4.6.4 release

* Fri Jun 12 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.3-2
- Fix applet configure with python3.9

* Sat Jun 06 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.3-1
- Update to 4.6.3 release

* Wed May 27 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.2-1
- Update to 4.6.2 release

* Thu May 21 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.1-1
- Update to 4.6.1 release

* Wed May 13 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.0-1
- Update to 4.6.0 release

* Mon Apr 20 2020 Leigh Scott <leigh123linux@gmail.com> - 4.4.8-8
- Use desktop-backgrounds-basic for background instead of fedora default

* Tue Apr 14 2020 Leigh Scott <leigh123linux@gmail.com> - 4.4.8-7
- Fix last commit

* Tue Apr 14 2020 Leigh Scott <leigh123linux@gmail.com> - 4.4.8-6
- Disable bell-mode

* Tue Apr 14 2020 Leigh Scott <leigh123linux@gmail.com> - 4.4.8-5
- Remove BuildRequires pkgconfig(gconf-2.0)

* Wed Feb 26 2020 Leigh Scott <leigh123linux@googlemail.com> - 4.4.8-4
- Bump for f33 rawhide

* Mon Feb 17 2020 Leigh Scott <leigh123linux@googlemail.com> - 4.4.8-3
- Enable notification sound
- Patch cinnamon-setting info for python-3.8

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Leigh Scott <leigh123linux@googlemail.com> - 4.4.8-1
- Update to 4.4.8 release

* Mon Dec 30 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.6-1
- Update to 4.4.6 release

* Thu Dec 12 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.5-2
- Switch to xapp-status for bluetooth

* Thu Dec 12 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.5-1
- Update to 4.4.5 release

* Tue Dec 10 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.4-1
- Update to 4.4.4 release

* Sat Dec 07 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.3-1
- Update to 4.4.3 release

* Fri Nov 29 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.2-2
- Tweak applet layout

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.2-1
- Update to 4.4.2 release

* Tue Nov 26 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.1-1
- Update to 4.4.1 release

* Sun Nov 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-6
- fix cinnamon-desktop isa mistake

* Sun Nov 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-5
- Add missing isa

* Sun Nov 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-4
- Add requires python3-xapp and python3-setproctitle

* Sun Nov 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-3
- Add requires python3-pytz and libtimezonemap

* Sun Nov 24 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-2
- Readd polkit-cinnamon-authentication-agent-1 to autostart patch

* Fri Nov 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-1
- Update to 4.4.0 release

* Thu Nov 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-0.1.20191120git6a9367b
- Update to git master snapshot

* Sat Sep 14 2019 Leigh Scott <leigh123linux@gmail.com> - 4.2.4-2
- Fix cinnamon-settings default issue (rhbz#1752134)

* Wed Sep 04 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.4-1
- Update to 4.2.4 release

* Wed Aug 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.3-2
- Add notification fix
- Switch rawhide to 32

* Wed Jul 31 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.3-1
- Update to 4.2.3 release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.2-1
- Update to 4.2.2 release

* Sun Jun 30 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-2
- Add requires python3-tinycss

* Sat Jun 29 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-1
- Update to 4.2.0 release

* Sun Jun 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-0.1.20190614git369148f
- Update snapshot

* Wed Jun 12 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.11-0.4.20190611gitd7c6da5
- Update snapshot

* Wed Jun 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.11-0.3.20190604gitdf5150a
- Update snapshot

* Tue Apr 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.11-0.2.20190416giteccebdd
- Update snapshot

* Fri Apr 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.11-0.1.20190405gitc843f36
- Update to git master snapshot

* Wed Apr 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.10-1
- Update to 4.0.10 release

* Mon Mar 11 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.9-1
- Update to 4.0.9 release

* Mon Mar 04 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-5
- Bump for f30 backgrounds

* Thu Feb 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-4
- Add monospace font override

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-2
- Tweak panel layout

* Sat Dec 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-1
- Update to 4.0.8 release

* Sun Dec 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.7-1
- Update to 4.0.7 release

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.5-1
- Update to 4.0.5 release

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.4-1
- Update to 4.0.4 release

* Wed Nov 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.3-1
- Update to 4.0.3 release

* Tue Nov 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.2-1
- Update to 4.0.2 release

* Wed Nov 14 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.1-2
- Switch theme and add version to cinnamon-themes requires

* Mon Nov 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.1-1
- Update to 4.0.1 release

* Sat Nov 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.0-1
- Update to 4.0.0 release

