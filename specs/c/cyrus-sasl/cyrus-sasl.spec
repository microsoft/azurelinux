## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 34;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global username    saslauth

%global _plugindir2 %{_libdir}/sasl2
%global bootstrap_cyrus_sasl 0
%global bdb_migration %[!(0%{?rhel} >= 10)]
%global gdbm_db_file /etc/sasl2/sasldb2

Summary: The Cyrus SASL library
Name: cyrus-sasl
Version: 2.1.28
Release: %autorelease
License: BSD-Attribution-HPND-disclaimer
URL: https://www.cyrusimap.org/sasl/

# Source0 originally comes from https://www.cyrusimap.org/releases/;
# make-no-dlcompatorsrp-tarball.sh removes the "dlcompat" subdirectory and builds a
# new tarball.
Source0: cyrus-sasl-%{version}-nodlcompatorsrp.tar.gz
Source3: saslauth.sysusers
Source5: saslauthd.service
Source7: sasl-mechlist.c
Source9: saslauthd.sysconfig
Source10: make-no-dlcompatorsrp-tarball.sh
# From upstream git, required for reconfigure after applying patches to configure.ac
# https://raw.githubusercontent.com/cyrusimap/cyrus-sasl/master/autogen.sh
Source11: autogen.sh


Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Patch11: cyrus-sasl-2.1.25-no_rpath.patch
Patch15: cyrus-sasl-2.1.20-saslauthd.conf-path.patch
Patch23: cyrus-sasl-2.1.23-man.patch
Patch24: cyrus-sasl-2.1.21-sizes.patch
# The 64 bit *INT8 type is not used anywhere and other types match
Patch49: cyrus-sasl-2.1.26-md5global.patch

Patch101: cyrus-sasl-2.1.27-Add-basic-test-infrastructure.patch
Patch102: cyrus-sasl-2.1.27-Add-Channel-Binding-support-for-GSSAPI-GSS-SPNEGO.patch
#https://github.com/simo5/cyrus-sasl/commit/ebd2387f06c84c7f9aac3167ec041bb01e5c6e48
Patch106: cyrus-sasl-2.1.27-nostrncpy.patch
# Upstream PR: https://github.com/cyrusimap/cyrus-sasl/pull/635
Patch107: cyrus-sasl-2.1.27-more-tests.patch
Patch108: cyrus-sasl-2.1.27-Add-support-for-setting-max-ssf-0-to-GSS-SPNEGO.patch
#Migration tool should be removed from Fedora 36
Patch109: cyrus-sasl-2.1.27-Migration-from-BerkeleyDB.patch
Patch500: cyrus-sasl-2.1.27-coverity.patch
Patch501: cyrus-sasl-2.1.27-cumulative-digestmd5.patch
Patch502: cyrus-sasl-2.1.27-cumulative-ossl3.patch
Patch503: cyrus-sasl-2.1.28-SAST.patch

Patch599: cyrus-sasl-2.1.28-fedora-c99.patch
Patch600: cyrus-sasl-2.1.28-gcc15.patch

BuildRequires: autoconf, automake, libtool, gdbm-devel, groff
BuildRequires: krb5-devel >= 1.2.2, openssl-devel, pam-devel, pkgconfig
BuildRequires: mariadb-connector-c-devel, libpq-devel, zlib-devel
%if ! %{bootstrap_cyrus_sasl}
BuildRequires: openldap-devel
%endif
%if %{bdb_migration}
#build reqs for migration from BerkeleyDB
BuildRequires: libdb-devel-static
%endif
#build reqs for make check
BuildRequires: python3 nss_wrapper socket_wrapper krb5-server
BuildRequires: make
BuildRequires: libxcrypt-devel
Requires: /sbin/nologin
Provides: user(%username)
Provides: group(%username)

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/saslauthd
%endif

%description
The %{name} package contains the Cyrus implementation of SASL.
SASL is the Simple Authentication and Security Layer, a method for
adding authentication support to connection-based protocols.

%package lib
Summary: Shared libraries needed by applications which use Cyrus SASL

%description lib
The %{name}-lib package contains shared libraries which are needed by
applications which use the Cyrus SASL library.

%package devel
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Summary: Files needed for developing applications with Cyrus SASL

%description devel
The %{name}-devel package contains files needed for developing and
compiling applications which use the Cyrus SASL library.

%package gssapi
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: GSSAPI authentication support for Cyrus SASL

%description gssapi
The %{name}-gssapi package contains the Cyrus SASL plugins which
support GSSAPI authentication. GSSAPI is commonly used for Kerberos
authentication.

%package plain
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: PLAIN and LOGIN authentication support for Cyrus SASL

%description plain
The %{name}-plain package contains the Cyrus SASL plugins which support
PLAIN and LOGIN authentication schemes.

%package md5
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: CRAM-MD5 and DIGEST-MD5 authentication support for Cyrus SASL

%description md5
The %{name}-md5 package contains the Cyrus SASL plugins which support
CRAM-MD5 and DIGEST-MD5 authentication schemes.

# This would more appropriately be named cyrus-sasl-auxprop-sql.
%package sql
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: SQL auxprop support for Cyrus SASL

%description sql
The %{name}-sql package contains the Cyrus SASL plugin which supports
using a RDBMS for storing shared secrets.

