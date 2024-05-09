Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global mpr_version 5.03-2390-2390-20191017
Summary: Russian man pages from the Linux Documentation Project
Name: man-pages-ru
Version: 5.03
Release: 4%{?dist}
# Multiple man pages are distributed under different licenses.
License: GPL+ and BSD and MIT and GFDL
URL: https://sourceforge.net/projects/man-pages-ru/
Source: https://sourceforge.net/projects/man-pages-ru/files/man-pages-ru_%{mpr_version}.tar.bz2

Requires: man-pages-reader
Supplements: (man-pages and langpacks-ru)

BuildArch: noarch

%description
Manual pages from the Linux Documentation Project, translated into
Russian.

%prep
%setup -q -n man-pages-ru_%{mpr_version}

# remove .so links to nonexisting pages
for exp in $(grep -rw "^\.so" . | tr " " "_"); do
    link=${exp#.*:\.so_}
    [ -f $link ] || rm -f ${exp%:.*}
done

# Remove non-free files. License has a restriction on modification
# or no permission to modify at all.
rm man2/sysinfo.2
rm man2/getitimer.2

%build
# nothing to build

%install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/ru
cp -pr ./man? $RPM_BUILD_ROOT%{_mandir}/ru

%files
%doc README
%license License
%{_mandir}/ru/man*/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.03-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.03-3.20191017
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Nikola Forró <nforro@redhat.com> - 5.03-2.20191017
- Update to version 5.03-2390-2390-20191017
  resolves #1762595

* Mon Sep 30 2019 Nikola Forró <nforro@redhat.com> - 5.03-1.20190927
- Update to version 5.03-2389-2389-20190927
  resolves #1756464

* Wed Sep 25 2019 Nikola Forró <nforro@redhat.com> - 5.02-1.20190918
- Update to version 5.02-2387-2387-20190918
  resolves #1753344

* Wed Aug 21 2019 Nikola Forró <nforro@redhat.com> - 5.00-1.20190811
- Update to version 5.00-2386-2386-20190811
  resolves #1742665

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.16-4.20180422
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.16-3.20180422
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.16-2.20180422
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 Nikola Forró <nforro@redhat.com> - 4.16-1.20180422
- Update to version 4.16-2383-2383-20180422
  resolves #1570375

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.15-2.20180113
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Nikola Forró <nforro@redhat.com> - 4.15-1.20180113
- Update to version 4.15-2383-2383-20180113
  resolves #1534131

* Thu Jan 04 2018 Nikola Forró <nforro@redhat.com> - 4.15-1.20171221
- Update to version 4.15-2383-2383-20171221
  resolves #1528488

* Tue Dec 12 2017 Jiri Kucera <jkucera@redhat.com> - 4.15-1.20171208
- Update to version 4.15-2380-2380-20171208
  resolves #1523887

* Tue Nov 14 2017 Nikola Forró <nforro@redhat.com> - 4.14-1.20171111
- Update to version 4.14-2374-2374-20171111
  resolves #1512183

* Fri Oct 20 2017 Nikola Forró <nforro@redhat.com> - 4.13-1.20171018
- Update to version 4.13-2363-2363-20171018
  resolves #1504360

* Tue Sep 05 2017 Nikola Forró <nforro@redhat.com> - 4.11-1.20170904
- Update to version 4.11-2358-2358-20170904
  resolves #1488137

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.08-2.20170321
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Nikola Forró <nforro@redhat.com> - 4.08-1.20170321
- Update to version 4.08-2329-2272-20170321
  resolves #1434630

* Wed Mar 15 2017 Nikola Forró <nforro@redhat.com> - 4.08-1.20170309
- Update to version 4.08-2329-2269-20170309
  resolves #1430954

* Tue Mar 07 2017 Nikola Forró <nforro@redhat.com> - 4.08-1.20170304
- Update to version 4.08-2329-1767-20170304
  resolves #1429982

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.05-2.20161008
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Nikola Forró <nforro@redhat.com> - 4.05-1.20161008
- Update to version 4.05-2306-2240-20161008
  resolves #1397272

* Mon Jun 13 2016 Tom Callaway <spot@fedoraproject.org> - 3.81-4.20151031
- remove non-free file (bz1334292)

* Sat Feb 27 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.81-3.20151031
- Add Supplements: for https://fedoraproject.org/wiki/Packaging:Langpacks guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.81-2.20151031
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Nikola Forró <nforro@redhat.com> - 3.81-1.20151031
- Update to version 3.81-2230-2024-20151031
  resolves #1284280

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.41-5.20120901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.41-4.20120901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.41-3.20120901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.41-2.20120901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Peter Schiffer <pschiffe@redhat.com> - 3.41-1.20120901
- updated to the latest upstream tarball 3.41-2145-1699-20120901
- cleaned .spec file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 30 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.98-5
- Man-pages-ru 3.32-2087-1553-20110626
- fix build

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Alexey Kurov <nucleo@fedoraproject.org> - 0.98-3
- Man-pages-ru 3.32-2087-1512-20101219

* Fri Aug 13 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.98-2
- remove bogus links

* Fri Jul 23 2010 Alexey Kurov <nucleo@fedoraproject.org> - 0.98-1
- updated Source to 0.98 (0.97-0.98 patch)
- updated Source1 to 3.25-2064-1352-20100717
- moved encoding converting to prep section

* Tue May 11 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.97-10
- add new source (Source1)

* Fri Apr 16 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.97-9
- add man-pages-reader dependence

* Wed Mar 17 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 0.97-8
- remove directories from the package
  fix minor spec problems

* Fri Dec 18 2009 Ivana Hutarova Varekova <varekova@redhat.com> - 0.97-7
- fix the source tags

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.97-4
- fix license tag

* Mon Jun 16 2008 Ivana Varekova <varekova@redhat.com> - 0.97-3
- rebuild
- change license tag

* Fri Mar  2 2007 Ivana Varekova <varekova@redhat.com> - 0.97-2
- Resolves: 226129
  incorporate package review feedback

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.97-1.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Oct 21 2004 Adrian Havill <havill@redhat.com> 0.97-1
- Russian translation project active again; newest update merged with
  working Makefile (#131659)

* Wed Sep 29 2004 Elliot Lee <sopwith@redhat.com> 0.7-8
- Rebuild

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 11 2003 Phil Knirsch <pknirsch@redhat.com> 0.7-6
- Convert all manpages to utf-8.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.7-5
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 0.7-4
- rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 13 2002 Trond Eivind Glomsrød <teg@redhat.com> 0.7-1
- 0.7

* Thu Aug  2 2001 Trond Eivind Glomsrød <teg@redhat.com>
- s/Copyright/License/
- Own %%{_mandir}/ru

* Wed Apr  4 2001 Trond Eivind Glomsrød <teg@redhat.com>
- roff fixes

* Mon Feb  5 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Version 0.6

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 20 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to compress man pages.

* Sun Jun 11 2000 Trond Eivind Glomsrød <teg@redhat.com>
- first build
