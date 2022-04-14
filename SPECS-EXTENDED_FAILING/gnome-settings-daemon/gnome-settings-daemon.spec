Vendor:         Microsoft Corporation
Distribution:   Mariner
%global glib2_version 2.56
%global colord_version 1.3.5
%global geocode_glib_version 3.10.0
%global gnome_desktop_version 3.34.2
%global gsettings_desktop_schemas_version 3.35.91
%global gtk3_version 3.15.3
%global libgweather_version 3.9.5
%global geoclue_version 2.3.1

Name:           gnome-settings-daemon
Version:        3.36.1
Release:        2%{?dist}
Summary:        The daemon sharing settings from GNOME to GTK+/KDE applications

License:        GPLv2+
URL:            https://download.gnome.org/sources/%{name}
Source0:        https://download.gnome.org/sources/%{name}/3.36/%{name}-%{version}.tar.xz
Source1:        org.gnome.settings-daemon.plugins.power.gschema.override

BuildRequires:  meson >= 0.44.0
BuildRequires:  gcc
BuildRequires:  cups-devel
BuildRequires:  gettext
BuildRequires:  perl-interpreter
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(colord) >= %{colord_version}
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gcr-base-3)
BuildRequires:  pkgconfig(geoclue-2.0) >= %{geoclue_version}
BuildRequires:  pkgconfig(geocode-glib-1.0) >= %{geocode_glib_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-desktop-3.0) >= %{gnome_desktop_version}
BuildRequires:  pkgconfig(gsettings-desktop-schemas) >= %{gsettings_desktop_schemas_version}
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(gweather-3.0) >= %{libgweather_version}
BuildRequires:  pkgconfig(lcms2) >= 2.2
BuildRequires:  pkgconfig(libcanberra-gtk3)
BuildRequires:  pkgconfig(libgeoclue-2.0)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-mainloop-glib)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(mm-glib)
BuildRequires:  pkgconfig(nss)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(wayland-client)
%ifnarch s390 s390x
BuildRequires:  pkgconfig(libwacom) >= 0.7
BuildRequires:  pkgconfig(xorg-wacom)
%endif

