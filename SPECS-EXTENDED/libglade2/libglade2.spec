Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary: The libglade library for loading user interfaces
Name: libglade2
Version: 2.6.4
Release: 24%{?dist}
License: LGPLv2+
Source: https://download.gnome.org/sources/libglade/2.6/libglade-%{version}.tar.bz2
URL: https://www.gnome.org

Requires: xml-common
BuildRequires: libxml2-devel 
BuildRequires: gtk2-devel 
BuildRequires: fontconfig
BuildRequires: pango-devel
BuildRequires: libtool
BuildRequires: gettext-devel

# https://bugzilla.gnome.org/show_bug.cgi?id=121025
Patch1: libglade-2.0.1-nowarning.patch
# https://bugzilla.gnome.org/show_bug.cgi?id=510736
Patch2: libglade-secondary.patch

%description
Libglade is a small library that allows a program to load its user
interface from am XML description at runtime. Libglade uses the XML
file format used by the GLADE user interface builder GLADE, so
libglade acts as an alternative to GLADE's code generation
approach. Libglade also provides a simple interface for connecting
handlers to the various signals in the interface (on platforms where
the gmodule library works correctly, it is possible to connect all the
handlers with a single function call). Once the interface has been
instantiated, libglade gives no overhead, so other than the short
initial interface loading time, there is no performance tradeoff.

%package devel
Summary: The files needed for libglade application development
Requires: %{name} = %{version}-%{release}

%description devel
The libglade-devel package contains the libraries and include files
that you can use to develop libglade applications.

%prep
%setup -q -n libglade-%{version}

%patch 1 -p1 -b .nowarning
%patch 2 -p1 -b .secondary

%build
%configure --disable-gtk-doc --disable-static
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}/libglade/2.0
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -delete


%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS NEWS README
%{_libdir}/lib*.so.*
%dir %{_libdir}/libglade
%dir %{_libdir}/libglade/2.0
%{_datadir}/xml/libglade

