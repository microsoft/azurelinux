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

%global         MLNX_OFED_VERSION 24.10-0.7.0.0

Summary:        Mellanox userland tools and scripts
Name:           mlnx-tools
Version:        24.10
Release:        1%{?dist}
License:        GPLv2 or BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://github.com/Mellanox/mlnx-tools
Source0:        https://linux.mellanox.com/public/repo/mlnx_ofed/%{MLNX_OFED_VERSION}/SRPMS/%{name}-%{version}.tar.gz
Obsoletes:      mlnx-ofa_kernel < 5.4
Obsoletes:      mlnx_en-utils < 5.4

BuildRoot: %{?build_root:%{build_root}}%{!?build_root:/var/tmp/%{name}}

%description
Mellanox userland tools and scripts

%global RHEL8 0%{?rhel} >= 8
%global FEDORA3X 0%{?fedora} >= 30
%global SLES15 0%{?suse_version} >= 1500
%global OPENEULER 0%{?openEuler} >= 2
%global PYTHON3 %{RHEL8} || %{FEDORA3X} || %{SLES15} || %{OPENEULER}
%global python_dir %{_datadir}/%{name}/python

%prep
%setup -n %{name}-%{version}

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
%if %PYTHON3
sed -i -e '1s/python\>/python3/' %{buildroot}/usr/{s,}bin/* \
	%{buildroot}%{python_dir}/*.py
%endif

%if "%{_prefix}" != "/usr"
	conf_env=/etc/profile.d/mlnx-tools.sh
	install -d %{buildroot}/etc/profile.d
	add_env %{buildroot}$conf_env PATH %{_bindir}
	add_env %{buildroot}$conf_env PATH %{_sbindir}
	echo $conf_env >> mlnx-tools-files
%endif

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
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*.8*
%{python_dir}/dcbnetlink.py*
%{python_dir}/netlink.py*
%exclude %{python_dir}/__pycache__/*.pyc
/lib/udev/mlnx_bf_udev

%changelog
* Thu Jan 09 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> 24.10-1
- Upgrade package to version 24.10

* Fri Jul 22 2022 Rachel Menge <rachelmenge@microsoft.com> 5.2.0-2
- Initial CBL-Mariner import from NVIDIA (license: GPLv2).
- Lint spec to conform to Mariner 
- License verified

* Wed May 12 2021 Tzafrir Cohen <nvidia@cohens.org.il> - 5.2.0-1
- MLNX_OFED branch

* Wed Nov 01 2017 Vladimir Sokolovsky <vlad@mellanox.com> - 4.6.0-1
- Initial packaging
