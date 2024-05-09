Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        Library providing low-level IEEE-1394 access - 2.1.2-
Name:           libraw1394
Version:        2.1.2
Release:        12%{?dist}
License:        LGPLv2+
Source:         https://www.kernel.org/pub/linux/libs/ieee1394/%{name}-%{version}.tar.xz
URL:            https://git.kernel.org/pub/scm/libs/ieee1394/libraw1394.git/about
ExcludeArch:    s390 s390x
BuildRequires:  gcc
BuildRequires:  kernel-headers

%description
The libraw1394 library provides direct access to the IEEE-1394 bus.
Support for both the obsolete ieee1394 interface and the new firewire
intererface are included, with run-time detection of the active stack.

%package devel
Summary:        Development libs for libraw1394
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development libraries needed to build applications against libraw1394.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/libraw1394.la

%ldconfig_scriptlets

%files
%license COPYING.LIB
%doc README NEWS
%{_bindir}/dumpiso
%{_bindir}/sendiso
%{_bindir}/testlibraw
%{_libdir}/libraw1394.so.*
%{_mandir}/man1/dumpiso.1*
%{_mandir}/man1/sendiso.1*
%{_mandir}/man1/testlibraw.1*
%{_mandir}/man5/isodump.5*

%files devel
%doc doc/libraw1394.sgml
%{_includedir}/libraw1394/
%{_libdir}/libraw1394.so
%{_libdir}/pkgconfig/libraw1394.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.2-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 26 2018 Owen Taylor <otaylor@redhat.com> - 2.1.2-8
- Handle both compressed and uncompressed man pages

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Nils Philippsen <nils@tiptoe.de> - 2.1.2-6
- require gcc for building

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 27 2016 Nils Philippsen <nils@tiptoe.de> - 2.1.2-1
- fix bogus changelog date

