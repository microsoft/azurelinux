## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global tarball_version %%(echo %{version} | tr '~' '.')
%global major_version %(echo -n %{tarball_version} | sed 's/[.].*//')

%global gettext_version                         0.19.6
%global gnome_desktop_version                   44.0
%global glib2_version                           2.68.0
%global gtk4_version                            3.24.27
%global mutter_version                          49~beta
%global gsettings_desktop_schemas_version       40~rc
%global ibus_version                            1.5.24
%global gnome_settings_daemon_version           40~rc

%if 0%{?fedora} && 0%{?fedora} < 43
%bcond x11 1
%else
%bcond x11 0
%endif

Name:           gnome-kiosk
Version:        49.0
Release:        %autorelease
Summary:        Window management and application launching for GNOME

License:        GPL-2.0-or-later
URL:            https://gitlab.gnome.org/GNOME/gnome-kiosk
Source0:        https://download.gnome.org/sources/%{name}/%{major_version}/%{name}-%{tarball_version}.tar.xz

%if %{with x11}
Provides:       firstboot(windowmanager) = %{name}
%endif

BuildRequires:  dconf
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext >= %{gettext_version}
BuildRequires:  git
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  meson
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-desktop-4) >= %{gnome_desktop_version}
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(ibus-1.0) >= %{ibus_version}
BuildRequires:  pkgconfig(libmutter-17) >= %{mutter_version}

Requires:       gnome-settings-daemon%{?_isa} >= %{gnome_settings_daemon_version}
Requires:       gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Recommends:     xorg-x11-server-Xwayland

%description
GNOME Kiosk provides a desktop enviroment suitable for fixed purpose, or
single application deployments like wall displays and point-of-sale systems.

%package search-appliance
Summary:        Example search application application that uses GNOME Kiosk
Requires:       %{name} = %{version}-%{release}
Requires:       firefox
Requires:       gnome-session
BuildArch:      noarch

%description search-appliance
This package provides a full screen firefox window pointed to google.

%package script-session
Summary:        Basic session used for running kiosk application from shell script
Requires:       %{name} = %{version}-%{release}
Recommends:     gedit
Requires:       gnome-session
BuildArch:      noarch

%description script-session
This package generates a shell script and the necessary scaffolding to start that shell script within a kiosk session.

%prep
%autosetup -S git -n %{name}-%{tarball_version}

%build
%meson
%meson_build

%install
%meson_install

%if !%{with x11}
rm -rf %{buildroot}%{_datadir}/xsessions
rm -f %{buildroot}%{_userunitdir}/org.gnome.Kiosk@x11.service
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Kiosk.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.Kiosk.SearchApp.desktop

%files
%license COPYING
%doc NEWS README.md CONFIG.md
%{_bindir}/gnome-kiosk
%{_datadir}/applications/org.gnome.Kiosk.desktop
%{_datadir}/dconf/profile/gnomekiosk
%{_datadir}/gnome-kiosk/gnomekiosk.dconf.compiled
%{_userunitdir}/org.gnome.Kiosk.target
%{_userunitdir}/org.gnome.Kiosk@wayland.service
%if %{with x11}
%{_userunitdir}/org.gnome.Kiosk@x11.service
%endif

%files -n gnome-kiosk-search-appliance
%{_userunitdir}/gnome-session@org.gnome.Kiosk.SearchApp.target.d/session.conf
%{_userunitdir}/org.gnome.Kiosk.SearchApp.service
%{_datadir}/applications/org.gnome.Kiosk.SearchApp.desktop
%{_datadir}/gnome-session/sessions/org.gnome.Kiosk.SearchApp.session
%{_datadir}/wayland-sessions/org.gnome.Kiosk.SearchApp.Session.desktop
%if %{with x11}
%{_datadir}/xsessions/org.gnome.Kiosk.SearchApp.Session.desktop
%endif

%files -n gnome-kiosk-script-session
%{_bindir}/gnome-kiosk-script
%{_userunitdir}/gnome-session@gnome-kiosk-script.target.d/session.conf
%{_userunitdir}/org.gnome.Kiosk.Script.service
%{_datadir}/applications/org.gnome.Kiosk.Script.desktop
%{_datadir}/gnome-session/sessions/gnome-kiosk-script.session
%{_datadir}/wayland-sessions/gnome-kiosk-script-wayland.desktop
%if %{with x11}
%{_datadir}/xsessions/gnome-kiosk-script-xorg.desktop
%endif

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 49.0-4
- Latest state for gnome-kiosk

* Wed Oct 15 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49.0-3
- Code style cleanup

* Wed Oct 08 2025 Olivier Fourdan <ofourdan@redhat.com> - 49.0-2
- Add Xwayland as weak dependency

* Tue Sep 16 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49.0-1
- Update to 49.0

* Fri Sep 05 2025 Adam Williamson <awilliam@redhat.com> - 49~rc-1
- Update to 49.rc

* Fri Sep 05 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49~alpha.1.2-2
- Bump NVR

* Mon Aug 18 2025 nmontero <nmontero@redhat.com> - 49~alpha.1.2-1
- Update to 49~alpha.1.2

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 49~alpha.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Milan Crha <mcrha@redhat.com> - 49~alpha.0-1
- Update to 49.alpha.0

