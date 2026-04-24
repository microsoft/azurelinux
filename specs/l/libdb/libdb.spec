# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This must remain enabled even for RHEL/ELN until all libdb dependencies
# are dropped, then this should be Fedora-only
%bcond_without subpackages

%define __soversion_major 5
%define __soversion %{__soversion_major}.3
%define __tclversion 8.6
%define _converter_version 1.0.3

# The SQLite configure script does not support --runstatedir and is not
# regenerated.
%undefine _configure_use_runstatedir

Summary: The Berkeley DB database library for C
Name: libdb
Version: 5.3.28
Release: 67%{?dist}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Source1: http://download.oracle.com/berkeley-db/db.1.85.tar.gz
# For mt19937db.c
Source2: http://www.gnu.org/licenses/lgpl-2.1.txt
# libdb man pages generated from the 5.3.28 documentation
Source3: libdb-5.3.28-manpages.tar.gz
Source4: https://github.com/fila43/db_converter/archive/refs/tags/v%{_converter_version}.tar.gz
Patch0: libdb-multiarch.patch
# db-1.85 upstream patches
Patch10: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.1
Patch11: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.2
Patch12: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.3
Patch13: http://www.oracle.com/technology/products/berkeley-db/db/update/1.85/patch.1.4
# other patches
Patch20: db-1.85-errno.patch
Patch22: db-4.6.21-1.85-compat.patch
Patch24: db-4.5.20-jni-include-dir.patch
# License clarification patch
# http://devel.trisquel.info/gitweb/?p=package-helpers.git;a=blob;f=helpers/DATA/db4.8/007-mt19937db.c_license.patch;h=1036db4d337ce4c60984380b89afcaa63b2ef88f;hb=df48d40d3544088338759e8bea2e7f832a564d48
Patch25: 007-mt19937db.c_license.patch
# memp_stat fix provided by upstream (rhbz#1211871)
Patch27: db-5.3.21-memp_stat-upstream-fix.patch
# fix for mutexes not being released provided by upstream (rhbz#1277887)
Patch28: db-5.3.21-mutex_leak.patch
# fix for overflowing hash variable inside bundled lemon
Patch29: db-5.3.28-lemon_hash.patch
# upstream patch adding the ability to recreate libdb's environment on version mismatch
# or when libpthread.so is modified (rhbz#1394862)
Patch30: db-5.3.28-condition_variable.patch
# additional changes to the upstream patch to address rhbz#1460003
Patch31: db-5.3.28-condition-variable-ppc.patch
# downstream patch that adds a check for rpm transaction lock in order to be able to update libdb
# FIXME: remove when able
Patch32: db-5.3.28-rpm-lock-check.patch
# downstream patch to hotfix rhbz#1464033, sent upstream
Patch33: db-5.3.28-cwd-db_config.patch
Patch34: libdb-5.3.21-region-size-check.patch
# Patch sent upstream
Patch35: checkpoint-opd-deadlock.patch
Patch36: db-5.3.28-atomic_compare_exchange.patch
# CDB race (rhbz #1099509)
Patch37: libdb-cbd-race.patch
# Limit concurrency to max 1024 CPUs (rhbz#1245410)
# A fix for the issue should be in an upstream release already
# https://community.oracle.com/message/13274780#13274780
Patch38: libdb-limit-cpu.patch
# rhbz#1608749 Patch sent upstream
# Expects libdb-5.3.21-mutex_leak.patch applied
Patch39: libdb-5.3.21-trickle_cpu.patch
# cve-2019-2708 fixed by mmuzila
Patch40: db-5.3.28_cve-2019-2708.patch
# Prevents high CPU usage
Patch41: db-5.3.28-mmap-high-cpu-usage.patch

Patch42: libdb-1.85-c99.patch
Patch43: libdb-c99.patch
Patch44: libdb-configure-c99.patch
Patch45: libdb-sqlite-c99.patch
# Fix build with tcl8
Patch46: libdb-sqlite-tcl8.patch

