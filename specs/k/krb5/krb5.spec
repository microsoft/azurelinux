## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Set this so that find-lang.sh will recognize the .po files.
%global gettext_domain mit-krb5
# Guess where the -libs subpackage's docs are going to go.
%define libsdocdir %{?_pkgdocdir:%(echo %{_pkgdocdir} | sed -e s,krb5,krb5-libs,g)}%{!?_pkgdocdir:%{_docdir}/%{name}-libs-%{version}}
# Figure out where the default ccache lives and how we set it.
%global configure_default_ccache_name 1
%global configured_default_ccache_name KEYRING:persistent:%%{uid}

%global krb5_release %{autorelease}

# This should be e.g. beta1 or %%nil
%global pre_release %nil
%if "x%{?pre_release}" != "x"
%global krb5_release %autorelease -p -e %pre_release
# Use for tarball
%global krb5_pre_release -%{pre_release}
%endif

%global krb5_version_major 1
%global krb5_version_minor 22
# For a release without a patch number set to %%nil
%global krb5_version_patch 2

%global krb5_version_major_minor %{krb5_version_major}.%{krb5_version_minor}
%global krb5_version %{krb5_version_major_minor}
%if "x%{?krb5_version_patch}" != "x"
%global krb5_version %{krb5_version_major_minor}.%{krb5_version_patch}
%endif

# Should be in form 5.0, 6.1, etc.
%global kdbversion 9.0

Summary: The Kerberos network authentication system
Name: krb5
Version: %{krb5_version}
Release: %{krb5_release}

# rharwood has trust path to signing key and verifies on check-in
Source0: https://web.mit.edu/kerberos/dist/krb5/%{krb5_version_major_minor}/krb5-%{krb5_version}%{?krb5_pre_release}.tar.gz
Source1: https://web.mit.edu/kerberos/dist/krb5/%{krb5_version_major_minor}/krb5-%{krb5_version}%{?krb5_pre_release}.tar.gz.asc

Source2: kprop.service
Source3: kadmin.service
Source4: krb5kdc.service
Source5: krb5.conf
Source6: kdc.conf
Source7: kadm5.acl
Source8: krb5kdc.sysconfig
Source9: kadmin.sysconfig
Source10: kprop.sysconfig
Source11: ksu.pamd
Source12: krb5kdc.logrotate
Source13: kadmind.logrotate
Source14: krb5-krb5kdc.conf
Source15: %{name}-tests

# FIXME Backport bug fixes to https://<url>/<repo>/<branch>
# This will give us CI and makes it easy to generate patchsets.
#
# Generate the patchset using:
#   git format-patch -l1 --stdout -N > krb5-1.22-redhat.patch
# Where N is the number of patches
Patch0:        krb5-1.22-redhat.patch

License: Brian-Gladman-2-Clause AND BSD-2-Clause AND (BSD-2-Clause OR GPL-2.0-or-later) AND BSD-2-Clause-first-lines AND BSD-3-Clause AND BSD-4-Clause AND CMU-Mach-nodoc AND FSFULLRWD AND HPND AND HPND-export2-US AND HPND-export-US AND HPND-export-US-acknowledgement AND HPND-export-US-modify AND ISC AND MIT AND MIT-CMU AND OLDAP-2.8 AND OpenVision
URL: https://web.mit.edu/kerberos/www/
BuildRequires: autoconf, bison, make, flex, gawk, gettext, pkgconfig, sed
BuildRequires: gcc, gcc-c++
BuildRequires: libcom_err-devel, libedit-devel, libss-devel
BuildRequires: gzip, ncurses-devel
BuildRequires: python3, python3-sphinx
BuildRequires: keyutils, keyutils-libs-devel >= 1.5.8
BuildRequires: libselinux-devel
BuildRequires: pam-devel
BuildRequires: systemd-units
BuildRequires: tcl-devel
BuildRequires: libverto-devel
BuildRequires: openldap-devel
BuildRequires: lmdb-devel
BuildRequires: perl-interpreter
BuildRequires: openssl-devel >= 1:3.0.0

# For autosetup
BuildRequires: git

# Enable compilation of optional tests
BuildRequires: resolv_wrapper
BuildRequires: libcmocka-devel
BuildRequires: opensc
BuildRequires: softhsm

%description
Kerberos V5 is a trusted-third-party network authentication system,
which can improve your network's security by eliminating the insecure
practice of sending passwords over the network in unencrypted form.

%package devel
Summary: Development files needed to compile Kerberos 5 programs
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: libkadm5%{?_isa} = %{version}-%{release}
Requires: libcom_err-devel
Requires: keyutils-libs-devel, libselinux-devel
Requires: libverto-devel
Provides: krb5-kdb-devel-version = %{kdbversion}
# IPA wants ^ to be a separate symbol because they don't trust package
# managers to match -server and -devel in version.  Just go with it.

%description devel
Kerberos is a network authentication system. The krb5-devel package
contains the header files and libraries needed for compiling Kerberos
5 programs. If you want to develop Kerberos-aware programs, you need
to install this package.

%package libs
Summary: The non-admin shared libraries used by Kerberos 5
%if 0%{?fedora} > 35 || 0%{?rhel} >= 9
Requires: openssl-libs >= 1:3.0.0
%else
Requires: openssl-libs >= 1:1.1.1d-4
Requires: openssl-libs < 1:3.0.0
%endif
Requires: coreutils
Requires: keyutils-libs >= 1.5.8
Requires: /etc/crypto-policies/back-ends/krb5.config

%description libs
Kerberos is a network authentication system. The krb5-libs package
contains the shared libraries needed by Kerberos 5. If you are using
Kerberos, you need to install this package.

%package server
Summary: The KDC and related programs for Kerberos 5
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-pkinit%{?_isa} = %{version}-%{release}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
# we drop files in its directory, but we don't want to own that directory
Requires: logrotate
# we specify /usr/share/dict/words (provided by words) as the default dict_file in kdc.conf
Requires: words
# for run-time, and for parts of the test suite
BuildRequires: libverto-module-base
Requires: libverto-module-base
Requires: libkadm5%{?_isa} = %{version}-%{release}
Provides: krb5-kdb-version = %{kdbversion}

%description server
Kerberos is a network authentication system. The krb5-server package
contains the programs that must be installed on a Kerberos 5 key
distribution center (KDC).  If you are installing a Kerberos 5 KDC,
you need to install this package (in other words, most people should
NOT install this package).

%package server-ldap
Summary: The LDAP storage plugin for the Kerberos 5 KDC
Requires: %{name}-server%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: libkadm5%{?_isa} = %{version}-%{release}

%description server-ldap
Kerberos is a network authentication system. The krb5-server package
contains the programs that must be installed on a Kerberos 5 key
distribution center (KDC).  If you are installing a Kerberos 5 KDC,
and you wish to use a directory server to store the data for your
realm, you need to install this package.

%package workstation
Summary: Kerberos 5 programs for use on workstations
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-pkinit%{?_isa} = %{version}-%{release}
Requires: libkadm5%{?_isa} = %{version}-%{release}

%description workstation
Kerberos is a network authentication system. The krb5-workstation
package contains the basic Kerberos programs (kinit, klist, kdestroy,
kpasswd). If your network uses Kerberos, this package should be
installed on every workstation.

%package pkinit
Summary: The PKINIT module for Kerberos 5
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes: krb5-pkinit-openssl < %{version}-%{release}
Provides: krb5-pkinit-openssl = %{version}-%{release}

%description pkinit
Kerberos is a network authentication system. The krb5-pkinit
package contains the PKINIT plugin, which allows clients
to obtain initial credentials from a KDC using a private key and a
certificate.

%package xrealmauthz
Summary: Xrealmauthz policy module for Kerberos 5 KDC
Group: System Environment/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description xrealmauthz
Kerberos is a network authentication system. The krb5-xrealmauthz
package contains the xrealmauthz KDC plugin, which allows to configure
access rules to local realm for client principals from direct or
transitive cross-realms.

%package -n libkadm5
Summary: Kerberos 5 Administrative libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description -n libkadm5
Kerberos is a network authentication system. The libkadm5 package
contains only the libkadm5clnt and libkadm5serv shared objects. This
interface is not considered stable.

%package tests
Summary: Test sources for krb5 build

# Build dependencies
Requires: coreutils, gawk, sed
Requires: gcc-c++
Requires: gettext
Requires: libcom_err-devel
Requires: libselinux-devel
Requires: libss-devel
Requires: libverto-devel
Requires: lmdb-devel
Requires: openldap-devel
Requires: pam-devel
Requires: redhat-rpm-config
%if 0%{?fedora} > 35 || 0%{?rhel} >= 9
Requires: openssl-devel >= 1:3.0.0
%else
Requires: openssl-devel >= 1:1.1.1d-4
Requires: openssl-devel < 1:3.0.0
%endif

# Test dependencies
Requires: dejagnu
Requires: hostname
Requires: iproute
Requires: keyutils, keyutils-libs-devel >= 1.5.8
Requires: libcmocka-devel
Requires: libverto-module-base
Requires: logrotate
Requires: net-tools, rpcbind
Requires: perl-interpreter
Requires: procps-ng
Requires: python3-kdcproxy
Requires: resolv_wrapper
Requires: /etc/crypto-policies/back-ends/krb5.config
Requires: words
Requires: opensc
Requires: softhsm
Recommends: python3-pyrad

# Restore once openldap upstream tests are fixed
#Recommends: openldap-servers
#Recommends: openldap-clients

%description tests
FOR TESTING PURPOSE ONLY
Test sources for krb5 build, with pre-defined compilation parameters

%prep
%autosetup -S git_am -n %{name}-%{version}%{?dashpre}
ln NOTICE LICENSE

# Generate an FDS-compatible LDIF file.
inldif=src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
cat > '60kerberos.ldif' << EOF
# This is a variation on kerberos.ldif which 389 Directory Server will like.
dn: cn=schema
EOF
grep -Eiv '(^$|^dn:|^changetype:|^add:)' $inldif >> 60kerberos.ldif
touch -r $inldif 60kerberos.ldif

# Rebuild the configure scripts.
pushd src
autoreconf -fiv
popd

# Mess with some of the default ports that we use for testing, so that multiple
# builds going on the same host don't step on each other.
cfg="src/util/k5test.py"
LONG_BIT=`getconf LONG_BIT`
PORT=`expr 61000 + $LONG_BIT - 48`
sed -i -e s,61000,`expr "$PORT" + 0`,g $cfg
PORT=`expr 1750 + $LONG_BIT - 48`
sed -i -e s,1750,`expr "$PORT" + 0`,g $cfg
sed -i -e s,1751,`expr "$PORT" + 1`,g $cfg
sed -i -e s,1752,`expr "$PORT" + 2`,g $cfg
PORT=`expr 8888 + $LONG_BIT - 48`
sed -i -e s,8888,`expr "$PORT" - 0`,g $cfg
sed -i -e s,8887,`expr "$PORT" - 1`,g $cfg
sed -i -e s,8886,`expr "$PORT" - 2`,g $cfg
PORT=`expr 7777 + $LONG_BIT - 48`
sed -i -e s,7777,`expr "$PORT" + 0`,g $cfg
sed -i -e s,7778,`expr "$PORT" + 1`,g $cfg

# Fix kadmind port hard-coded in tests
PORT=`expr 61000 + $LONG_BIT - 48`
sed -i -e \
    "s,params.kadmind_port = 61001;,params.kadmind_port = $((PORT + 1));," \
    src/lib/kadm5/t_kadm5.c


%build
# Go ahead and supply tcl info, because configure doesn't know how to find it.
source %{_libdir}/tclConfig.sh
pushd src

# This should be safe to remove once we have autoconf >= 2.70
export runstatedir=/run

# Work out the CFLAGS and CPPFLAGS which we intend to use.
INCLUDES=-I%{_includedir}/et
CFLAGS="`echo $RPM_OPT_FLAGS $DEFINES $INCLUDES -fPIC -fno-strict-aliasing -fstack-protector-all`"
CPPFLAGS="`echo $DEFINES $INCLUDES`"
%configure \
    CC="%{__cc}" \
    CFLAGS="$CFLAGS" \
    CPPFLAGS="$CPPFLAGS" \
    SS_LIB="-lss" \
    PKCS11_MODNAME="p11-kit-proxy.so" \
    --enable-shared \
    --runstatedir=/run \
    --localstatedir=%{_var}/kerberos \
    --disable-rpath \
    --without-krb5-config \
    --with-system-et \
    --with-system-ss \
    --enable-dns-for-realm \
    --with-ldap \
    --enable-pkinit \
    --with-crypto-impl=openssl \
    --with-tls-impl=openssl \
    --with-system-verto \
    --with-pam \
    --with-selinux \
    --with-lmdb \
    || (cat config.log; exit 1)

# Check we have required features enabled
for x in DNS_LOOKUP DNS_LOOKUP_REALM; do
    grep -q "#define KRB5_${x} 1" include/autoconf.h
done

# Sanity check the KDC_RUN_DIR.
pushd include
%make_build osconf.h
popd
configured_dir=`grep KDC_RUN_DIR include/osconf.h | awk '{print $NF}'`
configured_dir=`eval echo $configured_dir`
if test "$configured_dir" != /run/krb5kdc ; then
    echo Failed to configure KDC_RUN_DIR.
    exit 1
fi

%make_build
popd

# Build the docs.
make -C src/doc paths.py version.py
cp src/doc/paths.py doc/
install -d -m 0755 build-man build-html
sphinx-build -a -b man   -t pathsubs doc build-man
sphinx-build -a -b html  -t pathsubs doc build-html
rm -fr build-html/_sources

%install
# Sample KDC config files (bundled kdc.conf and kadm5.acl).
install -d -m 0755 %{buildroot}%{_var}/kerberos/krb5kdc
install -pm 600 %{SOURCE6} %{buildroot}%{_var}/kerberos/krb5kdc/
install -pm 600 %{SOURCE7} %{buildroot}%{_var}/kerberos/krb5kdc/

# Where per-user keytabs live by default.
install -d -m 0755 %{buildroot}%{_var}/kerberos/krb5/user

# Default configuration file for everything.
install -d -m 0755 %{buildroot}%{_sysconfdir}
install -pm 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/krb5.conf

# Default include on this directory
install -d -m 0755 %{buildroot}%{_sysconfdir}/krb5.conf.d
ln -sv %{_sysconfdir}/crypto-policies/back-ends/krb5.config %{buildroot}%{_sysconfdir}/krb5.conf.d/crypto-policies

# Parent of configuration file for list of loadable GSS mechs ("mechs").  This
# location is not relative to sysconfdir, but is hard-coded in g_initialize.c.
mkdir -m 755 -p %{buildroot}%{_sysconfdir}/gss
# Parent of groups of configuration files for a list of loadable GSS mechs
# ("mechs").  This location is not relative to sysconfdir, and is also
# hard-coded in g_initialize.c.
mkdir -m 755 -p %{buildroot}%{_sysconfdir}/gss/mech.d

# If the default configuration needs to start specifying a default cache
# location, add it now, then fixup the timestamp so that it looks the same.
%if 0%{?configure_default_ccache_name}
export DEFCCNAME="%{configured_default_ccache_name}"
awk '{print}
     /^#    default_realm/{print "    default_ccache_name =", ENVIRON["DEFCCNAME"]}' \
     %{SOURCE5} > %{buildroot}%{_sysconfdir}/krb5.conf
touch -r %{SOURCE5} %{buildroot}%{_sysconfdir}/krb5.conf
grep default_ccache_name %{buildroot}%{_sysconfdir}/krb5.conf
%endif

# Server init scripts (krb5kdc,kadmind,kpropd) and their sysconfig files.
install -d -m 0755 %{buildroot}%{_unitdir}
for unit in \
    %{SOURCE4}\
     %{SOURCE3} \
     %{SOURCE2} ; do
    # In the past, the init script was supposed to be named after the service
    # that the started daemon provided.  Changing their names is an
    # upgrade-time problem I'm in no hurry to deal with.
    install -pm 644 ${unit} %{buildroot}%{_unitdir}
done
install -d -m 0755 %{buildroot}/%{_tmpfilesdir}
install -pm 644 %{SOURCE14} %{buildroot}/%{_tmpfilesdir}/
install -d -m 0755 %{buildroot}/%{_localstatedir}/run/krb5kdc

install -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
for sysconfig in %{SOURCE8} %{SOURCE9} %{SOURCE10} ; do
    install -pm 644 ${sysconfig} \
            %{buildroot}%{_sysconfdir}/sysconfig/`basename ${sysconfig} .sysconfig`
done

# logrotate configuration files
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d/
for logrotate in \
    %{SOURCE12} \
     %{SOURCE13} ; do
    install -pm 644 ${logrotate} \
            %{buildroot}%{_sysconfdir}/logrotate.d/`basename ${logrotate} .logrotate`
done

# PAM configuration files.
install -d -m 0755 %{buildroot}%{_sysconfdir}/pam.d/
for pam in %{SOURCE11} ; do
    install -pm 644 ${pam} \
            %{buildroot}%{_sysconfdir}/pam.d/`basename ${pam} .pamd`
done

# Plug-in directories.
install -pdm 755 %{buildroot}/%{_libdir}/krb5/plugins/preauth
install -pdm 755 %{buildroot}/%{_libdir}/krb5/plugins/kdb
install -pdm 755 %{buildroot}/%{_libdir}/krb5/plugins/authdata

# The rest of the binaries, headers, libraries, and docs.
%make_install -C src EXAMPLEDIR=%{libsdocdir}/examples

# Munge krb5-config yet again.  This is totally wrong for 64-bit, but chunks
# of the buildconf patch already conspire to strip out /usr/<anything> from the
# list of link flags, and it helps prevent file conflicts on multilib systems.
sed -r -i -e 's|^libdir=/usr/lib(64)?$|libdir=/usr/lib|g' %{buildroot}%{_bindir}/krb5-config

# Workaround krb5-config reading too much from LDFLAGS.
# https://bugzilla.redhat.com/show_bug.cgi?id=1997021
# https://bugzilla.redhat.com/show_bug.cgi?id=2048909
sed -i -r -e 's/^(LDFLAGS=).*/\1/' %{buildroot}%{_bindir}/krb5-config

