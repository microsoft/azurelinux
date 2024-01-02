Summary:        A Router Advertisement daemon
Name:           radvd
Version:        2.19
Release:        1%{?dist}
# The code includes the advertising clause, so it's GPL-incompatible
License:        BSD WITH advertising
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.litech.org/radvd/
Source0:        %{url}dist/%{name}-%{version}.tar.xz
Source1:        radvd-tmpfs.conf
## https://github.com/reubenhwk/radvd/commit/6e45acbf3d64b9bd945adcb3de622fd7d059ceb9.patch
Patch0:         radvd-werror.patch
Patch1:         radvd-endianess.patch
Patch2:         radvd-stderr_logging.patch
Patch3:         radvd-nodaemon_manpage,patch
Patch4:         radvd-double_free_ifacelist.patch

BuildRequires:  bison
BuildRequires:  check-devel
BuildRequires:  flex
BuildRequires:  flex-static
BuildRequires:  gcc
BuildRequires:  pkg-config
BuildRequires:  systemd

Requires(pre):  shadow-utils
%{?systemd_requires}

%description
radvd is the router advertisement daemon for IPv6.  It listens to router
solicitations and sends router advertisements as described in "Neighbor
Discovery for IP Version 6 (IPv6)" (RFC 2461).  With these advertisements
hosts can automatically configure their addresses and some other
parameters.  They also can choose a default router based on these
advertisements.

Install radvd if you are setting up IPv6 network and/or Mobile IPv6
services.

%prep
%setup -q

for F in CHANGES; do
    iconv -f iso-8859-1 -t utf-8 < "$F" > "${F}.new"
    touch -r "$F" "${F}.new"
    mv "${F}.new" "$F"
done

%build
export CFLAGS="%{optflags} -fPIE "
export LDFLAGS='-pie -Wl,-z,relro,-z,now,-z,noexecstack,-z,nodlopen'
%configure \
    --with-check \
    --disable-silent-rules \
    --with-pidfile=/run/radvd/radvd.pid
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}/run/radvd
mkdir -p %{buildroot}%{_unitdir}

install -m 644 redhat/SysV/radvd.conf.empty %{buildroot}%{_sysconfdir}/radvd.conf
install -m 644 redhat/SysV/radvd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/radvd

install -d -m 755 %{buildroot}%{_tmpfilesdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_tmpfilesdir}/radvd.conf
install -m 644 redhat/systemd/radvd.service %{buildroot}%{_unitdir}

%check
make check

%postun
%systemd_postun_with_restart radvd.service

%post
%systemd_post radvd.service

%preun
%systemd_preun radvd.service

# Static UID and GID defined by /usr/share/doc/setup-*/uidgid
%pre
getent group radvd >/dev/null || groupadd -r -g 75 radvd
getent passwd radvd >/dev/null || \
  useradd -r -u 75 -g radvd -d / -s %{_sbindir}/nologin -c "radvd user" radvd
exit 0