%if ! %{bootstrap_cyrus_sasl}
# This was *almost* named cyrus-sasl-auxprop-ldapdb, but that's a lot of typing.
%package ldap
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: LDAP auxprop support for Cyrus SASL

%description ldap
The %{name}-ldap package contains the Cyrus SASL plugin which supports using
a directory server, accessed using LDAP, for storing shared secrets.
%endif

%package scram
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: SCRAM auxprop support for Cyrus SASL

%description scram
The %{name}-scram package contains the Cyrus SASL plugin which supports
the SCRAM authentication scheme.

%package gs2
Requires: %{name}-lib%{?_isa} = %{version}-%{release}
Summary: GS2 support for Cyrus SASL

%description gs2
The %{name}-gs2 package contains the Cyrus SASL plugin which supports
the GS2 authentication scheme.

###


%prep
%setup -q -n cyrus-sasl-%{version}
%patch -P11 -p1 -b .no_rpath
%patch -P15 -p1 -b .path
%patch -P23 -p1 -b .man
%patch -P24 -p1 -b .sizes
%patch -P49 -p1 -b .md5global.h
%patch -P101 -p1 -b .tests
%patch -P102 -p1 -b .gssapi_cbs
%patch -P106 -p1 -b .nostrncpy
%patch -P107 -p1 -b .moretests
%patch -P108 -p1 -b .maxssf0
%if %{bdb_migration}
%patch -P109 -p1 -b .frombdb
%endif
%patch -P500 -p1 -b .coverity
%patch -P501 -p1 -b .digestmd5
%patch -P502 -p1 -b .ossl3
%patch -P503 -p1 -b .sast
%patch -P599 -p1 -b .c99
%patch -P600 -p1 -b .gcc15

%build
# reconfigure
cp %{SOURCE11} ./
rm configure aclocal.m4 config/ltmain.sh Makefile.in
export NOCONFIGURE=yes
sh autogen.sh

%set_build_flags
# Find Kerberos.
krb5_prefix=`krb5-config --prefix`
if test x$krb5_prefix = x%{_prefix} ; then
        krb5_prefix=
else
        CPPFLAGS="-I${krb5_prefix}/include $CPPFLAGS"; export CPPFLAGS
        LDFLAGS="-L${krb5_prefix}/%{_lib} $LDFLAGS"; export LDFLAGS
fi

# Find OpenSSL.
LIBS="-lcrypt"; export LIBS
if pkg-config openssl ; then
        CPPFLAGS="`pkg-config --cflags-only-I openssl` $CPPFLAGS"; export CPPFLAGS
        LDFLAGS="`pkg-config --libs-only-L openssl` $LDFLAGS"; export LDFLAGS
fi

# Find the MySQL libraries used needed by the SQL auxprop plugin.
INC_DIR="`mysql_config --include`"
if test x"$INC_DIR" != "x-I%{_includedir}"; then
        CPPFLAGS="$INC_DIR $CPPFLAGS"; export CPPFLAGS
fi
LIB_DIR="`mysql_config --libs | sed -e 's,-[^L][^ ]*,,g' -e 's,^ *,,' -e 's, *$,,' -e 's,  *, ,g'`"
if test x"$LIB_DIR" != "x-L%{_libdir}"; then
        LDFLAGS="$LIB_DIR $LDFLAGS"; export LDFLAGS
fi

# Find the PostgreSQL libraries used needed by the SQL auxprop plugin.
INC_DIR="-I`pg_config --includedir`"
if test x"$INC_DIR" != "x-I%{_includedir}"; then
        CPPFLAGS="$INC_DIR $CPPFLAGS"; export CPPFLAGS
fi
LIB_DIR="-L`pg_config --libdir`"
if test x"$LIB_DIR" != "x-L%{_libdir}"; then
        LDFLAGS="$LIB_DIR $LDFLAGS"; export LDFLAGS
fi

# run "make check" against the built library rather than the one in buildroot
LDFLAGS="-Wl,--enable-new-dtags $LDFLAGS"; export LDFLAGS

echo "$CFLAGS"
echo "$CPPFLAGS"
echo "$LDFLAGS"

%configure \
        --enable-shared --disable-static \
        --disable-java \
        --with-plugindir=%{_plugindir2} \
        --with-configdir=%{_plugindir2}:%{_sysconfdir}/sasl2 \
        --disable-krb4 \
        --enable-gssapi${krb5_prefix:+=${krb5_prefix}} \
        --with-gss_impl=mit \
        --with-rc4 \
        --with-dblib=gdbm \
        --with-dbpath=%{gdbm_db_file} \
        --with-saslauthd=/run/saslauthd --without-pwcheck \
%if ! %{bootstrap_cyrus_sasl}
        --with-ldap \
%endif
        --with-devrandom=/dev/urandom \
        --enable-anon \
        --enable-cram \
        --enable-digest \
        --disable-ntlm \
        --enable-plain \
        --enable-login \
        --enable-alwaystrue \
        --enable-httpform \
        --disable-otp \
%if ! %{bootstrap_cyrus_sasl}
        --enable-ldapdb \
%endif
        --enable-sql --with-mysql=yes --with-pgsql=yes \
        --without-sqlite \
        --enable-auth-sasldb \
        "$@"
make sasldir=%{_plugindir2}
make -C saslauthd testsaslauthd
make -C sample

