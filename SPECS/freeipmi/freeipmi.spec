Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1
# Copyright (c) 2003 FreeIPMI Core Team

Name:             freeipmi
Version:          1.6.11
Release:          1%{?dist}
Summary:          IPMI remote console and system management software
License:          GPLv3+
URL:              http://www.gnu.org/software/freeipmi/
Source0:          http://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.gz
Source1:          bmc-watchdog.service
Source2:          ipmidetectd.service
Source3:          ipmiseld.service
BuildRequires:    libgcrypt-devel 
BuildRequires:    texinfo 
BuildRequires:    systemd 
%{?systemd_requires}
BuildRequires:    gcc

%description
The FreeIPMI project provides "Remote-Console" (out-of-band) and
"System Management Software" (in-band) based on Intelligent
Platform Management Interface specification.

%package          devel
Summary:          Development package for FreeIPMI
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description      devel
Development package for FreeIPMI. This package includes the FreeIPMI
header files and libraries.

%package          bmc-watchdog
Summary:          IPMI BMC watchdog
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description      bmc-watchdog
Provides a watchdog daemon for OS monitoring and recovery.

%package          ipmidetectd
Summary:          IPMI node detection monitoring daemon
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description      ipmidetectd
Provides a tool and a daemon for IPMI node detection.

%package          ipmiseld
Summary:          IPMI SEL syslog logging daemon
Requires:         %{name}%{?_isa} = %{version}-%{release}
%description      ipmiseld
IPMI SEL syslog logging daemon.

%if %{?_with_debug:1}%{!?_with_debug:0}
  %global _enable_debug --enable-debug --enable-trace --enable-syslog
%endif

%prep
%autosetup -p1

%build
export CFLAGS="-D_GNU_SOURCE $RPM_OPT_FLAGS"
%configure --program-prefix=%{?_program_prefix:%{_program_prefix}} \
           %{?_enable_debug} --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{_infodir}/dir
# kludge to get around rpmlint complaining about 0 length semephore file
echo freeipmi > %{buildroot}%{_localstatedir}/lib/freeipmi/ipckey

# Remove .la files
find %{buildroot} -name '*.la' -delete -print

# Install systemd units
install -m755 -d %{buildroot}%{_unitdir}
install -pm644 %SOURCE1 %SOURCE2 %SOURCE3 %{buildroot}%{_unitdir}/

# Remove initscripts
rm -frv %{buildroot}%{_initrddir} %{buildroot}%{_sysconfdir}/init.d

%post bmc-watchdog
%systemd_post bmc-watchdog.service

%preun bmc-watchdog
%systemd_preun bmc-watchdog.service

%postun bmc-watchdog
%systemd_postun_with_restart bmc-watchdog.service

%post ipmiseld
%systemd_post ipmiseld.service

%preun ipmiseld
%systemd_preun ipmiseld.service

%postun ipmiseld
%systemd_postun_with_restart ipmiseld.service

%post ipmidetectd
%systemd_post ipmidetectd.service

%preun ipmidetectd
%systemd_preun ipmidetectd.service

%postun ipmidetectd
%systemd_postun_with_restart ipmidetectd.service

%triggerun -- freeipmi-bmc-watchdog < 1.1.1-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save bmc-watchdog >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del bmc-watchdog >/dev/null 2>&1 || :
/bin/systemctl try-restart bmc-watchdog.service >/dev/null 2>&1 || :

%triggerun -- freeipmi-ipmidetectd < 1.1.1-2
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply httpd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save ipmidetectd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del ipmidetectd >/dev/null 2>&1 || :
/bin/systemctl try-restart ipmidetectd.service >/dev/null 2>&1 || :

