#
# Copyright (c) 2017 Mellanox Technologies. All rights reserved.
#
# This Software is licensed under one of the following licenses:
#
# 1) under the terms of the "Common Public License 1.0" a copy of which is
#    available from the Open Source Initiative, see
#    https://www.opensource.org/licenses/cpl.php.
#
# 2) under the terms of the "The BSD License" a copy of which is
#    available from the Open Source Initiative, see
#    https://www.opensource.org/licenses/bsd-license.php.
#
# 3) under the terms of the "GNU General Public License (GPL) Version 2" a
#    copy of which is available from the Open Source Initiative, see
#    https://www.opensource.org/licenses/gpl-license.php.
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

%global         MLNX_OFED_VERSION 5.6-1.0.3.3
%global         BF_VERSION 3.9.0

Summary:        Mellanox userland tools and scripts
Name:           mlnx-tools
Version:        5.2.0
Release:        2%{?dist}
License:        CPL 1.0 or BSD or GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Programming
URL:            https://github.com/Mellanox/mlnx-tools
Source0:        https://linux.mellanox.com/public/repo/bluefield/%{BF_VERSION}/extras/mlnx_ofed/%{MLNX_OFED_VERSION}/SOURCES/%{name}_%{version}.orig.tar.gz#/%{name}-%{version}.tar.gz
Obsoletes:      mlnx-ofa_kernel < 5.4
Obsoletes:      mlnx_en-utils < 5.4

%description
Mellanox userland tools and scripts

%define debug_package %{nil}
%define __python %{_bindir}/python3
BuildRequires: python3
# mlnx_tune is python2 but is not important enough to create a dependency
# on python2 in a python3 system:
%global __requires_exclude_from mlnx_tune

%prep
%autosetup -n %{name}-%{version}

%build

%install

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
mlnx_python_sitelib=%{python_sitelib}
if [ "$(echo %{_prefix} | sed -e 's@/@@g')" != "usr" ]; then
	mlnx_python_sitelib=$(echo %{python_sitelib} | sed -e 's@/usr@%{_prefix}@')
fi
export PKG_VERSION="%{version}"
%make_install PYTHON="%__python" PYTHON_SETUP_EXTRA_ARGS="-O1 --prefix=%{buildroot}%{_prefix} --install-lib=%{buildroot}${mlnx_python_sitelib}"

if [ "$(echo %{_prefix} | sed -e 's@/@@g')" != "usr" ]; then
	conf_env=/etc/profile.d/mlnx-tools.sh
	install -d %{buildroot}/etc/profile.d
	add_env %{buildroot}$conf_env PYTHONPATH $mlnx_python_sitelib
	add_env %{buildroot}$conf_env PATH %{_bindir}
	add_env %{buildroot}$conf_env PATH %{_sbindir}
	echo $conf_env >> mlnx-tools-files
fi
find %{buildroot}${mlnx_python_sitelib} -type f -print | sed -e 's@%{buildroot}@@' >> mlnx-tools-files

%files -f mlnx-tools-files
%doc doc/*
%license debian/copyright
%defattr(-,root,root,-)
/sbin/sysctl_perf_tuning
/sbin/mlnx_bf_configure
/sbin/mlnx_bf_configure_ct
/sbin/mlnx-sf
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man8/ib2ib_setup.8*
/lib/udev/mlnx_bf_udev

%changelog
* Fri Jul 22 2022 Rachel Menge <rachelmenge@microsoft.com> 5.2.0-2
- Initial CBL-Mariner import from NVIDIA (license: GPLv2).
- Lint spec to conform to Mariner 
- License verified

* Wed May 12 2021 Tzafrir Cohen <nvidia@cohens.org.il> - 5.2.0-1
- MLNX_OFED branch

* Wed Nov  1 2017 Vladimir Sokolovsky <vlad@mellanox.com> - 4.6.0-1
- Initial packaging
