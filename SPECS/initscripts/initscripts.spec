Summary:        Scripts to bring up network interfaces and legacy utilities
Name:           initscripts
Version:        10.19
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/fedora-sysv/initscripts
Source0:        https://github.com/fedora-sysv/initscripts/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gettext
BuildRequires:  glib-devel
BuildRequires:  pkg-config
BuildRequires:  popt-devel
BuildRequires:  python3
BuildRequires:  systemd
Requires:       dbus
Requires:       iproute
Requires:       systemd
Provides:       /sbin/service
Provides:       network-scripts = %{version}-%{release}

%description
This package contains the script that activates and deactivates most
network interfaces, some utilities, and other legacy files.

%prep
%setup -q

%build
%make_build PYTHON=%{__python3}

%install
%make_install

# This installs the NLS language files:
%find_lang %{name}

%ifnarch s390 s390x
  rm -f %{buildroot}%{_sysconfdir}/sysconfig/network-scripts/ifup-ctc
%endif

# Additional ways to access documentation:
install -m 0755 -d %{buildroot}%{_docdir}/network-scripts

ln -s  %{_docdir}/%{name}/sysconfig.txt %{buildroot}%{_docdir}/network-scripts/
ln -sr %{_mandir}/man8/ifup.8           %{buildroot}%{_mandir}/man8/ifdown.8

# We are now using alternatives approach to better co-exist with NetworkManager:
touch %{buildroot}%{_sbindir}/ifup
touch %{buildroot}%{_sbindir}/ifdown

%post
%systemd_post import-state.service loadmodules.service

%preun
%systemd_preun import-state.service loadmodules.service

%postun
%systemd_postun import-state.service loadmodules.service

