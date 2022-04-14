Vendor:         Microsoft Corporation
Distribution:   Mariner
%bcond_without wcheck

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%define major_ver 8.4
%define upversion 8.5
%define tcltk_ver 8.4.13
#define for 8.4 is needed, tclx wasn't updated on higher version

Summary: Extensions for Tcl and Tk
Name: tclx
Version: %{major_ver}.0
Release: 36%{?dist}
License: BSD
URL: http://tclx.sourceforge.net/
Source: http://downloads.sourceforge.net/%{name}/%{name}%{major_ver}.tar.bz2
Requires: tcl%{?_isa} >= %{tcltk_ver}, tk%{?_isa} >= %{tcltk_ver}
BuildRequires:  gcc
BuildRequires: tcl-devel >= %{tcltk_ver}, tk-devel >= %{tcltk_ver}
#BuildRequires: autoconf
Patch1: tclx-%{major_ver}-varinit.patch
Patch2: tclx-%{major_ver}-relid.patch
Patch3: tclx-%{major_ver}-man.patch
Patch4: tclx-%{major_ver}-tcl86.patch

%description
Extended Tcl (TclX) is a set of extensions to the Tcl programming language.
Extended Tcl is oriented towards system programming tasks and large
application development. TclX provides additional interfaces to the
operating system, and adds many new programming constructs, text manipulation
and debugging tools.

%package devel
Summary: Extended Tcl development files
Requires: tclx = %{version}-%{release}

%description devel
This package contains the tclx development files needed for building
applications embedding tclx.

%prep
%setup -q -n tclx%{major_ver}
%patch1 -p1 -b .1.varinit
%patch2 -p1 -b .2.relid
%patch3 -p1 -b .3.patch
%patch4 -p1 -b .4.tcl86

# patch2 touches tcl.m4

%build
%configure \
   --enable-tk=YES \
   --with-tclconfig=%{_libdir} \
   --with-tkconfig=%{_libdir} \
   --with-tclinclude=%{_includedir} \
   --with-tkinclude=%{_includedir} \
   --enable-gcc \
   --disable-threads \
   --enable-64bit \
   --libdir=%{tcl_sitearch}
# smp building doesn't work
make %{?_smp_mflags}

%check
# run "make test" by default
%if %{without wcheck}
   make test
