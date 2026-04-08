# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define webroot /var/www/lighttpd

# We have an bunch of --with/--without options to pass, make it easy with bcond
%define confswitch() %{expand:%%{?with_%{1}:--with-%{1}}%%{!?with_%{1}:--without-%{1}}}

%bcond_without attr
%bcond_with    pcre
%bcond_without pcre2
%bcond_without nettle
%bcond_with    unwind

%bcond_without lua

%bcond_without brotli
%bcond_with    bzip2
%bcond_without zlib
%bcond_without zstd

%bcond_without maxminddb

%if 0%{?rhel} >= 9
%bcond_with    dbi
%else
%bcond_without dbi
%endif
%bcond_without ldap
%bcond_without mysql
%bcond_without pgsql

%bcond_without krb5
%bcond_without pam
%bcond_without sasl

%bcond_without gnutls
%bcond_without mbedtls
%bcond_without nss
%bcond_without openssl

# We can't have bcond names with hyphens
%bcond_without webdavprops
%bcond_without webdavlocks

# The /var/run/lighttpd directory uses tmpfiles.d when mounted using tmpfs
%if 0%{?fedora} || 0%{?rhel} >= 8
%bcond_without tmpfiles
%else
%bcond_with    tmpfiles
%endif

Summary: Lightning fast webserver with light system requirements
Name: lighttpd
Version: 1.4.82
Release: 1%{?dist}
License: BSD-3-Clause
URL: http://www.lighttpd.net/
Source0: http://download.lighttpd.net/lighttpd/releases-1.4.x/lighttpd-%{version}.tar.xz
Source1: lighttpd.logrotate
Source2: php.d-lighttpd.ini
Source10: index.html
Source11: http://www.lighttpd.net/favicon.ico
Source12: http://www.lighttpd.net/light_button.png
Source13: http://www.lighttpd.net/light_logo.png
Source14: lighttpd-empty.png
Patch0: lighttpd-1.4.79-defaultconf.patch
Requires: system-logos
Requires: %{name}-filesystem
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
# preserve installation of modules historically bundled with lighttpd package
Requires(post): %{name}-mod_deflate
Requires(post): %{name}-mod_webdav
%{?with_lua:Requires(post): %{name}-mod_magnet}
%{?with_openssl:Requires(post): %{name}-mod_openssl}
Provides: webserver
BuildRequires: autoconf, automake, libtool, m4, pkg-config, /usr/bin/awk
BuildRequires: libxcrypt-devel
%{?with_pcre:BuildRequires: pcre-devel}
%{?with_pcre2:BuildRequires: pcre2-devel}
%{?with_nettle:BuildRequires: nettle-devel}
%{?with_unwind:BuildRequires: libunwind-devel}

%description
lighttpd (pronounced /lighty/) is a secure, fast, compliant, and very flexible
web server that has been optimized for high-performance environments. lighttpd
uses memory and CPU efficiently and has lower resource use than other popular
web servers. Its advanced feature-set (FastCGI, CGI, Auth, Output-Compression,
URL-Rewriting and much more) make lighttpd the perfect web server for all
systems, small and large.


%package fastcgi
Summary: FastCGI module and spawning helper for lighttpd and PHP configuration
Requires: %{name} = %{version}-%{release}

%description fastcgi
This package contains the spawn-fcgi helper for lighttpd's automatic spawning
of local FastCGI programs. Included is also a PHP .ini file to change a few
defaults needed for correct FastCGI behavior.


%if %{with dbi}
%package mod_authn_dbi
Summary: Authentication module for lighttpd that uses DBI
Requires: %{name} = %{version}-%{release}
%{?with_dbi:BuildRequires: libdbi-devel}
%{?with_dbi:Suggests: libdbi-dbd-mysql}
%{?with_dbi:Suggests: libdbi-dbd-pgsql}
%{?with_dbi:Suggests: libdbi-dbd-sqlite}

%description mod_authn_dbi
Authentication module for lighttpd that uses DBI
%endif


%if %{with krb5}
%package mod_authn_gssapi
Summary: Authentication module for lighttpd that uses GSSAPI
Requires: %{name} = %{version}-%{release}
%{?with_krb5:BuildRequires: krb5-devel}

%description mod_authn_gssapi
Authentication module for lighttpd that uses GSSAPI
%endif


%if %{with ldap}
%package mod_authn_ldap
Summary: Authentication module for lighttpd that uses LDAP
Requires: %{name} = %{version}-%{release}
%{?with_ldap:BuildRequires: openldap-devel}

%description mod_authn_ldap
Authentication module for lighttpd that uses LDAP
%endif


%if %{with pam}
%package mod_authn_pam
Summary: Authentication module for lighttpd that uses PAM
Requires: %{name} = %{version}-%{release}
%{?with_pam:BuildRequires: pam-devel}

%description mod_authn_pam
Authentication module for lighttpd that uses PAM.
%endif


%if %{with sasl}
%package mod_authn_sasl
Summary: Authentication module for lighttpd that uses SASL
Requires: %{name} = %{version}-%{release}
%{?with_sasl:BuildRequires: cyrus-sasl-devel}

%description mod_authn_sasl
Authentication module for lighttpd that uses SASL.
%endif


