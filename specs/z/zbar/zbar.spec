# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%ifarch %{java_arches}
%global JAVA 1
%else
%global JAVA 0
%endif

Name:		zbar
Version:	0.23.93
Release:	9%{?dist}
Summary:	Bar code reader

License:	LGPL-2.1-or-later
URL:		http://zbar.sourceforge.net/
Source0:	https://linuxtv.org/downloads/%{name}/%{name}-%{version}.tar.bz2
Patch0:		use_python3_on_python_script.patch
Patch1:		fix_qt_overlinking.patch

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gettext-devel
BuildRequires:	GraphicsMagick-devel
BuildRequires:	gtk3-devel
BuildRequires:	libSM-devel
BuildRequires:	libtool
BuildRequires:	libv4l-devel
BuildRequires:	libXv-devel
BuildRequires:	make
BuildRequires:	python3-gobject-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qtx11extras-devel
BuildRequires:	xmlto
%if %{JAVA}
BuildRequires:	java-devel
%endif
BuildRequires:	python3-devel
BuildRequires:  python3-setuptools

%description
ZBar Bar Code Reader is an open source software suite for reading bar
codes from various sources, such as video streams, image files and raw
intensity sensors. It supports EAN-13/UPC-A, UPC-E, EAN-8, Code 128,
Code 93, Code 39, Codabar, Interleaved 2 of 5, QR Code and SQ Code.

%package devel
Summary: Bar code reader library extra development files
Requires: %{name}-libs%{_isa} = %{version}-%{release}

%description devel
This package contains header files and additional libraries used for
developing applications that read bar codes with this library.

%package libs
Summary: Bar code reader library

%description libs
This package contains the ZBar Bar Code Reader library.

%package gtk
Summary: Bar code reader GTK widget
Requires: %{name}-libs%{_isa} = %{version}-%{release}
# Obsoleted in F37
Obsoletes: %{name}-gi < %{version}-%{release}

%description gtk
This package contains a bar code scanning widget for use with GUI
applications based on GTK 3.

%package gtk-devel
Summary: Bar code reader GTK widget extra development files
Requires: %{name}-devel%{_isa} = %{version}-%{release}
Requires: %{name}-gtk%{_isa} = %{version}-%{release}

%description gtk-devel
This package contains header files and additional libraries used for
developing GUI applications based on GTK 3 that include a bar code
scanning widget.

%package qt
Summary: Bar code reader Qt widget
Requires: %{name}-libs%{_isa} = %{version}-%{release}

%description qt
This package contains a bar code scanning widget for use with GUI
applications based on Qt4.

%package qt-devel
Summary: Bar code reader Qt widget extra development files
Requires: %{name}-devel%{_isa} = %{version}-%{release}
Requires: %{name}-qt%{_isa} = %{version}-%{release}

%description qt-devel
This package contains header files and additional libraries used for
developing GUI applications based on Qt5 that include a bar code
scanning widget.

%package -n python3-zbar
Summary: Bar code reader PyGTK widget
Requires: %{name}-libs%{_isa} = %{version}-%{release}
Requires: python3-pillow
# Renamed in F37
Obsoletes: %{name}-python3 < %{version}-%{release}

%description -n python3-zbar
This package contains a bar code scanning widget for use on
python applications that work with images.

%if %{JAVA}
%package java
Summary: Bar code reader Java library
Requires: %{name}-devel%{_isa} = %{version}-%{release}
Requires: %{name}-gtk%{_isa} = %{version}-%{release}

%description java
This package contains header files and additional libraries used for
on Java Native Interface (JNI) applications using ZBar.
%endif

%prep
%setup -q
%patch 0 -p1
%patch 1 -p1

%build
autoreconf -fiv
%configure --with-python=python3 --with-gtk=auto --with-dbusconfdir=%{_sysconfdir} --docdir=%{_docdir}/%{name}-%{version} --with-graphicsmagick --without-xshm --without-xv --enable-codes=ean,databar,code128,code93,code39,codabar,i25,qrcode,sqcode,pdf417

# rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install
%if %{JAVA}
install -d %{buildroot}%{_jnidir}
mv %{buildroot}%{_datadir}/zbar/lib/zbar.jar %{buildroot}%{_jnidir}
mv %{buildroot}%{_datadir}/zbar/lib/libzbarjni.so* %{buildroot}%{_libdir}
%endif
cp test/test_python.py %{buildroot}%{_docdir}

#Remove .la and .a files
find ${RPM_BUILD_ROOT} -name '*.la' -or -name '*.a' | xargs rm -f

# Remove installed doc
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/

%ldconfig_scriptlets

%ldconfig_scriptlets devel

%ldconfig_scriptlets gtk

%ldconfig_scriptlets qt

%find_lang zbar

