%global tarball xf86-video-dummy
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/drivers
	
%undefine _hardened_build
	
Summary:   Xorg X11 dummy video driver	
Name:      xorg-x11-drv-dummy	
Version:   0.4.1
Release:   3%{?dist}
URL:       http://www.x.org
License:   MIT AND X11
		
Source0:   https://www.x.org/archive/individual/driver/%{tarball}-%{version}.tar.xz
 
BuildRequires: make
BuildRequires: xorg-x11-server-devel >= 1.10.99.902
BuildRequires: autoconf automake libtool
	
Requires: Xorg %(xserver-sdk-abi-requires ansic)
Requires: Xorg %(xserver-sdk-abi-requires videodrv)
	
%description 
X.Org X11 dummy video driver.
	
%prep
%setup -q -n %{tarball}-%{version}
autoreconf -vif
 
%build	
%configure --disable-static
%make_build
	
%install
%make_install
	
# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --
 
%files	
%doc README.md
%{driverdir}/dummy_drv.so
	
%changelog
* Thu May 2 2024 Alberto David Perez Guevara <aperezguevar@microsoft.com> - 0.4.1-3
- Initial CBL-Mariner import from Fedora (license: MIT).
 
* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Thu Oct 05 2023 José Expósito <jexposit@redhat.com> - 0.4.1-1
- xorg-x11-drv-dummy 0.4.1
 
* Thu Sep 07 2023 José Expósito <jexposit@redhat.com> - 0.3.7-20
- SPDX Migration
 
* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
	
* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
	
* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Thu Nov  5 09:50:45 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.7-13
- Add BuildRequires for make
 
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Mon Apr 02 2018 Adam Jackson <ajax@redhat.com> - 0.3.7-7
- Rebuild for xserver 1.20
 
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild
	
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
	
