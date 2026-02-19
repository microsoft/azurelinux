%define	glib2_version	2.13.6
%define	gtk2_version	2.12.0

%define po_package gtksourceview-2.0

Summary:	A library for viewing source files
Name:		gtksourceview2
Version:	2.11.2
Release:	46%{?dist}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Overall		LGPL-2.0-or-later
# data/language-specs/php.lang		GPL-2.0-or-later
# data/language-specs/ruby.lang		GPL-2.0-or-later
# SPDX confirmed
License:	LGPL-2.0-or-later AND GPL-2.0-or-later

URL:		https://gtksourceview.sourceforge.net/
#VCS: git:git://git.gnome.org/gtksourceview
Source0:	https://download.gnome.org/sources/gtksourceview/2.11/gtksourceview-%{version}.tar.bz2
# https://bugzilla.redhat.com/show_bug.cgi?id=661068
Patch0:	gtksourceview-2.11.2-cflags.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=672823
Patch1:	gtksourceview-2.11-fix-GCONST-def.patch
Patch2:	gtksourceview-2.11-add-libs.patch
Patch3:	gtksourceview-2.11-glib-unicode-constant.patch
Patch4:	gtksourceview-2.11-c99.patch
# https://gitlab.gnome.org/GNOME/gtksourceview/-/commit/b25e71c57fc934a7ce36e51826af9fa7c2cf9a80
Patch5:	gtksourceview-b25e71c-c99-type-cast.patch
# test_get_language needs /language-specs/ source, currently it is searched only
# from installed path, set search path from source directory
Patch6:	gtksourceview-2.11.2-test-get-languate-set-search-path.patch

BuildRequires:	GConf2-devel
BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gtk+-2.0) >= %{gtk2_version}
BuildRequires:	intltool >= 0.35
BuildRequires:	gettext
BuildRequires:	gobject-introspection-devel
BuildRequires:	make
# %%check
BuildRequires:	xorg-x11-server-Xvfb

%description
GtkSourceView is a text widget that extends the standard GTK+
GtkTextView widget. It improves GtkTextView by implementing
syntax highlighting and other features typical of a source code editor.

This package contains version 2 of GtkSourceView. The older version
1 is contains in the gtksourceview package.

%package devel
Summary: Files to compile applications that use gtksourceview2
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
gtksourceview2-devel contains the files required to compile
applications which use GtkSourceView 2.x.

%prep
%setup -q -n gtksourceview-%{version}
%patch -P0 -p1 -b .cflags
%patch -P1 -p1 -b .gconst
#%%patch2 -p1 -b .addlibs
%patch -P3 -p1 -b .glib-deprecated
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1 -b .search_path

# Explictly use gtk+-2.0
sed -i.gtk configure -e '\@gtk+-3.0@s|2.90|9999|'

%build
# Add pkgconfig search path to find out generated pc file
export PKG_CONFIG_PATH=%{_datadir}/pkgconfig:%{_libdir}/pkgconfig:$(pwd)
%configure \
	--disable-gtk-doc \
	--disable-static \
	--disable-deprecations \
	--disable-silent-rules \
	%{nil}

%make_build

%install
%make_install

# remove unwanted files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-2.0/language-specs/check.sh
rm -f $RPM_BUILD_ROOT%{_datadir}/gtksourceview-2.0/language-specs/convert.py

%find_lang %{po_package}

%check
xvfb-run \
	make check \
	%{nil}

%ldconfig_scriptlets

%files -f %{po_package}.lang
%doc	README
%doc	AUTHORS
%license	COPYING
%license	COPYING.lib
%doc	NEWS
%doc	MAINTAINERS

%dir %{_datadir}/gtksourceview-2.0
%{_datadir}/gtksourceview-2.0/language-specs/
%{_datadir}/gtksourceview-2.0/styles/

%{_libdir}/libgtksourceview-2.0.so.0{,.*}
%{_libdir}/girepository-1.0/GtkSource-2.0.typelib

