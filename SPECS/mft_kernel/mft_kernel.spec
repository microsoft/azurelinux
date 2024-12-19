
%if 0%{azl}
%global target_kernel_version_full f.a.k.e
%else
%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{VERSION}-%{RELEASE}' kernel-headers)
%endif

%global KVERSION %{target_kernel_version_full}
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

# KMP is disabled by default
%{!?KMP: %global KMP 0}

# take cpu arch from uname -m
%global _cpu_arch %(uname -m)
%global docdir /etc/mft
%global mlxfwreset_ko_path %{docdir}/mlxfwreset/


# take kernel version or default to uname -r
# %{!?KVERSION: %global KVERSION %(uname -r)}
%{!?KVERSION: %global KVERSION %{target_kernel_version_full}}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
# take path to kernel sources if provided, otherwise look in default location (for non KMP rpms).
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}

%if "%{KMP}" == "1"
%global _name kernel-mft-mlnx
%else
%global _name kernel-mft
%endif

%{!?version: %global version 4.30.0}
%{!?_release: %global _release 1}
%global _kmp_rel %{_release}%{?_kmp_build_num}%{?_dist}

Name:		 kernel-mft
Summary:	 %{name} Kernel Module for the %{KVERSION} kernel
Version:	 %{version}
Release:	 1%{?dist}
License:	 Dual BSD/GPL
Group:		 System Environment/Kernel
BuildRoot:	 /var/tmp/%{name}-%{version}-build
Source0:         https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/kernel-mft-4.30.0.tgz#/kernel-mft-%{version}.tgz
Vendor:          Microsoft Corporation
Distribution:	 Azure Linux

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
mft kernel module(s)

%global debug_package %{nil}

%global IS_RHEL_VENDOR "%{_vendor}" == "redhat" || "%{_vendor}" == "bclinux" || "%{_vendor}" == "openEuler"

# build KMP rpms?
%if "%{KMP}" == "1"
%global kernel_release() $(make -C %{1} M=$PWD kernelrelease | grep -v make | tail -1)
BuildRequires: %kernel_module_package_buildreqs
# prep file list for kmp rpm
%(cat > %{_builddir}/kmp.files << EOF
%defattr(644,root,root,755)
/lib/modules/%2-%1
%if %{IS_RHEL_VENDOR}
%config(noreplace) %{_sysconfdir}/depmod.d/kernel-mft-*.conf
%endif
EOF)
%{kernel_module_package -f %{_builddir}/kmp.files -r %{_kmp_rel} }
%else
%global kernel_source() %{K_SRC}
%global kernel_release() %{KVERSION}
%global flavors_to_build default
%endif

%description
This package provides a %{name} kernel module for kernel.

%if "%{KMP}" == "1"
%package utils
Summary: KO utils for MFT
Group: System Environment/Kernel
Vendor: Microsoft Corporation
%description utils
mft utils kernel module(s)
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
    $RPM_BUILD_DIR/kernel-mft-%{version}/source/tools/sign-modules $RPM_BUILD_ROOT/lib/modules/ %{kernel_source default} || exit 1 \
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

%if %{IS_RHEL_VENDOR}
%global __find_requires %{nil}
%endif

# set modules dir
%if %{IS_RHEL_VENDOR}
%if 0%{?fedora}
%global install_mod_dir updates
%else
%global install_mod_dir extra/%{name}
%endif
%endif

%if "%{_vendor}" == "suse"
%global install_mod_dir updates
%endif

%{!?install_mod_dir: %global install_mod_dir updates}

%prep
%setup -n kernel-mft-%{version}
set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
rm -rf $RPM_BUILD_ROOT
export EXTRA_CFLAGS='-DVERSION=\"%version\"'
for flavor in %{flavors_to_build}; do
	rm -rf obj/$flavor
	cp -a source obj/$flavor
	cd $PWD/obj/$flavor
	export KSRC=%{kernel_source $flavor}
	export KVERSION=%{kernel_release $KSRC}
	make KPVER=$KVERSION
	cd -
done

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=%{install_mod_dir}
mkdir -p %{install_mod_dir}
for flavor in %{flavors_to_build}; do
	export KSRC=%{kernel_source $flavor}
	export KVERSION=%{kernel_release $KSRC}
	install -d $INSTALL_MOD_PATH/lib/modules/$KVERSION/%{install_mod_dir}
	cp $PWD/obj/$flavor/mst_backward_compatibility/mst_pci/mst_pci.ko $INSTALL_MOD_PATH/lib/modules/$KVERSION/%{install_mod_dir}
	cp $PWD/obj/$flavor/mst_backward_compatibility/mst_pciconf/mst_pciconf.ko $INSTALL_MOD_PATH/lib/modules/$KVERSION/%{install_mod_dir}
    %if "%{_cpu_arch}" == "ppc64" || "%{_cpu_arch}" == "ppc64le"
        install -d $INSTALL_MOD_PATH/%{mlxfwreset_ko_path}/$KVERSION
        install $PWD/obj/$flavor/mst_backward_compatibility/mst_ppc/mst_ppc_pci_reset.ko $INSTALL_MOD_PATH/%{mlxfwreset_ko_path}/$KVERSION/
    %endif
    %if "%{_cpu_arch}" == "aarch64"
        cp $PWD/obj/$flavor/misc_drivers/bf3_livefish/bf3_livefish.ko $INSTALL_MOD_PATH/lib/modules/$KVERSION/%{install_mod_dir}
    %endif
done

%if %{IS_RHEL_VENDOR}
# Set the module(s) to be executable, so that they will be stripped when packaged.
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;

%if ! 0%{?fedora}
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
for module in `find %{buildroot}/ -name '*.ko*' | grep -v "%{mlxfwreset_ko_path}" | sort`
do
ko_name=${module##*/}
mod_name=${ko_name/.ko*/}
mod_path=${module/*%{name}}
mod_path=${mod_path/\/${ko_name}}
echo "override ${mod_name} * weak-updates/%{name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/%{name}-${mod_name}.conf
echo "override ${mod_name} * extra/%{name}${mod_path}" >> %{buildroot}%{_sysconfdir}/depmod.d/%{name}-${mod_name}.conf
done
%endif
%else
find %{buildroot} -type f -name \*.ko -exec %{__strip} -p --strip-debug --discard-locals -R .comment -R .note \{\} \;
%endif

%post
/sbin/depmod %{KVERSION}

%postun
/sbin/depmod %{KVERSION}

%if "%{KMP}" != "1"
%files
%defattr(-,root,root,-)
/lib/modules/%{KVERSION}/%{install_mod_dir}/
%if %{IS_RHEL_VENDOR}
%if ! 0%{?fedora}
%config(noreplace) %{_sysconfdir}/depmod.d/kernel-mft-*.conf
%endif
%endif
%endif
%if "%{_cpu_arch}" == "ppc64" || "%{_cpu_arch}" == "ppc64le"
%if "%{KMP}" == "1"
%files utils
%defattr(-,root,root,-)
%endif
%{docdir}
%endif

%changelog
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
- Moving to core from azlinux-ai-ml repo
- Initial Azure Linux import from NVIDIA (license: GPL)
- License verified
* Thu Nov 07 2024 Suresh Babu Chalamalasetty <schalam@microsoft.com>
- Initial version Azure Linux
