# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global gtk3_version    %(pkg-config --modversion gtk+-3.0 2>/dev/null || echo bad)
%global gtk4_version    %(pkg-config --modversion gtk4 2>/dev/null || echo bad)
%global glib2_version   %(pkg-config --modversion glib-2.0 2>/dev/null || echo bad)
%global nm_version      1:1.16.0
%global libnma_version  1.8.27
%global obsoletes_ver   1:0.9.7

%if 0%{?fedora} > 31 || 0%{?rhel} > 8
%bcond_with libnma_gtk4
%else
%bcond_without libnma_gtk4
%endif

%if 0%{?fedora} || 0%{?rhel} < 9
%bcond_without appindicator
%else
%bcond_with appindicator
%endif

Name: network-manager-applet
Summary: A network control and status applet for NetworkManager
Version: 1.36.0
Release: 7%{?dist}
License: GPL-2.0-or-later
URL: http://www.gnome.org/projects/NetworkManager/
Obsoletes: NetworkManager-gnome < %{obsoletes_ver}

Source: https://download.gnome.org/sources/network-manager-applet/1.36/%{name}-%{version}.tar.xz
Patch1: 0001-nm-applet-no-notifications.patch

%if ! 0%{?flatpak}
Requires: NetworkManager >= %{nm_version}
%endif
Requires: nm-connection-editor%{?_isa} = %{version}-%{release}
Requires: libnma%{?_isa} >= %{libnma_version}

BuildRequires: NetworkManager-libnm-devel >= %{nm_version}
BuildRequires: libnma-devel >= %{libnma_version}
BuildRequires: ModemManager-glib-devel >= 1.0
BuildRequires: glib2-devel >= 2.32
BuildRequires: gtk3-devel >= 3.10
%if %{with libnma_gtk4}
BuildRequires: gtk4-devel >= 3.96
%endif
BuildRequires: gobject-introspection-devel >= 0.10.3
BuildRequires: gettext-devel
BuildRequires: /usr/bin/autopoint
BuildRequires: pkgconfig
BuildRequires: meson
BuildRequires: intltool
BuildRequires: gtk-doc
BuildRequires: desktop-file-utils
BuildRequires: iso-codes-devel
BuildRequires: libsecret-devel >= 0.12
BuildRequires: jansson-devel
BuildRequires: gcr-devel
BuildRequires: libselinux-devel
BuildRequires: mobile-broadband-provider-info-devel
%if %{with appindicator}
BuildRequires: libappindicator-gtk3-devel
%endif
%if 0%{?fedora} || 0%{?rhel} < 9
BuildRequires: libdbusmenu-gtk3-devel
%endif

%description
This package contains a network control and status notification area applet
for use with NetworkManager.

%package -n nm-connection-editor
Summary: A network connection configuration editor for NetworkManager
Requires: libnma%{?_isa} >= %{libnma_version}

%description -n nm-connection-editor
This package contains a network configuration editor and Bluetooth modem
utility for use with NetworkManager.


%package -n nm-connection-editor-desktop
Summary: The desktop file for nm-connection-editor
Requires: nm-connection-editor%{?_isa} = %{version}-%{release}

%description -n nm-connection-editor-desktop
This package contains the desktop file and appdata for nm-connection-editor.
Without it, the nm-connection-editor cannot be started from the desktop
environment.


%prep
%autosetup -p1

%build
%meson \
    -Dselinux=true \
%if %{with appindicator}
    -Dappindicator=auto
%else
    -Dappindicator=no
%endif
%meson_build

%install
%meson_install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/gnome-vpn-properties

%find_lang nm-applet
cat nm-applet.lang >> %{name}.lang

# validate .desktop and autostart files
desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nm-applet.desktop
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/nm-connection-editor.desktop

%check
%meson_test


