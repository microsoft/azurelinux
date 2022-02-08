#%%global prerelease rc
#%%global prereleasenum 1

%global prerel1 %{?prerelease:.%{prerelease}%{prereleasenum}}
%global prerel2 %{?prerelease:-%{prerelease}.%{prereleasenum}}

Summary:      A dynamic adaptive system tuning daemon
Name:         tuned
Version:      2.15.0
Release:      4%{?dist}
License:      GPLv2+
Vendor:       Microsoft Corporation
Distribution: Mariner
Source0:      https://github.com/redhat-performance/%{name}/archive/v%{version}%{?prerel2}/%{name}-%{version}%{?prerel2}.tar.gz
Patch0:       skip-gui-files.patch
URL:          http://www.tuned-project.org/
BuildArch:    noarch

BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: systemd

# BuildRequires for 'make test'
BuildRequires: python3-configobj
BuildRequires: python3-dbus
BuildRequires: python3-decorator
BuildRequires: python3-pyudev

Requires: dbus
Requires: ethtool
Requires: gawk
Requires: polkit
Requires: python3-configobj
Requires: python3-dbus 
Requires: python3-decorator
Requires: python3-linux-procfs
Requires: python3-perf
Requires: python3-gobject
Requires: python3-pyudev
Requires: python3-schedutils
# Requires: python3-syspurpose
Requires: util-linux
Requires: virt-what

Requires(post):   systemd
Requires(post):   virt-what
Requires(postun): systemd
Requires(preun):  systemd

Recommends: dmidecode
Recommends: hdparm
Recommends: kmod

%description
The tuned package contains a daemon that tunes system settings dynamically.
It does so by monitoring the usage of several system components periodically.
Based on that information components will then be put into lower or higher
power saving modes to adapt to the current usage. Currently only ethernet
network and ATA harddisk devices are implemented.

%global docdir %{_docdir}/%{name}

%package utils
Requires: %{name} = %{version}-%{release}
Summary: Various tuned utilities

%description utils
This package contains utilities that can help you to fine tune and
debug your system and manage tuned profiles.

%package utils-systemtap
Summary: Disk and net statistic monitoring systemtap scripts
Requires: %{name} = %{version}-%{release}
Requires: systemtap

%description utils-systemtap
This package contains several systemtap scripts to allow detailed
manual monitoring of the system. Instead of the typical IO/sec it collects
minimal, maximal and average time between operations to be able to
identify applications that behave power inefficient (many small operations
instead of fewer large ones).

%package profiles-sap
Summary: Additional tuned profile(s) targeted to SAP NetWeaver loads
Requires: %{name} = %{version}

%description profiles-sap
Additional tuned profile(s) targeted to SAP NetWeaver loads.

%package profiles-mssql
Summary: Additional tuned profile(s) for MS SQL Server
Requires: %{name} = %{version}

%description profiles-mssql
Additional tuned profile(s) for MS SQL Server.

%package profiles-oracle
Summary: Additional tuned profile(s) targeted to Oracle loads
Requires: %{name} = %{version}

%description profiles-oracle
Additional tuned profile(s) targeted to Oracle loads.

%package profiles-sap-hana
Summary: Additional tuned profile(s) targeted to SAP HANA loads
Requires: %{name} = %{version}

%description profiles-sap-hana
Additional tuned profile(s) targeted to SAP HANA loads.

%package profiles-atomic
Summary: Additional tuned profile(s) targeted to Atomic
Requires: %{name} = %{version}

%description profiles-atomic
Additional tuned profile(s) targeted to Atomic host and guest.

%package profiles-realtime
Summary: Additional tuned profile(s) targeted to realtime
Requires: %{name} = %{version}
Requires: tuna

%description profiles-realtime
Additional tuned profile(s) targeted to realtime.

%package profiles-nfv-guest
Summary: Additional tuned profile(s) targeted to Network Function Virtualization (NFV) guest
Requires: %{name} = %{version}
Requires: %{name}-profiles-realtime = %{version}
Requires: tuna

%description profiles-nfv-guest
Additional tuned profile(s) targeted to Network Function Virtualization (NFV) guest.

%package profiles-nfv-host
Summary: Additional tuned profile(s) targeted to Network Function Virtualization (NFV) host
Requires: %{name} = %{version}
Requires: %{name}-profiles-realtime = %{version}
Requires: tuna
Requires: nmap-ncat

%description profiles-nfv-host
Additional tuned profile(s) targeted to Network Function Virtualization (NFV) host.

%package profiles-cpu-partitioning
Summary: Additional tuned profile(s) optimized for CPU partitioning
Requires: %{name} = %{version}

%description profiles-cpu-partitioning
Additional tuned profile(s) optimized for CPU partitioning.

%package profiles-spectrumscale
Summary: Additional tuned profile(s) optimized for IBM Spectrum Scale
Requires: %{name} = %{version}

%description profiles-spectrumscale
Additional tuned profile(s) optimized for IBM Spectrum Scale.

%package profiles-compat
Summary: Additional tuned profiles mainly for backward compatibility with tuned 1.0
Requires: %{name} = %{version}

%description profiles-compat
Additional tuned profiles mainly for backward compatibility with tuned 1.0.
It can be also used to fine tune your system for specific scenarios.

%package profiles-postgresql
Summary: Additional tuned profile(s) targeted to PostgreSQL server loads
Requires: %{name} = %{version}

%description profiles-postgresql
Additional tuned profile(s) targeted to PostgreSQL server loads.

%prep
%autosetup -p1 -n %{name}-%{version}%{?prerel2}

%build
# Nothing

%install
make install DESTDIR=%{buildroot} DOCDIR=%{docdir} PYTHON=/usr/bin/python3
sed -i 's/\(dynamic_tuning[ \t]*=[ \t]*\).*/\10/' %{buildroot}%{_sysconfdir}/tuned/tuned-main.conf

