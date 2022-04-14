Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		opal
Summary:	Open Phone Abstraction Library
Version:	3.10.11
Release:	6%{?dist}
URL:		http://www.opalvoip.org/
License:	MPLv1.0

# We cannot use unmodified upstream source code because it contains some areas of legal concern.
# rm -rf plugins/video/H.263-1998/ 
# rm -rf plugins/video/H.264/
# rm -rf plugins/video/MPEG4-ffmpeg/
# Source0:	ftp://ftp.gnome.org/pub/gnome/sources/%{name}/3.10/%{name}-%{version}.tar.xz
Source0:	%{name}-%{version}-clean.tar.xz
Patch0:		opal-3.10-fix-cflags.patch

BuildRequires:	expat-devel
BuildRequires:	gcc-c++
BuildRequires:	gsm-devel
BuildRequires:	libtheora-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	ptlib-devel = 2.10.11
BuildRequires:	SDL-devel
BuildRequires:	speex-devel
BuildRequires:	speexdsp-devel

%description
Open Phone Abstraction Library, implementation of the ITU H.323
teleconferencing protocol, and successor of the openh323 library.

%package devel
Summary:	Development package for opal
Requires:	opal = %{version}-%{release}
Requires:	openssl-devel
Requires:	ptlib-devel = 2.10.11
Requires:	pkgconfig

%description devel
The opal-devel package includes the development libraries and 
header files for opal.

%prep
%setup -q 
%patch0 -p1 -b.cf

for file in dll so bin lib exe; do 
  find . -name "*.$file" -delete
done    

%build
# Note: SILK is only disabled because the SDK libs are not in Fedora
%configure --disable-silk

make OPTCCFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install

rm -f %{buildroot}/%{_datadir}/opal/opal_inc.mak
rm -f %{buildroot}/%{_libdir}/libopal_s.a

# avoid multilib conflict
mv %{buildroot}/%{_includedir}/opal/opal/buildopts.h \
   %{buildroot}/%{_includedir}/opal/opal/buildopts-%{__isa_bits}.h
cat >%{buildroot}/%{_includedir}/opal/opal/buildopts.h <<EOF
#ifndef OPAL_BUILDOPTS_H_MULTILIB
#define OPAL_BUILDOPTS_H_MULTILIB

#include <bits/wordsize.h>

#if  __WORDSIZE == 32
# include "buildopts-32.h"
#elif __WORDSIZE == 64
# include "buildopts-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

%ldconfig_scriptlets

