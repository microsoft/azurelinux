# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?tcl_version: %global tcl_version %((echo 0; echo 'puts $tcl_version' | tclsh8) | tail -1)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

# This package is old and only kept for compatibility.
# There is no real benefit to modernizing the code to support C23.
%global optflags %{optflags} -std=gnu17

# Same logic for not updating to TCL9.

Name:           sqlite2
Version:        2.8.17
Release:        47%{?dist}

Summary:        Embeddable SQL engine in a C library
License:        blessing AND LicenseRef-Fedora-Public-Domain
URL:            http://www.sqlite.org/
Source0:        http://www.sqlite.org/sqlite-%{version}.tar.gz
Patch1:         sqlite-2.8.15.rpath.patch
Patch2:         sqlite-2.8.15-makefile.patch
Patch3:         sqlite-2.8.3.test.rh9.patch
Patch4:         sqlite-64bit-fixes.patch
Patch5:         sqlite-2.8.15-arch-double-differences.patch
Patch6:         sqlite-2.8.17-test.patch
Patch7:         sqlite-2.8.17-tcl.patch
Patch8:         sqlite-2.8.17-ppc64.patch
Patch9:         sqlite-2.8.17-format-security.patch
Patch10:        sqlite-2.8.17-tcl86.patch
Patch11:        sqlite-2.8.17-cleanup-temp-c.patch
Patch12:        sqlite-2.8.17-suse-cleanups.patch
Patch13:        sqlite-2.8.17-suse-detect-sqlite3.patch
Patch14:        sqlite-2.8.17-CVE-2007-1888.patch
Patch15:        sqlite-2.8.17-lemon-snprintf.patch
Patch16:        sqlite-2.8.17-fix-sort-syntax.patch
Patch17:        sqlite-2.8.17-ldflags.patch
Patch18:        sqlite-2.8.17-fix-unsigned-FTBFS.patch
Patch19:        sqlite-2.8.17-gcc10.patch
Patch20:        sqlite2-configure-c99.patch
Patch21:        sqlite2-lemon-c99.patch

BuildRequires: make
BuildRequires:  gcc-c++
BuildRequires:  ncurses-devel, readline-devel, tcl8-devel
Obsoletes:      sqlite < 3

%description
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views. A complete database
is stored in a single cross-platform disk file. The native C/C++ API
is simple and easy to use. Bindings for other languages are also
available.

%package        devel
Summary:        Development files for SQLite
Requires:       %{name}%{?_isa} = %{version}-%{release}, pkgconfig
Obsoletes:      sqlite-devel < 3

%description    devel
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views.
This package contains static library and header files for developing
applications using sqlite.

%package        tcl
Summary:        Tcl bindings for sqlite
%if 0%{?rhel}%{?fedora} > 5
Requires:       tcl(abi) = %{tcl_version}
%else
Requires:       tcl%{?_isa} >= %{tcl_version}
%endif
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      sqlite-tcl < 3

%description    tcl
SQLite is a small, fast, embeddable SQL database engine that supports
most of SQL92, including transactions with atomic commit and rollback,
subqueries, compound queries, triggers, and views.
This package contains tcl bindings for sqlite.

%prep
%setup -q -n sqlite-%{version}
find . -type d -name CVS -print0 | xargs -0 rm -r
%patch -P1 -p1 -b .rpath
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1
%patch -P10 -p1
%patch -P11 -p1 -b .cleanup-tempc
%patch -P12 -p1 -b .suse
%patch -P13 -p1 -b .detect-sqlite3
%patch -P14 -p1 -b .CVE-2007-1888
%patch -P15 -p1 -b .snprintf
%patch -P16 -p1 -b .fix-sort-syntax
%patch -P17 -p1 -b .ldflags
%patch -P18 -p1 -b .unsigned-fix
%patch -P19 -p1 -b .gcc10
%patch -P20 -p1
%patch -P21 -p1
sed -i.rpath 's!__VERSION__!%{version}!g' Makefile.in
# Patch additional /usr/lib locations where we don't have $(libdir)
# to substitute with.
sed -i.lib 's!@exec_prefix@/lib!%{_libdir}!g' Makefile.in

sed -i 's!tclsh !tclsh8 !g' Makefile.in

%build
CFLAGS="$RPM_OPT_FLAGS -DNDEBUG=1"
%configure --enable-utf8 --disable-static --disable-rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make
make tclsqlite libtclsqlite.la doc

%check
#obs. make test doesn't like root
LD_LIBRARY_PATH=./.libs make test

%install
rm -rf $RPM_BUILD_ROOT
DIRECTORY=$RPM_BUILD_ROOT%{_libdir}/sqlite-%{version}
install -d $DIRECTORY
echo 'package ifneeded sqlite 2 [list load [file join $dir libtclsqlite.so]]' > $DIRECTORY/pkgIndex.tcl

%makeinstall
install -D -m 0644 sqlite.1 $RPM_BUILD_ROOT%{_mandir}/man1/sqlite.1
mkdir -p $RPM_BUILD_ROOT%{tcl_sitearch}
mv -f $DIRECTORY $RPM_BUILD_ROOT%{tcl_sitearch}/sqlite2

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_bindir}/tclsqlite

%ldconfig_scriptlets

