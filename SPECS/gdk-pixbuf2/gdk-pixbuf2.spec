%global glib2_version 2.48.0
Summary:        An image loading library
Name:           gdk-pixbuf2
Version:        2.40.0
Release:        5%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.gnome.org/GNOME/gdk-pixbuf
Source0:        https://download.gnome.org/sources/gdk-pixbuf/2.40/gdk-pixbuf-%{version}.tar.xz
BuildRequires:  gettext
BuildRequires:  gtk-doc
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  meson
BuildRequires:  pkg-config
# gdk-pixbuf does a configure time check which uses the GIO mime
# layer; we need to actually have the mime type database.
BuildRequires:  shared-mime-info
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 0.9.3
Requires:       glib2%{?_isa} >= %{glib2_version}
# We also need MIME information at runtime
Requires:       shared-mime-info

%description
gdk-pixbuf is an image loading library that can be extended by loadable
modules for new image formats. It is used by toolkits such as GTK+ or
clutter.

%package        modules
Summary:        Additional image modules for gdk-pixbuf
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description modules
This package contains the additional modules that are needed to load various
image formats such as ICO and JPEG.

%package        devel
Summary:        Development files for gdk-pixbuf
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glib2-devel%{?_isa} >= %{glib2_version}

%description devel
This package contains the libraries and header files that are needed
for writing applications that are using gdk-pixbuf.

%package        tests
Summary:        Tests for the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -n gdk-pixbuf-%{version} -p1

%build
%meson -Dbuiltin_loaders=png \
       -Ddocs=true \
       -Djasper=true \
       -Dx11=false

%meson_build

%install
%meson_install

touch %{buildroot}%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache

(cd %{buildroot}%{_bindir}
 mv gdk-pixbuf-query-loaders gdk-pixbuf-query-loaders-%{__isa_bits}
)

%find_lang gdk-pixbuf

%transfiletriggerin -- %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%transfiletriggerpostun -- %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache

