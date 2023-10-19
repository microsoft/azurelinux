%global _default_patch_fuzz 2
# Is elliptic curve cryptography supported?
%global HAVE_EC_CRYPTO 1
%global debug_package %{nil}

Summary:        High-performance and highly configurable free RADIUS server
Name:           freeradius
Version:        3.2.3
Release:        2%{?dist}
License:        GPLv2+ AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://freeradius.org/

%global dist_base freeradius-server-%{version}
%global docdir %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
Source0:        ftp://ftp.freeradius.org/pub/radius/%{dist_base}.tar.bz2
Source100:      radiusd.service
Source102:      freeradius-logrotate
Source103:      freeradius-pam-conf
Source104:      freeradius-tmpfiles.conf
Source105:      freeradius.sysusers
Patch1:         freeradius-Adjust-configuration-to-fit-Red-Hat-specifics.patch
Patch2:         freeradius-Use-system-crypto-policy-by-default.patch
Patch3:         freeradius-bootstrap-create-only.patch
Patch4:         freeradius-no-buildtime-cert-gen.patch
Patch5:         freeradius-bootstrap-make-permissions.patch
Patch6:         fix-error-for-expansion-of-macro-in-thread.h.patch
BuildRequires:  autoconf
BuildRequires:  gcc
BuildRequires:  gdbm-devel
BuildRequires:  libpcap-devel
BuildRequires:  libtalloc-devel
BuildRequires:  make
BuildRequires:  net-snmp-devel
BuildRequires:  net-snmp-utils
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  pcre-devel
BuildRequires:  readline-devel
BuildRequires:  systemd-units
BuildRequires:  zlib-devel
# Require OpenSSL version we built with, or newer, to avoid startup failures
# due to runtime OpenSSL version checks.
Requires: openssl >= %(rpm -q --queryformat '%%{VERSION}' openssl)
Requires(pre): shadow-utils glibc-common
Requires(post): systemd-sysv
Requires(post): systemd-units
# Needed for certificate generation
Requires(post): make
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
The FreeRADIUS Server Project is a high performance and highly configurable
GPL'd free RADIUS server. The server is similar in some respects to
Livingston's 2.0 server.  While FreeRADIUS started as a variant of the
Cistron RADIUS server, they don't share a lot in common any more. It now has
many more features than Cistron or Livingston, and is much more configurable.

FreeRADIUS is an Internet authentication daemon, which implements the RADIUS
protocol, as defined in RFC 2865 (and others). It allows Network Access
Servers (NAS boxes) to perform authentication for dial-up users. There are
also RADIUS clients available for Web servers, firewalls, Unix logins, and
more.  Using RADIUS allows authentication and authorization for a network to
be centralized, and minimizes the amount of re-configuration which has to be
done when adding or deleting new users.

%package doc
Summary:        FreeRADIUS documentation

%description doc
All documentation supplied by the FreeRADIUS project is included
in this package.

%package utils
Summary:        FreeRADIUS utilities
Requires:       %{name} = %{version}-%{release}
Requires:       libpcap >= 0.9.4
Requires:       perl-Net-IP

%description utils
The FreeRADIUS server has a number of features found in other servers,
and additional features not found in any other server. Rather than
doing a feature by feature comparison, we will simply list the features
of the server, and let you decide if they satisfy your needs.

Support for RFC and VSA Attributes Additional server configuration
attributes Selecting a particular configuration Authentication methods

%package devel
Summary:        FreeRADIUS development files
Requires:       %{name} = %{version}-%{release}

%description devel
Development headers and libraries for FreeRADIUS.

%package ldap
Summary:        LDAP support for freeradius
BuildRequires:  openldap-devel
Requires:       %{name} = %{version}-%{release}

%description ldap
This plugin provides the LDAP support for the FreeRADIUS server project.

%package krb5
Summary:        Kerberos 5 support for freeradius
BuildRequires:  krb5-devel
Requires:       %{name} = %{version}-%{release}

%description krb5
This plugin provides the Kerberos 5 support for the FreeRADIUS server project.

%package perl
Summary:        Perl support for freeradius
%{?fedora:BuildRequires: perl-devel}
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::Embed)
Requires:       %{name} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description perl
This plugin provides the Perl support for the FreeRADIUS server project.

%package -n python3-freeradius
Summary:        Python 3 support for freeradius
%{?python_provide:%python_provide python3-freeradius}
BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}

%description -n python3-freeradius
This plugin provides the Python 3 support for the FreeRADIUS server project.

%package mysql
Summary:        MySQL support for freeradius
BuildRequires:  mariadb-connector-c-devel
Requires:       %{name} = %{version}-%{release}

%description mysql
This plugin provides the MySQL support for the FreeRADIUS server project.

%package postgresql
Summary:        Postgresql support for freeradius
BuildRequires:  postgresql-devel
Requires:       %{name} = %{version}-%{release}

%description postgresql
This plugin provides the postgresql support for the FreeRADIUS server project.

%package sqlite
Summary:        SQLite support for freeradius
BuildRequires:  sqlite-devel
Requires:       %{name} = %{version}-%{release}

%description sqlite
This plugin provides the SQLite support for the FreeRADIUS server project.

%package unixODBC
Summary:        Unix ODBC support for freeradius
BuildRequires:  unixODBC-devel
Requires:       %{name} = %{version}-%{release}

%description unixODBC
This plugin provides the unixODBC support for the FreeRADIUS server project.

%package rest
Summary:        REST support for freeradius
BuildRequires:  json-c-devel
BuildRequires:  libcurl-devel
Requires:       %{name} = %{version}-%{release}

%description rest
This plugin provides the REST support for the FreeRADIUS server project.

%prep
%autosetup -p1 -n %{dist_base}

%build
# Force compile/link options, extra security for network facing daemon
%global _hardened_build 1

# Hack: rlm_python3 as stable; prevents building other unstable modules.
sed 's/rlm_python/rlm_python3/g' src/modules/stable -i

# python3-config is broken:
# https://bugzilla.redhat.com/show_bug.cgi?id=1772988
export PY3_LIB_DIR=%{_libdir}/"$(python3-config --configdir | sed 's#/usr/lib/##g')"
export PY3_INC_DIR="$(python3 -c 'import sysconfig; print(sysconfig.get_config_var("INCLUDEPY"))')"

# In order for the above hack to stick, do a fake configure so
# we can run reconfig before cleaning up after ourselves and running
# configure for real.
./configure && make reconfig && (make clean distclean || true)

%configure \
        --libdir=%{_libdir}/freeradius \
        --enable-reproducible-builds \
        --disable-openssl-version-check \
        --with-openssl \
        --with-udpfromto \
        --with-threads \
        --with-docdir=%{docdir} \
        --with-rlm-sql_postgresql-include-dir=/usr/include/pgsql \
        --with-rlm-sql-postgresql-lib-dir=%{_libdir} \
        --with-rlm-sql_mysql-include-dir=/usr/include/mysql \
        --with-mysql-lib-dir=%{_libdir}/mariadb \
        --with-unixodbc-lib-dir=%{_libdir} \
        --with-rlm-dbm-lib-dir=%{_libdir} \
        --with-rlm-krb5-include-dir=/usr/kerberos/include \
        --with-rlm_python3 \
        --with-rlm-python3-lib-dir=$PY3_LIB_DIR \
        --with-rlm-python3-include-dir=$PY3_INC_DIR \
        --without-rlm_eap_ikev2 \
        --without-rlm_eap_tnc \
        --without-rlm_sql_iodbc \
        --without-rlm_sql_firebird \
        --without-rlm_sql_db2 \
        --without-rlm_sql_oracle \
        --without-rlm_unbound \
        --without-rlm_redis \
        --without-rlm_rediswho \
        --without-rlm_cache_memcached

make

%install
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/radiusd
make install R=$RPM_BUILD_ROOT

# logs
mkdir -p $RPM_BUILD_ROOT/var/log/radius/radacct
touch $RPM_BUILD_ROOT/var/log/radius/{radutmp,radius.log}

install -D -m 644 %{SOURCE100} $RPM_BUILD_ROOT/%{_unitdir}/radiusd.service
install -D -m 644 %{SOURCE102} $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/radiusd
install -D -m 644 %{SOURCE103} $RPM_BUILD_ROOT/%{_sysconfdir}/pam.d/radiusd

mkdir -p %{buildroot}%{_tmpfilesdir}
mkdir -p %{buildroot}%{_localstatedir}/run/
install -d -m 0710 %{buildroot}%{_localstatedir}/run/radiusd/
install -d -m 0700 %{buildroot}%{_localstatedir}/run/radiusd/tmp
install -m 0644 %{SOURCE104} %{buildroot}%{_tmpfilesdir}/radiusd.conf
install -p -D -m 0644 %{SOURCE105} %{buildroot}%{_sysusersdir}/freeradius.conf

