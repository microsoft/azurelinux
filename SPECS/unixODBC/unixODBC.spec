# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond   gui_related_parts 1

Name:    unixODBC
Version: 2.3.14
Release: 2%{?dist}

# See README: Programs are GPL, libraries are LGPL
# News Server library (Drivers/nn/yyparse.c) is GPLv3+
# (but that one is not compiled nor shipped)
License: GPL-2.0-or-later AND LGPL-2.1-or-later

Summary: A complete ODBC driver manager for Linux
URL:     http://www.unixODBC.org/

Source:  http://www.unixODBC.org/%{name}-%{version}.tar.gz
Source1: odbcinst.ini

Patch8:  so-version-bump.patch
Patch9:  keep-typedefs.patch

BuildRequires: make automake autoconf libtool libtool-ltdl-devel bison flex
BuildRequires: readline-devel
BuildRequires: multilib-rpm-config

Conflicts: iodbc

Suggests: mariadb-connector-odbc
Suggests: mysql-connector-odbc
Suggests: postgresql-odbc
Suggests: unixODBC-gui-qt

%description
Install unixODBC if you want to access databases through ODBC.
You will also need the mariadb-connector-odbc package if you want to access
a MySQL or MariaDB database, and/or the postgresql-odbc package for PostgreSQL.

%package devel
Summary: Development files for programs which will use the unixODBC library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The unixODBC package can be used to access databases through ODBC
drivers. If you want to develop programs that will access data through
ODBC, you need to install this package.


%prep
%setup -q
%patch -P8 -p1 -b .soname-bump
%patch -P9 -p1

autoreconf -vfi

%build
%configure \
  --with-gnu-ld=yes \
  --enable-threads=yes \
  --enable-drivers=no \
%if %{with gui_related_parts}
  --enable-driver-config=yes
%else
  --enable-driver-config=no
%endif

# Get rid of the rpaths
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build


%install
%make_install

install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
%multilib_fix_c_header --file %{_includedir}/unixODBC/unixodbc_conf.h

# make directory for unversioned plugins
mkdir $RPM_BUILD_ROOT%{_libdir}/%{name}

# copy text driver documentation into main doc directory
# currently disabled because upstream no longer includes text driver
# mkdir -p doc/Drivers/txt
# cp -pr Drivers/txt/doc/* doc/Drivers/txt

# don't want to install doc Makefiles as docs
find doc -name 'Makefile*' | xargs rm

# we do not want to ship static libraries
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libltdl.*
rm -rf $RPM_BUILD_ROOT%{_datadir}/libtool

# initialize lists of .so files
find $RPM_BUILD_ROOT%{_libdir} -name "*.so.*" | sed "s|^$RPM_BUILD_ROOT||" > base-so-list
find $RPM_BUILD_ROOT%{_libdir} -name "*.so"   | sed "s|^$RPM_BUILD_ROOT||" > devel-so-list


%files -f base-so-list
%license COPYING
%doc README AUTHORS ChangeLog
%if %{with gui_related_parts}
%doc doc
%endif

%config(noreplace) %{_sysconfdir}/odbc*

