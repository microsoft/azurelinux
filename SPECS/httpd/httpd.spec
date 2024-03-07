%define mmn 20120211
%define _confdir %{_sysconfdir}
Summary:        The Apache HTTP Server
Name:           httpd
Version:        2.4.58
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://httpd.apache.org/
Source0:        https://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
Source1:        macros.httpd
Source2:        httpd-ssl-pass-dialog
Source3:        00-ssl.conf
Source4:        01-ldap.conf
Source5:        00-proxyhtml.conf
Source6:        ssl.conf
Source7:        01-session.conf
Source8:        10-listen443.conf
Source9:        httpd-init.service
Source10:       httpd-ssl-gencerts

# https://www.linuxfromscratch.org/patches/blfs/svn/httpd-2.4.56-blfs_layout-1.patch
Patch0:         httpd-2.4.53-blfs_layout-3.patch
Patch1:         httpd-uncomment-ServerName.patch
Patch2:         httpd-fix-apache-layout-log-path.patch

# CVE-1999-0236 must be mitigated by the user. See "Server Side Includes" at https://httpd.apache.org/docs/2.4/misc/security_tips.html
Patch100:       CVE-1999-0236.nopatch
# CVE-1999-1412 applies only to MacOS X
Patch101:       CVE-1999-1412.nopatch
# CVE-2007-0086 has been disputed to not be a vulnerability since 2007 due to default system configurations securing against it.
Patch102:       CVE-2007-0086.nopatch

BuildRequires:  apr
BuildRequires:  apr-util
BuildRequires:  apr-util-devel
BuildRequires:  expat-devel
BuildRequires:  libdb-devel
BuildRequires:  lua-devel
BuildRequires:  openldap
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel
BuildRequires:  systemd-rpm-macros

Requires:       apr-util
Requires:       libdb
Requires:       lua
Requires:       openldap
Requires:       openssl
Requires:       pcre
Requires(postun): %{_sbindir}/groupdel
Requires(postun): %{_sbindir}/userdel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

Provides:       apache2
Provides:       %{name}-mmn = %{mmn}
Provides:       %{name}-filesystem = %{version}-%{release}

%description
The Apache HTTP Server.

%package devel
Summary:        Header files for httpd
Group:          Applications/System

Requires:       apr-devel
Requires:       apr-util-devel
Requires:       httpd

%description devel
These are the header files of httpd.

%package docs
Summary:        Help files for httpd
Group:          Applications/System

Requires:       httpd

%description docs
These are the help files of httpd.

%package tools
Summary:        Tools for httpd
Group:          System Environment/Daemons

%description tools
The httpd-tools of httpd.

%package -n mod_ldap
Summary:        LDAP authentication modules for the Apache HTTP Server

Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-mmn = %{mmn}
Requires:       apr-util-ldap

%description -n mod_ldap
The mod_ldap and mod_authnz_ldap modules add support for LDAP
authentication to the Apache HTTP Server.

%package -n mod_proxy_html
Summary:        HTML and XML content filters for the Apache HTTP Server

BuildRequires:  libxml2-devel

Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-mmn = %{mmn}

%description -n mod_proxy_html
The mod_proxy_html and mod_xml2enc modules provide filters which can
transform and modify HTML and XML content.

%package -n mod_session
Summary:        Session interface for the Apache HTTP Server

Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-mmn = %{mmn}

%description -n mod_session
The mod_session module and associated backends provide an abstract
interface for storing and accessing per-user session data.

%package -n mod_ssl
Summary:        SSL/TLS module for the Apache HTTP Server

BuildRequires:  openssl-devel

Requires:       %{_sbindir}/nologin
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-mmn = %{mmn}
Requires:       sscg >= 2.2.0
Requires(pre):  %{name}-filesystem

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure \
            --datadir=%{_sysconfdir}/httpd         \
            --enable-authnz-fcgi                   \
            --enable-mods-shared="all cgi"         \
            --enable-mpms-shared=all               \
            --enable-ssl                           \
            --exec-prefix=%{_prefix}               \
            --libexecdir=%{_libdir}/httpd/modules  \
            --prefix=%{_sysconfdir}/httpd          \
            --sysconfdir=%{_confdir}/httpd/conf    \
            --with-apr-util=%{_prefix}             \
            --with-apr=%{_prefix}                  \
            --with-ssl

