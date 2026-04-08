# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           allegro
Version:        4.4.3.1
Release:        18%{?dist}

Summary:        A game programming library
Summary(es):    Una libreria de programacion de juegos
Summary(fr):    Une librairie de programmation de jeux
Summary(it):    Una libreria per la programmazione di videogiochi
Summary(cs):    Knihovna pro programování her

License:        Giftware
URL:            http://liballeg.org/
Source0:        https://github.com/liballeg/allegro5/releases/download/%{version}/allegro-%{version}.tar.gz
Patch1:         allegro-4.0.3-cfg.patch
Patch2:         allegro-4.0.3-libdir.patch
Patch5:         allegro-4.4.2-buildsys-fix.patch
Patch6:         allegro-4.4.2-doc-noversion.patch
# Replace racy recursive mutex implementation with proper recursive mutexes
Patch8:         allegro-4.4.2-mutex-fix.patch
# Calling Xsync from the bg thread causes deadlock issues
Patch9:         allegro-4.4.2-no-xsync-from-thread.patch
# gnome-shell starts apps while gnome-shell has the keyb grabbed...
Patch10:        allegro-4.4.2-keybgrab-fix.patch
# 4.4.3 has dropped the fadd/fsub etc aliases, but some apps need them
Patch11:        allegro-4.4.2-compat-fix-aliases.patch
# 4.4.3 accidentally broke the tools, fix them (rhbz1682921)
Patch12:        allegro-4.4.3-datafile-double-free.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1767827
# starting texinfo-6.7 the default encoding is UTF-8 and because allegro's
# source .texi file is encoded in ISO-8859-1, additional command is needed
Patch13:        allegro-4.4.3-texinfo-non-utf8-input-fix.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2225996
# Fix a buffer overflow in dat2c tool causing FTBFS of allegro using packages
Patch14:        allegro-4.4.3-dat2c-buffer-overflow.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  texinfo cmake
BuildRequires:  xorg-x11-proto-devel libX11-devel libXpm-devel libXcursor-devel
BuildRequires:  libXxf86vm-devel libXxf86dga-devel libGL-devel libGLU-devel
BuildRequires:  alsa-lib-devel jack-audio-connection-kit-devel
BuildRequires:  libjpeg-devel libpng-devel libvorbis-devel
Requires:       timidity++-patches

%description
Allegro is a cross-platform library intended for use in computer games
and other types of multimedia programming.

%description -l es
Allegro es una librería multi-plataforma creada para ser usada en la
programación de juegos u otro tipo de programación multimedia.

%description -l fr
Allegro est une librairie multi-plateforme destinée à être utilisée
dans les jeux vidéo ou d'autres types de programmation multimédia.

%description -l it
Allegro è una libreria multipiattaforma dedicata all'uso nei
videogiochi ed in altri tipi di programmazione multimediale.

%description -l cs
Allegro je multiplatformní knihovna pro počítačové hry a jiné
typy multimediálního programování.


%package devel
Summary:        A game programming library
Summary(es):    Una libreria de programacion de juegos
Summary(fr):    Une librairie de programmation de jeux
Summary(it):    Una libreria per la programmazione di videogiochi
Summary(cs):    Knihovna pro programování her
Requires:       %{name}%{?_isa} = %{version}-%{release}, xorg-x11-proto-devel
Requires:       libX11-devel, libXcursor-devel

%description devel
Allegro is a cross-platform library intended for use in computer games
and other types of multimedia programming. This package is needed to
build programs written with Allegro.

%description devel -l es
Allegro es una librería multi-plataforma creada para ser usada en la
programación de juegos u otro tipo de programación multimedia. Este
paquete es necesario para compilar los programas que usen Allegro.

%description devel -l fr
Allegro est une librairie multi-plateforme destinée à être utilisée
dans les jeux vidéo ou d'autres types de programmation multimédia. Ce
package est nécessaire pour compiler les programmes utilisant Allegro.

