# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define with_python3 1
%define with_gtk_doc 1
%define with_btrfs 1
%define with_crypto 1
%define with_dm 1
%define with_loop 1
%define with_lvm 1
%define with_lvm_dbus 1
%define with_mdraid 1
%define with_mpath 1
%define with_swap 1
%define with_part 1
%define with_fs 1
%define with_nvdimm 1
%define with_gi 1
%define with_escrow 1
%define with_tools 1
%define with_nvme 1
%define with_smart 1
%define with_smartmontools 1

# btrfs is not available on RHEL > 7
%if 0%{?rhel} > 7 || %{with_btrfs} == 0
%define with_btrfs 0
%define btrfs_copts --without-btrfs
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
%if %{with_part} != 1
%define part_copts --without-part
%endif
%if %{with_fs} != 1
%define fs_copts --without-fs
%endif
%if %{with_nvdimm} != 1
%define nvdimm_copts --without-nvdimm
%endif
%if %{with_tools} != 1
%define tools_copts --without-tools
%endif
%if %{with_gi} != 1
%define gi_copts --disable-introspection
%endif
%if %{with_nvme} != 1
%define nvme_copts --without-nvme
%endif
%if %{with_smart} != 1
%define smart_copts --without-smart
%endif
%if %{with_smartmontools} != 1
%define smartmontools_copts --without-smartmontools
%endif

%define configure_opts %{?python3_copts} %{?lvm_dbus_copts} %{?btrfs_copts} %{?crypto_copts} %{?dm_copts} %{?loop_copts} %{?lvm_copts} %{?lvm_dbus_copts} %{?mdraid_copts} %{?mpath_copts} %{?swap_copts} %{?part_copts} %{?fs_copts} %{?nvdimm_copts} %{?tools_copts} %{?gi_copts} %{?nvme_copts} %{?smart_copts} %{?smartmontools_copts}

Name:        libblockdev
Version:     3.4.0
Release:     1%{?dist}
Summary:     A library for low-level manipulation with block devices
License:     LGPL-2.1-or-later
URL:         https://github.com/storaged-project/libblockdev
Source0:     https://github.com/storaged-project/libblockdev/releases/download/%{version}/%{name}-%{version}.tar.gz

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

# obsolete removed subpackages to allow upgrades
Provides: libblockdev-kbd = %{version}-%{release}
Obsoletes: libblockdev-kbd < %{version}-%{release}
Provides: libblockdev-vdo = %{version}-%{release}
Obsoletes: libblockdev-vdo < %{version}-%{release}

Requires: %{name}-utils%{?_isa} = %{version}-%{release}

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
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

# obsolete removed devel subpackages to allow upgrades
Provides: libblockdev-kbd-devel = %{version}-%{release}
Obsoletes: libblockdev-kbd-devel < %{version}-%{release}
Provides: libblockdev-vdo-devel = %{version}-%{release}
Obsoletes: libblockdev-vdo-devel < %{version}-%{release}

%description devel
This package contains header files and pkg-config files needed for development
with the libblockdev library.

%if %{with_python3}
%package -n python3-blockdev
Summary:     Python3 gobject-introspection bindings for libblockdev
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: python3-gobject-base
Requires: python3-bytesize
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
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: btrfs-progs

%description btrfs
The libblockdev library plugin (and in the same time a standalone library)
providing the BTRFS-related functionality.

%package btrfs-devel
Summary:     Development files for the libblockdev-btrfs plugin/library
Requires: %{name}-btrfs%{?_isa} = %{version}-%{release}
Requires: glib2-devel
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}

%description btrfs-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-btrfs plugin/library.
%endif


%if %{with_crypto}
%package crypto
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
BuildRequires: cryptsetup-devel >= 2.3.0
BuildRequires: libblkid-devel
BuildRequires: keyutils-libs-devel

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
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description crypto-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-crypto plugin/library.
%endif


%if %{with_dm}
%package dm
BuildRequires: device-mapper-devel
BuildRequires: systemd-devel
Summary:     The Device Mapper plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: device-mapper

%description dm
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to Device Mapper.

