# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           glade
Version:        3.40.0
Release: 14%{?dist}
Summary:        User Interface Designer for GTK+

# - /usr/bin/glade is GPLv2+
# - /usr/bin/glade-previewer is LGPLv2+
# - libgladeui-2.so, libgladegtk.so, and libgladepython.so all combine
#   GPLv2+ and LGPLv2+ code, so the resulting binaries are GPLv2+
# Automatically converted from old format: GPLv2+ and LGPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+
URL:            https://glade.gnome.org/
Source0:        https://download.gnome.org/sources/glade/3.40/glade-%{version}.tar.xz

BuildRequires:  desktop-file-utils
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gjs-devel
BuildRequires:  gtk3-devel
BuildRequires:  gtk-doc
BuildRequires:  itstool
BuildRequires:  libxml2-devel
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  python3-gobject-devel
BuildRequires:  webkit2gtk4.1-devel
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/xsltproc

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

BuildRequires: gobject-introspection-devel
%description
Glade is a RAD tool to enable quick and easy development of user interfaces for
the GTK+ toolkit and the GNOME desktop environment.

The user interfaces designed in Glade are saved as XML, which can be used in
numerous programming languages including C, C++, C#, Vala, Java, Perl, Python,
and others.


%package libs
Summary:        Widget library for Glade UI designer

%description    libs
The %{name}-libs package consists of the widgets that compose the Glade GUI as
a separate library to ease the integration of Glade into other applications.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use Glade widget library.


%prep
%autosetup -p1
# glade does not use libsoup, no other porting necessary
sed -i -e 's/webkit2gtk-4.0/webkit2gtk-4.1/' meson.build


%build
%meson -Dgtk_doc=true
%meson_build


%install
%meson_install

%find_lang glade --with-gnome


%check
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_datadir}/metainfo/org.gnome.Glade.appdata.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/org.gnome.Glade.desktop


%files -f glade.lang
%license COPYING*
%doc AUTHORS NEWS
%{_bindir}/glade
%{_bindir}/glade-previewer
%{_datadir}/applications/org.gnome.Glade.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.gnome.Glade.svg
%{_datadir}/icons/hicolor/symbolic/apps/glade-brand-symbolic.svg
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Glade-symbolic.svg
%{_datadir}/metainfo/org.gnome.Glade.appdata.xml
%{_mandir}/man1/glade.1*
%{_mandir}/man1/glade-previewer*

%files libs
%license COPYING*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Gladeui-2.0.typelib
%dir %{_libdir}/glade/
%dir %{_libdir}/glade/modules/
%{_libdir}/glade/modules/libgladegjs.so
%{_libdir}/glade/modules/libgladegtk.so
%{_libdir}/glade/modules/libgladepython.so
%{_libdir}/glade/modules/libgladewebkit2gtk.so
%{_libdir}/libgladeui-2.so.13*
%{_datadir}/glade/

%files devel
%{_includedir}/libgladeui-2.0/
%{_libdir}/libgladeui-2.so
%{_libdir}/pkgconfig/gladeui-2.0.pc
%dir %{_datadir}/gettext
%dir %{_datadir}/gettext/its
%{_datadir}/gettext/its/glade-catalog.its
%{_datadir}/gettext/its/glade-catalog.loc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Gladeui-2.0.gir
%doc %{_datadir}/gtk-doc/


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.40.0-12
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 3.40.0-10
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.40.0-8
- Rebuilt for Python 3.13

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 3.40.0-4
- Rebuilt for Python 3.12

* Sun Mar 26 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.40.0-3
- Use webkit2gtk-4.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 11 2022 Kalev Lember <klember@redhat.com> - 3.40.0-1
- Update to 3.40.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.38.2-7
- Rebuilt for Python 3.11

* Fri Jun 10 2022 Miro Hrončok <mhroncok@redhat.com> - 3.38.2-6
- Fix build with meson 0.61+
- Fixes: rhbz#2082581

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 3.38.2-3
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Kalev Lember <klember@redhat.com> - 3.38.2-1
- Update to 3.38.2
- Drop old obsoletes
- BR python3-gobject-devel rather than pygobject3-devel

