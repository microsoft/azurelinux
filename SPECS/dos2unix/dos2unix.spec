Summary:       Text file format converters
Name:          dos2unix
Version:       7.5.1
Release:       1%{?dist}
License:       BSD
URL:           https://waterlan.home.xs4all.nl/dos2unix.html
Source:        https://waterlan.home.xs4all.nl/dos2unix/%{name}-%{version}.tar.gz
Vendor:        Microsoft Corporation
Distribution:  Mariner

BuildRequires: gcc
BuildRequires: gettext
Provides:      unix2dos = %{version}-%{release}
Obsoletes:     unix2dos < 5.1-1

%description
Convert text files with DOS or Mac line endings to Unix line endings and 
vice versa.

%prep
%setup -q

%build
make %{?_smp_mflags} LDFLAGS="%{build_ldflags}"

%install
make DESTDIR=$RPM_BUILD_ROOT install

# We add doc files manually to %%doc
rm -rf $RPM_BUILD_ROOT%{_docdir}

%find_lang %{name} --with-man --all-name

%files -f %{name}.lang
%license COPYING.txt 
%doc man/man1/dos2unix.htm ChangeLog.txt
%doc NEWS.txt README.txt TODO.txt
%{_bindir}/dos2unix
%{_bindir}/mac2unix
%{_bindir}/unix2dos
%{_bindir}/unix2mac
%{_mandir}/man1/*.1*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 7.5.1-1
- Auto-upgrade to 7.5.1 - Azure Linux 3.0 - package upgrades

* Fri Jan 21 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 7.4.2-1
- Upgrade to 7.4.2

* Tue Aug 25 2020 Nicolas Ontiveros <niontive@microsoft.com> - 7.4.1-4
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
- License verified.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 24 2019 Tim Waugh <twaugh@redhat.com> - 7.4.1-1
- Update to 7.4.1 (#1755150)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Than Ngo <than@redhat.com> - 7.4.0-7
- Enable tests

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Tim Waugh <twaugh@redhat.com> - 7.4.0-5
- Build requires gcc (bug #1603820).

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 08 2018 Tim Waugh <twaugh@redhat.com> - 7.4.0-3
- Fix build flags injection (bug #1573086).

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 11 2017 Tim Waugh <twaugh@redhat.com> 7.4.0-1
- 7.4.0.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul  5 2017 Tim Waugh <twaugh@redhat.com> 7.3.5-1
- 7.3.5.

* Mon Apr 10 2017 Erwin Waterlander <waterlan@xs4all.nl> 7.3.4-3
- Removed build requirement perl-Pod-Checker

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed May 25 2016 Tim Waugh <twaugh@redhat.com> 7.3.4-1
- 7.3.4.

* Mon Feb 15 2016 Tim Waugh <twaugh@redhat.com> 7.3.3-1
- 7.3.3 (bug #1308277).

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 30 2015 Tim Waugh <twaugh@redhat.com> 7.3.2-1
- 7.3.2 (bug #1284134).

* Thu Oct  1 2015 Tim Waugh <twaugh@redhat.com> 7.3.1-1
- 7.3.1 (bug #1267773).

* Mon Aug 24 2015 Tim Waugh <twaugh@redhat.com> 7.3-1
- 7.3.

* Thu Jul  2 2015 Tim Waugh <twaugh@redhat.com> 7.2.3-1
- 7.2.3 (bug #1238484).

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Tim Waugh <twaugh@redhat.com> 7.2.2-1
- 7.2.2 (bug #1224433).

* Thu Apr  2 2015 Tim Waugh <twaugh@redhat.com> 7.2.1-1
- 7.2.1.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 7.2-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Wed Feb 11 2015 Tim Waugh <twaugh@redhat.com> 7.2-1
- 7.2.

* Tue Oct  7 2014 Tim Waugh <twaugh@redhat.com> 7.1-1
- 7.1.

* Wed Sep 10 2014 Tim Waugh <twaugh@redhat.com> 7.0-1
- 7.0.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug  4 2014 Tim Waugh <twaugh@redhat.com> 6.0.6-1
- 6.0.6.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Tim Waugh <twaugh@redhat.com> 6.0.5-1
- 6.0.5 (bug #1089931).

* Thu Jan  2 2014 Tim Waugh <twaugh@redhat.com> 6.0.4-1
- 6.0.4.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Tim Waugh <twaugh@redhat.com> 6.0.3-2
- Build requires perl-Pod-Checker.
- Fixed bogus changelog dates.

* Mon Jan 28 2013 Tim Waugh <twaugh@redhat.com> 6.0.3-1
- 6.0.3.

* Fri Sep  7 2012 Tim Waugh <twaugh@redhat.com> 6.0.2-1
- 6.0.2.

* Thu Jul 26 2012 Tim Waugh <twaugh@redhat.com> 6.0.1-1
- 6.0.1.

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May  8 2012 Tim Waugh <twaugh@redhat.com> 6.0-1
- 6.0.

* Tue Mar 13 2012 Tim Waugh <twaugh@redhat.com> 5.3.3-1
- 5.3.3.

* Mon Jan 30 2012 Tim Waugh <twaugh@redhat.com> 5.3.2-1
- 5.3.2.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 10 2011 Tim Waugh <twaugh@redhat.com> 5.3.1-1
- 5.3.1.

* Fri May 20 2011 Tim Waugh <twaugh@redhat.com> 5.3-2
- No longer requires ghostscript or groff.
- Large file support taken care of upstream now.

* Wed Apr 27 2011 Tim Waugh <twaugh@redhat.com> 5.3-1
- 5.3.

* Mon Apr 11 2011 Tim Waugh <twaugh@redhat.com> 5.2.1-1
- 5.2.1.

* Tue Feb 15 2011 Tim Waugh <twaugh@redhat.com> 5.2-3
- Build requires perl (for pod2man).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Tim Waugh <twaugh@redhat.com> 5.2-1
- Update to 5.2.
- Build requires groff and ghostscript.

* Thu Aug 19 2010 Chen Lei <supercyper@163.com> 5.1.1-1
- Update to 5.1.1

* Wed Aug 18 2010 Tim Waugh <twaugh@redhat.com> 5.1-1
- Applied changes from Chen Lei (bug #592922):
  * Sun Aug 15 2010 Chen Lei <supercyper1@gmail.com> 5.1-1
  - 5.1.
  - Update spec to match latest guidelines w.r.t buildroot tag

* Tue Jan 26 2010 Tim Waugh <twaugh@redhat.com> 4.1.2-1
- 4.1.2.

* Fri Jan 22 2010 Tim Waugh <twaugh@redhat.com> 4.1.1-1
- 4.1.1.  New upstream.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep 24 2008 Tim Waugh <twaugh@redhat.com> 3.1-34
- Moved 'make clean' to prep section and added comment about there
  being no upstream (bug #225706).

* Mon Sep  8 2008 Tim Waugh <twaugh@redhat.com> 3.1-33
- Preserve file modes (bug #437465).
- Fixed manpage grammar (bug #460731).

* Mon Apr 14 2008 Tim Waugh <twaugh@redhat.com> 3.1-32
- Adjust license tag (bug #225706).
- Fix missing prototype (bug #225706).
- Install copy as symbolic links (bug #225706).

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 3.1-31
- Rebuild for GCC 4.3.

* Fri Jan 18 2008 Tim Waugh <twaugh@redhat.com> 3.1-30
- Applied patch from bug #292100 to fix segfault with missing -c argument.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 3.1-29
- Rebuild.

* Tue Feb  6 2007 Tim Waugh <twaugh@redhat.com> 3.1-28
- Fixed build root (bug #225706).
- Build with SMP flags (bug #225706).
- Use dist in release tag (bug #225706).
- Fixed macros in changelog (bug #225706).
- Preserve timestamps when using install (bug #225706).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.1-27.1
- rebuild

* Mon Jul 10 2006 Tim Waugh <twaugh@redhat.com> 3.1-27
- Re-encoded spec file in UTF-8 (bug #197817).

* Mon Jun  5 2006 Tim Waugh <twaugh@redhat.com> 3.1-26
- Rebuilt.

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 3.1-25
- Build with large file support.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.1-24.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.1-24.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Apr 13 2005 Tim Waugh <twaugh@redhat.com> 3.1-24
- Fixed tmppath patch (bug #150277).

* Thu Mar  3 2005 Mike A. Harris <mharris@redhat.com> 3.1-23
- Bump and rebuild for FC4, using gcc 4.

* Tue Feb  8 2005 Mike A. Harris <mharris@redhat.com> 3.1-22
- Bump and rebuild for FC4

* Wed Oct 20 2004 Miloslav Trmac <mitr@redhat.com> - 3.1-21
- Don't just delete the original file when destination and current directory
  are on different filesystems (#65548, #123069, patch by James Antill)
- Fix return type of StripDelimiter in dos2unix-3.1-safeconv.patch (#136148)

* Wed Oct  6 2004 Mike A. Harris <mharris@redhat.com> 3.1-20
- Added dos2unix-3.1-manpage-update-57507.patch to fix manpage (#57507)
- Added dos2unix-3.1-preserve-file-modes.patch to properly preserve file
  permissions (#91331,55183,112710,132145)

* Sun Sep 26 2004 Rik van Riel <riel@redhat.com> 3.1-19
- safer conversion w/ mac2unix (fix from bz #57508)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 05 2003 Elliot Lee <sopwith@redhat.com> 3.1-15
- Remove build dependency on perl, since perl BuildRequires: dos2unix,
  and there's no good reason not to just use sed here.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Oct  7 2002 Mike A. Harris <mharris@redhat.com> 3.1-13
- All-arch rebuild
- Added BuildRequires: perl

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 3.1-10
- Build in new environment

* Thu Jan 17 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix bug #57700 (segfault)
- Add the mac2unix symlink recommended in README
- Fix compiler warnings

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jan 10 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- shut up rpmlint

* Fri Nov 17 2000 Tim Powers <timp@redhat.com>
- use mkstemp instead of mktemp. Not much needed to change.

* Thu Nov 16 2000 Tim Powers <timp@redhat.com>
- cleaned up specfile a bit
- built for 7.1

* Wed Jul 07 1999 Peter Soos <sp@osb.hu> 
- Added Hungarian "Summary:" and "%%description" 
- Corrected the file and directory attributes to rebuild the package 
  under RedHat Linux 6.0