%endif

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/
echo '%{_libdir}/tcl%{tcl_version}/%{name}%{major_ver}' > $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
# File refers to tcl BSD license- actual license is pulled in as runtime requirement
%license license.terms
%doc ChangeLog README
%{_libdir}/tcl8.6/tclx8.4/
%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf
%exclude %{_mandir}/man3/CmdWrite.*
%exclude %{_mandir}/man3/Handles.*
%exclude %{_mandir}/man3/TclXInit.3*
%exclude %{_mandir}/man3/Keylist.3*
%{_mandir}/mann/*
%{_mandir}/man3/*

%files devel
%{_includedir}/*
%{_mandir}/man3/TclXInit.3*
%{_mandir}/man3/Keylist.3*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.4.0-36
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan  2 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 8.4.0-27
- Fixed hardcoded TCL path in ld.so.conf.d

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.4.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 8.4.0-23
- Fixed build with tcl/tk-8.6 (by tcl86 patch)
- Fixed bogus dates in changelog (best effort)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jan 23 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 8.4.0-18
- Fixed multilib deps
  Resolves: rhbz#783891

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 29 2009 Nikola Pajkovsky <npajkovs@redhat.com> 8.4.0-15
- resolved: Bug 525058 -  ld.so not correctly configured after install

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 29 2008 Marcela Mašláňová <mmaslano@redhat.com> - 8.4.0-12
- review, thanks for help to Patrice Dumas

* Tue Sep 23 2008 Marcela Maslanova <mmaslano@redhat.com> - 8.4.0-11
- change macros

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 8.4.0-10
- Autorebuild for GCC 4.3

* Mon Jan  7 2008 Marcela Maslanova <mmaslano@redhat.com> - 8.4.0-9
- rebuild for tcl8.5

* Fri Aug 24 2007 Marcela Maslanova <mmaslano@redhat.com> - 8.4.0-8
- rebuild for mass rebuild, check license

* Tue Mar 20 2007 Marcela Maslanova <mmaslano@redhat.com> - 8.4.0-7
- rebuild for merge review

* Wed Mar 7 2007 Marcela Maslanova <mmaslano@redhat.com> - 8.4.0-6
- rebuild for merge review

* Mon Oct 2 2006 Marcela Maslanova <mmaslano@redhat.com> - 8.4.0-5
- rebuild

* Fri Sep 15 2006 Marcela Maslanova <mmaslano@redhat.com> - 8.4-4
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 8.4.0-3.1
- rebuild

* Thu Jun 29 2006 David Cantrell <dcantrell@redhat.com> - 8.4.0-3
- Unit tests broken, disabling for now (#197107)

* Thu Apr 20 2006 David Cantrell <dcantrell@redhat.com> - 8.4.0-2
- Rebuild against Tcl/Tk 8.4.13

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 8.4.0-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.4.0-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 03 2006 David Cantrell <dcantrell@redhat.com> - 8.4.0-1
- Upgraded to tclx-8.4.0
- Removed patches that applied to the old build method for tclx
- Removed Tcl and Tk doc archives

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  9 2005 Jens Petersen <petersen@redhat.com> - 8.3.5-6
- add unversioned symlinks to the static libs (Dave Botsch, 149734)
- rebuild with gcc 4
  - add tclx-8.3.5-clock_t-gcc4.patch to skip clock_t test in configure
  - buildrequire autoconf213

* Sun Feb 13 2005 Jens Petersen <petersen@redhat.com> - 8.3.5-5
- rebuild

* Thu Sep 30 2004 Jens Petersen <petersen@redhat.com> - 8.3.5-4
- buildrequire groff (Maxim Dzumanenko, 124554)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Mar 03 2004 Jens Petersen <petersen@redhat.com> - 8.3.5-2
- install using utf-8 locale so that tclhelp help files get built properly
  (#116804)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> - 8.3.5-1.1
- rebuilt

* Wed Feb 25 2004 Jens Petersen <petersen@redhat.com> - 8.3.5-1
- new package split out from tcltk
- update to 8.3.5 release
- update source url
- no longer need tclx-8.3-argv.patch and tclx-8.3-helpdir.patch
- new devel and doc subpackages
- set TCLX_INST_LIB for configure
- add symlink for libtkx.so too
- clean build remnants from tclxConfig.sh and tkxConfig.sh
- rename memory.n to Memory.n, since tcl provides memory.n
- move help and manpages to -doc subpackage
- filtered out non-tclx changelog entries
- define tcltk_ver and use it
- include copy of tcl and tk manpages for buildhelp and
  apply tclx-8.3.5-tcltk-man-help.patch to point at them

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-92
- rebuild again for #91211

* Fri Jan 17 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-85
- build all except tclx with _smp_mflags
- add some requires

* Tue Jan 14 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-84
- link all libs with DT_SONAME using tcl.m4 patch (#81297)
- drop synthetic lib provides
- remove obsolete patches from srpm
- update buildrequires
- use buildroot instead of RPM_BUILD_ROOT
- install all man pages under mandir, instead of moving some from /usr/man
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
- build and install tclx with _libdir (not libdir!)
- fix summary-not-capitalized for tclx, tcllib, tcl-html

* Mon Dec  9 2002 Jens Petersen <petersen@redhat.com> 8.3.5-76
- make it build on x86_64 (details below)
- don't explicitly update config.{guess,sub} since %%configure does it for us
- build and install tclx and tkx with INST_RUNTIME files under datadir, and
  EXEC_RUNTIME file under libdir
- generate filelists from datadir and not from mandir from now on

* Tue Dec  3 2002 Jens Petersen <petersen@redhat.com>
- update url for tcl, tk, tclx, itcl, tcllib
- build without all makecfg patches for now
  - in particular use upstream versioned library name convention
- add backward compatible lib symlinks for now
- use make's -C option rather than jumping in and out of source dirs
  during install
- use INSTALL_ROOT destdir-like make variable instead of makeinstall
  for all subpackages except tix and itcl

* Mon Oct 21 2002 Jens Petersen <petersen@redhat.com>
- move tclx HELP_DIR fix to separate patch

* Sat Jul 20 2002 Akira TAGOH <tagoh@redhat.com> 8.3.3-70
- tclx-8.3-nonstrip.patch: applied to fix the stripped binary issue.

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix config.guess and config.sub to newer versions

* Wed Aug  8 2001 Adrian Havill <havill@redhat.com>
- re-enable glibc string and math inlines; recent gcc is a-ok.
- optimize at -O2 instead of -O
- rename "soname" patches related to makefile/autoconf changes
- added elf "needed" for tk, tclx, tix, itk
- removed warnings from tclX

* Wed Jul 25 2001 Adrian Havill <havill@redhat.com>
- fixed 64 bit RPM provides for dependencies

* Thu Jul 19 2001 Adrian Havill <havill@redhat.com>
- updated tclX to the latest version
- fixed tclX 8.3's busted help install
- eliminated make TK_LIB kludge for multiple math libs for tclX
- used %%makeinstall to brute force fix any remaining unflexible makefile dirs

* Sun Jul  8 2001 Adrian Havill <havill@redhat.com>
- refresh all sources to latest stable (TODO: separate expect/expectk)
- massage out some build stuff to patches (TODO: libtoolize hacked constants)
- remove patches already rolled into the upstream
- removed RPATH (bugs 45569, 46085, 46086), added SONAMEs to ELFs
- changed shared object filenames to something less gross
- fixed tclX shell's argv parsing (bug 47710)

* Fri Mar 23 2001 Bill Nottingham <notting@redhat.com>
- bzip2 sources

* Mon Mar 19 2001 Bill Nottingham <notting@redhat.com>
- build with -D_GNU_SOURCE - fixes expect on ia64

* Tue Jun  6 2000 Jeff Johnson <jbj@redhat.com>
- tclX had wrong version.

* Fri Jun  2 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging changes.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Make changes from bug number 7602
- Apply patch from bug number 7537

* Tue Nov 30 1999 Jakub Jelinek <jakub@redhat.com>
- fix tclX symlinks.
- compile on systems where SIGPWR == SIGLOST.

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- upgrade tcl/tk/tclX to 8.0.4

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update tcl/tk/tclX to 8.0.3, expect is updated also.

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Mar 25 1998 Cristian Gafton <gafton@redhat.com>
- updated tclX to 8.0.2

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- fixed dangling tclx/tkx symlinks
