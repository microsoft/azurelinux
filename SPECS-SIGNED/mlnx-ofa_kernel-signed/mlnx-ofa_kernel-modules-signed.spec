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

%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

%global KVERSION %{target_kernel_version_full}
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

# KMP is disabled by default
%{!?KMP: %global KMP 0}

%global WITH_SYSTEMD %(if ( test -d "%{_unitdir}" > /dev/null); then echo -n '1'; else echo -n '0'; fi)

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

# Kernel module packages to be included into kernel-ib
%global build_ipoib %(if ( echo %{configure_options} | grep "with-ipoib-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%global build_oiscsi %(if ( echo %{configure_options} | grep "with-iscsi-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)
%global build_mlx5 %(if ( echo %{configure_options} | grep "with-mlx5-mod" > /dev/null ); then echo -n '1'; else echo -n '0'; fi)

%{!?LIB_MOD_DIR: %global LIB_MOD_DIR /lib/modules/%{KVERSION}/updates}

%{!?IB_CONF_DIR: %global IB_CONF_DIR /etc/infiniband}

%{!?KERNEL_SOURCES: %global KERNEL_SOURCES /lib/modules/%{KVERSION}/source}

%{!?_name: %global _name mlnx-ofa_kernel}
%{!?_version: %global _version 24.10}
%{!?_release: %global _release OFED.24.10.0.7.0.1}
%global _kmp_rel %{_release}%{?_kmp_build_num}%{?_dist}

%global utils_pname %{_name}
%global devel_pname %{_name}-devel
%global non_kmp_pname %{_name}-modules

# mlnx-ofa_kernel-modules is a sub-package in SPECS/mlnx-ofa_kernel.
# We are making that into a main package for signing.

Summary:	 Infiniband HCA Driver
Name:		 %{_name}-modules
Version:	 %{_version}
Release:	 1_%{_release}%{?_dist}
License:	 GPLv2
Url:		 http://www.mellanox.com/
Group:		 System Environment/Base

# This package's "version" and "release" must reflect the unsigned version that
# was signed.
# An important consequence is that when making a change to this package, the
# unsigned version/release must be increased to keep the two versions consistent.
# Ideally though, this spec will not change much or at all, so the version will
# just track the unsigned package's version/release.
#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:        mlx_compat.ko
Source2:        ib_cm.ko
Source3:        ib_core.ko
Source4:        ib_ucm.ko
Source5:        ib_umad.ko
Source6:        ib_uverbs.ko
Source7:        iw_cm.ko
Source8:        rdma_cm.ko
Source9:        rdma_ucm.ko
Source10:       bnxt_re.ko
Source11:       efa.ko
Source12:       mlx4_ib.ko
Source13:       mlx5_ib.ko
Source14:       rdma_rxe.ko
Source15:       ib_ipoib.ko
Source16:       ib_iser.ko
Source17:       ib_isert.ko
Source18:       ib_srp.ko
Source19:       mlx5_core.ko
Source10:       mlxfw.ko
Source11:       mlxsw_spectrum.ko
Source12:       nvme-rdma.ko
Source13:       nvmet-rdma.ko
Source14:       mlxdevm.ko
Source15:       smc.ko
Source16:       smc_diag.ko
Source17:       rpcrdma.ko
Source18:       svcrdma.ko
Source19:       xprtrdma.ko

BuildRoot:	 /var/tmp/%{name}-%{version}-build
Vendor:		 Microsoft Corporation
Distribution:	 Azure Linux

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

BuildRequires:  kernel-devel = %{target_kernel_version_full}
BuildRequires:  kernel-headers = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  kmod
BuildRequires:  libstdc++-devel
BuildRequires:  libunwind-devel
BuildRequires:  pkgconfig

Requires: kernel = %{target_kernel_version_full}
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


%if "%{KMP}" == "1"
BuildRequires: %kernel_module_package_buildreqs
BuildRequires: /usr/bin/perl
%endif

%description 
Mellanox infiniband kernel modules.
The driver sources are located at: http://www.mellanox.com/downloads/

%prep

%build
rpm2cpio %{Source0} | cpio -idmv -D %{buildroot}

%install
cp %{Source1} %{buildroot}/lib/modules/%{KVERSION}/updates/compat/mlx_compat.ko
cp %{Source2} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_cm.ko
cp %{Source3} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_core.ko
cp %{Source4} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_ucm.ko
cp %{Source5} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_umad.ko
cp %{Source6} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_uverbs.ko
cp %{Source7} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/core/iw_cm.ko
cp %{Source8} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/core/rdma_cm.ko
cp %{Source9} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/core/rdma_ucm.ko
cp %{Source10} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/bnxt_re/bnxt_re.ko
cp %{Source11} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/efa/efa.ko
cp %{Source12} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/mlx4/mlx4_ib.ko
cp %{Source13} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/mlx5/mlx5_ib.ko
cp %{Source14} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/sw/rxe/rdma_rxe.ko
cp %{Source15} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/ipoib/ib_ipoib.ko
cp %{Source16} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/iser/ib_iser.ko
cp %{Source17} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/isert/ib_isert.ko
cp %{Source18} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/srp/ib_srp.ko
cp %{Source19} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/net/ethernet/mellanox/mlx5/core/mlx5_core.ko
cp %{Source10} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/net/ethernet/mellanox/mlxfw/mlxfw.ko
cp %{Source11} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/net/ethernet/mellanox/mlxsw/mlxsw_spectrum.ko
cp %{Source12} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/nvme/host/nvme-rdma.ko
cp %{Source13} %{buildroot}/lib/modules/%{KVERSION}/updates/drivers/nvme/target/nvmet-rdma.ko
cp %{Source14} %{buildroot}/lib/modules/%{KVERSION}/updates/net/mlxdevm/mlxdevm.ko
cp %{Source15} %{buildroot}/lib/modules/%{KVERSION}/updates/net/smc/smc.ko
cp %{Source16} %{buildroot}/lib/modules/%{KVERSION}/updates/net/smc/smc_diag.ko
cp %{Source17} %{buildroot}/lib/modules/%{KVERSION}/updates/net/sunrpc/xprtrdma/rpcrdma.ko
cp %{Source18} %{buildroot}/lib/modules/%{KVERSION}/updates/net/sunrpc/xprtrdma/svcrdma.ko
cp %{Source19} %{buildroot}/lib/modules/%{KVERSION}/updates/net/sunrpc/xprtrdma/xprtrdma.ko

%clean
rm -rf %{buildroot}

%post
/sbin/depmod %{KVERSION}

%postun
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
	/sbin/depmod %{KVERSION}
fi

%files
/lib/modules/%{KVERSION}/%{install_mod_dir}/
%endif

%changelog
* Tue Dec  16 2024 Binu Jose Philip <bphilip@microsoft.com> - 24.10
- Creating signed spec
