Summary:        A hexadecimal file viewer and editor
Name:           hexedit
Version:        1.2.13
Release:        19%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://rigaux.org/hexedit.html
Source:         http://rigaux.org/%{name}-%{version}.src.tgz
Patch1:         hexedit-1.2.13-config.patch
# Document --color option.  Sent upstream 2013-04-05.
Patch2:         hexedit-man-page-color.patch

BuildRequires:  gcc
BuildRequires:  ncurses-devel

%description
Hexedit shows a file both in ASCII and in hexadecimal. The file can be a device
as the file is read a piece at a time. Hexedit can be used to modify the file
and search through it.

%prep
%setup -q -n %{name}

%patch1 -p1 -b .config
%patch2 -p1 -b .color

%build
%configure
make %{_smp_mflags}

%install
make install \
  mandir=%{buildroot}%{_mandir} \
  bindir=%{buildroot}%{_bindir} \
  INSTALL='install -p'

%files
%license COPYING
%doc hexedit-%{version}.lsm Changes
%{_bindir}/hexedit
%{_mandir}/man1/hexedit.1*

%changelog
* Fri Apr 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.13-19
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.13-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Marek Skalický <mskalick@redhat.com> - 1.2.13-13
- Add missing BuildRequires: gcc/gcc-c++

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 05 2013 Richard W.M. Jones <rjones@redhat.com> - 1.2.13-3
- Add patch to document --color option.
- Modernize the spec file.

* Tue Mar 26 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.2.13-2
- Bring back config patch to fix -debuginfo, it hasn't been upstreamed yet.
- Drop empty TODO from docs.

* Thu Mar 21 2013 Jon Ciesla <limburger@gmail.com> - 1.2.13-1
- Latest upstream.
- Config patch upstreamed.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2.12-15
- Fix URL and Source for new upstream location.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 12 2008 Jiri Moskovcak <jmoskovc@redhat.com> - 1.2.12-9
- rebuild

* Mon Dec 17 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 1.2.12-8
- minor spec file fixes

* Thu Nov  1 2007 Jiri Moskovcak <jmoskovc@redhat.com> - 1.2.12-7
- spec file cleanup

* Tue Sep 18 2007 Jiri Moskovcak <jmoskovc@redhat.com> 1.2.12-6
- changed to new upstream source tarbal with some minor fixes

* Fri Apr 06 2007 Jindrich Novy <jnovy@redhat.com> 1.2.12-5
- spec fixes

* Wed Nov 29 2006 Jindrich Novy <jnovy@redhat.com> 1.2.12-4
- fix URL, add dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.12-3.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.12-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.12-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 26 2006 Jindrich Novy <jnovy@redhat.com> 1.2.12-3
- rebuilt (#178824)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Oct 25 2005 Jindrich Novy <jnovy@redhat.com> 1.2.12-2
- rewrite %%description - the original one was a nonsense (#171685)

* Mon Oct  3 2005 Jindrich Novy <jnovy@redhat.com> 1.2.12-1
- update to 1.2.12
- new upstream release introduces "fruit salad" colored hexeditor ;-)
  (try --color)

* Fri Mar  4 2005 Jindrich Novy <jnovy@redhat.com> 1.2.10-4
- rebuilt with gcc4

* Thu Feb 10 2005 Jindrich Novy <jnovy@redhat.com> 1.2.10-3
- remove -D_FORTIFY_SOURCE=2 from CFLAGS, present in RPM_OPT_FLAGS

* Wed Feb  9 2005 Jindrich Novy <jnovy@redhat.com> 1.2.10-2
- rebuilt with -D_FORTIFY_SOURCE=2

* Mon Aug 2 2004 Jindrich Novy <jnovy@redhat.com> 1.2.10-1
- updated to 1.2.10-1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 1.2.7-1
- update to 1.2.7

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 6 2003 Than Ngo <than@redhat.com> 1.2.4-1
- 1.2.4

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.2.2-7
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 18 2002 Than Ngo <than@redhat.com> 1.2.2-5
- don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Feb 28 2002 Than Ngo <than@redhat.com> 1.2.2-3
- rebuild in new inviroment

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Nov 27 2001 Than Ngo <than@redhat.com> 1.2.2-1
- updated to 1.2.2
- fixed Url

* Thu Aug  9 2001 Than Ngo <than@redhat.com> 1.2.1-3
- install man page in correct place

* Tue Jul 31 2001 Than Ngo <than@redhat.com> 1.2.1-2
- fix bug #50488

* Tue Jun 26 2001 Than Ngo <than@redhat.com> 1.2.1-1
- update to 1.2.1
- Copyright -> License
- add some Buildprereqs

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- built for the ldistro

* Fri Feb  9 2001 Tim Powers <timp@redhat.com>
- patched so that it doesn't segfault on ia64 (bug 26845)

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jun 7 2000 Tim Powers <timp@redhat.com>
- fixed man page location
- use %%makeinstall
- use predefined RPM macros wherever possible
- patched so that regular users can build

* Fri May 12 2000 Tim Powers <timp@redhat.com>
- rbeuilt for 7.0
- made so that man pages are gzipped by RPM (glob)

* Thu Jul 15 1999 Tim Powers <timp@redhat.com>
- updated source
- cleaned up %%build section. Now uses make install instead of install
  blah....
-built for 6.1

* Tue Oct 06 1998 Michael Maher <mike@redhat.com>
- updated package

* Mon Jul 20 1998 Michael Maher <mike@redhat.com> 
- built package
