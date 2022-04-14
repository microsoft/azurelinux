%global rhel7_minor %(%{__grep} -o "7.[0-9]*" /etc/redhat-release |%{__sed} -s 's/7.//')

# we don't want to provide private python extension libs
%define __provides_exclude_from %{python3_sitearch}/.*\.so$|%{_libdir}/%{name}/modules/libwbclient.so.*$

# SSSD fails to build with -Wl,-z,defs
%undefine _strict_symbol_defs_build

%define _hardened_build 1

    %global enable_polkit_rules_option --disable-polkit-rules-path

# Determine the location of the LDB modules directory
%global ldb_modulesdir %(pkg-config --variable=modulesdir ldb)
%global ldb_version 1.2.0

    %global with_cifs_utils_plugin 1

%global enable_systemtap 1
    %global enable_systemtap_opt --enable-systemtap

    %global with_kcm 1

    %global with_gdm_pam_extensions 1


    %global use_openssl 1


%global libwbc_alternatives_version 0.14
%global libwbc_lib_version %{libwbc_alternatives_version}.0
%global libwbc_alternatives_suffix %nil
%if 0%{?__isa_bits} == 64
%global libwbc_alternatives_suffix -64
%endif

Name: sssd
Version: 2.3.1
Release: 4%{?dist}
Summary: System Security Services Daemon
License: GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: https://github.com/SSSD/sssd/
Source0: https://github.com/SSSD/sssd/releases/download/sssd-2_3_1/sssd-2.3.1.tar.gz

### Patches ###

### Downstream only patches ###
Patch0502: 0502-SYSTEMD-Use-capabilities.patch


### Dependencies ###

Requires: sssd-common = %{version}-%{release}
Requires: sssd-ldap = %{version}-%{release}
Requires: sssd-krb5 = %{version}-%{release}
Requires: sssd-ipa = %{version}-%{release}
Requires: sssd-ad = %{version}-%{release}
Recommends: sssd-proxy = %{version}-%{release}
Suggests: python3-sssdconfig = %{version}-%{release}
Suggests: sssd-dbus = %{version}-%{release}

%global servicename sssd
%global sssdstatedir %{_localstatedir}/lib/sss
%global dbpath %{sssdstatedir}/db
%global keytabdir %{sssdstatedir}/keytabs
%global pipepath %{sssdstatedir}/pipes
%global mcpath %{sssdstatedir}/mc
%global pubconfpath %{sssdstatedir}/pubconf
%global gpocachepath %{sssdstatedir}/gpo_cache
%global secdbpath %{sssdstatedir}/secrets
%global deskprofilepath %{sssdstatedir}/deskprofile

### Build Dependencies ###

BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: cyrus-sasl-devel
BuildRequires: libtool
BuildRequires: m4
BuildRequires: gcc
BuildRequires: popt-devel
BuildRequires: libtalloc-devel
BuildRequires: libtevent-devel
BuildRequires: libtdb-devel
BuildRequires: libldb-devel >= %{ldb_version}
BuildRequires: libdhash-devel >= 0.4.2
BuildRequires: libcollection-devel
BuildRequires: libini_config-devel >= 1.1
BuildRequires: dbus-devel
BuildRequires: dbus-libs
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: nss-devel
BuildRequires: nspr-devel
BuildRequires: pcre-devel
BuildRequires: libxslt
BuildRequires: libxml2
BuildRequires: docbook-style-xsl
BuildRequires: krb5-devel
BuildRequires: c-ares-devel
BuildRequires: python3-devel
BuildRequires: check-devel
BuildRequires: doxygen
BuildRequires: libselinux-devel
BuildRequires: libsemanage-devel
BuildRequires: bind-utils
BuildRequires: keyutils-libs-devel
BuildRequires: gettext-devel
BuildRequires: pkgconfig
BuildRequires: diffstat
BuildRequires: findutils
BuildRequires: glib2-devel
BuildRequires: libcmocka-devel >= 1.0.0
BuildRequires: uid_wrapper
BuildRequires: nss_wrapper
BuildRequires: pam_wrapper
BuildRequires: libnl3-devel
BuildRequires: systemd-devel
BuildRequires: systemd
BuildRequires: cifs-utils-devel
BuildRequires: libnfsidmap-devel
BuildRequires: samba4-devel
BuildRequires: libsmbclient-devel
BuildRequires: samba-winbind
BuildRequires: systemtap-sdt-devel
BuildRequires: http-parser-devel
BuildRequires: libuuid-devel
BuildRequires: jansson-devel
BuildRequires: libcurl-devel
BuildRequires: gdm-pam-extensions-devel
%if (0%{?use_openssl} == 1)
BuildRequires: p11-kit-devel
BuildRequires: openssl-devel
BuildRequires: gnutls-utils
BuildRequires: softhsm >= 2.1.0
%endif
BuildRequires: openssl
BuildRequires: openssh
BuildRequires: nss-tools
BuildRequires: libwbclient-devel

%description
Provides a set of daemons to manage access to remote directories and
authentication mechanisms. It provides an NSS and PAM interface toward
the system and a plug-gable back-end system to connect to multiple different
account sources. It is also the basis to provide client auditing and policy
services for projects like FreeIPA.

The sssd sub-package is a meta-package that contains the daemon as well as all
the existing back ends.

%package common
Summary: Common files for the SSSD
License: GPLv3+
# Conflicts
Conflicts: selinux-policy < 3.10.0-46
Conflicts: sssd < 1.10.0-8%{?dist}.beta2
# Requires
# due to ABI changes in 1.1.30/1.2.0
Requires: libldb >= %{ldb_version}
Requires: sssd-client%{?_isa} = %{version}-%{release}
Recommends: libsss_sudo = %{version}-%{release}
Recommends: libsss_autofs%{?_isa} = %{version}-%{release}
Recommends: sssd-nfs-idmap = %{version}-%{release}
Requires: libsss_idmap = %{version}-%{release}
%{?systemd_requires}

### Provides ###
Provides: libsss_sudo-devel = %{version}-%{release}
Obsoletes: libsss_sudo-devel <= 1.10.0-7%{?dist}.beta1

%description common
Common files for the SSSD. The common package includes all the files needed
to run a particular back end, however, the back ends are packaged in separate
sub-packages such as sssd-ldap.

%package client
Summary: SSSD Client libraries for NSS and PAM
License: LGPLv3+
Requires(post): /sbin/ldconfig
Requires(post):  /usr/sbin/alternatives
Requires(preun): /usr/sbin/alternatives

%description client
Provides the libraries needed by the PAM and NSS stacks to connect to the SSSD
service.

%package -n libsss_sudo
Summary: A library to allow communication between SUDO and SSSD
License: LGPLv3+
Conflicts: sssd-common < %{version}-%{release}

%description -n libsss_sudo
A utility library to allow communication between SUDO and SSSD

%package -n libsss_autofs
Summary: A library to allow communication between Autofs and SSSD
License: LGPLv3+
Conflicts: sssd-common < %{version}-%{release}

%description -n libsss_autofs
A utility library to allow communication between Autofs and SSSD

%package tools
Summary: Userspace tools for use with the SSSD
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
# required by sss_obfuscate
Requires: python3-sss = %{version}-%{release}
Requires: python3-sssdconfig = %{version}-%{release}
Recommends: sssd-dbus

%description tools
Provides userspace tools for manipulating users, groups, and nested groups in
SSSD when using id_provider = local in /etc/sssd/sssd.conf.

Also provides several other administrative tools:
    * sss_debuglevel to change the debug level on the fly
    * sss_seed which pre-creates a user entry for use in kickstarts
    * sss_obfuscate for generating an obfuscated LDAP password
    * sssctl -- an sssd status and control utility

%package -n python3-sssdconfig
Summary: SSSD and IPA configuration file manipulation classes and functions
License: GPLv3+
BuildArch: noarch
%{?python_provide:%python_provide python3-sssdconfig}

%description -n python3-sssdconfig
Provides python3 files for manipulation SSSD and IPA configuration files.

%package -n python3-sss
Summary: Python3 bindings for sssd
License: LGPLv3+
Requires: sssd-common = %{version}-%{release}
%{?python_provide:%python_provide python3-sss}

%description -n python3-sss
Provides python3 module for manipulating users, groups, and nested groups in
SSSD when using id_provider = local in /etc/sssd/sssd.conf.

Also provides several other useful python3 bindings:
    * function for retrieving list of groups user belongs to.
    * class for obfuscation of passwords

%package -n python3-sss-murmur
Summary: Python3 bindings for murmur hash function
License: LGPLv3+
%{?python_provide:%python_provide python3-sss-murmur}

%description -n python3-sss-murmur
Provides python3 module for calculating the murmur hash version 3

%package ldap
Summary: The LDAP back end of the SSSD
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}

%description ldap
Provides the LDAP back end that the SSSD can utilize to fetch identity data
from and authenticate against an LDAP server.

%package krb5-common
Summary: SSSD helpers needed for Kerberos and GSSAPI authentication
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: cyrus-sasl-gssapi%{?_isa}
Requires: sssd-common = %{version}-%{release}

%description krb5-common
Provides helper processes that the LDAP and Kerberos back ends can use for
Kerberos user or host authentication.

%package krb5
Summary: The Kerberos authentication back end for the SSSD
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}

%description krb5
Provides the Kerberos back end that the SSSD can utilize authenticate
against a Kerberos server.

%package common-pac
Summary: Common files needed for supporting PAC processing
License: GPLv3+
Requires: sssd-common = %{version}-%{release}

%description common-pac
Provides common files needed by SSSD providers such as IPA and Active Directory
for handling Kerberos PACs.

%package ipa
Summary: The IPA back end of the SSSD
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: libipa_hbac%{?_isa} = %{version}-%{release}
Recommends: bind-utils
Requires: sssd-common-pac = %{version}-%{release}

%description ipa
Provides the IPA back end that the SSSD can utilize to fetch identity data
from and authenticate against an IPA server.

%package ad
Summary: The AD back end of the SSSD
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}
Requires: sssd-krb5-common = %{version}-%{release}
Requires: sssd-common-pac = %{version}-%{release}
Recommends: bind-utils
Recommends: adcli
Suggests: sssd-libwbclient = %{version}-%{release}
Suggests: sssd-winbind-idmap = %{version}-%{release}

%description ad
Provides the Active Directory back end that the SSSD can utilize to fetch
identity data from and authenticate against an Active Directory server.

%package proxy
Summary: The proxy back end of the SSSD
License: GPLv3+
Conflicts: sssd < 1.10.0-8.beta2
Requires: sssd-common = %{version}-%{release}

%description proxy
Provides the proxy back end which can be used to wrap an existing NSS and/or
PAM modules to leverage SSSD caching.

%package -n libsss_idmap
Summary: FreeIPA Idmap library
License: LGPLv3+

%description -n libsss_idmap
Utility library to convert SIDs to Unix uids and gids

%package -n libsss_idmap-devel
Summary: FreeIPA Idmap library
License: LGPLv3+
Requires: libsss_idmap = %{version}-%{release}

%description -n libsss_idmap-devel
Utility library to SIDs to Unix uids and gids

%package -n libipa_hbac
Summary: FreeIPA HBAC Evaluator library
License: LGPLv3+

%description -n libipa_hbac
Utility library to validate FreeIPA HBAC rules for authorization requests

%package -n libipa_hbac-devel
Summary: FreeIPA HBAC Evaluator library
License: LGPLv3+
Requires: libipa_hbac = %{version}-%{release}

%description -n libipa_hbac-devel
Utility library to validate FreeIPA HBAC rules for authorization requests

%package -n python3-libipa_hbac
Summary: Python3 bindings for the FreeIPA HBAC Evaluator library
License: LGPLv3+
Requires: libipa_hbac = %{version}-%{release}
%{?python_provide:%python_provide python3-libipa_hbac}

%description -n python3-libipa_hbac
The python3-libipa_hbac contains the bindings so that libipa_hbac can be
used by Python applications.

%package -n libsss_nss_idmap
Summary: Library for SID and certificate based lookups
License: LGPLv3+

%description -n libsss_nss_idmap
Utility library for SID and certificate based lookups

%package -n libsss_nss_idmap-devel
Summary: Library for SID and certificate based lookups
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}

%description -n libsss_nss_idmap-devel
Utility library for SID and certificate based lookups

%package -n python3-libsss_nss_idmap
Summary: Python3 bindings for libsss_nss_idmap
License: LGPLv3+
Requires: libsss_nss_idmap = %{version}-%{release}
%{?python_provide:%python_provide python3-libsss_nss_idmap}

