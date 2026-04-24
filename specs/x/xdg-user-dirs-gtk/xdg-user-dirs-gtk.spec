# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		xdg-user-dirs-gtk
Version:	0.16
Release: 2%{?dist}
Summary:	Gnome integration of special directories

License:	GPL-2.0-or-later
URL:		https://gitlab.gnome.org/GNOME/xdg-user-dirs-gtk
Source0:	https://download.gnome.org/sources/xdg-user-dirs-gtk/%{version}/%{name}-%{version}.tar.xz

# https://gitlab.gnome.org/GNOME/xdg-user-dirs-gtk/-/merge_requests/22
Patch0:		xdg-user-dirs-gtk-0.16-not-showin-kde.patch

BuildRequires:	desktop-file-utils
BuildRequires:	gcc
BuildRequires:	meson
BuildRequires:	systemd-rpm-macros
BuildRequires:	xdg-user-dirs
BuildRequires:	pkgconfig(gtk+-3.0)

Requires:	xdg-user-dirs

%description
Contains some integration of xdg-user-dirs with the gnome
desktop, including creating default bookmarks and detecting
locale changes.

%prep
%autosetup -p1

%build
%meson
%meson_build


%install
%meson_install

%find_lang %name

desktop-file-validate $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/user-dirs-update-gtk.desktop $RPM_BUILD_ROOT%{_datadir}/applications/user-dirs-update-gtk.desktop

%post
%systemd_user_post user-dirs-update-gtk.service

%preun
%systemd_user_preun user-dirs-update-gtk.service

%postun
%systemd_user_postun_with_restart user-dirs-update-gtk.service

%files -f %{name}.lang
%doc NEWS AUTHORS README ChangeLog
%license COPYING
%{_bindir}/xdg-user-dirs-gtk-update
%{_datadir}/applications/user-dirs-update-gtk.desktop
%{_userunitdir}/user-dirs-update-gtk.service
%config(noreplace) %{_sysconfdir}/xdg/autostart/user-dirs-update-gtk.desktop


%changelog
* Tue Dec 16 2025 David King <amigadave@amigadave.com> - 0.16-1
- Update to 0.16 (#2422022)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 David King <amigadave@amigadave.com> - 0.11-1
- Update to 0.11 (#2135328)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 11 2020 Timm Bäder <tbaeder@redhat.com> - 0.10-19
- Use make macros
- https://docs.fedoraproject.org/en-US/packaging-guidelines/#_parallel_make

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.10-7
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan 27 2014 Matthias Clasen <mclasen@redhat.com> - 0.10-4
- Add Mate to OnlyShowIn

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Matthias Clasen <mclasen@redhat.com> - 0.10-2
- Make 'Don't ask again' checkbox work properly (#968955)

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 0.10-1
- Update to 0.10

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 11 2012 Kalev Lember <kalevlember@gmail.com> - 0.9-1
- Update to 0.9
- Adjust BuildRequires to build with gtk3
- Drop lxde patch, merged upstream
- Validate the desktop file

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Adam Jackson <ajax@redhat.com> 0.8-7
- Rebuild to break bogus libpng dep

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 13 2010 Matthias Clasen <mclasen@redhat.com>
- Work in LXDE too (#563827)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep  8 2008 Tomas Bzatek <tbzatek@redhat.com> - 0.8-2
- Require intltool

* Fri Sep  5 2008 Matthias Clasen  <mclasen@redhat.com> - 0.8-1
- Update to 0.8
 
* Tue Aug 12 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 0.7-2
- Fix license tag.

* Tue Feb 12 2008 Alexander Larsson <alexl@redhat.com> - 0.7-1
- Update to 0.7
- Uncomment missing patches

* Sun Nov  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.6-4
- Correct the URL

* Mon Oct  1 2007 Matthias Clasen <mclasen@redhat.com> - 0.6-2
- Fix the special case for en_US  (#307881)

* Tue Aug 21 2007 Alexander Larsson <alexl@redhat.com> - 0.6-1
- Update to 0.6 (new translations)

* Fri Jul  6 2007  Matthias Clasen  <mclasen@redhat.com> - 0.5-2
- Make the autostart file work in KDE (#247304)

* Wed Apr 25 2007  <alexl@redhat.com> - 0.5-1
- Update to 0.5
- Fixes silly dialog when no translations (#237384)

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 0.4-1
- update to 0.4 (#234512)

* Tue Mar  6 2007 Alexander Larsson <alexl@redhat.com> - 0.3-1
- update to 0.3
- Add xdg-user-dirs buildreq

* Fri Mar  2 2007 Alexander Larsson <alexl@redhat.com> - 0.2-1
- Update to 0.2

* Fri Mar  2 2007 Alexander Larsson <alexl@redhat.com> - 0.1-2
- Add buildrequires
- Mark autostart file as config

* Wed Feb 28 2007 Alexander Larsson <alexl@redhat.com> - 0.1-1
- Initial version

