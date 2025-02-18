# this is purely a shell script, so no debug packages
%global debug_package %{nil}

Name: rear
Version: 2.9
Release: 2%{?dist}
Summary: Relax-and-Recover is a Linux disaster recovery and system migration tool
URL: https://relax-and-recover.org

License: GPL-3.0-or-later AND LGPL-2.1-or-later

Source0: https://github.com/rear/rear/archive/%{version}/rear-%{version}.tar.gz
# Add cronjob and systemd timer as documentation
Source1: rear.cron
Source2: rear.service
Source3: rear.timer

# Required for HTML user guide
BuildRequires: asciidoctor
BuildRequires: efi-srpm-macros
# Needed for %%autosetup -S git
BuildRequires: git-core
BuildRequires: make

######################
# upstream backports #
######################
# Patch101 - Patch121 Reserved
# Empty...

######################
# downstream patches #
######################
# No-longer applicable
# Patch201: rear-bz1492177-warning.patch

# avoid vgcfgrestore on unsupported volume types
# https://github.com/pcahyna/rear/commit/5d5d1db3ca621eb80b9481924d1fc470571cfc09
Patch202: rear-bz1747468.patch

# No-longer applicable
# Patch203: rear-bz2119501.patch

# additional fixes for NBU support
Patch204: rear-bz2120736.patch
Patch205: rear-bz2188593-nbu-systemd.patch
Patch206: rear-nbu-RHEL-17390-RHEL-17393.patch

# rear contains only bash scripts plus documentation so that on first glance it could be "BuildArch: noarch"
# but actually it is not "noarch" because it only works on those architectures that are explicitly supported.
# Of course the rear bash scripts can be installed on any architecture just as any binaries can be installed on any architecture.
# But the meaning of architecture dependent packages should be on what architectures they will work.
# Therefore only those architectures that are actually supported are explicitly listed.
# This avoids that rear can be "just installed" on architectures that are actually not supported (e.g. ARM):
ExclusiveArch: %ix86 x86_64 ppc ppc64 ppc64le ia64 s390x
# Furthermore for some architectures it requires architecture dependent packages (like syslinux for x86 and x86_64)
# so that rear must be architecture dependent because ifarch conditions never match in case of "BuildArch: noarch"
# see the GitHub issue https://github.com/rear/rear/issues/629
%ifarch %ix86 x86_64
Requires: syslinux-extlinux
%endif
%ifarch ppc ppc64 ppc64le
# Called by grub2-install (except on PowerNV)
Requires:   /usr/sbin/ofpathname
# Needed to make PowerVM LPARs bootable
Requires:   /usr/sbin/bootlist
%endif
%ifarch s390x
# Contain many utilities for working with DASDs
Requires:   s390utils-base
Requires:   s390utils-core
%endif

# See https://github.com/rhboot/efi-rpm-macros/blob/main/README
%ifarch %{efi}
# We need mkfs.vfat for recreating EFI System Partition
Requires: dosfstools
# Needed for ISO image creation
Requires: grub2-efi-%{efi_arch}-modules
%endif


### Mandatory dependencies:
Requires: attr
Requires: bc
Requires: binutils
Requires: dhcpcd
Requires: ethtool
Requires: file
Requires: gawk
Requires: gzip
Requires: iproute
Requires: iputils
Requires: openssl
Requires: parted
Requires: tar
# No ISO image support on s390x (may change when we add support for LPARs)
%ifnarch s390x
Requires: xorriso
%endif
%if 0%{?rhel}
Requires: util-linux
%endif

%description
Relax-and-Recover is the leading Open Source disaster recovery and system
migration solution. It comprises of a modular
frame-work and ready-to-go workflows for many common situations to produce
a bootable image and restore from backup using this image. As a benefit,
it allows to restore to different hardware and can therefore be used as
a migration tool as well.

Currently Relax-and-Recover supports various boot media (incl. ISO, PXE,
OBDR tape, USB or eSATA storage), a variety of network protocols (incl.
sftp, ftp, http, nfs, cifs) as well as a multitude of backup strategies
(incl.  IBM TSM, MircroFocus Data Protector, Symantec NetBackup, EMC NetWorker,
Bacula, Bareos, BORG, Duplicity, rsync).

Relax-and-Recover was designed to be easy to set up, requires no maintenance
and is there to assist when disaster strikes. Its setup-and-forget nature
removes any excuse for not having a disaster recovery solution implemented.

Professional services and support are available.

#-- PREP, BUILD & INSTALL -----------------------------------------------------#
%prep
%autosetup -p1 -S git

# Change /lib to /usr/lib for COPY_AS_IS
sed -E -e "s:([\"' ])/lib:\1/usr/lib:g" \
    -i usr/share/rear/prep/GNU/Linux/*include*.sh

# Same for Linux.conf
sed -e 's:/lib/:/usr/lib/:g' \
    -e 's:/lib\*/:/usr/lib\*/:g' \
    -e 's:/usr/usr/lib:/usr/lib:g' \
    -i 'usr/share/rear/conf/GNU/Linux.conf'

