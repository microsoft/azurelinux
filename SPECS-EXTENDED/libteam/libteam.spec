Name: libteam
Version: 1.30
Release: 3%{?dist}
Summary: Library for controlling team network device
License: LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://www.libteam.org
Source: https://www.libteam.org/files/libteam-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: jansson-devel
BuildRequires: libdaemon-devel
BuildRequires: libnl3-devel
BuildRequires: dbus-devel
BuildRequires: systemd
BuildRequires: swig
BuildRequires: doxygen

%description
This package contains a library which is a user-space
counterpart for team network driver. It provides an API
to control team network devices.

%package devel
Summary: Libraries and header files for libteam development
Requires: %{name}%{?_isa} = %{version}-%{release}

%package doc
Summary: API documentation for libteam and libteamd
Requires: %{name}%{?_isa} = %{version}-%{release}

%description doc
This package contains libteam and libteamd API documentation

%package -n teamd
Summary: Team network device control daemon
Requires: %{name}%{?_isa} = %{version}-%{release}

%package -n teamd-devel
Summary: Libraries and header files for teamd development
Requires: %{name}%{?_isa} = %{version}-%{release}

%package -n network-scripts-teamd
Summary: teamd legacy network service support
Requires: network-scripts
Supplements: (%{name} and network-scripts)

%description devel
The libteam-devel package contains the header files and libraries
necessary for developing programs using libteam.

%description -n teamd
The teamd package contains team network device control daemon.

%description -n teamd-devel
The teamd-devel package contains the header files and libraries
necessary for developing programs using libteamdctl.

%description -n network-scripts-teamd
This provides the ifup and ifdown scripts for use with the legacy network
service.
service.

%prep
%setup -q

