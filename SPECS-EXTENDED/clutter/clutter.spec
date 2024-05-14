%global glib2_version 2.53.4
%global cogl_version 1.21.2
%global json_glib_version 0.12.0
%global cairo_version 1.14.0
%global libinput_version 0.19.0
Summary:        Open Source software library for creating rich graphical user interfaces
Name:           clutter
Version:        1.26.4
Release:        10%{?dist}
License:        LGPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://www.clutter-project.org/
Source0:        https://download.gnome.org/sources/%{name}/1.26/%{name}-%{version}.tar.xz
BuildRequires:  gettext
BuildRequires:  make
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(atk)
BuildRequires:  pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires:  pkgconfig(cogl-1.0) >= %{cogl_version}
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 1.39.0
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libinput) >= %{libinput_version}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xkbcommon)
Requires:       cairo%{?_isa} >= %{cairo_version}
Requires:       cogl%{?_isa} >= %{cogl_version}
Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       json-glib%{?_isa} >= %{json_glib_version}
Requires:       libinput%{?_isa} >= %{libinput_version}
Recommends:     mesa-dri-drivers%{?_isa}

%description
Clutter is an open source software library for creating fast,
visually rich graphical user interfaces. The most obvious example
of potential usage is in media center type applications.
We hope however it can be used for a lot more.

%package        devel
Summary:        Clutter development environment
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Header files and libraries for building a extension library for the
clutter

%package        doc
Summary:        Documentation for %{name}
Requires:       %{name} = %{version}-%{release}

%description    doc
Clutter is an open source software library for creating fast,
visually rich graphical user interfaces. The most obvious example
of potential usage is in media center type applications.
We hope however it can be used for a lot more.

This package contains documentation for clutter.

%package        tests
Summary:        Tests for the clutter package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tests
The clutter-tests package contains tests that can be used to verify
the functionality of the installed clutter package.

%prep
%autosetup -p1

%build
%configure \
	--enable-xinput \
        --enable-gdk-backend \
	--enable-installed-tests \
        --enable-egl-backend \
        --enable-evdev-input \
        --enable-wayland-backend \
        --enable-wayland-compositor

%make_build

%install
%make_install

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete -print

%find_lang clutter-1.0

