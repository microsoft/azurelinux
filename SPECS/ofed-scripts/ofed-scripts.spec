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

Summary:        OFED scripts
Name:           ofed-scripts
Version:        5.6
Release:        1%{?dist}
License:        GPLv2/BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://www.openfabrics.org
#Source0:       https://linux.mellanox.com/public/repo/doca/1.3.0/extras/mlnx_ofed/5.6-1.0.3.3/SOURCES/ofed-scripts_5.6.orig.tar.gz
Source0:        %{name}-%{version}.tar.gz
%global CUSTOM_PREFIX %(if ( echo %{_prefix} | grep -E "^/usr$|^/usr/$" > /dev/null ); then echo -n '0'; else echo -n '1'; fi)
%global debug_package %{nil}
%global long-release OFED.5.6.0.6.8

%description
OpenFabrics scripts

%prep
%autosetup -p1 -n %{name}-%{version}
cp debian/copyright COPYRIGHT

%build

%install
%if "%{CUSTOM_PREFIX}" == "1"
touch ofed-files
%endif

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

%if "%{CUSTOM_PREFIX}" == "1"
install -d %{buildroot}/etc/profile.d
cat > %{buildroot}/etc/profile.d/ofed.sh << EOF
if ! echo \${PATH} | grep -q %{_bindir} ; then
        PATH=\${PATH}:%{_bindir}
fi
if ! echo \${PATH} | grep -q %{_sbindir} ; then
        PATH=\${PATH}:%{_sbindir}
fi
if ! echo \${MANPATH} | grep -q %{_mandir} ; then
        MANPATH=\${MANPATH}:%{_mandir}
fi
EOF
cat > %{buildroot}/etc/profile.d/ofed.csh << EOF
if (\$?path) then
if ( "\${path}" !~ *%{_bindir}* ) then
        set path = ( \$path %{_bindir} )
endif
if ( "\${path}" !~ *%{_sbindir}* ) then
        set path = ( \$path %{_sbindir} )
endif
else
        set path = ( %{_bindir} %{_sbindir} )
endif
if (\$?MANPATH) then
if ( "\${MANPATH}" !~ *%{_mandir}* ) then
        setenv MANPATH \${MANPATH}:%{_mandir}
endif
else
        setenv MANPATH %{_mandir}:
endif
EOF

install -d %{buildroot}/etc/ld.so.conf.d
echo %{_libdir} > %{buildroot}/etc/ld.so.conf.d/ofed.conf
%ifarch x86_64 ppc64
echo "%{_prefix}/lib" >> %{buildroot}/etc/ld.so.conf.d/ofed.conf
%endif
echo "/etc/profile.d/ofed.sh" >> ofed-files
echo "/etc/profile.d/ofed.csh" >> ofed-files
echo "/etc/ld.so.conf.d/ofed.conf" >> ofed-files

%endif
# End of CUSTOM_PREFIX

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

%if "%{CUSTOM_PREFIX}" == "1"
%files -f ofed-files
%else
%files
%endif
%defattr(-,root,root)
%license COPYRIGHT
%{_bindir}/*
%{_sbindir}/*

%changelog
* Fri Jul 22 2022 Rachel Menge <rachelmenge@microsoft.com> - 5.6-1
- Initial CBL-Mariner import from NVIDIA (license: ASL 2.0)
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
