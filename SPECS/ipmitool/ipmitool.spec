%global        gitname     IPMITOOL
%global        gitversion  1_8_19

Name:          ipmitool
Summary:       Utility for IPMI control
Version:       1.8.19
Release:       1%{?dist}
License:       BSD
Vendor:        Microsoft Corporation
Distribution:  Mariner
URL:           https://github.com/ipmitool/ipmitool

Source0:       https://github.com/%{name}/%{name}/archive/%{gitname}_%{gitversion}/%{name}-%{version}.tar.gz
Source1:       openipmi-ipmievd.sysconf
Source2:       ipmievd.service
Source3:       exchange-bmc-os-info.service
Source4:       exchange-bmc-os-info.sysconf
Source5:       set-bmc-url.sh
Source6:       exchange-bmc-os-info
# https://www.iana.org/assignments/enterprise-numbers.txt
Source7:       enterprise-numbers
 
# https://github.com/ipmitool/ipmitool/issues/170
Patch1:       ipmitool-1.8.19-set-kg-key.patch
Patch2:       0004-slowswid.patch
Patch3:       0005-sensor-id-length.patch
Patch4:       0007-check-input.patch

BuildRequires: openssl-devel readline-devel ncurses-devel
%{?systemd_requires}
BuildRequires: systemd
# bootstrap
BuildRequires: automake autoconf libtool
Obsoletes: OpenIPMI-tools < 2.0.14-3
Provides: OpenIPMI-tools = 2.0.14-3


%description
This package contains a utility for interfacing with devices that support
the Intelligent Platform Management Interface specification.  IPMI is
an open standard for machine health, inventory, and remote power control.

This utility can communicate with IPMI-enabled devices through either a
kernel driver such as OpenIPMI or over the RMCP LAN protocol defined in
the IPMI specification.  IPMIv2 adds support for encrypted LAN
communications and remote Serial-over-LAN functionality.

It provides commands for reading the Sensor Data Repository (SDR) and
displaying sensor values, displaying the contents of the System Event
Log (SEL), printing Field Replaceable Unit (FRU) information, reading and
setting LAN configuration, and chassis power control.


%package -n ipmievd
Requires: %{name} = %{version}-%{release}
%{?systemd_requires}
BuildRequires: systemd
Summary: IPMI event daemon for sending events to syslog
%description -n ipmievd
ipmievd is a daemon which will listen for events from the BMC that are
being  sent to the SEL and also log those messages to syslog.


%package -n bmc-snmp-proxy
Requires: net-snmp
Requires: exchange-bmc-os-info
BuildArch: noarch
Summary: Reconfigure SNMP to include host SNMP agent within BMC
%description -n bmc-snmp-proxy
Given a host with BMC, this package would extend system configuration
of net-snmp to include redirections to BMC based SNMP.


%package -n exchange-bmc-os-info
Requires: net-tools
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%{?systemd_requires}
BuildRequires: systemd

Summary: Let OS and BMC exchange info

%description -n exchange-bmc-os-info
Given a host with BMC, this package would pass the hostname &
OS information to the BMC and also capture the BMC ip info
for the host OS to use.


%prep
%autosetup -n %{name}-%{gitname}_%{gitversion} -p1

for f in AUTHORS ChangeLog; do
    iconv -f iso-8859-1 -t utf8 < ${f} > ${f}.utf8
    mv ${f}.utf8 ${f}
done

%build
# --disable-dependency-tracking speeds up the build
# --enable-file-security adds some security checks
# --disable-intf-free disables FreeIPMI support - we don't want to depend on
#   FreeIPMI libraries, FreeIPMI has its own ipmitoool-like utility.

# begin: release auto-tools
# Used to be needed by aarch64 support, now only cxoem patch makefiles are left.
aclocal
libtoolize --automake --copy
autoheader
automake --foreign --add-missing --copy
aclocal
autoconf
automake --foreign
# end: release auto-tools

install -Dm 644 %{SOURCE7} .
%configure --disable-dependency-tracking --enable-file-security --disable-intf-free
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -Dpm 644 %{SOURCE2} %{buildroot}%{_unitdir}/ipmievd.service
install -Dpm 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/ipmievd
install -Dm 644 %{SOURCE3} %{buildroot}%{_unitdir}/exchange-bmc-os-info.service
install -Dm 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/exchange-bmc-os-info
install -Dm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/profile.d/set-bmc-url.sh
install -Dm 755 %{SOURCE6} %{buildroot}%{_libexecdir}/exchange-bmc-os-info


