%bcond_with libreport

Summary:        The mdadm program controls Linux md devices (software RAID arrays)
Name:           mdadm
Version:        4.1
Release:        9%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.kernel.org/pub/linux/utils/raid/mdadm/
Source0:        http://www.kernel.org/pub/linux/utils/raid/mdadm/%{name}-%{version}.tar.xz
Source1:        raid-check
Source2:        mdadm.rules
Source3:        mdadm-raid-check-sysconfig
Source4:        mdmonitor.service
Source5:        mdadm.conf
Source6:        mdadm_event.conf
Source7:        raid-check.timer
Source8:        raid-check.service
# Build without -Werror. From Debian.
Patch00:        https://sources.debian.org/data/main/m/mdadm/4.1-2/debian/patches/debian-no-Werror.diff#/mdadm-4.1-no-Werror.patch
# Fedora customization patches, keeping in Mariner for now.
Patch97:        mdadm-3.3-udev.patch
Patch98:        mdadm-2.5.2-static.patch

BuildRequires:  binutils-devel
BuildRequires:  gcc
BuildRequires:  systemd-rpm-macros

Requires(post): coreutils
Requires(post): systemd
Requires(postun): coreutils
Requires(postun): systemd
Requires(preun): systemd
%if %{with libreport}
Requires:       libreport-filesystem
%endif

%description
The mdadm program is used to create, manage, and monitor Linux MD (software
RAID) devices.  As such, it provides similar functionality to the raidtools
package.  However, mdadm is a single program, and it can perform
almost all functions without a configuration file, though a configuration
file can be used to help with some common tasks.

%prep
%autosetup -p1 -n %{name}-%{version}%{?subversion:_%{subversion}}

%build
make %{?_smp_mflags} CXFLAGS="%{optflags}" LDFLAGS="$RPM_LD_FLAGS" SYSCONFDIR="%{_sysconfdir}" mdadm mdmon

%install
make DESTDIR=%{buildroot} MANDIR=%{_mandir} BINDIR=%{_sbindir} SYSTEMD_DIR=%{_unitdir} UDEVDIR=%{_libdir}/udev/ install install-systemd
install -Dp -m 755 %{SOURCE1} %{buildroot}%{_sbindir}/raid-check
install -Dp -m 644 %{SOURCE2} %{buildroot}%{_udevrulesdir}/65-md-incremental.rules
install -Dp -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/raid-check
mkdir -p -m 710 %{buildroot}/run/mdadm

# systemd
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE4} %{buildroot}%{_unitdir}
install -m644 %{SOURCE7} %{buildroot}%{_unitdir}
install -m644 %{SOURCE8} %{buildroot}%{_unitdir}

# tmpfile
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0710 %{buildroot}/run/%{name}/

# abrt
%if %{with libreport}
mkdir -p %{buildroot}%{_sysconfdir}/libreport/events.d
install -m644 %{SOURCE6} %{buildroot}%{_sysconfdir}/libreport/events.d
%endif

%post
%systemd_post mdmonitor.service raid-check.timer

%preun
%systemd_preun mdmonitor.service raid-check.timer

%postun
%systemd_postun_with_restart mdmonitor.service