%files
%{_bindir}/nm-applet
%{_datadir}/applications/nm-applet.desktop
%{_datadir}/icons/hicolor/22x22/apps/nm-adhoc.png
%{_datadir}/icons/hicolor/22x22/apps/nm-insecure-warn.png
%{_datadir}/icons/hicolor/22x22/apps/nm-mb-roam.png
%{_datadir}/icons/hicolor/22x22/apps/nm-secure-lock.png
%{_datadir}/icons/hicolor/22x22/apps/nm-signal-*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-stage*-connecting*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-tech-*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-vpn-active-lock.png
%{_datadir}/icons/hicolor/22x22/apps/nm-vpn-connecting*.png
%{_datadir}/icons/hicolor/22x22/apps/nm-wwan-tower.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
%{_datadir}/GConf/gsettings/nm-applet.convert
%{_sysconfdir}/xdg/autostart/nm-applet.desktop
%{_mandir}/man1/nm-applet*
%doc NEWS CONTRIBUTING
%license COPYING

# Yes, lang files for the applet go in nm-connection-editor RPM since it
# is the RPM that everything else depends on
%files -n nm-connection-editor -f %{name}.lang
%{_bindir}/nm-connection-editor
%{_datadir}/icons/hicolor/*/apps/nm-device-*.*
%{_datadir}/icons/hicolor/*/apps/nm-no-connection.*
%{_datadir}/icons/hicolor/16x16/apps/nm-vpn-standalone-lock.png
%{_mandir}/man1/nm-connection-editor*
%dir %{_datadir}/gnome-vpn-properties


%files -n nm-connection-editor-desktop
%{_datadir}/applications/nm-connection-editor.desktop
%{_datadir}/metainfo/nm-connection-editor.appdata.xml


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Richard W.M. Jones <rjones@redhat.com> - 1.36.0-4
- Rebuild for Jansson 2.14
  (https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/3PYINSQGKQ4BB25NQUI2A2UCGGLAG5ND/)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Íñigo Huguet <ihuguet@redhat.com> - 1.36.0-1
- Update to 1.36.0 release

* Thu Nov  2 2023 Íñigo Huguet <ihuguet@redhat.com> - 1.34.0-2
- migrate to SPDX license

* Mon Oct 16 2023 Beniamino Galvani <bgalvani@redhat.com> - 1.34.0-1
- Update to 1.34.0 release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 16 2023 Lubomir Rintel <lkundrak@v3.sk> - 1.32.0-1
- Update to 1.32.0 release

* Fri Feb 17 2023 Lubomir Rintel <lkundrak@v3.sk> - 1.30.0-3
- applet: use appindicator if we can outside of X11

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 07 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.30.0-1
- Update to 1.30.0 release

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 07 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.28.0-1
- Update to 1.28.0 release

* Fri May 13 2022 Thomas Haller <thaller@redhat.com> - 1.26.0-2
- Rebuild and spec file cleanup