%description -n python3-libsss_nss_idmap
The python3-libsss_nss_idmap contains the bindings so that libsss_nss_idmap can
be used by Python applications.

%package dbus
Summary: The D-Bus responder of the SSSD
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
%{?systemd_requires}

%description dbus
Provides the D-Bus responder of the SSSD, called the InfoPipe, that allows
the information from the SSSD to be transmitted over the system bus.

%package -n libsss_simpleifp
Summary: The SSSD D-Bus responder helper library
License: GPLv3+
Requires: sssd-dbus = %{version}-%{release}

%description -n libsss_simpleifp
Provides library that simplifies D-Bus API for the SSSD InfoPipe responder.

%package -n libsss_simpleifp-devel
Summary: The SSSD D-Bus responder helper library
License: GPLv3+
Requires: dbus-devel
Requires: libsss_simpleifp = %{version}-%{release}

%description -n libsss_simpleifp-devel
Provides library that simplifies D-Bus API for the SSSD InfoPipe responder.

%package libwbclient
Summary: The SSSD libwbclient implementation
License: GPLv3+ and LGPLv3+
Conflicts: libwbclient < 4.2.0-0.2.rc2
Conflicts: sssd-common < %{version}-%{release}

%description libwbclient
The SSSD libwbclient implementation.

%package libwbclient-devel
Summary: Development libraries for the SSSD libwbclient implementation
License: GPLv3+ and LGPLv3+
Requires: sssd-libwbclient = %{version}-%{release}
Conflicts: libwbclient-devel < 4.2.0-0.2.rc2

%description libwbclient-devel
Development libraries for the SSSD libwbclient implementation.

%package winbind-idmap
Summary: SSSD's idmap_sss Backend for Winbind
License: GPLv3+ and LGPLv3+
Conflicts: sssd-common < %{version}-%{release}

%description winbind-idmap
The idmap_sss module provides a way for Winbind to call SSSD to map UIDs/GIDs
and SIDs.

%package nfs-idmap
Summary: SSSD plug-in for NFSv4 rpc.idmapd
License: GPLv3+
Conflicts: sssd-common < %{version}-%{release}

%description nfs-idmap
The libnfsidmap sssd module provides a way for rpc.idmapd to call SSSD to map
UIDs/GIDs to names and vice versa. It can be also used for mapping principal
(user) name to IDs(UID or GID) or to obtain groups which user are member of.

%package -n libsss_certmap
Summary: SSSD Certificate Mapping Library
License: LGPLv3+
Conflicts: sssd-common < %{version}-%{release}

%description -n libsss_certmap
Library to map certificates to users based on rules

%package -n libsss_certmap-devel
Summary: SSSD Certificate Mapping Library
License: LGPLv3+
Requires: libsss_certmap = %{version}-%{release}

%description -n libsss_certmap-devel
Library to map certificates to users based on rules

%package kcm
Summary: An implementation of a Kerberos KCM server
License: GPLv3+
Requires: sssd-common = %{version}-%{release}
%{?systemd_requires}

%description kcm
An implementation of a Kerberos KCM server. Use this package if you want to
use the KCM: Kerberos credentials cache.

%prep
# Update timestamps on the files touched by a patch, to avoid non-equal
# .pyc/.pyo files across the multilib peers within a build, where "Level"
# is the patch prefix option (e.g. -p1)
# Taken from specfile for python-simplejson
UpdateTimestamps() {
  Level=$1
  PatchFile=$2

  # Locate the affected files:
  for f in $(diffstat $Level -l $PatchFile); do
    # Set the files to have the same timestamp as that of the patch:
    touch -r $PatchFile $f
  done
}

%setup -q

for p in %patches ; do
    %__patch -p1 -i $p
    UpdateTimestamps -p1 $p
done

%build
autoreconf -ivf

# This is a hack to get it building, as libwbclient is not resolved
# Anyways, libwbclient is deprecated and the dependency will be removed soon.
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib/samba/wbclient/"

%configure \
    --with-smb-idmap-interface-version=5 \
    --with-test-dir=/dev/shm \
    --with-db-path=%{dbpath} \
    --with-mcache-path=%{mcpath} \
    --with-pipe-path=%{pipepath} \
    --with-pubconf-path=%{pubconfpath} \
    --with-gpo-cache-path=%{gpocachepath} \
    --with-init-dir=%{_initrddir} \
    --with-krb5-rcache-dir=%{_localstatedir}/cache/krb5rcache \
    --with-pid-path=%{_rundir} \
    --enable-nsslibdir=%{_libdir} \
    --enable-pammoddir=%{_libdir}/security \
    --enable-nfsidmaplibdir=%{_libdir}/libnfsidmap \
    --disable-static \
    --disable-rpath \
    --with-libwbclient \
    --with-initscript=systemd \
    --with-syslog=journald \
    --without-python2-bindings \
%if (0%{?use_openssl} == 1)
    --with-crypto=libcrypto \
%endif
    --enable-sss-default-nss-plugin \
    --enable-files-domain \
    %{?with_cifs_utils_plugin_option} \
    %{?enable_systemtap_opt}

make %{?_smp_mflags} all docs runstatedir=%{_rundir}

sed -i -e 's:/usr/bin/python:/usr/bin/python3:' src/tools/sss_obfuscate

%check
export CK_TIMEOUT_MULTIPLIER=10
make %{?_smp_mflags} check VERBOSE=yes
unset CK_TIMEOUT_MULTIPLIER

%install

make install DESTDIR=$RPM_BUILD_ROOT

if [ ! -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/modules/libwbclient.so.%{libwbc_lib_version} ]
then
    echo "Expected libwbclient version not found, please check if version has changed."
    exit -1
fi


# Prepare language files
/usr/lib/rpm/find-lang.sh $RPM_BUILD_ROOT sssd

# Copy default logrotate file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d
install -m644 src/examples/logrotate $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/sssd

# Make sure SSSD is able to run on read-only root
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rwtab.d
install -m644 src/examples/rwtab $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/sssd

# Kerberos KCM credential cache by default
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/krb5.conf.d
cp $RPM_BUILD_ROOT/%{_datadir}/sssd-kcm/kcm_default_ccache \
   $RPM_BUILD_ROOT/%{_sysconfdir}/krb5.conf.d/kcm_default_ccache

# Create directory for cifs-idmap alternative
# Otherwise this directory could not be owned by sssd-client
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/cifs-utils

# Remove .la files created by libtool
find $RPM_BUILD_ROOT -name "*.la" -exec rm -f {} \;

# Suppress developer-only documentation
rm -Rf ${RPM_BUILD_ROOT}/%{_docdir}/%{name}

# Older versions of rpmbuild can only handle one -f option
# So we need to append to the sssd*.lang file
for file in `ls $RPM_BUILD_ROOT/%{python3_sitelib}/*.egg-info 2> /dev/null`
do
    echo %{python3_sitelib}/`basename $file` >> python3_sssdconfig.lang
done

touch sssd.lang
for subpackage in sssd_ldap sssd_krb5 sssd_ipa sssd_ad sssd_proxy sssd_tools \
                  sssd_client sssd_dbus sssd_nfs_idmap sssd_winbind_idmap \
                  libsss_certmap sssd_kcm
do
    touch $subpackage.lang
done

for man in `find $RPM_BUILD_ROOT/%{_mandir}/??/man?/ -type f | sed -e "s#$RPM_BUILD_ROOT/%{_mandir}/##"`
do
    lang=`echo $man | cut -c 1-2`
    case `basename $man` in
        sss_cache*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
        sss_ssh*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
        sss_rpcidmapd*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_nfs_idmap.lang
            ;;
        sss_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_tools.lang
            ;;
        sssctl*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_tools.lang
            ;;
        sssd_krb5_*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        pam_sss*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_client.lang
            ;;
        sssd-ldap*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ldap.lang
            ;;
        sssd-krb5*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_krb5.lang
            ;;
        sssd-ipa*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ipa.lang
            ;;
        sssd-ad*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_ad.lang
            ;;
        sssd-proxy*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_proxy.lang
            ;;
        sssd-ifp*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_dbus.lang
            ;;
        sssd-kcm*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_kcm.lang
            ;;
        idmap_sss*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd_winbind_idmap.lang
            ;;
        sss-certmap*)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> libsss_certmap.lang
            ;;
        *)
            echo \%lang\(${lang}\) \%{_mandir}/${man}\* >> sssd.lang
            ;;
    esac
done

# Print these to the rpmbuild log
echo "sssd.lang:"
cat sssd.lang

echo "python3_sssdconfig.lang:"
cat python3_sssdconfig.lang

for subpackage in sssd_ldap sssd_krb5 sssd_ipa sssd_ad sssd_proxy sssd_tools \
                  sssd_client sssd_dbus sssd_nfs_idmap sssd_winbind_idmap \
                  libsss_certmap sssd_kcm
do
    echo "$subpackage.lang:"
    cat $subpackage.lang
done

%files
%license COPYING

%files common -f sssd.lang
%license COPYING
%doc src/examples/sssd-example.conf
%{_sbindir}/sssd
%{_unitdir}/sssd.service
%{_unitdir}/sssd-autofs.socket
%{_unitdir}/sssd-autofs.service
%{_unitdir}/sssd-nss.socket
%{_unitdir}/sssd-nss.service
%{_unitdir}/sssd-pac.socket
%{_unitdir}/sssd-pac.service
%{_unitdir}/sssd-pam.socket
%{_unitdir}/sssd-pam-priv.socket
%{_unitdir}/sssd-pam.service
%{_unitdir}/sssd-ssh.socket
%{_unitdir}/sssd-ssh.service
%{_unitdir}/sssd-sudo.socket
%{_unitdir}/sssd-sudo.service

%dir %{_libexecdir}/%{servicename}
%{_libexecdir}/%{servicename}/sssd_be
%{_libexecdir}/%{servicename}/sssd_nss
%{_libexecdir}/%{servicename}/sssd_pam
%{_libexecdir}/%{servicename}/sssd_autofs
%{_libexecdir}/%{servicename}/sssd_ssh
%{_libexecdir}/%{servicename}/sssd_sudo
%{_libexecdir}/%{servicename}/p11_child
%{_libexecdir}/%{servicename}/sssd_check_socket_activated_responders

%dir %{_libdir}/%{name}
# The files provider is intentionally packaged in -common
%{_libdir}/%{name}/libsss_files.so
%{_libdir}/%{name}/libsss_simple.so

#Internal shared libraries
%{_libdir}/%{name}/libsss_child.so
%{_libdir}/%{name}/libsss_crypt.so
%{_libdir}/%{name}/libsss_cert.so
%{_libdir}/%{name}/libsss_debug.so
%{_libdir}/%{name}/libsss_krb5_common.so
%{_libdir}/%{name}/libsss_ldap_common.so
%{_libdir}/%{name}/libsss_util.so
%{_libdir}/%{name}/libsss_semanage.so
%{_libdir}/%{name}/libifp_iface.so
%{_libdir}/%{name}/libifp_iface_sync.so
%{_libdir}/%{name}/libsss_iface.so
%{_libdir}/%{name}/libsss_iface_sync.so
%{_libdir}/%{name}/libsss_sbus.so
%{_libdir}/%{name}/libsss_sbus_sync.so

%{ldb_modulesdir}/memberof.so
%{_bindir}/sss_ssh_authorizedkeys
%{_bindir}/sss_ssh_knownhostsproxy
%{_sbindir}/sss_cache
%{_libexecdir}/%{servicename}/sss_signal

%dir %{sssdstatedir}
%dir %{_localstatedir}/cache/krb5rcache
%attr(700,root,root) %dir %{dbpath}
%attr(775,root,root) %dir %{mcpath}
%attr(700,root,root) %dir %{secdbpath}
%attr(751,root,root) %dir %{deskprofilepath}
%ghost %attr(0664,root,root) %verify(not md5 size mtime) %{mcpath}/passwd
%ghost %attr(0664,root,root) %verify(not md5 size mtime) %{mcpath}/group
%ghost %attr(0664,root,root) %verify(not md5 size mtime) %{mcpath}/initgroups
%attr(755,root,root) %dir %{pipepath}
%attr(700,root,root) %dir %{pipepath}/private
%attr(755,root,root) %dir %{pubconfpath}
%attr(755,root,root) %dir %{gpocachepath}
%attr(750,root,root) %dir %{_var}/log/%{name}
%attr(700,root,root) %dir %{_sysconfdir}/sssd
%attr(711,root,root) %dir %{_sysconfdir}/sssd/conf.d
%if (0%{?use_openssl} == 1)
%attr(711,root,root) %dir %{_sysconfdir}/sssd/pki
%endif
%ghost %attr(0600,root,root) %config(noreplace) %{_sysconfdir}/sssd/sssd.conf
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/sssd
%dir %{_sysconfdir}/rwtab.d
%config(noreplace) %{_sysconfdir}/rwtab.d/sssd
%dir %{_datadir}/sssd
%{_sysconfdir}/pam.d/sssd-shadowutils
%dir %{_libdir}/%{name}/conf
%{_libdir}/%{name}/conf/sssd.conf