%files -f clutter-1.0.lang
%doc NEWS README.md
%license COPYING
%{_libdir}/*.so.0
%{_libdir}/*.so.0.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/*.typelib

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%dir %{_datadir}/clutter-1.0
%dir %{_datadir}/clutter-1.0/valgrind
%{_datadir}/clutter-1.0/valgrind/clutter.supp
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/*.gir

%files doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/clutter

%files tests
%{_libexecdir}/installed-tests/clutter
%{_datadir}/installed-tests

%changelog
* Thu Jan 05 2023 Sumedh Sharma <sumsharma@microsoft.com> - 1.26.4-10
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 09 2021 Jeff Law <jlaw@tachyum.com> - 1.26.4-6
- Re-enable LTO

* Tue Apr 13 2021 Kalev Lember <klember@redhat.com> - 1.26.4-5
- Recommend rather than require mesa-dri-drivers
- Avoid hard requiring gobject-introspection

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 1.26.4-2
- Disable LTO

* Mon Mar 09 2020 Kalev Lember <klember@redhat.com> - 1.26.4-1
- Update to 1.26.4
- Include clutter.supp valgrind suppression file
- Fix issues with various unowned directories

* Tue Mar 03 2020 Kalev Lember <klember@redhat.com> - 1.26.2-11
- Backport fixes for 10-bit color (#1800865)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 18 2018 Kalev Lember <klember@redhat.com> - 1.26.2-6
- Remove wayland conditionals
- Require mesa-dri-drivers (#1568881)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.26.2-4
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri May 12 2017 Kalev Lember <klember@redhat.com> - 1.26.2-1
- Update to 1.26.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 1.26.0-1
- Update to 1.26.0

* Fri Feb 19 2016 David King <amigadave@amigadave.com> - 1.25.6-1
- Update to 1.25.6 (#1310079)
- Use pkgconfig for BuildRequires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Kalev Lember <klember@redhat.com> - 1.25.4-1
- Update to 1.25.4

* Thu Dec 17 2015 Kalev Lember <klember@redhat.com> - 1.25.2-1
- Update to 1.25.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 1.24.2-1
- Update to 1.24.2

* Tue Sep 15 2015 Kalev Lember <klember@redhat.com> - 1.24.0-1
- Update to 1.24.0

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 1.23.6-1
- Update to 1.23.6

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 1.23.4-2
- Re-enable parallel make
- Use make_install macro

* Thu Jul 23 2015 Florian Müllner <fmuellner@redhat.com> - 1.23.4-1
- Update to 1.23.4

* Tue Jun 30 2015 Kalev Lember <klember@redhat.com> - 1.23.2-2
- Add minimum version requirements for a few deps

* Mon Jun 29 2015 Kalev Lember <klember@redhat.com> - 1.23.2-1
- Update to 1.23.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.22.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 17 2015 Kalev Lember <kalevlember@gmail.com> - 1.22.2-2
- x11: Fix touchpad detection (#1206961)

* Tue May 12 2015 Kalev Lember <kalevlember@gmail.com> - 1.22.2-1
- Update to 1.22.2

* Thu May 07 2015 Kalev Lember <kalevlember@gmail.com> - 1.22.0-2
- gdk: Use RGBA visual if there is one (#1206960)

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 1.22.0-1
- Update to 1.22.0

* Sun Mar 15 2015 Kalev Lember <kalevlember@gmail.com> - 1.21.8-1
- Update to 1.21.8
- Use %%license macro for the COPYING file

* Tue Mar 10 2015 Peter Hutterer <peter.hutterer@redhat.com> - 1.21.6-2
- Rebuild for libinput soname bump

* Tue Mar 03 2015 Kalev Lember <kalevlember@gmail.com> - 1.21.6-1
- Update to 1.21.6

* Thu Jan 22 2015 Florian Müllner <fmuellner@redhat.com> - 1.21.4-1
- Do not run "make check" (which requires access to an X display)

* Thu Jan 22 2015 Florian Müllner <fmuellner@redhat.com> - 1.21.4-1
- Update to 1.21.4

* Mon Jan 19 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.21.2-3
- Run autoreconf

* Mon Jan 19 2015 Peter Hutterer <peter.hutterer@redhat.com> 1.21.2-2
- Update to libinput 0.8

* Thu Dec 18 2014 Richard Hughes <rhughes@redhat.com> - 1.21.2-1
- Update to 1.21.2

* Tue Oct 28 2014 Richard Hughes <rhughes@redhat.com> - 1.20.0-3
- Fix compile when not using Wayland, harder.

* Tue Oct 28 2014 Richard Hughes <rhughes@redhat.com> - 1.20.0-2
- Fix compile when not using Wayland.

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.20.0-1
- Update to 1.20.0

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 1.19.10-1
- Update to 1.19.10

* Fri Sep 12 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.19.8-2
- Rebuild for libinput soname bump

* Thu Aug 21 2014 Kalev Lember <kalevlember@gmail.com> - 1.19.8-1
- Update to 1.19.8

* Wed Aug 20 2014 Kalev Lember <kalevlember@gmail.com> - 1.19.6-3
- Backport an upstream patch for setting xkb layout index

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Kalev Lember <kalevlember@gmail.com> - 1.19.6-1
- Update to 1.19.6

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.19.4-4
- Rebuilt for gobject-introspection 1.41.4

* Fri Jul 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.19.4-2
- Enable make check
- Build installed tests (thanks Vadim Rutkovsky) RHBZ 1117375
- Drop old obsoletes

* Wed Jun 25 2014 Richard Hughes <rhughes@redhat.com> - 1.19.4-1
- Update to 1.19.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Florian Müllner <fmuellner@redhat.com> - 1.19.2-1
- Update to 1.19.2

* Tue Apr 15 2014 Kalev Lember <kalevlember@gmail.com> - 1.18.2-1
- Update to 1.18.2

* Wed Mar 19 2014 Florian Müllner <fmuellner@redhat.com> - 1.18.0-1
- Update to 1.18.0

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 1.17.6-1
- Update to 1.17.6

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 1.17.4-1
- Update to 1.17.4

* Sun Feb 09 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.17.2-2
- Rebuild for libevdev soname bump

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 1.17.2-1
- Update to 1.17.2

* Wed Jan 29 2014 Richard Hughes <rhughes@redhat.com> - 1.16.4-1
- Update to 1.16.4

* Thu Dec 26 2013 Adam Williamson <awilliam@redhat.com> - 1.16.2-4
- backport upstream patch to stop using deprecated libevdev functions

* Mon Dec  9 2013 Matthias Clasen <mclasen@redhat.com> - 1.16.2-3
- A followup fix to the previous changes

* Tue Nov 26 2013 Matthias Clasen <mclasen@redhat.com> - 1.16.2-2
- Avoid excessive redraws when windows are moved in gnome-shell

* Thu Nov 21 2013 Richard Hughes <rhughes@redhat.com> - 1.16.2-1
- Update to 1.16.2

* Mon Oct 07 2013 Adam Jackson <ajax@redhat.com> 1.16.0-2
- Fix touchpads to not warp to bizarre places on initial touch.

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 1.16.0-1
- Update to 1.16.0

* Fri Sep 20 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.96-1
- Update to 1.15.96

* Fri Sep 20 2013 Matthias Clasen <mclasen@redhat.com> - 1.15.94-2
- Fix a shell crash

* Thu Sep 19 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.94-1
- Update to 1.15.94

* Thu Sep 12 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.92-3
- Add missing build deps

* Thu Sep 12 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.92-2
- Add configure options that are needed to enable the gnome-shell
  Wayland compositor

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.92-1
- Update to 1.15.92

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.90-1
- Update to 1.15.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 1.15.2-1
- Update to 1.15.2
- Dropped upstream patches
- Backport patches for wayland / cogl 1.15.4 API changes

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 23 2013 Matthias Clasen <mclasen@redhat.com> - 1.14.4-3
- Backport another upstream patch for gnome-shell crashes (#954054)

* Fri May 17 2013 Kalev Lember <kalevlember@gmail.com> - 1.14.4-2
- Backport an upstream patch for frequent gnome-shell crashes (#827158)

* Wed May 15 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.14.4-1
- Update to 1.14.4

* Wed Apr 17 2013 Richard Hughes <rhughes@redhat.com> - 1.14.2-1
- Update to 1.14.2

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 1.14.0-1
- Update to 1.14.0

* Tue Mar 19 2013 Matthias Clasen <mclasen@redhat.com> - 1.13.10-1
- Update to 1.13.10

* Thu Mar 14 2013 Bastien Nocera <bnocera@redhat.com> 1.13.8-4
- Prefer the X11 backend to the Wayland one, and enable wayland

* Thu Mar 14 2013 Matthias Clasen <mclasen@redhat.com> 1.13.8-3
- Enabling Wayland broke the login screen, so disable for now

* Wed Mar 13 2013 Matthias Clasen <mclasen@redhat.com> 1.13.8-2
- Enable Wayland backend

* Tue Mar  5 2013 Matthias Clasen <mclasen@redhat.com> 1.13.8-1
- Update to 1.13.8

* Thu Feb 21 2013 Bastien Nocera <bnocera@redhat.com> 1.13.6-1
- Update to 1.13.6

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 1.13.4-4
- Backport a patch to use XI2.3, so that clutter keeps working with gtk+ 3.7.8

* Wed Jan 30 2013 Matthias Clasen <mclasen@redhat.com> - 1.13.4-3
- Fix a gnome-shell crash

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.13.4-2
- Rebuild for new cogl

* Wed Jan 16 2013 Matthias Clasen <mclasen@redhat.com> - 1.13.4-1
- Update to 1.13.4

* Tue Dec 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.13.2-1
- Update to 1.13.2

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 1.12.2-1
- Update to 1.12.2

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 1.12.0-2
- Obsolete clutter-gtk010 and clutter-sharp as well

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 1.12.0-1
- Update to 1.12.0
- Obsolete pyclutter, -gst and -gtk packages

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.11.16-1
- Update to 1.11.16

* Wed Sep 05 2012 Kalev Lember <kalevlember@gmail.com> - 1.11.14-2
- Rebuilt with gobject-introspection 1.33.10 (bgo #682124)

* Mon Sep  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.11.14-1
- Update to 1.11.12

* Tue Aug 28 2012 Matthias Clasen <mclasen@redhat.com> - 1.11.12-3
- Rebuild against new cogl

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 1.11.12-1
- Update to 1.11.12

* Tue Aug  7 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.11.10-1
- Update to 1.11.10

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.11.8-1
- Update to 1.11.8

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 1.11.6-1
- Update to 1.11.6

* Tue Jun  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.11.4-1
- Update to 1.11.4

* Thu May 10 2012 Kalev Lember <kalevlember@gmail.com> - 1.11.2-1
- Update to 1.11.2

* Thu May 03 2012 Bastien Nocera <bnocera@redhat.com> 1.10.4-2
- Add patches to fix crashes with touch events

* Tue May  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.10.4-1
- Update to 1.10.4

* Tue Apr 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.10.2-1
- Update to 1.10.2

* Thu Apr 12 2012 Peter Hutterer <peter.hutterer@redhat.com> 1.10.0-5
- Fix misnamed define to enable XI 2.2 support (#809864)

* Fri Apr 06 2012 Zeeshan Ali <zeenix@redhat.com> - 1.10.0-4
- Include layout fix (Needed by gnome-boxes at least).

* Wed Apr 04 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.0-3
- Obsolete clutter-gesture and clutter-imcontext packages (#809864)

* Thu Mar 29 2012 Kalev Lember <kalevlember@gmail.com> - 1.10.0-2
- Build with xi2.2 support (#803430)
- Enable the GDK backend

* Thu Mar 22 2012 Matthias Clasen <mclasen@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 1.9.16-1
- Update to 1.9.16

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.14-1
- Update to 1.9.14

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.12-1
- Update to 1.9.12

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.10-1
- Update to 1.9.10

* Wed Jan 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.8-1
- 1.9.8 release
- https://ftp.gnome.org/pub/GNOME/sources/clutter/1.9/clutter-1.9.8.news
- Back to tar file releases

* Sat Jan 21 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.7-0.1.20120121
- A snapshot that may now really work with gnome-shell

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 1.9.6-1
- 1.9.6 release
- https://ftp.gnome.org/pub/GNOME/sources/clutter/1.9/clutter-1.9.6.news
- Should work with gnome-shell again

* Wed Jan 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.4-1
- 1.9.4 release
- https://ftp.gnome.org/pub/GNOME/sources/clutter/1.9/clutter-1.9.4.news

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.9.2-1
- Update to 1.9.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-2
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.2-1
- 1.8.2 stable release
- https://ftp.gnome.org/pub/GNOME/sources/clutter/1.8/clutter-1.8.2.news

* Mon Sep 19 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.8.0-1
- 1.8.0 stable release
- https://ftp.gnome.org/pub/GNOME/sources/clutter/1.8/clutter-1.8.0.news

* Mon Sep 12 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.90-1
- Update to 1.7.90
- https://ftp.gnome.org/pub/GNOME/sources/clutter/1.7/clutter-1.7.90.news

* Mon Sep  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.14-1
- Update to 1.7.14

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.12-1
- Update to 1.7.12

* Thu Aug 18 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.10-1
- Update to 1.7.10

* Mon Aug 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.8-1
- Update to 1.7.8

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 1.7.6-1
- Update to 1.7.6

* Mon Jul  4 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.7.4-1
- Update to 1.7.4 devel build
- Build against cogl
- Add patch to fix DSO linking

* Fri Jun 24 2011 Adam Jackson <ajax@redhat.com> 1.6.16-3
- clutter-1.6.16-no-drm-hax.patch: Remove the insane DRM-banging fallback for
  sync to vblank.

* Fri Jun 17 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.6.16-2
- Fix G_CONST_RETURN usage

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.6.16-1
- Update to 1.6.16

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> - 1.6.14-1
- Update to 1.6.14

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 1.6.12-1
- Update to 1.6.12

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 1.6.10-1
- Update to 1.6.10

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 1.6.8-1
- Update to 1.6.8

* Wed Mar  2 2011 Matthias Clasen <mclasen@redhat.com> - 1.6.6-2
- Fix icon corruption in gnome-shell

* Mon Feb 21 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.6-1
- Update to 1.6.6

* Mon Feb 14 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.4-1
- Update to 1.6.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Mon Jan 31 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Mon Jan 24 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.14-1
- Update to 1.5.14

* Wed Jan 12 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.12-1
- Update to 1.5.12

* Tue Dec 28 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.10-1
- Update to 1.5.10

* Mon Dec  6 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 1.5.8-3
- Drop unneeded gtk2-devel builddep that causes issues for gtk3 clutter apps
- Add the independent deps that were pulled in by gtk2-devel

* Mon Nov 29 2010 Owen Taylor <otaylor@redhat.com> - 1.5.8-2
- Update to 1.5.8
- Add cairo-gobject-devel dependency
- Drop unneeded patches

* Mon Nov 22 2010 Dan Williams <dcbw@redhat.com> - 1.4.0-4
- Add a patch cherry-picked from upstream for
  https://bugzilla.clutter-project.org/attachment.cgi?id=2366
  (gnome-shell/mutter hang when gnome-settings-daemon restarts)

* Tue Oct  5 2010 Owen Taylor <otaylor@redhat.com> - 1.4.0-3
- Add a patch cherry-picked from upstream for
  https://bugzilla.clutter-project.org/show_bug.cgi?id=2324
  (gnome-shell crashes on root background changes)

* Wed Sep 29 2010 jkeating - 1.4.0-2
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.0-1
- Update to stable 1.4.0 release

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> - 1.3.14-1
- Update to 1.3.14

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 1.3.12-2
- Rebuild against newer gobject-introspection

* Tue Aug 31 2010 Colin Walters <walters@verbum.org> - 1.3.12-1
- New upstream

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 1.2.10-3
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 1.2.10-2
- Rebuild against new gobject-introspection

* Sun Jul 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.10-1
- Update to new upstream stable 1.2.10 release

* Tue Jul  6 2010 Colin Walters <walters@verbum.org> - 1.2.8-4
- Changes to support git snapshot builds

* Thu Jul  1 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.2.8-3
- Rebuild for "Incompatible version 1.0 (supported: 1.1)"
  for introspection file

* Thu Jun 10 2010 Colin Walters <walters@verbum.org> 1.2.8-2
- Drop gir-repository dependency, we don't need it anymore 

* Sat May 15 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.8-1
- Update to new upstream stable 1.2.8 release
- Drop upstreamed patches

* Fri Apr 30 2010 Owen Taylor <otaylor@redhat.com> 1.2.6-1
- Update to new upstream stable 1.2.6 release
- Work around Radeon driver problem with color channel confusion.
- Fix Mutter not seeing BufferSwapComplete events and freezing
- Remove incorrect warning message about BufferSwapComplete events

* Tue Mar 20 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.4-1
- Update to new upstream stable 1.2.4 release

* Mon Mar 15 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.2-1
- Update to new upstream stable 1.2.2 release

* Tue Mar  2 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.0-1
- Update to new upstream stable 1.2.0 release

* Sun Feb 28 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.14-1
- Update to 1.1.14

* Wed Feb 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.10-2
- Add patch to fix 64bit build 

* Wed Feb 11 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.10-1
- Update to 1.1.10

* Thu Feb  4 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.6-1
- Update to 1.1.6

* Thu Jan  7 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.8-2
- A few minor spec cleanups

* Mon Jan  4 2010 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.8-1
- Update to 1.0.8

* Tue Sep 22 2009 Bastien Nocera <bnocera@redhat.com> 1.0.6-1
- Update to 1.0.6

* Sun Aug 30 2009 Owen Taylor <otaylor@redhat.com> - 1.0.4-1
- Update to 1.0.4, update gobject-introspection requirement

* Fri Aug 14 2009 Bastien Nocera <bnocera@redhat.com> 1.0.2-1
- Update to 1.0.2

* Sun Aug  1 2009 Matthias Clasen <mclasen@redhat.com> 1.0.0-4
- Move ChangeLog to -devel to save some space

* Fri Jul 31 2009 Matthias Clasen <mclasen@redhat.com> 1.0.0-3
- Drop the gir-repository-devel dep, which pulls a bunch of -devel
  onto the live cd

* Wed Jul 29 2009 Bastien Nocera <bnocera@redhat.com> 1.0.0-1
- Update to 1.0.0

* Tue Jul 28 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.9.8-3
- fix bz #507389

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Bastien Nocera <bnocera@redhat.com> 0.9.8-1
- Update to 0.9.8

* Fri Jul 17 2009 Bastien Nocera <bnocera@redhat.com> 0.9.6-2
- Patch from Owen Taylor <otaylor@redhat.com> to add gobject-
  introspection support to clutter (#512260)

* Fri Jul 10 2009 Bastien Nocera <bnocera@redhat.com> 0.9.6-1
- Update to 0.9.6

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 0.9.4-1
- Update to 0.9.4

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 0.9.2-1
- Update to 0.9.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Allisson Azevedo <allisson@gmail.com> 0.8.6-3
- Remove noarch from doc subpackage

* Wed Jan 21 2009 Allisson Azevedo <allisson@gmail.com> 0.8.6-2
- Added gtk-doc for cogl
- Created doc subpackage

* Wed Jan 21 2009 Allisson Azevedo <allisson@gmail.com> 0.8.6-1
- Update to 0.8.6

* Mon Oct  6 2008 Allisson Azevedo <allisson@gmail.com> 0.8.2-1
- Update to 0.8.2
- Removed clutter-0.8.0-clutter-fixed.patch

* Sat Sep  6 2008 Allisson Azevedo <allisson@gmail.com> 0.8.0-1
- Update to 0.8.0
- Added clutter-0.8.0-clutter-fixed.patch

* Sat Jun 14 2008 Allisson Azevedo <allisson@gmail.com> 0.6.4-1
- Update to 0.6.4

* Sat May 17 2008 Allisson Azevedo <allisson@gmail.com> 0.6.2-1
- Update to 0.6.2

* Tue Feb 19 2008 Allisson Azevedo <allisson@gmail.com> 0.6.0-1
- Update to 0.6.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.4.2-2
- Autorebuild for GCC 4.3

* Wed Oct  3 2007 Allisson Azevedo <allisson@gmail.com> 0.4.2-1
- Update to 0.4.2

* Mon Sep  3 2007 Allisson Azevedo <allisson@gmail.com> 0.4.1-1
- Update to 0.4.1

* Sat Jul 21 2007 Allisson Azevedo <allisson@gmail.com> 0.3.1-1
- Update to 0.3.1

* Thu Apr 12 2007 Allisson Azevedo <allisson@gmail.com> 0.2.3-1
- Update to 0.2.3

* Sun Mar 28 2007 Allisson Azevedo <allisson@gmail.com> 0.2.2-4
- Changed buildrequires and requires

* Sun Mar 27 2007 Allisson Azevedo <allisson@gmail.com> 0.2.2-3
- Fix .spec

* Sun Mar 24 2007 Allisson Azevedo <allisson@gmail.com> 0.2.2-2
- Fix .spec

* Sun Mar 23 2007 Allisson Azevedo <allisson@gmail.com> 0.2.2-1
- Initial RPM release
