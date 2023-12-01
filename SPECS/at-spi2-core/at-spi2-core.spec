%define majmin %(echo %{version} | cut -d. -f1-2)
Summary:        Protocol definitions and daemon for D-Bus at-spi
Name:           at-spi2-core
Version:        2.36.1
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.gnome.org/GNOME/at-spi2-core
Source0:        http://download.gnome.org/sources/%{name}/%{majmin}/%{name}-%{version}.tar.xz
# https://gitlab.gnome.org/GNOME/at-spi2-core/-/issues/25
Patch0:         fix-login-screen-a11y.patch
BuildRequires:  dbus-devel
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  systemd-devel
Requires:       dbus

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

%package        devel
Summary:        Development files and headers for at-spi2-core
Requires:       %{name} = %{version}-%{release}

%description devel
The at-spi2-core-devel package includes the header files and
API documentation for libatspi.

%prep
%autosetup -p1

%build
%meson -Ddocs=true -Ddefault_bus=dbus-broker -Ddbus_daemon=%{_bindir}/dbus-daemon -Ddbus_broker=%{_bindir}/dbus-broker-launch
%meson_build

%install
%meson_install

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc AUTHORS README
%{_libexecdir}/at-spi2-registryd
%dir %{_datadir}/defaults
%dir %{_datadir}/defaults/at-spi2
%{_datadir}/defaults/at-spi2/accessibility.conf
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop
%{_libdir}/libatspi.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Atspi-2.0.typelib
%{_libexecdir}/at-spi-bus-launcher
%{_datadir}/dbus-1/accessibility-services/org.a11y.atspi.Registry.service
%{_datadir}/dbus-1/services/org.a11y.Bus.service
%{_userunitdir}/at-spi-dbus-bus.service

%files devel
%{_libdir}/libatspi.so
%{_datadir}/gtk-doc/html/libatspi
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Atspi-2.0.gir
%{_includedir}/at-spi-2.0
%{_libdir}/pkgconfig/atspi-2.pc

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.36.1-3
- License verified
- Lint spec

* Mon Mar 01 2021 Henry Li <lihl@microsoft.com> - 2.36.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove LibXi and LibXtst from BuildRequires

* Fri Oct  9 2020 Kalev Lember <klember@redhat.com> - 2.36.1-1
- Update to 2.36.1

* Thu Sep 24 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 2.36.0-2
- Add patch to fix a11y on login screen

* Sun Mar 08 2020 Kalev Lember <klember@redhat.com> - 2.36.0-1
- Update to 2.36.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 2.35.92-1
- Update to 2.35.92

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.35.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Kalev Lember <klember@redhat.com> - 2.35.1-1
- Update to 2.35.1

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 2.33.92-1
- Update to 2.33.92

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 2.33.90-1
- Update to 2.33.90

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.33.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Kalev Lember <klember@redhat.com> - 2.33.2-1
- Update to 2.33.2

* Tue May 21 2019 Kalev Lember <klember@redhat.com> - 2.33.1-1
- Update to 2.33.1

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 2.32.1-2
- Rebuild with Meson fix for #1699099

