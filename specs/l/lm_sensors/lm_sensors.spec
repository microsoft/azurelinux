# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: lm_sensors
Version: 3.6.0
Release: 23%{?dist}
Summary: Hardware monitoring tools

%define upstream_version %(echo %{version} | sed -e 's/\\./-/g')

# Some man pages are licensed Linux-man-pages-copyleft-var and Linux-man-pages-copyleft (lib/sensors.conf.5,
# prog/sensors/sensors.1). Files from dist-git are licensed
# MIT (according to the Fedora Project Contributor Agreement
# https://docs.fedoraproject.org/en-US/legal/fedora-linux-license/).
# lib/* are LGPL-2.1-or-later (in subpackage)
# The rest is GPL-2.0-or-later.
License: GPL-2.0-or-later AND Linux-man-pages-copyleft-var AND Linux-man-pages-copyleft AND MIT

URL: http://github.com/lm-sensors/lm-sensors/

Source0: https://github.com/lm-sensors/lm-sensors/archive/V%{upstream_version}/lm-sensors-%{upstream_version}.tar.gz
Source1: lm_sensors.sysconfig
# This one was taken from PLD-linux, Thanks!
Source2: sensord.sysconfig
Source3: lm_sensors-modprobe-wrapper
Source4: lm_sensors-modprobe-r-wrapper
Source5: sensord.service
Source6: sensord-service-wrapper
Source7: lm_sensors.service
Source8: lm_sensors-wrapper

# Downstream-only:
Patch0: 0001-Revert-unnecessary-soname-bump.patch

# Upstream patch:
Patch1: 0001-Change-PIDFile-path-from-var-run-to-run.patch
Patch2: lm_sensors-3.6.0-allow_no_sensors.patch
# Upstream commit 5deee7d0c301df779:
Patch3: lm_sensors-3.6.0-sensors-detect-Add-support-for-AMD-CPU-Family-19h.patch
# rrdtool has constified all argv
Patch4: lm_sensors-3.6.0-rrd-const-argv.patch

Requires: /usr/sbin/modprobe
%ifarch %{ix86} x86_64
Requires: /usr/sbin/dmidecode
%endif
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires(post): systemd-units
BuildRequires: kernel-headers >= 2.2.16, bison, flex, gawk
BuildRequires: perl-generators
BuildRequires: rrdtool-devel
BuildRequires: gcc
BuildRequires: make


%description
The lm_sensors package includes a collection of modules for general SMBus
access and hardware monitoring.


%package libs
Summary: Lm_sensors core libraries
License: LGPL-2.1-or-later

%description libs
Core libraries for lm_sensors applications


%package devel
Summary: Development files for programs which will use lm_sensors
Requires: %{name}-libs = %{version}-%{release}
# One manual page is licensed Linux-man-pages-copyleft (lib/libsensors.3). The rest is LGPLv2+.
License: LGPL-2.1-or-later AND Linux-man-pages-copyleft

%description devel
The lm_sensors-devel package includes a header files and libraries for use
when building applications that make use of sensor data.


%package sensord
Summary: Daemon that periodically logs sensor readings
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
# One man page is licensed Linux-man-pages-copyleft (prog/sensord/sensord.8). Files from
# dist-git are licensed MIT according to the FPCA. The rest is GPLv2+.
License: GPL-2.0-or-later AND Linux-man-pages-copyleft AND MIT

%description sensord
Daemon that periodically logs sensor readings to syslog or a round-robin
database, and warns of sensor alarms.


%prep
%setup -q -n lm-sensors-%{upstream_version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%patch -P4 -p1
%endif

# Remove currently unused files to make sure we've got the license right
rm -f prog/init/sysconfig-lm_sensors-convert prog/hotplug/unhide_ICH_SMBus

mv prog/init/README prog/init/README.initscripts
chmod -x prog/init/fancontrol.init

# fixing the sensord-service-wrapper path
cp -p %{SOURCE5} sensord.service
cp -p %{SOURCE7} lm_sensors.service
sed -i "s|\@WRAPPER_DIR\@|%{_libexecdir}/%{name}|" sensord.service
sed -i "s|\@WRAPPER_DIR\@|%{_libexecdir}/%{name}|" lm_sensors.service

sed -i 's|SBINDIR := \$(PREFIX)/sbin|SBINDIR := %_sbindir|' Makefile

%build
%set_build_flags
%{make_build} PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} ETCDIR=%{_sysconfdir} \
  EXLDFLAGS="$LDFLAGS" PROG_EXTRA=sensord BUILD_STATIC_LIB=0 user


