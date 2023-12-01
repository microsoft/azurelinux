%global pkgname xbitmaps
%global debug_package %{nil}
Summary:        X.Org X11 application bitmaps
Name:           xorg-x11-%{pkgname}
Version:        1.1.1
Release:        20%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.x.org
Source0:        https://xorg.freedesktop.org/archive/individual/data/%{pkgname}-%{version}.tar.bz2
BuildRequires:  automake
BuildRequires:  gcc
Requires:       pkg-config
BuildArch:      noarch

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
%license COPYING
%{_includedir}/X11
%{_datadir}/pkgconfig/xbitmaps.pc

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.1.1-20
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.1-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
