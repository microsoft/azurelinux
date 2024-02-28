# Force QEMU to run as non-root
%define qemu_user  qemu
%define qemu_group  qemu

# Its dependencies cannot run their post-install scripts due to systemd not working in the build container.
%bcond_with missing_dependencies
%bcond_with netcf

Summary:        Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:           libvirt
Version:        7.10.0
Release:        6%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Virtualization/Libraries
URL:            https://libvirt.org/
Source0:        https://libvirt.org/sources/%{name}-%{version}.tar.xz
# CVE-2023-2700 is fixed by https://gitlab.com/libvirt/libvirt/-/commit/6425a311b8ad19d6f9c0b315bf1d722551ea3585
Patch1:         CVE-2023-2700.patch

BuildRequires:  audit-libs-devel
BuildRequires:  augeas
BuildRequires:  bash-completion
BuildRequires:  cyrus-sasl-devel
BuildRequires:  dbus-devel
BuildRequires:  device-mapper-devel
BuildRequires:  dnsmasq >= 2.41
BuildRequires:  e2fsprogs-devel
BuildRequires:  fuse-devel >= 2.8.6
BuildRequires:  glusterfs-api-devel >= 3.4.1
BuildRequires:  glusterfs-devel >= 3.4.1
BuildRequires:  gnutls-devel
BuildRequires:  iscsi-initiator-utils
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libiscsi-devel
BuildRequires:  libnl3-devel
BuildRequires:  libpcap-devel >= 1.5.0
BuildRequires:  libpciaccess-devel
BuildRequires:  librados2-devel
BuildRequires:  librbd1-devel
BuildRequires:  libselinux-devel
BuildRequires:  libssh2-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  lvm2
BuildRequires:  meson >= 0.54.0
%if %{with netcf}
BuildRequires:  netcf-devel >= 0.2.2
%endif
BuildRequires:  ninja-build
BuildRequires:  numactl-devel
BuildRequires:  numad
BuildRequires:  parted
BuildRequires:  polkit
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  qemu-img
BuildRequires:  readline-devel
BuildRequires:  rpcsvc-proto
BuildRequires:  sanlock-devel
BuildRequires:  systemd-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  yajl-devel

Requires:       %{name}-client = %{version}-%{release}
Requires:       %{name}-daemon-config-network = %{version}-%{release}
Requires:       %{name}-daemon-config-nwfilter = %{version}-%{release}
Requires:       %{name}-daemon-driver-interface = %{version}-%{release}
Requires:       %{name}-daemon-driver-network = %{version}-%{release}
Requires:       %{name}-daemon-driver-nodedev = %{version}-%{release}
Requires:       %{name}-daemon-driver-nwfilter = %{version}-%{release}
Requires:       %{name}-daemon-driver-qemu = %{version}-%{release}
Requires:       %{name}-daemon-driver-secret = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage = %{version}-%{release}
Requires:       %{name}-daemon-driver-vbox = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       cyrus-sasl
Requires:       device-mapper
Requires:       e2fsprogs
Requires:       gnutls
Requires:       libcap-ng
Requires:       libnl3
Requires:       libselinux
Requires:       libssh2
Requires:       libtirpc
Requires:       libxml2
Requires:       parted
Requires:       readline
Requires:       systemd

%description
Libvirt is collection of software that provides a convenient way to manage virtual machines and other virtualization functionality, such as storage and network interface management. These software pieces include an API library, a daemon (libvirtd), and a command line utility (virsh).  An primary goal of libvirt is to provide a single way to manage multiple different virtualization providers/hypervisors. For example, the command 'virsh list --all' can be used to list the existing virtual machines for any supported hypervisor (KVM, Xen, VMWare ESX, etc.) No need to learn the hypervisor specific tools!

%package admin
Summary:        Set of tools to control libvirt daemon

Requires:       %{name}-libs = %{version}-%{release}
Requires:       readline

%description admin
The client side utilities to control the libvirt daemon.

%package client
Summary:        Client side utilities of the libvirt library

Requires:       %{name}-libs = %{version}-%{release}
# Needed by libvirt-guests.sh script.
Requires:       gettext
# Needed by virt-pki-validate script.
Requires:       gnutls-utils
Requires:       ncurses
Requires:       readline

%description client
The client binaries needed to access the virtualization
capabilities of recent versions of Linux (and other OSes).

%package daemon
Summary:        Server side daemon and supporting files for libvirt library

# (client invokes 'nc' against the UNIX socket on the server)
Requires:       %{_bindir}/nc
Requires:       %{name}-libs = %{version}-%{release}
# libvirtd depends on 'messagebus' service
Requires:       dbus
# for /sbin/ip & /sbin/tc
Requires:       iproute
# for modprobe of pci devices
Requires:       module-init-tools
Requires:       numad
Requires:       polkit >= 0.112
Requires(post): systemd-sysv
# For service management
Requires(post): systemd-units
Requires(postun): systemd-units
# For uid creation during pre
Requires(pre):  shadow-utils
Requires(preun): systemd-units
%ifarch x86_64
# For virConnectGetSysinfo
Requires:       dmidecode
%endif