%files
%license COPYRIGHT
%doc CHANGES INTRO.html README TODO
%{_unitdir}/radvd.service
%config(noreplace) %{_sysconfdir}/radvd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/radvd
%{_tmpfilesdir}/radvd.conf
%dir %attr(755,radvd,radvd) /run/radvd/
%doc radvd.conf.example
%{_mandir}/*/*
%{_sbindir}/radvd
%{_sbindir}/radvdump

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.19-1
- Auto-upgrade to 2.19 - Azure Linux 3.0 - package upgrades

* Thu Feb 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.18-5
- License verified.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.18-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Pavel Zhukov <pzhukov@redhat.com> - 2.17-19
- change tmpfiles location (#1678147)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 27 2019 Pavel Zhukov <pzhukov@redhat.com> - 2.17-17
- Fix double-free in InterfaceList

* Tue Nov 27 2018 Pavel Zhukov <pzhukov@redhat.com> - 2.17-16
- Depends on network-online target (#1652459)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Pavel Zhukov <pzhukov@redhat.com> - 2.17-14
- Log to stderr in non-daemon mode
- Add nodaemon option into manpage
- Re-enable test again

* Mon Jun 04 2018 Pavel Zhukov <pzhukov@redhat.com> - 2.17-12
- Enable tests and fix them on big endian arches

* Thu Apr 12 2018 Pavel Zhukov <pzhukov@redhat.com> - 2.17-11
- Enable Werror=all

* Mon Feb 19 2018 Pavel Zhukov <pzhukov@redhat.com> - 2.17-10
- Add gcc BR

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Pavel Zhukov <pzhukov@redhat.com> - 2.17-8
- Add systemd BR for unitdir definition

* Tue Jan 30 2018 Pavel Zhukov <pzhukov@redhat.com> - 2.17-7
- removal of systemd-units and conforming to packaging guidelines

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Pavel Zhukov  <landgraf@fedoraproject.org> - 2.17-5
- Revert pid file change
- Don't include /var/run but /run instead
- Drop ghost attr

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 04 2017 Pavel Zhukov  <landgraf@fedoraproject.org> - 2.17-1
- New relase 2.17 (#1467637)

* Fri Jun 30 2017 Pavel Zhukov  <landgraf@fedoraproject.org> - 2.16-2
- Create pid file in /var/run instead of /var/run/radvd (#1438478)

* Sat Apr 15 2017 Pavel Zhukov <landgraf@fedoraproject.org> -2.16-1
- New release 2.16 (#1379105)

* Sat Apr 15 2017 Pavel Zhukov <landgraf@fedoraproject.org> -2.14-3
- FTBFS Do not use glibc headers if linux ones are available (#143873)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 13 2016 Pavel Šimerda <psimerda@redhat.com> - 2.14-1
- New version 2.14

* Wed Jun 22 2016 Pavel Šimerda <psimerda@redhat.com> - 2.13-1
- New version 2.13

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 12 2015 Pavel Šimerda <psimerda@redhat.com> - 2.11-2
- Resolves: #1188891 - radvdump: show routes with prefixlen > 64

* Sat Apr 11 2015 Pavel Šimerda <psimerda@redhat.com> - 2.11-1
- new version 2.11

* Thu Mar 12 2015 Pavel Šimerda <psimerda@redhat.com> - 2.10-1
- new version 2.10

* Fri Oct 10 2014 Pavel Šimerda <psimerda@redhat.com> - 2.8-1
- new version 2.8

* Thu Sep 11 2014 Pavel Šimerda <psimerda@redhat.com> - 2.7-1
- new version 2.7

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Pavel Šimerda <psimerda@redhat.com> - 2.5-1
- new version 2.5

* Wed Jul 30 2014 Pavel Šimerda <psimerda@redhat.com> - 2.2-1
- new version 2.2

* Tue Jul 29 2014 Pavel Šimerda <psimerda@redhat.com> - 2.1-1
- new version 2.1

* Thu Jul 17 2014 Pavel Šimerda <psimerda@redhat.com> - 2.0-1
- new version 2.0

* Fri Jul 11 2014 Pavel Šimerda <psimerda@redhat.com> - 1.14-1
- new version 1.14

* Thu Jun 12 2014 Pavel Šimerda <psimerda@redhat.com> - 1.12-1
- new version 1.12

* Fri Jun 06 2014 Pavel Šimerda <psimerda@redhat.com> - 1.11-1
- new version 1.11

* Mon Mar 24 2014 Pavel Šimerda <psimerda@redhat.com> - 1.10.0-2
- #1079758 - Add support for systemctl-reload action

* Thu Mar 20 2014 Pavel Šimerda <psimerda@redhat.com> - 1.10.0-1
- new package version 1.10.0

* Wed Mar 05 2014 Pavel Šimerda <psimerda@redhat.com> - 1.9.9-1
- bump to 1.9.9

* Wed Mar 05 2014 b'Pavel \xc5\xa0imerda <psimerda@redhat.com>' - b'1.9.9-1\n'
- rebuilt

* Mon Jan 13 2014 Pavel Šimerda <psimerda@redhat.com> - 1.9.8-1
- 1.9.8 bump

* Mon Jan 06 2014 Pavel Šimerda <psimerda@redhat.com> - 1.9.7-2
- #984330 - use _tmpfilesdir macro instead of the old location

* Mon Jan 06 2014 Pavel Šimerda <psimerda@redhat.com> - 1.9.7-1
- 1.9.7 bump

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Petr Pisar <ppisar@redhat.com> - 1.9.2-2
- Create radvd user and and group with ID 75

* Wed Nov 21 2012 Petr Pisar <ppisar@redhat.com> - 1.9.2-1
- 1.9.2 bump

* Wed Aug 22 2012 Petr Pisar <ppisar@redhat.com> - 1.9.1-4
- Modernize systemd scriptlets (bug #850292)

* Tue Aug 07 2012 Petr Pisar <ppisar@redhat.com> - 1.9.1-3
- Remove useless chkconfig invocation (bug #845562)
- Do not reload unit file while unistalling

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 20 2012 Petr Pisar <ppisar@redhat.com> - 1.9.1-1
- 1.9.1 bump

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.9-2
- Drop already defined _GNU_SOURCE symbol

* Fri Jun 15 2012 Petr Pisar <ppisar@redhat.com> - 1.9-1
- 1.9 bump

* Wed May 23 2012 Petr Pisar <ppisar@redhat.com> - 1.8.5-4
- Start service independently on network state (bug #824205)
- Do not force systemd logging to syslog (bug #824205)

* Thu Apr 12 2012 Petr Pisar <ppisar@redhat.com> - 1.8.5-3
- Store PID before daemonizing (bug #811997)

* Tue Apr 03 2012 Petr Pisar <ppisar@redhat.com> - 1.8.5-2
- Clean up spec file
- Remove System V init support
- Fix radvd account creation

* Wed Feb 01 2012 Jiri Skala <jskala@redhat.com> - 1.8.5-1
- update to latest upstream version 1.8.5

* Mon Jan 23 2012 Jiri Skala <jskala@redhat.com> - 1.8.4-1
- update to latest upstream version 1.8.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Jiri Skala <jskala@redhat.com> - 1.8.3-1
- update to latest upstream version 1.8.3

* Mon Oct 10 2011 Jiri Skala <jskala@redhat.com> - 1.8.2-2
- fixes CVE-2011-3602

* Fri Oct 07 2011 Jiri Skala <jskala@redhat.com> - 1.8.2-1
- update to latest upstream version 1.8.2
- this update fixes CVE-2011-360{1..5}

* Wed Aug 24 2011 Jiri Skala <jskala@redhat.com> - 1.8.1-1
- update to latest upstream version 1.8.1

* Fri Aug 12 2011 Jiri Skala <jskala@redhat.com> - 1.8-2
- fixes #729367 - supress unadvisable messages - applied upstream changes

* Tue May 17 2011 Jiri Skala <jskala@redhat.com> - 1.8-1
- update to latest upstream version 1.8

* Mon Feb 28 2011 Jiri Skala <jskala@redhat.com> - 1.7-3
- fixes #679830 - radvd dies when reloading, initscript reports "OK"

* Wed Feb 23 2011 Jiri Skala <jskala@redhat.com> - 1.7-2
- fixes #679821 - provides native systemd service file

* Wed Feb 09 2011 Jiri Skala <jskala@redhat.com> - 1.7-1
- update to latest upstream version 1.7

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 01 2010 Jiri Skala <jskala@redhat.com> - 1.6-4
- #656682 - using tmpfiles.d

* Wed Dec 01 2010 Jiri Skala <jskala@redhat.com> - 1.6-3
- fixes #656682 - using %%ghost on files in /var/run
- added necessary buildrequres flex-static 

* Fri May 21 2010 Jiri Skala <jskala@redhat.com> - 1.6-2
- ensure fax group id == fax user id

* Mon Mar 29 2010 Jiri Skala <jskala@redhat.com> - 1.6-1
- update to latest upstream version

* Mon Jan 25 2010 Jiri Skala <jskala@redhat.com> - 1.5-3
- spec file uses Source1 for radvd.init no more init from tarball
- radvd.init modified to make rmplint more silent
- removed userdel usage from postun

* Wed Jan 13 2010 Jan Gorig <jgorig@redhat.com> - 1.5-2
- mistake in last build

* Wed Jan 13 2010 Jan Gorig <jgorig@redhat.com> - 1.5-1
- updated do latest upstream version
- fixed #554125 - added error message

* Sun Oct 18 2009 Jiri Skala <jskala@redhat.com> - 1.3-4
- fixed #528178 - added force-reload

* Sun Oct 18 2009 Jiri Skala <jskala@redhat.com> - 1.3-3
- fixed #528178 - retval in init script to be posix compliant

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Jiri Skala <jskala@redhat.com> - 1.3-1
- updated to latest upstream version

* Wed Jun 03 2009 Jiri Skala <jskala@redhat.com> - 1.2-3
- changed echos to be able to accept localization

* Tue Apr 28 2009 Jiri Skala <jskala@redhat.com> - 1.2-2
- fixed ambiguous condition in init script (exit 4)

* Mon Apr 27 2009 Jiri Skala <jskala@redhat.com> - 1.2-1
- updated to latest upstream version

* Fri Feb 27 2009 Jiri Skala <jskala@redhat.com> - 1.1-8
- regenerated posix patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Jiri Skala <jskala@redhat.com> - 1.1-6
- init script modified to be POSIX compliant

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1-5
- fix license tag

* Mon Jun 23 2008 Jiri Skala <jskala@redhat.com> - 1.1-4
- radvd.init LSB compliant

* Fri Apr 11 2008 Martin Nagy <mnagy@redhat.com> - 1.1-3
- remove stale pid file on start

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 1.1-2
- fix up string comparison in init script (#427047)

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 1.1-1
- update to new upstream version
- remove patch fixed in upstream: initscript

* Mon Feb 11 2008 Martin Nagy <mnagy@redhat.com> - 1.0-6
- rebuild for gcc-4.3

* Tue Nov 13 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-5
- resolves #376081: The radvd init script exits without doing anything if /usr/sbin/radvd exists

* Thu Aug 23 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-4.1
- Rebuild

* Fri Aug  3 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-4
- resolves: #247041: Initscript Review

* Wed Feb 14 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-3
- specfile cleanup for review

* Thu Feb  1 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-2
- linking with -pie flag turned on again

* Wed Jan 31 2007 Martin Bacovsky <mbacovsk@redhat.com> - 1.0-1
- rebase to upstream 1.0
- Resolves: #225542: radvd 1.0 released

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-4
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 0.9.1-3
- rebuild for new FC-6 build environment

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 0.9.1-2
- fix BuildRequires for Mock

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.9.1-1.1.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jason Vas Dias <jvdias@redhat.com> - 0.9.1-1.1
- rebuild for new gcc, glibc, glibc-kernheaders

* Mon Jan 16 2006 Jason Vas Dias<jvdias@redhat.com> - 0.9.1-1
- Upgrade to upstream version 0.9.1

* Sun Dec 18 2005 Jason Vas Dias<jvdias@redhat.com>
- Upgrade to upstream version 0.9

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Jul 19 2005 Jason Vas Dias <jvdias@redhat.com> 0.8.2.FC5
- fix bug 163593: must use '%%configure' to get correct conf file location

* Mon Jul 18 2005 Jason Vas Dias <jvdias@redhat.com> 0.8-1.FC5
- Upgrade to upstream version 0.8

* Fri Jul  8 2005 Pekka Savola <pekkas@netcore.fi> 0.8-1
- 0.8.
- Ship the example config file as %%doc (Red Hat's #159005)

* Fri Feb 25 2005 Jason Vas Dias <jvdias@redhat.com> 0.7.3-1_FC4
- make version compare > that of FC3

* Mon Feb 21 2005 Jason Vas Dias <jvdias@redhat.com> 0.7.3-1
- Upgrade to radvd-0.7.3
- add execshield -fPIE / -pie compile / link options

* Mon Feb 21 2005 Pekka Savola <pekkas@netcore.fi> 0.7.3-1
- 0.7.3.

* Mon Oct 28 2002 Pekka Savola <pekkas@netcore.fi>
- 0.7.2.

* Tue May  7 2002 Pekka Savola <pekkas@netcore.fi>
- remove '-g %%{RADVD_GID}' when creating the user, which may be problematic
  if the user didn't exist before.

* Fri Apr 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 0.7.1-1
- 0.7.1 (bugfix release, #61023), fixes:
  - Check that forwarding is enabled when starting radvd
    (helps avoid odd problems) 
  - Check configuration file permissions (note: in setuid operation, must not
    be writable by the user.group) 
  - Cleanups and enhancements for radvdump
  - Ensure NULL-termination with strncpy even with overlong strings
    (non-criticals, but better safe than sorry) 
  - Update config.{guess,sub} to cope with some newer architectures 
  - Minor fixes and cleanups 

* Mon Jan 14 2002 Pekka Savola <pekkas@netcore.fi>
- 0.7.1.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Pekka Savola <pekkas@netcore.fi>
- Change 'reload' to signal HUP to radvd instead or restarting.

* Fri Dec 28 2001 Pekka Savola <pekkas@netcore.fi>
- License unfortunately is BSD *with* advertising clause, so to be pedantic,
  change License: to 'BSD-style'.

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- 0.7.0

* Wed Nov 14 2001 Pekka Savola <pekkas@netcore.fi>
- spec file cleanups
- update to 0.7.0.

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- initial Red Hat Linux build

* Sun Jun 24 2001 Pekka Savola <pekkas@netcore.fi>
- add a patch from USAGI for overflow, Copyright -> License.

* Wed Jun 20 2001 Pekka Savola <pekkas@netcore.fi>
- use /sbin/service.
- update to 0.6.2pl4.

* Sat Apr 28 2001 Pekka Savola <pekkas@netcore.fi>
- update to 0.6.2pl3.

* Wed Apr 11 2001 Pekka Savola <pekkas@netcore.fi>
- update to 0.6.2pl2.

* Wed Apr  4 2001 Pekka Savola <pekkas@netcore.fi>
- update to 0.62pl1.  Bye bye patches!
- Require: initscripts (should really be with a version providing IPv6)
- clean up the init script, make condrestart work properly
- Use a static /etc/rc.d/init.d; init.d/radvd required it anyway.

* Sun Apr  1 2001 Pekka Savola <pekkas@netcore.fi>
- add patch to chroot (doesn't work well yet, as /proc is used directly)
- clean up droproot patch, drop the rights earlier; require user-writable
pidfile directory
- set up the pidfile directory at compile time.

* Sat Mar 31 2001 Pekka Savola <pekkas@netcore.fi>
- add select/kill signals patch from Nathan Lutchansky <lutchann@litech.org>.
- add address syntax checked fix from Marko Myllynen <myllynen@lut.fi>.
- add patch to check the pid file before fork.
- add support for OPTIONS sourced from /etc/sysconfig/radvd, provide a nice
default one.
- add/delete radvd user, change the pidfile to /var/run/radvd/radvd.pid.
- fix initscript NETWORKING_IPV6 check.

* Sun Mar 18 2001 Pekka Savola <pekkas@netcore.fi>
- add droproot patch, change to nobody by default (should use radvd:radvd or
the like, really).

* Mon Mar  5 2001 Tim Powers <timp@redhat.com>
- applied patch supplied by Pekka Savola in #30508
- made changes to initscript as per Pekka's suggestions

* Thu Feb 15 2001 Tim Powers <timp@redhat.com>
- needed -D_GNU_SOURCE to build properly

* Tue Feb  6 2001 Tim Powers <timp@redhat.com>
- use %%configure and %%makeinstall, just glob the manpages, cleans
  things up
- fixed initscript so that it can be internationalized in the future

* Fri Feb 2 2001 Pekka Savola <pekkas@netcore.fi>
- Create a single package(source) for glibc21 and glibc22 (automatic
Requires can handle this just fine).
- use %%{_mandir} and friends
- add more flesh to %%doc
- streamline %%config file %%attrs
- streamline init.d file a bit:
   * add a default chkconfig: (default to disable for security etc. reasons; 
     also, the default config isn't generic enough..)
   * add reload/condrestart
   * minor tweaks
   * missing: localization support (initscripts-5.60)
- use %%initdir macro

* Thu Feb 1 2001 Lars Fenneberg <lf@elemental.net>
- updated to new release 0.6.2

* Thu Feb 1 2001 Marko Myllynen <myllynen@lut.fi>
- initial version, radvd version 0.6.1
