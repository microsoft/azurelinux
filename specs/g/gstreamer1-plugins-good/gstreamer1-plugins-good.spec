# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         majorminor      1.0

# Only build extras on fedora
%if 0%{?fedora}
%bcond_without extras
%bcond_without nasm
%else
%bcond_with extras
%bcond_with nasm
%endif

# Only build amrnb/amrwbdec on fedora
%if 0%{?fedora}
%bcond_without amr
%else
%bcond_with amr
%endif

# RHEL 10 will provide Qt 6 and drop Qt 5
%if 0%{?rhel} >= 10
%bcond_with qt5
%else
%bcond_without qt5
%endif

%if 0%{?rhel} && 0%{?rhel} < 10
%bcond_with qt6
%else
%bcond_without qt6
%endif

#global gitrel     140
#global gitcommit  9865730cfa5b3a8b2560d082e7e56b350042d3d2
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

Name:           gstreamer1-plugins-good
Version:        1.26.10
Release: 2%{?dist}
Summary:        GStreamer plugins with good code and licensing

License:        CC0-1.0 AND GPL-2.0-only AND LGPL-2.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND xlock AND MIT AND BSD-3-Clause AND CC-BY-3.0 
URL:            http://gstreamer.freedesktop.org/

%if 0%{?gitrel}
# git clone git://anogit.freedesktop.org/gstreamer/gst-plugins-good
# cd gst-plugins-good; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
Source0:        gst-plugins-good-%{version}.tar.xz
%else
Source0:        http://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-%{version}.tar.xz
%endif

# Register as an AppStream component to be visible in the software center
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
Source1:        gstreamer-good.appdata.xml

BuildRequires:  meson >= 0.48.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

BuildRequires:  cairo-devel >= 1.10.0
BuildRequires:  cairo-gobject-devel >= 1.10.0
BuildRequires:  flac-devel >= 1.1.4
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel >= 1.2.0
BuildRequires:  libshout-devel
BuildRequires:  libsoup3-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXfixes-devel
BuildRequires:  orc-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  speex-devel
BuildRequires:  taglib-devel
BuildRequires:  wavpack-devel
BuildRequires:  libv4l-devel
BuildRequires:  libvpx-devel >= 1.1.0
BuildRequires:  gtk3-devel >= 3.4
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  lame-devel
BuildRequires:  mpg123-devel
BuildRequires:  twolame-devel
BuildRequires:  qt6-qtshadertools
%if %{with nasm}
BuildRequires:  nasm
%endif
BuildRequires:  libgudev-devel
%if %{with amr}
BuildRequires:  opencore-amr-devel
%endif

# extras
%if %{with extras}
BuildRequires:  pipewire-jack-audio-connection-kit-devel
%ifnarch s390 s390x
BuildRequires:  libavc1394-devel
BuildRequires:  libdv-devel
BuildRequires:  libiec61883-devel
BuildRequires:  libraw1394-devel
%endif
%endif

# The soup elements dynamically load either version of libsoup at runtime,
# defaulting to libsoup3 if libsoup2 is not already loaded in the process
Recommends:     libsoup3%{?_isa}

# Obsoletes/Provides moved from plugins-bad-free
Obsoletes:      gstreamer1-plugin-mpg123 < 1.13.1
Provides:       gstreamer1-plugin-mpg123 = %{version}-%{release}

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.


%package gtk
Summary:         GStreamer "good" plugins gtk plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}
# handle upgrade path
Obsoletes:       gstreamer1-plugins-bad-free-gtk < 1.13.1-2
Provides:        gstreamer1-plugins-bad-free-gtk = %{version}-%{release}
Provides:        gstreamer1-plugins-bad-free-gtk%{?_isa} = %{version}-%{release}

%description gtk
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.

This package (%{name}-gtk) contains the gtksink output plugin.

%if %{with qt5}
%package qt
Summary:         GStreamer "good" plugins qt qml plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}

BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5WaylandClient)
BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-linguist

Supplements: (gstreamer1-plugins-good and qt5-qtdeclarative)

%description qt
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.

This package (%{name}-qt) contains the qtsink output plugin.
%endif

