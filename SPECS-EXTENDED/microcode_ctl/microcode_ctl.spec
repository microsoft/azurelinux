%define upstream_version 2.1-29
%global debug_package %{nil}

Summary:        Tool to transform and deploy CPU microcode update for x86
Name:           microcode_ctl
Version:        2.1
Release:        41%{?dist}
License:        GPLv2+ and Redistributable, no modification permitted
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pagure.io/microcode_ctl
Source0:        https://releases.pagure.org/microcode_ctl/%{name}-%{upstream_version}.tar.xz
Patch0:         enable-wildcards-in-tar.patch
ExclusiveArch:  %{ix86} x86_64

%description
The microcode_ctl utility is a companion to the microcode driver written
by Tigran Aivazian <tigran@aivazian.fsnet.co.uk>.

The microcode update is volatile and needs to be uploaded on each system
boot i.e. it doesn't reflash your cpu permanently, reboot and it reverts
back to the old microcode.

%prep
%setup -q -n %{name}-%{upstream_version}
%patch0 -p1
# License not extracted from nested tar by Makefile- do it manually here
tar --no-anchored --strip-components=1 -xvf microcode*.tar.gz license

%build
make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} INSDIR=/usr/sbin install clean

%files
%license license
/lib/firmware/*
%doc /usr/share/doc/microcode_ctl/*


%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.1-41
- Remove epoch

* Wed Dec 16 2020 Ruying Chen <v-ruyche@microsoft.com> 2:2.1-40
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Enable wildcards for tar extraction

* Tue Jun 16 2020 Anton Arapov <aarapov@redhat.com> 2:2.1-39
- Update to upstream 2.1-29. 20200616

* Wed Jun 10 2020 Anton Arapov <aarapov@redhat.com> 2:2.1-38
- Update to upstream 2.1-28. 20200609

* Thu May 21 2020 Anton Arapov <aarapov@redhat.com> 2:2.1-37
- Update to upstream 2.1-27. 20200520

* Mon May 11 2020 Anton Arapov <aarapov@redhat.com> 2:2.1-36
- Update to upstream 2.1-26. 20200508

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-34
- Update to upstream 2.1-25. 20191115

* Tue Nov 12 2019 Justin Forbes <jforbes@fedoraproject.org> 2:2.1-33
- Update to microcode-20191112 for CVE fixes

* Wed Oct 02 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-32
- Update to upstream 2.1-23. 20190918

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 20 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-30
- Update to upstream 2.1-22. 20190618

* Wed May 15 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-29
- Update to upstream 2.1-21. 20190514

* Thu May 09 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-28
- Update to upstream 2.1-20. 20190312

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-26
- Update to upstream 2.1-19. 20180807

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-24
- Update to upstream 2.1-18. 20180703

* Wed May 16 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-23
- Update to upstream 2.1-17. 20180425

* Thu Mar 15 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-22
- Update to upstream 2.1-16. 20180312

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-20
- Update to upstream 2.1-15. 20180108

* Tue Nov 21 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-19
- Update to upstream 2.1-14. 20171117

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-16
- Update to upstream 2.1-13. 20170707

* Tue May 23 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-15
- Update to upstream 2.1-12. 20170511

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-14.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Anton Arapov <arapov@gmail.com> 2.1-13.1
- Update to upstream 2.1-11. 20161104

* Thu Jul 21 2016 Anton Arapov <arapov@gmail.com> 2.1-13
- Update to upstream 2.1-10. 20160714
- Fixes rhbz#1353103

* Fri Jun 24 2016 Anton Arapov <arapov@gmail.com> 2.1-12
- Update to upstream 2.1-9. 20160607

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Anton Arapov <arapov@gmail.com> 2.1-10
- Update to upstream 2.1-8. 20151106

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 03 2015 Anton Arapov <arapov@gmail.com> 2.1-8.1
- Update to upstream 2.1-7. 20150121

* Sun Sep 21 2014 Anton Arapov <arapov@gmail.com> 2.1-8
- Update to upstream 2.1-6. 20140913

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 08 2014 Anton Arapov <anton@descope.org> 2.1-6
- Update to upstream 2.1-5. 20140624

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Anton Arapov <anton@redhat.com> 2.1-4
- Update to upstream 2.1-4.

* Fri Jan 24 2014 Anton Arapov <anton@redhat.com> 2.1-3
- Update to upstream 2.1-3.

* Mon Sep 09 2013 Anton Arapov <anton@redhat.com> 2.1-2
- Update to upstream 2.1-2.

* Wed Aug 14 2013 Anton Arapov <anton@redhat.com> 2.1-1
- Update to upstream 2.1-1.

* Sat Jul 27 2013 Anton Arapov <anton@redhat.com> 2.1-0
- Update to upstream 2.1. AMD microcode has been removed, find it in linux-firmware.

* Wed Apr 03 2013 Anton Arapov <anton@redhat.com> 2.0-3.1
- Update to upstream 2.0-3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Anton Arapov <anton@redhat.com> 2.0-2
- Update to upstream 2.0-2

* Tue Oct 02 2012 Anton Arapov <anton@redhat.com> 2.0-1
- Update to upstream 2.0-1

* Mon Aug 06 2012 Anton Arapov <anton@redhat.com> 2.0
- Update to upstream 2.0

* Wed Jul 25 2012 Anton Arapov <anton@redhat.com> 1.18-1
- Update to upstream 1.18

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Anton Arapov <anton@redhat.com> 1.17-25
- Update to microcode-20120606.dat

* Tue Feb 07 2012 Anton Arapov <anton@redhat.com> 1.17-24
- Update to amd-ucode-2012-01-17.tar

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Anton Arapov <anton@redhat.com> 1.17-21
- Fix a segfault that may be triggered by very long parameter [#768803]

* Tue Dec 13 2011 Anton Arapov <anton@redhat.com> 1.17-20
- Update to microcode-20111110.dat

* Tue Sep 27 2011 Anton Arapov <anton@redhat.com> 1.17-19
- Update to microcode-20110915.dat

* Thu Aug 04 2011 Anton Arapov <anton@redhat.com> 1.17-18
- Ship splitted microcode for Intel CPUs [#690930]
- Include tool for splitting microcode for Intl CPUs (Kay Sievers )

* Thu Jun 30 2011 Anton Arapov <anton@redhat.com> 1.17-17
- Fix udev rules (Dave Jones ) [#690930]

* Thu May 12 2011 Anton Arapov <anton@redhat.com> 1.17-14
- Update to microcode-20110428.dat

* Thu Mar 24 2011 Anton Arapov <anton@redhat.com> 1.17-13
- fix memory leak.

* Mon Mar 07 2011 Anton Arapov <anton@redhat.com> 1.17-12
- Update to amd-ucode-2011-01-11.tar

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Anton Arapov <anton@redhat.com> 1.17-10
- manpage fix (John Bradshaw ) [#670879]

* Wed Jan 05 2011 Anton Arapov <anton@redhat.com> 1.17-9
- Update to microcode-20101123.dat

* Mon Nov 01 2010 Anton Arapov <anton@redhat.com> 1.17-8
- Update to microcode-20100914.dat

* Wed Sep 29 2010 jkeating - 1:1.17-7
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Anton Arapov <anton@redhat.com> 1.17-6
- Update to microcode-20100826.dat

* Tue Sep 07 2010 Toshio Kuratomi <toshio@fedoraproject.org> 1.17-5
- Fix license tag: bz#450491

* Fri Aug 27 2010 Dave Jones <davej@redhat.com> 1.17-4
- Update to microcode-20100826.dat

* Tue Mar 23 2010 Anton Arapov <anton@redhat.com> 1.17-3
- Fix the udev rules (Harald Hoyer )

* Mon Mar 22 2010 Anton Arapov <anton@redhat.com> 1.17-2
- Make microcode_ctl event driven (Bill Nottingham ) [#479898]

* Thu Feb 11 2010 Dave Jones <davej@redhat.com> 1.17-1.58
- Update to microcode-20100209.dat

* Fri Dec 04 2009 Kyle McMartin <kyle@redhat.com> 1.17-1.57
- Fix duplicate message pointed out by Edward Sheldrake.

* Wed Dec 02 2009 Kyle McMartin <kyle@redhat.com> 1.17-1.56
- Add AMD x86/x86-64 microcode. (Dated: 2009-10-09)
  Doesn't need microcode_ctl modifications as it's loaded by
  request_firmware() like any other sensible driver.
- Eventually, this AMD firmware can probably live inside
  kernel-firmware once it is split out.

* Wed Sep 30 2009 Dave Jones <davej@redhat.com>
- Update to microcode-20090927.dat

* Fri Sep 11 2009 Dave Jones <davej@redhat.com>
- Remove some unnecessary code from the init script.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-1.52.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009 Dave Jones <davej@redhat.com>
- Shorten sleep time during init.
  This really needs to be replaced with proper udev hooks, but this is
  a quick interim fix.

* Wed Jun 03 2009 Kyle McMartin <kyle@redhat.com> 1:1.17-1.50
- Change ExclusiveArch to i586 instead of i386. Resolves rhbz#497711.

* Wed May 13 2009 Dave Jones <davej@redhat.com>
- update to microcode 20090330

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-1.46.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Dave Jones <davej@redhat.com>
- update to microcode 20080910

* Tue Apr 01 2008 Jarod Wilson <jwilson@redhat.com>
- Update to microcode 20080401

* Sat Mar 29 2008 Dave Jones <davej@redhat.com>
- Update to microcode 20080220
- Fix rpmlint warnings in specfile.

* Mon Mar 17 2008 Dave Jones <davej@redhat.com>
- specfile cleanups.

* Fri Feb 22 2008 Jarod Wilson <jwilson@redhat.com>
- Use /lib/firmware instead of /etc/firmware

* Wed Feb 13 2008 Jarod Wilson <jwilson@redhat.com>
- Fix permissions on microcode.dat

* Thu Feb 07 2008 Jarod Wilson <jwilson@redhat.com>
- Spec cleanup and macro standardization.
- Update license
- Update microcode data file to 20080131 revision.

* Mon Jul  2 2007 Dave Jones <davej@redhat.com>
- Update to upstream 1.17

* Thu Oct 12 2006 Jon Masters <jcm@redhat.com>
- BZ209455 fixes.

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Fri Jun 16 2006 Bill Nottingham <notting@redhat.com>
- remove kudzu requirement
- add prereq for coreutils, awk, grep

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Jan 27 2006 Dave Jones <davej@redhat.com>
- Update to upstream 1.13

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Dave Jones <davej@redhat.com>
- initscript tweaks.

* Tue Sep 13 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.12

* Wed Aug 17 2005 Dave Jones <davej@redhat.com>
- Check for device node *after* loading the module. (#157672)

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Thu Feb 17 2005 Dave Jones <davej@redhat.com>
- s/Serial/Epoch/

* Tue Jan 25 2005 Dave Jones <davej@redhat.com>
- Drop the node creation/deletion change from previous release.
  It'll cause grief with selinux, and was a hack to get around
  a udev shortcoming that should be fixed properly.

* Fri Jan 21 2005 Dave Jones <davej@redhat.com>
- Create/remove the /dev/cpu/microcode dev node as needed.
- Use correct path again for the microcode.dat.
- Remove some no longer needed tests in the init script.

* Fri Jan 14 2005 Dave Jones <davej@redhat.com>
- Only enable microcode_ctl service if the CPU is capable.
- Prevent microcode_ctl getting restarted multiple times on initlevel change (#141581)
- Make restart/reload work properly
- Do nothing if not started by root.

* Wed Jan 12 2005 Dave Jones <davej@redhat.com>
- Adjust dev node location. (#144963)

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Load/Remove microcode module in initscript.

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.11 release.

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based upon kernel-utils.

