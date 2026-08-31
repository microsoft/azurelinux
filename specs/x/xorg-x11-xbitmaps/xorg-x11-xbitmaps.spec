# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname xbitmaps

%global debug_package %{nil}

Summary: X.Org X11 application bitmaps
Name: xorg-x11-%{pkgname}
Version: 1.1.3
Release: 5%{?dist}
License: HPND AND ICU
URL: http://www.x.org
BuildArch: noarch

Source0: https://www.x.org/pub/individual/data/xbitmaps-%{version}.tar.xz

BuildRequires: make
BuildRequires: automake gcc
Requires: pkgconfig

%description
X.Org X11 application bitmaps

%prep
%setup -q -n xbitmaps-%{version}

%build
%configure
%make_build

%install
%make_install

%files
%doc COPYING
%{_includedir}/X11
%{_datadir}/pkgconfig/xbitmaps.pc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 05 2023 José Expósito <jexposit@redhat.com> - 1.1.3-1
- xorg-x11-xbitmaps 1.1.3

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com> - 1.1.2-5
- SPDX Migration

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.2-1
- xbitmaps 1.1.2
- Use make macros, see
  https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 11:00:41 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.1-20
- Add BuildRequires for make

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.1.1-14
- Add BR for gcc

* Mon Feb 19 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.1.1-13
- Add BR for automake

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Peter Hutterer <peter.hutterer@redhat.com>
- Remove unnecessary defattr

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 02 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.1.1-2
- Requires pkgconfig

* Tue Jun 21 2011 Adam Jackson <ajax@redhat.com> 1.1.1-1
- xbitmaps 1.1.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.1.0-3
- Own the /usr/include/X11 as discussed on packaging list.

* Mon Aug 30 2010 Adam Jackson <ajax@redhat.com> 1.1.0-2
- Merge review cleanups (#226649)

* Tue Oct 13 2009 Adam Jackson <ajax@redhat.com> 1.1.0-1
- xbitmaps 1.1.0
- BuildArch: noarch

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.1-8
- Un-require xorg-x11-filesystem

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.1-6
- Fix license tag.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.1-5.1
- Autorebuild for GCC 4.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-4
- Bump release and rebuild for FC6.

* Thu Mar 02 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Made package arch specific due to pkgconfig files being placed in lib64
  if the noarch packages manage to get built on x86_64/ppc64/s390x.

* Wed Mar 01 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Cleaned up file manifest.
- Made package noarch, as it is just header files.
- Disable debuginfo processing, as there are no ELF objects in package.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated to xbitmaps 1.0.1 from X11R7.0

* Sat Dec 17 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated to xbitmaps 1.0.0 from X11R7 RC4.

* Wed Nov 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-4
- Updated dep to "Requires(pre): xorg-x11-filesystem >= 0.99.2-3" for new fix.
- Moved bitmap files back into the upstream default of _includedir (#173665).

* Mon Nov 21 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-1" to attempt to
  workaround bug( #173384).

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-2
- Clean up specfile.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated to xbitmaps 0.99.1 from X11R7 RC2

* Fri Aug 26 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