%files devel
%doc test-libglade.c
# Python2 script, anything that needed/wanted to convert to Glade2 would have done so long ago
%exclude %{_bindir}/libglade-convert
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/gtk-doc/html/libglade

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.4-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 29 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.6.4-22
- Don't ship Py2 libglade-convert, anything wanting to convert to Glade2 should have long done so

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.6.4-6
- Rebuild against new libpng

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.6.4-4
- Merge-review cleanup (#226010)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 14 2009 Matthias Clasen <mclasen@redhat.com> 2.6.4-2
- Require xml-common

* Tue Mar 17 2009 Matthias Clasen <mclasen@redhat.com> 2.6.4-1
- Update to 2.6.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Matthias Clasen <mclasen@redhat.com> 2.6.3-3
- Treat help buttons in dialogs properly

* Sun Nov 09 2008 Debarshi Ray <rishi@fedoraproject.org> 2.6.3-2
- Create and own %%{_libdir}/libglade and %%{_libdir}/libglade/2.0.

* Fri Aug 22 2008 Matthias Clasen  <mclasen@redhat.com>  2.6.3-1
- Update to 2.6.3
- Drop upstreamed patch

* Tue Feb 19 2008 Matthias Clasen  <mclasen@redhat.com>  2.6.2-5
- Fix a crash

* Sat Feb  9 2008 Matthias Clasen  <mclasen@redhat.com>  2.6.2-4
- Rebuild for gcc 4.3

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.6.2-3
- Rebuild for selinux ppc32 issue.

* Fri Aug  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.6.2-2
- Update the license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.6.2-1
- Update to 2.6.2

* Tue Jun 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.6.1-1
- Update to 2.6.1

* Fri Dec  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.6.0-3
- Small spec file cleanups

* Fri Jul 14 2006 Matthias Clasen <mclasen@redhat.com> - 2.6.0-2
- BuildRequire gettext

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.6.0-1
- Update to 2.6.0

* Thu Mar 23 2006 Matthias Clasen <mclasen@redhat.com> - 2.5.1-5
- Make non-ASCII invisible characters work

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.5.1-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.5.1-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- Rebuilt

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 2.5.1-2
- Rebuild with gcc4

* Fri Feb 11 2005 Matthias Clasen <mclasen@redhat.com> - 2.5.1-1
- Update to 2.5.1

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> - 2.5.0-1
- update to 2.5.0

* Mon Aug 16 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.0-5
- Remove unnecessary auto-* invokations

* Wed Jul 14 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.0-4
- Escape macros in %%changelog (#127050)

* Mon Jun 21 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.0-2
- Require a new enough gtk+ (#117436)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 20 2004 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- Upgrade to 2.4.0

* Wed Mar 10 2004 Mark McLoughlin <markmc@redhat.com> 2.3.6-1
- Update to 2.3.6

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Alexander Larsson <alexl@redhat.com> 2.3.2-1
- Update to 2.3.2

* Fri Aug 29 2003 Owen Taylor <otaylor@redhat.com> 2.0.1-5.0
- Fix a couple of warnings for unknown properties GtkToolbar (Hardy Merrill, 
  #85384) and GtkCList.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 14 2003 Tim Powers <timp@redhat.com> 2.0.1-3
- remove BuildRequires on Xft

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov  8 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1

* Tue Oct  8 2002 Havoc Pennington <hp@redhat.com>
- destroy .la files

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Jun 15 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- check over file list, add XML DTD to it

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- don't run auto*

* Fri May 17 2002 Havoc Pennington <hp@redhat.com>
- 1.99.12
- remove gtk-doc hack, --disable-gtk-doc now works

* Thu May  2 2002 Havoc Pennington <hp@redhat.com>
- 1.99.11

* Thu Apr  4 2002 Jeremy Katz <katzj@redhat.com>
- 1.99.10

* Tue Mar 19 2002 Alex Larsson <alexl@redhat.com>
- Update autoconf dependency to 2.53

* Mon Mar 11 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.99.9

* Mon Feb 25 2002 Alex Larsson <alexl@redhat.com>
- Bump for rebuild

* Thu Feb 21 2002 Alex Larsson <alexl@redhat.com>
- Bump for rebuild

* Tue Feb 19 2002 Alex Larsson <alexl@redhat.com>
- Add horrible buildroot check hacks. Require new Gtk+.

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- rebuild for new gtk

* Wed Jan 30 2002 Owen Taylor <otaylor@redhat.com>
- Rebuild against new GTK+

* Tue Jan 22 2002 Havoc Pennington <hp@redhat.com>
- put "nogtkdoc" patch back, it avoids X display requirement
- automake14

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- 1.99.5.90 snap
- comment out "nogtkdoc" patch, don't run autoconf

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- new 1.99.4.91 snap with Jacob's fixes, he 
  assures me we are 1.99.4.90 ABI-compatible

* Mon Nov 26 2001 Havoc Pennington <hp@redhat.com>
- new 1.99.4.90 snap, gtk 1.3.11

* Fri Oct 26 2001 Havoc Pennington <hp@redhat.com>
- new snap, rebuild on gtk 1.3.10

* Sat Oct  6 2001 Havoc Pennington <hp@redhat.com>
- new snap, add hack to avoid trying to build docs
- add the ltmain.sh hack to avoid relinking

* Mon Sep 24 2001 Havoc Pennington <hp@redhat.com>
- new snap

* Fri Sep 21 2001 Havoc Pennington <hp@redhat.com>
- convert libglade rpm to libglade2 rpm, initial build of libglade2

* Mon Aug 20 2001 Jonathan Blandford <jrb@redhat.com>
- Escape strings, #51966

* Sun Jul 22 2001 Havoc Pennington <hp@redhat.com>
- add build requires, bug #49508

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Apr 17 2001 Jonathan Blandford <jrb@redhat.com>
- New Version.

* Thu Mar 01 2001 Owen Taylor <otaylor@redhat.com>
- Rebuild for GTK+-1.2.9 include paths

* Thu Feb 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add libtoolize to make porting to new archs easy

* Fri Dec 29 2000 Matt Wilson <msw@redhat.com>
- 0.14
- added patch for gtk-doc scanner linkage

* Fri Aug 11 2000 Jonathan Blandford <jrb@redhat.com>
- Up Epoch and release

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Owen Taylor <otaylor@redhat.com>
- specfile fixes

* Wed May 31 2000 Owen Taylor <otaylor@redhat.com>
- Upgraded to libglade-0.13
- Use %%makeinstall, since that is required when %%configure is used.

* Fri May 19 2000 Owen Taylor <otaylor@redhat.com>
- Upgraded to libglade-0.12

* Tue Sep 07 1999 Elliot Lee <sopwith@redhat.com>
- Updated RHL 6.1 package to libglade-0.5

* Sun Nov  1 1998 James Henstridge <james@daa.com.au>

- Updated the dependencies of the devel package, so users must have gtk+-devel.

* Sun Oct 25 1998 James Henstridge <james@daa.com.au>

- Initial release 0.0.1
