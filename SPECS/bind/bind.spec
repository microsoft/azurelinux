%global        bind_dir          %{_var}/named
%global        chroot_prefix     %{bind_dir}/chroot
%global        chroot_create_directories /dev /run/named %{_localstatedir}/{log,named,tmp} \\\
                                         %{_sysconfdir}/crypto-policies/back-ends %{_sysconfdir}/pki/dnssec-keys %{_sysconfdir}/named \\\
                                         %{_libdir}/bind %{_libdir}/named %{_datadir}/GeoIP
## The order of libs is important. See lib/Makefile.in for details
%define bind_export_libs isc dns isccfg irs
%{!?_export_dir:%global _export_dir /bind9-export/}

Summary:        Domain Name System software
Name:           bind
Version:        9.20.11
Release:        1%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Tools
URL:            https://www.isc.org/downloads/bind/
Source0:        https://ftp.isc.org/isc/bind9/%{version}/%{name}-%{version}.tar.xz
Source1:        named.sysconfig
Source2:        named.logrotate
Source3:        named.root
Source4:        named.localhost
Source5:        named.loopback
Source6:        named.empty
Source7:        named.rfc1912.zones
Source8:        named.conf.sample
Source9:        named.root.key
Source11:       setup-named-chroot.sh
Source12:       generate-rndc-key.sh
Source13:       named.rwtab
Source14:       named-chroot.files
Source15:       https://gitlab.isc.org/isc-projects/dlz-modules/-/archive/main/dlz-modules-main.tar.gz

Patch0:         nongit-fix.patch
Patch1:         fix-maybe-uninitialized-warning-in-dlz_mysqldyn_mod.patch

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  json-c-devel
BuildRequires:  krb5-devel
BuildRequires:  libcap-devel
BuildRequires:  libtool
BuildRequires:  libuv-devel
BuildRequires:  lmdb-devel
BuildRequires:  make
BuildRequires:  mariadb-devel
BuildRequires:  nghttp2-devel
BuildRequires:  openldap-devel
BuildRequires:  openssl-devel
BuildRequires:  postgresql-devel
BuildRequires:  python3
BuildRequires:  python3-ply
BuildRequires:  sqlite-devel
BuildRequires:  systemd-libs
BuildRequires:  systemd-rpm-macros
BuildRequires:  userspace-rcu-devel

Requires:       %{name}-libs = %{version}-%{release}
Requires:       libuv
Requires:       openssl
Requires:       userspace-rcu
Requires(postun): %{_sbindir}/groupdel
Requires(postun): %{_sbindir}/userdel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
# Enforce fix for CVE-2019-6470
Conflicts:      dhcp < 4.4.1
# libisc-nosym requires to be linked with unresolved symbols
# When libisc-nosym linking is fixed, it can be defined to 1
# Visit https://bugzilla.redhat.com/show_bug.cgi?id=1540300
%undefine _strict_symbol_defs_build

%description
BIND is open source software that implements the Domain Name System (DNS) protocols
for the Internet. It is a reference implementation of those protocols, but it is
also production-grade software, suitable for use in high-volume and high-reliability applications.

%package dlz-filesystem
Summary:        BIND server filesystem DLZ module
Requires:       bind%{?_isa} = %{version}-%{release}

%description dlz-filesystem
Dynamic Loadable Zones filesystem module for BIND server.

%package dlz-ldap
Summary:        BIND server ldap DLZ module
Requires:       bind%{?_isa} = %{version}-%{release}

%description dlz-ldap
Dynamic Loadable Zones LDAP module for BIND server.

%package dlz-mysql
Summary:        BIND server mysql and mysqldyn DLZ modules
Requires:       bind%{?_isa} = %{version}-%{release}
Provides:       %{name}-dlz-mysqldyn = %{version}-%{release}

%description dlz-mysql
Dynamic Loadable Zones MySQL module for BIND server.
Contains also mysqldyn module with dynamic DNS updates (DDNS) support.