%if %{with qt6}
%package qt6
Summary:         GStreamer "good" plugins qt6 qml plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}

BuildRequires: pkgconfig(Qt6Gui)
BuildRequires: pkgconfig(Qt6Qml)
BuildRequires: pkgconfig(Qt6Quick)
BuildRequires: pkgconfig(Qt6WaylandClient)
BuildRequires: pkgconfig(Qt6Linguist)
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-linguist

Supplements: (gstreamer1-plugins-good and qt6-qtdeclarative)

%description qt6
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.

This package (%{name}-qt6) contains the qml6sink output plugin.
%endif

%if %{with extras}
%package extras
Summary:        Extra GStreamer plugins with good code and licensing
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description extras
GStreamer is a streaming media framework, based on graphs of filters
which operate on media data.

GStreamer Good Plugins is a collection of well-supported plugins of
good quality and under the LGPL license.

%{name}-extras contains extra "good" plugins
which are not used very much and require additional libraries
to be installed.
%endif


%prep
%setup -q -n gst-plugins-good-%{version}

%build
%meson \
  -D package-name='Fedora GStreamer-plugins-good package' \
  -D package-origin='http://download.fedoraproject.org' \
  -D doc=disabled \
  -D asm=%{?with_nasm:enabled}%{!?with_nasm:disabled} \
  -D doc=disabled \
  -D orc=enabled \
  -D monoscope=disabled \
  -D aalib=disabled \
  -D libcaca=disabled \
  -D rpicamsrc=disabled \
  -D amrnb=%{?with_amr:enabled}%{!?with_amr:disabled} \
  -D amrwbdec=%{?with_amr:enabled}%{!?with_amr:disabled} \
  -D jack=%{?with_extras:enabled}%{!?with_extras:disabled} \
%ifarch s390 s390x
  -D dv=disabled -D dv1394=disabled \
%else
  -D dv=%{?with_extras:enabled}%{!?with_extras:disabled} \
  -D dv1394=%{?with_extras:enabled}%{!?with_extras:disabled} \
%endif
%if 0%{?flatpak_runtime}
  -D v4l2-gudev=disabled \
%endif
  -D qt-egl=disabled \
  -D qt5=%{?with_qt5:enabled}%{!?with_qt5:disabled} \
  -D qt6=%{?with_qt6:enabled}%{!?with_qt6:disabled}

%meson_build

%install
%meson_install

install -p -D %{SOURCE1} %{buildroot}%{_metainfodir}/gstreamer-good.appdata.xml

find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'

%find_lang gst-plugins-good-%{majorminor}

%files -f gst-plugins-good-%{majorminor}.lang
%license COPYING
%doc AUTHORS NEWS README.md README.static-linking RELEASE REQUIREMENTS
%{_metainfodir}/gstreamer-good.appdata.xml
%if 0
%doc %{_datadir}/gtk-doc/html/gst-plugins-good-plugins-%{majorminor}
%endif

# presets
%dir %{_datadir}/gstreamer-%{majorminor}/presets/
%{_datadir}/gstreamer-%{majorminor}/presets/GstVP8Enc.prs
%{_datadir}/gstreamer-%{majorminor}/presets/GstIirEqualizer10Bands.prs
%{_datadir}/gstreamer-%{majorminor}/presets/GstIirEqualizer3Bands.prs
%{_datadir}/gstreamer-%{majorminor}/presets/GstQTMux.prs

