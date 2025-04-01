%define majorver 8.6
%define vers %{majorver}.14

Summary: The graphical toolkit for the Tcl scripting language
Name: tk
Version: %{vers}
Release: 2%{?dist}
Epoch:   1
License: TCL AND HPND-Pbmplus AND CC-BY-SA-3.0 AND MIT-open-group AND MIT
URL: http://tcl.sourceforge.net
Source0: http://download.sourceforge.net/sourceforge/tcl/%{name}%{version}-src.tar.gz
Requires: tcl = %{epoch}:%{vers}
BuildRequires: make
BuildRequires: gcc
BuildRequires: tcl-devel = %{epoch}:%{vers}, autoconf
BuildRequires: libX11-devel
BuildRequires: libXft-devel
# panedwindow.n from itcl conflicts
Conflicts: itcl <= 3.2
Obsoletes: tile <= 0.8.2
Provides: tile = 0.8.2
Patch1: tk-8.6.12-make.patch
Patch2: tk-8.6.12-conf.patch
# https://core.tcl-lang.org/tk/tktview/dccd82bdc70dc25bb6709a6c14880a92104dda43
Patch3: tk-8.6.10-font-sizes-fix.patch

%description
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

%package devel
Summary: Tk graphical toolkit development files
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: tcl-devel = %{epoch}:%{vers}
Requires: libX11-devel libXft-devel

%description devel
When paired with the Tcl scripting language, Tk provides a fast and powerful
way to create cross-platform GUI applications.

The package contains the development files and man pages for tk.

%prep
%autosetup -p1 -n %{name}%{vers}

%build
cd unix
autoconf
%configure --enable-threads
%make_build CFLAGS="%{optflags}" TK_LIBRARY=%{_datadir}/%{name}%{majorver}

%check
# do not run "make test" by default since it requires an X display
%{?_with_check: %define _with_check 1}
%{!?_with_check: %define _with_check 0}

%if %{_with_check}
#  make test
%endif

%install
make install -C unix INSTALL_ROOT=%{buildroot} TK_LIBRARY=%{_datadir}/%{name}%{majorver}

ln -s wish%{majorver} %{buildroot}%{_bindir}/wish

# for linking with -l%%{name}
ln -s lib%{name}%{majorver}.so %{buildroot}%{_libdir}/lib%{name}.so

mkdir -p %{buildroot}/%{_includedir}/%{name}-private/{generic/ttk,unix}
find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/%{name}-private/'{}' ';'
( cd %{buildroot}/%{_includedir}
  for i in *.h ; do
    [ -f %{buildroot}/%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/%{name}-private/generic ;
  done
)

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir}/%{name}Config.sh

%if 0%{?flatpak}
mkdir -p %{buildroot}%{_usr}/bin
ln -s %{_bindir}/wish %{_bindir}/wish%{majorver} %{buildroot}%{_usr}/bin/
%endif

%pre
[ ! -h %{_prefix}/%{_lib}/%{name}%{majorver} ] || rm %{_prefix}/%{_lib}/%{name}%{majorver}

%ldconfig_scriptlets

