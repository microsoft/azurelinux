%global with_mingw 0

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libgsf
Version:        1.14.53
Release:        3%{?dist}
Summary:        GNOME Structured File library

License:        LGPL-2.1-only
URL:     https://gitlab.gnome.org/GNOME/libgsf/
Source:  https://download.gnome.org/sources/%{name}/1.14/%{name}-%{version}.tar.xz

BuildRequires: bzip2-devel
BuildRequires: chrpath
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: make
BuildRequires: pkgconfig(gdk-pixbuf-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(libxml-2.0)

Obsoletes: libgsf-gnome < 1.14.22
Obsoletes: libgsf-python < 1.14.26

%if %{with_mingw}
BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc-c++

BuildRequires: mingw64-bzip2
BuildRequires: mingw32-bzip2
BuildRequires: mingw64-glib2
BuildRequires: mingw32-glib2
BuildRequires: mingw64-libxml2
BuildRequires: mingw32-libxml2
%endif

%description
A library for reading and writing structured files (e.g. MS OLE and Zip)

%package devel
Summary: Support files necessary to compile applications with libgsf
Requires: libgsf = %{version}-%{release}, glib2-devel, libxml2-devel
Requires: pkgconfig
Obsoletes: libgsf-gnome-devel < 1.14.22

%description devel
Libraries, headers, and support files necessary to compile applications using 
libgsf.

%if %{with_mingw}
%package -n mingw32-libgsf
Summary: MinGW GNOME Structured File library
BuildArch: noarch

%description -n mingw32-libgsf
A library for reading and writing structured files (e.g. MS OLE and Zip)

%package -n mingw64-libgsf
Summary: MinGW GNOME Structured File library
BuildArch: noarch

%description -n mingw64-libgsf
A library for reading and writing structured files (e.g. MS OLE and Zip)

%{?mingw_debug_package}
%endif

%prep
%autosetup -p1

%build
%global _configure ../configure

mkdir -p build/doc && pushd build
ln -s ../../doc/html doc # some day meson... libgsf!4
%configure --disable-gtk-doc --disable-static --enable-introspection=yes \
%if 0%{?flatpak}
--with-typelib_dir=%{_libdir}/girepository-1.0 --with-gir-dir=%{_datadir}/gir-1.0
%endif

%make_build
popd

%if %{with_mingw}
%mingw_configure --disable-static
%mingw_make_build
%endif

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
pushd build
%make_install
popd

%find_lang %{name}

%if %{with_mingw}
%mingw_make_install
%mingw_debug_install_post
%mingw_find_lang %{name} --all-name
%endif

# Remove lib rpaths
chrpath --delete %{buildroot}%{_bindir}/gsf*

# Remove .la files
find %{buildroot} -name '*.la' -delete -print

%ldconfig_scriptlets

%files -f libgsf.lang
%doc AUTHORS README
%license COPYING
%{_libdir}/libgsf-1.so.*
%{_libdir}/girepository-1.0/Gsf-1.typelib
%{_bindir}/gsf-office-thumbnailer
%{_mandir}/man1/gsf-office-thumbnailer.1*
%dir %{_datadir}/thumbnailers
%{_datadir}/thumbnailers/gsf-office.thumbnailer

%files devel
%{_bindir}/gsf
%{_bindir}/gsf-vba-dump
%{_libdir}/libgsf-1.so
%{_libdir}/pkgconfig/libgsf-1.pc
%dir %{_includedir}/libgsf-1
%{_includedir}/libgsf-1/gsf
%{_datadir}/gtk-doc/html/gsf
%{_datadir}/gir-1.0/Gsf-1.gir
%{_mandir}/man1/gsf.1*
%{_mandir}/man1/gsf-vba-dump.1*

%if %{with_mingw}
%files -n mingw32-libgsf -f mingw32-libgsf.lang
%license COPYING
%{mingw32_bindir}/gsf.exe
%{mingw32_bindir}/gsf-vba-dump.exe
%{mingw32_bindir}/gsf-office-thumbnailer.exe
%{mingw32_bindir}/libgsf-1-114.dll
%{mingw32_bindir}/libgsf-win32-1-114.dll
%{mingw32_libdir}/libgsf-1.dll.a
%{mingw32_libdir}/libgsf-win32-1.dll.a
%{mingw32_libdir}/pkgconfig/libgsf-1.pc
%{mingw32_libdir}/pkgconfig/libgsf-win32-1.pc
%{mingw32_includedir}/libgsf-1/
%{mingw32_mandir}/man1/gsf.1*
%{mingw32_mandir}/man1/gsf-vba-dump.1*
%{mingw32_mandir}/man1/gsf-office-thumbnailer.1*
%{mingw32_datadir}/thumbnailers/gsf-office.thumbnailer

%files -n mingw64-libgsf -f mingw64-libgsf.lang
%license COPYING
%{mingw64_bindir}/gsf.exe
%{mingw64_bindir}/gsf-vba-dump.exe
%{mingw64_bindir}/gsf-office-thumbnailer.exe
%{mingw64_bindir}/libgsf-1-114.dll
%{mingw64_bindir}/libgsf-win32-1-114.dll
%{mingw64_libdir}/libgsf-1.dll.a
%{mingw64_libdir}/libgsf-win32-1.dll.a
%{mingw64_libdir}/pkgconfig/libgsf-1.pc
%{mingw64_libdir}/pkgconfig/libgsf-win32-1.pc
%{mingw64_includedir}/libgsf-1/
%{mingw64_mandir}/man1/gsf.1*
%{mingw64_mandir}/man1/gsf-vba-dump.1*
%{mingw64_mandir}/man1/gsf-office-thumbnailer.1*
%{mingw64_datadir}/thumbnailers/gsf-office.thumbnailer
%endif

%changelog
* Wed Nov 27 2024 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.14.53-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Wed Nov 06 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.14.53-2
- Fix find_lang order for 2280661

* Fri Oct 11 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.14.53-1
- 1.14.53

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 31 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.14.52-1
- 1.14.52

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.51-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.51-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 30 2023 David King <amigadave@amigadave.com> - 1.14.51-2
- Fix building against libxml 2.12.0
- Use pkgconfig for BuildRequires

* Thu Nov 16 2023 Dan Horák <dan[at]danny.cz> - 1.14.51-1
- New upstream release 1.14.51
- Resolves: rhbz#2214335 rhbz#2249742 rhbz#2249979

* Wed Aug 02 2023 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.14.50-4
- Add MinGW packages

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 27 2023 Florian Weimer <fweimer@redhat.com> - 1.14.50-2
- Port configure script to C99

* Thu Mar 23 2023 Caolán McNamara <caolanm@redhat.com> 1.14.50-1
- latest version

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.47-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.47-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.47-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.47-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.47-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14.47-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Mar 27 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.14.47-1
- New upstream release 1.14.47

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.43-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 7 2019 Jan Beran <jaberan@redhat.com> - 1.14.43-7
- Fixing previous commit (forgotten backlash and wrong date)

* Wed Aug 7 2019 Jan Beran <jaberan@redhat.com> - 1.14.43-6
- Add explicit path for girdir and typelib_dir when building flatpak 

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.43-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Jan Beran <jaberan@redhat.com> - 1.14.43-4
-Avoid using .gz when listing manpages

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.43-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 08 2018 Caolán McNamara <caolanm@redhat.com> 1.14.43-1
- Resolves: rhbz#1575409 bump to 1.14.43

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Caolán McNamara <caolanm@redhat.com> 1.14.41-1
- Resolves: rhbz#1213052 bump to 1.14.33

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Caolán McNamara <caolanm@redhat.com> 1.14.33-1
- Resolves: rhbz#1213052 bump to 1.14.33

* Tue Apr 07 2015 Caolán McNamara <caolanm@redhat.com> 1.14.32-1
- Resolves: rhbz#1209211 bump to 1.14.32

* Thu Mar 19 2015 Caolán McNamara <caolanm@redhat.com> 1.14.29-6
- Resolves: rhbz#1202683 thumbnails not created in absence of ImageMagick
  because gdk-pixbuf2-devel not present at build time

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.14.29-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.14.29-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 26 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.14.29-1
- Update to 1.14.29

* Tue Aug 27 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.14.28-1
- Update to 1.14.28
- Enable gobject introspection
- Cleanup and modernise spec
- Drop old dependencies

* Thu Jul 25 2013 Caolán McNamara <caolanm@redhat.com> 1.14.27-1
- latest version

* Thu Apr 04 2013 Caolán McNamara <caolanm@redhat.com> 1.14.26-4
- Resolves: rhbz#922395 crash on fwrite

* Thu Apr 04 2013 Caolán McNamara <caolanm@redhat.com> 1.14.26-3
- Resolves: rhbz#925752 support aarch64

* Fri Mar 15 2013 Caolán McNamara <caolanm@redhat.com> 1.14.26-2
- Resolves: (well, push it along a bit) rhbz#921311 selinux foo

* Mon Mar 04 2013 Caolán McNamara <caolanm@redhat.com> 1.14.26-1
- latest version
- drop integrated gnome689706.gsf_input_dup.patch
- libgsf-python is gone with "excise old bit-rotted python support"

* Fri Feb 22 2013 Caolán McNamara <caolanm@redhat.com> 1.14.25-2
- Resolves: gnome#689706 fix gsf_input_dup

* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> 1.14.25-1
- latest version

* Mon Jan 14 2013 Caolán McNamara <caolanm@redhat.com> 1.14.24-2
- Resolves: rhbz#894018 co-own /usr/share/thumbnailers

* Mon Sep 10 2012 Caolán McNamara <caolanm@redhat.com> 1.14.24-1
- Resolves: rhbz#855608 latest version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Caolán McNamara <caolanm@redhat.com> 1.14.23-1
- latest version

* Fri Mar 09 2012 Caolán McNamara <caolanm@redhat.com> 1.14.22-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 1.14.21-2
- Rebuild for new libpng

* Sun May 22 2011 Caolán McNamara <caolanm@redhat.com> 1.14.21-1
- latest version

* Sat Apr 02 2011 Caolán McNamara <caolanm@redhat.com> 1.14.20-1
- latest version
- drop integrated libgsf.gnome634435.avoidcrash.patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 09 2010 Caolán McNamara <caolanm@redhat.com> 1.14.19-3
- Resolves: rhbz#650874 / gnome#634435 crash parsing ancient .ppt

* Wed Sep 29 2010 jkeating - 1.14.19-2
- Rebuilt for gcc bug 634757

* Sun Sep 26 2010 Caolán McNamara <caolanm@redhat.com> 1.14.19-1
- latest version

* Tue Jul 27 2010 Caolán McNamara <caolanm@redhat.com> 1.14.18-5
- Resolves: rhbz#618514 pre/post only needed in gnome subpackage

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.14.18-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul 19 2010 Caolán McNamara <caolanm@redhat.com> 1.14.18-3
- Resolves: rhbz#226023 merge review comments

* Sun Jun 13 2010 Caolán McNamara <caolanm@redhat.com> 1.14.18-2
- include COPYING.LIB

* Thu Apr 08 2010 Caolán McNamara <caolanm@redhat.com> 1.14.18-1
- latest version

* Sun Feb 14 2010 Caolán McNamara <caolanm@redhat.com> 1.14.17-1
- latest version

* Fri Oct 16 2009 Caolán McNamara <caolanm@redhat.com> 1.14.16-1
- latest version
- drop integrated libgsf.gnome594359.gdk-pixbuf.patch

* Mon Sep 07 2009 Caolán McNamara <caolanm@redhat.com> 1.14.15-4
- Resolves: rhbz#521513 try gdk-pixbuf before ImageMagick convert

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 10 2009 Caolán McNamara <caolanm@redhat.com> 1.14.15-2
- clean some rpmlint warnings

* Mon Jun 22 2009 Caolán McNamara <caolanm@redhat.com> 1.14.15-1
- latest version

* Tue May 26 2009 Caolán McNamara <caolanm@redhat.com> 1.14.14-1
- latest version

* Thu May 07 2009 Caolán McNamara <caolanm@redhat.com> 1.14.13-1
- latest version

* Wed Apr 29 2009 Caolán McNamara <caolanm@redhat.com> 1.14.12-1
- latest version, drop integrated libgsf-1.14.11.gcc39015.patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Caolán McNamara <caolanm@redhat.com> 1.14.11-2
- fix g_enum_register_static use

* Wed Jan 07 2009 Caolán McNamara <caolanm@redhat.com> 1.14.11-1
- latest version

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.14.10-2
- Rebuild for Python 2.6

* Mon Oct 20 2008 Caolán McNamara <caolanm@redhat.com> 1.14.10-1
- latest version

* Tue Sep 23 2008 Matthias Clasen  <mclasen@redhat.com> - 1.14.9-2
- Drop the ImageMagick dependency again, since it causes size problems on 
  the live cd

* Wed Sep 03 2008 Caolán McNamara <caolanm@redhat.com> 1.14.9-1
- latest version with gio support

* Fri Aug 08 2008 Caolán McNamara <caolanm@redhat.com> 1.14.8-2
- Resolves: rhbz#458353 gsf-office-thumbnailer doesn't work without ImageMagick's convert.
  Move that into the gnome subpackage

* Thu Mar 06 2008 Caolán McNamara <caolanm@redhat.com> 1.14.8-1
- latest version

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.14.7-3
- Autorebuild for GCC 4.3

* Fri Dec 21 2007 Caolán McNamara <caolanm@redhat.com> 1.14.7-2
- Resolves: rhbz#426436 fix up python x86_64 import gsf

* Fri Sep 14 2007 Matthias Clasen <mclasen@redhat.com> 1.14.7-1
- Update to 1.14.7

* Wed Sep 05 2007 Caolán McNamara <caolanm@redhat.com> 1.14.6-1
- next version

* Wed Aug 29 2007 Caolán McNamara <caolanm@redhat.com> 1.14.5-3
- rebuild

* Thu Aug 02 2007 Caolán McNamara <caolanm@redhat.com> 1.14.5-2
- clarify license: LGPL v2.1 in source headers, no "later"

* Thu Jul 12 2007 Caolán McNamara <caolanm@redhat.com> 1.14.5-1
- next version

* Mon Jun 18 2007 Caolán McNamara <caolanm@redhat.com> 1.14.4-1
- next version

* Sun Mar 25 2007 Caolán McNamara <caolanm@redhat.com> 1.14.3-4
- Resolves rhbz#233862 unowned directory fix from Michael Schwendt

* Fri Feb 09 2007 Caolán McNamara <caolanm@redhat.com> 1.14.3-3
- some spec cleanups

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.14.3-2
- rebuild for python 2.5

* Thu Nov 09 2006 Caolán McNamara <caolanm@redhat.com> 1.14.3-1
- bump to 1.14.3

* Wed Nov  1 2006 Dan Williams <dcbw@redhat.com> - 1.14.2-2
- Split to remove gnome-vfs2 dependency on core sub-packages

* Mon Oct 09 2006 Caolán McNamara <caolanm@redhat.com> - 1.14.2-1
- bump to 1.14.2

* Fri Jul 14 2006 Bill Nottingham <notting@redhat.com> - 1.14.1-6
- gnome-vfs2-devel no longer requires libbonobo-devel; add it as a buildreq

* Thu Jul 13 2006 Jesse Keating <jkeating@redhat.com> - 1.14.1-5
- rebuild
- add missing br gettext

* Mon May 29 2006 Caolán McNamara <caolanm@redhat.com> 1.14.1-4
- rh#193417# Add BuildRequires perl-XML-Parser

* Tue May 23 2006 Caolán McNamara <caolanm@redhat.com> 1.14.1-3
- rh#192707# disable rebuilding of gtk-doc so as to allow multi-arch devel

* Wed May 10 2006 Matthias Clasen <mclasen@redhat.com> 1.14.1-2
- Update to 1.14.1

* Mon Mar 20 2006 Caolán McNamara <caolanm@redhat.com> 1.14.0-1
- next version

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.13.3-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.13.3-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Dec  5 2005 Caolán McNamara <caolanm@redhat.com> 1.13.3-2
- rh#172062# Obsolete extras libgsf113

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> 1.13.3-1
- Update to 1.13.3

* Tue Sep 20 2005 Caolán McNamara <caolanm@redhat.com> 1.12.3-1
- bump to next version
- add manpage for gsf-office-thumbnailer

* Fri Aug 26 2005 Caolán McNamara <caolanm@redhat.com> 1.12.2-1
- bump to latest version

* Wed Jun 15 2005 Caolán McNamara <caolanm@redhat.com> 1.12.1-1
- bump to latest version

* Wed Mar  2 2005 Caolán McNamara <caolanm@redhat.com> 1.12.0-1
- bump to latest version
- clean spec

* Wed Mar  2 2005 Caolán McNamara <caolanm@redhat.com> 1.11.1-2
- rebuild with gcc4

* Thu Dec 16 2004 Caolán McNamara <caolanm@redhat.com> 1.11.1-1
- upgrade to 1.11.1

* Tue Aug 31 2004 Caolán McNamara <caolanm@redhat.com> 1.10.1-1
- upgrade to 1.10.1

* Wed Aug 18 2004 Caolán McNamara <caolanm@redhat.com> 1.10.0-1
- upgrade to 1.10.0

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May  6 2004 Dams <anvil[AT]livna.org> 1.9.0-2
- -devel now requires libgsf=version-release
- Added smp_mflags
- Fixed double included .so files

* Wed May 5 2004 Caolán McNamara <caolanm@redhat.com> 1.9.0-1
* upgrade to 1.9.0 to get crash fixes

* Sun Apr 11 2004 Warren Togami <wtogami@redhat.com> 1.8.2-3
- BR libtool libxml2-devel gnome-vfs2-devel bzip2-devel
- -devel req glib2-devel libxml2-devel gnome-vfs2-devel

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 12 2004 Jonathan Blandford <jrb@redhat.com> 1.8.2-1
- make $includedir/libgsf-1 owned by -devel

* Fri Sep 19 2003 Havoc Pennington <hp@redhat.com> 1.8.2-1
- 1.8.2

* Wed Aug 13 2003 Jonathan Blandford <jrb@redhat.com>
- rebuild

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com> 1.8.1-5
- Fix libtool

* Sat Jul 12 2003 Jeremy Katz <katzj@redhat.com> 1.8.1-4
- use system libtool so that lib64 library deps are correct

* Thu Jul 10 2003 Jeremy Katz <katzj@redhat.com> 1.8.1-3
- forcibly disable gtk-doc (openjade is broken on s390)

* Mon Jul  7 2003 Jeremy Katz <katzj@redhat.com> 1.8.1-2
- ldconfig in %%post/%%postun

* Sun Jul  6 2003 Jeremy Katz <katzj@redhat.com> 1.8.1-1
- use standard macros
- build for Red Hat Linux

* Tue May 13 2003 Rui M. Seabra <rms@407.org>
- fix spec to reflect current stat of the build

* Tue Jun 18 2002 Rui M. Seabra <rms@407.org>
- set permission correctly
- fix common mistake of Copyright flag into License flag.

* Thu May 23 2002 Jody Goldberg <jody@gnome.org>
- Initial version
