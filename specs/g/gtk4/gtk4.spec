## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora}
%global with_broadway 1
%endif

%global glib2_version 2.80.0
%global pango_version 1.56.0
%global cairo_version 1.18.0
%global gdk_pixbuf_version 2.30.0
%global gstreamer_version 1.24.0
%global harfbuzz_version 8.4
%global wayland_protocols_version 1.31
%global wayland_version 1.21.0
%global epoxy_version 1.4

%global bin_version 4.0.0

# Filter provides for private modules
%global __provides_exclude_from ^%{_libdir}/gtk-4.0

# FTBFS on i686 with GCC 14 -Werror=int-conversion
# https://gitlab.gnome.org/GNOME/gtk/-/issues/6033
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%ifarch %{ix86}
%global build_type_safety_c 1
%endif
%endif

Name:           gtk4
Version:        4.20.3
Release:        %autorelease
Summary:        GTK graphical user interface library

# Most files are either LGPL-2.0-or-later or LGPL-2.1-or-later.
# gtk/roaring/ and gtk/timsort/ are Apache-2.0
# .editorconfig is CC0-1.0
# po/kg.po is LGPL-2.0-or-later
# po/po2tbl.sed.in is GPL-2.0-or-later
# tests/testscrolledge.c is GPL-3.0-or-later
# gdk/macos/gdkmacoskeymap.c and testsuite/gsk/shader.c are (LGPL-2.1-or-later AND MIT)
# .gitlab-ci/pages/fonts.css is LGPL-2.1-or-later AND OFL-1.0 but omitted here because it's not part of the binary RPM
# gdk/x11/gdkxftdefaults.c LGPL-2.1-or-later AND HPND-sell-variant
# gdk/x11/gdkasync.c is LGPL-2.1-or-later AND MIT-open-group
# gdk/win32/winpointer.h is LGPL-2.0-or-later AND ZPL-2.1
# The following files are HPND-sell-variant:
#  gdk/x11/xsettings-client.c
#  gdk/x11/xsettings-client.h
#  gtk/gtk-text-input.xml
#  gtk/text-input-unstable-v3.xml
# The following files are MIT:
#  demos/gtk-demo/css_multiplebgs.css
#  demos/gtk-demo/gtkgears.c
#  gdk/win32/gdkkeys-win32-impl-wow64.c
#  gdk/win32/gdkkeys-win32-impl.c
#  gdk/win32/gdkkeys-win32.h
#  gtk/inspector/css-editor.c
#  gtk/inspector/css-editor.h
#  gtk/inspector/css-node-tree.h
#  gtk/inspector/init.c
#  gtk/inspector/inspect-button.c
#  gtk/inspector/logs.c
#  gtk/inspector/logs.h
#  gtk/inspector/object-tree.c
#  gtk/inspector/object-tree.h
#  gtk/inspector/prop-list.c
#  gtk/inspector/prop-list.h
#  gtk/inspector/window.c
#  gtk/inspector/window.h
#  tests/gtkgears.c
# testsuite/gsk/fonts/Cantarell-VF.otf is OFL-1.1
#
# The license was last checked for GTK 4.19.3.
License:        LGPL-2.0-or-later AND LGPL-2.1-or-later AND Apache-2.0 AND CC0-1.0 AND MIT AND MIT-open-group AND HPND-sell-variant AND GPL-2.0-or-later AND GPL-3.0-or-later AND OFL-1.1
URL:            https://www.gtk.org
Source0:        https://download.gnome.org/sources/gtk/4.20/gtk-%{version}.tar.xz

BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  glslc
BuildRequires:  meson
BuildRequires:  python3-gobject
BuildRequires:  pkgconfig(avahi-gobject)
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
BuildRequires:  pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires:  pkgconfig(colord)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(graphene-gobject-1.0)
BuildRequires:  pkgconfig(gstreamer-player-1.0) >= %{gstreamer_version}
BuildRequires:  pkgconfig(harfbuzz) >= %{harfbuzz_version}
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(pango) >= %{pango_version}
BuildRequires:  pkgconfig(sysprof-capture-4)
BuildRequires:  pkgconfig(tracker-sparql-3.0)
BuildRequires:  pkgconfig(vulkan)
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
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/rst2man

# standard icons
Requires: adwaita-icon-theme
# required for icon theme apis to work
Requires: hicolor-icon-theme
# split out in a subpackage
Requires: gtk-update-icon-cache