install -Dm 644 contrib/bmc-snmp-proxy.sysconf %{buildroot}%{_sysconfdir}/sysconfig/bmc-snmp-proxy
install -Dm 644 contrib/bmc-snmp-proxy.service %{buildroot}%{_unitdir}/bmc-snmp-proxy.service
install -Dm 755 contrib/bmc-snmp-proxy         %{buildroot}%{_libexecdir}/bmc-snmp-proxy

%post -n ipmievd
%systemd_post ipmievd.service

%preun -n ipmievd
%systemd_preun ipmievd.service

%postun -n ipmievd
%systemd_postun_with_restart ipmievd.service

%post -n exchange-bmc-os-info
%systemd_post exchange-bmc-os-info.service

%preun -n exchange-bmc-os-info
%systemd_preun exchange-bmc-os-info.service

%postun -n exchange-bmc-os-info
%systemd_postun_with_restart exchange-bmc-os-info.service


%triggerun -- ipmievd < 1.8.11-7
# Save the current service runlevel info
# User must manually run systemd-sysv-convert --apply ipmievd
# to migrate them to systemd targets
/usr/bin/systemd-sysv-convert --save ipmievd >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del ipmievd >/dev/null 2>&1 || :
/bin/systemctl try-restart ipmievd.service >/dev/null 2>&1 || :

%files
%{_bindir}/ipmitool
%{_mandir}/man1/ipmitool.1*
%doc %{_datadir}/doc/ipmitool
%{_datadir}/ipmitool
%{_datadir}/misc/enterprise-numbers

%files -n ipmievd
%config(noreplace) %{_sysconfdir}/sysconfig/ipmievd
%{_unitdir}/ipmievd.service
%{_sbindir}/ipmievd
%{_mandir}/man8/ipmievd.8*

%files -n exchange-bmc-os-info
%config(noreplace) %{_sysconfdir}/sysconfig/exchange-bmc-os-info
%{_sysconfdir}/profile.d/set-bmc-url.sh
%{_unitdir}/exchange-bmc-os-info.service
%{_libexecdir}/exchange-bmc-os-info

%files -n bmc-snmp-proxy
%config(noreplace) %{_sysconfdir}/sysconfig/bmc-snmp-proxy
%{_unitdir}/bmc-snmp-proxy.service
%{_libexecdir}/bmc-snmp-proxy

%changelog
* Fri Jan 05 2024 Muhammad Falak <mwani@microsoft.com> - 1.8.19-1
- Upgrade version to 1.8.19
- Drop un-needed patches

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.8.18-22
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jun 19 2020 Andrew Phelps <anphel@microsoft.com> - 1.8.18-21
- Require net-tools instead of hostname

* Wed Jun 17 2020 Joe Schmitt <joschmit@microsoft.com> - 1.8.18-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- License verified.
- Update URL.