# non-core plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstadaptivedemux2.so
%{_libdir}/gstreamer-%{majorminor}/libgstalaw.so
%{_libdir}/gstreamer-%{majorminor}/libgstalphacolor.so
%{_libdir}/gstreamer-%{majorminor}/libgstalpha.so
%{_libdir}/gstreamer-%{majorminor}/libgstapetag.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiofx.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioparsers.so
%{_libdir}/gstreamer-%{majorminor}/libgstauparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstautodetect.so
%{_libdir}/gstreamer-%{majorminor}/libgstavi.so
%{_libdir}/gstreamer-%{majorminor}/libgstcutter.so
%{_libdir}/gstreamer-%{majorminor}/libgstdebug.so
%{_libdir}/gstreamer-%{majorminor}/libgstdeinterlace.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtmf.so
%{_libdir}/gstreamer-%{majorminor}/libgsteffectv.so
%{_libdir}/gstreamer-%{majorminor}/libgstequalizer.so
%{_libdir}/gstreamer-%{majorminor}/libgstflv.so
%{_libdir}/gstreamer-%{majorminor}/libgstflxdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstgoom2k1.so
%{_libdir}/gstreamer-%{majorminor}/libgstgoom.so
%{_libdir}/gstreamer-%{majorminor}/libgsticydemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3demux.so
%{_libdir}/gstreamer-%{majorminor}/libgstimagefreeze.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterleave.so
%{_libdir}/gstreamer-%{majorminor}/libgstisomp4.so
%{_libdir}/gstreamer-%{majorminor}/libgstlevel.so
%{_libdir}/gstreamer-%{majorminor}/libgstmatroska.so
%{_libdir}/gstreamer-%{majorminor}/libgstmulaw.so
%{_libdir}/gstreamer-%{majorminor}/libgstmultifile.so
%{_libdir}/gstreamer-%{majorminor}/libgstmultipart.so
%{_libdir}/gstreamer-%{majorminor}/libgstnavigationtest.so
%{_libdir}/gstreamer-%{majorminor}/libgstoss4.so
%{_libdir}/gstreamer-%{majorminor}/libgstreplaygain.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtsp.so
%{_libdir}/gstreamer-%{majorminor}/libgstshapewipe.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmpte.so
%{_libdir}/gstreamer-%{majorminor}/libgstspectrum.so
%{_libdir}/gstreamer-%{majorminor}/libgstudp.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideobox.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideocrop.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideofilter.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideomixer.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstximagesrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstxingmux.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4menc.so

# gstreamer-plugins with external dependencies but in the main package
%{_libdir}/gstreamer-%{majorminor}/libgstcairo.so
%{_libdir}/gstreamer-%{majorminor}/libgstflac.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdkpixbuf.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpeg.so
%{_libdir}/gstreamer-%{majorminor}/libgstossaudio.so
%{_libdir}/gstreamer-%{majorminor}/libgstpng.so
%{_libdir}/gstreamer-%{majorminor}/libgstpulseaudio.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtpmanager.so
%{_libdir}/gstreamer-%{majorminor}/libgstshout2.so
%{_libdir}/gstreamer-%{majorminor}/libgstsoup.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeex.so
%{_libdir}/gstreamer-%{majorminor}/libgsttaglib.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideo4linux2.so
%{_libdir}/gstreamer-%{majorminor}/libgstvpx.so
%{_libdir}/gstreamer-%{majorminor}/libgstwavpack.so
%{_libdir}/gstreamer-%{majorminor}/libgstlame.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpg123.so
%{_libdir}/gstreamer-%{majorminor}/libgsttwolame.so

%if %{with amr}
%{_libdir}/gstreamer-%{majorminor}/libgstamrnb.so
%{_libdir}/gstreamer-%{majorminor}/libgstamrwbdec.so
%{_datadir}/gstreamer-%{majorminor}/presets/GstAmrnbEnc.prs
%endif

%files gtk
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstgtk.so

%if %{with qt5}
%files qt
%{_libdir}/gstreamer-%{majorminor}/libgstqmlgl.so
%endif

%if %{with qt6}
%files qt6
%{_libdir}/gstreamer-%{majorminor}/libgstqml6.so
%endif

%if %{with extras}
%files extras
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstjack.so
%ifnarch s390 s390x
%{_libdir}/gstreamer-%{majorminor}/libgstdv.so
%{_libdir}/gstreamer-%{majorminor}/libgst1394.so
%endif
%endif


%changelog
* Tue Jan 06 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.26.10-1
- 1.26.10

* Wed Dec 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.9-1
- 1.26.9

* Wed Nov 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.8-1
- 1.26.8

* Sat Nov 01 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.7-4
- Qt6 re-rebuild

* Thu Oct 30 2025 Jan Grulich <jgrulich@redhat.com> - 1.26.7-3
- Rebuild (qt6)

* Tue Oct 21 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.7-2
- v4l2: Fix NULL pointer dereference in probe error path

* Tue Oct 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.7-1
- 1.26.7

