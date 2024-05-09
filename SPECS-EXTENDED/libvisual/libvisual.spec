Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global smallversion 0.4

Name:           libvisual
Version:        0.4.0
Release:        30%{?dist}
Summary:        Abstraction library for audio visualisation plugins
License:        LGPLv2+
URL:            https://libvisual.sf.net
Source0:        https://dl.sf.net/libvisual/libvisual-%{version}.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  xorg-x11-proto-devel
# https://bugzilla.redhat.com/show_bug.cgi?id=435771
Patch0:         libvisual-0.4.0-better-altivec-detection.patch
Patch1:         libvisual-0.4.0-inlinedefineconflict.patch
Patch2:		libvisual-0.4.0-format-security.patch

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
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Libvisual is an abstraction library that comes between applications and
audio visualisation plugins.

This package contains the files needed to build an application with libvisual.

%prep
%setup -q
%patch 0 -p1 -b .altivec-detection
%patch 1 -p1 -b .inlinedefineconflict
%patch 2 -p1 -b .format-security

%build
%ifarch i386
export CFLAGS="${RPM_OPT_FLAGS} -mmmx"
%endif
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

%find_lang %{name}-%{smallversion}

%ldconfig_scriptlets

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
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.4.0-30
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.4.0-29
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
