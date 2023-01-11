Summary:        Revision Control System (RCS) file version management tools
Name:           rcs
Version:        5.10.1
Release:        4%{?dist}
License:        GPL-3.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gnu.org/software/rcs/
Source:         http://ftp.gnu.org/gnu/rcs/%{name}-%{version}.tar.lz
BuildRequires:  autoconf
# BuildRequires: ghostscript
BuildRequires:  ed
BuildRequires:  gcc
BuildRequires:  groff
BuildRequires:  lzip
BuildRequires:  make
BuildRequires:  texinfo
Requires:       diffutils
# for bundled(gnulib) see https://fedorahosted.org/fpc/ticket/174
Provides:       bundled(gnulib)

%description
The Revision Control System (RCS) is a system for managing multiple
versions of files.  RCS automates the storage, retrieval, logging,
identification and merging of file revisions.  RCS is useful for text
files that are revised frequently (for example, programs,
documentation, graphics, papers and form letters).

The rcs package should be installed if you need a system for managing
different versions of files.

%prep
%setup -q

autoconf

%build
%configure --with-diffutils
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

install -m 755 src/rcsfreeze %{buildroot}%{_bindir}

rm -f %{buildroot}/%{_infodir}/dir

%check
make check XFAIL_TESTS="`tests/known-failures %{version}`"

%files
%license COPYING
%doc ChangeLog THANKS NEWS README
%{_bindir}/*
%{_mandir}/man[15]/*
%{_infodir}/*

%changelog
* Wed Jan 11 2023 Suresh Thelkar <sthelkar@microsoft.com> - 5.10.1-4
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Mon Nov 07 2022 Christoph Karl <pampelmuse [AT] gmx [DOT] at> - 5.10.1-3
- SPDX

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Feb 04 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.1-1
- Update to upstream 5.10.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Apr 04 2021 Christoph Karl <pampelmuse [AT] gmx [DOT] at> - 5.10.0-3
- patch SIGSTKSZ

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Nov 14 2020 Christoph Karl <pampelmuse [AT] gmx [DOT] at> - 5.10.0-1
- Update to upstream 5.10.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 27 2018 Matej Mužila <mmuzial@redhat.com> - 5.9.4-9
- Disable t810 test

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jul 05 2015 Ralf Corsépius <corsepiu@fedoraproject.org> - 5.9.4-3
- Append -stc=c99 to CFLAGS (Fix FTBFS).

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 24 2015 Matej Muzila <mmuzila@redhat.com> - 5.9.4-1
- Update to upstream 5.9.4

* Tue Sep 30 2014 Matej Muzila <mmuzila@redhat.com> - 5.9.3-1
- Update to upstream 5.9.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec  3 2013 Honza Horak <hhorak@redhat.com> - 5.9.2-2
- Explicitly require texinfo during build

* Fri Nov 29 2013 Honza Horak <hhorak@redhat.com> - 5.9.2-1
- Update to upstream 5.9.2

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 10 2013 Honza Horak <hhorak@redhat.com> - 5.9.0-1
- Update to upstream 5.9.0

* Thu Apr  4 2013 Honza Horak <hhorak@redhat.com> - 5.8.2-1
- Update to upstream 5.8.2
- Fix some man page vs. help incompatibilities

* Thu Jan 24 2013 Honza Horak <hhorak@redhat.com> - 5.8.1-5
- Remove sendmail from build requirements, it's not configured to be used
  Related: #903368

* Fri Nov 23 2012 Honza Horak <hhorak@redhat.com> - 5.8.1-4
- Use make DESTDIR=... install instead of %%make_install

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Honza Horak <hhorak@redhat.com> - 5.8.1-2
- Provides: bundled(gnulib) added, as per #821786
- minor spec file clean up
- install-info run in postin/postun

* Wed Jun 06 2012 Honza Horak <hhorak@redhat.com> - 5.8.1-1
- Update to upstream 5.8.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 08 2011 Honza Horak <hhorak@redhat.com> - 5.8-1
- Update to upstream 5.8
- Dropped patches -security, -DESTDIR and -option that are not needed 
  anymore
- Run tests in %%check

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 11 2010 Ville Skyttä <ville.skytta at iki.fi> - 5.7-36
- Add dependency on diffutils.
- Apply build tweaks patch from Debian (incl installing rcsfreeze).
- BuildRequire autoconf instead of automake.
- Actually configure instead of shipping a pregenerated conf.h (#226356).
- Ship docs as PDF rather than troff source.
- Run test suite during build.
- Include COPYING.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.7-33
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 5.7-32
- Autorebuild for GCC 4.3

* Tue Jul 17 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 5.7-31
- Addded support for new svn syntax.
- Resolves: #247998

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.7-30.1
- rebuild

* Mon Jun 12 2006 Jesse Keating <jkeating@redhat.com> - 5.7-30
- Add missing BR automake

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.7-29.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.7-29.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 10 2005 Phil Knirsch <pknirsch@redhat.com> 5.7-29
- Fixed bug with obsolete and changed -u option for diff (#165071)

* Wed Mar 02 2005 Phil Knirsch <pknirsch@redhat.com> 5.7-28
- bump release and rebuild with gcc 4

* Sun Feb 13 2005 Florian La Roche <laroche@redhat.com> 5.7-27
- add spec change from #144485

* Tue Sep 21 2004 Phil Knirsch <pknirsch@redhat.com> 5.7-26
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com> 5.7-25
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 5.7-24
- rebuilt

* Wed Feb 04 2004 Phil Knirsch <pknirsch@redhat.com> 5.7-23
- Switched copyright to license. :-)

* Fri Oct 31 2003 Phil Knirsch <pknirsch@redhat.com> 5.7-22
- Included sameuserlocks patch from James Olin Oden (#107947).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 5.7-19
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Fri Jan 05 2001 Preston Brown <pbrown@redhat.com>
- tmpfile security patch from Olaf Kirch <okir@lst.de>

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Mon Feb  7 2000 Jeff Johnson <jbj@redhat.com>
- compress man pages.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 10)

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Cristian Gafton <gafton@redhat.com>
- fixed the spec file; added BuildRoot

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
-built against glibc
