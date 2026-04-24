# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libgtop2
Version:        2.41.3
Release: 5%{?dist}
Summary:        LibGTop library (version 2)

License:        GPL-2.0-or-later
URL:            https://download.gnome.org/sources/libgtop
Source0:        https://download.gnome.org/sources/libgtop/2.41/libgtop-%{version}.tar.xz

BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  gettext
BuildRequires:  make

%description
LibGTop is a library for portably obtaining information about processes,
such as their PID, memory usage, etc.

%package        devel
Summary:        Libraries and include files for developing with libgtop
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package provides the necessary development libraries and include
files to allow you to develop with LibGTop.

%prep
%autosetup -p1 -n libgtop-%{version}

%build
%configure --disable-gtk-doc --disable-static
%make_build

%install
%make_install
find %{buildroot} -name '*.la' -print -delete


%find_lang libgtop

%ldconfig_scriptlets

%files -f libgtop.lang
%doc AUTHORS NEWS README
%license COPYING
%{_libexecdir}/libgtop_daemon2
%{_libexecdir}/libgtop_server2
%{_libdir}/libgtop-2.0.so.11*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GTop-2.0.typelib

%files devel
%{_libdir}/libgtop-2.0.so
%{_includedir}/libgtop-2.0
%{_libdir}/pkgconfig/libgtop-2.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GTop-2.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/libgtop
# not worth fooling with
%exclude %{_datadir}/info

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 19 2024 David King <amigadave@amigadave.com> - 2.41.3-1
- Update to 2.41.3

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 21 2023 Kalev Lember <klember@redhat.com> - 2.41.2-1
- Update to 2.41.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.41.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 08 2023 David King <amigadave@amigadave.com> - 2.41.1-1
- Update to 2.41.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 2.40.0-1
- Update to 2.40.0

* Mon Feb 18 2019 Kalev Lember <klember@redhat.com> - 2.39.91-1
- Update to 2.39.91

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 2.39.90-1
- Update to 2.39.90

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.38.0-2
- Switch to %%ldconfig_scriptlets

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 2.38.0-1
- Update to 2.38.0

* Thu Sep 07 2017 Kalev Lember <klember@redhat.com> - 2.37.92-1
- Update to 2.37.92

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 2.37.90-1
- Update to 2.37.90

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.37.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.37.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Kalev Lember <klember@redhat.com> - 2.37.2-2
- Tighten .so globs to avoid inadvertent soname bumps

* Mon Jun 12 2017 Kalev Lember <klember@redhat.com> - 2.37.2-1
- Update to 2.37.2

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 2.36.0-1
- Update to 2.36.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 2.35.92-1
- Update to 2.35.92

* Tue Feb 14 2017 Richard Hughes <rhughes@redhat.com> - 2.35.90-1
- Update to 2.35.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.34.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Kalev Lember <klember@redhat.com> - 2.34.2-1
- Update to 2.34.2

* Sun Aug 21 2016 Kalev Lember <klember@redhat.com> - 2.34.1-1
- Update to 2.34.1
- Drop unneeded group tag

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Tue Mar 01 2016 Richard Hughes <rhughes@redhat.com> - 2.33.91-1
- Update to 2.33.91

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.33.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 David King <amigadave@amigadave.com> - 2.33.4-1
- Update to 2.33.4

* Mon Dec 14 2015 Kalev Lember <klember@redhat.com> - 2.33.3-1
- Update to 2.33.3

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Mon Sep 14 2015 Kalev Lember <klember@redhat.com> - 2.31.91-1
- Update to 2.31.91

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 2.31.90-1
- Update to 2.31.90
- Use make_install macro

* Mon Aug 10 2015 David King <amigadave@amigadave.com> - 2.31.4-1
- Update to 2.31.4
- Tighten dependency on subpackages