# conditional support for grub2, grub2 is not available on all architectures
# and tuned is noarch package, thus the following hack is needed
mkdir -p %{buildroot}%{_datadir}/tuned/grub2
mv %{buildroot}%{_sysconfdir}/grub.d/00_tuned %{buildroot}%{_datadir}/tuned/grub2/00_tuned
rmdir %{buildroot}%{_sysconfdir}/grub.d

# ghost for persistent storage
mkdir -p %{buildroot}%{_var}/lib/tuned

# ghost for NFV
mkdir -p %{buildroot}%{_sysconfdir}/modprobe.d
touch %{buildroot}%{_sysconfdir}/modprobe.d/kvm.rt.tuned.conf

%post
%systemd_post tuned.service

# convert active_profile from full path to name (if needed)
sed -i 's|.*/\([^/]\+\)/[^\.]\+\.conf|\1|' /etc/tuned/active_profile

# convert GRUB_CMDLINE_LINUX to GRUB_CMDLINE_LINUX_DEFAULT
if [ -r "%{_sysconfdir}/default/grub" ]; then
  sed -i 's/GRUB_CMDLINE_LINUX="$GRUB_CMDLINE_LINUX \\$tuned_params"/GRUB_CMDLINE_LINUX_DEFAULT="$GRUB_CMDLINE_LINUX_DEFAULT \\$tuned_params"/' \
    %{_sysconfdir}/default/grub
fi