%description daemon
Server side daemon required to manage the virtualization capabilities
of recent versions of Linux. Requires a hypervisor specific sub-RPM
for specific drivers.

%package daemon-config-network
Summary:        Default configuration files for the libvirtd daemon

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-daemon-driver-network = %{version}-%{release}

%description daemon-config-network
Default configuration files for setting up NAT based networking

%package daemon-config-nwfilter
Summary:        Network filter configuration files for the libvirtd daemon

Requires:       libvirt-daemon = %{version}-%{release}
Requires:       libvirt-daemon-driver-nwfilter = %{version}-%{release}

%description daemon-config-nwfilter
Network filter configuration files for cleaning guest traffic

%package daemon-driver-interface
Summary:        Interface driver plugin for the libvirtd daemon

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
%if 0%{with netcf}
Requires:       netcf-libs >= 0.2.2
%endif

%description daemon-driver-interface
The interface driver plugin for the libvirtd daemon, providing
an implementation of the host network interface APIs.

%package daemon-driver-network
Summary:        Network driver plugin for the libvirtd daemon

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       dnsmasq >= 2.41
Requires:       iptables
Requires:       radvd

%description daemon-driver-network
The network driver plugin for the libvirtd daemon, providing
an implementation of the virtual network APIs using the Linux
bridge capabilities.

%package daemon-driver-nodedev
Summary:        Nodedev driver plugin for the libvirtd daemon

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       systemd

%description daemon-driver-nodedev
The nodedev driver plugin for the libvirtd daemon, providing
an implementation of the node device APIs using the udev
capabilities.

%package daemon-driver-nwfilter
Summary:        Nwfilter driver plugin for the libvirtd daemon

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       ebtables
Requires:       iptables

%description daemon-driver-nwfilter
The nwfilter driver plugin for the libvirtd daemon, providing
an implementation of the firewall APIs using the ebtables,
iptables and ip6tables capabilities

%package daemon-driver-qemu
Summary:        QEMU driver plugin for the libvirtd daemon

Requires:       qemu-img
Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       bzip2
# For image compression
Requires:       gzip
Requires:       lzop
Requires:       xz

%if 0%{with missing_dependencies}
Requires:       systemd-container
%endif

%description daemon-driver-qemu
The qemu driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
QEMU

%package daemon-driver-secret
Summary:        Secret driver plugin for the libvirtd daemon

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description daemon-driver-secret
The secret driver plugin for the libvirtd daemon, providing
an implementation of the secret key APIs.

%package daemon-driver-storage
Summary:        Storage driver plugin including all backends for the libvirtd daemon

Requires:       %{name}-daemon-driver-storage-core = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage-disk = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage-iscsi = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage-logical = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage-mpath = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage-rbd = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage-scsi = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage-gluster = %{version}-%{release}

%description daemon-driver-storage
The storage driver plugin for the libvirtd daemon, providing
an implementation of the storage APIs using LVM, iSCSI,
parted and more.

%package daemon-driver-storage-core
Summary:        Storage driver plugin including base backends for the libvirtd daemon

Requires:       qemu-img
Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       nfs-utils
# For mkfs
Requires:       util-linux

%description daemon-driver-storage-core
The storage driver plugin for the libvirtd daemon, providing
an implementation of the storage APIs using files, local disks, LVM, SCSI,
iSCSI, and multipath storage.

%package daemon-driver-storage-disk
Summary:        Storage driver plugin for disk

Requires:       %{name}-daemon-driver-storage-core = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       device-mapper
Requires:       parted

%description daemon-driver-storage-disk
The storage driver backend adding implementation of the storage APIs for block
volumes using the host disks.

%package daemon-driver-storage-gluster
Summary:        Storage driver plugin for gluster

Requires:       %{_sbindir}/gluster
Requires:       %{name}-daemon-driver-storage-core = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       glusterfs-client >= 2.0.1

%description daemon-driver-storage-gluster
The storage driver backend adding implementation of the storage APIs for gluster
volumes using libgfapi.

%package daemon-driver-storage-iscsi
Summary:        Storage driver plugin for iscsi

Requires:       %{name}-daemon-driver-storage-core = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
Requires:       iscsi-initiator-utils

%description daemon-driver-storage-iscsi
The storage driver backend adding implementation of the storage APIs for iscsi
volumes using the host iscsi stack.

%package daemon-driver-storage-logical
Summary:        Storage driver plugin for lvm volumes

Requires:       libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires:       libvirt-libs = %{version}-%{release}
Requires:       lvm2