%package mod_deflate
Summary: Compression module for lighttpd
Requires: %{name} = %{version}-%{release}
%{?with_zlib:BuildRequires: zlib-devel}
%{?with_zstd:BuildRequires: libzstd-devel}
%{?with_bzip2:BuildRequires: bzip2-devel}
%{?with_brotli:BuildRequires: brotli-devel}

%description mod_deflate
Compression module for lighttpd.


%if %{with gnutls}
%package mod_gnutls
Summary: TLS module for lighttpd that uses GnuTLS
Requires: %{name} = %{version}-%{release}
%{?with_gnutls:BuildRequires: gnutls-devel}

%description mod_gnutls
TLS module for lighttpd that uses GnuTLS.
%endif


%if %{with lua}
%package mod_magnet
Summary: Lua module for lighttpd
Requires: %{name} = %{version}-%{release}
%{?with_lua:BuildRequires: lua-devel}

%description mod_magnet
Lua module for lighttpd.
%endif


%if %{with maxminddb}
%package mod_maxminddb
Summary: GeoIP2 module for lighttpd to use for location lookups
Requires: %{name} = %{version}-%{release}
%{?with_maxminddb:BuildRequires: libmaxminddb-devel}
%{?with_maxminddb:Recommends: GeoIP-GeoLite-data}
%{?with_maxminddb:Recommends: GeoIP-GeoLite-data-extra}
%{?with_maxminddb:Suggests: geoipupdate}
%{?with_maxminddb:Suggests: geoipupdate-cron}

%description mod_maxminddb
GeoIP2 module for lighttpd to use for location lookups.
%endif


%if %{with mbedtls}
%package mod_mbedtls
Summary: TLS module for lighttpd that uses mbedTLS
Requires: %{name} = %{version}-%{release}
%{?with_mbedtls:BuildRequires: mbedtls-devel}

%description mod_mbedtls
TLS module for lighttpd that uses mbedTLS.
%endif


%if %{with nss}
%package mod_nss
Summary: TLS module for lighttpd that uses NSS
Requires: %{name} = %{version}-%{release}
%{?with_nss:BuildRequires: nss-devel}

%description mod_nss
TLS module for lighttpd that uses NSS.
%endif


%if %{with openssl}
%package mod_openssl
Summary: TLS module for lighttpd that uses OpenSSL
Requires: %{name} = %{version}-%{release}
%{?with_openssl:BuildRequires: openssl-devel}

%description mod_openssl
TLS module for lighttpd that uses OpenSSL.
%endif


%if %{with dbi}
%package mod_vhostdb_dbi
Summary: Virtual host module for lighttpd that uses DBI
Requires: %{name} = %{version}-%{release}
%{?with_dbi:BuildRequires: libdbi-devel}
%{?with_dbi:Suggests: libdbi-dbd-mysql}
%{?with_dbi:Suggests: libdbi-dbd-pgsql}
%{?with_dbi:Suggests: libdbi-dbd-sqlite}

%description mod_vhostdb_dbi
Virtual host module for lighttpd that uses DBI.
%endif


%if %{with ldap}
%package mod_vhostdb_ldap
Summary: Virtual host module for lighttpd that uses LDAP
Requires: %{name} = %{version}-%{release}
%{?with_ldap:BuildRequires: openldap-devel}

%description mod_vhostdb_ldap
Virtual host module for lighttpd that uses LDAP.
%endif


%if %{with mysql}
%package mod_vhostdb_mysql
Summary: Virtual host module for lighttpd that uses MySQL
Requires: %{name} = %{version}-%{release}
%{?with_mysql:BuildRequires: mariadb-connector-c-devel}

%description mod_vhostdb_mysql
Virtual host module for lighttpd that uses MySQL.
%endif


%if %{with pgsql}
%package mod_vhostdb_pgsql
Summary: Virtual host module for lighttpd that uses PostgreSQL
Requires: %{name} = %{version}-%{release}
%{?with_pgsql:BuildRequires: libpq-devel}

%description mod_vhostdb_pgsql
Virtual host module for lighttpd that uses PostgreSQL.
%endif


%package mod_webdav
Summary: WebDAV module for lighttpd
Requires: %{name} = %{version}-%{release}
%{?with_webdavprops:BuildRequires: libxml2-devel}
%{?with_webdavprops:BuildRequires: sqlite-devel}
%{?with_webdavlocks:BuildRequires: libxml2-devel}
%{?with_webdavlocks:BuildRequires: sqlite-devel}

%description mod_webdav
WebDAV module for lighttpd.


%package filesystem
Summary: The basic directory layout for lighttpd
BuildArch: noarch

%description filesystem
The lighttpd-filesystem package contains the basic directory layout
for the lighttpd server including the correct permissions
for the directories.


%prep
%setup -q
%patch -P 0 -p0 -b .defaultconf

# Create a sysusers.d config file
cat >lighttpd.sysusers.conf <<EOF
u lighttpd - 'lighttpd web server' %{webroot} -
EOF

