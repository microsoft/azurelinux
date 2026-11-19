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
#  $Id: ofed-scripts.spec 8402 2006-07-06 06:35:57Z vlad $
#

%global debug_package %{nil}

Summary: OFED scripts
%global upstream_name ofed-scripts

Name: ofed-scripts
Version: 26.04
Release: %autorelease
# The upstream spec and file headers grant a choice of these three licenses;
# their bsd-license.php reference resolves to BSD-2-Clause. Upstream ships no
# separate license text file.
License: CPL-1.0 OR BSD-2-Clause OR GPL-2.0-only
Url: http://www.openfabrics.org
Group: System Environment/Base
# AZL: NVIDIA's MLNX_OFED source bundle (origin URL and hash are pinned in
# ofed-scripts.comp.toml); %%prep extracts the nested ofed-scripts SRPM.
Source6000: MLNX_OFED_SRC-26.04-0.8.5.0.tgz
BuildArch: noarch
BuildRequires: cpio
# AZL: ofed_info locates rpm with which(1).
Requires: which

%description
OpenFabrics scripts: ofed_info and ofed_rpm_info report the MLNX OFED
bundle version and component list, and sysinfo-snapshot.py collects
system and network diagnostics.

%prep
tar -xf %{SOURCE6000}
_ofed_scripts_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/ofed-scripts-%{version}-*.src.rpm' -print -quit)
if [ -z "$_ofed_scripts_srpm" ]; then
        echo "ERROR: ofed-scripts source RPM not found inside %{SOURCE6000}" >&2
        exit 1
fi
rpm2cpio "$_ofed_scripts_srpm" | cpio -idm './ofed-scripts-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf ofed-scripts-%{version}.tar.gz
%setup -q -T -D -n %{upstream_name}-%{version}

%build

%install
# AZL: install only the reporting and diagnostics tools. The vendor
# ofed_uninstall.sh force-removes (rpm -e --nodeps) every package matching
# rdma/ofed/infiniband/..., including distro packages, and its
# vendor_pre/post_uninstall.sh hooks only serve NVIDIA's installer; Azure
# Linux packages are removed with dnf. The vendor's non-/usr prefix
# (profile.d and ld.so.conf.d) handling is dropped since %%{_prefix} is /usr.
install -d %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
install -m 0755 sysinfo-snapshot.py %{buildroot}%{_sbindir}
install -m 0755 ofed_info %{buildroot}%{_bindir}
install -m 0755 ofed_rpm_info %{buildroot}%{_bindir}

%files
%{_bindir}/ofed_info
%{_bindir}/ofed_rpm_info
%{_sbindir}/sysinfo-snapshot.py

%changelog
%autochangelog