%description daemon-driver-storage-logical
The storage driver backend adding implementation of the storage APIs for block
volumes using lvm.

%package daemon-driver-storage-mpath
Summary:        Storage driver plugin for multipath volumes

Requires:       device-mapper
Requires:       libvirt-daemon-driver-storage-core = %{version}-%{release}
Requires:       libvirt-libs = %{version}-%{release}

%description daemon-driver-storage-mpath
The storage driver backend adding implementation of the storage APIs for
multipath storage using device mapper.

%package daemon-driver-storage-rbd
Summary:        Storage driver plugin for rbd

Requires:       %{name}-daemon-driver-storage-core = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description daemon-driver-storage-rbd
The storage driver backend adding implementation of the storage APIs for rbd
volumes using the ceph protocol.

%package daemon-driver-storage-scsi
Summary:        Storage driver plugin for local scsi devices

Requires:       %{name}-daemon-driver-storage-core = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description daemon-driver-storage-scsi
The storage driver backend adding implementation of the storage APIs for scsi
host devices.

%package daemon-driver-vbox
Summary:        VirtualBox driver plugin for the libvirtd daemon

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}

%description daemon-driver-vbox
The vbox driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
VirtualBox

%package daemon-kvm
Summary:        Server side daemon & driver required to run KVM guests

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-daemon-driver-interface = %{version}-%{release}
Requires:       %{name}-daemon-driver-network = %{version}-%{release}
Requires:       %{name}-daemon-driver-nodedev = %{version}-%{release}
Requires:       %{name}-daemon-driver-nwfilter = %{version}-%{release}
Requires:       %{name}-daemon-driver-qemu = %{version}-%{release}
Requires:       %{name}-daemon-driver-secret = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage = %{version}-%{release}
Requires:       qemu-kvm

%description daemon-kvm
Server side daemon and driver required to manage the virtualization
capabilities of the KVM hypervisor

%package daemon-vbox
Summary:        Server side daemon & driver required to run VirtualBox guests

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-daemon-driver-interface = %{version}-%{release}
Requires:       %{name}-daemon-driver-network = %{version}-%{release}
Requires:       %{name}-daemon-driver-nodedev = %{version}-%{release}
Requires:       %{name}-daemon-driver-nwfilter = %{version}-%{release}
Requires:       %{name}-daemon-driver-secret = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage = %{version}-%{release}
Requires:       %{name}-daemon-driver-vbox = %{version}-%{release}

%description daemon-vbox
Server side daemon and driver required to manage the virtualization
capabilities of VirtualBox

%package devel
Summary:        libvirt devel
Group:          Development/Tools

Requires:       %{name} = %{version}-%{release}
Requires:       libtirpc-devel

%description devel
This contains development tools and libraries for libvirt.

%package docs
Summary:        libvirt docs
Group:          Development/Tools

%description docs
The contains libvirt package doc files.

%package libs
Summary:        Client side libraries

# So remote clients can access libvirt over SSH tunnel
Requires:       cyrus-sasl
# Needed by default sasl.conf - no onerous extra deps, since
# 100's of other things on a system already pull in krb5-libs
Requires:       cyrus-sasl-gssapi

%description libs
Shared libraries for accessing the libvirt daemon.

%package nss
Summary:        Libvirt plugin for Name Service Switch

Requires:       %{name}-daemon-driver-network = %{version}-%{release}

%package lock-sanlock
Summary:        Sanlock lock manager plugin for QEMU driver

Requires:       %{name}-daemon = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}
#for virt-sanlock-cleanup require augeas
Requires:       augeas
Requires:       sanlock

%description lock-sanlock
Includes the Sanlock lock manager plugin for the QEMU
driver

%description nss
Libvirt plugin for NSS for translating domain names into IP addresses.

%prep
%autosetup -p1

%define _vpath_builddir build

%build
%meson \
    -Daudit=enabled \
    -Dbash_completion=enabled \
    -Dbash_completion_dir="%{_datadir}/bash-completion/completions" \
    -Ddriver_libvirtd=enabled \
    -Ddriver_network=enabled \
    -Ddriver_qemu=enabled \
    -Dfuse=enabled \
    -Dglusterfs=enabled \
    -Dlibssh2=enabled \
%if 0%{with netcf}
    -Dnetcf=enabled \
