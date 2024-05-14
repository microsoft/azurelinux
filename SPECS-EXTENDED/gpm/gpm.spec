Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: A mouse server for the Linux console
Name: gpm
Version: 1.20.7
Release: 24%{?dist}
License: GPLv2
URL: https://www.nico.schottelius.org/software/gpm/
#URL2 : https://freecode.com/projects/gpm

# The upstream source contains PDF docs with unclear licensing,
# and that's why we need to remove them and recreate the tarball
#
# 1.] mkdir docs-removal && cd docs-removal
# 2.] wget https://www.nico.schottelius.org/software/gpm/archives/%{name}-%{version}.tar.lzma
# 3.] tar xf %{name}-%{version}.tar.lzma
# 4.] rm -rf %{name}-%{version}/doc/specs
# 5.] tar cJf %{name}-%{version}.tar.xz %{name}-%{version}

Source: %{_distro_sources_url}/%{name}-%{version}.tar.xz
Source1: gpm.service
Patch0: https://github.com/telmich/gpm/compare/1.20.7...4a938233fbe6de7af05aabc74891b68d4bae40f8.diff
# https://github.com/telmich/gpm/pull/37/
Patch3: f04f24dd5ca5c1c13608b144ab66e2ccd47f106a.patch
Patch1: gpm-1.20.6-multilib.patch
Patch2: gpm-1.20.1-lib-silent.patch
Patch4: gpm-1.20.5-close-fds.patch
Patch5: gpm-1.20.1-weak-wgetch.patch
Patch7: gpm-1.20.7-rhbz-668480-gpm-types-7-manpage-fixes.patch

# Disabled, need to be reviewed
Patch8: gpm-1.20.6-missing-header-dir-in-make-depend.patch
Patch9: gpm-1.20.6-capability.patch

Requires(post): systemd info
Requires(preun): systemd info
Requires(postun): systemd
# this defines the library version that this package builds.
%define LIBVER 2.1.0
BuildRequires: sed gawk texinfo bison ncurses-devel autoconf automake libtool libcap-ng-devel
BuildRequires: systemd
Requires: linuxconsoletools
Requires: %{name}-libs = %{version}-%{release}

%description
Gpm provides mouse support to text-based Linux applications like the
Emacs editor and the Midnight Commander file management system.  Gpm
also provides console cut-and-paste operations using the mouse and
includes a program to allow pop-up menus to appear at the click of a
mouse button.

%package libs
Summary: Dynamic library for for the gpm

%description libs
This package contains the libgpm.so dynamic library which contains
the gpm system calls and library functions.

%package devel
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Summary: Development files for the gpm library

%description devel
The gpm-devel package includes header files and libraries necessary
for developing programs which use the gpm library. The gpm provides
mouse support to text-based Linux applications.

%package static
Requires: %{name} = %{version}-%{release}
Summary: Static development files for the gpm library

%description static
The gpm-static package includes static libraries of gpm. The gpm provides
mouse support to text-based Linux applications.


%prep
%setup -q

%patch 0 -p1 -b .master
%patch 3 -p1 -b .gcc10
%patch 1 -p1 -b .multilib
%patch 2 -p1 -b .lib-silent
%patch 4 -p1 -b .close-fds
%patch 5 -p1 -b .weak-wgetch
%patch 7 -p1
# not sure if this is really needed
#patch8 -p1

#patch9 -p1 -b .capability

%build
./autogen.sh
%configure
%make_build

%install
%make_install

chmod 0755 %{buildroot}/%{_libdir}/libgpm.so.%{LIBVER}
ln -sf libgpm.so.%{LIBVER} %{buildroot}/%{_libdir}/libgpm.so

rm -f %{buildroot}%{_datadir}/emacs/site-lisp/t-mouse.el

%ifnarch s390 s390x
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}%{_unitdir}
install -m 644 conf/gpm-* %{buildroot}%{_sysconfdir}
# Systemd
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
rm -rf %{buildroot}%{_initrddir}
%else
# we're shipping only libraries in s390[x], so
# remove stuff from the buildroot that we aren't shipping
rm -rf %{buildroot}%{_sbindir}
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_mandir}
%endif

%post
%ifnarch s390 s390x
%systemd_post gpm.service
%endif

