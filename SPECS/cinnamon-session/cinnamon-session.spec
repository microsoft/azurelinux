# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 829519b1d36668e4a178f15900bd49af55548926
%global date 20231109
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

%global cinnamon_desktop_version 6.4.0

Summary: Cinnamon session manager
Name:    cinnamon-session
Version: 6.4.0
Release: 4%{?dist}
# Automatically converted from old format: GPLv2+ and LGPLv2+ - review is highly recommended.
License: GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+
URL:     https://github.com/linuxmint/%{name}
%if 0%{?tag:1}
Source0: %url/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0: %url/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif
Patch0:  %url/commit/8042c7f4756773b32e30f902d2cb05c865b9f6d7.patch

ExcludeArch: %{ix86}

Requires: system-logos
# Needed for cinnamon-settings-daemon
Requires: cinnamon-control-center-filesystem

# pull in dbus-x11, see bug 209924
Requires: dbus-x11

# an artificial requires to make sure we get dconf, for now
Requires: dconf

Requires: cinnamon-desktop >= %{cinnamon_desktop_version}

BuildRequires: pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0) >= 2.37.3
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(pango)
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(ice)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xapp) >= 1.4.6
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xtrans)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(cinnamon-desktop) >= %{cinnamon_desktop_version}
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: meson
BuildRequires: gcc
BuildRequires: intltool
BuildRequires: python3-packaging
BuildRequires: xmlto

%description
Cinnamon-session manages a Cinnamon desktop or GDM login session. It starts up
the other core components and handles logout and saving the session.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif


%build
%meson
%meson_build

%install
%meson_install


%ldconfig_scriptlets


%files
%doc AUTHORS README
%doc %{_mandir}/man*/*
%license COPYING
%{_bindir}/*
%{_libexecdir}/cinnamon-session-binary
%{_libexecdir}/cinnamon-session-check-accelerated
%{_libexecdir}/cinnamon-session-check-accelerated-helper
%{_datadir}/cinnamon-session/
%{_datadir}/icons/hicolor/*/apps/cinnamon-session-properties.png
%{_datadir}/icons/hicolor/scalable/apps/cinnamon-session-properties.svg
%{_datadir}/glib-2.0/schemas/org.cinnamon.SessionManager.gschema.xml

%changelog
* Wed Sep 03 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.0-4
- Fix systemd inhibitor issue

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Nov 27 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.0-1
- Update to 6.4.0

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 6.2.1-2
- convert license to SPDX

* Fri Jul 19 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.1-1
- Update to 6.2.1

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-3
- Remove polkit-gnome requires

* Thu Jun 13 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-2
- Fix restart/shutdown

* Wed Jun 12 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-1
- Update to 6.2.0

* Sat May 04 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.4-1
- Update to 6.0.4 release

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.1-3
- AAdd buildrequires python3-packaging

* Sat Jan 06 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.1-2
- Make sure wayland sessions get a login shell

* Tue Nov 28 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.1-1
- Update to 6.0.1 release

* Tue Nov 28 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.0-3
- Unset some environment variables on systemd

* Wed Nov 22 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.0-2
- Fix glib warning

* Sun Nov 19 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.0-1
- Update to 6.0.0 release

* Thu Nov 09 2023 Leigh Scott <leigh123linux@gmail.com> - 5.9.0-1.20231109git829519b
- Update to git snapshot

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 23 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.1-1
- Update to 5.8.1 release

* Fri Jun 02 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.0-1
- Update to 5.8.0 release

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 18 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.0-1
- Update to 5.6.0 release

* Sat Sep 03 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-3
- Accept Desktop Entry Specification v1.5

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 10 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-1
- Update to 5.4.0 release

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 19 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.0-1
- Update to 5.2.0 release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 28 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.0-1
- Update to 5.0.0 release

* Fri Apr 09 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.0-3
- Fixes for desktop spec and systemd user env blacklist

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.0-1
- Update to 4.8.0 release

* Tue Aug 11 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.2-1
- Update to 4.6.2 release

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 27 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.1-1
- Update to 4.6.1 release

* Tue May 12 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.0-1
- Update to 4.6.0 release

* Fri Feb 14 2020 Leigh Scott <leigh123linux@googlemail.com> - 4.4.1-1
- Update to 4.4.1 release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-1
- Update to 4.4.0 release

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 04 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.1-1
- Update to 4.2.1 release

* Sun Jun 23 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-1
- Update to 4.2.0 release

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.0-1
- Update to 4.0.0 release

* Sun Oct 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.2-2
- Drop EPEL/RHEL support

* Thu Aug 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.2-1
- Update to 3.8.2 release

* Fri Jul 13 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.1-3
- Add buildrequires gcc

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.1-1
- Update to 3.8.1 release

* Wed Apr 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.0-1
- Update to 3.8.0 release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.6.1-2
- Remove obsolete scriptlets

* Wed Nov 22 2017 Björn Esser <besser82@fedoraproject.org> - 3.6.1-1
- update to 3.6.1 release

* Tue Nov 21 2017 Björn Esser <besser82@fedoraproject.org> - 3.6.0-2
- Add patch to optionally disable DBus user session

* Mon Oct 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.0-1
- update to 3.6.0 release

