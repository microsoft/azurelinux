Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           SFML
Version:        2.5.1
Release:        5%{?dist}
Summary:        Simple and Fast Multimedia Library

# src/SFML/Audio/stb_vorbis/stb_vorbis.{c,h} are Public Domain
License:        zlib and Public Domain
URL:            http://www.sfml-dev.org/
# This is https://www.sfml-dev.org/files/SFML-2.5.1-sources.zip
# with the non free contents removed - See rhbz#1310387 and rhbz#1003569
# List of deleted files
#
# examples/sound/resources/canary.wav
# examples/iOS/resources/canary.wav
# examples/android/app/src/main/assets/canary.wav
# examples/sound/resources/orchestral.ogg
# examples/iOS/resources/orchestral.ogg
# examples/android/app/src/main/assets/orchestral.ogg
# tools/xcode/templates/SFML/SFML CLT.xctemplate/sansation.ttf
# tools/xcode/templates/SFML/SFML App.xctemplate/sansation.ttf
# examples/shader/resources/sansation.ttf
# examples/pong/resources/sansation.ttf
# examples/opengl/resources/sansation.ttf
# examples/joystick/resources/sansation.ttf
# examples/island/resources/sansation.ttf
# examples/iOS/resources/sansation.ttf
# examples/cocoa/resources/sansation.ttf
# examples/android/app/src/main/assets/sansation.ttf
# examples/shader/resources/background.jpg
# examples/opengl/resources/background.jpg
# examples/opengl/resources/texture.jpg
# examples/pong/resources/ball.wav
# examples/shader/resources/devices.png
# examples/win32/resources/image1.jpg
# examples/win32/resources/image2.jpg

Source0:        %{name}-%{version}-clean.tar.gz
Patch0:         SFML-do-not-use-Pong-trademark.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  freetype-devel
BuildRequires:  libvorbis-devel
BuildRequires:  flac-devel
BuildRequires:  systemd-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  glew-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libsndfile-devel
BuildRequires:  libXrandr-devel
BuildRequires:  openal-devel

%description
SFML is a portable and easy to use multimedia API written in C++. You can see
it as a modern, object-oriented alternative to SDL.
SFML is composed of several packages to perfectly suit your needs. You can use
SFML as a minimal windowing system to interface with OpenGL, or as a
fully-featured multimedia library for building games or interactive programs.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p0
# fixup non needed executable permission on regular files
find -type f -print0 | xargs -0 chmod -x
# use system-wide extlibs; so, delete everything modulo stb_image header files
find extlibs/ -type f ! -name 'stb_image*' -print0 | xargs -0 rm


%build
%cmake -DSFML_BUILD_DOC=TRUE .
make %{?_smp_mflags}


%install
%make_install
# remove duplicated documentation
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/*.md
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/doc


%ldconfig_scriptlets


%files
%doc license.md readme.md
%{_libdir}/*.so.*

%files devel
%doc doc/html/*
%{_libdir}/cmake/%{name}/*.cmake
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/sfml-*.pc
%{_libdir}/libsfml-*.so


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.5.1-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 22 2018 Pranav Kant <pranvk@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1
- Drop unnecessary patches
- Remove usage of -DSFML_INSTALL_PKGCONFIG_FILES=ON

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 Pranav Kant <pranvk@fedoraproject.org> - 2.4.2-2
- Rename SFML-2.4.2-clean directory to SFML-2.4.2 before compressing

* Fri Feb 17 2017 Pranav Kant <pranvk@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2
- Patch for -Wstrict-aliasing

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Feb 05 2017 Pranav Kant <pranvk@fedoraproejct.org> - 2.4.1-2
- Add missing update change log entry here

* Sun Feb 05 2017 Pranav Kant <pranvk@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1

* Sat Mar 19 2016 Pranav Kant <pranvk@fedoraproject.org> - 2.3.2-4
- Remove copyright/trademark content - rhbz#1310387

* Sat Feb 27 2016 Hans de Goede <hdegoede@redhat.com> - 2.3.2-3
- Fix unresolved __cpu_model symbol in sfml-graphics.so

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 16 2015 Pranav Kant <pranvk@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Mon Jun 22 2015 Pranav Kant <pranvk@fedoraproject.org> - 2.3-1
- Update to 2.3

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.1-4
- Rebuilt for GCC 5 C++11 ABI change

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 10 2014 Hans de Goede <hdegoede@redhat.com> - 2.1-1
- Update to version 2.1 (rhbz#1033924)

* Mon Nov 18 2013 Hans de Goede <hdegoede@redhat.com> - 2.0-6
- Really move cmake file to proper location (rhbz#997679)
- Remove non free font from source tarbal (rhbz#1003569)

* Mon Nov 18 2013 Hans de Goede <hdegoede@redhat.com> - 2.0-5
- Drop changes to make parallel installable with 1.6, instead compat-SFML16
  has now been changed to avoid the conflicts (rhbz#997679)
- Move cmake file to proper location and put it in -devel

* Mon Nov 18 2013 Dave Airlie <airlied@redhat.com> - 2.0-4
- rebuilt for GLEW 1.10

* Fri Aug 02 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 26 2013 Hans de Goede <hdegoede@redhat.com> - 2.0-2
- Make parallel installable with 1.6 (avoid conflict with compat-SFML16)
- Fix rpmlint warnings
- Fix Source0 URL

* Wed May 01 2013 Julian Sikorski <belegdol@fedoraproject.org> - 2.0-1
- Updated to 2.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.6-9
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 13 2012 Adam Jackson <ajax@redhat.com> - 1.6-8
- Rebuild for glew 1.9.0

* Fri Jul 27 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.6-7
- Rebuilt for glew-1.7

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-5
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.6-4
- Fixed the License tag

* Thu Jan 12 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.6-3
- Use one patch and variables in place of sed to fix the makefile
- Fixed building with libpng-1.5 using a patch from Gentoo
- Updated the gcc patch for gcc-4.7

* Fri Dec 23 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.6-2
- s/libSOIL/SOIL
- Fixed the shared libs usage

* Wed Nov 30 2011 Julian Sikorski <belegdol@fedoraproject.org> - 1.6-1
- Initial RPM release based on Debian package