* Tue Sep 30 2025 Jan Grulich <jgrulich@redhat.com> - 1.26.6-2
- Rebuild (qt6)

* Mon Sep 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.6-1
- 1.26.6

* Fri Aug 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.5-1
- 1.26.5

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.3-1
- 1.26.3

* Fri May 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.2-1
- 1.26.2

* Tue May 27 2025 Jitka Plesnikova <jplesnik@redhat.com> - 1.26.1-2
- Rebuilt for flac 1.5.0

* Fri Apr 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.1-1
- 1.26.1

* Tue Mar 25 2025 Jan Grulich <jgrulich@redhat.com> - 1.26.0-2
- Rebuild (qt6)

* Wed Mar 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.0-1
- 1.26.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.24.11-1
- 1.24.11

* Wed Dec 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.10-1
- 1.24.10

* Thu Oct 31 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.9-1
- 1.24.9

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 1.24.8-2
- Rebuild (qt6)

* Thu Sep 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.8-1
- 1.24.8

* Wed Aug 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.7-1
- 1.24.7

* Mon Jul 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.6-1
- 1.24.6

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.5-1
- 1.24.5

* Wed May 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.4-1
- 1.24.4

* Tue Apr 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.3-1
- 1.24.3

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 1.24.0-2
- Rebuild (qt6)

* Tue Mar 05 2024 Wim Taymans <wtaymans@redhat.com> - 1.24.0-1
- Update to 1.24.0

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 1.22.9-3
- Rebuild (qt6)

* Tue Feb 13 2024 Pete Walter <pwalter@fedoraproject.org> - 1.22.9-2
- Rebuild for libvpx 1.14.x

* Thu Jan 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.22.9-1
- 1.22.9

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.22.8-1
- 1.22.8

* Wed Nov 29 2023 Jan Grulich <jgrulich@redhat.com> - 1.22.7-2
- Rebuild (qt6)

* Tue Nov 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.22.7-1
- 1.22.7

* Fri Oct 13 2023 Jan Grulich <jgrulich@redhat.com> - 1.22.5-3
- Rebuild (qt6)

* Thu Oct 05 2023 Jan Grulich <jgrulich@redhat.com> - 1.22.5-2
- Rebuild (qt6)

* Fri Jul 21 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.5-1
- Update to 1.22.5
- Disable qt-egl and add some BuildRequires to make things compile.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 18 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.22.3-2
- Enable Qt6 plugin, disable Qt5 plugin for RHEL 10

* Thu May 25 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.3-1
- Update to 1.22.3

* Thu Apr 13 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.2-1
- Update to 1.22.2

* Mon Mar 13 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.1-1
- Update to 1.22.1

* Wed Feb 15 2023 Tom Callaway <spot@fedoraproject.org> - 1.22.0-2
- rebuild for new libvpx

* Tue Jan 24 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.0-1
- Update to 1.22.0

* Fri Jan 20 2023 Wim Taymans <wtaymans@redhat.com> - 1.21.90-1
- Update to 1.21.90

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Wim Taymans <wtaymans@redhat.com> - 1.20.5-1
- Update to 1.20.5

* Thu Oct 13 2022 Wim Taymans <wtaymans@redhat.com> - 1.20.4-1
- Update to 1.20.4

* Tue Sep 13 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.20.3-3
- Rebuilt for flac 1.4.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Wim Taymans <wtaymans@redhat.com> - 1.20.3-1
- Update to 1.20.3

* Fri Feb 4 2022 Wim Taymans <wtaymans@redhat.com> - 1.20.0-1
- Update to 1.20.0

* Thu Jan 27 2022 Tom Callaway <spot@fedoraproject.org> - 1.19.3-4
- rebuild for libvpx

* Wed Jan 26 2022 Wim Taymans <wtaymans@redhat.com> - 1.19.3-3
- Fix build

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 11 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.3-1
- Update to 1.19.3

* Thu Sep 23 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.2-1
- Update to 1.19.2

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.1-1
- Update to 1.19.1

* Fri May 14 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.4-2
- Move libdv and friends to extras

* Tue Mar 16 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.4-1
- Update to 1.18.4

