# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global libadwaita_version 1.6~beta
%global gtk4_version 4.15.2

%global tarball_version %%(echo %{version} | tr '~' '.')

Name:		gnome-bluetooth
Epoch:		1
Version:	47.1
Release:	3%{?dist}
Summary:	Bluetooth graphical utilities

License:	GPL-2.0-or-later
URL:		https://wiki.gnome.org/Projects/GnomeBluetooth
Source0:	https://download.gnome.org/sources/gnome-bluetooth/47/gnome-bluetooth-%{tarball_version}.tar.xz
# https://gitlab.gnome.org/GNOME/gnome-bluetooth/-/merge_requests/223
Patch0:         0001-tests-Fix-meson-setup-with-pygobject.patch

%if 0%{?rhel}
ExcludeArch:	s390 s390x
%endif

BuildRequires:	gettext
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	meson
BuildRequires:	pkgconfig(gsound)
BuildRequires:	pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:	pkgconfig(libadwaita-1) >= %{libadwaita_version}
BuildRequires:	pkgconfig(libnotify)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(upower-glib)
BuildRequires:	python3-dbusmock >= 0.25.0-1

Provides:	dbus-bluez-pin-helper

# Otherwise we might end up with mismatching version
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	bluez >= 5.0
Requires:	gtk4 >= %{gtk4_version}
Requires:	libadwaita >= %{libadwaita_version}
%ifnarch s390 s390x
Requires:	pulseaudio-module-bluetooth
Requires:	bluez-obexd
%endif

%description
The gnome-bluetooth package contains graphical utilities to setup,
monitor and use Bluetooth devices.

%package libs
Summary:	GTK+ Bluetooth device selection widgets
License:	LGPL-2.1-or-later

%description libs
This package contains libraries needed for applications that
want to display a Bluetooth device selection widget.

%package libs-devel
Summary:	Development files for %{name}-libs
License:	LGPL-2.1-or-later
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description libs-devel
This package contains the libraries and header files that are needed
for writing applications that require a Bluetooth device selection widget.

%prep
%autosetup -p1 -n %{name}-%{tarball_version}

%build
%meson -Dgtk_doc=true
%meson_build

%install
%meson_install

%find_lang gnome-bluetooth-3.0

