# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without snmp
%bcond_without vrrp
%bcond_without sha1
%bcond_without json
%bcond_without nftables
%bcond_with profile
%bcond_with debug

%global _hardened_build 1

Name: keepalived
Summary: High Availability monitor built upon LVS, VRRP and service pollers
Version: 2.2.8
Release: 9%{?dist}
License: GPL-2.0-or-later
URL: http://www.keepalived.org/

Source0: http://www.keepalived.org/software/keepalived-%{version}.tar.gz
Source1: keepalived.service
#Patch0: keepalived-configure-c99.patch

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%if %{with snmp}
BuildRequires: net-snmp-devel
%endif
%if %{with nftables}
BuildRequires: libmnl-devel
BuildRequires: libnftnl-devel
%else
BuildRequires: ipset-devel
BuildRequires: iptables-devel
%endif
BuildRequires: gcc
BuildRequires: systemd-units
BuildRequires: systemd-devel
BuildRequires: openssl-devel
BuildRequires: libnl3-devel
BuildRequires: libnfnetlink-devel
BuildRequires: file-devel
BuildRequires: make

%description
Keepalived provides simple and robust facilities for load balancing
and high availability to Linux system and Linux based infrastructures.
The load balancing framework relies on well-known and widely used
Linux Virtual Server (IPVS) kernel module providing Layer4 load
balancing. Keepalived implements a set of checkers to dynamically and
adaptively maintain and manage load-balanced server pool according
their health. High availability is achieved by VRRP protocol. VRRP is
a fundamental brick for router failover. In addition, keepalived
implements a set of hooks to the VRRP finite state machine providing
low-level and high-speed protocol interactions. Keepalived frameworks
can be used independently or all together to provide resilient
infrastructures.

%prep
%autosetup -p1

# Prevent re-running autotools.
touch aclocal.m4 Makefile.in lib/config.h.in configure

%build
%configure \
    %{?with_debug:--enable-debug} \
    %{?with_profile:--enable-profile} \
    %{!?with_vrrp:--disable-vrrp} \
    %{?with_snmp:--enable-snmp --enable-snmp-rfc} \
    %{?with_nftables:--enable-nftables --disable-iptables} \
    %{?with_json:--enable-json} \
    %{?with_sha1:--enable-sha1} \
    --with-init=systemd
%{__make} %{?_smp_mflags} STRIP=/bin/true

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_initrddir}/
rm -rf %{buildroot}%{_sysconfdir}/keepalived/samples/
mv %{buildroot}%{_sysconfdir}/keepalived/keepalived.conf.sample \
   %{buildroot}%{_sysconfdir}/keepalived/keepalived.conf
%{__install} -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/keepalived.service
mkdir -p %{buildroot}%{_libexecdir}/keepalived

%post
%systemd_post keepalived.service

%preun
%systemd_preun keepalived.service

%postun
%systemd_postun_with_restart keepalived.service