%files
%dir %{_sysconfdir}/freeipmi/
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/freeipmi/freeipmi.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/freeipmi/ipmidetect.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/freeipmi/freeipmi_interpret_sel.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/freeipmi/freeipmi_interpret_sensor.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/freeipmi/libipmiconsole.conf
%doc %{_datadir}/doc/%{name}/AUTHORS
%doc %{_datadir}/doc/%{name}/COPYING
%doc %{_datadir}/doc/%{name}/ChangeLog
%doc %{_datadir}/doc/%{name}/ChangeLog.0
%doc %{_datadir}/doc/%{name}/INSTALL
%doc %{_datadir}/doc/%{name}/NEWS
%doc %{_datadir}/doc/%{name}/README
%doc %{_datadir}/doc/%{name}/README.argp
%doc %{_datadir}/doc/%{name}/README.build
%doc %{_datadir}/doc/%{name}/README.openipmi
%doc %{_datadir}/doc/%{name}/TODO
%doc %{_infodir}/*
%doc %{_datadir}/doc/%{name}/COPYING.ipmiping
%doc %{_datadir}/doc/%{name}/COPYING.ipmipower
%doc %{_datadir}/doc/%{name}/COPYING.ipmiconsole
%doc %{_datadir}/doc/%{name}/COPYING.ipmimonitoring
%doc %{_datadir}/doc/%{name}/COPYING.pstdout
%doc %{_datadir}/doc/%{name}/COPYING.ipmidetect
%doc %{_datadir}/doc/%{name}/COPYING.ipmi-fru
%doc %{_datadir}/doc/%{name}/COPYING.ipmi-dcmi
%doc %{_datadir}/doc/%{name}/COPYING.sunbmc
%doc %{_datadir}/doc/%{name}/COPYING.ZRESEARCH
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmiping
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmipower
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmiconsole
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmimonitoring
%doc %{_datadir}/doc/%{name}/DISCLAIMER.pstdout
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmidetect
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmi-fru
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmi-dcmi
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmiping.UC
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmipower.UC
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmiconsole.UC
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmimonitoring.UC
%doc %{_datadir}/doc/%{name}/DISCLAIMER.pstdout.UC
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmidetect.UC
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmi-fru.UC
%doc %{_datadir}/doc/%{name}/freeipmi-coding.txt
%doc %{_datadir}/doc/%{name}/freeipmi-design.txt
%doc %{_datadir}/doc/%{name}/freeipmi-hostrange.txt
%doc %{_datadir}/doc/%{name}/freeipmi-libraries.txt
%doc %{_datadir}/doc/%{name}/freeipmi-bugs-issues-and-workarounds.txt
%doc %{_datadir}/doc/%{name}/freeipmi-testing.txt
%doc %{_datadir}/doc/%{name}/freeipmi-oem-documentation-requirements.txt
%dir %{_datadir}/doc/%{name}
%dir %{_datadir}/doc/%{name}/contrib
%dir %{_datadir}/doc/%{name}/contrib/ganglia
%doc %{_datadir}/doc/%{name}/contrib/ganglia/*
%dir %{_datadir}/doc/%{name}/contrib/nagios
%doc %{_datadir}/doc/%{name}/contrib/nagios/*
%dir %{_datadir}/doc/%{name}/contrib/pet
%doc %{_datadir}/doc/%{name}/contrib/pet/*
%{_libdir}/libipmiconsole*so.*
%{_libdir}/libfreeipmi*so.*
%{_libdir}/libipmidetect*so.*
%{_libdir}/libipmimonitoring.so.*
%{_localstatedir}/lib/*
%{_sbindir}/bmc-config
%{_sbindir}/bmc-info
%{_sbindir}/bmc-device
%{_sbindir}/ipmi-config
%{_sbindir}/ipmi-fru
%{_sbindir}/ipmi-locate
%{_sbindir}/ipmi-oem
%{_sbindir}/ipmi-pef-config
%{_sbindir}/pef-config
%{_sbindir}/ipmi-raw
%{_sbindir}/ipmi-sel
%{_sbindir}/ipmi-sensors
%{_sbindir}/ipmi-sensors-config
%{_sbindir}/ipmiping
%{_sbindir}/ipmi-ping
%{_sbindir}/ipmipower
%{_sbindir}/ipmi-power
%{_sbindir}/rmcpping
%{_sbindir}/rmcp-ping
%{_sbindir}/ipmiconsole
%{_sbindir}/ipmi-console
%{_sbindir}/ipmimonitoring
%{_sbindir}/ipmi-chassis
%{_sbindir}/ipmi-chassis-config
%{_sbindir}/ipmi-dcmi
%{_sbindir}/ipmi-pet
%{_sbindir}/ipmidetect
%{_sbindir}/ipmi-detect
%{_mandir}/man8/bmc-config.8*
%{_mandir}/man5/bmc-config.conf.5*
%{_mandir}/man8/bmc-info.8*
%{_mandir}/man8/bmc-device.8*
%{_mandir}/man8/ipmi-config.8*
%{_mandir}/man5/ipmi-config.conf.5*
%{_mandir}/man8/ipmi-fru.8*
%{_mandir}/man8/ipmi-locate.8*
%{_mandir}/man8/ipmi-oem.8*
%{_mandir}/man8/ipmi-pef-config.8*
%{_mandir}/man8/pef-config.8*
%{_mandir}/man8/ipmi-raw.8*
%{_mandir}/man8/ipmi-sel.8*
%{_mandir}/man8/ipmi-sensors.8*
%{_mandir}/man8/ipmi-sensors-config.8*
%{_mandir}/man8/ipmiping.8*
%{_mandir}/man8/ipmi-ping.8*
%{_mandir}/man8/ipmipower.8*
%{_mandir}/man8/ipmi-power.8*
%{_mandir}/man5/ipmipower.conf.5*
%{_mandir}/man8/rmcpping.8*
%{_mandir}/man8/rmcp-ping.8*
%{_mandir}/man8/ipmiconsole.8*
%{_mandir}/man8/ipmi-console.8*
%{_mandir}/man5/ipmiconsole.conf.5*
%{_mandir}/man8/ipmimonitoring.8*
%{_mandir}/man5/ipmi_monitoring_sensors.conf.5*
%{_mandir}/man5/ipmimonitoring_sensors.conf.5*
%{_mandir}/man5/ipmimonitoring.conf.5*
%{_mandir}/man5/freeipmi_interpret_sel.conf.5*
%{_mandir}/man5/freeipmi_interpret_sensor.conf.5*
%{_mandir}/man5/libipmimonitoring.conf.5*
%{_mandir}/man8/ipmi-chassis.8*
%{_mandir}/man8/ipmi-chassis-config.8*
%{_mandir}/man8/ipmi-dcmi.8*
%{_mandir}/man8/ipmi-pet.8*
%{_mandir}/man8/ipmidetect.8*
%{_mandir}/man8/ipmi-detect.8*
%{_mandir}/man5/freeipmi.conf.5*
%{_mandir}/man5/ipmidetect.conf.5*
%{_mandir}/man5/libipmiconsole.conf.5*
%{_mandir}/man7/freeipmi.7*
%dir %{_localstatedir}/cache/ipmimonitoringsdrcache

%files devel
%dir %{_datadir}/doc/%{name}/contrib/libipmimonitoring
%doc %{_datadir}/doc/%{name}/contrib/libipmimonitoring/*
%{_libdir}/libipmiconsole.so
%{_libdir}/libfreeipmi.so
%{_libdir}/libipmidetect.so
%{_libdir}/libipmimonitoring.so
%dir %{_includedir}/freeipmi
%dir %{_includedir}/freeipmi/api
%dir %{_includedir}/freeipmi/cmds
%dir %{_includedir}/freeipmi/debug
%dir %{_includedir}/freeipmi/driver
%dir %{_includedir}/freeipmi/fiid
%dir %{_includedir}/freeipmi/fru
%dir %{_includedir}/freeipmi/interface
%dir %{_includedir}/freeipmi/interpret
%dir %{_includedir}/freeipmi/locate
%dir %{_includedir}/freeipmi/payload
%dir %{_includedir}/freeipmi/record-format
%dir %{_includedir}/freeipmi/record-format/oem
%dir %{_includedir}/freeipmi/sdr
%dir %{_includedir}/freeipmi/sdr/oem
%dir %{_includedir}/freeipmi/sel
%dir %{_includedir}/freeipmi/sensor-read
%dir %{_includedir}/freeipmi/spec
%dir %{_includedir}/freeipmi/spec/oem
%dir %{_includedir}/freeipmi/templates
%dir %{_includedir}/freeipmi/templates/oem
%dir %{_includedir}/freeipmi/util
%{_includedir}/ipmiconsole.h
%{_includedir}/ipmidetect.h
%{_includedir}/ipmi_monitoring*.h
%{_includedir}/freeipmi/*.h
%{_includedir}/freeipmi/api/*.h
%{_includedir}/freeipmi/cmds/*.h
%{_includedir}/freeipmi/debug/*.h
%{_includedir}/freeipmi/driver/*.h
%{_includedir}/freeipmi/fiid/*.h
%{_includedir}/freeipmi/fru/*.h
%{_includedir}/freeipmi/interface/*.h
%{_includedir}/freeipmi/interpret/*.h
%{_includedir}/freeipmi/locate/*.h
%{_includedir}/freeipmi/payload/*.h
%{_includedir}/freeipmi/record-format/*.h
%{_includedir}/freeipmi/record-format/oem/*.h
%{_includedir}/freeipmi/sdr/*.h
%{_includedir}/freeipmi/sdr/oem/*.h
%{_includedir}/freeipmi/sel/*.h
%{_includedir}/freeipmi/sensor-read/*.h
%{_includedir}/freeipmi/spec/*.h
%{_includedir}/freeipmi/spec/oem/*.h
%{_includedir}/freeipmi/templates/*.h
%{_includedir}/freeipmi/templates/oem/*.h
%{_includedir}/freeipmi/util/*.h
%{_mandir}/man3/*
%{_libdir}/pkgconfig/*

%files bmc-watchdog
%doc %{_datadir}/doc/%{name}/COPYING.bmc-watchdog
%doc %{_datadir}/doc/%{name}/DISCLAIMER.bmc-watchdog
%doc %{_datadir}/doc/%{name}/DISCLAIMER.bmc-watchdog.UC
%config(noreplace) %{_sysconfdir}/sysconfig/bmc-watchdog
%{_sbindir}/bmc-watchdog
%{_mandir}/man8/bmc-watchdog.8*
%{_unitdir}/bmc-watchdog.service

%files ipmidetectd
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/freeipmi/ipmidetectd.conf
%{_sbindir}/ipmidetectd
%{_mandir}/man5/ipmidetectd.conf.5*
%{_mandir}/man8/ipmidetectd.8*
%{_unitdir}/ipmidetectd.service

%files ipmiseld
%doc %{_datadir}/doc/%{name}/COPYING.ipmiseld
%doc %{_datadir}/doc/%{name}/DISCLAIMER.ipmiseld
%{_unitdir}/ipmiseld.service
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/freeipmi/ipmiseld.conf
%{_sbindir}/ipmiseld
%{_mandir}/man5/ipmiseld.conf.5*
%{_mandir}/man8/ipmiseld.8*
%dir %{_localstatedir}/cache/ipmiseld

%changelog
* Thu Jul 28 2022 Henry Li <lihl@microsoft.com> - 1.6.6-3
- Fix spec formatting
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.6-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Wed Oct 07 2020 Josef Ridky <jridky@redhat.com> - 1.6.6-1
- New upstream release 1.6.6 (#1875941)

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Václav Doležal <vdolezal@redhat.com> - 1.6.5-1
- New upstream release 1.6.5

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Vaclav Dolezal <vdolezal@redhat.com> - 1.6.4-1
- New upstream release 1.6.4

* Fri Aug 02 2019 Vaclav Dolezal <vdolezal@redhat.com> - 1.6.3-1
- New upstream release 1.6.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 09 2018 Josef Ridky <jridky@redhat.com> - 1.6.2-1
- New upstream release 1.6.2 (#1574750)

* Tue Apr 10 2018 Josef Ridky <jridky@redhat.com> - 1.6.1-1
- New upstream release 1.6.1 (#1541578)

* Thu Mar 08 2018 Josef Ridky <jridky@redhat.com> - 1.5.7-4
- Fix gcc dependency

* Wed Feb 21 2018 Josef Ridky <jridky@redhat.com> - 1.5.7-3
- Spec clean up (remove Group tag, add new macros and gcc dependency)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 25 2017 Josef Ridky <jridky@redhat.com> - 1.5.7-1
- New upstream release 1.5.7 (#1482285)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Josef Ridky <jridky@redhat.com> - 1.5.6-1
- New upstream release 1.5.6 (#1468062)
- Fix issue with capital letters in commands in manpage (#1468984)

* Mon Mar 27 2017 Josef Ridky <jridky@redhat.com> - 1.5.5-1
- New upstream release 1.5.5 (#1436115)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 14 2016 Boris Ranto <branto@redhat.com> - 0:1.5.4-1
- New version (0:1.5.4-1)

* Tue May 24 2016 Boris Ranto <branto@redhat.com> - 0:1.5.2-1
- New version (0:1.5.2-1)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 2 2015 Boris Ranto <branto@redhat.com> - 1.5.1-1
- Update to 1.5.1 (#1287346)

* Sat Oct 31 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.4.11-1
- Update to 1.4.11 (#1227126)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 Ales Ledvinka <aledvink@redhat.com> - 1.4.8-2
- Remove modalias dependency.

* Mon Feb 23 2015 Christopher Meng <rpm@cicku.me> - 1.4.8-1
- Updated to freeipmi-1.4.8
 - Fix segfault in crypt code with libgcrypt versions >= 1.6.0.
 - Fix --fanout command line parse bug.
 - Fix typ - from FRU spec, language "Tegulu" is actually "Telugu".
 - Fix typ - in SEL session output, "Invalid Username of Password" to
  "Invalid Username or Password".
 - Loop on select() call if interrupted by EINTR in openipmi, ssif, and
  sunbmc inband drivers.
 - Fix integer overflow bug in ipmi-config when configure vlan ID > 255.
 - Add workaround for ipmi-config issue on Supermicr - X10DDW-i.
 - Fix error handling bug in bmc-info.

* Tue Nov 04 2014 Ales Ledvinka <aledvink@redhat.com> - 1.4.6-1
- Updated to upstream freeipmi-1.4.6
 - In ipmi-fru, support output of DDR4 SDRAM modules.
 - Fix EFI probing on non IA64 systems.
 - Fix corner case in ipmi-raw w/ standard input or --file and empty lines.
 - Fix parsing corner case in ipmi-chassis.
 - Support SSIF bridging.
 - Fix libipmiconsole calculation bug w/ SOL character send size.
 - Support Supermicro H8DGU and H8DG6 OEM sensors and events.
 - Minor documentation updates.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 Ales Ledvinka <aledvink@redhat.com> - 1.4.4-1
- Updated to upstream freeipmi-1.4.4
 - Support retrys of SSIF reads to handle SSIF NACKs.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Ales Ledvinka <aledvink@redhat.com> - 1.4.3-1
- Updated to upstream freeipmi-1.4.3
 - In ipmi-oem, support Supermicro get-power-supply-status and
   get-pmbus-power-supply-status commands.
 - Support 'ipmiping' workaround in ipmipower.
 - Minor documentation updates.

* Tue Mar 04 2014 Ales Ledvinka <aledvink@redhat.com> - 1.4.1-1
- Updated to upstream freeipmi-1.4.1
 - Support new tool ipmi-config.  Ipmi-config is a consolidated
   configuration tool implementing everything that was previously in
   bmc-config, ipmi-pef-config, ipmi-sensors-config, and
   ipmi-chassis-config.
   - The consolidated tool will allow users to checkout, commit, and
     diff sections/fields across the four former tools using only one
     tool.
   - The consolidated tool will also allow users to checkout, commit,
     and diff new sections/fields not yet covered in the four former
     tools.
   - Legacy scripts for bmc-config, ipmi-pef-config,
     ipmi-sensors-config, and ipmi-chassis-config will point to the new
     tool with all appropriate options to ensure full backwards
     compatability.
   - The ipmi-pef-config --info option has been made legacy.  It is
     still supported but no longer advertised.
 - Support Intel Data Center Host Interface / Management Engine as
   optional driver type for in-band communication.
   - Typically these are loaded as /dev/dcmi and /dev/mei drivers.
   - This driver is identified as the "inteldcmi" type, as it is
     specific to Intel systems.
 - Support OEM extensions for Intel Windmill, Wiwynn Windmill, and
   Quanta Winterfell motherboards in ipmi-sel and ipmi-sensors.  These
   motherboards are also know as motherboards for the Open Compute
   Project (OCP).
 - Support DCMI configuration in ipmi-config.
 - Update FreeIPMI for changes in IPMI 2.0 Errata 5.  Include are:
   - New sensor events for Power Supply and OS Boot sensors.  New
     events are supported in all areas, ipmi-sensors, ipmi-sel,
     libipmimonitoring, etc.
   - PEF now supports 255 filter numbers, not 127.  This is supported
     in ipmi-config (formerly ipmi-pef-config).
   - Support get/set of new System Info Parameters Present OS Version,
     BMC URL, and Base OS/Hypervisor URL.  This is supported in
     bmc-info and bmc-device.
 - Update ipmi-oem Intel Node Manager OEM commands for changes listed
   in Intelligent Power Node Manager 2.0 specification.
   - Due to changes in the specification, minor text changes may exist
     in some output from intelnm OEM commands.
 - Update ipmi-sel to support new SEL events in Intelligent Power Node
   Manager 2.0 specification.
 - Support 'serialalertsdeferred' workaround in ipmiconsole.
 - Support 'solpacketseq' workaround in ipmiconsole.
 - Fix portability issues for Apple / OS X.
 - Fix bmc-info output of GUID, format was output with two bytes out of
   order.
   - May affect scripts parsing and using the GUID.
 - Bmc-info now supports --get-system-guid and outputs the System GUID
   as well as the Device GUID by default.
   - The Device GUID is not prefixed with the text "Device GUID"
     instead of just "GUID".  Any scripts scripting against this will
     need to be adjusted.
 - Bmc-info now supports a workaround of 'guidformat' to read the GUID
   with a format a number of vendors have incorrectly used.
 - In ipmi-config's sensor configuration, decimal values that cannot be
   encoded accurately now report a clearer error message.

* Tue Jan 14 2014 Ales Ledvinka <aledvink@redhat.com> - 1.3.4-2
- Module alias dependencies.
- Changes for previous 1.3.4 update:
 - Support 'solchannelsupport' workraound in ipmiconsole /
   IPMICONSOLE_WORKAROUND_SKIP_CHANNEL_PAYLOAD_SUPPORT workaround flag in
   libipmiconsole.
 - Fix SDR cache workaround for motherboards with invalid SDR record
   counts listed.
 - Workaround Supermicro bug in bmc-watchdog. 
 - Fix error checks in sensor decoding functions, leading to possible
   problems in ipmi-sensors-config.
 - Update documentation with additional workarounds for motherboards.

* Tue Dec 17 2013 Christopher Meng <rpm@cicku.me> - 1.3.4-1
- Updated to freeipmi-1.3.4

* Fri Nov  8 2013 Ales Ledvinka <aledvink@redhat.com> - 1.3.3-1
- Updated to freeipmi-1.3.3
 - Add support for intelnm get-node-manager-alert-destination and
   set-node-manager-alert-destination in ipmi-oem.
 - Under very verbose mode, ipmi-sel will now record types for OEM
   records.  This should allow OEM parses outside of FreeIPMI to more
   effectively parse OEM specific SEL records.
 - Fix big endian portability bugs.

* Mon Sep 23 2013 Ales Ledvinka <aledvink@redhat.com> - 1.3.2-1
- Updated to freeipmi-1.3.2
 - Update FreeIPMI tools to check libfreeipmi API error codes
   correctly.
 - Update ipmi-api.h to list mappings of IPMI completion codes and
   RMCPPlus codes to API Error codes.

* Mon Sep  2 2013 Ales Ledvinka <aledvink@redhat.com> - 1.3.1-1
- Updated to freeipmi-1.3.1
 - Timestamp UTC/localtime reporting compliant with specification.
   Remote timestamp expected to be in localtime already.
 - Timestamp reporting options --utc-to-localtime,
   --localtime-to-utc and --utc-offset.
 - In ipmi-fru, support output of DDR3 SDRAM modules.
 - In ipmi-fru, support output of new FRU multirecords, most notably
   extended DC output and extended DC load (per FRU Revision 1.2).
 - Support additional chassis types (per FRU Revision 1.2 update).
 - and more

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Ales Ledvinka <aledvink@redhat.com> - 1.2.9-2
- Requires modalias package for module loading dependency.

* Fri Jul 19 2013 Ales Ledvinka <aledvink@redhat.com> - 1.2.9-1
- Updated to upstream freeipmi-1.2.9
 - Fix threshold output corner case in ipmi-sensors.
 - Fix invalid declaration in libipmimonitoring header.
 - Fix older compiler build problems.
 -
 - Fix portability build bug on ARM systems.
 - Add 'internal IPMI error' troubleshooting to manpages.
 - Fix bmc-info corner case on Bull 510 systems.

* Fri May 31 2013 Ales Ledvinka <aledvink@redhat.com> - 1.2.7-2
- Fix build on architectures where va_list is not pointer.

* Mon May 20 2013 Ales Ledvinka <aledvink@redhat.com> - 1.2.7-1
- Updated to freeipmi-1.2.7
 - Fix sensor output errors with OEM sensors.

* Fri May 17 2013 Ales Ledvinka <aledvink@redhat.com> - 1.2.6-2
- spec update by Christopher Meng <rpm@cicku.me>
- hardened build flags should include PIE also for bmc-watchdog.

* Fri May 03 2013 Ales Ledvinka <aledvink@redhat.com> - 1.2.6-1
- Updated to freeipmi-1.2.6
 - Support HP Proliant DL160 G8 OEM sensors.
 - Support Supermicro X9SCM-iiF OEM sensors and events.
 - Support output of temperature sampling period to ipmi-dcmi.
 - Clarify error message when SOL session cannot be stolen in
   ipmiconsole/libipmiconsole.
 - Fix dcmi rolling average time period output error
 - Fix ipmi-dcmi output errors with --get-dcmi-sensor-info.
 - Fix corner case in calculation of confidentiality pad length with
   AES-CBC-128 encryption.  Incorrect pad effects some vendor firmware
   implementations.
 - Send IPMI 2.0 packets differently than IPMI 1.5 packets, as the
   former does not require legacy pad data to be appended to payloads.
 - Fix Intel OEM SEL buffer overflow.
 - Fix out of trunk source build.
 - Support new ipmi_rmcpplus_sendto() and ipmi_rmcpplus_recvfrom()
   functions.
 - Support new HP Proliant DL160 G8 OEM sensor events.

* Thu Feb 28 2013 Ales Ledvinka <aledvink@redhat.com> - 1.2.5-1
- Updated to freeipmi-1.2.5:
 - Support Supermicro X9SPU-F-O OEM sensors and events.
 - Support Supermicro X9DRI-LN4F+ OEM intepretations (previously
   forgotten).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 Ales Ledvinka <aledvink@redhat.com> - 1.2.4-1
- Updated to freeipmi-1.2.4:
 - Support Supermicro X9DRI-LN4F+ OEM sensors and events.
 - Fix output corner case for "session-based" channels.
 - Fix ipmi-oem set-power-restore-delay corner case in time settings.
 - Fix ipmiseld memleak.
 - Fix libfreeipmi potential fd leak when generating random numbers.
 - Fix libfreeipmi error output bug in RMCP interface.
 - Fix several minor corner cases discovered by static code analysis.

* Thu Nov 15 2012 Ales Ledvinka <aledvink@redhat.com> - 1.2.3-1
- Updated to freeipmi-1.2.3:
 - In ipmi-oem, support new Dell Poweredge R720 OEM commands extensions,
   including:
  - get-nic-selection-failover
  - set-nic-selection-failover
  - power-monitoring-over-interval
  - power-monitoring-interval-range
  - get-last-post-code
 - In ipmi-oem, update active-lom-status for Dell Poweredge R720.
 - In ipmi-oem, support new Dell Poweredge R720 get-system-info option
   'cmc-info'.
 - In ipmi-oem, Dell get-system-info "slot-number" key changed to
   "blade-slot-info".  Legacy option still supported.
 - In ipmi-sel, support Dell Poweredge R720 OEM SEL extensions.
 - In all tools, support nochecksumcheck workaround option.
 - In all daemons (ipmiseld, ipmidetectd, bmc-watchdog), check for
   syscall errors during daemon setup.

 - In libfreeipmi, support Dell R720 OEM extension intepretations.
 - In libfreeipmi, libipmimonitoring, and libipmiconsole, support
   NO_CHECKSUM_CHECK workaround flag.
 - In libipmiconsole, IPMICONSOLE_DEBUG_FILE logs debug to files in
   current working directory and not /var/log.  PID is also appended to
   debug files.

* Fri Oct 12 2012 Ales Ledvinka <aledvink@redhat.com> - 1.2.2-1
- Updated to freeipmi-1.2.2:
 - Support new --sol-payload-instance and --deactivate-all-instances
   options in ipmiconsole.
 - Fix ipmiseld compile issue with -Werror=format-security.

* Mon Aug 27 2012 Jan Safranek <jsafrane@redhat.com> - 1.2.1-1
- Reworked RPM scriptlets to use systemd-rpm macros (#850117).
- Updated to freeipmi-1.2.1:
 - Support new ipmiseld daemon, a daemon that regularly polls the SEL
   and stores the events to the local syslog.
 - In ipmipower, support --oem-power-type option to support OEM
   specific power control operations.  Included in this support were
   the follow changes to ipmipower:
   - Support initial OEM power type of C410X.
   - Re-architect to allow input of extra information for an OEM power
     operation via the '+' operator after the hostname.
   - Re-architect to allow input of target hostname multiple times
     under OEM power cases.
   - Re-architect to allow serialization of power control operations to
     the same host.
 - Globally in tools, support --target-channel-number and
   --target-slave-address to specify specific targets.
 - Globally in tools, support ability to specify alternate port via
   optional [:port] in hostname or host config.
 - In ipmi-fru, support --bridge-fru option to allow reading FRU entries
   from satellite controllers.
 - In bmc-config, add configuration support for
   Maximum_Privilege_Cipher_Suite_Id_15 under RMCPplus_Conf_Privilege.
 - Globally support Cipher Suite ID 15 and 16 based on comments from
   Intel.
 - In ipmi-sensors, support --output-sensor-thresholds, to allow
   outputting of sensor thresholds in default output for scripting.
 - In ipmi-sel, support new --post-clear option.
 - In bmc-device, support new --set-sensor-reading-and-event-status
   option.
 - In ipmi-oem, support additional Intel Node Manager commands,
   including:
   - get-node-manager-capabilities
   - node-manager-policy-control 
   - get-node-manager-policy
   - set-node-manager-policy
   - remove-node-manager-policy
   - get-node-manager-alert-thresholds
   - set-node-manager-alert-thresholds
   - get-node-manager-policy-suspend-periods
   - set-node-manager-policy-suspend-periods
   - set-node-manager-power-draw-range
 - In ipmi-oem, support Wistron OEM commands extensions.
 - In ipmi-sel, support Wistron OEM SEL interpretations.
 - In ipmi-fru, support Wistron OEM FRU records.
 - In ipmi-pef-config, support configuration volatile Alert String 0
   and Lan Alert Destination 0.

* Tue Jul 31 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.7-1
- Updated to freeipmi-1.1.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.6-3
- fixed License to GPLv3+

* Tue Jul 17 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.6-2
- fixed upstream URL

* Fri Jun 29 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.6-1
- Updated to freeipmi-1.1.6

* Fri May 18 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.5-1
- Updated to freeipmi-1.1.5

* Fri Apr 20 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.4-1
- Updated to freeipmi-1.1.4

* Wed Mar  7 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.3-1
- Updated to freeipmi-1.1.3

* Wed Feb  8 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.2-1
- Updated to freeipmi-1.1.2

* Fri Jan  6 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.1-2
- added systemd unit files (#767611)

* Wed Jan  4 2012 Jan Safranek <jsafrane@redhat.com> - 1.1.1-1
- Updated to freeipmi-1.1.1

* Wed Dec 14 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.10-1
- Updated to freeipmi-1.0.10

* Tue Nov 22 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.9-1
- Updated to freeipmi-1.0.9

* Thu Oct 27 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.8-1
- enable build on all archs, the iopl issue #368541 is fixed
- Updated to freeipmi-1.0.8

* Thu Sep 29 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.7-1
- Updated to freeipmi-1.0.7

* Mon Sep  5 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.6-1
- Updated to freeipmi-1.0.6

* Fri Jul  1 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.5-1
- Updated to freeipmi-1.0.5

* Fri Apr 22 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.4-1
- Updated to freeipmi-1.0.4

* Wed Mar 30 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.3-1
- Updated to freeipmi-1.0.3, see announce at
  http://lists.gnu.org/archive/html/freeipmi-users/2011-03/msg00017.html

* Wed Feb 23 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.2-1
- Updated to freeipmi-1.0.2, see announce at
  http://lists.gnu.org/archive/html/freeipmi-users/2011-02/msg00027.html

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Jan Safranek <jsafrane@redhat.com> - 1.0.1:1
- Updated to freeipmi-1.0.1, see announce at
  http://lists.gnu.org/archive/html/freeipmi-users/2011-01/msg00006.html
- Configuration files moved from /etc/ to /etc/freeipmi/. Support legacy config
  files for backwards compatibility.
- More detailed release information can be found in the NEWS file.

