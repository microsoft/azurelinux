%define arches_qemu_kvm         %{ix86} x86_64 %{power64} %{arm} aarch64 s390x

%define arches_64bit            x86_64 %{power64} aarch64 s390x riscv64
%define arches_x86              %{ix86} x86_64

%define arches_systemtap_64bit  %{arches_64bit}
%define arches_dmidecode        %{arches_x86}
%define arches_xen              %{arches_x86} aarch64
%define arches_vbox             %{arches_x86}
%define arches_ceph             %{arches_64bit}
%define arches_zfs              %{arches_x86} %{power64} %{arm}
%define arches_numactl          %{arches_x86} %{power64} aarch64 s390x
%define arches_numad            %{arches_x86} %{power64} aarch64

# The hypervisor drivers that run in libvirtd
%define with_qemu          0%{!?_without_qemu:1}
%define with_lxc           0%{!?_without_lxc:1}
%define with_libxl         0%{!?_without_libxl:1}
%define with_vbox          0%{!?_without_vbox:1}

%ifarch %{arches_qemu_kvm}
    %define with_qemu_kvm      %{with_qemu}
%else
    %define with_qemu_kvm      0
%endif

%define with_qemu_tcg      %{with_qemu}

%if ! %{with_qemu_tcg} && ! %{with_qemu_kvm}
    %define with_qemu 0
%endif

# Then the hypervisor drivers that run outside libvirtd, in libvirt.so
%define with_openvz        0%{!?_without_openvz:1}
%define with_vmware        0%{!?_without_vmware:1}
%define with_esx           0%{!?_without_esx:1}
%define with_hyperv        0%{!?_without_hyperv:1}

# azl: to maintain azl2.0 settings, explicitly disable curl
# and enable driver_esx by setting with_esx=0
%define with_esx           0

# Then the secondary host drivers, which run inside libvirtd
%define with_storage_rbd      0%{!?_without_storage_rbd:1}
# azl: for azl3.0 preview, disable ceph dependencies
%define with_storage_rbd      0

%define with_storage_gluster 0%{!?_without_storage_gluster:1}

%define with_storage_zfs      0

%define with_storage_iscsi_direct 0%{!?_without_storage_iscsi_direct:1}
# azl: to maintain azl2.0 settings, explicitly disable iscsi
# by setting with_storage_iscsi_direct=0
%define with_storage_iscsi_direct 0

# Other optional features
%define with_numactl          0%{!?_without_numactl:1}

# A few optional bits off by default, we enable later
%define with_fuse             0
%define with_sanlock          0
%define with_numad            0
%define with_nbdkit           0
%define with_nbdkit_config_default 0
%define with_firewalld_zone   0
%define with_netcf            0
%define with_libssh2          0
%define with_wireshark        0
%define with_libssh           0
%define with_dmidecode        0

# Finally set the OS / architecture specific special cases

# Architecture-dependent features
%ifnarch %{arches_xen}
    %define with_libxl 0
%endif
%ifnarch %{arches_vbox}
    %define with_vbox 0
%endif
%ifnarch %{arches_numactl}
    %define with_numactl 0
%endif
%ifnarch %{arches_zfs}
    %define with_storage_zfs 0
%endif
%ifnarch %{arches_ceph}
    %define with_storage_rbd 0
%endif

%define with_openvz 0
%define with_vbox 0
%define with_vmware 0
%define with_libxl 0
%define with_hyperv 0
%define with_lxc 0

%define with_netcf 0

# fuse is used to provide virtualized /proc for LXC
%if %{with_lxc}
    %define with_fuse      0%{!?_without_fuse:1}
%endif
# azl: to maintain azl2.0 settings, explicitly enable fuse
# by setting with_fuse=1
%define with_fuse 1

# Enable sanlock library for lock management with QEMU
# Sanlock is available only on arches where kvm is available for RHEL
%define with_sanlock 0%{!?_without_sanlock:1}

# Enable libssh2 transport for new enough distros
# azl: to maintain azl2.0 settings, explicitly enable libssh2
# by setting with_libssh2=1
%define with_libssh2 1

# Enable wireshark plugins for all distros
# azl: to maintain azl2.0 settings, explicitly disnable wireshark
# by setting _with_wireshark=0
%define with_wireshark 0
%define wireshark_plugindir %(pkg-config --variable plugindir wireshark)/epan

# Enable libssh transport for all distros
%define with_libssh 0%{!?_without_libssh:1}
# azl: to maintain azl2.0 settings, explicitly disable libssh
# by setting with_libssh=0
%define with_libssh 0

%if %{with_qemu} || %{with_lxc}
# numad is used to manage the CPU and memory placement dynamically,
# it's not available on many non-x86 architectures.
    %ifarch %{arches_numad}
        %define with_numad    0%{!?_without_numad:1}
    %endif
%endif

%ifarch %{arches_dmidecode}
    %define with_dmidecode 0%{!?_without_dmidecode:1}
%endif

%define with_modular_daemons 0

# Force QEMU to run as non-root
%define qemu_user  qemu
%define qemu_group  qemu

# Locations for QEMU data
%define qemu_moddir %{_libdir}/qemu
%define qemu_datadir %{_datadir}/qemu

# Native builds
%define with_native 0%{!?_without_native:1}

%if !%{with_native}
    # Building the debugsource package apparently only works if the
    # native build is enabled. debuginfo packages don't have this
    # problem and setting this doesn't disable them
    %global debug_package %{nil}
%endif

%define enable_werror -Dwerror=false -Dgit_werror=disabled

%define tls_priority "@LIBVIRT,SYSTEM"

# libvirt 8.1.0 stops distributing any sysconfig files.
# If the user has customized their sysconfig file,
# the RPM upgrade path will rename it to .rpmsave
# because the file is no longer managed by RPM.
# To prevent a regression we rename it back after the
# transaction to preserve the user's modifications
%define libvirt_sysconfig_pre() \
    for sc in %{?*} ; do \
        test -f "%{_sysconfdir}/sysconfig/${sc}.rpmsave" || continue ; \
        mv -v "%{_sysconfdir}/sysconfig/${sc}.rpmsave" "%{_sysconfdir}/sysconfig/${sc}.rpmsave.old" ; \
    done \
    %{nil}
%define libvirt_sysconfig_posttrans() \
    for sc in %{?*} ; do \
        test -f "%{_sysconfdir}/sysconfig/${sc}.rpmsave" || continue ; \
        mv -v "%{_sysconfdir}/sysconfig/${sc}.rpmsave" "%{_sysconfdir}/sysconfig/${sc}" ; \
    done \
    %{nil}

Summary:        Library providing a simple virtualization API
Name:           libvirt
Version:        10.0.0
Release:        3%{?dist}
License:        GPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND OFL-1.1
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Virtualization/Libraries
URL:            https://libvirt.org/
%if %(echo %{version} | grep -q "\.0$"; echo $?) == 1
    %define mainturl stable_updates/
%endif
Source:         https://download.libvirt.org/%{?mainturl}libvirt-%{version}.tar.xz
Patch0:         libvirt-conf.patch

Requires: libvirt-daemon = %{version}-%{release}
Requires: libvirt-daemon-config-network = %{version}-%{release}
Requires: libvirt-daemon-config-nwfilter = %{version}-%{release}
%if %{with_libxl}
Requires: libvirt-daemon-driver-libxl = %{version}-%{release}
%endif
%if %{with_lxc}
Requires: libvirt-daemon-driver-lxc = %{version}-%{release}
%endif
%if %{with_qemu}
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
Requires: libvirt-client-qemu = %{version}-%{release}
%endif
# We had UML driver, but we've removed it.
Obsoletes: libvirt-daemon-driver-uml <= 5.0.0
Obsoletes: libvirt-daemon-uml <= 5.0.0
%if %{with_vbox}
Requires: libvirt-daemon-driver-vbox = %{version}-%{release}
%endif
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-client = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}

# All build-time requirements. Run-time requirements are
# listed against each sub-RPM
BuildRequires: python3-docutils
BuildRequires: meson >= 0.56.0
BuildRequires: ninja-build
BuildRequires: git
BuildRequires: perl-interpreter
BuildRequires: python3
BuildRequires: python3-pytest
BuildRequires: python3-pip
# For xmllint
BuildRequires: libxml2
# For xsltproc
BuildRequires: libxslt
BuildRequires: gettext
BuildRequires: systemd-rpm-macros
# Fedora build root suckage
BuildRequires: gawk
%if %{with_native}
BuildRequires: gcc
    %if %{with_libxl}
BuildRequires: xen-devel
    %endif
BuildRequires: glib2-devel >= 2.56
BuildRequires: libxml2-devel
BuildRequires: readline-devel
BuildRequires: bash-completion >= 2.0
BuildRequires: libtasn1-devel
BuildRequires: gnutls-devel
BuildRequires: libattr-devel
# For pool-build probing for existing pools
BuildRequires: libblkid-devel >= 2.17
# for augparse, optionally used in testing
BuildRequires: augeas
BuildRequires: systemd-devel >= 185
BuildRequires: libpciaccess-devel >= 0.10.9
BuildRequires: yajl-devel
    %if %{with_sanlock}
BuildRequires: sanlock-devel >= 2.4
    %endif
BuildRequires: libpcap-devel >= 1.5.0
BuildRequires: libnl3-devel
BuildRequires: libselinux-devel
BuildRequires: iptables
BuildRequires: ebtables
# For modprobe
BuildRequires: kmod
BuildRequires: cyrus-sasl-devel
BuildRequires: polkit >= 0.112
# For mount/umount in FS driver
BuildRequires: util-linux
    %if %{with_qemu}
# For managing ACLs
BuildRequires: libacl-devel
# From QEMU RPMs, used by virstoragetest
BuildRequires: qemu-img
    %endif
# nbdkit support requires libnbd
    %if %{with_nbdkit}
BuildRequires: libnbd-devel
    %endif
# For LVM drivers
BuildRequires: lvm2
# For pool type=iscsi
BuildRequires: iscsi-initiator-utils
    %if %{with_storage_iscsi_direct}
# For pool type=iscsi-direct
BuildRequires: libiscsi-devel
    %endif