* Tue Apr 09 2019 Kalev Lember <klember@redhat.com> - 2.32.1-1
- Update to 2.32.1

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Mon Mar 04 2019 Kalev Lember <klember@redhat.com> - 2.31.92-1
- Update to 2.31.92

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 08 2019 Kalev Lember <klember@redhat.com> - 2.31.1-1
- Update to 2.31.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 2.30.0-2
- Rebuilt against fixed atk (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Tue Aug 28 2018 Stephen Gallagher <sgallagh@redhat.com> - 2.28.0-4
- Update to newer version of dbus-broker support
- Resolves: rhbz#1622545

* Fri Aug 10 2018 David Herrmann <dh.herrmann@gmail.com> - 2.28.0-3
- Add support for dbus-broker alongside dbus-daemon

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Kalev Lember <klember@redhat.com> - 2.27.1-2
- Drop unused buildrequires

* Tue Dec 19 2017 Kalev Lember <klember@redhat.com> - 2.27.1-1
- Update to 2.27.1

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 2.26.2-1
- Update to 2.26.2

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Thu Sep 07 2017 Kalev Lember <klember@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Fri Aug 25 2017 Kalev Lember <klember@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Mon Aug 14 2017 Ville Skyttä <ville.skytta@iki.fi> - 2.25.4-4
- Own %%{_libdir}/girepository-1.0 and %%{_datadir}/{defaults,gir-1.0} dirs

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 25 2017 Kalev Lember <klember@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Mon Jun 12 2017 Kalev Lember <klember@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Feb 14 2017 Richard Hughes <rhughes@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 26 2016 Kalev Lember <klember@redhat.com> - 2.22.0-1
- Update to 2.22.0
- Don't set group tags

* Wed Jul 20 2016 Richard Hughes <rhughes@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Mon May 09 2016 Kalev Lember <klember@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 2.20.1-1
- Update to 2.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Mar 15 2016 Richard Hughes <rhughes@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Tue Mar 01 2016 Richard Hughes <rhughes@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Kalev Lember <klember@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 2.17.90-1
- Update to 2.17.90
- Use make_install macro

* Tue Jul 28 2015 Kalev Lember <klember@redhat.com> - 2.17.1-1
- Update to 2.17.1
- Use license macro for COPYING

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 2.16.0-1
- Update to 2.16.0

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 2.15.90-1
- Update to 2.15.90

* Tue Jan 20 2015 Richard Hughes <rhughes@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Wed Dec 17 2014 Kalev Lember <kalevlember@gmail.com> - 2.15.3-1
- Update to 2.15.3

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 2.15.2-1
- Update to 2.15.2

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 2.14.1-1
- Update to 2.14.1

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.14.0-1
- Update to 2.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.92-1
- Update to 2.13.92

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.90-1
- Update to 2.13.90

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.4-2
- Rebuilt for gobject-introspection 1.41.4

* Sun Jul 20 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.4-1
- Update to 2.13.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Richard Hughes <rhughes@redhat.com> - 2.13.1-1
- Update to 2.13.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 2.12.0-2
- Tighten -devel deps

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 2.11.92-1
- Update to 2.11.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 2.11.91-1
- Update to 2.11.91

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 2.11.90-1
- Update to 2.11.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 2.11.5-1
- Update to 2.11.5

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 2.11.3-1
- Update to 2.11.3

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 2.11.2-1
- Update to 2.11.2

* Mon Nov 04 2013 Kalev Lember <kalevlember@gmail.com> - 2.11.1-1
- Update to 2.11.1

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 2.10.0-1
- Update to 2.10.0

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.92-1
- Update to 2.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.91-1
- Update to 2.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.90-1
- Update to 2.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.5-1
- Update to 2.9.5

* Sun Jul 28 2013 Rui Matos <rmatos@redhat.com> - 2.9.4-3
- Pass --force to autoreconf to be sure it does what we want

* Sat Jul 20 2013 Rui Matos <rmatos@redhat.com> - 2.9.4-2
- Run autoreconf instead of a sed hack to avoid RPATH embedding

* Tue Jul 16 2013 Richard Hughes <rhughes@redhat.com> - 2.9.4-1
- Update to 2.9.4

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.3-1
- Update to 2.9.3

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.2-1
- Update to 2.9.2

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.91-1
- Update to 2.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.90-1
- Update to 2.7.90

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.5-1
- Update to 2.7.5

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.4.1-1
- Update to 2.7.4.1

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.3-1
- Update to 2.7.3

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.1-1
- Update to 2.7.1

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.6.1-1
- Update to 2.6.1

* Tue Sep 25 2012 Richard Hughes <hughsient@gmail.com> - 2.6.0-1
- Update to 2.6.0

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 2.5.92-1
- Update to 2.5.92

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 2.5.91-1
- Update to 2.5.91

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 2.5.5-1
- Update to 2.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 2.5.4-1
- Update to 2.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 2.5.3-1
- Update to 2.5.3

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 2.5.2-1
- Update to 2.5.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 2.5.1-1
- Update to 2.5.1

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 2.3.92-1
- Update to 2.3.92

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.91-1
- Update to 2.3.91

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.90-1
- Update to 2.3.90

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.5-1
- Update to 2.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.4-1
- Update to 2.3.4

* Tue Jan 10 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.3.3-2
- Fix the rpath issue for building gobject-introspection properly as suggested from upstream

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.3-1
- Update to 2.3.3

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.92-1
- Update to 2.1.92

* Mon Sep 5 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.91-1
- Update to 2.1.91

* Thu Sep 1 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.90-3
- Drop the %%{_isa} again, it seems to give autoqa trouble

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.90-2
- Fix requires

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.90-1
- Update to 2.1.90

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.5-1
- Update to 2.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.4-1
- Update to 2.1.4

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.1.2-1
- Update to 2.1.2

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Fri Apr  1 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.93-2
- Fix 30 second wait during login (#691995)

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.93-1
- Update to 1.91.93

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.92-1
- Update to 2.91.92

* Wed Mar  9 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.91-2
- Fix a crash on logout

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.91-1
- Update to 1.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.90-1
- Update to 1.91.90

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.91.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6.1-1
- Update to 1.91.6.1

* Tue Feb  1 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6-1
- Update to 1.91.6

* Fri Jan 21 2011 Christopher Aillon <caillon@redhat.com> - 1.91.5-2
- Add gobject-introspection support

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-1
- Update to 1.91.5

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.2-1
- Update 1.91.2

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.0-1
- Update to 1.91.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.91-1
- Update to 0.3.91

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.90-1
- Update to 0.3.90

* Tue Jun 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.4-1
- Update to 0.3.4

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.3-1
- Update to 0.3.3

* Tue Jun  1 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.2-2
- Don't relocate the dbus a11y stack

* Fri May 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Sat May 15 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.1-1
- Update to 0.3.1

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.8-1
- Update to 0.1.8

* Sat Feb 20 2010 Matthias Clasen <mclasen@redhat.com> - 0.1.7-1
- Update to 0.1.7

* Wed Feb 10 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.1.6-1
- Update to 0.1.6

* Wed Jan 20 2010 Matthias Clasen <mlasen@redhat.com> - 0.1.5-2
- Specify the right location for the dbus daemon

* Sun Jan 17 2010 Matthias Clasen <mlasen@redhat.com> - 0.1.5-1
- Update to 0.1.5

* Tue Dec 22 2009 Matthias Clasen <mlasen@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Fri Dec  4 2009 Matthias Clasen <mlasen@redhat.com> - 0.1.3-1
- Initial packaging
