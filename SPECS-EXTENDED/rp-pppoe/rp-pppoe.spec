Name: rp-pppoe
Version: 4.0
Release: 5%{?dist}
Summary: A PPP over Ethernet client (for xDSL support).
License: GPL-2.0-or-later
Url: https://dianne.skoll.ca/projects/rp-pppoe/

Source: https://dianne.skoll.ca/projects/rp-pppoe/download/rp-pppoe-%{version}.tar.gz

BuildRequires: make
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: coreutils
BuildRequires: ppp-devel
BuildRequires: systemd

Requires: ppp >= 2.4.6
Requires: iproute >= 2.6
Requires: coreutils
Requires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. This package contains the
Roaring Penguin PPPoE client, a user-mode program that does not
require any kernel modifications. It is fully compliant with RFC 2516,
the official PPPoE specification.

%prep
%autosetup -p1

%build
cd src
%configure #--docdir=%{_pkgdocdir}
make

%install
mkdir -p %{buildroot}%{_sbindir} %{buildroot}%{_unitdir}

make -C src install DESTDIR=%{buildroot}
rm -rf %{buildroot}/etc/ppp/plugins

%files
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%{_sbindir}/*
%{_mandir}/man?/*
%doc %{_docdir}/*

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 27 2023 Than Ngo <than@redhat.com> - 4.0-1
- fix #2190023, update to 4.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 07 2021 Than Ngo <than@redhat.com> - 3.15-1
- fix bz#1958237, Rebase to 3.15

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.14-5
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Than Ngo <than@redhat.com> - 3.14-1
- update to 3.14

* Wed Apr 08 2020 Than Ngo <than@redhat.com> - 3.13-1
- update to 3.13

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.12-11
- Escape macros in %%changelog

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Than Ngo <than@redhat.com> - 3.12-8
- fixed bz#1469960, conflict glibc/kernel header 

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jun 03 2016 Than Ngo <than@redhat.com> - 3.12-6
- bz#948950, fix manpage issue

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Than Ngo <than@redhat.com> - 3.12-4
- fix issue rp-pppoe plugin cannot be found

* Mon Dec 14 2015 Than Ngo <than@redhat.com> - 3.12-3
- drop rp-pppoe plugin, use the one from ppp

* Fri Dec 11 2015 Than Ngo <than@redhat.com> - 3.12-2
- enable rp-pppoe plugin

* Mon Nov 16 2015 Than Ngo <than@redhat.com> - 3.12-1
- update to 3.12

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 21 2015 Than Ngo <than@redhat.com> 3.11-13
- bz#1182077, build for s390 and s390x

* Mon Sep 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.11-12
- Minor fix to pppoe-status (RHBZ 1141660)

* Tue Sep  2 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.11-11
- Cleanup and modernise spec
- Build as a hardened build as per packaging guidelines
- Unify pppoe* scripts on ip use to enable to drop net-tools dependency

* Thu Aug 21 2014 Than Ngo <than@redhat.com> - 3.11-10
- bz#850300, new systemd-rpm macros in rp-pppoe spec file

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 30 2014 Than Ngo <than@redhat.com> - 3.11-8
- bz#1073897, systemd service file pppoe-server.service installed with unnecessary exec perms

* Thu Jul 03 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 3.11-7
- Let package honor %%_pkgdocdir (Fix F20FTBFS RHBZ #993206,
  F21FTBFS RHBZ #1107035).
- Modernize spec.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 08 2013 Than Ngo <than@redhat.com> - 3.11-6
- cleanup

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Than Ngo <than@redhat.com> - 3.11-4
- bz#961529, add Requirement on net-tools

* Thu Apr 25 2013 Than Ngo <than@redhat.com> - 3.11-3
- build with -fno-strict-aliasing

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Than Ngo <than@redhat.com> - 3.11-1
- 3.11
- bz#540763, add IP allocation by pppd ability to pppoe-server
- bz#808676, add missing %% symbol for triggerun

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Mar 19 2012 Than Ngo <than@redhat.com> - 3.10-12
- fix bz#804396, add missing [Unit] section

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 3.10-11
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 05 2011 Than Ngo <than@redhat.com> - 3.10-9
- bz#697664, native systemd file

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 07 2009 Than Ngo <than@redhat.com> - 3.10-7
- fix url

* Wed Sep 09 2009 Than Ngo <than@redhat.com> - 3.10-6
- rebuilt

* Wed Sep 09 2009 Than Ngo <than@redhat.com> - 3.10-5
- wrong path to initscript bz#522010
- add remove services in %%postun/%%preun

* Mon Sep 07 2009 Than Ngo <than@redhat.com> - 3.10-4
- add feature, save and restore all information about default routes bz#191242
- add startup script for pppoe-server bz#507123

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov 11 2008 Than Ngo <than@redhat.com> 3.10-1
- 3.10

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.8-5
- fix license tag

* Thu Apr 10 2008 Karsten Hopp <karsten@redhat.com> 3.8-4
- Build with $RPM_OPT_FLAGS (#249978) (Ville Skyttä)

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 3.8-3
- rebuild

* Tue Mar 20 2007 Than Ngo <than@redhat.com> - 3.8-2.fc7
- setting DEBUG for adsl-start causes adsl-connect to exit, #195828

* Tue Mar 20 2007 Than Ngo <than@redhat.com> - 3.8-1.fc7
- update to 3.8

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.5-32.1
- rebuild

* Sat Jun 10 2006 Than Ngo <than@redhat.com> 3.5-32
- fix build problem in mock

* Wed Feb 15 2006 Than Ngo <than@redhat.com> 3.5-31
- apply patch to use mktemp

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.5-30.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.5-30.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Aug 15 2005 Than Ngo <than@redhat.com> 3.5-30
- defaultroute should not overridden #152014

* Mon Jul 04 2005 Than Ngo <than@redhat.com> 3.5-29 
- fix broken dependencies 

* Mon Jun 13 2005 Than Ngo <than@redhat.com> 3.5-28
- use iproute2 instead of old ifconfig #134816

* Mon Mar 07 2005 Than Ngo <than@redhat.com> 3.5-27
- rebuilt

* Sat Jan 22 2005 Than Ngo <than@redhat.com> 3.5-26
- rename config files #145255

* Wed Jan 19 2005 David Woodhouse <dwmw2@redhat.com> 3.5-25
- Kill br2684ctl after ifdown if we started it

* Wed Jan 19 2005 David Woodhouse <dwmw2@redhat.com> 3.5-24
- Add support for RFC2684 Ethernet-over-ATM (for PPPoE-over-ATM)

* Mon Nov 22 2004 Than Ngo <than@redhat.com> 3.5-23
- fix typo in adsl-setup #140287

* Fri Oct 15 2004 Than Ngo <than@redhat.com> 3.5-22
- Fix ip conflict in dsl connect, #135012

* Thu Oct 07 2004 David Woodhouse <dwmw2@redhat.com> 3.5-21
- Fix ordering of VCI and VPI in pppoatm address.

* Thu Oct 07 2004 David Woodhouse <dwmw2@redhat.com> 3.5-20
- Add support for static IP with demand option.
- Add support for using PPP over ATM plugin.

* Thu Oct 07 2004 Than Ngo <than@redhat.com> 3.5-19
- fix typo bug in adsl connect
- remove unused rp-pppoe plugin, it's now included in new ppppd

* Wed Oct 06 2004 Than Ngo <than@redhat.com> 3.5-18
- fix adsl connect for using MTU/MRU

* Thu Sep 30 2004 Than Ngo <than@redhat.com> 3.5-17
- fix idle parameter in asdl connect

* Mon Aug 02 2004 Than Ngo <than@redhat.com> 3.5-16
- use iptables instead ipchains, thanks to Robert Scheck

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr 01 2004 Than Ngo <than@redhat.com> 3.5-14
- fixed typo 

* Tue Mar 30 2004 Than Ngo <than@redhat.com> 3.5-13
- fixed reconnect problem

* Mon Mar 29 2004 Than Ngo <than@redhat.com> 3.5-12
- fixed wrong idle parameter, #119280

* Thu Mar 04 2004 Than Ngo <than@redhat.com> 3.5-11
- fixed default route problem, #114875
- fixed restart issue, #100610
- fixed a bug in adsl status

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Nov 10 2003 Than Ngo <than@redhat.com> 3.5-9
- better fix for nickename issue

* Wed Oct 29 2003 Than Ngo <than@redhat.com> 3.5-8
- fix a bug in connect script

* Mon Oct 27 2003 Than Ngo <than@redhat.com> 3.5-7
- fix nickename issue

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Than Ngo <than@redhat.com> 3.5-5
- add correct PPOE_TIMEOUT/LCP_INTERVAL bug #82630

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix initdir in triggerpostun

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Than Ngo <than@redhat.com> 3.5-1
- update to 3.5

* Thu Nov  7 2002 Than Ngo <than@redhat.com> 3.4-8
- unpackaged files issue

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Than Ngo <than@redhat.com> 3.4-5
- Don't forcibly strip binaries

* Sun Jun 09 2002 Than Ngo <than@redhat.com> 3.4-4
- Fix up creation of first device (#64773)

* Fri Jun 07 2002 Than Ngo <than@redhat.com> 3.4-3
- set correct default value for PPPoE timeout (bug #64903)

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Harald Hoyer <harald@redhat.de> 3.4-1
- 3.4
- added kernel plugin

* Sun Apr 14 2002 Than Ngo <than@redhat.com> 3.3-7
- add fix for neat-control

* Sat Feb 23 2002 Than Ngo <than@redhat.com> 3.3-6
- fix a bug in adsl-stop (#60138)

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.3-5
- Fix up creation of first device (#59236)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Dec 16 2001 Than Ngo <than@redhat.com> 3.3-3
- fix bugs #57070, #55627, #55140
- add man pages, Docs and example scripts

* Mon Nov 05 2001 Than Ngo <than@redhat.com> 3.3-2
- fix a bug in adsl-connect

* Wed Sep 19 2001 Than Ngo <than@redhat.com> 3.3-1
- update to 3.3 (bug #53697)

* Thu Aug 16 2001 Than Ngo <than@redhat.com> 3.2-4
- don't print messages as default

* Wed Aug  8 2001 Than Ngo <than@redhat.com>
- fix softlinks

* Sun Jul 22 2001 Than Ngo <than@redhat.com>
- update to 3.2

* Thu Jul 19 2001 Than Ngo <than@redhat.com> 3.0-5
- fix bug in trigger

* Fri Jun 22 2001 Than Ngo <than@redhat.com>
- Copyright -> License
- fix activate ethernet device problem
- get rid of pppoe initscript, use ifup/ifdown
  to activate/shutdown xDSL connection
- convert old pppoe config format into new format
- remove adsl-setup, Users have to use netconf to setup xDSL connection
- excludearch s390

* Mon May 14 2001 Than Ngo <than@redhat.com>
- clean PID files when connection fails (Bug #40349)
- fix order of pppoe script (Bug #40454)

* Wed May 02 2001 Than Ngo <than@redhat.com>
- fixed a firewall bug in adsl-setup (Bug #38550)

* Sun Apr 22 2001 Than Ngo <than@redhat.com>
- update to 3.0 (bug #34075)

* Thu Mar 15 2001 Than Ngo <than@redhat.com>
- fix BOOT enviroment again, it should work fine now 

* Wed Mar 14 2001 Than Ngo <than@redhat.com>
- fix bug in adsl-setup (DEVICE enviroment)

* Thu Feb 08 2001 Than Ngo <than@redhat.com>
- fixed a problem in startup (Bug #26454)
- fixed i18n in initscript (Bug #26540)

* Sat Feb 03 2001 Than Ngo <than@redhat.com>
- updated to 2.6
- some fixes in pppoe script

* Fri Feb 02 2001 Than Ngo <than@redhat.com>
- fixed starting pppoe service at boot time. (Bug #25494)

* Sun Jan 28 2001 Than Ngo <than@redhat.com>
- fixed so that pppoe script does not kill adsl connection when
  the runlevel is changed. 
- remove excludearch ia64

* Tue Jan 23 2001 Than Ngo <than@redhat.com>
- hacked for using USEPEERDNS

* Mon Dec 11 2000 Than Ngo <than@redhat.com>
- updated to 2.5, it fixes a denial-of-service vulnerability

* Tue Aug 08 2000 Than Ngo <than@redhat.de>
- fix german configuration HOWTO to T-DSL

* Mon Aug 07 2000 Than Ngo <than@redhat.de>
- fixes for starting pppd under /usr/sbin
- added german configuration HOWTO to T-DSL

* Tue Aug 01 2000 Than Ngo <than@redhat.de>
- update to 2.2

* Fri Jul 28 2000 Than Ngo <than@redhat.de>
- fixed initscripts so that condrestart doesn't return 1 when the test fails

* Thu Jul 27 2000 Than Ngo <than@redhat.de>
- update to 2.1
- don't detect pppd for building

* Thu Jul 27 2000 Than Ngo <than@redhat.de>
- rename the rp-pppoe startup script (Bug #14734)

* Wed Jul 26 2000 Bill Nottingham <notting@redhat.com>
- don't run by default; it hangs if not configured

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- prereq /etc/init.d (it's referenced in the initscript)

* Tue Jul 18 2000 Than Ngo <than@redhat.de>
- inits back to rc.d/init.d, using service to fire them up

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul 08 2000 Than Ngo <than@redhat.de>
- add Prereq: /etc/init.d

* Fri Jun 30 2000 Than Ngo <than@redhat.de>
- turned off deamon by default

* Tue Jun 27 2000 Than Ngo <than@redhat.de>
- don't prereq, only require initscripts

* Mon Jun 26 2000 Than Ngo <than@redhat.de>
- /etc/rc.d/init.d -> /etc/init.d
- add condrestart directive
- fix post/preun/postun scripts
- prereq initscripts >= 5.20

* Sun Jun 18 2000 Than Ngo <than@redhat.de>
- use RPM macros
- rebuilt in the new build environment

* Wed May 31 2000 Than Ngo <than@redhat.de> 
- adopted for Winston.