* Thu Feb 06 2020 Václav Doležal <vdolezal@redhat.com> - 1.8.18-19
- Backport fix for CVE-2020-5208 (#1798722); for details see
  https://github.com/ipmitool/ipmitool/security/advisories/GHSA-g659-9qxw-p7cp

* Mon Feb 03 2020 Václav Doležal <vdolezal@redhat.com> - 1.8.18-18
- Backport patch to autoselect best cipher suite when working over lanplus backend
- Fixed 'ipmitool pef status/info' not printing final newline
- Expanded column for sensor name in 'ipmi sdr/sensor' output so longer names are aligned

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Václav Doležal <vdolezal@redhat.com> - 1.8.18-16
- Fix FTBFS with GCC 10

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.18-14
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Apr 10 2018 Josef Ridky <jridky@redhat.com> - 1.8.18-11
- Project moved to github

* Thu Feb 22 2018 Josef Ridky <jridky@redhat.com> - 1.8.18-10
- Spec clean up
- Add support to set kg key
- Fix DDR4 memory issues
- Increase length of sensor id
- Enable usb interface by default
- Fix input options 

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Josef Ridky <jridky@redhat.com> - 1.8.18-8
- remove old systemd dependencies

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 21 2017 Josef Ridky <jridky@redhat.com> - 1.8.18-5
- Fix allocation issue

* Tue Feb 21 2017 Josef Ridky <jridky@redhat.com> - 1.8.18-4
- Add support for OpenSSL-1.1.0 library (#1423743)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.8.18-2
- Rebuild for readline 7.x

* Mon Oct 10 2016 Boris Ranto <branto@redhat.com> - 0:1.8.18-1
- New version (0:1.8.18-1)
- CVE-2011-4339 OpenIPMI

* Tue May 10 2016 Boris Ranto <branto@redhat.com> - 0:1.8.17-1
- New version (0:1.8.17-1)
- CVE-2011-4339 OpenIPMI

* Tue Feb 23 2016 Boris Ranto <branto@redhat.com> - 1.8.16-1
- Rebase to version 1.8.16

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Boris Ranto <branto@redhat.com> - 1.8.15-5
- Split ipmievd bits into a separate package

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 Ales Ledvinka <aledvink@redhat.com> 1.8.15-3
- Remove modalias dependency.

* Thu Mar 19 2015 Ales Ledvinka <aledvink@redhat.com> 1.8.15-1
- Upstream release 1.8.15

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr  8 2014 Ales Ledvinka <aledvink@redhat.com> 1.8.13-4
- Support for environment variable short options.

* Tue Nov  5 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.13-3
- Cleanup of dual bridge option.

* Tue Oct 15 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.13-2
- BMC SNMP agent redirection

* Mon Oct 14 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.13-1
- Upstream release 1.8.13

* Fri Aug 09 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.12-13073103
- Avoid FIPS mode crashes if possible.
- Document FIPS limitations.

* Wed Jul  31 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.12-13073101
- Include current upstream bugfixes.

* Thu Jul 25 2013 Ales Ledvinka <aledvink@redhat.com> 1.8.12-16
- Calxeda OEM extensions.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.8.12-14
- Updated the exchange-bmc-os-info's service file with Requires stmt

* Fri Dec 14 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-13
- fixed argument parsing leaks
- ask user for password only once and do so only when interactive password
  is the chosen password method.

* Thu Dec 13 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.8.12-12
- Removed the extra symbols in the patch, as the build is failing.

* Thu Dec 13 2012 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.8.12-11
- Subpackage for exchange-bmc-os-info as it requires OPenIPMI

* Wed Dec 12 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-10
- documented fixed and conditional defaults. adjusted synopsis

* Tue Dec 4 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-9
- fixed ipmitool documentation

* Fri Nov 30 2012 Praveen K Paladugu <praveen_paladugu@dell.com> 1.8.12-8
- service & scripts to allow OS to capture BMC's IP & URL info
- Also pass the OS information to BMC
- patches submitted by Charles Rose (charles_rose[at]dell.com)

* Fri Nov 16 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-7
- failed sol session activation crashes while logging exit

* Fri Nov 16 2012 Ales Ledvinka <aledvink@redhat.com> 1.8.12-6
- revert default cipersuite back to 3 which includes integrity and confidentiality

* Thu Oct 18 2012 Dan Horák <dan[at]danny.cz> - 1.8.12-5
- fix build on big endian arches

* Wed Oct 17 2012 Ales Ledvinka <aledvink@redhat.cz> 1.8.12-4
- support setting OS name and Hostname on BMC

* Tue Sep 04 2012 Dan Horák <dan[at]danny.cz> - 1.8.12-3
- fix build on big endian arches

* Mon Aug 27 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.12-2
- Fixed starting ipmievd under systemd (#819234).
- Updated RPM scriplets with latest systemd-rpm macros (#850161)

* Fri Aug 10 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.12-1
- update to ipmitool-1.8.12

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.11-11
- start ipmievd.service after ipmi (#819234)

* Thu Apr 26 2012 Jan Safranek <jsafrane@redhat.com> - 1.8.11-10
- fixed ipmievd.service systemd unit (#807757)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Jan Safranek <jsafrane@redhat.com> - 1.8.11-8
- fixed CVE-2011-4339

* Mon Sep 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.11-7
- convert to systemd

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 Jan Safranek <jsafrane@redhat.com> - 1.8.11-5
- Fixed exit code of ipmievd initscript with wrong arguments

* Mon Nov  2 2009 Jan Safranek  <jsafrane@redhat.com> 1.8.11-4
- fix ipmievd initscript 'condrestart' action (#532188)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.8.11-3
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Jan Safranek <jsafrane@redhat.com> 1.8.11-1
- updated to new version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 1.8.10-3
- rebuild with new openssl

* Tue Oct 14 2008 Jan Safranek <jsafrane@redhat.com> 1.8.10-2
- fix issues found during package review:
  - clear Default-Start: line in the init script, the service should be 
    disabled by default
  - added Obsoletes: OpenIPMI-tools
  - compile with --disable-dependency-tracking to speed things up
  - compile with --enable-file-security
  - compile with --disable-intf-free, don't depend on FreeIPMI libraries
    (FreeIPMI has its own ipmitool-like utility)

* Mon Oct 13 2008 Jan Safranek <jsafrane@redhat.com> 1.8.10-1
- package created, based on upstream .spec file