%files
%license mpl-1.0.htm
%{_libdir}/*.so.*
%{_libdir}/%{name}-%{version}

%files devel
%doc docs/*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/opal.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.10.11-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.11-2
- Rebuild

* Sun Jul 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.11-1
- 3.10.11 stable release
- Build with system gsm
- Spec cleanups

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.10.10-8
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 26 2015 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.10-7
- rebuild (gcc5)

* Thu Jan 29 2015 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.10-6
- Add speexdsp-devel as a dep to fix FTBFS

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Oct  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.10.10-3
- Avoid multilib conflict

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 20 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.10
- New 3.10.10 stable release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.9-2
- Fix devel dependencies

* Mon Nov 26 2012 Peter Robinson <pbrobinson@fedoraproject.org> 3.10.9-1
- New 3.10.9 stable release

* Sat Aug 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.10.7-1
- New 3.10.7 stable release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 22 2012 Tom Callaway <spot@fedoraproject.org> - 3.10.2-4
- post audit update

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 3.10.2-2
- Fix versioning for -devel

* Tue Aug 23 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 3.10.2-1
- New 3.10.2 stable release

* Sat Jul 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 3.10.1-1
- New 3.10.1 stable release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 3.8.3-1
- New 3.8.3 stable release

* Mon May 31 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.8-1
- New 3.6.8 stable release

* Tue Jan 26 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.6-2
- Package review cleanup

* Tue Sep 22 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.6-1
- New 3.6.6 stable release

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.6.4-4
- rebuilt with new openssl

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.4-2
- Increment required ptlib version

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.4-1
- New 3.6.4 stable release

* Thu May 28 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.2-2
- Add an upstream patch to fix a deadlock issue.

* Tue May 19 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.2-1
- New stable release for ekiga 3.2.1

* Sun Apr 26 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.1-3
- pull in some upstream fixes for possible crashes

* Tue Apr 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 3.6.1-2
- pull out ilbc codec due to legal issues

* Wed Mar 18 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.1-1
- New stable release for ekiga 3.2.0

* Fri Mar  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.0-2
- Remove CELT until the bitstream is stable and can hence intercommunicate between versions

* Tue Mar  3 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.6.0-1
- New release for ekiga 3.1.2 beta

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5.2-7
- Add patches to fix gcc44 compilation, remove celt until issues
  are fixed upstream

* Tue Feb 3  2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5.2-6
- Add support for the celt codec

* Mon Feb 2  2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5.2-5
- Fix blank soname 

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 3.5.2-4
- rebuild with new openssl

* Tue Jan 13 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5.2-3
- Yet another dep that configure doesn't check and it just fails on

* Tue Jan 13 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5.2-2
- Add a build dep

* Tue Jan  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5.2-1
- New release for ekiga 3.1.0 beta
- Some updates from merge review

* Fri Dec  5 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 3.4.2-2
- Update spec to ensure we own directories

* Mon Oct 20 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 3.4.2-1
- Update to new stable release for ekiga 3.0.1

* Tue Sep 23 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 3.4.1-1
- Update to new stable release for ekiga 3

* Thu Sep 11 2008 Peter Robinson <pbrobinson@fedoraproject.org> - 3.3.1-1
- Update release to 3.3.1 for ekiga 3 beta

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.2.11-5
- fix license tag

* Mon May 12 2008 Paul W. Frields <stickster@gmail.com> - 2.2.11-4
- Rebuild in service of ekiga (#441202)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.2.11-3
- Autorebuild for GCC 4.3

* Thu Dec  6 2007 Jeremy Katz <katzj@redhat.com> - 2.2.11-2
- rebuild for new openssl and openldap

* Tue Sep 18 2007 Daniel Veillard <veillard@redhat.com> - 2.2.11-1
- upstream release of 2.2.11

* Tue Sep 18 2007 Daniel Veillard <veillard@redhat.com> - 2.2.10-1
- upstream release of 2.2.10
- includes the 2 cisco patches

* Wed Aug 22 2007 Daniel Veillard <veillard@redhat.com> - 2.2.8-5.fc8
- added 2 patches needed when using a CISCO server

* Sun Apr 15 2007 Daniel Veillard <veillard@redhat.com> - 2.2.8-1
- upstream release of 2.2.8

* Mon Mar 12 2007 Daniel Veillard <veillard@redhat.com> - 2.2.6-1
- upstream release of 2.2.6

* Wed Feb 14 2007 Daniel Veillard <veillard@redhat.com> - 2.2.5-1
- upstream release of 2.2.5

* Mon Jan 22 2007 Daniel Veillard <veillard@redhat.com> - 2.2.4-1
- upstream release of 2.2.4

* Wed Dec 20 2006 Daniel Veillard <veillard@redhat.com> - 2.2.3-4
- applied patch from upstream to fix RFC2833 DTMF duration problem
- Resolves: rhbz#220333

* Mon Nov  6 2006 Daniel Veillard <veillard@redhat.com> - 2.2.3-3
- moved the .so to -devel
- Resolves: rhbz#203633

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.3-2
- Rebuild against newer pwlib

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.3-1
- Update to 2.2.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.2-1.1
- rebuild

* Wed May 31 2006 Daniel Veillard <veillard@redhat.com> - 2.2.2-1
- new release for ekiga-2.0.2
- try to fix #192740 mutilib problem

* Tue Mar 14 2006 Daniel Veillard <veillard@redhat.com> - 2.2.1-1
- last minute break fix and new release

* Tue Mar 14 2006 Ray Strode <rstrode@redhat.com> - 2.2.0-2
- rebuild

* Mon Mar 13 2006 Daniel Veillard <veillard@redhat.com> - 2.2.0-1
- final version for ekiga-2.0.0

* Mon Feb 13 2006 Daniel Veillard <veillard@redhat.com> - 2.1.3-1
- new beta version for ekiga

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Daniel Veillard <veillard@redhat.com> - 2.1-1
- initial version based on the openh323 spec file