%files -f %{name}.lang
%license COPYING
%doc doc/sysconfig.txt
%dir %{_sysconfdir}/rc.d
%dir %{_sysconfdir}/rc.d/init.d
%dir %{_sysconfdir}/rc.d/rc[0-6].d
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/legacy-actions
%{_sysconfdir}/rc.d/init.d/functions
# RC symlinks:
%{_sysconfdir}/rc[0-6].d
%{_sysconfdir}/init.d
%{_bindir}/*
%{_sbindir}/consoletype
%{_sbindir}/genhostid
%{_libexecdir}/import-state
%{_libexecdir}/loadmodules
%{_prefix}/lib/systemd/system/import-state.service
%{_prefix}/lib/systemd/system/loadmodules.service
%{_prefix}/lib/udev/rename_device
%{_udevrulesdir}/*
%{_mandir}/man1/*
%{_sbindir}/service
%{_mandir}/man8/service.*
%doc doc/examples/
%dir %{_sysconfdir}/sysconfig/network-scripts
%{_sysconfdir}/rc.d/init.d/network
%{_sysconfdir}/sysconfig/network-scripts/*
%ghost                %{_sbindir}/ifup
%ghost                %{_sbindir}/ifdown
%attr(4755,root,root) %{_sbindir}/usernetctl
%{_mandir}/man8/ifup.*
%{_mandir}/man8/ifdown.*
%{_mandir}/man8/usernetctl.*
%{_docdir}/network-scripts/*
%config(noreplace) %{_sysconfdir}/sysconfig/netconsole
%{_libexecdir}/netconsole
%{_prefix}/lib/systemd/system/netconsole.service
%dir %{_sharedstatedir}/stateless
%dir %{_sharedstatedir}/stateless/state
%dir %{_sharedstatedir}/stateless/writable
%config(noreplace) %{_sysconfdir}/rwtab
%config(noreplace) %{_sysconfdir}/statetab
%config(noreplace) %{_sysconfdir}/sysconfig/readonly-root
%{_libexecdir}/readonly-root
%{_prefix}/lib/systemd/system/readonly-root.service

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 10.19-1
- Auto-upgrade to 10.19 - Azure Linux 3.0 - package upgrades

* Tue Feb 22 2022 Cameron Baird <cameronbaird@microsoft.com> - 10.15-1
- Update source to v10.15
- Use python3 to build

* Mon Mar 29 2021 Henry Li <lihl@microsoft.com> - 9.70-8
- Replace incorrect %%{_lib} usage with %%{_libdir}.

* Tue Mar 23 2021 Henry Li <lihl@microsoft.com> - 9.70-7
- Add provides for network-scripts.

* Mon Apr 27 2020 Emre Girgin <mrgirgin@microsoft.com> 9.70-6
- Rename iproute2 to iproute.

* Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 9.70-5
- Verified license. Removed sha1. Fixed download URL. Fixed formatting.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 9.70-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sat Jan 05 2019 Ankit Jain <ankitja@vmware.com> 9.70-3
- Added network configuration to fix "service --status-all"

* Tue Dec 26 2017 Divya Thaluru <dthaluru@vmware.com> 9.70-2
- Fixed return code in /etc/init.d/functions bash script

* Mon Apr 3 2017 Dheeraj Shetty <dheerajs@vmware.com> 9.70-1
- Updated to version 9.70

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.65-2
- GA - Bump release of all rpms

* Fri Feb 12 2016 Divya Thaluru <dthaluru@vmware.com> 9.65-2
- Fixing service script to start services using systemctl by default

* Tue Jan 26 2016 Xiaolin Li <xiaolinl@vmware.com> 9.65-1
- Updated to version 9.65

* Mon Jul 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.63-1
- Got Spec file from source tar ball and modified it to be compatible to build in Photon

* Mon May 18 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 9.63-1
- remove ipcalc, it has its own package now
- network: tell NM to reload its configuration during start
- bonding: warn if the ifup for slave device failed
- sysctl.conf: drop SHMALL and SHMMAX, they have sane default values in kernel
- ifup: don't call NM for loopback
- clarify daemon() usage message
- rename_device: allow non-channel nics for s390x machines
- ifup: add missing quotes

* Thu Apr 09 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 9.62-1
- network-functions: fix change_resolv_conf after grep update
- ifup-aliases: don't return with error when arping fails
- init.d/functions: rc.debug option to debug initscripts
- ifup-aliases: inherit ARPCHECK from parent device
- network: report that we can't shut down network for root on netfs
- ifdown-eth: use scope host for lo

* Thu Jan 22 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 9.61-1
- specfile cleanup
- ifup-ipv6: set accept_ra to 2 when IPV6FORWARDING=yes and IPV6_AUTOCONF=yes
- ifup-post: check resolve.conf also with DNS2
- ifup-aliases: do not fail when only ipv6 addr is specified
- fedora-import-state.service: run a little bit later
- fedora-readonly: Updates for systemd random-seed handling
- network-functions: is_available_wait should wait even in the case that is_available returns 2
- ifdown-post: remove resolv.conf only in specific cases
- network-functions: fix check in install_bonding_driver

* Tue Dec 16 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.60-1
- improve check for bond master in install bonding driver
- network-functions: reeplace iwconfig with iw
- ifup: fix typo
- ifdown-ipv6: reset addrgenmode to eui64 for device

* Wed Nov 12 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.59-1
- adjust LINKDELAY when STP is on

* Thu Nov 06 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.58-1
- ifup,vlan: fix typo
- doc: be consistent and use BOOTPROTO=none

* Tue Oct 07 2014 Zbigniew Jędrzejewski-Szmek - 9.57
- Remove /etc/inittab, /etc/crypttab, utmp, wtmp, btmp

* Tue Oct 07 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.56-1
- network_function: return immediately when device is pres
ent
- add configurable DEVTIMEOUT
- fedora-import-state: do not clobber /
- network-functions: grep->fgrep in bonding masters matchi
ng
- man: update sys-unconfig.8
- rename_devices: comments need to have a blank before them
- add example ifcfg files
- network-functions: improve bonding_masters grep
- ifup: if we were unable to determine DEVICE always call nmcli up
- ifup-tunnel: call ifup-ipv6 in the end
- ifup: also set multicast_snooping after the bridge is up
- network-functions: ETHTOOL_DELAY introduction patch
- use pie and relro by default
- custom naming for VLAN devices
- vi.po: fix parentheses
- ifup-wireless: add support for wowlan
- ifup-wireless: add support for wowlan (second part)
- ifup-aliases: do not bring up ipv6 for range files
- sys-unconfig: use poweroff instead of halt
- ifup-aliases: improve duplicate address detection
- network-functions: handle BONDING_OPTS better
- network: tell nm to wake the slaves

* Tue Jul 22 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.55-1
- fix license handling
- ipcalc: -c allow netmask
- ipcalc: parse prefix more safely
- inittab: fix path and mention set-default
- don't require /sbin/sysctl
- init.d/functions: check parent dir of pid file for accessibility
- ifup-eth: some options for bridge can be applied after the bridge is up
- remove ppp from translation

* Tue Apr 15 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.54-1
- move ppp support to ppp package
- remove fedora-configure
- network: detect if / is on netfs
- is_nm_handling: fix RE
- bonding: match whole name of interface
- network: add support for team devices
- ifup-wireless: fix syntax error
- fedora-readonly: fix prefix detection

* Wed Mar 26 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.53-1
- bridging: add possibility to set prio and ageing
- ifup: add possibility to specify value for -w parameter of arping
- network: try to not compete with NM during boot
- fedora-domainname: DefaultDependencies=no
- service: add condrestart to allowed commands
- update ifup/ifdown NetworkManager interaction once more(#1036701, #1061810)
- network: modify ifup-wireless so it doesn't call exit
- set shmmax and shmall defaults to match rhel6 values (#1056547)
- update ifup/ifdown NetworkManager interaction (#1036701, #1061810)
- service: fix action matching
- remove ifup-ipx from spec
- Delete IPX support.
- remove dependency on sysvinit-tools

* Tue Jan 14 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 9.52-1
- require procps-ng

* Tue Jan 14 2014 Lukáš Nykrýn <lnykryn@redhat.com> 9.51-1
- readonly-root: bind-mount only necessary subset of entries in rwtab
- readonly-root: Add /var/log/audit/audit.log to rwtab
- readonly-root: restore selinux context after bind mount
- rename_device: remove comments and trailing whitespaces
- service: suggest using systemctl if unknown action is used
- ifup-eth: fix typo in error message
- use iw instead of iwconfig and friends
- update functions who call nmcli
- ifdown: fix typo in nmcli call

* Tue Sep 03 2013 Lukas Nykryn <lnykryn@redhat.com> - 9.50-1
- ipcalc: support RFC3021 (#997271)
- symlink /etc/sysctl.conf -> /etc/sysctl.d/
- man: only action specified in LSB are redirected to systemd
- service: filter actions that are not supported by systemctl in service (#947823)
- install_bonding_driver: drop check for existing device (#991335)
- consider IPV6INIT undefined as YES
- don't care about network filesystems

* Fri Jul 12 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 9.48-1
- man: add systemd man pages to service.8 "see also" section
- add possibility to set domainname through /etc/sysconfig/network
- rename_device: don't wait for lock with lower permissions
- 256term.csh: remove quotes around variable (#979796)
- drop useless variables from /etc/sysconfig/init
- readonly-root: rpcidmapd restart is not needed anymore
- ifup-eth: print error only if arping is really called (#974603)
- readonly-root: Add /var/lib/samba to rwtab

* Fri May 31 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 9.47-1
- network-functions: to determine state of nscd check socket not lock (#960779)
- sysconfig.txt advised saslauthd -a instad of -v
- update translations from transifex
- drop translation for other initscripts
- tweak ifup/ifdown usage and man page (#961917)
- ctrl-alt-delete.target is provided by systemd package
- remove some defaults from arch specific sysctl.conf
- readonly-root: remount rpc_pipefs if readonly-root is used
- service: mention legacy actions and systemctl redirection in man page

* Fri Apr 12 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 9.46-1
- add /var/lib/NetworkManager
- add ipip6 tunneling support (#928232, raorn@raorn.name)
- bonding: set master up before slaves
- set net.ipv6.conf.SYSCTLDEVICE.autoconf in ifup-ipv6
- ifdown: don't call nmcli on interface that is alread down
- remove some defaults from sysctl.conf (move to systemd)
- call flush addresses with scope global
- service: action should not be empty when calling legacy-actions (#947817)
- ifup-eth: ignore arping errors (#928379)
- replace tunctl with ip tuntap (#947875)
- reload sysctl settings for vlans on ifup
- try dhcpv6 after v4 failed (#846618)

* Fri Mar 15 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 9.45-2
- provides /sbin/service

* Fri Mar 15 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 9.45-1
- turn on symlink protections in sysctl (#922030)
- add systemd-random-seed.service to  Before= in fedora-readonly.service (#888615)
- mention rule6 files in sysconfig.txt
- skip nmcli for wireless device (#863707)
- remove config-noreplace from /etc/inittab (#627474)
- remount-rootfs.service got renamed to systemd-remount-fs.service
- compile netreport and usernetctl with full RELRO and PIE (#853178)
- move stuff directly to /usr (#905492)
- Remove NETWORKING_IPV6 from sysconfig.txt (#918622)
- fix greps to correctly handle comments and quotation

* Wed Feb 20 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 9.44-1
- limit udev rule for network renaming (#907365, mschmidt@redhat.com)
- fix path for arpwatch, seems to be in /var/lib on Fedora 18
- fix the path for lvm cache, there is no file /etc/lvm/.cache ( but there is one /etc/lvm/cache )
- fix path for dhcpd, is /var/lib/dhcpd since 2005 ( see 31cdb58df77 on the dhcp package git )
- fix the patch for apache modules in rwtab, that are now in /var/cache/httpd
- remove no longer used directory ( at least in Fedora ), hald is deprecated,
  /var/tux cannot be found and xend seems to use a subdirectory of /var/lib/xen
- correct the path for puppet directory in /etc/rwtab, now use /var/lib/puppet by default
- allow passing -F from /.autorelabel to fixfiles when relabeling system (#904279)
- correctly detect Open vSwitch device types
- clear DEVICE and TYPE variables before every iteration (#902463)
- sets BONDING_OPTS before interface is brougth up
- check an IP address for existence in ifup-alias (#852005)
- sync FSF address with GPL 2 text.
- fix rpmlint's spaces vs tabs warning.
- fix bogus %changelog dates.
- build with $RPM_LD_FLAGS.
- use -sf, not -s. (#901827)
- add /usr/libexec/initscripts to file list (#894475)
- rename term256 to 256term (glob sort) (#849429)
- readd missing shebang. (#885821)
- migrate even further away from /etc/sysconfig/network for hostname, and /etc/sysconfig/i18n.

* Fri Dec  7 2012 Bill Nottingham <notting@redhat.com> - 9.43-1
- 60-net.rules: explicitly set the interface name (#870859)
- ifup-eth: set firewall zone before ifup-ipv6 for DHCPv6 (#802415)
- migrate to /etc/locale.conf, /etc/vconsole.conf (#881923)
- rename_device: fix bogus locking
- fix wireless device detection for kernel 3.6 (#875328)
- drop fedora-storage-init, fedora-wait-storage (<prajinoha@redhat.com>)

* Wed Oct 31 2012 Bill Nottingham <notting@redhat.com> - 9.42-1
- Halloween release!
- add a default /etc/sysctl.conf that describes how to change values, and where the defaults now live. (#760254)
- translation updates
- fedora-autorelabel: don't pass -F to fixfiles (#863662, <dwalsh@redhat.com>)
- fix calling of firewall-cmd in ifup-post/ifdown-post (<jpopelka@redhat.com>)

* Fri Oct  5 2012 Bill Nottingham <notting@redhat.com> - 9.41-1
- debugmode: MALLOC_CHECK_ is not thread safe. Don't enable it by default (#853175)
- Add support for 256 color terminals (<pbrady@redhat.com>)
- ifdown-eth: be less strict about VLAN name (#505314, <vpavlin@redhat.com>)
- drop prefdm
- ifup-eth: allow duplicate address detection to be disabled (<bcodding@uvm.edu>)
- process rule6-* for sit devices (#840009, <lnykryn@redhat.com>)

* Mon Aug  6 2012 Bill Nottingham <notting@redhat.com> - 9.40-1
- drop support for booting non-systemd systems
- drop legacy commands: getkey, fstab-decode, testd

* Fri Jun 29 2012 Bill Nottingham <notting@redhat.com> - 9.39-1
- assorted documentation cleanups
- typo, spelling, licenese clean up (<ville.skytta@iki.fi>)
- service: add support for legacy custom actions packaged in
  /usr/libexec/initscripts/legacy-actions/<script>/<action>
- network-functions: handle quoted HWADDR (#835372)
- allow bridge names that start with '-' (<danken@redhat.com>)
- remove all non-legacy uses of /sbin/route (#682308)
- move default sysctl.conf to /usr/lib/sysctl.d (#760254)

* Fri Mar 16 2012 Bill Nottingham <notting@redhat.com> - 9.37-1
- Add support for firewalld zones (#802415, from <jpopelka@redhat.com>)

* Mon Mar 12 2012 Bill Nottingham <notting@redhat.com> - 9.36-1
- ifup-aliases: fix IFS usage mangling of device names (#802119)
- ifup/ifdown: fix typo (#802055, <lubek@users.sourceforge.net>)

* Fri Mar  9 2012 Bill Nottingham <notting@redhat.com> - 9.35-1
- use the same DHCP lease file names as NetworkManager, where appropriate
- copy network state from initramfs with a systemd service, not inline (<wwoods@redhat.com>)
- sysconfig.txt: clean up section on disabling IPv6
- ifup: allow for ifup-$TYPE/ifdown-$TYPE
- fedora-readonly.service: drop StandardInput=tty (#785662)
- sysconfig.txt: document additional ETHTOOL_OPTS enhancements (<raghusiddarth@gmail.com>)
- port assorted ancient ifup-XYZ scripts away from ifconfig
- don't use ifconfig in ifup-aliases (#721010, 588993, based on <tgummels@redhat.com>)
- fedora-storage-init: handle dmraid sets with spaces (#728795, <lnykryn@redhat.com>)
- fedora-readonly: don't exit with an error if SEinux isn't active. (#768628)
- init.d/network: fix checks for network filesystems (#760018)
- fedora-wait-storage: drop stdin/stdout/stderr (#735867)
- netfs: move to legacy package
- translation updates

* Tue Oct 25 2011 Bill Nottingham <notting@redhat.com> - 9.34-1
- read locale.conf if it exists (#706756)
- ifdown: fix logic error with removing arp_ip_target (#745681)

* Wed Oct 12 2011 Bill Nottingham <notting@redhat.com> - 9.33-1
- netconsole: only use the first ARP response (#744309, <doug.knight@karmix.org>)
- udev/rules.d/88-clock.rules: drop this entirely, as it causes issues in conjunction with systemd
- init.d/network: be less picky about ifcfg file names. (#742276)
- /sbin/service: do not check for the existence of a systemd unit before redirecting (<mschmidt@redhat.com>)
- init.d/functions: only run consoletype if connected to something that's console-ish. (#657869)

* Fri Sep  2 2011 Bill Nottingham <notting@redhat.com> - 9.32-1
- prefdm: if exec() of all DMs fails, call 'plymouth quit' (#735215)
- %%ghost rc.local (but leave it around on upgrade) (#734268)
- ifup: support random bridging options via BRIDGING_OPTS (#734045, #665378)
- selinuxfs moved to /sys/fs, handle it (#733759)
- netfs/fedora-storage-init: call multipath and kpartx with -u (#733437)
- plymouth lives in /bin (#702814)
- drop fedora-autoswap
- ifdown-eth: fix dhclient pid file for IPv6 (#729292, <daveg@dgit.ndo.co.uk>)
- move some more things to the legacy subpackage
- netfs: don't mount gfs2 here (#689593)
- readonly-root: add an empty CLIENTSTATE definition (#725476)
- drop sysinit hack/unhack
- ifup-eth: allow more options in ETHTOOL_OPTS (#692410, #693583)
- rwtab: update for systemd (#704783)
- debug.csh: fix for latest csh
- update translations: eu_ES, hy, ku, lo, my, wa

* Tue Jun 21 2011 Bill Nottingham <notting@redhat.com> - 9.31-1
- remove ifup/ifdown-ipsec; they're now in ipsec-tools
- rc.sysinit: start udev by hand, start_udev is no more (#714531)
- ifup-aliases: if IPv6 is configured on the alias, configure it. (#583409)
- ifup-eth: ensure DHCP_HOSTNAME is a short hostname, seed it from HOSTNAME if needed. (#697877)
- network-functions: override NETMASK from PREFIX where specified (#705367, <mpoole@redhat.com>)
- exclude single symlink from main package (#705457)
- network: VLAN, etc. interfaces can be slaves; check for being a slave first. (#703475)
- network: use LC_ALL=C when calling sed. (https://bugs.mageia.org/show_bug.cgi?id=1216, via <sander.lepik@eesti.ee>)
- functions: (umount_loop) fuser -k defaults to -9; set the initial pass to kill -15. (#703457)
- init.d/halt: don't match filesystem types in hostnames (#703203, <jmueller@data-tronics.com>)

* Wed Apr 27 2011 Bill Nottingham <notting@redhat.com> - 9.30-1
- ifup-eth: handle IPADDRx correctly for static addresses (#697838)
- systemd: fix storage setup service after cryptsetup.target (#699918)
- prefdm: tweak how plymouth is quit in the gdm/kdm case (<rstrode@redhat.com>)
- support /etc/hostname as an override for hostname in /etc/sysconfig/network
- init.d/single: only ship this in -legacy
- network-functions: fix IPADDRx index handling (<jklimes@redhat.com>)
- ifup/down-eth: properly handle apr_ip_target, when used with module options (#604669, <harald@redhat.com>)
- ifup-eth: ensure bond exists before bringing up slaves (#694501)

* Wed Apr 06 2011 Bill Nottingham <notting@redhat.com> - 9.29-1
- systemd: add a storage setup service after cryptsetup.target (#692198)
- fix /.autorelabel handling (<mschimdt@redhat.com>)
- don't explicitly disallow IPv6 aliases (#583409, #612877)
- netfs: don't print errors if mdadm isn't installed. (#692187)
- ifup-eth: use /run/initramfs rather then /dev/.run/initramfs (<harald@redhat.com>)

* Fri Mar 25 2011 Bill Nottingham <notting@redhat.com> - 9.28-1
- add some generic network logging, port scripts to it (#507515, #653630)
- add an error when setting the gateway fails (#672202)

* Thu Mar 17 2011 Bill Nottingham <notting@redhat.com> - 9.27-1
- init.d/functions: fix mishandled argument to fstab-decode. (#685137)
- support ipv6 routing rules, merge route/rule code (#680872, <tobiasoed@hotmail.com>)
- autorelabel.service, loadmodules.service: fix conditions so that they operate as OR, not AND. (#684125)

* Thu Mar 10 2011 Bill Nottingham <notting@redhat.com> - 9.26-1
- network-functions: fix check for unmanaged devices (#670154)
- ifup-eth: also check /dev/.run/initramfs (<harald@redhat.com>)
- systemd: execute fedora-sysinit-unhack after sysinit.target (<arvidjaar@gmail.com>)
- init.d/functions: don't do force/lazy umount for the first nfs umount. (#676851, <jlayton@redhat.com>)
- further sysctl.d fixes (#593211)
- init.d/functions: make killproc more granular when delay is passed. (#428029, <xjakub@fi.muni.cz>)
- ifup: add GVRP support (#597598, <tomek@jot23.org>)
- init.d/functions: add support for noauto crypt devices, to mirror systemd
- documentation updates
- bash cleanups (<ville.skytta@iki.fi>)
- ifup: remove network device naming requirement from VLAN devices (#462095, <Matt_Domsch@dell.com>)

* Fri Feb 25 2011 Bill Nottingham <notting@redhat.com> - 9.25-1
- remove 'Red Hat Linux' references from sysctl.conf* (<ville.skytta@iki.fi>)
- rc.sysinit: add support for sysctl.d (#593211, <martin@laptop.org>)
- console_check: support OMAP serial console (#678875, <ndevos@redhat.com>)
- /sbin/service: accept --ignore-dependencies, --skip-redirect as options
- /sbin/service: honor SYSTEMCTL_IGNORE_DEPENDENCIES (<lennart@poettering.net>)
- translation updates: kn, pa, ta, uk

* Fri Jan 21 2011 Bill Nottingham <notting@redhat.com> - 9.24-1
- ifup-eth/ifdown-eth: handle 'MASTER' being quoted. (#651450, <gfidente@redhat.com>)
- tmpfiles.d: remove entries that exist in systemd
- frob device when calling sysctl, in case of vlans. (#665601, #667211, <ossman@cendio.se>)
- netfs: rework to handle bind-mounted cifs/ncpfs (#663140, <dmudrich@nospam.mudrichsystems.com>)
- own /etc/crypttab (#664309)
- init.d/network: add # as a valid character in network device names (<Matt_Domsch@dell.com>)
- ifup-eth: fix routing regression (#660363)
- sysctl.conf.s390 - system z optimized sysctl settings per default (#633323, <plautrba@redhat.com>)
- serial.conf, tty.conf: stop tty and serial also on runlevel 's' (#629257, <plautrba@redhat.com>)
- translation updates: bn_IN, es, gu, hi, nds, or, pa, uk, zh_CN

* Thu Dec 02 2010 Bill Nottingham <notting@redhat.com> - 9.23-1
- don't throw errors on unreadable /dev/stderr (#650103, <plautrba@redhat.com>)
- support multiple ipv4 addresses, not just alias devices (#132912, #633984, <jklimes@redhat.com>)
- properly handle /var/run on tmpfs (#656602, <plautrba@redhat.com>)
- allow '0' as a vlan tag (#624704, #635360)
- assorted systemd unit cleanup (<lennart@poettering.net>)

* Tue Nov 16 2010 Bill Nottingham <notting@redhat.com> - 9.22-1
- merge in systemd-specific startup support; package a -legacy package
  (based on work by <harald@redhat.com>)
- init-ipv6.global: don't load sit module on shutdown. (#654098, <ejsheldrake@gmail.com>)
- do not call rhgb-client
- network-functions: add infiniband mapping (#648524, <monis@voltaire.com>)
- fix ifdown nmcli invocation (#612934, jklimes@redhat.com>)
- *ipv6*: don't use obsolete /sbin/ip wrapper
- sysconfig.txt: adjust clock docs (#637058)
- lang.csh: fix tcsh + grep-2.7. (#636552)

* Fri Sep 17 2010 Bill Nottingham <notting@redhat.com> - 9.21-1
- build for systemd only
- ship a default.target link in case the one in /etc gets deleted
- rc.sysinit: reset btmp on boot if necessary (#633768, <dmach@redhat.com>)
- single.service: fix invocation so that 'runlevel' works (#630914)

* Thu Sep  9 2010 Bill Nottingham <notting@redhat.com> - 9.20-1
- use new pidof -m option to avoid false positives (#632321)
- systemd/single: set $HOME for single-user mode. (#631590)
- systemd/killal.service: require shutdown.target (#630935, #632198)

* Tue Sep  7 2010 Bill Nottingham <notting@redhat.com> - 9.19-1
- fix packaging of prefdm, rc-local systemd units (#630952)
- systemd/single.service: conflict with shutdown.target (#630935)
- translation updates: ja, pt_BR, ru

* Fri Sep  3 2010 Bill Nottingham <notting@redhat.com> - 9.18-1
- fix for new cgroups location (#612789, others <plautrba@redhat.com>)
- add in basic systemd units
- translation updates: nb, pt, sv

* Wed Aug 25 2010 Bill Nottingham <notting@redhat.com> - 9.17-1
- init.d/functions: redirect start/stop/condrestart/etc to systemctl in a systemd environment (#612728)
- rc.sysinit: don't frob the console loglevel on boot (#621257, #626572)
- service: use systemctl on systemd services
- 10-console.rules: only init consoles on add, not change (<lennart@poettering.net>)
- halt: fix unmounting bind mounts (#620461, <phr@doc.ic.ac.uk>)
- killall: exit 0 (#605519)
- translation updates: de, es, fi, fr, nl, pl, sv, uk

* Tue Jul 27 2010 Bill Nottingham <notting@redhat.com> - 9.16-1
- halt: don't umount cgroups (#612789)
- rename_device: dequote DEVICE key, handle SUBCHANNELS (<harald@redhat.com>)
- sysconfig.txt: document PREFIX/NETMASK (#617481, <jklimes@redhat.com>)
- sysconfig.txt: document NETWORKWAIT (#595386)
- remove support for hotkey interactive startup (#605016). Use 'confirm' on the commandline
  (but even that doesn't fully make sense in an upstart/systemd world)
- don't directly execute bash for single-user mode (#540216, #584443, #585053)

* Thu Jun 24 2010 Bill Nottingham <notting@redhat.com> - 9.15-1
- ifup-eth: check for dhclient configuration in /etc/dhcp as well (#607764, #607766)
- network-functions: handle quoted SUBCHANNELS (#607481)
- netfs: allow for encrypted network block devices (#605600)
- ifdown-ipsec: don't use a full path when killing racoon, so it works in MLS policy (#567295)
- network-functions: check NM_CONTROLLED before deciding to use NM for a connection. (#599707, probably others.)
- rc.sysinit: always reboot on autorelabel. (#595823)
- init.d/functions: handle permission denied on reading PID file. (#595597)
- clean up some deprecated items
- translation updates: el, nl, or, zh_CN

* Wed May 19 2010 Bill Nottingham <notting@redhat.com> - 9.14-1
- clean up plymouth shtudown splash (#590099, <rstrode@redhat.com>)
- rc.sysinit: use lvm2 --sysinit option (#588777)
- network-functions: behave sanely in the absence of $DEVICE (#589521)
- sysconfig/debug: export debug variables (#589378)
- netfs: check for NM to be connected, not just running (#589710)
- rcS*.conf: check if /etc/inittab exists (#590703, <plautrba@redhat.com>)
- port vlan code to /sbin/ip (#566485, <plautrba@redhat.com>)

* Wed May  5 2010 Bill Nottingham <notting@redhat.com> - 9.12-1
- update for final nmcli syntax

* Mon May  3 2010 Bill Nottingham <notting@redhat.com> - 9.11-1
- init/plymouth-shutdown.conf: add 'task' here as well

* Wed Apr 28 2010 Bill Nottingham <notting@redhat.com> - 9.10-1
- fstab-decode.8: fix formatting (#586476)
- prefdm: add --retain-splash for KDM as well (#585250)
- init.d/functions: handle being unable to read a specified pid file. (#584575)
- init/quit-plymouth.conf: use 'task' for stopping plymouth. (<rstrode@redhat.com>)
- ifup-eth: run dhclient -6 similar to dhclient -4. (#585047)
- net.hotplug: don't run on odd interfaces. (#584530)

* Fri Apr  9 2010 Bill Nottingham <notting@redhat.com> - 9.09-1
- rc.sysinit: change RAID handling (<dledford@redhat.com>)
- fix german mistranslation (#575954, <pb@bierenger.de>)
- init.d/functions: correct fix for environment with runuser. (#203010, #564093)
- halt: fix mdmom pid handling for newer mdadm (#549726, <dledford@redhat.com>)
- init.d/network: only blacklist the original loopback interface. (#579816, <evgsyr@gmail.com>
- translation updates: de, ja, nb, pt, sv, uk

* Mon Mar  8 2010 Bill Nottingham <notting@redhat.com> - 9.08-1
- network-functions: redirect error messages when nmcli isn't installed (#570828, <zing@fastmail.fm>)
- ifdown: use nmcli to get the device, if not specified
- ifdown: fix typo
- translation updates: fr

* Wed Mar  3 2010 Bill Nottingham <notting@redhat.com> - 9.07-1
- clean out some extraneous package requirements
- fix dmraid error checking now that dmraid has return codes (#568790, others)
- integrate with NetworkManager for ifup/ifdown (#523064)
- translation updates: cs, da, de, en_GB, es, fi, nl, pl, pt_BR, ru, sr

* Fri Feb 19 2010 Bill Nottingham <notting@redhat.com> - 9.06-1
- move ccw_init and ccw udev rules to s390utils (#539491)
- rc.sysinit: suppress LVM2 warnings.  (#561938, <prajnoha@redhat.com>)
- fix translated checks for user input (#566579)
- refresh translations

* Mon Feb 15 2010 Bill Nottingham <notting@redhat.com> - 9.05-1
- network-functions: don't use ethtool for link state, assorted other cleanups
- inittab: fix job paths in comments (<plautrba@redhat.com>)
- init.d/functions: don't clear environment in runuser (#203010, #564093)
- 88-clock.rules: use ATTR, not SYSFS (#560756)
- init.d/network: don't quote regex argument to bash's =~ (<ville.skytta@iki.fi>)
- network-functions: use HWADDR to determine DEVICE if DEVICE isn't set (#545597)
- don't HUP init when messagebus starts (#557791)
- setsysfont: use UNIMAP, not SYSFONTACM, when calling unicode_start (#557089)
- ifup: don't leave the link down on link failure for DHCP (#462013, #491009)
- translation updates: cs

* Fri Jan 15 2010 Bill Nottingham <notting@redhat.com> - 9.04-1
- various shell-related cleanups and optimizations <ville.skytta@iki.fi>
- ifup-eth: use dhclient's -H option instead of munging dhclient config files
- rc.sysinit: move mdadm after dmraid (#494821)
- ifup-eth: use dhclient -6, not the no-longer-included dhcp6c
- add more man pages (#529328, <plautrba@redhat.com>)
- move is_wireless after MACADDR/MTU setting (#552638)
- serial.conf: respawn correctly. (#552324, <zing@fastmail.fm>)
- network-functions: use sysfs for wireless check (#551019, <adel.gadllah@gmail.com>)
- reload init on started messagebus (<plautrba@redhat.com>)
- honor HOTPLUG in ifdown (#547737)
- network-functions: silence error. (#516569)

* Wed Dec  9 2009 Bill Nottingham <notting@redhat.com> - 9.03-1
- migrate to upstart 0.6.x (<notting@redhat.com>, <plautrba@redhat.com>)
-- jobs move to /etc/init
-- collapse rcX and ttyX jobs into single job definitions
-- jobs are no longer %%config
- remove obsolete doexec command
- rc.sysinit: handle yet another random return string from dmraid
- remove never-used 'sulogin' upstart event
- fix time-setting udev rules for old-style RTC devices (#537595)
- init.d/network: keep error codes limited to '1'. (#537841)
- add initial ifup/ifdown man pages. (#529328, <plautrba@redhat.com>)

* Tue Oct 27 2009 Bill Nottingham <notting@redhat.com> - 9.02-1
- remove long-since deprecated initlog
- remove IUCV support (#507217)
- halt: put a wrapper around killall5 to account for retval 2 not being an error (#526539, <hdegoede@redhat.com>)
- ifup-eth: honor DEFROUTE=yes|no for 'all' connection types. (#528822)
- network-functions: load bonding driver if BONDING_OPTS is defined. (#516569)
- rc.sysinit: put /dev/shm in mtab too, as dracut now mounts it. (#528667)

* Fri Oct  9 2009 Bill Nottingham <notting@redhat.com> - 9.01-1
- rc.sysinit: fix handling of dmraid output to avoid error messages (#527726, <mschmidt@redhat.com>)
- rwtab: add /var/lib/xend (#526046)
- translation updates: fi, nb, pl

* Fri Oct  2 2009 Bill Nottingham <notting@redhat.com> - 9.00-1
- halt: wrap /sbin/killall5 to catch some return codes (#526539)
- netfs, netconsle, network: fix return codes to match LSB spec (#524489, #524480, #524486)
- handle kernels compiled both with and without CONFIG_RTC_HCTOSYS
- halt: use killall5's return code to avoid unncesssary sleeping (#524359, <hdegoede@redhat.com>)
- halt: don't kill mdmon on shutdown. (#524357, <hdegoede@redhat.com>)
- rc.sysinit: do not try and activate ISW raidsets, unless noiswmd is passed. (#524355, <hdegoede@redhat.com>)
- translation updates: ca, cs, da, mai, po, sv, uk

* Mon Sep 14 2009 Bill Nottingham <notting@redhat.com> - 8.99-1
- init.d/functions: add a '-l' option to status to pass lock file name (#521772)
- tweak kernel conflict
- translation updates: as, bn_IN, de, fr, hi, it, hu, kn, mr, or, pa, pt, ru, te

* Wed Sep  2 2009 Bill Nottingham <notting@redhat.com> - 8.98-1
- sysconfig.txt: doucment DHCP_HOSTNAME (#498052)
- 88-clock.rules: Use --systz instead of --hctosys. (#517886, #489494)
- Support rwtab and state passed from dracut initrd (#515771, <wtogami@redhat.com>)
- restore context of *tmp files (#519748)
- halt: don't try and save mixer settings if it's not writable. (#515771)
- rwtab: add /var/spool, /var/lib/dbus, others (#494973, #515771)
- sysconfig.txt: clarify docs (#518614)
- rc.sysinit: don't pretend /selinux is configurable (#518164)
- assorted ipv6 redundant code deletion
- translation updates: bn, ca, de, es, fi, fr, gu, hi, it, ja, ko, ml, nb, nl, pl, pt, pt_BR, ru, sr, ta, zh_CN, zh_TW

* Mon Aug 10 2009 Bill Nottingham <notting@redhat.com> - 8.97-1
- ipcalc: fix IPv6 address checking (#516319)
- ifup-aliases: fix syntax error from earlier cleanups. (#515612, <jik@kamens.brookline.ma.us>)
- translation updates: nb
- rc.sysinit: remove useless call to pam_console_apply

* Mon Aug  3 2009 Bill Nottingham <notting@redhat.com> - 8.96-1
- fix up upstart rules for s390(x). (#515222)
- leave ChangeLog in the tarball only. (#515012)
- disable netfilter on bridged interfaces. (#512206)
- assorted shell-related cleanups to ipv6 and other code (<victor.lowther@gmail.com>)
- use resolv.conf from dracut netboot before setting hostname. (#514801, <wtogami@redhat.com>)
- ipcalc updates (<victor.lowther@gmail.com>)
- only use ethtool for link checking; no more mii-tool
- require /sbin/blkid directly, as it moves between packages (#508413)
- redirect bash errors on 'unset' to /dev/null. (#482888)
- fix dmraid partition naming (#501476, <hdegoede@redhat.com>)
- don't quote upstart signals. (#501155)
- translation updates: bn_IN, da, es, sk

* Fri May  1 2009 Bill Nottingham <notting@redhat.com> - 8.95-1
- don't kill runlevel events on subsequent entering of the same runlevel (#498514)
- lang.*sh: handle spaces in $HOME (#498482)
- network-functions: explicitly source from the proper directory. (#496233)
- remove persistent names on sys-unconfig. (#448322)
- init.d/functions: cgexec has moved to /bin (#495715)
- allow changing of VLAN type even if the module is already loaded. (#495053, <pietro@bertera.it>)
- translation updates: fr, ml, pt

* Tue Apr  7 2009 Bill Nottingham <notting@redhat.com> - 8.94-1
- prefdm: add simple fallbacks, sort rpmdb query for consistency (#494461)
- translation updates; bn, de, pt, ru, te

* Thu Apr  2 2009 Bill Nottingham <notting@redhat.com> - 8.93-1
- rc.sysinit: add a disk synchronization point with scsi_wait_scan post-udev (#481470)
- netfs: drop smbfs support, we don't even ship the module or tools any more
- setsysfont: honor LC_CTYPE (#487133, <skasal@redhat.com>)
- prefdm: do fallbacks based on provides of 'service(graphical-login)' (#485751)
- rc.sysinit: handle multiple IP addresses without choking in the stateless code (#443945)
- rc.sysinit: catch the right error code from checking for passphrases (#483269, <vladis.kletnieks@vt.edu>)
- prefdm: handle empty /etc/sysconfig/desktop correctly (#480113)
- ifup-ipsec: allow use of either ESP only or AH only (#251494, <stijn.tintel@x-tend.be>)
- ifup-eth: allow passing of arguments to dhcp6c (#437949, <pekkas@netcore.fi>)
- ifup-eth: fix dhcpv6 when there is no IPv4 configuration (#486507)
- ifup-ppp: avoid spurious SIGCHLD to pppd (#448881)
- ifup-eth: add support for creating TUN/TAP devices on the fly (#453973, <scott@zahna.com>)
- stop plymouth when starting single-user mode. (#491062)
- add plymouth shutdown script (#473237, <jmccann@redhat.com>)
- fix lang.sh/lang.sh/consoletype for execution with '-e'
- ifdown-eth: remove arp_ip_target on ifdown for bonding devices. (#483711)
- add vlan support for s390 HSI interfaces. (#490584)
- ipcalc: support IPv6 (#464268, <dcantrell@redhat.com>)
- translation updates: all

* Mon Mar 16 2009 Bill Nottingham <notting@redhat.com> - 8.91-1
- fix DHCP reading of options from ifcfg-XXX (#483257)
- ifdown-eth: clean up bridges on ifdown (#463325, <sean@bruenor.org>)
- support MD on iSCSI (#480627)
- remove support for 'ifcfg-foo-bar' configurations that inherit from 'ifcfg-foo'
- remove slip support
- translation updates: es, pl, ca, sr, de, sv, pa, pt_BR

* Mon Mar  9 2009 Bill Nottingham <notting@redhat.com> - 8.90-1
- init.d/functions: cgroup support (<jsafrane@redhat.com>)
- fix various issues with dmraid handling (#485895, <hdegoede@redhat.com>)
- rc.sysinit: fix typo. (#487926)
- console_init: loadkeys has a -q option for silent running. Use it.
- ifup-tunnel: add compatibility for openNHRP tunnels (#486559, <claude.tompers@ieee.lu>)
- ccw_init: don't re-init an existing device, it causes errors. (#484411, <jpayne@redhat.com>)
- netfs: use same kpartx arguments as rc.sysinit
- don't list mtab in rwtab (#457941)
- translation updates: fi, de, mai

* Wed Jan 28 2009 Bill Nottingham <notting@redhat.com> - 8.89-1
- use a leading path when sourcing files (#482826)
- netfs: don't unmount nfsd filesystem by accident (#481794, <sprabhu@redhat.com>)
- bring up ipsec interfaces last (#481733)
- ifdown-eth: fix bridge + vlan (#481557, <danken@redhat.com>)

* Tue Jan 20 2009 Bill Nottingham <notting@redhat.com> - 8.88-1
- init.d/network: return success/failure correctly (#480677)
- init.d/halt: fix typo (#480799)

* Mon Jan 19 2009 Bill Nottingham <notting@redhat.com> - 8.87-1
- rename_device: be much faster in the presence of many devices (#480687, <danms@us.ibm.com>)
- fix switching from targeted to MLS policy (#479054, <dwalsh@redhat.com>)
- rc.sysinit: don't set $(uname -r) or $(uname -m); they're not used
- network-functions-ipv6: set MTU correctly for 6to4. (#477976, <ackistler@yahoo.com>)
- add more entries to rwtab (#476799, <harald@redhat.com>)
- net.hotplug: Bail out sooner if the network service isn't running
- init.d/halt: determine reboot/halt via existing INIT_HALT environment variable. (#475227)
- event.d/serial: add some docs
- init.d/functions: __pids_var_run: Handle multi-line pid files correctly (#473287)
- remove support for no longer existing 'brctl setgcint' command. (#360471)
- add %%config back for ifcfg-lo (#472761)
- rcS/rcS-sulogin: don't match commented lines when finding runlevel (#472717)
- updated translations: de, sk

* Tue Nov 11 2008 Bill Nottingham <notting@redhat.com> - 8.86-1
- stop plymouth before stopping the runlevel (#467207)
- fix get_config_by_subchannel (#459044, <harald@redhat.com>)
- use blkid -l to pick a single most appropriate device (#470027)
- don't mkswap on halt, as it breaks swap-by-label/UUID (#469823)

* Fri Oct 31 2008 Bill Nottingham <notting@redhat.com> - 8.85-1
- add some error handling/hiding to netfs NM dispatcher script (#469197)
- halt: fix code that causes a syntax error on multiple sound cards (#469156)
- require a new enough udev version to handle where we put the rules
- exit 0 in /etc/rc.d/rc (#469050)
- don't set up encrypted devices that have already been set up under different
  names (#462371, <wwoods@redhat.com>)
- accept either the '+<addr>', or comma-separated addresses for arp_ip_target. (#467954,
  <darcy.sherwood@gmail.com>)
- translation updates: hu, kn, ko, ml, sr, sr@latin

* Tue Oct 14 2008 Bill Nottingham <notting@redhat.com> - 8.84-1
- override Arabic, Persian, and Hebrew on the console (<alsadi@ojuba.org>)
- explicitly run mdadm on boot to catch degraded arrays. (<dledford@redhat.com>)
- fix setting of console font/map (#458362, <ak@sensi.org>)
- translations updates: hi, kn, nb, sk, sv, ta

* Tue Sep 30 2008 Bill Nottingham <notting@redhat.com> - 8.83-1
- various merge review fixes (#225900)
  Notably: init scripts/network scripts are no longer %%config
- remove some extraneous device-mapper initialization
- use pidfile in status before calling pidof (#463205)
- use plymouth directly, not the rhgb-client wrapper
- move bridging after bonding (#449950, <djuran@redhat.com>)
- use alsactl to save sound settings. (#462677, <jkysela@redhat.com>)
- quit plymouth differently (<rstrode@redhat.com>)
- make sure we don't try and spawn a repair shell when there's no
  tty (#463161)
- move udev rules to /lib
- stateless updates (#433702, <harald@redhat.com>)
- call logger with a full path (#447928, <harald@redhat.com>)
- translation updates: as, bn_IN, ca, cz, de, es, fi, fr, gu, it, ja,
  lv, mr, nl, or, pa, pl, pt_BR, ru, te, zh_TW

* Wed Sep 10 2008 Bill Nottingham <notting@redhat.com> - 8.82-1
- refresh translation strings
- plymouth updates. (#460702, <rstrode@redhat.com>)
- translation updates: fi, lv, no
- remove duplicate dependency (#465182)
- ifup-eth: Change how we set the zeroconf route. (#239609)
- ifup*: Use 0.0.0.0/0, not 0/0. (#460580)

* Fri Aug 29 2008 Bill Nottingham <notting@redhat.com> - 8.81-1
- rc.sysinit: Don't use -L in find (#458652, #458504, CVE-2008-3524)
- ifup: kill more code from loopback bringup

* Tue Jul 29 2008 Bill Nottingham <notting@redhat.com> - 8.80-1
- Fix translation typo (#455804, <ruslanpisarev@gmail.com>)
- Turn off syncookies
- Cleanups for proper plymouth support
- Move the mcheck code to a debugmode package, make it more generic

* Mon Jul 14 2008 Bill Nottingham <notting@redhat.com> - 8.79-1
- fix mcheck stuff to be installed correctly
- don't do an arping check for loopback interfaces
- console_init: don't wait (<arjan@infradead.org>)
- rc: clean up extraneous set -x noise
- remove references to static dmraid/multipath binaries (#453987)
- translation updates: lv

* Fri Jun 20 2008 Bill Nottingham <notting@redhat.com> - 8.78-1
- fix mounting of /dev/pts

* Thu Jun 19 2008 Bill Nottingham <notting@redhat.com> - 8.77-1
- NMDispatcher/05-netfs: fix check for default route (#445509)
- service: don't set $LANG, rely on it to inherit from system locales (#422141)
- init.d/functions: fix resolve_dm_raid() for older dmraid configs
- Don't unmount sysfs in halt. (#446292)
- rc.sysinit: don't try to startup crypto if we can't find the device
- rc.sysinit: don't echo crypto stuff unless we're actually *doing* something
- ifup: don't try to rename devices - udev rules are the way to go
- rc.sysinit: fix typo, and don't restorecon on swap, etc. partitions (#448886)
- set MALLOC_CHECK_ & MALLOC_PERTURB_ if configured (<pjones@redhat.com>)
- console_init: support SYSFONTACM correctly, and support UNIMAP (#448704,
  <vvv+fedora@colocall.net>)
- don't export GRAPHICAL - plymouth is for all modes. also, don't start rhgb
- fix clock rules to properly handle old-style RTC devices (#447019)
- translation updates: ko, or, pl

* Fri May  2 2008 Bill Nottingham <notting@redhat.com> - 8.76-1
- fix tcsh syntax error (#444998)
- remove debugging cruft from rcS-sulogin

* Tue Apr 29 2008 Bill Nottingham <notting@redhat.com> - 8.74-1
- use full path to /sbin/ip in NetworkManagerDispatcher script (#444378)
- lang.{sh,csh}: read only user customization if LANG is already set (#372151)

* Fri Apr 25 2008 Bill Nottingham <notting@redhat.com> - 8.73-1
- move event-compat-sysv events here, obsolete it
- fix ctrl-alt-del during rc.sysinit (#444050)
- fix 'telinit X' from single-user mode (#444001)

* Thu Apr 24 2008 Bill Nottingham <notting@redhat.com> - 8.72-1
- don't have a S99single when using upstart (#444001, indirectly)

* Wed Apr 23 2008 Bill Nottingham <notting@redhat.com> - 8.71-1
- adjust to gdm using LANG instead of GDM_LANG (#372151, <rstrode@redhat.com>)
- rework netfs' check for networking availability to properly handle both network
  and NetworkManager

* Tue Apr 15 2008 Bill Nottingham <notting@redhat.com> - 8.70-1
- find is now in /bin. Use it. (#192991, #239914, #244941, #442178)
- require event-compat-sysv for now (#442291)
- fix serial event to wait properly
- handle encrypted LVs properly (#441728)
- add a sit tunnel type (#441635)
- translation updates: ru

* Tue Apr  8 2008 Bill Nottingham <notting@redhat.com> - 8.69-1
- Bring up lo whenever it shows up, not just in network/NM
- fix shutdown-related oddities (#438444)
- translation updates: el, sr, sr@latin, sv

* Fri Apr  4 2008 Bill Nottingham <notting@redhat.com> - 8.68-1
- netfs: umount 'ncp' filesystems as well (#437117)
- improve performance of s390 ccw rules (#437110, <mernst@de.ibm.com>)
- fix consoletype environment leak (#439546)
- ifdown-eth: make sure NEWCONFIG exists before grepping for it (#390271, continued)
- console_check: always open with NONBLOCK, clear the serial structs first,
  handle non-16550 ports (<dwmw2@infradead.org>)
- halt: don't use /etc/sysconfig/clock (#438337)
- ifup: don't attempt to re-enslave already-enslaved devices (#440077)
- netfs: run as a NetworkManagerDispatcher script (#439242)
- netfs: remove $local_fs from the list of provides (making it implicitly provided
  by booting)
- serial: add a crude hack to wait for runlevels to finish (#437379)
- serial: frob /etc/securetty when necessary (#437381)
- add a upstart-specific inittab
- translation updates: as, bn_IN, cs, de, es, fi, fr, gu, hi, it, ja, kn, ml, mr, nb,
  nl, pa, pl, pt_BR, ru, sk, sr, ta, te, zh_CN

* Tue Mar 11 2008 Bill Nottingham <notting@redhat.com> - 8.67-1
- actually, don't

* Tue Mar 11 2008 Bill Nottingham <notting@redhat.com> - 8.66-1
- use upstart to start rhgb (#433156, <cdahlin@ncsu.edu>)

* Mon Mar 10 2008 Bill Nottingham <notting@redhat.com> - 8.65-1
- Add a serial console udev/upstart handler (#434764, indirectly)
- Add some upstart notification for sysv scripts (modified from <cjdahlin@ncsu.edu>, #431231)
- Handle _rnetdev correctly (#435358, <pjones@redhat.com>)
- various minor speedups (<arjan@infradead.org>)
- translation updates: el, fr
- disable network by default, in favor of NetworkManager

* Tue Feb 26 2008 Bill Nottingham <notting@redhat.com> - 8.64-1
- Add a console_init udev helper to do console initialization
- add /sbin/pidof requirement (#434863)

* Fri Feb  1 2008 Bill Nottingham <notting@redhat.com> - 8.63-1
- don't start RAID arrays in rc.sysinit, that's done by udev (corollary of #429604)
- add a NetworkManager-dispatcher script that does netreport on interface changes
- use udev rules to set the clock, avoiding issues with modular rtcs (#290731)

* Mon Jan 21 2008 Bill Nottingham <notting@redhat.com> - 8.62-1
- rc.d/rc.sysinit: fix syntax error (#429556)
- migrate sr@Latn -> sr@latin (<kmilos@gmail.com>)

* Fri Jan 18 2008 Bill Nottingham <notting@redhat.com> - 8.61-1
- use lvm, not lvm.static (#429222)
- ifup-eth: don't do something odd if we find a mac address that
  matches the user-set MACADDR (#251415)
- rc.sysinit: fix root fs check to catch 'rw,ordered,noatime,etc.' properly
  (#334171)
- rc.sysinit: Use proper invocations for authconfig, system-config-network
  (#426372, #428202)
- service: handle unreadable scripts (#427767)
- initscripts.spec: add requirements for stateless
- fix perms on /etc/profile.d (#407531, <ville.skytta@iki.fi>)
- rename_device: handle quoted HWADDR, etc. in ifcfg scripts (#351291)
- minor stateless fixes
- Makefile cleanups (from OLPC, <cscott@cscott.net>)
- translation updates: fr, ru, nb
- don't endelessly loop on ifdown (#390271)
- rc.sysinit: - fix encrypted swap partitions with random key
  (<harald@redhat.com>)

* Tue Oct  9 2007 Bill Nottingham <notting@redhat.com> - 8.60-1
- don't chvt with rhgb - just kill it when needed

* Mon Oct  8 2007 Bill Nottingham <notting@redhat.com> - 8.59-1
- rc.sysinit: fix rhgb check
- prefdm: add wdm section (#248087)
- init.d/functions, halt: clean up some extraneous delays (#219816)
- ifup-wireless: set mode before bringing link up (#254046, <linville@redhat.com>)
- translation updates: pt_BR, hr

* Fri Oct  5 2007 Bill Nottingham <notting@redhat.com> - 8.58-1
- revert kernel conflict so that xen can still work (#319401)
- rename_device, 60-net.rules: only suggest an interface name (part of #264901)
- require newer udev for persistent net rules (part of #264901)
- don't hang if someone puts a dangling pipe in /etc/rhgb/temp (#251219)
- genhostid: fix for 64-bit systems (#306811)
- more bash matching fixes (#220087)
- translation updates: is, nb

* Tue Sep 25 2007 Bill Nottingham <notting@redhat.com> - 8.57-1
- work around upstream bash changes (#220087, modified from <nvigier@mandriva.com>)
- init.d/network: add Should-Start for firewall services
- ifup-eth: handle arp_ip_target separately (#288151, <agospoda@redhat.com>)
- rc.sysinit: remove rc.serial support - should be udev rules
- rc.sysinit: remove acpi module loading - now supported by the kernel automatically
- fix en_GB translation (#271201)
- translation updates: as, bn_IN, bg, ca, cs, de, el, es, fi, gu, hi, it, ja, ko, kn, ml,
  mr, nb, nl, pa, pl, pt, pt_BR, ro, sl, sr, sr@Latn, sv, ta, te, zh_CN

* Wed Aug 29 2007 Bill Nottingham <notting@redhat.com> - 8.56-1
- rename_device: fix open() call
- rc.sysinit: optimize out some excess greps (<harald@redhat.com>)
- halt: support newer nut syntax, conflict with old versions (#252973, <tsmetana@redhat.com>)
- fix buildreq from popt -> popt-devel
 - newer popt is in /lib|/lib64 - require it, and link dynamically
- rc.sysinit: added support for cryptsetup-uuids (bug #242078, <harald@redhat.com>)
- netconsole: fix status(), assorted other cleanups
- translation updates: fr, ro, sk

* Fri Jul 27 2007 Bill Nottingham <notting@redhat.com>
- add /etc/networks (#239602)
- rc.sysinit: fix quotacheck, remove obsolete convertquota (#249003, <tometzky@batory.org.pl>)
- rc.sysinit: add gfs2 to the 'don't mount here' list (#248985)
- netfs: check for rpcbind, not portmap (#245595)
- ifup-eth: set 'primary' later for bonding devices (#236897, <agospoda@redhat.com>)
- translation updates: cy, en_GB, mk, ml, ms, pl, sk, ta, zh_CN

* Tue Jul 17 2007 Nils Philippsen <nphilipp@redhat.com>
- avoid calling unicode_start unnecessarily often during startup/shutdown which
  causes certain monitor/video card combos to flicker heavily (#237839)

* Tue May 15 2007 Bill Nottingham <notting@redhat.com> 8.54-1
- translation updates: as, bg, cs, ja, ms
- redirect bogus errors from cryptsetup to /dev/null <karsten@redhat.com>

* Thu Apr 19 2007 Bill Nottingham <notting@redhat.com> 8.53-1
- init.d/halt: use sound saving wrapper from alsa-utils, conflict with
  older versions (#236916)
- usernetctl: drop user gid (#229372)
- translation updates: ta, pt_BR, nb, as, hi, de

* Mon Apr 16 2007 Bill Nottingham <notting@redhat.com> 8.52-1
- lang.sh: fix locales where SYSFONT is not the default (#229996)
- ifup-wireless: properly quote arguments (#234756)
- readonly-root: add options for mounting state (#234916)
- rwtab: updates (#219339, <law@redhat.com>)
- add netconsole init script (#235952)
- disable link checking when PERSISTENT_DHCLIENT is set (#234075)
- restore file context on /etc/resolv.conf (#230776, <dwalsh@redhat.com>)
- ifup-post: only use the first address (#230157, <michal@harddata.com>)
- ifup-ipsec: allow overriding of my_identifier (#229343, <cmadams@hiwaay.net>)
- ifup-wireless: set link up before itweaking wireless parameters (#228253)
- rc.sysinit: restorecon on mount points when relabeling (#220322)
- init.ipv6-global: cleanup & optimize sysctl usage (#217595)
- ifup-eth: support ETHTOOL_OPTS on bridge devices (#208043, <bbaetz@acm.org>)
- network-functions-ipv6: as we don't use NETWORKING_IPV6, silence errors (#195845)
- fix description (#229919)
- translation updates

* Fri Feb 23 2007 Bill Nottingham <notting@redhat.com> 8.51-1
- fix 'Fedora Fedora' in rc.sysinit
- halt: use kexec -x to not shut down network (#223932, <mchristi@redhat.com>)
- network_functions: fix is_bonding_device logic (#229643)
- translation updates: nb

* Mon Feb 19 2007 Bill Nottingham <notting@redhat.com> 8.50-1
- lang.csh, lang.sh: if $LANG is set, don't override it (#229102)
- initlog.1: fix man page formatting (<esr@thyrsus.com>)
- network-functions: simplify bonding test (#215887, <herbert.xu@redhat.com>)
- fix ifup-post when lookup fails (#220318, <hiroshi.fujishima+redhat@gmail.com>)
- add bridging docs (#221412, <markmc@redhat.com>)
- release bonding slaves properly (#220525)
- fix ppp-watch with ONBOOT=yes (#216749)
- support VLAN_PLUS_VID_NO_PAD (#222975, #223011)
- remove NETWORKING_IPV6; to disable, use a modprobe rule
- translation updates: ms, de, el, pt_BR, fi, bs, sr, it, ko

* Tue Dec 19 2006 Bill Nottingham <notting@redhat.com> 8.49-1
- rc.sysinit: remove raidautorn (#219226)
- ifup-eth: set MACADDR, MTU before initializing bonding slaves, etc (#218792)
- translation updates: mr, ms, hi, te, ml

* Tue Nov 28 2006 Bill Nottingham <notting@redhat.com> 8.48-1
- add a step to rename any temporarily renamed devices (#208740, #214817)
- make sure network modules don't get accidentally reloaded (#211474)
- rc.sysinit: fix dmraid test (#216334)
- init.d/halt: don't unmount network filesystems
- ipsec: Add a way to manually manage racoon.conf (#159343, <mitr@redhat.com>)
- sysconfig.txt: Document ~/.i18n (#199323, <mitr@redhat.com>)
- some translation updates

* Mon Nov  6 2006 Bill Nottingham <notting@redhat.com> 8.47-1
- lang.{sh,csh}: handle sinhalese as well in CJKI clauses (#212438)
- rc.sysinit: add '--auto=yes' to mdadm invocation (#213671)
- rename_device: fix incorrect handling of .bak files
- mount tmpfs with -n (#213132)
- various SUBCHANNELS related s390 fixage (#204803)
- lang.{sh,csh}: support iso-8859-8 (#212738, <matan@svgalib.org>)

* Fri Oct 27 2006 Bill Nottingham <notting@redhat.com> 8.46-1
- ifup-eth: restorecon on moved lease file
- rc.sysinit: handle "nodmraid" and "nompath" command line options (#209377, <pjones@redhat.com>)
- revert early-login support (#210836, essentially)
- blacklist CJKI on the virtual console (#120819)
- rc.sysinit: use dmraid.static (#211297)
- use sysfs interface for bonding (#202443, <agospoda@redhat.com>)
- use /etc/statetab, /etc/statetab.d for local state (#211839, <markmc@redhat.com>)
- fix or_IN and similar locales (#212219)
- use SUBCHANNELS as the primary key for s390 network devices (#204803)
- translation updates

* Fri Oct  6 2006 Bill Nottingham <notting@redhat.com> 8.45-1
- lang.csh/lang.sh - do *not* stty iutf8; too much chaos with SIGTTOU
  (reverts: #186961; fixes #209469)
- translation updates: ms

* Wed Oct  4 2006 Bill Nottingham <notting@redhat.com> 8.44-1
- separate tmpfs-usage for state from readonly-root
- set keymap correctly in non-utf8 locale (#167363)
- setsysfont: run unicode_stop if in non-unicode locale
- lang.csh/lang.sh: set iutf8 if appropriate (#186961)
- lang.csh/lang.sh: handle non-utf8 locales correctly (#200100)
- rc.sysinit: redirect stderr from setsysfont (#209204, indirectly)
- rwtab: fix iscsi file location (#208864)
- translation updates: el, da, as, or
- fix stateless updates (#206331, <law@redhat.com>)

* Wed Sep 27 2006 Bill Nottingham <notting@redhat.com> 8.43-1
- move ccwgroup initialization to a udev rule (should fix #199139,
  #199655, #169161)
- init.d/functions: don't write to gdmfifo
- remove unused-since-RHL-7 consolechars code, update docs (#206106)
- stateless updates (#206331, <law@redhat.com>)
- translation updates (el, ms, hr, sl)

* Thu Sep 21 2006 Bill Nottingham <notting@redhat.com> 8.42-1
- run rc.sysinit, /etc/rc in monitor mode (part of #184340)
- use a better check for 'native' services (#190989, #110761, adapted
  from <matthias@rpmforge.net>)

* Tue Sep 19 2006 Bill Nottingham <notting@redhat.com> 8.41-1
- fix network ipv6 hang (#207137, others)
- rc.sysinit: change blkid.tab path to /etc/blkid/blkid.tab
- rename_device: reset DEVPATH also when renaming (#206884, <phil@fifi.org>)
- sysconfig.txt: clarify onboot/onparent usage

* Fri Sep 15 2006 Bill Nottingham <notting@redhat.com> 8.40-1
- translation updates
- rename_device: use '__tmpXXXX' instead of 'devXXXX' as a temporary device
  name to avoid any realistic namespace clashes
- rc.sysinit: set default affinity if specified on commandline (#203359)
- always pass path to '.' (#206035)
- run setsysfont, loadkeys always when /dev/tty{0,1} exist (#150769)
- allow going to a shell when system is shut down cleanly (from <dwalsh@redhat.com>)

* Tue Sep  5 2006 Bill Nottingham <notting@redhat.com> 8.39-1
- translation updates
- Handle partitions on multipath/dmraid better (<pjones@redhat.com>)
- make /dev/mapper/control ourselves (<pjones@redhat.com>)
- init.d/network: simplify 'status' call
- fix actual 169.254 networks (#203591)
- rc.sysinit: don't run vgscan (#191879)
- init.d/halt: don't umount /dev/root<foo> (<oblin@mandriva.com>)
- rc.sysinit: catch more dmraid errors (#200683)
- support 'tmp' option in /etc/crypttab (#201382, <mitr@redhat.com>,
  <lv@lekv.de>)
- IPv6 updates (<pb@bieringer.de>, includes a fix for #143452)

* Tue Aug  1 2006 Bill Nottingham <notting@redhat.com> 8.38-1
- translation updates
- bring down bonding slaves on ifdown (#199706)
- support LINKDELAY for dhcp (#191137)
- netfs: run multipath on netdev devices (#180977)
- halt: use /proc/mounts instead of /etc/mtab (#198426, <mitr@redhat.com>)
- rc.sysinit: fix getkey race (#191453, <mitr@redhat.com>)
- spec cleanups (#188614, <kloczek@rudy.mif.pg.gda.pl>)
- support aliases on vlan (#193133, <mitr@redhat.com>)
- clean up ifcfg file handling (<mitr@redhat.com>, <michal@harddata.com>)
- GRE and IPIP tunnel support (#168990, <mitr@redhat.com>,
  <razvan.vilt@linux360.ro>, <aaron.hope@unh.edu>, <sean@enertronllc.com>)
- rc.sysinit: don't format encrypted swap always (#127378)
- don't try to add routes to alias devices (#199825, #195656)

* Fri Jul 21 2006 Bill Nottingham <notting@redhat.com> 8.37-1
- update translations

* Fri Jul 21 2006 Bill Nottingham <notting@redhat.com> 8.36-1
- rework automatic swapon - only run if AUTOSWAP=yes, and fix errors
  (#198695, #196179, #196208)
- redo single so it starts last in runlevel 1, and doesn't kill/start
  services itself
- add configurable delay for killproc() (#198429, <jorton@redhat.com>)
- fix loop in rename_device (#199242, <markmc@redhat.com>)
- rc.sysinit: stateless updates (#197972, <law@redhat.com>)
- support for copying dhcp leases from initramfs (#198601, <markmc@redhat.com>)
- readonly-root: SELinux works now in the kernel, allow it
- init.d/network: don't bring down network if root is on a network device
- init.d/halt: don't use -i to halt; causes problems with iscsi
- add support for routing rule-$device (#132252, <mitr@redhat.com>)
- fix rhgb output (#192604, <tonynelson@georgeanelson.com>)
- fix crypttab options for LUKS (#197656, <mitr@redhat.com>)
- ipsec: various fixes & new features (#150682, #168972, <mitr@redhat.com>, <alex@milivojevic.org>)
- ipsec: add check for IKE_METHOD (#197576, <john_smyth@mail.ru>)
- rename_device: ignore alias devices, fix race (#186355)
- ifup/ifdown: don't mark as %%config
- rwtab: some additions/cleanup

* Mon Jun 12 2006 Bill Nottingham <notting@redhat.com> 8.35-1
- readonly root enhancments (modified from <law@redhat.com>, #193164)
- encrypted swap, non-root filesystem support (#127378, <mitr@redhat.com, <redhat@flyn.org>)
- clarify killproc usage (#193711, <mitr@redhat.com>)
- document BRIDGE= (#192576, <mitr@redhat.com>)
- rc.sysinit: allow for sulogin instead of automatic relabeling (<dwalsh@rehdat.com>)

* Tue May 23 2006 Bill Nottingham <notting@redhat.com> 8.34-1
- link glib2 dynamically now that it's in /lib, conflict with older
  versions
- handle cups specially when cleaning /var (#189168)
- remove ifdown-aliases (<mitr@redhat.com>)
- ifup-ipsec: fix key handling when only one of AH or ESP is used
  (#166257, <mituc@iasi.rdsnet.ro>)
- IPv6 updates, including RFC 3041 support (<pb@bieringer.de>)
- routing fixes, add METRIC support for default routes (#124045, <mitr@redhat.com>)
- fix handling of mount points with white space (#186713, <mitr@redhat.com>)

* Thu Apr 20 2006 Bill Nottingham <notting@redhat.com> 8.33-1
- support for readonly root
- rc.sysinit: remove call to zfcpconf.sh - that should be udev rules
- ifup*: add NETWORKDELAY and LINKDELAY (#176851, <mitr@redhat.com>)
- rc.sysinit: remove obsolete initrd code (<pjones@redhat.com>)

* Mon Apr 10 2006 Bill Nottingham <notting@redhat.com> 8.32-1
- netfs: fix redirect (#187505)
- rc.sysinit add forcequotacheck (#168118, <mitr@redhat.com>)
- functions/pidof: various fixes (#182623, others <mitr@redhat.com>)
- add support for DHCP on bridges (#125259, <mitr@redhat.com>,
  anders@kaseorg.com>)
- rc.sysinit: use pidof, not killall (#185429, <pjones@redhat.com>)
- ppp fixes (#129195, #163950, #92023, <mitr@redhat.com>, <avi@argo.co.il>)
- ifup/ifdown: unset $WINDOW (#174336, <mitr@redhat.com>)

* Fri Mar 17 2006 Bill Nottingham <notting@redhat.com> 8.31.2-1
- add udev helper to rename network devices on device creation

* Tue Mar 14 2006 Bill Nottingham <notting@redhat.com> 8.31.1-1
- fix context of /dev/pts (#185436)
- translation updates

* Sun Mar  5 2006 Bill Nottingham <notting@redhat.com> 8.31-1
- fix kexec support (<jmoyer@redhat.com>)
- translation updates

* Tue Feb 28 2006 Bill Nottingham <notting@redhat.com> 8.30-1
- hotplug: don't cause modules to be reloaded on ifdown/rmmod (#179809)
- fix endless loops in ifup/ifdown (#177792, #182466)
- fix enabling of enforcing SELinux mode after relabel (#181893)
- remove debugging code from ifup-bnep
- add /proc, /sys mounting back to rc.sysinit
  Note: booting without an initrd is deprecated
- translation updates

* Tue Feb 14 2006 Peter Jones <pjones@redhat.com> 8.29-1
- scrub another possible error message from dmraid output

* Mon Feb 13 2006 Bill Nottingham <notting@redhat.com> 8.28-1
- kill nash-hotplug before starting udev (<pjones@redhat.com>)
- silence warnings on /dev/pts remount (<pjones@redhat.com>)
- more translation updates

* Mon Feb 13 2006 Bill Nottingham <notting@redhat.com> 8.27-1
- translation updates
- lang.sh: revert fix for #176832, it's broken
- ifup-aliases fixes (<pjones@redhat.com>,<mitr@redhat.com>)

* Tue Feb  7 2006 Bill Nottingham <notting@redhat.com> 8.26-1
- revert "rc.sysinit: don't mount usbfs, libusb no longer uses it" change
- add some ugly hacks to make sure net hotplug doesn't run after unclean
  shutdown (#177795)
- don't mount /sys and /proc in rc.sysinit - the initrd already does
  (<pjones@redhat.com>)
- halt: try to unmount tmpfs filesystems before swapoff (#174000,
  <mitr@redhat.com>)

* Thu Feb  2 2006 Bill Nottingham <notting@redhat.com> 8.25-1
- ifup: don't run the arping check if the address is already on the device

* Wed Feb  1 2006 Bill Nottingham <notting@redhat.com> 8.24-1
- init.d/functions: fix sendmail startup
- sysconfig.txt: fix typos (<mitr@redhat.com>)

* Tue Jan 31 2006 Peter Jones <pjones@redhat.com> 8.23-1
- rc.sysinit: do a better job of not activating already active dmraids

* Tue Jan 31 2006 Bill Nottingham <notting@redhat.com> 8.22-1
- remove references to /usr/X11R6/bin (#177938)
- rc.sysinit: fix SELinux message formatting (#178532)
- rc.sysinit: clean cvs as well (#178539, <ville.skytta@iki.fi>)
- init.d/halt: move halt.local so that it runs before /  is remounted r/o (#179314)
- rc.sysinit: don't activate already active dmraids (<pjones@redhat.com>)
- rc.sysinit: don't mount usbfs, libusb no longer uses it
- init.d/functions: Add -p to status() (#134363, <mitr@redhat.com>)
- init.d/functions: Separate /var/run/*.pid handling and pidof calls
  to private functions (#63440, <mitr@redhat.com>)
- init.d/functions: update for current LSB, including -p pidfile
  (#99325, #134363, <mitr@redhat.com>, <tobias.burnus@physik.fu-berlin.de>)
- getkey: various cleanups, add man page (#54481, <mitr@redhat.com>)
- lang.sh: don't always call consoletype (<laroche@redhat.com>)

* Fri Jan 20 2006 Bill Nottingham <notting@redhat.com> 8.21-1
- move handling of network hotplug events here, add appropriate udev
  rules, obsolete hotplug
- get rid of some path lookups (#178321, <mclasen@redhat.com>)
- get hwaddrs from sysfs as opposed to ip | sed
- translation updates
- lang.sh: don't run unicode_start for subshells (#176832)
- halt: ignore sysfs but not /sys<otherstuff> (#177612, <bnocera@redhat.com>)
- add service(8) man page (#44857) <mitr@redhat.com>

* Wed Dec 21 2005 Bill Nottingham <notting@redhat.com> 8.20-1
- remove kmodule. udev handles module loading now
- require appropriate udev

* Thu Dec 15 2005 Bill Nottingham <notting@redhat.com> 8.19-1
- Require syslog, for alternate implementations thereof (#172885)
- Fix fsck invocation for weeding out netdev devices (#175803)

* Fri Dec  2 2005 Bill Nottingham <notting@redhat.com> 8.18-1
- use new dhclient file paths, add appropriate conflict (#169164)

* Wed Oct  5 2005 Bill Nottingham <notting@redhat.com> 8.17-1
- make sure corefile limiting works for user processes as well
  (#166511, <ville.skytta@iki.fi>)
- ifup-routes: handle no EOF in the route file (#156972)
- rc.sysinit: tweak mesage (#156972)
- ifdown-eth: clean up error message (#135167)
- rc.sysinit: call kpartx on multipath devices (#160227)
- ifup-eth: move wireless options before bridge options (#122801)
- ifup-wireless: silence error (#90601)
- init.d/functions: change translated string (#54682)

* Tue Sep 27 2005 Than Ngo <than@redhat.com> 8.16-1
- fix typo bug

* Mon Sep 26 2005 Than Ngo <than@redhat.com> 8.15-1
- support proper dial-in configuration, thanks to Peter Bieringer (#158380)

* Thu Sep 22 2005 Bill Nottingham <notting@redhat.com>
- kmodule: don't probe for uninteresting devices. speeds things up
- network-functions: deal with broken networks better (#168947)
- rc.sysinit: automatically reboot if labels are really out of date
  (<dwalsh@redhat.com>)
- network-functions: throw out nameif error messages
- rc.sysinit: use multipath.static (#168321)
- rc.sysinit: use ignorelocking (#168195)

* Mon Sep 12 2005 Bill Nottingham <notting@redhat.com> 8.14-1
- fix usage of the module blacklist (#168020)

* Fri Sep  9 2005 Bill Nottingham <notting@redhat.com> 8.13-1
- fix on-boot relabelling (<dwalsh@redhat.com>)

* Mon Aug 22 2005 Bill Nottingham <notting@redhat.com> 8.12-1
- ifup-eth: fix interface renaming (#158774)
- rc.sysinit: use modprobe, not insmod (#159120, <tmus@tmus.dk>)
- remove workaround for the fonts-not-initialized-on-secondary-consoles
  problem (fixed in 2.6.12-rc4 and later)
- setsysfont: correctly bracket systfontacm (#159706)
- rc.sysinit: always use udevsend, even if no modules (#160987)
- ifdown-aliases: add 'cd' to the proper dir (#161170)
- add diskdump restore support (<tuchida@redhat.com>),
  conflict with appropriate diskdumputils
- rc.sysinit: dmraid/multipath support
  - remove LVM1 support
- init.d/functions: handle odd quoting in args (#161316, <stransky@redhat.com>)
- ifup-wireless: set rate in quotes (#163123)
- handle lvm & fsck for network block devices (#148764,
  <alewis@redhat.com>)
- initlog: fix invalid free calls,  (#165033), (#163973,<dwalsh@redhat.com>)
- sysconfig.txt: remove hdparm docs, since the code isn't there (#162962)
- updated translations: ms, ja, ko, et, zh_CN, zh_TW, sr, ar

* Tue May 10 2005 Bill Nottingham <notting@redhat.com> 8.11-1
- fix mis-bringup of interfaces due to accidentally matched HWADDR
  (a.k.a. ONBOOT=no not working) (#153669, #157252)
- support automatic relabeling later if rebooted w/o SELinux
  (<dwalsh@redhat.com>)
- rc.sysinit: fix fixfiles invocation (#157182)
- btmp should be 0600 (#156900)
- translation updates: fr, bg, ru, mk, pa, es

* Fri Apr 29 2005 Bill Nottingham <notting@redhat.com> 8.10-1
- fix hang on stale GDM sockets (#156355)

* Wed Apr 27 2005 Bill Nottingham <notting@redhat.com> 8.09-1
- rc.sysinit: clean up screen sockets (#155969)
- functions: use pidof -c in various functions
- ifup-ppp: fix static routes with ppp demand dialing (#20142,
  <ohrn+redhat@chalmers.se>)
- add btmp support (#155537)
- don't send dhcp hostname (revert of fix for #149667)
- more early-login modifications (<mclasen@redhat.com>)
- functions: fix echo (#155270)

* Mon Apr 18 2005 Karsten Hopp <karsten@redhat.de> 8.08-3
- fix ifup-routes script (#155195)

* Mon Apr 18 2005 Florian La Roche <laroche@redhat.com>
- fix strstr call in rc.sysinit

* Fri Apr 15 2005 Bill Nottingham <notting@redhat.com> 8.08-1
- update translation base
- automatically send hostname for DHCP if it's available and not
  overridden (#149667)
- load user-defined module scripts from /etc/sysconfig/modules at
  boot (#123927)
- halt: reverse sort the mount list, avoiding errors
  (#147254, <jamesodhunt@hotmail.com>)
- ifup-wireless: add SECURITYMODE (#145407)
- network-functions: don't error out if hotplug doesn't exist (#140008)
- ifup: always return errors on trying to bring up nonexistent devices (#131461)
- ifup: fix error message (#143674)
- rc.sysinit: add a autorelabel boot target (#154496)
- prefdm: if something else is specified as $DISPLAYMANAGER, try that (#147304)
- remove support for the old firewall type
- network: optimize some (#138557, <drepper@redhat.com>)
- prefdm: fix prefdm arg handling (#154312, <khc@pm.waw.pl>)
- gdm early-login support (adapted from <rstrode@redhat.com>)
- ifup-routes: make sure commented lines are handled correctly (#154353,
  #114548, <link@pobox.com>)
- some sysconfig.txt updates (<link@pobox.com>, <jvdias@redhat.com>)
- rc.sysinit: fix restorecon invocation (#153100)
- initlog: free some of the more egregious memory leaks (#85935)
- initlog: fix potential memory overread (#153685, <in-redhat@baka.org>)
- remove some conflicts, %%post scripts, etc. that were only relelvant
  for upgrades from pre-7.0
- other minor fixes, see ChangeLog

* Thu Mar 31 2005 Bill Nottingham <notting@redhat.com> 8.07-1
- bring back initlog for third-party scripts until a new framework is
  in place

* Wed Mar 30 2005 Bill Nottingham <notting@redhat.com> 8.06-1
- handle alternate VLAN naming schemes (#115001, <kas@informatics.muni.cz>)
- ifup-ipsec: handle non-ascii keys (#150552)
- add proper ipsec route (#146169, #140654)
- add a restorecon for /tmp to rc.sysinit
- document ONHOTPLUG in sysconfig.txt
- fix mistranslation (#151120)
- don't return 1 for stopping a process if it isn't running at all
- don't explicitly set fwd polices for ipsec traffic. Let setkey
  handle it.

* Mon Mar  7 2005 Bill Nottingham <notting@redhat.com> 8.05-1
- ipv6 cleanups (<pb@bieringer.de>)
- rc.sysinit: fix rngd check (#130350)
  ... then turn it off entirely
- rc.sysinit: get rid of duplicate date printout (#149795)
- ifdown: handle being called on down devices better
- handle saved resolv.conf on all device types
- fix network-functions cleanup
- netfs: fix _netdev unmounting (#147610, <alewis@redhat.com>)
- dhcp release cleanups (<jvdias@redhat.com>)
- ifup-bnep: bluetooth update <dwmw2@infradead.org>
- more ipsec stuff (#147001, <ckjohnson@gwi.net>)

* Wed Jan 19 2005 Bill Nottingham <notting@redhat.com> 8.04-1
- split out ifup/ifdown general case to ifup/ifdown-eth;
  add ifup/ifdown-bnep (<dwmw2@redhat.com>)
- ifup-ipsec: add fwd policies (#145507)
- fix multiple scsi_hostadapter loads (#145432)
- enable syncookies in sysctl.conf (#145201)

* Wed Jan 12 2005 Bill Nottingham <notting@redhat.com> 8.03-1
- use udevsend to handle hotplug events (requires recent udev)
- remove pump, dhcpcd support
- fix ONxxx (#136531, <cww@redhat.com>)
- fix various fgreps to not catch commented lines (#136531, expanded
  from <cww@redhat.com>)
- set ETHTOOL_OPTS on addressless devices (#144682, <mpoole@redhat.com>)
- kill dhcp client even if BOOTOPROTO is now static (#127726, others)
- replace the use of route/ifconfig with ip in IPv6 code, remove support
  for ipv6calc (<pb@bierenger.de>, <pekkas@netcore.fi>)
- fix quoting in daemon() (#144634)
- make sysctl be silent (#144483)

* Mon Jan  3 2005 Bill Nottingham <notting@redhat.com> 8.02-1
- remove initlog, minilogd
- add a flag to kmodule for use with kudzu's socket mode, use it
- change setting of IPv6 default route (#142308, <pb@bieringer.de>)
- netfs: don't unmount NFS root FS (#142169)

* Mon Dec  6 2004 Bill Nottingham <notting@redhat.com> 8.01-1
- further bootup noise reductions
- rc.d/rc.sysinit: do implicit unicode conversion on keymap

* Mon Nov 29 2004 Bill Nottingham <notting@redhat.com> 8.00-1
- fix previous fix (#139656)

* Wed Nov 24 2004 Bill Nottingham <notting@redhat.com> 7.99-1
- clear and repopulate mtab before mounting other filesystems (#139656)
- remove more devfs compat

* Tue Nov 23 2004 Bill Nottingham <notting@redhat.com> 7.98-1
- various kmodule speedups
- rc.d/init.d/netfs: don't mount GFS (#140281)
- fix various minilogd bogosities (#106338)

* Mon Nov 15 2004 Karsten Hopp <karsten@redhat.de> 7.97-1
- configure CTC protocol if CTCPROT is set (#133088)

* Mon Nov 15 2004 Bill Nottingham <notting@redhat.com>
- fix check_link_down to still check negotiation if link is
  listed as "up" on entering (#110164, <dbaron@dbaron.org>)

* Thu Nov 11 2004 Karsten Hopp <karsten@redhat.de> 7.96-1
- parse OPTIONS for QETH, CTC, LCS interfaces (#136256, mainframe)

* Tue Nov  9 2004 Bill Nottingham <notting@redhat.com>
- fix typo (#134787, <bnocera@redhat.com>)

* Sun Nov  7 2004 Bill Nottingham <notting@redhat.com> 7.95-1
- various translation updates

* Tue Nov  2 2004 Bill Nottingham <notting@redhat.com>
- take an axe to rc.sysinit:
  - remove delay on unclean startup
  - remove hdparm code
  - remove LVM1 code
  - remove old raidtab code in favor of mdadm
  - remove support for old isapnp tools
  - move all block device mangling before fsck. run fsck *once*, not twice
  - some more LC_ALL=C stuff

* Sun Oct 31 2004 Florian La Roche <laroche@redhat.com>
- /etc/rc.d/rc: use "LC_ALL=C grep" for small speedup
- /etc/rc.d/rc.sysinit:
  - do not read udev.conf, this seems to be all in the start_udev script
  - fix detection of "nomodules" kernel command line option
  - read /proc/cmdline earlier and convert rhgb to use that, too
  - load_module(): change redirection to /dev/null
  - some checks for RHGB_STARTED="" looked strange
- /etc/sysconfig/network-scripts/ifup-ppp:
  - remove a call to basename with shell builtins
- /etc/sysconfig/network-scripts/network-functions:
  - remove some calls to basename/sed with shell builtins

* Wed Oct 27 2004 Bill Nottingham <notting@redhat.com> 7.93.2-1
- fix prefdm fallback to installed display managers (#137274)
- fix incorrect rhgb temporary path (#137391)

* Mon Oct 18 2004 Bill Nottingham <notting@redhat.com> 7.93-1
- translation updates
- fix handling of GATEWAYDEV (#133575, <pekkas@netcore.fi>)

* Sun Oct 17 2004 Bill Nottingham <notting@redhat.com> 7.91-1
- rc.d/rc.sysinit: remove devlabel call
- mdadm support, now that raidtools is gone (#126636, #88785)
- call ipv6to4 scripts in /etc/ppp/(ip-up|ip-down) (#124390, <dwmw2@redhat.com>)
- cleanup a couple of nits that could affect bug #134754
- make sure we return to rhgb after fsck (#133966, #112839, #134449)
- automatically reboot when fsck calls for it, instead of requiring
  manual intervention (#117641 and duplicates)
- ifup-wireless: fix key for open vs. restricted (#135235, <dax@gurulabs.com>)
- translation updates

* Fri Oct 08 2004 Karsten Hopp <karsten@redhat.de> 7.90-1
- fix portname for LCS devices

* Fri Oct 08 2004 Bill Nottingham <notting@redhat.com>
- remove sysconfig/rawdevices, as initscript is removed

* Thu Oct 07 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- change /etc/sysctl.conf to not allow source routed packets per default

* Wed Oct  6 2004 Bill Nottingham <notting@redhat.com> - 7.88-1
- fix requires

* Tue Oct  5 2004 Dan Walsh <dwalsh@redhat.com> - 7.87-1
- Change SELinux relabel to not remount /

* Mon Oct  4 2004 Bill Nottingham <notting@redhat.com>
- use runuser instead of su; require it
- init.d/halt: use right file name for random seed (#134432)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> - 7.86-1
- use /etc/hotplug/blacklist to blacklist modules in hardware init (#132719)
- filter indic locales on the console (#134198)

* Wed Sep 29 2004 Bill Nottingham <notting@redhat.com> - 7.85-1
- ifup, network-functions: fix worked-by-accident shell quoting
- lang.csh: remove setting of dspmbyte (#89549, <mitr@redhat.com>)
- SELinux fixes
- clean up prefdm
- init.d/functions: export LC_MESSAGES (#133786)
- allow daemon to coredump if requested (#130175)
- network-functions: be more liberal in what we accept for link types (#90602, #127984)
- fix overzealousness with -range aliases (#65415)
- rc.sysinit: use s-c-keyboard, not kbdconfig (#133929)
- fix checkpid logic, clean up potential errors (#134030)
- translation updates

* Wed Sep 22 2004 Bill Nottingham <notting@redhat.com> - 7.84-1
- only start udev once

* Wed Sep 22 2004 Jeremy Katz <katzj@redhat.com> - 7.83-1
- conflict with old udev
- use udev if it's present

* Tue Sep 21 2004 Bill Nottingham <notting@redhat.com>
- don't mount usbfs without usb. also, at least be consistent in filesystem type

* Fri Sep 17 2004 Bill Nottingham <notting@redhat.com> - 7.82-1
- fix handling of nonexistent devices (#132839)
- rhgb enhancements (<veillard@redhat.com>, #132665)
- initscripts.spec: require nash (#132513)
- translation updates

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 7.81-1
- load iucv device config after /etc/sysconfig/network so that
  GATEWAY doesn't get overwritten

* Fri Sep 10 2004 Bill Nottingham <notting@redhat.com> - 7.80-1
- fix IPv6 6to4 & NAT (#118928, <pb@bieringer.de>, <pekkas@netcore.fi>)

* Fri Sep 10 2004 Karsten Hopp <karsten@redhat.com> - 7.79-1
- load ctc device config after /etc/sysconfig/network so that
  GATEWAY doesn't get overwritten

* Wed Sep  8 2004 Dan Walsh <dwalshg@redhat.com> - 7.78-2
- fix setting SELinux contexts on udev-created-in-initrd devices
- Let restorecon check if selinux is enabled.

* Wed Sep  8 2004 Bill Nottingham <notting@redhat.com> - 7.78-1
- set SELinux contexts on udev-created-in-initrd devices, if necessary

* Wed Sep  1 2004 Bill Nottingham <notting@redhat.com> - 7.77-1
- mount usbfs (#131347)
- start any automatic raid devices
- remove triggers for ancient releases, bulletproof remaining ones (#131356)

* Wed Sep  1 2004 Jeremy Katz <katzj@redhat.com> - 7.76-1
- udev uses UDEV_TMPFS now

* Wed Sep 01 2004 Karsten Hopp <karsten@redhat.de> 7.75-1
- fix sysfs configuration of qeth and lcs network interfaces
  (eth, tr, hsi)

* Mon Aug 30 2004 Karsten Hopp <karsten@redhat.de> 7.74-1
- fix support for LCS portnumbers (mainframe)

* Fri Aug 27 2004 Jason Vas Dias  <jvdias@redhat.com> 7.73-1
- Add support for running the DHCPv6 client to ifup
- (new DHCPV6C=yes/no ifcfg-${IF} variable) + update sysconfig.txt

* Fri Aug 27 2004 Bill Nottingham <notting@redhat.com> 7.72-1
- flip the kernel conflict to a Requires:

* Thu Aug 26 2004 Karsten Hopp <karsten@redhat.de> 7.71-1
- ifcfg-iucv/ctc: drop REMIP and use GATEWAY instead

* Thu Aug 26 2004 Bill Nottingham <notting@redhat.com> 7.70-1
- autoload hardware modules on startup
- minor fsck cleanup (#115028, <leonard-rh-bugzilla@den.ottolander.nl>)
- ifup: support STP bridging (#123324)
- rc.sysinit: do a SELinux relabel if forced
- rc.sysinit: remove devfs compat and the remaining 2.4 compat
- ifup-wireless: support multiple keys (#127957)
- fix firmware loading (#129155, <bnocera@redhat.com>)

* Tue Aug 24 2004 Karsten Hopp <karsten@redhat.de> 7.68-1
- execute zfcfconf.sh if available (mainframe)

* Mon Aug 23 2004 Jason Vas Dias <jvdias@redhat.com> 7.67-1
- fix change_resolv_conf: if pre-existing /etc/resolv.conf
- non-existent or empty, replace with new file contents.

* Fri Aug 20 2004 Jason Vas Dias <jvdias@redhat.com> 7.66-1
- Allow users to use generic /etc/dhclient.conf if per-device
- /etc/dhclient-${DEVICE}.conf is non-existent or empty

* Fri Aug 20 2004 Jason Vas Dias <jvdias@redhat.com> 7.66-1
- Preserve "options" settings in resolv.conf (bug 125712)

* Fri Aug 20 2004 Jeremy Katz <katzj@redhat.com> - 7.65-1
- look at /etc/udev/udev.conf, not /etc/sysconfig/udev (#130431)

* Fri Aug 20 2004 Bill Nottingham <notting@redhat.com> 7.64-1
- rc.d/rc.sysinit: check for dev file too (#130350)

* Thu Aug 19 2004 Than Ngo <than@redhat.com> 7.63-1
- allow CBCP with own number (#125710)

* Thu Aug 19 2004 Bill Nottingham <notting@redhat.com> 7.62-1
- fix up resolv.conf munging (#129921)
- use rngd if available
- run start_udev if necessary (#120605)
- readonly root updates (#129893, <markmc@redhat.com>)
- ifup-wireless: quote key (#129930)
- remove rawdevices (#130048)
- handle binfmt_misc in rc.sysinit for the case where it's built in (#129954)
- remove mkkerneldoth
- don't remove linguas in lang.* (part of #9733)
- fix nfs unmounting (#129765)
- fix URL (#129433)

* Wed Aug 11 2004 Jason Vas Dias <jvdias@redhat.com> 7.61-1
- fix for bug 120093: add PERSISTENT_DHCLIENT option to ifcfg files

* Tue Aug  3 2004 Karsten Hopp <karsten@redhat.de> 7.60-1
- write peerid into sysfs for IUCV devices (mainframe)

* Tue Aug  3 2004 Bill Nottingham <notting@redhat.com>
- don't remove /dev/mapper/control - nash will do it if it has to (#127115)

* Fri Jul 30 2004 Jason Vas Dias <jvdias@redhat.com> 7.60-1
- fix for bug 125712: add 'change_resolv.conf' function

* Tue Jul 27 2004 Bill Nottingham <notting@redhat.com>
- rc.d/init.d/network: don't bring interfaces down twice (#127487)

* Wed Jul 14 2004 Bill Nottingham <notting@redhat.com>
- fix bonding + no IP (#127285)
- wrap second LVM initialization in vgscan check to avoid extraneous messages (#127639)

* Wed Jul  7 2004 Bill Nottingham <notting@redhat.com>
- move random stuff to rc.sysinit/halt; move all swap to after this.
  prereq of bug #123278

* Fri Jul  2 2004 Bill Nottingham <notting@redhat.com> 7.59-1
- set context on ICE directory after making it (#127099, <concert@europe.com>)
- don't mount GFS filesystems in rc.sysinit

* Tue Jun 29 2004 Bill Nottingham <notting@redhat.com> 7.58-1
- rc.d/rc.sysinit: hack: make ICE directory on boot (#86480)
- set devicetype for xDSL (#126194)
- ignore locking failures when starting lvm volumes (#126192, <radu@primit.ro>)
- unset LC_MESSAGES for rhgb (#126020, <ynakai@redhat.com>)
- bonding fixes
- setsysfont: remove error (#100559)
- remove duplicate setting of network routes (#125450)
- vlan fixes (#107504, <hrunting@texas.net>)
- ifup-aliases: remove bogus route setting (#120908)

* Tue May 25 2004 Bill Nottingham <notting@redhat.com> 7.57-1
- readonly root fixes (<alexl@redhat.com>)

* Tue May 25 2004 Karsten Hopp <karsten@redhat.de> 7.56-1
- special TYPE for qeth devices to differenciate them from ethX

* Mon May 24 2004 Bill Nottingham <notting@redhat.com>
- fix pppd vs. ppp typo in conflicts (#123680)

* Fri May 21 2004 Bill Nottingham <notting@redhat.com>
- fix bridging confusing module order (#122848, <luto@myrealbox.com>)
- rc.d/rc.sysinit: don't mount cifs (#122501)

* Tue May 18 2004 Karsten Hopp <karsten@redhat.de> 7.55-1
- add support for ccwgroup devices on mainframe

* Thu May 13 2004 Than Ngo <than@redhat.com> 7.54-1
- add patch to enable PIE build of usernetctl

* Fri May  7 2004 Jeremy Katz <katzj@redhat.com> - 7.53-1
- little lvm tweak (#121963)

* Tue May  4 2004 Bill Nottingham <notting@redhat.com> 7.52-1
- ipv4 addresses are ints, not longs (#122479)

* Tue May  4 2004 Bill Nottingham <notting@redhat.com> 7.51-1
- get rid of LVM error when no volumes are defined (#121197)
- fix selinux short-circuit test (#121143, <michal@harddata.com>)
- /dev/mapper/control is a special file, check it accordingly (#121963)
- support ETHTOOL_OPTS on bonding slaves (#119430, <hrunting@texas.net>)
- handle multiple spaces correctly in rc.sysinit, network-functions
  (#118583, <pallas@kadan.cz>)
- cleanup fd leaks, mem leaks, other bogosities
  (#119987, <linux_4ever@yahoo.com>)
- rc.d/init.d/network: remove ipv6 bogosity (#114128)
- translation updates

* Fri Apr 16 2004 Bill Nottingham <notting@redhat.com> 7.50-1
- fix LVM issues in rc.sysinit (#120458, #119975)
- deal with fixed racoon parser
- translation updates from translators
- fix USB loading (#120911)

* Fri Mar 26 2004 Bill Nottingham <notting@redhat.com> 7.49-1
- use alsa for mixer saving in halt
- don't umount /proc in halt (#118880)
- various translation updates from translators

* Wed Mar 17 2004 Bill Nottingham <notting@redhat.com> 7.48-1
- disable enforcing in emergency mode for now, relabel some commonly
  mislabeled files on boot

* Wed Mar 17 2004 Bill Nottingham <notting@redhat.com> 7.47-1
- translation: catch more input strings (#106285, <mitr@volny.cz>)
- remove autologin from prefdm (#108969)
- return to rhgb after ./unconfigured (#109807, <jkeating@j2solutions.net>)
- handle iso15 in setsysfont (#110243)
- clean up samba & vmware in rc.sysinit (#113104)
- some sysconfig.txt documentation (#110427, #118063)
- fix bug in umount-on-halt (#113088, <giardina@airlab.elet.polimi.it>)
- handle CIFS in netfs (#115691)
- make sure hotplug isn't stuck unset (#116666, <aoliva@redhat.com>)
- handle network fs better in rc.sysinit (#111290)
- nomodules applies to usb/firewire too (#113278)
- ipsec fix (#116922, <felipe_alfaro@linuxmail.org>)
- make sure rc exits cleanly (#117827, <enrico.scholz@informatik.tu-chemnitz.de>)
- fsck root FS from initrd, for dynamic majors (#117575, <sct@redhat.com>)

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Mon Feb  2 2004 Bill Nottingham <notting@redhat.com> 7.46-1
- some more rc.sysinit tweaks and refactoring

* Fri Jan 30 2004 Bill Nottingham <notting@redhat.com> 7.45-1
- fix rc.sysinit typo
- rc.d/init.d/network: clear out environment (#113937, #111584)

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 7.44-1
- NFSv4 support (<chucklever@bigfoot.com>, <steved@redhat.com>)
- handle 2.6-style 'install ethX ...' lines correctly
- mount sysfs by default
- time to clean up the cruft. remove:
  - boot-time depmod
  - linking of /boot/System.map to /boot/System.map-`uname -r`
  - /var/log/ksyms.X
  - libredhat-kernel support

* Fri Jan  16 2004 Dan Walsh <dwalsh@redhat.com> 7.43-2
- Remove selinux run_init code from service script.  It is no longer needed.

* Fri Dec  5 2003 Jeremy Katz <katzj@redhat.com> 7.43-1
- basic lvm2 support

* Tue Oct 28 2003 Bill Nottingham <notting@redhat.com> 7.42-1
- show rhgb details on service failures

* Wed Oct 22 2003 Bill Nottingham <notting@redhat.com> 7.41-1
- tweak some rhgb interactions (#100894, #107725)
- fix dvorak keymap loading (#106854)

* Wed Oct 22 2003 Than Ngo <than@redhat.com> 7.40-1
- add better fix to support nickname (#105785)

* Wed Oct 22 2003 Than Ngo <than@redhat.com> 7.39-1
- add support nickname (#105785)

* Fri Oct 17 2003 Bill Nottingham <notting@redhat.com> 7.38-1
- rhgb updates, now pass 'rhgb' to use it, instead of passing 'nogui'
  to disable it

* Fri Oct 10 2003 Bill Nottingham <notting@redhat.com> 7.37-1
- bridging updates (#104421, <dwmw2@redhat.com>)

* Wed Oct  8 2003 Bill Nottingham <notting@redhat.com> 7.36-1
- mount /dev/pts before starting rhgb

* Wed Oct  1 2003 Bill Nottingham <notting@redhat.com> 7.35-1
- load acpi modules on startup if necessary
- fix typo in ipsec comments & sysconfig.txt

* Mon Sep 15 2003 Than Ngo <than@redhat.com> 7.34-1
- use upsdrvctl to start the shutdown process

* Mon Sep 15 2003 Bill Nottingham <notting@redhat.com> 7.33-1
- ipsec fixes (#104227, <harald@redhat.com>)
- ppp fixes (#104128, #97845, #85447)

* Thu Sep 11 2003 Bill Nottingham <notting@redhat.com> 7.32-1
- fix ip calls for some device names (#104187)
- ipsec fixes

* Fri Sep  5 2003 Bill Nottingham <notting@redhat.com> 7.31-1
- fix bonding + dhcp (#91399)
- fix typo (#103781)
- sysconfig/network-scripts/ifup: fix use of local
- fix shutdown with NFS root (#100556, <Julian.Blake@cern.ch>)
- remove /var/run/confirm when done with /etc/rc (#100898)
- ipcalc: fix some memory handling (#85478, <miked@ed.ac.uk>)
- handle sorting > 10 network devices (#98209)
- unset ONPARENT after use (#101384)
- random other fixes
- bridging support (<dwmw2@redhat.com>)

* Fri Aug 15 2003 Bill Nottingham <notting@redhat.com> 7.30-1
- IPv6 updates (#86210, #91375, <pekkas@netcore.fi>)

* Fri Aug  8 2003 Bill Nottingham <notting@redhat.com> 7.29-1
- setsysfont: don't echo to /dev/console (#102004)
- fix ethernet device renaming deadlock (#101566)
- consoletype: don't return 'vt' on vioconsole (#90465)
- ifup: fix short-circuit (#101445)

* Fri Jul 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- ifup-routes: pass the interface name to handle_file() so that we don't try
  to use the routes file's name as an interface name

* Wed Jul  9 2003 Bill Nottingham <notting@redhat.com> 7.28-1
- switch from $CONFIG.keys to keys-$CONFIG

* Tue Jul  8 2003 Bill Nottingham <notting@redhat.com> 7.27-1
- add a check to consoletype for the current foreground console
- use it when running unicode_start (#98753)

* Wed Jul  2 2003 Bill Nottingham <notting@redhat.com> 7.26-1
- ipsec support (see sysconfig.txt, ifup-ipsec)
- read $CONFIG.keys, for non-world-readable keys
- allow default window size for routes to be set with WINDOW= (#98112)
- support setting device options with ethtool opts
- fix s390 bootup spew (#98078)
- support renaming interfaces with nameif based on hwaddr

* Mon Jun 23 2003 Bill Nottingham <notting@redhat.com> 7.25-1
- fix DNS punching in the case of other rules for the DNS server
  (#97686, <martin@zepler.org>)
- initlog, ppp-watch, and usernetctl tweaks (<linux_4ever@yahoo.com>)
- fix grep for mingetty (#97188)
- fix rhgb-client bad syntax
- change network device searching, use correct naming, fix route issues
  (<harald@redhat.com>)
- other random tweaks

* Fri May 23 2003 Bill Nottingham <notting@redhat.com> 7.24-1
- now even still yet more tweaks for graphical boot

* Thu May 22 2003 Bill Nottingham <notting@redhat.com> 7.23-1
- even still yet more tweaks for graphical boot

* Tue May 20 2003 Bill Nottingham <notting@redhat.com> 7.22-1
- still yet more tweaks for graphical boot

* Tue May 20 2003 Bill Nottingham <notting@redhat.com> 7.21-1
- yet more tweaks for graphical boot

* Fri May  2 2003 Bill Nottingham <notting@redhat.com> 7.20-1
- more tweaks for graphical boot

* Wed Apr 30 2003 Bill Nottingham <notting@redhat.com> 7.18-1
- some tweaks for graphical boot

* Mon Apr 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- initscripts-s390.patch: remove not needed parts about PNP=
- inittab.390: sync with normal version
- rc.sysinit: remove two further calls to /sbin/consoletype with $CONSOLETYPE

* Fri Apr 18 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- sysconfig/init.s390: set LOGLEVEL=3 as for other archs
- rc.d/init.d/network, rc.d/rc: change confirmation mode to
  not use an environment variable
- rc.d/init.d/functions: make strstr() even shorter, remove old
  "case" version that has been already commented out
- rc.d/rc.sysinit:
  - no need to set NETWORKING=no, it is not used/exported
  - do not export BOOTUP
  - delete two "sleep 1" calls that wants to add time to go
    into confirmation mode. There is enough time to press a
    key anyway or use "confirm" in /proc/cmdline.
  - read /proc/cmdline into a variable
  - use strstr() to search in /proc/cmdline
  - add "forcefsck" as possible option in /proc/cmdline
  - while removing lock files, no need to call `basename`
  - add unamer=`uname -r` and reduce number of forks
  - do not fork new bash to create /var/log/ksyms.0

* Thu Apr 03 2003 Karsten Hopp <karsten@redhat.de> 7.15-1
- Mainframe has no /dev/ttyX devices and no mingetty, don't
  initialize them. This gave error messages during startup

* Mon Mar 17 2003 Nalin Dahyabhai <nalin@redhat.com>
- init.d/network: don't advertise "probe: true" in the header if we don't
  recognize "probe" as an argument

* Wed Mar 12 2003 Bill Nottingham <notting@redhat.com> 7.14-1

* - do not handle changed chain name; change was reverted

* Tue Feb 25 2003 Bill Nottingham <notting@redhat.com> 7.13-1
- handle 7.x SYSFONTACM settings in setsysfont (#84183)

* Mon Feb 24 2003 Bill Nottingham <notting@redhat.com> 7.12-1
- handle changed chain name
- init vts used in all cases

* Fri Feb 21 2003 Bill Nottingham <notting@redhat.com> 7.10-1
- handle LANGUAGE specially for zh_CN.GB18030 and gdm (#84773)

* Thu Feb 20 2003 Bill Nottingham <notting@redhat.com> 7.09-1
- initialize two ttys past # of mingettys (for GDM)
- fix zeroconf route
- redhat-config-network writes $NAME.route for some static routes
  (e.g., ppp); handle that (#84193)

* Tue Feb 18 2003 Bill Nottingham <notting@redhat.com> 7.08-1
- load keybdev & mousedev even if hid is already loaded/static
- run fewer scripts through action (#49670, #75279, #81531)

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 7.07-1
- fix nicknames & profiles (#82246)
- fix check_device_down (#83780, <pzb@datstacks.com>)
- vlan fixes (<tis@foobar.fi>)
- fix groff macros (#83531, <tsekine@sdri.co.jp>)
- various updated translations
- fix checkpid for multiple pids (#83401)

* Fri Jan 31 2003 Bill Nottingham <notting@redhat.com> 7.06-1
- 802.1Q VLAN support (<tis@foobar.fi>, #82593)
- update translations

* Thu Jan 30 2003 Bill Nottingham <notting@redhat.com> 7.05-1
- fix syntax error in rc.sysinit when there are fsck errors
- fix zh_TW display on console (#82235)

* Wed Jan 15 2003 Bill Nottingham <notting@redhat.com> 7.04-1
- tweak some translatable strings
- fix for rc.sysinit on machines that pass arguments to mingetty
  (<nalin@redhat.com>)

* Tue Jan 14 2003 Bill Nottingham <notting@redhat.com> 7.03-1
- move system font setting sooner (<milan.kerslager@pslib.cz>)
- fix link checking for dhcp, use both ethtool and mii-tool
- fix CJK text on the console, and locale-archive held open
  on shutdown
- IPv6 updates <pekkas@netcore.fi>, <pb@bieringer.de>
- speedup tweaks (<drepper@redhat.com>)
- use glib2 for ppp-watch (#78690, <kisch@mindless.com>)
- add zeroconf route (#81738)
- fix ifup-ppp for dial-on-demand, and onboot (<goeran@uddeborg.pp.se>)
- tweak raidtab parsing, don't worry about not-in-fstab RAID devices
  (#71087, #78467, <aja@mit.edu>)
- don't automatically bring up aliases if 'ONPARENT=no' is set (#78992)
- getkey cleanups/tweaks (#76071, <ben@enchantedforest.org>)
- rework halt_get_remaining (#76831, <michal@harddata.com>)
- ipcalc: fix calculation of /32 addresses (#76646)
- various other tweaks and fixes

* Fri Dec 20 2002 Bill Nottingham <notting@redhat.com> 7.01-1
- %%config(noreplace) inittab

* Tue Dec 17 2002 Nalin Dahyabhai <nalin@redhat.com>
- add a "nofirewire" option to /etc/rc.sysinit, analogous to "nousb"

* Tue Dec 17 2002 Bill Nottingham <notting@redhat.com> 7.00-1
- tweaks for potential GUI bootup
- loop checking for network link state, don't unilterally wait five
  seconds

* Sat Dec 14 2002 Karsten Hopp <karsten@redhat.de> 6.99-1
- remove call to /sbin/update for S/390, too

* Wed Dec 11 2002 Bill Nottingham <notting@redhat.com> 6.98-1
- remove call to /sbin/update
- fix netprofile

* Mon Dec  2 2002 Bill Nottingham <notting@redhat.com> 6.97-1
- IPv6 update (<pekkas@netcore.fi>, <pb@bieringer.de>)
- devlabel support (<Gary_Lerhaupt@Dell.com>)
- do lazy NFS umounts

* Tue Nov 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- correctly remove non-packaged files for mainframe

* Tue Nov 12 2002 Bill Nottingham <notting@redhat.com> 6.96-1
- fix various static-routes brokeness (#74317, #74318, #74320, #76619,
  #75604)
- fix handling of SYSFONTACM in setsysfont (#75662)
- fix lang.csh for CJK (#76908, <ynakai@redhat.com>)
- IPv6 update (<pekkas@netcore.fi>, <pb@bieringer.de>)
- other minor tweaks

* Mon Sep 16 2002 Than Ngo <than@redhat.com>
- owns directory /etc/ppp/peers (bug #74037)

* Wed Sep  4 2002 Bill Nottingham <notting@redhat.com> 6.95-1
- fix syntax error in duplicate route removal section of ifup

* Wed Sep  4 2002 Nalin Dahyabhai <nalin@redhat.com> 6.94-1
- fix syntax error calling unicode_start when SYSFONTACM isn't set

* Mon Sep  2 2002 Bill Nottingham <notting@redhat.com>
- fix calling of unicode_start in lang.{sh,csh}
- ipv6 tweak

* Wed Aug 28 2002 Bill Nottingham <notting@redhat.com>
- don't infinite loop on ifdown
- remove disabling of DMA; this can cause problems
- move swap startup to after LVM (#66588)

* Tue Aug 20 2002 Bill Nottingham <notting@redhat.com>
- don't cycle through eth0-eth9 on dhcp link check (#68127)
- don't retry indefinitely on ppp startup
- activate network profile passed on kernel commandline via netprofile=
- fix iptables invocations again
- translation refresh

* Wed Aug 14 2002 Bill Nottingham <notting@redhat.com>
- fix silly typo in rc.sysinit
- increase timeout for link to 5 seconds (#70545)

* Tue Aug 13 2002 Bill Nottingham <notting@redhat.com>
- require /etc/redhat-release (#68903)
- fix tty2-tty6 (sort of)
- fix iptables invocations (#70807, #71201, #68368)
- other minor tweaks

* Wed Jul 24 2002 Bill Nottingham <notting@redhat.com>
- fix unicode checks in rc.sysinit, lang.{sh,csh} to handle UTF-8@euro

* Tue Jul 16 2002 Bill Nottingham <notting@redhat.com>
- use iptables, not ipchains

* Tue Jul 16 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- /sbin/service: set PATH before calling startup scripts
  HOME and TERM are also set during bootup, but they should not make
  a difference for well-written daemons.

* Mon Jul 15 2002 Bill Nottingham <notting@redhat.com>
- fix boot-time cleanup of /var
- update po files

* Thu Jul 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- /etc/init.d/functions:
  daemon(): avoid starting another bash
  killproc(): avoid starting another bash for the default case
- do not call "insmod -p" before loading the "st" module

* Tue Jul 09 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- allow an option for ups poweroff  #68123
- change grep for ONBOOT=  #63903
- allow building with a cross-compiler  #64362,#64255
- faster check in network-functions:check_default_route()
- better checks for backup files
- drastically reduce the number of consoletype invocations
- do not export "GATEWAY" in network-functions
- code cleanups in rc.sysinit

* Fri Jul 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- rc.sysinit: do not load raid modules unless /etc/raidtab exists
- many cleanups for more consistent shell programming and also
  many smaller speedups within network scripts, no un-necessary sourcing
  of files etc
- nearly re-code /etc/rc.d/rc

* Thu Jun 27 2002 Bill Nottingham <notting@redhat.com>
- a couple minor unicode tweaks in rc.sysinit

* Wed Jun 26 2002 Bill Nottingham <notting@redhat.com>
- move /proc/bus/usb mount, in case USB is in the initrd

* Wed Jun 26 2002 Preston Brown <pbrown@redhat.com>
- don't try to set wireless freq/channel when in Managed mode

* Wed Jun 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- start some sh coding cleanups
- change to /etc/init.d/functions
- eliminate some un-necessary PATH settings
- eliminate some TEXTDOMAIN settings

* Wed Jun 12 2002 Bill Nottingham <notting@redhat.com> 6.78-1
- fix UTF-8 checks

* Wed Jun 05 2002 Than Ngo <than@redhat.com> 6.77-1
- fixed a bug in setting defaultgateway

* Thu May 30 2002 Bill Nottingham <notting@redhat.com> 6.76-1
- call unicode_start in lang.{sh,csh}, setsysfont when necessary

* Tue May 28 2002 Bill Nottingham <notting@redhat.com> 6.75-1
- add check for link for dhcp back in

* Fri Apr 19 2002 Bill Nottingham <notting@redhat.com> 6.67-1
- fix silly cut&paste bug in hdparm settings in initscripts

* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 6.65-1
- Update translations

* Sun Apr 14 2002 Bill Nottingham <notting@redhat.com> 6.64-1
- make sure chatdbg is set before using it (#63448, <Bertil@Askelid.com>)
- allow tweaking of more devices with hdparm (#53511), and
  tweak non-disk devices iff they explicitly have a config file
  for that device (#56575, #63415)
- some translation updates

* Fri Apr 12 2002 Bill Nottingham <notting@redhat.com> 6.63-1
- ipcalc cleanups (#58410)
- quit stripping binaries
- do LVM init after RAID init too (#63238)
- export all locale variables (#56142)
- run sysctl -p after network init as well

* Tue Apr 09 2002 Bill Nottingham <notting@redhat.com> 6.62-1
- delete X/VNC locks on startup (#63035)
- shut up DMA disabling, move it to after ide-scsi (#62873, #62956)
- use full path to /sbin/ifconfig (#59457)
- /sbin/service: change to root directory before staring/stopping;
  also sanitize environment

* Tue Apr 02 2002 Bill Nottingham <notting@redhat.com> 6.61-1
- when disabling DMA, don't use things in /usr

* Thu Mar 28 2002 Bill Nottingham <notting@redhat.com> 6.60-1
- disable DMA on CD-ROMs at bootup

* Wed Mar 27 2002 Bill Nottingham <notting@redhat.com> 6.59-1
- add local hook to halt

* Fri Mar 15 2002 Than Ngo <than@redhat.com> 6.58-1
- fix usernetctl for working with neat

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 6.57-1
- update translations

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 6.56-1
- use nameif for interfaces where we don't agree on HWADDR with the
  config file (<harald@redhat.com>)
- LSB support tweaks

* Tue Mar 12 2002 Mike A. Harris  <mharris@redhat.com> 6.55-1
- Removed process accounting stuff from rc.sysinit and halt scripts as it is
  now handled by the psacct initscript in the psacct package

* Thu Feb 28 2002 Bill Nottingham <notting@redhat.com>
- conflict with older psacct

* Fri Feb 22 2002 Bill Nottingham <notting@redhat.com>
- fix invocation of need_hostname (#58946), a couple other minor tweaks

* Tue Feb 12 2002 Mike A. Harris  <mharris@redhat.com>
- rc.sysinit: changed /var/log/pacct to /var/account/pacct for FHS 2.2 compliance

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com>
- run /bin/setfont, not /usr/bin/setfont (kbd)
- lots-o-random bugfixes/tweaks (see ChangeLog)

* Thu Jan 17 2002 Michael K. Johnson <johnsonm@redhat.com>
- Added support for libredhat-kernel.so.* symlink handling

* Wed Nov  7 2001 Than Ngo <than@redhat.com>
- fix bug in setting netmask on s390/s390x (bug #55421)
  nmbd daemon works now ;-)

* Fri Nov  2 2001 Than Ngo <than@redhat.com>
- fixed typo bug ifup-ippp

* Mon Oct 29 2001 Than Ngo <than@redhat.com>
- fix bug in channel bundling if MSN is missed
- support DEBUG option

* Wed Sep 19 2001 Than Ngo <than@redhat.com>
- don't show user name by DSL connection

* Sat Sep  8 2001 Bill Nottingham <notting@redhat.com>
- don't run hwclock --adjust on a read-only filesystem

* Thu Sep  6 2001 Than Ngo <than@redhat.com>

* update initscripts-s390.patch for s390/s390x

* Wed Sep  5 2001 Bill Nottingham <notting@redhat.com>
- translation updates
- quota and hwclock tweaks (<pbrown@redhat.com>)

* Mon Sep  3 2001 Bill Nottingham <notting@redhat.com>
- fix severe alias problems (#52882)

* Mon Sep  3 2001 Than Ngo <than@redhat.com>
- don't start pppbind if encapsulation is rawip (bug #52491)

* Sun Sep  2 2001 Than Ngo <than@redhat.com>
- add ISDN patches from pekkas@netcore.fi and pb@bieringer.de (bug #52491)
- fix handling of ISDN LSZ Compresssion

* Thu Aug 30 2001 Than Ngo <than@redhat.com>
- po/de.po: fix typo bug, lo instead 1o

* Wed Aug 29 2001 David Sainty <dsainty@redhat.com>
- fix ifdown for multiple dhcpcd interfaces

* Wed Aug 29 2001 Than Ngo <than@redhat.com>
- fix ISDN dial on demand bug
- fix typo bug in network-functions

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com>
- document /etc/sysconfig/authconfig

* Tue Aug 28 2001 Bill Nottingham <notting@redhat.com> 6.31-1
- message un-tweaks (<johnsonm@redhat.com>)
- make getkey more useful, fix some of the autofsck stuff (<johnsonm@redhat.com>)

* Mon Aug 27 2001 Bill Nottingham <notting@redhat.com>
- autofsck support, archive modules/symbol info (<johnsonm@redhat.com>)

* Mon Aug 27 2001 Than Ngo <than@redhat.com>
- fix some typo bugs in ifup-ippp <ubeck@c3pdm.com>

* Fri Aug 24 2001 Bill Nottingham <notting@redhat.com>
- sort output of halt_get_remaining (#52180)
- fix bad translation (#52503)

* Wed Aug 22 2001 Bill Nottingham <notting@redhat.com>
- fix ifup-wireless (#52135)

* Wed Aug 22 2001 Than Ngo <than@redhat.com>
- fix return code of isdnctrl (bug #52225)

* Tue Aug 21 2001 Than Ngo <than@redhat.com>
- fix Bringing up isdn device again. It works now correct.

* Tue Aug 21 2001 Than Ngo <than@redhat.com>
- fix shutdown/Bringing up isdn device

* Mon Aug 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix syntax error in lang.csh
- set codeset by echoing to /dev/tty instead of /proc/self/fd/15

* Sun Aug 19 2001 Bill Nottingham <notting@redhat.com>
- fix a broken call to check_device_down
- make all loopback addresses have host scope, not global scope.
  Fixes #49374, possibly others

* Wed Aug 15 2001 Bill Nottingham <notting@redhat.com>
- add is_available() network function, use it; cleans up ugly modprobe
  error messages
- update translation info
- fix #51787

* Wed Aug 15 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- adjust s390 patch
- fix up ifup-ctc and mkkerneldoth.s390 (both are s390 specific)

* Mon Aug 13 2001 Yukihiro Nakai <ynakai@redhat.com>
- don't display Chinese Korean if we aren't on a pty

* Sat Aug 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- adjust s390 patches to current sources

* Fri Aug 10 2001 Bill Nottingham <notting@redhat.com>
- use GDM_LANG if it's set in lang.sh/lang.csh (#51432, <otaylor@redhat.com>)

* Fri Aug 10 2001 Than Ngo <than@redhat.com>
- don't set MSN if it' empty (it's now optional)
- don't give login name as a cmdline-option (Bug #23066)
- remove peer device file if ppp connection is down
- fix channel bundling

* Thu Aug  9 2001 Bill Nottingham <notting@redhat.com>
- require SysVinit (#51335)

* Wed Aug  8 2001 Bill Nottingham <notting@redhat.com>
- tweak raittab grep slightly (#51231)
- allow resetting of default route for DHCP addresses (#48994)
- save resolv.conf in ifup-ppp for restoration by ifdown-post (#50759)
- when munging firewall rules for dns, only allow dest ports 1025-65535 (#44038, #40833)
- allow shell characters in ppp names (#43719)
- allow setting DHCP arguments, just kill dhcpcd instead of using -k (#46492)
- behave sanely if ifup called when dhcpcd is running (#49392, #51038)

* Mon Aug  6 2001 Bill Nottingham <notting@redhat.com>
- honor HOTPLUG=no if running under hotplug (#47483)
- use awk, not grep, for modprobe -c checks (#49616)
- don't print ugly messages for the case where the device doesn't exist,
  and there is no alias (i.e., PCMCIA ONBOOT=yes (#various))
- run kbdconfig in /.unconfigured mode (#43941)
- use a bigger buffer size argument to dmesg (#44024)
- detach loopback devices on shutdown (#43919, #45826)

* Thu Aug  2 2001 Bill Nottingham <notting@redhat.com>
- fix halt_get_remaining() (#50720)

* Tue Jul 31 2001 Bill Nottingham <notting@redhat.com>
- mount all FS types r/o at halt (#50461)
- don't use mii-tool at all (#various)

* Thu Jul 26 2001 Bill Nottingham <notting@redhat.com>
- don't use kbd commands in setsysfont now that we've switched back to
  console-tools (#50075)
- sleep in check_link_down; some devices require it
- only bring link down if check_link_down fails

* Wed Jul 25 2001 Bill Nottingham <notting@redhat.com>
- set link up before checking with mii-tool (#49949)

* Tue Jul 24 2001 Bill Nottingham <notting@redhat.com>
- update netdev stuff to use _netdev
- IPv6 updates (<pekkas@netcore.fi>)
- fix downing of devices with static IPs (#49777, #49783)
- put ifcfg-lo back in the package

* Fri Jul 20 2001 Preston Brown <pbrown@redhat.com> 6.06
- updates for quota

* Tue Jul 17 2001 Bill Nottingham <notting@redhat.com>
- own some more directories
- use -O nonetdev, require mount package that understands this
- fix do_netreport when called as non-root
- remove ip addresses from interfaces on ifdown
- oops, fix ifup/ifdown

* Mon Jul 16 2001 Than Ngo <than@redhat.com>
- fix country_code for ISDN

* Mon Jul  9 2001 Bill Nottingham <notting@redhat.com>
- fix '--check'
- prereq sh-utils (#43065)
- fix some invocations of reboot/halt (#45966)
- fix typo in ifup-wireless
- don't muck with /etc/issue each boot
- big IPv6 update (<pekkas@netcore.fi>)

* Fri Jul  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add new directories required by new network tool

* Thu Jul 05 2001 Karsten Hopp <karsten@redhat.de>
- disable hwclock on S390 (no such executable)
- Fix up kernel versioning on binary-only modules (S390)
- don't use newt scripts on S390 console

* Sun Jul 01 2001 Trond Eivind Glomsrød <teg@redhat.com>
- reenable pump, but make sure dhcpcd is the default. This
  way, upgrades of systems without dhcpcd has a better chance at
  working.

* Thu Jun 28 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Disable pump completely

* Wed Jun 27 2001 Than Ngo <than@redhat.com>
- fix pap/chap authentication for syncppp
- support ippp options

* Mon Jun 25 2001 Bill Nottingham <notting@redhat.com>
- add ifup-wireless

* Fri Jun 22 2001 Than Ngo <than@redhat.com>
- add support xDSL

* Thu Jun 21 2001 Bill Nottingham <notting@redhat.com>
- more networking script fixes (#45364)
- add stuff for unmounting /initrd

* Thu Jun 21 2001 Than Ngo <than@redhat.com>
- add support ISDN

* Wed Jun 20 2001 Bill Nottingham <notting@redhat.com>
- fix extremely broken new network scripts

* Wed Jun 20 2001 Bill Nottingham <notting@redhat.com>
- bump version to 5.89
- make it build

* Thu May 17 2001 Bill Nottingham <notting@redhat.com>
- don't run ifup ppp0 if ppp-watch gets SIGINT (#40585, ak@cave.hop.stu.neva.ru)
- fix do_netreport (#37716, #39603 <crlf@aeiou.pt>)

* Wed May 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- copyright: GPL -> license: GPL
- fix a syntax error in lang.csh
- skip commented-out i18n configuration lines in lang.csh

* Fri May 11 2001 Preston Brown <pbrown@redhat.com>
- new network-scripts infrastructure; ifcfg-lo moved to /etc/sysconfig/networking

* Wed May  2 2001 Bernhard Rosenkraenzer <bero@redhat.com> 5.86-1
- support kbd in setsysfont
- bzip2 source

* Wed Apr 25 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add further s390 changes:
  - ifup-iucv
  - mkkerneldoth.s390

* Tue Apr 24 2001 Than Ngo <than@redhat.com>
- add shutdown UPS into halt (bug #34312)

* Sat Apr  7 2001 Preston Brown <pbrown@redhat.com>
- broke out kernel.h updater from rc.sysinit into /sbin/mkkerneldoth

* Fri Apr  6 2001 Bill Nottingham <notting@redhat.com>
- be a little more careful in do_netreport (#34933)

* Tue Apr  3 2001 Bill Nottingham <notting@redhat.com>
- set umask explicitly to 022 in /etc/init.d/functions

* Mon Apr  2 2001 Bill Nottingham <notting@redhat.com>
- fix segfault in usernetctl (#34353)

* Mon Mar 26 2001 Bill Nottingham <notting@redhat.com>
- don't print errors in /etc/init.d/network if kernel.hotplug doesn't exist

* Thu Mar 22 2001 Erik Troan <ewt@redhat.com>
- take advantage of new swapon behaviors

* Wed Mar 14 2001 Bill Nottingham <notting@redhat.com>
- add cipe interfaces last (#31597)

* Tue Mar 13 2001 Bill Nottingham <notting@redhat.com>
- fix typo in ifup (#31627)
- update translation source

* Tue Mar 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix typo in rc.sysinit
- fix ifup-routes not setting DEVICE properly

* Mon Mar 12 2001 Preston Brown <pbrown@redhat.com>
- Work properly with new quota utilities

* Mon Mar  5 2001 Bill Nottingham <notting@redhat.com>
- IPv6 fixes (#30506)
- make static-routes handling more sane and consistent (#29500, #29549)
- handle multiple USB controllers *correctly*

* Wed Feb 28 2001 Nalin Dahyabhai <nalin@redhat.com>
- usernetctl, ppp-watch: cleanups
- netreport: use O_NOFOLLOW
- ifup-ppp: let ppp-watch watch over demand-dialed connections (#28927)

* Tue Feb 27 2001 Bill Nottingham <notting@redhat.com>
- don't run isapnp on isapnp-enabled 2.4 kernels (part of #29450)
- disable hotplug during network initscript
- don't munge wireless keys in ifup; that will be done with the
  PCMCIA wireless stuff
- run sndconfig --mungepnp for non-native-isapnp soundcards
- don't explicitly kill things in init.d/single, init will do it
- don't explicitly load usb-storage; mount the usbdevfs before initializing
  host controller modules

* Wed Feb 21 2001 Bill Nottingham <notting@redhat.com>
- initialize multiple USB controllers if necessary

* Wed Feb 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- close extra file descriptors before exec()ing commands in initlog

* Mon Feb 19 2001 Bill Nottingham <notting@redhat.com>
- fix some substitions in init.d/functions (fixes various killproc issues)
- make sure ipv6 module alias is available if configured
- fix initlog segfaults in popt when called with bogus stuff (#28140)

* Thu Feb 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- make pidofproc() and killproc() try to use the PID associated with the full
  pathname first before killing the daemon by its basename (for daemons that
  share the same basename, i.e. "master" in postfix and cyrus-imapd) (#19016)
- fix status() as well

* Wed Feb 14 2001 Bill Nottingham <notting@redhat.com>
- fix init.d/single to work around possible kernel problem

* Tue Feb 13 2001 Bill Nottingham <notting@redhat.com>
- fix unmounting of loopback stuff (#26439, #14672)

* Mon Feb 12 2001 Bill Nottingham <notting@redhat.com>
- fix ifup-post so that it will work right when not called from ifup

* Sat Feb 10 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add all save changes for s390 s390x that won't break anything
  patches are from Oliver Paukstadt @ millenux.com

* Fri Feb  9 2001 Bill Nottingham <notting@redhat.com>
- muck with the font in lang.csh/lang.sh, but don't spit out errors (#26903)

* Wed Feb  7 2001 Bill Nottingham <notting@redhat.com>
- ipv6 sync ups (#26502, #25775)
- fix hangs at shutdown (#25744)
- fix ifup-ppp (#26323)

* Tue Feb  6 2001 Bill Nottingham <notting@redhat.com>
- modify firewall on ifup to allow any new DNS servers through (#25951)
- don't muck with the font in lang.csh/lang.sh (#26349)
- don't display Japanese if we aren't on a pty (#25041)
- load ide-scsi if passed on /proc/cmdline

* Mon Feb  5 2001 Trond Eivind Glomsrød <teg@redhat.com>
- i18n updates

* Fri Feb  2 2001 Bill Nottingham <notting@redhat.com>
- actually *ship* the ipv6 (and plusb) files

* Thu Feb  1 2001 Trond Eivind Glomsrød <teg@redhat.com>
- i18n updates

* Tue Jan 30 2001 Bill Nottingham <notting@redhat.com>
- various init.d/functions cleanups (#10761, from <mjt@tls.msk.ru>)
- in daemon(), only look at pidfile to determine if process is running
  (#17244, others)
- ifup-ppp enhancements (#17388, from <ayn2@cornell.edu>)
- ipv6 support (#23576, originally by Peter Bieringer <pb@bieringer.de>)
- lots of other minor fixes (see ChangeLog)

* Mon Jan 29 2001 Bill Nottingham <notting@redhat.com>
- add plusb support (#18892, patch from <eric.ayers@compgen.com>)
- don't ignore RETRYTIMEOUT when we never connect (#14071, patch from
  <ak@cave.hop.stu.neva.ru>)

* Wed Jan 24 2001 Bill Nottingham <notting@redhat.com>
- quiet LVM setup (#24841)
- fix inability to shutdown cleanly (#24889)

* Tue Jan 23 2001 Bill Nottingham <notting@redhat.com>
- new i18n mechanism

* Tue Jan 23 2001 Matt Wilson <msw@redhat.com>
- fixed typo in init.d/network - missing | in pipeline

* Mon Jan 22 2001 Bill Nottingham <notting@redhat.com>
- do LVM setup through normal initscripts mechanisms
- ignore backup files in /etc/sysconfig/network-scripts
- lots of .po file updates

* Tue Jan  2 2001 Bill Nottingham <notting@redhat.com>
- initial i18n support - originally from Conectiva

* Mon Dec 11 2000 Bill Nottingham <notting@redhat.com>
- only load sound if persistent DMA buffers are necessary
- fix lots of bugs: #18619, #21187, #21283, #12097
- integrate MAXFAIL option for ppp-watch
- don't load keymaps/fonts on a serial console

* Tue Nov 21 2000 Karsten Hopp <karsten@redhat.de>
- changed hdparm section in rc.sysinit to allow different
  parameters for each disk (if needed) by copying
  /etc/sysconfig/harddisks to /etc/sysconfig/harddiskhda (hdb,hdc..)
- fix RFE #20967

* Tue Oct 31 2000 Than Ngo <than@redhat.com>
- fix the adding default route if GATEWAY=0.0.0.0

* Tue Oct 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- handle "gw x.x.x.x" as the last pair of flags in ifup-routes (#18804)
- fix top-level makefile install target
- make usernetctl just fall-through if getuid() == 0

* Sun Sep  3 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- /etc/init.d is already provided by chkconfig

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- set "holdoff ${RETRYTIMEOUT} ktune" for demand-dialed PPP links

* Tue Aug 22 2000 Bill Nottingham <notting@redhat.com>
- update documentation (#15475)

* Tue Aug 22 2000 Than Ngo <than@redhat.de>
- add KDE2 support to prefdm

* Mon Aug 21 2000 Bill Nottingham <notting@redhat.com>
- add usleep after kill -KILL in pidofproc, works around lockd issues (#14847)
- add some fallback logic to prefdm (#16464)

* Fri Aug 18 2000 Bill Nottingham <notting@redhat.com>
- don't load usb drivers if they're compiled statically
- don't call ifdown-post twice for ppp (#15285)

* Wed Aug 16 2000 Bill Nottingham <notting@redhat.com>
- fix /boot/kernel.h generation (#16236, #16250)

* Tue Aug 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- be more careful about creating files in netreport (#16164)

* Fri Aug 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- move documentation for the DEMAND and IDLETIMEOUT values to the right
  section of sysconfig.txt

* Wed Aug  9 2000 Bill Nottingham <notting@redhat.com>
- load agpgart if necessary (hack)
- fix /boot/kernel.h stuff (jakub)

* Mon Aug  7 2000 Bill Nottingham <notting@redhat.com>
- remove console-tools requirement
- in netfs, start portmap if needed
- cosmetic cleanups, minor tweaks
- don't probe USB controllers

* Mon Aug  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix demand-dialing support for PPP devices
- change updetach back to nodetach

* Sun Aug  6 2000 Bill Nottingham <notting@redhat.com>
- add RETRYCONNECT option for ifcfg-pppX files (kenn@linux.ie)

* Wed Jul 26 2000 Bill Nottingham <notting@redhat.com>
- fix unclean shutdown

* Tue Jul 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- s/nill/null/g

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- unmount usb filesystem on halt
- run /sbin/ifup-pre-local if it exists

* Tue Jul 18 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add "nousb" command line parameter
- fix some warnings when mounting /proc/bus/usb

* Sat Jul 15 2000 Matt Wilson <msw@redhat.com>
- kill all the PreTransaction stuff
- directory ownership cleanups, add more LSB symlinks
- move all the stuff back in to /etc/rc.d/

* Thu Jul 13 2000 Bill Nottingham <notting@redhat.com>
- fix == tests in rc.sysinit
- more %%pretrans tweaks

* Thu Jul 13 2000 Jeff Johnson <jbj@redhat.com>
- test if /etc/rc.d is a symlink already in pre-transaction syscalls.

* Tue Jul 11 2000 Bill Nottingham <notting@redhat.com>
- implement the %%pre with RPM Magic(tm)

* Sat Jul  8 2000 Bill Nottingham <notting@redhat.com>
- fix it to not follow /etc/rc.d

* Fri Jul  7 2000 Bill Nottingham <notting@redhat.com>
- fix %%pre, again

* Thu Jul  6 2000 Bill Nottingham <notting@redhat.com>
- tweak %%pre back to a mv (rpm is fun!)
- do USB initialization before fsck, so keyboard works if it fails

* Mon Jul  3 2000 Bill Nottingham <notting@redhat.com>
- rebuild; allow 'fastboot' kernel command line option to skip fsck

* Mon Jul 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix demand-dialing with PPP

* Sun Jul 02 2000 Trond Eivind Glomsrød <teg@redhat.com>
- don't use tail

* Wed Jun 28 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add support for USB controllers and HID devices
  (mice, keyboards)

* Tue Jun 27 2000 Trond Eivind Glomsrød <teg@redhat.com>
- add support for EIDE optimization

* Mon Jun 26 2000 Bill Nottingham <notting@redhat.com>
- tweak %%pre

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- noreplace for adjtime file

* Fri Jun 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- ifup-ppp: add hooks for demand-dialing PPP
- functions: use basename of process when looking for its PID file

* Thu Jun 15 2000 Bill Nottingham <notting@redhat.com>
- move from /etc/rc.d/init.d -> /etc/init.d

* Tue Jun 13 2000 Bill Nottingham <notting@redhat.com>
- set soft limit, not hard, in daemon function
- /var/shm -> /dev/shm

* Thu Jun 08 2000 Preston Brown <pbrown@redhat.com>
- use dhcpcd if pump fails.
- use depmod -A (faster)

* Sun Jun  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- add autologin support to prefdm

* Thu Jun  1 2000 Bill Nottingham <notting@redhat.com>
- random networking fixes (alias routes, others)
- conf.modules -> modules.conf

* Thu May 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix incorrect grep invocation in rc.sysinit (bug #11267)

* Wed Apr 19 2000 Bill Nottingham <notting@redhat.com>
- fix lang.csh, again (oops)
- use /poweroff, /halt to determine whether to poweroff

* Fri Apr 14 2000 Bill Nottingham <notting@redhat.com>
- fix testing of RESOLV_MODS (which shouldn't be used anyways)

* Tue Apr 04 2000 Ngo Than <than@redhat.de>
- fix overwrite problem of resolv.conf on ippp/ppp/slip connections

* Mon Apr  3 2000 Bill Nottingham <notting@redhat.com>
- fix typo in functions file
- explicitly set --localtime when calling hwclock if necessary

* Fri Mar 31 2000 Bill Nottingham <notting@redhat.com>
- fix typo in /etc/rc.d/init.d/network that broke linuxconf (#10472)

* Mon Mar 27 2000 Bill Nottingham <notting@redhat.com>
- remove compatibility chkconfig links
- run 'netfs stop' on 'network stop' if necessary

* Tue Mar 21 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Mount /var/shm if required (2.3.99, 2.4)

* Mon Mar 20 2000 Bill Nottingham <notting@redhat.com>
- don't create resolv.conf 0600
- don't run ps as much (speed issues)
- allow setting of MTU
- other minor fixes

* Sun Mar 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Start devfsd if installed and needed (Kernel 2.4...)

* Wed Mar  8 2000 Bill Nottingham <notting@redhat.com>
- check that network devices are up before bringing them down

* Wed Mar  8 2000 Jakub Jelinek <jakub@redhat.com>
- update sysconfig.txt

* Tue Mar  7 2000 Bill Nottingham <notting@redhat.com>
- rerun sysctl on network start (for restarts)

* Mon Feb 28 2000 Bill Nottingham <notting@redhat.com>
- don't read commented raid devices

* Mon Feb 21 2000 Bill Nottingham <notting@redhat.com>
- fix typo in resolv.conf munging

* Thu Feb 17 2000 Bill Nottingham <notting@redhat.com>
- sanitize repair prompt
- initial support for isdn-config stuff

* Mon Feb 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- add which as a package dependency (bug #9416)

* Tue Feb  8 2000 Bill Nottingham <notting@redhat.com>
- fixes for sound module loading

* Mon Feb  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- check that LC_ALL/LINGUAS and LANG are set before referencing them in lang.csh
- fix check for /var/*/news, work around for bug #9140

