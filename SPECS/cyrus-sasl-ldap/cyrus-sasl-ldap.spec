# NOTE: this is a copy of 'cyrus-sasl.spec' with the only difference being the `--with-ldap` config option meant to enable building the `openldap`-dependent bits of `cyrus-sasl-ldap`.
# The spec was split to break the cyclic build dependency between `openldap` and `cyrus-sasl`.
%define _soversion 3
%global _plugindir2 %{_libdir}/sasl2
%global _base_name cyrus-sasl

Summary:        Cyrus Simple Authentication Service Layer (SASL) library
Name:           %{_base_name}-ldap
Version:        2.1.28
Release:        2%{?dist}
License:        BSD with advertising
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.cyrusimap.org/sasl/
Source0:        https://github.com/cyrusimap/%{_base_name}/releases/download/%{_base_name}-%{version}/%{_base_name}-%{version}.tar.gz

BuildRequires:  e2fsprogs-devel
BuildRequires:  krb5-devel >= 1.12
BuildRequires:  mariadb-devel
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  postgresql-devel
BuildRequires:  postgresql-libs
BuildRequires:  systemd
BuildRequires:  libdb-devel

Requires:       %{_base_name}-lib = %{version}-%{release}

%description
The Cyrus SASL package contains a Simple Authentication and Security
Layer, a method for adding authentication support to
connection-based protocols. To use SASL, a protocol includes a command
for identifying and authenticating a user to a server and for
optionally negotiating protection of subsequent protocol interactions.
If its use is negotiated, a security layer is inserted between the
protocol and the connection.

The %{_base_name}-ldap package contains the Cyrus SASL plugin which supports using
a directory server, accessed using LDAP, for storing shared secrets.

%prep
%autosetup -n %{_base_name}-%{version} -p1

%build
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

autoreconf -fi
%configure \
    CFLAGS="%{optflags} -fPIC" \
    CXXFLAGS="%{optflags}" \
    --disable-macos-framework \
    --disable-otp \
    --disable-sample \
    --disable-srp \
    --disable-static \
    --enable-anon \
    --enable-digest \
    --enable-fast-install \
    --enable-gss_mutexes \
    --enable-krb4 \
    --enable-ldapdb \
    --enable-login \
    --enable-ntlm \
    --enable-plain \
    --enable-shared \
    --enable-sql \
    --with-bdb=db \
    --with-dblib=berkeley \
    --with-ldap \
    --with-mysql=yes \
    --with-pgsql=yes \
    --with-plugindir=%{_plugindir2} \
    --with-saslauthd=/run/saslauthd \
    --without-authdaemond \
    --without-sqlite

make

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
find %{buildroot} -type f -name "*.la" -delete -print
install -D -m644 COPYING %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
%{_fixperms} %{buildroot}/*

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
cat << EOF >> %{buildroot}/%{_sysconfdir}/sysconfig/saslauthd
# Directory in which to place saslauthd's listening socket, pid file, and so
# on.  This directory must already exist.
SOCKETDIR=/run/saslauthd

# Mechanism to use when checking passwords.  Run "saslauthd -v" to get a list
# of which mechanism your installation was compiled with the ablity to use.
MECH=pam

# Additional flags to pass to saslauthd on the command line.  See saslauthd(8)
# for the list of accepted flags.
FLAGS=
EOF

mkdir -p %{buildroot}/lib/systemd/system
cat << EOF >> %{buildroot}/lib/systemd/system/saslauthd.service
[Unit]
Description=SASL authentication daemon.

[Service]
Type=forking
PIDFile=/run/saslauthd/saslauthd.pid
EnvironmentFile=%{_sysconfdir}/sysconfig/saslauthd
ExecStart=%{_sbindir}/saslauthd -m \$SOCKETDIR -a \$MECH \$FLAGS
RuntimeDirectory=saslauthd

[Install]
WantedBy=multi-user.target
EOF

install -vdm755 %{buildroot}%{_libdir}/systemd/system-preset
echo "disable saslauthd.service" > %{buildroot}%{_libdir}/systemd/system-preset/50-saslauthd.preset

%check
make %{?_smp_mflags} check

%post
%{_sbindir}/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_plugindir2}/libldapdb.so
%{_plugindir2}/libldapdb.so.%{_soversion}*

# %files -n %{_base_name}
%exclude %{_sysconfdir}/sysconfig/saslauthd
%exclude /lib/systemd/system/saslauthd.service
%exclude %{_libdir}/systemd/system-preset/50-saslauthd.preset
%exclude %{_sbindir}/*
%exclude %{_datadir}/licenses/%{name}/LICENSE
%exclude %{_mandir}/man8/*

# %files -n %{_base_name}-devel
%exclude %{_includedir}/*
%exclude %{_libdir}/libsasl2.so
%exclude %{_libdir}/pkgconfig/*.pc
%exclude %{_mandir}/man3/*

# %files -n %{_base_name}-gs2
%exclude %{_plugindir2}/libgs2.so
%exclude %{_plugindir2}/libgs2.so.%{_soversion}*

# %files -n %{_base_name}-gssapi
%exclude %{_plugindir2}/libgssapiv2.so
%exclude %{_plugindir2}/libgssapiv2.so.%{_soversion}*

# %files -n %{_base_name}-lib
#%exclude COPYING
#%exclude doc/html/*.html
%exclude %{_libdir}/libsasl2.so.%{_soversion}*
%exclude %dir %{_plugindir2}/
%exclude %{_plugindir2}/libanonymous.so
%exclude %{_plugindir2}/libanonymous.so.%{_soversion}*
%exclude %{_plugindir2}/libsasldb.so
%exclude %{_plugindir2}/libsasldb.so.%{_soversion}*
%exclude %{_sbindir}/saslpasswd2
%exclude %{_sbindir}/sasldblistusers2

# %files -n %{_base_name}-md5
%exclude %{_plugindir2}/libcrammd5.so
%exclude %{_plugindir2}/libcrammd5.so.%{_soversion}*
%exclude %{_plugindir2}/libdigestmd5.so
%exclude %{_plugindir2}/libdigestmd5.so.%{_soversion}*

# %files -n %{_base_name}-ntlm
%exclude %{_plugindir2}/libntlm.so
%exclude %{_plugindir2}/libntlm.so.%{_soversion}*

# %files -n %{_base_name}-plain
%exclude %{_plugindir2}/liblogin.so
%exclude %{_plugindir2}/liblogin.so.%{_soversion}*
%exclude %{_plugindir2}/libplain.so
%exclude %{_plugindir2}/libplain.so.%{_soversion}*

# %files -n %{_base_name}-scram
%exclude %{_plugindir2}/libscram.so
%exclude %{_plugindir2}/libscram.so.%{_soversion}*

# %files -n %{_base_name}-sql
%exclude %{_plugindir2}/libsql.so
%exclude %{_plugindir2}/libsql.so.%{_soversion}*

%changelog
* Tue Jan 31 2023 Sriram Nambakam <snambakam@microsoft.com> - 2.1.28-2
- Cloning from the cyrus-sasl spec version 2.1.28-1
- Resolve cyclic dependency with openldap on cyrus-sasl
- Initial CBL-Mariner import from Photon (license: Apache2).
- License verified