* Thu May  4 2017 Orion Poplawski <orion@cora.nwra.com> - 0.3.7-3
- Build for s390x (bug #1447533)
 
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Wed Nov  9 2016 Hans de Goede <hdegoede@redhat.com> - 0.3.7-1
- New upstream release 0.7.3
- Fix undefined symbol error with xserver-1.19 (rhbz#1393114)
 
* Thu Sep 29 2016 Hans de Goede <hdegoede@redhat.com> - 0.3.6-26
- Rebuild against xserver-1.19
	
* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
	
* Thu Jan 28 2016 Peter Hutterer <peter.hutterer@redhat.com>
- Remove unnecessary defattr
	
* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/
 
* Wed Jul 29 2015 Dave Airlie <airlied@redhat.com> - 0.3.6-24
- 1.15 ABI rebuild
 
* Tue Jun 23 2015 Adam Jackson <ajax@redhat.com> - 0.3.6-23
- Undefine _hardened_build
 
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
	
* Wed Feb 11 2015 Hans de Goede <hdegoede@redhat.com> - 0.3.6-21
- xserver 1.17 ABI rebuild
	
* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild
 
* Mon Jun 16 2014 Hans de Goede <hdegoede@redhat.com> - 0.3.6-19
- xserver 1.15.99.903 ABI rebuild
	
* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
	
* Mon Apr 28 2014 Hans de Goede <hdegoede@redhat.com> - 0.3.6-17
- xserver 1.15.99-20140428 git snapshot ABI rebuild
	
* Mon Jan 13 2014 Adam Jackson <ajax@redhat.com> - 0.3.6-16
- 1.15 ABI rebuild
	
* Tue Dec 17 2013 Adam Jackson <ajax@redhat.com> - 0.3.6-15
- 1.15RC4 ABI rebuild
	
* Wed Nov 20 2013 Adam Jackson <ajax@redhat.com> - 0.3.6-14
- 1.15RC2 ABI rebuild
	
* Wed Nov 06 2013 Adam Jackson <ajax@redhat.com> - 0.3.6-13
- 1.15RC1 ABI rebuild
	
* Fri Oct 25 2013 Adam Jackson <ajax@redhat.com> - 0.3.6-12
- ABI rebuild
	
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
	
* Tue Mar 19 2013 Adam Jackson <ajax@redhat.com> 0.3.6-10
- Less RHEL customization
 
* Thu Mar 07 2013 Dave Airlie <airlied@redhat.com> 0.3.6-9
- autoreconf for aarch64
	
* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.6-8
- require xorg-x11-server-devel, not -sdk
	
* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.6-7
- ABI rebuild
	
* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.6-6
- ABI rebuild
 
* Fri Feb 15 2013 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.6-5
- ABI rebuild
 
* Thu Jan 10 2013 Adam Jackson <ajax@redhat.com> - 0.3.6-3
- ABI rebuild
	
* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
	
* Wed Jul 18 2012 Dave Airlie <airlied@redhat.com> 0.3.6-1
- dummy 0.3.6
	
* Thu Apr 05 2012 Adam Jackson <ajax@redhat.com> - 0.3.5-5
- RHEL arch exclude updates
 
* Sat Feb 11 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.5-4
- ABI rebuild
	
* Fri Feb 10 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.5-3
- ABI rebuild
	
* Tue Jan 24 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.5-2
- ABI rebuild
	
* Mon Jan 16 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.3.5-1
- dummy 0.3.5
	
* Wed Jan 04 2012 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.4-11
- Rebuild for server 1.12
	
* Fri Dec 16 2011 Adam Jackson <ajax@redhat.com> - 0.3.4-10
- Drop xinf file
	
* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> - 0.3.4-9
- ABI rebuild
	
* Wed Nov 09 2011 ajax <ajax@redhat.com> - 0.3.4-8
- ABI rebuild
	
* Thu Aug 18 2011 Adam Jackson <ajax@redhat.com> - 0.3.4-7
- Rebuild for xserver 1.11 ABI
	
* Wed May 11 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.4-6
- Rebuild for server 1.11
	
* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.4-5
- Rebuild for server 1.10
	
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
	
* Thu Dec 02 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.4-3
- Rebuild for server 1.10
 
* Wed Oct 27 2010 Adam Jackson <ajax@redhat.com> 0.3.4-2
- Add ABI requires magic. (#542742)
 
* Mon Jul 05 2010 Dave Airlie <airlied@redhat.com> 0.3.4-1
- update to latest dummy release for 1.9
	
* Mon Jul 05 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.3-3
- rebuild for X Server 1.9
	
* Thu Jan 21 2010 Peter Hutterer <peter.hutterer@redhat.com> - 0.3.3-2
- Rebuild for server 1.8
	
* Tue Dec 01 2009 Adam Jackson <ajax@redhat.com> 0.3.3-1
- dummy 0.3.3
	
* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
	
* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 0.3.2-1.1
- ABI bump
	
* Thu Jul 02 2009 Adam Jackson <ajax@redhat.com> 0.3.2-1
- dummy 0.3.2
	
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
	
* Tue Feb 24 2009 Adam Jackson <ajax@redhat.com> 0.3.1-1
- dummy 0.3.1
 
* Thu Mar 20 2008 Dave Airlie <airlied@redhat.com> 0.3.0-1
- Latest upstream release
 
* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.0-8
- Autorebuild for GCC 4.3
 
* Wed Jan 09 2008 Adam Jackson <ajax@redhat.com> 0.2.0-7
- Rebuild for new server ABI.
 
* Tue Nov 13 2007 Adam Jackson <ajax@redhat.com> 0.2.0-6
- Require xserver 1.4.99.1
 
* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 0.2.0-5
- Rebuild for PPC toolchain bug
	
* Mon Jun 18 2007 Adam Jackson <ajax@redhat.com> 0.2.0-4
- Update Requires and BuildRequires.  Disown the module directories.  Add
  Requires: hwdata.
	
* Fri Feb 16 2007 Adam Jackson <ajax@redhat.com> 0.2.0-3
- ExclusiveArch -> ExcludeArch
	
* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild
 
* Tue May 23 2006 Adam Jackson <ajackson@redhat.com> 0.2.0-2
- Rebuild for 7.1 ABI fix.
	
* Sun Apr  9 2006 Adam Jackson <ajackson@redhat.com> 0.2.0-1
- Update to 0.2.0 from 7.1RC1.
	
* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.1.0.5-1.2
- bump again for double-long bug on ppc(64)
 
* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.1.0.5-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes
	
* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 0.1.0.5-1
- Updated xorg-x11-drv-dummy to version 0.1.0.5 from X11R7.0
	
* Tue Dec 20 2005 Mike A. Harris <mharris@redhat.com> 0.1.0.4-1
- Updated xorg-x11-drv-dummy to version 0.1.0.4 from X11R7 RC4
- Removed 'x' suffix from manpage dirs to match RC4 upstream.
	
* Wed Nov 16 2005 Mike A. Harris <mharris@redhat.com> 0.1.0.2-1
- Updated xorg-x11-drv-dummy to version 0.1.0.2 from X11R7 RC2
	
* Fri Nov 4 2005 Mike A. Harris <mharris@redhat.com> 0.1.0.1-1
- Updated xorg-x11-drv-dummy to version 0.1.0.1 from X11R7 RC1
- Fix *.la file removal.
 
* Mon Oct 3 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update BuildRoot to use Fedora Packaging Guidelines.
- Deglob file manifest.
- Add alpha/sparc/sparc64 to "ExclusiveArch"
	
* Fri Sep 2 2005 Mike A. Harris <mharris@redhat.com> 0.1.0-0
- Initial spec file for dummy video driver generated automatically
  by my xorg-driverspecgen script.