* Wed Oct 26 2016 Nils Philippsen <nils@tiptoe.de> - 2.1.2-1
- version 2.1.2
- tidy up spec file
- use %%license for license file
- require same arch main from devel package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.1.0-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Feb 25 2013 Jay Fenlason <fenlason@redhat.com> 2.1.0-1
- New upstream vesion.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 6 2012 Jay Fenlason <fenlason@redhat.com> 2.0.8-2
- Clean up description (#800438)

* Mon Feb 20 2012 Jay Fenlason <fenlason@redhat.com> 2.0.8-1
- New upstream release (#795374)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 04 2011 Jarod Wilson <jarod@redhat.com> 2.0.7-1
- New upstream release (#683413)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Jay Fenlason <fenlason@redhat.com> 2.0.6-1
- Upgrade to new upstream, which obsoletes the HUP patch.

* Mon Apr 19 2010 Jarod Wilson <jarod@redhat.com> 2.0.5-2
- Fix overlooked device HUP using firewire driver stack

* Thu Jan 7 2010 Jay Fenlason <fenlason@redhat.com> 2.0.5-1
- New upstream version

* Thu Sep 17 2009 Jarod Wilson <jarod@redhat.com> - 2.0.4-1
- Update to libraw1394 v2.0.4 release
- Point to new download location and project page

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Jarod Wilson <jarod@redhat.com> - 2.0.1-1
- Update to libraw1394 v2.0.1 release

* Tue Jan 13 2009 Jarod Wilson <jarod@redhat.com> - 2.0.0-6
- Set errno = ENOSYS for all unimplemented functions
- Make dvgrab and friends work w/o requiring r/w on the local fw node (#441073)

* Mon Dec 08 2008 Jarod Wilson <jarod@redhat.com> - 2.0.0-5
- Fix up iso stop command so starting/stopping/starting iso reception works
- Plug firewire handle leak

* Fri Dec 05 2008 Jarod Wilson <jarod@redhat.com> - 2.0.0-4
- Fix channel modify code, should make iso reception work reliably now

* Thu Nov 20 2008 Jarod Wilson <jarod@redhat.com> - 2.0.0-3
- Address some compiler warnings
- Reduce nesting depth in new_handle dispatches
- Fix segfault in handle_arm_request

* Wed Oct 01 2008 Jarod Wilson <jarod@redhat.com> - 2.0.0-2
- Misc fixes from Erik Hovland, based on coverity prevent analysis

* Fri Jul 18 2008 Jarod Wilson <jwilson@redhat.com> - 2.0.0-1
- Update to libraw1394 v2.0.0 release

* Mon Jun 23 2008 Jarod Wilson <jwilson@redhat.com> - 2.0.0-0.2.20080430_git
- Restore ieee1394 raw1394_read_cycle_timer, add firewire variant

* Tue Jun 17 2008 Jarod Wilson <jwilson@redhat.com> - 2.0.0-0.1.20080430_git
- Update to pre-2.0.0 git tree, which features merged "juju" firewire
  stack support, enabled simultaneously with classic ieee1394 support

* Tue Jun 17 2008 Jarod Wilson <jwilson@redhat.com> - 1.3.0-7
- Fully initialize data structures and plug dir leak. Resolves
  crashes when used with kino (Philippe Troin, #451727)

* Mon Apr 28 2008 Jarod Wilson <jwilson@redhat.com> - 1.3.0-6
- Unmap the correct memory range on iso receive teardown, fixes
  segfault on exit from dvgrab (Mladen Kuntner, #444354)

* Tue Feb 26 2008 Jarod Wilson <jwilson@redhat.com> - 1.3.0-5
- Update license and kill an errant tab (#226039)

* Wed Jan 30 2008 Jarod Wilson <jwilson@redhat.com> - 1.3.0-4
- Use firewire-cdev.h provided by kernel-headers

* Wed Oct 24 2007 Jarod Wilson <jwilson@redhat.com> - 1.3.0-3
- Update firewire-cdev.h to match kernel and eliminate
  bitfield usage, fixes capture on big-endian systems (#345221)

* Fri Oct 19 2007 Jarod Wilson <jwilson@redhat.com> - 1.3.0-2
- Fix the 'double free' crash on shutdown (#328011)

* Thu Oct 18 2007 Jarod Wilson <jwilson@redhat.com> - 1.3.0-1
- libraw1394 v1.3.0

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.1-10
- Rebuild for selinux ppc32 issue.

* Fri Jun 15 2007 Jarod Wilson <jwilson@redhat.com> - 1.2.1-9
- Drop Conficts, causes interesting issues if people have an
  older kernel installed and/or kernel-xen installed (#244474)

* Thu Jun 14 2007 Jarod Wilson <jwilson@redhat.com> - 1.2.1-8
- Switch kernel Requires to a Conflicts so we don't end up pulling
  kernels into build chroot, and bump to GA kernel ver (#244128)

* Wed Apr 18 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.1-7
- Update firewire-cdev.h again to get the iso context create ioctl changes.
- Bump kernel requires accordingly.

* Tue Apr 17 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.1-6
- Update to latest ioctl changes.

* Thu Apr 12 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.1-5
- Make rawiso support actually work.
- Update fw-device-cdev.h to sync with latest kernel patch.
- Add Requires to pull in a recent enough kernel.

* Tue Apr  3 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.1-4
- Update juju patch with rawiso support.

* Mon Mar 19 2007 Kristian Høgsberg <krh@redhat.com> 1.2.1-3
- Add support for new stack (juju).

* Sun Feb 04 2007 Jarod Wilson <jwilson@redhat.com> - 1.2.1-2
- Minor spec cleanups for Core/Extras merger (#226039)

* Wed Jul 12 2006 Jarod Wilson <jwilson@redhat.com> - 1.2.1-1
- update to 1.2.1
- use %%dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.fc5.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.fc5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.fc5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005 Warren Togami <wtogami@redhat.com> - 1.2.0-3
- disable static and remove .la (#172642)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Warren Togami <wtogami@redhat.com> - 1.2.0-2
- spec fixes from Matthias (#172105)

* Fri Jul 22 2005 Warren Togami <wtogami@redhat.com> - 1.2.0-1
- 1.2.0

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Warren Togami <wtogami@redhat.com. 1.1.0-2
- gcc4 rebuild

* Sun Feb 06 2005 Warren Togami <wtogami@redhat.com> 1.1.0-1
- 1.1.0

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 0.10.1-3
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 05 2004 Warren Togami <wtogami@redhat.com> 0.10.1-1
- 0.10.1, license LGPL

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks to shared libs already at install time

* Thu Feb 12 2004 Warren Togami <wtogami@redhat.com> 0.10.0-1
- upgrade to 0.10.0
- Spec cleanups
- Remove INSTALL, add NEWS
- Add new binaries
- libtool, auto* not needed

* Mon Aug 25 2003 Bill Nottingham <notting@redhat.com> 0.9.0-12
- have -devel require main pacakge

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 0.9.0-10
- fix build with gcc 3.3

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com>
- ppc64 fix

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude mainframe
- allow lib64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Michael Fulbright <msf@redhat.com>
- fixed up %%files list for devel subpackage and included api docs

* Sun Jun 09 2002 Michael Fulbright <msf@redhat.com>
- First RPM build

