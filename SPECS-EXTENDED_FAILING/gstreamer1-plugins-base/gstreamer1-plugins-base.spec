Vendor:         Microsoft Corporation
Distribution:   Mariner
%global         majorminor      1.0

#global gitrel     140
#global gitcommit  c52adc8fcccf691754ab762e667fffb5465c3354
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

Name:           gstreamer1-plugins-base
Version:        1.16.2
Release:        6%{?dist}
Summary:        GStreamer streaming media framework base plugins

License:        GPLv2+
URL:            http://gstreamer.freedesktop.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/gst-plugins-base
# cd gst-plugins-base; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
Source0:        gst-plugins-base-%{version}.tar.xz
%else
Source0:        http://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-%{version}.tar.xz
%endif
Patch0:         0001-missing-plugins-Remove-the-mpegaudioversion-field.patch

BuildRequires:  gcc-c++
BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gobject-introspection-devel >= 1.31.1
BuildRequires:  iso-codes-devel

BuildRequires:  alsa-lib-devel
BuildRequires:  libogg-devel >= 1.0
BuildRequires:  libtheora-devel >= 1.1
BuildRequires:  libvisual-devel
BuildRequires:  libvorbis-devel >= 1.0
BuildRequires:  libXv-devel
BuildRequires:  orc-devel >= 0.4.18
BuildRequires:  pango-devel
BuildRequires:  pkgconfig
BuildRequires:  opus-devel
# for autogen.sh
BuildRequires:  automake gettext-devel libtool
BuildRequires:  chrpath
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  wayland-devel
BuildRequires:  egl-wayland-devel
BuildRequires:  graphene-devel
# pkgconfig-style deps specifically searched-for by autotools/configure
BuildRequires: pkgconfig(wayland-client) >= 1.0
BuildRequires: pkgconfig(wayland-cursor) >= 1.0
BuildRequires: pkgconfig(wayland-egl) >= 9.0
BuildRequires: pkgconfig(wayland-protocols) >= 1.15

# documentation
BuildRequires:  libxslt-devel
BuildRequires:  docbook-style-xsl
BuildRequires:  gtk-doc >= 1.3

Requires:       iso-codes

#  libgstgl moved here
Conflicts: gstreamer1-plugins-bad-free < 1.13


%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains a set of well-maintained base plug-ins.


%package tools
Summary:        Tools for GStreamer streaming media framework base plugins
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description tools
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plug-ins.

This package contains the command-line tools for the base plugins.
These include:

* gst-discoverer


%package devel
Summary:        GStreamer Base Plugins Development files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files
for developing applications that use %{name}.


%package devel-docs
Summary:        Developer documentation for GStreamer Base plugins library
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description devel-docs
This %{name}-devel-docs package contains developer documentation
for the GStreamer Base Plugins library.


%prep
%setup -q -n gst-plugins-base-%{version}
%patch0 -p1

%build
cat /etc/xml/catalog
ls /etc/xml/catalog
export XML_CATALOG_FILES=/etc/xml/catalog
# die rpath (method of modifying libtool fails here)
NOCONFIGURE=1 \
./autogen.sh

%configure \
  --with-package-name='Fedora GStreamer-plugins-base package' \
  --with-package-origin='http://download.fedoraproject.org' \
  --enable-experimental \
  --disable-cdparanoia \
  --disable-fatal-warnings \
  --disable-silent-rules \
  --disable-gtk-doc \
  --enable-orc \
  PYTHON=%{python3}

%make_build V=1


%install
%make_install

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/gstreamer-base.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-base</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - Base</name>
  <summary>Multimedia playback for Ogg, Theora and Vorbis</summary>
  <description>
    <p>
      This addon includes system codecs that are essential for the running system.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <keywords>
    <keyword>Ogg</keyword>
    <keyword>Theora</keyword>
    <keyword>Vorbis</keyword>
  </keywords>
  <compulsory_for_desktop>GNOME</compulsory_for_desktop>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang gst-plugins-base-%{majorminor}

# Clean out files that should not be part of the rpm.
find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'
#rm -f $RPM_BUILD_ROOT%{_bindir}/gst-visualise*
#rm -f $RPM_BUILD_ROOT%{_mandir}/man1/gst-visualise*

