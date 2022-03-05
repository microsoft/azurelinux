%define release_number %(echo "%{release}" | cut -d. -f1)

Vendor:         Microsoft Corporation
Distribution:   Mariner
%define with_python2 0
%define with_python3 1
%define with_gtk_doc 1
%define with_bcache 1
%define with_btrfs 1
%define with_crypto 1
%define with_dm 1
%define with_loop 1
%define with_lvm 1
%define with_lvm_dbus 1
%define with_mdraid 1
%define with_mpath 1
%define with_swap 1
%define with_kbd 1
%define with_part 1
%define with_fs 1
%define with_nvdimm 1
%define with_vdo 0
%define with_gi 1
%define with_escrow 1
%define with_dmraid 1
%define with_tools 1

%define python2_copts --without-python2

# bcache is not available on RHEL
%if (0%{?rhel}) || %{with_bcache} == 0
%define with_bcache 0
%define bcache_copts --without-bcache
%endif

%if %{with_lvm_dbus} == 0
%define with_lvm_dbus 0
%define lvm_dbus_copts --without-lvm-dbus
%endif

# vdo is not available on non-x86_64 on older RHEL
%if (0%{?rhel} && 0%{?rhel} <= 7)
%ifnarch x86_64
%define with_vdo 0
%define vdo_copts --without-vdo
%endif
%endif

# btrfs is not available on RHEL > 7
%if 0%{?rhel} > 7 || %{with_btrfs} == 0
%define with_btrfs 0
%define btrfs_copts --without-btrfs
%endif

# dmraid is not available on RHEL > 7
%if 0%{?rhel} > 7
%define with_dmraid 0
%endif

%if %{with_btrfs} != 1
%define btrfs_copts --without-btrfs
%endif
%if %{with_crypto} != 1
%define crypto_copts --without-crypto
%else
%if %{with_escrow} != 1
%define crypto_copts --without-escrow
%endif
%endif
%if %{with_dm} != 1
%define dm_copts --without-dm
%else
%if %{with_dmraid} != 1
%define dm_copts --without-dmraid
%endif
%endif
%if %{with_loop} != 1
%define loop_copts --without-loop
%endif
%if %{with_lvm} != 1
%define lvm_copts --without-lvm
%endif
%if %{with_lvm_dbus} != 1
%define lvm_dbus_copts --without-lvm_dbus
%endif
%if %{with_mdraid} != 1
%define mdraid_copts --without-mdraid
%endif
%if %{with_mpath} != 1
%define mpath_copts --without-mpath
%endif
%if %{with_swap} != 1
%define swap_copts --without-swap
%endif
%if %{with_kbd} != 1
%define kbd_copts --without-kbd
%endif
%if %{with_part} != 1
%define part_copts --without-part
%endif
%if %{with_fs} != 1
%define fs_copts --without-fs
%endif
%if %{with_nvdimm} != 1
%define nvdimm_copts --without-nvdimm
%endif
%if %{with_vdo} != 1
%define vdo_copts --without-vdo
%endif
%if %{with_tools} != 1
%define tools_copts --without-tools
%endif
%if %{with_gi} != 1
%define gi_copts --disable-introspection
%endif

%define configure_opts %{?python2_copts} %{?python3_copts} %{?bcache_copts} %{?lvm_dbus_copts} %{?btrfs_copts} %{?crypto_copts} %{?dm_copts} %{?loop_copts} %{?lvm_copts} %{?lvm_dbus_copts} %{?mdraid_copts} %{?mpath_copts} %{?swap_copts} %{?kbd_copts} %{?part_copts} %{?fs_copts} %{?nvdimm_copts} %{?vdo_copts} %{?tools_copts} %{?gi_copts}

Name:        libblockdev
Version:     2.26
Release:     1%{?dist}
Summary:     A library for low-level manipulation with block devices
License:     LGPLv2+
URL:         https://github.com/storaged-project/libblockdev
Source0:     https://github.com/storaged-project/libblockdev/releases/download/%{version}-%{release_number}/%{name}-%{version}.tar.gz
Patch0:      0001-s390-Remove-double-fclose-in-bd_s390_dasd_online-204.patch

BuildRequires: make
BuildRequires: glib2-devel
%if %{with_gi}
BuildRequires: gobject-introspection-devel
%endif
%if %{with_python3}
BuildRequires: python3-devel
%endif
%if %{with_gtk_doc}
BuildRequires: gtk-doc
%endif
BuildRequires: glib2-doc
BuildRequires: autoconf-archive

# Needed for the escrow tests in tests/crypto_test.py, but not used to build
# BuildRequires: volume_key
# BuildRequires: nss-tools

# Needed for python 2 vs. 3 compatibility in the tests, but not used to build
# BuildRequires: python2-six
# BuildRequires: python3-six

%description
The libblockdev is a C library with GObject introspection support that can be
used for doing low-level operations with block devices like setting up LVM,
BTRFS, LUKS or MD RAID. The library uses plugins (LVM, BTRFS,...) and serves as
a thin wrapper around its plugins' functionality. All the plugins, however, can
be used as standalone libraries. One of the core principles of libblockdev is
that it is stateless from the storage configuration's perspective (e.g. it has
no information about VGs when creating an LV).

%package devel
Summary:     Development files for libblockdev
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description devel
This package contains header files and pkg-config files needed for development
with the libblockdev library.

%if %{with_python3}
%package -n python3-blockdev
Summary:     Python3 gobject-introspection bindings for libblockdev
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3-gobject-base
%{?python_provide:%python_provide python3-blockdev}

%description -n python3-blockdev
This package contains enhancements to the gobject-introspection bindings for
libblockdev in Python3.
%endif

%package utils
BuildRequires: kmod-devel
Summary:     A library with utility functions for the libblockdev library

%description utils
The libblockdev-utils is a library providing utility functions used by the
libblockdev library and its plugins.

%package utils-devel
Summary:     Development files for libblockdev-utils
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description utils-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-utils library.


%if %{with_btrfs}
%package btrfs
BuildRequires: libbytesize-devel
Summary:     The BTRFS plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
Requires: btrfs-progs

%description btrfs
The libblockdev library plugin (and in the same time a standalone library)
providing the BTRFS-related functionality.

%package btrfs-devel
Summary:     Development files for the libblockdev-btrfs plugin/library
Requires: %{name}-btrfs%{?_isa} = %{version}-%{release}
Requires: glib2-devel
Requires: %{name}-utils-devel%{?_isa}

%description btrfs-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-btrfs plugin/library.
%endif


%if %{with_crypto}
%package crypto
BuildRequires: cryptsetup-devel
BuildRequires: libblkid-devel

%if %{with_escrow}
BuildRequires: volume_key-devel >= 0.3.9-7
BuildRequires: nss-devel
%endif

Summary:     The crypto plugin for the libblockdev library

%description crypto
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to encrypted devices (LUKS).

%package crypto-devel
Summary:     Development files for the libblockdev-crypto plugin/library
Requires: %{name}-crypto%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description crypto-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-crypto plugin/library.
%endif


%if %{with_dm}
%package dm
BuildRequires: device-mapper-devel
%if %{with_dmraid}
BuildRequires: dmraid-devel
%endif
BuildRequires: systemd-devel
Summary:     The Device Mapper plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
Requires: device-mapper
%if %{with_dmraid}
Requires: dmraid
%endif

%description dm
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to Device Mapper.

%package dm-devel
Summary:     Development files for the libblockdev-dm plugin/library
Requires: %{name}-dm%{?_isa} = %{version}-%{release}
Requires: glib2-devel
Requires: device-mapper-devel
Requires: systemd-devel
%if %{with_dmraid}
Requires: dmraid-devel
%endif
Requires: %{name}-utils-devel%{?_isa}

%description dm-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-dm plugin/library.
%endif


%if %{with_fs}
%package fs
BuildRequires: parted-devel
BuildRequires: libblkid-devel
BuildRequires: libmount-devel
Summary:     The FS plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11

%description fs
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to operations with file systems.

%package fs-devel
Summary:     Development files for the libblockdev-fs plugin/library
Requires: %{name}-fs%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel
Requires: xfsprogs
Requires: dosfstools

%description fs-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-fs plugin/library.
%endif


%if %{with_kbd}
%package kbd
BuildRequires: libbytesize-devel
Summary:     The KBD plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
%if %{with_bcache}
Requires: bcache-tools >= 1.0.8
%endif

%description kbd
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to kernel block devices (namely zRAM and
Bcache).

%package kbd-devel
Summary:     Development files for the libblockdev-kbd plugin/library
Requires: %{name}-kbd%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description kbd-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-kbd plugin/library.
%endif


%if %{with_loop}
%package loop
Summary:     The loop plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11

%description loop
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to loop devices.

%package loop-devel
Summary:     Development files for the libblockdev-loop plugin/library
Requires: %{name}-loop%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description loop-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-loop plugin/library.
%endif


%if %{with_lvm}
%package lvm
BuildRequires: device-mapper-devel
Summary:     The LVM plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
Requires: lvm2

%description lvm
The libblockdev library plugin (and in the same time a standalone library)
providing the LVM-related functionality.

%package lvm-devel
Summary:     Development files for the libblockdev-lvm plugin/library
Requires: %{name}-lvm%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description lvm-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-lvm plugin/library.
%endif

%if %{with_lvm_dbus}
%package lvm-dbus
BuildRequires: device-mapper-devel
Summary:     The LVM plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 1.4
Requires: lvm2-dbusd >= 2.02.156

%description lvm-dbus
The libblockdev library plugin (and in the same time a standalone library)
providing the LVM-related functionality utilizing the LVM DBus API.

%package lvm-dbus-devel
Summary:     Development files for the libblockdev-lvm-dbus plugin/library
Requires: %{name}-lvm-dbus%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} >= 1.4
Requires: glib2-devel

%description lvm-dbus-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-lvm-dbus plugin/library.
%endif


%if %{with_mdraid}
%package mdraid
BuildRequires: libbytesize-devel
Summary:     The MD RAID plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
Requires: mdadm

%description mdraid
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to MD RAID.

%package mdraid-devel
Summary:     Development files for the libblockdev-mdraid plugin/library
Requires: %{name}-mdraid%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description mdraid-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-mdraid plugin/library.
%endif


%if %{with_mpath}
%package mpath
BuildRequires: device-mapper-devel
Summary:     The multipath plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
Recommends: device-mapper-multipath

%description mpath
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to multipath devices.

%package mpath-devel
Summary:     Development files for the libblockdev-mpath plugin/library
Requires: %{name}-mpath%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description mpath-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-mpath plugin/library.
%endif

%if %{with_nvdimm}
%package nvdimm
BuildRequires: ndctl-devel
BuildRequires: libuuid-devel
Summary:     The NVDIMM plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
Requires: ndctl

%description nvdimm
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to operations with NVDIMM devices.

%package nvdimm-devel
Summary:     Development files for the libblockdev-nvdimm plugin/library
Requires: %{name}-nvdimm%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description nvdimm-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-nvdimm plugin/library.
%endif


%if %{with_part}
%package part
BuildRequires: parted-devel
Summary:     The partitioning plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
Requires: gdisk
Requires: util-linux

%description part
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to partitioning.

%package part-devel
Summary:     Development files for the libblockdev-part plugin/library
Requires: %{name}-part%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description part-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-part plugin/library.
%endif


