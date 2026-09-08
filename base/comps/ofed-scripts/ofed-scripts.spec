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

%global CUSTOM_PREFIX %(if ( echo %{_prefix} | grep -E "^/usr$|^/usr/$" > /dev/null ); then echo -n '0'; else echo -n '1'; fi)

%global debug_package %{nil}

Summary: OFED scripts
%global upstream_name ofed-scripts

Name: ofed-scripts
Version: 26.04
Release: OFED.26.04.0.8.5
License: GPL/BSD
Url: http://www.openfabrics.org
Group: System Environment/Base
Source0: MLNX_OFED_SRC-26.04-0.8.5.0.tgz
Source6000: MLNX_OFED_SRC-26.04-0.8.5.0.tgz
BuildRoot: %{?build_root:%{build_root}}%{!?build_root:/var/tmp/%{name}-%{version}-root}
Vendor: OpenFabrics

# Packages that are no longer in MLNX_OFED and break package manager
# upgrade:
Obsoletes: ar_mgr

%description
OpenFabrics scripts

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
[ "${RPM_BUILD_ROOT}" != "/" -a -d ${RPM_BUILD_ROOT} ] && rm -rf $RPM_BUILD_ROOT
%setup -q -T -D -n %{upstream_name}-%{version}

%build

%install
%if "%{CUSTOM_PREFIX}" == "1"
touch ofed-files
%endif

install -d $RPM_BUILD_ROOT%{_prefix}/bin
install -d $RPM_BUILD_ROOT%{_prefix}/sbin
install -m 0755 uninstall.sh $RPM_BUILD_ROOT%{_prefix}/sbin/ofed_uninstall.sh
install -m 0755 sysinfo-snapshot.py $RPM_BUILD_ROOT%{_prefix}/sbin
install -m 0755 vendor_pre_uninstall.sh $RPM_BUILD_ROOT%{_prefix}/sbin
install -m 0755 vendor_post_uninstall.sh $RPM_BUILD_ROOT%{_prefix}/sbin
install -m 0755 ofed_info $RPM_BUILD_ROOT%{_prefix}/bin
install -m 0755 ofed_rpm_info $RPM_BUILD_ROOT%{_prefix}/bin

%if "%{CUSTOM_PREFIX}" == "1"
install -d $RPM_BUILD_ROOT/etc/profile.d
cat > $RPM_BUILD_ROOT/etc/profile.d/ofed.sh << EOF
if ! echo \${PATH} | grep -q %{_prefix}/bin ; then
        PATH=\${PATH}:%{_prefix}/bin
fi
if ! echo \${PATH} | grep -q %{_prefix}/sbin ; then
        PATH=\${PATH}:%{_prefix}/sbin
fi
if ! echo \${MANPATH} | grep -q %{_mandir} ; then
        MANPATH=\${MANPATH}:%{_mandir}
fi
EOF
cat > $RPM_BUILD_ROOT/etc/profile.d/ofed.csh << EOF
if (\$?path) then
if ( "\${path}" !~ *%{_prefix}/bin* ) then
        set path = ( \$path %{_prefix}/bin )
endif
if ( "\${path}" !~ *%{_prefix}/sbin* ) then
        set path = ( \$path %{_prefix}/sbin )
endif
else
        set path = ( %{_prefix}/bin %{_prefix}/sbin )
endif
if (\$?MANPATH) then
if ( "\${MANPATH}" !~ *%{_mandir}* ) then
        setenv MANPATH \${MANPATH}:%{_mandir}
endif
else
        setenv MANPATH %{_mandir}:
endif
EOF

install -d $RPM_BUILD_ROOT/etc/ld.so.conf.d
echo %{_libdir} > $RPM_BUILD_ROOT/etc/ld.so.conf.d/ofed.conf
%ifarch x86_64 ppc64
echo "%{_prefix}/lib" >> $RPM_BUILD_ROOT/etc/ld.so.conf.d/ofed.conf
%endif
echo "/etc/profile.d/ofed.sh" >> ofed-files
echo "/etc/profile.d/ofed.csh" >> ofed-files
echo "/etc/ld.so.conf.d/ofed.conf" >> ofed-files

%endif
# End of CUSTOM_PREFIX

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%clean
[ "${RPM_BUILD_ROOT}" != "/" -a -d ${RPM_BUILD_ROOT} ] && rm -rf $RPM_BUILD_ROOT

%if "%{CUSTOM_PREFIX}" == "1"
%files -f ofed-files
%else
%files
%endif
%defattr(-,root,root)
%{_prefix}/bin/*
%{_prefix}/sbin/*

%changelog
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
* Mon Apr  2 2007 Vladimir Sokolovsky <vlad@mellanox.co.il>
- uninstall.sh renamed to ofed_uninstall.sh and placed under %{_prefix}/sbin
* Tue Jun  13 2006 Vladimir Sokolovsky <vlad@mellanox.co.il>
- Initial packaging