%make_build

%install
%make_install

# Install systemd service files
mkdir -p %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE9} %{buildroot}%{_unitdir}/httpd-init.service

# install conf file/directory
mkdir %{buildroot}%{_sysconfdir}/httpd/conf.d \
      %{buildroot}%{_sysconfdir}/httpd/conf.modules.d
for conf in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE7}; do
  install -m 644 -p $conf %{buildroot}%{_sysconfdir}/httpd/conf.modules.d/$(basename $conf)
done

install -m 644 -p %{SOURCE6} %{buildroot}%{_sysconfdir}/httpd/conf.d/ssl.conf

# install systemd override drop directory
# Web application packages can drop snippets into this location if
# they need ExecStart[pre|post].
mkdir %{buildroot}%{_unitdir}/httpd.service.d
mkdir %{buildroot}%{_unitdir}/httpd.socket.d

install -m 644 -p %{SOURCE8} %{buildroot}%{_unitdir}/httpd.socket.d/10-listen443.conf

# Create cache directory
mkdir -p %{buildroot}%{_localstatedir}/cache/httpd \
         %{buildroot}%{_localstatedir}/cache/httpd/proxy \
         %{buildroot}%{_localstatedir}/cache/httpd/ssl

# install 'http-ssl-gencerts' and 'http-ssl-pass-dialog'
mkdir -p %{buildroot}%{_libexecdir}
for exec in %{SOURCE2} %{SOURCE10}; do
  install -m 644 -p $exec %{buildroot}%{_libexecdir}/$(basename $exec)
done

install -vdm755 %{buildroot}%{_libdir}/systemd/system
install -vdm755 %{buildroot}%{_sysconfdir}/httpd/logs

