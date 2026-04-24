# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define contentdir %{_datadir}/httpd
%define docroot /var/www
%define suexec_caller apache
%define mmn 20120211
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}
%define vstring %(source /etc/os-release; echo ${NAME})
%define bugurl %(source /etc/os-release; echo ${BUG_REPORT_URL})
%if 0%{?fedora} > 26 || 0%{?rhel} > 7
%global mpm event
%else
%global mpm prefork
%endif

%if 0%{?fedora} > 35 || 0%{?rhel} > 9
%bcond_without pcre2
%bcond_with pcre
%else
%bcond_with pcre2
%bcond_without pcre
%endif

%if 0%{?fedora} > 40 || 0%{?rhel} > 9
%bcond_with engine
%else
%bcond_without engine
%endif

# Similar issue to https://bugzilla.redhat.com/show_bug.cgi?id=2043092
%undefine _package_note_flags

Summary: Apache HTTP Server
Name: httpd
Version: 2.4.66
Release: 2%{?dist}
URL: https://httpd.apache.org/
Source0: https://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2
Source1: https://www.apache.org/dist/httpd/httpd-%{version}.tar.bz2.asc
# gpg key file downloaded and verified by luhliarik
# https://httpd.apache.org/dev/verification.html
Source2: https://dist.apache.org/repos/dist/release/httpd/KEYS
Source3: httpd.logrotate
Source4: instance.conf
Source5: httpd-ssl-pass-dialog
Source6: httpd.tmpfiles
Source7: httpd.service
Source8: action-graceful.sh
Source9: action-configtest.sh
Source10: server-status.conf
Source11: httpd.conf
Source12: 00-base.conf
Source13: 00-mpm.conf
Source14: 00-lua.conf
Source15: 01-cgi.conf
Source16: 00-dav.conf
Source17: 00-proxy.conf
Source18: 00-ssl.conf
Source19: 01-ldap.conf
Source20: 00-proxyhtml.conf
Source21: userdir.conf
Source22: ssl.conf
Source23: welcome.conf
Source24: manual.conf
Source25: 00-systemd.conf
Source26: 01-session.conf
Source27: 10-listen443.conf
Source28: httpd.socket
Source29: 00-optional.conf
Source30: README.confd
Source31: README.confmod
Source32: httpd.service.xml
Source33: htcacheclean.service.xml
Source34: httpd.conf.xml
Source35: 00-brotli.conf
Source40: htcacheclean.service
Source41: htcacheclean.sysconf
Source42: httpd-init.service
Source43: httpd-ssl-gencerts
Source44: httpd@.service
Source45: config.layout
Source46: apachectl.sh
Source47: apachectl.xml
Source48: apache-poweredby.png
Source49: httpd.sysusers

# build/scripts patches
Patch2: httpd-2.4.43-apxs.patch
Patch3: httpd-2.4.43-deplibs.patch
# Needed for socket activation and mod_systemd patch
Patch19: httpd-2.4.53-detect-systemd.patch
# Features/functional changes
Patch20: httpd-2.4.48-r1842929+.patch
Patch21: httpd-2.4.64-mod_systemd.patch
Patch22: httpd-2.4.53-export.patch
Patch23: httpd-2.4.43-corelimit.patch
Patch24: httpd-2.4.54-icons.patch
Patch25: httpd-2.4.43-cachehardmax.patch
Patch26: httpd-2.4.43-sslciphdefault.patch
Patch27: httpd-2.4.64-sslprotdefault.patch
Patch28: httpd-2.4.43-logjournal.patch
Patch29: httpd-2.4.63-r1912477+.patch
Patch30: httpd-2.4.64-separate-systemd-fns.patch

# Bug fixes
# https://bugzilla.redhat.com/show_bug.cgi?id=1397243
Patch60: httpd-2.4.43-enable-sslv3.patch
Patch61: httpd-2.4.65-hcheck-stuck.patch

# Security fixes
# Patch200: ...

# Apache-2.0: everything
# BSD-3-Clause: util_pcre.c, ap_regex.h
# metamail AND HPND-sell-variant:: server/util_md5.c:
# Spencer-94: modules/metadata/mod_mime_magic.c
License: Apache-2.0 AND (BSD-3-Clause AND metamail AND HPND-sell-variant AND Spencer-94)

BuildRequires: gcc, autoconf, pkgconfig, findutils, xmlto
BuildRequires: perl-interpreter, perl-generators, systemd-devel
BuildRequires: zlib-devel, libselinux-devel, lua-devel, brotli-devel
BuildRequires: apr-devel >= 1.5.0, apr-util-devel >= 1.5.0
BuildRequires: openldap-devel
BuildRequires: systemd-rpm-macros
BuildRequires: libxcrypt-devel
%if %{with pcre2}
BuildRequires: pcre2-devel
%endif
%if %{with pcre}
BuildRequires: pcre-devel > 5.0
%endif
BuildRequires: gnupg2
Requires: system-logos(httpd-logo-ng)
Provides: webserver
Requires: httpd-core = 0:%{version}-%{release}
Recommends: mod_http2, mod_lua
%{?systemd_requires}

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package core
Summary: httpd minimal core
Provides: mod_dav = %{version}-%{release}, httpd-suexec = %{version}-%{release}
Provides: httpd-mmn = %{mmn}, httpd-mmn = %{mmnisa}
Provides: mod_proxy_uwsgi = %{version}-%{release}
Requires: /etc/mime.types
Requires: httpd-tools = %{version}-%{release}
Requires: httpd-filesystem = %{version}-%{release}
%if 0%{?fedora} > 39 || 0%{?rhel} > 9
Requires: apr-util-1(dbm)%{_isa}
%endif
Requires(pre): httpd-filesystem
Conflicts: apr < 1.5.0-1
Conflicts: httpd < 2.4.53-2
Obsoletes: mod_proxy_uwsgi < 2.0.17.1-2

# Compat symlinks for Requires in other packages.
%if "%{_sbindir}" == "%{_bindir}"
# We rely on filesystem to create the symlink for us.
Requires:           filesystem(unmerged-sbin-symlinks)
Provides:           /usr/sbin/apachectl
Provides:           /usr/sbin/httpd
%endif

%description core
The httpd-core package contains essential httpd binaries.

%package devel
Summary: Development interfaces for the Apache HTTP Server
Requires: apr-devel, apr-util-devel, pkgconfig, libtool
Requires: httpd-core = 0:%{version}-%{release}

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP Server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package manual
Summary: Documentation for the Apache HTTP Server
Requires: httpd-core = 0:%{version}-%{release}
BuildArch: noarch

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP Server. The information can
also be found at https://httpd.apache.org/docs/2.4/.

%package filesystem
Summary: The basic directory layout for the Apache HTTP Server
BuildArch: noarch
%{?sysusers_requires_compat}

%description filesystem
The httpd-filesystem package contains the basic directory layout
for the Apache HTTP Server including the correct permissions
for the directories.

%package tools
Summary: Tools for use with the Apache HTTP Server

%description tools
The httpd-tools package contains tools which can be used with 
the Apache HTTP Server.

%package -n mod_ssl
Summary: SSL/TLS module for the Apache HTTP Server
Epoch: 1
BuildRequires: openssl-devel
Requires(pre): httpd-filesystem
Requires: httpd-core = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
Requires: sscg >= 3.0.3, /usr/bin/hostname
# Require an OpenSSL which supports PROFILE=SYSTEM
Conflicts: openssl-libs < 1:1.0.1h-4
# mod_ssl/mod_nss cannot both be loaded simultaneously
Conflicts: mod_nss

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache HTTP
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%package -n mod_proxy_html
Summary: HTML and XML content filters for the Apache HTTP Server
Requires: httpd-core = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
BuildRequires: libxml2-devel
BuildRequires: make
Epoch: 1
Obsoletes: mod_proxy_html < 1:2.4.1-2

%description -n mod_proxy_html
The mod_proxy_html and mod_xml2enc modules provide filters which can
transform and modify HTML and XML content.

%package -n mod_ldap
Summary: LDAP authentication modules for the Apache HTTP Server
Requires: httpd-core = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
Requires: apr-util-ldap

%description -n mod_ldap
The mod_ldap and mod_authnz_ldap modules add support for LDAP
authentication to the Apache HTTP Server.

%package -n mod_session
Summary: Session interface for the Apache HTTP Server
Requires: httpd-core = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}

%description -n mod_session
The mod_session module and associated backends provide an abstract
interface for storing and accessing per-user session data.

%package -n mod_lua
Summary: Lua scripting support for the Apache HTTP Server
Requires: httpd-core = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}

%description -n mod_lua
The mod_lua module allows the server to be extended with scripts
written in the Lua programming language.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -S gendiff

# Patch in the vendor string
sed -i '/^#define PLATFORM/s/Unix/%{vstring}/' os/unix/os.h

# Prevent use of setcap in "install-suexec-caps" target.
sed -i '/suexec/s,setcap ,echo Skipping setcap for ,' Makefile.in

%if %{without engine}
: Forcibly disable ENGINE support in mod_ssl
sed -i.engine '/^#define MODSSL_HAVE_ENGINE_API/{s/1/0/}' modules/ssl/ssl_private.h
! diff -u modules/ssl/ssl_private.h{.engine,}
%endif

