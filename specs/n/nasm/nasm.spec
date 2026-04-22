# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?rhel} > 0
# On RHEL we default to building WITHOUT documentation.
%bcond_with documentation
%else
# Default to building WITH documentation.
%bcond_without documentation
%endif

Summary: A portable x86 assembler which uses Intel-like syntax
Name: nasm
Version: 2.16.03
Release: 5%{?dist}
License: BSD-2-Clause
URL: http://www.nasm.us
Source0: https://www.nasm.us/pub/nasm/releasebuilds/%{version}/%{name}-%{version}.tar.xz
Source1: https://www.nasm.us/pub/nasm/releasebuilds/%{version}/%{name}-%{version}-xdoc.tar.xz

BuildRequires: perl(Env)
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: gcc
BuildRequires: make
Obsoletes: nasm-rdoff < 2.16.01-1

%if %{with documentation}
%package doc
Summary: Documentation for NASM
BuildRequires: perl(Font::TTF::Font)
BuildRequires: perl(Sort::Versions)
BuildRequires: perl(File::Spec)
BuildRequires: perl(sort)
BuildRequires: adobe-source-sans-pro-fonts
BuildRequires: adobe-source-code-pro-fonts
BuildRequires: ghostscript
BuildArch: noarch
# For arch to noarch conversion
Obsoletes: %{name}-doc < %{version}-%{release}
%endif

%description
NASM is the Netwide Assembler, a free portable assembler for the Intel
80x86 microprocessor series, using primarily the traditional Intel
instruction mnemonics and syntax.

%if %{with documentation}
%description doc
This package contains documentation for the Netwide Assembler (NASM),
in HTML, PDF, PostScript, and text formats.
%endif

%prep
%autosetup -p1

tar xJf %{SOURCE1} --strip-components 1

%build
%configure
%if %{with documentation}
make everything %{?_smp_mflags}
gzip -9f doc/nasmdoc.{ps,txt}
%else
make all %{?_smp_mflags}
%endif

%install
%make_install

%check
make -C test golden test diff

%files
%license LICENSE
%doc AUTHORS CHANGES README.md
%{_bindir}/nasm
%{_bindir}/ndisasm
%{_mandir}/man1/nasm*
%{_mandir}/man1/ndisasm*

