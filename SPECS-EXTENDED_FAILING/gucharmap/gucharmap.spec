Vendor:         Microsoft Corporation
Distribution:   Mariner
%define glib2_version 2.32.0
# this is already higher than the minimum supported upstream
%define gtk3_version 3.15.9

Name:           gucharmap
Version:        13.0.5
Release:        2%{?dist}
Summary:        Unicode character picker and font browser

License:        GPLv3+ and GFDL and MIT
# GPL for the source code, GFDL for the docs, MIT for Unicode data
URL:            https://wiki.gnome.org/Apps/Gucharmap
Source:         https://gitlab.gnome.org/GNOME/gucharmap/-/archive/%{version}/gucharmap-%{version}.tar.bz2
Patch0:         %{name}-gcc11.patch

BuildRequires:  appdata-tools
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  gtk3-devel >= %{gtk3_version}
BuildRequires:  gobject-introspection-devel
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate
BuildRequires:  unicode-ucd
BuildRequires:  unicode-ucd-unihan
BuildRequires:  vala
BuildRequires:  perl(Env)

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
This program allows you to browse through all the available Unicode
characters and categories for the installed fonts, and to examine their
detailed properties. It is an easy way to find the character you might
only know by its Unicode name or code point.

%package libs
Summary: libgucharmap library

%description libs
The %{name}-libs package contains the libgucharmap library.

%package devel
Summary: Libraries and headers for libgucharmap
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The gucharmap-devel package contains header files and other resources
needed to use the libgucharmap library.

%prep
%autosetup -p1

%build
%meson -Ducd_path=%{_datadir}/unicode/ucd -Ddocs=false

%meson_build

%install
%meson_install

# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
appstream-util replace-screenshots $RPM_BUILD_ROOT%{_datadir}/metainfo/gucharmap.metainfo.xml \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/gucharmap/a.png \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/gucharmap/b.png

%find_lang gucharmap --with-gnome

%check
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/gucharmap.desktop

%files -f gucharmap.lang
%license COPYING COPYING.GFDL COPYING.UNICODE
%doc README.md
%{_bindir}/gucharmap
%{_datadir}/applications/gucharmap.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.Charmap.gschema.xml
%{_datadir}/metainfo/gucharmap.metainfo.xml

%files libs
%license COPYING
%{_libdir}/libgucharmap_2_90.so.*
%{_libdir}/girepository-1.0/

%files devel
%{_includedir}/gucharmap-2.90
%{_libdir}/libgucharmap_2_90.so
%{_libdir}/pkgconfig/gucharmap-2.90.pc
%{_datadir}/gir-1.0
%{_datadir}/vala/vapi/gucharmap-2.90.deps
%{_datadir}/vala/vapi/gucharmap-2.90.vapi

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 13.0.5-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Sat Jan 09 2021 Alexander Ploumistos <alexpl@fedoraproject.org> - 13.0.5-1
- Update to 13.0.5

* Sat Nov 14 2020 Jeff Law <law@redhat.com> - 13.0.4-2
- Fix bogus volatile caught by gcc-11

* Sun Oct 04 2020 Alexander Ploumistos <alexpl@fedoraproject.org> - 13.0.4-1
- Update to 13.0.4

* Sun Sep 13 2020 Alexander Ploumistos <alexpl@fedoraproject.org> - 13.0.3-1
- Update to 13.0.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 21 2020 Alexander Ploumistos <alexpl@fedoraproject.org> - 13.0.2-2
- Drop intltool and itstool from BR
- Remove unneeded _smp_mflags macro

* Sat Apr 25 2020 Alexander Ploumistos <alexpl@fedoraproject.org> - 13.0.2-1
- Update to 13.0.2