* Fri Feb  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bug #9102

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- if LC_ALL/LINGUAS == LANG, don't set them

* Wed Feb  2 2000 Bill Nottingham <notting@redhat.com>
- fix problems with linuxconf static routes

* Tue Feb  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- shvar cleaning
- fix wrong default route ip in network-functions

* Mon Jan 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- attempt to restore default route if PPP takes it over
- man page fix for ipcalc
- shvar cleaning
- automate maintaining /boot/System.map symlinks

* Mon Jan 31 2000 Bill Nottingham <notting@redhat.com>
- fix hanging ppp-watch
- fix issues with cleaning of /var/{run,lock}

* Fri Jan 21 2000 Bill Nottingham <notting@redhat.com>
- fix pidof calls in pidofproc

* Wed Jan 19 2000 Bill Nottingham <notting@redhat.com>
- fix ifup-ipx, don't munge resolv.conf if $DNS1 is already in it

* Thu Jan 13 2000 Bill Nottingham <notting@redhat.com>
- link popt statically

* Mon Jan 10 2000 Bill Nottingham <notting@redhat.com>
- don't try to umount /loopfs

* Mon Dec 27 1999 Bill Nottingham <notting@redhat.com>
- switch to using sysctl

* Mon Dec 13 1999 Bill Nottingham <notting@redhat.com>
- umount /proc *after* trying to turn off raid

