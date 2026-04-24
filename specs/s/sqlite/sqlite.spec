# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# bcond default logic is nicely backwards...
%bcond_without tcl
%bcond_without sqldiff
%bcond_with static
%bcond_without check

%define majorver 3
%define realver 3500200
%define docver 3500200
%define rpmver 3.50.2
%define year 2025

Summary: Library that implements an embeddable SQL database engine
Name: sqlite
Version: %{rpmver}
Release: 3%{?dist}
License: blessing
URL: http://www.sqlite.org/

Source0: http://www.sqlite.org/%{year}/sqlite-src-%{realver}.zip
Source1: http://www.sqlite.org/%{year}/sqlite-doc-%{docver}.zip
Source2: http://www.sqlite.org/%{year}/sqlite-autoconf-%{realver}.tar.gz
# Support a system-wide lemon template
Patch1: sqlite-3.6.23-lemon-system-template.patch
Patch2: sqlite-3.49.0-fix-lemon-missing-cflags.patch

BuildRequires: make
BuildRequires: gcc gcc-c++
BuildRequires: ncurses-devel readline-devel glibc-devel
BuildRequires: autoconf
BuildRequires: /usr/bin/tclsh
BuildRequires: zlib-ng-compat-devel
BuildRequires: chrpath
%if %{with tcl}
BuildRequires: tcl-devel
%{!?tcl_version: %global tcl_version 9.0}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%endif

Requires: %{name}-libs = %{version}-%{release}
Provides: %{name}3 = %{version}-%{release}

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1

%description
SQLite is a C library that implements an SQL database engine. A large
subset of SQL92 is supported. A complete database is stored in a
single disk file. The API is designed for convenience and ease of use.
Applications that link against SQLite can enjoy the power and
flexibility of an SQL database without the administrative hassles of
supporting a separate database server. Version 2 and version 3 binaries
are named to permit each to be installed on a single host

SQLite is built with some non-default settings:
- Additional APIs for table's and query's metadata are enabled 
  (SQLITE_ENABLE_COLUMN_METADATA)
- Directory syncs are disabled (SQLITE_DISABLE_DIRSYNC)
- `secure_delete` defaults to 'on', so deleted content is overwritten
  with zeros (SQLITE_SECURE_DELETE)
- `sqlite3_unlock_notify()` is enabled - this feature allows to register a 
  callback that's invoked when lock is removed (SQLITE_ENABLE_UNLOCK_NOTIFY)
- `dbstat` virtual table with disk space usage is enabled
- `dbpage` virtual table providing direct access to underlying database file
  is enabled (SQLITE_ENABLE_DBPAGE_VTAB)
- Threadsafe mode is set to 1 - Serialized, so it is safe to use in a 
  multithreaded environment (SQLITE_THREADSAFE=1)
- FTS3, FTS4 and FTS5 are enabled so versions 3 to 5 of the full-text search
  engine are available (SQLITE_ENABLE_FTS3, SQLITE_ENABLE_FTS4, 
  SQLITE_ENABLE_FTS5)
- Pattern parser in FTS3 extension supports nested parenthesis and operators
  `AND`, `OR` (SQLITE_ENABLE_FTS3_PARENTHESIS)
- R*Tree index extension is enabled (SQLITE_ENABLE_RTREE)
- Extension loading is enabled
- Sessions (sqlite-session feature) is enabled
- Preupdate hook is enabled

It is also important to note that shell has some extensions as its dependencies,
so some extensions are enabled by default in SQLite shell, but not in the system
libraries. Only the aforementioned extensions are available in the libraries:
FTS3, FTS4, FTS5, R*Tree


%package devel
Summary: Development tools for the sqlite3 embeddable SQL database engine
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and development documentation 
for %{name}. If you like to develop programs using %{name}, you will need 
to install %{name}-devel.

%package libs
Summary: Shared library for the sqlite3 embeddable SQL database engine.

# Ensure updates from pre-split work on multi-lib systems
Obsoletes: %{name} < 3.11.0-1
Conflicts: %{name} < 3.11.0-1

%description libs
This package contains the shared library for %{name}.

%package doc
Summary: Documentation for sqlite
BuildArch: noarch

%description doc
This package contains most of the static HTML files that comprise the
www.sqlite.org website, including all of the SQL Syntax and the 
C/C++ interface specs and other miscellaneous documentation.

%package -n lemon
Summary: A parser generator

%description -n lemon
Lemon is an LALR(1) parser generator for C or C++. It does the same
job as bison and yacc. But lemon is not another bison or yacc
clone. It uses a different grammar syntax which is designed to reduce
the number of coding errors. Lemon also uses a more sophisticated
parsing engine that is faster than yacc and bison and which is both
reentrant and thread-safe. Furthermore, Lemon implements features
that can be used to eliminate resource leaks, making is suitable for
use in long-running programs such as graphical user interfaces or
embedded controllers.


%package debug
Summary: SQLite shell configured for development and debugging purposes

%description debug
This version of SQLite shell contains features that are useful for
debugging purposes. These features are not present in a normal SQLite shell
because some have negative impact on a non-developer user experience.

Current list of modification from normal SQLite shell (in sqlite package):
- Ability to enable .scanstats for metrics regarding query speeds


%if %{with sqldiff}
%package tools
Summary: %{name} tools
Group: Development/Tools

%description tools
%{name} related tools. Currently contains only sqldiff.
- sqldiff: The sqldiff binary is a command-line utility program
  that displays the differences between SQLite databases.
%endif

%if %{with tcl}
%package tcl
Summary: Tcl module for the sqlite3 embeddable SQL database engine
Requires: %{name} = %{version}-%{release}
Requires: tcl(abi) = %{tcl_version}

%description tcl
This package contains the tcl modules for %{name}.

%package analyzer
Summary: An analysis program for sqlite3 database files
Requires: %{name} = %{version}-%{release}
Requires: tcl(abi) = %{tcl_version}

%description analyzer
This package contains the analysis program for %{name}.
%endif

%prep
%setup -q -a1 -n %{name}-src-%{realver}
%patch -P 1 -p1
%patch -P 2 -p1

# The atof test is failing on the i686 architecture, when binary configured with
# --enable-rtree option. Failing part is text->real conversion and
# text->real->text conversion in lower significant values after decimal point in a number.
# func4 tests fail for i686 on float<->int conversions.
%ifarch == i686
rm test/atof1.test
rm test/func4.test
%endif

# Remove backup-file
rm -f %{name}-doc-%{docver}/sqlite.css~ || :