%preun
%ifnarch s390 s390x
%systemd_preun gpm.service
%endif

%postun
%ifnarch s390 s390x
%systemd_postun_with_restart gpm.service
%endif

%ldconfig_scriptlets libs

%files
%license COPYING
%doc README TODO
%doc doc/README* doc/FAQ doc/Announce doc/changelog
%{_infodir}/*
%ifnarch s390 s390x
%config(noreplace) %{_sysconfdir}/gpm-*
%{_unitdir}/gpm.service
%{_sbindir}/*
%{_bindir}/*
%{_mandir}/man?/*
%endif

%files libs
%{_libdir}/libgpm.so.*

%files devel
%{_includedir}/*
%{_libdir}/libgpm.so

%files static
%{_libdir}/libgpm.a

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.7-24
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.7-23
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.20.7-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Sat Feb 22 2020 Sérgio Basto <sergio@serjux.com> - 1.20.7-21
- Better comments in spec file

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
- Add upstream commits for git master which contains patches 9, 10 and 11
- Add GCC10 fix
- Cleanups

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 24 2019 Sérgio Basto <sergio@serjux.com> - 1.20.7-18
-  updating /var/run/gpm.pid → /run/gpm.pid (rhbz #1692104)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 1.20.7-15
- Use default build flags (PIE works now)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 10 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.20.7-13
- Include upstream pull request patches to fix FTBFS (BZ#1500092)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.20.7-8
- Drop old scriptlets causing FTBFS with new rpm

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 05 2014 Jaromir Capik <jcapik@redhat.com> - 1.20.7-4
- Fixing format-security flaws (#1037099)

* Wed Aug 07 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.7-3
- Removing PDF docs with unclear licensing from the source archive
- Fixing the license tag

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.7-1
- Update to 1.20.7

* Wed Jul 03 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.6-33
- Replacing systemd unit path with _unitdir macro

* Wed Jul 03 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.6-32
- Fixing full RELRO ... bind_now -> now (#884017)

* Mon Apr 08 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.6-31
- fixing bogus dates in the changelog

* Thu Mar 28 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.6-30
- aarch64 support (#925474)

* Wed Mar 06 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.6-29
- Removing OPTFLAGS
- Introducing full RELRO
- Missing header dir in Makefile.in / depend
- Fixing UsrMove for i686 (mv -f says 'directory not empty')

* Wed Mar 06 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.6-28
- Adding missing requires
- Passing OPTFLAGS to make
- UsrMove

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 03 2013 Jaromir Capik <jcapik@redhat.com> - 1.20.6-26
- Removing bundled 'inputattach' tool (#875604)
- ...gonna be shipped separately (linuxconsoletools)

* Mon Sep 17 2012 Václav Pavlín <vpavlin@redhat.com> - 1.20.6-25
- Scriptlets replaced with new systemd macros (#850134)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 16 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.20.6-23
- Add w8001 support to inputattach (#645235)

* Tue Jan 24 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.20.6-22
- 668480 - gpm-types(7) manpage fixes

* Tue Jan 24 2012 Nikola Pajkovsky <npajkovs@redhat.com> - 1.20.6-21
- 753627 - Get an error message when installing the gpm package via yum

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Dec  4 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.20.6-19
- Move scriptlet ldconfig calls from main package to -libs.

* Fri Aug 05 2011 Nikola Pajkovsky <npajkovs@redhat.com> 1.20.6-18
- unpackaged files (do not install t-mouse.el)

* Tue Jul 26 2011 Jóhann B. Guðmundsson <johannbg@gmail.com> - 1.20.6-17
- Drop SysV support

* Thu May 05 2011 Bill Nottingham <notting@redhat.com> 1.20.6-16
- Fix systemd scriptlets

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 25 2010 Nikola Pajkovsky <npajkovs@redhat.com> 1.20.6-14
- fix url and source0(yaneti@declera.com)

* Tue Oct 19 2010 Nikola Pajkovsky <npajkovs@redhat.com> 1.20.6-13
- 644318 - Incomplete systemd service file for gpm(yaneti@declera.com)

* Mon Oct 18 2010 Nikola Pajkovsky <npajkovs@redhat.com> 2.20.6-12
- disable debuging mode in gpm.service

* Thu Aug 19 2010 Nikola Pajkovsky <npajkovs@redhat.com> 1.20.6-11
- Resolved: #617327, #622665, #624253

* Wed Aug 11 2010 Nikola Pajkovsky <npajkovs@redhat.com> 1.20.6-10
- Providing native systemd file for upcoming F14 Feature Systemd

* Thu Dec 10 2009 Nikola Pajkovsky <npajkovs@redhat.com> 1.20.6-9
- add try-restart into gpm.init to be more LSB-compilant

* Thu Nov 19 2009 Nikola Pajkovsky <npajkovs@redhat.com> 1.20.6-8
- drop patch7
- resolved #537724(does not work with capabilities)

* Wed Sep 30 2009 Nikola Pajkovsky <npajkovs@redhat.com> 1.20.6-7
- add BuildRequires: libcap-ng-devel
- fix patch .capability

* Thu Aug 20 2009 Zdenek Prikryl <zprikryl@redhat.com> 1.20.6-6
- Don't complain if installing with --excludedocs (#515927)
- Drop unnecessary capabilities in gpm (#517659)

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.20.6-5
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Zdenek Prikryl <zprikryl@redhat.com> 1.20.6-3
- created new subpackage gpm-libs (#495124)

* Tue Feb 24 2009 Zdenek Prikryl <zprikryl@redhat.com> - 1.20.6-2
- Fixed gpm.info.gz building

* Tue Feb 03 2009 Zdenek Prikryl <zprikryl@redhat.com> - 1.20.6-1
- Spec review (#225856)
- Updated to 1.20.6

* Tue Dec 02 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.20.5-2
- Fixed debug mode (#473422)
- Fixed description in init script (#474337)

* Thu Jul 17 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.20.5-1
- Updated to 1.20.5
- Removed doc patch
- Removed lisp stuff, it is part of emacs-common now 
- Spec clean up

* Wed Jun 04 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.20.3-2
- Enable gpm in runlevel 5

* Thu May 29 2008 Zdenek Prikryl <zprikryl@redhat.com> - 1.20.3-1
- Updated to 1.20.3
- Fixed init script to comply with LSB standard (#246937)
- Mass patch cleanup
- Fixed typo in doc (#446679)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.20.1-90
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-89
- license tag update (and rebuild for BuildID, etc.)

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 1.20.1-88
- Rebuild for RH #249435

* Tue Jul 24 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-87
- replace OPEN_MAX with sysconf(_SC_OPEN_MAX), fixing build with 2.6.23 kernel

* Tue Jul 24 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-86
- don't install t-mouse.el, emacs-common contains a newer version,
  fixes #249362

* Fri Jun 29 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-85
- applied patch for #246219, fixing segfault with vsyslog on x86_64

* Wed May 23 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-84
- applied patch for #240389, fixing default handlers

* Thu May 03 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-83
- gpm-devel now requires version-release correctly, fixes #238785

* Mon Apr 02 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-82
- updated inputattach.c to 1.24 from cvs, fixes #231635

* Fri Mar 23 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-81
- the patch for #168076 caused a strange behaviour with ncurses, fixed it
  differently

* Mon Jan 22 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-80
- forgot to add the patch for #168076

* Mon Jan 22 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-79
- added disttag to release

* Mon Jan 22 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-78
- refuse connections while waiting for console, fixes #168076

* Mon Jan 22 2007 Tomas Janousek <tjanouse@redhat.com> - 1.20.1-77
- #223696: non-failsafe install-info use in scriptlets

* Tue Oct 10 2006 Petr Rockai <prockai@redhat.com> - 1.20-1-76
- align sleeps to tick boundary, should reduce cpu wakeups
  on laptops, fixes #205064 (patch by Arjan van de Ven)
- disable gpm altogether in runlevel 5, it is probably not
  worth the overhead considering it is barely used at all

* Fri Sep 22 2006 Petr Rockai <prockai@redhat.com> - 1.20.1-75
- fix a bug where gpm daemon kept stdin/out/err open after
  detaching from terminal, causing eg. pipes from initscript
  to hang for the lifetime of gpm

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.20.1-74.1
- rebuild

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1.20.1-74
- rebuild for -devel deps

* Mon Feb 13 2006 Petr Rockai <prockai@redhat.com> - 1.20.1-73.3
- rebuild due to failure on x86-64 (possibly a glitch?)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.20.1-73.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.20.1-73.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Petr Rockai <prockai@redhat.com> 1.20.1-73
- do not ooops in gpm when console device cannot be found, print
  an error message instead and exit(1), as per BR 140025, 176178
- do not print messages in libgpm, unless envvar GPM_VERBOSE
  is set -- avoids unwanted clutter from libgpm in apps like dialog
  or mc when gpm is not available

* Thu Dec 22 2005 Jesse Keating <jkeating@redhat.com> 1.20.1-72
- rebuilt again

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt
- added autoconf as a BuildReq

* Fri Mar 04 2005 Petr Rockai <prockai@redhat.com>
- rebuilt

* Mon Feb 14 2005 Adrian Havill <havill@redhat.com>
- rebuilt

* Thu Oct 21 2004 Adrian Havill <havill@redhat.com> 1.20.1-66
- avoid spawning multiple copies of inputattach, and kill process
  when gpm shuts down (#135776)

* Wed Oct 20 2004 Bill Nottingham <notting@redhat.com> 1.20.1-65
- remove buildroot paths from gpm.info, fixing #135305

* Wed Oct 20 2004 Adrian Havill <havill@redhat.com> 1.20.1-64
- fixing multilib conflict (#135305):
  o remove buildsys check/conditional for gziping info pages (let rpm
    do it)
  o don't pre-byte-compile emacs code

* Thu Oct 14 2004 Bill Nottingham <notting@redhat.com> 1.20.1-62
- fix remaining sourcing of /etc/sysconfig/gpm (#135776)

* Wed Oct 13 2004 Adrian Havill <havill@redhat.com> 1.20.1-61
- remove unnecessary diagnostic and check of the consolename (#129962)
- remove /etc/sysconfig/gpm; set unset defaults in the init script instead
  after mousecfg is (or is not) read

* Wed Oct 13 2004 Florian La Roche <laroche@redhat.com>
- sysconfig/gpm should probably go away, that is more confusing than
  helping anyone
- read at least sysconfig/gpm first as it seems to have the default values
  and sysconfig/mouse is getting probed values and probably has better
  settings in it.

* Tue Oct 12 2004 Adrian Havill <havill@redhat.com> 1.20.1-57
- read both the sysconfig/mouse and sysconfig/gpm (preferrence to gpm
  settings), not just one of them, if both exist (#134389)

* Tue Oct 12 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- remove gzip of info pages within .spec file, #135305

* Sat Oct 09 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- initscript cleanup

* Thu Sep 23 2004 Adrian Havill <havill@redhat.com> 1.20.1-54
- change init so that MOUSECFG fallsback to /etc/sysconfig/gpm if
  /etc/sysconfig/mouse doesn't exist (#133141)
- fixed compile vs new kernheaders (#131783)

* Tue May 04 2004 Adrian Havill <havill@redhat.com> 1.20.1-49
- remove superfluous "i die" msg (#121845)

* Tue May 04 2004 Adrian Havill <havill@redhat.com> 1.20.1-48
- restore gpmopen() NULL check that was removed with the
  evdev superpatch (#118554)

* Fri Apr 16 2004 Adrian Havill <havill@redhat.com> 1.20.1-47
- make presence of t-mouse.el flexible (#120958)

* Wed Mar 31 2004 Adrian Havill <havill@redhat.com> 1.20.1-46
- revise nodebug patch as liblow reporting the VC to the console through
  stderr has re-appeared (#117676)

* Mon Mar 22 2004 Adrian Havill <havill@redhat.com> 1.20.1-45
- remove circular ncurses dep for prelink by restoring wgetch
  patch (#117150)

* Wed Mar 17 2004 Bill Nottingham <notting@redhat.com> 1.20.1-44
- include inputattach
- if configured mouse has IMOUSETYPE, use inputattach

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Adrian Havill <havill@redhat.com> 1.20.1-43
- add event device (for 2.6 kernel) superpatch-- includes all
  patches up to release 38; thanks to Dmitry Torokhov
- change default mouse device over to /dev/input/mice
- set mouse type to Intellimouse Explorer (exps2), which is what
  the 2.6 kernel exports by default

* Sat Feb 14 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- already add shared lib symlinks at install time
- fix subscript #114289

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Nov 18 2003 Adrian Havill <havill@redhat.com> 1.20.1-39
- re-add the $OPTIONS that gets pulled in from /etc/sysconfig/gpm
  to the init.d script (#110248)

* Thu Aug 07 2003 Adrian Havill <havill@redhat.com> 1.20.1-38
- Gpm_Open() NULL deref revisited (#101104). Patch by
  <leonardjo@hetnet.nl>
* Wed Jul 30 2003 Adrian Havill <havill@redhat.com> 1.20.1-37
- removed auto-add of repeat with -M (#84310)

* Tue Jul 29 2003 Adrian Havill <havill@redhat.com> 1.20.1-36
- fixed grammar typos in the init script (#89109)
- don't deref NULL string in Gpm_Open (#101104)

* Wed Jul 02 2003 Adrian Havill <havill@redhat.com> 1.20.1-35
- remove debug output from gpm_report() to prevent spurious
  debugging msgs even when not in debug mode (#98210)
  
* Thu Jun 26 2003 Adrian Havill <havill@redhat.com> 1.20.1-33
- reversed -t and -m params in init script, removed $OPTION
- add doc blurb regarding no auto-repeat with multiple mice

* Tue Jun 24 2003 Adrian Havill <havill@redhat.com> 1.20.1-32
- update version
- add -lm for ceil()
- add hltest, mouse-test for all but zSeries

* Mon Jun 16 2003 Jakub Jelinek <jakub@redhat.com>
- don't link against -lncurses, instead make wgetch and stdscr weak
  undefined symbols to break library dependency cycle

* Thu Jun 12 2003 Elliot Lee <sopwith@redhat.com>
- Remove pam requirement

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 29 2003 Bill Nottingham <notting@redhat.com> 1.19.13-27
- ship libraries on s390/s390x

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan 13 2003 Bill Nottingham <notting@redhat.com> 1.19.13-25
- don't automatically enable the repeater when '-M' is in use

* Fri Nov 22 2002 Tim Powers <timp@redhat.com>
- remove unpackaged files from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Apr  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 
- Revert to the version from 7.2 because later versions have some grave
  issues I can't {reproduce,debug} with my hardware, such as
  #62540 and #61691

* Thu Jul 19 2001 Preston Brown <pbrown@redhat.com>
- more documentation fixes for Netmouse type devices (#48885)

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add link from library major version number

* Mon Jun 25 2001 Preston Brown <pbrown@redhat.com>
- small fixlet in init script (#36995)

* Tue Jun 19 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add ExcludeArch: s390 s390x

* Fri Apr  6 2001 Preston Brown <pbrown@redhat.com>
- work better with unsupported devfs (#23500, #34883)

* Mon Feb 05 2001 Karsten Hopp <karsten@redhat.de>
- found another bug: tmpfile was never removed if
  gpm was already running

* Mon Feb 05 2001 Karsten Hopp <karsten@redhat.de>
- really fix tmpfile path

* Mon Feb 05 2001 Karsten Hopp <karsten@redhat.de>
- fix tmpfile path (bugzilla  #25967)

* Tue Jan 30 2001 Preston Brown <pbrown@redhat.com>
- don't make PID file world-writable.

* Mon Jan 29 2001 Preston Brown <pbrown@redhat.com>
- fix up devel dependency on main package

* Sun Jan 28 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Don't crash if we can't open /dev/console
  (Happens with some devfs enabled kernels)

* Tue Jan 23 2001 Trond Eivind Glomsr�d <teg@redhat.com>
- fix bug in i18n of initscript

* Tue Jan 23 2001 Preston Brown <pbrown@redhat.com>
- bash2 style of i18n for initscript

* Wed Jan 17 2001 Preston Brown <pbrown@redhat.com>
- i18n the initscript.

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add hooks for extra options in /etc/sysconfig/gpm (#23547)

* Fri Jan 05 2001 Preston Brown <pbrown@redhat.com>
- patch added to abort if running on a serial console (#15784)

* Fri Jul 28 2000 Preston Brown <pbrown@redhat.com>
- cleaned up post section

* Wed Jul 26 2000 Preston Brown <pbrown@redhat.com>
- clarification: pam requirement added to fix permissions on /dev/gpmctl (#12849)

* Sat Jul 22 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.19.3

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Fri Jun 30 2000 Matt Wilson <msw@redhat.com>
- use sysconf(_SC_OPEN_MAX)

* Tue Jun 27 2000 Preston Brown <pbrown@redhat.com>
- don't prereq, only require initscripts

* Mon Jun 26 2000 Preston Brown <pbrown@redhat.com>
- fix up and move initscript
- prereq initscripts >= 5.20

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- fix %%config tag for initscript

* Thu Jun 15 2000 Bill Nottingham <notting@redhat.com>
- move it back

* Thu Jun 15 2000 Preston Brown <pbrown@redhat.com>
- move init script

* Wed Jun 14 2000 Preston Brown <pbrown@redhat.com>
- security patch on socket descriptor from Chris Evans.  Thanks Chris.
- include limits.h for OPEN_MAX

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- 1.19.2, fix up root (setuid) patch
- FHS paths

* Thu Apr  6 2000 Jakub Jelinek <jakub@redhat.com>
- 1.19.1
- call initgroups in gpm-root before spawning command as user
- make gpm-root work on big endian

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- call ldconfig directly in postun

* Wed Mar 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new libncurses

* Sat Mar 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.19.0
- fix build on systems that don't have emacs
  (configure built t-mouse* only if emacs was installed)

* Tue Feb 29 2000 Preston Brown <pbrown@redhat.com>
- important fix: improperly buildrooted for /usr/share/emacs/site-lisp, fixed.

* Tue Feb 15 2000 Jakub Jelinek <jakub@redhat.com>
- avoid cluttering of syslog with gpm No data messages

* Mon Feb 14 2000 Preston Brown <pbrown@redhat.com>
- disable-paste and mouse-test removed, they seem broken.

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- updated gpm.init to have better shutdown and descriptive messages
- strip lib

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Wed Jan 12 2000 Preston Brown <pbrown@redhat.com>
- 1.18.1.

* Tue Sep 28 1999 Preston Brown <pbrown@redhat.com>
- upgraded to 1.18, hopefully fixes sparc protocol issues

* Fri Sep 24 1999 Bill Nottingham <notting@redhat.com>
- install-info sucks, and then you die.

* Fri Sep 10 1999 Bill Nottingham <notting@redhat.com>
- chkconfig --del in %%preun, not %%postun

* Fri Aug 27 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.17.9
- the maintainers are taking care of .so version now, removed patch

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Wed Jun  2 1999 Jeff Johnson <jbj@redhat.com>
- disable-paste need not be setuid root in Red Hat 6.0 (#2654)

* Tue May 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- gpm.init had wrong pidfile name in comments; confused linuxconf

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- make sure all binaries are stripped, make init stuff more chkconfig style
- removed sparc-specific mouse stuff
- bumped libver to 1.17.5
- fixed texinfo source

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Thu Mar  4 1999 Matt Wilson <msw@redhat.com>
- updated to 1.75.5

* Tue Feb 16 1999 Cristian Gafton <gafton@redhat.com>
- avoid using makedev for internal functions (it is a #define in the system
  headers)

* Wed Jan 13 1999 Preston Brown <pbrown@redhat.com>
- upgrade to 1.17.2.

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- enforce the use of -D_GNU_SOURCE so that it will compile on the ARM
- build against glibc 2.1

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Wed Apr 22 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscript

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- recompiled for manhattan

* Wed Apr 08 1998 Erik Troan <ewt@redhat.com>
- updated to 1.13

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- added patch from Richard to get things to build on the SPARC

* Tue Oct 28 1997 Donnie Barnes <djb@redhat.com>
- fixed the emacs patch to install the emacs files in the right
  place (hopefully).

* Mon Oct 13 1997 Erik Troan <ewt@redhat.com>
- added chkconfig support
- added install-info

* Thu Sep 11 1997 Donald Barnes <djb@redhat.com>
- upgraded from 1.10 to 1.12
- added status/restart functionality to init script
- added define LIBVER 1.11

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
