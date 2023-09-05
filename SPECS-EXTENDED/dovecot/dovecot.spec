%global __provides_exclude_from %{_docdir}
%global __requires_exclude_from %{_docdir}
%global prever %{nil}
%global pigeonholever 0.5.20

Summary:        Secure imap and pop3 server
Name:           dovecot
Version:        2.3.20
Release:        1%{?dist}
#dovecot itself is MIT, a few sources are PD, pigeonhole is LGPLv2
License:        MIT AND LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.dovecot.org/
Source:         https://www.dovecot.org/releases/2.3/%{name}-%{version}%{?prever}.tar.gz
Source1:        dovecot.init
Source2:        dovecot.pam
Source8:        https://pigeonhole.dovecot.org/releases/2.3/dovecot-2.3-pigeonhole-%{pigeonholever}.tar.gz
Source9:        dovecot.sysconfig
Source10:       dovecot.tmpfilesd
#our own
Source14:       dovecot.conf.5
Source15:       prestartscript
# 3x Fedora/RHEL specific
Patch1:         dovecot-2.0-defaultconfig.patch
Patch2:         dovecot-1.0.beta2-mkcert-permissions.patch
Patch3:         dovecot-1.0.rc7-mkcert-paths.patch
#wait for network
Patch6:         dovecot-2.1.10-waitonline.patch
Patch8:         dovecot-2.2.20-initbysystemd.patch
Patch9:         dovecot-2.2.22-systemd_w_protectsystem.patch
Patch10:        dovecot-2.3.0.1-libxcrypt.patch
Patch15:        dovecot-2.3.11-bigkey.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bzip2-devel
BuildRequires:  clucene-core-devel
BuildRequires:  expat-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
# gettext-devel is needed for running autoconf because of the
# presence of AM_ICONV
BuildRequires:  gettext-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libcurl-devel
BuildRequires:  libexttextcat-devel
BuildRequires:  libicu-devel
BuildRequires:  libpq-devel
BuildRequires:  libsodium-devel
BuildRequires:  libstemmer-devel
BuildRequires:  libtool
BuildRequires:  libxcrypt-devel
BuildRequires:  libzstd-devel
BuildRequires:  lz4-devel
BuildRequires:  make
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
BuildRequires:  quota-devel
BuildRequires:  sqlite-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
# Explicit Runtime Requirements for executalbe
Requires:       openssl >= 0.9.7f-4
# Package includes an initscript service file, needs to require initscripts package
Requires(pre): shadow-utils
Requires: systemd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%global ssldir %{_sysconfdir}/pki/%{name}
%global restart_flag /run/%{name}/%{name}-restart-after-rpm-install

%description
Dovecot is an IMAP server for Linux/UNIX-like systems, written with security
primarily in mind.  It also contains a small POP3 server.  It supports mail
in either of maildir or mbox formats.

The SQL drivers and authentication plug-ins are in their subpackages.

%package pigeonhole
Summary:        Sieve and managesieve plug-in for dovecot
Requires:       %{name} = %{version}-%{release}

%description pigeonhole
This package provides sieve and managesieve plug-in for dovecot LDA.

%package pgsql
Summary:        Postgres SQL back end for dovecot
Requires:       %{name} = %{version}-%{release}

%description pgsql
This package provides the Postgres SQL back end for dovecot-auth etc.

%package mysql
Summary:        MySQL back end for dovecot
Requires:       %{name} = %{version}-%{release}

%description mysql
This package provides the MySQL back end for dovecot-auth etc.

%package devel
Summary:        Development files for dovecot
Requires:       %{name} = %{version}-%{release}

%description devel
This package provides the development files for dovecot.

%prep
%setup -q -n %{name}-%{version}%{?prever} -a 8
%patch1 -p1 -b .default-settings
%patch2 -p1 -b .mkcert-permissions
%patch3 -p1 -b .mkcert-paths
%patch6 -p1 -b .waitonline
%patch8 -p1 -b .initbysystemd
%patch9 -p1 -b .systemd_w_protectsystem
%patch15 -p1 -b .bigkey

#pushd dovecot-2*3-pigeonhole-%{pigeonholever}
#popd
sed -i '/DEFAULT_INCLUDES *=/s|$| '"$(pkg-config --cflags libclucene-core)|" src/plugins/fts-lucene/Makefile.in

%build
# This package references hidden symbols during an LTO link.  This needs further
# investigation.  Until then, disable LTO
%define _lto_cflags %{nil}
#required for fdpass.c line 125,190: dereferencing type-punned pointer will break strict-aliasing rules
%global _hardened_build 1
export CFLAGS="%{__global_cflags} -fno-strict-aliasing -fstack-reuse=none"
export LDFLAGS="-Wl,-z,now -Wl,-z,relro %{?__global_ldflags}"
mkdir -p m4
autoreconf -I . -fiv #required for aarch64 support
%configure                       \
    INSTALL_DATA="install -c -p -m644" \
    --with-rundir=%{_rundir}/%{name}   \
    --docdir=%{_docdir}/%{name}  \
    --disable-static             \
    --disable-rpath              \
    --with-nss                   \
    --with-shadow                \
    --with-pam                   \
    --with-gssapi=plugin         \
    --with-ldap=plugin           \
    --with-sql=plugin            \
    --with-pgsql                 \
    --with-mysql                 \
    --with-sqlite                \
    --with-zlib                  \
    --with-zstd                  \
    --with-libcap                \
    --with-icu                   \
    --with-lucene                \
    --with-ssl=openssl           \
    --with-ssldir=%{ssldir}      \
    --with-solr                  \
    --with-docs                  \
    systemdsystemunitdir=%{_unitdir}

sed -i 's|/etc/ssl|/etc/pki/dovecot|' doc/mkcert.sh doc/example-config/conf.d/10-ssl.conf

make %{?_smp_mflags}

#pigeonhole
pushd dovecot-2*3-pigeonhole-%{pigeonholever}

# required for snapshot
[ -f configure ] || autoreconf -fiv
[ -f ChangeLog ] || echo "Pigeonhole ChangeLog is not available, yet" >ChangeLog

%configure                             \
    INSTALL_DATA="install -c -p -m644" \
    --disable-static                   \
    --with-dovecot=../                 \
    --without-unfinished-features

make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

#move doc dir back to build dir so doc macro in files section can use it
mv $RPM_BUILD_ROOT/%{_docdir}/%{name} %{_builddir}/%{name}-%{version}%{?prever}/docinstall


pushd dovecot-2*3-pigeonhole-%{pigeonholever}
make install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/%{_docdir}/%{name} $RPM_BUILD_ROOT/%{_docdir}/%{name}-pigeonhole

install -m 644 AUTHORS ChangeLog COPYING COPYING.LGPL INSTALL NEWS README $RPM_BUILD_ROOT/%{_docdir}/%{name}-pigeonhole
popd

install -p -D -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/dovecot

#install man pages
install -p -D -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_mandir}/man5/dovecot.conf.5

#install waitonline script
install -p -D -m 755 %{SOURCE15} $RPM_BUILD_ROOT%{_libexecdir}/dovecot/prestartscript

# generate ghost .pem files
mkdir -p $RPM_BUILD_ROOT%{ssldir}/certs
mkdir -p $RPM_BUILD_ROOT%{ssldir}/private
touch $RPM_BUILD_ROOT%{ssldir}/certs/dovecot.pem
chmod 600 $RPM_BUILD_ROOT%{ssldir}/certs/dovecot.pem
touch $RPM_BUILD_ROOT%{ssldir}/private/dovecot.pem
chmod 600 $RPM_BUILD_ROOT%{ssldir}/private/dovecot.pem

install -p -D -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_tmpfilesdir}/dovecot.conf

mkdir -p $RPM_BUILD_ROOT/run/dovecot/{login,empty,token-login}

# Install dovecot configuration and dovecot-openssl.cnf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/conf.d
install -p -m 644 docinstall/example-config/dovecot.conf $RPM_BUILD_ROOT%{_sysconfdir}/dovecot
install -p -m 644 docinstall/example-config/conf.d/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/conf.d
install -p -m 644 $RPM_BUILD_ROOT/%{_docdir}/%{name}-pigeonhole/example-config/conf.d/*.conf $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/conf.d
install -p -m 644 docinstall/example-config/conf.d/*.conf.ext $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/conf.d
install -p -m 644 $RPM_BUILD_ROOT/%{_docdir}/%{name}-pigeonhole/example-config/conf.d/*.conf.ext $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/conf.d ||:
install -p -m 644 doc/dovecot-openssl.cnf $RPM_BUILD_ROOT%{ssldir}/dovecot-openssl.cnf

install -p -m755 doc/mkcert.sh $RPM_BUILD_ROOT%{_libexecdir}/%{name}/mkcert.sh

mkdir -p $RPM_BUILD_ROOT/var/lib/dovecot

#remove the libtool archives
find $RPM_BUILD_ROOT%{_libdir}/%{name}/ -name '*.la' | xargs rm -f

#remove what we don't want
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/README
pushd docinstall
rm -f securecoding.txt thread-refs.txt
popd


%pre
#dovecot uid and gid are reserved, see /usr/share/doc/setup-*/uidgid
getent group dovecot >/dev/null || groupadd -r --gid 97 dovecot
getent passwd dovecot >/dev/null || \
useradd -r --uid 97 -g dovecot -d /usr/libexec/dovecot -s /usr/sbin/nologin -c "Dovecot IMAP server" dovecot

getent group dovenull >/dev/null || groupadd -r dovenull
getent passwd dovenull >/dev/null || \
useradd -r -g dovenull -d /usr/libexec/dovecot -s /usr/sbin/nologin -c "Dovecot's unauthorized user" dovenull

# do not let dovecot run during upgrade rhbz#134325
if [ "$1" = "2" ]; then
  rm -f %restart_flag
  /bin/systemctl is-active %{name}.service >/dev/null 2>&1 && touch %restart_flag ||:
  /bin/systemctl stop %{name}.service >/dev/null 2>&1
fi

%post
if [ $1 -eq 1 ]
then
  %systemd_post dovecot.service
fi

install -d -m 0755 -g dovecot -d /run/dovecot
install -d -m 0755 -d /run/dovecot/empty
install -d -m 0750 -g dovenull -d /run/dovecot/login
install -d -m 0750 -g dovenull -d /run/dovecot/token-login
[ -x /sbin/restorecon ] && /sbin/restorecon -R /run/dovecot

%preun
if [ $1 = 0 ]; then
        /bin/systemctl disable dovecot.service dovecot.socket >/dev/null 2>&1 || :
        /bin/systemctl stop dovecot.service dovecot.socket >/dev/null 2>&1 || :
    rm -rf /run/dovecot
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

if [ "$1" -ge "1" -a -e %restart_flag ]; then
    /bin/systemctl start dovecot.service >/dev/null 2>&1 || :
rm -f %restart_flag
fi

%posttrans
# dovecot should be started again in %%postun, but it's not executed on reinstall
# if it was already started, restart_flag won't be here, so it's ok to test it again
if [ -e %restart_flag ]; then
    /bin/systemctl start dovecot.service >/dev/null 2>&1 || :
rm -f %restart_flag
fi

%check
make check
cd dovecot-2*3-pigeonhole-%{pigeonholever}
make check

