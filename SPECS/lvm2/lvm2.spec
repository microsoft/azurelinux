%global systemd_version 249

Summary:        Userland logical volume management tools
Name:           lvm2
Version:        2.03.15
Release:        1%{?dist}
License:        GPLv2 AND BSD 2-Clause AND LGPLv2.1
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://sourceware.org/lvm2/
Source0:        https://sourceware.org/pub/lvm2/LVM2.%{version}.tgz
Source1:        lvm2-activate.service
Patch0:         lvm2-set-default-preferred_names.patch
BuildRequires:  libaio-devel
BuildRequires:  libselinux-devel
BuildRequires:  libsepol-devel
BuildRequires:  ncurses-devel
BuildRequires:  python3-dbus
BuildRequires:  python3-devel
BuildRequires:  python3-pyudev
BuildRequires:  python3-setuptools
BuildRequires:  readline-devel
BuildRequires:  systemd-bootstrap-devel
Requires:       device-mapper = %{version}-%{release}
Requires:       device-mapper-event = %{version}-%{release}
Requires:       device-mapper-event-libs = %{version}-%{release}
Requires:       device-mapper-libs = %{version}-%{release}

%description
LVM2 includes all of the support for handling read/write operations on
physical volumes (hard disks, RAID-Systems, magneto optical, etc.,
multiple devices (MD), see mdadd(8) or even loop devices, see
losetup(8)), creating volume groups (kind of virtual disks) from one
or more physical volumes and creating one or more logical volumes
(kind of logical partitions) in volume groups.

%package dbusd
Summary: LVM2 D-Bus daemon
License: GPLv2
BuildArch: noarch
Requires: lvm2 >= %{version}-%{release}
Requires: dbus
Requires: python3-dbus
Requires: python3-gobject-base
Requires(post): systemd-units >= %{systemd_version}
Requires(preun): systemd-units >= %{systemd_version}
Requires(postun): systemd-units >= %{systemd_version}

%description dbusd

Daemon for access to LVM2 functionality through a D-Bus interface.

%package    devel
Summary:        Development libraries and headers
License:        LGPLv2
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       device-mapper-devel = %{version}-%{release}
Requires:       util-linux-devel

%description    devel
This package contains files needed to develop applications that use
the lvm2 libraries.

%package    libs
Summary:        Shared libraries for lvm2
License:        LGPLv2
Group:          System Environment/Libraries
Requires:       device-mapper-event-libs = %{version}-%{release}
Requires:       device-mapper-libs = %{version}-%{release}

%description    libs
This package contains shared lvm2 libraries for applications.

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%package -n device-mapper
Summary:        Device mapper utility
License:        GPLv2, BSD 2-Clause AND LGPLv2.1
Group:          System Environment/Base
URL:            http://sources.redhat.com/dm
Requires:       device-mapper-libs

%description -n device-mapper
This package contains the supporting userspace utility, dmsetup,
for the kernel device-mapper.

%package -n device-mapper-devel
Summary:        Development libraries and headers for device-mapper
License:        LGPLv2
Group:          Development/Libraries
Requires:       device-mapper = %{version}-%{release}
Requires:       libselinux-devel

%description -n device-mapper-devel
This package contains files needed to develop applications that use
the device-mapper libraries.

%package -n device-mapper-libs
Summary:        Device-mapper shared library
License:        LGPLv2
Group:          System Environment/Libraries
Requires:       libselinux
Requires:       libsepol

%description -n device-mapper-libs
This package contains the device-mapper shared library, libdevmapper.

%post -n device-mapper-libs -p /sbin/ldconfig
%postun -n device-mapper-libs -p /sbin/ldconfig

%package -n device-mapper-event
Summary:        Device-mapper event daemon
License:        GPLv2, BSD 2-Clause AND LGPLv2.1
Group:          System Environment/Base
Requires:       device-mapper = %{version}-%{release}
Requires:       device-mapper-event-libs = %{version}-%{release}

%description -n device-mapper-event
This package contains the dmeventd daemon for monitoring the state
of device-mapper devices.

%post -n device-mapper-event
%systemd_post dm-event.service dm-event.socket
if [ $1 -eq 1 ];then
    # This is initial installation
    systemctl start dm-event.socket
fi

%preun -n device-mapper-event
if [ $1 -eq 0 ];then
    # This is erase operation
    systemctl stop dm-event.socket
fi
%systemd_preun dm-event.service dm-event.socket

%postun -n device-mapper-event
%systemd_postun_with_restart dm-event.service dm-event.socket

%package -n device-mapper-event-libs
Summary:        Device-mapper event daemon shared library
License:        LGPLv2
Group:          System Environment/Libraries
Requires:       device-mapper-libs = %{version}-%{release}

%description -n device-mapper-event-libs
This package contains the device-mapper event daemon shared library,
libdevmapper-event.