# For disk driver
BuildRequires: parted-devel
# For Multipath support
BuildRequires: device-mapper-devel
    %if %{with_storage_rbd}
BuildRequires: librados2-devel
BuildRequires: librbd1-devel
    %endif
    %if %{with_storage_gluster}
BuildRequires: glusterfs-api-devel >= 3.4.1
BuildRequires: glusterfs-devel >= 3.4.1
    %endif
    %if %{with_numactl}
# For QEMU/LXC numa info
BuildRequires: numactl-devel
    %endif
BuildRequires: libcap-ng-devel >= 0.5.0
    %if %{with_fuse}
BuildRequires: fuse-devel >= 2.8.6
    %endif
    %if %{with_libssh2}
BuildRequires: libssh2-devel >= 1.3.0
    %endif
    %if %{with_netcf}
BuildRequires: netcf-devel >= 0.2.2
    %endif
    %if %{with_esx}
BuildRequires: libcurl-devel
    %endif
    %if %{with_hyperv}
BuildRequires: libwsman-devel >= 2.6.3
    %endif
BuildRequires: audit-libs-devel
# we need /usr/sbin/dtrace
BuildRequires: systemtap-sdt-devel
# For mount/umount in FS driver
BuildRequires: util-linux
# For showmount in FS driver (netfs discovery)
BuildRequires: nfs-utils
    %if %{with_numad}
BuildRequires: numad
    %endif
    %if %{with_wireshark}
# was disabled before ... stay disabled?
BuildRequires: wireshark-devel
    %endif
    %if %{with_libssh}
BuildRequires: libssh-devel >= 0.8.1
    %endif
BuildRequires: libtirpc-devel
    %if %{with_firewalld_zone}
# Needed for the firewalld_reload macro
BuildRequires: firewalld-filesystem
    %endif
%endif

%description
Libvirt is a C toolkit to interact with the virtualization capabilities
of recent versions of Linux (and other OSes). The main package includes
the libvirtd server exporting the virtualization support.

%if %{with_native}
%package docs
Summary: API reference and website documentation

%description docs
Includes the API reference for the libvirt C library, and a complete
copy of the libvirt.org website documentation.

%package daemon
Summary: Server side daemon and supporting files for libvirt library

# All runtime requirements for the libvirt package (runtime requrements
# for subpackages are listed later in those subpackages)

# The client side, i.e. shared libs are in a subpackage
Requires: libvirt-libs = %{version}-%{release}
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-daemon-lock = %{version}-%{release}
Requires: libvirt-daemon-plugin-lockd = %{version}-%{release}
Requires: libvirt-daemon-log = %{version}-%{release}
Requires: libvirt-daemon-proxy = %{version}-%{release}

%description daemon
Server side daemon required to manage the virtualization capabilities
of recent versions of Linux. Requires a hypervisor specific sub-RPM
for specific drivers.

%package daemon-common
Summary: Files and utilities used by daemons
Requires: libvirt-libs = %{version}-%{release}
# The libvirt-guests.sh script requires virsh from libvirt-client subpackage,
# but not every deployment wants to use libvirt-guests service. Using
# Recommends here will install libvirt-client by default (if available), but
# RPM won't complain if the package is unavailable, masked, or removed later.
Recommends: libvirt-client = %{version}-%{release}
# for /sbin/ip
Requires: iproute
Requires: iproute-tc
Requires: polkit >= 0.112
    %if %{with_dmidecode}
# For virConnectGetSysinfo
Requires: dmidecode
    %endif
# For service management
# azl has systemd-bootstrap which also provides /usr/bin/sysctl, explicitly request full systemd.
Requires(posttrans): systemd
Requires(preun):  systemd
# libvirtd depends on 'messagebus' service
Requires: dbus
# For uid creation during pre
Requires(pre): shadow-utils
# Needed by /usr/libexec/libvirt-guests.sh script.
Requires: gettext

# Ensure smooth upgrades
Obsoletes: libvirt-admin < 7.3.0
Provides: libvirt-admin = %{version}-%{release}
Obsoletes: libvirt-bash-completion < 7.3.0

%description daemon-common
Miscellaneous files and utilities used by other libvirt daemons

%package daemon-lock
Summary: Server side daemon for managing locks
Requires: libvirt-libs = %{version}-%{release}

%description daemon-lock
Server side daemon used to manage locks held against virtual machine
resources

%package daemon-plugin-lockd
Summary: lockd client plugin for virtlockd
Requires: libvirt-libs = %{version}-%{release}
Requires: libvirt-daemon-lock = %{version}-%{release}

%description daemon-plugin-lockd
A client-side plugin that implements disk locking using POSIX fcntl advisory
locks via communication with the virtlockd daemon

%package daemon-log
Summary: Server side daemon for managing logs
Requires: libvirt-libs = %{version}-%{release}

%description daemon-log
Server side daemon used to manage logs from virtual machine consoles

%package daemon-proxy
Summary: Server side daemon providing libvirtd proxy
Requires: libvirt-libs = %{version}-%{release}
# netcat is needed on the server side so that clients that have
# libvirt < 6.9.0 can connect, but newer versions will prefer
# virt-ssh-helper. Making this a Recommends means that it gets
# installed by default, but can still be removed if compatibility
# with old clients is not required
Recommends: /usr/bin/nc

%description daemon-proxy
Server side daemon providing functionality previously provided by
the monolithic libvirtd

%package daemon-config-network
Summary: Default configuration files for the libvirtd daemon

Requires: libvirt-daemon-driver-network = %{version}-%{release}

%description daemon-config-network
Default configuration files for setting up NAT based networking

%package daemon-config-nwfilter
Summary: Network filter configuration files for the libvirtd daemon

Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}

%description daemon-config-nwfilter
Network filter configuration files for cleaning guest traffic

%package daemon-driver-network
Summary: Network driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: dnsmasq >= 2.41
Requires: iptables

%description daemon-driver-network
The network driver plugin for the libvirtd daemon, providing
an implementation of the virtual network APIs using the Linux
bridge capabilities.

%package daemon-driver-nwfilter
Summary: Nwfilter driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: iptables
Requires: ebtables

%description daemon-driver-nwfilter
The nwfilter driver plugin for the libvirtd daemon, providing
an implementation of the firewall APIs using the ebtables,
iptables and ip6tables capabilities

%package daemon-driver-nodedev
Summary: Nodedev driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
# needed for device enumeration
Requires: systemd >= 185
Requires: mdevctl
# for modprobe of pci devices
Requires: module-init-tools

%description daemon-driver-nodedev
The nodedev driver plugin for the libvirtd daemon, providing
an implementation of the node device APIs using the udev
capabilities.

%package daemon-driver-interface
Summary: Interface driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
    %if %{with_netcf}
Requires: netcf-libs >= 0.2.2
    %endif

%description daemon-driver-interface
The interface driver plugin for the libvirtd daemon, providing
an implementation of the host network interface APIs.

%package daemon-driver-secret
Summary: Secret driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}

%description daemon-driver-secret
The secret driver plugin for the libvirtd daemon, providing
an implementation of the secret key APIs.

%package daemon-driver-storage-core
Summary: Storage driver plugin including base backends for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: nfs-utils
# For mkfs
Requires: util-linux
# For storage wiping with different algorithms
Requires: scrub
    %if %{with_qemu}
# From QEMU RPMs
Requires: qemu-img
    %endif
    %if !%{with_storage_rbd}
Obsoletes: libvirt-daemon-driver-storage-rbd < 5.2.0
    %endif
Obsoletes: libvirt-daemon-driver-storage-sheepdog < 8.8.0

%description daemon-driver-storage-core
The storage driver plugin for the libvirtd daemon, providing
an implementation of the storage APIs using files, local disks, LVM, SCSI,
iSCSI, and multipath storage.

%package daemon-driver-storage-logical
Summary: Storage driver plugin for lvm volumes
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: lvm2

%description daemon-driver-storage-logical
The storage driver backend adding implementation of the storage APIs for block
volumes using lvm.

%package daemon-driver-storage-disk
Summary: Storage driver plugin for disk
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: parted
Requires: device-mapper

%description daemon-driver-storage-disk
The storage driver backend adding implementation of the storage APIs for block
volumes using the host disks.

%package daemon-driver-storage-scsi
Summary: Storage driver plugin for local scsi devices
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}

%description daemon-driver-storage-scsi
The storage driver backend adding implementation of the storage APIs for scsi
host devices.

%package daemon-driver-storage-iscsi
Summary: Storage driver plugin for iscsi
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: iscsi-initiator-utils

%description daemon-driver-storage-iscsi
The storage driver backend adding implementation of the storage APIs for iscsi
volumes using the host iscsi stack.

    %if %{with_storage_iscsi_direct}
%package daemon-driver-storage-iscsi-direct
Summary: Storage driver plugin for iscsi-direct
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}

%description daemon-driver-storage-iscsi-direct
The storage driver backend adding implementation of the storage APIs for iscsi
volumes using libiscsi direct connection.
    %endif

%package daemon-driver-storage-mpath
Summary: Storage driver plugin for multipath volumes
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: device-mapper

%description daemon-driver-storage-mpath
The storage driver backend adding implementation of the storage APIs for
multipath storage using device mapper.

    %if %{with_storage_gluster}
%package daemon-driver-storage-gluster
Summary: Storage driver plugin for gluster
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: glusterfs-client >= 2.0.1

%description daemon-driver-storage-gluster
The storage driver backend adding implementation of the storage APIs for gluster
volumes using libgfapi.
    %endif

    %if %{with_storage_rbd}
%package daemon-driver-storage-rbd
Summary: Storage driver plugin for rbd
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}

%description daemon-driver-storage-rbd
The storage driver backend adding implementation of the storage APIs for rbd
volumes using the ceph protocol.
    %endif

    %if %{with_storage_zfs}
%package daemon-driver-storage-zfs
Summary: Storage driver plugin for ZFS
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
# Support any conforming implementation of zfs
Requires: /sbin/zfs
Requires: /sbin/zpool

%description daemon-driver-storage-zfs
The storage driver backend adding implementation of the storage APIs for
ZFS volumes.
    %endif