%package dlz-sqlite3
Summary:        BIND server sqlite3 DLZ module
Requires:       bind%{?_isa} = %{version}-%{release}

%description dlz-sqlite3
Dynamic Loadable Zones sqlite3 module for BIND server.

%package libs
Summary:        Libraries used by the BIND DNS packages
Requires:       bind-license = %{version}-%{release}
Provides:       bind-libs-lite = %{version}-%{release}
Obsoletes:      bind-libs-lite < 9.16.13

%description libs
Contains heavyweight version of BIND suite libraries used by both named DNS
server and utilities in bind-utils package.

%package license
Summary:        License of the BIND DNS suite
BuildArch:      noarch

%description license
Contains license of the BIND DNS suite.

%package devel
Summary:        Header files and libraries needed for bind-dyndb-ldap
Requires:       bind-libs%{?_isa} = %{version}-%{release}
Requires:       json-c-devel%{?_isa}
Requires:       krb5-devel%{?_isa}
Requires:       libcap-devel%{?_isa}
Requires:       libxml2-devel%{?_isa}
Requires:       lmdb-devel%{?_isa}
Requires:       openssl-devel%{?_isa}
Provides:       bind-lite-devel = %{version}-%{release}
Obsoletes:      bind-lite-devel < 9.16.6-3

%description devel
The bind-devel package contains full version of the header files and libraries
required for building bind-dyndb-ldap. Upstream no longer supports nor recommends
bind libraries for third party applications.

%package chroot
Summary:        A chroot runtime environment for the ISC BIND DNS server, named(8)
Requires:       bind%{?_isa} = %{version}-%{release}
# grep is required due to setup-named-chroot.sh script
Requires:       grep

%description chroot
This package contains a tree of files which can be used as a
chroot(2) jail for the named(8) program from the BIND package.
Based on the code from Jan "Yenya" Kasprzak <kas@fi.muni.cz>

%package dnssec-utils
Summary:        DNSSEC keys and zones management utilities
Requires:       bind-dnssec-doc = %{version}-%{release}
Requires:       bind-libs%{?_isa} = %{version}-%{release}
Requires:       python3-bind = %{version}-%{release}
Recommends:     bind-utils

%description dnssec-utils
Bind-dnssec-utils contains a collection of utilities for editing
DNSSEC keys and BIND zone files. These tools provide generation,
revocation and verification of keys and DNSSEC signatures in zone files.

You should install bind-dnssec-utils if you need to sign a DNS zone
or maintain keys for it.

%package dnssec-doc
Summary:        Manual pages of DNSSEC utilities
Requires:       bind-license = %{version}-%{release}
BuildArch:      noarch

%description dnssec-doc
Bind-dnssec-doc contains manual pages for bind-dnssec-utils.

%package -n python3-bind
Summary:        A module allowing rndc commands to be sent from Python programs
Requires:       bind-license = %{version}-%{release}
Requires:       python3
Requires:       python3-ply
BuildArch:      noarch

%description -n python3-bind
This package provides a module which allows commands to be sent to rndc directly from Python programs.

%package utils
Summary:        BIND utilities

%description utils
%{summary}.

%prep
%setup -q

# DLZ modules do not support oot builds. Copy files into build
mkdir -p build/contrib/dlz
pushd build/contrib/dlz
tar --no-same-owner -xf %{SOURCE15}
mv dlz-modules-main/modules ./
popd

%autopatch -p1