%{_bindir}/odbcinst
%{_bindir}/isql
%{_bindir}/dltest
%{_bindir}/iusql
%{_bindir}/odbc_config
%{_bindir}/slencheck
%{_mandir}/man*/*

%files devel -f devel-so-list
%{_includedir}/*
%_libdir/pkgconfig/*.pc


%changelog
* Fri Jan 09 2026 Michal Schorm <mschorm@redhat.com> - 2.3.14-2
- Bump release to test Packit automation

* Fri Jan 09 2026 Michal Schorm <mschorm@redhat.com> - 2.3.14-1
- Rebase to 2.3.14

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Florian Weimer <fweimer@redhat.com> - 2.3.12-4
- Fix out-of-bounds stack write (GCC 14 compatibility)

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Honza Horak <hhorak@redhat.com> - 2.3.12-2
- SPDX migration

* Thu Sep 14 2023 Packit <hello@packit.dev> - 2.3.12-1
- New Release 2.3.12 (lurcher)
- Don't check state with shared env (lurcher)
- Add --enable-singleenv option (lurcher)
- Allow longer messages via SQLGetDiag (lurcher)
- Add --enable-utf8ini flag and coding (lurcher)
- Fix possible seg faults with SQLAPI and pooling (lurcher)
- Fix possible seg faults with SQLAPI and pooling (lurcher)
- Remove self-reference (Stefan)
- Avoid implicit function declarations, for C99 compatibility (Florian Weimer)
- Fix --enable-stats config error (lurcher)
- Allow diagnostics to be retrieved on SQL_NO_DATA (Kevin Adler)
- isql.1: Add information about passwords containing semicolons (Hugh McMaster)
- isql.1: Various text updates (Hugh McMaster)
- Export __clear_ini_cache from libodbcinst (lurcher)
- Revert "Add call to atexit to clear the ini cache" (lurcher)
- Add call to atexit to clear the ini cache (lurcher)
- Add extra iusql connectionstring syntax (lurcher)
- Allow longer connection strings (part 3) (lurcher)
- Allow longer connection strings (part 2) (lurcher)
- Allow longer connection strings (lurcher)
- Fixed Connection String (Stefan)
- Add extra connection syntax to isql help (lurcher)
- Add extra logging for ODBCINST connect settings (lurcher)
- Allow isql to handle SQLPrepare returning SQL_SUCCESS_WITH_INFO (and report warning) (lurcher)
- Allow isql to handle SQLPrepare returning SQL_SUCCESS_WITH_INFO (lurcher)
- Allow passing complete connection string into iusql (lurcher)
- Remove __get_connection from cursor lib (lurcher)
- Avoid failed build if clock_gettime() is not available (lurcher)
- Update change log (lurcher)
- DriverManager/_info.c: Get locale encoding on Windows. (Markus Mützel)
- DriverManager/drivermanager.h: fix build without threads (Fabrice Fontaine)
- Fix iconv handle leak with pooling (lurcher)
- Fix buffer overrun (lurcher)
- Create SECURITY.md (Nick Gorham)
- Move to 2.3.12pre (lurcher)
- Makefile.am: Do not install config.h (Hugh McMaster)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Florian Weimer <fweimer@redhat.com> - 2.3.11-3
- Port to C99

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 16 2022 Michal Schorm <mschorm@redhat.com> - 2.3.11-1
- Rebase to 2.3.11

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 02 2021 Michal Schorm <mschorm@redhat.com> - 2.3.9-3
- Bump release after fix of the default configuration for MySQL driver
  comming from "mysql-connector-odbc" package

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.3.9-1
- rebase to version 2.3.9
- move unversioned *.so files back to *-devel package

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.3.7-4
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 30 2018 Michal Schorm <mschorm@redhat.com> - 2.3.7-2
- Bump for rebuild to ship updated configuration

* Sat Aug 11 2018 Pavel Raiskup <praiskup@redhat.com> - 2.3.7-1
- update to version 2.3.7

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 27 2018 Pavel Raiskup <praiskup@redhat.com> - 2.3.6-1
- update to version 2.3.6

* Wed Mar 07 2018 Honza Horak <hhorak@redhat.com> - 2.3.5-3
- Bump for a rebuild

* Tue Feb 20 2018 Pavel Raiskup <praiskup@redhat.com> - 2.3.5-2
- cleanup autotool hacks

* Mon Feb 19 2018 Jan Staněk <jstanek@redhat.com> - 2.3.5-1
- Update to version 2.3.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 03 2018 Honza Horak <hhorak@redhat.com> - 2.3.4-9
- Include mariadb-connector-odbc driver spec in the odbcinst.ini

* Wed Aug 30 2017 Tomas Repik <trepik@redhat.com> - 2.3.4-8
- move libtdsS.so to the main package and add tds config to odbcinst.ini
- rhbz#1448890

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.3.4-4
- Rebuild for readline 7.x

* Wed Jun 22 2016 Pavel Raiskup <praiskup@redhat.com> - 2.3.4-3
- delegate multilib hacks to multilib-rpm-config package

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 01 2015 Jan Stanek <jstanek@redhat.com> - 2.3.4-1
- Update to version 2.3.4

* Tue Aug 25 2015 Jan Stanek <jstanek@redhat.com> - 2.3.3-1
- Update to version 2.3.3
- Removed patches and sources included upstream
- Recreated so-version-bump.patch

* Wed Aug 12 2015 Jan Stanek <jstanek@redhat.com> - 2.3.2-8
- Backported changes necessary for building with new autotools version.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Jan Stanek <jstanek@redhat.com> - 2.3.2-4
- Added manual pages for iusql, dltest, odbc_config

* Fri Dec 06 2013 Jan Stanek <jstanek@redhat.com> - 2.3.2-3
- Renamed README.fedora to README.dist

* Thu Oct 24 2013 Jan Stanek <jstanek@redhat.com> - 2.3.2-2
- Add man page describing enviromental variables (#991018)

* Thu Oct 10 2013 Jan Stanek <jstanek@redhat.com> - 2.3.2-1
- Update to 2.3.2 version
- Removed extra man-pages and patch already shipped by upstream

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul  4 2013 Honza Horak <hhorak@redhat.com> 2.3.1-6
- Spec file clean-up
- Provide man pages created by Jan Stanek

* Thu Jul  4 2013 Honza Horak <hhorak@redhat.com> 2.3.1-5
- Fix Coverity patch
  Resolves: #981060

* Tue Mar 19 2013 Tom Lane <tgl@redhat.com> 2.3.1-4
- Fix assorted small bugs found by Coverity
Related: #760877

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Tom Lane <tgl@redhat.com> 2.3.1-1
- Update to version 2.3.1.  The main externally-visible change is that the
  GUI programs are not part of the unixODBC tarball anymore, so they are no
  longer in this package, and the unixODBC-kde sub-RPM has disappeared.
  There is a separate package unixODBC-gui-qt that now provides those programs.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.14-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 31 2010 Tom Lane <tgl@redhat.com> 2.2.14-12
- Fix isql crash at EOF with -b option
Resolves: #628909

* Mon May  3 2010 Tom Lane <tgl@redhat.com> 2.2.14-11
- Re-add accidentally-removed desktop icon for ODBCConfig
Related: #587933

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.2.14-10
- BR qt-assistant-adp-devel

* Sat Dec 19 2009 Tom Lane <tgl@redhat.com> 2.2.14-9
- Fix bug preventing drivers from being selected in ODBCConfig
Resolves: #544852

* Wed Nov 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.2.14-8
- Rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable ABI)

* Thu Oct 15 2009 Tom Lane <tgl@redhat.com> 2.2.14-7
- Clean up bogosity in multilib stub header support: ia64 should not be
  listed (it's not multilib), sparcv9 isn't a possible uname -i output

* Fri Aug 21 2009 Tom Lane <tgl@redhat.com> 2.2.14-6
- Switch to building against qt4, not qt3.  This means the DataManager,
  DataManagerII, and odbctest applications are gone.
Resolves: #514064
- Use Driver64/Setup64 to eliminate need for hand-adjustment of odbcinst.ini
Resolves: #514688
- Fix misdeclaration of SQLBIGINT and SQLUBIGINT in generated header files
Resolves: #518623

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun  9 2009 Peter Lemenkov <lemenkov@gmail.com> - 2.2.14-4
- Properly install *.desktop files
- No need to ship INSTALL in docs
- Use macros instead of hardcoded /usr/share and /usr/include
- fixed permissions on some doc- and src-files
- Almost all rpmlint messages are gone now

* Sat Jun 06 2009 Dennis Gilmore <dennis@ausil.us> - 2.2.14-3
- add sparc support to the multilib includes header

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Tom Lane <tgl@redhat.com> 2.2.14-1
- Update to unixODBC 2.2.14.  Note this involves an ABI break and a consequent
  soname version bump, because upstream fixed some mistakes in the widths of
  some API datatypes for 64-bit platforms.  Also, the formerly embedded
  mysql, postgresql, and text drivers have been removed.  (For mysql and
  postgresql, use the separate mysql-connector-odbc and postgresql-odbc
  packages, which are far more up to date.  The text driver is not currently
  shipped by upstream at all, but might get revived as a separate SRPM later.)
- Stop shipping .a library files, per distro policy.
- Fixes for libtool 2.2.

* Mon Jul 28 2008 Tom Lane <tgl@redhat.com> 2.2.12-9
- Fix build failure caused by new default patch fuzz = 0 policy in rawhide.

* Fri Jun 13 2008 Tom Lane <tgl@redhat.com> 2.2.12-8
- Install icons in /usr/share/pixmaps, not /usr/share/icons as this package
  has historically done; the former is considered correct.

* Fri Apr  4 2008 Tom Lane <tgl@redhat.com> 2.2.12-7
- Must BuildRequire qt3 now that Fedora has renamed qt4 to qt
Resolves: #440798

* Mon Feb 11 2008 Tom Lane <tgl@redhat.com> 2.2.12-6
- Move libodbcinst.so symlink into main package, since it's often dlopen'd
Related: #204882
- Clean up specfile's ugly coding for making base-vs-devel decisions

* Sun Dec 30 2007 Tom Lane <tgl@redhat.com> 2.2.12-5
- Add missing BuildRequires for flex.
Resolves: #427063

* Thu Aug  2 2007 Tom Lane <tgl@redhat.com> 2.2.12-4
- Update License tag to match code.

* Fri Apr 20 2007 Tom Lane <tgl@redhat.com> 2.2.12-3
- Make configure find correct Qt libraries when building on a multilib machine

* Mon Apr 16 2007 Tom Lane <tgl@redhat.com> 2.2.12-2
- Drop BuildRequires for kdelibs-devel
Resolves: #152717
- Clean up a few rpmlint complaints

* Wed Dec  6 2006 Tom Lane <tgl@redhat.com> 2.2.12-1
- Update to unixODBC 2.2.12.
- Add missing BuildPrereq for bison.
Resolves: #190427

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.11-7.1
- rebuild

* Mon Mar 27 2006 Tom Lane <tgl@redhat.com> 2.2.11-7
- Fix minor problems in desktop files (bug #185764)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.2.11-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.2.11-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 21 2005 Tom Lane <tgl@redhat.com> 2.2.11-6
- Patch NO-vs-no discrepancy between aclocal/acinclude and recent autoconf
  versions (not sure if this has been broken for a long time, or was just
  exposed by modular X changeover).
- Apparently need to require libXt-devel too for modular X.

* Mon Nov  7 2005 Tom Lane <tgl@redhat.com> 2.2.11-5
- Adjust BuildPrereq for modular X.

* Sun Oct 16 2005 Florian La Roche <laroche@redhat.com> 2.2.11-4
- link against dependent libs
- fix some bugs to resolve unknown symbols ;-(

* Thu Sep 29 2005 Tom Lane <tgl@redhat.com> 2.2.11-3
- Force update of yac.h because the copy in the distributed tarball does not
  match bison 2.0's numbering of symbols (bz #162676)
- Include documentation of text-file driver
- Use private libltdl so we can omit RTLD_GLOBAL from dlopen flags (bz #161399)

* Sat Sep 24 2005 Tom Lane <tgl@redhat.com> 2.2.11-2
- Remove Makefiles accidentally included in docs installation (bz #168819)
- Updates to keep newer libtool code from installing itself as part of package

* Fri Apr  8 2005 Tom Lane <tgl@redhat.com> 2.2.11-1
- Update to unixODBC 2.2.11

* Mon Mar  7 2005 Tom Lane <tgl@redhat.com> 2.2.10-3
- Rebuild with gcc4.

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.2.10-2
- Rebuilt for new readline.

* Thu Oct 28 2004 Tom Lane <tgl@redhat.com> 2.2.10-1
- Update to unixODBC 2.2.10

* Wed Sep 22 2004 Tom Lane <tgl@redhat.com> 2.2.9-1
- Update to unixODBC 2.2.9

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May  8 2004 Tom Lane <tgl@redhat.com> 2.2.8-5
- Backpatch fix for double-free error from upstream devel sources.
- rebuilt

* Wed May  5 2004 Tom Lane <tgl@redhat.com> 2.2.8-4
- Add dependency to ensure kde subpackage stays in sync with main
  (needed because we moved odbctest from one pkg to the other,
  cf bug #122478)
- rebuilt

* Wed Mar 10 2004 Tom Lane <tgl@redhat.com> 2.2.8-3
- Use installed libltdl
- rebuilt for Fedora Core 2

* Tue Mar  9 2004 Tom Lane <tgl@redhat.com> 2.2.8-2
- Rename lo_xxx() to odbc_lo_xxx() (bug #117211) (temporary until 2.2.9)
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar  1 2004 Tom Lane <tgl@redhat.com>
- Update to 2.2.8
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Dec  4 2003 Joe Orton <jorton@redhat.com> 2.2.5-10
- rebuild to restore sqltypes.h after #111195

* Thu Oct 16 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-9
- Add XFree86-devel to the list of BuildPrereq.  Did not bump
  release as there is no need to rebuild.

* Thu Oct 16 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-9
- Add comments to the /etc/odbcinst.ini file regarding the proper
  setup for MySQL and the origin of each library needed.

* Tue Oct 14 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-8
- Move libodbcmyS.so to the main package as well.  It is used the
  same way as libodbcpsqlS.so.

* Tue Oct 14 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-7
- Bumped the version so it rebuilds.

* Tue Oct 14 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-4
- Revert previous change and special case libodbcpsql.so and
  libodbcpsqlS.so instead.  Here is the explanation (from Elliot
  Lee):
  ".so files are only used at link time for normal dynamic libraries.
   The libraries referred to here are being used as dynamically loaded
   modules, so I guess moving those particular .so files back to the
   main package would make sense, but the other .so files should stay
   in the devel subpackage."

* Fri Oct 10 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-3
- Moved all the shared library symlinks to the main package.
  They were deliberatedly being added to the devel package for
  unknown reasons but this was forcing users to install the
  devel package always.
- No need to special-case libodbc.so anymore

* Fri Sep 05 2003 Elliot Lee <sopwith@redhat.com> 2.2.5-2
- Run auto* so it rebuilds.

* Mon Jul 07 2003 Fernando Nasser <fnasser@redhat.com> 2.2.5-1
- Moved odbctest to the kde package to remove require on Qt stuff
  from the main package.
- Removed stray "\" from doc/Makefile.am
- Applied libtool fix (provided by Alex Oliva) so that it build
 with cross-compilers (which are used by 64 bit systems)
- Updated sources to the 2.2.5 community release
- Changed the included libtool to the 1.5-3 one so that
  it properly link the libraries with the newly generated ones
  and not with the ones installed on the build system (or give
  an error if an old version is not installed (# 91110)
- Added new files for executable DataManagerII and icons LinuxODBC.xpm
  and odbc.xpm

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> 2.2.3-5
- debloat

* Tue Dec 17 2002 Elliot Lee <sopwith@redhat.com> 2.2.3-4
- Run libtoolize etc.

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 2.2.3-3
- Rebuild to fix filelist errors...?

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 2.2.3-2
- remove unpackaged files from the buildroot

* Tue Nov 19 2002 Elliot Lee <sopwith@redhat.com> 2.2.3-1
- Rebuild, update to 2.2.3

* Mon Aug 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.2-3
- Move libodbc.so to the main package, so programs dlopening
  it don't break (#72653)

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.2-1
- 2.2.2
- desktop file changes (# 69371)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon May 20 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.1-1
- 2.2.1
- Reenable other archs, as this should now build on 64 bit archs

* Sun May 19 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add at least mainframe; should this really be a i386-only rpm?

* Wed Apr 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.2.0-5
- rebuild

* Fri Apr  5 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.0-4
- Avoid having files in more than one package (#62755)

* Tue Mar 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.0-3
- Don't include kde plugin .so as a devel symlink (#61039)

* Fri Mar  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 2.2.0-2
- Rebuild with KDE 3.x

* Tue Feb 26 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.2.0-1
- Just build on i386 now, there are 64 bit oddities
- 2.2.0

* Fri Jan 11 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.1.1-2
- move libodbcinstQ* to the kde subpackage

* Fri Jan 11 2002 Trond Eivind Glomsrd <teg@redhat.com> 2.1.1-1
- 2.1.1
- minor cleanups

* Fri Dec 14 2001 Trond Eivind Glomsrd <teg@redhat.com> 2.0.7-5
- Rebuild

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Sun Jun 24 2001 Than Ngo <than@redhat.com>
- rebuild against qt-2.3.1, kde-2.1.x

* Fri Jun 15 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Better default odbcinst.ini
- Minor cleanups

* Wed Jun  6 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 2.0.7

* Wed Apr 25 2001 Trond Eivind Glomsrd <teg@redhat.com>
- Fix for isql segfault on EOF/ctrl-d exit

* Fri Apr 20 2001 Trond Eivind Glomsrd <teg@redhat.com>
- 2.0.6
- add patch for 64 bit archs (dword shouldn't be "long int")

* Wed Feb 28 2001 Trond Eivind Glomsrd <teg@redhat.com>
- rebuild

* Tue Nov 28 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 1.8.13

* Tue Oct 10 2000 Trond Eivind Glomsrd <teg@redhat.com>
- enable GUI now that we have KDE compiled with the standard
  compiler
- move the applnk entries to the KDE package

* Thu Aug 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- add the missing shared libs to the non-devel package

* Wed Aug 23 2000 Preston Brown <pbrown@redhat.com>
- 1.8.12 fixes problems with the postgresql driver

* Mon Jul 31 2000 Trond Eivind Glomsrd <teg@redhat.com>
- disable KDE subpackage to avoid the mess that is C++ binary
  compatibility

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Florian La Roche <laroche@redhat.com>
- improved QTDIR detection

* Wed Jun 28 2000 Trond Eivind Glomsrd <teg@redhat.com>
- 1.8.10
- use %%{_tmppath}
- update URL
- including two missing libraries

* Tue Jun 13 2000 Preston Brown <pbrown@redhat.com>
- 1.8.9

* Fri Jun 09 2000 Preston Brown <pbrown@redhat.com>
- adopted for Winston, changed to Red Hat packaging standards

* Tue Apr 18 2000 Murray Todd Williams <murray@codingapes.com>
- added a unixODBC-devel RPM to the group, added KDE links and icons to system
- all of which came from recommendations from Fredrick Meunier
- <Fredrick.Meunier@computershare.com.au>

* Mon Apr 17 2000 Murray Todd Williams <murray@codingapes.com>
- unixODBC-1.8.7
- moved install to $RPM_BUILD_ROOT so it didn't overrun existing files.
