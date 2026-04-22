# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global         majorminor 1.0
%global         _gobject_introspection  1.31.1

# Only have extras package on fedora
%bcond aom %{defined fedora}
%bcond extras %{defined fedora}
%bcond opencv %{defined fedora}
%bcond openh264 %{defined fedora}
%bcond svtav1 %{defined fedora}
# requires new webrtc-audio-processing-1/-2
%bcond webrtc %[ %{defined fedora} || 0%{?rhel} >= 10 ]
%bcond webrtc1 %[ %{with webrtc} && ! (0%{?fedora} >= 44 || 0%{?rhel} >= 11) ]
# The 1394 stack is not built on s390x
# libldac is not built on s390x, see rhbz#1677491
%ifnarch s390x
%bcond dc1394 %{defined fedora}
%bcond ldac %{defined fedora}
%endif
%ifnarch %{ix86} riscv64 s390x
%bcond onnx %{defined fedora}
%endif
# VPL runtimes (intel-mediasdk/intel-vpl-gpu-rt) are x86_64 only
%ifarch x86_64
%bcond vpl %{defined fedora}
%endif

#global gitrel     140
#global gitcommit  4ca3a22b6b33ad8be4383063e76f79c4d346535d
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

Name:           gstreamer1-plugins-bad-free
Version:        1.26.10
Release: 3%{?dist}
Summary:        GStreamer streaming media framework "bad" plugins

# Automatically converted from old format: LGPLv2+ and LGPLv2 - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+ AND LicenseRef-Callaway-LGPLv2
URL:            http://gstreamer.freedesktop.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/gst-plugins-bad
# cd gst-plugins-bad; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
Source0:        gst-plugins-bad-%{version}.tar.xz
%else
Source:         https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-%{version}.tar.xz
%endif

# https://gitlab.freedesktop.org/gstreamer/gstreamer/-/merge_requests/5622
Patch0:          openh264-add-license-file.patch

BuildRequires:  meson >= 0.48.0
BuildRequires:  gcc-c++
%ifarch x86_64
# work around https://bugzilla.redhat.com/show_bug.cgi?id=2352531
BuildRequires:  libatomic
%endif
BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

BuildRequires:  check
BuildRequires:  gettext-devel
BuildRequires:  libXt-devel
BuildRequires:  gobject-introspection-devel >= %{_gobject_introspection}

BuildRequires:  bzip2-devel
BuildRequires:  exempi-devel
BuildRequires:  glslc
BuildRequires:  gsm-devel
BuildRequires:  pkgconfig(bluez) >= 5.0
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(fdk-aac)
BuildRequires:  pkgconfig(gtk+-wayland-3.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(lc3)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libsrtp2)
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwebpmux)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(orc-0.4)
BuildRequires:  pkgconfig(sbc)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(soundtouch)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(vulkan)
%if %{with aom}
BuildRequires:  pkgconfig(aom)
%endif
%if %{with dc1394}
BuildRequires:  pkgconfig(libdc1394-2)
%endif
%if %{with ldac}
BuildRequires:  pkgconfig(ldacBT-enc)
%endif
%if %{with onnx}
BuildRequires:  pkgconfig(libonnxruntime) >= 1.16.1
%endif
%if %{with opencv}
BuildRequires:  pkgconfig(opencv4)
%endif
%if %{with openh264}
BuildRequires:  pkgconfig(openh264)
%endif
%if %{with svtav1}
BuildRequires:  pkgconfig(SvtAv1Enc)
%endif
%if %{with vpl}
BuildRequires:  pkgconfig(vpl) >= 2.2
%endif
%if %{with webrtc}
%if %{with webrtc1}
BuildRequires:  pkgconfig(webrtc-audio-coding-1)
BuildRequires:  pkgconfig(webrtc-audio-processing-1)
%else
BuildRequires:  pkgconfig(webrtc-audio-processing-2)
%endif
%endif
%if %{with extras}
BuildRequires:  faad2-devel
BuildRequires:  flite-devel
BuildRequires:  game-music-emu-devel
BuildRequires:  ladspa-devel
BuildRequires:  libmpcdec-devel
BuildRequires:  pkgconfig(avtp)
BuildRequires:  pkgconfig(fluidsynth)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbs2b)
BuildRequires:  pkgconfig(libchromaprint)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libdca)
BuildRequires:  pkgconfig(libmodplug)
BuildRequires:  pkgconfig(libopenmpt)
BuildRequires:  pkgconfig(libqrencode)
BuildRequires:  pkgconfig(libssh2)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(lilv-0)
BuildRequires:  pkgconfig(lrdf)
BuildRequires:  pkgconfig(microdns)
BuildRequires:  pkgconfig(mjpegtools) >= 2.0.0
BuildRequires:  pkgconfig(nice)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(OpenEXR)
BuildRequires:  pkgconfig(spandsp) >= 0.0.6
BuildRequires:  pkgconfig(srt)
BuildRequires:  pkgconfig(vo-amrwbenc)
BuildRequires:  pkgconfig(wildmidi)
BuildRequires:  pkgconfig(zbar)
BuildRequires:  pkgconfig(zvbi-0.2)
BuildRequires:  pkgconfig(zxing)
%endif

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