%files
%{_bindir}/sql*
%{_libdir}/libsql*.so.*
%{_mandir}/man1/*

%files devel
%doc README doc/*
%{_libdir}/libsql*.so
%{_includedir}/*
%{_libdir}/pkgconfig/*

%files tcl
%doc doc/tclsqlite.html
%{tcl_sitearch}/sqlite2/

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 12 2025 Tom Callaway <spot@fedoraproject.org> - 2.8.17-46
- fix FTBFS, use -std=gnu17 and tcl8

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Tom Callaway <spot@fedoraproject.org> - 2.8.17-43
- change file dep to package dep on tcl-devel

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec  2 2022 Florian Weimer <fweimer@redhat.com> - 2.8.17-39
- Port to C99 (#2150360)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Tom Callaway <spot@fedoraproject.org> - 2.8.17-35
- disable rpath

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Tom Callaway <spot@fedoraproject.org> - 2.8.17-32
- fix FTBFS

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 13 2019 Tom Callaway <spot@fedoraproject.org> - 2.8.17-30
- new rpm does not like obsoletes for provide strings, removed them, fixes FTBFS

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 10 2019 Tom Callaway <spot@fedoraproject.org> - 2.8.17-28
- bring in all the good fixes from suse and debian
  ... including the one that resolves the FTBFS since Fedora 26. yikes.

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.8.17-27
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.8.17-20
- Rebuild for readline 7.x

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.17-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Luis Bazan <lbazan@fedoraproject.org> - 2.8.17-16
- Don't ship CVS files thanks "Ville Skyttä ville.skytta@iki.fi"
 
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2.8.17-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Sun Dec 08 2013 Robert Scheck <robert@fedoraproject.org> 2.8.17-13
- Solved build failures with "-Werror=format-security" (#1037335)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep 02 2012 Robert Scheck <robert@fedoraproject.org> - 2.8.17-10
- Use macros to ensure that the correct tcl version is always used

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Robert Scheck <robert@fedoraproject.org> - 2.8.17-8
- Added a patch to avoid segmentation fault of tests on ppc64

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 18 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.8.17-5
- Install tcl subpackage in correct place, thanks to hkoba for patch (#516411)
- Use new tclver define, depend on at least tcl 8.5

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar 23 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 2.8.17-3
- Add patches to build with new TCL and fix tests (#491726)
  thanks to D. Marlin.
  
* Wed Oct 03 2007 Alex Lancaster <alexl@users.sourceforge.net> 2.8.17-2
- Rebuild for merged Fedora

* Sun Sep 10 2006 Mike McGrath <imlinux@gmail.com> 2.8.17-1
- New upstream source

* Tue Feb 28 2006 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.8.16-3
- Rebuild for Fedora Extras 5

* Sat Nov 26 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.8.16-2
- Disable static libs

* Fri May 20 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.8.16-1
- Name change to sqlite2
- Dropped Epoch
- Added Obsoletes to all subpackages
- Minor cosmetic changes

* Wed Feb 16 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:2.8.16-1
- Update to 2.8.16 bug-fix release + update patches.

* Tue Feb 15 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 2.8.15-2
- add sqlite-64bit-fixes.patch and sqlite-2.8.15-arch-double-differences.patch
  fixes x86_64; Both were found in a mandrake srpm
- remove exclusive arch ix86; hopefully this fixes ppc also

* Sun Jan 23 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:2.8.15-1
- Add exclusive arch ix86 for now (make test segfaults on x86_64).
- Update makefile patch, $(exec_prefix)/lib -> $(libdir), and
  substitute additional /usr/lib locations in %%prep for multilib
  people to play with.

* Sun Sep 26 2004 Adrian Reber <adrian@lisas.de> - 0:2.8.15-0.fdr.1
- Update to 2.8.15
- Update patches

* Sat Jun 19 2004 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.14-0.fdr.1
- Update to 2.8.14
- Update patches
- --enable-releasemode
- small spec file tweaks

* Sat Dec 27 2003 Jean-Luc Fontaine <jfontain@free.fr> - 0:2.8.6-0.fdr.6
- in tcl rpm, removed tclsqlite, moved shared library in own sqlite
  sub-directory add added pkgIndex.tcl file to make package dynamically
  loadable in a Tcl interpreter
- in build requirements, work around tcl-devel and tk-devel packages non
  existence in RH 8.0 and 9
- in tcl rpm, added tcl package requirement
- in tcl rpm, post ldconfig is not necessary

* Wed Nov 12 2003 Nils O. Selåsdal <NOS@Utel.no> -  0:2.8.6-0.fdr.5
- BuildRequires tcl-devel
- small .spec tweaks

* Tue Oct 28 2003 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.6-0.fdr.4
- exclude libtclsqlite.a

* Mon Oct 27 2003 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.6-0.fdr.3
- Fix readme -> README

* Mon Oct 27 2003 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.6-0.fdr.2
- Better summary/description
- Add patch for not using rpath
- Add patch that builds tclsqlite (From Anvil's package)
- Add patch that fixes the tests (From Anvil's package)
- New tcl subpackage
- Also make the tests during build
- Build docs, and include them in -devel

* Fri Oct 10 2003 Nils O. Selåsdal <NOS@Utel.no> - 0:2.8.6-0.fdr.1
- Initial RPM release.