%files -f gdk-pixbuf.lang
%license COPYING
%doc NEWS
%{_libdir}/libgdk_pixbuf-2.0.so.*
%{_libdir}/girepository-1.0
%dir %{_libdir}/gdk-pixbuf-2.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0
%dir %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders
%ghost %{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{_bindir}/gdk-pixbuf-query-loaders-%{__isa_bits}
%{_bindir}/gdk-pixbuf-thumbnailer
%{_mandir}/man1/gdk-pixbuf-query-loaders.1*
%{_datadir}/thumbnailers/

%files modules
%{_libdir}/gdk-pixbuf-2.0/2.10.0/loaders/*.so

%files devel
%dir %{_includedir}/gdk-pixbuf-2.0
%{_includedir}/gdk-pixbuf-2.0/gdk-pixbuf
%{_libdir}/libgdk_pixbuf-2.0.so
%{_libdir}/pkgconfig/gdk-pixbuf-2.0.pc
%{_bindir}/gdk-pixbuf-csource
%{_bindir}/gdk-pixbuf-pixdata
%{_datadir}/gir-1.0
%{_datadir}/gtk-doc/html/*
%{_mandir}/man1/gdk-pixbuf-csource.1*

%files tests
%{_libexecdir}/installed-tests
%{_datadir}/installed-tests

%changelog
* Fri Mar 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.40.0-5
- Bumping release to re-build with newer 'libtiff' libraries.

* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.40.0-4
- License verified
- Lint spec

* Thu Feb 25 2021 Henry Li <lihl@microsoft.com> - 2.40.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Disable Xlib dependencies 
- Add -Dx11=false to not use x11 when building
- Remove xlib and xlib-devel subpackages

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Kalev Lember <klember@redhat.com> - 2.40.0-1
- Update to 2.40.0

* Mon Aug 19 2019 Kalev Lember <klember@redhat.com> - 2.39.2-1
- Update to 2.39.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 28 2019 Kalev Lember <klember@redhat.com> - 2.38.1-1
- Update to 2.38.1

* Tue Feb 12 2019 Kalev Lember <klember@redhat.com> - 2.38.0-6
- Backport a patch to fix perl-Gtk3 build (#1676474)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 10 2018 Kalev Lember <klember@redhat.com> - 2.38.0-4
- Disable parallel make to work around thumbnailer generation issue (#1626835)

* Mon Sep 10 2018 Kalev Lember <klember@redhat.com> - 2.38.0-3
- Rebuilt to pick up all thumbnailers (#1626835)

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 2.38.0-2
- Rebuilt against fixed atk (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 2.38.0-1
- Update to 2.38.0
- Switch to the meson build system
- Remove ancient conflicts
- Remove ldconfig scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Apr 08 2018 Kalev Lember <klember@redhat.com> - 2.36.12-1
- Update to 2.36.12

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 06 2017 Kalev Lember <klember@redhat.com> - 2.36.11-1
- Update to 2.36.11

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 2.36.10-1
- Update to 2.36.10

* Mon Aug 21 2017 Kalev Lember <klember@redhat.com> - 2.36.9-1
- Update to 2.36.9

* Wed Aug 16 2017 Kalev Lember <klember@redhat.com> - 2.36.8-2
- Fix tiff loader to build again

* Tue Aug 08 2017 Kalev Lember <klember@redhat.com> - 2.36.8-1
- Update to 2.36.8

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Florian Weimer <fweimer@redhat.com> - 2.36.7-5
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Kalev Lember <klember@redhat.com> - 2.36.7-4
- Backport a patch to fix ico quality sorting

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Kalev Lember <klember@redhat.com> - 2.36.7-2
- Rebuilt for a s390x binutils issue

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 2.36.7-1
- Update to 2.36.7

* Thu Jul 13 2017 Bastien Nocera <bnocera@redhat.com> - 2.36.6-2
+ gdk-pixbuf2-2.36.6-2
- Fix crasher in jpeg loader

* Mon Apr 03 2017 Kalev Lember <klember@redhat.com> - 2.36.6-1
- Update to 2.36.6

* Mon Feb 13 2017 Kalev Lember <klember@redhat.com> - 2.36.5-1
- Update to 2.36.5

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Kalev Lember <klember@redhat.com> - 2.36.4-1
- Update to 2.36.4

* Wed Jan 04 2017 Kalev Lember <klember@redhat.com> - 2.36.3-1
- Update to 2.36.3

* Tue Dec 20 2016 Kalev Lember <klember@redhat.com> - 2.36.2-1
- Update to 2.36.2

* Tue Dec 13 2016 Kalev Lember <klember@redhat.com> - 2.36.1-1
- Update to 2.36.1

* Fri Dec 02 2016 Kalev Lember <klember@redhat.com> - 2.36.0-3
- Re-enable the libjasper JPEG-2000 loader now that it's getting maintainance
  upstream again

* Thu Oct 27 2016 Richard W.M. Jones <rjones@redhat.com> - 2.36.0-2
- Disable "silent rules".

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 2.36.0-1
- Update to 2.36.0

* Thu Sep 15 2016 Richard Hughes <rhughes@redhat.com> - 2.35.5-2
- Disable the libjasper JPEG-2000 loader because it's horribly insecure.

* Tue Sep 13 2016 Kalev Lember <klember@redhat.com> - 2.35.5-1
- Update to 2.35.5
- Don't set group tags

* Mon Aug 29 2016 Kalev Lember <klember@redhat.com> - 2.35.4-1
- Update to 2.35.4

* Thu Aug 04 2016 Kalev Lember <klember@redhat.com> - 2.35.3-1
- Update to 2.35.3

* Wed Jun 22 2016 Richard Hughes <rhughes@redhat.com> - 2.35.2-1
- Update to 2.35.2

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 2.35.1-1
- Update to 2.35.1

* Thu Mar 24 2016 Kalev Lember <klember@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.33.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Kalev Lember <klember@redhat.com> - 2.33.2-1
- Update to 2.33.2

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 2.33.1-1
- Update to 2.33.1

* Fri Sep 25 2015 Kalev Lember <klember@redhat.com> - 2.32.1-1
- Update to 2.32.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Sep 01 2015 Kalev Lember <klember@redhat.com> - 2.31.7-1
- Update to 2.31.7

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 2.31.6-1
- Update to 2.31.6
- Use make_install macro

* Wed Aug 05 2015 Kalev Lember <klember@redhat.com> - 2.31.5-3
- Use the right macro name in file triggers

* Wed Aug  5 2015 Matthias Clasen <mclasen@redhat.com> - 2.31.5-2
- Add file triggers

* Mon Jul 20 2015 David King <amigadave@amigadave.com> - 2.31.5-1
- Update to 2.31.5
- Use pkgconfig for some BuildRequires

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Kalev Lember <kalevlember@gmail.com> - 2.31.4-1
- Update to 2.31.4

* Fri Mar 20 2015 Richard Hughes <rhughes@redhat.com> - 2.31.3-5
- Fix a typo causing building applications to fail.

* Fri Mar 20 2015 Richard Hughes <rhughes@redhat.com> - 2.31.3-4
- Put the xlib headers in the right package.

* Fri Mar 20 2015 Richard Hughes <rhughes@redhat.com> - 2.31.3-3
- Split out the xlib code as a subpackage to allows us to depend on the core
  library on the cloud image and not depends on half of Xorg.

* Fri Mar 20 2015 Richard Hughes <rhughes@redhat.com> - 2.31.3-2
- Split out the modules as a subpackage to allows us to depend on the core
  library on the cloud image and not drag every image loader known to man.

* Sat Mar 07 2015 Kalev Lember <kalevlember@gmail.com> - 2.31.3-1
- Update to 2.31.3
- Use the %%license macro for the COPYING file

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.31.2-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Nov 23 2014 Kalev Lember <kalevlember@gmail.com> - 2.31.2-1
- Update to 2.31.2

* Mon Sep 01 2014 Kalev Lember <kalevlember@gmail.com> - 2.31.1-1
- Update to 2.31.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.31.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.31.0-2
- Rebuilt for gobject-introspection 1.41.4

* Sat Jul 19 2014 Kalev Lember <kalevlember@gmail.com> - 2.31.0-1
- Update to 2.31.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 2.30.8-1
- Update to 2.30.8

* Tue Mar 25 2014 Richard Hughes <rhughes@redhat.com> - 2.30.7-1
- Update to 2.30.7

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 2.30.6-1
- Update to 2.30.6

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 2.30.5-1
- Update to 2.30.5

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 2.30.4-1
- Update to 2.30.4

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 2.30.3-1
- Update to 2.30.3

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 2.30.2-1
- Update to 2.30.2

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 2.30.0-1
- Update to 2.30.0

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 2.29.3-1
- Update to 2.29.3
- Tighten deps with %%_isa

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.29.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 2.29.2-1
- Update to 2.29.2
- Add a tests subpackage

* Mon Jun 17 2013 Peter Robinson <pbrobinson@fedoraproject.org> 2.29.0-2
- Rebuild (libpng)

* Sat May 04 2013 Kalev Lember <kalevlember@gmail.com> - 2.29.0-1
- Update to 2.29.0

* Mon Apr 15 2013 Richard Hughes <rhughes@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 2.28.0-1
- Update to 2.28.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.27.3-1
- Update to 2.27.3

* Mon Mar 04 2013 Richard Hughes <rhughes@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.27.1-1
- Update to 2.27.1

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 2.27.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.27.0-1
- Update to 2.27.0

* Tue Jan 15 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.26.5-3
- Require glib2 >= 2.34.0 for g_type_ensure().

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 2.26.5-2
- rebuild against new libjpeg

* Mon Nov 12 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.5-1
- Update to 2.26.5

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.4-1
- Update to 2.26.4

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 2.26.2-1
- Update to 2.26.2

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Richard Hughes <hughsient@gmail.com> - 2.26.1-1
- Update to 2.26.1

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.26.0-1
- Update to 2.26.0

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.25.0-1
- Update to 2.25.0

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Rebuild against new libpng

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Jun 27 2011 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5 (fixes CVE-2011-2485)

* Wed Jun 15 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Wed Mar 30 2011 Matthias Clasen <mclasen@redhat.com> 2.23.3-1
- Update to 2.23.3

* Sat Mar  5 2011 Matthias Clasen <mclasen@redhat.com> 2.23.1-1
- Update to 2.23.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan  9 2011 Matthias Clasen <mclasen@redhat.com> 2.23.0-1
- Update to 2.23.0

* Fri Nov  5 2010 Matthias Clasen <mclasen@redhat.com> 2.22.1-1
- Update to 2.22.1

* Wed Sep 29 2010 jkeating - 2.22.0-2
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> 2.22.0-1
- Update to 2.22.0

* Mon Jul 19 2010 Bastien Nocera <bnocera@redhat.com> 2.21.6-3
- Require libpng for linking

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.21.6-2
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> - 2.21.6-1
- Update to 2.21.6

* Fri Jul  2 2010 Colin Walters <walters@verbum.org> - 2.21.5-4
- Also Require shared-mime-info for same reason

* Fri Jul  2 2010 Colin Walters <walters@verbum.org> - 2.21.5-3
- BR shared-mime-info; see comment above it

* Tue Jun 29 2010 Colin Walters <walters@pocket> - 2.21.5-2
- Changes to support snapshot builds

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.21.5-1
- Update to 2.21.5

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-2
- Rename to gdk-pixbuf2 to avoid conflict with the
  existing gdk-pixbuf package

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.4-1
- Update to 2.21.4
- Incorporate package review feedback

* Sat Jun 26 2010 Matthias Clasen <mclasen@redhat.com> 2.21.3-1
- Initial packaging