%package daemon-driver-storage
Summary: Storage driver plugin including all backends for the libvirtd daemon
Requires: libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires: libvirt-daemon-driver-storage-disk = %{version}-%{release}
Requires: libvirt-daemon-driver-storage-logical = %{version}-%{release}
Requires: libvirt-daemon-driver-storage-scsi = %{version}-%{release}
Requires: libvirt-daemon-driver-storage-iscsi = %{version}-%{release}
Requires: libvirt-daemon-driver-storage-mpath = %{version}-%{release}
    %if %{with_storage_iscsi_direct}
Requires: libvirt-daemon-driver-storage-iscsi-direct = %{version}-%{release}
    %endif
    %if %{with_storage_gluster}
Requires: libvirt-daemon-driver-storage-gluster = %{version}-%{release}
    %endif
    %if %{with_storage_rbd}
Requires: libvirt-daemon-driver-storage-rbd = %{version}-%{release}
    %endif
    %if %{with_storage_zfs}
Requires: libvirt-daemon-driver-storage-zfs = %{version}-%{release}
    %endif

%description daemon-driver-storage
The storage driver plugin for the libvirtd daemon, providing
an implementation of the storage APIs using LVM, iSCSI,
parted and more.

    %if %{with_qemu}
%package daemon-driver-qemu
Summary: QEMU driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-daemon-log = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Requires: qemu-img
# For image compression
Requires: gzip
Requires: bzip2
Requires: lzop
Requires: xz
Requires: swtpm-tools
        %if %{with_numad}
Requires: numad
        %endif
# azl: Upstream libivirt.spec.in adds Recommends for passt and
#      passt-selinux here.  This is omitted for now, decision can
#      be revisited.
        %if %{with_nbdkit}
Recommends: nbdkit
Recommends: nbdkit-curl-plugin
Recommends: nbdkit-ssh-plugin
        %endif

%description daemon-driver-qemu
The qemu driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
QEMU
    %endif

    %if %{with_lxc}
%package daemon-driver-lxc
Summary: LXC driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
# There really is a hard cross-driver dependency here
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: systemd-container
# for modprobe of nbd driver
Requires: module-init-tools
        %if %{with_numad}
Requires: numad
        %endif

%description daemon-driver-lxc
The LXC driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
the Linux kernel
    %endif

    %if %{with_vbox}
%package daemon-driver-vbox
Summary: VirtualBox driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}

%description daemon-driver-vbox
The vbox driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
VirtualBox
    %endif

    %if %{with_libxl}
%package daemon-driver-libxl
Summary: Libxl driver plugin for the libvirtd daemon
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-libs = %{version}-%{release}
Obsoletes: libvirt-daemon-driver-xen < 4.3.0

%description daemon-driver-libxl
The Libxl driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
Libxl
    %endif

    %if %{with_qemu_tcg}
%package daemon-qemu
Summary: Server side daemon & driver required to run QEMU guests

        %if %{with_modular_daemons}
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-daemon-log = %{version}-%{release}
Requires: libvirt-daemon-lock = %{version}-%{release}
Requires: libvirt-daemon-plugin-lockd = %{version}-%{release}
Requires: libvirt-daemon-proxy = %{version}-%{release}
Recommends: libvirt-daemon = %{version}-%{release}
        %else
Requires: libvirt-daemon = %{version}-%{release}
        %endif
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
Requires: qemu-kvm

%description daemon-qemu
Server side daemon and driver required to manage the virtualization
capabilities of the QEMU TCG emulators
    %endif

    %if %{with_qemu_kvm}
%package daemon-kvm
Summary: Server side daemon & driver required to run KVM guests

        %if %{with_modular_daemons}
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-daemon-log = %{version}-%{release}
Requires: libvirt-daemon-lock = %{version}-%{release}
Requires: libvirt-daemon-plugin-lockd = %{version}-%{release}
Requires: libvirt-daemon-proxy = %{version}-%{release}
Recommends: libvirt-daemon = %{version}-%{release}
        %else
Requires: libvirt-daemon = %{version}-%{release}
        %endif
Requires: libvirt-daemon-driver-qemu = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
Requires: qemu-kvm

%description daemon-kvm
Server side daemon and driver required to manage the virtualization
capabilities of the KVM hypervisor
    %endif

    %if %{with_lxc}
%package daemon-lxc
Summary: Server side daemon & driver required to run LXC guests

        %if %{with_modular_daemons}
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-daemon-proxy = %{version}-%{release}
Recommends: libvirt-daemon = %{version}-%{release}
        %else
Requires: libvirt-daemon = %{version}-%{release}
        %endif
Requires: libvirt-daemon-driver-lxc = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}

%description daemon-lxc
Server side daemon and driver required to manage the virtualization
capabilities of LXC
    %endif

    %if %{with_libxl}
%package daemon-xen
Summary: Server side daemon & driver required to run XEN guests

        %if %{with_modular_daemons}
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-daemon-lock = %{version}-%{release}
Requires: libvirt-daemon-plugin-lockd = %{version}-%{release}
Requires: libvirt-daemon-proxy = %{version}-%{release}
Recommends: libvirt-daemon = %{version}-%{release}
        %else
Requires: libvirt-daemon = %{version}-%{release}
        %endif
Requires: libvirt-daemon-driver-libxl = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}
Requires: xen

%description daemon-xen
Server side daemon and driver required to manage the virtualization
capabilities of XEN
    %endif

    %if %{with_vbox}
%package daemon-vbox
Summary: Server side daemon & driver required to run VirtualBox guests

        %if %{with_modular_daemons}
Requires: libvirt-daemon-common = %{version}-%{release}
Requires: libvirt-daemon-proxy = %{version}-%{release}
Recommends: libvirt-daemon = %{version}-%{release}
        %else
Requires: libvirt-daemon = %{version}-%{release}
        %endif
Requires: libvirt-daemon-driver-vbox = %{version}-%{release}
Requires: libvirt-daemon-driver-interface = %{version}-%{release}
Requires: libvirt-daemon-driver-network = %{version}-%{release}
Requires: libvirt-daemon-driver-nodedev = %{version}-%{release}
Requires: libvirt-daemon-driver-nwfilter = %{version}-%{release}
Requires: libvirt-daemon-driver-secret = %{version}-%{release}
Requires: libvirt-daemon-driver-storage = %{version}-%{release}

%description daemon-vbox
Server side daemon and driver required to manage the virtualization
capabilities of VirtualBox
    %endif

%package client
Summary: Client side utilities of the libvirt library
Requires: libvirt-libs = %{version}-%{release}
# Needed by virt-pki-validate script.
Requires: gnutls-utils

# Ensure smooth upgrades
Obsoletes: libvirt-bash-completion < 7.3.0

%description client
The client binaries needed to access the virtualization
capabilities of recent versions of Linux (and other OSes).

%package client-qemu
Summary: Additional client side utilities for QEMU
Requires: libvirt-libs = %{version}-%{release}
Requires: python3-libvirt >= 3.7.0
Requires: python3-cryptography
Requires: python3-lxml

%description client-qemu
The additional client binaries are used to interact
with some QEMU specific features of libvirt.

%package libs
Summary: Client side libraries
# So remote clients can access libvirt over SSH tunnel
Requires: cyrus-sasl
# Needed by default sasl.conf - no onerous extra deps, since
# 100's of other things on a system already pull in krb5-libs
Requires: cyrus-sasl-gssapi

%description libs
Shared libraries for accessing the libvirt daemon.

    %if %{with_wireshark}
%package wireshark
Summary: Wireshark dissector plugin for libvirt RPC transactions
Requires: wireshark
Requires: libvirt-libs = %{version}-%{release}

%description wireshark
Wireshark dissector plugin for better analysis of libvirt RPC traffic.
    %endif

    %if %{with_lxc}
%package login-shell
Summary: Login shell for connecting users to an LXC container
Requires: libvirt-libs = %{version}-%{release}

%description login-shell
Provides the set-uid virt-login-shell binary that is used to
connect a user to an LXC container when they login, by switching
namespaces.
    %endif

%package devel
Summary: Libraries, includes, etc. to compile with the libvirt library
Requires: libvirt-libs = %{version}-%{release}
Requires: pkgconfig

%description devel
Include header files & development libraries for the libvirt C library.

    %if %{with_sanlock}
%package daemon-plugin-sanlock
Summary: Sanlock lock manager plugin for QEMU driver
Requires: sanlock >= 2.4
#for virt-sanlock-cleanup require augeas
Requires: augeas
Requires: libvirt-libs = %{version}-%{release}
Obsoletes: libvirt-lock-sanlock < 9.1.0
Provides: libvirt-lock-sanlock = %{version}-%{release}

%description daemon-plugin-sanlock
Includes the Sanlock lock manager plugin for the QEMU
driver
    %endif

%package nss
Summary: Libvirt plugin for Name Service Switch
Requires: libvirt-daemon-driver-network = %{version}-%{release}

%description nss
Libvirt plugin for NSS for translating domain names into IP addresses.
%endif

%prep
%autosetup -S git_am

%build

%if %{with_qemu}
    %define arg_qemu -Ddriver_qemu=enabled
%else
    %define arg_qemu -Ddriver_qemu=disabled
%endif

%if %{with_openvz}
    %define arg_openvz -Ddriver_openvz=enabled
%else
    %define arg_openvz -Ddriver_openvz=disabled
%endif

%if %{with_lxc}
    %define arg_lxc -Ddriver_lxc=enabled
    %define arg_login_shell -Dlogin_shell=enabled
%else
    %define arg_lxc -Ddriver_lxc=disabled
    %define arg_login_shell -Dlogin_shell=disabled
%endif

%if %{with_vbox}
    %define arg_vbox -Ddriver_vbox=enabled
%else
    %define arg_vbox -Ddriver_vbox=disabled
%endif

%if %{with_libxl}
    %define arg_libxl -Ddriver_libxl=enabled
%else
    %define arg_libxl -Ddriver_libxl=disabled
%endif

%if %{with_esx}
    %define arg_esx -Ddriver_esx=enabled -Dcurl=enabled
