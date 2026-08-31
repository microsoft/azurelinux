# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: A perfect hash function generator
Name: gperf
Version: 3.2.1
Release: 2%{?dist}
License: GPL-3.0-or-later
Source: https://ftp.gnu.org/pub/gnu/gperf/gperf-%{version}.tar.gz
URL: http://www.gnu.org/software/gperf/

BuildRequires:  gcc-c++
BuildRequires:  make

%description
Gperf is a perfect hash function generator written in C++. Simply
stated, a perfect hash function is a hash function and a data
structure that allows recognition of a key word in a set of words
using exactly one probe into the data structure.

%prep
%setup -q

%build
%configure
%make_build

%install
#mkdir -p $RPM_BUILD_ROOT/usr/share/{man,info}
%make_install

# remove the stuff from the buildroot
rm -rf $RPM_BUILD_ROOT{%{_mandir}/{dvi,html},%{_datadir}/doc}

%files
%doc README NEWS doc/*.{html,pdf} COPYING
%{_bindir}/%{name}
%{_mandir}/man1/gperf.1*
%{_infodir}/gperf.info*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Apr 13 2025 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1 (#2357802)

* Mon Apr 07 2025 Sérgio Basto <sergio@serjux.com> - 3.2-1
- Update gperf to 3.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 12 2023 Lukáš Zaoral <lzaoral@redhat.com> - 3.1-16
- migrate to SPDX license format

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Richard W.M. Jones <rjones@redhat.com> - 3.1-1
- New upstream version 3.1.
- Remove some obsolete cruft from the spec file.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.0.4-10
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 01 2010 Roman Rakus <rrakus@redhat.com> - 3.0.4-2
- Fixed license to the right GPLv3+

* Mon Mar 01 2010 Roman Rakus <rrakus@redhat.com> - 3.0.4-1
- Version 3.0.4

* Tue Aug 11 2009 Roman Rakus <rrakus@redhat.com> - 3.0.3-9
- Don't print errors in post and preun sections (#515942)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 27 2009 Roman Rakus <rrakus@redhat.com> - 3.0.3-6
- Don't use makeinstall
- Remove ps files from doc
  Resolves: #225854

* Mon Jan 19 2009 Roman Rakus <rrakus@redhat.com> - 3.0.3-5
- Specfile fixes
  Resolves: #225854

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.0.3-4
- Autorebuild for GCC 4.3

* Tue Jan 08 2008 Florian La Roche <laroche@redhat.com> - 3.0.3-3
- fix license tag and summary

* Tue Aug 21 2007 Florian La Roche <laroche@redhat.com> - 3.0.3-2
- rebuild

* Sun Jun 03 2007 Florian La Roche <laroche@redhat.com> - 3.0.3-1
- 3.0.3

* Mon Jan 22 2007 Florian La Roche <laroche@redhat.com>
- rhbz#223695

* Sat Nov 04 2006 Florian La Roche <laroche@redhat.com>
- 3.0.2 (#213852)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.0.1-7.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.0.1-7.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.0.1-7.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Aug 02 2005 Karsten Hopp <karsten@redhat.de> 3.0.1-7
- Gcc4 fix (Tomo Vuckovic) #164885 

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 3.0.1-6
- build with gcc-4

* Wed Feb 09 2005 Karsten Hopp <karsten@redhat.de> 3.0.1-5
- rebuilt

* Mon Oct 11 2004 Ivana Varekova <varekova@redhat.com>
- minor spec updates

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 3.0.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 08 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 3.0

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 22 2002 Tim Powers <timp@redhat.com>
- remove unpackaged files from the buildroot

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Mon Jul 22 2002 Tim Powers <timp@redhat.com>
- rebuild using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Sep 12 2001 Tim Powers <timp@redhat.com>
- rebuild with new gcc and binutils

* Tue Apr 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.7.2-1
- Update to 2.7.2

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- user infodir and mandir macros for FHS
- use %%makeinstall

* Fri Feb  4 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- rebuild to gzip manpage
- don't use CC=egcs
- fix description

* Wed Mar 24 1999 Cristian Gafton <gafton@redhat.com>
- added patches for egcs from UP

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Oct 29 1998 Bill Nottingham <notting@redhat.com>
- patch for latest egcs

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binary

* Tue Jul 28 1998 Jeff Johnson <jbj@redhat.com>
- create.