%post -n device-mapper-event-libs -p /sbin/ldconfig
%postun -n device-mapper-event-libs -p /sbin/ldconfig

%package -n device-mapper-event-devel
Summary:        Development libraries and headers for the device-mapper event daemon
License:        LGPLv2
Group:          Development/Libraries
Requires:       device-mapper-devel = %{version}-%{release}
Requires:       device-mapper-event = %{version}-%{release}

%description -n device-mapper-event-devel
This package contains files needed to develop applications that use
the device-mapper event library.

%prep
%setup -q -n LVM2.%{version}
%patch0 -p1 -b .preferred_names

%build
%define _default_pid_dir /run
%define _default_dm_run_dir /run
%define _default_run_dir /run/lvm
%define _default_locking_dir /run/lock/lvm
%define _udevdir %{_libdir}/udev/rules.d

%configure \
    --prefix=%{_prefix} \
    --enable-applib \
    --enable-blkid_wiping \
    --enable-cmdlib \
    --enable-dbus-service --enable-notify-dbus \
    --enable-dmeventd \
    --enable-fsadm \
    --enable-lvm1_fallback \
    --enable-pkgconfig \
    --enable-write_install \
    --with-cache=internal \
    --with-cluster=internal --with-clvmd=none \
    --with-default-dm-run-dir=%{_default_dm_run_dir} \
    --with-default-locking-dir=%{_default_locking_dir} \
    --with-default-pid-dir=%{_default_pid_dir} \
    --with-default-run-dir=%{_default_run_dir} \
    --with-pool=internal \
    --with-thin=internal \
    --with-udevdir=%{_udevdir} --enable-udev_sync \
    --with-usrlibdir=%{_libdir}


make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
make install_system_dirs DESTDIR=%{buildroot}
make install_systemd_units DESTDIR=%{buildroot}
make install_systemd_generators DESTDIR=%{buildroot}
make install_tmpfiles_configuration DESTDIR=%{buildroot}
cp %{SOURCE1} %{buildroot}%{_libdir}/systemd/system/lvm2-activate.service

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable lvm2-activate.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-lvm2.preset
echo "disable lvm2-monitor.service" >> %{buildroot}%{_libdir}/systemd/system-preset/50-lvm2.preset

%preun
%systemd_preun lvm2-monitor.service lvm2-activate.service

%preun dbusd
%systemd_preun lvm2-lvmdbusd.service

%post
/sbin/ldconfig
%systemd_post lvm2-monitor.service lvm2-activate.service

%post dbusd
%systemd_post lvm2-lvmdbusd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart lvm2-monitor.service lvm2-activate.service

%postun dbusd
%systemd_postun lvm2-lvmdbusd.service

