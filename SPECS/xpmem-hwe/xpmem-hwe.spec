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

%{!?_mofed_full_version: %define _mofed_full_version 25.07-3%{release_suffix}%{?dist}}

# %{!?KVERSION: %global KVERSION %(uname -r)}
%{!?KVERSION: %global KVERSION %{target_kernel_version_full}}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}
# A separate variable _release is required because of the odd way the
# script append_number_to_package_release.sh works:
%global _release 1.2507097

%bcond_without kernel_only

%if %{with kernel_only}
%undefine _debugsource_packages
%global debug_package %{nil}
%global make_kernel_only SUBDIRS=kernel
%else
%global make_kernel_only %{nil}
%endif

%define need_firmware_dir 0%{?euleros} > 0

%if "%_vendor" == "openEuler"
%global __find_requires %{nil}
%endif

Summary:	 Cross-partition memory
Name:		 xpmem-hwe
Version:	 2.7.4
Release:	 27%{release_suffix}%{?dist}
License:	 GPLv2 and LGPLv2.1
Group:		 System Environment/Libraries
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
BuildRequires:	 automake autoconf
URL:		 https://github.com/openucx/xpmem
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:         %{_distro_sources_url}/xpmem-%{version}.tar.gz

# name gets a different value in subpackages
%global kernel_suffix hwe
%global _kmp_rel %{release}%{?_kmp_build_num}%{?_dist}
# Required for e.g. SLES12:
%if %{undefined make_build}
%global make_build %{__make} %{?_smp_mflags}
%endif

# Ugly workaround until anolis kmod package stops requiring
# 'kernel(' dependencies its kernel package does not provide.
# This uses the __find_provides from /usr/lib/rpm/redhat/macros
# rather than the one from /usr/lib/rpm/macros.d/macros.kmp
%if 0%{?anolis} > 0
%{?filter_setup}
%endif

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-hwe-devel = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod
BuildRequires:  mlnx-ofa_kernel-hwe-devel = %{_mofed_full_version}

%description
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package includes helper tools for the kernel module.

# build KMP rpms?
%if "%{KMP}" == "1"
%global kernel_release() $(make -C %{1} M=$PWD kernelrelease | grep -v make)
BuildRequires: %kernel_module_package_buildreqs
%(cat > %{_builddir}/preamble << EOF
EOF)
%{kernel_module_package -r %{_kmp_rel} -p %{_builddir}/preamble}
%else # not KMP
%global kernel_source() %{K_SRC}
%global kernel_release() %{KVERSION}
%global flavors_to_build default

%package modules
# %{nil}: to avoid having the script that build OFED-internal
# munge the release version here as well:
Summary: XPMEM: kernel modules
Group: System Environment/Libraries

Requires:       mlnx-ofa_kernel
Requires:       mlnx-ofa_kernel-hwe-modules = %{_mofed_full_version}
Requires:       kernel-hwe = %{target_kernel_version_full}
Requires:       kmod
Conflicts:      xpmem-modules

%description modules
XPMEM is a Linux kernel module that enables a process to map the
memory of another process into its virtual address space. Source code
can be obtained by cloning the Git repository, original Mercurial
repository or by downloading a tarball from the link above.

This package includes the kernel module (non KMP version).
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
    $RPM_BUILD_DIR/xpmem-%{version}/tools/sign-modules $RPM_BUILD_ROOT/lib/modules/ %{kernel_source default} || exit 1 \
%{nil}

# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}} \
  %{__arch_install_post} \
  %{__os_install_post} \
  %{__modsign_install_post} \
%{nil}

%endif # end of setup module sign scripts
#

%if 0%{?rhel} > 0 || 0%{?euleros} >= 2
%global install_mod_dir extra/%{name}
%endif

%{!?install_mod_dir: %global install_mod_dir updates}

%global moduledir /lib/modules/%{KVERSION}/%{install_mod_dir}

