# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# For a complete build enable this
%bcond all_codecs 0

# Break dependency cycles by disabling certain optional dependencies.
%bcond bootstrap 0

# If building with all codecs, then set the pkg_suffix to %%nil.
# We can't handle this with a conditional, as srpm
# generation would not take it into account.
%global pkg_suffix -free

# For alternative builds (do not enable in Fedora!)
%bcond freeworld_lavc 0

%if %{with freeworld_lavc}
# Freeworld builds enable all codecs
%global with_all_codecs 1
# Freeworld builds do not need a package suffix
%global pkg_suffix %{nil}
%global basepkg_suffix -free
%endif

# Fails due to asm issue
%ifarch %{ix86} %{arm}
%bcond lto 0
%else
%bcond lto 1
%endif

%ifarch x86_64
%bcond vpl 1
%bcond vmaf 1
%else
%bcond vpl 0
%bcond vmaf 0
%endif

%ifarch s390 s390x riscv64
%bcond dc1394 0
%bcond ffnvcodec 0
%else
%bcond dc1394 1
%bcond ffnvcodec 1
%endif

%if 0%{?rhel}
# Disable dependencies not available or wanted on RHEL/EPEL
%bcond chromaprint 0
%bcond flite 0
%bcond lc3 0
%else
# Break chromaprint dependency cycle (Fedora-only):
#   ffmpeg (libavcodec-free) → chromaprint → ffmpeg
%bcond chromaprint %{?_with_bootstrap:0}%{!?_with_bootstrap:1}
%bcond flite 1
%bcond lc3 1
%endif

%if 0%{?rhel} && 0%{?rhel} <= 9
# Disable some features because RHEL 9 packages are too old
%bcond lcms2 0
%bcond placebo 0
%else
%bcond lcms2 1
%bcond placebo 1
%endif

# For using an alternative build of EVC codecs
%bcond evc_main 0

%if %{with all_codecs}
%bcond rtmp 1
%bcond vvc 1
%bcond x264 1
%bcond x265 1
%else
%bcond rtmp 0
%bcond vvc 0
%bcond x264 0
%bcond x265 0
%endif

%if %{without lto}
%global _lto_cflags %{nil}
%endif

# FIXME: GCC says there's incompatible pointer casts going on in libavdevice...
%global build_type_safety_c 2

%global av_codec_soversion 61
%global av_device_soversion 61
%global av_filter_soversion 10
%global av_format_soversion 61
%global av_util_soversion 59
%global postproc_soversion 58
%global swresample_soversion 5
%global swscale_soversion 8

Name:           ffmpeg
%global pkg_name %{name}%{?pkg_suffix}

Version:        7.1.2
Release:        4%{?dist}
Summary:        A complete solution to record, convert and stream audio and video
License:        GPL-3.0-or-later
URL:            https://ffmpeg.org/
Source0:        https://ffmpeg.org/releases/ffmpeg-%{version}.tar.xz
Source1:        https://ffmpeg.org/releases/ffmpeg-%{version}.tar.xz.asc
# https://ffmpeg.org/ffmpeg-devel.asc
# gpg2 --import --import-options import-export,import-minimal ffmpeg-devel.asc > ./ffmpeg.keyring
Source2:        ffmpeg.keyring
Source20:       enable_decoders
Source21:       enable_encoders

# Fixes for reduced codec selection on free build
Patch1:         ffmpeg-codec-choice.patch
# Allow to build with fdk-aac-free
# See https://bugzilla.redhat.com/show_bug.cgi?id=1501522#c112
Patch2:         ffmpeg-allow-fdk-aac-free.patch
# Support building with EVC base profile libraries
Patch3:         https://code.ffmpeg.org/FFmpeg/FFmpeg/pulls/20329.patch#/ffmpeg-support-evc-base-libraries.patch

# Backport fix for CVE-2025-22921
Patch10:        https://git.ffmpeg.org/gitweb/ffmpeg.git/patch/7f9c7f9849a2155224711f0ff57ecdac6e4bfb57#/ffmpeg-CVE-2025-22921.patch

# Add first_dts getter to libavformat for Chromium
# See: https://bugzilla.redhat.com/show_bug.cgi?id=2240127
# Reference: https://crbug.com/1306560
Patch1002:      ffmpeg-chromium.patch


Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}