%files devel
%{_includedir}/gtksourceview-2.0
%{_datadir}/gtk-doc/html/*
%{_libdir}/pkgconfig/gtksourceview-2.0.pc
%{_libdir}/libgtksourceview-2.0.so
%{_datadir}/gir-1.0/GtkSource-2.0.gir

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 2.11.2-46
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.11.2-42
- SPDX migration
- Execute testsuite, fix testcase so that spec file needed for testcase
  can be searched inside source directory

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.11.2-40
- Backport upstream patch for type casting (for -Werror=incompatible-pointer-types)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Apr 12 2023 Arjun Shankar <arjun@redhat.com> - 2.11.2-38
- Port to C99

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.11.2-30
- Fix FTBFS
  - Remove linker flags from previous patch, actually not needed
  - Add pkgconfig search patch to find out generated pc

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.11.2-26
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.11.2-18
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar  2 2012 Daniel Drake <dsd@laptop.org> - 2.11.2-13
- Fix build against new glib (avoid G_UNICODE_COMBINING_MARK) (#716176)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec  6 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 2.11.2-11
- Add patches and fix FTBFS. Bugs 672823 716176

* Tue Dec  6 2011 Adam Jackson <ajax@redhat.com> - 2.11.2-10
- Rebuild for new libpng

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.11.2-9
- Rebuild for new libpng

* Wed Jul 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.11.2-8
- Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Dan Horák <dan[at]danny.cz> - 2.11.2-6
- fix FTBFS #661068

* Wed Sep 29 2010 jkeating - 2.11.2-5
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.2-3
- Rebuild with newer gobject-introspection

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.11.2-2
- Rebuild with new gobject-introspection
- Drop gir-repository-devel

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.2-1
- Update to 2.11.2

* Wed Jun  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to 2.11.1

* Thu May 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.10.2-1
- Update to 2.10.2

* Tue Apr 27 2010 Matthias Clasen <mclasen@redhat.com> - 2.10.1-1
- Update to 2.10.1

* Sun Mar 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.10.0-1
- Update to 2.10.0

* Sun Mar 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.9-1
- Update to 2.9.9

* Tue Mar  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.8-1
- Update to 2.9.8

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.7-1
- Update to 2.9.7

* Tue Jan 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.5-1
- Update to 2.9.5

* Sat Jan 16 2010 Matthias Clasen <mclasen@redhat.com> - 2.9.4-1
- Update to 2.9.4

* Tue Dec 01 2009 Bastien Nocera <bnocera@redhat.com> 2.9.3-1
- Update to 2.9.3

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Mon Sep 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.5-1
- Update to 2.7.5

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.3-1
- Update to 2.7.3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.1-2
- Minor directory ownership cleanup

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Sun Apr 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.6.1-1
- Update to 2.6.1
- See http://download.gnome.org/sources/gtksourceview/2.6/gtksourceview-2.6.1.news

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 2.6.0-1
- Update to 2.6.0

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.6-1
- Update to 2.5.6

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.5-1
- Update to 2.5.5

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.4-1
- Update to 2.5.4

* Fri Jan 30 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.3-2
- Recognize %%else in spec files (#480587)

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.3-1
- Update to 2.5.3

* Tue Jan  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.5.2-1
- Update to 2.5.2

* Wed Nov 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.4.1-1
- Update to 2.4.1

* Sun Sep 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.3.3-1
- Update to 2.3.3

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.3.2-1
- Update to 2.3.2

* Wed Aug 13 2008 Matthias Clasen <mclasen@redhat.com> - 2.3.1-1
- Update to 2.3.1

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.1.3-1
- Update to 2.1.3

* Wed Feb  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.1.2-1
- Update to 2.1.2

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Mon Nov 26 2007 Matthias Clasen <mclasen@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Mon Nov 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.0.0-1
- Update to 2.0.0

* Tue Sep 11 2007 Matthew Barnes <mbarnes@redhat.com> - 1.90.5-1
- Update to 1.90.5

* Tue Sep  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.4-1
- Update to 1.90.4

* Tue Aug  7 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.3-2
- Update license field

* Wed Aug  1 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.3-1
- Update to 1.90.3

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.2-1
- Update to 1.90.2

* Mon Jul  2 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.1-4
- More package review feedback:
  + don't ship check.sh and convert.py scripts
  + use GRegex from glib

* Fri Jun 29 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.1-3
- Package review feedback

* Wed Jun 27 2007 Matthias Clasen <mclasen@redhat.com> - 1.90.1-2
- New package for GtkSourceView 2.x, based on gtksourceview
