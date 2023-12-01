%define _soversion 3
%global _plugindir2 %{_libdir}/sasl2

Summary:        Cyrus Simple Authentication Service Layer (SASL) library
Name:           cyrus-sasl
Version:        2.1.28
Release:        5%{?dist}
License:        BSD with advertising
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.cyrusimap.org/sasl/
Source0:        https://github.com/cyrusimap/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

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
BuildRequires:  libxcrypt-devel

Requires:       %{name}-lib = %{version}-%{release}
Requires:       krb5 >= 1.12
Requires:       openssl
Requires:       pam
Requires:       systemd
Requires:       libdb

Obsoletes:      %{name}-bootstrap <= %{version}-%{release}

%description
The Cyrus SASL package contains a Simple Authentication and Security
Layer, a method for adding authentication support to
connection-based protocols. To use SASL, a protocol includes a command
for identifying and authenticating a user to a server and for
optionally negotiating protection of subsequent protocol interactions.
If its use is negotiated, a security layer is inserted between the
protocol and the connection.

%package devel
Summary:        Files needed for developing applications with Cyrus SASL

Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-lib = %{version}-%{release}
Requires:       pkg-config
Obsoletes:      %{name}-bootstrap-devel <= %{version}-%{release}

%description devel
The %{name}-devel package contains files needed for developing and
compiling applications which use the Cyrus SASL library.

%package gs2
Summary:        GS2 support for Cyrus SASL

Requires:       %{name}-lib = %{version}-%{release}

%description gs2
The %{name}-gs2 package contains the Cyrus SASL plugin which supports
the GS2 authentication scheme.

%package gssapi
Summary:        GSSAPI authentication support for Cyrus SASL

Requires:       %{name}-lib = %{version}-%{release}

%description gssapi
The %{name}-gssapi package contains the Cyrus SASL plugins which
support GSSAPI authentication. GSSAPI is commonly used for Kerberos
authentication.

%package ldap
Summary:        LDAP auxprop support for Cyrus SASL

Requires:       %{name}-lib = %{version}-%{release}

%description ldap
The %{name}-ldap package contains the Cyrus SASL plugin which supports using
a directory server, accessed using LDAP, for storing shared secrets.

%package lib
Summary:        Shared libraries needed by applications which use Cyrus SASL
Obsoletes:      %{name}-bootstrap-lib <= %{version}-%{release}

%description lib
The %{name}-lib package contains shared libraries which are needed by
applications which use the Cyrus SASL library.

%package md5
Summary:        CRAM-MD5 and DIGEST-MD5 authentication support for Cyrus SASL

Requires:       %{name}-lib = %{version}-%{release}

%description md5
The %{name}-md5 package contains the Cyrus SASL plugins which support
CRAM-MD5 and DIGEST-MD5 authentication schemes.

%package ntlm
Summary:        NTLM authentication support for Cyrus SASL

Requires:       %{name}-lib = %{version}-%{release}

%description ntlm
The %{name}-ntlm package contains the Cyrus SASL plugin which supports
the NTLM authentication scheme.

%package plain
Summary:        PLAIN and LOGIN authentication support for Cyrus SASL

Requires:       %{name}-lib = %{version}-%{release}

%description plain
The %{name}-plain package contains the Cyrus SASL plugins which support
PLAIN and LOGIN authentication schemes.

%package scram
Summary:        SCRAM auxprop support for Cyrus SASL

Requires:       %{name}-lib = %{version}-%{release}

%description scram
The %{name}-scram package contains the Cyrus SASL plugin which supports
the SCRAM authentication scheme.

%package sql
Summary:        SQL auxprop support for Cyrus SASL

Requires:       %{name}-lib = %{version}-%{release}

%description sql
The %{name}-sql package contains the Cyrus SASL plugin which supports
using a RDBMS for storing shared secrets.

%prep
%autosetup -p1

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
%systemd_post saslauthd.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart saslauthd.service

%preun
%systemd_preun saslauthd.service

