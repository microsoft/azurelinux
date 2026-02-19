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


%global target_azl_build_kernel_version %azl_kernel_hwe_version
%global target_kernel_release %azl_kernel_hwe_release
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}

%global KVERSION %{target_kernel_version_full}

%{!?_name: %global _name mlnx-ofa_kernel-hwe-modules}

# mlnx-ofa_kernel-modules is a sub-package in SPECS/mlnx-ofa_kernel.
# We are making that into a main package for signing.

Summary:	 Infiniband HCA Driver
Name:		 %{_name}-signed
Version:	 25.07
Release:	 5%{release_suffix}%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com/
Group:		 System Environment/Base

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{_name}-%{version}-%{release}.%{_arch}.rpm
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
Source30:       fwctl.ko
Source31:       mlx5_fwctl.ko
Source32:       mana_ib.ko
Source33:       mlx5_dpll.ko
%ifarch aarch64
Source34:       rnbd-client.ko
Source35:       rnbd-server.ko
Source36:       iw_cxgb4.ko
Source37:       erdma.ko
Source38:       ib_mthca.ko
Source39:       ocrdma.ko
Source40:       qedr.ko
Source41:       siw.ko
Source42:       rtrs-client.ko
Source43:       rtrs-core.ko
Source44:       rtrs-server.ko
Source45:       ib_srpt.ko
Source46:       mlx5-vfio-pci.ko
Source47:       9pnet_rdma.ko
Source48:       rds_rdma.ko
%endif

Vendor:          Microsoft Corporation
Distribution:    Azure Linux


%description 
Mellanox infiniband kernel modules.
The driver sources are located at: http://www.mellanox.com/downloads/

%package -n %{_name}
Summary:        %{summary}

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
Obsoletes: fwctl-hwe <= 24.10
Provides:  fwctl-hwe = %{version}-%{release}

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

%description -n %{_name}
%{description}

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
cp -rf %{SOURCE30} ./lib/modules/%{KVERSION}/updates/drivers/fwctl/fwctl.ko
cp -rf %{SOURCE31} ./lib/modules/%{KVERSION}/updates/drivers/fwctl/mlx5/mlx5_fwctl.ko
cp -rf %{SOURCE32} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/mana/mana_ib.ko
cp -rf %{SOURCE33} ./lib/modules/%{KVERSION}/updates/drivers/net/ethernet/mellanox/mlx5/core/mlx5_dpll.ko
%ifarch aarch64
cp -rf %{SOURCE34} ./lib/modules/%{KVERSION}/updates/drivers/block/rnbd/rnbd-client.ko
cp -rf %{SOURCE35} ./lib/modules/%{KVERSION}/updates/drivers/block/rnbd/rnbd-server.ko
cp -rf %{SOURCE36} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/cxgb4/iw_cxgb4.ko
cp -rf %{SOURCE37} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/erdma/erdma.ko
cp -rf %{SOURCE38} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/mthca/ib_mthca.ko
cp -rf %{SOURCE39} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/ocrdma/ocrdma.ko
cp -rf %{SOURCE40} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/hw/qedr/qedr.ko
cp -rf %{SOURCE41} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/sw/siw/siw.ko
cp -rf %{SOURCE42} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/rtrs/rtrs-client.ko
cp -rf %{SOURCE43} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/rtrs/rtrs-core.ko
cp -rf %{SOURCE44} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/rtrs/rtrs-server.ko
cp -rf %{SOURCE45} ./lib/modules/%{KVERSION}/updates/drivers/infiniband/ulp/srpt/ib_srpt.ko
cp -rf %{SOURCE46} ./lib/modules/%{KVERSION}/updates/drivers/vfio/pci/mlx5/mlx5-vfio-pci.ko
cp -rf %{SOURCE47} ./lib/modules/%{KVERSION}/updates/net/9p/9pnet_rdma.ko
cp -rf %{SOURCE48} ./lib/modules/%{KVERSION}/updates/net/rds/rds_rdma.ko
%endif

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd


%post -n %{_name}
/sbin/depmod %{KVERSION}

%postun -n %{_name}
if [ $1 = 0 ]; then  # 1 : Erase, not upgrade
	/sbin/depmod %{KVERSION}
fi

%files -n %{_name}
/lib/modules/%{KVERSION}/updates/
%license %{_datadir}/licenses/%{_name}/copyright

%changelog
* Tue Feb 10 2026 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 25.07-5_6.12.57.1.2
- Tweak specs to use dynamic versioning for kernel

* Fri Feb 06 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07-4_6.12.57.1.4
- Bump to match kernel-hwe.

* Mon Feb 02 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07-3_6.12.57.1.3
- Bump to match kernel-hwe.

* Mon Jan 19 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07-2_6.12.57.1.2
- Bump to match kernel-hwe.

* Tue Nov 18 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07-1_6.12.57.1.1
- Upgrade version to 25.07.
- Enable build on x86_64 kernel hwe.
- Update additional kernel modules fwctl mana and mlx5_dpll included from 25.07

* Wed Nov 05 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 24.10-24_6.12.57.1.1
- Bump to match kernel-hwe

* Fri Oct 10 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 24.10-23_6.12.50.2-1
- Bump release to rebuild for new release

* Fri Oct 06 2025 Siddharth Chintamaneni <siddharthc@microsoft.com> - 24.10-22_6.12.50.2-1
- Bump to match kernel-hwe
- Fix signed spec for -hwe variant

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
- Re-naming the package to de-duplicate the SRPM name.

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
