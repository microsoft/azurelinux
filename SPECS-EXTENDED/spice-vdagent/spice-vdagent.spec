Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           spice-vdagent
Version:        0.20.0
Release:        3%{?dist}
Summary:        Agent for Spice guests
License:        GPLv3+
URL:            https://spice-space.org/
Source0:        https://spice-space.org/download/releases/%{name}-%{version}.tar.bz2
Source1:        https://spice-space.org/download/releases/%{name}-%{version}.tar.bz2.sig
Source2:        victortoso-E37A484F.keyring
BuildRequires:  systemd-devel
BuildRequires:  glib2-devel >= 2.50
BuildRequires:  spice-protocol >= 0.14.1
BuildRequires:  libpciaccess-devel libXrandr-devel libXinerama-devel
BuildRequires:  libXfixes-devel systemd desktop-file-utils libtool
BuildRequires:  alsa-lib-devel dbus-devel libdrm-devel
# For autoreconf, needed after clipboard patch series
BuildRequires:  automake autoconf
BuildRequires:  gnupg2
%{?systemd_requires}

Patch0001: 0001-vdagentd-work-around-GLib-s-fork-issues.patch
Patch0002: 0002-vdagentd-init-static-uinput-before-fork.patch

%description
Spice agent for Linux guests offering the following features:

Features:
* Client mouse mode (no need to grab mouse by client, no mouse lag)
  this is handled by the daemon by feeding mouse events into the kernel
  via uinput. This will only work if the active X-session is running a
  spice-vdagent process so that its resolution can be determined.
* Automatic adjustment of the X-session resolution to the client resolution
* Support of copy and paste (text and images) between the active X-session
  and the client


%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -p1
autoreconf -fi


%build
%configure --with-session-info=systemd --with-init-script=systemd
make %{?_smp_mflags} V=2


%install
make install DESTDIR=$RPM_BUILD_ROOT V=2


%post
%systemd_post spice-vdagentd.service spice-vdagentd.socket

%preun
%systemd_preun spice-vdagentd.service spice-vdagentd.socket

%postun
%systemd_postun_with_restart spice-vdagentd.service spice-vdagentd.socket


%files
%doc COPYING CHANGELOG.md README.md
/usr/lib/udev/rules.d/70-spice-vdagentd.rules
%{_unitdir}/spice-vdagentd.service
%{_unitdir}/spice-vdagentd.socket
%{_prefix}/lib/tmpfiles.d/spice-vdagentd.conf
%{_bindir}/spice-vdagent
%{_sbindir}/spice-vdagentd
%{_var}/run/spice-vdagentd
%{_sysconfdir}/xdg/autostart/spice-vdagent.desktop
# For /usr/share/gdm/autostart/LoginWindow/spice-vdagent.desktop
# We own the dir too, otherwise we must Require gdm
%{_datadir}/gdm
%{_mandir}/man1/%{name}*.1*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Mar 26 2020 Victor Toso <victortoso@redhat.com> 0.20.0-2
- Fix agent shutdown
  Resolves: rhbz#1813667

* Tue Mar 10 2020 Victor Toso <victortoso@redhat.com> 0.20.0-1
- Update to spice-vdagent 0.20.0

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 04 2019 Adam Williamson <awilliam@redhat.com> - 0.19.0-4
- Backport clipboard-race patches for #1755038

* Fri Sep 13 2019 Benjamin Berg <bberg@redhat.com> - 0.19.0-3
- Add patch to lookup graphical session
  https://gitlab.freedesktop.org/spice/linux/vd_agent/merge_requests/2
- Resolves: #1750120

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 12 2019 Victor Toso <victortoso@redhat.com> 0.19.0-1
- Update to spice-vdagent 0.19.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Victor Toso <victortoso@redhat.com> 0.18.0-1
- Update to spice-vdagent 0.18.0

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.17.0-5
- Fix systemd executions/requirements

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Nov 22 2016 Christophe Fergeau <cfergeau@redhat.com> 0.17.0-1
- Update to spice-vdagent 0.17.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 05 2015 Christophe Fergeau <cfergeau@redhat.com> 0.16.0-2
- Add upstream patch fixing a memory corruption bug (double free)
  Resolves: rhbz#1268666
  Exit with a non-0 exit code when the virtio device cannot be opened by the
  agent

* Tue Jun 30 2015 Christophe Fergeau <cfergeau@redhat.com> 0.16.0-1
- Update to 0.16.0 release

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.15.0-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 14 2013 Alon Levy <alevy@redhat.com> - 0.15.0-1
- New upstream release 0.15.0

* Tue Sep 10 2013 Hans de Goede <hdegoede@redhat.com> - 0.14.0-5
- Silence session agent error logging when not running in a vm (rhbz#999804)
- Release guest clipboard ownership on client disconnect (rhbz#1003977)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul  3 2013 Hans de Goede <hdegoede@redhat.com> - 0.14.0-3
- Advertise clipboard line-endings for copy and paste line-ending conversion
- Build spice-vdagentd as pie + relro

* Mon May 20 2013 Hans de Goede <hdegoede@redhat.com> - 0.14.0-2
- Drop the no longer needed /etc/modules-load.d/spice-vdagentd.conf (#963201)

* Fri Apr 12 2013 Hans de Goede <hdegoede@redhat.com> - 0.14.0-1
- New upstream release 0.14.0
- Adds support for file transfers from client to guest
- Adds manpages for spice-vdagent and spice-vdagentd

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Hans de Goede <hdegoede@redhat.com> - 0.12.1-1
- New upstream release 0.12.1
- Fixes various issues with dynamic monitor / resolution support

* Mon Nov 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.12.0-2
- Fix setting of mode on non arbitrary resolution capable X driver
- Fix wrong mouse coordinates on vms with multiple qxl devices

* Sat Sep  1 2012 Hans de Goede <hdegoede@redhat.com> - 0.12.0-1
- New upstream release 0.12.0
- This moves the tmpfiles.d to /usr/lib/tmpfiles.d (rhbz#840194)
- This adds a systemd .service file (rhbz#848102)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Hans de Goede <hdegoede@redhat.com> - 0.10.1-1
- New upstream release 0.10.1

* Thu Mar 22 2012 Hans de Goede <hdegoede@redhat.com> - 0.10.0-1
- New upstream release 0.10.0
- This supports using systemd-logind instead of console-kit (rhbz#756398)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 18 2011 Hans de Goede <hdegoede@redhat.com> 0.8.1-1
- New upstream release 0.8.1

* Fri Jul 15 2011 Hans de Goede <hdegoede@redhat.com> 0.8.0-2
- Make the per session agent process automatically reconnect to the system
  spice-vdagentd when the system daemon gets restarted

* Tue Apr 19 2011 Hans de Goede <hdegoede@redhat.com> 0.8.0-1
- New upstream release 0.8.0

* Mon Mar 07 2011 Hans de Goede <hdegoede@redhat.com> 0.6.3-6
- Fix setting of the guest resolution from a multi monitor client

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Hans de Goede <hdegoede@redhat.com> 0.6.3-4
- Make sysvinit script exit cleanly when not running on a spice enabled vm

* Fri Nov 19 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-3
- Put the pid and log files into their own subdir (#648553)

* Mon Nov  8 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-2
- Fix broken multiline description in initscript lsb header (#648549)

* Sat Oct 30 2010 Hans de Goede <hdegoede@redhat.com> 0.6.3-1
- Initial Fedora package