%files dbusd
%defattr(555,root,root,-)
%{_sbindir}/lvmdbusd
%defattr(444,root,root,-)
%{_sysconfdir}/dbus-1/system.d/com.redhat.lvmdbus1.conf
%{_datadir}/dbus-1/system-services/com.redhat.lvmdbus1.service
%{_mandir}/man8/lvmdbusd.8.gz
%{_unitdir}/lvm2-lvmdbusd.service
%{python3_sitelib}/lvmdbusd/*

%files devel
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/liblvm2cmd.so
%{_libdir}/libdevmapper-event-lvm2.so
%{_includedir}/lvm2cmd.h

%files libs
%defattr(-,root,root,-)
%{_libdir}/liblvm2cmd.so.*
%{_libdir}/libdevmapper-event-lvm2.so.*
%dir %{_libdir}/device-mapper
%{_libdir}/device-mapper/libdevmapper-event-lvm2mirror.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2snapshot.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2raid.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2thin.so
%{_libdir}/device-mapper/libdevmapper-event-lvm2vdo.so
%{_libdir}/libdevmapper-event-lvm2mirror.so
%{_libdir}/libdevmapper-event-lvm2snapshot.so
%{_libdir}/libdevmapper-event-lvm2raid.so
%{_libdir}/libdevmapper-event-lvm2thin.so
%{_libdir}/libdevmapper-event-lvm2vdo.so

%files -n device-mapper
%defattr(-,root,root,-)
%attr(555, -, -) %{_sbindir}/dmsetup
%{_sbindir}/dmstats
%{_mandir}/man8/dmsetup.8.gz
%{_mandir}/man8/dmstats.8.gz
%{_udevdir}/10-dm.rules
%{_udevdir}/13-dm-disk.rules
%{_udevdir}/95-dm-notify.rules

%files -n device-mapper-devel
%defattr(-,root,root,-)
%{_libdir}/libdevmapper.so
%{_includedir}/libdevmapper.h
%{_libdir}/pkgconfig/devmapper.pc

%files -n device-mapper-libs
%defattr(555,root,root,-)
%{_libdir}/libdevmapper.so.*

%files -n device-mapper-event
%defattr(-,root,root,-)
%attr(555, -, -) %{_sbindir}/dmeventd
%{_mandir}/man8/dmeventd.8.gz
%{_unitdir}/dm-event.socket
%{_unitdir}/dm-event.service

%files -n device-mapper-event-libs
%defattr(555,root,root,-)
%{_libdir}/libdevmapper-event.so.*

%files -n device-mapper-event-devel
%defattr(444,root,root,-)
%{_libdir}/libdevmapper-event.so
%{_includedir}/libdevmapper-event.h
%{_libdir}/pkgconfig/devmapper-event.pc

%files
%defattr(-,root,root)
%dir %{_sysconfdir}/lvm/backup
%dir %{_sysconfdir}/lvm/cache
%dir %{_sysconfdir}/lvm/archive
%{_udevdir}/11-dm-lvm.rules
%{_udevdir}/69-dm-lvm.rules
%{_sbindir}/blkdeactivate
%{_sbindir}/fsadm
%{_sbindir}/lv*
%exclude %{_sbindir}/lvmdbusd
%{_sbindir}/pv*
%{_sbindir}/vg*
%{_mandir}/man5/lvm.conf.5.gz
%{_mandir}/man7/lv*
%{_mandir}/man8/blkdeactivate.8.gz
%{_mandir}/man8/fsadm.8.gz
%{_mandir}/man8/lv*
%exclude %{_mandir}/man8/lvmdbusd.8.gz
%{_mandir}/man8/pv*
%{_mandir}/man8/vg*
%{_unitdir}/blk-availability.service
%{_unitdir}/lvm2-*
%exclude %{_unitdir}/lvm2-lvmdbusd.service
%{_libdir}/systemd/system-preset/50-lvm2.preset
%{_libdir}/tmpfiles.d/lvm2.conf
%dir %{_sysconfdir}/lvm
%attr(644, -, -) %config(noreplace) %{_sysconfdir}/lvm/lvm.conf
%config(noreplace) %{_sysconfdir}/lvm/lvmlocal.conf
%dir %{_sysconfdir}/lvm/profile
%{_sysconfdir}/lvm/profile/*
%ghost %{_sysconfdir}/lvm/cache/.cache

%changelog
* Fri Jan 05 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.03.15-1
- Auto-upgrade to 2.03.15 - none

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.03.15-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Apr 21 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.03.15-2
- Fix double-packaging of dbusd files in main package
- Remove manual pkgconfig provide

* Wed Feb 23 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.03.15-1
- Upgrading to newest version 2.03.15

* Fri Jan 07 2022 Thomas Crain <thcrain@microsoft.com> - 2.03.05-9
- Remove references to lvmetad (removed from upstream in 2.03.0)
- Bump required systemd version to 249
- Use non-FTP source URL
- Remove references to old patch files
- License verified

* Wed Sep 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.03.05-8
- Adding the 'lvm2-dbusd' package using Fedora 32 (license: MIT) specs as guidance.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.03.05-7
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Nov 03 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.03.05-6
- Systemd supports merged /usr. Update with corresponding file locations and macros.

*   Tue Jun 09 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.03.05-5
-   Remove systemd-bootstrap from Requires, which fixes chroot install issue. 

*   Fri May 29 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.03.05-4
-   Use systemd-bootstrap to break circular dependencies. 

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.03.05-3
-   Added %%license line automatically

*   Wed Apr 08 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.03.05-2
-   Remove thin-provisioning-tools from build requires.

*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 2.03.05-1
-   Update to 2.03.05. Fix URL. Fix Source0 URL. License verified.
-   Remove deprecated python bindings and lvm2app.
-   https://github.com/lvmteam/lvm2/issues/1

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.02.181-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.02.181-1
-   Update to version 2.02.181

*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.02.171-3
-   Disabled all lvm services by default

*   Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.02.171-2
-   Added python3 subpackage.

*   Thu May 4  2017 Bo Gan <ganb@vmware.com> 2.02.171-1
-   Update to 2.02.171

*   Wed Dec 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.02.141-8
-   device-mapper requires systemd.

*   Wed Nov 30 2016 Anish Swaminathan <anishs@vmware.com>  2.02.141-7
-   Start lvmetad socket with the service

*   Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com>  2.02.141-6
-   Change systemd dependency

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.02.141-5
-   GA - Bump release of all rpms

*   Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.02.141-4
-   Adding upgrade support in pre/post/un scripts.

*   Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 2.02.141-3
-   Fix post scripts for lvm

*   Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> 2.02.141-2
-   Adding device mapper event to Requires

*   Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  2.02.116-4
-   Change config file attributes.

*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  2.02.116-3
-   Add systemd to Requires and BuildRequires

*   Thu Sep 10 2015 Divya Thaluru <dthaluru@vmware.com> 2.02.116-2
-   Packaging systemd service and configuration files

*   Thu Feb 26 2015 Divya Thaluru <dthaluru@vmware.com> 2.02.116-1
-   Initial version
