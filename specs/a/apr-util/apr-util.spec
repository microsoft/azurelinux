# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%define aprver 1

%if 0%{?fedora} < 39 && 0%{?rhel} <= 9
%global with_lmdb 0
%else
%global with_lmdb 1
%endif

%if %{with_lmdb}
%define dbdep lmdb-devel
%else
%if 0%{?fedora} < 18 && 0%{?rhel} < 7
%define dbdep db4-devel
%else
%define dbdep libdb-devel
%endif
%endif

%if 0%{?fedora} < 27 && 0%{?rhel} <= 7
%global with_nss 1
%else
%global with_nss 0
%endif

%if 0%{?fedora} < 36 && 0%{?rhel} <= 9
%global ldaplib ldap_r
%else
%global ldaplib ldap
%endif

# Disable .la file removal since the .la file is exported via apu-config.
%global __brp_remove_la_files %nil

%define apuver 1

Summary: Apache Portable Runtime Utility library
Name: apr-util
Version: 1.6.3
Release: 25%{?dist}
# Apache-2.0:  everything
# RSA-MD:      https://gitlab.com/fedora/legal/fedora-legal-docs/-/merge_requests/187
#              include\apr_md5.h, passwd\apr_md5.c, crypto\apr_md4.c, include\apr_md4.h
#
# LicenseRef-Fedora-Public-Domain: crypto\crypt_blowfish.c, crypto\crypt_blowfish.h
# Beerware:                        passwd\apr_md5.c
# OLDAP-2.7 AND BSD-4.3RENO:       ldap/apr_ldap_url.c
License: Apache-2.0 AND (Beerware AND LicenseRef-Fedora-Public-Domain AND OLDAP-2.7 AND BSD-4.3RENO)
URL: https://apr.apache.org/
Source0: https://www.apache.org/dist/apr/%{name}-%{version}.tar.bz2
Patch1: apr-util-1.2.7-pkgconf.patch
Patch2: apr-util-1.4.1-private.patch
Patch3: apr-util-1.6.3-allow-ipv6.patch
Patch4: apr-util-configure-c99.patch
Patch5: apr-util-1.6.3-lmdb-support.patch
Patch6: apr-util-1.6.3-r1908586.patch
Patch7: apr-util-1.6.3-r1908584.patch
Patch8: apr-util-1.6.3-r1908585.patch
Patch9: apr-util-1.6.3-drop-engine-headers.patch
Patch10: apr-util-1.6.3-r1928729.patch
BuildRequires: gcc
BuildRequires: autoconf, apr-devel >= 1.3.0
BuildRequires: %{dbdep}, expat-devel, libuuid-devel
BuildRequires: libxcrypt-devel
Recommends: apr-util-openssl%{_isa} = %{version}-%{release}
%if %{with_lmdb}
Recommends: apr-util-lmdb%{_isa} = %{version}-%{release}
%else
%if 0%{?fedora} < 27
Requires: apr-util-bdb%{?_isa} = %{version}-%{release}
%else
Recommends: apr-util-bdb%{_isa} = %{version}-%{release}
%endif
%endif

%description
The mission of the Apache Portable Runtime (APR) is to provide a
free library of C data structures and routines.  This library
contains additional utility interfaces for APR; including support
for XML, LDAP, database interfaces, URI parsing and more.

%package devel
Summary: APR utility library development kit
Requires: apr-util%{?_isa} = %{version}-%{release}, apr-devel%{?_isa}, pkgconfig
Requires: expat-devel%{?_isa}, openldap-devel%{?_isa}

%description devel
This package provides the support files which can be used to 
build applications using the APR utility library.  The mission 
of the Apache Portable Runtime (APR) is to provide a free 
library of C data structures and routines.

%package pgsql
Summary: APR utility library PostgreSQL DBD driver
BuildRequires: libpq-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description pgsql
This package provides the PostgreSQL driver for the apr-util
DBD (database abstraction) interface.

