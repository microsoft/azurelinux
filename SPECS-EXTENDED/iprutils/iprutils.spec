Summary: Utilities for the IBM Power Linux RAID adapters
Name:    iprutils
Version: 2.4.17.1
Release: 5%{?dist}
License: CPL
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:     https://sourceforge.net/projects/iprdd/
Source0: https://sourceforge.net/projects/iprdd/files/iprutils%20for%202.6%20kernels/2.4.17/%{name}-%{version}.tar.gz

# missing man page
Source1: iprdbg.8.gz

BuildRequires: libtool
BuildRequires: ncurses-devel
BuildRequires: libcap-devel
BuildRequires: kernel-headers
BuildRequires: systemd
BuildRequires: zlib-devel


%description
Provides a suite of utilities to manage and configure SCSI devices
supported by the ipr SCSI storage device driver.


%prep
%autosetup -p1

autoreconf -vif


%build
%configure --with-systemd --without-initscripts --disable-static --disable-sosreport
%{make_build}


%install
%{make_install}

# missing man page
install -p -m 0644 %SOURCE1 %{buildroot}%{_mandir}/man8/

#install bash completion
mv %{buildroot}/%{_sysconfdir}/bash_completion.d/{iprconfig-bash-completion.sh,iprconfig}

# Remove temporary files and scripts that will not be packaged.
rm %{buildroot}/%{_sysconfdir}/ha.d/resource.d/iprha


%post
%systemd_post iprinit.service
%systemd_post iprdump.service
%systemd_post iprupdate.service
%systemd_post iprutils.target

%preun
%systemd_preun iprinit.service
%systemd_preun iprdump.service
%systemd_preun iprupdate.service
%systemd_preun iprutils.target

%files
%license LICENSE
%doc README
%{_sbindir}/*
%{_sysconfdir}/bash_completion.d/
%{_mandir}/man*/*
%{_unitdir}/iprinit.service
%{_unitdir}/iprdump.service
%{_unitdir}/iprupdate.service
%{_unitdir}/iprutils.target
%{_udevrulesdir}/90-iprutils.rules


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.17.1-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.17.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Than Ngo <than@redhat.com> - 2.4.17.1-2
- add tests

* Mon Mar 04 2019 Than Ngo <than@redhat.com> - 2.4.17.1-1
- update to 2.4.17.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.16.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 14 2018 Dan Horák <dan[at]danny.cz> - 2.4.16.1-2
- use better patch for udev activation

* Fri May 11 2018 Dan Horák <dan[at]danny.cz> - 2.4.16.1-1
- rebased to 2.4.16.1
- spec file cleanup

* Thu Mar 15 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.4.15.1-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Merlin Mathesius <mmathesi@redhat.com> - 2.4.15.1-2
- Not building kernel modules, so use kernel-headers instead of kernel-devel

* Fri Oct 13 2017 Sinny Kumari <sinnykunmari@fedoraproject.org> - 2.4.15.1-1
- Rebase to 2.4.15.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 05 2017 Sinny Kumari <sinnykunmari@fedoraproject.org> - 2.4.14.1-1
- Rebase to 2.4.14.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 10 2016 Sinny Kumari <sinnykumari@fedoraproject.org> - 2.4.12.1-1
- Rebase to 2.4.12.1

* Mon Apr 11 2016 Sinny Kumari <sinnykumari@fedoraproject.org> - 2.4.11.1-1
- Update to 2.4.11.1
- Add zlib-devel as BuildRequires

* Sat Feb 27 2016 Jakub Čajka <jcajka@redhat.com> - 2.4.10.1-1
- rebase to 2.4.10.1
- Resolves: #1289145 - iprutils-2.4.9 package update in Fedora

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 10 2015 Gabriel Krisman Bertazi <krisman@linux.vnet.ibm.com> - 2.4.8-1
- Rebase to 2.4.8
- Move to Autotools
- Remove unused files
- Rebase patch 0001 to use autotools
- Install bash completion
- Spec file clean up

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Nov 19 2014 Jakub Čajka <jcajka@redhat.com> - 2.4.5-1
- Rebase to 2.4.5

* Wed Oct 1 2014 Jakub Čajka <jcajka@redhat.com> - 2.4.4-1
- Rebase to 2.4.4
- Moved to systemd
- Spec file clean up
- Fixed build flags

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Dec 29 2012 Peter Robinson <pbrobinson@fedoraproject.org> 2.3.13-1
- update to 2.3.13

