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

%global glib2_version 2.56.0
%global glycin_version 2.0.1

# Normally we want auto features enabled to ensure no important feature gets
# disabled by mistake. But in this package, the auto features are mostly legacy
# or unwanted, and we should manually enable only what we want.
%global __meson_auto_features disabled

Name:           gdk-pixbuf2
Version:        2.44.5
Release:        %autorelease
Summary:        An image loading library

License:        LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/gdk-pixbuf
Source0:        https://download.gnome.org/sources/gdk-pixbuf/2.44/gdk-pixbuf-%{version}.tar.xz

BuildRequires:  docbook-style-xsl
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(glycin-2) >= %{glycin_version}
BuildRequires:  libxslt
BuildRequires:  meson
BuildRequires:  pkgconfig(gobject-introspection-1.0)
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info
BuildRequires:  /usr/bin/rst2man

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: glycin-libs%{?_isa} >= %{glycin_version}
# We also need MIME information at runtime
Requires: shared-mime-info

# All modules previously provided by gdk-pixbuf itself are obsoleted by Glycin.
Obsoletes: %{name}-modules < %{version}-%{release}

# Most third-party pixbuf loaders are also obsolete. If Glycin supports the
# format, then it will take precedence and the third-party loader won't be used.
# The Provides can be removed when nothing in Fedora depends on them anymore.
Obsoletes: avif-pixbuf-loader <= 1.1.1-4
Provides:  avif-pixbuf-loader
Obsoletes: heif-pixbuf-loader <= 1.20.1-2
Provides:  heif-pixbuf-loader
Obsoletes: jxl-pixbuf-loader <= 0.11.1-4
Provides:  jxl-pixbuf-loader
Obsoletes: rsvg-pixbuf-loader <= 2.61.0-1
Provides:  rsvg-pixbuf-loader
Obsoletes: webp-pixbuf-loader <= 0.2.7-4
Provides:  webp-pixbuf-loader

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%package devel
Summary: Development files for gdk-pixbuf2
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: glib2-devel%{?_isa} >= %{glib2_version}
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends: gi-docgen-fonts

%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf2.

%package tests
Summary: Tests for the %{name} package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -n gdk-pixbuf-%{version} -p1

%build
%meson \
       -Ddocumentation=true \
       -Dintrospection=enabled \
       -Dglycin=enabled \
       %{nil}
%meson_build

%install
%meson_install

mkdir -p $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
touch $RPM_BUILD_ROOT%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

# Rename gdk-pixbuf-query-loaders
(cd $RPM_BUILD_ROOT%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)
# ... and fix up gdk-pixbuf-query-loaders reference in the .pc file
sed -i -e 's/gdk-pixbuf-query-loaders/gdk-pixbuf-query-loaders-%{__isa_bits}/' \
    $RPM_BUILD_ROOT%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc

%find_lang gdk-pixbuf

%transfiletriggerin -- %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%transfiletriggerpostun -- %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%files -f gdk-pixbuf.lang
%license COPYING
%doc NEWS README.md
%{_libdir}/libgdk_pixbuf-2.0.so.0{,.*}
%{_libdir}/girepository-1.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*

%files devel
%dir %{_includedir}/gdk-pixbuf-2.0
%{_includedir}/gdk-pixbuf-2.0/gdk-pixbuf
%{_libdir}/libgdk_pixbuf-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_datadir}/gir-1.0/
%{_mandir}/man1/gdk-pixbuf-csource.1*
%doc %{_datadir}/doc/gdk-pixbuf/
%doc %{_datadir}/doc/gdk-pixdata/

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.44.5-2
- Latest state for gdk-pixbuf2

* Thu Jan 29 2026 Barry Dunn <badunn@redhat.com> - 2.44.5-1
- Update to 2.44.5

* Fri Oct 24 2025 Matthias Clasen <mclasen@redhat.com> - 2.44.4-1
- Update to 2.44.4

* Mon Oct 20 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.44.3-3
- Another fix for .svgz in glycin-svg

* Sun Oct 12 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.44.3-2
- Fix loading of .svgz icons by the glycin-svg loader

* Tue Sep 30 2025 David King <amigadave@amigadave.com> - 2.44.3-1
- Update to 2.44.3

* Fri Sep 26 2025 Petr Schindler <pschindl@redhat.com> - 2.44.2-1
- Update to 2.44.2

* Mon Sep 15 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.44.1-1
- Update to 2.44.1

* Wed Sep 10 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.44.0-1
- Update to 2.44.0

* Fri Sep 05 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.43.5-2
- Add Provides for pixbuf-loaders, and an additional Obsoletes

* Thu Sep 04 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.43.5-1
- Update to 2.43.5, including some major changes

* Sat Aug 16 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.43.3-7
- Drop sort.patch

* Fri Aug 15 2025 Fabio Valentini <decathorpe@gmail.com> - 2.43.3-6
- Do not ship thumbnailer on multilib / i686

* Thu Aug 14 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.43.3-5
- Sort MIME types in the thumbnailer file

* Thu Jul 31 2025 Marek Kasik <mkasik@redhat.com> - 2.43.3-4
- Be more careful with chunked icc data

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.43.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Milan Crha <mcrha@redhat.com> - 2.43.3-2
- Disable glycin for i686 (not available there)

* Mon Jul 07 2025 Milan Crha <mcrha@redhat.com> - 2.43.3-1
- Update to 2.43.3

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.12-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Sep 20 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.42.12-9
- Recommend webp loader only on Fedora, redux

* Thu Aug 22 2024 Tomas Popela <tpopela@redhat.com> - 2.42.12-8
- Recommend webp loader only on Fedora

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 14 2024 Nieves Montero <nmontero@redhat.com> - 2.42.12-3
- Update to 2.42.12

* Wed Jun 12 2024 Nieves Montero <nmontero@redhat.com> - 2.42.12-2
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
