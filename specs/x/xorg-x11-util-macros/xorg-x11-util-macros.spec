# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pkgname util-macros
%global debug_package %{nil}

Summary: X.Org X11 Autotools macros
Name: xorg-x11-util-macros
Version: 1.20.2
Release: 4%{?dist}
License: HPND-sell-variant AND MIT
URL: http://www.x.org
BuildArch: noarch
Source0:  https://www.x.org/pub/individual/util/util-macros-%{version}.tar.xz

BuildRequires: make

Requires: autoconf automake pkgconfig

%description
X.Org X11 autotools macros required for building the various packages that
comprise the X Window System.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%doc COPYING ChangeLog
%{_datadir}/aclocal/xorg-macros.m4
%{_datadir}/pkgconfig/xorg-macros.pc
%{_datadir}/util-macros

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 14 2024 Dr. Tilmann Bubeck <bubeck@fedoraproject.org> - 1.20.2-1
- update to util-macros 1.20.2

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 17 2024 Dr. Tilmann Bubeck <bubeck@fedoraproject.org> - 1.20.1-1
- update to util-macros 1.20.1

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 07 2023 José Expósito <jexposit@redhat.com> - 1.20.0-3
- SPDX Migration

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 14 2023 Dr. Tilmann Bubeck <bubeck@fedoraproject.org> - 1.20.0-1
- update to util-macros 1.20.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 17:55:38 CET 2021 Dr. Tilmann Bubeck <bubeck@fedoraproject.org> - 1.19.3-1
- Update to util-macros 1.19.3

* Thu Nov  5 10:40:38 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.19.2-9
- Add BuildRequires for make

* Thu Nov  5 10:40:38 AEST 2020 Peter Hutterer <peter.hutterer@redhat.com> - 1.19.2-8
- Add BuildRequires for make

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 01 2018 Adam Jackson <ajax@redhat.com> - 1.19.2-2
- HTTPS URLs

* Mon Mar 05 2018 Dr. Tilmann Bubeck <tilmann@bubecks.de> - 1.19.2-1
- util-macros 1.19.2

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Peter Hutterer <peter.hutterer@redhat.com>
- Remove unnecessary defattr

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jul 05 2014 Dr. Tilmann Bubeck <tilmann@bubecks.de> - 1.19.0-3
- Include missing INSTALL (bz #1083749)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Peter Hutterer <peter.hutterer@redhat.com> 1.19.0-1
- util-macros 1.19.0

* Wed Dec 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.18.0-1
- util-macros 1.18.0

* Mon Sep 09 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.17.1-1
- util-macros 1.17.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.17-1
- util-macros 1.17

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.16.2-1
- util-macros 1.16.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.16.0-1
- util-macros 1.16

* Tue Jul 05 2011 Adam Jackson <ajax@redhat.com> 1.15.0-1
- util-macros 1.15

* Mon May 30 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.14.0-1
- util-macros 1.14

* Tue Mar 15 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.13.0-1
- util-macros 1.13

* Mon Feb 28 2011 Peter Hutterer <peter.hutterer@redhat.com> 1.12.0-1
- util-macros 1.12

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.11.0-2
- util-macros 1.11

* Tue Jul 20 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.10.0-2
- Spec file cleanup. Patch from Parag An. (#226646)

* Mon Jun 28 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.10.0-1
- util-macros 1.10.0

* Thu Jun 24 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.9.0-1
- util-macros 1.9.0

* Tue Jun 01 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.8.0-1
- util-macros 1.8.0

* Tue May 18 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.6.0-1
- util-macros 1.6.0

* Thu Feb 04 2010 Dave Airlie <airlied@redhat.com> 1.5.0-1
- util-macros 1.5.0

* Mon Dec 14 2009 Adam Jackson <ajax@redhat.com> 1.4.1-1
- util-macros 1.4.1

* Thu Sep 10 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.3.0-1
- util-macros 1.3.0

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.2.2-1
- util-macros 1.2.2

* Tue Apr 21 2009 Adam Jackson <ajax@redhat.com> 1.2.1-3
- Add Requires: for the things you inevitably require if you need this
  package.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 17 2008 Adam Jackson <ajax@redhat.com> 1.2.1-1
- util-macros 1.2.1
- BuildArch: noarch

* Mon Aug 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.1.6-2
- Fix license tag.

* Wed Mar 05 2008 Adam Jackson <ajax@redhat.com> 1.1.6-1
- Update to 1.1.6

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.5-2
- Autorebuild for GCC 4.3

* Fri Jan 05 2007 Adam Jackson <ajax@redhat.com> 1.1.5-1
- Update to 1.1.5

* Fri Dec 1 2006 Adam Jackson <ajax@redhat.com> 1.1.3-1
- Update to 1.1.3

* Thu Oct 12 2006 Adam Jackson <ajackson@redhat.com> 1.1.1-1.fc6
- Update to upstream 1.1.1.

* Sat Jul 15 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-4.fc6
- Make dist tag usage a conditional (#198988)

* Thu Jul 13 2006 Kristian Høgsberg <krh@redhat.com> 1.0.2-3
- Bump for rawhide build.

* Thu Jul 13 2006 Kristian Høgsberg <krh@redhat.com> 1.0.2-2.fc5.aiglx
- Tag as 1.0.2-2.fc5.aiglx

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.2-1.1
- rebuild

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-1
- Update to util-macros-1.0.2 from X11R7.1
- Added COPYING, ChangeLog to file manifest.
- Use "make install" instead of makeinstall macro.
- Use setup -n instead of setup -c

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 23 2005 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Update to util-macros-1.0.1 from X11R7.

* Thu Dec 15 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Update to util-macros-1.0.0 from the X11R7 RC4 release.

* Tue Dec 06 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Update to util-macros-0.99.2 from the X11R7 RC3 release.

* Wed Oct 19 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Update to util-macros-0.99.1 from the X11R7 RC1 release.
- Disable debuginfo package creation, as there are no ELF objects present.
- Add xorg-macros.m4 to file list.

* Wed Jul 13 2005 Mike A. Harris <mharris@redhat.com> 0.0.1-1
- Initial build
