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

%global debug_package %{nil}
# The default %%__os_install_post macro ends up stripping the signatures off of the kernel module.
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}

%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

%global KVERSION %{target_kernel_version_full}

%{!?_name: %global _name mlnx-ofa_kernel}

# mlnx-ofa_kernel-modules is a sub-package in SPECS/mlnx-ofa_kernel.
# We are making that into a main package for signing.

Summary:	 Infiniband HCA Driver
Name:		 %{_name}-modules
Version:	 24.10
Release:	 14%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com/
Group:		 System Environment/Base

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
Source20:       mlxfw.ko
Source21:       mlxsw_spectrum.ko
Source22:       nvme-rdma.ko
Source23:       nvmet-rdma.ko
Source24:       mlxdevm.ko
Source25:       smc.ko
Source26:       smc_diag.ko
Source27:       rpcrdma.ko
Source28:       svcrdma.ko
Source29:       xprtrdma.ko

Vendor:          Microsoft Corporation
Distribution:    Azure Linux
ExclusiveArch:   x86_64

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


%description 
Mellanox infiniband kernel modules.
The driver sources are located at: http://www.mellanox.com/downloads/

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed modules
rpm2cpio %{SOURCE0} | cpio -idmv

cp -rf %{SOURCE1} ./lib/modules/%{KVERSION}/updates/compat/mlx_compat.ko
cp -rf %{SOURCE2} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_cm.ko
cp -rf %{SOURCE3} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_core.ko
cp -rf %{SOURCE4} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_ucm.ko
cp -rf %{SOURCE5} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_umad.ko
cp -rf %{SOURCE6} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/core/ib_uverbs.ko
cp -rf %{SOURCE7} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/core/iw_cm.ko
cp -rf %{SOURCE8} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/core/rdma_cm.ko
cp -rf %{SOURCE9} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/core/rdma_ucm.ko
cp -rf %{SOURCE10} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/bnxt_re/bnxt_re.ko
cp -rf %{SOURCE11} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/efa/efa.ko
cp -rf %{SOURCE12} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/mlx4/mlx4_ib.ko
cp -rf %{SOURCE13} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/mlx5/mlx5_ib.ko
cp -rf %{SOURCE14} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/sw/rxe/rdma_rxe.ko
cp -rf %{SOURCE15} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/ipoib/ib_ipoib.ko
cp -rf %{SOURCE16} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/iser/ib_iser.ko
cp -rf %{SOURCE17} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/isert/ib_isert.ko
cp -rf %{SOURCE18} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/srp/ib_srp.ko
cp -rf %{SOURCE19} ./lib/modules/%{KVERSION}/updates/drivers/net/ethernet/mellanox/mlx5/core/mlx5_core.ko
cp -rf %{SOURCE20} ./lib/modules/%{KVERSION}/updates/drivers/net/ethernet/mellanox/mlxfw/mlxfw.ko
cp -rf %{SOURCE21} ./lib/modules/%{KVERSION}/updates/drivers/net/ethernet/mellanox/mlxsw/mlxsw_spectrum.ko
cp -rf %{SOURCE22} ./lib/modules/%{KVERSION}/updates/drivers/nvme/host/nvme-rdma.ko
cp -rf %{SOURCE23} ./lib/modules/%{KVERSION}/updates/drivers/nvme/target/nvmet-rdma.ko
cp -rf %{SOURCE24} ./lib/modules/%{KVERSION}/updates/net/mlxdevm/mlxdevm.ko
cp -rf %{SOURCE25} ./lib/modules/%{KVERSION}/updates/net/smc/smc.ko
cp -rf %{SOURCE26} ./lib/modules/%{KVERSION}/updates/net/smc/smc_diag.ko
cp -rf %{SOURCE27} ./lib/modules/%{KVERSION}/updates/net/sunrpc/xprtrdma/rpcrdma.ko
cp -rf %{SOURCE28} ./lib/modules/%{KVERSION}/updates/net/sunrpc/xprtrdma/svcrdma.ko
cp -rf %{SOURCE29} ./lib/modules/%{KVERSION}/updates/net/sunrpc/xprtrdma/xprtrdma.ko

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd


%post
/sbin/depmod %{KVERSION}

%postun
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
	/sbin/depmod %{KVERSION}
fi

%files
/lib/modules/%{KVERSION}/updates/
%license %{_datadir}/licenses/%{name}/copyright

%changelog
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

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-2
- Bump release to match kernel

* Sat Jan 18 2025 Binu Jose Philip <bphilip@microsoft.com> - 24.10-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