%endif
    -Dnss=enabled \
    -Dnumactl=enabled \
    -Dnumad=enabled \
    -Dpciaccess=enabled \
    -Dpolkit=enabled \
    -Dqemu_group=%{qemu_group} \
    -Dqemu_user=%{qemu_user} \
    -Dsanlock=enabled \
    -Dsasl=enabled \
    -Dselinux=enabled \
    -Dselinux_mount="/sys/fs/selinux" \
    -Dstorage_disk=enabled \
    -Dstorage_gluster=enabled \
    -Dstorage_iscsi=enabled \
    -Dstorage_lvm=enabled \
    -Dstorage_mpath=enabled \
    -Dstorage_rbd=enabled \
    -Dudev=enabled \
    -Dyajl=enabled \
    -Dapparmor=disabled \
    -Dapparmor_profiles=disabled \
    -Dcurl=disabled \
    -Ddriver_bhyve=disabled \
    -Ddriver_ch=disabled \
    -Ddriver_esx=disabled \
    -Ddriver_hyperv=disabled \
    -Ddriver_libxl=disabled \
    -Ddriver_lxc=disabled \
    -Ddriver_vz=disabled \
    -Dfirewalld_zone=disabled \
    -Dlibssh=disabled \
    -Dlogin_shell=disabled \
%if ! 0%{with netcf}
    -Dnetcf=disabled \
%endif
    -Dopenwsman=disabled \
    -Dpm_utils=disabled \
    -Drpath=disabled \
    -Dsecdriver_apparmor=disabled \
    -Dstorage_iscsi_direct=disabled \
    -Dstorage_sheepdog=disabled \
    -Dstorage_vstorage=disabled \
    -Dstorage_zfs=disabled \
    -Dwireshark_dissector=disabled

%meson_build

%install
%meson_install

find %{buildroot} -type f -name "*.la" -delete -print

install -d -m 0755 %{buildroot}%{_datadir}/lib/libvirt/dnsmasq/

# We don't want to install /etc/libvirt/qemu/networks in the main %%files list
# because if the admin wants to delete the default network completely, we don't
# want to end up re-incarnating it on every RPM upgrade.
install -d -m 0755 %{buildroot}%{_datadir}/libvirt/networks/
cp %{buildroot}%{_sysconfdir}/libvirt/qemu/networks/default.xml \
   %{buildroot}%{_datadir}/libvirt/networks/default.xml
# libvirt saves this file with mode 0600
chmod 0600 %{buildroot}%{_sysconfdir}/libvirt/qemu/networks/default.xml