BuildRequires:  AMF-devel
BuildRequires:  fdk-aac-free-devel
%if %{with flite}
BuildRequires:  flite-devel >= 2.2
%endif
BuildRequires:  game-music-emu-devel
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  gnupg2
BuildRequires:  gsm-devel
BuildRequires:  ladspa-devel
BuildRequires:  lame-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libklvanc-devel
BuildRequires:  libmysofa-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXv-devel
BuildRequires:  make
BuildRequires:  nasm
BuildRequires:  perl(Pod::Man)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(aribb24) >= 1.0.3
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(caca)
BuildRequires:  pkgconfig(codec2)
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(frei0r)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libilbc)
BuildRequires:  pkgconfig(jack)
%if %{with lc3}
BuildRequires:  pkgconfig(lc3) >= 1.1.0
%endif
%if %{with lcms2}
BuildRequires:  pkgconfig(lcms2) >= 2.13
%endif
BuildRequires:  pkgconfig(libaribcaption) >= 1.1.1
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libbs2b)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
%if %{with chromaprint}
BuildRequires:  pkgconfig(libchromaprint)
%endif
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libjxl) >= 0.7.0
BuildRequires:  pkgconfig(libmodplug)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libopenmpt)
%if %{with placebo}
BuildRequires:  pkgconfig(libplacebo) >= 4.192.0
%endif
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libqrencode)
BuildRequires:  pkgconfig(librabbitmq)
BuildRequires:  pkgconfig(librist)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libssh)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzmq)
BuildRequires:  pkgconfig(lilv-0)
BuildRequires:  pkgconfig(lv2)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(opencore-amrnb)
BuildRequires:  pkgconfig(OpenCL)
BuildRequires:  pkgconfig(openh264)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(rav1e)
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(shaderc) >= 2019.1
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(snappy)
BuildRequires:  pkgconfig(soxr)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(srt)
BuildRequires:  pkgconfig(SvtAv1Enc) >= 0.9.0
BuildRequires:  pkgconfig(tesseract)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(twolame)
BuildRequires:  pkgconfig(vapoursynth)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(vidstab)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vo-amrwbenc)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(vulkan) >= 1.3.255
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(zimg)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(zvbi-0.2)
BuildRequires:  texinfo
BuildRequires:  xvidcore-devel

%if %{with dc1394}
BuildRequires:  pkgconfig(libavc1394)
BuildRequires:  pkgconfig(libdc1394-2)
BuildRequires:  pkgconfig(libiec61883)
%endif
%if %{with rtmp}
BuildRequires:  librtmp-devel
%endif
%if %{with vpl}
BuildRequires:  pkgconfig(vpl) >= 2.6
%endif
%if %{with evc_main}
BuildRequires:  pkgconfig(xevd)
BuildRequires:  pkgconfig(xeve)
%else
BuildRequires:  pkgconfig(xevdb)
BuildRequires:  pkgconfig(xeveb)
%endif
%if %{with x264}
BuildRequires:  pkgconfig(x264)
%endif
%if %{with x265}
BuildRequires:  pkgconfig(x265)
%endif
%if %{with vmaf}
BuildRequires:  pkgconfig(libvmaf)
%endif


%description
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%dnl --------------------------------------------------------------------------------

%if ! %{with freeworld_lavc}

%if "x%{?pkg_suffix}" != "x"
%package -n     %{pkg_name}
Summary:        A complete solution to record, convert and stream audio and video
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}


%description -n %{pkg_name}
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

#/ "x%%{?pkg_suffix}" != "x"
%endif

%files -n %{pkg_name}
%doc CREDITS README.md
%{_bindir}/ffmpeg
%{_bindir}/ffplay
%{_bindir}/ffprobe
%{_mandir}/man1/ff*.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ffprobe.xsd
%{_datadir}/%{name}/libvpx-*.ffpreset

%dnl --------------------------------------------------------------------------------

%package -n     %{pkg_name}-devel
Summary:        Development package for %{name}
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       pkgconfig