%build
autoreconf -if
%configure \
    --libdir='%{_libdir}/lighttpd' \
    %{confswitch pcre} \
    %{confswitch pcre2} \
    %{confswitch nettle} \
    %{confswitch attr} \
    %{confswitch mysql} \
    %{confswitch pgsql} \
    %{confswitch dbi} \
    %{confswitch krb5} \
    %{confswitch ldap} \
    %{confswitch pam} \
    %{confswitch sasl} \
    %{confswitch gnutls} \
    %{confswitch mbedtls} \
    %{confswitch nss} \
    %{confswitch openssl} \
    %{?with_webdavprops:--with-webdav-props} \
    %{?with_webdavlocks:--with-webdav-locks} \
    %{?with_lua:--with-lua=lua} \
    %{confswitch zlib} \
    %{confswitch zstd} \
    %{confswitch bzip2} \
    %{confswitch brotli} \
    %{confswitch maxminddb} \
    %{confswitch unwind}
%make_build


%install
%make_install

# Install our own logrotate entry
install -D -p -m 0644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/logrotate.d/lighttpd

# Install our own php.d ini file
install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_sysconfdir}/php.d/lighttpd.ini

# Install upstream systemd service
install -D -p -m 0644 doc/systemd/lighttpd.service \
    %{buildroot}%{_unitdir}/lighttpd.service

# Install our own default web page and images
mkdir -p %{buildroot}%{webroot}
install -p -m 0644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} \
    %{buildroot}%{webroot}/

# Symlink for the powered-by-$DISTRO image (install empty image on EL5)
%if %{with systemlogos}
ln -s %{_datadir}/pixmaps/poweredby.png \
%else
install -p -m 0644 %{SOURCE14} \
%endif
    %{buildroot}%{webroot}/poweredby.png