# install SNMP MIB files
mkdir -p $RPM_BUILD_ROOT%{_datadir}/snmp/mibs/
install -m 644 mibs/*RADIUS*.mib $RPM_BUILD_ROOT%{_datadir}/snmp/mibs/

# remove unneeded stuff
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.crt
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.crl
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.csr
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.der
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.key
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.pem
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/*.p12
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/index.*
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/serial*
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/dh
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/certs/random

rm -f $RPM_BUILD_ROOT/usr/sbin/rc.radiusd
rm -f $RPM_BUILD_ROOT/usr/bin/rbmonkey
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.a
rm -rf $RPM_BUILD_ROOT/%{_libdir}/freeradius/*.la

rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/main/mssql

rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/ippool/oracle
rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/ippool/mssql
rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/ippool-dhcp/oracle
rm -rf $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/main/oracle
rm -r $RPM_BUILD_ROOT/etc/raddb/mods-config/sql/moonshot-targeted-ids

rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-available/unbound
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-config/unbound/default.conf
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-available/couchbase
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-available/abfab*
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-available/moonshot-targeted-ids
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/policy.d/abfab*
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/policy.d/moonshot-targeted-ids
rm $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/sites-available/abfab*

rm $RPM_BUILD_ROOT/%{_libdir}/freeradius/rlm_test.so

# remove unsupported config files
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/experimental.conf

# Mongo will never be supported on Fedora or RHEL
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-config/sql/ippool/mongo/queries.conf
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/raddb/mods-config/sql/main/mongo/queries.conf

# install doc files omitted by standard install
for f in COPYRIGHT CREDITS INSTALL.rst README.rst VERSION; do
    cp $f $RPM_BUILD_ROOT/%{docdir}
done
cp LICENSE $RPM_BUILD_ROOT/%{docdir}/LICENSE.gpl
cp src/lib/LICENSE $RPM_BUILD_ROOT/%{docdir}/LICENSE.lgpl
cp src/LICENSE.openssl $RPM_BUILD_ROOT/%{docdir}/LICENSE.openssl

# add Red Hat specific documentation
cat >> $RPM_BUILD_ROOT/%{docdir}/REDHAT << EOF

Red Hat, RHEL, Fedora, and CentOS specific information can be found on the
FreeRADIUS Wiki in the Red Hat FAQ.

http://wiki.freeradius.org/guide/Red-Hat-FAQ

Please reference that document.

All documentation is in the freeradius-doc sub-package.

EOF


# Make sure our user/group is present prior to any package or subpackage installation
%pre
%sysusers_create_package %{name} %{SOURCE105}

%preun
%systemd_preun radiusd.service

%postun
%systemd_postun_with_restart radiusd.service

/bin/systemctl try-restart radiusd.service >/dev/null 2>&1 || :

%files

# doc
%license %{docdir}/LICENSE.gpl
%license %{docdir}/LICENSE.lgpl
%license %{docdir}/LICENSE.openssl
%doc %{docdir}/REDHAT

# system
%config(noreplace) %{_sysconfdir}/pam.d/radiusd
%config(noreplace) %{_sysconfdir}/logrotate.d/radiusd
%{_unitdir}/radiusd.service
%{_tmpfilesdir}/radiusd.conf
%{_sysusersdir}/freeradius.conf
%dir %attr(710,radiusd,radiusd) %{_localstatedir}/run/radiusd
%dir %attr(700,radiusd,radiusd) %{_localstatedir}/run/radiusd/tmp
%dir %attr(755,radiusd,radiusd) %{_localstatedir}/lib/radiusd

# configs (raddb)
%dir %attr(755,root,radiusd) /etc/raddb
%defattr(-,root,radiusd)
/etc/raddb/README.rst
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/panic.gdb

%attr(644,root,radiusd) %config(noreplace) /etc/raddb/dictionary
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/clients.conf

%attr(640,root,radiusd) %config(noreplace) /etc/raddb/templates.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/trigger.conf

# symlink: /etc/raddb/hints -> ./mods-config/preprocess/hints
%config /etc/raddb/hints

# symlink: /etc/raddb/huntgroups -> ./mods-config/preprocess/huntgroups
%config /etc/raddb/huntgroups

%attr(640,root,radiusd) %config(noreplace) /etc/raddb/proxy.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/radiusd.conf

# symlink: /etc/raddb/users -> ./mods-config/files/authorize
%config(noreplace) /etc/raddb/users

# certs
%dir %attr(770,root,radiusd) /etc/raddb/certs
%config(noreplace) /etc/raddb/certs/Makefile
%config(noreplace) /etc/raddb/certs/passwords.mk
/etc/raddb/certs/README.md
%config(noreplace) /etc/raddb/certs/xpextensions
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/certs/*.cnf
%attr(750,root,radiusd) /etc/raddb/certs/bootstrap

# mods-config
%dir %attr(750,root,radiusd) /etc/raddb/mods-config
/etc/raddb/mods-config/README.rst
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/attr_filter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/attr_filter/*
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/files
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/files/*
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/preprocess
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/preprocess/*
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/realm/freeradius-naptr-to-home-server.sh

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/counter
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/cui
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool-dhcp
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main

# sites-available
%dir %attr(750,root,radiusd) /etc/raddb/sites-available
/etc/raddb/sites-available/README
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/aws-nlb
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/resource-check
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/control-socket
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/decoupled-accounting
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/robust-proxy-accounting
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/soh
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/coa
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/coa-relay
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/example
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/inner-tunnel
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/dhcp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/check-eap-tls
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/status
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/dhcp.relay
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/virtual.example.com
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/originate-coa
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/vmps
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/default
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/proxy-inner-tunnel
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/dynamic-clients
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/copy-acct-to-home-server
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/buffered-sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/tls
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/totp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/channel_bindings
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/challenge
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/google-ldap-auth
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/sites-available/tls-cache

# sites-enabled
# symlink: /etc/raddb/sites-enabled/xxx -> ../sites-available/xxx
%dir %attr(750,root,radiusd) /etc/raddb/sites-enabled
%config(missingok) /etc/raddb/sites-enabled/inner-tunnel
%config(missingok) /etc/raddb/sites-enabled/default

# mods-available
%dir %attr(750,root,radiusd) /etc/raddb/mods-available
/etc/raddb/mods-available/README.rst
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/always
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/attr_filter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/cache
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/cache_auth
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/chap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/counter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/cui
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/date
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/detail
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/detail.example.com
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/detail.log
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dhcp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dhcp_files
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dhcp_passwd
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dhcp_sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dhcp_sqlippool
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/digest
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/dynamic_clients
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/eap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/echo
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/etc_group
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/exec
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/expiration
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/expr
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/files
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/idn
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/inner-eap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/ippool
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/json
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/ldap_google
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/linelog
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/logintime
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/mac2ip
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/mac2vlan
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/mschap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/ntlm_auth
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/opendirectory
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/pam
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/pap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/passwd
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/preprocess
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/python
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/python3
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/radutmp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/realm
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/redis
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/rediswho
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/replicate
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/smbpasswd
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/smsotp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/soh
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sometimes
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sql_map
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sqlcounter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sqlippool
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/sradutmp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/totp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/unix
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/unpack
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/utf8
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/wimax
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/yubikey

# mods-enabled
# symlink: /etc/raddb/mods-enabled/xxx -> ../mods-available/xxx
%dir %attr(750,root,radiusd) /etc/raddb/mods-enabled
%config(missingok) /etc/raddb/mods-enabled/always
%config(missingok) /etc/raddb/mods-enabled/attr_filter
%config(missingok) /etc/raddb/mods-enabled/chap
%config(missingok) /etc/raddb/mods-enabled/date
%config(missingok) /etc/raddb/mods-enabled/detail
%config(missingok) /etc/raddb/mods-enabled/detail.log
%config(missingok) /etc/raddb/mods-enabled/digest
%config(missingok) /etc/raddb/mods-enabled/dynamic_clients
%config(missingok) /etc/raddb/mods-enabled/eap
%config(missingok) /etc/raddb/mods-enabled/echo
%config(missingok) /etc/raddb/mods-enabled/exec
%config(missingok) /etc/raddb/mods-enabled/expiration
%config(missingok) /etc/raddb/mods-enabled/expr
%config(missingok) /etc/raddb/mods-enabled/files
%config(missingok) /etc/raddb/mods-enabled/linelog
%config(missingok) /etc/raddb/mods-enabled/logintime
%config(missingok) /etc/raddb/mods-enabled/mschap
%config(missingok) /etc/raddb/mods-enabled/ntlm_auth
%config(missingok) /etc/raddb/mods-enabled/pap
%config(missingok) /etc/raddb/mods-enabled/passwd
%config(missingok) /etc/raddb/mods-enabled/preprocess
%config(missingok) /etc/raddb/mods-enabled/radutmp
%config(missingok) /etc/raddb/mods-enabled/realm
%config(missingok) /etc/raddb/mods-enabled/replicate
%config(missingok) /etc/raddb/mods-enabled/soh
%config(missingok) /etc/raddb/mods-enabled/sradutmp
%config(missingok) /etc/raddb/mods-enabled/totp
%config(missingok) /etc/raddb/mods-enabled/unix
%config(missingok) /etc/raddb/mods-enabled/unpack
%config(missingok) /etc/raddb/mods-enabled/utf8

# policy
%dir %attr(750,root,radiusd) /etc/raddb/policy.d
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/accounting
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/canonicalization
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/control
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/cui
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/debug
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/dhcp
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/eap
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/filter
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/operator-name
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/policy.d/rfc7542


# binaries
%defattr(-,root,root)
/usr/sbin/checkrad
/usr/sbin/raddebug
/usr/sbin/radiusd
/usr/sbin/radmin

# dictionaries
%dir %attr(755,root,root) /usr/share/freeradius
/usr/share/freeradius/*

# logs
%dir %attr(700,radiusd,radiusd) /var/log/radius/
%dir %attr(700,radiusd,radiusd) /var/log/radius/radacct/
%ghost %attr(644,radiusd,radiusd) /var/log/radius/radutmp
%ghost %attr(600,radiusd,radiusd) /var/log/radius/radius.log

# libs
%attr(755,root,root) %{_libdir}/freeradius/lib*.so*

# loadable modules
%dir %attr(755,root,root) %{_libdir}/freeradius
%{_libdir}/freeradius/proto_dhcp.so
%{_libdir}/freeradius/proto_vmps.so
%{_libdir}/freeradius/rlm_always.so
%{_libdir}/freeradius/rlm_attr_filter.so
%{_libdir}/freeradius/rlm_cache.so
%{_libdir}/freeradius/rlm_cache_rbtree.so
%{_libdir}/freeradius/rlm_chap.so
%{_libdir}/freeradius/rlm_counter.so
%{_libdir}/freeradius/rlm_date.so
%{_libdir}/freeradius/rlm_detail.so
%{_libdir}/freeradius/rlm_dhcp.so
%{_libdir}/freeradius/rlm_digest.so
%{_libdir}/freeradius/rlm_dynamic_clients.so
%{_libdir}/freeradius/rlm_eap.so
%{_libdir}/freeradius/rlm_eap_fast.so
%{_libdir}/freeradius/rlm_eap_gtc.so
%{_libdir}/freeradius/rlm_eap_md5.so
%{_libdir}/freeradius/rlm_eap_mschapv2.so
%{_libdir}/freeradius/rlm_eap_peap.so
%if %{HAVE_EC_CRYPTO}
%{_libdir}/freeradius/rlm_eap_pwd.so
%endif
%{_libdir}/freeradius/rlm_eap_sim.so
%{_libdir}/freeradius/rlm_eap_tls.so
%{_libdir}/freeradius/rlm_eap_ttls.so
%{_libdir}/freeradius/rlm_exec.so
%{_libdir}/freeradius/rlm_expiration.so
%{_libdir}/freeradius/rlm_expr.so
%{_libdir}/freeradius/rlm_files.so
%{_libdir}/freeradius/rlm_ippool.so
%{_libdir}/freeradius/rlm_json.so
%{_libdir}/freeradius/rlm_linelog.so
%{_libdir}/freeradius/rlm_logintime.so
%{_libdir}/freeradius/rlm_mschap.so
%{_libdir}/freeradius/rlm_pam.so
%{_libdir}/freeradius/rlm_pap.so
%{_libdir}/freeradius/rlm_passwd.so
%{_libdir}/freeradius/rlm_preprocess.so
%{_libdir}/freeradius/rlm_radutmp.so
%{_libdir}/freeradius/rlm_realm.so
%{_libdir}/freeradius/rlm_replicate.so
%{_libdir}/freeradius/rlm_soh.so
%{_libdir}/freeradius/rlm_sometimes.so
%{_libdir}/freeradius/rlm_sql.so
%{_libdir}/freeradius/rlm_sqlcounter.so
%{_libdir}/freeradius/rlm_sqlippool.so
%{_libdir}/freeradius/rlm_sql_map.so
%{_libdir}/freeradius/rlm_sql_null.so
%{_libdir}/freeradius/rlm_totp.so
%{_libdir}/freeradius/rlm_unix.so
%{_libdir}/freeradius/rlm_unpack.so
%{_libdir}/freeradius/rlm_utf8.so
%{_libdir}/freeradius/rlm_wimax.so
%{_libdir}/freeradius/rlm_yubikey.so

# main man pages
%{_mandir}/man5/clients.conf.5.gz
%{_mandir}/man5/dictionary.5.gz
%{_mandir}/man5/radiusd.conf.5.gz
%{_mandir}/man5/radrelay.conf.5.gz
%{_mandir}/man5/rlm_always.5.gz
%{_mandir}/man5/rlm_attr_filter.5.gz
%{_mandir}/man5/rlm_chap.5.gz
%{_mandir}/man5/rlm_counter.5.gz
%{_mandir}/man5/rlm_detail.5.gz
%{_mandir}/man5/rlm_digest.5.gz
%{_mandir}/man5/rlm_expr.5.gz
%{_mandir}/man5/rlm_files.5.gz
%{_mandir}/man5/rlm_idn.5.gz
%{_mandir}/man5/rlm_mschap.5.gz
%{_mandir}/man5/rlm_pap.5.gz
%{_mandir}/man5/rlm_passwd.5.gz
%{_mandir}/man5/rlm_realm.5.gz
%{_mandir}/man5/rlm_sql.5.gz
%{_mandir}/man5/rlm_unbound.5.gz
%{_mandir}/man5/rlm_unix.5.gz
%{_mandir}/man5/unlang.5.gz
%{_mandir}/man5/users.5.gz
%{_mandir}/man8/raddebug.8.gz
%{_mandir}/man8/radiusd.8.gz
%{_mandir}/man8/radmin.8.gz
%{_mandir}/man8/radrelay.8.gz
%{_mandir}/man8/rlm_sqlippool_tool.8.gz

# MIB files
%{_datadir}/snmp/mibs/*RADIUS*.mib

%files doc

%doc %{docdir}/

%files utils
/usr/bin/*

# utils man pages
%doc %{_mandir}/man1/radclient.1.gz
%doc %{_mandir}/man1/radeapclient.1.gz
%doc %{_mandir}/man1/radlast.1.gz
%doc %{_mandir}/man1/radtest.1.gz
%doc %{_mandir}/man1/radwho.1.gz
%doc %{_mandir}/man1/radzap.1.gz
%doc %{_mandir}/man1/rad_counter.1.gz
%doc %{_mandir}/man1/smbencrypt.1.gz
%doc %{_mandir}/man1/dhcpclient.1.gz
%doc %{_mandir}/man5/checkrad.5.gz
%doc %{_mandir}/man8/radcrypt.8.gz
%doc %{_mandir}/man8/radsniff.8.gz
%doc %{_mandir}/man8/radsqlrelay.8.gz
%doc %{_mandir}/man8/rlm_ippool_tool.8.gz

%files devel
/usr/include/freeradius

%files krb5
%{_libdir}/freeradius/rlm_krb5.so
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/krb5

%files perl
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/perl

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/perl
%attr(640,root,radiusd) /etc/raddb/mods-config/perl/example.pl

%{_libdir}/freeradius/rlm_perl.so

%files -n python3-freeradius
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/python3
/etc/raddb/mods-config/python3/example.py*
/etc/raddb/mods-config/python3/radiusd.py*
%{_libdir}/freeradius/rlm_python3.so

%files mysql
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/counter/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/weeklycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/mysql/noresetcounter.conf

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/cui/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/mysql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/dhcp/mssql
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/mssql/queries.conf
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/mssql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/dhcp/mysql
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/mysql/queries.conf
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/mysql/schema.sql
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/mysql/setup.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/dhcp/oracle
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/oracle/queries.conf
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/oracle/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/dhcp/postgresql
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/postgresql/queries.conf
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/postgresql/schema.sql
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/postgresql/setup.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/dhcp/sqlite
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/sqlite/queries.conf
%attr(640,root,radiusd) /etc/raddb/mods-config/sql/dhcp/sqlite/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/mysql/schema.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/mysql/procedure.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/mysql/procedure-no-skip-locked.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool-dhcp/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mysql/schema.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mysql/procedure.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mysql/procedure-no-skip-locked.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool-dhcp/mssql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mssql/procedure.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mssql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/mssql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool-dhcp/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/postgresql/procedure.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/postgresql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/mysql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/setup.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/schema.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/process-radacct.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/mysql/extras
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/mysql/extras/wimax
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/extras/wimax/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/mysql/extras/wimax/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/ndb
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/ndb/setup.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/ndb/schema.sql
/etc/raddb/mods-config/sql/main/ndb/README

%{_libdir}/freeradius/rlm_sql_mysql.so

%files postgresql
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/counter/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/weeklycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/postgresql/noresetcounter.conf

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/cui/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/postgresql/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/postgresql/schema.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/postgresql/procedure.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/postgresql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/setup.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/schema.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/process-radacct.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/postgresql/extras
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/extras/voip-postpaid.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/postgresql/extras/cisco_h323_db_schema.sql

%{_libdir}/freeradius/rlm_sql_postgresql.so

%files sqlite
%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/counter/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/dailycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/expire_on_login.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/weeklycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/monthlycounter.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/counter/sqlite/noresetcounter.conf

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/cui/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/cui/sqlite/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool/sqlite/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/ippool-dhcp/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/ippool-dhcp/sqlite/schema.sql

%dir %attr(750,root,radiusd) /etc/raddb/mods-config/sql/main/sqlite
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/sqlite/queries.conf
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/sqlite/schema.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/sqlite/process-radacct-schema.sql
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/sqlite/process-radacct-close-after-reload.pl
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-config/sql/main/sqlite/process-radacct-new-data-usage-period.sh

%{_libdir}/freeradius/rlm_sql_sqlite.so

%files ldap
%{_libdir}/freeradius/rlm_ldap.so
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/ldap

%files unixODBC
%{_libdir}/freeradius/rlm_sql_unixodbc.so

%files rest
%{_libdir}/freeradius/rlm_rest.so
%attr(640,root,radiusd) %config(noreplace) /etc/raddb/mods-available/rest

%changelog
* Wed Oct 18 2023 Archana Choudhary <archana1@microsoft.com> - 3.2.3-2
- Correct unavailable sysusers_create_compat macro to available sysusers_create_package macro
- Add runtime requirement for utils subpackage
- Update build requirement for postgresql subpackage
- Disable generation of debuginfo package as its files conflict with filsystem package

* Tue Sep 05 2023 Archana Choudhary <archana1@microsoft.com> - 3.2.3-1
- Upgrade to 3.2.3
- Address CVE-2022-41860, CVE-2022-41861
- Update Patch2 & Patch4
- Add Patch6 to address build error
- Add Source105 for user management during installation
- License verified

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.21-9
- Making binaries paths compatible with CBL-Mariner's paths.

* Fri Feb 05 2021 Henry Li <lihl@microsoft.com> - 3.0.21-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove %%{EPOCH}
- Remove python2-freeradius

* Wed May 13 2020 Alexander Scheel <ascheel@redhat.com> - 3.0.21-7
- Fix certificate permissions after make-based generation
  Resolves: bz#1835249

* Wed May 13 2020 Alexander Scheel <ascheel@redhat.com> - 3.0.21-2
- Fix certificate generation
  Resolves: bz#1835249

* Wed Apr 01 2020 Alexander Scheel <ascheel@redhat.com> - 3.0.21-1
- Rebased to 3.0.21
  Resolves: bz#1816745

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 11 2020 Paul Wouters <pwouters@redhat.com> - 3.0.20-2
- fixup tmpfile to use /run instead of /var/run

* Fri Nov 15 2019 Alexander Scheel <ascheel@redhat.com> - 3.0.20-1
- Rebased to 3.0.20
  Resolves: bz#1772710
- Introduced new rlm_python3 module

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.19-4
- Perl 5.30 rebuild

* Wed May 08 2019 Alexander Scheel <ascheel@redhat.com> - 3.0.19-3
- Update boostrap to change ownership of all certificates to root:radiusd

* Wed May 08 2019 Alexander Scheel <ascheel@redhat.com> - 3.0.19-2
- Updated crypto-policies patch
- Updated /etc/raddb/certs/bootstrap to only create certificates if missing: bz#1705165 bz#1672284
- Updated logrotate definitions to run as radiusd:radiusd: bz#1705343
- Drop python2 package on Fedora 31+
- Add database dependencies: bz#1658697
- Don't generate certificate during build

* Wed Apr 10 2019 Alexander Scheel <ascheel@redhat.com> - 3.0.19-1
- Rebased to 3.0.19

* Wed Mar 06 2019 Alexander Scheel <ascheel@redhat.com> - 3.0.18-1
- Rebased to 3.0.18

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.17-6
- Rebuild for readline 8.0

* Tue Feb 05 2019 Alexander Scheel <ascheel@redhat.com> - 3.0.17-5
- Unit file generates certificates if not present.
  Resolves: bz#1672284

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 3.0.17-3
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Dec 14 2018 Alexander Scheel <ascheel@redhat.com> - 3.0.17-2
- Updates radiusd.service to start after network-online.target
  Resolves: bz#1637275

* Thu Oct 18 2018 Alexander Scheel <ascheel@redhat.com> - 3.0.17-1
- Update to FreeRADIUS server version 3.0.17
- Adds OpenSSL HMAC patches from upstream (unreleased)
- Adds Python2 shebang patches from upstream (unreleased)

* Mon Sep 17 2018 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.15-18
- Actually apply patches added previously.
  Related: Bug#1611286 Man page scan results for freeradius

* Fri Sep 14 2018 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.15-17
- Fix a few minor manpage issues.
  Resolves: Bug#1611286 Man page scan results for freeradius

* Fri Sep 07 2018 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.15-16
- Add make to BuildRequires and Requires(post) to fix build and certificate
  generation on install.
  Resolves: Bug#1574783 Installing freeradius without make results in an
                        unworkable default configuration

* Tue Sep 04 2018 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.15-15
- Add gcc to BuildRequires.
  Resolves: Bug#1622470 FTBFS freeradius (rawhide)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.15-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.15-13
- Perl 5.28 rebuild

* Tue Mar 06 2018 Björn Esser <besser82@fedoraproject.org> - 3.0.15-12
- Rebuilt for libjson-c.so.4 (json-c v0.13.1)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.15-11
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3.0.15-9
- Rebuilt for switch to libxcrypt

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.0.15-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Dec 10 2017 Björn Esser <besser82@fedoraproject.org> - 3.0.15-7
- Rebuilt for libjson-c.so.3

* Thu Oct 26 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.15-6
- Use mariadb-connector-c-devel instead of mysql-devel or mariadb-devel
  Resolves: Bug#1493904 Use mariadb-connector-c-devel instead of mysql-devel
                        or mariadb-devel

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.15-5
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.0.15-4
- Python 2 binary package renamed to python2-freeradius
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.15-1
- Upgrade to upstream v3.0.15 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).
- Resolves: Bug#1471848 CVE-2017-10978 freeradius: Out-of-bounds read/write
                        due to improper output buffer size check in
                        make_secret()
- Resolves: Bug#1471860 CVE-2017-10983 freeradius: Out-of-bounds read in
                        fr_dhcp_decode() when decoding option 63
- Resolves: Bug#1471861 CVE-2017-10984 freeradius: Out-of-bounds write in
                        data2vp_wimax()
- Resolves: Bug#1471863 CVE-2017-10985 freeradius: Infinite loop and memory
                        exhaustion with 'concat' attributes
- Resolves: Bug#1471864 CVE-2017-10986 freeradius: Infinite read in
                        dhcp_attr2vp()
- Resolves: Bug#1471865 CVE-2017-10987 freeradius: Buffer over-read in
                        fr_dhcp_decode_suboptions()
- Resolves: Bug#1456220 freeradius-3.0.15 is available

* Thu Jul 13 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.14-3
- Rebuild with updated MySQL client library

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.14-2
- Perl 5.26 rebuild

* Tue May 30 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.14-1
- Upgrade to upstream v3.0.14 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).
- Fix TLS resumption authentication bypass (CVE-2017-9148)

* Wed Mar 29 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.13-3
- Explicitly disable rlm_cache_memcached to avoid error when the module's
  dependencies are installed, and it is built, but not packaged.
- Prevent segfaults by adding a missing handling of connection errors in
  rlm_ldap.
- Make radtest use Cleartext-Password for EAP, fixing its support for eap-md5.

* Wed Mar 15 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.13-2
- Fix permissions of default key files in raddb/certs.
- Require OpenSSL version we built with, or newer, to avoid startup failures
  due to runtime OpenSSL version checks.
  Resolves: Bug#1299388
- Fix some issues found with static analyzers.

* Tue Mar 07 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.13-1
- Upgrade to upstream v3.0.13 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).

* Tue Feb 21 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.12-3
- Do not fail logrotate if radiusd is not running.
- Fix output to log file specified with -l option.
- Fix long hostnames interpreted as IP addresses.
- Avoid clashes with libtool library symbols.
- Remove mentions of Auth-Type = System from docs.
- Improve ip/v4/v6/addr documentation.

* Mon Feb 20 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.12-2
- Fix three cases of comparing pointers to zero characters
- Support OpenSSL v1.1.0
  Resolves: Bug#1385588

* Fri Feb 17 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.12-1
- Upgrade to upstream v3.0.12 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).

* Fri Feb 17 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.11-7
- Make sure FreeRADIUS starts after IPA, directory, and Kerberos servers
- Don't rotate radutmp, as it's not a log file
- Logrotate with "systemctl" instead of "service"
- Remove executable bits from "radiusd.service"

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.11-5
- Move tmpfiles.d config to %%{_tmpfilesdir}
- Install license files as %%license

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.0.11-4
- Rebuild for readline 7.x

* Mon Sep 26 2016 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.11-3
- Switch default configuration to use system's crypto policy.
  Resolves: Bug#1179224

* Tue May 17 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.11-2
- Perl 5.24 rebuild

* Tue Apr 12 2016 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.11-1
- Upgrade to upstream v3.0.10 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 09 2015 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.10-1
- Upgrade to upstream v3.0.10 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).
  Related: Bug#1133959
- Remove rlm_eap_tnc support as the required package "tncfhh" was retired.

* Wed Aug 19 2015 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.9-1
- Upgrade to upstream v3.0.9 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).
  Resolves: Bug#1133959

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.8-2
- Perl 5.22 rebuild

* Tue Apr 28 2015 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.8-1
- Upgrade to upstream v3.0.7 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).
  Related: Bug#1133959

* Thu Mar 19 2015 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.7-1
- Upgrade to upstream v3.0.7 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).
  Resolves: Bug#1133959
- Add freeradius-rest package containing rlm_rest module.
  Resolves: Bug#1196276

* Fri Feb 13 2015 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.4-4
- Bump release number to catch up with Fedora 21.

* Mon Jan 19 2015 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.4-3
- Fix OpenSSL version parsing when checking for compatibility at run time.
  Resolves: Bug#1173821
- Don't remove backslash from unknown escape sequences in LDAP values.
  Resolves: Bug#1173526
- Improve dhcpclient and rad_counter online help.
  Resolves: Bug#1146966
- raddb: Move trigger.conf INCLUDE before modules, making it easier to refer
  to trigger variables from module configurations.
  Resolves: Bug#1155961
- Fix ipaddr option fallback onto ipv6.
  Resolves: Bug#1168868
- raddb: Comment on ipaddr/ipv4addr/ipv6addr use.
  Resolves: Bug#1168247
- Disable rlm_rest building explicitly to avoid unintended builds on some
  architectures breaking RPM build.
  Resolves: Bug#1162156
- Add -D option support to dhcpclient.
  Related: Bug#1146939
- Don't install rbmonkey - a test tool only useful to developers.
  Related: Bug#1146966
- Update clients(5) man page
  Resolves: Bug#1147464
- Fix possible group info corruption/segfault in rlm_unix' fr_getgrnam.
- Fix file configuration item parsing.
- Fix a number of trigger issues.
  Resolves: Bug#1110407 radiusd doesn't send snmp trap after "radmin -e 'hup
                        files'"
  Resolves: Bug#1110414 radiusd doesn't send snmp trap when sql connection is
                        opened,closed or fail
  Resolves: Bug#1110186 radiusd doesn't send snmp trap when ldap connection
                        fails/opens/closes
  Resolves: Bug#1109164 snmp trap messages send by radiusd are inconsistent
                        and incomplete
- Fix two omissions from radtest manpage.
  Resolves: Bug#1146898 'eap-md5' value is missing in -t option in SYNOPSIS
                        of radtest man page
  Resolves: Bug#1114669 Missing -P option in radtest manpage
- Disable OpenSSL version checking to avoid the need to edit radiusd.conf to
  confirm heartbleed is fixed.
  Resolves: Bug#1155070 FreeRADIUS doesn't start after upgrade due to failing
                        OpenSSL version check

* Mon Oct  6 2014 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.4-2
- Fix abort on home server triggers.
- Fix segfault upon example.pl read failure.
- Fix example.pl permissions.
- Fix integer handling in various cases.
- Fix dhcpclient's dictionary.dhcp loading.

* Mon Sep 15 2014 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.4-1
- Upgrade to upstream 3.0.4 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).
- Resolves: Bug#1099620

* Tue Sep 09 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.4-0.2.rc2
- Perl 5.20 mass

* Mon Sep  8 2014 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.4-0.1.rc2
- Upgrade to upstream 3.0.4-rc2 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.0.3-5
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.3-2
- Add explicit dependency on OpenSSL package with fixed CVE-2014-0160
  (Heartbleed bug).
- Add confirmation of CVE-2014-0160 being fixed in OpenSSL to radiusd.conf.

* Wed May 14 2014 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.3-1
- Upgrade to upstream 3.0.3 release.
  See upstream ChangeLog for details (in freeradius-doc subpackage).
- Minor configuration parsing change: "Double-escaping of characters in Perl,
  and octal characters has been fixed. If your configuration has text like
  "\\000", you will need to remove one backslash."
- Additionally includes post-release fixes for:
  * case-insensitive matching in compiled regular expressions not working,
  * upstream issue #634 "3.0.3 SIGSEGV on config parse",
  * upstream issue #635 "3.0.x - rlm_perl - strings are still
    escaped when passed to perl from FreeRADIUS",
  * upstream issue #639 "foreach may cause ABORT".
- Fixes bugs 1097266 1070447

* Wed May  7 2014 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.2-1
- Upgrade to upstream 3.0.2 release, configuration compatible with 3.0.1.
  See upstream ChangeLog for details (in freeradius-doc subpackage)
- Fixes bugs 1058884 1061408 1070447 1079500

* Mon Feb 24 2014 Nikolai Kondrashov <Nikolai.Kondrashov@redhat.com> - 3.0.1-4
- Fix CVE-2014-2015 "freeradius: stack-based buffer overflow flaw in rlm_pap
  module"
- resolves: bug#1066984 (fedora 1066763)

* Fri Feb 21 2014 John Dennis <jdennis@redhat.com> - 3.0.1-3
- resolves: bug#1068798 (fedora 1068795)
  rlm_perl attribute values truncated

* Sun Jan 19 2014 John Dennis <jdennis@redhat.com> - 3.0.1-2
- resolves: bug#1055073 (fedora 1055072)
  rlm_ippool; bad config file attribute and fails to send reply attributes
- resolves: bug#1055567 (fedora 1056227)
  bad mysql sql syntax
- change CFLAGS -imacros to -include to address gcc/gdb bug 1004526
  where gdb will not display source information, only <command-line>

* Tue Jan 14 2014 John Dennis <jdennis@redhat.com> - 3.0.1-1
- Upgrade to upstream 3.0.1 release, full config compatible with 3.0.0.
  This is a roll-up of all upstream bugs fixes found in 3.0.0
  See upstream ChangeLog for details (in freeradius-doc subpackage)
- fixes bugs 1053020 1044747 1048474 1043036

* Tue Nov 26 2013 John Dennis <jdennis@redhat.com> - 3.0.0-4
- resolves: bug#1031035
  remove radeapclient man page,
  upstream no longer supports radeapclient, use eapol_test instead
- resolves: bug#1031061
  rlm_eap_leap memory corruption, see freeradius-rlm_leap.patch
- move man pages for utils into utils subpackage from doc subpackage
- fix HAVE_EC_CRYPTO test to include f20
- add new directory /var/run/radiusd/tmp
  update mods-available/eap so tls-common.verify.tmpdir to point to it

* Wed Nov 13 2013 John Dennis <jdennis@redhat.com> - 3.0.0-3
- resolves: bug#1029941
  PW_TYPE_BOOLEAN config item should be declared int, not bool

* Mon Oct 28 2013 John Dennis <jdennis@redhat.com> - 3.0.0-2
- resolves: bug#1024119
  tncfhh-devel is now available in RHEL-7, remove conditional BuildRequires

* Sun Oct 13 2013 John Dennis <jdennis@redhat.com> - 3.0.0-1
- Offical 3.0 gold release from upstream
- resolves: bug#1016873
- resolves: bug#891297

* Sun Sep  8 2013 John Dennis <jdennis@redhat.com> - 3.0.0-0.4.rc1
- upgrade to second 3.0 release candidate rc1

* Mon Aug 26 2013 John Dennis <jdennis@redhat.com> - 3.0.0-0.3.rc0
- add missingok config attribute to /etc/raddb/sites-enabled/* symlinks

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 3.0.0-0.2.rc0
- Perl 5.18 rebuild

* Fri Jul 26 2013 Ville Skyttä <ville.skytta@iki.fi> - 3.0.0-0.1.rc0
- Install docs to %%{_pkgdocdir} where available.

* Mon Jul 22 2013 John Dennis <jdennis@redhat.com> - 3.0.0-0.rc0
- Upgrade to new upstream major version release

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.2.0-7
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 14 2012 John Dennis <jdennis@redhat.com> - 2.2.0-5
- resolves: bug#850119 - Introduce new systemd-rpm macros (>= F18)

* Thu Dec 13 2012 John Dennis <jdennis@redhat.com> - 2.2.0-4
- add compile option -fno-strict-aliasing

* Thu Dec 13 2012 John Dennis <jdennis@redhat.com> - 2.2.0-3
- specify homedir (/var/lib/radiusd) for radiusd user in useradd,
  do not permit useradd to default the homedir.

* Wed Dec 12 2012 John Dennis <jdennis@redhat.com> - 2.2.0-2
- add security options to compiler/linker

* Mon Dec 10 2012 John Dennis <jdennis@redhat.com> - 2.2.0-1
- resolves: bug#876564 - fails to start without freeradius-mysql
- use upstream version of freeradius-exclude-config-file.patch

* Wed Oct  3 2012 John Dennis <jdennis@redhat.com> - 2.2.0-0
- Add new patch to avoid reading .rpmnew, .rpmsave and other invalid
  files when loading config files
- Upgrade to new 2.2.0 upstream release
- Upstream changelog for 2.1.12:
  Feature improvements
  * 100% configuration file compatible with 2.1.x.
    The only fix needed is to disallow "hashsize=0" for rlm_passwd
  * Update Aruba, Alcatel Lucent, APC, BT, PaloAlto, Pureware,
    Redback, and Mikrotik dictionaries
  * Switch to using SHA1 for certificate digests instead of MD5.
    See raddb/certs/*.cnf
  * Added copyright statements to the dictionaries, so that we know
    when people are using them.
  * Better documentation for radrelay and detail file writer.
    See raddb/modules/radrelay and raddb/radrelay.conf
  * Added TLS-Cert-Subject-Alt-Name-Email from patch by Luke Howard
  * Added -F <file> to radwho
  * Added query timeouts to MySQL driver.  Patch from Brian De Wolf.
  * Add /etc/default/freeradius to debian package.
    Patch from Matthew Newton
  * Finalize DHCP and DHCP relay code.  It should now work everywhere.
    See raddb/sites-available/dhcp, src_ipaddr and src_interface.
  * DHCP capabilitiies are now compiled in by default.
    It runs as a DHCP server ONLY when manually enabled.
  * Added one letter expansions: %%G - request minute and %%I request
    ID.
  * Added script to convert ISC DHCP lease files to SQL pools.
    See scripts/isc2ippool.pl
  * Added rlm_cache to cache arbitrary attributes.
  * Added max_use to rlm_ldap to force connection to be re-established
    after a given number of queries.
  * Added configtest option to Debian init scripts, and automatic
    config test on restart.
  * Added cache config item to rlm_krb5. When set to "no" ticket
    caching is disabled which may increase performance.
  Bug fixes
  * Fix CVE-2012-3547.  All users of 2.1.10, 2.1.11, 2.1.12,
    and 802.1X should upgrade immediately.
  * Fix typo in detail file writer, to skip writing if the packet
    was read from this detail file.
  * Free cached replies when closing resumed SSL sessions.
  * Fix a number of issues found by Coverity.
  * Fix memory leak and race condition in the EAP-TLS session cache.
    Thanks to Phil Mayers for tracking down OpenSSL APIs.
  * Restrict ATTRIBUTE names to character sets that make sense.
  * Fix EAP-TLS session Id length so that OpenSSL doesn't get
    excited.
  * Fix SQL IPPool logic for non-timer attributes.  Closes bug #181
  * Change some informational messages to DEBUG rather than error.
  * Portability fixes for FreeBSD.  Closes bug #177
  * A much better fix for the _lt__PROGRAM__LTX_preloaded_symbols
    nonsense.
  * Safely handle extremely long lines in conf file variable expansion
  * Fix for Debian bug #606450
  * Mutex lock around rlm_perl Clone routines. Patch from Eike Dehling
  * The passwd module no longer permits "hashsize = 0".  Setting that
    is pointless for a host of reasons.  It will also break the server.
  * Fix proxied inner-tunnel packets sometimes having zero authentication
    vector.  Found by Brian Julin.
  * Added $(EXEEXT) to Makefiles for portability.  Closes bug #188.
  * Fix minor build issue which would cause rlm_eap to be built twice.
  * When using "status_check=request" for a home server, the username
    and password must be specified, or the server will not start.
  * EAP-SIM now calculates keys from the SIM identity, not from the
    EAP-Identity.  Changing the EAP type via NAK may result in
    identities changing.  Bug reported by Microsoft EAP team.
  * Use home server src_ipaddr when sending Status-Server packets
  * Decrypt encrypted ERX attributes in CoA packets.
  * Fix registration of internal xlat's so %%{mschap:...} doesn't
    disappear after a HUP.
  * Can now reference tagged attributes in expansions.
    e.g. %%{Tunnel-Type:1} and %%{Tunnel-Type:1[0]} now work.
  * Correct calculation of Message-Authenticator for CoA and Disconnect
    replies.  Patch from Jouni Malinen
  * Install rad_counter, for managing rlm_counter files.
  * Add unique index constraint to all SQL flavours so that alternate
    queries work correctly.
  * The TTLS diameter decoder is now more lenient.  It ignores
    unknown attributes, instead of rejecting the TTLS session.
  * Use "globfree" in detail file reader.  Prevents very slow leak.
    Closes bug #207.
  * Operator =~ shouldn't copy the attribute, like :=.  It should
    instead behave more like ==.
  * Build main Debian package without SQL dependencies
  * Use max_queue_size in threading code
  * Update permissions in raddb/sql/postgresql/admin.sql
  * Added OpenSSL_add_all_algorithms() to fix issues where OpenSSL
    wouldn't use methods it knew about.
  * Add more sanity checks in dynamic_clients code so the server won't
    crash if it attempts to load a badly formated client definition.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 2.1.12-9
- Perl 5.16 rebuild

* Tue May 15 2012 John Dennis <jdennis@redhat.com> - 2.1.12-8
- resolves: bug#821407 - openssl dependency

* Sat Apr 14 2012 John Dennis <jdennis@redhat.com> - 2.1.12-7
- resolves: bug#810605 Segfault with freeradius-perl threading

* Tue Feb 28 2012 John Dennis <jdennis@redhat.com> - 2.1.12-6
  Fixing bugs in RHEL6 rebase, applying fixes here as well
  resolves: bug#700870 freeradius not compiled with --with-udpfromto
  resolves: bug#753764 shadow password expiration does not work
  resolves: bug#712803 radtest script is not working with eap-md5 option
  resolves: bug#690756 errors in raddb/sql/postgresql/admin.sql template

* Tue Feb  7 2012 John Dennis <jdennis@redhat.com> - 2.1.12-5
- resolves: bug#781877 (from RHEL5) rlm_dbm_parse man page misspelled
- resolves: bug#760193 (from RHEL5) radtest PPPhint option is not parsed properly

* Sun Jan 15 2012 John Dennis <jdennis@redhat.com> - 2.1.12-4
- resolves: bug#781744
  systemd service file incorrectly listed pid file as
  /var/run/radiusd/radiusd which it should have been
  /var/run/radiusd/radiusd.pid

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 31 2011 John Dennis <jdennis@redhat.com> - 2.1.12-2
- rename /etc/tmpfiles.d/freeradius.conf to /etc/tmpfiles.d/radiusd.conf
  remove config(noreplace) because it must match files section and
  permissions differ between versions.
- fixup macro usage for /var/run & /var/lib

* Mon Oct  3 2011 John Dennis <jdennis@redhat.com> - 2.1.12-1
- Upgrade to latest upstream release: 2.1.12
- Upstream changelog for 2.1.12:
  Feature improvements
  * Updates to dictionary.erx, dictionary.siemens, dictionary.starent,
    dictionary.starent.vsa1, dictionary.zyxel, added dictionary.symbol
  * Added support for PCRE from Phil Mayers
  * Configurable file permission in rlm_linelog
  * Added "relaxed" option to rlm_attr_filter.  This copies attributes
    if at least one match occurred.
  * Added documentation on dynamic clients.
    See raddb/modules/dynamic_clients.
  * Added support for elliptical curve cryptography.
    See ecdh_curve in raddb/eap.conf.
  * Added support for 802.1X MIBs in checkrad
  * Added support for %%{rand:...}, which generates a uniformly
    distributed number between 0 and the number you specify.
  * Created "man" pages for all installed commands, and documented
    options for all commands.  Patch from John Dennis.
  * Allow radsniff to decode encrypted VSAs and CoA packets.
    Patch from Bjorn Mork.
  * Always send Message-Authenticator in radtest. Patch from John Dennis.
    radclient continues to be more flexible.
  * Updated Oracle schema and queries
  * Added SecurID module.  See src/modules/rlm_securid/README
  Bug fixes
  * Fix memory leak in rlm_detail
  * Fix "failed to insert event"
  * Allow virtual servers to be reloaded on HUP.
    It no longer complains about duplicate virtual servers.
  * Fix %%{string:...} expansion
  * Fix "server closed socket" loop in radmin
  * Set ownership of control socket when starting up
  * Always allow root to connect to control socket, even if
    "uid" is set.  They're root.  They can already do anything.
  * Save all attributes in Access-Accept when proxying inner-tunnel
    EAP-MSCHAPv2
  * Fixes for DHCP relaying.
  * Check certificate validity when using OCSP.
  * Updated Oracle "configure" script
  * Fixed typos in dictionary.alvarion
  * WARNING on potential proxy loop.
  * Be more aggressive about clearing old requests from the
    internal queue
  * Don't open network sockets when using -C

* Wed Sep 21 2011 Tom Callaway <spot@fedoraproject.org> - 2.1.11-7
- restore defattr customization in the main package

* Fri Sep  9 2011 Tom Callaway <spot@fedoraproject.org> - 2.1.11-6
- add missing systemd scriptlets

* Thu Sep  8 2011 Tom Callaway <spot@fedoraproject.org> - 2.1.11-5
- convert to systemd

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 2.1.11-4
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 2.1.11-3
- Perl mass rebuild

* Thu Jun 23 2011 John Dennis <jdennis@redhat.com> - 2.1.11-2
- reload the server (i.e. HUP) after logrotate

* Wed Jun 22 2011 John Dennis <jdennis@redhat.com> - 2.1.11-1
- Upgrade to latest upstream release: 2.1.11
- Remove the following two patches as upstream has incorporated them:
    freeradius-radtest-ipv6.patch
    freeradius-lt-dladvise.patch
- Upstream changelog for 2.1.11:
  Feature improvements
  * Added doc/rfc/rfc6158.txt: RADIUS Design Guidelines.
    All vendors need to read it and follow its directions.
  * Microsoft SoH support for PEAP from Phil Mayers.
    See doc/SoH.txt
  * Certificate "bootstrap" script now checks for certificate expiry.
    See comments in raddb/eap.conf, and then "make_cert_command".
  * Support for dynamic expansion of EAP-GTC challenges.
    Patch from Alexander Clouter.
  * OCSP support from Alex Bergmann.  See raddb/eap.conf, "ocsp"
    section.
  * Updated dictionary.huawei, dictionary.3gpp, dictionary.3gpp3.
  * Added dictionary.eltex, dictionary.motorola, and dictionary.ukerna.
  * Experimental redis support from Gabriel Blanchard.
    See raddb/modules/redis and raddb/modules/rediswho
  * Add "key" to rlm_fastusers.  Closes bug #126.
  * Added scripts/radtee from original software at
    http://horde.net/~jwm/software/misc/comparison-tee
  * Updated radmin "man" page for new commands.
  * radsniff now prints the hex decoding of the packet (-x -x -x)
  * mschap module now reloads its configuration on HUP
  * Added experimental "replicate" module.  See raddb/modules/replicate
  * Policy "foo" can now refer to module "foo".  This lets you
    over-ride the behavior of a module.
  * Policy "foo.authorize" can now over-ride the behavior of module
    "foo", "authorize" method.
  * Produce errors in more situations when the configuration files
    have invalid syntax.
  Bug fixes
  * Ignore pre/post-proxy sections if proxying is disabled
  * Add configure checks for pcap_fopen*.
  * Fix call to otp_write in rlm_otp
  * Fix issue with Access-Challenge checking from 2.1.10, when the
    debug flag was set after server startup.  Closes #116 and #117.
  * Fix typo in zombie period start time.
  * Fix leak in src/main/valuepair.c.  Patch from James Ballantine.
  * Allow radtest to use spaces in shared secret.
    Patch from Cedric Carree.
  * Remove extra calls to HMAC_CTX_init() in rlm_wimax, fixing leak.
    Patch from James Ballantine.
  * Remove MN-FA key generation.  The NAS does this, not AAA.
    Patch from Ben Weichman.
  * Include dictionary.mikrotik by default.  Closes bug #121.
  * Add group membership query to MS-SQL examples.  Closes bug #120.
  * Don't cast NAS-Port to integer in Postgresql queries.
    Closes bug #112.
  * Fixes for libtool and autoconf from Sam Hartman.
  * radsniff should read the dictionaries in more situations.
  * Use fnmatch to check for detail file reader==writer.
    Closes bug #128.
  * Check for short writes (i.e. disk full) in rlm_detail.
    Closes bug #130.  Patches and testing from John Morrissey.
  * Fix typo in src/lib/token.c.  Closes bug #124
  * Allow workstation trust accounts to use MS-CHAP.
    Closes bug #123.
  * Assigning foo=`/bin/echo hello` now produces a syntax error
    if it is done outside of an "update" section.
  * Fix "too many open file descriptors" problem when using
    "verify client" in eap.conf.
  * Many fixes to dialup_admin for PHP5, by Stefan Winter.
  * Allow preprocess module to have "hints = " and "huntgroups =",
    which allows them to be empty or non-existent.
  * Renamed "php3" files to "php" in dialup_admin/
  * Produce error when sub-TLVs are used in a dictionary.  They are
    supported only in the "master" branch, and not in 2.1.x.
  * Minor fix in dictionary.redback.  Closes bug #138.
  * Fixed MySQL "NULL" issues in ippool.conf.  Closes bug #129.
  * Fix to Access-Challenge warning from Ken-ichirou Matsuzawa.
    Closes bug #118.
  * DHCP fixes to send unicast packets in more situations.
  * Fix to udpfromto, to enable it to work on IPv6 networks.
  * Fixes to the Oracle accounting_onoff_query.
  * When using both IPv4 and IPv6 home servers, ensure that we use the
    correct local socket for proxying.  Closes bug #143.
  * Suppress messages when thread pool is nearly full, all threads
    are busy, and we can't create new threads.
  * IPv6 is now enabled for udpfromto.  Closes bug #141
  * Make sqlippool query buffer the same size as sql module.
    Closes bug #139.
  * Make Coa / Disconnect proxying work again.
  * Configure scripts for rlm_caching from Nathaniel McCallum
  * src/lib/dhcp.c and src/include/libradius.h are LGPL, not GPL.
  * Updated password routines to use time-insensitive comparisons.
    This prevents timing attacks (though none are known).
  * Allow sqlite module to do normal SELECT queries.
  * rlm_wimax now has a configure script
  * Moved Ascend, USR, and Motorola "illegal" dictionaries to separate
    files.  See share/dictionary for explanations.
  * Check for duplicate module definitions in the modules{} section,
    and refuse to start if duplicates are found.
  * Check for duplicate virtual servers, and refuse to start if
    duplicates are found.
  * Don't use udpfromto if source is INADDR_ANY.  Closes bug #148.
  * Check pre-conditions before running radmin "inject file".
  * Don't over-ride "no match" with "match" for regexes.
    Closes bug #152.
  * Make retry and error message configurable in mschap.
    See raddb/modules/mschap
  * Allow EAP-MSCHAPv2 to send error message to client.  This change
    allows some clients to prompt the user for a new password.
    See raddb/eap.conf, mschapv2 section, "send_error".
  * Load the default virtual server before any others.
    This matches what users expect, and reduces confusion.
  * Fix configure checks for udpfromto.  Fixes Debian bug #606866
  * Definitive fix for bug #35, where the server could crash under
    certain loads.  Changes src/lib/packet.c to use RB trees.
  * Updated "configure" checks to allow IPv6 udpfromto on Linux.
  * SQL module now returns NOOP if the accounting start/interim/stop
    queries don't do anything.
  * Allow %%{outer.control: ... } in string expansions
  * home_server coa config now matches raddb/proxy.conf
  * Never send a reply to a DHCP Release.

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.1.10-8
- Perl mass rebuild

* Wed Mar 23 2011 John Dennis <jdennis@redhat.com> - 2.1.10-7
- Resolves: #689045 Using rlm_perl cause radiusd failed to start
  Fix configure typo which caused lt_dladvise_* functions to be skipped.
  run autogen.sh because HAVE_LT_DLADVISE_INIT isn't in src/main/autogen.h
  Implemented by: freeradius-lt-dladvise.patch

* Wed Mar 23 2011 John Dennis <jdennis@redhat.com> - 2.1.10-6
- Resolves: #599528 - make radtest IPv6 compatible

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 2.1.10-5
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan  1 2011 John Dennis <jdennis@redhat.com> - 2.1.10-3
- bug 666589 - removing freeradius from system does not delete the user "radiusd"
  fix scriptlet argument testing, simplify always exiting with zero

* Thu Dec 30 2010 John Dennis <jdennis@redhat.com> - 2.1.10-2
- rebuild for new MySQL libs

* Tue Oct 19 2010 John Dennis <jdennis@redhat.com> - 2.1.10-1
  Feature improvements
  * Install the "radcrypt" program.
  * Enable radclient to send requests containing MS-CHAPv1
    Send packets with: MS-CHAP-Password = "password".  It will
    be automatically converted to the correct MS-CHAP attributes.
  * Added "-t" command-line option to radtest.  You can use "-t pap",
   "-t chap", "-t mschap", or "-t eap-md5".  The default is "-t pap"
  * Make the "inner-tunnel" virtual server listen on 127.0.0.1:18120
    This change and the previous one makes PEAP testing much easier.
  * Added more documentation and examples for the "passwd" module.
  * Added dictionaries for RFC 5607 and RFC 5904.
  * Added note in proxy.conf that we recommend setting
    "require_message_authenticator = yes" for all home servers.
  * Added example of second "files" configuration, with documentation.
    This shows how and where to use two instances of a module.
  * Updated radsniff to have it write pcap files, too.  See '-w'.
  * Print out large WARNING message if we send an Access-Challenge
    for EAP, and receive no follow-up messages from the client.
  * Added Cached-Session-Policy for EAP session resumption.  See
    raddb/eap.conf.
  * Added support for TLS-Cert-* attributes. For details, see
    raddb/sites-available/default, "post-auth" section.
  * Added sample raddb/modules/{opendirectory,dynamic_clients}
  * Updated Cisco and Huawei, HP, Redback, and ERX dictionaries.
  * Added RFCs 5607, 5904, and 5997.
  * For EAP-TLS, client certificates can now be validated using an
    external command.  See eap.conf, "validate" subsection of "tls".
  * Made rlm_pap aware of {nthash} prefix, for compatibility with
    legacy RADIUS systems.
  * Add Module-Failure-Message for mschap module (ntlm_auth)
  * made rlm_sql_sqlite database configurable.  Use "filename"
    in sql{} section.
  * Added %%{tolower: ...string ... }, which returns the lowercase
    version of the string.  Also added %%{toupper: ... } for uppercase.
  Bug fixes
  * Fix endless loop when there are multiple sub-options for
    DHCP option 82.
  * More debug output when sending / receiving DHCP packets.
  * EAP-MSCHAPv2 should return the MPPE keys when used outside
    of a TLS tunnel.  This is needed for IKE.
  * Added SSL "no ticket" option to prevent SSL from creating sessions
    without IDs.  We need the IDs, so this option should be set.
  * Fix proxying of packets from inside a TTLS/PEAP tunnel.
    Closes bug #25.
  * Allow IPv6 address attributes to be created from domain names
    Closes bug #82.
  * Set the string length to the correct value when parsing double
    quotes.  Closes bug #88.
  * No longer look users up in /etc/passwd in the default configuration.
    This can be reverted by enabling "unix" in the "authorize" section.
  * More #ifdef's to enable building on systems without certain
    features.
  * Fixed SQL-Group comparison to register only if the group
    query is defined.
  * Fixed SQL-Group comparison to register <instance>-SQL-Group,
    just like rlm_ldap.  This lets you have multiple SQL group checks.
  * Fix scanning of octal numbers in "unlang".  Closes bug #89.
  * Be less aggressive about freeing "stuck" requests.  Closes bug #35.
  * Fix example in "originate-coa" to refer to the correct packet.
  * Change default timeout for dynamic clients to 1 hour, not 1 day.
  * Allow passwd module to map IP addresses, too.
  * Allow passwd module to be used for CoA packets
  * Put boot filename into DHCP header when DHCP-Boot-Filename
    is specified.
  * raddb/certs/Makefile no longer has certs depend on index.txt and
     serial.  Closes bug #64.
  * Ignore NULL errorcode in PostgreSQL client.  Closes bug #39
  * Made Exec-Program and Exec-Program-Wait work in accounting
    section again.  See sites-available/default.
  * Fix long-standing memory leak in esoteric conditions.  Found
    by Jerry Nichols.
  * Added "Password-With-Header == userPassword" to raddb/ldap.attrmap
    This will automatically convert more passwords.
  * Updated rlm_pap to decode Password-With-Header, if it was base64
    encoded, and to treat the contents as potentially binary data.
  * Fix Novell eDir code to use the right function parameters.
    Closes bug #86.
  * Allow spaces to be escaped when executing external programs.
    Closes bug #93.
  * Be less restrictive about checking permissions on control socket.
    If we're root, allow connecting to a non-root socket.
  * Remove control socket on normal server exit.  If the server isn't
    running, the control socket should not exist.
  * Use MS-CHAP-User-Name as Name field from EAP-MSCHAPv2 for MS-CHAP
    calculations.  It *MAY* be different (upper / lower case) from
    the User-Name attribute.  Closes bug #17.
  * If the EAP-TLS methods have problems, more SSL errors are now
    available in the Module-Failure-Message attribute.
  * Update Oracle configure scripts.  Closes bug #57.
  * Added text to DESC fields of doc/examples/openldap.schema
  * Updated more documentation to use "Restructured Text" format.
    Thanks to James Lockie.
  * Fixed typos in raddb/sql/mssql/dialup.conf.  Closes bug #11.
  * Return error for potential proxy loops when using "-XC"
  * Produce better error messages when slow databases block
    the server.
  * Added notes on DHCP broadcast packets for FreeBSD.
  * Fixed crash when parsing some date strings.  Closes bug #98
  * Improperly formatted Attributes are now printed as "Attr-##".
    If they are not correct, they should not use the dictionary name.
  * Fix rlm_digest to be check the format of the Digest attributes,
    and return "noop" rather than "fail" if they're not right.
  * Enable "digest" in raddb/sites-available/default.  This change
    enables digest authentication to work "out of the box".
  * Be less aggressive about marking home servers as zombie.
    If they are responding to some packets, they are still alive.
  * Added Packet-Transmit-Counter, to track detail file retransmits.
    Closes bug #13.
  * Added configure check for lt_dladvise_init().  If it exists, then
    using it solves some issues related to libraries loading libraries.
  * Added indexes to the MySQL IP Pool schema.
  * Print WARNING message if too many attributes are put into a packet.
  * Include dhcp test client (not built by default)
  * Added checks for LDAP constraint violation.  Closes bug #18.
  * Change default raddebug timeout to 60 seconds.
  * Made error / warning messages more consistent.
  * Correct back-slash handling in variable expansion.  Closes bug #46.
    You SHOULD check your configuration for backslash expansion!
  * Fix typo in "configure" script (--enable-libltdl-install)
  * Use local libltdl in more situations.  This helps to avoid
    compile issues complaining about lt__PROGRAM__LTX_preloaded_symbols.
  * Fix hang on startup when multiple home servers were defined
    with "src_ipaddr" field.
  * Fix 32/64 bit issue in rlm_ldap.  Closes bug #105.
  * If the first "listen" section defines 127.0.0.1, don't use that
    as a source IP for proxying.  It won't work.
  * When Proxy-To-Realm is set to a non-existent realm, the EAP module
    should handle the request, rather than expecting it to be proxied.
  * Fix IPv4 issues with udpfromto.  Closes bug #110.
  * Clean up child processes of raddebug.  Closes bugs #108 and #109
  * retry OTP if the OTP daemon fails.  Closes bug #58.
  * Multiple calls to ber_printf seem to work better.  Closes #106.
  * Fix "unlang" so that "attribute not found" is treated as a "false"
    comparison, rather than a syntax error in the configuration.
  * Fix issue with "Group" attribute.

* Sat Jul 31 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 2.1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.1.9-2
- Mass rebuild with perl-5.12.0

* Mon May 24 2010 John Dennis <jdennis@redhat.com> - 2.1.9-1
- update to latest upstream, mainly bug fix release
  Feature improvements
  * Add radmin command "stats detail <file>" to see what
    is going on inside of a detail file reader.
  * Added documentation for CoA.  See raddb/sites-available/coa
  * Add sub-option support for Option 82.  See dictionary.dhcp
  * Add "server" field to default SQL NAS table, and documented it.
  Bug fixes
  * Reset "received ping" counter for Status-Server checks.  In some
    corner cases it was not getting reset.
  * Handle large VMPS attributes.
  * Count accounting responses from a home server in SNMP / statistics
    code.
  * Set EAP-Session-Resumed = Yes, not "No" when session is resumed.
  * radmin packet counter statistics are now unsigned, for numbers
    2^31..2^32.  After that they roll over to zero.
  * Be more careful about expanding data in PAP and MS-CHAP modules.
    This prevents login failures when passwords contain '{'.
  * Clean up zombie children if there were many "exec" modules being
    run for one packet, all with "wait = no".
  * re-open log file after HUP.  Closes bug #63.
  * Fix "no response to proxied packet" complaint for Coa / Disconnect
    packets.  It shouldn't ignore replies to packets it sent.
  * Calculate IPv6 netmasks correctly.  Closes bug #69.
  * Fix SQL module to re-open sockets if they unexpectedly close.
  * Track scope for IPv6 addresses.  This lets us use link-local
    addresses properly.  Closes bug #70.
  * Updated Makefiles to no longer use the shell for recursing into
    subdirs.  "make -j 2" should now work.
  * Updated raddb/sql/mysql/ippool.conf to use "= NULL".  Closes
    bug #75.
  * Updated Makefiles so that "make reconfig" no longer uses the shell
    for recursing into subdirs, and re-builds all "configure" files.
  * Used above method to regenerate all configure scripts.
    Closes bug #34.
  * Updated SQL module to allow "server" field of "nas" table
    to be blank: "".  This means the same as it being NULL.
  * Fixed regex realm example.  Create Realm attribute with value
    of realm from User-Name, not from regex.  Closes bug #40.
  * If processing a DHCP Discover returns "fail / reject", ignore
    the packet rather than sending a NAK.
  * Allow '%%' to be escaped in sqlcounter module.
  * Fix typo internal hash table.
  * For PEAP and TTLS, the tunneled reply is added to the reply,
    rather than integrated via the operators.  This allows multiple
    VSAs to be added, where they would previously be discarded.
  * Make request number unsigned.  This changes nothing other than
    the debug output when the server receives more than 2^31 packets.
  * Don't block when reading child output in 'exec wait'.  This means
    that blocked children get killed, instead of blocking the server.
  * Enabled building without any proxy functionality
  * radclient now prefers IPv4, to match the default server config.
  * Print useful error when a realm regex is invalid
  * relaxed rules for preprocess module "with_cisco_vsa_hack".  The
    attributes can now be integer, ipaddr, etc.  (i.e. non-string)
  * Allow rlm_ldap to build if ldap_set_rebind_proc() has only
    2 arguments.
  * Update configure script for rlm_python to avoid dynamic linking
    problems on some platforms.
  * Work-around for bug #35
  * Do suid to "user" when running in debug mode as root
  * Make "allow_core_dumps" work in more situations.
  * In detail file reader, treat bad records as EOF.
    This allows it to continue working when the disk is full.
  * Fix Oracle default accounting queries to work when there are no
    gigawords attributes.  Other databases already had the fix.
  * Fix rlm_sql to show when it opens and closes sockets.  It already
    says when it cannot connect, so it should say when it can connect.
  * "chmod -x" for a few C source files.
  * Pull update spec files, etc. from RedHat into the redhat/ directory.
  * Allow spaces when parsing integer values.  This helps people who
    put "too much" into an SQL value field.

* Thu Jan  7 2010 John Dennis <jdennis@redhat.com> - 2.1.8-2
- resolves: bug #526559 initial install should run bootstrap to create certificates
  running radiusd in debug mode to generate inital temporary certificates
  is no longer necessary, the /etc/raddb/certs/bootstrap is invoked on initial
  rpm install (not upgrade) if there is no existing /etc/raddb/certs/server.pem file
- resolves: bug #528493 use sha1 algorithm instead of md5 during cert generation
  the certificate configuration (/etc/raddb/certs/{ca,server,client}.cnf) files
  were modifed to use sha1 instead of md5 and the validity reduced from 1 year to 2 months

* Wed Dec 30 2009 John Dennis <jdennis@redhat.com> - 2.1.8-1
- update to latest upstream
  Feature improvements
  * Print more descriptive error message for too many EAP sessions.
    This gives hints on what to do when "failed to store handler"
  * Commands received from radmin are now printed on stdout when
    in debugging mode.
  * Allow accounting packets to be written to a detail file, even
    if they were read from a different detail file.
  * Added OpenSSL license exception (src/LICENSE.openssl)
  Bug fixes
  * DHCP sockets can now set the broadcast flag before binding to a
    socket.  You need to set "broadcast = yes" in the DHCP listener.
  * Be more restrictive on string parsing in the config files
  * Fix password length in scripts/create-users.pl
  * Be more flexible about parsing the detail file.  This allows
    it to read files where the attributes have been edited.
  * Ensure that requests read from the detail file are cleaned up
    (i.e. don't leak) if they are proxied without a response.
  * Write the PID file after opening sockets, not before
    (closes bug #29)
  * Proxying large numbers of packets no longer gives error
    "unable to open proxy socket".
  * Avoid mutex locks in libc after fork
  * Retry packet from detail file if there was no response.
  * Allow old-style dictionary formats, where the vendor name is the
    last field in an ATTRIBUTE definition.
  * Removed all recursive use of mutexes.  Some systems just don't
    support this.
  * Allow !* to work as documented.
  * make templates work (see templates.conf)
  * Enabled "allow_core_dumps" to work again
  * Print better errors when reading invalid dictionaries
  * Sign client certificates with CA, rather than server certs.
  * Fix potential crash in rlm_passwd when file was closed
  * Fixed corner cases in conditional dynamic expansion.
  * Use InnoDB for MySQL IP Pools, to gain transactional support
  * Apply patch to libltdl for CVE-2009-3736.
  * Fixed a few issues found by LLVM's static checker
  * Keep track of "bad authenticators" for accounting packets
  * Keep track of "dropped packets" for auth/acct packets
  * Synced the "debian" directory with upstream
  * Made "unlang" use unsigned 32-bit integers, to match the
    dictionaries.

* Wed Dec 30 2009 John Dennis <jdennis@redhat.com> - 2.1.7-7
- Remove devel subpackage. It doesn't make much sense to have a devel package since
  we don't ship libraries and it produces multilib conflicts.

* Mon Dec 21 2009 John Dennis <jdennis@redhat.com> - 2.1.7-6
- more spec file clean up from review comments
- remove freeradius-libs subpackage, move libfreeradius-eap and
  libfreeradius-radius into the main package
- fix subpackage requires, change from freeradius-libs to main package
- fix description of the devel subpackage, remove referene to non-shipped libs
- remove execute permissions on src files included in debuginfo
- remove unnecessary use of ldconfig
- since all sub-packages now require main package remove user creation for sub-packages
- also include the LGPL library license file in addition to the GPL license file
- fix BuildRequires for perl so it's compatible with both Fedora, RHEL5 and RHEL6

* Mon Dec 21 2009 John Dennis <jdennis@redhat.com> - 2.1.7-5
- fix various rpmlint issues.

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 2.1.7-4
- rebuild against perl 5.10.1

* Thu Dec  3 2009 John Dennis <jdennis@redhat.com> - 2.1.7-3
- resolves: bug #522111 non-conformant initscript
  also change permission of /var/run/radiusd from 0700 to 0755
  so that "service radiusd status" can be run as non-root

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.7-2
- use password-auth common PAM configuration instead of system-auth

* Tue Sep 15 2009 John Dennis <jdennis@redhat.com> - 2.1.7-1
- enable building of the rlm_wimax module
- pcap wire analysis support is enabled and available in utils subpackage
- Resolves bug #523053 radtest manpage in wrong package
- update to latest upstream release, from upstream Changelog:
  Feature improvements
    * Full support for CoA and Disconnect packets as per RFC 3576
      and RFC 5176.  Both receiving and proxying CoA is supported.
    * Added "src_ipaddr" configuration to "home_server".  See
      proxy.conf for details.
    * radsniff now accepts -I, to read from a filename instead of
      a device.
    * radsniff also prints matching requests and any responses to those
      requests when '-r' is used.
    * Added example of attr_filter for Access-Challenge packets
    * Added support for udpfromto in DHCP code
    * radmin can now selectively mark modules alive/dead.
      See "set module state".
    * Added customizable messages on login success/fail.
      See msg_goodpass && msg_badpass in log{} section of radiusd.conf
    * Document "chase_referrals" and "rebind" in raddb/modules/ldap
    * Preliminary implementation of DHCP relay.
    * Made thread pool section optional.  If it doesn't exist,
      the server will run single-threaded.
    * Added sample radrelay.conf for people upgrading from 1.x
    * Made proxying more stable by failing over, rather than
      rejecting the first request.  See "response_window" in proxy.conf
    * Allow home_server_pools to exist without realms.
    * Add dictionary.iea (closes bug #7)
    * Added support for RFC 5580
    * Added experimental sql_freetds module from Gabriel Blanchard.
    * Updated dictionary.foundry
    * Added sample configuration for MySQL cluster in raddb/sql/ndb
      See the README file for explanations.
  Bug fixes
    * Fixed corner case where proxied packets could have extra
      character in User-Password attribute.  Fix from Niko Tyni.
    * Extended size of "attribute" field in SQL to 64.
    * Fixes to ruby module to be more careful about when it builds.
    * Updated Perl module "configure" script to check for broken
      Perl installations.
    * Fix "status_check = none".  It would still send packets
      in some cases.
    * Set recursive flag on the proxy mutex, which enables safer
      cleanup on some platforms.
    * Copy the EAP username verbatim, rather than escaping it.
    * Update handling so that robust-proxy-accounting works when
      all home servers are down for extended periods of time.
    * Look for DHCP option 53 anywhere in the packet, not just
      at the start.
    * Fix processing of proxy fail handler with virtual servers.
    * DHCP code now prints out correct src/dst IP addresses
      when sending packets.
    * Removed requirement for DHCP to have clients
    * Fixed handling of DHCP packets with message-type buried in the packet
    * Fixed corner case with negation in unlang.
    * Minor fixes to default MySQL & PostgreSQL schemas
    * Suppress MSCHAP complaints in debugging mode.
    * Fix SQL module for multiple instance, and possible crash on HUP
    * Fix permissions for radius.log for sites that change user/group,
      but which don't create the file before starting radiusd.
    * Fix double counting of packets when proxying
    * Make %%l work
    * Fix pthread keys in rlm_perl
    * Log reasons for EAP failure (closes bug #8)
    * Load home servers and pools that aren't referenced from a realm.
    * Handle return codes from virtual attributes in "unlang"
      (e.g. LDAP-Group).  This makes "!(expr)" work for them.
    * Enable VMPS to see contents of virtual server again
    * Fix WiMAX module to be consistent with examples.  (closes bug #10)
    * Fixed crash with policies dependent on NAS-Port comparisons
    * Allowed vendor IDs to be be higher than 32767.
    * Fix crash on startup with certain regexes in "hints" file.
    * Fix crash in attr_filter module when packets don't exist
    * Allow detail file reader to be faster when "load_factor = 100"
    * Add work-around for build failures with errors related to
      lt__PROGRAM__LTX_preloaded_symbols.  libltdl / libtool are horrible.
    * Made ldap module "rebind" option aware of older, incompatible
      versions of OpenLDAP.
    * Check value of Fall-Through in attr_filter module.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.6-6
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 John Dennis <jdennis@redhat.com> - 2.1.6-4
- install COPYRIGHT CREDITS INSTALL LICENSE README into docdir

* Tue Jun 23 2009 John Dennis <jdennis@redhat.com> - 2.1.6-3
- resolves bug #507571 freeradius packages do not check for user/group existence

* Tue Jun  2 2009 John Dennis <jdennis@redhat.com> - 2.1.6-2
- make /etc/raddb/sites-available/* be config(noreplace)

* Mon May 18 2009 John Dennis <jdennis@redhat.com> - 2.1.6-1
- update to latest upstream release, from upstream Changelog:
  Feature improvements
    * radclient exits with 0 on successful (accept / ack), and 1
      otherwise (no response / reject)
    * Added support for %%{sql:UPDATE ..}, and insert/delete
      Patch from Arran Cudbard-Bell
    * Added sample "do not respond" policy.  See raddb/policy.conf
      and raddb/sites-available/do_not_respond
    * Cleanups to Suse spec file from Norbert Wegener
    * New VSAs for Juniper from Bjorn Mork
    * Include more RFC dictionaries in the default install
    * More documentation for the WiMAX module
    * Added "chase_referrals" and "rebind" configuration to rlm_ldap.
      This helps with Active Directory.  See raddb/modules/ldap
    * Don't load pre/post-proxy if proxying is disabled.
    * Added %%{md5:...}, which returns MD5 hash in hex.
    * Added configurable "retry_interval" and "poll_interval"
      for "detail" listeners.
    * Added "delete_mppe_keys" configuration option to rlm_wimax.
      Apparently some WiMAX clients misbehave when they see those keys.
    * Added experimental rlm_ruby from
      http://github.com/Antti/freeradius-server/tree/master
    * Add Tunnel attributes to ldap.attrmap
    * Enable virtual servers to be reloaded on HUP.  For now, only
      the "authorize", "authenticate", etc. processing sections are
      reloaded.  Clients and "listen" sections are NOT reloaded.
    * Updated "radwatch" script to be more robust.  See scripts/radwatch
    * Added certificate compatibility notes in raddb/certs/README,
      for compatibility with different operating systems. (i.e. Windows)
    * Permit multiple "-e" in radmin.
    * Add support for originating CoA-Request and Disconnect-Request.
      See raddb/sites-available/originate-coa.
    * Added "lifetime" and "max_queries" to raddb/sql.conf.
      This helps address the problem of hung SQL sockets.
    * Allow packets to be injected via radmin.  See "inject help"
      in radmin.
    * Answer VMPS reconfirmation request.  Patch from Hermann Lauer.
    * Sample logrotate script in scripts/logrotate.freeradius
    * Add configurable poll interval for "detail" listeners
    * New "raddebug" command.  This prints debugging information from
      a running server.  See "man raddebug.
    * Add "require_message_authenticator" configuration to home_server
      configuration.  This makes the server add Message-Authenticator
      to all outgoing Access-Request packets.
    * Added smsotp module, as contributed by Siemens.
    * Enabled the administration socket in the default install.
      See raddb/sites-available/control-socket, and "man radmin"
    * Handle duplicate clients, such as with replicated or
      load-balanced SQL servers and "readclients = yes"
  Bug fixes
    * Minor changes to allow building without VQP.
    * Minor fixes from John Center
    * Fixed raddebug example
    * Don't crash when deleting attributes via unlang
    * Be friendlier to very fast clients
    * Updated the "detail" listener so that it only polls once,
      and not many times in a row, leaking memory each time...
    * Update comparison for Packet-Src-IP-Address (etc.) so that
      the operators other than '==' work.
    * Did autoconf magic to work around weird libtool bug
    * Make rlm_perl keep tags for tagged attributes in more situations
    * Update UID checking for radmin
    * Added "include_length" field for TTLS.  It's needed for RFC
      compliance, but not (apparently) for interoperability.
    * Clean up control sockets when they are closed, so that we don't
      leak memory.
    * Define SUN_LEN for systems that don't have it.
    * Correct some boundary conditions in the conditional checker ("if")
      in "unlang".  Bug noted by Arran Cudbard-Bell.
    * Work around minor building issues in gmake.  This should only
      have affected developers.
    * Change how we manage unprivileged user/group, so that we do not
      create control sockets owned by root.
    * Fixed more minor issues found by Coverity.
    * Allow raddb/certs/bootstrap to run when there is no "make"
      command installed.
    * In radiusd.conf, run_dir depends on the name of the program,
      and isn't hard-coded to "..../radiusd"
    * Check for EOF in more places in the "detail" file reader.
    * Added Freeswitch dictionary.
    * Chop ethernet frames in VMPS, rather than droppping packets.
    * Fix EAP-TLS bug.  Patch from Arnaud Ebalard
    * Don't lose string for regex-compares in the "users" file.
    * Expose more functions in rlm_sql to rlm_sqlippool, which
      helps on systems where RTLD_GLOBAL is off.
    * Fix typos in MySQL schemas for ippools.
    * Remove macro that was causing build issues on some platforms.
    * Fixed issues with dead home servers.  Bug noted by Chris Moules.
    * Fixed "access after free" with some dynamic clients.
- fix packaging bug, some directories missing execute permission
  /etc/raddb/dictionary now readable by all.

* Tue Feb 24 2009 John Dennis <jdennis@redhat.com> - 2.1.3-4
- fix type usage in unixodbc to match new type usage in unixodbc API

* Thu Feb 19 2009 John Dennis <jdennis@redhat.com> - 2.1.3-3
- add pointer to Red Hat documentation in docdir

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> - 2.1.3-2
- rebuild for dependencies

* Thu Dec  4 2008 John Dennis <jdennis@redhat.com> - 2.1.3-1
- upgrade to latest upstream release, upstream summary follows:
  The focus of this release is stability.
  Feature Improvements:
    * Allow running with "user=radiusd" and binding to secure sockets.
    * Start sending Status-Server "are you alive" messages earlier, which
      helps with proxying multiple realms to a home server.
    * Removed thread pool code from rlm_perl.  It's not necessary.
    * Added example Perl configuration to raddb/modules/perl
    * Force OpenSSL to support certificates with SHA256. This seems to be
      necessary for WiMAX certs.
  Bug fixes:
    * Fix Debian patch to allow it to build.
    * Fix potential NULL dereference in debugging mode on certain
      platforms for TTLS and PEAP inner tunnels.
    * Fix uninitialized memory in handling of vendor definitions
    * Fix parsing of quoted (but non-string) attributes in the "users" file.
    * Initialize uknown NAS IP to 255.255.255.255, rather than 0.0.0.0
    * use SUN_LEN in control socket, to avoid truncation on some platforms.
    * Correct internal handling of "debug condition" to prevent it from
      being over-written.
    * Check return code of regcomp in "unlang", so that invalid regular
      expressions are caught rather than mishandled.
    * Make rlm_sql use <ltdl.h>.  Addresses bug #610.
    * Document list "type = status" better.  Closes bug #580.
    * Set "default days" for certificates, because OpenSSL won't do it.
      This closes bug #615.
    * Reference correct list in example raddb/modules/ldap. Closes #596.
    * Increase default schema size for Acct-Session-Id to 64. Closes #540.
    * Fix use of temporary files in dialup-admin.  Closes #605 and
      addresses CVE-2008-4474.
    * Addressed a number of minor issues found by Coverity.
    * Added DHCP option 150 to the dictionary.  Closes #618.

* Wed Dec  3 2008 John Dennis <jdennis@redhat.com> - 2.1.1-8
- add --with-system-libtool to configure as a workaround for
undefined reference to lt__PROGRAM__LTX_preloaded_symbols

* Mon Dec  1 2008 John Dennis <jdennis@redhat.com> - 2.1.1-7
- add obsoletes tag for dialupadmin subpackages which were removed

* Mon Dec  1 2008 John Dennis <jdennis@redhat.com> - 2.1.1-7
- add readline-devel BuildRequires

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.1.1-4
- Rebuild for Python 2.6

* Fri Nov 21 2008 John Dennis <jdennis@redhat.com> - 2.1.1-3
- make spec file buildable on RHEL5.2 by making perl-devel a fedora only dependency.
- remove diaupadmin packages, it's not well supported and there are problems with it.

* Fri Sep 26 2008 John Dennis <jdennis@redhat.com> - 2.1.1-1
- Resolves: bug #464119 bootstrap code could not create initial certs in /etc/raddb/certs because
  permissions were 750, radiusd running as euid radiusd could not write there, permissions now 770

* Thu Sep 25 2008 John Dennis <jdennis@redhat.com> - 2.1.1-1
- upgrade to new upstream 2.1.1 release

* Wed Jul 30 2008 John Dennis <jdennis@redhat.com> - 2.0.5-2
- Resolves: bug #453761: FreeRADIUS %%post should not include chown -R
  specify file attributes for /etc/raddb/ldap.attrmap
  fix consistent use of tabs/spaces (rpmlint warning)

* Mon Jun  9 2008 John Dennis <jdennis@redhat.com> - 2.0.5-1
- upgrade to latest upstream, see Changelog for details,
  upstream now has more complete fix for bug #447545, local patch removed

* Wed May 28 2008 John Dennis <jdennis@redhat.com> - 2.0.4-1
- upgrade to latest upstream, see Changelog for details
- resolves: bug #447545: freeradius missing /etc/raddb/sites-available/inner-tunnel

* Fri May 16 2008  <jdennis@redhat.com> - 2.0.3-3
- # Temporary fix for bug #446864, turn off optimization

* Fri Apr 18 2008 John Dennis <jdennis@redhat.com> - 2.0.3-2
- remove support for radrelay, it's different now
- turn off default inclusion of SQL config files in radiusd.conf since SQL
  is an optional RPM install
- remove mssql config files

* Thu Apr 17 2008 John Dennis <jdennis@redhat.com> - 2.0.3-1
- Upgrade to current upstream 2.0.3 release
- Many thanks to Enrico Scholz for his spec file suggestions incorporated here
- Resolve: bug #438665: Contains files owned by buildsystem
- Add dialupadmin-mysql, dialupadmin-postgresql, dialupadmin-ldap subpackages
  to further partition external dependencies.
- Clean up some unnecessary requires dependencies
- Add versioned requires between subpackages

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.0.2-2
- add Requires for versioned perl (libperl.so)

* Thu Feb 28 2008  <jdennis@redhat.com> - 2.0.2-1
- upgrade to new 2.0 release
- split into subpackages for more fine grained installation

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.7-4.4.ipa
- Autorebuild for GCC 4.3

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.7-3.4.ipa
- Rebuild for deps

* Sat Nov 10 2007  <jdennis@redhat.com> - 1.1.7-3.3.ipa
- add support in rlm_ldap for reading clients from ldap
- fix TLS parameter controling if a cert which fails to validate
  will be accepted (i.e. self-signed),
  rlm_ldap config parameter=tls_require_cert
  ldap LDAP_OPT_X_TLS_REQUIRE_CERT parameter was being passed to
  ldap_set_option() when it should have been ldap_int_tls_config()

* Sat Nov 3 2007  <jdennis@redhat.com> - 1.1.7-3.2.ipa
- add support in rlm_ldap for SASL/GSSAPI binds to the LDAP server

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-3.1
- made init script fully lsb conform

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-3
- fixed initscript problem (rhbz#292521)

* Tue Aug 28 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-2
- fixed initscript for LSB (rhbz#243671, rhbz#243928)
- fixed license tag

* Tue Aug  7 2007 Thomas Woerner <twoerner@redhat.com> 1.1.7-1
- new versin 1.1.7
- install snmp MIB files
- dropped LDAP_DEPRECATED flag, it is upstream
- marked config files for sub packages as config (rhbz#240400)
- moved db files to /var/lib/raddb (rhbz#199082)

* Fri Jun 15 2007 Thomas Woerner <twoerner@redhat.com> 1.1.6-2
- radiusd expects /etc/raddb to not be world readable or writable
  /etc/raddb now belongs to radiusd, post script sets permissions

* Fri Jun 15 2007 Thomas Woerner <twoerner@redhat.com> 1.1.6-1
- new version 1.1.6

* Fri Mar  9 2007 Thomas Woerner <twoerner@redhat.com> 1.1.5-1
- new version 1.1.5
  - no /etc/raddb/otppasswd.sample anymore
  - build is pie by default, dropped pie patch
- fixed build requirement for perl (perl-devel)

* Fri Feb 23 2007 Karsten Hopp <karsten@redhat.com> 1.1.3-3
- remove trailing dot from summary
- fix buildroot
- fix post/postun/preun requirements
- use rpm macros

* Fri Dec  8 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-2.1
- rebuild for new postgresql library version

* Thu Nov 30 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-2
- fixed ldap code to not use internals, added LDAP_DEPRECATED compile time flag
  (#210912)

* Tue Aug 15 2006 Thomas Woerner <twoerner@redhat.com> 1.1.3-1
- new version 1.1.3 with lots of upstream bug fixes, some security fixes
  (#205654)

* Tue Aug 15 2006 Thomas Woerner <twoerner@redhat.com> 1.1.2-2
- commented out include for sql.conf in radiusd.conf (#202561)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.1.2-1.1
- rebuild

* Thu Jun  1 2006 Thomas Woerner <twoerner@redhat.com> 1.1.2-1
- new version 1.1.2

* Wed May 31 2006 Thomas Woerner <twoerner@redhat.com> 1.1.1-1
- new version 1.1.1
- fixed incorrect rlm_sql globbing (#189095)
  Thanks to Yanko Kaneti for the fix.
- fixed chown syntax in post script (#182777)
- dropped gcc34, libdir and realloc-return patch
- spec file cleanup with additional libtool build fixes

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005 Thomas Woerner <twoerner@redhat.com> 1.0.5-1
- new version 1.0.5

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> - 1.0.4-5
- Rebuild due to mysql update.

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> - 1.0.4-4
- rebuilt with new openssl
- fixed ignored return value of realloc

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 1.0.4-3
- use include instead of pam_stack in pam config

* Wed Jul 20 2005 Thomas Woerner <twoerner@redhat.com> 1.0.4-2
- added missing build requires for libtool-ltdl-devel (#160877)
- modified file list to get a report for missing plugins

* Tue Jun 28 2005 Thomas Woerner <twoerner@redhat.com> 1.0.4-1
- new version 1.0.4
- droppend radrelay patch (fixed upstream)

* Thu Apr 14 2005 Warren Togami <wtogami@redhat.com> 1.0.2-2
- rebuild against new postgresql-libs

* Mon Apr  4 2005 Thomas Woerner <twoerner@redhat.com> 1.0.2-1
- new version 1.0.2

* Fri Nov 19 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-3
- rebuild for MySQL 4
- switched over to installed libtool

* Fri Nov  5 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-2
- Fixed install problem of radeapclient (#138069)

* Wed Oct  6 2004 Thomas Woerner <twoerner@redhat.com> 1.0.1-1
- new version 1.0.1
- applied radrelay CVS patch from Kevin Bonner

* Wed Aug 25 2004 Warren Togami <wtogami@redhat.com> 1.0.0-3
- BuildRequires pam-devel and libtool
- Fix errant text in description
- Other minor cleanups

* Wed Aug 25 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-2.1
- renamed /etc/pam.d/radius to /etc/pam.d/radiusd to match default
  configuration (#130613)

* Wed Aug 25 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-2
- fixed BuildRequires for openssl-devel (#130606)

* Mon Aug 16 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-1
- 1.0.0 final

* Mon Jul  5 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-0.pre3.2
- added buildrequires for zlib-devel (#127162)
- fixed libdir patch to prefer own libeap instead of installed one (#127168)
- fixed samba account maps in LDAP for samba v3 (#127173)

* Thu Jul  1 2004 Thomas Woerner <twoerner@redhat.com> 1.0.0-0.pre3.1
- third "pre" release of version 1.0.0
- rlm_ldap is using SASLv2 (#126507)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun  3 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-4.1
- fixed BuildRequires for gdbm-devel

* Tue Mar 30 2004 Harald Hoyer <harald@redhat.com> - 0.9.3-4
- gcc34 compilation fixes

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-3.2
- added sql scripts for rlm_sql to documentation (#116435)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-2.1
- using -fPIC instead of -fpic for s390 ans s390x

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 0.9.3-2
- radiusd is pie, now

* Tue Nov 25 2003 Thomas Woerner <twoerner@redhat.com> 0.9.3-1
- new version 0.9.3 (bugfix release)

* Fri Nov  7 2003 Thomas Woerner <twoerner@redhat.com> 0.9.2-1
- new version 0.9.2

* Mon Sep 29 2003 Thomas Woerner <twoerner@redhat.com> 0.9.1-1
- new version 0.9.1

* Mon Sep 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.0-2.2
- modify default PAM configuration to remove the directory part of the module
  name, so that 32- and 64-bit libpam (called from 32- or 64-bit radiusd) on
  multilib systems will always load the right module for the architecture
- modify default PAM configuration to use pam_stack

* Mon Sep  1 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-2.1
- com_err.h moved to /usr/include/et

* Tue Jul 22 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-1
- 0.9.0 final

* Wed Jul 16 2003 Thomas Woerner <twoerner@redhat.com> 0.9.0-0.9.0
- new version 0.9.0 pre3

* Thu May 22 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-6
- included directory /var/log/radius/radacct for logrotate

* Wed May 21 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-5
- moved log and run dir to files section, cleaned up post

* Wed May 21 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-4
- added missing run dir in post

* Tue May 20 2003 Thomas Woerner <twoerner@redhat.com> 0.8.1-3
- fixed module load patch

* Fri May 16 2003 Thomas Woerner <twoerner@redhat.com>
- removed la files, removed devel package
- split into 4 packages: freeradius, freeradius-mysql, freeradius-postgresql,
    freeradius-unixODBC
- fixed requires and buildrequires
- create logging dir in post if it does not exist
- fixed module load without la files

* Thu Apr 17 2003 Thomas Woerner <twoerner@redhat.com>
- Initial build.
