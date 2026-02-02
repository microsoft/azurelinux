#
# Copyright (c) 2014 Mellanox Technologies. All rights reserved.
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

%global target_azl_build_kernel_version %azl_kernel_hwe_version
%global target_kernel_release %azl_kernel_hwe_release
%global target_mlnx_ofa_kernel_version %azl_mlnx_ofa_kernel_hwe_version
%global target_mlnx_ofa_kernel_release %azl_mlnx_ofa_kernel_hwe_release
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}
%else
%global target_kernel_version_full f.a.k.e
%endif

%global KVERSION %{target_kernel_version_full}
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

%{!?_name: %define _name srp-hwe}
%{!?_mofed_full_version: %define _mofed_full_version %{target_mlnx_ofa_kernel_version}-%{target_mlnx_ofa_kernel_release}%{?dist}}
%{!?_release: %define _release OFED.25.07.0.9.7.1}

# KMP is disabled by default
%{!?KMP: %global KMP 0}

# take kernel version or default to uname -r
# %{!?KVERSION: %global KVERSION %(uname -r)}
%{!?KVERSION: %global KVERSION %{target_kernel_version_full}}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
# take path to kernel sources if provided, otherwise look in default location (for non KMP rpms).
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}

# define release version
%{!?src_release: %global src_release %{_release}_%{krelver}}
%if "%{KMP}" != "1"
%global _release1 %{src_release}
%else
%global _release1 %{_release}
%endif
%global _kmp_rel %{_release1}%{?_kmp_build_num}%{?_dist}

Summary:	 srp driver
Name:		 srp-hwe
Version:	 25.07
Release:	 3%{release_suffix}%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com
Group:		 System Environment/Base
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:         %{_distro_sources_url}/srp-%{version}.tgz
BuildRoot:	 /var/tmp/%{name}-%{version}-build
Vendor:          Microsoft Corporation
Distribution:    Azure Linux

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-hwe-devel = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod
BuildRequires:  libconfig-devel
BuildRequires:  mlnx-ofa_kernel-hwe-devel = %{_mofed_full_version}

Requires:       mlnx-ofa_kernel
Requires:       mlnx-ofa_kernel-hwe-modules  = %{_mofed_full_version}
Requires:       kernel-hwe = %{target_kernel_version_full}
Requires:       kmod
Conflicts:      srp

%description
%{name} kernel modules

# build KMP rpms?
%if "%{KMP}" == "1"
%global kernel_release() $(make -s -C %{1} kernelrelease M=$PWD)
BuildRequires: %kernel_module_package_buildreqs
%(mkdir -p %{buildroot})
%(echo '%defattr (-,root,root)' > %{buildroot}/file_list)
%(echo '/lib/modules/%2-%1' >> %{buildroot}/file_list)
%(echo '%config(noreplace) %{_sysconfdir}/depmod.d/zz02-%{_name}-*-%1.conf' >> %{buildroot}/file_list)
%{kernel_module_package -f %{buildroot}/file_list -x xen -r %{_kmp_rel} }
%else
%global kernel_source() %{K_SRC}
%global kernel_release() %{KVERSION}
%global flavors_to_build default
%endif

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
    %{_builddir}/srp-%{version}/source/tools/sign-modules %{buildroot}/lib/modules/  %{kernel_source default} || exit 1 \
%{nil}

%global __debug_package 1
%global buildsubdir srp-%{version}
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

%if 0%{?anolis} == 8
%global __find_requires %{nil}
%endif

# set modules dir
%if "%{_vendor}" == "redhat" || ("%{_vendor}" == "openEuler")
%if 0%{?fedora}
%global install_mod_dir updates/%{name}
%else
%global install_mod_dir extra/%{name}
%endif
%endif

%if "%{_vendor}" == "suse"
%global install_mod_dir updates/%{name}
%endif

%{!?install_mod_dir: %global install_mod_dir updates/%{name}}

%prep
%setup -n srp-%{target_mlnx_ofa_kernel_version}
set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
export EXTRA_CFLAGS='-DVERSION=\"%version\"'
export INSTALL_MOD_DIR=%{install_mod_dir}
export CONF_OPTIONS="%{configure_options}"
for flavor in %{flavors_to_build}; do
	export K_BUILD=%{kernel_source $flavor}
	export KVER=%{kernel_release $K_BUILD}
	export LIB_MOD_DIR=/lib/modules/$KVER/$INSTALL_MOD_DIR
	rm -rf obj/$flavor
	cp -r source obj/$flavor
	cd $PWD/obj/$flavor
	make
	cd -
done

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=%{install_mod_dir}
export PREFIX=%{_prefix}
for flavor in %flavors_to_build; do
	export K_BUILD=%{kernel_source $flavor}
	export KVER=%{kernel_release $K_BUILD}
	cd $PWD/obj/$flavor
	make install KERNELRELEASE=$KVER
	# Cleanup unnecessary kernel-generated module dependency files.
	find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;
	cd -
done

# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} \( -type f -name '*.ko' -o -name '*ko.gz' \) -exec %{__chmod} u+x \{\} \;

%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
for module in `find %{buildroot}/ -name '*.ko' -o -name '*.ko.gz' | sort`
do
ko_name=${module##*/}
mod_name=${ko_name/.ko*/}
mod_path=${module/*\/%{name}}
mod_path=${mod_path/\/${ko_name}}
%if "%{_vendor}" == "suse"
    for flavor in %{flavors_to_build}; do
        if [[ $module =~ $flavor ]] || [ "X%{KMP}" != "X1" ];then
            echo "override ${mod_name} * updates/%{name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/zz02-%{_name}-${mod_name}-$flavor.conf
        fi
    done
%else
    %if 0%{?fedora}
        echo "override ${mod_name} * updates/%{name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/zz02-%{_name}-${mod_name}.conf
    %else
        %if "%{_vendor}" == "redhat" || ("%{_vendor}" == "openEuler")
            echo "override ${mod_name} * weak-updates/%{name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/zz02-%{_name}-${mod_name}.conf
        %endif
        echo "override ${mod_name} * extra/%{name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/zz02-%{_name}-${mod_name}.conf
    %endif
%endif
done


%clean
rm -rf %{buildroot}

%post
if [ $1 -ge 1 ]; then # 1 : This package is being installed or reinstalled
  /sbin/depmod %{KVERSION}
fi # 1 : closed
# add SRP_LOAD=no to  openib.conf
if [ -f "/etc/infiniband/openib.conf" ] && ! (grep -q SRP_LOAD /etc/infiniband/openib.conf > /dev/null 2>&1) ; then
    echo "# Load SRP module" >> /etc/infiniband/openib.conf
    echo "SRP_LOAD=no" >> /etc/infiniband/openib.conf
fi
# END of post

%postun
/sbin/depmod %{KVERSION}

%if "%{KMP}" != "1"
%files
%defattr(-,root,root,-)
%license source/debian/copyright
/lib/modules/%{KVERSION}/%{install_mod_dir}/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-%{_name}-*.conf
%endif

%changelog
* Mon Feb 02 2026 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 25.07-3_6.12.57.1.2
- Tweak specs to use dynamic versioning for kernel and MOFED

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

* Thu Jan 9 2025 Binu Jose Philip <bphilip@microsoft.com> - 24.10-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified

* Thu Feb 20 2014 Alaa Hleihel <alaa@mellanox.com>
- Initial packaging
