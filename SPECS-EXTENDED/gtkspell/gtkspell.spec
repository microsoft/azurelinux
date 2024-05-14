Vendor:         Microsoft Corporation
Distribution:   Azure Linux
### Abstract ###

Name: gtkspell
Version: 2.0.16
Release: 23%{?dist}
License: GPLv2+
Summary: On-the-fly spell checking for GtkTextView widgets
URL: https://gtkspell.sourceforge.net/
Source: https://gtkspell.sourceforge.net/download/%{name}-%{version}.tar.gz

### Build Dependencies ###

BuildRequires: gcc
BuildRequires: perl(File::Find)
BuildRequires: make
BuildRequires: enchant-devel
BuildRequires: gtk2-devel
BuildRequires: gettext
BuildRequires: intltool

%description
GtkSpell provides word-processor-style highlighting and replacement of
misspelled words in a GtkTextView widget as you type. Right-clicking a
misspelled word pops up a menu of suggested replacements.

%package devel
Summary: Development files for GtkSpell
Requires: %{name} = %{version}-%{release}
Requires: gtk2-devel
Requires: pkgconfig

%description devel
The gtkspell-devel package provides header files for developing
applications which use GtkSpell.

%prep
%setup -q

%build
%configure --disable-gtk-doc --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -name "*.la" -exec rm {} \;

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%license COPYING
%doc README AUTHORS
%{_libdir}/libgtkspell.so.0*

%files devel
%{_datadir}/gtk-doc/html/gtkspell
%{_includedir}/gtkspell-2.0
%{_libdir}/libgtkspell.so
%{_libdir}/pkgconfig/gtkspell-2.0.pc

%changelog
* Wed Feb 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.16-23
- License verified.

* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.16-22
- Adding missing BRs on Perl modules.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.16-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 18 2018 Sandro Mani <manisandro@gmail.com> - 2.0.16-16
- Add missing BR: gcc, make

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.0.16-3
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 02 2009 Matthew Barnes <mbarnes@redhat.com> - 2.0.16-1.fc13
- Update to 2.0.16
- No need to run libtoolize and autoreconf.
- Remove language comparison patch (fixed upstream).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Dec 12 2008 Matthew Barnes <mbarnes@redhat.com> - 2.0.15-1.fc11
- Update to 2.0.15
- Add patch for a language comparison bug reported by Zdeněk Jurka.

* Thu Nov 27 2008 Matthew Barnes <mbarnes@redhat.com> - 2.0.14-1.fc11
- Update to 2.0.14

* Sat Nov 22 2008 Matthew Barnes <mbarnes@redhat.com> - 2.0.13-2.fc11
- Shorten the summary.

* Mon Jun 09 2008 Matthew Barnes <mbarnes@redhat.com> - 2.0.13-1.fc9
- Update to 2.0.13
- Add BuildRequires: intltool
- Remove "libs" patch (fixed upstream).
- Remove patch for RH bug #216412 (fixed upstream).
- Remove patch for RH bug #245888 (fixed upstream).

* Sat Feb 09 2008 Matthew Barnes <mbarnes@redhat.com> - 2.0.11-8.fc9
- Rebuild with GCC 4.3

* Mon Jan 21 2008 Matthew Barnes <mbarnes@redhat.com> - 2.0.11-7.fc9
- Incorporate package review feedback from Parag AN (RH bug #225876).

* Fri Dec 28 2007 Matthew Barnes <mbarnes@redhat.com> - 2.0.11-6.fc9
- Remove aspell dependency from devel subpackage.

* Thu Dec 20 2007 Matthew Barnes <mbarnes@redhat.com> - 2.0.11-5.fc9
- Add patch for RH bug #245888 (use Enchant).

* Wed Oct 10 2007 Matthew Barnes <mbarnes@redhat.com> - 2.0.11-4.fc8
- Rebuild

* Wed Feb 14 2007 Matthew Barnes <mbarnes@redhat.com> - 2.0.11-3.fc7
- Add patch for RH bug #216142 (symbols missing "static" qualifier).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.0.11-2.1
- rebuild

* Wed May 24 2006 Matthew Barnes <mbarnes@redhat.com> - 2.0.11-2
- Remove @SPELLER_LIB@ from Libs in gtkspell-2.0.pc.in (closes #116914).
- Disable gtk-doc to resolve multilib conflict (closes #192683).
- Various spec file cleanups.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.0.11-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.0.11-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 David Malcolm <dmalcolm@redhat.com> - 2.0.11-1
- 2.0.11

* Wed Mar 16 2005 David Malcolm <dmalcolm@redhat.com> - 2.0.7-3
- rebuild with GCC 4

* Mon Aug 30 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.7-2
- rerun ldconfig upon uninstall; thanks to Matthias Saou (#131277)

* Mon Aug 23 2004 Warren Togami <wtogami@redhat.com> - 2.0.7-1
- 2.0.7 should fix more i18n stuff

* Sat Aug 21 2004 Warren Togami <wtogami@redhat.com> - 2.0.6-3
- nosnilmot informed us about broken i18n fixed in upstream CVS

* Fri Jul 30 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add ldconfig symlink into rpm

* Fri Jul  2 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.6-1
- 2.0.6; added find_lang; updated description

* Mon Jun 21 2004 David Malcolm <dmalcolm@redhat.com> - 2.0.4-6
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec 15 2003 Matt Wilson <msw@redhat.com> 2.0.4-3
- added BuildRequires: gtk-doc (#111107)
- added Requires: gtk2-devel for gtkspell-devel subpackage (#111139)

* Mon Sep 29 2003 Matt Wilson <msw@redhat.com> 2.0.4-2
- add aspell-devel to gtkspell-devel as a requirement (#105944,
  #104562)

* Tue Jul 15 2003 Matt Wilson <msw@redhat.com> 2.0.4-1
- Initial build.