# mpeg2enc, mplex used to be shipped in -freeworld
Conflicts: gstreamer1-plugins-bad-freeworld < 1:1.26.3-3
# Plugins get moved around from time to time
Conflicts: %{name}-extras < %{version}-%{release}

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


%package zbar
Summary:         GStreamer "bad" plugins zbar plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}

%description zbar
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

gstreamer-plugins-bad contains plug-ins that aren't tested well enough,
or the code is not of good enough quality.

This package (%{name}-zbar) contains the zbar
plugin which allows decode bar codes.


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


%package lv2
Summary:         GStreamer "bad" plugins LV2 plugin
Requires:        %{name}%{?_isa} = %{version}-%{release}
Conflicts:       %{name}-extras < 1.26.2-2

%description lv2
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

gstreamer-plugins-bad contains plug-ins that aren't tested well enough,
or the code is not of good enough quality.

This package (%{name}-lv2) contains the lv2 plugin which allows using
LV2 audio plugins (which need to be installed separately).


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


%if %{with opencv}
%package opencv
Summary:         GStreamer "bad" plugins OpenCV plugins
Requires:        %{name}%{?_isa} = %{version}-%{release}
Requires:        opencv-data

%description opencv
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

gstreamer-plugins-bad contains plug-ins that aren't tested well enough,
or the code is not of good enough quality.

This package (%{name}-opencv) contains the OpenCV plugins.
%endif


%if %{with openh264}
%package -n gstreamer1-plugin-openh264
Summary:        GStreamer OpenH264 plugin
# Automatically converted from old format: LGPL-2.0-or-later AND BSD-2-Clause - review is highly recommended.
License:        LGPL-2.0-or-later AND BSD-2-Clause
# Prefer actual openh264 library over the noopenh264 stub
Suggests:       openh264%{_isa}

%description -n gstreamer1-plugin-openh264
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the OpenH264 plugin.
%endif


%package libs
Summary:        Runtime libraries for the GStreamer media framework "bad" plug-ins

%description libs
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the runtime libraries for plugins that
aren't tested well enough, or the code is not of good enough quality.


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
%autosetup -n gst-plugins-bad-%{version} -p3

%build
%meson \
    -D package-name="Fedora GStreamer-plugins-bad package" \
    -D package-origin="http://download.fedoraproject.org" \
    -D gpl=enabled \
    -D doc=disabled \
    -D tests=disabled \
%if %{without aom}
    -D aom=disabled \
%endif
%if %{without dc1394}
    -D dc1394=disabled \
%endif
%if %{without ldac}
    -D ldac=disabled \
%endif
%if %{without onnx}
    -D onnx=disabled \
%endif
%if %{without opencv}
    -D opencv=disabled \
%endif
%if %{without openh264}
    -D openh264=disabled \
%endif
%if %{without svtav1}
    -D svtav1=disabled \
%endif
%if %{without vpl}
    -D msdk=disabled \
    -D qsv=disabled \
%endif
%if %{without webrtc1}
    -D isac=disabled \
%endif
%if %{without webrtc}
    -D webrtcdsp=disabled \
%endif
%if %{without extras}
    -D assrender=disabled \
    -D avtp=disabled \
    -D bs2b=disabled \
    -D chromaprint=disabled \
    -D curl=disabled -D curl-ssh2=disabled \
    -D d3dvideosink=disabled \
    -D decklink=disabled \
    -D directsound=disabled \
    -D dts=disabled \
    -D faad=disabled \
    -D fbdev=disabled \
    -D flite=disabled \
    -D fluidsynth=disabled \
    -D gme=disabled \
    -D ladspa=disabled \
    -D ldac=disabled \
    -D lv2=disabled \
    -D microdns=disabled \
    -D modplug=disabled \
    -D mpeg2enc=disabled \
    -D mplex=disabled \
    -D musepack=disabled \
    -D openal=disabled \
    -D openexr=disabled \
    -D openmpt=disabled \
    -D qroverlay=disabled \
    -D spandsp=disabled \
    -D srt=disabled \
    -D teletext=disabled \
    -D ttml=disabled \
    -D voamrwbenc=disabled \
    -D webrtc=disabled \
    -D wildmidi=disabled \
    -D zbar=disabled \
    -D zxing=disabled \