# prepare example dir for -devel
mkdir -p _tmpdoc1/examples
rm examples/python/*.py
cp -p examples/*.c _tmpdoc1/examples

%build
%configure --disable-static
make %{?_smp_mflags}
make html

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name \*.la -delete
rm -rf $RPM_BUILD_ROOT/%{_bindir}/team_*
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d
install -p teamd/dbus/teamd.conf $RPM_BUILD_ROOT%{_sysconfdir}/dbus-1/system.d/
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p teamd/redhat/systemd/teamd@.service $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-Team $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-Team $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifup-TeamPort $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 teamd/redhat/initscripts_systemd/network-scripts/ifdown-TeamPort $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts
install -p -m 755 utils/bond2team $RPM_BUILD_ROOT%{_bindir}/bond2team

%ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/libteam.so.*
%{_bindir}/teamnl
%{_mandir}/man8/teamnl.8*

%files devel
%doc _tmpdoc1/examples
%{_includedir}/team.h
%{_libdir}/libteam.so
%{_libdir}/pkgconfig/libteam.pc

%files doc
%doc doc/api

%files -n teamd
%doc teamd/example_configs teamd/redhat/example_ifcfgs/
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/dbus-1/system.d/teamd.conf
%config(noreplace) %attr(644,root,root) %{_unitdir}/teamd@.service
%{_libdir}/libteamdctl.so.*
%{_bindir}/teamd
%{_bindir}/teamdctl
%{_bindir}/bond2team
%{_mandir}/man8/teamd.8*
%{_mandir}/man8/teamdctl.8*
%{_mandir}/man5/teamd.conf.5*
%{_mandir}/man1/bond2team.1*

%files -n teamd-devel
%{_includedir}/teamdctl.h
%{_libdir}/libteamdctl.so
%{_libdir}/pkgconfig/libteamdctl.pc

%files -n network-scripts-teamd
%{_sysconfdir}/sysconfig/network-scripts/ifup-Team
%{_sysconfdir}/sysconfig/network-scripts/ifdown-Team
%{_sysconfdir}/sysconfig/network-scripts/ifup-TeamPort
%{_sysconfdir}/sysconfig/network-scripts/ifdown-TeamPort

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.30-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild


* Thu Jan 09 2020 Jiri Pirko <jiri@resnulli.us> - 1.30-1
- 1.30 release
- teamd/lacp: fix segfault due to NULL pointer dereference
- teamd: fix build error in expansion of macro teamd_log_dbgx
- teamd: update ctx->hwaddr after setting team dev to new hwaddr
- libteam: wapper teamd_log_dbg with teamd_log_dbgx
- teamd: Disregard current state when considering port enablement
- man teamd.conf: update some parameter default values

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Jiri Pirko <jiri@resnulli.us> - 1.29-1
- 1.29 release
- teamd: improve the error output for non-integer port prio
- teamd: return 0 if tdport doesn't exist in teamd_config_port_set
- teamd: add port_master_ifindex_changed for link_watch_port_watch_ops
- initscripts: fix if/fi align
- teamd: fix a json object memleak in get_port_obj()
- libteam: set netlink event socket as non-blocking
- libteam: double NETLINK_RCVBUF to fix -ENOMEM error
- teamd: add a default value 1000 for link_watch.interval
- teamd: use enabled option_changed to sync enabled to link_up for lb runner
- teamd: tdport has to exist if item->per_port is set in __find_by_item_path
- teamd: remove port if adding fails
- teamd: lacp: update port state according to partner's sync bit
- man: fix runner.min_ports default value
- teamd: lw: nsna_ping: only send ns on enabled port
- teamd: lw: arp_ping: only check arp reply message
- teamd: config: update local prio to kernel
- teamnl: update help message

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 09 2018 Jiri Pirko <jiri@resnulli.us> - 1.28-1
- 1.28 release
- teamd: lacp: send LACPDU when port state transitions from DEFAULT to CURRENT
- man teamd.conf: Document ARP Ping link_watch.vlanid option
- man teamd.conf: fix indentation of link_watch.send_always
- libteam/options: fix s32/u32 data storage on big endian
- teamd: add an option to force log output to stdout, stderr or syslog
- teamd: add port_master_ifindex_changed for teamd_event_watch_ops
- utils: check to_stdout return correctly in bond2team
- binding/python: use SWIG_FromCharPtrAndSize for Python3 support
- man: add 'random' to the list of available runners
- libteam: don't crash when trying to print unregistered device name
- configure.ac: Empty LDFLAGS before checking for libnl3
- man: fix runner.sys_prio default
- examples: fix duplex comparison against best port
- teamd: add port_hwaddr_changed for lacp runner
- teamd: add port_hwaddr_changed for lb runner
- teamd: add port_hwaddr_changed for ab runner
- teamd: do not process lacpdu before the port ifinfo is set

* Tue Sep 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.27-11
- Remove Python 2 subpackage (#1627333)

* Thu Aug  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.27-10
- Properly move network-scripts dep to right package

* Thu Aug  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.27-9
- Move legacy network scripts into network-scripts-teamd sub package

* Sun Jul 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.27-8
- Cleanup spec, fix deps

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.27-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.27-4
- Python 2 binary package renamed to python2-libteam
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Jiri Pirko <jiri@resnulli.us> - 1.27-1
- 1.27 release
- teamd: check target host with nap.nah.nd_na_target
- teamd: check ipv6 packet only with the 4 bits version
- teamd: set correct bits for standby ports
- libteam: Add team_get_port_enabled function
- teamd: check port link_up when a port is added with loadbalance runner
- libteam: resynchronize ifinfo after lost RTNLGRP_LINK notifications
- SubmittingPatches: add checkpatch note
- README: add note regarding pull requests
- teamd: escape some sensitive characters in ifname with double quotation marks

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 26 2016 Jiri Pirko <jiri@resnulli.us> - 1.26-1
- 1.26 release
- teamd: lacp: Do not unselect port if it changes state to "expired"
- man: in lacp it's 'port_config', not 'port_options'
- teamd: fix the issue that network blocks when systemctl stop teamd
- teamd: change to Before=network-pre.target in systemd service file
- man teamd.conf: fix indentation
- misc: fix an out-of-bound write with zero-length hardware address
- teamd: LACP runner does not set Agg bit on first slave

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May 20 2016 Jiri Pirko <jiri@resnulli.us> - 1.25-1
- 1.25 release
- teamd: handle vlan 0 packets
- libteam: fix TEAM_OPTION_TYPE_BOOL type for big endian architectures

* Fri Apr 15 2016 Jiri Pirko <jiri@resnulli.us> - 1.24-1
- 1.24 release
- teamd: lacp: use original hwaddr as source address in lacpdus
- teamd: do correct l3/l4 tx hashing with vlans
- libteam: Fix broken links

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Jiri Pirko <jiri@resnulli.us> - 1.23-1
- 1.23 release
- dbus: don't do <deny send_interface="..." /> in template dbus s. f.
- libteam: retry on NLE_DUMP_INTR error

* Tue Nov 03 2015 Jiri Pirko <jiri@resnulli.us> - 1.22-1
- 1.22 release
- dbus: don't do <deny send_interface="..." /> in dbus service file
- teamd: Fix member port state change on master team admin UP.
- teamd: add CAP_NET_RAW capability for LACP packet sockets
- add teamd.conf.in to EXTRA_DIST

* Mon Oct 05 2015 Jiri Pirko <jiri@resnulli.us> - 1.21-1
- 1.21 release
- libteam: add missing "static inline" in nl_updates
- libteam: check for definition of NLA_PUT_S* separatelly

* Mon Oct 05 2015 Jiri Pirko <jiri@resnulli.us> - 1.20-1
- 1.20 release
- libteam: fix compile error with newer libnl

* Mon Oct 05 2015 Jiri Pirko <jiri@resnulli.us> - 1.19-1
- 1.19 release
- teamd: add Before=network.target to systemd service file
- teamd: lacp: update actor state before sending LACP frames
- regenerate dbus policy file from template when user changed
- drop privileges to usr/grp specified at build time
- make teamd's run directory configurable
- create run directory at teamd program start
- teamd: fix cut&paste issue on delay_up
- Add stamp-h1 artifact to .gitignore
- Reduce usock file permissions to 700.
- Do not fail teamd_add_ports() when one port is missing
- Add missing prototypes for admin_state functions
- teamd: lacp: Don't send LACP frames when master team device is down.
- libteam, teamd: Track admin state of team device and add handlers to watch for changes.
- teamd: loadbalance mode lacks a .hwaddr_changed in teamd_event_watch_ops
- libteamdctl: fix timeval value for select

* Fri Aug 21 2015 Jiri Pirko <jiri@resnulli.us> - 1.18-1
- 1.18 release
- teamd: lacp: change actor system value on team mac change
- Fix sending duplicate LACP frames at the start of establishing a logical channel.
- Fix teamd memory corruption issues seen by missing port unlink in ifinfo_destroy()
- libteam: Add check to disallow creating device names longer than 15 chars.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 02 2015 Jiri Pirko <jpirko@redhat.com> - 1.17-1
- 1.17 release
- update copyright dates
- man: teamdctl: add entry for item set of debug_level
- teamd: lw: nsna_ping: fix na rx handling
- teamd: lw: arp_ping: fix arp rx handling
- libteam: ifinfo: fix rtnl dellink handling

* Tue Mar 24 2015 Jiri Pirko <jpirko@redhat.com> - 1.16-1
- 1.16 release
- teamd: events: update ctx->hwaddr_len before calling hwaddr_changed handlers
- teamd: do not change ctx->hwaddr pointer
- teamd: lacp: change port mac address when team mac address is changed
- teamdctl: show port link down count in state output
- teamd: lw: count how many times has been the port down
- init unitialized value to 0/NULL to silence gcc warnings instead of x=x
- libteamdctl: rename recvmsg variable to recv_message
- teamd: check retval of malloc in lw_tipc_link_state_change
- teamd: fix potential memory leak in __set_sockaddr error path
- libteamdctl: fix typo in warning message in cli_zmq_recv
- libteam: check phys_port_id_len in update_phys_port_id
- teamnl: fix potential memory leak in run_cmd_getoption

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.15-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Dec 17 2014 Jiri Pirko <jpirko@redhat.com> - 1.15-1
- 1.15 release
- teamd: ignore SIGPIPE
- libteamdctl: Fix a typo in DBus method name

* Wed Nov 05 2014 Jiri Pirko <jpirko@redhat.com> - 1.14-1
- 1.14 release
- teamd: lw_arp_ping: make buf static and avoid returning local pointer

* Wed Nov 05 2014 Jiri Pirko <jpirko@redhat.com> - 1.13-1
- 1.13 release
- teamd: fix coding style a bit after previous commit
- teamd: Don't ever kill PID 0
- teamd: tipc: topology-aware failover
- teamd: tipc: fix team port removal bugs
- zmq: remove unused my_free_msg
- libteamdctl: zmq: remove include of teamd.h
- teamd: add teamd_zmq_common.h to noinst headers

* Tue Aug 19 2014 Jiri Pirko <jpirko@redhat.com> - 1.12-1
- 1.12 release
- teamd: teamd_state_val_dump move TEAMD_BUG_ON so it can be actually triggered
- teamd: fix coverity error in teamd_sriov_physfn_addr
- libteamdctl: adjust doc comments to be processed by doxygen
- remove forgotten src dir
- libteam: stringify.c adjust doc comments to be processed by doxygen
- libteam: ports.c adjust doc comments to be processed by doxygen
- libteam: options.c adjust doc comments to be processed by doxygen
- libteam: ifinfo.c adjust doc comments to be processed by doxygen
- libteam: libteam.c adjust doc comments to be processed by doxygen
- add doxygen html doc generation into autoconf
- teamd: tipc: use TIPC_MAX_*_NAME for buffers and check len
- fix strncmp len in ifname2ifindex
- teamd: fix incorrect usage of sizeof in __str_sockaddr

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 26 2014 Jiri Pirko <jpirko@redhat.com> - 1.11-1
- 1.11 release
- teamd: add forgotten teamd_link_watch.h to noinst_HEADERS
- teamd: add tipc.h kernel header
- teamd: Add support for TIPC link watcher
- teamd: add TIPC link watcher
- teamd: move icmp6 NS/NA ping link watcher to a separate file
- teamd: move arp ping link watcher to a separate file
- teamd: move psr template link watcher to a separate file
- teamd: move ethtool link watcher to a separate file
- teamd_dbus: add PortConfigDump to introspection
- teamd: allow restart on failure through systemd
- teamd: distinguish exit code between init error and runtime error
- man teamd.conf: remove "mandatory" since the options are no longer mandatory
- teamd: add "debug_level" config option
- teamd: allow to change debug level during run
- teamd: register debug callback at the start of callbacks list
- libteam: add team_change_handler_register_head function
- teamd: lacp: update partner info before setting state
- teamd: lacp: do not check SYNCHRO flag before enable of port
- teamd: lacp: "expired" port is not selectable, only "current"
- teamd: lacp: update actor system (mac) before sending lacpdu
- teamd: respect currently set user linkup for created linkwatches
- teamd: split --take-over option into --no-quit-destroy
- teamd: fix port removal when using take_over
- libteam: add SubmittingPatches doc
- libteam: Use u8 for put/get TEAM_ATTR_OPTION_TYPE

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Jiri Pirko <jpirko@redhat.com> - 1.10-1
- Update to 1.10
- teamd: quit when our team device is removed from outside
- libteam: ifinfo: watch for dellink messages and call change handlers for that
- initscripts: make ifup/ifdown scripts usable by ifup/ifdown-eth scripts
- teamdctl: unmess check_teamd_team_devname and fix double free there
- man: correct type of "*_host" options
- teamd_link_watch: specify "missed_max" option default value
- bond2team: do not guess source_host option
- teamd_link_watch: allow to send ARP probes if no source_host is specified
- initscripts: do not try to re-add port if it is already there
- teamdctl: add command for easy port presention checking
- Fix potential small memory leak
- usock: accept multiline message string parameters
- libteamdctl: add notice for caller to do not modify or free certain strings
- teamd: do not remove ports from team dev in case of take over mode
- teamd: look for existing ports before adding new ones
- libteam: introduce ream_refresh
- teamd: fixed couple comments.
- teamd: update hwaddr when changing team's macaddr
- redhat: fix boolean types in example 2
- initscripts: fix port up before master and port down after master
- lb: enable/disable port according to linkwatch state
- fix comment typo in ifdown-Team scripts
- man teamd.conf: Minor improvements to style and language
- man teamdctl: Minor improvements to style and language

* Thu Jan 23 2014 Jiri Pirko <jpirko@redhat.com> - 1.9-2
- fix multilib

* Tue Nov 12 2013 Jiri Pirko <jpirko@redhat.com> - 1.9-1
- Update to 1.9
- libteamdctl: remove false lib dependencies
- teamdctl: use new port config get function
- libteamdctl: introduce support for port config get
- libteamdctl: cache reply strings into list
- teamd: introduce PortConfigDump control method
- teamd: make teamd_get_port_by_ifname ifname argument const
- Minor improvements to style and language.
- do not install example binaries
- minor man page(s) correction(s) and lintianisation
- teamdctl: print error message if ifindex cannot be obtained
- fix cflags path in pc files

* Tue Aug 13 2013 Jiri Pirko <jpirko@redhat.com> - 1.8-1
- Update to 1.8

* Mon Aug 12 2013 Jiri Pirko <jpirko@redhat.com> - 1.7-1
- Update to 1.7

* Thu Aug 08 2013 Jiri Pirko <jpirko@redhat.com> - 1.6-1
- Update to 1.6

* Tue Jul 30 2013 Jiri Pirko <jpirko@redhat.com> - 1.5-1
- Update to 1.5

* Tue Jun 11 2013 Jiri Pirko <jpirko@redhat.com> - 1.3-1
- Update to 1.3

* Wed May 29 2013 Jiri Pirko <jpirko@redhat.com> - 1.2-1
- Update to 1.2

* Thu May 16 2013 Jiri Pirko <jpirko@redhat.com> - 1.1-1
- Update to 1.1

* Thu Jan 31 2013 Jiri Pirko <jpirko@redhat.com> - 1.0-1
- Update to 1.0

* Sun Jan 20 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-27.20130110gitf16805c
- Rebuilt for libnl3

* Sun Jan 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.1-26.20130110gitf16805c
- Rebuilt for libnl3

* Thu Jan 10 2013 Jiri Pirko <jpirko@redhat.com> - 0.1-25.20130110gitf16805c
- Rebase to git commit f16805c

* Wed Dec 12 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-24.20121212git01fe4bd
- Rebase to git commit 01fe4bd

* Thu Dec 06 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-23.20121206git659a848
- Rebase to git commit 659a848

* Thu Nov 22 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-22.20121122git18b6701
- Rebase to git commit 18b6701

* Thu Nov 15 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-21.20121115gitffb5267
- Rebase to git commit ffb5267

* Mon Nov 05 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-20.20121105git3b95b34
- Rebase to git commit 3b95b34

* Thu Oct 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-19.20121025git7fe7c72
- Rebase to git commit 7fe7c72

* Fri Oct 19 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-18.20121019git1a91059
- Rebase to git commit 1a91059

* Sun Oct 07 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-17.20121007git6f48751
- Rebase to git commit 6f48751

* Tue Sep 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-16.20120925gitcc5cddc
- Rebase to git commit cc5cddc

* Sun Sep 23 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-15.20120923git8448186
- Rebase to git commit 8448186

* Tue Sep 04 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-14.20120904gitbdcf72c
- Rebase to git commit bdcf72c

* Wed Aug 22 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-13.20120822gitc0d943d
- Rebase to git commit c0d943d

* Tue Aug 07 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-12.20120807git9fa4a96
- Rebase to git commit 9fa4a96

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-11.20120628gitca7b526
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-10.20120628gitca7b526
- Rebase to git commit ca7b526

* Wed Jun 27 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-9.20120627git96569f8
- Rebase to git commit 96569f8

* Wed Jun 27 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-8.20120627gitcd6b557
- Rebase to git commit cd6b557

* Wed Jun 20 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-7.20120620gita88fabf
- Rebase to git commit a88fabf

* Fri May 04 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-6.20120504git11e234a
- Rebase to git commit 11e234a

* Thu Apr 05 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-5.20120405gita82f8ac
- Rebase to git commit a82f8ac

* Tue Feb 21 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-4.20120221gitfe97f63
- Rebase to git commit fe97f63

* Mon Jan 30 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-3.20120130gitb5cf2a8
- Rebase to git commit b5cf2a8

* Wed Jan 25 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-2.20120125gita1718f8
- Rebase to git commit a1718f8

* Wed Jan 18 2012 Jiri Pirko <jpirko@redhat.com> - 0.1-1.20120113git302672e
- Initial build.