%preun
%systemd_preun tuned.service
if [ "$1" == 0 ]; then
# clear persistent storage
  rm -f %{_var}/lib/tuned/*
# clear temporal storage
  rm -f /run/tuned/*
fi


%postun
%systemd_postun_with_restart tuned.service

# conditional support for grub2, grub2 is not available on all architectures
# and tuned is noarch package, thus the following hack is needed
if [ "$1" == 0 ]; then
  rm -f %{_sysconfdir}/grub.d/00_tuned || :
# unpatch /etc/default/grub
  if [ -r "%{_sysconfdir}/default/grub" ]; then
    sed -i '/GRUB_CMDLINE_LINUX_DEFAULT="${GRUB_CMDLINE_LINUX_DEFAULT:+$GRUB_CMDLINE_LINUX_DEFAULT }\\$tuned_params"/d' %{_sysconfdir}/default/grub
  fi

# cleanup for Boot loader specification (BLS)

# clear grubenv variables
  grub2-editenv - unset tuned_params tuned_initrd &>/dev/null || :
# unpatch BLS entries
  MACHINE_ID=`cat /etc/machine-id 2>/dev/null`
  if [ "$MACHINE_ID" ]
  then
    for f in /boot/loader/entries/$MACHINE_ID-*.conf
    do
      # Skip non-files and rescue entries
      if [ ! -f "$f" -o "${f: -12}" == "-rescue.conf" ]
      then
        continue
      fi
      # Skip boom managed entries
      if [[ "$f" =~ \w*-[0-9a-f]{7,}-.*-.*.conf ]]
      then
        continue
      fi
      sed -i '/^\s*options\s\+.*\$tuned_params/ s/\s\+\$tuned_params\b//g' "$f" &>/dev/null || :
      sed -i '/^\s*initrd\s\+.*\$tuned_initrd/ s/\s\+\$tuned_initrd\b//g' "$f" &>/dev/null || :
    done
  fi
fi


%posttrans
# conditional support for grub2, grub2 is not available on all architectures
# and tuned is noarch package, thus the following hack is needed
if [ -d %{_sysconfdir}/grub.d ]; then
  cp -a %{_datadir}/tuned/grub2/00_tuned %{_sysconfdir}/grub.d/00_tuned
  selinuxenabled &>/dev/null && \
    restorecon %{_sysconfdir}/grub.d/00_tuned &>/dev/null || :
fi


%files
%license COPYING
%exclude %{docdir}/README.utils
%exclude %{docdir}/README.scomes
%exclude %{docdir}/README.NFV
%doc %{docdir}
%{_datadir}/bash-completion/completions/tuned-adm
%exclude %{python3_sitelib}/tuned/gtk
%{python3_sitelib}/tuned
%{_sbindir}/tuned
%{_sbindir}/tuned-adm
%exclude %{_sysconfdir}/tuned/realtime-variables.conf
%exclude %{_sysconfdir}/tuned/realtime-virtual-guest-variables.conf
%exclude %{_sysconfdir}/tuned/realtime-virtual-host-variables.conf
%exclude %{_sysconfdir}/tuned/cpu-partitioning-variables.conf
%exclude %{_prefix}/lib/tuned/default
%exclude %{_prefix}/lib/tuned/desktop-powersave
%exclude %{_prefix}/lib/tuned/laptop-ac-powersave
%exclude %{_prefix}/lib/tuned/server-powersave
%exclude %{_prefix}/lib/tuned/laptop-battery-powersave
%exclude %{_prefix}/lib/tuned/enterprise-storage
%exclude %{_prefix}/lib/tuned/spindown-disk
%exclude %{_prefix}/lib/tuned/sap-netweaver
%exclude %{_prefix}/lib/tuned/sap-hana
%exclude %{_prefix}/lib/tuned/mssql
%exclude %{_prefix}/lib/tuned/oracle
%exclude %{_prefix}/lib/tuned/atomic-host
%exclude %{_prefix}/lib/tuned/atomic-guest
%exclude %{_prefix}/lib/tuned/realtime
%exclude %{_prefix}/lib/tuned/realtime-virtual-guest
%exclude %{_prefix}/lib/tuned/realtime-virtual-host
%exclude %{_prefix}/lib/tuned/cpu-partitioning
%exclude %{_prefix}/lib/tuned/spectrumscale-ece
%exclude %{_prefix}/lib/tuned/postgresql
%exclude %{_sbindir}/tuned-gui
%exclude %{_datadir}/tuned/ui
%exclude %{_datadir}/icons/hicolor/scalable/apps/tuned.svg
%exclude %{_datadir}/applications/tuned-gui.desktop
%exclude %{_bindir}/powertop2tuned
%{_prefix}/lib/tuned
%dir %{_sysconfdir}/tuned
%dir %{_sysconfdir}/tuned/recommend.d
%dir %{_libexecdir}/tuned
%{_libexecdir}/tuned/defirqaffinity*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/tuned/active_profile
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/tuned/profile_mode
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/tuned/post_loaded_profile
%config(noreplace) %{_sysconfdir}/tuned/tuned-main.conf
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/tuned/bootcmdline
%{_sysconfdir}/dbus-1/system.d/com.redhat.tuned.conf
%verify(not size mtime md5) %{_sysconfdir}/modprobe.d/tuned.conf
%{_tmpfilesdir}/tuned.conf
%{_unitdir}/tuned.service
%dir %{_localstatedir}/log/tuned
%dir /run/tuned
%dir %{_var}/lib/tuned
%{_mandir}/man5/tuned*
%{_mandir}/man7/tuned-profiles.7*
%{_mandir}/man8/tuned*
%dir %{_datadir}/tuned
%{_datadir}/tuned/grub2
%{_datadir}/polkit-1/actions/com.redhat.tuned.policy
%ghost %{_sysconfdir}/modprobe.d/kvm.rt.tuned.conf
%{_prefix}/lib/kernel/install.d/92-tuned.install

%files utils
%{_libexecdir}/tuned/pmqos-static*

%files utils-systemtap
%doc doc/README.utils
%doc doc/README.scomes
%{_sbindir}/varnetload
%{_sbindir}/netdevstat
%{_sbindir}/diskdevstat
%{_sbindir}/scomes
%{_mandir}/man8/varnetload.*
%{_mandir}/man8/netdevstat.*
%{_mandir}/man8/diskdevstat.*
%{_mandir}/man8/scomes.*

%files profiles-sap
%{_prefix}/lib/tuned/sap-netweaver
%{_mandir}/man7/tuned-profiles-sap.7*

%files profiles-sap-hana
%{_prefix}/lib/tuned/sap-hana
%{_mandir}/man7/tuned-profiles-sap-hana.7*

%files profiles-mssql
%{_prefix}/lib/tuned/mssql
%{_mandir}/man7/tuned-profiles-mssql.7*

%files profiles-oracle
%{_prefix}/lib/tuned/oracle
%{_mandir}/man7/tuned-profiles-oracle.7*

%files profiles-atomic
%{_prefix}/lib/tuned/atomic-host
%{_prefix}/lib/tuned/atomic-guest
%{_mandir}/man7/tuned-profiles-atomic.7*

%files profiles-realtime
%config(noreplace) %{_sysconfdir}/tuned/realtime-variables.conf
%{_prefix}/lib/tuned/realtime
%{_mandir}/man7/tuned-profiles-realtime.7*

%files profiles-nfv-guest
%config(noreplace) %{_sysconfdir}/tuned/realtime-virtual-guest-variables.conf
%{_prefix}/lib/tuned/realtime-virtual-guest
%{_mandir}/man7/tuned-profiles-nfv-guest.7*

%files profiles-nfv-host
%config(noreplace) %{_sysconfdir}/tuned/realtime-virtual-host-variables.conf
%{_prefix}/lib/tuned/realtime-virtual-host
%{_mandir}/man7/tuned-profiles-nfv-host.7*

%files profiles-cpu-partitioning
%config(noreplace) %{_sysconfdir}/tuned/cpu-partitioning-variables.conf
%{_prefix}/lib/tuned/cpu-partitioning
%{_mandir}/man7/tuned-profiles-cpu-partitioning.7*

%files profiles-spectrumscale
%{_prefix}/lib/tuned/spectrumscale-ece
%{_mandir}/man7/tuned-profiles-spectrumscale-ece.7*

%files profiles-compat
%{_prefix}/lib/tuned/default
%{_prefix}/lib/tuned/desktop-powersave
%{_prefix}/lib/tuned/laptop-ac-powersave
%{_prefix}/lib/tuned/server-powersave
%{_prefix}/lib/tuned/laptop-battery-powersave
%{_prefix}/lib/tuned/enterprise-storage
%{_prefix}/lib/tuned/spindown-disk
%{_mandir}/man7/tuned-profiles-compat.7*

%files profiles-postgresql
%defattr(-,root,root,-)
%{_prefix}/lib/tuned/postgresql
%{_mandir}/man7/tuned-profiles-postgresql.7*

%changelog
* Thu Jan 20 2022 Cameron Baird <cameronbaird@microsoft.com> 2.15.0-4
- Initial CBL-Mariner import from CentOS 8 (license: MIT).
- License verified

* Fri Aug 13 2021 Hernan Gatta <hegatta@microsoft.com> - 2.15.0-3
- Remove dependency on desktop-file-utils

* Fri Mar 12 2021 Hernan Gatta <hegatta@microsoft.com> - 2.15.0-2
- Initial import into ECF Mariner from CentOS 8 (License: GPLv2)
- Removed GUI components due to missing GTK dependencies in Mariner

* Thu Dec 17 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.15.0-1
- new release
  - rebased tuned to latest upstream
    related: rhbz#1874052

* Tue Dec  1 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.15.0-0.1.rc1
- new release
  - rebased tuned to latest upstream
    resolves: rhbz#1874052
  - added plugin service for linux services control
    resolves: rhbz#1869991
  - scheduler: added default_irq_smp_affinity option
    resolves: rhbz#1896348
  - bootloader: skip boom managed BLS snippets
    resolves: rhbz#1901532
  - scheduler: added perf_process_fork option to enable processing of fork
    resolves: rhbz#1894610
  - scheduler: added perf_mmap_pages option to set perf buffer size
    resolves: rhbz#1890219
  - bootloader: fixed cmdline duplication with BLS and grub2-mkconfig
    resolves: rhbz#1777874

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul  3 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.14.0-2
- scheduler: fixed isolated_cores to work with cgroups
  related: rhbz#1784648
- throughput-performance: fix performance regression on AMD platforms
  related: rhbz#1746957

* Mon Jun 22 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.14.0-1
- new release
  - rebased tuned to latest upstream
    related: rhbz#1792264

* Mon Jun  8 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2.14.0-0.1.rc1
- new release
  - rebased tuned to latest upstream
    resolves: rhbz#1792264
  - oracle: turned off NUMA balancing
    resolves: rhbz#1782233
  - man: documented the possibility to apply multiple profiles
    resolves: rhbz#1794337
  - cpu-partitioning: disabled kernel.timer_migration
    resolves: rhbz#1797629
  - profiles: new profile optimize-serial-console
    resolves: rhbz#1840689
  - added support for a post-loaded profile
    resolves: rhbz#1798183
  - plugins: new irqbalance plugin
    resolves: rhbz#1784645
  - throughput-performance: added architecture specific tuning for Marvell ThunderX
    resolves: rhbz#1746961
  - throughput-performance: added architecture specific tuning for AMD
    resolves: rhbz#1746957
  - scheduler: added support for cgroups
    resolves: rhbz#1784648

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.13.0-4
- Rebuilt for Python 3.9

* Mon Apr 06 2020 Miro Hrončok <mhroncok@redhat.com> - 2.13.0-3
- Build without unittest2

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 11 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.13.0-1
- new release
  - rebased tuned to latest upstream
    related: rhbz#1738250
  - sap-hana: updated tuning
    resolves: rhbz#1779821
  - latency-performance: updated tuning
    resolves: rhbz#1779759
  - added sst profile
    resolves: rhbz#1743879

* Sun Dec  1 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.13.0-0.1.rc1
- new release
  - rebased tuned to latest upstream
    resolves: rhbz#1738250
  - cpu: fixed checking if EPB is supported
    resolves: rhbz#1690929
  - scheduler: fixed IRQ SMP affinity verification to respect ignore_missing
    resolves: rhbz#1729936
  - realtime: enabled ktimer_lockless_check
    resolves: rhbz#1734096
  - plugins: support cpuinfo_regex and uname_regex matching
    resolves: rhbz#1748965
  - sysctl: made reapply_sysctl ignore configs from /usr
    resolves: rhbz#1759597
  - added support for multiple include directives
    resolves: rhbz#1760390
  - realtime: added nowatchdog kernel command line option
    resolves: rhbz#1767614

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.12.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.12.0-3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.12.0-1
- new release
  - rebased tuned to latest upstream
    resolves: rhbz#1685585

* Wed Jun 12 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.12.0-0.1.rc1
- new release
  - rebased tuned to latest upstream
    resolves: rhbz#1685585
  - sap-netweaver: changed values of kernel.shmall and kernel.shmmax to RHEL-8 defaults
    resolves: rhbz#1708418
  - sap-netweaver: changed value of kernel.sem to RHEL-8 default
    resolves: rhbz#1701394
  - sap-hana-vmware: dropped profile
    resolves: rhbz#1715541
  - s2kb function: fixed to be compatible with python3
    resolves: rhbz#1684122
  - do fallback to the powersave governor (balanced and powersave profiles)
    resolves: rhbz#1679205
  - added support for negation of CPU list
    resolves: rhbz#1676588
  - switched from sysctl tool to own implementation
    resolves: rhbz#1666678
  - realtime-virtual-host: added tsc-deadline=on to qemu cmdline
    resolves: rhbz#1554458
  - fixed handling of devices that have been removed and re-attached
    resolves: rhbz#1677730

* Thu Mar 21 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.11.0-1
- new release
  - rebased tuned to latest upstream
    related: rhbz#1643654
  - used dmidecode only on x86 architectures
    resolves: rhbz#1688371
  - recommend: fixed to work without tuned daemon running
    resolves: rhbz#1687397
  - powertop2tuned: added support for wakeup tuning (powertop-2.10)
    resolves: rhbz#1690354

* Sun Mar 10 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.11.0-0.1.rc1
- new release
  - rebased tuned to latest upstream
    resolves: rhbz#1643654
  - use online CPUs for cpusets calculations instead of present CPUs
    resolves: rhbz#1613478
  - realtime-virtual-guest: run script.sh
    related: rhbz#1616043
  - make python-dmidecode a weak dependency
    resolves: rhbz#1565598
  - make virtual-host identical to latency-performance
    resolves: rhbz#1588932
  - added support for Boot loader specification (BLS)
    resolves: rhbz#1576435
  - scheduler: keep polling file objects alive long enough
    resolves: rhbz#1659140
  - mssql: updated tuning
    resolves: rhbz#1660178
  - s2kb: fixed to be compatible with python3
    resolves: rhbz#1684122
  - profiles: fallback to the 'powersave' scaling governor
    resolves: rhbz#1679205
  - disable KSM only once, re-enable it only on full rollback
    resolves: rhbz#1622239
  - functions: reworked setup_kvm_mod_low_latency to count with kernel changes
    resolves: rhbz#1649408
  - updated virtual-host profile
    resolves: rhbz#1569375
  - added log message for unsupported parameters in plugin_net
    resolves: rhbz#1533852
  - added range feature for cpu exclusion
    resolves: rhbz#1533908
  - make a copy of devices when verifying tuning
    resolves: rhbz#1592743
  - fixed disk plugin/plugout problem
    resolves: rhbz#1595156
  - fixed unit configuration reading
    resolves: rhbz#1613379
  - reload profile configuration on SIGHUP
    resolves: rhbz#1631744
  - use built-in functionality to apply system sysctl
    resolves: rhbz#1663412

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2.10.0-6
- Fixed disk plugin to correctly match devices with python3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.10.0-4
- Fix a traceback in tuned-gui

* Tue Jul 10 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.10.0-3
- Used python intepreter path from the rpm macro

* Tue Jul 10 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2.10.0-2
- tuned-adm: Fix a traceback when run without action specified
- Fixed compatibility with python-3.7

* Wed Jul  4 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.10.0-1
- new release
  - rebased tuned to latest upstream
    related: rhbz#1546598
  - IRQ affinity handled by scheduler plugin
    resolves: rhbz#1590937

* Mon Jun 11 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.10.0-0.1.rc1
- new release
  - rebased tuned to latest upstream
    resolves: rhbz#1546598
  - script: show stderr output in the log
    resolves: rhbz#1536476
  - realtime-virtual-host: script.sh: add error checking
    resolves: rhbz#1461509
  - man: improved tuned-profiles-cpu-partitioning.7
    resolves: rhbz#1548148
  - bootloader: check if grub2_cfg_file_name is None in _remove_grub2_tuning()
    resolves: rhbz#1571403
  - plugin_scheduler: whitelist/blacklist processed also for thread names
    resolves: rhbz#1512295
  - bootloader: patch all GRUB2 config files
    resolves: rhbz#1556990
  - profiles: added mssql profile
    resolves: rhbz#1442122
  - tuned-adm: print log excerpt when changing profile
    resolves: rhbz#1538745
  - cpu-partitioning: use no_balance_cores instead of no_rebalance_cores
    resolves: rhbz#1550573
  - sysctl: support assignment modifiers as other plugins do
    resolves: rhbz#1564092
  - oracle: fixed ip_local_port_range parity warning
    resolves: rhbz#1527219
  - Fix verifying cpumask on systems with more than 32 cores
    resolves: rhbz#1528368
  - oracle: updated the profile to be in sync with KCS 39188
    resolves: rhbz#1447323

* Fri Mar 23 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9.0-9
- Used weak deps for tuned-profiles-nfv-host-bin

* Wed Mar 21 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9.0-8
- Dropped tuned-profiles-nfv-host-bin, now provided by standalone package

* Fri Mar  2 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9.0-7
- Dropped exlusive arch in tuned-profiles-nfv-host-bin (it seems it
  blocked all tuned packages on non x86 architectures)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.9.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan 31 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9.0-4
- Fixed perf requirement, explicitly require python2-perf

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.9.0-3
- Remove obsolete scriptlets

* Mon Nov 13 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9.0-2
- added tscdeadline_latency.flat benchmark
  resolves: rhbz#1504680

* Sun Oct 29 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9.0-1
- new release
  - rebased tuned to latest upstream
    related: rhbz#1467576

* Fri Oct 20 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9.0-0.2.rc2
- new release
  - rebased tuned to latest upstream
    related: rhbz#1467576
  - fixed expansion of the variables in the 'devices' section
    related: rhbz#1490399
  - cpu-partitioning: add no_rebalance_cores= option
    resolves: rhbz#1497182

* Thu Oct 12 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.9.0-0.1.rc1
- new release
  - rebased tuned to latest upstream
    resolves: rhbz#1467576
  - added recommend.d functionality
    resolves: rhbz#1459146
  - recommend: added support for matching of processes
    resolves: rhbz#1461838
  - plugin_video: added support for the 'dpm' power method
    resolves: rhbz#1417659
  - list available profiles on 'tuned-adm profile'
    resolves: rhbz#988433
  - cpu-partitioning: used tuned instead of tuna for cores isolation
    resolves: rhbz#1442229
  - inventory: added workaround for pyudev < 0.18
    resolves: rhbz#1251240
  - realtime: used skew_tick=1 in kernel cmdline
    resolves: rhbz#1447938
  - realtime-virtual-guest: re-assigned kernel thread priorities
    resolves: rhbz#1452357
  - bootloader: splitted string for removal from cmdline
    resolves: rhbz#1461279
  - network-latency: added skew_tick=1 kernel command line parameter
    resolves: rhbz#1451073
  - bootloader: accepted only certain values for initrd_remove_dir
    resolves: rhbz#1455161
  - increased udev monitor buffer size, made it configurable
    resolves: rhbz#1442306
  - bootloader: don't add nonexistent overlay image to grub.cfg
    resolves: rhbz#1454340
  - plugin_cpu: don't log error in execute() if EPB is not supported
    resolves: rhbz#1443182
  - sap-hana: fixed description of the sap-hana profiles
    resolves: rhbz#1482005
  - plugin_systemd: on full_rollback notify about need of initrd regeneration
    resolves: rhbz#1469258
  - don't log errors about missing files on verify with ignore_missing set
    resolves: rhbz#1451435
  - plugin_scheduler: improved logging
    resolves: rhbz#1474961
  - improved checking if we are rebooting or not
    resolves: rhbz#1475571
  - started dbus exports after a profile is applied
    resolves: rhbz#1443142
  - sap-hana: changed force_latency to 70
    resolves: rhbz#1501252

* Mon Aug 21 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8.0-5
- kernel-tools made weak dependency

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8.0-3
- fixed traceback in disk plugin if dynamic tuning is enabled

* Fri Apr 28 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8.0-2
- qemu-kvm-tools-rhev made weak dependency

* Fri Apr  7 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8.0-1
- new release
  - rebase tuned to latest upstream
    resolves: rhbz#1388454
  - cpu-partitioning: enabled timer migration
    resolves: rhbz#1408308
  - cpu-partitioning: disabled kvmclock sync and ple
    resolves: rhbz#1395855
  - spec: muted error if there is no selinux support
    resolves: rhbz#1404214
  - units: implemented instance priority
    resolves: rhbz#1246172
  - bootloader: added support for initrd overlays
    resolves: rhbz#1414098
  - cpu-partitioning: set CPUAffinity early in initrd image
    resolves: rhbz#1394965
  - cpu-partitioning: set workqueue affinity early
    resolves: rhbz#1395899
  - scsi_host: fixed probing of ALPM, missing ALPM logged as info
    resolves: rhbz#1416712
  - added new profile cpu-partitioning
    resolves: rhbz#1359956
  - bootloader: improved inheritance
    resolves: rhbz#1274464
  - units: mplemented udev-based regexp device matching
    resolves: rhbz#1251240
  - units: introduced pre_script, post_script
    resolves: rhbz#1246176
  - realtime-virtual-host: accommodate new ktimersoftd thread
    resolves: rhbz#1332563
  - defirqaffinity: fixed traceback due to syntax error
    resolves: rhbz#1369791
  - variables: support inheritance of variables
    resolves: rhbz#1433496
  - scheduler: added support for cores isolation
    resolves: rhbz#1403309
  - tuned-profiles-nfv splitted to host/guest and dropped unneeded dependency
    resolves: rhbz#1413111
  - desktop: fixed typo in profile summary
    resolves: rhbz#1421238
  - with systemd don't do full rollback on shutdown / reboot
    resolves: rhbz#1421286
  - builtin functions: added virt_check function and support to include
    resolves: rhbz#1426654
  - cpulist_present: explicitly sorted present CPUs
    resolves: rhbz#1432240
  - plugin_scheduler: fixed initialization
    resolves: rhbz#1433496
  - log errors when applying a profile fails
    resolves: rhbz#1434360
  - systemd: added support for older systemd CPUAffinity syntax
    resolves: rhbz#1441791
  - scheduler: added workarounds for low level exceptions from
    python-linux-procfs
    resolves: rhbz#1441792
  - bootloader: workaround for adding tuned_initrd to new kernels on restart
    resolves: rhbz#1441797

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 17 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7.1-3
- Fixed traceback when non-existent profile is queried through
  tuned-adm profile_info
  Resolves: rhbz#1385145

* Wed Sep 21 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7.1-2
- Fixed pkexec
  Resolves: rhbz#1377896

* Tue Aug  2 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7.1-1
- New release
  Resolves: rhbz#1362481
- Dropped tuned-gui-traceback-fix and tuned-adm-list-no-dbus-traceback-fix
  patches (both upstreamed)

* Thu Jul 21 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7.0-2
- Fixed tuned-gui traceback (by tuned-gui-traceback-fix patch)
  Resolves: rhbz#1358846
- Fixed 'tuned-adm list' traceback if daemon is not running
  (by tuned-adm-list-no-dbus-traceback-fix patch)

* Tue Jul 19 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.7.0-1
- new-release
  - gui: fixed save profile
    resolves: rhbz#1242491
  - tuned-adm: added --ignore-missing parameter
    resolves: rhbz#1243807
  - plugin_vm: added transparent_hugepage alias
    resolves: rhbz#1249610
  - plugins: added modules plugin
    resolves: rhbz#1249618
  - plugin_cpu: do not show error if cpupower or x86_energy_perf_policy are
    missing
    resolves: rhbz#1254417
  - tuned-adm: fixed restart attempt if tuned is not running
    resolves: rhbz#1258755
  - nfv: avoided race condition by using synchronous mode
    resolves: rhbz#1259039
  - realtime: added check for isolcpus sanity
    resolves: rhbz#1264128
  - pm_qos: fixed exception if PM_QoS is not available
    resolves: rhbz#1296137
  - plugin_sysctl: reapply system sysctl after Tuned sysctl are applied
    resolves: rhbz#1302953
  - atomic: increase number of inotify watches
    resolves: rhbz#1322001
  - realtime-virtual-host/guest: added rcu_nocbs kernel boot parameter
    resolves: rhbz#1334479
  - realtime: fixed kernel.sched_rt_runtime_us to be -1
    resolves: rhbz#1346715
  - tuned-adm: fixed detection of no_daemon mode
    resolves: rhbz#1351536
  - plugin_base: correctly strip assignment modifiers even if not used
    resolves: rhbz#1353142
  - plugin_disk: try to workaround embedded '/' in device names
    related: rhbz#1353142
  - sap-hana: explicitly setting kernel.numa_balancing = 0 for better performance
    resolves: rhbz#1355768
  - switched to polkit authorization
    resolves: rhbz#1095142
  - plugins: added scsi_host plugin
    resolves: rhbz#1246992
  - spec: fixed conditional support for grub2 to work with selinux
    resolves: rhbz#1351937
  - gui: added tuned icon and desktop file
    resolves: rhbz#1356369

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan  5 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2.6.0-1
- new-release
  - plugin_cpu: do not show error if cpupower or x86_energy_perf_policy are missing
  - plugin_sysctl: fixed quoting of sysctl values
    resolves: rhbz#1254538
  - tuned-adm: added log file location hint to verify command output
  - libexec: fixed listdir and isdir in defirqaffinity.py
    resolves: rhbz#1252160
  - plugin_cpu: save and restore only intel pstate attributes that were changed
    resolves: rhbz#1252156
  - functions: fixed sysfs save to work with options
    resolves: rhbz#1251507
  - plugins: added scsi_host plugin
  - tuned-adm: fixed restart attempt if tuned is not running
  - spec: fixed post scriptlet to work without grub
    resolves: rhbz#1265654
  - tuned-profiles-nfv: fix find-lapictscdeadline-optimal.sh for CPUS where ns > 6500
    resolves: rhbz#1267284
  - functions: fixed restore_logs_syncing to preserve SELinux context on rsyslog.conf
    resolves: rhbz#1268901
  - realtime: set unboud workqueues cpumask
    resolves: rhbz#1259043
  - spec: correctly remove tuned footprint from /etc/default/grub
    resolves: rhbz#1268845
  - gui: fixed creation of new profile
    resolves: rhbz#1274609
  - profiles: removed nohz_full from the realtime profile
    resolves: rhbz#1274486
  - profiles: Added nohz_full and nohz=on to realtime guest/host profiles
    resolves: rhbz#1274445
  - profiles: fixed lapic_timer_adv_ns cache
    resolves: rhbz#1259452
  - plugin_sysctl: pass verification even if the option doesn't exist
    related: rhbz#1252153
  - added support for 'summary' and 'description' of profiles,
    extended D-Bus API for Cockpit
    related: rhbz#1228356

* Wed Aug 12 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5.1-2
- packaging fixes for rpm-4.12.90
- dropped qemu-kvm-tools-rhev requirement (not in Fedora)

* Tue Aug  4 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5.1-1
- new-release
  related: rhbz#1155052
  - plugin_scheduler: work with nohz_full
    resolves: rhbz#1247184
  - fixed realtime-virtual-guest/host profiles packaged twice
    resolves: rhbz#1249028
  - fixed requirements of realtime and nfv profiles
  - fixed tuned-gui not starting
  - various other minor fixes

* Sun Jul  5 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.5.0-1
- new-release
  resolves: rhbz#1155052
  - add support for ethtool -C to tuned network plugin
    resolves: rhbz#1152539
  - add support for ethtool -K to tuned network plugin
    resolves: rhbz#1152541
  - add support for calculation of values for the kernel command line
    resolves: rhbz#1191595
  - no error output if there is no hdparm installed
    resolves: rhbz#1191775
  - do not run hdparm on hotplug events if there is no hdparm tuning
    resolves: rhbz#1193682
  - add oracle tuned profile
    resolves: rhbz#1196298
  - fix bash completions for tuned-adm
    resolves: rhbz#1207668
  - add glob support to tuned sysfs plugin
    resolves: rhbz#1212831
  - add tuned-adm verify subcommand
    resolves: rhbz#1212836
  - do not install tuned kernel command line to rescue kernels
    resolves: rhbz#1223864
  - add variables support
    resolves: rhbz#1225124
  - add built-in support for unit conversion into tuned
    resolves: rhbz#1225135
  - fix vm.max_map_count setting in sap-netweaver profile
    resolves: rhbz#1228562
  - add tuned profile for RHEL-RT
    resolves: rhbz#1228801
  - plugin_scheduler: added support for runtime tuning of processes
    resolves: rhbz#1148546
  - add support for changing elevators on xvd* devices (Amazon EC2)
    resolves: rhbz#1170152
  - add workaround to be run after systemd-sysctl
    resolves: rhbz#1189263
  - do not change settings of transparent hugepages if set in kernel cmdline
    resolves: rhbz#1189868
  - add tuned profiles for RHEL-NFV
    resolves: rhbz#1228803
  - plugin_bootloader: apply $tuned_params to existing kernels
    resolves: rhbz#1233004

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-5
- fixed configobj class imports
  resolves: rhbz#1217327

* Thu Apr  2 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-4
- fixed bash completion
  resolves: rhbz#1207668

* Fri Jan  9 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-3
- fixed KeyError exception in powertop2tuned

* Mon Jan  5 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-2
- remove 00_tuned grub2 template upon tuned uninstall
  resolves: rhbz#1178310

* Thu Oct 16 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.1-1
- new-release
  - fixed return code of tuned grub template
    resolves: rhbz#1151768
  - plugin_bootloader: fix for multiple parameters on command line
    related: rhbz#1148711
  - tuned-adm: fixed traceback on "tuned-adm list"
    resolves: rhbz#1149162
  - plugin_bootloader is automatically disabled if grub2 is not found
    resolves: rhbz#1150047
  - plugin_disk: set_spindown and set_APM made independent
    resolves: rhbz#976725

* Wed Oct  1 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.4.0-1
- new-release
  resolves: rhbz#1093883
  - fixed traceback if profile cannot be loaded
    related: rhbz#953128
  - powertop2tuned: fixed traceback if rewriting file instead of dir
    resolves: rhbz#963441
  - throughput-performance: altered dirty ratios for better performance
    resolves: rhbz#1043533
  - latency-performance: leaving THP on its default
    resolves: rhbz#1064510
  - used throughput-performance profile on server by default
    resolves: rhbz#1063481
  - network-latency: added new profile
    resolves: rhbz#1052418
  - network-throughput: added new profile
    resolves: rhbz#1052421
  - recommend.conf: fixed config file
    resolves: rhbz#1069123
  - systemd: added cpupower.service conflict
    resolves: rhbz#1073392
  - balanced: used medium_power ALPM policy
  - added support for >, < assignment modifiers in tuned.conf
  - handled root block devices
  - balanced: used conservative CPU governor
    resolves: rhbz#1124125
  - plugins: added selinux plugin
  - plugin_net: added nf_conntrack_hashsize parameter
  - profiles: added atomic-host profile
    resolves: rhbz#1091977
  - profiles: added atomic-guest profile
    resolves: rhbz#1091979
  - moved profile autodetection from post install script to tuned daemon
    resolves: rhbz#1144067
  - profiles: included sap-hana and sap-hana-vmware profiles
  - man: structured profiles manual pages according to sub-packages
  - added missing hdparm dependency
    resolves: rhbz#1144858
  - improved error handling of switch_profile
    resolves: rhbz#1068699
  - tuned-adm: active: detect whether tuned deamon is running
    related: rhbz#1068699
  - removed active_profile from RPM verification
    resolves: rhbz#1104126
  - plugin_disk: readahead value can be now specified in sectors
    resolves: rhbz#1127127
  - plugins: added bootloader plugin
    resolves: rhbz#1044111
  - plugin_disk: added error counter to hdparm calls
  - plugins: added scheduler plugin
    resolves: rhbz#1100826
  - added tuned-gui

* Thu Mar  6 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3.0-3
- added kernel-tools requirement
  resolves: rhbz#1072981

* Fri Nov  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3.0-2
- fixed race condition in the start/stop code
  resolves: rhbz#1028119
- improved tuned responsiveness
  resolves: rhbz#1028122

* Wed Nov  6 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.3.0-1
- new-release
  resolves: rhbz#1020743
  - audio plugin: fixed audio settings in standard profiles
    resolves: rhbz#1019805
  - video plugin: fixed tunings
  - daemon: fixed crash if preset profile is not available
    resolves: rhbz#953128
  - man: various updates and corrections
  - functions: fixed usb and bluetooth handling
  - tuned: switched to lightweighted pygobject3-base
  - daemon: added global config for dynamic_tuning
    resolves: rhbz#1006427
  - utils: added pmqos-static script for debug purposes
    resolves: rhbz#1015676
  - throughput-performance: various fixes
    resolves: rhbz#987570
  - tuned: added global option update_interval
  - plugin_cpu: added support for x86_energy_perf_policy
    resolves: rhbz#1015675
  - dbus: fixed KeyboardInterrupt handling
  - plugin_cpu: added support for intel_pstate
    resolves: rhbz#996722
  - profiles: various fixes
    resolves: rhbz#922068
  - profiles: added desktop profile
    resolves: rhbz#996723
  - tuned-adm: implemented non DBus fallback control
  - profiles: added sap profile
  - tuned: lowered CPU usage due to python bug
    resolves: rhbz#917587

* Tue Mar 19 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2.2-1
- new-release:
  - cpu plugin: fixed cpupower workaround
  - cpu plugin: fixed crash if cpupower is installed

* Fri Mar  1 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.2.1-1
- new release:
  - audio plugin: fixed error handling in _get_timeout
  - removed cpupower dependency, added sysfs fallback
  - powertop2tuned: fixed parser crash on binary garbage
    resolves: rhbz#914933
  - cpu plugin: dropped multicore_powersave as kernel upstream already did
  - plugins: options manipulated by dynamic tuning are now correctly saved and restored
  - powertop2tuned: added alias -e for --enable option
  - powertop2tuned: new option -m, --merge-profile to select profile to merge
  - prefer transparent_hugepage over redhat_transparent_hugepage
  - recommend: use recommend.conf not autodetect.conf
  - tuned.service: switched to dbus type service
    resolves: rhbz#911445
  - tuned: new option --pid, -P to write PID file
  - tuned, tuned-adm: added new option --version, -v to show version
  - disk plugin: use APM value 254 for cleanup / APM disable instead of 255
    resolves: rhbz#905195
  - tuned: new option --log, -l to select log file
  - powertop2tuned: avoid circular deps in include (one level check only)
  - powertop2tuned: do not crash if powertop is not installed
  - net plugin: added support for wake_on_lan static tuning
    resolves: rhbz#885504
  - loader: fixed error handling
  - spec: used systemd-rpm macros
    resolves: rhbz#850347

* Mon Jan 28 2013 Jan Vcelak <jvcelak@redhat.com> 2.2.0-1
- new release:
  - remove nobarrier from virtual-guest (data loss prevention)
  - devices enumeration via udev, instead of manual retrieval
  - support for dynamically inserted devices (currently disk plugin)
  - dropped rfkill plugins (bluetooth and wifi), the code didn't work

* Wed Jan  2 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2.1.2-1
- new release:
  - systemtap {disk,net}devstat: fix typo in usage
  - switched to configobj parser
  - latency-performance: disabled THP
  - fixed fd leaks on subprocesses

* Thu Dec 06 2012 Jan Vcelak <jvcelak@redhat.com> 2.1.1-1
- fix: powertop2tuned execution
- fix: ownership of /etc/tuned

* Mon Dec 03 2012 Jan Vcelak <jvcelak@redhat.com> 2.1.0-1
- new release:
  - daemon: allow running without selected profile
  - daemon: fix profile merging, allow only safe characters in profile names
  - daemon: implement missing methods in DBus interface
  - daemon: implement profile recommendation
  - daemon: improve daemonization, PID file handling
  - daemon: improved device matching in profiles, negation possible
  - daemon: various internal improvements
  - executables: check for EUID instead of UID
  - executables: run python with -Es to increase security
  - plugins: cpu - fix cpupower execution
  - plugins: disk - fix option setting
  - plugins: mounts - new, currently supports only barriers control
  - plugins: sysctl - fix a bug preventing settings application
  - powertop2tuned: speedup, fix crashes with non-C locales
  - powertop2tuned: support for powertop 2.2 output
  - profiles: progress on replacing scripts with plugins
  - tuned-adm: bash completion - suggest profiles from all supported locations
  - tuned-adm: complete switch to D-bus
  - tuned-adm: full control to users with physical access

* Mon Oct 08 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.2-1
- New version
- Systemtap scripts moved to utils-systemtap subpackage

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 12 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.1-3
- another powertop-2.0 compatibility fix
  Resolves: rhbz#830415

* Tue Jun 12 2012 Jan Kaluza <jkaluza@redhat.com> - 2.0.1-2
- fixed powertop2tuned compatibility with powertop-2.0

* Tue Apr 03 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.1-1
- new version

* Fri Mar 30 2012 Jan Vcelak <jvcelak@redhat.com> 2.0-1
- first stable release
