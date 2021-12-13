Vendor:         Microsoft Corporation
Distribution:   Mariner
%define majorver 8.6
%define	vers %{majorver}.10
%{!?sdt:%define sdt 1}

Summary: Tool Command Language, pronounced tickle
Name: tcl
Version: %{vers}
Release: 4%{?dist}
License: TCL
URL: http://tcl.sourceforge.net/
Source0: http://downloads.sourceforge.net/sourceforge/tcl/tcl-core%{version}-src.tar.gz
Buildrequires: autoconf
BuildRequires:  gcc
BuildRequires: zlib-devel
Provides: tcl(abi) = %{majorver}
Obsoletes: tcl-tcldict <= %{vers}
Provides: tcl-tcldict = %{vers}
Patch0: tcl-8.6.10-autopath.patch
Patch1: tcl-8.6.10-conf.patch
Patch2: tcl-8.6.10-hidden.patch
Patch3: tcl-8.6.10-tcltests-path-fix.patch

%if %sdt
BuildRequires: systemtap-sdt-devel
%endif

%description
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

%package doc
Summary: Tcl documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
TCL documentation.

%package devel
Summary: Tcl scripting language development environment
Requires: %{name} = %{version}-%{release}

%description devel
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the development files and man pages for tcl.

%prep
%setup -q -n %{name}%{version}
rm -r compat/zlib
chmod -x generic/tclStrToD.c

%patch0 -p1 -b .autopath
%patch1 -p1 -b .conf
%patch2 -p1 -b .hidden
%patch3 -p1 -b .tcltests-path-fix

%build
pushd unix
autoconf
%configure \
%if %sdt
--enable-dtrace \
%endif
--enable-threads \
--enable-symbols \
--enable-shared

make %{?_smp_mflags} CFLAGS="%{optflags}" TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

%check
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}

%if ! %{_without_check}
  cd unix
  make test
%endif

%install
make install -C unix INSTALL_ROOT=%{buildroot} TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

ln -s tclsh%{majorver} %{buildroot}%{_bindir}/tclsh

# for linking with -lib%%{name}
ln -s lib%{name}%{majorver}.so %{buildroot}%{_libdir}/lib%{name}.so

mkdir -p %{buildroot}/%{_libdir}/%{name}%{majorver}

# postgresql and maybe other packages too need tclConfig.sh
# paths don't look at /usr/lib for efficiency, so we symlink into tcl8.6 for now
ln -s %{_libdir}/%{name}Config.sh %{buildroot}/%{_libdir}/%{name}%{majorver}/%{name}Config.sh

mkdir -p %{buildroot}/%{_includedir}/%{name}-private/{generic,unix}
find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/%{name}-private/'{}' ';'
( cd %{buildroot}/%{_includedir}
	for i in *.h ; do
		[ -f %{buildroot}/%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/%{name}-private/generic ;
	done
)

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir}/%{name}Config.sh
rm -rf %{buildroot}/%{_datadir}/%{name}%{majorver}/ldAix

%ldconfig_scriptlets

