Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# hardened build if not overridden
%{!?_hardened_build:%global _hardened_build 1}

%if %{?_hardened_build}%{!?_hardened_build:0}
%global harden -pie -Wl,-z,relro,-z,now
%endif

Summary: ACPI Event Daemon
Name: acpid
Version: 2.0.32
Release: 3%{?dist}
License: GPLv2+
Source: https://downloads.sourceforge.net/acpid2/%{name}-%{version}.tar.xz
Source2: acpid.video.conf
Source3: acpid.power.conf
Source4: acpid.power.sh
Source5: acpid.service
Source6: acpid.sysconfig
Source7: acpid.socket
# https://sourceforge.net/p/acpid2/tickets/14/
Patch0: acpid-2.0.32-kacpimon-dynamic-connections.patch
ExclusiveArch: ia64 x86_64 %{ix86} %{arm} aarch64
URL: https://sourceforge.net/projects/acpid2/
BuildRequires: systemd, gcc
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires: systemd

%description
acpid is a daemon that dispatches ACPI events to user-space programs.

%prep
%setup -q
%patch 0 -p1 -b .kacpimon-dynamic-connections

%build
%configure
make %{?_smp_mflags} CFLAGS="%{optflags} %{?harden}"

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}
make install DESTDIR=%{buildroot} docdir=%{_docdir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/acpi/events
mkdir -p %{buildroot}%{_sysconfdir}/acpi/actions
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig

chmod 755 %{buildroot}%{_sysconfdir}/acpi/events
install -p -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/acpi/events/videoconf
install -p -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/acpi/events/powerconf
install -p -m 755 %{SOURCE4} %{buildroot}%{_sysconfdir}/acpi/actions/power.sh
install -p -m 644 %{SOURCE5} %{SOURCE7} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/sysconfig/acpid

%files
%doc %{_docdir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.socket
%dir %{_sysconfdir}/acpi
%dir %{_sysconfdir}/acpi/events
%dir %{_sysconfdir}/acpi/actions
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/videoconf
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/acpi/events/powerconf
%config(noreplace) %attr(0755,root,root) %{_sysconfdir}/acpi/actions/power.sh
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/acpid
%{_bindir}/acpi_listen
%{_sbindir}/acpid
%{_sbindir}/kacpimon
%{_mandir}/man8/acpid.8.gz
%{_mandir}/man8/acpi_listen.8.gz
%{_mandir}/man8/kacpimon.8.gz

%pre
if [ "$1" = "2" ]; then
	conflist=`ls %{_sysconfdir}/acpi/events/*.conf 2> /dev/null`
	RETCODE=$?
	if [ $RETCODE -eq 0 ]; then
		for i in $conflist; do
			rmdot=`echo $i | sed 's/.conf/conf/'`
			mv $i $rmdot
		done
	fi
fi

%post
%systemd_post %{name}.socket %{name}.service

%preun
%systemd_preun %{name}.socket %{name}.service

%postun
%systemd_postun_with_restart %{name}.socket %{name}.service

%triggerun -- %{name} < 2.0.10-2
	/sbin/chkconfig --del acpid >/dev/null 2>&1 || :
	/bin/systemctl try-restart acpid.service >/dev/null 2>&1 || :

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.32-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 20 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.32-1
- New version
  Resolves: rhbz#1742776

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 15 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.30-2
- Dropped sysvinit support

* Thu Jul 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.30-1
- New version
  Resolves: rhbz#1602974

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.29-1
- New version
  Resolves: rhbz#1568392

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.0.28-8
- Add gcc to BuildRequires

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.28-6
- Switched kacpimon to dynamic connections (increased max connections
  from 20 to 1024)
  Resolves: rhbz#1450980
- Consolidated new line delimiters

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Ondřej Lysoněk <olysonek@redhat.com> - 2.0.28-2
- Fixed obtaining process list in power.sh to avoid SELinux denials
  Resolves: rhbz#1408457

* Fri Sep 16 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.28-1
- New version
  Resolves: rhbz#1376618

* Wed Aug  3 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.27-4
- Fixed service autostart (if enabled)
  Resolves: rhbz#1363632

* Wed Jul 20 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.27-3
- Added exception for plasmashell to power.sh
  Related: rhbz#1319885

* Wed Jul 20 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.27-2
- Added exception for kded5 to power.sh
  Resolves: rhbz#1319885

* Wed Mar 16 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.27-1
- New version
  Resolves: rhbz#1299109

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.25-4
- Preserve timestamps on installed files

* Wed Sep  2 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.25-3
- Fixed typo

* Wed Sep  2 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.25-2
- Simplified macros check related to hardening

* Mon Aug 17 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.25-1
- New version
  Resolves: rhbz#1253985

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.23-4
- Used socket for stdin to support socket activation

* Tue May 19 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.23-3
- Changed PATH to /usr/sbin:/usr/bin in power.sh
  Resolves: rhbz#1192817

* Thu Mar 05 2015 Adam Jackson <ajax@redhat.com> 2.0.23-2
- Drop sysvinit subpackage in F23+

* Tue Aug 26 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.23-1
- New version
  Resolves: rhbz#1133263

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Dennis Gilmore <dennis@ausil.us> - 2.0.22-2
- enable building on aarch64 and 32 bit arm

* Mon Mar 17 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.22-1
- New version

* Tue Feb 18 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.21-2
- Used unitdir macro instead of the hardcoded systemd paths

* Wed Feb 12 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.21-1
- New version
  Resolves: rhbz#1054057

* Fri Jan 10 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.0.20-3
- Use socket activation, fix rpmlint tabs vs spaces warnings.

* Wed Nov 13 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.20-2
- Fixed loginctl and added support for cinnamon and mate (patch by Leigh Scott)
  Resolves: rhbz#1029868

* Mon Sep 16 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.20-1
- New version
  Resolves: rhbz#1008344
- Fixed bogus date in changelog (best effort)

* Wed Aug 14 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.19-6
- Added systemd build requires
  Resolves: rhbz#995158

* Mon Aug 12 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.19-5
- Hardened build
  Resolves: rhbz#983609

* Fri Aug  9 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.19-4
- Fixed systemd requires
  Resolves: rhbz#995158

* Tue Aug  6 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.19-3
- Used unversioned docs
  Resolves: rhbz#993661

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.19-1
- New version

* Mon Feb 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.18-3
- Switched to systemd-rpm macros
  Resolves: rhbz#850020

* Fri Feb 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.18-2
- Fixed source URL

* Fri Feb 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.18-1
- New version
- Replaced RPM_BUILD_ROOT variables by {buildroot} macros
- Updated URLs to project home page and source code
- Dropped mk patch, handled better way in the spec

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 17 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.17-1
- New version
  Resolves: rhbz#857695

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.16-4
- Update of power.sh to be compatible with new systemd-loginctl
  Resolves: rhbz#819547

* Thu Jun 14 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.16-3
- Silenced possible ck-list-sessions errors in power.sh

* Thu Jun 14 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.16-2
- Added support for systemd-loginctl list-sessions
  Resolves: rhbz#819559

* Thu Mar 29 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.16-1
- New version

* Fri Mar 16 2012 Jiri Skala <jskala@redhat.com> - 2.0.15-1
- updated to latest upstream 2.0.15

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jan 02 2012 Jiri Skala <jskala@redhat.com> - 2.0.14-2
- fixes #722325 - xfce4-power-manager does not seem to be supported

* Mon Dec 19 2011 Jiri Skala <jskala@redhat.com> - 2.0.14-1
- updated to latest upstream 2.0.14

* Wed Nov 16 2011 Jiri Skala <jskala@redhat.com> - 2.0.13-1
- updated to latest upstream 2.0.13

* Tue Aug 16 2011 Jiri Skala <jskala@redhat.com> - 2.0.12-1
- updated to latest upstream 2.0.12

* Mon Aug 01 2011 Jiri Skala <jskala@redhat.com> - 2.0.11-1
- updated to latest upstream 2.0.11

* Mon Jun 27 2011 Jiri Skala <jskala@redhat.com> - 2.0.10-2
- fixes #716923 - move SysV initscript file into an optional subpackage

* Wed May 18 2011 Jiri Skala <jskala@redhat.com> - 2.0.10-1
- update to latest upstream 2.0.10

* Fri May 06 2011 Bill Nottingham <notting@redhat.com> - 2.0.9-4
- fix systemd scriptlets to properly handle upgrade

* Tue May 03 2011 Jiri Skala <jskala@redhat.com> - 2.0.9-3
- corrected relase number to be min equal to f15

* Mon Apr 18 2011 Jiri Skala <jskala@redhat.com> - 2.0.9-1
- update to latest upstream 2.0.9

* Wed Feb 16 2011 Jiri Skala <jskala@redhat.com> - 2.0.8-1
- update to latest upstream 2.0.8

* Wed Feb 09 2011 Jiri Skala <jskala@redhat.com> - 2.0.7-3
- fixes unused varable and coparison of different var types

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Jiri Skala <jskala@redhat.com> - 2.0.7-1
- update to latest upstream
- fixes #660459 - Should be able to set options with /etc/sysconfig/acpi

* Wed Nov 03 2010 Jiri Skala <jskala@redhat.com> - 2.0.5-5
- fixes #648221 - SELinux is preventing /sbin/iwconfig access to a leaked /dev/input/event0 file descriptor

* Wed Sep 29 2010 jkeating - 2.0.5-4
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Jiri Skala <jskala@redhat.com> - 2.0.5-3
- fixes #629740 - acpid doesn't fork, but systemd unit file claims otherwise

* Wed Aug 11 2010 Jiri Skala <jskala@redhat.com> - 2.0.5-2
- fixes #617317 - Providing native systemd file for upcoming F14 Feature Systemd

* Tue Jul 13 2010 Jiri Skala <jskala@redhat.com> - 2.0.5-1
- latest upstream version
- fixes #613315 kernel-2.6.35 doesn't create /proc/acpi/event

* Wed May 05 2010 Jiri Skala <jskala@redhat.com> - 2.0.4-1
- latest upstream version

* Wed Mar 17  2010 Jiri Skala <jskala@redhat.com> - 2.0.3-2
- fixes #575320 - acpid fails to load any event config files

* Thu Feb 25 2010 Jiri Skala <jskala@redhat.com> - 2.0.2-1
- latest upstream version
- removed spare umask
- fixes missing headers

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Apr 23 2009 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.10-1
- Updated to version 1.0.10

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.8-2
- power.sh works with KDE 4.* (#483417)

* Tue Nov 11 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.8-1
- Updated to version 1.0.8
- power.sh works with ConsoleKit >= 0.3.0 (#470752)
- Fixed conditions in power.sh, which look for power-managers (#470752)
- Added check to init script

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.6-8
- fix license tag

* Thu Apr 17 2008 Bill Nottingham <notting@redhat.com> - 1.0.6-7.fc9
- adjust start/stop priority to not conflict with HAL (#442759)

* Thu Feb 14 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-6.fc9
- Update of acpid-1.0.6-makefile.patch, it fix building with gcc 4.3

* Wed Jan 23 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-5.fc9
- Fixed managing of power button (#361501)
- Fixed power script to check for KDE power manager (#419331)

* Fri Nov 23 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-4.fc9
- Removed old logrotate file
- Fixed socket leak (#394431)
- Fixed dumping useless info to log (#389581)

* Tue Oct 23 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-3.fc9
- Silent initscript
- Resolves: #345611

* Wed Sep 26 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-2.fc8
- Fixed leak of a file descriptor
- Resolves: #304761

* Tue Aug 07 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.6-1.fc8
- Updated to version 1.0.6

* Wed Jul 25 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.0.4-8.fc8
- Fixed init script to comply with LSB standard
- Resolves: #237754

* Wed Feb 14 2007 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-7.fc7
- Dropped /var/log/acpid ownership as per review (225237)

* Wed Feb 07 2007 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-6.fc7
- Tons of specfile changes due to review (#225237)

* Tue Oct 10 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-5
- Made acpid a PIE binary (#210016)

* Thu Aug 24 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-4
- Made a better fix for the powerdown button which checks if g-p-m is running
- Don't install sample.conf anymore, not needed

* Thu Aug 10 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-3
- Disable the automatic shutdown -h via powerdown button by default due to
  conflicts with gnome-power-manager

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.4-2.1
- rebuild

* Wed Mar 01 2006 Phil Knirsch <pknirsch@redhat.com> - 1.0.4-2
- Added video.conf file to turn on DPMS when opening the laptop lid. Disabled
  by default.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.4-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Bill Nottingham <notting@redhat.com> - 1.0.4-1
- update to 1.0.4

* Mon Aug  9 2004 Miloslav Trmac <mitr@redhat.com> - 1.0.3-2
- Update to 1.0.3 (fixes #128834)
- s/Copyright/License/
- Add logrotate config file (#110677, from Michal Jaegermann)
- Don't verify contents of /var/log/acpid (#125862)
- Use $RPM_OPT_FLAGS
- Fix and cleanup acpid-1.0.1-pm1.patch
- Add condrestart to %%postun

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Oct 22 2003  Bill Nottingham <notting@redhat.com> 1.0.2-5
- fix handling of sample.conf (#107160)
- mark for translations (#107459)

* Sun Oct 19 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add %%clean specfile target

* Wed Oct  1 2003  Bill Nottingham <notting@redhat.com> 1.0.2-3
- re-enable x86
- don't load the button module

* Thu Aug  7 2003  Bill Nottingham <notting@redhat.com> 1.0.2-2
- no x86 for now

* Mon Jul  7 2003  Bill Nottingham <notting@redhat.com> 1.0.2-1
- update to 1.0.2

* Wed Dec 11 2002  Bill Nottingham <notting@redhat.com> 1.0.1-4
- don't start if /proc/acpi/event isn't there

* Thu Nov 14 2002  Bill Nottingham <notting@redhat.com> 1.0.1-3
- build on more arches

* Mon Aug 26 2002  Bill Nottingham <notting@redhat.com> 1.0.1-2
- tweak default config to run shutdown -h now on a power button event

* Thu Aug 22 2002  Bill Nottingham <notting@redhat.com> 1.0.1-1
- initial build, bang on included specfile

* Fri Mar 15 2002  Tim Hockin <thockin@sun.com>
  - Updated RPM spec with patch from sun for chkconfig on/off
  - Add Changelog, make 'make rpm' use it.

* Wed Mar 13 2002  Tim Hockin <thockin@sun.com>
  - Fixed logging bug - not appending to log (O_APPEND needed)
  - Fix 'make install' to not need root access
  - Fix RPM spec to not need root

* Thu Sep 6 2001 Tim Hockin <thockin@sun.com>
  - 1.0.0

* Thu Aug 16 2001  Tim Hockin <thockin@sun.com>
  - Added commandline options to actions

* Wed Aug 15 2001  Tim Hockin <thockin@sun.com>
  - Added UNIX domain socket support
  - Changed /etc/acpid.d to /etc/acpid/events

* Mon Aug 13 2001  Tim Hockin <thockin@sun.com>
  - added changelog
  - 0.99.1-1

