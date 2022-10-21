# Copyright © INRIA 2009-2010
# Brice Goglin <Brice.Goglin@inria.fr>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

%global MLNX_OFED_VERSION OFED.5.6.0.1.6.1
%global nvidia_version 90mlnx1
%global BF_VERSION 3.9.0
%global kver %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-devel))
%global ksrc %{_libdir}/modules/%{kver}/build

# set package name
%{!?_name: %global _name knem}

Summary:        KNEM: High-Performance Intra-Node MPI Communication
Name:           knem
# Update extended_release and nvidia_version with version updates
Version:        1.1.4
Release:        1%{?dist}
License:        BSD and GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
Source:         https://linux.mellanox.com/public/repo/bluefield/%{BF_VERSION}/extras/mlnx_ofed/5.6-1.0.3.3/SOURCES/%{name}_%{version}.%{nvidia_version}.orig.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  kernel-devel
BuildRequires:  kmod
Requires:       kernel
Provides:       knem-mlnx = %{version}-%{release}
Obsoletes:      knem-mlnx < %{version}-%{release}

%description
KNEM is a Linux kernel module enabling high-performance intra-node MPI communication for large messages. KNEM offers support for asynchronous and vectorial data transfers as well as offloading memory copies on to Intel I/OAT hardware.
See http://knem.gitlabpages.inria.fr for details. 
OFED release is %MLNX_OFED_VERSION of NVIDIA version %nvidia_version of knem

%global debug_package %{nil}

%global kernel_source() %{ksrc}
%global kernel_release() %{kver}
%global flavors_to_build default

%package modules
Summary: KNEM: High-Performance Intra-Node MPI Communication
Group: System Environment/Libraries
%description modules
KNEM is a Linux kernel module enabling high-performance intra-node MPI communication for large messages. KNEM offers support for asynchronous and vectorial data transfers as well as loading memory copies on to Intel I/OAT hardware.
See http://runtime.bordeaux.inria.fr/knem/ for details.


%global install_mod_dir extra/%{_name}


%prep
%autosetup -p1 -n %{name}-%{version}.%{nvidia_version}
set -- *
mkdir source
mv "$@" source/
mkdir obj
cp source/COPYING* .

%build
export INSTALL_MOD_DIR=%{install_mod_dir}
for flavor in %flavors_to_build; do
	export KSRC=%{kernel_source $flavor}
	export K_BUILD=%{kernel_source $flavor}
	export KVER=%{kernel_release $K_BUILD}
	export LIB_MOD_DIR=/lib/modules/$KVER/$INSTALL_MOD_DIR
	export MODULE_DESTDIR=/lib/modules/$KVER/$INSTALL_MOD_DIR
	rm -rf obj/$flavor
	cp -a source obj/$flavor
	cd $PWD/obj/$flavor
	find . -type f -exec touch -t 200012201010 '{}' \; || true
	./configure --prefix=/opt/knem-%{version} --with-linux-release=$KVER --with-linux=/lib/modules/$KVER/source --with-linux-build=$KSRC --libdir=/opt/knem-%{version}/lib
	make
	cd -
done

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=%install_mod_dir
export KPNAME=%{_name}
mkdir -p %{buildroot}/etc/udev/rules.d
install -d %{buildroot}/usr/lib64/pkgconfig
for flavor in %flavors_to_build; do
	cd $PWD/obj/$flavor
	export KSRC=%{kernel_source $flavor}
	export K_BUILD=%{kernel_source $flavor}
	export KVER=%{kernel_release $K_BUILD}
	make DESTDIR=%{buildroot} install KERNELRELEASE=$KVER
	export MODULE_DESTDIR=/lib/modules/$KVER/$INSTALL_MOD_DIR
	mkdir -p %{buildroot}/lib/modules/$KVER/$INSTALL_MOD_DIR
	MODULE_DESTDIR=/lib/modules/$KVER/$INSTALL_MOD_DIR DESTDIR=%{buildroot} KVERSION=$KVER %{buildroot}/opt/knem-%{version}/sbin/knem_local_install
	cp knem.pc  %{buildroot}/usr/lib64/pkgconfig
	cd -
done

/bin/rm -rf %{buildroot}/opt/knem-%{version}/lib/modules || true

# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} \( -type f -name '*.ko' -o -name '*ko.gz' \) -exec %{__strip} -p --strip-debug --discard-locals -R .comment -R .note \{\} \;

%post
getent group rdma >/dev/null 2>&1 || groupadd -r rdma
touch /etc/udev/rules.d/10-knem.rules
# load knem
/sbin/modprobe -r knem > /dev/null 2>&1
/sbin/modprobe knem > /dev/null 2>&1

# automatically load knem onboot
if [ -d /etc/sysconfig/modules ]; then
	# RH
	echo "/sbin/modprobe knem > /dev/null 2>&1" > /etc/sysconfig/modules/knem.modules
	chmod +x /etc/sysconfig/modules/knem.modules
elif [ -e /etc/sysconfig/kernel ]; then
	# SLES
	if ! (grep -w knem /etc/sysconfig/kernel); then
		sed -i -r -e 's/^(MODULES_LOADED_ON_BOOT=)"(.*)"/\1"\2 knem"/' /etc/sysconfig/kernel
	fi
fi

%preun
# unload knem
/sbin/modprobe -r knem > /dev/null 2>&1
# RH
/bin/rm -f /etc/sysconfig/modules/knem.modules
# SLES
if (grep -qw knem /etc/sysconfig/kernel 2>/dev/null); then
	sed -i -e 's/ knem//g' /etc/sysconfig/kernel 2>/dev/null
fi

%post modules
depmod %{kver} -a

%postun modules
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
	depmod %{kver} -a
fi

%files
%defattr(-, root, root)
%license COPYING COPYING.BSD-3 COPYING.GPL-2
/opt/knem-%{version}
/usr/lib64/pkgconfig/knem.pc
%config(noreplace)
/etc/udev/rules.d/10-knem.rules
%files modules
/lib/modules/%{kver}/%{install_mod_dir}/

%changelog
* Fri Jul 22 2022 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4-1
- Initial CBL-Mariner import from NVIDIA (license: GPLv2).
- Lint spec to conform to Mariner
- Remove unused module signing
- License verified

* Mon Mar 17 2014 Alaa Hleihel <alaa@mellanox.com>
- Use one spec for KMP and non-KMP OS's.

* Thu Apr 18 2013 Alaa Hleihel <alaa@mellanox.com>
- Added KMP support
