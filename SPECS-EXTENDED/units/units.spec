Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: A utility for converting amounts from one unit to another
Name: units
Version: 2.23
Release: 4%{?dist}
Source: https://ftp.gnu.org/gnu/units/%{name}-%{version}.tar.gz
URL: https://www.gnu.org/software/units/units.html
License: GPL-3.0-or-later

Requires: less

BuildRequires: bison
BuildRequires: gcc
BuildRequires: make
BuildRequires: ncurses-devel
BuildRequires: python3-devel
BuildRequires: readline-devel

# do not update currency.units from network during build
Patch100: 0100-units-2.22-no-network.patch

# make less a default pager to avoid error about missing /usr/bin/pager
Patch101: 0101-fix-make-less-default-pager.patch

%description
Units converts an amount from one unit to another, or tells you what
mathematical operation you need to perform to convert from one unit to
another. The units program can handle multiplicative scale changes as 
well as conversions such as Fahrenheit to Celsius.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

# replace an absolute symlink by a relative symlink
ln -fsv ../../..%{_sharedstatedir}/units/currency.units %{buildroot}%{_datadir}/units

gzip %{buildroot}%{_infodir}/units.info

# provide a man page for units_cur as a symlink to units.1
ln -s units.1 %{buildroot}%{_mandir}/man1/units_cur.1

%check
make check

