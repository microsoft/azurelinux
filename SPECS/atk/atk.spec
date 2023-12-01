%define majmin %(echo %{version} | cut -d. -f1-2)
Summary:        Interfaces for accessibility support
Name:           atk
Version:        2.36.0
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.gnome.org/GNOME/atk
Source0:        https://download.gnome.org/sources/%{name}/%{majmin}/%{name}-%{version}.tar.xz
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  meson

%description
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
with tools such as screen readers, magnifiers, and alternative input
devices.

%package        devel
Summary:        Development files for the ATK accessibility toolkit
Requires:       %{name} = %{version}-%{release}

%description devel
This package includes libraries, header files, and developer documentation
needed for development of applications or toolkits which use ATK.

%prep
%autosetup -p1

%build
%meson -Ddocs=true
%meson_build

%install
%meson_install

%find_lang atk10

%files -f atk10.lang
%license COPYING
%doc README AUTHORS NEWS
%{_libdir}/libatk-1.0.so.*
%{_libdir}/girepository-1.0

%files devel
%{_libdir}/libatk-1.0.so
%{_includedir}/atk-1.0
%{_libdir}/pkgconfig/atk.pc
%{_datadir}/gtk-doc/html/atk
%{_datadir}/gir-1.0

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.36.0-3
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.36.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Apr 02 2020 Kalev Lember <klember@redhat.com> - 2.36.0-1
- Update to 2.36.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.35.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 02 2019 Kalev Lember <klember@redhat.com> - 2.35.1-1
- Update to 2.35.1

* Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 2.34.1-1
- Update to 2.34.1

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.33.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Kalev Lember <klember@redhat.com> - 2.33.3-1
- Update to 2.33.3

