Vendor:         Microsoft Corporation
Distribution:   Mariner
%global commit  93cfe7c8d66ed486001c4f3f55399b7a
Summary:        Power Management Service
Name:           upower
Version:        0.99.11
Release:        5%{?dist}
License:        GPLv2+
URL:            http://upower.freedesktop.org/
Source0:        https://gitlab.freedesktop.org/upower/upower/uploads/%{commit}/%{name}-%{version}.tar.xz

BuildRequires:  %{_bindir}/xsltproc
BuildRequires:  sqlite-devel
BuildRequires:  libtool
BuildRequires:  gettext
BuildRequires:  libgudev1-devel
%ifnarch s390 s390x
BuildRequires:  libusbx-devel
BuildRequires:  libimobiledevice-devel
%endif
BuildRequires:  glib2-devel >= 2.6.0
BuildRequires:  gobject-introspection-devel
BuildRequires:  systemd
Requires:       udev
Requires:       gobject-introspection


%description
UPower (formerly DeviceKit-power) provides a daemon, API and command
line tools for managing power devices attached to the system.

%package devel
Summary: Headers and libraries for UPower
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Headers and libraries for UPower.

%prep
%autosetup -p1

# Disable docs generation.
sed -i -E 's/^(SUBDIRS.*) doc(.*)/\1\2/g' Makefile.in

%build
%configure \
        --disable-gtk-doc \
        --disable-static \
        --enable-introspection \
        --with-udevrulesdir=%{_udevrulesdir} \
        --with-systemdsystemunitdir=%{_unitdir} \
%ifarch s390 s390x
	--with-backend=dummy
%endif

# Disable SMP build, fails to build docs
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%find_lang upower

%ldconfig_scriptlets

%post
%systemd_post upower.service

%preun
%systemd_preun upower.service

%postun
%systemd_postun_with_restart upower.service