%if %{with_swap}
%package swap
BuildRequires: libblkid-devel
Summary:     The swap plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11
Requires: util-linux

%description swap
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to swap devices.

%package swap-devel
Summary:     Development files for the libblockdev-swap plugin/library
Requires: %{name}-swap%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description swap-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-swap plugin/library.
%endif


%if %{with_vdo}
%package vdo
BuildRequires: libbytesize-devel
BuildRequires: libyaml-devel
Summary:     The vdo plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} >= 0.11

# weak dependencies doesn't work on older RHEL
%if (0%{?rhel} && 0%{?rhel} <= 7)
Requires: vdo
Requires: kmod-kvdo
%else
# we want to build the plugin everywhere but the dependencies might not be
# available so just use weak dependency
Recommends: vdo
Recommends: kmod-kvdo
%endif

%description vdo
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to VDO devices.

%package vdo-devel
Summary:     Development files for the libblockdev-vdo plugin/library
Requires: %{name}-vdo%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description vdo-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-vdo plugin/library.
%endif

%if %{with_tools}
%package tools
Summary:    Various nice tools based on libblockdev
Requires:   %{name}
Requires:   %{name}-lvm
BuildRequires: libbytesize-devel
%if %{with_lvm_dbus} == 1
Recommends: %{name}-lvm-dbus
%endif

%description tools
Various nice storage-related tools based on libblockdev.

%endif

%ifarch s390 s390x
%package s390
Summary:    The s390 plugin for the libblockdev library
Requires: s390utils

%description s390
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to s390 devices.

%package s390-devel
Summary:     Development files for the libblockdev-s390 plugin/library
Requires: %{name}-s390%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa}
Requires: glib2-devel

%description s390-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-s390 plugin/library.
%endif

%package plugins-all
Summary:     Meta-package that pulls all the libblockdev plugins as dependencies
Requires: %{name}%{?_isa} = %{version}-%{release}

%if %{with_btrfs}
Requires: %{name}-btrfs%{?_isa} = %{version}-%{release}
%endif

%if %{with_crypto}
Requires: %{name}-crypto%{?_isa} = %{version}-%{release}
%endif

%if %{with_dm}
Requires: %{name}-dm%{?_isa} = %{version}-%{release}
%endif

%if %{with_fs}
Requires: %{name}-fs%{?_isa} = %{version}-%{release}
%endif

%if %{with_kbd}
Requires: %{name}-kbd%{?_isa} = %{version}-%{release}
%endif

%if %{with_loop}
Requires: %{name}-loop%{?_isa} = %{version}-%{release}
%endif

%if %{with_lvm}
Requires: %{name}-lvm%{?_isa} = %{version}-%{release}
%endif

%if %{with_mdraid}
Requires: %{name}-mdraid%{?_isa} = %{version}-%{release}
%endif

%if %{with_mpath}
Requires: %{name}-mpath%{?_isa} = %{version}-%{release}
%endif

%if %{with_nvdimm}
Requires: %{name}-nvdimm%{?_isa} = %{version}-%{release}
%endif

%if %{with_part}
Requires: %{name}-part%{?_isa} = %{version}-%{release}
%endif

%if %{with_swap}
Requires: %{name}-swap%{?_isa} = %{version}-%{release}
%endif

%if %{with_vdo}
Requires: %{name}-vdo%{?_isa} = %{version}-%{release}
%endif

%ifarch s390 s390x
Requires: %{name}-s390%{?_isa} = %{version}-%{release}
%endif

%description plugins-all
A meta-package that pulls all the libblockdev plugins as dependencies.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
autoreconf -ivf
%configure %{?configure_opts}
%{__make} %{?_smp_mflags}

%install
%{make_install}
find %{buildroot} -type f -name "*.la" | xargs %{__rm}


%ldconfig_scriptlets
%ldconfig_scriptlets utils

%if %{with_btrfs}
%ldconfig_scriptlets btrfs
%endif

%if %{with_crypto}
%ldconfig_scriptlets crypto
%endif

%if %{with_dm}
%ldconfig_scriptlets dm
%endif

%if %{with_fs}
%ldconfig_scriptlets fs
%endif

%if %{with_loop}
%ldconfig_scriptlets loop
%endif

%if %{with_lvm}
%ldconfig_scriptlets lvm
%endif

%if %{with_lvm_dbus}
%ldconfig_scriptlets lvm-dbus
%endif

%if %{with_mdraid}
%ldconfig_scriptlets mdraid
%endif

%if %{with_mpath}
%ldconfig_scriptlets mpath
%endif

%if %{with_nvdimm}
%ldconfig_scriptlets nvdimm
%endif

%if %{with_part}
%ldconfig_scriptlets part
%endif

%if %{with_swap}
%ldconfig_scriptlets swap
%endif

%if %{with_vdo}
%ldconfig_scriptlets vdo
%endif

%ifarch s390 s390x
%ldconfig_scriptlets s390
%endif

%if %{with_kbd}
%ldconfig_scriptlets kbd
%endif


%files
%license LICENSE
%{_libdir}/libblockdev.so.*
%if %{with_gi}
%{_libdir}/girepository*/BlockDev*.typelib
%endif
%dir %{_sysconfdir}/libblockdev
%dir %{_sysconfdir}/libblockdev/conf.d
%config %{_sysconfdir}/libblockdev/conf.d/00-default.cfg

%files devel
%doc features.rst specs.rst
%{_libdir}/libblockdev.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/blockdev.h
%{_includedir}/blockdev/plugins.h
%{_libdir}/pkgconfig/blockdev.pc
%if %{with_gtk_doc}
%{_datadir}/gtk-doc/html/libblockdev
%endif
%if %{with_gi}
%{_datadir}/gir*/BlockDev*.gir
%endif

%if %{with_python3}
%files -n python3-blockdev
%{python3_sitearch}/gi/overrides/BlockDev*
%{python3_sitearch}/gi/overrides/__pycache__/BlockDev*
%endif

%files utils
%{_libdir}/libbd_utils.so.*
%{_libdir}/libbd_part_err.so.*

%files utils-devel
%{_libdir}/libbd_utils.so
%{_libdir}/libbd_part_err.so
%{_libdir}/pkgconfig/blockdev-utils.pc
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/utils.h
%{_includedir}/blockdev/sizes.h
%{_includedir}/blockdev/exec.h
%{_includedir}/blockdev/extra_arg.h
%{_includedir}/blockdev/dev_utils.h
%{_includedir}/blockdev/module.h
%{_includedir}/blockdev/dbus.h


%if %{with_btrfs}
%files btrfs
%{_libdir}/libbd_btrfs.so.*

%files btrfs-devel
%{_libdir}/libbd_btrfs.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/btrfs.h
%endif


%if %{with_crypto}
%files crypto
%{_libdir}/libbd_crypto.so.*

%files crypto-devel
%{_libdir}/libbd_crypto.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/crypto.h
%endif


%if %{with_dm}
%files dm
%{_libdir}/libbd_dm.so.*

%files dm-devel
%{_libdir}/libbd_dm.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/dm.h
%endif


%if %{with_fs}
%files fs
%{_libdir}/libbd_fs.so.*