# nwfilter files are installed in /usr/share/libvirt and copied to /etc in %%post
# to avoid verification errors on changed files in /etc
install -d -m 0755 %{buildroot}%{_datadir}/libvirt/nwfilter/
cp -a %{buildroot}%{_sysconfdir}/libvirt/nwfilter/*.xml \
    %{buildroot}%{_datadir}/libvirt/nwfilter/
# libvirt saves these files with mode 600
chmod 600 %{buildroot}%{_sysconfdir}/libvirt/nwfilter/*.xml

# Strip auto-generated UUID - we need it generated per-install
sed -i -e "/<uuid>/d" %{buildroot}%{_datadir}/libvirt/networks/default.xml

# Copied into libvirt-docs subpackage eventually
mv %{buildroot}%{_docdir}/libvirt libvirt-docs

%ifarch x86_64
mv %{buildroot}%{_datadir}/systemtap/tapset/libvirt_probes.stp \
   %{buildroot}%{_datadir}/systemtap/tapset/libvirt_probes-64.stp

mv %{buildroot}%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp \
   %{buildroot}%{_datadir}/systemtap/tapset/libvirt_qemu_probes-64.stp
%endif

# We're building with '--without-libxl'
rm -rf %{buildroot}%{_sysconfdir}/logrotate.d/libvirtd.libxl

# We're building with '--without-lxc'
rm -rf %{buildroot}%{_sysconfdir}/logrotate.d/libvirtd.lxc

%find_lang %{name}

%check
VIR_TEST_DEBUG=1 %meson_test --no-suite syntax-check

%preun client

%systemd_preun libvirt-guests.service

%post client
%systemd_post libvirt-guests.service

%postun client
%systemd_postun libvirt-guests.service

%pre daemon
# 'libvirt' group is just to allow password-less polkit access to
# libvirtd. The uid number is irrelevant, so we use dynamic allocation
# described at the above link.
getent group libvirt >/dev/null || groupadd -r libvirt

exit 0

%post daemon

%systemd_post virtlockd.socket virtlockd-admin.socket
%systemd_post virtlogd.socket virtlogd-admin.socket
%systemd_post libvirtd.socket libvirtd-ro.socket libvirtd-admin.socket
%systemd_post libvirtd-tcp.socket libvirtd-tls.socket
%systemd_post libvirtd.service

# request daemon restart in posttrans
mkdir -p %{_localstatedir}/lib/rpm-state/libvirt || :
touch %{_localstatedir}/lib/rpm-state/libvirt/restart || :

%preun daemon
%systemd_preun libvirtd.service
%systemd_preun libvirtd-tcp.socket libvirtd-tls.socket
%systemd_preun libvirtd.socket libvirtd-ro.socket libvirtd-admin.socket
%systemd_preun virtlogd.socket virtlogd-admin.socket virtlogd.service
%systemd_preun virtlockd.socket virtlockd-admin.socket virtlockd.service

%postun daemon
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    /bin/systemctl reload-or-try-restart virtlockd.service >/dev/null 2>&1 || :
    /bin/systemctl reload-or-try-restart virtlogd.service >/dev/null 2>&1 || :
fi

%posttrans daemon
if [ -f %{_localstatedir}/lib/rpm-state/libvirt/restart ]; then
    # See if user has previously modified their install to
    # tell libvirtd to use --listen
    grep -E '^LIBVIRTD_ARGS=.*--listen' %{_sysconfdir}/sysconfig/libvirtd 1>/dev/null 2>&1
    if test $? = 0
    then
        # Then lets keep honouring --listen and *not* use
        # systemd socket activation, because switching things
        # might confuse mgmt tool like puppet/ansible that
        # expect the old style libvirtd
        /bin/systemctl mask libvirtd.socket >/dev/null 2>&1 || :
        /bin/systemctl mask libvirtd-ro.socket >/dev/null 2>&1 || :
        /bin/systemctl mask libvirtd-admin.socket >/dev/null 2>&1 || :
        /bin/systemctl mask libvirtd-tls.socket >/dev/null 2>&1 || :
        /bin/systemctl mask libvirtd-tcp.socket >/dev/null 2>&1 || :
    else
        # Old libvirtd owns the sockets and will delete them on
        # shutdown. Can't use a try-restart as libvirtd will simply
        # own the sockets again when it comes back up. Thus we must
        # do this particular ordering, so that we get libvirtd
        # running with socket activation in use
        /bin/systemctl is-active libvirtd.service 1>/dev/null 2>&1
        if test $? = 0
        then
            /bin/systemctl stop libvirtd.service >/dev/null 2>&1 || :

            /bin/systemctl try-restart libvirtd.socket >/dev/null 2>&1 || :
            /bin/systemctl try-restart libvirtd-ro.socket >/dev/null 2>&1 || :
            /bin/systemctl try-restart libvirtd-admin.socket >/dev/null 2>&1 || :

            /bin/systemctl start libvirtd.service >/dev/null 2>&1 || :
        fi
    fi
fi
rm -rf %{_localstatedir}/lib/rpm-state/libvirt || :

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

    UUID=`%{_bindir}/uuidgen`
    sed -e "s/${orig_sub}/${sub}/g" \
        -e "s,</name>,</name>\n  <uuid>$UUID</uuid>," \
         < %{_datadir}/libvirt/networks/default.xml \
         > %{_sysconfdir}/libvirt/qemu/networks/default.xml
    ln -s ../default.xml %{_sysconfdir}/libvirt/qemu/networks/autostart/default.xml
    # libvirt saves this file with mode 0600
    chmod 0600 %{_sysconfdir}/libvirt/qemu/networks/default.xml

    # Make sure libvirt picks up the new network defininiton
    mkdir -p %{_localstatedir}/lib/rpm-state/libvirt || :
    touch %{_localstatedir}/lib/rpm-state/libvirt/restart || :
fi

%posttrans daemon-config-network
if [ -f %{_localstatedir}/lib/rpm-state/libvirt/restart ]; then
    /bin/systemctl try-restart libvirtd.service >/dev/null 2>&1 || :
fi
rm -rf %{_localstatedir}/lib/rpm-state/libvirt || :

%post daemon-config-nwfilter
cp %{_datadir}/libvirt/nwfilter/*.xml %{_sysconfdir}/libvirt/nwfilter/
# libvirt saves these files with mode 600
chmod 600 %{_sysconfdir}/libvirt/nwfilter/*.xml
# Make sure libvirt picks up the new nwfilter defininitons
mkdir -p %{_localstatedir}/lib/rpm-state/libvirt || :
touch %{_localstatedir}/lib/rpm-state/libvirt/restart || :

%posttrans daemon-config-nwfilter
if [ -f %{_localstatedir}/lib/rpm-state/libvirt/restart ]; then
    /bin/systemctl try-restart libvirtd.service >/dev/null 2>&1 || :
fi
rm -rf %{_localstatedir}/lib/rpm-state/libvirt || :

%pre daemon-driver-qemu
# We want soft static allocation of well-known ids, as disk images
# are commonly shared across NFS mounts by id rather than name; see
# https://fedoraproject.org/wiki/Packaging:UsersAndGroups
getent group kvm >/dev/null || groupadd -f -g 36 -r kvm
getent group qemu >/dev/null || groupadd -f -g 107 -r qemu
if ! getent passwd qemu >/dev/null; then
  if ! getent passwd 107 >/dev/null; then
    useradd -r -u 107 -g qemu -G kvm -d / -s %{_sbindir}/nologin -c "qemu user" qemu
  else
    useradd -r -g qemu -G kvm -d / -s %{_sbindir}/nologin -c "qemu user" qemu
  fi
fi
exit 0

%files

%files admin
%{_mandir}/man1/virt-admin.1*
%{_bindir}/virt-admin
%{_datadir}/bash-completion/completions/virt-admin

%files client
%{_mandir}/man1/virsh.1*
%{_mandir}/man1/virt-xml-validate.1*
%{_mandir}/man1/virt-pki-validate.1*
%{_mandir}/man1/virt-host-validate.1*
%{_bindir}/virsh
%{_bindir}/virt-xml-validate
%{_bindir}/virt-pki-query-dn
%{_bindir}/virt-pki-validate
%{_bindir}/virt-host-validate

%{_datadir}/bash-completion/completions/virsh
%{_datadir}/systemtap/tapset/libvirt_functions.stp
%{_datadir}/systemtap/tapset/libvirt_probes*.stp
%{_datadir}/systemtap/tapset/libvirt_qemu_probes*.stp

%{_unitdir}/libvirt-guests.service
%config(noreplace) %{_sysconfdir}/sysconfig/libvirt-guests
%attr(0755, root, root) %{_libexecdir}/libvirt-guests.sh

%files daemon

%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/

%{_unitdir}/libvirtd.service
%{_unitdir}/libvirtd.socket
%{_unitdir}/libvirtd-ro.socket
%{_unitdir}/libvirtd-admin.socket
%{_unitdir}/libvirtd-tcp.socket
%{_unitdir}/libvirtd-tls.socket
%{_unitdir}/virtproxyd.service
%{_unitdir}/virtproxyd.socket
%{_unitdir}/virtproxyd-ro.socket
%{_unitdir}/virtproxyd-admin.socket
%{_unitdir}/virtproxyd-tcp.socket
%{_unitdir}/virtproxyd-tls.socket
%{_unitdir}/virt-guest-shutdown.target
%{_unitdir}/virtlogd.service
%{_unitdir}/virtlogd.socket
%{_unitdir}/virtlogd-admin.socket
%{_unitdir}/virtlockd.service
%{_unitdir}/virtlockd.socket
%{_unitdir}/virtlockd-admin.socket
%config(noreplace) %{_sysconfdir}/sysconfig/libvirtd
%config(noreplace) %{_sysconfdir}/sysconfig/virtlogd
%config(noreplace) %{_sysconfdir}/sysconfig/virtlockd
%config(noreplace) %{_sysconfdir}/sysconfig/virtproxyd
%config(noreplace) %{_sysconfdir}/libvirt/libvirtd.conf
%config(noreplace) %{_sysconfdir}/libvirt/virtproxyd.conf
%config(noreplace) %{_sysconfdir}/libvirt/virtlogd.conf
%config(noreplace) %{_sysconfdir}/libvirt/virtlockd.conf
%config(noreplace) %{_sysconfdir}/sasl2/libvirt.conf
%config(noreplace) %{_libdir}/sysctl.d/60-libvirtd.conf

%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd
%dir %{_datadir}/libvirt/

%ghost %dir %{_rundir}/libvirt/

%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/images/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/filesystems/
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/boot/
%dir %attr(0711, root, root) %{_localstatedir}/cache/libvirt/

%dir %attr(0755, root, root) %{_libdir}/libvirt/
%dir %attr(0755, root, root) %{_libdir}/libvirt/connection-driver/
%dir %attr(0755, root, root) %{_libdir}/libvirt/lock-driver

%attr(0755, root, root) %{_bindir}/virt-ssh-helper
%attr(0755, root, root) %{_libdir}/libvirt/lock-driver/lockd.so

%{_datadir}/augeas/lenses/libvirtd.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd.aug
%{_datadir}/augeas/lenses/virtlogd.aug
%{_datadir}/augeas/lenses/tests/test_virtlogd.aug
%{_datadir}/augeas/lenses/virtlockd.aug
%{_datadir}/augeas/lenses/tests/test_virtlockd.aug
%{_datadir}/augeas/lenses/virtproxyd.aug
%{_datadir}/augeas/lenses/tests/test_virtproxyd.aug
%{_datadir}/augeas/lenses/libvirt_lockd.aug
%{_datadir}/augeas/lenses/tests/test_libvirt_lockd.aug

%{_datadir}/polkit-1/actions/org.libvirt.unix.policy
%{_datadir}/polkit-1/actions/org.libvirt.api.policy
%{_datadir}/polkit-1/rules.d/50-libvirt.rules

%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/

%attr(0755, root, root) %{_libexecdir}/libvirt_iohelper

%attr(0755, root, root) %{_sbindir}/libvirtd
%attr(0755, root, root) %{_sbindir}/virtproxyd
%attr(0755, root, root) %{_sbindir}/virtlogd
%attr(0755, root, root) %{_sbindir}/virtlockd

%{_mandir}/man8/libvirtd.8*
%{_mandir}/man8/virtlogd.8*
%{_mandir}/man8/virtlockd.8*
%{_mandir}/man8/virtproxyd.8*
%{_mandir}/man7/virkey*.7*

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
%config(noreplace) %{_sysconfdir}/sysconfig/virtinterfaced
%config(noreplace) %{_sysconfdir}/libvirt/virtinterfaced.conf
%{_datadir}/augeas/lenses/virtinterfaced.aug
%{_datadir}/augeas/lenses/tests/test_virtinterfaced.aug
%{_unitdir}/virtinterfaced.service
%{_unitdir}/virtinterfaced.socket
%{_unitdir}/virtinterfaced-ro.socket
%{_unitdir}/virtinterfaced-admin.socket
%attr(0755, root, root) %{_sbindir}/virtinterfaced
%{_libdir}/%{name}/connection-driver/libvirt_driver_interface.so
%{_mandir}/man8/virtinterfaced.8*

%files daemon-driver-network
%config(noreplace) %{_sysconfdir}/sysconfig/virtnetworkd
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
%{_libdir}/%{name}/connection-driver/libvirt_driver_network.so
%{_mandir}/man8/virtnetworkd.8*

%files daemon-driver-nodedev
%config(noreplace) %{_sysconfdir}/sysconfig/virtnodedevd
%config(noreplace) %{_sysconfdir}/libvirt/virtnodedevd.conf
%{_datadir}/augeas/lenses/virtnodedevd.aug
%{_datadir}/augeas/lenses/tests/test_virtnodedevd.aug
%{_unitdir}/virtnodedevd.service
%{_unitdir}/virtnodedevd.socket
%{_unitdir}/virtnodedevd-ro.socket
%{_unitdir}/virtnodedevd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtnodedevd
%{_libdir}/%{name}/connection-driver/libvirt_driver_nodedev.so
%{_mandir}/man8/virtnodedevd.8*

%files daemon-driver-nwfilter
%config(noreplace) %{_sysconfdir}/sysconfig/virtnwfilterd
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
%{_libdir}/%{name}/connection-driver/libvirt_driver_nwfilter.so
%{_mandir}/man8/virtnwfilterd.8*

%files daemon-driver-qemu
%config(noreplace) %{_sysconfdir}/sysconfig/virtqemud
%config(noreplace) %{_sysconfdir}/libvirt/virtqemud.conf
%{_datadir}/augeas/lenses/virtqemud.aug
%{_datadir}/augeas/lenses/tests/test_virtqemud.aug
%{_unitdir}/virtqemud.service
%{_unitdir}/virtqemud.socket
%{_unitdir}/virtqemud-ro.socket
%{_unitdir}/virtqemud-admin.socket
%attr(0755, root, root) %{_sbindir}/virtqemud
%dir %attr(0700, root, root) %{_sysconfdir}/libvirt/qemu/
%dir %attr(0700, root, root) %{_localstatedir}/log/libvirt/qemu/
%config(noreplace) %{_sysconfdir}/libvirt/qemu.conf
%config(noreplace) %{_sysconfdir}/libvirt/qemu-lockd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/libvirtd.qemu
%ghost %dir %{_rundir}/libvirt/qemu/
%dir %attr(0751, %{qemu_user}, %{qemu_group}) %{_localstatedir}/lib/libvirt/qemu/
%dir %attr(0750, %{qemu_user}, %{qemu_group}) %{_localstatedir}/cache/libvirt/qemu/
%{_datadir}/augeas/lenses/libvirtd_qemu.aug
%{_datadir}/augeas/lenses/tests/test_libvirtd_qemu.aug
%{_libdir}/%{name}/connection-driver/libvirt_driver_qemu.so
%dir %attr(0711, root, root) %{_localstatedir}/lib/libvirt/swtpm/
%dir %attr(0711, root, root) %{_localstatedir}/log/swtpm/libvirt/qemu/
%{_bindir}/virt-qemu-run
%{_mandir}/man1/virt-qemu-run.1*
%{_mandir}/man8/virtqemud.8*

%files daemon-driver-secret
%config(noreplace) %{_sysconfdir}/sysconfig/virtsecretd
%config(noreplace) %{_sysconfdir}/libvirt/virtsecretd.conf
%{_datadir}/augeas/lenses/virtsecretd.aug
%{_datadir}/augeas/lenses/tests/test_virtsecretd.aug
%{_unitdir}/virtsecretd.service
%{_unitdir}/virtsecretd.socket
%{_unitdir}/virtsecretd-ro.socket
%{_unitdir}/virtsecretd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtsecretd
%{_libdir}/%{name}/connection-driver/libvirt_driver_secret.so
%{_mandir}/man8/virtsecretd.8*

%files daemon-driver-storage

%files daemon-driver-storage-core
%config(noreplace) %{_sysconfdir}/sysconfig/virtstoraged
%config(noreplace) %{_sysconfdir}/libvirt/virtstoraged.conf
%{_datadir}/augeas/lenses/virtstoraged.aug
%{_datadir}/augeas/lenses/tests/test_virtstoraged.aug
%{_unitdir}/virtstoraged.service
%{_unitdir}/virtstoraged.socket
%{_unitdir}/virtstoraged-ro.socket
%{_unitdir}/virtstoraged-admin.socket
%attr(0755, root, root) %{_sbindir}/virtstoraged
%attr(0755, root, root) %{_libexecdir}/libvirt_parthelper
%{_libdir}/%{name}/connection-driver/libvirt_driver_storage.so
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_fs.so
%{_libdir}/%{name}/storage-file/libvirt_storage_file_fs.so
%{_mandir}/man8/virtstoraged.8*

%files daemon-driver-storage-disk
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_disk.so

%files daemon-driver-storage-gluster
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_gluster.so
%{_libdir}/%{name}/storage-file/libvirt_storage_file_gluster.so

%files daemon-driver-storage-iscsi
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_iscsi.so

%files daemon-driver-storage-logical
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_logical.so

%files daemon-driver-storage-mpath
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_mpath.so

%files daemon-driver-storage-rbd
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_rbd.so

%files daemon-driver-storage-scsi
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_scsi.so

%files daemon-kvm

%files daemon-driver-vbox
%config(noreplace) %{_sysconfdir}/sysconfig/virtvboxd
%config(noreplace) %{_sysconfdir}/libvirt/virtvboxd.conf
%{_datadir}/augeas/lenses/virtvboxd.aug
%{_datadir}/augeas/lenses/tests/test_virtvboxd.aug
%{_unitdir}/virtvboxd.service
%{_unitdir}/virtvboxd.socket
%{_unitdir}/virtvboxd-ro.socket
%{_unitdir}/virtvboxd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtvboxd
%{_libdir}/%{name}/connection-driver/libvirt_driver_vbox.so
%{_mandir}/man8/virtvboxd.8*

%files daemon-vbox

%files devel
%{_includedir}/libvirt/*
%{_libdir}/libvirt*.so
%{_libdir}/pkgconfig/libvirt*

%dir %{_datadir}/libvirt/api/
%{_datadir}/libvirt/api/libvirt-api.xml
%{_datadir}/libvirt/api/libvirt-admin-api.xml
%{_datadir}/libvirt/api/libvirt-qemu-api.xml
%{_datadir}/libvirt/api/libvirt-lxc-api.xml

%files docs
%doc AUTHORS.rst NEWS.rst README.rst
%doc libvirt-docs/*

%files libs -f %{name}.lang
%license COPYING COPYING.LESSER
%config(noreplace) %{_sysconfdir}/libvirt/libvirt.conf
%config(noreplace) %{_sysconfdir}/libvirt/libvirt-admin.conf
%{_libdir}/libvirt.so.*
%{_libdir}/libvirt-qemu.so.*
%{_libdir}/libvirt-lxc.so.*
%{_libdir}/libvirt-admin.so.*
%dir %{_datadir}/libvirt/
%dir %{_datadir}/libvirt/schemas/
%dir %attr(0755, root, root) %{_localstatedir}/lib/libvirt/

%{_datadir}/libvirt/schemas/*.rng

%{_datadir}/libvirt/cpu_map/*.xml

%{_datadir}/libvirt/test-screenshot.png

%files lock-sanlock
%config(noreplace) %{_sysconfdir}/libvirt/qemu-sanlock.conf

%attr(0755, root, root) %{_libdir}/libvirt/lock-driver/sanlock.so
%{_datadir}/augeas/lenses/libvirt_sanlock.aug
%{_datadir}/augeas/lenses/tests/test_libvirt_sanlock.aug
%dir %attr(0770, root, sanlock) %{_localstatedir}/lib/libvirt/sanlock
%{_sbindir}/virt-sanlock-cleanup
%{_mandir}/man8/virt-sanlock-cleanup.8*
%attr(0755, root, root) %{_libexecdir}/libvirt_sanlock_helper

%files nss
%{_libdir}/libnss_libvirt.so.2
%{_libdir}/libnss_libvirt_guest.so.2

%changelog
* Wed Jan 17 2024 Harshit Gupta <guptaharshit@microsoft.com> - 7.10.0-6
- Release bump with no changes to force a rebuild and consume new libssh2 build

* Wed May 25 2023 Sharath Srikanth Chellappa <sharathsr@microsoft.com> - 7.10.0-5
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