%description devel -l it
Allegro è una libreria multipiattaforma dedicata all'uso nei
videogiochi ed in altri tipi di programmazione multimediale. Questo
pacchetto è necessario per compilare programmi scritti con Allegro.

%description devel -l cs
Allegro je multiplatformní knihovna pro počítačové hry a jiné
typy multimediálního programování. Tento balíček je je potřebný
k sestavení programů napsaných v Allegru.


%package tools
Summary:        Extra tools for the Allegro programming library
Summary(es):    Herramientas adicionales para la librería de programación Allegro
Summary(fr):    Outils supplémentaires pour la librairie de programmation Allegro
Summary(it):    Programmi di utilità aggiuntivi per la libreria Allegro
Summary(cs):    Přídavné nástroje pro programovou knihovnu Allegro
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description tools
Allegro is a cross-platform library intended for use in computer games
and other types of multimedia programming. This package contains extra
tools which are useful for developing Allegro programs.

%description tools -l es
Allegro es una librería multi-plataforma creada para ser usada en la
programación de juegos u otro tipo de programación multimedia. Este
paquete contiene herramientas adicionales que son útiles para
desarrollar programas que usen Allegro.

%description tools -l fr
Allegro est une librairie multi-plateforme destinée à être utilisée
dans les jeux vidéo ou d'autres types de programmation multimédia. Ce
package contient des outils supplémentaires qui sont utiles pour le
développement de programmes avec Allegro.

%description tools -l it
Allegro è una libreria multipiattaforma dedicata all'uso nei
videogiochi ed in altri tipi di programmazione multimediale. Questo
pacchetto contiene programmi di utilità aggiuntivi utili allo sviluppo
di programmi con Allegro.

%description tools -l cs
Allegro je multiplatformní knihovna pro počítačové hry a jiné
typy multimediálního programování. Tento balíček obsahuje přídavné nástroje,
které jsou užitečné pro vývoj Allegro programů.

%package jack-plugin
Summary:        Allegro JACK (Jack Audio Connection Kit) plugin
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description jack-plugin
This package contains a plugin for Allegro which enables Allegro to playback
sound through JACK (Jack Audio Connection Kit).


%package -n alleggl
Summary:        OpenGL support library for Allegro
License:        Zlib OR GPL-1.0-or-later
URL:            http://allegrogl.sourceforge.net/
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n alleggl
AllegroGL is an Allegro add-on that allows you to use OpenGL alongside Allegro.
You use OpenGL for your rendering to the screen, and Allegro for miscellaneous
tasks like gathering input, doing timers, getting cross-platform portability,
loading data, and drawing your textures. So this library fills the same hole
that things like glut do.

%package -n alleggl-devel
Summary:        Development files for alleggl
License:        Zlib OR GPL-1.0-or-later
Requires:       alleggl%{?_isa} = %{version}-%{release}

%description -n alleggl-devel
The alleggl-devel package contains libraries and header files for
developing applications that use alleggl.


%package -n jpgalleg
Summary:        JPEG library for the Allegro game library
License:        Zlib
URL:            http://www.ecplusplus.com/index.php?page=projects&pid=1
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n jpgalleg
jpgalleg is a JPEG library for use with the Allegro game library. It allows
using JPEG's as Allegro bitmaps.

%package -n jpgalleg-devel
Summary:        Development files for jpgalleg
License:        Zlib
Requires:       jpgalleg%{?_isa} = %{version}-%{release}

%description -n jpgalleg-devel
The jpgalleg-devel package contains libraries and header files for
developing applications that use jpgalleg.


%package loadpng
Summary:        OGG/Vorbis library for the Allegro game library
License:        LicenseRef-Fedora-Public-Domain
URL:            http://wiki.allegro.cc/index.php?title=LoadPNG
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description loadpng
loadpng is some glue that makes it easy to use libpng to load and
save bitmaps from Allegro programs.

%package loadpng-devel
Summary:        Development files for loadpng
License:        LicenseRef-Fedora-Public-Domain
Requires:       %{name}-loadpng%{?_isa} = %{version}-%{release}