# Example conf for instances
cp $RPM_SOURCE_DIR/instance.conf .
sed < $RPM_SOURCE_DIR/httpd.conf >> instance.conf '
0,/^ServerRoot/d;
/# Supplemental configuration/,$d
/^ *CustomLog .logs/s,logs/,logs/${HTTPD_INSTANCE}_,
/^ *ErrorLog .logs/s,logs/,logs/${HTTPD_INSTANCE}_,
'
touch -r $RPM_SOURCE_DIR/instance.conf instance.conf
cp -p $RPM_SOURCE_DIR/server-status.conf server-status.conf

# Safety check: prevent build if defined MMN does not equal upstream MMN.
vmmn=`echo MODULE_MAGIC_NUMBER_MAJOR | cpp -include include/ap_mmn.h | sed -n '/^2/p'`
if test "x${vmmn}" != "x%{mmn}"; then
   : Error: Upstream MMN is now ${vmmn}, packaged MMN is %{mmn}
   : Update the mmn macro and rebuild.
   exit 1
fi

# A new logo which comes together with a new test page
cp %{SOURCE48} ./docs/icons/apache_pb3.png

# Provide default layout
cp $RPM_SOURCE_DIR/config.layout .

for f in httpd.conf htcacheclean.service httpd.service apachectl; do
   sed '
s,@MPM@,%{mpm},g
s,@DOCROOT@,%{docroot},g
s,@LOGDIR@,%{_localstatedir}/log/httpd,g
s|@BUG_REPORT_URL@|%{bugurl}|g
' < $RPM_SOURCE_DIR/${f}.xml > ${f}.xml
   xmlto man ${f}.xml
done

: Building with MMN %{mmn}, MMN-ISA %{mmnisa}
: Default MPM is %{mpm}, vendor string is '%{vstring}'
: Regex Engine: PCRE=%{with pcre} PCRE2=%{with pcre2}
: mod_ssl ENGINE support: %{with engine}

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
        support/apxs.in

%set_build_flags

# Build the daemon
./configure \
        --prefix=%{_sysconfdir}/httpd \
        --exec-prefix=%{_prefix} \
        --bindir=%{_bindir} \
        --sbindir=%{_sbindir} \
        --mandir=%{_mandir} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir}/httpd/conf \
        --includedir=%{_includedir}/httpd \
        --libexecdir=%{_libdir}/httpd/modules \
        --datadir=%{contentdir} \
        --enable-layout=Fedora \
        --with-installbuilddir=%{_libdir}/httpd/build \
        --enable-mpms-shared=all \
        --with-apr=%{_prefix} --with-apr-util=%{_prefix} \
        --enable-suexec --with-suexec \
        --enable-suexec-capabilities \
        --with-suexec-caller=%{suexec_caller} \
        --with-suexec-docroot=%{docroot} \
        --without-suexec-logfile \
        --with-suexec-syslog \
        --with-suexec-bin=%{_sbindir}/suexec \
        --with-suexec-uidmin=1000 --with-suexec-gidmin=1000 \
        --with-brotli \
        --enable-pie \
%if %{with pcre2}
        --with-pcre2=%{_bindir}/pcre2-config \
%endif
%if %{with pcre}
        --with-pcre=%{_bindir}/pcre-config \
%endif
        --enable-mods-shared=all \
        --enable-ssl --with-ssl --disable-distcache \
        --enable-proxy --enable-proxy-fdpass \
        --enable-cache \
        --enable-disk-cache \
        --enable-ldap --enable-authnz-ldap \
        --enable-cgid --enable-cgi --enable-authnz-fcgi \
        --enable-cgid-fdpassing \
        --enable-authn-anon --enable-authn-alias \
        --enable-systemd \
        --disable-imagemap --disable-file-cache \
        --disable-http2 \
        --disable-md \
        $*

if grep -q ac_cv_have_threadsafe_pollset=no config.log; then
   cat config.log
   : Failed to find thread-safe APR.
   exit 1
fi

%make_build

%install
rm -rf $RPM_BUILD_ROOT

%make_install

# Install systemd service files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
for s in httpd.service htcacheclean.service httpd.socket \
         httpd@.service httpd-init.service; do
  install -p -m 644 $RPM_SOURCE_DIR/${s} \
                    $RPM_BUILD_ROOT%{_unitdir}/${s}
done

# install conf file/directory
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d \
      $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d
install -m 644 $RPM_SOURCE_DIR/README.confd \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/README
install -m 644 $RPM_SOURCE_DIR/README.confmod \
    $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/README
for f in 00-base.conf 00-mpm.conf 00-lua.conf 01-cgi.conf 00-dav.conf \
         00-proxy.conf 00-ssl.conf 01-ldap.conf 00-proxyhtml.conf \
         01-ldap.conf 00-systemd.conf 01-session.conf 00-optional.conf \
         00-brotli.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/$f
done

sed -i '/^#LoadModule mpm_%{mpm}_module /s/^#//' \
     $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/00-mpm.conf
touch -r $RPM_SOURCE_DIR/00-mpm.conf \
     $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/00-mpm.conf

# install systemd override drop directory
# Web application packages can drop snippets into this location if
# they need ExecStart[pre|post].
mkdir $RPM_BUILD_ROOT%{_unitdir}/httpd.service.d \
      $RPM_BUILD_ROOT%{_unitdir}/httpd.socket.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/httpd.service.d

install -m 644 -p $RPM_SOURCE_DIR/10-listen443.conf \
      $RPM_BUILD_ROOT%{_unitdir}/httpd.socket.d/10-listen443.conf

for f in welcome.conf ssl.conf manual.conf userdir.conf; do
  install -m 644 -p $RPM_SOURCE_DIR/$f \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/$f
done

# Split-out extra config shipped as default in conf.d:
for f in autoindex; do
  install -m 644 docs/conf/extra/httpd-${f}.conf \
        $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/${f}.conf
done

# Extra config trimmed:
rm -v docs/conf/extra/httpd-{ssl,userdir}.conf

rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/*.conf
install -m 644 -p $RPM_SOURCE_DIR/httpd.conf \
   $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

mkdir $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 -p $RPM_SOURCE_DIR/htcacheclean.sysconf \
   $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/htcacheclean

# tmpfiles.d configuration
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d 
install -m 644 -p $RPM_SOURCE_DIR/httpd.tmpfiles \
   $RPM_BUILD_ROOT%{_prefix}/lib/tmpfiles.d/httpd.conf

# Other directories
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/httpd \
         $RPM_BUILD_ROOT/run/httpd/htcacheclean

# Substitute in defaults which are usually done (badly) by "make install"
sed -i \
   "/^DavLockDB/d;
    s,@@ServerRoot@@/user.passwd,/etc/httpd/conf/user.passwd,;
    s,@@ServerRoot@@/docs,%{docroot},;
    s,@@ServerRoot@@,%{docroot},;
    s,@@Port@@,80,;" \
    docs/conf/extra/*.conf

# Set correct path for httpd binary in apachectl script
sed 's,@HTTPDBIN@,%{_sbindir}/httpd,g' $RPM_SOURCE_DIR/apachectl.sh \
    > apachectl.sh

# Create cache directory
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/proxy \
         $RPM_BUILD_ROOT%{_localstatedir}/cache/httpd/ssl

# Make the MMN accessible to module packages
echo %{mmnisa} > $RPM_BUILD_ROOT%{_includedir}/httpd/.mmn
mkdir -p $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d
cat > $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.httpd <<EOF
%%_httpd_mmn %{mmnisa}
%%_httpd_apxs %%{_libdir}/httpd/build/vendor-apxs
%%_httpd_modconfdir %%{_sysconfdir}/httpd/conf.modules.d
%%_httpd_confdir %%{_sysconfdir}/httpd/conf.d
%%_httpd_contentdir %{contentdir}
%%_httpd_moddir %%{_libdir}/httpd/modules
%%_httpd_requires Requires: httpd-mmn = %%{_httpd_mmn}
%%_httpd_statedir %%{_localstatedir}/lib/httpd
EOF

# Handle contentdir
mkdir $RPM_BUILD_ROOT%{contentdir}/noindex \
      $RPM_BUILD_ROOT%{contentdir}/server-status
ln -s ../../testpage/index.html \
      $RPM_BUILD_ROOT%{contentdir}/noindex/index.html
install -m 644 -p docs/server-status/* \
        $RPM_BUILD_ROOT%{contentdir}/server-status
rm -rf %{contentdir}/htdocs

# remove manual sources
find $RPM_BUILD_ROOT%{contentdir}/manual \( \
    -name \*.xml -o -name \*.xml.* -o -name \*.ent -o -name \*.xsl -o -name \*.dtd \
    \) -print0 | xargs -0 rm -f

# Strip the manual down just to English and replace the typemaps with flat files:
set +x
for f in `find $RPM_BUILD_ROOT%{contentdir}/manual -name \*.html -type f`; do
   if test -f ${f}.en; then
      cp ${f}.en ${f}
      rm ${f}.*
   fi
done
set -x

# Clean Document Root
rm -v $RPM_BUILD_ROOT%{docroot}/html/*.html \
      $RPM_BUILD_ROOT%{docroot}/cgi-bin/*

# Symlink for the powered-by-$DISTRO image:
ln -s ../../pixmaps/poweredby.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/poweredby.png

# Symlink for the system logo
%if 0%{?rhel} >= 9
ln -s ../../pixmaps/system-noindex-logo.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/system_noindex_logo.png
%endif

# symlinks for /etc/httpd
rmdir $RPM_BUILD_ROOT/etc/httpd/{state,run}
ln -s ../..%{_localstatedir}/log/httpd $RPM_BUILD_ROOT/etc/httpd/logs
ln -s ../..%{_localstatedir}/lib/httpd $RPM_BUILD_ROOT/etc/httpd/state
ln -s /run/httpd $RPM_BUILD_ROOT/etc/httpd/run
ln -s ../..%{_libdir}/httpd/modules $RPM_BUILD_ROOT/etc/httpd/modules

# install http-ssl-pass-dialog
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m755 $RPM_SOURCE_DIR/httpd-ssl-pass-dialog \
        $RPM_BUILD_ROOT%{_libexecdir}/httpd-ssl-pass-dialog

# install http-ssl-gencerts
install -m755 $RPM_SOURCE_DIR/httpd-ssl-gencerts \
        $RPM_BUILD_ROOT%{_libexecdir}/httpd-ssl-gencerts

# Install scripts
install -m 755 apachectl.sh $RPM_BUILD_ROOT%{_sbindir}/apachectl
touch -r $RPM_SOURCE_DIR/apachectl.sh $RPM_BUILD_ROOT%{_sbindir}/apachectl
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd
for f in graceful configtest; do
    install -p -m 755 $RPM_SOURCE_DIR/action-${f}.sh \
            $RPM_BUILD_ROOT%{_libexecdir}/initscripts/legacy-actions/httpd/${f}
done

# Install logrotate config
mkdir -p $RPM_BUILD_ROOT/etc/logrotate.d
install -m 644 -p $RPM_SOURCE_DIR/httpd.logrotate \
        $RPM_BUILD_ROOT/etc/logrotate.d/httpd

# Install man pages
install -d $RPM_BUILD_ROOT%{_mandir}/man8 $RPM_BUILD_ROOT%{_mandir}/man5
install -m 644 -p httpd.service.8 httpd-init.service.8 httpd.socket.8 \
        httpd@.service.8 htcacheclean.service.8 apachectl.8 \
        $RPM_BUILD_ROOT%{_mandir}/man8
install -m 644 -p httpd.conf.5 \
        $RPM_BUILD_ROOT%{_mandir}/man5

# fix man page paths
sed -e "s|/usr/local/apache2/conf/httpd.conf|/etc/httpd/conf/httpd.conf|" \
    -e "s|/usr/local/apache2/conf/mime.types|/etc/mime.types|" \
    -e "s|/usr/local/apache2/conf/magic|/etc/httpd/conf/magic|" \
    -e "s|/usr/local/apache2/logs/error_log|/var/log/httpd/error_log|" \
    -e "s|/usr/local/apache2/logs/access_log|/var/log/httpd/access_log|" \
    -e "s|/usr/local/apache2/logs/httpd.pid|/run/httpd/httpd.pid|" \
    -e "s|/usr/local/apache2|/etc/httpd|" < docs/man/httpd.8 \
  > $RPM_BUILD_ROOT%{_mandir}/man8/httpd.8

# Make ap_config_layout.h libdir-agnostic
sed -i '/.*DEFAULT_..._LIBEXECDIR/d;/DEFAULT_..._INSTALLBUILDDIR/d' \
    $RPM_BUILD_ROOT%{_includedir}/httpd/ap_config_layout.h

# Fix path to instdso in special.mk
sed -i '/instdso/s,top_srcdir,top_builddir,' \
    $RPM_BUILD_ROOT%{_libdir}/httpd/build/special.mk

# vendor-apxs uses an unsanitized config_vars.mk which may
# have dependencies on redhat-rpm-config.  apxs uses the
# config_vars.mk with a sanitized config_vars.mk
cp -p $RPM_BUILD_ROOT%{_libdir}/httpd/build/config_vars.mk \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor_config_vars.mk

# Sanitize CFLAGS & LIBTOOL in standard config_vars.mk
sed -e '/^[A-Z]*FLAGS = /s,-specs[^ ]*,,g' \
    -e '/^LIBTOOL/s,/.*/libtool,%{_bindir}/libtool,' \
    -i $RPM_BUILD_ROOT%{_libdir}/httpd/build/config_vars.mk
diff -u $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor_config_vars.mk \
     $RPM_BUILD_ROOT%{_libdir}/httpd/build/config_vars.mk || true

sed 's/config_vars.mk/vendor_config_vars.mk/' \
    $RPM_BUILD_ROOT%{_bindir}/apxs \
    > $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs
touch -r $RPM_BUILD_ROOT%{_bindir}/apxs \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs
chmod 755 $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs

# Fix content dir in sysusers file and install it
install -p -D -m 0644 %{SOURCE49} %{buildroot}%{_sysusersdir}/httpd.conf