Requires: cairo%{?_isa} >= %{cairo_version}
Requires: cairo-gobject%{?_isa} >= %{cairo_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: harfbuzz%{?_isa} >= %{harfbuzz_version}
Requires: libepoxy%{?_isa} >= %{epoxy_version}
Requires: gstreamer1-plugins-bad-free-libs%{?_isa} >= %{gstreamer_version}
Requires: libwayland-client%{?_isa} >= %{wayland_version}
Requires: libwayland-cursor%{?_isa} >= %{wayland_version}
Requires: pango%{?_isa} >= %{pango_version}

# make sure we have a reasonable gsettings backend
Recommends: dconf%{?_isa}

%description
GTK is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 4 of GTK.

%package devel
Summary: Development files for GTK
Requires: gtk4%{?_isa} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications with version 4 of the GTK widget toolkit.

%package devel-docs
Summary: Developer documentation for GTK
BuildArch: noarch
Requires: gtk4 = %{version}-%{release}
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends: gi-docgen-fonts

%description devel-docs
This package contains developer documentation for version 4 of the GTK
widget toolkit.

%package devel-tools
Summary: Developer tools for GTK
Requires: gtk4%{?_isa} = %{version}-%{release}

%description devel-tools
This package contains helpful applications for developers using GTK.

%prep
%autosetup -p1 -n gtk-%{version}

%build
export CFLAGS='-std=c11 -fno-strict-aliasing -DG_DISABLE_CAST_CHECKS -DG_DISABLE_ASSERT %optflags'
%meson \
%if 0%{?with_broadway}
        -Dbroadway-backend=true \
%endif
        -Dsysprof=enabled \
        -Dtracker=enabled \
        -Dcolord=enabled \
        -Ddocumentation=true \
        -Dman-pages=true \
        -Dbuild-testsuite=false \
        -Dbuild-tests=false \
        -Dbuild-examples=false

%meson_build

%install
%meson_install

%find_lang gtk40

%if !0%{?with_broadway}
rm $RPM_BUILD_ROOT%{_mandir}/man1/gtk4-broadwayd.1*
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-4.0
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-4.0/modules

%check
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_metainfodir}/*.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

%files -f gtk40.lang
%license COPYING
%doc AUTHORS NEWS README.md
%{_bindir}/gtk4-launch
%{_bindir}/gtk4-update-icon-cache
%{_libdir}/libgtk-4.so.1{,.*}
%dir %{_libdir}/gtk-4.0
%{_libdir}/gtk-4.0/modules
%{_libdir}/girepository-1.0/
%{_mandir}/man1/gtk4-launch.1*
%{_mandir}/man1/gtk4-update-icon-cache.1*
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Inspector.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.EmojiChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.FileChooser.gschema.xml
%dir %{_datadir}/gtk-4.0
%{_datadir}/gtk-4.0/emoji/
%if 0%{?with_broadway}
%{_bindir}/gtk4-broadwayd
%{_mandir}/man1/gtk4-broadwayd.1*
%endif

%files devel
%{_libdir}/libgtk-4.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk4-builder-tool
%{_bindir}/gtk4-encode-symbolic-svg
%{_bindir}/gtk4-path-tool
%{_bindir}/gtk4-query-settings
%{_datadir}/bash-completion/completions/gtk4-builder-tool
%{_datadir}/gettext/
%{_datadir}/gir-1.0/
%{_datadir}/gtk-4.0/gtk4builder.rng
%{_datadir}/gtk-4.0/valgrind/
%{_mandir}/man1/gtk4-builder-tool.1*
%{_mandir}/man1/gtk4-encode-symbolic-svg.1*
%{_mandir}/man1/gtk4-path-tool.1*
%{_mandir}/man1/gtk4-query-settings.1*

%files devel-docs
%{_datadir}/doc/gdk4/
%{_datadir}/doc/gdk4-wayland/
%{_datadir}/doc/gdk4-x11/
%{_datadir}/doc/gsk4/
%{_datadir}/doc/gtk4/

%files devel-tools
%{_bindir}/gtk4-demo
%{_bindir}/gtk4-demo-application
%{_bindir}/gtk4-image-tool
%{_bindir}/gtk4-node-editor
%{_bindir}/gtk4-print-editor
%{_bindir}/gtk4-rendernode-tool
%{_bindir}/gtk4-widget-factory
%{_datadir}/applications/org.gtk.gtk4.NodeEditor.desktop
%{_datadir}/applications/org.gtk.Demo4.desktop
%{_datadir}/applications/org.gtk.PrintEditor4.desktop
%{_datadir}/applications/org.gtk.WidgetFactory4.desktop
%{_datadir}/bash-completion/completions/gtk4-demo
%{_datadir}/bash-completion/completions/gtk4-image-tool
%{_datadir}/bash-completion/completions/gtk4-node-editor
%{_datadir}/bash-completion/completions/gtk4-path-tool
%{_datadir}/bash-completion/completions/gtk4-print-editor
%{_datadir}/bash-completion/completions/gtk4-rendernode-tool
%{_datadir}/bash-completion/completions/gtk4-widget-factory
%{_datadir}/icons/hicolor/*/apps/org.gtk.gtk4.NodeEditor*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.Demo4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.PrintEditor4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.WidgetFactory4*.svg
%{_datadir}/glib-2.0/schemas/org.gtk.Demo4.gschema.xml
%{_metainfodir}/org.gtk.gtk4.NodeEditor.appdata.xml
%{_metainfodir}/org.gtk.Demo4.appdata.xml
%{_metainfodir}/org.gtk.PrintEditor4.appdata.xml
%{_metainfodir}/org.gtk.WidgetFactory4.appdata.xml
%{_mandir}/man1/gtk4-demo.1*
%{_mandir}/man1/gtk4-demo-application.1*
%{_mandir}/man1/gtk4-image-tool.1*
%{_mandir}/man1/gtk4-node-editor.1*
%{_mandir}/man1/gtk4-rendernode-tool.1*
%{_mandir}/man1/gtk4-widget-factory.1*

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 4.20.3-2
- Latest state for gtk4

