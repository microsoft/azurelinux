Summary:        Library implementing the Unicode Bidirectional Algorithm
Name:           fribidi
Version:        1.0.12
Release:        1%{?dist}
License:        LGPLv2+ AND UCD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/fribidi/fribidi/
Source:         https://github.com/%{name}/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Patch0:         %{name}-drop-bundled-gnulib.patch
BuildRequires:  gcc
BuildRequires:  meson

%description
A library to handle bidirectional scripts (for example Hebrew, Arabic),
so that the display is done in the proper way; while the text data itself
is always written in logical order.

%package devel
Summary:        Libraries and include files for FriBidi
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Include files and libraries needed for developing applications which use
FriBidi.

%prep
%autosetup -p1

%build
%meson -Ddocs=false
%meson_build

%check
%meson_test

%install
%meson_install
find %{buildroot} -type f -name "*.la" -delete -print

%ldconfig_scriptlets

%files
%doc README AUTHORS ChangeLog THANKS NEWS TODO
%license COPYING
%{_bindir}/fribidi
%{_libdir}/libfribidi.so.0*

%files devel
%{_includedir}/fribidi
%{_libdir}/libfribidi.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Sep 19 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.12-1
- Upgrade to 1.0.12

* Tue Feb 08 2022 Minghe Ren <mingheren@microsoft.com> - 1.0.10-1
- Update to Version 1.0.10

* Thu Apr 15 2021 Henry Li <lihl@microsoft.com> - 1.0.9-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove distro check that does not apply to CBL-Mariner.
- License verified.

* Thu Mar 05 2020 Akira TAGOH <tagoh@redhat.com> - 1.0.9-1
- New upstream release.
  Resolves: rhbz#1809478

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Akira TAGOH <tagoh@redhat.com> - 1.0.8-2
- Restore the deprecated API that was accidentally removed in the previous release.
  Resolves: rhbz#1787293

* Fri Dec 13 2019 Akira TAGOH <tagoh@redhat.com> - 1.0.8-1
- New upstream release.
  Resolves: rhbz#1783205

* Wed Dec 11 2019 Akira TAGOH <tagoh@redhat.com> - 1.0.7-2
- Fix CVE-2019-18397
  Resolves: rhbz#1781218

* Mon Sep 30 2019 Akira TAGOH <tagoh@redhat.com> - 1.0.7-1
- New upstream release.
  Resolves: rhbz#1756434

* Fri Sep 27 2019 Akira TAGOH <tagoh@redhat.com> - 1.0.6-1
- New upstream release.
  Resolves: rhbz#1756212
- Use meson to build.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Akira TAGOH <tagoh@redhat.com> - 1.0.5-3
- Backport upstream patch to remove HAVE_CONFIG_H from public API.
  Fixes rhbz#1730516

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 06 2018 Akira TAGOH <tagoh@redhat.com> - 1.0.5-1
- New upstream release. (#1609080)

* Thu Jul 26 2018 Akira TAGOH <tagoh@redhat.com> - 1.0.4-6
- Drop bundled gnulib code.

* Tue Jul 17 2018 Akira TAGOH <tagoh@redhat.com> - 1.0.4-5
- Add BR: gcc.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Akira TAGOH <tagoh@redhat.com> - 1.0.4-3
- Modernize spec file.

* Fri Jun 29 2018 Akira TAGOH <tagoh@redhat.com> - 1.0.4-2
- Use ldconfig rpm macro.

* Fri Jun 08 2018 Akira TAGOH <tagoh@redhat.com> - 1.0.4-1
- New upstream release. (#1587985)

* Thu May 31 2018 Akira TAGOH <tagoh@redhat.com> - 1.0.3-1
- New upstream release. (#1584541)

* Fri May 04 2018 Caolán McNamara <caolanm@redhat.com> - 1.0.2-1
- Resolves: rhbz#1574858 latest version, --disable-docs because there's no c2man

* Wed Feb 28 2018 Caolán McNamara <caolanm@redhat.com> - 1.0.1-1
- Resolves: rhbz#1549934 latest version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 16 2017 Caolán McNamara <caolanm@redhat.com> - 0.19.7-6
- Resolves: rhbz#1502675 enable make check

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 11 2015 Caolán McNamara <caolanm@redhat.com> - 0.19.7-1
- Resolves: rhbz#1250755 latest fribidi

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.19.6-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 13 2014 Caolán McNamara <caolanm@redhat.com> - 0.19.6-1
- Resolves: rhbz#1052148 latest fribidi
- drop integrated signedwarning.patch
- drop integrated fribidi-aarch64.patch

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 03 2013 Caolán McNamara <caolanm@redhat.com> - 0.19.4-4
- Resolves: rhbz#925368 support aarch64

* Mon Feb 18 2013 Caolán McNamara <caolanm@redhat.com> - 0.19.4-3
- Resolves: rhbz#884000 remove empty man pages

* Mon Dec 10 2012 Caolán McNamara <caolanm@redhat.com> - 0.19.4-2
- Resolves: rhbz#884000 signed warning (thanks mfabian)

* Tue Nov 27 2012 Caolán McNamara <caolanm@redhat.com> - 0.19.4-1
- Resolves: rhbz#880490 bump to latest version

* Tue Oct 16 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.19.2-6
- spec cleanup for changed packaging guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 26 2009 Behdad Esfahbod <besfahbo@redhat.com> 0.19.2-1
- Update to 0.19.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.19.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 12 2009 Caolán McNamara <caolanm@redhat.com> - 0.19.1-3
- rebuild to get provides pkgconfig(fribidi)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.19.1-2
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Caolan McNamara <caolanm@redhat.com> 0.19.1-1
- next version
- workaround PAGE_SIZE requirement

* Wed Aug 29 2007 Caolan McNamara <caolanm@redhat.com> 0.10.9-2
- rebuild

* Fri Aug 10 2007 Caolan McNamara <caolanm@redhat.com> 0.10.9-1
- next version

* Thu Aug 02 2007 Caolan McNamara <caolanm@redhat.com> 0.10.8-2
- clarify license

* Thu May 31 2007 Caolan McNamara <caolanm@redhat.com> 0.10.8-1
- next version

* Mon Feb 05 2007 Caolan McNamara <caolanm@redhat.com> 0.10.7-6
- Resolves: rhbz#225771 spec cleanups

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.10.7-5.1
- rebuild

* Thu Jun 29 2006 Caolan McNamara <caolanm@redhat.com> 0.10.7-5
- rh#197223# devel Require pkg-config

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 0.10.7-4
- put devel .so symlink in the right subpackage

* Tue May 23 2006 Caolan McNamara <caolanm@redhat.com> 0.10.7-3
- rh#192669# clearly I didn't actually get around to basing fribidi-config 
  of pkg-config output

* Tue May 02 2006 Caolan McNamara <caolanm@redhat.com> 0.10.7-2
- base fribidi-config on pkg-config output
- allow fribidi_config.h to be the same on 32 and 64 bit

* Mon Mar 27 2006 Caolan McNamara <caolanm@redhat.com> 0.10.7-1
- latest version

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.10.4-8.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.10.4-8.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar  2 2005 Caolan McNamara <caolanm@redhat.com> 0.10.4-8
- rebuild with gcc4

* Wed Feb 09 2005 Caolan McNamara <caolanm@redhat.com> 0.10.4-7
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Sep 24 2003 Jeremy Katz <katzj@redhat.com> 0.10.4-4
- update description
- include docs (#104964)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add ldconfig to post/postun

* Fri May 16 2003 Jeremy Katz <katzj@redhat.com> 0.10.4-2
- Initial build in Red Hat Linux
