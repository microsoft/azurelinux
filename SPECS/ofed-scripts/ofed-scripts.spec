#
# Copyright (c) 2012 Mellanox Technologies. All rights reserved.
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
#  $Id: ofed-scripts.spec 8402 2006-07-06 06:35:57Z vlad $
#

Summary:        OFED scripts
Name:           ofed-scripts
# Update long_release with the OFED version along with version updates
Version:        5.6
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://www.openfabrics.org
Source0:        https://linux.mellanox.com/public/repo/doca/1.3.0/extras/mlnx_ofed/5.6-1.0.3.3/SOURCES/ofed-scripts_5.6.orig.tar.gz#/%{name}-%{version}.tar.gz

%global debug_package %{nil}
%global long_release OFED.5.6.1.0.3

%description
OpenFabrics scripts from NVIDA %long_release

%prep
%autosetup -p1 -n %{name}-%{version}

%build

%install

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -m 0755 uninstall.sh %{buildroot}%{_sbindir}/ofed_uninstall.sh
install -m 0755 sysinfo-snapshot.py %{buildroot}%{_sbindir}
install -m 0755 vendor_pre_uninstall.sh %{buildroot}%{_sbindir}
install -m 0755 vendor_post_uninstall.sh %{buildroot}%{_sbindir}
install -m 0755 ofed_info %{buildroot}%{_bindir}
install -m 0755 ofed_rpm_info %{buildroot}%{_bindir}
# Mariner not yet supported upstream
# install -m 0755 hca_self_test.ofed %{buildroot}%{_bindir}

%post
if [ $1 -ge 1 ]; then #This package is being installed or reinstalled
	if [ -e /etc/yum.conf ]; then
		list="ibutils-libs"
		lista=`echo ${list} | sed -e "s/ /* /g" -e "s/$/*/"`

		if [ -n "$list" ]; then
			if ( grep -q "^exclude=" /etc/yum.conf ); then
				new_list=
				for pkg in $list
				do
					if (grep "^exclude=" /etc/yum.conf | grep -wq "$pkg"); then
						continue
					else
						new_list="$new_list ${pkg}*"
					fi
				done
				perl -ni -e "s@^(exclude=.*)@\$1 $new_list@;print" /etc/yum.conf
			else
				perl -i -ne "if (m@^\[main\]@) {
					print q@[main]
exclude=$lista
@;
				} else {
					print;
				}" /etc/yum.conf
			fi
		fi
	fi
fi

/sbin/ldconfig

%postun
if [ $1 = 0 ]; then  #Erase, not upgrade
	if [ -e /etc/yum.conf ]; then
		list="ibutils-libs"

		if [ -n "$list" ]; then
			if ( grep -q "^exclude=" /etc/yum.conf ); then
				for pkg in $list
				do
					if (grep "^exclude=" /etc/yum.conf | grep -wq "$pkg"); then
						sed -i -e "s/\<$pkg\>\*//" /etc/yum.conf
						sed -i -e "s/\<$pkg\>//" /etc/yum.conf
					fi
				done
			fi
		fi
		perl -ni -e "print unless /^exclude=\s+$/" /etc/yum.conf
		sed -i -e "s/^exclude= \{1,\}/exclude=/" -e "s/ \{1,\}$//" /etc/yum.conf
	fi
fi
/sbin/ldconfig

%files
%defattr(-,root,root)
%license debian/copyright
%{_bindir}/*
%{_sbindir}/*

%changelog
* Fri Jul 22 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.6-1
- Initial CBL-Mariner import from NVIDIA (license: GPLv2)
- License verified

* Sun Jan 08 2017 Alaa Hleihel <alaa@mellanox.com>
- Added hca_self_test.ofed script

* Sun Dec 13 2015 Nizar Swidan <nizars@mellanox.com>
- Replaced sysinfo-snapshot.sh with sysinfo-snapshot.py

* Tue Nov 13 2012 Vladimir Sokolovsky <vlad@mellanox.com>
- Added ofed_rpm_info

* Tue Aug  7 2012 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added sysinfo-snapshot.sh

* Wed Jul 25 2012 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added QoS utilities

* Tue Oct  9 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Added ofed.[c]sh and ofed.conf if prefix is not /usr

* Tue Aug 21 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Changed version to 1.3

* Mon Apr  2  2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- uninstall.sh renamed to ofed_uninstall.sh and placed under %{_prefix}/sbin

* Tue Jun  13 2006 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Initial packaging