* Mon Dec 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- improvements in clone device handling
- better signal handling in ppp-watch
- yet another attempt to fix those rare PAP/CHAP problems

* Sun Nov 28 1999 Bill Nottingham <notting@redhat.com>
- impressive. Three new features, three new bugs.

* Mon Nov 22 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix more possible failed CHAP authentication (with chat scripts)
- fix ppp default route problem
- added ppp-watch man page, fixed usernetctl man page
- make ifup-ppp work again when called from netcfg and linuxconf
- try to keep ppp-watch from filling up logs by respawning pppd too fast
- handle all linuxconf-style alias files with linuxconf

* Mon Nov 22 1999 Bill Nottingham <notting@redhat.com>
- load mixer settings for monolithic sound
- man page for ppp-watch
- add ARP variable for ifup
- some i18n fixes

* Wed Nov 10 1999 Bill Nottingham <notting@redhat.com>
- control stop-a separately from sysrq

* Mon Nov 08 1999 Michael K. Johnson <johnsonm@redhat.com>
- fix some failed CHAP authentication
- fix extremely unlikely, but slightly possible kill-random-process
  bug in ppp-watch
- allow DNS{1,2} in any ifcfg-* file, not just PPP, and
  add nameserver entries, don't just replace them
- don't use /tmp/confirm, use /var/run/confirm instead

