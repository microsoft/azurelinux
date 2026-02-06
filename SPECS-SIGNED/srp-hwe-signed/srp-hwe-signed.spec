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

%global debug_package %{nil}
# The default %%__os_install_post macro ends up stripping the signatures off of the kernel module.
%define __os_install_post %{__os_install_post_leave_signatures} %{nil}

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

%define _name srp-hwe
%{!?_mofed_full_version: %define _mofed_full_version %{target_mlnx_ofa_kernel_version}-%{target_mlnx_ofa_kernel_release}%{?dist}}

Summary:	 srp driver
Name:		 %{_name}-signed
Version:	 25.07
Release:	 3%{release_suffix}%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com
Group:		 System Environment/Base

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:         %{_name}-%{version}-%{release}.%{_arch}.rpm
Source1:         ib_srp.ko
Source2:         scsi_transport_srp.ko

Vendor:          Microsoft Corporation
Distribution:    Azure Linux

%description
srp kernel modules

%package -n %{_name}
Summary:        %{summary}
Requires:       mlnx-ofa_kernel
Requires:       mlnx-ofa_kernel-hwe-modules = %{_mofed_full_version}
Requires:       kernel-hwe = %{target_kernel_version_full}
Requires:       kmod
Conflicts:      srp

%description -n %{_name}
%{description}

%prep

%build
mkdir rpm_contents
pushd rpm_contents

# This spec's whole purpose is to inject the signed modules
rpm2cpio %{SOURCE0} | cpio -idmv

cp -rf %{SOURCE1} ./lib/modules/%{KVERSION}/updates/%{_name}/ib_srp.ko
cp -rf %{SOURCE2} ./lib/modules/%{KVERSION}/updates/%{_name}/scsi/scsi_transport_srp.ko

popd

%install
pushd rpm_contents

# Don't use * wildcard. It does not copy over hidden files in the root folder...
cp -rp ./. %{buildroot}/

popd

%files -n %{_name}
%defattr(-,root,root,-)
/lib/modules/%{KVERSION}/updates/%{_name}/ib_srp.ko
/lib/modules/%{KVERSION}/updates/%{_name}/scsi/scsi_transport_srp.ko
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-srp-*.conf
%license %{_datadir}/licenses/%{_name}/copyright

%changelog
* Mon Feb 02 2026 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 25.07-3_6.12.57.1.2
- Tweak specs to use dynamic versioning for kernel and MOFED

* Mon Jan 19 2026 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07-2_6.12.57.1.2
- Bump to match kernel-hwe.

* Tue Nov 18 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 25.07-1_6.12.57.1.1
- Upgrade version to 25.07.
- Enable build on x86_64 kernel hwe.

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

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-2
- Bump release to match kernel

* Sat Jan 18 2025 Binu Jose Philip <bphilip@microsoft.com> - 24.10-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
