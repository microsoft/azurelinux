Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: Library for tracking application startup
Name: startup-notification
Version: 0.12
Release: 20%{?dist}
URL: https://www.freedesktop.org/software/startup-notification/
#VCS: git:git://git.freedesktop.org/git/startup-notification
Source0: https://www.freedesktop.org/software/startup-notification/releases/%{name}-%{version}.tar.gz
License: LGPLv2
BuildRequires:  gcc
BuildRequires: libX11-devel
BuildRequires: libXt-devel
BuildRequires: xcb-util-devel

%description
This package contains libstartup-notification which implements a
startup notification protocol. Using this protocol a desktop
environment can track the launch of an application and provide
feedback such as a busy cursor, among other features.

%package devel
Summary: Development portions of startup-notification
Requires: %{name} = %{version}-%{release}
Requires: libX11-devel
Requires: pkgconfig

%description devel
Header files and static libraries for libstartup-notification.

%prep
%setup -q
mkdir examples
cp -p test/*.c test/*.h examples

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
/bin/rm -f $RPM_BUILD_ROOT%{_libdir}/*.{a,la}

%ldconfig_scriptlets

%files
%doc doc/startup-notification.txt
%doc AUTHORS COPYING ChangeLog NEWS
%{_libdir}/lib*.so.*

%files devel
%doc examples 
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Aug 20 2012 Adam Jackson <ajax@redhat.com> 0.12-5
- Rebuild for new xcb-util soname

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Adam Jackson <ajax@redhat.com> 0.12-2
- Rebuild for new xcb-util

* Tue May 24 2011 Colin Walters <walters@verbum.org> - 0.12-1
- Update to 0.12; allows us to drop patch

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Apr 05 2010 Colin Walters <walters@verbum.org> - 0.10-4
- Add patch from upstream for better GNOME 3 support

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Matthias Clasen <mclasen@redhat.com> 0.10-1
- Update to 0.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec  2 2008 Matthias Clasen <mclasen@redhat.com>
- Rebuild for pkg-config provides

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9-4
- Autorebuild for GCC 4.3

* Wed Oct 03 2007 Parag Nemade <pnemade@redhat.com> - 0.9-3
- Added test examples to -devel package
- Use macros in Source URL 
- update spec as per 226435

* Thu Aug 23 2007 Adam Jackson <ajax@redhat.com> - 0.9-2
- Rebuild for build ID

* Sun Mar 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.9-1
- Update to 0.9

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.8-4.1
- rebuild

* Mon May 22 2006 Matthias Clasen <mclasen@redhat.com> - 0.8-4
- Add missing BuildRequires
- Don't install static libraries

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.8-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.8-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov  1 2005 Ray Strode <rstrode@redhat.com> 0.8-3
- change to new modular X dependencies
- move configure to build instead of prep
- use make install DESTDIR=$RPM_BUILD_ROOT instead of
  makeinstall macro

* Wed Mar  2 2005 Mark McLoughlin <markmc@redhat.com> 0.8-2
- Rebuild with gcc4

* Thu Jan 27 2005 Matthias Clasen <mclasen@redhat.com> 0.8-1
- Update to 0.8

* Wed Aug  4 2004 Mark McLoughlin <markmc@redhat.com> 0.7-1
- Update to 0.7

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Warren Togami <wtogami@redhat.com> 0.6-2
- #110753 XFree86-devel

* Thu Apr  1 2004 Mark McLoughlin <markmc@redhat.com> 0.6-1
- Update to 0.6

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb  5 2003 Havoc Pennington <hp@redhat.com> 0.5-1
- 0.5

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- Initial build.