URL: http://www.oracle.com/database/berkeley-db/
License: BSD-3-Clause AND LGPL-2.1-only AND Sleepycat
BuildRequires: gcc gcc-c++
BuildRequires: perl-interpreter libtool
BuildRequires: tcl-devel < 1:9.0
BuildRequires: chrpath
BuildRequires: zlib-devel
BuildRequires: make gdbm-devel lmdb-devel
Conflicts: filesystem < 3

# libdb was marked as deprecated in F33:
# https://fedoraproject.org/wiki/Changes/Libdb_deprecated
Provides:  deprecated()

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package utils
Summary: Command line tools for managing Berkeley DB databases
Requires: %{name}%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. DB supports C, C++ and Perl APIs.

%package devel
Summary: C development files for the Berkeley DB library
Requires: %{name}%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package devel-doc
Summary: C development documentation files for the Berkeley DB library
Requires: %{name} = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
BuildArch: noarch

Provides:  deprecated()

%description devel-doc
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the header files,
libraries, and documentation for building programs which use the
Berkeley DB.

%package devel-static
Summary: Berkeley DB static libraries
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description devel-static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains static libraries
needed for applications that require static linking of
Berkeley DB.

%package cxx
Summary: The Berkeley DB database library for C++
Requires: %{name}%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description cxx
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package cxx-devel
Summary: The Berkeley DB database library for C++
Requires: %{name}-cxx%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description cxx-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. The Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching, and database
recovery. The Berkeley DB supports C, C++, and Perl APIs. It is
used by many applications, including Python and Perl, so this should
be installed on all systems.

%package tcl
Summary: Development files for using the Berkeley DB with tcl
Requires: %{name}%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description tcl
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

%package tcl-devel
Summary: Development files for using the Berkeley DB with tcl
Requires: %{name}-tcl%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description tcl-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in Tcl.

%package sql
Summary: Development files for using the Berkeley DB with sql
Requires: %{name}%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description sql
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in SQL.

%package sql-devel
Summary: Development files for using the Berkeley DB with sql
Requires: %{name}-sql%{?_isa} = %{version}-%{release}

Provides:  deprecated()

%description sql-devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in SQL.

%package convert-util
Summary: Development files for using the Berkeley DB with sql

%description convert-util
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. This package contains the libraries
for building programs which use the Berkeley DB in SQL.


%prep
%setup -q -n db-%{version} -a 1
cp %{SOURCE2} .
tar -xf %{SOURCE3}
# db_converter
tar -xf %{SOURCE4}


%patch -P0 -p1
pushd db.1.85/PORT/linux
%patch -P10 -p0
popd
pushd db.1.85
%patch -P11 -p0
%patch -P12 -p0
%patch -P13 -p0
%patch -P20 -p1
popd

%patch -P22 -p1
%patch -P24 -p1
%patch -P25 -p1
%patch -P27 -p1
%patch -P28 -p1
%patch -P29 -p1
%patch -P30 -p1
%patch -P31 -p1
%patch -P32 -p1
%patch -P33 -p1
%patch -P34 -p1
%patch -P35 -p1
%patch -P36 -p1
%patch -P37 -p1
%patch -P38 -p1
%patch -P39 -p1
%patch -P40 -p1 -b .cve-2019-2708
%patch -P41 -p1
%patch -P42 -p1
%patch -P43 -p1
%patch -P44 -p1
%patch -P45 -p1
%patch -P46 -p1

cd dist
./s_config
cd ..

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -std=gnu99"
CFLAGS="$CFLAGS -DSHAREDSTATEDIR='\"%{_sharedstatedir}\"' -DSQLITE_ENABLE_COLUMN_METADATA=1 -DSQLITE_DISABLE_DIRSYNC=1 -DSQLITE_ENABLE_FTS3=3 -DSQLITE_ENABLE_RTREE=1 -DSQLITE_SECURE_DELETE=1 -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -I../../../lang/sql/sqlite/ext/fts3/"
export CFLAGS

# Build the old db-185 libraries.
make -C db.1.85/PORT/%{_os} OORG="$CFLAGS"