# Build a small program to list the available mechanisms, because I need it.
pushd lib
../libtool --mode=link %{__cc} -o sasl2-shared-mechlist -I../include $CFLAGS %{SOURCE7} $LDFLAGS ./libsasl2.la


%install
test "$RPM_BUILD_ROOT" != "/" && rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT sasldir=%{_plugindir2}
make install DESTDIR=$RPM_BUILD_ROOT sasldir=%{_plugindir2} -C plugins

install -m755 -d $RPM_BUILD_ROOT%{_bindir}
./libtool --mode=install \
install -m755 sample/client $RPM_BUILD_ROOT%{_bindir}/sasl2-sample-client
./libtool --mode=install \
install -m755 sample/server $RPM_BUILD_ROOT%{_bindir}/sasl2-sample-server
%if %{bdb_migration} && "%{_sbindir}" != "%{_bindir}"
mv $RPM_BUILD_ROOT%{_sbindir}/cyrusbdb2current $RPM_BUILD_ROOT%{_bindir}/cyrusbdb2current
%endif
./libtool --mode=install \
install -m755 saslauthd/testsaslauthd $RPM_BUILD_ROOT%{_sbindir}/testsaslauthd

# Install the saslauthd mdoc page in the expected location.  Sure, it's not
# really a man page, but groff seems to be able to cope with it.
install -m755 -d $RPM_BUILD_ROOT%{_mandir}/man8/
install -m644 -p saslauthd/saslauthd.mdoc $RPM_BUILD_ROOT%{_mandir}/man8/saslauthd.8
install -m644 -p saslauthd/testsaslauthd.8 $RPM_BUILD_ROOT%{_mandir}/man8/testsaslauthd.8

# Install the systemd unit file for saslauthd and the config file.
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir} $RPM_BUILD_ROOT/etc/sysconfig
install -m644 -p %{SOURCE5} $RPM_BUILD_ROOT/%{_unitdir}/saslauthd.service
install -m644 -p %{SOURCE9} $RPM_BUILD_ROOT/etc/sysconfig/saslauthd

# Install the config dirs if they're not already there.
install -m755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/sasl2
install -m755 -d $RPM_BUILD_ROOT/%{_plugindir2}

# Provide an easy way to query the list of available mechanisms.
./libtool --mode=install \
install -m755 lib/sasl2-shared-mechlist $RPM_BUILD_ROOT/%{_sbindir}/

# Sysusers file
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/cyrus-sasl.conf

# Remove unpackaged files from the buildroot.
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/libotp.*
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/sasl2/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_mandir}/cat8/saslauthd.8

%check
make check %{?_smp_mflags}


%post
%systemd_post saslauthd.service

%preun
%systemd_preun saslauthd.service

%postun
%systemd_postun_with_restart saslauthd.service

%ldconfig_scriptlets lib