%build
# build HTML user guide
# asciidoc writes a timestamp to files it produces, based on the last
# modified date of the source file, but is sensitive to the timezone.
# This makes the results differ according to the timezone of the build machine
# and spurious changes will be seen.
# Set the timezone to UTC as a workaround.
# https://wiki.debian.org/ReproducibleBuilds/TimestampsInDocumentationGeneratedByAsciidoc
TZ=UTC %make_build doc

%install
%make_install sbindir=%{_sbindir}
install -p -d %{buildroot}%{_docdir}/%{name}/
install -m 0644 %{SOURCE1} %{buildroot}%{_docdir}/%{name}/
install -m 0644 %{SOURCE2} %{buildroot}%{_docdir}/%{name}/
install -m 0644 %{SOURCE3} %{buildroot}%{_docdir}/%{name}/

#-- FILES ---------------------------------------------------------------------#
%files
%license COPYING
%doc MAINTAINERS README.md doc/user-guide doc/*.txt
%dir %{_sysconfdir}/rear/
%config(noreplace) %{_sysconfdir}/rear/local.conf
%{_datadir}/rear/
%{_docdir}/%{name}/rear.*
%{_mandir}/man8/rear.8*
%{_sbindir}/rear
%{_sharedstatedir}/rear/

#-- CHANGELOG -----------------------------------------------------------------#
%changelog
* Wed Feb 05 2025 Lukáš Zaoral <lzaoral@redhat.com> - 2.9-2
- require syslinux-extlinux which is necessary for USB devices bootable on
  legacy BIOS

* Tue Feb 04 2025 Lukáš Zaoral <lzaoral@redhat.com> - 2.9-1
- rebase to version 2.9 (rhbz#2343296)
- drop upstreamed patches
- remove obsolete patch for rhbz2119501
  - ReaR 2.7 and newer do not copy dangling symlinks in /lib/modules/*/
- remove broken patch for rhbz1492177 (VERBOSE is a read-only var, so the script silently failed)
  - install correct packages using proper RPM dependencies instead
- rebase remaining patches

* Tue Jan 21 2025 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-14
- fix FTBFS after F42 bin/sbin merge

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug  8 2024 Pavel Cahyna <pcahyna@redhat.com> - 2.7-12
- Remove doc/rear-release-notes.txt, it is CC-BY-ND-3.0, which is not an allowed
  license for documentation, and use a cleaned tarball (with the file removed)
  for build

* Wed Aug  7 2024 Pavel Cahyna <pcahyna@redhat.com> - 2.7-11
- Generate /etc/rear/os.conf during build again, it is better than generating it
  in %%post, but do not mark it as config file to allow it to be updated during
  package upgrade and avoid containing an old OS version information

* Mon Aug 05 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-10
- skip btrfs subvolumes when detecting ESP partitions
- fix booting on UEFI systems with multiple CDROM devices
- fix copying of console kernel cmdline parameters
- Use git to apply patches in %%prep
- Sync with patches in CentOS Stream 9 (kudos to @pcahyna!):
  - Backport PR 3250 to fix useless warning that libsystemd-core requires
    additional libraries and ReaR recovery system needs additional libraries
  - Backport PR 3242 to fix IPv6 address in nfs:// and sshfs://
    BACKUP/OUTPUT_URL
- fix backup of btrfs subvolumes

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 09 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-8
- Sync with patches in CentOS Stream 9 (kudos to @pcahyna!) chronologically
  from the latest:
  - Resolve libs for executable links in COPY_AS_IS, PR 3073
  - Skip invalid disk drives when saving layout PR 3047
  - Do not delete NetBackup logs in case of errors and save
    /usr/openv/netbackup/logs to the restored system after a successful recovery
  - Add /usr/openv/var to COPY_AS_IS_NBU, fixes an issue seen
    with NetBackup 10.2.0.1
  - Support saving and restoring hybrid BIOS/UEFI bootloader, PRs 3145 3136

* Thu Feb 08 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-7
- do not generate /etc/rear/os.conf during build

* Wed Feb 07 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-6
- copy the console= kernel arguments from the original system

