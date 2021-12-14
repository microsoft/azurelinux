Vendor:         Microsoft Corporation
Distribution:   Mariner
%global glib_version 2.48
%global gtk_version 3.22

Name:           gtksourceview4
Version:        4.6.1
Release:        2%{?dist}
Summary:        Source code editing widget

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/GtkSourceView
Source0:        https://download.gnome.org/sources/gtksourceview/4.6/gtksourceview-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gtk-doc
BuildRequires:  itstool
BuildRequires:  meson
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gladeui-2.0)
BuildRequires:  pkgconfig(glib-2.0) >= %{glib_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk_version}
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pango)
BuildRequires:  vala

Requires: glib2%{?_isa} >= %{glib_version}
Requires: gtk3%{?_isa} >= %{gtk_version}

%description
GtkSourceView is a GNOME library that extends GtkTextView, the standard GTK+
widget for multiline text editing. GtkSourceView adds support for syntax
highlighting, undo/redo, file loading and saving, search and replace, a
completion system, printing, displaying line numbers, and other features
typical of a source code editor.

This package contains version 4 of GtkSourceView.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        tests
Summary:        Tests for the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -n gtksourceview-%{version}

%build
%meson -Dgtk_doc=true -Dglade_catalog=true -Dinstall_tests=true
%meson_build

%install
%meson_install

%find_lang gtksourceview-4

%files -f gtksourceview-4.lang
%license COPYING
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GtkSource-4.typelib
%{_libdir}/libgtksourceview-4.so.0*
%{_datadir}/gtksourceview-4/

%files devel
%{_includedir}/gtksourceview-4/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libgtksourceview-4.so
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GtkSource-4.gir
%dir %{_datadir}/glade
%dir %{_datadir}/glade/catalogs
%{_datadir}/glade/catalogs/gtksourceview.xml
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/*
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gtksourceview-4.deps
%{_datadir}/vala/vapi/gtksourceview-4.vapi

%files tests
%dir %{_libexecdir}/installed-tests
%{_libexecdir}/installed-tests/gtksourceview-4/
%dir %{_datadir}/installed-tests
%{_datadir}/installed-tests/gtksourceview-4/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.6.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Jul 20 2020 Kalev Lember <klember@redhat.com> - 4.6.1-1
- Update to 4.6.1

* Sat Mar 07 2020 Kalev Lember <klember@redhat.com> - 4.6.0-1
- Update to 4.6.0

* Mon Feb 17 2020 Kalev Lember <klember@redhat.com> - 4.5.91-1
- Update to 4.5.91

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 4.4.0-1
- Update to 4.4.0

* Wed Sep 04 2019 Kalev Lember <klember@redhat.com> - 4.3.92-1
- Update to 4.3.92

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 29 2019 Phil Wyett <philwyett@kathenas.org> - 4.3.1-1
- Update to 4.3.1
- Convert to meson

* Sat Mar 16 2019 Kalev Lember <klember@redhat.com> - 4.2.0-1
- Update to 4.2.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 4.0.3-2
- Rebuilt against fixed atk (#1626575)

* Fri Sep 07 2018 Pete Walter <pwalter@fedoraproject.org> - 4.0.3-1
- Initial packaging of GtkSourceView 4
