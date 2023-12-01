Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Utility to create fonts.scale files for truetype fonts
Name: ttmkfdir
Version: 3.0.9
Release: 60%{?dist}
# Only licensing attribution ("GNU Library General Public License") is in README, no version.
License: LGPLv2+
# This is a Red Hat maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.
Source0: %{_mariner_sources_url}/%{name}-%{version}.tar.bz2
Source1: %{name}-LICENSE.txt
Patch: ttmkfdir-3.0.9-cpp.patch
Patch1: ttmkfdir-3.0.9-zlib.patch
Patch2: ttmkfdir-3.0.9-fix-freetype217.patch
Patch3: ttmkfdir-3.0.9-namespace.patch
Patch4: ttmkfdir-3.0.9-fix-crash.patch
Patch5: ttmkfdir-3.0.9-warnings.patch
Patch6: ttmkfdir-3.0.9-segfaults.patch
Patch7: ttmkfdir-3.0.9-encoding-dir.patch
Patch8: ttmkfdir-3.0.9-font-scale.patch
Patch9: ttmkfdir-3.0.9-bug434301.patch
Patch10:ttmkfdir-3.0.9-freetype-header-fix2.patch
Patch11:ttmkfdir-3.0.9-fedora-ldflags.patch
Source10: ttmkfdir.1

BuildRequires: freetype-devel >= 2.0
BuildRequires: flex libtool
BuildRequires: bzip2-devel
BuildRequires: zlib-devel
BuildRequires: gcc-c++

%description
ttmkfdir is a utility used to create fonts.scale files in
TrueType font directories in order to prepare them for use
by the font server.

%prep
%autosetup -p1
cp %{SOURCE1} ./LICENSE.txt

%build
make %{?_smp_mflags} OPTFLAGS="$RPM_OPT_FLAGS"

%install
make DESTDIR=$RPM_BUILD_ROOT PREFIX="%{_prefix}" install INSTALL="install -p"
mkdir -p %{buildroot}%{_mandir}/man1/
cp -p %{SOURCE10} %{buildroot}%{_mandir}/man1/

%files
%license LICENSE.txt
%doc README
%{_bindir}/ttmkfdir
%{_mandir}/man1/ttmkfdir.1*

%changelog
* Mon Apr 25 2022 Mateusz Malisz <mamalisz@microsoft.com> - 3.0.9-61
- Update Source0

* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.0.9-60
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.9-59
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

