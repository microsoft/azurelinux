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

%global target_azl_build_kernel_version %azl_kernel_version
%global target_kernel_release %azl_kernel_release
%global target_mlnx_ofa_kernel_version %azl_mlnx_ofa_kernel_version
%global target_mlnx_ofa_kernel_release %azl_mlnx_ofa_kernel_release
%global target_kernel_version_full %{target_azl_build_kernel_version}-%{target_kernel_release}%{?dist}
%global release_suffix _%{target_azl_build_kernel_version}.%{target_kernel_release}

%global KVERSION %{target_kernel_version_full}

%{!?_name: %define _name virtiofs}
%{!?_mofed_full_version: %define _mofed_full_version %{target_mlnx_ofa_kernel_version}-%{target_mlnx_ofa_kernel_release}%{?dist}}

Summary:	 %{_name} Driver
Name:		 virtiofs-signed
Version:	 2607.0.100
Release:	 1%{release_suffix}%{?dist}
License:	 GPLv2
Url:		 http://www.mellanox.com
Group:		 System Environment/Base

#
# To populate these sources:
#   1. Build the unsigned packages as normal
#   2. Sign the desired binary
#   3. Place the unsigned package and signed binary in this spec's folder
#   4. Build this spec

Source0:	 %{_name}-%{version}-%{release}.%{_arch}.rpm
Source1:         virtiofs.ko

Vendor:          Microsoft Corporation
Distribution:    Azure Linux
ExclusiveArch:   x86_64

%description
virtiofs signed kernel modules

%package -n %{_name}
Summary:        %{summary}
Requires:       mlnx-ofa_kernel = %{_mofed_full_version}
Requires:       mlnx-ofa_kernel-modules  = %{_mofed_full_version}
Requires:       kernel = %{target_kernel_version_full}
Requires:       kmod

%description -n %{_name}
%{description}

%prep
mkdir rpm_contents
pushd rpm_contents

rpm2cpio %{SOURCE0} | cpio -idmv
set -- "%{SOURCE1}"
for module; do basename "$module"; done | sort > ../signed-modules
find ./lib/modules/%{KVERSION}/updates -type f -name '*.ko' \
    -exec basename {} \; | sort > ../unsigned-modules
if ! cmp ../signed-modules ../unsigned-modules; then
    echo "Signed sources do not match the unsigned module inventory" >&2
    exit 1
fi
for module; do
    target=$(find ./lib/modules/%{KVERSION}/updates -type f -name "$(basename "$module")")
    cp -f "$module" "$target"
done
popd

%build

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
%config(noreplace) %{_sysconfdir}/depmod.d/zz02-%{_name}-*.conf

%changelog
* Sat Nov 14 2026 Azure Linux Team - 2607.0.100-1
- Upgrade to DOCA 3.5.0 (OFED 26.07-0.7.7.0)
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified

