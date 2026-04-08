## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
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
* Mon Apr 06 2026 azldev <> - 2.03.34-3
- Latest state for lvm2

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
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
