Vendor:         Microsoft Corporation
Distribution:   Mariner
%global         clutter_version 1.23.7
%global         gtk3_version 3.21.0

%global         api_ver 1.0

Name:           clutter-gtk
Version:        1.8.4
Release:        8%{?dist}
Summary:        A basic GTK clutter widget

License:        LGPLv2+
URL:            http://www.clutter-project.org
Source0:        http://download.gnome.org/sources/clutter-gtk/1.8/clutter-gtk-%{version}.tar.xz

BuildRequires:  clutter-devel >= %{clutter_version}
BuildRequires:  gtk3-devel >= %{gtk3_version}
BuildRequires:  gobject-introspection-devel

Requires:       clutter%{?_isa} >= %{clutter_version}
Requires:       gtk3%{?_isa} >= %{gtk3_version}

%description
clutter-gtk is a library which allows the embedding of a Clutter
canvas (or "stage") into a GTK+ application, as well as embedding
GTK+ widgets inside the stage.

%package devel
Summary:        Clutter-gtk development environment
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
clutter-gtk.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags} V=1


%install
%make_install

#Remove libtool archives.
find %{buildroot} -type f -name "*.la" -delete

%find_lang cluttergtk-1.0

%check
make check %{?_smp_mflags} V=1


%ldconfig_scriptlets

%files -f cluttergtk-1.0.lang
%license COPYING
%doc NEWS
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/GtkClutter-%{api_ver}.typelib

