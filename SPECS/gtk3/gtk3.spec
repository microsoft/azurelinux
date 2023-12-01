%global with_broadway 1
%global with_sysprof 0
%global glib2_version 2.57.2
%global pango_version 1.41.0
%global atk_version 2.35.1
%global cairo_version 1.14.0
%global gdk_pixbuf_version 2.30.0
%global xrandr_version 1.5.0
%global wayland_protocols_version 1.17
%global wayland_version 1.14.91
%global epoxy_version 1.4
%global bin_version 3.0.0
# Filter provides for private modules
%global __provides_exclude_from ^%{_libdir}/gtk-3.0
Summary:        GTK+ graphical user interface library
Name:           gtk3
Version:        3.24.28
Release:        9%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.gtk.org
Source0:        https://download.gnome.org/sources/gtk+/3.24/gtk+-%{version}.tar.xz
# https://bugzilla.redhat.com/show_bug.cgi?id=1946133
# https://gitlab.gnome.org/GNOME/gtk/-/merge_requests/3387
Patch0:         3387.patch
BuildRequires:  cairo-devel >= %{cairo_version}
BuildRequires:  cairo-gobject-devel >= %{cairo_version}
BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  gtk-doc
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(atk) >= %{atk_version}
BuildRequires:  pkgconfig(atk-bridge-2.0)
BuildRequires:  pkgconfig(avahi-gobject)
BuildRequires:  colord-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(pango) >= %{pango_version}
BuildRequires:  pkgconfig(rest-1.0)
BuildRequires:  pkgconfig(wayland-client) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-cursor) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-egl) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr) >= %{xrandr_version}
BuildRequires:  pkgconfig(xrender)
%if 0%{?with_sysprof}
BuildRequires:  pkgconfig(sysprof-capture-4)
%endif
# standard icons
Requires:       adwaita-icon-theme
Requires:       atk >= %{atk_version}
Requires:       cairo >= %{cairo_version}
Requires:       cairo-gobject >= %{cairo_version}
# required to support all the different image formats
Requires:       gdk-pixbuf2-modules
Requires:       glib2 >= %{glib2_version}
# split out in a subpackage
Requires:       gtk-update-icon-cache
# required for icon theme apis to work
Requires:       hicolor-icon-theme
Requires:       libXrandr >= %{xrandr_version}
Requires:       colord-libs
Requires:       libepoxy >= %{epoxy_version}
Requires:       libwayland-client >= %{wayland_version}
Requires:       libwayland-cursor >= %{wayland_version}
Requires:       pango >= %{pango_version}

# make sure we have a reasonable gsettings backend
Recommends:     dconf
Provides:       adwaita-gtk3-theme = %{version}-%{release}

%description
GTK+ is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK+ is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 3 of GTK+.

%package        immodules
Summary:        Input methods for GTK+
# for im-cedilla.conf
Requires:       gtk2-immodules
Requires:       gtk3 = %{version}-%{release}

%description immodules
The gtk3-immodules package contains standalone input methods that
are shipped as part of GTK+ 3.

%package        immodule-xim
Summary:        XIM support for GTK+
Requires:       gtk3 = %{version}-%{release}

%description immodule-xim
The gtk3-immodule-xim package contains XIM support for GTK+ 3.

%package        devel
Summary:        Development files for GTK+
Requires:       gtk3 = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications with version 3 of the GTK+ widget toolkit. If
you plan to develop applications with GTK+, consider installing the
gtk3-devel-docs package.

%package        devel-docs
Summary:        Developer documentation for GTK+
Requires:       gtk3 = %{version}-%{release}

%description devel-docs
This package contains developer documentation for version 3 of the GTK+
widget toolkit.

%package        tests
Summary:        Tests for the %{name} package
Requires:       %{name} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -n gtk+-%{version} -p1

%build
export CFLAGS='-fno-strict-aliasing %{optflags}'
(if ! test -x configure; then NOCONFIGURE=1 ./autogen.sh; CONFIGFLAGS=--enable-gtk-doc; fi;
 %configure $CONFIGFLAGS \
        --enable-xkb \
        --enable-xinerama \
        --enable-xrandr \
        --enable-xfixes \
        --enable-xcomposite \
        --enable-xdamage \
        --enable-x11-backend \
        --enable-wayland-backend \
%if 0%{?with_broadway}
        --enable-broadway-backend \
%endif
        --enable-colord \
        --enable-installed-tests \
        --with-included-immodules=wayland
)

# fight unused direct deps
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0/g' libtool

