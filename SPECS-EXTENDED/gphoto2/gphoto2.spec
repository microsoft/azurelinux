Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           gphoto2
Version:        2.5.27
Release:        2%{?dist}
Summary:        Software for accessing digital cameras
License:        GPLv2+
Url:            https://www.gphoto.org/
Source0:        https://downloads.sourceforge.net/gphoto/%{name}-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libgphoto2) >= %{version}
BuildRequires:  libjpeg-devel
BuildRequires:  pkgconfig(libexif)
BuildRequires:  popt-devel
BuildRequires:  readline-devel

%description
The gPhoto2 project is a universal, free application and library
framework that lets you download images from several different
digital camera models, including the newer models with USB
connections. Note that
a) for some older camera models you must use the old "gphoto" package.
b) for USB mass storage models you must use the driver in the kernel

This package contains the command-line utility gphoto2.

Other (GUI) frontends are available separately.

%prep
%autosetup

%build
%configure
%make_build

%install
%make_install
rm %{buildroot}%{_docdir}/%{name}/test-hook.sh
%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc NEWS README TODO
%{_bindir}/gphoto2
%{_mandir}/man1/gphoto2.1*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.5.27-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Wed Mar 10 2021 Josef Ridky <jridky@redhat.com> - 2.5.27-1
- New upstream release 2.5.27 (#1931190)

* Wed Jan 27 2021 Josef Ridky <jridky@redhat.com> - 2.5.26-1
- New upstream release 2.5.26 (#1887196)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 21 2019 Josef Ridky <jridky@redhat.com> - 2.5.23-1
- Update to 2.5.23

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.20-3
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.20-1
- Update to 2.5.20

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Apr 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.17-1
- Update to 2.5.17

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 04 2017 Josef Ridky <jridky@redhat.com> - 2.5.15-1
- Update to 2.5.15

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.14-1
- Update to 2.5.14

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.5.11-2
- Rebuild for readline 7.x

* Mon Nov 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.5.11-1
- Update to 2.5.11

* Tue Jul 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.5.10-1
- update to 2.5.10
- Use %%license

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 20 2015 Peter Robinson <pbrobinson@fedoraproject.org> 2.5.6-1
- update to 2.5.6

* Sun Sep 07 2014 Jindrich Novy <novyjindrich@gmail.com> - 2.5.5-1
- update to 2.5.5

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Jon Disnard <jdisnard@gmail.com> - 2.5.3-1
- Bump to latest updtream version 2.5.3
- Add Source1 gpg2 signature to SRPM

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May  6 2013 Hans de Goede <hdegoede@redhat.com> - 2.5.2-1
- New upstream release 2.5.2

* Thu May  2 2013 Hans de Goede <hdegoede@redhat.com> - 2.5.1-1
- New upstream release 2.5.1
- This adds aarch64 support (rhbz#925472)
- Modernize spec-file

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.5.0-4
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.5.0-3
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Jindrich Novy <jnovy@redhat.com> 2.5.0-1
- update to 2.5.0

* Mon Apr 16 2012 Jindrich Novy <jnovy@redhat.com> 2.4.14-1
- update to 2.4.14

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Apr 18 2011 Jindrich Novy <jnovy@redhat.com> 2.4.11-1
- update to 2.4.11

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Dan Horák <dan[at]danny.cz> 2.4.10-2
- drop the s390(x) ExcludeArch

* Tue Aug 17 2010 Jindrich Novy <jnovy@redhat.com> 2.4.10-1
- update to 2.4.10

* Mon Apr 12 2010 Jindrich Novy <jnovy@redhat.com> 2.4.9-1
- update to 2.4.9

* Mon Jan 25 2010 Jindrich Novy <jnovy@redhat.com> 2.4.8-1
- update to 2.4.8

* Mon Aug 24 2009 Jindrich Novy <jnovy@redhat.com> 2.4.7-1
- update to 2.4.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 08 2009 Jindrich Novy <jnovy@redhat.com> 2.4.5-1
- update to 2.4.5

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Jindrich Novy <jnovy@redhat.com> 2.4.4-1
- update to 2.4.4

* Mon Oct 20 2008 Jindrich Novy <jnovy@redhat.com> 2.4.3-1
- update to 2.4.3

* Mon Aug 11 2008 Jindrich Novy <jnovy@redhat.com> 2.4.2-4
- convert ChangeLog to UTF-8

* Thu Aug  7 2008 Jindrich Novy <jnovy@redhat.com> 2.4.2-3
- another merge review fixes:
  - remove bogus Source0
  - remove useless BR: pkgconfig
  - update file attributes

* Sat Aug  2 2008 Jindrich Novy <jnovy@redhat.com> 2.4.2-2
- merge review fixes (#225855):
  - remove useless multilib_arches needed because of libgphoto2
  - fix source0 URL
  - fix description to not to mention the library is shipped
  - remove unused/pointless configure parameters
  - preserve timestamps
  - fix license
  - drop redundant BR libusb-devel, libexif-devel, lockdev-devel
  - add BR gettext
  - use %%{buildroot} exclusively

* Fri Aug  1 2008 Jindrich Novy <jnovy@redhat.com> 2.4.2-1
- update to 2.4.2
- introduces --capture-image and --capture-image-and-download

* Mon Jun  2 2008 Jindrich Novy <jnovy@redhat.com> 2.4.1-1
- update to 2.4.1 (#443515, #436138)
- remove libgphoto2, it's now packaged separately

* Tue Apr 22 2008 David Zeuthen <davidz@redhat.com> 2.4.0-9
- Rebuild

* Sat Apr 19 2008 David Zeuthen <davidz@redhat.com> 2.4.0-8
- Add a patch to fix build on ppc

* Thu Apr 17 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-7
- backport patch from upstream to avoid segfault when
  data phase is skipped for certain devices (#435413)

* Mon Feb 25 2008 Jindrich Novy <jnovy@redhat.com> 2.4.0-6
- fix gphoto2 build on alpha arch (#416941)
- manual rebuild because of gcc-4.3 (#434187)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.4.0-5
- Autorebuild for GCC 4.3

* Tue Nov 27 2007 Jindrich Novy <jnovy@redhat.com> 2.4.0-4
- fix permission problems while accessing camera (#400491)

* Tue Sep 18 2007 Jindrich Novy <jnovy@redhat.com> 2.4.0-3
- avoid tagging mass storage devices as cameras (#295051)
- add missing BR popt-devel

* Thu Aug 23 2007 Jindrich Novy <jnovy@redhat.com> 2.4.0-2
- update License
- rebuild for BuildID

* Tue Jul 31 2007 Jindrich Novy <jnovy@redhat.com> 2.4.0-1
- update gphoto2 and libgphoto2 to 2.4.0
- add missing libtool-ltdl-devel buildrequires
- package check-mtp-device

* Wed Feb 21 2007 Jindrich Novy <jnovy@redhat.com> 2.3.1-5
- include back the 10-camera-libgphoto2.fdi removed in
  the previous build (#229230)

* Mon Feb 19 2007 Jindrich Novy <jnovy@redhat.com> 2.3.1-4
- ACL handling is now moved into HAL (#229230)

* Thu Jan 18 2007 Jindrich Novy <jnovy@redhat.com> 2.3.1-3
- gphoto2-devel requires libusb-devel (#222015)

* Thu Jan 11 2007 Jindrich Novy <jnovy@redhat.com> 2.3.1-2
- really fix the gphoto2-devel multilib conflict (#205211)

* Mon Dec 25 2006 Jindrich Novy <jnovy@redhat.com> 2.3.1-1
- update to 2.3.1
- merry christmas!

* Mon Dec 11 2006 Jindrich Novy <jnovy@redhat.com> 2.3.0-2
- don't ship docs in separate tarball, use the internal one

* Tue Dec  5 2006 Jindrich Novy <jnovy@redhat.com> 2.3.0-1
- update to 2.3.0
- enable lockdev
- spec cleanup

* Fri Dec  1 2006 Jindrich Novy <jnovy@redhat.com> 2.2.0-4
- nuke useless PreReq and BuildRequires

* Fri Nov  3 2006 Jindrich Novy <jnovy@redhat.com> 2.2.0-3
- fix BuildRoot, use dist tag
- specify version of libgphoto2 in Provides

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.0-2.1
- rebuild

* Fri Jun 23 2006 Radek Vokál <rvokal@redhat.com> 2.2.0-2
- fix print-camera-list to not require libgphoto2 at build time

* Thu Jun 22 2006 Radek Vokál <rvokal@redhat.com> 2.2.0-1
- update to gphoto2-2.2.0 and libgphoto2-2.2.1

* Wed Jun  7 2006 Radek Vokál <rvokal@redhat.com> 2.1.99-14
- fix policy file (#189936)

* Mon May 29 2006 Radek Vokal <rvokal@redhat.com> 2.1.99-13
- remove Canon IXUS 700 support (#167347)
- add new USB ids

* Thu May 25 2006 Radek Vokal <rvokal@redhat.com> 2.1.99-12
- fix multilib -devel conflicts (#192678)

* Thu May 18 2006 Radek Vokál <rvokal@redhat.com> 2.1.99-11
- include docs on side, disable compiling them (bug in gtk-doc!?)

* Tue Apr 04 2006 Radek Vokál <rvokal@redhat.com> 2.1.99-10
- fix crash in ptp2 module

* Tue Mar 14 2006 Than Ngo <than@redhat.com> 2.1.99-9
- fix gphoto2-config

* Wed Mar 08 2006 Bill Nottingham <notting@redhat.com> 2.1.99-8
- fix i386/x86_64 conflict on fdi files

* Fri Mar 03 2006 Radek Vokál <rvokal@redhat.com> 2.1.99-7
- remove .la files (#183367) 

* Thu Mar 02 2006 Ray Strode <rstrode@redhat.com> 2.1.99-6
- potentially work around bug 183371 by looping/checking for
  5 seconds.

* Wed Mar 01 2006 Radek Vokál <rvokal@redhat.com> 2.1.99-5.4
- spec file tweak, become self-building again

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.99-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.99-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Bill Nottingham <notting@redhat.com> 2.1.99-5
- set permissions on /dev/bus/usb/XXX as well - that's what new
  libusb uses by default

* Mon Jan 23 2006 Radek Vokal <rvokal@redhat.com> 2.1.99-4
- fixed gphoto2 --summary segfault with Canon cameras (#178572)

* Fri Jan 13 2006 Radek Vokal <rvokal@redhat.com> 2.1.99-3
- export LIBDIR before creating .fdi file

* Fri Jan 13 2006 Radek Vokal <rvokal@redhat.com> 2.1.99-2
- spec file clean-up
- use ./print-usb-map 
- docs are back in -devel package

* Thu Jan 05 2006 Radek Vokal <rvokal@redhat.com> 2.1.99-1
- upgrade to 2.1.99 + dbus patch

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> 2.1.6-7.1
- rebuilt

* Sun Nov 13 2005 John (J5) Palmieri <johnp@redhat.com> 2.1.6-7
- Add callout to cameras with ptp access methods

* Fri Nov 11 2005 John (J5) Palmieri <johnp@redhat.com> 2.1.6-6
- Fix typo in fdi file to point to the correct script
- Install the fdi file to the policy directory instead of information

* Fri Nov 11 2005 John (J5) Palmieri <johnp@redhat.com> 2.1.6-5
- Fix to not install scripts as directories

* Fri Nov 11 2005 John (J5) Palmieri <johnp@redhat.com> 2.1.6-4
- Add gphoto-set-procperm and 90-gphoto-camera-policy.fdi to
  have HAL set permissions on the usb cameras
- Remove hotplug support since we don't use it anymore (udev takes care
  of devices and HAL takes care of permissions)

* Mon Nov 07 2005 Radek Vokal <rvokal@redhat.com> 2.1.6-3
- become self-hosting, don't depend on installed libs (#106442,#172519)

* Wed Jul 27 2005 Tim Waugh <twaugh@redhat.com> 2.1.6-2
- Rebuilt.

* Thu Jun 23 2005 Tim Waugh <twaugh@redhat.com> 2.1.6-1
- 2.1.6.

* Wed Jun  1 2005 Bill Nottingham <notting@redhat.com> 2.1.5-10
- fix multilib conflict on fdi files, and their generation on x86_64
  in general

* Sat May 14 2005 Tim Waugh <twaugh@redhat.com> 2.1.5-9
- Fixed buffer overrun in ricoh/g3 (bug #157739).

* Mon May  2 2005 David Zeuthen <davidz@redhat.com> 2.1.5-8
- Build and install hal device information files

* Tue Mar 29 2005 Tim Waugh <twaugh@redhat.com>
- Re-enable docs.

* Mon Mar 28 2005 Matthias Clasen <mclasen@redhat.com> 2.1.5-7
- Rebuild against newer libexif

* Thu Mar 24 2005 Warren Togami <wtogami@redhat.com>
- BR libtool, pkgconfig

* Thu Mar 24 2005 Tim Waugh <twaugh@redhat.com>
- Disable docs again until gtk-doc is fixed (GNOME bug #169087).

* Thu Mar 24 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 2.1.5-6
- Avoid creation of bad rpaths by removing libtool hacks from spec.

* Thu Mar 24 2005 Tim Waugh <twaugh@redhat.com>
- Disable docs again until gtk-doc is fixed (GNOME bug #169087).

* Mon Mar 21 2005 Tim Waugh <twaugh@redhat.com>
- Fixed memset() usage bug.

* Fri Mar 11 2005 Tim Waugh <twaugh@redhat.com>
- Re-enable docs.

* Fri Mar 11 2005 Tim Waugh <twaugh@redhat.com> 2.1.5-5
- Rebuild with GCC 4 fixes.
- Disable docs again until gtk-doc is fixed (GNOME bug #169087).

* Fri Mar  4 2005 Tim Waugh <twaugh@redhat.com>
- Re-enable docs.

* Fri Mar  4 2005 Tim Waugh <twaugh@redhat.com> 2.1.5-4
- Disable docs until gtk-doc is fixed (GNOME bug #169087).
- Rebuilt for new GCC.

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 2.1.5-3
- Rebuilt for new readline.

* Mon Jan 10 2005 Tim Waugh <twaugh@redhat.com> 2.1.5-2
- 2.1.5 (bug #143141).

* Fri Oct  8 2004 Tim Waugh <twaugh@redhat.com> 2.1.4-7
- devel sub-package requires libexif-devel (bug #135058).

* Tue Aug 31 2004 Tim Waugh <twaugh@redhat.com> 2.1.4-6
- Fixed mis-applied patch (bug #130755).

* Thu Aug 26 2004 Tim Waugh <twaugh@redhat.com> 2.1.4-5
- Apply patch from David Zeuthen to fix hotplug script (bug #130755).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 19 2004 Tim Waugh <twaugh@redhat.com> 2.1.4-3
- BuildRequires libjpeg-devel, readline-devel (bug #121238).

* Wed Mar 10 2004 Tim Waugh <twaugh@redhat.com>
- Apply Jeff Law's cast-as-lvalue patch.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Tim Waugh <twaugh@redhat.com> 2.1.4-1
- 2.1.4.

* Tue Dec 23 2003 Tim Waugh <twaugh@redhat.com> 2.1.3-3
- Build with libexif support.

* Thu Dec  4 2003 Tim Waugh <twaugh@redhat.com> 2.1.3-2
- Rebuilt.

* Wed Dec  3 2003 Tim Waugh <twaugh@redhat.com> 2.1.3-1
- 2.1.3.

* Tue Sep 16 2003 Tim Waugh <twaugh@redhat.com> 2.1.2-1
- 2.1.2.

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com> 2.1.1-4
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 2.1.1-2
- Ship print-usb-usermap, fix post scriptlet.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 2.1.1-1
- Use installed libtool.
- 2.1.1.

* Sat Feb 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- only package man3 in devel rpm

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sun Dec 01 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- remove some old mainframe ifdefs

* Tue Nov 19 2002 Tim Waugh <twaugh@redhat.com> 2.1.0-5
- Fix file lists.
- Don't install files not shipped.
- Rebuild in new environment.

* Wed Jul 24 2002 Tim Waugh <twaugh@redhat.com> 2.1.0-4
- Rebuild, just in case (readline).

* Thu Jul 18 2002 Tim Waugh <twaugh@redhat.com> 2.1.0-3
- Own some more directories.

* Fri Jun 28 2002 Tim Waugh <twaugh@redhat.com> 2.1.0-2
- Don't use -rpath (bug #65983).

* Tue Jun 25 2002 Tim Waugh <twaugh@redhat.com> 2.1.0-1
- 2.1.0.
- No longer need cvsfixes or consolelock patches.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.0-9
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com> 2.0-8
- automated rebuild

* Thu May  9 2002 Tim Waugh <twaugh@redhat.com> 2.0-7
- Require lockdev (bug #64193).

* Mon Apr 29 2002 Tim Waugh <twaugh@redhat.com> 2.0-6
- In fact, don't even build for mainframe.

* Mon Apr 29 2002 Florian La Roche <Florian.LaRoche@redhat.de> 2.0-5
- do not require hotplug for mainframe

* Mon Apr 15 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0-4
- Set the owner of the device to the console lock holder, not the owner
  of /dev/console, in the hotplug agent, fixing access for users who log
  in at VTs and use startx (#62976).

* Fri Apr 12 2002 Tim Waugh <twaugh@redhat.com> 2.0-3
- Rebuild (fixed bug #63355).

* Wed Feb 27 2002 Tim Waugh <twaugh@redhat.com> 2.0-2
- Fix from CVS: close port unconditionally in gp_camera_exit().

* Mon Feb 25 2002 Tim Waugh <twaugh@redhat.com> 2.0-1
- 2.0 is released.
- Ship the .so symlinks in the devel package.

* Mon Feb 25 2002 Tim Waugh <twaugh@redhat.com> 2.0-0.rc4.1
- 2.0rc4.

* Fri Feb 22 2002 Tim Waugh <twaugh@redhat.com> 2.0-0.rc3.1
- 2.0rc3.  No longer need CVS patch.
- Build no longer requires xmlto.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 2.0-0.rc2.2
- Fix DC240 hangs (patch from CVS).
- Rebuild in new environment.

* Tue Feb 19 2002 Tim Waugh <twaugh@redhat.com> 2.0-0.rc2.1
- 2.0rc2 (bug #59993).  No longer need docs patch or man page.
- Really fix up libtool libraries (bug #60002).

* Fri Feb 15 2002 Tim Waugh <twaugh@redhat.com> 2.0-0.beta5.2
- PreReq /sbin/ldconfig, grep, and fileutils (bug #59941).

* Tue Feb 12 2002 Tim Waugh <twaugh@redhat.com> 2.0-0.beta5.1
- 2.0beta5.
- Fix Makefiles so that documentation can be built.
- Ship pkgconfig file.
- Add man page.

* Thu Feb  7 2002 Tim Waugh <twaugh@redhat.com> 2.0-0.beta4.1
- 2.0beta4.
- Build requires transfig, and at least version 0.1.5 of libusb.
- Clean up file lists.
- Build documentation.

* Fri Jan 25 2002 Tim Waugh <twaugh@redhat.com> 2.0-0.beta3.2
- Rebuild in new environment.
- Dump docbook-dtd30-sgml requirement; gtk-doc is sufficient.

* Sun Nov 18 2001 Tim Waugh <twaugh@redhat.com> 2.0-0.beta3.1
- Adapted for Red Hat Linux.

* Sat Oct 27 2001 Hans Ulrich Niedermann <gp@n-dimensional.de>
- fixed update behaviour for hotplug list (do not erase it when updating)

* Thu Oct 25 2001 Tim Waugh <twaugh@redhat.com>
- hotplug dependency is a prereq not a requires (the package scripts
  need it).

* Sun Oct 14 2001 Hans Ulrich Niedermann <gp@n-dimensional.de>
- integrated spec file into source package

* Sun Oct 14 2001 Hans Ulrich Niedermann <gp@n-dimensional.de>
- 2.0beta3

* Tue Oct  2 2001 Tim Waugh <twaugh@redhat.com> 2.0beta2-0.1
- Adapted for Red Hat Linux.
- 2.0beta2.

* Mon Aug  6 2001 Till Kamppeter <till@mandrakesoft.com> 2.0-0.beta1.2mdk
- Corrected "Requires:"

* Mon Aug  6 2001 Till Kamppeter <till@mandrakesoft.com> 2.0-0.beta1.1mdk
- Initial release



