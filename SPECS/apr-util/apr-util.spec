%define     apuver    1

Summary:        The Apache Portable Runtime Utility Library
Name:           apr-util
Version:        1.6.3
Release:        2%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Libraries
URL:            https://apr.apache.org/
Source0:        https://archive.apache.org/dist/apr/%{name}-%{version}.tar.gz
# Using Fedora 40 patch to enable LMDB support:
Patch0:         apr-util-1.6.3-lmdb-support.patch

BuildRequires:  apr-devel
BuildRequires:  expat-devel
BuildRequires:  openssl-devel
BuildRequires:  sqlite-devel

Requires:       apr
Requires:       expat
Requires:       openssl

%description
The Apache Portable Runtime Utility Library.

%package lmdb
Summary: APR utility library LMDB driver

BuildRequires:  lmdb-devel
Requires:       apr-util%{?_isa} = %{version}-%{release}

%description lmdb
This package provides the LMDB driver for the apr-util
DBM (database abstraction) interface.

%package devel
Summary:        APR utility library development kit
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}
Requires:       apr-devel
Requires:       expat-devel

%description devel
This package provides the support files which can be used to
build applications using the APR utility library.

%package ldap
Summary:        APR utility library LDAP support
Group:          Development/Libraries

BuildRequires:  openldap

Requires:       %{name} = %{version}-%{release}
Requires:       openldap

%description ldap
This package provides the LDAP support for the apr-util.

%package mysql
Summary:        APR utility library MySQL DBD driver

BuildRequires:  mariadb-devel

Requires:       %{name} = %{version}-%{release}

%description mysql
This package provides the MySQL driver for the apr-util DBD
(database abstraction) interface.

%package odbc
Summary:        APR utility library ODBC DBD driver

BuildRequires:  unixODBC-devel

Requires:       %{name} = %{version}-%{release}

%description odbc
This package provides the ODBC driver for the apr-util DBD
(database abstraction) interface.

%package openssl
Summary:        APR utility library OpenSSL crypto support

BuildRequires:  openssl-devel

Requires:       %{name} = %{version}-%{release}

%description openssl
This package provides the OpenSSL crypto support for the apr-util.

%package pgsql
Summary:        APR utility library PostgreSQL DBD driver
Group:          Development/Libraries

BuildRequires:  postgresql-devel >= 10.5

Requires:       %{name} = %{version}-%{release}
Requires:       postgresql >= 10.5

%description pgsql
This package provides the PostgreSQL driver for the apr-util DBD (database abstraction) interface.

%package sqlite
Summary:        APR utility library SQLite DBD driver.
Group:          Development/Libraries

Requires:       %{name} = %{version}-%{release}

%description sqlite
This package provides the SQLite driver for the apr-util DBD
(database abstraction) interface.

%prep
%autosetup -p1

%build
autoheader && autoconf
%configure --with-apr=%{_prefix} \
        --includedir=%{_includedir}/apr-%{apuver} \
        --with-crypto \
        --with-dbm=lmdb --with-lmdb \
        --with-ldap \
        --with-mysql \
        --with-odbc \
        --with-openssl=%{_prefix} \
        --with-pgsql \
        --with-sqlite3 \
        --without-gdbm \
        --without-nss \
        --without-sqlite2

%make_build

%install
%make_install

%check
# Disable smp_flag because of race condition
%make_build -j1 check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/aprutil.exp
%{_libdir}/libaprutil-%{apuver}.so.*
%exclude %{_libdir}/debug

%files lmdb
%defattr(-,root,root)
%{_libdir}/apr-util-%{apuver}/apr_dbm_lmdb*

%files devel
%defattr(-,root,root)
%{_libdir}/libaprutil-%{apuver}.*a
%{_libdir}/libaprutil-%{apuver}.so
%{_bindir}/*
%{_includedir}/*
%{_libdir}/pkgconfig/apr-util-%{apuver}.pc

%files ldap
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_ldap*

%files mysql
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_mysql*

%files odbc
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_odbc*

%files openssl
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_crypto_openssl*

%files pgsql
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_pgsql*

%files sqlite
%defattr(-,root,root,-)
%{_libdir}/apr-util-%{apuver}/apr_dbd_sqlite*

%changelog
* Fri Jun 07 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.3-2
- Switching to LMDB from BDB using Fedora 40 (license: MIT) spec for guidance.

* Mon Feb 06 2023 Rachel Menge <rachelmenge@microsoft.com> - 1.6.3-1
- Upgrade to 1.6.3
- Fix license tag

* Tue Nov 30 2021 Mateusz Malisz <mamalisz@microsoft.com> - 1.6.1-6
- Add libdb dependencies to berkleydb subpackage.

* Tue Aug 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.1-5
- Added support for more databases: BDB, ODBC, MySQL.
- Split out the "*-openssl" subpackage.
- Removed NSS components.
- Removed the "sha1" macro.
- License verified.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.6.1-4
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.6.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> - 1.6.1-2
- Consuming postgresql 10.5

* Tue Sep 18 2018 Ankit Jain <ankitja@vmware.com> - 1.6.1-1
- Updated to version 1.6.1

* Mon Sep 18 2017 Rui Gu <ruig@vmware.com> - 1.5.4-12
- Disable smp_flag on make check because of race condition

* Thu Jul 6 2017 Divya Thaluru <dthaluru@vmware.com> - 1.5.4-11
- Added build requires on postgresql-devel

* Wed May 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.5.4-10
- Add missing Requires.

* Tue Apr 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.5.4-9
- Add expat-devel build deps otherwise it builds expat from its source tree

* Fri Nov 18 2016 Alexey Makhalov <amakhalov@vmware.com> - 1.5.4-8
- Add sqlite-devel build deps

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.5.4-7
- GA - Bump release of all rpms

* Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 1.5.4-6
- remove libexpat files

* Tue Sep 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 1.5.4-5
- Updated build-requires after creating devel package for apr.

* Wed Sep 16 2015 Xiaolin Li <xiaolinl@vmware.com> - 1.5.4-4
- Seperate Separate apr-util to apr-util, apr-util-devel, aprutil-ldap, apr-util-pgsql, and apr-utilsqlite.

* Wed Jul 15 2015 Sarah Choi <sarahc@vmware.com> - 1.5.4-4
- Use apuver(=1) instead of version for mesos

* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> - 1.5.2-3
- Exclude /usr/lib/debug

* Wed Jul 01 2015 Touseef Liaqat <tliaqat@vmware.com> - 1.5.2-2
- Fix tags and paths.

* Wed May 20 2015 Touseef Liaqat <tliaqat@vmware.com> - 1.5.4-1
- Initial build. First version
