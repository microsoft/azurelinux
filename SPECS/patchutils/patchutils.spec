Summary: A collection of programs for manipulating patch files
Name: patchutils
Version: 0.4.2
Release: 4%{?dist}
License: GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL: http://cyberelk.net/tim/patchutils/
Source0: http://cyberelk.net/tim/data/patchutils/stable/%{name}-%{version}.tar.xz
Obsoletes: interdiff <= 0.0.10
Provides: interdiff = 0.0.11
Requires: patch
BuildRequires:  gcc
BuildRequires: perl-generators
BuildRequires: xmlto
BuildRequires: automake, autoconf

%description
This is a collection of programs that can manipulate patch files in
a variety of ways, such as interpolating between two pre-patches, 
combining two incremental patches, fixing line numbers in hand-edited 
patches, and simply listing the files modified by a patch.

%prep
%setup -q

%build
%configure
%make_build

%check
make check

%install
make DESTDIR=%{buildroot} install

%files
%{!?_licensedir:%global license %doc}
%doc AUTHORS ChangeLog README BUGS NEWS
%license COPYING
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.4.2-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue May 02 2023 Cameron Baird <cameronbaird@microsoft.com> - 0.4.2-3
- Moved to SPECS
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.2-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jul 17 2020 Tim Waugh <twaugh@redhat.com> - 0.4.2-1
- 0.4.2.