cat << EOF >> %{buildroot}%{_libdir}/systemd/system/httpd.service
[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
PIDFile=/run/httpd/httpd.pid
RuntimeDirectory=httpd
ExecStart=%{_sbindir}/httpd -k start
ExecStop=%{_sbindir}/httpd -k stop
ExecReload=%{_sbindir}/httpd -k graceful

[Install]
WantedBy=multi-user.target

EOF

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -m 644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.httpd

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable httpd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-httpd.preset

ln -s %{_sbindir}/httpd %{buildroot}%{_sbindir}/apache2
ln -s %{_sysconfdir}/httpd/conf/httpd.conf %{buildroot}%{_sysconfdir}/httpd/httpd.conf

%post
/sbin/ldconfig
if [ $1 -eq 1 ]; then
    # this is initial installation
    if ! getent group apache >/dev/null; then
        groupadd -g 25 apache
    fi
    if ! getent passwd apache >/dev/null; then
        useradd -c "Apache Server" -d /srv/www -g apache \
            -s /bin/false -u 25 apache
    fi

    if [ -h %{_sysconfdir}/mime.types ]; then
        mv %{_sysconfdir}/mime.types %{_sysconfdir}/mime.types.orig
    fi
fi

ln -sf %{_sysconfdir}/httpd/conf/mime.types %{_sysconfdir}/mime.types
mkdir -p %{_var}/run/httpd
%systemd_post httpd.service

%preun
%systemd_preun httpd.service

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
    # this is delete operation
    if getent passwd apache >/dev/null; then
        userdel apache
    fi
    if getent group apache >/dev/null; then
        groupdel apache
    fi

    if [ -f %{_sysconfdir}/mime.types.orig ]; then
        mv %{_sysconfdir}/mime.types.orig %{_sysconfdir}/mime.types
    fi
fi
%systemd_postun_with_restart httpd.service

%files devel
%defattr(-,root,root)
%license LICENSE
%{_bindir}/apxs
%{_bindir}/dbmmanage
%{_mandir}/man1/apxs.1*
%{_includedir}/*
%{_rpmconfigdir}/macros.d/macros.httpd

%files docs
%defattr(-,root,root)
%{_sysconfdir}/httpd/manual/*

%files
%defattr(-,root,root)
%{_libdir}/httpd/*
%exclude %{_libdir}/httpd/modules/mod_auth_form.so
%exclude %{_libdir}/httpd/modules/mod_*ldap.so
%exclude %{_libdir}/httpd/modules/mod_proxy_html.so
%exclude %{_libdir}/httpd/modules/mod_session*.so
%exclude %{_libdir}/httpd/modules/mod_ssl.so
%exclude %{_libdir}/httpd/modules/mod_xml2enc.so
%{_bindir}/*
%exclude %{_bindir}/apxs
%exclude %{_bindir}/dbmmanage
%{_sbindir}/*
%{_datadir}/*
%{_sysconfdir}/httpd/build/*
%{_sysconfdir}/httpd/cgi-bin/*
%{_sysconfdir}/httpd/conf/extra
%{_sysconfdir}/httpd/conf/original
%config(noreplace) %{_sysconfdir}/httpd/conf/magic
%{_sysconfdir}/httpd/conf/envvars
%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%{_sysconfdir}/httpd/conf/mime.types
%{_sysconfdir}/httpd/error/*
%{_sysconfdir}/httpd/htdocs/*
%{_sysconfdir}/httpd/icons/*
%{_sysconfdir}/httpd/httpd.conf
%dir %{_sysconfdir}/httpd/logs
%{_libdir}/systemd/system/httpd.service
%{_libdir}/systemd/system-preset/50-httpd.preset

%files tools
%defattr(-,root,root)
%{_bindir}/*
%{_mandir}/man1/*
%license LICENSE
%doc NOTICE
%exclude %{_bindir}/apxs
%exclude %{_mandir}/man1/apxs.1*

%files -n mod_ldap
%{_libdir}/httpd/modules/mod_*ldap.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf

%files -n mod_proxy_html
%{_libdir}/httpd/modules/mod_proxy_html.so
%{_libdir}/httpd/modules/mod_xml2enc.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf

%files -n mod_session
%{_libdir}/httpd/modules/mod_session*.so
%{_libdir}/httpd/modules/mod_auth_form.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%files -n mod_ssl
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/httpd/ssl
%{_unitdir}/httpd.socket.d/10-listen443.conf
%{_unitdir}/httpd-init.service
%{_libexecdir}/httpd-ssl-gencerts
%{_libexecdir}/httpd-ssl-pass-dialog

%changelog
* Fri Oct 20 2023 Muhammad Falak <mwani@microsoft.com> - 2.4.58-1
- Upgrade version to address CVE-2023-45802, CVE-2023-43622 & CVE-2023-31122

* Wed Aug 16 2023 Andy Zaugg <azaugg@linkedin.com> - 2.4.56-1
- Patch config.layout and provide and provide a real log path
- Fix PIDfile reference to /run/httpd/httpd.pid

* Tue Mar 14 2023 Thien Trung Vuong <tvuong@microsoft.com> - 2.4.56-1
- Upgrade to version 2.4.56 - Fixes CVE-2023-27522, CVE-2023-25690

* Tue Feb 07 2023 Rachel Menge <rachelmenge@microsoft.com> - 2.4.55-1
- Upgrade to version 2.4.55. Fixes CVE-2022-36760

* Tue Nov 08 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.4.54-1
- Auto-upgrade to 2.4.54 - CVE-2022-31813,CVE-2022-28615

* Tue Apr 12 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.4.53-1
- Update httpd version to 2.4.53 to fix CVE CVE-2022-22720, CVE-2022-22721, CVE-2022-23943.

* Wed Jan 19 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.4.52-1
- Update httpd version to 2.4.52.

* Tue Nov 30 2021 Mateusz Malisz <mamalisz@microsoft.com> - 2.4.46-10
- Add explicit requires for libdb.

* Wed Sep 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.46-9
- Added missing BR on "systemd-rpm-macros".

* Wed Sep 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.46-8
- Fixing invalid past release numbering in the changelog.
- Introduced following subpackages using Fedora 32 (license: MIT) specs as guidance:
  - mod_ldap,
  - mod_proxy_html,
  - mod_session,
  - mod_ssl.

* Thu Jun 24 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> 2.4.46-7
- CVE-2021-26691 fix

* Tue Jun 22 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> 2.4.46-6
- CVE-2020-13950 CVE-2021-26690 CVE-2021-30641 and CVE-2020-35452 fixes

* Wed Apr 07 2021 Henry Li <lihl@microsoft.com> - 2.4.46-5
- Add macros.httpd to provide necessary httpd macros

* Tue Feb 09 2021 Henry Li <lihl@microsoft.com> - 2.4.46-4
- Add Provides for httpd-mmn and httpd-filesystem from httpd
- Fix files section for httpd-devel and httpd-tools

* Tue Oct 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.4.46-3
- Mark CVE-2007-0086 as nopatch

* Mon Sep 28 2020 Daniel McIlvaney <damcilva@microsoft.com> 2.4.46-2
- Mark CVE-1999-0236 CVE-1999-1412 as nopatch

* Tue Aug 18 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.4.46-1
- Updated to 2.4.46 to resolve CVE-2020-11984.

* Tue May 19 2020 Ruying Chen <v-ruyche@microsoft.com> 2.4.43-1
- Updated to 2.4.43 to resolve the following CVEs
- CVE-2019-10081, CVE-2019-10082, CVE-2019-10092, CVE-2019-10097
- CVE-2019-10098, CVE-2020-1927, CVE-2020-1934

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.4.39-4
- Added %%license line automatically

* Tue Apr 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.4.39-3
- Updated and verified 'Source0', 'Patch0' and 'URL' tags.
- License verified.
- Removed '%%define sha1' line.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.4.39-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Apr 16 2019 Dweep Advani <dadvani@vmware.com> 2.4.39-1
- Upgrading to 2.4.39 for fixing multiple CVEs
- (1) CVE-2018-17189 (2) CVE-2018-17199 (3) CVE-2019-0190
- (4) CVE-2019-0211 (5) CVE-2019-0215 (6) CVE-2019-0217

* Thu Jan 24 2019 Dweep Advani <dadvani@vmware.com> 2.4.34-2
- Fixed CVE-2018-11763

* Wed Aug 29 2018 Tapas Kundu <tkundu@vmware.com> 2.4.34-1
- Updated to version 2.4.34, fix CVE-2018-1333

* Mon Oct 02 2017 Xiaolin Li <xiaolinl@vmware.com> 2.4.28-1
- Updated to version 2.4.28

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.27-3
- Remove shadow from requires and use explicit tools for post actions

* Mon Aug 07 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-2
- Add shadow to requires for useradd/groupadd

* Mon Jul 24 2017 Anish Swaminathan <anishs@vmware.com>  2.4.27-1
- Updated to version 2.4.27 - Fixes CVE-2017-3167

* Wed May 31 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 2.4.25-3
- Provide preset file to disable service by default.

* Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-2
- Fixing httpd.pid file write issue

* Fri Mar 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.4.25-1
- Updated to version 2.4.25

* Tue Dec 27 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.18-8
- BuildRequires lua, Requires lua.

* Wed Dec 21 2016 Anish Swaminathan <anishs@vmware.com>  2.4.18-7
- Change config file properties for httpd.conf

* Thu Jul 28 2016 Divya Thaluru <dthaluru@vmware.com> 2.4.18-6
- Removed packaging of debug files

* Wed Jul 27 2016 Divya Thaluru <dthaluru@vmware.com> 2.4.18-5
- Added patch for CVE-2016-5387

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.18-4
- GA - Bump release of all rpms

* Thu May 05 2016 Kumar Kaushik <kaushikk@vmware.com> 2.4.18-3
- Adding upgrade support in pre/post/un script.

* Mon Mar 21 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 2.4.18-2
- Fixing systemd service

* Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.18-1
- Updated to version 2.4.18

* Mon Nov 23 2015 Sharath George <sharathg@vmware.com> 2.4.12-4
- Add /etc/mime.types

* Tue Sep 29 2015 Xiaolin Li <xiaolinl@vmware.com> 2.4.12-3
- Move perl script to tools package.

* Thu Jul 16 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-2
- Added service file. Changed installation paths.

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> 2.4.12-1
- Initial build. First version
