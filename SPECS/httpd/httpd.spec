%define contentdir %{_datadir}/httpd
%define docroot /var/www
%define suexec_caller apache
%define mmn 20120211
%define mmnisa %{mmn}%{__isa_name}%{__isa_bits}
%define vstring %(source /etc/os-release; echo ${NAME})
%global mpm event

%define _confdir %{_sysconfdir}

Summary:        The Apache HTTP Server
Name:           httpd
Version:        2.4.52
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://httpd.apache.org/
Source0:        https://archive.apache.org/dist/%{name}/%{name}-%{version}.tar.bz2
Source3:        httpd.logrotate
Source4:        instance.conf
Source5:        httpd-ssl-pass-dialog
Source6:        httpd.tmpfiles
Source7:        httpd.service
Source8:        action-graceful.sh
Source9:        action-configtest.sh
Source10:       server-status.conf
Source11:       httpd.conf
Source12:       00-base.conf
Source13:       00-mpm.conf
Source14:       00-lua.conf
Source15:       01-cgi.conf
Source16:       00-dav.conf
Source17:       00-proxy.conf
Source18:       00-ssl.conf
Source19:       01-ldap.conf
Source20:       00-proxyhtml.conf
Source21:       userdir.conf
Source22:       ssl.conf
Source23:       welcome.conf
Source24:       manual.conf
Source25:       00-systemd.conf
Source26:       01-session.conf
Source27:       10-listen443.conf
Source28:       httpd.socket
Source29:       00-optional.conf
Source30:       README.confd
Source31:       README.confmod
Source32:       httpd.service.xml
Source33:       htcacheclean.service.xml
Source34:       httpd.conf.xml
Source40:       htcacheclean.service
Source41:       htcacheclean.sysconf
Source42:       httpd-init.service
Source43:       httpd-ssl-gencerts
Source44:       httpd@.service
Source45:       config.layout
Source46:       apachectl.sh
Source47:       apachectl.xml
Source48:       apache-poweredby.png

# build/scripts patches
Patch2:         httpd-2.4.43-apxs.patch
Patch3:         httpd-2.4.43-deplibs.patch
# Needed for socket activation and mod_systemd patch
Patch19:        httpd-2.4.43-detect-systemd.patch
# Features/functional changes
Patch21:        httpd-2.4.48-r1842929+.patch
Patch22:        httpd-2.4.43-mod_systemd.patch
Patch23:        httpd-2.4.48-export.patch
Patch24:        httpd-2.4.43-corelimit.patch
Patch25:        httpd-2.4.43-selinux.patch
Patch26:        httpd-2.4.43-gettid.patch
Patch27:        httpd-2.4.43-icons.patch
Patch30:        httpd-2.4.43-cachehardmax.patch
Patch34:        httpd-2.4.43-socket-activation.patch
Patch38:        httpd-2.4.43-sslciphdefault.patch
Patch39:        httpd-2.4.43-sslprotdefault.patch
Patch40:        httpd-2.4.43-r1861269.patch
Patch41:        httpd-2.4.43-r1861793+.patch
Patch42:        httpd-2.4.48-r1828172+.patch
Patch45:        httpd-2.4.43-logjournal.patch
Patch60:        httpd-2.4.43-enable-sslv3.patch
Patch61:        httpd-2.4.48-r1878890.patch
Patch63:        httpd-2.4.46-htcacheclean-dont-break.patch
Patch65:        httpd-2.4.51-r1894152.patch

BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  pkg-config
BuildRequires:  findutils
BuildRequires:  xmlto
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  systemd-devel
BuildRequires:  zlib-devel
BuildRequires:  libselinux-devel
BuildRequires:  apr >= 1.5.0
BuildRequires:  apr-devel >= 1.5.0
BuildRequires:  apr-util >= 1.5.0
BuildRequires:  apr-util-devel >= 1.5.0
BuildRequires:  brotli-devel
BuildRequires:  expat-devel
BuildRequires:  libdb-devel
BuildRequires:  lua-devel
BuildRequires:  openldap
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  pcre-devel >= 5.0
BuildRequires:  systemd-rpm-macros
BuildRequires:  gnupg2

