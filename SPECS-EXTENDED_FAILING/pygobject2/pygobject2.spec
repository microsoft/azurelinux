Vendor:         Microsoft Corporation
Distribution:   Mariner
# Turn off auto byte compilation for directories outside of interpreter-specific paths
%global _python_bytecompile_extra 0

### Abstract ###

Name: pygobject2
Version: 2.28.7
Release: 8%{?dist}
License: LGPLv2+
Summary: Python 2 bindings for GObject 
URL: http://www.pygtk.org/
#VCS: git:git://git.gnome.org/pygobject
Source0: http://ftp.gnome.org/pub/GNOME/sources/pygobject/2.28/pygobject-%{version}.tar.xz

### Build Dependencies ###

BuildRequires: gcc
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(python2)
BuildRequires: pkgconfig(cairo-gobject)

# Bootstrap requirements
BuildRequires: automake autoconf libtool

%description
The %{name} package provides a convenient wrapper for the GObject library
for use in Python programs.

%package codegen
Summary: The code generation program for PyGObject

%description codegen
The package contains the C code generation program for PyGObject.

%package devel
Summary: Development files for building add-on libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-codegen = %{version}-%{release}
Requires: %{name}-doc = %{version}-%{release}
Requires: glib2-devel
Requires: python2-devel
Requires: pkgconfig

%description devel
This package contains files required to build wrappers for %{name}-based
libraries such as pygtk2.

%package doc
Summary: Documentation files for %{name}

%description doc
This package contains documentation files for %{name}.

%prep
%setup -q -n pygobject-%{version}

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python2}|'

%build
PYTHON=%{__python2}
export PYTHON
%configure --disable-introspection
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name '*.la' -delete
find $RPM_BUILD_ROOT -name '*.a' -delete
rm examples/Makefile*

