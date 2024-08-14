%global _hardened_build 1

Summary: Network diagnostic tool combining 'traceroute' and 'ping'
Name: mtr
Version: 0.95
Release: 2%{?dist}
License: GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://www.bitwizard.nl/mtr/
Source0: https://github.com/traviscross/mtr/archive/v%{version}/%{name}-%{version}.tar.gz
Source1: net-x%{name}.desktop
Source2: mtr-gtk-pkexec-wrapper.sh
Source3: org.fedoraproject.mtr.policy

BuildRequires: ncurses-devel
BuildRequires: autoconf automake libtool git

%description
MTR combines the functionality of the 'traceroute' and 'ping' programs
in a single network diagnostic tool.

When MTR is started, it investigates the network connection between the
host MTR runs on and the user-specified destination host. Afterwards it
determines the address of each network hop between the machines and sends
a sequence of ICMP echo requests to each one to determine the quality of
the link to each machine. While doing this, it prints running statistics
about each machine.

MTR provides two user interfaces: an ncurses interface, useful for the
command line, e.g. for SSH sessions; and a GTK+ interface for X (provided
in the mtr-gtk package).

%prep
%autosetup

%build
export CFLAGS="%{optflags} -fPIE"
export LDFLAGS="-z now -pie"

# Upstream forgot to ship .tarball-version
echo "%{version}" > .tarball-version

./bootstrap.sh
%configure --without-gtk
%make_build

