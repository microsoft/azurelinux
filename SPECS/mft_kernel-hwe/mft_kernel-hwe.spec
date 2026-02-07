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

%{!?version: %global version 4.33.0}
%{!?_release: %global _release 3}
%global _kmp_rel %{_release}%{?_kmp_build_num}%{?_dist}

Name:		 mft_kernel-hwe
Summary:	 %{name} Kernel Module for the %{KVERSION} kernel
Version:	 4.33.0
Release:	 3%{release_suffix}%{?dist}
License:	 Dual BSD/GPLv2
Group:		 System Environment/Kernel
BuildRoot:	 /var/tmp/%{name}-%{version}-build
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:         %{_distro_sources_url}/kernel-mft-%{version}.tgz
Vendor:          Microsoft Corporation
Distribution:    Azure Linux

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-hwe-devel = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod

Requires:       kernel-hwe = %{target_kernel_version_full}
Requires:       kmod
Conflicts:      mft_kernel
Conflicts:      kernel-mft

# Azure Linux attempts to match the spec file name and the "Name" tag.
# Upstream's mft_kernel spec set rpm name as kernel-mft. To comply, we
# set "Name" as mft_kernel but add a "Provides" for kernel-mft.
Provides:       kernel-hwe-mft = %{version}-%{release}

%description
This package provides a %{name} kernel module for kernel.

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
%license source/COPYING
/lib/modules/%{KVERSION}/%{install_mod_dir}/
%if %{IS_RHEL_VENDOR}
%if ! 0%{?fedora}
%config(noreplace) %{_sysconfdir}/depmod.d/kernel-mft-*.conf
%endif
%endif
%endif

%changelog
* Mon Feb 02 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.33.0-3_6.12.57.1.3
- Bump to match kernel-hwe.

* Mon Jan 19 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.33.0-2_6.12.57.1.2
- Bump to match kernel-hwe.

* Tue Nov 18 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 4.33.0-1_6.12.57.1.1
- Upgrade version to 4.33.0.
- Enable build on x86_64 kernel hwe.
- Update source path

* Wed Nov 05 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 4.30.0-24_6.12.57.1.1
- Bump to match kernel-hwe

* Fri Oct 10 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.30.0-23_6.12.50.2-1
- Adjusted package dependencies on user space components.

* Fri Oct 06 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 4.30.0-22_6.12.50.2-1
- Bump to match kernel-hwe

* Fri Sep 12 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-21
- Bump to match kernel-hwe

* Mon Sep 08 2025 Elaheh Dehghani <edehghani@microsoft.com> - 4.30.0-20
- Build using kernel-hwe for aarch64 architecture

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.30.0-19
- Bump release to rebuild for new kernel release

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 4.30.0-18
- Bump release to rebuild for new kernel release

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 4.30.0-17
- Bump release to rebuild for new kernel release

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 4.30.0-16
- Bump release to rebuild for new kernel release

* Tue Apr 08 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.30.0-15
- Removing duplicate description.

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.30.0-14
- Bump release to rebuild for new kernel release

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.30.0-13
- Bump release to rebuild for new kernel release

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.30.0-12
- Bump release to rebuild for new kernel release

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 4.30.0-11
- Bump release to rebuild for new kernel release

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-10
- Bump release to rebuild for new kernel release

* Tue Mar 04 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-9
- Bump release to rebuild for new kernel release

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 4.30.0-8
- Bump release to rebuild for new kernel release

* Tue Feb 11 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-7
- Bump release to rebuild for new kernel release

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 4.30.0-6
- Bump release to rebuild for new kernel release

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 4.30.0-5
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 4.30.0-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 4.30.0-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 4.30.0-2
- Bump release to match kernel

* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 4.30.0-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
