# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh8)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
%global majorver 5.45.4

Summary: A program-script interaction and testing utility
Name: expect
Version: %{majorver}
Release: 29%{?dist}
License: LicenseRef-Fedora-Public-Domain
URL: https://core.tcl.tk/expect/index
Source: http://downloads.sourceforge.net/%{name}/%{name}%{version}.tar.gz
Buildrequires: gcc autoconf automake chrpath
BuildRequires: tcl-devel < 1:9
BuildRequires: make
# Patch0: fixes change log file permissions
Patch0: expect-5.43.0-log_file.patch
# Patch1: fixes install location, change pkgIndex
Patch1: expect-5.43.0-pkgpath.patch
# Patch2: fixes minor man page formatting issue
Patch2: expect-5.45-man-page.patch
# Patch3: fixes segmentation fault during matching characters
Patch3: expect-5.45-match-gt-numchars-segfault.patch
# Patch4: fixes memory leak when using -re, http://sourceforge.net/p/expect/patches/13/
Patch4: expect-5.45-re-memleak.patch
# Patch5: use vsnprintf instead of vsprintf to avoid buffer overflow
Patch5: expect-5.45-exp-log-buf-overflow.patch
# Patch6: fixes segfaults if Tcl is built with stubs and Expect is used directly
#   from C program rhbz#1091060
Patch6: expect-5.45-segfault-with-stubs.patch
# Patch7: fixes leaked fd, patch by Matej Mužila, rhbz#1001220
Patch7: expect-5.45-fd-leak.patch
# Patch8: unificates usage message of expect binary and man page, adds -h flag
Patch8: expect-5.45.4-unification-of-usage-and-man-page.patch
# Patch9: fixes issues detected by static analysis
Patch9: expect-5.45.4-covscan-fixes.patch
# examples patches
# Patch100: changes random function
Patch100: expect-5.32.2-random.patch
# Patch101: fixes bz674184 - mkpasswd fails randomly
Patch101: expect-5.45-mkpasswd-dash.patch
# Patch102: fixes bz703702 - let user know that telnet is needed for
# running some examples
Patch102: expect-5.45-check-telnet.patch
# Patch103: use full path to 'su', it's safer
Patch103: expect-5.45-passmass-su-full-path.patch
# Patch104: rhbz 963889, fixes inaccuracy in mkpasswd man page
Patch104: expect-5.45-mkpasswd-man.patch
# Patch105: Fix error with -Werror=format-security
Patch105: expect-5.45-format-security.patch
Patch106: expect-configure-c99.patch
Patch107: expect-c99.patch
# Patch108: fix tclsh path for 'example' binaries (tcl8 compat package has no 'tclsh')
Patch108: expect-5.45.4-tclsh8.patch

%description
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains expect and some scripts that use it.

%package devel
Summary: A program-script interaction and testing utility
Requires: expect = %{version}-%{release}

%description devel
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package contains development files for the expect library.

%package -n expectk
Summary: A program-script interaction and testing utility
Requires: expect = %{version}-%{release}

%description -n expectk
Expect is a tcl application for automating and testing
interactive applications such as telnet, ftp, passwd, fsck,
rlogin, tip, etc. Expect makes it easy for a script to
control another program and interact with it.

This package originally contained expectk and some scripts
that used it. As expectk was removed from upstream tarball
in expect-5.45, now the package contains just these scripts.
Please use tclsh with package require Tk and Expect instead
of expectk.

%prep
%setup -q -n expect%{version}
%patch -P0 -p1 -b .log_file
%patch -P1 -p1 -b .pkgpath
%patch -P2 -p1 -b .man-page
%patch -P3 -p1 -b .match-gt-numchars-segfault
%patch -P4 -p1 -b .re-memleak
%patch -P5 -p1 -b .exp-log-buf-overflow
%patch -P6 -p1 -b .segfault-with-stubs
%patch -P7 -p1 -b .fd-leak
%patch -P8 -p1 -b .unification-of-usage-and-man-page
%patch -P9 -p1 -b .covscan-fixes
# examples fixes
%patch -P100 -p1 -b .random
%patch -P101 -p1 -b .mkpasswd-dash
%patch -P102 -p1 -b .check-telnet
%patch -P103 -p1 -b .passmass-su-full-path
%patch -P104 -p1 -b .mkpasswd-man
%patch -P105 -p0 -b .format-security
%patch -P106 -p1 -b .configure-c99
%patch -P 107 -p1
%patch -P 108 -p1 -b .tclsh
# -pkgpath.patch touch configure.in
aclocal
autoconf
( cd testsuite
  autoconf -I.. )

