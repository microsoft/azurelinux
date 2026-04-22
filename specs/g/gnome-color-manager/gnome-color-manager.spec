# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:      gnome-color-manager
Version:   3.36.2
Release: 3%{?dist}
Summary:   Color management tools for GNOME
License:   GPL-2.0-or-later
URL:       https://gitlab.gnome.org/GNOME/gnome-color-manager
Source0:   http://download.gnome.org/sources/gnome-color-manager/3.36/%{name}-%{version}.tar.xz

BuildRequires: gcc
BuildRequires: gtk3-devel >= 3.0.0
BuildRequires: gettext
BuildRequires: lcms2-devel
BuildRequires: glib2-devel >= 2.25.9-2
BuildRequires: docbook-utils
BuildRequires: colord-devel >= 0.1.12
BuildRequires: itstool
BuildRequires: meson

Requires: shared-mime-info

# obsolete sub-package
Obsoletes: gnome-color-manager-devel <= 3.1.1
Provides: gnome-color-manager-devel

%description
gnome-color-manager is a session framework that makes it easy to manage, install
and generate color profiles in the GNOME desktop.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%find_lang %name --with-gnome

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README
%{_bindir}/gcm-*
%{_datadir}/applications/gcm-*.desktop
%{_datadir}/applications/org.gnome.ColorProfileViewer.desktop
%dir %{_datadir}/gnome-color-manager
%dir %{_datadir}/gnome-color-manager/figures
%{_datadir}/gnome-color-manager/figures/*
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/scalable/*/*.svg*
%{_datadir}/metainfo/org.gnome.ColorProfileViewer.appdata.xml
%{_mandir}/man1/*.1*

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jan 21 2025 nmontero <nmontero@redhat.com> - 3.36.2-1
- Update to 3.36.2

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Richard Hughes <rhughes@redhat.com> - 3.36.0-5
- Remove BRs no longer required for building

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 02 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Wed Mar 04 2020 Kalev Lember <klember@redhat.com> - 3.35.90-1
- Update to 3.35.90

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Richard Hughes <rhughes@redhat.com> - 3.32.0-3
- Remove the req for argyllcms as it is now orphaned

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Wed Jan 30 2019 Rex Dieter <rdieter@fedoraproject.org> - 3.30.0-3
- rebuild (exiv2)

* Wed Jan 30 2019 Björn Esser <besser82@fedoraproject.org> - 3.30.0-2
- rebuild (exiv2)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.0-2
- Remove obsolete scriptlets

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 3.25.90-1
- Update to 3.25.90
- Switch to the meson build system

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 3.24.0-2
- rebuild (exiv2)

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Sat Mar 11 2017 Richard Hughes <rhughes@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 23 2016 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Mon Aug 29 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91
- Don't set group tags

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Mon Feb 15 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Wed Jun 24 2015 Rex Dieter <rdieter@fedoraproject.org> - 3.16.0-4
- rebuild (exiv2)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Mon Mar 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91
- Use the %%license macro for the COPYING file

* Mon Feb 16 2015 Richard Hughes <rhughes@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Tue Jan 20 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 27 2014 Rex Dieter <rdieter@fedoraproject.org> 3.13.1-5
- omit needless scriptlet deps, %%postun update-mime-database only on removal

* Fri Jun 27 2014 Bastien Nocera <bnocera@redhat.com> 3.13.1-4
- Don't run update-mime-database in post, we don't ship mime XML
  files anymore.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Drop gnome-icon-theme dependency

* Mon Apr 28 2014 Richard Hughes <rhughes@redhat.com> - 3.13.1-1
- Update to 3.13.1

* Fri Apr 11 2014 Richard Hughes <rhughes@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Mon Feb 17 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Thu Dec 05 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-3
- Fix calibration when using new versions of ArgyllCMS

* Tue Dec 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 3.10.1-2
- rebuild (exiv2)

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92
- Include the appdata file
- Drop scrollkeeper and gnome-doc-utils build deps

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.2-4
- Rebuilt for libgnome-desktop soname bump

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.2-3
- Rebuilt for cogl 1.15.4 soname bump

* Wed Jul 31 2013 Adam Williamson <awilliam@redhat.com> - 3.8.2-2
- rebuild for new colord

* Mon May 13 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Richard Hughes <rhughes@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Richard Hughes <rhughes@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Mon Mar 18 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-3
- Rebuilt for cogl soname bump

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5-2
- Rebuilt for libgnome-desktop soname bump

* Tue Feb 05 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.6.1-2
- Rebuild for new cogl

* Thu Jan 10 2013 Richard Hughes <hughsient@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-3
- Rebuilt for libgnome-desktop-3 3.7.3 soname bump

* Tue Oct  2 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.0-2
- Drop unnecessary GConf2 dep
- Update to 3.6.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Fri Jun  8 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.1-3
- Rebuild

* Mon May 28 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.5.1-2
- Add missing colord-gtk-devel, itstool dependencies

* Thu May 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Wed May 02 2012 Rex Dieter <rdieter@fedoraproject.org> - 3.4.0-2
- rebuild (exiv2)

* Mon Mar 26 2012 Richard Hughes <rhughes@redhat.com> - 3.4.0-1
- New upstream version.

* Wed Mar 14 2012 Richard Hughes <rhughes@redhat.com> - 3.3.91-1
- New upstream version.

* Mon Feb 06 2012 Richard Hughes <rhughes@redhat.com> - 3.3.5-1
- New upstream version.

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-4
- Rebuild against new cogl

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 19 2011 Richard Hughes <rhughes@redhat.com> - 3.3.3-2
- Add BR gnome-desktop3-devel

* Mon Dec 19 2011 Richard Hughes <rhughes@redhat.com> - 3.3.3-1
- New upstream version.

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-2
- Rebuild against new clutter

* Mon Oct 17 2011 Richard Hughes <rhughes@redhat.com> - 3.2.1-1
- New upstream version.

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 3.2.0-4
- rebuild (exiv2)

* Thu Oct 06 2011 Adam Jackson <ajax@redhat.com> 3.2.0-3
- 0001-Initialize-error-pointer-for-gdk_pixbuf_new_from_fil.patch: Backport
  a crash fix from mainline.

* Mon Sep 26 2011 Richard Hughes <rhughes@redhat.com> - 3.2.0-2
- Rebuild for libmash API update.

* Mon Sep 26 2011 Richard Hughes <rhughes@redhat.com> - 3.2.0-1
- New upstream version.

* Mon Sep 19 2011 Richard Hughes <rhughes@redhat.com> - 3.1.92-1
- New upstream version.

* Fri Sep 16 2011 Richard Hughes <rhughes@redhat.com> - 3.1.91-3
- Rebuild for libmash soname update (which for the moment will disable
  the 3D renderer code).

* Mon Sep 05 2011 Richard Hughes <rhughes@redhat.com> - 3.1.91-1
- New upstream version.

* Tue Aug 30 2011 Richard Hughes <rhughes@redhat.com> - 3.1.90-2
- BR a high enough colord.

* Tue Aug 30 2011 Richard Hughes <rhughes@redhat.com> - 3.1.90-1
- New upstream version.

* Mon Jun 13 2011 Richard Hughes <rhughes@redhat.com> - 3.1.2-1
- New upstream version.

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.1.1-2
- Update gsettings scriptlet

* Fri May 06 2011 Richard Hughes <rhughes@redhat.com> - 3.1.1-1
- New upstream version.

* Mon Apr 04 2011 Richard Hughes <rhughes@redhat.com> - 3.0.0-1
- New upstream version.

* Mon Mar 21 2011 Richard Hughes <rhughes@redhat.com> - 2.91.92-3
- No gtk-doc anymore.

* Mon Mar 21 2011 Richard Hughes <rhughes@redhat.com> - 2.91.92-2
- We're installing into gnome-settings-daemon-3.0 now.

* Mon Mar 21 2011 Richard Hughes <rhughes@redhat.com> - 2.91.92-1
- New upstream version.

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-2
- Rebuild against newer gtk

* Tue Jan 11 2011 Richard Hughes <rhughes@redhat.com> - 2.91.5-1
- New upstream version.

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.3-4
- Rebuild against newer gtk3

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 2.91.3-3
- rebuild (exiv2)

* Fri Dec 03 2010 Peter Robinson <pbrobinson@gmail.com> 2.91.3-2
- Move devel files to sub package, cleanup spec file

* Wed Dec 01 2010 Richard Hughes <richard@hughsie.com> 2.91.3-1
- New upstream release.

* Mon Nov 08 2010 Richard Hughes <richard@hughsie.com> 2.91.2-1
- New upstream release.

* Wed Nov 03 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.3.20101102
- Rebuild now libnotify 0.7.0 is in rawhide, actually.

* Wed Nov 03 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.2.20101102
- Rebuild now libnotify 0.7.0 is in rawhide.

* Tue Nov 02 2010 Richard Hughes <richard@hughsie.com> 2.91.2-0.1.20101102
- Update to a git snapshot to fix rawhide.

* Tue Oct 05 2010 Richard Hughes <richard@hughsie.com> 2.91.1-4
- Add BR docbook-utils

* Tue Oct 05 2010 Richard Hughes <richard@hughsie.com> 2.91.1-3
- Add BR libusb1-devel

* Tue Oct 05 2010 Richard Hughes <richard@hughsie.com> 2.91.1-2
- Add BR gnome-settings-daemon-devel

* Tue Oct 05 2010 Richard Hughes <richard@hughsie.com> 2.91.1-1
- New upstream release.

* Mon Sep 20 2010 Richard Hughes <richard@hughsie.com> 2.31.4-2
- Remove the explicit dependency on yelp.
- Resolves: #626242

* Thu Jul 01 2010 Richard Hughes <richard@hughsie.com> 2.31.4-1
- New upstream release.

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.31.3-3
- Rebuild

* Tue Jun 22 2010 Richard Hughes <richard@hughsie.com> 2.31.3-2
- Actually upload new tarball. Grrr.

* Mon Jun 21 2010 Richard Hughes <richard@hughsie.com> 2.31.3-1
- New upstream release.

* Wed Jun 16 2010 Matthias Clasen <mclasen@redhat.com> 2.31.2-5
- Nuke the scrollkeeper runtime dep

* Thu Jun 03 2010 Richard Hughes <richard@hughsie.com> 2.31.2-4
- Patience is a virtue, pursue it if you can -- never in a programmer
  always in a can.

* Wed Jun 02 2010 Richard Hughes <richard@hughsie.com> 2.31.2-3
- Build against the fixed sane-backends.

* Wed Jun 02 2010 Richard Hughes <richard@hughsie.com> 2.31.2-2
- Actually upload source tarball...

* Wed Jun 02 2010 Richard Hughes <richard@hughsie.com> 2.31.2-1
- New upstream release.

* Thu May 06 2010 Richard Hughes <richard@hughsie.com> 2.31.1-1
- New upstream release.

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1

* Fri Apr  2 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-4
- BR GConf to make the macros work
- Modernize icon cache handling

* Wed Mar 31 2010 Richard Hughes <richard@hughsie.com> 2.30.0-3
- Fix up a scriptlet problem.
- Resolves: #578611

* Mon Mar 29 2010 Richard Hughes <richard@hughsie.com> 2.30.0-2
- Add libnotify BR.

* Mon Mar 29 2010 Richard Hughes <richard@hughsie.com> 2.30.0-1
- New upstream release.

* Tue Mar 09 2010 Richard Hughes <richard@hughsie.com> 2.29.4-2
- Update to the latest version of the Fedora Packaging Guidelines
- Remove the custom BuildRoot
- Do not clean the buildroot before install
- Use the gconf_schema defines for the GConf schemas
- Remove some over-zealous Requires that are already picked up by rpm.
- Resolves #571658

* Mon Mar 01 2010 Richard Hughes <richard@hughsie.com> 2.29.4-1
- New upstream release.

* Mon Feb 22 2010 Richard Hughes <richard@hughsie.com> 2.29.4-0.1.20100222
- Another new snapshot from upstream with lots of bugs fixed from the Fedora
  test day.

* Thu Feb 18 2010 Richard Hughes <richard@hughsie.com> 2.29.4-0.1.20100218
- Another new snapshot from upstream for the Fedora test day.

* Wed Feb 17 2010 Richard Hughes <richard@hughsie.com> 2.29.4-0.1.20100217
- New snapshot from upstream for the Fedora test day.

* Mon Feb 01 2010 Richard Hughes <richard@hughsie.com> 2.29.3-1
- New upstream release.

* Mon Jan 18 2010 Matthias Clasen <mclasen@redhat.com> 2.29.2-3
- Rebuild against new gnome-desktop

* Mon Jan 04 2010 Richard Hughes <richard@hughsie.com> 2.29.2-2
- Rebuild, hopefully koji has now a working glibc.

* Mon Jan 04 2010 Richard Hughes <richard@hughsie.com> 2.29.2-1
- New upstream release.

* Fri Dec 04 2009 Richard Hughes <richard@hughsie.com> 2.29.1-1
- Initial spec for review.

