# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1

%global systemctl_bin /usr/bin/systemctl
%global check_password_version 1.1

%global so_ver 2
%global so_ver_compat 2

# Build openldap-servers package and its libslapi in openldap-devel and openldap-compat
%bcond servers 1

# When you change "Version: " to the new major version, remember to change this value too
%global major_version 2.6

# Disable automatic .la file removal
%global __brp_remove_la_files %nil

Name: openldap
Version: 2.6.10
Release: 4%{?dist}
Summary: LDAP support libraries
License: OLDAP-2.8
URL: http://www.openldap.org/

Source0: https://openldap.org/software/download/OpenLDAP/openldap-release/openldap-%{version}.tgz
Source1: slapd.service
Source2: slapd.tmpfiles
Source3: slapd.ldif
Source4: ldap.conf
Source6: openldap.sysusers
Source10: https://github.com/ltb-project/openldap-ppolicy-check-password/archive/v%{check_password_version}/openldap-ppolicy-check-password-%{check_password_version}.tar.gz
Source50: libexec-functions
Source52: libexec-check-config.sh

# Patches for 2.6
Patch0: openldap-manpages.patch
Patch1: openldap-reentrant-gethostby.patch

Patch3: openldap-smbk5pwd-overlay.patch
Patch4: openldap-ai-addrconfig.patch
Patch5: openldap-allop-overlay.patch

# fix back_perl problems with lt_dlopen()
# might cause crashes because of symbol collisions
# the proper fix is to link all perl modules against libperl
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=327585
Patch6: openldap-switch-to-lt_dlopenadvise-to-get-RTLD_GLOBAL-set.patch

# System-wide default for CA certs
Patch7: openldap-openssl-manpage-defaultCA.patch
Patch8: openldap-add-export-symbols-LDAP_CONNECTIONLESS.patch
Patch9: openldap-libldap-avoid-SSL-context-cleanup-during-library-des.patch
Patch10: openldap-ITS-10297-Defer-hostname-resolution-til-first-use.patch

# check-password module specific patches
Patch90: check-password-makefile.patch
Patch91: check-password.patch

BuildRequires: cyrus-sasl-devel
BuildRequires: gcc
BuildRequires: glibc-devel
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libtool-ltdl-devel
BuildRequires: libevent-devel
BuildRequires: libxcrypt-devel
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: perl(ExtUtils::Embed)
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: unixODBC-devel
BuildRequires: cracklib-devel
BuildRequires: systemd
BuildRequires: systemd-rpm-macros

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%package devel
Summary: LDAP development libraries and header files
Requires: openldap%{?_isa} = %{version}-%{release}
Requires: cyrus-sasl-devel%{?_isa}

%description devel
The openldap-devel package includes the development libraries and
header files needed for compiling applications that use LDAP
(Lightweight Directory Access Protocol) internals. LDAP is a set of
protocols for enabling directory services over the Internet. Install
this package only if you plan to develop or will need to compile
customized LDAP clients.

%package compat
Summary: Package providing legacy non-threaded libldap
Requires: openldap%{?_isa} = %{version}-%{release}
# since libldap is manually linked from libldap_r, the provides is not generated automatically
%ifarch armv7hl i686
Provides: libldap-2.4.so.%{so_ver_compat}
Provides: libldap_r-2.4.so.%{so_ver_compat}
Provides: liblber-2.4.so.%{so_ver_compat}
%if %{with servers}
Provides: libslapi-2.4.so.%{so_ver_compat}
%endif
%else
Provides: libldap-2.4.so.%{so_ver_compat}()(%{__isa_bits}bit)
Provides: libldap_r-2.4.so.%{so_ver_compat}()(%{__isa_bits}bit)
Provides: liblber-2.4.so.%{so_ver_compat}()(%{__isa_bits}bit)
%if %{with servers}
Provides: libslapi-2.4.so.%{so_ver_compat}()(%{__isa_bits}bit)
%endif
%endif

%description compat
The openldap-compat package contains shared libraries named as libldap-2.4.so,
%if %{with servers}
libldap_r-2.4.so, liblber-2.4.so and libslapi-2.4.so.
%else
libldap_r-2.4.so and liblber-2.4.so
%endif
The libraries are just links to the current version shared libraries,
and are available for compatibility reasons.

%if %{with servers}
%package servers
Summary: LDAP server
Requires: openldap%{?_isa} = %{version}-%{release}
%{?systemd_requires}
# migrationtools (slapadd functionality):
Provides: ldif2ldbm

%description servers
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. This package contains the slapd server and related files.
# endif servers
%endif

%package clients
Summary: LDAP client utilities
Requires: openldap%{?_isa} = %{version}-%{release}

%description clients
OpenLDAP is an open-source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap-clients package contains the client
programs needed for accessing and modifying OpenLDAP directories.

%prep
%setup -q -c -a 0 -a 10

pushd openldap-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1

# build smbk5pwd with other overlays
ln -s ../../../contrib/slapd-modules/smbk5pwd/smbk5pwd.c servers/slapd/overlays
mv contrib/slapd-modules/smbk5pwd/README contrib/slapd-modules/smbk5pwd/README.smbk5pwd
# build allop with other overlays
ln -s ../../../contrib/slapd-modules/allop/allop.c servers/slapd/overlays
mv contrib/slapd-modules/allop/README contrib/slapd-modules/allop/README.allop
mv contrib/slapd-modules/allop/slapo-allop.5 doc/man/man5/slapo-allop.5

mv servers/slapd/back-perl/README{,.back_perl}

# fix documentation encoding
for filename in doc/drafts/draft-ietf-ldapext-acl-model-xx.txt; do
  iconv -f iso-8859-1 -t utf-8 "$filename" > "$filename.utf8"
  mv "$filename.utf8" "$filename"
done

popd

pushd openldap-ppolicy-check-password-%{check_password_version}
%patch -P90 -p1
%patch -P91 -p1
popd

%build

%set_build_flags
# enable experimental support for LDAP over UDP (LDAP_CONNECTIONLESS)
export CFLAGS="${CFLAGS} ${LDFLAGS} -Wl,--as-needed -Wl,-z,now -DLDAP_CONNECTIONLESS"
# disable legacy hash algorithm
export CFLAGS="${CFLAGS} -DOPENSSL_NO_MD2"

pushd openldap-%{version}
%configure \
	--enable-debug \
	--enable-dynamic \
	--enable-versioning \
	\
	--enable-dynacl \
	--enable-cleartext \
	--enable-crypt \
	--enable-lmpasswd \
	--enable-spasswd \
	--enable-modules \
	--enable-perl \
	--enable-rewrite \
	--enable-rlookups \
%if %{with servers}
	--enable-slapi \
%endif
	--disable-slp \
	\
	--enable-backends=mod \
	--enable-bdb=yes \
	--enable-hdb=yes \
	--enable-mdb=yes \
	--enable-monitor=yes \
	--disable-ndb \
	--disable-sql \
	--disable-wt \
	\
	--enable-overlays=mod \
	\
	--disable-static \
	\
	--enable-balancer=mod \
        \
	--with-cyrus-sasl \
	--without-fetch \
	--with-threads \
	--with-pic \
	--with-gnu-ld \
	\
	--libexecdir=%{_libdir}

%make_build
popd

pushd openldap-ppolicy-check-password-%{check_password_version}
%make_build LDAP_INC="-I../openldap-%{version}/include \
 -I../openldap-%{version}/servers/slapd \
 -I../openldap-%{version}/build-servers/include"
popd

%install

mkdir -p %{buildroot}%{_libdir}/
%if %{with servers}
install -p -D -m 0644 %{SOURCE6} %{buildroot}%{_sysusersdir}/openldap.conf
%endif

pushd openldap-%{version}
%make_install STRIP_OPTS=""
popd

# install check_password module
pushd openldap-ppolicy-check-password-%{check_password_version}
mv check_password.so check_password.so.%{check_password_version}
ln -s check_password.so.%{check_password_version} %{buildroot}%{_libdir}/openldap/check_password.so
install -m 755 check_password.so.%{check_password_version} %{buildroot}%{_libdir}/openldap/
# install -m 644 README %{buildroot}%{_libdir}/openldap
install -d -m 755 %{buildroot}%{_sysconfdir}/openldap
cat > %{buildroot}%{_sysconfdir}/openldap/check_password.conf <<EOF
# OpenLDAP pwdChecker library configuration

#useCracklib 1
#minPoints 3
#minUpper 0
#minLower 0
#minDigit 0
#minPunct 0
EOF
mv README{,.check_pwd}
popd

# setup directories for TLS certificates
mkdir -p %{buildroot}%{_sysconfdir}/openldap/certs

# setup data and runtime directories
mkdir -p %{buildroot}%{_sharedstatedir}
mkdir -p %{buildroot}%{_localstatedir}
install -m 0700 -d %{buildroot}%{_sharedstatedir}/ldap
install -m 0755 -d %{buildroot}%{_localstatedir}/run/openldap

# setup autocreation of runtime directories on tmpfs
mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE2 %{buildroot}%{_tmpfilesdir}/slapd.conf

# install default ldap.conf (customized)
rm %{buildroot}%{_sysconfdir}/openldap/ldap.conf
install -m 0644 %SOURCE4 %{buildroot}%{_sysconfdir}/openldap/ldap.conf

# setup maintainance scripts
mkdir -p %{buildroot}%{_libexecdir}
install -m 0755 -d %{buildroot}%{_libexecdir}/openldap
install -m 0644 %SOURCE50 %{buildroot}%{_libexecdir}/openldap/functions
install -m 0755 %SOURCE52 %{buildroot}%{_libexecdir}/openldap/check-config.sh

# remove build root from config files and manual pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_sysconfdir}/openldap/*.conf
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

