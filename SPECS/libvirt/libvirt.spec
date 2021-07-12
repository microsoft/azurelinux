%bcond_with qemu
%bcond_with libxl

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

BuildRequires:  augeas
BuildRequires:  bash-completion
BuildRequires:  cyrus-sasl
BuildRequires:  device-mapper-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  gnutls-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libnl3-devel
BuildRequires:  libselinux-devel
BuildRequires:  libssh2-devel
BuildRequires:  libtirpc-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt
BuildRequires:  parted
BuildRequires:  python-docutils
BuildRequires:  python3-devel
BuildRequires:  readline-devel
BuildRequires:  rpcsvc-proto
BuildRequires:  sanlock-devel
BuildRequires:  systemd-devel
BuildRequires:  systemtap-sdt-devel
BuildRequires:  yajl-devel

Requires:       %{name}-client  = %{version}-%{release}
Requires:       %{name}-libs    = %{version}-%{release}
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
Requires: libvirt-daemon-driver-network = %{version}-%{release}

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
    --with-macvtap \
    --with-nss-plugin \
    --with-pciaccess=no \
    --with-udev=no \
    --with-sanlock \
    --with-yajl

make %{?_smp_mflags}

%install
cd %{_vpath_builddir}
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print

%find_lang %{name}

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

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/libvirt/storage-file/libvirt_storage_file_fs.so
%{_libdir}/libvirt/storage-backend/*
%{_libdir}/libvirt/connection-driver/*.so
%{_libdir}/libvirt/lock-driver/*.so
%{_libdir}/sysctl.d/60-libvirtd.conf
%{_libdir}/systemd/system/*
%{_libexecdir}/*
%{_sbindir}/*

%config(noreplace)%{_sysconfdir}/sasl2/libvirt.conf
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
%{_datadir}/augeas/lenses/*
%{_datadir}/libvirt/*
%{_docdir}/libvirt/*
%{_datadir}/locale/*
%{_mandir}/*

%files libs
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
%if 0%{with qemu}
%config(noreplace) %{_sysconfdir}/libvirt/qemu-sanlock.conf
%endif
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