%files
%license COPYING
%doc README.md NEWS
%{_bindir}/bluetooth-sendto
%{_datadir}/applications/*.desktop
%{_datadir}/gnome-bluetooth-3.0/
%{_mandir}/man1/*

%files -f gnome-bluetooth-3.0.lang libs
%license COPYING.LIB
%{_libdir}/libgnome-bluetooth-3.0.so.*
%{_libdir}/libgnome-bluetooth-ui-3.0.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GnomeBluetooth-3.0.typelib

%files libs-devel
%{_includedir}/gnome-bluetooth-3.0/
%{_libdir}/libgnome-bluetooth-3.0.so
%{_libdir}/libgnome-bluetooth-ui-3.0.so
%{_libdir}/pkgconfig/gnome-bluetooth-3.0.pc
%{_libdir}/pkgconfig/gnome-bluetooth-ui-3.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GnomeBluetooth-3.0.gir
%{_datadir}/gtk-doc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:47.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:47.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 07 2024 Bastien Nocera <bnocera@redhat.com> - 47.1-1
- Update to 47.1

* Mon Sep 16 2024 nmontero <nmontero@redhat.com> - 1:47.0-1
- Update to 47.0

* Fri Aug 30 2024 David King <amigadave@amigadave.com> - 1:47~rc-1
- Update to 47.rc

* Sun Aug 04 2024 David King <amigadave@amigadave.com> - 1:47~beta-1
- Update to 47.beta

* Fri Jul 19 2024 David King <amigadave@amigadave.com> - 47~alpha-1
- Update to 47.alpha

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:46.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 19 2024 David King <amigadave@amigadave.com> - 1:46.0-1
- Update to 46.0

* Sat Feb 10 2024 David King <amigadave@amigadave.com> - 1:46~beta-1
- Update to 46.beta

* Tue Feb 06 2024 David King <amigadave@amigadave.com> - 1:42.8-1
- Update to 42.8

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:42.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:42.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 16 2023 Kalev Lember <klember@redhat.com> - 1:42.7-1
- Update to 42.7

* Mon Aug 14 2023 Kalev Lember <klember@redhat.com> - 1:42.6-1
- Update to 42.6

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:42.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 16 2023 David King <amigadave@amigadave.com> - 1:42.5-3
- Use pkgconfig for BuildRequires

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:42.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Bastien Nocera <bnocera@redhat.com> - 42.5-1
- Update to 42.5

* Tue Nov 08 2022 Bastien Nocera <bnocera@redhat.com> - 42.4-3
- Require bluez-obexd (#2090443)

* Tue Sep 06 2022 Kalev Lember <klember@redhat.com> - 42.4-2
- Rebuild to include in GNOME 43.rc mega-update

* Mon Sep 05 2022 Bastien Nocera <bnocera@redhat.com> - 42.4-1
+ gnome-bluetooth-42.4-1
- Update to 42.4

* Wed Aug 24 2022 Bastien Nocera <bnocera@redhat.com> - 42.3-1
+ gnome-bluetooth-42.3-1
- Update to 42.3

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:42.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Bastien Nocera <bnocera@redhat.com> - 42.2-1
+ gnome-bluetooth-42.2-1
- Update to 42.2

* Thu Jun 09 2022 Bastien Nocera <bnocera@redhat.com> - 42.1-1
+ gnome-bluetooth-42.1-1
- Update to 42.1

* Fri Mar 18 2022 Bastien Nocera <bnocera@redhat.com> - 42.0-1
+ gnome-bluetooth-42.0-1
- Update to 42.0

* Thu Mar 10 2022 David King <amigadave@amigadave.com> - 42~rc-1
- Update to 42.rc

* Wed Feb 23 2022 Bastien Nocera <bnocera@redhat.com> - 42~beta.2-1
+ gnome-bluetooth-42~beta.2-1
- Update to 42.beta.2

* Wed Feb 16 2022 Bastien Nocera <bnocera@redhat.com> - 42~beta-1
+ gnome-bluetooth-42~beta-1
- Update to 42.beta

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.34.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.34.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 23 2021 Bastien Nocera <bnocera@redhat.com> - 3.34.5-1
+ gnome-bluetooth-3.34.5-1
- Update to 3.34.5

* Mon Mar 22 2021 Bastien Nocera <bnocera@redhat.com> - 3.34.4-1
+ gnome-bluetooth-3.34.4-1
- Update to 3.34.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.34.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 01 2020 Bastien Nocera <bnocera@redhat.com> - 3.34.3-1
+ gnome-bluetooth-3.34.3-1
- Update to 3.34.3

* Wed Sep 23 2020 Bastien Nocera <bnocera@redhat.com> - 3.34.2-1
+ gnome-bluetooth-3.34.2-1
- Update to 3.34.2

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.34.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.34.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 09 2020 Bastien Nocera <bnocera@redhat.com> - 3.34.1-1
+ gnome-bluetooth-3.34.1-1
- Update to 3.34.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 06 2019 Kalev Lember <klember@redhat.com> - 1:3.34.0-1
- Update to 3.34.0

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 1:3.33.90-1
- Update to 3.33.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.32.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 1:3.32.1-2
- Rebuild with Meson fix for #1699099

* Fri Mar 29 2019 Kalev Lember <klember@redhat.com> - 1:3.32.1-1
- Update to 3.32.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 1:3.32.0-1
- Update to 3.32.0

* Wed Feb 06 2019 Kalev Lember <klember@redhat.com> - 1:3.31.1-1
- Update to 3.31.1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 01 2018 Bastien Nocera <bnocera@redhat.com> - 3.28.2-1
+ gnome-bluetooth-3.28.2-1
- Update to 3.28.2

* Fri Jul 27 2018 Bastien Nocera <bnocera@redhat.com> - 3.28.1-2
+ gnome-bluetooth-3.28.1-2
- Remove a number of unused BRs
- Remove obexd conditional for RHEL > 7

* Thu Jul 19 2018 Bastien Nocera <bnocera@redhat.com> - 3.28.1-1
+ gnome-bluetooth-3.28.1-1
- Work-around bluez bug that would leave adapters on Discoverable
  when exiting

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 1:3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 1:3.27.92-1
- Update to 3.27.92
- Drop ldconfig scriptlets

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:3.26.1-4
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.26.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:3.26.1-2
- Remove obsolete scriptlets

* Fri Sep 15 2017 Kalev Lember <klember@redhat.com> - 1:3.26.1-1
- Update to 3.26.1

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 1:3.26.0-1
- Update to 3.26.0

* Mon Aug 28 2017 Kalev Lember <klember@redhat.com> - 1:3.25.91-1
- Update to 3.25.91
- Switch to the meson build system

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Kalev Lember <klember@redhat.com> - 1:3.20.1-1
- Update to 3.20.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 1:3.20.0-2
- Update project URLs
- Don't set group tags
- Co-own gir directories
- Require bluez-obexd that got split out
- Drop old obsoletes

* Tue May 24 2016 Bastien Nocera <bnocera@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 1:3.18.3-1
- Update to 3.18.3

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 1:3.18.2-1
- Update to 3.18.2

* Tue Nov 10 2015 Kalev Lember <klember@redhat.com> - 1:3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 1:3.18.0-1
- Update to 3.18.0

* Mon Sep 14 2015 Kalev Lember <klember@redhat.com> - 1:3.17.92-1
- Update to 3.17.92

* Tue Aug 18 2015 Kalev Lember <klember@redhat.com> - 1:3.17.90-2
- Remove libgnome-bluetooth.la file

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 1:3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 19 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.16.1-1
- Update to 3.16.1
- Use license macro for COPYING files
- Tighten deps with the _isa macro

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 1:3.16.0-1
- Update to 3.16.0

* Tue Jan 20 2015 Richard Hughes <rhughes@redhat.com> - 1:3.15.4-1
- Update to 3.15.4

* Sun Nov 16 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.0-3
- Move compat-gnome-bluetooth310-libs obsoletes to -libs subpackage

* Sun Nov 16 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.0-2
- Obsolete compat-gnome-bluetooth310-libs from rhughes-f20-gnome-3-12 copr

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.14.0-1
- Update to 3.14.0

* Mon Aug 18 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1:3.12.0-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 1:3.12.0-1
- Update to 3.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 1:3.11.91-1
- Update to 3.11.91

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 1:3.11.3-1
- Update to 3.11.3

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.91-2
- Drop the dep on gvfs-obexftp

* Tue Sep 10 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.91-1
- Update to 3.9.91

* Sun Aug 18 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.3-4
- Drop an obsolete dep on obexd

* Wed Aug 14 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.3-3
- Require bluez >= 5.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.9.3-1
- Update to 3.9.3

* Mon Jun 03 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.8.1-1
- Update to 3.8.1

* Fri May 10 2013 Adam Williamson <awilliam@redhat.com>
- no reason to update icon cache in %%postun of main package *and* libs

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 1:3.7.92-1
- Update to 3.7.92

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.4-4
- Drop the runtime dep on control-center

* Mon Jan 28 2013 Matthias Clasen <mclasen@redhat.com> - 1:3.7.4-3
- Install the udev rule in /usr/lib

* Sat Jan 26 2013 Kalev Lember <kalevlember@gmail.com> - 1:3.7.4-2
- Spec file cleanup
- Drop the desktop-notification-daemon requires now that the applet is gone
- Fix the build with gcc 4.8
- Move the libgnome-bluetooth-applet.so symlink to the -devel package

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 1:3.7.4-1
- Update to 3.7.4

* Thu Nov 29 2012 Dan Horák <dan[at]danny.cz> - 1:3.6.1-2
- revive on Fedora/s390x, but drop Requires there - it's needed to fulfil compose dependencies

* Thu Nov 15 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 1:3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.92-1
- Update to 3.5.92

* Tue Aug 14 2012 Debarshi Ray <rishi@fedoraproject.org> - 1:3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 20 2012 Richard Hughes <hughsient@gmail.com> - 1:3.5.4-1
- Update to 3.5.4

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 1:3.4.2-1
- Update to 3.4.2

* Tue Jun 12 2012 Bastien Nocera <bnocera@redhat.com> 3.4.1-1
- Update to 3.4.1

* Tue May 08 2012 Bastien Nocera <bnocera@redhat.com> 3.4.0-3
- Don't build on s390

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.4.0-2
- Silence rpm scriptlet output

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 1:3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> 3.3.92-1
- Update to 3.3.92

* Wed Jan 18 2012 Bastien Nocera <bnocera@redhat.com> 3.3.4-1
- Update to 3.3.4
- Moblin code is goner

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Sun Nov 27 2011 Peter Robinson <pbrobinson@fedoraproject.org> -3.3.2-2
- Temporarily add libtool archive to devel package as gnome-shell needs is (for g-i bindings?)

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.2.1-2
- Rebuilt for glibc bug#747377

* Mon Oct 17 2011 Bastien Nocera <bnocera@redhat.com> 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Bastien Nocera <bnocera@redhat.com> 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Bastien Nocera <bnocera@redhat.com> 3.1.92-1
- Update to 3.1.92

* Thu Sep 08 2011 Bastien Nocera <bnocera@redhat.com> 3.1.4-3
- Update to 3.1.4
- Update udev rule again (#733326)

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Fri May 27 2011 Bastien Nocera <bnocera@redhat.com> 3.0.1-1
- Update to 3.0.1

* Mon Apr 04 2011 Bastien Nocera <bnocera@redhat.com> 3.0.0-1
- Update to 3.0.0

* Sat Mar 26 2011 Dan Horák <dan[at]danny.cz> 2.91.92-2
- update BRs when the moblin subpackage is disabled

* Mon Mar 21 2011 Bastien Nocera <bnocera@redhat.com> 2.91.92-1
- Update to 2.91.92

* Tue Mar 08 2011 Bastien Nocera <bnocera@redhat.com> 2.91.91-1
- Update to 2.91.91

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-6
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.91.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Bastien Nocera <bnocera@redhat.com> 2.91.5-4
- Rebuild against newer control-center

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-3
- Rebuild against newer gtk

* Thu Jan 20 2011 Matthias Clasen <mclasen@redhat.com> 2.91.5-2
- Drop unneeded requires

* Mon Jan 17 2011 Bastien Nocera <bnocera@redhat.com> 2.91.5-1
- Update to 2.91.5

* Sat Jan  8 2011 Matthias Clasen <mclasen@redhat.com> 2.91.2-3
- Rebuild against new gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> 2.91.2-2
- Rebuild against new gtk

* Thu Nov 11 2010 Bastien Nocera <bnocera@redhat.com> 2.91.2-1
- Update to 2.91.2

* Wed Nov  3 2010 Matthias Clasen <mclasen@redhat.com> 1:2.90.0-10
- Rebuild against libnotify 0.7.0

* Wed Sep 29 2010 jkeating - 1:2.90.0-9
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-8
- Fix the build against newer gtk

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-7
- Rebuild against newer gobject-introspection

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-6
- Co-own /usr/share/gtk-doc

* Thu Aug 05 2010 Bastien Nocera <bnocera@redhat.com> 2.90.0-5
- Fix requires for new epoch

* Wed Aug 04 2010 Bastien Nocera <bnocera@redhat.com> 2.90.0-4
- Up the epoch due to F-14 changes

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.90.0-4
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 2.90.0-3
- Rebuild against new gobject-introspection

* Mon Jul  5 2010 Peter Robinson <pbrobinson@fedoraproject.org> 2.90.0-2
- Rebuild for new libmx

* Wed Jun 30 2010 Bastien Nocera <bnocera@redhat.com> 2.90.0-1
- Update to 2.90.0

* Mon Jun 28 2010 Bastien Nocera <bnocera@redhat.com> 2.30.0-3
- Fix moblin package description

* Thu Jun 03 2010 Bastien Nocera <bnocera@redhat.com> 2.30.0-2
- Fix /dev/rfkill permissions when using newer udev >= 154 (#588660)
  (with thanks to Sven Arvidsson and Debian)

* Mon Mar 29 2010 Bastien Nocera <bnocera@redhat.com> 2.30.0-1
- Update to 2.30.0

* Wed Feb 24 2010 Bastien Nocera <bnocera@redhat.com> 2.29.91-2
- Require -libs of the same version to avoid conflicts

* Mon Feb 15 2010 Bastien Nocera <bnocera@redhat.com> 2.29.91-1
- Update to 2.29.91

* Sun Feb 14 2010 Matthias Clasen <mclasen@redhat.com> 2.29.3-5
- Add missing libs

* Thu Jan 28 2010 Bastien Nocera <bnocera@redhat.com> 2.29.3-4
- Fix a few rpmlint warnings

* Tue Dec 15 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-3
- Enable introspection

* Mon Dec 14 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-2
- Add patch to fix possible crasher in bluetooth-sendto (#544881)

* Mon Nov 30 2009 Bastien Nocera <bnocera@redhat.com> 2.29.3-1
- Update to 2.29.3

* Tue Nov 17 2009 Bastien Nocera <bnocera@redhat.com> 2.29.2-1
- Update to 2.29.2
- Add moblin subpackage

* Tue Oct 20 2009 Bastien Nocera <bnocera@redhat.com> 2.28.3-1
- Update to 2.28.3

* Tue Oct 20 2009 Bastien Nocera <bnocera@redhat.com> 2.28.2-1
- Update to 2.28.2

* Tue Sep 29 2009 Bastien Nocera <bnocera@redhat.com> 2.28.1-1
- Update to 2.28.1

* Sat Sep 19 2009 Bastien Nocera <bnocera@redhat.com> 2.28.0-1
- Update to 2.28.0

* Fri Sep 11 2009 Bastien Nocera <bnocera@redhat.com> 2.27.90-3
- Fix possible pairing failure

* Thu Sep 03 2009 Bastien Nocera <bnocera@redhat.com> 2.27.90-2
- Fix connecting to audio devices not working when disconnected
  at start

* Wed Sep 02 2009 Bastien Nocera <bnocera@redhat.com> 2.27.90-1
- Update to 2.27.90

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 2.27.9-5
- Fix the friendly name not being editable (#516801)

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 2.27.9-4
- Add udev rules to access /dev/rfkill (#514798)

* Tue Aug 11 2009 Bastien Nocera <bnocera@redhat.com> 2.27.9-3
- Don't crash when exiting the wizard

* Thu Aug 06 2009 Bastien Nocera <bnocera@redhat.com> 2.27.9-2
- Remove requirement on the main package from -libs, and move
  the icons from the main package to the -libs sub-package (#515845)

* Tue Aug 04 2009 Bastien Nocera <bnocera@redhat.com> 2.27.9-1
- Update to 2.27.9

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Bastien Nocera <bnocera@redhat.com> 2.27.8-1
- Update to 2.27.8

* Thu Jun 25 2009 Bastien Nocera <bnocera@redhat.com> 2.27.7.1-1
- Update to 2.27.7.1

* Thu Jun 25 2009 Bastien Nocera <bnocera@redhat.com> 2.27.7-1
- Update to 2.27.7

* Wed Jun 17 2009 Bastien Nocera <bnocera@redhat.com> 2.27.6-1
- Update to 2.27.6
- Require newer BlueZ for SSP support

* Sat May 16 2009 Matthias Clasen <mclasen@redhat.com> 2.27.5-2
- Require the virtual provides for notification daemon (#500585)

* Wed May 06 2009 Bastien Nocera <bnocera@redhat.com> 2.27.5-1
- Update to 2.27.5

* Fri May 01 2009 Bastien Nocera <bnocera@redhat.com> 2.27.4-4
- Use the scriplets on the wiki for the icon update

* Fri May 01 2009 Bastien Nocera <bnocera@redhat.com> 2.27.4-3
- Touch the icon theme directory, should fix the icon not appearing
  properly on new installs

* Thu Apr 16 2009 - Bastien Nocera <bnocera@redhat.com> - 2.27.4-2
- Require the PA Bluetooth plugins

* Tue Apr 14 2009 - Bastien Nocera <bnocera@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Thu Apr 09 2009 - Bastien Nocera <bnocera@redhat.com> - 2.27.3-1
- Update to 2.27.3

* Wed Apr 08 2009 - Bastien Nocera <bnocera@redhat.com> - 2.27.2-2
- Fix schema installation

* Wed Apr 08 2009 - Bastien Nocera <bnocera@redhat.com> - 2.27.2-1
- Upgrade to 2.27.2

* Tue Mar 10 2009 - Bastien Nocera <bnocera@redhat.com> - 2.27.1-4
- Make the -libs-devel obsolete and provide the -devel package, so
  we can actually upgrade...

* Thu Mar 05 2009 - Bastien Nocera <bnocera@redhat.com> - 2.27.1-3
- Add patch to fix sendto

* Wed Mar 04 2009 - Bastien Nocera <bnocera@redhat.com> - 2.27.1-2
- Update to 2.27.1
- Loads of fixes mentioned by Bill Nottingham in bug #488498

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 - Bastien Nocera <bnocera@redhat.com> - 0.12.0-1
- Update to 0.12.0

* Thu Dec  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.11.0-8
- Rebuild for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.11.0-7
- Rebuild for Python 2.6

* Fri Oct 31 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.0-6
- Remove a few more .la files

* Thu Sep 11 2008 Matthias Clasen  <mclasen@redhat.com> - 0.11.0-5
- Rebuild against new bluez-libs

* Wed May 14 2008 - Ondrej Vasik <ovasik@redhat.com> - 0.11.0-4
- Changed name of icon file(#444811)

* Wed Feb 27 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.0-3
- Remove gnome-obex-server, we should use gnome-user-share now

* Mon Feb 11 2008 - Ondrej Vasik <ovasik@redhat.com> - 0.11.0-1
- gcc43 rebuild

* Mon Jan 21 2008 - Bastien Nocera <bnocera@redhat.com> - 0.11.0
- Update to 0.11.0

* Mon Jan 21 2008 - Bastien Nocera <bnocera@redhat.com> - 0.10.0
- Update to 0.10.0

* Mon Oct 22 2007 - Ondrej Vasik <ovasik@redhat.com> - 0.9.1-4
- marked gnome-obex-server.schemas as config file
- changed upstream URL

* Tue Sep 18 2007 - Ondrej Vasik <ovasik@redhat.com> - 0.9.1-3
- fixed wrong source URL

* Thu Aug 23 2007 - Ondrej Vasik <ovasik@redhat.com> - 0.9.1-2
- rebuilt for F8
- changed license tag to GPLv2 and LGPLv2+

* Mon Jul 23 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.1-1
- Upgrade to 0.9.1 to fix a crasher in the server

* Thu Jul 12 2007 - Bastien Nocera <bnocera@redhat.com> - 0.9.0-1
- Update for 0.9.0
- Fix installation of the python bindings

* Mon Apr  2 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.0-4
- Remove unncessary gconfd killing from scripts (#224561)

* Tue Feb 27 2007 Harald Hoyer <harald@redhat.com> - 0.8.0-3%{?dist}
- corrected BuildRoot
- smp flags added
- specfile cleanup
- fixed desktop file

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.8.0-2
- rebuild for python 2.5

* Mon Nov 13 2006 Harald Hoyer <harald@redhat.com> - 0.8.0-1
- version 0.8.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.7.0-10.1
- rebuild

* Wed Jun 14 2006 Harald Hoyer <harald@redhat.com> - 0.7.0-10
- bump for new openobex

* Sun Jun 11 2006 Jesse Keating <jkeating@redhat.com> - 0.7.0-9
- Missing automake, libtool, gettext BR

* Sun Jun 11 2006 Jesse Keating <jkeating@redhat.com> - 0.7.0-6
- Bump for new libbluetooth

* Wed May 31 2006 Harald Hoyer <harald@redhat.com> - 0.7.0-6
- add dependency on bluez-utils, cosmetic tweaks (bug #190280)

* Tue May 30 2006 Harald Hoyer <harald@redhat.com> - 0.7.0-5
- install schemata correctly (bug #193518)

* Mon May 29 2006 Harald Hoyer <harald@redhat.com> - 0.7.0-3
- more build requires (bug #193374)

* Mon Feb 27 2006 Harald Hoyer <harald@redhat.com> - 0.7.0-2
- pydir fixes for lib64

* Thu Feb 16 2006 Harald Hoyer <harald@redhat.com> - 0.7.0-1
- version 0.7.0

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.0-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.6.0-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Oct 07 2005 Harald Hoyer <harald@redhat.com> - 0.6.0-2
- Fix relative path for the icons in desktop files which no longer works
  with the icon cache.

* Wed Sep 28 2005 Harald Hoyer <harald@redhat.com> - 0.6.0-1
- new version 0.6.0

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> 0.5.1-14
- rebuild for new cairo

* Thu Jul  7 2005 Matthias Saou <http://freshrpms.net/> 0.5.1-13
- Minor spec file cleanups.
- Fix relative path for the icons in desktop files which no longer works
  with the icon cache.
- Remove useless zero epochs.
- Remove explicit python abi requirement, it's automatic for FC4 and up.

* Thu Mar 31 2005 Harald Hoyer <harald@redhat.com> - 0.5.1-12
- removed base requirement from libs

* Tue Mar 29 2005 Warren Togami <wtogami@redhat.com> - 0.5.1-11
- devel req glib2-devel libbtctl-devel for pkgconfig (#152488)

* Wed Mar 02 2005 Harald Hoyer <harald@redhat.com> 
- rebuilt

* Mon Feb 21 2005 Harald Hoyer <harald@redhat.com> - 0.5.1-9
- added gnome hbox patch for bug rh#149215

* Tue Dec 07 2004 Harald Hoyer <harald@redhat.com> - 0.5.1-8
- added requires for python-abi

* Tue Dec 07 2004 Harald Hoyer <harald@redhat.com> - 0.5.1-7
- split package into app, libs and devel

* Mon Oct 25 2004 Harald Hoyer <harald@redhat.com> - 0.5.1-6
- fixed again gnome-bluetooth-manager script for 64bit (bug 134864)

* Fri Oct 08 2004 Harald Hoyer <harald@redhat.com> - 0.5.1-5
- buildrequire pygtk2-devel (bug 135032)
- fixed gnome-bluetooth-manager script for 64bit (bug 134864)
- fixed segfault on file receive (bug 133041)

* Mon Sep 27 2004 Harald Hoyer <harald@redhat.com> - 0.5.1-4
- buildrequire libbtctl-devel
- buildrequire openobex-devel >= 1.0.1
- pythondir -> pyexecdir

* Wed Jul 28 2004 Harald Hoyer <harald@redhat.com> - 0.5.1-3
- added build dependency for librsvg2-devel

* Tue Jul 27 2004 Harald Hoyer <harald@redhat.com> - 0.5.1-2
- added pydir patch

* Thu Jul 22 2004 Harald Hoyer <harald@redhat.com> - 0.5.1-1
- version 0.5.1

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 25 2004 Harald Hoyer <harald@redhat.com> - 0.4.1-8
- corrected BuildRequires

* Wed Mar 10 2004 Harald Hoyer <harald@redhat.com> - 0.4.1-7
- added EggToolBar patch for gcc34

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Harald Hoyer <harald@redhat.de> 0.4.1-4
- added autofoo patch

* Thu Aug 28 2003 Harald Hoyer <harald@redhat.de> 0.4.1-3
- add .so to gnome-vfs module, if libtool does not!

* Thu Aug 07 2003 Harald Hoyer <harald@redhat.de> 0.4.1-2
- call libtool finish

* Wed Aug  6 2003 Harald Hoyer <harald@redhat.de> 0.4.1-1
- new version 0.4.1

* Thu Jun  5 2003 Harald Hoyer <harald@redhat.de> 0.4-1
- initial RPM