test -d dist/dist-tls || mkdir dist/dist-tls
# Static link db_dump185 with old db-185 libraries.
/bin/sh libtool --tag=CC --mode=compile	%{__cc} $RPM_OPT_FLAGS -Idb.1.85/PORT/%{_os}/include -D_REENTRANT -c util/db_dump185.c -o dist/dist-tls/db_dump185.lo
/bin/sh libtool --tag=CC --mode=link %{__cc} $RPM_LD_FLAGS -o dist/dist-tls/db_dump185 dist/dist-tls/db_dump185.lo db.1.85/PORT/%{_os}/libdb.a

# Update config files to understand aarch64
for dir in dist lang/sql/sqlite lang/sql/jdbc lang/sql/odbc; do
  cp /usr/lib/rpm/redhat/config.{guess,sub} "$dir"
done

pushd dist/dist-tls
%define _configure ../configure
%configure -C \
	--enable-compat185 --enable-dump185 \
	--enable-shared --enable-static \
	--enable-tcl --with-tcl=/usr/%{_lib} TCLSH_CMD=$(which tclsh%{__tclversion}) \
	--enable-cxx --enable-sql \
	--enable-test \
	--disable-rpath

# Remove libtool predep_objects and postdep_objects wonkiness so that
# building without -nostdlib doesn't include them twice.  Because we
# already link with g++, weird stuff happens if you don't let the
# compiler handle this.
perl -pi -e 's/^predep_objects=".*$/predep_objects=""/' libtool
perl -pi -e 's/^postdep_objects=".*$/postdep_objects=""/' libtool
perl -pi -e 's/-shared -nostdlib/-shared/' libtool

%make_build

# Run some quick subsystem checks
echo "source ../../test/tcl/test.tcl; r env; r mut; r memp" | tclsh%{__tclversion}
popd

pushd db_converter-%{_converter_version}
# libdb-5.3.a is part of static package, build produces libdb.a
sed -i 's/-ldb-5.3/-ldb/g' Makefile
# Set path to headers and library to previously built files
# since this tool is intended to build statically
make LDFLAGS="-I../dist/dist-tls -L../dist/dist-tls -Wl,-z,now $RPM_LD_FLAGS" CFLAGS="-g -fPIC %build_cflags" static
popd

%install
%if %{with subpackages}
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
%make_install STRIP=/bin/true -C dist/dist-tls

# XXX Nuke non-versioned archives and symlinks
rm -f ${RPM_BUILD_ROOT}%{_libdir}/{libdb.a,libdb_cxx.a,libdb_tcl.a,libdb_sql.a}

