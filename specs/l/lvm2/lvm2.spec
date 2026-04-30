## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global device_mapper_version 1.02.208

%global enable_cache 1
%global enable_lvmdbusd 1
%global enable_lvmlockd 1
%global enable_lvmpolld 1
%global enable_thin 1
%global enable_dmfilemapd 1
%global enable_testsuite 1
%global enable_vdo 1
%global enable_writecache 1
%global enable_integrity 1

%global system_release_version 23
%global systemd_version 256~rc1
%global dracut_version 002-18
%global util_linux_version 2.24
%global bash_version 4.0
%global dlm_version 4.0.6-1
%global libselinux_version 1.30.19-4
%global persistent_data_version 0.7.0-0.1.rc6
%global sanlock_version 3.3.0-2

%global enable_lockd_sanlock %{enable_lvmlockd}
%if 0%{?rhel} >= 10
%global enable_lockd_dlm 0
%else
%global enable_lockd_dlm %{enable_lvmlockd}
%endif

%if 0%{?rhel} && 0%{?rhel} <= 8
  %ifnarch i686 x86_64 ppc64le s390x
    %global enable_lockd_dlm 0
  %endif

  %ifnarch x86_64 ppc64 aarch64
    %global enable_lockd_sanlock 0
  %endif
%endif

# Do not reset Release to 1 unless both lvm2 and device-mapper
# versions are increased together.
#
# NOTE: At the moment it is better to increase DM version together with lvm.
# This siplifies life for other packagers as well.

Summary: Userland logical volume management tools
Name: lvm2
%if 0%{?rhel}
Epoch: %{rhel}
%endif
Version: 2.03.34
Release: %autorelease
License: GPL-2.0-only
URL: https://sourceware.org/lvm2
Source0: https://sourceware.org/pub/lvm2/releases/LVM2.%{version}.tgz

BuildRequires: make
BuildRequires: gcc
%if %{enable_testsuite}
BuildRequires: gcc-c++
%endif
BuildRequires: libselinux-devel >= %{libselinux_version}, libsepol-devel
BuildRequires: libblkid-devel >= %{util_linux_version}
BuildRequires: ncurses-devel
BuildRequires: libedit-devel
BuildRequires: libaio-devel
%if %{enable_lockd_dlm}
BuildRequires: dlm-devel >= %{dlm_version}
%endif
BuildRequires: module-init-tools
BuildRequires: pkgconfig
BuildRequires: systemd-devel
BuildRequires: systemd-units
%if %{enable_lvmdbusd}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-dbus
BuildRequires: python3-pyudev
%endif
%if %{enable_thin} || %{enable_cache}
BuildRequires: device-mapper-persistent-data >= %{persistent_data_version}
%endif
%if %{enable_lockd_sanlock}
BuildRequires: sanlock-devel >= %{sanlock_version}
%endif
Requires: %{name}-libs = %{?epoch}:%{version}-%{release}
%if 0%{?fedora}
Requires(post): (system-release >= %{system_release_version} if system-release)
%endif
Requires: bash >= %{bash_version}
Requires(post): systemd-units >= %{systemd_version}, systemd-sysv
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}
Requires: module-init-tools
%if %{enable_thin} || %{enable_cache}
Requires: device-mapper-persistent-data >= %{persistent_data_version}
%endif

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/lvm
%endif

%description
LVM2 includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadm(8) or even loop devices, see
losetup(8)), creating volume groups (kind of virtual disks) from one
or more physical volumes and creating one or more logical volumes
(kind of logical partitions) in volume groups.

%prep
%autosetup -p1 -n LVM2.%{version}

%build
%global _default_pid_dir /run
%global _default_dm_run_dir /run
%global _default_run_dir /run/lvm
%global _default_locking_dir /run/lock/lvm

%global _udevdir %{_prefix}/lib/udev/rules.d

%configure \
  --with-default-dm-run-dir=%{_default_dm_run_dir} \
  --with-default-run-dir=%{_default_run_dir} \
  --with-default-pid-dir=%{_default_pid_dir} \
  --with-default-locking-dir=%{_default_locking_dir} \
  --with-usrlibdir=%{_libdir} \
  --enable-fsadm \
  --enable-write_install \
  --with-user= \
  --with-group= \
  --with-device-uid=0 \
  --with-device-gid=6 \
  --with-device-mode=0660 \
  --enable-pkgconfig \
  --enable-cmdlib \
  --enable-dmeventd \
  --enable-blkid_wiping \
  --with-udevdir=%{_udevdir} --enable-udev_sync \
%if %{enable_thin}
  --with-thin=internal \
%endif
%if %{enable_cache}
  --with-cache=internal \
%endif
%if %{enable_lvmpolld}
  --enable-lvmpolld \
%endif
%if %{enable_lockd_dlm}
  --enable-lvmlockd-dlm --enable-lvmlockd-dlmcontrol \
%endif
%if %{enable_lockd_sanlock}
  --enable-lvmlockd-sanlock \
%endif
%if %{enable_lvmdbusd}
  --enable-dbus-service --enable-notify-dbus \
%endif
%if %{enable_dmfilemapd}
  --enable-dmfilemapd \
%endif
%if %{enable_writecache}
  --with-writecache=internal \
%endif
%if %{enable_vdo}
  --with-vdo=internal --with-vdo-format=%{_bindir}/vdoformat \
%endif
%if %{enable_integrity}
  --with-integrity=internal \
%endif
  --with-default-use-devices-file=1 \
  --disable-silent-rules \
  --enable-app-machineid \
  --enable-editline \
  --disable-readline

V=1 %make_build

%install
V=1 %make_install
V=1 make install_system_dirs DESTDIR=$RPM_BUILD_ROOT
V=1 make install_systemd_units DESTDIR=$RPM_BUILD_ROOT
V=1 make install_systemd_generators DESTDIR=$RPM_BUILD_ROOT
V=1 make install_tmpfiles_configuration DESTDIR=$RPM_BUILD_ROOT
#install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/lvm/devices
%if %{enable_testsuite}
%make_install -C test
%endif

%post
%systemd_post blk-availability.service lvm2-monitor.service
if [ "$1" = "1" ] ; then
	# FIXME: what to do with this? We do not want to start it in a container/chroot
	# enable and start lvm2-monitor.service on completely new installation only, not on upgrades
	systemctl enable lvm2-monitor.service
	systemctl start lvm2-monitor.service >/dev/null 2>&1 || :
fi

%if %{enable_lvmpolld}
%systemd_post lvm2-lvmpolld.socket
# lvm2-lvmpolld socket is always enabled and started and ready to serve if lvmpolld is used
# replace direct systemctl calls with systemd rpm macro once this is provided in the macro:
# http://cgit.freedesktop.org/systemd/systemd/commit/?id=57ab2eabb8f92fad5239c7d4492e9c6e23ee0678
systemctl enable lvm2-lvmpolld.socket
systemctl start lvm2-lvmpolld.socket >/dev/null 2>&1 || :
%endif

%preun
%systemd_preun blk-availability.service lvm2-monitor.service

%if %{enable_lvmpolld}
%systemd_preun lvm2-lvmpolld.service lvm2-lvmpolld.socket
%endif

%postun
%systemd_postun lvm2-monitor.service

%if %{enable_lvmpolld}
%systemd_postun_with_restart lvm2-lvmpolld.service
%endif

%triggerun -- %{name} < 2.02.86-2
%{_bindir}/systemd-sysv-convert --save lvm2-monitor >/dev/null 2>&1 || :
/bin/systemctl --no-reload enable lvm2-monitor.service > /dev/null 2>&1 || :
/sbin/chkconfig --del lvm2-monitor > /dev/null 2>&1 || :
/bin/systemctl try-restart lvm2-monitor.service > /dev/null 2>&1 || :

%files
%license COPYING COPYING.LIB
%doc README VERSION WHATS_NEW
%doc doc/lvm_fault_handling.txt

# Main binaries
%{_sbindir}/fsadm
%{_sbindir}/lvm
%{_sbindir}/lvmconfig
%{_sbindir}/lvmdevices
%{_sbindir}/lvmdump
%{_sbindir}/lvmpersist
%if %{enable_lvmpolld}
%{_sbindir}/lvmpolld
%endif
%{_sbindir}/lvm_import_vdo

# Other files
%{_sbindir}/lvchange
%{_sbindir}/lvconvert
%{_sbindir}/lvcreate
%{_sbindir}/lvdisplay
%{_sbindir}/lvextend
%{_sbindir}/lvmdiskscan
%{_sbindir}/lvmsadc
%{_sbindir}/lvmsar
%{_sbindir}/lvreduce
%{_sbindir}/lvremove
%{_sbindir}/lvrename
%{_sbindir}/lvresize
%{_sbindir}/lvs
%{_sbindir}/lvscan
%{_sbindir}/pvchange
%{_sbindir}/pvck
%{_sbindir}/pvcreate
%{_sbindir}/pvdisplay
%{_sbindir}/pvmove
%{_sbindir}/pvremove
%{_sbindir}/pvresize
%{_sbindir}/pvs
%{_sbindir}/pvscan
%{_sbindir}/vgcfgbackup
%{_sbindir}/vgcfgrestore
%{_sbindir}/vgchange
%{_sbindir}/vgck
%{_sbindir}/vgconvert
%{_sbindir}/vgcreate
%{_sbindir}/vgdisplay
%{_sbindir}/vgexport
%{_sbindir}/vgextend
%{_sbindir}/vgimport
%{_sbindir}/vgimportclone
%{_sbindir}/vgimportdevices
%{_sbindir}/vgmerge
%{_sbindir}/vgmknodes
%{_sbindir}/vgreduce
%{_sbindir}/vgremove
%{_sbindir}/vgrename
%{_sbindir}/vgs
%{_sbindir}/vgscan
%{_sbindir}/vgsplit
%attr(755, -, -) %{_libexecdir}/lvresize_fs_helper
%{_mandir}/man5/lvm.conf.5.gz
%{_mandir}/man7/lvmautoactivation.7.gz
%{_mandir}/man7/lvmcache.7.gz
%{_mandir}/man7/lvmraid.7.gz
%{_mandir}/man7/lvmreport.7.gz
%{_mandir}/man7/lvmthin.7.gz
%{_mandir}/man7/lvmvdo.7.gz
%{_mandir}/man7/lvmsystemid.7.gz
%{_mandir}/man8/fsadm.8.gz
%{_mandir}/man8/lvchange.8.gz
%{_mandir}/man8/lvconvert.8.gz
%{_mandir}/man8/lvcreate.8.gz
%{_mandir}/man8/lvdisplay.8.gz
%{_mandir}/man8/lvextend.8.gz
%{_mandir}/man8/lvm.8.gz
%{_mandir}/man8/lvm-config.8.gz
%{_mandir}/man8/lvm-dumpconfig.8.gz
%{_mandir}/man8/lvm-fullreport.8.gz
%{_mandir}/man8/lvmconfig.8.gz
%{_mandir}/man8/lvmdevices.8.gz
%{_mandir}/man8/lvmdiskscan.8.gz
%{_mandir}/man8/lvmdump.8.gz
%{_mandir}/man8/lvmpersist.8.gz
%{_mandir}/man8/lvmsadc.8.gz
%{_mandir}/man8/lvmsar.8.gz
%{_mandir}/man8/lvreduce.8.gz
%{_mandir}/man8/lvremove.8.gz
%{_mandir}/man8/lvrename.8.gz
%{_mandir}/man8/lvresize.8.gz
%{_mandir}/man8/lvs.8.gz
%{_mandir}/man8/lvscan.8.gz
%{_mandir}/man8/pvchange.8.gz
%{_mandir}/man8/pvck.8.gz
%{_mandir}/man8/pvcreate.8.gz
%{_mandir}/man8/pvdisplay.8.gz
%{_mandir}/man8/pvmove.8.gz
%{_mandir}/man8/pvremove.8.gz
%{_mandir}/man8/pvresize.8.gz
%{_mandir}/man8/pvs.8.gz
%{_mandir}/man8/pvscan.8.gz
%{_mandir}/man8/lvm_import_vdo.8.gz
%{_mandir}/man8/vgcfgbackup.8.gz
%{_mandir}/man8/vgcfgrestore.8.gz
%{_mandir}/man8/vgchange.8.gz
%{_mandir}/man8/vgck.8.gz
%{_mandir}/man8/vgconvert.8.gz
%{_mandir}/man8/vgcreate.8.gz
%{_mandir}/man8/vgdisplay.8.gz
%{_mandir}/man8/vgexport.8.gz
%{_mandir}/man8/vgextend.8.gz
%{_mandir}/man8/vgimport.8.gz
%{_mandir}/man8/vgimportclone.8.gz
%{_mandir}/man8/vgimportdevices.8.gz
%{_mandir}/man8/vgmerge.8.gz
%{_mandir}/man8/vgmknodes.8.gz
%{_mandir}/man8/vgreduce.8.gz
%{_mandir}/man8/vgremove.8.gz
%{_mandir}/man8/vgrename.8.gz
%{_mandir}/man8/vgs.8.gz
%{_mandir}/man8/vgscan.8.gz
%{_mandir}/man8/vgsplit.8.gz
%{_udevdir}/11-dm-lvm.rules
%{_udevdir}/69-dm-lvm.rules
%if %{enable_lvmpolld}
%{_mandir}/man8/lvmpolld.8.gz
%{_mandir}/man8/lvm-lvpoll.8.gz
%endif
%dir %{_sysconfdir}/lvm
%ghost %{_sysconfdir}/lvm/cache/.cache
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvm.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lvm/lvmlocal.conf
%dir %{_sysconfdir}/lvm/profile
%{_sysconfdir}/lvm/profile/command_profile_template.profile
%{_sysconfdir}/lvm/profile/metadata_profile_template.profile
%{_sysconfdir}/lvm/profile/thin-generic.profile
%{_sysconfdir}/lvm/profile/thin-performance.profile
%{_sysconfdir}/lvm/profile/cache-mq.profile
%{_sysconfdir}/lvm/profile/cache-smq.profile
%{_sysconfdir}/lvm/profile/lvmdbusd.profile
%if %{enable_vdo}
%{_sysconfdir}/lvm/profile/vdo-small.profile
%endif
%dir %{_sysconfdir}/lvm/backup
%dir %{_sysconfdir}/lvm/cache
%dir %{_sysconfdir}/lvm/archive
%dir %{_sysconfdir}/lvm/devices
%dir %{_default_locking_dir}
%dir %{_default_run_dir}
%{_tmpfilesdir}/%{name}.conf
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-monitor.service
#%%{_unitdir}/lvm-vgchange@.service # vgchange is now part of udev rule
%if %{enable_lvmpolld}
%{_unitdir}/lvm2-lvmpolld.socket
%{_unitdir}/lvm2-lvmpolld.service
%endif
%{_unitdir}/lvm-devices-import.service
%{_unitdir}/lvm-devices-import.path

##############################################################################
# Library and Development subpackages
##############################################################################
%package devel
Summary: Development libraries and headers
License: LGPL-2.1-only
Requires: %{name} = %{?epoch}:%{version}-%{release}
Requires: device-mapper-devel = %{?epoch}:%{device_mapper_version}-%{release}
Requires: device-mapper-event-devel = %{?epoch}:%{device_mapper_version}-%{release}
Requires: pkgconfig