* Wed Dec 10 2025 Adrian Vovk <adrianvovk@gmail.com> - 4.20.3-1
- Update to 4.20.3

* Tue Sep 30 2025 David King <amigadave@amigadave.com> - 4.20.2-1
- Update to 4.20.2

* Wed Sep 10 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 4.20.1-1
- Update to 4.20.1

* Tue Sep 02 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 4.20.0-2
- Stop requiring gdk-pixbuf-modules

* Fri Aug 29 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 4.20.0-1
- Update to 4.20.0

* Thu Aug 28 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 4.19.4-4
- Change OFL-1.1-no-RFN to OFL-1.1

* Tue Aug 26 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 4.19.4-3
- Update license field again

* Tue Aug 26 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 4.19.4-2
- Update license field

* Tue Aug 19 2025 nmontero <nmontero@redhat.com> - 4.19.4-1
- Update to 4.19.4

* Tue Aug 05 2025 nmontero <nmontero@redhat.com> - 4.19.3-1
- Update to 4.19.3

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Milan Crha <mcrha@redhat.com> - 4.19.2-1
- Update to 4.19.2

* Mon May 05 2025 nmontero <nmontero@redhat.com> - 4.19.1-1
- Update to 4.19.1

* Mon Apr 07 2025 nmontero <nmontero@redhat.com> - 4.19.0-1
- Update to 4.19.0

* Thu Apr 03 2025 nmontero <nmontero@redhat.com> - 4.18.3-1
- Update to 4.18.3

* Mon Mar 17 2025 nmontero <nmontero@redhat.com> - 4.18.2-1
- Update to 4.18.2

* Thu Mar 06 2025 nmontero <nmontero@redhat.com> - 4.17.6-1
- Update to 4.17.6

* Mon Mar 03 2025 nmontero <nmontero@redhat.com> - 4.17.5-1
- Update to 4.17.5

* Thu Feb 06 2025 nmontero <nmontero@redhat.com> - 4.17.4-3
- Rebuild for the renaming of tracker to tinysparql

* Thu Feb 06 2025 nmontero <nmontero@redhat.com> - 4.17.4-2
- Rebuild for the renaming of tracker to tinysparql

* Mon Feb 03 2025 nmontero <nmontero@redhat.com> - 4.17.4-1
- Update to 4.17.4

* Wed Jan 22 2025 nmontero <nmontero@redhat.com> - 4.17.3-1
- Update to 4.17.3

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 nmontero <nmontero@redhat.com> - 4.17.2-1
- Update to 4.17.2