%package dm-devel
Summary:     Development files for the libblockdev-dm plugin/library
Requires: %{name}-dm%{?_isa} = %{version}-%{release}
Requires: glib2-devel
Requires: device-mapper-devel
Requires: systemd-devel
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}

%description dm-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-dm plugin/library.
%endif


%if %{with_fs}
%package fs
BuildRequires: libblkid-devel
BuildRequires: libmount-devel
BuildRequires: libuuid-devel
BuildRequires: e2fsprogs-devel
Summary:     The FS plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}

%description fs
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to operations with file systems.

%package fs-devel
Summary:     Development files for the libblockdev-fs plugin/library
Requires: %{name}-fs%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description fs-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-fs plugin/library.
%endif


%if %{with_loop}
%package loop
Summary:     The loop plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}

%description loop
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to loop devices.

%package loop-devel
Summary:     Development files for the libblockdev-loop plugin/library
Requires: %{name}-loop%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description loop-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-loop plugin/library.
%endif


%if %{with_lvm}
%package lvm
BuildRequires: device-mapper-devel
BuildRequires: libyaml-devel
Summary:     The LVM plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: lvm2

%description lvm
The libblockdev library plugin (and in the same time a standalone library)
providing the LVM-related functionality.

%package lvm-devel
Summary:     Development files for the libblockdev-lvm plugin/library
Requires: %{name}-lvm%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description lvm-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-lvm plugin/library.
%endif

%if %{with_lvm_dbus}
%package lvm-dbus
BuildRequires: device-mapper-devel
BuildRequires: libyaml-devel
Summary:     The LVM plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: lvm2-dbusd >= 2.02.156

%description lvm-dbus
The libblockdev library plugin (and in the same time a standalone library)
providing the LVM-related functionality utilizing the LVM DBus API.

%package lvm-dbus-devel
Summary:     Development files for the libblockdev-lvm-dbus plugin/library
Requires: %{name}-lvm-dbus%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description lvm-dbus-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-lvm-dbus plugin/library.
%endif


%if %{with_mdraid}
%package mdraid
BuildRequires: libbytesize-devel
Summary:     The MD RAID plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: mdadm

%description mdraid
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to MD RAID.

%package mdraid-devel
Summary:     Development files for the libblockdev-mdraid plugin/library
Requires: %{name}-mdraid%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description mdraid-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-mdraid plugin/library.
%endif


%if %{with_mpath}
%package mpath
BuildRequires: device-mapper-devel
Summary:     The multipath plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Recommends: device-mapper-multipath

%description mpath
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to multipath devices.

%package mpath-devel
Summary:     Development files for the libblockdev-mpath plugin/library
Requires: %{name}-mpath%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
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
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: ndctl

%description nvdimm
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to operations with NVDIMM devices.

%package nvdimm-devel
Summary:     Development files for the libblockdev-nvdimm plugin/library
Requires: %{name}-nvdimm%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description nvdimm-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-nvdimm plugin/library.
%endif


%if %{with_nvme}
%package nvme
BuildRequires: libnvme-devel
BuildRequires: libuuid-devel
Summary:     The NVMe plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}

%description nvme
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to operations with NVMe devices.

%package nvme-devel
Summary:     Development files for the libblockdev-nvme plugin/library
Requires: %{name}-nvme%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description nvme-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-nvme plugin/library.
%endif


%if %{with_part}
%package part
BuildRequires: libfdisk-devel
Summary:     The partitioning plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: util-linux

%description part
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to partitioning.

%package part-devel
Summary:     Development files for the libblockdev-part plugin/library
Requires: %{name}-part%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description part-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-part plugin/library.
%endif


%if %{with_smart}
%package smart
BuildRequires: libatasmart-devel >= 0.17
Summary:     The smart plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}

%description smart
The libblockdev library plugin (and in the same time a standalone library)
providing S.M.A.R.T. monitoring and testing functionality, based
on libatasmart.

%package smart-devel
Summary:     Development files for the libblockdev-smart plugin/library
Requires: %{name}-smart%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description smart-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-smart plugin/library.
%endif


%if %{with_smartmontools}
%package smartmontools
BuildRequires: json-glib-devel
Summary:     The smartmontools plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: smartmontools >= 7.0

