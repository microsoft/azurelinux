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

%global target_kernel_version_full %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}-%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_azurelinux_build_kernel_version %(/bin/rpm -q --queryformat '%{RPMTAG_VERSION}' $(/bin/rpm -q --whatprovides kernel-headers))
%global target_kernel_release %(/bin/rpm -q --queryformat '%{RPMTAG_RELEASE}' $(/bin/rpm -q --whatprovides kernel-headers) | /bin/cut -d . -f 1)

%global KVERSION %{target_kernel_version_full}
%global K_SRC /lib/modules/%{target_kernel_version_full}/build

%{!?_name: %define _name isert}
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
# %{!?K_SRC: %global K_SRC /lib/modules/%{KVERSION}/build}

# define release version
%{!?src_release: %global src_release %{_release}_%{krelver}}
%if "%{KMP}" != "1"
%global _release1 %{src_release}
%else
%global _release1 %{_release}
%endif
%global _kmp_rel %{_release1}%{?_kmp_build_num}%{?_dist}

Summary:	 %{_name} Driver
Name:		 %{_name}
Version:	 %{_version}
Release:	 1_%{_release1}%{?_dist}
License:	 GPLv2
Url:		 http://www.mellanox.com
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

Source0:	 %{name}-%{version}-%{release}.%{_arch}.rpm
Source1:         ib_isert.ko

BuildRoot:	 /var/tmp/%{name}-%{version}-build
Vendor:		 Microsoft Corporation
Distribution:	 Azure Linux

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kernel-devel = %{target_kernel_version_full}
BuildRequires:  kernel-headers = %{target_kernel_version_full}
BuildRequires:  binutils
BuildRequires:  systemd
BuildRequires:  kmod
BuildRequires:  mlnx-ofa_kernel-devel = %{_version}
BuildRequires:  mlnx-ofa_kernel-source = %{_version}

Requires:       mlnx-ofa_kernel = %{_version}
Requires:       mlnx-ofa_kernel-modules  = %{_version}
Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description
isert signed kernel modules

%prep

%build
rpm2cpio %{Source0} | cpio -idmv -D %{buildroot}

%install
cp %{Source1} %{buildroot}/lib/modules/%{KVERSION}/updates/isert/ib_isert.ko

%clean
rm -rf %{buildroot}

%post
if [ $1 -ge 1 ]; then # 1 : This package is being installed or reinstalled
  /sbin/depmod %{KVERSION}
fi # 1 : closed
# END of post

%postun
/sbin/depmod %{KVERSION}

%if "%{KMP}" != "1"
%files
%defattr(-,root,root,-)
/lib/modules/%{KVERSION}/%{install_mod_dir}/
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-%{name}-*.conf
%endif

%changelog
* Tue Dec  16 2024 Binu Jose Philip <bphilip@microsoft.com> - 24.10.0.6.7.1
- Creating signed spec
