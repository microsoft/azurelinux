Name:		transfig
Version:	3.2.7b
Release:	4%{?dist}
Summary:	Utility for converting FIG files (made by xfig) to other formats
License:	MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		https://sourceforge.net/projects/mcj/
Source0:	http://downloads.sourceforge.net/mcj/fig2dev-%{version}.tar.xz
Source1:  %{name}-LICENSE.txt
# Patches from upstream for CVE-2019-19746 and CVE-2019-19797 + deps
Patch1:		0001-Embed-png-and-jpeg-images-unchanged-into-pdfs.patch
Patch2:		0002-Allow-fig-2-text-ending-with-multiple-A-ticket-55.patch
Patch3:		0003-Reject-huge-arrow-types-ticket-57.patch
Patch4:		0004-Convert-polygons-with-too-few-points-to-polylines.patch
Patch5:		0005-Correctly-scan-embedded-pdfs-for-MediaBox-value.patch
Patch6:		0006-fig2dev-version-prints-version-information.patch
Patch7:		0007-Use-getopt-from-standard-libraries-if-available.patch
Patch8:		0008-Replace-most-calls-to-fgets-by-getline-in-read.c.patch
Patch9:   fix-header.patch

Requires:	ghostscript
Requires:	bc
Requires:	netpbm-progs

BuildRequires:	gcc libtool
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	ghostscript

%description
The transfig utility creates a makefile which translates FIG (created
by xfig) or PIC figures into a specified LaTeX graphics language (for
example, PostScript(TM)).  Transfig is used to create TeX documents
which are portable (i.e., they can be printed in a wide variety of
environments).

Install transfig if you need a utility for translating FIG or PIC
figures into certain graphics languages.


%prep
%autosetup -p1 -n fig2dev-%{version}
autoreconf -i
# Fix the manpage not being in UTF-8
iconv -f ISO-8859-15 -t UTF-8 man/fig2dev.1.in -o fig2dev.1.in.new
touch -r man/fig2dev.1.in fig2dev.1.in.new
mv fig2dev.1.in.new man/fig2dev.1.in

cp %{SOURCE1} ./LICENSE.txt


%build
%configure --enable-transfig
%make_build


%install
%make_install