# we don't need the default files -- RPM handles changes
rm %{buildroot}%{_sysconfdir}/openldap/*.default

# install an init script for the servers
mkdir -p %{buildroot}%{_unitdir}
install -m 0644 %SOURCE1 %{buildroot}%{_unitdir}/slapd.service

# move slapd out of _libdir
mv %{buildroot}%{_libdir}/slapd %{buildroot}%{_sbindir}/

# setup tools as symlinks to slapd
for X in acl add auth cat dn index modify passwd test schema ; do
  rm %{buildroot}%{_sbindir}/slap$X
  ln -s slapd %{buildroot}%{_sbindir}/slap$X
done

# re-symlink unversioned libraries, so ldconfig is not confused
pushd %{buildroot}%{_libdir}
v=%{version}
version=$(echo ${v%.[0-9]*})
for lib in liblber libldap %{?with_servers:libslapi}; do
        rm -f ${lib}.so
        ln -s ${lib}.so.%{so_ver} ${lib}.so
done

for lib in $(ls | grep libldap); do
    IFS='.'
    read -r -a libsplit <<< "$lib"
    if [[ -z "${libsplit[3]}" && -n "${libsplit[2]}" ]]
    then
        so_ver_short_2_4="%{so_ver_compat}"
    elif [ -n "${libsplit[3]}" ]
    then
        so_ver_full_2_4="%{so_ver_compat}.${libsplit[3]}.${libsplit[4]}"
    fi
    unset IFS
done

# Provide only libldap and copy it to libldap_r for both 2.4 and 2.6+ versions, make a versioned lib link
# We increase it by 2 because libldap-2.4 has the 'so.2' major version on 2.4.59 (one of the last versions which is EOL)
gcc -shared -o "%{buildroot}%{_libdir}/libldap-2.4.so.${so_ver_short_2_4}" -Wl,--no-as-needed \
       -Wl,-soname -Wl,libldap-2.4.so.${so_ver_short_2_4} -L "%{buildroot}%{_libdir}" -Wl,-z,now -lldap
gcc -shared -o "%{buildroot}%{_libdir}/libldap_r-2.4.so.${so_ver_short_2_4}" -Wl,--no-as-needed \
       -Wl,-soname -Wl,libldap_r-2.4.so.${so_ver_short_2_4} -L "%{buildroot}%{_libdir}" -Wl,-z,now -lldap
gcc -shared -o "%{buildroot}%{_libdir}/liblber-2.4.so.${so_ver_short_2_4}" -Wl,--no-as-needed \
       -Wl,-soname -Wl,liblber-2.4.so.${so_ver_short_2_4} -L "%{buildroot}%{_libdir}" -Wl,-z,now -llber
%if %{with servers}
gcc -shared -o "%{buildroot}%{_libdir}/libslapi-2.4.so.${so_ver_short_2_4}" -Wl,--no-as-needed \
       -Wl,-soname -Wl,libslapi-2.4.so.${so_ver_short_2_4} -L "%{buildroot}%{_libdir}" -Wl,-z,now -lslapi
ln -s libslapi-2.4.so.{${so_ver_short_2_4},${so_ver_full_2_4}}
%endif
ln -s libldap-2.4.so.{${so_ver_short_2_4},${so_ver_full_2_4}}
ln -s libldap_r-2.4.so.{${so_ver_short_2_4},${so_ver_full_2_4}}
ln -s liblber-2.4.so.{${so_ver_short_2_4},${so_ver_full_2_4}}

popd

# tweak permissions on the libraries to make sure they're correct
chmod 0755 %{buildroot}%{_libdir}/lib*.so*
chmod 0644 %{buildroot}%{_libdir}/lib*.*a
chmod 0644 %{buildroot}%{_libdir}/openldap/*.la

# slapd.conf(5) is obsoleted since 2.3, see slapd-config(5)
mkdir -p %{buildroot}%{_datadir}
install -m 0755 -d %{buildroot}%{_datadir}/openldap-servers
install -m 0644 %SOURCE3 %{buildroot}%{_datadir}/openldap-servers/slapd.ldif
install -m 0700 -d %{buildroot}%{_sysconfdir}/openldap/slapd.d
rm %{buildroot}%{_sysconfdir}/openldap/slapd.conf
rm %{buildroot}%{_sysconfdir}/openldap/slapd.ldif

# move doc files out of _sysconfdir
mv %{buildroot}%{_sysconfdir}/openldap/schema/README README.schema

# remove files which we don't want packaged
rm %{buildroot}%{_libdir}/*.la  # because we do not want files in %{_libdir}/openldap/ removed, yet

%ldconfig_scriptlets

%if %{with servers}

%post servers
%systemd_post slapd.service

# generate configuration if necessary
if [[ ! -f %{_sysconfdir}/openldap/slapd.d/cn=config.ldif && \
      ! -f %{_sysconfdir}/openldap/slapd.conf
   ]]; then
      # if there is no configuration available, generate one from the defaults
      mkdir -p %{_sysconfdir}/openldap/slapd.d/ &>/dev/null || :
      /usr/sbin/slapadd -F %{_sysconfdir}/openldap/slapd.d/ -n0 -l %{_datadir}/openldap-servers/slapd.ldif
      chown -R ldap:ldap %{_sysconfdir}/openldap/slapd.d/
      %{systemctl_bin} try-restart slapd.service &>/dev/null
fi

# restart after upgrade
if [ $1 -ge 1 ]; then
    %{systemctl_bin} condrestart slapd.service &>/dev/null || :
fi

exit 0

%preun servers
%systemd_preun slapd.service

%postun servers
%systemd_postun_with_restart slapd.service
%endif
# endif servers

%files
%doc openldap-%{version}/ANNOUNCEMENT
%doc openldap-%{version}/CHANGES
%license openldap-%{version}/COPYRIGHT
%license openldap-%{version}/LICENSE
%doc openldap-%{version}/README
%dir %{_sysconfdir}/openldap
%dir %{_sysconfdir}/openldap/certs
%config(noreplace) %{_sysconfdir}/openldap/ldap.conf
%dir %{_libexecdir}/openldap/
%{_libdir}/liblber.so.*
%{_libdir}/libldap.so.*
%if %{with servers}
%{_libdir}/libslapi.so.*
%endif
%{_mandir}/man5/ldif.5*
%{_mandir}/man5/ldap.conf.5*

%if %{with servers}
%files servers
%doc openldap-%{version}/contrib/slapd-modules/smbk5pwd/README.smbk5pwd
%doc openldap-%{version}/doc/guide/admin/*.html
%doc openldap-%{version}/doc/guide/admin/*.png
%doc openldap-%{version}/servers/slapd/back-perl/SampleLDAP.pm
%doc openldap-%{version}/servers/slapd/back-perl/README.back_perl
%doc openldap-ppolicy-check-password-%{check_password_version}/README.check_pwd
%doc README.schema
%config(noreplace) %dir %attr(0750,ldap,ldap) %{_sysconfdir}/openldap/slapd.d
%config(noreplace) %{_sysconfdir}/openldap/schema
%config(noreplace) %{_sysconfdir}/openldap/check_password.conf
%{_tmpfilesdir}/slapd.conf
%dir %attr(0700,ldap,ldap) %{_sharedstatedir}/ldap
%dir %attr(-,ldap,ldap) %{_localstatedir}/run/openldap
%{_unitdir}/slapd.service
%{_datadir}/openldap-servers/
%{_libdir}/openldap/accesslog*
%{_libdir}/openldap/allop*
%{_libdir}/openldap/auditlog*
%{_libdir}/openldap/autoca*
%{_libdir}/openldap/back_asyncmeta*
%{_libdir}/openldap/back_dnssrv*
%{_libdir}/openldap/back_ldap*
%{_libdir}/openldap/back_meta*
%{_libdir}/openldap/back_null*
%{_libdir}/openldap/back_passwd*
%{_libdir}/openldap/back_relay*
%{_libdir}/openldap/back_sock*
%{_libdir}/openldap/check_password*
%{_libdir}/openldap/collect*
%{_libdir}/openldap/constraint*
%{_libdir}/openldap/dds*
%{_libdir}/openldap/deref*
%{_libdir}/openldap/dyngroup*
%{_libdir}/openldap/dynlist*
%{_libdir}/openldap/home*
%{_libdir}/openldap/lloadd*
%{_libdir}/openldap/memberof*
%{_libdir}/openldap/nestgroup*
%{_libdir}/openldap/otp*
%{_libdir}/openldap/pcache*
%{_libdir}/openldap/ppolicy*
%{_libdir}/openldap/refint*
%{_libdir}/openldap/remoteauth*
%{_libdir}/openldap/retcode*
%{_libdir}/openldap/rwm*
%{_libdir}/openldap/seqmod*
%{_libdir}/openldap/smbk5pwd*
%{_libdir}/openldap/sssvlv*
%{_libdir}/openldap/syncprov*
%{_libdir}/openldap/translucent*
%{_libdir}/openldap/unique*
%{_libdir}/openldap/valsort*
%{_libexecdir}/openldap/functions
%{_libexecdir}/openldap/check-config.sh
%{_sbindir}/slap*
%{_mandir}/man5/lloadd.conf.5*
%{_mandir}/man8/lloadd.8*
%{_mandir}/man5/slapd*.5*
%{_mandir}/man5/slapo-*.5*
%{_mandir}/man5/slappw-argon2.5*
%{_mandir}/man8/slap*.8*
%{_sysusersdir}/openldap.conf
# obsolete configuration
%ghost %config(noreplace,missingok) %attr(0640,ldap,ldap) %{_sysconfdir}/openldap/slapd.conf
%else
%exclude %{_datadir}/openldap-servers/
%exclude %{_libdir}/openldap/
%exclude %{_libexecdir}/openldap/check-config.sh
%exclude %{_libexecdir}/openldap/functions
%exclude %{_mandir}/man5/slapd*.5*
%exclude %{_mandir}/man5/slapo-*.5*
%exclude %{_mandir}/man5/lloadd.conf.5*
%exclude %{_mandir}/man5/slappw-argon2.5*
%exclude %{_mandir}/man8/*
%exclude %{_sbindir}/slap*
%exclude %{_sysconfdir}/openldap/check_password.conf
%exclude %{_sysconfdir}/openldap/schema
%exclude %{_tmpfilesdir}/slapd.conf
%exclude %{_unitdir}/slapd.service
%endif
# endif servers


%files clients
%{_bindir}/ldap*
%{_mandir}/man1/ldap*.1*

%files devel
%doc openldap-%{version}/doc/drafts openldap-%{version}/doc/rfc
%{_libdir}/liblber.so
%{_libdir}/libldap.so
%if %{with servers}
%{_libdir}/libslapi.so
%endif
%{_includedir}/*
%{_libdir}/pkgconfig/lber.pc
%{_libdir}/pkgconfig/ldap.pc
%{_mandir}/man3/*

%files compat
%{_libdir}/libldap-2.4*.so.*
%{_libdir}/libldap_r-2.4*.so.*
%{_libdir}/liblber-2.4*.so.*
%if %{with servers}
%{_libdir}/libslapi-2.4*.so.*
%endif

%changelog
* Fri Aug 29 2025 Simon Pichugin <spichugi@redhat.com> - 2.6.10-4
- Fix LDAP initialization does unnecessary resolution of hostname (rhbz#2392068)
- Convert STI tests to FMF (rhbz#2392069)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.10-2
- Perl 5.42 rebuild

* Tue Jun 10 2025 Simon Pichugin <spichugi@redhat.com> - 2.6.10-1
- Rebase to version 2.6.10 (rhbz#2368103)

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.9-5
- Drop call to %sysusers_create_compat

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 2.6.9-4
- Add explicit BR: libxcrypt-devel

* Fri Jan 24 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.9-3
- Adjust file patterns for the sbin merge

* Thu Jan 16 2025 Simon Pichugin <spichugi@redhat.com> - 2.6.9-2
- Disable MD2 hash algorithm (rhbz#2338556)

* Thu Jan 9 2025 Simon Pichugin <spichugi@redhat.com> - 2.6.9-1
- Rebase to version 2.6.9 (rhbz#2329002)

* Tue Dec 3 2024 Simon Pichugin <spichugi@redhat.com> - 2.6.8-6
- Avoid SSL context cleanup during library destruction

* Tue Jul 23 2024 Simon Pichugin <spichugi@redhat.com> - 2.6.8-5
- Clean up spec file so it's aligned with c10s
- Remove UPGRADE_INSTRUCTIONS for openldap-server upgrade (rhbz#2133526)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.6.8-3
- Disable libslapi and servers in RHEL builds

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.8-2
- Perl 5.40 rebuild

* Wed May 22 2024 Simon Pichugin <spichugi@redhat.com> - 2.6.8-1
- Rebase to version 2.6.8 (rhbz#2282258)

* Fri Feb 9 2024 Simon Pichugin <spichugi@redhat.com> - 2.6.7-1
- Rebase to version 2.6.7 (rhbz#2261163)
- Use systemd-sysusers for ldap user and group (rhbz#2173965)
- Fix compiler errors (rhbz#2261427)
- Replace License with SPDX identifier

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jul 31 2023 Simon Pichugin <spichugi@redhat.com> - 2.6.6-1
- Rebase to version 2.6.6
  Related: rhbz#2227948

* Wed Jul 26 2023 Simon Pichugin <spichugi@redhat.com> - 2.6.5-1
- Rebase to version 2.6.5
  Related: rhbz#2221798

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.4-3
- Perl 5.38 rebuild

* Sat Apr 15 2023 Florian Weimer <fweimer@redhat.com> - 2.6.4-2
- Apply upstream patch to fix C99 compatibility issues

* Mon Feb 27 2023 Simon Pichugin <spichugi@redhat.com> - 2.6.4-1
- Rebase to version 2.6.4
  Related: rhbz#2168351

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 17 2022 Simon Pichugin <spichugi@redhat.com> - 2.6.3-1
- Rebase to version 2.6.3
  Related: rhbz#2107382

* Thu Aug 11 2022 Simon Pichugin <spichugi@redhat.com> - 2.6.2-5
- Add export symbols related to LDAP_CONNECTIONLESS
  Related: rhbz#2117825

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 27 2022 Simon Pichugin <spichugi@redhat.com> - 2.6.2-3
- Fix debuginfo missing issue (#2101615)

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 2.6.2-2
- Perl 5.36 rebuild

* Wed May 25 2022 Simon Pichugin <spichugi@redhat.com> - 2.6.2-1
- Rebase to version 2.6.2 (#2090447)

* Wed Feb 2 2022 Simon Pichugin <spichugi@redhat.com> - 2.6.1-2
- Fix twice packaged compat libraries issue (#2049085)

* Mon Jan 31 2022 Simon Pichugin <spichugi@redhat.com> - 2.6.1-1
- Update to new major release OpenLDAP 2.6.1 (#1955293)
  + rediff all patches and remove patches now upstream
  + use upstream source location for check password module
  + and rediff patch due to this
  + add patch to fix build issue in 2.5.4 (from upstream)
  + clean and sort buildreqs
  + remove various refs to bdb
  + remove now default -DLDAP_USE_NON_BLOCKING_TLS
  + add new modules and enable load balancer as module
  + disable wiredtired backend due to missing build deps
  + don't remove files that don't exist
  + let check-config work on *.mdb over legacy files
  + remove refs to old-style config
  + new soname names
  + remove libldap_r link as the library was merged with libldap
  + refactor openldap-compat package to support the transition from 2.4
  + add UPGRADE_INSTRUCTIONS for openldap-server upgrade
- The original patch was submitted by Fedora user - terjeros
  https://src.fedoraproject.org/rpms/openldap/pull-request/6

* Mon Jan 24 2022 Timm Bäder <tbaeder@redhat.com> - 2.4.59-6
- Disable automatic .la file removal
- https://fedoraproject.org/wiki/Changes/RemoveLaFiles

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.59-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 30 2021 Simon Pichugin <spichugi@redhat.com> - 2.4.59-4
- Backport TLS SNI feature from OpenLDAP 2.5 (#2009534)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.4.59-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul  7 2021 Simon Pichugin <spichugi@redhat.com> - 2.4.59-1
- Rebase to version 2.4.59 (#1980015)
- Update the spec file for upcoming autoconf-2.71 (#1943079)

* Tue Jun 15 2021 Simon Pichugin <spichugi@redhat.com> - 2.4.58-5
- Fix slapd.tmpfiles complaints (#1972147)
- Use https:// for source (#1972141)

* Thu Jun  3 2021 Simon Pichugin <spichugi@redhat.com> - 2.4.58-4
- Rebuild without MP_2 support (#1967136)
- Fix coverity issues

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.58-3
- Perl 5.34 rebuild

* Thu Apr  8 2021 Simon Pichugin <spichugi@redhat.com> - 2.4.58-2
- Backport Channel Binding support (#1822904, #1822737)

* Tue Mar 23 2021 Simon Pichugin <spichugi@redhat.com> - 2.4.58-1
- Rebase to version 2.4.58 (#1939663)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.57-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Simon Pichugin <spichugi@redhat.com> - 2.4.57-1
- Rebase to version 2.4.57 (#1917583)

* Thu Nov 26 2020 Simon Pichugin <spichugi@redhat.com> - 2.4.56-4
- Use gcc to link libldap_r to libldap (#1537260)

* Fri Nov 20 2020 Simon Pichugin <spichugi@redhat.com> - 2.4.56-3
- Fix 32-bit libraries build (#1537260)

* Fri Nov 20 2020 Simon Pichugin <spichugi@redhat.com> - 2.4.56-2
- Drop non-threaded libldap (#1537260)

* Wed Nov 18 2020 Simon Pichugin <spichugi@redhat.com> - 2.4.56-1
- Rebase to version 2.4.56 (#1896508)

* Mon Nov 02 2020 Simon Pichugin <spichugi@redhat.com> - 2.4.55-1
- Rebase to version 2.4.55 (#1891622)

* Tue Oct 13 2020 Simon Pichugin <spichugi@redhat.com> - 2.4.54-1
- Rebase to version 2.4.54 (#1887581)

* Thu Sep 10 2020 Simon Pichugin <spichugi@redhat.com> - 2.4.53-1
- Rebase to version 2.4.53 (#1868240)

* Thu Sep 03 2020 Simon Pichugin <spichugi@redhat.com> - 2.4.52-1
- Rebase to version 2.4.52 (#1868240)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.50-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.50-2
- Perl 5.32 rebuild

* Wed Jun 17 2020 Matus Honek <mhonek@redhat.com> - 2.4.50-1
- Rebase to version 2.4.50 (#1742285)

* Tue Jun 16 2020 Tom Stellard <tstellar@redhat.com> - 2.4.47-5
- Spec file cleanups
- Add BuildRequres: gcc [1]
- make_build [2] and make_install [3]
- [1] https://docs.fedoraproject.org/en-US/packaging-guidelines/C_and_C++/#_buildrequires_and_requires
- [2] https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make
- [3] https://docs.fedoraproject.org/en-US/packaging-guidelines/#_why_the_makeinstall_macro_should_not_be_used

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.47-2
- Perl 5.30 rebuild

* Wed Feb 13 2019 Matus Honek <mhonek@redhat.com> - 2.4.47-1
- Rebase to upstream version 2.4.47

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.46-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 2.4.46-12
- Rebuilt for libcrypt.so.2 (#1666033)

* Mon Dec 17 2018 Matus Honek <mhonek@redhat.com> - 2.4.46-11
- Reference default system-wide CA certificates in manpages (#1611591)

* Tue Oct 16 2018 Matus Honek <mhonek@redhat.com> - 2.4.46-10
- Revert "Fix: Cannot use SSL3 anymore"

* Mon Oct 08 2018 Matus Honek <mhonek@redhat.com> - 2.4.46-9
- Backport upstream fixes for ITS 7595 - add OpenSSL EC support (#1623495)

* Tue Aug 14 2018 Matus Honek <mhonek@redhat.com> - 2.4.46-8
- Fix: Cannot use SSL3 anymore (#1592431)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.46-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul  6 2018 Matus Honek <mhonek@redhat.com> - 2.4.46-6
- Build with LDAP_USE_NON_BLOCKING_TLS (#1594928)
- Remove unused leftover MozNSS Compat. Layer references (cont.) (#1557967)

* Fri Jul 06 2018 Petr Pisar <ppisar@redhat.com> - 2.4.46-5
- Perl 5.28 rebuild

* Wed Jul  4 2018 Matus Honek <mhonek@redhat.com> - 2.4.46-4
- Remove unused leftover MozNSS Compat. Layer references (#1557967)

* Wed Jul  4 2018 Matus Honek <mhonek@redhat.com> - 2.4.46-3
- MozNSS Compat. Layer: Make log messages more clear (#1598103)
- MozNSS Compat. Layer: Fix memleaks reported by valgrind (#1595203)

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.46-2
- Perl 5.28 rebuild
- MozNSS Compat. Layer: Fix typos, and spelling in the README file header (#1564161)

* Tue Mar 27 2018 Matus Honek <mhonek@redhat.com> - 2.4.46-1
- Rebase to version OpenLDAP 2.4.46 (#1559652)

* Mon Mar  5 2018 Matus Honek <mhonek@redhat.com> - 2.4.45-14
- Utilize system-wide crypto-policies (#1483979)

* Thu Mar  1 2018 Matus Honek <mhonek@redhat.com> - 2.4.45-13
- fix: openldap does not use Fedora build flags
  + makes use of redhat-rpm-config package
- Drop superfluous back-sql linking patch

* Wed Feb 28 2018 Matus Honek <mhonek@redhat.com> - 2.4.45-12
- MozNSS Compat. Layer: fix: libldap tlsmc continues even after it fails to extract CA certificates (#1550110)

* Wed Feb 21 2018 Matus Honek <mhonek@redhat.com> - 2.4.45-11
- TLS: Use system trusted CA store by default (#1270678, #1537259)

* Sun Feb 11 2018 Matus Honek <mhonek@redhat.com> - 2.4.45-10
- Complete change: Disable TLSMC in F29+

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.4.45-9
- Escape macros in %%changelog
- Disable TLSMC in F29+
- Remove obsolete Group tag
- Don't call ldconfig in servers subpackage
- Switch to %%ldconfig_scriptlets
- Remove unneeded Requires(post): systemd-sysv, chkconfig
- Switch to %%systemd_requires
- Change BuildRequires: systemd-units to systemd

* Wed Feb  7 2018 Matus Honek <mhonek@redhat.com> - 2.4.45-8
- Drop TCP wrappers support (#1531487)

* Wed Feb  7 2018 Matus Honek <mhonek@redhat.com> - 2.4.45-7
- MozNSS Compat. Layer fixes (#1400570)
  - fix incorrect parsing of CACertDir (orig. #1533955)
  - fix PIN disclaimer not always shown (orig. #1516409)
  - fix recursive directory deletion (orig. #1516409)
  - Ensure consistency of a PEM dir before usage (orig. #1516409)
    + Warn just before use of a PIN about key file extraction
  - Enable usage of NSS DB with PEM cert/key (orig. #1525485)
    + Fix a possible invalid dereference (covscan)

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 2.4.45-6
- Rebuilt for switch to libxcrypt

* Wed Dec  6 2017 Matus Honek <mhonek@redhat.com> - 2.4.45-5
- Fix issues in MozNSS compatibility layer (#1400570)
  + Force write file with fsync to avoid race conditions
  + Always filestamp both sql and dbm NSS DB variants to not rely on default DB type prefix
  + Allow missing cert and key which is a valid usecase
  + Create extraction folder only in /tmp to simplify selinux rules
  + Fix Covscan issues

* Fri Nov  3 2017 Matus Honek <mhonek@redhat.com> - 2.4.45-4
- Build with OpenSSL with MozNSS compatibility layer (#1400570)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul  7 2017 Matus Honek <mhonek@redhat.com> - 2.4.45-1
- Rebase to version 2.4.45 (#1458081)
  * fixes CVE-2017-9287 (#1456712, #1456713)
- Update the 'sources' file with new SHA512 hashes

* Fri Jul  7 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-12
- Change Requires to Recommends for nss-tools (#1415086)

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.44-11
- Perl 5.26 rebuild

* Fri Mar 31 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-10
- NSS: Maximal TLS protocol version should be equal to NSS default (#1435692)

* Thu Mar 30 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-9
- NSS: Enhance OpenLDAP to support TLSv1.3 protocol with NSS (#1435692)
- NSS: Rearrange ciphers-, parsing-, and protocol-related patches (#1435692)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.44-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-7
- NSS: Update list of ciphers (#1387868)

* Mon Jan 30 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-6
- NSS: Use what NSS considers default for DEFAULT cipher string (#1387868)

* Thu Jan 26 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-5
- NSS: fix: incorrect multi-keyword parsing and support new ones (#1243517)

* Mon Jan 23 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-4
- fix previous commit (#1375432)

* Fri Jan 20 2017 Matus Honek <mhonek@redhat.com> - 2.4.44-3
- fix: Setting olcTLSProtocolMin does not change supported protocols (#1375432)
- fix: slapd should start after network-online.service (#1336487)

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.44-2
- Perl 5.24 rebuild

* Wed May 11 2016 Matus Honek <mhonek@redhat.com> - 2.4.44-1
- Update to 2.4.44 (#1305191)

* Tue May  3 2016 Matus Honek <mhonek@redhat.com> - 2.4.43-5
- Bring back *.la files in %%{_libdir}/openldap/ (#1331484)

* Wed Apr 27 2016 Matus Honek <mhonek@redhat.com> - 2.4.43-4
- Keep *.so libraries in %%{_libdir}/openldap/ (#1331484)
- Include AllOp overlay (#1319782)

* Sun Apr 10 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.43-3
- Ensure all libtool archive files are removed (.la)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.4.43-1
- Update to 2.4.43 (#1253871)

* Thu Jul 16 2015 Matúš Honěk <mhonek@redhat.com> - 2.4.41-1
- New upstream release 2.4.41 (#1238251)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.40-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.40-13
- Perl 5.22 rebuild

* Mon Apr 27 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-12
- fix: bring back tmpfiles config (#1215655)

* Mon Mar 30 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-11
- remove spurious ghosted file

* Fri Feb 20 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-10
- link against moznss again (#1187742)

* Wed Feb 11 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-9
- fix: Unknown Berkeley DB major version in db.h (#1191098)

* Tue Feb 10 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-9
- CVE-2015-1545: slapd crashes on search with deref control (#1190645)

* Tue Jan 27 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-8
- link against openssl by default
- simplify package even more by removing certificate generation

* Mon Jan 26 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-7
- remove tmpfiles config since it's no longer needed
- fix invalid ldif
- simplify checking for missing server configuration

* Fri Jan 16 2015 Jan Synáček <jsynacek@redhat.com> - 2.4.40-6
- remove openldap-fedora-systemd.patch
- remove openldap-ldaprc-currentdir.patch
- remove openldap-userconfig-setgid.patch
- remove openldap-syncrepl-unset-tls-options.patch
- remove unneeded configure flags, disable sql backend and aci
- make mdb default after a new installation
- remove pid file and args file
- renumber patches and sources

* Wed Dec 17 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.40-5
- harden the build
- improve check_password
- provide an unversioned symlink to check_password.so.1.1

* Tue Dec 16 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.40-4
- remove openldap.pc

* Tue Dec  9 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.40-3
- enhancement: generate openldap.pc (#1171493)

* Fri Nov 14 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.40-2
- enhancement: support TLSv1 and later (#1160466)

* Mon Oct  6 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.40-1
- new upstream release (#1147877)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2.4.39-12
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.39-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 2.4.39-10
- fix license handling

* Mon Jul 14 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-9
- fix: fix typo in generate-server-cert.sh (#1117229)

* Mon Jun  9 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-8
- fix: make default service configuration listen on ldaps:/// as well (#1105634)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.39-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-6
- fix: remove correct tmp file when generating server cert (#1103102)

* Mon Mar 24 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-5
- re-symlink unversioned libraries, so ldconfig is not confused (#1028557)

* Tue Mar  4 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-4
- don't automatically convert slapd.conf to slapd-config

* Wed Feb 19 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-3
- remove redundant sysconfig-related stuff
- add documentation reference to service file
- alias slapd.service as openldap.service

* Tue Feb  4 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-2
- CVE-2013-4449: segfault on certain queries with rwm overlay (#1060851)

* Wed Jan 29 2014 Jan Synáček <jsynacek@redhat.com> - 2.4.39-1
- new upstream release (#1059186)

* Mon Nov 18 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.38-1
- new upstream release (#1031608)

* Mon Nov 11 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.37-2
- fix: slaptest incorrectly handles 'include' directives containing a custom file (#1028935)

* Wed Oct 30 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.37-1
- new upstream release (#1023916)
- fix: missing a linefeed at the end of file /etc/openldap/ldap.conf (#1019836)

* Mon Oct 21 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.36-4
- fix: slapd daemon fails to start with segmentation fault on s390x (#1020661)

* Tue Oct 15 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.36-3
- rebuilt for libdb-5.3.28

* Mon Oct 14 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.36-2
- fix: CLDAP is broken for IPv6 (#1018688)

* Wed Sep  4 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.36-2
- fix: typos in manpages

* Tue Aug 20 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.36-1
- new upstream release
  + compile-in mdb backend

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.35-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.4.35-6
- Perl 5.18 rebuild

* Fri Jun 14 2013 Jan Synáček <jsynacek@redhat.com> - 2.4.35-5
- fix: using slaptest to convert slapd.conf to LDIF format ignores "loglevel 0"

* Thu May 09 2013 Jan Synáček <jsynacek@redhat.com> 2.4.35-4
- do not needlessly run ldconfig after installing openldap-devel
- fix: LDAPI with GSSAPI does not work if SASL_NOCANON=on (#960222)
- fix: lt_dlopen() with back_perl (#960048)

* Tue Apr 09 2013 Jan Synáček <jsynacek@redhat.com> 2.4.35-3
- fix: minor documentation fixes
- set SASL_NOCANON to on by default (#949864)
- remove trailing spaces

* Fri Apr 05 2013 Jan Synáček <jsynacek@redhat.com> 2.4.35-2
- drop the evolution patch

* Tue Apr 02 2013 Jan Synáček <jsynacek@redhat.com> 2.4.35-1
- new upstream release (#947235)
- fix: slapd.service should ensure that network is up before starting (#946921)
- fix: NSS related resource leak (#929357)

* Mon Mar 18 2013 Jan Synáček <jsynacek@redhat.com> 2.4.34-2
- fix: syncrepl push DELETE operation does not recover (#920482)
- run autoreconf every build, drop autoreconf patch (#926280)

* Mon Mar 11 2013 Jan Synáček <jsynacek@redhat.com> 2.4.34-1
- enable perl backend (#820547)
- package ppolicy-check-password (#829749)
- add perl specific BuildRequires
- fix bogus dates

* Wed Mar 06 2013 Jan Vcelak <jvcelak@fedoraproject.org> 2.4.34-1
- new upstream release (#917603)
- fix: slapcat segfaults if cn=config.ldif not present (#872784)
- use systemd-rpm macros in spec file (#850247)

* Thu Jan 31 2013 Jan Synáček <jsynacek@redhat.com> 2.4.33-4
- rebuild against new cyrus-sasl

* Wed Oct 31 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.33-3
- fix update: libldap does not load PEM certificate if certdb is used as TLS_CACERTDIR (#857455)

* Fri Oct 12 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.33-2
- fix: slapd with rwm overlay segfault following ldapmodify (#865685)

* Thu Oct 11 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.33-1
- new upstream release:
  + slapd: ACLs, syncrepl
  + backends: locking and memory management in MDB
  + manpages: slapo-refint
- patch update: MozNSS certificate database in SQL format cannot be used (#860317)
- fix: slapd.service should not use /tmp (#859019)

* Fri Sep 14 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.32-3
- fix: some TLS ciphers cannot be enabled (#852338)
- fix: connection hangs after fallback to second server when certificate hostname verification fails (#852476)
- fix: not all certificates in OpenSSL compatible CA certificate directory format are loaded (#852786)
- fix: MozNSS certificate database in SQL format cannot be used (#857373)
- fix: libldap does not load PEM certificate if certdb is used as TLS_CACERTDIR (#857455)

* Mon Aug 20 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.32-2
- enhancement: TLS, prefer private keys from authenticated slots
- enhancement: TLS, allow certificate specification including token name
- resolve TLS failures in replication in 389 Directory Server

* Wed Aug 01 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.32-1
- new upstream release
  + library: double free, SASL handling
  + tools: read SASL_NOCANON from config file
  + slapd: config index renumbering, duplicate error response
  + backends: various fixes in mdb, bdb/hdb, ldap
  + accesslog, syncprov: fix memory leaks in with replication
  + sha2: portability, thread safety, support SSHA256,384,512
  + documentation fixes

* Sat Jul 21 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-7
- fix: slapd refuses to set up TLS with self-signed PEM certificate (#842022)

* Fri Jul 20 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-6
- multilib fix: move libslapi from openldap-servers to openldap package

* Thu Jul 19 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-5
- fix: querying for IPv6 DNS records when IPv6 is disabled on the host (#835013)
- fix: smbk5pwd module computes invalid LM hashes (#841560)

* Wed Jul 18 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-4
- modify the package build process
  + fix autoconfig files to detect Mozilla NSS library using pkg-config
  + remove compiler flags which are not needed currently
  + build server, client and library together
  + avoid stray dependencies by using --as-needed linker flag
  + enable SLAPI interface in slapd

* Wed Jun 27 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-3
- update fix: count constraint broken when using multiple modifications (#795766)
- fix: invalid order of TLS shutdown operations (#808464)
- fix: TLS error messages overwriting in tlsm_verify_cert() (#810462)
- fix: reading pin from file can make all TLS connections hang (#829317)
- CVE-2012-2668: cipher suite selection by name can be ignored (#825875)
- fix: slapd fails to start on reboot (#829272)
- fix: default cipher suite is always selected (#828790)
- fix: less influence between individual TLS contexts:
  - replication with TLS does not work (#795763)
  - possibly others

* Fri May 18 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-2
- fix: nss-tools package is required by the base package, not the server subpackage
- fix: MozNSS CA certdir does not work together with PEM CA cert file (#819536)

* Tue Apr 24 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.31-1
- new upstream release
  + library: IPv6 url detection
  + library: rebinding to failed connections
  + server: various fixes in mdb backend
  + server: various fixes in replication
  + server: various fixes in overlays and minor backends
  + documentation fixes
- remove patches which were merged upstream

* Thu Apr 05 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.30-3
- rebuild due to libdb rebase

* Mon Mar 26 2012 Jan Synáček <jsynacek@redhat.com> 2.4.30-2
- fix: Re-binding to a failed connection can segfault (#784989)

* Thu Mar 01 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.30-1
- new upstream release
  + server: fixes in mdb backend
  + server: fixes in manual pages
  + server: fixes in syncprov, syncrepl, and pcache
- removed patches which were merged upstream

* Wed Feb 22 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.29-4
- fix: missing options in manual pages of client tools (#796232)
- fix: SASL_NOCANON option missing in ldap.conf manual page (#732915)

* Tue Feb 21 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.29-3
- fix: ldap_result does not succeed for sssd (#771484)
- Jan Synáček <jsynacek@redhat.com>:
  + fix: count constraint broken when using multiple modifications (#795766)

* Mon Feb 20 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.29-2
- fix update: provide ldif2ldbm, not ldib2ldbm (#437104)
- Jan Synáček <jsynacek@redhat.com>:
  + unify systemctl binary paths throughout the specfile and make them usrmove compliant
  + make path to chkconfig binary usrmove compliant

* Wed Feb 15 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.29-1
- new upstream release
  + MozNSS fixes
  + connection handling fixes
  + server: buxfixes in mdb backend
  + server: buxfixes in overlays (syncrepl, meta, monitor, perl, sql, dds, rwm)
- openldap-servers now provide ldib2ldbm (#437104)
- certificates management improvements
  + create empty Mozilla NSS certificate database during installation
  + enable builtin Root CA in generated database (#789088)
  + generate server certificate using Mozilla NSS tools instead of OpenSSL tools
  + fix: correct path to check-config.sh in service file (Jan Synáček <jsynacek@redhat.com>)
- temporarily disable certificates checking in check-config.sh script
- fix: check-config.sh get stuck when executing command as a ldap user

* Tue Jan 31 2012 Jan Vcelak <jvcelak@redhat.com> 2.4.28-3
- fix: replication (syncrepl) with TLS causes segfault (#783431)
- fix: slapd segfaults when PEM certificate is used and key is not set (#772890)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.28-1
- new upstream release
  + server: support for delta-syncrepl in multi master replication
  + server: add experimental backend - MDB
  + server: dynamic configuration for passwd, perl, shell, sock, and sql backends
  + server: support passwords in APR1
  + library: support for Wahl (draft)
  + a lot of bugfixes
- remove patches which were merged upstream
- compile backends as modules (except BDB, HDB, and monitor)
- reload systemd daemon after installation

* Tue Nov 01 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-6
- package cleanup:
  + hardened build: switch from LDFLAGS to RPM macros
  + remove old provides and obsoletes
  + add new slapd maintainance scripts
  + drop defattr macros, clean up permissions in specfile
  + fix rpmlint warnings: macros in comments/changelog
  + fix rpmlint warnings: non UTF-8 documentation
  + rename environment file to be more consistent (ldap -> slapd)
- replace sysv initscript with systemd service file (#
- new format of environment file due to switch to systemd
  (automatic conversion is performed)
- patch OpenLDAP to skip empty command line arguments
  (arguments expansion in systemd works different than in shell)
- CVE-2011-4079: one-byte buffer overflow in slapd (#749324)

* Thu Oct 06 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-5
- rebuild: openldap does not work after libdb rebase (#743824)
- regression fix: openldap built without tcp_wrappers (#743213)

* Wed Sep 21 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-4
- new feature update: honor priority/weight with ldap_domain2hostlist (#733078)

* Mon Sep 12 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-3
- fix: SSL_ForceHandshake function is not thread safe (#701678)
- fix: allow unsetting of tls_* syncrepl options (#734187)

* Wed Aug 24 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-2
- security hardening: library needs partial RELRO support added (#733071)
- fix: NSS_Init* functions are not thread safe (#731112)
- fix: incorrect behavior of allow/try options of VerifyCert and TLS_REQCERT (#725819)
- fix: memleak - free the return of tlsm_find_and_verify_cert_key (#725818)
- fix: conversion of constraint overlay settings to cn=config is incorrect (#733067)
- fix: DDS overlay tolerance parametr doesn't function and breakes default TTL (#733069)
- manpage fix: errors in manual page slapo-unique (#733070)
- fix: matching wildcard hostnames in certificate Subject field does not work (#733073)
- new feature: honor priority/weight with ldap_domain2hostlist (#733078)
- manpage fix: wrong ldap_sync_destroy() prototype in ldap_sync(3) manpage (#717722)

* Sun Aug 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.4.26-1.1
- Rebuilt for rpm (#728707)

* Wed Jul 20 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.26-1
- rebase to new upstream release
- fix: memleak in tlsm_auth_cert_handler (#717730)

* Mon Jun 27 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.25-1
- rebase to new upstream release
- change default database type from BDB to HDB
- enable ldapi:/// interface by default
- set cn=config management ACLs for root user, SASL external schema (#712495)
- fix: server scriptlets require initscripts package (#716857)
- fix: connection fails if TLS_CACERTDIR doesn't exist but TLS_REQCERT
  is set to 'never' (#716854)
- fix: segmentation fault caused by double-free in ldapexop (#699683)
- fix: segmentation fault of client tool when input line in LDIF file
  is splitted but indented incorrectly (#716855)
- fix: segmentation fault of client tool when LDIF input file is not terminated
  by a new line character (#716858)

* Fri Mar 18 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-2
- new: system resource limiting for slapd using ulimit
- fix update: openldap can't use TLS after a fork() (#636956)
- fix: possible null pointer dereference in NSS implementation
- fix: openldap-servers upgrade hangs or do not upgrade the database (#664433)

* Mon Feb 14 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.24-1
- rebase to 2.4.24
- BDB backend switch from DB4 to DB5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.23-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-8
- fix update: openldap can't use TLS after a fork() (#636956)

* Tue Jan 25 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-7
- fix: openldap can't use TLS after a fork() (#636956)
- fix: openldap-server upgrade gets stuck when the database is damaged (#664433)

* Thu Jan 20 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-6
- fix: some server certificates refused with inadequate type error (#668899)
- fix: default encryption strength dropped in switch to using NSS (#669446)
- systemd compatibility: add configuration file (#656647, #668223)

* Thu Jan 06 2011 Jan Vcelak <jvcelak@redhat.com> 2.4.23-5
- initscript: slaptest with '-u' to skip database opening (#667768)
- removed slurpd options from sysconfig/ldap
- fix: verification of self issued certificates (#657984)

* Mon Nov 22 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-4
- Mozilla NSS - implement full non-blocking semantics
  ldapsearch -Z hangs server if starttls fails (#652822)
- updated list of all overlays in slapd.conf (#655899)
- fix database upgrade process (#656257)

* Thu Nov 18 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-3
- add support for multiple prefixed Mozilla NSS database files in TLS_CACERTDIR
- reject non-file keyfiles in TLS_CACERTDIR (#652315)
- TLS_CACERTDIR precedence over TLS_CACERT (#652304)
- accept only files in hash.0 format in TLS_CACERTDIR (#650288)
- improve SSL/TLS trace messages (#652818)

* Mon Nov 01 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-2
- fix possible infinite loop when checking permissions of TLS files (#641946)
- removed outdated autofs.schema (#643045)
- removed outdated README.upgrade
- removed relics of migrationtools

* Fri Aug 27 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.23-1
- rebase to 2.4.23
- embeded db4 library removed
- removed bogus links in "SEE ALSO" in several man-pages (#624616)

* Thu Jul 22 2010 Jan Vcelak <jvcelak@redhat.com> 2.4.22-7
- Mozilla NSS - delay token auth until needed (#616552)
- Mozilla NSS - support use of self signed CA certs as server certs (#614545)

* Tue Jul 20 2010 Jan Vcelak <jvcelak@redhat.com> - 2.4.22-6
- CVE-2010-0211 openldap: modrdn processing uninitialized pointer free (#605448)
- CVE-2010-0212 openldap: modrdn processing IA5StringNormalize NULL pointer dereference (#605452)
- obsolete configuration file moved to /usr/share/openldap-servers (#612602)

* Thu Jul 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-5
- another shot at previous fix

* Thu Jul 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-4
- fixed issue with owner of /usr/lib/ldap/__db.* (#609523)

* Thu Jun  3 2010 Rich Megginson <rmeggins@redhat.com> - 2.4.22-3
- added ldif.h to the public api in the devel package
- added -lldif to the public api
- added HAVE_MOZNSS and other flags to use Mozilla NSS for crypto

* Tue May 18 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-2
- rebuild with connectionless support (#587722)
- updated autofs schema (#584808)

* Tue May 04 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.22-1
- rebased to 2.4.22 (mostly bugfixes, added back-ldif, back-null testing support)
- due to some possible issues pointed out in last update testing phase, I'm
  pulling back the last change (slapd can't be moved since it depends on /usr
  possibly mounted from network)

* Fri Mar 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-6
- moved slapd to start earlier during boot sequence

* Tue Mar 16 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-5
- minor corrections of init script (#571235, #570057, #573804)

* Wed Feb 24 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-4
- fixed SIGSEGV when deleting data using hdb (#562227)

* Mon Feb 01 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-3
- fixed broken link /usr/sbin/slapschema (#559873)

* Tue Jan 19 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-2
- removed some static libraries from openldap-devel (#556090)

* Mon Jan 11 2010 Jan Zeleny <jzeleny@redhat.com> - 2.4.21-1
- rebased openldap to 2.4.21
- rebased bdb to 4.8.26

* Mon Nov 23 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-3
- minor corrections in init script

* Mon Nov 16 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-2
- fixed tls connection accepting when TLSVerifyClient = allow
- /etc/openldap/ldap.conf removed from files owned by openldap-servers
- minor changes in spec file to supress warnings
- some changes in init script, so it would be possible to use it when
  using old configuration style

* Fri Nov 06 2009 Jan Zeleny <jzeleny@redhat.com> - 2.4.19-1
- rebased openldap to 2.4.19
- rebased bdb to 4.8.24

* Wed Oct 07 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-4
- updated smbk5pwd patch to be linked with libldap (#526500)
- the last buffer overflow patch replaced with the one from upstream
- added /etc/openldap/slapd.d and /etc/openldap/slapd.conf.bak
  to files owned by openldap-servers

* Thu Sep 24 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-3
- cleanup of previous patch fixing buffer overflow

* Tue Sep 22 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-2
- changed configuration approach. Instead od slapd.conf slapd
  is using slapd.d directory now
- fix of some issues caused by renaming of init script
- fix of buffer overflow issue in ldif.c pointed out by new glibc

* Fri Sep 18 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.18-1
- rebase of openldap to 2.4.18

* Wed Sep 16 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-7
- updated documentation (hashing the cacert dir)

* Wed Sep 16 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-6
- updated init script to be LSB-compliant (#523434)
- init script renamed to slapd

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 2.4.16-5
- rebuilt with new openssl

* Tue Aug 25 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-4
- updated %%pre script to correctly install openldap group

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.16-1
- rebase of openldap to 2.4.16
- fixed minor issue in spec file (output looking interactive
  when installing servers)

* Tue Jun 09 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-4
- added $SLAPD_URLS variable to init script (#504504)

* Thu Apr 09 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-3
- extended previous patch (#481310) to remove options cfMP
  from some client tools
- correction of patch setugid (#494330)

* Thu Mar 26 2009 Jan Zeleny <jzeleny@redhat.com> 2.4.15-2
- removed -f option from some client tools (#481310)

* Wed Feb 25 2009 Jan Safranek <jsafranek@redhat.com> 2.4.15-1
- new upstream release

* Tue Feb 17 2009 Jan Safranek <jsafranek@redhat.com> 2.4.14-1
- new upstream release
- upgraded to db-4.7.25

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> 2.4.12-3
- rebuild with new openssl

* Mon Dec 15 2008 Caolán McNamara <caolanm@redhat.com> 2.4.12-2
- rebuild for libltdl, i.e. copy config.sub|guess from new location

* Wed Oct 15 2008 Jan Safranek <jsafranek@redhat.com> 2.4.12-1
- new upstream release

* Mon Oct 13 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-3
- add SLAPD_SHUTDOWN_TIMEOUT to /etc/sysconfig/ldap, allowing admins
  to set non-default slapd shutdown timeout
- add checkpoint to default slapd.conf file (#458679)

* Mon Sep  1 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-2
- provide ldif2ldbm functionality for migrationtools
- rediff all patches to get rid of patch fuzz

* Mon Jul 21 2008 Jan Safranek <jsafranek@redhat.com> 2.4.11-1
- new upstream release
- apply official bdb-4.6.21 patches

* Wed Jul  2 2008 Jan Safranek <jsafranek@redhat.com> 2.4.10-2
- fix CVE-2008-2952 (#453728)

* Thu Jun 12 2008 Jan Safranek <jsafranek@redhat.com> 2.4.10-1
- new upstream release

* Wed May 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.9-5
- use /sbin/nologin as shell of ldap user (#447919)

* Tue May 13 2008 Jan Safranek <jsafranek@redhat.com> 2.4.9-4
- new upstream release
- removed unnecessary MigrationTools patches

* Thu Apr 10 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-4
- bdb upgraded to 4.6.21
- reworked upgrade logic again to run db_upgrade when bdb version
  changes

* Wed Mar  5 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-3
- reworked the upgrade logic, slapcat/slapadd of the whole database
  is needed only if minor version changes (2.3.x -> 2.4.y)
- do not try to save database in LDIF format, if openldap-servers package
  is  being removed (it's up to the admin to do so manually)

* Thu Feb 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-2
- migration tools carved out to standalone package "migrationtools"
  (#236697)

* Fri Feb 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.8-1
- new upstream release

* Fri Feb  8 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-7
- fix CVE-2008-0658 (#432014)

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-6
- init script fixes

* Mon Jan 28 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-5
- init script made LSB-compliant (#247012)

* Fri Jan 25 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-4
- fixed rpmlint warnings and errors
  - /etc/openldap/schema/README moved to /usr/share/doc/openldap

* Tue Jan 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-3
- obsoleting compat-openldap properly again :)

* Tue Jan 22 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-2
- obsoleting compat-openldap properly (#429591)

* Mon Jan 14 2008 Jan Safranek <jsafranek@redhat.com> 2.4.7-1
- new upstream version (openldap-2.4.7)

* Mon Dec  3 2007 Jan Safranek <jsafranek@redhat.com> 2.4.6-1
- new upstream version (openldap-2.4)
- deprecating compat- package

* Mon Nov  5 2007 Jan Safranek <jsafranek@redhat.com> 2.3.39-1
- new upstream release

* Tue Oct 23 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-4
- fixed multilib issues - all platform independent files have the
  same content now (#342791)

* Thu Oct  4 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-3
- BDB downgraded back to 4.4.20 because 4.6.18 is not supported by
  openldap (#314821)

* Mon Sep 17 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-2
- skeleton /etc/sysconfig/ldap added
- new SLAPD_LDAP option to turn off listening on ldap:/// (#292591)
- fixed checking of SSL (#292611)
- fixed upgrade with empty database

* Thu Sep  6 2007 Jan Safranek <jsafranek@redhat.com> 2.3.38-1
- new upstream version
- added images to the guide.html (#273581)

* Wed Aug 22 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-3
- just rebuild

* Thu Aug  2 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-2
- do not use specific automake and autoconf
- do not distinguish between NPTL and non-NPTL platforms, we have NPTL
  everywhere
- db-4.6.18 integrated
- updated openldap-servers License: field to reference BDB license

* Tue Jul 31 2007 Jan Safranek <jsafranek@redhat.com> 2.3.37-1
- new upstream version

* Fri Jul 20 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-7
- MigrationTools-47 integrated

* Wed Jul  4 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-6
- fix compat-slapcat compilation. Now it can be found in
  /usr/lib/compat-openldap/slapcat, because the tool checks argv[0]
  (#246581)

* Fri Jun 29 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-5
- smbk5pwd added (#220895)
- correctly distribute modules between servers and servers-sql packages

* Mon Jun 25 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-4
- Fix initscript return codes (#242667)
- Provide overlays (as modules; #246036, #245896)
- Add available modules to config file

* Tue May 22 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-3
- do not create script in /tmp on startup (bz#188298)
- add compat-slapcat to openldap-compat (bz#179378)
- do not import ddp services with migrate_services.pl
  (bz#201183)
- sort the hosts by adders, preventing duplicities
  in migrate*nis*.pl (bz#201540)
- start slupd for each replicated database (bz#210155)
- add ldconfig to devel post/postun (bz#240253)
- include misc.schema in default slapd.conf (bz#147805)

* Mon Apr 23 2007 Jan Safranek <jsafranek@redhat.com> 2.3.34-2
- slapadd during package update is now quiet (bz#224581)
- use _localstatedir instead of var/ during build (bz#220970)
- bind-libbind-devel removed from BuildRequires (bz#216851)
- slaptest is now quiet during service ldap start, if
  there is no error/warning (bz#143697)
- libldap_r.so now links with pthread (bz#198226)
- do not strip binaries to produce correct .debuginfo packages
  (bz#152516)

* Mon Feb 19 2007 Jay Fenlason <fenlason<redhat.com> 2.3.34-1
- New upstream release
- Upgrade the scripts for migrating the database so that they might
  actually work.
- change bind-libbind-devel to bind-devel in BuildPreReq

* Mon Dec  4 2006 Thomas Woerner <twoerner@redhat.com> 2.3.30-1.1
- tcp_wrappers has a new devel and libs sub package, therefore changing build
  requirement for tcp_wrappers to tcp_wrappers-devel

* Wed Nov 15 2006 Jay Fenlason <fenlason@redhat.com> 2.3.30-1
- New upstream version

* Wed Oct 25 2006 Jay Fenlason <fenlason@redhat.com> 2.3.28-1
- New upstream version

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.3.27-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 Jay Fenlason <fenlason@redhat.com> 2.3.27-3
- Include --enable-multimaster to close
  bz#185821: adding slapd_multimaster to the configure options
- Upgade guide.html to the correct one for openladp-2.3.27, closing
  bz#190383: openldap 2.3 packages contain the administrator's guide for 2.2
- Remove the quotes from around the slaptestflags in ldap.init
  This closes one part of
  bz#204593: service ldap fails after having added entries to ldap
- include __db.* in the list of files to check ownership of in
  ldap.init, as suggested in
  bz#199322: RFE: perform cleanup in ldap.init

* Fri Aug 25 2006 Jay Fenlason <fenlason@redhat.com> 2.3.27-2
- New upstream release
- Include the gethostbyname_r patch so that nss_ldap won't hang
  on recursive attemts to ldap_initialize.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.24-2.1
- rebuild

* Wed Jun 7 2006 Jay Fenlason <fenlason@redhat.com> 2.3.24-2
- New upstream version

* Thu Apr 27 2006 Jay Fenlason <fenlason@redhat.com> 2.3.21-2
- Upgrade to 2.3.21
- Add two upstream patches for db-4.4.20

* Mon Feb 13 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-4
- Re-fix ldap.init

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.19-3.1
- bump again for double-long bug on ppc(64)

* Thu Feb 9 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-3
- Modify the ldap.init script to call runuser correctly.

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.19-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 10 2006 Jay Fenlason <fenlason@redhat.com> 2.3.19-2
- Upgrade to 2.3.19, which upstream now considers stable
- Modify the -config.patch, ldap.init, and this spec file to put the
  pid file and args file in an ldap-owned openldap subdirectory under
  /var/run.
- Move back_sql* out of _sbindir/openldap , which requires
  hand-moving slapd and slurpd to _sbindir, and recreating symlinks
  by hand.
- Retire openldap-2.3.11-ads.patch, which went upstream.
- Update the ldap.init script to run slaptest as the ldap user rather
  than as root.  This solves
  bz#150172 Startup failure after database problem
- Add to the servers post and preun scriptlets so that on preun, the
  database is slapcatted to /var/lib/ldap/upgrade.ldif and the
  database files are saved to /var/lib/ldap/rpmorig.  On post, if
  /var/lib/ldap/upgrade.ldif exists, it is slapadded.  This means that
  on upgrades from 2.3.16-2 to higher versions, the database files may
  be automatically upgraded.  Unfortunatly, because of the changes to
  the preun scriptlet, users have to do the slapcat, etc by hand when
  upgrading to 2.3.16-2.  Also note that the /var/lib/ldap/rpmorig
  files need to be removed by hand because automatically removing your
  emergency fallback files is a bad idea.
- Upgrade internal bdb to db-4.4.20.  For a clean upgrade, this will
  require that users slapcat their databases into a temp file, move
  /var/lib/ldap someplace safe, upgrade the openldap rpms, then
  slapadd the temp file.


* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Jay Fenlason <fenlason@redhat.com> 2.3.11-3
- Remove Requires: cyrus-sasl and cyrus-sasl-md5 from openldap- and
  compat-openldap- to close
  bz#173313 Remove exlicit 'Requires: cyrus-sasl" + 'Requires: cyrus-sasl-md5'

* Thu Nov 10 2005 Jay Fenlason <fenlason@redhat.com> 2.3.11-2
- Upgrade to 2.3.11, which upstream now considers stable.
- Switch compat-openldap to 2.2.29
- remove references to nss_ldap_build from the spec file
- remove references to 2.0 and 2.1 from the spec file.
- reorganize the build() function slightly in the spec file to limit the
  number of redundant and conflicting options passedto configure.
- Remove the attempt to hardlink ldapmodify and ldapadd together, since
  the current make install make ldapadd a symlink to ldapmodify.
- Include the -ads patches to allow SASL binds to an Active Directory
  server to work.  Nalin <nalin@redhat.com> wrote the patch, based on my
  broken first attempt.

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 2.2.29-3
- rebuilt against new openssl

* Mon Oct 10 2005 Jay Fenlason <fenlason@redhat.com> 2.2.29-2
- New upstream version.

* Thu Sep 29 2005 Jay Fenlason <fenlason@redhat.com> 2.2.28-2
- Upgrade to nev upstream version.  This makes the 2.2.*-hop patch obsolete.

* Mon Aug 22 2005 Jay Fenlason <fenlason@redhat.com> 2.2.26-2
- Move the slapd.pem file to /etc/pki/tls/certs
  and edit the -config patch to match to close
  bz#143393  Creates certificates + keys at an insecure/bad place
- also use _sysconfdir instead of hard-coding /etc

* Thu Aug 11 2005 Jay Fenlason <fenlason@redhat.com>
- Add the tls-fix-connection-test patch to close
  bz#161991 openldap password disclosure issue
- add the hop patches to prevent infinite looping when chasing referrals.
  OpenLDAP ITS #3578

* Fri Aug  5 2005 Nalin Dahyabhai <nalin@redhat.com>
- fix typo in ldap.init (call $klist instead of klist, from Charles Lopes)

* Thu May 19 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.26-1
- run slaptest with the -u flag if no id2entry db files are found, because
  you can't check for read-write access to a non-existent database (#156787)
- add _sysconfdir/openldap/cacerts, which authconfig sets as the
  TLS_CACERTDIR path in /etc/openldap/ldap.conf now
- use a temporary wrapper script to launch slapd, in case we have arguments
  with embedded whitespace (#158111)

* Wed May  4 2005 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2.26 (stable 20050429)
- enable the lmpasswd scheme
- print a warning if slaptest fails, slaptest -u succeeds, and one of the
  directories listed as the storage location for a given suffix in slapd.conf
  contains a readable file named __db.001 (#118678)

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.25-1
- update to 2.2.25 (release)

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.24-1
- update to 2.2.24 (stable 20050318)
- export KRB5_KTNAME in the init script, in case it was set in the sysconfig
  file but not exported

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-4
- prefer libresolv to libbind

* Tue Mar  1 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-3
- add bind-libbind-devel and libtool-ltdl-devel buildprereqs

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 2.2.23-2
- rebuild with openssl-0.9.7e

* Mon Jan 31 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.23-1
- update to 2.2.23 (stable-20050125)
- update notes on upgrading from earlier versions
- drop slapcat variations for 2.0/2.1, which choke on 2.2's config files

* Tue Jan  4 2005 Nalin Dahyabhai <nalin@redhat.com> 2.2.20-1
- update to 2.2.20 (stable-20050103)
- warn about unreadable krb5 keytab files containing "ldap" keys
- warn about unreadable TLS-related files
- own a ref to subdirectories which we create under _libdir/tls

* Tue Nov  2 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.17-0
- rebuild

* Thu Sep 30 2004 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.2.17 (stable-20040923) (#135188)
- move nptl libraries into arch-specific subdirectories on x86 boxes
- require a newer glibc which can provide nptl libpthread on i486/i586

* Tue Aug 24 2004 Nalin Dahyabhai <nalin@redhat.com>
- move slapd startup to earlier in the boot sequence (#103160)
- update to 2.2.15 (stable-20040822)
- change version number on compat-openldap to include the non-compat version
  from which it's compiled, otherwise would have to start 2.2.15 at release 3
  so that it upgrades correctly

* Thu Aug 19 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-2
- build a separate, static set of libraries for openldap-devel with the
  non-standard ntlm bind patch applied, for use by the evolution-connector
  package (#125579), and installing them under
  evolution_connector_prefix)
- provide openldap-evolution-devel = version-release in openldap-devel
  so that evolution-connector's source package can require a version of
  openldap-devel which provides what it wants

* Mon Jul 26 2004 Nalin Dahyabhai <nalin@redhat.com>
- update administrator guide

* Wed Jun 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-1
- add compat-openldap subpackage
- default to bdb, as upstream does, gambling that we're only going to be
  on systems with nptl now

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 2.2.13-0
- preliminary 2.2.13 update
- move ucdata to the -servers subpackage where it belongs

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.30-1
- build experimental sql backend as a loadable module

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.30-0
- update to 2.1.30

* Thu May 13 2004 Thomas Woerner <twoerner@redhat.com> 2.1.29-3
- removed rpath
- added pie patch: slapd and slurpd are now pie
- requires libtool >= 1.5.6-2 (PIC libltdl.a)

* Fri Apr 16 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-2
- move rfc documentation from main to -devel (#121025)

* Wed Apr 14 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-1
- rebuild

* Tue Apr  6 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.29-0
- update to 2.1.29 (stable 20040329)

* Mon Mar 29 2004 Nalin Dahyabhai <nalin@redhat.com>
- don't build servers with --with-kpasswd, that option hasn't been recognized
  since 2.1.23

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 2.1.25-5.1
- rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 2.1.25-5
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 10 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-4
- remove 'reload' from the init script -- it never worked as intended (#115310)

* Wed Feb  4 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-3
- commit that last fix correctly this time

* Tue Feb  3 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-2
- fix incorrect use of find when attempting to detect a common permissions
  error in the init script (#114866)

* Fri Jan 16 2004 Nalin Dahyabhai <nalin@redhat.com>
- add bug fix patch for DB 4.2.52

* Thu Jan  8 2004 Nalin Dahyabhai <nalin@redhat.com> 2.1.25-1
- change logging facility used from daemon to local4 (#112730, reversing #11047)
  BEHAVIOR CHANGE - SHOULD BE MENTIONED IN THE RELEASE NOTES.

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com>
- incorporate fix for logic quasi-bug in slapd's SASL auxprop code (Dave Jones)

* Thu Dec 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.25, now marked STABLE

* Thu Dec 11 2003 Jeff Johnson <jbj@jbj.org> 2.1.22-9
- update to db-4.2.52.

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-8
- add another section to the ABI note for the TLS libdb so that it's marked as
  not needing an executable stack (from Arjan Van de Ven)

* Thu Oct 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-7
- force bundled libdb to not use O_DIRECT by making it forget that we have it

* Wed Oct 15 2003 Nalin Dahyabhai <nalin@redhat.com>
- build bundled libdb for slapd dynamically to make the package smaller,
  among other things
- on tls-capable arches, build libdb both with and without shared posix
  mutexes, otherwise just without
- disable posix mutexes unconditionally for db 4.0, which shouldn't need
  them for the migration cases where it's used
- update to MigrationTools 45

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 2.1.22-6.1
- upgrade db-4.1.25 to db-4.2.42.

* Fri Sep 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-6
- drop rfc822-MailMember.schema, merged into upstream misc.schema at some point

* Wed Aug 27 2003 Nalin Dahyabhai <nalin@redhat.com>
- actually require newer libtool, as was intended back in 2.1.22-0, noted as
  missed by Jim Richardson

* Fri Jul 25 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-5
- enable rlookups, they don't cost anything unless also enabled in slapd's
  configuration file

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-4
- rebuild

* Thu Jul 17 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-3
- rebuild

* Wed Jul 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-2
- rebuild

* Tue Jul 15 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-1
- build

* Mon Jul 14 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.22-0
- 2.1.22 now badged stable
- be more aggressive in what we index by default
- use/require libtool 1.5

* Mon Jun 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.22

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.21-1
- update to 2.1.21
- enable ldap, meta, monitor, null, rewrite in slapd

* Mon May 19 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.20-1
- update to 2.1.20

* Thu May  8 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.19-1
- update to 2.1.19

* Mon May  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.1.17-1
- switch to db with crypto

* Fri May  2 2003 Nalin Dahyabhai <nalin@redhat.com>
- install the db utils for the bundled libdb as %%{_sbindir}/slapd_db_*
- install slapcat/slapadd from 2.0.x for migration purposes

* Wed Apr 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.1.17
- disable the shell backend, not expected to work well with threads
- drop the kerberosSecurityObject schema, the krbName attribute it
  contains is only used if slapd is built with v2 kbind support

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-8
- back down to db 4.0.x, which 2.0.x can compile with in ldbm-over-db setups
- tweak SuSE patch to fix a few copy-paste errors and a NULL dereference

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-6
- rebuild

* Mon Dec 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-5
- rebuild

* Fri Dec 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-4
- check for setgid as well

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-3
- rebuild

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- incorporate fixes from SuSE's security audit, except for fixes to ITS 1963,
  1936, 2007, 2009, which were included in 2.0.26.
- add two more patches for db 4.1.24 from sleepycat's updates page
- use openssl pkgconfig data, if any is available

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-2
- add patches for db 4.1.24 from sleepycat's updates page

* Mon Nov  4 2002 Nalin Dahyabhai <nalin@redhat.com>
- add a sample TLSCACertificateFile directive to the default slapd.conf

* Tue Sep 24 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.27-1
- update to 2.0.27

* Fri Sep 20 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.26-1
- update to 2.0.26, db 4.1.24.NC

* Fri Sep 13 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.25-2
- change LD_FLAGS to refer to /usr/kerberos/_libdir instead of
  /usr/kerberos/lib, which might not be right on some arches

* Mon Aug 26 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.25-1
- update to 2.0.25 "stable", ldbm-over-gdbm (putting off migration of LDBM
  slapd databases until we move to 2.1.x)
- use %%{_smp_mflags} when running make
- update to MigrationTools 44
- enable dynamic module support in slapd

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-5
- rebuild in new environment

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-3
- use the gdbm backend again

* Mon Feb 18 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-2
- make slapd.conf read/write by root, read by ldap

* Sun Feb 17 2002 Nalin Dahyabhai <nalin@redhat.com>
- fix corner case in sendbuf fix
- 2.0.23 now marked "stable"

* Tue Feb 12 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.23-1
- update to 2.0.23

* Fri Feb  8 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.22-2
- switch to an internalized Berkeley DB as the ldbm back-end  (NOTE: this breaks
  access to existing on-disk directory data)
- add slapcat/slapadd with gdbm for migration purposes
- remove Kerberos dependency in client libs (the direct Kerberos dependency
  is used by the server for checking {kerberos} passwords)

* Fri Feb  1 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.22-1
- update to 2.0.22

* Sat Jan 26 2002 Florian La Roche <Florian.LaRoche@redhat.de> 2.0.21-5
- prereq chkconfig for server subpackage

* Fri Jan 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-4
- update migration tools to version 40

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-3
- free ride through the build system

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.21-2
- update to 2.0.21, now earmarked as STABLE

* Wed Jan 16 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-2
- temporarily disable optimizations for ia64 arches
- specify pthreads at configure-time instead of letting configure guess

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com>
- and one for Raw Hide

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-0.7
- build for RHL 7/7.1

* Mon Jan 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.20-1
- update to 2.0.20 (security errata)

* Thu Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.19-1
- update to 2.0.19

* Tue Nov  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.18-2
- fix the commented-out replication example in slapd.conf

* Fri Oct 26 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.18-1
- update to 2.0.18

* Mon Oct 15 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.17-1
- update to 2.0.17

* Wed Oct 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable kbind support (deprecated, and I suspect unused)
- configure with --with-kerberos=k5only instead of --with-kerberos=k5
- build slapd with threads

* Thu Sep 27 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.15-2
- rebuild, 2.0.15 is now designated stable

* Fri Sep 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.15-1
- update to 2.0.15

* Mon Sep 10 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.14-1
- update to 2.0.14

* Fri Aug 31 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.12-1
- update to 2.0.12 to pull in fixes for setting of default TLS options, among
  other things
- update to migration tools 39
- drop tls patch, which was fixed better in this release

* Tue Aug 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.11-13
- install saucer correctly

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- try to fix ldap_set_options not being able to set global options related
  to TLS correctly

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't attempt to create a cert at install-time, it's usually going
  to get the wrong CN (#51352)

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add a build-time requirement on pam-devel
- add a build-time requirement on a sufficiently-new libtool to link
  shared libraries to other shared libraries (which is needed in order
  for prelinking to work)

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- require cyrus-sasl-md5 (support for DIGEST-MD5 is required for RFC
  compliance) by name (follows from #43079, which split cyrus-sasl's
  cram-md5 and digest-md5 modules out into cyrus-sasl-md5)

* Fri Jul 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- enable passwd back-end (noted by Alan Sparks and Sergio Kessler)

* Wed Jul 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- start to prep for errata release

* Fri Jul  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- link libldap with liblber

* Wed Jul  4 2001 Than Ngo <than@redhat.com> 2.0.11-6
- add symlink liblber.so libldap.so and libldap_r.so in /usr/lib

* Tue Jul  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- move shared libraries to /lib
- redo init script for better internationalization (#26154)
- don't use ldaprc files in the current directory (#38402) (patch from
  hps@intermeta.de)
- add BuildPrereq on tcp wrappers since we configure with
  --enable-wrappers (#43707)
- don't overflow debug buffer in mail500 (#41751)
- don't call krb5_free_creds instead of krb5_free_cred_contents any
  more (#43159)

* Mon Jul  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- make config files noreplace (#42831)

* Tue Jun 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually change the default config to use the dummy cert
- update to MigrationTools 38

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- build dummy certificate in %%post, use it in default config
- configure-time shenanigans to help a confused configure script

* Wed Jun 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak migrate_automount and friends so that they can be run from anywhere

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.11

* Wed May 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.10

* Mon May 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.9

* Tue May 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.8
- drop patch which came from upstream

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Thu Feb  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- back out pidfile patches, which interact weirdly with Linux threads
- mark non-standard schema as such by moving them to a different directory

* Mon Feb  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to MigrationTools 36, adds netgroup support

* Mon Jan 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix thinko in that last patch

* Thu Jan 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- try to work around some buffering problems

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize the init script

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- gettextize the init script

* Fri Jan 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- move the RFCs to the base package (#21701)
- update to MigrationTools 34

* Wed Jan 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- add support for additional OPTIONS, SLAPD_OPTIONS, and SLURPD_OPTIONS in
  a /etc/sysconfig/ldap file (#23549)

* Fri Dec 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- change automount object OID from 1.3.6.1.1.1.2.9 to 1.3.6.1.1.1.2.13,
  per mail from the ldap-nis mailing list

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- force -fPIC so that shared libraries don't fall over

* Mon Dec  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add Norbert Klasen's patch (via Del) to fix searches using ldaps URLs
  (OpenLDAP ITS #889)
- add "-h ldaps:///" to server init when TLS is enabled, in order to support
  ldaps in addition to the regular STARTTLS (suggested by Del)

* Mon Nov 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- correct mismatched-dn-cn bug in migrate_automount.pl

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to the correct OIDs for automount and automountInformation
- add notes on upgrading

* Tue Nov  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.7
- drop chdir patch (went mainstream)

* Thu Nov  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- change automount object classes from auxiliary to structural

* Tue Oct 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to Migration Tools 27
- change the sense of the last simple patch

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- reorganize the patch list to separate MigrationTools and OpenLDAP patches
- switch to Luke Howard's rfc822MailMember schema instead of the aliases.schema
- configure slapd to run as the non-root user "ldap" (#19370)
- chdir() before chroot() (we don't use chroot, though) (#19369)
- disable saving of the pid file because the parent thread which saves it and
  the child thread which listens have different pids

* Wed Oct 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add missing required attributes to conversion scripts to comply with schema
- add schema for mail aliases, autofs, and kerberosSecurityObject rooted in
  our own OID tree to define attributes and classes migration scripts expect
- tweak automounter migration script

* Mon Oct  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- try adding the suffix first when doing online migrations
- force ldapadd to use simple authentication in migration scripts
- add indexing of a few attributes to the default configuration
- add commented-out section on using TLS to default configuration

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.6
- add buildprereq on cyrus-sasl-devel, krb5-devel, openssl-devel
- take the -s flag off of slapadd invocations in migration tools
- add the cosine.schema to the default server config, needed by inetorgperson

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the nis.schema and inetorgperson.schema to the default server config
- make ldapadd a hard link to ldapmodify because they're identical binaries

* Fri Sep 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.4

* Fri Sep 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove prereq on /etc/init.d (#17531)
- update to 2.0.3
- add saucer to the included clients

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.1

* Fri Sep  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.0.0
- patch to build against MIT Kerberos 1.1 and later instead of 1.0.x

* Tue Aug 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove that pesky default password
- change "Copyright:" to "License:"

* Sun Aug 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- adjust permissions in files lists
- move libexecdir from %%{_prefix}/sbin to %%{_sbindir}

* Fri Aug 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add migrate_automount.pl to the migration scripts set

* Tue Aug  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- build a semistatic slurpd with threads, everything else without
- disable reverse lookups, per email on OpenLDAP mailing lists
- make sure the execute bits are set on the shared libraries

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- change logging facility used from local4 to daemon (#11047)

* Thu Jul 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- split off clients and servers to shrink down the package and remove the
  base package's dependency on Perl
- make certain that the binaries have sane permissions

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the init script back

* Thu Jul 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak the init script to only source /etc/sysconfig/network if it's found

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- switch to gdbm; I'm getting off the db merry-go-round
- tweak the init script some more
- add instdir to @INC in migration scripts

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak init script to return error codes properly
- change initscripts dependency to one on /etc/init.d

* Tue Jul  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- prereq initscripts
- make migration scripts use mktemp

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- do condrestart in post and stop in preun
- move init script to /etc/init.d

* Fri Jun 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.11
- add condrestart logic to init script
- munge migration scripts so that you don't have to be
  /usr/share/openldap/migration to run them
- add code to create pid files in /var/run

* Mon Jun  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS tweaks
- fix for compiling with libdb2

* Thu May  4 2000 Bill Nottingham <notting@redhat.com>
- minor tweak so it builds on ia64

* Wed May  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- more minimalistic fix for bug #11111 after consultation with OpenLDAP team
- backport replacement for the ldapuser patch

* Tue May  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix segfaults from queries with commas in them in in.xfingerd (bug #11111)

* Tue Apr 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.10
- add revamped version of patch from kos@bastard.net to allow execution as
  any non-root user
- remove test suite from %%build because of weirdness in the build system

* Wed Apr 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- move the defaults for databases and whatnot to /var/lib/ldap (bug #10714)
- fix some possible string-handling problems

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- start earlier, stop later.

* Thu Feb  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- auto rebuild in new environment (release 4)

* Tue Feb  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add -D_REENTRANT to make threaded stuff more stable, even though it looks
  like the sources define it, too
- mark *.ph files in migration tools as config files

* Fri Jan 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 1.2.9

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip files

* Sat Sep 11 1999 Bill Nottingham <notting@redhat.com>
- update to 1.2.7
- fix some bugs from bugzilla (#4885, #4887, #4888, #4967)
- take include files out of base package

* Fri Aug 27 1999 Jeff Johnson <jbj@redhat.com>
- missing ;; in init script reload) (#4734).

* Tue Aug 24 1999 Cristian Gafton <gafton@redhat.com>
- move stuff from /usr/libexec to /usr/sbin
- relocate config dirs to /etc/openldap

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Wed Aug 11 1999 Cristian Gafton <gafton@redhat.com>
- add the migration tools to the package

* Fri Aug 06 1999 Cristian Gafton <gafton@redhat.com>
- upgrade to 1.2.6
- add rc.d script
- split -devel package

* Sun Feb 07 1999 Preston Brown <pbrown@redhat.com>
- upgrade to latest stable (1.1.4), it now uses configure macro.

* Fri Jan 15 1999 Bill Nottingham <notting@redhat.com>
- build on arm, glibc2.1

* Wed Oct 28 1998 Preston Brown <pbrown@redhat.com>
- initial cut.
- patches for signal handling on the alpha
