Vendor:         Microsoft Corporation
Distribution:   Mariner
%global         majorminor 1.0
%global         _gobject_introspection  1.31.1
%{!?_metainfodir: %global _metainfodir %{_datadir}/metainfo}

%bcond_with gtk_doc
%bcond_with extras

#global gitrel     140
#global gitcommit  4ca3a22b6b33ad8be4383063e76f79c4d346535d
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

Name:           gstreamer1-plugins-bad-free
Version:        1.16.2
Release:        6%{?dist}
Summary:        GStreamer streaming media framework "bad" plugins

License:        LGPLv2+ and LGPLv2
URL:            http://gstreamer.freedesktop.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/gst-plugins-good
# cd gst-plugins-good; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
# modified with gst-p-bad-cleanup.sh from SOURCE1
%else
# The source is:
# http://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz
# modified with gst-p-bad-cleanup.sh from SOURCE1
%endif
Source0:        gst-plugins-bad-free-%{version}.tar.xz
Source1:        gst-p-bad-cleanup.sh

# https://gitlab.freedesktop.org/gstreamer/common/-/merge_requests/4
# https://bugzilla.redhat.com/show_bug.cgi?id=1799497
Patch0:         gstreamer1-plugins-bad-build-adapt-to-backwards-incompatible-change.patch

# https://gitlab.freedesktop.org/gstreamer/gst-plugins-bad/-/merge_requests/1125
# https://bugzilla.redhat.com/show_bug.cgi?id=1799497
Patch1:         gstreamer1-plugins-bad-lv2-make-it-build-with-fno-common.patch

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  check
BuildRequires:  gettext-devel
BuildRequires:  libXt-devel

BuildRequires:  gobject-introspection-devel >= %{_gobject_introspection}
%if %{with gtk_doc}
BuildRequires:  gtk-doc
%endif

BuildRequires:  bzip2-devel
BuildRequires:  exempi-devel
BuildRequires:  fdk-aac-free-devel
BuildRequires:  gsm-devel
BuildRequires:  jasper-devel
BuildRequires:  ladspa-devel
BuildRequires:  lcms2-devel
BuildRequires:  libdvdnav-devel
BuildRequires:  libexif-devel
BuildRequires:  libmpcdec-devel
BuildRequires:  libnice-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libsndfile-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  openssl-devel
BuildRequires:  orc-devel
BuildRequires:  soundtouch-devel
BuildRequires:  wavpack-devel
BuildRequires:  opus-devel
BuildRequires:  nettle-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  wayland-devel
BuildRequires:  gnutls-devel
BuildRequires:  libsrtp-devel
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  gtk3-devel >= 3.4
BuildRequires:  bluez-libs-devel >= 5.0
BuildRequires:  libwebp-devel
BuildRequires:  mesa-libEGL-devel
#BuildRequires:  vulkan-devel
#BuildRequires:  mesa-vulkan-devel
BuildRequires:  webrtc-audio-processing-devel
BuildRequires:  lilv-devel

%if %{with extras}
BuildRequires:  libbs2b-devel >= 3.1.0
## Plugins not ported
#BuildRequires:  dirac-devel
#BuildRequires:  gmyth-devel >= 0.4
BuildRequires:  fluidsynth-devel
BuildRequires:  libass-devel
BuildRequires:  libchromaprint-devel
## Plugin not ported
#BuildRequires:  libcdaudio-devel
BuildRequires:  libcurl-devel
BuildRequires:  game-music-emu-devel
BuildRequires:  libkate-devel
BuildRequires:  libmodplug-devel
BuildRequires:  libofa-devel
## Plugins not ported
#BuildRequires:  libmusicbrainz-devel
#BuildRequires:  libtimidity-devel
BuildRequires:  libvdpau-devel
BuildRequires:  openal-soft-devel
#BuildRequires:  opencv-devel
BuildRequires:  openjpeg2-devel
## Plugins not ported
#BuildRequires:  SDL-devel
BuildRequires:  wildmidi-devel
BuildRequires:  zbar-devel
BuildRequires:  zvbi-devel
BuildRequires:  OpenEXR-devel
%endif