# Copying auxiliary files with libtoolize. Some files will be replaced by libtoolize -c -f.
# The files "compile", "depcomp", and "missing" will be deleted by this process, as some
# temporary files have the same name. The "compile" file is necessary for "configure",
# so we need to save a backup of these files.
mkdir backup
mv compile depcomp missing backup/
libtoolize -c -f; %{_bindir}/aclocal -I m4 --force; %{_bindir}/autoconf -f
mv backup/* .
rmdir backup

%build
./configure \
    --prefix=%{_prefix} \
    --localstatedir=%{_var} \
    --disable-static \
    --includedir=%{_includedir}/bind9 \
    --with-lmdb=yes \
    --with-json-c \
    --enable-fixed-rrset \
    --with-docbook-xsl=%{_datadir}/sgml/docbook/xsl-ns-stylesheets \
    --enable-full-report \

%make_build

pushd build/contrib/dlz/modules
for DIR in filesystem ldap mysql mysqldyn sqlite3; do
  make -C $DIR CFLAGS="-fPIC -I../include $CFLAGS $LDFLAGS"
done
popd

%install
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_libdir}/{bind,named}
mkdir -p %{buildroot}%{_localstatedir}/named/{slaves,data,dynamic}
mkdir -p %{buildroot}%{_mandir}/{man1,man5,man8}
mkdir -p %{buildroot}/run/named

#chroot
for D in %{chroot_create_directories}
do
  mkdir -p %{buildroot}/%{chroot_prefix}${D}
done

# create symlink as it is on real filesystem
pushd %{buildroot}/%{chroot_prefix}%{_var}
ln -s ../run run
popd

# these are required to prevent them being erased during upgrade of previous
touch %{buildroot}/%{chroot_prefix}%{_sysconfdir}/named.conf
#end chroot

%make_install

mkdir -p  %{buildroot}%{_libexecdir}
install -m 755 %{SOURCE11} %{buildroot}%{_libexecdir}/setup-named-chroot.sh
install -m 755 %{SOURCE12} %{buildroot}%{_libexecdir}/generate-rndc-key.sh

install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/named
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/named
install -m 644 %{SOURCE14} %{buildroot}%{_sysconfdir}/named-chroot.files

# Install isc/errno2result.h header
install -m 644 lib/isc/errno2result.h %{buildroot}%{_includedir}/bind9/isc

# Files required to run test-suite outside of build tree:
cp -fp config.h %{buildroot}%{_includedir}/bind9

# Remove libtool .la files:
find %{buildroot} -type f -name "*.la" -delete -print

# configuration files:
touch %{buildroot}%{_sysconfdir}/rndc.{key,conf}
install -m 644 %{SOURCE9} %{buildroot}%{_sysconfdir}/named.root.key
mkdir -p %{buildroot}%{_sysconfdir}/named

# data files:
mkdir -p %{buildroot}%{_localstatedir}/named
install -m 640 %{SOURCE3} %{buildroot}%{_localstatedir}/named/named.ca
install -m 640 %{SOURCE4} %{buildroot}%{_localstatedir}/named/named.localhost
install -m 640 %{SOURCE5} %{buildroot}%{_localstatedir}/named/named.loopback
install -m 640 %{SOURCE6} %{buildroot}%{_localstatedir}/named/named.empty
install -m 640 %{SOURCE7} %{buildroot}%{_sysconfdir}/named.rfc1912.zones

mkdir -p %{buildroot}/%{_tmpfilesdir}
cat << EOF >> %{buildroot}/%{_sysconfdir}/named.conf
zone "." in {
    type master;
    allow-update {none;}; // no DDNS by default
};
EOF
echo "d /run/named 0755 named named - -" > %{buildroot}/%{_tmpfilesdir}/named.conf

# sample bind configuration files for %%doc:
mkdir -p sample/etc sample/var/named/{data,slaves}
install -m 644 %{SOURCE8} sample/etc/named.conf
# Copy default configuration to %%doc to make it usable from system-config-bind
cp %{buildroot}/%{_tmpfilesdir}/named.conf named.conf.default
install -m 644 %{SOURCE7} sample/etc/named.rfc1912.zones
install -m 644 %{SOURCE4} %{SOURCE5} %{SOURCE6}  sample/var/named
install -m 644 %{SOURCE3} sample/var/named/named.ca
for f in my.internal.zone.db slaves/my.slave.internal.zone.db slaves/my.ddns.internal.zone.db my.external.zone.db; do
  echo '@ in soa localhost. root 1 3H 15M 1W 1D
  ns localhost.' > sample/var/named/$f;
done
:;

mkdir -p %{buildroot}%{_sysconfdir}/rwtab.d
install -m 644 %{SOURCE13} %{buildroot}%{_sysconfdir}/rwtab.d/named

pushd build/contrib/dlz/modules
for DIR in filesystem ldap mysql mysqldyn sqlite3; do
  %make_install -C $DIR libdir=%{_libdir}/named
done
pushd %{buildroot}%{_libdir}/bind
  cp -s ../named/dlz_*.so .
popd
mkdir -p doc/{mysql,mysqldyn}
cp -p mysqldyn/testing/README doc/mysqldyn/README.testing
cp -p mysqldyn/testing/* doc/mysqldyn
cp -p mysql/testing/* doc/mysql
popd

# Remove unwanted files
rm -f %{buildroot}%{_prefix}%{_sysconfdir}/bind.keys

%pre
if [ $1 -eq 1 ]; then
  if ! getent group named >/dev/null; then
      groupadd -r named
  fi
  if ! getent passwd named >/dev/null; then
      useradd -g named -d %{_sharedstatedir}/bind\
          -s /bin/false -M -r named
  fi
fi

%post -p /sbin/ldconfig
%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
  if getent passwd named >/dev/null; then
      userdel named
  fi
  if getent group named >/dev/null; then
      groupdel named
  fi
fi

# Fix permissions on existing device files on upgrade
%define chroot_fix_devices() \
if [ $1 -gt 1 ]; then \
  for DEV in "%{1}/dev"/{null,random,zero}; do \
    if [ -e "$DEV" -a "$(/bin/stat --printf="%{G} %{a}" "$DEV")" = "root 644" ]; \
    then \
      /bin/chmod 0664 "$DEV" \
      /bin/chgrp named "$DEV" \
    fi \
  done \
fi

%ldconfig_scriptlets libs

%post chroot
%chroot_fix_devices %{chroot_prefix}

%posttrans chroot
if [ -x %{_sbindir}/selinuxenabled ] && %{_sbindir}/selinuxenabled; then
  [ -x /sbin/restorecon ] && /sbin/restorecon %{chroot_prefix}/dev/* > /dev/null 2>&1;
fi;

%files
%dir %{_libdir}/bind
%{_libdir}/bind/filter-a.so
%{_libdir}/bind/filter-aaaa.so
%dir %{_libdir}/named
%{_libdir}/named/*.so
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/named
%config(noreplace) %attr(0644,root,named) %{_sysconfdir}/named.root.key
%config(noreplace) %{_sysconfdir}/logrotate.d/named
%{_sysconfdir}/rwtab.d/named
%{_tmpfilesdir}/named.conf
%{_bindir}/named-journalprint
%{_bindir}/named-checkconf
%{_bindir}/named-rrchecker
%{_bindir}/mdig
%{_sbindir}/named

%{_sbindir}/rndc*
%{_libexecdir}/generate-rndc-key.sh
%{_mandir}/man1/mdig.1*
%{_mandir}/man1/named-rrchecker.1*
%{_mandir}/man5/named.conf.5*
%{_mandir}/man5/rndc.conf.5*
%{_mandir}/man8/rndc.8*
%{_mandir}/man8/named.8*
%{_mandir}/man1/named-checkconf.1*
%{_mandir}/man8/rndc-confgen.8*
%{_mandir}/man1/named-journalprint.1*
%{_mandir}/man8/filter-aaaa.8.gz
%{_mandir}/man8/filter-a.8.gz
%doc README.md named.conf.default
%doc sample/

%defattr(0660,root,named,01770)
%dir %{_localstatedir}/named
%defattr(0660,named,named,0770)
%dir %{_localstatedir}/named/slaves
%dir %{_localstatedir}/named/data
%dir %{_localstatedir}/named/dynamic
%ghost %{_localstatedir}/log/named.log
%defattr(0640,root,named,0750)
%config %verify(not link) %{_localstatedir}/named/named.ca
%config %verify(not link) %{_localstatedir}/named/named.localhost
%config %verify(not link) %{_localstatedir}/named/named.loopback
%config %verify(not link) %{_localstatedir}/named/named.empty
%ghost %config(noreplace) %{_sysconfdir}/rndc.key
# ^- rndc.key now created on first install only if it does not exist
%ghost %config(noreplace) %{_sysconfdir}/rndc.conf
# ^- The default rndc.conf which uses rndc.key is in named's default internal config -
# so rndc.conf is not necessary.
%dir /run/named
%config(noreplace) %verify(not link) %{_sysconfdir}/named.conf
%config(noreplace) %verify(not link) %{_sysconfdir}/named.rfc1912.zones

%files dlz-filesystem
%{_libdir}/{named,bind}/dlz_filesystem_dynamic.so

%files dlz-mysql
%{_libdir}/{named,bind}/dlz_mysql_dynamic.so
%doc build/contrib/dlz/modules/doc/mysql
%{_libdir}/{named,bind}/dlz_mysqldyn_mod.so
%doc build/contrib/dlz/modules/doc/mysqldyn

%files dlz-ldap
%{_libdir}/{named,bind}/dlz_ldap_dynamic.so
%doc build/contrib/dlz/modules/ldap/testing/*

%files dlz-sqlite3
%{_libdir}/{named,bind}/dlz_sqlite3_dynamic.so
%doc build/contrib/dlz/modules/sqlite3/testing/*

%files libs
%{_libdir}/libdns*.so
%{_libdir}/libisc*.so
%{_libdir}/libns*.so

%files license
%license LICENSE
%license COPYRIGHT

%files devel
%dir %{_includedir}/bind9
%{_includedir}/bind9/config.h
%{_includedir}/bind9/isccc
%{_includedir}/bind9/ns
%{_includedir}/bind9/dns
%{_includedir}/bind9/dst
%{_includedir}/bind9/irs
%{_includedir}/bind9/isc
%{_includedir}/bind9/isccfg

%files dnssec-utils
%{_bindir}/dnssec*

%files dnssec-doc
%{_mandir}/man1/dnssec*.1*

%files -n python3-bind
%exclude %{python3_sitelib}/python3-ply-*.noarch

%files chroot
%config(noreplace) %{_sysconfdir}/named-chroot.files
%{_libexecdir}/setup-named-chroot.sh
%defattr(0664,root,named,-)
%ghost %dev(c,1,3) %verify(not mtime) %{chroot_prefix}/dev/null
%ghost %dev(c,1,8) %verify(not mtime) %{chroot_prefix}/dev/random
%ghost %dev(c,1,9) %verify(not mtime) %{chroot_prefix}/dev/urandom
%ghost %dev(c,1,5) %verify(not mtime) %{chroot_prefix}/dev/zero
%defattr(0640,root,named,0750)
%dir %{chroot_prefix}
%dir %{chroot_prefix}/dev
%dir %{chroot_prefix}%{_sysconfdir}
%dir %{chroot_prefix}%{_sysconfdir}/named
%dir %{chroot_prefix}%{_sysconfdir}/pki
%dir %{chroot_prefix}%{_sysconfdir}/pki/dnssec-keys
%dir %{chroot_prefix}%{_sysconfdir}/crypto-policies
%dir %{chroot_prefix}%{_sysconfdir}/crypto-policies/back-ends
%dir %{chroot_prefix}%{_localstatedir}
%dir %{chroot_prefix}/run
%ghost %config(noreplace) %{chroot_prefix}%{_sysconfdir}/named.conf
%defattr(-,root,root,-)
%dir %{chroot_prefix}%{_prefix}
%dir %{chroot_prefix}/%{_libdir}
%dir %{chroot_prefix}/%{_libdir}/bind
%dir %{chroot_prefix}/%{_datadir}/GeoIP
%defattr(0660,root,named,01770)
%dir %{chroot_prefix}%{_localstatedir}/named
%defattr(0660,named,named,0770)
%dir %{chroot_prefix}%{_localstatedir}/tmp
%dir %{chroot_prefix}%{_localstatedir}/log
%defattr(-,named,named,-)
%dir %{chroot_prefix}/run/named
%{chroot_prefix}%{_localstatedir}/run

%files utils
%defattr(-,root,root)
%{_bindir}/dig
%{_bindir}/delv
%{_bindir}/host
%{_bindir}/nslookup
%{_bindir}/nsupdate
%{_bindir}/arpaname
%{_sbindir}/ddns-confgen
%{_sbindir}/tsig-keygen
%{_bindir}/nsec3hash
%{_bindir}/named-checkzone
%{_bindir}/named-compilezone
%{_bindir}/named-nzd2nzf
%{_mandir}/man1/host.1*
%{_mandir}/man1/nsupdate.1*
%{_mandir}/man1/dig.1*
%{_mandir}/man1/delv.1*
%{_mandir}/man1/nslookup.1*
%{_mandir}/man1/arpaname.1*
%{_mandir}/man8/ddns-confgen.8*
%{_mandir}/man8/tsig-keygen.8*
%{_mandir}/man1/nsec3hash.1*
%{_mandir}/man1/named-checkzone.1*
%{_mandir}/man1/named-compilezone.1*
%{_mandir}/man1/named-nzd2nzf.1*

%changelog
* Fri Jul 18 2025 Kevin Lockwood <v-klockwood@microsoft.com> - 9.20.11-1
- Upgrade to 9.20.11 - for CVE-2025-40777

* Mon May 26 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.20.9-1
- Auto-upgrade to 9.20.9 - for CVE-2025-40775

* Mon Mar 03 2025 Andrew Phelps <anphel@microsoft.com> - 9.20.5-4
- Remove duplicate shared object files in base and devel packages
- Remove duplicate files from utils package
- Add requires for bind-libs from base package

* Thu Feb 27 2025 Tobias Brick <tobiasb@microsoft.com> - 9.20.5-3
- Fix uninitialized memory warning.

* Tue Feb 25 2025 Tobias Brick <tobiasb@microsoft.com> - 9.20.5-2
- Fix warning during package uninstall.

* Tue Feb 04 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.20.5-1
- Auto-upgrade to 9.20.5 - to fix CVE-2024-12705 & CVE-2024-11187
- Refresh nongit-fix patch to apply cleanly.

* Wed Jul 24 2024 Muhammad Falak <mwani@microsoft.com> - 9.20.0-1
- Upgrade version to 9.20.0 to address CVE-CVE-2024-0760, CVE-2024-1737, CVE-2024-1975 & CVE-2024-4076
- Refresh patches to apply cleanly

* Tue Feb 20 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.19.21-1
- Auto-upgrade to 9.19.21 - Mariner 3.0 package upgrade
- Update the locations of files in the new build
- Remove configure flags that no longer exist
- Add patch to avoid error when not downloading bind source from git
- Add backup of compile file to avoid deleting it by mistake
- Remove libbind9 and libirs as they are part of the removed features in 9.19
- Remove PKCS-11 subpackages as starting from BIND 9.18, native PKCS#11 support has been removed 
- Update subpackages dependencies

* Thu Dec 14 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 9.16.44-2
- Fix resetting of passwd and group on package update

* Wed Sep 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.16.44-1
- Auto-upgrade to 9.16.44 - Fix CVE-2023-3341

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 9.16.37-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Sep 07 2023 Betty Lakes <bettylakes@microsoft.com> - 9.16.37-1
- Bump the version to 9.16.37 to fix CVE-2022-3924, CVE-2022-3094, CVE-2022-3736

* Wed Jul 26 2023 Suresh Thelkar <sthelkar@microsoft.com> - 9.16.33-2
- Patch to fix CVE-2023-2828

* Mon Nov 14 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 9.16.33-1
- Auto-upgrade to 9.16.33 - CVE-2022-2795,CVE-2022-3080

* Mon Sep 12 2022 Olivia Crain <oliviacrain@microsoft.com - 9.16.29-2
- Move named tmpfiles configuration to base package from utils subpackage
- Move files under %%{_sysconfdir} in utils subpackage to base package 

* Wed Jun 08 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.16.29-1
- Updating to 9.16.29 to fix CVE-2021-25219.

* Mon Apr 04 2022 Henry Li <lihl@microsoft.com> - 9.16.15-4
- Remove trusted-key.key which works with +sigchase, a deprecated feature
- License Verified

* Sat Oct 02 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.16.15-3
- Adding missing BR on 'systemd-rpm-macros'.

* Fri Aug 27 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 9.16.15-2
- Adding DBZ subpackages using Fedora 34 (license: MIT) specs as guidance.

* Tue Jul 27 2021 Jon Slobodzian <joslobo@microsoft.com> - 9.16.15-1
- Update version to 9.16.15 to fix CVE-2021-25215
- Remove unprovided soname version of libraries
- Include versioned library names in libs subpackage

* Fri May 14 2021 Thomas Crain <thcrain@microsoft.com> - 9.16.3-5
- Merge the following releases from 1.0 to dev branch
- nicolasg@microsoft.com, 9.16.3-3: Fixes CVE-2020-8625

* Thu May 13 2021 Henry Li <lihl@microsoft.com> - 9.16.3-4
- Fix file path error caused by linting
- Remove duplicate %files section for bind-license
- Remove named.conf from main package, which is already provided by bind-utils

* Mon May 03 2021 Henry Li <lihl@microsoft.com> - 9.16.3-3
- Add bind, bind-devel, bind-libs, bind-license, bind-pkcs11, bind-pkcs11-libs,
  bind-pkcs11-utils, bind-pkcs11-devel, bind-dnssec-utils, bind-dnssec-doc,
  bind-python3-bind and bind-chroot packages

*   Mon Mar 01 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 9.16.3-3
-   Fixes CVE-2020-8625

*   Fri Sep 11 2020 Ruying Chen <v-ruyche@microsoft.com> - 9.16.3-2
-   Fixes CVE-2020-8618, CVE-2020-8619, CVE-2020-8620,
-   CVE-2020-8621, CVE-2020-8622, CVE-2020-8623, CVE-2020-8624

*   Wed May 27 2020 Daniel McIlvaney <damcilva@microsoft.com> - 9.16.3-1
-   Update to version 9.16.3, fixes CVE-2018-5743, CVE-2018-5744, CVE-2019-6465, CVE-2019-6467, CVE-2019-6471, CVE-2020-8616, CVE-2020-8617

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 9.13.3-4
-   Added %%license line automatically

*   Fri May  1 2020 Emre Girgin <mrgirgin@microsoft.com> 9.13.3-3
-   Renaming bindutils to bind.
-   Add bind-utils subpackage.

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 9.13.3-2
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Sun Sep 23 2018 Sujay G <gsujay@vmware.com> 9.13.3-1
-   Bump bindutils version to 9.13.3

*   Mon Feb 12 2018 Xiaolin Li <xiaolinl@vmware.com> 9.10.6-1
-   Upgrading version to 9.10.6-P1, fix CVE-2017-3145

*   Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 9.10.4-4
-   Remove shadow from requires and use explicit tools for post actions

*   Fri Apr 14 2017 Kumar Kaushik <kaushikk@vmware.com> 9.10.4-3
-   Upgrading version to 9.10.4-P8

*   Mon Nov 21 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.4-2
-   add shadow to requires

*   Mon Jun 06 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 9.10.4-1
-   Upgraded the version to 9.10.4

*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 9.10.3-3
-   GA - Bump release of all rpms

*   Fri Apr 29 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-2
-   Add group named and user named

*   Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 9.10.3-1
-   Updated to version 9.10.3

*   Tue Aug 11 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-1
-   Fixing release

*   Tue Jan 20 2015 Divya Thaluru <dthaluru@vmware.com> 9.10.1-P1
-   Initial build. First version