%description loadpng-devel
The loadpng-devel package contains libraries and header files for
developing applications that use loadpng.


%package logg
Summary:        OGG/Vorbis library for the Allegro game library
License:        MIT
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description logg
LOGG is an Allegro add-on library for playing OGG/Vorbis audio files.

%package logg-devel
Summary:        Development files for logg
License:        MIT
Requires:       %{name}-logg%{?_isa} = %{version}-%{release}

%description logg-devel
The logg-devel package contains libraries and header files for
developing applications that use logg.


%prep
%autosetup -p1

%build
export CMAKE_POLICY_VERSION_MINIMUM=3.5
%cmake \
%if "%{?_lib}" == "lib64"
 %{?_cmake_lib_suffix64} \
%endif
 -DOpenGL_GL_PREFERENCE:STRING=LEGACY -DCMAKE_SKIP_RPATH:BOOL=YES -DCMAKE_SKIP_INSTALL_RPATH:BOOL=YES \
 -DDOCDIR:STRING=%{_pkgdocdir} -DCMAKE_VERBOSE_MAKEFILE:BOOL=TRUE
%cmake_build

pushd %{_vpath_builddir}
# Converting text documentation to UTF-8 encoding.
for file in docs/AUTHORS docs/CHANGES docs/THANKS \
        docs/info/*.info docs/txt/*.txt docs/man/get_camera_matrix.3 \
        ../addons/allegrogl/changelog; do
  iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
  touch -r $file $file.new && \
  mv $file.new $file
done
popd

%install
%cmake_install

pushd %{_vpath_builddir}
# installation of these is broken, because they use a cmake GLOB, but
# that gets "resolved" when runnning cmake, and at that time the files
# to install aren't generated yet ...
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/html
install -p -m 644 docs/man/*.3 $RPM_BUILD_ROOT%{_mandir}/man3
install -p -m 644 docs/html/*.{html,css} \
    $RPM_BUILD_ROOT%{_pkgdocdir}/html/
install -m 755 docs/makedoc $RPM_BUILD_ROOT%{_bindir}/allegro-makedoc
popd

# Install some extra files
install -Dpm 644 allegro.cfg $RPM_BUILD_ROOT%{_sysconfdir}/allegrorc
install -pm 755 tools/x11/xfixicon.sh $RPM_BUILD_ROOT%{_bindir}
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/allegro
install -pm 644 keyboard.dat language.dat $RPM_BUILD_ROOT%{_datadir}/allegro
install -Dpm 644 misc/allegro.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal/allegro.m4

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/allegrogl
install -pm 644 addons/allegrogl/changelog addons/allegrogl/faq.txt \
 addons/allegrogl/readme.txt addons/allegrogl/bugs.txt \
 addons/allegrogl/extensions.txt addons/allegrogl/howto.txt addons/allegrogl/quickstart.txt \
 addons/allegrogl/todo.txt $RPM_BUILD_ROOT%{_pkgdocdir}/allegrogl/

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/loadpng
install -pm 644 addons/loadpng/CHANGES.txt addons/loadpng/README.txt addons/loadpng/THANKS.txt \
 $RPM_BUILD_ROOT%{_pkgdocdir}/loadpng/

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/jpgalleg
install -pm 644 addons/jpgalleg/readme.txt \
 $RPM_BUILD_ROOT%{_pkgdocdir}/jpgalleg/


%ldconfig_scriptlets 
%ldconfig_scriptlets -n alleggl 

%ldconfig_scriptlets -n jpgalleg

%ldconfig_scriptlets loadpng

%ldconfig_scriptlets logg


%files
%{_pkgdocdir}/
%exclude %{_pkgdocdir}/dat*.txt
%exclude %{_pkgdocdir}/grabber.txt
%exclude %{_pkgdocdir}/allegrogl
%exclude %{_pkgdocdir}/jpgalleg
%exclude %{_pkgdocdir}/loadpng
%exclude %{_pkgdocdir}/loadpng
%license %{_pkgdocdir}/license.txt
%config(noreplace) %{_sysconfdir}/allegrorc
%{_libdir}/liballeg.so.4*
%{_datadir}/allegro
# We cannot use exclude for alleg-jack.so because then the build-id for it
# still ends up in the main allegro package, e.g. rpmlint says:
# allegro.x86_64: W: dangling-relative-symlink /usr/lib/.build-id/48/024a0ddad02d9c6f4b956fb18f20d4a0bfde41 ../../../../usr/lib64/allegro/4.4.3/alleg-jack.so
%dir %{_libdir}/allegro
%dir %{_libdir}/allegro/4.4.3
%{_libdir}/allegro/4.4.3/alleg-alsa*.so
%{_libdir}/allegro/4.4.3/alleg-dga2.so
%{_libdir}/allegro/4.4.3/modules.lst

%files devel
%{_bindir}/allegro-config
%{_bindir}/allegro-makedoc
%{_libdir}/liballeg.so
%{_libdir}/pkgconfig/allegro.pc
%{_includedir}/allegro
%{_includedir}/allegro.h
%{_includedir}/xalleg.h
%{_datadir}/aclocal/allegro.m4
%{_infodir}/allegro.info*
%{_mandir}/man3/*

%files tools
%{_pkgdocdir}/dat*.txt
%{_pkgdocdir}/grabber.txt
%{_bindir}/colormap
%{_bindir}/dat
%{_bindir}/dat2s
%{_bindir}/dat2c
%{_bindir}/exedat
%{_bindir}/grabber
%{_bindir}/pack
%{_bindir}/pat2dat
%{_bindir}/rgbmap
%{_bindir}/textconv
%{_bindir}/xfixicon.sh

%files jack-plugin
%{_libdir}/allegro/4.4.3/alleg-jack.so

%files -n alleggl
%license addons/allegrogl/gpl.txt
%license addons/allegrogl/zlib.txt
%{_libdir}/liballeggl.so.4*

%files -n alleggl-devel
%{_pkgdocdir}/allegrogl/
%{_libdir}/liballeggl.so
%{_libdir}/pkgconfig/allegrogl.pc
%{_includedir}/alleggl.h
%{_includedir}/allegrogl

%files -n jpgalleg
%license addons/jpgalleg/license.txt
%{_libdir}/libjpgalleg.so.4*

%files -n jpgalleg-devel
%{_pkgdocdir}/jpgalleg/
%{_libdir}/libjpgalleg.so
%{_libdir}/pkgconfig/jpgalleg.pc
%{_includedir}/jpgalleg.h

%files loadpng
%license addons/loadpng/LICENSE.txt
%{_pkgdocdir}/loadpng/
%{_libdir}/libloadpng.so.4*

%files loadpng-devel
%{_libdir}/libloadpng.so
%{_libdir}/pkgconfig/loadpng.pc
%{_includedir}/loadpng.h

%files logg
%license addons/logg/LICENSE.txt
%{_libdir}/liblogg.so.4*

%files logg-devel
%{_libdir}/liblogg.so
%{_libdir}/pkgconfig/logg.pc
%{_includedir}/logg.h


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Cristian Le <git@lecris.dev> - 4.4.3.1-17
- Add LIB_SUFFIX flag explicitly (rhbz#2381173)

* Fri May 30 2025 Cristian Le <git@lecris.dev> - 4.4.3.1-16
- Allow to build with CMake 4.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 26 2023 Hans de Goede <hdegoede@redhat.com> - 4.4.3.1-11
- Fix dat2c bug causing FTBFS of allegro using packages (rhbz#2225996)
- Trim changelog

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Antonio Trande <sagitter@fedoraproject.org> - 4.4.3.1-1
- Release 4.4.3.1
- Use %%_pkgdocdir
- Use CMake3 on epel
- Use dedicated CMake 'build' directory
- Patched for texinfo-6.7 (rhbz#1767827)