# libgstfdkaac.so used to be shipped in -nonfree
Obsoletes: gstreamer1-plugins-bad-nonfree < 1.16.1-2

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins that aren't tested well enough, or the code
is not of good enough quality.


%if %{with extras}
%package extras
Summary:         Extra GStreamer "bad" plugins (less often used "bad" plugins)
Requires:        %{name}%{?_isa} = %{version}-%{release}

%description extras
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

gstreamer-plugins-bad contains plug-ins that aren't tested well enough,
or the code is not of good enough quality.

This package (%{name}-extras) contains
extra "bad" plugins for sources (mythtv), sinks (fbdev) and
effects (pitch) which are not used very much and require additional
libraries to be installed.


%package fluidsynth
Summary:         GStreamer "bad" plugins fluidsynth plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}
Requires:        soundfont2-default

%description fluidsynth
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

gstreamer-plugins-bad contains plug-ins that aren't tested well enough,
or the code is not of good enough quality.

This package (%{name}-fluidsynth) contains the fluidsynth
plugin which allows playback of midi files.


%package wildmidi
Summary:         GStreamer "bad" plugins wildmidi plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}

%description wildmidi
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

gstreamer-plugins-bad contains plug-ins that aren't tested well enough,
or the code is not of good enough quality.

This package (%{name}-wildmidi) contains the wildmidi
plugin which allows playback of midi files.
%endif


%package devel
Summary:        Development files for the GStreamer media framework "bad" plug-ins
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gstreamer1-plugins-base-devel

%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins that
aren't tested well enough, or the code is not of good enough quality.


%prep
%setup -q -n gst-plugins-bad-%{version}
%patch0 -p1
%patch1 -p1


%build
autoreconf --force --install
%configure --disable-silent-rules --disable-fatal-warnings \
    --with-package-name="Fedora GStreamer-plugins-bad package" \
    --with-package-origin="http://download.fedoraproject.org" \
    %if %{with gtk_doc}
    --enable-gtk-doc \
    %endif
    %{!?with_extras:--disable-curl --disable-fbdev --disable-decklink --disable-linsys} \
    --enable-debug --disable-static --enable-experimental \
    --disable-dts --disable-faac --disable-faad --disable-nas \
    --disable-mimic --disable-libmms --disable-mpeg2enc --disable-mplex \
    --disable-neon --disable-rtmp --disable-xvid \
    --disable-flite --disable-mpg123 --disable-sbc --disable-opencv \
    --disable-spandsp --disable-voamrwbenc --disable-x265

%make_build

%install
%make_install

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_metainfodir}
cat > $RPM_BUILD_ROOT%{_metainfodir}/gstreamer-bad-free.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-bad-free</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - Extra</name>
  <summary>Multimedia playback for AIFF, DVB, GSM, MIDI, MXF and Opus</summary>
  <description>
    <p>
      This addon includes several additional codecs that are missing
      something - perhaps a good code review, some documentation, a set of
      tests, a real live maintainer, or some actual wide use.
      However, they might be good enough to play your media files.
    </p>
    <p>
      These codecs can be used to encode and decode media files where the
      format is not patent encumbered.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <keywords>
    <keyword>AIFF</keyword>
    <keyword>DVB</keyword>
    <keyword>GSM</keyword>
    <keyword>MIDI</keyword>
    <keyword>MXF</keyword>
    <keyword>Opus</keyword>
  </keywords>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang gst-plugins-bad-%{majorminor}

# unpackaged files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'


%ldconfig_scriptlets

%files -f gst-plugins-bad-%{majorminor}.lang
%license COPYING COPYING.LIB
%doc AUTHORS README REQUIREMENTS