%files
%license COPYING
%doc mdadm.conf-example misc/*
%{_udevrulesdir}/*
%{_sbindir}/*
%{_unitdir}/*
%{_mandir}/man*/md*
%{_libdir}/systemd/system-shutdown/*
%config(noreplace) %{_sysconfdir}/sysconfig/*
%dir /run/%{name}/
%config(noreplace) %{_tmpfilesdir}/%{name}.conf
%if %{with libreport}
%{_sysconfdir}/libreport/events.d/*
%endif

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.1-9
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1-8
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.1-7
- Disable usage of libreport by default
- License verified
- Lint spec

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.1-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Apr 01 2020 Xiao Ni <xni@redhat.com> - 4.1-5
- Fix raid check systemd config errors
- Resolves bz1801010

* Sun Mar 08 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 4.1-4
- Fix install location of udev rules (rhbz 1809117)

* Fri Feb 07 2020 Alejandro Domínguez Muñoz <adomu@net-c.com> - 4.1-3
- Replace raid-check cron job with systemd timer

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Peter Robinson <pbrobinson@fedoraproject.org> 4.1-1
- Update to 4.1 GA
- Spec cleanups and updates
- Update mdadm.pid location (rhbz 1701114, rhbz 1557623, rhbz 1557623)

* Sun Dec 15 2019 Julian Sikorski <belegdol@fedoraproject.org> - 4.1-rc2.0.5.2
- Fix invalid substitution type error
- Resolves bz1740662, bz1749859

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-rc2.0.5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Xiao Ni <xni@redhat.com> - 4.1-rc2.0.5
- Update tmpfiles directory to non-legacy location
- Resolves bz1704517

* Wed Apr 17 2019 Xiao Ni <xni@redhat.com> - 4.1-rc2.0.4
- Change tmpfiles directory to /run/mdadm
- Resovles bz1701821

* Sat Mar 16 2019 Björn Esser <besser82@fedoraproject.org> - 4.1-rc2.0.3
- Add patch to build without -Werror, fixes FTBFS (#1675363)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-rc2.0.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 13 2018 Adam Williamson <awilliam@redhat.com> - 4.1-rc2.0.2
- Fix multipath check in udev rule, broke array init in F29
- Resolves bz1628192

* Sun Aug 26 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.1-rc2.0.1
- Update to 4.1 rc2

* Fri Jul 20 2018 Xiao Ni <xni@redhat.com> - 4.1-rc1_1.2
- Add gcc into BuildRequires
- Resolves bz1604811

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-rc1_1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Xiao Ni <xni@redhat.com> 4.1-rc1-1
- Update to latest upstream version 4.1-rc1
- Resolves bz1556591

* Wed Jul  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.0-7
- Cleanup spec, use %%licenece, drop old sys-v migration bits

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 26 2017 Xiao Ni <xni@redhat.com> - 4.0-3
- Fix building errors against newer gcc (>=7.0)
- Resolves bz1444756

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Xiao Ni <xni@redhat.com> - 4.0-1
- Upgrade to mdadm-4.0 
- Resolves bz1411555

* Mon Aug 15 2016 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.4-3
- Fix build against newer glibc (Fedora 26+)

* Fri Aug 12 2016 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.4-2
- Fix i686 build error
- Fix problem where it was not possible to stop an IMSM array during reshape
- Fix Degraded Raid1 array becomes inactive after rebooting
- Fix problem with raid0 arrays not being detected by Anaconda due to it
  setting MALLOC_PERTURB_
- Fix problem with reshaping IMSM arrays, where a new reshape could be
  launched before the first reshape had fully completed, leading to
  unpected results.
- Fix problem with mdadm large device names overflowing an internal buffer
- Fix problem about reshape stuck at beginning
- Resolves bz1303380

* Fri Aug 12 2016 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.4-1
- Upgrade to mdadm-3.4
- Resolves bz1303380

* Mon May 30 2016 Xiao Ni <xni@redhat.com> - 3.3.4-4
- Fix Degraded Raid1 array becomes inactive after rebooting
- Resolves bz1337004

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 5 2015 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3.4-2
- Fix race when assembling or stopping IMSM RAID arrays
- Resolves bz1268955

* Mon Oct 5 2015 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3.4-1
- Upgrade to mdadm-3.3.4
- Resolves bz1246474

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Aug 26 2014 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3.2-1
- Upgrade to mdadm-3.3.2
- Resolves bz1132847

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 5 2014 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3.1-6
- Apply proper fix for bz1125883, clean up after rogue patch application
- Resolves bz1125883

* Mon Aug 04 2014 Dan Horák <dan[at]danny.cz> - 3.3.1-5
- revert the previous fix, not upstream yet

* Mon Aug 04 2014 Dan Horák <dan[at]danny.cz> - 3.3.1-4
- fix FTBFS on ppc64 (#1125883)

* Tue Jul 29 2014 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3.1-3
- Improve error message for "--grow -n2" when used on Linear arrays
- Fix problem where explicitly specified arrays were not assembled if
  they were disabled in /etc/mdadm.conf
- Resolves bz1122146, bz1124310

* Thu Jun 12 2014 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3.1-2
- Revert 'change' event support fix from 3.3.1-1 - this requires a lot
  more testing if we are to go there.

* Tue Jun 10 2014 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3.1-1
- Update to mdadm-3.3.1
- Fixup mdadm.rules to honor 'change' events
- Resolvez bz1105136

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 14 2014 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3-7
- Don't depend on syslog.target in mdmonitor.service
- Resolves bz1055202

* Fri Jan 31 2014 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3-6
- Revert changes introduced in 3.3-5, they were based on incorrect
  recommendations.
- Resolves bz1053176

* Thu Jan 30 2014 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3-5
- Do not create /var/run/mdadm in the rpm file, since this is sitting on
  tmpfs and is created by tmpfiles during boot.
- Resolves bz1053176

* Thu Oct 10 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3-4
- Fix byteswap macros return types to allow for building on big endian
  architectures again.
- Resolves bz1015494

* Wed Oct 9 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3-3
- Check for DM_UDEV_DISABLE_OTHER_RULES_FLAG instead of
  DM_UDEV_DISABLE_DISK_RULES_FLAG in 65-md-incremental.rules 
- Resolves bz1015521

* Tue Oct 8 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3-2
- Fix dracut requirement, minimum version 034-1

* Thu Sep 5 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.3-1
- Update to mdadm-3.3
- Resolves bz977826

* Tue Aug 13 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-21
- Fix pointless rpmbuild noise over mismatching date info
- Remove Fedora 17 support
- Fix problem where first stop command doesn't stop container during
  IMSM volume's reshape bz956053 (f18), bz956056 (f19)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 24 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-19
- Fix problem where  rebuild of IMSM RAID5 volume started in OROM,
  does not proceed in OS 
- Resolves bz956021 (f18), bz956026 (f17), bz956031 (f19)

* Tue Apr 23 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-18
- Fix problem with IMSM metadata where resync progress would be lost
  if an array was stopped during ongoing expansion of a RAID1/5 volume.
- Resolves bz948745

* Tue Apr 23 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-17
- Reorder patches to allow for udev query patch to be applied on
  Fedora 17 as well.

* Mon Apr 22 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-16
- Rely on rpm macros to place files in correct directories, and match /usr
  move
- Resolves bz955248

* Thu Mar 7 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-15
- Cleanup .spec file handling of different Fedora versions
- Resolves bz914629

* Tue Feb 5 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-14
- Resync with final version of upstream patches for launching mdmon
  via systemctl. Require dracut 024-025 or later to match.
- Resolves bz879327

* Fri Feb 1 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-13
- Update to upstream solution for launching mdmon via systemctl
- Resolves bz879327

* Mon Jan 21 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-12
- Launch mdmon via systemctl to avoid it ending up in the wrong cgroup
  and getting killed in the boot process when switching from the
  initrd to the real root.
- Resolves bz879327

* Tue Jan 8 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-11
- Move code to leave udev cgroup into mdmon and excute it after we
  work, to make sure it actually does the right thing.

* Mon Jan 7 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-10
- Fix mdmonitor-takeover.service dangling symlink problem for real

* Mon Jan 7 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-9
- Reintroduce fix for removing dangling symlink of
  mdmonitor-takeover.service which got lost in the fix introduced in
  3.2.6-8

* Fri Jan 4 2013 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-8
- mdmonitor-takeover.service is obsolete with the --offroot support,
  and it is harmful as of 3.2.6
- Resolves bz834245

* Mon Dec 10 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-7
- Fix issue with udev scripts where if an raid volume with one of
  the disks failing, the failed disk is still present in the volume
  and container. The raid volume stays is in normal state (should be
  degraded) and the rebuild cannot start.
- Resolves bz886123

* Mon Dec 10 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-5
- mdadm-sysvinit is obsolete given that we no longer support booting
  using sysvinit scripts
- Resolves bz884993

* Mon Dec 10 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-4
- Fix typo in error message in fix for 880972. No functional changes

* Fri Nov 30 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-3
- Disallow creating a second IMSM RAID array size 0 (bz880972)
- Disallow creating IMSM RAIDs that spans multiple controllers (bz880974)
- Resolves bz880972, bz880974

* Thu Nov 15 2012 Doug Ledford <dledford@redhat.com> - 3.2.6-2
- Modify mdadm to set the cgroup of mdmon to systemd if it's available
- Related bz873576 (and others)

* Thu Oct 25 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.6-1
- Upgrade to mdadm-3.2.6
- Resolves bz869930

* Fri Oct 19 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-14
- Dummy update to work around bodhi breakage. No actual code changes.

* Fri Oct 19 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-13
- Relax installation requirements for abrt script to only depend on
  libreport-filesystem rather than the full abrt package

* Thu Oct 18 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-12
- Add abrt script to retrieve /proc/mdstat output in case of crash
- Resolves bz867842

* Wed Oct 17 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-11
- Remove package requirements for udev and initscripts for F18+
- Resolves bz864562

* Wed Oct 3 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-9
- Resolve issue with ambiguous licenses
- Resolves bz862761

* Mon Sep 10 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-8
- Switch to using new systemd macros for F18+
- Resolves bz850202

* Thu Aug 2 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-7
- Remove bogus rogue patch applied in 3.2.5-5 with justification and
  without following the structure of the mdadm package.

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 18 2012 Karsten Hopp <karsten@redhat.com> 3.2.5-5
- include <linux/types.h> in some to avoid type clashes.
  same problem as rhbz #840902  

* Mon Jul 16 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-4
- Move /etc/tmpfiles.d/mdadm.conf to /lib/tmpfiles.d/ to comply with
  Fedora tmpfile rules
- Resolves bz840187

* Mon Jun 25 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-3
- Fix problem where reshape of RAID volume is broken after trying to
  stop all MD devices.
- Enhance raid-check to allow the adming to specify the max number of
  concurrent arrays to be checked at any given time.
- Resolves bz830177, bz820124

* Wed Jun 13 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-2
- Fix uninstall script to remove dangling symlink to
  mdmonitor-takeover.service, if the mdadm package is uninstalled from
  the system.
- Resolves bz828354

* Mon May 21 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.5-1
- Upgrade to mdadm-3.2.5
- Resolves bz822850

* Tue May 15 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.4-3
- Fix mdadm-3.2.4 introduced bug where --add fails in common cases
- Resolves bz821717 (f17) bz821718 (f16) bz821719 (f15)

* Thu May 10 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.4-2
- Fix mdadm.conf to use 'd' for /var/run/mdadm creation, to avoid the
  map file getting deleted during boot.

* Thu May 10 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.4-1
- Upgrade to mdadm-3.2.4
- Resolves bz820534 (rawhide) bz820527 (f17) bz820531 (f16) bz820532 (f15)

* Mon Apr 30 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-9
- Fix Monitor mode sometimes crashes when a resync completes
- Fix missing symlink for mdadm container device when incremental creates
  the array
- Make sure when creating a second array in a container that the second
  array uses all available space since leaving space for a third array
  is invalid
- Validate the number of imsm volumes per controller
- Fix issues with imsm arrays and disks larger than 2TB
- Add support for expanding imsm arrays/containers
- The support for expanding imsm arrays/containers was accepted upstream,
  update to the official patches from there
- Fix for the issue of --add not being very smart
- Fix an issue causing rebuilds to fail to restart on reboot (data
  corrupter level problem)
- Reset the bad flag on map file updates
- Correctly fix failure when trying to add internal bitmap to 1.0 arrays
- Resolves: bz817023 (f17) bz817024 (f17) bz817026 (f17) bz817028 (f17)
- Resolves: bz817029 (f17) bz817032 (f17) bz817038 (f17) bz808774 (f17)
- Resolves: bz817039 (f17) bz817042 (f17)

* Mon Apr 30 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-8
- Fix bug where IMSM arrays stay inactive in case a reboot is
- performed during the reshape process.
- Resolves: bz817522 (f17) bz817535 (f16) bz817537 (f15)

* Wed Mar 28 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-7
- Fix issue when re-adding drive to a raid1 array with bitmap
- Resolves: bz807743 (f17) bz769323 (f16) bz791159 (f15)

* Thu Feb 23 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-6
- Fix double free on buggy old kernel sysfs read
- Fix segfault if trying to write superblock to non existing device
- Resolves: bz795707 (f17) bz795747 (f16) bz795748 (f15)
- Resolves: bz795461 (f17) bz795749 (f16) bz795750 (f15)

* Thu Feb 16 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-5
- Fix issue with devices failing to be added to a raid using bitmaps,
  due to trying to write the bitmap with mis-aligned buffers using
  O_DIRECT 
- Resolves: bz789898 (f16) bz791189 (f15)

* Mon Jan 30 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-4
- Add support for --offroot to mdadm/mdmon
- Resolves: bz785739 (rawhide) bz785737 (f16) bz771405 (f15)

* Thu Jan 12 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-3
- Fix case where we have to retry in case a remove fails due to an array
  being busy
- Resolves: bz773337 (rawhide) bz773340 (f16) bz773341 (f15)

* Thu Jan 5 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-2
- Workaround for gcc-4.7 strict aliasing breaking the build

* Wed Jan 4 2012 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.3-1
- Update to upstream 3.2.3
- Resolves: bz770110 (rawhide) bz771413 (f16) bz759014 (rawhide)
- Resolves: bz759015 (f16) bz759035 (rawhide) bz759036 (f16)
- Resolves: bz771608 (f15) bz759016 (f15) bz759039 (f15)

* Mon Nov 21 2011 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.2-15
- Backport upstream fix for memory leak that can prevent migration to
  RAID5 from completing.
- Backport upstream fix preventing mounting a device while it is in
  process of reshaping
- Resolves: bz755005 bz755009

* Wed Nov 9 2011 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.2-14
- Backport upstream fixes to prevent growing v0.90 metadata raid out
  of supported size.
- Add missing 'disable' argument to systemctl in preun script
- Resolves: bz735306 (Fedora 15) bz748731 (Fedora 16) bz748732 (rawhide),
  Resolves: bz751716

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-13
- Rebuilt for glibc bug#747377

* Sat Oct 22 2011 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.2-12
- Backport upstream version of fix for IMSM RAID assembly problem,
  which resolves issues when booting off sysvinit based system.
- Resolves: bz736387 (Fedora 15) bz744217 (Fedora 16)

* Wed Oct 19 2011 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.2-11
- Fix systemd dependency problem
- Resolves: bz741115 (F16) bz744226 (rawhide)

* Wed Oct 19 2011 Jes Sorensen <Jes.Sorensen@redhat.com> - 3.2.2-10
- Fix problem where a dirty IMSM RAID isn't assembled correctly during
  boot, preventing booting from this RAID device.
- Resolves: bz736387 (Fedora 15) bz744217 (Fedora 16)
- Fix race between udev and mdadm when assembling md device using
  mdadm -I, where udev would spawn an additional mdadm command to
  perform the assembly in parallel.

* Wed Aug 31 2011 Doug Ledford <dledford@redhat.com> - 3.2.2-9
- Fix boot with older imsm arrays that have an unused attribute set
- Resolves: bz729205

* Thu Aug 25 2011 Doug Ledford <dledford@redhat.com> - 3.2.2-8
- Rework the 65-md-incremental.rules file to add the following support:
  Nested md raid arrays should now work
  MD on top of LUKS or other lvm based devices should now work
  We should no longer grab multipath paths before multipath can

* Wed Jul 27 2011 Doug Ledford <dledford@redhat.com> - 3.2.2-7
- Fix a bug with readding a device
- Fix a bug with writemostly flag handling

* Mon Jul 18 2011 Doug Ledford <dledford@redhat.com> - 3.2.2-6
- Bump and rebuild again

* Fri Jul 15 2011 Doug Ledford <dledford@redhat.com> - 3.2.2-5
- Bump and rebuild to keep version ahead of f15 version

* Thu Jul 14 2011 Doug Ledford <dledford@redhat.com> - 3.2.2-4
- Fix minor issue in man page
- Resolves: bz717795

* Thu Jul 07 2011 Milan Broz <mbroz@redhat.com> - 3.2.2-3
- Use unit files with systemd. (johannbg)
- Add sub-package sysvinit for SysV init script.
- Resolves: bz713573

* Wed Jul 06 2011 Milan Broz <mbroz@redhat.com> - 3.2.2-2
- Fix build on PPC.
- Resolves: bz719380

* Tue Jun 28 2011 Milan Broz <mbroz@redhat.com> - 3.2.2-1
- Update to latest upstream version
- Resolves: bz714083

* Tue Jun 14 2011 Doug Ledford <dledford@redhat.com> - 3.2.1-5
- Fix for bz710646

* Thu Mar 31 2011 Doug Ledford <dledford@redhat.com> - 3.2.1-4
- Somehow the 64-md-raid.rules file went missing.  Put it back.
- Resolves: bz692248

* Thu Mar 31 2011 Doug Ledford <dledford@redhat.com> - 3.2.1-3
- Fix mdmonitor init script setup of SELinux on PIDPATH
- Resolves: bz692559

* Mon Mar 28 2011 Doug Ledford <dledford@redhat.com> - 3.2.1-2
- Restore build command to sane command instead of test command

* Mon Mar 28 2011 Doug Ledford <dledford@redhat.com> - 3.2.1-1
- Update to latest upstream version
- Resolves: 691353

* Fri Mar 25 2011 Doug Ledford <dledford@redhat.com> - 3.1.5-1
- Update to latest upstream stable release
- Update mdadm.rules file to honor noiswmd and nodmraid command line options
- Ghost the directory in /var/run, create /var/run/mdadm in mdmonitor init
  script
- Don't report mismatch counts on either raid1 or raid10
- Check both active and idle arrays during raid check runs
- Move the raid-check script from cron.weekly to /usr/sbin, add a crontab
  file to /etc/cron.d and mark it config(noreplace).  This way users can
  select their own raid-check frequency and have it honored through
  upgrades.
- Allow the raid-check script to set the process and io priority of the
  thread performing the check in order to preserve responsiveness of the
  machine during the check.
- Resolves: 633229, 656620. 679843, 671076, 659933

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-0.git20100804.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 04 2010 Doug Ledford <dledford@redhat.com> - 3.1.3-0.git20100804.2
- Add udev patch to not have incremental assembly in two rules files

* Wed Aug 04 2010 Doug Ledford <dledford@redhat.com> - 3.1.3-0.git20100804.1
- Update to latest upstream release (resolves an issue with stale lock
  files on the md device map file)

* Thu Jul 22 2010 Doug Ledford <dledford@redhat.com> - 3.1.3-0.git20100722.2
- Remove the glibc-static buildreq and don't build the static mdadm since
  we don't install it anyway
- Remove the udev file since adding it was supposed to be a rawhide only change

* Thu Jul 22 2010 Doug Ledford <dledford@redhat.com> - 3.1.3-0.git20100722.1
- Change git date format to the correct format (YYYYMMDD)
- Update to latest upstream push (fixes bz604023)

* Tue Jul 20 2010 Doug Ledford <dledford@redhat.com> - 3.1.3-0.git07202010.2
- Fix racy locking of mapfile (bz616596)

* Tue Jul 20 2010 Doug Ledford <dledford@redhat.com> - 3.1.3-0.git07202010.1
- Update to latest git repo (3.1.2 plus pending changes, fixes bz602457)
- Add in 64-md-raid.rules to compensate for it no longer being in udev
  (bz581905)
- Remove mdadm.static as its no longer used in initrd creation

* Tue Apr 13 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-10
- Minor update to mdadm.rules to make anaconda happy

* Thu Apr 08 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-9
- Slight fix on container patch

* Thu Apr 08 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-8
- Updated container patch that also enables mdadm -IRs for imsm devices

* Tue Apr 06 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-7
- Fix up directory in mdmonitor init script so that we restart mdmon like we
  are supposed to
- Add a rule to run incremental assembly on containers in case there are
  multiple volumes in a container and we only started some of them in the
  initramfs
- Make -If work with imsm arrays.  We had too restrictive of a test in
  sysfs_unique_holder.
- Make incremental assembly of containers act like incremental assembly of
  regular devices (aka, --run is needed to start a degraded array)

* Tue Apr 06 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-6
- Typo in new rules file

* Tue Apr 06 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-5
- Enable incremental support for imsm devices

* Tue Apr 06 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-4
- One line fix for ppc64 compiles

* Tue Apr 06 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-3
- Clean up directory mess once and for all
- Add incremental remove support

* Wed Mar 17 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-2
- Add a little more paranoia checking to the RebuildMap code to avoid ever
  having the same infinite loop as in bz569019 again even if we change file
  locations to somewhere where we can't create a mapfile

* Tue Mar 16 2010 Doug Ledford <dledford@redhat.com> - 3.1.2-1
- Grab latest upstream release instead of git repo snapshot (bz552344, bz572561)
- The lack of /dev/md is causing problems, so add code to mapfile.c to cause
  us to create /dev/md if it doesn't exist (bz569019)

* Tue Feb 23 2010 Doug Ledford <dledford@redhat.com> - 3.1.1-0.gcd9a8b5.6
- Newer version of imsm patch that leaves warning, but only when there
  actually are too many devices on the command line (bz554974)

* Sun Feb 21 2010 Doug Ledford <dledford@redhat.com> - 3.1.1-0.gcd9a8b5.5
- The uuid patch cause a different problem during assembly, so use a gross
  hack to work around the uuid issue that won't break assembly until fixed
  properly upstream (bz567132)

* Sun Feb 21 2010 Doug Ledford <dledford@redhat.com> - 3.1.1-0.gcd9a8b5.4
- Fix problem with booting multiple imsm containers when they aren't listed
  "just so" in the mdadm.conf file (bz554974)

* Fri Feb 19 2010 Doug Ledford <dledford@redhat.com> - 3.1.1-0.gcd9a8b5.3
- Don't run the raid-check script if the kernel doesn't support
  md devices (bz557053)
- Don't report any mismatch_cnt issues on raid1 devices as there are
  legitimate reasons why the count may not be 0 and we are getting enough
  false positives that it renders the check useless (bz554217, bz547128)

* Thu Feb 18 2010 Doug Ledford <dledford@redhat.com> - 3.1.1-0.gcd9a8b5.2
- Fix s390/ppc64 UUID byte swap issue

* Wed Feb 17 2010 Doug Ledford <dledford@redhat.com> - 3.1.1-0.gcd9a8b5.1
- Update to head of upstream git repo, which contains a significant number
  of bug fixes we need (bz543746)

* Fri Jan 15 2010 Doug Ledford <dledford@redhat.com> - 3.0.3-3
- Fix crash when AUTO keyword is in mdadm.conf (bz552342)

* Tue Dec 01 2009 Doug Ledford <dledford@redhat.com> - 3.0.3-2
- Minor tweak to init script for LSB compliance (bz527957)

* Wed Nov 04 2009 Doug Ledford <dledford@redhat.com> - 3.0.3-1
- New upstream release 3.0.3 (bz523320, bz527281)
- Update a couple internal patches
- Drop a patch in that was in Neil's tree for 3.0.3 that we had pulled for
  immediate use to resolve a bug
- Drop the endian patch because it no longer applied cleanly and all attempts
  to reproduce the original problem as reported in bz510605 failed, even up
  to and including downloading the specific package that was reported as
  failing in that bug and trying to reproduce with it on both ppc and ppc64
  hardware and with both ppc and ppc64 versions on the 64bit hardware.
  Without a reproducer, it is impossible to determine if a rehashed patch
  to apply to this code would actually solve the problem, so remove the patch
  entirely since the original problem, as reported, was an easy to detect DOA
  issue where installing to a raid array was bound to fail on reboot and so
  we should be able to quickly and definitively tell if the problem resurfaces.
- Update the mdmonitor init script for LSB compliance (bz527957)
- Link from mdadm.static man page to mdadm man page (bz529314)
- Fix a problem in the raid-check script (bz523000)
- Fix the intel superblock handler so we can test on non-scsi block devices

* Fri Oct  2 2009 Hans de Goede <hdegoede@redhat.com> - 3.0.2-1
- New upstream release 3.0.2
- Add a patch fixing mdadm --detail -export segfaults (bz526761, bz523862)
- Add a patch making mdmon store its state under /dev/.mdadm for initrd
  mdmon, rootfs mdmon handover
- Restart mdmon from initscript (when running) for rootfs mdmon handover

* Thu Sep 17 2009 Doug Ledford <dledford@redhat.com> - 3.0-4
- Stop some mdmon segfaults (bz523860)

* Tue Sep 15 2009 Doug Ledford <dledford@redhat.com> - 3.0-3
- Update to current head of upstream git repo for various imsm related fixes
  (fixes bz523262)
- Fix display of metadata version in output of Detail mode
- Add UUID output to --detail --export (bz523314)

* Fri Jul 24 2009 Doug Ledford <dledford@redhat.com> - 3.0-2
- Improved raid-check script as well as the ability to configure what devices
  get checked
- Endian patch for uuid generation

* Mon Jun 29 2009 Doug Ledford <dledford@redhat.com> - 3.0-1
- Remove stale patches already accepted by upstream
- Fix the raid-check script to only try and check a device if it is
  checkable
- Update to official mdadm-3.0 version
- Resolves: bz505587, bz505552

* Tue May 19 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel3.7
- Move the mdadm.map file from /dev/md/ to /dev/ so the installer doesn't
  need to precreate the /dev/md/ directory in order for incremental
  assembly to work

* Tue May 19 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel3.6
- Only check raid devices automatically, do not attempt to repair them
  during the weekly data scrubbing

* Fri Mar 20 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel3.5
- Fix a few issues with the new code to determine when a device gets to
  keep its name and when it doesn't

* Fri Mar 20 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel3.4
- Change the perms on the udev rules file, it doesn't need to be +x

* Fri Mar 20 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel3.3
- Slightly tweak the udev rules to make sure we don't start arrays
  while running in rc.sysinit...leave array starting to it instead
- Modify mdadm to put its mapfile in /dev/md instead of /var/run/mdadm
  since at startup /var/run/mdadm is read-only by default and this
  breaks incremental assembly
- Change how mdadm decides to assemble incremental devices using their 
  preferred name or a random name to avoid possible conflicts when plugging
  a foreign array into a host

* Wed Mar 18 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel3.2
- Change around the mdadm udev rules we ship to avoid a udev file conflict

* Tue Mar 17 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel3.1
- Update to latest devel release
- Remove the no longer necessary udev patch
- Remove the no longer necessary warn patch
- Remove the no longer necessary alias patch
- Update the mdadm.rules file to only pay attention to device adds, not
  changes and to enable incremental assembly
- Add a cron job to run a weekly repair of the array to correct bad sectors
- Resolves: bz474436, bz490972

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.devel2.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel2.2
- Readd our old mdadm rules file that does incremental assembly
- Remove the new mdadm rules file from upstream as we already have this in
  our udev package (and the one in the udev package already has a bug fixed)

* Thu Feb 12 2009 Doug Ledford <dledford@redhat.com> - 3.0-0.devel2.1
- Update to latest upstream devel release
- Use the udev rules file included with mdadm instead of our own
- Drop all the no longer relevant patches
- Fix a build error in mdopen.c
- Fix the udev rules path in Makefile
- Fix a compile issue with the __le32_to_cpu() macro usage (bad juju to
  to operations on the target of the macro as it could get executed
  multiple times, and gcc now throws an error on that)
- Add some casts to some print statements to keep gcc from complaining

* Fri Oct 24 2008 Doug Ledford <dledford@redhat.com> - 2.6.7.1-1
- Updated to latest upstream stable release (#466803)
- Change udev rule to not assemble degraded arrays (#453314)
- Fix metadata matching in config file (#466078)
- Fix assembly of raid10 devices (#444237)
- Fix incremental assembly of partitioned raid devices (#447818)

* Thu Jun 26 2008 Doug Ledford <dledford@redhat.com> - 2.6.7-1
- Update to latest upstream version (should resolve #444237)
- Drop incremental patch as it's now part of upstream
- Clean up all the open() calls in the code (#437145)
- Fix the build process to actually generate mdassemble (#446988)
- Update the udev rules to get additional info about arrays being assembled
  from the /etc/mdadm.conf file (--scan option) (#447818)
- Update the udev rules to run degraded arrays (--run option) (#452459)

* Thu Apr 17 2008 Bill Nottingham <notting@redhat.com> - 2.6.4-4
- make /dev/md if necessary in incremental mode (#429604)
- open RAID devices with O_EXCL to avoid racing against other --incremental processes (#433932)

* Fri Feb  1 2008 Bill Nottingham <notting@redhat.com> - 2.6.4-3
- add a udev rules file for device assembly (#429604)

* Fri Jan 18 2008 Doug Ledford <dledford@redhat.com> - 2.6.4-2
- Bump version and rebuild

* Fri Oct 19 2007 Doug Ledford <dledford@redhat.com> - 2.6.4-1
- Update to latest upstream and remove patches upstream has taken

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.6.2-5
- Rebuild for selinux ppc32 issue.

* Mon Jul 09 2007 Doug Ledford <dledford@redhat.com> - 2.6.2-4
- Oops, if we call -C -e1, minor_version is no longer properly set, fix that
  up
- Related: bz230207

* Fri Jul 06 2007 Doug Ledford <dledford@redhat.com> - 2.6.2-3
- Oops, had to update the file leak patch, missed one thing
- Minor tweak to return codes in init script and add LSB header
- Resolves: bz244582, bz246980

* Mon Jul 02 2007 Doug Ledford <dledford@redhat.com> - 2.6.2-2
- Fix a file leak issue when mdadm is in monitor mode
- Update mdadm init script so that status will always run and so
  return codes are standards compliant
- Fix assembly of version 1 superblock devices
- Make the attempt to create an already running device have a clearer
  error message
- Allow the creation of a degraded raid4 array like we allow for raid5
- Make mdadm actually pay attention to raid4 devices when in monitor mode
- Make the mdmonitor script use daemon() correctly
- Fix a bug where manage mode would not add disks correctly under certain
  conditions
- Resolves: bz244582, bz242688, bz230207, bz169516, bz171862, bz171938
- Resolves: bz174642, bz224272, bz186524

* Mon Jul 02 2007 Doug Ledford <dledford@redhat.com> - 2.6.2-1
- Update to latest upstream
- Remove requirement for /usr/sbin/sendmail - it's optional and not on by
  default, and sendmail isn't *required* for mdadm itself to work, and isn't
  even required for the monitoring capability to work, just if you want to
  have the monitoring capability do the automatic email thing instead of
  run your own program (and if you use the program option of the monitor
  capability, your program could email you in a different manner entirely)

* Mon Apr 16 2007 Doug Ledford <dledford@redhat.com> - 2.6.1-4
- More cleanups for merge review process
- Related: bz226134

* Wed Apr 11 2007 Doug Ledford <dledford@redhat.com> - 2.6.1-3
- Various cleanups as part of merge review process
- Related: bz226134

* Sat Mar 31 2007 Doug Ledford <dledford@redhat.com> - 2.6.1-2
- Oops, missing a dependency in the Makefile

* Sat Mar 31 2007 Doug Ledford <dledford@redhat.com> - 2.6.1-1
- Update to latest upstream version
- Resolves: bz233422

* Fri Jan 26 2007 Doug Ledford <dledford@redhat.com> - 2.6-1
- Update to latest upstream version
- Remove the mdmpd daemon entirely.  Now that multipath tools from the lvm/dm
  packages handles multipath devices well, this is no longer needed.
- Various cleanups in the spec file

* Thu Nov 09 2006 Doug Ledford <dledford@redhat.com> - 2.5.4-3
- Add a fix for the broken printout of array GUID when using the -E --brief
  flags

* Fri Oct 13 2006 Doug Ledford <dledford@redhat.com> - 2.5.4-2
- tag present on another branch and can't be forcibly moved
  required number bump

* Fri Oct 13 2006 Doug Ledford <dledford@redhat.com> - 2.5.4-1
- Update to 2.5.4 (listed as a bugfix update by upstream)
- Remove previous bitmap patch that's now part of 2.5.4

* Sun Oct  8 2006 Doug Ledford <dledford@redhat.com> - 2.5.3-2
- Fix a big-endian machine error in the bitmap code (Paul Clements)

* Mon Aug  7 2006 Doug Ledford <dledford@redhat.com> - 2.5.3-1
- Update to 2.5.3 which upstream calls a "bug fix" release

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.5.2-1.1
- rebuild

* Fri Jul  7 2006 Doug Ledford <dledford@redhat.com> - 2.5.2-1
- Update to 2.5.2
- Remove auto default patch as upstream now has a preferred default auto method

* Wed Mar  8 2006 Peter Jones <pjones@redhat.com> - 2.3.1-3
- fix build on ppc64

* Wed Mar  8 2006 Jeremy Katz <katzj@redhat.com> - 2.3.1-2
- fix build on ppc

* Wed Mar  8 2006 Jeremy Katz <katzj@redhat.com> - 2.3.1-1
- update to 2.3.1 to fix raid5 (#184284)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2-1.fc5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2-1.fc5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec 05 2005 Warren Togami <wtogami@redhat.com> 2.2-1
- 2.2 upgrade (#167897)
- disable diet because we don't ship it anymore
  and we don't actually use mdassemble now

* Mon May 16 2005 Doug Ledford <dledford@redhat.com> 1.11.0-4.fc4
- Make the mdmonitor init script use the pid-file option, major cleanup
  of the script now possible (#134459)

* Mon May 16 2005 Doug Ledford <dledford@redhat.com> 1.11.0-3.fc4
- Put back the obsoletes: raidtools that was present in 1.11.0-1.fc4

* Mon May 16 2005 Doug Ledford <dledford@redhat.com> 1.11.0-2.fc4
- Change the default auto= mode so it need not be on the command line to
  work with udev, however it is still supported on the command line (#132706)
- Add a man page (from Luca Berra) for mdassemble

* Wed May 11 2005 Doug Ledford <dledford@redhat.com> - 1.11.0-1.fc4
- Upgrade to 1.11.0

* Wed Apr 27 2005 Jeremy Katz <katzj@redhat.com> - 1.9.0-3.fc4
- fix mdmonitor initscript (#144717)

* Mon Mar 21 2005 Doug Ledford <dledford@redhat.com> 1.9.0-2
- Build mdadm.static and mdassemble (static as well) to be used in initrd
  images

* Wed Mar 09 2005 Doug Ledford <dledford@redhat.com> 1.9.0-1
- Initial upgrade to 1.9.0 and update of doc files
- Fix an s390 build error

* Mon Oct 04 2004 Doug Ledford <dledford@redhat.com> 1.6.0-2
- Remove /etc/mdadm.conf from the file list.  Anaconda will write one out
  if it's needed.

* Fri Oct 01 2004 Doug Ledford <dledford@redhat.com> 1.6.0-1
- Update to newer upstream version
- Make mdmpd work on kernels that don't have the event interface patch

* Fri Jul 30 2004 Dan Walsh <dwalsh@redhat.com> 1.5.0-11
- Create a directory /var/run/mdadm to contain mdadm.pid
- This cleans up SELinux problem

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 22 2004 Doug Ledford <dledford@redhat.com> - 1.5.0-9
- Fix Makefile and build method to satisfy bz #123769
- Add mdmpd man page, update mdmpd version to 0.3 - bz #117160
- Make sure mdadm --monitor closes all md device files so that md devices
  can be stopped while mdadm is still running - bz #119532

* Thu May 20 2004 Jeremy Katz <katzj@redhat.com> - 1.5.0-8
- remove unneeded patch, can use --run instead

* Wed May 19 2004 Jeremy Katz <katzj@redhat.com> - 1.5.0-7
- add patch with reallyforce mode on creation to be used by anaconda

* Wed May 12 2004 Doug Ledford <dledford@redhat.com> 2.5.0-6
- Fix a bug in the postun scriptlet related to downgrading to a version
  of mdadm that doesn't include the mdmpd daemon.

* Fri May 07 2004 Doug Ledford <dledford@redhat.com> 1.5.0-5
- Disable service mdmpd by default to avoid [Failed] messages on
  current 2.6 kernels.  Possibly re-enable it by default once the
  2.6 kernels have the md event interface.

* Thu Apr 22 2004 Doug Ledford <dledford@redhat.com> 1.5.0-4
- Update mdmonitor script to start daemon more cleanly
- Repackage mdmpd tarball to include gcc-3.4 changes and to make
  mdmpd properly daemonize at startup instead of forking and leaving
  the child attached to the terminal.

* Thu Mar  4 2004 Bill Nottingham <notting@redhat.com> 1.5.0-3
- ship /var/run/mpmpd (#117497)

* Thu Feb 26 2004 Doug Ledford <dledford@redhat.com> 1.5.0-2
- Add a default MAILADDR line to the mdadm.conf file installed by default
  (Bugzilla #92447)
- Make it build with gcc-3.4

* Mon Feb 23 2004 Doug Ledford <dledford@redhat.com> 1.5.0-1
- Update to 1.5.0 (from Matthew J. Galgoci <mgalgoci@redhat.com>)

* Sun Nov 16 2003 Doug Ledford <dledford@redhat.com> 1.4.0-1
- fix problem with recovery thread sleeping in mdmpd

* Fri Nov 14 2003 Doug Ledford <dledford@redhat.com>
- sync upstream
- add mdmpd package into mdadm package

* Wed Sep 10 2003 Michael K. Johnson <johnsonm@redhat.com> 1.3.0-1
- sync upstream

* Tue Mar 11 2003 Michael K. Johnson <johnsonm@redhat.com> 1.1.0-1
- sync upstream

* Tue Jan 28 2003 Michael K. Johnson <johnsonm@redhat.com> 1.0.1-1
- update for rebuild

* Wed Dec 25 2002 Tim Powers <timp@redhat.com> 1.0.0-8
- fix references to %%install in the changelog so that it will build

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com> 1.0.0-7
- Rebuild

* Fri Jul 12 2002 Michael K. Johnson <johnsonm@redhat.com>
- Changed RPM Group to System Environment/Base

* Wed May 15 2002 Michael K. Johnson <johnsonm@redhat.com>
- minor cleanups to the text, conditionalize rm -rf
- added mdmonitor init script

* Fri May 10 2002  <neilb@cse.unsw.edu.au>
- update to 1.0.0
- Set CXFLAGS instead of CFLAGS

* Sat Apr  6 2002  <neilb@cse.unsw.edu.au>
- change %%install to use "make install"

* Fri Mar 15 2002  <gleblanc@localhost.localdomain>
- beautification
- made mdadm.conf non-replaceable config
- renamed Copyright to License in the header
- added missing license file
- used macros for file paths

* Fri Mar 15 2002 Luca Berra <bluca@comedia.it>
- Added Obsoletes: mdctl
- missingok for configfile

* Tue Mar 12 2002 NeilBrown <neilb@cse.unsw.edu.au>
- Add md.4 and mdadm.conf.5 man pages

* Fri Mar 08 2002 Chris Siebenmann <cks@cquest.utoronto.ca>
- builds properly as non-root.

* Fri Mar 08 2002 Derek Vadala <derek@cynicism.com>
- updated for 0.7, fixed /usr/share/doc and added manpage

* Tue Aug 07 2001 Danilo Godec <danci@agenda.si>
- initial RPM build
