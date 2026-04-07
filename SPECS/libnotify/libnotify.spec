# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define glib2_version 2.38.0

Name:           libnotify
Version:        0.8.8
Release:        1%{?dist}
Summary:        Desktop notification library

License:        LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/libnotify
Source0:        https://download.gnome.org/sources/libnotify/0.8/%{name}-%{version}.tar.xz

BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  docbook-xsl-ns
BuildRequires:  gi-docgen
BuildRequires:  meson
BuildRequires:  xmlto
BuildRequires:  /usr/bin/xsltproc

Requires:       glib2%{?_isa} >= %{glib2_version}

%description
libnotify is a library for sending desktop notifications to a notification
daemon, as defined in the freedesktop.org Desktop Notifications spec. These
notifications can be used to inform the user about an event or display some
form of information without getting in the user's way.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files needed for
development of programs using %{name}.

%prep
%autosetup -p1

%build
%meson -Dtests=false
%meson_build

%install
%meson_install

%files
%license COPYING
%doc NEWS AUTHORS README.md
%{_bindir}/notify-send
%{_libdir}/libnotify.so.*
%{_libdir}/girepository-1.0/Notify-0.7.typelib
%{_mandir}/man1/notify-send.1*

%files devel
%dir %{_includedir}/libnotify
%{_includedir}/libnotify/*
%{_libdir}/libnotify.so
%{_libdir}/pkgconfig/libnotify.pc
%{_datadir}/gir-1.0/Notify-0.7.gir
%{_docdir}/libnotify-0/
%doc %{_docdir}/libnotify/spec/

%changelog
* Thu Jan 22 2026 Barry Dunn <badunn@redhat.com> - 0.8.8-1
- Update to 0.8.8

* Fri Sep 26 2025 Petr Schindler <pschindl@redhat.com> - 0.8.7-1
- Update to 0.8.7

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 31 2025 nmontero <nmontero@redhat.com> - 0.8.6-1
- Update to 0.8.6

* Mon Mar 03 2025 nmontero <nmontero@redhat.com> - 0.8.4-1
- Update to 0.8.4

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 21 2023 Kalev Lember <klember@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Feb 20 2023 David King <amigadave@amigadave.com> - 0.8.2-1
- Update to 0.8.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Kalev Lember <klember@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Thu May 05 2022 David King <amigadave@amigadave.com> - 0.7.12-1
- Update to 0.7.12

* Thu Apr 28 2022 David King <amigadave@amigadave.com> - 0.7.11-1
- Update to 0.7.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 David King <amigadave@amigadave.com> - 0.7.9-6
- Use pkgconfig for BuildRequires
- Disable building unused tests

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 26 2020 Kalev Lember <klember@redhat.com> - 0.7.9-1
- Update to 0.7.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 0.7.8-2
- Rebuild with Meson fix for #1699099

* Sat Apr 06 2019 Kalev Lember <klember@redhat.com> - 0.7.8-1
- Update to 0.7.8
- Switch to the meson build system
- Build DocBook documentation

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 14 2016 Kalev Lember <klember@redhat.com> - 0.7.7-1
- Update to 0.7.7
- Remove lib64 rpaths
- Don't set group tags
- Use make_install macro
- Don't manually set deps that pkgconfig dep extractor automatically does
- Drop old, unused build deps
- Tighten deps with the _isa macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> - 0.7.6-6
- Drop the dependency on desktop-notification-daemon
- Use license macro for the COPYING file

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.7.6-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.7.6-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 04 2013 Kalev Lember <kalevlember@gmail.com> - 0.7.6-1
- Update to 0.7.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 0.7.5-5
- Fix RHBZ #925824
- Update source URL
- Fix mix of spaces and tabs in spec file
- Fix bogus changelog date

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Ville Skyttä <ville.skytta@iki.fi> - 0.7.5-2
- Fix glib2 dependency version.

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 0.7.5-1
- Update to 0.7.5

* Sun Mar  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.7.4-2
- Merge newer F-16 version into rawhide

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.4-1
- Update to 0.7.4

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1
- Enable introspection

* Mon Jan  3 2011 Bill Nottingham <notting@redhat.com> - 0.7.0-2
- unbreak firefox and similar apps that free pixbufs they send to set_image_from_pixbuf (#654628)

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 0.7.0-1
- Update to 0.7.0

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Tue Jun 29 2010 Bastien Nocera <bnocera@redhat.com> 0.5.1-1
- Update to 0.5.1

* Mon Jun 28 2010 Bastien Nocera <bnocera@redhat.com> 0.5.0-1
- Update to 0.5.0

* Wed Nov 11 2009 Matthias Clasen <mclasen@redhat.com> - 0.4.5-4
- Close notifications with non-default actions on uninit

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.4.5-1
- Update to 0.4.5
- Drop obsolete patches
- Tweak %%summary and %%description

* Sat Aug 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.4.4-12
- Handle extra parameter of the closed signal

* Tue Jun 10 2008 Colin Walters <walters@redhat.com> - 0.4.4-11
- Add patch neccessary for reliable notification positioning

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.4-10
- Autorebuild for GCC 4.3

* Tue Oct 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-9
- Rebuild against new dbus-glib

* Wed Oct 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-8
- Rebuild

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-7
- Update licence field

* Wed Jun  6 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-6
- Re-add notification-daemon requirement again

* Tue Jun  5 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-5
- Temporarily remove the notification-daemon requires 
  for bootstrapping

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-4
- Re-add notification-daemon requirement

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-3
- Temporarily remove the notification-daemon requires 
  for bootstrapping

* Sun Mar 25 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-2
- Require gtk2-devel in the -devel package (#216946)

* Fri Mar 23 2007 Matthias Clasen <mclasen@redhat.com> - 0.4.4-1
- Update to 0.4.4, which contains important bug fixes 
  and memory leak fixes
- Require pkgconfig in the -devel package

* Sat Dec  9 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.3-2
- Another typo (#214275)

* Sat Nov 11 2006 Ray Strode <rstrode@redhat.com> - 0.4.3-1
- Update 0.4.3

* Tue Nov  7 2006 Matthias Clasen <mclasen@redhat.com> - 0.4.2-5
- Fix typos in the spec (#214275)
 
* Sun Sep 17 2006 Christopher Aillon <caillon@redhat.com> - 0.4.2-4
- Add upstream patch (r2899) to correct an invalid assertion when
  creating notifications using status icons

* Tue Aug 15 2006 Luke Macken <lmacken@redhat.com> - 0.4.2-3
- Add upstream patch libnotify-0.4.2-status-icon.patch to emit the correct
  property change notification 'status-icon' instead of 'attach-icon'

* Fri Jul 21 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.2-2
- Add developer docs to the devel section

* Fri Jul 21 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.2-1
- Update to upstream version 0.4.2
- Add dist tag to release
- Add Requires to devel package

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-3.2
- reinstate desktop-notification dependency

* Wed Jul 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-3.1
- comment out desktop-notification dependency so we can build the
  notification daemon

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-3
- Add BR on dbus-glib-devel

* Thu Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 0.4.0-2
- rebuild
- add missing brs

* Fri May 19 2006 John (J5) Palmieri <johnp@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Sat Mar 11 2006 Bill Nottingham <notting@redhat.com> - 0.3.0-6
- define %%{glib2_version} if it's in a requirement

* Thu Mar  2 2006 Ray Strode <rstrode@redhat.com> - 0.3.0-5
- patch out config.h include from public header

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-4.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.3.0-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Jan 12 2006 Christopher Aillon <caillon@redhat.com> - 0.3.0-4
- Require a desktop-notification-daemon to be present.  Currently,
  this is notify-daemon, but libnotify doesn't specifically require
  that one.  Require 'desktop-notification-daemon' which daemons
  providing compatible functionality are now expected to provide.

* Wed Jan 11 2006 Christopher Aillon <caillon@redhat.com> - 0.3.0-3
- Let there be libnotify-devel...

* Tue Nov 15 2005 John (J5) Palmieri <johnp@redhat.com> - 0.3.0-2
- Actual release of the 0.3.x series

* Tue Nov 15 2005 John (J5) Palmieri <johnp@redhat.com> - 0.3.0-1
- Bump version to not conflict with older libnotify libraries

* Tue Nov 15 2005 John (J5) Palmieri <johnp@redhat.com> - 0.0.2-1
- inital build