%description smartmontools
The libblockdev library plugin (and in the same time a standalone library)
providing S.M.A.R.T. monitoring and testing functionality, based
on smartmontools.

%package smartmontools-devel
Summary:     Development files for the libblockdev-smart plugin/library
Requires: %{name}-smartmontools%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description smartmontools-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-smart plugin/library.
%endif


%if %{with_swap}
%package swap
BuildRequires: libblkid-devel
Summary:     The swap plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: util-linux

%description swap
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to swap devices.

%package swap-devel
Summary:     Development files for the libblockdev-swap plugin/library
Requires: %{name}-swap%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
Requires: glib2-devel

%description swap-devel
This package contains header files and pkg-config files needed for development
with the libblockdev-swap plugin/library.
%endif

%if %{with_tools}
%package tools
Summary:    Various nice tools based on libblockdev
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-lvm = %{version}-%{release}
BuildRequires: libbytesize-devel
BuildRequires: parted-devel
%if %{with_lvm_dbus} == 1
Recommends: %{name}-lvm-dbus
%endif

%description tools
Various nice storage-related tools based on libblockdev.

%endif

%ifarch s390 s390x
%package s390
Summary:    The s390 plugin for the libblockdev library
Requires: %{name}-utils%{?_isa} = %{version}-%{release}
Requires: s390utils

%description s390
The libblockdev library plugin (and in the same time a standalone library)
providing the functionality related to s390 devices.

%package s390-devel
Summary:     Development files for the libblockdev-s390 plugin/library
Requires: %{name}-s390%{?_isa} = %{version}-%{release}
Requires: %{name}-utils-devel%{?_isa} = %{version}-%{release}
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

%if %{with_nvme}
Requires: %{name}-nvme%{?_isa} = %{version}-%{release}
%endif

%if %{with_part}
Requires: %{name}-part%{?_isa} = %{version}-%{release}
%endif

%if %{with_smart}
Requires: %{name}-smart%{?_isa} = %{version}-%{release}
%endif

%if %{with_smartmontools}
Requires: %{name}-smartmontools%{?_isa} = %{version}-%{release}
%endif

%if %{with_swap}
Requires: %{name}-swap%{?_isa} = %{version}-%{release}
%endif

%ifarch s390 s390x
Requires: %{name}-s390%{?_isa} = %{version}-%{release}
%endif

%description plugins-all
A meta-package that pulls all the libblockdev plugins as dependencies.


%prep
%autosetup -n %{name}-%{version} -p1

%build
# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=2247319
%ifarch aarch64
find . -name Makefile.am | xargs sed -i -e 's/-Werror//g'
%endif

autoreconf -ivf

# workaround for https://bugzilla.redhat.com/show_bug.cgi?id=2247319
%ifarch aarch64
%global _fortify_level 0
%global optflags $(echo %optflags | sed -e 's/-O2/-O0/g') -Wp,-D_FORTIFY_SOURCE=0
%endif

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

%if %{with_nvme}
%ldconfig_scriptlets nvme
%endif

%if %{with_part}
%ldconfig_scriptlets part
%endif

%if %{with_smart}
%ldconfig_scriptlets smart
%endif

%if %{with_smartmontools}
%ldconfig_scriptlets smartmontools
%endif

%if %{with_swap}
%ldconfig_scriptlets swap
%endif

%ifarch s390 s390x
%ldconfig_scriptlets s390
%endif


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libblockdev.so.*
%if %{with_gi}
%{_libdir}/girepository*/BlockDev*.typelib
%endif
%dir %{_sysconfdir}/libblockdev
%dir %{_sysconfdir}/libblockdev/3/conf.d
%config %{_sysconfdir}/libblockdev/3/conf.d/00-default.cfg

%files devel
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

%files utils-devel
%{_libdir}/libbd_utils.so
%{_libdir}/pkgconfig/blockdev-utils.pc
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/utils.h
%{_includedir}/blockdev/sizes.h
%{_includedir}/blockdev/exec.h
%{_includedir}/blockdev/extra_arg.h
%{_includedir}/blockdev/dev_utils.h
%{_includedir}/blockdev/module.h
%{_includedir}/blockdev/dbus.h
%{_includedir}/blockdev/logging.h


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
%config %{_sysconfdir}/libblockdev/3/conf.d/10-lvm-dbus.cfg

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


