## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global blueprint_compiler_version 0.17
%global gcr_version 4.1.0
%global gnome_online_accounts_version 3.51.0
%global glib2_version 2.76.6
%global gnome_desktop_version 44.0-7
%global gsd_version 48~rc
%global gsettings_desktop_schemas_version 48~alpha-2
%global upower_version 1.90.6
%global gtk4_version 4.15.2
%global gnome_bluetooth_version 42~alpha
%global libadwaita_version 1.8~alpha
%global nm_version 1.52.0

%global tarball_version %%(echo %{version} | tr '~' '.')

# Disable parental control for RHEL builds
%bcond malcontent %[!0%{?rhel}]

Name:           gnome-control-center
Version:        49.4
Release:        %autorelease
Summary:        Utilities to configure the GNOME desktop

License:        GPL-2.0-or-later AND CC0-1.0
URL:            https://gitlab.gnome.org/GNOME/gnome-control-center/
Source0:        https://download.gnome.org/sources/%{name}/49/%{name}-%{tarball_version}.tar.xz
# libgnome-volume-control patch to fix inconsistencies in device selection after MR31
# Includes:
# https://gitlab.gnome.org/GNOME/libgnome-volume-control/-/merge_requests/29
# https://gitlab.gnome.org/GNOME/libgnome-volume-control/-/merge_requests/32
# https://gitlab.gnome.org/GNOME/libgnome-volume-control/-/merge_requests/33
Source1:        gvc-33.patch

BuildRequires:  blueprint-compiler >= %{blueprint_compiler_version}
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-style-xsl libxslt
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  pkgconfig(accountsservice)
BuildRequires:  pkgconfig(colord)
BuildRequires:  pkgconfig(colord-gtk4)
BuildRequires:  pkgconfig(cups)
BuildRequires:  pkgconfig(gcr-4) >= %{gcr_version}
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gdk-wayland-3.0)
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-desktop-4) >= %{gnome_desktop_version}
BuildRequires:  pkgconfig(gnome-settings-daemon) >= %{gsd_version}
BuildRequires:  pkgconfig(goa-1.0) >= %{gnome_online_accounts_version}
BuildRequires:  pkgconfig(goa-backend-1.0)
BuildRequires:  pkgconfig(gsettings-desktop-schemas) >= %{gsettings_desktop_schemas_version}
BuildRequires:  pkgconfig(gsound)
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(ibus-1.0)
BuildRequires:  pkgconfig(libadwaita-1) >= %{libadwaita_version}
BuildRequires:  pkgconfig(libgtop-2.0)
BuildRequires:  pkgconfig(libnm) >= %{nm_version}
BuildRequires:  pkgconfig(libnma-gtk4)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-mainloop-glib)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
%if %{with malcontent}
BuildRequires:  pkgconfig(malcontent-0)
%endif
BuildRequires:  pkgconfig(mm-glib)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(pwquality)
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(tecla)
BuildRequires:  pkgconfig(udisks2)
BuildRequires:  pkgconfig(upower-glib) >= %{upower_version}
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
%ifnarch s390 s390x
BuildRequires:  pkgconfig(gnome-bluetooth-3.0) >= %{gnome_bluetooth_version}
BuildRequires:  pkgconfig(libwacom)
%endif