#autoupdate
#autoconf # Rerun with new autoconf to add support for aarm64

%build
# First build executable for debug subpackage
# following CFLAGS are not possible to set via the configure script
export CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS \
               -DSQLITE_ENABLE_COLUMN_METADATA=1 \
               -DSQLITE_DISABLE_DIRSYNC=1 \
               -DSQLITE_SECURE_DELETE=1 \
               -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
               -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 \
               -DSQLITE_ENABLE_STMT_SCANSTATUS \
               -DSQLITE_ENABLE_DBPAGE_VTAB \
               -DSQLITE_ENABLE_SESSION \
               -DSQLITE_ENABLE_PREUPDATE_HOOK \
               -Wall -fno-strict-aliasing"

%configure %{!?with_tcl:--disable-tcl} \
           --enable-rtree \
           --enable-fts3 \
           --enable-fts4 \
           --enable-fts5 \
           --enable-threadsafe \
           --enable-load-extension \
           --soname=legacy \
           --disable-static

%make_build

mv sqlite3 sqlite3-debug

make clean

# Now rebuild rest of the packages normally
export CFLAGS="$RPM_OPT_FLAGS $RPM_LD_FLAGS \
               -DSQLITE_ENABLE_COLUMN_METADATA=1 \
               -DSQLITE_DISABLE_DIRSYNC=1 \
               -DSQLITE_SECURE_DELETE=1 \
               -DSQLITE_ENABLE_UNLOCK_NOTIFY=1 -DSQLITE_ENABLE_DBSTAT_VTAB=1 \
               -DSQLITE_ENABLE_FTS3_PARENTHESIS=1 \
               -DSQLITE_ENABLE_DBPAGE_VTAB \
               -DSQLITE_ENABLE_SESSION \
               -DSQLITE_ENABLE_PREUPDATE_HOOK \
               -Wall -fno-strict-aliasing"

%configure %{!?with_tcl:--disable-tcl} \
           --enable-rtree \
           --enable-fts3 \
           --enable-fts4 \
           --enable-fts5 \
           --enable-threadsafe \
           --enable-load-extension \
           --soname=legacy \
           --disable-static

%make_build

# Build sqlite3_analyzer
# depends on tcl
%if %{with tcl}
%make_build sqlite3_analyzer
%endif

# Build sqldiff
%if %{with sqldiff}
%make_build sqldiff
%endif

%install
mkdir -p ${RPM_BUILD_ROOT}%{tcl_sitearch}
%make_install

install -D -m0644 sqlite3.1 $RPM_BUILD_ROOT/%{_mandir}/man1/sqlite3.1
install -D -m0755 lemon $RPM_BUILD_ROOT/%{_bindir}/lemon
install -D -m0644 tool/lempar.c $RPM_BUILD_ROOT/%{_datadir}/lemon/lempar.c
install -D -m0755 sqlite3-debug $RPM_BUILD_ROOT/%{_bindir}/sqlite3-debug