* Tue Nov  2 1999 Bill Nottingham <notting@redhat.com>
- fix lang.csh /tmp race oops

* Wed Oct 27 1999 Bill Nottingham <notting@redhat.com>
- we now ship hwclock on alpha.

* Mon Oct 25 1999 Jakub Jelinek <jakub@redhat.com>
- fix check for serial console, don't use -C argument to fsck
  on serial console.

* Mon Oct 18 1999 Bill Nottingham <notting@redhat.com>
- do something useful with linuxconf 'any' static routes.

* Tue Oct 12 1999 Matt Wilson <msw@redhat.com>
- added patch from Owen to source i18n configuration before starting prefdm

* Mon Oct 11 1999 Bill Nottingham <notting@redhat.com>
- support for linuxconf alias files
- add support for Jensen clocks.

* Tue Oct  5 1999 Bill Nottingham <notting@redhat.com>
- assorted brown paper bag fixes
- check for programs/files before executing/sourcing them
- control stop-a like magic sysrq

* Thu Sep 30 1999 Bill Nottingham <notting@redhat.com>
- req. e2fsprogs >= 1.15

* Fri Sep 24 1999 Bill Nottingham <notting@redhat.com>
- munge C locale definitions to en_US
- use fsck's completion bar

* Thu Sep 23 1999 Michael K. Johnson <johnsonm@redhat.com>
- ppp-watch now always kills pppd pgrp to make sure dialers are dead,
  and tries to hang up the modem

