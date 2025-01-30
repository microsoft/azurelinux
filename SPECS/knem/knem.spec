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

# KMP is disabled by default
%{!?KMP: %global KMP 0}

%global last-known-kernel 6.6.64.2

%if 0%{azl}
%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{VERSION}-%{RELEASE}' kernel-headers)
%else
%global target_kernel_version_full f.a.k.e
%endif

%global KVERSION %{target_kernel_version_full}
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

%{!?_release: %global _release OFED.23.10.0.2.1.1}
# %{!?KVERSION: %global KVERSION %(uname -r)}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}
%global _kmp_rel %{_release}%{?_kmp_build_num}%{?_dist}
%global IS_RHEL_VENDOR "%{_vendor}" == "redhat" || ("%{_vendor}" == "bclinux") || ("%{_vendor}" == "openEuler")
%global KMOD_PREAMBLE "%{_vendor}" != "openEuler"

# set package name
%{!?_name: %global _name knem}
%global non_kmp_pname %{_name}-modules

Summary:	 KNEM: High-Performance Intra-Node MPI Communication
Name:		 knem
Version:	 1.1.4.90mlnx3
Release:	 2%{?dist}
Provides:	 knem-mlnx = %{version}-%{release}
Obsoletes:	 knem-mlnx < %{version}-%{release}
License:	 BSD and GPLv2
Group:		 System Environment/Libraries
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
Source0:	 https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/knem-1.1.4.90mlnx3.tar.gz#/knem-%{version}.tar.gz
BuildRoot:       /var/tmp/%{name}-%{version}-build
ExclusiveArch:   x86_64

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel = %{target_kernel_version_full}
BuildRequires:  kernel-headers = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod

Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod


%description
KNEM is a Linux kernel module enabling high-performance intra-node MPI communication for large messages. KNEM offers support for asynchronous and vectorial data transfers as well as offloading memory copies on to Intel I/OAT hardware.
See http://knem.gitlabpages.inria.fr for details.

%global debug_package %{nil}

# build KMP rpms?
%if "%{KMP}" == "1"
%global kernel_release() $(make -C %{1} M=$PWD kernelrelease | grep -v make)
BuildRequires: %kernel_module_package_buildreqs
# prep file list for kmp rpm
%(cat > %{_builddir}/kmp.files << EOF
%defattr(644,root,root,755)
/lib/modules/%2-%1
%if %{IS_RHEL_VENDOR}
%config(noreplace) %{_sysconfdir}/depmod.d/%{_name}.conf
%endif
EOF)
%(cat > %{_builddir}/preamble << EOF
Obsoletes: kmod-knem-mlnx < %{version}-%{release}
Obsoletes: knem-mlnx-kmp-default < %{version}-%{release}
Obsoletes: knem-mlnx-kmp-trace < %{version}-%{release}
Obsoletes: knem-mlnx-kmp-xen < %{version}-%{release}
Obsoletes: knem-mlnx-kmp-trace < %{version}-%{release}
Obsoletes: knem-mlnx-kmp-ppc64 < %{version}-%{release}
Obsoletes: knem-mlnx-kmp-ppc < %{version}-%{release}
Obsoletes: knem-mlnx-kmp-smp < %{version}-%{release}
Obsoletes: knem-mlnx-kmp-pae < %{version}-%{release}
EOF)
%if %KMOD_PREAMBLE
%kernel_module_package -f %{_builddir}/kmp.files -r %{_kmp_rel} -p %{_builddir}/preamble
%else
%kernel_module_package -f %{_builddir}/kmp.files -r %{_kmp_rel}
%endif
%else # not KMP
%global kernel_source() %{K_SRC}
%global kernel_release() %{KVERSION}
%global flavors_to_build default

%package -n %{non_kmp_pname}
Release: 2%{?dist}
Summary: KNEM: High-Performance Intra-Node MPI Communication
Group: System Environment/Libraries
%description -n %{non_kmp_pname}
KNEM is a Linux kernel module enabling high-performance intra-node MPI communication for large messages. KNEM offers support for asynchronous and vectorial data transfers as well as loading memory copies on to Intel I/OAT hardware.
See http://runtime.bordeaux.inria.fr/knem/ for details.
%endif #end if "%{KMP}" == "1"

#
# setup module sign scripts if paths to the keys are given
#
%global WITH_MOD_SIGN %(if ( test -f "$MODULE_SIGN_PRIV_KEY" && test -f "$MODULE_SIGN_PUB_KEY" ); \
	then \
		echo -n '1'; \
	else \
		echo -n '0'; fi)