sed -r -i 's|#! ?/usr/bin/env python|#!%{__python2}|' %{buildroot}%{_datadir}/pygobject/2.0/codegen/*.py

# Manually invoke this byte compilation macro for paths outside of 
# interpreter-specific directories so that auto-invocation doesn't
# try to use python3
%py_byte_compile %{__python2} %{buildroot}%{_datadir}/pygobject/2.0
%py_byte_compile %{__python2} %{buildroot}%{_datadir}/pygobject/xsl

%ldconfig_scriptlets

%files
%doc AUTHORS NEWS README examples
%{_libdir}/libpyglib-2.0-python2.so*
%dir %{python2_sitearch}/gtk-2.0
%dir %{python2_sitearch}/gobject
%dir %{python2_sitearch}/glib
%{python2_sitearch}/gtk-2.0/*
%{python2_sitearch}/pygtk.*
%{python2_sitearch}/gobject/*
%{python2_sitearch}/glib/*

%files codegen
%{_bindir}/pygobject-codegen-2.0
%dir %{_datadir}/pygobject/2.0
%{_datadir}/pygobject/2.0/codegen

%files devel
%dir %{_datadir}/pygobject
%dir %{_includedir}/pygtk-2.0
%{_datadir}/pygobject/2.0/defs
%{_includedir}/pygtk-2.0/pyglib.h
%{_includedir}/pygtk-2.0/pygobject.h
%{_libdir}/pkgconfig/pygobject-2.0.pc

%files doc
%{_datadir}/gtk-doc/html/pygobject
%{_datadir}/pygobject/xsl

%changelog
* Thu Jun 17 2021 Thomas Crain <thcrain@microsoft.com> - 2.28.7-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Manually enable auto byte compilation for directories outside of interpreter-specific paths

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar  6 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.28.7-5
- Mangle shebangs to fix build

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug  9 2018 Hans de Goede <hdegoede@redhat.com> - 2.28.7-4
- Invoke /usr/bin/python2 instead of /usr/bin/python, fixes #1605545, #1606784

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Kalev Lember <klember@redhat.com> - 2.28.7-1
- Update to 2.28.7

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.6-16
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Sep 19 2013 Tomáš Mráz <tmraz@redhat.com> - 2.28.6-11
- allow old pygtk applications to work with pygobject 2.28.x and glib 2.35.x

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Colin Walters <walters@redhat.com> - 2.28.6-8
- Add various missing BuildRequires, switch to pkgconfig() syntax
- Backport upstream patch which fixes a crasher in some applications

* Fri Jul 27 2012 Ville Skyttä <ville.skytta@iki.fi> - 2.28.6-7
- Add ldconfig post(un)install scriptlets.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 David Malcolm <dmalcolm@redhat.com> - 2.28.6-5
- fix warnings on startup (patch 1; rhbz#790053)

* Mon Feb 13 2012 Matthias Clasen <mclasen@redhat.com> - 2.28.6-4
- Require python2-devel in -devel

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 John (J5) Palmieri <johnp@redhat.com> - 2.28.6-2
- disable introspection in anticipation of pygobject3
- https://bugzilla.redhat.com/show_bug.cgi?id=731851
- pygobject2 now becomes legacy for static binding support (e.g. PyGTK)

* Mon Jun 13 2011 John (J5) Palmieri <johnp@redhat.com> - 2.28.6-1
- update to upstream 2.28.6
- closure: avoid double free crash
- GVariantType is a boxed struct in newer versions of glib
- Revert back to a GVariant workaround since the fix hasn't migrated to
  Fedora's version of glib yet (workaround works in both cases)
- closure: Check the out arg is not null.
- Fix GC-related crash during PyGObject deallocation (remove patch from
  previous spec)

* Mon Jun 06 2011 Daniel Drake <dsd@laptop.org> - 2.28.4-3
- add upstream patch to solve Python GC crash during gobject deallocation

* Thu Apr 21 2011 John (J5) Palmieri <johnp@redhat.com> - 2.28.4-2
- require gobject-introspection version 0.10.8

* Thu Apr 21 2011 John (J5) Palmieri <johnp@redhat.com> - 2.28.4-1
- update to upstream 2.28.4

* Tue Mar 22 2011 John (J5) Palmieri <johnp@redhat.com> - 2.28.3-1
- update to upstream 2.28.3

* Mon Mar 21 2011 John (J5) Palmieri <johnp@redhat.com> - 2.28.2-1
- update to upstream version 2.28.2 stable
- fixes issue in bug - https://bugzilla.redhat.com/show_bug.cgi?id=682543

* Mon Mar 21 2011 John (J5) Palmieri <johnp@redhat.com> - 2.28.1-1
- update to upstream version 2.28.1 stable
- fix the spec file's sources line to point to the correct ftp directory

* Tue Mar 08 2011 John (J5) Palmieri <johnp@redhat.com> - 2.28.0-1
- update to upstream version 2.28.0 stable

* Mon Feb 28 2011 John (J5) Palmieri <johnp@redhat.com> - 2.27.91-1
- update to upstream version 2.27.91

* Fri Feb 11 2011 John (J5) Palmieri <johnp@redhat.com> - 2.27.90-2
- update files manifest to reflect files that moved around

* Fri Feb 11 2011 John (J5) Palmieri <johnp@redhat.com> - 2.27.90-1
- update to upstream version 2.27.90

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 John (J5) Palmieri <johnp@redhat.com> - 2.27.0-1
- update to upstream version 2.27.0

* Thu Sep 30 2010 John (J5) Palmieri <johnp@redhat.com> - 2.26.0-4
- Edit PyCapsule patch to only use PyCapsule in Python 3.x
  since this effects header files which require other modules to 
  be recompiled.  There is actually discussion upstream to undeprecate it
  for the 2.x series

* Tue Sep 28 2010 John (J5) Palmieri <johnp@redhat.com> - 2.26.0-3
- add patch to work with PyCapsule since PyCObject is removed from 
  Python 3.2 which we ship in rawhide

* Tue Sep 28 2010 John (J5) Palmieri <johnp@redhat.com> - 2.26.0-2
- add another py3k patch so that we compile correctly under python 3
- fixes a couple of print syntax and a try, except syntax

* Tue Sep 28 2010 John (J5) Palmieri <johnp@redhat.com> - 2.26.0-1
- Update to upstream 2.26.0
- package python3-gobject module

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.21.5-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Colin Walters <walters@verbum.org> - 2.21.5-2
- Rebuild against new gobject-introspection
- Strip noarch docs hack, seems obsolete now

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 2.21.5-1
- New upstream version

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 2.21.4-5
- Require g-i 0.9.0 

* Wed Jul  7 2010 Colin Walters <walters@verbum.org> - 2.21.4-4
- Update to latest upstream
- Drop upstreamed patches
- Require pycairo, since we have a module that uses it
- Drop libtool overriding; was not commented and seems fine
  without
- Drop --enable-thread, it's default now
- Drop --enable-pygi, it's default now
- Drop clean section, no longer needed in F-14
- Drop python-sitearch copy&paste, no longer needed in F-14
- Add SMP flags to make

* Thu May 27 2010 Colin Walters <walters@verbum.org> - 2.21.1-9
- Readd my patch to not blow up mysteriously
  Resolves: #596392

* Mon May 24 2010 Colin Walters <walters@verbum.org> - 2.21.1-7
- Reenable pygi in preparation for getting it packaged

* Wed May 05 2010 Colin Walters <walters@verbum.org> - 2.21.1-6
- Switch to disabling pygi, remove my patch for now.  See commentary
  https://bugzilla.redhat.com/show_bug.cgi?id=569885#c38

* Wed May 05 2010 Colin Walters <walters@verbum.org> - 2.21.1-5
- Another patch to clear error when we've enabled pygi
  Should really fix bug #569885

* Fri Mar 26 2010 Colin Walters <walters@verbum.org> - 2.21.1-4
- Cherrypick patch from HEAD to fix pygi imports
  Hopefully fixes bug #569885

* Sat Jan 23 2010 Thomas Spura <tomspur@fedoraproject.org> - 2.21.1-3
- add --enable-pygi (fixes bug #558003)
- replace global with define

* Fri Jan 08 2010 Matthew Barnes <mbarnes@redhat.com> - 2.21.1-2.fc13
- Provide a complete URI for the Source field.

* Sat Jan 02 2010 Matthew Barnes <mbarnes@redhat.com> - 2.21.1-1.fc13
- Update to 2.21.1

* Sun Dec 20 2009 Matthew Barnes <mbarnes@redhat.com> - 2.21.0-1.fc13
- Update to 2.21.0

* Wed Sep 23 2009 Matthew Barnes <mbarnes@redhat.com> - 2.20.0-1.fc12
- Update to 2.20.0

* Tue Aug 11 2009 Matthew Barnes <mbarnes@redhat.com> - 2.19.0-1.fc12
- Update to 2.19.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Matthew Barnes <mbarnes@redhat.com> - 2.18.0-1.fc12
- Update to 2.18.0

* Thu Apr 30 2009 Matthew Barnes <mbarnes@redhat.com> - 2.17.1-1.fc12
- Update to 2.17.0
- Remove patch for GNOME bug #566571 (fixed upstream).

* Wed Apr 22 2009 Matthew Barnes <mbarnes@redhat.com> - 2.16.1-4.fc11
- Add patch for GNOME bug #566571 (classic vs new-style inheritance crash).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.16.1-2
- Make -doc noarch

* Sun Feb 22 2009 - Matthew Barnes <mbarnes@redhat.com> - 2.16.1-1.fc11
- Update to 2.16.1

* Sun Jan 04 2009 - Matthew Barnes <mbarnes@redhat.com> - 2.16.0-1.fc11
- Update to 2.16.0
- Remove patch for RH bug #457502 (fixed upstream).
- Remove patch for GNOME bug #551059 and #551212 (fixed upstream).

* Sat Nov 29 2008 - Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.15.4-4
- Rebuild for Python 2.6

* Tue Oct 21 2008 - Bastien Nocera <bnocera@redhat.com> - 2.15.4-3.fc10
- Add patch to fix typos breaking compilation

* Tue Oct 21 2008 - Bastien Nocera <bnocera@redhat.com> - 2.15.4-2.fc10
- Add 2-liner fixing the load_contents functions not working appropriately

* Wed Sep 03 2008 Matthew Barnes <mbarnes@redhat.com> - 2.15.4-1.fc10
- Update to 2.15.4

* Sun Aug 31 2008 Matthew Barnes <mbarnes@redhat.com> - 2.15.3-1.fc10
- Update to 2.15.3

* Tue Aug 12 2008 Matthew Barnes <mbarnes@redhat.com> - 2.15.2-3.fc10
- Modify thread initialization patch to fix RH bug #458522.

* Thu Aug 07 2008 Matthew Barnes <mbarnes@redhat.com> - 2.15.2-2.fc10
- Add patch for RH bug #457502 (error on gtk.gdk.threads_init).

* Sat Jul 26 2008 Matthew Barnes <mbarnes@redhat.com> - 2.15.2-1.fc10
- Update to 2.15.2

* Sun Jul 20 2008 Matthew Barnes <mbarnes@redhat.com> - 2.15.1-2.fc10
- Fix directory ownership.  (RH bug #455974, patch by Robert Scheck).

* Wed Jul 16 2008 Matthew Barnes <mbarnes@redhat.com> - 2.15.1-1.fc10
- Update to 2.15.1
- Bump glib2_version to 2.16.0.
- Remove ancient automake_version.
- Add a pygobject2-codegen subpackage.

* Fri May 23 2008 Matthew Barnes <mbarnes@redhat.com> - 2.14.2-1.fc10
- Update to 2.14.2

* Sun Feb 17 2008 Matthew Barnes <mbarnes@redhat.com> - 2.14.1-2.fc9
- Rebuild with GCC 4.3

* Thu Jan 03 2008 Matthew Barnes <mbarnes@redhat.com> - 2.14.1-1.fc9
- Update to 2.14.1

* Fri Oct 26 2007 Matthew Barnes <mbarnes@redhat.com> - 2.14.0-2.fc9
- Remove redundant requirements.
- Use name tag where appropriate.

* Sun Sep 16 2007 Matthew Barnes <mbarnes@redhat.com> - 2.14.0-1.fc8
- Update to 2.14.0

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.13.2-3
- Rebuild for selinux ppc32 issue.

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.13.2-2
- Update the license field

* Sat Jul 07 2007 Matthew Barnes <mbarnes@redhat.com> - 2.13.2-1.fc8
- Update to 2.13.2

* Fri May 18 2007 Matthew Barnes <mbarnes@redhat.com> - 2.13.1-1.fc8
- Update to 2.13.1
- Remove patch for RH bug #237179 (fixed upstream).

* Thu May 03 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.3-5.fc7
- Fix devel subpackage dependency (RH bug #238793).

* Thu Apr 19 2007 Matthew Barnes <mbarnes@redhat.com> - 2.12.3-3.fc7
- Add patch for RH bug #237179 (memory leak).

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.12.3-2
- rebuild against python 2.5

* Sat Nov 18 2006 Matthew Barnes <mbarnes@redhat.com> - 2.12.3-1.fc7
- Update to 2.12.3

* Thu Oct 26 2006 Matthew Barnes <mbarnes@redhat.com> - 2.12.2-3.fc7
- Add subpackage pygobject2-doc (bug #205231).

* Tue Oct 24 2006 Matthew Barnes <mbarnes@redhat.com> - 2.12.2-2.fc7
- Use python_sitearch instead of python_sitelib.

* Sun Oct 15 2006 Matthew Barnes <mbarnes@redhat.com> - 2.12.2-1.fc7
- Update to 2.12.2

* Sun Sep 24 2006 Matthew Barnes <mbarnes@redhat.com> - 2.12.1-3.fc6
- Require glib2-devel for the -devel package.

* Fri Sep 22 2006 Matthew Barnes <mbarnes@redhat.com> - 2.12.1-2.fc6
- Define a python_sitelib macro for files under site_packages.
- Spec file cleanups.

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.12.1-1.fc6
- Update to 2.12.1
- Require pkgconfig for the -devel package

* Sun Aug 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.4-1.fc6
- Update to 2.11.4
- Use pre-built docs

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.3-1.fc6
- Update to 2.11.3

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.2-2.fc6
- BR libxslt

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.2-1.fc6
- Update to 2.11.2

* Wed Jul 19 2006 Jesse Keating <jkeating@redhat.com> - 2.11.0-2
- rebuild

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.11.0-1
- Update to 2.11.0

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.10.1-3
- rebuild
- Add missing br libtool

* Fri May 19 2006 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-2
- Cleanup

* Fri May 12 2006 John (J5) Palmieri <johnp@redhat.com> - 2.10.1-1
- Initial package