# Example configuration to be included as %%doc
rm -rf config
cp -a doc/config config
find config -name 'Makefile*' | xargs rm -f
# Remove +x from scripts to be included as %%doc to avoid auto requirement
chmod -x doc/scripts/*.sh

# Install (*patched above*) sample config files
mkdir -p %{buildroot}%{_sysconfdir}/lighttpd
cp -a config/*.conf config/*.d %{buildroot}%{_sysconfdir}/lighttpd/
mkdir -p %{buildroot}/usr/lib/modules-load.d
echo tls > %{buildroot}/usr/lib/modules-load.d/lighttpd-mod_gnutls.conf
echo tls > %{buildroot}/usr/lib/modules-load.d/lighttpd-mod_openssl.conf

# Install empty log directory to include
mkdir -p %{buildroot}%{_var}/log/lighttpd

# Install empty run directory to include (for the example fastcgi socket)
mkdir -p %{buildroot}%{_var}/run/lighttpd
%if %{with tmpfiles}
# Setup tmpfiles.d config for the above
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
echo 'D /run/lighttpd 0750 lighttpd lighttpd -' > \
    %{buildroot}/usr/lib/tmpfiles.d/lighttpd.conf
%endif

mkdir -p %{buildroot}%{_var}/lib/lighttpd/

install -m0644 -D lighttpd.sysusers.conf %{buildroot}%{_sysusersdir}/lighttpd.conf


%post
%systemd_post lighttpd.service

%preun
%systemd_preun lighttpd.service

%postun
%systemd_postun_with_restart lighttpd.service

%files
%license COPYING
%doc AUTHORS README
%doc config/ doc/scripts/cert-staple.sh doc/scripts/rrdtool-graph.sh
%config(noreplace) %{_sysconfdir}/lighttpd/*.conf
%config(noreplace) %{_sysconfdir}/lighttpd/conf.d/*.conf
%exclude %{_sysconfdir}/lighttpd/conf.d/deflate.conf
%exclude %{_sysconfdir}/lighttpd/conf.d/fastcgi.conf
%exclude %{_sysconfdir}/lighttpd/conf.d/magnet.conf
%exclude %{_sysconfdir}/lighttpd/conf.d/webdav.conf
%exclude %{_sysconfdir}/lighttpd/conf.d/tls.conf.defaultconf
%config %{_sysconfdir}/lighttpd/conf.d/mod.template
%config %{_sysconfdir}/lighttpd/vhosts.d/vhosts.template
%config(noreplace) %{_sysconfdir}/logrotate.d/lighttpd
%{_unitdir}/lighttpd.service
%if %{with tmpfiles}
%config(noreplace) /usr/lib/tmpfiles.d/lighttpd.conf
%endif
%{_sbindir}/lighttpd
%{_sbindir}/lighttpd-angel
%{_libdir}/lighttpd/
%exclude %{_libdir}/lighttpd/mod_authn_dbi.so
%exclude %{_libdir}/lighttpd/mod_authn_gssapi.so
%exclude %{_libdir}/lighttpd/mod_authn_ldap.so
%exclude %{_libdir}/lighttpd/mod_authn_pam.so
%exclude %{_libdir}/lighttpd/mod_authn_sasl.so
%exclude %{_libdir}/lighttpd/mod_deflate.so
%exclude %{_libdir}/lighttpd/mod_gnutls.so
%exclude %{_libdir}/lighttpd/mod_magnet.so
%exclude %{_libdir}/lighttpd/mod_maxminddb.so
%exclude %{_libdir}/lighttpd/mod_mbedtls.so
%exclude %{_libdir}/lighttpd/mod_openssl.so
%exclude %{_libdir}/lighttpd/mod_nss.so
%exclude %{_libdir}/lighttpd/mod_vhostdb_dbi.so
%exclude %{_libdir}/lighttpd/mod_vhostdb_ldap.so
%exclude %{_libdir}/lighttpd/mod_vhostdb_mysql.so
%exclude %{_libdir}/lighttpd/mod_vhostdb_pgsql.so
%{_mandir}/man8/lighttpd*8*
%{webroot}/*.ico
%{webroot}/*.png
# This is not really configuration, but prevent loss of local changes
%config %{webroot}/index.html

%files fastcgi
%doc doc/outdated/fastcgi*.txt
%config(noreplace) %{_sysconfdir}/php.d/lighttpd.ini
%config(noreplace) %{_sysconfdir}/lighttpd/conf.d/fastcgi.conf

%if %{with dbi}
%files mod_authn_dbi
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_authn_dbi.so
%endif

%if %{with krb5}
%files mod_authn_gssapi
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_authn_gssapi.so
%endif

%if %{with ldap}
%files mod_authn_ldap
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_authn_ldap.so
%endif

%if %{with pam}
%files mod_authn_pam
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_authn_pam.so
%endif

%if %{with sasl}
%files mod_authn_sasl
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_authn_sasl.so
%endif

%files mod_deflate
%doc doc/outdated/compress.txt
%config(noreplace) %{_sysconfdir}/lighttpd/conf.d/deflate.conf
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_deflate.so

%if %{with gnutls}
%files mod_gnutls
%config(noreplace) /usr/lib/modules-load.d/lighttpd-mod_gnutls.conf
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_gnutls.so
%endif

%if %{with lua}
%files mod_magnet
%doc doc/outdated/magnet.txt
%config(noreplace) %{_sysconfdir}/lighttpd/conf.d/magnet.conf
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_magnet.so
%endif

%if %{with maxminddb}
%files mod_maxminddb
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_maxminddb.so
%endif

%if %{with mbedtls}
%files mod_mbedtls
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_mbedtls.so
%endif

%if %{with nss}
%files mod_nss
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_nss.so
%endif

%if %{with openssl}
%files mod_openssl
%config(noreplace) /usr/lib/modules-load.d/lighttpd-mod_openssl.conf
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_openssl.so
%endif

%if %{with dbi}
%files mod_vhostdb_dbi
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_vhostdb_dbi.so
%endif

%if %{with ldap}
%files mod_vhostdb_ldap
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_vhostdb_ldap.so
%endif

%if %{with mysql}
%files mod_vhostdb_mysql
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_vhostdb_mysql.so
%endif

%if %{with pgsql}
%files mod_vhostdb_pgsql
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_vhostdb_pgsql.so
%endif

%files mod_webdav
%doc doc/outdated/webdav.txt
%config(noreplace) %{_sysconfdir}/lighttpd/conf.d/webdav.conf
%dir %{_libdir}/lighttpd/
%{_libdir}/lighttpd/mod_webdav.so

%files filesystem
%dir %{_sysconfdir}/lighttpd/
%dir %{_sysconfdir}/lighttpd/conf.d/
%dir %{_sysconfdir}/lighttpd/vhosts.d/
%dir %{_var}/run/lighttpd/
%dir %{_var}/lib/lighttpd/
%if %{with tmpfiles}
%ghost %attr(0750, lighttpd, lighttpd) %{_var}/run/lighttpd/
%else
%attr(0750, lighttpd, lighttpd) %{_var}/run/lighttpd/
%endif
%attr(0750, lighttpd, lighttpd) %{_var}/lib/lighttpd/
%attr(0750, lighttpd, lighttpd) %{_var}/log/lighttpd/
%attr(0700, lighttpd, lighttpd) %dir %{webroot}/
%{_sysusersdir}/lighttpd.conf

%changelog
* Fri Sep 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.82-1
- 1.4.82

* Mon Aug 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.81-1
- 1.4.81

* Wed Aug 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.80-1
- 1.4.80

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.79-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.79-2
- Use systemctl kill for logrotate, BZ 2372677.
- Clean up old obs/provides

* Fri Apr 04 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.79-1
- 1.4.79
- Switch to upstream unit file.

* Tue Mar 25 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.78-2
- Rebuild for mbedtls 3.6

* Mon Mar 24 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.78-1
- 1.4.78

* Wed Mar 19 2025 Peter Robinson <pbrobinson@fedoraproject.org> - 1.4.77-5
- Rebuild for mbedtls 3.6

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.77-4
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 1.4.77-3
- Add explicit BR: libxcrypt-devel

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.4.77-1
- 1.4.77

* Tue Sep 03 2024 Morten Stevens <mstevens@fedoraproject.org> - 1.4.76-4
- Rebuilt for mbedTLS 3.6.1

* Mon Jul 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.4.76-3
- Implement upstream spec suggestions.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.4.76-1
- 1.4.76

* Wed Mar 13 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.4.75-1
- 1.4.75

* Tue Feb 20 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.4.74-1
- 1.4.74

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.73-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Florian Weimer <fweimer@redhat.com> - 1.4.73-2
- Fix C compatibility issue in configure script

* Tue Oct 31 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.73-1
- 1.4.73

* Tue Oct 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.72-1
- 1.4.72

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.71-1
- 1.4.71

* Thu May 11 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.70-1
- 1.4.70

* Sun Mar 05 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.69-2
- migrated to SPDX license

* Fri Feb 10 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.69-1
- 1.4.69

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 1.4.68-2
- Remove sysvinit references
- Use make macros

* Wed Jan 04 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.4.68-1
- 1.4.68

* Mon Sep 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.67-1
- 1.4.67

* Tue Aug 09 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.66-1
- 1.4.66

* Thu Jul 28 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.65-5
- Update document-root

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.65-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.65-3
- Drop spawn-fastcgi requirement.

* Thu Jun 16 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.65-2
- Update lua flag, unit file enhancements.

* Wed Jun 08 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.65-1
- 1.4.65

* Sat Jan 22 2022 Morten Stevens <mstevens@fedoraproject.org> - 1.4.64-2
- Rebuilt for mbedTLS 2.28.0

* Wed Jan 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.64-1
- 1.4.64

* Fri Jan 07 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.63-4
- Update lib/httpd permissions.

* Tue Jan 04 2022 Gwyn Ciesla <gwync@protonmail.com> - 1.4.63-3
- Fix typos.

* Wed Dec 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.4.63-2
- Drop mod_authn_mysql, mod_mysql_vhost, mod_geoip
- Add mod_maxminddb, mod_authn_dbi, mod_authn_sasl
- Add mod_vhostdb_dbi mod_vhostdb_mysql mod_vhostdb_pgsql
- Add mod_openssl, mod_gnutls, mod_mbedtls, mod_nss
- mod_deflate built with brotli, zstd
- mod_webdav built with PROPPATCH and LOCK support

* Tue Dec 07 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.4.63-1
- 1.4.63
- Use modern lua.
- Upstream patches for setrlimit, mod_auth trace.
- Migrated to pcre2

* Fri Oct 29 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.4.61-1
- 1.4.61

* Mon Oct 04 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.4.60-1
- 1.4.60, patches for glibc change.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.4.59-4
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4.59-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Feb 02 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.4.59-1
- 1.4.59

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 28 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.58-1
- 1.4.58

* Thu Dec 17 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.57-1
- 1.4.57

* Wed Dec 02 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.56-2
- Drop fam/gamin, no longer used.

* Mon Nov 30 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.56-1
- 1.4.56 final.

* Mon Oct 26 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.56-0.rc1
- 1.4.56 rc1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.55-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.55-3
- Fix tmpfiles for EL-8.

* Mon Apr 27 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.55-2
- Fix ipv6 default config bug.

* Mon Feb 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.55-1
- 1.4.55

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.54-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.4.54-5
- Path corrections, BZ 1789874

* Fri Nov 01 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.4.54-4
- Conditional correction.

* Fri Nov 01 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.4.54-3
- Conditionalize GeoIP, fix logo requires.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 1.4.54-1
- 1.4.54.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Gwyn Ciesla <limburgher@gmail.com> - 1.4.53-1
- 1.4.53.

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.4.52-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Nov 29 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.4.52-1
- 1.4.52.

* Mon Oct 15 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.4.51-1
- 1.4.51.

* Mon Aug 13 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.4.50-1
- 1.4.50.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.49-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.4.49-1
- 1.4.49

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.4.48-3
- Rebuilt for switch to libxcrypt

* Mon Nov 27 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.4.48-2
- Flag corrections, BZ 1516422.

* Mon Nov 13 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.4.48-1
- 1.4.48.

* Mon Oct 23 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.4.47-1
- 1.4.47.

* Wed Sep 20 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.4.45-6
- Switch to mariadb-connector-c, BZ 1493633.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.45-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Jon Ciesla <limburgher@gmail.com> - 1.4.45-2
- Spec cleanup, patch cleanup per upstream.

* Tue Jan 17 2017 Jon Ciesla <limburgher@gmail.com> - 1.4.45-1
- 1.4.45.

* Tue Dec 27 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.44-1
- 1.4.44.

* Thu Dec 15 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.43-3
- Require fedora-logos-httpd, BZ 1387752.
- Move some configs to subpackages, BZ 1387763.
- Create filesystem subpackage for php-fpm integration, BZ 117282.

* Fri Nov 04 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.43-2
- Patch for MySQL deps.

* Mon Oct 31 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.43-1
- 1.4.43.

* Wed Oct 26 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.42-3
- Patch for MySQL deps, split out gssapi and mysql authn modules.

* Mon Oct 17 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.42-2
- Patch for FTBFS

* Mon Oct 17 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.42-1
- 1.4.42, now with included mod_geoip

* Fri Aug 05 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.41-2
- Permissions, defaultconf patch correction, BZ 1201056.

* Mon Aug 01 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.41-1
- 1.4.41

* Wed Jul 27 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.40-4
- Patch for CVE-2016-1000212.

* Thu Jul 21 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.40-3
- Patch for connection state issue.

* Thu Jul 21 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.40-2
- Patch for ipv6 blocking issue.

* Tue Jul 19 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.40-1
- 1.4.40

* Tue Jun 28 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.39-4
- Correct socket location, BZ 1310297.

* Tue Mar 01 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.39-3
- Restored defaultconf, BZ 1310036.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 03 2016 Jon Ciesla <limburgher@gmail.com> - 1.4.39-1
- 1.4.39, BZ 1295149.

* Mon Dec 07 2015 Jon Ciesla <limburgher@gmail.com> - 1.4.38-1
- 1.4.38, BZ 1288708.
- defaultconf patch upstreamed.

* Mon Aug 31 2015 Jon Ciesla <limburgher@gmail.com> - 1.4.37-1
- 1.4.37, BZ 1258284.

* Mon Jul 27 2015 Jon Ciesla <limburgher@gmail.com> - 1.4.36-1
- 1.4.36 1246857, 1224910, 1224911.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.35-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 07 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.35-3
- Use system crypto policy, BZ 1109112.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 12 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.35-1
- 1.4.35, SA-2014-01.

* Fri Feb 21 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.34-4
- Enable lua, BZ 912546.

* Mon Feb 10 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.34-3
- Enable PIE, BZ 955145.

* Mon Feb 10 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.34-2
- Apply Ken Dreyer's spec patches from BZ 850188.

* Wed Feb 05 2014 Jon Ciesla <limburgher@gmail.com> - 1.4.34-1
- 1.4.34, multiple security fixes.

* Mon Aug 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.4.32-1
- Update to 1.4.32, BZ 878915.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Matthias Saou <matthias@saou.eu> 1.4.31-1
- Update to 1.4.31 (#828198).

* Tue Apr 17 2012 Jon Ciesla <limburgher@gmail.com> - 1.4.30-2
- service file patch per BZ 720210.

* Mon Mar 26 2012 Matthias Saou <matthias@saou.eu> 1.4.30-1
- Update to 1.4.30 (#768903).
- Update mod_geoip patch.
- Remove upstreamed ssl_no_ecdh patch.

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.4.29-3
- Rebuild against PCRE 8.30

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Aug 21 2011 Matthias Saou <matthias@saou.eu> 1.4.29-1
- Re-update to 1.4.29, including ssl_no_ecdh to fix build (#625737).

* Mon Jul 11 2011 Matthias Saou <matthias@saou.eu> 1.4.28-3
- Update the defaultconf patch to hint at selinux change to fix server.max-fds.
- Start using %%bcond, including quick defines to also support EL4.
- Include systemd service for F16+, don't add all of the ugly trigger for sysv
  migration (yet : new versions might be released before F16 final) (#720210).

* Sat Jul  9 2011 Matthias Saou <matthias@saou.eu> 1.4.28-2
- Rebase F15 master to the 1.4.28 update.
- Try to update to 1.4.29 (#625737).
- Rebase geoip patch for 1.4.29.
- Update /var/run to work with F15+ (#656612).
- Include all of the new example configuration, with conf.d files and vhosts.d.
- Disable server.max-fds by default since SELinux denies it.

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 1.4.26-4
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  8 2010 Matthias Saou <matthias@saou.eu> 1.4.28-1
- Update to 1.4.28.
- Update defaultconf patch.
- Remove upstreamed ssl-2157 patch.

* Fri Apr 16 2010 Matthias Saou <matthias@saou.eu> 1.4.26-2
- Update to 1.4.26.
- Update the geoip patch.
- Remove no longer provided ChangeLog from %%doc.
- Include patch to fix upstream SSL related bug #2157.

* Thu Sep  3 2009 Matthias Saou <matthias@saou.eu> 1.4.23-1
- Update to 1.4.23.
- Update defaultconf and mod_geoip patches.
- Remove no longer shipped spawn-fcgi, it's a separate source package now.
- Remove unused patch to the init script.

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.4.22-5
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Matthias Saou <matthias@saou.eu> 1.4.22-3
- Update init script to new style.
- No longer include a sysconfig file, though one can be set to override the
  default configuration file location.

* Mon Mar 30 2009 Matthias Saou <matthias@saou.eu> 1.4.22-2
- Update to 1.4.22.
- Add missing defattr for the spawn-fcgi package.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Saou <matthias@saou.eu> 1.4.21-1
- Update to 1.4.21.

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> 1.4.20-7
- rebuild for dependencies

* Wed Dec 24 2008 Matthias Saou <matthias@saou.eu> 1.4.20-6
- Partially revert last change by creating a "spawn-fastcgi" symlink, so that
  nothing breaks currently (especially for EL).
- Install empty poweredby image on RHEL since the symlink's target is missing.
- Split spawn-fcgi off in its own sub-package, have fastcgi package require it
  to provide backwards compatibility.

* Mon Dec 22 2008 Matthias Saou <matthias@saou.eu> 1.4.20-3
- Rename spawn-fastcgi to lighttpd-spawn-fastcgi to avoid clash with other
  packages providing it for their own needs (#472749). It's not used as-is
  by lighttpd, so it shouldn't be a problem... at worst, some custom scripts
  will need to be updated.

* Mon Dec 22 2008 Matthias Saou <matthias@saou.eu> 1.4.20-2
- Include conf.d/*.conf configuration snippets (#444953).
- Mark the default index.html in order to not loose changes upon upgrade if it
  was edited or replaced with a different file (#438564).
- Include patch to add the INIT INFO block to the init script (#246973).

* Mon Oct 13 2008 Matthias Saou <matthias@saou.eu> 1.4.20-1
- Update to 1.4.20 final.

* Mon Sep 22 2008 Matthias Saou <matthias@saou.eu> 1.4.20-0.1.r2303
- Update to 1.4.20 r2303 pre-release.

* Mon Sep 22 2008 Matthias Saou <matthias@saou.eu> 1.4.19-5
- Include memory leak patch (changeset #2305 from ticket #1774).

* Thu Apr 24 2008 Matthias Saou <matthias@saou.eu> 1.4.19-4
- Merge in second changest from upstream fix for upstream bug #285.

* Thu Mar 27 2008 Matthias Saou <matthias@saou.eu> 1.4.19-3
- Include sslshutdown patch, upstream fix to upstream bug #285 (#439066).

* Sat Mar 22 2008 Matthias Saou <matthias@saou.eu> 1.4.19-2
- Provide "webserver" (#437884).

* Wed Mar 12 2008 Matthias Saou <matthias@saou.eu> 1.4.19-1
- Update to 1.4.19, which includes all previous security fixes + bugfixes.

* Tue Mar  4 2008 Matthias Saou <matthias@saou.eu> 1.4.18-6
- Include patch for CVE-2008-0983 (crash when low on file descriptors).
- Include patch for CVE-2008-1111 (cgi source disclosure).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org>
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org>
 - Rebuild for deps

* Wed Oct 31 2007 Matthias Saou <matthias@saou.eu> 1.4.18-3
- Update mod_geoip source to fix segfault upon stopping lighttpd.

* Mon Oct 22 2007 Matthias Saou <matthias@saou.eu> 1.4.18-2
- Include mod_geoip additional source, make it an optional sub-package.
- Reorder sub-packages alphabetically in spec file.
- Make sub-packages require exact release, just in case.
- Change default webroot back from /srv to /var.

* Mon Sep 10 2007 Matthias Saou <matthias@saou.eu> 1.4.18-1
- Update to 1.4.18.
- Include newly installed lighttpd-angel ("angel" process meant to always run
  as root and restart lighttpd when it crashes, spawn processes on SIGHUP), but
  it's in testing stage and must be run with -D for now.

* Wed Sep  5 2007 Matthias Saou <matthias@saou.eu> 1.4.17-1
- Update to 1.4.17.
- Update defaultconf patch to match new example configuration.
- Include patch to fix log file rotation with max-workers set (trac #902).
- Add /var/run/lighttpd/ directory where to put fastcgi sockets.

* Thu Aug 23 2007 Matthias Saou <matthias@saou.eu> 1.4.16-3
- Add /usr/bin/awk build requirement, used to get LIGHTTPD_VERSION_ID.

* Wed Aug 22 2007 Matthias Saou <matthias@saou.eu> 1.4.16-2
- Rebuild to fix wrong execmem requirement on ppc32.

* Thu Jul 26 2007 Matthias Saou <matthias@saou.eu> 1.4.16-1
- Update to 1.4.16 security fix release.

* Mon Apr 16 2007 Matthias Saou <matthias@saou.eu> 1.4.15-1
- Update to 1.4.15.
- Remove now included previous patch.
- Switch to using the bz2 source.
- Add optional --with-webdav-locks support.

* Fri Feb 16 2007 Matthias Saou <matthias@saou.eu> 1.4.13-6
- Include patch to fix 99% cpu bug when client connection is dropped.

* Fri Feb  2 2007 Matthias Saou <matthias@saou.eu> 1.4.13-5
- Update defaultconf patch to change php binary to /usr/bin/php-cgi (#219723).
- Noticed %%{?_smp_mflags} was missing, so add it as it works fine.

* Mon Jan 29 2007 Matthias Saou <matthias@saou.eu> 1.4.13-4
- Remove readline-devel build req, added by lua but since fixed (#213895).

* Mon Nov  6 2006 Matthias Saou <matthias@saou.eu> 1.4.13-3
- Switch to using killall for log rotation to fix it when using workers.

* Mon Oct 16 2006 Matthias Saou <matthias@saou.eu> 1.4.13-2
- Remove gcc-c++ build req, it's part of the defaults.
- Add readline-devel build req, needed on RHEL4.

* Wed Oct 11 2006 Matthias Saou <matthias@saou.eu> 1.4.13-1
- Update to 1.4.13, which contains the previous fix.

* Tue Oct  3 2006 Matthias Saou <matthias@saou.eu> 1.4.12-3
- Include fix for segfaults (lighttpd bug #876, changeset 1352).

* Mon Sep 25 2006 Matthias Saou <matthias@saou.eu> 1.4.12-1
- Update to 1.4.12 final.

* Fri Sep 22 2006 Matthias Saou <matthias@saou.eu> 1.4.12-0.1.r1332
- Update to latest 1.4.12 pre-release, fixes SSL issues and other bugs.
- Update powered_by_fedora.png to the new logo.

* Mon Aug 28 2006 Matthias Saou <matthias@saou.eu> 1.4.11-2
- FC6 rebuild.

* Thu Mar  9 2006 Matthias Saou <matthias@saou.eu> 1.4.11-1
- Update to 1.4.11.

* Mon Mar  6 2006 Matthias Saou <matthias@saou.eu> 1.4.10-2
- FC5 rebuild.

* Wed Feb  8 2006 Matthias Saou <matthias@saou.eu> 1.4.10-1
- Update to 1.4.10.
- Remove now included fix.

* Wed Jan 25 2006 Matthias Saou <matthias@saou.eu> 1.4.9-2
- Add mod_fastcgi-fix patch to fix crash on backend overload.

* Mon Jan 16 2006 Matthias Saou <matthias@saou.eu> 1.4.9-1
- Update to 1.4.9.

* Wed Nov 23 2005 Matthias Saou <matthias@saou.eu> 1.4.8-1
- Update to 1.4.8.

* Fri Nov  4 2005 Matthias Saou <matthias@saou.eu> 1.4.7-1
- Update to 1.4.7.

* Wed Oct 12 2005 Matthias Saou <matthias@saou.eu> 1.4.6-1
- Update to 1.4.6.

* Mon Oct  3 2005 Matthias Saou <matthias@saou.eu> 1.4.5-1
- Update to 1.4.5.
- Disable gamin/fam support for now, it does not work.

* Tue Sep 27 2005 Matthias Saou <matthias@saou.eu> 1.4.4-3
- Update to current SVN to check if it fixes the remaining load problems.

* Wed Sep 21 2005 Matthias Saou <matthias@saou.eu> 1.4.4-2
- Patch to SVN 722 revision : Fixes a crash in mod_mysql_vhost and a problem
  with keepalive and certain browsers.

* Mon Sep 19 2005 Matthias Saou <matthias@saou.eu> 1.4.4-1
- Update to 1.4.4 final.
- Enable ldap auth, gdbm and gamin/fam support by default.

* Thu Sep 15 2005 Matthias Saou <matthias@saou.eu> 1.4.4-0
- Update to 1.4.4 pre-release (fixes another fastcgi memleak).
- Enable lua (cml module) by default.
- Add --with-webdav-props conditional option.

* Tue Sep 13 2005 Matthias Saou <matthias@saou.eu> 1.4.3-2
- Include lighttpd-1.4.3-stat_cache.patch to fix memleak.

* Fri Sep  2 2005 Matthias Saou <matthias@saou.eu> 1.4.3-1.1
- Rearrange the included index.html to include the new logo, button and
  favicon from lighttpd.net.

* Fri Sep  2 2005 Matthias Saou <matthias@saou.eu> 1.4.3-1
- Update to 1.4.3.
- No longer override libdir at make install stage, use DESTDIR instead, as
  the resulting binary would now have referenced to %%{buildroot} :-(

* Tue Aug 30 2005 Matthias Saou <matthias@saou.eu> 1.4.2-1
- Update to 1.4.2.

* Mon Aug 22 2005 Matthias Saou <matthias@saou.eu> 1.4.1-1
- Update to 1.4.1.

* Sun Aug 21 2005 Matthias Saou <matthias@saou.eu> 1.4.0-1
- Update to 1.4.0.
- Add conditional of gamin, gdbm, memcache and lua options.

* Mon Aug  1 2005 Matthias Saou <matthias@saou.eu> 1.3.16-2
- Update to 1.3.16, rebuild.

* Mon Jul 18 2005 Matthias Saou <matthias@saou.eu> 1.3.15-1
- Update to 1.3.15.

* Mon Jun 20 2005 Matthias Saou <matthias@saou.eu> 1.3.14-1
- Update to 1.3.14.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.3.13-5
- rebuild on all arches

* Mon Apr  4 2005 Matthias Saou <matthias@saou.eu> 1.3.13-4
- Change signal sent from the logrotate script from USR1 to HUP, as that's the
  correct one.

* Fri Apr  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 1.3.13-2
- Include /etc/lighttpd directory.

* Sun Mar  6 2005 Matthias Saou <matthias@saou.eu> 1.3.13-1
- Update to 1.3.13.

* Wed Mar  2 2005 Matthias Saou <matthias@saou.eu> 1.3.12-1
- Update to 1.3.12.
- Remove obsolete empty_cgi_handler patch.

* Tue Mar  1 2005 Matthias Saou <matthias@saou.eu> 1.3.11-2
- Add missing defattr to sub-packages (#150018).

* Mon Feb 21 2005 Matthias Saou <matthias@saou.eu> 1.3.11-0
- Update to 1.3.11.
- Remove cleanconf and init.d patches (merged upstream).
- Add empty_cgi_handler patch.

* Fri Feb 18 2005 Matthias Saou <matthias@saou.eu> 1.3.10-0
- Split off -fastcgi sub-package.
- Include php.d entry to set sane FastCGI defaults.

* Wed Feb 16 2005 Matthias Saou <matthias@saou.eu> 1.3.10-0
- Spec file cleanup for freshrpms.net/Extras.
- Compile OpenSSL support unconditionally.
- Put modules in a subdirectory of libdir.
- Don't include all of libdir's content to avoid debuginfo content.
- Add optional LDAP support.
- Add patch to change the default configuration.
- Add dedicated lighttpd user/group creation.
- Add logrotate entry.
- Include a nice little default page for the default setup.
- Split off mod_mysql_vhost sub-package, get dep only there.
- Use webroot in /srv by default.
- Exclude .la files, I doubt anyone will need them.

* Thu Sep 30 2004 <jan@kneschke.de> 1.3.1
- upgraded to 1.3.1

* Tue Jun 29 2004 <jan@kneschke.de> 1.2.3
- rpmlint'ed the package
- added URL
- added (noreplace) to start-script
- change group to Networking/Daemon (like apache)

* Sun Feb 23 2003 <jan@kneschke.de>
- initial version

