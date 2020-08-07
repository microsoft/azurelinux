Summary:        Virtualization API library that supports KVM, QEMU, Xen, ESX etc
Name:           libvirt
Version:        6.1.0
Release:        1%{?dist}
License:        LGPL
URL:            https://libvirt.org/
Source0:        https://libvirt.org/sources/%{name}-%{version}.tar.xz
# The fix for this CVE is already in 6.1.0.
Patch0:         CVE-2019-3886.nopatch
# The fix for this CVE is already in 6.1.0.
Patch1:         CVE-2017-1000256.nopatch
Group:          Virtualization/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  cyrus-sasl
BuildRequires:  device-mapper-devel
BuildRequires:  gnutls-devel
BuildRequires:  libxml2-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  libcap-ng-devel
BuildRequires:  libnl3-devel
BuildRequires:  libselinux-devel
BuildRequires:  libssh2-devel
BuildRequires:  systemd-devel
BuildRequires:  parted
BuildRequires:  python3-devel
BuildRequires:  readline-devel
BuildRequires:  libxslt
BuildRequires:  libtirpc-devel
BuildRequires:  python-docutils
BuildRequires:  rpcsvc-proto
Requires:       cyrus-sasl
Requires:       device-mapper
Requires:       gnutls
Requires:       libxml2
Requires:       e2fsprogs
Requires:       libcap-ng
Requires:       libnl3
Requires:       libselinux
Requires:       libssh2
Requires:       systemd
Requires:       parted
Requires:       python2
Requires:       readline
Requires:       libtirpc

%description
Libvirt is collection of software that provides a convenient way to manage virtual machines and other virtualization functionality, such as storage and network interface management. These software pieces include an API library, a daemon (libvirtd), and a command line utility (virsh).  An primary goal of libvirt is to provide a single way to manage multiple different virtualization providers/hypervisors. For example, the command 'virsh list --all' can be used to list the existing virtual machines for any supported hypervisor (KVM, Xen, VMWare ESX, etc.) No need to learn the hypervisor specific tools!

%package docs
Summary:        libvirt docs
Group:          Development/Tools
%description docs
The contains libvirt package doc files.

%package devel
Summary:        libvirt devel
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Requires:       libtirpc-devel
%description devel
This contains development tools and libraries for libvirt.

%prep
%setup -q

%define _vpath_builddir build
%build
mkdir %{_vpath_builddir}
cd %{_vpath_builddir}
../configure \
    --disable-silent-rules \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --with-udev=no \
    --with-pciaccess=no

make %{?_smp_mflags}

%install
cd %{_vpath_builddir}
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%check
cd %{_vpath_builddir}
make check

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_libdir}/libvirt*.so.*
%{_libdir}/libvirt/storage-file/libvirt_storage_file_fs.so
%{_libdir}/libvirt/storage-backend/*
%{_libdir}/libvirt/connection-driver/*.so
%{_libdir}/libvirt/lock-driver/*.so
%{_libdir}/sysctl.d/60-libvirtd.conf
%{_libdir}/systemd/system/*
/usr/libexec/*
%{_sbindir}/*

%config(noreplace)%{_sysconfdir}/sasl2/libvirt.conf
%config(noreplace)%{_sysconfdir}/libvirt/*.conf
%{_sysconfdir}/libvirt/nwfilter/*
%{_sysconfdir}/libvirt/qemu/*
%{_sysconfdir}/logrotate.d/*
%{_sysconfdir}/sysconfig/*

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
/usr/share/augeas/lenses/*
/usr/share/libvirt/*
/usr/share/doc/libvirt/*
/usr/share/locale/*
%{_mandir}/*

%changelog
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