* Thu Jul 16 2020 Tim Waugh <twaugh@redhat.com> - 0.4.0-1
- 0.4.0.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Tim Waugh <twaugh@redhat.com> - 0.3.4-12
- Requires patch (bug #1609946).

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Tim Waugh <twaugh@redhat.com> - 0.3.4-7
- Don't use regerror() result as format string.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 21 2015 Tim Waugh <twaugh@redhat.com> - 0.3.4-4
- Spec file cleanups (bug #1251587).

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  9 2015 Tim Waugh <twaugh@redhat.com> - 0.3.4-2
- Fixed handling of delete-file diffs from git (bug #1226985).

* Mon Apr 20 2015 Tim Waugh <twaugh@redhat.com> - 0.3.4-1
- 0.3.4.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.3.3-3
- Perl 5.18 rebuild

* Thu Apr 11 2013 Tim Waugh <twaugh@redhat.com> 0.3.3-2
- Fixed help output (bug #948973).
- Fixed changelog dates.

* Tue Apr  2 2013 Tim Waugh <twaugh@redhat.com> 0.3.3-1
- 0.3.3.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Feb 10 2011 Tim Waugh <twaugh@redhat.com> 0.3.2-1
- 0.3.2.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Tim Waugh <twaugh@redhat.com> 0.3.1-1
- 0.3.1.

* Wed Jul  2 2008 Tim Waugh <twaugh@redhat.com> 0.3.0-1
- 0.3.0.

* Wed Feb 13 2008 Tim Waugh <twaugh@redhat.com> 0.2.31-5
- Rebuild for GCC 4.3.

* Mon Dec  3 2007 Tim Waugh <twaugh@redhat.com> 0.2.31-4
- Versioned obsoletes/provides (bug #226234).
- Created %%check section (bug #226234).
- Avoid %%makeinstall (bug #226234).
- Fixed defattr declaration (bug #226234).

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 0.2.31-3
- Added dist tag.
- Better buildroot tag.
- More specific license tag.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.2.31-2.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.2.31-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.2.31-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Jul 22 2005 Tim Waugh <twaugh@redhat.com>
- Better structure in XML documentation.

* Tue Jul 19 2005 Tim Waugh <twaugh@redhat.com> 0.2.31-2
- Rebuilt to pick up new man-pages stylesheet.

* Mon Jun 13 2005 Tim Waugh <twaugh@redhat.com> 0.2.31-1
- 0.2.31.

* Wed Mar  2 2005 Tim Waugh <twaugh@redhat.com> 0.2.30-4
- Rebuild for new GCC.

* Mon Nov 22 2004 Tim Waugh <twaugh@redhat.com> 0.2.30-3
- Moved last fix into docbook-style-xsl.

* Mon Nov 22 2004 Jindrich Novy <jnovy@redhat.com> 0.2.30-2
- fix flipdiff.1 man page (#139341)

* Thu Jul 22 2004 Tim Waugh <twaugh@redhat.com> 0.2.30-1
- 0.2.30.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Tim Waugh <twaugh@redhat.com> 0.2.29-2
- Fix no-newline handling in filterdiff.

* Mon Apr  5 2004 Tim Waugh <twaugh@redhat.com> 0.2.29-1
- 0.2.29.

* Wed Mar 10 2004 Tim Waugh <twaugh@redhat.com> 0.2.28-1
- 0.2.28.

* Thu Feb 26 2004 Tim Waugh <twaugh@redhat.com> 0.2.27-1
- 0.2.27.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 12 2004 Tim Waugh <twaugh@redhat.com> 0.2.26-1
- 0.2.26.

* Tue Jan  6 2004 Tim Waugh <twaugh@redhat.com>
- Ship AUTHORS and ChangeLog as well (bug #112936).

* Mon Dec 15 2003 Tim Waugh <twaugh@redhat.com> 0.2.25-1
- 0.2.25.

* Wed Sep  3 2003 Tim Waugh <twaugh@redhat.com>
- Remove buildroot before installing.

* Thu Jul 31 2003 Tim Waugh <twaugh@redhat.com> 0.2.24-2
- Add support for -H in lsdiff/grepdiff (from CVS).

* Fri Jul 25 2003 Tim Waugh <twaugh@redhat.com> 0.2.24-1
- 0.2.24 (fixes bug #100795).

* Thu Jun 5 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun  5 2003 Tim Waugh <twaugh@redhat.com> 0.2.23-2
- Added patch from CVS which adds timestamp removal to filterdiff.

* Thu Jun  5 2003 Tim Waugh <twaugh@redhat.com> 0.2.23-1.1
- Rebuilt.

* Thu Jun  5 2003 Tim Waugh <twaugh@redhat.com> 0.2.23-1
- 0.2.23.  Fixes bug #92320.

* Sat Mar  8 2003 Tim Waugh <twaugh@redhat.com> 0.2.22-1
- 0.2.22.

* Thu Jan 23 2003 Tim Waugh <twaugh@redhat.com> 0.2.19-1
- 0.2.19, incorporating all patches.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.2.18-3
- rebuilt

* Wed Jan 22 2003 Tim Waugh <twaugh@redhat.com>
- Apply editdiff patch from 0.2.19pre2.

* Wed Jan 22 2003 Tim Waugh <twaugh@redhat.com> 0.2.18-2
- Bug-fix for rediff.

* Mon Dec 16 2002 Tim Waugh <twaugh@redhat.com> 0.2.18-1
- Fix file_exists().
- 0.2.18.

* Wed Oct 16 2002 Tim Waugh <twaugh@redhat.com> 0.2.17-1
- 0.2.17.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat May 18 2002 Tim Waugh <twaugh@redhat.com> 0.2.14-1
- 0.2.14.

* Thu May  9 2002 Tim Waugh <twaugh@redhat.com> 0.2.13-1
- 0.2.13.

* Tue Apr 23 2002 Tim Waugh <twaugh@redhat.com> 0.2.13-0.pre1.1
- 0.2.13pre1 (now handles diffutils 2.8.1 output).
- Run tests after build step.

* Fri Apr 19 2002 Tim Waugh <twaugh@redhat.com> 0.2.12-1
- 0.2.12.

* Wed Mar 20 2002 Tim Waugh <twaugh@redhat.com> 0.2.11-2
- Fix handling of context diffs so that it handles GNU diff's output
  style.

* Thu Mar 14 2002 Tim Waugh <twaugh@redhat.com> 0.2.11-1
- 0.2.11.

* Mon Mar 04 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- I need this. :-)

* Tue Nov 27 2001 Tim Waugh <twaugh@redhat.com>
- Initial spec file.
