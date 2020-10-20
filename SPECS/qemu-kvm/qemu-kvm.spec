Summary:	QEMU is a machine emulator and virtualizer
Name:		qemu-kvm
Version:	4.2.0
Release:    11%{?dist}
License:    GPLv2 and GPLv2+ and CC-BY and BSD
Group:      Development/Tools
URL:        https://www.qemu.org/
Source0:    https://download.qemu.org/qemu-%{version}.tar.xz
Source1:    65-kvm.rules
# https://git.qemu.org/?p=qemu.git;a=commit;h=8ffb7265af64ec81748335ec8f20e7ab542c3850
Patch0:      CVE-2020-11102.patch
# This vulnerability is in libslirp source code. And qemu is exposed to it when configured with libslirp.
# Since Mariner does not have libslirp, it is not applicable.
Patch1:      CVE-2020-7039.nopatch
Patch2:      CVE-2020-1711.patch
Patch3:      CVE-2020-7211.patch
Patch4:      CVE-2019-20175.patch
Patch5:      CVE-2020-13659.patch
Patch6:      CVE-2020-16092.patch
Patch7:      CVE-2020-15863.patch
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires: python3-devel
BuildRequires: glib-devel
BuildRequires: pixman-devel
BuildRequires: alsa-lib-devel
BuildRequires: zlib-devel
Requires: alsa-lib
Requires: cyrus-sasl
Requires: pixman

%description
QEMU is a generic and open source machine & userspace emulator and virtualizer.

%global debug_package %{nil}

%package -n qemu-img
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools
Requires: glib
Requires: pixman
Requires: libstdc++

%description -n qemu-img
This package provides a command line tool for manipulating disk images.

%prep
%setup -q -n qemu-%{version}
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build

%ifarch aarch64
   QEMU_ARCH=aarch64-softmmu
%else
   QEMU_ARCH=x86_64-softmmu
%endif

./configure \
 --prefix="%{_prefix}" \
 --libdir="%{_libdir}" \
 --audio-drv-list=alsa \
%ifarch aarch64
 --extra-cflags="%{optflags} -fPIC" \
%endif
 --target-list=$QEMU_ARCH &&
unset QEMU_ARCH &&
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/udev
install -d %{buildroot}%{_libdir}/udev/rules.d
install -D -m0644 %{SOURCE1} %{buildroot}%{_libdir}/udev/rules.d

chgrp kvm  %{buildroot}%{_libexecdir}/qemu-bridge-helper &&
chmod 4750 %{buildroot}%{_libexecdir}/qemu-bridge-helper

ln -sv qemu-system-`uname -m` %{buildroot}%{_bindir}/qemu
chmod 755 %{buildroot}%{_bindir}/qemu

%check
# Deliberately empty

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/qemu-system-*
%{_bindir}/elf2dmp
%{_bindir}/ivshmem-client
%{_bindir}/ivshmem-server
%{_bindir}/qemu-edid
%{_bindir}/qemu-ga
%{_bindir}/qemu-pr-helper
%{_bindir}/qemu
%{_bindir}/virtfs-proxy-helper
%{_libdir}/*
%{_libexecdir}/*
%{_datadir}/*

%files -n qemu-img
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd

%changelog
*   Mon Sep 14 2020 Nicolas Guibourge <nicolasg@microsoft.com> 4.2.0-11
-   Add patch for CVE-2020-15863
*   Wed Sep 02 2020 Nicolas Ontiveros <niontive@microsoft.com> 4.2.0-10
-   Add patch for CVE-2020-16092
*   Tue Jun 09 2020 Paul Monson <paulmon@microsoft.com> 4.2.0-9
-   Add patch for CVE-2019-20175
-   Add patch for CVE-2020-13659
*   Thu May 21 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 4.2.0-8
-   Fix CVE-2020-1711 and CVE-2020-7211.
*   Sat May 09 00:20:51 PST 2020 Nick Samson <nisamson@microsoft.com> - 4.2.0-7
-   Added %%license line automatically
*   Fri May  1 2020 Emre Girgin <mrgirgin@microsoft.com> 4.2.0-6
-   Renaming qemu to qemu-kvm
*   Tue Apr 21 2020 Emre Girgin <mrgirgin@microsoft.com> 4.2.0-5
-   Fix CVE-2020-11102.
-   Ignore CVE-2020-7039.
-   Update license and URL.
-   License verified.
*   Mon Mar 30 2020 Chris Co <chrco@microsoft.com> 4.2.0-4
-   Fix changelog to not define a sha1 macro
*   Fri Mar 27 2020 Chris Co <chrco@microsoft.com> 4.2.0-3
-   Add elf2dmp and virtfs-proxy-helper binaries to package
-   Delete unused sha1
*   Tue Mar 24 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 4.2.0-2
-   Add Qemu KVM support
*   Wed Jan 8 2020 Paul Monson <paulmon@microsoft.com> 4.2.0-1
-   Original version for CBL-Mariner.
