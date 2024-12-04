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
# Source tgz from https://github.com/Mellanox/mlnx-tools/archive/refs/tags/v<version>.tar.gz
#

%global         MLNX_OFED_VERSION 24.10.0.7.0.1
%global         BF_VERSION 3.9.0

Summary:        Mellanox userland tools and scripts
Name:           mlnx-tools
Version:        24.10.0
Release:        1%{?dist}
License:        BSD or GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Programming
URL:            https://github.com/Mellanox/mlnx-tools
Source0:        https://github.com/Mellanox/mlnx-tools/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Obsoletes:      mlnx-ofa_kernel < 5.4
Obsoletes:      mlnx_en-utils < 5.4

%description
Mellanox userland tools and scripts

BuildRequires: python3

%define debug_package %{nil}

# mlnx_tune is python2 but is not important enough to create a dependency
# on python2 in a python3 system:
%global __requires_exclude_from mlnx_tune

# This is always true for AZURELINUX
%global PYTHON3 1
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

# These are delivered by mlnx-ofa_kernel, mlnx-tools should stay away
rm -f %{buildroot}/lib/udev/{sf-rep-netdev-rename,vf-net-link-name.sh}

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
/sbin/mlnx_bf_configure_ct
/sbin/mlnx-sf
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/*.8*
%{python_dir}/dcbnetlink.py*
%{python_dir}/netlink.py*
%if %(ls %{python_dir}/__pycache__/*.pyc 2> /dev/null | wc -l)
%exclude %{python_dir}/__pycache__/*.pyc
%endif
/etc/modprobe.d/mlnx-bf.conf
/lib/udev/auxdev-sf-netdev-rename
/lib/udev/mlnx_bf_assign_ct_cores.sh
/lib/udev/mlnx_bf_udev
/lib/udev/rules.d/82-net-setup-link.rules
/lib/udev/rules.d/83-mlnx-sf-name.rules

%changelog
* Tue Nov 26 2024 Binu Jose Philip <bphilip@microsoft.com>
- Upgrade to 24.10.0
- Pickup source tarball from blobstore

* Fri Jul 22 2022 Rachel Menge <rachelmenge@microsoft.com> 5.2.0-2
- Initial CBL-Mariner import from NVIDIA (license: GPLv2).
- Lint spec to conform to Mariner 
- License verified

* Wed May 12 2021 Tzafrir Cohen <nvidia@cohens.org.il> - 5.2.0-1
- MLNX_OFED branch

* Wed Nov  1 2017 Vladimir Sokolovsky <vlad@mellanox.com> - 4.6.0-1
- Initial packaging