* Tue Feb 23 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.2-3
- use only nasm on fedora

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.2-1
- Update to 1.18.2

* Fri Oct 30 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.1-1
- Update to 1.18.1

* Wed Oct 28 2020 Jeff Law <law@redhat.com> - 1.18.0-2
- Fix bogus use of volatile diagnosed by gcc-11

* Tue Sep 8 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.0-1
- Update to 1.18.0

* Fri Aug 21 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.90-1
- Update to 1.17.90
- disable rpicamsrc

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 6 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.2-1
- Update to 1.17.2

* Mon Jun 22 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.1-1
- Update to 1.17.1
- disable dv and 1394 on s390

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 2 2020 Wim Taymans <wtaymans@redhat.com> - 1.16.2-1
- Update to 1.16.2

* Fri Sep 27 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.1-2
- Enable cairo plugins. (rhbz#1737254)

* Tue Sep 24 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.1-1
- Update to 1.16.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.0-1
- Update to 1.16.0

* Thu Mar 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.15.2-3
- -qt: fix Supplements

* Thu Mar 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.15.2-2
- -qt subpkg

* Fri Mar 01 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.2-1
- Update to 1.15.2

* Tue Feb 05 2019 Björn Esser <besser82@fedoraproject.org> - 1.15.1-3
- rebuilt (libvpx)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.1-1
- Update to 1.15.1

* Wed Oct 03 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.4-1
- Update to 1.14.4

* Tue Sep 18 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.3-1
- Update to 1.14.3

* Mon Jul 23 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.2-1
- Update to 1.14.2

* Fri Jul 20 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-5
- Add c++ buildrequires
- Only build extras on fedora

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-3
- Rebuild to correct Provides (#1581325)
- Remove check line that was added for testing

* Tue May 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.1-2
- use %%make_build %%make_install %%_metainfodir
- %%build: --disable-qt (for now)

* Mon May 21 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-1
- Update to 1.14.1

* Fri Mar 23 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.14.0-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Mar 20 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.0-1
- Update to 1.14.0

* Wed Mar 14 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.91-1
- Update to 1.13.91

* Mon Mar 05 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.90-1
- Update to 1.13.90

* Tue Feb 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.13.1-3
- -gtk: Obsoletes/Provides: gstreamer1-plugins-bad-free-gtk
- Obsoletes/Provides: gstreamer1-plugin-mpg123

* Tue Feb 27 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.1-2
- The gtk plugin was moved from -bad, make a new subpackage for it.
- the mp3 plugins were moved from -ugly, add BuildRequires.
- build requires GL now for gtkglsink

* Tue Feb 27 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.1-1
- Update to 1.13.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.12.4-3
- rebuild (libvpx)

* Fri Jan 26 2018 Tom Callaway <spot@fedoraproject.org> - 1.12.4-2
- rebuild for new libvpx

* Mon Dec 11 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.4-1
- Update to 1.12.4

* Fri Oct 13 2017 Troy Dawson <tdawson@redhat.com> - 1.12.3-2
- Cleanup spec file conditionals

* Tue Sep 19 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.3-1
- Update to 1.12.3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.2-1
- Update to 1.12.2

* Tue Jun 20 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.1-1
- Update to 1.12.1

* Wed May 10 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.0-1
- Update to 1.12.0

* Fri Apr 28 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.91-1
- Update to 1.11.91

* Tue Apr 11 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.90-1
- Update to 1.11.90
- Update plugin names

* Fri Feb 24 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.2-1
- Update to 1.11.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.1-1
- Update to 1.11.1

* Mon Dec 05 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.2-1
- Update to 1.10.2
- Remove obsolete patches

* Mon Nov 28 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.1-2
- Add fix for gstreamer FLIC decoder vulnerability

* Mon Nov 28 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Thu Nov 03 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Sat Oct 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.90-1
- Update to 1.9.90
- add QTMux presets

* Thu Sep 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.2-1
- Update to 1.9.2

* Fri Jul 22 2016 Tom Callaway <spot@fedoraproject.org> - 1.9.1-2
- rebuild for new libvpx

* Thu Jul 07 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Thu Jun 09 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Thu Apr 21 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Thu Mar 24 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Wed Mar 16 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.91-1
- Update to 1.7.91

* Wed Mar 02 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.90-1
- Update to 1.7.90

* Fri Feb 19 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.2-1
- Update to 1.7.2

* Fri Feb 05 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.7.1-3
- Append --disable-fatal-warnings to %%configure to prevent
  building from aborting for negligible warnings (Fix F24FTBFS)
- Append --disable-silent-rules to %%configure to make
  building verbose.
- Don't remove buildroot before installing.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 5 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Tue Dec 15 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.2-1
- Update to 1.6.2

* Tue Dec 1 2015 Tom Callaway <spot@fedoraproject.org> - 1.6.1-2
- rebuild for libvpx 1.5.0

* Mon Nov 2 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0
- Use license macro for COPYING

* Mon Sep 21 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.91-1
- Update to 1.5.91

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 1.5.90-2
- Add optional data to AppStream metadata.

* Wed Aug 19 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.90-1
- Update to 1.5.90

* Sat Jul 18 2015 Francesco Frassinelli <fraph24@gmail.com> - 1.5.2-2
- Add missing dependencies required by ximagesrc. (#1136317)

* Thu Jun 25 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 8 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.1-1
- Update to 1.5.1
- Remove obsolete patches

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.5-5
- Rebuilt for GCC 5 C++11 ABI change

* Mon Apr  6 2015 Tom Callaway <spot@fedoraproject.org> - 1.4.5-4
- rebuild against libvpx 1.4.0

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.4.5-3
- Register as an AppStream component.

* Fri Mar 06 2015 David Woodhouse <dwmw2@infradead.org> - 1.4.5-2
- Don't force RTP jitterbuffer clock-rate (#1199579)

* Wed Jan 28 2015 Bastien Nocera <bnocera@redhat.com> - 1.4.5-1
- Update to 1.4.5

* Fri Nov 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.4-1
- Update to 1.4.4

* Mon Sep 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.2-1
- Update to 1.4.2.
- Drop old patches

* Fri Aug 29 2014 Hans de Goede <hdegoede@redhat.com> - 1.4.1-2
- Fix v4l2-src not working with some v4l2 devices (bgo#735660)

* Fri Aug 29 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.1-1
- Update to 1.4.1.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.0-1
- Update to 1.4.0.

* Fri Jul 11 2014 Wim Taymans <wtaymans@redhat.com> - 1.3.91-1
- Update to 1.3.91.

* Tue Jun 17 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.4-1
- Update to 1.2.4.
- Drop old patches

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.3-2
- Rebuild for libvpx ABI break. See #1068664
- fix doc build

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.

* Tue Jan 14 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.2-2
- Disable the cairo plugin, we don't package it.

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.90-1
- Update to 1.1.90.

* Wed Aug 28 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4.

* Mon Jul 29 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3.

* Fri Jul 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Sun Mar 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Drop BR on PyXML.

* Wed Feb  6 2013 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.5-3
- Add gdk-pixbuf2-devel build dep. It was pulled in by something else for gst 0.10

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 1.0.5-2
- rebuild due to "jpeg8-ABI" feature drop

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3
- Drop speexdec patch. Fixed upstream.
- Drop vp8 patches. Fixed upstream.

* Wed Nov  7 2012 Debarshi Ray <rishi@fedoraproject.org> - 1.0.2-3
- Fixes for GNOME #687464 and #687793

* Fri Nov  2 2012 Debarshi Ray <rishi@fedoraproject.org> - 1.0.2-2
- Fixes for vp8dec including GNOME #687376

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- Drop upstream patches since they are included in latest release.

* Wed Oct 24 2012 Debarshi Ray <rishi@fedoraproject.org> - 1.0.1-2
- Fix target-bitrate for vp8enc

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Tue Oct  2 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-3
- Add required version for vpx-devel. (#862157)

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-2
- Enable verbose build

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Fri Sep 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-2
- Add vp8 plugin to package from gst1-plugins-bad. (#859505)

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.
- Drop v4l2-buffer patch. Fixed upstream.

* Wed Aug 15 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.
- Add batch to fix build with recent kernels, the v4l2_buffer input field was removed.
- Use %%global instead of %%define.

* Wed Jul 18 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec.
