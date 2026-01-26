%define gettext_package libgnomecanvas-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: GnomeCanvas widget
Name: libgnomecanvas
Version: 2.30.3
Release: 33%{?dist}
URL: https://www.gnome.org/
Source0: https://download.gnome.org/sources/libgnomecanvas/2.30/%{name}-%{version}.tar.bz2
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2+
BuildRequires: gtk2-devel
BuildRequires: libart_lgpl-devel
BuildRequires: libglade2-devel 
BuildRequires: gail-devel
BuildRequires: libtool gettext
BuildRequires: intltool
BuildRequires: make

%description
The canvas widget allows you to create custom displays using stock items
such as circles, lines, text, and so on. It was originally a port of the
Tk canvas widget but has evolved quite a bit over time.

%package devel
Summary: Libraries and headers for libgnomecanvas
Requires: %{name} = %{version}-%{release}
# for /usr/share/gtk-doc/html
Requires: gtk-doc

%description devel
The canvas widget allows you to create custom displays using stock items
such as circles, lines, text, and so on. It was originally a port of the
Tk canvas widget but has evolved quite a bit over time.

%prep
%setup -q

%build
%configure --disable-gtk-doc --enable-glade --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} 

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%find_lang %{gettext_package}

%ldconfig_scriptlets

%files -f %{gettext_package}.lang
%doc AUTHORS NEWS README
%license COPYING.LIB
%{_libdir}/lib*.so.*
%{_libdir}/libglade/2.0/libcanvas.so

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gtk-doc/html/libgnomecanvas

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.30.3-33
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 2.30.3-30
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.30.3-3
- Rebuild against new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Christopher Aillon <caillon@redhat.com> 2.30.3-1
- Update to 2.30.3

* Thu Sep 30 2010 Matthias Clasen <mclasen@redhat.com> 2.30.2-1
- Update to 2.30.2