%files devel
%{_includedir}/clutter-gtk-%{api_ver}/
%{_libdir}/pkgconfig/clutter-gtk-%{api_ver}.pc
%{_libdir}/*.so
%{_datadir}/gir-1.0/GtkClutter-%{api_ver}.gir
%{_datadir}/gtk-doc/html/clutter-gtk-1.0

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8.4-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.4-2
- Switch to %%ldconfig_scriptlets

* Wed Aug 09 2017 Kalev Lember <klember@redhat.com> - 1.8.4-1
- Update to 1.8.4

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 19 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.8.2-1
- Update to 1.8.0

* Mon Sep 05 2016 Kalev Lember <klember@redhat.com> - 1.8.0-2
- embed: remove non double buffer setting

* Wed Mar 30 2016 Kalev Lember <klember@redhat.com> - 1.8.0-1
- Update to 1.8.0
- Set minimum required gtk3 version

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 1.6.6-1
- Update to 1.6.6

* Tue Sep 15 2015 Kalev Lember <klember@redhat.com> - 1.6.4-1
- Update to 1.6.4
- Use make_install macro

* Tue Jun 30 2015 Kalev Lember <klember@redhat.com> - 1.6.2-1
- Update to 1.6.2
- Require minimum clutter 1.22.3 version
- Use license macro for COPYING

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.6.0-1
- Update to 1.6.0

* Sun Sep 07 2014 Kalev Lember <kalevlember@gmail.com> - 1.5.4-2
- Revert "Prefer the GDK windowing backend for Clutter" (#1134921, #1139052)

* Thu Aug 21 2014 Kalev Lember <kalevlember@gmail.com> - 1.5.4-1
- Update to 1.5.4
- Drop duplicate deps that rpmbuild autogenerates
- Drop an obsolete unused patch
- Tighten deps with %%{?_isa}

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.5.2-5
- Rebuilt for gobject-introspection 1.41.4

* Fri Jul 11 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.5.2-4
- Enable make check

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 1.5.2-2
- Rebuilt for cogl soname bump

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 1.4.4-5
- Rebuild for libevdev soname bump

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 1.4.4-4
- Rebuild for cogl soname bump

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.4-3
- Rebuilt for cogl 1.15.4 soname bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 1.4.4-1
- Update to 1.4.4

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 1.4.2-3
- Rebuilt for cogl soname bump

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.2-2
- Rebuild for new cogl

* Tue Dec 18 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.2-1
- New 1.4.2 stable release

* Fri Oct 19 2012 Peter Robinson <pbrobinson@fedoraproject.org> 1.4.0-1
- New 1.4.0 stable release

* Fri Aug 17 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.2-3
- Rebuild for new cogl

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun  6 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 1.1.2-5
- Rebuild against new cogl

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 1.1.2-4
- Rebuild against new cogl

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 1.1.2-3
- Rebuild against new cogl

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Matthias Clasen <mclasen@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Tue Sep 27 2011 Ray <rstrode@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.2-4
- Rebuild for clutter 1.8.0 again

* Tue Sep 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.2-3
- Rebuild for clutter 1.8.0

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> 1.0.2-2
- Rebuild

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> 1.0.2-1
- Update to 1.0.2

* Tue Apr  5 2011 Matthias Clasen <mclasen@redhat.com> 1.0.0-1
- Update to 1.0.0

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.91.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-2
- Rebuild against newer gtk

* Fri Jan 14 2011 Matthias Clasen <mclasen@redhat.com> 0.91.8-1
- Update to 0.91.8

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 0.91.6-2
- Rebuild against GTK+ 2.99.0

* Tue Dec 28 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.91.6-1
- Update to 0.91.6
- Fix deps and other bits of spec file

* Wed Dec 22 2010 Dan Horák <dan[at]danny.cz> - 0.91.4-2
- Update to recent gtk (FTBFS)

* Thu Nov 11 2010 Matthias Clasen <mclasen@redhat.com> - 0.91.4-1
- Update to 0.91.4

* Sun Oct 10 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.91.2-1
- Update to 0.91.2

* Wed Sep 29 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.90.2-3
- Add upstream patches to compile with latest gobject-introspection

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> 0.90.2-2
- Rebuild against newer gobject-introspection

* Wed Sep  1 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.90.2-1
- Update to 0.90.2

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 0.10.4-5
- Rebuild with new gobject-introspection
- Drop gir-repository-devel

* Mon May  3 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.4-3
- cleanup removal of libtool archives

* Wed Mar 24 2010 Bastien Nocera <bnocera@redhat.com> 0.10.4-2
- Move the API docs to -devel

* Sun Mar 21 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.4-1
- Update to 0.10.4

* Wed Jul 29 2009 Bastien Nocera <bnocera@redhat.com> 0.10.2-1
- Update to 0.10.2

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Bastien Nocera <bnocera@redhat.com> 0.9.2-1
- Update to 0.9.2

* Sat Jun 20 2009 Bastien Nocera <bnocera@redhat.com> 0.9.0-2
- Rebuild for new clutter

* Tue May 26 2009 Bastien Nocera <bnocera@redhat.com> 0.9.0-1
- Update to 0.9.0

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Fri Jan 23 2009 Allisson Azevedo <allisson@gmail.com> 0.8.2-2
- Rebuild

* Wed Oct 15 2008 Allisson Azevedo <allisson@gmail.com> 0.8.2-1
- Update to 0.8.2

* Sat Sep  6 2008 Allisson Azevedo <allisson@gmail.com> 0.8.1-1
- Update to 0.8.1

* Thu Jun 26 2008 Colin Walters <walters@redhat.com> 0.6.1-1
- Update to 0.6.1 so we can make tweet go
- Loosen files globs so we don't have to touch them every version

* Thu Feb 21 2008 Allisson Azevedo <allisson@gmail.com> 0.6.0-1
- Update to 0.6.0

* Mon Sep  3 2007 Allisson Azevedo <allisson@gmail.com> 0.4.0-1
- Update to 0.4.0

* Thu May 10 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-3
- fix devel files section

* Thu May 10 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-2
- INSTALL removed from docs
- fix make install for keeping timestamps
- fix devel files section
- changed license for LGPL

* Fri Apr 13 2007 Allisson Azevedo <allisson@gmail.com> 0.1.0-1
- Initial RPM release
