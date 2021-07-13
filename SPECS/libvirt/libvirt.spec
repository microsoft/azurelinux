%bcond_with libxl

# Force QEMU to run as non-root
%define qemu_user  qemu
%define qemu_group  qemu

Summary:        Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:           libvirt
Version:        6.1.0
Release:        3%{?dist}
License:        LGPL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Virtualization/Libraries
URL:            https://libvirt.org/
Source0:        https://libvirt.org/sources/%{name}-%{version}.tar.xz
# The fix for this CVE is already in 6.1.0.
Patch0:         CVE-2019-3886.nopatch
# The fix for this CVE is already in 6.1.0.
Patch1:         CVE-2017-1000256.nopatch
Patch2:         CVE-2020-25637.patch

BuildRequires:  /usr/bin/qemu-img
BuildRequires:  augeas
BuildRequires:  bash-completion
BuildRequires:  cyrus-sasl-devel
BuildRequires:  dbus-devel
BuildRequires:  device-mapper-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  gnutls-devel
BuildRequires:  libacl-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libnl3-devel
BuildRequires:  libpciaccess-devel
BuildRequires:  libselinux-devel
BuildRequires:  libssh2-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  numactl-devel
BuildRequires:  numad
BuildRequires:  parted
BuildRequires:  polkit
BuildRequires:  python-docutils
BuildRequires:  python3-devel
BuildRequires:  readline-devel
BuildRequires:  rpcsvc-proto
BuildRequires:  sanlock-devel
BuildRequires:  systemd-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  yajl-devel

Requires:       %{name}-client               =  %{version}-%{release}
Requires:       %{name}-daemon-driver-interface = %{version}-%{release}
Requires:       %{name}-daemon-driver-network = %{version}-%{release}
Requires:       %{name}-daemon-driver-nodedev = %{version}-%{release}
Requires:       %{name}-daemon-driver-nwfilter = %{version}-%{release}
Requires:       %{name}-daemon-driver-qemu = %{version}-%{release}
Requires:       %{name}-daemon-driver-secret = %{version}-%{release}
Requires:       %{name}-daemon-driver-storage = %{version}-%{release}
Requires:       %{name}-daemon-driver-vbox   =  %{version}-%{release}
Requires:       %{name}-libs                 =  %{version}-%{release}
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
Requires:       python2
Requires:       readline
Requires:       systemd

%description
Libvirt is collection of software that provides a convenient way to manage virtual machines and other virtualization functionality, such as storage and network interface management. These software pieces include an API library, a daemon (libvirtd), and a command line utility (virsh).  An primary goal of libvirt is to provide a single way to manage multiple different virtualization providers/hypervisors. For example, the command 'virsh list --all' can be used to list the existing virtual machines for any supported hypervisor (KVM, Xen, VMWare ESX, etc.) No need to learn the hypervisor specific tools!

%package admin
Summary: Set of tools to control libvirt daemon

Requires: %{name}-bash-completion = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: readline

%description admin
The client side utilities to control the libvirt daemon.

%package bash-completion
Summary: Bash completion script

%description bash-completion
Bash completion script stub.

%package client
Summary: Client side utilities of the libvirt library

Requires: %{name}-bash-completion = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
# Needed by libvirt-guests.sh script.
Requires: gettext
# Needed by virt-pki-validate script.
Requires: gnutls-utils
Requires: ncurses
Requires: readline

%description client
The client binaries needed to access the virtualization
capabilities of recent versions of Linux (and other OSes).

%package daemon
Summary: Server side daemon and supporting files for libvirt library

Requires: %{name}-libs = %{version}-%{release}

# (client invokes 'nc' against the UNIX socket on the server)
Requires: /usr/bin/nc

%ifarch x86_64
# For virConnectGetSysinfo
Requires: dmidecode
%endif

# for modprobe of pci devices
Requires: module-init-tools

# for /sbin/ip & /sbin/tc
Requires: iproute

Requires: polkit >= 0.112

Requires: numad

# libvirtd depends on 'messagebus' service
Requires: dbus

# For uid creation during pre
Requires(pre): shadow-utils

# For service management
Requires(post): systemd-units
Requires(post): systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units

%description daemon
Server side daemon required to manage the virtualization capabilities
of recent versions of Linux. Requires a hypervisor specific sub-RPM
for specific drivers.

%package daemon-driver-qemu
Summary: QEMU driver plugin for the libvirtd daemon
Requires: %{name}-daemon = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: /usr/bin/qemu-img
# For image compression
Requires: gzip
Requires: bzip2
Requires: lzop
Requires: xz
    %if 0%{?fedora} || 0%{?rhel} > 7
Requires: systemd-container
    %endif

%description daemon-driver-qemu
The qemu driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
QEMU