* Thu Sep 23 2010 Parag Nemade <paragn AT fedoraproject.org> 2.30.1-2
- Merge-review cleanup (#226012)

* Thu Apr  1 2010 Matthias Clasen <mclasen@redhat.com> 2.30.1-1
- Update to 2.30.1

* Wed Mar 31 2010 Matthias Clasen <mclasen@redhat.com> 2.30.0-1
- Update to 2.30.0

* Sat Feb 13 2010 Matthias Clasen <mclasen@redhat.com> 2.26.0-3
- Add missing libs

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> 2.26.0-1
- Update to 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> 2.25.90-2
- Update to 2.25.90
- Drop obsolete patches
- BR intltool

* Sun Nov 09 2008 Debarshi Ray <rishi@fedoraproject.org> 2.20.1.1-4
- Use 'Requires: libglade2 >= 2.6.3-2' to prevent unowned
  %%{_libdir}/libglade and %%{_libdir}/libglade/2.0.

* Sun Nov 09 2008 Debarshi Ray <rishi@fedoraproject.org> 2.20.1.1-3
- Disown %%{_libdir}/libglade and %%{_libdir}/libglade/2.0, and add
  'Requires: libglade2' instead.

* Sat Feb  9 2008 Matthias Clasen <mclasen@redhat.com> 2.20.1.1-2
- Rebuild for gcc 4.3

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> 2.20.1.1-1
- Update to 2.20.1.1

* Mon Nov 12 2007 Matthias Clasen <mclasen@redhat.com> 2.20.1-2
- Readd the scrolling patch, with an extra fix for redraw problems

* Mon Oct 15 2007 Matthias Clasen <mclasen@redhat.com> 2.20.1-1
- Update to 2.20.1 (translation updates)

* Tue Oct  9 2007 Matthias Clasen <mclasen@redhat.com> 2.20.0-2
- Take out the scrolling patch, since it causes redraw problems (#289281)

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> 2.20.0-1
- Update to 2.20.0

* Sat Aug 25 2007 Ray Strode <rstrode@redhat.com> - 2.19.2-2
- Apply patch from Federico Mena Quintero to avoid
  tearing during scrolls and such
  (See http://mail.gnome.org/archives/desktop-devel-list/2007-August/msg00159.html)

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-2
- Update the license field

* Wed Jul 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.0-1
- Update to 2.19.0

* Thu Dec  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-5
- Small spec file cleanups

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.0-4.1
- rebuild

* Fri Jun  9 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-4
- Add missing BuildRequires

* Mon Jun  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-3
- Rebuild

* Tue May 23 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-2
- Fix multilib conflicts
- Don't ship .la files
- Some spec file cleanups

* Mon Mar 13 2006 Matthias Clasen  <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.0-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.0-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.0-1
- Update to 2.13.0

* Tue Dec 13 2005 Jeremy Katz <katzj@redhat.com> - 2.12.0-1.2
- rebuild with -O1 to workaround (#175669)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- update to 2.12.0

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 2.11.1-3
- rebuild for new cairo

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- Rebuilt

* Tue Jun 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to 2.11.1

* Mon Mar 14 2005 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1
- update to 2.10.0

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.2-1
- update to 2.9.2

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.1-1
- update to 2.9.1

* Wed Sep 22 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- update to 2.8.0

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.92-1
- update to 2.7.92

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> 2.7.1-1
- update to 2.7.1
- drop the gtk-doc patch

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 20 2004 Matthias Clasen <mclasen@redhat.com> 2.6.1.1-1
- update to 2.6.1.1

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Thu Mar 11 2004 Alex Larsson <alexl@redhat.com> 2.5.91-2
- enable gtk-doc

* Wed Mar 10 2004 Alexander Larsson <alexl@redhat.com> 2.5.91-1
- update to 2.5.91

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.5.90-1
- 2.5.90

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 20 2004 Alexander Larsson <alexl@redhat.com> 2.5.3-1
- 2.5.3

* Wed Sep  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- 2.4.0

* Tue Aug 12 2003 Alexander Larsson <alexl@redhat.com> 2.3.6-1
- gnome 2.3 update

* Wed Aug 6 2003 Elliot Lee <sopwith@redhat.com>
- Fix libtool

* Wed Jun 5 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jun  5 2003 Jeremy Katz <katzj@redhat.com> 2.2.0.2-2
- rebuild

* Tue Apr  8 2003 Jeremy Katz <katzj@redhat.com> 2.2.0.2-1
- update to 2.2.0.2
- use system libtool

* Thu Jan 23 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.1-1
- Update to 2.2.0.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan 16 2003 Alexander Larsson <alexl@redhat.com> 2.1.90-2
- Run libtoolize to make package rebuilding possible 
  without the package already installed (#78045)

* Thu Jan  9 2003 Alexander Larsson <alexl@redhat.com>
- Update to 2.1.90

* Fri Nov  8 2002 Havoc Pennington <hp@redhat.com>
- 2.1.0

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- 2.0.2

* Fri Jul 12 2002 Havoc Pennington <hp@redhat.com>
- fix gettext package name

* Mon Jun 17 2002 Havoc Pennington <hp@redhat.com>
- remove empty AUTHORS/README

* Sat Jun 15 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1
- check file list, add glade module and gtk-doc docs

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- 1.117.0

* Thu May  2 2002 Havoc Pennington <hp@redhat.com>
- rebuild for new libglade
- 1.116.0

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- 1.114.0

* Tue Feb 19 2002 Alex Larsson <alexl@redhat.com>
- Add nasty version check stuff.

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.111.0

* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.110.0

* Fri Jan 25 2002 Havoc Pennington <hp@redhat.com>
- rebuild in rawhide

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- 1.108.0.90 cvs snap

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- cvs snap 1.105.0.90, gtk 1.3.11

* Fri Oct 26 2001 Havoc Pennington <hp@redhat.com>
- new cvs snap, rebuild for gtk 1.3.10, 
  add libglade dep, fix libart dep

* Fri Oct  5 2001 Havoc Pennington <hp@redhat.com>
- rebuild cvs snap for new glib/gtk

* Fri Sep 21 2001 Havoc Pennington <hp@redhat.com>
- new cvs snap with upstream changes

* Thu Sep 13 2001 Havoc Pennington <hp@redhat.com>
- Initial build.