%else
    %define arg_esx -Ddriver_esx=disabled -Dcurl=disabled
%endif

%if %{with_hyperv}
    %define arg_hyperv -Ddriver_hyperv=enabled -Dopenwsman=enabled
%else
    %define arg_hyperv -Ddriver_hyperv=disabled -Dopenwsman=disabled
%endif

%if %{with_vmware}
    %define arg_vmware -Ddriver_vmware=enabled
%else
    %define arg_vmware -Ddriver_vmware=disabled
%endif

%if %{with_storage_rbd}
    %define arg_storage_rbd -Dstorage_rbd=enabled
%else
    %define arg_storage_rbd -Dstorage_rbd=disabled
%endif

%if %{with_storage_gluster}
    %define arg_storage_gluster -Dstorage_gluster=enabled -Dglusterfs=enabled
%else
    %define arg_storage_gluster -Dstorage_gluster=disabled -Dglusterfs=disabled
%endif

%if %{with_storage_zfs}
    %define arg_storage_zfs -Dstorage_zfs=enabled
%else
    %define arg_storage_zfs -Dstorage_zfs=disabled
%endif

%if %{with_numactl}
    %define arg_numactl -Dnumactl=enabled
%else
    %define arg_numactl -Dnumactl=disabled
%endif

%if %{with_numad}
    %define arg_numad -Dnumad=enabled
%else
    %define arg_numad -Dnumad=disabled
%endif

%if %{with_nbdkit}
    %define arg_nbdkit -Dnbdkit=enabled
%else
    %define arg_nbdkit -Dnbdkit=disabled
%endif

%if %{with_nbdkit_config_default}
    %define arg_nbdkit_config_default -Dnbdkit_config_default=enabled
%else
    %define arg_nbdkit_config_default -Dnbdkit_config_default=disabled
%endif

%if %{with_fuse}
    %define arg_fuse -Dfuse=enabled
%else
    %define arg_fuse -Dfuse=disabled
%endif

%if %{with_sanlock}
    %define arg_sanlock -Dsanlock=enabled
%else
    %define arg_sanlock -Dsanlock=disabled
%endif

%if %{with_firewalld_zone}
    %define arg_firewalld_zone -Dfirewalld_zone=enabled
%else
    %define arg_firewalld_zone -Dfirewalld_zone=disabled
%endif

%if %{with_netcf}
    %define arg_netcf -Dnetcf=enabled
%else
    %define arg_netcf -Dnetcf=disabled
%endif

%if %{with_wireshark}
    %define arg_wireshark -Dwireshark_dissector=enabled
%else
    %define arg_wireshark -Dwireshark_dissector=disabled
%endif

%if %{with_storage_iscsi_direct}
    %define arg_storage_iscsi_direct -Dstorage_iscsi_direct=enabled -Dlibiscsi=enabled
%else
    %define arg_storage_iscsi_direct -Dstorage_iscsi_direct=disabled -Dlibiscsi=disabled
%endif

%if %{with_libssh}
    %define arg_libssh -Dlibssh=enabled
%else
    %define arg_libssh -Dlibssh=disabled
%endif

%if %{with_libssh2}
    %define arg_libssh2 -Dlibssh2=enabled
%else
    %define arg_libssh2 -Dlibssh2=disabled
%endif

%if %{with_modular_daemons}
    %define arg_remote_mode -Dremote_default_mode=direct
%else
    %define arg_remote_mode -Dremote_default_mode=legacy
%endif

%define when  %(date +"%%F-%%T")
%define where %(hostname)
%define who   %{?packager}%{!?packager:Unknown}
%define arg_packager -Dpackager="%{who}, %{when}, %{where}"
%define arg_packager_version -Dpackager_version="%{release}"
%define arg_selinux_mount -Dselinux_mount="/sys/fs/selinux"

# place macros above and build commands below this comment

export SOURCE_DATE_EPOCH=$(stat --printf='%Y' %{_specdir}/libvirt.spec)

%if %{with_native}
%meson \
           -Drunstatedir=%{_rundir} \
           -Dinitconfdir=%{_sysconfdir}/sysconfig \
           %{?arg_qemu} \
           %{?arg_openvz} \
           %{?arg_lxc} \
           %{?arg_vbox} \
           %{?arg_libxl} \
           -Dsasl=enabled \
           -Dpolkit=enabled \
           -Ddriver_libvirtd=enabled \
           -Ddriver_remote=enabled \
           -Ddriver_test=enabled \
           %{?arg_esx} \
           %{?arg_hyperv} \
           %{?arg_vmware} \
           -Ddriver_vz=disabled \
           -Ddriver_bhyve=disabled \
           -Ddriver_ch=disabled \
           %{?arg_remote_mode} \
           -Ddriver_interface=enabled \
           -Ddriver_network=enabled \
           -Dstorage_fs=enabled \
           -Dstorage_lvm=enabled \
           -Dstorage_iscsi=enabled \
           %{?arg_storage_iscsi_direct} \
           -Dstorage_scsi=enabled \
           -Dstorage_disk=enabled \
           -Dstorage_mpath=enabled \
           %{?arg_storage_rbd} \
           %{?arg_storage_gluster} \
           %{?arg_storage_zfs} \
           -Dstorage_vstorage=disabled \
           %{?arg_numactl} \
           %{?arg_numad} \
           -Dcapng=enabled \
           %{?arg_fuse} \
           %{?arg_netcf} \
           -Dnls=enabled \
           -Dselinux=enabled \
           %{?arg_selinux_mount} \
           -Dapparmor=disabled \
           -Dapparmor_profiles=disabled \
           -Dsecdriver_apparmor=disabled \
           -Dudev=enabled \
           -Dyajl=enabled \
           %{?arg_sanlock} \
           -Dlibpcap=enabled \
           %{?arg_nbdkit} \
           %{?arg_nbdkit_config_default} \
           -Dlibnl=enabled \
           -Daudit=enabled \
           -Ddtrace=enabled \
           -Dfirewalld=enabled \
           %{?arg_firewalld_zone} \
           %{?arg_wireshark} \
           %{?arg_libssh} \
           %{?arg_libssh2} \
           -Dpm_utils=disabled \
           -Dnss=enabled \
           %{arg_packager} \
           %{arg_packager_version} \
           -Dqemu_user=%{qemu_user} \
           -Dqemu_group=%{qemu_group} \
           -Dqemu_moddir=%{qemu_moddir} \
           -Dqemu_datadir=%{qemu_datadir} \
           -Dtls_priority=%{tls_priority} \
           %{?enable_werror} \
           -Dexpensive_tests=enabled \
           -Dinit_script=systemd \
           -Ddocs=enabled \
           -Dtests=enabled \
           -Drpath=disabled \
           %{?arg_login_shell}

%meson_build
%endif

%install
rm -fr %{buildroot}

export SOURCE_DATE_EPOCH=$(stat --printf='%Y' %{_specdir}/libvirt.spec)

%if %{with_native}
%meson_install

# We don't want to install /etc/libvirt/qemu/networks in the main %%files list
# because if the admin wants to delete the default network completely, we don't
# want to end up re-incarnating it on every RPM upgrade.
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/
cp $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml \
   $RPM_BUILD_ROOT%{_datadir}/libvirt/networks/default.xml
# libvirt saves this file with mode 0600
chmod 0600 $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu/networks/default.xml