%if %{with_nvme}
%files nvme
%{_libdir}/libbd_nvme.so.*

%files nvme-devel
%{_libdir}/libbd_nvme.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/nvme.h
%endif


%if %{with_part}
%files part
%{_libdir}/libbd_part.so.*

%files part-devel
%{_libdir}/libbd_part.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/part.h
%endif


%if %{with_smart}
%files smart
%{_libdir}/libbd_smart.so.*

%files smart-devel
%{_libdir}/libbd_smart.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/smart.h
%endif


%if %{with_smartmontools}
%files smartmontools
%{_libdir}/libbd_smartmontools.so.*

%files smartmontools-devel
%{_libdir}/libbd_smartmontools.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/smart.h
%endif


%if %{with_swap}
%files swap
%{_libdir}/libbd_swap.so.*

%files swap-devel
%{_libdir}/libbd_swap.so
%dir %{_includedir}/blockdev
%{_includedir}/blockdev/swap.h
%endif


%if %{with_tools}
%files tools
%{_bindir}/lvm-cache-stats
%{_bindir}/vfat-resize
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
* Wed Sep 24 2025 Packit <hello@packit.dev> - 3.4.0-1
- Update to version 3.4.0

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.3.1-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.3.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 19 2025 Vojtech Trefny <vtrefny@redhat.com> - 3.3.1-2
- Re-apply patches removed by 3.3.1 update

* Wed Jun 18 2025 Packit <hello@packit.dev> - 3.3.1-1
- Update to version 3.3.1

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.3.0-4
- Rebuilt for Python 3.14

* Thu Mar 20 2025 Tomas Bzatek <tbzatek@redhat.com> - 3.3.0-3
- smart: Use libatasmart drive self-assessment as an overall status

* Tue Mar 11 2025 Vojtech Trefny <vtrefny@redhat.com> - 3.3.0-2
- crypto: Add a function to set persistent flags for LUKS

* Thu Feb 13 2025 Packit <hello@packit.dev> - 3.3.0-1
- Update to version 3.3.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 07 2024 Vojtech Trefny <vtrefny@redhat.com> - 3.2.1-1
- Makefile: Fix generating RPM log during bumpver (vtrefny)
- nvme: Avoid element-type g-i annotations (tbzatek)
- ci: Install 'python3-libdnf5' for TMT test plans (vtrefny)
- lvm: Clarify the global config functionallity in libblockdev (vtrefny)
- smart: Clarify ID_ATA_SMART_ACCESS udev property values (tbzatek)
- smart: Clarify use of ID_ATA_SMART_ACCESS udev property (tbzatek)
- ci: Do not try to install test dependencies for CodeQL analysis (vtrefny)
- misc: Fix installing test dependencies on Debian/Ubuntu (vtrefny)
- dist: Sync spec with downstream (vtrefny)
- crypto: check that IOC_OPAL_GET_STATUS is defined (james.hilliard1)
- packit: Fix generating spec from template (vtrefny)
- dist: Fix source URL in spec (vtrefny)
- README: Update supported technologies (vtrefny)