%make_build

%install
%make_install RUN_QUERY_IMMODULES_TEST=false

%find_lang gtk30
%find_lang gtk30-properties

(cd %{buildroot}%{_bindir}
 mv gtk-query-immodules-3.0 gtk-query-immodules-3.0-%{__isa_bits}
)

echo ".so man1/gtk-query-immodules-3.0.1" > %{buildroot}%{_mandir}/man1/gtk-query-immodules-3.0-%{__isa_bits}.1

# Remove unpackaged files
find %{buildroot} -type f -name "*.la" -delete -print
rm -f %{buildroot}%{_bindir}/gtk-update-icon-cache
rm -f %{buildroot}%{_mandir}/man1/gtk-update-icon-cache.1*

%if !0%{?with_broadway}
rm %{buildroot}%{_mandir}/man1/broadwayd.1*
%endif

touch %{buildroot}%{_libdir}/gtk-3.0/%{bin_version}/immodules.cache

mkdir -p %{buildroot}%{_sysconfdir}/gtk-3.0
mkdir -p %{buildroot}%{_libdir}/gtk-3.0/modules
mkdir -p %{buildroot}%{_libdir}/gtk-3.0/immodules
mkdir -p %{buildroot}%{_libdir}/gtk-3.0/%{bin_version}/theming-engines

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%transfiletriggerin -- %{_libdir}/gtk-3.0/3.0.0/immodules
gtk-query-immodules-3.0-%{__isa_bits} --update-cache &>/dev/null || :

%transfiletriggerpostun -- %{_libdir}/gtk-3.0/3.0.0/immodules
gtk-query-immodules-3.0-%{__isa_bits} --update-cache &>/dev/null || :

%files -f gtk30.lang
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/gtk-query-immodules-3.0*
%{_bindir}/gtk-launch
%{_libdir}/libgtk-3.so.*
%{_libdir}/libgdk-3.so.*
%{_libdir}/libgailutil-3.so.*
%dir %{_libdir}/gtk-3.0
%dir %{_libdir}/gtk-3.0/%{bin_version}
%{_libdir}/gtk-3.0/%{bin_version}/theming-engines
%dir %{_libdir}/gtk-3.0/%{bin_version}/immodules
%{_libdir}/gtk-3.0/%{bin_version}/printbackends
%{_libdir}/gtk-3.0/modules
%{_libdir}/gtk-3.0/immodules
%{_datadir}/themes/Default
%{_datadir}/themes/Emacs
%{_libdir}/girepository-1.0
%ghost %{_libdir}/gtk-3.0/%{bin_version}/immodules.cache
%{_mandir}/man1/gtk-query-immodules-3.0*
%{_mandir}/man1/gtk-launch.1*
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.EmojiChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.Settings.FileChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.exampleapp.gschema.xml
%if 0%{?with_broadway}
%{_bindir}/broadwayd
%{_mandir}/man1/broadwayd.1*
%endif

%files immodules
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cedilla.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-am-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-cyrillic-translit.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-inuktitut.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ipa.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-multipress.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-thai.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-er.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-ti-et.so
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-viqr.so
%if 0%{?with_broadway}
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-broadway.so
%endif
%config(noreplace) %{_sysconfdir}/gtk-3.0/im-multipress.conf

%files immodule-xim
%{_libdir}/gtk-3.0/%{bin_version}/immodules/im-xim.so

