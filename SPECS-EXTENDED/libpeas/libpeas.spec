Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

%global apiver 1.0

Name:           libpeas
Version:        1.26.0
Release:        3%{?dist}
Summary:        Plug-ins implementation convenience library

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Libpeas
Source0:        https://download.gnome.org/sources/%{name}/1.26/%{name}-%{version}.tar.xz

BuildRequires:  %{_bindir}/xsltproc
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(pygobject-3.0)
BuildRequires:  python3-devel

%description
libpeas is a convenience library making adding plug-ins support
to glib-based applications.

%package gtk
Summary:        GTK+ plug-ins support for libpeas
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gtk
libpeas-gtk is a convenience library making adding plug-ins support
to GTK+-based applications.

%package loader-python3
Summary:        Python 3 loader for libpeas
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       python3-gobject

Obsoletes: libpeas-loader-python < %{version}-%{release}
Provides: libpeas-loader-python = %{version}-%{release}

%description loader-python3
This package contains the Python 3 loader that is needed to
run Python 3 plugins that use libpeas.

%package devel
Summary:        Development files for libpeas
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-gtk%{?_isa} = %{version}-%{release}

%description devel
This package contains development libraries and header files
that are needed to write applications that use libpeas.

%prep
%autosetup -p1

%build
%meson \
  -Ddemos=false \
  -Dvapi=true \
  -Dgtk_doc=false

%meson_build

%install
%meson_install

%find_lang libpeas-1.0

%ldconfig_scriptlets