%if %{with documentation}
%files doc
%doc doc/html doc/nasmdoc.txt.gz doc/nasmdoc.ps.gz doc/nasmdoc.pdf
%endif

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 22 2024 Dominik Mierzejewski <rpm@greysector.net> - 2.16.03-1
- update to 2.16.03 (resolves rhbz#2273692)

* Sat Apr 06 2024 Dominik Mierzejewski <rpm@greysector.net> - 2.16.02-1
- update 2.16.02 (#2273692)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.01-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Nick Clifton  <nickc@redhat.com> - 2.16.01-4
- Spec File: Migrated to SPDX license.  (#2222114)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Dominik Mierzejewski <rpm@greysector.net> - 2.16.01-2
- add Obsoletes for the dropped subpackage

* Wed Jan 04 2023 Dominik Mierzejewski <rpm@greysector.net> - 2.16.01-1
- update to 2.16.01 (#2155636)
- drop obsolete patch
- drop rdoff subpackage (discontinued upstream)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 03 2021 Dominik Mierzejewski <rpm@greysector.net> - 2.15.05-1
- update to 2.15.05 (#1851651)
- run internal tests in check section

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.03-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.03-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 18 2020 Merlin Mathesius <mmathesi@redhat.com> - 2.15.03-3
- Patch to workaround renamed SourceSans font family

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.15.03-1
- Update to 2.15.03

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.14.02-1
- Update to 2.14.02

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.03-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.03-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Michael Simacek <msimacek@redhat.com> - 2.13.03-1
- Update to upstream version 2.13.03

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Michael Simacek <msimacek@redhat.com> - 2.13.02-2
- Add missing BR ghostscript

* Tue Jan 02 2018 Michael Simacek <msimacek@redhat.com> - 2.13.02-1
- Update to upstream version 2.13.02
- Resolves: CVE-2017-17810, CVE-2017-17811, CVE-2017-17812, CVE-2017-17813,
  CVE-2017-17814, CVE-2017-17815, CVE-2017-17816, CVE-2017-17817,
  CVE-2017-17818, CVE-2017-17819, CVE-2017-17820

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.13.01-3
- Fix use-after-free and heap buffer overflow vulnerabilities
- Resolves: CVE-2017-10686, CVE-2017-11111

* Tue Jul 04 2017 Nils Philippsen <nils@redhat.com> - 2.13.01-2
- don't build documentation during modular build
- fix bogus changelog date

* Mon May 22 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.13.01-1
- Update to upstream version 2.13.01

* Tue May  2 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.13-1
- Update to upstream version 2.13

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Roman Vais <rvais@redhat.com> - 2.12.02-1
- Update to upstream version 2.12.02

* Tue Mar 22 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12.01-1
- Update to upstream version 2.12.01

* Thu Mar  3 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12-2
- Fix build failure on ppc64

* Mon Feb 29 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.12-1
- Update to upstream version 2.12

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.08-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Feb 23 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.08-1
- Update to upstream version 2.11.08

* Tue Oct 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.06-1
- Update to upstream version 2.11.06

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.05-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.05-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.05-1
- Update to upstream version 2.11.05

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.04-1
- Update to upstream version 2.11.04

* Mon May 12 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.03-1
- Update to upstream version 2.11.03

* Fri Mar  7 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11.02-1
- Update to upstream version 2.11.02

* Thu Jan  2 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.11-1
- Update to upstream version 2.11

* Thu Sep 12 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.09-1
- Update to upstream version 2.10.09

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10.07-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  1 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.07-5
- Backport upsteam manpage fixes

* Mon Apr  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.07-4
- Add missing BR: perl(Env)
- Move rdf manpages to rdf subpackage

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.07-3
- Properly obsolete arch-specific doc subpackage

* Thu Mar  7 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.07-2
- Update to current packaging guidelines
- Resolves: rhbz#919008 (doc subpackage should be noarch)

* Wed Jan 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.07-1
- Update to upstream version 2.10.07

* Mon Aug  6 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.10.03-1
- Update to upstream version 2.10.03

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 15 2012 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 2.10-1
- update to 2.10 (#797858)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09.08-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Apr 26 2011 Vojtech Vitek (V-Teq) <vvitek@redhat.com> - 2.09.08-1
- update to 2.09.08
  Resolves: #685125 

* Mon Mar 14 2011 Adam Tkac <atkac redhat com> - 2.09.07-1
- update to 2.09.07

* Mon Feb 21 2011 Adam Tkac <atkac redhat com> - 2.09.05-1
- update to 2.09.05

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 23 2010 Adam Tkac <atkac redhat com> - 2.09.04-1
- update to 2.09.04

* Thu Nov 11 2010 Adam Tkac <atkac redhat com> - 2.09.03-2
- fix URL (#652012)

* Tue Nov 02 2010 Adam Tkac <atkac redhat com> - 2.09.03-1
- update to 2.09.03

* Wed Sep 29 2010 jkeating - 2.09.02-2
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Adam Tkac <atkac redhat com> - 2.09.02-1
- update to 2.09.02

* Mon Sep 13 2010 Adam Tkac <atkac redhat com> - 2.09.01-1
- update to 2.09.01

* Thu Sep 02 2010 Adam Tkac <atkac redhat com> - 2.09-1
- update to 2.09

* Fri Aug 13 2010 Adam Tkac <atkac redhat com> - 2.08.02-1
- update to 2.08.02

* Wed Jul 14 2010 Todd Zullinger <tmz@gaggle.net> - 2.08.01-2
- Fix license tag, nasm is under 2 clause BSD since 2.07

* Tue Mar 23 2010 Adam Tkac <atkac redhat com> - 2.08.01-1
- update to 2.08.01

* Thu Aug 20 2009 Zdenek Prikryl <zprikryl@redhat.com> - 2.07-3
- Don't complain if installing with --excludedocs (#515944)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Adam Tkac <atkac redhat com> - 2.07-1
- update to 2.07

* Fri Jul 10 2009 Zdenek Prikryl <zprikryl@redhat.com> - 2.06-1
- updated to 2.06

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.05.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 12 2008 Zdenek Prikryl <zprikryl@redhat.com> - 2.05.01-1
- updated to 2.05.01

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.03.01-2
- fix license tag

* Thu Jun 19 2008 Petr Machata <pmachata@redhat.com> - 2.03.01-1
- rebase to a new stable upstream version 2.03.01

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.01-2
- Autorebuild for GCC 4.3

* Tue Jan 29 2008 Petr Machata <pmachata@redhat.com> - 2.01-1
- rebase to a new stable upstream version 2.01

* Wed Feb  7 2007 Petr Machata <pmachata@redhat.com> - 0.98.39-5
- tidy up the specfile per rpmlint comments
- use utf-8 and fix national characters in contributor's names
- port bogus elf patch to new nasm version and turn it on again

* Thu Jan 25 2007 Petr Machata <pmachata@redhat.com> - 0.98.39-4
- Ville Skyttä: patch for non-failing %%post, %%preun
- Resolves: #223714

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.98.39-3.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.98.39-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.98.39-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Apr  4 2005 Jeremy Katz <katzj@redhat.com> - 0.98.39-3
- pdf docs are duplication of html, txt and postscript

* Fri Apr 01 2005 Jindrich Novy <jnovy@redhat.com> 0.98.39-2
- fix yet another vsprintf buffer overflow (#152963)

* Thu Mar 31 2005 Jindrich Novy <jnovy@redhat.com> 0.98.39-1
- update to 0.98.39
- add BuildRequires ghostscript, texinfo to doc subpackage (#110584)
- generate also PDF documentation for nasm (#88431)
- new release fixes CAN-2004-1287 (#143052)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 26 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 0.98.38 and specfile cleanup

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 17 2002 Phil Knirsch <pknirsch@redhat.com> 0.98.35-2
- Removed ExclusiveArch tag.
- Fixed typo in homepage URL.

* Wed Dec 11 2002 Thomas Woerner <twoerner@redhat.com> 0.98.35-1
- new version 0.98.35
- nasm has new homepage (#77323)

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 0.98.34-2
- fix %%doc list
- remove unpackaged files from the buildroot

* Mon Sep 16 2002 Jeremy Katz <katzj@redhat.com> 0.98.34-1hammer
- add x86_64 to ExclusiveArch list

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.98.34-1
- 0.98.34

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.98.32-1
- 0.98.32
- Various doc files have changed names/been removed/added
- New download location (after the license change, it's at sourceforge)
- The new version is LGPL
- Only build on x86 (#65255)

* Tue Feb 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.98.22-2
- Rebuild

* Mon Jan 21 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to 0.98.22 to fix bogus code generation in SDL
- Fix spec file, handle RPM_OPT_FLAGS

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Aug  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Updated patch from H.J. Lu for bogus elf generation (#45986,
  verified by reporter) 

* Thu Apr 26 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Updated patch for bogus elf generation from hjl@gnu.org

* Tue Feb 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add patch from H.J. Lu to avoid creating bogus elf objects (#27489)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- rewrote almost everything. The old specfile was bad, bad, bad.
  Really Bad.

* Tue Apr 04 2000 Erik Troan <ewt@redhat.com>
- moved to distribution (syslinux needs it)
- gzipped man pages

* Thu Dec 02 1999 Preston Brown <pbrown@redhat.com>
- adopted from one of the best .spec files I have seen in a long time. :)