* Tue Sep 10 2024 Vojtech Trefny <vtrefny@redhat.com> - 3.2.0-1
- ci: Add a simple GH action to run spelling tools on our code (vtrefny)
- crypto: Fix GType macro for crypto context (vtrefny)
- misc: Fix typos (vtrefny)
- part: Document type_name in BDPartSpec docstring (vtrefny)
- docs: Fix documentation for the SMART plugin (vtrefny)
- docs: Add BDCryptoLUKSHWEncryptionType to libblockdev-sections.txt (vtrefny)
- crypto: Fixing missing quotation marks in some error messages (vtrefny)
- crypto: Fix name of bd_crypto_opal_wipe_device in crypto.h (vtrefny)
- tests: Fix skipping VDO tests on Debian and CentOS 10 (vtrefny)
- crypto: Add a function to run OPAL PSID reset (vtrefny)
- ci: Remove priority from Testing farm repositories (vtrefny)
- NEWS: add preliminary release notes for the smart plugin (tbzatek)
- smart: Add documentation (tbzatek)
- crypto: Check for kernel SED OPAL support for OPAL operations (vtrefny)
- tests: Add a simple test case for LUKS HW-OPAL support (vtrefny)
- crypto: Add support for creating new LUKS HW-OPAL devices (vtrefny)
- crypto: Add information about HW encryption to BDCryptoLUKSInfo (vtrefny)
- crypto: Add a function to wipe a LUKS HW-OPAL device (vtrefny)
- crypto: Add a function to check for OPAL support for a device (vtrefny)
- tests: No longer need to skip exfat UUID tests on Fedora (vtrefny)
- smart: Mark drivedb integration as experimental (tbzatek)
- fs: Fix docstring for bd_fs_ext?_get_min_size functions (vtrefny)
- part: Add human readable partition type to BDPartSpec (vtrefny)
- crypto: Show error when trying using an invalid DM name (vtrefny)
- nvme: Fix potential memory leak (tbzatek)
- tests: Temporarily skip LVM VDO tests on RHEL/CentOS 10 (vtrefny)
- misc: Add vdo to test dependencies on Fedora (vtrefny)
- lvm: Get VDO stats from device mapper instead of /sys/kvdo (vtrefny)
- lvm: Check for dm-vdo instead of kvdo module for VDO support (vtrefny)
- infra: bump github/codeql-action from 2 to 3 (49699333+dependabot[bot])
- infra: bump actions/upload-artifact from 3 to 4 (49699333+dependabot[bot])
- infra: Add dependabot to automatically update GH actions (vtrefny)
- part: Fix copy-paste bug in bd_part_spec_copy (vtrefny)
- docs: Fix link to Python bindings documentation (vtrefny)
- tests: Add more libatasmart skdump samples (tbzatek)
- tests: Fix smartmontools plugin parsing of /dev/random (tbzatek)
- tests: Adapt smart plugin tests for the added extra arguments (tbzatek)
- smart: Add BDExtraArg arguments (tbzatek)
- tests: Add bd_utils_exec_and_capture_output_no_progress() tests (tbzatek)
- utils/exec: Add bd_utils_exec_and_capture_output_no_progress() (tbzatek)
- tests: Skip exFAT UUID tests also on Fedora 39 (vtrefny)
- ci: Run UDisks reverse dependency tests on pull requests (vtrefny)
- utils/exec: Refactor extra args append out (tbzatek)
- misc: Add kernel-modules-extra to test dependencies (vtrefny)
- ci: Add a simple tmt test and run it via packit (vtrefny)
- ci: Run Blivet reverse dependency tests on pull requests (vtrefny)
- Add cache size ratio to the output of lvm-cache-stats (v.podzimek)
- misc: Fix enabling source repositories on latest Ubuntu (vtrefny)
- ci: Use Ubuntu 24.04 in GitHub actions (vtrefny)
- fs: Fix ignoring errors from libext2fs (vtrefny)
- fs: Ignore shift-count-overflow warning in FS plugin (vtrefny)
- fs: Ignore unused-parameter warning in the FS plugin (vtrefny)
- tests: Skip ExFAT UUID tests with recent exfatprogs (vtrefny)
- tests: Split libatasmart and smartmontool tests (tbzatek)
- smart: Rework libatasmart temperature reporting (tbzatek)
- tests: Add SiliconPower SSD skdump reporting incorrect temp (tbzatek)
- build: Install lvm.h when only lvm_dbus enabled (tbzatek)
- smart: Use smartmontools drivedb.h for libatasmart validation (tbzatek)
- smart: Implement bd_smart_ata_get_info_from_data() (tbzatek)
- smart: Introduce new libatasmart plugin (tbzatek)
- smart: Refactor and split into libbd_smartmontools (tbzatek)
- smart: Introduce well-known attribute names, validation and pretty values (tbzatek)
- smart: Remove the ATA low-power mode detection (tbzatek)
- tests: Add SCSI SMART tests (tbzatek)
- smart: Add SCSI/SAS status retrieval (tbzatek)
- tests: Add tests for bd_smart_device_self_test() (tbzatek)
- tests: Add tests for bd_smart_set_enabled() (tbzatek)
- tests: Add SMART tests over supplied JSON dumps (tbzatek)
- tests: Add basic SMART tests (tbzatek)
- smart: Add bd_smart_device_self_test() (tbzatek)
- smart: Add bd_smart_set_enabled() (tbzatek)
- New SMART plugin (tbzatek)
- utils: Check also for aliases in bd_utils_have_kernel_module (vtrefny)
- Fix pylint possibly-used-before-assignment warning in BlockDev.py (vtrefny)
- build: Fix linking with LLD (vadorovsky)
- misc: Remove CentOS 8 Stream from Vagrantfile and test dependencies (vtrefny)
- misc: Vagrantfile update (vtrefny)
- tests: Skip filesystem tests if kernel module is not available (vtrefny)
- ci: Fix bumping release for Packit builds (vtrefny)
- ci: Get version for packit from the SPEC file (vtrefny)
- tests: Fix running tests without ntfsprogs (vtrefny)
- ci: Set custom release number for Packit (vtrefny)
- Bump version to 3.1.1 (vtrefny)
- utils: Clarify usage of version in bd_utils_check_util_version (vtrefny)
- crypto: Fix double free in bd_crypto_luks_remove_key (vtrefny)
- fixed md_create issue #1013 (guazhang)
- lvm-dbus: Fix leaking error in bd_lvm_init (vtrefny)
- lvm-dbus: Fix potential segfault in bd_lvm_init (vtrefny)
- lvm-dbus: Fix passing size for pvresize over DBus (vtrefny)
- nvme: Add bd_nvme_is_tech_avail to the API file (vtrefny)
- tests: Add NVMe controller type checks (tbzatek)
- tests: Add NVMe persistent discovery controller tests (tbzatek)
- btrfs: make btrfs subvolume listing consistent (jvanderwaa)
- crypto: Add support for conversion between different LUKS formats (xyakimo1)
- tests: Fix removing custom LVM devices file (vtrefny)
- tests: Ignore LVM devices file for non-LVM tests (vtrefny)
- tests: Manually remove removed PVs from LVM devices file (vtrefny)
- tests: introduce setup_test_device helper function (jvanderwaa)
- tests: split multi device tests into a new testcase class (jvanderwaa)
- dm_logging: Annotate redirect_dm_log() printf format (tbzatek)
- Fix some more occurrences of missing port to G_GNUC_UNUSED (tbzatek)
- Port to G_GNUC_INTERNAL for controlling symbols visibility (tbzatek)
- Use glib2 G_GNUC_UNUSED in place of UNUSED locally defined (giulio.benetti)
- Makefile: Fix bumpver to work with micro versions (vtrefny)
- Makefile: Do not include release in the tag (vtrefny)

* Thu Aug 15 2024 Vojtech Trefny <vtrefny@redhat.com> - 3.1.1-11
- crypto: LUKS OPAL support (#2304174)

* Fri Jul 26 2024 Vojtech Trefny <vtrefny@redhat.com> - 3.1.1-10
- fs: Ignore unused-parameter warning in the FS plugin

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.1.1-8
- Rebuilt for Python 3.13

* Thu Apr 11 2024 Dan Horák <dan[at]danny.cz> - 3.1.1-7
- Disable -Werror and build with -O0 on aarch64 to workaround #2247319

* Mon Apr 08 2024 Dan Horák <dan[at]danny.cz> - 3.1.1-6
- Back to standard build by reverting instrumentations for #2247319

* Fri Apr 05 2024 Dan Horák <dan[at]danny.cz> - 3.1.1-5
- Apply ASAN instrumentation for #2247319

* Wed Mar 27 2024 Adam Williamson <awilliam@redhat.com> - 3.1.1-4
- Apply UBSAN instrumentation per Dan Horák for #2247319

* Tue Mar 26 2024 Adam Williamson <awilliam@redhat.com> - 3.1.1-3
- Drop the de-optimization changes from -2

* Tue Mar 26 2024 Adam Williamson <awilliam@redhat.com> - 3.1.1-2
- Backport proposed upstream fix for #2247319
- Disable -Werror and build with -O0 to help further debug #2247319

* Tue Mar 26 2024 Vojtech Trefny <vtrefny@redhat.com> - 3.1.1-1
- lvm-dbus: Fix passing size for pvresize over DBus (vtrefny)
- nvme: Add bd_nvme_is_tech_avail to the API file (vtrefny)
- tests: Add NVMe controller type checks (tbzatek)
- tests: Add NVMe persistent discovery controller tests (tbzatek)
- tests: Fix removing custom LVM devices file (vtrefny)
- tests: Ignore LVM devices file for non-LVM tests (vtrefny)
- tests: Manually remove removed PVs from LVM devices file (vtrefny)
- dm_logging: Annotate redirect_dm_log() printf format (tbzatek)
- Fix some more occurrences of missing port to G_GNUC_UNUSED (tbzatek)
- Port to G_GNUC_INTERNAL for controlling symbols visibility (tbzatek)
- Use glib2 G_GNUC_UNUSED in place of UNUSED locally defined (giulio.benetti)
- Makefile: Fix bumpver to work with micro versions (vtrefny)

* Sat Mar 23 2024 Adam Williamson <awilliam@redhat.com> - 3.1.0-6
- Slightly stronger workaround attempt for #2247319

* Sat Mar 23 2024 Adam Williamson <awilliam@redhat.com> - 3.1.0-5
- Tentative workaround for #2247319 based on diagnosis from -4

* Fri Mar 22 2024 Adam Williamson <awilliam@redhat.com> - 3.1.0-4
- Try something else dumb to diagnose #2247319

* Thu Mar 21 2024 Adam Williamson <awilliam@redhat.com> - 3.1.0-3
- Disable some log statements to see if it works around #2247319

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Vojtech Trefny <vtrefny@redhat.com> - 3.1.0-1
- tests: Skip some checks for btrfs errors with btrfs-progs 6.6.3 (vtrefny)
- Fix missing progress initialization in bd_crypto_luks_add_key (vtrefny)
- fs: Report reason for open() and ioctl() failures (tbzatek)
- utils: Add expected printf string annotation (tbzatek)
- lvm-dbus: Avoid using already-freed memory (tbzatek)
- lvm-dbus: Fix leaking error (tbzatek)
- python: Add a deepcopy function to our structs (vtrefny)
- tests: Remove unreliable nvme attribute checks (tbzatek)
- tests: Use BDPluginSpec constructor in LVM DBus plugin tests (vtrefny)
- tests: Avoid setting up intermediary loop device for the nvme target (tbzatek)
- tests: Default to /tmp for create_sparse_tempfile() (tbzatek)
- part: Fix potential double free when getting parttype (vtrefny)
- Mark NVDIMM plugin as deprecated since 3.1 (vtrefny)
- tests: Remove some obsolete rules to skip tests (vtrefny)
- fs: Add support for getting filesystem min size for NTFS and Ext (vtrefny)
- fs: Fix allowed UUID for generic mkfs with VFAT (vtrefny)
- fs: Add a generic function to check for fs info availability (vtrefny)
- fs: Add a function to check label format for F2FS (vtrefny)
- swap: Add support for checking label and UUID format (vtrefny)
- ci: Remove the custom version command for Packit (vtrefny)
- ci: Manually prepare spec file for Packit (vtrefny)
- overrides: Remove unused 'sys' import (vtrefny)
- Add BDPluginSpec constructor and use it in plugin_specs_from_names (vtrefny)
- Sync spec with downstream (vtrefny)
- ci: Add an action to compile libblockdev with different compilers (vtrefny)

* Fri Oct 13 2023 Vojtech Trefny <vtrefny@redhat.com> - 3.0.4-1
- tests: Fix "invalid escape sequence '\#'" warning from Python 3.12 (vtrefny)
- tests: Fail early when recompilation fails in library_test (vtrefny)
- lvm-dbus: Replace g_critical calls with bd_utils_log_format (vtrefny)
- Use log function when calling a plugin function that is not loaded (vtrefny)
- logging: Default to DEBUG log level if compiled with --enable-debug (vtrefny)
- nvme: Rework memory allocation for device ioctls (tbzatek)
- packit: Add configuration for downstream builds (vtrefny)
- fs: correct btrfs set label description (jvanderwaa)
- fs: Disable progress for ntfsresize (vtrefny)
- part: Do not open disk read-write for read only operations (vtrefny)
- ci: Bump actions/checkout from v3 to v4 (vtrefny)
- plugins: btrfs: use g_autofree where possible for g_free (jvanderwaa)
- plugins: use g_autofree for free'ing g_char's (jvanderwaa)
- spec: Move obsoleted devel subpackages to libblockdev-devel (vtrefny)
- spec: Obsolete vdo plugin packages (vtrefny)

* Wed Sep 06 2023 Vojtech Trefny <vtrefny@redhat.com> - 3.0.3-2
- Obsolete vdo plugin packages (#2237477)

* Thu Aug 31 2023 Vojtech Trefny <vtrefny@redhat.com> - 3.0.3-1
- crypto: Correctly convert passphrases from Python to C (vtrefny)
- tests: Minor NVMe HostNQN fixes (tbzatek)
- nvme: Generate HostID when missing (tbzatek)
- Always use "--fs ignore" with lvresize (mvollmer)
- nvme: Use interim buffer for nvme_get_log_sanitize() (tbzatek)
- fs: Fix memory leak (vtrefny)
- fs: Fix leaking directories with temporary mounts (vtrefny)
- tests: Specificy required versions when importing GLib and BlockDev introspection (biebl)
- tests: Replace deprecated unittest assert calls (vtrefny)

* Thu Jul 20 2023 Vojtech Trefny <vtrefny@redhat.com> - 3.0.2-1
- fs: Avoid excess logging in extract_e2fsck_progress (vtrefny)
- loop: Report BD_LOOP_ERROR_DEVICE on empty loop devices (tbzatek)
- lib: Silence the missing DEFAULT_CONF_DIR_PATH (tbzatek)
- fs: Document that generic functions can mount filesystems (vtrefny)
- fs: Use read-only mount where possible for generic FS functions (vtrefny)
- docs: Fix test quotation (marecki)
- fs: Fix unused error in extract_e2fsck_progress (vtrefny)
- Use ntfsinfo instead of ntfscluster for faster bd_fs_ntfs_get_info (amubtdx)
- Restrict list of exported symbols via -export-symbols-regex (biebl)
- Fix formatting in NEWS.rst (vtrefny)

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 3.0.1-2
- Rebuilt for Python 3.12

* Tue Jul 04 2023 Vojtech Trefny <vtrefny@redhat.com> - 3.0.1-1
- fs: Simplify struct BDFSInfo (tbzatek)
- boilerplate_generator: Annotate stub func args as G_GNUC_UNUSED (tbzatek)
- crypto: Remove stray struct redefinition (tbzatek)
- loop: Remove unused variable (tbzatek)
- build: Exit before AC_OUTPUT on error (tbzatek)
- loop: define LOOP_SET_BLOCK_SIZE is not defined (giulio.benetti)
- Make the conf.d directory versioned (vtrefny)
- configure: Fix MAJOR_VER macro (vtrefny)
- spec: Add dependency on libblockdev-utils to the s390 plugin (vtrefny)
- nvme: Mark private symbols as hidden (tbzatek)
- dist: Sync spec with downstream (vtrefny)
- misc: Update steps and Dockerfile for Python documentation (vtrefny)
- fs: Add missing copy and free functions to the header file (vtrefny)
- lvm: Add bd_lvm_segdata_copy/free to the header file (vtrefny)
- loop: Remove bd_loop_get_autoclear definition (vtrefny)
- lvm: Fix declaration for bd_lvm_vdolvpoolname (vtrefny)
- lvm: Make _vglock_start_stop static (vtrefny)
- vdo_stats: Remove unused libparted include (vtrefny)

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 3.0-2
- Rebuilt for Python 3.12

* Fri Jun 23 2023 Vojtech Trefny <vtrefny@redhat.com> - 3.0-1
- Libblockdev 3.0 release