* Tue Sep 21 1999 Bill Nottingham <notting@redhat.com>
- add a DEFRAG_IPV4 option

* Mon Sep 20 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed to more modern defaults for PPP connections

* Mon Sep 20 1999 Bill Nottingham <notting@redhat.com>
- kill processes for umount in halt, too.
- fixes to remove /usr dependencies

* Fri Sep 17 1999 Bill Nottingham <notting@redhat.com>
- load/save mixer settings in rc.sysinit, halt

* Mon Sep 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- add --remotename option to wvdial code
- make sure we do not have an earlier version of wvdial that doesn't
  know how handle --remotename
- make ppp-watch background itself after 30 seconds even if
  connection does not come up, at boot time only, so that a
  non-functional PPP connection cannot hang boot.

* Sun Sep 12 1999 Bill Nottingham <notting@redhat.com>
- a couple of /bin/sh -> /bin/bash fixes
- fix swapoff silliness

* Fri Sep 10 1999 Bill Nottingham <notting@redhat.com>
- chkconfig --del in %%preun, not %%postun
- use killall5 in halt
- swapoff non-/etc/fstab swap

* Wed Sep 08 1999 Michael K. Johnson <johnsonm@redhat.com>
- ifdown now synchronous (modulo timeouts)
- several unrelated cleanups, primarily in ifdown