chmod +x ${RPM_BUILD_ROOT}%{_libdir}/*.so*

# Move the header files to a subdirectory, in case we're deploying on a
# system with multiple versions of DB installed.
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}/%{name}
mv ${RPM_BUILD_ROOT}%{_includedir}/*.h ${RPM_BUILD_ROOT}%{_includedir}/%{name}/

# Create symlinks to includes so that "use <db.h> and link with -ldb" works.
for i in db.h db_cxx.h db_185.h; do
	ln -s %{name}/$i ${RPM_BUILD_ROOT}%{_includedir}
done

# Eliminate installed doco
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/docs

# XXX Avoid Permission denied. strip when building as non-root.
chmod u+w ${RPM_BUILD_ROOT}%{_bindir} ${RPM_BUILD_ROOT}%{_bindir}/*

# remove unneeded .la files (#225675)
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

# remove RPATHs
chrpath -d ${RPM_BUILD_ROOT}%{_libdir}/*.so ${RPM_BUILD_ROOT}%{_bindir}/*

# unify documentation and examples, remove stuff we don't need
rm -rf docs/csharp
rm -rf examples/csharp
rm -rf docs/installation
mv examples docs
mv man/* ${RPM_BUILD_ROOT}%{_mandir}/man1

%ldconfig_scriptlets
%ldconfig_scriptlets cxx
%ldconfig_scriptlets sql
%ldconfig_scriptlets tcl
%else
mkdir -p %{buildroot}%{_bindir}
%endif
install -m 0755 db_converter-%{_converter_version}/db_converter %{buildroot}/%{_bindir}/db_converter

%files
%license LICENSE lgpl-2.1.txt
%if %{with subpackages}
%doc README
%{_libdir}/libdb-%{__soversion}.so
%{_libdir}/libdb-%{__soversion_major}.so
%else
%{_bindir}/db_converter
%endif

%if %{with subpackages}
%files devel
%{_libdir}/libdb.so
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/db.h
%{_includedir}/%{name}/db_185.h
%{_includedir}/db.h
%{_includedir}/db_185.h
%endif

%if %{with subpackages}
%files devel-doc
%doc	docs/*
%endif

%if %{with subpackages}
%files devel-static
%{_libdir}/libdb-%{__soversion}.a
%{_libdir}/libdb_cxx-%{__soversion}.a
%{_libdir}/libdb_tcl-%{__soversion}.a
%{_libdir}/libdb_sql-%{__soversion}.a
%endif

%if %{with subpackages}
%files utils
%{_bindir}/db*_archive
%{_bindir}/db*_checkpoint
%{_bindir}/db*_deadlock
%{_bindir}/db*_dump*
%{_bindir}/db*_hotbackup
%{_bindir}/db*_load
%{_bindir}/db*_printlog
%{_bindir}/db*_recover
%{_bindir}/db*_replicate
%{_bindir}/db*_stat
%{_bindir}/db*_upgrade
%{_bindir}/db*_verify
%{_bindir}/db*_tuner
%{_mandir}/man1/db_*
%endif

%if %{with subpackages}
%files convert-util
%{_bindir}/db_converter
%endif

%if %{with subpackages}
%files cxx
%{_libdir}/libdb_cxx-%{__soversion}.so
%{_libdir}/libdb_cxx-%{__soversion_major}.so
%endif

%if %{with subpackages}
%files cxx-devel
%{_includedir}/%{name}/db_cxx.h
%{_includedir}/db_cxx.h
%{_libdir}/libdb_cxx.so
%endif

%if %{with subpackages}
%files tcl
%{_libdir}/libdb_tcl-%{__soversion}.so
%{_libdir}/libdb_tcl-%{__soversion_major}.so
%endif

%if %{with subpackages}
%files tcl-devel
%{_libdir}/libdb_tcl.so
%endif

%if %{with subpackages}
%files sql
%{_libdir}/libdb_sql-%{__soversion}.so
%{_libdir}/libdb_sql-%{__soversion_major}.so
%endif

%if %{with subpackages}
%files sql-devel
%{_bindir}/dbsql
%{_libdir}/libdb_sql.so
%{_includedir}/%{name}/dbsql.h
%endif

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-66
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-65
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 16 2024 Filip Janus <fjanus@redhat.com> - 5.3.28-64
- Rebase db_converter to the latest upstream version

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-63
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Ales Nezbeda <anezbeda@redhat.com> - 5.3.28-62
- Fix BZ#1817751 - Compile with PIE flag

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Florian Weimer <fweimer@redhat.com> - 5.3.28-59
- Additional C compatibility fixes (#2152303)

* Fri Sep 08 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.3.28-58
- Re-enable subpackages in RHEL builds

* Tue Aug 29 2023 Filip Janus <fjanus@redhat.com> - 5.3.25-57
- Add convert-util subpackage
- It allowes to convert BerkeleyDB database format to GDBM/LMDB format
- Disable shiping libdb for rhel except convert-tool

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 10 2022 Florian Weimer <fweimer@redhat.com> - 5.3.28-54
- Various changes to improve C99 compatibility (#2152303)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-53
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 02 2022 Filip Janus <fjanus@redhat.com> - 5.3.28-52
- Marked package as deprecated

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 16 2021 Filip Januš <fjanus@redhat.com> - 5.3.29-50
- Fix mistake in patch 41

* Wed Sep 15 2021 Filip Januš <fjanus@redhat.com> - 5.3.28-49
- Improve previous (patch 41) to cover more cases

* Mon Sep 13 2021 Filip Januš <fjanus@redhat.com> - 5.3.28-48
- Bad order of sys calls cause high CPU usage
- Related: #1992402
- Patch no. 41 was added

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 Matej Mužila <mmuzila@redhat.com> 5.3.28-45
- Resolves: CVE-2019-2708 (#1853243)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Tom Stellard <tstellar@redhat.com> - 5.3.28-43
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 14 2020 Ondrej Dubaj <odubaj@redhat.com> - 5.3.28-42
- Remove java subpackage due to jdk-11 (#1846398)

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 5.3.28-41
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 22 2019 Petr Kubat <pkubat@redhat.com> 5.3.28-39
- Set correct tcl-devel version for BuildRequires (#1712532)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Petr Kubat <pkubat@redhat.com> 5.3.28-36
- Optimize trickle thread CPU usage (#1608749)

* Wed Jan 16 2019 Petr Kubat <pkubat@redhat.com> - 5.3.28-35
- Add patch to workaround issues on large systems (>1024 CPU)
  Resolves: #1245410

* Wed Sep 05 2018 Petr Kubat <pkubat@redhat.com> - 5.3.28-34
- Add patch for CDB race issue (#1099509)

* Tue Jul 24 2018 Petr Kubat <pkubat@redhat.com> - 5.3.28-33
- Add BuildRequires for gcc and gcc-c++ (#1604566)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 23 2018 Petr Kubat <pkubat@redhat.com> - 5.3.28-31
- Rename __atomic_compare_exchange to not clash with gcc built-in

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 31 2017 Petr Kubat <pkubat@redhat.com> 5.3.28-29
- Fix deadlocks when reading/writing off-page duplicate tree (#1349779)

* Tue Oct 24 2017 Petr Kubat <pkubat@redhat.com> 5.3.28-28
- Run a number of quick subsystem checks on build

* Thu Sep 07 2017 Petr Kubat <pkubat@redhat.com> 5.3.28-27
- Fail properly when encountering removed or 0-byte regions (#1471011)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Petr Kubat <pkubat@redhat.com> - 5.3.28-24
- Fix some defects found by covscan

* Mon Jun 26 2017 Petr Kubat <pkubat@redhat.com> - 5.3.28-23
- Try looking at env lock via /proc/locks during env_attach (#1460003)
- Check rpm's transaction lock via /proc/locks
- Do not access DB_CONFIG when db_home is not set (#1464033)

* Tue Jun 13 2017 Petr Kubat <pkubat@redhat.com> - 5.3.28-23
- Reintroduce patches removed in 5.3.28-22
- Modify upstream patch to fail on pthread version mismatch (#1460003)

* Fri Jun 09 2017 Adam Williamson <awilliam@redhat.com> - 5.3.28-22
- Drop rhbz#1394862 patches again, DB corruption still being reported

* Thu Jun 01 2017 Petr Kubat <pkubat@redhat.com> - 5.3.28-21
- Reintroduce upstream patch for rhbz#1394862
- Do not rebuild rpm's environment during a rpm transaction

* Fri May 26 2017 Adam Williamson <awilliam@redhat.com> - 5.3.28-20
- Drop rhbz#1394862 patch for now, it has serious issues

* Wed May 24 2017 Petr Kubat <pkubat@redhat.com> - 5.3.28-19
- Fix some issues present in the upstream patch for rhbz#1394862

* Tue May 23 2017 Adam Williamson <awilliam@redhat.com> - 5.3.28-18
- Fix issue causing RPM to hang when glibc/libpthread change (#1394862)

* Wed Feb 22 2017 Petr Kubat <pkubat@redhat.com> - 5.3.28-17
- Fix overflowing integer in bundled-in lemon.c (#1423842)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Petr Kubat <pkubat@redhat.com> 5.3.28-16
- Add man pages for libdb-utils

* Mon Nov 14 2016 Petr Kubat <pkubat@redhat.com> 5.3.28-15
- Fix mutexes not being released properly (#1272680)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.28-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.28-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Jan Stanek <jstanek@redhat.com> - 5.3.28-12
- Add upstream patch for a memp_stat issue.
- Resolves: rhbz#1211871

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.3.28-11
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 5.3.28-10
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.28-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 5.3.28-8
- fix license handling

* Mon Jul 14 2014 Jakub Čajka <jcajka@redhat.com> - 5.3.28-7
- Fixed build with Java 8

* Tue Jun 10 2014 Jan Stanek <jstanek@redhat.com> - 5.3.28-6
- Fixed search path for new tcl, new BuildRequires for zlib

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Feb 22 2014 Peter Robinson <pbrobinson@fedoraproject.org> 5.3.28-4
- Add some of the previous aarch64 bits back as the sub configure don't use the macro

* Sun Jan 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 5.3.28-3
- Fix configure macro usage for better aarch64 build fix

* Wed Nov 06 2013 Jan Stanek <jstanek@redhat.com> - 5.3.28-2
- Updated config files to allow build on aarch64 (#1022970)

* Tue Oct 08 2013 Jan Stanek <jstanek@redhat.com> - 5.3.28-1
- Added Sleepycat to the license list (#1013841)
- Updated to 5.3.28 (#1013233)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.21-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Tom Callaway <spot@fedoraproject.org> - 5.3.21-12
- add copy of lgpl-2.1.txt

* Thu May 16 2013 Jan Stanek <jstanek@redhat.com> - 5.3.21-11
- Fix missing debuginfo issue for utils subpackage

* Thu May  9 2013 Tom Callaway <spot@fedoraproject.org> - 5.3.21-10
- add license clarification fix

* Wed Apr 03 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-9
- Added sqlite compability CFLAGS (#788496)

* Wed Mar 27 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-8
- Cleaning the specfile - removed gcc-java dependecy other way

* Wed Mar 27 2013 Jan Stanek <jstanek@redhat.com> 5.3.21-7
- Removed dependency on obsolete gcc-java package (#927742)

* Thu Mar  7 2013 Jindrich Novy <jnovy@redhat.com> 5.3.21-6
- add LGPLv2+ and remove Sleepycat in license tag (#886838)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tom Callaway <spot@fedoraproject.org> - 5.3.21-4
- fix license tag

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 5.3.21-2
- Specify tag for libtool (fixes FTBFS # 838334 )

* Thu Jul  5 2012 Jindrich Novy <jnovy@redhat.com> 5.3.21-1
- update to 5.3.21
http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_3.html

* Tue Jul  3 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-5
- move C++ header files to cxx-devel

* Tue Jul  3 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-4
- fix -devel packages dependencies yet more (#832225)

* Sun May  6 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-3
- package -devel packages correctly

* Sat Apr 21 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-2
- fix multiarch conflict in libdb-devel (#812901)
- remove unneeded dos2unix BR

* Thu Mar 15 2012 Jindrich Novy <jnovy@redhat.com> 5.3.15-1
- update to 5.3.15
  http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_3.html

* Fri Feb 17 2012 Deepak Bhole <dbhole@redhat.com> 5.2.36-5
- Resolves rhbz#794472
- Patch from Omair Majid <omajid@redhat.com> to remove explicit Java 6 req.

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 5.2.36-4
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 5.2.36-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 15 2011 Jindrich Novy <jnovy@redhat.com> 5.2.36-1
- update to 5.2.36,
  http://download.oracle.com/otndocs/products/berkeleydb/html/changelog_5_2.html#id3647664

* Wed Jun 15 2011 Jindrich Novy <jnovy@redhat.com> 5.2.28-2
- move development documentation to devel-doc subpackage (#705386)

* Tue Jun 14 2011 Jindrich Novy <jnovy@redhat.com> 5.2.28-1
- update to 5.2.28

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Jindrich Novy <jnovy@redhat.com> 5.1.25-1
- update to 5.1.25

* Wed Sep 29 2010 jkeating - 5.1.19-2
- Rebuilt for gcc bug 634757

* Fri Sep 10 2010 Jindrich Novy <jnovy@redhat.com> 5.1.19-1
- update to 5.1.19
- rename -devel-static to -static subpackage (#617800)
- build java on all arches

* Wed Jul  7 2010 Jindrich Novy <jnovy@redhat.com> 5.0.26-1
- update to 5.0.26
- drop BR: ed

* Thu Jun 17 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-2
- add Requires: libdb-cxx to libdb-devel

* Wed Apr 21 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-1
- initial build

* Thu Apr 15 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-0.2
- remove C# documentation
- disable/remove rpath
- fix description
- tighten dependencies
- run ldconfig for cxx and sql subpackages

* Fri Apr  9 2010 Jindrich Novy <jnovy@redhat.com> 5.0.21-0.1
- enable sql
- package 5.0.21