%files
%doc COPYING NEWS README
%{_bindir}/units
%{_bindir}/units_cur
%{_datadir}/units
%{_sharedstatedir}/units
%{_infodir}/*
%{_mandir}/man1/*

%changelog
* Thu Jan 16 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 2.23-4
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 11 2024 Jan Macku <jamacku@redhat.com> - 2.23-2
- fix make less the default pager (#2268395)

* Mon Feb 19 2024 Jan Macku <jamacku@redhat.com> - 2.23-1
- new upstream release

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.22-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 30 2023 Florian Weimer <fweimer@redhat.com> - 2.22-7
- C compatibility fix for the configure script (#2252276)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Lukáš Zaoral <lzaoral@redhat.com> - 2.22-5
- migrate to SPDX license format

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.22-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 06 2022 Kamil Dudka <kdudka@redhat.com> - 2.22-3
- remove a build system tweak related to Python 3 no longer needed

* Tue Sep 06 2022 Kamil Dudka <kdudka@redhat.com> - 2.22-2
- replace an absolute symlink by a relative symlink
- use %%make_build and %%make_install RPM macros

* Tue Sep 06 2022 Kamil Dudka <kdudka@redhat.com> - 2.22-1
- new upstream release

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Kamil Dudka <kdudka@redhat.com> - 2.21-1
- new upstream release

* Thu Oct 01 2020 Kamil Dudka <kdudka@redhat.com> - 2.20-1
- new upstream release

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jun 01 2019 Kamil Dudka <kdudka@redhat.com> - 2.19-1
- new upstream release

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.18-3
- Rebuild for readline 8.0

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 29 2018 Kamil Dudka <kdudka@redhat.com> - 2.18-1
- new upstream release

* Wed Aug 08 2018 Kamil Dudka <kdudka@redhat.com> - 2.17-5
- do not update currency.units from network during build
- units_cur: validate rate data from server (#1598913)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Kamil Dudka <kdudka@redhat.com> - 2.17-3
- use %%{__python3} as the python interpreter

* Wed Jun 27 2018 Kamil Dudka <kdudka@redhat.com> - 2.17-2
- drop the dependency on python3-unidecode no longer used by units_cur

* Tue Jun 26 2018 Kamil Dudka <kdudka@redhat.com> - 2.17-1
- new upstream release

* Mon May 28 2018 Kamil Dudka <kdudka@redhat.com> - 2.16-5
- make units_cur work again (#1574835)

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 2.16-4
- add explicit BR for the gcc compiler

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Kamil Dudka <kdudka@redhat.com> - 2.16-2
- make units_cur use Python 3

* Wed Nov 01 2017 Kamil Dudka <kdudka@redhat.com> - 2.16-1
- new upstream release

* Tue Oct 31 2017 Kamil Dudka <kdudka@redhat.com> - 2.15-1
- new upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 09 2017 Kamil Dudka <kdudka@redhat.com> - 2.14-1
- new upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.13-2
- Rebuild for readline 7.x

* Tue Jun 21 2016 Kamil Dudka <kdudka@redhat.com> - 2.13-1
- new upstream release

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 15 2015 Kamil Dudka <kdudka@redhat.com> - 2.12-1
- new upstream release

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Oct 13 2014 Kamil Dudka <kdudka@redhat.com> - 2.11-4
- add BR for python in order to get the units_cur script installed (#1151997)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Kamil Dudka <kdudka@redhat.com> - 2.11-1
- new upstream release

* Mon Mar 31 2014 Kamil Dudka <kdudka@redhat.com> - 2.10-2
- require python-unidecode used by the units_cur script
- improve utf-8 support in the units_cur script

* Thu Mar 27 2014 Kamil Dudka <kdudka@redhat.com> - 2.10-1
- new upstream release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Kamil Dudka <kdudka@redhat.com> - 2.02-1
- new upstream release

* Mon May 20 2013 Kamil Dudka <kdudka@redhat.com> - 2.01-3
- provide a man page for units_cur as a symlink to units.1
- mention the --check-verbose option in units.1 man page

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.01-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 25 2012 Kamil Dudka <kdudka@redhat.com> - 2.01-1
- new upstream release

* Fri Sep 07 2012 Kamil Dudka <kdudka@redhat.com> - 2.00-4
- run the upstream smoke-test during build

* Tue Aug 28 2012 Kamil Dudka <kdudka@redhat.com> - 2.00-3
- fix specfile issues reported by the fedora-review script

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 02 2012 Kamil Dudka <kdudka@redhat.com> - 2.00-1
- new upstream release, dropped applied patches
- patch Makefile.in to respect $(DESTDIR)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.88-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 17 2011 Kamil Dudka <kdudka@redhat.com> - 1.88-5
- improve the units-1.88-coverity.patch (thanks to Adrian Mariano)

* Wed Nov 16 2011 Kamil Dudka <kdudka@redhat.com> - 1.88-4
- fix code defects found by Coverity

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.88-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May 05 2010 Kamil Dudka <kdudka@redhat.com> - 1.88-2
- fix typo in man page (#588565)

* Tue Feb 23 2010 Kamil Dudka <kdudka@redhat.com> - 1.88-1
- new upstream release, dropped applied patches

* Tue Dec 01 2009 Kamil Dudka <kdudka@redhat.com> - 1.87-7
- add BuildRequires for bison

* Tue Dec 01 2009 Kamil Dudka <kdudka@redhat.com> - 1.87-6
- update license to GPLv3+, sanitize specfile
- fix tons of gcc warnings

* Thu Aug 20 2009 Zdenek Prikryl <zprikryl@redhat.com> - 1.87-5
- Don't complain if installing with --excludedocs (#515941)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.87-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.87-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.87-2
- Autorebuild for GCC 4.3

* Wed Oct 31 2007 Zdenek Prikryl <zprikryl@redhat.com> - 1.87-1
- New version 1.87 

* Thu Aug 23 2007 Harald Hoyer <harald@redhat.com> - 1.86-7
- changed license tag

* Thu Jul 05 2007 Florian La Roche <laroche@redhat.com>
- fix preun script to properly remove the info file

* Fri Mar 23 2007 Harald Hoyer <harald@redhat.com> - 1.86-5
- more specfile cleanups

* Tue Mar 20 2007 Harald Hoyer <harald@redhat.com> - 1.86-4
- added readline build requirement
- changed BUILDROOT

* Wed Jan 24 2007 Harald Hoyer <harald@redhat.com> - 1.86-3
- fixed previous fix for rhbz#220533

* Tue Jan 23 2007 Florian La Roche <laroche@redhat.com> - 1.86-2
- rhbz#220533

* Mon Nov 13 2006 Florian La Roche <laroche@redhat.com> - 1.86-1
- 1.86

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.85-1.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.85-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.85-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Jul 19 2005 Harald Hoyer <harald@redhat.com> - 1.85-1
- version 1.85

* Thu Mar 03 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com>
- Rebuilt for new readline.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 24 2003 Harald Hoyer <harald@redhat.de> 1.80-8
- au is now astronomicalunit

* Wed Jun 11 2003 Harald Hoyer <harald@redhat.de> 1.80-7
- fix parsecs #96982

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 23 2003 Jeremy Katz <katzj@redhat.com> 1.80-5
- fix build with gcc 3.3

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 17 2002 Harald Hoyer <harald@redhat.de> 1.80-2
- changed description

* Tue Nov 05 2002 Harald Hoyer <harald@redhat.de> 1.80-1
- update to version 1.80

* Tue Jul 23 2002 Harald Hoyer <harald@redhat.de>
- removed prestripping

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 14 2001 Harald Hoyer <harald@redhat.de> 1.74-1
- bumped version
- this fixed #54971

* Fri May 11 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.55-10
- rebuild with new readline

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- rebuild, FHS stuff

* Wed Apr  5 2000 Bill Nottingham <notting@redhat.com>
- rebuild against current ncurses/readline

* Fri Mar 24 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild with new readline

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Mon Nov 22 1999 Bill Nottingham <notting@redhat.com>
- fix install-info (#6631)

* Mon Sep 13 1999 Bill Nottingham <notting@redhat.com>
- strip files

* Mon Aug  2 1999 Bill Nottingham <notting@redhat.com>
- update to 1.55

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Thu Dec 17 1998 Michael Maher <mike@redhat.com>
- built package for 6.0

* Sun Aug 23 1998 Jeff Johnson <jbj@redhat.com>
- units.lib corrections (problem #685)

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- spec file cleanups

* Mon Jul 21 1997 Erik Troan <ewt@redhat.com>
- built against glibc