%{_datadir}/sssd/cfg_rules.ini
%{_datadir}/sssd/sssd.api.conf
%{_datadir}/sssd/sssd.api.d
%{_mandir}/man1/sss_ssh_authorizedkeys.1*
%{_mandir}/man1/sss_ssh_knownhostsproxy.1*
%{_mandir}/man5/sssd.conf.5*
%{_mandir}/man5/sssd-files.5*
%{_mandir}/man5/sssd-simple.5*
%{_mandir}/man5/sssd-sudo.5*
%{_mandir}/man5/sssd-session-recording.5*
%{_mandir}/man8/sssd.8*
%{_mandir}/man8/sss_cache.8*
%dir %{_datadir}/sssd/systemtap
%{_datadir}/sssd/systemtap/id_perf.stp
%{_datadir}/sssd/systemtap/nested_group_perf.stp
%{_datadir}/sssd/systemtap/dp_request.stp
%{_datadir}/sssd/systemtap/ldap_perf.stp
%dir %{_datadir}/systemtap
%dir %{_datadir}/systemtap/tapset
%{_datadir}/systemtap/tapset/sssd.stp
%{_datadir}/systemtap/tapset/sssd_functions.stp
%{_mandir}/man5/sssd-systemtap.5*


%files ldap -f sssd_ldap.lang
%license COPYING
%{_libdir}/%{name}/libsss_ldap.so
%{_mandir}/man5/sssd-ldap.5*
%{_mandir}/man5/sssd-ldap-attributes.5*

%files krb5-common
%license COPYING
%attr(755,root,root) %dir %{pubconfpath}/krb5.include.d
%{_libexecdir}/%{servicename}/ldap_child
%{_libexecdir}/%{servicename}/krb5_child

%files krb5 -f sssd_krb5.lang
%license COPYING
%{_libdir}/%{name}/libsss_krb5.so
%{_mandir}/man5/sssd-krb5.5*

%files common-pac
%license COPYING
%{_libexecdir}/%{servicename}/sssd_pac

%files ipa -f sssd_ipa.lang
%license COPYING
%attr(700,root,root) %dir %{keytabdir}
%{_libdir}/%{name}/libsss_ipa.so
%{_libexecdir}/%{servicename}/selinux_child
%{_mandir}/man5/sssd-ipa.5*

%files ad -f sssd_ad.lang
%license COPYING
%{_libdir}/%{name}/libsss_ad.so
%{_libexecdir}/%{servicename}/gpo_child
%{_mandir}/man5/sssd-ad.5*

%files proxy
%license COPYING
%{_libexecdir}/%{servicename}/proxy_child
%{_libdir}/%{name}/libsss_proxy.so

%files dbus -f sssd_dbus.lang
%license COPYING
%{_libexecdir}/%{servicename}/sssd_ifp
%{_mandir}/man5/sssd-ifp.5*
%{_unitdir}/sssd-ifp.service
# InfoPipe DBus plumbing
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.sssd.infopipe.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.sssd.infopipe.service

%files -n libsss_simpleifp
%{_libdir}/libsss_simpleifp.so.*

%files -n libsss_simpleifp-devel
%doc sss_simpleifp_doc/html
%{_includedir}/sss_sifp.h
%{_includedir}/sss_sifp_dbus.h
%{_libdir}/libsss_simpleifp.so
%{_libdir}/pkgconfig/sss_simpleifp.pc

%files client -f sssd_client.lang
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libnss_sss.so.2
%{_libdir}/security/pam_sss.so
%{_libdir}/krb5/plugins/libkrb5/sssd_krb5_locator_plugin.so
%{_libdir}/krb5/plugins/authdata/sssd_pac_plugin.so
%dir %{_libdir}/cifs-utils
%{_libdir}/cifs-utils/cifs_idmap_sss.so
%dir %{_sysconfdir}/cifs-utils
%ghost %{_sysconfdir}/cifs-utils/idmap-plugin
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/sssd_krb5_localauth_plugin.so
%{_mandir}/man8/pam_sss.8*
%{_mandir}/man8/sssd_krb5_locator_plugin.8*

%files -n libsss_sudo
%license src/sss_client/COPYING
%{_libdir}/libsss_sudo.so*

%files -n libsss_autofs
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/libsss_autofs.so

%files tools -f sssd_tools.lang
%license COPYING
%{_sbindir}/sss_obfuscate
%{_sbindir}/sss_override
%{_sbindir}/sss_debuglevel
%{_sbindir}/sss_seed
%{_sbindir}/sssctl
%{_mandir}/man8/sss_obfuscate.8*
%{_mandir}/man8/sss_override.8*
%{_mandir}/man8/sss_debuglevel.8*
%{_mandir}/man8/sss_seed.8*
%{_mandir}/man8/sssctl.8*