%description devel
This package contains files needed to develop applications that use
the lvm2 libraries.

%files devel
%{_libdir}/liblvm2cmd.so
%{_libdir}/libdevmapper-event-lvm2.so
%{_includedir}/lvm2cmd.h

%package libs
Summary: Shared libraries for lvm2
License: LGPL-2.1-only
Requires: device-mapper-event = %{?epoch}:%{device_mapper_version}-%{release}

%description libs
This package contains shared lvm2 libraries for applications.

%ldconfig_scriptlets libs

%files libs
%license COPYING.LIB
%{_libdir}/liblvm2cmd.so.*
%{_libdir}/libdevmapper-event-lvm2.so.*
%dir %{_libdir}/device-mapper
%{_libdir}/device-mapper/libdevmapper-event-lvm2mirror.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2snapshot.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2raid.so
%{_libdir}/libdevmapper-event-lvm2mirror.so
%{_libdir}/libdevmapper-event-lvm2snapshot.so
%{_libdir}/libdevmapper-event-lvm2raid.so

%if %{enable_thin}
%{_libdir}/libdevmapper-event-lvm2thin.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2thin.so
%endif

%{_libdir}/libdevmapper-event-lvm2vdo.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2vdo.so

##############################################################################
# LVM locking daemon
##############################################################################
%if %{enable_lockd_dlm} || %{enable_lockd_sanlock}
%package lockd
Summary: LVM locking daemon
Requires: lvm2 = %{?epoch}:%{version}-%{release}
%if %{enable_lockd_sanlock}
Requires: sanlock-lib >= %{sanlock_version}
%endif
%if %{enable_lockd_dlm}
Requires: dlm-lib >= %{dlm_version}
%endif
Requires(post): systemd-units >= %{systemd_version}
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

%description lockd

LVM commands use lvmlockd to coordinate access to shared storage.

%post lockd
%systemd_post lvmlockd.service lvmlocks.service

%preun lockd
%systemd_preun lvmlockd.service lvmlocks.service

%postun lockd
%systemd_postun lvmlockd.service lvmlocks.service

%files lockd
%{_sbindir}/lvmlockd
%{_sbindir}/lvmlockctl
%{_mandir}/man8/lvmlockd.8.gz
%{_mandir}/man8/lvmlockctl.8.gz
%{_unitdir}/lvmlockd.service
%{_unitdir}/lvmlocks.service

%endif

##############################################################################
# LVM D-Bus daemon
##############################################################################
%if %{enable_lvmdbusd}

%package dbusd
Summary: LVM2 D-Bus daemon
License: GPL-2.0-only
BuildArch: noarch
Requires: lvm2 >= %{?epoch}:%{version}-%{release}
Requires: dbus
Requires: python3-dbus
Requires: python3-pyudev
Requires: python3-gobject-base
Requires(post): systemd-units >= %{systemd_version}
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

%description dbusd

Daemon for access to LVM2 functionality through a D-Bus interface.

%post dbusd
%systemd_post lvm2-lvmdbusd.service

%preun dbusd
%systemd_preun lvm2-lvmdbusd.service

%postun dbusd
%systemd_postun lvm2-lvmdbusd.service

%files dbusd
%{_sbindir}/lvmdbusd
%{_sysconfdir}/dbus-1/system.d/com.redhat.lvmdbus1.conf
%{_datadir}/dbus-1/system-services/com.redhat.lvmdbus1.service
%{_mandir}/man8/lvmdbusd.8.gz
%{_unitdir}/lvm2-lvmdbusd.service
%{python3_sitelib}/lvmdbusd

%endif

##############################################################################
# Device-mapper subpackages
##############################################################################
%package -n device-mapper
Summary: Device mapper utility
Version: %{device_mapper_version}
License: GPL-2.0-only
URL: https://www.sourceware.org/dm/
Requires: device-mapper-libs = %{?epoch}:%{device_mapper_version}-%{release}
Requires: util-linux-core >= %{util_linux_version}
Requires: systemd >= %{systemd_version}
# We need dracut to install required udev rules if udev_sync
# feature is turned on so we don't lose required notifications.
Conflicts: dracut < %{dracut_version}

%description -n device-mapper
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%files -n device-mapper
%license COPYING COPYING.LIB
%doc WHATS_NEW_DM VERSION_DM README
%doc udev/12-dm-permissions.rules
%{_sbindir}/dmsetup
%{_sbindir}/blkdeactivate
%{_sbindir}/dmstats
%{_mandir}/man8/dmsetup.8.gz
%{_mandir}/man8/dmstats.8.gz
%{_mandir}/man8/blkdeactivate.8.gz
%if %{enable_dmfilemapd}
%{_sbindir}/dmfilemapd
%{_mandir}/man8/dmfilemapd.8.gz
%endif
%{_udevdir}/10-dm.rules
%{_udevdir}/13-dm-disk.rules
%{_udevdir}/95-dm-notify.rules

%package -n device-mapper-devel
Summary: Development libraries and headers for device-mapper
Version: %{device_mapper_version}
License: LGPL-2.1-only
Requires: device-mapper = %{?epoch}:%{device_mapper_version}-%{release}
Requires: pkgconfig

%description -n device-mapper-devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%files -n device-mapper-devel
%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%package -n device-mapper-libs
Summary: Device-mapper shared library
Version: %{device_mapper_version}
License: LGPL-2.1-only
Requires: device-mapper = %{?epoch}:%{device_mapper_version}-%{release}

%description -n device-mapper-libs
This package contains the device-mapper shared library, libdevmapper.

%ldconfig_scriptlets -n device-mapper-libs

%files -n device-mapper-libs
%license COPYING COPYING.LIB
%{_libdir}/libdevmapper.so.*

