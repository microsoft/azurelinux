# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%if ( 0%{?suse_version} )
BuildRequires: distribution-release
%if ( ! 0%{?is_opensuse} )
BuildRequires: sles-release >= 12
Requires: sles-release >= 12
%else
BuildRequires: openSUSE-release
Requires: openSUSE-release
%endif
%endif

# Conditionally enable some FSALs, disable others.
#
# 1. rpmbuild accepts these options (gpfs as example):
#    --with gpfs
#    --without gpfs

%define on_off_switch() %%{?with_%1:ON}%%{!?with_%1:OFF}

# A few explanation about %%bcond_with and %%bcond_without
# /!\ be careful: this syntax can be quite messy
# %%bcond_with means you add a "--with" option, default = without this feature
# %%bcond_without adds a"--without" so the feature is enabled by default

%bcond_without nullfs
%global use_fsal_null %{on_off_switch nullfs}

%bcond_without mem
%global use_fsal_mem %{on_off_switch mem}

%bcond_without gpfs
%global use_fsal_gpfs %{on_off_switch gpfs}

%bcond_with xfs
%global use_fsal_xfs %{on_off_switch xfs}

%bcond_with lustre
%global use_fsal_lustre %{on_off_switch lustre}

%ifnarch i686 armv7hl
%bcond_without ceph
%else
%bcond_with ceph
%endif
%global use_fsal_ceph %{on_off_switch ceph}

%ifnarch i686 armv7hl
%bcond_without rgw
%else
%bcond_with rgw
%endif
%global use_fsal_rgw %{on_off_switch rgw}

%bcond_without gluster
%global use_fsal_gluster %{on_off_switch gluster}

%bcond_without saunafs
%global use_fsal_saunafs %{on_off_switch saunafs}

%bcond_with kvsfs
%global use_fsal_kvsfs %{on_off_switch kvsfs}

%bcond_with rdma
%global use_rdma %{on_off_switch rdma}

%bcond_with 9P
%global use_9P %{on_off_switch 9P}

%bcond_with jemalloc

%bcond_with lttng
%global use_lttng %{on_off_switch lttng}

%bcond_without utils
%global use_utils %{on_off_switch utils}

%bcond_without gui_utils
%global use_gui_utils %{on_off_switch gui_utils}

%bcond_without system_ntirpc
%global use_system_ntirpc %{on_off_switch system_ntirpc}

%bcond_without qos
%global use_qos %{on_off_switch_qos}

%bcond_without man_page
%global use_man_page %{on_off_switch man_page}

%ifnarch i686 armv7hl
%bcond_without rados_recov
%else
%bcond_with rados_recov
%endif
%global use_rados_recov %{on_off_switch rados_recov}

%ifnarch i686 armv7hl
%bcond_without rados_urls
%else
%bcond_with rados_urls
%endif
%global use_rados_urls %{on_off_switch rados_urls}

%bcond_without rpcbind
%global use_rpcbind %{on_off_switch rpcbind}

%bcond_without unwind
%global use_unwind %{on_off_switch unwind}

%bcond_without unwind_enriched_bt
%global use_unwind_enriched_bt %{on_off_switch unwind_enriched_bt}

%bcond_without mspac_support
%global use_mspac_support %{on_off_switch mspac_support}

%bcond_with sanitize_address
%global use_sanitize_address %{on_off_switch sanitize_address}

%bcond_with legacy_python_install
%global use_legacy_python_install %{on_off_switch legacy_python_install}

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%global _rundir %{_localstatedir}/run
%endif

%global dev_version %{lua: s = string.gsub('@GANESHA_EXTRA_VERSION@', '^%-', ''); s2 = string.gsub(s, '%-', '.'); print((s2 ~= nil and s2 ~= '') and s2 or "0.1") }
#%%global dev rc6

Name:		nfs-ganesha
Version:	7.2
Release:	2%{?dev:%{dev}}%{?dist}
Summary:	NFS-Ganesha is a NFS Server running in user space
License:	LGPL-3.0-or-later
Url:		https://github.com/nfs-ganesha/nfs-ganesha/wiki

Source0:	https://github.com/%{name}/%{name}/archive/V%{version}%{?dev:-%{dev}}/%{name}-%{version}%{?dev:%{dev}}.tar.gz
Patch:		0001-config_samples-log_rotate.patch

