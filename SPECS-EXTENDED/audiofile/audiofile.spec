Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Summary: Library for accessing various audio file formats
Name: audiofile
Version: 0.3.6
Release: 27%{?dist}
# library is LGPL / the two programs GPL / see README
License: LGPLv2+ and GPLv2+
Source: https://audiofile.68k.org/%{name}-%{version}.tar.gz
URL: https://audiofile.68k.org/
BuildRequires:  gcc-c++
BuildRequires: libtool
BuildRequires: alsa-lib-devel
BuildRequires: flac-devel
# optional for rebuilding manual pages from .txt
#BuildRequires: asciidoc

Patch0: audiofile-0.3.6-CVE-2015-7747.patch
# fixes to make build with GCC 6
Patch1: audiofile-0.3.6-left-shift-neg.patch
Patch2: audiofile-0.3.6-narrowing.patch
# pull requests #42,#43,#44
Patch3: audiofile-0.3.6-pull42.patch
Patch4: audiofile-0.3.6-pull43.patch
Patch5: audiofile-0.3.6-pull44.patch
Patch6: 822b732fd31ffcb78f6920001e9b1fbd815fa712.patch
Patch7: 941774c8c0e79007196d7f1e7afdc97689f869b3.patch
Patch8: fde6d79fb8363c4a329a184ef0b107156602b225.patch

%description
The Audio File library is an implementation of the Audio File Library
from SGI, which provides an API for accessing audio file formats like
AIFF/AIFF-C, WAVE, and NeXT/Sun .snd/.au files. This library is used
by the EsounD daemon.

Install audiofile if you are installing EsounD or you need an API for
any of the sound file formats it can handle.

%package devel
Summary: Development files for Audio File applications
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The audiofile-devel package contains libraries, include files, and
other resources you can use to develop Audio File applications.

%prep
%setup -q
%patch 0 -p1 -b .CVE-2015-7747
%patch 1 -p1 -b .left-shift-neg
%patch 2 -p1 -b .narrowing-conversion
%patch 3 -p1 -b .pull42
%patch 4 -p1 -b .pull43
%patch 5 -p1 -b .pull44
%patch 6 -p1 -b .CVE-2018-17095
%patch 7 -p1 -b .CVE-2018-13440
%patch 8 -p1 -b .CVE-2018-13440


%build
%configure
%make_build

%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

# Disable check temporarily
# BUG(@mfrw): [41224018]
# The check section produces a ~35Gb log file which breaks Ptest pipeline
%check
#make check


%ldconfig_scriptlets