%prep
%setup -q -n xpmem-%{version}

%build
env=
if [ "$CROSS_COMPILE" != '' ]; then
  env="$env CC=${CROSS_COMPILE}gcc"
fi
./autogen.sh
%{configure} \
  --with-module-prefix= \
  --with-kerneldir=%{K_SRC} \
  $env \
  #
%{make_build} %{make_kernel_only}

%install
%{make_install} moduledir=%{moduledir} %{make_kernel_only}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/libxpmem.la
rm -rf $RPM_BUILD_ROOT/etc/init.d/xpmem
%if %{with kernel_only}
rm -rf $RPM_BUILD_ROOT/lib/udev/rules.d
rm -f $RPM_BUILD_ROOT/usr/lib*/pkgconfig/cray-xpmem.pc
%else
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modules-load.d
echo "xpmem" >$RPM_BUILD_ROOT%{_prefix}/lib/modules-load.d/xpmem.conf
%endif
%if %{need_firmware_dir}
mkdir -p $RPM_BUILD_ROOT/lib/firmware
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if "%{KMP}" != "1"
%post modules
depmod %{KVERSION}

%postun modules
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
	/sbin/depmod %{KVERSION}
fi

%files modules
%{moduledir}/xpmem.ko
%license COPYING COPYING.LESSER
%endif

%changelog
* Mon Feb 02 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.7.4-27_6.12.57.1.3
- Bump to match kernel-hwe.

* Mon Jan 19 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.7.4-26_6.12.57.1.2
- Bump to match kernel-hwe.

* Tue Nov 04 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.7.4-25_6.12.57.1.1
- Build with OFED 25.07.0.9.7.1.
- Enable build on x86_64 kernel hwe.
- Update source path

* Wed Nov 05 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 2.7.4-24_6.12.57.1.1
- Bump to match kernel-hwe

* Fri Oct 10 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.4-23_6.12.50.2-1
- Adjusted package dependencies on user space components.
- Align %%post* scripts with other kmod packages.

* Fri Oct 03 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 2.7.4-22_6.12.50.2-1
- Bump to match kernel-hwe

* Fri Sep 12 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-21
- Bump to match kernel-hwe

* Mon Sep 08 2025 Elaheh Dehghani <edehghani@microsoft.com> - 2.7.4-20
- Build using kernel-hwe for aarch64 architecture

* Fri May 23 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.4-19
- Bump release to rebuild for new kernel release

* Tue May 13 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 2.7.4-18
- Bump release to rebuild for new kernel release

* Tue Apr 29 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 2.7.4-17
- Bump release to rebuild for new kernel release

* Fri Apr 25 2025 Chris Co <chrco@microsoft.com> - 2.7.4-16
- Bump release to rebuild for new kernel release

* Wed Apr 09 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.4-15
- Removed extra 'Release' tag from the spec file

* Sat Apr 05 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.4-14
- Bump release to rebuild for new kernel release

* Fri Mar 14 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.4-13
- Bump release to rebuild for new kernel release

* Tue Mar 11 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.7.4-12
- Bump release to rebuild for new kernel release

* Mon Mar 10 2025 Chris Co <chrco@microsoft.com> - 2.7.4-11
- Bump release to rebuild for new kernel release

* Wed Mar 05 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-10
- Bump release to rebuild for new kernel release

* Tue Mar 04 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-9
- Bump release to rebuild for new kernel release

* Wed Feb 19 2025 Chris Co <chrco@microsoft.com> - 2.7.4-8
- Bump release to rebuild for new kernel release

* Tue Feb 11 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-7
- Bump release to rebuild for new kernel release

* Wed Feb 05 2025 Tobias Brick <tobiasb@microsoft.com> - 2.7.4-6
- Bump release to rebuild for new kernel release

* Tue Feb 04 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-5
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 2.7.4-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 2.7.4-2
- Bump release to match kernel

* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 2.7.4-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