* Mon Dec 09 2024 nmontero <nmontero@redhat.com> - 4.17.1-1
- Update to 4.17.1

* Thu Nov 07 2024 nmontero <nmontero@redhat.com> - 4.17.0-1
- Update to 4.17.0

* Mon Nov 04 2024 nmontero <nmontero@redhat.com> - 4.16.5-1
- Update to 4.16.5

* Sun Oct 06 2024 David King <amigadave@amigadave.com> - 4.16.3-1
- Update to 4.16.3

* Tue Sep 24 2024 nmontero <nmontero@redhat.com> - 4.16.2-1
- Update to 4.16.2

* Thu Sep 19 2024 nmontero <nmontero@redhat.com> - 4.16.1-1
- Update to 4.16.1

* Wed Sep 11 2024 Adam Williamson <awilliam@redhat.com> - 4.16.0-2
- Backport MR #7704 to fix printing with only one printer

* Sat Sep 07 2024 David King <amigadave@amigadave.com> - 4.16.0-1
- Update to 4.16.0

* Tue Aug 27 2024 David King <amigadave@amigadave.com> - 4.15.6-1
- Update to 4.15.6

* Mon Aug 26 2024 Adam Williamson <awilliam@redhat.com> - 4.15.5-3
- Revert "Backport MR #7633 to fix X session issues affecting Budgie"

* Mon Aug 26 2024 Adam Williamson <awilliam@redhat.com> - 4.15.5-2
- Backport MR #7633 to fix X session issues affecting Budgie

* Mon Aug 12 2024 David King <amigadave@amigadave.com> - 4.15.5-1
- Update to 4.15.5

* Sat Aug 03 2024 David King <amigadave@amigadave.com> - 4.15.4-1
- Update to 4.15.4

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.15.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Nieves Montero <nmontero@redhat.com> - 4.15.3-1
- Update to 4.15.3

* Wed May 22 2024 David King <amigadave@amigadave.com> - 4.15.1-1
- Update to 4.15.1

* Mon Apr 22 2024 Nieves Montero <nmontero@redhat.com> - 4.15.0-1
- Update to GTK 4.15.0

* Fri Apr 19 2024 David King <amigadave@amigadave.com> - 4.14.3-1
- Update to 4.14.3

* Tue Apr 09 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 4.14.2-2
- Add patch to hopefully fix Snapshot crash on startup

* Fri Apr 05 2024 David King <amigadave@amigadave.com> - 4.14.2-1
- Update to 4.14.2

* Tue Mar 19 2024 David King <amigadave@amigadave.com> - 4.14.1-1
- Update to 4.14.1

* Wed Mar 13 2024 David King <amigadave@amigadave.com> - 4.14.0-1
- Update to 4.14.0

* Tue Mar 05 2024 David King <amigadave@amigadave.com> - 4.13.9-1
- Update to 4.13.9

* Wed Feb 28 2024 Adam Williamson <awilliam@redhat.com> - 4.13.8-2
- Backport MR #6927 to fix gnome-text-editor crash

* Wed Feb 21 2024 David King <amigadave@amigadave.com> - 4.13.8-1
- Update to 4.13.8

* Mon Feb 12 2024 David King <amigadave@amigadave.com> - 4.13.7-1
- Update to 4.13.7

* Wed Feb 07 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 4.13.6-2
- Reduce GCC 14 type safety on i686

* Fri Jan 26 2024 David King <amigadave@amigadave.com> - 4.13.6-1
- Update to 4.13.6

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.13.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 14 2024 Kalev Lember <klember@redhat.com> - 4.13.5-2
- Add explicit vulkan build dep

* Wed Jan 10 2024 Kalev Lember <klember@redhat.com> - 4.13.5-1
- Update to 4.13.5

* Wed Jan 03 2024 Kalev Lember <klember@redhat.com> - 4.13.4-1
- Update to 4.13.4

* Wed Nov 15 2023 Kalev Lember <klember@redhat.com> - 4.13.3-1
- Update to 4.13.3

* Wed Oct 25 2023 Kalev Lember <klember@redhat.com> - 4.13.2-1
- Update to 4.13.2
- Package new gtk4-path-tool in -devel subpackage

* Tue Oct 03 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 4.12.3-2
- Remove unused settings.ini from git repo

