# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: ipvsadm
Summary: Utility to administer the Linux Virtual Server
Version: 1.31
Release: 17%{?dist}
License: GPL-2.0-or-later
URL: https://kernel.org/pub/linux/utils/kernel/ipvsadm/

Source0: https://kernel.org/pub/linux/utils/kernel/ipvsadm/%{name}-%{version}.tar.gz
Source1: ipvsadm.service
Source2: ipvsadm-config

Patch0: 0003-ipvsadm-use-CFLAGS-and-LDFLAGS-environment-variables.patch

BuildRequires: gcc
Buildrequires: libnl3-devel
Buildrequires: popt-devel
BuildRequires: systemd
BuildRequires: make

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
ipvsadm is used to setup, maintain, and inspect the virtual server
table in the Linux kernel. The Linux Virtual Server can be used to
build scalable network services based on a cluster of two or more
nodes. The active node of the cluster redirects service requests to a
collection of server hosts that will actually perform the
services. Supported Features include:
  - two transport layer (layer-4) protocols (TCP and UDP)
  - three packet-forwarding methods (NAT, tunneling, and direct routing)
  - eight load balancing algorithms (round robin, weighted round robin,
    least-connection, weighted least-connection, locality-based
    least-connection, locality-based least-connection with
    replication, destination-hashing, and source-hashing)

%prep
%setup -q
%patch -P0 -p1

%build
%set_build_flags
%{__make}

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/rc.d/init.d
%{__make} install BUILD_ROOT=%{buildroot}%{_prefix} SBIN=%{buildroot}%{_sbindir} MANDIR=%{buildroot}%{_mandir} MAN=%{buildroot}%{_mandir}/man8 INIT=%{buildroot}%{_sysconfdir}/rc.d/init.d