%{_metainfodir}/*.appdata.xml

# presets
%dir %{_datadir}/gstreamer-%{majorminor}/presets/
%{_datadir}/gstreamer-%{majorminor}/presets/GstFreeverb.prs

# opencv data
#{_datadir}/gst-plugins-bad/%{majorminor}/opencv_haarcascades/

%{_libdir}/libgstadaptivedemux-%{majorminor}.so.*
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so.*
%{_libdir}/libgstbadaudio-%{majorminor}.so.*
%{_libdir}/libgstcodecparsers-%{majorminor}.so.*
%{_libdir}/libgstinsertbin-%{majorminor}.so.*
%{_libdir}/libgstisoff-%{majorminor}.so.*
%{_libdir}/libgstmpegts-%{majorminor}.so.*
%{_libdir}/libgstplayer-%{majorminor}.so.*
%{_libdir}/libgstphotography-%{majorminor}.so.*
%{_libdir}/libgstsctp-%{majorminor}.so.*
%{_libdir}/libgsturidownloader-%{majorminor}.so.*
%{_libdir}/libgstwebrtc-%{majorminor}.so.*
%{_libdir}/libgstwayland-%{majorminor}.so.*

%{_libdir}/girepository-1.0/GstInsertBin-1.0.typelib
%{_libdir}/girepository-1.0/GstMpegts-1.0.typelib
%{_libdir}/girepository-1.0/GstPlayer-1.0.typelib
%{_libdir}/girepository-1.0/GstWebRTC-1.0.typelib

# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstaccurip.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstadpcmenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstaiff.so
%{_libdir}/gstreamer-%{majorminor}/libgstasfmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiobuffersplit.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiofxbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiolatency.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiomixmatrix.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiovisualizers.so
%{_libdir}/gstreamer-%{majorminor}/libgstautoconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstbayer.so
%{_libdir}/gstreamer-%{majorminor}/libgstcamerabin.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoloreffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstdashdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaceoverlay.so
%if %{with extras}
%{_libdir}/gstreamer-%{majorminor}/libgstfbdevsink.so
%endif

%{_libdir}/gstreamer-%{majorminor}/libgstfdkaac.so
%{_libdir}/gstreamer-%{majorminor}/libgstfestival.so
%{_libdir}/gstreamer-%{majorminor}/libgstfieldanalysis.so
%{_libdir}/gstreamer-%{majorminor}/libgstfreeverb.so
%{_libdir}/gstreamer-%{majorminor}/libgstfrei0r.so
%{_libdir}/gstreamer-%{majorminor}/libgstgaudieffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstgdp.so
%{_libdir}/gstreamer-%{majorminor}/libgstgeometrictransform.so
%{_libdir}/gstreamer-%{majorminor}/libgstlegacyrawparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstid3tag.so
%{_libdir}/gstreamer-%{majorminor}/libgstipcpipeline.so
%{_libdir}/gstreamer-%{majorminor}/libgstinter.so
%{_libdir}/gstreamer-%{majorminor}/libgstinterlace.so
%{_libdir}/gstreamer-%{majorminor}/libgstivfparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstivtc.so
%{_libdir}/gstreamer-%{majorminor}/libgstjp2kdecimator.so
%{_libdir}/gstreamer-%{majorminor}/libgstjpegformat.so
%{_libdir}/gstreamer-%{majorminor}/libgstmidi.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsdemux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegpsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpegtsmux.so
%{_libdir}/gstreamer-%{majorminor}/libgstmxf.so
%{_libdir}/gstreamer-%{majorminor}/libgstnetsim.so
%{_libdir}/gstreamer-%{majorminor}/libgstpcapparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstpnm.so
%{_libdir}/gstreamer-%{majorminor}/libgstproxy.so
%{_libdir}/gstreamer-%{majorminor}/libgstremovesilence.so
%{_libdir}/gstreamer-%{majorminor}/libgstresindvd.so
%{_libdir}/gstreamer-%{majorminor}/libgstrfbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstrsvg.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtponvif.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdpelem.so
%{_libdir}/gstreamer-%{majorminor}/libgstsegmentclip.so
%{_libdir}/gstreamer-%{majorminor}/libgstshm.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmooth.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmoothstreaming.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeed.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgsttimecode.so
%{_libdir}/gstreamer-%{majorminor}/libgstuvch264.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideofiltersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoframe_audiolevel.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoparsersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideosignal.so
%{_libdir}/gstreamer-%{majorminor}/libgstvmnc.so
%{_libdir}/gstreamer-%{majorminor}/libgstyadif.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4mdec.so

# System (Linux) specific plugins
%{_libdir}/gstreamer-%{majorminor}/libgstdvb.so

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstbluez.so
%{_libdir}/gstreamer-%{majorminor}/libgstbz2.so
%{_libdir}/gstreamer-%{majorminor}/libgstclosedcaption.so
%{_libdir}/gstreamer-%{majorminor}/libgstcolormanagement.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtls.so
%{_libdir}/gstreamer-%{majorminor}/libgsthls.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
%{_libdir}/gstreamer-%{majorminor}/libgstkms.so
%{_libdir}/gstreamer-%{majorminor}/libgstladspa.so
%{_libdir}/gstreamer-%{majorminor}/libgstlv2.so
%{_libdir}/gstreamer-%{majorminor}/libgstopusparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstsndfile.so
%{_libdir}/gstreamer-%{majorminor}/libgstsoundtouch.so
%{_libdir}/gstreamer-%{majorminor}/libgstsrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstttmlsubs.so
#{_libdir}/gstreamer-%{majorminor}/libgstvulkan.so
%{_libdir}/gstreamer-%{majorminor}/libgstwaylandsink.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebp.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebrtc.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebrtcdsp.so

#debugging plugin
%{_libdir}/gstreamer-%{majorminor}/libgstdebugutilsbad.so


%if %{with extras}
%files extras
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstassrender.so
%{_libdir}/gstreamer-%{majorminor}/libgstbs2b.so
%{_libdir}/gstreamer-%{majorminor}/libgstchromaprint.so
%{_libdir}/gstreamer-%{majorminor}/libgstcurl.so
%{_libdir}/gstreamer-%{majorminor}/libgstdecklink.so
%{_libdir}/gstreamer-%{majorminor}/libgstgme.so
%{_libdir}/gstreamer-%{majorminor}/libgstkate.so
%{_libdir}/gstreamer-%{majorminor}/libgstmodplug.so
%{_libdir}/gstreamer-%{majorminor}/libgstofa.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenal.so
#{_libdir}/gstreamer-%{majorminor}/libgstopencv.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenexr.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenjpeg.so
%{_libdir}/gstreamer-%{majorminor}/libgstteletext.so
%{_libdir}/gstreamer-%{majorminor}/libgstvdpau.so
%{_libdir}/gstreamer-%{majorminor}/libgstzbar.so


%files fluidsynth
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstfluidsynthmidi.so

%files wildmidi
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so
%endif


%files devel
%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-plugins-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-libs-%{majorminor}

%{_datadir}/gir-1.0/GstInsertBin-%{majorminor}.gir
%{_datadir}/gir-1.0/GstMpegts-%{majorminor}.gir
%{_datadir}/gir-1.0/GstPlayer-%{majorminor}.gir
%{_datadir}/gir-1.0/GstWebRTC-%{majorminor}.gir

%{_libdir}/libgstadaptivedemux-%{majorminor}.so
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so
%{_libdir}/libgstbadaudio-%{majorminor}.so
%{_libdir}/libgstcodecparsers-%{majorminor}.so
%{_libdir}/libgstinsertbin-%{majorminor}.so
%{_libdir}/libgstisoff-%{majorminor}.so
%{_libdir}/libgstmpegts-%{majorminor}.so
%{_libdir}/libgstplayer-%{majorminor}.so
%{_libdir}/libgstphotography-%{majorminor}.so
%{_libdir}/libgstsctp-%{majorminor}.so
%{_libdir}/libgsturidownloader-%{majorminor}.so
%{_libdir}/libgstwebrtc-%{majorminor}.so
%{_libdir}/libgstwayland-%{majorminor}.so

%{_includedir}/gstreamer-%{majorminor}/gst/audio
%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers
%{_includedir}/gstreamer-%{majorminor}/gst/insertbin
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/photography*
%{_includedir}/gstreamer-%{majorminor}/gst/isoff/
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts
%{_includedir}/gstreamer-%{majorminor}/gst/player
%{_includedir}/gstreamer-%{majorminor}/gst/sctp
%{_includedir}/gstreamer-%{majorminor}/gst/uridownloader
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/

# pkg-config files
%{_libdir}/pkgconfig/gstreamer-bad-audio-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-codecparsers-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-insertbin-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-mpegts-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-player-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-plugins-bad-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-sctp-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-webrtc-%{majorminor}.pc


%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.2-6
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Fri Jun 18 2021 Thomas Crain <thcrain@microsoft.com> - 1.16.2-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Define %%_metainfodir macro if not already present during build
- Conditionalize building of gtk docs
- Remove Redhat-specific version checks
- Turn off extras by default

* Fri May 07 2021 Carl George <carl@george.computer> - 1.16.2-4
- Rebuilt for fluidsynth soname bump rhbz#1958008

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 7 2020 Tom Callaway <spot@fedoraproject.org> - 1.16.2-2
- rebuild for libsrtp2

* Thu Jan 2 2020 Wim Taymans <wtaymans@redhat.com> - 1.16.2-1
- Update to 1.16.2

* Fri Nov 15 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.16.1-3
- rebuild for libdvdread ABI bump

* Fri Oct 04 2019 Kalev Lember <klember@redhat.com> - 1.16.1-2
- Bump gstreamer1-plugins-bad-nonfree obsoletes version

* Tue Sep 24 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.1-1
- Update to 1.16.1

* Mon Sep 23 2019 Kalev Lember <klember@redhat.com> - 1.16.0-4
- Enable AAC support through fdk-aac-free

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.16.0-2
- BR: lilv-devel, enables lv2 plugin
- use %%_metainfodir macro

* Tue Apr 23 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.0-1
- Update to 1.16.0

* Fri Mar 01 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.2-1
- Update to 1.15.2
- The vcdsrc plugin was removed

* Thu Feb 28 2019 Pete Walter <pwalter@fedoraproject.org> - 1.15.1-3
- Update wayland deps

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.1-1
- Update to 1.15.1
- Remove dependency on removed package
- Add sctp and closedcaption plugins

* Wed Oct 03 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.4-1
- Update to 1.14.4

* Tue Sep 18 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.3-1
- Update to 1.14.3

* Wed Aug 15 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.2-2
- Enable LV2 plugin support (#1616070)

* Mon Jul 23 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.2-1
- Update to 1.14.2

* Tue Jul 17 2018 Wim Taymans <wtaymans@redhat.org> - 1.14.1-7
- Only build extras on Fedora
- bluez is not in extras
- vdpau is in extras

* Tue Jul 17 2018 Wim Taymans <wtaymans@redhat.org> - 1.14.1-6
- remove unused liboil BR

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 14 2018 Simone Caronni <negativo17@gmail.com> - 1.14.1-4
- Rebuild for updated libass.

* Fri May 25 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-3
- rebuild (#1581325) to update Provides

* Tue May 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.1-2
- rebuild (file)

* Mon May 21 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-1
- Update to 1.14.1
- Use openjpeg2 instead of openjpeg (#1553079)

* Thu May 10 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.0-2
- Add libnice-devel to get webrtc plugin (#1575244)

* Tue Mar 20 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.0-1
- Update to 1.14.0
- add webrtc gir and typelib

* Wed Mar 14 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.91-1
- Update to 1.13.91

* Mon Mar 5 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.90-1
- Update to 1.13.90
- Add audiolatency
- Schrodinger element was removed

* Tue Feb 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.13.1-2
- drop -gtk subpkg, moved to gst1-plugins-good

* Fri Feb 23 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.13.1-1
- 1.13.1
- use %%ldconfig_scriptlets %%make_build %%make_install
- fix rpath in gst-p-bad-cleanup.sh
- tighten subpkg deps with %%{?_isa}
- -gtk subpkg now empty.  FIXME

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 8 2018 Wim Taymans <wtaymans@redhat.com> - 1.12.4-2
- Rebuild for chromaprint .so change

* Mon Dec 11 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.4-1
- Update to 1.12.4

* Fri Oct 13 2017 Troy Dawson <tdawson@redhat.com> - 1.12.3-3
- Cleanup spec file conditionals

* Sat Sep 30 2017 Jerry James <loganjerry@gmail.com> - 1.12.3-2
- Rebuild for soundtouch 2.0.0

* Tue Sep 19 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.3-1
- Update to 1.12.3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.12.2-4
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Jan Horak <jhorak@redhat.com> - 1.12.2-3
- Added missing buildrequire on EGL

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
- Remove old rawparse plugin
- Add new allocator lib and legacyrawparse

* Fri Feb 24 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.2-1
- Update to 1.11.2
- add audiomixmatrix

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 1.11.1-2
- Rebuild (libwebp)

* Fri Jan 13 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.1-1
- Update to 1.11.1
- Add audiobuffersplit
- Dataurisrc was moved to core
- Add ttmlsubs plugin

* Mon Dec 05 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.2-1
- Update to 1.10.2

* Mon Nov 28 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Thu Nov 03 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Sat Oct 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.90-1
- Update to 1.9.90

* Fri Sep 02 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.2-2
- Rebuild

* Thu Sep 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.2-1
- Update to 1.9.2

* Fri Aug 26 2016 Hans de Goede <hdegoede@redhat.com> - 1.9.1-3
- Rebuild for new wildmidi

* Wed Aug 10 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.1-2
- Merge patches from Kevin Kofler (#1267665)
- Split gtksink into a -gtk subpackage (#1295444)
- Split wildmidi plugin into a -wildmidi subpackage (#1267665)
- BR mesa-libGLES-devel to enable OpenGL ES 2 support in GstGL (#1308290)

* Thu Jul 07 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.1-1
- Update to 1.9.1
- add musepack plugin
- add kmssink plugin

* Thu Jun 09 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Sun May 08 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.1-2
- Rebuild for opencv
- Disable opencv, the version is too new

* Thu Apr 21 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Thu Mar 24 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Wed Mar 16 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.91-1
- Update to 1.7.91
- The opus parse was not moved so we still need opus-devel and we still
  ship a plugin.
- the plugin was renamed to opusparse

* Wed Mar 02 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.90-1
- Update to 1.7.90
- the opus plugin was moved to -base.

* Thu Feb 25 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.2-2
- Rebuild for soundtouch ABI break (#1311323)

* Fri Feb 19 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.2-1
- Update to 1.7.2
- remove rtpbad plugin, it was moved
- add new libraries and netsim plugin

* Tue Feb 16 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.1-5
- add chromaprint plugin

* Thu Feb 04 2016 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.7.1-4
- Append --disable-fatal-warnings to %%configure to prevent
  building from aborting for negligible warnings (Fix F24FTBFS)
- Append --disable-silent-rules to %%configure to make
  building verbose.
- Don't remove buildroot before installing.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 5 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.1-2
- remove rpath from gtksink and mxf
- Fix description line too long

* Tue Jan 5 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.1-1
- Update to 1.7.1
- rename fragmented -> hls
- remove liveadder
- add gstplayer
- add teletextdec and videoframe_audiolevel

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 1.6.2-2
- rebuild (libwebp)

* Tue Dec 15 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.2-1
- Update to 1.6.2

* Mon Nov 9 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.1-2
- Enable more plugins: gtksink, webp, bluez, bs2b, gme, ofa, openal,
  opencv, openjpeg

* Mon Nov 2 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0
- Remove lib64 rpaths from a few more libraries
- Use license macro for COPYING and COPYING.LIB

* Mon Sep 21 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.91-1
- Update to 1.5.91

* Fri Sep 18 2015 Richard Hughes <rhughes@redhat.com> - 1.5.90-3
- Add optional data to AppStream metadata.

* Mon Aug 24 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.90-2
- Enable uvch264

* Wed Aug 19 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.90-1
- Update to 1.5.90

* Thu Jun 25 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.1-1
- Update to 1.5.1
- Drop old patch

* Mon May 04 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.5-5
- Rebuilt for nettle soname bump

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.5-4
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.4.5-3
- Register as an AppStream component.

* Fri Mar 06 2015 David Woodhouse <dwmw2@infradead.org> - 1.4.5-2
- Fix RTP/RTCP muxing (#1199578)

* Tue Feb 03 2015 Wim Taymans <wtaymans@redhat.com> - 1.4.5-1
- Update to 1.4.5

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 1.4.4-2
- rebuild (openexr)

* Fri Nov 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.4-1
- Update to 1.4.4

* Fri Nov 14 2014 Tom Callaway <spot@fedoraproject.org> - 1.4.2-3
- Rebuild for new libsrtp

* Mon Sep 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.2-2
- Remove celt buildreq, the plugin was removed and so is celt-devel

* Mon Sep 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.2-1
- Update to 1.4.2.

* Fri Aug 29 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.1-1
- Update to 1.4.1.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.0-1
- Update to 1.4.0.

* Fri Jul 11 2014 Wim Taymans <wtaymans@redhat.com> - 1.3.91-1
- Update to 1.3.91.
- Remove old libraries

* Tue Jun 17 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.4-1
- Update to 1.2.4.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Hans de Goede <hdegoede@}redhat.com> - 1.2.3-3
- Put the fluidsynth plugin in its own subpackage and make it require
  soundfont2-default (rhbz#1078925)

* Wed Mar 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.3-2
- Bump (libass)

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.

* Thu Feb  6 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-2
- Build the srtp plugin. (#1055669)

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Fri Nov 15 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-4
- Build fluidsynth plugin. (#1024906)

* Thu Nov 14 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-3
- Add BR on gnutls-devel for HLS support. (#1030491)

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-2
- Build ladspa, libkate, and wildmidi plugins.

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.

* Fri Nov  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-3
- Build gobject-introspection support. (#1028156)

* Fri Oct 04 2013 Bastien Nocera <bnocera@redhat.com> 1.2.0-2
- Build the wayland video output plugin

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

* Tue May 07 2013 Colin Walters <walters@verbum.org> - 1.0.7-2
- Move libgstdecklink to its correct place in extras; needed for RHEL

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Sun Mar 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Drop BR on PyXML.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1
- Add frei0r plugin to file list.

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-3
- Enable verbose build

* Wed Sep 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-2
- Build opus plugin.

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Thu Sep 20 2012 Bastien Nocera <bnocera@redhat.com> 0.11.99-2
- The soundtouch-devel BR should be on, even with extras disabled

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.

* Sat Aug 18 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-2
- Fix permission on tarball clean-up script.
- Re-enable soundtouch-devel.
- Add COPYING.LIB to package.
- Use %%global instead of %%define.

* Wed Aug 15 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.

* Fri Jul 20 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec file.
