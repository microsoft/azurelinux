#
# Copyright (c) 2012 Mellanox Technologies. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 1) under the terms of the "Common Public License 1.0" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/cpl.php.
#
# 2) under the terms of the "The BSD License" a copy of which is
#    available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/bsd-license.php.
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    http://www.opensource.org/licenses/gpl-license.php.
#
# Licensee has the right to choose one of the above licenses.
#
# Redistributions of source code must retain the above copyright
# notice and one of the license notices.
#
# Redistributions in binary form must reproduce both the above copyright
# notice, one of the license notices in the documentation
# and/or other materials provided with the distribution.
#
#

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

# KMP is disabled by default
%{!?KMP: %global KMP 0}

%{!?configure_options: %global configure_options --with-core-mod --with-user_mad-mod --with-user_access-mod --with-addr_trans-mod --with-mlx5-mod --with-mlxfw-mod --with-ipoib-mod}

%global MEMTRACK %(if ( echo %{configure_options} | grep "with-memtrack" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%global MADEYE %(if ( echo %{configure_options} | grep "with-madeye-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)

%global WINDRIVER %(if (grep -qiE "Wind River" /etc/issue /etc/*release* 2>/dev/null); then echo -n '1'; else echo -n '0'; fi)
%global POWERKVM %(if (grep -qiE "powerkvm" /etc/issue /etc/*release* 2>/dev/null); then echo -n '1'; else echo -n '0'; fi)
%global BLUENIX %(if (grep -qiE "Bluenix" /etc/issue /etc/*release* 2>/dev/null); then echo -n '1'; else echo -n '0'; fi)
%global XENSERVER65 %(if (grep -qiE "XenServer.*6\.5" /etc/issue /etc/*release* 2>/dev/null); then echo -n '1'; else echo -n '0'; fi)

%global IS_RHEL_VENDOR "%{_vendor}" == "redhat" || ("%{_vendor}" == "bclinux") || ("%{_vendor}" == "openEuler")
%global KMOD_PREAMBLE "%{_vendor}" != "openEuler"

# MarinerOS 1.0 sets -fPIE in the hardening cflags
# (in the gcc specs file).
# This seems to break only this package and not other kernel packages.
%if "%{_vendor}" == "mariner" || "%{_vendor}" == "azl" || "%{_vendor}" == "azurelinux" || (0%{?rhel} >= 10)
%global _hardened_cflags %{nil}
%endif

# WA: Centos Stream 10 kernel doesn't support PIC mode, so we removed the following flags
%if (0%{?rhel} >= 10)
%global _hardening_gcc_ldflags %{nil}
%global _gcc_lto_cflags %{nil}
%endif

# %{!?KVERSION: %global KVERSION %(uname -r)}
%{!?KVERSION: %global KVERSION %{target_kernel_version_full}}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
# take path to kernel sources if provided, otherwise look in default location (for non KMP rpms).
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}

# Select packages to build

%{!?LIB_MOD_DIR: %global LIB_MOD_DIR /lib/modules/%{KVERSION}/updates}

%{!?IB_CONF_DIR: %global IB_CONF_DIR /etc/infiniband}

%{!?KERNEL_SOURCES: %global KERNEL_SOURCES /lib/modules/%{KVERSION}/source}

%global base_name mlnx-ofa_kernel
%{!?_name: %global _name %{base_name}-hwe}
%{!?_version: %global _version 25.07}
%{!?_release: %global _release OFED.25.07.0.9.7.1}
%global _kmp_rel %{_release}%{?_kmp_build_num}%{?_dist}
%global MLNX_OFA_DRV_SRC 24.10-0.7.0

%global utils_pname %{name}
%global devel_pname %{name}-devel
%global non_kmp_pname %{name}-modules

# !!!! some OOT spec depends on this the exact version and release nb of this component
# !!!! do not forget to upgrade those spec when upgrading version or release nb
# !!!! e.g.: when going from version 24.10 to 24.11 or going from release 20 to 21
# !!!! to identify the depend spec look for "_mofed_full_version"

Summary:	 Infiniband HCA Driver
Name:		 mlnx-ofa_kernel-hwe
Version:	 25.07
Release:	 3%{release_suffix}%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com/
Group:		 System Environment/Base
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:         %{_distro_sources_url}/mlnx-ofa_kernel-%{_version}.tgz

BuildRoot:	 /var/tmp/%{name}-%{version}-build
Vendor:          Microsoft Corporation
Distribution:    Azure Linux

Obsoletes: kernel-ib
Obsoletes: mlnx-en
Obsoletes: mlnx_en
Obsoletes: mlnx-en-utils
Obsoletes: kmod-mlnx-en
Obsoletes: mlnx-en-kmp-default
Obsoletes: mlnx-en-kmp-xen
Obsoletes: mlnx-en-kmp-trace
Obsoletes: mlnx-en-doc
Obsoletes: mlnx-en-debuginfo
Obsoletes: mlnx-en-sources

BuildRequires:  kernel-hwe-devel = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  kmod
BuildRequires:  libstdc++-devel
BuildRequires:  libunwind-devel
BuildRequires:  pkgconfig

%if "%{KMP}" == "1"
BuildRequires: %kernel_module_package_buildreqs
BuildRequires: /usr/bin/perl
%endif
%description
InfiniBand "verbs", Access Layer  and ULPs.
Utilities rpm.
The driver sources are located at: http://www.mellanox.com/downloads/ofed/mlnx-ofa_kernel-%{MLNX_OFA_DRV_SRC}.tgz


# build KMP rpms?
%if "%{KMP}" == "1"
%global kernel_release() $(make -s -C %{1} kernelrelease M=$PWD)
# prep file list for kmp rpm
%(cat > %{_builddir}/kmp.files << EOF
%defattr(644,root,root,755)
/lib/modules/%2-%1
%if %{IS_RHEL_VENDOR}
%config(noreplace) %{_sysconfdir}/depmod.d/zz01-%{_name}-*.conf
%endif
EOF)
%(echo "Obsoletes: kmod-mlnx-rdma-rxe, mlnx-rdma-rxe-kmp" >> %{_builddir}/preamble)
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
Obsoletes: kernel-ib
Obsoletes: mlnx-en
Obsoletes: mlnx_en
Obsoletes: mlnx-en-utils
Obsoletes: kmod-mlnx-en
Obsoletes: mlnx-en-kmp-default
Obsoletes: mlnx-en-kmp-xen
Obsoletes: mlnx-en-kmp-trace
Obsoletes: mlnx-en-doc
Obsoletes: mlnx-en-debuginfo
Obsoletes: mlnx-en-sources
Obsoletes: mlnx-rdma-rxe
Obsoletes: fwctl-hwe <= 24.10
Provides:  fwctl-hwe = %{version}-%{release}

Summary: Infiniband Driver and ULPs kernel modules
Group: System Environment/Libraries

Requires: kernel-hwe = %{target_kernel_version_full}
Requires: kmod
Requires: libstdc++
Requires: libunwind

Requires: mlnx-tools >= 5.2.0
Requires: coreutils
Requires: pciutils
Requires: grep
Requires: procps
Requires: module-init-tools
Requires: lsof
Requires: ofed-scripts
Conflicts: mlnx-ofa_kernel-modules

%description -n %{non_kmp_pname}
Core, HW and ULPs kernel modules
Non-KMP format kernel modules rpm.
The driver sources are located at: http://www.mellanox.com/downloads/ofed/mlnx-ofa_kernel-%{MLNX_OFA_DRV_SRC}.tgz
%endif #end if "%{KMP}" == "1"

%package -n %{devel_pname}
Obsoletes: kernel-ib-devel
Obsoletes: kernel-ib
Obsoletes: mlnx-en
Obsoletes: mlnx_en
Obsoletes: mlnx-en-utils
Obsoletes: kmod-mlnx-en
Obsoletes: mlnx-en-kmp-default
Obsoletes: mlnx-en-kmp-xen
Obsoletes: mlnx-en-kmp-trace
Obsoletes: mlnx-en-doc
Obsoletes: mlnx-en-debuginfo
Obsoletes: mlnx-en-sources
Requires: coreutils
Requires: pciutils
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Summary: Infiniband Driver and ULPs kernel modules sources
Group: System Environment/Libraries
%description -n %{devel_pname}
Core, HW and ULPs kernel modules sources
The driver sources are located at: http://www.mellanox.com/downloads/ofed/

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
    %{_builddir}/%{base_name}-$VERSION/source/ofed_scripts/tools/sign-modules %{buildroot}/lib/modules/ %{kernel_source default} || exit 1 \
%{nil}

%global __debug_package 1
%global buildsubdir mlnx-ofa_kernel-%{version}
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
%debug_package
%endif

%if %{IS_RHEL_VENDOR}
%global __find_requires %{nil}
%endif

# set modules dir
%if %{IS_RHEL_VENDOR}
%if 0%{?fedora}
%global install_mod_dir updates
%else
%global install_mod_dir extra/%{_name}
%endif
%endif

%if "%{_vendor}" == "suse"
%global install_mod_dir updates
%endif

%{!?install_mod_dir: %global install_mod_dir updates}

%prep
%setup -n mlnx-ofa_kernel-%{_version}

set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
EXTRA_CFLAGS='-DVERSION=\"%version\"'
%if (0%{?rhel} >= 10)
EXTRA_CFLAGS+=' -fno-exceptions'
%endif
export EXTRA_CFLAGS
export CFLAGS="$CFLAGS  -fno-exceptions "
export INSTALL_MOD_DIR=%{install_mod_dir}
export CONF_OPTIONS="%{configure_options}"
for flavor in %flavors_to_build; do
	export KSRC=%{kernel_source $flavor}
	export KVERSION=%{kernel_release $KSRC}
	export LIB_MOD_DIR=/lib/modules/$KVERSION/$INSTALL_MOD_DIR
	rm -rf obj/$flavor
	cp -a source obj/$flavor
	cd $PWD/obj/$flavor
	find compat -type f -exec touch -t 200012201010 '{}' \; || true
	./configure --build-dummy-mods --prefix=%{_prefix} --kernel-version $KVERSION --kernel-sources $KSRC --modules-dir $LIB_MOD_DIR $CONF_OPTIONS %{?_smp_mflags}
	make %{?_smp_mflags} kernel
	cd -
done

%install
export RECORD_PY_FILES=1
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=%{install_mod_dir}
export NAME=%{_name}
export VERSION=%{version}
export PREFIX=%{_prefix}
mkdir -p %{buildroot}/%{_prefix}/src/ofa_kernel/%{_arch}
for flavor in %flavors_to_build; do
	export KSRC=%{kernel_source $flavor}
	export KVERSION=%{kernel_release $KSRC}
	cd $PWD/obj/$flavor
	make install_modules KERNELRELEASE=$KVERSION
	mkdir -p %{_builddir}/src/$NAME/$flavor
	cp -ar include/ %{_builddir}/src/$NAME/$flavor
	cp -ar config* %{_builddir}/src/$NAME/$flavor
	cp -ar compat*  %{_builddir}/src/$NAME/$flavor
	cp -ar ofed_scripts %{_builddir}/src/$NAME/$flavor

	modsyms=`find . -name Module.symvers -o -name Modules.symvers`
	if [ -n "$modsyms" ]; then
		for modsym in $modsyms
		do
			cat $modsym >> %{_builddir}/src/$NAME/$flavor/Module.symvers
		done
	else
		./ofed_scripts/create_Module.symvers.sh
		cp ./Module.symvers %{_builddir}/src/$NAME/$flavor/Module.symvers
	fi
	cp -a %{_builddir}/src/$NAME/$flavor %{buildroot}/%{_prefix}/src/ofa_kernel/%{_arch}/$KVERSION
	# Cleanup unnecessary kernel-generated module dependency files.
	find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;
	cd -
done

# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} \( -type f -name '*.ko' -o -name '*ko.gz' \) -exec %{__chmod} u+x \{\} \;

%if %{IS_RHEL_VENDOR}
%if ! 0%{?fedora}
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
for module in `find %{buildroot}/ -name '*.ko' -o -name '*.ko.gz' | sort`
do
ko_name=${module##*/}
mod_name=${ko_name/.ko*/}
mod_path=${module/*%{_name}}
mod_path=${mod_path/\/${ko_name}}
echo "override ${mod_name} * weak-updates/%{_name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/zz01-%{_name}-${mod_name}.conf
echo "override ${mod_name} * extra/%{_name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/zz01-%{_name}-${mod_name}.conf
done
%endif
%endif

# Fix path of BACKPORT_INCLUDES
sed -i -e "s@=-I.*backport_includes@=-I/usr/src/ofa_kernel-$VERSION/backport_includes@" %{buildroot}/%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION}/configure.mk.kernel || true

%clean
rm -rf %{buildroot}


%if "%{KMP}" != "1"
%post -n %{non_kmp_pname}
/sbin/depmod %{KVERSION}
# W/A for OEL6.7/7.x inbox modules get locked in memory
# in dmesg we get: Module mlx4_core locked in memory until next boot
if (grep -qiE "Oracle.*(6.([7-9]|10)| 7)" /etc/issue /etc/*release* 2>/dev/null); then
	/sbin/dracut --force
fi

%postun -n %{non_kmp_pname}
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
	/sbin/depmod %{KVERSION}
	# W/A for OEL6.7/7.x inbox modules get locked in memory
	# in dmesg we get: Module mlx4_core locked in memory until next boot
	if (grep -qiE "Oracle.*(6.([7-9]|10)| 7)" /etc/issue /etc/*release* 2>/dev/null); then
		/sbin/dracut --force
	fi
fi
%endif # end KMP=1

%post -n %{devel_pname}
if [ -d "%{_prefix}/src/ofa_kernel/default" -a $1 -gt 1 ]; then
	touch %{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION}.missing_link
	# Will run update-alternatives in posttrans
else
	update-alternatives --install \
		%{_prefix}/src/ofa_kernel/default \
		ofa_kernel_headers \
		%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION} \
		20
fi

%posttrans -n %{devel_pname}
symlink="%{_prefix}/src/ofa_kernel/default"
# Should only be used for upgrading from pre-5.5-0.2.6.0 packages:
# At the time of upgrade there was still a directory, so postpone
# generating the alternative symlink to that point:
for flag_file in %{_prefix}/src/ofa_kernel/*/*.missing_link; do
	dir=${flag_file%.missing_link}
	if [ ! -d "$dir" ]; then
		# Directory is no longer there. Nothing left to handle
		rm -f "$flag_file"
		continue
	fi
	if [ -d "$symlink" ]; then
		echo "%{devel_pname}-%{version}: $symlink is still a non-empty directory. Deleting in preparation for a symlink."
		rm -rf "$symlink"
	fi
	update-alternatives --install \
		"$symlink" \
		ofa_kernel_headers \
		"$dir" \
		20
	rm -f "$flag_file"
done

%postun -n %{devel_pname}
update-alternatives --remove \
	ofa_kernel_headers \
	%{_prefix}/src/ofa_kernel/%{_arch}/%{KVERSION} \

%if "%{KMP}" != "1"
%files -n %{non_kmp_pname}
%license source/debian/copyright
/lib/modules/%{KVERSION}/%{install_mod_dir}/
%if %{IS_RHEL_VENDOR}
%if ! 0%{?fedora}
%config(noreplace) %{_sysconfdir}/depmod.d/zz01-%{_name}-*.conf
%endif
%endif
%endif

%files -n %{devel_pname}
%defattr(-,root,root,-)
%license source/debian/copyright
%{_prefix}/src/ofa_kernel/%{_arch}/[0-9]*

%changelog
* Mon Feb 02 2026 Sean Dougherty <sdougherty@microsoft.com> - 25.07-3_6.12.57.1.3
- Bump release to match kernel-hwe

* Mon Jan 19 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07-2_6.12.57.1.2
- Bump to match kernel-hwe.

* Tue Nov 18 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07-1_6.12.57.1.1
- Upgrade version to 25.07.
- Enable build on x86_64 kernel hwe.
- Update source path

* Wed Nov 05 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 24.10-24_6.12.57.1.1
- Bump to match kernel-hwe

* Fri Oct 10 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 24.10-23_6.12.50.2-1
- Adjusted package dependencies on user space components.

* Fri Oct 06 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 24.10-22_6.12.50.2-1
- Bump to match kernel-hwe

* Fri Sep 12 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-21
- Bump to match kernel-hwe

* Mon Sep 08 2025 Elaheh Dehghani <edehghani@microsoft.com> - 24.10-20
- Build using kernel-hwe for aarch64 architecture

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 24.10-19
- Bump release to rebuild for new kernel release

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 24.10-18
- Bump release to rebuild for new kernel release

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 24.10-17
- Bump release to rebuild for new kernel release

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 24.10-16
- Bump release to rebuild for new kernel release

* Tue Apr 08 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 24.10-15
- Bump release to match "signed" spec changes.
- Removed extra 'Release' tag from the spec file.

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 24.10-14
- Bump release to rebuild for new kernel release

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 24.10-13
- Bump release to rebuild for new kernel release

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 24.10-12
- Bump release to rebuild for new kernel release

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 24.10-11
- Bump release to rebuild for new kernel release

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-10
- Bump release to rebuild for new kernel release

* Tue Mar 04 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-9
- Bump release to rebuild for new kernel release

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 24.10-8
- Bump release to rebuild for new kernel release

* Tue Feb 11 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-7
- Bump release to rebuild for new kernel release

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 24.10-6
- Bump release to rebuild for new kernel release

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 24.10-5
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 24.10-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 24.10-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-2
- Bump release to match kernel

* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 24.10-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
* Thu Jun 18 2015 Alaa Hleihel <alaa@mellanox.com>
- Renamed kernel-ib package to mlnx-ofa_kernel-modules
* Thu Apr 10 2014 Alaa Hleihel <alaa@mellanox.com>
- Add QoS utils.
* Thu Mar 13 2014 Alaa Hleihel <alaa@mellanox.com>
- Use one spec for KMP and non-KMP OS's.
* Tue Apr 24 2012 Vladimir Sokolovsky <vlad@mellanox.com>
- Remove FC support
* Tue Mar 6 2012 Vladimir Sokolovsky <vlad@mellanox.com>
- Add weak updates support
* Wed Jul 6 2011 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Add KMP support
* Mon Oct 4 2010 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Add mlx4_fc and mlx4_vnic support
* Mon May 10 2010 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Support install macro that removes RPM_BUILD_ROOT
* Thu Feb 4 2010 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added ibdev2netdev script
* Mon Sep 8 2008 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added nfsrdma support
* Wed Aug 13 2008 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added mlx4_en support
* Tue Aug 21 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added %build macro
* Sun Jan 28 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Created spec file for kernel-ib