* Thu Sep 28 2023 Kalev Lember <klember@redhat.com> - 4.12.3-1
- Update to 4.12.3

* Wed Sep 27 2023 Kalev Lember <klember@redhat.com> - 4.12.2-3
- Backport MR #6437 to fix crash when printing from loupe (rhbz#2240222)

* Thu Sep 21 2023 Kalev Lember <klember@redhat.com> - 4.12.2-2
- Fix the build with sysprof 45

* Wed Sep 20 2023 Kalev Lember <klember@redhat.com> - 4.12.2-1
- Update to 4.12.2

* Thu Sep 07 2023 Kalev Lember <klember@redhat.com> - 4.12.1-3
- Validate appstream metadata

* Thu Sep 07 2023 Kalev Lember <klember@redhat.com> - 4.12.1-2
- Add missing trailing slashes to directory entries in files list

* Fri Aug 25 2023 Kalev Lember <klember@redhat.com> - 4.12.1-1
- Update to 4.12.1

* Thu Aug 17 2023 Kalev Lember <klember@redhat.com> - 4.12.0-6
- Backport upstream patch to fix .pc file requires

* Tue Aug 15 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 4.12.0-5
- Drop special hint settings, remove settings.ini

* Tue Aug 15 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 4.12.0-4
- Drop special hint settings, remove settings.ini

* Tue Aug 15 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 4.12.0-3
- Ensure correct fonts are installed for HTML docs

* Mon Aug 07 2023 Kalev Lember <klember@redhat.com> - 4.12.0-2
- Backport a patch to fix undefined symbols in the cups backend

* Sat Aug 05 2023 Kalev Lember <klember@redhat.com> - 4.12.0-1
- Update to 4.12.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Kalev Lember <klember@redhat.com> - 4.11.4-1
- Update to 4.11.4

* Wed Jun 07 2023 Kalev Lember <klember@redhat.com> - 4.11.3-1
- Update to 4.11.3

* Wed May 10 2023 David King <amigadave@amigadave.com> - 4.11.2-1
- Update to 4.11.2

* Mon Apr 10 2023 David King <amigadave@amigadave.com> - 4.11.1-1
- Update to 4.11.1

* Tue Mar 14 2023 David King <amigadave@amigadave.com> - 4.10.1-1
- Update version

* Tue Mar 14 2023 David King <amigadave@amigadave.com> - 4.10.0-5
- Update to 4.10.1

* Mon Mar 13 2023 David King <amigadave@amigadave.com> - 4.10.0-4
- Fix combo box allocations

* Fri Mar 10 2023 Adam Williamson <awilliam@redhat.com> - 4.10.0-3
- Rebuild with no changes for F38 Bodhi purposes

* Thu Mar 09 2023 Ray Strode <rstrode@redhat.com> - 4.10.0-2
- Short most recent files first in Recent Files in file chooser

* Sun Mar 05 2023 David King <amigadave@amigadave.com> - 4.10.0-1
- Update to 4.10.0

* Wed Feb 15 2023 David King <amigadave@amigadave.com> - 4.9.4-1
- Update to 4.9.4

* Thu Feb 09 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 4.9.3-3
- Remove librest-0.7 BuildRequires

* Mon Feb 06 2023 David King <amigadave@amigadave.com> - 4.9.3-1
- Update to 4.9.3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 30 2022 David King <amigadave@amigadave.com> - 4.9.2-1
- Update to 4.9.2