%install
install -D -p -m 0755 mtr %{buildroot}%{_sbindir}/mtr
%make_install

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS FORMATS NEWS README.md SECURITY
%{_sbindir}/%{name}
%caps(cap_net_raw=pe) %{_sbindir}/%{name}-packet
%{_mandir}/man8/*
%dir %{_datadir}/bash-completion/
%dir %{_datadir}/bash-completion/completions/
%{_datadir}/bash-completion/completions/%{name}

%changelog
* Mon Jul 22 2024 Aditya Dubey <adityadubey@microsoft.com> - 0.95-2
- Promoting package from SPECS-EXTENDED to SPECS

* Thu Jun 23 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 0.95-1
- Upgrade version to 0.95 to fix build break
- License verified

* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 0.92-8
- Remove epoch

* Fri Jan 08 2021 Joe Schmitt <joschmit@microsoft.com> - 2:0.92-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove x11 support

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.92-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.92-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.92-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.92-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 26 2017 Robert Scheck <robert@fedoraproject.org> - 2:0.92-1
- Rebase to 0.92 (#1458265)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.87-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.87-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar  2 2017 Michal Sekletar <msekleta@redhat.com> - 2:0.87-4
- Don't include git revision in version string

* Wed Mar 01 2017 Michal Sekletar <msekleta@redhat.com> - 2:0.87-3
- One more version bump for the same reason (hopefully last one)

* Wed Mar 01 2017 Michal Sekletar <msekleta@redhat.com> - 2:0.87-2
- Rebuilt because previous build doesn't have correct dist-tag

* Tue Feb 28 2017 Michal Sekletar <msekleta@redhat.com> - 2:0.87-1
- Rebase to latest upstream (#1365128)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.86-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May 13 2016 Michal Sekletar <msekleta@redhat.com> - 2:0.86-1
- rebase to 0.86

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:0.85-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.85-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.85-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.85-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Oct 18 2013 Michal Sekletar <msekleta@redhat.com> - 2:0.85-4
- rebuild with new upstream tarball for release 0.85 (#1020926)

* Tue Oct 01 2013 Michal Sekletar <msekleta@redhat.com> - 2:0.85-3
- enable hardened build
- migrate from consolehelper to policykit (#502750)
- specfile cleanup
- introduce grace period (#1009051)
- query all ipv6 nameservers (#966174)
- add missing documentation (#1015552)

* Mon Aug 05 2013 Michal Sekletar <msekleta@redhat.com> - 2:0.85-2
- add generate-tarball.sh script

* Sun Aug 04 2013 Michal Sekletar <msekleta@redhat.com> - 2:0.85-1
- update to 0.85
- fix bogus dates in changelog

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.84-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Michal Sekletar <msekleta@redhat.com> - 2:0.84-2
- fix crash when dns resolver is configured with both IPv4 and IPv6 nameservers

* Wed Apr 03 2013 Michal Sekletar <msekleta@redhat.com> - 2:0.84-1
- update to the newest upstream release
- specfile cleanup

* Mon Feb 18 2013 Adam Tkac <atkac redhat com> - 2:0.83-2
- make non-gtk version of mtr buildable

* Mon Feb 18 2013 Adam Tkac <atkac redhat com> - 2:0.83-1
- update to 0.83
- patches merged
  - mtr081-rh703549.patch

* Thu Feb 14 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 2:0.82-5
- Remove --vendor flag from desktop-file-install https://fedorahosted.org/fesco/ticket/1077

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 07 2011 Adam Tkac <atkac redhat com> - 2:0.82-1
- update to 0.82

* Tue Nov 01 2011 Adam Tkac <atkac redhat com> - 2:0.81-1
- update to 0.81
- mtr-now-waits-for-last-response.patch is no longer needed
- fixed wide report output (#703549)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Adam Tkac <atkac redhat com> 2:0.80-2
- use file capabilities instead of SUID (#646479)

* Tue Oct 26 2010 Jan Görig <jgorig redhat com> 2:0.80-1
- update to 0.80
- mtr now waits for last sent packet (#611739)
- fixed crashes in XML format
- XML format fixes

* Mon Jun 28 2010 Adam Tkac <atkac redhat com> 2:0.79-1
- update to 0.79
- patches merged
  - mtr-0.75-fd-flags.path
  - mtr075-rh516603.patch

* Mon Dec 07 2009 Adam Tkac <atkac redhat com> 2:0.75-6
- install mtr as SUID binary (#518828)
- use fprintf instead of perror when getaddrinfo fails (#516603)

* Fri Sep 25 2009 Adam Tkac <atkac redhat com> 2:0.75-5
- remove unneeded build requires (#525547)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.75-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 29 2008 Zdenek Prikryl <zprikryl@redhat.com> - 2:0.75-2
- Fixed setting socket flags in ipv4 only environment (#467964)

* Tue Sep 23 2008 Zdenek Prikryl <zprikryl@redhat.com> - 2:0.75-1
- Updated to 0.75
- Removed confusing underflow patch
- Removed format patch bacause of -w option

* Tue Sep 09 2008 Zdenek Prikryl <zprikryl@redhat.com> - 2:0.74-1
- Updated to 0.74

* Tue Sep 02 2008 Zdenek Prikryl <zprikryl@redhat.com> - 2:0.73-2
- Minor fix in the patch underflow

* Wed May 21 2008 Zdenek Prikryl <zprikryl@redhat.com> - 2:0.73-1
- Updated to 0.73
- Fixed mtr-0.69-CVE-2002-0497.patch
- Added build requirement for GTK+

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:0.72-4
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Marcela Maslanova <mmaslano@redhat.com> - 2:0.72-3
- rebuild for mas rebuild
- check license

* Thu Mar 15 2007 Karsten Hopp <karsten@redhat.com> 2:0.72-2
- rebuild with current gtk2 to add png support (#232013)

* Thu Feb 22 2007 Marcela Maslanova <mmaslano@redhat.com> - 2:0.72-1
- review
- rhbz#226164

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:0.71-3.1
- rebuild

* Mon Jul 3 2006 Marcela Maslanova <mmaslano@redhat.com> - 2:0.71-3
- bugzilla #195458 – reverse-map bug in mtr and patch - resolving ipv6 hostname correctly

* Tue May 30 2006 Marcela Maslanova <mmaslano@redhat.com> - 2:0.71-2
- underflow solved

* Fri Mar 24 2006 Miroslav Lichvar <mlichvar@redhat.com> - 2:0.71-1
- update to mtr-0.71

* Thu Mar 23 2006 Miroslav Lichvar <mlichvar@redhat.com> - 2:0.70-1
- update to mtr-0.70
- replace s390x patch, drop automake dependency

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:0.69-7.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:0.69-7.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Oct 21 2005 Phil Knirsch <pknirsch@redhat.com> 2:0.69-7
- Fixed xmtr to be installed in /usr/bin instead of /usr/X11R6/bin (#170945)

* Mon Oct 10 2005 Phil Knirsch <pknirsch@redhat.com> 2:0.69-6
- Added missing gtk+-devel BuildPreReq (#168215)

* Fri Oct  7 2005 Tomas Mraz <tmraz@redhat.com> 2:0.69-5
- use include instead of pam_stack in pam config

* Mon Sep 05 2005 Phil Knirsch <pknirsch@redhat.com> 2:0.69-4
- Made the output, especially for reports much more readable (#147865)
- Fixed --address option (#162029)

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 2:0.69-3
- bump release and rebuild with gcc 4

* Thu Feb 10 2005 Karsten Hopp <karsten@redhat.de> 2:0.69-2
- build with --enable-gtk2 (John Thacker)

* Wed Feb 09 2005 Phil Knirsch <pknirsch@redhat.com> 2:0.69-1
- Updated to mtr-0.69
- Dropped quite a few patches
- Forewardported the CVE patch

* Mon Oct 18 2004 Phil Knirsch <pknirsch@redhat.com> 2:0.54-10
- rebuilt

* Wed Oct 06 2004 Phil Knirsch <pknirsch@redhat.com> 2:0.54-9
- Add CVE patch for security reasons (#129386)
- Add patch to fix broken --address option (#132628)
- Add patch to fix broken reverse DNS lookups for ipv6 (#134532)

* Tue Aug 24 2004 Warren Togami <wtogami@redhat.com> 2:0.54-8
- #121705 and other spec cleanups
- remove redundant documentation

* Thu Jul 01 2004 Phil Knirsch <pknirsch@redhat.com> 0.54-7
- Fixed broken behaviour with resolver SERVFAIL results (#125392)
- Added ncurses-devel libtermcap-devel as BuildPreReq (#124553)
- Added gtk+ Requires for mtr-gtk package (#121705)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 21 2004 Phil Knirsch <pknirsch@redhat.com> 0.54-5
- Removed absolute path for Icon in desktop file (#120170)

* Mon Feb 16 2004 Phil Knirsch <pknirsch@redhat.com>
- Added IPv6 patch from ftp://ftp.kame.net/pub/kame/misc/mtr-054-*
- Enabled IPv6 in mtr.
- Included fix from Robert Scheck to make GTK optional in configure.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 04 2004 Phil Knirsch <pknirsch@redhat.com> 0.54-2
- Fix to build on current tree.

* Sat Oct 18 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.54

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Phil Knirsch <pknirsch@redhat.com> 0.52-1
- Update to latest upstream version (0.52).

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com> 0.49-9
- Remove absolute paths from the PAM configuration, ensuring that the modules
  for the right arch get used on multilib systems.
- Remove Icon:.

* Tue Sep 24 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.49-7a
- Fix build on s390x

* Mon Aug 19 2002 Phil Knirsch <pknirsch@redhat.com> 0.49-7
- Fixed consolehelper support.

* Wed Aug 07 2002 Phil Knirsch <pknirsch@redhat.com> 0.49-6
- Desktop file fixes (#69550).

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.49-5
- automated rebuild

* Tue Jun 18 2002 Phil Knirsch <pknirsch@redhat.com> 0.49-4
- Added consolehelper support to xmtr.

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Phil Knirsch <pknirsch@redhat.com> 0.49-2
- Fixed autoFOO problems.

* Fri Mar 08 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- 0.49 update

* Thu Mar 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- 0.48 update

* Mon Jun 25 2001 Preston Brown <pbrown@redhat.com>
- 0.44 bugfix release
- fix display of icon in .desktop entry

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Feb 12 2001 Preston Brown <pbrown@redhat.com>
- don't advertise gtk support in non-gtk binary (#27172)

* Fri Oct 20 2000 Bill Nottingham <notting@redhat.com>
- fix autoconf check for resolver functions

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- fix group

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul  6 2000 Bill Nottingham <notting@redhat.com>
- fix setuid bit
- remove symlink
- force build of non-gtk version

* Mon Jun 19 2000 Preston Brown <pbrown@redhat.com>
- disable SUID bits
- desktop entry

* Mon Jun 19 2000 Than Ngo <than@redhat.de>
- FHS fixes

* Fri May 26 2000 Preston Brown <pbrown@redhat.com>
- adopted for Winston

* Thu Aug 19 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.41-1]
- Added afr's patch to allow disabeling of gtk without Robn's hack.
- Made report mode report the newly added extra resolution.

* Wed Aug 18 1999 Ryan Weaver <ryanw@infohwy.com>
- renamed mtr-gtk to xmtr
- added symlink from /usr/bin/mtr to /usr/sbin/mtr

  [mtr-0.40-1]
- Fixed some problems with HPUX and SunOS.
- Included Olav Kvittem's patch to do packetsize option.
- Made the timekeeping in micro seconds.

* Thu Jun 10 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.39-1]
- Updated to version 0.39.

* Wed Jun  9 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.38-1]
- Updated to version 0.38.

* Thu Apr 15 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.37-2]
- Changed RPM headers to conform to Red Hat Contrib|Net specs.

* Mon Apr 12 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.37-1]
- v0.37
- Added Bill Bogstad's "show the local host & time" patch.
- Added R. Sparks' show-last-ping patch, submitted by Philip Kizer.

- v0.36
- Added Craigs change-the-interval-on-the-fly patch.
- Added Moritz Barsnick's "do something sensible if host not found"
  patch.
- Some cleanup of both Craigs and Moritz' patches.

* Wed Apr  7 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.35-1]
- v0.35
- Added Craig Milo Rogers pause/resume for GTK patch.
- Added Craig Milo Rogers cleanup of "reset". (restart at the beginning)
- Net_open used to send a first packet. After that the display-driver
  got a chance to distort the timing by taking its time to initialize.

* Mon Apr  5 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.34-1]
- v0.34
- Added Matt's nifty "use the icmp unreachables to do the timing" patch.
- Added Steve Kann's pause/resume patch.

* Wed Mar 10 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.33-1]
- v0.33
- Fixed the Linux glibc resolver problems.
- Fixed the off-by-one problem with -c option.

* Mon Mar  8 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.32-1]
- v0.32
- Fixed the FreeBSD bug detection stuff.

* Fri Mar  5 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.31-1]
- v0.31
- Fixed a few documentation issues. -- Matt
- Changed the autoconf stuff to find the resolver library on
  Solaris. -- REW
- Cleaned up the autoconf.in file a bit. -- Matt.

* Thu Mar  4 1999 Ryan Weaver <ryanw@infohwy.com>
  [mtr-0.30-1]
- Build gtk version against gtk+-1.2.0
- v0.30
- Fixed a typo in the changelog (NEWS) entry for 0.27. :-)
- added use of "MTR_OPTIONS" environment variable for defaults.