* Tue Jan 28 2020 Kalev Lember <klember@redhat.com> - 3.0.9-58
- Avoid hardcoding /usr prefix
- Use globs for man page compression

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-57
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-55
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.0.9-54
- Partial injection of build flags (rh#1548462)

* Mon Feb 19 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.0.9-53
- Add BuildRequires: gcc-c++ as per packaging guidelines
- Removed group tag
- Used %%autosetup

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-50
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-49
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 23 2016 Pravin Satpute <psatpute@redhat.com> - 3.0.9-48
- Removed ttmkfdir-3.0.9-freetype-header-fix.patch
- Resolves #1308197: ttmkfdir: FTBFS in rawhide

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-46
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.0.9-45
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug  2 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.0.9-43
- Add bzip2-devel as explicit build dep
- Drop ancient Obsoletes

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 26 2014 Parag Nemade <pnemade AT redhat DOT com> - 3.0.9-41
- Resolves:rh#1080516 - ttmkfdir ftbfs in rawhide due to freetype header move
- Thanks baude for your patch

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 28 2013 Pravin Satpute <psatpute@redhat.com> - 3.0.9-39
- added manpage (#928684)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Pravin Satpute <psatpute@redhat.com> - 3.0.9-37
- Spec cleanup (#878321)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-35
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Jens Petersen <petersen@redhat.com> - 3.0.9-31
- simplify ttmkfdir-3.0.9-encoding-dir.patch to drop X11R6/ check (#173705)

* Tue Mar 03 2009 Caolán McNamara <caolanm@redhat.com> - 3.0.9-30
- fix ttmkfdir-3.0.9-segfaults.patch to include stdio.h for added printf

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Pravin Satpute <psatpute@redhat.com> - 3.0.9-28
- modified spec file as per merge review suggestions bug 226506

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.0.9-27
- fix license tag

* Wed Feb 27 2008 Lingning Zhang <lizhang@redhat.com> - 3.0.9-26
- fix bug434301.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.9-25
- Autorebuild for GCC 4.3

* Thu Nov 30 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-24.fc7
- add ttmkfdir-3.0.9-font-scale.patch to fix bug #209102.
- Patch from Akira TAGOH.

* Wed Oct 18 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-23
- rebuild

* Fri Sep 29 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-22
- delete "%%post" and "Requires(post)" in ttmkfdir.spec

* Thu Sep 28 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-21
- modify release

* Wed Sep 27 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-20.4
- modify "%%post" and add "Requires(post)" in ttmkfdir.spec for fixing bug173591, bug207279, bug208122

* Wed Sep 06 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-20.3
- add "%%post" in ttmkfdir.spec for fixing bug173591

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.0.9-20.2.1
- rebuild

* Tue Jun 20 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-20.2
- add "BuildRequires: libtool" in ttmkfdir.spec

* Mon Jun 19 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-20.1
- remove the modifying part of ttmkfdir-3.0.9/Makefile, recover the old Makefile
- modify ttmkfdir-3.0.9-encoding-dir.patch about Makefile

* Thu Jun 15 2006 Lingning Zhang <lizhang@redhat.com> - 3.0.9-20
- add ttmkfdir-3.0.9-encoding-dir.patch to fix bug #173705
- modify ttmkfdir-3.0.9/Makefile to delete the compiling flag of "ggdb"

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.0.9-19.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0.9-19.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 8 2005 LingNing Zhang <lizhang@redhat.com> -3.0.9-19
- add ttmkfdir-3.0.9-segfaults.patch to fix bug #164969

* Wed Aug  3 2005 Jens Petersen <petersen@redhat.com> - 3.0.9-17
- replace ttmkfdir-3.0.9-defautl_enc_size.patch and
  ttmkfdir-3.0.9-crashplus.patch with ttmkfdir-3.0.9-fix-crash.patch
  to fix missing native encodings of fonts
  (Akira Tagoh, #143941)
- buildrequire flex
- add ttmkfdir-3.0.9-warnings.patch to silence most of compiler warnings

* Sun Mar 20 2005 Yu Shao <yshao@redhat.com> 3.0.9-16
- rebuild with GCC 4

* Fri Sep 10 2004 Yu Shao <yshao@redhat.com> 3.0.9-14
- bug #100560, requires zlib-devel rather than zlib

* Tue Aug 17 2004 Elliot Lee <sopwith@redhat.com> 3.0.9-13
- Follow-on fix for the issue detailed in #118713
- Improve performance when checking if a font has a mapping present
- Base font file selection on the magic at the start of the file, rather than the filename

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 19 2004 Yu Shao <yshao@redhat.com> 3.0.9-11
- set default encoding size to DEFAULT_SIZE, bug #118713

* Fri Mar 12 2004 Yu Shao <yshao@redhat.com> 3.0.9-10
- patch suggested from law@redhat.com not to use semicolon in GCC3.4, 3.5

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 12 2004 Yu Shao <yshao@redhat.com> 3.0.9-8
- patch for building package against freetype-2.1.7
- from kanagawa jigorou (jigorou3@mail.goo.ne.jp) #114682

* Mon Sep 15 2003 Yu Shao <yshao@redhat.com> 3.0.9-6
- updated zlib patch from Nalin Dahyabhai #104331

* Thu Aug 21 2003 Yu Shao <yshao@redhat.com> 3.0.9-4
- added zlib build requirement, partly releated to #100560
- other fixes

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com>
- Fix compile error (cpp.patch)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 23 2003 Yu Shao <yshao@redhat.com> 3.0.9-1
- added freetype-devel build requirement #82468

* Mon Jan 20 2003 Yu Shao <yshao@redhat.com> 3.0.8-1
- revert additional-entries to 0 #82125

* Wed Jan 15 2003 Yu Shao <yshao@redhat.com> 3.0.7-1
- set default value of additional-entries to 1

* Mon Jan 13 2003 Yu Shao <yshao@redhat.com> 3.0.6-1
- added iso8859-13 support from Nerijus Baliunas #77289
- added README

* Wed Jan 8 2003 Yu Shao <yshao@redhat.com> 3.0.5-1
- encoding.l fix and ttc support patch
- default read system encodings.dir instead of the one
- in current directory

* Wed Dec 18 2002 Yu Shao <yshao@redhat.com> 3.0.4-1
- make ttmkfdir keep silent with FIRSTINDEX. #61769

* Wed Dec 18 2002 Yu Shao <yshao@redhat.com> 3.0.3-1
- Applied new patches to make ttmkfdir provide more infomation when meets
- bad fonts

* Mon Dec  9 2002 Mike A. Harris <mharris@devel.capslock.lan> 3.0.2-1
- Changed the nonstandard RPM Group from System/Utilities to Applications/System
- Added a new Makefile install target, and changed specfile to use makeinstall

* Mon Dec  9 2002 Mike A. Harris <mharris@devel.capslock.lan> 3.0.1-1
- Imported ttmkfdir into CVS on cvs.devel and applied all patches to CVS
- Removed patches from spec file
- Rewrote Makefile, now uses freetype-config to autodetect CFLAGS and libs,
  allowing a lot of spec file cleanups.  Added new targets for tagging CVS,
  making tarball, and making srpm.

* Mon Dec  2 2002 Mike A. Harris <mharris@devel.capslock.lan> 3.0.0-2
- Added Conflicts for prior packages which contained ttmkfdir

* Fri Nov 29 2002 Mike A. Harris <mharris@devel.capslock.lan> 3.0.0-1
- Initial build.  Basically just renamed our existing ttmkfdir to version
  3.0.0 to differentiate it.  It's the same old thing as before, but is
  likely going to move to CVS for easier development.