%files -n python3-sssdconfig -f python3_sssdconfig.lang
%dir %{python3_sitelib}/SSSDConfig
%{python3_sitelib}/SSSDConfig/*.py*
%dir %{python3_sitelib}/SSSDConfig/__pycache__
%{python3_sitelib}/SSSDConfig/__pycache__/*.py*

%files -n python3-sss
%{python3_sitearch}/pysss.so

%files -n python3-sss-murmur
%{python3_sitearch}/pysss_murmur.so

%files -n libsss_idmap
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_idmap.so.*

%files -n libsss_idmap-devel
%doc idmap_doc/html
%{_includedir}/sss_idmap.h
%{_libdir}/libsss_idmap.so
%{_libdir}/pkgconfig/sss_idmap.pc

%files -n libipa_hbac
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libipa_hbac.so.*

%files -n libipa_hbac-devel
%doc hbac_doc/html
%{_includedir}/ipa_hbac.h
%{_libdir}/libipa_hbac.so
%{_libdir}/pkgconfig/ipa_hbac.pc

%files -n libsss_nss_idmap
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_nss_idmap.so.*

%files -n libsss_nss_idmap-devel
%doc nss_idmap_doc/html
%{_includedir}/sss_nss_idmap.h
%{_libdir}/libsss_nss_idmap.so
%{_libdir}/pkgconfig/sss_nss_idmap.pc

%files -n python3-libsss_nss_idmap
%{python3_sitearch}/pysss_nss_idmap.so

%files -n python3-libipa_hbac
%{python3_sitearch}/pyhbac.so

%files libwbclient
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/modules
%{_libdir}/%{name}/modules/libwbclient.so.*

%files libwbclient-devel
%{_includedir}/wbclient_sssd.h
%{_libdir}/%{name}/modules/libwbclient.so
%{_libdir}/pkgconfig/wbclient_sssd.pc

%files winbind-idmap -f sssd_winbind_idmap.lang
%dir %{_libdir}/samba/idmap
%{_libdir}/samba/idmap/sss.so
%{_mandir}/man8/idmap_sss.8*

%files nfs-idmap -f sssd_nfs_idmap.lang
%{_mandir}/man5/sss_rpcidmapd.5*
%{_libdir}/libnfsidmap/sss.so

%files -n libsss_certmap -f libsss_certmap.lang
%license src/sss_client/COPYING src/sss_client/COPYING.LESSER
%{_libdir}/libsss_certmap.so.*
%{_mandir}/man5/sss-certmap.5*

%files -n libsss_certmap-devel
%doc certmap_doc/html
%{_includedir}/sss_certmap.h
%{_libdir}/libsss_certmap.so
%{_libdir}/pkgconfig/sss_certmap.pc

%files kcm -f sssd_kcm.lang
%{_libexecdir}/%{servicename}/sssd_kcm
%config(noreplace) %{_sysconfdir}/krb5.conf.d/kcm_default_ccache
%dir %{_datadir}/sssd-kcm
%{_datadir}/sssd-kcm/kcm_default_ccache
%{_unitdir}/sssd-kcm.socket
%{_unitdir}/sssd-kcm.service
%{_mandir}/man8/sssd-kcm.8*
%{_libdir}/%{name}/libsss_secrets.so

%post common
%systemd_post sssd.service
%systemd_post sssd-autofs.socket
%systemd_post sssd-nss.socket
%systemd_post sssd-pac.socket
%systemd_post sssd-pam.socket
%systemd_post sssd-pam-priv.socket
%systemd_post sssd-ssh.socket
%systemd_post sssd-sudo.socket

%preun common
%systemd_preun sssd.service
%systemd_preun sssd-autofs.socket
%systemd_preun sssd-nss.socket
%systemd_preun sssd-pac.socket
%systemd_preun sssd-pam.socket
%systemd_preun sssd-pam-priv.socket
%systemd_preun sssd-ssh.socket
%systemd_preun sssd-sudo.socket

%postun common
%systemd_postun_with_restart sssd-autofs.socket
%systemd_postun_with_restart sssd-autofs.service
%systemd_postun_with_restart sssd-nss.socket
%systemd_postun_with_restart sssd-nss.service
%systemd_postun_with_restart sssd-pac.socket
%systemd_postun_with_restart sssd-pac.service
%systemd_postun_with_restart sssd-pam.socket
%systemd_postun_with_restart sssd-pam-priv.socket
%systemd_postun_with_restart sssd-pam.service
%systemd_postun_with_restart sssd-ssh.socket
%systemd_postun_with_restart sssd-ssh.service
%systemd_postun_with_restart sssd-sudo.socket
%systemd_postun_with_restart sssd-sudo.service

%post dbus
%systemd_post sssd-ifp.service

%preun dbus
%systemd_preun sssd-ifp.service

%postun dbus
%systemd_postun_with_restart sssd-ifp.service

%post kcm
%systemd_post sssd-kcm.socket

%preun kcm
%systemd_preun sssd-kcm.socket

%postun kcm
%systemd_postun_with_restart sssd-kcm.socket
%systemd_postun_with_restart sssd-kcm.service

%post client
%{?ldconfig}
/usr/sbin/alternatives --install /etc/cifs-utils/idmap-plugin cifs-idmap-plugin %{_libdir}/cifs-utils/cifs_idmap_sss.so 20

%preun client
if [ $1 -eq 0 ] ; then
        /usr/sbin/alternatives --remove cifs-idmap-plugin %{_libdir}/cifs-utils/cifs_idmap_sss.so
fi

%ldconfig_postun client

%ldconfig_scriptlets -n libsss_sudo

%ldconfig_scriptlets -n libipa_hbac

%ldconfig_scriptlets -n libsss_idmap

%ldconfig_scriptlets -n libsss_nss_idmap

%ldconfig_scriptlets -n libsss_simpleifp

%ldconfig_scriptlets -n libsss_certmap

%posttrans common
%systemd_postun_with_restart sssd.service

%posttrans libwbclient
%{_sbindir}/update-alternatives \
    --install %{_libdir}/libwbclient.so.%{libwbc_alternatives_version} \
              libwbclient.so.%{libwbc_alternatives_version}%{libwbc_alternatives_suffix} \
              %{_libdir}/%{name}/modules/libwbclient.so.%{libwbc_lib_version} 5
/sbin/ldconfig

%preun libwbclient
%{_sbindir}/update-alternatives \
    --remove libwbclient.so.%{libwbc_alternatives_version}%{libwbc_alternatives_suffix} \
             %{_libdir}/%{name}/modules/libwbclient.so.%{libwbc_lib_version}
/sbin/ldconfig

%posttrans libwbclient-devel
%{_sbindir}/update-alternatives --install %{_libdir}/libwbclient.so \
                                libwbclient.so%{libwbc_alternatives_suffix} \
                                %{_libdir}/%{name}/modules/libwbclient.so 5

%preun libwbclient-devel
%{_sbindir}/update-alternatives --remove \
                                libwbclient.so%{libwbc_alternatives_suffix} \
                                %{_libdir}/%{name}/modules/libwbclient.so

%changelog
* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.1-4
- Added missing BR on 'cyrus-sasl-devel'.

* Thu Aug 19 2021 Muhammad Falak <mwani@microsoft.com> - 2.3.1-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add explict BuildRequires for `libwbclient-devel` which provides libwbclient
- Remove dependency on `selinux-policy-targeted`
- Use smb-idmap-interface-version=5
- Append `/usr/lib/samba/wbclient` to LD_LIBRARY_PATH to resolve `libwbclient`

* Mon Jul 27 2020 Pavel Březina <pbrezina@redhat.com> - 2.3.1-2
- Use correct run dir (RHBZ#1557622)

* Fri Jul 24 2020 Pavel Březina <pbrezina@redhat.com> - 2.3.1-1
- Rebase to SSSD 2.3.1

* Wed May 20 2020 Pavel Březina <pbrezina@redhat.com> - 2.3.0-1
- Rebase to SSSD 2.3.0

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-13
- Resolves: upstream#4159 - p11_child should have an option to skip
                            C_WaitForSlotEvent if the PKCS#11 module does not
                            implement it properly

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-12
- Resolves: upstream#4135 - util/sss_ptr_hash.c: potential double free in
                            `sss_ptr_hash_delete_cb()`

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-11
- Resolves: upstream#4118 - sssd requires timed sudoers ldap entries to be
  specified up to the seconds

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-11
- Add sssd-dbus package as a dependency of sssd-tools

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-10
- Resolves: upstream#4142 - sssd_be frequent crash

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-9
- Resolves: upstream#4131 Force LDAPS over 636 with AD Provider

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-8
- Resolves: upstream#3630 - Randomize ldap_connection_expire_timeout either
                            by default or w/ a configure option

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-7
- Resolves: upstream#4135 - util/sss_ptr_hash.c: potential double free in
                            `sss_ptr_hash_delete_cb()`
* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-6
- Resolves: upstream#4088 - server/be: SIGTERM handling is incorrect

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-5
- Resolves: upstream##4089 Watchdog implementation or usage is incorrect

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-4
- Resolves: upstream#4126 pcscd rejecting sssd ldap_child as unauthorized

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-3
- Resolves: upstream#4127 - [Doc]Provide explanation on escape character for
                            match rules sss-certmap

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-2
- Resolves: upstream#4129 - sssctl config-check command does not give proper
                            error messages with line numbers

* Wed Feb 26 2020 Michal Židek <mzidek@redhat.com> - 2.2.3-1
- Update to latest released upstream version
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_2_2_3.htm

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Stephen Gallagher <sgallagh@redhat.com> - 2.2.2-5
- Fix build against samba-4.12.0rc1

* Fri Jan 24 2020 Mohan Boddu <mboddu@bhujji.com> - 2.2.2-4
- Rebuild for samba-4.12.0rc1

* Tue Oct 22 2019 Adam Williamson <awilliam@redhat.com> - 2.2.2-3
- Resolves: rhbz#1755643 - Upgrade to sssd 2.2.2-1.fc30 breaks setting
                           up FreeIPA replica in containers

* Tue Oct 22 2019 Adam Williamson <awilliam@redhat.com> - 2.2.2-2
- Resolves: rhbz#1757224 - Tickets act like they're expiring prematurely
                           when using KCM cache

* Wed Sep 11 2019 Michal Židek <mzidek@redhat.com> - 2.2.2-1
- Update to latest released upstream version
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_2_2_2.html
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_2_2_1.html

* Mon Aug 26 2019 Stephen Gallagher <sgallagh@redhat.com> - 2.2.0-6
- Rebuilding for libldb 2.0.5

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.2.0-5
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul  5 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.2.0-3
- Resolves: rhbz#1721636 - sssd-kcm calls sssd-genconf which triggers
                           nscd warning

* Fri Jul  5 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.2.0-2
- Resolves: rhbz#1724717 - sssd-proxy crashes resolving groups with
                           no members

* Mon Jun 17 2019 Michal Židek <mzidek@redhat.com> - 2.2.0-1
- Update to latest released upstream version
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_2_2_0.html

* Wed Mar 27 2019 Michal Židek <mzidek@redhat.com> - 2.1.0-2
- Resolves: upstream#3867 - [RFE] Need an option in SSSD so that it will skip
                             GPOs that have groupPolicyContainers unreadable
                             by SSSD.
- CVE-2018-16838

* Wed Mar 27 2019 Michal Židek <mzidek@redhat.com> - 2.1.0-1
- Update to latest released upstream version
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_2_1_0.html

* Wed Feb 13 2019 Sinny Kumari <skumari@redhat.com> - 2.0.0-9
- Resolves: rhbz#1667444 -  sssd: make python3-sssdconfig as suggest

* Wed Feb 13 2019 Adam Williamson <awilliam@redhat.com> - 2.0.0-8
- Resolves: rhbz#1676946 - startup fail with status NOTIMPLEMENTED

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Adam Williamson <awilliam@redhat.com> - 2.0.0-6
- Resolves: rhbz#1654537 - sbus: use 120 second default timeout
- Backport two other patches from master to fix build with recent krb5

* Wed Nov 07 2018 Michal Židek <mzidek@redhat.com> - 2.0.0-5
- Resolves: rhbz#1629737 - sssd: Remove python2 (sub)packages from Fedora 30+

* Wed Aug 29 2018 Michal Židek <mzidek@redhat.com> - 2.0.0-4
- Resolves: upstream#3821 - crash related to sbus_router_destructor()
- Resolves: upstream#3810 - sbus2: fix memory leak in sbus_message_bound_ref
- Resolves: upstream#3819 - sssd only sets the SELinux login context if it
                            differs from the default
- Resolves: upstream#3807 - The sbus codegen script relies on "python" which
                            might not be available on all distributions
- Resolves: upstream#3820 - sudo: search with lower cased name for case
                            insensitive domains
- Resolves: upstream#3701 - [RFE] Allow changing default behavior of SSSD from
                            an allow-any default to a deny-any default when it
                            can't find any GPOs to apply to a user login.
- Resolves: upstream#3828 - Invalid domain provider causes SSSD to abort
                            startup
- Resolves: upstream#3500 - Make sure sssd is a replacement for pam_pkcs11
                            also for local account authentication
- Resolves: upstream#3812 - sssd 2.0.0 segfaults on startup
- Resolves: upstream#3826 - Remove references of sss_user/group/add/del
                            commands in man pages since local provider is
                            deprecated
- Resolves: upstream#3827 - SSSD should log to syslog if a domain is not
                            started due to a misconfiguration
- Resolves: upstream#3830 - Printing incorrect information about domain with
                            sssctl utility
- Resolves: upstream#3489 - p11_child should work wit openssl1.0+
- Resolves: upstream#3750 - [RFE] man 5 sssd-files should mention necessary
                            changes in nsswitch.conf
- Resovles: upstream#3650 - RFE: Require smartcard authentication
- Resolves: upstream#3334 - sssctl config-check does not check any special
                            characters in domain name of domain section
- Resolves: upstream#3849 - Files: The files provider always enumerates
                            which causes duplicate when running getent passwd
- Related: upstream#3855 - session not recording for local user when groups
                           defined
- Resolves: upstream#3802 - Reuse sysdb_error_to_errno() outside sysdb
- Related: upstream#3493 - Remove the pysss.local interface

* Wed Aug 29 2018 Michal Židek <mzidek@redhat.com> - 2.0.0-3
- Resolves: rhbz#1622760 - Console login as FreeIPA domain user fails in
                           current Fedora Rawhide / 29

* Wed Aug 29 2018 Michal Židek <mzidek@redhat.com> - 2.0.0-2
- Fix linking issues

* Tue Aug 14 2018 Michal Židek <mzidek@redhat.com> - 2.0.0-1
- New upstream release 2.0.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.16.2-5
- Rebuilt for Python 3.7

* Mon Jun 25 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.2-4
- Related: upstream#941 - return multiple server addresses to the Kerberos
                          locator plugin
- Related: upstream#3652 - kdcinfo doesn't get populated for other domains
- Resolves: upstream#3747 - sss_ssh_authorizedkeys exits abruptly if SSHD
                            closes its end of the pipe before reading all the
                            SSH keys
- Resolves: upstream#3607 - Handle conflicting e-mail addresses more gracefully
- Resolves: upstream#3754 - SSSD AD uses LDAP filter to detect POSIX attributes
                            stored in AD GC also for regular AD DC queries
- Related: upstream#3219 - [RFE] Regular expression used in sssd.conf not being
                           able to consume an @-sign in the user/group name.
- Resolves: upstream#3766 - CVE-2018-10852: information leak from the sssd-sudo
                            responder

* Thu Jun 21 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.2-3
- Resolves: rhbz#1591804 - something keeps /lib/libnss_systemd.so.2 open on
                           minimal appliance image, breaking composes

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.16.2-2
- Rebuilt for Python 3.7

* Mon Jun 11 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.2-1
- New upstream release 1.16.2
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_1_16_2.html

* Thu May 24 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-9
- Related: upstream#3742 - Change of: User may not run sudo --> a password is
                           required

* Thu May 17 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-8
- Revert 589d1a48 as the builders are back to f27

* Wed May 16 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-7
- Related: upstream#3436 - Certificates used in unit tests have limited
                           lifetime
- Add: "ExcludeArch: armv7hl"

* Mon May 14 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-6
- Related: upstream#3436 - Add openssl, openssh and nss-tools as BuildRequires

* Mon May 14 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-5
- Related: upstream#3436 - Certificates used in unit tests have limited
                           lifetime
- Resolves: upstream#3725 - sssd not honoring dyndns_server if the DNS update
                            process is terminated with a signal
- Resolves: upstream#3726 - SSSD with ID provider 'ad' should give a warning
                            in case the ldap schema is manually changed to
                            something different than 'ad'.
- Related: upstream#2653 - Group renaming issue when "id_provider = ldap" is
                           set.
- Resolves: upstream#3719 - The SSSD IPA provider allocates information about
                            external groups on a long lived memory context,
                            causing memory growth of the sssd_be process
- Resolves: upstream#3728 - Request by ID outside the min_id/max_id limit of a
                            first domain does not reach the second domain
- Resolves: upstream#3731 - nss_clear_netgroup_hash_table(): only remove
                            entries from the hash table, do not free them
- Resolves: upstream#3595 - ID override GID from Default Trust View is not
                            properly resolved in case domain resolution order
                            is set

* Sat May 05 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-4
- Resolves: rhbz#1574778 - sssd fails to download known_hosts from freeipa

* Fri Apr 27 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-3
- Resolves: upstream#3684 - A group is not updated if its member is removed
                            with the cleanup task, but the group does not
                            change
- Resolves: upstream#3558 - sudo: report error when two rules share cn
- Tone down shutdown messages for socket activated responders
- IPA: Qualify the externalUser sudo attribute
- Resolves: upstream#3550 - refresh_expired_interval does not work with
                            netgrous in 1.15
- Resolves: upstream#3402 - Support alternative sources for the files provider
- Resolves: upstream#3646 - SSSD's GPO code ignores ad_site option
- Resolves: upstream#3679 - Make nss netgroup requests more robust
- Resolves: upstream#3634 - sssctl COMMAND --help fails if sssd is not
                            configured
- Resolves: upstream#3469 - extend sss-certmap man page regarding priority
                            processing
- Improve docs/debug message about GC detection
- Resolves: upstream#3715 - ipa 389-ds-base crash in krb5-libs - k5_copy_etypes
                            list out of bound?
- Resolves: upstream#2653 - Group renaming issue when "id_provider = ldap" is
                            set.
- Document which principal does the AD provider use
- Resolves: upstream#3680 - GPO: SSSD fails to process GPOs If a rule is
                            defined, but contains no SIDs
- Resolves: upstream#3520 - Files provider supports only BE_FILTER_ENUM
- Resolves: rhbz#1540703 - FreeIPA/SSSD implicit_file sssd_nss error: The Data
                           Provider returned an error
                           [org.freedesktop.sssd.Error.DataProvider.Fatal]
- Add gcc to build dependencies

* Fri Mar 30 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-2
- Resolves: upstream#3573 - sssd won't show netgroups with blank domain
- Resolves: upstream#3660 - confdb_expand_app_domains() always fails
- Resolves: upstream#3658 - Application domain is not interpreted correctly
- Resolves: upstream#3687 - KCM: Don't pass a non null terminated string to
                            json_loads()
- Resolves: upstream#3386 - KCM: Payload buffer is too small
- Resolves: upstream#3666 - Fix usage of str.decode() in our tests
- A few KCM misc fixes

* Fri Mar  9 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.1-1
- New upstream release 1.16.1
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_1_16_1.html

* Tue Feb 20 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-13
- Resolves: upstream#3621 - backport bug found by static analyzers

* Wed Feb 14 2018 Fabiano Fidêncio <fidencio@fedoraproject.org> - 1.16.0-12
- Resolves: rhbz#1538643 - SSSD crashes when retrieving a Desktop Profile
                           with no specific host/hostgroup set
- Resolves: upstream#3621 - FleetCommander integration must not require
                            capability DAC_OVERRIDE

* Wed Feb 07 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-11
- Resolves: upstream#3618 - selinux_child segfaults in a docker container

* Tue Feb 06 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-10
- Resolves: rhbz#1431153 - sssd: libsss_proxy.so needs to be linked with -ldl

* Thu Jan 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.16.0-9
- Fix systemd executions/requirements

* Thu Jan 25 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-8
- Fix building on rawhide. Remove -Wl,-z,defs from LDFLAGS

* Thu Jan 11 2018 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-7
- Fix building of sssd-nfs-idmap with libnfsidmap.so.1

* Thu Jan 11 2018 Björn Esser <besser82@fedoraproject.org> - 1.16.0-6
- Rebuilt for libnfsidmap.so.1

* Mon Dec 04 2017 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-5
- Resolves: upstream#3523 - ABRT crash - /usr/libexec/sssd/sssd_nss in
                            setnetgrent_result_timeout
- Resolves: upstream#3588 - sssd_nss consumes more memory until restarted
                            or machine swaps
- Resolves: failure in glibc tests
            https://sourceware.org/bugzilla/show_bug.cgi?id=22530
- Resolves: upstream#3451 - When sssd is configured with id_provider proxy and
                            auth_provider ldap, login fails if the LDAP server
                            is not allowing anonymous binds
- Resolves: upstream#3285 - SSSD needs restart after incorrect clock is
                            corrected with AD
- Resolves: upstream#3586 - Give a more detailed debug and system-log message
                            if krb5_init_context() failed
- Resolves: rhbz#1431153 - SSSD ships a drop-in configuration snippet
                           in /etc/systemd/system
- Backport few upstream features from 1.16.1

* Tue Nov 21 2017 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-4
- Resolves: rhbz#1494002 - sssd_nss crashed in cache_req_search_domains_next

* Fri Nov 17 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.16.0-3
- Backport extended NSS API from upstream master branch

* Fri Nov 03 2017 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-2
- Resolves: upstream#3529 - sssd-kcm Fix restart during/after upgrade

* Fri Oct 20 2017 Lukas Slebodnik <lslebodn@fedoraproject.org> - 1.16.0-1
- New upstream release 1.16.0
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_1_16_0.html

* Wed Oct 11 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-5
- Resolves: rhbz#1499354 - CVE-2017-12173 sssd: unsanitized input when
                           searching in local cache database access on
                           the sock_file system_bus_socket

* Mon Sep 11 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-4
- Resolves: rhbz#1488327 - SELinux is preventing selinux_child from write
                           access on the sock_file system_bus_socket
- Resolves: rhbz#1490402 - SSSD does not create /var/lib/sss/deskprofile and
                           fails to download desktop profile data
- Resolves: upstream#3485 - getsidbyid does not work with 1.15.3
- Resolves: upstream#3488 - SUDO doesn't work for IPA users on IPA clients
                            after applying ID Views for them in IPA server
- Resolves: upstream#3501 - Accessing IdM kerberos ticket fails while id
                            mapping is applied

* Fri Sep 01 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-3
- Backport few upstream patches/fixes

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-1
- New upstream release 1.15.3
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_1_15_3.html

* Tue Jun 27 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-0.beta.5
- Rebuild with libldb-1.2.0

* Tue Jun 27 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-0.beta.4
- Fix build issues: Update expided certificate in unit tests

* Sat Apr 29 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-0.beta.3
- Resolves: rhbz#1445680 - Properly fall back to local Smartcard authentication
- Resolves: rhbz#1437199 - sssd-nfs-idmap-1.15.2-1.fc25.x86_64 conflicts with
                           file from package sssd-common-1.15.1-1.fc25.x86_64
- Resolves: rhbz#1063278 - sss_ssh_knownhostsproxy doesn't fall back to ipv4

* Thu Apr 06 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-0.beta.2
- Fix issue with IPA + SELinux in containers
- Resolves: upstream https://fedorahosted.org/sssd/ticket/3297

* Tue Apr 04 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.3-0.beta.1
- Backport upstream patches for 1.15.3 pre-release
- required for building freeipa-4.5.x in rawhide

* Thu Mar 16 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.2-1
- New upstream release 1.15.2
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_1_15_2.html

* Mon Mar 06 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.1-1
- New upstream release 1.15.1
- https://docs.pagure.org/SSSD.sssd/users/relnotes/notes_1_15_1.html

* Wed Feb 22 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.15.0-4
- Cherry-pick patches from upstream that enable the files provider
- Enable the files domain
- Retire patch 0501-Partially-revert-CONFIG-Use-default-config-when-none.patch
  which is superseded by the files domain autoconfiguration
- Related: rhbz#1357418 - SSSD fast cache for local users

* Tue Feb 14 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.0-3
- Add missing %%license macro

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Lukas Slebodnik <lslebodn@redhat.com> - 1.15.0-1
- New upstream release 1.15.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.15.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.14.2-3
- Rebuild for Python 3.6

* Tue Dec 13 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.2-2
- Resolves: rhbz#1369130 - nss_sss should not link against libpthread
- Resolves: rhbz#1392916 - sssd failes to start after update
- Resolves: rhbz#1398789 - SELinux is preventing sssd from 'write' accesses
                           on the directory /etc/sssd

* Thu Oct 20 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.2-1
- New upstream release 1.14.2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.14.2

* Fri Oct 14 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.1-4
- libwbclient-sssd: update interface to version 0.13

* Thu Sep 22 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.1-3
- Fix regression with krb5_map_user
- Resolves: rhbz#1375552 - krb5_map_user doesn't seem effective anymore
- Resolves: rhbz#1349286 - authconfig fails with SSSDConfig.NoDomainError:
                           default if nonexistent domain is mentioned

* Thu Sep 01 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.1-2
- Backport important patches from upstream 1.14.2 prerelease
- Resolves: upstream #3154 - sssd exits if clock is adjusted backwards after
                             boot
- Resolves: upstream #3163 - resolving IPA nested user group is broken in 1.14

* Fri Aug 19 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.1-1
- New upstream release 1.14.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.14.1

* Mon Aug 15 2016 Stephen Gallagher <sgallagh@redhat.com> - 1.14.0-5
- Add workaround patch for RHBZ #1366403

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 08 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.0-3
- New upstream release 1.14.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.14.0

* Fri Jul 01 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.0-2.beta
- New upstream release 1.14 beta
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.14.0beta

* Tue Jun 21 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.14.0-1.alpha
- New upstream release 1.14 alpha
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.14.0alpha

* Fri May 13 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.4-3
- Resolves: rhbz#1335639 - [abrt] sssd-dbus: ldb_msg_find_element():
                           sssd_ifp killed by SIGSEGV

* Fri Apr 22 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.4-2
- Resolves: rhbz#1328108 - Protocol error with FreeIPA on CentOS 6

* Thu Apr 14 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.4-1
- New upstream release 1.13.4
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.13.4

* Tue Mar 22 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.3-6
- Resolves: rhbz#1276868 - Sudo PAM Login should support multiple password
                           prompts (e.g. Password + Token)
- Resolves: rhbz#1313041 - ssh with sssd proxy fails with "Connection closed
                           by remote host" if locale not available

* Thu Feb 25 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.3-5
- Resolves: rhbz#1310664 - [RFE] IPA: resolve external group memberships of IPA
                           groups during getgrnam and getgrgid
- Resolves: rhbz#1301303 - sss_obfuscate: SyntaxError: Missing parentheses
                           in call to 'print'

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.3-3
- Additional upstream fixes

* Tue Jan 19 2016 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.3-2
- Resolves: rhbz#1256849 - SUDO: Support the IPA schema

* Wed Dec 16 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.3-1
- New upstream release 1.13.3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.13.3

* Fri Nov 20 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.2-1
- New upstream release 1.13.2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.13.2

* Fri Nov 06 2015 Robert Kuska <rkuska@redhat.com> - 1.13.1-5
- Rebuilt for Python3.5 rebuild

* Tue Oct 27 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.1-4
- Fix building pac responder with the krb5-1.14

* Mon Oct 19 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.1-3
- python-sssdconfig: Fix parssing sssd.conf without config_file_version
- Resolves: upstream #2837 - REGRESSION: ipa-client-automout failed

* Wed Oct 07 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.1-2
- Fix few segfaults
- Resolves: upstream #2811 - PAM responder crashed if user was not set
- Resolves: upstream #2810 - sssd_be crashed in ipa_srv_ad_acct_lookup_step

* Thu Oct 01 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.1-1
- New upstream release 1.13.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.13.1

* Thu Sep 10 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.0-6
- Fix OTP bug
- Resolves: upstream #2729 - Do not send SSS_OTP if both factors were
                             entered separately

* Mon Sep 07 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.0-5
- Backport upstream patches required by FreeIPA 4.2.1

* Tue Jul 21 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.0-4
- Fix ipa-migration bug
- Resolves: upstream #2719 - IPA: returned unknown dp error code with disabled
                             migration mode

* Wed Jul 08 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.0-3
- New upstream release 1.13.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.13.0

* Tue Jun 30 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.0-2.alpha
- Unify return type of list_active_domains for python{2,3}

* Mon Jun 22 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.13.0-1.alpha
- New upstream release 1.13 alpha
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.13.0alpha

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.5-3
- Fix libwbclient alternatives

* Fri Jun 12 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.5-2
- Backport important patches from upstream 1.13 prerelease

* Fri Jun 12 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.5-1
- New upstream release 1.12.5
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.5

* Fri May 08 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.4-8
- Backport important patches from upstream 1.13 prerelease
- Resolves: rhbz#1060325 - Does sssd-ad use the most suitable
                           attribute for group name
- Resolves: upstream #2335 - Investigate using the krb5 responder
                             for driving the PAM conversation with OTPs
- Enable cmocka tests for secondary architectures

* Fri May 08 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.4-7
- Backport patches from upstream 1.12.5 prerelease - contains many fixes

* Wed Apr 15 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.4-6
- Fix slow login with ipa and SELinux
- Resolves: upstream #2624 - Only set the selinux context if the context
                             differs from the local one

* Mon Mar 23 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.4-5
- Fix regressions with ipa and SELinux
- Resolves: upstream #2587 - With empty ipaselinuxusermapdefault security
                             context on client is staff_u

* Fri Mar  6 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.12.4-4
- Also relax libldb Requires
- Remove --enable-ldb-version-check

* Fri Mar  6 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.12.4-3
- Relax libldb BuildRequires to be greater-or-equal

* Wed Feb 25 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.4-2
- Add support for python3 bindings
- Add requirement to python3 or python3 bindings
- Resolves: rhbz#1014594 - sssd: Support Python 3

* Wed Feb 18 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.4-1
- New upstream release 1.12.4
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.4

* Sat Feb 14 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-7
- Backport patches with Python3 support from upstream

* Thu Feb 12 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-6
- Fix double free in monitor
- Resolves: rhbz#1186887 [abrt] sssd-common: talloc_abort():
                        sssd killed by SIGABRT

* Wed Jan 28 2015 Jakub Hrozek <jhrozek@redhat.com> - 1.12.3-5
- Rebuild for new libldb

* Thu Jan 22 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-4
- Decrease priority of sssd-libwbclient 20 -> 5
- It should be lower than priority of samba veriosn of libwbclient.
- https://bugzilla.redhat.com/show_bug.cgi?id=1175511#c18

* Mon Jan 19 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-3
- Apply a number of patches from upstream to fix issues found 1.12.3
- Resolves: rhbz#1176373 - dyndns_iface does not accept multiple
                           interfaces, or isn't documented to be able to
- Resolves: rhbz#988068 - getpwnam_r fails for non-existing users when sssd is
                          not running
- Resolves: upstream #2557  authentication failure with user from AD

* Fri Jan 09 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-2
- Resolves: rhbz#1164156 - libsss_simpleifp should pull sssd-dbus
- Resolves: rhbz#1179379 - gzip: stdin: file size changed while
                           zipping when rotating logfile

* Thu Jan 08 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.3-1
- New upstream release 1.12.3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.3
- Fix spelling errors in description (fedpkg lint)

* Tue Jan  6 2015 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.2-8
- Rebuild for libldb 1.1.19

* Fri Dec 19 2014 Sumit Bose <sbose@redhat.com> - 1.12.2-7
- Resolves: rhbz#1175511 - sssd-libwbclient conflicts with Samba's and causes
                           crash in wbinfo
                           - in addition to the patch libwbclient.so is
                             filtered out of the Provides list of the package

* Wed Dec 17 2014 Lukas Slebodnik <lslebodn@redhat.com> - 1.12.2-6
- Fix regressions and bugs in sssd upstream 1.12.2
- https://fedorahosted.org/sssd/ticket/{id}
- Regressions: #2471, #2475, #2483, #2487, #2529, #2535
- Bugs: #2287, #2445

* Sun Dec  7 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-5
- Rebuild for libldb 1.1.18

* Wed Nov 26 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-4
- Fix typo in libwbclient-devel %%preun

* Tue Nov 25 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-3
- Use alternatives for libwbclient

* Wed Oct 22 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-2
- Backport several patches from upstream.
- Fix a potential crash against old (pre-4.0) IPA servers

* Mon Oct 20 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.2-1
- New upstream release 1.12.2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.2

* Mon Sep 15 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.1-2
- Resolves: rhbz#1139962 - Fedora 21, FreeIPA 4.0.2: sssd does not find user
                           private group from server

* Mon Sep  8 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.1-1
- New upstream release 1.12.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.1

* Fri Aug 22 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-7
- Do not crash on resolving a group SID in IPA server mode

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Stephen Gallagher <sgallagh@redhat.com> 1.12.0-5
- Fix release version for upgrades

* Wed Jul 09 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-1
- New upstream release 1.12.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.0-4.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-1.beta2
- New upstream release 1.12 beta2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.0beta2

* Mon Jun 02 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-2.beta1
- Fix tests on big-endian
- Fix previous changelog entry

* Fri May 30 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.12.0-1.beta1
- New upstream release 1.12 beta1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.12.0beta1

* Thu May 29 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.5.1-4
- Rebuild against new ding-libs

* Thu May 08 2014 Stephen Gallagher <sgallagh@redhat.com> - 1.11.5.1-3
- Make LDB dependency a strict equivalency

* Thu May 08 2014 Stephen Gallagher <sgallagh@redhat.com> - 1.11.5.1-2
- Rebuild against new libldb

* Fri Apr 11 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.5.1-1
- New upstream release 1.11.5.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.5.1

* Thu Apr 10 2014 Stephen Gallagher <sgallagh@redhat.com> 1.11.5-2
- Fix bug in generation of systemd unit file

* Tue Apr 08 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.5-1
- New upstream release 1.11.5
- Remove upstreamed patch
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.5

* Thu Mar 13 2014 Sumit Bose <sbose@redhat.com> - 1.11.4-3
- Handle new error code for IPA password migration

* Tue Mar 11 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.4-2
- Include couple of patches from upstream 1.11 branch

* Mon Feb 17 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.4-1
- New upstream release 1.11.4
- Remove upstreamed patch
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.4

* Tue Feb 11 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.11.3-2
- Handle OTP response from FreeIPA server gracefully

* Wed Oct 30 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.3-1
- New upstream release 1.11.3
- Remove upstreamed patches
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.3

* Wed Oct 30 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.2-1
- New upstream release 1.11.2
- Remove upstreamed patches
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.2

* Wed Oct 16 2013 Sumit Bose <sbose@redhat.com> - 1.11.1-5
- Fix potential crash with external groups in trusted IPA-AD setup

* Mon Oct 14 2013 Sumit Bose <sbose@redhat.com> - 1.11.1-4
- Add plugin for cifs-utils
- Resolves: rhbz#998544

* Tue Oct 08 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.1-3
- Fix failover from Global Catalog to LDAP in case GC is not available

* Fri Oct 04 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.1-2
- Remove the ability to create public ccachedir (#1015089)

* Fri Sep 27 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.1-1
- New upstream release 1.11.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.1

* Thu Sep 26 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0-3
- Fix multicast checks in the SSSD
- Resolves: rhbz#1007475 - The multicast check is wrong in the sudo source
                           code getting the host info

* Wed Aug 28 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0-2
- Backport simplification of ccache management from 1.11.1
- Resolves: rhbz#1010553 - sssd setting KRB5CCNAME=(null) on login

* Wed Aug 28 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0-1
- New upstream release 1.11.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.0

* Fri Aug 23 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0-0.4.beta2
- Resolves: #967012 - [abrt] sssd-1.9.5-1.fc18: sss_mmap_cache_gr_invalidate_gid:
                      Process /usr/libexec/sssd/sssd_nss was killed by
                      signal 11 (SIGSEGV)
- Resolves: #996214 - sssd proxy_child segfault

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-0.3.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0.2beta2
- Resolves: #906427 - Do not use %%{_lib} in specfile for the nss and
                      pam libraries

* Wed Jul 24 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0.1beta2
- New upstream release 1.11 beta 2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.11.0beta2

* Thu Jul 18 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.1-1
- New upstream release 1.10.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.1

* Mon Jul 08 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-17
- sssd-tools should require sssd-common, not sssd

* Tue Jul 02 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.10.0-16
- Move sssd_pac to the sssd-ipa and sssd-ad subpackages
- Trim out RHEL5-specific macros since we don't build on RHEL 5
- Trim out macros for Fedora older than F18
- Update libldb requirement to 1.1.16
- Trim RPM changelog down to the last year

* Tue Jul 02 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.10.0-15
- Move sssd_pac to the sssd-krb5 subpackage

* Mon Jul 01 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.10.0-14
- Fix Obsoletes: to account for dist tag
- Convert post and pre scripts to run on the sssd-common subpackage
- Remove old conversion from SYSV

* Thu Jun 27 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-13
- New upstream release 1.10
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.0

* Mon Jun 17 2013 Dan Horák <dan[at]danny.cz> - 1.10.0-12.beta2
- the cmocka toolkit exists only on selected arches

* Sun Jun 16 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-11.beta2
- Apply a number of patches from upstream to fix issues found post-beta,
  in particular:
  -- segfault with a high DEBUG level
  -- Fix IPA password migration (upstream #1873)
  -- Fix fail over when retrying SRV resolution (upstream #1886)

* Thu Jun 13 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-10.beta2
- Only BuildRequire libcmocka on Fedora

* Thu Jun 13 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-9.beta2
- Fix typo in Requires that prevented an upgrade (#973916)
- Use a hardcoded version in Conflicts, not less-than-current

* Wed Jun 12 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-8.beta1
- Enable hardened build for RHEL7

* Wed Jun 12 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-8.beta2
- New upstream release 1.10 beta2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.0beta2
- BuildRequire libcmocka-devel in order to run all upstream tests during build
- BuildRequire libnl3 instead of libnl1
- No longer BuildRequire initscripts, we no longer use /sbin/service
- Remove explicit krb5-libs >= 1.10 requires; this platform doensn't carry any
  older krb5-libs version

* Fri May 24 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-7.beta1
- Apply a couple of patches from upstream git that resolve crashes when
  ID mapping object was not initialized properly but needed later

* Tue May 14 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-6.beta1
- Resolves: rhbz#961357 - Missing dyndns_update entry in sssd.conf during
                          realm join
- Resolves: rhbz#961278 - Login failure: Enterprise Principal enabled by
                          default for AD Provider
- Resolves: rhbz#961251 - sssd does not create user's krb5 ccache dir/file
                          parent directory when logging in

* Tue May  7 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-5.beta1
- BuildRequire recent libini_config to ensure consistent behaviour

* Tue May  7 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-4.beta1
- Explicitly Require libini_config >= 1.0.0.1 to work around a SONAME bug
  in ding-libs
- Fix SSH integration with fully-qualified domains
- Add the ability to dynamically discover the NetBIOS name

* Fri May  3 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-3.beta1
- New upstream release 1.10 beta1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.0beta1

* Wed Apr 17 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-2.alpha1
- Add a patch to fix krb5 ccache creation issue with krb5 1.11

* Tue Apr  2 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-1.alpha1
- New upstream release 1.10 alpha1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.10.0alpha1

* Fri Mar 29 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.5-10
- Add a patch to fix krb5 unit tests

* Fri Mar 01 2013 Stephen Gallagher <sgallagh@redhat.com> - 1.9.4-9
- Split internal helper libraries into a shared object
- Significantly reduce disk-space usage

* Thu Feb 14 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-8
- Fix the Kerberos password expiration warning (#912223)

* Thu Feb 14 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-7
- Do not write out dots in the domain-realm mapping file (#905650)

* Mon Feb 11 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-6
- Include upstream patch to build with krb5-1.11

* Thu Feb 07 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-5
- Rebuild against new libldb

* Mon Feb 04 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-4
- Fix build with new automake versions

* Wed Jan 30 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-3
- Recreate Kerberos ccache directory if it's missing
- Resolves: rhbz#853558 - [sssd[krb5_child[PID]]]: Credential cache
                          directory /run/user/UID/ccdir does not exist

* Tue Jan 29 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-2
- Fix changelog dates to make F19 rpmbuild happy

* Mon Jan 28 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.4-1
- New upstream release 1.9.4

* Thu Dec 06 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.3-1
- New upstream release 1.9.3

* Tue Oct 30 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-5
- Resolve groups from AD correctly

* Tue Oct 30 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-4
- Check the validity of naming context

* Thu Oct 18 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-3
- Move the sss_cache tool to the main package

* Sun Oct 14 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-2
- Include the 1.9.2 tarball

* Sun Oct 14 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.2-1
- New upstream release 1.9.2

* Sun Oct 07 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.1-1
- New upstream release 1.9.1

* Wed Oct 03 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-24
- require the latest libldb

* Tue Sep 25 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-24
- Use mcpath insted of mcachepath macro to be consistent with
  upsteam spec file

* Tue Sep 25 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-23
- New upstream release 1.9.0

* Fri Sep 14 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-22.rc1
- New upstream release 1.9.0 rc1

* Thu Sep 06 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-21.beta7
- New upstream release 1.9.0 beta7
- obsoletes patches #1-#3

* Mon Sep 03 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-20.beta6
- Rebuild against libldb 1.12

* Tue Aug 28 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-19.beta6
- Rebuild against libldb 1.11

* Fri Aug 24 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-18.beta6
- Change the default ccache location to DIR:/run/user/${UID}/krb5cc
  and patch man page accordingly
- Resolves: rhbz#851304

* Mon Aug 20 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-17.beta6
- Rebuild against libldb 1.10

* Fri Aug 17 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-16.beta6
- Only create the SELinux login file if there are SELinux mappings on
  the IPA server

* Fri Aug 10 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-14.beta6
- Don't discard HBAC rule processing result if SELinux is on
  Resolves: rhbz#846792 (CVE-2012-3462)

* Thu Aug 02 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-13.beta6
- New upstream release 1.9.0 beta 6
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta6
- A new option, override_shell was added. If this option is set, all users
  managed by SSSD will have their shell set to its value.
- Fixes for the support for setting default SELinux user context from FreeIPA.
- Fixed a regression introduced in beta 5 that broke LDAP SASL binds
- The SSSD supports the concept of a Primary Server and a Back Up Server in
  failover
- A new command-line tool sss_seed is available to help prime the cache with
  a user record when deploying a new machine
- SSSD is now able to discover and save the domain-realm mappings
  between an IPA server and a trusted Active Directory server.
- Packaging changes to fix ldconfig usage in subpackages (#843995)
- Rebuild against libldb 1.1.9

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-13.beta5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-12.beta5
- New upstream release 1.9.0 beta 5
- Obsoletes the patch for missing DP_OPTION_TERMINATOR in AD provider options
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta5
- Many fixes for the support for setting default SELinux user context from
  FreeIPA, most notably fixed the specificity evaluation
- Fixed an incorrect default in the krb5_canonicalize option of the AD
  provider which was preventing password change operation
- The shadowLastChange attribute value is now correctly updated with the
  number of days since the Epoch, not seconds

* Mon Jul 16 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-11.beta4
- Fix broken ARM build
- Add missing DP_OPTION_TERMINATOR in AD provider options

* Wed Jul 11 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-10.beta4
- Own several directories create during make install (#839782)

* Wed Jul 11 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.0-9.beta4
- New upstream release 1.9.0 beta 4
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta4
- Add a new AD provider to improve integration with Active Directory 2008 R2
  or later servers
- SUDO integration was completely rewritten. The new implementation works
  with multiple domains and uses an improved refresh mechanism to download
  only the necessary rules
- The IPA authentication provider now supports subdomains
- Fixed regression for setups that were setting default_tkt_enctypes
  manually by reverting a previous workaround.

* Mon Jun 25 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-8.beta3
- New upstream release 1.9.0 beta 3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta3
- Add a new PAC responder for dealing with cross-realm Kerberos trusts
- Terminate idle connections to the NSS and PAM responders

* Wed Jun 20 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-7.beta2
- Switch unicode library from libunistring to Glib
- Drop unnecessary explicit Requires on keyutils
- Guarantee that versioned Requires include the correct architecture

* Mon Jun 18 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-6.beta2
- Fix accidental disabling of the DIR cache support

* Fri Jun 15 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-5.beta2
- New upstream release 1.9.0 beta 2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta2
- Add support for the Kerberos DIR cache for storing multiple TGTs
  automatically
- Major performance enhancement when storing large groups in the cache
- Major performance enhancement when performing initgroups() against Active
  Directory
- SSSDConfig data file default locations can now be set during configure for
  easier packaging

* Tue May 29 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-4.beta1
- Fix regression in endianness patch

* Tue May 29 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-3.beta1
- Rebuild SSSD against ding-libs 0.3.0beta1
- Fix endianness bug in service map protocol

* Thu May 24 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-2.beta1
- Fix several regressions since 1.5.x
- Ensure that the RPM creates the /var/lib/sss/mc directory
- Add support for Netscape password warning expiration control
- Rebuild against libldb 1.1.6

* Fri May 11 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.9.0-1.beta1
- New upstream release 1.9.0 beta 1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.9.0beta1
- Add native support for autofs to the IPA provider
- Support for ID-mapping when connecting to Active Directory
- Support for handling very large (> 1500 users) groups in Active Directory
- Support for sub-domains (will be used for dealing with trust relationships)
- Add a new fast in-memory cache to speed up lookups of cached data on
  repeated requests

* Thu May 03 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.3-11
- New upstream release 1.8.3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.3
- Numerous manpage and translation updates
- LDAP: Handle situations where the RootDSE isn't available anonymously
- LDAP: Fix regression for users using non-standard LDAP attributes for user
  information

* Mon Apr 09 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.2-10
- New upstream release 1.8.2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.2
- Several fixes to case-insensitive domain functions
- Fix for GSSAPI binds when the keytab contains unrelated principals
- Fixed several segfaults
- Workarounds added for LDAP servers with unreadable RootDSE
- SSH knownhostproxy will no longer enter an infinite loop preventing login
- The provided SYSV init script now starts SSSD earlier at startup and stops
  it later during shutdown
- Assorted minor fixes for issues discovered by static analysis tools

* Mon Mar 26 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.1-9
- Don't duplicate libsss_autofs.so in two packages
- Set explicit package contents instead of globbing

* Wed Mar 21 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.1-8
- Fix uninitialized value bug causing crashes throughout the code
- Resolves: rhbz#804783 - [abrt] Segfault during LDAP 'services' lookup

* Mon Mar 12 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.1-7
- New upstream release 1.8.1
- Resolve issue where we could enter an infinite loop trying to connect to an
  auth server
- Fix serious issue with complex (3+ levels) nested groups
- Fix netgroup support for case-insensitivity and aliases
- Fix serious issue with lookup bundling resulting in requests never
  completing
- IPA provider will now check the value of nsAccountLock during pam_acct_mgmt
  in addition to pam_authenticate
- Fix several regressions in the proxy provider
- Resolves: rhbz#743133 - Performance regression with Kerberos authentication
                          against AD
- Resolves: rhbz#799031 - --debug option for sss_debuglevel doesn't work

* Tue Feb 28 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-6
- New upstream release 1.8.0
- Support for the service map in NSS
- Support for setting default SELinux user context from FreeIPA
- Support for retrieving SSH user and host keys from LDAP (Experimental)
- Support for caching autofs LDAP requests (Experimental)
- Support for caching SUDO rules (Experimental)
- Include the IPA AutoFS provider
- Fixed several memory-corruption bugs
- Fixed a regression in group enumeration since 1.7.0
- Fixed a regression in the proxy provider
- Resolves: rhbz#741981 - Separate Cache Timeouts for SSSD
- Resolves: rhbz#797968 - sssd_be: The requested tar get is not configured is
                          logged at each login
- Resolves: rhbz#754114 - [abrt] sssd-1.6.3-1.fc16: ping_check: Process
                          /usr/sbin/sssd was killed by signal 11 (SIGSEGV)
- Resolves: rhbz#743133 - Performance regression with Kerberos authentication
                          against AD
- Resolves: rhbz#773706 - SSSD fails during autodetection of search bases for
                          new LDAP features
- Resolves: rhbz#786957 - sssd and kerberos should change the default location for create the Credential Cashes to /run/usr/USERNAME/krb5cc

* Wed Feb 22 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-5.beta3
- Change default kerberos credential cache location to /run/user/<username>

* Wed Feb 15 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-4.beta3
- New upstream release 1.8.0 beta 3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.0beta3
- Fixed a regression in group enumeration since 1.7.0
- Fixed several memory-corruption bugs
- Finalized the ABI for the autofs support
- Fixed a regression in the proxy provider

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.8.0-3.beta2
- Rebuild against PCRE 8.30

* Mon Feb 06 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-1.beta2
- New upstream release
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.0beta2
- Fix two minor manpage bugs
- Include the IPA AutoFS provider

* Mon Feb 06 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.8.0-1.beta1
- New upstream release
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.8.0beta1
- Support for the service map in NSS
- Support for setting default SELinux user context from FreeIPA
- Support for retrieving SSH user and host keys from LDAP (Experimental)
- Support for caching autofs LDAP requests (Experimental)
- Support for caching SUDO rules (Experimental)

* Wed Feb 01 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-5
- Resolves: rhbz#773706 - SSSD fails during autodetection of search bases for
                          new LDAP features - fix netgroups and sudo as well

* Wed Feb 01 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-4
- Fixes a serious memory hierarchy bug causing unpredictable behavior in the
  LDAP provider.

* Wed Feb 01 2012 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-3
- Resolves: rhbz#773706 - SSSD fails during autodetection of search bases for
                          new LDAP features

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.7.0-1
- New upstream release 1.7.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.7.0
- Support for case-insensitive domains
- Support for multiple search bases in the LDAP provider
- Support for the native FreeIPA netgroup implementation
- Reliability improvements to the process monitor
- New DEBUG facility with more consistent log levels
- New tool to change debug log levels without restarting SSSD
- SSSD will now disconnect from LDAP server when idle
- FreeIPA HBAC rules can choose to ignore srchost options for significant
  performance gains
- Assorted performance improvements in the LDAP provider

* Mon Dec 19 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.4-1
- New upstream release 1.6.4
- Rolls up previous patches applied to the 1.6.3 tarball
- Fixes a rare issue causing crashes in the failover logic
- Fixes an issue where SSSD would return the wrong PAM error code for users
  that it does not recognize.

* Wed Dec 07 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-5
- Rebuild against libldb 1.1.4

* Tue Nov 29 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-4
- Resolves: rhbz#753639 - sssd_nss crashes when passed invalid UTF-8 for the
                          username in getpwnam()
- Resolves: rhbz#758425 - LDAP failover not working if server refuses
                          connections

* Thu Nov 24 2011 Jakub Hrozek <jhrozek@redhat.com> - 1.6.3-3
- Rebuild for libldb 1.1.3

* Thu Nov 10 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-2
- Resolves: rhbz#752495 - Crash when apply settings

* Fri Nov 04 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.3-1
- New upstream release 1.6.3
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.6.3
- Fixes a major cache performance issue introduced in 1.6.2
- Fixes a potential infinite-loop with certain LDAP layouts

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-5
- Rebuilt for glibc bug#747377

* Sun Oct 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-4
- Change selinux policy requirement to Conflicts: with the old version,
  rather than Requires: the supported version.

* Fri Oct 21 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-3
- Add explicit requirement on selinux-policy version to address new SBUS
  symlinks.

* Wed Oct 19 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-2
- Remove %%files reference to sss_debuglevel copied from wrong upstreeam
  spec file.

* Tue Oct 18 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.2-1
- Improved handling of users and groups with multi-valued name attributes
  (aliases)
- Performance enhancements
    Initgroups on RFC2307bis/FreeIPA
    HBAC rule processing
- Improved process-hang detection and restarting
- Enabled the midpoint cache refresh by default (fewer cache misses on
  commonly-used entries)
- Cleaned up the example configuration
- New tool to change debug level on the fly

* Mon Aug 29 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.1-1
- New upstream release 1.6.1
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.6.1
- Fixes a serious issue with LDAP connections when the communication is
  dropped (e.g. VPN disconnection, waking from sleep)
- SSSD is now less strict when dealing with users/groups with multiple names
  when a definitive primary name cannot be determined
- The LDAP provider will no longer attempt to canonicalize by default when
  using SASL. An option to re-enable this has been provided.
- Fixes for non-standard LDAP attribute names (e.g. those used by Active
  Directory)
- Three HBAC regressions have been fixed.
- Fix for an infinite loop in the deref code

* Wed Aug 03 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.0-2
- Build with _hardened_build macro

* Wed Aug 03 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.6.0-1
- New upstream release 1.6.0
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.6.0
- Add host access control support for LDAP (similar to pam_host_attr)
- Finer-grained control on principals used with Kerberos (such as for FAST or
- validation)
- Added a new tool sss_cache to allow selective expiring of cached entries
- Added support for LDAP DEREF and ASQ controls
- Added access control features for Novell Directory Server
- FreeIPA dynamic DNS update now checks first to see if an update is needed
- Complete rewrite of the HBAC library
- New libraries: libipa_hbac and libipa_hbac-python

* Tue Jul 05 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.11-2
- New upstream release 1.5.11
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.11
- Fix a serious regression that prevented SSSD from working with ldaps:// URIs
- IPA Provider: Fix a bug with dynamic DNS that resulted in the wrong IPv6
- address being saved to the AAAA record

* Fri Jul 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.10-1
- New upstream release 1.5.10
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.10
- Fixed a regression introduced in 1.5.9 that could result in blocking calls
- to LDAP

* Thu Jun 30 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.9-1
- New upstream release 1.5.9
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.9
- Support for overriding home directory, shell and primary GID locally
- Properly honor TTL values from SRV record lookups
- Support non-POSIX groups in nested group chains (for RFC2307bis LDAP
- servers)
- Properly escape IPv6 addresses in the failover code
- Do not crash if inotify fails (e.g. resource exhaustion)
- Don't add multiple TGT renewal callbacks (too many log messages)

* Fri May 27 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.8-1
- New upstream release 1.5.8
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.8
- Support for the LDAP paging control
- Support for multiple DNS servers for name resolution
- Fixes for several group membership bugs
- Fixes for rare crash bugs

* Mon May 23 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.7-3
- Resolves: rhbz#706740 - Orphaned links on rc0.d-rc6.d
- Make sure to properly convert to systemd if upgrading from newer
- updates for Fedora 14

* Mon May 02 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.7-2
- Fix segfault in TGT renewal

* Fri Apr 29 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.7-1
- Resolves: rhbz#700891 - CVE-2011-1758 sssd: automatic TGT renewal overwrites
-                         cached password with predicatable filename

* Wed Apr 20 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.6.1-1
- Re-add manpage translations

* Wed Apr 20 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.6-1
- New upstream release 1.5.6
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.6
- Fixed a serious memory leak in the memberOf plugin
- Fixed a regression with the negative cache that caused it to be essentially
- nonfunctional
- Fixed an issue where the user's full name would sometimes be removed from
- the cache
- Fixed an issue with password changes in the kerberos provider not working
- with kpasswd

* Wed Apr 20 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-5
- Resolves: rhbz#697057 - kpasswd fails when using sssd and
-                         kadmin server != kdc server
- Upgrades from SysV should now maintain enabled/disabled status

* Mon Apr 18 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-4
- Fix %%postun

* Thu Apr 14 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-3
- Fix systemd conversion. Upgrades from SysV to systemd weren't properly
- enabling the systemd service.
- Fix a serious memory leak in the memberOf plugin
- Fix an issue where the user's full name would sometimes be removed
- from the cache

* Tue Apr 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-2
- Install systemd unit file instead of sysv init script

* Tue Apr 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.5-1
- New upstream release 1.5.5
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.5
- Fixes for several crash bugs
- LDAP group lookups will no longer abort if there is a zero-length member
- attribute
- Add automatic fallback to 'cn' if the 'gecos' attribute does not exist

* Thu Mar 24 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.4-1
- New upstream release 1.5.4
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.4
- Fixes for Active Directory when not all users and groups have POSIX attributes
- Fixes for handling users and groups that have name aliases (aliases are ignored)
- Fix group memberships after initgroups in the IPA provider

* Thu Mar 17 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.3-2
- Resolves: rhbz#683267 - sssd 1.5.1-9 breaks AD authentication

* Fri Mar 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.3-1
- New upstream release 1.5.3
- Support for libldb >= 1.0.0

* Thu Mar 10 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.2-1
- New upstream release 1.5.2
- https://fedorahosted.org/sssd/wiki/Releases/Notes-1.5.2
- Fixes for support of FreeIPA v2
- Fixes for failover if DNS entries change
- Improved sss_obfuscate tool with better interactive mode
- Fix several crash bugs
- Don't attempt to use START_TLS over SSL. Some LDAP servers can't handle this
- Delete users from the local cache if initgroups calls return 'no such user'
- (previously only worked for getpwnam/getpwuid)
- Use new Transifex.net translations
- Better support for automatic TGT renewal (now survives restart)
- Netgroup fixes

* Sun Feb 27 2011 Simo Sorce <ssorce@redhat.com> - 1.5.1-9
- Rebuild sssd against libldb 1.0.2 so the memberof module loads again.
- Related: rhbz#677425

* Mon Feb 21 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-8
- Resolves: rhbz#677768 - name service caches names, so id command shows
-                         recently deleted users

* Fri Feb 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-7
- Ensure that SSSD builds against libldb-1.0.0 on F15 and later
- Remove .la for memberOf

* Fri Feb 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-6
- Fix memberOf install path

* Fri Feb 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-5
- Add support for libldb 1.0.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 01 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-3
- Fix nested group member filter sanitization for RFC2307bis
- Put translated tool manpages into the sssd-tools subpackage

* Thu Jan 27 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-2
- Restore Requires: cyrus-sasl-gssapi as it is not auto-detected during
- rpmbuild

* Thu Jan 27 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.1-1
- New upstream release 1.5.1
- Addresses CVE-2010-4341 - DoS in sssd PAM responder can prevent logins
- Vast performance improvements when enumerate = true
- All PAM actions will now perform a forced initgroups lookup instead of just
- a user information lookup
-   This guarantees that all group information is available to other
-   providers, such as the simple provider.
- For backwards-compatibility, DNS lookups will also fall back to trying the
- SSSD domain name as a DNS discovery domain.
- Support for more password expiration policies in LDAP
-    389 Directory Server
-    FreeIPA
-    ActiveDirectory
- Support for ldap_tls_{cert,key,cipher_suite} config options
-Assorted bugfixes

* Tue Jan 11 2011 Stephen Gallagher <sgallagh@redhat.com> - 1.5.0-2
- CVE-2010-4341 - DoS in sssd PAM responder can prevent logins

* Wed Dec 22 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.5.0-1
- New upstream release 1.5.0
- Fixed issues with LDAP search filters that needed to be escaped
- Add Kerberos FAST support on platforms that support it
- Reduced verbosity of PAM_TEXT_INFO messages for cached credentials
- Added a Kerberos access provider to honor .k5login
- Addressed several thread-safety issues in the sss_client code
- Improved support for delayed online Kerberos auth
- Significantly reduced time between connecting to the network/VPN and
- acquiring a TGT
- Added feature for automatic Kerberos ticket renewal
- Provides the kerberos ticket for long-lived processes or cron jobs
- even when the user logs out
- Added several new features to the LDAP access provider
- Support for 'shadow' access control
- Support for authorizedService access control
- Ability to mix-and-match LDAP access control features
- Added an option for a separate password-change LDAP server for those
- platforms where LDAP referrals are not supported
- Added support for manpage translations


* Thu Nov 18 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.1-3
- Solve a shutdown race-condition that sometimes left processes running
- Resolves: rhbz#606887 - SSSD stops on upgrade

* Tue Nov 16 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.1-2
- Log startup errors to the syslog
- Allow cache cleanup to be disabled in sssd.conf

* Mon Nov 01 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.1-1
- New upstream release 1.4.1
- Add support for netgroups to the proxy provider
- Fixes a minor bug with UIDs/GIDs >= 2^31
- Fixes a segfault in the kerberos provider
- Fixes a segfault in the NSS responder if a data provider crashes
- Correctly use sdap_netgroup_search_base

* Mon Oct 18 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.0-2
- Fix incorrect tarball URL

* Mon Oct 18 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.4.0-1
- New upstream release 1.4.0
- Added support for netgroups to the LDAP provider
- Performance improvements made to group processing of RFC2307 LDAP servers
- Fixed nested group issues with RFC2307bis LDAP servers without a memberOf plugin
- Build-system improvements to support Gentoo
- Split out several libraries into the ding-libs tarball
- Manpage reviewed and updated

* Mon Oct 04 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-35
- Fix pre and post script requirements

* Mon Oct 04 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-34
- Resolves: rhbz#606887 - sssd stops on upgrade

* Fri Oct 01 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-33
- Resolves: rhbz#626205 - Unable to unlock screen

* Tue Sep 28 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-32
- Resolves: rhbz#637955 - libini_config-devel needs libcollection-devel but
-                         doesn't require it

* Thu Sep 16 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-31
- Resolves: rhbz#632615 - the krb5 locator plugin isn't packaged for multilib

* Tue Aug 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.3.0-30
- Resolves: CVE-2010-2940 - sssd allows null password entry to authenticate
-                           against LDAP

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.91-21
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 09 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.2.91-20
- New upstream version 1.2.91 (1.3.0rc1)
- Improved LDAP failover
- Synchronous sysdb API (provides performance enhancements)
- Better online reconnection detection

* Mon Jun 21 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.2.1-15
- New stable upstream version 1.2.1
- Resolves: rhbz#595529 - spec file should eschew %%define in favor of
-                         %%global
- Resolves: rhbz#593644 - Empty list of simple_allow_users causes sssd service
-                         to fail while restart.
- Resolves: rhbz#599026 - Makefile typo causes SSSD not to use the kernel
-                         keyring
- Resolves: rhbz#599724 - sssd is broken on Rawhide

* Mon May 24 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.2.0-12
- New stable upstream version 1.2.0
- Support ServiceGroups for FreeIPA v2 HBAC rules
- Fix long-standing issue with auth_provider = proxy
- Better logging for TLS issues in LDAP

* Tue May 18 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.92-11
- New LDAP access provider allows for filtering user access by LDAP attribute
- Reduced default timeout for detecting offline status with LDAP
- GSSAPI ticket lifetime made configurable
- Better offline->online transition support in Kerberos

* Fri May 07 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.91-10
- Release new upstream version 1.1.91
- Enhancements when using SSSD with FreeIPA v2
- Support for deferred kinit
- Support for DNS SRV records for failover

* Fri Apr 02 2010 Simo Sorce <ssorce@redhat.com> - 1.1.1-3
- Bump up release number to avoid library sub-packages version issues with
  previous releases.

* Thu Apr 01 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.1-1
- New upstream release 1.1.1
- Fixed the IPA provider (which was segfaulting at start)
- Fixed a bug in the SSSDConfig API causing some options to revert to
- their defaults
- This impacted the Authconfig UI
- Ensure that SASL binds to LDAP auto-retry when interrupted by a signal

* Tue Mar 23 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.0-2
- Release SSSD 1.1.0 final
- Fix two potential segfaults
- Fix memory leak in monitor
- Better error message for unusable confdb

* Wed Mar 17 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.1.0-1.pre20100317git0ea7f19
- Release candidate for SSSD 1.1
- Add simple access provider
- Create subpackages for libcollection, libini_config, libdhash and librefarray
- Support IPv6
- Support LDAP referrals
- Fix cache issues
- Better feedback from PAM when offline

* Wed Feb 24 2010 Stephen Gallagehr <sgallagh@redhat.com> - 1.0.5-2
- Rebuild against new libtevent

* Fri Feb 19 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.5-1
- Fix licenses in sources and on RPMs

* Mon Jan 25 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.4-1
- Fix regression on 64-bit platforms

* Fri Jan 22 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.3-1
- Fixes link error on platforms that do not do implicit linking
- Fixes double-free segfault in PAM
- Fixes double-free error in async resolver
- Fixes support for TCP-based DNS lookups in async resolver
- Fixes memory alignment issues on ARM processors
- Manpage fixes

* Thu Jan 14 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.2-1
- Fixes a bug in the failover code that prevented the SSSD from detecting when it went back online
- Fixes a bug causing long (sometimes multiple-minute) waits for NSS requests
- Several segfault bugfixes

* Mon Jan 11 2010 Stephen Gallagher <sgallagh@redhat.com> - 1.0.1-1
- Fix CVE-2010-0014

* Mon Dec 21 2009 Stephen Gallagher <sgallagh@redhat.com> - 1.0.0-2
- Patch SSSDConfig API to address
- https://bugzilla.redhat.com/show_bug.cgi?id=549482

* Fri Dec 18 2009 Stephen Gallagher <sgallagh@redhat.com> - 1.0.0-1
- New upstream stable release 1.0.0

* Fri Dec 11 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.99.1-1
- New upstream bugfix release 0.99.1

* Mon Nov 30 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.99.0-1
- New upstream release 0.99.0

* Tue Oct 27 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.7.1-1
- Fix segfault in sssd_pam when cache_credentials was enabled
- Update the sample configuration
- Fix upgrade issues caused by data provider service removal

* Mon Oct 26 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.7.0-2
- Fix upgrade issues from old (pre-0.5.0) releases of SSSD

* Fri Oct 23 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.7.0-1
- New upstream release 0.7.0

* Thu Oct 15 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.6.1-2
- Fix missing file permissions for sssd-clients

* Tue Oct 13 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.6.1-1
- Add SSSDConfig API
- Update polish translation for 0.6.0
- Fix long timeout on ldap operation
- Make dp requests more robust

* Tue Sep 29 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.6.0-1
- Ensure that the configuration upgrade script always writes the config
  file with 0600 permissions
- Eliminate an infinite loop in group enumerations

* Mon Sep 28 2009 Sumit Bose <sbose@redhat.com> - 0.6.0-0
- New upstream release 0.6.0

* Mon Aug 24 2009 Simo Sorce <ssorce@redhat.com> - 0.5.0-0
- New upstream release 0.5.0

* Wed Jul 29 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.4.1-4
- Fix for CVE-2009-2410 - Native SSSD users with no password set could log in
  without a password. (Patch by Stephen Gallagher)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Simo Sorce <ssorce@redhat.com> - 0.4.1-2
- Fix a couple of segfaults that may happen on reload

* Thu Jun 11 2009 Simo Sorce <ssorce@redhat.com> - 0.4.1-1
- add missing configure check that broke stopping the daemon
- also fix default config to add a missing required option

* Mon Jun  8 2009 Simo Sorce <ssorce@redhat.com> - 0.4.1-0
- latest upstream release.
- also add a patch that fixes debugging output (potential segfault)

* Mon Apr 20 2009 Simo Sorce <ssorce@redhat.com> - 0.3.2-2
- release out of the official 0.3.2 tarball

* Mon Apr 20 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.3.2-1
- bugfix release 0.3.2
- includes previous release patches
- change permissions of the /etc/sssd/sssd.conf to 0600

* Tue Apr 14 2009 Simo Sorce <ssorce@redhat.com> - 0.3.1-2
- Add last minute bug fixes, found in testing the package

* Mon Apr 13 2009 Simo Sorce <ssorce@redhat.com> - 0.3.1-1
- Version 0.3.1
- includes previous release patches

* Mon Apr 13 2009 Simo Sorce <ssorce@redhat.com> - 0.3.0-2
- Try to fix build adding automake as an explicit BuildRequire
- Add also a couple of last minute patches from upstream

* Mon Apr 13 2009 Simo Sorce <ssorce@redhat.com> - 0.3.0-1
- Version 0.3.0
- Provides file based configuration and lots of improvements

* Tue Mar 10 2009 Simo Sorce <ssorce@redhat.com> - 0.2.1-1
- Version 0.2.1

* Tue Mar 10 2009 Simo Sorce <ssorce@redhat.com> - 0.2.0-1
- Version 0.2.0

* Sun Mar 08 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.1.0-5.20090309git691c9b3
- package git snapshot

* Fri Mar 06 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.1.0-4
- fixed items found during review
- added initscript

* Thu Mar 05 2009 Sumit Bose <sbose@redhat.com> - 0.1.0-3
- added sss_client

* Mon Feb 23 2009 Jakub Hrozek <jhrozek@redhat.com> - 0.1.0-2
- Small cleanup and fixes in the spec file

* Thu Feb 12 2009 Stephen Gallagher <sgallagh@redhat.com> - 0.1.0-1
- Initial release (based on version 0.1.0 upstream code)
