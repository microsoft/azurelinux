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

%if 0%{azl}
# hard code versions due to ADO bug:58993948
%global target_azl_build_kernel_version 6.12.57.1
%global target_kernel_release 3
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}
%else
%global target_kernel_version_full f.a.k.e
%endif

%global KVERSION %{target_kernel_version_full}
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

%{!?_release: %global _release OFED.25.07.0.9.7.1}
# %{!?KVERSION: %global KVERSION %(uname -r)}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}
%global _kmp_rel %{_release}%{?_kmp_build_num}%{?_dist}
%global IS_RHEL_VENDOR "%{_vendor}" == "redhat" || ("%{_vendor}" == "bclinux") || ("%{_vendor}" == "openEuler")
%global KMOD_PREAMBLE "%{_vendor}" != "openEuler"

# set package name
%{!?_name: %global _name knem-hwe}
%global non_kmp_pname %{name}-modules

Summary:	 KNEM: High-Performance Intra-Node MPI Communication
Name:		 knem-hwe
Version:	 1.1.4.90mlnx3
Release:	 27%{release_suffix}%{?dist}
Provides:	 knem-hwe-mlnx = %{version}-%{release}
Obsoletes:	 knem-hwe-mlnx < %{version}-%{release}
License:	 BSD and GPLv2
Group:		 System Environment/Libraries
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:         %{_distro_sources_url}/knem-%{version}.tar.gz
BuildRoot:       /var/tmp/%{name}-%{version}-build

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-hwe-devel = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod

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
Summary: KNEM: High-Performance Intra-Node MPI Communication
Group: System Environment/Libraries
Requires: kernel-hwe = %{target_kernel_version_full}
Requires: kmod
Conflicts: knem-modules

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
for flavor in %flavors_to_build; do
	cd $PWD/obj/$flavor
	export KSRC=%{kernel_source $flavor}
	export KVERSION=%{kernel_release $KSRC}
	make DESTDIR=$RPM_BUILD_ROOT install KERNELRELEASE=$KVERSION
	export MODULE_DESTDIR=/lib/modules/$KVERSION/$INSTALL_MOD_DIR
	mkdir -p $RPM_BUILD_ROOT/lib/modules/$KVERSION/$INSTALL_MOD_DIR
	MODULE_DESTDIR=/lib/modules/$KVERSION/$INSTALL_MOD_DIR DESTDIR=$RPM_BUILD_ROOT KVERSION=$KVERSION $RPM_BUILD_ROOT/opt/knem-%{version}/sbin/knem_local_install
	cd -
done

/bin/rm -rf %{buildroot}/opt/knem-%{version}
/bin/rm -rf %{buildroot}/etc/udev/rules.d

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

%if "%{KMP}" != "1"
%post -n %{non_kmp_pname}
depmod %{KVERSION} -a

%postun -n %{non_kmp_pname}
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
	depmod %{KVERSION} -a
fi
%endif # end KMP=1


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
* Mon Feb 02 2026 Sean Dougherty <sdougherty@microsoft.com> - 1.1.4.90mlnx3-27_6.12.57.1.3
- Bump release to match kernel-hwe

* Mon Jan 19 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1.4.90mlnx3-26_6.12.57.1.2
- Bump to match kernel-hwe.

* Tue Nov 18 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.1.4.90mlnx3-25_6.12.57.1.1
- Build with OFED 25.07.0.9.7.1.
- Enable build on x86_64 kernel hwe.
- Update source path

* Wed Nov 05 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 1.1.4.90mlnx3-24_6.12.57.1.1
- Bump to match kernel-hwe

* Fri Oct 10 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.4.90mlnx3-23_6.12.50.2-1
- Adjusted package dependencies on user space components.

* Fri Oct 06 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 1.1.4.90mlnx3-22_6.12.50.2-1
- Bump to match kernel-hwe

* Fri Sep 12 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-21
- Bump to match kernel-hwe

* Mon Sep 08 2025 Elaheh Dehghani <edehghani@microsoft.com> - 1.1.4.90mlnx3-20
- Build using kernel-hwe for aarch64 architecture

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4.90mlnx3-19
- Bump release to rebuild for new kernel release

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 1.1.4.90mlnx3-18
- Bump release to rebuild for new kernel release

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 1.1.4.90mlnx3-17
- Bump release to rebuild for new kernel release

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 1.1.4.90mlnx3-16
- Bump release to rebuild for new kernel release

* Wed Apr 09 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.4.90mlnx3-15
- Removed extra 'Release' tag from the spec file

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4.90mlnx3-14
- Bump release to rebuild for new kernel release

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4.90mlnx3-13
- Bump release to rebuild for new kernel release

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.1.4.90mlnx3-12
- Bump release to rebuild for new kernel release

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 1.1.4.90mlnx3-11
- Bump release to rebuild for new kernel release

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-10
- Bump release to rebuild for new kernel release

* Tue Mar 04 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-9
- Bump release to rebuild for new kernel release

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 1.1.4.90mlnx3-8
- Bump release to rebuild for new kernel release

* Tue Feb 11 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-7
- Bump release to rebuild for new kernel release

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 1.1.4.90mlnx3-6
- Bump release to rebuild for new kernel release

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 1.1.4.90mlnx3-5
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevara@microsoft.com> - 1.1.4.90mlnx3-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevara@microsoft.com> - 1.1.4.90mlnx3-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 1.1.4.90mlnx3-2
- Bump release to match kernel

* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 1.1.4.90mlnx3-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
* Mon Mar 17 2014 Alaa Hleihel <alaa@mellanox.com>
- Use one spec for KMP and non-KMP OS's.
* Thu Apr 18 2013 Alaa Hleihel <alaa@mellanox.com>
- Added KMP support
