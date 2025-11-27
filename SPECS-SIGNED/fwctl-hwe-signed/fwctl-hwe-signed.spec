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

%global debug_package %{nil}
# The default %%__os_install_post macro ends up stripping the signatures off of the kernel module.
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}

# hard code versions due to ADO bug:58993948
%global target_azl_build_kernel_version 6.12.57.1
%global target_kernel_release 1
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}

%global KVERSION %{target_kernel_version_full}

%{!?_name: %define _name fwctl-hwe}
%{!?_mofed_full_version: %define _mofed_full_version 24.10-24%{release_suffix}%{?dist}}

Summary:	 %{_name} Driver
Name:		 %{_name}-signed
Version:	 24.10
Release:	 24%{release_suffix}%{?dist}
License:	 GPLv2
Url:		 http://nvidia.com
Group:		 System Environment/Base

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:        %{_name}-%{version}-%{release}.%{_arch}.rpm
Source1:        fwctl.ko
Source2:        mlx5_fwctl.ko

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
ExclusiveArch:  aarch64

%description
fwctl signed kernel modules

%package -n %{_name}
Summary:        %{summary}
Requires:       mlnx-ofa_kernel
Requires:       mlnx-ofa_kernel-hwe-modules  = %{_mofed_full_version}
Requires:       kernel-hwe = %{target_kernel_version_full}
Requires:       kmod
Conflicts:	    fwctl

%description -n %{_name}
%{description}

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed modules
rpm2cpio %{SOURCE0} | cpio -idmv

cp -rf %{SOURCE1} ./lib/modules/%{KVERSION}/updates/%{_name}/fwctl.ko
cp -rf %{SOURCE2} ./lib/modules/%{KVERSION}/updates/%{_name}/mlx5/mlx5_fwctl.ko

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%post -n %{_name}
if [ $1 -ge 1 ]; then # 1 : This package is being installed or reinstalled
  /sbin/depmod %{KVERSION}
fi # 1 : closed
# END of post

%postun -n %{_name}
/sbin/depmod %{KVERSION}

%files -n %{_name}
%defattr(-,root,root,-)
%license %{_datadir}/licenses/%{_name}/copyright
/lib/modules/%{KVERSION}/updates/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-fwctl-*.conf

%changelog
* Wed Nov 05 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 24.10-24_6.12.57.1.1
- Bump to match kernel-hwe

* Fri Oct 10 2025 Pawel Winogrodzki <pawelwi@microsoft.com> - 24.10-23_6.12.50.2-1
- Adjusted package dependencies on user space components.

* Fri Oct 06 2025 Siddharth Chintamaneni <sidchintamaneni@gmail.com> - 24.10-22_6.12.50.2-1
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

* Fri Jan 31 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 24.10-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-2
- Bump release to match kernel

* Sat Jan 18 2025 Binu Jose Philip <bphilip@microsoft.com> - 24.10-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