%package daemon-driver-secret
Summary: Secret driver plugin for the libvirtd daemon
Requires: %{name}-daemon = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description daemon-driver-secret
The secret driver plugin for the libvirtd daemon, providing
an implementation of the secret key APIs.

%package daemon-driver-storage-core
Summary: Storage driver plugin including base backends for the libvirtd daemon

Requires: %{name}-daemon = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: nfs-utils
# For mkfs
Requires: util-linux
Requires: /usr/bin/qemu-img

%description daemon-driver-storage-core
The storage driver plugin for the libvirtd daemon, providing
an implementation of the storage APIs using files, local disks, LVM, SCSI,
iSCSI, and multipath storage.

%package daemon-driver-vbox
Summary: VirtualBox driver plugin for the libvirtd daemon

Requires: %{name}-daemon = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description daemon-driver-vbox
The vbox driver plugin for the libvirtd daemon, providing
an implementation of the hypervisor driver APIs using
VirtualBox

%package daemon-vbox
Summary: Server side daemon & driver required to run VirtualBox guests

Requires: %{name}-daemon = %{version}-%{release}
Requires: %{name}-daemon-driver-vbox = %{version}-%{release}
Requires: %{name}-daemon-driver-interface = %{version}-%{release}
Requires: %{name}-daemon-driver-network = %{version}-%{release}
Requires: %{name}-daemon-driver-nodedev = %{version}-%{release}
Requires: %{name}-daemon-driver-nwfilter = %{version}-%{release}
Requires: %{name}-daemon-driver-secret = %{version}-%{release}
Requires: %{name}-daemon-driver-storage = %{version}-%{release}

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
Summary: Client side libraries
# So remote clients can access libvirt over SSH tunnel
Requires: cyrus-sasl
# Needed by default sasl.conf - no onerous extra deps, since
# 100's of other things on a system already pull in krb5-libs
Requires: cyrus-sasl-gssapi

%description libs
Shared libraries for accessing the libvirt daemon.

%package nss
Summary: Libvirt plugin for Name Service Switch
Requires: %{name}-daemon-driver-network = %{version}-%{release}

%package lock-sanlock
Summary: Sanlock lock manager plugin for QEMU driver

Requires: sanlock
#for virt-sanlock-cleanup require augeas
Requires: augeas
Requires: %{name}-daemon = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}

%description lock-sanlock
Includes the Sanlock lock manager plugin for the QEMU
driver

%description nss
Libvirt plugin for NSS for translating domain names into IP addresses.

%prep
%autosetup -p1

%define _vpath_builddir build

%build
mkdir %{_vpath_builddir}
cd %{_vpath_builddir}
../configure \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --with-driver-modules \
    --with-libvirtd \
    --with-macvtap \
    --with-nss-plugin \
    --with-numactl \
    --with-numad \
    --with-pciaccess \
    --with-polkit \
    --with-qemu \
    --with-qemu-user=%{qemu_user} \
    --with-qemu-group=%{qemu_group} \
    --with-sanlock \
    --with-sasl \
    --with-udev \
    --with-yajl

make %{?_smp_mflags}

%install
cd %{_vpath_builddir}
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%find_lang %{name}

# Copied into libvirt-docs subpackage eventually
mv %{buildroot}%{_datadir}/doc/libvirt libvirt-docs

%ifarch x86_64
mv %{buildroot}%{_datadir}/systemtap/tapset/libvirt_probes.stp \
   %{buildroot}%{_datadir}/systemtap/tapset/libvirt_probes-64.stp

mv %{buildroot}%{_datadir}/systemtap/tapset/libvirt_qemu_probes.stp \
   %{buildroot}%{_datadir}/systemtap/tapset/libvirt_qemu_probes-64.stp
%endif

%check
cd %{_vpath_builddir}
make check

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
    grep -E '^LIBVIRTD_ARGS=.*--listen' /etc/sysconfig/libvirtd 1>/dev/null 2>&1
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

%pre daemon-driver-qemu
# We want soft static allocation of well-known ids, as disk images
# are commonly shared across NFS mounts by id rather than name; see
# https://fedoraproject.org/wiki/Packaging:UsersAndGroups
getent group kvm >/dev/null || groupadd -f -g 36 -r kvm
getent group qemu >/dev/null || groupadd -f -g 107 -r qemu
if ! getent passwd qemu >/dev/null; then
  if ! getent passwd 107 >/dev/null; then
    useradd -r -u 107 -g qemu -G kvm -d / -s /usr/sbin/nologin -c "qemu user" qemu
  else
    useradd -r -g qemu -G kvm -d / -s /usr/sbin/nologin -c "qemu user" qemu
  fi