* Fri May 30 2025 Neal Gompa <ngompa@fedoraproject.org> - 48.0-5
- Delete unwanted X11 files when X11 is disabled

* Fri May 30 2025 Neal Gompa <ngompa@fedoraproject.org> - 48.0-4
- Disable X11 for Fedora 43+ and RHEL

* Thu Apr 03 2025 Olivier Fourdan <ofourdan@redhat.com> - 48.0-3
- Specify the right configuration file name

* Thu Apr 03 2025 Olivier Fourdan <ofourdan@redhat.com> - 48.0-2
- Add CONFIG.md for documentation

* Mon Mar 17 2025 nmontero <nmontero@redhat.com> - 48.0-1
- Update to 48.0

* Thu Mar 06 2025 nmontero <nmontero@redhat.com> - 48~rc-1
- Update to 48~rc

* Thu Mar 06 2025 Olivier Fourdan <ofourdan@redhat.com> - 48~alpha-3
- search-app: Add systemd session files

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 48~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Florian Müllner <fmuellner@redhat.com> - 48~alpha-1
- Update to 48.alpha

* Fri Sep 20 2024 nmontero <nmontero@redhat.com> - 47.0-1
- Update to 47.0

* Wed Sep 18 2024 nmontero <nmontero@redhat.com> - 47~rc-1
- Update to 47.rc

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 47~alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Ray Strode <rstrode@redhat.com> - 47~alpha-2
- Bump deps

* Wed Jul 03 2024 Ray Strode <rstrode@redhat.com> - 47~alpha-1
- Update to 47.alpha

* Fri Mar 29 2024 David King <amigadave@amigadave.com> - 46.0-1
- Update to 46.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 Kalev Lember <klember@redhat.com> - 45.0-2
- Build against mutter API version 14

* Tue Sep 19 2023 Kalev Lember <klember@redhat.com> - 45.0-1
- Update to 45.0

* Tue Sep 19 2023 Kalev Lember <klember@redhat.com> - 45~rc-3
- Fix the build

* Sun Sep 10 2023 Ray Strode <rstrode@redhat.com> - 45~rc-2
- Update gnome-desktop buildreq

* Sun Sep 10 2023 Ray Strode <rstrode@redhat.com> - 45~rc-1
- Update to 45.rc

* Tue Aug 08 2023 Kalev Lember <klember@redhat.com> - 44.0-3
- Build against mutter 45

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 44.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Mar 21 2023 David King <amigadave@amigadave.com> - 44.0-1
- Update to 44.0

* Mon Mar 06 2023 David King <amigadave@amigadave.com> - 44~rc-1
- Update to 44.rc

* Thu Feb 16 2023 Kevin Fenzi <kevin@scrye.com> - 44~beta-3
- Add BuildRequires on dconf and add 2 profile files produced.

* Thu Feb 16 2023 Adam Williamson <awilliam@redhat.com> - 44~beta-2
- Update sources (sigh)

* Thu Feb 16 2023 Adam Williamson <awilliam@redhat.com> - 44~beta-1
- Update to 44-beta, rebuild against new libmutter

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 43.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 20 2022 Kalev Lember <klember@redhat.com> - 43.0-1
- Update to 43.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 42.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Adam Williamson <awilliam@redhat.com> - 42.0-2
- Bump mutter requirements and rebuild against mutter 43

* Tue Mar 22 2022 David King <amigadave@amigadave.com> - 42.0-1
- Update to 42.0

* Mon Jan 24 2022 David King <amigadave@amigadave.com> - 42~alpha-1
- Update to 42.alpha

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 41.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 17 2022 David King <amigadave@amigadave.com> - 41.0-2
- Build against mutter 42 (#2040955)

* Thu Sep 23 2021 Kalev Lember <klember@redhat.com> - 41.0-1
- Update to 41.0

* Wed Aug 18 2021 Ray Strode <rstrode@redhat.com> - 41~beta-2
- Update mutter dep

* Wed Aug 18 2021 Ray Strode <rstrode@redhat.com> - 41~beta-1
- Update to 41.beta

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Ray Strode <rstrode@redhat.com> - 40.0-1
- Update to 40.0

* Wed May 12 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-12
- Fix crash

* Thu May 06 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-11
- Fix window ordering bug

* Wed Apr 28 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-10
- Fix desktop file

* Fri Apr 23 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-9
- Remove duplicate vprovides

* Fri Apr 23 2021 Radek Vykydal <rvykydal@redhat.com> - 40~alpha-8
- Add vprovides so initial-setup can use this

* Fri Apr 23 2021 Radek Vykydal <rvykydal@redhat.com> - 40~alpha-7
- Add gnome-kiosk among window managers usable by initial-setup

* Wed Apr 21 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-6
- Fix keyboard layouts getting out of sync in anaconda

* Tue Apr 20 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-5
- Fix typos in last patch

* Tue Apr 20 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-4
- Fix infinite loop

* Mon Apr 19 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-3
- Fix crash

* Mon Apr 19 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-2
- Make work better with Anaconda
- Work with 3rd party keyboard layout selectors
- Be less aggressive about fullscreening windows

* Tue Apr 13 2021 Ray Strode <rstrode@redhat.com> - 40~alpha-1
- Initial import
## END: Generated by rpmautospec