%files -f upower.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS AUTHORS HACKING README
%{_libdir}/libupower-glib.so.*
%{_datadir}/dbus-1/system.d/*.conf
%ifnarch s390 s390x
%{_udevrulesdir}/*.rules
%endif
%ghost %dir %{_localstatedir}/lib/upower
%dir %{_sysconfdir}/UPower
%config %{_sysconfdir}/UPower/UPower.conf
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/girepository-1.0/*.typelib
%{_datadir}/dbus-1/system-services/*.service
%{_unitdir}/*.service

%files devel
%{_datadir}/dbus-1/interfaces/*.xml
%{_libdir}/libupower-glib.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%dir %{_includedir}/libupower-glib
%{_includedir}/libupower-glib/up-*.h
%{_includedir}/libupower-glib/upower.h

%changelog
* Mon Mar 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.99.11-5
- Adding BR on '%%{_bindir}/xsltproc'.
- Disabled gtk doc generation to remove network dependency during build-time.
- License verified.

* Tue Jun 01 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.99.11-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Specify udev rules directory and systemd system unit dir

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep  4 2019 Christian Kellner <ckellner@redhat.com> - 0.99.11-2
- Add systemd service snippets
- Use macros for _unitdir and _udevrulesdir
- Mark _datadir/gtk-doc as directory

* Tue Sep  3 2019 Christian Kellner <ckellner@redhat.com> - 0.99.11-1
- New upstream release 0.99.11
- Intltool has been replaced by gettext
- D-Bus configuration moved from sysconfdir to datadir
- Systemd is creating /var/lib/upower, so 'ghost' the dir

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Christian Kellner <ckellner@redhat.com> - 0.99.10-1
- New upstream release with the following changes:
- Set 'pending-charge' for DisplayDevice if at least one battery is in
  the 'pending-charge' state
- Map pending-charge to fully-charged when charge is 100%

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Christian Kellner <ckellner@redhat.com> - 0.99.9-1
- New upstream release
- Drop unneccessary patch to fix udev events access
- Fix daemon lockdown issues (keyboard backlight, AC status changes)
- Out-of-tree build fixes and documentation fixes

* Sun Oct 07 2018 Kalev Lember <klember@redhat.com> - 0.99.8-3
- Backport an upstream fix for upower not having access to udev events

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Bastien Nocera <bnocera@redhat.com> - 0.99.8-1
+ upower-0.99.8-1
- Update to 0.99.8

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.99.7-2
- Switch to %%ldconfig_scriptlets

* Tue Nov 28 2017 Bastien Nocera <bnocera@redhat.com> - 0.99.7-1
+ upower-0.99.7-1
- Update to 0.99.7
- Add Bluetooth LE battery support
- Fix critical action after resume from hibernate

* Mon Sep 11 2017 Richard Hughes <rhughes@redhat.com> - 0.99.6-1
- New upstream release
- Detect joysticks as gaming input devices
- Fix crash when '@' is present in the device name
- Grab the model name from device if unavailable from battery

* Thu Aug 24 2017 Benjamin Berg <bberg@redhat.com> - 0.99.5-4
- Add patch to not correctly close the inhibitor FD

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Richard Hughes <rhughes@redhat.com> - 0.99.5-1
- New upstream release
- Add BatteryLevel property for devices with a finite number of power levels
- Add support for pausing and resuming of the daemon poll
- Do not spin in a loop when /proc/timer_stats cannot be written
- Fix reading and writing the keyboard brightness level
- Get a serial number for device batteries
- Refresh devices after waking up from sleep
- Lower initial power usage when iDevice isn't accessible

* Tue Feb 14 2017 Dan Horák <dan[at]danny.cz> - 0.99.4-4
- Add explicit BR:systemd to fix s390(x) build

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Mar 14 2016 Bastien Nocera <bnocera@redhat.com> 0.99.4-2
- Fix getting the critical action

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 0.99.4-1
- New upstream release
- Add support for Logitech G700s/G700 Gaming Mouse
- Change the default low battery policy to percentage

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.99.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Richard Hughes <rhughes@redhat.com> - 0.99.3-1
- New upstream release
- Fix several crashes
- Properly detect bluetooth mice and keyboards that are HID devices
- Support Logitech Unifying in Linux 3.19
- Work-around broken battery on the Onda v975w

* Wed Mar 18 2015 Rex Dieter <rdieter@fedoraproject.org> - 0.99.2-4
- pull in upstream crash fix (#1128390)
- use %%autosetup
- -devel: tighten subpkg dep via %%_isa
- -devel-docs: fix Summary

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.99.2-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 11 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.99.2-2
- Rebuild (libimobiledevice)
- Use %%license

* Thu Dec 18 2014 Richard Hughes <rhughes@redhat.com> - 0.99.2-1
- New upstream release
- Fix various memory and reference leaks
- Respect the CriticalPowerAction config option
- Set update-time on the aggregate device
- Update display device when battery is removed

* Sun Nov 16 2014 Kalev Lember <kalevlember@gmail.com> - 0.99.1-3
- Obsolete compat-upower09 from rhughes-f20-gnome-3-12 copr

* Wed Oct 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.99.1-2
- Rebuild for libimobiledevice 1.1.7

* Mon Aug 18 2014 Richard Hughes <rhughes@redhat.com> - 0.99.1-1
- New upstream release
- Create the history directory at runtime
- Do not log a critical warning when using _set_object_path_sync()
- Fix API doc for up_client_get_on_battery()
- Fix possible UpHistoryItem leak on failure
- Fix segfault on getting property when daemon is not running
- Fix shutdown on boot on some machines
- Fix small memleak on startup with Logitech devices
- Free the obtained device list array after use
- Remove IsDocked property
- Remove unused polkit dependency

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.99.0-6
- Rebuilt for gobject-introspection 1.41.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.99.0-4
- Rebuild for libimobiledevice 1.1.6

* Mon Mar 17 2014 Richard Hughes <rhughes@redhat.com> - 0.99.0-3
- Split out a new devel-docs subpackage to fix multilib_policy=all installs.
- Resolves: #1070661

* Fri Nov 08 2013 Bastien Nocera <bnocera@redhat.com> 0.99.0-2
- Fix crash when D-Bus isn't available

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 0.99.0-1
- New upstream release
- This version contains major API changes and bumps library soname.
- Add DisplayDevice composite battery
- Add WarningLevel and IconName properties to all devices
- Clamp percentage for overfull batteries
- Emit PropertiesChanged signals
- Enforce critical battery policy on the daemon side
- Reduce client-side and daemon-side wake-ups
- Register objects on the bus once they've been setup
- Remove DeviceChanged and Changed signals
- Remove OnLowBattery property (use WarningLevel instead)
- Remove QoS support
- Remove battery recall support

* Fri Oct 18 2013 Richard Hughes <rhughes@redhat.com> - 0.9.23-1
- New upstream release
- Add missing dbus-glib-1 to private requires
- Avoid trying to close fd that wasn't opened
- Disable Watts-Up devices by default
- Don't guess discharging state for devices
- Fix crasher calling _about_to_sleep_sync()
- Really don't overwrite retval with prop values
- Update and correct Toshiba recall list

* Wed Oct 09 2013 Bastien Nocera <bnocera@redhat.com> 0.9.22-1
- Update to 0.9.22
- Fixes incorrect reporting of some properties
- Fixes battery values for Logitech unifying devices
- Bluetooth input devices support
- Device name fixes

* Fri Jul 26 2013 Richard Hughes <rhughes@redhat.com> - 0.9.21-1
- New upstream release
- Add support for Logitech Wireless (NonUnifying) devices
- Allow clients to call org.freedesktop.DBus.Peer
- Update the upower man page with all the current options
- Use PIE to better secure installed tools and also use full RELRO in the daemon

* Thu Apr 25 2013 Matthias Clasen <mclasen@redhat.com> - 0.9.20-3
- Enabled hardened build
- Don't use /lib/udev in file paths

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 0.9.20-2
- Rebuild

* Mon Mar 11 2013 Richard Hughes <rhughes@redhat.com> - 0.9.20-1
- New upstream release
- Add a --enable-deprecated configure argument to remove pm-utils support
- Deprecate running the powersave scripts
- Factor out the Logitech Unifying support to support other devices
- Require unfixed applications to define UPOWER_ENABLE_DEPRECATED
- Fix batteries which report current energy but full charge
- Fix several small memory leaks

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Richard Hughes <rhughes@redhat.com> - 0.9.19-1
- New upstream release
- Add a Documentation tag to the service file
- Add support for Logitech Unifying devices
- Do not continue to poll if /proc/timer_stats is not readable
- Fix device matching for recent kernels
- Resolves: #848521

* Wed Oct 24 2012 Dan Horák <dan[at]danny.cz> - 0.9.18-2
- the notify-upower script is not installed with dummy backend on s390(x)

* Wed Aug 08 2012 Richard Hughes <rhughes@redhat.com> - 0.9.18-1
- New upstream release
- Use systemd for suspend and hibernate

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