%{__rm} -f %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -p -D -m 0600 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}-config

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc MAINTAINERS README
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}-config
%{_sbindir}/%{name}
%{_sbindir}/%{name}-restore
%{_sbindir}/%{name}-save
%{_mandir}/man8/%{name}.8*
%{_mandir}/man8/%{name}-restore.8*
%{_mandir}/man8/%{name}-save.8*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 04 2023 Ryan O'Hara <rohara@redhat.com> - 1.31-11
- Migrate to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.31-5
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 02 2020 Ryan O'Hara <rohara@redhat.com> - 1.31-1
- Update to 1.31 (#1726210)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Ryan O'Hara <rohara@redhat.com> - 1.29-8
- Use CFLAGS and LDFLAGS environment variables (#1543790)

* Fri Feb 23 2018 Ryan O'Hara <rohara@redhat.com> - 1.29-7
- Add %set_build_flags (#1543790)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Ryan O'Hara <rohara@redhat.com> - 1.29-5
- Catch the original errno from netlink answer (#1526813)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 29 2016 Ryan O'Hara <rohara@redhat.com> - 1.29-1
- Update to 1.29 (#1408437)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 09 2015 Ryan O'Hara <rohara@redhat.com> - 1.28-1
- Update to 1.28

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Ryan O'Hara <rohara@redhat.com> - 1.27-5
- Fix ipvsadm to show backup sync daemon

* Tue May 20 2014 Ryan O'Hara <rohara@redhat.com> - 1.27-4
- Fix compiler warnings

* Mon May 19 2014 Ryan O'Hara <rohara@redhat.com> - 1.27-3
- Update spec file and fix install paths

* Fri Nov 22 2013 Xose Vazquez Perez <xose.vazquez@gmail.com> - 1.27-2
- Link with libnl3

* Fri Sep 06 2013 Ryan O'Hara <rohara@redhat.com> - 1.27-1
- Update to 1.27

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Ryan O'Hara <rohara@redhat.com> - 1.26-8
- Use new systemd-rpm macros in ipvsadm spec file (#850168).

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul  9 2012 Ryan O'Hara <rohara@redhat.com> - 1.26-5
- Fix list_daemon to not assume sync daemon status is ordered (#805208).

* Thu Apr 19 2012 Jon Ciesla <limburgher@gmail.com> - 1.26-4
- Migrate to systemd, BZ 720175.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 11 2011 Matthias Saou <http://freshrpms.net/> 1.26-2
- Backport the init script from RHEL6, which contains lots of changes to make
  it behave simlarly to the iptables init script (#593276).

* Sat Jul  9 2011 Matthias Saou <http://freshrpms.net/> 1.26-1
- Update to 1.26 (#676167).
- Remove upstreamed Makefile and activeconns patchs, rebase popt patch.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 29 2010 Matthias Saou <http://freshrpms.net/> 1.25-5
- Include patch to fix activeconns when using the netlink interface (#573921).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 24 2008 Matthias Saou <http://freshrpms.net/> 1.25-2
- Fork the included init script to be (mostly) LSB compliant (#246955).

* Mon Dec 22 2008 Matthias Saou <http://freshrpms.net/> 1.25-1
- Prepare update to 1.25 for when devel will update to kernel 2.6.28.
- Build require libnl-devel and popt-devel (+ patch to fix popt detection).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Mon Oct 22 2007 Matthias Saou <http://freshrpms.net/> 1.24-10
- Update to latest upstream sources. Same filename, but updated content!
- Update kernhdr patch for it to still apply, update ip_vs.h from 1.2.0 to
  1.2.1 from kernel 2.6.23.1.

* Fri Aug 24 2007 Matthias Saou <http://freshrpms.net/> 1.24-9
- Spec file cleanup.
- Update License field.
- Don't "chkconfig --del" upon update.
- Add missing kernel-headers build requirement.
- Update URL and Source locations.
- Remove outdated piranha obsoletes, it has never been part of any Fedora.
- No longer mark init script as config.
- Include Makefile patch to prevent stripping and install init script.
- The init script could use a rewrite... leave that one for later.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.24-8.1
- rebuild

* Mon May 15 2006 Phil Knirsch <pknirsch@redhat.com> - 1.24-8
- Added missing prereq to chkconfig

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.24-7.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.24-7.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar 14 2005 Lon Hohberger <lhh@redhat.com> 1.24-7
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 16 2004 Mike McLean <mikem@redhat.com> 1.24-4.2.ipvs120
- bump release

* Tue Mar 02 2004 Mike McLean <mikem@redhat.com> 1.24-4.1.ipvs120
- update to new version for 2.6 kernel

* Thu Jan 08 2004 Mike McLean <mikem@redhat.com> 1.21-10.ipvs108
- fixing a minor bug/typo in output format processing

* Wed Aug 06 2003 Mike McLean <mikem@redhat.com> 1.21-9.ipvs108
- Dropping kernel-source BuildRequires and including a local copy of 
  net/ip_vs.h to compensate.
- Incorporating some upstream changes, most notably the --sort option.

* Fri Jun 13 2003 Mike McLean <mikem@redhat.com> 1.21-8
- dropping ppc from excluded arches

* Fri Apr 4 2003 Mike McLean <mikem@redhat.com> 1.21-7
- changing %%ExcludeArch

* Fri Apr 4 2003 Mike McLean <mikem@redhat.com> 1.21-6
- added BuildRequires: kernel-source
- escaped all %% characters in %%changelog

* Mon Dec 2 2002 Mike McLean <mikem@redhat.com> 1.21-5
- Improved the description in the ipvsadm initscript.
- fixed Buildroot to use _tmppath

* Wed Aug 21 2002 Philip Copeland <bryce@redhat.com> 1.21-4
- Argh,.. %%docdir was defined which overrode what I'd
  intended to happen

* Thu Aug 1 2002 Philip Copeland <bryce@redhat.com>
- Ah... the manuals were being pushed into /usr/man
  instead of /usr/share/man. Fixed.

* Tue Jul 16 2002 Philip Copeland <bryce@redhat.com>
- Minor Makefile tweak so that we do a minimal hunt for to find
  the ip_vs.h file location

* Sun Dec 16 2001 Wensong Zhang <wensong@linuxvirtualserver.org>
- Changed to install ipvsadm man pages according to the %%{_mandir}

* Sat Dec 30 2000 Wensong Zhang <wensong@linuxvirtualserver.org>
- update the %%file section

* Sun Dec 17 2000 Wensong Zhang <wensong@linuxvirtualserver.org>
- Added a if-condition to keep both new or old rpm utility building
  the package happily.

* Tue Dec 12 2000 P.opeland <bryce@redhat.com>
- Small modifications to make the compiler happy in RH7 and the Alpha
- Fixed the documentation file that got missed off in building
  the rpm
- Made a number of -pedantic mods though popt will not compile with
  -pedantic

* Wed Aug 9 2000 Horms <horms@vergenet.net>
- Removed Obseletes tag as ipvsadm is back in /sbin where it belongs 
  as it is more or less analogous to both route and ipchains both of
  which reside in /sbin.
- Create directory to install init script into. Init scripts won't install
  into build directory unless this is done

* Thu Jul  6 2000 Wensong Zhang <wensong@linuxvirtualserver.org>
- Changed to build rpms on the ipvsadm tar ball directly

* Wed Jun 21 2000 P.Copeland <copeland@redhat.com>
- fixed silly install permission settings

* Mon Jun 19 2000 P.Copeland <copeland@redhat.com>
- Added 'dist' and 'rpms' to the Makefile
- Added Obsoletes tag since there were early versions
  of ipvsadm-*.rpm that installed in /sbin
- Obsolete tag was a bit vicious re: piranha

* Mon Apr 10 2000 Horms <horms@vergenet.net>
- created for version 1.9

