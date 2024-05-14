Summary:        A C programming language indexing and/or cross-reference tool
Name:           ctags
Version:        6.1.0
Release:        1%{?dist}
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        GPLv2+
URL:            https://ctags.io/
Source0:        https://github.com/universal-ctags/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gcc
BuildRequires:  jansson-devel
BuildRequires:  libseccomp-devel
BuildRequires:  libxml2-devel
BuildRequires:  libyaml-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  python3-docutils

Obsoletes:      %{name}-etags <= 5.8

%description
Ctags generates an index (or tag) file of C language objects found in
C source and header files.  The index makes it easy for text editors or
other utilities to locate the indexed items.  Ctags can also generate a
cross reference file which lists information about the various objects
found in a set of C language files in human readable form.  Exuberant
Ctags improves on ctags because it can find all types of C language tags,
including macro definitions, enumerated values (values inside enum{...}),
function and method definitions, enum/struct/union tags, external
function prototypes, typedef names and variable declarations.  Exuberant
Ctags is far less likely to be fooled by code containing #if preprocessor
conditional constructs than ctags.  Exuberant ctags supports output of
Emacs style TAGS files and can be used to print out a list of selected
objects found in source files.

Install ctags if you are going to use your system for C programming.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
./autogen.sh
%configure

%make_build

%install
%make_install

%check
make check

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/optscript
%{_bindir}/readtags
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man7/*

%changelog
* Thu Feb 08 2024 Suresh Thelkar <sthelkar@microsoft.com> - 6.1.0-1
- Upgrade to version 6.1.0.

* Mon Jul 25 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.9.20220619.0-7
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.
- Added Group and changed version to majorversion.upstreamversion.

* Thu Jun 23 2022 Than Ngo <than@redhat.com> - 5.9-6.20220619.0
- update to 5.9.6.20220619.0

* Thu May 12 2022 Than Ngo <than@redhat.com> - 5.9-6.20220508.0
- update to 5.9.20220508.0

* Tue Apr 26 2022 Than Ngo <than@redhat.com> - 5.9-5.20220424.0
- 20220424.0

* Mon Mar 21 2022 Than Ngo <than@redhat.com> - 5.9-4.20220313.0
- update to 5.9-4.20220313.0

* Tue Feb 08 2022 Than Ngo <than@redhat.com> - 5.9-3.20220206.0
- update to p5.9.20220206.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-2.20210725.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Than Ngo <than@redhat.com> - 5.9-1.20210725.0
- update to p5.9-20210725

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-0.2.20210509.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 10 2021 Than Ngo <than@redhat.com> - 5.9-0.1.20210509.0
- update to 5.9.20210509.0

* Thu Mar 11 2021 Than Ngo <than@redhat.com> - 5.9-0.1.20210307.0
- switch to universal ctags

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 5.8-29
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Than Ngo <than@redhat.com> - 5.8-27
- Added gating tests

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Than Ngo <than@redhat.com> - 5.8-24
- fixed FTBFS

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Feb 05 2017 Than Ngo <than@redhat.com> - - 5.8-19
- fixed bz#1418434, added missing %%license

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Sep 30 2014 Than Ngo <than@redhat.com> - 5.8-16
- CVE-2014-7204, denial of service issue

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 14 2014 Jaromir Capik <jcapik@redhat.com> - 5.8-13
- Fixing format-security flaws (#1037028)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 13 2013 John Dennis <jdennis@redhat.com> - 5.8-11
- add ctags-5.8-memmove.patch
  bug #284 absoluteFilename uses strcpy on overlapping strings 
  https://sourceforge.net/p/ctags/bugs/284/  
  The bug was fixed upstream on 2012-03-26 in the following commit
  https://sourceforge.net/p/ctags/code/782/
  ctags-5.8-memmove.patch simply adds the same patch as the above commit.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov  5 2012 Marcela Mašláňová <mmaslano@redhat.com> - 5.8-9
- fix license field again

* Thu Oct 18 2012 Than Ngo <than@redhat.com> - 5.8-8
- fix the crash in cssparse

* Thu Aug 02 2012 Than Ngo <than@redhat.com> - 5.8-7
- backport from upstream to fix several crashes in ocaml

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 08 2012 Than Ngo <than@redhat.com> - 5.8-5
- bz#786451, add css support

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan  4 2010 Marcela Mašláňová <mmaslano@redhat.com> - 5.8-2
- fix license tag

* Tue Sep 01 2009 Than Ngo <than@redhat.com> - 5.8-1
- 5.8
- apply patch to fix segment fault, thanks to Masatake YAMATO

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 29 2008 Than Ngo <than@redhat.com>  5.7-3
- add subpackage ctags-etags

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 5.7-2
- fix license tag

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 5.7-1
- 5.7
- merge review: ctags

* Mon Jul 17 2006 Nalin Dahyabhai <nalin@redhat.com> 5.6-1.1
- rebuild

* Tue Jun 06 2006 Than Ngo <than@redhat.com> 5.6-1
- update to 5.6

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.5.4-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.5.4-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Jul 31 2005 Florian La Roche <laroche@redhat.com>
- remove etags

* Thu Mar 03 2005 Than Ngo <than@redhat.com> 5.5.4-3
- rebuilt

* Wed Feb 09 2005 Than Ngo <than@redhat.com> 5.5.4-2
- rebuilt

* Thu Jun 17 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 5.5.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Sep 27 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 5.5.2, no patch needed anymore

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  6 2003 Than Ngo <than@redhat.com> 5.5-1
- 5.5

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 13 2002 Karsten Hopp <karsten@redhat.de>
- update to 5.4

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Than Ngo <than@redhat.com> 5.2.3-3
- don't forcibly strip binaries

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 22 2002 Harald Hoyer <harald@redhat.de>
- 5.2.3

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 5.2.2-2
- rebuild in new enviroment

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 5.2.2-1
- 5.2.2

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jul 11 2001 Jakub Jelinek <jakub@redhat.com>
- rebuilt against binutils-2.11.90.0.8-3 to reserve .dynamic space

* Mon Jun 11 2001 Preston Brown <pbrown@redhat.com>
- 5.0.1

* Thu Jan 04 2001 Preston Brown <pbrown@redhat.com>
- 4.0.3
- remove etags, it is not fully compatible with cmd line of GNU etags.

* Sun Jul 16 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 4.0.2 from sourceforge

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jun 17 2000 Matt Wilson <msw@redhat.com>
- added defattr

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- FHS paths

* Mon May  8 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Update to 3.5.2
- minor cleanups to spec file

* Tue Feb 16 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Update to 3.4 to fix bug #9446

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- compress man page.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)
- version 3.2

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 2.0.3

* Mon Nov 03 1997 Michael K. Johnson <johnsonm@redhat.com>
- removed etags.  Emacs provides its own; and needs to support
  more than just C.

* Thu Oct 23 1997 Donnie Barnes <djb@redhat.com>
- updated from 1.5 to 1.6

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc
