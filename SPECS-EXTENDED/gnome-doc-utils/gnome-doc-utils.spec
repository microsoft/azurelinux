Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: gnome-doc-utils
Version: 0.20.10
Release: 22%{?dist}
Summary: Documentation utilities for GNOME

License: GPLv2+ and LGPLv2+ and GFDL
URL:     https://wiki.gnome.org/Projects/GnomeDocUtils
Source:  https://download.gnome.org/sources/%{name}/0.20/%{name}-%{version}.tar.xz
#VCS: git:git://git.gnome.org/gnome-doc-utils
# RH bug #438638 / GNOME bug #524207
Patch1:  gnome-doc-utils-0.14.0-package.patch
Patch2:  gnome-doc-utils-0.20.10-python3.patch

BuildArch: noarch

BuildRequires: gcc
BuildRequires: libxml2-devel >= 2.6.12
BuildRequires: libxslt-devel >= 1.1.8
BuildRequires: python3-libxml2
BuildRequires: python3-devel
BuildRequires: intltool
BuildRequires: gettext

Requires: libxml2 >= 2.6.12
Requires: libxslt >= 1.1.8
Requires: python3-libxml2
# for /usr/share/aclocal
Requires: automake
# for /usr/share/gnome/help
#Requires: yelp
# Currently creates a chicken/egg problem; gnome-doc-utils is needed in
# the build-chain for yelp, thus making it nearly impossible to ever
# update yelp for say newer Firefox.
Requires: gnome-doc-utils-stylesheets = %{version}-%{release}


%description
gnome-doc-utils is a collection of documentation utilities for the GNOME
project. Notably, it contains utilities for building documentation and
all auxiliary files in your source tree.

# note that this is an "inverse dependency" subpackage
%package stylesheets
Summary: XSL stylesheets used by gnome-doc-utils
License: LGPLv2+
# for the validation with xsltproc to use local dtds
Requires: docbook-dtds
# for /usr/share/pkgconfig
Requires: pkgconfig
# for /usr/share/xml
Requires: xml-common

%description stylesheets
The gnome-doc-utils-stylesheets package contains XSL stylesheets which
are used by the tools in gnome-doc-utils and by yelp.

%prep
%setup -q
%patch1 -p1 -b .package
%patch2 -p1 -b .python3

%build
%configure --disable-scrollkeeper --enable-build-utils
%make_build
sed -i s/python$/python3/g xml2po/xml2po/xml2po

%install
%make_install

sed -i -e '/^Requires:/d' %{buildroot}%{_datadir}/pkgconfig/xml2po.pc

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS README NEWS
%license COPYING COPYING.GPL COPYING.LGPL
%{_bindir}/*
%{_datadir}/aclocal/gnome-doc-utils.m4
%{_datadir}/gnome/help/gnome-doc-make
%{_datadir}/gnome/help/gnome-doc-xslt
%{_datadir}/gnome-doc-utils
%{_mandir}/man1/xml2po.1*
%{python3_sitelib}/xml2po/
%{_datadir}/pkgconfig/gnome-doc-utils.pc
%{_datadir}/pkgconfig/xml2po.pc

%files stylesheets
%{_datadir}/xml/gnome
%{_datadir}/xml/mallard

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20.10-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.10-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 13 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.20.10-20
- Anchor regex.

* Tue Sep 10 2019 Gwyn Ciesla <gwync@protonmail.com> - 0.20.10-19
- Port to Python 3.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.10-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.20.10-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 David King <amigadave@amigadave.com> - 0.20.10-12
- Use license macro for COPYING*
- Update URL
- Use some more modern macros
- Update man page glob
- Remove Group tag

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Merlin Mathesius <mmathesi@redhat.com> - 0.20.10-10
- Add BuildRequires: python to fix FTBFS (BZ#1414528).

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.10-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 0.20.10-2
- Depend on docbook-dtds for local validation

* Mon Mar 26 2012 Matthew Barnes <mbarnes@redhat.com> - 0.20.10-1
- Update to 0.20.10 (needed for evolution-3.4.0)

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 0.20.9-1
- Update to 0.20.9

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 0.20.7-1
- Update to 0.20.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 0.20.6-1
- Update to 0.20.6

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 0.20.5-1
- Update to 0.20.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.20.4-1
- Update to 0.20.4

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.20.2-2
- Carry over a change from the f14 branch

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 0.20.2-1
- Update to 0.20.2

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Apr 26 2010 Matthias Clasen <mclasen@redhat.com> - 0.20.1-1
- Update to 0.20.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.20.0-1
- Update to 0.20.0

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 0.19.5-1
- Update to 0.19.5

* Mon Feb 08 2010 Matthew Barnes <mbarnes@redhat.com> - 0.19.4-1
- Update to 0.19.4

* Sat Jan 23 2010 Matthew Barnes <mbarnes@redhat.com> - 0.19.3-1
- Update to 0.19.3

* Mon Jan 11 2010 Matthew Barnes <mbarnes@redhat.com> - 0.19.2-1
- Update to 0.19.2

* Wed Jan 06 2010 Matthew Barnes <mbarnes@redhat.com> - 0.19.1-1
- Update to 0.19.1

* Sun Dec 20 2009 Matthew Barnes <mbarnes@redhat.com> - 0.18.1-1
- Update to 0.18.1

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 0.18.0-1
- Update to 0.18.0

* Mon Sep  7 2009 Matthias Clasen <mclasen@redhat.com> - 0.17.5-1
- Update to 0.17.5

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 0.17.4-1
- Update to 0.17.4

* Tue Jul 28 2009 Matthias Clasen <mclasen@redhat.com> - 0.17.3-1
- Update to 0.17.3

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Matthew Barnes <mbarnes@redhat.com> - 0.17.2-1
- Update to 0.17.2
- Require libxml2-python for building.

* Mon Jun 15 2009 Matthias Clasen <mclasen@redhat.com> - 0.17.1-1
- Update to 0.17.1

* Tue Apr 14 2009 Matthias Clasen <mclasen@redhat.com> - 0.16.1-1
- Update to 0.16.1

* Mon Mar 16 2009 Matthias Clasen <mclasen@redhat.com> - 0.16.0-1
- Update to 0.16.0

* Mon Mar 02 2009 Matthew Barnes <mbarnes@redhat.com> - 0.15.2-1
- Update to 0.15.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb  3 2009 Matthias Clasen <mclasen@redhat.com> - 0.15.1-2
- Update to 0.15.1

* Sun Jan 11 2009 Matthias Clasen <mclasen@redhat.com> - 0.14.2-1
- Update to 0.14.2

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.14.1-1
- Update to 0.14.1

* Mon Dec  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.14.0-7
- Fight pkg-config-induced dependency bloat

* Mon Dec 01 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.14.0-4
- Rebuild for Python 2.6

* Sat Nov 29 2008 Matthew Barnes <mbarnes@redhat.com> - 0.14.0-3
- Add patch for RH bug #438638 (monospace <package> elements).

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 0.14.0-2
- Tweak %%summary and %%description

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.14.0-1
- Update to 0.14.0

* Tue Sep  2 2008 Matthias Clasen <mclasen@redhat.com> - 0.13.1-1
- Update to 0.13.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 0.12.2-1
- Update to 0.12.2

* Mon Feb 18 2008 Matthew Barnes <mbarnes@redhat.com> - 0.12.1-2
- Package review corrections (RH bug #225816).

* Tue Feb 12 2008 Matthew Barnes <mbarnes@redhat.com> - 0.12.1-1
- Update to 0.12.1

* Mon Sep 17 2007 Matthias Clasen  <mclasen@redhat.com> - 0.12.0-1
- Update to 0.12.0

* Mon Sep  3 2007 Matthias Clasen  <mclasen@redhat.com> - 0.11.2-1
- Update to 0.11.2

* Thu Aug  2 2007 Matthias Clasen  <mclasen@redhat.com> - 0.11.1-2
- Update the license field

* Mon Jul 30 2007 Matthias Clasen  <mclasen@redhat.com> - 0.11.1-1
- Update to 0.11.1

* Mon Jul 23 2007 Matthias Clasen  <mclasen@redhat.com> - 0.10.3-4
- Split out stylesheets as subpackage to avoid pulling automake
  in the live CD

* Fri Jul 20 2007 Jesse Keating <jkeating@redhat.com> - 0.10.3-3
- Don't require yelp for now

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 0.10.3-2
- Fix up Requires and BuildRequires

* Mon Apr 09 2007 Matthew Barnes <mbarnes@redhat.com> - 0.10.3-1.fc7
- Update to 0.10.3

* Mon Mar 12 2007 Matthew Barnes <mbarnes@redhat.com> - 0.10.1-1.fc7
- Update to 0.10.1

* Wed Jan 31 2007 Matthias Clasen <mclasen@redhat.com> - 0.9.2-1
- Update to 0.9.2

* Sat Dec 09 2006 Matthew Barnes <mbarnes@redhat.com> - 0.8.0-3
- Add patch for GNOME bug #355521 (look for local m4 files).

* Fri Sep  8 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.0-2
- Fix some directory ownership issues  (#205677)

* Mon Sep  4 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.0-1.fc6
- Update to 0.8.0

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1.fc6
- Update to 0.7.2

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.0-3
- Add a BuildRequires for perl-XML-Parser

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.0-2
- Add a missing Requires

* Sun Mar 12 2006 Ray Strode <rstrode@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.7-1
- Update to 0.5.7

* Mon Feb 20 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.6-1
- Update to 0.5.6

* Sun Feb 12 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.5-1
- Update to 0.5.5

* Mon Jan 30 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.4-1
- Update to 0.5.4

* Fri Jan 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Tue Dec 20 2005 Matthias Clasen <mclasen@redhat.com> - 0.5.2-1
- Update to 0.5.2

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 30 2005 Matthias Clasen <mclasen@redhat.com> - 0.5.1-1
- Update to 0.5.1

* Tue Oct 25 2005 Matthias Clasen <mclasen@redhat.com> - 0.4.3-1
- Update to 0.4.3

* Thu Sep 29 2005 Matthias Clasen <mclasen@redhat.com> - 0.4.2-1
- Update to 0.4.2

* Thu Sep  8 2005 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Wed Jul 27 2005 Christopher Aillon <caillon@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Wed Jul 13 2005 Matthias Clasen <mclasen@redhat.com> - 0.3.1-1
- Newer upstream version

* Tue Apr 26 2005 Ray Strode <rstrode@redhat.com> - 0.2.0-2
- Add patch that might fix yelp links (bug 146862)

* Fri Apr 8 2005 Ray Strode <rstrode@redhat.com> - 0.2.0-1
- Update to upstream version 0.2.0

* Thu Mar 17 2005 Ray Strode <rstrode@redhat.com> - 0.1.3-1
- Update to upstream version 0.1.3

* Wed Feb  2 2005 Nalin Dahyabhai <nalin@redhat.com> - 0.1.2-2
- remove explicit libxml dependency (should have been libxml2)
- add libxml2-devel and libxslt-devel as buildprereqs

* Fri Jan 28 2005 Matthias Clasen <mclasen@redhat.com> - 0.1.2-1
- Initial build.