%package -n device-mapper-event
Summary: Device-mapper event daemon
Version: %{device_mapper_version}
Requires: device-mapper = %{?epoch}:%{device_mapper_version}-%{release}
Requires: device-mapper-event-libs = %{?epoch}:%{device_mapper_version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n device-mapper-event
This package contains the dmeventd daemon for monitoring the state
of device-mapper devices.

%post -n device-mapper-event
%systemd_post dm-event.socket
# dm-event.socket is always enabled and started and ready to serve if dmeventd is used
# replace direct systemctl calls with systemd rpm macro once this is provided in the macro:
# http://cgit.freedesktop.org/systemd/systemd/commit/?id=57ab2eabb8f92fad5239c7d4492e9c6e23ee0678
systemctl enable dm-event.socket
systemctl start dm-event.socket >/dev/null 2>&1 || :
if [ -e %{_default_pid_dir}/dmeventd.pid ]; then
	%{_sbindir}/dmeventd -R || echo "Failed to restart dmeventd daemon. Please, try manual restart."
fi

%preun -n device-mapper-event
%systemd_preun dm-event.service dm-event.socket

%files -n device-mapper-event
%{_sbindir}/dmeventd
%{_mandir}/man8/dmeventd.8.gz
%{_unitdir}/dm-event.socket
%{_unitdir}/dm-event.service

%package -n device-mapper-event-libs
Summary: Device-mapper event daemon shared library
Version: %{device_mapper_version}
License: LGPL-2.1-only

%description -n device-mapper-event-libs
This package contains the device-mapper event daemon shared library,
libdevmapper-event.

%ldconfig_scriptlets -n device-mapper-event-libs

%files -n device-mapper-event-libs
%license COPYING.LIB
%{_libdir}/libdevmapper-event.so.*

%package -n device-mapper-event-devel
Summary: Development libraries and headers for the device-mapper event daemon
Version: %{device_mapper_version}
License: LGPL-2.1-only
Requires: device-mapper-event = %{?epoch}:%{device_mapper_version}-%{release}
Requires: pkgconfig

%description -n device-mapper-event-devel
This package contains files needed to develop applications that use
the device-mapper event library.

%files -n device-mapper-event-devel
%{_libdir}/libdevmapper-event.so
%{_includedir}/libdevmapper-event.h
%{_libdir}/pkgconfig/devmapper-event.pc

##############################################################################
# Testsuite
##############################################################################
%if %{enable_testsuite}
%package testsuite
Summary: LVM2 Testsuite
# Most of the code is GPLv2, the harness in test/lib/{brick-shelltest.h,runner.cpp} is BSD, and C files in test/api are LGPLv2...
License: GPL-2.0-only AND LGPL-2.1-only AND BSD-2-Clause

%description testsuite
An extensive functional testsuite for LVM2.

%files testsuite
%license COPYING COPYING.LIB COPYING.BSD
%{_datadir}/lvm2-testsuite/
%{_libexecdir}/lvm2-testsuite/
%{_bindir}/lvm2-testsuite
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.03.34-3
- test: add initial lock files

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.03.34-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 30 2025 Marian Csontos <mcsontos@redhat.com> - 2.03.34-1
- New upstream release v2.03.34

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Marian Csontos <mcsontos@redhat.com> - 2.03.33-1
- New upstream release v2.03.33

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.03.32-2
- Rebuilt for Python 3.14

* Mon May 05 2025 Marian Csontos <mcsontos@redhat.com> - 2.03.32-1
- New upstream release v2.03.32

* Thu Feb 27 2025 Marian Csontos <mcsontos@redhat.com> - 2.03.31-1
- New upstream release v2.03.31

* Fri Jan 31 2025 Marian Csontos <mcsontos@redhat.com> - 2.03.30-4
- [WIP] Use autochangelog

* Fri Jan 31 2025 Marian Csontos <mcsontos@redhat.com> - 2.03.30-3
- Fix race causing lvm2 does not recognize active devices

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Marian Csontos <mcsontos@redhat.com> - 2.03.30-1
- New upstream release v2.03.30

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.03.29-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Mon Dec 09 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.29-1
- New upstream release v2.03.29

* Sun Oct 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.03.27-2
- Disable DLM on RHEL 10 and later

* Wed Oct 02 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.27-1
- New upstream release v2.03.27

* Fri Aug 23 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.26-1
- New upstream release v2.03.26

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 13 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.03.25-3
- Rebuilt for the bin-sbin merge (again)

* Fri Jul 12 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.25-2
- Fix DM version

* Fri Jul 12 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.25-1
- New upstream release v2.03.25

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.03.24-4
- Add compat sbin Provides

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.03.24-3
- Rebuilt for Python 3.13

* Wed May 22 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.24-2
- Allow system.devices to be automatically created on first boot

* Thu May 16 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.24-1
- New upstream release v2.03.24

* Mon Feb 12 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.23-2
- Update License fields to SPDX

* Wed Jan 24 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.23-1
- New upstream release v2.03.23

* Wed Jan 24 2024 Marian Csontos <mcsontos@redhat.com> - 2.03.22-3
- Update spec file

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 Marian Csontos <mcsontos@redhat.com> - 2.03.22-1
- New upstream release v2.03.22

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Adam Williamson <awilliam@redhat.com> - 2.03.21-4
- Backport PR #121 to fix build with Python 3.12

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 2.03.21-3
- Rebuilt for Python 3.12

* Sun May 21 2023 Todd Zullinger <tmz@pobox.com> - 2.03.21-2
- Avoid unowned %%%%{python3_sitelib}/lvmdbusd directory

* Fri Apr 21 2023 Marian Csontos <mcsontos@redhat.com> - 2.03.21-1
- New upstream release v2.03.21

* Tue Apr 04 2023 Marian Csontos <mcsontos@redhat.com> - 2.03.20-3
- Fix segfault in lvmdbusd on s390x

* Wed Mar 22 2023 Adam Williamson <awilliam@redhat.com> - 2.03.20-2
- Backport PR #114 to fix #2180557

* Tue Mar 21 2023 Marian Csontos <mcsontos@redhat.com> - 2.03.20-1
- New upstream release v2.03.20

* Wed Mar 08 2023 Marian Csontos <mcsontos@redhat.com> - 2.03.19-2
- Fix a segfault when using -S|--select

* Tue Feb 21 2023 Marian Csontos <mcsontos@redhat.com> - 2.03.19-1
- New upstream release v2.03.19

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Marian Csontos <mcsontos@redhat.com> - 2.03.18-1
- New upstream release v2.03.18

* Thu Dec 01 2022 Marian Csontos <mcsontos@redhat.com> - 2.03.17-3
- Fix syntax

* Wed Nov 30 2022 Marian Csontos <mcsontos@redhat.com> - 2.03.17-2
- Fix permissions on lvresize_fs_helper

* Wed Nov 16 2022 Marian Csontos <mcsontos@redhat.com> - 2.03.17-1
- New upstream release v2.03.17

* Mon Sep 26 2022 Marian Csontos <mcsontos@redhat.com> - 2.03.16-2
- Update sources

* Mon Sep 26 2022 Marian Csontos <mcsontos@redhat.com> - 2.03.16-1
- New upstream release v2.03.16

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.11-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.03.11-12
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.11-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 09 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.03.11-10
- Require util-linux-core instead of util-linux

* Thu Sep 09 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.03.11-9
- Use a "rich dependency" for the system-release req

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.03.11-7
- Rebuilt for Python 3.10

* Mon Mar 22 2021 Marian Csontos <mcsontos@redhat.com> - 2.03.11-6
- Fix editline compilation

* Tue Mar 16 2021 Marian Csontos <mcsontos@redhat.com> - 2.03.11-5
- Replace readline by editline

* Tue Mar 16 2021 Marian Csontos <mcsontos@redhat.com> - 2.03.11-4
- Fix conditionals

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.03.11-3
- Rebuilt for updated systemd-rpm-macros

* Thu Feb 25 2021 Marian Csontos <mcsontos@redhat.com> - 2.03.11-2
- Merge remote-tracking branch 'fedora_robert/cleanup' into main

* Mon Feb 22 2021 Marian Csontos <mcsontos@redhat.com> - 2.03.11-1
- New upstream release v2.03.11

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Tom Stellard <tstellar@redhat.com> - 2.03.10-2
- Add BuildRequires: make

* Sun Aug 09 2020 Marian Csontos <mcsontos@redhat.com> - 2.03.10-1
- New upstream release v2.03.10

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.03.09-3
- Use make macros

* Tue May 26 2020 Miro Hrončok <miro@hroncok.cz> - 2.03.09-2
- Rebuilt for Python 3.9

* Thu Mar 26 2020 Marian Csontos <mcsontos@redhat.com> - 2.03.09-1
- New upstream release v2.03.09

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.07-1
- New upstream release v2.03.07

* Wed Oct 23 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.06-1
- New upstream release v2.03.06

* Wed Sep 18 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.05-5
- Fix invalid value warning in 11-dm-lvm.rules:40

* Tue Aug 27 2019 Adam Williamson <awilliam@redhat.com> - 2.03.05-4
- Backport fix for converting dbus.UInt to string in Python 3.8

* Mon Aug 19 2019 Miro Hrončok <miro@hroncok.cz> - 2.03.05-3
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.05-2
- Disable dlmcontrol until dlm is updated

* Wed Jul 31 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.05-1
- New upstream release v2.03.05

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.185-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Marian Csontos <mcsontos@redhat.com> - 2.02.185-1
- New upstream release v2.02.185

* Mon Apr 01 2019 Marian Csontos <mcsontos@redhat.com> - 2.02.184-1
- New upstream release v2.02.184

* Thu Mar 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-6
- Remove obsolete scriptlets

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-5
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.183-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-3
- Remove obsolete Group tag

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-2
- Remove obsolete ldconfig scriptlets

* Fri Dec 07 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.183-1
- New upstream release v2.02.183

* Wed Oct 31 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.182-1
- New upstream release v2.02.182

* Tue Oct 02 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.181-2
- No %%ghost for dirs at tmpfiles.d

* Thu Aug 02 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.181-1
- New upstream release v2.02.181

* Thu Jul 19 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.180-1
- New upstream release v2.02.180

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.179-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-6
- Really bump release number

* Tue Jul 10 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-5
- Bump release number

* Tue Jul 10 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-4
- Remove python bindings

* Tue Jul 10 2018 Jason Tibbitts <tibbs@math.uh.edu> - 2.02.179-3
- Remove needless use of %%defattr

* Tue Jun 19 2018 Miro Hrončok <miro@hroncok.cz> - 2.02.179-2
- Rebuilt for Python 3.7

* Mon Jun 18 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-1
- New upstream release v2.02.179

* Wed Jun 13 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-5
- New upstream release v2.02.178

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-4
- Hide output of systemctl calls

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-3
- Fix commented out python_provide

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-2
- Forgot to run new-sources etc

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-1
- New upstream release v2.02.178-rc1

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.177-8
- Address Bug 1552971

* Wed Apr 04 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.177-7
- Remove python2 bindings

* Mon Mar 05 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.177-6
- Add gcc and gcc-c++ to BuildRequires

* Wed Feb 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.177-5
- Remove %%clean section

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.177-4
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.177-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 2.02.177-2
- Update Python 2 dependency declarations to new packaging standards

* Tue Dec 19 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.177-1
- New upstream release v2.02.177

* Thu Dec 14 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.176-3
- Add and enable testsuite subpackage
- Escape percent signs in changelog

* Tue Dec 12 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.176-2
- Add epoch for easier downstream (el) rebuild.

* Fri Nov 03 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.176-1
- New upstream release v2.02.176

* Mon Oct 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.175-1
- New upstream release v2.02.175
- Fix D-Bus spelling, uncomment python_provide

* Mon Oct 02 2017 Troy Dawson <tdawson@redhat.com> - 2.02.174-2
- Bump to rebuild on rebuilt corosync

* Wed Sep 20 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.174-1
- New upstream release v2.02.174

* Wed Sep 06 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.173-5
- [WIP] Fix python subpackage names to follow guidelines

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.173-4
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.02.173-3
- Rebuild with fixed binutils for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.173-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.173-1
- New upstream release v2.02.173.

* Thu Jun 29 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.172-1
- New upstream release v2.02.172.

* Fri Jun 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-5
- Fix changelog

* Fri Jun 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-4
- Add patch for lvmdbusd

* Wed May 17 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-3
- Add patch for lvmdbusd

* Tue May 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-2
- Fix permissions on license files

* Tue May 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-1
- New upstream release v2.02.171.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.168-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.02.168-3
- Rebuild for readline 7.x

* Mon Dec 19 2016 Miro Hrončok <miro@hroncok.cz> - 2.02.168-2
- Rebuild for Python 3.6

* Thu Dec 01 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.168-1
- New upstream release v2.02.168.

* Mon Nov 21 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-4
- Fix typo in lvm2 package description.

* Tue Nov 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-3
- Only log msg as debug if lvm2-lvmdbusd unit missing for D-Bus
  notification.

* Mon Nov 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-2
- New upstream release v2.02.167.

* Mon Nov 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-1
- New upstream release v2.02.167.

* Thu Oct 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.166-2
- Add various fixes for lvmdbusd from upcoming lvm2 version 2.02.167.

* Mon Sep 26 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.166-1
- New upstream release v2.02.166.

* Wed Sep 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.165-2
- Add new lvmraid.7 man page to lvm2 package

* Wed Sep 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.165-1
- New upstream release v2.02.165.

* Mon Aug 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.164-2
- Fix date in changelog

* Mon Aug 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.164-1
- New upstream release v2.02.164.

* Wed Aug 10 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.163-1
- New upstream release v2.02.163.

* Fri Jul 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.162-1
- New upstream release v2.02.162.

* Thu Jul 21 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.161-3
- Enable LVM notifications over dbus for lvmdbusd.

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.161-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Mon Jul 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.161-1
- New upstream release v2.02.161.

* Thu Jul 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.160-1
- New upstream release v2.02.160.

* Thu Jul 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.159-1
- New upstream release v2.02.159.

* Tue Jun 28 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.158-1
- New upstream release v2.02.158.

* Fri Jun 17 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.157-1
- New upstream release v2.02.157.

* Mon Jun 13 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.156-1
- New upstream release v2.02.156.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-4
- Fix regression in blkdeactivate script.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-3
- Fix regression in blkdeactivate script.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-2
- Fix regression in blkdeactivate script.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-1
- New upstream release v2.02.155.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.154-2
- New upstream release v2.02.155.

* Mon May 16 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.154-1
- New upstream release v2.02.154.

* Tue May 10 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.153-1
- New upstream release v2.02.153.

* Mon May 02 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.152-1
- New upstream release v2.02.152.

* Mon Apr 25 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.151-1
- New upstream release v2.02.151.

* Mon Apr 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.150-1
- New upstream release v2.02.150.

* Mon Apr 04 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.149-3
- New upstream release v2.02.149.

* Mon Apr 04 2016 Peter Rajnoha <prajnoha@redhat.com>
- New upstream release v2.02.149.

* Tue Mar 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.148-1
- New upstream release v2.02.148.

* Mon Mar 21 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.147-1
- New upstream release v2.02.147.

* Fri Mar 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.146-2
- New upstream release v2.02.146.

* Fri Mar 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.146-1
- New upstream release v2.02.146.

* Wed Mar 09 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.145-2
- Require python3-gobject-base insetad of python3-gobject.

* Mon Mar 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.145-1
- New upstream release v2.02.145.

* Mon Feb 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.144-3
- Remove unneded patch.

* Mon Feb 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.144-2
- Require newer version of sanlock.

* Mon Feb 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.144-1
- New upstream release v2.02.144.

* Wed Feb 24 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-6
- Reinstate lvm2-lockd on all architectures as sanlock package is fixed
  now.

* Tue Feb 23 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-5
- Remove Requires: sanlock-lib for lvm2-lockd subpackage if sanlock not
  compiled.

* Tue Feb 23 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-4
- Build lvm2-lockd with sanlock support only on x86_64, arch64 and power64
  arch.

* Tue Feb 23 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-3
- Add Requires: python3-gobject for lvm2-dbusd subpackage.

* Mon Feb 22 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-2
- Patch lvm2 v2.02.143 Makefile for lvmdbusd.

* Mon Feb 22 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-1
- New upstream release v2.02.143 introducing LVM D-Bus daemon.

* Mon Feb 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.142-1
- New upstream release v2.02.142.

* Thu Feb 04 2016 Dennis Gilmore <dennis@ausil.us> - 2.02.141-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.141-1
- New upstream release v2.02.141.

* Mon Jan 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.140-2
- New upstream release v2.02.140.

* Mon Jan 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.140-1
- New upstream release v2.02.140.

* Mon Jan 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.139-1
- New upstream release v2.02.139.

* Mon Jan 04 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.138-1
- New upstream release v2.02.138.

* Mon Dec 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.137-1
- New upstream release v2.02.137.

* Wed Dec 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.136-1
- New upstream release v2.02.136.

* Mon Nov 23 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.135-1
- New upstream release v2.02.135.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-5
- Changelog.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-4
- Changelog.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-3
- Bump version because of device-mapper not having a new release.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-2
- Bump version because of device-mapper not having a new release.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-1
- New upstream release v2.02.134.

* Tue Nov 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 2.02.133-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.133-2
- Shutdown lvmetad automatically after one hour of inactivity

* Fri Oct 30 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.133-1
- New upstream release v2.02.133.

* Mon Oct 26 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.132-2
- Remove %%epoch from cmirror package.

* Wed Sep 23 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.132-1
- New upstream release v2.02.132.

* Wed Sep 16 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.131-1
- New upstream release v2.02.131.

* Mon Sep 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.130-1
- New upstream release v2.02.130.

* Wed Sep 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.129-2
- Reinstate dm_task_get_info@Base to libdevmapper exports. (1.02.106)

* Thu Aug 27 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.129-1
- New upstream release v2.02.129.

* Tue Aug 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.128-2
- Pack cache-mq and cache-smq configuration profiles that appearead in
  v128.

* Tue Aug 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.128-1
- New upstream release v2.02.128.

* Mon Aug 10 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.127-1
- New upstream release v2.02.127.

* Mon Jul 27 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.126-2
- New upstream release v2.02.126.

* Mon Jul 27 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.126-1
- New upstream release v2.02.126.

* Tue Jul 14 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.125-2
- Remove Requires: fedora-release dependency, use system-release instead.

* Tue Jul 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.125-1
- New upstream release v2.02.125.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.124-3
- Remove extra tgz file that is uploaded already.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.124-2
- New upstream release v2.02.124.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.124-1
- New upstream release v2.02.124.

* Wed Jul 01 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.123-1
- New upstream release v2.02.123.

* Mon Jun 22 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.122-1
- New upstream release v2.02.122.

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 2.02.120-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.120-2
- New upstream lvm2 release v2.02.120.

* Mon May 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.120-1
- New upstream lvm2 release v2.02.120.

* Mon May 04 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.119-2
- New upstream release v2.02.119.

* Mon May 04 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.119-1
- New upstream release v2.02.119.

* Tue Mar 24 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.118-2
- Update to latest upstream lvm2 release version 2.02.118.

* Tue Mar 24 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.118-1
- Update to latest upstream lvm2 release version 2.02.118.

* Fri Jan 30 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.116-1
- New upstream release.

* Thu Jan 29 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.115-2
- Fixes: use default cache mode when unset and add BuildRequires: device-
  mapper-persistent-data.

* Thu Jan 22 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.115-1
- New upstream release with various fixes and enhancements.

* Fri Nov 28 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.114-1
- New upstream with fixes.

* Thu Nov 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.113-3
- Changelog.

* Thu Nov 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.113-2
- Add some fixes from upcoming lvm2 v2.02.114.

* Tue Nov 25 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.113-1
- New upstream bugfix release.

* Wed Nov 12 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.112-3
- Still the date in changelog.

* Wed Nov 12 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.112-2
- Fix date in changelog.

* Tue Nov 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.112-1
- Update to latest lvm2 upstream release v2.02.112.

* Mon Sep 01 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.111-1
- Update to latest lvm2 upstream release 2.02.111.

* Wed Aug 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.110-1
- New upstream release - lvm2 v2.02.110.

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 2.02.109-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.109-1
- Update to lvm2 upstream bug fix release 2.02.109.

* Fri Jul 25 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.108-1
- Merge branch 'master' into f21

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.02.107-2
- fix license handling

* Tue Jun 24 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.107-1
- Update to latest lvm2 upstream release v2.02.107.

* Mon Jun 09 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.106-6
- Fix spec file after mass rebuild script broke subpackage release tags.

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 2.02.106-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-4
- Remove obsolete lvm2-sysvinit subpackage.

* Thu Apr 24 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-3
- Always require the exact version for all LVM2 subpackages so all of them
  are synchronously updated.

* Fri Apr 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-2
- Update 'upstream' file.

* Fri Apr 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-1
- Update to latest upstream release lvm v2.02.106.

* Mon Jan 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-3
- Avoid exposing temporary devices when initializing thin pool volume.

* Mon Jan 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-2
- Remove handling of specific inappropriate mpath and cryptsetup events.

* Tue Jan 21 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-1
- New upstream release (v2.02.105).

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.02.104-4
- Drop INSTALL from docs, escape percents in %%changelog.

* Fri Dec 13 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-3
- Require lvm2 pkg for lvm2-python-libs.

* Wed Dec 11 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-2
- Additional fix for SYSTEMD_READY env var assignment in lvmetad udev
  rules.

* Thu Nov 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-1
- New upstream release (v2.02.104).

* Wed Oct 30 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-7
- Additional fixes from upcoming v104 (related to udev).

* Fri Oct 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-6
- Fix changelog date.

* Fri Oct 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-5
- Additional fixes from upcoming v104.

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-4
- Add thin-performance.profile to lvm2 package.

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-3
- Modify patch that enables lvmetad for it to be applicable again (the
  lvm.conf context changed).

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-2
- Remove unused patch.

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-1
- New upstream release (v2.02.103).

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-5
- Add one more patch.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-4
- Update Source0 address.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-3
- Also increase device-mapper version.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-2
- A few more edits for lvm2 v2.02.102.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-1
- New upstream release (lvm2 v2.02.102).

* Tue Aug 06 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-4
- Fix MDA offset/size overflow while using lvmetad and some spec file
  changes.

* Tue Jul 30 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-3
- Fix spec files %%define util-linux_version -> %%define util_linux_version
  for proper expansion

* Thu Jul 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-2
- remove items from changelog for patches already attached in previous
  builds as part of v2.02.98

* Thu Jul 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-1
- New upstream release (2.02.99)

* Thu May 30 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-16
- Do not include /lib/udev and /lib/udev/rules.d in device-mapper package.

* Tue May 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-15
- Additional lvmetad fixes.

* Tue May 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-14
- Add various fixes from upcoming lvm2 upstream release.

* Fri May 03 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-13
- Fix non-functional autoactivation of LVM volumes on top of MD devices.

* Fri Apr 19 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-12
- Autoactivate VG/LV on coldplug of DM-based PVs at boot.

* Tue Apr 09 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-11
- Additional fixes for autoactivation feature.

* Thu Feb 14 2013 Dennis Gilmore <dennis@ausil.us> - 2.02.98-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-9
- Skip mlocking [vectors] on arm architecture.

* Sat Nov 17 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-8
- Exit pvscan --cache immediately if cluster locking used or lvmetad not
  used.

* Mon Nov 05 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-7
- Handle blank configure_cmirror and configure_cluster.

* Fri Nov 02 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-6
- Amendment to lvm2-2_02_99-various-updates-and-fixes-for-systemd-
  units.patch.

* Thu Nov 01 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-5
- lvmetad enabled by default, add lvm2-activation-generator and related
  fixes
- Add lvm2-activation-generator systemd generator to automatically systemd
  units to activate LVM2 volumes even if lvmetad is not This replaces lvm
  activation part of the former fedora-storage-init script that was
  included in the initscripts package before.
- Enable lvmetad - the LVM metadata daemon by default.
- Don't use lvmetad in lvm2-monitor.service ExecStop to avoid a systemd
  issue.
- Remove dependency on fedora-storage-init.service in lvm2 systemd units.
- Depend on lvm2-lvmetad.socket in lvm2-monitor.service systemd unit.
- Init lvmetad lazily to avoid early socket access on config overrides.
- Hardcode use_lvmetad=0 if cluster locking used and issue a warning  msg.
- Fix dm_task_set_cookie to properly process udev flags if udev_sync
  disabled.

* Sat Oct 20 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-4
- lvm2_spec.patch not needed

* Sat Oct 20 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-3
- Incorporate python-lvm pkg as lvm2-python-libs subpkg.

* Wed Oct 17 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-2
- Fix changelog header.

* Tue Oct 16 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-1
- New upstream release and spec file cleanup.

* Tue Aug 07 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.97-4
- tmpfiles.d isn't a config file when in lib

* Tue Aug 07 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.97-3
- another attempt to fix tmpfiles lib dir

* Tue Aug 07 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.97-2
- moved tmpfiles.d from etc to lib

* Tue Aug 07 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.97-1
- New upstream with bug fixes and improved thin support.

* Thu Jul 19 2012 Dennis Gilmore <dennis@ausil.us> - 2.02.96-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.96-5
- Further spec file cleanups.

* Wed Jul 04 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.96-4
- Fix spec file conditional for non-rawhide releases.

* Tue Jul 03 2012 Peter Rajnoha <prajnoha@redhat.com>
- Remove unused 'configure_default_data_alignment'.

* Mon Jul 02 2012 Peter Rajnoha <prajnoha@redhat.com>
- Clean up spec file, compile in lvmetad, autoactivation.

* Mon Jun 18 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.96-1
- New upstream, using device-mapper-persistent-data.

* Thu Jun 07 2012 Kay Sievers <kay@vrfy.org> - 2.02.95-26
- Remove Requires: libudev

* Tue Jun 05 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-25
- Use BuildRequires: systemd-devel instead of libudev-devel.

* Wed Apr 11 2012 Milan Broz <mbroz@redhat.com> - 2.02.95-24
- Build cluster only on x86_64 and i686 on RHEL.

* Thu Mar 29 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.95-23
- BuildRequires and Requires on newer version of corosync and dlm. -
  Restart clvmd on upgrades.

* Wed Mar 28 2012 Milan Broz <mbroz@redhat.com> - 2.02.95-22
- Restart clvmd on update.

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-21
- Do not strictly require openais for cmirror subpackage.

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-20
- Add F17 specific configure options (different corosync version).

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-19
- Reinstate cmirror support and fixes for lvmetad udev rules/init scripts.

* Fri Mar 16 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.95-18
- Rebuild against new version of corosync (soname change) Bump Requires and
  BuildRequires on new corosync

* Fri Mar 09 2012 Milan Broz <mbroz@redhat.com> - 2.02.95-17
- Fix spec for non-cluster architectures.

* Thu Mar 08 2012 Peter Rajnoha <prajnoha@redhat.com>
- Reload dm-event systemd service on upgrade.

* Tue Mar 06 2012 Alasdair G Kergon <agk@redhat.com>
- New upstream with minor thinprov and name mangling fixes.

* Mon Mar 05 2012 Peter Rajnoha <prajnoha@redhat.com>
- Prepare hooks for lvmetad support.

* Sat Mar 03 2012 Alasdair G Kergon <agk@redhat.com>
- New upstream with many small fixes, some thin provisioning improvements
  and preparations for the new metadata daemon.

* Thu Feb 23 2012 Alasdair G Kergon <agk@redhat.com>
- fix build

* Thu Feb 23 2012 Alasdair G Kergon <agk@redhat.com>
- new upstream with minor fixes and tmpfiles dirs

* Mon Feb 20 2012 Alasdair G Kergon <agk@redhat.com>
- New upstream with a few fixes including encoding device names to restrict
  them to the udev characterset.

* Thu Feb 16 2012 Peter Rajnoha <prajnoha@redhat.com>
- Update udev requirement for F17+ to v176 at least (built-in blkid).

* Mon Feb 13 2012 Peter Rajnoha <prajnoha@redhat.com>
- Add configure --with-systemdsystemunitdir.

* Sun Feb 12 2012 Alasdair G Kergon <agk@redhat.com>
- New upstream with trivial fixes and refactoring of some lvmcache and
  orphan code.

* Wed Feb 01 2012 Alasdair G Kergon <agk@redhat.com>
- Try with dlm requirement

* Wed Feb 01 2012 Alasdair G Kergon <agk@redhat.com>
- A few little fixes and attempt to make it work with new version of
  corosync.

* Fri Jan 27 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.89-4
- reissued upstream release

* Fri Jan 27 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.89-3
- Reissued upstream release.

* Thu Jan 26 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.89-2
- Install thin monitoring

* Thu Jan 26 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.89-1
- New upstream with experimental support for thinly-provisioned devices.

* Fri Jan 13 2012 Dennis Gilmore <dennis@ausil.us> - 2.02.88-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Peter Robinson <pbrobinson@gmail.com> - 2.02.88-3
- update util-linux-ng -> util-linux dependency as it changed long ago.

* Thu Dec 29 2011 Peter Robinson <pbrobinson@gmail.com> - 2.02.88-2
- update util-linux-ng -> util-linux

* Mon Aug 22 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.88-1
- New upstream - extend lvconvert raid1 support.

* Fri Aug 12 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.87-1
- New upstream release.

* Wed Aug 03 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-5
- Change DEFAULT_UDEV_SYNC to 1 so udev_sync is used even without any
  config.

* Thu Jul 28 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-4
- More systemd support.

* Wed Jul 20 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-3
- Fix broken lvm2-sysinit Requires: lvm2 dependency.

* Mon Jul 18 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-2
- Convert form SysV init to systemd. Add systemd units and sysvinit
  subpackage.

* Fri Jul 08 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.86-1
- New upstream with important snapshot+pvmove fixes.

* Wed Jun 22 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-5
- Rebuild with updated uname string test

* Wed Jun 22 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-4
- Merge branch 'f14'

* Wed Jun 22 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-3
- Update uname patch

* Sat Jun 04 2011 Milan Broz <mbroz@fedoraproject.org> - 2.02.84-2
- Accept kernel 3.0 uname string in libdevmapper initialization.

* Wed Feb 09 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.84-1
- New upstream with essential big-endian fix.

* Wed Feb 09 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.83-3
- New upstream with essential big-endian checksum fix.

* Tue Feb 08 2011 Dennis Gilmore <dennis@ausil.us> - 2.02.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.83-1
- New upstream with assorted small fixes and performance improvements.

* Mon Jan 24 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.82-1
- new upstream with minor fixes

* Tue Jan 18 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.81-1
- New upstream & update /var dirs for systemd.

* Tue Dec 21 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.79-2
- ghost /var/run/lvm

* Tue Dec 21 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.79-1
- New upstream - in particular: clvmd should now cope if /var/run/lvm is
  missing; race in selinux labelling removed; a memory bug introduced in
  2.02.78 is fixed.

* Mon Dec 06 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.78-1
- New upstream with some small fixes.

* Mon Nov 22 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.77-1
- New upstream with minor fixes and enhancements.

* Tue Nov 09 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.76-1
- New upstream with fixes.

* Tue Nov 09 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.75-2
- New upstream with fixes.

* Mon Oct 25 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.75-1
- New upstream - a few fixes and small improvements.

* Wed Sep 29 2010 Jesse Keating <jkeating@redhat.com> - 2.02.74-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.74-1
- New upstream - several bug fixes.

* Wed Aug 25 2010 Peter Rajnoha <prajnoha@redhat.com> - 2.02.73-2
- Add support for setting default data alignment in configure and lvm.conf.

* Wed Aug 18 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.73-1
- Update to 2.02.73

* Wed Aug 18 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-9
- Update to 2.02.73

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-8
- Merge branch 'f12/master'

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-7
- merge f12 with rawhide

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-6
- Merge branch 'f13/master'

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-5
- Merge f13 spec file.

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-4
- remove workaround for /var/run/lvm - fixed by last patch

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-3
- Merge remote branch 'origin/f14/master'

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-2
- sync .gitignore with f14

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-1
- update to 2.02.72

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.70-2
- dist-git conversion

* Wed Jul 07 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.70-1
- more upstream fixes

* Wed Jun 30 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.69-1
- Make it easier to have only a small number of copies of metadata in VGs
  with a large number of PVs.

* Thu Jun 24 2010 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.68-2
- Remove the patch that reverted a fix in udev rules that tries to handle
  spurious events more properly. Add Requires: udev >= 158-1 for it to
  work.

* Wed Jun 23 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.68-1
- new upstream

* Fri Jun 04 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.67-2
- new upstream

* Fri Jun 04 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.67-1
- new upstream (incomplete)

* Thu May 20 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.66-1
- Minor bug fixes; spec file and package 'Requires' cleanups.

* Mon May 17 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.65-1
- More upstream fixes

* Fri Apr 30 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.64-2
- relative symlinks now made upstream

* Fri Apr 30 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.64-1
- more upstream fixes

* Thu Apr 15 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.63-6
- revert - built locally ok but fails in koji

* Thu Apr 15 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.63-5
- Misc. spec file cleaning. Move plugin .so files into new subdir.

* Wed Apr 14 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.63-4
- changelog

* Wed Apr 14 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.63-3
- next iteration - workaround more new 'make install' bugs

* Wed Apr 14 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.63-2
- first iteration (broken make install)

* Wed Apr 14 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.63-1
- new upstream (incomplete)

* Tue Mar 09 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.62-1
- more upstream bug fixes/simple enhancements

* Fri Mar 05 2010 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.61-3
- Change spec file to support excluding cluster components from the build.

* Tue Feb 16 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.61-2
- reinstate a so.2.02

* Tue Feb 16 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.61-1
- new upstream - minor fixes

* Fri Jan 29 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.60-2
- 8 spaces = tab, I hope

* Sat Jan 23 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.60-1
- After these iterations, hopefully this is the first relesae with cmirror
  and dmeventd both working.

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.59-5
- Other as-yet-undocumented upstream fixes. - Fix failed locking messages
  to be more descriptive

* Fri Jan 22 2010 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.59-4
- Drop duplicated BuildRequires on openaislib-devel. Drop Requires on
  clusterlib for cmirror subpackage (cmirror doesn't use any library from
  cluster) clvmd subpackage should Requires cman (#506592).

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.59-3
- 2nd fix to release

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.59-2
- old

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.59-1
- Add cmirror subpackage for clustered mirrors. Set 'preferred_names' in
  default lvm.conf (until we fix it properly upstream). Use new upstream
  package with miscellaneous fixes.

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.58-4
- first fix to release

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.58-3
- updated upstream source

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.58-2
- Change default preferred_names until we fix the upstream code.

* Thu Jan 14 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.58-1
- add snapshot merge support

* Tue Jan 12 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.57-2
- Missing hyphens!

* Tue Jan 12 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.57-1
- New upstream - lots of fixes & some minor new features.

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 2.02.56-2
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Tue Nov 24 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.56-1
- Several essential fixes to the last release.

* Thu Nov 19 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.55-1
- New upstream - contains important mirror+dmeventd monitoring fixes.

* Fri Nov 13 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.54-3
- Remove last_rule from udev rules and support udev flags even when
  udev_sync is disabled.

* Tue Nov 03 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.54-2
- Enable udev synchronisation code and install default udev rules.

* Tue Oct 27 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.54-1
- New upstream - fixes and minor features.

* Mon Oct 19 2009 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.53-4
- Enable openais support in clvmd

* Sat Sep 26 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.53-3
- Reissued upstream release to fix compilation warning.

* Fri Sep 25 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.53-2
- old

* Fri Sep 25 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.53-1
- folded patches into tarball & a few more fixes

* Thu Sep 24 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.52-13
- Disable udev synchronisation code.

* Mon Sep 21 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.52-12
- Include /lib/udev/rules.d directory in the package.

* Mon Sep 21 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.52-11
- Enable udev synchronisation code and install default udev rules.

* Thu Sep 17 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-10
- Enable dmeventd monitoring section of config file by default.

* Thu Sep 17 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-9
- Fix dmeventd _temporary_log_fn in plugins

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-8
- add monitoring patch from upstream

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-7
- Update monitoring script

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-6
- fix -event version

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-5
- event already pulls in -event-libs

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-4
- event-libs does not require -event (circular)

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-3
- First attempt at including dmeventd.

* Tue Sep 15 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-2
- fix tarball - remove test/api from build

* Tue Sep 15 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-1
- New upstream with fixes and new udev code (not yet switched on).

* Mon Aug 24 2009 Milan Broz <mbroz@fedoraproject.org> - 2.02.51-4
- Fix global locking in PV reporting commands (2.02.49). Fix pvcreate on a
  partition (2.02.51). Build clvmd with both cman and corosync support.

* Thu Aug 06 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.51-3
- The build system failed to recover correctly from the build failure and
  left the database in an inconsistent state. Abandon -1.

* Thu Aug 06 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.51-2
- inc dm version no

* Thu Aug 06 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.51-1
- New upstream, fixing a bug that made lvm2-cluster 2.02.50 unusable and
  finishing the data alignment support.

* Thu Jul 30 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.50-4
- inc release

* Thu Jul 30 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.50-3
- lvm2-devel requires device-mapper-devel. Fix lvm2app.pc filename.

* Tue Jul 28 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.50-2
- new upstream

* Tue Jul 28 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.50-1
- New upstream with a few bug fixes plus the first version of an
  application library for LVM2. The API is not yet frozen.

* Sat Jul 25 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.02.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.49-2
- Revert a patch that broke clvmd compilation.

* Wed Jul 15 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.49-1
- new upstream development release

* Fri Jul 10 2009 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.48-2
- Make sure to Requires and BuildRequires corosync-lib and cluster-lib in
  stable version. There was no API or ABI change since last time LVM2 was
  rebuilt so this change can flow in peacefully at the next update.

* Wed Jul 01 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.48-1
- New upstream

* Thu Jun 11 2009 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.47-3
- BuildRequire newer version of corosynclib (0.97-1) to link against latest
  libraries version (soname 4.0.0). Add lvm2-2_02_48-cluster-cpg-new-
  api.patch to port clvmd-corosync to new corosync cpg API.

* Fri May 22 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.47-2
- included in release

* Fri May 22 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.47-1
- new upstream release

* Fri Apr 17 2009 Milan Broz <mbroz@fedoraproject.org> - 2.02.45-4
- Add MMC (mmcblk) device type to filters. (483686)

* Mon Mar 30 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.45-3
- Add upstream source location (bz 226111) and summarise corosync comment.

* Mon Mar 30 2009 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.45-2
- Rebuild on top of fixed corosynclib

* Tue Mar 03 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.45-1
- new upstream release and switch cluster code to use corosync...

* Wed Feb 25 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.02.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.44-1
- New upstream release.

* Mon Nov 10 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.43-2
- fix upstream configure

* Mon Nov 10 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.43-1
- New upstream release with merged lvm2 & dm source trees.

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-15
- and again...

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-14
- and again

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-13
- Try to workaround this yet another way...

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-12
- and again

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-11
- and another try...

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-10
- fix patch

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-9
- another attempt at fixing to work with new version of rpm

* Tue Sep 30 2008 Bill Nottingham <notting@fedoraproject.org> - 2.02.39-8
- reorder changelog so RPM does not choke on it

* Fri Sep 26 2008 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.39-7
- Add BuildRequires on cmanlib-devel. This is required after libcman split
  from cman and cman-devel into cmanlib and cmanlib-devel. Make versioned
  BuildRequires on cman-devel and cmanlib-devel more strict to guarantee to
  get the right version.

* Thu Sep 25 2008 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.39-6
- Add versioned BuildRequires on cman-devel

* Tue Sep 23 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-5
- Explicitly create /sbin in the build root. (It used to work without
  this.)

* Tue Sep 23 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-4
- Change %%%%patch to %%%%patch0 to match Patch0 as required by RPM package
  update.

* Tue Sep 16 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-3
- fix percent in comments; add comment for patch

* Thu Aug 07 2008 Tom Callaway <spot@fedoraproject.org> - 2.02.39-2
- fix license tag

* Fri Jun 27 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-1
- more upstream fixes and small enhancements

* Wed Jun 25 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.38-2
- new upstream with dmsetup options closer to udev requirements

* Fri Jun 13 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.38-1
- Update to latest upstream.

* Thu Apr 03 2008 Jeremy Katz <katzj@fedoraproject.org> - 2.02.33-3
- Adjust for new name for vio disks (from danpb) - And fix the build (also
  from danpb)

* Wed Mar 05 2008 Jeremy Katz <katzj@fedoraproject.org> - 2.02.33-2
- recognize vio disks

* Thu Jan 31 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.33-1
- Improve internal label caching performance while locks are held. Fix
  mirror log name construction during lvconvert.

* Tue Jan 29 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.32-1
- fix version

* Tue Jan 29 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.31-2
- new upstream bug fix release

* Sat Jan 19 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.31-1
- couple of fixes to last release

* Fri Jan 18 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.30-3
- revert make ordering

* Fri Jan 18 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.30-2
- del old sig

* Fri Jan 18 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.30-1
- New upstream with fixes and enhancements. Removed static libraries and
  binaries & moved most remaining ones out of /usr.

* Thu Dec 20 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-7
- new upstream device-mapper (readahead fixes)

* Thu Dec 13 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-6
- missing modprobe deps

* Fri Dec 07 2007 Jeremy Katz <katzj@fedoraproject.org> - 2.02.29-5
- Defining a macro to define the release is overkill; just use %%release.
  This then pulls in the disttag and fixes the broken deps

* Thu Dec 06 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-4
- add back intro

* Thu Dec 06 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-3
- copies not needed

* Thu Dec 06 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-2
- merge dm build into lvm2 one

* Wed Dec 05 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-1
- new upstream

* Mon Oct 15 2007 Bill Nottingham <notting@fedoraproject.org> - 2.02.28-2
- makefile update to properly grab makefile.common

* Fri Aug 24 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.28-1
- new upstream

* Thu Aug 09 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.27-4
- fix date in changelog

* Thu Aug 09 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.27-3
- licence is v2 only of GPL.

* Wed Aug 01 2007 Milan Broz <mbroz@fedoraproject.org> - 2.02.27-2
- Add SUN's LDOM virtual block device (vdisk) and ps3disk to filters.
  Resolves: #249672

* Wed Jul 18 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.27-1
- latest release

* Thu May 03 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.24-4
- revert koji test (as f7 hasn't branched)

* Thu May 03 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.24-3
- Build test using koji.

* Mon Mar 19 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.24-2
- add buildreq readline-static till makefiles fixed (makefile needs it but
  static binary doesn't)

* Mon Mar 19 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.24-1
- more fixes

* Thu Mar 08 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.23-1
- Move .cache into new /etc/lvm/cache/ dir to assist selinux. vgrename-by-
  uuid fix

* Wed Feb 14 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.22-4
- Rebuild after device-mapper package split.

* Wed Feb 14 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.22-3
- Remove readline support from lvm.static

* Tue Feb 13 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.22-2
- Add ncurses-static BuildRequires after package split.

* Tue Feb 13 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.22-1
- minor upstream bugfixes

* Mon Feb 05 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-5
- Remove file wildcards and unintentional lvmconf installation.

* Mon Feb 05 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-4
- update dm dep

* Mon Feb 05 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-3
- Add build dependency on new device-mapper-devel package.

* Wed Jan 31 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-2
- Remove superfluous execute perm from .cache data file.

* Tue Jan 30 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-1
- new upstream

* Fri Jan 26 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.20-1
- new upstream

* Mon Jan 22 2007 Milan Broz <mbroz@fedoraproject.org> - 2.02.19-2
- Remove BuildRequires libtermcap-devel Resolves: #223766

* Wed Jan 17 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.19-1
- new upstream

* Fri Jan 12 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.18-3
- brew test

* Thu Jan 11 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.18-2
- fix date

* Thu Jan 11 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.18-1
- Upstream update. N.B. Note dumpconfig syntax change.

* Thu Dec 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.17-1
- more fixes

* Fri Dec 01 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.16-1
- new upstream with fixes

* Tue Nov 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.15-4
- Fix clvmd init script line truncation.

* Tue Nov 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.15-3
- fix date

* Tue Nov 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.15-2
- fix lvm.conf segfault

* Mon Nov 20 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.15-1
- several fixes

* Fri Nov 10 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.14-1
- new upstream

* Mon Oct 30 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.13-2
- Fix high-level free-space check on partial allocation.

* Fri Oct 27 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.13-1
- New upstream.

* Fri Oct 20 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.12-3
- Remove no-longer-used ldconfig from lvm2-cluster and fix lvmconf to cope
  without the shared library.

* Mon Oct 16 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.12-2
- fix patch for 2.0.12

* Mon Oct 16 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.12-1
- Fix pvdisplay to use vg_read() for non-orphans. Fall back to internal
  locking if external locking lib is missing or fails. Retain activation
  state after changing LV minor number with --force. Propagate clustered
  flag in vgsplit and require resizeable flag.

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-9
- fix file list and %%define -_

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org>
- attempt to incorporate lvm2-cluster as a subpackage

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-7
- Install lvmdump script.

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-6
- Build in cluster locking with fallback if external locking fails to load.
  [Preparation for combining the spec file with the lvm2-cluster one.]

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-5
- Drop .0 suffix from release.

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-4
- Append %%{?dist} to Release.

* Fri Oct 13 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-3
- inc dm dependency

* Fri Oct 13 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-2
- remove 2.2.6 patch

* Fri Oct 13 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-1
- New upstream with numerous fixes and small enhancements.

* Thu Sep 28 2006 Peter Jones <pjones@fedoraproject.org> - 2.02.06-1
- Fix alignment issues on ppc64 (#206202)

* Tue Sep 19 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.10-1
- new upstream

* Tue Aug 01 2006 Jeremy Katz <katzj@fedoraproject.org> - 2.02.06-6
- require new libselinux to avoid segfaults on xen (#200783)

* Thu Jul 27 2006 Jeremy Katz <katzj@fedoraproject.org> - 2.02.06-5
- free trip through the buildsystem

* Wed Jul 12 2006 Jesse Keating <jkeating@fedoraproject.org> - 2.02.06-4
- bumped for rebuild

* Tue Jun 06 2006 Stephen Tweedie <sct@fedoraproject.org> - 2.02.06-3
- Rebuild to pick up new nosegneg libc.a for lvm.static

* Mon May 22 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.06-2
- BuildRequires libsepol-devel.

* Fri May 12 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.06-1
- new upstream release

* Sat Apr 22 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.05-3
- exclude archs that aren't building

* Fri Apr 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.05-2
- build fails without the new dm package

* Fri Apr 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.05-1
- Fix VG uuid comparisons.

* Wed Apr 19 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.04-1
- New release upstream, including better handling of duplicated VG names.

* Sat Feb 11 2006 Jesse Keating <jkeating@fedoraproject.org> - 2.02.01-7
- bump for bug in double-long on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@fedoraproject.org> - 2.02.01-6
- bump for new gcc/glibc

* Fri Dec 09 2005 Jesse Keating <jkeating@fedoraproject.org> - 2.02.01-5
- gcc update bump

* Fri Dec 02 2005 Peter Jones <pjones@fedoraproject.org> - 2.02.01-4
- fix /etc/lvm in files

* Fri Dec 02 2005 Peter Jones <pjones@fedoraproject.org> - 2.02.01-3
- directories should still be owned

* Fri Dec 02 2005 Peter Jones <pjones@fedoraproject.org> - 2.02.01-2
- xvd patch is applied upstream

* Fri Dec 02 2005 Peter Jones <pjones@fedoraproject.org> - 2.02.01-1
- update to 1.02.02

* Wed Nov 09 2005 Jeremy Katz <katzj@fedoraproject.org> - 2.01.14-5
- add patch for xen block devices

* Sat Oct 15 2005 Florian La Roche <laroche@fedoraproject.org> - 2.01.14-4
- fix compile problems

* Thu Sep 15 2005 Jeremy Katz <katzj@fedoraproject.org> - 2.01.14-3
- the distro doesn't really work without a 2.6 kernel, so no need to
  require it

* Thu Aug 04 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.14-2
- fix changelog date

* Thu Aug 04 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.14-1
- A few more bug fixes.

* Wed Jul 13 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.13-1
- fix some bugs discovered in last release

* Tue Jun 14 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.12-3
- fix static build

* Tue Jun 14 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.12-2
- update dm dep

* Tue Jun 14 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.12-1
- A few more fixes since yesterday.

* Mon Jun 13 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.11-1
- New version upstream with a lot of fixes and enhancements.

* Wed Apr 27 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.08-3
- Add /etc/lvm

* Wed Apr 27 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.08-2
- No longer abort read operations if archive/backup directories aren't
  there. Add runtime directories and file to the package.

* Tue Mar 22 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.08-1
- Improve detection of external changes affecting internal cache. - Add
  clustered VG attribute. - Suppress rmdir opendir error message.

* Thu Mar 10 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.07-4
- And another compiler message.

* Thu Mar 10 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.07-3
- Suppress more compiler messages.

* Thu Mar 10 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.07-2
- suppress some new compiler messages

* Tue Mar 08 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.07-1
- Remove build directory from built-in path. Extra /dev scanning required
  for clustered operation.

* Thu Mar 03 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.06-1
- Allow anaconda to suppress warning messages.

* Fri Feb 18 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.05-1
- Upstream changes not affecting Fedora.

* Wed Feb 09 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.04-1
- Offset pool minors; lvm2cmd.so skips open fd check; pvmove -f gone.

* Tue Feb 01 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.03-1
- Fix snapshot device size & 64-bit display output.

* Fri Jan 21 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.02-1
- minor fixes

* Wed Jan 19 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.01-1
- Update vgcreate man page. Preparation for snapshot origin extension fix.

* Mon Jan 17 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.00-1
- Fix metadata auto-correction. Only request open_count when needed.

* Wed Jan 12 2005 Tim Waugh <twaugh@fedoraproject.org> - 2.00.33-2
- Rebuilt for new readline.

* Fri Jan 07 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.00.33-1
- wipe ext fs label; several clvm fixes

* Thu Jan 06 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.00.32-2
- Remove temporary /sbin symlinks no longer needed. Include read-only pool
  support in the build.

* Wed Dec 22 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.32-1
- More fixes (143501).

* Sun Dec 12 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.31-1
- Fix pvcreate installer issues.

* Fri Dec 10 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.30-1
- Additional debugging code.

* Tue Nov 30 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.29-4
- Reinstate archs.

* Sun Nov 28 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.29-3
- Try excluding more archs

* Sat Nov 27 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.29-2
- Try without s390x which is failing.

* Sat Nov 27 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.29-1
- Fix last fix.

* Sat Nov 27 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.28-1
- Endian fix.

* Wed Nov 24 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.27-1
- Fix partition table detection & an out of memory segfault.

* Tue Nov 23 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.26-1
- Several installation-related fixes & man page updates.

* Mon Oct 25 2004 Elliot Lee <sopwith@fedoraproject.org> - 2.00.25-2
- Fix 2.6 kernel requirement

* Wed Sep 29 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.25-1
- Fix vgmknodes return code & vgremove locking.

* Fri Sep 17 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.24-2
- Obsolete old lvm1 packages; refuse install if running kernel 2.4. [bz
  128185]

* Thu Sep 16 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.24-1
- More upstream fixes & a couple of requested buildrequires.

* Wed Sep 15 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.23-1
- Various minor upstream fixes. Support for 'make new-base'.

* Tue Sep 14 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.22-1
- Reinstate updates lost during the migration

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.21-2
- auto-import changelog data from lvm2-2.00.21-2.src.rpm Thu Sep 02 2004
  Jeremy Katz <katzj@redhat.com> - 2.00.21-2 - fix permissions on vg dirs

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.21-1
- auto-import changelog data from lvm2-2.00.21-1.src.rpm Thu Aug 19 2004
  Alasdair Kergon <agk@redhat.com> - 2.00.21-1 - New upstream release
  incorporating fixes plus minor enhancements.

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.20-2
- auto-import changelog data from lvm2-2.00.20-2.src.rpm Tue Aug 17 2004
  Jeremy Katz <katzj@redhat.com> - 2.00.20-2 - add patch for iSeries
  viodasd support - add patch to check file type using stat(2) if d_type ==
  DT_UNKNOWN (#129674)

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.20-1
- auto-import changelog data from lvm2-2.00.20-1.src.rpm Sat Jul 03 2004
  Alasdair Kergon <agk@redhat.com> - 2.00.20-1 - New upstream release fixes
  2.6 kernel device numbers.

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.19-1
- auto-import changelog data from lvm2-2.00.19-1.src.rpm Tue Jun 29 2004
  Alasdair Kergon <agk@redhat.com> - 2.00.19-1 - Latest upstream release.
  Lots of changes (see WHATS_NEW).

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.15-4
- auto-import changelog data from lvm2-2.00.15-5.src.rpm Tue Jun 15 2004
  Elliot Lee <sopwith@redhat.com> - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.15-3
- auto-import lvm2-2.00.15-4 from lvm2-2.00.15-4.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.15-2
- auto-import changelog data from lvm2-2.00.15-3.src.rpm Wed May 26 2004
  Alasdair Kergon <agk@redhat.com> - 2.00.15-3 - vgscan shouldn't return
  error status when no VGs present

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.15-1
- auto-import changelog data from lvm2-2.00.15-2.src.rpm Thu May 06 2004
  Warren Togami <wtogami@redhat.com> - 2.00.15-2 - i2o patch from Markus
  Lidel Tue Apr 20 2004 Bill Nottingham <notting@redhat.com> - 2.00.15-1.1
  - handle disabled SELinux correctly, so that LVMs can be detected in a
  non-SELinux context Mon Apr 19 2004 Alasdair Kergon <agk@redhat.com> -
  2.00.15-1 - Fix non-root build with current version of 'install'. Fri Apr
  16 2004 Alasdair Kergon <agk@redhat.com> - 2.00.14-1 - Use 64-bit file
  offsets. Fri Apr 16 2004 Alasdair Kergon <agk@redhat.com> - 2.00.13-1 -
  Avoid scanning devices containing md superblocks. - Integrate ENOTSUP
  patch. Thu Apr 15 2004 Jeremy Katz <katzj@redhat.com> - 2.00.12-4 - don't
  die if we get ENOTSUP setting selinux contexts Thu Apr 15 2004 Alasdair
  Kergon <agk@redhat.com> 2.00.12-3 - Add temporary pvscan symlink for LVM1
  until mkinitrd gets updated. Wed Apr 14 2004 Alasdair Kergon
  <agk@redhat.com> 2.00.12-2 - Mark config file noreplace. Wed Apr 14 2004
  Alasdair Kergon <agk@redhat.com> 2.00.12-1 - Install default
  /etc/lvm/lvm.conf. - Move non-static binaries to /usr/sbin. - Add
  temporary links in /sbin to lvm.static until rc.sysinit gets updated. Thu
  Apr 08 2004 Alasdair Kergon <agk@redhat.com> 2.00.11-1 - Fallback to
  using LVM1 tools when using a 2.4 kernel without device-mapper. Wed Apr
  07 2004 Alasdair Kergon <agk@redhat.com> 2.00.10-2 - Install the full
  toolset, not just 'lvm'. Wed Apr 07 2004 Alasdair Kergon <agk@redhat.com>
  2.00.10-1 - Update to version 2.00.10, which incorporates the RH-specific
  patches and includes various fixes and enhancements detailed in
  WHATS_NEW.

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.08-7
- auto-import changelog data from lvm2-2.00.08-5.src.rpm Wed Mar 17 2004
  Jeremy Katz <katzj@redhat.com> 2.00.08-5 - Fix sysfs patch to find sysfs
  - Take patch from dwalsh and tweak a little for setting SELinux contexts
  on device node creation and also do it on the symlink creation. Part of
  this should probably be pushed down to device-mapper instead Thu Feb 19
  2004 Stephen C. Tweedie <sct@redhat.com> 2.00.08-4 - Add sysfs filter
  patch - Allow non-root users to build RPM Fri Feb 13 2004 Elliot Lee
  <sopwith@redhat.com> - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 2.00.08-6
- auto-import changelog data from lvm2-2.00.08-2.src.rpm Fri Dec 05 2003
  Jeremy Katz <katzj@redhat.com> 2.00.08-2 - add static lvm binary Tue Dec
  02 2003 Jeremy Katz <katzj@redhat.com> - Initial build.

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-5
- Another attempt to fix the build.

* Sat Jul 31 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-4
- remove explicit Base version from libs

* Sat Jul 31 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-3
- sources file was missing

* Sat Jul 31 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-2
- Latest upstream release, fixing lvm2-cluster CVE-2010-2526.

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-1
- Update to 2.02.72-4.

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.62-4
- dist-git conversion

* Fri Mar 19 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.62-3
- more haste...less speed...

* Fri Mar 19 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.62-2
- Fix libdevmapper-event pkgconfig version string to match libdevmapper.

* Mon Mar 15 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.62-1
- latest fixes incl. reducing locked memory usage

* Wed Feb 17 2010 Jesse Keating <jkeating@fedoraproject.org> - 2.02.61-3
- Initialize branch F-13 for lvm2

* Tue Feb 16 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.61-2
- reinstate a so.2.02

* Tue Feb 16 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.61-1
- new upstream - minor fixes

* Fri Jan 29 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.60-2
- 8 spaces = tab, I hope

* Sat Jan 23 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.60-1
- After these iterations, hopefully this is the first relesae with cmirror
  and dmeventd both working.

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.59-5
- Other as-yet-undocumented upstream fixes. - Fix failed locking messages
  to be more descriptive

* Fri Jan 22 2010 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.59-4
- Drop duplicated BuildRequires on openaislib-devel. Drop Requires on
  clusterlib for cmirror subpackage (cmirror doesn't use any library from
  cluster) clvmd subpackage should Requires cman (#506592).

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.59-3
- 2nd fix to release

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.59-2
- old

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.59-1
- Add cmirror subpackage for clustered mirrors. Set 'preferred_names' in
  default lvm.conf (until we fix it properly upstream). Use new upstream
  package with miscellaneous fixes.

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.58-4
- first fix to release

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.58-3
- updated upstream source

* Fri Jan 22 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.58-2
- Change default preferred_names until we fix the upstream code.

* Thu Jan 14 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.58-1
- add snapshot merge support

* Tue Jan 12 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.57-2
- Missing hyphens!

* Tue Jan 12 2010 Alasdair Kergon <agk@fedoraproject.org> - 2.02.57-1
- New upstream - lots of fixes & some minor new features.

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 2.02.56-2
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Tue Nov 24 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.56-1
- Several essential fixes to the last release.

* Thu Nov 19 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.55-1
- New upstream - contains important mirror+dmeventd monitoring fixes.

* Fri Nov 13 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.54-3
- Remove last_rule from udev rules and support udev flags even when
  udev_sync is disabled.

* Tue Nov 03 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.54-2
- Enable udev synchronisation code and install default udev rules.

* Tue Oct 27 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.54-1
- New upstream - fixes and minor features.

* Mon Oct 19 2009 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.53-4
- Enable openais support in clvmd

* Sat Sep 26 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.53-3
- Reissued upstream release to fix compilation warning.

* Fri Sep 25 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.53-2
- old

* Fri Sep 25 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.53-1
- folded patches into tarball & a few more fixes

* Thu Sep 24 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.52-13
- Disable udev synchronisation code.

* Mon Sep 21 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.52-12
- Include /lib/udev/rules.d directory in the package.

* Mon Sep 21 2009 Peter Rajnoha <prajnoha@fedoraproject.org> - 2.02.52-11
- Enable udev synchronisation code and install default udev rules.

* Thu Sep 17 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-10
- Enable dmeventd monitoring section of config file by default.

* Thu Sep 17 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-9
- Fix dmeventd _temporary_log_fn in plugins

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-8
- add monitoring patch from upstream

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-7
- Update monitoring script

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-6
- fix -event version

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-5
- event already pulls in -event-libs

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-4
- event-libs does not require -event (circular)

* Wed Sep 16 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-3
- First attempt at including dmeventd.

* Tue Sep 15 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-2
- fix tarball - remove test/api from build

* Tue Sep 15 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.52-1
- New upstream with fixes and new udev code (not yet switched on).

* Mon Aug 24 2009 Milan Broz <mbroz@fedoraproject.org> - 2.02.51-4
- Fix global locking in PV reporting commands (2.02.49). Fix pvcreate on a
  partition (2.02.51). Build clvmd with both cman and corosync support.

* Thu Aug 06 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.51-3
- The build system failed to recover correctly from the build failure and
  left the database in an inconsistent state. Abandon -1.

* Thu Aug 06 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.51-2
- inc dm version no

* Thu Aug 06 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.51-1
- New upstream, fixing a bug that made lvm2-cluster 2.02.50 unusable and
  finishing the data alignment support.

* Thu Jul 30 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.50-4
- inc release

* Thu Jul 30 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.50-3
- lvm2-devel requires device-mapper-devel. Fix lvm2app.pc filename.

* Tue Jul 28 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.50-2
- new upstream

* Tue Jul 28 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.50-1
- New upstream with a few bug fixes plus the first version of an
  application library for LVM2. The API is not yet frozen.

* Sat Jul 25 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.02.49-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.49-2
- Revert a patch that broke clvmd compilation.

* Wed Jul 15 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.49-1
- new upstream development release

* Fri Jul 10 2009 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.48-2
- Make sure to Requires and BuildRequires corosync-lib and cluster-lib in
  stable version. There was no API or ABI change since last time LVM2 was
  rebuilt so this change can flow in peacefully at the next update.

* Wed Jul 01 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.48-1
- New upstream

* Thu Jun 11 2009 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.47-3
- BuildRequire newer version of corosynclib (0.97-1) to link against latest
  libraries version (soname 4.0.0). Add lvm2-2_02_48-cluster-cpg-new-
  api.patch to port clvmd-corosync to new corosync cpg API.

* Fri May 22 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.47-2
- included in release

* Fri May 22 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.47-1
- new upstream release

* Fri Apr 17 2009 Milan Broz <mbroz@fedoraproject.org> - 2.02.45-4
- Add MMC (mmcblk) device type to filters. (483686)

* Mon Mar 30 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.45-3
- Add upstream source location (bz 226111) and summarise corosync comment.

* Mon Mar 30 2009 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.45-2
- Rebuild on top of fixed corosynclib

* Tue Mar 03 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.45-1
- new upstream release and switch cluster code to use corosync...

* Wed Feb 25 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.02.44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Alasdair Kergon <agk@fedoraproject.org> - 2.02.44-1
- New upstream release.

* Mon Nov 10 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.43-2
- fix upstream configure

* Mon Nov 10 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.43-1
- New upstream release with merged lvm2 & dm source trees.

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-15
- and again...

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-14
- and again

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-13
- Try to workaround this yet another way...

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-12
- and again

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-11
- and another try...

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-10
- fix patch

* Tue Oct 07 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-9
- another attempt at fixing to work with new version of rpm

* Tue Sep 30 2008 Bill Nottingham <notting@fedoraproject.org> - 2.02.39-8
- reorder changelog so RPM does not choke on it

* Fri Sep 26 2008 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.39-7
- Add BuildRequires on cmanlib-devel. This is required after libcman split
  from cman and cman-devel into cmanlib and cmanlib-devel. Make versioned
  BuildRequires on cman-devel and cmanlib-devel more strict to guarantee to
  get the right version.

* Thu Sep 25 2008 Fabio M. Di Nitto <fabbione@fedoraproject.org> - 2.02.39-6
- Add versioned BuildRequires on cman-devel

* Tue Sep 23 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-5
- Explicitly create /sbin in the build root. (It used to work without
  this.)

* Tue Sep 23 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-4
- Change %%%%patch to %%%%patch0 to match Patch0 as required by RPM package
  update.

* Tue Sep 16 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-3
- fix percent in comments; add comment for patch

* Thu Aug 07 2008 Tom Callaway <spot@fedoraproject.org> - 2.02.39-2
- fix license tag

* Fri Jun 27 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.39-1
- more upstream fixes and small enhancements

* Wed Jun 25 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.38-2
- new upstream with dmsetup options closer to udev requirements

* Fri Jun 13 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.38-1
- Update to latest upstream.

* Thu Apr 03 2008 Jeremy Katz <katzj@fedoraproject.org> - 2.02.33-3
- Adjust for new name for vio disks (from danpb) - And fix the build (also
  from danpb)

* Wed Mar 05 2008 Jeremy Katz <katzj@fedoraproject.org> - 2.02.33-2
- recognize vio disks

* Thu Jan 31 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.33-1
- Improve internal label caching performance while locks are held. Fix
  mirror log name construction during lvconvert.

* Tue Jan 29 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.32-1
- fix version

* Tue Jan 29 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.31-2
- new upstream bug fix release

* Sat Jan 19 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.31-1
- couple of fixes to last release

* Fri Jan 18 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.30-3
- revert make ordering

* Fri Jan 18 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.30-2
- del old sig

* Fri Jan 18 2008 Alasdair Kergon <agk@fedoraproject.org> - 2.02.30-1
- New upstream with fixes and enhancements. Removed static libraries and
  binaries & moved most remaining ones out of /usr.

* Thu Dec 20 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-7
- new upstream device-mapper (readahead fixes)

* Thu Dec 13 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-6
- missing modprobe deps

* Fri Dec 07 2007 Jeremy Katz <katzj@fedoraproject.org> - 2.02.29-5
- Defining a macro to define the release is overkill; just use %%release.
  This then pulls in the disttag and fixes the broken deps

* Thu Dec 06 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-4
- add back intro

* Thu Dec 06 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-3
- copies not needed

* Thu Dec 06 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-2
- merge dm build into lvm2 one

* Wed Dec 05 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.29-1
- new upstream

* Mon Oct 15 2007 Bill Nottingham <notting@fedoraproject.org> - 2.02.28-2
- makefile update to properly grab makefile.common

* Fri Aug 24 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.28-1
- new upstream

* Thu Aug 09 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.27-4
- fix date in changelog

* Thu Aug 09 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.27-3
- licence is v2 only of GPL.

* Wed Aug 01 2007 Milan Broz <mbroz@fedoraproject.org> - 2.02.27-2
- Add SUN's LDOM virtual block device (vdisk) and ps3disk to filters.
  Resolves: #249672

* Wed Jul 18 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.27-1
- latest release

* Thu May 03 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.24-4
- revert koji test (as f7 hasn't branched)

* Thu May 03 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.24-3
- Build test using koji.

* Mon Mar 19 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.24-2
- add buildreq readline-static till makefiles fixed (makefile needs it but
  static binary doesn't)

* Mon Mar 19 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.24-1
- more fixes

* Thu Mar 08 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.23-1
- Move .cache into new /etc/lvm/cache/ dir to assist selinux. vgrename-by-
  uuid fix

* Wed Feb 14 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.22-4
- Rebuild after device-mapper package split.

* Wed Feb 14 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.22-3
- Remove readline support from lvm.static

* Tue Feb 13 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.22-2
- Add ncurses-static BuildRequires after package split.

* Tue Feb 13 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.22-1
- minor upstream bugfixes

* Mon Feb 05 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-5
- Remove file wildcards and unintentional lvmconf installation.

* Mon Feb 05 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-4
- update dm dep

* Mon Feb 05 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-3
- Add build dependency on new device-mapper-devel package.

* Wed Jan 31 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-2
- Remove superfluous execute perm from .cache data file.

* Tue Jan 30 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.21-1
- new upstream

* Fri Jan 26 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.20-1
- new upstream

* Mon Jan 22 2007 Milan Broz <mbroz@fedoraproject.org> - 2.02.19-2
- Remove BuildRequires libtermcap-devel Resolves: #223766

* Wed Jan 17 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.19-1
- new upstream

* Fri Jan 12 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.18-3
- brew test

* Thu Jan 11 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.18-2
- fix date

* Thu Jan 11 2007 Alasdair Kergon <agk@fedoraproject.org> - 2.02.18-1
- Upstream update. N.B. Note dumpconfig syntax change.

* Thu Dec 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.17-1
- more fixes

* Fri Dec 01 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.16-1
- new upstream with fixes

* Tue Nov 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.15-4
- Fix clvmd init script line truncation.

* Tue Nov 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.15-3
- fix date

* Tue Nov 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.15-2
- fix lvm.conf segfault

* Mon Nov 20 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.15-1
- several fixes

* Fri Nov 10 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.14-1
- new upstream

* Mon Oct 30 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.13-2
- Fix high-level free-space check on partial allocation.

* Fri Oct 27 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.13-1
- New upstream.

* Fri Oct 20 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.12-3
- Remove no-longer-used ldconfig from lvm2-cluster and fix lvmconf to cope
  without the shared library.

* Mon Oct 16 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.12-2
- fix patch for 2.0.12

* Mon Oct 16 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.12-1
- Fix pvdisplay to use vg_read() for non-orphans. Fall back to internal
  locking if external locking lib is missing or fails. Retain activation
  state after changing LV minor number with --force. Propagate clustered
  flag in vgsplit and require resizeable flag.

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-9
- fix file list and %%define -_

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org>
- attempt to incorporate lvm2-cluster as a subpackage

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-7
- Install lvmdump script.

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-6
- Build in cluster locking with fallback if external locking fails to load.
  [Preparation for combining the spec file with the lvm2-cluster one.]

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-5
- Drop .0 suffix from release.

* Sat Oct 14 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-4
- Append %%{?dist} to Release.

* Fri Oct 13 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-3
- inc dm dependency

* Fri Oct 13 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-2
- remove 2.2.6 patch

* Fri Oct 13 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.11-1
- New upstream with numerous fixes and small enhancements.

* Thu Sep 28 2006 Peter Jones <pjones@fedoraproject.org> - 2.02.06-1
- Fix alignment issues on ppc64 (#206202)

* Tue Sep 19 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.10-1
- new upstream

* Tue Aug 01 2006 Jeremy Katz <katzj@fedoraproject.org> - 2.02.06-6
- require new libselinux to avoid segfaults on xen (#200783)

* Thu Jul 27 2006 Jeremy Katz <katzj@fedoraproject.org> - 2.02.06-5
- free trip through the buildsystem

* Wed Jul 12 2006 Jesse Keating <jkeating@fedoraproject.org> - 2.02.06-4
- bumped for rebuild

* Tue Jun 06 2006 Stephen Tweedie <sct@fedoraproject.org> - 2.02.06-3
- Rebuild to pick up new nosegneg libc.a for lvm.static

* Mon May 22 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.06-2
- BuildRequires libsepol-devel.

* Fri May 12 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.06-1
- new upstream release

* Sat Apr 22 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.05-3
- exclude archs that aren't building

* Fri Apr 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.05-2
- build fails without the new dm package

* Fri Apr 21 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.05-1
- Fix VG uuid comparisons.

* Wed Apr 19 2006 Alasdair Kergon <agk@fedoraproject.org> - 2.02.04-1
- New release upstream, including better handling of duplicated VG names.

* Sat Feb 11 2006 Jesse Keating <jkeating@fedoraproject.org> - 2.02.01-7
- bump for bug in double-long on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@fedoraproject.org> - 2.02.01-6
- bump for new gcc/glibc

* Fri Dec 09 2005 Jesse Keating <jkeating@fedoraproject.org> - 2.02.01-5
- gcc update bump

* Fri Dec 02 2005 Peter Jones <pjones@fedoraproject.org> - 2.02.01-4
- fix /etc/lvm in files

* Fri Dec 02 2005 Peter Jones <pjones@fedoraproject.org> - 2.02.01-3
- directories should still be owned

* Fri Dec 02 2005 Peter Jones <pjones@fedoraproject.org> - 2.02.01-2
- xvd patch is applied upstream

* Fri Dec 02 2005 Peter Jones <pjones@fedoraproject.org> - 2.02.01-1
- update to 1.02.02

* Wed Nov 09 2005 Jeremy Katz <katzj@fedoraproject.org> - 2.01.14-5
- add patch for xen block devices

* Sat Oct 15 2005 Florian La Roche <laroche@fedoraproject.org> - 2.01.14-4
- fix compile problems

* Thu Sep 15 2005 Jeremy Katz <katzj@fedoraproject.org> - 2.01.14-3
- the distro doesn't really work without a 2.6 kernel, so no need to
  require it

* Thu Aug 04 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.14-2
- fix changelog date

* Thu Aug 04 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.14-1
- A few more bug fixes.

* Wed Jul 13 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.13-1
- fix some bugs discovered in last release

* Tue Jun 14 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.12-3
- fix static build

* Tue Jun 14 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.12-2
- update dm dep

* Tue Jun 14 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.12-1
- A few more fixes since yesterday.

* Mon Jun 13 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.11-1
- New version upstream with a lot of fixes and enhancements.

* Wed Apr 27 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.08-3
- Add /etc/lvm

* Wed Apr 27 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.08-2
- No longer abort read operations if archive/backup directories aren't
  there. Add runtime directories and file to the package.

* Tue Mar 22 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.08-1
- Improve detection of external changes affecting internal cache. - Add
  clustered VG attribute. - Suppress rmdir opendir error message.

* Thu Mar 10 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.07-4
- And another compiler message.

* Thu Mar 10 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.07-3
- Suppress more compiler messages.

* Thu Mar 10 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.07-2
- suppress some new compiler messages

* Tue Mar 08 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.07-1
- Remove build directory from built-in path. Extra /dev scanning required
  for clustered operation.

* Thu Mar 03 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.06-1
- Allow anaconda to suppress warning messages.

* Fri Feb 18 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.05-1
- Upstream changes not affecting Fedora.

* Wed Feb 09 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.04-1
- Offset pool minors; lvm2cmd.so skips open fd check; pvmove -f gone.

* Tue Feb 01 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.03-1
- Fix snapshot device size & 64-bit display output.

* Fri Jan 21 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.02-1
- minor fixes

* Wed Jan 19 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.01-1
- Update vgcreate man page. Preparation for snapshot origin extension fix.

* Mon Jan 17 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.01.00-1
- Fix metadata auto-correction. Only request open_count when needed.

* Wed Jan 12 2005 Tim Waugh <twaugh@fedoraproject.org> - 2.00.33-2
- Rebuilt for new readline.

* Fri Jan 07 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.00.33-1
- wipe ext fs label; several clvm fixes

* Thu Jan 06 2005 Alasdair Kergon <agk@fedoraproject.org> - 2.00.32-2
- Remove temporary /sbin symlinks no longer needed. Include read-only pool
  support in the build.

* Wed Dec 22 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.32-1
- More fixes (143501).

* Sun Dec 12 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.31-1
- Fix pvcreate installer issues.

* Fri Dec 10 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.30-1
- Additional debugging code.

* Tue Nov 30 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.29-4
- Reinstate archs.

* Sun Nov 28 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.29-3
- Try excluding more archs

* Sat Nov 27 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.29-2
- Try without s390x which is failing.

* Sat Nov 27 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.29-1
- Fix last fix.

* Sat Nov 27 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.28-1
- Endian fix.

* Wed Nov 24 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.27-1
- Fix partition table detection & an out of memory segfault.

* Tue Nov 23 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.26-1
- Several installation-related fixes & man page updates.

* Mon Oct 25 2004 Elliot Lee <sopwith@fedoraproject.org> - 2.00.25-2
- Fix 2.6 kernel requirement

* Wed Sep 29 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.25-1
- Fix vgmknodes return code & vgremove locking.

* Fri Sep 17 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.24-2
- Obsolete old lvm1 packages; refuse install if running kernel 2.4. [bz
  128185]

* Thu Sep 16 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.24-1
- More upstream fixes & a couple of requested buildrequires.

* Wed Sep 15 2004 Alasdair Kergon <agk@fedoraproject.org> - 2.00.23-1
- Various minor upstream fixes. Support for 'make new-base'.

* Mon Aug 02 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.72-1
- merge f12 with rawhide

* Thu Jul 29 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02.53-3
- dist-git conversion

* Thu Nov 26 2009 Bill Nottingham <notting@fedoraproject.org> - 2.02.53-2
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Tue Sep 29 2009 Jesse Keating <jkeating@fedoraproject.org> - 2.02.53-1
- Initialize branch F-12 for lvm2

* Wed Jun 22 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-3
- Remove unused patch file for f14

* Fri May 06 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-2
- Add config options for systemd files

* Thu May 05 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-1
- Merge branch 'master' into f14

* Fri Oct 15 2010 Alasdair G Kergon <agk@redhat.com> - 2.02.73-2
- Support setting md uuid post-creation.

* Thu Sep 30 2010 Jesse Keating <jkeating@redhat.com> - 2.02.73-1
- Rebuilt for gcc bug 634757

* Wed Jul 23 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.108-1
- Update to latest lvm2 upstream release 2.02.108.

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.02.107-1
- fix license handling

* Thu Dec 24 2020 Robert Scheck <robert@fedoraproject.org> - 2.03.10-2
- Spec file cleanup and simplification

* Sun Aug 09 2020 Marian Csontos <mcsontos@redhat.com> - 2.03.10-1
- New upstream release v2.03.10

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 2.03.09-3
- Use make macros

* Tue May 26 2020 Miro Hrončok <miro@hroncok.cz> - 2.03.09-2
- Rebuilt for Python 3.9

* Thu Mar 26 2020 Marian Csontos <mcsontos@redhat.com> - 2.03.09-1
- New upstream release v2.03.09

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.03.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.07-1
- New upstream release v2.03.07

* Wed Oct 23 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.06-1
- New upstream release v2.03.06

* Wed Sep 18 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.05-5
- Fix invalid value warning in 11-dm-lvm.rules:40

* Tue Aug 27 2019 Adam Williamson <awilliam@redhat.com> - 2.03.05-4
- Backport fix for converting dbus.UInt to string in Python 3.8

* Mon Aug 19 2019 Miro Hrončok <miro@hroncok.cz> - 2.03.05-3
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.05-2
- Disable dlmcontrol until dlm is updated

* Wed Jul 31 2019 Marian Csontos <mcsontos@redhat.com> - 2.03.05-1
- New upstream release v2.03.05

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.185-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 13 2019 Marian Csontos <mcsontos@redhat.com> - 2.02.185-1
- New upstream release v2.02.185

* Mon Apr 01 2019 Marian Csontos <mcsontos@redhat.com> - 2.02.184-1
- New upstream release v2.02.184

* Thu Mar 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-6
- Remove obsolete scriptlets

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-5
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.183-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-3
- Remove obsolete Group tag

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.183-2
- Remove obsolete ldconfig scriptlets

* Fri Dec 07 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.183-1
- New upstream release v2.02.183

* Wed Oct 31 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.182-1
- New upstream release v2.02.182

* Tue Oct 02 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.181-2
- No %%ghost for dirs at tmpfiles.d

* Thu Aug 02 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.181-1
- New upstream release v2.02.181

* Thu Jul 19 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.180-1
- New upstream release v2.02.180

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.179-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-6
- Really bump release number

* Tue Jul 10 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-5
- Bump release number

* Tue Jul 10 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-4
- Remove python bindings

* Tue Jul 10 2018 Jason Tibbitts <tibbs@math.uh.edu> - 2.02.179-3
- Remove needless use of %%defattr

* Tue Jun 19 2018 Miro Hrončok <miro@hroncok.cz> - 2.02.179-2
- Rebuilt for Python 3.7

* Mon Jun 18 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.179-1
- New upstream release v2.02.179

* Wed Jun 13 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-5
- New upstream release v2.02.178

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-4
- Hide output of systemctl calls

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-3
- Fix commented out python_provide

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-2
- Forgot to run new-sources etc

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.178-1
- New upstream release v2.02.178-rc1

* Tue May 29 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.177-8
- Address Bug 1552971

* Wed Apr 04 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.177-7
- Remove python2 bindings

* Mon Mar 05 2018 Marian Csontos <mcsontos@redhat.com> - 2.02.177-6
- Add gcc and gcc-c++ to BuildRequires

* Wed Feb 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.177-5
- Remove %%clean section

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.02.177-4
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.177-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 2.02.177-2
- Update Python 2 dependency declarations to new packaging standards

* Tue Dec 19 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.177-1
- New upstream release v2.02.177

* Thu Dec 14 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.176-3
- Add and enable testsuite subpackage
- Escape percent signs in changelog

* Tue Dec 12 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.176-2
- Add epoch for easier downstream (el) rebuild.

* Fri Nov 03 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.176-1
- New upstream release v2.02.176

* Mon Oct 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.175-1
- New upstream release v2.02.175
- Fix D-Bus spelling, uncomment python_provide

* Mon Oct 02 2017 Troy Dawson <tdawson@redhat.com> - 2.02.174-2
- Bump to rebuild on rebuilt corosync

* Wed Sep 20 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.174-1
- New upstream release v2.02.174

* Wed Sep 06 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.173-5
- [WIP] Fix python subpackage names to follow guidelines

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.173-4
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.02.173-3
- Rebuild with fixed binutils for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.173-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.173-1
- New upstream release v2.02.173.

* Thu Jun 29 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.172-1
- New upstream release v2.02.172.

* Fri Jun 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-5
- Fix changelog

* Fri Jun 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-4
- Add patch for lvmdbusd

* Wed May 17 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-3
- Add patch for lvmdbusd

* Tue May 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-2
- Fix permissions on license files

* Tue May 09 2017 Marian Csontos <mcsontos@redhat.com> - 2.02.171-1
- New upstream release v2.02.171.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.168-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.02.168-3
- Rebuild for readline 7.x

* Mon Dec 19 2016 Miro Hrončok <miro@hroncok.cz> - 2.02.168-2
- Rebuild for Python 3.6

* Thu Dec 01 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.168-1
- New upstream release v2.02.168.

* Mon Nov 21 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-4
- Fix typo in lvm2 package description.

* Tue Nov 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-3
- Only log msg as debug if lvm2-lvmdbusd unit missing for D-Bus
  notification.

* Mon Nov 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-2
- New upstream release v2.02.167.

* Mon Nov 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.167-1
- New upstream release v2.02.167.

* Thu Oct 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.166-2
- Add various fixes for lvmdbusd from upcoming lvm2 version 2.02.167.

* Mon Sep 26 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.166-1
- New upstream release v2.02.166.

* Wed Sep 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.165-2
- Add new lvmraid.7 man page to lvm2 package

* Wed Sep 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.165-1
- New upstream release v2.02.165.

* Mon Aug 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.164-2
- Fix date in changelog

* Mon Aug 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.164-1
- New upstream release v2.02.164.

* Wed Aug 10 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.163-1
- New upstream release v2.02.163.

* Fri Jul 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.162-1
- New upstream release v2.02.162.

* Thu Jul 21 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.161-3
- Enable LVM notifications over dbus for lvmdbusd.

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.02.161-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Mon Jul 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.161-1
- New upstream release v2.02.161.

* Thu Jul 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.160-1
- New upstream release v2.02.160.

* Thu Jul 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.159-1
- New upstream release v2.02.159.

* Tue Jun 28 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.158-1
- New upstream release v2.02.158.

* Fri Jun 17 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.157-1
- New upstream release v2.02.157.

* Mon Jun 13 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.156-1
- New upstream release v2.02.156.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-4
- Fix regression in blkdeactivate script.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-3
- Fix regression in blkdeactivate script.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-2
- Fix regression in blkdeactivate script.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.155-1
- New upstream release v2.02.155.

* Mon Jun 06 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.154-2
- New upstream release v2.02.155.

* Mon May 16 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.154-1
- New upstream release v2.02.154.

* Tue May 10 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.153-1
- New upstream release v2.02.153.

* Mon May 02 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.152-1
- New upstream release v2.02.152.

* Mon Apr 25 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.151-1
- New upstream release v2.02.151.

* Mon Apr 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.150-1
- New upstream release v2.02.150.

* Mon Apr 04 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.149-3
- New upstream release v2.02.149.

* Mon Apr 04 2016 Peter Rajnoha <prajnoha@redhat.com>
- New upstream release v2.02.149.

* Tue Mar 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.148-1
- New upstream release v2.02.148.

* Mon Mar 21 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.147-1
- New upstream release v2.02.147.

* Fri Mar 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.146-2
- New upstream release v2.02.146.

* Fri Mar 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.146-1
- New upstream release v2.02.146.

* Wed Mar 09 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.145-2
- Require python3-gobject-base insetad of python3-gobject.

* Mon Mar 07 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.145-1
- New upstream release v2.02.145.

* Mon Feb 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.144-3
- Remove unneded patch.

* Mon Feb 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.144-2
- Require newer version of sanlock.

* Mon Feb 29 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.144-1
- New upstream release v2.02.144.

* Wed Feb 24 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-6
- Reinstate lvm2-lockd on all architectures as sanlock package is fixed
  now.

* Tue Feb 23 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-5
- Remove Requires: sanlock-lib for lvm2-lockd subpackage if sanlock not
  compiled.

* Tue Feb 23 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-4
- Build lvm2-lockd with sanlock support only on x86_64, arch64 and power64
  arch.

* Tue Feb 23 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-3
- Add Requires: python3-gobject for lvm2-dbusd subpackage.

* Mon Feb 22 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-2
- Patch lvm2 v2.02.143 Makefile for lvmdbusd.

* Mon Feb 22 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.143-1
- New upstream release v2.02.143 introducing LVM D-Bus daemon.

* Mon Feb 15 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.142-1
- New upstream release v2.02.142.

* Thu Feb 04 2016 Dennis Gilmore <dennis@ausil.us> - 2.02.141-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.141-1
- New upstream release v2.02.141.

* Mon Jan 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.140-2
- New upstream release v2.02.140.

* Mon Jan 18 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.140-1
- New upstream release v2.02.140.

* Mon Jan 11 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.139-1
- New upstream release v2.02.139.

* Mon Jan 04 2016 Peter Rajnoha <prajnoha@redhat.com> - 2.02.138-1
- New upstream release v2.02.138.

* Mon Dec 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.137-1
- New upstream release v2.02.137.

* Wed Dec 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.136-1
- New upstream release v2.02.136.

* Mon Nov 23 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.135-1
- New upstream release v2.02.135.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-5
- Changelog.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-4
- Changelog.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-3
- Bump version because of device-mapper not having a new release.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-2
- Bump version because of device-mapper not having a new release.

* Wed Nov 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.134-1
- New upstream release v2.02.134.

* Tue Nov 10 2015 Peter Robinson <pbrobinson@fedoraproject.org> - 2.02.133-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.133-2
- Shutdown lvmetad automatically after one hour of inactivity

* Fri Oct 30 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.133-1
- New upstream release v2.02.133.

* Mon Oct 26 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.132-2
- Remove %%epoch from cmirror package.

* Wed Sep 23 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.132-1
- New upstream release v2.02.132.

* Wed Sep 16 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.131-1
- New upstream release v2.02.131.

* Mon Sep 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.130-1
- New upstream release v2.02.130.

* Wed Sep 02 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.129-2
- Reinstate dm_task_get_info@Base to libdevmapper exports. (1.02.106)

* Thu Aug 27 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.129-1
- New upstream release v2.02.129.

* Tue Aug 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.128-2
- Pack cache-mq and cache-smq configuration profiles that appearead in
  v128.

* Tue Aug 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.128-1
- New upstream release v2.02.128.

* Mon Aug 10 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.127-1
- New upstream release v2.02.127.

* Mon Jul 27 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.126-2
- New upstream release v2.02.126.

* Mon Jul 27 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.126-1
- New upstream release v2.02.126.

* Tue Jul 14 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.125-2
- Remove Requires: fedora-release dependency, use system-release instead.

* Tue Jul 07 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.125-1
- New upstream release v2.02.125.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.124-3
- Remove extra tgz file that is uploaded already.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.124-2
- New upstream release v2.02.124.

* Fri Jul 03 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.124-1
- New upstream release v2.02.124.

* Wed Jul 01 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.123-1
- New upstream release v2.02.123.

* Mon Jun 22 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.122-1
- New upstream release v2.02.122.

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 2.02.120-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.120-2
- New upstream lvm2 release v2.02.120.

* Mon May 18 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.120-1
- New upstream lvm2 release v2.02.120.

* Mon May 04 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.119-2
- New upstream release v2.02.119.

* Mon May 04 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.119-1
- New upstream release v2.02.119.

* Tue Mar 24 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.118-2
- Update to latest upstream lvm2 release version 2.02.118.

* Tue Mar 24 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.118-1
- Update to latest upstream lvm2 release version 2.02.118.

* Fri Jan 30 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.116-1
- New upstream release.

* Thu Jan 29 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.115-2
- Fixes: use default cache mode when unset and add BuildRequires: device-
  mapper-persistent-data.

* Thu Jan 22 2015 Peter Rajnoha <prajnoha@redhat.com> - 2.02.115-1
- New upstream release with various fixes and enhancements.

* Fri Nov 28 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.114-1
- New upstream with fixes.

* Thu Nov 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.113-3
- Changelog.

* Thu Nov 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.113-2
- Add some fixes from upcoming lvm2 v2.02.114.

* Tue Nov 25 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.113-1
- New upstream bugfix release.

* Wed Nov 12 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.112-3
- Still the date in changelog.

* Wed Nov 12 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.112-2
- Fix date in changelog.

* Tue Nov 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.112-1
- Update to latest lvm2 upstream release v2.02.112.

* Mon Sep 01 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.111-1
- Update to latest lvm2 upstream release 2.02.111.

* Wed Aug 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.110-1
- New upstream release - lvm2 v2.02.110.

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 2.02.109-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.109-1
- Update to lvm2 upstream bug fix release 2.02.109.

* Wed Jul 23 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.108-1
- Update to latest lvm2 upstream release 2.02.108.

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.02.107-2
- fix license handling

* Tue Jun 24 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.107-1
- Update to latest lvm2 upstream release v2.02.107.

* Mon Jun 09 2014 Alasdair G Kergon <agk@redhat.com> - 2.02.106-6
- Fix spec file after mass rebuild script broke subpackage release tags.

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 2.02.106-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-4
- Remove obsolete lvm2-sysvinit subpackage.

* Thu Apr 24 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-3
- Always require the exact version for all LVM2 subpackages so all of them
  are synchronously updated.

* Fri Apr 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-2
- Update 'upstream' file.

* Fri Apr 11 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.106-1
- Update to latest upstream release lvm v2.02.106.

* Mon Jan 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-3
- Avoid exposing temporary devices when initializing thin pool volume.

* Mon Jan 27 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-2
- Remove handling of specific inappropriate mpath and cryptsetup events.

* Tue Jan 21 2014 Peter Rajnoha <prajnoha@redhat.com> - 2.02.105-1
- New upstream release (v2.02.105).

* Thu Jan 16 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.02.104-4
- Drop INSTALL from docs, escape percents in %%changelog.

* Fri Dec 13 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-3
- Require lvm2 pkg for lvm2-python-libs.

* Wed Dec 11 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-2
- Additional fix for SYSTEMD_READY env var assignment in lvmetad udev
  rules.

* Thu Nov 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.104-1
- New upstream release (v2.02.104).

* Wed Oct 30 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-7
- Additional fixes from upcoming v104 (related to udev).

* Fri Oct 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-6
- Fix changelog date.

* Fri Oct 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-5
- Additional fixes from upcoming v104.

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-4
- Add thin-performance.profile to lvm2 package.

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-3
- Modify patch that enables lvmetad for it to be applicable again (the
  lvm.conf context changed).

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-2
- Remove unused patch.

* Fri Oct 04 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.103-1
- New upstream release (v2.02.103).

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-5
- Add one more patch.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-4
- Update Source0 address.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-3
- Also increase device-mapper version.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-2
- A few more edits for lvm2 v2.02.102.

* Tue Sep 24 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.102-1
- New upstream release (lvm2 v2.02.102).

* Tue Aug 06 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-4
- Fix MDA offset/size overflow while using lvmetad and some spec file
  changes.

* Tue Jul 30 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-3
- Fix spec files %%define util-linux_version -> %%define util_linux_version
  for proper expansion

* Thu Jul 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-2
- remove items from changelog for patches already attached in previous
  builds as part of v2.02.98

* Thu Jul 25 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.99-1
- New upstream release (2.02.99)

* Thu May 30 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-16
- Do not include /lib/udev and /lib/udev/rules.d in device-mapper package.

* Tue May 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-15
- Additional lvmetad fixes.

* Tue May 14 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-14
- Add various fixes from upcoming lvm2 upstream release.

* Fri May 03 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-13
- Fix non-functional autoactivation of LVM volumes on top of MD devices.

* Fri Apr 19 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-12
- Autoactivate VG/LV on coldplug of DM-based PVs at boot.

* Tue Apr 09 2013 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-11
- Additional fixes for autoactivation feature.

* Thu Feb 14 2013 Dennis Gilmore <dennis@ausil.us> - 2.02.98-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-9
- Skip mlocking [vectors] on arm architecture.

* Sat Nov 17 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-8
- Exit pvscan --cache immediately if cluster locking used or lvmetad not
  used.

* Mon Nov 05 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-7
- Handle blank configure_cmirror and configure_cluster.

* Fri Nov 02 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-6
- Amendment to lvm2-2_02_99-various-updates-and-fixes-for-systemd-
  units.patch.

* Thu Nov 01 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-5
- lvmetad enabled by default, add lvm2-activation-generator and related
  fixes
- Add lvm2-activation-generator systemd generator to automatically systemd
  units to activate LVM2 volumes even if lvmetad is not This replaces lvm
  activation part of the former fedora-storage-init script that was
  included in the initscripts package before.
- Enable lvmetad - the LVM metadata daemon by default.
- Don't use lvmetad in lvm2-monitor.service ExecStop to avoid a systemd
  issue.
- Remove dependency on fedora-storage-init.service in lvm2 systemd units.
- Depend on lvm2-lvmetad.socket in lvm2-monitor.service systemd unit.
- Init lvmetad lazily to avoid early socket access on config overrides.
- Hardcode use_lvmetad=0 if cluster locking used and issue a warning  msg.
- Fix dm_task_set_cookie to properly process udev flags if udev_sync
  disabled.

* Sat Oct 20 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-4
- lvm2_spec.patch not needed

* Sat Oct 20 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-3
- Incorporate python-lvm pkg as lvm2-python-libs subpkg.

* Wed Oct 17 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-2
- Fix changelog header.

* Tue Oct 16 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.98-1
- New upstream release and spec file cleanup.

* Tue Aug 07 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.97-4
- tmpfiles.d isn't a config file when in lib

* Tue Aug 07 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.97-3
- another attempt to fix tmpfiles lib dir

* Tue Aug 07 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.97-2
- moved tmpfiles.d from etc to lib

* Tue Aug 07 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.97-1
- New upstream with bug fixes and improved thin support.

* Thu Jul 19 2012 Dennis Gilmore <dennis@ausil.us> - 2.02.96-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 04 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.96-5
- Further spec file cleanups.

* Wed Jul 04 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.96-4
- Fix spec file conditional for non-rawhide releases.

* Tue Jul 03 2012 Peter Rajnoha <prajnoha@redhat.com>
- Remove unused 'configure_default_data_alignment'.

* Mon Jul 02 2012 Peter Rajnoha <prajnoha@redhat.com>
- Clean up spec file, compile in lvmetad, autoactivation.

* Mon Jun 18 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.96-1
- New upstream, using device-mapper-persistent-data.

* Thu Jun 07 2012 Kay Sievers <kay@vrfy.org> - 2.02.95-26
- Remove Requires: libudev

* Tue Jun 05 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-25
- Use BuildRequires: systemd-devel instead of libudev-devel.

* Wed Apr 11 2012 Milan Broz <mbroz@redhat.com> - 2.02.95-24
- Build cluster only on x86_64 and i686 on RHEL.

* Thu Mar 29 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.95-23
- BuildRequires and Requires on newer version of corosync and dlm. -
  Restart clvmd on upgrades.

* Wed Mar 28 2012 Milan Broz <mbroz@redhat.com> - 2.02.95-22
- Restart clvmd on update.

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-21
- Do not strictly require openais for cmirror subpackage.

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-20
- Add F17 specific configure options (different corosync version).

* Mon Mar 19 2012 Peter Rajnoha <prajnoha@redhat.com> - 2.02.95-19
- Reinstate cmirror support and fixes for lvmetad udev rules/init scripts.

* Fri Mar 16 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.02.95-18
- Rebuild against new version of corosync (soname change) Bump Requires and
  BuildRequires on new corosync

* Fri Mar 09 2012 Milan Broz <mbroz@redhat.com> - 2.02.95-17
- Fix spec for non-cluster architectures.

* Thu Mar 08 2012 Peter Rajnoha <prajnoha@redhat.com>
- Reload dm-event systemd service on upgrade.

* Tue Mar 06 2012 Alasdair G Kergon <agk@redhat.com>
- New upstream with minor thinprov and name mangling fixes.

* Mon Mar 05 2012 Peter Rajnoha <prajnoha@redhat.com>
- Prepare hooks for lvmetad support.

* Sat Mar 03 2012 Alasdair G Kergon <agk@redhat.com>
- New upstream with many small fixes, some thin provisioning improvements
  and preparations for the new metadata daemon.

* Thu Feb 23 2012 Alasdair G Kergon <agk@redhat.com>
- fix build

* Thu Feb 23 2012 Alasdair G Kergon <agk@redhat.com>
- new upstream with minor fixes and tmpfiles dirs

* Mon Feb 20 2012 Alasdair G Kergon <agk@redhat.com>
- New upstream with a few fixes including encoding device names to restrict
  them to the udev characterset.

* Thu Feb 16 2012 Peter Rajnoha <prajnoha@redhat.com>
- Update udev requirement for F17+ to v176 at least (built-in blkid).

* Mon Feb 13 2012 Peter Rajnoha <prajnoha@redhat.com>
- Add configure --with-systemdsystemunitdir.

* Sun Feb 12 2012 Alasdair G Kergon <agk@redhat.com>
- New upstream with trivial fixes and refactoring of some lvmcache and
  orphan code.

* Wed Feb 01 2012 Alasdair G Kergon <agk@redhat.com>
- Try with dlm requirement

* Wed Feb 01 2012 Alasdair G Kergon <agk@redhat.com>
- A few little fixes and attempt to make it work with new version of
  corosync.

* Fri Jan 27 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.89-4
- reissued upstream release

* Fri Jan 27 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.89-3
- Reissued upstream release.

* Thu Jan 26 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.89-2
- Install thin monitoring

* Thu Jan 26 2012 Alasdair G Kergon <agk@redhat.com> - 2.02.89-1
- New upstream with experimental support for thinly-provisioned devices.

* Fri Jan 13 2012 Dennis Gilmore <dennis@ausil.us> - 2.02.88-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 30 2011 Peter Robinson <pbrobinson@gmail.com> - 2.02.88-3
- update util-linux-ng -> util-linux dependency as it changed long ago.

* Thu Dec 29 2011 Peter Robinson <pbrobinson@gmail.com> - 2.02.88-2
- update util-linux-ng -> util-linux

* Mon Aug 22 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.88-1
- New upstream - extend lvconvert raid1 support.

* Fri Aug 12 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.87-1
- New upstream release.

* Wed Aug 03 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-5
- Change DEFAULT_UDEV_SYNC to 1 so udev_sync is used even without any
  config.

* Thu Jul 28 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-4
- More systemd support.

* Wed Jul 20 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-3
- Fix broken lvm2-sysinit Requires: lvm2 dependency.

* Mon Jul 18 2011 Peter Rajnoha <prajnoha@redhat.com> - 2.02.86-2
- Convert form SysV init to systemd. Add systemd units and sysvinit
  subpackage.

* Fri Jul 08 2011 Alasdair G Kergon <agk@redhat.com> - 2.02.86-1
- New upstream with important snapshot+pvmove fixes.

* Wed Jun 22 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-6
- Rebuild with updated uname string test

* Wed Jun 22 2011 Zdenek Kabelac <zkabelac@redhat.com> - 2.02.84-5
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
