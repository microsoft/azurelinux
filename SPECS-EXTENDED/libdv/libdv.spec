Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary:        Software decoder for DV format video
Name:           libdv
Version:        1.0.0
Release:        32%{?dist}
License:        LGPLv2+
URL:            http://libdv.sourceforge.net/
Source:         http://downloads.sourceforge.net/libdv/libdv-%{version}.tar.gz
Patch1:         libdv-0.104-no-exec-stack.patch
Patch2:         libdv-1.0.0-pic.patch
Patch3:         libdv-1.0.0-gtk2.patch
Patch4:         libdv-1.0.0-dso-linking.patch

BuildRequires:  gtk2-devel
BuildRequires:  libXt-devel
BuildRequires:  libXv-devel
BuildRequires:  popt-devel
BuildRequires:  SDL-devel
BuildRequires:  autoconf, automake, libtool

%description
The Quasar DV codec (libdv) is a software codec for DV video, the
encoding format used by most digital camcorders, typically those that
support the IEEE 1394 (a.k.a. FireWire or i.Link) interface. libdv was
developed according to the official standards for DV video: IEC 61834
and SMPTE 314M.

%package tools
Summary:        Basic tools to manipulate Digital Video streams
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
This package contains some basic programs to display and encode
digital video streams. This programs uses the Quasar DV codec (libdv),
a software codec for DV video, the encoding format used by most
digital camcorders, typically those that support the IEEE 1394
(a.k.a. FireWire or i.Link) interface.

%package devel
Summary:        Development package for libdv
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       pkgconfig

%description devel
This package contains development files for libdv.

%prep
%setup -q
%patch1 -p0 -b .no-exec-stack
%patch2 -p1 -b .pic
%patch3 -p1 -b .gtk2
%patch4 -p1 -b .dso-linking
# Required for libtool 2.2
libtoolize
# Required for the gtk2 patch
autoreconf -vif

%build
%configure --with-pic
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/libdv.a
rm $RPM_BUILD_ROOT%{_libdir}/libdv.la

%ldconfig_scriptlets

%files
%doc ChangeLog
%license COPYING COPYRIGHT
%{_libdir}/libdv.so.*

%files tools
%doc README.* AUTHORS
%{_bindir}/dubdv
%{_bindir}/dvconnect
%{_bindir}/encodedv
%{_bindir}/playdv
%{_mandir}/man1/dubdv.1*
%{_mandir}/man1/dvconnect.1*
%{_mandir}/man1/encodedv.1*
%{_mandir}/man1/playdv.1*

%files devel
%{_includedir}/libdv/
%{_libdir}/libdv.so
%{_libdir}/pkgconfig/libdv.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.0-32
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Feb 17 2018 Antonio Trande <sagitter@fedoraproject.org> - 1.0.0-27
- Use %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 01 2016 Antonio Trande <sagitter@fedoraproject.org> 1.0.0-22
- Rebuild for new branches
- Use %%license tag

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.0-17
- Fix FTBFS and cleanup spec

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.0.0-12
- Rebuild for new libpng

* Thu May 05 2011 Dan Horák <dan[at]danny.cz> - 1.0.0-11
- don't exclude s390(x)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Jay Fenlason <fenlason@redhat.com> 1.0.0-9
- Add dso-linking patch to explicitly pull in the X libraries that
  playdv depends on.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 03 2009 Robert Scheck <robert@fedoraproject.org> 1.0.0-7
- Rebuilt against libtool 2.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.0.0-5
- fix conditional comparison

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> 1.0.0-4
- Bump and rebuild with gcc 4.3

* Wed Sep 12 2007 Jarod Wilson <jwilson@redhat.com> 1.0.0-3
- A few more fixes from Matthias Saou:
 - List man pages in %%files consistently w/o gz extension
 - Add BR: popt-devel for f8+, its now split fromm rpm-devel

* Wed Sep 12 2007 Jarod Wilson <jwilson@redhat.com> 1.0.0-2
- Update License field (Matthias Saou)
- Remove useless zero epoch (Matthias Saou)
- Add pkgconfig devel sub-package req (Matthias Saou)
- Minor spec formatting changes and clean-ups

* Fri Jan 19 2007 Jarod Wilson <jwilson@redhat.com> 1.0.0-1
- New upstream release
- PIC patch from Mike Frysinger <vapier@gentoo.org> (#146596)
- Re-enable asm on i386

* Thu Sep 21 2006 Jarod Wilson <jwilson@redhat.com> 0.104-5
- Disable asm on i386 for now to prevent text relocations in DSO

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:0.104-4.fc6.1
- rebuild

* Wed May 24 2006 Jarod Wilson <jwilson@redhat.com> 0.104-4
- disable PIC patch for now, it reliably causes segfaults on x86

* Sat May 13 2006 Jarod Wilson <jwilson@redhat.com> 0.104-3
- rebuilt against latest X libs

* Tue Mar 07 2006 Warren Togami <wtogami@redhat.com> 0.104-2
- remove instead of exclude static libs

* Wed Feb 15 2006 Matthias Saou <http://freshrpms.net/> 0.104-1
- Update to 0.104 at last (#147311)
- Include no-exec-stack, pic-fix, amd64reloc and gtk2 patches from Gentoo
  and PLD (merge gcc4 fix to the pic-fix patch).
- Now build against gtk2 (thanks to the patch above).
- Exclude static library.

* Mon Feb 13 2006 Paul Nasrat <pnasrat@redhat.com> - 0:0.103-4.3
- Patch to build with gcc 4.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:0.103-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:0.103-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Warren Togami <wtogami@redhat.com> - 0:0.103-3
- gcc4 rebuild

* Sun Feb 06 2005 Warren Togami <wtogami@redhat.com> - 0:0.103-2
- Fix erroneously requiring an executable stack (Nicholas Miell #146590)

* Sun Sep 19 2004 Warren Togami <wtogami@redhat.com> - 0:0.103-1
- upgrade to 0.103

* Sun Jun 20 2004 Jeremy Katz <katzj@redhat.com> - 0:0.102-4
- gtk+ doesn't need to be in the .pc file (committed upstream, reported
- don't require gtk+-devel for -devel package (unneeded)
  to fedora-devel-list by John Thacker)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun May 30 2004 Warren Togami <wtogami@redhat.com> 0:0.102-2
- Bug #123367 -devel Req gtk+-devel

* Mon Mar 29 2004 Warren Togami <wtogami@redhat.com> 0:0.102-1
- update to 0.102

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 14 2004 Warren Togami <wtogami@redhat.com> 0:0.101-2
- upgrade to 0.101
- spec cleanup
- exclude from mainframes
- GPL -> LGPL

* Sun Apr 27 2003 Dams <anvil[AT]livna.org> 0:0.99-0.fdr.2
- Added post/postun scriptlets

* Fri Apr 25 2003 Dams <anvil[AT]livna.org>
- Initial build.