# Install processed man pages.
for section in 1 5 8 ; do
    install -m 644 build-man/*.${section} \
            %{buildroot}/%{_mandir}/man${section}/
done

# I'm tired of warnings about these not having man pages
rm -- "%{buildroot}/%{_sbindir}/krb5-send-pr"
rm -- "%{buildroot}/%{_sbindir}/sim_server"
rm -- "%{buildroot}/%{_sbindir}/gss-server"
rm -- "%{buildroot}/%{_sbindir}/uuserver"
rm -- "%{buildroot}/%{_bindir}/sim_client"
rm -- "%{buildroot}/%{_bindir}/gss-client"
rm -- "%{buildroot}/%{_bindir}/uuclient"

# These files are already packaged elsewhere
rm -- "%{buildroot}/%{_docdir}/krb5-libs/examples/kdc.conf"
rm -- "%{buildroot}/%{_docdir}/krb5-libs/examples/krb5.conf"
rm -- "%{buildroot}/%{_docdir}/krb5-libs/examples/services.append"

# This is only needed for tests
rm -- "%{buildroot}/%{_libdir}/krb5/plugins/preauth/test.so"

# Generate tests launching script
sed -e 's/{{ name }}/%{name}/g' \
    -e 's/{{ version }}/%{krb5_version}/g' \
    -e 's/{{ release }}/%{krb5_release}/g' \
    -e 's/{{ arch }}/%{_arch}/g' \
    -i %{SOURCE15}
install -d -m 0755 %{buildroot}%{_libexecdir}
install -pm 755 %{SOURCE15} %{buildroot}%{_libexecdir}/%{name}-tests-%{_arch}

# Copy source files from build folder to system data folder
install -pdm 755 %{buildroot}%{_datarootdir}/%{name}-tests/%{_arch}
pushd src
cp -p --parents -t "%{buildroot}%{_datarootdir}/%{name}-tests/%{_arch}/" \
    $(find . -type f -exec file -i "{}" + \
          | sed -n \
                -e 's|^\./\([^:]\+\): \+text/.\+$|\1|p' \
                -e 's|^\./\([^:]\+\): \+application/x-pem-file.\+$|\1|p' \
                -e 's|^\./\([^:]\+\): \+application/json.\+$|\1|p' \
          | grep -Ev '~$')
popd

# Copy binary test files
install -pm 644 src/tests/pkinit-certs/*.p12 \
    "%{buildroot}%{_datarootdir}/%{name}-tests/%{_arch}/tests/pkinit-certs/"

# Unset executable bit if no shebang in script
for f in $(find "%{buildroot}%{_datarootdir}/%{name}-tests/%{_arch}/" -type f -executable)
do
    head -n1 "$f" | grep -Eq '^#!' || chmod a-x "$f"
done

%find_lang %{gettext_domain}

%ldconfig_scriptlets libs

%ldconfig_scriptlets server-ldap

%post server
%tmpfiles_create %{_tmpfilesdir}/krb5-krb5kdc.conf
%systemd_post krb5kdc.service kadmin.service kprop.service
# assert sanity.  A cleaner solution probably exists but it is opaque
/bin/systemctl daemon-reload
exit 0

%preun server
%systemd_preun krb5kdc.service kadmin.service kprop.service
exit 0

%postun server
%systemd_postun_with_restart krb5kdc.service kadmin.service kprop.service
exit 0

%ldconfig_scriptlets -n libkadm5

%files workstation
%doc src/config-files/services.append
%doc src/config-files/krb5.conf
%doc build-html/*

# Clients of the KDC, including tools you're likely to need if you're running
# app servers other than those built from this source package.
%{_bindir}/kdestroy
%{_mandir}/man1/kdestroy.1*
%{_bindir}/kinit
%{_mandir}/man1/kinit.1*
%{_bindir}/klist
%{_mandir}/man1/klist.1*
%{_bindir}/kpasswd
%{_mandir}/man1/kpasswd.1*
%{_bindir}/kswitch
%{_mandir}/man1/kswitch.1*

%{_bindir}/kvno
%{_mandir}/man1/kvno.1*
%{_bindir}/kadmin
%{_mandir}/man1/kadmin.1*
%{_bindir}/k5srvutil
%{_mandir}/man1/k5srvutil.1*
%{_bindir}/ktutil
%{_mandir}/man1/ktutil.1*

# Doesn't really fit anywhere else.
%attr(4755,root,root) %{_bindir}/ksu
%{_mandir}/man1/ksu.1*
%config(noreplace) %{_sysconfdir}/pam.d/ksu

%files server
%docdir %{_mandir}
%doc src/config-files/kdc.conf
%{_unitdir}/krb5kdc.service
%{_unitdir}/kadmin.service
%{_unitdir}/kprop.service
%{_tmpfilesdir}/krb5-krb5kdc.conf
%dir %{_localstatedir}/run/krb5kdc
%config(noreplace) %{_sysconfdir}/sysconfig/krb5kdc
%config(noreplace) %{_sysconfdir}/sysconfig/kadmin
%config(noreplace) %{_sysconfdir}/sysconfig/kprop
%config(noreplace) %{_sysconfdir}/logrotate.d/krb5kdc
%config(noreplace) %{_sysconfdir}/logrotate.d/kadmind

%dir %{_var}/kerberos
%dir %{_var}/kerberos/krb5kdc
%config(noreplace) %{_var}/kerberos/krb5kdc/kdc.conf
%config(noreplace) %{_var}/kerberos/krb5kdc/kadm5.acl

%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%dir %{_libdir}/krb5/plugins/preauth
%dir %{_libdir}/krb5/plugins/authdata
%{_libdir}/krb5/plugins/preauth/otp.so
%{_libdir}/krb5/plugins/kdb/db2.so
%{_libdir}/krb5/plugins/kdb/klmdb.so

# KDC binaries and configuration.
%{_mandir}/man5/kadm5.acl.5*
%{_mandir}/man5/kdc.conf.5*
%{_sbindir}/kadmin.local
%{_mandir}/man8/kadmin.local.8*
%{_sbindir}/kadmind
%{_mandir}/man8/kadmind.8*
%{_sbindir}/kdb5_util
%{_mandir}/man8/kdb5_util.8*
%{_sbindir}/kprop
%{_mandir}/man8/kprop.8*
%{_sbindir}/kpropd
%{_mandir}/man8/kpropd.8*
%{_sbindir}/kproplog
%{_mandir}/man8/kproplog.8*
%{_sbindir}/krb5kdc
%{_mandir}/man8/krb5kdc.8*

# This is here for people who want to test their server.  It was formerly also
# included in -devel.
%{_bindir}/sclient
%{_mandir}/man1/sclient.1*
%{_sbindir}/sserver
%{_mandir}/man8/sserver.8*

%files server-ldap
%docdir %{_mandir}
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.ldif
%doc src/plugins/kdb/ldap/libkdb_ldap/kerberos.schema
%doc 60kerberos.ldif
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdb
%{_libdir}/krb5/plugins/kdb/kldap.so
%{_libdir}/libkdb_ldap.so
%{_libdir}/libkdb_ldap.so.*
%{_mandir}/man8/kdb5_ldap_util.8.gz
%{_sbindir}/kdb5_ldap_util

%files libs -f %{gettext_domain}.lang
%doc README NOTICE
%{!?_licensedir:%global license %%doc}
%license LICENSE
%docdir %{_mandir}
# These are hard-coded, not-dependent-on-the-configure-script paths.
%dir %{_sysconfdir}/gss
%dir %{_sysconfdir}/gss/mech.d
%dir %{_sysconfdir}/krb5.conf.d
%config(noreplace) %{_sysconfdir}/krb5.conf
%config(noreplace,missingok) %{_sysconfdir}/krb5.conf.d/crypto-policies
%{_mandir}/man5/.k5identity.5*
%{_mandir}/man5/.k5login.5*
%{_mandir}/man5/k5identity.5*
%{_mandir}/man5/k5login.5*
%{_mandir}/man5/krb5.conf.5*
%{_mandir}/man7/kerberos.7*
%{_libdir}/libgssapi_krb5.so.*
%{_libdir}/libgssrpc.so.*
%{_libdir}/libk5crypto.so.*
%{_libdir}/libkdb5.so.*
%{_libdir}/libkrad.so.*
%{_libdir}/libkrb5.so.*
%{_libdir}/libkrb5support.so.*
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/*
%{_libdir}/krb5/plugins/tls/k5tls.so
%{_libdir}/krb5/plugins/preauth/spake.so
%dir %{_var}/kerberos
%dir %{_var}/kerberos/krb5
%dir %{_var}/kerberos/krb5/user

%files pkinit
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/preauth
%{_libdir}/krb5/plugins/preauth/pkinit.so

%files xrealmauthz
%dir %{_libdir}/krb5
%dir %{_libdir}/krb5/plugins
%dir %{_libdir}/krb5/plugins/kdcpolicy
%{_libdir}/krb5/plugins/kdcpolicy/xrealmauthz.so

%files devel
%docdir %{_mandir}

%{_includedir}/gssapi.h
%{_includedir}/kdb.h
%{_includedir}/krad.h
%{_includedir}/krb5.h
%{_includedir}/profile.h
%{_includedir}/gssapi/
%{_includedir}/gssrpc/
%{_includedir}/kadm5/
%{_includedir}/krb5/
%{_libdir}/libgssapi_krb5.so
%{_libdir}/libgssrpc.so
%{_libdir}/libk5crypto.so
%{_libdir}/libkdb5.so
%{_libdir}/libkrad.so
%{_libdir}/libkrb5.so
%{_libdir}/libkrb5support.so
%{_libdir}/pkgconfig/gssrpc.pc
%{_libdir}/pkgconfig/kadm-client.pc
%{_libdir}/pkgconfig/kadm-server.pc
%{_libdir}/pkgconfig/kdb.pc
%{_libdir}/pkgconfig/krb5-gssapi.pc
%{_libdir}/pkgconfig/krb5.pc
%{_libdir}/pkgconfig/mit-krb5-gssapi.pc
%{_libdir}/pkgconfig/mit-krb5.pc

%{_bindir}/krb5-config
%{_mandir}/man1/krb5-config.1*

%files -n libkadm5
%{_libdir}/libkadm5clnt.so
%{_libdir}/libkadm5clnt_mit.so
%{_libdir}/libkadm5srv.so
%{_libdir}/libkadm5srv_mit.so
%{_libdir}/libkadm5clnt_mit.so.*
%{_libdir}/libkadm5srv_mit.so.*

%files tests
%{_libexecdir}/%{name}-tests-%{_arch}
%{_datarootdir}/%{name}-tests/%{_arch}

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.22.2-3
- Latest state for krb5

* Mon Feb 16 2026 Julien Rische <jrische@redhat.com> - 1.22.2-2
- Force "fork" method for RADIUS daemon in OTP test
- Create sub-package for xrealmautz KDC plugin
- resolves: rhbz#2437324
- Fix PKINIT paChecksum2 ASN.1 tests

* Thu Feb 12 2026 Andreas Schneider <asn@redhat.com> - 1.22.2-1
- Update to version 1.22.2
- resolves: rhbz#2388209
- resolves: rhbz#2422257

* Thu Feb 12 2026 Andreas Schneider <asn@redhat.com> - 1.21.3-11
- Replace /etc with %%{_sysconfdir}

* Thu Feb 12 2026 Andreas Schneider <asn@redhat.com> - 1.21.3-10
- Replace $RPM_BUILD_ROOT with %%{buildroot}

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Julien Rische <jrische@redhat.com> - 1.21.3-6
- Do not block HMAC-MD4/5 in FIPS mode
  Resolves: rhbz#2370259
- PKINIT: implement paChecksum2 from MS-PKCA v20230920
  Resolves: rhbz#2357215
- Disallow RC4 HMAC-MD5 session keys by default (CVE-2025-3576)
  Resolves: rhbz#2359705

* Wed Jan 29 2025 Julien Rische <jrische@redhat.com> - 1.21.3-5
- Prevent overflow when calculating ulog block size (CVE-2025-24528)
  Resolves: rhbz#2342798
- Support PKCS11 EC client certs in PKINIT
  Resolves: rhbz#2341962
- kdb5_util: fix DB entry flags on modification
  Resolves: rhbz#2336555
- Add ECDH support for PKINIT (RFC5349)
  Resolves: rhbz#2214326
- Remove dependency of krb5-libs on gawk and sed
  Resolves: rhbz#2323859

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Oct 30 2024 Julien Rische <jrische@redhat.com> - 1.21.3-3
- libkrad: implement support for Message-Authenticator (CVE-2024-3596)
  Resolves: rhbz#2304071
- Fix various issues detected by static analysis
  Resolves: rhbz#2322704
- Remove RSA protocol for PKINIT
  Resolves: rhbz#2322706
- Make TCP waiting time configurable
  Resolves: rhbz#2322711

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Julien Rische <jrische@redhat.com> - 1.21.3-1
- New upstream version (1.21.3)
- CVE-2024-26458: Memory leak in src/lib/rpc/pmap_rmt.c
  Resolves: rhbz#2266732
- CVE-2024-26461: Memory leak in src/lib/gssapi/krb5/k5sealv3.c
  Resolves: rhbz#2266741
- CVE-2024-26462: Memory leak in src/kdc/ndr.c
  Resolves: rhbz#2266743
- Add missing SPDX license identifiers
  Resolves: rhbz#2265333

* Mon Jul 08 2024 Julien Rische <jrische@redhat.com> - 1.21.2-6
- CVE-2024-37370 CVE-2024-37371: GSS message token handling
  Resolves: rhbz#2294678 rhbz#2294680
- Fix double free in klist's show_ccache()
  Resolves: rhbz#2257301
- Do not include files with "~" termination in krb5-tests

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Julien Rische <jrische@redhat.com> - 1.21.2-3
- Fix double free in klist's show_ccache()
  Resolves: rhbz#2257301
- Store krb5-tests files in architecture-specific directories
  Resolves: rhbz#2244601

* Tue Oct 10 2023 Julien Rische <jrische@redhat.com> - 1.21.2-2
- Use SPDX expression for license tag
- Fix unimportant memory leaks
  Resolves: rhbz#2223274

* Wed Aug 16 2023 Julien Rische <jrische@redhat.com> - 1.21.2-1
- New upstream version (1.21.2)
- Fix double-free in KDC TGS processing (CVE-2023-39975)
  Resolves: rhbz#2229113
- Make tests compatible with Python 3.12
  Resolves: rhbz#2224013

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Marek Blaha <mblaha@redhat.com> - 1.21-2
- Replace file dependency with package name
  Resolves: rhbz#2216903

* Mon Jun 12 2023 Julien Rische <jrische@redhat.com> - 1.21-1
- New upstream version (1.21)
- Do not disable PKINIT if some of the well-known DH groups are unavailable
  Resolves: rhbz#2214297
- Make PKINIT CMS SHA-1 signature verification available in FIPS mode
  Resolves: rhbz#2214300
- Allow to set PAC ticket signature as optional
  Resolves: rhbz#2181311
- Add support for MS-PAC extended KDC signature (CVE-2022-37967)
  Resolves: rhbz#2166001
- Fix syntax error in aclocal.m4
  Resolves: rhbz#2143306

* Tue Jan 31 2023 Julien Rische <jrische@redhat.com> - 1.20.1-9
- Add support for MS-PAC extended KDC signature (CVE-2022-37967)
  Resolves: rhbz#2166001

* Mon Jan 30 2023 Julien Rische <jrische@redhat.com> - 1.20.1-8
- Bypass FIPS restrictions to use KRB5KDF in case AES SHA-1 HMAC is enabled
- Lazily load MD4/5 from OpenSSL if using RADIUS or RC4 enctype in FIPS mode

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Julien Rische <jrische@redhat.com> - 1.20.1-6
- Set aes256-cts-hmac-sha384-192 as EXAMLE.COM master key in kdc.conf
- Add AES SHA-2 HMAC family as EXAMPLE.COM supported etypes in kdc.conf
  Resolves: rhbz#2114771

* Mon Jan 09 2023 Julien Rische <jrische@redhat.com> - 1.20.1-5
- Strip debugging data from ksu executable file

* Thu Jan 05 2023 Julien Rische <jrische@redhat.com> - 1.20.1-4
- Include missing OpenSSL FIPS header
- Make tests compatible with sssd_krb5_locator_plugin.so

* Tue Dec 06 2022 Julien Rische <jrische@redhat.com> - 1.20.1-3
- Enable TMT integration with Fedora CI

* Thu Dec  1 2022 Alexander Bokovoy <abokovoy@redhat.com> - 1.20.1-2
- Bump KDB ABI version provide to 9.0

* Wed Nov 23 2022 Julien Rische <jrische@redhat.com> - 1.20.1-1
- New upstream version (1.20.1)
  Resolves: rhbz#2124463
- Restore "supportedCMSTypes" attribute in PKINIT preauth requests
- Set SHA-512 or SHA-256 with RSA as preferred CMS signature algorithms
  Resolves: rhbz#2114766
- Update error checking for OpenSSL CMS_verify
  Resolves: rhbz#2119704
- Remove invalid password expiry warning
  Resolves: rhbz#2129113

* Wed Nov 09 2022 Julien Rische <jrische@redhat.com> - 1.19.2-13
- Fix integer overflows in PAC parsing (CVE-2022-42898)
  Resolves: rhbz#2143011

* Tue Aug 02 2022 Andreas Schneider <asn@redhat.com> - 1.19.2-12
- Use baserelease to set the release number
- Do not define netlib, but use autoconf detection for res_* functions
- Add missing BR for resolv_wrapper to run t_discover_uri.py

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-11.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Julien Rische <jrische@redhat.com> - 1.19.2-11
- Allow libkrad UDP/TCP connection to localhost in FIPS mode
  Resolves: rhbz#2082189
- Read GSS configuration files with mtime 0

* Mon May  2 2022 Julien Rische <jrische@redhat.com> - 1.19.2-10
- Use p11-kit as default PKCS11 module
  Resolves: rhbz#2073274
- Try harder to avoid password change replay errors
  Resolves: rhbz#2072059

* Tue Apr 05 2022 Alexander Bokovoy <abokovoy@redhat.com> - 1.19.2-9
- Fix libkrad client cleanup
- Fixes rhbz#2072059

* Tue Apr 05 2022 Alexander Bokovoy <abokovoy@redhat.com> - 1.19.2-8
- Allow use of larger RADIUS attributes in krad library

* Wed Mar 23 2022 Julien Rische <jrische@redhat.com> - 1.19.2-7
- Use SHA-256 instead of SHA-1 for PKINIT CMS digest

* Tue Feb  8 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.19.2-6
- Drop old trigger scriplet
- Reenable package notes and strip LDFLAGS from krb5-config (rhbz#2048909)

* Wed Feb 02 2022 Alexander Bokovoy <abokovoy@redhat.com> - 1.19.2-5
- Temporarily remove package note to unblock krb5-dependent packages
  Resolves: rhbz#2048909

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 3 2021 Antonio Torres <antorres@redhat.com> - 1.19.2-4
- Add patches to support OpenSLL 3.0.0
- Remove TCL-based libkadm5 API tests

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.19.2-3.1
- Rebuilt with OpenSSL 3.0.0

* Tue Aug 24 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.2-3
- Remove -specs= from krb5-config output

* Thu Aug 19 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.2-2
- Fix KDC null deref on TGS inner body null server (CVE-2021-37750)

* Mon Jul 26 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.2-1
- New upstream version (1.19.2)

* Wed Jul 21 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-15
- Fix defcred leak in krb5 gss_inquire_cred()

* Mon Jul 12 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-14
- Fix KDC null deref on bad encrypted challenge (CVE-2021-36222)

* Thu Jul 01 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-13
- Fix use-after-free during krad remote_shutdown()

* Mon Jun 28 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-12
- MEMORY locking fix and static analysis pullup

* Mon Jun 21 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-11
- Add the backward-compatible parts of openssl3 support

* Wed Jun 09 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-10
- Fix three canonicalization cases for fallback

* Wed Jun 02 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-9
- Fix doc build for Sphinx 4.0

* Thu May 20 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-8
- Add all the sssd-kcm workarounds

* Thu May 20 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-7
- Fix context for previous backport

* Thu May 20 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-6
- Add KCM_OP_GET_CRED_LIST and KCM_OP_RETRIEVE support

* Tue May 04 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-5
- Suppress static analyzer warning in FIPS override

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.19.1-3.1
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Mar 01 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-3
- Further test dependency fixes; no code changes

* Mon Mar 01 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-2
- Make test dependencies contingent on skipcheck; no code changes

* Thu Feb 18 2021 Robbie Harwood <rharwood@redhat.com> - 1.19.1-1
- New upstream version (1.19.1)

* Wed Feb 17 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-3
- Restore krb5_set_default_tgs_ktypes()

* Fri Feb 05 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-2
- No code change; just coping with reverted autoconf

* Tue Feb 02 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-1
- New upstream version (1.19)

* Thu Jan 28 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-0.beta2.5
- Support host-based GSS initiator names

* Thu Jan 28 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-0.beta2.4
- Require krb5-pkinit from krb5-{server,workstation}

* Thu Jan 28 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-0.beta2.3
- Fix up weird mass rebuild versioning

* Thu Jan 28 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-0.beta2.2.2
- Add APIs for marshalling credentials

* Wed Jan 27 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-0.beta2.1.2
- Cope with new autotools behavior wrt runstatedir

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19-0.beta2.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 2021 Robbie Harwood <rharwood@redhat.com> - 1.19-1
- New upstream version (1.19-beta2)

* Wed Dec 16 2020 Robbie Harwood <rharwood@redhat.com> - 1.19-0.beta1.2
- New upstream version (1.19-beta1)

* Wed Dec 16 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.3-5
- Fix runstatedir configuration
- Why couldn't systemd just leave it alone?

* Tue Nov 24 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.3-4
- Document -k option in kvno(1) synopsis

* Fri Nov 20 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.3-3
- Upstream executable shared libraries patch

* Wed Nov 18 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.3-2
- Fix build failure in -1

* Wed Nov 18 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.3-1
- New upstream version (1.18.3)

* Tue Nov 17 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-30
- Migrate /var/run to /run, an exercise in pointlessness
  Resolves: rhbz#1898410

* Thu Nov 05 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-29
- Add recursion limit for ASN.1 indefinite lengths (CVE-2020-28196)

* Fri Oct 23 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-28
- Fix minor static analysis defects

* Wed Oct 21 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-27
- Fix build of previous

* Wed Oct 21 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-26
- Cross-realm s4u fixes for samba (rhbz#1836630)

* Thu Oct 15 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-25
- Unify kvno option documentation

* Fri Oct 02 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-24
- Add md5 override to krad

* Thu Sep 10 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-23
- Use `systemctl reload` to HUP the KDC during logrotate
  Resolves: rhbz#1877692

* Wed Sep 09 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-22
- Fix input length checking in SPNEGO DER decoding

* Fri Aug 28 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-21
- Mark crypto-polices snippet as missingok
  Resolves: rhbz#1868379

* Thu Aug 13 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-20
- Temporarily dns_canonicalize_hostname=fallback changes
- Hopefully unbreak IPA while we debug further

* Fri Aug 07 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-19
- Expand dns_canonicalize_hostname=fallback support

* Tue Aug 04 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-18
- Fix leak in KERB_AP_OPTIONS_CBT server support

* Mon Aug 03 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-17
- Revert qualify_shortname removal

* Mon Aug 03 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-16
- Disable tests on s390x
  Resolves: rhbz#1863952

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-15
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 31 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-14
- Revert qualify_shortname changes

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-12
- Ignore bad enctypes in krb5_string_to_keysalts()
- Allow gss_unwrap_iov() of unpadded RC4 tokens

* Wed Jul 15 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-11
- Ignore bad enctypes in krb5_string_to_keysalts()

* Wed Jul 08 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-10
- Set qualify_shortname empty in default configuration
  Resolves: rhbz#1852041

* Mon Jun 15 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-9
- Use two queues for concurrent t_otp.py daemons

* Mon Jun 15 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-8
- Match Heimdal behavior for channel bindings

* Mon Jun 08 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-7
- Fix test suite by removing wrapper workarounds

* Mon Jun 08 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-6
- Omit PA_FOR_USER if we can't compute its checksum

* Sat May 30 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-5
- Replace gssrpc tests with a Python script

* Sat May 30 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-4
- Default dns_canonicalize_hostname to "fallback"

* Tue May 26 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-3
- dns_canonicalize_hostname = fallback

* Tue May 26 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-2
- Pass channel bindings through SPNEGO

* Fri May 22 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.2-1
- New upstream release (1.18.2)

* Fri May 22 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.1-6
- Fix SPNEGO acceptor mech filtering

* Mon May 18 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.1-5
- Fix typo ("in in") in the ksu man page

* Fri May 08 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.1-4
- Omit KDC indicator check for S4U2Self requests

* Tue Apr 28 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.1-3
- Pass gss_localname() through SPNEGO

* Tue Apr 14 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-1.1
- Drop yasm requirement since we don't use builtin crypto

* Tue Apr 14 2020 Robbie Harwood <rharwood@redhat.com> - 1.18.1-1
- New upstream version (1.18.1)

* Tue Apr 07 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-12
- Make ksu honor KRB5CCNAME again

* Thu Apr 02 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-11
- Do expiration warnings for all init_creds APIs

* Wed Apr 01 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-10
- Correctly import "service@" GSS host-based name

* Thu Mar 26 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-9
- Eliminate redundant PKINIT responder invocation

* Thu Mar 26 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-8
- Add finalization safety check to com_err

* Fri Mar 20 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-7
- Add maximum openssl version in preparation for openssl 3

* Tue Mar 17 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-6
- Document client keytab usage

* Tue Mar 03 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-5
- Refresh manually acquired creds from client keytab

* Fri Feb 28 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-4
- Allow deletion of require_auth with LDAP KDB

* Thu Feb 27 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-3
- Allow certauth modules to set hw-authent flag

* Fri Feb 21 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-2
- Fix AS-REQ checking of KDB-modified indicators

* Wed Feb 12 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-1
- New upstream version (1.18)

* Fri Feb 07 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-0.beta2.3
- Don't assume OpenSSL failures are memory errors

* Thu Feb 06 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-0.beta2.2
- Put KDB authdata first

* Fri Jan 31 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-0.beta2.1
- New upstream beta release - 1.18-beta2
- Adjust naming convention for downstream patches

* Fri Jan 10 2020 Robbie Harwood <rharwood@redhat.com> - 1.18-0.beta1.1
- New upstream beta release - 1.18-beta1

* Wed Jan 08 2020 Robbie Harwood <rharwood@redhat.com> - 1.17.1-5
- Fix LDAP policy enforcement of pw_expiration
- Fix handling of invalid CAMMAC service verifier

* Mon Jan 06 2020 Robbie Harwood <rharwood@redhat.com> - 1.17.1-4
- Fix xdr_bytes() strict-aliasing violations

* Fri Jan 03 2020 Robbie Harwood <rharwood@redhat.com> - 1.17.1-3
- Don't warn in kadmin when no policy is specified
- Do not always canonicalize enterprise principals

* Fri Dec 13 2019 Robbie Harwood <rharwood@redhat.com> - 1.17.1-2
- Enable the LMDB backend for the KDB

* Thu Dec 12 2019 Robbie Harwood <rharwood@redhat.com> - 1.17.1-1
- New upstream version - 1.17.1
- Stop building and packaging PDFs

* Fri Dec 06 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-54
- Qualify short hostnames when not using DNS

* Wed Nov 27 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-53
- Various gssalloc fixes

* Thu Nov 21 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-52
- Turns out openssl has an epoch

* Wed Nov 20 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-51
- Fix runtime openssl version to actually propogate

* Wed Nov 20 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-50
- Add runtime openssl version requirement too

* Wed Nov 20 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-49
- Fix kadmin addprinc -randkey -kvno

* Tue Nov 19 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-48
- Use OpenSSL's backported KDFs
- Restore MD4 in FIPS mode (for samba)

* Fri Nov 08 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-47
- Add default_principal_flags to example kdc.conf

* Wed Oct 02 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-46
- Log unknown enctypes as unsupported in KDC

* Wed Sep 25 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-45
- Fix KDC crash when logging PKINIT enctypes (CVE-2019-14844)

* Thu Sep 12 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-44
- Static analyzer appeasement

* Tue Aug 27 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-43
- Simplify krb5_dbe_def_search_enctype()

* Thu Aug 22 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-42
- Update FIPS patches to remove SPAKE

* Thu Aug 15 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-41
- Fix KCM client time offset propagation

* Fri Aug 09 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-40
- Initialize life/rlife in kdcpolicy interface

* Tue Aug 06 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-39
- Fix memory leaks in soft-pkcs11 code

* Tue Jul 30 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-38
- Add soft-pkcs11 and use it for testing

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-36
- Filter enctypes in gss_set_allowable_enctypes()

* Mon Jul 15 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-35
- Don't error on invalid enctypes in keytab
  Resolves: rhbz#1724380

* Tue Jul 02 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-34
- Remove now-unused checksum functions

* Wed Jun 26 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-33
- Fix typo in 3des commit

* Wed Jun 26 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-32
- Remove PKINIT draft9 support (compat with EOL, pre-2008 Windows)

* Mon Jun 10 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-31
- Remove strerror() calls from k5_get_error()

* Fri Jun 07 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-30
- Remove 3des from kdc.conf example

* Mon Jun 03 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-29
- Remove 3DES support

* Mon Jun 03 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-28
- Remove 3des support

* Thu May 30 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-27
- Remove krb5int_c_combine_keys() and no-flags SAM-2 preauth

* Tue May 28 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-26
- Remove support for single-DES and CRC

* Wed May 22 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-25
- Add missing newlines to deprecation warnings
- Switch to upstream's ksu path patch

* Tue May 21 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-24
- Update default krb5kdc mkey manual-entry enctype
- Also update account lockout patch to upstream version

* Mon May 20 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-23
- Test & docs fixes in preparation for DES removal

* Wed May 15 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-22
- Drop krb5_realm_compare() etc. NULL check patches


* Wed May 15 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-21
- Re-provide krb5-kdb-version in -devel as well (IPA wants it)

* Tue May 14 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-20
- (Patch consolidation; hopefully no changes)

* Tue May 14 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-19
- Remove checksum type profile variables

* Fri May 10 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-18
- Pull in 2019-05-02 static analysis updates

* Fri May 03 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-17
- Move krb5-kdb-version provide into krb5-server for freeipa

* Wed May 01 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-16
- Use secure_getenv() where appropriate

* Wed Apr 24 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-15
- Fix us up real nice with rpmlint

* Wed Apr 24 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-14
- Add dns_canonicalize_hostname=fallback support

* Wed Apr 24 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-13
- Check more errors in OpenSSL crypto backend

* Mon Apr 22 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-12
- Fix potential close(-1) in cc_file.c

* Wed Apr 17 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-11
- Remove ovsec_adm_export and confvalidator

* Wed Apr 17 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-10
- Fix config realm change logic in FILE remove_cred

* Thu Apr 11 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-9
- Remove Kerberos v4 support vestiges (including ktany support)

* Thu Apr 11 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-8
- Implement krb5_cc_remove_cred for remaining types
  Resolves: rhbz#1693836

* Mon Apr 01 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-7
- FIPS-aware SPAKE group negotiation

* Mon Feb 25 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-6
- Fix memory leak in 'none' replay cache type
- Silence a coverity warning while we're here.

* Fri Feb 01 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-5
- Update FIPS blocking for RC4

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-3
- enctype logging and explicit_bzero()

* Tue Jan 08 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-2
- New upstream version (1.17)

* Fri Jan 04 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta2.6
- Use openssl's PRNG in FIPS mode

* Fri Jan 04 2019 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta2.5
- Address some optimized-out memset() calls

* Thu Dec 20 2018 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta2.4
- Remove incorrect KDC assertion

* Thu Dec 20 2018 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta2.3
- Fix syntax on pkinit_anchors field in default krb5.conf

* Mon Dec 17 2018 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta2.2
- Restore pdfs source file
  Resolves: rhbz#1659716

* Thu Dec 06 2018 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta2.1
- New upstream release (1.17-beta2)
- Drop pdfs source file

* Thu Nov 29 2018 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta1.3
- Add tests for KCM ccache type

* Mon Nov 12 2018 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta1.2
- Gain FIPS awareness

* Thu Nov 08 2018 Robbie Harwood <rharwood@redhat.com> - 1.17-1.beta1.1
- Fix spurious errors from kcmio_unix_socket_write
  Resolves: rhbz#1645912

* Thu Nov 01 2018 Robbie Harwood <rharwood@redhat.com> - 1.17-0.beta1.1
- New upstream beta release

* Wed Oct 24 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-25
- Update man pages to reference kerberos(7)
  Resolves: rhbz#1143767

* Wed Oct 17 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-24
- Use port-sockets.h macros in cc_kcm, sendto_kdc
  Resolves: rhbz#1631998

* Wed Oct 17 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-23
- Correct kpasswd_server description in krb5.conf(5)
  Resolves: rhbz#1640272

* Mon Oct 15 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-22
- Prefer TCP to UDP for password changes
  Resolves: rhbz#1637611

* Tue Oct 09 2018 Adam Williamson <awilliam@redhat.com> - 1.16.1-21
- Revert the patch from -20 for now as it seems to make FreeIPA worse

* Tue Oct 02 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-20
- Fix bugs with concurrent use of MEMORY ccaches

* Wed Aug 01 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-19
- In FIPS mode, add plaintext fallback for RC4 usages and taint

* Thu Jul 26 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-18
- Fix k5test prompts for Python 3

* Thu Jul 19 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-17
- Remove outdated note in krb5kdc man page

* Thu Jul 19 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-16
- Make krb5kdc -p affect TCP ports

* Thu Jul 19 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-15
- Eliminate preprocessor-disabled dead code

* Wed Jul 18 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-14
- Fix some broken tests for Python 3

* Mon Jul 16 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-13
- Zap copy of secret in RC4 string-to-key

* Thu Jul 12 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-12
- Convert Python tests to Python 3

* Wed Jul 11 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-11
- Add build dependency on gcc

* Tue Jul 10 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-10
- Use SHA-256 instead of MD5 for audit ticket IDs

* Fri Jul 06 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-9
- Add BuildRequires on python2 so we can run tests at build-time

* Fri Jul 06 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-8
- Explicitly look for python2 in configure.in

* Thu Jun 14 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-7
- Add flag to disable encrypted timestamp on client

* Thu Jun 14 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-6
- Switch to python3-sphinx for docs
  Resolves: rhbz#1590928

* Thu Jun 14 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-5
- Make docs build python3-compatible
  Resolves: rhbz#1590928

* Thu Jun 07 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-4
- Update includedir processing to match upstream

* Fri Jun 01 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-3
- Log when non-root ksu authorization fails
  Resolves: rhbz#1575771

* Fri May 04 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-2
- Remove "-nodes" option from make-certs scripts

* Fri May 04 2018 Robbie Harwood <rharwood@redhat.com> - 1.16.1-1
- New upstream release - 1.16.1

* Thu May 03 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-27
- Fix configuration of default ccache name to match file indentation

* Mon Apr 30 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-26
- Set error message on KCM get_princ failure

* Mon Apr 30 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-25
- Set error message on KCM get_princ failure

* Tue Apr 24 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-24
- Fix KDC null dereference on large TGS replies

* Mon Apr 23 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-23
- Explicitly use openssl rather than builtin crypto
  Resolves: rhbz#1570910

* Tue Apr 17 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-22
- Merge duplicate subsections in profile library

* Mon Apr 09 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-21
- Restrict pre-authentication fallback cases

* Tue Apr 03 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-20
- Be more careful asking for AS key in SPAKE client

* Mon Apr 02 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-19
- Zap data when freeing krb5_spake_factor

* Thu Mar 29 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-18
- Continue after KRB5_CC_END in KCM cache iteration

* Tue Mar 27 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-17
- Fix SPAKE memory leak

* Tue Mar 27 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-16
- Fix gitignore problem with previous patchset

* Tue Mar 27 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-15
- Add SPAKE support
- Improve protections on internal sensitive buffers
- Improve internal hex encoding/decoding

* Tue Mar 20 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-14
- Fix problem with ccache_name logic in previous build

* Tue Mar 20 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-13
- Add pkinit_anchors default value to krb5.conf
- Reindent krb5.conf to not be terrible

* Tue Mar 20 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-12
- Log preauth names in trace output
- Misc bugfixes from upstream

* Mon Mar 19 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-11
- Add PKINIT KDC support for freshness token

* Wed Mar 14 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-10
- Exit with status 0 from kadmind

* Tue Mar 13 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-9
- Fix hex conversion of PKINIT certid strings

* Wed Mar 07 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-8
- Fix capaths "." values on client
  Resolves: 1551099

* Tue Feb 13 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-7
- Fix flaws in LDAP DN checking
- CVE-2018-5729, CVE-2018-5730

* Mon Feb 12 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-6
- Fix a leak in the previous commit
- Restore dist macro that was accidentally removed
  Resolves: rhbz#1540939

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.16-4
- Switch to %%ldconfig_scriptlets

* Mon Jan 29 2018 Robbie Harwood <rharwood@redhat.com> - 1.16-3
- Process included directories in alphabetical order

* Tue Dec 12 2017 Robbie Harwood <rharwood@redhat.com> - 1.16-2
- Fix network service dependencies
  Resolves: rhbz#1525230

* Wed Dec 06 2017 Robbie Harwood <rharwood@redhat.com> - 1.16-1
- New upstream release (1.16)
- No changes from beta2

* Mon Nov 27 2017 Robbie Harwood <rharwood@redhat.com> - 1.16-0.beta2.1
- New upstream prerelease (1.16-beta2)

* Tue Oct 24 2017 Robbie Harwood <rharwood@redhat.com> - 1.16-0.beta1.4
- Fix CVE-2017-15088 (Buffer overflow in get_matching_data())

* Mon Oct 23 2017 Robbie Harwood <rharwood@redhat.com> - 1.16-0.beta1.3
- Drop dependency on python2-pyrad (dead upstream, broken with new python)

* Mon Oct 09 2017 Robbie Harwood <rharwood@redhat.com> - 1.16-0.beta1.2
- Actually bump kdbversion like I was supposed to

* Thu Oct 05 2017 Robbie Harwood <rharwood@redhat.com> - 1.16-0.beta1.1
- New upstream prerelease (1.16-beta1)

* Thu Sep 28 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.2-2
- Add German translation

* Mon Sep 25 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.2-1
- New upstream release - krb5-1.15.2
- Adjust patches as appropriate

* Wed Sep 06 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-28
- Save other programs from worrying about CVE-2017-11462
  Resolves: rhbz#1488873
  Resolves: rhbz#1488874

* Tue Sep 05 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-27
- Add hostname-based ccselect module
  Resolves: rhbz#1463665

* Tue Sep 05 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-26
- Backport upstream certauth EKU fixes

* Fri Aug 25 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-25
- Backport certauth eku security fix

* Mon Aug 21 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-24
- Backport kdc policy plugin, but this time with dependencies

* Mon Aug 21 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-23
- Backport kdcpolicy interface

* Wed Aug 16 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-22

* Mon Aug 07 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-21
- Display an error message if ocsp pkinit is requested

* Wed Aug 02 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-20
- Disable dns_canonicalize_hostname.  This may break some setups.

* Wed Aug 02 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-19
- Re-enable test suite on ppc64le (no other changes)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-17
- Fix CVE-2017-11368 (remote triggerable assertion failure)

* Wed Jul 19 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-16
- Explicitly require python2 packages

* Wed Jul 19 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-15
- Add support to query the SSF of a context
- Pick up rename of perl dependency

* Thu Jul 06 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-14
-  Fix leaks in gss_inquire_cred_by_oid()

* Mon Jun 26 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-13
- Fix arch name (ppc64le, not ppc64el)
- Related-to: rhbz#1464381

* Mon Jun 26 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-12
- Skip test suite on ppc64el
- Related-to: rhbz#1464381

* Fri Jun 23 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-11
- Include more test suite changes from upstream
  Resolves: rhbz#1464381

* Wed Jun 07 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-10
- Fix custom build with -DDEBUG

* Wed May 24 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-9
- Use standard trigger logic for krb5 snippet

* Fri Apr 28 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-8
- Add kprop service env config file

* Wed Apr 19 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-7
- Update backports of certauth and corresponding test

* Thu Apr 13 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-6
- Include fixes for previous commit
  Resolves: rhbz#1433083

* Thu Apr 13 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-5
- Automatically add includedir where not present
- Try removing sleep statement to see if it is still needed
  Resolves: rhbz#1433083

* Fri Apr 07 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-4
- Fix use of enterprise principals with forwarding

* Wed Mar 22 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-3
- Backport certauth plugin and related pkinit changes

* Tue Mar 07 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-2
- Remove duplication between subpackages
  Resolves: rhbz#1250228

* Fri Mar 03 2017 Robbie Harwood <rharwood@redhat.com> - 1.15.1-1
- New upstream release - 1.15.1

* Wed Mar 01 2017 Robbie Harwood <rharwood@redhat.com> - 1.15-9
- Patch build by disabling failing test; will fix properly soon

* Fri Feb 17 2017 Robbie Harwood <rharwood@redhat.com> - 1.15-8
- Hammer refresh around transient rawhide issue

* Fri Feb 17 2017 Robbie Harwood <rharwood@redhat.com> - 1.15-7
- Backport fix for GSSAPI fallback realm

* Tue Feb 07 2017 Robbie Harwood <rharwood@redhat.com> - 1.15-6
- Move krb5-kdb-version provides from -libs to -devel

* Fri Jan 20 2017 Robbie Harwood <rharwood@redhat.com> - 1.15-5
- Add free hook to KDB; increments KDB version
- Add KDB version flag

* Mon Dec 05 2016 Robbie Harwood <rharwood@redhat.com> - 1.15-4
- New upstream release

* Wed Nov 16 2016 Robbie Harwood <rharwood@redhat.com> - 1.15-beta2-3
- New upstream release

* Thu Nov 10 2016 Robbie Harwood <rharwood@redhat.com> - 1.15-beta1-2
- Ensure we can build with the new CFLAGS
- Remove the git versioning in patches

* Thu Oct 20 2016 Robbie Harwood <rharwood@redhat.com> - 1.15-beta1-1
- New upstream release
- Update selinux with RHEL hygene
  Resolves: rhbz#1314096

* Tue Oct 11 2016 Tomáš Mráz <tmraz@redhat.com> - 1.14.4-6
- rebuild with OpenSSL 1.1.0, added backported upstream patch

* Fri Sep 30 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.4-5
- Properly close krad sockets
  Resolves: rhbz#1380836

* Fri Sep 30 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.4-4
- Fix backward check in kprop.service

* Fri Sep 30 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.4-3
- Switch to using autosetup macro.
  - Patches come from git, so it is easiest to just make a git repo

* Thu Sep 22 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.4-2
- Backport getrandom() support
- Remove patch numbering

* Mon Sep 19 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.4-1
- New upstream release
- Update names and numbers to match external git

* Mon Sep 19 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-9
- Add krb5_db_register_keytab
  Resolves: rhbz#1376812

* Mon Aug 29 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-8
- Use responder for non-preauth AS requests
  Resolves: rhbz#1370622

* Mon Aug 29 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-7
- Guess Samba client mutual flag using ap_option
  Resolves: rhbz#1370980

* Thu Aug 25 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-6
- Fix KDC return code and set prompt types for OTP client preauth
  Resolves: rhbz#1370072

* Mon Aug 15 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-5
- Turn OFD locks back on with glibc workaround
  Resolves: rhbz#1274922

* Wed Aug 10 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-4
- Fix use of KKDCPP with SNI
  Resolves: rhbz#1365027

* Fri Aug 05 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-3
- Make krb5-devel depend on libkadm5
  Resolves: rhbz#1364487

* Wed Aug 03 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-2
- Up-port a bunch of stuff from the el-7.3 cycle
  Resolves: rhbz#1255450, rhbz#1314989

* Mon Aug 01 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.3-1
- New upstream version 1.14.3

* Thu Jul 28 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-9
- Fix CVE-2016-3120
  Resolves: rhbz#1361051

* Wed Jun 22 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-8
- Fix incorrect recv() size calculation in libkrad

* Thu Jun 16 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-7
- Separate out the kadm5 libs

* Fri May 27 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-6
- Fix setting of AS key in OTP preauth failure

* Tue Apr 05 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-5
- Use the correct patches this time.
  Resolves: rhbz#1321135

* Mon Apr 04 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-4
- Add send/receive sendto_kdc hooks and corresponding tests
  Resolves: rhbz#1321135

* Fri Mar 18 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-3
- Fix CVE-2016-3119 (NULL deref in LDAP module)

* Thu Mar 17 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-2
- Backport OID mech fix
  Resolves: rhbz#1317609

* Mon Feb 29 2016 Robbie Harwood <rharwood@redhat.com> - 1.14.1-1
- New rawhide, new upstream version
- Drop CVE patches
- Rename fix_interposer.patch to acquire_cred_interposer.patch
- Update acquire_cred_interposer.patch to apply to new source

* Mon Feb 22 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-23
- Fix log file permissions patch with our selinux
  Resolves: rhbz#1309421

* Fri Feb 19 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-22
- Backport my interposer fixes from upstream
  - Supersedes krb5-mechglue_inqure_attrs.patch

* Tue Feb 16 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-21
- Adjust dependency on crypto-polices to be just the file we want
- Patch courtesy of lslebodn
  Resolves: rhbz#1308984

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-19
- Replace _kadmin/_kprop with systemd macros
- Remove traces of upstart from fedora package per policy
  Resolves: rhbz#1290185

* Wed Jan 27 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-18
- Fix CVE-2015-8629, CVE-2015-8630, CVE-2015-8631

* Thu Jan 21 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-17
- Make krb5kdc.log not world-readable by default
  Resolves: rhbz#1276484

* Thu Jan 21 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-16
- Allow verification of attributes on krb5.conf

* Wed Jan 20 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-15
- Use "new" systemd macros for service handling.  (Thanks vpavlin!)
  Resolves: rhbz#850399

* Wed Jan 20 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-14
- Remove WITH_NSS macro (always false)
- Remove WITH_SYSTEMD macro (always true)
- Remove WITH_LDAP macro (always true)
- Remove WITH_OPENSSL macro (always true)

* Fri Jan 08 2016 Robbie Harwood <rharwood@redhat.com> - 1.14-13
- Backport fix for chrome crash in spnego_gss_inquire_context
  Resolves: rhbz#1295893

* Wed Dec 16 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-12
- Backport patch to fix mechglue for gss_inqure_attrs_for_mech()

* Thu Dec 03 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-11
- Backport interposer fix (rhbz#1284985)
- Drop workaround pwsize initialization patch (gcc has been fixed)

* Tue Nov 24 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-10
- Fix FTBFS by no longer working around bug in nss_wrapper

* Mon Nov 23 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-9
- Upstream release.  No actual change from beta, just version bump
- Clean up unused parts of spec file

* Mon Nov 16 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-beta2-8
- New upstream beta version

* Wed Nov 04 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-beta1-7
- Patch CVE-2015-2698

* Tue Oct 27 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-beta1-6
- Patch CVE-2015-2697, CVE-2015-2696, CVE-2015-2695

* Thu Oct 22 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-beta1-5
- Ensure pwsize is initialized in chpass_util.c

* Thu Oct 22 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-beta1-4
- Fix typo of crypto-policies file in previous version

* Mon Oct 19 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-beta1-3
- Start using crypto-policies

* Mon Oct 19 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-beta1-2
- TEMPORARILY disable usage of OFD locks as a workaround for x86

* Thu Oct 15 2015 Robbie Harwood <rharwood@redhat.com> - 1.14-beta1-1
- New upstream beta version

* Thu Oct 08 2015 Robbie Harwood <rharwood@redhat.com> - 1.13.2-13
- Work around KDC client prinicipal in referrals issue (rhbz#1259844)

* Thu Oct 01 2015 Robbie Harwood <rharwood@redhat.com> - 1.13.2-12
- Enable building with bad system /etc/krb5.conf

* Wed Sep 23 2015 Robbie Harwood <rharwood@redhat.com> - 1.13.2-11
- Drop dependency on pax, ksh
- Remove support for fedora < 20

* Wed Sep 23 2015 Robbie Harwood <rharwood@redhat.com> - 1.13.2-10
- Nix /usr/share/krb5.conf.d to reduce complexity

* Wed Sep 23 2015 Robbie Harwood <rharwood@redhat.com> - 1.13.2-9
- Depend on crypto-policies which provides /etc/krb5.conf.d (rhbz#1225792)

* Thu Sep 10 2015 Robbie Harwood <rharwood@redhat.com> - 1.13.2-8
- Remove dependency on systemd-sysv which is no longer needed for fedora > 20
  This also fixes a fail-to-build issue.
- Miscalaneous spec cleanup fixes

* Thu Sep 10 2015 Robbie Harwood <rharwood@redhat.com> - 1.13.2-7
- Support config snippets in /etc/krb5.conf.d/ and /usr/share/krb5.conf.d/
  (rhbz#1225792, rhbz#1146370, rhbz#1145808)

* Thu Jun 25 2015 Roland Mainz <rmainz@redhat.com> - 1.13.2-6
- Use system nss_wrapper and socket_wrapper for testing.
  Patch by Andreas Schneider <asn@redhat.com>

* Thu Jun 25 2015 Roland Mainz <rmainz@redhat.com> - 1.13.2-5
- Remove Zanata test glue and related workarounds
  - rhbz#1234292 ("IPA server cannot be run in container due to incorrect /usr/sbin/_kadmind")
  - rhbz#1234326 ("krb5-server introduces new rpm dependency on ksh")

* Thu Jun 18 2015 Roland Mainz <rmainz@redhat.com> - 1.13.2-4
- Fix dependicy on binfmt.service

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 2 2015 Roland Mainz <rmainz@redhat.com> - 1.13.2-2
- Add patch to fix Redhat rhbz#1227542 ("[SELinux] AVC denials may appear
  when kadmind starts"). The issue was caused by an unneeded |htons()|
  which triggered SELinux AVC denials due to the "random" port usage.

* Thu May 21 2015 Roland Mainz <rmainz@redhat.com> - 1.13.2-1
- Add fix for RedHat rhbz#1164304 ("Upstream unit tests loads
  the installed shared libraries instead the ones from the build")

* Thu May 14 2015 Roland Mainz <rmainz@redhat.com> - 1.13.2-0
- Update to krb5-1.13.2
  - drop patch for krb5-1.13.2-CVE_2015_2694_requires_preauth_bypass_in_PKINIT_enabled_KDC, fixed in krb5-1.13.2
  - drop patch for krb5-1.12.1-CVE_2014_5355_fix_krb5_read_message_handling, fixed in krb5-1.13.2
- Add script processing for upcoming Zanata l10n support
- Minor spec cleanup

* Mon May 4 2015 Roland Mainz <rmainz@redhat.com> - 1.13.1-4
- fix for CVE-2015-2694 (rhbz#1216133) "requires_preauth bypass
  in PKINIT-enabled KDC".
  In MIT krb5 1.12 and later, when the KDC is configured with
  PKINIT support, an unauthenticated remote attacker can
  bypass the requires_preauth flag on a client principal and
  obtain a ciphertext encrypted in the principal's long-term
  key.  This ciphertext could be used to conduct an off-line
  dictionary attack against the user's password.

* Wed Mar 25 2015 Roland Mainz <rmainz@redhat.com> - 1.13.1-3
- Add temporay workaround for RH rhbz#1204646 ("krb5-config
  returns wrong -specs path") which modifies krb5-config post
  build so that development of krb5 dependicies gets unstuck.
  This MUST be removed before rawhide becomes F23 ...

* Thu Mar 19 2015 Roland Mainz <rmainz@redhat.com> - 1.13.1-2
- fix for CVE-2014-5355 (rhbz#1193939) "krb5: unauthenticated
  denial of service in recvauth_common() and others"

* Fri Feb 13 2015 Roland Mainz <rmainz@redhat.com> - 1.13.1-1
- Update to krb5-1.13.1
  - drop patch for CVE_2014_5353_fix_LDAP_misused_policy_name_crash, fixed in krb5-1.13.1
  - drop patch for kinit -C loops (MIT/krb5 bug #243), fixed in krb5-1.13.1
  - drop patch for CVEs { 2014-9421, 2014-9422, 2014-9423, 2014-5352 }, fixed in krb5-1.13.1
- Minor spec cleanup

* Wed Feb 4 2015 Roland Mainz <rmainz@redhat.com> - 1.13-8
- fix for CVE-2014-5352 (rhbz#1179856) "gss_process_context_token()
  incorrectly frees context (MITKRB5-SA-2015-001)"
- fix for CVE-2014-9421 (rhbz#1179857) "kadmind doubly frees partial
  deserialization results (MITKRB5-SA-2015-001)"
- fix for CVE-2014-9422 (rhbz#1179861) "kadmind incorrectly
  validates server principal name (MITKRB5-SA-2015-001)"
- fix for CVE-2014-9423 (rhbz#1179863) "libgssrpc server applications
  leak uninitialized bytes (MITKRB5-SA-2015-001)"

* Wed Feb 4 2015 Roland Mainz <rmainz@redhat.com> - 1.13-7
- Remove "python-sphinx-latex" and "tar" from the build requirements
  to fix build failures on F22 machines.
- Minor spec cleanup

* Mon Feb 02 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.13-6
- Support KDC_ERR_MORE_PREAUTH_DATA_REQUIRED (RT#8063)

* Mon Jan 26 2015 Roland Mainz <rmainz@redhat.com> - 1.13-5
- fix for kinit -C loops (rhbz#1184629, MIT/krb5 issue 243, "Do not
  loop on principal unknown errors").
- Added "python-sphinx-latex" to the build requirements
  to fix build failures on F22 machines.

* Thu Dec 18 2014 Roland Mainz <rmainz@redhat.com> - 1.13-4
- fix for CVE-2014-5354 (rhbz#1174546) "krb5: NULL pointer
  dereference when using keyless entries"

* Wed Dec 17 2014 Roland Mainz <rmainz@redhat.com> - 1.13-3
- fix for CVE-2014-5353 (rhbz#1174543) "Fix LDAP misused policy
  name crash"

* Wed Oct 29 2014 Roland Mainz <rmainz@redhat.com> - 1.13-2
- Bump 1%%{?dist} to 2%%{?dist} to workaround RPM sort issue
  which would lead yum updates to treat the last alpha as newer
  than the final version.

* Wed Oct 29 2014 Roland Mainz <rmainz@redhat.com> - 1.13-1
- Update from krb5-1.13-alpha1 to final krb5-1.13
- Removed patch for CVE-2014-5351 (rhbz#1145425) "krb5: current
  keys returned when randomizing the keys for a service principal" -
  now part of upstream sources
- Use patch for glibc |eventfd()| prototype mismatch (rhbz#1147887) only
  for Fedora > 20

* Tue Sep 30 2014 Roland Mainz <rmainz@redhat.com> - 1.13-0.alpha1.3
- fix build failure caused by change of prototype for glibc
  |eventfd()| (rhbz#1147887)

* Mon Sep 29 2014 Roland Mainz <rmainz@redhat.com> - 1.13-0.alpha1.3
- fix for CVE-2014-5351 (rhbz#1145425) "krb5: current keys returned when
  randomizing the keys for a service principal"

* Mon Sep  8 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.13-0.alpha1.3
- fix the problem where the %%license file has been a dangling symlink

* Tue Aug 26 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.13-0.alpha1.2
- kpropd hasn't bothered with -S since 1.11; stop trying to use that flag
  in the systemd unit file

* Fri Aug 22 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.13-0.alpha1.1
- update to 1.13 alpha1
  - drop upstreamed and backported patches

* Wed Aug 20 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.2-3
- pull in upstream fix for an incorrect check on the value returned by a
  strdup() call (rhbz#1132062)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.2-1
- update to 1.12.2
  - drop patch for RT#7820, fixed in 1.12.2
  - drop patch for rhbz#231147, fixed as RT#3277 in 1.12.2
  - drop patch for RT#7818, fixed in 1.12.2
  - drop patch for RT#7836, fixed in 1.12.2
  - drop patch for RT#7858, fixed in 1.12.2
  - drop patch for RT#7924, fixed in 1.12.2
  - drop patch for RT#7926, fixed in 1.12.2
  - drop patches for CVE-2014-4341/CVE-2014-4342, included in 1.12.2
  - drop patch for CVE-2014-4343, included in 1.12.2
  - drop patch for CVE-2014-4344, included in 1.12.2
  - drop patch for CVE-2014-4345, included in 1.12.2
- replace older proposed changes for ksu with backports of the changes
  after review and merging upstream (rhbz#1015559, rhbz#1026099, rhbz#1118347)

* Thu Aug  7 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-14
- incorporate fix for MITKRB5-SA-2014-001 (CVE-2014-4345)

* Mon Jul 21 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-13
- gssapi: pull in upstream fix for a possible NULL dereference
  in spnego (CVE-2014-4344)

* Wed Jul 16 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-12
- gssapi: pull in proposed fix for a double free in initiators (David
  Woodhouse, CVE-2014-4343, rhbz#1117963)

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 1.12.1-11
- fix license handling

* Mon Jul  7 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-10
- pull in fix for denial of service by injection of malformed GSSAPI tokens
  (CVE-2014-4341, CVE-2014-4342, rhbz#1116181)

* Tue Jun 24 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-9
- pull in changes from upstream which add processing of the contents of
  /etc/gss/mech.d/*.conf when loading GSS modules (rhbz#1102839)

* Thu Jun 12 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-8
- pull in fix for building against tcl 8.6 (rhbz#1107061)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Nathaniel McCallum <npmccallum@redhat.com> - 1.12.1-6
- Backport fix for change password requests when using FAST (RT#7868)

* Mon Feb 17 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-5
- spnego: pull in patch from master to restore preserving the OID of the
  mechanism the initiator requested when we have multiple OIDs for the same
  mechanism, so that we reply using the same mechanism OID and the initiator
  doesn't get confused (rhbz#1066000, RT#7858)

* Fri Feb  7 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-4
- pull in patch from master to move the default directory which the KDC uses
  when computing the socket path for a local OTP daemon from the database
  directory (/var/kerberos/krb5kdc) to the newly-added run directory
  (/run/krb5kdc), in line with what we're expecting in 1.13 (RT#7859, more
  of rhbz#1040056 as rhbz#1063905)
- add a tmpfiles.d configuration file to have /run/krb5kdc created at
  boot-time
- own /var/run/krb5kdc

* Fri Jan 31 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-3
- refresh nss_wrapper and add socket_wrapper to the %%check environment

* Fri Jan 31 2014 Nalin Dahyabhai <nalin@redhat.com>
- add currently-proposed changes to teach ksu about credential cache
  collections and the default_ccache_name setting (rhbz#1015559,rhbz#1026099)

* Tue Jan 21 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-2
- pull in multiple changes to allow replay caches to be added to a GSS
  credential store as "rcache"-type credentials (RT#7818/rhbz#7819/rhbz#7836,
  rhbz#1056078/rhbz#1056080)

* Fri Jan 17 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12.1-1
- update to 1.12.1
  - drop patch for RT#7794, included now
  - drop patch for RT#7797, included now
  - drop patch for RT#7803, included now
  - drop patch for RT#7805, included now
  - drop patch for RT#7807, included now
  - drop patch for RT#7045, included now
  - drop patches for RT#7813 and RT#7815, included now
  - add patch to always retrieve the KDC time offsets from keyring caches,
    so that we don't mistakenly interpret creds as expired before their
    time when our clock is ahead of the KDC's (RT#7820, rhbz#1030607)

* Mon Jan 13 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12-11
- update the PIC patch for iaesx86.s to not use ELF relocations to the version
  that landed upstream (RT#7815, rhbz#1045699)

* Thu Jan  9 2014 Nalin Dahyabhai <nalin@redhat.com>
- pass -Wl,--warn-shared-textrel to the compiler when we're creating shared
  libraries

* Thu Jan  9 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12-10
- amend the PIC patch for iaesx86.s to also save/restore ebx in the
  functions where we modify it, because the ELF spec says we need to

* Mon Jan  6 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12-9
- grab a more-commented version of the most recent patch from upstream
  master
- make a guess at making the 32-bit AES-NI implementation sufficiently
  position-independent to not require execmod permissions for libk5crypto
  (more of rhbz#1045699)

* Thu Jan  2 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12-8
- add patch from Dhiru Kholia for the AES-NI implementations to allow
  libk5crypto to be properly marked as not needing an executable stack
  on arches where they're used (rhbz#1045699, and so many others)

* Thu Jan  2 2014 Nalin Dahyabhai <nalin@redhat.com> - 1.12-7
- revert that last change for a bit while sorting out execstack when we
  use AES-NI (rhbz#1045699)

* Thu Dec 19 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-6
- add yasm as a build requirement for AES-NI support, on arches that have
  yasm and AES-NI

* Thu Dec 19 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-5
- pull in fix from master to make reporting of errors encountered by
  the SPNEGO mechanism work better (RT#7045, part of rhbz#1043962)

* Thu Dec 19 2013 Nalin Dahyabhai <nalin@redhat.com>
- update a test wrapper to properly handle things that the new libkrad does,
  and add python-pyrad as a build requirement so that we can run its tests

* Wed Dec 18 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-4
- revise previous patch to initialize one more element

* Wed Dec 18 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-3
- backport fixes to krb5_copy_context (RT#7807, rhbz#1044735/rhbz#1044739)

* Wed Dec 18 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-2
- pull in fix from master to return a NULL pointer rather than allocating
  zero bytes of memory if we read a zero-length input token (RT#7794, part of
  rhbz#1043962)
- pull in fix from master to ignore an empty token from an acceptor if
  we've already finished authenticating (RT#7797, part of rhbz#1043962)
- pull in fix from master to avoid a memory leak when a mechanism's
  init_sec_context function fails (RT#7803, part of rhbz#1043962)
- pull in fix from master to avoid a memory leak in a couple of error
  cases which could occur while obtaining acceptor credentials (RT#7805, part
  of rhbz#1043962)

* Wed Dec 11 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-1
- update to 1.12 final

* Mon Dec  2 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-beta2.0
- update to beta2
  - drop obsolete backports for storing KDC time offsets and expiration times
    in keyring credential caches

* Tue Nov 19 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-beta1.0
- rebase to master
- update to beta1
  - drop obsolete backport of fix for RT#7706

* Mon Nov 18 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.4-2
- pull in fix to store KDC time offsets in keyring credential caches (RT#7768,
  rhbz#1030607)
- pull in fix to set expiration times on credentials stored in keyring
  credential caches (RT#7769, rhbz#1031724)

* Tue Nov 12 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.4-1
- update to 1.11.4
  - drop patch for RT#7650, obsoleted
  - drop patch for RT#7706, obsoleted as RT#7723
  - drop patch for CVE-2013-1418/CVE-2013-6800, included in 1.11.4

* Tue Nov 12 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-31
- switch to the simplified version of the patch for rhbz#1029110 (RT#7764)

* Mon Nov 11 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-30
- check more thoroughly for errors when resolving KEYRING ccache names of type
  "persistent", which should only have a numeric UID as the next part of the
  name (rhbz#1029110)

* Tue Nov  5 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-29
- incorporate upstream patch for remote crash of KDCs which serve multiple
  realms simultaneously (RT#7756, CVE-2013-1418/CVE-2013-6800,
  rhbz#1026997/rhbz#1031501)

* Mon Nov  4 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-28
- drop patch to add additional access() checks to ksu - they add to breakage
  when non-FILE: caches are in use (rhbz#1026099), shouldn't be resulting in any
  benefit, and clash with proposed changes to fix its cache handling

* Tue Oct 22 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-27
- add some minimal description to the top of the wrapper scripts we use
  when starting krb5kdc and kadmind to describe why they exist (tooling)

* Thu Oct 17 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.12-alpha1.0
- initial update to alpha1
  - drop backport of persistent keyring support
  - drop backport for RT#7689
  - drop obsolete patch for fixing a use-before-init in a test program
  - drop obsolete patch teaching config.guess/config.sub about aarch64-linux
  - drop backport for RT#7598
  - drop backport for RT#7172
  - drop backport for RT#7642
  - drop backport for RT#7643
  - drop patches from master to not test GSSRPC-over-UDP and to not
    depend on the portmapper, which are areas where our build systems
    often give us trouble, too; obsolete
  - drop backports for RT#7682
  - drop backport for RT#7709
  - drop backport for RT#7590 and partial backport for RT#7680
  - drop OTP backport
  - drop backports for RT#7656 and RT#7657
- BuildRequires: libedit-devel to prefer it
- BuildRequires: pkgconfig, since configure uses it

* Wed Oct 16 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-26
- create and own /etc/gss (rhbz#1019937)

* Tue Oct 15 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-25
- pull up fix for importing previously-exported credential caches in the
  gssapi library (RT# 7706, rhbz#1019420)

* Mon Oct 14 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-24
- backport the callback to use the libkrb5 prompter when we can't load PEM
  files for PKINIT (RT#7590, includes part of rhbz#965721/rhbz#1016690)
- extract the rest of the fix rhbz#965721/rhbz#1016690 from the changes for RT#7680

* Mon Oct 14 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-23
- fix trigger scriptlet's invocation of sed (rhbz#1016945)

* Fri Oct  4 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-22
- rebuild with keyutils 1.5.8 (part of rhbz#1012043)

* Wed Oct  2 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-21
- switch to the version of persistent-keyring that was just merged to
  master (RT#7711), along with related changes to kinit (RT#7689)
- go back to setting default_ccache_name to a KEYRING type

* Mon Sep 30 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-20
- pull up fix for not calling a kdb plugin's check-transited-path
  method before calling the library's default version, which only knows
  how to read what's in the configuration file (RT#7709, rhbz#1013664)

* Thu Sep 26 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-19
- configure --without-krb5-config so that we don't pull in the old default
  ccache name when we want to stop setting a default ccache name at configure-
  time

* Wed Sep 25 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-18
- fix broken dependency on awk (should be gawk, rdieter)

* Wed Sep 25 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-17
- add missing dependency on newer keyutils-libs (rhbz#1012034)

* Tue Sep 24 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-16
- back out setting default_ccache_name to the new default for now, resetting
  it to the old default while the kernel/keyutils bits get sorted (sgallagh)

* Mon Sep 23 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-15
- add explicit build-time dependency on a version of keyutils that's new
  enough to include keyctl_get_persistent() (more of rhbz#991148)

* Thu Sep 19 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-14
- incorporate Simo's updated backport of his updated persistent-keyring changes
  (more of rhbz#991148)

* Fri Sep 13 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-13
- don't break during %%check when the session keyring is revoked

* Fri Sep 13 2013 Nalin Dahyabhai <nalin@redhat.com> - 1.11.3-12
- pull the newer F21 defaults back to F20 (sgallagh)

* Mon Sep  9 2013 Nalin Dahyabhai <nalin@redhat.com>
- only apply the patch to autocreate /run/user/0 when we're hard-wiring the
  default ccache location to be under it; otherwise it's unnecessary

* Mon Sep  9 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-11
- don't let comments intended for one scriptlet become part of the "script"
  that gets passed to ldconfig as part of another one (Mattias Ellert, rhbz#1005675)

* Fri Sep  6 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-10
- incorporate Simo's backport of his persistent-keyring changes (rhbz#991148)
- restore build-time default DEFCCNAME on Fedora 21 and later and EL, and
  instead set default_ccache_name in the default krb5.conf's [libdefaults]
  section (rhbz#991148)
- on releases where we expect krb5.conf to be configured with a
  default_ccache_name, add it whenever we upgrade from an older version of
  the package that wouldn't have included it in its default configuration
  file (rhbz#991148)

* Fri Aug 23 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-9
- take another stab at accounting for UnversionedDocdirs for the -libs
  subpackage (spotted by ssorce)
- switch to just the snapshot of nss_wrapper we were using, since we
  no longer need to carry anything that isn't in the cwrap.org repository
  (ssorce)

* Thu Aug 15 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-8
- drop a patch we weren't not applying (build tooling)
- wrap kadmind and kpropd in scripts which check for the presence/absence
  of files which dictate particular exit codes before exec'ing the actual
  binaries, instead of trying to use ConditionPathExists in the unit files
  to accomplish that, so that we exit with failure properly when what we
  expect isn't actually in effect on the system (rhbz#800343)

* Mon Jul 29 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-7
- attempt to account for UnversionedDocdirs for the -libs subpackage

* Fri Jul 26 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-6
- tweak configuration files used during tests to try to reduce the number
  of conflicts encountered when builds for multiple arches land on the same
  builder

* Mon Jul 22 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-5
- pull up changes to allow GSSAPI modules to provide more functions
  (RT#7682, rhbz#986564/rhbz#986565)

* Fri Jul 19 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-4
- use (a bundled, for now, copy of) nss_wrapper to let us run some of the
  self-tests at build-time in more places than we could previously (rhbz#978756)
- cover inconsistencies in whether or not there's a local caching nameserver
  that's willing to answer when the build environment doesn't have a
  resolver configuration, so that nss_wrapper's faking of the local
  hostname can be complete

* Mon Jul  1 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-3
- specify dependencies on the same arch of krb5-libs by using the %%{?_isa}
  suffix, to avoid dragging 32-bit libraries onto 64-bit systems (rhbz#980155)

* Thu Jun 13 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-2
- special-case /run/user/0, attempting to create it when resolving a
  directory cache below it fails due to ENOENT and we find that it doesn't
  already exist, either, before attempting to create the directory cache
  (maybe helping, maybe just making things more confusing for rhbz#961235)

* Tue Jun  4 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.3-1
- update to 1.11.3
  - drop patch for RT#7605, fixed in this release
  - drop patch for CVE-2002-2443, fixed in this release
  - drop patch for RT#7369, fixed in this release
- pull upstream fix for breaking t_skew.py by adding the patch for rhbz#961221

* Fri May 31 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-10
- respin with updated version of patch for RT#7650 (rhbz#969331)

* Thu May 30 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-9
- don't forget to set the SELinux label when creating the directory for
  a DIR: ccache
- pull in proposed fix for attempts to get initial creds, which end up
  following referrals, incorrectly trying to always use master KDCs if
  they talked to a master at any point (should fix RT#7650)

* Thu May 30 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-8
- pull in patches from master to not test GSSRPC-over-UDP and to not
  depend on the portmapper, which are areas where our build systems
  often give us trouble, too

* Tue May 28 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-7
- backport fix for not being able to verify the list of transited realms
  in GSS acceptors (RT#7639, rhbz#959685)
- backport fix for not being able to pass an empty password to the
  get-init-creds APIs and have them actually use it (RT#7642, rhbz#960001)
- add backported proposed fix to use the unauthenticated server time
  as the basis for computing the requested credential expiration times,
  rather than the client's idea of the current time, which could be
  significantly incorrect (rhbz#961221)

* Tue May 21 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-6
- pull in upstream fix to start treating a KRB5CCNAME value that begins
  with DIR:: the same as it would a DIR: value with just one ccache file
  in it (RT#7172, rhbz#965574)

* Mon May 13 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-5
- pull up fix for UDP ping-pong flaw in kpasswd service (CVE-2002-2443,
  rhbz#962531,rhbz#962534)

* Mon Apr 29 2013 Nathaniel McCallum <npmccallum@redhat.com> 1.11.2-4
- Update otp patches
- Merge otp patches into a single patch
- Add keycheck patch

* Tue Apr 23 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-3
- pull the changing of the compiled-in default ccache location to
  DIR:/run/user/%%{uid}/krb5cc back into F19, in line with SSSD and
  the most recent pam_krb5 build

* Wed Apr 17 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-2
- correct some configuration file paths which the KDC_DIR patch missed

* Mon Apr 15 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.2-1
- update to 1.11.2
  - drop pulled in patch for RT#7586, included in this release
  - drop pulled in patch for RT#7592, included in this release
- pull in fix for keeping track of the message type when parsing FAST requests
  in the KDC (RT#7605, rhbz#951843) (also rhbz#951965)

* Fri Apr 12 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.1-9
- move the compiled-in default ccache location from the previous default of
  FILE:/tmp/krb5cc_%%{uid} to DIR:/run/user/%%{uid}/krb5cc (part of rhbz#949588)

* Tue Apr 09 2013 Nathaniel McCallum <npmccallum@redhat.com> - 1.11.1-8
- Update otp backport patches (libk5radius => libkrad)

* Wed Apr  3 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.1-7
- when testing the RPC library, treat denials from the local portmapper the
  same as a portmapper-not-running situation, to allow other library tests
  to be run while building the package

* Thu Mar 28 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.1-6
- create and own /var/kerberos/krb5/user instead of /var/kerberos/kdc/user,
  since that's what the libraries actually look for
- add buildrequires on nss-myhostname, in an attempt to get more of the tests
  to run properly during builds
- pull in Simo's patch to recognize "client_keytab" as a key type which can
  be passed in to gss_acquire_cred_from() (RT#7598)

* Tue Mar 26 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.1-5
- pull up Simo's patch to mark the correct mechanism on imported GSSAPI
  contexts (RT#7592)
- go back to using reconf to run autoconf and autoheader (part of rhbz#925640)
- add temporary patch to use newer config.guess/config.sub (more of rhbz#925640)

* Mon Mar 18 2013 Nalin Dahyabhai <nalin@redhat.com>
- fix a version comparison to expect newer texlive build requirements when
  %%{_rhel} > 6 rather than when it's > 7

* Mon Mar 11 2013 Nathaniel McCallum <npmccallum@redhat.com> 1.11.1-4
- Add libverto-devel requires for krb5-devel
- Add otp support

* Thu Feb 28 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.1-3
- fix a memory leak when acquiring credentials using a keytab (RT#7586, rhbz#911110)

* Wed Feb 27 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.1-2
- prebuild PDF docs to reduce multilib differences (internal tooling, rhbz#884065)
- drop the kerberos-iv portreserve file, and drop the rest on systemd systems
- escape uses of macros in comments (more of rhbz#884065)

* Mon Feb 25 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11.1-1
- update to 1.11.1
  - drop patch for noticing negative timeouts being passed to the poll()
    wrapper in the client transmit functions

* Fri Feb  8 2013 Nalin Dahyabhai <nalin@redhat.com> 1.11-2
- set "rdns = false" in the default krb5.conf (rhbz#908323,rhbz#908324)

* Tue Dec 18 2012 Nalin Dahyabhai <nalin@redhat.com> 1.11-1
- update to 1.11 release

* Thu Dec 13 2012 Nalin Dahyabhai <nalin@redhat.com> 1.11-0.beta2.0
- update to 1.11 beta 2

* Thu Dec 13 2012 Nalin Dahyabhai <nalin@redhat.com>
- when building with our bundled copy of libverto, package it in with -libs
  rather than with -server (rhbz#886049)

* Wed Nov 21 2012 Nalin Dahyabhai <nalin@redhat.com> 1.11-0.beta1.0
- update to 1.11 beta 1

* Fri Nov 16 2012 Nalin Dahyabhai <nalin@redhat.com> 1.11-0.alpha1.1
- handle releases where texlive packaging wasn't yet as complicated as it
  is in Fedora 18
- fix an uninitialized-variable error building one of the test programs

* Fri Nov 16 2012 Nalin Dahyabhai <nalin@redhat.com> 1.11-0.alpha1.0
- move the rather large pile of html and pdf docs to -workstation, so
  that just having something that links to the libraries won't drag
  them onto a system, and we avoid having to sort out hard-coded paths
  that include %%{_libdir} showing up in docs in multilib packages
- actually create %%{_var}/kerberos/kdc/user, so that it can be packaged
- correct the list of packaged man pages
- don't dummy up required tex stylesheets, require them
- require pdflatex and makeindex

* Thu Nov 15 2012 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.11 alpha 1
  - drop backported patch for RT rhbz#7406
  - drop backported patch for RT rhbz#7407
  - drop backported patch for RT rhbz#7408
  - the new docs system generates PDFs, so stop including them as sources
  - drop backported patch to allow deltat.y to build with the usual
    warning flags and the current gcc
  - drop backported fix for disabling use of a replay cache when verifying
    initial credentials
  - drop backported fix for teaching PKINIT clients which trust the KDC's
    certificate directly to verify signed-data messages that are signed with
    the KDC's certificate, when the blobs don't include a copy of the KDC's
    certificate
  - drop backported patches to make keytab-based authentication attempts
    work better when the client tells the KDC that it supports a particular
    cipher, but doesn't have a key for it in the keytab
  - drop backported fix for avoiding spurious clock skew when a TGT is
    decrypted long after the KDC sent it to the client which decrypts it
  - move the cross-referenced HTML docs into the -libs package to avoid
    broken internal links
  - drop patches to fixup paths in man pages, shouldn't be needed any more

* Wed Oct 17 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.3-7
- tag a couple of other patches which we still need to be applied during
  %%{?_rawbuild} builds (zmraz)

* Tue Sep 25 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.3-6
- actually pull up the patch for RT#7063, and not some other ticket (rhbz#773496)

* Mon Sep 10 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.3-5
- add patch based on one from Filip Krska to not call poll() with a negative
  timeout when the caller's intent is for us to just stop calling it (rhbz#838548)

* Fri Sep  7 2012 Nalin Dahyabhai <nalin@redhat.com>
- on EL6, conflict with libsmbclient before 3.5.10-124, which is when it
  stopped linking with a symbol which we no longer export (rhbz#771687)
- pull up patch for RT#7063, in which not noticing a prompt for a long
  time throws the client library's idea of the time difference between it
  and the KDC really far out of whack (rhbz#773496)
- add a backport of more patches to set the client's list of supported enctypes
  when using a keytab to be the list of types of keys in the keytab, plus the
  list of other types the client supports but for which it doesn't have keys,
  in that order, so that KDCs have a better chance of being able to issue
  tickets with session keys of types that the client can use (rhbz#837855)

* Thu Sep  6 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.3-4
- cut down the number of times we load SELinux labeling configuration from
  a minimum of two times to actually one (more of rhbz#845125)

* Thu Aug 30 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.3-3
- backport patch to disable replay detection in krb5_verify_init_creds()
  while reading the AP-REQ that's generated in the same function (RT#7229)

* Thu Aug 30 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.3-2
- undo rename from krb5-pkinit-openssl to krb5-pkinit on EL6
- version the Obsoletes: on the krb5-pkinit-openssl to krb5-pkinit rename
- reintroduce the init scripts for non-systemd releases
- forward-port %%{?_rawbuild} annotations from EL6 packaging

* Thu Aug  9 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.3-1
- update to 1.10.3, rolling in the fixes from MITKRB5-SA-2012-001

* Thu Aug  2 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.2-7
- selinux: hang on to the list of selinux contexts, freeing and reloading
  it only when the file we read it from is modified, freeing it when the
  shared library is being unloaded (rhbz#845125)

* Thu Aug  2 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.2-6
- go back to not messing with library file paths on Fedora 17: it breaks
  file path dependencies in other packages, and since Fedora 17 is already
  released, breaking that is our fault

* Tue Jul 31 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.2-5
- add upstream patch to fix freeing an uninitialized pointer and dereferencing
  another uninitialized pointer in the KDC (MITKRB5-SA-2012-001, CVE-2012-1014
  and CVE-2012-1015, rhbz#844779 and rhbz#844777)
- fix a thinko in whether or not we mess around with devel .so symlinks on
  systems without a separate /usr (sbose)

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.2-3
- backport a fix to allow a PKINIT client to handle SignedData from a KDC
  that's signed with a certificate that isn't in the SignedData, but which
  is available as an anchor or intermediate on the client (RT#7183)

* Tue Jun  5 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.2-2
- back out this labeling change (dwalsh):
  - when building the new label for a file we're about to create, also mix
    in the current range, in addition to the current user

* Fri Jun  1 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.2-1
- update to 1.10.2
  - when building the new label for a file we're about to create, also mix
    in the current range, in addition to the current user
  - also package the PDF format admin, user, and install guides
  - drop some PDFs that no longer get built right
- add a backport of Stef's patch to set the client's list of supported
  enctypes to match the types of keys that we have when we are using a
  keytab to try to get initial credentials, so that a KDC won't send us
  an AS reply that we can't encrypt (RT#2131, rhbz#748528)
- don't shuffle around any shared libraries on releases with no-separate-/usr,
  since /usr/lib is the same place as /lib
- add explicit buildrequires: on 'hostname', for the tests, on systems where
  it's in its own package, and require net-tools, which used to provide the
  command, everywhere

* Mon May  7 2012 Nalin Dahyabhai <nalin@redhat.com>
- skip the setfscreatecon() if fopen() is passed "rb" as the open mode (part
  of rhbz#819115)

* Tue May  1 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.1-3
- have -server require /usr/share/dict/words, which we set as the default
  dict_file in kdc.conf (rhbz#817089)

* Tue Mar 20 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.1-2
- change back dns_lookup_kdc to the default setting (Stef Walter, rhbz#805318)
- comment out example.com examples in default krb5.conf (Stef Walter, rhbz#805320)

* Fri Mar  9 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10.1-1
- update to 1.10.1
  - drop the KDC crash fix
  - drop the KDC lookaside cache fix
  - drop the fix for kadmind RPC ACLs (CVE-2012-1012)

* Wed Mar  7 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-5
- when removing -workstation, remove our files from the info index while
  the file is still there, in %%preun, rather than %%postun, and use the
  compressed file's name (rhbz#801035)

* Tue Feb 21 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.10-4
- Fix string RPC ACLs (RT#7093); CVE-2012-1012

* Tue Jan 31 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.10-3
- Add upstream lookaside cache behavior fix (RT#7082)

* Mon Jan 30 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-2
- add patch to accept keytab entries with vno==0 as matches when we're
  searching for an entry with a specific name/kvno (rhbz#230382/rhbz#782211,RT#3349)

* Mon Jan 30 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-1
- update to 1.10 final

* Thu Jan 26 2012 Nathaniel McCallum <nathaniel@natemccallum.com> - 1.10-0.beta1.2
- Add upstream crashfix patch (RT#7081)

* Thu Jan 12 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.beta1.1
- update to beta 1

* Wed Jan 11 2012 Peter Robinson <pbrobinson@gmail.com>
- mktemp was long obsoleted by coreutils

* Wed Jan  4 2012 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha2.2
- modify the deltat grammar to also tell gcc (4.7) to suppress
  "maybe-uninitialized" warnings in addition to the "uninitialized" warnings
  it's already being told to suppress (RT#7080)

* Tue Dec 20 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha2.1
- update to alpha 2
- drop a couple of patches which were integrated for alpha 2

* Tue Dec 13 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha1.3
- pull in patch for RT#7046: tag a ccache containing credentials obtained via
  S4U2Proxy with the principal name of the proxying principal (part of rhbz#761317)
  so that the default principal name can be set to that of the client for which
  it is proxying, which results in the ccache looking more normal to consumers
  of the ccache that don't care that there's proxying going on
- pull in patch for RT#7047: allow tickets obtained via S4U2Proxy to be cached
  (more of rhbz#761317)
- pull in patch for RT#7048: allow PAC verification to only bother trying to
  verify the signature with keys that it's given (still more of rhbz#761317)

* Tue Dec  6 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha1.2
- apply upstream patch to fix a null pointer dereference when processing
  TGS requests (CVE-2011-1530, rhbz#753748)

* Wed Nov 30 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha1.1
- correct a bug in the fix for rhbz#754001 so that the file creation context is
  consistently reset

* Tue Nov 15 2011 Nalin Dahyabhai <nalin@redhat.com> 1.10-0.alpha1.0
- update to 1.10 alpha 1
- on newer releases where we can assume NSS >= 3.13, configure PKINIT to build
  using NSS
- on newer releases where we build PKINIT using NSS, configure libk5crypto to
  build using NSS
- rename krb5-pkinit-openssl to krb5-pkinit on newer releases where we're
  expecting to build PKINIT using NSS instead
- during %%check, run check in the library and kdc subdirectories, which
  should be able to run inside of the build system without issue

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-19
- Rebuilt for glibc rhbz#747377

* Tue Oct 18 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-18
- apply upstream patch to fix a null pointer dereference with the LDAP kdb
  backend (CVE-2011-1527, rhbz#744125), an assertion failure with multiple kdb
  backends (CVE-2011-1528), and a null pointer dereference with multiple kdb
  backends (CVE-2011-1529) (rhbz#737711)

* Thu Oct 13 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-17
- pull in patch from trunk to rename krb5int_pac_sign() to krb5_pac_sign() and
  make it public (rhbz#745533)

* Fri Oct  7 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-16
- kadmin.service: fix rhbz#723723 again
- kadmin.service,krb5kdc.service: remove optional use of $KRB5REALM in command
  lines, because systemd parsing doesn't handle alternate value shell variable
  syntax
- kprop.service: add missing Type=forking so that systemd doesn't assume simple
- kprop.service: expect the ACL configuration to be there, not absent
- handle a harder-to-trigger assertion failure that starts cropping up when we
  exit the transmit loop on time (rhbz#739853)

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> 1.9.1-15
- hardcode pid file as option in krb5kdc.service

* Fri Sep 30 2011 Tom Callaway <spot@fedoraproject.org> 1.9.1-14
- fix pid path in krb5kdc.service

* Mon Sep 19 2011 Tom Callaway <spot@fedoraproject.org> 1.9.1-13
- convert to systemd

* Tue Sep  6 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-12
- pull in upstream patch for RT#6952, confusion following referrals for
  cross-realm auth (rhbz#734341)
- pull in build-time deps for the tests

* Thu Sep  1 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-11
- switch to the upstream patch for rhbz#727829

* Wed Aug 31 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-10
- handle an assertion failure that starts cropping up when the patch for
  using poll (rhbz#701446) meets servers that aren't running KDCs or against
  which the connection fails for other reasons (rhbz#727829, rhbz#734172)

* Mon Aug  8 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-9
- override the default build rules to not delete temporary y.tab.c files,
  so that they can be packaged, allowing debuginfo files which point to them
  do so usefully (rhbz#729044)

* Fri Jul 22 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-8
- build shared libraries with partial RELRO support (rhbz#723995)
- filter out potentially multiple instances of -Wl,-z,relro from krb5-config
  output, now that it's in the buildroot's default LDFLAGS
- pull in a patch to fix losing track of the replay cache FD, from SVN by
  way of Kevin Coffman

* Wed Jul 20 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-7
- kadmind.init: drop the attempt to detect no-database-present errors (rhbz#723723),
  which is too fragile in cases where the database has been manually moved or
  is accessed through another kdb plugin

* Tue Jul 19 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-6
- backport fixes to teach libkrb5 to use descriptors higher than FD_SETSIZE
  to talk to a KDC by using poll() if it's detected at compile-time (rhbz#701446,
  RT#6905)

* Thu Jun 23 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-5
- pull a fix from SVN to try to avoid triggering a PTR lookup in getaddrinfo()
  during krb5_sname_to_principal(), and to let getaddrinfo() decide whether or
  not to ask for an IPv6 address based on the set of configured interfaces
  (rhbz#717378, RT#6922)
- pull a fix from SVN to use AI_ADDRCONFIG more often (RT#6923)

* Mon Jun 20 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-4
- apply upstream patch by way of Burt Holzman to fall back to a non-referral
  method in cases where we might be derailed by a KDC that rejects the
  canonicalize option (for example, those from the RHEL 2.1 or 3 era) (rhbz#715074)

* Tue Jun 14 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-3
- pull a fix from SVN to get libgssrpc clients (e.g. kadmin) authenticating
  using the old protocol over IPv4 again (RT#6920)

* Tue Jun 14 2011 Nalin Dahyabhai <nalin@redhat.com>
- incorporate a fix to teach the file labeling bits about when replay caches
  are expunged (rhbz#576093)

* Thu May 26 2011 Nalin Dahyabhai <nalin@redhat.com>
- switch to the upstream patch for rhbz#707145

* Wed May 25 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-2
- klist: don't trip over referral entries when invoked with -s (rhbz#707145,
  RT#6915)

* Fri May  6 2011 Nalin Dahyabhai <nalin@redhat.com>
- fixup URL in a comment
- when built with NSS, require 3.12.10 rather than 3.12.9

* Thu May  5 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9.1-1
- update to 1.9.1:
  - drop no-longer-needed patches for CVE-2010-4022, CVE-2011-0281,
    CVE-2011-0282, CVE-2011-0283, CVE-2011-0284, CVE-2011-0285

* Wed Apr 13 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-9
- kadmind: add upstream patch to fix free() on an invalid pointer (rhbz#696343,
  MITKRB5-SA-2011-004, CVE-2011-0285)

* Mon Apr  4 2011 Nalin Dahyabhai <nalin@redhat.com>
- don't discard the error code from an error message received in response
  to a change-password request (rhbz#658871, RT#6893)

* Fri Apr  1 2011 Nalin Dahyabhai <nalin@redhat.com>
- override INSTALL_SETUID at build-time so that ksu is installed into
  the buildroot with the right permissions (part of rhbz#225974)

* Fri Mar 18 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-8
- backport change from SVN to fix a computed-value-not-used warning in
  kpropd (rhbz#684065)

* Tue Mar 15 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-7
- turn off NSS as the backend for libk5crypto for now to work around its
  DES string2key not working (rhbz#679012)
- add revised upstream patch to fix double-free in KDC while returning
  typed-data with errors (MITKRB5-SA-2011-003, CVE-2011-0284, rhbz#674325)

* Thu Feb 17 2011 Nalin Dahyabhai <nalin@redhat.com>
- throw in a not-applied-by-default patch to try to make pkinit debugging
  into a run-time boolean option named "pkinit_debug"

* Wed Feb 16 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-6
- turn on NSS as the backend for libk5crypto, adding nss-devel as a build
  dependency when that switch is flipped

* Wed Feb  9 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-5
- krb5kdc init script: prototype some changes to do a quick spot-check
  of the TGS and kadmind keys and warn if there aren't any non-weak keys
  on file for them (to flush out parts of rhbz#651466)

* Tue Feb  8 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-4
- add upstream patches to fix standalone kpropd exiting if the per-client
  child process exits with an error (MITKRB5-SA-2011-001), a hang or crash
  in the KDC when using the LDAP kdb backend, and an uninitialized pointer
  use in the KDC (MITKRB5-SA-2011-002) (CVE-2010-4022, rhbz#664009,
  CVE-2011-0281, rhbz#668719, CVE-2011-0282, rhbz#668726, CVE-2011-0283, rhbz#676126)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Nalin Dahyabhai <nalin@redhat.com>
- fix a compile error in the SELinux labeling patch when -DDEBUG is used (Sumit
  Bose)

* Tue Feb  1 2011 Nalin Dahyabhai <nalin@redhat.com>
- properly advertise that the kpropd init script now supports force-reload
  (Zbysek Mraz, rhbz#630587)

* Wed Jan 26 2011 Nalin Dahyabhai <nalin@redhat.com> 1.9-2
- pkinit: when verifying signed data, use the CMS APIs for better
  interoperability (rhbz#636985, RT#6851)

* Wed Dec 22 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-1
- update to 1.9 final

* Mon Dec 20 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta3.1
- fix link flags and permissions on shared libraries (ausil)

* Thu Dec 16 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta3.0
- update to 1.9 beta 3

* Mon Dec  6 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta2.0
- update to 1.9 beta 2

* Tue Nov  9 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta1.1
- drop not-needed-since-1.8 build dependency on rsh (ssorce)

* Fri Nov  5 2010 Nalin Dahyabhai <nalin@redhat.com> 1.9-0.beta1.0
- start moving to 1.9 with beta 1
  - drop patches for RT#5755, RT#6762, RT#6774, RT#6775
  - drop no-longer-needed backport patch for rhbz#539423
  - drop no-longer-needed patch for CVE-2010-1322
- if WITH_NSS is set, built with --with-crypto-impl=nss (requires NSS 3.12.9)

* Tue Oct  5 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-8
- incorporate upstream patch to fix uninitialized pointer crash in the KDC's
  authorization data handling (CVE-2010-1322, rhbz#636335)

* Mon Oct  4 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-7
- rebuild

* Mon Oct  4 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-6
- pull down patches from trunk to implement k5login_authoritative and
  k5login_directory settings for krb5.conf (rhbz#539423)

* Wed Sep 29 2010 jkeating - 1.8.3-5
- Rebuilt for gcc rhbz#634757

* Wed Sep 15 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-4
- fix reading of keyUsage extensions when attempting to select pkinit client
  certs (part of rhbz#629022, RT#6775)
- fix selection of pkinit client certs when one or more don't include a
  subjectAltName extension (part of rhbz#629022, RT#6774)

* Fri Sep  3 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-3
- build with -fstack-protector-all instead of the default -fstack-protector,
  so that we add checking to more functions (i.e., all of them) (rhbz#629950)
- also link binaries with -Wl,-z,relro,-z,now (part of rhbz#629950)

* Tue Aug 24 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-2
- fix a logic bug in computing key expiration times (RT#6762, rhbz#627022)

* Wed Aug  4 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.3-1
- update to 1.8.3
  - drop backports of fixes for gss context expiration and error table
    registration/deregistration mismatch
  - drop patch for upstream rhbz#6750

* Wed Jul  7 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-3
- tell krb5kdc and kadmind to create pid files, since they can
- add logrotate configuration files for krb5kdc and kadmind (rhbz#462658)
- fix parsing of the pidfile option in the KDC (upstream rhbz#6750)

* Mon Jun 21 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-2
- libgssapi: pull in patch from svn to stop returning context-expired errors
  when the ticket which was used to set up the context expires (rhbz#605366,
  upstream rhbz#6739)

* Mon Jun 21 2010 Nalin Dahyabhai <nalin@redhat.com>
- pull up fix for upstream rhbz#6745, in which the gssapi library would add the
  wrong error table but subsequently attempt to unload the right one

* Thu Jun 10 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-1
- update to 1.8.2
  - drop patches for CVE-2010-1320, CVE-2010-1321

* Tue Jun  1 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-7
- rebuild

* Thu May 27 2010 Nalin Dahyabhai <nalin@redhat.com>
- ksu: move session management calls to before we drop privileges, like
  su does (rhbz#596887), and don't skip the PAM account check for root or the
  same user (more of rhbz#540769)

* Mon May 24 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-6
- make krb5-server-ldap also depend on the same version-release of krb5-libs,
  as the other subpackages do, if only to make it clearer than it is when we
  just do it through krb5-server
- drop explicit linking with libtinfo for applications that use libss, now
  that readline itself links with libtinfo (as of readline-5.2-3, since
  fedora 7 or so)
- go back to building without strict aliasing (compiler warnings in gssrpc)

* Tue May 18 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-5
- add patch to correct GSSAPI library null pointer dereference which could be
  triggered by malformed client requests (CVE-2010-1321, rhbz#582466)

* Tue May  4 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-4
- fix output of kprop's init script's "status" and "reload" commands (rhbz#588222)

* Tue Apr 20 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-3
- incorporate patch to fix double-free in the KDC (CVE-2010-1320, rhbz#581922)

* Wed Apr 14 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-2
- fix a typo in kerberos.ldif

* Fri Apr  9 2010 Nalin Dahyabhai <nalin@redhat.com> 1.8.1-1
- update to 1.8.1
  - no longer need patches for rhbz#555875, rhbz#561174, rhbz#563431, RT#6661, CVE-2010-0628
- replace buildrequires on tetex-latex with one on texlive-latex, which is
  the package that provides it now

* Thu Apr  8 2010 Nalin Dahyabhai <nalin@redhat.com>
- kdc.conf: no more need to suggest a v4 mode, or listening on the v4 port

* Thu Apr  8 2010 Nalin Dahyabhai <nalin@redhat.com>
- drop patch to suppress key expiration warnings sent from the KDC in
  the last-req field, as the KDC is expected to just be configured to either
  send them or not as a particular key approaches expiration (rhbz#556495)

* Tue Mar 23 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-5
- add upstream fix for denial-of-service in SPNEGO (CVE-2010-0628, rhbz#576325)
- kdc.conf: no more need to suggest keeping keys with v4-compatible salting

* Fri Mar 19 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-4
- remove the krb5-appl bits (the -workstation-clients and -workstation-servers
  subpackages) now that krb5-appl is its own package
- replace our patch for rhbz#563431 (kpasswd doesn't fall back to guessing your
  principal name using your user name if you don't have a ccache) with the
  one upstream uses

* Fri Mar 12 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-3
- add documentation for the ticket_lifetime option (rhbz#561174)

* Mon Mar  8 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-2
- pull up patch to get the client libraries to correctly perform password
  changes over IPv6 (Sumit Bose, RT#6661)

* Fri Mar  5 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.8-1
- update to 1.8
  - temporarily bundling the krb5-appl package (split upstream as of 1.8)
    until its package review is complete
  - profile.d scriptlets are now only needed by -workstation-clients
  - adjust paths in init scripts
  - drop upstreamed fix for KDC denial of service (CVE-2010-0283)
  - drop patch to check the user's password correctly using crypt(), which
    isn't a code path we hit when we're using PAM

* Wed Mar  3 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-6
- fix a null pointer dereference and crash introduced in our PAM patch that
  would happen if ftpd was given the name of a user who wasn't known to the
  local system, limited to being triggerable by gssapi-authenticated clients by
  the default xinetd config (Olivier Fourdan, rhbz#569472)

* Tue Mar  2 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-5
- fix a regression (not labeling a kdb database lock file correctly, rhbz#569902)

* Thu Feb 25 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-4
- move the package changelog to the end to match the usual style (jdennis)
- scrub out references to RPM_SOURCE_DIR (jdennis)
- include a symlink to the readme with the name LICENSE so that people can
  find it more easily (jdennis)

* Wed Feb 17 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-3
- pull up the change to make kpasswd's behavior better match the docs
  when there's no ccache (rhbz#563431)

* Tue Feb 16 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-2
- apply patch from upstream to fix KDC denial of service (CVE-2010-0283,
  rhbz#566002)

* Wed Feb  3 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7.1-1
- update to 1.7.1
  - don't trip AD lockout on wrong password (rhbz#542687, rhbz#554351)
  - incorporates fixes for CVE-2009-4212 and CVE-2009-3295
  - fixes gss_krb5_copy_ccache() when SPNEGO is used
- move sim_client/sim_server, gss-client/gss-server, uuclient/uuserver to
  the devel subpackage, better lining up with the expected krb5/krb5-appl
  split in 1.8
- drop kvno,kadmin,k5srvutil,ktutil from -workstation-servers, as it already
  depends on -workstation which also includes them

* Mon Jan 25 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-23
- tighten up default permissions on kdc.conf and kadm5.acl (rhbz#558343)

* Fri Jan 22 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-22
- use portreserve correctly -- portrelease takes the basename of the file
  whose entries should be released, so we need three files, not one

* Mon Jan 18 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-21
- suppress warnings of impending password expiration if expiration is more than
  seven days away when the KDC reports it via the last-req field, just as we
  already do when it reports expiration via the key-expiration field (rhbz#556495)
- link with libtinfo rather than libncurses, when we can, in future RHEL

* Fri Jan 15 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-20
- krb5_get_init_creds_password: check opte->flags instead of options->flags
  when checking whether or not we get to use the prompter callback (rhbz#555875)

* Thu Jan 14 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-19
- use portreserve to make sure the KDC can always bind to the kerberos-iv
  port, kpropd can always bind to the krb5_prop port, and that kadmind can
  always bind to the kerberos-adm port (rhbz#555279)
- correct inadvertent use of macros in the changelog (rpmlint)

* Tue Jan 12 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-18
- add upstream patch for integer underflow during AES and RC4 decryption
  (CVE-2009-4212), via Tom Yu (rhbz#545015)

* Wed Jan  6 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-17
- put the conditional back for the -devel subpackage
- back down to the earlier version of the patch for rhbz#551764; the backported
  alternate version was incomplete

* Tue Jan  5 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-16
- use %%global instead of %%define
- pull up proposed patch for creating previously-not-there lock files for
  kdb databases when 'kdb5_util' is called to 'load' (rhbz#551764)

* Mon Jan  4 2010 Dennis Gregorovic <dgregor@redhat.com>
- fix conditional for future RHEL

* Mon Jan  4 2010 Nalin Dahyabhai <nalin@redhat.com> - 1.7-15
- add upstream patch for KDC crash during referral processing (CVE-2009-3295),
  via Tom Yu (rhbz#545002)

* Mon Dec 21 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-14
- refresh patch for rhbz#542868 from trunk

* Thu Dec 10 2009 Nalin Dahyabhai <nalin@redhat.com>
- move man pages that live in the -libs subpackage into the regular
  %%{_mandir} tree where they'll still be found if that package is the
  only one installed (rhbz#529319)

* Wed Dec  9 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-13
- and put it back in

* Tue Dec  8 2009 Nalin Dahyabhai <nalin@redhat.com>
- back that last change out

* Tue Dec  8 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-12
- try to make gss_krb5_copy_ccache() work correctly for spnego (rhbz#542868)

* Fri Dec  4 2009 Nalin Dahyabhai <nalin@redhat.com>
- make krb5-config suppress CFLAGS output when called with --libs (rhbz#544391)

* Thu Dec  3 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-11
- ksu: move account management checks to before we drop privileges, like
  su does (rhbz#540769)
- selinux: set the user part of file creation contexts to match the current
  context instead of what we looked up
- configure with --enable-dns-for-realm instead of --enable-dns, which isn't
  recognized any more

* Fri Nov 20 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-10
- move /etc/pam.d/ksu from krb5-workstation-servers to krb5-workstation,
  where it's actually needed (rhbz#538703)

* Fri Oct 23 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-9
- add some conditional logic to simplify building on older Fedora releases

* Tue Oct 13 2009 Nalin Dahyabhai <nalin@redhat.com>
- don't forget the README

* Mon Sep 14 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-8
- specify the location of the subsystem lock when using the status() function
  in the kadmind and kpropd init scripts, so that we get the right error when
  we're dead but have a lock file - requires initscripts 8.99 (rhbz#521772)

* Tue Sep  8 2009 Nalin Dahyabhai <nalin@redhat.com>
- if the init script fails to start krb5kdc/kadmind/kpropd because it's already
  running (according to status()), return 0 (part of rhbz#521772)

* Mon Aug 24 2009 Nalin Dahyabhai <nalin@redhat.com> - 1.7-7
- work around a compile problem with new openssl

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.7-6
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-5
- rebuild to pick up the current forms of various patches

* Mon Jul  6 2009 Nalin Dahyabhai <nalin@redhat.com>
- simplify the man pages patch by only preprocessing the files we care about
  and moving shared configure.in logic into a shared function
- catch the case of ftpd printing file sizes using %%i, when they might be
  bigger than an int now

* Tue Jun 30 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-4
- try to merge and clean up all the large file support for ftp and rcp
  - ftpd no longer prints a negative length when sending a large file
    from a 32-bit host

* Tue Jun 30 2009 Nalin Dahyabhai <nalin@redhat.com>
- pam_rhosts_auth.so's been gone, use pam_rhosts.so instead

* Mon Jun 29 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-3
- switch buildrequires: and requires: on e2fsprogs-devel into
  buildrequires: and requires: on libss-devel, libcom_err-devel, per
  sandeen on fedora-devel-list

* Fri Jun 26 2009 Nalin Dahyabhai <nalin@redhat.com>
- fix a type mismatch in krb5_copy_error_message()
- ftp: fix some odd use of strlen()
- selinux labeling: use selabel_open() family of functions rather than
  matchpathcon(), bail on it if attempting to get the mutex lock fails

* Tue Jun 16 2009 Nalin Dahyabhai <nalin@redhat.com>
- compile with %%{?_smp_mflags} (Steve Grubb)
- drop the bit where we munge part of the error table header, as it's not
  needed any more

* Fri Jun  5 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-2
- add and own %%{_libdir}/krb5/plugins/authdata

* Thu Jun  4 2009 Nalin Dahyabhai <nalin@redhat.com> 1.7-1
- update to 1.7
  - no need to work around build issues with ASN1BUF_OMIT_INLINE_FUNCS
  - configure recognizes --enable/--disable-pkinit now
  - configure can take --disable-rpath now
  - no more libdes425, krb524d, krb425.info
  - kadmin/k5srvutil/ktutil are user commands now
  - new kproplog
  - FAST encrypted-challenge plugin is new
- drop static build logic
- drop pam_krb5-specific configuration from the default krb5.conf
- drop only-use-v5 flags being passed to various things started by xinetd
- put %%{krb5prefix}/sbin in everyone's path, too (rhbz#504525)

* Tue May 19 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-106
- add an auth stack to ksu's PAM configuration so that pam_setcred() calls
  won't just fail

* Mon May 11 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-105
- make PAM support for ksu also set PAM_RUSER

* Thu Apr 23 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-104
- extend PAM support to ksu: perform account and session management for the
  target user
- pull up and merge James Leddy's changes to also set PAM_RHOST in PAM-aware
  network-facing services

* Tue Apr 21 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-103
- fix a typo in a ksu error message (Marek Mahut)
- "rev" works the way the test suite expects now, so don't disable tests
  that use it

* Mon Apr 20 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-102
- add LSB-style init script info

* Fri Apr 17 2009 Nalin Dahyabhai <nalin@redhat.com>
- explicitly run the pdf generation script using sh (part of rhbz#225974)

* Tue Apr  7 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-101
- add patches for read overflow and null pointer dereference in the
  implementation of the SPNEGO mechanism (CVE-2009-0844, CVE-2009-0845)
- add patch for attempt to free uninitialized pointer in libkrb5
  (CVE-2009-0846)
- add patch to fix length validation bug in libkrb5 (CVE-2009-0847)
- put the krb5-user .info file into just -workstation and not also
  -workstation-clients

* Mon Apr  6 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-100
- turn off krb4 support (it won't be part of the 1.7 release, but do it now)
- use triggeruns to properly shut down and disable krb524d when -server and
  -workstation-servers gets upgraded, because it's gone now
- move the libraries to /%%{_lib}, but leave --libdir alone so that plugins
  get installed and are searched for in the same locations (rhbz#473333)
- clean up buildprereq/prereqs, explicit mktemp requires, and add the
  ldconfig for the -server-ldap subpackage (part of rhbz#225974)
- escape possible macros in the changelog (part of rhbz#225974)
- fixup summary texts (part of rhbz#225974)
- take the execute bit off of the protocol docs (part of rhbz#225974)
- unflag init scripts as configuration files (part of rhbz#225974)
- make the kpropd init script treat 'reload' as 'restart' (part of rhbz#225974)

* Tue Mar 17 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-19
- libgssapi_krb5: backport fix for some errors which can occur when
  we fail to set up the server half of a context (CVE-2009-0845)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-17
- rebuild

* Thu Sep  4 2008 Nalin Dahyabhai <nalin@redhat.com>
- if we successfully change the user's password during an attempt to get
  initial credentials, but then fail to get initial creds from a non-master
  using the new password, retry against the master (rhbz#432334)

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.3-16
- fix license tag

* Wed Jul 16 2008 Nalin Dahyabhai <nalin@redhat.com>
- clear fuzz out of patches, dropping a man page patch which is no longer
  necessary
- quote %%{__cc} where needed because it includes whitespace now
- define ASN1BUF_OMIT_INLINE_FUNCS at compile-time (for now) to keep building

* Fri Jul 11 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-15
- build with -fno-strict-aliasing, which is needed because the library
  triggers these warnings
- don't forget to label principal database lock files
- fix the labeling patch so that it doesn't break bootstrapping

* Sat Jun 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.6.3-14
- generate src/include/krb5/krb5.h before building
- fix conditional for sparcv9

* Wed Apr 16 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-13
- ftp: use the correct local filename during mget when the 'case' option is
  enabled (rhbz#442713)

* Fri Apr  4 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-12
- stop exporting kadmin keys to a keytab file when kadmind starts -- the
  daemon's been able to use the database directly for a long long time now
- belatedly add aes128,aes256 to the default set of supported key types

* Tue Apr  1 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-11
- libgssapi_krb5: properly export the acceptor subkey when creating a lucid
  context (Kevin Coffman, via the nfs4 mailing list)

* Tue Mar 18 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-10
- add fixes from MITKRB5-SA-2008-001 for use of null or dangling pointer
  when v4 compatibility is enabled on the KDC (CVE-2008-0062, CVE-2008-0063,
  rhbz#432620, rhbz#432621)
- add fixes from MITKRB5-SA-2008-002 for array out-of-bounds accesses when
  high-numbered descriptors are used (CVE-2008-0947, rhbz#433596)
- add backport bug fix for an attempt to free non-heap memory in
  libgssapi_krb5 (CVE-2007-5901, rhbz#415321)
- add backport bug fix for a double-free in out-of-memory situations in
  libgssapi_krb5 (CVE-2007-5971, rhbz#415351)

* Tue Mar 18 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-9
- rework file labeling patch to not depend on fragile preprocessor trickery,
  in another attempt at fixing rhbz#428355 and friends

* Tue Feb 26 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-8
- ftp: add patch to fix "runique on" case when globbing fixes applied
- stop adding a redundant but harmless call to initialize the gssapi internals

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com>
- add patch to suppress double-processing of /etc/krb5.conf when we build
  with --sysconfdir=/etc, thereby suppressing double-logging (rhbz#231147)

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com>
- remove a patch, to fix problems with interfaces which are "up" but which
  have no address assigned, which conflicted with a different fix for the same
  problem in 1.5 (rhbz#200979)

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com>
- ftp: don't lose track of a descriptor on passive get when the server fails to
  open a file

* Mon Feb 25 2008 Nalin Dahyabhai <nalin@redhat.com>
- in login, allow PAM to interact with the user when they've been strongly
  authenticated
- in login, signal PAM when we're changing an expired password that it's an
  expired password, so that when cracklib flags a password as being weak it's
  treated as an error even if we're running as root

* Mon Feb 18 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-7
- drop netdb patch
- kdb_ldap: add patch to treat 'nsAccountLock: true' as an indication that
  the DISALLOW_ALL_TIX flag is set on an entry, for better interop with Fedora,
  Netscape, Red Hat Directory Server (Simo Sorce)

* Wed Feb 13 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-6
- patch to avoid depending on <netdb.h> to define NI_MAXHOST and NI_MAXSERV

* Tue Feb 12 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-5
- enable patch for key-expiration reporting
- enable patch to make kpasswd fall back to TCP if UDP fails (rhbz#251206)
- enable patch to make kpasswd use the right sequence number on retransmit
- enable patch to allow mech-specific creds delegated under spnego to be found
  when searching for creds

* Wed Jan  2 2008 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-4
- some init script cleanups
  - drop unquoted check and silent exit for "$NETWORKING" (rhbz#426852, rhbz#242502)
  - krb524: don't barf on missing database if it looks like we're using kldap,
    same as for kadmin
  - return non-zero status for missing files which cause startup to
    fail (rhbz#242502)

* Tue Dec 18 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-3
- allocate space for the nul-terminator in the local pathname when looking up
  a file context, and properly free a previous context (Jose Plans, rhbz#426085)

* Wed Dec  5 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-2
- rebuild

* Tue Oct 23 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.3-1
- update to 1.6.3, dropping now-integrated patches for CVE-2007-3999
  and CVE-2007-4000 (the new pkinit module is built conditionally and goes
  into the -pkinit-openssl package, at least for now, to make a buildreq
  loop with openssl avoidable)

* Wed Oct 17 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-10
- make proper use of pam_loginuid and pam_selinux in rshd and ftpd

* Fri Oct 12 2007 Nalin Dahyabhai <nalin@redhat.com>
- make krb5.conf %%verify(not md5 size mtime) in addition to
  %%config(noreplace), like /etc/nsswitch.conf (rhbz#329811)

* Mon Oct  1 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-9
- apply the fix for CVE-2007-4000 instead of the experimental patch for
  setting ok-as-delegate flags

* Tue Sep 11 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-8
- move the db2 kdb plugin from -server to -libs, because a multilib libkdb
  might need it

* Tue Sep 11 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-7
- also perform PAM session and credential management when ftpd accepts a
  client using strong authentication, missed earlier
- also label kadmind log files and files created by the db2 plugin

* Thu Sep  6 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-6
- incorporate updated fix for CVE-2007-3999 (CVE-2007-4743)
- fix incorrect call to "test" in the kadmin init script (rhbz#252322,rhbz#287291)

* Tue Sep  4 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-5
- incorporate fixes for MITKRB5-SA-2007-006 (CVE-2007-3999, CVE-2007-4000)

* Sat Aug 25 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-4
- cover more cases in labeling files on creation
- add missing gawk build dependency

* Thu Aug 23 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-3
- rebuild

* Thu Jul 26 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-2
- kdc.conf: default to listening for TCP clients, too (rhbz#248415)

* Thu Jul 19 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.2-1
- update to 1.6.2
- add "buildrequires: texinfo-tex" to get texi2pdf

* Wed Jun 27 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-8
- incorporate fixes for MITKRB5-SA-2007-004 (CVE-2007-2442,CVE-2007-2443)
  and MITKRB5-SA-2007-005 (CVE-2007-2798)

* Mon Jun 25 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-7
- reintroduce missing %%postun for the non-split_workstation case

* Mon Jun 25 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-6
- rebuild

* Mon Jun 25 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-5.1
- rebuild

* Sun Jun 24 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-5
- add missing pam-devel build requirement, force selinux-or-fail build

* Sun Jun 24 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-4
- rebuild

* Sun Jun 24 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-3
- label all files at creation-time according to the SELinux policy (rhbz#228157)

* Fri Jun 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- perform PAM account / session management in krshd (rhbz#182195,rhbz#195922)
- perform PAM authentication and account / session management in ftpd
- perform PAM authentication, account / session management, and password-
  changing in login.krb5 (rhbz#182195,rhbz#195922)

* Fri Jun 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- preprocess kerberos.ldif into a format FDS will like better, and include
  that as a doc file as well

* Fri Jun 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- switch man pages to being generated with the right paths in them
- drop old, incomplete SELinux patch
- add patch from Greg Hudson to make srvtab routines report missing-file errors
  at same point that keytab routines do (rhbz#241805)

* Thu May 24 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-2
- pull patch from svn to undo unintentional chattiness in ftp
- pull patch from svn to handle NULL krb5_get_init_creds_opt structures
  better in a couple of places where they're expected

* Wed May 23 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6.1-1
- update to 1.6.1
  - drop no-longer-needed patches for CVE-2007-0956,CVE-2007-0957,CVE-2007-1216
  - drop patch for sendto bug in 1.6, fixed in 1.6.1

* Fri May 18 2007 Nalin Dahyabhai <nalin@redhat.com>
- kadmind.init: don't fail outright if the default principal database
  isn't there if it looks like we might be using the kldap plugin
- kadmind.init: attempt to extract the key for the host-specific kadmin
  service when we try to create the keytab

* Wed May 16 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-6
- omit dependent libraries from the krb5-config --libs output, as using
  shared libraries (no more static libraries) makes them unnecessary and
  they're not part of the libkrb5 interface (patch by Rex Dieter, rhbz#240220)
  (strips out libkeyutils, libresolv, libdl)

* Fri May  4 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-5
- pull in keyutils as a build requirement to get the "KEYRING:" ccache type,
  because we've merged

* Fri May  4 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-4
- fix an uninitialized length value which could cause a crash when parsing
  key data coming from a directory server
- correct a typo in the krb5.conf man page ("ldap_server"->"ldap_servers")

* Fri Apr 13 2007 Nalin Dahyabhai <nalin@redhat.com>
- move the default acl_file, dict_file, and admin_keytab settings to
  the part of the default/example kdc.conf where they'll actually have
  an effect (rhbz#236417)

* Thu Apr  5 2007 Nalin Dahyabhai <nalin@redhat.com> 1.5-24
- merge security fixes from RHSA-2007:0095

* Tue Apr  3 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-3
- add patch to correct unauthorized access via krb5-aware telnet
  daemon (rhbz#229782, CVE-2007-0956)
- add patch to fix buffer overflow in krb5kdc and kadmind
  (rhbz#231528, CVE-2007-0957)
- add patch to fix double-free in kadmind (rhbz#231537, CVE-2007-1216)

* Thu Mar 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- back out buildrequires: keyutils-libs-devel for now

* Thu Mar 22 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-2
- add buildrequires: on keyutils-libs-devel to enable use of keyring ccaches,
  dragging keyutils-libs in as a dependency

* Mon Mar 19 2007 Nalin Dahyabhai <nalin@redhat.com> 1.5-23
- fix bug ID in changelog

* Thu Mar 15 2007 Nalin Dahyabhai <nalin@redhat.com> 1.5-22

* Thu Mar 15 2007 Nalin Dahyabhai <nalin@redhat.com> 1.5-21
- add preliminary patch to fix buffer overflow in krb5kdc and kadmind
  (rhbz#231528, CVE-2007-0957)
- add preliminary patch to fix double-free in kadmind (rhbz#231537, CVE-2007-1216)

* Wed Feb 28 2007 Nalin Dahyabhai <nalin@redhat.com>
- add patch to build semi-useful static libraries, but don't apply it unless
  we need them

* Tue Feb 27 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-20
- temporarily back out %%post changes, fix for rhbz#143289 for security update
- add preliminary patch to correct unauthorized access via krb5-aware telnet

* Mon Feb 19 2007 Nalin Dahyabhai <nalin@redhat.com>
- make profile.d scriptlets mode 644 instead of 755 (part of rhbz#225974)

* Tue Jan 30 2007 Nalin Dahyabhai <nalin@redhat.com> 1.6-1
- clean up quoting of command-line arguments passed to the krsh/krlogin
  wrapper scripts

* Mon Jan 22 2007 Nalin Dahyabhai <nalin@redhat.com>
- initial update to 1.6, pre-package-reorg
- move workstation daemons to a new subpackage (rhbz#81836, rhbz#216356, rhbz#217301), and
  make the new subpackage require xinetd (rhbz#211885)

* Mon Jan 22 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-18
- make use of install-info more failsafe (Ville Skyttä, rhbz#223704)
- preserve timestamps on shell scriptlets at %%install-time

* Tue Jan 16 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-17
- move to using pregenerated PDF docs to cure multilib conflicts (rhbz#222721)

* Fri Jan 12 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-16
- update backport of the preauth module interface (part of rhbz#194654)

* Tue Jan  9 2007 Nalin Dahyabhai <nalin@redhat.com> - 1.5-14
- apply fixes from Tom Yu for MITKRB5-SA-2006-002 (CVE-2006-6143) (rhbz#218456)
- apply fixes from Tom Yu for MITKRB5-SA-2006-003 (CVE-2006-6144) (rhbz#218456)

* Wed Dec 20 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-12
- update backport of the preauth module interface

* Mon Oct 30 2006 Nalin Dahyabhai <nalin@redhat.com>
- update backport of the preauth module interface
- add proposed patches 4566, 4567
- add proposed edata reporting interface for KDC
- add temporary placeholder for module global context fixes

* Mon Oct 23 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-11
- don't bail from the KDC init script if there's no database, it may be in
  a different location than the default (fenlason)
- remove the [kdc] section from the default krb5.conf -- doesn't seem to have
  been applicable for a while

* Wed Oct 18 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-10
- rename krb5.sh and krb5.csh so that they don't overlap (rhbz#210623)
- way-late application of added error info in kadmind.init (rhbz#65853)

* Wed Oct 18 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-9.pal_18695
- add backport of in-development preauth module interface (rhbz#208643)

* Mon Oct  9 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-9
- provide docs in PDF format instead of as tex source (Enrico Scholz, rhbz#209943)

* Wed Oct  4 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-8
- add missing shebang headers to krsh and krlogin wrapper scripts (rhbz#209238)

* Wed Sep  6 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-7
- set SS_LIB at configure-time so that libss-using apps get working readline
  support (rhbz#197044)

* Fri Aug 18 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-6
- switch to the updated patch for MITKRB-SA-2006-001

* Tue Aug  8 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-5
- apply patch to address MITKRB-SA-2006-001 (CVE-2006-3084)

* Mon Aug  7 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-4
- ensure that the gssapi library's been initialized before walking the
  internal mechanism list in gss_release_oid(), needed if called from
  gss_release_name() right after a gss_import_name() (rhbz#198092)

* Tue Jul 25 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-3
- rebuild

* Tue Jul 25 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-2
- pull up latest revision of patch to reduce lockups in rsh/rshd

* Mon Jul 17 2006 Nalin Dahyabhai <nalin@redhat.com> - 1.5-1.2
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5-1.1
- rebuild

* Thu Jul  6 2006 Nalin Dahyabhai <nalin@redhat.com> 1.5-1
- build

* Wed Jul  5 2006 Nalin Dahyabhai <nalin@redhat.com> 1.5-0
- update to 1.5

* Fri Jun 23 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-9
- mark profile.d config files noreplace (Laurent Rineau, rhbz#196447)

* Thu Jun  8 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-8
- add buildprereq for autoconf

* Mon May 22 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-7
- further munge krb5-config so that 'libdir=/usr/lib' is given even on 64-bit
  architectures, to avoid multilib conflicts; other changes will conspire to
  strip out the -L flag which uses this, so it should be harmless (rhbz#192692)

* Fri Apr 28 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-6
- adjust the patch which removes the use of rpath to also produce a
  krb5-config which is okay in multilib environments (rhbz#190118)
- make the name-of-the-tempfile comment which compile_et adds to error code
  headers always list the same file to avoid conflicts on multilib installations
- strip SIZEOF_LONG out of krb5.h so that it doesn't conflict on multilib boxes
- strip GSS_SIZEOF_LONG out of gssapi.h so that it doesn't conflict on mulitlib
  boxes

* Fri Apr 14 2006 Stepan Kasal <skasal@redhat.com> 1.4.3-5
- Fix formatting typo in kinit.1 (krb5-kinit-man-typo.patch)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.4.3-4.1
- bump again for double-long bug on ppc(64)

* Mon Feb  6 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-4
- give a little bit more information to the user when kinit gets the catch-all
  I/O error (rhbz#180175)

* Thu Jan 19 2006 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-3
- rebuild properly when pthread_mutexattr_setrobust_np() is defined but not
  declared, such as with recent glibc when _GNU_SOURCE isn't being used

* Thu Jan 19 2006 Matthias Clasen <mclasen@redhat.com> 1.4.3-2
- Use full paths in krb5.sh to avoid path lookups

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Nalin Dahyabhai <nalin@redhat.com>
- login: don't truncate passwords before passing them into crypt(), in
  case they're significant (rhbz#149476)

* Thu Nov 17 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.3-1
- update to 1.4.3
- make ksu setuid again (rhbz#137934, others)

* Tue Sep 13 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-4
- mark %%{krb5prefix}/man so that files which are packaged within it are
  flagged as %%doc (rhbz#168163)

* Tue Sep  6 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-3
- add an xinetd configuration file for encryption-only telnetd, parallelling
  the kshell/ekshell pair (rhbz#167535)

* Wed Aug 31 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-2
- change the default configured encryption type for KDC databases to the
  compiled-in default of des3-hmac-sha1 (rhbz#57847)

* Thu Aug 11 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.2-1
- update to 1.4.2, incorporating the fixes for MIT-KRB5-SA-2005-002 and
  MIT-KRB5-SA-2005-003

* Wed Jun 29 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-6
- rebuild

* Wed Jun 29 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-5
- fix telnet client environment variable disclosure the same way NetKit's
  telnet client did (CAN-2005-0488) (rhbz#159305)
- keep apps which call krb5_principal_compare() or krb5_realm_compare() with
  malformed or NULL principal structures from crashing outright (Thomas Biege)
  (rhbz#161475)

* Tue Jun 28 2005 Nalin Dahyabhai <nalin@redhat.com>
- apply fixes from draft of MIT-KRB5-SA-2005-002 (CAN-2005-1174,CAN-2005-1175)
  (rhbz#157104)
- apply fixes from draft of MIT-KRB5-SA-2005-003 (CAN-2005-1689) (rhbz#159755)

* Fri Jun 24 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-4
- fix double-close in keytab handling
- add port of fixes for CAN-2004-0175 to krb5-aware rcp (rhbz#151612)

* Fri May 13 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-3
- prevent spurious EBADF in krshd when stdin is closed by the client while
  the command is running (rhbz#151111)

* Fri May 13 2005 Martin Stransky <stransky@redhat.com> 1.4.1-2
- add deadlock patch, removed old patch

* Fri May  6 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4.1-1
- update to 1.4.1, incorporating fixes for CAN-2005-0468 and CAN-2005-0469
- when starting the KDC or kadmind, if KRB5REALM is set via the /etc/sysconfig
  file for the service, pass it as an argument for the -r flag

* Wed Mar 23 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4-3
- drop krshd patch for now

* Thu Mar 17 2005 Nalin Dahyabhai <nalin@redhat.com>
- add draft fix from Tom Yu for slc_add_reply() buffer overflow (CAN-2005-0469)
- add draft fix from Tom Yu for env_opt_add() buffer overflow (CAN-2005-0468)

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4-2
- don't include <term.h> into the telnet client when we're not using curses

* Thu Feb 24 2005 Nalin Dahyabhai <nalin@redhat.com> 1.4-1
- update to 1.4
  - v1.4 kadmin client requires a v1.4 kadmind on the server, or use the "-O"
    flag to specify that it should communicate with the server using the older
    protocol
  - new libkrb5support library
  - v5passwdd and kadmind4 are gone
  - versioned symbols
- pick up $KRB5KDC_ARGS from /etc/sysconfig/krb5kdc, if it exists, and pass
  it on to krb5kdc
- pick up $KADMIND_ARGS from /etc/sysconfig/kadmin, if it exists, and pass
  it on to kadmind
- pick up $KRB524D_ARGS from /etc/sysconfig/krb524, if it exists, and pass
  it on to krb524d *instead of* "-m"
- set "forwardable" in [libdefaults] in the default krb5.conf to match the
  default setting which we supply for pam_krb5
- set a default of 24h for "ticket_lifetime" in [libdefaults], reflecting the
  compiled-in default

* Mon Dec 20 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.6-3
- rebuild

* Mon Dec 20 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.6-2
- rebuild

* Mon Dec 20 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.6-1
- update to 1.3.6, which includes the previous fix

* Mon Dec 20 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-8
- apply fix from Tom Yu for MITKRB5-SA-2004-004 (CAN-2004-1189)

* Fri Dec 17 2004 Martin Stransky <stransky@redhat.com> 1.3.5-7
- fix deadlock during file transfer via rsync/krsh
- thanks goes to James Antill for hint

* Fri Nov 26 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-6
- rebuild

* Mon Nov 22 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-3
- fix predictable-tempfile-name bug in krb5-send-pr (CAN-2004-0971, rhbz#140036)

* Tue Nov 16 2004 Nalin Dahyabhai <nalin@redhat.com>
- silence compiler warning in kprop by using an in-memory ccache with a fixed
  name instead of an on-disk ccache with a name generated by tmpnam()

* Tue Nov 16 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-2
- fix globbing patch port mode (rhbz#139075)

* Mon Nov  1 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.5-1
- fix segfault in telnet due to incorrect checking of gethostbyname_r result
  codes (rhbz#129059)

* Fri Oct 15 2004 Nalin Dahyabhai <nalin@redhat.com>
- remove rc4-hmac:norealm and rc4-hmac:onlyrealm from the default list of
  supported keytypes in kdc.conf -- they produce exactly the same keys as
  rc4-hmac:normal because rc4 string-to-key ignores salts
- nuke kdcrotate -- there are better ways to balance the load on KDCs, and
  the SELinux policy for it would have been scary-looking
- update to 1.3.5, mainly to include MITKRB5SA 2004-002 and 2004-003

* Tue Aug 31 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-7
- rebuild

* Tue Aug 24 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-6
- rebuild

* Tue Aug 24 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-5
- incorporate revised fixes from Tom Yu for CAN-2004-0642, CAN-2004-0644,
  CAN-2004-0772

* Mon Aug 23 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-4
- rebuild

* Mon Aug 23 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-3
- incorporate fixes from Tom Yu for CAN-2004-0642, CAN-2004-0772
  (MITKRB5-SA-2004-002, rhbz#130732)
- incorporate fixes from Tom Yu for CAN-2004-0644 (MITKRB5-SA-2004-003, rhbz#130732)

* Tue Jul 27 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-2
- fix indexing error in server sorting patch (rhbz#127336)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun 14 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-0.1
- update to 1.3.4 final

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.4-0
- update to 1.3.4 beta1
- remove MITKRB5-SA-2004-001, included in 1.3.4

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-8
- rebuild

* Fri Jun  4 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-7
- rebuild

* Fri Jun  4 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-6
- apply updated patch from MITKRB5-SA-2004-001 (revision 2004-06-02)

* Tue Jun  1 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-5
- rebuild

* Tue Jun  1 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-4
- apply patch from MITKRB5-SA-2004-001 (rhbz#125001)

* Wed May 12 2004 Thomas Woerner <twoerner@redhat.com> 1.3.3-3
- removed rpath

* Thu Apr 15 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-2
- re-enable large file support, fell out in 1.3-1
- patch rcp to use long long and %%lld format specifiers when reporting file
  sizes on large files

* Tue Apr 13 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.3-1
- update to 1.3.3

* Wed Mar 10 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.2-1
- update to 1.3.2

* Mon Mar  8 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-12
- rebuild

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 1.3.1-11.1
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 1.3.1-11
- rebuilt

* Mon Feb  9 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-10
- catch krb4 send_to_kdc cases in kdc preference patch

* Mon Feb  2 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-9
- remove patch to set TERM in klogind which, combined with the upstream fix in
  1.3.1, actually produces the bug now (rhbz#114762)

* Mon Jan 19 2004 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-8
- when iterating over lists of interfaces which are "up" from getifaddrs(),
  skip over those which have no address (rhbz#113347)

* Mon Jan 12 2004 Nalin Dahyabhai <nalin@redhat.com>
- prefer the kdc which last replied to a request when sending requests to kdcs

* Mon Nov 24 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-7
- fix combination of --with-netlib and --enable-dns (rhbz#82176)

* Tue Nov 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- remove libdefault ticket_lifetime option from the default krb5.conf, it is
  ignored by libkrb5

* Thu Sep 25 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-6
- fix bug in patch to make rlogind start login with a clean environment a la
  netkit rlogin, spotted and fixed by Scott McClung

* Tue Sep 23 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-5
- include profile.d scriptlets in krb5-devel so that krb5-config will be in
  the path if krb5-workstation isn't installed, reported by Kir Kolyshkin

* Mon Sep  8 2003 Nalin Dahyabhai <nalin@redhat.com>
- add more etypes (arcfour) to the default enctype list in kdc.conf
- don't apply previous patch, refused upstream

* Fri Sep  5 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-4
- fix 32/64-bit bug storing and retrieving the issue_date in v4 credentials

* Wed Sep 3 2003 Dan Walsh <dwalsh@redhat.com> 1.3.1-3
- Don't check for write access on /etc/krb5.conf if SELinux

* Tue Aug 26 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-2
- fixup some int/pointer varargs wackiness

* Tue Aug  5 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-1
- rebuild

* Mon Aug  4 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3.1-0
- update to 1.3.1

* Thu Jul 24 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3-2
- pull fix for non-compliant encoding of salt field in etype-info2 preauth
  data from 1.3.1 beta 1, until 1.3.1 is released.

* Mon Jul 21 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3-1
- update to 1.3

* Mon Jul  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.8-4
- correctly use stdargs

* Wed Jun 18 2003 Nalin Dahyabhai <nalin@redhat.com> 1.3-0.beta.4
- test update to 1.3 beta 4
- ditch statglue build option
- krb5-devel requires e2fsprogs-devel, which now provides libss and libcom_err

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Jeremy Katz <katzj@redhat.com> 1.2.8-2
- gcc 3.3 doesn't implement varargs.h, include stdarg.h instead

* Wed Apr  9 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.8-1
- update to 1.2.8

* Mon Mar 31 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-14
- fix double-free of enc_part2 in krb524d

* Fri Mar 21 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-13
- update to latest patch kit for MITKRB5-SA-2003-004

* Wed Mar 19 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-12
- add patch included in MITKRB5-SA-2003-003 (CAN-2003-0028)

* Mon Mar 17 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-11
- add patches from patchkit from MITKRB5-SA-2003-004 (CAN-2003-0138 and
  CAN-2003-0139)

* Thu Mar  6 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-10
- rebuild

* Thu Mar  6 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-9
- fix buffer underrun in unparsing certain principals (CAN-2003-0082)

* Tue Feb  4 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-8
- add patch to document the reject-bad-transited option in kdc.conf

* Mon Feb  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- add patch to fix server-side crashes when principals have no
  components (CAN-2003-0072)

* Thu Jan 23 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-7
- add patch from Mark Cox for exploitable bugs in ftp client

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-5
- use PICFLAGS when building code from the ktany patch

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> 1.2.7-4
- debloat

* Tue Jan  7 2003 Jeremy Katz <katzj@redhat.com> 1.2.7-3
- include .so.* symlinks as well as .so.*.*

* Mon Dec  9 2002 Jakub Jelinek <jakub@redhat.com> 1.2.7-2
- always #include <errno.h> to access errno, never do it directly
- enable LFS on a bunch of other 32-bit arches

* Wed Dec  4 2002 Nalin Dahyabhai <nalin@redhat.com>
- increase the maximum name length allowed by kuserok() to the higher value
  used in development versions

* Mon Dec  2 2002 Nalin Dahyabhai <nalin@redhat.com>
- install src/krb524/README as README.krb524 in the -servers package,
  includes information about converting for AFS principals

* Fri Nov 15 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.7-1
- update to 1.2.7
- disable use of tcl

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.7-beta2 (internal only, not for release), dropping dnsparse
  and kadmind4 fixes

* Wed Oct 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-5
- add patch for buffer overflow in kadmind4 (not used by default)

* Fri Oct 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-4
- drop a hunk from the dnsparse patch which is actually redundant (thanks to
  Tom Yu)

* Wed Oct  9 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-3
- patch to handle truncated dns responses

* Mon Oct  7 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-2
- remove hashless key types from the default kdc.conf, they're not supposed to
  be there, noted by Sam Hartman on krbdev

* Fri Sep 27 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.6-1
- update to 1.2.6

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.5-7
- use %%{_lib} for the sake of multilib systems

* Fri Aug  2 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.5-6
- add patch from Tom Yu for exploitable bugs in rpc code used in kadmind

* Tue Jul 23 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.5-5
- fix bug in krb5.csh which would cause the path check to always succeed

* Fri Jul 19 2002 Jakub Jelinek <jakub@redhat.com> 1.2.5-4
- build even libdb.a with -fPIC and $RPM_OPT_FLAGS.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May  1 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.5-1
- update to 1.2.5
- disable statglue

* Fri Mar  1 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.4-1
- update to 1.2.4

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-5
- rebuild in new environment
- reenable statglue

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq chkconfig for the server subpackage

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-3
- build without -g3, which gives us large static libraries in -devel

* Tue Jan 15 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-2
- reintroduce ld.so.conf munging in the -libs %%post

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 1.2.3-1
- rename the krb5 package back to krb5-libs; the previous rename caused
  something of an uproar
- update to 1.2.3, which includes the FTP and telnetd fixes
- configure without --enable-dns-for-kdc --enable-dns-for-realm, which now set
  the default behavior instead of enabling the feature (the feature is enabled
  by --enable-dns, which we still use)
- reenable optimizations on Alpha
- support more encryption types in the default kdc.conf (heads-up from post
  to comp.protocols.kerberos by Jason Heiss)

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-14
- rename the krb5-libs package to krb5 (naming a subpackage -libs when there
  is no main package is silly)
- move defaults for PAM to the appdefaults section of krb5.conf -- this is
  the area where the krb5_appdefault_* functions look for settings)
- disable statglue (warning: breaks binary compatibility with previous
  packages, but has to be broken at some point to work correctly with
  unpatched versions built with newer versions of glibc)

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com> 1.2.2-13
- bump release number and rebuild

* Wed Aug  1 2001 Nalin Dahyabhai <nalin@redhat.com>
- add patch to fix telnetd vulnerability

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak statglue.c to fix stat/stat64 aliasing problems
- be cleaner in use of gcc to build shlibs

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- use gcc to build shared libraries

* Wed Jun 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- add patch to support "ANY" keytab type (i.e.,
  "default_keytab_name = ANY:FILE:/etc/krb5.keytab,SRVTAB:/etc/srvtab"
  patch from Gerald Britton, rhbz#42551)
- build with -D_FILE_OFFSET_BITS=64 to get large file I/O in ftpd (rhbz#30697)
- patch ftpd to use long long and %%lld format specifiers to support the SIZE
  command on large files (also rhbz#30697)
- don't use LOG_AUTH as an option value when calling openlog() in ksu (rhbz#45965)
- implement reload in krb5kdc and kadmind init scripts (rhbz#41911)
- lose the krb5server init script (not using it any more)

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- pass some structures by address instead of on the stack in krb5kdc

* Tue May 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Apr 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- add patch from Tom Yu to fix ftpd overflows (rhbz#37731)

* Wed Apr 18 2001 Than Ngo <than@redhat.com>
- disable optimizations on the alpha again

* Fri Mar 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- add in glue code to make sure that libkrb5 continues to provide a
  weak copy of stat()

* Thu Mar 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- build alpha with -O0 for now

* Thu Mar  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix the kpropd init script

* Mon Mar  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.2, which fixes some bugs relating to empty ETYPE-INFO
- re-enable optimization on Alpha

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- build alpha with -O0 for now
- own %%{_var}/kerberos

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- own the directories which are created for each package (rhbz#26342)

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize init scripts

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- add some comments to the ksu patches for the curious
- re-enable optimization on alphas

* Mon Jan 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix krb5-send-pr (rhbz#18932) and move it from -server to -workstation
- buildprereq libtermcap-devel
- temporariliy disable optimization on alphas
- gettextize init scripts

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- force -fPIC

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add bison as a BuildPrereq (rhbz#20091)

* Mon Oct 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- change /usr/dict/words to /usr/share/dict/words in default kdc.conf (rhbz#20000)

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply kpasswd bug fixes from David Wragg

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- make krb5-libs obsolete the old krb5-configs package (rhbz#18351)
- don't quit from the kpropd init script if there's no principal database so
  that you can propagate the first time without running kpropd manually
- don't complain if /etc/ld.so.conf doesn't exist in the -libs %%post

* Tue Sep 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix credential forwarding problem in klogind (goof in KRB5CCNAME handling)
  (rhbz#11588)
- fix heap corruption bug in FTP client (rhbz#14301)

* Wed Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix summaries and descriptions
- switched the default transfer protocol from PORT to PASV as proposed on
  bugzilla (rhbz#16134), and to match the regular ftp package's behavior

* Wed Jul 19 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Fri Jul 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable servers by default to keep linuxconf from thinking they need to be
  started when they don't

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- change cleanup code in post to not tickle chkconfig
- add grep as a Prereq: for -libs

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- move condrestarts to postun
- make xinetd configs noreplace
- add descriptions to xinetd configs
- add /etc/init.d as a prereq for the -server package
- patch to properly truncate $TERM in krlogind

* Fri Jun 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.1
- back out Tom Yu's patch, which is a big chunk of the 1.2 -> 1.2.1 update
- start using the official source tarball instead of its contents

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Tom Yu's patch to fix compatibility between 1.2 kadmin and 1.1.1 kadmind
- pull out 6.2 options in the spec file (sonames changing in 1.2 means it's not
  compatible with other stuff in 6.2, so no need)

* Wed Jun 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak graceful start/stop logic in post and preun

* Mon Jun 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to the 1.2 release
- ditch a lot of our patches which went upstream
- enable use of DNS to look up things at build-time
- disable use of DNS to look up things at run-time in default krb5.conf
- change ownership of the convert-config-files script to root.root
- compress PS docs
- fix some typos in the kinit man page
- run condrestart in server post, and shut down in preun

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- only remove old krb5server init script links if the init script is there

* Sat Jun 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable kshell and eklogin by default

* Thu Jun 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch mkdir/rmdir problem in ftpcmd.y
- add condrestart option to init script
- split the server init script into three pieces and add one for kpropd

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- make sure workstation servers are all disabled by default
- clean up krb5server init script

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply second set of buffer overflow fixes from Tom Yu
- fix from Dirk Husung for a bug in buffer cleanups in the test suite
- work around possibly broken rev binary in running test suite
- move default realm configs from /var/kerberos to %%{_var}/kerberos

* Tue Jun  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- make ksu and v4rcp owned by root

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- use %%{_infodir} to better comply with FHS
- move .so files to -devel subpackage
- tweak xinetd config files (bugs rhbz#11833, rhbz#11835, rhbz#11836, rhbz#11840)
- fix package descriptions again

* Wed May 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- change a LINE_MAX to 1024, fix from Ken Raeburn
- add fix for login vulnerability in case anyone rebuilds without krb4 compat
- add tweaks for byte-swapping macros in krb.h, also from Ken
- add xinetd config files
- make rsh and rlogin quieter
- build with debug to fix credential forwarding
- add rsh as a build-time req because the configure scripts look for it to
  determine paths

* Wed May 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix config_subpackage logic

* Tue May 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove setuid bit on v4rcp and ksu in case the checks previously added
  don't close all of the problems in ksu
- apply patches from Jeffrey Schiller to fix overruns Chris Evans found
- reintroduce configs subpackage for use in the errata
- add PreReq: sh-utils

* Mon May 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix double-free in the kdc (patch merged into MIT tree)
- include convert-config-files script as a documentation file

* Wed May 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch ksu man page because the -C option never works
- add access() checks and disable debug mode in ksu
- modify default ksu build arguments to specify more directories in CMD_PATH
  and to use getusershell()

* Wed May 03 2000 Bill Nottingham <notting@redhat.com>
- fix configure stuff for ia64

* Mon Apr 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- add LDCOMBINE=-lc to configure invocation to use libc versioning (rhbz#10653)
- change Requires: for/in subpackages to include %%{version}

* Wed Apr 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- add man pages for kerberos(1), kvno(1), .k5login(5)
- add kvno to -workstation

* Mon Apr 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge krb5-configs back into krb5-libs.  The krb5.conf file is marked as
  a %%config file anyway.
- Make krb5.conf a noreplace config file.

* Thu Mar 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- Make klogind pass a clean environment to children, like NetKit's rlogind does.

* Wed Mar 08 2000 Nalin Dahyabhai <nalin@redhat.com>
- Don't enable the server by default.
- Compress info pages.
- Add defaults for the PAM module to krb5.conf

* Mon Mar 06 2000 Nalin Dahyabhai <nalin@redhat.com>
- Correct copyright: it's exportable now, provided the proper paperwork is
  filed with the government.

* Fri Mar 03 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply Mike Friedman's patch to fix format string problems
- don't strip off argv[0] when invoking regular rsh/rlogin

* Thu Mar 02 2000 Nalin Dahyabhai <nalin@redhat.com>
- run kadmin.local correctly at startup

* Mon Feb 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- pass absolute path to kadm5.keytab if/when extracting keys at startup

* Sat Feb 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix info page insertions

* Wed Feb  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak server init script to automatically extract kadm5 keys if
  /var/kerberos/krb5kdc/kadm5.keytab doesn't exist yet
- adjust package descriptions

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix for potentially gzipped man pages

* Fri Jan 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix comments in krb5-configs

* Fri Jan  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- move /usr/kerberos/bin to end of PATH

* Tue Dec 28 1999 Nalin Dahyabhai <nalin@redhat.com>
- install kadmin header files

* Tue Dec 21 1999 Nalin Dahyabhai <nalin@redhat.com>
- patch around TIOCGTLC defined on alpha and remove warnings from libpty.h
- add installation of info docs
- remove krb4 compat patch because it doesn't fix workstation-side servers

* Mon Dec 20 1999 Nalin Dahyabhai <nalin@redhat.com>
- remove hesiod dependency at build-time

* Sun Dec 19 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- rebuild on 1.1.1

* Thu Oct  7 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- clean up init script for server, verify that it works [jlkatz]
- clean up rotation script so that rc likes it better
- add clean stanza

* Mon Oct  4 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- backed out ncurses and makeshlib patches
- update for krb5-1.1
- add KDC rotation to rc.boot, based on ideas from Michael's C version

* Mon Sep 27 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- added -lncurses to telnet and telnetd makefiles

* Mon Jul  5 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- added krb5.csh and krb5.sh to /etc/profile.d

* Tue Jun 22 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- broke out configuration files

* Mon Jun 14 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- fixed server package so that it works now

* Sat May 15 1999 Nalin Dahyabhai <nsdahya1@eos.ncsu.edu>
- started changelog (previous package from zedz.net)
- updated existing 1.0.5 RPM from Eos Linux to krb5 1.0.6
- added --force to makeinfo commands to skip errors during build

## END: Generated by rpmautospec