%build
export CFLAGS="$RPM_OPT_FLAGS -std=gnu17"
%configure --with-tcl=%{_libdir} --with-tk=%{_libdir} --enable-shared \
	--with-tclinclude=%{_includedir}/tcl-private/generic
make %{?_smp_mflags}

%check
make test

%install
rm -rf "$RPM_BUILD_ROOT"
make install DESTDIR="$RPM_BUILD_ROOT"

# move
mv "$RPM_BUILD_ROOT"%{tcl_sitearch}/expect%{version}/libexpect%{version}.so "$RPM_BUILD_ROOT"%{_libdir}

# for linking with -lexpect
ln -s libexpect%{majorver}.so "$RPM_BUILD_ROOT"%{_libdir}/libexpect.so

# remove cryptdir/decryptdir, as Linux has no crypt command (bug 6668).
rm -f "$RPM_BUILD_ROOT"%{_bindir}/{cryptdir,decryptdir}
rm -f "$RPM_BUILD_ROOT"%{_mandir}/man1/{cryptdir,decryptdir}.1*
rm -f "$RPM_BUILD_ROOT"%{_bindir}/autopasswd

# rename mkpasswd, as it collides with more powerful variant from whois package (bug 1649456)
mv "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd-expect
mv "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd.1 "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd-expect.1
sed -i 's/mkpasswd/mkpasswd-expect/g;s/MKPASSWD/MKPASSWD-EXPECT/g' "$RPM_BUILD_ROOT"%{_mandir}/man1/mkpasswd-expect.1
sed -i 's/mkpasswd/mkpasswd-expect/g' "$RPM_BUILD_ROOT"%{_bindir}/mkpasswd-expect

# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libexpect%{version}.so


%files
%doc FAQ HISTORY NEWS README
%{_bindir}/expect
%{_bindir}/autoexpect
%{_bindir}/dislocate
%{_bindir}/ftp-rfc
%{_bindir}/kibitz
%{_bindir}/lpunlock
%{_bindir}/mkpasswd-expect
%{_bindir}/passmass
%{_bindir}/rftp
%{_bindir}/rlogin-cwd
%{_bindir}/timed-read
%{_bindir}/timed-run
%{_bindir}/unbuffer
%{_bindir}/weather
%{_bindir}/xkibitz
%dir %{tcl_sitearch}/expect%{version}
%{tcl_sitearch}/expect%{version}/pkgIndex.tcl
%{_libdir}/libexpect%{version}.so
%{_libdir}/libexpect.so
%{_mandir}/man1/autoexpect.1.gz
%{_mandir}/man1/dislocate.1.gz
%{_mandir}/man1/expect.1.gz
%{_mandir}/man1/kibitz.1.gz
%{_mandir}/man1/mkpasswd-expect.1.gz
%{_mandir}/man1/passmass.1.gz
%{_mandir}/man1/unbuffer.1.gz
%{_mandir}/man1/xkibitz.1.gz

