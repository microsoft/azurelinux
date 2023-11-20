Summary:        The NIS daemon which binds NIS clients to an NIS domain
Name:           ypbind
Version:        2.7.2
Release:        11%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/thkukuk/ypbind-mt
Source0:        https://github.com/thkukuk/ypbind-mt/archive/v%{version}.tar.gz#/ypbind-mt-%{version}.tar.gz
#Source1: ypbind.init
Source2:        nis.sh
Source3:        ypbind.service
Source4:        ypbind-pre-setdomain
Source5:        ypbind-post-waitbind
# Fedora-specific patch. Renaming 'ypbind' package to proper
# 'ypbind-mt' would allow us to drop it.
Patch1:         ypbind-1.11-gettextdomain.patch
# Not sent to upstream.
Patch2:         ypbind-2.5-helpman.patch
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  dbus-glib-devel
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gettext-devel
BuildRequires:  libnsl2-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libxslt
BuildRequires:  make
BuildRequires:  systemd
BuildRequires:  systemd-devel
# New nss_nis package in F25+
Requires:       nss_nis
Requires:       rpcbind
Requires:       yp-tools >= 4.2.2-2
# This is for /bin/systemctl
Requires(post): systemd
Requires(postun): systemd
Requires(preun): systemd

%description
The Network Information Service (NIS) is a system that provides
network information (login names, passwords, home directories, group
information) to all of the machines on a network. NIS can allow users
to log in on any machine on the network, as long as the machine has
the NIS client programs running and the user's password is recorded in
the NIS passwd database. NIS was formerly known as Sun Yellow Pages
(YP).

This package provides the ypbind daemon. The ypbind daemon binds NIS
clients to an NIS domain. Ypbind must be running on any machines
running NIS client programs.

Install the ypbind package on any machines running NIS client programs
(included in the yp-tools package). If you need an NIS server, you
also need to install the ypserv package to a machine on your network.

%prep
%setup -q -n ypbind-mt-%{version}
%patch1 -p1 -b .gettextdomain
%patch2 -p1 -b .helpman

autoreconf -fiv

%build
%ifarch s390 s390x
export CFLAGS="%{optflags} -fPIC"
%else
export CFLAGS="%{optflags} -fpic"
%endif
export LDFLAGS="$LDFLAGS -pie -Wl,-z,relro,-z,now"

#export CFLAGS="$CFLAGS -H"

%configure
%make_build


%install
%make_install

mkdir -p %{buildroot}%{_localstatedir}/yp/binding
mkdir -p %{buildroot}%{_sysconfdir}/dhcp/dhclient.d
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_libexecdir}
install -m 644 etc/yp.conf %{buildroot}%{_sysconfdir}/yp.conf
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/dhcp/dhclient.d/nis.sh
install -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/ypbind.service
install -m 755 %{SOURCE4} %{buildroot}%{_libexecdir}/ypbind-pre-setdomain
install -m 755 %{SOURCE5} %{buildroot}%{_libexecdir}/ypbind-post-waitbind