* Wed Sep 13 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.2-4
- Previous commit isn't needed for EPEL7

* Sat Sep 09 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.2-3
- Add patch for properly restarting dbus user-session

* Wed Aug 30 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.2-2
- Adjustments for EPEL7

* Wed Aug 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.2-1
- update to 3.4.2 release

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 3.4.1-4
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.1-3
- Add build requires mesa-libGL-devel

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.1-1
- update to 3.4.1 release

* Fri May 26 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.0-6
- Updated patch for g-s-d blacklist

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.0-5
- Updated patch to update environment for dbus and systemd user-session

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.0-4
- Updated patch to update environment for dbus and systemd user-session

* Sun May 07 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.0-3
- Updated patch to update environment for dbus and systemd user-session

* Sat May 06 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.0-2
- Add patch to update environment for dbus and systemd user-session

* Thu May 04 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.0-1
- update to 3.4.0 release

* Sun Apr 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.0-0.2.20170423gitd87d97d>
- update to git snapshot

* Fri Mar 31 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.0-4
- remove polkit-desktop-policy requires

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.0-2
- blacklist gnome-settings-daemon plugins from auto starting

* Mon Nov 07 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.2.0-1
- update to 3.2.0 release

* Wed Jul 13 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.1-3
- Make QT5 apps configurable using the qt5ct tool

* Wed Jul 13 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.1-2
- patch to fix the qt override

* Sat May 21 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.1-1
- update to 3.0.1 release

* Tue May 17 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.0-3
- add setting for gtk overlay scrollbars

* Sat May 14 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.0-2
- fix gnome-keyring autostart issue

* Sat Apr 23 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.0-1
- update to 3.0.0 release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 09 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.2-2
- rebuilt

* Mon Nov 09 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.2-1
- update to 2.8.2 release

* Sat Oct 17 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.0-1
- update to 2.8.0 release

* Wed Jul 15 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.3-2
- disable overlay scrollbars

* Sun Jun 28 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.3-1
- update to 2.6.3 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.1-1
- update to 2.6.1 release

* Wed May 20 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.0-1
- update to 2.6.0 release

* Wed May 06 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.5.1-0.3.git2a18785
- update to git snapshot

* Tue May 05 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.5.1-0.2.gitfc7111e
- blacklist xscreensaver from autostarting

* Tue May 05 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.5.1-0.1.gitfc7111e
- update to git snapshot

* Sun Feb 22 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-5
- set clutter env for f22+

* Tue Jan 20 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-4
- patch cinnamon-session-properties for gtk-3.14 changes

* Fri Nov 21 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-3
- blacklist gnome-initial-setup from autostart (bz 1165893)

* Thu Nov 20 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-2
- revert upstream commit (somethings are rotten and should remain dead)

* Sat Nov 08 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.1-1
- update to 2.4.1

* Fri Oct 31 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-1
- update to 2.4.0

* Mon Oct 06 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.3.git8c1b918
- use upstream commits for invisible session properties dialog (gtk-3.14)

* Mon Oct 06 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.2.git8c1b918
- invisible session properties dialog (gtk-3.14)

* Tue Sep 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.1.git8c1b918
- update to latest git

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 27 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.2-1
- update to 2.2.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.1-1
- update to 2.2.1

* Fri May 09 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-3
- revert disable tracker from session startup

* Wed May 07 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-2
- Patch to prevent tracker crapware from autostarting

* Sat Apr 12 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-1
- update to 2.2.0

* Wed Apr 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.6-1
- update to 2.0.6
- readd Br pangox-compat-devel for epel
- add upstream fix for clutter xinput (bz 873434)

* Mon Jan 13 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.5-2
- make changes for epel7

* Sun Nov 10 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.5-1
- update to 2.0.5

* Thu Nov 07 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.4-2
- fix upower compile issue

* Sun Nov 03 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.4-1
- update to 2.0.4
- drop upstream patches

* Wed Oct 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-2
- fix screeensaver command

* Wed Oct 09 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-1
- update to 2.0.1
- drop upstream patches

* Sun Oct 06 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-2
- add patch so user switch works in lightdm

* Wed Oct 02 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-1
- update to 2.0.0
- drop upstream patches

* Mon Sep 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.2-1
- update to 1.9.2

* Tue Sep 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.12.git405f80d
- add some build conditionals

* Sun Sep 15 2013 Rex Dieter <rdieter@fedoraproject.org> 1.0.0-0.11.git405f80d
- support systemd_login1 suspend/hibernate

* Sun Aug 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.10.git405f80d
- update to latest git
- add requires cinnamon-desktop

* Thu Aug 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.9.git58710ea
- rebuilt

* Tue Aug 06 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.8.git58710ea
- add systemd patch

* Sun Jul 28 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.7.git58710ea
- remove requires notification-daemon
- fix missing menu icon

* Thu Jul 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.6.git58710ea
- patch to remove session-migration (ubuntu leftover)

* Wed Jul 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.5.git58710ea
- don't delete the glade file as we need it

* Wed Jul 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.4.git58710ea
- change require gnome control-center to cinnamon

* Wed Jul 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.3.git58710ea
- update to latest git

* Tue Jul 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.2.gitdf909ee
- update to latest git

* Sat May 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.0.0-0.1.git090f4bd
- Initial build