* Mon Oct  5 2020 Kalev Lember <klember@redhat.com> - 3.38.1-1
- Update to 3.38.1

* Fri Oct 02 2020 Kalev Lember <klember@redhat.com> - 3.38.0-2
- Drop compat ABI version

* Sun Sep 13 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0
- Temporarily ship previous soname for ABI compat

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 3.37.0-1
- Update to 3.37.0
- Switch to the meson build system

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.36.0-3
- Rebuilt for Python 3.9

* Fri May 22 2020 Kalev Lember <klember@redhat.com> - 3.36.0-2
- Tighten libgladeui soname globs

* Thu May 07 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0
- Use https download URLs

* Wed Feb 26 2020 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.22.1-6
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 3.22.1-2
- Rebuilt for Python 3.7

* Tue Apr 03 2018 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 3.20.4-1
- Update to 3.20.4

* Sat Feb 24 2018 Kalev Lember <klember@redhat.com> - 3.20.3-1
- Update to 3.20.3
- Remove ldconfig scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.20.2-2
- Remove obsolete scriptlets

* Fri Dec 01 2017 Kalev Lember <klember@redhat.com> - 3.20.2-1
- Update to 3.20.2

* Thu Oct 12 2017 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1
- Fix gir directory ownership

* Mon Oct 02 2017 Karsten Hopp <karsten@redhat.com> - 3.20.0-6
- apply upstream patch from Jonh Wendell to fix g_ptr_array_find types and make it
  build with latest glib2

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.20.0-2
- Rebuild for Python 3.6

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 05 2015 Robert Kuska <rkuska@redhat.com> - 3.19.0-4
- Rebuilt for Python3.5 rebuild

* Fri Jul 03 2015 Kalev Lember <klember@redhat.com> - 3.19.0-3
- Switch to Python 3 (#1238957)
- Use the make_install macro
- Use upstream screenshots for appdata
- Validate appdata file
- Tighten deps with the _isa macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Kalev Lember <kalevlember@gmail.com> - 3.19.0-1
- Update to 3.19.0
- Use license macro for COPYING files

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 3.18.3-5
- Use better AppData screenshots

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.18.3-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.18.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.18.3-1
- Update to 3.18.3

* Wed Apr 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.18.2-1
- Update to 3.18.2

* Wed Mar 26 2014 Kalev Lember <kalevlember@gmail.com> - 3.18.1-1
- Update to 3.18.1

* Mon Mar 24 2014 Kalev Lember <kalevlember@gmail.com> - 3.18.0-1
- Update to 3.18.0

* Wed Jan 08 2014 Richard Hughes <rhughes@redhat.com> - 3.16.1-1
- Update to 3.16.1

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 3.16.0-1
- Update to 3.16.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.15.4-1
- Update to 3.15.4

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.15.3-1
- Update to 3.15.3

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 3.15.2-3.git9d3b3b3
- Update to git snapshot to adapt to API changes in GTK+ 3.9.10
- Add man pages

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.15.2-1
- Update to 3.15.2

* Fri May 10 2013 Richard Hughes <rhughes@redhat.com> - 3.15.1-1
- Update to 3.15.1

* Mon Mar 18 2013 Richard Hughes <rhughes@redhat.com> - 3.15.0-1
- Update to 3.15.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.14.2-2
- Revise the summary for consistency with the parallel installable
  glade2/glade3 packages (#882557)

* Mon Nov 26 2012 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0
- Remove the unrecognized --disable-scrollkeeper option

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.13.0-1
- Update to 3.13.0

* Sun May 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Thu Apr 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.12.0-3
- Update the spec file comments about licensing and simplify the License tag
- Install the typelib in -libs subpackage

* Fri Apr 06 2012 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Review fixes (#806093)
- Use find_lang --with-gnome for including help files
- Include license files also in the main package in addition to -libs

* Wed Apr 04 2012 Kalev Lember <kalevlember@gmail.com> - 3.12.0-1
- Update to 3.12.0

* Thu Mar 22 2012 Kalev Lember <kalevlember@gmail.com> - 3.11.0-1
- Initial packaging based on Fedora glade3
- Rename the package to glade; added obsoletes for upgrade path
- Spec clean up for review