BuildRequires:	cmake
BuildRequires:	make
%ifarch x86_64 aarch64
BuildRequires:	mold
%endif
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig
BuildRequires:	userspace-rcu-devel
BuildRequires:	krb5-devel
%if ( 0%{?with rados_recov} || 0%{?with rados_urls} )
BuildRequires: librados-devel >= 0.61
%endif
%if ( 0%{?suse_version} >= 1330 )
BuildRequires:	libnsl-devel
%else
%if ( 0%{?fedora} >= 28 || 0%{?rhel} >= 8 )
BuildRequires:	libnsl2-devel
%endif
%endif
%if ( 0%{?suse_version} )
BuildRequires:	dbus-1-devel
Requires:	dbus-1
BuildRequires:	systemd-rpm-macros
%else
BuildRequires:	dbus-devel
Requires:	dbus
%endif
BuildRequires:	libcap-devel
BuildRequires:	libblkid-devel
BuildRequires:	libuuid-devel
%if ( 0%{?with_mspac_support} )
BuildRequires: libwbclient-devel
%endif
BuildRequires:	gcc gcc-c++
%if ( 0%{?with_system_ntirpc} )
BuildRequires:	libntirpc-devel >= 7.0
%else
Requires: libntirpc = @NTIRPC_VERSION_EMBED@
%endif
%if ( 0%{?rhel} && 0%{?rhel} <= 7 )
# this should effectively be a no-op, as all Red Hat Enterprise Linux installs should have it
# with selinux.
Requires:	policycoreutils-python
%endif
%if ( 0%{?fedora} )
# The nfs-ganesha.service unit requires dbus-send
Requires:	dbus-tools
# this should effectively be a no-op, as all Fedora installs should have it
# with selinux.
Requires:	policycoreutils-python-utils
%endif
%if ( 0%{?with_sanitize_address} )
BuildRequires: libasan
%endif
Requires:	nfs-utils

%if ( 0%{?with_rpcbind} )
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 6 ) || ( 0%{?suse_version} )
Requires:	rpcbind
%else
Requires:	portmap
%endif
%endif

%if ( 0%{?suse_version} )
BuildRequires:	nfsidmap-devel
%else
BuildRequires:	libnfsidmap-devel
%endif

%if ( 0%{?with_rdma} )
BuildRequires:	libmooshika-devel >= 0.6-0
%endif
%if ( 0%{?with_jemalloc} )
BuildRequires:	jemalloc-devel
%endif
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%if ( 0%{?with_man_page} )
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
BuildRequires: python-sphinx
%else
%if ( 0%{?suse_version} )
BuildRequires: python3-Sphinx
%else
BuildRequires: python3-sphinx
%endif
%endif
%endif
Requires(post): psmisc

%if ( 0%{?fedora} >= 30 || 0%{?rhel} >= 8 )
Requires: nfs-ganesha-selinux = %{version}-%{release}
%endif

# Use CMake variables

%description
nfs-ganesha : NFS-GANESHA is a NFS Server running in user space.
It comes with various back-end modules (called FSALs) provided as
shared objects to support different file systems and name-spaces.

%if ( 0%{?with_9P} )
%package mount-9P
Summary: a 9p mount helper

%description mount-9P
This package contains the mount.9P script that clients can use
to simplify mounting to NFS-GANESHA. This is a 9p mount helper.
%endif

%package -n ganesha_monitoring
Summary: The NFS-GANESHA Monitoring module
Group: Applications/System
Provides: libganesha_monitoring.so

%description -n ganesha_monitoring
The monitoring module contains metrics collectors and HTTP exposer
in Prometheus format.

%package vfs
Summary: The NFS-GANESHA VFS FSAL
BuildRequires: libattr-devel
Obsoletes: %{name}-xfs <= %{version}
Requires: nfs-ganesha = %{version}-%{release}

%description vfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support VFS based filesystems

%package proxy-v4
Summary: The NFS-GANESHA PROXY_V4 FSAL
BuildRequires: libattr-devel
Requires: nfs-ganesha = %{version}-%{release}

%description proxy-v4
This package contains a FSAL shared object to
be used with NFS-Ganesha to support PROXY_V4 based filesystems

%package proxy-v3
Summary: The NFS-GANESHA PROXY_V3 FSAL
BuildRequires: libattr-devel
Requires: nfs-ganesha = %{version}-%{release}