Requires:       apr-util
Requires:       libdb
Requires:       lua
Requires:       openldap
Requires:       openssl
Requires:       pcre
Requires:       /etc/mime.types
Provides:       webserver
Provides:       mod_dav = %{version}-%{release}, httpd-suexec = %{version}-%{release}
Provides:       httpd-mmn = %{mmn}, httpd-mmn = %{mmnisa}
Requires:       httpd-tools = %{version}-%{release}
Requires:       httpd-filesystem = %{version}-%{release}
Recommends:     mod_http2, mod_lua
Requires(pre):  httpd-filesystem
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-units
Conflicts:      apr < 1.5.0-1
Provides:       mod_proxy_uwsgi = %{version}-%{release}
Obsoletes:      mod_proxy_uwsgi < 2.0.17.1-2

%description
The Apache HTTP Server is a powerful, efficient, and extensible
web server.

%package devel
Summary: Development interfaces for the Apache HTTP Server
Requires: apr-devel, apr-util-devel, pkgconfig
Requires: httpd = %{version}-%{release}

%description devel
The httpd-devel package contains the APXS binary and other files
that you need to build Dynamic Shared Objects (DSOs) for the
Apache HTTP Server.

If you are installing the Apache HTTP Server and you want to be
able to compile or develop additional modules for Apache, you need
to install this package.

%package manual
Summary: Documentation for the Apache HTTP Server
Requires: httpd = %{version}-%{release}
BuildArch: noarch

%description manual
The httpd-manual package contains the complete manual and
reference guide for the Apache HTTP Server. The information can
also be found at https://httpd.apache.org/docs/2.4/.

%package filesystem
Summary: The basic directory layout for the Apache HTTP Server
BuildArch: noarch
Requires(pre): /usr/sbin/useradd

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
BuildRequires: openssl-devel
Requires(pre): httpd-filesystem
Requires:      httpd = 0:%{version}-%{release}
Requires:      httpd-mmn = %{mmnisa}
Requires:      net-tools
Requires:      sscg >= 2.2.0
# mod_ssl/mod_nss cannot both be loaded simultaneously
Conflicts:     mod_nss

%description -n mod_ssl
The mod_ssl module provides strong cryptography for the Apache HTTP
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols.

%package -n mod_proxy_html
Summary: HTML and XML content filters for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
BuildRequires: libxml2-devel
BuildRequires: make

%description -n mod_proxy_html
The mod_proxy_html and mod_xml2enc modules provide filters which can
transform and modify HTML and XML content.

%package -n mod_ldap
Summary: LDAP authentication modules for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}
Requires: apr-util-ldap

%description -n mod_ldap
The mod_ldap and mod_authnz_ldap modules add support for LDAP
authentication to the Apache HTTP Server.

%package -n mod_session
Summary: Session interface for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}

%description -n mod_session
The mod_session module and associated backends provide an abstract
interface for storing and accessing per-user session data.

%package -n mod_lua
Summary: Lua scripting support for the Apache HTTP Server
Requires: httpd = 0:%{version}-%{release}, httpd-mmn = %{mmnisa}

%description -n mod_lua
The mod_lua module allows the server to be extended with scripts
written in the Lua programming language.

%prep

%setup -q
%patch2 -p1 -b .apxs
%patch3 -p1 -b .deplibs

%patch19 -p1 -b .detectsystemd

%patch21 -p1 -b .r1842929+
%patch22 -p1 -b .mod_systemd
%patch23 -p1 -b .export
%patch24 -p1 -b .corelimit
%patch25 -p1 -b .selinux
%patch26 -p1 -b .gettid
%patch27 -p1 -b .icons
%patch30 -p1 -b .cachehardmax
%patch34 -p1 -b .socketactivation
%patch38 -p1 -b .sslciphdefault
%patch39 -p1 -b .sslprotdefault
%patch40 -p1 -b .r1861269
%patch41 -p1 -b .r1861793+
%patch42 -p1 -b .r1828172+
%patch45 -p1 -b .logjournal

%patch60 -p1 -b .enable-sslv3
%patch61 -p1 -b .r1878890
%patch63 -p1 -b .htcacheclean-dont-break
%patch65 -p1 -b .r1894152

# Patch in the vendor string
sed -i '/^#define PLATFORM/s/Unix/%{vstring}/' os/unix/os.h

# Prevent use of setcap in "install-suexec-caps" target.
sed -i '/suexec/s,setcap ,echo Skipping setcap for ,' Makefile.in

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