%files
%doc docinstall/* AUTHORS ChangeLog COPYING COPYING.LGPL COPYING.MIT NEWS README
%{_sbindir}/dovecot

%{_bindir}/doveadm
%{_bindir}/doveconf
%{_bindir}/dsync
%{_bindir}/dovecot-sysreport


%_tmpfilesdir/dovecot.conf
%{_unitdir}/dovecot.service
%{_unitdir}/dovecot-init.service
%{_unitdir}/dovecot.socket

%dir %{_sysconfdir}/dovecot
%dir %{_sysconfdir}/dovecot/conf.d
%config(noreplace) %{_sysconfdir}/dovecot/dovecot.conf
#list all so we'll be noticed if upstream changes anything
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-auth.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-director.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-logging.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-mail.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-master.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-metrics.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/10-ssl.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/15-lda.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/15-mailboxes.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/20-imap.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/20-lmtp.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/20-pop3.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/20-submission.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/90-acl.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/90-quota.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/90-plugin.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-checkpassword.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-deny.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-dict.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-ldap.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-master.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-passwdfile.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-sql.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-static.conf.ext
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/auth-system.conf.ext

%config(noreplace) %{_sysconfdir}/pam.d/dovecot
%config(noreplace) %{ssldir}/dovecot-openssl.cnf

%dir %{ssldir}
%dir %{ssldir}/certs
%dir %{ssldir}/private
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssldir}/certs/dovecot.pem
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{ssldir}/private/dovecot.pem

%dir %{_libdir}/dovecot
%dir %{_libdir}/dovecot/auth
%dir %{_libdir}/dovecot/dict
%{_libdir}/dovecot/doveadm
%exclude %{_libdir}/dovecot/doveadm/*sieve*
%{_libdir}/dovecot/*.so.*
#these (*.so files) are plugins, not devel files
%{_libdir}/dovecot/*_plugin.so
%exclude %{_libdir}/dovecot/*_sieve_plugin.so
%{_libdir}/dovecot/auth/lib20_auth_var_expand_crypt.so
%{_libdir}/dovecot/auth/libauthdb_imap.so
%{_libdir}/dovecot/auth/libauthdb_ldap.so
%{_libdir}/dovecot/auth/libmech_gssapi.so
%{_libdir}/dovecot/auth/libdriver_sqlite.so
%{_libdir}/dovecot/dict/libdriver_sqlite.so
%{_libdir}/dovecot/dict/libdict_ldap.so
%{_libdir}/dovecot/libdriver_sqlite.so
%{_libdir}/dovecot/libssl_iostream_openssl.so
%{_libdir}/dovecot/libfs_compress.so
%{_libdir}/dovecot/libfs_crypt.so
%{_libdir}/dovecot/libfs_mail_crypt.so
%{_libdir}/dovecot/libdcrypt_openssl.so
%{_libdir}/dovecot/lib20_var_expand_crypt.so
%{_libdir}/dovecot/old-stats/libold_stats_mail.so
%{_libdir}/dovecot/old-stats/libstats_auth.so

%dir %{_libdir}/dovecot/settings

%{_libexecdir}/%{name}
%exclude %{_libexecdir}/%{name}/managesieve*

%dir %attr(0755,root,dovecot) %ghost /run/dovecot
%attr(0750,root,dovenull) %ghost /run/dovecot/login
%attr(0750,root,dovenull) %ghost /run/dovecot/token-login
%attr(0755,root,root) %ghost /run/dovecot/empty

%attr(0750,dovecot,dovecot) /var/lib/dovecot

%{_datadir}/%{name}

%{_mandir}/man1/deliver.1*
%{_mandir}/man1/doveadm*.1*
%{_mandir}/man1/doveconf.1*
%{_mandir}/man1/dovecot*.1*
%{_mandir}/man1/dsync.1*
%{_mandir}/man5/dovecot.conf.5*
%{_mandir}/man7/doveadm-search-query.7*

%files devel
%{_includedir}/dovecot
%{_datadir}/aclocal/dovecot*.m4
%{_libdir}/dovecot/libdovecot*.so
%{_libdir}/dovecot/dovecot-config

%files pigeonhole
%{_bindir}/sieve-dump
%{_bindir}/sieve-filter
%{_bindir}/sieve-test
%{_bindir}/sievec
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/20-managesieve.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/90-sieve.conf
%config(noreplace) %{_sysconfdir}/dovecot/conf.d/90-sieve-extprograms.conf

%{_docdir}/%{name}-pigeonhole

%{_libexecdir}/%{name}/managesieve
%{_libexecdir}/%{name}/managesieve-login

%{_libdir}/dovecot/doveadm/*sieve*
%{_libdir}/dovecot/*_sieve_plugin.so
%{_libdir}/dovecot/settings/libmanagesieve_*.so
%{_libdir}/dovecot/settings/libpigeonhole_*.so
%{_libdir}/dovecot/sieve/

%{_mandir}/man1/sieve-dump.1*
%{_mandir}/man1/sieve-filter.1*
%{_mandir}/man1/sieve-test.1*
%{_mandir}/man1/sievec.1*
%{_mandir}/man1/sieved.1*
%{_mandir}/man7/pigeonhole.7*

%files mysql
%{_libdir}/%{name}/libdriver_mysql.so
%{_libdir}/%{name}/auth/libdriver_mysql.so
%{_libdir}/%{name}/dict/libdriver_mysql.so

%files pgsql
%{_libdir}/%{name}/libdriver_pgsql.so
%{_libdir}/%{name}/auth/libdriver_pgsql.so
%{_libdir}/%{name}/dict/libdriver_pgsql.so

%changelog
* Wed Aug 30 2023 Archana Choudhary <archana1@microsoft.com> - 2.3.20-1
- Upgrade to 2.3.20
- Resolves: CVE-2021-33515 CVE-2021-29157 CVE-2022-30550 CVE-2020-28200
- Update patch #6 and #8
- Remove patch #16 as it is not needed
- Update files
- Verified license

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.3.13-5
- Remove epoch

* Fri Oct 08 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.13-4
- Adding missing BR on 'systemd-rpm-macros'.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.13-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Thu Jan 07 2021 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.13-2
- fix rundir location

* Wed Jan 06 2021 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.13-1
- fix release number

* Mon Jan 04 2021 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.13-0
- dovecot updated to 2.3.13, pigeonhole to 0.5.13
- CVE-2020-24386: Specially crafted command can cause IMAP hibernate to
  allow logged in user to access other people's emails and filesystem
  information.
- Metric filter and global event filter variable syntax changed to a
  SQL-like format. 
- auth: Added new aliases for %{variables}. Usage of the old ones is
  possible, but discouraged.
- auth: Removed RPA auth mechanism, SKEY auth mechanism, NTLM auth
  mechanism and related password schemes.
- auth: Removed passdb-sia, passdb-vpopmail and userdb-vpopmail.
- auth: Removed postfix postmap socket

* Wed Oct 21 2020 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.11.3-7
- change run directory from /var/run to /run (#1777922)

* Wed Oct 21 2020 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.11.3-6
- use bigger default key size (#1882939)

* Wed Sep 02 2020 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.11.3-5
- fix gssapi issue

* Wed Aug 26 2020 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.11.3-4
- fix FTBFS on 32bit systems

* Mon Aug 17 2020 Jeff Law <law@redhat.com> - 1:2.3.11.3-2
- Disable LTO

* Sat Aug 15 2020 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.11.3-1
- CVE-2020-12100: Parsing mails with a large number of MIME parts could
  have resulted in excessive CPU usage or a crash due to running out of
  stack memory.
- CVE-2020-12673: Dovecot's NTLM implementation does not correctly check
  message buffer size, which leads to reading past allocation which can
  lead to crash.
- CVE-2020-10967: lmtp/submission: Issuing the RCPT command with an
  address that has the empty quoted string as local-part causes the lmtp
  service to crash.
- CVE-2020-12674: Dovecot's RPA mechanism implementation accepts
  zero-length message, which leads to assert-crash later on.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.10.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 18 2020 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.10.1-1
- dovecot updated to 2.3.10.1
- fixes CVE-2020-10967, CVE-2020-10958, CVE-2020-10957

* Tue Apr 21 2020 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.10-1
- dovecot updated to 2.3.10, pigeonhole updated to 0.5.10

* Wed Feb 12 2020 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.9.3-1
- dovecot updated to 2.3.9.3
- fixes CVE-2020-7046: Truncated UTF-8 can be used to DoS
      submission-login and lmtp processes.
- fixes CVE-2020-7957: Specially crafted mail can crash snippet generation.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 19 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.9.2-1
- CVE-2019-19722: Mails with group addresses in From or To fields
  caused crash in push notification drivers.

* Wed Dec 04 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.9-1
- dovecot updated to 2.3.9, pigeonhole updated to 0.5.9 

* Thu Oct 10 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.8-1
- dovecot updated to 2.3.8, pigeonhole 0.5.8

* Thu Aug 29 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.7.2-1
- dovecot updated to 2.3.7.2, pigeonhole 0.5.7.2
- fixes CVE-2019-11500: IMAP protocol parser does not properly handle NUL byte
  when scanning data in quoted strings, leading to out of bounds heap
  memory writes

* Mon Aug 19 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:1-2.3.7.1
- dovecot updated to 2.3.7.1, pigeonhole updated to 0.5.7.1

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.6-3
- disable gcc 9 stack reuse temporarily

* Mon May 13 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.6-2
- use /run instead of /var/run (#1706372)

* Thu May 02 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.6-1
- dovecot updated to 2.3.6, pigeonhole updated to 0.5.6

* Thu Apr 18 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.5.2-1
- dovecot updated to 2.3.5.2
- fixes CVE-2019-10691: Trying to login with 8bit username containing
  invalid UTF8 input causes auth process to crash if auth policy is enabled.

* Thu Mar 28 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.5.1-1
- dovecot updated to 2.3.5.1
- CVE-2019-7524: Missing input buffer size validation leads into
  arbitrary buffer overflow when reading fts or pop3 uidl header
  from Dovecot index.

* Wed Mar 06 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.5-1
- dovecot updated to 2.3.5, pigeonhole updated to 0.5.5

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1:2.3.4-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Wed Jan 09 2019 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.4-1
- dovecot updated to 2.3.4, pigeonhole updated to 0.5.4

* Tue Oct 02 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.3-1
- dovecot updated to 2.3.3, pigeonhole pdated to 0.5.3
- doveconf hides more secrets now in the default output
- NUL bytes in mail headers can cause truncated replies when fetched. 
- virtual plugin: Some searches used 100% CPU for many seconds 
- dsync assert-crashed with acl plugin in some situations. 
- imapc: Fixed various assert-crashes when reconnecting to server. 

* Tue Oct 02 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.2.1-4
- fix dovecot-init service syntax error (#1635017)

* Mon Aug 13 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.2.1-3
- do not try to generate ssl-params as its obsolete (#1614640)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.2.1-1
- SSL/TLS servers may have crashed during client disconnection

* Mon Jul 09 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.2-1
- dovecot updated to 2.3.2, pigeonhole to 0.5.2

* Wed Mar 28 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.1-2
- fix ftbfs - murmurhash3 check fail

* Wed Mar 28 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.1-1
- dovecot updated to 2.3.1, pigeonhole updated to 0.5.1

* Tue Mar 27 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.0.1-3
- use libxcrypt for Fedora >= 28, part of ftbfs fix (#1548520)

* Wed Mar 07 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.0.1-2
- add gcc buildrequire

* Thu Mar 01 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.3.0.1-1
- dovecot updated to 2.3.0.1, pigeonhole updated to 0.5.0.1

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:2.2.33.2-5
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.33.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1:2.2.33.2-3
- Rebuilt for switch to libxcrypt

* Mon Jan 08 2018 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.33.2-2
- remove tcp_wrappers on Fedora 28 and later (#1518761)
- use use mariadb-connector-c-devel instead of mysql-devel on Fedora 28 and later (#1493624)

* Tue Oct 24 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.33.2-1
- dovecot updated to 2.2.33.2
- doveadm: Fix crash in proxying (or dsync replication) if remote is
  running older than v2.2.33
- auth: Fix memory leak in %%{ldap_dn}
- dict-sql: Fix data types to work correctly with Cassandra

* Wed Oct 18 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.33.1-1
- dovecot updated to 2.2.33.1, pigeonhole updated to 
- Added %%{if}, see https://wiki2.dovecot.org/Variables#Conditionals
- sdbox: Mails were always opened when expunging, unless
  mail_attachment_fs was explicitly set to empty.
- lmtp/doveadm proxy: hostip passdb field was ignored, which caused
  unnecessary DNS lookups if host field wasn't an IP
- lmtp proxy: Fix crash when receiving unexpected reply in RCPT TO
- quota_clone: Update also when quota is unlimited (broken in v2.2.31)
- mbox, zlib: Fix assert-crash when accessing compressed mbox
- doveadm director kick -f parameter didn't work
- doveadm director flush <host> resulted flushing all hosts, if <host>
  wasn't an IP address.
- director: Various fixes to handling backend/director changes at
   abnormal times, especially while ring was unsynced.
- director: Use less CPU in imap-login processes when moving/kicking
  many users.
- lmtp: Session IDs were duplicated/confusing with multiple RCPT TOs
  when lmtp_rcpt_check_quota=yes
- LDA Sieve plugin: Fixed sequential execution of LDAP-based scripts. A
  missing LDAP-based script could cause the script sequence to exit earlier.
- sieve-filter: Removed the (now) duplicate utf8 to mutf7 mailbox name
  conversion. This caused problems with mailbox names containing UTF-8
  characters. 

* Mon Aug 28 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.32-2
- pigeonhole updated to 0.4.20
- Made the retention period for redirect duplicate identifiers
  configurable. Changed the default retention period from 24 to 12 hours.
- sieve-filter: Fixed memory leak: forgot to clean up script binary at
  end of execution
- managesieve-login: Fixed handling of AUTHENTICATE command. A second
  authenticate command would be parsed wrong.

* Fri Aug 25 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.32-1
- dovecot updated to 2.2.32
- Modseq tracking didn't always work correctly. This could have caused
  imap unhibernation to fail or IMAP QRESYNC/CONDSTORE extensions to
  not work perfectly.
- mdbox: "Inconsistency in map index" wasn't fixed automatically
- dict-ldap: %%variable values used in the LDAP filter weren't escaped.
- quota=count: quota_warning = -storage=.. was never executed (try #2).
- imapc: >= 32 kB mail bodies were supposed to be cached for subsequent
  FETCHes, but weren't.
- quota-status service didn't support recipient_delimiter
- acl: Don't access dovecot-acl-list files with acl_globals_only=yes
- mail_location: If INDEX dir is set, mailbox deletion deletes its
  childrens' indexes. 
- director: v2.2.31 caused rapid reconnection loops to directors
  that were down.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 11 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.31-3
- enable tcpwrap support (#1450587)

* Tue Jul 04 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.31-2
- revert commit breaking NOTIFY support

* Tue Jun 27 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.31-1
- dovecot updated to 2.2.31
- Various fixes to handling mailbox listing. Especially related to
  handling nonexistent autocreated/autosubscribed mailboxes and ACLs.
- Global ACL file was parsed as if it was local ACL file. This caused
  some of the ACL rule interactions to not work exactly as intended.
- Using mail_sort_max_read_count may have caused very high CPU usage.
- Message address parsing could have crashed on invalid input.
- imapc_features=fetch-headers wasn't always working correctly and
  caused the full header to be fetched.
- imapc: Various bugfixes related to connection failure handling.
- quota=count: quota_warning = -storage=.. was never executed
- quota=count: Add support for "ns" parameter
- dsync: Fix incremental syncing for mails that don't have Date or
  Message-ID headers.
- imap: Fix hang when client sends pipelined SEARCH +
  EXPUNGE/CLOSE/LOGOUT.
- oauth2: Token validation didn't accept empty server responses.
- imap: NOTIFY command has been almost completely broken since the
  beginning.
- pigeonhole updated to 0.4.19
- Fixed bug in handling of implicit keep in some cases.
- include extension: Fixed segfault that (sometimes) occurred when the
  global script location was left unconfigured.

* Wed Jun 07 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.30.2-1
- dovecot updated to 2.2.30.2
- auth: Multiple failed authentications within short time caused crashes
- push-notification: OX driver crashed at deinit

* Thu Jun 01 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.30.1-1
- dovecot updated to 2.2.30.1
- More fixes to automatically fix corruption in dovecot.list.index
- dsync-server: Fix support for dsync_features=empty-header-workaround
- imapc: Various bugfixes, including infinite loops on some errors
- IMAP NOTIFY wasn't working for non-INBOX if IMAP client hadn't
  enabled modseq tracking via CONDSTORE/QRESYNC.
- fts-lucene: Fix it to work again with mbox format
- Some internal error messages may have contained garbage in v2.2.29
- mail-crypt: Re-encrypt when copying/moving mails and per-mailbox keys
  are used. Otherwise the copied mails can't be opened.

* Wed Apr 12 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.29.1-1
- dovecot updated to 2.2.29.1
- dict-sql: Merging multiple UPDATEs to a single statement wasn't
  actually working.
- pigeonhole updated to 0.4.18
- imapsieve plugin: Implemented the copy_source_after rule action. When this
  is enabled for a mailbox rule, the specified Sieve script is executed for
  the message in the source mailbox during a "COPY" event. This happens only
  after the Sieve script that is executed for the corresponding message in the
  destination mailbox finishes running successfully.
- imapsieve plugin: Added non-standard Sieve environment items for the source
  and destination mailbox.
- multiscript: The execution of the discard script had an implicit "keep",
  rather than an implicit "discard". 

* Tue Apr 11 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.29-1
- dovecot updated to 2.2.29
- fts-tika: Fixed crash when parsing attachment without
  Content-Disposition header. Broken by 2.2.28.
- trash plugin was broken in 2.2.28
- auth: When passdb/userdb lookups were done via auth-workers, too much
  data was added to auth cache. This could have resulted in wrong
  replies when using multiple passdbs/userdbs.
- auth: passdb { skip & mechanisms } were ignored for the first passdb
- oauth2: Various fixes, including fixes to crashes
- dsync: Large Sieve scripts (or other large metadata) weren't always
  synced.
- Index rebuild (e.g. doveadm force-resync) set all mails as \Recent
- imap-hibernate: %%{userdb:*} wasn't expanded in mail_log_prefix
- doveadm: Exit codes weren't preserved when proxying commands via
  doveadm-server. Almost all errors used exit code 75 (tempfail).
- ACLs weren't applied to not-yet-existing autocreated mailboxes.
- Fixed a potential crash when parsing a broken message header.
- cassandra: Fallback consistency settings weren't working correctly.
- doveadm director status <user>: "Initial config" was always empty
- imapc: Various reconnection fixes.

* Mon Feb 27 2017 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.28-1
- dovecot updated to 2.2.28, pigeonhole to 0.4.17
- auth: Support OAUTHBEARER and XOAUTH2 mechanisms. Also support them
  in lib-dsasl for client side.
- imap: SEARCH/SORT may have assert-crashed in
  client_check_command_hangs
- imap: FETCH X-MAILBOX may have assert-crashed in virtual mailboxes.
- search: Using NOT n:* or NOT UID n:* wasn't handled correctly
- fts: fts_autoindex_exclude = \Special-use caused crashes
- doveadm-server: Fix leaks and other problems when process is reused
  for multiple requests (service_count != 1)
- sdbox: Fix assert-crash on mailbox create race
- lda/lmtp: deliver_log_format values weren't entirely correct if Sieve
  was used. especially %%{storage_id} was broken.
- imapsieve plugin: Fixed assert failure occurring when used with virtual
  mailboxes.
- doveadm sieve plugin: Fixed crash when setting Sieve script via attribute's
  string value.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Than Ngo <than@redhat.com> - 1:2.2.27-2
- fixed bz#1403760, big endian issue

* Mon Dec 05 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.27-1
- Fixed crash in auth process when auth-policy was configured and
  authentication was aborted/failed without a username set.
- director: If two users had different tags but the same hash,
  the users may have been redirected to the wrong tag's hosts.
- Index files may have been thought incorrectly lost, causing
  "Missing middle file seq=.." to be logged and index rebuild.
  This happened more easily with IMAP hibernation enabled.
- Various fixes to restoring state correctly in un-hibernation.
- dovecot.index files were commonly 4 bytes per email too large. This
  is because 3 bytes per email were being wasted that could have been
  used for IMAP keywords.
- Various fixes to handle dovecot.list.index corruption better.
- lib-fts: Fixed assert-crash in address tokenizer with specific input.
- Fixed assert-crash in HTML to text parsing with specific input
  (e.g. for FTS indexing or snippet generation)
- doveadm sync -1: Fixed handling mailbox GUID conflicts.
- sdbox, mdbox: Perform full index rebuild if corruption is detected
  inside lib-index, which runs index fsck.
- quota: Don't skip quota checks when moving mails between different
  quota roots.
- search: Multiple sequence sets or UID sets in search parameters
  weren't handled correctly. They were incorrectly merged together.

* Fri Dec 02 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.26.0-2
- fix remote crash when auth-policy component is activated (CVE-2016-8652,#1401025)

* Mon Oct 31 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.26.0-1
- dovecot updated to 2.2.26.0, pigeonhole updated to 0.4.16
- master process's listener socket was leaked to all child processes.
  This might have allowed untrusted processes to capture and prevent
  "doveadm service stop" comands from working.
- login proxy: Fixed crash when outgoing SSL connections were hanging.
- auth: userdb fields weren't passed to auth-workers, so %%{userdb:*}
  from previous userdbs didn't work there.
- auth: Fixed auth_bind=yes + sasl_bind=yes to work together
- lmtp: %%{userdb:*} variables didn't work in mail_log_prefix
- Fixed writing >2GB to iostream-temp files (used by fs-compress,
  fs-metawrap, doveadm-http)
- fts-solr: Fixed searching multiple mailboxes
- and more...

* Mon Jul 04 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.25-1
- dovecot updated to 2.2.25
- doveadm backup was sometimes deleting entire mailboxes unnecessarily.
- doveadm: Command -parameters weren't being sent to doveadm-server.
- if dovecot.index read failed e.g. because mmap() reached VSZ limit,
  an empty index could have been opened instead, corrupting the
  mailbox state.
- lazy-expunge: Fixed a crash when copying failed. Various other fixes.
- fts-lucene: Fixed crash on index rescan.
- dict-ldap: Various fixes
- dict-sql: NULL values crashed. Now they're treated as "not found".

* Wed Apr 27 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.24-1
- dovecot updated to 2.2.24
- Huge header lines could have caused Dovecot to use too much memory
- dsync: Detect and handle invalid/stale -s state string better.
- dsync: Fixed crash caused by specific mailbox renames
- auth: Auth cache is now disabled passwd-file. 
- fts-tika: Don't crash if it returns 500 error
- dict-redis: Fixed timeout handling
- SEARCH INTHREAD was crashing
- stats: Only a single fifo_listeners was supported, making it impossible to
  use both auth_stats=yes and mail stats plugin.
- SSL errors were logged in separate "Stacked error" log lines instead of as
  part of the disconnection reason.
- MIME body parser didn't handle properly when a child MIME part's --boundary
  had the same prefix as the parent.
- pigeonhole updated to 0.4.14
- extprograms plugin: Fixed epoll() panic caused by closing the output
  FD before the output stream.
- Made sure that the local part of a mail address is encoded properly
  using quoted string syntax when it is not a dot-atom.

* Thu Mar 31 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.23-1
- dovecot updated to 2.2.23, pigeonhole updated to 0.4.13
- Various fixes to doveadm. Especially running commands via
  doveadm-server was broken.
- director: Fixed user weakness getting stuck in some situations
- director: Fixed a situation where directors keep re-sending
  different states to each others and never becoming synced.
- director: Fixed assert-crash related to a slow "user killed" reply
- Fixed assert-crash related to istream-concat, which could have
  been triggered at least by a Sieve script.

* Wed Mar 16 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.22-1
- dovecot updated to 2.2.22
- auth: Auth caching was done too aggressively when %%variables were
  used in default_fields, override_fields or LDAP pass/user_attrs.
  userdb result_* were also ignored when user was found from cache.
- imap: Fixed various assert-crashes caused v2.2.20+. Some of them
  caught actual hangs or otherwise unwanted behavior towards IMAP
  clients.
- Expunges were forgotten in some situations, for example when
  pipelining multiple IMAP MOVE commands.
- quota: Per-namespaces quota were broken for dict and count backends
  in v2.2.20+
- fts-solr: Search queries were using OR instead of AND as the
  separator for multi-token search queries in v2.2.20+.
- Single instance storage support wasn't really working in v2.2.16+
- dbox: POP3 message ordering wasn't working correctly.
- virtual plugin: Fixed crashes related to backend mailbox deletions.

* Mon Feb 08 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.21-4
- pigeonhole updated to 0.4.12
- multiscript: Fixed bug in handling of (implicit) keep; final keep action was
  always executed as though there was a failure. 
- managesieve-login: Fixed proxy to allow SASL mechanisms other than PLAIN.
- ldap storage: Prevent segfault occurring when assigning certain (global)
  configuration options.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.21-2
- pigeonhole updated to 0.4.11
- Sieve mime extension: Fixed the header :mime :anychild test to work properly
  outside a foreverypart loop.
- Fixed assert failure occurring when text extraction is attempted on a
  empty or broken text part.
- Fixed assert failure in handling of body parts that are converted to text.
- Fixed header unfolding for (mime) headers parsed from any mime part.
- Fixed trimming for (mime) headers parsed from any mime part.
- Fixed erroneous changes to the message part tree structure performed when
  re-parsing the message.
- LDA Sieve plugin: Fixed bug in error handling of script storage initialization
- Fixed duplication of discard actions in the script result.
- Made sure that quota errors never get logged as errors in syslog.

* Wed Dec 16 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.21-1
- dovecot updated to 2.2.21
- doveadm mailbox list (and some others) were broken in v2.2.20
- director: Fixed making backend changes when running with only a
  single director server.
- virtual plugin: Fixed crash when trying to open nonexistent
  autocreated backend mailbox.
- pigeonhole updated to 0.4.10
- implemented the Sieve mime and foreverypart extensions (RFC 5703).
+ sieve body extension: Properly implemented the `:text' body
  transform. It now extracts text for HTML message parts.
- variables extension: Fixed handling of empty string by the `:length'
  set modifier. An empty string yielded an empty string rather than "0".
- Fixed memory leak in the Sieve script byte code dumping facility.
  Extension contexts were never actually freed.
- doveadm sieve plugin: Fixed crashes caused by incorrect context
  allocation in the sieve command implementations.

* Tue Dec 08 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.20-2
- move ssl initialization from %%post to dovecot-init.service

* Tue Dec 08 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.20-1
- dovecot updated to 2.2.20
- director: Backend tags weren't working correctly.
- ldap: tls_* settings weren't used for ldaps URIs.
- ldap, mysql: Fixed setting connect timeout.
- auth: userdb lookups via auth-worker couldn't change username
- dsync: Fixed handling deleted directories. Make sure we don't go to
  infinite mailbox renaming loop.
- imap: Fixed crash in NOTIFY when there were watched namespaces that
  didn't support NOTIFY.
- imap: After SETMETADATA was used, various commands (especially FETCH)
  could have started hanging when their output was large.
- stats: Idle sessions weren't refreshed often enough, causing stats
  process to forget them and log errors about unknown sessions when
  they were updated later.
- stats: Fixed "Duplicate session ID" errors when LMTP delivered to
  multiple recipients and fts_autoindex=yes.
- zlib plugin: Fixed copying causing cache corruption when zlib_save
  wasn't set, but the source message was compressed.
- fts-solr: Fixed escaping Solr query parameters.
- lmtp: quota_full_tempfail=yes was ignored with
  lmtp_rcpt_check_quota=yes

* Mon Oct 05 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.19-1
- dovecot updated to 2.2.19
- mdbox: Rebuilding could have caused message's reference count to
  overflow the 16bit number in some situations, causing problems when
  trying to expunge the duplicates.
- Various search fixes (fts, solr, tika, lib-charset, indexer)
- Various virtual plugin fixes
- Various fixes and optimizations to dsync, imapc and pop3-migration
- imap: Various RFC compliancy and crash fixes to NOTIFY
- pigeonhole updated to 0.4.9
- ManageSieve: Fixed an assert failure occurring when a client
  disconnects during the GETSCRIPT command.
- doveadm sieve plugin: Fixed incorrect initialization (mem leaks) of mail user.
- sieve-filter command line tool: Fixed handling of failure-related
  implicit keep when there is an explicit default destination folder.
- lib-sieve: Fixed bug in RFC5322 header folding.

* Mon Aug 24 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.18-5
- use the system crypto policy (#1109114)

* Fri Jun 19 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.18-4
- fix build for s390x and ppc64 (#1232650)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.2.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.18-2
- update pigeonhole to 0.4.8
- Fixed problem in address test: erroneously decoded mime-encoded words in
  address headers.
- extprograms plugin: Fixed failure occurring when connecting to script
  service without the need to read back the output from the external program.
- Fixed bug in script storage path normalization occurring with relative
  symbolic links below root.

* Fri May 15 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.18-1
- director: Login UNIX sockets were normally detected as doveadm or
  director ring sockets, causing it to break in existing installations.
- sdbox: When copying a mail in alt storage, place the destination to
  alt storage as well.

* Thu May 14 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.17-1
- dovecot updated to 2.2.17
- pigeonhole updated to 0.4.7
- auth: If auth_master_user_separator was set, auth process could be
  crashed by trying to log in with empty master username.
- imap-login, pop3-login: Fixed crash on handshake failures with new
  OpenSSL versions (v1.0.2) when SSLv3 was disabled.
- auth: If one passdb fails allow_nets check, it shouldn't have failed
  all the other passdb checks later on.
- imap: Server METADATA couldn't be accessed
- imapc: Fixed \Muted label handling in gmail-migration.
- imapc: Various bugfixes and improvements.
- Trash plugin fixes by Alexei Gradinari
- mbox: Fixed crash/corruption in some situations

* Tue Apr 28 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.16-2
- fix CVE-2015-3420: SSL/TLS handshake failures leading to a crash of the login process

* Mon Mar 16 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.16-1
- dovecot updated to 2.2.16
- auth: Don't crash if master user login is attempted without
  any configured master=yes passdbs
- Parsing UTF-8 text for mails could have caused broken results
  sometimes if buffering was split in the middle of a UTF-8 character.
  This affected at least searching messages.
- String sanitization for some logged output wasn't done properly:
  UTF-8 text could have been truncated wrongly or the truncation may
  not have happened at all.
- fts-lucene: Lookups from virtual mailbox consisting of over 32
  physical mailboxes could have caused crashes.

* Thu Feb 05 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.15-3
- fix mbox istream crashes (#1189198, #1186504)

* Mon Jan 05 2015 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.15-2
- fix crash related to logging BYE notifications (#1176282)
- update pigeonhole to 0.4.6

* Thu Oct 30 2014 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.15-1
- dovecot updated to 2.2.15
- various race condition fixes to LAYOUT=index
- v2.2.14 virtual plugin crashed in some situations

* Fri Oct 17 2014 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.14-1
- dovecot updated to 2.2.14, pigeonhole updated to 0.4.3
- fixed several race conditions with dovecot.index.cache handling that
  may have caused unnecessary "cache is corrupted" errors.
- auth: If auth client listed userdb and disconnected before finishing,
  the auth worker process got stuck
- imap-login, pop3-login: Fixed potential crashes when client
  disconnected unexpectedly.
- imap proxy: The connection was hanging in some usage patterns.

* Thu Aug 21 2014 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.13-4
- use network-online target instead of just network (#1119814)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.2.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.13-1
- dovecot updated to 2.2.13
- fixes CVE-2014-3430: denial of service through maxxing out SSL connections
- pop3 server was still crashing in v2.2.12 
- maildir: Various fixes and improvements to handling compressed mails
- fts-lucene, fts-solr: Fixed crash on search when the index contained
  duplicate entries.
- mail_attachment_dir: Attachments with the last base64-encoded line
  longer than the rest wasn't handled correctly.
- IMAP: SEARCH/SORT PARTIAL was handled completely wrong in v2.2.11+
- acl: Global ACL file handling was broken when multiple entries
  matched the mailbox name

* Sun Mar 30 2014 John Morris <john@zultron.com> - 1:2.2.12-2
- el6 build fixes (#1082384):
- el6 autoconf too old to regen; use packaged files
- fix compile error when __global_ldflags macro undefined

* Fri Feb 14 2014 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.12-1
- dovecot updated to 2.2.12
- fixes pop3 crash

* Thu Feb 13 2014 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.11-1
- dovecot updated to 2.2.11
- imap: SEARCH/SORT PARTIAL reponses may have been too large.
- doveadm backup: Fixed assert-crash when syncing mailbox deletion.

* Thu Jan 02 2014 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.10-1
- dovecot updated to 2.2.10
- quota-status: quota_grace was ignored
- ldap: Fixed memory leak with auth_bind=yes and without
  auth_bind_userdn.
- imap: Don't send HIGHESTMODSEQ anymore on SELECT/EXAMINE when
  CONDSTORE/QRESYNC has never before been enabled for the mailbox.
- imap: Fixes to handling mailboxes without permanent modseqs.
  (When [NOMODSEQ] is returned by SELECT, mainly with in-memory
  indexes.)
- imap: Various fixes to METADATA support.
- stats plugin: Processes that only temporarily dropped privileges
  (e.g. indexer-worker) may have been logging errors about not being
  able to open /proc/self/io.

* Mon Nov 25 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.9-1
- improved cache file handling exposed several old bugs related to fetching 
  mail headers.
- iostream handling changes were causing some connections to be disconnected
  before flushing their output

* Wed Nov 20 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.8-1
- Fixed infinite loop in message parsing if message ends with
  "--boundary" and CR (without LF). Messages saved via SMTP/LMTP can't
  trigger this, because messages must end with an "LF.". A user could
  trigger this for him/herself though.
- lmtp: Client was sometimes disconnected before all the output was
  sent to it.
- replicator: Database wasn't being exported to disk every 15 minutes
  as it should have. Instead it was being imported, causing "doveadm
  replicator remove" commands to not work very well.

* Thu Nov 14 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.7-2
- fix ostream infinite loop (#1029906)

* Mon Nov 04 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.7-1
- dovecot updated to 2.2.7
- master process was doing a hostname.domain lookup for each created
  process, which may have caused a lot of unnecessary DNS lookups.
- dsync: Syncing over 100 messages at once caused problems in some
  situations, causing messages to get new UIDs.
- fts-solr: Different Solr hosts for different users didn't work.

* Tue Oct 01 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.6-1
- dovecot updated to 2.2.6, pigeonhole updated to 0.4.2
- director: v2.2.5 changes caused "SYNC lost" errors
- dsync: Many fixes and error handling improvements
- doveadm -A: Don't waste CPU by doing a separate config lookup
  for each user
- Long-running ssl-params process no longer prevents Dovecot restart
- mbox: Fixed mailbox_list_index=yes to work correctly

* Thu Aug 08 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.5-2
- use unversioned doc dir (#993731)

* Wed Aug 07 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.5-1
- dovecot updated to 2.2.5
- added some missing man pages (by Pascal Volk)
- director: Users near expiration could have been redirected to
  different servers at the same time.
- pop3: Avoid assert-crash if client disconnects during LIST.
- mdbox: Corrupted index header still wasn't automatically fixed.
- dsync: Various fixes to work better with imapc and pop3c storages.
- ldap: sasl_bind=yes caused crashes, because Dovecot's lib-sasl
  symbols conflicted with Cyrus SASL library.

* Tue Jul 30 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.4-3
- dovecot pigeonhole updated to 0.4.1

* Wed Jul 10 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.4-2
- fix name conflict with cyrus-sasl (#975869)

* Tue Jun 25 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.4-1
- dovecot updated to 2.2.4
- imap/pop3 proxy: Master user logins were broken in v2.2.3
- sdbox/mdbox: A corrupted index header with wrong size was never
  automatically fixed in v2.2.3.
- mbox: Fixed assert-crashes related to locking.

* Mon Jun 17 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.3-1
- dovecot updated to 2.2.3
- IMAP: If subject contained only whitespace, Dovecot returned an
  ENVELOPE reply with a huge literal value, effectively causing the
  IMAP client to wait for more data forever.
- IMAP: Various URLAUTH fixes.
- imapc: Various bugfixes and improvements
- pop3c: Various fixes to make it work in dsync (without imapc)
- dsync: Fixes to syncing subscriptions. Fixes to syncing mailbox
  renames.

* Tue May 21 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.2-2
- fix location of tmpfiles configuration (#964448)

* Mon May 20 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.2-1
- dovecot updated to 2.2.2
- IMAP: Various URLAUTH fixes.
- IMAP: Fixed a hang with invalid APPEND parameters.
- IMAP LIST-EXTENDED: INBOX was never listed with \Subscribed flag.
- mailbox_list_index=yes still caused crashes.
- maildir: Fixed a crash after dovecot-keywords file was re-read.
- maildir: If files had reappeared unexpectedly to a Maildir, they
  were ignored until index files were deleted.
- Maildir: Fixed handling over 26 keywords in a mailbox. 
- imap/pop3-login proxying: Fixed a crash if TCP connection succeeded,
  but the remote login timed out.

* Thu May 16 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.1-4
- update pigeonhole to 0.4.0

* Mon Apr 29 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.1-3
- revert last change and use different fix

* Wed Apr 24 2013 Kalev Lember <kalevlember@gmail.com> - 1:2.2.1-2
- Filter out autogenerated perl deps (#956194)

* Fri Apr 19 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.1-1
- dovecot updated to 2.2.1
- mailbox_list_index=yes was broken.
- LAYOUT=index didn't list subscriptions.
- auth: Multiple master passdbs didn't work.
- Message parsing (e.g. during search) crashed when multipart message
  didn't actually contain any parts.
- dovecot updated to 2.2.1

* Mon Apr 15 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2.0-1
- dovecot updated to 2.2.0
- Mailbox list indexes weren't using proper file permissions based
  on the root directory.
- replicator: doveadm commands and user list export may have skipped
  some users.
- Various fixes to mailbox_list_index=yes

* Fri Apr 05 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2-0.4
- dovecot updated to 2.2 RC4
- various bugfixes to LDAP changes in rc3

* Wed Mar 27 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2-0.3
- dovecot updated to 2.2 RC3
- Fixed a crash when decoding quoted-printable content.
- dsync: Various bugfixes

* Thu Feb 28 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2-0.2
- do not print error when NetworkManager is not installed (#916456)

* Wed Feb 27 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.2-0.1
- major update to dovecot 2.2 RC2

* Mon Feb 11 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.15-1
- dovecot updated to 2.1.15
- v2.1.14's dovecot.index.cache fixes caused Dovecot to use more disk I/O
  and memory than was necessary.

* Tue Feb 05 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.14-2
- spec clean up

* Thu Jan 31 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.14-1
- dovecot updated to 2.1.14
- v2.1.11+ had a race condition where it sometimes overwrote data in
  dovecot.index.cache file. This could have caused Dovecot to return
  the same cached data to two different messages.
- mdbox: Fixes to handling duplicate GUIDs during index rebuild

* Tue Jan 15 2013 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.13-1
- dovecot updated to 2.1.13
- Some fixes to cache file changes in v2.1.11.
- virtual storage: Sorting mailbox by from/to/cc/bcc didn't work.

* Mon Dec 03 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.12-1
- dovecot updated to 2.1.12
- lmtp proxy: Fixed hanging if remote server was down.
- doveadm: Various fixes to handling doveadm-server connections.
- auth: passdb imap was broken in v2.1.10.

* Thu Nov 08 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.10-3
- fix network still not ready race condition (#871623)

* Fri Nov 02 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.10-2
- add reload command to service file

* Wed Sep 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.10-1
- dovecot updated to 2.1.10, pigeonhole updated to 0.3.3
- director: In some conditions director may have disconnected from
  another director (without logging about it), thinking it was sending
  invalid data.
- imap: Various fixes to listing mailboxes.
- login processes crashed if there were a lot of local {} or remote {}
  settings blocks.

* Fri Aug 24 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.9-2
- use new systemd rpm macros (#851238)

* Thu Aug 02 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.9-1
- dovecot updated to 2.1.9
- Full text search indexing might have failed for some messages,
  always causing indexer-worker process to run out of memory.
- fts-lucene: Fixed handling SEARCH HEADER FROM/TO/SUBJECT/CC/BCC when
  the header wasn't lowercased.
- fts-squat: Fixed crash when searching a virtual mailbox.
- pop3: Fixed assert crash when doing UIDL on empty mailbox on some
  setups. 
- auth: GSSAPI RFC compliancy and error handling fixes.
- Various fixes related to handling shared namespaces

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.8-2
- pigeonhole updated to 0.3.1
- Fixed several small issues, including a few potential segfault bugs, based
  on static source code analysis.

* Tue Jul 03 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.8-1
- dovecot updated to 2.1.8
- imap: Mailbox names were accidentally sent as UTF-8 instead of mUTF-7
  in previous v2.1.x releases for STATUS, MYRIGHTS and GETQUOTAROOT commands.
- lmtp proxy: Don't timeout connections too early when mail has a lot of RCPT TOs.
- director: Don't crash if the director is working alone.
- shared mailboxes: Avoid doing "@domain" userdb lookups.
- doveadm: Fixed crash with proxying some commands.
- fts-squat: Fixed handling multiple SEARCH parameters.
- imapc: Fixed a crash when message had more than 8 keywords.
- imapc: Don't crash on APPEND/COPY if server doesn't support UIDPLUS.

* Mon Jul 02 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.7-5
- make quota work with NFS mounted mailboxes

* Fri Jun 22 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.7-4
- posttrans argument is always zero

* Fri Jun 15 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.7-3
- do not let dovecot run during upgrade (#134325)

* Wed May 30 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.7-2
- fix changelog, 2.1.7-1 had copy-pasted upstream changelog, which was wrong
- director: Don't crash with quickly disconnecting incoming director
  connections.
- mdbox: If mail was originally saved to non-INBOX, and namespace
  prefix is non-empty, don't assert-crash when rebuilding indexes.
- sdbox: Don't use more fds than necessary when copying mails.
- auth: Fixed crash with DIGEST-MD5 when attempting to do master user
  login without master passdbs. 
- Several fixes to mail_shared_explicit_inbox=no
- imapc: Use imapc_list_prefix also for listing subscriptions.

* Wed May 30 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.7-1
- updated to 2.1.7
- v2.1.5: Using "~/" as mail_location or elsewhere failed to actually
  expand it to home directory.
- dbox: Fixed potential assert-crash when reading dbox files.
- trash plugin: Fixed behavior when quota is already over limit.
- mail_log plugin: Logging "copy" event didn't work.
- Proxying to backend server with SSL: Verifying server certificate
  name always failed, because it was compared to an IP address.

* Wed May 09 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.6-2
- fix socket activation again, fix in 2.1.6 is incomplete

* Wed May 09 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.6-1
- v2.1.5: Using "~/" as mail_location or elsewhere failed to actually
  expand it to home directory.
- dbox: Fixed potential assert-crash when reading dbox files.
- trash plugin: Fixed behavior when quota is already over limit.
- Proxying to backend server with SSL: Verifying server certificate
  name always failed, because it was compared to an IP address.

* Tue Apr 24 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.5-1
- IMAP: Several fixes related to mailbox listing in some configs
- director: A lot of fixes and performance improvements
- mbox: Deleting a mailbox didn't delete its index files.
- pop3c: TOP command was sent incorrectly
- trash plugin didn't work properly
- LMTP: Don't add a duplicate Return-Path: header when proxying.
- listescape: Don't unescape namespace prefixes.

* Tue Apr 24 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.4-2
- close systemd extra sockets that are not configured

* Tue Apr 10 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.4-1
- dovecot updated to 2.1.4
- Proxying SSL connections crashed in v2.1.[23]
- fts-solr: Indexing mail bodies was broken.
- director: Several changes to significantly improve error handling
- doveadm import didn't import messages' flags
- mail_full_filesystem_access=yes was broken
- Make sure IMAP clients can't create directories when accessing
  nonexistent users' mailboxes via shared namespace.
- Dovecot auth clients authenticating via TCP socket could have failed
  with bogus "PID already in use" errors.

* Mon Mar 19 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.3-1
- dovecot updated to 2.1.3
- multi-dbox format in dovecot 2.1.2 was broken
- temporarily disable check phase until bug #798968 is fixed

* Fri Mar 16 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.2-1
- dovecot updated to 2.1.2
- doveadm sync: If mailbox was expunged empty, messages may have
  become back instead of also being expunged in the other side.
- imap_id_* settings were ignored before login.
- Several fixes to mailbox_list_index=yes
- Previous v2.1.x didn't log all messages at shutdown.

* Thu Mar 01 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.1-2
- enable fts_lucene plugin (#798661)

* Fri Feb 24 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.1-1
- dovecot updated to 2.1.1
- acl plugin + autocreated mailboxes crashed when listing mailboxes
- doveadm force-resync: Don't skip autocreated mailboxes (especially
  INBOX). 
- If process runs out of fds, stop listening for new connections only
  temporarily, not permanently (avoids hangs with process_limit=1
  services)
- auth: passdb imap crashed for non-login authentication (e.g. smtp).

* Mon Feb 20 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1.0-1
- updated to 2.1.0 (no major changes since .rc6)
- include pigeonhole doc files (NEWS, README, ...)

* Tue Feb 14 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1-0.7.rc6
- updated to 2.1.rc6
- dbox: Fixed error handling when saving failed or was aborted
- IMAP: Using COMPRESS extension may have caused assert-crashes
- IMAP: THREAD REFS sometimes returned invalid (0) nodes.
- dsync: Fixed handling non-ASCII characters in mailbox names.

* Tue Feb 07 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1-0.6.rc5
- use PrivateTmp in systemd unit file

* Tue Feb 07 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1-0.5.rc5
- updated to 2.1.rc5
- director: With >2 directors ring syncing might have stalled during
  director connect/disconnect, causing logins to fail.
- LMTP client/proxy: Fixed potential hanging when sending (big) mails
- Compressed mails with external attachments (dbox + SIS + zlib) failed
  sometimes with bogus "cached message size wrong" errors.

* Mon Jan 09 2012 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1-0.4.rc3
- updated to 2.1.rc3
- dsync was merged into doveadm
- added pop3c (= POP3 client) storage backend

* Wed Dec 14 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1-0.3.rc1
- allow imap+TLS and pop3+TLS by default

* Fri Dec 02 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1-0.2.rc1
- call systemd reload in postun

* Wed Nov 30 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.1-0.1.rc1
- updated to 2.1.rc1
- major changes since 2.0.x:
- plugins now use UTF-8 mailbox names rather than mUTF-7
- auth_username_format default changed to %%Lu
- solr full text search backend changed to use mailbox GUIDs instead of
  mailbox names, requiring reindexing everything

* Mon Nov 21 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.16-1
- dovecot updated to 2.0.16

* Mon Oct 24 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.15-2
- do not use obsolete settings in default configuration (#743444)

* Mon Sep 19 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.15-1
- dovecot updated to 2.0.15
- v2.0.14: Index reading could have eaten a lot of memory in some
  situations
- mbox: Fixed crash during mail delivery when mailbox didn't yet have
  GUID assigned to it.
- zlib+mbox: Fetching last message from compressed mailboxes crashed.

* Tue Sep 13 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.14-2
- do not enable insecure connections by default

* Mon Aug 29 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.14-1
- dovecot updated to 2.0.14
- userdb extra fields can now return name+=value to append to an
  existing name
- script-login attempted an unnecessary config lookup, which usually
  failed with "Permission denied".
- lmtp: Fixed parsing quoted strings with spaces as local-part for
  MAIL FROM and RCPT TO.
- imap: FETCH BODY[HEADER.FIELDS (..)] may have crashed or not
  returned all data sometimes.
- ldap: Fixed random assert-crashing with with sasl_bind=yes.
- Fixes to handling mail chroots
- Fixed renaming mailboxes under different parent with FS layout when
  using separate ALT, INDEX or CONTROL paths.
- zlib: Fixed reading concatenated .gz files.

* Fri Jul 15 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.13-2
- do not include sysv init script

* Thu May 12 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.13-1
- dovecot updated to 2.0.13
- mdbox purge: Fixed wrong warning about corrupted extrefs.
- script-login binary wasn't actually dropping privileges to the
  user/group/chroot specified by its service settings.
- Fixed potential crashes and other problems when parsing header names
  that contained NUL characters.

* Fri Apr 15 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.12-2
- pigeonhole updated to 0.2.3, which includes:
- managesieve: fixed bug in UTF-8 checking of string values
- sieve command line tools now avoid initializing the mail store unless necessary
- removed header MIME-decoding to fix erroneous address parsing
- fixed segfault bug in extension configuration, triggered when unknown
  extension is mentioned in sieve_extensions setting.

* Wed Apr 13 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.12-1
- dbox: Fixes to handling external attachments
- dsync: More fixes to avoid hanging with remote syncs
- dsync: Many other syncing/correctness fixes
- doveconf: v2.0.10 and v2.0.11 didn't output plugin {} section right

* Mon Mar 28 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.11-5
- rebuild with new patch

* Mon Mar 28 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.11-4
- fix regression in config file parsing (#690401)

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 1:2.0.11-3
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Wed Mar 23 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.11-2
- rebuild because of updated dependencies

* Mon Mar 07 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.11-1
- IMAP: Fixed hangs with COMPRESS extension
- IMAP: Fixed a hang when trying to COPY to a nonexistent mailbox. 
- IMAP: Fixed hang/crash with SEARCHRES + pipelining $.
- IMAP: Fixed assert-crash if IDLE+DONE is sent in same TCP packet.

* Thu Feb 17 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.9-3
- add missing section to dovecot's systemd service file

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 13 2011 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.9-1
- dovecot updated to 2.0.9
- fixed a high system CPU usage / high context switch count performance problem
- lda: Fixed a crash when trying to send "out of quota" reply

* Mon Dec 20 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.8-3
- add full path and check to restorecon in post

* Tue Dec 07 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.8-2
- fix s/foobar/dovecot/ typo in post script

* Tue Dec 07 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.8-1
- dovecot updated to 2.0.8, pigeonhole updated to 0.2.2
- services' default vsz_limits weren't being enforced correctly
- added systemd support
- dbox: Fixes to handling external mail attachments
- imap, pop3: When service { client_count } was larger than 1, the
  log messages didn't use the correct prefix
- MySQL: Only the first specified host was ever used

* Mon Nov 29 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.7-3
- make it work with /var/run on tmpfs (#656577)

* Tue Nov 23 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.7-2
- fix regression with  valid_chroot_dirs being ignored (#654083)

* Tue Nov 09 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.7-1
- dovecot updated to 2.0.7
- IMAP: Fixed LIST-STATUS when listing subscriptions with subscriptions=no namespaces.
- IMAP: Fixed SELECT QRESYNC not to crash on mailbox close if a lot of changes were being sent. 
- quota: Don't count virtual mailboxes in quota
- doveadm expunge didn't always actually do the physical expunging
- Fixed some index reading optimizations introduced by v2.0.5.
- LMTP proxying fixes

* Fri Oct 22 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.6-1
- dovecot updated to 2.0.6
- Pre-login CAPABILITY includes IDLE again. Mainly to make Blackberry
  servers happy.
- auth: auth_cache_negative_ttl default was 0 in earlier v2.0.x, but it
  was supposed to be 1 hour as in v1.x. Changed it back to 1h.
- doveadm: Added import command for importing mails from other storages.
- Reduced NFS I/O operations for index file accesses
- dbox, Maildir: When copying messages, copy also already cached fields
  from dovecot.index.cache
- Maildir: LDA/LMTP assert-crashed sometimes when saving a mail.
- Fixed leaking fds when writing to dovecot.mailbox.log.
- Fixed rare dovecot.index.cache corruption
- IMAP: SEARCH YOUNGER/OLDER wasn't working correctly

* Mon Oct 04 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.5-1
- dovecot updated to 2.0.5
- acl: Fixed the logic of merging multiple ACL entries
- sdbox: Fixed memory leak when copying messages with hard links. 
- zlib: Fixed several crashes, which mainly showed up with mbox.
- quota: Don't crash if user has quota disabled, but plugin loaded.
- acl: Fixed crashing when sometimes listing shared mailboxes via dict proxy.

* Tue Sep 28 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.4-1
- dovecot updated to 2.0.4
- multi-dbox: If :INDEX=path is specified, keep storage/dovecot.map.index* 
  files also in the index path rather than in the main storage directory.
- dsync: POP3 UIDLs weren't copied with Maildir
- dict file: Fixed fd leak (showed up easily with LMTP + quota)

* Mon Sep 20 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.3-1
- dovecot updated to 2.0.3
- dovecot-lda: Removed use of non-standard Envelope-To: header as 
  a default for -a
- dsync: Fixed handling \Noselect mailboxes
- Fixed an infinite loop introduced by v2.0.2's message parser changes.
- Fixed a crash introduced by v2.0.2's istream-crlf changes.

* Thu Sep 16 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.2-1
- dovecot updated
- vpopmail support is disabled for now, since it's broken. You can use
  it via checkpassword support or its sql/ldap database directly.
- maildir: Fixed "duplicate uidlist entry" errors that happened at
  least with LMTP when mail was delivered to multiple recipients
- Deleting ACLs didn't cause entries to be removed from acl_shared_dict
- mail_max_lock_timeout setting wasn't working with all locks

* Wed Aug 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0.1-1
- dovecot and pigeonhole updated
- sieve: sieved renamed to sieve-dump
- when dsync is started as root, remote dsync command is now also executed 
  as root instead of with dropped privileges.
- IMAP: QRESYNC parameters for SELECT weren't handled correctly.
- UTF-8 string validity checking wasn't done correctly
- dsync: Fixed a random assert-crash with remote dsyncing

* Tue Aug 17 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-1
- dovecot and pigeonhole updated
- dict quota didn't always decrease quota when messages were expunged
- Shared INBOX wasn't always listed with FS layout

* Wed Aug 11 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.21.rc5
- dovecot and pigeonhole updated
- Using more than 2 plugins could have caused broken behavior
- Listescape plugin fixes
- mbox: Fixed a couple of assert-crashes
- mdbox: Fixed potential assert-crash when saving multiple messages 
  in one transaction

* Thu Aug 05 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.20.rc4
- dovecot and pigeonhole updated
- doveadm mailbox status: Fixed listing non-ASCII mailbox names. 
- doveadm fetch: Fixed output when fetching message header or body
- doveadm director map/add/remove: Fixed handling IP address as parameter. 
- dsync: A few more fixes

* Wed Jul 21 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.19.rc3
- dovecot and pigeonhole updated
- fixed lda + sieve crash
- added mail_temp_dir setting, used by deliver and lmtp for creating
  temporary mail files. Default is /tmp.
- imap: Fixed checking if list=children namespace has children.
- mdbox: Race condition fixes related to copying and purging

* Fri Jul 16 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.18.rc2.20100716
- dovecot and pigeonhole updated
- enabled pigeonhole's build time test suite
- acl: Fixed crashon FS layout with non-default hierarchy separator
- dbox renamed to sdbox
- dsync fixes and improvements

* Mon Jul 12 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.17.rc2.20100712
- dovecot and pigeonhole updated
- fixed a crash with empty mail_plugins
- fixed sharing INBOX to other users
- director+LMTP proxy wasn't working correctly
- v1.x config parser failed with some settings if pigeonhole wasn't installed.
- virtual: If non-matching messages weren't expunged within same session,
  they never got expunged.

* Wed Jul 07 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.16.rc1.20100707
- updated dovecot and pigeonhole
- a lot of dsync fixes
- improved (m)dbox recovery

* Mon Jun 28 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.15.beta6.20100626
- updated dovecot, pigeonhole and man pages
- moved disable_plaintext_auth to 10-auth.conf
- mdbox: Fixed assert-crash on storage rebuild if file got lost
- lib-charset: Don't assert-crash when iconv() skips lots of invalid input
- master: Fixed crash on deinit (maybe also on reload)

* Thu Jun 10 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.14.beta5.20100610
- dovecot updated 
- lib-storage: Fixed accessing uncommitted saved mails with dsync
- example-config: Moved ACL and quota settings to a separate .conf files
- dbox, mdbox: Fixed race conditions when creating mailboxes

* Mon May 31 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.13.beta5.20100529
- dovecot and pigeonhole updated
- enable solr fulltext search
- master: Fixed crash on config reload
- lib-storage: Don't assert-crash when copying a mail fails

* Tue May 18 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.12.beta5.20100515
- dovenull is unauthorized user, needs own dovenull group

* Tue May 18 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.11.beta5.20100515
- fix typo in dovenull username

* Mon May 17 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.9.beta5.20100515
- pigeonhole and dovecot updated to snapshot 20100515
- fix crash for THREAD command

* Wed May 05 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.8.beta4.20100505
- pigeonhole and dovecot updated to snapshot 20100505
- mdbox: Avoid rebuilding storage if another process already did it
- lib-storage: Fixed () sublists in IMAP SEARCH parser
- example-config: auth-checkpassword include wasn't listed in 10-auth.conf
- doveadm: Added search command
- lib-master: Don't crash after timeouting an auth-master request
- master: If inet listener uses DNS name, which returns multiple IPs, 
  listen in all of them

* Wed Apr 28 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.7.beta4.20100427
- updated to snapshot 20100427
- doveconf <setting name> now prints only the one setting's value
- mdbox: Automatically delete old temp.* files from storage/ directory
- mdbox: use flock locking by default

* Wed Apr 21 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.6.beta4.20100421
- updated to snapshot 20100421
- mdbox: Purge crashed if it purged all messages from a file
- lib-storage: Shared namespace's prefix_len wasn't updated after prefix was truncated
- imap-quota: Iterate quota roots only once when replying to GETQUOTAROOT
- idle: Do cork/uncork when sending "OK Still here" notification
- login: If proxy returns ssl=yes and no port, switch port to imaps/pop3s

* Wed Apr 14 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.5.beta4.20100414
- add make check
- updated to snapshot 20100414
- config: Added nn- prefix to *.conf files so the sort ordering makes more sense
- lib-master: Log an error if login client disconnects too early
- mdbox: If purging found corrupted files, it didn't auto-rebuild storage
- lib-storage: Added support for searching save date
- and more...
- pigeonhole updated:
- Mailbox extension: fixed memory leak in the mailboxexists test
- added login failure handler

* Tue Apr 06 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.4.beta4.20100406
- updated to snapshot 20100406
- auth: If userdb lookup fails internally, don't cache the result.
- Added support for userdb lookup to fail with a reason
- sdbox: mailbox_update() could have changed UIDVALIDITY incorrectly
- layout=maildir++: Fixed deleting mailboxes with mailbox=file storages
- Fixed potential problems with parsing invalid address groups.
- dsync: Don't repeatedly try to keep opening the same failing mailbox
- lib-storage: Don't crash if root mail directory isn't given.

* Tue Mar 30 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.3.beta4.20100330
- fix certs location in ssl.conf

* Mon Mar 29 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.2.beta4.aefa279e2c70
- update to snapshot aefa279e2c70 from 2010-03-27
- fixes complains about missing tcpwrap (#577426)

* Thu Mar 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:2.0-0.1.beta4
- dovecot updated to 2.0 beta 4

* Fri Mar 12 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.11-2
- fix missing bzip2 support in zlib plugin (#572797)

* Tue Mar 09 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.11-1
- updated to 1.2.11
- mbox: Message header reading was unnecessarily slow. Fetching a
  huge header could have resulted in Dovecot eating a lot of CPU.
  Also searching messages was much slower than necessary.
- maildir: Reading uidlist could have ended up in an infinite loop.
- IMAP IDLE: v1.2.7+ caused extra load by checking changes every
  0.5 seconds after a change had occurred in mailbox

* Tue Feb 23 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.10-4
- move libs to correct package

* Fri Feb 19 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.10-3
- merged dovecot-sieve and dovecot-managesieve into dovecot-pigeonhole
- merged dovecot-sqlite, dovecot-gssapi and dovecot-ldap into dovecot

* Mon Jan 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.10-2
- updated sive and managesieve
- Added preliminary support for Sieve plugins and added support for
  installing Sieve development headers
- Variables extension: added support for variable namespaces.
- Added configurable script size limit. Compiler will refuse to
  compile files larger than sieve_max_script_size.
- Fixed a bug in the i;ascii-numeric comparator. If one of the
  strings started with a non-digit character, the comparator would
  always yield less-than.
- Imap4flags extension: fixed bug in removeflag: removing a single
  flag failed due to off-by-one error (bug report by Julian Cowley).
- Fixed parser recovery. In particular cases it would trigger spurious
  errors after an initial valid error and sometimes additional errors
  were inappropriately ignored.
- Implemented ManageSieve QUOTA enforcement.
- Added MAXREDIRECTS capability after login.
- Implemented new script name rules specified in most recent
  ManageSieve draft.
- Fixed assertion failure occuring with challenge-response SASL
  mechanisms.

* Mon Jan 25 2010 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.10-1
- updated to 1.2.10
- %%variables now support %%{host}, %%{pid} and %%{env:ENVIRONMENT_NAME}
  everywhere.
- LIST-STATUS capability is now advertised
- maildir: Fixed several assert-crashes.
- imap: LIST "" inbox shouldn't crash when using namespace with
  "INBOX." prefix.
- lazy_expunge now ignores non-private namespaces.

* Tue Dec 22 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.9-2
- sieve updated to 0.1.14
- managesieve updated to 0.11.10 

* Fri Dec 18 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.9-1
- updated to 1.2.9
- maildir: When saving, filenames now always contain ,S=<size>.
  Previously this was done only when quota plugin was loaded. It's
  required for zlib plugin and may be useful for other things too.
- maildir: v1.2.7 and v1.2.8 caused assert-crashes in
  maildir_uidlist_records_drop_expunges()
- maildir_copy_preserve_filename=yes could have caused crashes.
- Maildir++ quota: % limits weren't updated when limits were read
  from maildirsize.
- virtual: v1.2.8 didn't fully fix the "lots of mailboxes" bug
- virtual: Fixed updating virtual mailbox based on flag changes.
- fts-squat: Fixed searching multi-byte characters.

* Wed Nov 25 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.8-4
- spec cleanup

* Tue Nov 24 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.8-3
- fix dovecot's restart after update (#518753)

* Tue Nov 24 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.8-2
- fix initdddir typo (for rhel rebuilds)

* Fri Nov 20 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.8-1
- update to dovecot 1.2.8

* Mon Nov 16 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.7-2
- use originall managesieve to dovecot diff
- EPEL-ize spec for rhel5 rebuilds (#537666)

* Fri Nov 13 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.7-1
- updated to dovecot 1.2.7
- add man pages
- IMAP: IDLE now sends "Still here" notifications to same user's
  connections at the same time. This hopefully reduces power usage
  of some mobile clients that use multiple IDLEing connections.
- IMAP: If imap_capability is set, show it in the login banner.
- IMAP: Implemented SORT=DISPLAY extension.
- Login process creation could have sometimes failed with epoll_ctl()
  errors or without epoll probably some other strange things could
  have happened.
- Maildir: Fixed some performance issues
- Maildir: Fixed crash when using a lot of keywords.
- Several fixes to QRESYNC extension and modseq handling
- mbox: Make sure failed saves get rolled back with NFS.
- dbox: Several fixes.

* Mon Nov 02 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.6-5
- spec cleanup

* Wed Oct 21 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.6-4
- imap-login: If imap_capability is set, show it in the banner 
  instead of the default (#524485)

* Mon Oct 19 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.6-3
- sieve updated to 0.1.13 which brings these changes:
- Body extension: implemented proper handling of the :raw transform
  and added various new tests to the test suite. However, :content
  "multipart" and :content "message/rfc822" are still not working.
- Fixed race condition occuring when multiple instances are saving the
  same binary (patch by Timo Sirainen).
- Body extension: don't give SKIP_BODY_BLOCK flag to message parser,
  we want the body!
- Fixed bugs in multiscript support; subsequent keep actions were not
  always merged correctly and implicit side effects were not always
  handled correctly.
- Fixed a segfault bug in the sieve-test tool occuring when compile
  fails.
- Fixed segfault bug in action procesing. It was triggered while
  merging side effects in duplicate actions.
- Fixed bug in the Sieve plugin that caused it to try to stat() a NULL
  path, yielding a 'Bad address' error.

* Fri Oct 09 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.6-2
- fix init script for case when no action was specified

* Tue Oct 06 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.6-1
- dovecot updated to 1.2.6
- Added authtest utility for doing passdb and userdb lookups.
- login: ssl_security string now also shows the used compression.
- quota: Don't crash with non-Maildir++ quota backend.
- imap proxy: Fixed crashing with some specific password characters.
- fixed broken dovecot --exec-mail.
- Avoid assert-crashing when two processes try to create index at the
  same time.

* Tue Sep 29 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.5-2
- build with libcap enabled

* Thu Sep 17 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.5-1
- updated to dovecot 1.2.5
- Authentication: DIGEST-MD5 and RPA mechanisms no longer require
  user's login realm to be listed in auth_realms. It only made
  configuration more difficult without really providing extra security.
- zlib plugin: Don't allow clients to save compressed data directly.
  This prevents users from exploiting (most of the) potential security
  holes in zlib/bzlib.
- fix index file handling that could have caused an assert-crash
- IMAP: Fixes to QRESYNC extension.
- deliver: Don't send rejects to any messages that have Auto-Submitted
  header. This avoids emails loops.

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 1:1.2.4-3
- use password-auth common PAM configuration instead of system-auth

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1:1.2.4-2
- rebuilt with new openssl

* Fri Aug 21 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.4-1
- updated: dovecot 1.2.4, managesieve 0.11.9, sieve 0.1.12
- fixed a crash in index file handling
- fixed a crash in saving messages where message contained a CR
  character that wasn't followed by LF
- fixed a crash when listing shared namespace prefix
- sieve: implemented the new date extension. This allows matching
  against date values in header fields and the current date at
  the time of script evaluation
- managesieve: reintroduced ability to abort SASL with "*" response

* Mon Aug 10 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.3-1
- updated: dovecot 1.2.3, managesieve 0.11.8, sieve 0.1.11
- Mailbox names with control characters can't be created anymore.
  Existing mailboxes can still be accessed though.
- Allow namespace prefix to be opened as mailbox, if a mailbox
  already exists in the root dir.
- Maildir: dovecot-uidlist was being recreated every time a mailbox
  was accessed, even if nothing changed.
- listescape plugin was somewhat broken
- ldap: Fixed hang when >128 requests were sent at once.
- fts_squat: Fixed crashing when searching virtual mailbox.
- imap: Fixed THREAD .. INTHREAD crashing.

* Tue Jul 28 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.2-1.20090728snap
- updated to post 1.2.2 snapshot (including post release GSSAPI fix)
- Fixed "corrupted index cache file" errors
- IMAP: FETCH X-* parameters weren't working.
- Maildir++ quota: Quota was sometimes updated wrong
- Dovecot master process could hang if it received signals too rapidly

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.1-2
- updated sieve plugin to 0.1.9

* Mon Jul 13 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2.1-1
- updated to 1.2.1
- GSSAPI authentication is fixed (#506782)
- logins now fail if home directory path is relative, because it was 
  not working correctly and never was expected to work
- sieve and managesieve update

* Mon Apr 20 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2-0.rc3.1
- updated to 1.2.rc3

* Mon Apr 06 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2-0.rc2.1
- updated to 1.2.rc2

* Mon Mar 30 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2-0.beta4.2
- fix typo and rebuild

* Mon Mar 30 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.2-0.beta4.1
- spec clean-up
- updated to 1.2.beta4

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.11-1
- updated to 1.1.11
- IMAP: PERMANENTFLAGS list didn't contain \*, causing some clients
  not to save keywords.
- auth: Using "username" or "domain" passdb fields caused problems
  with cache and blocking passdbs in v1.1.8 .. v1.1.10.   
- userdb prefetch + blocking passdbs was broken with non-plaintext
  auth in v1.1.8 .. v1.1.10.

* Tue Jan 27 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.10-1
- updated to 1.1.10

* Sat Jan 24 2009 Dan Horak <dan[at]danny.cz> - 1:1.1.8-3
- rebuild with new mysql

* Tue Jan 13 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.8-2
- added managesieve support (thanks Helmut K. C. Tessarek)

* Thu Jan 8 2009 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.8-1
- dovecot updated to 1.1.8
- sieve-plugin updated to 1.1.6

* Tue Dec 2 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.7-2
- revert changes from 1:1.1.6-2 and 1:1.1.6-1
- password can be stored in different file readable only for root 
  via !include_try directive

* Tue Dec 2 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.7-1
- update to upstream version 1.1.7

* Mon Nov 3 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.6-2
- changed comment in sysconfig to match actual state

* Mon Nov 3 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.6-1
- update to upstream version 1.1.6
- change permissions of deliver and dovecot.conf to prevent possible password exposure

* Wed Oct 29 2008 Michal Hlavinka <mhlavink@redhat.com> - 1:1.1.5-1
- update to upstream version 1.1.5 (Resolves: CVE-2008-4577, CVE-2008-4578)

* Tue Sep  2 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.3-1
- update to upstream version 1.1.3

* Tue Jul 29 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.2-2
- really ask for the password during start-up

* Tue Jul 29 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.2-1
- update to upstream version 1.1.2
- final solution for #445200 (add /etc/sysconfig/dovecot for start-up options)

* Fri Jun 27 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.1-2
- update default settings to listen on both IPv4 and IPv6 instead of IPv6 only

* Sun Jun 22 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.1-1
- update to upstream version 1.1.1

* Sat Jun 21 2008 Dan Horak <dan[at]danny.cz> - 1:1.1.0-1
- update to upstream version 1.1.0
- update sieve plugin to 1.1.5
- remove unnecessary patches
- enable ldap and gssapi plugins
- change ownership of dovecot.conf (Resolves: #452088)

* Wed Jun 18 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.14-4
- update init script (Resolves: #451838)

* Fri Jun  6 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.14-3
- build devel subpackage (Resolves: #306881)

* Thu Jun  5 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.14-2
- install convert-tool (Resolves: #450010)

* Tue Jun  3 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.14-1
- update to upstream version 1.0.14
- remove setcred patch (use of setcred must be explictly enabled in config)

* Thu May 29 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.13-8
- update scriptlets to follow UsersAndGroups guideline
- remove support for upgrading from version < 1.0 from scriptlets
- Resolves: #448095

* Tue May 20 2008 Dan Horak <dan[at]danny.cz> - 1:1.0.13-7
- spec file cleanup
- update sieve plugin to 1.0.3
- Resolves: #445200, #238018

* Sun Mar 09 2008 Tomas Janousek <tjanouse@redhat.com> - 1:1.0.13-6
- update to latest upstream stable (1.0.13)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.0.10-5
- Autorebuild for GCC 4.3

* Mon Jan 07 2008 Tomas Janousek <tjanouse@redhat.com> - 1:1.0.10-4
- update to latest upstream stable (1.0.10)

* Wed Dec 05 2007 Jesse Keating <jkeating@redhat.com> - 1:1.0.7-3
- Bump for deps

* Mon Nov 05 2007 Tomas Janousek <tjanouse@redhat.com> - 1:1.0.7-2
- update to latest upstream stable (1.0.7)
- added the winbind patch (#286351)

* Tue Sep 25 2007 Tomas Janousek <tjanouse@redhat.com> - 1:1.0.5-1
- downgraded to lastest upstream stable (1.0.5)

* Wed Aug 22 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-16.1.alpha3
- updated license tags

* Mon Aug 13 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-16.alpha3
- updated to latest upstream alpha
- update dovecot-sieve to 0367450c9382 from hg

* Fri Aug 10 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-15.alpha2
- updated to latest upstream alpha
- split ldap and gssapi plugins to subpackages

* Wed Jul 25 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-14.6.hg.a744ae38a9e1
- update to a744ae38a9e1 from hg
- update dovecot-sieve to 131e25f6862b from hg and enable it again

* Thu Jul 19 2007 Tomas Janousek <tjanouse@redhat.com> - 1.1-14.5.alpha1
- update to latest upstream alpha
- don't build dovecot-sieve, it's only for 1.0

* Sun Jul 15 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.2-13.5
- update to latest upstream

* Mon Jun 18 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.1-12.5
- update to latest upstream

* Fri Jun 08 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.0-11.7
- specfile merge from 145241 branch
    - new sql split patch
    - support for not building all sql modules
    - split sql libraries to separate packages

* Sat Apr 14 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.0-11.1
- dovecot-1.0.beta2-pam-tty.patch is no longer needed

* Fri Apr 13 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0.0-11
- update to latest upstream

* Tue Apr 10 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-10.rc31
- update to latest upstream

* Fri Apr 06 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-9.rc30
- update to latest upstream

* Fri Mar 30 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-8.1.rc28
- spec file cleanup (fixes docs path)

* Fri Mar 23 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-8.rc28
- update to latest upstream

* Mon Mar 19 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-7.rc27
- use dovecot-sieve's version for the package

* Mon Mar 19 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-6.rc27
- update to latest upstream
- added dovecot-sieve

* Fri Mar 02 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-5.rc25
- update to latest upstream

* Sun Feb 25 2007 Jef Spaleta <jspaleta@gmail.com> - 1.0-4.rc22
- Merge review changes

* Thu Feb 08 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-3.rc22
- update to latest upstream, fixes a few bugs

* Mon Jan 08 2007 Tomas Janousek <tjanouse@redhat.com> - 1.0-2.rc17
- update to latest upstream, fixes a few bugs

* Thu Dec 21 2006 Tomas Janousek <tjanouse@redhat.com> - 1.0-1.1.rc15
- reenabled GSSAPI (#220377)

* Tue Dec 05 2006 Tomas Janousek <tjanouse@redhat.com> - 1.0-1.rc15
- update to latest upstream, fixes a few bugs, plus a security
  vulnerability (#216508, CVE-2006-5973)

* Tue Oct 10 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.3.rc7
- fix few inconsistencies in specfile, fixes #198940

* Wed Oct 04 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.2.rc7
- fix default paths in the example mkcert.sh to match configuration
  defaults (fixes #183151)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.1.rc7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.rc7
- update to latest upstream release candidate, should fix occasional
  hangs and mbox issues... INBOX. namespace is still broken though
- do not run over symlinked certificates in new locations on upgrade

* Tue Aug 15 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.rc2.2
- include /var/lib/dovecot in the package, prevents startup failure
  on new installs

* Mon Jul 17 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.rc2.1
- reenable inotify and see what happens

* Thu Jul 13 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.rc2
- update to latest upstream release candidate
- disable inotify for now, doesn't build -- this needs fixing though

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.beta8.2.1
- rebuild

* Thu Jun 08 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta8.2
- put back pop3_uidl_format default that got lost
  in the beta2->beta7 upgrade (would cause pop3 to not work
  at all in many situations)

* Thu May 04 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta8.1
- upgrade to latest upstream beta release (beta8)
- contains a security fix in mbox handling

* Thu May 04 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta7.1
- upgrade to latest upstream beta release
- fixed BR 173048

* Fri Mar 17 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.8
- fix sqlite detection in upstream configure checks, second part
  of #182240

* Wed Mar  8 2006 Bill Nottingham <notting@redhat.com> - 1.0-0.beta2.7
- fix scriplet noise some more

* Mon Mar  6 2006 Jeremy Katz <katzj@redhat.com> - 1.0-0.beta2.6
- fix scriptlet error (mitr, #184151)

* Mon Feb 27 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.5
- fix #182240 by looking in lib64 for libs first and then lib
- fix comment #1 in #182240 by copying over the example config files
  to documentation directory

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.beta2.4.1
- bump again for double-long bug on ppc(64)

* Thu Feb 09 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.4
- enable inotify as it should work now (#179431)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0-0.beta2.3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.3
- change the compiled-in defaults and adjust the default's configfile
  commented-out example settings to match compiled-in defaults,
  instead of changing the defaults only in the configfile, as per #179432
- fix #179574 by providing a default uidl_format for pop3
- half-fix #179620 by having plaintext auth enabled by default... this
  needs more thinking (which one we really want) and documentation
  either way

* Tue Jan 31 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.2
- update URL in description
- call dovecot --build-ssl-parameters in postinst as per #179430

* Mon Jan 30 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2.1
- fix spec to work with BUILD_DIR != SOURCE_DIR
- forward-port and split pam-nocred patch

* Mon Jan 23 2006 Petr Rockai <prockai@redhat.com> - 1.0-0.beta2
- new upstream version, hopefully fixes #173928, #163550
- fix #168866, use install -p to install documentation

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> - 0.99.14-10.fc5
- Rebuild due to mysql update.

* Wed Nov  9 2005 Tomas Mraz <tmraz@redhat.com> - 0.99.14-9.fc5
- rebuilt with new openssl

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 0.99.14-8.fc5
- use include instead of pam_stack in pam config

* Wed Jul 27 2005 John Dennis <jdennis@redhat.com> - 0.99.14-7.fc5
- fix bug #150888, log authenication failures with ip address

* Fri Jul 22 2005 John Dennis <jdennis@redhat.com> - 0.99.14-6.fc5
- fix bug #149673, add dummy PAM_TTY

* Thu Apr 28 2005 John Dennis <jdennis@redhat.com> - 0.99.14-5.fc4
- fix bug #156159 insecure location of restart flag file

* Fri Apr 22 2005 John Dennis <jdennis@redhat.com> - 0.99.14-4.fc4
- openssl moved its certs, CA, etc. from /usr/share/ssl to /etc/pki

* Tue Apr 12 2005 Tom Lane <tgl@redhat.com> 0.99.14-3.fc4
- Rebuild for Postgres 8.0.2 (new libpq major version).

* Mon Mar  7 2005 John Dennis <jdennis@redhat.com> 0.99.14-2.fc4
- bump rev for gcc4 build

* Mon Feb 14 2005 John Dennis <jdennis@redhat.com> - 0.99.14-1.fc4
- fix bug #147874, update to 0.99.14 release
  v0.99.14 2005-02-11  Timo Sirainen <tss at iki.fi>
  - Message address fields are now parsed differently, fixing some
    issues with spaces. Affects only clients which use FETCH ENVELOPE
    command.
  - Message MIME parser was somewhat broken with missing MIME boundaries
  - mbox: Don't allow X-UID headers in mails to override the UIDs we
    would otherwise set. Too large values can break some clients and
    cause other trouble.
  - passwd-file userdb wasn't working
  - PAM crashed with 64bit systems
  - non-SSL inetd startup wasn't working
  - If UID FETCH notices and skips an expunged message, don't return
    a NO reply. It's not needed and only makes clients give error
    messages.

* Wed Feb  2 2005 John Dennis <jdennis@redhat.com> - 0.99.13-4.devel
- fix bug #146198, clean up temp kerberos tickets

* Mon Jan 17 2005 John Dennis <jdennis@redhat.com> 0.99.13-3.devel
- fix bug #145214, force mbox_locks to fcntl only
- fix bug #145241, remove prereq on postgres and mysql, allow rpm auto
  dependency generator to pick up client lib dependency if needed.

* Thu Jan 13 2005 John Dennis <jdennis@redhat.com> 0.99.13-2.devel
- make postgres & mysql conditional build
- remove execute bit on migration example scripts so rpm does not pull
  in additional dependences on perl and perl modules that are not present
  in dovecot proper.
- add REDHAT-FAQ.txt to doc directory

* Thu Jan  6 2005 John Dennis <jdennis@redhat.com> 0.99.13-1.devel
- bring up to date with latest upstream, 0.99.13, bug #143707
  also fix bug #14462, bad dovecot-uid macro name

* Thu Jan  6 2005 John Dennis <jdennis@redhat.com> 0.99.11-10.devel
- fix bug #133618, removed LITERAL+ capability from capability string

* Wed Jan  5 2005 John Dennis <jdennis@redhat.com> 0.99.11-9.devel
- fix bug #134325, stop dovecot during installation

* Wed Jan  5 2005 John Dennis <jdennis@redhat.com> 0.99.11-8.devel
- fix bug #129539, dovecot starts too early,
  set chkconfig to 65 35 to match cyrus-imapd
- also delete some old commented out code from SSL certificate creation

* Thu Dec 23 2004 John Dennis <jdennis@redhat.com> 0.99.11-7.devel
- add UW to Dovecot migration documentation and scripts, bug #139954
  fix SSL documentation and scripts, add missing documentation, bug #139276

* Mon Nov 15 2004 Warren Togami <wtogami@redhat.com> 0.99.11-2.FC4.1
- rebuild against MySQL4

* Thu Oct 21 2004 John Dennis <jdennis@redhat.com>
- fix bug #136623
  Change License field from GPL to LGPL to reflect actual license

* Thu Sep 30 2004 John Dennis <jdennis@redhat.com> 0.99.11-1.FC3.3
- fix bug #124786, listen to ipv6 as well as ipv4

* Wed Sep  8 2004 John Dennis <jdennis@redhat.com> 0.99.11-1.FC3.1
- bring up to latest upstream,
  comments from Timo Sirainen <tss at iki.fi> on release v0.99.11 2004-09-04  
  + 127.* and ::1 IP addresses are treated as secured with
    disable_plaintext_auth = yes
  + auth_debug setting for extra authentication debugging
  + Some documentation and error message updates
  + Create PID file in /var/run/dovecot/master.pid
  + home setting is now optional in static userdb
  + Added mail setting to static userdb
  - After APPENDing to selected mailbox Dovecot didn't always notice the
    new mail immediately which broke some clients
  - THREAD and SORT commands crashed with some mails
  - If APPENDed mail ended with CR character, Dovecot aborted the saving
  - Output streams sometimes sent data duplicated and lost part of it.
    This could have caused various strange problems, but looks like in
    practise it rarely caused real problems.

* Wed Aug  4 2004 John Dennis <jdennis@redhat.com>
- change release field separator from comma to dot, bump build number

* Mon Aug  2 2004 John Dennis <jdennis@redhat.com> 0.99.10.9-1,FC3,1
- bring up to date with latest upstream, fixes include:
- LDAP support compiles now with Solaris LDAP library
- IMAP BODY and BODYSTRUCTURE replies were wrong for MIME parts which
  didn't contain Content-Type header.
- MySQL and PostgreSQL auth didn't reconnect if connection was lost
  to SQL server
- Linking fixes for dovecot-auth with some systems
- Last fix for disconnecting client when downloading mail longer than
  30 seconds actually made it never disconnect client. Now it works
  properly: disconnect when client hasn't read _any_ data for 30
  seconds.
- MySQL compiling got broken in last release
- More PostgreSQL reconnection fixing

* Mon Jul 26 2004 John Dennis <jdennis@redhat.com> 0.99.10.7-1,FC3,1
- enable postgres and mySQL in build
- fix configure to look for mysql in alternate locations
- nuke configure script in tar file, recreate from configure.in using autoconf
- bring up to latest upstream, which included:
- Added outlook-pop3-no-nuls workaround to fix Outlook hang in mails with NULs.
- Config file lines can now contain quoted strings ("value ")
- If client didn't finish downloading a single mail in 30 seconds,
  Dovecot closed the connection. This was supposed to work so that
  if client hasn't read data at all in 30 seconds, it's disconnected.
- Maildir: LIST now doesn't skip symlinks

* Wed Jun 30 2004 John Dennis <jdennis@redhat.com>
- bump rev for build
- change rev for FC3 build

* Fri Jun 25 2004 John Dennis <jdennis@redhat.com> - 0.99.10.6-1
- bring up to date with upstream,
  recent change log comments from Timo Sirainen were:
  SHA1 password support using OpenSSL crypto library
  mail_extra_groups setting
  maildir_stat_dirs setting
  Added NAMESPACE capability and command
  Autocreate missing maildirs (instead of crashing)
  Fixed occational crash in maildir synchronization
  Fixed occational assertion crash in ioloop.c
  Fixed FreeBSD compiling issue
  Fixed issues with 64bit Solaris binary

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 27 2004 David Woodhouse <dwmw2@redhat.com> 0.99.10.5-1
- Update to 0.99.10.5 to fix maildir segfaults (#123022)

* Fri May 07 2004 Warren Togami <wtogami@redhat.com> 0.99.10.4-4
- default auth config that is actually usable
- Timo Sirainen (author) suggested functionality fixes
  maildir, imap-fetch-body-section, customflags-fix

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Tue Feb 17 2004 Jeremy Katz <katzj@redhat.com> - 0.99.10.4-3
- restart properly if it dies (#115594)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Nov 24 2003 Jeremy Katz <katzj@redhat.com> 0.99.10.4-1
- update to 0.99.10.4

* Mon Oct  6 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-7
- another patch from upstream to fix returning invalid data on partial 
  BODY[part] fetches
- patch to avoid confusion of draft/deleted in indexes

* Tue Sep 23 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-6
- add some patches from upstream (#104288)

* Thu Sep  4 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-5
- fix startup with 2.6 with patch from upstream (#103801)

* Tue Sep  2 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-4
- fix assert in search code (#103383)

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.99.10-3
- rebuild

* Thu Jul 17 2003 Bill Nottingham <notting@redhat.com> 0.99.10-2
- don't run by default

* Thu Jun 26 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-1
- 0.99.10

* Mon Jun 23 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-0.2
- 0.99.10-rc2 (includes ssl detection fix)
- a few tweaks from fedora
  - noreplace the config file
  - configure --with-ldap to get LDAP enabled

* Mon Jun 23 2003 Jeremy Katz <katzj@redhat.com> 0.99.10-0.1
- 0.99.10-rc1
- add fix for ssl detection
- add zlib-devel to BuildRequires
- change pam service name to dovecot
- include pam config

* Thu May  8 2003 Jeremy Katz <katzj@redhat.com> 0.99.9.1-1
- update to 0.99.9.1
- add patch from upstream to fix potential bug when fetching with 
  CR+LF linefeeds
- tweak some things in the initscript and config file noticed by the 
  fedora folks

* Sun Mar 16 2003 Jeremy Katz <katzj@redhat.com> 0.99.8.1-2
- fix ssl dir
- own /var/run/dovecot/login with the correct perms
- fix chmod/chown in post

* Fri Mar 14 2003 Jeremy Katz <katzj@redhat.com> 0.99.8.1-1
- update to 0.99.8.1

* Tue Mar 11 2003 Jeremy Katz <katzj@redhat.com> 0.99.8-2
- add a patch to fix quoting problem from CVS

* Mon Mar 10 2003 Jeremy Katz <katzj@redhat.com> 0.99.8-1
- 0.99.8
- add some buildrequires
- fixup to build with openssl 0.9.7
- now includes a pop3 daemon (off by default)
- clean up description and %%preun
- add dovecot user (uid/gid of 97)
- add some buildrequires
- move the ssl cert to %%{_datadir}/ssl/certs
- create a dummy ssl cert in %%post
- own /var/run/dovecot
- make the config file a source so we get default mbox locks of fcntl

* Sun Dec  1 2002 Seth Vidal <skvidal@phy.duke.edu>
- 0.99.4 and fix startup so it starts imap-master not vsftpd :)

* Tue Nov 26 2002 Seth Vidal <skvidal@phy.duke.edu>
- first build