* Wed Apr 15 2020 Alexander Ploumistos <alexpl@fedoraproject.org> - 13.0.1-1
- Update to 13.0.1
- Switch to meson build system
- Enable vala bindings

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Alexander Ploumistos <alexpl@fedoraproject.org> - 12.0.1-3
- Build against newer unicode-ucd - fix RHBZ#1735327
- Add Debian patch for Unicode 12.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 12.0.1-1
- Update to 12.0.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 12.0.0-1
- Update to 12.0.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Kalev Lember <klember@redhat.com> - 11.0.3-1
- Update to 11.0.3

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 11.0.2-2
- Rebuilt against fixed atk (#1626575)

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 11.0.2-1
- Update to 11.0.2
- Drop ldconfig scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 10.0.4-1
- Update to 10.0.4

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 10.0.3-2
- Remove obsolete scriptlets

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 10.0.3-1
- Update to 10.0.3

* Mon Oct 09 2017 Kalev Lember <klember@redhat.com> - 10.0.2-1
- Update to 10.0.2

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 10.0.1-1
- Update to 10.0.1

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 21 2017 Kalev Lember <klember@redhat.com> - 10.0.0-1
- Update to 10.0.0

* Wed May 10 2017 Kalev Lember <klember@redhat.com> - 9.0.4-1
- Update to 9.0.4

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 9.0.3-1
- Update to 9.0.3

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 23 2016 Kalev Lember <klember@redhat.com> - 9.0.2-1
- Update to 9.0.2

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 9.0.1-1
- Update to 9.0.1
- Update project URLs
- Move desktop file validation to check section

* Tue Jul 26 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 9.0.0-1
- Update for https://fedoraproject.org/wiki/Changes/Unicode_9.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 3.17.90-2
- Split out gucharmap-libs
- Minor spec file cleanup

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 10 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 3.16.0-2
- Use better AppData screenshots

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92
- Use license macro for the COPYING file
- Tighten -devel deps with the _isa macro

* Tue Jan 20 2015 Richard Hughes <rhughes@redhat.com> - 3.15.0-1
- Update to 3.15.0

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Sun Sep 21 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Thu Nov 14 2013 Richard Hughes <rhughes@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 3.9.99-1
- Update to 3.9.99

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Richard Hughes <rhughes@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.6.1-3
- Drop the desktop file vendor prefix

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 13 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.1-1
- Update to 3.6.1

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.99-1
- Update to 3.5.99

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Richard Hughes <hughsient@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.0-1
- Update to 3.5.0

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1.1-2
- Silence rpm scriptlet output

* Tue Apr 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1.1-1
- Update to 3.4.1.1

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.0.1-1
- Update to 3.4.0.1

* Wed Mar  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.1-2
- Fix pc file

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.1-1
- Update to 3.3.1

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.0-1
- Update to 3.3.0

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.2-1
- Update to 3.2.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Sat May 07 2011 Christopher Aillon <caillon@redhat.com> - 3.0.1-2
- Update scriptlets

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Feb 24 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-6
- Enable introspection

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-5
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.33.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-3
- Rebuild

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-2
- Rebuild

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.33.2-1
- Update to 2.33.2

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.2-0.2.gitc50414f
- Rebuild against new gtk

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.2-0.1.gitc50414f
- Git snapshot that builds against new gtk3

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.0-3
- Update license field to match changed license (#639133)

* Wed Oct  6 2010 Paul Howarth <paul@city-fan.org> - 2.33.0-2
- gtk2 dependencies become gtk3 dependencies

* Mon Oct  4 2010 Matthias Clasen <mclasen@redhat.com> - 2.33.0-1
- Update to 2.33.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Thu Aug 19 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Thu Mar 11 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Fri Dec  4 2009 Matthias Clasen <mclasen@redhat.com> - 2.29.1-1
- Update to 2.29.1

* Mon Oct 19 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.3.1-2
- Fix some stubborn button images

* Sun Jul 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.3.1-1
- Update to 2.26.3.1

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Thu Jan 15 2009 Matthias Clasen <mclasen@redhat.com> - 2.24.3-1
- Update to 2.24.3

* Mon Oct 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Wed Oct  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Mon Aug  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Tue Jul 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.23.4-2
- fix license tag

* Tue Jun 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Sun Mar  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Wed Jan 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Tue Jan 15 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Dec 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.4-1
- Update to 2.21.4

* Thu Dec  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.3-1
- Update to 2.21.3

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.0-2
- Update license field
- Use %%find_lang for help files

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 1.8.0-1
- Update to 1.8.0
- Require pgkconfig for the -devel package

* Wed Aug 02 2006 Behdad Esfahbod <besfahbo@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.6.0-8.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-8
- Add missing BuildRequires

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-7
- Rebuild

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-6
- Make -devel require the exact n-v-r

* Tue Apr 18 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-5
- incorporate more package review feedback

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-4
- split off a -devel package

* Mon Apr 17 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-3
- fix issues pointed out in package review

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> 1.6.0-2
- Initial revision