%files
%{_bindir}/tclsh*
%{_datadir}/%{name}%{majorver}
%exclude %{_datadir}/%{name}%{majorver}/tclAppInit.c
%{_datadir}/%{name}8
%{_libdir}/lib%{name}%{majorver}.so
%{_mandir}/man1/*
%dir %{_libdir}/%{name}%{majorver}
%doc README.md changes
%doc license.terms

%files doc
%{_mandir}/man3/*
%{_mandir}/mann/*

%files devel
%{_includedir}/*
%{_libdir}/lib%{name}stub%{majorver}.a
%{_libdir}/lib%{name}.so
%{_libdir}/%{name}Config.sh
%{_libdir}/%{name}ooConfig.sh
%{_libdir}/%{name}%{majorver}/%{name}Config.sh
%{_libdir}/pkgconfig/tcl.pc
%{_datadir}/%{name}%{majorver}/tclAppInit.c

%changelog
* Fri Oct 29 2021 Muhammad Falak <mwani@microsft.com> - 8.6.10-4
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:8.6.10-3
- Initial CBL-Mariner import from Fedora 20 (license: MIT).

* Wed May 13 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.10-2
- Fixed tcltests path
  Resolves: rhbz#1833701

* Tue Nov 26 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.10-1
- New version
- Updated patches

* Wed Nov  6 2019 Tom Callaway <spot@fedoraproject.org> - 1:8.6.9-1
- update to 8.6.9

* Thu May 17 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.8-2
- Reverted _module_build macro check, i.e. always build with systemtap probes

* Mon Mar 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.8-1
- New version
- Updated patches

* Sun Feb 25 2018 Florian Weimer <fweimer@redhat.com> - 1:8.6.7-3
- Late arrival for mass rebuild for Fedora 28

* Tue Aug 29 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.7-2
- Rebuilt due to glibc dropping libieee
  Resolves: rhbz#1486352

* Thu Aug 10 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.7-1
- New version
  Resolves: rhbz#1476424

* Fri Apr 21 2017 Karsten Hopp <karsten@redhat.com> - 1:8.6.6-4
- use new _module_build macro to limit dependencies for Modularity

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:8.6.6-3
- Rebuild for readline 7.x

* Thu Sep 29 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.6-2
- Splitted documentation to the doc subpackage
  Resolves: rhbz#1380291
- Fixed whitespace
- Dropped obsoleted defattr

* Wed Jul 27 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.6-1
- New version
  Resolves: rhbz#1360516

* Mon Jul 25 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.6-0.1.rc1
- New version
  Resolves: rhbz#1359463

* Tue Mar 22 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.5-1
- New version
  Resolves: rhbz#1313909
- Fixed parallel make
  Resolves: rhbz#1304799

* Fri Mar 13 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.4-1
- New version

* Fri Nov 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.3-1
- New version
  Resolves: rhbz#1163350
- Defuzzified patches

* Wed Aug 27 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.2-1
- New version
  Resolves: rhbz#1134023

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.1.1-5
- Re-enabled threads (previously reported bugs are no more reproducible)

* Mon Jun  2 2014 Ville Skyttä <ville.skytta@iki.fi> - 1:8.6.1-4
- Use system zlib instead of bundled one

* Tue May 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.1-3
- Fixed TCL_PACKAGE_PATH to point to tcl8.6

* Wed Apr 30 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.1-2
- Fixed bogus date in changelog

* Thu Apr 24 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.1-1
- New version
- Defuzzified patches

* Wed Jan 01 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.0-1
- New version
  Resolves: rhbz#889201
- Minor cleanups

* Fri Dec  6 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1:8.5.15-1
- Update to 8.5.15

* Thu Aug 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.14-1
- New version

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 12 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.13-1
- New version
  Resolves: rhbz#875830

* Tue Aug 21 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.12-3
- Removed pic patch

* Fri Aug 10 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.12-2
- Enabled upstream test suite
- Enabled stack checking

* Mon Jul 30 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.12-1
- New version
  Resolves: rhbz#843902

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  8 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.11-1
- New version
  Resolves: rhbz#752041

* Mon Jun 27 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.10-1
- New version
  Resolves: rhbz#716877

* Thu May 05 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.9-3
- Packaged tclAppInit.c into devel subpackage (#702088)
- Removed rpmlint warning - macro in comment

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.9-1
- New version (#641574)
- Updated hidden patch
- Removed sigabrt patch (integraged upstream)

* Wed Sep 29 2010 jkeating - 1:8.5.8-4
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.8-3
- rebuilt with TCL_NO_STACK_CHECK

* Wed Jun 09 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.8-2
- Reverted back tk paths (#540296)

* Wed Mar 17 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.8-1
- 562148 update to 8.5.8

* Thu Jan 21 2010 Nikola Pajkovsky <npajkovs@redhat.com> - 1:8.5.7-5
- fix sigabort patch(add +1 to length)

* Mon Aug 10 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 1:8.5.7-4
- Enable SEPolicy for libtcl. 
- fix sigabort

* Tue Jul 28 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 1:8.5.7-3
- 513997 fixed. SELinux policy problem with libtcl8.5.so

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18  2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:8.5.7-1
- 489017 update to 8.5.7 with systemtap support

* Wed Apr 1  2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:8.5.6-6
- add missing part of patch

* Tue Mar 31 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:8.5.6-5
- 492541 newer http prevents connection (reproduced on amsn)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:8.5.6-3
- fix hidden patch for functional expect

* Mon Feb  9 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:8.5.6-1
- update to 8.5.6

* Mon Nov 24 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.5-2
- change summary according to discussion on fedora-devel 
	RFC fix summary :)

* Wed Nov 19 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.5-1
- update to 8.5.5

* Fri Jul 25 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.3-1
- update to 8.5.3
- create vers macro for provides, obsoletes

* Mon Jul 21 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.2-3
- tclConfig.sh was fixed again with symlink into libdir/tcl8.5.
Many packages are looking in /usr/lib, because tcl dir is versioned.

* Tue Jun 24 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.2-2
- update to 8.5.2
- 451750 PostgreSQL need tclConfig.sh in paths
- 437399 now really own directories

* Wed Apr 23 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.1-4
- #443246 configure with disabled threads. Threads could lead to segfaults
	of dependent programme.

* Mon Mar 17 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.1-3
- #436567 change auto path, tk can't be found.
- #437399 fix files permission

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:8.5.1-2
- Autorebuild for GCC 4.3

* Fri Jan 18 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.1-1
- new version tcl8.5.1
- fix 433151 problem with regular expression
- Version 2.5.3 of the http package requires Tcl 8.4 or better ->
	change make patch, add tm files back to 8.4

* Tue Jan 15 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-6
- tclsh8.5 is back because of back compatibility #428712

* Tue Jan  8 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-5
- stack checking is ok, error is in application. Removing withouth stack.
- tcl-8.5.0-hidden.patch isn't ok, fix should be in expect. In the meantime
	the patch stay here.

* Mon Jan  7 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-4
- add patch from atkac at redhat dot com - fix linking with hidden objects

* Sat Jan  5 2008 Wart <wart@kobold.org> - 1:8.5.0-3
- Obsolete the tcl-tcldict package that has been incorporated
  into the main Tcl source code.
- Disable the the stack checking code; it makes assumptions that are
  not necessarily true on Fedora and causes some apps to fail (BZ #425799)

* Thu Jan  3 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-2
- rebuilt because of nonsense in tag

* Wed Jan  2 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-1
- upgrade on the new whole version 8.5.0
- thank you for patches and clean spec to wart (at kobold)

* Fri Nov 16 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-6
- CVE-2007-4772 NFA optimization cause hang in loop. Back ported patch
	from upstream development version.

* Wed Sep 26 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-5
- fix of patch - set auto_path was broken
- Resolves: rhbz#306321

* Fri Aug 24 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-4
- rebuild for mass rebuild
- check license & path for 32b/64b fix

* Thu Aug  9 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-3
- Resolves: rhbz#251410

* Mon Aug 6 2007 Michael Thomas <wart@kobold.org> - 1:8.4.15-2
- Explicitly add %%{_datadir}/tcl8.4 and %%{_libdir}/tcl8.4 to the
  auto_path.

* Tue May 22 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-1
- Update Tcl-8.4.15

* Tue May 22 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-18
- rhbz#235812

* Tue Apr  3 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-16
- rhbz#227725

* Tue Apr  3 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-15
- cleaning spec

* Wed Mar 21 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-14
- multilib problem, rhbz#227200

* Tue Feb 27 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-12
- review

* Wed Feb 21 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-11
- review

* Thu Feb 15 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-10
- review

* Tue Feb 13 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-9
- review again

* Fri Feb 09 2007 David Cantrell <dcantrell@redhat.com> - 1:8.4.13-8
- rebuild

* Thu Feb  8 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-7
- downgrade back to 8.4.13
- rhbz #226479 review

* Mon Feb  5 2007 Marcela Maslanova <mmaslano@redhat.com> - 8.5a5-8
- rhbz#227173

* Sun Feb  4 2007 Jakub Jelinek <jakub@redhat.com> - 8.5a5-7
- fix broken stack checking code (#226785)

* Thu Jan 25 2007 Marcela Maslanova <mmaslano@redhat.com> - 8.5a5-6
- rebuilt for obsoletes rhbz#217735

* Thu Jan 25 2007 Marcela Maslanova <mmaslano@redhat.com> - 8.5a5-5
- rebuilt

* Mon Dec 18 2006 Marcela Maslanova <mmaslano@redhat.com> - 8.5a5-4
- change in spec for compatibility with tk, version 8.5a5
- Resolves: rhbz#160441

* Thu Jul 20 2006 David Cantrell <dcantrell@redhat.com> - 8.4.13-3
- Fix cflags patch so it applies correctly
- Changes $(CFLAGS) to ${CFLAGS} in cflags patch

* Thu Jul 20 2006 David Cantrell <dcantrell@redhat.com> - 8.4.13-2
- Patch from Dennis Gilmore <dennis@ausil.us> for sparc64 (#199375)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 8.4.13-1.2
- rebuild

* Wed Apr 19 2006 David Cantrell <dcantrell@redhat.com> - 8.4.13-1
- Upgraded to Tcl 8.4.13

* Fri Feb 17 2006 David Cantrell <dcantrell@redhat.com> - 8.4.12-4
- Enable threads (#181871)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 8.4.12-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.4.12-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 David Cantrell <dcantrell@redhat.com> - 8.4.12-3
- Patched syntax errors in configure and tcl.m4 so it works with bash

* Thu Feb 02 2006 David Cantrell <dcantrell@redhat.com> - 8.4.12-2
- Don't use ksh on ia64

* Thu Feb 02 2006 David Cantrell <dcantrell@redhat.com> - 8.4.12-1
- Upgraded to tcl-8.4.12
- Use ksh rather than bash for the configure script (known bug w/ bash-3.1)
- Generate HTML docs from source
- Add in the Tk source for HTML doc generation

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul  1 2005 Jens Petersen <petersen@redhat.com> - 8.4.11-1
- update to latest stable release
  - update tcl-8.4-autoconf.patch
- buildrequire sed and use it instead of perl for editting tclConfig.sh

* Wed Mar  9 2005 Jens Petersen <petersen@redhat.com> - 8.4.9-3
- rebuild with gcc 4

* Tue Dec 14 2004 Jens Petersen <petersen@redhat.com> - 8.4.9-2
- move tclConfig.sh into -devel (Axel Thimm, 142724)

* Thu Dec  9 2004 Jens Petersen <petersen@redhat.com> - 8.4.9-1
- new stable release

* Wed Nov 24 2004 Jens Petersen <petersen@redhat.com> - 8.4.8-1
- update to latest release

* Fri Oct 15 2004 Jens Petersen <petersen@redhat.com> - 8.4.7-2
- improve tcl8.3.5-tclConfig-package-path-90160.patch to look in libdir in
  addition to datadir for packages, so that tclsh can load binary packages
  in lib64 (135310)

* Fri Jul 30 2004 Jens Petersen <petersen@redhat.com> - 8.4.7-1
- update to 8.4.7
  - replace tcl-8.4.5-no_rpath.patch by tcl-8.4-no_rpath.patch
  - replace tcl-8.4.5-autoconf.patch by tcl-8.4-autoconf.patch
- no longer obsolete itcl

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 13 2004 Jens Petersen <petersen@redhat.com> - 8.4.6-1
- update to 8.4.6

* Wed Apr 21 2004 Warren Togami <wtogami@redhat.com> - 8.4.5-7
- obsolete former itcl package (#121414)

* Wed Mar 10 2004 Jens Petersen <petersen@redhat.com> - 8.4.5-6
- apply tcl-8.4.5-autoconf.patch to build with autoconf 2.5x
  (Robert Scheck, #116773)
- use %%{name} more extensively for script portability
- run "make test" by default when building (can be disabled with
  "--without check")
- add a backwards compatible symlink {_prefix}/lib/tk8.4 ->
  {_datadir}/tk8.4 (Michal Jaegermann, part of #90160)
- use "mkdir -p" instead of "mkdirhier" (Robert Scheck, #116771)
- include some doc files

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> - 8.4.5-5.1
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> - 8.4.5-5
- rebuilt

* Mon Feb  2 2004 Jens Petersen <petersen@redhat.com> - 8.4.5-4
- include all private .h files under {_includedir}/tcl-private

* Mon Dec  1 2003 Thomas Woerner <twoerner@redhat.com> 8.4.5-3
- removed rpath (patch 4)

* Fri Nov 28 2003 Jens Petersen <petersen@redhat.com> - 8.4.5-2
- put private header files under generic and unix subdirs
- include real generic/tclPort.h not just a symlink to tclUnixPort.h
- add tclMath.h to {_includedir}/tcl-private/generic for building tk
- remove build remnants from tclConfig.sh

* Thu Nov 27 2003 Jens Petersen <petersen@redhat.com> - 8.4.5-1
- new package split out from tcltk
- update to tcl 8.4.5 (#88429)
  - drop tcl-8.3.3-heiierarchy.patch, tcl-8.3.3-dlopen.patch
	 and tcl8.3.5-koi8-u.enc-88806.patch
- include private include headers under {_includedir}/tcl-private
- filtered changelog for tcl
- buildrequire autoconf213 (#110583) [mvd@mylinux.com.ua]

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-92
- rebuild again for #91211

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-91
- rebuild to fix gzipped file md5sums (#91211)

* Fri Jul 04 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-90
- split out devel files from tcl and tk into -devel subpackages (#90087)
- fix tcl package path in tclConfig.sh to point to datadir (#90160)
  [reported by Michal Jaegermann]
- remove gratuitous whitespace in koi8-u.enc (#88806)
  [reported with fix by Victor Cheburkin]
- update ucs4 patch to also change regcustom.h, but disable it for now (#89098)

* Thu Feb  6 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-88
- use ucs4 wide chars since python now does (tkinter)

* Fri Jan 17 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-85
- add some requires

* Tue Jan 14 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-84
- link all libs with DT_SONAME using tcl.m4 patch (#81297)
- drop synthetic lib provides
- remove obsolete patches from srpm
- update buildrequires
- use buildroot instead of RPM_BUILD_ROOT
- install all man pages under mandir, instead of moving some from /usr/man
- install libtcl and libtk mode 755
- introduce _genfilelist macro for clean single-sweep find filelist generation
  for each package
- use perl to remove buildroot prefix from filelists

* Tue Jan  7 2003 Jeff Johnson <jbj@redhat.com> 8.3.5-80
- rebuild to generate deps for4 DSO's w/o DT_SONAME correctly.

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 8.3.5-79
- set execute bits on library so that requires are generated.

* Tue Dec 10 2002 Jens Petersen <petersen@redhat.com> 8.3.5-78
- make lib symlinks to .so not .so.0

* Tue Dec 10 2002 Jens Petersen <petersen@redhat.com> 8.3.5-77
- fix summary-not-capitalized for tclx, tcllib, tcl-html

* Mon Dec  9 2002 Jens Petersen <petersen@redhat.com> 8.3.5-76
- make it build on x86_64 (details below)
- don't explicitly update config.{guess,sub} since %%configure does it for us
- added "--without check" rpmbuild option to disable running tests in future
- build and install tcl and tk with script files under datadir (not libdir)
- generate filelists from datadir and not from mandir from now on

* Tue Dec  3 2002 Jens Petersen <petersen@redhat.com>
- update to tcl-8.3.5, tk-8.3.5, tcl-html-8.3.5
- update url for tcl, tk, tclx, itcl, tcllib
- build without all makecfg patches for now
  - in particular use upstream versioned library name convention
- add backward compatible lib symlinks for now
- add unversioned symlinks for versioned bindir files
- use make's -C option rather than jumping in and out of source dirs
  during install
- use INSTALL_ROOT destdir-like make variable instead of makeinstall
  for all subpackages except tix and itcl

* Mon Oct 21 2002 Jens Petersen <petersen@redhat.com>
- update to tcl-8.3.4, tk-8.3.4 (#75600), tcllib-1.3, itcl-3.2.1,
  tix-8.1.3 (#59098)
- drop obsolete tcl cruft, tcl refcount, tix perf patches
- added tcltk html manual
- drop the crud compat dir symlinks in libdir
- package now builds without tcl or tk installed (partly #52606)
  - replace all relative paths by absolutes ones, using new tcltktop
  - give absolute paths to tcl and tk when configuring
  - give buildroot bindir path to tcllib make
  - export buildroot libdir in LD_LIBRARY_PATH when installing
- replace tclvers and tkvers by tcltkvers and use it
- replace tcl_major and tk_major by tcltk_major and use it
- don't explicitly provide 64bit libs on ia64 and sparc64

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix config.guess and config.sub to newer versions

* Wed Aug 29 2001 Adrian Havill <havill@redhat.com>

* Mon Aug  8 2001 Adrian Havill <havill@redhat.com>
- re-enable glibc string and math inlines; recent gcc is a-ok.
- optimize at -O2 instead of -O
- rename "soname" patches related to makefile/autoconf changes
- added elf "needed" for tk, tclx, tix, itk

* Thu Jul 19 2001 Adrian Havill <havill@redhat.com>
- used %%makeinstall to brute force fix any remaining unflexible makefile dirs
- fixed bad ref count release in tcl (bug 49406)
- revert --enable-threads, linux is (still) not ready (yet) (bug 49251)

* Sun Jul  8 2001 Adrian Havill <havill@redhat.com>
- refresh all sources to latest stable (TODO: separate expect/expectk)
- massage out some build stuff to patches (TODO: libtoolize hacked constants)
- remove patches already rolled into the upstream
- removed RPATH (bugs 45569, 46085, 46086), added SONAMEs to ELFs
- changed shared object filenames to something less gross
- reenable threads which seem to work now
- made compile-friendly for IA64

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild for 7.2.

* Fri Mar 23 2001 Bill Nottingham <notting@redhat.com>
- bzip2 sources

* Mon Mar 19 2001 Preston Brown <pbrown@redhat.com>
- build fix from ahavill.

* Tue Feb 13 2001 Adrian Havill <havill@redhat.com>
- added "ja_JP.eucJP" to locale list for tcl

* Tue Feb 13 2001 Adrian Havill <havill@redhat.com>
- rebuild so make check passes

* Fri Oct 20 2000 Than Ngo <than@redhat.com>
- rebuild with -O0 on alpha (bug #19461)

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Thu Aug  3 2000 Jeff Johnson <jbj@redhat.com>
- merge "best known" patches from searching, stubs were broken.

* Thu Jul 27 2000 Jeff Johnson <jbj@redhat.com>
- rebuild against "working" util-linux col.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 16 2000 Jeff Johnson <jbj@redhat.com>
- don't mess with %%{_libdir}, it's gonna be a FHS pita.

* Fri Jun  2 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging changes.
- revert --enable-threads, linux is not ready (yet) (#11789).
- tcl/tk: update to 8.3.1 (#10779).
- abstract major tcltk version for soname expansion etc.

* Sat Mar 18 2000 Jeff Johnson <jbj@redhat.com>
- update to (tcl,tk}-8.2.3, expect-5.31, and itcl-3.1.0, URL's as well.
- use perl to drill out pre-pended RPM_BUILD_ROOT.
- configure with --enable-threads (experimental).
- correct hierarchy spelling (#7082).

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Make changes from bug number 7602
- Apply patch from bug number 7537
- Apply fix from bug number 7157
- Add fixes from bug #7601 to the runtcl patch

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix descriptions
- man pages are compressed (whatapain)

* Tue Nov 30 1999 Jakub Jelinek <jakub@redhat.com>
- compile on systems where SIGPWR == SIGLOST.

* Sat May  1 1999 Jeff Johnson <jbj@redhat.com>
- update tcl/tk to 8.0.5.

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- upgrade tcl/tk/tclX to 8.0.4

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to allow building on the arm
- build for glibc 2.1
- strip binaries

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update tcl/tk/tclX to 8.0.3, expect is updated also.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Erik Troan <ewt@redhat.com>
- updated version numbers of tcl/tk to relflect inclusion of p2

* Wed Mar 25 1998 Cristian Gafton <gafton@redhat.com>
- updated tcl/tk to patch level 2

* Wed Oct 22 1997 Otto Hammersmith <otto@redhat.com>
- added patch to remove libieee test in configure.in for tcl and tk.
  Shouldn't be needed anymore for glibc systems, but this isn't the "proper" 
  solution for all systems
- fixed src urls

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- removed version numbers from descriptions

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to tcl/tk 8.0 and related versions of packages

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