%files
%doc saslauthd/LDAP_SASLAUTHD
%{_mandir}/man8/*
%{_sbindir}/pluginviewer
%{_sbindir}/saslauthd
%{_sbindir}/testsaslauthd
%config(noreplace) /etc/sysconfig/saslauthd
%{_unitdir}/saslauthd.service
%ghost %attr(755,root,root) /run/saslauthd
%{_sysusersdir}/cyrus-sasl.conf

%files lib
%license COPYING
%doc AUTHORS doc/html/*.html
%{_libdir}/libsasl*.so.*
%dir %{_sysconfdir}/sasl2
%dir %{_plugindir2}/
%{_plugindir2}/*anonymous*.so*
%{_plugindir2}/*sasldb*.so*
%{_sbindir}/saslpasswd2
%{_sbindir}/sasldblistusers2
%if %{bdb_migration}
%{_bindir}/cyrusbdb2current
%endif

%files plain
%{_plugindir2}/*plain*.so*
%{_plugindir2}/*login*.so*

%if ! %{bootstrap_cyrus_sasl}
%files ldap
%{_plugindir2}/*ldapdb*.so*
%endif

%files md5
%{_plugindir2}/*crammd5*.so*
%{_plugindir2}/*digestmd5*.so*

%files sql
%{_plugindir2}/*sql*.so*

%files gssapi
%{_plugindir2}/*gssapi*.so*

%files scram
%{_plugindir2}/libscram.so*

%files gs2
%{_plugindir2}/libgs2.so*

%files devel
%{_bindir}/sasl2-sample-client
%{_bindir}/sasl2-sample-server
%{_includedir}/*
%{_libdir}/libsasl*.*so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
%{_sbindir}/sasl2-shared-mechlist

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.1.28-34
- test: add initial lock files

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.28-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.28-32
- Drop call to %%sysusers_create_compat

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 2.1.28-31
- Add explicit BR: libxcrypt-devel

* Thu Jan 23 2025 Rob Crittenden <rcritten@redhat.com> - 2.1.28-30
- Add compatibility for gcc 15

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.28-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.28-28
- Rebuilt for the bin-sbin merge (2nd attempt)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.28-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.28-26
- Rebuilt for the bin-sbin merge

* Tue Jun 25 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.28-25
- Disable BDB migration tool on RHEL 10+

* Thu Jun 20 2024 Rob Crittenden <rcritten@redhat.com> - 2.1.28-24
- Change SPDX license to BSD-Attribution-HPND-disclaimer

* Thu May 30 2024 Software Management Team <packaging-team-maint@redhat.com> - 2.1.28-23
- Eliminate use of obsolete %%patchN syntax (#2283636)

* Mon May 20 2024 Rob Crittenden <rcritten@redhat.com> - 2.1.28-22
- Fix some issues uncovered by a static analyzer

* Sun Apr 14 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.28-21
- Add compat sbin Provides

* Tue Apr 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.28-20
- Prepare for bin-sbin merge

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.28-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.28-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Florian Weimer <fweimer@redhat.com> - 2.1.28-17
- sasl-mechlist.c: Cast function pointer to the expected type

* Mon Jan 15 2024 Rob Crittenden <rcritten@redhat.com> - 2.1.28-16
- Disable and drop the ntlm plugin as it is removed upstream

* Thu Jan 11 2024 Rob Crittenden <rcritten@redhat.com> - 2.1.28-15
- tests: Switch openldap database to the LMDB backend

* Mon Jan 08 2024 Rob Crittenden <rcritten@redhat.com> - 2.1.28-14
- Add a mode and ownership to the ghost /run/saslauthd directory

* Fri Sep 08 2023 Simo Sorce <simo@redhat.com> - 2.1.28-13
- Migrate license field to SPDX format

* Wed Jul 19 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.28-12
- Add --enable-new-dtags to LDFLAGS

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.28-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 20 2023 DJ Delorie <dj@redhat.com> - 2.1.28-10
- Fix C99 compatibility issue

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 18 2022 Kalev Lember <klember@redhat.com> - 2.1.28-8
- Avoid requires on systemd as well as per updated guidelines

* Fri Aug 05 2022 Kalev Lember <klember@redhat.com> - 2.1.28-7
- Avoid systemd_requires as per updated packaging guidelines

* Mon Aug 01 2022 Simo Sorce <simo@redhat.com> - 2.1.28-6
- Fix memory leak in digestmd5 patches

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 09 2022 Simo Sorce <simo@redhat.com> - 2.1.28-4
- Use systemd sysusers to create saslauth user

* Thu Jun 09 2022 Simo Sorce <simo@redhat.com> - 2.1.28-3
- Enable sasldb authentication mechanism

* Wed May 11 2022 Simo Sorce <simo@redhat.com> - 2.1.28-2
- Fix changelog section with correct syntax

* Wed Feb 23 2022 Simo Sorce <simo@redhat.com> - 2.1.28-1
- Update to 2.1.28

* Wed Feb 23 2022 Simo Sorce <simo@redhat.com> - 2.1.27-49
- Move to use autorelease macro

* Tue Oct 12 2021 Simo Sorce <simo@redhat.com> - 2.1.27-16
- Fix rpath patch
- Resolves: rhbz#2012172

* Wed Oct  6 2021 Simo Sorce <simo@redhat.com> - 2.1.27-15
- More openssl 3 compatibility and digestmd5 updates.

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.1.27-14
- Rebuilt with OpenSSL 3.0.0

* Tue Aug 10 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 2.1.27-13
- Preserve GDBM error to correctly deal with GDBM sasldb
- Related: rhbz#1952926

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.27-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 03 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 2.1.27-11
- Fix some coverity issues
- Set default sasldb database to GDBM instead of BerkeleyDB
- Add the migration tool from BerkeleyDB
- Add some PLAIN auth tests

* Tue Apr 06 2021 Simo Sorce <simo@redhat.com> - 2.1.27-10
- Fix issues with autoconf 2.70+

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.27-9
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 2.1.27-8
- rebuild for libpq ABI fix rhbz#1908268

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May  7 2020 Simo Sorce <simo@redhat.com> - 2.1.27-5
- Backport GSSAPI Channel Bindings support
- Add support for setting maxssf=0 in GSS-SPNEGO
- Reduce excessive GSSAPI plugin logging

* Thu Mar 19 2020 Simo Sorce - 2.1.27-4
- Fix CVE 2019 19906

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 13 2019 Simo Sorce - 2.1.27-1
- Update to final 2.1.27 sources
- Also add patch to use OpenSSL RC4, currently proposed as PR 559

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.27-0.6rc7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.1.27-0.5rc7
- Rebuilt for libcrypt.so.2 (#1666033)

* Sun Oct 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2.1.27-0.4rc7
- Clean up remanents of sys-v, spec cleanups

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.27-0.3rc7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Jakub Jelen <jjelen@redhat.com> - 2.1.27-0.2rc7
- Avoid multilib conflicts between devel subpackages (#1577675)

* Mon Mar 05 2018 Jakub Jelen <jjelen@redhat.com> - 2.1.27-0.1rc7
- New upstream (pre-)release
- Import LDFLAGS from redhat-rpm-config (#1548437)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.26-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.1.26-36
- Rebuilt for switch to libxcrypt

* Mon Oct 23 2017 Jakub Jelen <jjelen@redhat.com> - 2.1.26-35
- Use mariadb-connector-c-devel instead of mysql-devel (#1493620)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.26-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.26-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 19 2017 Jakub Jelen <jjelen@redhat.com> - 2.1.26-32
- Add missing patch for separate mutexes per connection in GSSAPI

* Tue Apr 18 2017 Jakub Jelen <jjelen@redhat.com> - 2.1.26-31
- Allow cyrus sasl to get the ssf from gssapi

* Wed Apr 12 2017 Petr Šabata <contyk@redhat.com> - 2.1.26-30
- Removing the obsolete scriptlet /sbin/service dependency

* Tue Mar 07 2017 Jakub Jelen <jjelen@redhat.com> - 2.1.26-29
- Fix GSS SPNEGO support (#1421663)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.26-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 07 2016 Jakub Jelen <jjelen@redhat.com> - 2.1.26-27
- Add support for OpenSSL 1.1.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.26-26.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jul 16 2015 Jakub Jelen <jjelen@redhat.com> 2.1.26-25.2
- Revert tmpfiles.d and use new systemd feature RuntimeDirectory

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.26-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Jakub Jelen <jjelen@redhat.com> 2.1.26-23
- Add ability to handle logging in gssapi plugin (#1187097)

* Mon Mar 16 2015 Jakub Jelen <jjelen@redhat.com> 2.1.26-22
- Rever "Do not leak memory in plugin_common.c ..." due the breakage of svn (#1202364)

* Thu Mar 12 2015 Jakub Jelen <jjelen@redhat.com> 2.1.26-21
- Add and Document ability to run saslauthd as non-root user, fix tpmfiles ownership (#1189203)
- Do not leak memory in sample server (#852755)
- Do not leak memory in plugin_common.c for password callback (#1191183)
- Cleanup spec file: tmpfiles.d macros and tab/space

* Wed Feb 04 2015 Petr Lautrbach <plautrba@redhat.com> 2.1.26-20
- Change the ownership of /run/saslauth to saslauth:saslauth (#1189203)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.26-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> - 2.1.26-18
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.26-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 19 2014 Ville Skyttä <ville.skytta@iki.fi> - 2.1.26-16
- Don't order service after syslog.target.

* Fri Nov 15 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-15
- Treat SCRAM-SHA-1/DIGEST-MD5 as more secure than PLAIN (#970718)
- improve configuration error message

* Fri Nov 01 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-14
- revert upstream commit 080e51c7fa0421eb2f0210d34cf0ac48a228b1e9 (#984079)

* Tue Oct 15 2013 Karsten Hopp <karsten@redhat.com> 2.1.26-13
- add ppc64p7 subarch support in config.sub (Fedora only)

* Mon Sep 09 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-12
- build with RPM_OPT_FLAGS <ville.skytta@iki.fi> (#1005535)

* Tue Sep 03 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-11
- fix hardening for /usr/sbin/saslauthd
- add testsaslauthd.8 man page to the package
- use static md5global.h file

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.26-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-9
- detect gsskrb5_register_acceptor_identity macro <nalin@redhat.com> (#976538)

* Tue Jun 04 2013 Karsten Hopp <karsten@redhat.com> 2.1.26-8
- disable incorrect check for MkLinux to allow building with shared libraries on PPC

* Tue May 21 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-7
- fix the spec file in order to build the cyrus-sasl-sql plugin
  with support for PostgreSQL and MySQL

* Thu Feb 21 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-6
- don't include system sasl2 library needed for rebuilds after rebase

* Mon Feb 11 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-5
- enable full relro and PIE compiler flags for saslauthd

* Fri Feb 01 2013 Petr Lautrbach <plautrba@redhat.com> 2.1.26-4
- fix library symlinks

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.26-3
- actually apply size_t patch (#906519)

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> 2.1.26-2
- sasl.h: +#include<sys/types.h> for missing size_t type (#906519)
- tighten subpkg deps via %%?_isa

* Thu Dec 20 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.26-1
- update to 2.1.26
- fix segfaults in sasl_gss_encode (#886140)

* Mon Dec 10 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.25-2
- always use the current external Berkeley DB when linking

* Fri Dec 07 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.25-1
- update to 2.1.25
- add cyrus-sasl-scram and cyrus-sasl-gs2 packages

* Fri Sep 14 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.23-36
- replace scriptlets with systemd macros (#856666)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.23-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.23-34
- move /etc/tmpfiles.d/saslauthd.conf to /usr/lib/tmpfiles.d/saslauthd.conf (#840193)

* Wed Jun 20 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.23-33
- properly deal with crypt() returning NULL (#816250)
- use fixed gid 76 for saslauth

* Mon Apr 16 2012 Jindrich Novy <jnovy@redhat.com> 2.1.23-32
- re-enable libdb support and utilities

* Wed Apr 04 2012 Jindrich Novy <jnovy@redhat.com> 2.1.23-31
- temporarily disable libdb support to resolve cyrus-sasl
  chicken and egg build problem against libdb

* Tue Apr 03 2012 Jindrich Novy <jnovy@redhat.com> 2.1.23-30
- rebuild against new libdb

* Wed Feb 08 2012 Petr Lautrbach <plautrba@redhat.com> 2.1.23-29
- Change saslauth user homedir to /run/saslauthd (#752889)
- Change all /var/run/ to /run/
- DAEMONOPTS are not supported any more in systemd units

* Mon Jan 09 2012 Jeroen van Meeuwen <vanmeeuwen@kolabsys.com> - 2.1.23-28
- Ship with sasl_pwcheck_method: alwaystrue

* Mon Dec 12 2011 Petr Lautrbach <plautrba@redhat.com> 2.1.23-27
- remove support for logging of the remote host via PAM (#759334)
- fix systemd files (#750436)

* Wed Aug 10 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-26
- Add partial relro support for libraries

* Mon Jul 25 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-25
- Add support for berkeley db 5

* Wed Jun 29 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-23
- Migrate the package to full native systemd unit files, according to the Fedora
  packaging guidelines.

* Wed Jun  1 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-22
- repair rimap support (more packets in response)

* Wed May 25 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-21
- repair ntlm support

* Mon May 23 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-20
- add logging of the remote host via PAM

* Thu Apr 28 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-19
- temporarilly revert systemd units

* Tue Apr 26 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-18
- update scriptlets

* Fri Apr 22 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-17
- Add systemd units

* Wed Mar 23 2011 Tomas Mraz <tmraz@redhat.com> - 2.1.23-16
- Rebuilt with new mysqlclient

* Fri Feb 25 2011 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-15
- set correct license tag
- add ghost to /var/run/saslauthd

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.23-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Apr  9 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-13
- Add /etc/tmpfiles.d element (#662734)

* Fri Apr  9 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-12
- Update init script to impeach pid file

* Thu Mar 11 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-11
- Update pre post preun and postun scripts (#572399)

* Wed Mar 10 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-10
- Rewrite spec file, make corect CFLAGS, CPPFLAGS and LDFLAGS

* Mon Feb 22 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-9
- solve race condition (#566875)

* Wed Feb 17 2010 Stepan Kasal <skasal@redhat.com> - 2.1.23-8
- improve m4 quoting to fix saslauthd/configure (#566088)
- call autotools in build, not in prep

* Fri Feb  5 2010 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-7
- Add man page to testtcpauthd (#526189)

* Fri Oct 16 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-6
- Create the saslauth user according to fedora packaging guide

* Thu Sep 24 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-5
- Repair initscript to make condrestart working properly (#522103)

* Wed Sep 23 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-3
- Add possibility to run the saslauth without root privilegies (#185614)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.23-2
- rebuilt with new openssl

* Fri Aug  7 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.23-1
- update to 2.1.23

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.22-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 11 2009 Jan F. Chadima <jchadima@redhat.com> - 2.1.22-24
- repair sasl_encode64 nul termination (#487251)

* Thu Apr 16 2009 Robert Scheck <robert@fedoraproject.org> - 2.1.22-23
- Don't build the krb4 plugin as krb5 1.7 will drop it (#225974 #c6)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.22-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb  6 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.22-21
- fix build with gcc-4.4

* Fri Jan 23 2009 Tomas Mraz <tmraz@redhat.com> - 2.1.22-20
- set LDAP_OPT_TIMEOUT (#326452)
- provide LSB compatible init script (#246900)

* Fri Sep 26 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-19
- always use the current external db4 when linking,
  thanks to Dan Horak for the original patch (#464098)

* Wed Sep 10 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-18
- fix most critical build warnings (#433583)
- use external db4

* Fri Aug 29 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-17
- always link against the internal db4 (#459163)
- rediff patches for no fuzz

* Wed Jul  9 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-16
- update internal db4 (#449737)

* Tue Jul  1 2008 Tomas Mraz <tmraz@redhat.com> - 2.1.22-15
- drop reload from initscript help (#448154)
- fix hang in rimap auth method (#438533)
- build the krb4 plugin (#154675)

* Fri May 23 2008 Dennis Gilmore <dennis@ausil.us> - 2.1.22-14
- make it so that bootstrap actually works

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.1.22-13.1
- minor release bump for sparc rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.22-13
- Autorebuild for GCC 4.3

* Thu Feb 14 2008 Steve Conklin <sconklin@redhat.com> - 2.1.22-12
- rebuild for gcc4.3

* Fri Jan 25 2008 Steve Conklin <sconklin@redhat.com> - 2.1.22-11
- Cleanup after merge review bz #225673
- no longer mark /etc/rc.d/init.d/saslauthd as config file
- removed -x permissions on include files
- added devel package dependency on cyrus-sasl
- removed some remaining .la files that were being delivered

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.1.22-10
 - Rebuild for deps

* Wed Nov  7 2007 Steve Conklin <sconklin@redhat.com> - 2.1.22-9
- Fixed a typo in the spec file

* Wed Nov  7 2007 Steve Conklin <sconklin@redhat.com> - 2.1.22-8
- Removed srp plugin source and added dist to NVR

* Tue Sep 18 2007 Steve Conklin <sconklin@redhat.com> 2.1.22-7
- use db4 version 4.6.19 bz#249737

* Mon Feb 26 2007 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-6
- install config files and init scripts using -p
- pull in patch to build with current automake (#229010, Jacek Konieczny
  and Robert Scheck)
- remove prereq on ldconfig, RPM should pick it up based on the -libs
  scriptlets
- pull in patch to correctly detect gsskrb5_register_acceptor_identity
  (#200892, Mirko Streckenbach)
- move sasldb auxprop modules into the -lib subpackage, so that we'll pick
  it up for multilib systems

* Thu Feb 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- pull CVS fix for not tripping over extra commas in digest-md5
  challenges (#229640)

* Fri Feb 16 2007 Nalin Dahyabhai <nalin@redhat.com>
- remove static build, which is no longer a useful option because not all of
  our dependencies are available as static libraries
- drop patches which were needed to keep static builds going
- drop gssapi-generic patch due to lack of interest
- update the bundled copy of db to 4.5.20 (#229012)
- drop dbconverter-2, as we haven't bundled v1 libraries since FC4

* Tue Dec  5 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-5
- rebuild
- add 'authentication' or 'auxprop' to summaries for plugin packages to
  better indicate what the plugin provides
- switch from automake 1.9 to automake 1.7

* Fri Sep 29 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-4
- rebuild without 'dlcompat' bits (#206119)

* Mon Jul 17 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-3
- rebuild

* Tue Jun 20 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-2
- fix a typo in sasl_client_start(3) (#196066)

* Mon May 22 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-1
- update to 2.1.22, adding pluginviewer to %%{_sbindir}

* Tue May 16 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-12
- add conditionalized build dependency on openldap-devel (#191855)
- patch md5global.h to be the same on all architectures

* Thu Apr 27 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-11
- add unapplied patch which makes the DIGEST-MD5 plugin omit the realm
  argument when the environment has $CYRUS_SASL_DIGEST_MD5_OMIT_REALM set to a
  non-zero value, for testing purposes
- add missing buildrequires on zlib-devel (#190113)

* Mon Feb 20 2006 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-10
- add missing buildrequires on gdbm-devel (Karsten Hopp)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.21-9.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.21-9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-9
- use --as-needed to avoid linking dbconverter-2 with SQL libraries, which
  it doesn't use because it manipulates files directly (#173321)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-8
- rebuild with new OpenLDAP, overriding the version checks to assume that
  2.3.11 is acceptable
- remove a lingering patch for 1.x which we no longer use

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 2.1.21-7
- Rebuild due to mysql update.

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> 2.1.21-6
- rebuilt with new openssl

* Fri Sep  9 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-5
- add missing buildrequires: on groff (#163032)

* Thu Sep  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-4
- move the ldapdb auxprop support into a subpackage (#167300)
  (note: the ldap password check support in saslauthd doesn't use auxprop)

* Tue Aug 30 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-3
- correct a use of uninitialized memory in the bundled libdb (Arjan van de Ven)

* Mon Aug 29 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-2
- move the ANONYMOUS mech plugin to the -lib subpackage so that multilib
  systems can use it without installing the main package
- build the static libraries without sql auxprop support

* Mon Aug 29 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-1
- update to 2.1.21
- turn off compilation of libsasl v1 (finally)
- explicitly disable sqlite to avoid the build warning
- change the default mechanism which is set for saslauthd from "shadow" to
  "pam" (#159194)
- split the shared library up from saslauthd so that multilib systems don't
  have to pull in every dependency of saslauthd for the compat arch (#166749)

* Wed Apr 13 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-5
- rebuild with new deps

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-4
- rebuild with new deps

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 2.1.20-3
- rebuild against db-4.3.21.

* Thu Nov 11 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-2
- build with mysql-devel instead of mysqlclient10

* Mon Nov  1 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-1
- build with mysqlclient10 instead of mysql-devel

* Wed Oct 27 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-0
- update to 2.1.20, including the fix for CAN-2004-0884

* Tue Oct  5 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-3
- use notting's fix for incorrect patch for CAN-2004-0884 for 1.5.28

* Tue Oct  5 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-2
- don't trust the environment in setuid/setgid contexts (CAN-2004-0884, #134660)

* Thu Aug 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-1
- rebuild (the 2.1.19 changelog for fixing a buffer overflow referred to a CVS
  revision between 2.1.18 and 2.1.19)

* Mon Jul 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-0
- update to 2.1.19, maybe for update

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.18-4
- enable sql auxprop support in a subpackage
- include LDAP_SASLAUTHD documentation file (#124830)

* Fri Jun  4 2004 Nalin Dahyabhai <nalin@redhat.com>
- turn on ntlm in a subpackage

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> 2.1.18-3
- removed rpath

* Tue Mar 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.18-2
- turn on building of libsasl v1 again

* Fri Mar 12 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.18-1
- update to 2.1.18
- saslauthd's ldap code is no longer marked experimental, so we build it

* Mon Mar  8 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-4
- rebuild

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb  3 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-2
- include default /etc/sysconfig/saslauthd configuration file for the init
  script (#114868)

* Thu Jan 29 2004 Nalin Dahyabhai <nalin@redhat.com>
- drop saslauthd_version patch for libsasl2

* Thu Jan 29 2004 Nalin Dahyabhai <nalin@redhat.com>
- add a saslauthd_version option to libsasl's saslauthd client and teach it to
  do the right thing
- enable the saslauthd client code in libsasl version 1 (it's still going away!)
- add saslauthd1-checkpass/saslauthd2-checkpass for testing the above change

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-1
- forcibly disable otp and sql plugins at compile-time

* Fri Dec 19 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.17, forcing the gssapi plugin to be shared now, as before
- use a bundled libdb (#112215)
- build static-with-all-plugins and normal-shared libsasl versions
- add sasl2-{shared,static}-mechlist for very basic sanity checking
- make inclusion of sasl1 stuffs conditional, because it's so going away

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 2.1.15-7
- rebuild against db-4.2.52.

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-6
- use /dev/urandom instead of /dev/random for SASL2 (docs indicate that this is
  safe if you aren't using OTP or SRP, and we build neither); SASL1 appears to
  use it to seed the libc RNG only (#103378)

* Mon Oct 20 2003 Nalin Dahyabhai <nalin@redhat.com>
- obey RPM_OPT_FLAGS again when krb5_prefix != %%{_prefix}

* Fri Oct 17 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-5
- install saslauthd's mdoc page instead of the pre-formatted man page, which
  would get formatted again

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 2.1.15-5
- rebuild against db-4.2.42.

* Mon Sep 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- include testsaslauthd
- note in the README that the saslauthd protocol is different for v1 and v2,
  so v1's clients can't talk to the v2 server

* Thu Aug 21 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-4
- rebuild

* Thu Aug 21 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-3
- add logic to build with gssapi libs in either /usr or /usr/kerberos

* Mon Jul 21 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-2
- rebuild

* Tue Jul 15 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.15-1
- update to 2.1.15

* Mon Jul 14 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.14-1
- update to 2.1.14

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May  9 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.13-3
- change -m argument to saslauthd to be a directory instead of a path

* Thu May  8 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.13-2
- link libsasl2 with -lpthread to ensure that the sasldb plug-in can always
  be loaded

* Tue Apr 29 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.13-1
- update to 2.1.13

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.10-3
- rebuild

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- consider either des_cbc_encrypt or DES_cbc_encrypt to be sufficient when
  searching for a DES implementation in libcrypto
- pull in CPPFLAGS and LDFLAGS from openssl's pkg-config data, if it exists

* Mon Dec  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.10-2
- rebuild

* Mon Dec  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.10-1
- update to 2.1.10, fixing buffer overflows in libsasl2 noted by Timo Sirainen

* Tue Nov 12 2002 Tim Powers <timp@redhat.com> 2.1.7-5
- remove files from $RPM_BUILD_ROOT that we don't intend to include

* Wed Oct  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.7-4
- update to SASLv1 to final 1.5.28

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.7-3
- rebuild, overriding sasldir when running make so that on multilib systems
  applications will be able to load modules for the right arch

* Mon Sep  2 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.7-2
- include dbconverter-2 (#68741)

* Fri Aug  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.7-1
- update to 2.1.7, fixing a race condition in digest-md5

* Wed Jul 17 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.6-1
- update to 2.1.6 and 1.5.28

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.5-1
- update to 2.1.5

* Mon Jun 10 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.4-1
- update to 2.1.4

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.2-1
- modify to build with db 4.x

* Thu Apr 18 2002 Nalin Dahyabhai <nalin@redhat.com>
- update cyrus-sasl 2 to 2.1.2
- change buildreq to db3-devel

* Tue Feb 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.1-3
- suppress output to stdout/stderr in %%postun

* Sun Feb 10 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.1-2
- configure sasldb2 to use berkeley DB instead of gdbm

* Wed Feb  6 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.1-1
- update to 2.1.1

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.0-1
- marge 1.5.24 back in, making a note that it should be removed at some
  point in the future

* Wed Jan 30 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.0, which is designed to be installed in parallel with cyrus sasl
  1.x, so fork the package and rename it to cyrus-sasl2
- add the sasldb auxprop plugin to the main package
- add disabled-by-default saslauthd init script
- move the .la files for plugins into their respective packages -- they're
  needed by the library

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-24
- free ride through the build system

* Fri Nov  2 2001 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-23
- patch to fix possible syslog format-string vulnerability 

* Mon Oct 29 2001 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-22
- add pam-devel as a buildprereq

* Wed Aug 29 2001 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-21
- include sample programs in the -devel subpackage, prefixing their names
  with "sasl-" to reduce future potential naming conflicts

* Tue Aug 14 2001 Nalin Dahyabhai <nalin@redhat.com> 1.5.24-20
- build without -ggdb

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- add gdbm-devel as a build dependency (#44990)
- split off CRAM-MD5 and DIGEST-MD5 into a subpackage of their own (#43079,
  and dialogs with David L. Parsley)

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- split out the PLAIN and LOGIN mechanisms into their own package (this allows
  an administrator to disable them by simply removing the package)

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Wed Dec  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix gssapi-over-tls

* Fri Oct 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable static libraries, but always build with -fPIC

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure the version of 1.5.24 in the package matches the masters (#18968)

* Mon Oct  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- re-add the libsasl.so symlink to the -devel package (oops)

* Fri Oct  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- move .so files for modules to their respective packages -- they're not -devel
  links meant for use by ld anyway

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- split off -devel subpackage
- add a -gssapi subpackage for the gssapi plugins

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix the summary text

* Sun Aug 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- re-enable arcfour and CRAM

* Fri Aug  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- force use of gdbm for database files to avoid DB migration weirdness
- enable login mechanism
- disable gssapi until it can coexist peacefully with non-gssapi setups
- actually do a make in the build section (#15410)

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.5.24

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment (release 3)

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- don't muck with syslogd in post
- remove patch for db-3.0 wackiness, no longer needed

* Thu Jun  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS cleanup
- don't strip anything by default

* Fri Feb 11 2000 Tim Powers <timp@redhat.com>
- fixed man pages not being gzipped

* Tue Nov 16 1999 Tim Powers <timp@redhat.com>
- incorporated changes from Mads Kiilerich
- release number is 1, not mk1

* Wed Nov 10 1999 Mads Kiilerich <mads@kiilerich.com>
- updated to sasl 1.5.11
- configure --disable-krb4 --without-rc4 --disable-cram 
  because of missing libraries and pine having cram as default...
- handle changing libsasl.so versions

* Mon Aug 30 1999 Tim Powers <timp@redhat.com>
- changed group

* Fri Aug 13 1999 Tim Powers <timp@redhat.com>
- first build for Powertools

## END: Generated by rpmautospec