%if %{with_lmdb}
%package lmdb
Summary: APR utility library LMDB driver
Requires: apr-util%{?_isa} = %{version}-%{release}
# Remove libdb dependency from apr-util
# https://bugzilla.redhat.com/show_bug.cgi?id=1779267
Obsoletes: apr-util-bdb < 1.6.3-13
Provides: apr-util-%{aprver}(dbm)%{?_isa} = %{version}-%{release}

%description lmdb
This package provides the LMDB driver for the apr-util
DBM (database abstraction) interface.
%else
%package bdb
Summary: APR utility library Berkeley DB driver
Requires: apr-util%{?_isa} = %{version}-%{release}
Provides: apr-util-%{aprver}(dbm)%{?_isa} = %{version}-%{release}

%description bdb
This package provides the Berkeley DB driver for the apr-util
DBM (database abstraction) interface.
%endif

%package mysql
Summary: APR utility library MySQL DBD driver
BuildRequires: mariadb-connector-c-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description mysql
This package provides the MySQL driver for the apr-util DBD
(database abstraction) interface.

%package sqlite
Summary: APR utility library SQLite DBD driver
BuildRequires: sqlite-devel >= 3.0.0
Requires: apr-util%{?_isa} = %{version}-%{release}

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.

%package odbc
Summary: APR utility library ODBC DBD driver
BuildRequires: unixODBC-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description odbc
This package provides the ODBC driver for the apr-util DBD
(database abstraction) interface.

%package ldap
Summary: APR utility library LDAP support
BuildRequires: openldap-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description ldap
This package provides the LDAP support for the apr-util.

%package openssl
Summary: APR utility library OpenSSL crypto support
BuildRequires: openssl-devel
Requires: apr-util%{?_isa} = %{version}-%{release}

%description openssl
This package provides the OpenSSL crypto support for the apr-util.

%if %{with_nss}
%package nss
Summary: APR utility library NSS crypto support
BuildRequires: nss-devel
BuildRequires: make
Requires: apr-util%{?_isa} = %{version}-%{release}

%description nss
This package provides the NSS crypto support for the apr-util.
%endif

%prep
%autosetup -p1

: Configured for LDAP library: %{ldaplib}
: Configured for DBM library: %{dbdep}

%build
autoheader && autoconf
# A fragile autoconf test which fails if the code trips
# any other warning; force correct result for OpenLDAP:
export ac_cv_ldap_set_rebind_proc_style=three
%configure --with-apr=%{_prefix} \
        --includedir=%{_includedir}/apr-%{apuver} \
        --with-ldap=%{ldaplib} --without-gdbm \
        --with-sqlite3 --with-pgsql --with-mysql --with-odbc \
%if %{with_lmdb}
        --with-dbm=lmdb --with-lmdb \
%else
        --with-dbm=db5 --with-berkeley-db \
%endif
        --without-sqlite2 \
        --with-crypto --with-openssl \
%if %{with_nss}
        --with-nss \
%else
        --without-nss \
%endif
   || { cat config.log; exit 1; }
%{make_build}

%install
rm -rf $RPM_BUILD_ROOT
%{make_install}

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/aclocal
install -m 644 build/find_apu.m4 $RPM_BUILD_ROOT/%{_datadir}/aclocal

# Unpackaged files; remove the static libaprutil
rm -f $RPM_BUILD_ROOT%{_libdir}/aprutil.exp \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.a

# And remove the reference to the static libaprutil from the .la
# file.
sed -i '/^old_library/s,libapr.*\.a,,' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la

# Remove unnecessary exports from dependency_libs
sed -ri '/^dependency_libs/{s,-l(pq|sqlite[0-9]|rt|dl|uuid) ,,g}' \
      $RPM_BUILD_ROOT%{_libdir}/libapr*.la