# Using a more robus approach above, avoids manual error-prone lists like below --rex
%if 0
# Remove rpath.
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideotestsrc.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstpango.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvorbis.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstogg.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudiorate.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstalsa.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstpbutils-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvolume.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstaudio-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstencoding.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstrawparse.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideoscale.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstplayback.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstcdparanoia.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libgstriff-1.0.so.*
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgsttheora.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgsttypefindfunctions.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudioresample.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstlibvisual.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideoconvert.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstvideorate.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstaudiotestsrc.so
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-device-monitor-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-discoverer-1.0
chrpath --delete $RPM_BUILD_ROOT%{_bindir}/gst-play-1.0
%endif


%ldconfig_scriptlets

%files -f gst-plugins-base-%{majorminor}.lang
%license COPYING
%doc AUTHORS README REQUIREMENTS
%{_datadir}/appdata/*.appdata.xml
%{_libdir}/libgstallocators-%{majorminor}.so.*
%{_libdir}/libgstaudio-%{majorminor}.so.*
%{_libdir}/libgstfft-%{majorminor}.so.*
%{_libdir}/libgstriff-%{majorminor}.so.*
%{_libdir}/libgsttag-%{majorminor}.so.*
%{_libdir}/libgstrtp-%{majorminor}.so.*
%{_libdir}/libgstvideo-%{majorminor}.so.*
%{_libdir}/libgstpbutils-%{majorminor}.so.*
%{_libdir}/libgstrtsp-%{majorminor}.so.*
%{_libdir}/libgstsdp-%{majorminor}.so.*
%{_libdir}/libgstapp-%{majorminor}.so.*
%{_libdir}/libgstgl-%{majorminor}.so.*

# gobject-introspection files
%{_libdir}/girepository-1.0/GstAllocators-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstApp-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstAudio-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstGL-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstPbutils-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstRtp-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstRtsp-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstSdp-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstTag-%{majorminor}.typelib
%{_libdir}/girepository-1.0/GstVideo-%{majorminor}.typelib

# base plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstadder.so
%{_libdir}/gstreamer-%{majorminor}/libgstapp.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiomixer.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudioresample.so
%{_libdir}/gstreamer-%{majorminor}/libgstaudiotestsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstcompositor.so
%{_libdir}/gstreamer-%{majorminor}/libgstencoding.so
%{_libdir}/gstreamer-%{majorminor}/libgstgio.so
%{_libdir}/gstreamer-%{majorminor}/libgstoverlaycomposition.so
%{_libdir}/gstreamer-%{majorminor}/libgstplayback.so
%{_libdir}/gstreamer-%{majorminor}/libgstpbtypes.so
%{_libdir}/gstreamer-%{majorminor}/libgstrawparse.so
%{_libdir}/gstreamer-%{majorminor}/libgstsubparse.so
%{_libdir}/gstreamer-%{majorminor}/libgsttcp.so
%{_libdir}/gstreamer-%{majorminor}/libgsttypefindfunctions.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoconvert.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideorate.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideoscale.so
%{_libdir}/gstreamer-%{majorminor}/libgstvideotestsrc.so
%{_libdir}/gstreamer-%{majorminor}/libgstvolume.so

# base plugins with dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstalsa.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdparanoia.so
%{_libdir}/gstreamer-%{majorminor}/libgstopengl.so
%{_libdir}/gstreamer-%{majorminor}/libgstlibvisual.so
%{_libdir}/gstreamer-%{majorminor}/libgstogg.so
%{_libdir}/gstreamer-%{majorminor}/libgstopus.so
%{_libdir}/gstreamer-%{majorminor}/libgstpango.so
%{_libdir}/gstreamer-%{majorminor}/libgsttheora.so
%{_libdir}/gstreamer-%{majorminor}/libgstvorbis.so
%{_libdir}/gstreamer-%{majorminor}/libgstximagesink.so
%{_libdir}/gstreamer-%{majorminor}/libgstxvimagesink.so


%files tools
%{_bindir}/gst-discoverer-%{majorminor}
%{_bindir}/gst-play-%{majorminor}
%{_bindir}/gst-device-monitor-%{majorminor}
%{_mandir}/man1/gst-discoverer-*.gz
%{_mandir}/man1/gst-play-*.gz
%{_mandir}/man1/gst-device-monitor-*.gz


%files devel
%dir %{_includedir}/gstreamer-%{majorminor}/gst/allocators
%{_includedir}/gstreamer-%{majorminor}/gst/allocators/allocators.h
%{_includedir}/gstreamer-%{majorminor}/gst/allocators/allocators-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/allocators/gstdmabuf.h
%{_includedir}/gstreamer-%{majorminor}/gst/allocators/gstfdmemory.h
%{_includedir}/gstreamer-%{majorminor}/gst/allocators/gstphysmemory.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/app
%{_includedir}/gstreamer-%{majorminor}/gst/app/app.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/app-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/app-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/gstappsink.h
%{_includedir}/gstreamer-%{majorminor}/gst/app/gstappsrc.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/audio
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-buffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-channels.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-channel-mixer.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-converter.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-format.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-info.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-quantize.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-resampler.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/audio-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioaggregator.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiobasesink.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiobasesrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiocdsrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioclock.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiodecoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioencoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiofilter.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioiec61937.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiometa.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudioringbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiosink.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiosrc.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/gstaudiostreamalign.h
%{_includedir}/gstreamer-%{majorminor}/gst/audio/streamvolume.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/fft
%{_includedir}/gstreamer-%{majorminor}/gst/fft/fft.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/fft-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstfft.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstfftf32.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstfftf64.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstffts16.h
%{_includedir}/gstreamer-%{majorminor}/gst/fft/gstffts32.h
%{_includedir}/gstreamer-%{majorminor}/gst/gl/
%{_libdir}/gstreamer-%{majorminor}/include/gst/gl/
%dir %{_includedir}/gstreamer-%{majorminor}/gst/pbutils
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/codec-utils.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/descriptions.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/encoding-profile.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/encoding-target.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/gstaudiovisualizer.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/gstdiscoverer.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/gstpluginsbaseversion.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/install-plugins.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/missing-plugins.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/pbutils-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/pbutils.h
%{_includedir}/gstreamer-%{majorminor}/gst/pbutils/pbutils-prelude.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/riff
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-ids.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-media.h
%{_includedir}/gstreamer-%{majorminor}/gst/riff/riff-read.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/rtp
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtcpbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbaseaudiopayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbasedepayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbasepayload.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpbuffer.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpdefs.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtp-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtphdrext.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtpmeta.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/gstrtppayloads.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/rtp.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtp/rtp-prelude.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/rtsp
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsp.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsp-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspconnection.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspdefs.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspextension.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspmessage.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsprange.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtsptransport.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/gstrtspurl.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/rtsp.h
%{_includedir}/gstreamer-%{majorminor}/gst/rtsp/rtsp-prelude.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/sdp
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/gstsdp.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/gstsdpmessage.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/gstmikey.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/sdp.h
%{_includedir}/gstreamer-%{majorminor}/gst/sdp/sdp-prelude.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/tag
%{_includedir}/gstreamer-%{majorminor}/gst/tag/gsttagdemux.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/gsttagmux.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/tag.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/tag-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/tag-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/tag/xmpwriter.h
%dir %{_includedir}/gstreamer-%{majorminor}/gst/video
%{_includedir}/gstreamer-%{majorminor}/gst/video/colorbalance.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/colorbalancechannel.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoaffinetransformationmeta.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoaggregator.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideodecoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoencoder.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideofilter.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideometa.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideopool.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideosink.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideotimecode.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/gstvideoutils.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/navigation.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-anc.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-blend.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-overlay-composition.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-chroma.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-color.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-converter.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-dither.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-enumtypes.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-event.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-format.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-frame.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-info.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-multiview.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-resampler.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-scaler.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-tile.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/video-prelude.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/videodirection.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/videoorientation.h
%{_includedir}/gstreamer-%{majorminor}/gst/video/videooverlay.h

%{_libdir}/libgstallocators-%{majorminor}.so
%{_libdir}/libgstaudio-%{majorminor}.so
%{_libdir}/libgstriff-%{majorminor}.so
%{_libdir}/libgstrtp-%{majorminor}.so
%{_libdir}/libgsttag-%{majorminor}.so
%{_libdir}/libgstvideo-%{majorminor}.so
%{_libdir}/libgstpbutils-%{majorminor}.so
%{_libdir}/libgstrtsp-%{majorminor}.so
%{_libdir}/libgstsdp-%{majorminor}.so
%{_libdir}/libgstfft-%{majorminor}.so
%{_libdir}/libgstapp-%{majorminor}.so
%{_libdir}/libgstgl-%{majorminor}.so

%dir %{_datadir}/gst-plugins-base/%{majorminor}/
%{_datadir}/gst-plugins-base/%{majorminor}/license-translations.dict

%{_datadir}/gir-1.0/GstAllocators-%{majorminor}.gir
%{_datadir}/gir-1.0/GstApp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstAudio-%{majorminor}.gir
%{_datadir}/gir-1.0/GstGL-%{majorminor}.gir
%{_datadir}/gir-1.0/GstPbutils-%{majorminor}.gir
%{_datadir}/gir-1.0/GstRtp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstRtsp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstSdp-%{majorminor}.gir
%{_datadir}/gir-1.0/GstTag-%{majorminor}.gir
%{_datadir}/gir-1.0/GstVideo-%{majorminor}.gir

# pkg-config files
%{_libdir}/pkgconfig/*.pc


%files devel-docs
%doc %{_datadir}/gtk-doc/html/gst-plugins-base-libs-%{majorminor}
%doc %{_datadir}/gtk-doc/html/gst-plugins-base-plugins-%{majorminor}


%changelog
* Tue Feb 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.2-6
- Removing BR on 'cdparanoia'.
- License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.16.2-5
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jun 16 2021 Thomas Crain <thcrain@microsoft.com> - 1.16.2-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn off gtk-doc to workaround bug in docbook-xsl-styles

* Thu Apr 16 2020 Wim Taymans <wtaymans@redhat.com> - 1.16.2-3
- Add BR graphene-devel to build gltransform
- Fixes rhbz#1822387

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 2 2020 Wim Taymans <wtaymans@redhat.com> - 1.16.2-1
- Update to 1.16.2

* Tue Sep 24 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.1-1
- Update to 1.16.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 23 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.0-1
- Update to 1.16.0

* Thu Mar 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.15.2-2
- update wayland-related build deps, --enable-gtk-doc

* Thu Mar 07 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.15.2-1
- %%build: --disable-gtk-doc to workaround FTBFS (hopefully temporary)

* Fri Mar 01 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.2-1
- Update to 1.15.2
- Add egl-wayland dep

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.2-1
- rebuild for dependencies

* Fri Jan 25 2019 Wim Taymans <wtaymans@redhat.com> - 1.15.1-1
- Update to 1.15.1

* Fri Jan 11 2019 Bastien Nocera <bnocera@redhat.com> - 1.14.4-2
+ gstreamer1-plugins-base-1.14.4-2
- Fix thumbnail colours for 10-bit MPEG-4 files

* Wed Oct 03 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.4-1
- Update to 1.14.4

* Tue Sep 18 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.3-1
- Update to 1.14.3

* Mon Jul 23 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.2-1
- Update to 1.14.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-3
- rebuild (#1581325)

* Tue May 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.1-2
- rebuild (file)

* Mon May 21 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.1-1
- Update to 1.14.1
- Remove obsolete patches

* Mon Mar 26 2018 Tomas Popela <tpopela@redhat.com> - 1.14.0-2
- Enable Wayland support (previously disabled due to missing wayland-devel
  as a BR - before it was probably brought in by something else).

* Tue Mar 20 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.0-1
- Update to 1.14.0

* Wed Mar 14 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.91-1
- Update to 1.13.91
- Add new prelude .h files

* Mon Mar 05 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.90-1
- Update to 1.13.90

* Sat Feb 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.13.1-2
- tigten subpkg deps
- fix rpaths
- update %%files
- use %%ldconfig_scriptlets %%make_build %%make_install
- %%build: --disable-fatal-warnings --disable-silent-rules
- Conflicts: gstreamer1-plugins-bad-free < 1.13

* Thu Feb 22 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.1-1
- Update to 1.13.1
- Add patch to fix aliasing compilation error
- Add GL buildrequires

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.4-1
- Update to 1.12.4

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
- Add new headers

* Tue Apr 11 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.90-1
- Update to 1.11.90
- Add new plugins

* Fri Feb 24 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.2-1
- Update to 1.11.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Wim Taymans <wtaymans@redhat.com> - 1.11.1-1
- Update to 1.11.1

* Mon Dec 05 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.2-1
- Update to 1.10.2

* Mon Nov 28 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.1-1
- Update to 1.10.1

* Thu Nov 3 2016 Wim Taymans <wtaymans@redhat.com> - 1.10.0-1
- Update to 1.10.0

* Fri Sep 30 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.90-1
- Update to 1.9.90

* Thu Sep 01 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.2-1
- Update to 1.9.2
- drop upstreamed patch
- add new files

* Thu Jul 07 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.1-2
- Fix build on big-endian

* Thu Jul 07 2016 Wim Taymans <wtaymans@redhat.com> - 1.9.1-1
- Update to 1.9.1
- add audio-resampler.h

* Thu Jun 09 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Thu Apr 21 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Thu Mar 24 2016 Wim Taymans <wtaymans@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Wed Mar 16 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.91-1
- Update to 1.7.91

* Thu Mar 03 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.90-2
- Add opus that was moved from -bad-free

* Wed Mar 02 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.90-1
- Update to 1.7.90

* Fri Feb 19 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.2-1
- Update to 1.7.2
- fix for renamed header

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 4 2016 Wim Taymans <wtaymans@redhat.com> - 1.7.1-1
- Update to 1.7.1
- Add new files

* Tue Dec 15 2015 Wim Taymans <wtaymans@redhat.com> - 1.6.2-1
- Update to 1.6.2

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

* Thu Jun 25 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.2-1
- Update to 1.5.2
- Don't produce gir and typlib for GstRiff
- Add multiview headers

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Wim Taymans <wtaymans@redhat.com> - 1.5.1-1
- Update to 1.5.1
- add missing headers

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.4.5-3
- Register as an AppStream component.

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.5-2
- Backport new missing plugins API

* Wed Jan 28 2015 Bastien Nocera <bnocera@redhat.com> 1.4.5-1
- Update to 1.4.5

* Fri Nov 14 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.4-1
- Update to 1.4.4

* Mon Sep 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.2-1
- Update to 1.4.2.

* Fri Aug 29 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.1-1
- Update to 1.4.1.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.4.0-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 22 2014 Wim Taymans <wtaymans@redhat.com> - 1.4.0-1
- Update to 1.4.0.

* Fri Jul 11 2014 Wim Taymans <wtaymans@redhat.com> - 1.3.91-1
- Update to 1.3.91.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Wim Taymans <wtaymans@redhat.com> - 1.2.4-2
- Improve conditional SSE and SSE2 compilation

* Sun Apr 20 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4.

* Mon Feb 10 2014 Brian Pepple <bpepple@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3.
- Drop patch to fix build on aarch64. Fixed upstream.

* Mon Jan 13 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.2.2-2
- Add upstream patch to fix build on aarch64

* Fri Dec 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2.

* Wed Dec 04 2013 Nils Philippsen <nils@redhat.com> - 1.2.1-2
- rebuild for new libvisual

* Mon Nov 11 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1.
- Drop patch to fix potential deadlock on startup. Fixed upstream.

* Thu Oct 03 2013 Bastien Nocera <bnocera@redhat.com> 1.2.0-2
- Fix potential deadlock on startup when playing audio files

* Tue Sep 24 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0.

* Thu Sep 19 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.90-1
- Update to 1.1.90.
- Bump minimum version of orc needed.

* Wed Aug 28 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4.

* Mon Jul 29 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3.

* Fri Jul 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.
- Drop contrast/brightness video playback patch. Fixed upstream.

* Wed May 29 2013 Daniel Drake <dsd@laptop.org> - 1.0.7-2
- Upstream patch to fix contrast/brightness in video playback

* Fri Apr 26 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.7-1
- Update to 1.0.7.

* Wed Apr  3 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-2
- Drop gst-visualise mention from description. (#947658)

* Fri Mar 22 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6.
- Drop BR on PyXML.
- Drop alsa delay patch. Fixed upstream.

* Thu Jan 24 2013 Daniel Drake <dsd@laptop.org> - 1.0.5-3
- Add upstream fix for excessive alsasink CPU usage

* Fri Jan 18 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-2
- Add patch to fix missing mp3 codec discovery. (#680809, #896018)

* Tue Jan  8 2013 Brian Pepple <bpepple@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5.

* Wed Dec 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Nov 21 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Thu Oct 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2.

* Sun Oct  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Mon Oct  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.0-2
- Enable verbose build

* Mon Sep 24 2012 Brian Pepple <bpepple@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0.

* Wed Sep 19 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.99-1
- Update to 0.11.99

* Fri Sep 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.94-1
- Update to 0.11.94.

* Tue Aug 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.93-1
- Update to 0.11.93.
- Package gst-visualise.

* Tue Aug  7 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-2
- Remove rpath.

* Tue Jul 17 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.11.92-1
- Initial Fedora spec file.