%install
make PREFIX=%{_prefix} LIBDIR=%{_libdir} MANDIR=%{_mandir} ETCDIR=%{_sysconfdir} PROG_EXTRA=sensord \
  DESTDIR=$RPM_BUILD_ROOT BUILD_STATIC_LIB=0 user_install

ln -s sensors.conf.5.gz $RPM_BUILD_ROOT%{_mandir}/man5/sensors3.conf.5.gz

mkdir -p $RPM_BUILD_ROOT%{_initrddir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sensors.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/lm_sensors
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/sensord

# service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -pm 644 prog/init/fancontrol.service $RPM_BUILD_ROOT%{_unitdir}
install -pm 644 lm_sensors.service           $RPM_BUILD_ROOT%{_unitdir}
install -pm 644 sensord.service              $RPM_BUILD_ROOT%{_unitdir}

# customized modprobe calls
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/%{name}
install -pm 755 %{SOURCE3} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lm_sensors-modprobe-wrapper
install -pm 755 %{SOURCE4} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lm_sensors-modprobe-r-wrapper
install -pm 755 %{SOURCE8} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lm_sensors-wrapper

# sensord service wrapper
install -pm 755 %{SOURCE6} $RPM_BUILD_ROOT%{_libexecdir}/%{name}/sensord-service-wrapper


# Note non standard systemd scriptlets, since reload / stop makes no sense
# for lm_sensors
%triggerun -- lm_sensors < 3.3.0-2
if [ -L /etc/rc3.d/S26lm_sensors ]; then
    /bin/systemctl enable lm_sensors.service >/dev/null 2>&1 || :
fi
/sbin/chkconfig --del lm_sensors

# ===== main =====

%post
%systemd_post lm_sensors.service

%preun
%systemd_preun lm_sensors.service

%postun
%systemd_postun_with_restart lm_sensors.service

# ==== sensord ===

%post sensord
%systemd_post sensord.service

%preun sensord
%systemd_preun sensord.service

%postun sensord
%systemd_postun_with_restart sensord.service

# ===== libs =====

%ldconfig_scriptlets libs


%files
%license COPYING
%doc CHANGES CONTRIBUTORS doc README*
%doc prog/init/fancontrol.init prog/init/README.initscripts
%config %{_sysconfdir}/sensors3.conf
%config(noreplace) %{_sysconfdir}/sysconfig/lm_sensors
%dir %{_sysconfdir}/sensors.d
%{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%if "%{_sbindir}" != "%{_bindir}"
%{_sbindir}/*
%endif
%{_unitdir}/lm_sensors.service
%{_unitdir}/fancontrol.service
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/lm_sensors-modprobe*wrapper
%{_libexecdir}/%{name}/lm_sensors-wrapper
%exclude %{_sbindir}/sensord
%exclude %{_mandir}/man8/sensord.8.gz

%files libs
%{_libdir}/*.so.*
%license COPYING.LGPL

%files devel
%{_includedir}/sensors
%{_libdir}/lib*.so
%{_mandir}/man3/*

%files sensord
%doc prog/sensord/README
%{_sbindir}/sensord
%{_mandir}/man8/sensord.8.gz
%config(noreplace) %{_sysconfdir}/sysconfig/sensord
%{_unitdir}/sensord.service
%{_libexecdir}/%{name}/sensord-service-wrapper


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.6.0-21
- Rebuilt for the bin-sbin merge (2nd attempt)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.6.0-19
- Rebuilt for the bin-sbin merge

* Tue Feb 13 2024 Joe Orton <jorton@redhat.com> - 3.6.0-18
- SPDX migration (Miroslav Suchý)

* Sun Feb 11 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 3.6.0-17
- Adapt to constification of argv parameters in rrdtool

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 9 2021 Artem Egorenkov <aegorenk@redhat.com> - 3.6.0-9
- Add support for AMD CPU Family 19h

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.6.0-8
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Sun Feb 14 2021 Artem Egorenkov <aegorenk@redhat.com> - 3.6.0-7
- New flag for no sensors added. This flag is used in VM environment
  to make sensors binaries not fail if no sensors was detected.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 Ondřej Lysoněk <olysonek@redhat.com> - 3.6.0-5
- Fix systemd warning about use of /var/run
- Resolves: rhbz#1869421

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Tom Stellard <tstellar@redhat.com> - 3.6.0-2
- Use make_build macro

* Fri Oct 18 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.6.0-1
- New version

* Thu Aug 15 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.5.0-6
- Add detection support for AMD family 17h model 70h
- Add detection support for Nuvoton NCT6797D
- Resolves: rhbz#1740735

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 06 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.5.0-4
- Added explicit Requires on lm_sensors-libs

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.5.0-2
- Detect AMD Rome - Family 17h model 30h

* Wed Jan 02 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.5.0-1
- New version
- Resolves: rhbz#1653259

* Fri Sep 28 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.0-18.20180522git70f7e08
- Drop unneeded build dependency on libsysfs-devel

* Tue Jul 17 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.0-17.20180522git70f7e08
- Corrected the License tag

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-16.20180522git70f7e08
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 25 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.0-15.20180522git70f7e08
- New version

* Fri May 04 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.0-14
- Add detection of AMD Ryzen w/ Vega graphics
- Resolves: rhbz#1573399
- Covscan fixes

* Fri Apr 20 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.0-13
- Detect AMD Family 17h thermal sensors
- Resolves: rhbz#1569542

* Thu Apr 12 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.0-12
- Use LDFLAGS when linking executables
- Resolves: rhbz#1548691

* Mon Apr 09 2018 Rafael Santos <rdossant@redhat.com> - 3.4.0-11
- Use standard Fedora build and linker flags (bug #1548691)

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.0-10
- Add gcc to BuildRequires

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May 15 2016 Hans de Goede <hdegoede@redhat.com> - 3.4.0-5
- Rebuilt for new librrd

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Aug 20 2015 Jaromir Capik <jcapik@redhat.com> - 3.4.0-3
- Removing 'noreplace' for sensors3.conf (#1239216)

* Tue Aug 04 2015 Jaromir Capik <jcapik@redhat.com> - 3.4.0-2
- Adding /etc/sensors.d in the %%files (#1236309)

* Thu Jun 25 2015 Jaromir Capik <jcapik@redhat.com> - 3.4.0-1
- Updating to 3.4.0 (#1235660)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Jan 25 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.3.5-3
- Own the %%{_libexecdir}/lm_sensors dir.
- Fix case of Public Domain in license tag.

* Fri Jan 24 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.5-2
- systemd units rework

* Thu Jan 23 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.5-1
- Update to 3.3.5 (#1056448)

* Sun Jan 19 2014 Ville Skyttä <ville.skytta@iki.fi> - 3.3.4-11
- Do not order services after syslog.target.

* Fri Jan 10 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.4-10
- Enhancing the sensord service wrapper (#863986)
- UsrMove and libexec path tunings

* Thu Jan 09 2014 Jaromir Capik <jcapik@redhat.com> - 3.3.4-9
- Introducing sensord service wrapper (#949521)

* Mon Sep 09 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.4-8
- Fixing use of uninitialized 'vendor_id' value on ppc (#996590)
- Fixing bogus date in the changelog

* Wed Aug 07 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.4-7
- Fixing the license tag

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 3.3.4-6
- Perl 5.18 rebuild

* Thu Aug 01 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.4-5
- RH man page scan (#948520)

* Tue Jul 30 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.4-4
- Avoiding modprobe errors when no sensors configured (#834215)
- Introducing fancontrol service file (#988922)
- Replacing hardcoded systemd unit path with _unitdir macro

* Thu Jul 25 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.4-3
- Avoiding warnings when piping /dev/null to sensors-detect (#843507)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 3.3.4-2
- Perl 5.18 rebuild

* Wed May 29 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 17 2013 Jaromir Capik <jcapik@redhat.com> - 3.3.3-2
- Fixing sensors-detect to avoid failures when the /dev/port is missing (#843521)

* Thu Dec 06 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Wed Sep 26 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.2-5
- #856120 - sensors - Inconsistency between man page and help

* Mon Aug 27 2012 Jaromir Capik <jcapik@redhat.com> - 3.3.2-4
- Migration to new systemd scriptlet macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 02 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 3.3.2-2
- rhbz#806364 - sensors-detect fails with "/sys/bus/pci/devices: No such file or directory at /usr/sbin/sensors-detect line 2895"
  PCI bus is always required even if it might be missing on
  some platforms. So don't choke is it is missing. Patch from
  Jaromir Capik

* Thu Mar 15 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 3.3.2-1
- upstream lm-sensors-3.3.2

* Mon Feb 13 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 3.3.1-3
- 789761 - Provide native systemd service

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 22 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 3.3.1-1
- new upstream release 3.3.1

* Sun Apr 24 2011 Hans de Goede <hdegoede@redhat.com> - 3.3.0-2
- Fix sensors-detect with the udevdb now living under /run (#697565)
- Provide a native systemd service file (#692159)
- Drop systemv initscript
- Drop configuration conversion scripts, the last Fedora with lm_sensors-2.x
  was Fedora 8 ! 

* Tue Mar 29 2011 Nikola Pajkovsky <npajkovs@redhat.com> - 3.3.0
- new upstream release 3.3.0
- Resolved: 691548 - include empty /etc/sensors.d into the package

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.2.0
- new upstream release 3.2.0
- change lincese to LGPLv2.1

* Fri Sep 03 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.2.svn5857
- update lm_sensors from svn
- drop patch lm_sensors-3.1.2-lm85.patch(already in svn)

* Wed Mar 31 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.2-2
- patch lm_sensors-3.1.2-lm85.patch add into sensors-detect driver lm85
- Resolved: 578527 - sensors-detect fails to detect

* Wed Feb 3 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.2-1
- new upstream release
- drop sensors-detect, beacuse it was taken form svn(531126)

* Thu Dec 17 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 3.1.1-7
- Resovles: #226101 - Merge Review: lm_sensors

* Tue Nov 10 2009 Dennis Gilmore <dennis@ausil.us> - 3.1.1-6
- remove Excludearch s390 s390x

* Tue Nov 10 2009 Nikola Pajkovsky <n.pajkovsky@gmail.com> - 3.1.1-5
- Resolved: 531126 - sensors-detect gives perl uninitialized var warnings

* Wed Sep 30 2009 Hans de Goede <hdegoede@redhat.com> 3.1.1-4
- Create a sensor3.conf.5 symlink to the sensors.conf.5 manpage (#526178)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Adam Jackson <ajax@redhat.com> 3.1.1-2
- Add -libs subpackage so perl doesn't get dragged in just for linking
  against libsensors.

* Tue Jul  7 2009 Nikola Pajokvsky <npajovs@redhat.com> 3.1.1-1
- New release 3.1.1

* Sun Mar  8 2009 Hans de Goede <hdegoede@redhat.com> 3.1.0-1
- New upstream release 3.1.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan  1 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.3-1
- New upstream release 3.0.3
- Add a patch to support drivers with an ACPI "bus" (new Asus atk0110 drv)

* Tue Jul  1 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.2-1
- New upstream release 3.0.2
- This release contains various important fixes to sensors-detect, which made
  it unsafe to run sensors-detect on certain systems
- Drop all patches (all upstreamed)

* Sat Jun 14 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-6
- Rebuild for new rrdtool

* Sun Mar 16 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-5
- Make libsensors work with hwmon class entries without a device link
  such as the acpi thermal_zone driver (bz 437637)

* Wed Mar 12 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-4
- One (last) minor cosmetical fix to the initscript

* Tue Feb 26 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-3
- Some improvements to the lsb-retcodes and service-default-off patches
  from a review by upstream

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.1-2
- Autorebuild for GCC 4.3

* Mon Feb 11 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.1-1
- New upstream release 3.0.1
- Drop several patches which are included in the new upstream release
- Add a patch to make the initscript returncodes LSB compliant (bug 431884)

* Tue Dec 18 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-3
- Fix sensors.conf errors with certain chips (patch send in by upstream)

* Thu Dec 13 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-2
- Fix sensord rdd mode (patch send in by upstream)

* Sat Nov 24 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 3.0.0-1
- New upstream release 3.0.0 (final)

* Sat Nov 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 3.0.0-0.1.rc3
- New upstream release 3.0.0-rc3
- Remove eeprommer sub-package as eeprommer (and the other i2c-tools)
  have moved to the new i2c-tools package

* Wed Aug 22 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.10.4-2
- Update License tag for new Licensing Guidelines compliance
- Disable service by default (no use without any sensors being configured),
  enable it automatically on a successfull sensors-detect run (bz 253750)

* Thu Jul 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.10.4-1
- New upstream release 2.10.4
- Drop upstreamed patches 4, 5, 7 and 8
- Drop no longer need patch 3
- Move libsensors.3 manpage to -devel sub-package
- Move sensord.8 manpage to -sensord sub-package
- Switch from ExclusiveArch: alph ix86 x86_64, to ExcludeArch: s390 s390x,
  so that we get build on ppc, arm, etc. too. (bz 181037 amongst others)

* Mon Jul  9 2007 Hans de Goede <j.w.r.degoede@hhs.nl> - 2.10.3-3
- Remove no longer needed patches 1, 2 & 6
- Various specfile cleanups to match the Fedora packaging guidelines
  this fixes bz 238787 amongst other things
- Use lm_sensors provided initscript instead of our own private one, this
  stops the sometimes unnecessary loading of i2c-dev
- No longer ship a static version of the library in -devel
- Compile sensord and eepromer extra programs and put each in its own
  subpackage (bz 236904)

* Tue Apr 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.10.3-2
- Fixed one more problem with sensors-detect (#215984)

* Tue Apr 17 2007 Phil Knirsch <pknirsch@redhat.com> - 2.10.3-1
- Update to lm_sensors-2.10.3

* Thu Mar 15 2007 Phil Knirsch <pknirsch@redhat.com> - 2.10.2-2
- Only require dmidecode on supported archs (#232264)

* Tue Feb 06 2007 Florian La Roche <laroche@redhat.com> - 2.10.2-1
- Update to lm_sensors-2.10.2

* Thu Nov 23 2006 Phil Knirsch <pknirsch@redhat.com> - 2.10.1-1.fc7
- Update to lm_sensors-2.10.1
- Tiny specfile updates

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.10.0-3.1
- rebuild

* Sun Jul 09 2006 Warren Togami <wtogami@redhat.com> 2.10.0-3
- change buildreq from sysfsutils-devel to libsysfs-devel (#198055)

* Mon Jun 05 2006 Jesse Keating <jkeating@redhat.com> 2.10.0-2
- Fix BuildRequires, added flex. (#193511)  Changed to Requires(post) and 
  (postun)

* Fri May 12 2006 Phil Knirsch <pknirsch@redhat.com> 2.10.0-1
- Update to lm_sensors-2.10.0
- Added missing buildprereq on sysfsutils-devel (#189196)
- Added missing prereq on chkconfig (#182838)
- Some fiddling to make it build on latest kernels

* Wed Feb 15 2006 Phil Knirsch <pknirsch@redhat.com> 2.9.2-2
- Added missing dependency to chkconfig

* Fri Feb 10 2006 Phil Knirsch <pknirsch@redhat.com> 2.9.2-1
- Update to lm_sensors-2.9.2
- Fixed wrong subsys locking (#176965)
- Removed lm_sensors pwmconfig, has been fixed upstream now

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.9.1-6.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 16 2006 Peter Jones <pjones@redhat.com> 2.9.1-6
- fix initscript subsys locking

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com> 2.9.1-5.1
- rebuilt for new gcj

* Tue Nov 08 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.1-5
- Fixed lm_sensors pwmconfig patch.

* Thu Sep 01 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.1-4
- Fixed CAN-2005-2672 lm_sensors pwmconfig insecure temporary file usage
  (#166673)
- Fixed missing optflags during build (#166910)

* Mon May 23 2005 Phil Knirsch <pknirsch@redhat.com> 2.9.1-3
- Update to lm_sensors-2.9.1
- Fixed wrong/missing location variables for make user
- Fixed missing check for /etc/modprobe.conf in sensors-detect (#139245)

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 2.8.8-5
- bump release and rebuild with gcc 4

* Tue Jan 11 2005 Dave Jones <davej@redhat.com> 2.8.8-4
- Add dependancy on dmidecode rather than the obsolete kernel-utils.
- Don't delete dmidecode from the buildroot.

* Thu Dec 23 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.8-2
- Fixed typo in initscript (#139030)

* Tue Dec 21 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.8-1
- Added Buildprereq for bison (#138888)
- Update to lm_sensors-2.8.8

* Thu Oct 14 2004 Harald Hoyer <harald@redhat.com> 2.8.7-2
- added initial /etc/sysconfig/lm_sensors
- added initscript
- MAKEDEV the initial i2c devices in initscript and sensors-detect

* Tue Jul 06 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.7-1
- Update to latest upstream version.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.6-1
- Update to latest upstream version.
- Enabled build for x86_64.

* Mon Mar 08 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.3-5
- Fixed initscript to work with 2.6 kernel and made it more quiet (#112286).
- Changed proposed location of sensors (#116496).
- Fixed rpath issue.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 05 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.3-3
- Modified sensors.conf to a noreplace config file.

* Wed Feb 04 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.3-2
- Fixed newly included initscript (#114608).

* Thu Jan 29 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.3-1
- Updated to latest upstream version 2.8.3

* Thu Jan 08 2004 Phil Knirsch <pknirsch@redhat.com> 2.8.2-1
- Update to latest upstream version 2.8.2
- Fixed wrong & usage in if expression.
- Included several new perl tools.

* Fri Oct 24 2003 Phil Knirsch <pknirsch@redhat.com> 2.8.1-1
- Update to latest upstream version 2.8.1

* Wed Jul 23 2003 Phil Knirsch <pknirsch@redhat.com> 2.8.0-1
- Update to latest upstream version 2.8.0

* Fri Jun 27 2003 Phil Knirsch <pknirsch@redhat.com> 2.6.5-6.1
- rebuilt

* Fri Jun 27 2003 Phil Knirsch <pknirsch@redhat.com> 2.6.5-6
- Included prog/init scripts and README (#90606).
- Require kernel-utils for dmidecode (#88367, #65057).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.6.5-5
- rebuilt

* Wed Dec 04 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.5-4
- Bump release and try to rebuild.

* Tue Dec  3 2002 Tim Powers <timp@redhat.com> 2.6.5-3
- don't include dmidecode, conflicts with kernel-utils

* Fri Nov 29 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.5-2
- Added patch to fix utf8 problem with sensors-detect.
- Fixed Copyright: to License: in specfile

* Fri Nov 29 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.5-1
- Updated userlevel to 2.6.5.
- Include all the /usr/sbin/ apps (like dmidecode).

* Fri Oct 04 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.3-3
- Removed Serverworks patch as it is already in sensors-detect.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.6.3-2
- automated rebuild

* Tue Jun 18 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.3-1
- Updated of userland package to 2.6.3
- Fixed file packaging bug (#66126).

* Thu May 23 2002 Tim Powers <timp@redhat.com> 2.6.2-2
- automated rebuild

* Mon Jan 28 2002 Phil Knirsch <pknirsch@redhat.com> 2.6.2-1
- Update to version 2.6.2

* Wed Aug 22 2001 Philipp Knirsch <pknirsch@redhat.de> 2.5.5-6
- Added the SMBus CSB5 detection (#50468)

* Mon Jul  9 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed duplicate Summary: entry for devel package (#47714)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Thu Feb 15 2001 Philipp Knirsch <pknirsch@redhat.de>
- Removed the i2c block patch as our newest kernel doesn't need it anymore.

* Mon Feb  5 2001 Matt Wilson <msw@redhat.com>
- added patch to not include sys/perm.h, as it's gone now.
- added alpha to ExclusiveArch
- use make "LINUX_HEADERS=/usr/include" to get kernel headers

* Tue Jan 16 2001 Philipp Knirsch <pknirsch@redhat.de>
- Updated to 2.5.5 which includes the Serverworks drivers. Kernel modules are
  not included though es they have to go into the kernel package
- Had to remove all references to I2C_SMBUS_I2C_BLOCK_DATA from
  kernel/busses/i2c-i801.c and prog/dump/i2cdump.c as this is not defined in
  our current kernel package

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- update to 2.5.4
- updated URL and Source entries to point to new home of lm-sensors
- rebuild

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix summary

* Fri Jul 28 2000 Harald Hoyer <harald@redhat.de>
- added static library to devel package

* Thu Jul 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2
- build against a kernel that actually has new i2c code in it

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- initial package without kernel support