%description proxy-v3
This package contains a FSAL shared object to
be used with NFS-Ganesha to support PROXY_V3 based filesystems

%if ( 0%{?with_utils} )
%package utils
Summary: The NFS-GANESHA util scripts
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
Requires:	dbus-python, pygobject2, pyparsing
BuildRequires:	python-devel
%else
Requires:	python3-gobject, python3-pyparsing
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%if ( ! 0%{?with_legacy_python_install} )
BuildRequires:	python3-wheel
BuildRequires:	python3-build
BuildRequires:	python3-installer
%endif
%if ( 0%{?suse_version} )
Requires:	dbus-1-python
%else
Requires:	python3-dbus
%endif
%endif

%if ( 0%{?with_gui_utils} )
%if ( 0%{?suse_version} )
BuildRequires:	python-qt5-devel
%else
%if ( 0%{?fedora} >= 31 || 0%{?rhel} >= 8 )
BuildRequires:	python3-qt5-devel
%else
BuildRequires:	PyQt4-devel
%endif
%endif
%endif

%description utils
This package contains utility scripts for managing the NFS-GANESHA server
%endif

%if ( 0%{?with_lttng} )
%package lttng
Summary: The NFS-GANESHA library for use with LTTng
BuildRequires:	lttng-ust-devel >= 2.3
BuildRequires:	lttng-tools-devel >= 2.3
Requires: nfs-ganesha = %{version}-%{release}

%description lttng
This package contains the libganesha_trace.so library. When preloaded
to the ganesha.nfsd server, it makes it possible to trace using LTTng.
%endif

%if ( 0%{?with_rados_recov} )
%package rados-grace
Summary: The NFS-GANESHA command for managing the RADOS grace database
Requires: nfs-ganesha = %{version}-%{release}

%description rados-grace
This package contains the ganesha-rados-grace tool for interacting with the
database used by the rados_cluster recovery backend and the
libganesha_rados_grace shared library for using RADOS storage for
recovery state.
%endif

%if ( 0%{?with_rados_urls} )
%package rados-urls
Summary: The NFS-GANESHA library for use with RADOS URLs
Group: Applications/System
Requires: nfs-ganesha = %{version}-%{release}

%description rados-urls
This package contains the libganesha_rados_urls library used for
handling RADOS URL configurations.
%endif

# Option packages start here. use "rpmbuild --with gpfs" (or equivalent)
# for activating this part of the spec file

# NULL
%if ( 0%{?with_nullfs} )
%package nullfs
Summary: The NFS-GANESHA NULLFS Stackable FSAL
Requires: nfs-ganesha = %{version}-%{release}

%description nullfs
This package contains a Stackable FSAL shared object to
be used with NFS-Ganesha. This is mostly a template for future (more sophisticated) stackable FSALs
%endif

# MEM
%if ( 0%{?with_mem} )
%package mem
Summary: The NFS-GANESHA Memory backed testing FSAL
Requires: nfs-ganesha = %{version}-%{release}

%description mem
This package contains a FSAL shared object to be used with NFS-Ganesha. This
is used for speed and latency testing.
%endif

# GPFS
%if ( 0%{?with_gpfs} )
%package gpfs
Summary: The NFS-GANESHA GPFS FSAL
Requires: nfs-ganesha = %{version}-%{release}

%description gpfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support GPFS backend
%endif

# CEPH
%if ( 0%{?with_ceph} )
%package ceph
Summary: The NFS-GANESHA CephFS FSAL
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	libcephfs-devel >= 12.2.0
BuildRequires:	libacl-devel

%description ceph
This package contains a FSAL shared object to
be used with NFS-Ganesha to support CephFS
%endif

# RGW
%if ( 0%{?with_rgw} )
%package rgw
Summary: The NFS-GANESHA Ceph RGW FSAL
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	librgw-devel >= 12.2.0

%description rgw
This package contains a FSAL shared object to
be used with NFS-Ganesha to support Ceph RGW
%endif

# XFS
%if ( 0%{?with_xfs} )
%package xfs
Summary: The NFS-GANESHA XFS FSAL
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	libattr-devel xfsprogs-devel

%description xfs
This package contains a shared object to be used with FSAL_VFS
to support XFS correctly
%endif

