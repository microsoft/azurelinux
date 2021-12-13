Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:		libchamplain
Version:	0.12.20
Release:	3%{?dist}
Summary:	Map view for Clutter

License:	LGPLv2+
URL:		https://wiki.gnome.org/Projects/libchamplain
Source0:	https://download.gnome.org/sources/libchamplain/0.12/%{name}-%{version}.tar.xz

BuildRequires:	clutter-devel
BuildRequires:	clutter-gtk-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	libsoup-devel
BuildRequires:	meson
BuildRequires:	sqlite-devel
BuildRequires:	gtk3-devel
BuildRequires:	vala

%description
Libchamplain is a C library aimed to provide a ClutterActor to display
rasterized maps.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	%{name}-gtk%{?_isa} = %{version}-%{release}
Obsoletes:	%{name}-gtk-devel < 0.12.12
Provides:	%{name}-gtk-devel = %{version}-%{release}
Obsoletes:	%{name}-vala < 0.12.8-1
Obsoletes:	%{name}-demos < 0.12.20-1

%description devel
This package contains development files for %{name}.

%package gtk
Summary:	Gtk+ widget wrapper for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gtk
Libchamplain-gtk is a library providing a GtkWidget to embed %{name}
into Gtk+ applications.

%prep
%setup -q

%build
%meson -Dgtk_doc=true
%meson_build

%install
%meson_install

%ldconfig_scriptlets
%ldconfig_scriptlets gtk

%files
%license COPYING
%doc AUTHORS README.md NEWS
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Champlain-0.12.typelib
%{_libdir}/libchamplain-0.12.so.0*

%files devel
%{_includedir}/champlain-0.12/
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Champlain-0.12.gir
%{_datadir}/gir-1.0/GtkChamplain-0.12.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/champlain-0.12/
%{_datadir}/vala/vapi/champlain-0.12.deps
%{_datadir}/vala/vapi/champlain-0.12.vapi
%{_datadir}/vala/vapi/champlain-gtk-0.12.deps
%{_datadir}/vala/vapi/champlain-gtk-0.12.vapi
%{_libdir}/libchamplain-0.12.so
%{_libdir}/libchamplain-gtk-0.12.so
%{_libdir}/pkgconfig/champlain-0.12.pc
%{_libdir}/pkgconfig/champlain-gtk-0.12.pc

%files gtk
%{_libdir}/girepository-1.0/GtkChamplain-0.12.typelib
%{_libdir}/libchamplain-gtk-0.12.so.0*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12.20-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Kalev Lember <klember@redhat.com> - 0.12.20-1
- Update to 0.12.20
- Drop separate -demos subpackage

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 03 2019 Kalev Lember <klember@redhat.com> - 0.12.19-1
- Update to 0.12.19
- Switch to the meson build system

* Thu Feb 21 2019 Kalev Lember <klember@redhat.com> - 0.12.18-1
- Update to 0.12.18

* Thu Feb 21 2019 Kalev Lember <klember@redhat.com> - 0.12.17-2
- Switch back to autotools as the meson build incorrectly bumps soname
- Tighten soname globs

* Wed Feb 20 2019 Kalev Lember <klember@redhat.com> - 0.12.17-1
- Update to 0.12.17
- Switch to the meson build system

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 30 2018 Debarshi Ray <rishi@fedoraproject.org> - 0.12.16-4
- Update URL and Source0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 07 2017 Kalev Lember <klember@redhat.com> - 0.12.16-1
- Update to 0.12.16

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 08 2017 Kalev Lember <klember@redhat.com> - 0.12.15-1
- Update to 0.12.15

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 0.12.14-2
- BR vala instead of obsolete vala-tools subpackage

* Wed Sep 07 2016 Kalev Lember <klember@redhat.com> - 0.12.14-1
- Update to 0.12.14
- Don't set group tags
- Avoid runtime requires on gobject-introspection

* Mon Feb 29 2016 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.13-1
- Update to 0.12.13

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 05 2015 Kalev Lember <klember@redhat.com> - 0.12.12-1
- Update to 0.12.12
- Simplify -devel subpackages