# Versioned library deps
Requires: libadwaita%{?_isa} >= %{libadwaita_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gnome-desktop4%{?_isa} >= %{gnome_desktop_version}
Requires: gnome-online-accounts%{?_isa} >= %{gnome_online_accounts_version}
Requires: gnome-settings-daemon%{?_isa} >= %{gsd_version}
Requires: gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires: gtk4%{?_isa} >= %{gtk4_version}
Requires: upower%{?_isa} >= %{upower_version}
%ifnarch s390 s390x
Recommends: gnome-bluetooth%{?_isa} >= 1:%{gnome_bluetooth_version}
%endif

Requires: %{name}-filesystem = %{version}-%{release}
# For user accounts
Requires: accountsservice
Requires: alsa-lib
# For the thunderbolt panel
Recommends: bolt
# For the color panel
Requires: colord
# For the printers panel
Requires: cups-pk-helper
Requires: dbus
# For the user languages
Requires: iso-codes
%if %{with malcontent}
# For parental controls support
Requires: malcontent
Recommends: malcontent-control
%endif
# For the network panel
Recommends: NetworkManager-wifi
Recommends: nm-connection-editor
# For Show Details in the color panel
Recommends: gnome-color-manager
# For the sharing panel
Recommends: gnome-remote-desktop
%if 0%{?fedora}
Recommends: rygel
%endif
# For the info/details panel
Recommends: switcheroo-control
# For the keyboard panel
Requires: /usr/bin/tecla
%if 0%{?fedora} >= 35 || 0%{?rhel} >= 9
# For the power panel
Recommends: ppd-service
%if 0%{?fedora} && 0%{?fedora} < 41
Suggests: power-profiles-daemon
%else
Suggests: tuned-ppd
%endif
%endif

# Renamed in F28
Provides: control-center = 1:%{version}-%{release}
Provides: control-center%{?_isa} = 1:%{version}-%{release}
Obsoletes: control-center < 1:%{version}-%{release}

%description
This package contains configuration utilities for the GNOME desktop, which
allow to configure accessibility options, desktop fonts, keyboard and mouse
properties, sound setup, desktop theme and background, user interface
properties, screen resolution, and other settings.

%package filesystem
Summary: GNOME Control Center directories
# NOTE: this is an "inverse dep" subpackage. It gets pulled in
# NOTE: by the main package and MUST not depend on the main package
BuildArch: noarch
# Renamed in F28
Provides: control-center-filesystem = 1:%{version}-%{release}
Obsoletes: control-center-filesystem < 1:%{version}-%{release}

%description filesystem
The GNOME control-center provides a number of extension points
for applications. This package contains directories where applications
can install configuration files that are picked up by the control-center
utilities.

%prep
%autosetup -p1 -n %{name}-%{tarball_version}
pushd subprojects/gvc
patch -p1 < %{SOURCE1}
popd

%build
%meson \
  -Ddocumentation=true \
  -Dlocation-services=enabled \
%if 0%{?fedora}
  -Ddistributor_logo=%{_datadir}/pixmaps/fedora_logo_med.png \
  -Ddark_mode_distributor_logo=%{_datadir}/pixmaps/fedora_whitelogo_med.png \
%endif
%if 0%{?rhel}
  -Ddistributor_logo=%{_datadir}/pixmaps/fedora-logo.png \
  -Ddark_mode_distributor_logo=%{_datadir}/pixmaps/system-logo-white.png \
%endif
%if %{with malcontent}
  -Dmalcontent=true \
%else
  -Dmalcontent=false \
%endif
  %{nil}
%meson_build

%install
%meson_install

# We do want this
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome/wm-properties

# We don't want these
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/autostart
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/cursor-fonts

%find_lang %{name} --all-name --with-gnome

%files -f %{name}.lang
%license COPYING
%doc NEWS README.md
%{_bindir}/gnome-control-center
%{_datadir}/applications/*.desktop
%{_datadir}/bash-completion/completions/gnome-control-center
%{_datadir}/dbus-1/services/org.gnome.Settings.SearchProvider.service
%{_datadir}/dbus-1/services/org.gnome.Settings.service
%{_datadir}/dbus-1/services/org.gnome.Settings.GlobalShortcutsProvider.service
%{_datadir}/dbus-1/interfaces/org.gnome.GlobalShortcutsRebind.xml
%{_datadir}/gettext/
%{_datadir}/glib-2.0/schemas/org.gnome.Settings.gschema.xml
%{_datadir}/gnome-control-center/keybindings/*.xml
%{_datadir}/gnome-control-center/pixmaps
%{_datadir}/gnome-shell/search-providers/org.gnome.Settings.search-provider.ini
%{_datadir}/icons/gnome-logo-text*.svg
%{_datadir}/icons/hicolor/*/*/*
%{_mandir}/man1/gnome-control-center.1*
%{_metainfodir}/org.gnome.Settings.metainfo.xml
%{_datadir}/pixmaps/faces
%{_datadir}/pkgconfig/gnome-keybindings.pc
%{_datadir}/polkit-1/actions/org.gnome.controlcenter.*.policy
%{_datadir}/polkit-1/rules.d/gnome-control-center.rules
%{_datadir}/sounds/gnome/default/*/*.ogg
%{_libexecdir}/gnome-control-center-search-provider
%{_libexecdir}/gnome-control-center-print-renderer
%{_libexecdir}/gnome-control-center-global-shortcuts-provider

%files filesystem
%dir %{_datadir}/gnome-control-center
%dir %{_datadir}/gnome-control-center/keybindings
%dir %{_datadir}/gnome/wm-properties

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 49.4-3
- Latest state for gnome-control-center

* Sun Feb 15 2026 Pablo Greco <pablo@fliagreco.com.ar> - 49.4-2
- Update gvc to d2442f455844e5292cb4a74ffc66ecc8d7595a9f

* Mon Jan 26 2026 Felipe Borges <felipeborges@gnome.org> - 49.4-1
- Update to 49.4

* Thu Jan 22 2026 Barry Dunn <badunn@redhat.com> - 49.3-1
- Update to 49.3

* Wed Dec 10 2025 Adrian Vovk <adrianvovk@gmail.com> - 49.2.2-1
- Update to 49.2.2

* Mon Oct 13 2025 Petr Schindler <pschindl@redhat.com> - 49.1-1
- Update to 49.1

* Tue Sep 16 2025 Felipe Borges <felipeborges@gnome.org> - 49.0-2
- Add a11y patches for Accessibility Conformance Report

* Mon Sep 15 2025 Felipe Borges <felipeborges@gnome.org> - 49.0-1
- Update to 49.0

* Tue Sep 02 2025 Felipe Borges <felipeborges@gnome.org> - 49~rc-1
- Update to 49.rc

* Tue Aug 05 2025 Felipe Borges <felipeborges@gnome.org> - 49~beta-1
- Update to 49.beta

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 49~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-1
- Update to 49.alpha

* Mon Jun 30 2025 Carlos Garnacho <cgarnach@redhat.com> - 48.3-1
- Update to 48.3

* Mon May 26 2025 nmontero <nmontero@redhat.com> - 48.2-1
- Update to 48.2

* Thu Apr 24 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 48.1-3
- Revert "Avoid pulling in pkgconfig"

* Thu Apr 24 2025 Fxzx micah <fxzxmicah@outlook.com> - 48.1-2
- Avoid pulling in pkgconfig

* Mon Apr 14 2025 nmontero <nmontero@redhat.com> - 48.1-1
- Update to 48.1

* Mon Mar 17 2025 Felipe Borges <felipeborges@gnome.org> - 48.0-1
- Update to 48.0

* Mon Feb 17 2025 Felipe Borges <felipeborges@gnome.org> - 48~beta-1
- Update to 48.beta

* Mon Jan 20 2025 Felipe Borges <felipeborges@gnome.org> - 48~alpha-2
- Update libadwaita and gsettings-desktop-schemas dependencies

* Mon Jan 20 2025 Felipe Borges <felipeborges@gnome.org> - 48~alpha-1
- Update to 48.alpha

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 47.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 nmontero <nmontero@redhat.com> - 47.3-1
- Update to 47.3

* Tue Nov 26 2024 nmontero <nmontero@redhat.com> - 47.2-1
- Update to 47.2

* Fri Nov 15 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 47.1.1-2
- Drop setxkbmap dependency

* Wed Oct 23 2024 nmontero <nmontero@redhat.com> - 47.1.1-1
- Update to 47.1.1

* Tue Oct 22 2024 nmontero <nmontero@redhat.com> - 47.1-1
- Update to 47.1

* Tue Oct 08 2024 Kate Hsuan <hpa@redhat.com> - 47.0.1-2
- Change Recommands to ppd-service

* Tue Sep 17 2024 nmontero <nmontero@redhat.com> - 47.0.1-1
- Update to 47.0.1

* Tue Sep 03 2024 David King <amigadave@amigadave.com> - 47~rc-1
- Update to 47.rc

* Tue Aug 13 2024 Felipe Borges <felipeborges@gnome.org> - 47~beta-1
- Update to 47.beta

* Tue Jul 30 2024 Kate Hsuan <hpa@redhat.com> - 47~alpha-3
- Switch to tuned

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 47~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Felipe Borges <felipeborges@gnome.org> - 47~alpha-1
- Update to 47.alpha

* Tue May 28 2024 David King <amigadave@amigadave.com> - 46.2-1
- Update to 46.2

* Thu Apr 25 2024 Felipe Borges <felipeborges@gnome.org> - 46.1-2
- Enable location-services for the time being

* Mon Apr 22 2024 David King <amigadave@amigadave.com> - 46.1-1
- Update to 46.1

* Wed Mar 27 2024 Felipe Borges <felipeborges@gnome.org> - 46.0.1-1
- Update to 46.0.1

* Tue Mar 26 2024 David King <amigadave@amigadave.com> - 46.0-2
- Fix showing thunderbolt page

* Wed Mar 20 2024 David King <amigadave@amigadave.com> - 46.0-1
- Update to 46.0

* Wed Mar 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 46~rc-2
- goa-backend rebuild

* Wed Mar 06 2024 David King <amigadave@amigadave.com> - 46~rc-1
- Update to 46.rc

* Fri Feb 16 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 46~beta.2-2
- Dummy empty commit. This commit is just to test whether I can commit.

* Fri Feb 16 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 46~beta.2-1
- Update to 46~beta.2

* Fri Jan 26 2024 Nieves Montero <nmontero@redhat.com> - 46~alpha-1
- Update to 46~alpha

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Florian Weimer <fweimer@redhat.com> - 45.2-3
- Backport upstream patch to fix C compatibility issue

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 09 2023 Kalev Lember <klember@redhat.com> - 45.2-1
- Update to 45.2

* Mon Oct 30 2023 Kalev Lember <klember@redhat.com> - 45.1-2
- Remove unused glx-utils dependency (rhbz#2247096)

* Tue Oct 24 2023 Kalev Lember <klember@redhat.com> - 45.1-1
- Update to 45.1

* Tue Oct 17 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 45.0-3
- Remove unused clutter-gtk dependency

* Tue Oct 03 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 45.0-2
- Add patch to fix VPN configuration

* Tue Sep 19 2023 Kalev Lember <klember@redhat.com> - 45.0-1
- Update to 45.0

* Tue Aug 29 2023 Ray Strode <rstrode@redhat.com> - 45~rc-2
- Fetch default input sources if not-configured in gsettings

* Fri Aug 25 2023 Felipe Borges <felipeborges@gnome.org> - 45~rc-1
- Update to 45.rc

* Mon Aug 07 2023 Kalev Lember <klember@redhat.com> - 45~beta-1
- Update to 45.beta
- Require tecla instead of gkbd-keyboard-display

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 45~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Kalev Lember <klember@redhat.com> - 45~alpha-1
- Update to 45.alpha

* Fri Jun 30 2023 Kalev Lember <klember@redhat.com> - 44.3-1
- Update to 44.3

* Thu Jun 22 2023 Tomas Popela <tpopela@redhat.com> - 44.2-2
- Disable parental control (through malcontent) on RHEL

* Thu May 25 2023 Kalev Lember <klember@redhat.com> - 44.2-1
- Update to 44.2

* Fri Apr 21 2023 David King <amigadave@amigadave.com> - 44.1-1
- Update to 44.1

* Tue Mar 21 2023 David King <amigadave@amigadave.com> - 44.0-1
- Update to 44.0

* Tue Mar 07 2023 David King <amigadave@amigadave.com> - 44~rc-1
- Update to 44.rc

* Mon Feb 27 2023 Dominik Mierzejewski <dominik@greysector.net> - 44~beta-3
- Recommend gnome-bluetooth instead of requiring it

* Thu Feb 16 2023 Ray Strode <rstrode@redhat.com> - 44~beta-2
- Fix crash in users panel

* Wed Feb 15 2023 David King <amigadave@amigadave.com> - 44~beta-1
- Update to 44.beta

* Mon Feb 06 2023 David King <amigadave@amigadave.com> - 44~alpha-1
- Update to 44.alpha

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 43.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 30 2022 David King <amigadave@amigadave.com> - 43.2-1
- Update to 43.2

* Thu Oct 27 2022 David King <amigadave@amigadave.com> - 43.1-1
- Update to 43.1

* Fri Oct 21 2022 Adam Williamson <awilliam@redhat.com> - 43.0-2
- Backport MR #1478 to fix crash on empty EAP password edit (#2136471)

* Mon Sep 19 2022 Kalev Lember <klember@redhat.com> - 43.0-1
- Update to 43.0

* Tue Sep 06 2022 Kalev Lember <klember@redhat.com> - 43~rc-1
- Update to 43.rc

* Tue Aug 30 2022 Adam Williamson <awilliam@redhat.com> - 43~beta-2
- Backport MRs #1439 and #1440 to fix unapplied settings (#2118152)

* Fri Aug 12 2022 Kalev Lember <klember@redhat.com> - 43~beta-1
- Update to 43.beta

* Thu Jul 28 2022 Kalev Lember <klember@redhat.com> - 43~alpha-1
- Update to 43.alpha
- Drop upstreamed distro-logo.patch
- Drop upstreamed timezone-map.patch

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 42.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Kalev Lember <klember@redhat.com> - 42.3-2
- Rebuilt for libgnome-desktop soname bump

* Wed Jul 06 2022 David King <amigadave@amigadave.com> - 42.3-1
- Update to 42.3

* Wed Jun 29 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 42.2-2
- Update timezone map

* Fri May 27 2022 David King <amigadave@amigadave.com> - 42.2-1
- Update to 42.2

* Wed May 04 2022 Felipe Borges <felipeborges@gnome.org> - 42.1-3
- Recommend "malcontent-control" instead of requiring it

* Tue May 03 2022 David King <amigadave@amigadave.com> - 42.1-2
- Fix freeze in wired connection properties

* Wed Apr 27 2022 David King <amigadave@amigadave.com> - 42.1-1
- Update to 42.1

* Tue Apr 19 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 42.0-4
- Add patch to fix switches in online accounts panel

* Wed Apr 06 2022 Felipe Borges <felipeborges@gnome.org> - 42.0-3
- Fix printer setting preventing from scrolling media size list

* Wed Mar 30 2022 Adam Williamson <awilliam@redhat.com> - 42.0-2
- Backport MR #1272 to fix GOA helper window (#2064462)

* Fri Mar 18 2022 David King <amigadave@amigadave.com> - 42.0-1
- Udpate to 42.0

* Wed Mar 16 2022 Bastien Nocera <hadess@hadess.net> - 42~rc-2
- Add patch to prettify info strings

* Tue Mar 08 2022 David King <amigadave@amigadave.com> - 42~rc-1
- Update to 42.rc

* Thu Mar 03 2022 David King <amigadave@amigadave.com> - 42~beta-9
- Revert "Use SVG version of Fedora logos"

* Thu Mar 03 2022 David King <amigadave@amigadave.com> - 42~beta-8
- Refresh resources dependency patch from upstream

* Wed Mar 02 2022 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 42~beta-7
- Use SVG version of Fedora logos

* Wed Feb 23 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 42~beta-6
- Properly use %%autorelease

* Tue Feb 15 2022 Adam Williamson <awilliam@redhat.com> - 42~beta-1
- Update to 42~beta

* Mon Feb 14 2022 David King <amigadave@amigadave.com> - 41.4-1
- Update to 41.4

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 41.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 13 2021 Peter Hutterer <peter.hutterer@redhat.com> - 41.2-2
- Rebuild for libwacom soname bump

* Tue Dec 07 2021 Kalev Lember <klember@redhat.com> - 41.2-1
- Update to 41.2

* Fri Oct 29 2021 Kalev Lember <klember@redhat.com> - 41.1-1
- Update to 41.1

* Sat Sep 18 2021 Kalev Lember <klember@redhat.com> - 41.0-1
- Update to 41.0

* Wed Sep 08 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 41~rc1-1
- Update to 41.rc1

* Thu Aug 26 2021 Bastien Nocera <bnocera@redhat.com> - 41~beta-3
+ gnome-control-center-41~beta-3
- Parental controls fixes

* Tue Aug 24 2021 Kalev Lember <klember@redhat.com> - 41~beta-2
- Require malcontent and malcontent-control for parental controls support

* Mon Aug 23 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 41~beta-1
- Update to 41.beta

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 40.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Felipe Borges <feborges@redhat.com> - 40.0-10
- Enable parental controls (malcontent)

* Fri Apr 02 2021 Kalev Lember <klember@redhat.com> - 40.0-9
- Only enable power-profiles-daemon on F35+ and RHEL 9+

* Wed Mar 31 2021 Pete Walter <pwalter@fedoraproject.org> - 40.0-8
- Add back power-profiles-daemon once more

* Wed Mar 31 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 40.0-7
- Drop Recommends: power-profiles-daemon for F34

* Tue Mar 30 2021 Pete Walter <pwalter@fedoraproject.org> - 40.0-6
- Use recommends for a few more things

* Tue Mar 30 2021 Bastien Nocera <bnocera@redhat.com> - 40.0-4
- Drag power-profiles-daemon in for the power panel

* Mon Mar 29 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 40.0-3
- Update Fedora logos to larger versions

* Wed Mar 24 2021 Kalev Lember <klember@redhat.com> - 40.0-2
- Rebuilt

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 40~rc-1
- Update to 40.rc

* Wed Mar 10 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 40~beta-5
- Refresh distro logo patch
- Drop Recommends: vino, let vino die!

* Sun Mar 07 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 40~beta-4
- Fix modifications of the networks (Fixes: RHBZ#1932674)

* Wed Feb 24 2021 Felipe Borges <feborges@redhat.com> - 40~beta-3
- Include missing patch from 40~beta-2

* Tue Feb 23 2021 Felipe Borges <feborges@redhat.com> - 40~beta-2
- Fix error preventing the Region & Language panel from loading

* Sun Feb 21 2021 Kalev Lember <klember@redhat.com> - 40~beta-1
- Update to 40.beta

* Mon Feb 15 2021 Kalev Lember <klember@redhat.com> - 3.38.4-1
- Update to 3.38.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kalev Lember <klember@redhat.com> - 3.38.3-1
- Update to 3.38.3

* Fri Nov 20 2020 Kalev Lember <klember@redhat.com> - 3.38.2-2
- search: Check for either tracker 2.x or 3.x schemas

* Fri Nov 20 2020 Kalev Lember <klember@redhat.com> - 3.38.2-1
- Update to 3.38.2

* Tue Oct 13 2020 Kalev Lember <klember@redhat.com> - 3.38.1-2
- Add Recommends: nm-connection-editor for the network panel (#1887891)

* Mon Oct  5 2020 Kalev Lember <klember@redhat.com> - 3.38.1-1
- Update to 3.38.1

* Sat Sep 19 2020 Yaroslav Fedevych <yaroslav@fedevych.name> - 3.38.0-2
- Specify the minimum libnm version needed to build the package

* Sat Sep 12 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Sun Sep 06 2020 Kalev Lember <klember@redhat.com> - 3.37.92-1
- Update to 3.37.92

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 3.37.90-1
- Update to 3.37.90

* Tue Aug 04 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 3.37.3-4
- Add Recommends: gnome-color-manager for the color panel

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Kalev Lember <klember@redhat.com> - 3.37.3-1
- Update to 3.37.3

* Mon Jul 20 2020 Kalev Lember <klember@redhat.com> - 3.36.4-1
- Update to 3.36.4

* Wed Jun 03 2020 Kalev Lember <klember@redhat.com> - 3.36.3-1
- Update to 3.36.3

* Fri May 01 2020 Kalev Lember <klember@redhat.com> - 3.36.2-1
- Update to 3.36.2

* Tue Apr 28 2020 Felipe Borges <feborges@redhat.com> - 3.36.1-2
- Add "Model" row info for Lenovo devices

* Fri Mar 27 2020 Kalev Lember <klember@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Thu Mar 19 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 3.36.0-3
- No changes, bump revision to maintain upgrade path from F32

* Mon Mar 16 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 3.36.0-2
- Update distro-logo.patch to use fedora_vertical version of logo.

* Sat Mar 07 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Mon Feb 17 2020 Kalev Lember <klember@redhat.com> - 3.35.91-1
- Update to 3.35.91

* Mon Feb 03 2020 Bastien Nocera <bnocera@redhat.com> - 3.35.90-1
+ gnome-control-center-3.35.90-1
- Update to 3.35.90

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.34.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Kalev Lember <klember@redhat.com> - 3.34.2-3
- Backport a patch to fix the build with latest libgnome-desktop

* Mon Dec 09 2019 Michael Catanzaro <mcatanzaro@gnome.org> - 3.34.2-2
- Drop nm-connection-editor requires, per gnome-control-center#512
- To edit mobile broadband connections, install nm-connection-editor

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 3.34.2-1
- Update to 3.34.2

* Thu Oct 10 2019 Adam Williamson <awilliam@redhat.com> - 3.34.1-4
- Add patch to fix crash when selecting display with no modes (rhbz#1756553)

* Wed Oct 09 2019 Felipe Borges <feborges@redhat.com> - 3.34.1-3
- Add patch to fix parsing of addresses while adding printers (rhbz#1750394)

* Mon Oct 07 2019 Benjamin Berg <bberg@redhat.com> - 3.34.1-2
- Add patch to fix resetting of system wide format locale (rhbz#1759221)

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Sat Oct 05 2019 Michael Catanzaro <mcatanzaro@gnome.org> - 3.34.0.1-3
- Add patch to fix editing wired connection settings (rhbz#1750805)
- Remove broken remote printers patch

* Wed Oct 02 2019 Michael Catanzaro <mcatanzaro@gnome.org> - 3.34.0.1-2
- Add patch to fix crash when configuring remote printers

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 3.34.0.1-1
- Update to 3.34.0.1

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Kalev Lember <klember@redhat.com> - 3.33.3-2
- Remove libXxf86misc-devel BuildRequires as the package no longer exists

* Wed Jun 19 2019 Kalev Lember <klember@redhat.com> - 3.33.3-1
- Update to 3.33.3

* Fri May 24 2019 Kalev Lember <klember@redhat.com> - 3.32.2-1
- Update to 3.32.2

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.1-2
- Rebuild with Meson fix for #1699099

* Fri Mar 29 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0.1-1
- Update to 3.32.0.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Mon Mar 04 2019 Kalev Lember <klember@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Sat Feb 23 2019 Kevin Fenzi <kevin@scrye.com> - 3.31.90-2
- Add https://gitlab.gnome.org/GNOME/gnome-control-center/merge_requests/387.patch 
  to fix udisks crash

* Thu Feb 07 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Kalev Lember <klember@redhat.com> - 3.31.4-1
- Update to 3.31.4

* Tue Nov 20 2018 Pete Walter <pwalter@fedoraproject.org> - 3.30.2-3
- Recommend gnome-remote-desktop for the sharing panel

* Sat Nov 17 2018 Pete Walter <pwalter@fedoraproject.org> - 3.30.2-2
- Change bolt requires to recommends (#1643709)
- Change rygel requires to recommends

* Thu Nov 01 2018 Kalev Lember <klember@redhat.com> - 3.30.2-1
- Update to 3.30.2

* Thu Oct 11 2018 David Herrmann <dh.herrmann@gmail.com> - 3.30.1-4
- Reduce 'dbus-x11' dependency to 'dbus'. The xinit scripts are no longer the
  canonical way to start dbus, but the 'dbus' package is nowadays required to
  provide a user and system bus to its dependents.

* Wed Oct 10 2018 Benjamin Berg <bberg@redhat.com> - 3.30.1-3
- Add patch to improve background loading. The patch is not acceptable
  upstream as is, but is also a good improvement on the current situation
  (#1631002)

* Sun Oct 07 2018 Kalev Lember <klember@redhat.com> - 3.30.1-2
- Backport an upstream fix for a crash in the online accounts panel

* Wed Sep 26 2018 Kalev Lember <klember@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Sun Aug 12 2018 Kalev Lember <klember@redhat.com> - 3.29.90-1
- Update to 3.29.90

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 29 2018 Kalev Lember <klember@redhat.com> - 3.28.2-1
- Update to 3.28.2

* Wed May 23 2018 Pete Walter <pwalter@fedoraproject.org> - 3.28.1-4
- Change NetworkManager-wifi requires to recommends (#1478661)

* Tue May 22 2018 Ray Strode <rstrode@redhat.com> - 3.28.1-3
- Change vino requires to a vino recommends

* Fri Apr 13 2018 Kalev Lember <klember@redhat.com> - 3.28.1-2
- Backport new thunderbolt panel

* Tue Apr 10 2018 Pete Walter <pwalter@fedoraproject.org> - 3.28.1-1
- Rename control-center to gnome-control-center

## END: Generated by rpmautospec