fi
exit 0

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libvirt/storage-file/libvirt_storage_file_fs.so
%{_libdir}/libvirt/storage-backend/*
%{_libdir}/libvirt/connection-driver/*.so
%{_libdir}/systemd/system/*
%{_libexecdir}/*
%{_sbindir}/*

%config(noreplace)%{_sysconfdir}/libvirt/*.conf
%{_sysconfdir}/libvirt/nwfilter/*
%{_sysconfdir}/libvirt/qemu/*
%{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sysconfig/*

%files admin
%{_bindir}/virt-admin
%{_datadir}/bash-completion/completions/virt-admin

%files bash-completion
%{_datadir}/bash-completion/completions/vsh

%files client
#%%{_mandir}/man1/virsh.1*
#%%{_mandir}/man1/virt-xml-validate.1*
#%%{_mandir}/man1/virt-pki-validate.1*
#%%{_mandir}/man1/virt-host-validate.1*
%{_bindir}/virsh
%{_bindir}/virt-xml-validate
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
%{_mandir}/man7/virkey*.7*

%files daemon-driver-qemu
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

%files daemon-driver-secret
%config(noreplace) %{_sysconfdir}/libvirt/virtsecretd.conf
%{_datadir}/augeas/lenses/virtsecretd.aug
%{_datadir}/augeas/lenses/tests/test_virtsecretd.aug
%{_unitdir}/virtsecretd.service
%{_unitdir}/virtsecretd.socket
%{_unitdir}/virtsecretd-ro.socket
%{_unitdir}/virtsecretd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtsecretd
%{_libdir}/%{name}/connection-driver/libvirt_driver_secret.so

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
%{_libdir}/%{name}/connection-driver/libvirt_driver_storage.so
%{_libdir}/%{name}/storage-backend/libvirt_storage_backend_fs.so
%{_libdir}/%{name}/storage-file/libvirt_storage_file_fs.so

%files daemon-driver-vbox
%config(noreplace) %{_sysconfdir}/libvirt/virtvboxd.conf
%{_datadir}/augeas/lenses/virtvboxd.aug
%{_datadir}/augeas/lenses/tests/test_virtvboxd.aug
%{_unitdir}/virtvboxd.service
%{_unitdir}/virtvboxd.socket
%{_unitdir}/virtvboxd-ro.socket
%{_unitdir}/virtvboxd-admin.socket
%attr(0755, root, root) %{_sbindir}/virtvboxd
%{_libdir}/%{name}/connection-driver/libvirt_driver_vbox.so

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
%doc AUTHORS ChangeLog NEWS README README.md
%doc %{_vpath_builddir}/libvirt-docs/*

%files libs -f %{_vpath_builddir}/%{name}.lang
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

%{_datadir}/libvirt/schemas/basictypes.rng
%{_datadir}/libvirt/schemas/capability.rng
%{_datadir}/libvirt/schemas/cputypes.rng
%{_datadir}/libvirt/schemas/domain.rng
%{_datadir}/libvirt/schemas/domainbackup.rng
%{_datadir}/libvirt/schemas/domaincaps.rng
%{_datadir}/libvirt/schemas/domaincheckpoint.rng
%{_datadir}/libvirt/schemas/domaincommon.rng
%{_datadir}/libvirt/schemas/domainsnapshot.rng
%{_datadir}/libvirt/schemas/interface.rng
%{_datadir}/libvirt/schemas/network.rng
%{_datadir}/libvirt/schemas/networkcommon.rng
%{_datadir}/libvirt/schemas/networkport.rng
%{_datadir}/libvirt/schemas/nodedev.rng
%{_datadir}/libvirt/schemas/nwfilter.rng
%{_datadir}/libvirt/schemas/nwfilter_params.rng
%{_datadir}/libvirt/schemas/nwfilterbinding.rng
%{_datadir}/libvirt/schemas/secret.rng
%{_datadir}/libvirt/schemas/storagecommon.rng
%{_datadir}/libvirt/schemas/storagepool.rng
%{_datadir}/libvirt/schemas/storagepoolcaps.rng
%{_datadir}/libvirt/schemas/storagevol.rng

%{_datadir}/libvirt/cpu_map/*.xml

%{_datadir}/libvirt/test-screenshot.png

%files lock-sanlock
%config(noreplace) %{_sysconfdir}/libvirt/qemu-sanlock.conf
%if 0%{with libxl}
%config(noreplace) %{_sysconfdir}/libvirt/libxl-sanlock.conf
%endif

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
*   Mon Jul 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.1.0-3
-    Extending with subpackages using Fedora 33 spec (license: MIT).
-    Added subpackages:
      - 'libvirt-admin',
      - 'libvirt-bash-completion',
      - 'libvirt-client',
      - 'libvirt-daemon',
      - 'libvirt-libs',
      - 'libvirt-lock-sanlock',
      - 'libvirt-nss'.

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