sed '
s,@MPM@,%{mpm},g
s,@DOCROOT@,%{docroot},g
s,@LOGDIR@,%{_localstatedir}/log/httpd,g
' < $RPM_SOURCE_DIR/httpd.conf.xml \
    > httpd.conf.xml

xmlto man ./httpd.conf.xml
xmlto man $RPM_SOURCE_DIR/htcacheclean.service.xml
xmlto man $RPM_SOURCE_DIR/httpd.service.xml

# apachectl.xml => apachectl.8
xmlto man %{SOURCE47}

: Building with MMN %{mmn}, MMN-ISA %{mmnisa}
: Default MPM is %{mpm}, vendor string is '%{vstring}'

%build
# forcibly prevent use of bundled apr, apr-util, pcre
rm -rf srclib/{apr,apr-util,pcre}

# regenerate configure scripts
autoheader && autoconf || exit 1

# Before configure; fix location of build dir in generated apxs
%{__perl} -pi -e "s:\@exp_installbuilddir\@:%{_libdir}/httpd/build:g" \
        support/apxs.in

export CFLAGS=$RPM_OPT_FLAGS
export LDFLAGS="-Wl,-z,relro,-z,now"

# Hard-code path to links to avoid unnecessary builddep
export LYNX_PATH=/usr/bin/links

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
        --with-pcre \
        --enable-mods-shared=all \
        --enable-ssl --with-ssl --disable-distcache \
        --enable-proxy --enable-proxy-fdpass \
        --enable-cache \
        --enable-disk-cache \
        --enable-ldap --enable-authnz-ldap \
        --enable-cgid --enable-cgi \
        --enable-cgid-fdpassing \
        --enable-authn-anon --enable-authn-alias \
        --enable-systemd \
        --disable-imagemap --disable-file-cache \
        --disable-http2 \
        --disable-md \
        $*
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
         01-ldap.conf 00-systemd.conf 01-session.conf 00-optional.conf; do
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
mkdir $RPM_BUILD_ROOT%{_unitdir}/httpd.service.d
mkdir $RPM_BUILD_ROOT%{_unitdir}/httpd.socket.d

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
ln -s ../../pixmaps/system-noindex-logo.png \
        $RPM_BUILD_ROOT%{contentdir}/icons/system_noindex_logo.png

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

# Sanitize CFLAGS in standard config_vars.mk
sed '/^CFLAGS/s,=.*$,= -O2 -g -Wall,' \
    -i $RPM_BUILD_ROOT%{_libdir}/httpd/build/config_vars.mk

sed 's/config_vars.mk/vendor_config_vars.mk/' \
    $RPM_BUILD_ROOT%{_bindir}/apxs \
    > $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs
touch -r $RPM_BUILD_ROOT%{_bindir}/apxs \
      $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs
chmod 755 $RPM_BUILD_ROOT%{_libdir}/httpd/build/vendor-apxs

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
getent group apache >/dev/null || groupadd -g 48 -r apache
getent passwd apache >/dev/null || \
  useradd -r -u 48 -g apache -s /sbin/nologin \
    -d %{contentdir} -c "Apache" apache
exit 0

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
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-ssl.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-proxyhtml.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/00-lua.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-ldap.conf
%exclude %{_sysconfdir}/httpd/conf.modules.d/01-session.conf
%config(noreplace) %{_sysconfdir}/sysconfig/htcacheclean
%{_prefix}/lib/tmpfiles.d/httpd.conf
%dir %{_libexecdir}/initscripts/legacy-actions/httpd
%{_libexecdir}/initscripts/legacy-actions/httpd/*
%{_sbindir}/ht*
%{_sbindir}/fcgistarter
%{_sbindir}/apachectl
%{_sbindir}/rotatelogs
%caps(cap_setuid,cap_setgid+pe) %attr(510,root,%{suexec_caller}) %{_sbindir}/suexec
%dir %{_libdir}/httpd
%dir %{_libdir}/httpd/modules
%{_libdir}/httpd/modules/mod*.so
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
%{_mandir}/man8/*
%{_mandir}/man5/*
%exclude %{_mandir}/man8/httpd-init.*
%{_unitdir}/httpd.service
%{_unitdir}/httpd@.service
%{_unitdir}/htcacheclean.service
%{_unitdir}/*.socket

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

%files tools
%{_bindir}/*
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