%files
%license LICENSE.txt
%doc CHANGES transfig/doc/manual.pdf
%{_bindir}/transfig
%{_bindir}/fig2dev
%{_bindir}/fig2ps2tex
%{_bindir}/pic2tpic
%{_datadir}/fig2dev/i18n/*.ps
%{_mandir}/man1/*.1.gz


%changelog
* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 3.2.7b-5
- License verified

* Thu Oct 28 2021 Muhammad Falak <mwani@microsft.com> - 3.2.7b-4
- Remove epoch

* Wed Mar 31 2021 Henry Li <lihl@microsoft.com> - 1:3.2.7b-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove libXpm-devel from build requirement 
- Add patch to include stddef.h

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.7b-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Hans de Goede <hdegoede@redhat.com> - 1:3.2.7b-1
- New upstream release 3.2.7b
- Add patch fixing CVE-2019-19746 (rhbz#1787040)
- Add patch fixing CVE-2019-19797 (rhbz#1786726)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.7a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:3.2.7a-2
- Add BR: ghostscript to fix ghostscript detection (#1720868)

* Thu Jun 06 2019 Ondrej Dubaj <odubaj@redhat.com> - 1:3.2.7a-1
- Updated to version 3.2.7a

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.6a-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 16 2018 Honza Horak <hhorak@redhat.com> - 1:3.2.6a-5
- Remove license GPLv3+

* Sun Jul 15 2018 Honza Horak <hhorak@redhat.com> - 1:3.2.6a-4
- Add license GPLv3+

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.6a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.6a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Hans de Goede <hdegoede@redhat.com> - 3.2.6a-1
- New upstream release 3.2.6a
- Add patch fixing CVE-2017-16899 (rhbz#1515695)

* Tue Nov 07 2017 Adam Jackson <ajax@redhat.com> - 3.2.6-6
- Remove unnecessary BuildRequires: imake

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 19 2016 Tomas Repik <trepik@redhat.com> - 1:3.2.6-2
- added missing requires for netpbm-progs (RHBZ#1371667)

* Fri Aug 12 2016 Jozef Mlich <imlich@fit.vutbr.cz> - 1:3.2.6-1
- Resolves #1366524
  rebase to fig2dev 3.2.6

* Thu Mar 31 2016 Tomas Repik <trepik@redhat.com> - 1:3.2.5d-18
- reading alpha channel of png files properly (#1282615)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.5d-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 03 2013 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5d-13
- make it compile with -Werror=format-security (#1037365)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 15 2013 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5d-11
- install man pages using the correct file name suffix
- provide the fig2ps2tex.sh man page as a symlink

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5d-9
- fix specfile issues reported by the fedora-review script

* Thu Aug 09 2012 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5d-8
- fix buffer overflow on loading a malformed .fig file (CVE-2009-4227)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 14 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1:3.2.5d-6
- add Gentoo patch to fix compilation with libpng 1.5

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1:3.2.5d-4
- Rebuild for new libpng

* Tue Aug 09 2011 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5d-3
- fix crash of fig2dev on a failure of ghostscript (#728825)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 04 2010 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5d-1
- new upstream release (#546623)

* Wed Mar 03 2010 Kamil Dudka <kdudka@redhat.com> - 1:3.2.5c-1
- new upstream release
- patch to generate comments compliant with DSC 3.0, thanks to Ian Dall
  (#558380)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May  5 2009 Ville Skyttä <ville.skytta at iki.fi> - 1:3.2.5-7
- Get rid of csh dependency, add missing one on bc (#435993).
- Build with $RPM_OPT_FLAGS (#329831).
- Convert specfile to UTF-8.
- Add URL, fix source URL.
- Escape macros in changelog.
- Improve summary.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 20 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1:3.2.5-5
- Add transfig-3.2.5-bitmap.patch, tweak permission on sources (BZ #209865).

* Wed Sep 10 2008 Stepan Kasal <skasal@redhat.com> - 1:3.2.5-4
- remove transfig.3.2.4-pstex.patch, which reintroduced #164140
  at the update to 3.2.5

* Mon Sep  8 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:3.2.5-3
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:3.2.5-2
- Autorebuild for GCC 4.3

* Mon Apr 16 2007 Than Ngo <than@redhat.com> - 1:3.2.5-1.fc7
- 3.2.5

* Wed Aug 16 2006 Stepan Kasal <skasal@redhat.com> - 1:3.2.4-16
- Require ghostscript; fig2dev calls it.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.2.4-15.1
- rebuild

* Tue May 16 2006 Than Ngo <than@redhat.com> 3.2.4-15
- fix #164140, transfig creates wrong dependencies for -L pstex

* Tue May 16 2006 Than Ngo <than@redhat.com> 3.2.4-14
- fix #191825, buildrequire on imake
- fix #173748, fig2dev still refers to /usr/X11R6/lib/X11/rgb.txt

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:3.2.4-13.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:3.2.4-13.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Dec 19 2005 Than Ngo <than@redhat.com> 3.2.4-13
- fix build problem with modular X

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 15 2005 Than Ngo <than@redhat.com> 1:3.2.4-12
- fix for modular X 

* Sat Mar 05 2005 Than Ngo <than@redhat.com> 1:3.2.4-11
- rebuild

* Tue Nov 30 2004 Than Ngo <than@redhat.com> 1:3.2.4-10
- fix compiler warnings #111394
- fix broken language selection #114849

* Tue Nov 30 2004 Than Ngo <than@redhat.com> 1:3.2.4-9
- add patch to fix getrgb #117099

* Mon Oct 18 2004 Miloslav Trmac <mitr@redhat.com> - 1:3.2.4-8
- Fix at least a few obvious instances of C abuse (partly #74594 with patch by
  Sysoltsev Slawa)
- Drop -Dcfree=free fix, not needed with current version

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Than Ngo <than@redhat.com> 3.2.4-4
- patch build problem

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 23 2003 Jeremy Katz <katzj@redhat.com> 1:3.2.4-2
- fix build with gcc 3.3

* Tue May  6 2003 Than Ngo <than@redhat.com> 3.2.4-1
- 3.2.4

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Than Ngo <than@redhat.com> 3.2.3d-8
- Added a patch file from d.binderman@virgin.net (bug #77980)

* Wed Jul 31 2002 Than Ngo <than@redhat.com> 3.2.3d-7
- fig2dev crashes with more than 1 gif files (bug #69917)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 14 2002 han Ngo <than@redhat.com> 3.2.3d-5
- fhs fixes (bug #66732)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jul 23 2001 Than Ngo <than@redhat.com>
- fix build dependencies (bug #49725)
- Copyright -> License

* Fri Jun 15 2001 Than Ngo <than@redhat.com>
- update to 3.2.3d release (Bug # 44742)

* Tue May 29 2001 Than Ngo <than@redhat.com>
- update to 3.2.3d beta2

* Fri Apr 13 2001 Than Ngo <than@redhat.com>
- fix core dump when using LDAP auth
- update ftp site 

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Enable Japanese

* Sat Aug 05 2000 Than Ngo <than@redhat.de>
- update to 3.2.3c (Bug fixed release)

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 13 2000 Trond Eivind Glomsrød <teg@redhat.com>
- make it build as nobody. Imake sucks.
- include LATEX.AND.XFIG
- use %%{_tmppath}

* Wed Apr 26 2000 Matt Wilson <msw@redhat.com>
- add enable_japanese option, disable it for now.

* Sun Apr 16 2000 Bryan C. Andregg <bandregg@redhat.com>
- new version to support -b and -g which xfig uses

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Tue Jul  7 1998 Jeff Johnson <jbj@redhat.com>
- update to 3.2.1.

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- add %%clean.

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Nov 13 1997 Otto Hammersmith <otto@redhat.com>
- fixed problem with Imakefile for fig2dev not including $(XLIB)
- build rooted.

* Fri Oct 24 1997 Otto Hammersmith <otto@redhat.com>
- recreated the glibc patch that is needed for an alpha build, missed it
  building on the intel.

* Tue Oct 21 1997 Otto Hammersmith <otto@redhat.com>
- updated version
- fixed source url

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