* Fri Sep 18 2015 Kalev Lember <klember@redhat.com> - 0.12.11-1
- Update to 0.12.11
- Use make_install macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 18 2015 Kalev Lember <kalevlember@gmail.com> - 0.12.10-1
- Update to 0.12.10
- Use license macro for the COPYING file

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 0.12.9-1
- Update to 0.12.9
- Tighten deps with the _isa macro

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.12.8-2
- Rebuilt for gobject-introspection 1.41.4

* Wed Jul 02 2014 Kalev Lember <kalevlember@gmail.com> - 0.12.8-1
- Update to 0.12.8
- Drop upstreamed patches
- Fix a -devel multilib conflict (#565676)
- Drop separate -vala subpackage and ship the vala files in -devel

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014 Adam Williamson <awilliam@redhat.com> - 0.12.7-3
- backport upstream fix for touch scrolling

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 0.12.7-2
- Rebuilt for cogl soname bump

* Thu Feb 06 2014 Kalev Lember <kalevlember@gmail.com> - 0.12.7-1
- Update to 0.12.7

* Wed Feb 05 2014 Kalev Lember <kalevlember@gmail.com> - 0.12.6-2
- Rebuilt for cogl soname bump

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 0.12.6-1
- Update to 0.12.6

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 0.12.5-1
- Update to 0.12.5

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 0.12.4-4
- Rebuilt for cogl 1.15.4 soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 0.12.4-2
- Don't ship ChangeLog (we need to save space on the live image)

* Fri May 17 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.4-1
- Update to 0.12.4
- http://ftp.gnome.org/pub/GNOME/sources/libchamplain/0.12/libchamplain-0.12.4.news

* Fri Jan 25 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.12.3-5
- Rebuild for new libcogl.

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.12.3-4
- Rebuild for new cogl

* Sun Aug 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.12.3-3
- Rebuild for new libcogl.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.3-1
- Update to 0.12.3
- http://ftp.gnome.org/pub/GNOME/sources/libchamplain/0.12/libchamplain-0.12.3.news

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 0.12.2-1
- Update to 0.12.2

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 0.12.1-5
- Rebuild for new cogl

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 0.12.1-4
- Rebuild for new cogl

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 0.12.1-3
- Rebuild for new cogl

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.1-1
- Update to 0.12.1
- http://ftp.gnome.org/pub/GNOME/sources/libchamplain/0.12/libchamplain-0.12.1.news

* Thu Nov 24 2011 Daniel Drake <dsd@laptop.org> - 0.12.0-3
- Add upstream patches to fix build against glib-2.31

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 0.12.0-2
- Rebuild against new clutter

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.12.0-1
- Update to 0.12.0
- http://ftp.gnome.org/pub/GNOME/sources/libchamplain/0.12/libchamplain-0.12.0.news

* Mon Sep  5 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.11.0-1
- Update to 0.11.0 devel release

* Sat Jun 11 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.0-4
- Cleanup requires
- Move demos to separate package

* Mon Apr 18 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.0-3
- Drop gtk-doc dep from devel package (RHBZ # 604381)
- Cleanup requires

* Fri Apr 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.10.0-2
- Bump build

* Mon Apr  4 2011 Tomas Bzatek <tbzatek@redhat.com> - 0.10.0-1
- Update to 0.10.0

* Sun Apr  3 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.1-1
- Version bump to 0.9.1.

* Tue Mar 22 2011 Brian Pepple <bpepple@fedoraproject.org> - 0.9.0-2
- Drop the reconfigure since it's no longer needed.

* Tue Feb 22 2011  Matthias Clasen <mclasen@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.8.1-3
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> - 0.8.1-1
- Update to 0.8.1

* Wed Sep 29 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 0.8.0-1
- update to 0.8.0
- patch configure* to look for clutter-gtk-1.0
- conditionalize python bindings

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 0.6.1-5
- Rebuild against newer gobject-introspection

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.6.1-3
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.6.1-2
- Rebuild against new gobject-introspection

* Mon Jul  5 2010 Peter Robinson <pbrobinson@fedoraproject.org> - 0.6.1-1
- Version bump to 0.6.1. Enable python and vala bindings
  http://ftp.gnome.org/pub/GNOME/sources/libchamplain/0.6/libchamplain-0.6.1.news

* Fri Apr 23 2010 Debarshi Ray <rishi@fedoraproject.org> - 0.4.5-1
- Version bump to 0.4.5.
  * Asynchronously load the tiles from the cache.
  * GObject Introspection is in a working state.
  * Limit the internal operations that happen when the user moves.
  * Limit the number of times the scale is redrawn.
  * Optimized the initialization process. Only the needed tiles are loaded.
  * Properly get rid of marker's previous image properly.
  * Removed the need to explicitly set the size of actors.
  * Deprecated champlain_view_set_size in favor of clutter_actor_set_size.
    (GNOME Bugzilla #580372)
  * Load the tiles in spiral order. (GNOME Bugzilla #606393)
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.5.news
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.4.news
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.5.changes
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.4.changes
- Added 'BuildRequires: chrpath' for removing rpaths.
- Added README to %%doc.
- Added demos/markers.h to %%doc of libchamplain-gtk-devel.

* Sun Jan 17 2010 Debarshi Ray <rishi@fedoraproject.org> - 0.4.3-1
- Version bump to 0.4.3.
  * A new scale.
  * User configurable additional license text to view.
  * An option to highlight points in polygons.
  * Fixed segmentation fault in function cairo_set_generator.
    (GNOME Bugzilla #604784)
  * Fixed segmentation fault when polygon has been deleted before redraw.
  * Made queue_redraw visible to subclasses.
  * Some memory usage improvements by reusing images already loaded.
  * Don't eat clicks on the map when using ChamplainSelectionLayer.
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.3.news
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.3.changes

* Thu Oct 29 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.4.2-1
- Version bump to 0.4.2.
  * Fixed acceptable values of "decel-rate". (GNOME Bugzilla #595552)
  * Fixed GObject Introspection build failure. (GNOME Bugzilla #598942)
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.2.news
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.2.changes

* Mon Oct 19 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.4.1-1
- Version bump to 0.4.1.
  * Added champlain_view_remove_layer.
  * ChamplainSelectionLayer now has a "changed" signal.
  * Added champlain_marker_get_highlighted_text_color,
    champlain_marker_set_highlighted_text_color and
    Added champlain_marker_get_highlighted_color.
  * Fixed slowdowns with big caches.
  * Don't emit invalid latitude and longitude notifications.
  * Ensure map is displayed in Eye of GNOME's champlain plugin. (GNOME
    Bugzilla #598106)
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.1.news
  * http://download.gnome.org/sources/libchamplain/0.4/libchamplain-0.4.1.changes

- Enabled GObject Introspection, and added 'Requires: gobject-introspection'
  and 'BuildRequires: gir-repository-devel'. Patched to fix build failure.
  (GNOME Bugzilla #598942)
- Explicitly disabled debug code.
- RPaths fixed by upstream. Removed 'BuildRequires: chrpath'.

* Mon Sep 21 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.4.0-1
- Version bump to 0.4.0.
  * ChamplainView now has keyboard shortcuts (but not when used with
    GtkChamplainEmbed).
  * Removed deprecated symbols introduced in 0.3.
  * Fixed X error when using GtkChamplainEmbed. (GNOME Bugzilla #590692)
  * Events were not being sent until the mouse moved. (GNOME Bugzilla #590727)
  * Fixed memory leak in ChamplainLayer. (GNOME Bugzilla #593505)
  * Initial center_on should not result on the map being in Antarctica.
    (GNOME Bugzilla #594963)
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.92.news
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.92.changes

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 0.3.91-1
- Version bump to 0.3.91.
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.91.news

* Tue Aug 11 2009 Matthias Clasen <mclasen@redhat.com> - 0.3.90-1
- Version bump to 0.3.90.
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.90.news
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.90.changes

* Mon Aug  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.3.6-1
- Version bump to 0.3.6.
  * New marker animation API.
  * Ported to Clutter 1.0. (GNOME Bugzilla #576391)
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.6.news
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.6.changes

* Sun Aug 02 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.3.5-1
- Version bump to 0.3.5.
  * Marker selection API. (GNOME Bugzilla #577909)
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.5.news
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.4.news
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.5.changes
  * http://download.gnome.org/sources/libchamplain/0.3/libchamplain-0.3.4.changes

* Fri Jul 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.3.3-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.3.3-1
- Version bump to 0.3.3.
  * Support for custom map sources and listing available map sources.
  * Smooth movement to a new position. (GNOME Bugzilla #557641)
  * Keep the center of the map in the center after a resize. (GNOME Bugzilla
    #557642)
  * Double click to zoom and center. (GNOME Bugzilla #557644)
  * Added a way to know the maximum and minimum zoom level. (GNOME Bugzilla
    #557965)
  * Fixed unwanted wrap effect when panning at zoom level >= 8. (GNOME
    Bugzilla #558020)
  * Fixed center on and zooming in behavior. (GNOME Bugzilla #558026)
  * Lack of user feedback during loading of tiles. (GNOME Bugzilla #559522)
  * Added missing zoom level to OpenStreetMap Mapnik. (GNOME Bugzilla
    #559446)
  * Fixed wrong elastic effect affecting Emapthy's map view. (GNOME Bugzilla
    #561700)
  * Added disk cache management. (GNOME Bugzillla #568931)
  * Host application should be able to limit the maximum and minimum zoom
    levels. (GNOME Bugzilla #571702)
  * Allow host applications to draw lines/routes on the map. (GNOME Bugzilla
    #572377)
  * Support proxies. (GNOME Bugzilla #573937)
  * Provide a way to make visible a bunch of markers. (GNOME Bugzilla #574809)
  * Do not allow negative zoom levels. (GNOME Bugzilla #575138)
  * Fixed corrupted map when double-clicking at maximum level. (GNOME Bugzilla
    #575139)
  * Prevent ChamplainNetworkMapSource from crashing when setting "proxy-uri".
    (GNOME Bugzilla #575902).
  * Implemented advanced markers. (GNOME Bugzilla #576055)
  * Various memory management fixes for ChamplainTile. (GNOME Bugzilla
    #576159)
  * Any go_to should stop a previous and not yet finished go_to. (GNOME
    Bugzilla #576832)
  * Prevent segmentation fault on 32 bit platforms. (GNOME Bugzilla #576698)
  * Introduced a new signal called ChamplainView::animation-completed. (GNOME
    Bugzilla #577169)
  * Set decel-rate correctly. (GNOME Bugzilla #580785)
  * champlain_network_map_source_fill_tile should be private. (GNOME Bugzilla
    #582786)
  * Fixed champlain_view_center_on. (GNOME Bugzilla #583502)
  * Fixed "longitude" and "latitude" properties, which were reversed. (GNOME
    Bugzilla #584365)
  * Make the cache work the first time. (GNOME Bugzilla #584390)
  * GNOME Goal: use accessor functions instead direct access. (GNOME Bugzilla
    #585698)
- Added 'BuildRequires: chrpath' for removing rpaths.

* Wed Mar 18 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.2.9-1
- Version bump to 0.2.9.
  * Fixed elastic effect.
  * Reduced exported symbols.

* Wed Feb 25 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.2.8-3
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.2.8-2
- Removed 'Requires: clutter-devel >= 0.8 pkgconfig' from libchamplain-devel
  for all distributions, except Fedora 10.
- Fixed sample code to not use generic headers.

* Wed Jan 14 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.2.8-1
- Initial build. Imported SPEC from openSUSE.
  * Added a new constructor for ChamplainMarkers made of an image.
  * Double clicking on the map will now zoom and recenter.
  * When resizing a ChamplainView, the centered content will still be
    centered after the resizing. Can be disabled.
  * The Map's license is displayed by default on the lower right corner. 
  * Fixed map centering on startup.
  * Fixed missing zoom level in OpenStreetMap Mapnik.
  * Fixed zooming and centering behaviour. (GNOME Bugzilla #558026)