#LUSTRE
%if ( 0%{?with_lustre} )
%package lustre
Summary: The NFS-GANESHA LUSTRE FSAL
BuildRequires: libattr-devel
BuildRequires: lustre-client
Requires: nfs-ganesha = %{version}-%{release}
Requires: lustre-client

%description lustre
This package contains a FSAL shared object to
be used with NFS-Ganesha to support LUSTRE based filesystems
%endif

# KVSFS
%if ( 0%{?with_kvsfs} )
%package kvsfs
Summary: The NFS-GANESHA KVSFS FSAL
Requires:	nfs-ganesha = %{version}-%{release}
Requires:	libkvsns >= 1.2.0
BuildRequires:	libkvsns-devel >= 1.2.0

%description kvsfs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support KVSFS/libkvsns
%endif

# GLUSTER
%if ( 0%{?with_gluster} )
%package gluster
Summary: The NFS-GANESHA GLUSTER FSAL
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	libgfapi-devel >= 7.0
BuildRequires:	libattr-devel, libacl-devel

%description gluster
This package contains a FSAL shared object to
be used with NFS-Ganesha to support Gluster
%endif

# SAUNA
%if ( 0%{?with_saunafs} )
%package saunafs
Summary: The NFS-GANESHA SAUNAFS FSAL
Requires:	nfs-ganesha = %{version}-%{release}

%description saunafs
This package contains a FSAL shared object to
be used with NFS-Ganesha to support Sauna FS
%endif

# SELINUX
%if ( 0%{?fedora} >= 29 || 0%{?rhel} >= 8 )
%package selinux
Summary: The NFS-GANESHA SELINUX targeted policy
BuildArch:	noarch
Requires:	nfs-ganesha = %{version}-%{release}
BuildRequires:	selinux-policy-devel
%{?selinux_requires}

%description selinux
This package contains an selinux policy for running ganesha.nfsd

%post selinux
%selinux_modules_install %{_selinux_store_path}/packages/ganesha.pp.bz2

%pre selinux
%selinux_relabel_pre

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall ganesha
fi

%posttrans
%selinux_relabel_post
%endif


# NTIRPC (if built-in)
%if ! %{?with_system_ntirpc}
%package -n libntirpc
Summary:	New Transport Independent RPC Library
License:	BSD-3-Clause
Version:	@NTIRPC_VERSION_EMBED@
Url:		https://github.com/nfs-ganesha/ntirpc

# libtirpc has /etc/netconfig, most machines probably have it anyway
# for NFS client
Requires:	libtirpc

%if %{with monitoring}
Requires:      ganesha_monitoring
%endif

%description -n libntirpc
This package contains a new implementation of the original libtirpc,
transport-independent RPC (TI-RPC) library for NFS-Ganesha. It has
the following features not found in libtirpc:
 1. Bi-directional operation
 2. Full-duplex operation on the TCP (vc) transport
 3. Thread-safe operating modes
 3.1 new locking primitives and lock callouts (interface change)
 3.2 stateless send/recv on the TCP transport (interface change)
 4. Flexible server integration support
 5. Event channels (remove static arrays of xprt handles, new EPOLL/KEVENT
    integration)

%package -n libntirpc-devel
Summary:	Development headers for libntirpc
Requires:	libntirpc = @NTIRPC_VERSION_EMBED@
License:	BSD-3-Clause
Version:	@NTIRPC_VERSION_EMBED@
Url:		https://github.com/nfs-ganesha/ntirpc

%description -n libntirpc-devel
Development headers and auxiliary files for developing with %{name}.
%endif

%prep
%autosetup -p1

# Create a sysusers.d config file
cat >nfs-ganesha.sysusers.conf <<EOF
u ganesha - 'NFS-Ganesha Daemon' %{_rundir}/ganesha -
EOF

