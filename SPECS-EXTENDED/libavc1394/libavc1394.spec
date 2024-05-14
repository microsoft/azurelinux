Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:        Audio/Video Control library for IEEE-1394 devices
Name:           libavc1394
Version:        0.5.4
Release:        13%{?dist}
License:        GPLv2+ and LGPLv2+
URL:            https://sourceforge.net/projects/libavc1394/
Source:         https://sourceforge.net/projects/libavc1394/files/libavc1394/libavc1394-%{version}.tar.gz
Patch1:         libavc1394-%{version}-librom.patch
BuildRequires:  libraw1394-devel
BuildRequires:  chrpath, gcc

# libraw1394 is not built on s390*
ExcludeArch:    s390 s390x

%description
The libavc1394 library allows utilities to control IEEE-1394 devices
using the AV/C specification.  Audio/Video Control allows applications
to control devices like the tape on a VCR or camcorder.

%package devel
Summary: Development libs for libavc1394

Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libraw1394-devel, pkgconfig

%description devel
Development libraries required to build applications using libavc1394.

%prep
%setup -q
%patch 1 -p1 -b .librom
chmod -x test/dvcont.c

%build
%configure
%make_build

%install
%make_install
# sigh, --disable-static doesn't work
rm -f $RPM_BUILD_ROOT%{_libdir}/*.{la,a}

chrpath -d $RPM_BUILD_ROOT%{_libdir}/lib*
chrpath -d $RPM_BUILD_ROOT%{_bindir}/*

%ldconfig_scriptlets

%files
%doc AUTHORS NEWS README ChangeLog TODO
%license COPYING
# binaries are GPLv2+
%{_bindir}/dvcont
%{_bindir}/mkrfc2734
%{_bindir}/panelctl
%{_mandir}/man1/dvcont.1.gz
%{_mandir}/man1/panelctl.1.gz
%{_mandir}/man1/mkrfc2734.1*
# libs are LGPLv2+
%{_libdir}/libavc1394.so.*
%{_libdir}/librom1394.so.*

%files devel
%{_includedir}/libavc1394/
%{_libdir}/pkgconfig/libavc1394.pc
%{_libdir}/libavc1394.so
%{_libdir}/librom1394.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.4-13
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Antonio Trande <sagitterATfedoraproject.org> - 0.5.4-8
- Add gcc BR

* Fri Feb 16 2018 Antonio Trande <sagitter@fedoraproject.org> - 0.5.4-7
- Use %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 21 2016 Antonio Trande <sagitter@fedoraproject.org> - 0.5.4-2
- Some minor fixes

* Sat Aug 20 2016 Antonio Trande <sagitter@fedoraproject.org> - 0.5.4-1
- Update to 0.5.4 (bz#628157)
- Patch updated
- Use %%license

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.5.3-17
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Jarod Wilson <jarod@redhat.com> 0.5.3-8
- Fix duplicate global symbols in libavc1394 vs. librom1394 (#216143)

* Mon May 18 2009 Jarod Wilson <jarod@redhat.com> 0.5.3-7
- Use included libtool, kill rpath a different way (#225988)

* Mon May 18 2009 Jarod Wilson <jarod@redhat.com> 0.5.3-6
- Fix up merge review issues (#225988)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.5.3-4
- fix license tag

* Tue Jul 22 2008 Jarod Wilson <jwilson@redhat.com> 0.5.3-3
- Bump and rebuild for libraw1394 v2.0.0

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> - 0.5.3-2
- Bump and rebuild with gcc 4.3

* Sun Sep 10 2006 Jarod Wilson <jwilson@redhat.com> - 0.5.3-1
- Upstream release 0.5.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-2.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.5.1-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Dec 22 2005 Warren Togami <wtogami@redhat.com> 0.5.1-2
- remove .a and .la (#172641)
- GPL -> LGPL (#165908)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Matthias Saou <https://freshrpms.net/> 0.5.1-1
- Update to 0.5.1.
- Update librom patch to still apply cleanly.

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- make sure librom1394 is linked to libraw1394 and also
  libavc1394 is linked to librom1394 (also bz 156938)

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Warren Togami <wtogami@redhat.com> 0.4.1-7
- gcc4 rebuild

* Sun Feb 06 2005 Warren Togami <wtogami@redhat.com> 0.4.1-6
- rebuild against new libraw1394

* Mon Jan 03 2005 Colin Walters <walters@redhat.com> 0.4.1-5
- Rerun autotools in attempt to get package to link to -lm
- Add patch libavc1394-0.4.1-kill-configure-insanity.patch

* Mon Nov 22 2004 Karsten Hopp <karsten@redhat.de> 0.4.1-4 
- remove bogus ldconfig after makeinstall

* Fri Jul 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks for ldconfig

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 12 2004 Warren Togami <wtogami@redhat.com> 0.4.1-1
- upgrade to 0.4.1
- Spec cleanups
- License -> Copyright
- Remove INSTALL; Add News, ChangeLog
- Applications/Multimedia -> System Environment/Libraries

* Mon Aug 25 2003 Bill Nottingham <notting@redhat.com> 0.3.1-7
- fix buildreqs (#102204)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 0.3.1-4
- rebuild on all arches

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude mainframe
- allow lib64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 09 2002 Michael Fulbright <msf@redhat.com>
- First RPM build

