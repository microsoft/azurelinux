# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define libmatchbox_devel_ver 1.9-2
%define alphatag 20070628svn

# https://src.fedoraproject.org/rpms/redhat-rpm-config/blob/master/f/buildflags.md#legacy-fcommon
%define _legacy_common_support 1

Summary:       Window manager for the Matchbox Desktop
Name:          matchbox-window-manager
Version:       1.2
Release:       39.%{alphatag}%{?dist}
Url:           http://matchbox-project.org/
# svn checkout http://svn.o-hand.com/repos/matchbox/trunk/matchbox-window-manager
License:       GPL-2.0-or-later
Source0:       %{name}-%{version}-%{alphatag}.tar.gz

Patch1: matchbox-window-manager-1.2-keysyms.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig 
BuildRequires:  expat-devel
BuildRequires:  libmatchbox-devel >= %{libmatchbox_devel_ver}
BuildRequires:  startup-notification-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-devel
BuildRequires:  pango-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXcursor-devel
Requires:       filesystem

%description
Matchbox is a base environment for the X Window System running on non-desktop
embedded platforms such as handhelds, set-top boxes, kiosks and anything else
for which screen space, input mechanisms or system resources are limited.

This package contains the window manager from Matchbox.

%prep
%autosetup -p 2

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%files
%doc AUTHORS README ChangeLog COPYING
%{_bindir}/*
%dir %{_sysconfdir}/matchbox
%config(noreplace) %{_sysconfdir}/matchbox/kbdconfig
%dir %{_datadir}/matchbox
%{_datadir}/matchbox/*
%{_datadir}/themes/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-39.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-38.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-37.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-36.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-35.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-34.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-33.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-32.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-31.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-30.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-29.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-28.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Feb  6 2020 Petr Lautrbach <plautrba@redhat.com> - 1.2-27.20070628svn
- add -fcommon to the flags (#1799634)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-26.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-25.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-24.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-23.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-22.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-21.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-20.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-19.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-18.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-17.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-16.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-15.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-14.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-13.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.2-12.20070628svn
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 1.2-11.20070628svn
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-10.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-9.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Adam Jackson <ajax@redhat.com> 1.2-8.20070628svn
- Rebuild for libpng 1.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5.20070628svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2-4.20070628svn
- fix license tag

* Sun Mar  9 2008 Marco Pesenti Gritti <mpg@redhat.com> - 1.2-3.20070628svn
- Add dist tag

* Fri Nov  9 2007 Marco Pesenti Gritti <marco@localhost.localdomain> - 1.2-3.20070628svn
- Add patch to fix some keybindings

* Thu Jun 28 2007 Marco Pesenti Gritti <mpg@redhat.com> - 1.2-2.20070628svn
- New snapshot

* Tue Jun 19 2007 Marco Pesenti Gritti <mpg@redhat.com> 1.2-1
- Update source to 1.2

* Tue Jun 19 2007 John (J5) Palmieri <johnp@redhat.com> 1.9-3
- Fix buildroot
- Add COPYING license file to docs
- Added {} braces around % macros
- Own {_sysconfdir}/matchbox directory
- Own {_datadir}/matchbox

* Sat Feb 24 2007 Marco Pesenti Gritti <mpg@redhat.com> 1.1-6.cvs20072402.6
- Update to cvs20072402

* Wed Jan 31 2007 Marco Pesenti Gritti <mpg@redhat.com> 1.1-5.cvs20073101.6
- Update to cvs20073101

* Wed Dec 20 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-5.cvs20061219.5
- Build with Xcursor support

* Tue Dec 19 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-5.cvs20061219.4
- Update to cvs20061219

* Tue Oct 17 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-5.cvs20060911.3
- Temporarily drop composite

* Thu Oct  5 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-5.cvs20060911.2
- Enable composite
- Add some composite dependencies

* Mon Sep 11 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-5.cvs20060911.1
- Remove some gconf leftovers

* Mon Sep 11 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-5.cvs20060911.0
- Rebuild

* Mon Sep 11 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-cvs20060911-1
- Update

* Mon Aug 21 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-3
- Rebuild
- Depend on libmatchbox 1.9-2
- Do not package gconf schemas

* Mon Aug 21 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-3
- Build with the default options

* Mon Aug 21 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-2
- Missing build reqs

* Mon Aug 21 2006 Marco Pesenti Gritti <mpg@redhat.com> 1.1-1
- Update to 1.1

* Thu Aug 25 2005 Austin Acton <austin@mandriva.org> 0.9.5-1mdk
- New release 0.9.5

* Thu May 12 2005 Austin Acton <austin@mandriva.org> 0.9.4-1mdk
- 0.9.4
- new URLs

* Mon Jan 24 2005 Austin Acton <austin@mandrake.org> 0.9.2-1mdk
- 0.9.2

* Mon Jan 10 2005 Austin Acton <austin@mandrake.org> 0.9-1mdk
- 0.9

* Wed Sep 29 2004 Austin Acton <austin@mandrake.org> 0.8.4-1mdk
- 0.8.4

* Mon Aug 23 2004 Austin Acton <austin@mandrake.org> 0.8.3-2mdk
- fix schemas

* Mon Aug 23 2004 Austin Acton <austin@mandrake.org> 0.8.3-1mdk
- 0.8.3

* Tue Aug 10 2004 Austin Acton <austin@mandrake.org> 0.8.2-3mdk
- buildrequires xsettings

* Tue Jul 27 2004 Austin Acton <austin@mandrake.org> 0.8.2-1mdk
- enable startup-notification

* Mon Jul 20 2004 Austin Acton <austin@mandrake.org> 0.8.2-1mdk
- 0.8.2