* Tue Sep  7 1999 Bill Nottingham <notting@redhat.com>
- add an 'unconfigure' sort of thing

* Mon Sep 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- added ppp-watch to make "ifup ppp*" synchronous

* Fri Sep  3 1999 Bill Nottingham <notting@redhat.com>
- require lsof

* Wed Sep  1 1999 Bill Nottingham <notting@redhat.com>
- add interactive prompt

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- disable magic sysrq by default

* Mon Aug 30 1999 Bill Nottingham <notting@redhat.com>
- new NFS unmounting from Bill Rugolsky <rugolsky@ead.dsa.com>
- fix ifup-sl/dip confusion
- more raid startup cleanup
- make utmp group 22

* Fri Aug 20 1999 Bill Nottingham <notting@redhat.com>
- pass hostname to pump
- add lang.csh

* Thu Aug 19 1999 Bill Nottingham <notting@redhat.com>
- more wvdial updates
- fix a *stupid* bug in process reading

* Fri Aug 13 1999 Bill Nottingham <notting@redhat.com>
- add new /boot/kernel.h boot kernel version file
- new RAID startup

* Fri Aug 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- use new linkname argument to pppd to make if{up,down}-ppp
  reliable -- requires ppp-2.3.9 or higher

* Mon Aug  2 1999 Bill Nottingham <notting@redhat.com>
- fix typo.
- add 'make check'

