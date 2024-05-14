Summary: Library for parsing IDL (Interface Definition Language)
Name: libIDL
Version: 0.8.14
Release: 23%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: https://ftp.gnome.org/pub/gnome/sources/libIDL/0.8/
Source: https://download.gnome.org/sources/libIDL/0.8/%{name}-%{version}.tar.bz2
Patch0: libIDL-0.8.6-multilib.patch
License: LGPLv2+
BuildRequires:  gcc
BuildRequires: pkgconfig >= 0.8
BuildRequires: glib2-devel >= 2.0
BuildRequires: flex bison

%description
libIDL is a library for parsing IDL (Interface Definition Language).
It can be used for both COM-style and CORBA-style IDL.

%package devel
Summary: Development libraries and header files for libIDL
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig >= 0.8
Requires: glib2-devel >= 2.0

%description devel
libIDL is a library for parsing IDL (Interface Definition Language).
It can be used for both COM-style and CORBA-style IDL.

This package contains the header files and libraries needed to write
or compile programs that use libIDL.

%prep
%setup -q -n %{name}-%{version}
%patch 0 -p1 -b .multilib

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*a

%ldconfig_scriptlets

%files
%{_libdir}/libIDL-*.so.*

%doc AUTHORS COPYING README NEWS BUGS MAINTAINERS

%files devel
%{_includedir}/libIDL-2.0/
%{_libdir}/libIDL-*.so
%{_libdir}/pkgconfig/libIDL-*.pc
%{_bindir}/libIDL-config-2
%{_infodir}/libIDL2.info.*

%changelog
* Wed Nov 03 2021 Muhammad Falak <mwani@microsft.com> - 0.8.14-23
- Remove epoch from pkgconfig

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.14-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Björn Esser <besser82@fedoraproject.org> - 0.8.14-19
- Remove hardcoded gzip suffix from GNU info pages

* Thu Mar  7 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 0.8.14-18
- Remove obsolete requirements for %%post/%%preun scriptlets

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.14-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Aug 18 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 0.8.14-2
- Merge review fixes (BZ #226028).

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 0.8.14-1
- Update to 0.8.14

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> - 0.8.13-1
- Update to 0.8.13

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.12-1
- Update to 0.8.12

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.11-1
- Update to 0.8.11

* Fri Feb  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.10-2
- Rebuild for gcc 4.3

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.10-1
- Update to 0.8.10

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.9-2
- Don't use G_GNUC_PRETTY_FUNCTION

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.9-1
- Update to 0.8.9

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.8-2
- Update the license field

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.8-1
- Update to 0.8.8

* Tue Jan 30 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.7-2
- Fix scriptlets to be failsafe (#223706)

* Wed Aug  2 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.7-1.fc6
- Update to 0.8.7

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8.6-6.1
- rebuild

* Mon Jun 12 2006 Bill Nottingham <notting@redhat.com> - 0.8.6-6
- we don't call the autotools or libtoolize during build - don't
  buildreq them

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.6-5
- Fix missing BuildRequires

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.6-4
- Fix missing BuildRequires

* Tue May 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.6-3
- Fix multilib conflicts

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8.6-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8.6-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov  7 2005 Matthias Clasen <mclasen@redhat.com> 0.8.6-2
- Remove .la files and static libraries from the 
  -devel package

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 0.8.6-1
- Update to 0.8.6

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> 0.8.5-2
- Rebuild

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> 0.8.5-1
- Update to 0.8.5

* Wed Aug 18 2004 Mark McLoughlin <markmc@redhat.com> 0.8.4-1
- Update to 0.8.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 0.8.3-1
- update to 0.8.3

* Thu Aug  7 2003 Jonathan Blandford <jrb@redhat.com> 0.8.2-1
- rebuild for GNOME 2.4

* Thu Jun 26 2003 Havoc Pennington <hp@redhat.com> 0.8.0-10
- rebuild again in different place...

* Tue Jun 24 2003 Havoc Pennington <hp@redhat.com> 0.8.0-9
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 0.8.0-7
- fix URL (#79157)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 10 2002 Tim Powers <timp@redhat.com> 0.8.0-5
- don't include info/dir, it conflicts with the info package

* Mon Dec  9 2002 Havoc Pennington <hp@redhat.com>
- rebuild

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 06 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun  4 2002 Havoc Pennington <hp@redhat.com>
- 0.8.0

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Apr 25 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- move include files to -devel
- other spec file tweaks

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 0.7.4

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- cvs snap 0.7.1.91

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- cvs snap, rebuild on new glib 1.3.11

* Fri Oct 26 2001 Havoc Pennington <hp@redhat.com>
- glib 1.3.10

* Thu Oct  4 2001 Havoc Pennington <hp@redhat.com>
- rebuild for new glib

* Thu Sep 27 2001 Havoc Pennington <hp@redhat.com>
- initial build of standalone libIDL
- fix braindamage