# Remove unpackaged files
rm -vf \
      $RPM_BUILD_ROOT%{_libdir}/*.exp \
      $RPM_BUILD_ROOT/etc/httpd/conf/mime.types \
      $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.exp \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/config.nice \
      $RPM_BUILD_ROOT%{_bindir}/{ap?-config,dbmmanage} \
      $RPM_BUILD_ROOT%{_sbindir}/{checkgid,envvars*} \
      $RPM_BUILD_ROOT%{contentdir}/htdocs/* \
      $RPM_BUILD_ROOT%{_mandir}/man1/dbmmanage.* \
      $RPM_BUILD_ROOT%{contentdir}/cgi-bin/*

rm -rf $RPM_BUILD_ROOT/etc/httpd/conf/{original,extra}

%pre filesystem
%sysusers_create_compat %{SOURCE49}

%post
%systemd_post httpd.service htcacheclean.service httpd.socket

%preun
%systemd_preun httpd.service htcacheclean.service httpd.socket

%postun
%systemd_postun httpd.service htcacheclean.service httpd.socket

%posttrans
test -f /etc/sysconfig/httpd-disable-posttrans || \
  /bin/systemctl try-restart --no-block httpd.service htcacheclean.service >/dev/null 2>&1 || :

%check
make -C server exports.o
nm --defined httpd > exports-actual.list
set +x
rv=0
nm --defined-only server/exports.o | \
  sed -n '/ap_hack_/{s/.* ap_hack_//;/^ap[ru]/d;p;}' | \
  while read sym; do
    if ! grep -q " "$sym\$ exports-actual.list; then
     echo ERROR: Symbol $sym missing in httpd exports
     rv=1
    fi
  done
if [ $rv -eq 0 ]; then
  echo PASS: Symbol export list verified.
fi
# Check the built modules are all PIC
if readelf -d $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so | grep TEXTREL; then
   echo FAIL: Modules contain non-relocatable code
   rv=1
else
   echo PASS: No non-relocatable code in module builds
fi
# Ensure every mod_* that's built is loaded.
for f in $RPM_BUILD_ROOT%{_libdir}/httpd/modules/*.so; do
  m=${f##*/}
  if ! grep -q $m $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/*.conf; then
    echo FAIL: Module $m not configured.  Disable it, or load it.
    rv=1
   else
    echo PASS: Module $m is configured and loaded.
  fi
done
# Ensure every loaded mod_* is actually built
mods=`grep -h ^LoadModule $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/*.conf | sed 's,.*modules/,,'`
for m in $mods; do
  f=$RPM_BUILD_ROOT%{_libdir}/httpd/modules/${m}
  if ! test -x $f; then
    echo FAIL: Module $m is configured but not built.
    rv=1
  else
    echo PASS: Loaded module $m is installed.
  fi
done
set -x
exit $rv

%files
%{_mandir}/man8/*
%{_mandir}/man5/*
%exclude %{_mandir}/man8/httpd-init.*

%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-brotli.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-systemd.conf
%{_libdir}/httpd/modules/mod_brotli.so
%{_libdir}/httpd/modules/mod_systemd.so

%{_unitdir}/httpd.service
%{_unitdir}/httpd@.service
%{_unitdir}/htcacheclean.service
%{_unitdir}/*.socket

%files core
%doc ABOUT_APACHE README CHANGES LICENSE VERSIONING NOTICE
%doc docs/conf/extra/*.conf
%doc instance.conf server-status.conf

%{_sysconfdir}/httpd/modules
%{_sysconfdir}/httpd/logs
%{_sysconfdir}/httpd/state
%{_sysconfdir}/httpd/run
%dir %{_sysconfdir}/httpd/conf

%config(noreplace) %{_sysconfdir}/httpd/conf/httpd.conf
%config(noreplace) %{_sysconfdir}/httpd/conf/magic

%config(noreplace) %{_sysconfdir}/logrotate.d/httpd

%config(noreplace) %{_sysconfdir}/httpd/conf.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.d/ssl.conf
%exclude %{_sysconfdir}/httpd/conf.d/manual.conf

%dir %{_sysconfdir}/httpd/conf.modules.d
%{_sysconfdir}/httpd/conf.modules.d/README

%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/*.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-brotli.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-systemd.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-lua.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%config(noreplace) %{_sysconfdir}/sysconfig/htcacheclean
%{_prefix}/lib/tmpfiles.d/httpd.conf

%dir %{_libexecdir}/initscripts/legacy-actions/httpd
%{_libexecdir}/initscripts/legacy-actions/httpd/*

%{_sbindir}/httpd
%{_sbindir}/htcacheclean
%{_sbindir}/fcgistarter
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%caps(cap_setuid,cap_setgid+pe) %attr(510,root,%{suexec_caller}) %{_sbindir}/suexec

%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod*.so
%exclude %{_libdir}/httpd/modules/mod_brotli.so
%exclude %{_libdir}/httpd/modules/mod_systemd.so
%exclude %{_libdir}/httpd/modules/mod_auth_form.so
%exclude %{_libdir}/httpd/modules/mod_ssl.so
%exclude %{_libdir}/httpd/modules/mod_*ldap.so
%exclude %{_libdir}/httpd/modules/mod_proxy_html.so
%exclude %{_libdir}/httpd/modules/mod_xml2enc.so
%exclude %{_libdir}/httpd/modules/mod_session*.so
%exclude %{_libdir}/httpd/modules/mod_lua.so

%dir %{contentdir}/error
%dir %{contentdir}/error/include
%dir %{contentdir}/noindex
%dir %{contentdir}/server-status
%{contentdir}/icons/*
%{contentdir}/error/README
%{contentdir}/error/*.var
%{contentdir}/error/include/*.html
%{contentdir}/noindex/index.html
%{contentdir}/server-status/*

%attr(0710,root,apache) %dir /run/httpd
%attr(0700,apache,apache) %dir /run/httpd/htcacheclean
%attr(0700,root,root) %dir %{_localstatedir}/log/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/lib/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd
%attr(0700,apache,apache) %dir %{_localstatedir}/cache/httpd/proxy


%files filesystem
%dir %{_sysconfdir}/httpd
%dir %{_sysconfdir}/httpd/conf.d
%{_sysconfdir}/httpd/conf.d/README
%dir %{docroot}
%dir %{docroot}/cgi-bin
%dir %{docroot}/html
%dir %{contentdir}
%dir %{contentdir}/icons
%attr(755,root,root) %dir %{_unitdir}/httpd.service.d
%attr(755,root,root) %dir %{_unitdir}/httpd.socket.d
%attr(755,root,root) %dir %{_sysconfdir}/systemd/system/httpd.service.d
%{_sysusersdir}/httpd.conf

%files tools
%{_bindir}/ab
%{_bindir}/htdbm
%{_bindir}/htdigest
%{_bindir}/httxt2dbm
%{_bindir}/htpasswd
%{_bindir}/logresolve
%{_mandir}/man1/*
%doc LICENSE NOTICE
%exclude %{_bindir}/apxs
%exclude %{_mandir}/man1/apxs.1*

%files manual
%{contentdir}/manual
%config(noreplace) %{_sysconfdir}/httpd/conf.d/manual.conf

%files -n mod_ssl
%{_libdir}/httpd/modules/mod_ssl.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%config(noreplace) %{_sysconfdir}/httpd/conf.d/ssl.conf
%attr(0700,apache,root) %dir %{_localstatedir}/cache/httpd/ssl
%{_unitdir}/httpd-init.service
%{_libexecdir}/httpd-ssl-pass-dialog
%{_libexecdir}/httpd-ssl-gencerts
%{_unitdir}/httpd.socket.d/10-listen443.conf
%{_mandir}/man8/httpd-init.*

%files -n mod_proxy_html
%{_libdir}/httpd/modules/mod_proxy_html.so
%{_libdir}/httpd/modules/mod_xml2enc.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf

%files -n mod_ldap
%{_libdir}/httpd/modules/mod_*ldap.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf

%files -n mod_session
%{_libdir}/httpd/modules/mod_session*.so
%{_libdir}/httpd/modules/mod_auth_form.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/01-session.conf

%files -n mod_lua
%{_libdir}/httpd/modules/mod_lua.so
%config(noreplace) %{_sysconfdir}/httpd/conf.modules.d/00-lua.conf

%files devel
%{_includedir}/httpd
%{_bindir}/apxs
%{_mandir}/man1/apxs.1*
%dir %{_libdir}/httpd/build
%{_libdir}/httpd/build/*.mk
%{_libdir}/httpd/build/*.sh
%{_libdir}/httpd/build/vendor-apxs
%{_rpmconfigdir}/macros.d/macros.httpd

%changelog
* Tue Dec 09 2025 Luboš Uhliarik <luhliari@redhat.com> - 2.4.66-1
- new version 2.4.66

* Wed Nov 12 2025 Luboš Uhliarik <luhliari@redhat.com> - 2.4.65-3
- mod_ssl: SSLVHostSNIPolicy - Fix handling of STRICT mode

* Tue Nov 04 2025 Luboš Uhliarik <luhliari@redhat.com> - 2.4.65-2
- mod_ssl: Add SSLVHostSNIPolicy directive to set the compatibility level
  required for VirtualHost matching.

* Sat Oct 18 2025 Luboš Uhliarik <luhliari@redhat.com> - 2.4.65-1
- new version 2.4.65
- mod_proxy_hcheck: reschedule health checks after child process restart

* Mon Sep 08 2025 Luboš Uhliarik <luhliari@redhat.com> - 2.4.64-4
- Add tmpfiles.d rules for /var directories (bootc compatibility)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Luboš Uhliarik <luhliari@redhat.com> - 2.4.64-2
- Fix RewriteRule with inverted pattern and RewriteCond regression

* Fri Jul 11 2025 Luboš Uhliarik <luhliari@redhat.com> - 2.4.64-1
- new version 2.4.64

* Tue Jun 24 2025 Joe Orton  <jorton@redhat.com> - 2.4.63-4
- mod_dav: add dav_get_base_path() API

* Mon Feb 10 2025 Joe Orton <jorton@redhat.com> - 2.4.63-3
- sync default httpd.conf with upstream

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 2.4.63-2
- Add explicit BR: libxcrypt-devel

* Fri Jan 24 2025 Luboš Uhliarik <luhliari@redhat.com> - 2.4.63-1
- new version 2.4.63

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.62-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.62-5
- Rebuilt for the bin-sbin merge (2nd attempt)

* Fri Oct 11 2024 Luboš Uhliarik <luhliari@redhat.com> - 2.4.62-4
- mod_rewrite: regression fixes

* Thu Aug 01 2024 Luboš Uhliarik <luhliari@redhat.com> - 2.4.62-3
- Fix regression introduced by CVE-2024-38474 fix
- added openldap-devel build dependency

* Fri Jul 19 2024 Luboš Uhliarik <luhliari@redhat.com> - 2.4.62-1
- new version 2.4.62

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.61-2
- Rebuilt for the bin-sbin merge

* Wed Jul 03 2024 Luboš Uhliarik <luhliari@redhat.com> - 2.4.61-1
- new version 2.4.61

* Thu May 23 2024 Joe Orton <jorton@redhat.com> - 2.4.59-4
- mod_ssl: add engine bcond, disable ENGINE support by default for F41+
- mod_ssl: enable SSL_OP_NO_RENEGOTIATION (upstream PR#426)

* Fri May  3 2024 Joe Orton <jorton@redhat.com> - 2.4.59-3
- apachectl(8): use BUG_REPORT_URL from /etc/os-release
- apachectl(8): fix grammar (#2278748)
- httpd.service.xml(8): mention ProtectSystem= setting

* Mon Apr 15 2024 Joe Orton <jorton@redhat.com> - 2.4.59-2
- mod_ssl: add DH param handling fix (r1916863)

* Fri Apr  5 2024 Joe Orton <jorton@redhat.com> - 2.4.59-1
- update to 2.4.59

* Thu Mar 28 2024 Joe Orton <jorton@redhat.com> - 2.4.58-8
- rebuild to fix changelog ordering

* Thu Mar 7 2024 Rahul Sundaram <sundaram@fedoraproject.org> - 2.4.58-7
- Update Systemd security settings as part of https://fedoraproject.org/wiki/Changes/SystemdSecurityHardening
- updated httpd.service(5) (Joe Orton)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.58-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.58-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan  5 2024 Joe Orton <jorton@redhat.com> - 2.4.58-4
- fix OpenSSL 3.0 deprecation warnings (r1913912, r1915067)
- mod_ssl: move to provider API for pkcs11 support (#2253014)

* Fri Dec  8 2023 Joe Orton <jorton@redhat.com> - 2.4.58-3
- mod_dav_fs: add DAVLockDBType, use global lock around lockdb
- fix build with libxml2 2.12

* Thu Nov  2 2023 Joe Orton <jorton@redhat.com> - 2.4.58-2
- add dependency on apr-util-1(dbm) so a DBM provider is present

* Fri Oct 20 2023 Luboš Uhliarik <luhliari@redhat.com> - 2.4.58-1
- new version 2.4.58

* Fri Oct 06 2023 Luboš Uhliarik <luhliari@redhat.com> - 2.4.57-4
- SPDX migration

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul  5 2023 Joe Orton <jorton@redhat.com> - 2.4.57-2
- package /etc/systemd/httpd/httpd.service.d
- also sanitize LDFLAGS/CXXFLAGS in non-vendor config_vars.mk

* Tue Apr 11 2023 Luboš Uhliarik <luhliari@redhat.com> - 2.4.57-1
- new version 2.4.57

* Thu Mar 09 2023 Luboš Uhliarik <luhliari@redhat.com> - 2.4.56-1
- new version 2.4.56

* Tue Mar  7 2023 Joe Orton <jorton@redhat.com> - 2.4.55-3
- build and load mod_authnz_fcgi

* Fri Feb 03 2023 Luboš Uhliarik <luhliari@redhat.com> - 2.4.55-2
- rebuilt with new apr/apr-util

* Wed Jan 25 2023 Luboš Uhliarik <luhliari@redhat.com> - 2.4.55-1
- new version 2.4.55

* Tue Jan 24 2023 Luboš Uhliarik <luhliari@redhat.com> - 2.4.54-12
- prevent sscg writing /dhparams.pem

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.54-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 20 2022 Joe Orton <jorton@redhat.com> - 2.4.54-10
- htcacheclean.service: add [Install] section, PrivateTmp=yes,
  Environment=LANG=C (#2149714)

* Mon Dec 19 2022 Joe Orton <jorton@redhat.com> - 2.4.54-9
- move SELinux context logging to mod_systemd

* Mon Dec 19 2022 Joe Orton <jorton@redhat.com> - 2.4.54-8
- define _httpd_statedir macro

* Wed Nov 30 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.54-7
- reduce AH03408 level to INFO in proxy_util.c

* Thu Oct 13 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.54-6
- Provide a sysusers.d file to get user() and group() provides (#2134430)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.54-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.54-4
- fix downgrade/upgrade issues
- mod_ssl and other modules should depend only on httpd-core package

* Fri Jun 17 2022 Joe Orton <jorton@redhat.com> - 2.4.54-3
- update PCRE config selection

* Thu Jun 09 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.54-2
- new version 2.4.54

* Mon May 16 2022 Joe Orton <jorton@redhat.com> - 2.4.53-7
- disable package notes

* Fri May 13 2022 Joe Orton <jorton@redhat.com> - 2.4.53-6
- use %%set_build_flags macro

* Thu Apr 21 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.53-5
- don't use bomb.gif icon for all files/dirs ending with core

* Wed Apr 20 2022 Joe Orton <jorton@redhat.com> - 2.4.53-4
- switch to PCRE2 for new releases

* Thu Apr 07 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.53-3
- Related: #2070517 - fix issue when mod_systemd is not loaded

* Wed Mar 30 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.53-2
- Resolves: #2070517 - Allow install httpd with smaller footprint
- try to minimize httpd dependencies (new httpd-core package)
- mod_systemd and mod_brotli are now in the main httpd package

* Thu Mar 17 2022 Luboš Uhliarik <luhliari@redhat.com> - 2.4.53-1
- new version 2.4.53
- fixes CVE-2022-23943, CVE-2022-22721, CVE-2022-22720 and CVE-2022-22719

* Tue Feb  1 2022 Joe Orton <jorton@redhat.com> - 2.4.52-5
- rebuild for new OpenLDAP (#2032699)

* Mon Jan 31 2022 Joe Orton <jorton@redhat.com> - 2.4.52-4
- add libtool to Requires: for httpd-devel (#2048281)

* Fri Jan 28 2022 Joe Orton <jorton@redhat.com> - 2.4.52-3
- use LIBTOOL=/usr/bin/libtool in the non-vendor config_vars.mk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Joe Orton <jorton@redhat.com> - 2.4.52-1
- update to 2.4.52

* Mon Dec 06 2021 Neal Gompa <ngompa@fedoraproject.org> - 2.4.51-3
- Use NAME from os-release(5) for vendor string
  Related: #2029071 - httpd on CentOS identifies as RHEL

* Tue Oct 12 2021 Joe Orton <jorton@redhat.com> - 2.4.51-2
- mod_ssl: updated patch for OpenSSL 3.0 compatibility (#2007178)
- mod_deflate/core: add two brigade handling correctness fixes

* Thu Oct 07 2021 Patrick Uiterwijk <patrick@puiterwijk.org> - 2.4.51-1
- new version 2.4.51

* Tue Oct 05 2021 Luboš Uhliarik <luhliari@redhat.com> - 2.4.50-1
- new version 2.4.50

* Wed Sep 22 2021 Luboš Uhliarik <luhliari@redhat.com> - 2.4.49-3
- Rebuilt for CI testing

* Thu Sep 16 2021 Luboš Uhliarik <luhliari@redhat.com> - 2.4.49-1
- new version 2.4.49 (#2004776)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.4.48-8
- Rebuilt with OpenSSL 3.0.0

* Fri Aug 06 2021 Luboš Uhliarik <luhliari@redhat.com> - 2.4.48-7
- add symlink to system logo for noindex test page

* Fri Aug  6 2021 Joe Orton <jorton@redhat.com> - 2.4.48-4
- add OpenSSL 3.x compatibility patch

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.48-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 16 2021 Joe Orton <jorton@redhat.com> - 2.4.48-2
- mod_cgi/mod_cgid: update to unification from trunk
- httpd.conf: add note on care with Listen and starting at boot

* Wed Jun 02 2021 Luboš Uhliarik <luhliari@redhat.com> - 2.4.48-1
- new version 2.4.48
- Resolves: #1964746 - httpd-2.4.48 is available

* Mon May 03 2021 Lubos Uhliarik <luhliari@redhat.com> - 2.4.46-13
- Related: #1934739 - Apache trademark update - new logo

* Fri Apr  9 2021 Joe Orton <jorton@redhat.com> - 2.4.46-12
- use OOMPolicy=continue in httpd.service, httpd@.service (#1947475)

* Wed Mar 31 2021 Lubos Uhliarik <luhliari@redhat.com> - 2.4.46-11
- Resolves: #1934739 - Apache trademark update - new logo

* Tue Feb 23 2021 Joe Orton <jorton@redhat.com> - 2.4.46-10
- add Conflicts: with mod_nss
- drop use of apr_ldap_rebind (r1878890, #1847585)

* Mon Feb 01 2021 Lubos Uhliarik <luhliari@redhat.com> - 2.4.46-9
- Resolves: #1914182 - RFE: CustomLog should be able to use journald

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.46-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Artem Egorenkov <aegorenk@redhat.com> - 2.4.46-7
- prevent htcacheclean from while break when first file processed

* Thu Dec 17 2020 Joe Orton <jorton@redhat.com> - 2.4.46-6
- move mod_lua to a subpackage
- Recommends: both mod_lua and mod_http2

* Fri Nov  6 2020 Joe Orton <jorton@redhat.com> - 2.4.46-5
- add %%_httpd_requires to macros

* Thu Aug 27 2020 Joe Orton <jorton@redhat.com> - 2.4.46-4
- use make macros (Tom Stellard)

* Thu Aug 27 2020 Joe Orton <jorton@redhat.com> - 2.4.46-3
- strip /usr/bin/apxs CFLAGS further

* Thu Aug 27 2020 Joe Orton <jorton@redhat.com> - 2.4.46-2
- sanitize CFLAGS used by /usr/bin/apxs by default (#1873020)
- add $libdir/httpd/build/vendor-apxs which exposes full CFLAGS
- redefine _httpd_apxs RPM macro to use vendor-apxs

* Tue Aug 25 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.46-1
- new version 2.4.46
- remove obsolete parts of this spec file
- fix systemd detection patch

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.43-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 09 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.43-6
- fix macro in mod_lua for lua 4.5

* Thu Jul 09 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.43-5
- Remove %ghosted /etc/sysconfig/httpd file (#1850082)

* Tue Jul  7 2020 Joe Orton <jorton@redhat.com> - 2.4.43-4
- use gettid() directly and use it for built-in ErrorLogFormat

* Fri Apr 17 2020 Joe Orton <jorton@redhat.com> - 2.4.43-3
- mod_ssl: updated coalescing filter to improve TLS efficiency

* Fri Apr 17 2020 Joe Orton <jorton@redhat.com> - 2.4.43-2
- mod_ssl: fix leak in OCSP stapling code (PR 63687, r1876548)
- mod_systemd: restore descriptive startup logging

* Tue Mar 31 2020 Lubos Uhliarik <luhliari@redhat.com> - 2.4.43-1
- new version 2.4.43 (#1819023)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.41-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Joe Orton <jorton@redhat.com> - 2.4.41-12
- mod_systemd: fix timeouts on reload w/ExtendedStatus off (#1590877)

* Mon Jan  6 2020 Joe Orton <jorton@redhat.com> - 2.4.41-11
- apachectl(8): update authors

* Sat Dec  7 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 2.4.41-10
- apachectl: Add man page for Fedora version

* Thu Nov 21 2019 Joe Orton <jorton@redhat.com> - 2.4.41-9
- mod_ssl: fix request body buffering w/TLSv1.3 PHA (#1775146)

* Wed Nov 13 2019 Joe Orton <jorton@redhat.com> - 2.4.41-8
- apachectl: in graceful/graceful-stop, only signal main process (#1758798)

* Mon Nov 11 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.41-7
- add automatic source tarball signature verification in %prep section

* Fri Oct  4 2019 Joe Orton <jorton@redhat.com> - 2.4.41-6
- mod_cgid/mod_cgi: further upstream consolidation patches

* Thu Oct  3 2019 Joe Orton <jorton@redhat.com> - 2.4.41-5
- mod_proxy_balancer: fix balancer-manager XSRF check (PR 63688)

* Wed Oct  2 2019 Joe Orton <jorton@redhat.com> - 2.4.41-4
- mod_cgid: possible stdout timeout handling fix (#1757683)

* Wed Sep 25 2019 Joe Orton <jorton@redhat.com> - 2.4.41-3
- mod_ssl: restore dependency on /usr/bin/hostname (#1135118)

* Thu Sep 19 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.4.41-2
- Use testpage from system-logos-httpd for proper branding

* Thu Aug 15 2019 Joe Orton <jorton@redhat.com> - 2.4.41-1
- update to 2.4.41

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.39-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Joe Orton <jorton@redhat.com> - 2.4.39-12
- drop /var/lib/dav directory, since mod_dav_fs uses statedir

* Wed Jul 17 2019 Joe Orton <jorton@redhat.com> - 2.4.39-11
- mod_cgid: use fd passing to fix script stderr handling (#1591157)

* Mon Jul  8 2019 Joe Orton <jorton@redhat.com> - 2.4.39-10
- htpasswd: add SHA-256/512 support
- apachectl: restore -V/-v/-t support (#1727434)

* Fri Jun 21 2019 Joe Orton <jorton@redhat.com> - 2.4.39-9
- create instance-specific StateDir in httpd@.service, instance.conf

* Thu Jun 20 2019 Joe Orton <jorton@redhat.com> - 2.4.39-8
- remove superfluous ap_hack_ symbols from httpd binary
- more verbose %%check section

* Thu Jun 13 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.39-7
- remove bundled mod_md module

* Thu Jun 13 2019 Joe Orton <jorton@redhat.com> - 2.4.39-6
- mod_ssl: fix "httpd -L" (etc) before httpd-init.service runs

* Wed Jun 12 2019 Joe Orton <jorton@redhat.com> - 2.4.39-5
- fixes for StateDir directive (upstream r1857731, r1857731)

* Thu May 02 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.39-4
- httpd dependency on initscripts is unspecified (#1705188)

* Tue Apr  9 2019 Joe Orton <jorton@redhat.com> - 2.4.39-3
- fix statedir symlink to point to /var/lib/httpd (#1697662)
- mod_reqtimeout: fix default values regression (PR 63325)

* Tue Apr 02 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.39-2
- update to 2.4.39

* Thu Feb 28 2019 Joe Orton <jorton@redhat.com> - 2.4.38-6
- apachectl: cleanup and replace script wholesale (#1641237)
 * drop "apachectl fullstatus" support
 * run systemctl with --no-pager option
 * implement graceful&graceful-stop by signal directly
- run "httpd -t" from legacy action script

* Tue Feb 05 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.38-5
- segmentation fault fix (FIPS)

* Tue Feb  5 2019 Joe Orton <jorton@redhat.com> - 2.4.38-4
- use serverroot-relative statedir, rundir by default

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.4.38-2
- new version 2.4.38 (#1668125)

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.4.37-6
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Nov 22 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.37-5
- Resolves: #1652678 - TLS connection allowed while all protocols are forbidden

* Thu Nov  8 2018 Joe Orton <jorton@redhat.com> - 2.4.37-4
- add httpd.conf(5) (#1611361)

* Wed Nov 07 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.37-3
- Resolves: #1647241 - fix apachectl script

* Wed Oct 31 2018 Joe Orton <jorton@redhat.com> - 2.4.37-2
- add DefaultStateDir/ap_state_dir_relative()
- mod_dav_fs: use state dir for default DAVLockDB
- mod_md: use state dir for default MDStoreDir

* Wed Oct 31 2018 Joe Orton <jorton@redhat.com> - 2.4.37-1
- update to 2.4.37

* Wed Oct 31 2018 Joe Orton <jorton@redhat.com> - 2.4.34-11
- add htcacheclean.service(8) man page

* Fri Sep 28 2018 Joe Orton <jorton@redhat.com> - 2.4.34-10
- apachectl: don't read /etc/sysconfig/httpd

* Tue Sep 25 2018 Joe Orton <jorton@redhat.com> - 2.4.34-9
- fix build if OpenSSL built w/o SSLv3 support

* Fri Sep 21 2018 Joe Orton <jorton@redhat.com> - 2.4.34-8
- comment-out SSLProtocol, SSLProxyProtocol from ssl.conf in
  default configuration; now follow OpenSSL system default (#1468322)

* Fri Sep 21 2018 Joe Orton <jorton@redhat.com> - 2.4.34-7
- mod_ssl: follow OpenSSL protocol defaults if SSLProtocol
  is not configured (Rob Crittenden, #1618371)

* Tue Aug 28 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.4.34-6
- mod_ssl: enable SSLv3 and change behavior of "SSLProtocol All"
  configuration (#1624777)

* Tue Aug 21 2018 Joe Orton <jorton@redhat.com> - 2.4.34-5
- mod_ssl: further TLSv1.3 fix (#1619389)

* Mon Aug 13 2018 Joe Orton <jorton@redhat.com> - 2.4.34-4
- mod_ssl: backport TLSv1.3 support changes from upstream (#1615059)

* Fri Jul 20 2018 Joe Orton <jorton@redhat.com> - 2.4.34-3
- mod_ssl: fix OCSP regression (upstream r1555631)

* Wed Jul 18 2018 Joe Orton <jorton@redhat.com> - 2.4.34-2
- update Obsoletes for mod_proxy_uswgi (#1599113)

* Wed Jul 18 2018 Joe Orton <jorton@redhat.com> - 2.4.34-1
- update to 2.4.34 (#1601160)

* Mon Jul 16 2018 Joe Orton <jorton@redhat.com> - 2.4.33-10
- don't block on service try-restart in posttrans scriptlet
- add Lua-based /server-status example page to docs
- obsoletes: and provides: for mod_proxy_uswgi (#1599113)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.33-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul  6 2018 Joe Orton <jorton@redhat.com> - 2.4.33-8
- add per-request memory leak fix (upstream r1833014)

* Fri Jul  6 2018 Joe Orton <jorton@redhat.com> - 2.4.33-7
- mod_ssl: add PKCS#11 cert/key support (Anderson Sasaki)

* Tue Jun 12 2018 Joe Orton <jorton@redhat.com> - 2.4.33-6
- mod_systemd: show bound ports in status and log to journal
  at startup.

* Thu Apr 19 2018 Joe Orton <jorton@redhat.com> - 2.4.33-5
- add httpd@.service; update httpd.service(8) and add new stub

* Mon Apr 16 2018 Joe Orton <jorton@redhat.com> - 2.4.33-4
- mod_md: change hard-coded default MdStoreDir to state/md (#1563846)

* Thu Apr 12 2018 Joe Orton <jorton@redhat.com> - 2.4.33-3
- mod_ssl: drop implicit 'SSLEngine on' for vhost w/o certs (#1564537)

* Fri Mar 30 2018 Adam Williamson <awilliam@redhat.com> - 2.4.33-2
- Exclude mod_md config file from main package (#1562413)

* Wed Mar 28 2018 Joe Orton <jorton@redhat.com> - 2.4.33-1
- rebase to 2.4.33 (#1560174)
- add mod_md subpackage; load mod_proxy_uwsgi by default

* Mon Mar 05 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.29-8
- Rebuilt with brotli 1.0.3

* Mon Feb 26 2018 Joe Orton <jorton@redhat.com> - 2.4.29-7
- simplify liblua detection in configure

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Joe Orton <jorton@redhat.com> - 2.4.29-5
- link mod_lua against -lcrypt (#1538992)

* Fri Jan 26 2018 Paul Howarth <paul@city-fan.org> - 2.4.29-4
- Rebuild with updated flags to work around compiler issues on i686
  (#1538648, #1538693)

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.4.29-3
- Rebuilt for switch to libxcrypt

* Thu Nov 23 2017 Joe Orton <jorton@redhat.com> - 2.4.29-2
- build and load mod_brotli

* Wed Oct 25 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.29-1
- new version 2.4.29

* Tue Oct 10 2017 Joe Orton <jorton@redhat.com> - 2.4.28-3
- drop obsolete Obsoletes
- update docs, Summary
- trim %%changelog

* Tue Oct 10 2017 Patrick Uiterwijk <patrick@puiterwijk.org> - 2.4.28-2
- Backport patch for fixing ticket key usage

* Fri Oct 06 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.28-1
- new version 2.4.28

* Tue Oct  3 2017 Joe Orton <jorton@redhat.com> - 2.4.27-14
- add notes on enabling httpd_graceful_shutdown boolean for prefork

* Fri Sep 22 2017 Joe Orton <jorton@redhat.com> - 2.4.27-13
- drop Requires(post) for mod_ssl

* Fri Sep 22 2017 Joe Orton <jorton@redhat.com> - 2.4.27-12
- better error handling in httpd-ssl-gencerts (#1494556)

* Thu Sep 21 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.4.27-11
- Require sscg 2.2.0 for creating service and CA certificates together

* Thu Sep 21 2017 Jeroen van Meeuwen <kanarip@fedoraproject.org> - 2.4.27-10
- Address CVE-2017-9798 by applying patch from upstream (#1490344)

* Thu Sep 21 2017 Joe Orton <jorton@redhat.com> - 2.4.27-9
- use sscg defaults; append CA cert to generated cert
- document httpd-init.service in httpd-init.service(8)

* Wed Sep 20 2017 Stephen Gallagher <sgallagh@redhat.com> - 2.4.27-8.1
- Generate SSL certificates on service start, not %%posttrans

* Tue Sep 19 2017 Joe Orton <jorton@redhat.com> - 2.4.27-8
- move httpd.service.d, httpd.socket.d dirs to -filesystem

* Wed Sep 13 2017 Joe Orton <jorton@redhat.com> - 2.4.27-7
- add new content-length filter (upstream PR 61222)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Joe Orton <jorton@redhat.com> - 2.4.27-4
- update mod_systemd (r1802251)

* Mon Jul 17 2017 Joe Orton <jorton@redhat.com> - 2.4.27-3
- switch to event by default for Fedora 27 and later (#1471708)

* Wed Jul 12 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.27-2
- Resolves: #1469959 - httpd update cleaned out /etc/sysconfig

* Mon Jul 10 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.27-1
- new version 2.4.27

* Fri Jun 30 2017 Joe Orton <jorton@redhat.com> - 2.4.26-2
- mod_proxy_fcgi: fix further regressions (PR 61202)

* Mon Jun 19 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.26-1
- new version 2.4.26

* Mon Jun  5 2017 Joe Orton <jorton@redhat.com> - 2.4.25-10
- move unit man pages to section 8, add as Documentation= in units

* Fri May 19 2017 Joe Orton <jorton@redhat.com> - 2.4.25-9
- add httpd.service(5) and httpd.socket(5) man pages

* Tue May 16 2017 Joe Orton <jorton@redhat.com> - 2.4.25-8
- require mod_http2, now packaged separately

* Wed Mar 29 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.25-7
- Resolves: #1397243 - Backport Apache Bug 53098 - mod_proxy_ajp:
  patch to set worker secret passed to tomcat

* Tue Mar 28 2017 Luboš Uhliarik <luhliari@redhat.com> - 2.4.25-6
- Resolves: #1434916 - httpd.service: Failed with result timeout

* Fri Mar 24 2017 Joe Orton <jorton@redhat.com> - 2.4.25-5
- link only httpd, not support/* against -lselinux -lsystemd

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Joe Orton <jorton@redhat.com> - 2.4.25-3
- mod_watchdog: restrict thread lifetime (#1410883)

* Thu Dec 22 2016 Luboš Uhliarik <luhliari@redhat.com> - 2.4.25-2
- Resolves: #1358875 - require nghttp2 >= 1.5.0

* Thu Dec 22 2016 Luboš Uhliarik <luhliari@redhat.com> - 2.4.25-1
- new version 2.4.25

* Mon Dec 05 2016 Luboš Uhliarik <luhliari@redhat.com> - 2.4.23-7
- Resolves: #1401530 - CVE-2016-8740 httpd: Incomplete handling of
  LimitRequestFields directive in mod_http2

* Mon Nov 14 2016 Joe Orton <jorton@redhat.com> - 2.4.23-6
- fix build with OpenSSL 1.1 (#1392900)
- fix typos in ssl.conf (josef randinger, #1379407)

* Wed Nov  2 2016 Joe Orton <jorton@redhat.com> - 2.4.23-5
- no longer package /etc/sysconfig/httpd
- synch ssl.conf with upstream

* Mon Jul 18 2016 Joe Orton <jorton@redhat.com> - 2.4.23-4
- add security fix for CVE-2016-5387

* Thu Jul  7 2016 Joe Orton <jorton@redhat.com> - 2.4.23-3
- load mod_watchdog by default (#1353582)

* Thu Jul  7 2016 Joe Orton <jorton@redhat.com> - 2.4.23-2
- restore build of mod_proxy_fdpass (#1325883)
- improve check tests to catch configured-but-not-built modules

* Thu Jul  7 2016 Joe Orton <jorton@redhat.com> - 2.4.23-1
- update to 2.4.23 (#1325883, #1353203)
- load mod_proxy_hcheck
- recommend use of "systemctl edit" in httpd.service

* Thu Apr  7 2016 Joe Orton <jorton@redhat.com> - 2.4.18-6
- have "apachectl graceful" start httpd if not running, per man page

* Wed Apr  6 2016 Joe Orton <jorton@redhat.com> - 2.4.18-5
- use redirects for lang-specific /manual/ URLs

* Fri Mar 18 2016 Joe Orton <jorton@redhat.com> - 2.4.18-4
- fix welcome page HTML validity (Ville Skyttä)

* Fri Mar 18 2016 Joe Orton <jorton@redhat.com> - 2.4.18-3
- remove httpd pre script (duplicate of httpd-filesystem's)
- in httpd-filesystem pre script, create group/user iff non-existent

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.18-1
- update to new version 2.4.18

* Wed Dec  9 2015 Joe Orton <jorton@redhat.com> - 2.4.17-4
- re-enable mod_asis due to popular demand (#1284315)

* Mon Oct 26 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.17-3
- fix crash when using -X argument (#1272234)

* Wed Oct 14 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.17-2
- rebase socket activation patch to 2.4.17

* Tue Oct 13 2015 Joe Orton <jorton@redhat.com> - 2.4.17-1
- update to 2.4.17 (#1271224)
- build, load mod_http2
- don't build mod_asis, mod_file_cache
- load mod_cache_socache, mod_proxy_wstunnel by default
- check every built mod_* is configured
- synch ssl.conf with upstream; disable SSLv3 by default

* Wed Jul 15 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.12-4
- update to 2.4.16

* Tue Jul  7 2015 Joe Orton <jorton@redhat.com> - 2.4.12-3
- mod_ssl: use "localhost" in the dummy SSL cert if len(FQDN) > 59 chars

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.12-1
- update to 2.4.12

* Tue Mar 24 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-17
- fix compilation with lua-5.3

* Tue Mar 24 2015 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-16
- remove filter for auto-provides of httpd modules, it is not needed since F20

* Wed Dec 17 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-15
- core: fix bypassing of mod_headers rules via chunked requests (CVE-2013-5704)
- mod_cache: fix NULL pointer dereference on empty Content-Type (CVE-2014-3581)
- mod_proxy_fcgi: fix a potential crash with long headers (CVE-2014-3583)
- mod_lua: fix handling of the Require line when a LuaAuthzProvider is used
  in multiple Require directives with different arguments (CVE-2014-8109)

* Tue Oct 14 2014 Joe Orton <jorton@redhat.com> - 2.4.10-14
- require apr-util 1.5.x

* Thu Sep 18 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-13
- use NoDelay and DeferAcceptSec in httpd.socket

* Mon Sep 08 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-12
- increase suexec minimum acceptable uid/gid to 1000 (#1136391)

* Wed Sep 03 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-11
- fix hostname requirement and conflict with openssl-libs

* Mon Sep 01 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-10
- use KillMode=mixed in httpd.service (#1135122)

* Fri Aug 29 2014 Joe Orton <jorton@redhat.com> - 2.4.10-9
- set vstring based on /etc/os-release (Pat Riehecky, #1114539)

* Fri Aug 29 2014 Joe Orton <jorton@redhat.com> - 2.4.10-8
- pull in httpd-filesystem as Requires(pre) (#1128328)
- fix cipher selection in default ssl.conf, depend on new OpenSSL (#1134348)
- require hostname for mod_ssl post script (#1135118)

* Fri Aug 22 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-7
- mod_systemd: updated to the latest version
- use -lsystemd instead of -lsystemd-daemon (#1125084)
- fix possible crash in SIGINT handling (#958934)

* Thu Aug 21 2014 Joe Orton <jorton@redhat.com> - 2.4.10-6
- mod_ssl: treat "SSLCipherSuite PROFILE=..." as special (#1109119)
- switch default ssl.conf to use PROFILE=SYSTEM (#1109119)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-4
- add /usr/bin/useradd dependency to -filesystem requires

* Thu Aug 14 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.10-3
- fix creating apache user in pre script (#1128328)

* Thu Jul 31 2014 Joe Orton <jorton@redhat.com> - 2.4.10-2
- enable mod_request by default for mod_auth_form
- move disabled-by-default modules from 00-base.conf to 00-optional.conf

* Mon Jul 21 2014 Joe Orton <jorton@redhat.com> - 2.4.10-1
- update to 2.4.10
- expand variables in docdir example configs

* Tue Jul 08 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-8
- add support for systemd socket activation (#1111648)

* Mon Jul 07 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-7
- remove conf.modules.d from httpd-filesystem subpackage (#1081453)

* Mon Jul 07 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-6
- add httpd-filesystem subpackage (#1081453)

* Fri Jun 20 2014 Joe Orton <jorton@redhat.com> - 2.4.9-5
- mod_ssl: don't use the default OpenSSL cipher suite in ssl.conf (#1109119)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-3
- add support for SetHandler + proxy (#1078970)

* Thu Mar 27 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-2
- move macros from /etc/rpm to macros.d (#1074277)
- remove unused patches

* Mon Mar 17 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.9-1
- update to 2.4.9

* Fri Feb 28 2014 Joe Orton <jorton@redhat.com> - 2.4.7-6
- use 2048-bit RSA key with SHA-256 signature in dummy certificate

* Fri Feb 28 2014 Stephen Gallagher <sgallagh@redhat.com> 2.4.7-5
- Create drop directory for systemd snippets

* Thu Feb 27 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.7-4
- remove provides of old MMN, because it contained double-dash (#1068851)

* Thu Feb 20 2014 Jan Kaluza <jkaluza@redhat.com> - 2.4.7-3
- fix graceful restart using legacy actions

* Thu Dec 12 2013 Joe Orton <jorton@redhat.com> - 2.4.7-2
- conflict with pre-1.5.0 APR
- fix sslsninotreq patch

* Wed Nov 27 2013 Joe Orton <jorton@redhat.com> - 2.4.7-1
- update to 2.4.7 (#1034071)

* Fri Nov 22 2013 Joe Orton <jorton@redhat.com> - 2.4.6-10
- switch to requiring system-logos-httpd (#1031288)

* Tue Nov 12 2013 Joe Orton <jorton@redhat.com> - 2.4.6-9
- change mmnisa to drop "-" altogether

* Tue Nov 12 2013 Joe Orton <jorton@redhat.com> - 2.4.6-8
- drop ambiguous invalid "-" in RHS of httpd-mmn Provide, keeping old Provide
  for transition

* Fri Nov  1 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-7
- systemd: use {MAINPID} notation to ensure /bin/kill has always the second arg

* Thu Oct 31 2013 Joe Orton <jorton@redhat.com> - 2.4.6-6
- mod_ssl: allow SSLEngine to override Listen-based default (r1537535)

* Thu Oct 24 2013 Jan kaluza <jkaluza@redhat.com> - 2.4.6-5
- systemd: send SIGWINCH signal without httpd -k in ExecStop

* Mon Oct 21 2013 Joe Orton <jorton@redhat.com> - 2.4.6-4
- load mod_macro by default (#998452)
- add README to conf.modules.d
- mod_proxy_http: add possible fix for threading issues (r1534321)
- core: add fix for truncated output with CGI scripts (r1530793)

* Thu Oct 10 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-3
- require fedora-logos-httpd (#1009162)

* Wed Jul 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.6-2
- revert fix for dumping vhosts twice

* Mon Jul 22 2013 Joe Orton <jorton@redhat.com> - 2.4.6-1
- update to 2.4.6
- mod_ssl: use revised NPN API (r1487772)

* Thu Jul 11 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-12
- mod_unique_id: replace use of hostname + pid with PRNG output (#976666)
- apxs: mention -p option in manpage

* Tue Jul  2 2013 Joe Orton <jorton@redhat.com> - 2.4.4-11
- add patch for aarch64 (Dennis Gilmore, #925558)

* Mon Jul  1 2013 Joe Orton <jorton@redhat.com> - 2.4.4-10
- remove duplicate apxs man page from httpd-tools

* Mon Jun 17 2013 Joe Orton <jorton@redhat.com> - 2.4.4-9
- remove zombie dbmmanage script

* Fri May 31 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-8
- return 400 Bad Request on malformed Host header

* Fri May 24 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-7
- ignore /etc/sysconfig/httpd and document systemd way of setting env variables
  in this file

* Mon May 20 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-6
- htpasswd/htdbm: fix hash generation bug (#956344)
- do not dump vhosts twice in httpd -S output (#928761)
- mod_cache: fix potential crash caused by uninitialized variable (#954109)

* Thu Apr 18 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-5
- execute systemctl reload as result of apachectl graceful
- mod_ssl: ignore SNI hints unless required by config
- mod_cache: forward-port CacheMaxExpire "hard" option
- mod_ssl: fall back on another module's proxy hook if mod_ssl proxy
  is not configured.

* Tue Apr 16 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-4
- fix service file to not send SIGTERM after ExecStop (#906321, #912288)

* Tue Mar 26 2013 Jan Kaluza <jkaluza@redhat.com> - 2.4.4-3
- protect MIMEMagicFile with IfModule (#893949)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-2
- really package mod_auth_form in mod_session (#915438)

* Tue Feb 26 2013 Joe Orton <jorton@redhat.com> - 2.4.4-1
- update to 2.4.4
- fix duplicate ownership of mod_session config (#914901)

* Fri Feb 22 2013 Joe Orton <jorton@redhat.com> - 2.4.3-17
- add mod_session subpackage, move mod_auth_form there (#894500)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Joe Orton <jorton@redhat.com> - 2.4.3-15
- add systemd service for htcacheclean

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-14
- drop patch for r1344712

* Tue Nov 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-13
- filter mod_*.so auto-provides (thanks to rcollet)
- pull in syslog logging fix from upstream (r1344712)

* Fri Oct 26 2012 Joe Orton <jorton@redhat.com> - 2.4.3-12
- rebuild to pick up new apr-util-ldap

* Tue Oct 23 2012 Joe Orton <jorton@redhat.com> - 2.4.3-11
- rebuild

* Wed Oct  3 2012 Joe Orton <jorton@redhat.com> - 2.4.3-10
- pull upstream patch r1392850 in addition to r1387633

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-9
- define PLATFORM in os.h using vendor string

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-8
- use systemd script unconditionally (#850149)

* Mon Oct  1 2012 Joe Orton <jorton@redhat.com> - 2.4.3-7
- use systemd scriptlets if available (#850149)
- don't run posttrans restart if /etc/sysconfig/httpd-disable-posttrans exists

* Mon Oct 01 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-6
- use systemctl from apachectl (#842736)

* Wed Sep 19 2012 Joe Orton <jorton@redhat.com> - 2.4.3-5
- fix some error log spam with graceful-stop (r1387633)
- minor mod_systemd tweaks

* Thu Sep 13 2012 Joe Orton <jorton@redhat.com> - 2.4.3-4
- use IncludeOptional for conf.d/*.conf inclusion

* Fri Sep 07 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.3-3
- adding mod_systemd to integrate with systemd better

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-2
- mod_ssl: add check for proxy keypair match (upstream r1374214)

* Tue Aug 21 2012 Joe Orton <jorton@redhat.com> - 2.4.3-1
- update to 2.4.3 (#849883)
- own the docroot (#848121)

* Mon Aug  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-23
- add mod_proxy fixes from upstream (r1366693, r1365604)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-21
- drop explicit version requirement on initscripts

* Thu Jul  5 2012 Joe Orton <jorton@redhat.com> - 2.4.2-20
- mod_ext_filter: fix error_log warnings

* Mon Jul  2 2012 Joe Orton <jorton@redhat.com> - 2.4.2-19
- support "configtest" and "graceful" as initscripts "legacy actions"

* Fri Jun  8 2012 Joe Orton <jorton@redhat.com> - 2.4.2-18
- avoid use of "core" GIF for a "core" directory (#168776)
- drop use of "syslog.target" in systemd unit file

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-17
- use _unitdir for systemd unit file
- use /run in unit file, ssl.conf

* Thu Jun  7 2012 Joe Orton <jorton@redhat.com> - 2.4.2-16
- mod_ssl: fix NPN patch merge

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-15
- move tmpfiles.d fragment into /usr/lib per new guidelines
- package /run/httpd not /var/run/httpd
- set runtimedir to /run/httpd likewise

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-14
- fix htdbm/htpasswd crash on crypt() failure (#818684)

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 2.4.2-13
- pull fix for NPN patch from upstream (r1345599)

* Thu May 31 2012 Joe Orton <jorton@redhat.com> - 2.4.2-12
- update suexec patch to use LOG_AUTHPRIV facility

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-11
- really fix autoindex.conf (thanks to remi@)

* Thu May 24 2012 Joe Orton <jorton@redhat.com> - 2.4.2-10
- fix autoindex.conf to allow symlink to poweredby.png

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-9
- suexec: use upstream version of patch for capability bit support

* Wed May 23 2012 Joe Orton <jorton@redhat.com> - 2.4.2-8
- suexec: use syslog rather than suexec.log, drop dac_override capability

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-7
- mod_ssl: add TLS NPN support (r1332643, #809599)

* Tue May  1 2012 Joe Orton <jorton@redhat.com> - 2.4.2-6
- add BR on APR >= 1.4.0

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-5
- use systemctl from logrotate (#221073)

* Fri Apr 27 2012 Joe Orton <jorton@redhat.com> - 2.4.2-4
- pull from upstream:
  * use TLS close_notify alert for dummy_connection (r1326980+)
  * cleanup symbol exports (r1327036+)

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-3
- really fix restart

* Fri Apr 20 2012 Joe Orton <jorton@redhat.com> - 2.4.2-2
- tweak default ssl.conf
- fix restart handling (#814645)
- use graceful restart by default

* Wed Apr 18 2012 Jan Kaluza <jkaluza@redhat.com> - 2.4.2-1
- update to 2.4.2

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-6
- fix macros

* Fri Mar 23 2012 Joe Orton <jorton@redhat.com> - 2.4.1-5
- add _httpd_moddir to macros

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-4
- fix symlink for poweredby.png
- fix manual.conf

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-3
- add mod_proxy_html subpackage (w/mod_proxy_html + mod_xml2enc)
- move mod_ldap, mod_authnz_ldap to mod_ldap subpackage

* Tue Mar 13 2012 Joe Orton <jorton@redhat.com> - 2.4.1-2
- clean docroot better
- ship proxy, ssl directories within /var/cache/httpd
- default config:
 * unrestricted access to (only) /var/www
 * remove (commented) Mutex, MaxRanges, ScriptSock
 * split autoindex config to conf.d/autoindex.conf
- ship additional example configs in docdir

* Tue Mar  6 2012 Joe Orton <jorton@redhat.com> - 2.4.1-1
- update to 2.4.1
- adopt upstream default httpd.conf (almost verbatim)
- split all LoadModules to conf.modules.d/*.conf
- include conf.d/*.conf at end of httpd.conf
- trim %%changelog