%build
export VERBOSE=1
cd src && %cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo	\
	-DBUILD_CONFIG=rpmbuild				\
	-DCMAKE_COLOR_MAKEFILE:BOOL=OFF			\
	-DUSE_FSAL_NULL=%{use_fsal_null}		\
	-DUSE_FSAL_MEM=%{use_fsal_mem}			\
	-DUSE_FSAL_XFS=%{use_fsal_xfs}			\
	-DUSE_FSAL_LUSTRE=%{use_fsal_lustre}		\
	-DUSE_FSAL_CEPH=%{use_fsal_ceph}		\
	-DUSE_FSAL_RGW=%{use_fsal_rgw}			\
	-DUSE_FSAL_GPFS=%{use_fsal_gpfs}		\
	-DUSE_FSAL_KVSFS=%{use_fsal_kvsfs}		\
	-DUSE_FSAL_GLUSTER=%{use_fsal_gluster}		\
	-DUSE_FSAL_SAUNAFS=%{use_fsal_saunafs}		\
	-DUSE_SYSTEM_NTIRPC=%{use_system_ntirpc}	\
	-DENABLE_QOS=%{use_qos}				\
	-DUSE_9P_RDMA=%{use_rdma}			\
	-DUSE_LTTNG=%{use_lttng}			\
	-DUSE_UNWIND=%{use_unwind}			\
	-DUSE_UNWIND_ENRICHED_BT=%{use_unwind_enriched_bt}	\
	-DUSE_ADMIN_TOOLS=%{use_utils}			\
	-DUSE_GUI_ADMIN_TOOLS=%{use_gui_utils}		\
	-DUSE_RADOS_RECOV=%{use_rados_recov}		\
	-DRADOS_URLS=%{use_rados_urls}			\
	-DUSE_FSAL_VFS=ON				\
	-DENABLE_VFS_POSIX_ACL=YES			\
	-DUSE_FSAL_PROXY_V4=ON				\
	-DUSE_FSAL_PROXY_V3=ON				\
	-DUSE_DBUS=ON					\
	-DUSE_9P=%{use_9P}				\
	-DDISTNAME_HAS_GIT_DATA=OFF			\
	-DUSE_MAN_PAGE=%{use_man_page}			\
	-DRPCBIND=%{use_rpcbind}			\
	-D_MSPAC_SUPPORT=%{use_mspac_support}		\
	-DSANITIZE_ADDRESS=%{use_sanitize_address}	\
	-DUSE_LEGACY_PYTHON_INSTALL=%{use_legacy_python_install} \
%ifarch x86_64 aarch64
       -DCMAKE_LINKER=%{_bindir}/ld.mold                \
%endif
%if ( 0%{?with_jemalloc} )
	-DALLOCATOR=jemalloc
%endif

export GCC_COLORS=
%cmake_build

%if ( 0%{?fedora} >= 30 || 0%{?rhel} >= 8 )
make -C selinux -f /usr/share/selinux/devel/Makefile ganesha.pp
pushd selinux && bzip2 -9 ganesha.pp && popd
%endif

%install
mkdir -p %{buildroot}%{_sysconfdir}/ganesha/
mkdir -p %{buildroot}%{_sysconfdir}/dbus-1/system.d
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_libdir}/ganesha
mkdir -p %{buildroot}%{_rundir}/ganesha
mkdir -p %{buildroot}%{_libexecdir}/ganesha
cd src
install -m 644 config_samples/logrotate_ganesha	%{buildroot}%{_sysconfdir}/logrotate.d/ganesha
install -m 644 scripts/ganeshactl/org.ganesha.nfsd.conf	%{buildroot}%{_sysconfdir}/dbus-1/system.d
install -m 755 scripts/nfs-ganesha-config.sh	%{buildroot}%{_libexecdir}/ganesha
%if ( 0%{?with_9P} )
install -m 755 tools/mount.9P	%{buildroot}%{_sbindir}/mount.9P
%endif
install -m 644 config_samples/vfs.conf %{buildroot}%{_sysconfdir}/ganesha
%if ( 0%{?with_rgw} )
install -m 644 config_samples/rgw.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

mkdir -p %{buildroot}%{_unitdir}
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
mkdir -p %{buildroot}%{_unitdir}/nfs-ganesha-lock.service.d
%endif

install -m 644 scripts/systemd/nfs-ganesha.service.el7	%{buildroot}%{_unitdir}/nfs-ganesha.service
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
install -m 644 scripts/systemd/nfs-ganesha-lock.service.el8    %{buildroot}%{_unitdir}/nfs-ganesha-lock.service
install -m 644 scripts/systemd/rpc-statd.conf.el8      %{buildroot}%{_unitdir}/nfs-ganesha-lock.service.d/rpc-statd.conf
%else
install -m 644 scripts/systemd/nfs-ganesha-lock.service.el7	%{buildroot}%{_unitdir}/nfs-ganesha-lock.service
%endif
install -m 644 scripts/systemd/nfs-ganesha-config.service	%{buildroot}%{_unitdir}/nfs-ganesha-config.service
install -m 644 scripts/systemd/sysconfig/nfs-ganesha	%{buildroot}%{_sysconfdir}/sysconfig/ganesha
mkdir -p %{buildroot}%{_localstatedir}/log/ganesha

