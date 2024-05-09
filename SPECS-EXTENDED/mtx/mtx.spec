Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: mtx
Version: 1.3.12
Release: 23%{?dist}
Summary: SCSI media changer control program
License: GPLv2
Source0: https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# https://mtx.opensource-sw.net/bugs/view.php?id=9
Patch0: %{name}-1.3.12-destdir.patch
# https://mtx.opensource-sw.net/bugs/view.php?id=13
# https://bugzilla.redhat.com/show_bug.cgi?id=538403
Patch1: %{name}-1.3.12-argc.patch
URL: https://mtx.sourceforge.net/
BuildRequires: gcc


%description
The MTX program controls the robotic mechanism in autoloaders and tape
libraries such as the HP SureStore DAT 40x6, Exabyte EZ-17, and
Exabyte 220. This program is also reported to work with a variety of
other tape libraries and autochangers from ADIC, Tandberg/Overland,
Breece Hill, HP, and Seagate.

If you have a backup tape device capable of handling more than one
tape at a time, you should install MTX.


%prep
%setup -q

%patch 0 -p2 -b .destdir
%patch 1 -p2 -b .argc

# remove exec permission
chmod a-x contrib/config_sgen_solaris.sh contrib/mtx-changer


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT



%files
%doc CHANGES COMPATABILITY contrib FAQ LICENSE
%doc mtx.doc mtxl.README.html README TODO
%{_mandir}/man1/*
%{_sbindir}/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.12-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 19 2009 Dan Horák <dan[at]danny.cz> 1.3.12-5
- dropped debug output when tools are called with wrong number of arguments (#538403)
- added patch to support DESTDIR for installing

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 21 2008 Dan Horák <dan[at]danny.cz> 1.3.12-2
- spec file cleanup for better compliance with the guidelines

* Mon Aug 25 2008 Dan Horák <dan[at]danny.cz> 1.3.12-1
- update to mtx-1.3.12

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.11-3
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 1.3.11-2
- update License
- rebuild for BuildID

* Wed Mar 28 2007 Jindrich Novy <jnovy@redhat.com> 1.3.11-1
- update to 1.3.11 (adds new scsieject utility, bugfixes)
- sync nostrip patch

* Tue Feb 06 2007 Jindrich Novy <jnovy@redhat.com> 1.3.10-1
- update to mtx-1.3.10
- update URL, Source0
- don't strip debuginfo

* Tue Dec 12 2006 Jindrich Novy <jnovy@redhat.com> 1.2.18-9
- spec cleanup

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.18-8.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.18-8.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.18-8.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar  7 2005 Jindrich Novy <jnovy@redhat.com> 1.2.18-8
- fix type confusion in SCSI_writet(), SCSI_readt(), slow_memcopy()
  and slow_bzero()
- rebuilt with gcc4

* Thu Feb 10 2005 Jindrich Novy <jnovy@redhat.com> 1.2.18-7
- remove -D_FORTIFY_SOURCE=2 from CFLAGS, present in RPM_OPT_FLAGS

* Wed Feb  9 2005 Jindrich Novy <jnovy@redhat.com> 1.2.18-6
- rebuilt with -D_FORTIFY_SOURCE=2

* Wed Aug 11 2004 Jindrich Novy <jnovy@redhat.com> 1.2.18-5
- dead code elimination
- updated spec link to recent source
- removed spec link to obsolete URL
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 13 2004 Than Ngo <than@redhat.com> 1.2.18-2
- rebuild

* Fri Sep 26 2003 Harald Hoyer <harald@redhat.de> 1.2.18-1
- 1.2.18

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.2.16-6
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Than Ngo <than@redhat.com> 1.2.16-4
- don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 1.2.16-2
- rebuild

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.2.16-1
- 1.2.16

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 14 2001 Than Ngo <than@redhat.com> 1.2.15-1
- update to 1.2.15

* Mon Aug 13 2001 Preston Brown <pbrown@redhat.com> 1.2.13-1
- 1.2.13 fixes "+ Too many Data Transfer Elements Reported" problem (#49258)

* Mon Jun 25 2001 Preston Brown <pbrown@redhat.com>
- 1.2.12
- moved binaries to /usr/sbin from /sbin

* Wed Feb 14 2001 Michael Stefaniuc <mstefani@redhat.com>
- 1.2.10
- updated %%doc

* Mon Dec 11 2000 Preston Brown <pbrown@redhat.com>
- 1.2.9

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 15 2000 Preston Brown <pbrown@redhat.com>
- 1.2.7

* Tue May 23 2000 Preston Brown <pbrown@redhat.com> 
- adopted for Winston

* Fri May 12 2000 Kenneth Porter <shiva@well.com>
- 1.2.6
- Fixed 'eepos' stuff to use | rather than || (whoops!)
- Accept a 4-byte element descriptor for the robot arm for certain older
- autochangers. 

* Mon May 8 2000 Kenneth Porter <shiva@well.com>
- Spell sourceforge right so the link at rpmfind.net will work.

* Thu May 4 2000 Kenneth Porter <shiva@well.com>
- 1.2.5

* Thu Oct 29 1998  Ian Macdonald <ianmacd@xs4all.nl>
- moved mtx from /sbin to /bin, seeing as mt is also located there

* Fri Oct 23 1998  Ian Macdonald <ianmacd@xs4all.nl>
- first RPM release