%if %{with tcl}
# fix up permissions to enable dep extraction
install -d $RPM_BUILD_ROOT%{tcl_sitearch}
mv $RPM_BUILD_ROOT%{_datadir}/tcl%{tcl_version}/sqlite* $RPM_BUILD_ROOT%{tcl_sitearch}/
chmod 0755 ${RPM_BUILD_ROOT}/%{tcl_sitearch}/sqlite%{majorver}/*.so
# Install sqlite3_analyzer
install -D -m0755 sqlite3_analyzer $RPM_BUILD_ROOT/%{_bindir}/sqlite3_analyzer
%endif

# Install sqldiff
%if %{with sqldiff}
install -D -m0755 sqldiff $RPM_BUILD_ROOT/%{_bindir}/sqldiff
%endif

%if ! %{with static}
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.{la,a}
%endif

# This is needed since rpath removal using sed won't work for tcl library for some reason
chrpath --delete $RPM_BUILD_ROOT/%{tcl_sitearch}/sqlite%{majorver}/*.so
chrpath --delete $RPM_BUILD_ROOT/%{_libdir}/*.so.%{version}

chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/sqlite3
chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/sqlite3-debug
chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/sqldiff
chrpath --delete $RPM_BUILD_ROOT/%{_bindir}/sqlite3_analyzer

%if %{with check}
%check
# XXX shell tests are broken due to loading system libsqlite3, work around...
export LD_LIBRARY_PATH=`pwd`/.libs
export MALLOC_CHECK_=3

# csv01 hangs on all non-intel archs i've tried
%ifarch x86_64 %{ix86}
%else
rm test/csv01.test
%endif

make test
%endif
# ends %%{with check} if

%ldconfig_scriptlets libs

%files
%{_bindir}/sqlite3
%{_mandir}/man?/*

%files libs
%doc README.md
%{_libdir}/*.so.%{version}
%{_libdir}/*.so.0

%files devel
%{_includedir}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%if %{with static}
%{_libdir}/*.a
%exclude %{_libdir}/*.la
%endif

%files doc
%doc %{name}-doc-%{docver}/*

%files -n lemon
%{_bindir}/lemon
%{_datadir}/lemon

%files debug
%{_bindir}/sqlite3-debug

%if %{with tcl}
%files tcl
%{tcl_sitearch}/sqlite%{majorver}

%if %{with sqldiff}
%files tools
%{_bindir}/sqldiff
%endif

%files analyzer
%{_bindir}/sqlite3_analyzer
%endif

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.50.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jun 28 2025 Packit <hello@packit.dev> - 3.50.2-1
- Update to version 3.50.2
- Resolves: rhbz#2370851

* Thu May 29 2025 Packit <hello@packit.dev> - 3.50.0-1
- Update to version 3.50.0
- Resolves: rhbz#2369200

* Wed May 21 2025 Packit <hello@packit.dev> - 3.49.2-1
- Update to version 3.49.2
- Resolves: rhbz#2364695

* Thu Mar 06 2025 Packit <hello@packit.dev> - 3.49.1-1
- Update to version 3.49.1
- Resolves: rhbz#2346264

* Thu Feb 6 2025 Ales Nezbeda <anezbeda@redhat.com> 3.49.0-1
- Update to 3.49.0
- https://www.sqlite.org/releaselog/3_49_0.html
- Resolves: rhbz#2337596

* Wed Feb 5 2025 Ales Nezbeda <anezbeda@redhat.com> - 3.48.0-1
- Update to 3.48.0
- https://www.sqlite.org/releaselog/3_48_0.html
- Resolves: rhbz#2337596

* Thu Jan 16 2025 Ales Nezbeda <anezbeda@redhat.com> - 3.47.2-2
- Enabled sqlite-session feature

* Mon Dec 9 2024 Ales Nezbeda <anezbeda@redhat.com> - 3.47.2-1
- Update to 3.47.2
- https://www.sqlite.org/releaselog/3_47_2.html
- Resolves: rhbz#2330986

* Tue Nov 26 2024 Ales Nezbeda <anezbeda@redhat.com> - 3.47.1-1
- Update to 3.47.1
- https://www.sqlite.org/releaselog/3_47_1.html
- Resolves: rhbz#2328654

* Wed Oct 23 2024 Ales Nezbeda <anezbeda@redhat.com> - 3.47.0-1
- Update to 3.47.0
- https://www.sqlite.org/releaselog/3_47_0.html
- Resolves: rhbz#2320418

* Tue Aug 13 2024 Ales Nezbeda <anezbeda@redhat.com> - 3.46.1-1
- Update to 3.46.1
- https://www.sqlite.org/releaselog/3_46_1.html

* Thu Aug 1 2024 Ales Nezbeda <anezbeda@redhat.com> - 3.46.0-4
- Adds used non-default options in compilation to the package
  description
- Fixes BZ:2296651

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.46.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Ales Nezbeda <anezbeda@redhat.com> - 3.46.0-2
- Add new -debug subpackage for development and debugging purposes

* Wed Jun 5 2024 Ales Nezbeda <anezbeda@redhat.com> - 3.46.0-1
- Updated to version 3.46.0 (https://sqlite.org/releaselog/3_46_0.html)

* Thu Apr 25 2024 Zuzana Miklankova <zmiklank@redhat.com> - 3.45.3-1
- Updated to version 3.45.3 (https://sqlite.org/releaselog/3_45_3.html)

* Tue Mar 12 2024 Zuzana Miklankova <zmiklank@redhat.com> - 3.45.2-1
- Updated to version 3.45.2 (https://sqlite.org/releaselog/3_45_2.html)

* Fri Feb 02 2024 Zuzana Miklankova <zmiklank@redhat.com> - 3.45.1-2
- bump changelog number to match real release number.

* Wed Jan 31 2024 Zuzana Miklankova <zmiklank@redhat.com> - 3.45.1-1
- Updated to version 3.45.1 (https://sqlite.org/releaselog/3_45_1.html)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.45.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Zuzana Miklankova <zmiklank@redhat.com> - 3.45.0-1
- Updated to version 3.45.0 (https://sqlite.org/releaselog/3_45_0.html)
- List versioned soname in files, preventing unnoticed soname bumps
- Disable func4 tests for i686 arch due to failing float<->int conversions

* Thu Dec 07 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.44.2-1
- Updated to version 3.44.2 (https://sqlite.org/releaselog/3_44_2.html)

* Thu Nov 23 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.44.1-1
- Updated to version 3.44.1 (https://sqlite.org/releaselog/3_44_1.html)

* Wed Nov 01 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.44.0-1
- Updated to version 3.44.0 (https://sqlite.org/releaselog/3_44_0.html)

* Mon Oct 23 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.43.2-1
- Updated to version 3.43.2 (https://sqlite.org/releaselog/3_43_2.html)

* Tue Sep 12 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.43.1-1
- Updated to version 3.43.1 (https://sqlite.org/releaselog/3_43_1.html)

* Mon Aug 28 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.43.0-1
- Updated to version 3.43.0 (https://sqlite.org/releaselog/3_43_0.html)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.42.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.42.0-6
- remove patch5 - adjusting sync test

* Thu Jul 13 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.42.0-5
- remove patch4 - disabling datetime test

* Thu Jul 13 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.42.0-4
- remove patch3 - temporary workaround for percentile test

* Thu Jul 13 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.42.0-3
- remove patch2 - no-malloc-usable-size, #801981

* Thu Jul 13 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.42.0-2
- Updated to version 3.42.0 (https://sqlite.org/releaselog/3_42_0.html)

* Fri Jun 23 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.41.2-3
- revert to version 3.41.2 as the 3.42.0 does not correctly work with dnf

* Wed Jun 21 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.42.0-1
- Updated to version 3.42.0 (https://sqlite.org/releaselog/3_42_0.html)
- Use %%patch -P N instead of deprecated %%patchN

* Thu May 25 2023 Siddhesh Poyarekar <siddhesh@redhat.com> - 3.41.2-2
- Drop duplicate -mbranch-protection.

* Mon Mar 27 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.41.2-1
- Updated to version 3.41.2 (https://sqlite.org/releaselog/3_41_2.html)
- Migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Zuzana Miklankova <zmiklank@redhat.com> - 3.40.1-1
- Updated to version 3.40.1 (https://sqlite.org/releaselog/3_40_1.html)

* Fri Nov 18 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.40.0-1
- Updated to version 3.40.0 (https://sqlite.org/releaselog/3_40_0.html)

* Wed Oct 19 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.39.4-1
- Updated to version 3.39.4 (https://sqlite.org/releaselog/3_39_4.html)

* Tue Sep 06 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.39.3-1
- Updated to version 3.39.3 (https://sqlite.org/releaselog/3_39_3.html)

* Fri Jul 29 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.39.2-1
- Updated to version 3.39.2 (https://sqlite.org/releaselog/3_39_2.html)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.39.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.39.1-1
- Updated to version 3.39.1 (https://sqlite.org/releaselog/3_39_1.html)

* Mon Jun 27 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.39.0-1
- Updated to version 3.39.0 (https://sqlite.org/releaselog/3_39_0.html)

* Thu Jun 09 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.38.5-2
- Fix build error --without sqldiff
- Fix typo in changelog

* Mon May 09 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.38.5-1
- Updated to version 3.38.5 (https://sqlite.org/releaselog/3_38_5.html)

* Mon May 02 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.38.3-2
- add flag -mbranch-protection=standard for aarch64
- remove configure flag --enable-json1, as this is default from 3.38.0
- run autoupdate before autoconf in %%prep

* Thu Apr 28 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.38.3-1
- Updated to version 3.38.3 (https://sqlite.org/releaselog/3_38_3.html)

* Thu Apr 07 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.38.2-1
- Updated to version 3.38.2 (https://sqlite.org/releaselog/3_38_2.html)

* Wed Mar 23 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.38.1-1
- Updated to version 3.38.1 (https://sqlite.org/releaselog/3_38_1.html)

* Thu Mar 03 2022 Zuzana Miklankova <zmiklank@redhat.com> - 3.38.0-1
- Updated to version 3.38.0 (https://sqlite.org/releaselog/3_38_0.html)
- Set flags with configure script, whenever possible

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 18 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.36.0-4
- Enabled SQLITE_DBPAGE virtual table (#1973454)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.36.0-2
- Support SHA-1 algorithms in sqlite (revert)

* Thu Jul 01 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.36.0-1
- Updated to version 3.36.0 (https://sqlite.org/releaselog/3_36_0.html)

* Tue Apr 20 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.35.5-1
- Updated to version 3.35.5 (https://sqlite.org/releaselog/3_35_5.html)

* Thu Apr 15 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.35.4-3
- Remove SHA-1 algorithms according to its deprecation in RHEL-9 (#1935442)

* Wed Apr 14 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.35.4-2
- Fixed handling LIKE experrsion in WHERE clause (#1947883)

* Tue Apr 06 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.35.4-1
- Updated to version 3.35.4 (https://sqlite.org/releaselog/3_35_4.html)

* Fri Mar 26 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.35.3-1
- Updated to version 3.35.3 (https://sqlite.org/releaselog/3_35_3.html)

* Thu Mar 18 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.35.2-1
- Updated to version 3.35.2 (https://sqlite.org/releaselog/3_35_2.html)

* Tue Mar 16 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.35.1-1
- Updated to version 3.35.1 (https://sqlite.org/releaselog/3_35_1.html)

* Mon Mar 15 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.35.0-1
- Updated to version 3.35.0 (https://sqlite.org/releaselog/3_35_0.html)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.34.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Ondrej Dubaj <odubaj@redhat.com> - 3.34.1-1
- Updated to version 3.34.1 (https://sqlite.org/releaselog/3_34_1.html)

* Wed Dec 02 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.34.0-1
- Updated to version 3.34.0 (https://sqlite.org/releaselog/3_34_0.html)
- Enabled fts3conf.test on s390x and ppc64 architectures

* Fri Oct 09 2020 Sheng Mao <shngmao@gmail.com> - 3.33.0-2
- Enable FTS4 extensions (rhbz#1887106)

* Fri Aug 14 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.33.0-1
- Updated to version 3.33.0 (https://sqlite.org/releaselog/3_33_0.html)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 3.32.3-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jun 19 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.32.3-1
- Updated to version 3.32.3 (https://sqlite.org/releaselog/3_32_3.html)

* Fri Jun 05 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.32.2-1
- Updated to version 3.32.2 (https://sqlite.org/releaselog/3_32_2.html)

* Tue May 26 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.32.1-1
- Updated to version 3.32.1 (https://sqlite.org/releaselog/3_32_1.html)

* Mon May 25 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.32.0-1
- Updated to version 3.32.0 (https://sqlite.org/releaselog/3_32_0.html)

* Wed Feb 05 2020 Ondrej Dubaj <odubaj@redhat.com> - 3.31.1-1
- Updated to version 3.31.1 (https://sqlite.org/releaselog/3_31_1.html)
- updated spec file, deleted useless patches
- Resolved s390 arch incompatibility
- Modified FTS tests to support big endian platforms

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.30.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Petr Kubat <pkubat@redhat.com> - 3.30.1-3
- introduce sqlite-tools package

* Thu Jan  9 2020 Tom Callaway <spot@fedoraproject.org> - 3.30.1-2
- apply upstream fix for CVE-2019-19926 (bz1789441)

* Mon Oct 14 2019 Petr Kubat <pkubat@redhat.com> - 3.30.1-1
- Updated to version 3.30.1 (https://sqlite.org/releaselog/3_30_1.html)

* Mon Oct 07 2019 Ondrej Dubaj <odubaj@redhat.com> - 3.30.0-1
- Updated to version 3.30.0 (https://sqlite.org/releaselog/3_30_0.html)
- updated spec file, deleted useless patches

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Petr Kubat <pkubat@redhat.com> - 3.29.0-1
- Updated to version 3.29.0 (https://sqlite.org/releaselog/3_29_0.html)
- Remove stupid-openfiles-test patch as the upstream test should now
  work properly even on systems with larger number of file descriptors
  Related: https://sqlite.org/src/info/a27b0b880d76c683

* Mon May 13 2019 Petr Kubat <pkubat@redhat.com> - 3.28.0-1
- Updated to version 3.28.0 (https://sqlite.org/releaselog/3_28_0.html)

* Thu Feb 28 2019 Petr Kubat <pkubat@redhat.com> - 3.27.2-1
- Updated to version 3.27.2 (https://sqlite.org/releaselog/3_27_2.html)

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.0-3
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Dec 12 2018 Petr Kubat <pkubat@redhat.com> - 3.26.0-1
- Updated to version 3.26.0 (https://sqlite.org/releaselog/3_26_0.html)

* Thu Oct 11 2018 Petr Kubat <pkubat@redhat.com> - 3.25.2-1
- Updated to version 3.25.2 (https://sqlite.org/releaselog/3_25_2.html)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 05 2018 Petr Kubat <pkubat@redhat.com> - 3.24.0-1
- Updated to version 3.24.0 (https://sqlite.org/releaselog/3_24_0.html)

* Wed Apr 11 2018 Petr Kubat <pkubat@redhat.com> - 3.23.1-1
- Updated to version 3.23.1 (https://sqlite.org/releaselog/3_23_1.html)

* Tue Apr 03 2018 Petr Kubat <pkubat@redhat.com> - 3.23.0-1
- Updated to version 3.23.0 (https://sqlite.org/releaselog/3_23_0.html)

* Wed Mar 21 2018 Petr Kubat <pkubat@redhat.com> - 3.22.0-4
- Fixed CVE-2018-8740 (#1558809)

* Fri Feb  9 2018 Florian Weimer <fweimer@redhat.com> - 3.22.0-3
- Use LDFLAGS from redhat-rpm-config for building lemon, too

* Mon Feb 05 2018 Petr Kubat <pkubat@redhat.com> - 3.22.0-2
- Fixed issue with some walro2 tests failing on ppc64

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.22.0-2
- Switch to %%ldconfig_scriptlets

* Thu Jan 25 2018 Petr Kubat <pkubat@redhat.com> - 3.22.0-1
- Fixed issue with some e_expr tests failing i686
- Fixed issue with a fts3rank test failing on big-endian systems

* Tue Jan 23 2018 Petr Kubat <pkubat@redhat.com> - 3.22.0-1
- Updated to version 3.22.0 (https://sqlite.org/releaselog/3_22_0.html)

* Wed Nov 01 2017 Petr Kubat <pkubat@redhat.com> - 3.21.0-1
- Updated to version 3.21.0 (https://sqlite.org/releaselog/3_21_0.html)

* Mon Aug 28 2017 Petr Kubat <pkubat@redhat.com> - 3.20.1-1
- Updated to version 3.20.1 (https://sqlite.org/releaselog/3_20_1.html)

* Tue Aug 22 2017 Kalev Lember <klember@redhat.com> - 3.20.0-2
- Build with --enable-fts5

* Wed Aug 02 2017 Petr Kubat <pkubat@redhat.com> - 3.20.0-1
- Updated to version 3.20.0 (https://sqlite.org/releaselog/3_20_0.html)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Petr Kubat <pkubat@redhat.com> - 3.19.3-1
- Updated to version 3.19.3 (https://sqlite.org/releaselog/3_19_3.html)
- Better detection of CVE-2017-10989 (#1469673)

* Thu May 25 2017 Petr Kubat <pkubat@redhat.com> - 3.19.1-1
- Updated to version 3.19.1 (https://sqlite.org/releaselog/3_19_1.html)

* Mon Apr 03 2017 Petr Kubat <pkubat@redhat.com> - 3.18.0-1
- Updated to version 3.18.0 (https://sqlite.org/releaselog/3_18_0.html)
- Modify sync2.test to pass with DIRSYNC turned off

* Thu Mar 02 2017 Petr Kubat <pkubat@redhat.com> - 3.17.0-2
- Rebuild using newest gcc (#1428286)

* Tue Feb 21 2017 Petr Kubat <pkubat@redhat.com> - 3.17.0-1
- Updated to version 3.17.0 (https://sqlite.org/releaselog/3_17_0.html)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.16.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.16.2-2
- Rebuild for readline 7.x

* Sat Jan  7 2017 Jakub Dorňák <jakub.dornak@misli.cz> - 3.16.2-1
- Updated to version 3.16.2 (https://sqlite.org/releaselog/3_16_2.html)

* Wed Jan  4 2017 Jakub Dorňák <jakub.dornak@misli.cz> - 3.16.1-1
- Updated to version 3.16.1 (https://sqlite.org/releaselog/3_16_1.html)

* Tue Jan  3 2017 Jakub Dorňák <jakub.dornak@misli.cz> - 3.16.0-1
- Updated to version 3.16.0 (https://sqlite.org/releaselog/3_16_0.html)

* Wed Sep 21 2016 Jakub Dorňák <jdornak@redhat.com> - 3.14.2-1
- Updated to version 3.14.2 (https://sqlite.org/releaselog/3_14_2.html)

* Mon Aug 15 2016 Jakub Dorňák <jdornak@redhat.com> - 3.14.1-1
- Updated to version 3.14.1 (https://sqlite.org/releaselog/3_14_1.html)

* Tue May 24 2016 Jakub Dorňák <jdornak@redhat.com> - 3.13.0-1
- Updated to version 3.13.0 (https://sqlite.org/releaselog/3_13_0.html)

* Mon Apr 25 2016 Jakub Dorňák <jdornak@redhat.com> - 3.12.2-1
- Updated to version 3.12.2 (https://sqlite.org/releaselog/3_12_2.html)

* Wed Mar 02 2016 Jan Stanek <jstanek@redhat.com> - 3.11.0-3
- Release bump for #1312506

* Tue Feb 23 2016 Nils Philippsen <nils@redhat.com> - 3.11.0-2
- add obsoletes/conflicts to make updates on multi-lib systems work (#1310441)
- make -devel package depend on arch-specific -libs (not main) package

* Wed Feb 17 2016 Jan Stanek <jstanek@redhat.com> - 3.11.0-1
- Updated to version 3.11.0 (https://sqlite.org/releaselog/3_11_0.html)

* Mon Feb 08 2016 Jan Stanek <jstanek@redhat.com> - 3.10.2-3
- Split the shared libraries to standalone subpackage

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Jan Stanek <jstanek@redhat.com> - 3.10.2-1
- Updated to version 3.10.2 (http://sqlite.org/releaselog/3_10_2.html)
- Enabled JSON1 Extension (rhbz#1277387)
- Made test failure nonfatal on MIPS (rhbz#1294888)

* Wed Jan 13 2016 Jan Stanek <jstanek@redhat.com> - 3.10.0-1
- Updated to version 3.10.0 (http://sqlite.org/releaselog/3_10_0.html)

* Mon Dec 21 2015 Jan Stanek <jstanek@redhat.com> - 3.9.2-1
- Updated to version 3.9.2 (http://sqlite.org/releaselog/3_9_2.html)

* Thu Dec 10 2015 Jan Stanek <jstanek@redhat.com> - 3.9.0-2
- Add autoconf amalgamation for stage2 builds.

* Thu Oct 15 2015 Jan Stanek <jstanek@redhat.com> - 3.9.0-1
- Updated to version 3.9.0 (https://sqlite.org/releaselog/3_9_0.html)

* Tue Sep 22 2015 Jan Stanek <jstanek@redhat.com> - 3.8.11.1-1
- Updated to version 3.8.11.1

* Tue Jul 28 2015 Jan Stanek <jstanek@redhat.com> - 3.8.11-1
- Updated to version 3.8.11 (https://sqlite.org/releaselog/3_8_11.html)

* Fri Jun 19 2015 Jan Stanek <jstanek@redhat.com> - 3.8.10.2-3
- Enabled SQLITE_ENABLE_FTS3_PARENTHESIS extension (rhbz#1232301)

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Jan Stanek <jstanek@redhat.com> - 3.8.10.2-1
- Updated to version 3.8.10.2 (https://sqlite.org/releaselog/3_8_10_2.html)

* Mon May 18 2015 Jan Stanek <jstanek@redhat.com> - 3.8.10.1-1
- Updated to version 3.8.10.1 (https://www.sqlite.org/releaselog/3_8_10_1.html)

* Tue Apr 14 2015 Jan Stanek <jstanek@redhat.com> - 3.8.9-1
- Updated to version 3.8.9 (https://www.sqlite.org/releaselog/3_8_9.html)

* Thu Feb 26 2015 Jan Stanek <jstanek@redhat.com> - 3.8.8.3-1
- Updated to version 3.8.8.3 (https://sqlite.org/releaselog/3_8_8_3.html)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.8.8-3
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb 03 2015 Jan Stanek <jstanek@redhat.com> - 3.8.8-2
- Fixed out-of-date source URLs (rhbz#1188092)

* Tue Jan 20 2015 Jan Stanek <jstanek@redhat.com> - 3.8.8-1
- Updated to version 3.8.8 (https://sqlite.org/releaselog/3_8_8.html)
- Recreated patches to work on current version.

* Fri Dec 12 2014 Jan Stanek <jstanek@redhat.com> - 3.8.7.4-1
- Updated to version 3.8.7.4 (http://www.sqlite.org/releaselog/3_8_7_4.html)

* Tue Nov 25 2014 Jan Stanek <jstanek@redhat.com> - 3.8.7.2-1
- Updated to version 3.8.7.2 (http://sqlite.org/releaselog/3_8_7_2.html)

* Tue Oct 21 2014 Jan Stanek <jstanek@redhat.com> - 3.8.7-1
- Updated to version 3.8.7 (http://sqlite.org/releaselog/3_8_7.html)
- Dropped patch for problem fixed upstream

* Tue Aug 19 2014 Jan Stanek <jstanek@redhat.com> - 3.8.6-2
- Added auto-selection of Tcl version based on Fedora version

* Tue Aug 19 2014 Jan Stanek <jstanek@redhat.com> - 3.8.6-1
- Updated to version 3.8.6 (http://www.sqlite.org/releaselog/3_8_6.html)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.8.5-2
- Re-enable tests on aarch64 now they pass again

* Tue Jun 10 2014 Jan Stanek <jstanek@redhat.com> - 3.8.5-1
- Update to version 3.8.5 (http://www.sqlite.org/releaselog/3_8_5.html)
- Dropped patch already included upstream

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.8.4.3-4
- Don't make tests fail the build on aarch64 like some of the other arches

* Wed May 28 2014 Jan Stanek <jstanek@redhat.com> - 3.8.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86 with correct tcl_version

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 3.8.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Tue Apr 29 2014 Jan Stanek <jstanek@redhat.com> - 3.8.4.3-1
- Update to version 3.8.4.3 (http://www.sqlite.org/releaselog/3_8_4_3.html)
- Changed patch for rhbz#1075889 to upstream version
  Related: #1075889

* Fri Apr 25 2014 Honza Horak <hhorak@redhat.com> - 3.8.4.2-3
- Revert part of the upstream commit dca1945aeb3fb005, since it causes
  nautilus to crash
  Related: #1075889

* Wed Apr 02 2014 Jan Stanek <jstanek@redhat.com> 3.8.4.2-2
- Added building and shipping of sqlite3_analyzer (#1007159)

* Fri Mar 28 2014 Jan Stanek <jstanek@redhat.com> 3.8.4.2-1
- Update to 3.8.4 (http://www.sqlite.org/releaselog/3_8_4_2.html)

* Tue Mar 11 2014 Jan Stanek <jstanek@redhat.com> 3.8.4-1
- Update to 3.8.4 (http://www.sqlite.org/releaselog/3_8_4.html)

* Sun Feb 23 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.8.3-2
- Re-enable check on ARM/aarch64 as failing test fixed upstream for non x86 arches
- Modernise spec

* Tue Feb 11 2014 Jan Stanek <jstanek@redhat.com> 3.8.3-1
- Update to 3.8.3 (http://www.sqlite.org/releaselog/3_8_3.html)
- Dropped man-page patch - included upstream

* Mon Jan  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.8.2-2
- Add aarch64 to all the other arch excludes for tests

* Tue Dec 10 2013 Jan Stanek <jstanek@redhat.com> - 3.8.2-1
- Update to 3.8.2 (http://www.sqlite.org/releaselog/3_8_2.html)

* Tue Nov 26 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.8.1-2
- Do not use transitive WHERE-clause constraints on LEFT JOINs (#1034714)

* Tue Oct 22 2013 Jan Stanek <jstanek@redhat.com> - 3.8.1-1
- Update to 3.8.1 (http://www.sqlite.org/releaselog/3_8_1.html)

* Thu Sep 26 2013 Jan Stanek <jstanek@redhat.com> - 3.8.0.2-4
- Removed fullversioned provides and start using full version for rpm version

* Mon Sep 23 2013 Jan Stanek <jstanek@redhat.com> - 3.8.0-3
- Added fullversioned Provides to fix broken dependency

* Mon Sep 16 2013 Jan Stanek <jstanek@redhat.com> - 3.8.0-2
- Dropped problematic percentile-2.1.50 test

* Thu Sep 05 2013 Jan Stanek <jstanek@redhat.com> - 3.8.0-1
- Update to 3.8.0.2 (http://sqlite.org/releaselog/3_8_0_2.html)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 22 2013 Jan Stanek <jstanek@redhat.com> - 3.7.17-1
- Update to 3.7.17 (http://www.sqlite.org/releaselog/3_7_17.html)

* Thu May 16 2013 Jan Stanek <jstanek@redhat.com> - 3.7.16.2-2
- Added missing options to man page (#948862)

* Mon Apr 29 2013 Jan Stanek <jstanek@redhat.com> - 3.7.16.2-1
- update to 3.7.16.2 (http://www.sqlite.org/releaselog/3_7_16_2.html)
- add support for aarch64 (rerunning autoconf) (#926568)

* Sun Mar 31 2013 Panu Matilainen <pmatilai@redhat.com> - 3.7.16.1-1
- update to 3.7.16.1 (https://www.sqlite.org/releaselog/3_7_16_1.html)

* Wed Mar 20 2013 Panu Matilainen <pmatilai@redhat.com> - 3.7.16-1
- update to 3.7.16 (http://www.sqlite.org/releaselog/3_7_16.html)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Panu Matilainen <pmatilai@redhat.com> - 3.7.15.2-1
- update to 3.7.15.2 (http://www.sqlite.org/releaselog/3_7_15_2.html)

* Thu Dec 13 2012 Panu Matilainen <pmatilai@redhat.com> - 3.7.15-1
- update to 3.7.15 (http://www.sqlite.org/releaselog/3_7_15.html)
- fix an old incorrect date in spec changelog

* Tue Nov 06 2012 Panu Matilainen <pmatilai@redhat.com> - 3.7.14.1-1
- update to 3.7.14.1 (http://www.sqlite.org/releaselog/3_7_14_1.html)

* Wed Oct 03 2012 Panu Matilainen <pmatilai@redhat.com> - 3.7.14-1
- update to 3.7.14 (http://www.sqlite.org/releaselog/3_7_14.html)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Panu Matilainen <pmatilai@redhat.com> - 3.7.13-1
- update to 3.7.13 (http://www.sqlite.org/releaselog/3_7_13.html)
- drop no longer needed savepoint relase patch

* Fri Jun 01 2012 Panu Matilainen <pmatilai@redhat.com> - 3.7.11-3
- don't abort pending queries on release of nested savepoint (#821642)

* Wed Apr 25 2012 Panu Matilainen <pmatilai@redhat.com> - 3.7.11-2
- run test-suite with MALLOC_CHECK_=3
- disable buggy malloc_usable_size code (#801981)

* Mon Mar 26 2012 Panu Matilainen <pmatilai@redhat.com> - 3.7.11-1
- update to 3.7.11 (http://www.sqlite.org/releaselog/3_7_11.html)

* Wed Mar 07 2012 Panu Matilainen <pmatilai@redhat.com> - 3.7.10-1
- update to 3.7.10 (http://www.sqlite.org/releaselog/3_7_10.html)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Panu Matilainen <pmatilai@redhat.com> - 3.7.9-1
- update to 3.7.9 (http://www.sqlite.org/releaselog/3_7_9.html)

* Fri Oct 28 2011 Panu Matilainen <pmatilai@redhat.com> - 3.7.8-1
- update to 3.7.8 (http://www.sqlite.org/releaselog/3_7_8.html)

* Wed Jul 13 2011 Panu Matilainen <pmatilai@redhat.com> - 3.7.7.1-1
- update to 3.7.7.1 (http://www.sqlite.org/releaselog/3_7_7_1.html)
- autoconf no longer needed for build, libdl check finally upstreamed

* Wed May 25 2011 Panu Matilainen <pmatilai@redhat.com> - 3.7.6.3-1
- update to 3.7.6.3 (http://www.sqlite.org/releaselog/3_7_6_3.html)

* Sat May 21 2011 Peter Robinson <pbrobinson@gmail.com> - 3.7.6.2-3
- add arm to the exclude from tests list

* Fri Apr 29 2011 Panu Matilainen <pmatilai@redhat.com> - 3.7.6.2-2
- comment out stupid tests causing very bogus build failure on koji

* Thu Apr 21 2011 Panu Matilainen <pmatilai@redhat.com> - 3.7.6.2-1
- update to 3.7.6.2 (http://www.sqlite.org/releaselog/3_7_6_2.html)

* Fri Feb 25 2011 Dennis Gilmore <dennis@ausil.us> - 3.7.5-4
- build tests on sparc expecting failures same as the other big endian arches

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 2 2011 Panu Matilainen <pmatilai@redhat.com> - 3.7.5-2
- unwanted cgi-script in docs creating broken dependencies, remove it
- make doc sub-package noarch

* Tue Feb 1 2011 Panu Matilainen <pmatilai@redhat.com> - 3.7.5-1
- update to 3.7.5 (http://www.sqlite.org/releaselog/3_7_5.html)

* Thu Dec 9 2010 Panu Matilainen <pmatilai@redhat.com> - 3.7.4-1
- update to 3.7.4 (http://www.sqlite.org/releaselog/3_7_4.html)
- deal with upstream source naming, versioning and format changing
- fixup wal2-test expections wrt SQLITE_DISABLE_DIRSYNC use

* Fri Nov 5 2010 Dan Horák <dan[at]danny.cz> - 3.7.3-2
- expect test failures also on s390x

* Mon Nov 1 2010 Panu Matilainen <pmatilai@redhat.com> - 3.7.3-1
- update to 3.7.3 (http://www.sqlite.org/releaselog/3_7_3.html)

* Thu Sep  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 3.7.0.1-2
- enable SQLITE_SECURE_DELETE, SQLITE_ENABLE_UNLOCK_NOTIFY for firefox 4

* Fri Aug 13 2010 Panu Matilainen <pmatilai@redhat.com> - 3.7.0.1-1
- update to 3.7.0.1 (http://www.sqlite.org/releaselog/3_7_0_1.html)

* Sat Jul  3 2010 Dan Horák <dan[at]danny.cz> - 3.6.23.1-2
- some tests are failing on s390 and ppc/ppc64 so don't fail the whole build there

* Mon Apr 19 2010 Panu Matilainen <pmatilai@redhat.com> - 3.6.23.1-1
- update to 3.6.23.1 (http://www.sqlite.org/releaselog/3_6_23_1.html)

* Wed Mar 10 2010 Panu Matilainen <pmatilai@redhat.com> - 3.6.23-1
- update to 3.6.23 (http://www.sqlite.org/releaselog/3_6_23.html)
- drop the lemon sprintf patch, upstream doesn't want it
- make test-suite errors fail build finally

* Mon Jan 18 2010 Panu Matilainen <pmatilai@redhat.com> - 3.6.22-1
- update to 3.6.22 (http://www.sqlite.org/releaselog/3_6_22.html)

* Tue Dec 08 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.21-1
- update to 3.6.21 (http://www.sqlite.org/releaselog/3_6_21.html)

* Tue Nov 17 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.20-1
- update to 3.6.20 (http://www.sqlite.org/releaselog/3_6_20.html)

* Tue Oct 06 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.18-1
- update to 3.6.18 (http://www.sqlite.org/releaselog/3_6_18.html)
- drop no longer needed test-disabler patches

* Fri Aug 21 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.17-1
- update to 3.6.17 (http://www.sqlite.org/releaselog/3_6_17.html)
- disable to failing tests until upstream fixes

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.14.2-1
- update to 3.6.14.2 (#505229)

* Mon May 18 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.14-2
- disable rpath
- add -doc subpackage instead of patching out reference to it

* Thu May 14 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.14-1
- update to 3.6.14 (http://www.sqlite.org/releaselog/3_6_14.html)
- merge-review cosmetics (#226429)
  - drop ancient sqlite3 obsoletes
  - fix tab vs space whitespace issues
  - remove commas from summaries
- fixup io-test fsync expectations wrt SQLITE_DISABLE_DIRSYNC

* Wed Apr 15 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.13-1
- update to 3.6.13

* Thu Apr 09 2009 Dennis Gilmore <dennis@ausil.us> - 3.6.12-3
- apply upstream patch for memory alignment issue (#494906)

* Tue Apr 07 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.12-2
- disable strict aliasing to work around brokenness on 3.6.12 (#494266)
- run test-suite on build but let it fail for now

* Fri Apr 03 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.12-1
- update to 3.6.12 (#492662)
- remove reference to non-existent sqlite-doc from manual (#488883)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 04 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.10-3
- enable RTREE and FTS3 extensions (#481417)

* Thu Jan 22 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.10-2
- upstream fix yum breakage caused by new keywords (#481189)

* Thu Jan 22 2009 Panu Matilainen <pmatilai@redhat.com> - 3.6.10-1
- update to 3.6.10

* Wed Dec 31 2008 Panu Matilainen <pmatilai@redhat.com> - 3.6.7-1
- update to 3.6.7
- avoid lemon ending up in main sqlite package too

* Fri Dec 05 2008 Panu Matilainen <pmatilai@redhat.com> - 3.6.6.2-4
- add lemon subpackage

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> - 3.6.6.2-3
- Rebuild for pkg-config provides 

* Tue Dec 02 2008 Panu Matilainen <pmatilai@redhat.com> - 3.6.6.2-2
- require tcl(abi) in sqlite-tcl subpackage (#474034)
- move tcl extensions to arch-specific location
- enable dependency extraction on the tcl dso
- require pkgconfig in sqlite-devel

* Sat Nov 29 2008 Panu Matilainen <pmatilai@redhat.com> - 3.6.6.2-1
- update to 3.6.6.2

* Sat Nov 08 2008 Panu Matilainen <pmatilai@redhat.com> - 3.6.4-1
- update to 3.6.4
- drop patches already upstream

* Mon Sep 22 2008 Panu Matilainen <pmatilai@redhat.com> - 3.5.9-2
- Remove references to temporary registers from cache on release (#463061)
- Enable loading of external extensions (#457433)

* Tue Jun 17 2008 Stepan Kasal <skasal@redhat.com> - 3.5.9-1
- update to 3.5.9

* Wed Apr 23 2008 Panu Matilainen <pmatilai@redhat.com> - 3.5.8-1
- update to 3.5.8
- provide full version in pkg-config (#443692)

* Mon Mar 31 2008 Panu Matilainen <pmatilai@redhat.com> - 3.5.6-2
- remove reference to static libs from -devel description (#439376)

* Tue Feb 12 2008 Panu Matilainen <pmatilai@redhat.com> - 3.5.6-1
- update to 3.5.6
- also fixes #432447

* Fri Jan 25 2008 Panu Matilainen <pmatilai@redhat.com> - 3.5.4-3
- enable column metadata API (#430258)

* Tue Jan 08 2008 Panu Matilainen <pmatilai@redhat.com> - 3.5.4-2
- avoid packaging CVS directory as documentation (#427755)

* Fri Dec 21 2007 Panu Matilainen <pmatilai@redhat.com> - 3.5.4-1
- Update to 3.5.4 (#413801)

* Fri Sep 28 2007 Panu Matilainen <pmatilai@redhat.com> - 3.4.2-3
- Add another build conditional for enabling %%check

* Fri Sep 28 2007 Panu Matilainen <pmatilai@redhat.com> - 3.4.2-2
- Use bconds for the spec build conditionals
- Enable -tcl subpackage again (#309041)

* Wed Aug 15 2007 Paul Nasrat <pnasrat@redhat.com> - 3.4.2-1
- Update to 3.4.2

* Sat Jul 21 2007 Paul Nasrat <pnasrat@redhat.com> - 3.4.1-1
- Update to 3.4.1

* Sun Jun 24 2007 Paul Nasrat <pnsarat@redhat.com> - 3.4.0-2
- Disable load for now (#245486)

* Tue Jun 19 2007 Paul Nasrat <pnasrat@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Fri Jun 01 2007 Paul Nasrat <pnasrat@redhat.com> - 3.3.17-2
- Enable load 
- Build fts1 and fts2
- Don't sync on dirs (#237427)

* Tue May 29 2007 Paul Nasrat <pnasrat@redhat.com> - 3.3.17-1
- Update to 3.3.17

* Mon Mar 19 2007 Paul Nasrat <pnasrat@redhat.com> - 3.3.13-1
- Update to 3.3.13

* Fri Aug 11 2006 Paul Nasrat <pnasrat@redhat.com> - 3.3.6-2
- Fix conditional typo (patch from Gareth Armstrong)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.3.6-1.1
- rebuild

* Mon Jun 26 2006 Paul Nasrat <pnasrat@redhat.com> - 3.3.6-1
- Update to 3.3.6
- Fix typo  (#189647)
- Enable threading fixes (#181298)
- Conditionalize static library

* Mon Apr 17 2006 Paul Nasrat <pnasrat@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.3.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.3.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Tue Jan 31 2006 Christopher Aillon <caillon@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Tue Jan 24 2006 Paul Nasrat <pnasrat@redhat.com> - 3.2.8-1
- Add --enable-threadsafe (Nicholas Miell)
- Update to 3.2.8

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Oct  4 2005 Jeremy Katz <katzj@redhat.com> - 3.2.7-2
- no more static file or libtool archive (#169874) 

* Wed Sep 28 2005 Florian La Roche <laroche@redhat.com>
- Upgrade to 3.2.7 release.

* Thu Sep 22 2005 Florian La Roche <laroche@redhat.com>
- Upgrade to 3.2.6 release.

* Sun Sep 11 2005 Florian La Roche <laroche@redhat.com>
- Upgrade to 3.2.5 release.

* Fri Jul  8 2005 Roland McGrath <roland@redhat.com> - 3.2.2-1
- Upgrade to 3.2.2 release.

* Sat Apr  9 2005 Warren Togami <wtogami@redhat.com> - 3.1.2-3
- fix buildreqs (#154298)

* Mon Apr  4 2005 Jeremy Katz <katzj@redhat.com> - 3.1.2-2
- disable tcl subpackage

* Wed Mar  9 2005 Jeff Johnson <jbj@redhat.com> 3.1.2-1
- rename to "sqlite" from "sqlite3" (#149719, #150012).

* Wed Feb 16 2005 Jeff Johnson <jbj@jbj.org> 3.1.2-1
- upgrade to 3.1.2.
- add sqlite3-tcl sub-package.

* Sat Feb  5 2005 Jeff Johnson <jbj@jbj.org> 3.0.8-3
- repackage for fc4.

* Mon Jan 17 2005 R P Herrold <info@owlriver.com> 3.0.8-2orc
- fix a man page nameing conflict when co-installed with sqlite-2, as
  is permissible