%files fs-devel
%{_libdir}/libbd_fs.so
%dir %{_includedir}/blockdev
%dir %{_includedir}/blockdev/fs
%{_includedir}/blockdev/fs.h
%{_includedir}/blockdev/fs/*.h
%endif


%if %{with_kbd}
%files kbd
%{_libdir}/libbd_kbd.so.*

%files kbd-devel
%{_libdir}/libbd_kbd.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/kbd.h
%endif


%if %{with_loop}
%files loop
%{_libdir}/libbd_loop.so.*

%files loop-devel
%{_libdir}/libbd_loop.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/loop.h
%endif


%if %{with_lvm}
%files lvm
%{_libdir}/libbd_lvm.so.*

%files lvm-devel
%{_libdir}/libbd_lvm.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/lvm.h
%endif


%if %{with_lvm_dbus}
%files lvm-dbus
%{_libdir}/libbd_lvm-dbus.so.*
%config %{_sysconfdir}/libblockdev/conf.d/10-lvm-dbus.cfg

%files lvm-dbus-devel
%{_libdir}/libbd_lvm-dbus.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/lvm.h
%endif


%if %{with_mdraid}
%files mdraid
%{_libdir}/libbd_mdraid.so.*

%files mdraid-devel
%{_libdir}/libbd_mdraid.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/mdraid.h
%endif


%if %{with_mpath}
%files mpath
%{_libdir}/libbd_mpath.so.*

%files mpath-devel
%{_libdir}/libbd_mpath.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/mpath.h
%endif


%if %{with_nvdimm}
%files nvdimm
%{_libdir}/libbd_nvdimm.so.*

%files nvdimm-devel
%{_libdir}/libbd_nvdimm.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/nvdimm.h
%endif


%if %{with_part}
%files part
%{_libdir}/libbd_part.so.*

%files part-devel
%{_libdir}/libbd_part.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/part.h
%endif


%if %{with_swap}
%files swap
%{_libdir}/libbd_swap.so.*

%files swap-devel
%{_libdir}/libbd_swap.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/swap.h
%endif


%if %{with_vdo}
%files vdo
%{_libdir}/libbd_vdo.so.*

%files vdo-devel
%{_libdir}/libbd_vdo.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/vdo.h
%endif

%if %{with_tools}
%files tools
%{_bindir}/lvm-cache-stats
%endif

%ifarch s390 s390x
%files s390
%{_libdir}/libbd_s390.so.*

%files s390-devel
%{_libdir}/libbd_s390.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/s390.h
%endif

%files plugins-all

%changelog
* Fri Mar 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.26-1
- Updating to version 2.26 using Fedora 36 spec (license: MIT) for guidance.
- License verified.

* Mon Mar 16 2021 Henry Li <lihl@microsoft.com> - 2.24-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable python2 build and enable python3 build

* Thu Sep 17 2020 Vojtech Trefny <vtrefny@redhat.com> - 2.24-2
- exec: Fix setting locale for util calls

* Fri May 22 2020 Vojtech Trefny <vtrefny@redhat.com> - 2.24-1
- Mark VDO plugin as deprecated since 2.24 (vtrefny)
- Fix multiple uninitialized values discovered by coverity (vtrefny)
- fs: Fix potential NULL pointer dereference in mount.c (vtrefny)
- utils: Remove deadcode in exec.c (vtrefny)
- Do not check VDO saving percent value in LVM DBus tests (vtrefny)
- Use libblkid to get label and UUID for XFS filesystems (vtrefny)
- Do not open devices as read-write for read-only fs operations (vtrefny)
- Create a common function to get label and uuid of a filesystem (vtrefny)
- lvm: Fix getting cache stats for cache thinpools (vtrefny)
- Do not skip LVM VDO tests when the kvdo module is already loaded (vtrefny)
- tests: Skip LVM VDO tests if kvdo module cannot be loaded (vtrefny)
- lvm-dbus: Add LVM VDO pools to bd_lvm_lvs (vtrefny)
- lvm: Add a function to get VDO pool name for a VDO LV (vtrefny)
- lvm-dbus: Get data LV name for LVM VDO pools too (vtrefny)
- Add functions to get VDO stats for LVM VDO volumes (vtrefny)
- Move VDO statistics code to a separate file (vtrefny)
- Fix copy-paste bug in lvm.api (vtrefny)
- exec: Disable encoding when reading data from stdout/stderr (vtrefny)
- Add function to get LVM VDO write policy from a string (vtrefny)
- Add extra parameters for creating LVM VDO volumes (vtrefny)
- Allow calling LVM functions without locking global_config_lock (vtrefny)
- Fix getting VDO data in the LVM DBus plugin (vtrefny)
- Fix getting string representation of unknown VDO state index (vtrefny)
- Add write policy and index size to LVM VDO data (vtrefny)
- Fix converting to VDO pool without name for the VDO LV (vtrefny)
- Add some helper functions to get LVM VDO mode and state strings (vtrefny)
- Add support for creating and managing VDO LVs with LVM (vtrefny)
- Fix LVM plugin so names in tests (vtrefny)
- Do not hardcode pylint executable name in Makefile (vtrefny)
- Add a function to check if a tool supports given feature (vtrefny)
- configure.ac: Avoid more bashisms (gentoo)
- mount: Fix a memleak (tbzatek)
- exec: Fix a memleak (tbzatek)
- vdo: Fix a memleak (tbzatek)
- configure.ac: Avoid bashisms (polynomial-c)
- tests: Specify loader for yaml.load in VDO tests (vtrefny)
- lvm-dbus: Fix memory leak in bd_lvm_thlvpoolname (vtrefny)
- lvm-dbus: Do not activate LVs during pvscan --cache (vtrefny)
- vdo: Run "vdo create" with "--force" (vtrefny)
- Fix typo in (un)mount error messages (vtrefny)
- utils: Add functions to get and check current linux kernel version (tbzatek)
- ext: Return empty string instead of "<none>" for empty UUID (vtrefny)
- Add support for BitLocker encrypted devices using cryptsetup (vtrefny)
- Add a helper function for closing an active crypto device (vtrefny)
- Manually remove symlinks not removed by udev in tests (vtrefny)
- Fix memory leak in LVM DBus plugin (vtrefny)
- Fix expected cache pool name with newest LVM (vtrefny)
- fs: Fix checking for UID/GID == 0 (vtrefny)
- Fixed a number of memory leaks in lvm-dbus plugin (mthompson)
- exec.c: Fix reading outputs with null bytes (vtrefny)
- Fix linking against utils on Debian (vtrefny)
- Add new function 'bd_fs_wipe_force' to control force wipe (vtrefny)
- Use 'explicit_bzero' to erase passphrases from key files (vtrefny)
- Sync spec with downstream (vtrefny)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Vojtech Trefny <vtrefny@redhat.com> - 2.23-1
- Fix how we get process exit code from g_spawn_sync (vtrefny)
- Skip tests for old-style LVM snapshots on recent Fedora (vtrefny)
- Fix skipping NTFS read-only test case on systems without NTFS (vtrefny)
- Fix LVM_MAX_LV_SIZE in the GIR file (vtrefny)
- Print skipped test "results" to stderr instead of stdout (vtrefny)
- Move the NTFS read-only device test to a separate test case (vtrefny)
- Fix parsing distro version from CPE name (vtrefny)
- Use 'kmod_module_probe_insert_module' function for loading modules (vtrefny)
- Hide filesystem-specific is_tech_available functions (vtrefny)
- Mark LVM global config locks as static (vtrefny)
- Remove unused 'get_PLUGIN_num_functions' and 'get_PLUGIN_functions' functions (vtrefny)
- Mark 'private' plugin management functions as static (vtrefny)
- Ignore coverity deadcode warning in 'bd_fs_is_tech_avail' (vtrefny)
- Ignore coverity deadcode warnings in the generated code (vtrefny)
- Use the new config file for skipping tests (vtrefny)
- Skip bcache tests if make-bcache is not installed (vtrefny)
- Add ability to read tests to skip from a config file (vtrefny)
- Mark 'test_set_bitmap_location' as unstable (vtrefny)
- Force LVM cli plugin in lvm_test (vtrefny)
- Add a special test tag for library tests that recompile plugins (vtrefny)
- Allow running tests against installed libblockdev (vtrefny)
- Remove duplicate test case (vtrefny)
- Use the new test tags in tests (vtrefny)
- Use test tags for skipping tests (vtrefny)
- Add a decorator for "tagging" tests (vtrefny)
- Add function for (un)freezing filesystems (vtrefny)
- Add a function to check whether a path is a mounpoint or not (vtrefny)
- Skip bcache tests on all Debian versions (vtrefny)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.22-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Vojtech Trefny <vtrefny@redhat.com> - 2.22-1
- tests: Fix Debian testing "version" for skipping (vtrefny)
- module: Fix libkmod related leak (tbzatek)
- btrfs: Fix number of memory leaks (tbzatek)
- mdraid: Fix leaking BDMDExamineData.metadata (tbzatek)
- mdraid: Fix leaking error (tbzatek)
- part: Fix leaking string in args (tbzatek)
- ext: Fix leaking string (tbzatek)
- part: Fix leaking objects (tbzatek)
- kbd: Fix g_match_info_fetch() leaks (tbzatek)
- ext: Fix g_match_info_fetch() leaks (tbzatek)
- ext: Fix g_strsplit() leaks (tbzatek)
- s390: Fix g_strsplit() leaks (tbzatek)
- mdraid: Fix g_strsplit() leaks (tbzatek)
- exec: Fix some memory leaks (tbzatek)
- lvm: Fix leaking BDLVMPVdata.vg_uuid (tbzatek)
- lvm: Use g_ptr_array_free() for creating lists (tbzatek)
- lvm: Fix some obvious memory leaks (tbzatek)
- Remove device-mapper-multipath dependency from fs and part plugins (vtrefny)
- bd_fs_xfs_get_info: Allow passing error == NULL (tbzatek)
- tests: Fix removing targetcli lun (vtrefny)
- Use existing cryptsetup API for changing keyslot passphrase (vtrefny)
- New function to get supported sector sizes for NVDIMM namespaces (vtrefny)
- Allow skiping tests only based on architecture (vtrefny)
- Sync spec file with python2 obsoletion added downstream (awilliam)
- Sync spec with downstream (vtrefny)

* Tue Apr 16 2019 Vojtech Trefny <vtrefny@redhat.com> - 2.21-3
- Remove device-mapper-multipath dependency from fs and part plugins

* Thu Feb 28 2019 Adam Williamson <awilliam@redhat.com> - 2.21-2
- Obsolete the python2 subpackage if we're not building it

* Thu Feb 21 2019 Vojtech Trefny <vtrefny@redhat.com> - 2.21-1
- Fix checking swap status on lvm/md (vtrefny)
- tests: Stop skipping some tests on Debian testing (vtrefny)
- tests: Remove some old/irrelevant skips (vtrefny)
- Use 512bit keys in LUKS by default (vratislav.podzimek)
- Add 'autoconf-archive' to build requires (vtrefny)
- vagrant: remove F27 and add F29 (vtrefny)
- vagrant: install 'autoconf-archive' on Ubuntu (vtrefny)
- Enable cryptsetup debug messages when compiled using --enable-debug (vtrefny)
- lvm-dbus: Do not pass extra arguments enclosed in a tuple (vtrefny)
- crypto: Do not try to use keyring on systems without keyring support (vtrefny)
- Fix LUKS2 resize password test (vtrefny)
- Use cryptsetup to check LUKS2 label (vtrefny)
- Skip LUKS2+integrity test on systems without dm-integrity module (vtrefny)
- Add custom error message for wrong passphrase for open (vtrefny)
- Use major/minor macros from sys/sysmacros.h instead of linux/kdev_t.h (vtrefny)
- crypto_test.py: Use blkid instead of lsblk to check luks label (vtrefny)
- Skip VDO grow physical test (vtrefny)
- Add libblkid-devel as a build dependency for the swap plugin (vtrefny)
- Add error codes and Python exceptions for swapon fails (vtrefny)
- Use libblkid to check swap status before swapon (vtrefny)
- Add a new subpackage with the tool(s) (v.podzimek)
- Document what the 'tools' directory contains (v.podzimek)
- Make building tools optional (v.podzimek)
- Add a tool for getting cached LVM statistics (v.podzimek)
- Discard messages from libdevmapper in the LVM plugins (v.podzimek)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 08 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.20-2
- Use libblkid to check swap status before swapon (vtrefny)
- Add error codes and Python exceptions for swapon fails (vtrefny)

* Wed Sep 26 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.20-1
- Use unsafe caching for storage for devel/testing VMs (v.podzimek)
- Require newer version of cryptsetup for LUKS2 tests (vtrefny)
- Skip nvdimm tests on systems without ndctl (vtrefny)
- Add Ubuntu 18.04 VM configuration to the vagrant template (vtrefny)
- Add some missing test dependencies to the vagrant template (vtrefny)
- Fix how/where the bcache tests are skipped (v.podzimek)
- Document what the 'misc' directory contains (v.podzimek)
- Add a Vagrantfile template (v.podzimek)
- Fix the error message when deleting partition fails (vpodzime)
- Fix build of plugins by changing linking order (devurandom)
- Fix how we check zram stats from /sys/block/zram0/stat (vtrefny)
- lvm-dbus: Fix parsing extra arguments for LVM methods calls (vtrefny)
- Skip MDTestAddRemove on Debian (vtrefny)
- Skip NTFS mount test on Debian testing (vtrefny)
- Skip bcache tests on Debian testing (vtrefny)
- tests: Try harder to get distribution version (vtrefny)
- Mark the function stubs as static (v.podzimek)
- Build the dm plugin without dmraid support on newer RHEL (vtrefny)
- Fix skipping zram tests on Fedora 27 (vtrefny)
- kbd: Check for zram module availability in 'bd_kbd_is_tech_avail' (vtrefny)
- Always build the VDO plugin (vtrefny)
- Do not require 'dmraid' package if built without dmraid support (vtrefny)
- Fix licence header in dbus.c (vtrefny)
- Fix spacing in NEWS.rst (vtrefny)

* Fri Aug 10 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.19-1
- Use python interpreter explicitly when running boilerplate_generator.py (vtrefny)
- vdo: Implement bd_vdo_get_stats() (tbzatek)
- Add test for is_tech_available with multiple dependencies (vtrefny)
- lvm-dbus.c: Check for 'lvmdbus' dependency in 'bd_lvm_is_tech_avail' (vtrefny)
- lvm.c: Check for 'lvm' dependency in 'bd_lvm_is_tech_avail' (vtrefny)
- Fix licence headers in sources (vtrefny)
- Fix three memory leaks in lvm-dbus.c (vtrefny)
- Ignore "bad-super-call" pylint warning in BlockDev.py (vtrefny)
- Fix running pylint in tests (vtrefny)
- Fix vdo configuration options definition in spec file (vtrefny)
- Fix calling BlockDev.reinit in swap tests (vtrefny)
- Fix how we check zram stats from /sys/block/zram0/mm_stat (vtrefny)
- Skip VDO tests also when the 'kvdo' module is not available (vtrefny)
- Add version to tests that should be skipped on CentOS/RHEL 7 (vtrefny)
- Skip btrfs tests if btrfs module is not available (vtrefny)
- Do not build KBD plugin with bcache support on RHEL (vtrefny)
- Do not build btrfs plugin on newer RHEL (vtrefny)
- fs: Properly close both ends of the pipe (tbzatek)
- Make sure library_test works after fixing -Wstrict-prototypes (vtrefny)
- Make sure library tests properly clean after themselves (vtrefny)
- pkg-config: add -L${libdir} and -I${includedir} (max.kellermann)
- plugins/kbd: make wait_for_file() static (max.kellermann)
- plugins/lvm{,-dbus}: get_lv_type_from_flags() returns const string (max.kellermann)
- plugins/dm: add explicit cast to work around -Wdiscarded-qualifiers (max.kellermann)
- plugins/crypto: work around -Wdiscarded-qualifiers (max.kellermann)
- plugins/check_deps: make all strings and `UtilDep` instances `const` (max.kellermann)
- exec: make `msg` parameters const (max.kellermann)
- fix -Wstrict-prototypes (max.kellermann)
- module.c: Accept kernel modules if they are built-in (marco.guerri.dev)
- BlockDev.py Convert dictionary keys to set before using them (vtrefny)
- Skip 'test_cache_pool_create_remove' on CentOS 7 (vtrefny)
- Re-order libbd_crypto_la_LIBADD to fix libtool issue (tom)
- acinclude.m4: Use AS_EXIT to fail in LIBBLOCKDEV_FAILURES (vtrefny)
- configure.ac: Fix missing parenthesis in blkid version check (vtrefny)
- Allow specifying extra options for PBKDF when creating LUKS2 (vtrefny)
- Reintroduce python2 support for Fedora 29 (vtrefny)
- Use versioned command for Python 2 (vtrefny)
- Fix few wrong names in doc strings (vtrefny)
- Make sure all our free and copy functions work with NULL (vtrefny)
- Use libblkid in bd_crypto_is_luks (vtrefny)
- vdo: Properly destroy the yaml parser (tbzatek)
- Add a simple test case for bd_crypto_tc_open (vtrefny)
- Add Python override for bd_crypto_tc_open_full (vtrefny)
- Show simple summary after configure (vtrefny)
- Do not build VDO plugin on non-x86_64 architectures (vtrefny)
- Sync spec with downstream (vtrefny)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.18-3
- Reitroduce python2 support for Fedora 29

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.18-2
- Rebuilt for Python 3.7

* Wed Jun 20 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.18-1
- Add VDO to features.rst (vtrefny)
- Remove roadmap.rst (vtrefny)
- vdo: Add tests for bd_vdo_grow_physical() (tbzatek)
- Do not try to build VDO plugin on Fedora (vtrefny)
- Introduce reporting function per thread (kailueke)
- vdo: Implement bd_vdo_grow_physical() (tbzatek)
- Correct arguments for ext4 repair with progress (kailueke)
- Clarify that checking an RW-mounted XFS file system is impossible (v.podzimek)
- vdo: Resolve real device file path (tbzatek)
- Adjust to new NVDIMM namespace modes (vtrefny)
- Use xfs_repair instead of xfs_db in bd_fs_xfs_check() (v.podzimek)
- Allow compiling libblockdev without libdmraid (vtrefny)
- Only require plugins we really need in LVM dbus tests (vtrefny)
- Add tests for VDO plugin (vtrefny)
- Add decimal units definition to utils/sizes.h (vtrefny)
- Add basic VDO plugin functionality (vtrefny)
- Add the VDO plugin (vtrefny)
- Always check for error when (un)mounting (vtrefny)
- Fix off-by-one error when counting TCRYPT keyfiles (segfault)
- Add 'bd_dm_is_tech_avail' to header file (vtrefny)
- Fix release number in NEWS.rst (vtrefny)
- Update specs.rst and features.rst (vtrefny)

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.17-2
- Rebuilt for Python 3.7

* Tue Apr 24 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.17-1
- Redirect cryptsetup log to libblockdev log (vtrefny)
- Add a generic logging function for libblockdev (vtrefny)
- Add functions to resize LUKS 2 (vtrefny)
- Add function to get information about LUKS 2 integrity devices (vtrefny)
- Add function to get information about a LUKS device (vtrefny)
- Add a basic test for creating LUKS 2 format (vtrefny)
- Use libblockdev function to create LUKS 2 in tests (vtrefny)
- Add support for creating LUKS 2 format (vtrefny)
- Skip bcache tests on Rawhide (vtrefny)
- Allow building libblockdev without Python 2 support (vtrefny)
- Allow compiling libblockdev crypto plugin without escrow support (vtrefny)
- Require at least libndctl 58.4 (vtrefny)
- New function for luks metadata size (japokorn)
- Add functions to backup and restore LUKS header (vtrefny)
- Add function for killing keyslot on a LUKS device (vtrefny)
- Add functions to suspend and resume a LUKS device (vtrefny)
- Use '=' instead of '==' to compare using 'test' (v.podzimek)
- lvm-dbus: Check returned job object for error (vtrefny)
- Get sector size for non-block NVDIMM namespaces too (vtrefny)
- Fix memory leaks discovered by clang (vtrefny)
- Add new functions to docs/libblockdev-sections.txt (segfault)
- Make a link point to the relevant section (segfault)
- Don't use VeraCrypt PIM if compiled against libcryptsetup < 2.0 (segfault)
- Make keyfiles parameter to bd_crypto_tc_open_full zero terminated (segfault)
- Add function bd_crypto_device_seems_encrypted (segfault)
- Support VeraCrypt PIM (segfault)
- Support TCRYPT system volumes (segfault)
- Support TCRYPT hidden containers (segfault)
- Support TCRYPT keyfiles (segfault)
- Support unlocking VeraCrypt volumes (segfault)
- Enforce ZERO_INIT gcc backwards compatibility (bjornpagen)
- Add function for getting NVDIMM namespace name from devname or path (vtrefny)
- Add --without-xyz to DISTCHECK_CONFIGURE_FLAGS for disabled plugins (vtrefny)
- Add tests for the NVDIMM plugin (vtrefny)
- Add the NVDIMM plugin (vtrefny)
- Fix build with clang (bjornpagen)
- s390: don't hardcode paths, search PATH (flokli)
- Fix build against musl libc (bjornpagen)
- Fix python2-gobject-base dependency on Fedora 26 and older (vtrefny)
- Sync the spec file with downstream (vtrefny)

* Wed Apr 11 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.16-3
- Add the NVDIMM plugin (vtrefny)
- Add tests for the NVDIMM plugin (vtrefny)
- Add --without-xyz to DISTCHECK_CONFIGURE_FLAGS for disabled plugins (vtrefny)
- Add function for getting NVDIMM namespace name from devname or path (vtrefny)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.16-2
- Escape macros in %%changelog

* Thu Feb 08 2018 Vojtech Trefny <vtrefny@redhat.com> - 2.16-1
- Add tests for progress report (jtulak)
- Add e2fsck progress (jtulak)
- Add progress reporting infrastructure for Ext fsck (jtulak)
- Add a function to test if prog. reporting was initialized (jtulak)
- Add support for LUKS 2 opening and key management (vtrefny)
- Fix few more links for project and documentation website (vtrefny)
- Sync the spec file with downstream (vpodzime)
- Check if 'journalctl' is available before trying to use it in tests (vtrefny)
- Update 'Testing libblockdev' section in documentation (vtrefny)
- Fix link to online documentation (vtrefny)
- Fix how the new kernel module functions are added to docs (vpodzime)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.15-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.15-2
- Switch to %%ldconfig_scriptlets

* Fri Dec 01 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.15-1
- Do not use the 'btrfs' plugin in overrides tests (vpodzime)
- Do not use the btrfs plugin in library tests (vpodzime)
- Check for btrfs module availability in btrfs module (vtrefny)
- Move kernel modules (un)loading and checking into utils (vtrefny)
- Free locale struct in kbd plugin (vtrefny)
- Add test for setting partition flags on GPT (vtrefny)
- Use only sgdisk to set flags on GPT (vtrefny)
- Move the fs.h file to its original place (vpodzime)
- Add a HACKING.rst file (vpodzime)
- Mark bcache tests as unstable (vpodzime)
- Fix memory leaks in bd_fs_vfat_get_info() (vpodzime)
- Revert the behaviour of bd_fs_check_deps() (vpodzime)
- Split the bd_fs_is_tech_avail() implementation (vpodzime)
- Split the FS plugin source into multiple files (vpodzime)
- Fix bd_s390_dasd_format (vponcova)
- Mark unstable tests as such (vpodzime)
- bd_s390_dasd_is_ldl should be true only for LDL DADSs (vponcova)
- Do not lie about tag creation (vpodzime)

* Wed Nov 08 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.14-2
- Rebuild for cryptsetup-2.0.0

* Tue Oct 31 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.14-1
- Support the legacy boot GPT flag (intrigeri)
- Respect the version in the blockdev.pc file (vpodzime)
- Add pkgconfig definitions for the utils library (vpodzime)
- fs.c: Fix potential NULL pointer dereference (vtrefny)
- dm.c: Fix uninitialized values in various dm plugin functions (vtrefny)
- dm.c: Check return values of dm_task_set_name/run/get_info functions (vtrefny)
- fs.c: Fix multiple "forward NULL" warnings in 'bd_fs_ntfs_get_info' (vtrefny)
- lvm-dbus.c: Fix multiple "use after free" coverity warnings (vtrefny)
- Fix duplicate 'const' in generated functions (vtrefny)
- Add some test cases for NTFS (kailueke)
- Add function wrappers for NTFS tools (kailueke)
- exec.c: Fix error message in 'bd_utils_exec_and_report_progress' (vtrefny)
- crypto.c: Fix waiting for enough entropy (vtrefny)
- Ignore some coverity false positive errors (vtrefny)
- exec.c: Ignore errors from 'g_io_channel_shutdown' (vtrefny)
- part.c: Check if we've found a place to put new logical partitions (vtrefny)
- kbd.c: Fix potential string overflow in 'bd_kbd_bcache_create' (vtrefny)
- exec.c: Fix resource leaks in 'bd_utils_exec_and_report_progress' (vtrefny)
- fs.c: Fix "forward null" in 'do_mount' and 'bd_fs_xfs_get_info' (vtrefny)
- part.c: Fix possible NULL pointer dereference (vtrefny)
- crypto.c: Use right key buffer in 'bd_crypto_luks_add_key' (vtrefny)
- exec.c: Fix "use after free" in 'bd_utils_check_util_version' (vtrefny)
- kbd.c: Fix double free in 'bd_kbd_zram_get_stats' (vtrefny)
- part.c: Check if file discriptor is >= 0 before closing it (vtrefny)
- mdraid.c: Fix resource leaks (vtrefny)
- lvm.c: Fix "use after free" in 'bd_lvm_get_thpool_meta_size' (vtrefny)
- fs.c: Fix for loop condition in 'bd_fs_get_fstype' (vtrefny)
- fs.c: Check sscanf return value in 'bd_fs_vfat_get_info' (vtrefny)
- fs.c: Fix resource leaks in 'bd_fs_get_fstype' (vtrefny)
- blockdev.c.in: Fix unused variables (vtrefny)
- Use libbytesize to parse bcache block size (vtrefny)
- Use system values in KbdTestBcacheStatusTest (vtrefny)
- Fix BSSize memory leaks in btrfs and mdraid plugins (vtrefny)
- Skip btrfs subvolume tests with btrfs-progs 4.13.2 (vtrefny)
- Added function to get DM device subsystem (japokorn)
- Sync spec with downstream (vpodzime)

* Fri Sep 29 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.13-1
- Fix the rpmlog and shortlog targets (vpodzime)
- Add a function for enabling/disabling plugins' init checks (vpodzime)
- Assign functions to tech-mode categories (vpodzime)
- Add missing items to particular sections in the documentation (vpodzime)
- Add a basic test for the runtime dependency checking (vpodzime)
- Simplify what WITH_BD_BCACHE changes in the KBD plugin (vpodzime)
- Add functions for querying available technologies (vpodzime)
- Dynamically check for the required utilities (vpodzime)
- Use shorter prefix for tempfiles (vtrefny)
- Try harder when waiting for lio device to show up (vtrefny)
- Better handle old and new zram sysfs api in tests (vtrefny)
- Skip btrfs tests on CentOS 7 aarch64 (vtrefny)
- Add new function for setting swap label (vtrefny)
- Use only one git tag for new releases (vtrefny)
- Fix source URL in spec file (vtrefny)
- Add NEWS.rst file (vtrefny)
- Do not include s390utils/vtoc.h in s390 plugin (vtrefny)
- Use "AC_CANONICAL_BUILD" to check architecture instead of "uname" (vtrefny)
- Bypass error proxy in s390 test (vtrefny)
- Fix zFCP LUN max length (vtrefny)
- Do not run g_clear_error after setting it (vtrefny)
- Allow compiling libblockdev without s390 plugin (vtrefny)
- Add a function for getting plugin name (vpodzime)

* Thu Sep 28 2017 Troy Dawson <tdawson@redhat.com> - 2.12-3
- Cleanup spec file conditionals correctly

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 2.12-2
- Cleanup spec file conditionals

* Wed Aug 30 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.12-1
- Own directories /etc/libblockdev and /etc/libblockdev/conf.d (vtrefny)
- Wait for resized partition (kailueke)
- Make sure the device is opened for libparted (vpodzime)
- Fix label check in swap_test (vtrefny)
- Use "run_tests" script for running tests from Makefile (vtrefny)
- Add a script for running tests (vtrefny)
- Tests: Move library initialization to setUpClass method (vtrefny)
- Stop skipping FAT resize tests on rawhide (vtrefny)
- Close filesystem before closing the partition during FAT resize (vtrefny)
- Use mountpoint for "xfs_info" calls (vtrefny)
- Use libmount cache when parsing /proc/mounts (vtrefny)
- Add some space for the CI status (vpodzime)
- Confirm the force when creating PVs in FS tests (vpodzime)
- Skip vgremove tests on 32bit Debian (vtrefny)
- Fix names of backing files in tests (vtrefny)
-  Fix checking for available locales (vtrefny)
- Skip dependency checking in mpath tests on Debian (vtrefny)
- Skip zRAM tests on Debian (vtrefny)
- Skip the test for device escrow on Debian too (vtrefny)
- Skip free region tests on Debian too (vtrefny)
- Fix redirecting command output to /dev/null in tests (vtrefny)
- Try harder to unmount devices in test cleanup (vtrefny)
- Require only plugins that are needed for given test (vtrefny)
- Try to get distribution info from "PrettyName" if "CPEName" isn't available (vtrefny)
- Use -ff when creating PVs in FS tests (vpodzime)
- Sync spec with downstream (vpodzime)

* Mon Jul 31 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.11-1
- Make the KbdZRAMDevicesTestCase inherit from KbdZRAMTestCase (vpodzime)
- Allow non-source directory builds (kailueke)
- Add a way to disable runtime dependency checks (vpodzime)
- Link to GObject even if no plugin is activated (kailueke)
- Skip zram tests on Rawhide (vpodzime)
- Keep most utilities available for tests (vpodzime)
- Use new libmount function to get (un)mount error message (vtrefny)
- Update the documentation URL (vpodzime)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 05 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.10-1
- Only enable partition size tolerance with alignment (vpodzime)
- Limit the requested partition size to maximum possible (vpodzime)
- Do not verify vfat FS' size after generic resize (vpodzime)
- Specify tolerance for partition size (kailueke)
- Only use the exact constraint if not using any other (vpodzime)
- Check resulting FS size in tests for generic FS resize (vpodzime)
- Query setting FS label support and generic relabeling (kailueke)
- Do not strictly require all FS utilities (vpodzime)
- Compile everything with the C99 standard (vpodzime)
- Add partition resize function (kailueke)
- Generic Check and Repair Functions (kailueke)
- Query functions for FS resize and repair support (kailueke)
- Update the project/source URL in the spec file (vpodzime)
- Add functions for opening/closing TrueCrypt/VeraCrypt volumes (vpodzime)
- Adapt to a change in behaviour in new libmount (vpodzime)
- Try RO mount also if we get EACCES (vpodzime)
- Size in bytes for xfs_resize_device (kailueke)
- src/plugins/Makefile.am: Remove hard coded include path in /usr prefix (tristan.vanberkom)
- Fixed include for libvolume_key.h (tristan.vanberkom)
- Ignore parted warnings if possible (squimrel)
- bcache tests: Remove FEELINGLUCKY checks (tasleson)
- kbd.c: Code review corrections (tasleson)
- kbd.c: Make bd_kbd_bcache_create work without abort (tasleson)

* Tue Jun 13 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.9-1
- Fix hardcoded reference to gcc (timo.gurr)
- Catch and ignore partial failures in LVM tests' cleanups (vpodzime)
- Fix hardcoded reference to pkg-config (timo.gurr)
- Make GObject introspection optional (vpodzime)
- Do not link libraries required by plugins to the GI files (vpodzime)
- Make sure the whole build status image is shown (vpodzime)
- Show CI status in README (at the GH repo's front page) (vpodzime)
- Always require the libudev pkg (tgurr)
- Make sure we give kernel time to fully setup zram device(s) (vpodzime)
- fs_test.py: Close FDs when calling utilities (tasleson)
- crypto.c: Correct segmentation fault (tasleson)

* Tue Jun 06 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.8-1
- Temporarily skip vfat generic resize test on rawhide (vtrefny)
- Use "safeprobe" in "bd_fs_wipe" (vtrefny)
- Add a generic filesystem resize function (vtrefny)
- Add a function to get mountpoint for a device (vtrefny)
- Add a function to get filesystem type for a device (vtrefny)
- Only include the LVM DBus config when shipping LVM DBus (vpodzime)
- Skip the LVM DBus vgreduce tests on Rawhide (vpodzime)
- Do not build the lvm-dbus plugin on RHEL/CentOS (vpodzime)
- Give zRAM more time to settle before trying to remove a device (vpodzime)
- Put zram tests adding/removing devices into a separate class (vpodzime)
- Skip LVM cache and RAID tests on Rawhide (vpodzime)
- Fix the skip_on decorator factory for tests (vpodzime)
- Use 'blkid -p' instead of lsblk to get device's FS type (vpodzime)
- Improve the lvm_set_global_config test (vpodzime)
- Pass '-y' to pvresize (vpodzime)
- Create a copy of os.environ for a child process (vpodzime)
- Revert "Use the "C.UTF-8" locale instead of just "C"" (vpodzime)
- Fix how we create vfat FS in tests (vpodzime)
- Skip the test if requiring unavailable locales (vpodzime)
- Use the "C.UTF-8" locale instead of just "C" (vpodzime)
- Add functions for working with ext2 and ext3 filesystems (vtrefny)
- Link to gobject when lvm or btrfs is enabled (andreas)
- Link to libm where needed (andreas)
- Add a function for cleaning a device (vtrefny)
- Add few code exaples to documentation (vtrefny)
- Use a special exception for no fs signature when doing wipe (vpodzime)
- One more incompatible os.symlink() call (vpodzime)
- Do not use pass-by-name in the os.symlink() call (vpodzime)
- Ignore previous errors when falling back to using ioctl() (vpodzime)
- Use ioctl() call to teardown loop devices (vpodzime)
- Resolve the device to remove for mdadm (vpodzime)
- Add a function for getting device symlinks (vpodzime)
- Use the new resolve_device() function where appropriate (vpodzime)
- Add the resolve_device() function to the utils library (vpodzime)
- First try to read the 'autoclear' flag from /sys/ (vpodzime)

* Wed Apr 26 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.7-1
- Skip btrfs min size tests on Fedora 25 (vtrefny)
- Make sure the loop device doesn't disappear during tests (vpodzime)
- Close the loop device when autoclear is (un)set (vpodzime)
- Do not enforce Python 3 for running tests in CI (vpodzime)
- Revert "Use different BTRFS_MIN_MEMBER_SIZE on aarch64" (vtrefny)
- Use both 'old' and 'new' sysfs files to read zRAM stats (vtrefny)
- Check if libparted-fs-resize pkgconfig is available (vpodzime)
- Do not try to get name for inactive partitions (vtrefny)
- Skip tests for getting free regions on CentOS/RHEL (vpodzime)
- Free the container holding the specs of free regions (vpodzime)
- Open loop devices as O_RDONLY when getting flags (vpodzime)
- Resolve maximum partition size when we know its start (vpodzime)
- Use --id instead of --part-type when setting partition id (vpodzime)
- Fix mdadm command for removing failed device from an array (vtrefny)
- Skip bcache tests on CentOS/RHEL 7 (vpodzime)
- Use six.assertRaisesRegex in the FS tests (vpodzime)
- Use mkdtemp() instead of TemporaryDirectory() (vpodzime)
- Fix installation without specifying --exec-prefix (vpodzime)
- Add options to force mkfs.ext4/vfat to create a FS on the whole device (vpodzime)
- Skip the test for device escrow on CentOS/RHEL (vpodzime)
- Define DEVNULL on our own if not in subprocess (vpodzime)
- Remove the patches from the spec file (vpodzime)
- Sync the spec file with downstream (vpodzime)
- Stop skipping zRAM stats tests (vtrefny)
- Add more tests for zRAM stats (vtrefny)
- Fix reading zRAM properties from sysfs (vtrefny)

* Wed Apr 12 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.6-3
- Do not try to parse 'raid_spec' for 'bd_md_activate' (vtrefny)
  Resolves: rhbz#1439111

* Tue Apr 11 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.6-2
- Make sure the returned thpool MD size is valid (vpodzime)

* Wed Mar 15 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.6-1
- Move the  part_err library before part and fs (vtrefny)
- Fix BuildRequires for crypto and dm packages (vtrefny)
- Fix mounting read-only devices (vtrefny)
- Fix the bd_s390_dasd_is_ldl function. (vponcova)
- Add the bd_s390_dasd_is_fba function to check if DASD is FBA (vponcova)
- Disable MD RAID tests on 32bit systems (vpodzime)
- Fix error message when mounting with a wrong fs type (vtrefny)
- Only create RPMs for requested/configured  plugins (vpodzime)
- Only check dependencies of plugins to be built (vpodzime)
- Only build and distribute plugins if configured so (vpodzime)
- Fix format-security and unused-result compiler warnings (vtrefny)
- Add an AC macro for modular builds (vpodzime)
- Add functions for mounting and unmounting filesystems (vtrefny)

* Mon Mar 06 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.5-1
- Do not try to get GVariant after not adding anything to its builder (vpodzime)
- Replace NULL with "" when building ExtraArg (vpodzime)
- Replace NULL with "" when adding it as a 's' GVariant (vpodzime)
- Make sure we don't try to add NULL as GVariant to DBus params (vpodzime)
- Add function for getting recommended thpool metadata size (vpodzime)
- Make udev settle after we create a LIO device (vpodzime)
- Always use '--yes' for lvremove (vpodzime)

* Tue Feb 21 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.4-1
- Update specs.rst to use present-tense and current API (agrover)
- Add functions using BLOBs as LUKS passphrases (vpodzime)
- Make sure the _error_quark() functions are in the library (vtrefny)
- Return a special error when trying to wipe empty device (vtrefny)
- Adapt tests to use LIO devices instead of loop devices (vpodzime)
- Add functions for creating and deleting LIO devices (vpodzime)
- MDRAID: Allow path as input for functions that work with sysfs (vtrefny)

* Wed Feb 15 2017 Vratislav Podzimek <vtrefny@redhat.com> - 2.3-3
- Rebuild with changelog fixed up

* Tue Feb 14 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.3-1
- Allow specifying raid 'name' in multiple way when calling md functions (vtrefny)
- Allow using both path and raid name in bd_md_set_bitmap_location (vtrefny)
- Fix potential memory issues in s390 sanitizate functions (vpodzime)
- Try multiple times when probing device for wiping (vpodzime)
- Check for libvolume_key.h and dmraid.h in configure.ac (vpodzime)
- Define our own macro for testing required header files (vpodzime)
- Include blockdev/utils.h in mdraid.h (vtrefny)
- Fix misspelling (agrover)
- Skip the bcache tests even on x86_64 (vpodzime)
- Take a break between bcache creation tests (vpodzime)
- Make sure ./configure fails if there are some soft failures (vpodzime)
- Improve the error message on missing GI support (vpodzime)
- Only require bcache-tools if supporting bcache (vpodzime)
- Skip bcache tests on non-x86_64 architectures (vpodzime)
- Try harder to register a new bcache device (vpodzime)
- Reimplement swapon/swapoff functions by using syscalls (vpodzime)
- Make sure bcache functions are correctly provided or not (vpodzime)
- Changelog fixup (vpodzime)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 11 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.2-2
- Rebuild with changelog fixed up

* Wed Jan 11 2017 Vratislav Podzimek <vpodzime@redhat.com> - 2.2-1
- Use the .in file as source when bumping version (vpodzime)
- Run pylint based on the python version and make it optional (vpodzime)
- Disable python3 and bcache on RHEL (vpodzime)
- Make bcache support optional (vpodzime)
- Teach boileplate_generator.py to skip things based on patterns (vpodzime)
- Require lower versions of some utilities (vpodzime)
- Do not require python3 for the boilerplate generation script (vpodzime)
- Use a proper initialization value for 'GPollFD fds[2]' (vpodzime)
- Deal with older parted and libblkid (vpodzime)
- Make python3 and gtk-doc optional (vpodzime)
- Bump the version of the utils library (vpodzime)
- Fix docstring for 'bd_md_node_from_name' (vtrefny)
- Add tests for added mdraid methods (vtrefny)
- Skip 'MDTestNominateDenominateActive' unless feeling lucky (vtrefny)
- MDRaid tests: change 'wait_for_resync' to wait for given action (vtrefny)
- Add functionality need by storaged to mdraid plugin (vtrefny)
- Move 'echo_str_to_file' method to utils (vtrefny)
- Add a function to setup a loop device from a file descriptor (vpodzime)
- Add functions to get/set the autoclear flag on a loop device (vpodzime)
- Fix checking /proc/mdstat for resync action (vtrefny)
- Adapt the test config files to version 2.x (vpodzime)

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.1-3
- Rebuild for Python 3.6

* Tue Nov 15 2016 Vratislav Podzimek <vpodzime@redhat.com> - 2.1-2
- Rebuild for a chain-build with storaged (vpodzime)

* Thu Nov 10 2016 Vratislav Podzimek <vpodzime@redhat.com> - 2.1-1
- Do not require an exclusive lock on the device to commit part stuff (vpodzime)
- Prevent failure if there are no btrfs subvolumes (vpodzime)
- Fix the test for getting version of a failing utility (vpodzime)
- Also run the utils tests (vpodzime)
- Bump the version of the pkgconfig module (vpodzime)
- Include utils.h in plugins that need it (vpodzime)
- Fix dependency check in fs plugin (vtrefny)
- Add support for setting part id (part type) on msdos part tables (vtrefny)
- Trim the extra info for MD RAID's name (vpodzime)
- Add xfsprogs and dosfstools as dependencies of the fs plugin (vpodzime)
- Fix md_name_from_node to work with the "/dev/" prefix (vpodzime)
- New major upstream release

* Wed Nov  9 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.9-8
- Revert "Prevent issues between libparted and udev" (vpodzime)
- Revert "Open the device file as RDWR when committing parts" (vpodzime)

* Thu Oct 27 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.9-7
- Open the device file as RDWR when committing parts (vpodzime)
- Handle mdadm --examine output during migration (adamw)
  Resolves: rhbz#1381996

* Mon Oct 24 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.9-6
- Prevent issues between libparted and udev (vpodzime)

* Mon Oct 10 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.9-5
- Make sure all object paths are passed and extracted as such (vpodzime)
  Resolves: rhbz#1374973

* Tue Oct  4 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.9-4
- Do not report volume name for FW RAID container device (vpodzime)
  Related: rhbz#1379865
- Search for just "UUID" in mdadm --examine output (vpodzime)
  Related: rhbz#1379865
- Use 'mdadm --examine --export' to get MD RAID level (vpodzime)
  Related: rhbz#1379865

* Mon Oct  3 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.9-3
- Try to search for "RAID Level" in mdadm's output (vpodzime)
  Resolves: rhbz#1379865
- Fix the number passed to LVM DBus as a job-creation timeout (vpodzime)
  Resolves: rhbz#1378970

* Mon Aug 29 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.9-2
- Explicitly cast number constants for GVariants (vpodzime)

* Wed Jul 27 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.9-1
- Add functions for creating thin/cache pools from existing LVs (vpodzime)
- Add the new mpath_get_members() function to the docs (vpodzime)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.8-1
- Add a function to get all mpath member devices (vpodzime)
- Fix backport issues in the zfcp-related functionality (#1348442) (vpodzime)
- Revert "Fix a few const params in the s390 plugin." (vpodzime)
- Fix creation of the version-only tags (vpodzime)

* Wed Jun 15 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.7-1
- Include the LV roles in the LVdata (vpodzime)
- Add a few missing items to the documentation (vpodzime)
- Document fields of the structures (vpodzime)
- Report (meta)data LV name properly for cache pools in lvm-dbus (vpodzime)
- Add information about related LVs to LVMLVdata (vpodzime)
- Remove unused code for getting supported functions (vpodzime)
- Add zFCP functionality to s390 plugin (sbueno+anaconda)
- Fix a few const params in the s390 plugin. (sbueno+anaconda)

* Wed Jun 01 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.6-1
- Ignore merge commits when creating changelog (vpodzime)
- Only take the number of the first %%changelog line found (vpodzime)
- Add some more detailed description to the part plugin (vpodzime)
- Fix a few extra issues with the const types (vpodzime)
- Add function for getting best free region (vpodzime)
- Add function for getting free regions (vpodzime)
- Fix the error message when setting part flag fails (vpodzime)
- Add function for setting disk flags (vpodzime)
- Add function for getting information about disk(s) (vpodzime)
- Do not set nonsense partition paths (vpodzime)
- Add function for getting partition by position (vpodzime)
- Indicate if there was error from parted or not in set_parted_error() (vpodzime)
- Minor fixes for the bd_part_get_part_spec() function (vpodzime)
- Add support for extra GPT flags (vpodzime)
- Add functionality for partition types (GUIDs) (vpodzime)
- Add functionality for partition names (vpodzime)
- Do not destroy disk objects we didn't get (vpodzime)
- Add a function for setting multiple partition flags at once (vpodzime)
- Remove the unused definition USE_PYTHON3 from configure.ac (vpodzime)
- Use different BTRFS_MIN_MEMBER_SIZE on aarch64 (vpodzime)
- Better release memory from parted objects on failures (vpodzime)
- Rework how we do optimal alignment (vpodzime)
- Do not try to destroy object we didn't get (vpodzime)
- Don't pass sizes in bytes to LVM (#1317373) (vpodzime)
- Add the libbytesize-devel build requires (vpodzime)
- Search for the LVM DBus service in both active and activatable names (vpodzime)
- Adapt to another stupid change in btrfs-progs (vpodzime)
- Add the XFS-related functions to the documentation (vpodzime)
- Add tests for the XFS-related functions (vpodzime)
- Add support for the XFS file system to the FS plugin (vpodzime)
- Add chunk_size to BDMDExamineData (vtrefny)
- Add the subpackage for the FS plugin (vpodzime)
- Add the FS plugin to the docs (vpodzime)
- Add tests for the ext4 functionality in the fs plugin (vpodzime)
- Add the FS plugin and the ext4 support (vpodzime)
- Add a function for running utility reporting error and exit code (vpodzime)
- Add the subpackage for the part plugin (vpodzime)
- Add a missing BuildRequires for parted-devel (vpodzime)
- Tag as both libblockdev-$version and just $version (vpodzime)
- Add the 'part' plugin to documentation (vpodzime)
- Add tests for the newly added part plugin (vpodzime)
- Add the part plugin with storaged-required functionality (vpodzime)

* Mon Mar 21 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.5-1
- Merge pull request #72 from vpodzime/master-faster_tests (vpodzime)
- Ignore all .bak files (vpodzime)
- Use python3-pylint and skip Python 2 tests (vpodzime)
- Try a bit harder when deactivating MD arrays in tests (vpodzime)
- Recompile only the LVM plugin in tests (vpodzime)
- Merge pull request #65 from vpodzime/master-loc_indep_error (vpodzime)
- Merge pull request #70 from vojtechtrefny/master-chunk_size (vpodzime)
- Add bd_md_create_with_chunk_size() function (vtrefny)
- Merge pull request #68 from vpodzime/master-no_intro_data (vpodzime)
- Merge pull request #71 from vpodzime/master-ipython3 (vpodzime)
- Run coverage with the right config directories (vpodzime)
- Merge pull request #67 from phatina/master (vpodzime)
- Merge pull request #69 from vpodzime/master-lvm_dbus_autostart (vpodzime)
- Use ipython3 for debugging and testing sessions (vpodzime)
- Don't expect to always get introspection data from DBus (vpodzime)
- Make invocation of tests configurable (phatina)
- Make error messages locale agnostic (vpodzime)

* Tue Mar 15 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.4-5
- Search for the LVM DBus service in activatable names (vpodzime)
- Better check for the LVM DBus API (vpodzime)

* Wed Mar  9 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.4-4
- Do not try to get object path of NULL in vgreduce (vpodzime)

* Tue Mar  1 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.4-3
- Depend on python3-gobject-base not python3-gobject so as to not pull in X components

* Thu Feb 25 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.4-2
- Add/fix the requirement for the LVM DBus daemon

* Thu Feb 25 2016 Vratislav Podzimek <vpodzime@redhat.com> - 1.4-1
- Merge pull request #62 from vpodzime/master-clean_up (vpodzime)
- Use addCleanup() instead of tearDown() in tests (vpodzime)
- Merge pull request #58 from vpodzime/master-lvm_dbus_pr (vpodzime)
- Add the VG renaming functionality (vpodzime)
- Packaging of the lvm-dbus plugin (vpodzime)
- The LVM DBus plugin (vpodzime)
- Add more generic functions for logging (vpodzime)
- Use MAX(a, b) instead of CLAMP(b, a, b) (vpodzime)
- Merge pull request #59 from vpodzime/master-vgrename (vpodzime)
- Add a function for renaming VGs (vpodzime)
- Merge pull request #57 from clumens/master (vpodzime)
- Fix error reporting when running "make test". (clumens)
- Merge pull request #54 from vojtechtrefny/master-pvsize (vpodzime)
- Do not try to create a PV with 4KiB metadata space (vpodzime)
- Add pv_info to BDLVMPVdata (vtrefny)
- btrfs now requires at least 128MiB device(s) (vpodzime)
- Merge pull request #52 from vpodzime/master (vpodzime)
- Round size in thpoolcreate() to KiB (vpodzime)
- Sync the %%changelog in spec with downstream (vpodzime)

* Wed Nov 25 2015 Vratislav Podzimek <vpodzime@redhat.com> - 1.3-4
- Create the cache pool before the to-be-cached LV (vpodzime)

* Thu Nov 05 2015 Robert Kuska <rkuska@redhat.com> - 1.3-3
- Rebuilt for Python3.5 rebuild

* Wed Nov 04 2015 Vratislav Podzimek <vpodzime@redhat.com> - 1.3-2
- Fix the annotation of bd_try_init in blockdev.c (vpodzime)

* Mon Oct 26 2015 Vratislav Podzimek <vpodzime@redhat.com> - 1.3-1
- Add missing python GI requires (vpodzime)
- Merge pull request #49 from dashea/libblockdev-python (vpodzime)
- Merge pull request #50 from vpodzime/master-fix_striped_lv (vpodzime)
- Merge pull request #46 from vpodzime/master-bcache_destroy (vpodzime)
- Merge pull request #39 from vpodzime/master-lvm_physical_space (vpodzime)
- Add a missing ldconfig that rpmlint found. (dshea)
- Move python files to separate packages (#1256758) (dshea)
- Fix lvcreate calls for striped LVs (vpodzime)
- Merge pull request #48 from vojtechtrefny/master_pvfree (vpodzime)
- Add pv_free to BDLVMPVdata (vtrefny)
- Merge pull request #47 from atodorov/add_coverage_report (vpodzime)
- Produce coverage report in CI (atodorov)
- Check bcache device's state before trying to detach the cache in destroy() (vpodzime)
- Fix URLs in the spec (vpodzime)
- Fix the int-float less-than comparison (vpodzime)
- Fix the calculation of physical space taken by an LV (vpodzime)

* Wed Sep 23 2015 Vratislav Podzimek <vpodzime@redhat.com> - 1.2-1
- Merge pull request #40 from vpodzime/master-config_support (vpodzime)
- Add tests for configuration support (vpodzime)
- Add a function for getting the loaded soname for a plugin (vpodzime)
- Add the default configuration (vpodzime)
- Load and respect configuration files when loading plugins (vpodzime)
- Add functions for finding and processing configuration files (vpodzime)
- Merge pull request #38 from vpodzime/master-md_superblock_size (vpodzime)
- Better document how MD RAID superblock size should be calculated (vpodzime)
- Merge pull request #36 from phatina/master (vpodzime)
- BTRFS: allow an arbitrary label to be set for a btrfs volume (phatina)
- Merge pull request #32 from phatina/master (vpodzime)
- BTRFS: fix parsing empty partition label (phatina)
- Merge pull request #35 from vpodzime/master (vpodzime)
- Define env variables for sudo via the env utility (vpodzime)
- Merge pull request #34 from dashea/python3-tests (vpodzime)
- Use unittest.addCleanup to simplify crypto_test. (dshea)
- Run tests with both python2 and python3 in the ci target. (dshea)
- Fix python3 issues in the unittests. (dshea)
- Do not run all tests in the 'ci' target (vpodzime)
- Merge pull request #33 from clumens/master (vpodzime)
- Add a new makefile target that does everything needed for jenkins. (clumens)
- Synchronize the .spec file with downstream (vpodzime)

* Fri Jul 24 2015 Vratislav Podzimek <vpodzime@redhat.com> - 1.1-2
- Explicitly specify the type of the cert_data parameter (#1246096) (vpodzime)

* Fri Jun 19 2015 Vratislav Podzimek <vpodzime@redhat.com> - 1.1-1
- Clean generated boilerplate code on 'make clean' (vpodzime)
- Merge pull request #31 from atodorov/use_lang_c (vpodzime)
- tests: use LANG=C in test_backup_passphrase() (atodorov)
- Merge pull request #30 from atodorov/makefile_updates (vpodzime)
- Makefile.am:   - add separate check target   - add coverage targets   - make it possible to test with Python3 (atodorov)
- Merge pull request #29 from atodorov/fix_issue_28 (vpodzime)
- Merge pull request #27 from atodorov/fix_docs_url (vpodzime)
- Merge pull request #26 from atodorov/test_docs (vpodzime)
- Change the modified sources back in tearDown() method as well. Closes #28. (atodorov)
- update URL to on-line documentation (atodorov)
- add test documentation (atodorov)
- Merge pull request #22 from dashea/escrow-tests (vpodzime)
- Merge pull request #25 from dashea/python-dep (vpodzime)
- Filter the python files from automatic rpm requires (dshea)
- Added tests for escrow packets and backup passphrases (dshea)
- Free leaked contexts from crypto_init (dshea)
- Cooperate with volume_key's memory management (dshea)
- Fix inheritance in the LVM tests to prevent multiple runs of some tests (vpodzime)
- Make the regexp for testing crypto_generate_backup_passphrase() stricter (vpodzime)
- Leave room in the backup passphrase for a trailing 0 (dshea)
- Add functions to get names of data/metadata internal LVs (vpodzime)
- Allow getting info for an internal LV (vpodzime)
- Gather information about all LVs (vpodzime)
- Round requested size to KBs in lvresize() (#1221247) (vpodzime)
- Add overrides for the ensure_init() function (vpodzime)
- Change the default value of the 'reload' parameter of try_reinit() (vpodzime)
- Merge pull request #21 from vpodzime/master-thpool_size_discard (vpodzime)
- Add overrides for the lvm_is_valid_thpool_chunk_size() function (vpodzime)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Vratislav Podzimek <vpodzime@redhat.com> - 1.0-1
- Adapt the release helper targets to autotools (vpodzime)
- Fixes of paths in Makefile.am's inspired by build failures on s390 (vpodzime)
- Add an s390-specific BuildRequires (vpodzime)
- Distribute also the boilerplate_generator.py script (vpodzime)
- Fix path to the generated blockdev.pc file (vpodzime)
- Adapt tests that compile stuff to autotools (vpodzime)
- Merge pull request #18 from vpodzime/master-autotools (vpodzime)
- Merge pull request #20 from dashea/gtkdoc-sections (vpodzime)
- Use the autotools building system instead of scons (vpodzime)
- Add the two new functions to the 'blockdev' docs section (vpodzime)
- Fix the line defining the docs file for the s390 section (vpodzime)
- Add a missing #include to the kbd.api file (vpodzime)
- Prevent s390-specific stuff from being used on other architectures (vpodzime)
- Update the documentation of the is_initialized() function (vpodzime)
- Merge pull request #19 from vpodzime/master-ensure_init (vpodzime)
- Remove private macros from the gtkdoc sections file. (dshea)
- Terminate ifdef statements for arch check. (sbueno+anaconda)
- Return early from the init functions if setting up logging fails (vpodzime)
- Add tests for the new and modified init functions (vpodzime)
- Add new try_init() and try_reinit() functions (vpodzime)
- Fix for adding number of loaded plugins (vpodzime)
- Fix for ensure_init() (vpodzime)
- Rename the try_init() function to ensure_init() and improve it (vpodzime)
- Check number of loaded plugins and library initialization state (vpodzime)
- Make 'reload' default to True instead of False in overrides (vpodzime)
- Add the s390 plugin test file. (sbueno+anaconda)
- Add the s390 plugin functions. (sbueno+anaconda)
- Add the s390 plugin. (sbueno+anaconda)
- Fix a typo in the spec file. (sbueno+anaconda)
- Require the kmod-devel package for the build process (vpodzime)
- Merge pull request #16 from dashea/escrow-encoding (vpodzime)
- Merge pull request #13 from vpodzime/master-lvm_cache (vpodzime)
- Merge pull request #12 from vpodzime/master-kbd_plugin (vpodzime)
- Merge pull request #14 from vpodzime/master-better_is_multipath (vpodzime)
- Use g_strdup() instead of g_strdup_printf() to just dup a string (vpodzime)
- Fix the spelling of "escrow" (dshea)
- Make the crypto plugin string parameters const (dshea)
- Set encoding to NULL before writing the escrow packet. (dshea)
- Get cache stats directly from the device mapper (vpodzime)
- Reimplement the is_mpath_member() function using device mapper (vpodzime)
- Add the LVM cache related symbols to the LVM section in the documentation (vpodzime)
- Update the list of LVM cache related functions in features.rst (vpodzime)
- Add tests for functions related to the LVM cache technology (vpodzime)
- Implement the lvm_cache_stats() function (vpodzime)
- Implement the lvm_cache_pool_name function (vpodzime)
- Implement the lvm_cache_create_cached_lv() function (vpodzime)
- Implement lvm_cache_attach/detach() functions (vpodzime)
- Implement the lvm_cache_create_pool() function plus two support functions (vpodzime)
- Implement the lvm_cache_get_default_md_size() function (vpodzime)
- Add the 'type' parameter to the lvm_lvcreate function (vpodzime)
- Teach boilerplate_generator to work with enum return types (vpodzime)
- Teach boilerplate_generator to work with 'const' return types (vpodzime)
- Add subpackages for the KBD plugin and its devel files (vpodzime)
- Add provided symbols to the documentation section of the KBD plugin (vpodzime)
- Implement the bcache_get_backing/cache_device functions (vpodzime)
- Exclude bcache tests from the normal 'test' target (vpodzime)
- Add some more and prolong some of the waits in KBD tests (vpodzime)
- Zero all newly allocated structures (vpodzime)
- Implement the bcache_status function and all it wants (vpodzime)
- Fix for the zram stats (vpodzime)
- Add bcache_get_mode and bcache_set_mode functions (vpodzime)
- Teach boilerplate_generator to work with enum return types (vpodzime)
- Teach boilerplate_generator to work with 'const' return types (vpodzime)
- Add the zram_get_stats function (vpodzime)
- Add the check() function for the KBD plugin (vpodzime)
- Add ErrorProxy instance for the KBD plugin (vpodzime)
- Add tests for bcache_create/attach/detach/destroy functions (vpodzime)
- Add the 'rebuild' Makefile target (vpodzime)
- Add bcache_create, bcache_attach, bcache_detach and bcache_destroy functions (vpodzime)
- Implement a helper function to echo string into a file (vpodzime)
- Add tests for zram_create_devices and zram_destroy_devices functions (vpodzime)
- Add the zram_destroy_devices function to the KBD plugin (vpodzime)
- Add first function to the KBD plugin: zram_create_devices (vpodzime)
- Add the KernelBlockDevices plugin (vpodzime)

* Wed May 13 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.13-1
- Prevent a leaky test from running in Jenkins (vpodzime)
- Try harder when cleaning up after MD RAID tests (vpodzime)
- Improve the MD RAID activate/deactivate test (vpodzime)
- One more @contextmanager that needs try-finally (vpodzime)
- Do not require metadata version to be reported by 'mdadm --examine' (#1217900) (vpodzime)
- Make sure we always set things back in context managers (vpodzime)
- Make the release date for version 1.0 more realistic (vpodzime)
- Merge pull request #11 from vpodzime/master (vpodzime)
- Run utilities with LC_ALL=C (vpodzime) (#1219033)
- Free GMatchInfo instance even in case of no match (vpodzime)
- Resolve /dev/md/ symlinks when checking swap status. (dlehman)

* Fri Apr 24 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.12-1
- Require minimum version of libblockdev-utils in some plugins (vpodzime)
- Report both stdout and stderr if exit code != 0 (vpodzime)

* Fri Apr 17 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.11-1
- Fix issues with using overriden functions over ErrorProxy (vpodzime)
- Update the roadmap.rst and features.rst with new stuff (vpodzime)
- Fix two minor issues with docs generation (vpodzime)

* Thu Apr 16 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.10-1
- Fix return type of the unload_plugins() function (vpodzime)
- Close the DL handle when check() or init() fail (vpodzime)
- Add one more check to the reload test (vpodzime)
- Drop reference to check() and init() functions (vpodzime)
- Add more cats to tests (vpodzime)
- Make regexp for getting btrfs version more generic (vpodzime)
- Merge pull request #8 from vpodzime/master-check_functions (vpodzime)
- Fix parameters passed to unoverridden swapon function (vpodzime)
- Implement and test swap plugin's check function (vpodzime)
- Implement and test MD RAID plugin's check function (vpodzime)
- Implement and test mpath plugin's check function (vpodzime)
- Try harder to get util's version (vpodzime)
- Implement and test loop plugin's check function (vpodzime)
- Implement and test DM plugin's check function (vpodzime)
- Implement and test BTRFS plugin's check function (vpodzime)
- Implement and test LVM plugin's check function (vpodzime)
- Init logging before loading plugins (vpodzime)
- Add function for utility availability checking (vpodzime)
- Fix default value for the fake_utils' path argument (vpodzime)
- Add ErrorProxy instance for the utils functions (vpodzime)
- Add function for version comparison (vpodzime)
- Merge pull request #9 from clumens/master (vpodzime)
- Disable pylint checking on the new exception proxy. (clumens)
- Fix XRules application and add a test for it (vpodzime)
- Raise NotImplementedError when an unavailable function is called (vpodzime)
- Merge pull request #4 from vpodzime/master-error_proxy (vpodzime)
- Merge branch 'master' into master-error_proxy (vpodzime)
- Merge pull request #5 from vpodzime/master-not_implemented_error (vpodzime)
- Add a simple test for unloaded/unavailable functions (vpodzime)
- Unload the plugins properly when reinit() is called (vpodzime)
- Raise error/exception when an unimplemented function is called (#1201475) (vpodzime)
- Do an ugly but necessary hack to make local GI overrides work (vpodzime)
- Add the __dir__ method to ErrorProxy (vpodzime)
- Add a rationale for the ErrorProxy to the overrides' docstring (vpodzime)
- Add some basic info about GI overrides to the documentation (vpodzime)
- Use pylint to check for errors in python overrides (vpodzime)
- Add the first small test for the ErrorProxy (vpodzime)
- Put the GI overrides in a special dir so that they are preferred (vpodzime)
- Add a cache for attributes already resolved by ErrorProxy (vpodzime)
- Implement the ErrorProxy python class and use it (vpodzime)

* Tue Apr 07 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.9-1
- Merge pull request #7 from vpodzime/master-fw_raid_fixes (vpodzime)
- Try a bit harder when trying to determine MD RAID name (#1207317) (vpodzime)
- Don't be naïve about mdadm --detail telling us what we want (#1207317) (vpodzime)
- Ignore libblockdev tarballs (vpodzime)
- Implement a test of btrfs_list_subvolumes on data from bug report (vpodzime)
- Implement a context manager for running tests with fake utils (vpodzime)
- Do not try to cannonicalize MD UUIDs if we didn't get them (#1207317) (vpodzime)
- Fix the table in roadmap.rst (vpodzime)
- Enrich the roadmap.rst file and add info about new plans (vpodzime)
- Sync spec file with downstream (vpodzime)

* Fri Mar 27 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.8-1
- Merge pull request #6 from vpodzime/master-sort_btrfs_subvolumes (vpodzime)
- Don't be naïve about mdadm providing us data we would like (#1206394) (vpodzime)
- Sort BTRFS subvolumes in a way that child never appears before parent (#1201120) (vpodzime)
- Let libcryptsetup handle LUKSname->/dev/mapper/LUKSname for us (vpodzime)
- Fix the crypto_luks_resize and create a test for it (vpodzime)
- Add targets to create the SRPM and RPM files easily (vpodzime)
- Don't round up to multiple of PE size bigger than max value of the rtype (vpodzime)
- Mark majority of MD RAID tests as slow (vpodzime)
- Merge pull request #1 from dashea/file-paths (vpodzime)
- Don't report error for no loop device associated with given file (vpodzime)
- Skip the detail_data.clean check when running tests in Jenkins (vpodzime)
- Make package file paths more specific (dshea)
- Implement and use MD RAID-specific wait for tests (vpodzime)
- Try to give MD RAID time to sync things before querying them (vpodzime)
- Fix the default value of the BDMDDetailData.clean field (vpodzime)
- Do cleanup after every single MD RAID tests (vpodzime)
- Do cleanup after every single LVM test (vpodzime)
- Do cleanup after every single BTRFS test (vpodzime)
- Make sure the LUKS device is closed and removed after tests (vpodzime)
- Make sure DM maps from tests are removed after tests (vpodzime)
- Make sure that loop devices are deactivated after tests (vpodzime)
- Make the tearDown method of the mpath test case better visible (vpodzime)
- Make sure that the swap is deactivated after tests (vpodzime)
- Fix docstrings in tests' utils helper functions (vpodzime)
- Improve the logging tests in utils_test.py (vpodzime)
- Update the features.rst file (vpodzime)
- Update the roadmap (vpodzime)
- Don't check if we get a mountpoint for BTRFS operations (vpodzime)

* Sun Mar 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.7-2
- Ship license as per packaging guidelines
- plugins-all should depend on base library too
- Add dev docs

* Fri Feb 27 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.7-1
- Be ready for mdadm --examine to not provide some of the values we want (vpodzime)
- Add exit code information to exec logging (vpodzime)
- Improve and add tests (vpodzime)
- Mark the test_force_plugin and test_reload as slow (vpodzime)
- Make sure we get some devices when creating btrfs volume (vpodzime)
- Add override for the lvremove function (vpodzime)
- Do not create LUKS format with no passphrase and no key file (vpodzime)
- Make sure we use the /dev/mapper/... path for luks_status (vpodzime)

* Thu Feb 19 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.6-1
- Don't report error when non-existing swap's status is queried (vpodzime)
- Make libblockdev-plugins-all pull the same version of plugins (vpodzime)
- Don't report error when asked for a backing file of an uknown loop (vpodzime)
- Fix accidental change in the spec's changelog (vpodzime)

* Mon Feb 16 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.5-1
- Add tests for what we can easily test from the mpath plugin (vpodzime)
- Add link to sources to the documentation (vpodzime)
- Add missing symbols into the libblockdev-sections.txt file (vpodzime)
- Do not build docs for testing (vpodzime)
- Add the bd_try_init function (vpodzime)
- Log stdout and stderr output when running processes (vpodzime)
- Allow a subset of plugins to be load instead of all (vpodzime)
- Make sure devmapper doesn't spam stdout with tons of messages (vpodzime)
- Let debug messages go to stderr when running ipython (vpodzime)
- Give plugins a way to initialize themselves (vpodzime)
- Give plugins a way how to check if they could run properly (vpodzime)
- Allow a subset of plugins to be load instead of all [TEST NEEDED] (vpodzime)
- Make sure we use the whole /dev/mapper path for cryptsetup (vpodzime)
- Fix vg_pv_count parsing when getting info about PV (vpodzime)
- Set default values to data structures if real values are not available (vpodzime)
- Fix the parameter name specifying pool metadata size (vpodzime)
- Activate LUKS as ReadWrite in luks_open (vpodzime)
- Make sure we pass key_size to cryptsetup in bytes (vpodzime)
- Add the min_entropy parameter to luks_format Python overrides (vpodzime)
- Pass size in KiB instead of B to lvcreate (vpodzime)
- Add underscore into dataalignment and metadatasize parameter names (vpodzime)
- Don't report error if non-mpath device is tested for being mpath member (vpodzime)
- Fix name of the invoked utility in mpath_set_friendly_names (vpodzime)

* Sat Jan 31 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.4-1
- Improve the test for lvm_set_global_config (vpodzime)
- Fix some minor issues in the spec file (vpodzime)
- Fix issues with the LVM global config str (vpodzime)
- Add couple more Python overrides (vpodzime)
- Fix the name of the lvm_thlvpoolname() function in the header file (vpodzime)
- Use assertEqual instead of assertTrue(a == b) (vpodzime)
- Add the min_entropy parameter to luks_format (vpodzime)
- Move internal dmraid-related macros into the source file (vpodzime)
- Add an override for the md_add function (vpodzime)
- Fix parameters in luks_open python overrides (vpodzime)
- Prevent init() from being done multiple times and provide a test function (vpodzime)
- Add the roadmap.rst document (vpodzime)
- Remove an extra parenthesis in one of the docstrings (vpodzime)
- Move the mddetail function next to the mdexamine function (vpodzime)
- Add some more constants required by blivet (vpodzime)

* Wed Jan 21 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.3-1
- Require volume_key-devel in a version that fixes build issues (vpodzime)
- Fix Python 2 devel package name in BuildRequires (vpodzime)
- Generate docs for the library and all plugins (vpodzime)
- Make doc comments better for documentation generation (vpodzime)
- Fix parameter names in function prototypes (vpodzime)
- Add the metadatasize parameter to pvcreate (vpodzime)
- Add the dataalignment parameter to lvm_pvcreate (vpodzime)
- Export non-internal constants via introspection (vpodzime)
- Expand size constants in the GI-scanned files (vpodzime)
- Fix usage printing in the boilerplate_generator (vpodzime)
- Add the build directory to .gitignore (vpodzime)
- Add the md_run function (vpodzime)
- Fix some issues in Python overrides (vpodzime)
- Add the escrow_device function to the crypto plugin (vpodzime)
- Fix version of GI files in the Makefile (vpodzime)
- Make the order of release target's dependencies more explicit (vpodzime)

* Mon Jan 12 2015 Vratislav Podzimek <vpodzime@redhat.com> - 0.2-1
- Fix dependencies of the release target (vpodzime)
- Python overrides for the GI-generated bindings (vpodzime)
- Pass version info to the code and use it to load plugins (vpodzime)

* Wed Dec 10 2014 Vratislav Podzimek <vpodzime@redhat.com> - 0.1-1
- Initial release