%files
%defattr(-,root,root)
%license COPYING
%{_sysconfdir}/sysconfig/saslauthd
/lib/systemd/system/saslauthd.service
%{_libdir}/systemd/system-preset/50-saslauthd.preset
%{_sbindir}/*
%{_datadir}/licenses/%{name}/LICENSE
%{_mandir}/man8/*

%files devel
%{_includedir}/*
%{_libdir}/libsasl2.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files gs2
%{_plugindir2}/libgs2.so
%{_plugindir2}/libgs2.so.%{_soversion}*

%files gssapi
%{_plugindir2}/libgssapiv2.so
%{_plugindir2}/libgssapiv2.so.%{_soversion}*

%files ldap
%{_plugindir2}/libldapdb.so
%{_plugindir2}/libldapdb.so.%{_soversion}*

%files lib
%license COPYING
%doc AUTHORS doc/html/*.html
%{_libdir}/libsasl2.so.%{_soversion}*
%dir %{_plugindir2}/
%{_plugindir2}/libanonymous.so
%{_plugindir2}/libanonymous.so.%{_soversion}*
%{_plugindir2}/libsasldb.so
%{_plugindir2}/libsasldb.so.%{_soversion}*
%{_sbindir}/saslpasswd2
%{_sbindir}/sasldblistusers2

%files md5
%{_plugindir2}/libcrammd5.so
%{_plugindir2}/libcrammd5.so.%{_soversion}*
%{_plugindir2}/libdigestmd5.so
%{_plugindir2}/libdigestmd5.so.%{_soversion}*

%files ntlm
%{_plugindir2}/libntlm.so
%{_plugindir2}/libntlm.so.%{_soversion}*

%files plain
%{_plugindir2}/liblogin.so
%{_plugindir2}/liblogin.so.%{_soversion}*
%{_plugindir2}/libplain.so
%{_plugindir2}/libplain.so.%{_soversion}*

%files scram
%{_plugindir2}/libscram.so
%{_plugindir2}/libscram.so.%{_soversion}*

%files sql
%{_plugindir2}/libsql.so
%{_plugindir2}/libsql.so.%{_soversion}*

%changelog
* Wed Nov 15 2023 Andrew Phelps <anphel@microsoft.com> - 2.1.28-5
- Add BR for libxcrypt-devel

* Mon Feb 27 2023 Cameron Baird <cameronbaird@microsoft.com> - 2.1.28-4
- Fix Obsoletes happening in md5 subpackage when it should be lib.
- Gate cyrus-sasl obsoletes by pkg version/rel

* Thu Feb 23 2023 Saul Paredes <saulparedes@microsoft.com> - 2.1.28-3
- Bump release to solve dependency issue

* Mon Feb 13 2023 Sriram Nambakam <snambakam@microsoft.com> - 2.1.28-2
- Indicate this package obsoletes cyrus-sasl-bootstrap

* Wed Mar 09 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.28-1
- Updating to version 2.1.28 to address CVE-2022-24407.

* Tue Nov 30 2021 Mateusz Malisz <mamalisz@microsoft.com> - 2.1.27-10
- Add libdb as an explicit dependency.

* Tue Sep 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.27-9
- Introduced following subpackages using Fedora 32 (license: MIT) specs as guidance:
  - cyrus-sasl-gs2,
  - cyrus-sasl-ldap,
  - cyrus-sasl-lib,
  - cyrus-sasl-md5,
  - cyrus-sasl-ntlm,
  - cyrus-sasl-plain,
  - cyrus-sasl-scram,
  - cyrus-sasl-sql.
- Moving common libs into the "*-devel" and "*-libs" subpackages.
- Moving MD5 plug-in libs into the "*-md5" subpackage.
- Removed SRP libs as they were unused.

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.1.27-8
- Merge the following releases from 1.0 to dev branch
- oliviacrain@microsoft.com, 2.1.27-5: Add nopatch for CVE-2020-8032, Lint spec

* Tue Jan 12 2021 Ruying Chen <v-ruyche@microsoft.com> - 2.1.27-7
- Provide cyrus-sasl-plain.

* Thu Dec 10 2020 Joe Schmitt <joschmit@microsoft.com> - 2.1.27-6
- Provide cyrus-sasl-gssapi and isa version.

* Tue Nov 03 2020 Joe Schmitt <joschmit@microsoft.com> - 2.1.27-5
- Provide cyrus-sasl-devel.

*   Thu May 28 2020 Andrew Phelps <anphel@microsoft.com> 2.1.27-4
-   Add patch to fix CVE-2019-19906

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.1.27-3
-   Added %%license line automatically

*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 2.1.27-2
-   Renaming Linux-PAM to pam

*   Wed Mar 25 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.1.27-1
-   Update version to 2.1.27. License verified. URL and Source0 updated.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.1.26-15
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Tue Nov 21 2017 Anish Swaminathan <anishs@vmware.com>  2.1.26-14
-   Update patch for memory leak fix

*   Tue Oct 10 2017 Anish Swaminathan <anishs@vmware.com>  2.1.26-13
-   Add patch for memory leak fix

*   Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com>  2.1.26-12
-   Disabled saslauthd service by default

*   Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.26-11
-   BuildRequires Linux-PAM-devel

*   Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> 2.1.26-10
-   Required krb5-devel.

*   Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.1.26-9
-   Modified %check

*   Thu May 26 2016 Divya Thaluru <dthaluru@vmware.com>  2.1.26-8
-   Fixed logic to restart the active services after upgrade

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.1.26-7
-   GA - Bump release of all rpms

*   Tue May 3 2016 Divya Thaluru <dthaluru@vmware.com>  2.1.26-6
-   Fixing spec file to handle rpm upgrade scenario correctly

*   Thu Dec 10 2015 Xiaolin Li <xiaolinl@vmware.com>  2.1.26-5
-   Add systemd to Requires and BuildRequires.

*   Wed Nov 11 2015 Xiaolin Li <xiaolinl@vmware.com> 2.1.26-4
-   Add saslauthd service to systemd.

*   Tue Sep 01 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.1.26-3
-   Enable CRAM.

*   Thu Jul 16 2015 Divya Thaluru <dthaluru@vmware.com> 2.1.26-2
-   Disabling parallel threads in make

*   Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.1.26-1
-   Initial build. First version