%files
%{_bindir}/wish*
%{_datadir}/%{name}%{majorver}
%exclude %{_datadir}/%{name}%{majorver}/tkAppInit.c
%{_libdir}/lib%{name}%{majorver}.so
%{_libdir}/%{name}%{majorver}
%{_mandir}/man1/*
%{_mandir}/mann/*
%if 0%{?flatpak}
%{_usr}/bin/wish*
%endif
%doc README.md changes license.terms

%files devel
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{name}stub%{majorver}.a
%{_libdir}/%{name}Config.sh
%{_libdir}/pkgconfig/tk.pc
%{_mandir}/man3/*
%{_datadir}/%{name}%{majorver}/tkAppInit.c

%changelog
* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Feb 29 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.14-1
- New version
  Related: rhbz#2267019

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.13-2
- Converted license to SPDX

* Tue Aug 29 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.13-1
- New version
  Related: rhbz#2231272

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 23 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.12-1
- New version
  Related: rhbz#1488695

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Tom Stellard <tstellar@redhat.com> - 1:8.6.10-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:8.6.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.10-2
- Fixed font sizes
  Resolves: rhbz#1244729

* Tue Nov 26 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.10-1
- New version
- Upated patches
- Dropped fix-xft patch (upstreamed)

* Wed Nov  6 2019 Tom Callaway <spot@fedoraproject.org> - 1:8.6.9.1-1
- update to 8.6.9.1

* Mon Mar 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.8-1
- New version

* Sun Feb 25 2018 Florian Weimer <fweimer@redhat.com> - 1:8.6.7-3
- Late arrival for mass rebuild for Fedora 28

* Thu Aug 31 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:8.6.7-2
- Rebuilt due to glibc dropping libieee

* Thu Aug 10 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.7-1
- New version
  Related: rhbz#1476424

* Wed Jul 27 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.6-1
- New version
  Related: rhbz#1360516

* Mon Jul 25 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.6-0.1.rc1
- New version
  Related: rhbz#1359463

* Tue Mar 22 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.5-1
- New version
  Related: rhbz#1313909

* Thu Jul  2 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.4-2
- Fixed crash if there is no font installed (by no-fonts-fix patch)
  Resolves: rhbz#1229991

* Fri Mar 13 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.4-1
- New version

* Fri Nov 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.3-1
- New version
  Resolves: rhbz#1163350
- Defuzzified conf patch

* Wed Aug 27 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.2-1
- New version
  Resolves: rhbz#1134023

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.1-2
- Re-enabled threads (previously reported bugs are no more reproducible)

* Thu Apr 24 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.1-1
- New version
- Defuzzified patches

* Wed Jan 01 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.6.0-1
- New version
  Resolves: rhbz#889201
- Removed seg_input patch (upstreamed)
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

* Mon Jul 30 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.12-1
- New version
  Resolves: rhbz#843902

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov  8 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.11-1
- New version

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.10-2
- Rebuilt for glibc bug#747377

* Mon Jun 27 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.10-1
- New version

* Thu May 05 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.9-4
- Packaged tkAppInit.c into devel subpackage (#702088)
- Removed spec code for deprecated prolog.ps file (#702088)
- Removed rpmlint warning - macro in comment

* Thu Feb 17 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.9-3
- Fix xft detection (#677692)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.9-1
- New version 8.5.9
- Updated make patch
- Removed color patch (integrated upstream)
- Removed wmiconphoto-fix patch (integrated upstream)

* Sun Jul 25 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.8-2
- Fixed wm iconphoto #615750

* Thu Mar 18 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.8-1
- Update to 8.5.8

* Fri Feb 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 1:8.5.7-4
- Fixed macro/variable conflict in spec

* Wed Dec 9 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 1:8.5.7-3
- Resolves: #545807 - Color hash problem on x86_64

* Tue Aug 11 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 1:8.5.7-2
- Fix Source0 url

* Wed Jul 22 2009 Nikola Pajkovsky <npajkovs@redhat.com> - 1:8.5.7-1
- update to 8.5.7

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:8.5.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:8.5.6-3
- 480742 patch fixes the input method. The reason for this behaviour
 is still unknown.

* Thu Feb 19 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:8.5.6-2
- 486132 add missing requires in tk-devel

* Tue Feb 10 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1:8.5.6-1
- update to 8.5.6

* Wed Nov 19 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.5-1
- update to 8.5.5

* Wed Aug  6 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.3-4
- rewrite patch once more - the same way how upstream fix it

* Mon Aug  4 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.3-3
- previous bug - remove my patch, add upstream patch
- Problem is updated xorg, which changed behaviour of GenericEvent

* Tue Jul 29 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.3-2
- fix 456922 - crash gitk resolved

* Fri Jul 25 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.3-1
- update to 8.5.3

* Mon May 19 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.2-1
- new version tk8.5.2

* Fri May  9 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.1-4
- 445836 added BR (thanks to jamatos)

* Wed Feb 20 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.1-3
- rebuilt without useless patches

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:8.5.1-2
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.1-1
- new version tk8.5.1

* Fri Jan 25 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-4
- attached upstream patch
- similar to CVE-2006-4484, problem with GIF again #430100

* Tue Jan 15 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-3
- wish8.5 is here again for back compatibility

* Sat Jan  5 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-2
- Obsolete the tile package that has been incorporated into the core
  tk source.

* Wed Jan  2 2008 Marcela Maslanova <mmaslano@redhat.com> - 1:8.5.0-1
- upgrade on the 8.5.0

* Mon Sep 17 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-5
- CVE-2007-4851 Tk GIF processing buffer overflow
- Resolves: rhbz#290991

* Fri Aug 31 2007 Jeremy Katz <katzj@redhat.com> - 1:8.4.15-4
- BR gawk to unbreak things

* Thu Aug  9 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-3
- check licence, build for mass rebuild

* Thu Aug  9 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-2
- Resolves: rhbz#251411

* Tue Jul 31 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.15-1
- Update tk8.4.15

* Tue Feb 20 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-5
- rhbz#226494 review again

* Wed Feb 14 2007 Marcela Maslanova <mmaslano@redhat.com> - 1:8.4.13-4
- rhbz#226494 review

* Sat Feb 10 2007 David Cantrell <dcantrell@redhat.com> - 1:8.4.13-3
- Require correct tcl package on tk

* Sat Feb 10 2007 David Cantrell <dcantrell@redhat.com> - 1:8.4.13-2
- Require correct tk package on tk-devel

* Fri Feb 09 2007 David Cantrell <dcantrell@redhat.com> - 1:8.4.13-1
- Revert to tk-8.4.13 since tcl has been reverted

* Thu Jan 25 2007 Marcela Maslanova <mmaslano@redhat.com> - 8.5a5-1
- update: version 8.5a5
- Resolves: rhbz#160442

* Thu Jul 20 2006 David Cantrell <dcantrell@redhat.com> - 8.4.13-3
- Patch from Dennis Gilmore <dennis@ausil.us> for sparc64 (#199378)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 8.4.13-2
- rebuild

* Thu Apr 20 2006 David Cantrell <dcantrell@redhat.com> - 8.4.13-1
- Upgraded to Tk 8.4.13

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 8.4.12-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.4.12-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 David Cantrell <dcantrell@redhat.com> - 8.4.12-1
- Upgraded to tk-8.4.12

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 15 2005 Warren Togami <wtogami@redhat.com> - 8.4.11-2
- xorg-x11-devel -> libX11-devel

* Fri Jul  1 2005 Jens Petersen <petersen@redhat.com> - 8.4.11-1
- update to 8.4.11 stable release
  - update tk-8.4.4-lib-perm.patch

* Wed Mar  9 2005 Jens Petersen <petersen@redhat.com> - 8.4.9-3
- tk-devel requires tcl-devel and xorg-x11-devel instead of XFree86-devel
- use sed instead of perl for fixing tkConfig.sh
  - buildrequire sed instead of perl
- buildrequire xorg-x11-devel instead of XFree86-devel
- rebuild with gcc 4

* Tue Dec 14 2004 Jens Petersen <petersen@redhat.com> - 8.4.9-2
- move tkConfig.sh into -devel (Axel Thimm, 142724)

* Thu Dec  9 2004 Jens Petersen <petersen@redhat.com> - 8.4.9-1
- latest stable release

* Wed Nov 24 2004 Jens Petersen <petersen@redhat.com> - 8.4.8-1
- update to latest release

* Fri Oct 15 2004 Jens Petersen <petersen@redhat.com> - 8.4.7-2
- move pkgIndex.tcl back into {_libdir}/{name}{majorver} so that multilib
  parallel installs works (135310)
  - drop tk-8.4.5-pkgIndex-loc.patch
  - remove any compat symlink present before installing
  - do not generate compat symlink after installing

* Fri Jul 30 2004 Jens Petersen <petersen@redhat.com> - 8.4.7-1
- update to 8.4.7
  - replace tk-8.4.5-no_rpath.patch with tk-8.4-no_rpath.patch
  - replace tk-8.4.5-autoconf.patch with tk-8.4-autoconf.patch

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 18 2004 Jeremy Katz <katzj@redhat.com> 8.4.6-2
- rebuild

* Thu May 13 2004 Jens Petersen <petersen@redhat.com> - 8.4.6-1
- update to 8.4.6

* Wed Apr 21 2004 Jens Petersen <petersen@redhat.com> - 8.4.5-8
- obsolete itcl since it also provided panedwindow.n (Warren Togami, 121414)

* Tue Mar 16 2004 Mike A. Harris <mharris@redhat.com> - 8.4.5-7
- Removed Requires: XFree86-libs and replaced with Buildrequires: XFree86-devel
  so that the package is X11 implementation agnostic for the inclusion of
  xorg-x11 (#118482)
- Added Requires(post,postun): /sbin/ldconfig
- Added BuildRequires: perl, as perl is used during install

* Thu Mar 11 2004 Jens Petersen <petersen@redhat.com> - 8.4.5-6
- generate compat symlink instead in post if /usr/lib/tk{majorver}
  does not exist

* Wed Mar 10 2004 Jens Petersen <petersen@redhat.com> - 8.4.5-5
- add tk-8.4.5-autoconf.patch and build with autoconf 2.5x
  (Robert Scheck, #116776)
- add tk-8.4.5-pkgIndex-loc.patch to install pkgIndex.tcl in the script dir
- use {name} throughout for greater portability
- add a "--with check" rpmbuild option
- use "mkdir -p" instead of "mkdirhier" (Robert Scheck, #116774)
- /usr/lib/tk8.4 is now a compat symlink to {_datadir}/tk8.4
- include all the private header files under /usr/include/tk-private
- add doc files

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Dec 12 2003 Jens Petersen <petersen@redhat.com> - 8.4.5-3
- add private header files needed to build tix in {_includedir}/{name}-private

* Mon Dec  1 2003 Thomas Woerner <twoerner@redhat.com> 8.4.5-2
- remove rpath with tk-8.4.5-no_rpath.patch

* Thu Nov 27 2003 Jens Petersen <petersen@redhat.com> - 8.4.5-1
- new package split out from tcltk
- update to tk 8.4.5 (#88429)
- filtered changelog for tk
- buildrequire autoconf213 (#110583) [mvd@mylinux.com.ua]
- remove build remnants from tkConfig.sh

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-92
- rebuild again for #91211

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-91
- rebuild to fix gzipped file md5sums (#91211)

* Fri Jul 04 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-90
- split out devel files from tcl and tk into -devel subpackages (#90087)

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

* Mon Dec  9 2002 Jens Petersen <petersen@redhat.com> 8.3.5-76
- make it build on x86_64 (details below)
- don't explicitly update config.{guess,sub} since configure does it for us
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
- used makeinstall to brute force fix any remaining unflexible makefile dirs
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
- don't mess with {_libdir}, it's gonna be a FHS pita.

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