%endif
    -D aja=disabled \
    -D androidmedia=disabled \
    -D amfcodec=disabled \
    -D cuda-nvmm=disabled \
    -D directfb=disabled \
    -D directshow=disabled \
    -D faac=disabled \
    -D gs=disabled \
    -D iqa=disabled \
    -D lcevcdecoder=disabled \
    -D lcevcencoder=disabled \
    -D libde265=disabled \
    -D magicleap=disabled \
    -D neon=disabled \
    -D nvcomp=disabled \
    -D nvdswrapper=disabled \
    -D openaptx=disabled \
    -D openni2=disabled \
    -D opensles=disabled \
    -D qt6d3d11=disabled \
    -D rtmp=disabled \
    -D svthevcenc=disabled \
    -D svtjpegxs=disabled \
    -D tinyalsa=disabled \
    -D voaacenc=disabled \
    -D wasapi=disabled -D wasapi2=disabled \
    -D wpe=disabled \
    -D x11=disabled \
    -D x265=disabled \
    %{nil}

%meson_build

%install
%meson_install

%if %{with opencv}
# no pkgconfig file or GIR, nothing aside from the plugin uses the library
rm -f $RPM_BUILD_ROOT%{_includedir}/gstreamer-%{majorminor}/gst/opencv/*
rm -f $RPM_BUILD_ROOT%{_libdir}/libgstopencv-%{majorminor}.so
%endif

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_metainfodir}
cat > $RPM_BUILD_ROOT%{_metainfodir}/gstreamer-bad-free.metainfo.xml <<EOF
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

%if %{with openh264}
cat > $RPM_BUILD_ROOT%{_metainfodir}/gstreamer-openh264.metainfo.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2015 Kalev Lember <klember@redhat.com> -->
<component type="codec">
  <id>gstreamer-openh264</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - H.264</name>
  <summary>Multimedia playback for H.264</summary>
  <description>
    <p>
      This addon includes a codec for H.264 playback and encoding.
    </p>
    <p>
      These codecs can be used to encode and decode media files where the
      format is not patent encumbered.
    </p>
    <p>
      A codec decodes audio and video for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF
%endif

%find_lang gst-plugins-bad-%{majorminor}

%ldconfig_scriptlets

%files -f gst-plugins-bad-%{majorminor}.lang
%license COPYING
%doc AUTHORS NEWS README.md README.static-linking RELEASE REQUIREMENTS

%{_metainfodir}/gstreamer-bad-free.metainfo.xml
%{_bindir}/gst-transcoder-%{majorminor}

# presets
%dir %{_datadir}/gstreamer-%{majorminor}/
%dir %{_datadir}/gstreamer-%{majorminor}/presets/
%{_datadir}/gstreamer-%{majorminor}/presets/GstFreeverb.prs
%dir %{_datadir}/gstreamer-%{majorminor}/encoding-profiles/
%dir %{_datadir}/gstreamer-%{majorminor}/encoding-profiles/device/
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/device/dvd.gep
%dir %{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/avi.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/flv.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/mkv.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/mp3.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/mp4.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/oga.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/ogv.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/ts.gep
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/file-extension/webm.gep
%dir %{_datadir}/gstreamer-%{majorminor}/encoding-profiles/online-services/
%{_datadir}/gstreamer-%{majorminor}/encoding-profiles/online-services/youtube.gep

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
%{_libdir}/gstreamer-%{majorminor}/libgstcodecalpha.so
%{_libdir}/gstreamer-%{majorminor}/libgstcodectimestamper.so
%{_libdir}/gstreamer-%{majorminor}/libgstcoloreffects.so
%{_libdir}/gstreamer-%{majorminor}/libgstdash.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdspu.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvbsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvbsuboverlay.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaceoverlay.so
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
%{_libdir}/gstreamer-%{majorminor}/libgstrfbsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstrist.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtmp2.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtpmanagerbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstrtponvif.so
%{_libdir}/gstreamer-%{majorminor}/libgstsdpelem.so
%{_libdir}/gstreamer-%{majorminor}/libgstsegmentclip.so
%{_libdir}/gstreamer-%{majorminor}/libgstsiren.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmooth.so
%{_libdir}/gstreamer-%{majorminor}/libgstsmoothstreaming.so
%{_libdir}/gstreamer-%{majorminor}/libgstspeed.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstswitchbin.so
%{_libdir}/gstreamer-%{majorminor}/libgsttensordecoders.so
%{_libdir}/gstreamer-%{majorminor}/libgsttimecode.so
%{_libdir}/gstreamer-%{majorminor}/libgsttranscode.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideofiltersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoframe_audiolevel.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoparsersbad.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideosignal.so
%{_libdir}/gstreamer-%{majorminor}/libgstvmnc.so
%{_libdir}/gstreamer-%{majorminor}/libgsty4mdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstinsertbin.so
%{_libdir}/gstreamer-%{majorminor}/libgstmse.so
%{_libdir}/gstreamer-%{majorminor}/libgstunixfd.so

# System (Linux) specific plugins
%{_libdir}/gstreamer-%{majorminor}/libgstbluez.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvb.so
%if %{with extras}
%{_libdir}/gstreamer-%{majorminor}/libgstfbdevsink.so
%endif
%if %{with vpl}
%{_libdir}/gstreamer-%{majorminor}/libgstmsdk.so
%{_libdir}/gstreamer-%{majorminor}/libgstqsv.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstshm.so
%{_libdir}/gstreamer-%{majorminor}/libgstuvcgadget.so
%{_libdir}/gstreamer-%{majorminor}/libgstuvch264.so
%{_libdir}/gstreamer-%{majorminor}/libgstv4l2codecs.so

# Plugins with external dependencies

%{_libdir}/gstreamer-%{majorminor}/libgstaes.so
%{_libdir}/gstreamer-%{majorminor}/libgstanalyticsoverlay.so
%{_libdir}/gstreamer-%{majorminor}/libgstbz2.so
%{_libdir}/gstreamer-%{majorminor}/libgstclosedcaption.so
%{_libdir}/gstreamer-%{majorminor}/libgstcodec2json.so
%{_libdir}/gstreamer-%{majorminor}/libgstcolormanagement.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtls.so
%{_libdir}/gstreamer-%{majorminor}/libgstfdkaac.so
%{_libdir}/gstreamer-%{majorminor}/libgsthls.so
%{_libdir}/gstreamer-%{majorminor}/libgstgsm.so
%{_libdir}/gstreamer-%{majorminor}/libgstgtkwayland.so
%{_libdir}/gstreamer-%{majorminor}/libgstkms.so
%{_libdir}/gstreamer-%{majorminor}/libgstlc3.so
%{_libdir}/gstreamer-%{majorminor}/libgstnvcodec.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenjpeg.so
%{_libdir}/gstreamer-%{majorminor}/libgstopusparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstresindvd.so
%{_libdir}/gstreamer-%{majorminor}/libgstrsvg.so
%{_libdir}/gstreamer-%{majorminor}/libgstsbc.so
%{_libdir}/gstreamer-%{majorminor}/libgstsctp.so
%{_libdir}/gstreamer-%{majorminor}/libgstsndfile.so
%{_libdir}/gstreamer-%{majorminor}/libgstsoundtouch.so
%{_libdir}/gstreamer-%{majorminor}/libgstsrtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstva.so
%{_libdir}/gstreamer-%{majorminor}/libgstvulkan.so
%{_libdir}/gstreamer-%{majorminor}/libgstwaylandsink.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebp.so
%if %{with aom}
%{_libdir}/gstreamer-%{majorminor}/libgstaom.so
%endif
%if %{with svtav1}
%{_libdir}/gstreamer-%{majorminor}/libgstsvtav1.so
%endif
%if %{with webrtc1}
%{_libdir}/gstreamer-%{majorminor}/libgstisac.so
%endif
%if %{with webrtc}
%{_libdir}/gstreamer-%{majorminor}/libgstwebrtcdsp.so
%endif
%if %{with extras}
%{_libdir}/gstreamer-%{majorminor}/libgstcurl.so
%{_libdir}/gstreamer-%{majorminor}/libgstfaad.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenal.so
%{_libdir}/gstreamer-%{majorminor}/libgstttmlsubs.so
%{_libdir}/gstreamer-%{majorminor}/libgstwebrtc.so
%endif

#debugging plugin
%{_libdir}/gstreamer-%{majorminor}/libgstdebugutilsbad.so


%if %{with extras}
%files extras
# presets
%{_datadir}/gstreamer-%{majorminor}/presets/GstVoAmrwbEnc.prs

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstassrender.so
%{_libdir}/gstreamer-%{majorminor}/libgstavtp.so
%{_libdir}/gstreamer-%{majorminor}/libgstbs2b.so
%{_libdir}/gstreamer-%{majorminor}/libgstchromaprint.so
%if %{with dc1394}
%{_libdir}/gstreamer-%{majorminor}/libgstdc1394.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstdecklink.so
%{_libdir}/gstreamer-%{majorminor}/libgstdtsdec.so
%{_libdir}/gstreamer-%{majorminor}/libgstflite.so
%{_libdir}/gstreamer-%{majorminor}/libgstgme.so
%{_libdir}/gstreamer-%{majorminor}/libgstladspa.so
%if %{with ldac}
%{_libdir}/gstreamer-%{majorminor}/libgstldac.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstmicrodns.so
%{_libdir}/gstreamer-%{majorminor}/libgstmodplug.so
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2enc.so
%{_libdir}/gstreamer-%{majorminor}/libgstmplex.so
%{_libdir}/gstreamer-%{majorminor}/libgstmusepack.so
%if %{with onnx}
%{_libdir}/gstreamer-%{majorminor}/libgstonnx.so
%endif
%{_libdir}/gstreamer-%{majorminor}/libgstopenexr.so
%{_libdir}/gstreamer-%{majorminor}/libgstopenmpt.so
%{_libdir}/gstreamer-%{majorminor}/libgstqroverlay.so
%{_libdir}/gstreamer-%{majorminor}/libgstspandsp.so
%{_libdir}/gstreamer-%{majorminor}/libgstsrt.so
%{_libdir}/gstreamer-%{majorminor}/libgstteletext.so
%{_libdir}/gstreamer-%{majorminor}/libgstvoamrwbenc.so
%{_libdir}/gstreamer-%{majorminor}/libgstzxing.so

%files lv2
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstlv2.so

%files zbar
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstzbar.so

%files fluidsynth
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstfluidsynthmidi.so

%files wildmidi
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstwildmidi.so
%endif

%if %{with opencv}
%files opencv
# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstopencv.so
%{_libdir}/libgstopencv-%{majorminor}.so.0{,.*}
%endif

%if %{with openh264}
%files -n gstreamer1-plugin-openh264
%license COPYING
%license ext/openh264/LICENSE
%{_metainfodir}/gstreamer-openh264.metainfo.xml
%{_libdir}/gstreamer-1.0/libgstopenh264.so
%endif

%files libs
%license COPYING
%{_libdir}/libgstanalytics-%{majorminor}.so.0{,.*}
%{_libdir}/libgstadaptivedemux-%{majorminor}.so.0{,.*}
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so.0{,.*}
%{_libdir}/libgstbadaudio-%{majorminor}.so.0{,.*}
%{_libdir}/libgstcodecparsers-%{majorminor}.so.0{,.*}
%{_libdir}/libgstcodecs-%{majorminor}.so.0{,.*}
%{_libdir}/libgstcuda-%{majorminor}.so.0{,.*}
%{_libdir}/libgstdxva-%{majorminor}.so.0{,.*}
%{_libdir}/libgstinsertbin-%{majorminor}.so.0{,.*}
%{_libdir}/libgstisoff-%{majorminor}.so.0{,.*}
%{_libdir}/libgstmpegts-%{majorminor}.so.0{,.*}
%{_libdir}/libgstmse-%{majorminor}.so.0{,.*}
%{_libdir}/libgstplay-%{majorminor}.so.0{,.*}
%{_libdir}/libgstplayer-%{majorminor}.so.0{,.*}
%{_libdir}/libgstphotography-%{majorminor}.so.0{,.*}
%{_libdir}/libgstsctp-%{majorminor}.so.0{,.*}
%{_libdir}/libgsttranscoder-%{majorminor}.so.0{,.*}
%{_libdir}/libgsturidownloader-%{majorminor}.so.0{,.*}
%{_libdir}/libgstvulkan-%{majorminor}.so.0{,.*}
%{_libdir}/libgstva-%{majorminor}.so.0{,.*}
%{_libdir}/libgstwebrtc-%{majorminor}.so.0{,.*}
%if %{with extras}
%{_libdir}/libgstwebrtcnice-%{majorminor}.so.0{,.*}
%endif
%{_libdir}/libgstwayland-%{majorminor}.so.0{,.*}

%{_libdir}/girepository-1.0/CudaGst-1.0.typelib
%{_libdir}/girepository-1.0/GstAnalytics-1.0.typelib
%{_libdir}/girepository-1.0/GstBadAudio-1.0.typelib
%{_libdir}/girepository-1.0/GstCodecs-1.0.typelib
%{_libdir}/girepository-1.0/GstCuda-1.0.typelib
%{_libdir}/girepository-1.0/GstDxva-1.0.typelib
%{_libdir}/girepository-1.0/GstInsertBin-1.0.typelib
%{_libdir}/girepository-1.0/GstMpegts-1.0.typelib
%{_libdir}/girepository-1.0/GstMse-1.0.typelib
%{_libdir}/girepository-1.0/GstPlay-1.0.typelib
%{_libdir}/girepository-1.0/GstPlayer-1.0.typelib
%{_libdir}/girepository-1.0/GstTranscoder-1.0.typelib
%{_libdir}/girepository-1.0/GstVa-1.0.typelib
%{_libdir}/girepository-1.0/GstVulkan-1.0.typelib
%{_libdir}/girepository-1.0/GstVulkanWayland-1.0.typelib
%{_libdir}/girepository-1.0/GstWebRTC-1.0.typelib

%files devel
%if 0
%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-plugins-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gst-plugins-bad-libs-%{majorminor}
%endif

%{_datadir}/gir-1.0/CudaGst-%{majorminor}.gir
%{_datadir}/gir-1.0/GstAnalytics-%{majorminor}.gir
%{_datadir}/gir-1.0/GstBadAudio-%{majorminor}.gir
%{_datadir}/gir-1.0/GstCodecs-%{majorminor}.gir
%{_datadir}/gir-1.0/GstCuda-%{majorminor}.gir
%{_datadir}/gir-1.0/GstDxva-%{majorminor}.gir
%{_datadir}/gir-1.0/GstInsertBin-%{majorminor}.gir
%{_datadir}/gir-1.0/GstMpegts-%{majorminor}.gir
%{_datadir}/gir-1.0/GstMse-%{majorminor}.gir
%{_datadir}/gir-1.0/GstPlay-%{majorminor}.gir
%{_datadir}/gir-1.0/GstPlayer-%{majorminor}.gir
%{_datadir}/gir-1.0/GstTranscoder-%{majorminor}.gir
%{_datadir}/gir-1.0/GstVa-%{majorminor}.gir
%{_datadir}/gir-1.0/GstVulkan-%{majorminor}.gir
%{_datadir}/gir-1.0/GstVulkanWayland-%{majorminor}.gir
%{_datadir}/gir-1.0/GstWebRTC-%{majorminor}.gir

%{_libdir}/libgstanalytics-%{majorminor}.so
%{_libdir}/libgstadaptivedemux-%{majorminor}.so
%{_libdir}/libgstbasecamerabinsrc-%{majorminor}.so
%{_libdir}/libgstbadaudio-%{majorminor}.so
%{_libdir}/libgstcuda-%{majorminor}.so
%{_libdir}/libgstcodecparsers-%{majorminor}.so
%{_libdir}/libgstcodecs-%{majorminor}.so
%{_libdir}/libgstdxva-%{majorminor}.so
%{_libdir}/libgstinsertbin-%{majorminor}.so
%{_libdir}/libgstisoff-%{majorminor}.so
%{_libdir}/libgstmpegts-%{majorminor}.so
%{_libdir}/libgstmse-%{majorminor}.so
%{_libdir}/libgstplay-%{majorminor}.so
%{_libdir}/libgstplayer-%{majorminor}.so
%{_libdir}/libgstphotography-%{majorminor}.so
%{_libdir}/libgstsctp-%{majorminor}.so
%{_libdir}/libgsttranscoder-%{majorminor}.so
%{_libdir}/libgsturidownloader-%{majorminor}.so
%{_libdir}/libgstvulkan-%{majorminor}.so
%{_libdir}/libgstva-%{majorminor}.so
%{_libdir}/libgstwebrtc-%{majorminor}.so
%if %{with extras}
%{_libdir}/libgstwebrtcnice-%{majorminor}.so
%endif
%{_libdir}/libgstwayland-%{majorminor}.so

%{_includedir}/gstreamer-%{majorminor}/gst/audio
%{_includedir}/gstreamer-%{majorminor}/gst/analytics
%{_includedir}/gstreamer-%{majorminor}/gst/basecamerabinsrc
%{_includedir}/gstreamer-%{majorminor}/gst/codecparsers
%{_includedir}/gstreamer-%{majorminor}/gst/cuda/
%{_includedir}/gstreamer-%{majorminor}/gst/insertbin
%{_includedir}/gstreamer-%{majorminor}/gst/interfaces/photography*
%{_includedir}/gstreamer-%{majorminor}/gst/isoff/
%{_includedir}/gstreamer-%{majorminor}/gst/mpegts
%{_includedir}/gstreamer-%{majorminor}/gst/mse/
%{_includedir}/gstreamer-%{majorminor}/gst/play
%{_includedir}/gstreamer-%{majorminor}/gst/player
%{_includedir}/gstreamer-%{majorminor}/gst/sctp
%{_includedir}/gstreamer-%{majorminor}/gst/transcoder
%{_includedir}/gstreamer-%{majorminor}/gst/uridownloader
%{_includedir}/gstreamer-%{majorminor}/gst/va/
%{_includedir}/gstreamer-%{majorminor}/gst/vulkan/
%{_includedir}/gstreamer-%{majorminor}/gst/wayland/
%{_includedir}/gstreamer-%{majorminor}/gst/webrtc/

# pkg-config files
%{_libdir}/pkgconfig/gstreamer-analytics-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-bad-audio-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-cuda-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-codecparsers-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-insertbin-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-mpegts-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-mse-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-photography-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-play-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-player-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-plugins-bad-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-sctp-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-transcoder-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-va-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-vulkan-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-vulkan-wayland-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-wayland-%{majorminor}.pc
%{_libdir}/pkgconfig/gstreamer-webrtc-%{majorminor}.pc
%if %{with extras}
%{_libdir}/pkgconfig/gstreamer-webrtc-nice-%{majorminor}.pc
%endif


%changelog
* Mon Feb 16 2026 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.26.10-2
- Disable onnx on riscv64 port

* Tue Jan 06 2026 Gwyn Ciesla <gwync@protonmail.com> - 1.26.10-1
- 1.26.10

* Wed Dec 10 2025 Nicolas Chauvet <kwizart@gmail.com> - 1.26.9-2
- Rebuilt for OpenCV-4.12

* Wed Dec 03 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.9-1
- 1.26.9

* Wed Nov 19 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.26.8-3
- Disable isac on F44+/EL11+

* Wed Nov 19 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.26.8-2
- Use webrtc-audio-processing-2 with Fedora 44+ and RHEL 11+

* Wed Nov 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.8-1
- 1.26.8

* Tue Oct 14 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.7-1
- 1.26.7

* Thu Oct 02 2025 Robert-André Mauchin <zebob.m@gmail.com> - 1.26.6-2
- Rebuild for svt-av1 soname bump

* Mon Sep 15 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.6-1
- 1.26.6

* Wed Aug 13 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.26.5-4
- Move sbc to main package

* Wed Aug 13 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.26.5-3
- Enable msdk plugin on x86_64
- Enable mpeg2enc, mplex, onnx, sbc plugins in extras

* Tue Aug 12 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.26.5-2
- Enable isac plugin

* Fri Aug 08 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.5-1
- 1.26.5

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 27 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.3-1
- 1.26.3

* Sun Jun 15 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 1.26.2-2
- Move aom, curl, openal, openjpeg to main package
- Move lv2 to separate subpackage (rhbz#1731750)
- Enable dvdspu, faad, qsv (x86_64 only)
- Enable dc1394 and zxing in extras subpackage

* Fri May 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.2-1
- 1.26.2

* Fri Apr 25 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.1-1
- 1.26.1

* Fri Mar 14 2025 Fabio Valentini <decathorpe@gmail.com> - 1.26.0-2
- Rebuild for noopenh264 2.6.0

* Wed Mar 12 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.26.0-1
- 1.26.0

* Tue Mar 04 2025 Wim Taymans <wtaymans@redhat.com> - 1.24.11-5
- Rebuild for openh264 2.6.0

* Wed Feb 05 2025 Robert-André Mauchin <zebob.m@gmail.com> - 1.24.11-4
- Rebuilt for aom 3.11.0

* Tue Feb 04 2025 Sérgio Basto <sergio@serjux.com> - 1.24.11-3
- Rebuild for opencv-4.11.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.24.11-1
- 1.24.11

* Wed Dec 04 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.10-1
- 1.24.10

* Thu Oct 31 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.9-1
- 1.24.9

* Thu Sep 19 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.8-1
- 1.24.8

* Fri Sep 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.24.7-3
- Disable SVT-AV1 on RHEL

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.24.7-2
- convert license to SPDX

* Wed Aug 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.7-1
- 1.24.7

* Mon Jul 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.6-1
- 1.24.6

* Thu Jul 25 2024 Sérgio Basto <sergio@serjux.com> - 1.24.5-3
- Rebuild for opencv 4.10.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 21 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.5-1
- 1.24.5

* Thu May 30 2024 Robert-André Mauchin <zebob.m@gmail.com> - 1.24.4-2
- Rebuild for svt-av1 2.1.0

* Wed May 29 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.4-1
- 1.24.4

* Tue Apr 30 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.3-1
- 1.24.3

* Mon Apr 22 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.24.0-3
- openexr rebuild

* Wed Mar 13 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.24.0-2
- Re-enable webrtcdsp for f40+ and ELN

* Tue Mar 05 2024 Wim Taymans <wtaymans@redhat.com> - 1.24.0-1
- Update to 1.24.0

* Thu Feb 08 2024 Kalev Lember <klember@redhat.com> - 1.22.9-3
- Add gstreamer1-plugin-openh264 subpackage with the openh264 plugin

* Tue Feb 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.22.9-2
- Rebuilt for opencv-4.9.0

* Thu Jan 25 2024 Gwyn Ciesla <gwync@protonmail.com> - 1.22.9-1
- 1.22.9

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.22.8-3
- Backport of "va: fixes for Mesa driver"
- Resolves: rhbz#2256693

* Wed Dec 20 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.22.8-2
- Enable dvbsuboverlay and siren plugins
- Enable avtp, dtsdec, and flite plugins in extras

* Mon Dec 18 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.22.8-1
- 1.22.8

* Tue Nov 21 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.22.7-2
- Move gstva from extras into main package

* Tue Nov 14 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.22.7-1
- 1.22.7

* Fri Sep 22 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.22.5-2
- Separate libs subpackage
- Enable opencv as separate subpackage

* Fri Jul 21 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.5-1
- Update to 1.22.5

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 25 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.3-1
- Update to 1.22.3

* Sun May 21 2023 Sérgio Basto <sergio@serjux.com> - 1.22.2-4
- Remove obsolete of plugins-bad-freeworld to workaround a dnf bug
  https://bugzilla.redhat.com/show_bug.cgi?id=1867376#c9

* Thu Apr 27 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.22.2-3
- Fix migration of musepack and voamrwbenc to -bad-free-extras

* Mon Apr 24 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.22.2-2
- Enable musepack and voamrwbenc in extras

* Thu Apr 13 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.2-1
- Update to 1.22.2

* Mon Mar 13 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.1-1
- Update to 1.22.1

* Tue Jan 24 2023 Wim Taymans <wtaymans@redhat.com> - 1.22.0-1
- Update to 1.22.0

* Fri Jan 20 2023 Wim Taymans <wtaymans@redhat.com> - 1.21.90-1
- Update to 1.21.90

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Wim Taymans <wtaymans@redhat.com> - 1.20.5-1
- Update to 1.20.5
- Remove unwanted crypto dependencies.

* Mon Nov 14 2022 Stephen Gallagher <sgallagh@redhat.com> - 1.20.4-2
- Drop vdpau configure option
- The libgstva plugin is now excluded from file listings when disabled
- Resolves: rhbz#2141093

* Thu Oct 13 2022 Wim Taymans <wtaymans@redhat.com> - 1.20.4-1
- Update to 1.20.4

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Wim Taymans <wtaymans@redhat.com> - 1.20.3-1
- Update to 1.20.3

* Wed Jun 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.20.0-4
- Rebuilt for new aom

* Sat Jun 18 2022 Scott Talbert <swt@techie.net> - 1.20.0-3
- Rebuild for srt-1.5.0 (#2097636, #2098341)

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 1.20.0-2
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Fri Feb 4 2022 Wim Taymans <wtaymans@redhat.com> - 1.20.0-1
- Update to 1.20.0

* Thu Feb 03 2022 Scott Talbert <swt@techie.net> - 1.19.3-6
- Enable rtmp2 plugin (#1915517)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Scott Talbert <swt@techie.net> - 1.19.3-4
- Fix GstPlayer with GstPlayerVideoOverlayVideoRenderer (#2035937)

* Mon Jan 10 2022 Scott Talbert <swt@techie.net> - 1.19.3-3
- Add BR for wayland-protocols-devel to fix another FTBFS

* Mon Nov 22 2021 Scott Talbert <swt@techie.net> - 1.19.3-2
- Fix FTBFS with meson 0.60.1 (#2025782)

* Thu Nov 11 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.3-1
- Update to 1.19.3
- Remove ofa plugin, is was removed

* Thu Sep 23 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.2-1
- Update to 1.19.2

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.19.1-8
- Rebuilt with OpenSSL 3.0.0

* Sat Aug 21 2021 Richard Shaw <hobbes1069@gmail.com> - 1.19.1-7
- Rebuild for OpenEXR/Imath 3.1.

* Tue Aug 10 2021 Richard Shaw <hobbes1069@gmail.com> - 1.19.1-6
- Rebuild for OpenEXR 3.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.1-4
- Enable sctp plugin

* Mon Jun 21 2021 Gwyn Ciesla <gwync@protonmail.com> - 1.19.1-3
- Fluidsynth rebuild.

* Sun Jun 13 2021 Robert-André Mauchin <zebob.m@gmail.com> - 1.19.1-2
- Rebuilt for aom v3.1.1

* Thu Jun 03 2021 Wim Taymans <wtaymans@redhat.com> - 1.19.1-1
- Update to 1.19.1

* Wed May 26 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.18.4-3
- Rebuilt for srt

* Tue Apr 6 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.4-2
- Add patch to fix multilib issues with vulkan (#1915341)

* Tue Mar 16 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.4-1
- Update to 1.18.4

* Tue Mar 09 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.2-9
- Fix typo when disabling microdns

* Thu Feb 25 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.2-8
- Move ladspa, microdns, openmpt, srt and zvbi to extras

* Mon Feb 08 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.2-7
- Rebuild for updated libmicrodns

* Wed Jan 20 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.2-6
- Move libaom to extras
- Remove unused musepack buildreq

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Leigh Scott <leigh123linux@gmail.com> - 1.18.2-4
- Rebuild for new libmicrodns .so version

* Tue Jan 12 2021 Wim Taymans <wtaymans@redhat.com> - 1.18.2-3
- Move libnice and webrtc to extras

* Fri Jan 01 2021 Richard Shaw <hobbes1069@gmail.com> - 1.18.2-2
- Rebuild for OpenEXR 2.5.3.

* Thu Dec 10 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.2-1
- Update to 1.18.2

* Fri Oct 30 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.1-1
- Update to 1.18.1
- Remove COPYING.LIB

* Mon Oct 19 2020 Troy Dawson <tdawson@redhat.com> - 1.18.0-5
- Do not run va tests when va is disabled

* Sat Oct 17 2020 Dominik Mierzejewski <rpm@greysector.net> - 1.18.0-4
- rebuild for libdvdread-6.1 ABI bump

* Tue Sep 22 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.18.0-3
- Obsolete/Provide gst-transcoder

* Thu Sep 10 2020 Adam Williamson <awilliam@redhat.com> - 1.18.0-2
- Disable opencv again (pulls in huge number of deps)

* Tue Sep 8 2020 Wim Taymans <wtaymans@redhat.com> - 1.18.0-1
- Update to 1.18.0
- Enable opencv

* Fri Aug 21 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.90-1
- Update to 1.17.90
- Remove obsolete -bad-transcoder .pc file
- Add vulkan wayland

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Robert-André Mauchin <zebob.m@gmail.com> - 1.17.2-2
- Rebuilt for aom 2.0.0

* Mon Jul 6 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.2-1
- Update to 1.17.2
- Add new libva plugin
- Add new pkgconfig files

* Mon Jun 22 2020 Wim Taymans <wtaymans@redhat.com> - 1.17.1-1
- Update to 1.17.1
- Add sources
- Disable wpe for now

* Fri Mar 20 2020 Debarshi Ray <rishi@fedoraproject.org> - 1.16.2-4
- Enable the spandsp plugin

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
