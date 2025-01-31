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

%if 0%{azl}
%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{VERSION}-%{RELEASE}' kernel-headers)
%else
%global target_kernel_version_full f.a.k.e
%endif

%global KVERSION %{target_kernel_version_full}

Summary:	 srp driver
Name:		 srp
Version:	 24.10
Release:	 3%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com
Group:		 System Environment/Base

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:         %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:         ib_srp.ko
Source2:         scsi_transport_srp.ko

Vendor:          Microsoft Corporation
Distribution:    Azure Linux
ExclusiveArch:   x86_64

Requires:       mlnx-ofa_kernel = %{version}
Requires:       mlnx-ofa_kernel-modules  = %{version}
Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description
srp kernel modules

%prep

%build

%install
rpm2cpio %{SOURCE0} | cpio -idmv -D %{buildroot}

cp -r %{SOURCE1} %{buildroot}/lib/modules/%{KVERSION}/updates/srp/ib_srp.ko
cp -r %{SOURCE2} %{buildroot}/lib/modules/%{KVERSION}/updates/srp/scsi/scsi_transport_srp.ko

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/lib/modules/%{KVERSION}/updates/srp/ib_srp.ko
/lib/modules/%{KVERSION}/updates/srp/scsi/scsi_transport_srp.ko
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-%{name}-*.conf
%license %{_datadir}/licenses/%{name}/copyright

%changelog
* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-3
- Bump release to match kernel

* Thu Jan 30 2025 Rachel Menge <rachelmenge@microsoft.com> - 24.10-2
- Bump release to match kernel

* Sat Jan 18 2024 Binu Jose Philip <bphilip@microsoft.com> - 24.10-1
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
