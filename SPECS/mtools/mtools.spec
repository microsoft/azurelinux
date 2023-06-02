Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Programs for accessing MS-DOS disks without mounting the disks
Name: mtools
Version: 4.0.43
Release: 2%{?dist}
License: GPLv3+
Source0: ftp://ftp.gnu.org/gnu/mtools/mtools-%{version}.tar.gz
Url: https://www.gnu.org/software/mtools/
Patch0: mtools-3.9.6-config.patch

BuildRequires: make
BuildRequires: gcc
BuildRequires: texinfo
BuildRequires: autoconf
BuildRequires: automake

%description
Mtools is a collection of utilities for accessing MS-DOS files.
Mtools allow you to read, write and move around MS-DOS filesystem
files (normally on MS-DOS floppy disks).  Mtools supports Windows95
style long file names, OS/2 XDF disks, and 2m disks

Mtools should be installed if you need to use MS-DOS disks

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .conf

%build
autoreconf -fiv
%configure --disable-floppyd
%make_build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc $RPM_BUILD_ROOT/%{_infodir}
%make_install
install -m644 mtools.conf $RPM_BUILD_ROOT/etc
gzip -9f $RPM_BUILD_ROOT/%{_infodir}/*

# We aren't shipping this.
find $RPM_BUILD_ROOT -name "floppyd*" -exec rm {} \;

# dir.gz is handled in %%post and %%preun sections
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir.gz

ln -s mtools.5.gz %{buildroot}%{_mandir}/man5/mtools.conf.5.gz

%files
%config(noreplace) /etc/mtools.conf
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README Release.notes
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/mtools.info*

%changelog
* Fri Jun 02 2023 Vince Perri <viperri@microsoft.com> 4.0.43-2
- License verified.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).

* Wed Mar 22 2023 Vojtech Trefny <vtrefny@redhat.com> 4.0.43-1
- Update to 4.0.43

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 11 2022 Vojtech Trefny <vtrefny@redhat.com> - 4.0.42-2
- Change license string to the SPDX format required by Fedora

* Mon Oct 24 2022 Vojtech Trefny <vtrefny@redhat.com> 4.0.42-1
- Update to 4.0.42

* Tue Sep 20 2022 Vojtech Trefny <vtrefny@redhat.com> 4.0.41-1
- Update to 4.0.41

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 06 2022 Vojtech Trefny <vtrefny@redhat.com> 4.0.40-1
- Update to 4.0.40

* Tue Apr 12 2022 Vojtech Trefny <vtrefny@redhat.com> 4.0.39-1
- Update to 4.0.39

* Mon Mar 07 2022 Vojtech Trefny <vtrefny@redhat.com> 4.0.38-1
- Update to 4.0.38

* Tue Feb 15 2022 Vojtech Trefny <vtrefny@redhat.com> 4.0.37-3
- Rebuilt for glibc flatpak dependency update

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Vojtech Trefny <vtrefny@redhat.com> 4.0.37-1
- Update to 4.0.37

* Mon Nov 22 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.36-1
- Update to 4.0.36

* Wed Nov 10 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.35-2
- Add dependency on glibc-gconv-extra (#2021637)

* Sun Aug 08 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.35-1
- Update to 4.0.35

* Sun Jul 25 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.34-1
- Update to 4.0.34

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.33-1
- Update to 4.0.33

* Wed Jul 14 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.32-1
- Update to 4.0.32

* Mon Jun 28 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.31-1
- Update to 4.0.31

* Fri Jun 18 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.30-1
- Update to 4.0.30

* Tue Jun 01 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.29-1
- Update to 4.0.29

* Mon Apr 19 2021 Vojtech Trefny <vtrefny@redhat.com> 4.0.27-1
- Update to 4.0.27

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Vojtech Trefny <vtrefny@redhat.com> 4.0.26-1
- Update to 4.0.26

* Thu Oct 29 2020 Vojtech Trefny <vtrefny@redhat.com> 4.0.25-1
- Update to 4.0.25

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 4.0.24-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Sun Mar 22 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 4.0.24-1
- Update to 4.0.24 (#1815863)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Vojtech Trefny <vtrefny@redhat.com> 4.0.23-1
- Update to 4.0.23

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 4.0.18-8
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 4.0.18-6
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Adam Tkac <atkac redhat com> - 4.0.18-3
- use bz2 compressed source instead of lz

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Adam Tkac <atkac redhat com> - 4.0.18-1
- update to 4.0.18

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Adam Tkac <atkac redhat com> 4.0.17-1
- update to 4.0.17

* Tue Apr 19 2011 Adam Tkac <atkac redhat com> 4.0.16-1
- update to 4.0.16

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Adam Tkac <atkac redhat com> 4.0.15-1
- update to 4.0.15

* Thu Mar 11 2010 Jan Görig <jgorig redhat com> 4.0.13-2
- added symlink to config manpage

* Mon Mar 01 2010 Adam Tkac <atkac redhat com> 4.0.13-1
- update to 4.0.13

* Tue Feb 23 2010 Adam Tkac <atkac redhat com> 4.0.12-2
- change license to GPLv3+

* Tue Nov 10 2009 Adam Tkac <atkac redhat com> 4.0.12-1
- update to 4.0.12

* Tue Sep 01 2009 Adam Tkac <atkac redhat com> 4.0.11-1
- update to 4.0.11

* Tue Aug 11 2009 Adam Tkac <atkac redhat com> 4.0.10-4
- fix installation with --excludedocs (#515932)

* Tue Aug 11 2009 Adam Tkac <atkac redhat com> 4.0.10-3
- correct source URL

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 04 2009 Adam Tkac <atkac redhat com> 4.0.10-1
- update to 4.0.10

* Mon Mar 09 2009 Adam Tkac <atkac redhat com> 4.0.9-1
- updated to 4.0.9
- merged mtools-3.9.7-bigdisk.patch to config patch
- mtools400-rh480112.patch merged to upstream

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Adam Tkac <atkac redhat com> 4.0.0-3
- fixed off-by-two error in unix_name function (#480112)

* Mon Jan 12 2009 Adam Tkac <atkac redhat com> 4.0.0-2
- don't ship infodir/dir.gz (#478322)

* Mon Dec 01 2008 Adam Tkac <atkac redhat com> 4.0.0-1
- updated to 4.0.0

* Wed Nov 19 2008 Adam Tkac <atkac redhat com> 4.0.0-0.1.pre2
- updated to 4.0.0_pre2

* Tue Nov 11 2008 Adam Tkac <atkac redhat com> 4.0.0-0.1.pre1
- updated to 4.0.0_pre1

* Fri Oct 03 2008 Adam Tkac <atkac redhat com> 3.9.11-5
- mtools-3.9.9-noargs.patch and mtools-3.9.6-paths.patch are not needed
- rebuild (#465040)

* Tue Feb 19 2008 Adam Tkac <atkac redhat com> 3.9.11-4
- fixed building on x86_64 (build with --disable-floppyd)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.9.11-3.1
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Adam Tkac <atkac redhat com> 3.9.11-2.1
- corrected post and preun sections (#428478)
- fix rpmlint errors
- start use autoreconf

* Wed Aug 22 2007 Adam Tkac <atkac redhat com> 3.9.11-2
- rebuild (BuildID feature)
- change license to GPLv2+

* Wed May 31 2007 Adam Tkac <atkac redhat com> 3.9.11-1
- updated to latest upstream (3.9.11)

* Fri May 11 2007 Adam Tkac <atkac redhat com> 3.9.10-7
- in the end script has been completely rewriten by <skasal@redhat.com>

* Fri May 11 2007 Adam Tkac <atkac redhat com> 3.9.10-6
- some minor changes in sh patch (changed sh to bash)

* Fri May 11 2007 Adam Tkac <atkac redhat com> 3.9.10-5
- patch to #239741 by Matej Cepl <mcepl@redhat.com>
  (rewrites /usr/bin/amuFormat.sh to /bin/sh)

* Tue Feb 05 2007 Adam Tkac <atkac redhat com> 3.9.10-4
- fixed some unstandard statements in spec file (#226162)

* Mon Jan 22 2007 Adam Tkac <atkac redhat com> 3.9.10-3
- Resolves: #223712
- applied Ville Skytta's (ville.skytta "antispam" iki.fi) patch
  (install-info scriptlet failures)

* Wed Aug 09 2006 Jitka Kudrnacova <jkudrnac@redhat.com> - 3.9.10-2
- rebuilt to prevent corruption on the 13th character (#195528)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.9.10-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.9.10-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.9.10-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Oct 19 2005 Tim Waugh <twaugh@redhat.com> 3.9.10-1
- 3.9.10.

* Mon Mar 21 2005 Tim Waugh <twaugh@redhat.com> 3.9.9-13
- Fixed memset() usage bug.

* Tue Mar 15 2005 Tim Waugh <twaugh@redhat.com> 3.9.9-12
- Fix build (bug #151135).

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 3.9.9-11
- Rebuild for new GCC.

* Fri Dec 10 2004 Tim Waugh <twaugh@redhat.com> 3.9.9-10
- Fixed mpartition --help output (bug #65293).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan  8 2004 Tim Waugh <twaugh@redhat.com> 3.9.9-7
- Fix mistaken use of '&' instead of '&&'.

* Tue Dec  9 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-6
- Remove last (incorrect) change.

* Tue Dec  9 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-5
- Fix mistaken variable assignment in comparison (bug #110823).

* Thu Nov 27 2003 Tim Waugh <twaugh@redhat.com>
- Build requires texinfo (bug #111000).

* Sat Oct 25 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-4
- Rebuilt.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-2
- Fix mcomp with no arguments (bug #91372).

* Tue Mar 18 2003 Tim Waugh <twaugh@redhat.com> 3.9.9-1
- 3.9.9.
- Add config lines for hpoj photo-card access on drive P:.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuilt in current collinst

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.8-2
- Add patch from maintainer

* Mon May 28 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.8-1
- 3.9.8 final

* Mon May 21 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.8-0.pre1.0
- 3.9.8pre1

* Wed May 16 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.7-6
- Fix support for disks > 1.44 MB (#40857)

* Tue May  8 2001 Bernhard Rosenkraenzer <bero@redhat.com> 3.9.7-5
- Update to 20010507

* Wed Jan 10 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Apply the author's current patches, fixes among other things
  ZIP drive support and doesn't crash when trying to access a BSD disk

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Trond Eivind Glomsrod <teg@redhat.com>
- specify ownership

* Wed Jun 07 2000 Trond Eivind Glomsrod <teg@redhat.com>
- Version 3.9.7
- use %%{_mandir}, %%{_makeinstall}, %%configure, %%makeinstall
  and %%{_tmppath}

* Wed Feb 09 2000 Cristian Gafton <gafton@redhat.com>
- get rid of mtools.texi as a doc file (we have the info file)
- fix config file so mtools work (#9264)
- fix references to the config file to be /etc/mtools.conf

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- expunge floppyd

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- man pages are compressed
- fix description
- version 3.9.6

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 5)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- patch to make the texi sources compile
- fix the spec file group and description
- fixed floppy drive sizes

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
- fixed invalid SAMPLE_FILE configuration file

* Wed Sep 02 1998 Michael Maher <mike@redhat.com>
- Built package for 5.2.
- Updated Source to 3.9.1.
- Cleaned up spec file.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Apr 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 3.8

* Tue Oct 21 1997 Otto Hammersmith
- changed buildroot to /var/tmp, rather than /tmp
- use install-info

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Thu Apr 17 1997 Erik Troan <ewt@redhat.com>
- Changed sysconfdir to be /etc

* Mon Apr 14 1997 Michael Fulbright <msf@redhat.com>
- Updated to 3.6