* Wed May 22 2019 Kalev Lember <klember@redhat.com> - 2.33.1-1
- Update to 2.33.1

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 2.31.92-1
- Update to 2.31.92

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 2.31.90-2
- Revert a commit that broke introspection (#1626575)

* Sun Feb 03 2019 Phil Wyett <philwyett@kathenas.org> - 2.31.90-1
- Update to 2.31.90

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 10 2018 Kalev Lember <klember@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 2.29.92-2
- Revert a commit that broke introspection (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 2.29.92-1
- Update to 2.29.92
- Switch to the meson build system
- Remove ldconfig scriptlets

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.27.1-2
- Switch to %%ldconfig_scriptlets

* Thu Nov 02 2017 Kalev Lember <klember@redhat.com> - 2.27.1-1
- Update to 2.27.1

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Kalev Lember <klember@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Fri Mar 17 2017 Kalev Lember <klember@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 2.22.0-1
- Update to 2.22.0
- Don't set group tags

* Sat Aug 13 2016 Kalev Lember <klember@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Mar 15 2016 Richard Hughes <rhughes@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Tue Feb 16 2016 Richard Hughes <rhughes@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 2.17.90-1
- Update to 2.17.90
- Use make_install macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 2.16.0-1
- Update to 2.16.0

* Tue Mar 03 2015 Kalev Lember <kalevlember@gmail.com> - 2.15.91-1
- Update to 2.15.91
- Use the %%license macro for the COPYING file

* Tue Jan 20 2015 Richard Hughes <rhughes@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Wed Dec 17 2014 Kalev Lember <kalevlember@gmail.com> - 2.15.3-1
- Update to 2.15.3

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 2.15.2-1
- Update to 2.15.2

* Thu Oct 30 2014 Florian Müllner <fmuellner@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.14.0-1
- Update to 2.14.0

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.90-1
- Update to 2.13.90

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.3-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 15 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.3-1
- Update to 2.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.2-1
- Update to 2.13.2

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.1-1
- Update to 2.13.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 2.12.0-2
- Tighten -devel deps

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 2.11.92-1
- Update to 2.11.92

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 2.11.90-1
- Update to 2.11.90

* Tue Feb 04 2014 Richard Hughes <rhughes@redhat.com> - 2.11.6-1
- Update to 2.11.6

* Wed Jan 15 2014 Richard Hughes <rhughes@redhat.com> - 2.11.5-1
- Update to 2.11.5

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 2.11.4-1
- Update to 2.11.4

* Mon Dec 09 2013 Richard Hughes <rhughes@redhat.com> - 2.11.3-1
- Update to 2.11.3

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 2.11.2-1
- Update to 2.11.2

* Wed Oct 30 2013 Richard Hughes <rhughes@redhat.com> - 2.11.1-1
- Update to 2.11.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 2.10.0-1
- Update to 2.10.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.4-1
- Update to 2.9.4

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.3-1
- Update to 2.9.3

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.2-1
- Update to 2.9.2

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.91-1
- Update to 2.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.90-1
- Update to 2.7.90

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.5-1
- Update to 2.7.5

* Tue Jan 15 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- Update to 2.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.3-1
- Update to 2.7.3

* Tue Sep 25 2012 Kalev Lember <kalevlember@gmail.com> - 2.6.0-1
- Update to 2.6.0

* Tue Sep 04 2012 Richard Hughes <hughsient@gmail.com> - 2.5.91-1
- Update to 2.5.91

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 2.5.4-1
- Update to 2.5.4

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 2.5.3-1
- Update to 2.5.3

* Tue Mar 27 2012 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Tue Mar 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.3.95-1
- Update to 2.3.95

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.93-1
- Update to 2.3.93

* Mon Mar  5 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.91-1
- Update to 2.3.91

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.3-1
- Update to 2.3.3

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for glibc bug#747377

* Mon Sep 26 2011 Ray <rstrode@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Mon Sep 19 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.92-1
- Update to 2.1.92

* Mon Sep  5 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.91-1
- Update to 2.1.91

* Tue Aug 16 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.5-1
- Update to 2.1.5

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Tue Jun 14 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Mon Apr  4 2011 Christopher Aillon <caillon@redhat.com> 2.0.0-1
- Update to 2.0.0

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> 1.91.92-1
- Update to 1.91.92

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.33.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 1.33.2-1
- Update to 1.33.2

* Mon Oct 04 2010 Bastien Nocera <bnocera@redhat.com> 1.32.0-2
- Update to 1.32.0

* Wed Sep 29 2010 jkeating - 1.30.0-8.gitb122c67.1
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 1.30.0-7.gitb122c67.1
- Bump gobject-introspection dep to 0.9.6

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 1.30.0-7.gitb122c67
- Update to a git snapshot

* Tue Sep 14 2010 Colin Walters <walters@verbum.org> - 1.30.0-6
- introspection: Add patch to export pkg-config file; necessary
  for dependent packages to build with introspection.

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 1.30.0-5
- Rebuild with new gobject-introspection

* Tue Jun 29 2010 Colin Walters <walters@verbum.org> - 1.30.0-4
- Support builds from snapshots

* Mon Jun 21 2010 Colin Walters <walters@verbum.org> - 1.30.0-2
- BR gtk-doc in case we run autogen
- Drop the gir-repository-devel BR, it no longer exists

* Mon Mar 29 2010 Matthias Clasen <mclasen@redhat.com> - 1.30.0-1
- Update to 1.30.0

* Tue Mar  9 2010 Matthias Clasen <mclasen@redhat.com> - 1.29.92-1
- Update to 1.29.92
- Add a VCS key
- Minor packaging cleanups

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> - 1.29.4-2
- Enable introspection

* Tue Dec 22 2009 Matthias Clasen <mclasen@redhat.com> - 1.29.4-1
- Update to 1.29.4

* Wed Dec  2 2009 Matthias Clasen <mclasen@redhat.com> - 1.29.3-2
- Drop BR

* Mon Nov 30 2009 Matthias Clasen <mclasen@redhat.com> - 1.29.3-1
- Update to 1.29.3

* Wed Oct  7 2009 Stepan Kasal <skasal@redhat.com> - 1.28.0-2
- drop gtk-doc requirement from atk-devel

* Wed Sep 23 2009 Matthias Clasen <mclasen@redhat.com> - 1.28.0-1
- Update to 2.28.0

* Mon Aug 10 2009 Matthias Clasen <mclasen@redhat.com> - 1.27.90-1
- Update to 2.27.90

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec  3 2008 Matthias Clasen <mclasen@redhat.com> - 1.25.2-1
- Update to 2.25.2

* Fri Nov 21 2008 Matthias Clasen <mclasen@redhat.com> - 1.24.0-2
- Tweak %%summary and %%description

* Mon Sep 22 2008 Matthias Clasen <mclasen@redhat.com> - 1.24.0-1
- Update to 1.24.0

* Mon Jul 21 2008 Matthias Clasen <mclasen@redhat.com> - 1.23.5-1
- Update to 1.23.5

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 1.22.0-1
- Update to 1.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.92-1
- Update to 1.21.92

* Fri Feb  8 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.5-2
- Rebuild for gcc 4.3

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 1.21.5-1
- Update to 1.21.5

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 1.20.0-1
- Update to 1.20.0

* Wed Aug 15 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.6-3
- Small fixes

* Mon Aug  6 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.6-2
- Update license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.6-1
- Update to 1.19.6

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.3-1
- Update to 1.19.3

* Sun May 20 2007 Matthias Clasen <mclasen@redhat.com> - 1.19.1-1
- Update to 1.19.1

* Tue Mar 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.18.0-1
- Update to 1.18.0

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 1.17.0-1
- Update to 1.17.0

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 1.13.2-1
- Update to 1.13.2

* Wed Jan 10 2007 Matthias Clasen <mclasen@redhat.com> - 1.13.1-1
- Update to 1.13.1

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 1.12.4-1
- Update to 1.12.4

* Fri Oct 20 2006 Matthias Clasen <mclasen@redhat.com> - 1.12.3-1
- Update to 1.12.3
- Require pkgconfig in the -devel package

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 1.12.2-1.fc6
- Update to 1.12.2

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.12.1-2
- Rebuild

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 1.12.1-1
- Update to 1.12.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.11.4-4.1
- rebuild

* Thu Jun  8 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.4-4
- Rebuild

* Thu Jun  1 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.4-3
- Rebuild

* Tue Apr  4 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.4-2
- Update to 1.11.4

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.3-1
- Update to 1.11.3

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.11.2-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.11.2-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.2-1
- Update to 1.11.2

* Mon Jan 16 2006 Matthias Clasen <mclasen@redhat.com> - 1.11.0-1
- Update to 1.11.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> - 1.10.3-1
- Update to 1.10.3

* Tue Jun 28 2005 Matthias Clasen <mclasen@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Mon Mar 14 2005 Matthias Clasen <mclasen@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 1.9.0-2
- Rebuilt

* Wed Jan 26 2005 Matthias Clasen <mclasen@redhat.com> - 1.9.0-1
- update to 1.9.0

* Tue Oct 12 2004 Matthias Clasen <mclasen@redhat.com> - 1.8.0-2
- convert tamil translations to UTF-8 (#135343)

* Wed Sep 22 2004 Matthias Clasen <mclasen@redhat.com> - 1.8.0-1
- update to 2.8.0

* Mon Aug 16 2004 Matthias Clasen <mclasen@redhat.com> - 1.7.3-2
- Remove unnecessary BuildPrereqs

* Fri Jul 30 2004 Matthias Clasen <clasen@redhat.com> 1.7.3-1
- update to 2.7.3

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 12 2004 Alex Larsson <alexl@redhat.com> 1.6.0-1
- update to 2.6.0

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Mark McLoughlin <markmc@redhat.com> 1.5.5-1
- Update to 1.5.5.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 23 2004 Jonathan Blandford <jrb@redhat.com> 1.5.2-1
- new version

* Tue Sep  9 2003 Jonathan Blandford <jrb@redhat.com> 1.4.0-1
- new version

* Tue Aug 19 2003 Jonathan Blandford <jrb@redhat.com> 1.3.5-1
- new version for 2.4

* Wed Jul  9 2003 Owen Taylor <otaylor@redhat.com> 1.2.4-3.0
- Remove specific version requirement from libtool

* Tue Jul  8 2003 Owen Taylor <otaylor@redhat.com> 1.2.4-2.0
- Bump for rebuild

* Tue Jun 10 2003 Owen Taylor <otaylor@redhat.com> 1.2.4-1
- Version 1.2.4

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec 20 2002 Owen Taylor <otaylor@redhat.com>
- Package documentation, instead of blowing it away
- Version 1.2.0

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 1.0.3-3
- remove unpackaged files from the buildroot

* Mon Oct  7 2002 Havoc Pennington <hp@redhat.com>
- require glib 2.0.6-3

* Wed Jul 31 2002 Owen Taylor <otaylor@redhat.com>
- Remove fixed-ltmain.sh
- Version 1.0.3

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 04 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue Jun  4 2002 Havoc Pennington <hp@redhat.com>
- 1.0.2

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 24 2002 Havoc Pennington <hp@redhat.com>
 - rebuild in different environment

* Wed Apr  3 2002 Alex Larsson <alexl@redhat.com>
- Update to version 1.0.1

* Fri Mar  8 2002 Owen Taylor <otaylor@redhat.com>
- Version 1.0.0

* Mon Feb 25 2002 Alex Larsson <alexl@redhat.com>
- Update to 0.13

* Thu Feb 21 2002 Alex Larsson <alexl@redhat.com>
- Bump for rebuild

* Mon Feb 18 2002 Havoc Pennington <hp@redhat.com>
- rebuild for glib 1.3.14

* Fri Feb 15 2002 Havoc Pennington <hp@redhat.com>
- add horrible buildrequires hack

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 0.12.90 cvs snap

* Tue Jan 29 2002 Owen Taylor <otaylor@redhat.com>
- Version 0.10

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan  2 2002 Havoc Pennington <hp@redhat.com>
- new snap 0.8.90

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- rebuild with glib hacked to work on 64-bit

* Sun Nov 25 2001 Havoc Pennington <hp@redhat.com>
- Version 0.7
- add explicit check for required glib2 version before we do the build,
  so we don't end up with bad RPMs on --nodeps builds

* Fri Oct 26 2001 Havoc Pennington <hp@redhat.com>
- rebuild due to hosage on ia64 build system causing link to old glib

* Thu Oct 25 2001 Owen Taylor <otaylor@redhat.com>
- Version 0.6

* Thu Sep 27 2001 Havoc Pennington <hp@redhat.com>
- 0.5
- sync with Owen's version

* Wed Sep 19 2001 Havoc Pennington <hp@redhat.com>
- 0.4
- fix requires
- --enable-static
- put static libs back in file list

* Mon Sep 10 2001 Havoc Pennington <hp@redhat.com>
- update to CVS snapshot

* Wed Sep 05 2001 Havoc Pennington <hp@redhat.com>
- require specific pango version
- fix ltmain.sh to destroy all relinking BS

* Tue Sep  4 2001 root <root@dhcpd37.meridian.redhat.com>
- Version 0.2

* Sat Jul 21 2001 Owen Taylor <otaylor@redhat.com>
- Configure with --disable-gtk-doc

* Tue Jul 10 2001 Trond Eivind Glomsrod <teg@redhat.com>
- Add post- and postun-sections running ldconfig

* Wed Jun 13 2001 Havoc Pennington <hp@redhat.com>
- 0.2

* Fri May  4 2001 Owen Taylor <otaylor@redhat.com>
- Initial version
