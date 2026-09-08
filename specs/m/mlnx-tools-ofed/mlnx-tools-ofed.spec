# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Copyright (c) 2017 Mellanox Technologies. All rights reserved.
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

Summary: Mellanox userland tools and scripts
# AZL: this package ships only scripts; disable auto debuginfo generation.
%global debug_package %{nil}
%global upstream_name mlnx-tools

Name: mlnx-tools-ofed
Version: 2604.0.13
Release: 1
Conflicts: mlnx-tools
License: GPLv2 or BSD
Url: https://github.com/Mellanox/mlnx-tools
Group: Applications/System
Source6000: MLNX_OFED_SRC-26.04-0.8.5.0.tgz
BuildRoot: %{?build_root:%{build_root}}%{!?build_root:/var/tmp/%{name}}
Vendor: Mellanox Technologies
Obsoletes: mlnx-ofa_kernel < 5.4, mlnx_en-utils < 5.4
# AZL: missing from upstream spec; required by make install.
BuildRequires: make
BuildRequires: gcc-c++
%description
Mellanox userland tools and scripts

%global python_dir %{_datadir}/%{upstream_name}/python
%if "%{rhel}" == "7"
%global PYTHON2 1
%else
%global PYTHON2 0
 %define _ver 2604.0.13 
 %define _rel 1 
%endif

%prep
tar -xf %{SOURCE6000}
_mlnx_tools_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/mlnx-tools-%{version}-*.src.rpm' -print -quit)
if [ -z "$_mlnx_tools_srpm" ]; then
	echo "ERROR: mlnx-tools source RPM not found inside %{SOURCE6000}" >&2
	exit 1
fi
rpm2cpio "$_mlnx_tools_srpm" | cpio -idm './mlnx-tools-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf mlnx-tools-%{version}.tar.gz
%setup -T -D -n %{upstream_name}-%{version}
%if %{PYTHON2}
sed -i -e '1s/python3/python/' \
	python/ib2ib_setup python/mlnx_dump_parser python/mlnx_perf \
	python/mlnx_qos python/mlnx_tune python/mlx_fs_dump python/tc_wrap.py \
	python/Python/dcbnetlink.py
%endif

%install
rm -rf %{buildroot}

add_env()
{
	efile=$1
	evar=$2
	epath=$3

cat >> $efile << EOF
if ! echo \$${evar} | grep -q $epath ; then
	export $evar=$epath:\$$evar
fi

EOF
}

touch mlnx-tools-files
export PKG_VERSION="%{version}"
%make_install

%if "%{_prefix}" != "/usr"
	conf_env=/etc/profile.d/mlnx-tools.sh
	install -d %{buildroot}/etc/profile.d
	add_env %{buildroot}$conf_env PATH %{_bindir}
	add_env %{buildroot}$conf_env PATH %{_sbindir}
	echo $conf_env >> mlnx-tools-files
%endif
install -d %{buildroot}/etc/mellanox/hugepages.d

%clean
rm -rf %{buildroot}

%if "%{_prefix}" != "/usr"
%files -f mlnx-tools-files
%else
%files
%endif
%license LICENSE
%doc doc/*
%defattr(-,root,root,-)
/sbin/sysctl_perf_tuning
/sbin/mlnx_bf_configure
/sbin/mlnx-sf
/sbin/doca-hugepages
# AZL: %{_sbindir} does not resolve to /usr/sbin in this build environment.
/usr/sbin/*
%{_bindir}/*
%{_mandir}/man8/*.8*
%{python_dir}/dcbnetlink.py*
%{python_dir}/netlink.py*
/lib/udev/mlnx_bf_udev
/etc/mellanox/hugepages.d

%changelog
* Tue Apr  28 2026 root - 2604.0.13-1
Automated build 1

* Wed May 12 2021 Tzafrir Cohen <nvidia@cohens.org.il> - 5.2.0-1
- MLNX_OFED branch
* Wed Nov  1 2017 Vladimir Sokolovsky <vlad@mellanox.com> - 4.6.0-1
- Initial packaging
