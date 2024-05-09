Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Database-specific drivers for libdbi
Name: libdbi-drivers
Version: 0.9.0
Release: 16%{?dist}
License: LGPLv2+
URL: https://libdbi-drivers.sourceforge.net/

Source: https://prdownloads.sourceforge.net/libdbi-drivers/%{name}-%{version}.tar.gz
# old automake does not offer aarch64
Patch1: libdbi-drivers-aarch64.patch

Requires: libdbi%{?_isa} >= 0.9
BuildRequires: libdbi-devel >= 0.9
BuildRequires: autoconf openjade docbook-style-dsssl
BuildRequires: gcc

%description
libdbi implements a database-independent abstraction layer in C, similar to the
DBI/DBD layer in Perl. Writing one generic set of code, programmers can
leverage the power of multiple databases and multiple simultaneous database
connections by using this framework.

libdbi-drivers contains the database-specific plugins needed to connect
libdbi to particular database servers.

%package -n libdbi-dbd-mysql
Summary: MySQL plugin for libdbi
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires: mariadb-connector-c-devel, openssl-devel

%description -n libdbi-dbd-mysql
This plugin provides connectivity to MySQL/MariaDB database servers through
the libdbi database independent abstraction layer. Switching a program's
plugin does not require recompilation or rewriting source code.

%package -n libdbi-dbd-pgsql
Summary: PostgreSQL plugin for libdbi
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires: libpq-devel, krb5-devel, openssl-devel

%description -n libdbi-dbd-pgsql
This plugin provides connectivity to PostgreSQL database servers through the
libdbi database independent abstraction layer. Switching a program's plugin
does not require recompilation or rewriting source code.

%package -n libdbi-dbd-sqlite
Summary: SQLite plugin for libdbi
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires: sqlite-devel

%description -n libdbi-dbd-sqlite
This plugin provides access to an embedded SQL engine using libsqlite3 through
the libdbi database independent abstraction layer. Switching a program's plugin
does not require recompilation or rewriting source code.

%prep
%setup -q -n %{name}-%{version}
%patch 1 -p1
autoconf
# mariadb provides headers in a subfolder <mysql/mysql.h>
sed -i -r 's|<(mysql\.h)>|<mysql/\1>|' drivers/mysql/dbd_mysql.c
# exporting LDFLAGS or LIBS or SQLITE3_LIBS before running autoconf or
#   ./configure doesn't help => hardcode it
sed -i -r "s|(SQLITE3_LIBS=)-lsqlite[^[:space:]]*|\1$(pkg-config --libs-only-l sqlite3)|" \
  configure

%build
# configure is broken, must pass both --with-*sql-libdir _AND_
# --with-*sql-incdir in order for --with-*sql-libdir to be used
%configure --with-mysql --with-pgsql --with-sqlite3 \
	--with-mysql-libdir=%{_libdir}/mariadb \
	--with-mysql-incdir=%{_includedir} \
	--with-pgsql-libdir=%{_libdir} \
	--with-pgsql-incdir=%{_includedir} \
	--with-sqlite3-libdir=%{_libdir} \
	--with-sqlite3-incdir=%{_includedir} \
	--with-dbi-libdir=%{_libdir}

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f ${RPM_BUILD_ROOT}%{_libdir}/dbd/*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/dbd/*.la

# package the docs via %%doc directives
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog COPYING README
%doc drivers/mysql/dbd_mysql/*.html
%doc drivers/mysql/*.pdf
%doc drivers/pgsql/dbd_pgsql/*.html
%doc drivers/pgsql/*.pdf
%doc drivers/sqlite3/dbd_sqlite3/*.html
%doc drivers/sqlite3/*.pdf
%dir %{_libdir}/dbd

%files -n libdbi-dbd-mysql
%{_libdir}/dbd/libdbdmysql.*

%files -n libdbi-dbd-pgsql
%{_libdir}/dbd/libdbdpgsql.*

%files -n libdbi-dbd-sqlite
%{_libdir}/dbd/libdbdsqlite3.*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.0-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Marek Skalický <mskalick@redhat.com> - 0.9.0-11
- Add missing BuildRequires: gcc/gcc-c++

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 17 2017 Marek Skalický <mskalick@redhat.com> - 0.9.0-9
- Use mariadb-connector-c-devel instead of mariadb-devel

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Jan Pacner <jpacner@redhat.com> - 0.9.0-1
- new release

* Mon Jul 29 2013 Honza Horak <hhorak@redhat.com> 0.8.3-13
- Spec file clean-up
- Add support for aarch64

* Tue Mar  5 2013 Tom Lane <tgl@redhat.com> 0.8.3-12
- Remove unnecessary package-name Requires:, since dependencies on library
  sonames should be enough, and we don't want to hard-wire assumptions about
  which packages provide which libraries
- isa-ify cross-subpackage Requires:

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Tom Lane <tgl@redhat.com> 0.8.3-8
- Rebuild for libmysqlclient 5.5.10 soname version bump

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep  3 2010 Tom Lane <tgl@redhat.com> 0.8.3-6
- Do not use -ffast-math; it breaks things and seems quite unlikely to offer
  any useful performance benefit for this type of package, anyway
Resolves: #629964

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Tom Lane <tgl@redhat.com> 0.8.3-3
- Rebuild for mysql 5.1

* Mon Sep  1 2008 Tom Lane <tgl@redhat.com> 0.8.3-2
- Fix mistaken external reference in libdbdsqlite3.so.  (I'm applying this
  as a patch, rather than updating to upstream's 0.8.3-1, because that isn't
  acceptable as an RPM Version tag.)
Resolves: #460734

* Mon Feb 11 2008 Tom Lane <tgl@redhat.com> 0.8.3-1
- Update to version 0.8.3.
- Code is now all licensed LGPLv2+, so adjust License tags.

* Tue Oct 30 2007 Tom Lane <tgl@redhat.com> 0.8.2-1.3
- Fix package's selection of CFLAGS to include RPM_OPT_FLAGS
Resolves: #330691

* Fri Aug  3 2007 Tom Lane <tgl@redhat.com> 0.8.2-1.2
- Correct License tag for sqlite subpackage; it's currently not same license
  as the rest of the code.

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 0.8.2-1.1
- Update to version 0.8.2-1.
- Update License tag to match code.
- Remove static libraries and .la files, per packaging guidelines.
- Fix up packaging of documentation.

* Mon Dec 11 2006 Tom Lane <tgl@redhat.com> 0.8.1a-2
- Enable building of sqlite driver
Resolves: #184568
- Rebuild needed anyway for Postgres library update

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1a-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1a-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.1a-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 12 2005 Tom Lane <tgl@redhat.com> 0.8.1a-1
- Update to version 0.8.1a.

* Tue Apr 12 2005 Tom Lane <tgl@redhat.com> 0.7.1-3
- Rebuild for Postgres 8.0.2 (new libpq major version).

* Fri Mar 11 2005 Tom Lane <tgl@redhat.com> 0.7.1-2
- Packaging improvements per discussion with sopwith.

* Thu Mar 10 2005 Tom Lane <tgl@redhat.com> 0.7.1-1
- Import new libdbi version, splitting libdbi-drivers into a separate SRPM
  so we can track new upstream packaging.