%description -n %{pkg_name}-devel
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%files -n %{pkg_name}-devel
%doc MAINTAINERS doc/APIchanges doc/*.txt
%doc _doc/examples

%dnl --------------------------------------------------------------------------------

%package -n libavcodec%{?pkg_suffix}
Summary:        FFmpeg codec library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
# We require libopenh264 library, which has a dummy implementation and a real one
# In the event that this is being installed, we want to prefer openh264 if available
Suggests:       openh264%{_isa}

%description -n libavcodec%{?pkg_suffix}
The libavcodec library provides a generic encoding/decoding framework
and contains multiple decoders and encoders for audio, video and
subtitle streams, and several bitstream filters.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%files -n libavcodec%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavcodec.so.%{av_codec_soversion}{,.*}

%dnl --------------------------------------------------------------------------------

%package -n libavcodec%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's codec library
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavcodec%{?pkg_suffix}-devel
The libavcodec library provides a generic encoding/decoding framework
and contains multiple decoders and encoders for audio, video and
subtitle streams, and several bitstream filters.

This subpackage contains the headers for FFmpeg libavcodec.

%files -n libavcodec%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavcodec
%{_libdir}/pkgconfig/libavcodec.pc
%{_libdir}/libavcodec.so
%{_mandir}/man3/libavcodec.3*

%dnl --------------------------------------------------------------------------------

%package -n libavdevice%{?pkg_suffix}
Summary:        FFmpeg device library
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libavdevice%{?pkg_suffix}
The libavdevice library provides a generic framework for grabbing from
and rendering to many common multimedia input/output devices, and
supports several input and output devices, including Video4Linux2, VfW,
DShow, and ALSA.

%files -n libavdevice%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavdevice.so.%{av_device_soversion}{,.*}

%dnl --------------------------------------------------------------------------------

%package -n libavdevice%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's device library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavdevice%{?pkg_suffix}-devel
The libavdevice library provides a generic framework for grabbing from
and rendering to many common multimedia input/output devices, and
supports several input and output devices, including Video4Linux2, VfW,
DShow, and ALSA.

This subpackage contains the headers for FFmpeg libavdevice.

%files -n libavdevice%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavdevice
%{_libdir}/pkgconfig/libavdevice.pc
%{_libdir}/libavdevice.so
%{_mandir}/man3/libavdevice.3*

%dnl --------------------------------------------------------------------------------

%package -n libavfilter%{?pkg_suffix}
Summary:        FFmpeg audio and video filtering library
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libavfilter%{?pkg_suffix}
The libavfilter library provides a generic audio/video filtering
framework containing several filters, sources and sinks.

%files -n libavfilter%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavfilter.so.%{av_filter_soversion}{,.*}

%dnl --------------------------------------------------------------------------------

%package -n libavfilter%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's audio/video filter library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavfilter%{?pkg_suffix}-devel
The libavfilter library provides a generic audio/video filtering
framework containing several filters, sources and sinks.

This subpackage contains the headers for FFmpeg libavfilter.

%files -n libavfilter%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavfilter
%{_libdir}/pkgconfig/libavfilter.pc
%{_libdir}/libavfilter.so
%{_mandir}/man3/libavfilter.3*

%dnl --------------------------------------------------------------------------------

%package -n libavformat%{?pkg_suffix}
Summary:        FFmpeg's stream format library
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libavformat%{?pkg_suffix}
The libavformat library provides a generic framework for multiplexing
and demultiplexing (muxing and demuxing) audio, video and subtitle
streams. It encompasses multiple muxers and demuxers for multimedia
container formats.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%files -n libavformat%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavformat.so.%{av_format_soversion}{,.*}

%dnl --------------------------------------------------------------------------------

%package -n libavformat%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's stream format library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavformat%{?pkg_suffix}-devel
The libavformat library provides a generic framework for multiplexing
and demultiplexing (muxing and demuxing) audio, video and subtitle
streams. It encompasses multiple muxers and demuxers for multimedia
container formats.

This subpackage contains the headers for FFmpeg libavformat.

%files -n libavformat%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavformat
%{_libdir}/pkgconfig/libavformat.pc
%{_libdir}/libavformat.so
%{_mandir}/man3/libavformat.3*

%dnl --------------------------------------------------------------------------------

%package -n libavutil%{?pkg_suffix}
Summary:        FFmpeg's utility library
Group:          System/Libraries

%description -n libavutil%{?pkg_suffix}
The libavutil library is a utility library to aid portable multimedia
programming. It contains safe portable string functions, random
number generators, data structures, additional mathematics functions,
cryptography and multimedia related functionality (like enumerations
for pixel and sample formats).

%files -n libavutil%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavutil.so.%{av_util_soversion}{,.*}

%dnl --------------------------------------------------------------------------------

%package -n libavutil%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's utility library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavutil%{?pkg_suffix}-devel
The libavutil library is a utility library to aid portable multimedia
programming. It contains safe portable string functions, random
number generators, data structures, additional mathematics functions,
cryptography and multimedia related functionality (like enumerations
for pixel and sample formats).

This subpackage contains the headers for FFmpeg libavutil.

%files -n libavutil%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavutil
%{_libdir}/pkgconfig/libavutil.pc
%{_libdir}/libavutil.so
%{_mandir}/man3/libavutil.3*

%dnl --------------------------------------------------------------------------------

%package -n libpostproc%{?pkg_suffix}
Summary:        FFmpeg post-processing library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libpostproc%{?pkg_suffix}
A library with video postprocessing filters, such as deblocking and
deringing filters, noise reduction, automatic contrast and brightness
correction, linear/cubic interpolating deinterlacing.

%files -n libpostproc%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libpostproc.so.%{postproc_soversion}{,.*}

%dnl --------------------------------------------------------------------------------

%package -n libpostproc%{?pkg_suffix}-devel
Summary:        Development files for the FFmpeg post-processing library
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libpostproc%{?pkg_suffix}-devel
A library with video postprocessing filters, such as deblocking and
deringing filters, noise reduction, automatic contrast and brightness
correction, linear/cubic interpolating deinterlacing.

This subpackage contains the headers for FFmpeg libpostproc.

%files -n libpostproc%{?pkg_suffix}-devel
%{_includedir}/%{name}/libpostproc
%{_libdir}/pkgconfig/libpostproc.pc
%{_libdir}/libpostproc.so

%dnl --------------------------------------------------------------------------------

%package -n libswresample%{?pkg_suffix}
Summary:        FFmpeg software resampling library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libswresample%{?pkg_suffix}
The libswresample library performs audio conversion between different
sample rates, channel layout and channel formats.

%files -n libswresample%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libswresample.so.%{swresample_soversion}{,.*}

%dnl --------------------------------------------------------------------------------

%package -n libswresample%{?pkg_suffix}-devel
Summary:        Development files for the FFmpeg software resampling library
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libswresample%{?pkg_suffix}-devel
The libswresample library performs audio conversion between different
sample rates, channel layout and channel formats.

This subpackage contains the headers for FFmpeg libswresample.

%files -n libswresample%{?pkg_suffix}-devel
%{_includedir}/%{name}/libswresample
%{_libdir}/pkgconfig/libswresample.pc
%{_libdir}/libswresample.so
%{_mandir}/man3/libswresample.3*

%dnl --------------------------------------------------------------------------------

%package -n libswscale%{?pkg_suffix}
Summary:        FFmpeg image scaling and colorspace/pixel conversion library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libswscale%{?pkg_suffix}
The libswscale library performs image scaling and colorspace and
pixel format conversion operations.

%files -n libswscale%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libswscale.so.%{swscale_soversion}{,.*}

%dnl --------------------------------------------------------------------------------

%package -n libswscale%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's image scaling and colorspace library
Provides:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Conflicts:      libswscale%{?pkg_suffix}-devel < %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libswscale%{?pkg_suffix}-devel
The libswscale library performs image scaling and colorspace and
pixel format conversion operations.

This subpackage contains the headers for FFmpeg libswscale.

%files -n libswscale%{?pkg_suffix}-devel
%{_includedir}/%{name}/libswscale
%{_libdir}/pkgconfig/libswscale.pc
%{_libdir}/libswscale.so
%{_mandir}/man3/libswscale.3*

%endif
# freeworld_lavc bcond

%dnl --------------------------------------------------------------------------------

%if %{with freeworld_lavc}
%package -n libavcodec-freeworld
Summary:        FFmpeg codec library - freeworld overlay
Requires:       libavutil%{?basepkg_suffix}%{_isa} >= %{version}-%{release}
Requires:       libswresample%{?basepkg_suffix}%{_isa} >= %{version}-%{release}
Supplements:    libavcodec%{?basepkg_suffix}%{_isa} >= %{version}-%{release}
# We require libopenh264 library, which has a dummy implementation and a real one
# In the event that this is being installed, we want to install this version
Requires:       openh264%{_isa}

%description -n libavcodec-freeworld
The libavcodec library provides a generic encoding/decoding framework
and contains multiple decoders and encoders for audio, video and
subtitle streams, and several bitstream filters.

This build includes the full range of codecs offered by ffmpeg.

%files -n libavcodec-freeworld
%{_sysconfdir}/ld.so.conf.d/%{name}-%{_lib}.conf
%{_libdir}/%{name}/libavcodec.so.%{av_codec_soversion}{,.*}

# Re-enable ldconfig_scriptlets macros
%{!?ldconfig:%global ldconfig /sbin/ldconfig}
%ldconfig_scriptlets -n libavcodec-freeworld

%endif

%dnl --------------------------------------------------------------------------------

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

%autosetup -S git_am
install -m 0644 %{SOURCE20} enable_decoders
install -m 0644 %{SOURCE21} enable_encoders
# fix -O3 -g in host_cflags
sed -i "s|check_host_cflags -O3|check_host_cflags %{optflags}|" configure
install -m0755 -d _doc/examples
cp -a doc/examples/{*.c,Makefile,README} _doc/examples/

%build
%set_build_flags

# This is not a normal configure script, don't use %%configure
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --datadir=%{_datadir}/%{name} \
    --docdir=%{_docdir}/%{name} \
    --incdir=%{_includedir}/%{name} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --arch=%{_target_cpu} \
    --optflags="%{build_cflags}" \
    --extra-ldflags="%{build_ldflags}" \
    --disable-htmlpages \
    --disable-static \
    --disable-stripping \
    --enable-pic \
    --enable-shared \
    --enable-gpl \
    --enable-version3 \
    --enable-amf \
    --enable-avcodec \
    --enable-avdevice \
    --enable-avfilter \
    --enable-avformat \
    --enable-alsa \
    --enable-bzlib \
%if %{with chromaprint}
    --enable-chromaprint \
%else
    --disable-chromaprint \
%endif
    --disable-cuda-nvcc \
%if %{with ffnvcodec}
    --enable-cuvid \
%endif
    --disable-decklink \
    --enable-frei0r \
    --enable-gcrypt \
    --enable-gmp \
    --enable-gnutls \
    --enable-gray \
    --enable-iconv \
    --enable-ladspa \
%if %{with lcms2}
    --enable-lcms2 \
%endif
    --enable-libaom \
    --enable-libaribb24 \
    --enable-libaribcaption \
    --enable-libass \
    --enable-libbluray \
    --enable-libbs2b \
    --enable-libcaca \
    --enable-libcdio \
    --enable-libcodec2 \
    --enable-libdav1d \
    --disable-libdavs2 \
%if %{with dc1394}
    --enable-libdc1394 \
%endif
    --enable-libdvdnav \
    --enable-libdvdread \
    --enable-libfdk-aac \
%if %{with flite}
    --enable-libflite \
%endif
    --enable-libfontconfig \
    --enable-libfreetype \
    --enable-libfribidi \
    --enable-libgme \
    --enable-libharfbuzz \
    --enable-libgsm \
%if %{with dc1394}
    --enable-libiec61883 \
%endif
    --enable-libilbc \
    --enable-libjack \
    --enable-libjxl \
    --enable-libklvanc \
    --disable-liblensfun \
    --disable-liblcevc-dec \
%if %{with lc3}
    --enable-liblc3 \
%endif
    --enable-libmodplug \
    --enable-libmp3lame \
    --enable-libmysofa \
    --disable-libnpp \
    --enable-libopencore-amrnb \
    --enable-libopencore-amrwb \
    --disable-libopencv \
    --enable-libopenh264 \
    --enable-libopenjpeg \
    --enable-libopenmpt \
    --enable-libopus \
%if %{with placebo}
    --enable-libplacebo \
%endif
    --enable-libpulse \
    --enable-libqrencode \
    --disable-libquirc \
    --enable-librabbitmq \
    --enable-librav1e \
    --enable-librist \
    --enable-librsvg \
%if %{with librtmp}
    --enable-librtmp \
%endif
    --enable-librubberband \
    --enable-libshaderc \
    --disable-libshine \
    --enable-libsmbclient \
    --enable-libsnappy \
    --enable-libsvtav1 \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libsrt \
    --enable-libssh \
    --disable-libtensorflow \
    --enable-libtesseract \
    --enable-libtheora \
    --disable-libtorch \
    --disable-libuavs3d \
    --enable-libtwolame \
    --enable-libv4l2 \
    --enable-libvidstab \
%if %{with vmaf}
    --enable-libvmaf \
%endif
    --enable-libvo-amrwbenc \
    --enable-libvorbis \
%if %{with vpl}
    --enable-libvpl \
%endif
    --enable-libvpx \
    --enable-libwebp \
%if %{with x264}
    --enable-libx264 \
%endif
%if %{with x265}
    --enable-libx265 \
%endif
    --disable-libxavs2 \
    --disable-libxavs \
    --enable-libxcb \
    --enable-libxcb-shape \
    --enable-libxcb-shm \
    --enable-libxcb-xfixes \
%if %{with evc_main}
    --enable-libxeve \
    --enable-libxevd \
%else
    --enable-libxeveb \
    --enable-libxevdb \
%endif
    --enable-libxml2 \
    --enable-libxvid \
    --enable-libzimg \
    --enable-libzmq \
    --enable-libzvbi \
%if %{with lto}
    --enable-lto \
%endif
    --enable-lv2 \
    --enable-lzma \
    --enable-manpages \
%if %{with ffnvcodec}
    --enable-nvdec \
    --enable-nvenc \
%endif
    --enable-openal \
    --disable-openssl \
    --enable-postproc \
    --enable-pthreads \
    --enable-sdl2 \
    --enable-shared \
    --enable-swresample \
    --enable-swscale \
    --enable-v4l2-m2m \
    --enable-vaapi \
    --enable-vapoursynth \
    --enable-vdpau \
    --enable-vulkan \
    --enable-xlib \
    --enable-zlib \
%if %{without all_codecs}
    --enable-muxers \
    --enable-demuxers \
    --enable-hwaccels \
    --disable-encoders \
    --disable-decoders \
    --disable-decoder="h264,hevc,vc1,vvc" \
    --enable-encoder="$(perl -pe 's{^(\w*).*}{$1,}gs' <enable_encoders)" \
    --enable-decoder="$(perl -pe 's{^(\w*).*}{$1,}gs' <enable_decoders)" \
%endif
%ifarch %{power64}
%ifarch ppc64
    --cpu=g5 \
%endif
%ifarch ppc64p7
    --cpu=power7 \
%endif
%ifarch ppc64le
    --cpu=power8 \
%endif
    --enable-pic \
%endif
%ifarch %{arm}
    --disable-runtime-cpudetect --arch=arm \
%ifarch armv6hl
    --cpu=armv6 \
%endif
%ifarch armv7hl armv7hnl
    --cpu=armv7-a \
    --enable-vfpv3 \
    --enable-thumb \
%endif
%ifarch armv7hl
    --disable-neon \
%endif
%ifarch armv7hnl
    --enable-neon \
%endif
%endif
    || cat ffbuild/config.log

cat config.h
cat config_components.h

# Paranoia check
%if %{without all_codecs}
# DECODER
for i in H264 HEVC HEVC_RKMPP VC1 VVC; do
    grep -q "#define CONFIG_${i}_DECODER 0" config_components.h
done

# ENCODER
for i in LIBX264 LIBX264RGB LIBX265; do
    grep -q "#define CONFIG_${i}_ENCODER 0" config_components.h
done
for i in H264 HEVC; do
    for j in MF VIDEOTOOLBOX; do
        grep -q "#define CONFIG_${i}_${j}_ENCODER 0" config_components.h
    done
done
%endif

%make_build V=1
%make_build documentation V=1
%make_build alltools V=1

%install
%make_install V=1

# We will package is as %%doc in the devel package
rm -rf %{buildroot}%{_datadir}/%{name}/examples

%if %{with freeworld_lavc}
# Install the libavcodec freeworld counterpart
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
mkdir -p %{buildroot}%{_libdir}/%{name}
echo -e "%{_libdir}/%{name}\n" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_lib}.conf
cp -pa %{buildroot}%{_libdir}/libavcodec.so.%{av_codec_soversion}{,.*} %{buildroot}%{_libdir}/%{name}
# Drop unneeded stuff
rm -f %{buildroot}%{_libdir}/*.*
rm -rf %{buildroot}%{_libdir}/pkgconfig
rm -rf %{buildroot}%{_includedir}
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_datadir}
%endif


%changelog
* Thu Dec 04 2025 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 7.1.2-4
- disable dc1394 and ffnvcodec on risc-v

* Sun Nov 02 2025 Dominik Mierzejewski <dominik@greysector.net> - 7.1.2-3
- Re-enable openal support (dropped by accident in commit 5917b714, resolves rhbz#2404091)

* Thu Oct 02 2025 Robert-André Mauchin <zebob.m@gmail.com> - 7.1.2-2
- Rebuild for svt-av1 soname bump

* Wed Sep 24 2025 Simone Caronni <negativo17@gmail.com> - 7.1.2-1
- Update to 7.1.2.
- Enable VANC processing for SDI.
- Explicitly list all implicitly enabled/disabled options.

* Tue Aug 26 2025 Neal Gompa <ngompa@fedoraproject.org> - 7.1.1-10
- Disable all subpackages except libavcodec-freeworld with the freeworld bcond

* Mon Aug 25 2025 Neal Gompa <ngompa@fedoraproject.org> - 7.1.1-9
- Enable support for MPEG-5/EVC

* Thu Aug 21 2025 Neal Gompa <ngompa@fedoraproject.org> - 7.1.1-8
- Reorganize spec to group subpackage definitions together
- Add freeworld conditional for third-party builds
- Drop unneeded scriptlets

* Fri Aug 01 2025 Neal Gompa <ngompa@fedoraproject.org> - 7.1.1-7
- Always verify sources

* Tue Jul 29 2025 Nicolas Chauvet <kwizart@gmail.com> - 7.1.1-6
- Rebuilt for libplacebo

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 Neal Gompa <ngompa@fedoraproject.org> - 7.1.1-4
- Switch to regular upstream sources for package build
- Enable more codecs

* Sat Mar 22 2025 Songsong Zhang <U2FsdGVkX1@gmail.com> - 7.1.1-3
- Add missing source files for riscv64

* Thu Mar 13 2025 Fabio Valentini <decathorpe@gmail.com> - 7.1.1-2
- Rebuild for noopenh264 2.6.0

* Thu Mar 06 2025 Dominik Mierzejewski <dominik@greysector.net> - 7.1.1-1
- Update to 7.1.1 (resolves rhbz#2349351)
- Enable LC3 codec via liblc3
- Backport fix for CVE-2025-22921 (resolves rhbz#2346558)

* Fri Feb 07 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 7.1-1
- Rebase to 7.1 (rhbz#2273572)

* Wed Feb 05 2025 Robert-André Mauchin <zebob.m@gmail.com> - 7.0.2-13
- Rebuilt for aom 3.11.0

* Sun Feb 02 2025 Sérgio Basto <sergio@serjux.com> - 7.0.2-12
- Rebuild for jpegxl (libjxl) 0.11.1

* Wed Jan 29 2025 Simone Caronni <negativo17@gmail.com> - 7.0.2-11
- Rebuild for updated VapourSynth.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Michel Lind <salimma@fedoraproject.org> - 7.0.2-9
- Rebuilt for rubberband 4

* Tue Nov 12 2024 Sandro Mani <manisandro@gmail.com> - 7.0.2-8
- Rebuild (tesseract)

* Mon Oct 07 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 7.0.2-7
- Properly enable aribb24/libaribcaption
- Disable VANC dependency as it depends on decklink

* Mon Oct 07 2024 Neal Gompa <ngompa@fedoraproject.org> - 7.0.2-6
- Enable SDI data processing (Kernel Labs VANC) processing
- Enable Japanese DVD subtitles/teletext (aribb24/libaribcaption)

* Mon Oct 07 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 7.0.2-5
- Properly enable noopenh264

* Wed Oct 02 2024 Neal Gompa <ngompa@fedoraproject.org> - 7.0.2-4
- Fix chromaprint bcond

* Wed Sep 25 2024 Michel Lind <salimma@fedoraproject.org> - 7.0.2-3
- Disable omxil completely, it's now retired
- Rebuild for tesseract-5.4.1-3 (soversion change from 5.4.1 to just 5.4)

* Fri Sep 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 7.0.2-2
- Rebuild for newer ffnvcodec

* Fri Sep 06 2024 Neal Gompa <ngompa@fedoraproject.org> - 7.0.2-1
- Rebase to 7.0.2 (rhbz#2273572)
- Drop OpenH264 dlopen headers as we use noopenh264 now
- Use modern bconds

* Sat Aug 24 2024 Fabio Valentini <decathorpe@gmail.com> - 6.1.2-1
- Update to 6.1.2

* Sat Jul 20 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.1.1-19
- Backport fixes for Mesa 24.0.6+ / 21.1.4+ changes for VA-API

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Nicolas Chauvet <kwizart@gmail.com> - 6.1.1-17
- Rebuilt for libplacebo/vmaf

* Wed Jun 19 2024 Dominik Mierzejewski <dominik@greysector.net> - 6.1.1-16
- Backport fix for CVE-2023-49528

* Thu Jun 13 2024 Sandro Mani <manisandro@gmail.com> - 6.1.1-15
- Rebuild for tesseract-5.4.1

* Wed May 29 2024 Robert-André Mauchin <zebob.m@gmail.com> - 6.1.1-14
- Rebuild for svt-av1 2.1.0

* Wed May 22 2024 Simone Caronni <negativo17@gmail.com> - 6.1.1-13
- Rebuild for updated VapourSynth.

* Tue Apr 23 2024 Kalev Lember <klember@redhat.com> - 6.1.1-12
- Stop using bundled openh264 headers in F40+ and build against noopenh264
- Backport a fix to build with Vulkan headers >= 1.3.280.0

* Wed Mar 13 2024 Sérgio Basto <sergio@serjux.com> - 6.1.1-11
- Rebuild for jpegxl (libjxl) 0.10.2

* Tue Mar 12 2024 Dominik Mierzejewski <dominik@greysector.net> - 6.1.1-10
- Enable drawtext filter (requires libharfbuzz)

* Wed Feb 14 2024 Sérgio Basto <sergio@serjux.com> - 6.1.1-9
- Rebuild for jpegxl (libjxl) 0.9.2 with soname bump

* Wed Feb 07 2024 Pete Walter <pwalter@fedoraproject.org> - 6.1.1-8
- Rebuild for libvpx 1.14.x

* Sun Jan 28 2024 Sandro Mani <manisandro@gmail.com> - 6.1.1-7
- Rebuild (tesseract)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.1.1-4
- Add missing files for some of the libraries to fix riscv64 builds

* Fri Jan 12 2024 Fabio Valentini <decathorpe@gmail.com> - 6.1.1-3
- Rebuild for dav1d 1.3.0

* Fri Jan 05 2024 Florian Weimer <fweimer@redhat.com> - 6.1.1-2
- Backport upstream patch to fix C compatibility issues

* Thu Jan 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.1.1-1
- Update to 6.1.1

* Thu Jan 04 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.1-1
- Rebase to 6.1

* Wed Dec 06 2023 Kalev Lember <klember@redhat.com> - 6.0.1-2
- Prefer openh264 over noopenh264
- Backport upstream patch to drop openh264 runtime version checks

* Sat Nov 11 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.0.1-1
- Update to 6.0.1
- Add ffmpeg chromium support patch (#2240127)
- Use git to apply patches

* Fri Nov 10 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.0-16
- Add patches to support enhanced RTMP and AV1 encoding through VA-API
- Force AAC decoding through fdk-aac-free

* Sun Oct 08 2023 Dominik Mierzejewski <dominik@greysector.net> - 6.0-15
- Backport upstream patch to fix segfault when passing non-existent filter
  option (rfbz#6773)

* Sat Oct 07 2023 Sandro Mani <manisandro@gmail.com> - 6.0-14
- Rebuild (tesseract)

* Fri Sep 29 2023 Nicolas Chauvet <nchauvet@linagora.com> - 6.0-13
- Rebuilt for libplacebo

* Fri Aug 25 2023 Dominik Mierzejewski <dominik@greysector.net> - 6.0-12
- Backport upstream patch to fix assembly with binutils 2.41.

* Sat Aug 05 2023 Richard Shaw <hobbes1069@gmail.com> - 6.0-11
- Rebuild for codec2.

* Fri Jul 28 2023 Dominik Mierzejewski <dominik@greysector.net> - 6.0-10
- Rebuild for libplacebo

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Sandro Mani <manisandro@gmail.com> - 6.0-8
- Rebuild (tesseract)

* Sun Jun 18 2023 Sérgio Basto <sergio@serjux.com> - 6.0-7
- Mass rebuild for jpegxl-0.8.1

* Mon Jun 12 2023 Dominik Mierzejewski <dominik@greysector.net> - 6.0-6
- Rebuild for libdc1394

* Thu Apr 06 2023 Adam Williamson <awilliam@redhat.com> - 6.0-5
- Rebuild (tesseract) again

* Mon Apr 03 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.0-4
- Include RISC-V support sources in the tarball

* Mon Apr 03 2023 Sandro Mani <manisandro@gmail.com> - 6.0-3
- Rebuild (tesseract)

* Wed Mar 22 2023 Nicolas Chauvet <kwizart@gmail.com> - 6.0-2
- Backport upstream patches for libplacebo support

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.0-1
- Rebase to version 6.0
- Enable SVT-AV1 on all architectures
- Use oneVPL for QSV
- Switch to SPDX license identifiers

* Wed Feb 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-12
- Enable support for the RIST protocol through librist

* Wed Feb 15 2023 Tom Callaway <spot@fedoraproject.org> - 5.1.2-11
- bootstrap off

* Wed Feb 15 2023 Tom Callaway <spot@fedoraproject.org> - 5.1.2-10
- rebuild for libvpx (bootstrap)

* Mon Feb 13 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.1.2-9
- Enable lcms2, lv2, placebo, rabbitmq, xv

* Mon Feb 13 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-8
- Disable flite for RHEL 9 as flite is too old

* Fri Feb 03 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.1.2-7
- Properly enable caca, flite, gme, iec61883

* Mon Jan 30 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-6
- Enable more approved codecs

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.1.2-4
- Properly enable libzvbi_teletext decoder

* Fri Dec 23 2022 Sandro Mani <manisandro@gmail.com> - 5.1.2-3
- Rebuild (tesseract)

* Wed Nov 09 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-2
- Unconditionally enable Vulkan

* Wed Oct 12 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-1
- Update to version 5.1.2
- Refresh dlopen headers and patch for OpenH264 2.3.1

* Sun Sep 04 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.1.1-1
- Update to version 5.1.1
- Refresh dlopen headers for OpenH264 2.3.0
- Disable omxil and crystalhd for RHEL

* Wed Aug 24 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.1-1
- Rebase to version 5.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Richard Shaw <hobbes1069@gmail.com> - 5.0.1-15
- Rebuild for codec2 1.0.4.

* Fri Jul 08 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-14
- Rebuild (tesseract)

* Wed Jun 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 5.0.1-13
- Rebuilt for new aom, dav1d, rav1e and svt-av1

* Fri Jun 17 2022 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 5.0.1-12
- Rebuild for new srt

* Thu Jun 09 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-11
- Ensure libavdevice-devel is pulled in with devel metapackage

* Sun Jun 05 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-10
- Update for OpenH264 2.2.0

* Tue May 31 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-9
- Rebuild for ilbc-3.0.4

* Thu May 26 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 5.0.1-9
- Rebuild for ilbc-3.0.4 (bootstrap)

* Sat May 21 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-8
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-7
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Sun Apr 24 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-6
- Add VAAPI encoders for mjpeg, mpeg2, vp8, and vp9
- Ensure hwaccels for enabled codecs are turned on

* Tue Apr 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-5
- Drop unused enca build dependency

* Tue Apr 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-4
- Use shaderc for Vulkan support

* Mon Apr 18 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-3
- Fix codec2 support enablement

* Mon Apr 18 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.0.1-2
- Properly enable decoding and encoding ilbc

* Tue Apr 12 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1 to fix crashes with muxing MP4 video (#2073980)

* Tue Apr 05 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.0-11
- Enable OpenCL acceleration
- be explicit about enabled external features in configure
- enable gcrypt
- drop duplicate CFLAGS and use Fedora LDFLAGS

* Thu Mar 10 2022 Sandro Mani <manisandro@gmail.com> - 5.0-10
- Rebuild for tesseract 5.1.0

* Tue Mar 08 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-9
- Drop ffmpeg chromium support patch (#2061392)

* Fri Feb 18 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-8
- Add patch to return correct AVERROR with bad OpenH264 versions

* Fri Feb 18 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-7
- Update OpenH264 dlopen patch to split dlopen code into c and h files

* Thu Feb 17 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-6
- Update OpenH264 dlopen patch to use AVERROR return codes correctly

* Tue Feb 15 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-5
- Disable hardware decoders due to broken failure modes

* Tue Feb 15 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-4
- Add support for dlopening OpenH264
- Add tarball scripts as sources

* Sun Feb 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-3
- Enable more QSV and V4L2M2M codecs

* Sun Feb 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-2
- Enable support for more hardware codecs

* Fri Feb 11 2022 Andreas Schneider <asn@redhat.com> - 5.0-1
- Initial import (fedora#2051008)