Requires: colord >= %{colord_version}
Requires: iio-sensor-proxy
Requires: geoclue2 >= %{geoclue_version}
Requires: geocode-glib%{?_isa} >= %{geocode_glib_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gnome-desktop3%{?_isa} >= %{gnome_desktop_version}
Requires: gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: libgweather%{?_isa} >= %{libgweather_version}

Obsoletes: %{name}-updates < 3.13.1
Obsoletes: drwright < 3.5.0-3
Obsoletes: gnome-settings-daemon-devel < 3.23.1

# Earlier gnome-session required "org.gnome.SettingsDaemon.Clipboard" that was
# dropped in 3.33.90 (and functionality moved over to mutter).
Conflicts: gnome-session < 3.33.90

%description
A daemon to share settings from GNOME to other applications. It also
handles global keybindings, as well as a number of desktop-wide settings.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

cp %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/glib-2.0/schemas

%find_lang %{name} --with-gnome

mkdir $RPM_BUILD_ROOT%{_libdir}/gnome-settings-daemon-3.0/gtk-modules

%files -f %{name}.lang
%license COPYING
%doc AUTHORS NEWS

# list daemons explicitly, so we notice if one goes missing
# some of these don't have a separate gschema
%{_libexecdir}/gsd-datetime
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Datetime.desktop

%{_libexecdir}/gsd-dummy

%{_libexecdir}/gsd-housekeeping
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Housekeeping.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.housekeeping.gschema.xml

%{_libexecdir}/gsd-keyboard
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Keyboard.desktop

%{_libexecdir}/gsd-media-keys
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.MediaKeys.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.media-keys.gschema.xml

%{_libexecdir}/gsd-backlight-helper
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.power.policy
%{_libexecdir}/gsd-power
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Power.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.power.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.power.gschema.override

%{_libexecdir}/gsd-print-notifications
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.PrintNotifications.desktop
%{_libexecdir}/gsd-printer

%{_libexecdir}/gsd-rfkill
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Rfkill.desktop

%{_libexecdir}/gsd-screensaver-proxy
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.ScreensaverProxy.desktop

%{_libexecdir}/gsd-smartcard
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Smartcard.desktop

%{_libexecdir}/gsd-sound
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Sound.desktop

%{_libexecdir}/gsd-usb-protection
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.UsbProtection.desktop

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.wacom.gschema.xml
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Wacom.desktop

%ifnarch s390 s390x
%{_libexecdir}/gsd-wacom
%{_libexecdir}/gsd-wacom-led-helper
%{_libexecdir}/gsd-wacom-oled-helper
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.wacom.policy
%endif

%{_libexecdir}/gsd-xsettings
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.XSettings.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xsettings.gschema.xml

%{_libexecdir}/gsd-a11y-settings
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.A11ySettings.desktop

%{_libexecdir}/gsd-color
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Color.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.color.gschema.xml

%{_libexecdir}/gsd-sharing
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Sharing.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.sharing.gschema.xml

%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Wwan.desktop
%{_libexecdir}/gsd-wwan
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.wwan.gschema.xml

%{_libdir}/gnome-settings-daemon-3.0/libgsd.so

%{_sysconfdir}/xdg/Xwayland-session.d/00-xrdb
%{_userunitdir}/*
/usr/lib/udev/rules.d/*.rules
%{_datadir}/gnome-settings-daemon/
%{_datadir}/GConf/gsettings/gnome-settings-daemon.convert

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.gschema.xml

%files devel
%{_includedir}/gnome-settings-daemon-3.0
%{_libdir}/pkgconfig/gnome-settings-daemon.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.36.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Apr 30 2020 Kalev Lember <klember@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Mon Mar 09 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Tue Feb 18 2020 Kalev Lember <klember@redhat.com> - 3.35.91-1
- Update to 3.35.91

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Kalev Lember <klember@redhat.com> - 3.35.0-2
- Rebuilt for libgnome-desktop soname bump

* Tue Jan 07 2020 Kalev Lember <klember@redhat.com> - 3.35.0-1
- Update to 3.35.0

* Mon Oct 14 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Fri Sep 06 2019 Kalev Lember <klember@redhat.com> - 3.33.92-1
- Update to 3.33.92

* Mon Aug 26 2019 Kalev Lember <klember@redhat.com> - 3.33.90-1
- Update to 3.33.90
- Drop old versioned conflicts

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Kalev Lember <klember@redhat.com> - 3.33.0-3
- Rebuilt for libgnome-desktop soname bump

* Mon Jul 08 2019 Kalev Lember <klember@redhat.com> - 3.33.0-2
- Rebuilt for libgweather soname bump

* Tue Jun 25 2019 Kalev Lember <klember@redhat.com> - 3.33.0-1
- Update to 3.33.0

* Wed Jun 19 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Tue May 28 2019 Marek Kasik <mkasik@redhat.com> - 3.32.0-2
- Fix NSS crash at smartcard plugin (#1688791)

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Wed Mar 06 2019 Kalev Lember <klember@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Wed Feb 20 2019 Kalev Lember <klember@redhat.com> - 3.31.91-1
- Update to 3.31.91

* Wed Feb 06 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Kalev Lember <klember@redhat.com> - 3.31.2-1
- Update to 3.31.2

* Tue Nov 20 2018 Pete Walter <pwalter@fedoraproject.org> - 3.30.1.2-3
- Move gnome-remote-desktop recommends to gnome-control-center

* Fri Nov 09 2018 Ray Strode <rstrode@redhat.com> - 3.30.1.2-2
- Add recommends for gnome-remote-desktop after irc discussion

* Thu Oct 04 2018 Kalev Lember <klember@redhat.com> - 3.30.1.2-1
- Update to 3.30.1.2

* Fri Sep 28 2018 Kalev Lember <klember@redhat.com> - 3.30.1.1-1
- Update to 3.30.1.1

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Sun Aug 12 2018 Kalev Lember <klember@redhat.com> - 3.29.90.1-1
- Update to 3.29.90.1

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 3.28.1-3
- Rebuild with fixed binutils

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 12 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Tue Apr 10 2018 Michael Catanzaro <mcatanzaro@gnome.org> - 3.28.0-2
- Disable automatic suspend, except when on battery power

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Fri Mar 02 2018 Kalev Lember <klember@redhat.com> - 3.27.91-1
- Update to 3.27.91

* Sat Feb 10 2018 Bastien Nocera <bnocera@redhat.com> - 3.27.90-4
+ gnome-settings-daemon-3.27.90-4
- Rebuild against newer gnome-desktop3 package

* Fri Feb 09 2018 Bastien Nocera <bnocera@redhat.com> - 3.27.90-3
+ gnome-settings-daemon-3.27.90-3
- Really fix gsd-* helper linkage
- Build fix for highly parallel builds

* Wed Feb 07 2018 Kalev Lember <klember@redhat.com> - 3.27.90-2
- Fix missing libcommon.so library

* Tue Feb 06 2018 Kalev Lember <klember@redhat.com> - 3.27.90-1
- Update to 3.27.90
- Switch to meson build system

* Mon Feb 05 2018 Kalev Lember <klember@redhat.com> - 3.26.2-5
- Rebuilt for libgweather soname bump

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3.26.2-4
- Rebuilt for switch to libxcrypt

* Fri Jan 12 2018 Bastien Nocera <bnocera@redhat.com> - 3.26.2-3
- Fix gdm session trying to change the backlight, resulting in a lot
  of spurious error messages (#1322588)

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.2-2
- Remove obsolete scriptlets

* Thu Nov 02 2017 Kalev Lember <klember@redhat.com> - 3.26.2-1
- Update to 3.26.2

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Tue Sep 05 2017 Kalev Lember <klember@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Thu Aug 24 2017 Kalev Lember <klember@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 3.25.4-2
- Add explicit conflicts to not break older gdm, gnome-session and gnome-shell

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Kalev Lember <klember@redhat.com> - 3.25.2-1
- Update to 3.25.2

* Wed May 10 2017 Kalev Lember <klember@redhat.com> - 3.24.2-1
- Update to 3.24.2

* Wed Apr 12 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Wed Feb 15 2017 Richard Hughes <rhughes@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Bastien Nocera <bnocera@redhat.com> - 3.23.3-1
+ gnome-settings-daemon-3.23.3-1
- Update to 3.23.3

* Tue Oct 11 2016 Bastien Nocera <bnocera@redhat.com> - 3.23.2-1
+ gnome-settings-daemon-3.23.2-1
- Update to 3.23.2

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92.1-1
- Update to 3.21.92.1

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92
- Don't set group tags

* Fri Aug 26 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Sun Apr 17 2016 Bastien Nocera <bnocera@redhat.com> - 3.20.1-3
- Fix crasher in newly enabled audio device selection dialogue

* Sun Apr 17 2016 Bastien Nocera <bnocera@redhat.com> - 3.20.1-2
- Require alsa to enable the audio device selection dialogue

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Thu Mar 17 2016 Kalev Lember <klember@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Fri Mar 04 2016 Kalev Lember <klember@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Wed Feb 17 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 3.19.5-1
- Update to 3.19.5

* Thu Dec 17 2015 Kalev Lember <klember@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Tue Dec 15 2015 Kalev Lember <klember@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Tue Nov 10 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Mon Sep 14 2015 Kalev Lember <klember@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.17.3-1
- Update to 3.17.3
- Use pkgconfig for BuildRequires

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Richard Hughes <rhughes@redhat.com> - 3.17.2-2
- Add runtime dep on iio-sensor-proxy for the ambient light sensor

* Fri Jun 05 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.2-1
- Update to 3.17.2

* Tue May 12 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92

* Tue Mar 03 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91
- Use the %%license macro for the COPYING file

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Thu Jan 22 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Thu Nov 27 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.1-1
- Update to 3.15.1

* Tue Nov 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Sat Nov 01 2014 Richard Hughes <rhughes@redhat.com> - 3.14.1-3
- Fix compile on RHEL

* Sun Oct 26 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-2
- Obsolete drwright

* Tue Oct 14 2014 Rui Matos <rmatos@redhat.com> - 3.14.1-1
- Update to 3.14.1

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Mon Aug 18 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Thu Jun 26 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Wed Jun 25 2014 Richard Hughes <rhughes@redhat.com> - 3.13.2-1
- Update to 3.13.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-1
- Update to 3.13.1
- Remove and obsolete the updates plugin

* Wed Apr 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1
- Tighten subpackage deps

* Mon Apr 14 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0.1-3
- Drop control-center-filesystem dependency

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0.1-2
- Update dep versions

* Wed Mar 26 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0.1-1
- Update to 3.12.0.1

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-2
- Rebuilt for gnome-desktop soname bump

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Thu Jan 30 2014 Richard Hughes <rhughes@redhat.com> - 3.11.3-2
- Rebuild for libpackagekit-glib soname bump

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 25 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Thu Oct 31 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Fri Oct 11 2013 Richard Hughes <rhughes@redhat.com> - 3.10.0-3
- Apply the previous patch on Fedora too.

* Fri Oct 11 2013 Richard Hughes <rhughes@redhat.com> - 3.10.0-2
- Grab a patch from upstream to fix the multiple notifications about updates.
- Resolves: https://bugzilla.redhat.com/show_bug.cgi?id=1009132

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 17 2013 Richard Hughes <rhughes@redhat.com> - 3.9.91.1-2
- Grab a patch from upstream so that the offline updates feature can
  actually work when reboot returns with success.

* Tue Sep 03 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.91.1-1
- Update to 3.9.91.1

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91
- Include the new datetime plugin

* Fri Aug 23 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-2
- Keep middle click paste enabled for now

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-1
- Update to 3.9.5
- Remove empty /etc/gnome-settings-daemon directory
- Install new rfkill plugin and add back the smartcard plugin

* Tue Jul 30 2013 Richard Hughes <rhughes@redhat.com> - 3.9.3-3
- Rebuild for colord soname bump

* Mon Jul 22 2013 Bastien Nocera <bnocera@redhat.com> 3.9.3-2
- Remove obsolete GStreamer 0.10 BRs

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.3-1
- Update to 3.9.3

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.2-1
- Update to 3.9.2
- Drop the ibus-kkc-libpinyin patch; the hardcoded input sources
  list is gone from g-s-d
- Set the minimum required gnome-desktop3 version

* Tue May 14 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Thu May  9 2013 Jens Petersen <petersen@redhat.com> - 3.8.1-2
- default ibus engine in Fedora is now kkc for Japanese
  and libpinyin for Chinese (#948117)

* Tue Apr 16 2013 Richard Hughes <rhughes@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Tue Mar  5 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Thu Feb 07 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5.1-1
- Update to 3.7.5.1

* Wed Feb 06 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.7.5-2
- Bump the gtk3 BuildRequires

* Tue Feb 05 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Mon Dec 31 2012 Dan Horák <dan[at]danny.cz> - 3.7.3-2
- fix filelist for s390(x) (and ppc/ppc64 in RHEL)

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3
- Adjust the spec file for the (temporarly) disabled smartcard plugin

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.1-1
- Update to 3.7.1
- Remove upstreamed patches

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.3-1
- Update to 3.6.3
- Drop the static man page patch and BR docbook-style-xsl instead

* Thu Nov 08 2012 Bastien Nocera <bnocera@redhat.com> 3.6.2-1
- Update to 3.6.2

* Thu Oct 18 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.1-3
- Fix a typo in the suspend patch (#858259)

* Mon Oct 08 2012 Dan Horák <dan[at]danny.cz> - 3.6.1-2
- fix build on s390(x)

* Mon Oct 08 2012 Bastien Nocera <bnocera@redhat.com> 3.6.1-1
- Update to 3.6.1

* Fri Oct  5 2012 Olivier Fourdan <mclasen@redhat.com> - 3.6.0-5
- Adds Wacom OSD window from upstream bug #679062

* Wed Oct  3 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-4
- Fix an inhibitor leak in the previous patch

* Tue Oct  2 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-3
- Fix lid close handling with new systemd

* Fri Sep 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.0-2
- Split out PackageKit into a sub package. Fixes #699348

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 3.5.92-1
- Update to 3.5.92

* Wed Sep 05 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.91-1
- Update to 3.5.91

* Wed Aug 22 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.6-1
- Update to 3.5.6

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 24 2012 Dan Horák <dan[at]danny.cz> - 3.5.5-3
- fix build without wacom

* Thu Jul 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.5-2
- Fix the updates plugin to load

* Thu Jul 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Tue Jul 17 2012 Dan Horák <dan[at]danny.cz> - 3.5.4-3
- fix build on s390(x) - cherry-picked from f17 branch
- allow build without wacom on ppc/ppc64

* Tue Jul 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.4-2
- Rebuild against new PackageKit

* Wed Jun 27 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Thu Jun 14 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.2-4
- Drop calculator patch, no longer needed

* Thu Jun 07 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.2-3
- Fix file lists

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-2
- Add missing BR

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 3.4.2-1
- Update to 3.4.2

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- New upstream version.

* Tue Mar 20 2012 Richard Hughes <rhughes@redhat.com> 3.3.92-1
- Update to 3.3.92

* Mon Mar 05 2012 Bastien Nocera <bnocera@redhat.com> 3.3.91-1
- Update to 3.3.91

* Wed Feb 22 2012 Bastien Nocera <bnocera@redhat.com> 3.3.90.1-1
- Update to 3.3.90.1

* Thu Feb  9 2012 Matthias Clasen <mclasen@redhat.com> 3.3.5-2
- Use systemd for session tracking

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> 3.3.5-1
- Update to 3.3.5

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> 3.3.4-2
- Some crash fixes

* Tue Jan 17 2012 Bastien Nocera <bnocera@redhat.com> 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3.1-2
- Fix a path problem in the gnome-settings-daemon autostart file

* Fri Dec 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3.1-1
- Update to 3.3.3.1

* Wed Dec 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Fri Nov 11 2011 Bastien Nocera <bnocera@redhat.com> 3.2.2-1
- Update to 3.2.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-4
- Rebuilt for glibc bug#747377

* Tue Oct 25 2011 Marek Kasik <mkasik@redhat.com> - 3.2.1-3
- Fix a typo in registration of an object on DBus (#747318)

* Mon Oct 24 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-2
- Fix calculator keybinding (#745367)

* Mon Oct 17 2011 Bastien Nocera <bnocera@redhat.com> 3.2.1-1
- Update to 3.2.1

* Wed Oct 12 2011 Adam Williamson <awilliam@redhat.com> - 3.2.0-2
- backport some greatest hits from git to stop the same bugs being
  reported over and over (all will be in 3.2.1)

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep  6 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.91-1
- Update to 3.1.91

* Tue Jul 26 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.1.4-2
- Add a patch to make the fallback mounter to build correctly
- Include the new power plugin

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Fri Jul 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.3-2
- Add support for chrony (#723212)

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Tue Jun 21 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-2
- Fix fortify fail in gsd-color-manager.c (#714625)

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Wed Jun 15 2011 Bastien Nocera <bnocera@redhat.com> 3.1.1-3
- Rebuild for new gnome-desktop3 libs

* Mon Jun 13 2011 Marek Kasik <mkasik@redhat.com> 3.1.1-2
- Remove requirement of system-config-printer-udev (#704381)

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-5
- Update gsettings schema scriptlet

* Mon May  2 2011 Matthias Clasen <mclasen@redhat.com> 3.0.1-4
- Try to fix a crash (#698533)

* Thu Apr 28 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-2
- Fix setting ntpd usage with SystemD

* Tue Apr 26 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-1
- Update to 3.0.1

* Wed Apr 06 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0.1-1
- Update to 3.0.0.1

* Mon Apr 04 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0-1
- Update to 3.0.0

* Wed Mar 30 2011 Marek Kasik <mkasik@redhat.com> 2.91.93-2
- Make CUPS' subscriptions expirable

* Fri Mar 25 2011 Bastien Nocera <bnocera@redhat.com> 2.91.93-1
- Update to 2.91.93

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> 2.91.92-1
- Update 2.91.92

* Wed Mar 16 2011 Richard Hughes <rhughes@redhat.com> 2.91.91-3
- Add a patch from upstream to fix the updates plugin.

* Fri Mar 11 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-2
- Add libXxf86misc-devel requires so that key repeat/delay works

* Tue Mar 08 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-1
- Update to 2.91.91

* Fri Feb 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-4
- Fix undefined symbols in the updates plugin

* Wed Feb 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-3
- BR PackageKit and cups
- Explicitly list plugins so we notice if they go missing

* Wed Feb 23 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.90-2
- Include an upstream patch to fix a possible crasher

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 2.91.90-1
- Update to 2.91.90

* Wed Feb 16 2011 Bastien Nocera <bnocera@redhat.com> 2.91.9-6
- Fix crasher when media keys GSettings value changes

* Sun Feb 13 2011 Christopher Aillon <caillon@redhat.com> - 2.91.9-5
- Rebuild for new libxklavier

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.9-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Bastien Nocera <bnocera@redhat.com> 2.91.9-2
- Fix setting timezones in the date & time panel (#674999)

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.9-1
- 2.91.9

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.8-1
- 2.91.8

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> 2.91.7-2
- Own %%{_libdir}/gnome-settings-daemon-3.0/gtk-modules

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.7-1
- Update to 2.91.7

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.6.2-1
- Update to 2.91.6.2

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.5.1-1
- Update to 2.91.5.1

* Thu Dec  2 2010 Dan Williams <dcbw@redhat.com> - 2.91.5-4
- Re-add patch handling org.gnome.media-handling gsettings schema rename

* Wed Dec  1 2010 Dan Williams <dcbw@redhat.com> - 2.91.5-3
- Fix various cases of forgetting to draw the background

* Tue Nov 30 2010 Owen Taylor <otaylor@redhat.com> - 2.91.5-2
- Add a patch handling org.gnome.media-handling gsettings schema rename

* Tue Nov 30 2010 Tomas Bzatek <tbzatek@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Nov 26 2010 Bastien Nocera <bnocera@redhat.com> 2.91.4-2
- Fix crasher on startup

* Thu Nov 25 2010 Bastien Nocera <bnocera@redhat.com> 2.91.4-1
- Update to 2.91.4

* Wed Nov 17 2010 Richard Hughes <richard@hughsie.com> 2.91.3-1
- Update to 2.91.3

* Wed Nov 10 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2.1-0.4.
- Update to 2.91.2.1

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-0.4.20101102
- Rebuild against new libnotify

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-0.3.20101102
- Make theme changing work

* Tue Nov 02 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.2.20101102
- Add BR gsettings-desktop-schemas-devel

* Tue Nov 02 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.1.20101102
- Update to a git snapshot to fix rawhide.

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.91.0-3
- Fix the pkgconfig file manually

* Wed Oct 06 2010 Richard Hughes <rhughes@redhat.com> 2.91.0-2
- Rebuild against the new libgnomekbd library

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.1-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Bastien Nocera <bnocera@redhat.com> 2.90.1-1
- Update to 2.90.1

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> 2.31.91-1
- Update to 2.31.91

* Fri Aug 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.6-2
- Fix a problem with warning bubbles in virtual machines (#624624)

* Tue Aug  3 2010 Matthias Clasen <mclasen@redhat.com> 2.31.6-1
- Update to 2.31.6

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5.1-1
- Update to 2.31.5.1

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5-1
- Update to 2.31.5

* Wed Jun 30 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4.2-1
- Update to 2.31.4.2

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4.1-1
- Update to 2.31.4.1

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-1
- Update to 2.31.4

* Mon Jun 28 2010 Bastien Nocera <bnocera@redhat.com> 2.31.3-3
- Don't remove the sound plugin if we want the caches to be
  updated

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-1
- Update to 2.31.3

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-1
- Update to 2.31.2

* Sun May 16 2010 Matthias Clasen <mclasen@redhat.com> 2.31.1-1
- Update to 2.31.1

* Fri Apr 30 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-4
- Waah, one more mistake in these macros

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-3
- Nobody understands macro processors...

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-2
- Fix a typo

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1
- Spec file cleanups

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Mon Mar 22 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-3
- Disable the font plugin by default

* Wed Mar 10 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-2
- Remove unneeded icons, already upstream

* Tue Mar 09 2010 Bastien Nocera <bnocera@redhat.com> 2.29.92-1
- Update to 2.29.92

* Sat Feb 27 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91.1-2
- Fix Fn-F8 OSD icon
- Modernize scriptlets

* Wed Feb 24 2010 Matthias Clasen <mclasen@redhat.com> 2.29.91.1-1
- Update to 2.29.91.1

* Wed Feb 17 2010 Matthias Clasen <mclasen@redhat.com> 2.29.90-2
- Set a name for the keyboard statusicon

* Wed Feb 10 2010 Tomas Bzatek <tbzatek@redhat.com> 2.29.90-1
- Update to 2.29.90

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> 2.29.6-1
- Update to 2.29.6

* Fri Dec 18 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-10
- Avoid warning messages from the OSD code

* Tue Dec 15 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-9
- Survive when running without XKB (#547780)

* Thu Nov 12 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-8
- Avoid a 'whitespace leak' around the display statusicon (gnome #601696)

* Mon Nov  9 2009 Matthias Clasen <mclasen@redhat.com> 2.28.1-7
- React to screen changes when showing the background (gnome #601203)

* Thu Nov 05 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-6
- Fix the volume going over 100% in the OSD

* Wed Oct 28 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-5
- Update OSD code again

* Tue Oct 27 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-4
- Fix bluriness in OSD

* Mon Oct 26 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-3
- Change default font rendering to use slight hinting

* Mon Oct 26 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.28.1-2
- left-handed-touchpad.patch: change physical touchpad buttons to
  left-handed, not tapping though (#498249)

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Thu Oct  1 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-4
- Fix keyboard variant handling

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-3
- Align the OSD visuals with the notification theme

* Tue Sep 22 2009 Adam Jackson <ajax@redhat.com> 2.28.0-2
- BuildRequires: libcanberra-devel

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Wed Sep 09 2009 Bastien Nocera <bnocera@redhat.com> 2.27.92-2
- Update left-hand touchpad patch

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Sun Aug 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-3
- Make 'Locate Pointer' work with metacity again

* Wed Aug 26 2009 Peter Hutterer <peter.hutterer@redhat.com> 2.27.91-2
- buttonmapping.patch: Don't check for IsXExtensionDevice, only skip button
  mappings for core devices instead (#502129).

* Mon Aug 24 2009 Bastien Nocera <bnocera@redhat.com> 2.27.91-1
- Update to 2.27.91

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 2.27.90-2
- Update gnome-volume-control code

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 2.27.90-1
- Update to 2.27.90

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-3
- Make locate-pointer not interfere with media keys

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-2
- Rebuild against new libgnomekbd

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> 2.27.4-1
- Update ot 2.27.4

* Tue Jun 30 2009 Matthias Clasen <mclasen@redhat.com> 2.27.3-2
- Rebuild against new libxklavier

* Tue Jun 16 2009 Matthias Clasen <mclasen@redhat.com> 2.27.3-1
- Update to 2.27.3

* Mon Jun  8 2009 Matthias Clasen <mclasen@redhat.com> 2.27.1-2
- Make the 'locate pointer' effect cope with changing compositing
  managers

* Sat May 16 2009 Matthias Clasen <mclasen@redhat.com> 2.27.1-1
- Update to 2.27.1

* Fri May 08 2009 Bastien Nocera <bnocera@redhat.com> 2.26.1-4
- Remove useless patch, see:
http://bugzilla.gnome.org/show_bug.cgi?id=580761 for details

* Wed Apr 29 2009 Bastien Nocera <bnocera@redhat.com> 2.26.1-3
- Don't set touchpads to be left-handed, otherwise the tap
  behaves like the 2nd mouse button (#483639)

* Mon Apr 27 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-2
- Don't drop schemas translations from po files

* Tue Apr 14 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Wed Apr  8 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-2
- Support touchpads

* Mon Mar 16 2009 Matthias Clasen  <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Mon Mar  2 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb  5 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.90-2
- Fix a warning (#484132)

* Wed Feb  4 2009 Matthias Clasen  <mclasen@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Mon Jan 19 2009 - Ray Strode <rstrode@redhat.com> - 2.25.3-4
- Update fade patch for new gnome-desktop release

* Thu Dec 18 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-3
- Rebuild

* Thu Dec 18 2008 - Ray Strode <rstrode@redhat.com> - 2.25.3-2
- Drop touchpad patch for now

* Thu Dec 18 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Thu Dec 18 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.2-11
- Fix touchpad patches

* Wed Dec 17 2008 Matthias Clasen  <mclasen@redhat.com> - 2.25.2-10
- Rebuild against new gnome-desktop

* Wed Dec 10 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-9
- Don't call SetPointerMapping when using Xinput since
  it duplicates effort but gets touchpads wrong (bug 324721)

* Wed Dec 10 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-8
- Shutdown cleanly when bus goes away (bug 445898 again)

* Wed Dec 10 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-7
- Don't map touch pad tap to right-click for left-handed
  users (bug 324721)

* Wed Dec 10 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-6
- Listen for DeviceAdded signals when configuring mouse
  (in addition to DeviceEnabled).  This may help with
  bug 474758.

* Tue Dec  9 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-5
- Shutdown cleanly on TERM signal (bug 445898)

* Sun Dec  7 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.25.2-4
- Add gnome-settings-daemon-2.24.1-umask.patch

* Thu Dec  4 2008 Ray Strode <rstrode@redhat.com> - 2.25.2-2
- Rebase fade patch to apply with Behdad's updates to
  g-s-d

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Ypdate to 2.25.2

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-4
- Rebuild

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-2
- Update to 2.25.1

* Fri Oct 24 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-14
- At fontconfig-devel buildrequires (bug 468304)

* Wed Oct 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-13
- Save some space

* Tue Oct 14 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-12
- Hold off on settings-daemon fade if nautilus is going to do
  it anyway.

* Tue Oct 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-11
- Show the shutdown dialog when the power button is pressed

* Tue Oct 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-9
- Drop a patch that is no longer needed with the evdev ruleset
  in xkeyboard-config

* Sun Oct 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-7
- Try harder not to override peoples configured keyboard layouts

* Sun Oct 12 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-6
- Update fade patch to skip crossfade when changing frames in
  slideshow background.

* Fri Oct 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-5
- Fix the picking up of the gdm keyboard layout even more

* Tue Sep 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-3
- Fix the picking up of the gdm keyboard layout

* Sun Sep 28 2008 Ray Strode <rstrode@redhat.com> - 2.24.0-2
- Don't draw background twice at startup

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Thu Sep 18 2008 Ray Strode <rstrode@redhat.com> - 2.23.92-3
- When switching desktop backgrounds fade between them

* Thu Sep 11 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.92-2
- Fix various bugs in the fn-F7 support

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Fri Sep  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-5
- Try harder to use the keyboard layout that gdm tells us

* Thu Sep 04 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-4
- Use the fn-F7 key, not the F7 key.

* Wed Sep 03 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-3
- Bump gnome-desktop requirement

* Wed Sep 03 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.91-2
- Add patch to do fn-f7 cycling

* Mon Sep 01 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Thu Aug 28 2008 Jon McCann <jmccann@redhat.com> - 2.23.91-0.2008.08.28.2
- BuildRequires libnotify-devel

* Thu Aug 28 2008 Jon McCann <jmccann@redhat.com> - 2.23.91-0.2008.08.28.1
- Update to snapshot

* Fri Aug 22 2008 Matthias Clasen <mclasne@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Thu Aug 14 2008 Lennart Poettering <lpoetter@redhat.com> - 2.23.6-3
- Rerun autotools after patching configure.ac

* Thu Aug 14 2008 Lennart Poettering <lpoetter@redhat.com> - 2.23.6-2
- Apply patch from gnome bug 545386. This hasn't been accepted in this form yet
  by upstream, will however very likely be merged in a similar form.
- Disable esd/sounds module since we don't need it to start PA anymore

* Tue Aug  5 2008 Matthias Clasen <mclasne@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Fri Jul 25 2008 Matthias Clasen <mclasne@redhat.com> - 2.23.5-3
- Use standard icon names in the volume OSD
 
* Fri Jul 25 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.5-2
- Fix build, call gtk-update-icon-cache as required

* Thu Jul 24 2008 Soren Sandmann <sandmann@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Wed Jun 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Tue Jun 17 2008 Colin Walters <walters@redhat.com> - 2.23.3-2
- Add (now upstreamed) patch to legacy ESD preference; see
  http://bugzilla.gnome.org/show_bug.cgi?id=533198
  https://bugzilla.redhat.com/show_bug.cgi?id=430624

* Wed Jun  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Wed May 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-0.2008.05.14.2
- Fix BuildRequires

* Wed May 14 2008 Jon McCann <jmccann@redhat.com> - 2.23.2-0.2008.05.14.1
- Build snapshot

* Tue May 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1-5
- Rebuild

* Mon May  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1-4
- Pick up the keyboard layout from the login screen

* Mon May  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1-1-3
- Fix background drawing without nautilus

* Tue Apr 29 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.1.1-2
- Add patch from upstream to avoid the Stop button triggering an Eject (#346201)

* Fri Apr 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.1.1-1
- Update to 2.23.1.1

* Tue Apr 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-2008.03.26.6
- Make the xrandr plugin survive the absence of Xrandr

* Sat Apr 5 2008 - Soren Sandmann <sandmann@redhat.com> - 2.22.1-2008.03.26.5
- Update randr plugin

* Mon Mar 31 2008 - Ray Strode <rstrode@redhat.com> - 2.22.1-0.2008.03.26.4
- Over the releases we've accumulated default.png, default-wide.png default-5_4.png
  and default.jpg.  We haven't been able to drop them because it would leave some
  users with white backgrounds on upgrade.  This patch just falls back to the
  default image if the user's background doesn't exist.

* Wed Mar 26 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.1-0.2008.03.26.3
- Add patch for the mouse plugin not to eat multimedia key events (#438942)

* Wed Mar 26 2008 Jon McCann <jmccann@redhat.com> - 2.22.1-0.2008.03.26.2
- Rebuild

* Wed Mar 26 2008 Jon McCann <jmccann@redhat.com> - 2.22.1-0.2008.03.26.1
- Update to snapshot
- Enable profiling

* Wed Mar 26 2008 - Bastien Nocera <bnocera@redhat.com> - 2.22.0-3
- apps_gnome_settings_daemon_default_editor.schemas is obsolete (#438937)

* Thu Mar 20 2008 Matthias Clasen <mclasen@redhat.com> 2.22.0-2
- Fix interaction between "Locate Pointer" and volume keys

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Sun Mar  9 2008 Ray Strode <rstrode@redhat.com> - 2.21.92-3
- Don't set keyboard model on startup from gconf if evdev is being used.
  Evdev needs to use its own keyboard model to work right.

* Sun Mar  2 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.92-2
- Update randr patch to handle video key

* Fri Feb 29 2008 Jon McCann <jmccann@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 12 2008 Soren Sandmann <sandmann@redhat.com> - 2.21.91-3
- Add patch to make the xrandr plugin listen for client messages from
  the control panel and reread the configuration file.

* Mon Feb 11 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-2
- Remove obsolete control-center translations

* Mon Feb 11 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.91-1
- Update to 2.21.91
- Remove obsolete patches

* Thu Feb  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90.1-3
- Load xkb settings initially

* Thu Jan 31 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90.1-2
- Fix the path for g-s-d, from upstream patch

* Tue Jan 29 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90.1-1
- Update to 2.21.90.1

* Tue Jan 29 2008 - Bastien Nocera <bnocera@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.5.2-2
- Incorporate review feedback (#428833)

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.5.2-1
- Update to 2.21.5.2

* Tue Jan 15 2008  Matthias Clasen <mclasen@redhat.com> - 2.21.5.1-1
- Update to 2.21.5.1
- Fix up BuildRequires

* Thu Dec 06 2007 - Bastien Nocera <bnocera@redhat.com> - 2.21.5-1
- First package