%files
%doc NEWS.md README.md INSTALL.md
%{_bindir}/zbarimg
%{_bindir}/zbarcam
%{_mandir}/man1/*
%{_sysconfdir}/dbus-1/system.d/org.linuxtv.Zbar.conf

%files libs -f zbar.lang
%license COPYING LICENSE.md
%{_libdir}/libzbar.so.0*

%files devel
%doc HACKING.md TODO.md
%{_libdir}/libzbar.so
%{_libdir}/pkgconfig/zbar.pc
%dir %{_includedir}/zbar
%{_includedir}/zbar.h
%{_includedir}/zbar/Exception.h
%{_includedir}/zbar/Symbol.h
%{_includedir}/zbar/Image.h
%{_includedir}/zbar/Scanner.h
%{_includedir}/zbar/Decoder.h
%{_includedir}/zbar/ImageScanner.h
%{_includedir}/zbar/Video.h
%{_includedir}/zbar/Window.h
%{_includedir}/zbar/Processor.h

%files gtk
%{_libdir}/libzbargtk.so.*
%{_bindir}/zbarcam-gtk



%files gtk-devel
%{_libdir}/libzbargtk.so
%{_libdir}/pkgconfig/zbar-gtk.pc
%{_includedir}/zbar/zbargtk.h



%files qt
%{_libdir}/libzbarqt.so.*
%{_bindir}/zbarcam-qt

%files qt-devel
%{_libdir}/libzbarqt.so
%{_libdir}/pkgconfig/zbar-qt.pc
%{_includedir}/zbar/QZBar*.h

%if %{JAVA}
%files java
%{_jnidir}/zbar.jar
%{_libdir}/libzbarjni.so*
%endif

%files -n python3-zbar
%{python3_sitearch}/zbar.so
%{_docdir}/test_python.py

%changelog
* Fri Sep 05 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 0.23.93-9
- Fix Qt overlinking

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.93-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.23.93-7
- Rebuilt for Python 3.14

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.93-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.93-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.23.93-4
- Rebuilt for Python 3.13

* Mon Apr 15 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.23.93-3
- Update python3-gobject BuildRequires

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 Gwyn Ciesla <gwync@protonmail.com> - 0.23.93-1
- 0.23.93

* Fri Jan 05 2024 Florian Weimer <fweimer@redhat.com> - 0.23.90-12
- Add missing Py_SIZE to py311.patch

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.90-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Michael J Gruber <mjg@fedoraproject.org> - 0.23.90-10
- Fix FTBFS with python 3.12 (rhbz#2220630)

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 0.23.90-9
- Rebuilt for Python 3.12

* Wed Mar 01 2023 Gwyn Ciesla <gwync@protonmail.com> - 0.23.90-8
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.90-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 21 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.23.90-6
- BR setuptools

* Fri Aug 26 2022 Kalev Lember <klember@redhat.com> - 0.23.90-5
- Misc packaging cleanup
- Sort BuildRequires and Requires and split them out one per line
- Move GObject Introspection bindings to -gtk and -gtk-devel subpackages
- Split libzbar out to zbar-libs subpackage
- Tighten subpackage deps with %%{_isa}
- Drop manual requires on pkgconfig and rely on rpm dep extractor
- Rename zbar-python3 to python3-zbar as per latest Python guidelines
- Use make_build and make_install macros

* Mon Aug 01 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.23.90-4
- Only build Java on supported platforms.

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.23.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.23.90-2
- Rebuilt for Python 3.11

* Tue May 31 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.23.90-1
- 0.23.90

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 0.23-14
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 0.23-12
- Fix 3.11 FTBFS.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.23-10
- Rebuilt for Python 3.10

* Thu Mar 25 2021 Gwyn Ciesla <gwync@protonmail.com> - 0.23-9
Fix FTBFS for autoconf 2.71.

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.23-6
- Update description.
- Patch for Python 3.9.
- Move back to GraphicsMagick.

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.23-5
- Rebuilt for Python 3.9

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.23-3
- Rebuilt for Python 3.8

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 23 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.23-1
- Bump to release 0.23.


* Tue May 14 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.22.92-1
- Third release candidate for 0.23.

* Fri May 10 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.22.90-1
- Release candidate for 0.23. Support for Gtk3 and GObject Introspection (GIR)

* Mon Apr 29 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.22.2-1
- Update to 0.22.2: added support for Java 11

* Wed Feb 20 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.22-1
- Bump to version 0.22: zbarcam-qt is now a full-featured application

* Tue Feb 12 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.21-1
- Bump to version 0.21: d-bus and SQ code support, improved zbarcam-qt

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan  7 2019 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.20.1-4
- Disable python2 bindings due to pygtk2 orphaned package

* Thu Aug  9 2018 Hans de Goede <hdegoede@redhat.com> - 0.20.1-3
- Drop zbar_fedora29_hack_for_codegen_to_work.patch now that pygobject2 is
  fixed (rhbz# 1606784)
- Use %%ldconfig_scriptlets so that we don't unnecessarily run ldconfig on F28+

* Wed Aug 08 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.20.1-2
- Re-enable python2 bindings

* Wed Aug 08 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.20.1-1
- Bump version to 0.20.1

* Tue Aug 07 2018 Mauro Carvalho Chehab <mchehab+samsung@kernel.org> - 0.20-8
- Fix python 2 dependencies

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.20-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 11 2017 Mauro Carvalho Chehab <mchehab@s-opensource.com> - 0.20-1
- Update it to version 0.20 with brings V4L2 controls to zbarcam-qt

* Sun Mar 26 2017 Mauro Carvalho Chehab <mchehab@s-opensource.com> - 0.10-29
- Make zbar-qt to use Qt5 and generate gtk and qt applications

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-27
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.10-25
- Add patch to include m4_pattern_allow([AM_PROG_AR])

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.10-23
- Add patch to use REQBUFS properly

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.10-22
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Aug 06 2013 Mauro Carvalho Chehab <m.chehab@samsung.com> - 0.10-19
- Fix Fedora 20 build problems

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.10-17
- Rebuild.

* Fri Feb 22 2013 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.10-16
- Change zbar to use GraphicsMagick instead of ImageMagick

* Fri Feb 22 2013 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.10-15
- zbar 0.10 source generated via hg archive -r 0.10 ../zbar-0.10.tar.bz2
  That allows to better handle the difference from 0.10 to -hg
- Update to the latest hg patch

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.10-13
- rebuild against new libjpeg

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 01 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.10-11
- Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.10-9
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 25 2010 Mauro Carvalho Chehab <mchehab@redhat.com> - 0.10-7
- Prefer to use non-emulated formats

* Sun Dec 05 2010 Mauro Carvalho Chehab <mchehab@redhat.com>
- Update it to the newest version available at zbar git directory
- Use libv4l to communicate with video devices

* Wed Sep 29 2010 jkeating - 0.10-5
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Hans de Goede <hdegoede@redhat.com> 0.10-4
- Rebuild for new ImageMagick

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Nov 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.10-2
- Rebuild for Qt 4.6.0 RC1 in F13 (was built against Beta 1 with unstable ABI)
- Always BR qt4-devel rather than qt-devel, it's provided by qt-devel anyway

* Mon Nov 02 2009 Bastien Nocera <bnocera@redhat.com> 0.10-1
- Update to 0.10

* Wed Jul 29 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-7
- Replace URL info

* Wed Jul 29 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.8-6
- fix epel build

* Tue Jul 28 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-5
- Now fixed Source0 url
- Removed ldconfig calls to devel subpackages
- Fixed directory ownership issue -pygtk
- Added %%{name} to URL
- Added comment to rpath
- Improved comment for removing .la and .a files

* Mon Jul 27 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-4
- Fixed sourceforge url
- Removed redundant libX11-devel package from BuildRequires
- Removed redundant ImageMagick package from Requires
- Removed Provides for not included static libs
- Removed redundant requires to subpackages -qt and -gtk
- Removed redundant {name} = %%{version}-%%{release} from -pygtk
- Replaced macros from % to %% in changelog
- Fixed ownership issue
- Added ldconfig call to devel, qt-devel and gtk-devel

* Fri Jul 24 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-3
- Fixed License from LGPLv2 to LGPLv2+
- Added to main BuildRequires libXv-devel and xmlto packages
- Removed pkgconfig from main BuildRequires
- Removed .la and .a files
- Removed version validation from ImageMagick-c++ and ImageMagick-c++-devel packages
- Replaced 3 {%%version} to %%{version} (packages: devel, qt-devel, gtk-devel)
- Removed duplicated description for each package
- Added %%{version}-%%{release} to packages: devel, gtk, gtk-devel, pygtk, qt
- Added pkgconfig to packages gtk-devel, qt-devel into Requires session
- Removed redundant packages
- Added dependency of gtk to pygtk
- Added timestamp on installed files
- Replaced %%{_datadir}/man to %%{_mandir}
- Removed INSTALL file
- Fixed %%doc session
- Added to -devel own of %%{_includedir}/zbar directory
- Replaced "%%{_libdir}/python*" to %%{python_sitearch}
- Fixed %%defattr
- Fixed Release Number and Changelog
- Fixed rpath error

* Thu Jul 16 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-2
- Added pkgconfig to devel package
- Fixed syntax to ldconfig
- Fixed warnings from rpmlint
- Fixed static path to docs

* Wed Jul 15 2009 Douglas Schilling Landgraf <dougsland@redhat.com> - 0.8-1
- First release, based on original zbar.spec provided by sources