%find_lang %{name}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files -f %{name}.lang
%license COPYING
%{_sbindir}/*
%{_mandir}/*/*
%{_libexecdir}/*
%{_unitdir}/*
%{_sysconfdir}/dhcp/dhclient.d/*
%config(noreplace) %{_sysconfdir}/yp.conf
%dir %{_localstatedir}/yp/binding
%doc README NEWS

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.7.2-11
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Aug 24 2022 Zhichun Wan <zhichunwan@microsoft.com> - 2.7.2-10
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Removed epoch
- License verified

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 3:2.7.2-7
- Rebuild(libnsl2)

* Tue Sep 28 2021 Marek Kulik <mkulik@redhat.com> - 3:2.7.2-6
- Fix setsebool message in logs, resolves: #1882069

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3:2.7.2-4
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 20 2020 Filip Januš <fjanus@redhat.com> - 2.7.2-1
- Update version to 2.7.2
- Resolves: #1796030
- Removing obsolete patches

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jul 30 2019 Matej Mužila <mmuzila@redhat.com> - 3:2.6.1-1
- Update to version 2.6.1
- Resolves: #1668439

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 07 2018 Matej Mužila <mmuzila@redhat.com> - 3:2.5-2
- Fix man pages

* Tue Jun 05 2018 Matej Mužila <mmuzila@redhat.com> - 3:2.5-1
- Update to version 2.5

* Mon Apr 30 2018 Petr Kubat <pkubat@redhat.com> - 3:2.4-8
- Add the runtime dependency on nss_nis back

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3:2.4-7
- Escape macros in %%changelog

* Tue Jan 16 2018 Petr Kubat <pkubat@redhat.com> - 3:2.4-6
- Temporarily remove nss_nis dependency as it got removed from glibc (#1534599)

* Thu Sep 21 2017 Matej Mužila <mmuzila@redhat.com> - 3:2.4-5
- Add "Wants" dependency on network-online.target
- Remove "After" dependency on NetworkManager-wait-online.service

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 29 2017 Matej Mužila <mmuzila@gmail.com> - 3:2.4-2
- Require yp-tools >= 4.2.2-2

* Fri May 19 2017 Matej Mužila <mmuzila@redhat.com> - 3:2.4-1
- Update to version 2.4 supporting IPv6

* Wed Mar 29 2017 Petr Kubat <pkubat@redhat.com> - 3:1.38-10
- Wait a while for dhcp to set up the domain (#1170400)

* Mon Mar 20 2017 Petr Kubat <pkubat@redhat.com> - 3:1.38-9
- Add a Wants dependency on nss-user-lookup.target (#1282440)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.38-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 23 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 3:1.38-7
- Remove check for libsystemd-daemon from ypbind-systemdso.patch (RHBZ#1396893).
- Add check for systemd/sd-daemon.h to ypbind-systemdso.patch.
- Spec file cosmetics.
- Add %%license tag.

* Mon Nov 07 2016 Petr Kubat <pkubat@redhat.com> - 3:1.38-6
- Add runtime dependency on nss_nis

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3:1.38-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Matej Muzila <mmuzila@redhat.com> 3:1.38-4
- Do not restart ypbind on dhcp renew if nis domain or nis servers
  haven't changed
  Resolves: rhbz#1301708

* Mon Nov 16 2015 Matej Muzila <mmuzila@redhat.com> 3:1.38-3
-  Load ypbind.service before nss-user-lookup.target
   Resolves: rhbz#1282440

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Oct 21 2014 Matej Mužila <mmuzila@redhat.com> - 3:1.38-1
- Update to 1.38

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.37.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Honza Horak <hhorak@redhat.com> - 3:1.37.2-2
- link with systemd.so

* Fri Aug 15 2014 Honza Horak <hhorak@redhat.com> - 3:1.37.2-1
- Update to 1.37.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.37.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 18 2013 Honza Horak <hhorak@redhat.com> - 3:1.37.1-9
- Replace autoreconf with autoconf

* Mon Nov 18 2013 Honza Horak <hhorak@redhat.com> - 3:1.37.1-8
- DHCP changes documented
  Related: #1031093

* Thu Aug 29 2013 Honza Horak <hhorak@redhat.com> - 3:1.37.1-7
- Add network-online.target dependency
  Resolves: #1002295

* Mon Aug 19 2013 Honza Horak <hhorak@redhat.com> - 3:1.37.1-6
- Improve systemd documentation

* Mon Jul 29 2013 Honza Horak <hhorak@redhat.com> - 3:1.37.1-5
- Remove SysV init conversion and systemd macros compatible code
- Require systemd instead systemd-units
- Remove systemd-sysv

* Thu May 09 2013 Honza Horak <hhorak@redhat.com> - 3:1.37.1-3
- Enable PrivateTmp feature, just for the case

* Tue May 07 2013 Honza Horak <hhorak@redhat.com> - 3:1.37.1-2
- Syncing help and man pages

* Mon May 06 2013 Honza Horak <hhorak@redhat.com> - 3:1.37.1-1
- Update to new version 1.37.1

* Tue Jan 29 2013 Honza Horak <hhorak@redhat.com> - 3:1.36-10
- Make re-bind interval a tune-able option
- Fixed bogus dates in changelog

* Wed Dec 19 2012 Honza Horak <hhorak@redhat.com> - 3:1.36-9
- Check presence of ypbind in /etc/rpc
  Related: #888778

* Fri Nov 30 2012 Honza Horak <hhorak@redhat.com> - 3:1.36-8
- Build with full relro

* Thu Oct 04 2012 Honza Horak <hhorak@redhat.com> - 3:1.36-7
- Run %%triggerun regardless of systemd_post variable definition

* Mon Sep 24 2012 Honza Horak <hhorak@redhat.com> - 3:1.36-6
- Use sdnotify to inform systemd that daemon is ready
- Minor spec file cleanup
- Use new systemd macros
  Resolves: #850375
- Add After: NetworkManager-wait-online.service
  Related: #846767

* Thu Aug 23 2012 Honza Horak <hhorak@redhat.com> - 3:1.36-5
- Enhance ypbind(8) with info about NISTIMEOUT
- Add suggestion about extending NISTIMEOUT if ypbind timeouts

* Mon Jul 23 2012 Honza Horak <hhorak@redhat.com> - 3:1.36-4
- Add SIGPIPE to proper signal set
  Related: #842228
- Fixed sending TERM signal in ypbind-post-waitbind

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.36-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Honza Horak <hhorak@redhat.com> - 3:1.36-2
- Minor spec file fixes
- Helper scripts moved to /usr/libexec

* Wed Jul 11 2012 Honza Horak <hhorak@redhat.com> - 3:1.36-1
- Update to new version 1.36

* Tue Jul 10 2012 Honza Horak <hhorak@redhat.com> - 3:1.35-5
- consider all 127.0.0.0/8 as localhost addresses
  Related: #829487

* Mon Jul 09 2012 Honza Horak <hhorak@redhat.com> - 3:1.35-4
- don't go offline when one of NIS servers is localhost
  Related: #829487

* Fri Jun 01 2012 Honza Horak <hhorak@redhat.com> - 3:1.35-3
- fixed kill call in ypbind-post-waitbind script

* Wed Apr 18 2012 Honza Horak <hhorak@redhat.com> - 3:1.35-2
- NetworkManager signal name changed
  Resolves: #812501

* Mon Mar 26 2012 Honza Horak <hhorak@redhat.com> - 3:1.35-1
- Update to new version with only minor changes

* Tue Jan 24 2012 Honza Horak <hhorak@redhat.com> - 3:1.33-11
- Don't fail when killing ypbind after unsuccessfull start fails
- Let ypbind start before systemd-user-sessions.service
  Resolves: #783447

* Thu Jan 12 2012 Honza Horak <hhorak@redhat.com> - 3:1.33-10
- Fail to start ypbind service if domainname is not set

* Wed Nov 16 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-9
- Fixed ypbind-post-waitbind to stop the service when binding is not success

* Tue Nov 15 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-8
- Fixed ypbind-post-waitbind to handle long rpcinfo requests
  Resolves: #624688

* Mon Sep 26 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-7
- Don't turn off allow_ypbind SELinux boolean
  Resolves: #741141

* Thu Sep 15 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-6
- Fixed systemd unit file
- Log messages when starting ypbind service made more verbose

* Tue Aug 02 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-5
- Fixed rpmlint errors
- Fixed systemd unit files packaging

* Mon Jun 13 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-4
- Changed -n option for staying in foreground to not overlap 
  with config-file option

* Tue Jun 07 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-3
- Fixed ypbind.service when selinux is disabled

* Tue May 10 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-2
- Added /etc/sysconfig/network to systemd service file

* Tue May 10 2011 Honza Horak <hhorak@redhat.com> - 3:1.33-1
- Update to new version

* Fri Apr 29 2011 Honza Horak <hhorak@redhat.com> - 3:1.32-11
- Removed NM_DBUS_VPN_SIGNAL_STATE_CHANGE, use own constant
  NM_DBUS_SIGNAL_STATE_CHANGED.
  (rhbz#696629)

* Thu Apr 28 2011 Honza Horak <hhorak@redhat.com> - 3:1.32-10
- Made EnvironmentFile in systemd definition optional
  (rhbz#632620)

* Thu Apr 14 2011 Honza Horak <hhorak@redhat.com> - 3:1.32-9
- Add native systemd unit file.
  (rhbz#693873)

* Thu Apr 14 2011 Honza Horak <hhorak@redhat.com> - 3:1.32-8
- Added rpcbind to LSB header in SysV init file.

* Wed Apr 06 2011 Honza Horak <hhorak@redhat.com> - 3:1.32-7
- Added LSB init service definition in ypbind.init.
- Fix D-Bus response codes to correspond with NetworkManager.
  (rhbz#693873)

* Fri Mar 18 2011 Honza Horak <hhorak@redhat.com> - 3:1.32-6
- Added the -typo2 patch which fixes a spelling error in a man pages.
  (rhbz#664870)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.32-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 29 2010 Karel Klic <kklic@redhat.com> - 3:1.32-4
- Added the -typo patch which fixes a spelling error in a message.

* Fri Nov 19 2010 Karel Klic <kklic@redhat.com> - 3:1.32-3
- ypbind.init: More effective syntax for #601296.

* Fri Nov 19 2010 Karel Klic <kklic@redhat.com> - 3:1.32-2
- Modified the chkconfig priorities from 27/73 to 24/76, to move
  ypbind before netfs. This is useful for hosts that mount NFS file
  systems that reside on a server which is resolvable through NIS.

* Thu Jul  8 2010 Karel Klic <kklic@redhat.com> - 3:1.32-1
- Update to new version which contains the -matches.patch

* Wed Jun 23 2010 Karel Klic <kklic@redhat.com> - 3:1.31-7
- Added -matches.patch removing matches when dereferencing
  DBus connection.

* Tue Jun  8 2010 Karel Klic <kklic@redhat.com> - 3:1.31-6
- ypbind.init: take the first domainname in yp.conf and use
  only that (rhbz#601296)

* Fri May 21 2010 Karel Klic <kklic@redhat.com> - 3:1.31-5
- Moved /sbin/ypbind to /usr/sbin/ypbind, as the package
  depends on several utilities from /usr (selinuxenabled,
  rpcinfo, ypwhich), and /usr/lib/libdbus-glib-1.so
- Removed trailing whitespaces from ChangeLog

* Wed May 19 2010 Karel Klic <kklic@redhat.com> - 3:1.31-4
- Update SELinux context of /etc/yp.conf in nis.sh (rhbz#593278)
- nis.sh: use condrestart instead of pidfile checking
- nis.sh: various simplifications
- Removed BuildRoot tag
- Removed %%clean section

* Wed Feb 24 2010 Karel Klic <kklic@redhat.com> - 3:1.31-3
- Added COPYING file to the package

* Thu Jan 21 2010 Karel Klic <kklic@redhat.com> - 3:1.31-2
- Rewrote initscript to become closer to Packaging:SysVInitScript
  Fedora guildeline. Also fixes rhbz#523913

* Mon Jan  4 2010 Karel Klic <kklic@redhat.com> - 3:1.31-1
- Updated to version 1.31 from upstream
- Removed signalstate patch because it was merged by upstream
- Removed man-port patch, because it was rejected by
  the upstream. Option '-p' does not work in all cases, it
  is not supported, intentionally not included in
  the documentation, and it is also removed from the usage
  string in this version

* Thu Nov 19 2009 Karel Klic <kklic@redhat.com> - 3:1.29.91-2
- Added signalstate patch, which fixes compilation with
  NetworkManaged-devel headers installed. Resolves #537064.

* Mon Oct 26 2009 Karel Klic <kklic@redhat.com> - 3:1.29.91-1
- Updated to 1.29.91 from upstream
- Removed 1.19-port-leak patch because the upstream source code has
  been changed and the port leaks should not happen anymore
- Removed 1.20.4-smartwrite patch because it was merged by upstream
- Removed 1.20.4-nm patch as the upstream merged the important part
- Removed 1.20.4-log-binds patch because it was merged by upstream
- Ported 1.20.4-man-port patch to the new release, sent to Thorsten Kukuk
- Removed 1.11-broadcast patch

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.20.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr  8 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-18
- Remove LSB Header from init script
  Resolves: #494827

* Wed Mar 18 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-17
- Fix nis.sh SELinux issue
  Resolves: #488865

* Thu Feb 26 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-16
- Fix ypbind script in dos format - bash syntax errors
  Resolves: #486722

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:1.20.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-14
- Update helper script for dhclient

* Mon Jan 26 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-13
- Fix ypbind can fail to bind if started soon after NetworkManager
  Resolves: #480096

* Mon Jan  5 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-12
- Ship helper script for dhclient

* Wed Dec  3 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-11
- Fix verbose option man page entry
- Add description of port option to man page
  Resolves: #474184

* Mon Nov 24 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-10
- Last few Merge Review related changes
- Fix init script arguments and return values
  Resolves: #247104, #467861

* Tue Oct 21 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-9
- Merge Review - remove dot from end of the summary, convert all tags
  in changelog to utf-8, escape %% character in changelog, fix
  requires and scriptlets, remove %%makeinstall, do not mark init
  script file as config, remove unused patches
  Resolves: #226663

* Tue Oct 21 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-8
- Rewrite binding files only when they are changed
  Resolves: #454581

* Mon Aug 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 3:1.20.4-7
- Fix license tag.

* Tue Jun 10 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-6
- Don't disable allow_ypbind SELinux boolean on service shutdown
  Resolves: #448240

* Wed May 21 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-5
- Fix init script timing again

* Tue Feb 12 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 3:1.20.4-4
- Fix Buildroot

* Fri Jan 11 2008 Steve Dickson <steved@redhat.com> - 3:1.20.4-3
- Fixed init script to wait for ypbind to come up. (bz 322101)

* Mon Sep 17 2007 Steve Dickson <steved@redhat.com> - 3:1.20.4-2
- Fixed a couple of typos in initscript (bz 281951)

* Thu May  3 2007 Steve Dickson <steved@redhat.com> - 3:1.20.4-1
- updated to latest upstream version ypbind-mt-1.20.4

* Tue Apr 17 2007 Steve Dickson <steved@redhat.com> - 3:1.19-9
- Fixed typo in init script (bz 233459)
- Changed init script to look in /etc/yp.conf for the
  domain name when not already set. (bz 113386)
- Reworked init script to eliminate unreasonable
  hangs when ypbind cannot bind to nis server. (bz 112770)

* Tue Apr  3 2007 Steve Dickson <steved@redhat.com> - 3:1.19-8
- Replace portmap dependency with an rpcbind dependency (bz 228894)

* Fri Dec  1 2006 Steve Dickson <steved@redhat.com> - 3:1.19-7
- Fixed leaking ports (bz 217874)
- Log all server bindings (bz 217782)
- Added better quoting to init script (bz 216739)

* Mon Nov 27 2006 Dan Walsh <dwalsh@redhat.com> - 3:1.19-6
- Correct ordering of turning off SELinux boolean

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> - 3:1.19-5
- Change init script to automatically turn on/off allow_ypbind boolean

* Wed Aug 23 2006 Steve Dickson <steved@redhat.com> - 3:1.19-4
- Remove the -s from install process making the -debuginfo
  package useful (bz 203851)
- Added the sourcing of /etc/sysconfig/ypbind (bz 199448)

* Fri Aug 11 2006 Steve Dickson <steved@redhat.com> - 3:1.19-2
- rebuild

* Tue Jul 25 2006 Steve Dickson <steved@redhat.com> - 3:1.19-0.3
- rebuild

* Tue Jul 18 2006 Steve Dickson <steved@redhat.com> - 3:1.19-0.2
- Added NISTIMEOUT variable to init scrip (bz 196078)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3:1.19-0.1
- rebuild

* Mon Feb 13 2006 Chris Feist <cfeist@redhat.com> - 3:1.19
- Build for latest version of ypbind-mt

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3:1.17.2-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3:1.17.2-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Jan 24 2005 Steve Dickson <SteveD@RedHat.com> 1.17.2-4
- Changed the initscript to use the logger command instead
  of initlog script, since the initlog script has gone away.

* Fri Oct 15 2004 Steve Dickson <SteveD@RedHat.com> 1.17.2-3
- Sped up the ypbind initscript by using fgrep
  instead of grep (bz# 81247)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Phil Knirsch <pknirsch@redhat.com> 1.17.2-1
- Another updated to latest upstream version.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 19 2004 Phil Knirsch <pknirsch@redhat.com> 1.16-1
- Updated to latest upstream version.

* Thu Nov 20 2003 Steve Dickson <SteveD@RedHat.com>
- Added a NULL check to test_bindings() to make sure
  clnt_call() is not called with a NULL pointer.

* Sat Oct  4 2003 Steve Dickson <SteveD@RedHat.com>
- Updated Release number for RHEL3 QU1

* Tue Sep  9 2003 Steve Dickson <SteveD@RedHat.com>
- Fixed a binding race where the wrong results were being returned.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Bill Nottingham <notting@redhat.com> 1.12-1.10
- make yp.conf %%config(noreplace)

* Thu Apr 24 2003 Steve Dickson <SteveD@RedHat.com>
- Updated to 1.12 from upstream.
- Removed ypbind-1.8-dos.patch since it
  was already commented out
- Updated broadcast patch

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Tim Powers <timp@redhat.com>
- build on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 11 2002 Alex Larsson <alexl@redhat.com> 1.11-1
- Updated to 1.11 from upstream.
- Removed patche that went in upstream.
- Updated broadcast patch

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Mar 25 2002 Alex Larsson <alexl@redhat.com> 1.10-7
- Get failure message right in init script (#37463 again)

* Mon Mar 25 2002 Alex Larsson <alexl@redhat.com> 1.10-6
- Fix bugs in initscript. Should fix #37463 and #61857

* Mon Mar 25 2002 Alex Larsson <alexl@redhat.com> 1.10-5
- New config patch that handles failing gethostbynames even better

* Thu Mar 21 2002 Alex Larsson <alexl@redhat.com> 1.10-4
- Added patch to avoid hanging if gethostbyname fails. (#56322)

* Sun Mar 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fixed #57393

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Nov 17 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to version 1.10

* Mon Aug 13 2001 Preston Brown <pbrown@redhat.com>
- eliminate potential DOS attack via ypwhich (#38637)
- install PO files

* Tue Jul 17 2001 Karsten Hopp <karsten@redhat.de>
- own /var/yp

* Fri Jun 29 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Mon Jun  4 2001 Preston Brown <pbrown@redhat.com>
- small fixes for initscript. Sometimes had trouble on slower systems (#37463)

* Sat Mar  3 2001 Preston Brown <pbrown@redhat.com>
- much more sane ypbind init script for when networking is down.

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- fix "usage" string (use $0)

* Wed Jan 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- prepare for initscript translation
- do not prereq /etc/init.d

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Start after netfs (#23526)

* Wed Nov 29 2000 Bill Nottingham <notting@redhat.com>
- set NIS domain name if it's not already set

* Mon Oct 02 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.7

* Thu Aug 31 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add again automatic fallback to broadcast

* Sun Aug 20 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- fix condrestart #16615
- security fix for syslog() call

* Sun Aug  6 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- do not include broadcast fallback until it is more tested

* Sun Aug  6 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- add automatic fallback to broadcast
- add "exit 0" to the scripts

* Wed Aug  2 2000 Bill Nottingham <notting@redhat.com>
- turn off broadcast; authconfig will enable this...
- put the pid that's actually listening to signals in the pidfile

* Thu Jul 20 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jul  7 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- prereq init.d

* Wed Jul  5 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- re-enable broadcasts

* Tue Jul  4 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix scripts

* Mon Jul  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- bump epoch

* Mon Jul  3 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- switch from ypbind to ypbind-mt