* Tue Feb 06 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-5
- replace dhcp-client with dhcpcd (rhbz#2247060)

* Tue Feb 06 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-4
- make initrd accessible only by root (CVE-2024-23301)

* Tue Feb 06 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-3
- fix unusable recovery with newer systemd (rbhz#2254871)

* Mon Feb 05 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-2
- migrate to SPDX license format
- properly use %%license and %%doc macros
- use https in URLs

* Fri Feb 02 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.7-1
- rebase to version 2.7 (rhbz#2215778)
- drop obsolete patches
- rebase remaining patches

* Fri Feb  2 2024 Lukáš Zaoral <lzaoral@redhat.com> - 2.6-14
- Sync with patches in CentOS Stream 9 (kudos to @pcahyna!) chronologically
  from the latest:
  - Backport PR 3061 to save LVM pool metadata volume size in disk layout
    and restore it
  - Backport PR 3058 to skip useless xfs mount options when mounting
    during recovery, prevents mount errors like "logbuf size must be greater
    than or equal to log stripe size"
  - Add patch to force removal of lvmdevices, prevents LVM problems after
    restoring to different disks/cloning. Upstream PR 3043
  - Add patch to start rsyslog and include NBU systemd units
  - Apply PR 3027 to ensure correct creation of the rescue environment
    when a file is shrinking while being read
  - Backport PR 2774 to increase USB_UEFI_PART_SIZE to 1024 MiB
  - Apply upstream patch for temp dir usage with LUKS to ensure
    that during recovery an encrypted disk can be unlocked using a keyfile
  - Backport upstream PR 3031: Secure Boot support for OUTPUT=USB
  - Correct a mistake done when backporting PR 2691
  - Backport PR2943 to fix s390x dasd formatting
  - Require s390utils-{core,base} on s390x
  - Apply PR2903 to protect against colons in pvdisplay output
  - Apply PR2873 to fix initrd regeneration on s390x
  - Apply PR2431 to migrate XFS configuration files
  - Exclude /etc/lvm/devices from the rescue system to work around a segfault
    in lvm pvcreate
  - Avoid stderr message about irrelevant broken links
  - Changes for NetBackup (NBU) 9.x support
  - Backport PR2831 - rsync URL refactoring
    fixes rsync OUTPUT_URL when different from BACKUP_URL
  - Apply PR2795 to detect changes in system files between backup
    and rescue image
  - Apply PR2808 to exclude dev/watchdog* from recovery system
  - Backport upstream PRs 2827 and 2839 to pass -y to lvcreate instead of one "y"
    on stdin
  - Apply PR2811 to add the PRE/POST_RECOVERY_COMMANDS directives
  - Recommend dosfstools on x86_64, needed for EFI System Partition
  - Backport PR2825 to replace defunct mkinitrd with dracut
  - Apply PR2580 to load the nvram module in the rescue environment in order
    to be able to set the boot order on ppc64le LPARs
  - Backport PR2822 to include the true vi executable in rescue ramdisk
  - Apply PR2675 to fix leftover temp dir bug (introduced in backported PR2625)
  - Apply PR2603 to ignore unused PV devices
  - Apply upstream PR2750 to avoid exclusion of wanted multipath devices
  - Remove unneeded xorriso dep on s390x (no ISO image support there)
  - Apply upstream PR2736 to add the EXCLUDE_{IP_ADDRESSES,NETWORK_INTERFACES}
    options
  - Add patch for better handling of thin pools and other LV types not supported
    by vgcfgrestore
  - Sync spec changes and downstream patches from RHEL 8 rear-2.6-2
    - Fix multipath performance regression in 2.6, introduced by upstream PR #2299.
      Resolves: rhbz1993296
    - On POWER add bootlist & ofpathname to the list of required programs
      conditionally (bootlist only if running under PowerVM, ofpathname
      always except on PowerNV) - upstream PR2665, add them to package
      dependencies
      Resolves: rhbz1983013
    - Backport PR2608:
      Fix setting boot path in case of UEFI partition (ESP) on MD RAID
      Resolves: rhbz1945869
    - Backport PR2625
      Prevents accidental backup removal in case of errors
      Resolves: rhbz1958247
    - Fix rsync error and option handling
      Resolves: rhbz1930662
  - Put TMPDIR on /var/tmp by default, otherwise it may lack space
    RHBZ #1988420, upstream PR2664
  - Sync spec changes and downstream patches from RHEL 8
    - Require xorriso instead of genisoimage
    - Add S/390 support and forgotten dependency on the file utility
    - Backport upstream code related to LUKS2 support
    - Modify the cron command to avoid an e-mail with error message after
      ReaR is installed but not properly configured when the cron command
      is triggered for the first time
    - Changes for NetBackup (NBU) support, upstream PR2544
  - Add dependency on dhcp-client, RHBZ #1926451

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.6-10
- Switch to xorriso for iso image creation

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Feb 26 2021 Christopher Engelhard <ce@lcts.de> - 2.6-5
- Change /lib to /usr/lib in scripts to fix RHBZ #1931112

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 23 2020 Christopher Engelhard <ce@lcts.de> - 2.6-3
- Stop auto-creating a cronjob, but ship example cronjob/
  systemd timer units in docdir instead (upstream issue #1829)
- Build & ship HTML user guide
- Remove %pre scriptlet, as it was introduced only to fix a
  specific upgrade issue with v1.15 in 2014

* Tue Sep 22 2020 Christopher Engelhard <ce@lcts.de> - 2.6-2
- Backport upstream PR#2469 to fix RHBZ #1831311

* Tue Sep 22 2020 Christopher Engelhard <ce@lcts.de> - 2.6-1
- Update to 2.6
- Streamline & clean up spec file

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 30 2015 Johannes Meixner <jsmeix@suse.de>
- For a changelog see the rear-release-notes.txt file.