* Tue Nov 29 2022 Adam Williamson <awilliam@redhat.com> - 4.9.1-2
- Bring back focus fix (MR #5189), it wasn't in 4.9.1

* Mon Nov 21 2022 David King <amigadave@amigadave.com> - 4.9.1-1
- Update to 4.9.1

* Tue Nov 01 2022 Adam Williamson <awilliam@redhat.com> - 4.8.2-2
- Attempt to fix a focus issue introduced in 4.8.2 (nautilus gl2574)
- Backport MR #5091 to fix a width problem (gtk gl5192)

* Thu Oct 27 2022 David King <amigadave@amigadave.com> - 4.8.2-1
- Update to 4.8.2

* Mon Sep 26 2022 Kalev Lember <klember@redhat.com> - 4.8.1-2
- Rebuild

* Fri Sep 16 2022 Kalev Lember <klember@redhat.com> - 4.8.1-1
- Update to 4.8.1

* Wed Sep 07 2022 Kalev Lember <klember@redhat.com> - 4.8.0-1
- Update to 4.8.0

* Tue Aug 16 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 4.7.2-2
- Enable font hinting (#1943794)

* Thu Aug 11 2022 Kalev Lember <klember@redhat.com> - 4.7.2-1
- Update to 4.7.2

* Mon Jul 25 2022 Kalev Lember <klember@redhat.com> - 4.7.1-3
- Work around broken rpm pkg-config dep extraction

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Kalev Lember <klember@redhat.com> - 4.7.1-1
- Update to 4.7.1

* Mon May 09 2022 David King <amigadave@amigadave.com> - 4.7.0-1
- Update to 4.7.0

* Thu Apr 28 2022 David King <amigadave@amigadave.com> - 4.6.3-1
- Update to 4.6.3

* Tue Apr 26 2022 Adam Williamson <awilliam@redhat.com> - 4.6.2-3
- Fix from Benjamin for gtk_widget_measure infinite loop issue (#2071228)

* Thu Mar 31 2022 Adam Williamson <awilliam@redhat.com> - 4.6.2-2
- Backport MR #4605 to fix portal save/load dialogs on X (#2068041)

* Sat Mar 19 2022 David King <amigadave@amigadave.com> - 4.6.2-1
- Update to 4.6.2

* Wed Mar 02 2022 Adam Williamson <awilliam@redhat.com> - 4.6.1-2
- Backport MR#4366 to fix launching control-center panes from overview

* Mon Feb 14 2022 David King <amigadave@amigadave.com> - 4.6.1-1
- Update to 4.6.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 31 2021 David King <amigadave@amigadave.com> - 4.6.0-1
- Update to 4.6.0

* Fri Dec 17 2021 David King <amigadave@amigadave.com> - 4.5.1-1
- Update to 4.5.1

* Mon Nov 01 2021 Kalev Lember <klember@redhat.com> - 4.5.0-2
- Build -devel-docs as noarch (#2018991)

* Mon Nov 01 2021 Kalev Lember <klember@redhat.com> - 4.5.0-1
- Update to 4.5.0

* Mon Sep 27 2021 Kalev Lember <klember@redhat.com> - 4.4.0-4
- Build with tracker support enabled (#1908874)

* Mon Sep 20 2021 Kalev Lember <klember@redhat.com> - 4.4.0-3
- Stop creating empty theming-engines directory as it's no longer used

* Thu Sep 02 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 4.4.0-2
- Split developer tools out to devel-tools subpackage

* Mon Aug 23 2021 Kalev Lember <klember@redhat.com> - 4.4.0-1
- Update to 4.4.0
- Switch to using new gi-docgen package instead of the bundled copy
- Remove cloudproviders support again, as per upstream suggestion

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 05 2021 Kalev Lember <klember@redhat.com> - 4.2.1-1
- Update to 4.2.1

* Mon May 03 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.2.0-5
- Re-enable documentation.

* Tue Apr 20 2021 Kalev Lember <klember@redhat.com> - 4.2.0-4
- Enable cloudproviders support (#1951539)

* Tue Apr 06 2021 Kalev Lember <klember@redhat.com> - 4.2.0-3
- Backport upstream fix for typing apostrophes / single quotes (#1946133)

* Thu Apr 01 2021 Kalev Lember <klember@redhat.com> - 4.2.0-2
- Disable vulkan renderer

* Tue Mar 30 2021 Kalev Lember <klember@redhat.com> - 4.2.0-1
- Update to 4.2.0

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 4.1.2-2
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 4.1.2-1
- Update to 4.1.2
- Disable gtk-doc support as we don't have gi-docgen in Fedora yet
- Remove old obsoletes

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 4.1.1-1
- Update to 4.1.1
- Enable sysprof support

* Fri Feb 19 2021 Kalev Lember <klember@redhat.com> - 4.1.0-3
- Backport upstream patch to fix a settings schema loading issue on Wayland

* Mon Feb 01 2021 Kalev Lember <klember@redhat.com> - 4.1.0-2
- Disable asserts and cast checks

* Sun Jan 31 2021 Kalev Lember <klember@redhat.com> - 4.1.0-1
- Update to 4.1.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Kalev Lember <klember@redhat.com> - 4.0.2-2
- Avoid rebuilding stylesheets with sassc during the build

* Tue Jan 19 2021 Kalev Lember <klember@redhat.com> - 4.0.2-1
- Update to 4.0.2

* Sat Jan 09 2021 Kalev Lember <klember@redhat.com> - 4.0.1-1
- Update to 4.0.1

* Sat Jan 09 2021 Kalev Lember <klember@redhat.com> - 4.0.0-3
- Fix vulkan reference in pc file

* Tue Dec 22 14:13:09 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-2
- Add back gtk4-devel-docs

* Wed Dec 16 2020 Kalev Lember <klember@redhat.com> - 4.0.0-1
- Update to 4.0.0
- Tighten soname globs

* Fri Dec 11 2020 Kalev Lember <klember@redhat.com> - 3.99.5-1
- Update to 3.99.5

* Wed Dec 09 2020 Jeff Law <law@redhat.com> - 3.99.4-3
- Avoid diagnostics for gcc-11 false positive out of bounds accesses

* Sun Nov 15 2020 Jeff Law <law@redhat.com> - 3.99.4-2
- Fix bogus volatile caught by gcc-11

* Thu Nov  5 2020 Kalev Lember <klember@redhat.com> - 3.99.4-1
- Update to 3.99.4

* Fri Oct 16 2020 Kalev Lember <klember@redhat.com> - 3.99.3-1
- Update to 3.99.3

* Thu Oct 01 2020 Kalev Lember <klember@redhat.com> - 3.99.2-2
- Update required pango and glib2 versions

* Tue Sep 29 2020 Kalev Lember <klember@redhat.com> - 3.99.2-1
- Update to 3.99.2

* Mon Sep 28 2020 Jeff Law <law@redhat.com> - 3.99.1-2
- Re-enable LTO as upstream GCC target/96939 has been fixed

* Thu Sep 03 2020 Kalev Lember <klember@redhat.com> - 3.99.1-1
- Update to 3.99.1
- Drop wayland build conditionals

* Mon Aug 17 2020 Jeff Law <law@redhat.com> - 3.99.0-2
- Disable LTO on armv7hl

* Sat Aug 01 2020 Kalev Lember <klember@redhat.com> - 3.99.0-1
- Update to 3.99.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.98.5-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.98.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 Kalev Lember <klember@redhat.com> - 3.98.5-1
- Update to 3.98.5

* Tue May 19 2020 Kalev Lember <klember@redhat.com> - 3.98.4-1
- Update to 3.98.4

* Tue Apr 21 2020 Kalev Lember <klember@redhat.com> - 3.98.3-1
- Update to 3.98.3
- Temporarily disable built documentation as we don't have new enough gtk-doc

* Wed Apr 01 2020 Kalev Lember <klember@redhat.com> - 3.98.2-1
- Update to 3.98.2

* Sun Mar 22 2020 Kalev Lember <klember@redhat.com> - 3.98.1-1
- Update to 3.98.1

* Thu Mar 12 2020 Kalev Lember <klember@redhat.com> - 3.98.0-2
- Install missing gtkemojichooser.h (#1806509)

* Tue Feb 11 2020 Kalev Lember <klember@redhat.com> - 3.98.0-1
- Update to 3.98.0
- Use https for source URLs

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.96.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.96.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 3.96.0-1
- Update to 3.96.0
- Use GTK instead of GTK+ in descriptions
- Don't ship installed tests as they are currently broken

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.94.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 01 2018 Kalev Lember <klember@redhat.com> - 3.94.0-1
- Update to 3.94.0
- Remove and obsolete immodules subpackages
- Build new gstreamer media backend

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.92.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 3.92.1-3
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.92.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 02 2017 Kalev Lember <klember@redhat.com> - 3.92.1-1
- Update to 3.92.1
- Enable installed tests

* Tue Aug 08 2017 Kalev Lember <klember@redhat.com> - 3.91.2-1
- Update to 3.91.2

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 3.91.1-1
- Update to 3.91.1

* Wed Jun 14 2017 Kalev Lember <klember@redhat.com> - 3.91.0-2
- Disable installed tests due to file conflicts between gtk3-tests and
  gtk4-tests

* Wed Jun 14 2017 Kalev Lember <klember@redhat.com> - 3.91.0-1
- Initial Fedora packaging

## END: Generated by rpmautospec
