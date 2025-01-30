#
# Copyright (c) 2024 Nvidia Inc. All rights reserved.
#
# This software is available to you under a choice of one of two
# licenses.  You may choose to be licensed under the terms of the GNU
# General Public License (GPL) Version 2, available from the file
# COPYING in the main directory of this source tree, or the
# OpenIB.org BSD license below:
#
#     Redistribution and use in source and binary forms, with or
#     without modification, are permitted provided that the following
#     conditions are met:
#
#      - Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      - Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials
#        provided with the distribution.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

%global KVERSION %{target_kernel_version_full}

%{!?_name: %define _name fwctl}

Summary:	 %{_name} Driver
Name:		 %{_name}
Version:	 24.10
Release:	 2%{?dist}
License:	 GPLv2
Url:		 http://nvidia.com
Group:		 System Environment/Base

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:        fwctl.ko
Source2:        mlx5_fwctl.ko

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
ExclusiveArch:  x86_64

Requires:       mlnx-ofa_kernel = %{version}
Requires:       mlnx-ofa_kernel-modules  = %{version}
Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description
fwctl signed kernel modules

%prep

%build

%install
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

cp -r %{SOURCE1} %{buildroot}/lib/modules/%{KVERSION}/updates/fwctl/fwctl.ko
cp -r %{SOURCE2} %{buildroot}/lib/modules/%{KVERSION}/updates/fwctl/mlx5/mlx5_fwctl.ko

%clean
rm -rf %{buildroot}

%post
if [ $1 -ge 1 ]; then # 1 : This package is being installed or reinstalled
  /sbin/depmod %{KVERSION}
fi # 1 : closed
# END of post

%postun
/sbin/depmod %{KVERSION}

%files
%defattr(-,root,root,-)
%license %{_datadir}/licenses/%{name}/copyright
/lib/modules/%{KVERSION}/updates/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-%{name}-*.conf


%changelog
* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-2
- Bump release to match kernel

* Sat Jan 18 2024 Binu Jose Philip <bphilip@microsoft.com> - 24.10-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