* Mon Jun 22 2015 David King <amigadave@amigadave.com> - 2.31.3-1
- Update to 2.31.3
- Use license macro for COPYING
- Use pkgconfig for BuildRequires

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.30.0-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.30.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Richard Hughes <rhughes@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 2.28.5-1
- Update to 2.28.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 12 2013 Cole Robinson <crobinso@redhat.com> - 2.28.4-4
- Fix fetching rootfs stats (bz #871629)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 30 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.4-1
- Update to 2.28.4

* Wed Aug 17 2011 Michel Salim <salimma@fedoraproject.org> - 2.28.3-2
- Enable introspection (# 693419, 720109)
- Remove -doc dependency on gtk-doc (# 604389)

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.28.3-1
- Update to 2.28.3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 01 2010 Parag Nemade <paragn AT fedoraproject.org> - 2.28.2-2
- Merge-review cleanup (#226026)

* Tue Sep 28 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Tue Mar 30 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Fri Feb 26 2010 Matthias Clasen <mclasen@redhat.com> - 2.28.0-2
- Examples don't build with pedantic linkers, so don't build them

* Mon Sep 21 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.3-1
- Update to 2.27.3
- http://download.gnome.org/sources/libgtop/2.27/libgtop-2.27.3.news

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.2-1
- Update to 2.27.2

* Mon May 18 2009 Bastien Nocera <bnocera@redhat.com> 2.27.1-1
- Update to 2.27.1

* Mon Apr 13 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.1-1
- Update to 2.26.1
- See http://download.gnome.org/sources/libgtop/2.26/libgtop-2.26.1.news

* Mon Mar  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 17 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Wed Dec 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-4
- Rebuild for pkg-config auto-provides

* Sun Nov  9 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-3
- Read /proc/cpuinfo completely (#467455)

* Tue Sep 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Fri Aug 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Tue Jul  1 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Tue May 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Mon Feb 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.21.5-2
- Autorebuild for GCC 4.3

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Nov 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Update top 2.21.1

* Sun Sep 16 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.92-1
- Update to 2.19.92

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 2.19.5-3
- Rebuild for PPC toolchain bug

* Wed Aug  8 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-2
- Update the license field

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Mon Jun  4 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.8-1
- Update to 2.14.8

* Mon Feb 12 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.7-1
- Update to 2.14.7

* Sun Jan 14 2007 Matthias Clasen <mclasen@redhat.com> - 2.14.6-1
- Update to 2.14.6

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.5-1
- Update to 2.14.5
- Require pkgconfig in the -devel package

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.14.4-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Soren Sandmann <sandmann@redhat.com> - 2.14.4-1.fc6
- Update to 2.14.4. The only change from 2.14.3 is the fix for 
  b.r.c 206616 / b.g.o 255290. 

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.3-1.fc6
- Update to 2.14.3

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.2-1.fc6
- Update to 2.14.2

* Thu Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 2.14.1-4
- rebuild
- add missing br libtool gettext

* Tue Jun  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-3
- Rebuild

* Mon Apr 10 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.3-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 27 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.3

* Tue Jan 03 2006 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.2

* Thu Dec 15 2005 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.1

* Wed Dec 14 2005 Matthias Clasen <mclasen@redhat.com>
- Update to 2.13.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  1 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.2-1
- Update to 2.12.2
- Drop static libraries

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> - 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- New upstream version

* Thu Aug  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.90-1
- New upstream version

* Tue Jul 12 2005 Matthias Clasen <mclasen@redhat.com> - 2.11.1-1
- Update to newer upstream version

* Fri Apr 29 2005 David Zeuthen <davidz@redhat.com> - 2.10.1-1
- New upstream version (#155188)

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> - 2.10.0-2
- Rebuilt

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> - 2.10.0-1
- Even newer upstream version

* Fri Mar 18 2005 David Zeuthen <davidz@redhat.com> - 2.9.92-1
- New upstream version

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.9.91-2
- Rebuild

* Wed Feb  9 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.91-1
- Update to 2.9.91

* Thu Jan 27 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.90-1
- Update to 2.9.90

* Wed Sep 22 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- update to 2.8.0

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.92-1
- update to 2.7.92

* Thu Aug  5 2004 Mark McLoughlin <markmc@redhat.com> 2.7.90-1
- Update to 2.7.90

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 13 2004 Warren Togami <wtogami@redhat.com> 2.5.2-2
- BR libtool texinfo gettext

* Fri Mar 12 2004 Alex Larsson <alexl@redhat.com> 2.5.2-1
- update to 2.5.2

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com> 2.5.1-1
- update to 2.5.1

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Alexander Larsson <alexl@redhat.com> 2.5.0-1
- update to 2.5.0

* Wed Jul 23 2003 Havoc Pennington <hp@redhat.com>
- automated rebuild

* Fri Jul 18 2003 Havoc Pennington <hp@redhat.com> 2.0.2-1
- 2.0.2
- forward port prog_as patch
- attempted fix to handle >4mb on IA32, #98676

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 2.0.0-10
- fix URL (#79390)

* Mon Feb  3 2003 Havoc Pennington <hp@redhat.com> 2.0.0-9
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 19 2002 Elliot Lee <sopwith@redhat.com> 2.0.0-7
- More missing libXau hackery (prog_as.patch so we can run auto* to pull 
in an updated libtool)
- _smp_mflags

* Wed Dec  4 2002 Havoc Pennington <hp@redhat.com>
- rebuild more, woot!

* Mon Dec  2 2002 Havoc Pennington <hp@redhat.com>
- rebuild to try and fix weird undefined Xau symbols

* Fri Nov  8 2002 Havoc Pennington <hp@redhat.com>
- rebuild
- remove nonexistent doc files
- fix uninstalled but unpackaged files

* Tue Jun 25 2002 Owen Taylor <otaylor@redhat.com>
- Fix missing po files

* Sat Jun 15 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- check file list, lose libgnomesupport

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu Apr 18 2002 Havoc Pennington <hp@redhat.com>
- .la files evil

* Thu Apr 18 2002 Havoc Pennington <hp@redhat.com>
- rebuild for glib 2.0

* Thu Feb 14 2002 Havoc Pennington <hp@redhat.com>
- 1.90.2

* Mon Jan 28 2002 Havoc Pennington <hp@redhat.com>
- Initial build