%if "%{WITH_MOD_SIGN}" == "1"
# call module sign script
%global __modsign_install_post \
    $RPM_BUILD_DIR/knem-%{version}/source/tools/sign-modules $RPM_BUILD_ROOT/lib/modules/ %{kernel_source default} || exit 1 \
%{nil}

# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%global __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  %{__modsign_install_post} \
%{nil}

%endif # end of setup module sign scripts
#

%if "%{_vendor}" == "suse"
%global install_mod_dir updates
%endif


%global install_mod_dir extra/%{_name}
%global __find_requires %{nil}

%prep
%setup -n knem-%{version}
set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
rm -rf $RPM_BUILD_ROOT
export INSTALL_MOD_DIR=%install_mod_dir
for flavor in %flavors_to_build; do
	export KSRC=%{kernel_source $flavor}
	export KVERSION=%{kernel_release $KSRC}
	export LIB_MOD_DIR=/lib/modules/$KVERSION/$INSTALL_MOD_DIR
	export MODULE_DESTDIR=/lib/modules/$KVERSION/$INSTALL_MOD_DIR
	rm -rf obj/$flavor
	cp -a source obj/$flavor
	cd $PWD/obj/$flavor
	find . -type f -exec touch -t 200012201010 '{}' \; || true
	./configure --prefix=/opt/knem-%{version} --with-linux-release=$KVERSION --with-linux=/lib/modules/$KVERSION/source --with-linux-build=$KSRC --libdir=/opt/knem-%{version}/lib
	make
	cd -
done

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=%install_mod_dir
export KPNAME=%{_name}
mkdir -p $RPM_BUILD_ROOT/etc/udev/rules.d
install -d $RPM_BUILD_ROOT/usr/lib64/pkgconfig
for flavor in %flavors_to_build; do
	cd $PWD/obj/$flavor
	export KSRC=%{kernel_source $flavor}
	export KVERSION=%{kernel_release $KSRC}
	make DESTDIR=$RPM_BUILD_ROOT install KERNELRELEASE=$KVERSION
	export MODULE_DESTDIR=/lib/modules/$KVERSION/$INSTALL_MOD_DIR
	mkdir -p $RPM_BUILD_ROOT/lib/modules/$KVERSION/$INSTALL_MOD_DIR
	MODULE_DESTDIR=/lib/modules/$KVERSION/$INSTALL_MOD_DIR DESTDIR=$RPM_BUILD_ROOT KVERSION=$KVERSION $RPM_BUILD_ROOT/opt/knem-%{version}/sbin/knem_local_install
	cp knem.pc  $RPM_BUILD_ROOT/usr/lib64/pkgconfig
	cd -
done

/bin/rm -rf %{buildroot}/opt/knem-%{version}/lib/modules || true

%if %{IS_RHEL_VENDOR}
# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} \( -type f -name '*.ko' -o -name '*ko.gz' \) -exec %{__chmod} u+x \{\} \;

%if ! 0%{?fedora}
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d/
echo "override knem * weak-updates/%{_name}" >> $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d/%{_name}.conf
echo "override knem * extra/%{_name}" >> $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d/%{_name}.conf
%endif
%else
find %{buildroot} \( -type f -name '*.ko' -o -name '*ko.gz' \) -exec %{__strip} -p --strip-debug --discard-locals -R .comment -R .note \{\} \;
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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

%if "%{KMP}" != "1"
%post -n %{non_kmp_pname}
depmod %{KVERSION} -a

%postun -n %{non_kmp_pname}
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
	depmod %{KVERSION} -a
fi
%endif # end KMP=1

%files
%defattr(-, root, root)
%license source/COPYING source/COPYING.BSD-3 source/COPYING.GPL-2
/opt/knem-%{version}
/usr/lib64/pkgconfig/knem.pc

%config(noreplace)
/etc/udev/rules.d/10-knem.rules


%if "%{KMP}" != "1"
%files -n %{non_kmp_pname}
%license source/COPYING source/COPYING.BSD-3 source/COPYING.GPL-2
/lib/modules/%{KVERSION}/%{install_mod_dir}/
%if %{IS_RHEL_VENDOR}
%if ! 0%{?fedora}
%config(noreplace) %{_sysconfdir}/depmod.d/%{_name}.conf
%endif
%endif
%endif

%changelog
* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-2
- Bump release to match kernel

* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 1.1.4.90mlnx3-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
* Mon Mar 17 2014 Alaa Hleihel <alaa@mellanox.com>
- Use one spec for KMP and non-KMP OS's.
* Thu Apr 18 2013 Alaa Hleihel <alaa@mellanox.com>
- Added KMP support