# nwfilter files are installed in /usr/share/libvirt and copied to /etc in %%post
# to avoid verification errors on changed files in /etc
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/libvirt/nwfilter/
cp -a $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/nwfilter/*.xml \
    $RPM_BUILD_ROOT%{_datadir}/libvirt/nwfilter/
# libvirt saves these files with mode 600
chmod 600 $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/nwfilter/*.xml

    %if ! %{with_qemu}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_qemu.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
rm -f $RPM_BUILD_ROOT%{_sysusersdir}/libvirt-qemu.conf
    %endif
%find_lang %{name}

    %if ! %{with_sanlock}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirt_sanlock.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
    %endif

    %if ! %{with_lxc}
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_lxc.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
    %endif

    %if ! %{with_qemu}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/qemu.conf
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.qemu
    %endif
    %if ! %{with_lxc}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/lxc.conf
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.lxc
    %endif
    %if ! %{with_libxl}
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/libvirt/libxl.conf
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/libvirtd.libxl
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/libvirtd_libxl.aug
rm -f $RPM_BUILD_ROOT%{_datadir}/augeas/lenses/tests/test_libvirtd_libxl.aug
    %endif

# Copied into libvirt-docs subpackage eventually
mv $RPM_BUILD_ROOT%{_datadir}/doc/libvirt libvirt-docs

    %ifarch %{arches_systemtap_64bit}
mv $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_probes.stp \
   $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_probes-64.stp

        %if %{with_qemu}
mv $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp \
   $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/libvirt_qemu_probes-64.stp
        %endif
    %endif
%endif

%check
pip3 install iniconfig
%if %{with_native}
# Building on slow archs, like emulated s390x in Fedora copr, requires
# raising the test timeout
VIR_TEST_DEBUG=1 %meson_test --no-suite syntax-check --timeout-multiplier 10
%endif

%define libvirt_rpmstatedir %{_localstatedir}/lib/rpm-state/libvirt

# Mark units such that presets will later be applied to them. Meant
# to be called during %pre. Units that already exist on the system
# will not be marked, with the assumption that presets have already
# been applied at some point in the past. This makes it safe to call
# this macro for all units each time %pre runs.
%define libvirt_systemd_schedule_preset() \
    mkdir -p %{libvirt_rpmstatedir} || : \
    for unit in %{?*}; do \
        if ! test -e %{_unitdir}/$unit; then \
            touch %{libvirt_rpmstatedir}/preset-$unit || : \
        fi \
    done \
    %{nil}

# Apply presets for units that have previously been marked. Meant to
# be called during %posttrans. Note that foo.service must be passed
# as the first argument, before all the various foo*.socket
# associated with it, for things to work correctly. This is necessary
# because Also=foo.socket is usually present in foo.service's
# [Install] section, and we want that configuration to take
# precedence over foo.socket's own presets.
%define libvirt_systemd_perform_preset() \
    %{?7:%{error:Too many arguments}} \
    for unit in %{?2} %{?3} %{?4} %{?5} %{?6} %1; do \
        if test -e %{libvirt_rpmstatedir}/preset-$unit; then \
            /usr/bin/systemctl --no-reload preset $unit || : \
        fi \
        rm -f %{libvirt_rpmstatedir}/preset-$unit \
    done \
    rmdir %{libvirt_rpmstatedir} 2>/dev/null || : \
    %{nil}

# Mark a single unit for restart. Meant to be called during %pre.
%define libvirt_systemd_schedule_restart() \
    mkdir -p %{libvirt_rpmstatedir} || : \
    touch %{libvirt_rpmstatedir}/restart-%1 || : \
    %{nil}

# Restart a unit that was previously marked. Meant to be called
# during %posttrans. If systemd is not running, no action will be
# performed.
%define libvirt_systemd_perform_restart() \
    if test -d /run/systemd/system && \
       test -e %{libvirt_rpmstatedir}/restart-%1; then \
        /usr/bin/systemctl try-restart %1 >/dev/null 2>&1 || : \
    fi \
    rm -f %{libvirt_rpmstatedir}/restart-%1 \
    rmdir %{libvirt_rpmstatedir} 2>/dev/null || : \
    %{nil}

# Mark a single unit for reload. Meant to be called during %pre.
%define libvirt_systemd_schedule_reload() \
    mkdir -p %{libvirt_rpmstatedir} || : \
    touch %{libvirt_rpmstatedir}/reload-%1 || : \
    %{nil}

# Reload a unit that was previously marked. Meant to be called during
# %posttrans. If systemd is not running, no action will be performed.
%define libvirt_systemd_perform_reload() \
    if test -d /run/systemd/system && \
       test -e %{libvirt_rpmstatedir}/reload-%1; then \
        /usr/bin/systemctl try-reload-or-restart %1 >/dev/null 2>&1 || : \
    fi \
    rm -f %{libvirt_rpmstatedir}/reload-%1 \
    rmdir %{libvirt_rpmstatedir} 2>/dev/null || : \
    %{nil}

# Disable a single unit, optionally stopping it if systemd is
# running. Meant to be called during %preun.
%define libvirt_systemd_disable() \
    if test -d /run/systemd/system; then \
        /usr/bin/systemctl --no-reload disable --now %{?*} || : \
    else \
        /usr/bin/systemctl --no-reload disable %{?*} || : \
    fi \
    %{nil}

# %pre implementation for services that should be restarted on
# upgrade. Note that foo.service must be passed as the first
# argument, before all the various foo*.socket associated with it.
%define libvirt_systemd_restart_pre() \
    %libvirt_systemd_schedule_preset %{?*} \
    %libvirt_systemd_schedule_restart %1 \
    %{nil}

# %pre implementation for services that should be reloaded on
# upgrade. Note that foo.service must be passed as the first
# argument, before all the various foo*.socket associated with it.
%define libvirt_systemd_reload_pre() \
    %libvirt_systemd_schedule_preset %{?*} \
    %libvirt_systemd_schedule_reload %1 \
    %{nil}

# %pre implementation for services that should be neither restarted
# nor reloaded on upgrade.
%define libvirt_systemd_noaction_pre() \
    %libvirt_systemd_schedule_preset %{?*} \
    %{nil}

# %posttrans implementation for all services. We can use a single
# macro to cover all scenarios, because each operation will only be
# performed if it had previously been scheduled. Note that
# foo.service must be passed as the first argument, before all the
# various foo*.socket associated with it.
%define libvirt_systemd_posttrans() \
    %libvirt_systemd_perform_preset %{?*} \
    %libvirt_systemd_perform_reload %1 \
    %libvirt_systemd_perform_restart %1 \
    %{nil}

# %preun implementation for all services.
%define libvirt_systemd_preun() \
    if [ $1 -lt 1 ]; then \
        %libvirt_systemd_disable %{?*} \
    fi \
    %{nil}

# For daemons with only UNIX sockets

%define libvirt_systemd_unix_pre() %libvirt_systemd_restart_pre %1.service %1.socket %1-ro.socket %1-admin.socket
%define libvirt_systemd_unix_posttrans() %libvirt_systemd_posttrans %1.service %1.socket %1-ro.socket %1-admin.socket
%define libvirt_systemd_unix_preun() %libvirt_systemd_preun %1.service %1.socket %1-ro.socket %1-admin.socket

# For daemons with UNIX and INET sockets
%define libvirt_systemd_inet_pre() %libvirt_systemd_restart_pre %1.service %1.socket %1-ro.socket %1-admin.socket %1-tls.socket %1-tcp.socket
%define libvirt_systemd_inet_posttrans() %libvirt_systemd_posttrans %1.service %1.socket %1-ro.socket %1-admin.socket %1-tls.socket %1-tcp.socket
%define libvirt_systemd_inet_preun() %libvirt_systemd_preun %1.service %1.socket %1-ro.socket %1-admin.socket %1-tls.socket %1-tcp.socket

# For daemons with only UNIX sockets and no unprivileged read-only access
%define libvirt_systemd_privileged_pre() %libvirt_systemd_reload_pre %1.service %1.socket %1-admin.socket
%define libvirt_systemd_privileged_posttrans() %libvirt_systemd_posttrans %1.service %1.socket %1-admin.socket
%define libvirt_systemd_privileged_preun() %libvirt_systemd_preun %1.service %1.socket %1-admin.socket

# For one-shot daemons that have no associated sockets and should never be restarted
%define libvirt_systemd_oneshot_pre() %libvirt_systemd_noaction_pre %1.service
%define libvirt_systemd_oneshot_posttrans() %libvirt_systemd_posttrans %1.service
%define libvirt_systemd_oneshot_preun() %libvirt_systemd_preun %1.service

# For packages that install configuration for other daemons
%define libvirt_systemd_config_pre() %libvirt_systemd_schedule_restart %1.service
%define libvirt_systemd_config_posttrans() %libvirt_systemd_perform_restart %1.service

%if %{with_native}
%pre daemon
%libvirt_sysconfig_pre libvirtd
%libvirt_systemd_inet_pre libvirtd

%posttrans daemon
%libvirt_sysconfig_posttrans libvirtd
%libvirt_systemd_inet_posttrans libvirtd

%preun daemon
%libvirt_systemd_inet_preun libvirtd

%pre daemon-common
%libvirt_sysconfig_pre libvirt-guests
%libvirt_systemd_oneshot_pre libvirt-guests
# 'libvirt' group is just to allow password-less polkit access to libvirt
# daemons. The uid number is irrelevant, so we use dynamic allocation.
getent group libvirt >/dev/null || groupadd -r libvirt
exit 0

%posttrans daemon-common
%libvirt_sysconfig_posttrans libvirt-guests
%libvirt_systemd_oneshot_posttrans libvirt-guests

%preun daemon-common
%libvirt_systemd_oneshot_preun libvirt-guests

%pre daemon-lock
%libvirt_sysconfig_pre virtlockd
%libvirt_systemd_privileged_pre virtlockd

%posttrans daemon-lock
%libvirt_sysconfig_posttrans virtlockd
%libvirt_systemd_privileged_posttrans virtlockd

%preun daemon-lock
%libvirt_systemd_privileged_preun virtlockd

%pre daemon-log
%libvirt_sysconfig_pre virtlogd
%libvirt_systemd_privileged_pre virtlogd

%posttrans daemon-log
%libvirt_sysconfig_posttrans virtlogd
%libvirt_systemd_privileged_posttrans virtlogd

%preun daemon-log
%libvirt_systemd_privileged_preun virtlogd

%pre daemon-proxy
%libvirt_sysconfig_pre virtproxyd
%libvirt_systemd_inet_pre virtproxyd

%posttrans daemon-proxy
%libvirt_sysconfig_posttrans virtproxyd
%libvirt_systemd_inet_posttrans virtproxyd

%preun daemon-proxy
%libvirt_systemd_inet_preun virtproxyd

%pre daemon-driver-network
%libvirt_sysconfig_pre virtnetworkd
%libvirt_systemd_unix_pre virtnetworkd

%post daemon-driver-network
    %if %{with_firewalld_zone}
    %firewalld_reload
    %endif

%posttrans daemon-driver-network
%libvirt_sysconfig_posttrans virtnetworkd
%libvirt_systemd_unix_posttrans virtnetworkd

%preun daemon-driver-network
%libvirt_systemd_unix_preun virtnetworkd

%postun daemon-driver-network
    %if %{with_firewalld_zone}
    %firewalld_reload
    %endif

%pre daemon-driver-nwfilter
%libvirt_sysconfig_pre virtnwfilterd
%libvirt_systemd_unix_pre virtnwfilterd

%posttrans daemon-driver-nwfilter
%libvirt_sysconfig_posttrans virtnwfilterd
%libvirt_systemd_unix_posttrans virtnwfilterd

%preun daemon-driver-nwfilter
%libvirt_systemd_unix_preun virtnwfilterd

%pre daemon-driver-nodedev
%libvirt_sysconfig_pre virtnodedevd
%libvirt_systemd_unix_pre virtnodedevd

%posttrans daemon-driver-nodedev
%libvirt_sysconfig_posttrans virtnodedevd
%libvirt_systemd_unix_posttrans virtnodedevd

%preun daemon-driver-nodedev
%libvirt_systemd_unix_preun virtnodedevd

%pre daemon-driver-interface
%libvirt_sysconfig_pre virtinterfaced
%libvirt_systemd_unix_pre virtinterfaced

%posttrans daemon-driver-interface
%libvirt_sysconfig_posttrans virtinterfaced
%libvirt_systemd_unix_posttrans virtinterfaced

%preun daemon-driver-interface
%libvirt_systemd_unix_preun virtinterfaced

%pre daemon-driver-secret
%libvirt_sysconfig_pre virtsecretd
%libvirt_systemd_unix_pre virtsecretd

%posttrans daemon-driver-secret
%libvirt_sysconfig_posttrans virtsecretd
%libvirt_systemd_unix_posttrans virtsecretd

%preun daemon-driver-secret
%libvirt_systemd_unix_preun virtsecretd

%pre daemon-driver-storage-core
%libvirt_sysconfig_pre virtstoraged
%libvirt_systemd_unix_pre virtstoraged

%posttrans daemon-driver-storage-core
%libvirt_sysconfig_posttrans virtstoraged
%libvirt_systemd_unix_posttrans virtstoraged

%preun daemon-driver-storage-core
%libvirt_systemd_unix_preun virtstoraged

    %if %{with_qemu}
%pre daemon-driver-qemu
%libvirt_sysconfig_pre virtqemud
%libvirt_systemd_unix_pre virtqemud
# We want soft static allocation of well-known ids, as disk images
# are commonly shared across NFS mounts by id rather than name; see
# https://fedoraproject.org/wiki/Packaging:UsersAndGroups
getent group kvm >/dev/null || groupadd -f -g 36 -r kvm
getent group qemu >/dev/null || groupadd -f -g 107 -r qemu
if ! getent passwd qemu >/dev/null; then
  if ! getent passwd 107 >/dev/null; then
    useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin -c "qemu user" qemu
  else
    useradd -r -g qemu -G kvm -d / -s /sbin/nologin -c "qemu user" qemu
  fi
fi
exit 0

%posttrans daemon-driver-qemu
%libvirt_sysconfig_posttrans virtqemud
%libvirt_systemd_unix_posttrans virtqemud

%preun daemon-driver-qemu
%libvirt_systemd_unix_preun virtqemud
    %endif

    %if %{with_lxc}
%pre daemon-driver-lxc
%libvirt_sysconfig_pre virtlxcd
%libvirt_systemd_unix_pre virtlxcd

%posttrans daemon-driver-lxc
%libvirt_sysconfig_posttrans virtlxcd
%libvirt_systemd_unix_posttrans virtlxcd

%preun daemon-driver-lxc
%libvirt_systemd_unix_preun virtlxcd
    %endif

    %if %{with_vbox}
%pre daemon-driver-vbox
%libvirt_sysconfig_pre virtvboxd
%libvirt_systemd_unix_pre virtvboxd

%posttrans daemon-driver-vbox
%libvirt_sysconfig_posttrans virtvboxd
%libvirt_systemd_unix_posttrans virtvboxd

%preun daemon-driver-vbox
%libvirt_systemd_unix_preun virtvboxd
    %endif

    %if %{with_libxl}
%pre daemon-driver-libxl
%libvirt_sysconfig_pre virtxend
%libvirt_systemd_unix_pre virtxend

%posttrans daemon-driver-libxl
%libvirt_sysconfig_posttrans virtxend
%libvirt_systemd_unix_posttrans virtxend

%preun daemon-driver-libxl
%libvirt_systemd_unix_preun virtxend
    %endif

%pre daemon-config-network
%libvirt_systemd_config_pre libvirtd
%libvirt_systemd_config_pre virtnetworkd

%post daemon-config-network
if test $1 -eq 1 && test ! -f %{_sysconfdir}/libvirt/qemu/networks/default.xml ; then
    # see if the network used by default network creates a conflict,
    # and try to resolve it
    # NB: 192.168.122.0/24 is used in the default.xml template file;
    # do not modify any of those values here without also modifying
    # them in the template.
    orig_sub=122
    sub=${orig_sub}
    nl='
'
    routes="${nl}$(ip route show | cut -d' ' -f1)${nl}"
    case ${routes} in
      *"${nl}192.168.${orig_sub}.0/24${nl}"*)
        # there was a match, so we need to look for an unused subnet
        for new_sub in $(seq 124 254); do
          case ${routes} in
          *"${nl}192.168.${new_sub}.0/24${nl}"*)
            ;;
          *)
            sub=$new_sub
            break;
            ;;
          esac
        done
        ;;
      *)
        ;;
    esac

    sed -e "s/${orig_sub}/${sub}/g" \
         < %{_datadir}/libvirt/networks/default.xml \
         > %{_sysconfdir}/libvirt/qemu/networks/default.xml
    ln -s ../default.xml %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
    # libvirt saves this file with mode 0600
    chmod 0600 %{_sysconfdir}/libvirt/qemu/networks/default.xml
fi

%posttrans daemon-config-network
%libvirt_systemd_config_posttrans libvirtd
%libvirt_systemd_config_posttrans virtnetworkd

%pre daemon-config-nwfilter
%libvirt_systemd_config_pre libvirtd
%libvirt_systemd_config_pre virtnwfilterd

%post daemon-config-nwfilter
for datadir_file in %{_datadir}/libvirt/nwfilter/*.xml; do
  sysconfdir_file=%{_sysconfdir}/libvirt/nwfilter/$(basename "$datadir_file")
  if [ ! -f "$sysconfdir_file" ]; then
    # libvirt saves these files with mode 600
    install -m 0600 "$datadir_file" "$sysconfdir_file"
  fi
done

%posttrans daemon-config-nwfilter
%libvirt_systemd_config_posttrans libvirtd
%libvirt_systemd_config_posttrans virtnwfilterd

    %if %{with_lxc}
%pre login-shell
getent group virtlogin >/dev/null || groupadd -r virtlogin
exit 0
    %endif
%endif

%if %{with_native}
%files

%files docs
%doc AUTHORS.rst NEWS.rst README.rst
%doc libvirt-docs/*

%files daemon
%{_unitdir}/libvirtd.service
%{_unitdir}/libvirtd.socket
%{_unitdir}/libvirtd-ro.socket
%{_unitdir}/libvirtd-admin.socket
%{_unitdir}/libvirtd-tcp.socket
%{_unitdir}/libvirtd-tls.socket
%config(noreplace) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %{_prefix}/lib/sysctl.d/60-libvirtd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd
%{_datadir}/augeas/lenses/libvirtd.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd.aug
%attr(0755, root, root) %{_sbindir}/libvirtd
%{_mandir}/man8/libvirtd.8*

%files daemon-common
%{_unitdir}/virt-guest-shutdown.target
%{_unitdir}/libvirt-guests.service
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%dir %{_datadir}/libvirt/
%ghost %dir %{_rundir}/libvirt/
%ghost %dir %{_rundir}/libvirt/common/
%dir %attr(0755, root, root) %{_localstatedir}/lib/libvirt/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/images/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/filesystems/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/boot/
%dir %attr(0711, root, root) %{_localstatedir}/cache/libvirt/
%dir %attr(0755, root, root) %{_libdir}/libvirt/
%dir %attr(0755, root, root) %{_libdir}/libvirt/connection-driver/
%dir %attr(0755, root, root) %{_libdir}/libvirt/storage-backend/
%dir %attr(0755, root, root) %{_libdir}/libvirt/storage-file/
%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%{_datadir}/polkit-1/actions/org.libvirt.api.policy
%{_datadir}/polkit-1/rules.d/50-libvirt.rules
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/
%attr(0755, root, root) %{_libexecdir}/libvirt_iohelper
%attr(0755, root, root) %{_bindir}/virt-ssh-helper
%attr(0755, root, root) %{_libexecdir}/libvirt-guests.sh
%{_mandir}/man1/virt-admin.1*
%{_mandir}/man1/virt-host-validate.1*
%{_mandir}/man8/virt-ssh-helper.8*
%{_mandir}/man8/libvirt-guests.8*
%{_bindir}/virt-host-validate
%{_bindir}/virt-admin
%{_datadir}/bash-completion/completions/virt-admin

%files daemon-lock
%{_unitdir}/virtlockd.service
%{_unitdir}/virtlockd.socket
%{_unitdir}/virtlockd-admin.socket
%config(noreplace) %{_sysconfdir}/libvirt/virtlockd.conf
%{_datadir}/augeas/lenses/virtlockd.aug
%{_datadir}/augeas/lenses/tests/test_virtlockd.aug
%{_datadir}/augeas/lenses/libvirt_lockd.aug
    %if %{with_qemu}
%{_datadir}/augeas/lenses/tests/test_libvirt_lockd.aug
    %endif
%attr(0755, root, root) %{_sbindir}/virtlockd
%{_mandir}/man8/virtlockd.8*

%files daemon-plugin-lockd
%dir %attr(0755, root, root) %{_libdir}/libvirt/lock-driver/
%attr(0755, root, root) %{_libdir}/libvirt/lock-driver/lockd.so

%files daemon-log
%{_unitdir}/virtlogd.service
%{_unitdir}/virtlogd.socket
%{_unitdir}/virtlogd-admin.socket
%config(noreplace) %{_sysconfdir}/libvirt/virtlogd.conf
%{_datadir}/augeas/lenses/virtlogd.aug
%{_datadir}/augeas/lenses/tests/test_virtlogd.aug
%attr(0755, root, root) %{_sbindir}/virtlogd
%{_mandir}/man8/virtlogd.8*

%files daemon-proxy
%{_unitdir}/virtproxyd.service
%{_unitdir}/virtproxyd.socket
%{_unitdir}/virtproxyd-ro.socket
%{_unitdir}/virtproxyd-admin.socket
%{_unitdir}/virtproxyd-tcp.socket
%{_unitdir}/virtproxyd-tls.socket
%config(noreplace) %{_sysconfdir}/libvirt/virtproxyd.conf
%{_datadir}/augeas/lenses/virtproxyd.aug
%{_datadir}/augeas/lenses/tests/test_virtproxyd.aug
%attr(0755, root, root) %{_sbindir}/virtproxyd
%{_mandir}/man8/virtproxyd.8*

%files daemon-config-network
%dir %{_datadir}/libvirt/networks/
%{_datadir}/libvirt/networks/default.xml
%ghost %{_sysconfdir}/libvirt/qemu/networks/default.xml
%ghost %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml

%files daemon-config-nwfilter
%dir %{_datadir}/libvirt/nwfilter/
%{_datadir}/libvirt/nwfilter/*.xml
%ghost %{_sysconfdir}/libvirt/nwfilter/*.xml

%files daemon-driver-interface
%config(noreplace) %{_sysconfdir}/libvirt/virtinterfaced.conf
%{_datadir}/augeas/lenses/virtinterfaced.aug
%{_datadir}/augeas/lenses/tests/test_virtinterfaced.aug
%{_unitdir}/virtinterfaced.service
%{_unitdir}/virtinterfaced.socket
%{_unitdir}/virtinterfaced-ro.socket
%{_unitdir}/virtinterfaced-admin.socket
%attr(0755, root, root) %{_sbindir}/virtinterfaced
%ghost %dir %{_rundir}/libvirt/interface/
%{_libdir}/libvirt/connection-driver/libvirt_driver_interface.so
%{_mandir}/man8/virtinterfaced.8*

%files daemon-driver-network
%config(noreplace) %{_sysconfdir}/libvirt/virtnetworkd.conf
%{_datadir}/augeas/lenses/virtnetworkd.aug
%{_datadir}/augeas/lenses/tests/test_virtnetworkd.aug
%{_unitdir}/virtnetworkd.service
%{_unitdir}/virtnetworkd.socket
%{_unitdir}/virtnetworkd-ro.socket
%{_unitdir}/virtnetworkd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtnetworkd
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/networks/autostart
%ghost %dir %{_rundir}/libvirt/network/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/network/
%dir %attr(0755, root, root) %{_localstatedir}/lib/libvirt/dnsmasq/
%attr(0755, root, root) %{_libexecdir}/libvirt_leaseshelper
%{_libdir}/libvirt/connection-driver/libvirt_driver_network.so
%{_mandir}/man8/virtnetworkd.8*
    %if %{with_firewalld_zone}
%{_prefix}/lib/firewalld/zones/libvirt.xml
%{_prefix}/lib/firewalld/zones/libvirt-routed.xml
%{_prefix}/lib/firewalld/policies/libvirt-routed-in.xml
%{_prefix}/lib/firewalld/policies/libvirt-routed-out.xml
%{_prefix}/lib/firewalld/policies/libvirt-to-host.xml
    %endif

%files daemon-driver-nodedev
%config(noreplace) %{_sysconfdir}/libvirt/virtnodedevd.conf
%{_datadir}/augeas/lenses/virtnodedevd.aug
%{_datadir}/augeas/lenses/tests/test_virtnodedevd.aug
%{_unitdir}/virtnodedevd.service
%{_unitdir}/virtnodedevd.socket
%{_unitdir}/virtnodedevd-ro.socket
%{_unitdir}/virtnodedevd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtnodedevd
%ghost %dir %{_rundir}/libvirt/nodedev/
%{_libdir}/libvirt/connection-driver/libvirt_driver_nodedev.so
%{_mandir}/man8/virtnodedevd.8*

%files daemon-driver-nwfilter
%config(noreplace) %{_sysconfdir}/libvirt/virtnwfilterd.conf
%{_datadir}/augeas/lenses/virtnwfilterd.aug
%{_datadir}/augeas/lenses/tests/test_virtnwfilterd.aug
%{_unitdir}/virtnwfilterd.service
%{_unitdir}/virtnwfilterd.socket
%{_unitdir}/virtnwfilterd-ro.socket
%{_unitdir}/virtnwfilterd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtnwfilterd
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/nwfilter/
%ghost %dir %{_rundir}/libvirt/network/
%ghost %dir %{_rundir}/libvirt/nwfilter-binding/
%ghost %dir %{_rundir}/libvirt/nwfilter/
%{_libdir}/libvirt/connection-driver/libvirt_driver_nwfilter.so
%{_mandir}/man8/virtnwfilterd.8*

%files daemon-driver-secret
%config(noreplace) %{_sysconfdir}/libvirt/virtsecretd.conf
%{_datadir}/augeas/lenses/virtsecretd.aug
%{_datadir}/augeas/lenses/tests/test_virtsecretd.aug
%{_unitdir}/virtsecretd.service
%{_unitdir}/virtsecretd.socket
%{_unitdir}/virtsecretd-ro.socket
%{_unitdir}/virtsecretd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtsecretd
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/secrets/
%ghost %dir %{_rundir}/libvirt/secrets/
%{_libdir}/libvirt/connection-driver/libvirt_driver_secret.so
%{_mandir}/man8/virtsecretd.8*

%files daemon-driver-storage

%files daemon-driver-storage-core
%config(noreplace) %{_sysconfdir}/libvirt/virtstoraged.conf
%{_datadir}/augeas/lenses/virtstoraged.aug
%{_datadir}/augeas/lenses/tests/test_virtstoraged.aug
%{_unitdir}/virtstoraged.service
%{_unitdir}/virtstoraged.socket
%{_unitdir}/virtstoraged-ro.socket
%{_unitdir}/virtstoraged-admin.socket
%attr(0755, root, root) %{_sbindir}/virtstoraged
%attr(0755, root, root) %{_libexecdir}/libvirt_parthelper
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/storage/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/storage/autostart/
%ghost %dir %{_rundir}/libvirt/storage/
%{_libdir}/libvirt/connection-driver/libvirt_driver_storage.so
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_fs.so
%{_libdir}/libvirt/storage-file/libvirt_storage_file_fs.so
%{_mandir}/man8/virtstoraged.8*

%files daemon-driver-storage-disk
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_disk.so

%files daemon-driver-storage-logical
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_logical.so

%files daemon-driver-storage-scsi
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_scsi.so

%files daemon-driver-storage-iscsi
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_iscsi.so

    %if %{with_storage_iscsi_direct}
%files daemon-driver-storage-iscsi-direct
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_iscsi-direct.so
    %endif

%files daemon-driver-storage-mpath
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_mpath.so

    %if %{with_storage_gluster}
%files daemon-driver-storage-gluster
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_gluster.so
%{_libdir}/libvirt/storage-file/libvirt_storage_file_gluster.so
    %endif

    %if %{with_storage_rbd}
%files daemon-driver-storage-rbd
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_rbd.so
    %endif

    %if %{with_storage_zfs}
%files daemon-driver-storage-zfs
%{_libdir}/libvirt/storage-backend/libvirt_storage_backend_zfs.so
    %endif

    %if %{with_qemu}
%files daemon-driver-qemu
%config(noreplace) %{_sysconfdir}/libvirt/virtqemud.conf
%config(noreplace) %{_prefix}/lib/sysctl.d/60-qemu-postcopy-migration.conf
%{_datadir}/augeas/lenses/virtqemud.aug
%{_datadir}/augeas/lenses/tests/test_virtqemud.aug
%{_unitdir}/virtqemud.service
%{_unitdir}/virtqemud.socket
%{_unitdir}/virtqemud-ro.socket
%{_unitdir}/virtqemud-admin.socket
%attr(0755, root, root) %{_sbindir}/virtqemud
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/autostart/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %{_sysconfdir}/libvirt/qemu-lockd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.qemu
%ghost %dir %{_rundir}/libvirt/qemu/
%ghost %dir %{_rundir}/libvirt/qemu/dbus/
%ghost %dir %{_rundir}/libvirt/qemu/passt/
%ghost %dir %{_rundir}/libvirt/qemu/slirp/
%ghost %dir %{_rundir}/libvirt/qemu/swtpm/
%dir %attr(0751, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/
%dir %attr(0751, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/checkpoint/
%dir %attr(0751, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/dump/
%dir %attr(0751, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/nvram/
%dir %attr(0751, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/ram/
%dir %attr(0751, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/save/
%dir %attr(0751, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/snapshot/
%dir %attr(0750, root, root) %{_localstatedir}/cache/libvirt/qemu/
%{_datadir}/augeas/lenses/libvirtd_qemu.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%{_libdir}/libvirt/connection-driver/libvirt_driver_qemu.so
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/swtpm/
%dir %attr(0730, tss, tss) %{_localstatedir}/log/swtpm/libvirt/qemu/
%{_bindir}/virt-qemu-run
%{_mandir}/man1/virt-qemu-run.1*
%{_mandir}/man8/virtqemud.8*
%{_sysusersdir}/libvirt-qemu.conf
    %endif

    %if %{with_lxc}
%files daemon-driver-lxc
%config(noreplace) %{_sysconfdir}/libvirt/virtlxcd.conf
%{_datadir}/augeas/lenses/virtlxcd.aug
%{_datadir}/augeas/lenses/tests/test_virtlxcd.aug
%{_unitdir}/virtlxcd.service
%{_unitdir}/virtlxcd.socket
%{_unitdir}/virtlxcd-ro.socket
%{_unitdir}/virtlxcd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtlxcd
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/lxc/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/lxc/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/lxc/autostart/
%config(noreplace) %{_sysconfdir}/libvirt/lxc.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.lxc
%ghost %dir %{_rundir}/libvirt/lxc/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/lxc/
%{_datadir}/augeas/lenses/libvirtd_lxc.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_lxc.aug
%attr(0755, root, root) %{_libexecdir}/libvirt_lxc
%{_libdir}/libvirt/connection-driver/libvirt_driver_lxc.so
%{_mandir}/man8/virtlxcd.8*
    %endif

    %if %{with_libxl}
%files daemon-driver-libxl
%config(noreplace) %{_sysconfdir}/libvirt/virtxend.conf
%{_datadir}/augeas/lenses/virtxend.aug
%{_datadir}/augeas/lenses/tests/test_virtxend.aug
%{_unitdir}/virtxend.service
%{_unitdir}/virtxend.socket
%{_unitdir}/virtxend-ro.socket
%{_unitdir}/virtxend-admin.socket
%attr(0755, root, root) %{_sbindir}/virtxend
%config(noreplace) %{_sysconfdir}/libvirt/libxl.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.libxl
%config(noreplace) %{_sysconfdir}/libvirt/libxl-lockd.conf
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/libxl/
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/libxl/autostart/
%{_datadir}/augeas/lenses/libvirtd_libxl.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_libxl.aug
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/libxl/
%ghost %dir %{_rundir}/libvirt/libxl/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/libxl/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/libxl/channel/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/libxl/channel/target/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/libxl/dump/
%dir %attr(0700, root, root) %{_localstatedir}/lib/libvirt/libxl/save/
%{_libdir}/libvirt/connection-driver/libvirt_driver_libxl.so
%{_mandir}/man8/virtxend.8*
    %endif

    %if %{with_vbox}
%files daemon-driver-vbox
%config(noreplace) %{_sysconfdir}/libvirt/virtvboxd.conf
%{_datadir}/augeas/lenses/virtvboxd.aug
%{_datadir}/augeas/lenses/tests/test_virtvboxd.aug
%{_unitdir}/virtvboxd.service
%{_unitdir}/virtvboxd.socket
%{_unitdir}/virtvboxd-ro.socket
%{_unitdir}/virtvboxd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtvboxd
%{_libdir}/libvirt/connection-driver/libvirt_driver_vbox.so
%{_mandir}/man8/virtvboxd.8*
    %endif

    %if %{with_qemu_tcg}
%files daemon-qemu
    %endif

    %if %{with_qemu_kvm}
%files daemon-kvm
    %endif

    %if %{with_lxc}
%files daemon-lxc
    %endif

    %if %{with_libxl}
%files daemon-xen
    %endif

    %if %{with_vbox}
%files daemon-vbox
    %endif

    %if %{with_sanlock}
%files daemon-plugin-sanlock
        %if %{with_qemu}
%config(noreplace) %{_sysconfdir}/libvirt/qemu-sanlock.conf
        %endif
        %if %{with_libxl}
%config(noreplace) %{_sysconfdir}/libvirt/libxl-sanlock.conf
        %endif
%dir %attr(0755, root, root) %{_libdir}/libvirt/lock-driver/
%attr(0755, root, root) %{_libdir}/libvirt/lock-driver/sanlock.so
%{_datadir}/augeas/lenses/libvirt_sanlock.aug
%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
%dir %attr(0770, root, sanlock) %{_localstatedir}/lib/libvirt/sanlock
%{_sbindir}/virt-sanlock-cleanup
%{_mandir}/man8/virt-sanlock-cleanup.8*
%attr(0755, root, root) %{_libexecdir}/libvirt_sanlock_helper
    %endif

%files client
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-query-dn.1*
%{_mandir}/man1/virt-pki-validate.1*
%{_mandir}/man7/virkey*.7*
%{_bindir}/virsh
%{_bindir}/virt-xml-validate
%{_bindir}/virt-pki-query-dn
%{_bindir}/virt-pki-validate
%{_datadir}/bash-completion/completions/virsh

    %if %{with_qemu}
%files client-qemu
%{_mandir}/man1/virt-qemu-qmp-proxy.1*
%{_mandir}/man1/virt-qemu-sev-validate.1*
%{_bindir}/virt-qemu-qmp-proxy
%{_bindir}/virt-qemu-sev-validate
    %endif

%files libs -f %{name}.lang
%license COPYING COPYING.LESSER
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/
%config(noreplace) %{_sysconfdir}/libvirt/libvirt.conf
%config(noreplace) %{_sysconfdir}/libvirt/libvirt-admin.conf
%{_libdir}/libvirt.so.*
%{_libdir}/libvirt-qemu.so.*
%{_libdir}/libvirt-lxc.so.*
%{_libdir}/libvirt-admin.so.*
%dir %{_datadir}/libvirt/
%dir %{_datadir}/libvirt/schemas/
%{_datadir}/systemtap/tapset/libvirt_probes*.stp
%{_datadir}/systemtap/tapset/libvirt_functions.stp
    %if %{with_qemu}
%{_datadir}/systemtap/tapset/libvirt_qemu_probes*.stp
    %endif
%{_datadir}/libvirt/schemas/*.rng
%{_datadir}/libvirt/cpu_map/*.xml
%{_datadir}/libvirt/test-screenshot.png

    %if %{with_wireshark}
%files wireshark
%{wireshark_plugindir}/libvirt.so
    %endif

%files nss
%{_libdir}/libnss_libvirt.so.2
%{_libdir}/libnss_libvirt_guest.so.2

    %if %{with_lxc}
%files login-shell
%attr(4750, root, virtlogin) %{_bindir}/virt-login-shell
%{_libexecdir}/virt-login-shell-helper
%config(noreplace) %{_sysconfdir}/libvirt/virt-login-shell.conf
%{_mandir}/man1/virt-login-shell.1*
    %endif

%files devel
%{_libdir}/libvirt.so
%{_libdir}/libvirt-admin.so
%{_libdir}/libvirt-qemu.so
%{_libdir}/libvirt-lxc.so
%dir %{_includedir}/libvirt
%{_includedir}/libvirt/virterror.h
%{_includedir}/libvirt/libvirt.h
%{_includedir}/libvirt/libvirt-admin.h
%{_includedir}/libvirt/libvirt-common.h
%{_includedir}/libvirt/libvirt-domain.h
%{_includedir}/libvirt/libvirt-domain-checkpoint.h
%{_includedir}/libvirt/libvirt-domain-snapshot.h
%{_includedir}/libvirt/libvirt-event.h
%{_includedir}/libvirt/libvirt-host.h
%{_includedir}/libvirt/libvirt-interface.h
%{_includedir}/libvirt/libvirt-network.h
%{_includedir}/libvirt/libvirt-nodedev.h
%{_includedir}/libvirt/libvirt-nwfilter.h
%{_includedir}/libvirt/libvirt-secret.h
%{_includedir}/libvirt/libvirt-storage.h
%{_includedir}/libvirt/libvirt-stream.h
%{_includedir}/libvirt/libvirt-qemu.h
%{_includedir}/libvirt/libvirt-lxc.h
%{_libdir}/pkgconfig/libvirt.pc
%{_libdir}/pkgconfig/libvirt-admin.pc
%{_libdir}/pkgconfig/libvirt-qemu.pc
%{_libdir}/pkgconfig/libvirt-lxc.pc
%dir %{_datadir}/libvirt/api/
%{_datadir}/libvirt/api/libvirt-api.xml
%{_datadir}/libvirt/api/libvirt-admin-api.xml
%{_datadir}/libvirt/api/libvirt-qemu-api.xml
%{_datadir}/libvirt/api/libvirt-lxc-api.xml
%endif

%changelog
* Thu May 30 2024 Sharath Srikanth Chellappa <sharathsr@microsoft.com> - 10.0.0-3
- Add patch to libvirt.conf to work with kubevirt.

* Wed Apr 03 2024 Betty Lakes <bettylakes@microsoft.com> - 10.0.0-2
- Make systemd dependency explicit to avoid confusion with systemd-bootstrap.

* Thu Jan 18 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 10.0.0-1
- Updating to version 10.0.0.
- Hard code configuration options to match Mariner 2.0 configurations. Ensure that
  each hard-coded value is commented as matching azl2.0
- Disable ceph-related dependencies

* Wed May 24 2023 Sharath Srikanth Chellappa <sharathsr@microsoft.com> - 7.10.0-5
- Patch CVE-2023-2700

* Thu Sep 08 2022 Andrew Phelps <anphel@microsoft.com> - 7.10.0-4
- Change qemu-img BR from binary to package

* Thu Feb 24 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.10.0-3
- Re-enabling '*-glusterfs' subpackage.
- Bringing back dependency on 'lzop' and 'radvd'.

* Thu Feb 17 2022 Thomas Crain <thcrain@microsoft.com> - 7.10.0-2
- Remove requirement on python2 (python in general is not needed at runtime)

* Tue Jan 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.10.0-1
- Updating to version 7.10.0.
- Switched to building with "meson".
- Removed obsolete 'libvirt-bash-completion' subpackage.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 6.1.0-4
- Use python3-docutils dependency instead of python-docutils
- License verified (specify as LGPLv2+ rather than just LGPL)

*   Mon Jul 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1.0-3
-   Extending with subpackages using Fedora 33 spec (license: MIT).
-   Added subpackages:
    - 'libvirt-admin',
    - 'libvirt-bash-completion',
    - 'libvirt-client',
    - 'libvirt-daemon',
    - 'libvirt-daemon-config-network',
    - 'libvirt-daemon-config-nwfilter',
    - 'libvirt-daemon-driver-interface',
    - 'libvirt-daemon-driver-network',
    - 'libvirt-daemon-driver-nodedev',
    - 'libvirt-daemon-driver-nwfilter',
    - 'libvirt-daemon-driver-qemu',
    - 'libvirt-daemon-driver-secret',
    - 'libvirt-daemon-driver-storage',
    - 'libvirt-daemon-driver-storage-core',
    - 'libvirt-daemon-driver-storage-disk',
    - 'libvirt-daemon-driver-storage-iscsi',
    - 'libvirt-daemon-driver-storage-logical',
    - 'libvirt-daemon-driver-storage-mpath',
    - 'libvirt-daemon-driver-storage-rbd',
    - 'libvirt-daemon-driver-storage-scsi',
    - 'libvirt-daemon-kvm',
    - 'libvirt-libs',
    - 'libvirt-lock-sanlock',
    - 'libvirt-nss'.
- Temporarily disable 'libvirt-daemon-driver-storage-gluster' subpackage build.
- Temporarily disable run-time requires for unused subpackages.

*   Mon Oct 26 2020 Nicolas Ontiveros <niontive@microsoft.com> - 6.1.0-2
-   Use autosetup
-   Patch CVE-2020-25637

*   Fri May 29 2020 Emre Girgin <mrgirgin@microsoft.com> 6.1.0-1
-   Upgrade to 6.1.0.

*   Sat May 09 00:21:42 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.7.0-5
-   Added %%license line automatically

*   Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 4.7.0-4
-   Rename libnl to libnl3.
-   Remove sha1 hash.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.7.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Sep 25 2018 Alexey Makhalov <amakhalov@vmware.com> 4.7.0-2
-   Use libtirpc

*   Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 4.7.0-1
-   Update to version 4.7.0

*   Thu Dec 07 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-4
-   Move so files in folder connection-driver and lock-driver to main package.

*   Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> 3.2.0-3
-   Fix CVE-2017-1000256

*   Wed Aug 23 2017 Rui Gu <ruig@vmware.com> 3.2.0-2
-   Fix missing deps in devel package

*   Thu Apr 06 2017 Kumar Kaushik <kaushikk@vmware.com> 3.2.0-1
-   Upgrading version to 3.2.0

*   Fri Feb 03 2017 Vinay Kulkarni <kulkarniv@vmware.com> 3.0.0-1
-   Initial version of libvirt package for Photon.
