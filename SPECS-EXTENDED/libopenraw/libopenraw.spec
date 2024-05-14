Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Summary:	Decode camera RAW files
Name:		libopenraw
Version:	0.1.3
Release:	8%{?dist}
License:	LGPLv3+
URL:		https://libopenraw.freedesktop.org
Source0:	https://libopenraw.freedesktop.org/download/%{name}-%{version}.tar.bz2

BuildRequires:  boost-devel
BuildRequires:  gcc-c++
BuildRequires:  libjpeg-devel
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libxml-2.0) >= 2.5.0

%description
libopenraw is an ongoing project to provide a free software
implementation for camera RAW files decoding. One of the main reason is
that dcraw is not suited for easy integration into applications, and
there is a need for an easy to use API to build free software digital
image processing application.

%package gnome
Summary:	GUI components of %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description gnome 
The %{name}-gnome package contains gui components of %{name}.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package gnome-devel
Summary:	Development files for %{name}-gnome
Requires:	%{name}-gnome%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description    gnome-devel
The %{name}-gnome-devel package contains libraries and header files for
developing applications that use %{name}-gnome.

%package pixbuf-loader
Summary:	RAW image loader for GTK+ applications

Requires:	gtk2
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description pixbuf-loader
%{name}-pixbuf-loader contains a plugin to load RAW images, as created by
digital cameras, in GTK+ applications.

%prep
%autosetup

%build
%configure --disable-static --enable-gnome --disable-silent-rules

# Omit unused direct shared library dependencies.
sed --in-place --expression 's! -shared ! -Wl,--as-needed\0!g' libtool

%{make_build}

%check
make check

%install
%make_install
find $RPM_BUILD_ROOT -type f -name "*.la" -delete

%ldconfig_scriptlets

%ldconfig_scriptlets gnome


%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README TODO
%{_libdir}/%{name}.so.*

%files gnome
%{_libdir}/%{name}gnome.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}-0.1.pc

%dir %{_includedir}/%{name}-0.1
%{_includedir}/%{name}-0.1/%{name}/*.h

%files gnome-devel
%{_libdir}/%{name}gnome.so
%{_libdir}/pkgconfig/%{name}-gnome-0.1.pc

%dir %{_includedir}/%{name}-0.1/%{name}-gnome
%{_includedir}/%{name}-0.1/%{name}-gnome/gdkpixbuf.h

%files pixbuf-loader
%{_libdir}/gdk-pixbuf-2.0/*/loaders/*.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.3-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jul 15 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.1.3-4
- Added gcc-c++ to BuildRequires as per https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Julian Sikorski <belegdol@fedoraproject.org> - 0.1.3-2
- Removed ldconfig scriptlets as per
  https://fedoraproject.org/wiki/Changes/Removing_ldconfig_scriptlets

* Fri May  4 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.3-1
- Updated to 0.1.3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 22 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.1.2-1
- Updated to 0.1.2

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Mar 27 2017 Julian Sikorski <belegdol@fedoraproject.org> - 0.1.1-1
- Updated to 0.1.1
- Dropped gdk-pixbuf loaders scriptlet

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Jonathan Wakely <jwakely@redhat.com> - 0.1.0-3
- Rebuilt for Boost 1.63

* Tue Nov 29 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.1.0-2
- Fixed %%{?_isa} usage

* Tue Nov 29 2016 Julian Sikorski <belegdol@fedoraproject.org> - 0.1.0-1
- Updated to 0.1.0
- Dropped upstreamed patches
- Cleaned up and modernised the .spec file

* Wed Jun 29 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 0.0.9-18
- Fix crash in GdkPixbuf loader (#1279152)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 16 2016 Jonathan Wakely <jwakely@redhat.com> - 0.0.9-16
- Rebuilt for Boost 1.60

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.0.9-15
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-14
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.0.9-13
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.0.9-11
- Rebuilt for GCC 5 C++11 ABI change

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.0.9-10
- Rebuild for boost 1.57.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.0.9-7
- Rebuild for boost 1.55.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 0.0.9-5
- Rebuild for boost 1.54.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.0.9-3
- rebuild due to "jpeg8-ABI" feature drop

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.0.9-2
- rebuild against new libjpeg

* Sun Sep 30 2012 Julian Sikorski <belegdol@fedoraproject.org> - 0.0.9-1
- Updated to 0.0.9
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Switched to .bz2 sources
- Dropped included patches

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-7
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 24 2010 Christian Krause <chkr@fedoraproject.org> - 0.0.8-4
- fix %%post and %%postun scripts and install directory for
  pixbuf-loader

* Sun Oct 24 2010 Christian Krause <chkr@fedoraproject.org> - 0.0.8-3
- add upstream patch 22287584fbfa4657098ee997957a6c4fc972a53b to
  properly decompress CFA from certain cameras (BZ 624283)

* Wed Sep 08 2010 Christian Krause <chkr@fedoraproject.org> - 0.0.8-2
- add upstream patch 1b15acdcfdc4664bc6c0be473cb6e096071a4e62
  to support certain PEF files and to fix a crash when opening
  such files (BZ 606898)

* Sat Dec 05 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.0.8-1
- Version bump to 0.0.8.
  * Fixed a huge memory leak. (FreeDesktop Bugzilla #21435)
  * cfa output should write the data in PGM as big endian.
  * Better handling of Canon CR2 "slices" to fix crasher with Canon
    450D/Digital Rebel XSi files (and possibly others).
  * Added new API or_rawfile_new_from_memory() to load a Raw file from a
    memory buffer.
  * Added new API or_rawfile_get_typeid() and the associated consts.
  * Added new API or_rawdata_get_minmax().
  * Added new API or_get_file_extensions().
  * Added new API or_rawfile_get_rendered_image() to get a rendered image.
  * Added new API or_bitmapdata_*().
  * New GdkPixbuf loader.
  * Decompress NEF files.
- License changed to LGPLv3 or later.
- Missing includes fixed by upstream.
- Replaced 'BuildRequires: chrpath glib2-devel' with 'BuildRequires:
  exempi-devel libcurl-devel'.
- Added 'Requires: gtk2' to pixbuf-loader for directory ownership.
- Added a %%check stanza.

* Fri Jul 24 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.0.5-4
- Autorebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Caolán McNamara <caolanm@redhat.com> - 0.0.5-3
- add stdio.h for fopen and friends

* Wed Feb 25 2009 Release Engineering <rel-eng@fedoraproject.org> - 0.0.5-2
- Autorebuild for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Mar 04 2008 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.5-1
- New upstream version.

* Wed Feb 20 2008 Release Engineering <rel-eng@fedoraproject.org> - 0.0.4-3
- Autorebuild for GCC 4.3

* Wed Jan 30 2008 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.4-2
- Added missing dependency on libxml

* Wed Jan 30 2008 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.4-1
- New upstream version.

* Fri Dec 28 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.3-1
- New upstream version.
- Updated license tag.
- Fixed rpath error.

* Thu May 03 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-5
- Added unowned directory to list of files.
- Changed license from GPL to LGPL.

* Wed May 02 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-4
- Moved gui components to a separate package.

* Tue May 01 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-3
- Added missing BuildRequirement.

* Mon Apr 30 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-2
- Added missing BuildRequirement.

* Sun Apr 29 2007 Trond Danielsen <trond.danielsen@gmail.com> - 0.0.2-1
- Inital version.