%files -f libpeas-1.0.lang
%doc AUTHORS NEWS README
%license COPYING
%{_libdir}/libpeas-%{apiver}.so.0*
%dir %{_libdir}/libpeas-%{apiver}/
%dir %{_libdir}/libpeas-%{apiver}/loaders
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Peas-%{apiver}.typelib
%{_datadir}/icons/hicolor/*/actions/libpeas-plugin.*

%files gtk
%{_libdir}/libpeas-gtk-%{apiver}.so.0*
%{_libdir}/girepository-1.0/PeasGtk-%{apiver}.typelib

%files loader-python3
%{_libdir}/libpeas-%{apiver}/loaders/libpython3loader.so

%files devel
%{_includedir}/libpeas-%{apiver}/
%{_libdir}/libpeas-%{apiver}.so
%{_libdir}/libpeas-gtk-%{apiver}.so
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Peas-%{apiver}.gir
%{_datadir}/gir-1.0/PeasGtk-%{apiver}.gir
%{_libdir}/pkgconfig/libpeas-%{apiver}.pc
%{_libdir}/pkgconfig/libpeas-gtk-%{apiver}.pc

%changelog
* Mon Mar 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.26.0-3
- Adding BR on '%%{_bindir}/xsltproc'.
- Disabled gtk doc generation to remove network dependency during build-time.
- License verified.

* Wed Jul 14 2021 Muhammad Falak Wani <mwani@microsoft.com> - 1.26.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove dependency on gladeui

* Fri Mar 06 2020 Kalev Lember <klember@redhat.com> - 1.26.0-1
- Update to 1.26.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Kalev Lember <klember@redhat.com> - 1.25.3-1
- Update to 1.25.3

* Thu Oct 31 2019 Kalev Lember <klember@redhat.com> - 1.24.1-1
- Update to 1.24.1

* Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 1.24.0-1
- Update to 1.24.0

* Thu Sep 05 2019 Kalev Lember <klember@redhat.com> - 1.23.92-1
- Update to 1.23.92

* Tue Aug 20 2019 Kalev Lember <klember@redhat.com> - 1.23.90.1-2
- Revert inadvertent soname bump
- Tighten spec file globs to avoid accidental soname bumps in the future

* Tue Aug 20 2019 Kalev Lember <klember@redhat.com> - 1.23.90.1-1
- Update to 1.23.90.1
- Switch to the meson build system

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.22.0-14
- Rebuilt for Python 3.8

* Thu Aug 01 2019 Bastien Nocera <bnocera@redhat.com> - 1.22.0-13
+ libpeas-1.22.0-13
- Force disable the Python2 loader, which could still be built by accident (#1736043)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Charalampos Stratakis <cstratak@redhat.com> - 1.22.0-11
- Fix FTBFS with Python 3.8 (#1715665)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.22.0-8
- Rebuilt for Python 3.7

* Wed Jun 06 2018 Bastien Nocera <bnocera@redhat.com> - 1.22.0-7
+ libpeas-1.22.0-7
- Obsolete libpeas-loader-python

* Thu Mar 22 2018 Bastien Nocera <bnocera@redhat.com> - 1.22.0-6
+ libpeas-1.22.0-6
- Remove python2 loader, all GNOME apps using libpeas were ported to Python3
  when ported to GTK+ 3.x

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.22.0-4
- Switch to %%ldconfig_scriptlets

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.22.0-3
- Remove obsolete scriptlets

* Thu Nov 30 2017 Merlin Mathesius <mmathesi@redhat.com> - 1.22.0-2
- Cleanup spec file conditionals

* Sun Sep 10 2017 Kalev Lember <klember@redhat.com> - 1.22.0-1
- Update to 1.22.0

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 1.21.0-1
- Update to 1.21.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-0.3.gitbcc8644
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-0.2.gitbcc8644
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 1.21.0-0.1.gitbcc8644
- Update to 1.21.0 git snapshot

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.20.0-4
- Rebuild for Python 3.6

* Thu Nov 24 2016 Kalev Lember <klember@redhat.com> - 1.20.0-3
- Remove lib64 rpaths
- Update RHEL conditionals
- Fix directory ownership

* Tue Nov 08 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.20.0-2
- Trivial fixes in spec
- disable silent building
- use %%autosetup
- split out GTK+ support to the subpackage
- use %%make_build
- remove all libtool files in libdir
- drop unneeded chrpath calls

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 1.20.0-1
- Update to 1.20.0
- Don't set group tags

* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.18.0-1
- Update to 1.18.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Kalev Lember <klember@redhat.com> - 1.17.0-1
- Update to 1.17.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 1.16.0-1
- Update to 1.16.0
- Use make_install macro

* Fri Jul 03 2015 David King <amigadave@amigadave.com> - 1.15.0-3
- Split out Python 2 and 3 loaders into subpackages (#1226879)

* Fri Jun 26 2015 David King <amigadave@amigadave.com> - 1.15.0-2
- Add Requires for Python plugin support (#750925)

* Thu Jun 25 2015 David King <amigadave@amigadave.com> - 1.15.0-1
- Update to 1.15.0 (#1235615)
- Update URL
- Use license macro for COPYING
- Use pkgconfig for BuildRequires
- Add README and NEWS to doc

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 1.14.0-1
- Update to 1.14.0

* Mon Feb 16 2015 Richard Hughes <rhughes@redhat.com> - 1.13.0-1
- Update to 1.13.0

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.12.1-1
- Update to 1.12.1
- Tighten deps with the _isa macro

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Kalev Lember <kalevlember@gmail.com> - 1.10.1-1
- Update to 1.10.1

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.10.0-4
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 31 2014 Richard Hughes <rhughes@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Wed Feb 05 2014 Adam Williamson <awilliam@redhat.com> - 1.9.0-3
- drop gjs plugin support (backported from upstream; no-one wants it)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 1.9.0-1
- Update to 1.9.0

* Tue Mar 26 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 1.8.0-1
- Update to 1.8.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jan 06 2013 Ignacio Casal Quinteiro <icq@gnome.org> - 1.7.0-1
- Update to 1.7.0

* Wed Nov 28 2012 Kalev Lember <kalevlember@gmail.com> - 1.6.2-1
- Update to 1.6.2
- Avoid runtime deps on gtk-doc (#754495)

* Mon Nov 19 2012 Bastien Nocera <bnocera@redhat.com> 1.6.1-2
- Fix source URL

* Tue Oct 16 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 1.6.1-1
- Update to 1.6.1

* Tue Sep 25 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 1.6.0-1
- Update to 1.6.0

* Wed Sep 19 2012 Bastien Nocera <bnocera@redhat.com> 1.5.0-1
- Disable vala, as it was disabled upstream:
https://git.gnome.org/browse/libpeas/commit/?id=1031aaeeef282ab2bb65cb6ae48fa4abff453c4d

* Wed Jul 18 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 1.5.0-1
- Update to 1.5.0

* Thu May 03 2012 Kalev Lember <kalevlember@gmail.com> - 1.4.0-2
- Re-enable the GJS loader
- Remove unwanted lib64 rpaths

* Wed Mar 28 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 1.4.0-1
- Update to 1.4.0

* Fri Mar  2 2012 Matthias Clasen <mclasen@redhat.com> - 1.3.0-2
- Make seed optional for RHEL

* Sat Feb 25 2012 Ignacio Casal Quinteiro <icq@gnome.org> - 1.3.0-1
- Update to 1.3.0

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Wed Sep 28 2011 Ray <rstrode@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Wed Aug 31 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 1.1.3-1
- Update to 1.1.3

* Wed Aug 31 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 1.1.2-2
- Rebuild for latest pygobject3

* Tue Aug 23 2011 Adam Williamson <awilliam@redhat.com> - 1.1.2-1
- Update to 1.1.2
- bump BR to pygobject3-devel

* Wed Aug 03 2011 Bastien Nocera <bnocera@redhat.com> 1.1.1-3
- Another attempt at building against the latest gjs

* Wed Aug 03 2011 Bastien Nocera <bnocera@redhat.com> 1.1.1-2
- Rebuild for newer gjs

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 1.1.1-1
- Update to 1.1.1

* Tue Jun 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 1.1.0-1
- Update to 1.1.0

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> 1.0.0-1
- Update to 1.0.0

* Sun Mar 27 2011 Bastien Nocera <bnocera@redhat.com> 0.9.0-1
- Update to 0.9.0

* Thu Mar 10 2011 Bastien Nocera <bnocera@redhat.com> 0.7.4-1
- Update to 0.7.4

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> 0.7.3-1
- Update to 0.7.3
- Drop unneeded dependencies

* Mon Feb 21 2011 Bastien Nocera <bnocera@redhat.com> 0.7.2-1
- Update to 0.7.2

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.7.1-7
- Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 0.7.1-5
- Rebuild against newer gtk

* Fri Jan 28 2011 Bastien Nocera <bnocera@redhat.com> 0.7.1-4
- Update to real 0.7.1 release

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 0.7.1-3.gita2f98e
- Rebuild against newer gtk

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 0.7.1-2.gita2f98e
- Rebuild against newer gtk

* Thu Nov 11 2010 Dan Williams <dcbw@redhat.com> - 0.7.1-1.gita2f98e
- Update to 0.7.1
- Fix some crashes with missing introspection data

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> 0.7.0-2
- Rebuild against newer gtk3

* Mon Oct 04 2010 Bastien Nocera <bnocera@redhat.com> 0.7.0-1
- Update to 0.7.0

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.5-2
- Rebuild against newer gobject-introspection

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.5-1
- Update to 0.5.5

* Thu Aug  5 2010 Matthias Clasen <mclasen@redhat.com> - 0.5.4-1
- Update to 0.5.4

* Tue Jul 27 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> 0.5.3-2
- Rebuild against python 2.7

* Fri Jul 23 2010 Bastien Nocera <bnocera@redhat.com> 0.5.3-1
- Update to 0.5.3

* Thu Jul 22 2010 Bastien Nocera <bnocera@redhat.com> 0.5.2-5
- Fix post scriplet (#615021)

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.5.2-4
- Rebuild with new gobject-introspection

* Tue Jul 13 2010 Matthias Clasen <mclasen@redhat.com> 0.5.2-3
- Rebuild

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 0.5.2-2
- Rebuild against new gobject-introspection

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> 0.5.2-1
- Update to 0.5.2

* Thu Jul  8 2010 Matthias Clasen <mclasen@redhat.com> 0.5.1-2
- Rebuild

* Mon Jun 28 2010 Bastien Nocera <bnocera@redhat.com> 0.5.1-1
- Update to 0.5.1

* Thu Jun 24 2010 Bastien Nocera <bnocera@redhat.com> 0.5.0-4
- Document rpath work-arounds disabling, and remove verbose build

* Fri Jun 18 2010 Bastien Nocera <bnocera@redhat.com> 0.5.0-3
- Fix a number of comments from review request

* Mon Jun 14 2010 Bastien Nocera <bnocera@redhat.com> 0.5.0-2
- Call ldconfig when installing the package

* Mon Jun 14 2010 Bastien Nocera <bnocera@redhat.com> 0.5.0-1
- First package