%files devel
%{_mandir}/man3/libexpect.3*
%{_includedir}/*

%files -n expectk
%{_bindir}/multixterm
%{_bindir}/tknewsbiff
%{_bindir}/tkpasswd
%{_bindir}/xpstat
%{_mandir}/man1/multixterm.1*
%{_mandir}/man1/tknewsbiff.1*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 05 2025 Adam Williamson <awilliam@redhat.com> - 5.45.4-28
- Fix tclsh path for 'example' binaries like unbuffer

* Fri Jan 31 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-27
- Switch to the compat tcl8/tk8

* Tue Jan 28 2025 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-26
- Fix FTBFS

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Florian Weimer <fweimer@redhat.com> - 5.45.4-21
- Use Tcl 8.4 channel type (GCC 14 compatibility)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 29 2023 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-19
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 18 2022 Florian Weimer <fweimer@redhat.com> - 5.45.4-17
- Update configure for building in strict C99 mode

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov 22 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-8
- Rename mkpasswd to mkpasswd-expect
  Resolves: #1649456

* Wed Oct 10 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-7
- Fix issues detected by static analysis

* Wed Aug 29 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-6
- Unificate and improve both man page and usage message of expect

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.45.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-4
- Fix wrong log file permissions

* Wed Jun 20 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-3
- Fix upstream URL

* Tue Feb 27 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-2
- Add BuildRequires gcc

* Tue Feb 06 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.4-1
- New upstream release 5.45.4
  Resolves: #1541735

* Mon Oct 23 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45.3-1
- New upstream release 5.45.3
  Resolves: #1503372
- Removed 'Group' tag from spec file

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.45-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.45-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 24 2017 Nils Philippsen <nils@redhat.com> - 5.45-26
- remove unnecessary tk-devel and libXft-devel build dependencies

* Tue Mar 28 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-25
- tknewsbiff man page should be only in expectk - removed its duplicate
  from expect package

* Fri Mar 24 2017 Stephen Gallagher <sgallagh@redhat.com> - 5.45-24
- Fix build failures with -Werror=format-security

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.45-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.45-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 05 2016 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-21
- Replace 'define' with 'global'

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.45-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 20 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-19
- Use different and probably better approach of fixing segfaults if Tcl is
  built with stubs and Expect is used directly from C program

* Tue Sep 09 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-18
- Fix leaked fd (patch by Matej Mužila)
  Resolves: #1001220

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.45-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.45-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 5.45-15
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Mon Apr 28 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-14
- Fix segfaults if Tcl is built with stubs and Expect is used directly from C program
  (patch taken from Debian project, written by Sergei Golovan)

* Thu Dec 12 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-13
- Use vsnprintf instead of vsprintf to avoid buffer overflow
  (it happens e.g. when running systemtap testsuite)

* Wed Oct 02 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-12
- Fix memory leak when using -re option

* Tue Aug 27 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-11
- Fix inaccuracy in mkpasswd man page
  Resolves: #963889

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.45-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 04 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-9
- Fix repeated words in man pages

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.45-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.45-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 06 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-6
- Fix character matching to avoid segmentation fault
- Move libexpect link out of -devel subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.45-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 06 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-4
- Let user know when expample script needs telnet and it is missing
  Resolves: #703702
- Use full path to 'su' in passmass example, it's safer
- Fix expect man page minor formatting issue

* Wed Mar 16 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-3
- Fix mkpasswd fails randomly
  Resolves: #674184

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.45-1
- Update to expect-5.45

* Wed Mar 10 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.44.1.15-1
- Update to 5.44.1.15 from upstream CVS
  Resolves: #528654, Resolves: #501820
- Remove config.sub (no longer needed), remove unused patches (few are
  upstream now, few are pointless with new version), comment patches
- Fix unbuffer to return exit code of ubuffered program
  Resolves: #547686
- Fix Tk initialization
  Resolves: #456738

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 5.43.0-19
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.43.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.43.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Vitezslav Crhonek <vcrhonek@redhat.com> - 5:43.0-16
- Modify and rebuild for new Tcl

* Thu Sep 25 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 5:43.0-15
- Rediff all patches to work with patch --fuzz=0

* Mon Jun  9 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 5:43.0-14
- Use latest config.sub file for package build
  Resolves: #449560

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 5:43.0-13
- Rebuild

* Mon Jan 14 2008 Wart <wart@kobold.org> - 5.43.0-12
- Update install locations to reflect updated auto_path in the tcl 8.5 package

* Mon Jan 07 2008 Adam Tkac <atkac redhat com> - 5.43.0-11
- updated "tcl8.5" patch

* Sat Jan  5 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 5.43.0-10
- Rebuild for new Tcl 8.5

* Thu Aug 23 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 5.43.0-9
- rebuild

* Sat Feb 10 2007 Jakub Jelinek <jakub@redhat.com> - 5.43.0-8
- Update to build this time with Tcl 8.4

* Thu Feb  8 2007 Miloslav Trmac <mitr@redhat.com> - 5.43.0-7
- s/%%{buildroot}/"$RPM_BUILD_ROOT"/g
- s,/usr/share/man,%%{_mandir},g
- Use the Fedora-specified Buildroot:
- Remove BuildRequires: libX11-devel
- Don't install pkgIndex.tcl as an executable file
- Drop the incorrect expect-5.32.2-fixcat.patch
- Remove comments from *.h.in because they confuse config.status; this makes
  the workaround expect-5.43.0-cfg-setpgrp.patch unnecesary.

* Sat Feb  3 2007 Miloslav Trmac <mitr@redhat.com> - 5.43.0-6
- Update to build with Tcl 8.5
- Drop static libraries
- Ship more documentation
- Use %%check for (make test), remove the conditional

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.43.0-5.1
- rebuild

* Mon May 15 2006 David Cantrell <dcantrell@redhat.com> - 5.43.0-5
- BuildRequires libX11-devel

* Fri Feb 24 2006 David Cantrell <dcantrell@redhat.com> - 5.43.0-4
- Patch expLogChannelOpen() to create files with 0666 permissions (#182724)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.43.0-3.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 David Cantrell <dcantrell@redhat.com> - 5.43.0-3
- Rebuilt

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue May 31 2005 Jens Petersen <petersen@redhat.com> - 5.43.0-2
- fix flushing of unbuffer script (Charles Sullivan, #143963)
  with unbuffer-child-flush-143963.patch (Don Libes)
- make autoconf include parent dir in testsuite to avoid error
  (Robert Scheck, 150369)
- separate the examples scripts patches from the rest

* Mon Mar  7 2005 Jens Petersen <petersen@redhat.com>
- replace expect-5.32.2-setpgrp.patch by expect-5.43.0-cfg-setpgrp.patch
  to set SETPGRP_VOID correctly

* Mon Mar  7 2005 Jens Petersen <petersen@redhat.com> - 5.43.0-1
- run test make target by default
  - can be turned off with --without check

* Sat Mar 05 2005 Robert Scheck <redhat@linuxnetz.de>
- update to 5.43.0 (150369)
  - no longer need expect-5.39.0-64bit-82547.patch,
    expect-5.38.0-autopasswd-9917.patch
    and expect-5.42-mkpasswd-verbose-user-141454.patch
- run aclocal and configure with current autoconf (116777)
  - buildrequire autoconf and automake instead of autoconf213

* Fri Dec  3 2004 Jens Petersen <petersen@redhat.com> - 5.42.1-2
- fix "mkpasswd -v" failure when user not specified with
  expect-5.42-mkpasswd-verbose-user-141454.patch (J F Wheeler, 141454)

* Thu Aug  5 2004 Jens Petersen <petersen@redhat.com> - 5.42.1-1
- update to 5.42.1 (Robert Scheck, 126536)
  - no longer need expect-5.32.2-kibitz.patch
  - update expect-5.38.0-autopasswd-9917.patch
- drop explicit tcl and tk requires

* Mon Jun 21 2004 Alan Cox <alan@redhat.com>
- Autopasswd doesnt work and isnt ever going to work with pam around
  since password setting depends on the modules in use (think "fingerprint"
  or "smartcard"..). Remove it.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 28 2003 Jens Petersen <petersen@redhat.com> - 5.39.0-95
- new package split out from tcltk
- build against installed tcl and tk
- filtered changelog for expect
- buildrequire autoconf213 (#110583) [mvd@mylinux.com.ua]

* Mon Nov 17 2003 Thomas Woerner <twoerner@redhat.com> 8.3.5-94
- fixed RPATH for expect and expectk: expect-5.39.0-libdir.patch

* Wed Oct 15 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-93
- update expect to 5.39.0 (fixes #58317)
- drop first hunk of 64bit patch and rename to expect-5.39.0-64bit-82547.patch
- expect-5.32.2-weather.patch and expect-5.32.2-expectk.patch no longer needed

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-92
- rebuild again for #91211

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 8.3.5-91
- rebuild to fix gzipped file md5sums (#91211)

* Fri Jul 04 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-90
- make sure expect and itcl are linked against buildroot not installroot libs

* Tue Jan 28 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-87
- bring back expect alpha patch, renamed to 64bit patch (#82547)

* Fri Jan 17 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-85
- add some requires

* Tue Jan 14 2003 Jens Petersen <petersen@redhat.com> - 8.3.5-84
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

* Mon Dec  9 2002 Jens Petersen <petersen@redhat.com> 8.3.5-76
- make it build on x86_64 (details below)
- add 100 to expect patches
- patch expect configure to get EXP_LIB_SPEC to use libdir
- don't explicitly update config.{guess,sub} since %%configure does it for us
- added "--without check" rpmbuild option to disable running tests in future
- generate filelists from datadir and not from mandir from now on

* Tue Dec  3 2002 Jens Petersen <petersen@redhat.com>
- build without all makecfg patches for now
  - in particular use upstream versioned library name convention
- add backward compatible lib symlinks for now
- add unversioned symlinks for versioned bindir files
- use make's -C option rather than jumping in and out of source dirs
  during install
- use INSTALL_ROOT destdir-like make variable instead of makeinstall
  for all subpackages except tix and itcl

* Mon Oct 21 2002 Jens Petersen <petersen@redhat.com>
- move expectk and expect-devel files out of expect into separate packages
  (#9832)
- drop the crud compat dir symlinks in libdir
- correct expect license
- don't explicitly provide 64bit libs on ia64 and sparc64

* Tue Aug 20 2002 Jens Petersen <petersen@redhat.com> 8.3.3-74
- fix compat symlink from /usr/lib/expect (#71606)

* Wed Aug 14 2002 Jens Petersen <petersen@redhat.com> 8.3.3-73
- update to expect spawn patch from hjl@gnu.org (bug 43310)

* Tue Aug 13 2002 Jens Petersen <petersen@redhat.com> 8.3.3-72
- update expect to 5.38.0
- fixes #71113 (reported by yarnall@lvc.edu)

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- quick hack to have a correct setpgrp() call in expect
- fix config.guess and config.sub to newer versions

* Tue Aug 28 2001 Adrian Havill <havill@redhat.com>
- expect's fixline1 busted for expectk scripts (tkpasswd/tknewsbiff/tkterm)

* Wed Aug  8 2001 Adrian Havill <havill@redhat.com>
- re-enable glibc string and math inlines; recent gcc is a-ok.
- optimize at -O2 instead of -O
- rename "soname" patches related to makefile/autoconf changes

* Wed Jul 25 2001 Adrian Havill <havill@redhat.com>
- fixed 64 bit RPM provides for dependencies

* Thu Jul 19 2001 Adrian Havill <havill@redhat.com>
- used %%makeinstall to brute force fix any remaining unflexible makefile dirs
- improved randomness of expect's mkpasswd script via /dev/random (bug 9507)
- revert --enable-threads, linux is (still) not ready (yet) (bug 49251)

* Sun Jul  8 2001 Adrian Havill <havill@redhat.com>
- refresh all sources to latest stable (TODO: separate expect/expectk)
- massage out some build stuff to patches (TODO: libtoolize hacked constants)
- remove patches already rolled into the upstream
- removed RPATH (bugs 45569, 46085, 46086), added SONAMEs to ELFs
- changed shared object filenames to something less gross
- reenable threads which seem to work now
- fixed spawn/eof read problem with expect (bug 43310)
- made compile-friendly for IA64

* Fri Mar 23 2001 Bill Nottingham <notting@redhat.com>
- bzip2 sources

* Mon Mar 19 2001 Bill Nottingham <notting@redhat.com>
- build with -D_GNU_SOURCE - fixes expect on ia64

* Mon Mar 19 2001 Preston Brown <pbrown@redhat.com>
- build fix from ahavill.

* Wed Feb 21 2001 Tim Powers <timp@redhat.com>
- fixed weather expect script using wrong server (#28505)

* Tue Feb 13 2001 Adrian Havill <havill@redhat.com>
- rebuild so make check passes

* Fri Oct 20 2000 Than Ngo <than@redhat.com>
- rebuild with -O0 on alpha (bug #19461)

* Thu Aug 17 2000 Jeff Johnson <jbj@redhat.com>
- summaries from specspo.

* Thu Jul 27 2000 Jeff Johnson <jbj@redhat.com>
- rebuild against "working" util-linux col.

* Fri Jun 16 2000 Jeff Johnson <jbj@redhat.com>
- don't mess with %%{_libdir}, it's gonna be a FHS pita.

* Fri Jun  2 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging changes.
- revert --enable-threads, linux is not ready (yet) (#11789).
- expect: update to 5.31.7+ (#11595).

* Sat Mar 18 2000 Jeff Johnson <jbj@redhat.com>
- update to (tcl,tk}-8.2.3, expect-5.31, and itcl-3.1.0, URL's as well.
- use perl to drill out pre-pended RPM_BUILD_ROOT.
- configure with --enable-threads (experimental).
- autopasswd needs to handle password starting with hyphen (#9917).
- handle 553 ftp status in rftp expect script (#7869).
- remove cryptdir/decryptdir, as Linux has not crypt command (#6668).
- correct hierarchy spelling (#7082).
- fix "expect -d ...", format string had int printed as string (#7775).

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

* Thu Apr  8 1999 Jeff Johnson <jbj@redhat.com>
- use /usr/bin/write in kibitz (#1320).
- use cirrus.sprl.umich.edu in weather (#1926).

* Tue Feb 16 1999 Jeff Johnson <jbj@redhat.com>
- expect does unaligned access on alpha (#989)
- upgrade expect to 5.28.

* Tue Jan 12 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to allow building on the arm
- build for glibc 2.1
- strip binaries

* Thu Sep 10 1998 Jeff Johnson <jbj@redhat.com>
- update tcl/tk/tclX to 8.0.3, expect is updated also.

* Mon Jun 29 1998 Jeff Johnson <jbj@redhat.com>
- expect: mkpasswd needs delay before sending password (problem #576)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- fixed expect binaries exec permissions

* Wed Oct 22 1997 Otto Hammersmith <otto@redhat.com>
- fixed src urls

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- removed version numbers from descriptions

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- updated to tcl/tk 8.0 and related versions of packages

* Tue Jun 17 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- fixed dangling tclx/tkx symlinks