* Tue Mar 29 2022 Ana Cabral <acabral@redhat.com> - 1.26.0-1.1
- Update to 1.26.0 release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 19 2021 Beniamino Galvani <bgalvani@redhat.com> - 1.24.0-1.1
- Update to 1.24.0 release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 10 2021 Beniamino Galvani <bgalvani@redhat.com> - 1.22.0-1
- Update to 1.22.0 release
- editor: fix crash evaluating secondary connections (rh #1942905)

* Wed Feb  3 2021 Thomas Haller <thaller@redhat.com> - 1.20.0-4
- Update to 1.20.0 release
- editor: drop NotShowIn=GNOME
- Use wireless-security code from libnma
- Add flatpak build configuration
- applet: hide unmanaged ethernet devices in nm-applet
- applet: fix Wi-Fi scan requests with appindicator
- editor: fix drop down list for connection.secondaries

* Tue Feb  2 2021 Thomas Haller <thaller@redhat.com> - 1.18.0-4
- Move desktop file to new nm-connection-editor-desktop package (rh #1923262)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan  6 2021 Thomas Haller <thaller@redhat.com> - 1.18.0-3
- Build without libdbusmenu-gtk3-devel on RHEL >=9

* Wed Nov 18 2020 Antonio Cardace <acardace@redhat.com> - 1.18.0-2
- Build without libappindicator-gtk3-devel on RHEL >=9

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Thomas Haller <thaller@redhat.com> - 1.18.0-1
- Update to 1.18.0 release
- Enable build with appindicator by default.
- Add WireGuard support to the editor.
- Support OWE (Opportunistic Wireless Encryption) in the editor.
- Fix crash when disposing VPN secret dialog.

* Thu Apr 30 2020 Ivan Mironov <mironov.ivan@gmail.com> - 1.16.0-2
- Build with libappindicator which enables Status Notifier Item support

* Sat Mar  7 2020 Thomas Haller <thaller@redhat.com> - 1.16.0-1
- Update to 1.16.0 release
- Move libnma to separate, independent project
- move org.gnome.nm-applet.gschema.xml to libnma

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.24-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 09 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.24-1
- Update to 1.8.24 release
- Enable experimental GTK4 build on Rawhide

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.22-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.22-1
- Update to 1.8.22 release

* Wed Feb 27 2019 Beniamino Galvani <bgalvani@redhat.com> - 1.8.20-2
- Fix parsing of hints in wifi secret dialog (rh #1679251)
- Import other upstream fixes after 1.8.20

* Fri Feb 08 2019 Beniamino Galvani <bgalvani@redhat.com> - 1.8.20-1
- Update to 1.8.20 release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 19 2019 Beniamino Galvani <bgalvani@redhat.com> - 1.8.18-3
- wifi-dialog: fix widget hiding logic (rh #1665653)

* Fri Sep 21 2018 Thomas Haller <thaller@redhat.com> - 1.8.18-2
- libnma: fix wrongly showing hidden GUI elements (rh #1626397) (2)

* Fri Sep  7 2018 Thomas Haller <thaller@redhat.com> - 1.8.18-1
- Update to 1.8.18 release
- libnma: fix wrongly showing hidden GUI elements (rh #1626397)

* Sat Aug 11 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.8.16-1
- Update to 1.8.16 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.14-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.8.14-1
- Update to 1.8.14 release

* Mon Jun  4 2018 Thomas Haller <thaller@redhat.com> - 1.8.12-4
- applet: fix double-free in ap-menu-item (rh #1585302)

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 1.8.12-3
- Fix GGO #1 (nm-connection-editor --keep-above fails with any other arg)

* Mon May 28 2018 Lubomir Rintel <lkundrak@v3.sk> - 1.8.12-2
- Update to 1.8.12 release

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.10-2.2
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.10-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb  4 2018 Thomas Haller <thaller@redhat.com> - 1.8.10-2
- fix double-free handling VPN data in nm-applet (rh #1541565)
- fix certificate chooser for no available modules (bgo #785674)

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.10-1.2
- Switch to %%ldconfig_scriptlets

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.10-1.1
- Remove obsolete scriptlets

* Tue Dec 19 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.8.10-1
- Update to 1.8.10 release

* Mon Dec 18 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.8.8-1
- Update to 1.8.8 release

* Mon Nov 13 2017 Kalev Lember <klember@redhat.com> - 1.8.6-3
- Backport an upstream patch to fix generated .pc file

* Wed Nov 08 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.8.6-2
- Meson build fixups

* Tue Nov 07 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.8.6-1
- Update to 1.8.6 release
- Switch to Meson build system

* Wed Sep 20 2017 Thomas Haller <thaller@redhat.com> - 1.8.4-1
- Update to 1.8.4 release

* Mon Sep 18 2017 Beniamino Galvani <bgalvani@redhat.com> - 1.8.2-4
- applet: fix status icon when a VPN has the default route (rh#1471510)

* Wed Aug 23 2017 Thomas Haller <thaller@redhat.com> - 1.8.2-3
- libnma: fix certificate picker for empty certificates (rh#1469852)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.8.2-2
- editor: fix a crash on connection save

* Tue Jun 13 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.8.2-1
- Update to network-manager-applet 1.8.2 release

* Fri Jun 09 2017 Lubomir Rintel <lrintel@redhat.com> - 1.8.0-2
- editor: fix crash when destroying 802.1x page (rh #1458567)
- po: update Japanese translation (rh #1379642)

* Wed May 10 2017 Thomas Haller <thaller@redhat.com> - 1.8.0-1
- Update to 1.8.0 release

* Fri Mar 24 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.8.0-0.1
- Update to a snapshot of network-manager-applet 1.8 release

* Mon Mar 06 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.4.6-1
- Update to network-manager-applet 1.4.6 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Lubomir Rintel <lkundrak@v3.sk> - 1.4.4-1
- Update to network-manager-applet 1.4.4 release

* Wed Aug 24 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.4.0-1
- Update to network-manager-applet 1.4.0 release

* Thu Aug  4 2016 Francesco Giudici <fgiudici@redhat.com> - 1.2.4-1
- Update to network-manager-applet 1.2.4 release

* Wed May 11 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.2-1
- Update to network-manager-applet 1.2.2 release

* Wed Apr 20 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-1
- Update to network-manager-applet 1.2.0 release

* Tue Apr  5 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-0.3.rc1
- Update to network-manager-applet 1.2-rc1

* Tue Mar 29 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-0.3.beta3
- Update to network-manager-applet 1.2-beta3

* Mon Mar 07 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-0.3.beta2
- Update to network-manager-applet 1.2-beta2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-0.3.beta1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-0.2.beta1
- Update to network-manager-applet 1.2-beta1

* Thu Sep  3 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.2.0-0.1.20150903git807cbdf
- Update to 1.2 git snapshot:
- Add libnma subpackages
- Add support for libnm-based properties plugins

* Wed Sep  2 2015 Thomas Haller <thaller@redhat.com> - 1.0.6-4
- show tooltip when connect button is disabled due to invalid connection (rh #1247885)

* Tue Sep  1 2015 Jiří Klimeš <jklimes@redhat.com> - 1.0.6-3
- libnm-gtk: fix a possible crash on password widget destroy (rh #1254043)

* Thu Aug 27 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.0.6-2
- Re-add an accidentally removed patch

* Thu Aug 27 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.0.6-1
- Update to 1.0.6 release

* Wed Jul 15 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.0.4-2
- Version the newly added ABI

* Tue Jul 14 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.0.4-1
- Update to 1.0.4 release

* Tue Jul 07 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.0.4-0.1.git20160702.25368df
- Update to a later Git snapshot

* Thu Jun 18 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.0.4-0.1.git20160615.28a0e28
- Update to a later Git snapshot

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Lubomir Rintel <lkundrak@v3.sk> - 1.0.2-1
- Update to 1.0.2 release

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.0.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Dec 22 2014 Dan Williams <dcbw@redhat.com> - 1.0.0-1
- Update to 1.0

* Mon Dec  1 2014 Jiří Klimeš <jklimes@redhat.com> - 0.9.10.1-1.git20141201.be5a9db
- update to latest git snapshot of 0.9.10 (git20141201 sha:be5a9db)

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.9.0-15.git20140424
- Backport a patch to hide nm-connection-editor launcher in GNOME

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.0-14.git20140424
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.9.0-13.git20140424
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.0-12.git20140424
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 0.9.9.0-11.git20140424
- Drop gnome-icon-theme dependency

* Thu Apr 24 2014 Jiří Klimeš <jklimes@redhat.com> - 0.9.9.0-10.git20140424
- update to latest git snapshot (git20140424 sha:9ba9c3e)

* Mon Mar 24 2014 Dan Winship <danw@redhat.com> - 0.9.9.0-9.git20140123
- Add ModemManager-glib-devel to BuildRequires

* Thu Jan 23 2014 Jiří Klimeš <jklimes@redhat.com> - 0.9.9.0-8.git20140123
- update to latest git snapshot (git20140123 sha:5d4f17e)
- applet: fix crash when "CA certificate is not required" (rh #1055535)

* Fri Dec 20 2013 Kevin Fenzi <kevin@scrye.com> 0.9.9.0-8.git20131028
- Remove bluetooth plugin, doesn't work with new gnome-bluetooth/bluez5

* Mon Oct 28 2013 Dan Winship <danw@redhat.com> - 0.9.9.0-7.git20131028
- update to latest git snapshot
- re-enable nm-applet on certain non-GNOME-Shell desktops (rh #1017471)

* Fri Sep 13 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-6.git20130906
- libnm-gtk: fix for enabling the Apply button for PEAP and TTLS (rh #1000564)
- libnm-gtk: only save CA certificate ignored value when connection is saved
- editor: fix display of VLAN parent interface

* Fri Sep 06 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-5.git20130906
- editor: fix missing user/password when re-editing a connection (rh #1000564)
- editor: fix handling of missing CA certificate prompts (rh #758076) (rh #809489)
- editor: fix handling of bonding modes (rh #953076)
- applet/editor: add InfiniBand device support (rh #867273)

* Tue Aug 06 2013 Dennis Gilmore <dennis@ausil.us> - 0.9.9.0-4.git20130515
- rebuild for soname bump in gnome-bluetooth

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.0-3.git20130515
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-2
- Disable migration tool and remove dependencies on GConf and gnome-keyring

* Wed May 15 2013 Dan Williams <dcbw@redhat.com> - 0.9.9.0-1.git20130515
- Update to 0.9.10 snapshot

* Tue Apr 30 2013 Dan Williams <dcbw@redhat.com> - 0.9.8.1-3.git20130430
- editor: fix possible crash canceling connection edit dialog
- applet: only request secrets from the user when allowed to
- applet: fix signal icons with newer libpng
- applet: fix possible crash getting secrets with libsecret

* Thu Apr 18 2013 Jiří Klimeš <jklimes@redhat.com> - 0.9.8.1-2.git20130327
- applet: fix crash while getting a PIN to unlock a modem (rh #950925)

* Wed Mar 27 2013 Dan Williams <dcbw@redhat.com> - 0.9.8.1-1.git20130327
- Update to 0.9.8.2 snapshot
- Updated translations
- editor: don't overwrite bridge/bond master interface name with UUID
- applet: fix WWAN PIN dialog invalid "label1" entry widget
- editor: fix allowed values for VLAN ID and MTU
- editor: preserve existing PPP connection LCP echo failure and reply values
- editor: ensure changes to the STP checkbox are saved
- editor: hide BSSID for AdHoc connection (rh #906133)
- editor: fix random data sneaking into IPv6 route gateway fields
- editor: fix handling of initial entry for MAC address widgets

* Wed Feb 27 2013 Jiří Klimeš <jklimes@redhat.com> - 0.9.8.0-1
- Update to 0.9.8.0

* Fri Feb  8 2013 Dan Williams <dcbw@redhat.com> - 0.9.7.997-1
- Update to 0.9.7.997 (0.9.8-beta2)
- editor: better handling of gateway entry for IPv4
- editor: fix some mnemonics (rh #893466)
- editor: fix saving connection when ignoring CA certificate
- editor: enable Bridge connection editing
- editor: hide widgets not relevant for VPN connections

* Tue Dec 11 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-6.git20121211
- editor: fix populating Firewall zone in 'General' tab

* Tue Dec 11 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-5.git20121211
- Update to git snapshot (git20121211) without bridges

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.7.0-4.git20121016
- Update the versioned obsoletes for the new F17 NM build

* Tue Oct 16 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-3.git20121016
- Update to git snapshot (git20121016)
- editor: fix a crash when no VPN plugins are installed

* Thu Oct  4 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-3.git20121004
- Update to git snapshot

* Wed Sep 12 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-3.git20120820
- move GSettings schema XML to nm-connection-editor rpm (rh #852792)

* Thu Aug 30 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.7.0-2.git20120820
- run glib-compile-schemas in %%post scriplet (rh #852792)

* Tue Aug 21 2012 Dan Winship <danw@redhat.com> - 0.9.7.0-1.git20120820
- Update to 0.9.7.0 snapshot

* Tue Aug 14 2012 Daniel Drake <dsd@laptop.org> - 0.9.5.96-2
- Rebuild for libgnome-bluetooth.so.11

* Mon Jul 23 2012 Dan Williams <dcbw@redhat.com> - 0.9.5.96-1
- Update to 0.9.6-rc2
- lib: recognize PKCS#12 files exported from Firefox
- lib: fix some wireless dialog crashes

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.95-3.git20120713
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Kalev Lember <kalevlember@gmail.com> - 0.9.5.95-2.git20120713
- Fix the versioned obsoletes

* Fri Jul 13 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.5.95-1.git20120713
- update to 0.9.5.95 (0.9.6-rc1)  snapshot
- editor: fixed UI mnemonics
- editor: fix defaults for PPP echo values
- applet: various crash and stability fixes
- applet: show IPv6 addressing page for VPN plugins that support it
- applet: port to GSettings and split out 0.8 -> 0.9 migration code into standalone tool

* Mon May 21 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-4
- update to git snapshot

* Wed May  2 2012 Jiří Klimeš <jklimes@redhat.com> - 0.9.4-3
- update to git snapshot

* Mon Mar 19 2012 Dan Williams <dcbw@redhat.com> - 0.9.3.997-1
- Initial package split from NetworkManager