* Wed Jul 28 1999 Michael K. Johnson <johnsonm@redhat.com>
- simple wvdial support for ppp connections

* Mon Jul 26 1999 Bill Nottingham <notting@redhat.com>
- stability fixes for initlog
- initlog now has a config file
- add alias speedup from dharris@drh.net
- move netfs links
- usleep updates

* Thu Jul  8 1999 Bill Nottingham <notting@redhat.com>
- remove timeconfig dependency
- i18n fixes from nkbj@image.dk
- move inputrc to setup package

* Tue Jul  6 1999 Bill Nottingham <notting@redhat.com>
- fix killall links, some syntax errors

* Fri Jun 25 1999 Bill Nottingham <notting@redhat.com>
- don't make module-info, System.map links
- handle utmpx/wtmpx
- fix lots of bugs in 4.21 release :)

* Thu Jun 17 1999 Bill Nottingham <notting@redhat.com>
- set clock as soon as possible
- use INITLOG_ARGS everywhere
- other random fixes in networking

* Mon Jun 14 1999 Bill Nottingham <notting@redhat.com>
- oops, don't create /var/run/utmp and then remove it.
- stomp RAID bugs flat. Sort of.

* Mon May 24 1999 Bill Nottingham <notting@redhat.com>
- clean out /var better
- let everyone read /var/run/ppp*.dev
- fix network startup so it doesn't depend on /usr

* Tue May 11 1999 Bill Nottingham <notting@redhat.com>
- various fixes to rc.sysinit
- fix raid startup
- allow for multi-processor /etc/issues

* Sun Apr 18 1999 Matt Wilson <msw@redhat.com>
- fixed typo - "Determing" to "Determining"

* Fri Apr 16 1999 Preston Brown <pbrown@redhat.com>
- updated inputrc so that home/end/del work on console, not just X

* Thu Apr 08 1999 Bill Nottingham <notting@redhat.com>
- fix more logic in initlog
- fix for kernel versions in ifup-aliases
- log to /var/log/boot.log

* Wed Apr 07 1999 Bill Nottingham <notting@redhat.com>
- fix daemon() function so you can specify pid to look for

* Wed Apr 07 1999 Erik Troan <ewt@redhat.com>
- changed utmp,wtmp to be group writeable and owned by group utmp

* Tue Apr 06 1999 Bill Nottingham <notting@redhat.com>
- fix loading of consolefonts/keymaps
- three changelogs. three developers. one day. Woohoo!

* Tue Apr 06 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed ifup-ipx mix-up over . and _

* Tue Apr 06 1999 Erik Troan <ewt@redhat.com>
- run /sbin/ifup-local after bringing up an interface (if that file exists)

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- load keymaps & console font early
- fixes for channel bonding, strange messages with non-boot network interfaces

* Sat Mar 27 1999 Cristian Gafton <gafton@redhat.com>
- added sysvinitfiles as a documenattaion file

* Fri Mar 26 1999 Bill Nottingham <notting@redhat.com>
- nfsfs -> netfs

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- don't source /etc/sysconfig/init if $BOOTUP is already set

* Fri Mar 19 1999 Bill Nottingham <notting@redhat.com>
- don't run linuxconf if /usr isn't mounted
- set macaddr before bootp
- zero in the /var/run/utmpx file (gafton)
- don't set hostname on ppp/slip (kills X)

* Wed Mar 17 1999 Bill Nottingham <notting@redhat.com>
- exit ifup if pump fails
- fix stupid errors in reading commands from subprocess

* Tue Mar 16 1999 Bill Nottingham <notting@redhat.com>
- fix ROFS logging
- make fsck produce more happy output
- fix killproc logic

* Mon Mar 15 1999 Bill Nottingham <notting@redhat.com>
- doc updates
- support for SYSFONTACM, other console-tools stuff
- add net route for interface if it isn't there.
- fix for a bash/bash2 issue

* Mon Mar 15 1999 Michael K. Johnson <johnsonm@redhat.com>
- pam_console lockfile cleanup added to rc.sysinit

* Sun Mar 14 1999 Bill Nottingham <notting@redhat.com>
- fixes in functions for 'action'
- fixes for pump

* Wed Mar 10 1999 Bill Nottingham <notting@redhat.com>
- Mmm. Must always remove debugging code. before release. *thwap*
- pump support
- mount -a after mount -a -t nfs

* Thu Feb 25 1999 Bill Nottingham <notting@redhat.com>
- put preferred support back in

* Thu Feb 18 1999 Bill Nottingham <notting@redhat.com>
- fix single-user mode (source functions, close if)

* Wed Feb 10 1999 Bill Nottingham <notting@redhat.com>
- turn off xdm in runlevel 5 (now a separate service)

* Thu Feb  4 1999 Bill Nottingham <notting@redhat.com>
- bugfixes (ifup-ppp, kill -TERM, force fsck, hwclock --adjust, setsysfont)
- add initlog support. Now everything is logged (and bootup looks different)

* Thu Nov 12 1998 Preston Brown <pbrown@redhat.com>
- halt now passed the '-i' flag so that network interfaces disabled

* Tue Nov 10 1998 Michael K. Johnson <johnsonm@redhat.com>
- handle new linuxconf output for ipaliases

* Thu Oct 15 1998 Erik Troan <ewt@redhat.com>
- fixed raid start stuff
- added raidstop to halt

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- handle LC_ALL

* Mon Oct 12 1998 Preston Brown <pbrown@redhat.com>
- adjusted setsysfont to always run setfont, even if only w/default font

* Tue Oct 06 1998 Cristian Gafton <gafton@redhat.com>
- rc.sysvinit should be working with all kernel versions now
- requires e2fsprogs (for fsck)
- set INPUTRC and LESSCHARSET on linux-lat

* Wed Sep 16 1998 Jeff Johnson <jbj@redhat.com>
- /etc/rc.d/rc: don't run /etc/rc.d/rcN.d/[KS]??foo.{rpmsave,rpmorig} scripts.
- /etc/rc.d/rc.sysinit: raid startup (Nigel.Metheringham@theplanet.net).
- /sbin/setsysfont: permit unicode fonts.

* Mon Aug 17 1998 Erik Troan <ewt@redhat.com>
- don't add 'Red Hat Linux' to /etc/issue; use /etc/redhat-release as is

* Sun Aug 16 1998 Jeff Johnson <jbj@redhat.com>
- paranoia improvements to .rhkmvtag
- if psacct with /sbin/accton, than turn off accounting

* Tue Jul  7 1998 Jeff Johnson <jbj@redhat.com>
- start/stop run levels changed.
- ipx_configure/ipx_internal_net moved to /sbin.

* Wed Jul 01 1998 Erik Troan <ewt@redhat.com>
- usernetctl didn't understand "" around USERCTL attribute

* Wed Jul  1 1998 Jeff Johnson <jbj@redhat.com>
- Use /proc/version to find preferred modules.
- Numerous buglets fixed.

* Sun Jun 07 1998 Erik Troan <ewt@redhat.com>
- rc.sysinit looks for bootfile= as well as BOOT_IMAGE to set
  /lib/modules/preferred symlink

* Mon Jun 01 1998 Erik Troan <ewt@redhat.com>
- ipcalc should *never* have been setgid anything
- depmod isn't run properly for non-serial numbered kernels

* Wed May 06 1998 Donnie Barnes <djb@redhat.com>
- added system font and language setting

* Mon May 04 1998 Michael K. Johnson <johnsonm@redhat.com>
- Added missing files to packagelist.

* Sat May 02 1998 Michael K. Johnson <johnsonm@redhat.com>
- Added lots of linuxconf support.  Should still work on systems that
  do not have linuxconf installed, but linuxconf gives enhanced support.
- In concert with linuxconf, added IPX support.  Updated docs to reflect it.

* Fri May 01 1998 Erik Troan <ewt@redhat.com>
- rc.sysinit uses preferred directory

* Sun Apr 05 1998 Erik Troan <ewt@redhat.com>
- updated rc.sysinit to deal with kernel versions with release numbers

* Sun Mar 22 1998 Erik Troan <ewt@redhat.com>
- use ipcalc to calculate the netmask if one isn't specified

* Tue Mar 10 1998 Erik Troan <ewt@redhat.com>
- added and made use of ipcalc

* Tue Mar 10 1998 Erik Troan <ewt@redhat.com>
- removed unnecessary dhcp log from /tmp

* Mon Mar 09 1998 Erik Troan <ewt@redhat.com>
- if bootpc fails, take down the device

* Mon Mar 09 1998 Erik Troan <ewt@redhat.com>
- added check for mktemp failure

* Thu Feb 05 1998 Erik Troan <ewt@redhat.com>
- fixed support for user manageable cloned devices

* Mon Jan 12 1998 Michael K. Johnson <johnsonm@redhat.com>
- /sbin/ isn't always in $PATH, so call /sbin/route in ifup-routes

* Wed Dec 31 1997 Erik Troan <ewt@redhat.com>
- touch /var/lock/subsys/kerneld after cleaning out /var/lock/subsys
- the logic for when  /var/lock/subsys/kerneld is touched was backwards

* Tue Dec 30 1997 Erik Troan <ewt@redhat.com>
- tried to get /proc stuff right one more time (uses -t nonfs,proc now)
- added support for /fsckoptions
- changed 'yse' to 'yes' in KERNELD= line

* Tue Dec 09 1997 Erik Troan <ewt@redhat.com>
- set domainname to "" if none is specified in /etc/sysconfig/network
- fix /proc mounting to get it in /etc/mtab

* Mon Dec 08 1997 Michael K. Johnson <johnsonm@redhat.com>
- fixed inheritance for clone devices

* Fri Nov 07 1997 Erik Troan <ewt@redhat.com>
- added sound support to rc.sysinit

* Fri Nov 07 1997 Michael K. Johnson <johnsonm@redhat.com>
- Added missing "then" clause

* Thu Nov 06 1997 Michael K. Johnson <johnsonm@redhat.com>
- Fixed DEBUG option in ifup-ppp
- Fixed PPP persistence
- Only change IP forwarding if necessary

* Tue Oct 28 1997 Donnie Barnes <djb@redhat.com>
- removed the skeleton init script
- added the ability to 'nice' daemons

* Tue Oct 28 1997 Erik Troan <ewt@redhat.com>
- touch /var/lock/subsys/kerneld if it's running, and after mounting /var
- applied dhcp fix

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- added status|restart to init scripts

* Thu Oct 23 1997 Michael K. Johnson <johnsonm@redhat.com>
- touch random seed file before chmod'ing it.

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>
- run domainname if NISDOMAIN is set

* Wed Oct 15 1997 Michael K. Johnson <johnsonm@redhat.com>
- Make the random seed file mode 600.

* Tue Oct 14 1997 Michael K. Johnson <johnsonm@redhat.com>
- bring down ppp devices if ifdown-ppp is called while ifup-ppp is sleeping.

* Mon Oct 13 1997 Erik Troan <ewt@redhat.com>
- moved to new chkconfig conventions

* Sat Oct 11 1997 Erik Troan <ewt@redhat.com>
- fixed rc.sysinit for hwclock compatibility

* Thu Oct 09 1997 Erik Troan <ewt@redhat.com>
- run 'ulimit -c 0' before running scripts in daemon function

* Wed Oct 08 1997 Donnie Barnes <djb@redhat.com>
- added chkconfig support
- made all rc*.d symlinks have missingok flag

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- fixed network-scripts to allow full pathnames as config files
- removed some old 3.0.3 pcmcia device handling

* Wed Oct 01 1997 Michael K. Johnson <johnsonm@redhat.com>
- /var/run/netreport needs to be group-writable now that /sbin/netreport
  is setguid instead of setuid.

* Tue Sep 30 1997 Michael K. Johnson <johnsonm@redhat.com>
- Added network-functions to spec file.
- Added report functionality to usernetctl.
- Fixed bugs I introduced into usernetctl while adding clone device support.
- Clean up entire RPM_BUILD_ROOT directory in %%clean.

* Mon Sep 29 1997 Michael K. Johnson <johnsonm@redhat.com>
- Clone device support in network scripts, rc scripts, and usernetctl.
- Disassociate from controlling tty in PPP and SLIP startup scripts,
  since they act as daemons.
- Spec file now provides start/stop symlinks, since they don't fit in
  the CVS archive.

* Tue Sep 23 1997 Donnie Barnes <djb@redhat.com>
- added mktemp support to ifup

* Thu Sep 18 1997 Donnie Barnes <djb@redhat.com>
- fixed some init.d/functions bugs for stopping httpd

* Tue Sep 16 1997 Donnie Barnes <djb@redhat.com>
- reworked status() to adjust for processes that change their argv[0] in
  the process table.  The process must still have it's "name" in the argv[0]
  string (ala sendmail: blah blah).

* Mon Sep 15 1997 Erik Troan <ewt@redhat.com>
- fixed bug in FORWARD_IPV4 support

* Sun Sep 14 1997 Erik Troan <ewt@redhat.com>
- added support for FORWARD_IPV4 variable

* Thu Sep 11 1997 Donald Barnes <djb@redhat.com>
- added status function to functions along with better killproc
  handling.
- added /sbin/usleep binary (written by me) and man page
- changed BuildRoot to /var/tmp instead of /tmp

* Tue Jun 10 1997 Michael K. Johnson <johnsonm@redhat.com>
- /sbin/netreport sgid rather than suid.
- /var/run/netreport writable by group root.
- /etc/ppp/ip-{up|down} no longer exec their local versions, so
  now ifup-post and ifdown-post will be called even if ip-up.local
  and ip-down.local exist.

* Tue Jun 03 1997 Michael K. Johnson <johnsonm@redhat.com>
- Added missing -f to [ invocation in ksyms check.

* Fri May 23 1997 Michael K. Johnson <johnsonm@redhat.com>
- Support for net event notification:
  Call /sbin/netreport to request that SIGIO be sent to you whenever
  a network interface changes status (won't work for brining up SLIP
  devices).
  Call /sbin/netreport -r to remove the notification request.
- Added ifdown-post, and made all the ifdown scrips call it, and
  added /etc/ppp/ip-down script that calls /etc/ppp/ip-down.local
  if it exists, then calls ifdown-post.
- Moved ifup and ifdown to /sbin

* Tue Apr 15 1997 Michael K. Johnson <johnsonm@redhat.com>
- usernetctl put back in ifdown
- support for slaved interfaces

* Wed Apr 02 1997 Erik Troan <ewt@redhat.com>
- Created ifup-post from old ifup
- PPP, PLIP, and generic ifup use ifup-post

* Fri Mar 28 1997 Erik Troan <ewt@redhat.com>
- Added DHCP support
- Set hostname via reverse name lookup after configuring a networking
  device if the current hostname is (none) or localhost

* Tue Mar 18 1997 Erik Troan <ewt@redhat.com>
- Got rid of xargs dependency in halt script
- Don't mount /proc twice (unmount it in between)
- sulogin and filesystem unmounting only happened for a corrupt root
  filesystem -- it now happens when other filesystems are corrupt as well

* Tue Mar 04 1997 Michael K. Johnson <johnsonm@redhat.com>
- PPP fixes and additions

* Mon Mar 03 1997 Erik Troan <ewt@redhat.com>
- Mount proc before trying to start kerneld so we can test for /proc/ksyms
  properly.

* Wed Feb 26 1997 Michael K. Johnson <johnsonm@redhat.com>
- Added MTU for PPP.
- Put PPPOPTIONS at the end of the options string instead of at the
  beginning so that they override other options.  Gives users more rope...
- Don't do module-based stuff on non-module systems.  Ignore errors if
  st module isn't there and we try to load it.

* Tue Feb 25 1997 Michael K. Johnson <johnsonm@redhat.com>
- Changed ifup-ppp and ifdown-ppp not to use doexec, because the argv[0]
  provided by doexec goes away when pppd gets swapped out.
- ifup-ppp now sets remotename to the logical name of the device.
  This will BREAK current PAP setups on netcfg-managed interfaces,
  but we needed to do this to add a reasonable interface-specific
  PAP editor to netcfg.

* Fri Feb 07 1997 Erik Troan <ewt@redhat.com>
- Added usernetctl wrapper for user mode ifup and ifdown's and man page
- Rewrote ppp and slip kill and retry code
- Added doexec and man page