%files devel -f gtk30-properties.lang
%{_libdir}/lib*.so
%{_includedir}/*
%{_datadir}/aclocal/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk3-demo
%{_bindir}/gtk3-icon-browser
%{_bindir}/gtk-builder-tool
%{_bindir}/gtk-encode-symbolic-svg
%{_bindir}/gtk-query-settings
%{_datadir}/applications/gtk3-demo.desktop
%{_datadir}/applications/gtk3-icon-browser.desktop
%{_datadir}/applications/gtk3-widget-factory.desktop
%{_datadir}/icons/hicolor/*/apps/gtk3-demo.png
%{_datadir}/icons/hicolor/*/apps/gtk3-demo-symbolic.symbolic.png
%{_datadir}/icons/hicolor/*/apps/gtk3-widget-factory.png
%{_datadir}/icons/hicolor/*/apps/gtk3-widget-factory-symbolic.symbolic.png
%{_bindir}/gtk3-demo-application
%{_bindir}/gtk3-widget-factory
%{_datadir}/gettext/
%{_datadir}/gir-1.0
%{_datadir}/glib-2.0/schemas/org.gtk.Demo.gschema.xml
%dir %{_datadir}/gtk-3.0
%{_datadir}/gtk-3.0/gtkbuilder.rng
%{_datadir}/gtk-3.0/valgrind/
%{_mandir}/man1/gtk3-demo.1*
%{_mandir}/man1/gtk3-demo-application.1*
%{_mandir}/man1/gtk3-icon-browser.1*
%{_mandir}/man1/gtk3-widget-factory.1*
%{_mandir}/man1/gtk-builder-tool.1*
%{_mandir}/man1/gtk-encode-symbolic-svg.1*
%{_mandir}/man1/gtk-query-settings.1*

%files devel-docs
%{_datadir}/gtk-doc

%files tests
%{_libexecdir}/installed-tests/
%{_datadir}/installed-tests/

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.24.28-9
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 03 2022 Henry Li <lihl@microsoft.com> - 3.24.28-8
- Use pkgconfig(rest-1.0) as BR 

* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.24.28-7
- License verified
- Lint spec

* Tue Dec 07 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.24.28-6
- Using HTTPS in URLs.
- License verified.

* Wed Oct 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.24.28-5
- Bringing back the dependency on 'cairo'.

* Fri May 21 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.24.28-4
- Remove gtk-update-icon-cache subpackage
- Turn off sysprof integration to break build cycle

* Tue Apr 20 2021 Henry Li <lihl@microsoft.com> - 3.24.28-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- Change dependency from cairo to UI-cairo

* Tue Apr 06 2021 Kalev Lember <klember@redhat.com> - 3.24.28-2
- Backport upstream fix for typing apostrophes / single quotes (#1946133)

* Sat Mar 27 2021 Kalev Lember <klember@redhat.com> - 3.24.28-1
- Update to 3.24.28

* Fri Mar 12 2021 Kalev Lember <klember@redhat.com> - 3.24.27-1
- Update to 3.24.27

* Tue Feb 23 2021 Kalev Lember <klember@redhat.com> - 3.24.26-1
- Update to 3.24.26

* Mon Feb 15 2021 Kalev Lember <klember@redhat.com> - 3.24.25-2
- Backport upstream patches to fix regressions in Compose file parsing
- Backport upstream patch to further tweak scrollbar transitions and size

* Fri Feb 12 2021 Kalev Lember <klember@redhat.com> - 3.24.25-1
- Update to 3.24.25

* Fri Dec 11 2020 Kalev Lember <klember@redhat.com> - 3.24.24-1
- Update to 3.24.24

* Fri Sep 04 2020 Kalev Lember <klember@redhat.com> - 3.24.23-1
- Update to 3.24.23

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 3.24.22-2
- Rebuild for sysprof-capture-4

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 3.24.22-1
- Update to 3.24.22

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Kalev Lember <klember@redhat.com> - 3.24.21-1
- Update to 3.24.21

* Mon Apr 27 2020 Kalev Lember <klember@redhat.com> - 3.24.20-1
- Update to 3.24.20

* Fri Apr 10 2020 Kalev Lember <klember@redhat.com> - 3.24.18-1
- Update to 3.24.18

* Fri Apr 03 2020 Kalev Lember <klember@redhat.com> - 3.24.17-1
- Update to 3.24.17

* Fri Apr 03 2020 Kalev Lember <klember@redhat.com> - 3.24.16-2
- Backport upstream fixes for an imwayland crash

* Fri Mar 27 2020 Kalev Lember <klember@redhat.com> - 3.24.16-1
- Update to 3.24.16

* Mon Feb 17 2020 Kalev Lember <klember@redhat.com> - 3.24.14-1
- Update to 3.24.14

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 3.24.13-1
- Update to 3.24.13

* Tue Oct 22 2019 Adam Williamson <awilliam@redhat.com> - 3.24.12-3
- Backport PR #1146 to fix a bug that #1142 introduced...

* Mon Oct 21 2019 Adam Williamson <awilliam@redhat.com> - 3.24.12-2
- Backport PR #1142 to try and fix intermittent copy/cut failures

* Fri Oct 04 2019 Kalev Lember <klember@redhat.com> - 3.24.12-1
- Update to 3.24.12

* Wed Sep 04 2019 Kalev Lember <klember@redhat.com> - 3.24.11-1
- Update to 3.24.11
- Build with sysprof support on F31+

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Kalev Lember <klember@redhat.com> - 3.24.10-1
- Update to 3.24.10

* Tue Jun 18 2019 Kalev Lember <klember@redhat.com> - 3.24.9-1
- Update to 3.24.9

* Thu Apr 11 2019 Kalev Lember <klember@redhat.com> - 3.24.8-1
- Update to 3.24.8

* Thu Mar 14 2019 Kalev Lember <klember@redhat.com> - 3.24.7-2
- Undo runtime gtk_window_present deprecation warnings

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 3.24.7-1
- Update to 3.24.7

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 3.24.6-1
- Update to 3.24.6

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 3.24.5-1
- Update to 3.24.5

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Kalev Lember <klember@redhat.com> - 3.24.4-1
- Update to 3.24.4

* Mon Jan 14 2019 Kalev Lember <klember@redhat.com> - 3.24.3-1
- Update to 3.24.3
- Co-own /usr/libexec/installed-tests directory

* Wed Sep 19 2018 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Mon Sep 10 2018 Adam Williamson <awilliam@redhat.com> - 3.24.0-4
- Revert a problematic change that breaks several things (GGO #1316)

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 3.24.0-3
- Rebuilt against fixed atk (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.24.0-2
- Backport two bugfixes from upstream

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 18 2018 Kalev Lember <klember@redhat.com> - 3.22.30-1
- Update to 3.22.30

* Tue Apr 10 2018 Kalev Lember <klember@redhat.com> - 3.22.29-2
- Build with --with-included-immodules=wayland

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 3.22.29-1
- Update to 3.22.29

* Fri Mar 02 2018 Kalev Lember <klember@redhat.com> - 3.22.28-1
- Update to 3.22.28

* Sun Feb 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.22.26-4
- Drop direct gtk-update-icon-cache calls
- Drop ldconfig scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 29 2017 Christophe Fergeau <cfergeau@redhat.com> - 3.22.26-2
- Backport fix for guest/host copy&paste issues in Boxes (Freedesktop #101353)

* Tue Nov 07 2017 Kalev Lember <klember@redhat.com> - 3.22.26-1
- Update to 3.22.26

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 3.22.25-1
- Update to 3.22.25

* Wed Oct 25 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.22.24-3
- Backport fix to prevent crashes when adding online accounts (GNOME #789141)

* Mon Oct 23 2017 Troy Dawson <tdawson@redhat.com> - 3.22.24-2
- Cleanup spec file conditionals

* Wed Oct 04 2017 Kalev Lember <klember@redhat.com> - 3.22.24-1
- Update to 3.22.24

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 3.22.21-1
- Update to 3.22.21

* Tue Sep 05 2017 Kalev Lember <klember@redhat.com> - 3.22.20-1
- Update to 3.22.20

* Tue Aug 22 2017 Kalev Lember <klember@redhat.com> - 3.22.19-1
- Update to 3.22.19

* Tue Aug 08 2017 Kalev Lember <klember@redhat.com> - 3.22.18-1
- Update to 3.22.18

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.22.17-2
- Backport fix to throttle system bell requests on Wayland (RH #1466654)

* Wed Jul 19 2017 Kalev Lember <klember@redhat.com> - 3.22.17-1
- Update to 3.22.17

* Wed Jun 21 2017 Kalev Lember <klember@redhat.com> - 3.22.16-1
- Update to 3.22.16
- Filter provides for private modules
- Update package summary

* Thu May 25 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.22.15-2
- Backport fix to not abort when the Wayland connection is lost (RH #1258818)

* Fri May 12 2017 Kalev Lember <klember@redhat.com> - 3.22.15-1
- Update to 3.22.15

* Wed May 10 2017 Kalev Lember <klember@redhat.com> - 3.22.14-1
- Update to 3.22.14

* Wed May 10 2017 Kalev Lember <klember@redhat.com> - 3.22.13-1
- Update to 3.22.13

* Thu Apr 20 2017 Kalev Lember <klember@redhat.com> - 3.22.12-2
- Try harder to remove all libtool .la files

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 3.22.12-1
- Update to 3.22.12

* Mon Mar 20 2017 Kalev Lember <klember@redhat.com> - 3.22.11-1
- Update to 3.22.11

* Tue Mar 14 2017 Kalev Lember <klember@redhat.com> - 3.22.10-1
- Update to 3.22.10

* Thu Mar 02 2017 Kalev Lember <klember@redhat.com> - 3.22.9-2
- Backport a patch to fix spurious key repeat in gnome-terminal (#1428280)

* Tue Feb 28 2017 Kalev Lember <klember@redhat.com> - 3.22.9-1
- Update to 3.22.9

* Tue Feb 14 2017 Kalev Lember <klember@redhat.com> - 3.22.8-2
- Set minimum required xrandr version

* Mon Feb 13 2017 Kalev Lember <klember@redhat.com> - 3.22.8-1
- Update to 3.22.8

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Kalev Lember <klember@redhat.com> - 3.22.7-1
- Update to 3.22.7

* Tue Jan 10 2017 Michael Catanzaro <mcatanzaro@gnome.org> - 3.22.6-2
- Add patch for GNOME #769835

* Thu Jan 05 2017 Kalev Lember <klember@redhat.com> - 3.22.6-1
- Update to 3.22.6

* Sun Dec 11 2016 Kalev Lember <klember@redhat.com> - 3.22.5-1
- Update to 3.22.5

* Mon Nov 21 2016 Kalev Lember <klember@redhat.com> - 3.22.4-1
- Update to 3.22.4

* Thu Nov 10 2016 Kalev Lember <klember@redhat.com> - 3.22.3-1
- Update to 3.22.3

* Tue Nov  8 2016 Matthias Clasen <mclasen@redhat.com> - 3.22.2-2
- Fix #1376471

* Mon Oct 24 2016 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Tue Oct 11 2016 Adam Jackson <ajax@redhat.com> - 3.22.1-2
- Prefer eglGetPlatformDisplay to eglGetDisplay

* Sat Oct 01 2016 David King <amigadave@amigadave.com> - 3.22.1-1
- Update to 3.22.1

* Wed Sep 28 2016 Kalev Lember <klember@redhat.com> - 3.22.0-2
- Backport a patch to fix shifted content in totem and gnome-maps (#1377741)

* Tue Sep 20 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.21.6-2
- gtkwindow: Update shadow size on state change (#1377313)

* Tue Sep 13 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.6-1
- Update to 3.21.6

* Tue Aug 30 2016 Kalev Lember <klember@redhat.com> - 3.21.5-1
- Update to 3.21.5
- Don't set group tags

* Wed Jul 27 2016 Kalev Lember <klember@redhat.com> - 3.21.4-2
- Install dconf gsettings backend by default (#1351236)

* Mon Jul 18 2016 Kalev Lember <klember@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 3.21.1-1
- Update to 3.21.1
- Set minimum required wayland-protocols version

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.3-1
- Update to 3.20.3

* Tue Apr  5 2016 Matthias Clasen <mclasen@redhat.com> - 3.20.2-2
- Drop no-longer-used Requires(post)

* Thu Mar 31 2016 Kalev Lember <klember@redhat.com> - 3.20.2-1
- Update to 3.20.2

* Fri Mar 25 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Tue Mar 15 2016 Kalev Lember <klember@redhat.com> - 3.19.12-1
- Update to 3.19.12

* Wed Mar 02 2016 Richard Hughes <rhughes@redhat.com> - 3.19.11-1
- Update to 3.19.11

* Wed Feb 24 2016 Matthias Clasen <mclasen@redhat.com> - 3.19.10-1
- Update to 3.19.10

* Wed Feb 17 2016 Richard Hughes <rhughes@redhat.com> - 3.19.9-1
- Update to 3.19.9

* Mon Feb 08 2016 Debarshi Ray <rishi@fedoraproject.org> - - 3.19.8-4
- Backport fix for missing focus-in/out events (GNOME #677329)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Ray Strode <rstrode@redhat.com> - 3.19.8-2
- Fix leak in wayland
  https://bugzilla.gnome.org/show_bug.cgi?id=761312

* Mon Feb  1 2016 Matthias Clasen <mclasen@redhat.com> - 3.19.8-1
- Update to 3.19.8

* Mon Jan 25 2016 Ray Strode <rstrode@redhat.com> - 3.19.7-2
- fix SIGBUG crasher in wayland
  Related: #1300390

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 3.19.7-1
- Update to 3.19.7

* Mon Jan 11 2016 Kalev Lember <klember@redhat.com> - 3.19.6-1
- Update to 3.19.6

* Thu Dec 17 2015 Kalev Lember <klember@redhat.com> - 3.19.5-2
- Fix GtkBorder / GdkBorder struct definitions

* Wed Dec 16 2015 Kalev Lember <klember@redhat.com> - 3.19.5-1
- Update to 3.19.5

* Sat Dec 05 2015 Kalev Lember <klember@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Wed Nov 25 2015 Matthias Clasen <mclasen@redhat.com> - 3.19.3-2
- Fix firefox popup positioning

* Mon Nov 23 2015 Matthias Clasen <mclasen@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Fri Nov 20 2015 Kalev Lember <klember@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 3.19.1-1
- Update to 3.19.1

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Sun Oct 04 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Tue Sep 15 2015 Kalev Lember <klember@redhat.com> - 3.17.9-1
- Update to 3.17.9

* Sun Sep 13 2015 Kalev Lember <klember@redhat.com> - 3.17.8-2
- Backport a patch to fix mouse scroll wheel events (#1258236)

* Wed Sep 02 2015 Kalev Lember <klember@redhat.com> - 3.17.8-1
- Update to 3.17.8

* Wed Aug 26 2015 Adam Williamson <awilliam@redhat.com> - 3.17.7-2
- revert a 3.17.7 change to fix BGO #754147 until it's fixed upstream

* Tue Aug 18 2015 Kalev Lember <klember@redhat.com> - 3.17.7-1
- Update to 3.17.7
- Use make_install macro

* Fri Aug 14 2015 Matthias Clasen <mclasen@redhat.com> - 3.17.6-3
- Add file triggers for im modules

* Fri Aug 14 2015 Matthias Clasen <mclasen@redhat.com> - 3.17.6-2
- Rely on glib file triggers

* Wed Aug  5 2015 Matthias Clasen <mclasen@redhat.com> - 3.17.6-1
- Update to 3.17.6

* Tue Jul 21 2015 David King <amigadave@amigadave.com> - 3.17.5-1
- Update to 3.17.5
- Preserve timestamps during install

* Mon Jul 13 2015 Adam Williamson <awilliam@redhat.com> - 3.17.4-2
- backport upstream CSS changes to fix BGO #752247
- backport upstream font default changes to help with RHBZ #1241724

* Wed Jun 24 2015 David King <amigadave@amigadave.com> - 3.17.4-1
- Update to 3.17.4

* Wed Jun 17 2015 Kalev Lember <klember@redhat.com> - 3.17.3-3
- Obsolete gtk-solidity-engine

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.3-1
- Update to 3.17.3

* Thu Apr 30 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-1
- Update to 3.17.1
- Include gtk-builder-tool in the -devel subpackage

* Fri Apr 17 2015 Rex Dieter <rdieter@fedoraproject.org> 3.16.2-2
- Obsoletes: oxygen-gtk3 < 2:1.4.1

* Tue Apr 14 2015 David King <amigadave@amigadave.com> - 3.16.2-1
- Update to 3.16.2

* Tue Apr  7 2015 Matthias Clasen <mclasen@redhat.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Fri Mar 20 2015 Richard Hughes <rhughes@redhat.com> - 3.15.12-2
- Depend on gdk-pixbuf2-modules as this is now an optional subpackage

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.12-1
- Update to 3.15.12
- Use license macro for the COPYING file

* Thu Mar 12 2015 Matthias Clasen <mclasen@redhat.com> - 3.15.11-1
- Update to 3.15.11

* Tue Mar 03 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.10-1
- Update to 3.15.10

* Tue Feb 24 2015 Matthias Clasen <mclasen@redhat.com> - 3.15.9-1
- Update to 3.15.9

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.15.8-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Fri Feb 20 2015 Matthias Clasen <mclasen@redhat.com> - 3.15.8-1
- Update to 3.15.8

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 3.15.7-1
- Update to 3.15.7

* Tue Feb 10 2015 Matthias Clasen <mclasen@redhat.com> - 3.15.6-1
- Update to 3.15.6

* Thu Jan 22 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Wed Dec 17 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.3-1
- Update to 3.15.3
- Add gtk-update-icon-cache subpackage that both gtk2 and gtk3 can depend on
- Run icon cache scriptlets for the -devel subpackage

* Mon Nov 24 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.2-1
- Update to 3.15.2

* Thu Oct 30 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.1-1
- Update to 3.15.1

* Tue Oct 21 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.4-1
- Update to 3.14.4

* Thu Oct 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.3-2
- Backport a patch to fix status icons in XFCE (#1134663)

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.3-1
- Update to 3.14.3

* Wed Oct 08 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Fri Oct 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-2
- Backport an upstream fix for GtkBuilder type name heuristics

* Tue Sep 30 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0
- Tighten deps with the _isa macro
- Set minimum required wayland version

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.9-1
- Update to 3.13.9

* Tue Sep 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.8-1
- Update to 3.13.8

* Thu Aug 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.7-3.git5ad60ca
- Update to today's git snapshot

* Wed Aug 27 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.7-2
- Backport a few upstream fixes for checkboxes

* Sun Aug 17 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.7-1
- Update to 3.13.7

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.6-1
- Update to 3.13.6

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.5-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.5-1
- Update to 3.13.5

* Tue Jul 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Thu Jun 26 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-2
- Obsolete adwaita-gtk3-theme

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Tim Waugh <twaugh@redhat.com> - 3.13.2-5
- Added build deps for cloudprint print backend module (bug #1104663).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-3
- Backport a GtkBuilder fix to ensure types get fully initialized

* Fri May 30 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-2
- Backport two fixes from git master

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Tue Apr 29 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Depend on adwaita-icon-theme to ensure standard icons are available

* Tue Apr 29 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-1
- Update to 3.13.1

* Sat Apr 12 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Update glib2 dep version

* Tue Mar 25 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Wed Mar 19 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.9-2
- Backport a patch for a gnome-terminal crash

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.9-1
- Update to 3.11.9

* Mon Mar 17 2014 Adam Williamson <awilliam@redhat.com> - 3.11.8-2
- backport patches for touch dragging of new-style GNOME windows

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.8-1
- Update to 3.11.8

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.7-1
- Update to 3.11.7

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.6-1
- Update to 3.11.6

* Wed Feb  5 2014 Debarshi Ray <rishi@fedoraproject.org> - 3.11.5-1
- Update to 3.11.5

* Wed Jan 15 2014 Debarshi Ray <rishi@fedoraproject.org> - 3.11.4-1
- Update to 3.11.4

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Mon Oct 28 2013 Richard Hughes <rhughes@redhat.com> - 3.11.0-1
- Update to 3.11.0

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.16-2
- Rebuilt with cairo 1.13.1 snapshot for device scale support

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.16-1
- Update to 3.9.16

* Tue Sep  3 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.14-1
- Update to 3.9.14

* Wed Aug 21 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.9.12-1
- Update to 3.9.12

* Thu Aug  1 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.9.10-1
- Update to 3.9.10

* Tue Jul 30 2013 Richard Hughes <rhughes@redhat.com> - 3.9.8-2
- Rebuild for colord soname bump

* Tue Jul  9 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.8-1
- Update to 3.9.8

* Thu Jul  4 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.6-2
- Don't put an empty dir into /etc.

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.6-1
- Update to 3.9.6
- Add a tests subpackage

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.4-1
- Update to 3.9.4

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.2-1
- Update to 3.9.2

* Wed May  8 2013 Matthias Clasen <mclasen@redhat.com> - 3.9.0-2
- Make man gtk-query-immodules-3.0-64 work

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.0-1
- Update to 3.9.0

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.14-1
- Update to 3.7.14

* Wed Mar  6 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.12-1
- Update to 3.7.12

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.10-1
- Update to 3.7.10

* Tue Feb 05 2013 Richard Hughes <rhughes@redhat.com> - 3.7.8-1
- Update to 3.7.8

* Mon Jan 28 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.6-4
- Move im-cedilla back to -immodules subpackage to avoid
  a conflict with gtk2-immodules (#797838)

* Thu Jan 24 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.6-3
- Enable the Wayland and Broadway backends

* Thu Jan 24 2013 Cosimo Cecchi <cosimoc@redhat.com> - 3.7.6-2
- Backport two patches from git master to fix window allocations

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.6-1
- Update to 3.7.6

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.0-1
- Update to 3.7.0

* Fri Oct 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.6.1-2
- Don't pull in imsettings just for a directory

* Tue Oct 16 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Fri Oct 12 2012 Bastien Nocera <bnocera@redhat.com> 3.6.0-2
- Add upstream patch to make Epiphany less painful to use

* Tue Sep 25 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.18-1
- Update to 3.5.18

* Thu Sep 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.16-1
- Update to 3.5.16

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 3.5.14-1
- Update to 3.5.14

* Wed Aug 22 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.12-2
- Backport a patch from upstream fixing crashers with app menus

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.12-1
- Update to 3.5.12

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.10-1
- Update to 3.5.10

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.8-1
- Update to 3.5.8

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.6-1
- Update to 3.5.6

* Wed Jun 06 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.20-1
- Update to 3.3.20

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.18-1
- Update to 3.3.18

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.16-1
- Update to 3.3.16

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.14-1
- Update to 3.3.14

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.10-1
- Update to 3.3.10

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.8-1
- Update to 3.3.8

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.6-2
- Revert a problematic focus handling change

* Mon Dec 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.6-1
- Update to 3.3.6

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Wed Nov  3 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Fri Oct 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Fri Sep 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-2
- Fix crashes when turning a11y on and off repeatedly

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Tue Sep 13 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90-1
- Update to 3.1.90

* Mon Sep  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.18-1
- Update to 3.1.18

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.16-1
- Update to 3.1.16

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.12-1
- Update to 3.1.12

* Sat Jul 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.10-1
- Update to 3.1.10

* Tue Jul  5 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.8-1
- Update to 3.1.8

* Tue Jun 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.6-1
- Update to 3.1.6

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.9-1
- Update to 3.0.9

* Thu Apr 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-3
- Move im-cedilla back to the main package (#637399)

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-2
- Add a missed backport

* Sun Apr  3 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.8-1
- Update to 3.0.8

* Fri Apr  1 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.7-1
- Update to 3.0.7

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.6-1
- Update to 3.0.6

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.5-1
- Update to 3.0.5

* Mon Mar 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.4-1
- Update to 3.0.4

* Mon Mar 14 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Mon Mar  7 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Sat Feb 26 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-2
- Fix frequent crashes on double-click events

* Mon Feb 21 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.99.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  1 2011 Matthias Clasen <mclasen@redhat.com> - 2.99.3-1
- Update to 2.99.3

* Mon Jan 24 2011 Dan Williams <dcbw@redhat.com> 2.99.2-2
- Fix bug in gtk_show_uri() which caused crashes when plugging in USB drives

* Wed Jan 12 2011 Matthias Clasen <mclasen@redhat.com> 2.99.2-1
- Update to 2.99.2

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.99.1-1
- Update to 2.99.1

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-3
- Obsolete gtk3-engines

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-2
- Provide the right directory for theming engines

* Thu Jan  6 2011 Matthias Clasen <mclasen@redhat.com> 2.99.0-1
- Update to 2.99.0
- Drop gtk-update-icon-cache and gtk-builder-convert to
  avoid conflict with gtk2
- Drop the tooltips-style patch for now

* Thu Dec  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.5-1
- Update to 2.91.5

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> 2.91.4-2
- Make gnome-terminal work again

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> 2.91.4-1
- Update to 2.91.4

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> 2.91.3-1
- Update to 2.91.3

* Wed Oct 20 2010 Richard Hughes <richard@hughsie.com> 2.91.1-1
- Update to 2.91.1

* Tue Oct 12 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-2
- Fix a crash in the tooltip code

* Sat Oct  2 2010 Matthias Clasen <mclasen@redhat.com> 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.7-3
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclaesn@redhat.com> 2.90.7-2
- Reinstate the tooltip look

* Mon Sep 20 2010 Bastien Nocera <bnocera@redhat.com> 2.90.7-1
- Update to 2.90.7

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.5-5
- Co-own /usr/share/gtk-doc
- gtk3-devel requires gdk-pixbuf2-devel

* Mon Jul 26 2010 Colin Walters <walters@verbum.org> - 2.90.5-4
- gtk3-devel requires gdk-pixbuf-devel

* Thu Jul 22 2010 Colin Walters <walters@verbum.org> - 2.90.5-2
- Rebuild with new gobject-introspection

* Mon Jul 22 2010 Matthias Clasen <mclasen@redhat.com> 2.90.5-1
- Update to 2.90.5

* Fri Jul  9 2010 Colin Walters <walters@verbum.org> - 2.90.4-3
- Update tooltip style patch to remove unused GdkRegion

* Tue Jun 29 2010 Colin Walters <walters@pocket> - 2.90.4-2
- Changes to support rebuilds from snapshots

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.90.4-1
- Update to 2.90.4

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> 2.90.3-1
- Update to 2.90.3

* Sat Jun 12 2010 Matthias Clasen <mclasen@redhat.com> 2.90.2-2
- Copy some tweaks from gtk2

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> 2.90.2-1
- Update to 2.90.2

* Tue May 25 2010 Matthias Clasen <mclasen@redhat.com> 2.90.1-1
- Update to 2.90.1

* Fri May 21 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-5
- Some more package review feedback

* Thu May 20 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-4
- Remove %%check again, it causes trouble

* Mon May 17 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-3
- More review feedback

* Wed May 12 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-2
- Incorporate review feedback

* Wed May 11 2010 Matthias Clasen <mclasen@redhat.com> 2.90.0-1
- Update to the 2.90.0 release
- Complete parallel installability

* Mon May 10 2010 Richard Hughes <richard@hughsie.com> 2.90.0-0.0.20100510git
- Update from git