%if ( 0%{?with_lustre} )
install -m 644 config_samples/lustre.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

%if ( 0%{?with_xfs} )
install -m 644 config_samples/xfs.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

%if ( 0%{?with_ceph} )
install -m 644 config_samples/ceph.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

%if ( 0%{?with_rgw} )
install -m 644 config_samples/rgw.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/rgw_bucket.conf %{buildroot}%{_sysconfdir}/ganesha
%endif

%if ( 0%{?with_gluster} )
install -m 644 config_samples/logrotate_fsal_gluster %{buildroot}%{_sysconfdir}/logrotate.d/ganesha-gfapi
%endif

%if ( 0%{?with_gpfs} )
install -m 644 config_samples/gpfs.conf	%{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.nfsd.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.main.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.log.conf %{buildroot}%{_sysconfdir}/ganesha
install -m 644 config_samples/gpfs.ganesha.exports.conf	%{buildroot}%{_sysconfdir}/ganesha
%endif

%cmake_install

%if ( 0%{?fedora} >= 30 || 0%{?rhel} >= 8 )
install -d %{buildroot}%{_selinux_store_path}/packages
install -d -p %{buildroot}%{_selinux_store_path}/devel/include/contrib
install -p -m 644 selinux/ganesha.if %{buildroot}%{_selinux_store_path}/devel/include/contrib
install -m 0644 selinux/ganesha.pp.bz2 %{buildroot}%{_selinux_store_path}/packages
%endif

%if ( ! 0%{?with_legacy_python_install} )
%if ( 0%{?with_gpfs} )
mv %{buildroot}/usr/bin/gpfs-epoch %{buildroot}/usr/libexec/ganesha/
%endif
%endif

%if ( 0%{?rhel} && 0%{?rhel} < 8 )
rm -rf %{buildroot}/%{python_sitelib}/gpfs*
rm -f %{buildroot}/%{python_sitelib}/__init__.*
%else
rm -rf %{buildroot}/%{python3_sitelib}/gpfs*
rm -rf %{buildroot}/%{python3_sitelib}/ganeshactl*
rm -f %{buildroot}/%{python3_sitelib}/__init__.*
rm -rf %{buildroot}/%{python3_sitelib}/__pycache__
rm -f %{buildroot}/%{python3_sitelib}/Ganesha/__init__.*
rm -f %{buildroot}/%{python3_sitelib}/Ganesha/QtUI/__init__.*
rm -rf %{buildroot}/%{python3_sitelib}/Ganesha/QtUI/__pycache__
%endif

install -m0644 -D ../nfs-ganesha.sysusers.conf %{buildroot}%{_sysusersdir}/nfs-ganesha.conf

%post
%if ( 0%{?suse_version} )
%service_add_post nfs-ganesha.service nfs-ganesha-lock.service nfs-ganesha-config.service
%else
%if ( 0%{?fedora} || ( 0%{?rhel} && 0%{?rhel} > 6 ) )
semanage fcontext -a -t ganesha_var_log_t %{_localstatedir}/log/ganesha > /dev/null 2>&1 || :
semanage fcontext -a -t ganesha_var_log_t %{_localstatedir}/log/ganesha/ganesha.log > /dev/null 2>&1 || :
%if ( 0%{?with_gluster} )
semanage fcontext -a -t ganesha_var_log_t %{_localstatedir}/log/ganesha/ganesha-gfapi.log > /dev/null 2>&1 || :
%endif
restorecon %{_localstatedir}/log/ganesha
%endif
%systemd_post nfs-ganesha.service
%systemd_post nfs-ganesha-lock.service
%systemd_post nfs-ganesha-config.service
%endif
killall -SIGHUP dbus-daemon >/dev/null 2>&1 || :


%preun
%if ( 0%{?suse_version} )
%service_del_preun nfs-ganesha-lock.service
%else
%systemd_preun nfs-ganesha-lock.service
%endif

%postun
%if ( 0%{?suse_version} )
%service_del_postun nfs-ganesha-lock.service
%debug_package
%else
%systemd_postun_with_restart nfs-ganesha-lock.service
%endif

%files
%license src/LICENSE.txt
%{_bindir}/ganesha.nfsd
%{_libdir}/libganesha_nfsd.so*
%config %{_sysconfdir}/dbus-1/system.d/org.ganesha.nfsd.conf
%config(noreplace) %{_sysconfdir}/sysconfig/ganesha
%config(noreplace) %{_sysconfdir}/logrotate.d/ganesha
%dir %{_sysconfdir}/ganesha/
%config(noreplace) %{_sysconfdir}/ganesha/ganesha.conf
%dir %{_rundir}/ganesha
%dir %{_libexecdir}/ganesha/
%{_libexecdir}/ganesha/nfs-ganesha-config.sh
%dir %attr(0755,ganesha,ganesha) %{_localstatedir}/log/ganesha

%{_unitdir}/nfs-ganesha.service
%{_unitdir}/nfs-ganesha-lock.service
%{_unitdir}/nfs-ganesha-config.service
%if ( 0%{?fedora} ) || ( 0%{?rhel} && 0%{?rhel} >= 8 )
%{_unitdir}/nfs-ganesha-lock.service.d/rpc-statd.conf
%endif

%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-config.8.gz
%{_mandir}/*/ganesha-core-config.8.gz
%{_mandir}/*/ganesha-export-config.8.gz
%{_mandir}/*/ganesha-cache-config.8.gz
%{_mandir}/*/ganesha-log-config.8.gz
%endif
%{_sysusersdir}/nfs-ganesha.conf

%if ( 0%{?with_rados_recov} )
%files rados-grace
%{_bindir}/ganesha-rados-grace
%{_libdir}/libganesha_rados_recov.so*
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-rados-grace.8.gz
%{_mandir}/*/ganesha-rados-cluster-design.8.gz
%endif
%endif

%if %{with qos}
%{_mandir}/*/ganesha-qos-config.8.gz
%endif

%if ( 0%{?with_rados_urls} )
%files rados-urls
%{_libdir}/libganesha_rados_urls.so*
%endif

%if ( 0%{?with_9P} )
%files mount-9P
%{_sbindir}/mount.9P
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-9p-config.8.gz
%endif
%endif

%files -n ganesha_monitoring
%{_libdir}/libganesha_monitoring*

%files vfs
%{_libdir}/ganesha/libfsalvfs*
%config(noreplace) %{_sysconfdir}/ganesha/vfs.conf
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-vfs-config.8.gz
%endif

%files proxy-v4
%{_libdir}/ganesha/libfsalproxy_v4*
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-proxy-v4-config.8.gz
%endif

%files proxy-v3
%{_libdir}/ganesha/libfsalproxy_v3*
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-proxy-v3-config.8.gz
%endif

# Optional packages
%if ( 0%{?with_lustre} )
%files lustre
%{_libdir}/ganesha/libfsallustre*
%config(noreplace) %{_sysconfdir}/ganesha/lustre.conf
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-lustre-config.8.gz
%endif
%endif

%if ( 0%{?with_nullfs} )
%files nullfs
%{_libdir}/ganesha/libfsalnull*
%endif

%if ( 0%{?with_mem} )
%files mem
%{_libdir}/ganesha/libfsalmem*
%endif

%if ( 0%{?with_gpfs} )
%files gpfs
%{_libdir}/ganesha/libfsalgpfs*
%{_libexecdir}/ganesha/gpfs-epoch
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.conf
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.ganesha.nfsd.conf
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.ganesha.main.conf
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.ganesha.log.conf
%config(noreplace) %{_sysconfdir}/ganesha/gpfs.ganesha.exports.conf
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-gpfs-config.8.gz
%endif
%endif

%if ( 0%{?with_xfs} )
%files xfs
%{_libdir}/ganesha/libfsalxfs*
%config(noreplace) %{_sysconfdir}/ganesha/xfs.conf
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-xfs-config.8.gz
%endif
%endif

%if ( 0%{?with_ceph} )
%files ceph
%{_libdir}/ganesha/libfsalceph*
%config(noreplace) %{_sysconfdir}/ganesha/ceph.conf
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-ceph-config.8.gz
%endif
%endif

%if ( 0%{?with_rgw} )
%files rgw
%{_libdir}/ganesha/libfsalrgw*
%config(noreplace) %{_sysconfdir}/ganesha/rgw.conf
%config(noreplace) %{_sysconfdir}/ganesha/rgw_bucket.conf
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-rgw-config.8.gz
%endif
%endif

%if ( 0%{?with_gluster} )
%files gluster
%config(noreplace) %{_sysconfdir}/logrotate.d/ganesha-gfapi
%{_libdir}/ganesha/libfsalgluster*
%if ( 0%{?with_man_page} )
%{_mandir}/*/ganesha-gluster-config.8.gz
%endif
%endif

%if ( 0%{?with_saunafs} )
%files saunafs
%{_libdir}/ganesha/libfsalsaunafs*
%endif

%if ( 0%{?fedora} >= 30 || 0%{?rhel} >= 8 )
%files selinux
%attr(0644,root,root) %{_selinux_store_path}/packages/ganesha.pp.bz2
%attr(0644,root,root) %{_selinux_store_path}/devel/include/contrib/ganesha.if
%endif

%if ! %{?with_system_ntirpc}
%files -n libntirpc
%{_libdir}/libntirpc.so.@NTIRPC_VERSION_EMBED@
%{_libdir}/libntirpc.so.4.0
%{_libdir}/libntirpc.so
%{!?_licensedir:%global license %%doc}
%license libntirpc/COPYING
%doc libntirpc/NEWS libntirpc/README
%files -n libntirpc-devel
%{_libdir}/pkgconfig/libntirpc.pc
%dir %{_includedir}/ntirpc
%{_includedir}/ntirpc/*
%endif

%if ( 0%{?with_kvsfs} )
%files kvsfs
%{_libdir}/ganesha/libfsalkvsfs*
%endif

%if ( 0%{?with_lttng} )
%files lttng
%{_libdir}/libganesha_trace*
%if ! %{with system_ntirpc}
%{_libdir}/libntirpc_tracepoints.so
%endif
%endif

%if ( 0%{?with_utils} )
%files utils
%if ( 0%{?rhel} && 0%{?rhel} < 8 )
%{python_sitelib}/Ganesha/*
%{python_sitelib}/ganeshactl-*-info
%endif
%if ( 0%{?with_gui_utils} )
%{_bindir}/ganesha-admin
%{_bindir}/manage_clients
%{_bindir}/manage_exports
%{_bindir}/manage_logger
%{_bindir}/ganeshactl
%{python3_sitelib}/Ganesha/*
%if ( 0%{?with_9P} )
%{_bindir}/client_stats_9pOps
%{_bindir}/export_stats_9pOps
%else
%exclude %{_bindir}/client_stats_9pOps
%exclude %{_bindir}/export_stats_9pOps
%endif
%endif
%{_bindir}/fake_recall
%{_bindir}/get_clientids
%{_bindir}/grace_period
%{_bindir}/ganesha_stats
%{_bindir}/sm_notify.ganesha
%{_bindir}/ganesha_mgr
%{_bindir}/ganesha_logrotate_mgr
%{_bindir}/ganesha_conf
%{_mandir}/*/ganesha_conf.8.gz
%endif

%changelog
* Wed Nov 19 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 7.2-2
- NFS-Ganesha 8.1, rpc-statd unitdir

* Tue Sep 30 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 7.2-1
- NFS-Ganesha 7.2 GA

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 7.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.0-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 30 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 7.0-1
- NFS-Ganesha 7.0 GA

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 4 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 6.5-5
- logrotate rbhz#2367645, selinux mods 

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 6.5-4
- Rebuilt for Python 3.14

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 6.5-3
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 9 2025 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 6.5-1
- NFS-Ganesha 6.5 GA

* Mon Dec 16 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 6.4-1
- NFS-Ganesha 6.4 GA

* Mon Nov 25 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 6.3-1
- NFS-Ganesha 6.3 GA

* Mon Oct 21 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 6.2-1
- NFS-Ganesha 6.2 GA

* Mon Sep 30 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 6.1-1
- NFS-Ganesha 6.1 GA

* Thu Aug 29 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 6.0-2
- NFS-Ganesha 6.0, enable rgw

* Mon Aug 26 2024 Kaleb S. KEITHLEY <kkeithle at redhat.com> - 6.0-1
- NFS-Ganesha 6.0 GA, rhbz#2307961