%files
%attr(0755,root,root) %{_sbindir}/keepalived
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/sysconfig/keepalived
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/keepalived/keepalived.conf
%doc AUTHOR ChangeLog CONTRIBUTORS COPYING README TODO
%doc doc/keepalived.conf.SYNOPSIS doc/samples/keepalived.conf.*
%dir %{_sysconfdir}/keepalived/
%dir %{_libexecdir}/keepalived/
%if %{with snmp}
%{_datadir}/snmp/mibs/KEEPALIVED-MIB.txt
%{_datadir}/snmp/mibs/VRRP-MIB.txt
%{_datadir}/snmp/mibs/VRRPv3-MIB.txt
%endif
%{_bindir}/genhash
%{_unitdir}/keepalived.service
%{_mandir}/man1/genhash.1*
%{_mandir}/man5/keepalived.conf.5*
%{_mandir}/man8/keepalived.8*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 04 2023 Ryan O'Hara <rohara@redhat.com> - 2.2.8-3
- Migrate to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Ryan O'Hara <rohara@redhat.com> - 2.2.8-1
- Update to 2.2.8 (#2211385)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Ryan O'Hara <rohara@redhat.com> - 2.2.7-5
- Enable JSON support

* Wed Dec  7 2022 Florian Weimer <fweimer@redhat.com> - 2.2.7-4
- Fix spurious implicit function declaration in broken configure check

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Ryan O'Hara <rohara@redhat.com> - 2.2.7-2
- Move keepalived.conf.sample to keepalived.conf

* Mon Feb 14 2022 Ryan O'Hara <rohara@redhat.com> - 2.2.7-1
- Update to 2.2.7 (#2041231)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.4-4
- Fix dbus policy (#2027158, CVE-2021-44225)

* Sat Nov 27 2021 Kevin Fenzi <kevin@scrye.com> - 2.2.4-3
- Rebuild for new libnftnl

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.2.4-2
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 23 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.4-1
- Update to 2.2.4 (#1996274)

* Sat Aug 14 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.3-1
- Update to 2.2.3 (#1993601)

* Tue Aug 03 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.2-5
- Add systemd notify support

* Tue Aug 03 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.2-4
- Fix build errors (#1987620)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 12 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.2-2
- Add BuildRequires for file-devel

* Wed Apr 07 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.2-1
- Update to 2.2.2 (#1935590)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2.1-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 18 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.1-1
- Update to 2.2.1 (#1917152)

* Thu Jan 14 2021 Ryan O'Hara <rohara@redhat.com> - 2.2.0-1
- Update to 2.2.0 (#1914512)

* Thu Aug 27 2020 Josef Řídký <jridky@redhat.com> - 2.1.5-3
- Rebuilt for new net-snmp release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Ryan O'Hara <rohara@redhat.com> - 2.1.5-1
- Update to 2.1.5 (#1794135)

* Tue Feb 18 2020 Ryan O'Hara <rohara@redhat.com> - 2.0.20-3
- Build with nftables support instead of iptables

* Thu Feb 13 2020 Ryan O'Hara <rohara@redhat.com> - 2.0.20-2
- Remove unused patches

* Wed Feb 12 2020 Ryan O'Hara <rohara@redhat.com> - 2.0.20-1
- Update to 2.0.20 (#1794135)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 12 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.19-4
- Fix file descriptor errors on reload

* Tue Nov 12 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.19-3
- Fix track_process with PIDs over 32767 (#1770766)

* Wed Nov 06 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.19-2
- Enable nftables support (#1769278)

* Wed Nov 06 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.19-1
- Update to 2.0.19 (#1763424)

* Tue Jul 30 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.18-2
- Change pidfile directory (#1712730)

* Tue Jul 30 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.18-1
- Update to 2.0.18 (#1678397)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Björn Esser <besser82@fedoraproject.org> - 2.0.12-2
- Rebuilt (iptables)

* Mon Feb 04 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.12-1
- Update to 2.0.12 (#1576138)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.11-1
- Update to 2.0.11

* Mon Nov 26 2018 Ryan O'Hara <rohara@redhat.com> - 2.0.10-1
- Update to 2.0.10
- Fix improper pathname validation (#1651864, CVE-2018-19044)
- Fix insecure permissions when creating temporary files (#1651868, CVE-2018-19045)
- Fix insecure use of temporary files (#1651870, CVE-2018-19046)
- Fix buffer overflow when parsing HTTP status codes (#1651873, CVE-2018-19047)

* Wed Jul 25 2018 Ryan O'Hara <rohara@redhat.com> - 2.0.6-1
- Update to 2.0.6 (#1576138)

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 2.0.5-3
- Rebuild for new net-snmp

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Ryan O'Hara <rohara@redhat.com> - 2.0.5-1
- Update to 2.0.5 (#1576138)

* Mon Jul 02 2018 Ryan O'Hara <rohara@redhat.com> - 1.4.5-1
- Update to 1.4.5

* Thu May 10 2018 Ryan O'Hara <rohara@redhat.com> - 1.4.4-1
- Update to 1.4.4 (#1576138)

* Thu Apr 19 2018 Ryan O'Hara <rohara@redhat.com> - 1.4.3-1
- Update to 1.4.3 (#1565388)

* Wed Mar 07 2018 Ryan O'Hara <rohara@redhat.com> - 1.4.2-1
- Update to 1.4.2 (#1539269)

* Mon Jan 29 2018 Ryan O'Hara <rohara@redhat.com> - 1.4.1-1
- Update to 1.4.1 (#1539269)

* Fri Jan 05 2018 Ryan O'Hara <rohara@redhat.com> - 1.4.0-1
- Update to 1.4.0 (#1529802)

* Wed Oct 25 2017 Ryan O'Hara <rohara@redhat.com> - 1.3.9-1
- Update to 1.3.9 (#1497576)

* Mon Sep 11 2017 Ryan O'Hara <rohara@redhat.com> - 1.3.6-1
- Update to 1.3.6 (#1481471)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 Ryan O'Hara <rohara@redhat.com> - 1.3.5-1
- Update to 1.3.5 (#1422063)

* Sun Feb 05 2017 Kalev Lember <klember@redhat.com> - 1.3.2-2
- Rebuilt for libxtables soname bump

* Mon Nov 28 2016 Ryan O'Hara <rohara@redhat.com> - 1.3.2-1
- Update to 1.3.2 (#1396857)

* Fri Sep 16 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.24-3
- Add BuildRequires for iptables-devel (#1361686)

* Fri Sep 16 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.24-2
- Fix configure script

* Thu Sep 15 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.24-1
- Update to 1.2.24 (#1376254)

* Wed Jul 13 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.23-1
- Update to 1.2.23 (#1354696)

* Wed Jun 15 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.22-1
- Update to 1.2.22 (#1346509)

* Tue Jun 14 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.21-3
- Remove net-snmp U64 typedef

* Fri Jun 03 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.21-2
- Remove unnecessary BuildRequires (#1327873)

* Fri Jun 03 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.21-1
- Update to 1.2.21 (#1341372)

* Sun Apr 10 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.20-2
- Install VRRP MIB

* Mon Apr 04 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.20-1
- Update to 1.2.20 (#1323526)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Ryan O'Hara <rohara@redhat.com> - 1.2.19-3
- Add PIDFile to systemd unit file (#1280437)

* Wed Jul 29 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.2.19-2
- Rebuilt for rpm 4.12.90

* Wed Jul 15 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.19-1
- Update to 1.2.19 (#1240863)

* Wed Jul 01 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.18-1
- Update to 1.2.18 (#1237377)

* Tue Jun 23 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.17-5
- Revert patch that changed VRRP notify scripts to list (#1232073)

* Wed Jun 17 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.17-4
- Fix multiple VRRP instances with same interface (#1232408)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 01 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.17-2
- Add VRRP MIB file

* Mon Jun 01 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.17-1
- Update to 1.2.17

* Wed Apr 01 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.16-1
- Update to 1.2.16

* Wed Mar 18 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.15-3
- Revert previous preempt extension (#1202584)

* Tue Jan 13 2015 Ryan O'Hara <rohara@redhat.com> - 1.2.15-2
- Depend on network-online.target systemd unit (#1181097)

* Tue Dec 23 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.15-1
- Update to 1.2.15

* Tue Dec 16 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.14-1
- Update to 1.2.14

* Tue Oct 28 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.13-4
- Create /usr/libexec/keepalived directory (#1158113)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.13-1
- Update to 1.2.13

* Mon Feb 10 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.12-1
- Update to 1.2.12

* Mon Feb 03 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.11-1
- Update to 1.2.11

* Mon Jan 13 2014 Ryan O'Hara <rohara@redhat.com> - 1.2.10-1
- Update to 1.2.10

* Mon Nov 11 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.9-1
- Update to 1.2.9.

* Thu Sep 19 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.8-2
- Bump release and rebuild.

* Thu Sep 05 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.8-1
- Update to 1.2.8.

* Mon Aug 19 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.7-10
- Add To header for SMTP alerts (#967641)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.7-8
- Fix macro in keepalived.conf.5 man page.

* Mon Jul 22 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.7-7
- Fix systemd requirements.

* Mon Jul 22 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.7-6
- Install the systemd unit file, not the init script.

* Mon Apr 22 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.7-5
- Build with PIE flags (#955150)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 2 2013 Ryan O'Hara <rohara@redhat.com> - 1.2.7-3
- Update spec file.
- Add option to prevent respawn of child processes.
- Remove duplicate command-line option code.
- Use popt to generate usage message.
- Fix pointer arithmetic for VRRP packets.
- Fix comparison of primary IP address.
- Fix loading of SSL certificate.
- Fix typo in error message.
- Update FSF address in GPLv2 license.
- Remove debug message from if_get_by_ifname.

* Mon Sep 24 2012 Václav Pavlín <vpavlin@redhat.com> - 1.2.7-2
- Scriptlets replaced with new systemd macros (#850173).

* Tue Sep 04 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.7-1
- Update to 1.2.7.
- Fix systemd service file (#769726).

* Mon Aug 20 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.6-1
- Update to 1.2.6.

* Tue Aug 14 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.5-2
- Install KEEPALIVED-MIB as KEEPALIVED-MIB.txt.

* Mon Aug 13 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.5-1
- Update to 1.2.5.

* Wed Aug 01 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.4-1
- Update to 1.2.4.

* Mon Jul 23 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.3-1
- Update to 1.2.3.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Ryan O'Hara <rohara@redhat.com> - 1.2.2-5
- Fix IPv4 address comparison (#768119).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 19 2011 Tom Callaway <spot@fedoraproject.org> - 1.2.2-3
- convert to systemd
- fix ip_vs.h path searching in configure

* Tue Jul 12 2011 Matthias Saou <http://freshrpms.net/> 1.2.2-2
- Build against libnl for Fedora. RHEL's libnl is too old.

* Sat May 21 2011 Matthias Saou <http://freshrpms.net/> 1.2.2-1
- Update to 1.2.2.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 16 2011 Dan Horák <dan[at]danny.cz> 1.1.20-2
- exclude arches where we don't provide 32-bit kernel

* Tue Jan 11 2011 Matthias Saou <http://freshrpms.net/> 1.2.1-1
- Update to 1.2.1, now with IPv6 support.

* Sun May 23 2010 Matthias Saou <http://freshrpms.net/> 1.1.20-1
- Update to 1.1.20 (#589923).
- Update BR conditional for RHEL6.
- No longer include goodies/arpreset.pl, it's gone from the sources.

* Tue Dec  8 2009 Matthias Saou <http://freshrpms.net/> 1.1.19-3
- Update init script to have keepalived start after the local MTA (#526512).
- Simplify the kernel source detection, to avoid running rpm from rpmbuild.

* Tue Nov 24 2009 Matthias Saou <http://freshrpms.net/> 1.1.19-2
- Include patch to remove obsolete -k option to modprobe (#528465).

* Wed Oct 21 2009 Matthias Saou <http://freshrpms.net/> 1.1.19-1
- Update to 1.1.19.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.17-3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Matthias Saou <http://freshrpms.net/> 1.1.17-1
- Update to 1.1.17.
- Update init script all the way.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 1.1.15-7
- rebuild with new openssl

* Mon Dec 22 2008 Matthias Saou <http://freshrpms.net/> 1.1.15-6
- Fork the init script to be (mostly for now) LSB compliant (#246966).

* Thu Apr 24 2008 Matthias Saou <http://freshrpms.net/> 1.1.15-5
- Add glob to the kerneldir location, since it contains the arch for F9+.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org>
- Rebuild for deps

* Mon Oct 22 2007 Matthias Saou <http://freshrpms.net/> 1.1.15-2
- Update to latest upstream sources, identical except for the included spec.

* Mon Sep 17 2007 Matthias Saou <http://freshrpms.net/> 1.1.15-1
- Update to 1.1.15.
- Remove merged genhashman and include patches.

* Fri Sep 14 2007 Matthias Saou <http://freshrpms.net/> 1.1.14-2
- Include patch from Shinji Tanaka to fix conf include from inside some
  directives like vrrp_instance.

* Thu Sep 13 2007 Matthias Saou <http://freshrpms.net/> 1.1.14-1
- Update to 1.1.14.
- Remove all upstreamed patches.
- Remove our init script and sysconfig files, use the same now provided by the
  upstream package (will need to patch for LSB stuff soonish).
- Include new goodies/arpreset.pl in %%doc.
- Add missing scriplet requirements.

* Wed Aug 22 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-8
- Rebuild for new BuildID feature.

* Sun Aug  5 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-7
- Update License field.

* Mon Mar 26 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-6
- Fix doc/samples/sample.misccheck.smbcheck.sh mode (600 -> 644).

* Thu Mar 22 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-5
- Include types patch to fix compile on F7 (David Woodhouse).
- Fix up file modes (main binary 700 -> 755 and config 600 -> 640).

* Tue Feb 13 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-4
- Add missing \n to the kernel define, for when multiple kernels are installed.
- Pass STRIP=/bin/true to "make" in order to get a useful debuginfo package.

* Tue Feb 13 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-3
- Add %%check section to make sure any build without LVS support will fail.

* Mon Feb  5 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-2
- Use our own init script, include a sysconfig entry used by it for options.

* Thu Jan 25 2007 Matthias Saou <http://freshrpms.net/> 1.1.13-1
- Update to 1.1.13.
- Change mode of configuration file to 0600.
- Don't include all of "doc" since it meant re-including all man pages.
- Don't include samples in the main configuration path, they're in %%doc.
- Include patch to add an optional label to interfaces.

* Sat Apr 08 2006 Dries Verachtert <dries@ulyssis.org> - 1.1.12-1.2
- Rebuild for Fedora Core 5.

* Sun Mar 12 2006 Dag Wieers <dag@wieers.com> - 1.1.12-1
- Updated to release 1.1.12.

* Fri Mar 04 2005 Dag Wieers <dag@wieers.com> - 1.1.11-1
- Updated to release 1.1.11.

* Wed Feb 23 2005 Dag Wieers <dag@wieers.com> - 1.1.10-2
- Fixed IPVS/LVS support. (Joe Sauer)

* Tue Feb 15 2005 Dag Wieers <dag@wieers.com> - 1.1.10-1
- Updated to release 1.1.10.

* Mon Feb 07 2005 Dag Wieers <dag@wieers.com> - 1.1.9-1
- Updated to release 1.1.9.

* Sun Oct 17 2004 Dag Wieers <dag@wieers.com> - 1.1.7-2
- Fixes to build with kernel IPVS support. (Tim Verhoeven)

* Fri Sep 24 2004 Dag Wieers <dag@wieers.com> - 1.1.7-1
- Updated to release 1.1.7. (Mathieu Lubrano)

* Mon Feb 23 2004 Dag Wieers <dag@wieers.com> - 1.1.6-0
- Updated to release 1.1.6.

* Mon Jan 26 2004 Dag Wieers <dag@wieers.com> - 1.1.5-0
- Updated to release 1.1.5.

* Mon Dec 29 2003 Dag Wieers <dag@wieers.com> - 1.1.4-0
- Updated to release 1.1.4.

* Fri Jun 06 2003 Dag Wieers <dag@wieers.com> - 1.0.3-0
- Initial package. (using DAR)