%files
%license COPYING COPYING.GPL
%doc ACKNOWLEDGEMENTS AUTHORS NEWS NOTES README TODO
%{_bindir}/sfconvert
%{_bindir}/sfinfo
%{_libdir}/lib*.so.1*
%{_mandir}/man1/*

%files devel
%doc ChangeLog docs/*.3.txt
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_mandir}/man3/*

%changelog
* Wed Sep 07 2022 Muhammad Falak <mwani@microsoft.com> - 0.3.6-27
- Drop macro `%make_check`
- Drop check section as it produces a 35GB log file breaking ptest
- License verified

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.3.6-26
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.3.6-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 09 2018 Gwyn Ciesla <limburgher@gmail.com> - 1:0.3.6-21
- Fixes for CVE-2018-13440.

* Tue Oct 09 2018 Gwyn Ciesla <limburgher@gmail.com> - 1:0.3.6-20
- Fix for CVE-2018-17095.

* Mon Aug 13 2018 Leigh Scott <leigh123linux@googlemail.com> - 1:0.3.6-19
- Fix build

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:0.3.6-17
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 12 2017 Michael Schwendt <mschwendt@fedoraproject.org> - 1:0.3.6-13
- Merge upstream pull requests #42,#43,#44 from Agostino Sarubbo to fix
  security issues.  CVE-2017-6827, CVE-2017-6828,
  CVE-2017-6829, CVE-2017-6830, CVE-2017-6831,
  CVE-2017-6832, CVE-2017-6833, CVE-2017-6834, CVE-2017-6835,
  CVE-2017-6836, CVE-2017-6837, CVE-2017-6838, CVE-2017-6839

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb  3 2016 Michael Schwendt <mschwendt@fedoraproject.org> - 1:0.3.6-11
- patch to compile with GCC 6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.3.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct  8 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 1:0.3.6-9
- Merge fix from upstream pull request #25 for CVE-2015-7747.
  Test conversion from e.g. 16-bit LE stereo to 8-bit LE mono
  no longer causes corruption.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1:0.3.6-7
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 11 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 1:0.3.6-6
- BR flac-devel for FLAC support introduced in 0.3.6.

* Tue Feb 10 2015 Michael Schwendt <mschwendt@fedoraproject.org> - 1:0.3.6-5
- Don't include docs subdir in base package. It duplicates the manual
  pages and their .txt sources. Include the *.3.txt manual sources in
  the -devel package instead.
- Spec cleanup: drop %%defattr, drop %%clean and buildroot removal.
- Drop explicit Requires on pkgconfig from -devel package
  (pkg-config 0.8 is from 2002 or so, btw).
- Use %%license and add file COPYING to it.
- The two included programs are GPLv2+ licensed.
- Include more doc files.
- Add %%?_isa to base package Requires.
- Add %%check section for included testsuite.

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 07 2013 Adam Jackson <ajax@redhat.com> 0.3.6-1
- audiofile 0.3.6

* Wed Feb 06 2013 Adam Jackson <ajax@redhat.com> 0.3.5-1
- audiofile 0.3.5

* Wed Oct 10 2012 Bastien Nocera <bnocera@redhat.com> 0.3.4-1
- Update to 0.3.4

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Mar 22 2010 Bastien Nocera <bnocera@redhat.com> 0.2.7-1
- Update to 0.2.7

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.2.6-9
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:0.2.6-8
- Autorebuild for GCC 4.3

* Fri Aug 24 2007 Adam Jackson <ajax@redhat.com> - 1:0.2.6-7
- Rebuild for build ID

* Sat Feb  3 2007 Matthias Clasen <mclasen@redhat.com> - 1:0.2.6-6
- Corrections from package review
 
* Thu Jul 27 2006 Matthias Clasen <mclasen@redhat.com> - 1:0.2.6-5
- Fix multilib conflicts
- Don't ship static libraries

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:0.2.6-4.1
- rebuild

* Mon Apr 17 2006 John (J5) Palmieri <johnp@redhat.com> - 1:0.2.6-4
- Remove Makefile* from docs so they are not installed

* Fri Mar 24 2006 Matthias Clasen <mclasen@redhat.com> - 1:0.2.6-3
- Reduce memory consumption by making data tables const

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1:0.2.6-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1:0.2.6-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com> - 0.2.6-2.1
- rebuilt

* Thu Mar 17 2005 John (J5) Palmieri <johnp@redhat.com> - 0.2.6-2
- rebuild for gcc 4.0

* Fri Jul 30 2004 Colin Walters  <walters@redhat.com>
- Update to 0.2.6
- Rework description to not contain apostrophe that
  makes emacs unhappy

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com>
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 1:0.2.5-1
- update to 0.2.5

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:0.2.3-7.1
- rebuild for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com>
- fix URL (#71010)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 03 2002 Elliot Lee <sopwith@redhat.com>
- Remove unpackaged files

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jan  8 2002 Owen Taylor <otaylor@redhat.com>
- Update to 0.2.3, update URLs

* Mon Jun 25 2001 Preston Brown <pbrown@redhat.com>
- explicit requirement of -devel package on main package (#45205)

* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- Bumped version to 0.2.1

* Mon Dec 11 2000 Preston Brown <pbrown@redhat.com>
- upgrade to 0.1.11.

* Mon Aug 14 2000 Than Ngo <than@redhat.com>
- add ldconfig to %%post and %%postun (Bug #15413)

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- use FHS macros

* Thu Feb 03 2000 Preston Brown <pbrown@redhat.com>
- strip library, use configure macro.

* Tue Sep 14 1999 Elliot Lee <sopwith@redhat.com>
- 0.1.8pre (take whatever is in CVS).

* Fri Aug 13 1999 Michael Fulbrght <drmike@redhat.com>
- version 1.7.0

* Sun Apr 18 1999 Matt Wilson <msw@redhat.com>
- updated patch from DaveM

* Fri Apr 16 1999 Matt Wilson <msw@redhat.com>
- added patch from Dave Miller to disable byte swapping in decoding

* Fri Mar 19 1999 Michael Fulbright <drmike@redhat.com>
- strip binaries before packaging

* Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com>
- Version 0.1.6

* Sun Feb 21 1999 Michael Fulbright <drmike@redhat.com>
- Removed libtoolize from %%build

* Wed Feb 3 1999 Jonathan Blandfor <jrb@redhat.com>
- Newer version with bug fix.  Upped release.

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- integrating into rawhide release at GNOME freeze

* Fri Nov 20 1998 Michael Fulbright <drmike@redhat.com>
- First try at a spec file
