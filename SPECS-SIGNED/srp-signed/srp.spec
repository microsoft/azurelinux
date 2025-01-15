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
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

%{!?_name: %define _name srp}
%{!?_version: %define _version 24.10}
%{!?_release: %define _release OFED.24.10.0.6.7.1}

# KMP is disabled by default
%{!?KMP: %global KMP 0}

# take kernel version or default to uname -r
# %{!?KVERSION: %global KVERSION %(uname -r)}
%{!?KVERSION: %global KVERSION %{target_kernel_version_full}}
%global kernel_version %{KVERSION}
%global krelver %(echo -n %{KVERSION} | sed -e 's/-/_/g')
# take path to kernel sources if provided, otherwise look in default location (for non KMP rpms).
%{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}

# define release version
%{!?src_release: %global src_release %{_release}_%{krelver}}
%if "%{KMP}" != "1"
%global _release1 %{src_release}
%else
%global _release1 %{_release}
%endif
%global _kmp_rel %{_release1}%{?_kmp_build_num}%{?_dist}

Summary:	 srp driver
Name:		 srp
Version:	 %{_version}
Release:	 1%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com
Group:		 System Environment/Base
Source0:         %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:         ib_srp.ko
Source2:         scsi_transport_srp.ko

BuildRoot:	 /var/tmp/%{name}-%{version}-build
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
ExclusiveArch:   x86_64

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel = %{target_kernel_version_full}
BuildRequires:  kernel-headers = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod
BuildRequires:  libconfig-devel
BuildRequires:  mlnx-ofa_kernel-devel = %{_version}
BuildRequires:  mlnx-ofa_kernel-source = %{_version}

Requires:       mlnx-ofa_kernel = %{_version}
Requires:       mlnx-ofa_kernel-modules  = %{_version}
Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description
srp kernel modules

%prep

%build
rpm2cpio %{Source0} | cpio -idmv -D %{buildroot}

%install
cp %{Source1} %{buildroot}/lib/modules/%{KVERSION}/updates/srp/ib_srp.ko
cp %{Source2} %{buildroot}/lib/modules/%{KVERSION}/updates/srp/scsi/scsi_transport_srp.ko

%clean
rm -rf %{buildroot}

%if "%{KMP}" != "1"
%files modules
/lib/modules/%{KVERSION}/updates/srp/ib_srp.ko
/lib/modules/%{KVERSION}/updates/srp/scsi/scsi_transport_srp.ko
%endif

%changelog
* Thu Jan 9 2024 Binu Jose Philip <bphilip@microsoft.com>
- Creating signed spec
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
