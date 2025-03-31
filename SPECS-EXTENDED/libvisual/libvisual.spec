%global smallversion 0.4

Name:           libvisual
Version:        0.4.1
Release:        5%{?dist}
Epoch:          1

Summary:        Abstraction library for audio visualisation plugins
License:        LGPL-2.1-or-later
URL:            https://libvisual.sf.net
Source0:        https://sourceforge.net/projects/%{name}/files/%{name}/%{name}-%{version}/%{name}-%{version}.tar.bz2

Patch0:         libvisual-0.4.0-better-altivec-detection.patch
Patch1:         libvisual-0.4.0-respect-environment-ldflags.patch
Patch2:         libvisual-c99.patch

BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  sdl12-compat-devel
BuildRequires:  xorg-x11-proto-devel

%description
Libvisual is an abstraction library that comes between applications and
audio visualisation plugins.

Often when it comes to audio visualisation plugins or programs that create
visuals they do depend on a player or something else, basically there is no
general framework that enable application developers to easy access cool
audio visualisation plugins. Libvisual wants to change this by providing
an interface towards plugins and applications, through this easy to use
interface applications can easily access plugins and since the drawing is
done by the application it also enables the developer to draw the visual
anywhere he wants.

%package        devel
Summary:        Development files for libvisual
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description    devel
Libvisual is an abstraction library that comes between applications and
audio visualisation plugins.

This package contains the files needed to build an application with libvisual.

%prep
%setup -q
%patch -P0 -p1 -b .better-altivec-detection
%patch -P1 -p1 -b .respect-environment-ldflags
%patch -P2 -p1 -b .c99

%build
%configure
%make_build

%install
%make_install

# Avoid multilib conflicts
case `uname -i` in
  i386 | ppc | s390 | sparc )
    wordsize="32"
    ;;
  x86_64 | ppc64 | s390x | sparc64 )
    wordsize="64"
    ;;
  *)
    wordsize=""
    ;;
esac

if test -n "$wordsize"
then
  mv %{buildroot}%{_includedir}/libvisual-%{smallversion}/libvisual/lvconfig.h \
     %{buildroot}%{_includedir}/libvisual-%{smallversion}/libvisual/lvconfig-$wordsize.h

  cat >%{buildroot}%{_includedir}/libvisual-%{smallversion}/libvisual/lvconfig.h <<EOF
#ifndef __LV_CONFIG_H_MULTILIB__
#define __LV_CONFIG_H_MULTILIB__

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "lvconfig-32.h"
#elif __WORDSIZE == 64
# include "lvconfig-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

fi

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%find_lang %{name}-%{smallversion}

%files -f %{name}-%{smallversion}.lang
%doc AUTHORS ChangeLog NEWS README TODO
%license COPYING
%{_libdir}/*.so.*

%files devel
%doc README NEWS TODO AUTHORS
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}-%{smallversion}


%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 08 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1:0.4.1-1
- Updated to version 0.4.1.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Florian Weimer <fweimer@redhat.com> - 1:0.4.0-37
- C99 compatibility fixes

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 23 2021 Timm Bäder <tbaeder@redhat.com> - 1:0.4.0-34
- Add patch to respect environment LDFLAGS

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Kalev Lember <klember@redhat.com> - 1:0.4.0-31
- Use make_build/make_install macros
- Drop unneeded ldconfig_scriptlets macro call
- Remove a no longer needed -mmmx CFLAGS addition
- Disable strict aliasing

* Fri Jan 15 2021 Kalev Lember <klember@redhat.com> - 1:0.4.0-30
- Fix multilib conflicts in lvconfig.h

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.4.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Tom Callaway <spot@fedoraproject.org> - 1:0.4.0-19
- spec file cleanups

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.4.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 13 2014 Kalev Lember <kalevlember@gmail.com> - 1:0.4.0-16
- Fix epoch use

* Wed Jun 11 2014 Tom Callaway <spot@fedoraproject.org> - 1:0.4.0-15
- 0.5.0 beta was a bad idea. nothing else supports it.
- fix format-security issue

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 07 2009 Caolán McNamara <caolanm@redhat.com> - 0.4.0-8
- defining inline causes problems trying to build against libvisual headers, 
  e.g. libvisual-plugins

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 11 2008 - Bastien Nocera <bnocera@redhat.com> - 0.4.0-6
- Better Altivec detection, code from David Woodhouse

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.0-5
- Autorebuild for GCC 4.3

* Sun Aug 26 2007 Aurelien Bompard <abompard@fedoraproject.org> 0.4.0-4
- fix license tag

* Wed Aug 30 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.4.0-3
- rebuild

* Sat Jul 08 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.4.0-2
- bump release

* Thu Jul 06 2006 Aurelien Bompard <abompard@fedoraproject.org> 0.4.0-1
- version 0.4.0
- drop Patch0 (applied upstream)

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-8
- fix dependency for modular X

* Tue Feb 21 2006 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-7
- rebuild for FC5

* Wed Jun 15 2005 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-6
- rebuild

* Wed Jun 15 2005 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-5
- fix build for GCC4

* Thu Jun  9 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.2.0-4
- use dist tag for all-arch-rebuild

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> 0.2.0-3
- rebuilt

* Mon Feb 14 2005 David Woodhouse <dwmw2@infradead.org> 0.2.0-2
- Fix bogus #if where #ifdef was meant

* Thu Feb 10 2005 Aurelien Bompard <gauret[AT]free.fr> 0.2.0-1
- version 0.2.0
- drop patch

* Sat Nov 27 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.1.7-0.fdr.1
- version 0.1.7

* Thu Oct 21 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.1.6-0.fdr.2
- Apply Adrian Reber's suggestions in bug 2182

* Tue Sep 28 2004 Aurelien Bompard <gauret[AT]free.fr> 0:0.1.6-0.fdr.1
- Initial RPM release.