* Tue Sep 11 2012 David Aquilina <dwa@redhat.com> 2.3.11-2
- Prevent the RPM from conflicting with itself (BZ #856330)

* Wed Sep 05 2012 Karsten Hopp <karsten@redhat.com> 2.3.11-1
- update to 2.3.11
- enable on all archs as it now supports some adapters on them, too.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 08 2012 Karsten Hopp <karsten@redhat.com> 2.3.10-1
- update to iprutils-2.3.10

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Jiri Skala <jskala@redhat.com> - 2.3.9-1
- Update to version 2.3.9

* Wed Aug 24 2011 Jiri Skala <jskala@redhat.com> - 2.3.7-1
- Update to version 2.3.7

* Fri Aug 05 2011 Jiri Skala <jskala@redhat.com> - 2.3.6-1
- Update to version 2.3.6

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 09 2011 Jiri Skala <jskala@redhat.com> - 2.3.2-1
- Update to version 2.3.2

* Mon Apr 12 2010 Roman Rakus <rrakus@redhat.com> - 2.2.20-1
- Update to version 2.2.20

* Thu Feb 11 2010 Roman Rakus <rrakus@redhat.com> 2.2.18-3
- added missing man page

* Tue Jan 26 2010 Roman Rakus <rrakus@redhat.com> 2.2.18-2
- moved files from /sbin to /usr/sbin and made symlinks

* Wed Nov 04 2009 Roman Rakus <rrakus@redhat.com> - 2.2.18-1
- Version 2.2.18

* Mon Oct 05 2009 Roman Rakus <rrakus@redhat.com> - 2.2.17-2
- Fixed initscripts (#522464, #522462, #522461)

* Thu Sep 17 2009 Roman Rakus <rrakus@redhat.com> - 2.2.17-1
- Version 2.2.17

* Mon Aug 17 2009 Roman Rakus <rrakus@redhat.com> - 2.2.16-1
- Bump to version 2.2.16

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 2 2009 Will Woods <wwoods@redhat.com> - 2.2.13-2
- Fix iprdump startup - #483340
- iprutils-swab-moved.patch - fix compilation with 2.6.29 kernels (#483643)

* Fri Nov 21 2008 Roman Rakus <rrakus@redhat.com> - 2.2.13-1
- New upstream version

* Wed Jul  2 2008 Roman Rakus <rrakus@redhat.com> - 2.2.8-6
- Fixed ExclusiveArch tag

* Wed Jul  2 2008 Roman Rakus <rrakus@redhat.com> - 2.2.8-5
- Fixed chkconfig issue - #453165

* Wed Apr  9 2008 Roman Rakus <rrakus@redhat.cz> - 2.2.8-4
- Rewrited initscripts for satisfying LSB spec

* Fri Feb 08 2008 David Cantrell <dcantrell@redhat.com> - 2.2.8-2
- Rebuild for gcc-4.3

* Fri Nov 16 2007 David Cantrell <dcantrell@redhat.com> - 2.2.8-1
- Upgrade to latest upstream release

* Mon Oct  1 2007 Jeremy Katz <katzj@redhat.com> - 2.2.6-3
- don't require redhat-lsb (#252343)

* Tue Aug 21 2007 David Cantrell <dcantrell@redhat.com> - 2.2.6-2
- Rebuild

* Thu May 17 2007 Paul Nasrat <pnasrat@redhat.com> - 2.2.6-1
- Update to latest upstream

* Thu Jul 13 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.5-1
- New upstream version

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.1.4-3.1
- rebuild

* Mon Jul 10 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.4-3
- Add redhat-lsb requires

* Mon Jul 10 2006 David Woodhouse <dwmw2@redhat.com> - 2.1.4-2
- Rebuild against new sysfsutils

* Mon Jun 26 2006 Paul Nasrat <pnasrat@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 23 2005 Paul Nasrat <pnasrat@redhat.com> - 2.1.1-1
- Update to 2.1.1
- Use RPM_OPT_FLAGS

* Tue Aug 02 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.15.3-1
- update to 2.0.15.3-1

* Wed May 11 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.14.2-1
- update to 2.0.14.2 (#156934)

* Thu Feb 24 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.13.7-1
- Update to 2.0.13.7 (#144654)
- Project moved location to sourceforge

* Mon Jan 03 2005 Paul Nasrat <pnasrat@redhat.com> - 2.0.13.5-1
- Update to 2.0.13.5 (#143593)

* Wed Dec  8 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.4-2
- link dynamically to sysfsutils instead of statically (#142310)

* Wed Dec 08 2004 Paul Nasrat <pnasrat@redhat.com> 2.0.13.4-1
- update to 2.0.13.4 (#142164)

* Fri Dec  3 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.3-1
- update to 2.0.13.3 (#141707)

* Mon Nov 15 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13.2-1
- update to 2.0.13.2 (#139083)
  - fix firmware upload for firmware in /lib instead of /usr/lib
  - fix sysfs race

* Wed Oct  6 2004 Jeremy Katz <katzj@redhat.com> - 2.0.13-1
- update to 2.0.13 (#128996)

* Tue Aug  3 2004 Jeremy Katz <katzj@redhat.com> - 2.0.12-1
- update to 2.0.12
- include a copy of libsysfs to build

* Tue Jun 15 2004 Jeremy Katz <katzj@redhat.com> - 1.0.7-1
- update to 1.0.7 (#125988)

* Tue May 11 2004 Jeremy Katz <katzj@redhat.com> - 1.0.5-3
- obsolete ipr-utils (old package name)

* Thu Mar 25 2004 Jeremy Katz <katzj@redhat.com> 1.0.5-2
- 1.0.5
- some spec file tweaks

* Tue Nov 25 2003 Brian King <brking@us.ibm.com> 1.0.3-2
- Fixed segmentation fault in iprupdate
