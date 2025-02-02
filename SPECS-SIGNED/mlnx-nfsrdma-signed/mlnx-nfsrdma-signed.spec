#
# Copyright (c) 2016 Mellanox Technologies. All rights reserved.
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

%define mlnx_version 24.10

%{!?_name: %define _name mlnx-nfsrdma}

Summary:	 %{_name} Driver
Name:		 %{_name}
Version:	 24.10
Release:	 4%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com
Group:		 System Environment/Base

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:        rpcrdma.ko
Source2:        svcrdma.ko
Source3:        xprtrdma.ko

Vendor:          Microsoft Corporation
Distribution:    Azure Linux
ExclusiveArch:   x86_64

Requires:       mlnx-ofa_kernel = %{mlnx_version}
Requires:       mlnx-ofa_kernel-modules  = %{mlnx_version}
Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description
mellanox rdma signed kernel modules

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed modules
rpm2cpio %{SOURCE0} | cpio -idmv
cp -rf %{SOURCE1} ./lib/modules/%{KVERSION}/updates/mlnx-nfsrdma/rpcrdma.ko
cp -rf %{SOURCE2} ./lib/modules/%{KVERSION}/updates/mlnx-nfsrdma/svcrdma.ko
cp -rf %{SOURCE3} ./lib/modules/%{KVERSION}/updates/mlnx-nfsrdma/xprtrdma.ko

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd


%post
if [ $1 -ge 1 ]; then # This package is being installed or reinstalled
  /sbin/depmod %{KVERSION}
fi
# END of post

%postun
/sbin/depmod %{KVERSION}

%files
%defattr(-,root,root,-)
%license %{_datadir}/licenses/%{name}/copyright
/lib/modules/%{KVERSION}/updates/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-%{name}-*.conf

%changelog
* Fri Jan 31 2025 Alberto David Perez Guevara <aperez@microsoft.com> - 24.10-4
- Bump release to rebuild for new kernel release

* Fri Jan 31 2025 Alberto David Perez Guevara <aperez@microsoft.com> - 24.10-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-2
- Bump release to match kernel

* Sat Jan 18 2024 Binu Jose Philip <bphilip@microsoft.com> - 24.10-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