# Trim libtool DSO cruft
rm -f $RPM_BUILD_ROOT%{_libdir}/apr-util-%{apuver}/*.*a

%check
# Run the less verbose test suites
export MALLOC_CHECK_=2 MALLOC_PERTURB_=$(($RANDOM % 255 + 1))
cd test
%{make_build} testall
# testall breaks with DBD DSO; ignore
export LD_LIBRARY_PATH=%{buildroot}/%{_libdir}/apr-util-%{apuver}
./testall -v -q

%ldconfig_scriptlets

%files
%doc CHANGES LICENSE NOTICE
%{_libdir}/libaprutil-%{apuver}.so.*
%dir %{_libdir}/apr-util-%{apuver}

%if %{with_lmdb}
%files lmdb
%{_libdir}/apr-util-%{apuver}/apr_dbm_lmdb*
%else
%files bdb
%{_libdir}/apr-util-%{apuver}/apr_dbm_db*
%endif

%files pgsql
%{_libdir}/apr-util-%{apuver}/apr_dbd_pgsql*

%files mysql
%{_libdir}/apr-util-%{apuver}/apr_dbd_mysql*

%files sqlite
%{_libdir}/apr-util-%{apuver}/apr_dbd_sqlite*

%files odbc
%{_libdir}/apr-util-%{apuver}/apr_dbd_odbc*

%files ldap
%{_libdir}/apr-util-%{apuver}/apr_ldap*

%files openssl
%{_libdir}/apr-util-%{apuver}/apr_crypto_openssl*

%if %{with_nss}
%files nss
%{_libdir}/apr-util-%{apuver}/apr_crypto_nss*
%endif

%files devel
%{_bindir}/apu-%{apuver}-config
%{_libdir}/libaprutil-%{apuver}.la
%{_libdir}/libaprutil-%{apuver}.so
%{_includedir}/apr-%{apuver}/*.h
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4

%changelog
* Thu Sep 25 2025 Luboš Uhliarik <luhliari@redhat.com> - 1.6.3-25
- apr_dbm lmdb: fix database access issues

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 1.6.3-23
- Add explicit BR: libxcrypt-devel

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug  6 2024 Joe Orton <jorton@redhat.com> - 1.6.3-21
- restore required openldap-devel dep from -devel (#2302876)

* Mon Jul 29 2024 Luboš Uhliarik <luhliari@redhat.com> - 1.6.3-20
- drop ENGINE support from apr_crypto
- fix (harmless) gcc snprintf warning in testbuckets.c

* Wed Jul 24 2024 Joe Orton <jorton@redhat.com> - 1.6.3-19
- drop unnecessary -devel deps on lmdb-devel, openldap-devel

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Joe Orton <jorton@redhat.com> - 1.6.3-17
- apr_dbm lmdb: disable locking by default

* Thu Feb  8 2024 Joe Orton <jorton@redhat.com> - 1.6.3-16
- fix ODBC type mismatch (r1908586)
- use autosetup

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Joe Orton <jorton@redhat.com> - 1.6.3-13
- re-enable LMDB by default again for Fedora >= 40 (#1779267)

* Thu Nov  2 2023 Joe Orton <jorton@redhat.com> - 1.6.3-12
- add apr-util-1(dbm) as virtual provide for dbm drivers
- disable LMDB for now

* Fri Oct 27 2023 Joe Orton <jorton@redhat.com> - 1.6.3-11
- remove Provides: for -bdb

* Tue Oct 24 2023 Luboš Uhliarik <luhliari@redhat.com> - 1.6.3-10
- add LMDB support and use it on Fedora >= 40
- Resolves: #1779267 - Remove libdb dependency from apr-util

* Tue Oct 03 2023 Luboš Uhliarik <luhliari@redhat.com> - 1.6.3-7
- SPDX migration

* Wed Aug 30 2023 Florian Weimer <fweimer@redhat.com> - 1.6.3-5
- Restore configure script port to C99

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 23 2023 Luboš Uhliarik <luhliari@redhat.com> - 1.6.3-3
- regression in IPv4 handling in r1907242. Cycle through the address list
  handling v4/v6 addresses correctly

* Fri Feb 10 2023 Luboš Uhliarik <luhliari@redhat.com> - 1.6.3-2
- memcache/apr_memcache.c (conn_connect): Allow use of IPv6

* Thu Feb 02 2023 Luboš Uhliarik <luhliari@redhat.com> - 1.6.3-1
- new version 1.6.3

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 22 2022 Florian Weimer <fweimer@redhat.com> - 1.6.1-23
- Port configure script to C99

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 13 2022 Joe Orton <jorton@redhat.com> - 1.6.1-21
- disable .la file removal

* Fri Jan 28 2022 Joe Orton <jorton@redhat.com> - 1.6.1-20
- fix build with OpenLDAP 2.6 (#2032706)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.6.1-18
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 1.6.1-16
- rebuild for libpq ABI fix rhbz#1908268

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Tom Stellard <tstellar@redhat.com> - 1.6.1-13
- Use make_build and make_install macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.6.1-9
- Rebuilt for libcrypt.so.2 (#1666033)

* Wed Sep 26 2018 Joe Orton <jorton@redhat.com> - 1.6.1-8
- Recommends: -openssl and -bdb so default crypto, dbm drivers are
  always available (#1491151, #1633152)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar  9 2018 Bojan Smojver <bojan@rexursive.com> - 1.6.1-6
- add gcc build requirement

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Florian Weimer <fweimer@redhat.com> - 1.6.1-4
- Rebuild with new build flags embedded in apr

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.6.1-3
- Rebuilt for switch to libxcrypt

* Tue Dec 19 2017 Honza Horak <hhorak@redhat.com> - 1.6.1-2
- Build with mariadb-connector-c

* Wed Oct 25 2017 Luboš Uhliarik <luhliari@redhat.com> - 1.6.1-1
- new version 1.6.1

* Mon Aug 21 2017 Joe Orton <jorton@redhat.com> - 1.6.0-1
- update to 1.6.0 (#1460831)
- move bdb support to loadable DSO in apr-util-dbd subpackage
- drop NSS, freetds support

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Nov 14 2016 Joe Orton <jorton@redhat.com> - 1.5.4-4
- update for OpenSSL 1.1.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 22 2014 Jan Kaluza <jkaluza@redhat.com> - 1.5.4-1
- update to 1.5.4

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 26 2013 Joe Orton <jorton@redhat.com> - 1.5.3-1
- update to 1.5.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 09 2013 Jan Kaluza <jkaluza@redhat.com> - 1.5.2-3
- do not build with freetds when it is not available

* Tue Apr  9 2013 Joe Orton <jorton@redhat.com> - 1.5.2-2
- update for aarch64

* Tue Apr  9 2013 Joe Orton <jorton@redhat.com> - 1.5.2-1
- update to 1.5.2

* Thu Feb 07 2013 Jon Ciesla <limburgher@gmail.com> - 1.4.1-8
- Apply private patch from Merge Review BZ 225254.

* Wed Nov 07 2012 Jan Kaluza <jkaluza@redhat.com> - 1.4.1-7
- ensure we use latest libdb5 (not libdb4)

* Thu Oct 18 2012 Joe Orton <jorton@redhat.com> - 1.4.1-6
- use -lldap_r instead of -lldap

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Joe Orton <jorton@redhat.com> - 1.4.1-4
- fix crypt_r failure modes (#819650)

* Tue Apr 24 2012 Joe Orton <jorton@redhat.com> - 1.4.1-3
- apply _isa to deps

* Mon Apr 23 2012 Joe Orton <jorton@redhat.com> - 1.4.1-2
- switch to libdb-devel

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Bojan Smojver <bojan@rexursive.com> - 1.4.1-1
- bump up to 1.4.1

* Fri May 20 2011 Bojan Smojver <bojan@rexursive.com> - 1.3.12-1
- bump up to 1.3.12

* Wed May 11 2011 Bojan Smojver <bojan@rexursive.com> - 1.3.11-2
- fix crash in apr_ldap_rebind_init()

* Mon May  9 2011 Bojan Smojver <bojan@rexursive.com> - 1.3.11-1
- bump up to 1.3.11

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 1.3.10-7
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Wed Mar 23 2011 Joe Orton <jorton@redhat.com> - 1.3.10-6
- rebuild for MySQL soname bump

* Wed Mar  2 2011 Joe Orton <jorton@redhat.com> - 1.3.10-5
- fix build

* Wed Mar  2 2011 Joe Orton <jorton@redhat.com> - 1.3.10-4
- rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Bojan Smojver <bojan@rexursive.com> - 1.3.10-2
- rebuild for MySQL 5.5.x

* Tue Oct  5 2010 Joe Orton <jorton@redhat.com> - 1.3.10-1
- update to 1.3.10

* Wed Nov 25 2009 Joe Orton <jorton@redhat.com> - 1.3.9-3
- rebuild for new BDB

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.3.9-2
- rebuilt with new openssl

* Thu Aug  6 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.9-1
- bump up to 1.3.9
- CVE-2009-2412
- allocator alignment fixes

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Bojan Smojver <bojan@rexursive.com> 1.3.8-2
- adjust apr-util-1.3.7-nodbmdso.patch

* Wed Jul 15 2009 Bojan Smojver <bojan@rexursive.com> 1.3.8-1
- bump up to 1.3.8

* Wed Jul 15 2009 Bojan Smojver <bojan@rexursive.com> 1.3.7-5
- BR: +libuuid-devel, -e2fsprogs-devel

* Tue Jun  9 2009 Joe Orton <jorton@redhat.com> 1.3.7-4
- disable DBM-drivers-as-DSO support
- backport r783046 from upstream

* Mon Jun  8 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.7-3
- make export of LD_LIBRARY_PATH simpler

* Mon Jun  8 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.7-2
- revert tests

* Mon Jun  8 2009 Bojan Smojver <bojan@rexursive.com> - 1.3.7-1
- bump up to 1.3.7
- CVE-2009-0023
- "billion laughs" fix of apr_xml_* interface

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Joe Orton <jorton@redhat.com> 1.3.4-2
- rebuild for new MySQL

* Sat Aug 16 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.4-1
- bump up to 1.3.4
- drop PostgreSQL patch, fixed upstream

* Wed Jul 16 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-8
- beat the fuzz, rework apr-util-1.2.7-pkgconf.patch

* Wed Jul 16 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-7
- ship find_apu.m4, fix bug #455189

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.2-6
- rebuild for new db4-4.7

* Tue Jul  8 2008 Joe Orton <jorton@redhat.com> 1.3.2-5
- restore requires for openldap-devel from -devel

* Wed Jul  2 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-4
- properly fix PostgreSQL detection

* Wed Jul  2 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-3
- revert build dependencies, change from -2 didn't help
- add apr-util-1.3.2-pgsql.patch (remove pgsql_LIBS during detection)

* Wed Jul  2 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-2
- try adding postgresql-server to build dependencies to pull some libs in

* Thu Jun 19 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.2-1
- bump up to 1.3.2

* Sun Jun  1 2008 Bojan Smojver <bojan@rexursive.com> - 1.3.0-1
- bump up to 1.3.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.2.12-5
- Autorebuild for GCC 4.3

* Tue Dec  4 2007 Joe Orton <jorton@redhat.com> 1.2.12-4
- rebuild for OpenLDAP soname bump

* Mon Dec  3 2007 Bojan Smojver <bojan@rexursive.com> - 1.2.12-3
- remove all instances of MySQL flags being added to APRUTIL_LDFLAGS

* Tue Nov 27 2007 Bojan Smojver <bojan@rexursive.com> - 1.2.12-1
- bump up to 1.2.12
- drop MySQL DBD driver, shipped upstream
- adjust various patches to apply
- rework tests in %%check (1.2.x got tests from trunk)

* Mon Sep 24 2007 Jesse Keating <jkeating@redhat.com> - 1.2.10-2
- Rebuild for upgrade path (add dist since that's now on F-7 branch)

* Sun Sep  9 2007 Bojan Smojver <bojan@rexursive.com> 1.2.10-1
- bump up to 1.2.10
- pick up newly checked in MySQL DBD driver directly from ASF
- remove dbdopen patch (fixed upstream)
- remove xmlns patch (fixed upstream)
- remove autoexpat patch (fixed upstream)

* Sun Sep  2 2007 Joe Orton <jorton@redhat.com> 1.2.8-12
- rebuild for fixed APR 32-bit ABI
- remove sqlite driver from main package (#274521)

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 1.2.8-11
- rebuild for expat soname bump

* Tue Aug 21 2007 Joe Orton <jorton@redhat.com> 1.2.8-10
- fix License

* Wed Aug  8 2007 Joe Orton <jorton@redhat.com> 1.2.8-9
- add rewrite of expat autoconf code (upstream r493791)
- fix build for new glibc open()-as-macro
- split out sqlite subpackage

* Tue Jul  3 2007 Joe Orton <jorton@redhat.com> 1.2.8-8
- add fix for attribute namespace handling in apr_xml (PR 41908)

* Thu Apr  5 2007 Joe Orton <jorton@redhat.com> 1.2.8-7
- remove old Conflicts, doxygen BR (#225254)

* Fri Mar 23 2007 Joe Orton <jorton@redhat.com> 1.2.8-6
- add DBD DSO lifetime fix (r521327)

* Thu Mar 22 2007 Joe Orton <jorton@redhat.com> 1.2.8-5
- drop doxygen documentation (which caused multilib conflicts)

* Wed Feb 28 2007 Joe Orton <jorton@redhat.com> 1.2.8-4
- add mysql driver in -mysql subpackage (Bojan Smojver, #222237)

* Tue Feb 27 2007 Joe Orton <jorton@redhat.com> 1.2.8-3
- build DBD drivers as DSOs (w/Bojan Smojver, #192922)
- split out pgsql driver into -pgsql subpackage

* Tue Dec  5 2006 Joe Orton <jorton@redhat.com> 1.2.8-2
- update to 1.2.8, pick up new libpq soname

* Fri Dec  1 2006 Joe Orton <jorton@redhat.com> 1.2.7-5
- really rebuild for db45

* Sat Nov 11 2006 Joe Orton <jorton@redhat.com> 1.2.7-4
- add support for BDB 4.5 from upstream, rebuild

* Wed Jul 19 2006 Joe Orton <jorton@redhat.com> 1.2.7-3
- fix buildconf with autoconf 2.60

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.7-2.1
- rebuild

* Tue May  2 2006 Joe Orton <jorton@redhat.com> 1.2.7-2
- update to 1.2.7
- use pkg-config in apu-1-config to make it libdir-agnostic

* Thu Apr  6 2006 Joe Orton <jorton@redhat.com> 1.2.6-2
- update to 1.2.6
- define LDAP_DEPRECATED in apr_ldap.h (r391985, #188073)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.2-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Joe Orton <jorton@redhat.com> 1.2.2-4
- rebuild to drop reference to libexpat.la

* Wed Jan 18 2006 Joe Orton <jorton@redhat.com> 1.2.2-3
- disable sqlite2 support
- BuildRequire e2fsprogs-devel
- enable malloc paranoia in %%check

* Tue Jan  3 2006 Jesse Keating <jkeating@redhat.com> 1.2.2-2.2
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Dec  6 2005 Joe Orton <jorton@redhat.com> 1.2.2-2
- trim exports from .la file/--libs output (#174924)

* Fri Nov 25 2005 Joe Orton <jorton@redhat.com> 1.2.2-1
- update to 1.2.2

* Thu Oct 20 2005 Joe Orton <jorton@redhat.com> 0.9.7-3
- fix epoch again

* Thu Oct 20 2005 Joe Orton <jorton@redhat.com> 0.9.7-2
- update to 0.9.7
- drop static libs (#170051)

* Tue Jul 26 2005 Joe Orton <jorton@redhat.com> 0.9.6-3
- add FILE bucket fix for truncated files (#159191)
- add epoch to dependencies

* Fri Mar  4 2005 Joe Orton <jorton@redhat.com> 0.9.6-2
- rebuild

* Wed Feb  9 2005 Joe Orton <jorton@redhat.com> 0.9.6-1
- update to 0.9.6

* Wed Jan 19 2005 Joe Orton <jorton@redhat.com> 0.9.5-3
- restore db-4.3 detection lost in 0.9.5 upgrade

* Wed Jan 19 2005 Joe Orton <jorton@redhat.com> 0.9.5-2
- rebuild

* Mon Nov 22 2004 Joe Orton <jorton@redhat.com> 0.9.5-1
- update to 0.9.5

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 0.9.4-19
- actually explicitly check for and detect db-4.3.

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 0.9.4-18
- rebuild against db-4.3.21.

* Fri Sep 17 2004 Joe Orton <jorton@redhat.com> 0.9.4-17
- add security fix for CAN-2004-0786

* Sat Jun 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-16
- have -devel require matching release of apr-util

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  1 2004 Joe Orton <jorton@redhat.com> 0.9.4-14
- fix use of SHA1 passwords (#119651)

* Tue Mar 30 2004 Joe Orton <jorton@redhat.com> 0.9.4-13
- remove fundamentally broken check_sbcs() from xlate code

* Fri Mar 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-12
- tweak xlate fix

* Fri Mar 19 2004 Joe Orton <jorton@redhat.com> 0.9.4-11
- rebuild with xlate fixes and tests enabled

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-10.1
- rebuilt

* Tue Mar  2 2004 Joe Orton <jorton@redhat.com> 0.9.4-10
- rename sdbm_* symbols to apu__sdbm_*

* Mon Feb 16 2004 Joe Orton <jorton@redhat.com> 0.9.4-9
- fix sdbm apr_dbm_exists() on s390x/ppc64

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 0.9.4-8
- rebuilt

* Thu Feb  5 2004 Joe Orton <jorton@redhat.com> 0.9.4-7
- fix warnings from use of apr_optional*.h with gcc 3.4

* Thu Jan 29 2004 Joe Orton <jorton@redhat.com> 0.9.4-6
- drop gdbm support

* Thu Jan  8 2004 Joe Orton <jorton@redhat.com> 0.9.4-5
- fix DB library detection

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 0.9.4-4
- rebuild against db-4.2.52.

* Mon Oct 13 2003 Jeff Johnson <jbj@jbj.org> 0.9.4-3
- rebuild against db-4.2.42.

* Mon Oct  6 2003 Joe Orton <jorton@redhat.com> 0.9.4-2
- fix 'apu-config --apu-la-file' output

* Mon Oct  6 2003 Joe Orton <jorton@redhat.com> 0.9.4-1
- update to 0.9.4.

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 0.9.3-10
- rebuild

* Mon Jul  7 2003 Joe Orton <jorton@redhat.com> 0.9.3-9
- rebuild
- don't run testuuid test because of #98677

* Thu Jul  3 2003 Joe Orton <jorton@redhat.com> 0.9.3-8
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Joe Orton <jorton@redhat.com> 0.9.3-6
- fix to detect crypt_r correctly (CAN-2003-0195)

* Thu May 15 2003 Joe Orton <jorton@redhat.com> 0.9.3-5
- fix to try linking against -ldb first (#90917)
- depend on openldap, gdbm, db4, expat appropriately.

* Tue May 13 2003 Joe Orton <jorton@redhat.com> 0.9.3-4
- rebuild

* Wed May  7 2003 Joe Orton <jorton@redhat.com> 0.9.3-3
- make devel package conflict with old subversion-devel
- run the less crufty parts of the test suite

* Tue Apr 29 2003 Joe Orton <jorton@redhat.com> 0.9.3-2
- run ldconfig in post/postun

* Mon Apr 28 2003 Joe Orton <jorton@redhat.com> 0.9.3-1
- initial build
