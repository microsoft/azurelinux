# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/qt6-qtwebengine.azl.macros}

%global qt_module qtwebengine

%global _hardened_build 1

# package-notes causes FTBFS (#2043178)
%undefine _package_note_file

# defines for Optional system libraries:
%global use_system_re2 1
%global use_system_libicu 1
%global use_system_libwebp 1
%global use_system_opus 1
%global use_system_ffmpeg 1
# libvpx is exclusive with VA-API support (libva) which is enabled by default
%global use_system_libvpx 0
%global use_system_snappy 1
%global use_system_glib 1
%global use_system_zlib 1
%global use_system_minizip 1
%global use_system_libevent 1
%global use_system_libxml 1
%global use_system_lcms2 1
%global use_system_libpng 1
%global use_system_libtiff 1
%global use_system_libjpeg 1
%global use_system_libopenjpeg2 1
%global use_system_harfbuzz 1
%global use_system_freetype 1
%global use_system_libpci 1
%global use_system_libudev 1

%if 0%{?rhel} && 0%{?rhel} == 9
%global use_system_re2 0
%global use_system_libicu 0
%global use_system_minizip 0
%global use_system_harfbuzz 0
%endif

%if 0%{?rhel} && 0%{?rhel} == 10
%global use_system_zlib 0
%endif

# ppc64le builds currently fail with V8/XFA enabled (qt 6.9.0)
%ifarch ppc64le
%global enable_pdf_v8 0
%else
%global enable_pdf_v8 1
%endif

%if 0%{?fedora} && 0%{?fedora} >= 39
# Bundled python-six is too old to work with Python 3.12+
%global use_system_py_six 1
%endif

# NEON support on ARM (detected at runtime) - disable this if you are hitting
# FTBFS due to e.g. GCC bug https://bugzilla.redhat.com/show_bug.cgi?id=1282495
#global arm_neon 1

# the QMake CONFIG flags to force debugging information to be produced in
# release builds, and for all parts of the code
%ifarch %{arm} aarch64
# the ARM builder runs out of memory during linking with the full setting below,
# so omit debugging information for the parts upstream deems it dispensable for
# (webcore, v8base)
%global debug_config %{nil}
%else
%global debug_config force_debug_info
# webcore_debug v8base_debug
%endif

# spellchecking dictionary directory
%global _qtwebengine_dictionaries_dir %{_qt6_datadir}/qtwebengine_dictionaries

# exclude plugins
%global __provides_exclude ^lib.*plugin\\.so.*$
# and designer plugins
%global __provides_exclude_from ^%{_qt6_plugindir}/.*\\.so$

# FIXME: we cannot use any ~rc or similar suffix as the build
# would fail for having too long filename
#global unstable 1
%if 0%{?unstable}
%global prerelease rc
%endif

%global examples 1

Summary: Qt6 - QtWebEngine components
Name:    qt6-qtwebengine
Version: 6.10.2
Release: 2%{?dist}

# See LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt, for details
# See also http://qt-project.org/doc/qt-5.0/qtdoc/licensing.html
# The other licenses are from Chromium and the code it bundles
License: (LGPLv2 with exceptions or GPLv3 with exceptions) and BSD and LGPLv2+ and ASL 2.0 and IJG and MIT and GPLv2+ and ISC and OpenSSL and (MPLv1.1 or GPLv2 or LGPLv2)
URL:     http://www.qt.io
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

# cleaned tarball with patent-encumbered codecs removed from the bundled FFmpeg
# ./qtwebengine-release.sh
# ./clean_qtwebengine.sh 6.9.0
%if 0%{?unstable}
Source0: %{qt_module}-everywhere-src-%{qt_version}-%{prerelease}-clean.tar.xz
%else
Source0: %{qt_module}-everywhere-src-%{version}-clean.tar.xz
%endif

# cleanup scripts used above
Source2: clean_qtwebengine.sh
Source3: clean_ffmpeg.sh
Source4: get_free_ffmpeg_source_files.py
# macros
Source10: macros.qt6-qtwebengine

# pulseaudio headers
Source20: pulseaudio-12.2-headers.tar.gz
Source9999: qt6-qtwebengine.azl.macros

# workaround FTBFS against kernel-headers-5.2.0+
Patch1:   qtwebengine-SIOCGSTAMP.patch
Patch2:   qtwebengine-link-pipewire.patch
# Fix/workaround FTBFS on aarch64 with newer glibc
Patch3:   qtwebengine-aarch64-new-stat.patch

# Enable OpenH264
Patch4:   qtwebengine-use-openh264.patch

# FTBFS - /usr/include/bits/siginfo-consts.h:219:3: error: expected identifier
# 219 |   SYS_SECCOMP = 1,              /* Seccomp triggered.  */
Patch5:   qtwebengine-chromium-141-glibc-2.42-SYS_SECCOMP.patch

## Upstream patches:
# https://bugreports.qt.io/browse/QTBUG-129985
Patch80:  qtwebengine-fix-arm-build.patch

## Upstreamable patches:
Patch100: qtwebengine-add-missing-pipewire-headers.patch
Patch101: qtwebengine-fix-build-against-gcc16.patch

## ppc64le port
Patch200: qtwebengine-6.9-ppc64.patch
Patch201: qtwebengine-chromium-ppc64.patch
# https://github.com/google/highway/commit/dcc0ca1cd4245ecff9e5ba50818e47d5e2ccf699
Patch202: qtwebengine-chromium-ppc64-highway.patch

# handled by qt6-srpm-macros, which defines %%qt6_qtwebengine_arches
# FIXME use/update qt6_qtwebengine_arches
# 32-bit arches not supported (https://bugreports.qt.io/browse/QTBUG-102143)
ExclusiveArch: aarch64 x86_64 ppc64le

BuildRequires: cmake
BuildRequires: ninja-build >= 1.7.2
BuildRequires: make
%if 0%{?rhel} && 0%{?rhel} < 10
BuildRequires: gcc-toolset-13
BuildRequires: gcc-toolset-13-libatomic-devel
%else
BuildRequires: gcc-c++
%endif

# gn links statically (for now)
BuildRequires: libstdc++-static
BuildRequires: libatomic

BuildRequires: %{__python3}
BuildRequires: python3-html5lib
BuildRequires: gperf
BuildRequires: bison
BuildRequires: flex
BuildRequires: perl-interpreter

BuildRequires: nodejs >= 14.9, /usr/bin/node
BuildRequires: krb5-devel
BuildRequires: git-core

BuildRequires: qt6-srpm-macros
BuildRequires: qt6-qtbase-devel
BuildRequires: qt6-qtbase-private-devel
%{?_qt6_version:Requires: qt6-qtbase%{?_isa} = %{_qt6_version}}

# TODO: check of = is really needed or if >= would be good enough -- rex
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: qt6-qtdeclarative-devel
BuildRequires: qt6-qtlocation-devel
BuildRequires: qt6-qtsensors-devel
BuildRequires: qt6-qtsvg-devel
BuildRequires: qt6-qttools-static
BuildRequires: qt6-qtquickcontrols2-devel
BuildRequires: qt6-qtwebchannel-devel
BuildRequires: qt6-qtwebsockets-devel
BuildRequires: qt6-qthttpserver-devel

# optional system libraries in the order of the -- Configure summary: listing
%if 0%{?use_system_re2}
BuildRequires: pkgconfig(re2) >= 11.0.0
%else
Provides: bundled(re2)
%endif
%if 0%{?use_system_libicu}
BuildRequires: libicu-devel >= 70
%endif
%if 0%{?use_system_libwebp}
BuildRequires: pkgconfig(libwebp) >= 0.6.0
%endif
%if 0%{?use_system_opus}
BuildRequires: pkgconfig(opus) >= 1.3.1
%endif
%if %{?use_system_ffmpeg}
BuildRequires: pkgconfig(libavutil) >= 58.29.100
BuildRequires: pkgconfig(libavcodec) >= 60.31.102
BuildRequires: pkgconfig(libavformat) >= 60.16.100
BuildRequires: pkgconfig(openh264)
%endif
%if %{?use_system_libvpx}
BuildRequires: pkgconfig(vpx) >= 1.10.0
%endif
%if 0%{?use_system_snappy}
BuildRequires: pkgconfig(snappy)
%endif
%if 0%{?use_system_glib}
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gio-2.0)
%endif
%if %{?use_system_zlib}
BuildRequires: pkgconfig(zlib)
%endif
%if 0%{?use_system_minizip}
BuildRequires: pkgconfig(minizip)
%else
Provides: bundled(minizip) = 2.8.1
%endif
%if 0%{?use_system_libevent}
BuildRequires: pkgconfig(libevent)
%endif
%if %{?use_system_libxml}
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(libxslt)
%else
# bundled as "libxml"
# see src/3rdparty/chromium/third_party/libxml/linux/include/libxml/xmlversion.h
Provides: bundled(libxml2) = 2.9.13
# see src/3rdparty/chromium/third_party/libxslt/linux/config.h for version
Provides: bundled(libxslt) = 1.1.3
%endif
%if 0%{?use_system_lcms2}
BuildRequires: pkgconfig(lcms2)
%endif
%if 0%{?use_system_libpng}
BuildRequires: pkgconfig(libpng) >= 1.6.0
%endif
%if 0%{?use_system_libtiff}
BuildRequires: pkgconfig(libtiff-4) >= 4.2.0
%endif
%if 0%{?use_system_libjpeg}
BuildRequires: pkgconfig(libjpeg)
%endif
%if 0%{?use_system_libopenjpeg2}
BuildRequires: pkgconfig(libopenjp2)
%endif
%if 0%{?use_system_harfbuzz}
BuildRequires: pkgconfig(harfbuzz) >= 4.3.0
%endif
%if 0%{?use_system_freetype}
BuildRequires: pkgconfig(freetype2) >= 2.4.2
BuildRequires: pkgconfig(fontconfig)
%endif
%if 0%{?use_system_libpci}
BuildRequires: pkgconfig(libpci)
%endif
%if 0%{?use_system_libudev}
BuildRequires: pkgconfig(libudev)
%endif

# qpa-xcb support libraries
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xproto)
BuildRequires: pkgconfig(xshmfence)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xcb)

# required for webrtc
BuildRequires: pkgconfig(xdamage)

# required for alsa
BuildRequires: pkgconfig(alsa)
# required for pulseaudio
BuildRequires: pkgconfig(libpulse)
# required for vaapi
BuildRequires: pkgconfig(libva)
# required for pipewire
BuildRequires: pkgconfig(libpipewire-0.3)

BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(epoxy)
BuildRequires: pkgconfig(expat)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(libcap)
BuildRequires: pkgconfig(nss) >= 3.26
BuildRequires: pkgconfig(poppler-cpp)


%if 0%{?fedora} && 0%{?fedora} >= 39
BuildRequires: python3-zombie-imp
%endif

# extra (non-upstream) functions needed, see
# src/3rdparty/chromium/third_party/sqlite/README.chromium for details
#BuildRequires: pkgconfig(sqlite3)

# Split subpackage
Requires: qt6-qtpdf%{?_isa} = %{version}-%{release}

## Various bundled libraries that Chromium does not support unbundling :-(
## Only the parts actually built are listed.
## Query for candidates:
## grep third_party/ build.log | sed 's!third_party/!\nthird_party/!g' | \
## grep third_party/ | sed 's!^third_party/!!g' | sed 's!/.*$!!g' | \
## sed 's/\;.*$//g' | sed 's/ .*$//g' | sort | uniq | less
## some false positives where only shim headers are generated for some reason
## some false positives with dummy placeholder dirs (swiftshader, widevine)
## some false negatives where a header-only library is bundled (e.g. x86inc)
## Spot's chromium.spec also has a list that I checked.

# Of course, Chromium itself is bundled. It cannot be unbundled because it is
# not a library, but forked (modified) application code.
Provides: bundled(chromium) = 118.0.5993.220

# Bundled in src/3rdparty/chromium/third_party:
# Check src/3rdparty/chromium/third_party/*/README.chromium for version numbers,
# except where specified otherwise.
# Note that many of those libraries are git snapshots, so version numbers are
# necessarily approximate.
# Also note that the list is probably not complete anymore due to Chromium
# adding more and more bundled stuff at every release, some of which (but not
# all) is actually built in QtWebEngine.
# src/3rdparty/chromium/third_party/angle/doc/ChoosingANGLEBranch.md points to
# http://omahaproxy.appspot.com/deps.json?version=87.0.4280.144 chromium_branch
Provides: bundled(angle)
# Google's fork of OpenSSL
# We cannot build against NSS instead because it no longer works with NSS 3.21:
# HTTPS on, ironically, Google's sites (Google, YouTube, etc.) stops working
# completely and produces only ERR_SSL_PROTOCOL_ERROR errors:
# http://kaosx.us/phpBB3/viewtopic.php?t=1235
# https://bugs.launchpad.net/ubuntu/+source/chromium-browser/+bug/1520568
# So we have to do what Chromium now defaults to (since 47): a "chimera build",
# i.e., use the BoringSSL code and the system NSS certificates.
Provides: bundled(boringssl)
Provides: bundled(brotli)
# Don't get too excited. MPEG and other legally problematic stuff is stripped
# out. See clean_qtwebengine.sh, clean_ffmpeg.sh, and
# get_free_ffmpeg_source_files.py.
# see src/3rdparty/chromium/third_party/ffmpeg/Changelog for the version number
Provides: bundled(ffmpeg) = 5.1.2
Provides: bundled(hunspell) = 1.6.0
Provides: bundled(iccjpeg)
# bundled as "khronos", headers only
Provides: bundled(khronos_headers)
# bundled as "leveldatabase"
Provides: bundled(leveldb) = 1.23
# bundled as "libjingle_xmpp"
Provides: bundled(libjingle)
# see src/3rdparty/chromium/third_party/libsrtp/CHANGES for the version number
Provides: bundled(libsrtp) = 2.4.0
Provides: bundled(libyuv) = 1819
Provides: bundled(modp_b64)
Provides: bundled(ots)
# see src/3rdparty/chromium/third_party/protobuf/CHANGES.txt for the version
Provides: bundled(protobuf) = 3.13.0.1
Provides: bundled(qcms) = 4
Provides: bundled(skia)
# bundled as "smhasher"
Provides: bundled(SMHasher) = 0-147
Provides: bundled(sqlite) = 3.39.4
Provides: bundled(usrsctp)
Provides: bundled(webrtc) = 90

%ifarch %{ix86} x86_64
# bundled by ffmpeg and libvpx:
# header (for assembly) only
Provides: bundled(x86inc)
%endif

# Bundled in src/3rdparty/chromium/base/third_party:
# Check src/3rdparty/chromium/third_party/base/*/README.chromium for version
# numbers, except where specified otherwise.
Provides: bundled(dynamic_annotations) = 4384
Provides: bundled(superfasthash) = 0
Provides: bundled(symbolize)
# bundled as "valgrind", headers only
Provides: bundled(valgrind.h)
# bundled as "xdg_mime"
Provides: bundled(xdg-mime)
# bundled as "xdg_user_dirs"
Provides: bundled(xdg-user-dirs) = 0.10

# Bundled in src/3rdparty/chromium/net/third_party:
# Check src/3rdparty/chromium/third_party/net/*/README.chromium for version
# numbers, except where specified otherwise.
Provides: bundled(mozilla_security_manager) = 1.9.2

# Bundled in src/3rdparty/chromium/url/third_party:
# Check src/3rdparty/chromium/third_party/url/*/README.chromium for version
# numbers, except where specified otherwise.
# bundled as "mozilla", file renamed and modified
Provides: bundled(nsURLParsers)

# Bundled outside of third_party, apparently not considered as such by Chromium:
Provides: bundled(mojo)
# see src/3rdparty/chromium/v8/include/v8_version.h for the version number
Provides: bundled(v8) = 11.8.172.18
# bundled by v8 (src/3rdparty/chromium/v8/src/base/ieee754.cc)
# The version number is 5.3, the last version that upstream released, years ago:
# http://www.netlib.org/fdlibm/readme
Provides: bundled(fdlibm) = 5.3

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
Requires: qt6-qtpdf-devel%{?_isa} = %{version}-%{release}
# not arch'd for now, see if can get away with avoiding multilib'ing -- rex
Requires: %{name}-devtools = %{version}-%{release}
%description devel
%{summary}.

%package devtools
Summary: WebEngine devtools_resources
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devtools
Support for remote debugging.

%if 0%{?examples}
%package examples
Summary: Example files for %{name}
%description examples
%{summary}.
%endif

%package -n qt6-qtpdf
Summary: Qt6 - QtPdf components
%description -n qt6-qtpdf
%{summary}.

%package -n qt6-qtpdf-devel
Summary: Development files for qt6-qtpdf
Requires: qt6-qtpdf%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
Requires: qt6-qtdeclarative-devel%{?_isa}
%description -n qt6-qtpdf-devel
%{summary}.

%package -n qt6-qtpdf-examples
Summary: Example files for qt6-qtpdf
Requires: qt6-qtsvg%{?_isa}
%description -n qt6-qtpdf-examples
%{summary}.

%prep
%setup -q -n %{qt_module}-everywhere-src-%{qt_version}%{?prerelease:-%{prerelease}} -a20

mv pulse src/3rdparty/chromium/

pushd src/3rdparty/chromium
popd

%patch -P1 -p1 -b .SIOCGSTAMP
%patch -P2 -p1 -b .link-pipewire
%patch -P3 -p1 -b .aarch64-new-stat
%patch -P4 -p1 -b .use-openh264
%if 0%{?fedora} > 43 || 0%{?rhel} > 10
%patch -P5 -p1 -b .chromium-141-glibc-2.42-SYS_SECCOMP
%endif

## upstream patches
%patch -P80 -p1 -b .fix-arm-build

## upstreamable patches
%patch -P100 -p1 -b .add-missing-pipewire-headers
%patch -P101 -p1 -b .fix-build-against-gcc16

# ppc64le support
%patch -P200 -p1
pushd src/3rdparty/chromium
%patch -P201 -p1
pushd third_party/highway/src
%patch -P202 -p1
popd
popd


# delete all "toolprefix = " lines from build/toolchain/linux/BUILD.gn, as we
# never cross-compile in native Fedora RPMs, fixes ARM and aarch64 FTBFS
sed -i -e '/toolprefix = /d' -e 's/\${toolprefix}//g' \
  src/3rdparty/chromium/build/toolchain/linux/BUILD.gn

%if 0%{?use_system_py_six}
rm src/3rdparty/chromium/third_party/six/src/six.py
rm src/3rdparty/chromium/third_party/catapult/third_party/six/six.py
rm src/3rdparty/chromium/third_party/wpt_tools/wpt/tools/third_party/six/six.py

ln -s /usr/lib/python%{python3_version}/site-packages/six.py src/3rdparty/chromium/third_party/six/src/six.py
ln -s /usr/lib/python%{python3_version}/site-packages/six.py src/3rdparty/chromium/third_party/catapult/third_party/six/six.py
ln -s /usr/lib/python%{python3_version}/site-packages/six.py src/3rdparty/chromium/third_party/wpt_tools/wpt/tools/third_party/six/six.py
%endif

#%%if 0%{?use_system_re2}
# http://bugzilla.redhat.com/1337585
# can't just delete, but we'll overwrite with system headers to be on the safe side
#cp -bv /usr/include/re2/*.h src/3rdparty/chromium/third_party/re2/src/re2/
#%%endif

# copy the Chromium license so it is installed with the appropriate name
cp -p src/3rdparty/chromium/LICENSE LICENSE.Chromium


# use system libraries not handled by cmake options correctly
system_libs=()
%if %{?use_system_ffmpeg}
system_libs+=(ffmpeg)
system_libs+=(openh264)
%endif
# Use system libraries
src/3rdparty/chromium/build/linux/unbundle/replace_gn_files.py --system-libraries ${system_libs[@]}

# consider doing this as part of the tarball creation step instead?  rdieter
# fix/workaround
# fatal error: QtWebEngineCore/qtwebenginecoreglobal.h: No such file or directory
# if [ ! -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h" ]; then
# {_qt6_libexecdir}/syncqt -version {version}
# fi
#
# # abort if this doesn't get created by syncqt.pl
# test -f "./include/QtWebEngineCore/qtwebenginecoreglobal.h"


%build
%if 0%{?rhel} && 0%{?rhel} < 10
. /opt/rh/gcc-toolset-13/enable
%endif
export STRIP=strip
export NINJAFLAGS="%{__ninja_common_opts}"
export NINJA_PATH=%{__ninja}

# this follows the logic of the Configure summary to turn on and off
%cmake_qt6 \
  -DCMAKE_TOOLCHAIN_FILE:STRING="%{_libdir}/cmake/Qt6/qt.toolchain.cmake" \
  -DFEATURE_webengine_build_gn:BOOL=ON \
  -DFEATURE_webengine_jumbo_build:BOOL=ON \
  -DFEATURE_webengine_developer_build:BOOL=OFF \
  -DFEATURE_qtwebengine_build:BOOL=ON \
  -DFEATURE_qtwebengine_core_build:BOOL=ON \
  -DFEATURE_qtwebengine_widgets_build:BOOL=ON \
  -DFEATURE_qtwebengine_quick_build:BOOL=ON \
  -DFEATURE_qtpdf_build:BOOL=ON \
  -DFEATURE_qtpdf_widgets_build:BOOL=ON \
  -DFEATURE_qtpdf_quick_build:BOOL=ON \
  -DFEATURE_webengine_system_re2:BOOL=%{?use_system_re2} \
  -DFEATURE_webengine_system_icu:BOOL=%{?use_system_libicu} \
  -DFEATURE_webengine_system_libwebp:BOOL=%{?use_system_libwebp} \
  -DFEATURE_webengine_system_opus:BOOL=%{?use_system_opus} \
  -DFEATURE_webengine_system_ffmpeg:BOOL=%{?use_system_ffmpeg} \
  -DFEATURE_webengine_system_libvpx:BOOL=%{?use_system_libvpx} \
  -DFEATURE_webengine_system_snappy:BOOL=%{?use_system_snappy} \
  -DFEATURE_webengine_system_glib:BOOL=%{?use_system_glib} \
  -DFEATURE_webengine_system_zlib:BOOL=%{?use_system_zlib} \
  -DFEATURE_webengine_system_minizip:BOOL=%{?use_system_minizip} \
  -DFEATURE_webengine_system_libevent:BOOL=%{?use_system_libevent} \
  -DFEATURE_webengine_system_libxml:BOOL=%{?use_system_libxml} \
  -DFEATURE_webengine_system_lcms2:BOOL=%{?use_system_lcms2} \
  -DFEATURE_webengine_system_libpng:BOOL=%{?use_system_libpng} \
  -DFEATURE_webengine_system_libtiff:BOOL=%{?use_system_libtiff} \
  -DFEATURE_webengine_system_libjpeg:BOOL=%{?use_system_libjpeg} \
  -DFEATURE_webengine_system_libopenjpeg2:BOOL=%{?use_system_libopenjpeg2} \
  -DFEATURE_webengine_system_harfbuzz:BOOL=%{?use_system_harfbuzz} \
  -DFEATURE_webengine_system_freetype:BOOL=%{?use_system_freetype} \
  -DFEATURE_webengine_system_libpci:BOOL=%{?use_system_libpci} \
  -DFEATURE_webengine_system_libudev:BOOL=%{?use_system_libudev} \
  -DFEATURE_webengine_embedded_build:BOOL=OFF \
  -DFEATURE_webengine_pepper_plugins:BOOL=ON \
  -DFEATURE_webengine_printing_and_pdf:BOOL=ON \
  -DFEATURE_webengine_proprietary_codecs:BOOL=ON \
  -DFEATURE_webengine_spellchecker:BOOL=ON \
  -DFEATURE_webengine_native_spellchecker:BOOL=OFF \
  -DFEATURE_webengine_webrtc:BOOL=ON \
  -DFEATURE_webengine_webrtc_pipewire:BOOL=ON \
  -DFEATURE_webengine_geolocation:BOOL=ON \
  -DFEATURE_webengine_webchannel:BOOL=ON \
  -DFEATURE_webengine_kerberos:BOOL=ON \
  -DFEATURE_webengine_extensions:BOOL=ON \
  -DFEATURE_webengine_ozone_x11:BOOL=ON \
  -DFEATURE_webengine_vulkan:BOOL=ON \
  -DFEATURE_webengine_vaapi:BOOL=ON \
  -DFEATURE_webengine_system_alsa:BOOL=ON \
  -DFEATURE_webengine_system_pulseaudio:BOOL=ON \
  -DFEATURE_webengine_system_gbm:BOOL=ON \
  -DFEATURE_webengine_v8_context_snapshot:BOOL=ON \
  -DFEATURE_webenginedriver:BOOL=ON \
  -DFEATURE_pdf_v8:BOOL=%{?enable_pdf_v8} \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{_rpmmacrodir}/macros.qt6-qtwebengine
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{_rpmmacrodir}/macros.qt6-qtwebengine

# .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
# explicitly omit, at least until there's a real library installed associated with it -- rex
rm -fv Qt6WebEngineCore.la
popd

mkdir -p %{buildroot}%{_qtwebengine_dictionaries_dir}

# adjust cmake dep(s) to allow for using the same Qt6 that was used to build it
# using the lesser of %%version, %%_qt6_version
%global lesser_version $(echo -e "%{version}\\n%{_qt6_version}" | sort -V | head -1)
sed -i -e "s|%{version} \${_Qt6WebEngine|%{lesser_version} \${_Qt6WebEngine|" \
  %{buildroot}%{_qt6_libdir}/cmake/Qt6WebEngine*/Qt6WebEngine*Config.cmake


%if 0%{?rhel} && 0%{?rhel} < 10
%filetriggerin -- %{_datadir}/myspell
%else
%filetriggerin -- %{_datadir}/hunspell
%endif

while read filename ; do
  case "$filename" in
    *.dic)
      bdicname=%{_qtwebengine_dictionaries_dir}/`basename -s .dic "$filename"`.bdic
      %{_qt6_libdir}/qt6/libexec/qwebengine_convert_dict "$filename" "$bdicname" &> /dev/null || :
      ;;
  esac
done

%files
%license LICENSE.*
%{_qt6_archdatadir}/sbom/%{qt_module}-%{version}.spdx
%{_qt6_archdatadir}/sbom/qtpdf-%{version}.spdx
%{_qt6_libdir}/libQt6WebEngineCore.so.*
%{_qt6_libdir}/libQt6WebEngineQuick.so.*
%{_qt6_libdir}/libQt6WebEngineQuickDelegatesQml.so.*
%{_qt6_libdir}/libQt6WebEngineWidgets.so.*
%{_qt6_libdir}/qt6/libexec/gn
%{_qt6_libdir}/qt6/libexec/qwebengine_convert_dict
%{_qt6_libdir}/qt6/libexec/QtWebEngineProcess
%{_qt6_libdir}/qt6/libexec/webenginedriver
%dir %{_qt6_libdir}/qt6/qml/QtWebEngine
%{_qt6_libdir}/qt6/qml/QtWebEngine/*
%dir %{_qt6_datadir}/resources/
%{_qt6_datadir}/resources/v8_context_snapshot.bin
%{_qt6_datadir}/resources/qtwebengine_resources.pak
%{_qt6_datadir}/resources/qtwebengine_resources_100p.pak
%{_qt6_datadir}/resources/qtwebengine_resources_200p.pak
%if ! 0%{?use_system_libicu}
%{_qt6_datadir}/resources/icudtl.dat
%endif
%dir %{_qtwebengine_dictionaries_dir}
%dir %{_qt6_translationdir}/qtwebengine_locales
%lang(am) %{_qt6_translationdir}/qtwebengine_locales/am.pak
%lang(ar) %{_qt6_translationdir}/qtwebengine_locales/ar.pak
%lang(bg) %{_qt6_translationdir}/qtwebengine_locales/bg.pak
%lang(bn) %{_qt6_translationdir}/qtwebengine_locales/bn.pak
%lang(ca) %{_qt6_translationdir}/qtwebengine_locales/ca.pak
%lang(cs) %{_qt6_translationdir}/qtwebengine_locales/cs.pak
%lang(da) %{_qt6_translationdir}/qtwebengine_locales/da.pak
%lang(de) %{_qt6_translationdir}/qtwebengine_locales/de.pak
%lang(el) %{_qt6_translationdir}/qtwebengine_locales/el.pak
%lang(en) %{_qt6_translationdir}/qtwebengine_locales/en-GB.pak
%lang(en) %{_qt6_translationdir}/qtwebengine_locales/en-US.pak
%lang(es) %{_qt6_translationdir}/qtwebengine_locales/es-419.pak
%lang(es) %{_qt6_translationdir}/qtwebengine_locales/es.pak
%lang(et) %{_qt6_translationdir}/qtwebengine_locales/et.pak
%lang(fa) %{_qt6_translationdir}/qtwebengine_locales/fa.pak
%lang(fi) %{_qt6_translationdir}/qtwebengine_locales/fi.pak
%lang(fil) %{_qt6_translationdir}/qtwebengine_locales/fil.pak
%lang(fr) %{_qt6_translationdir}/qtwebengine_locales/fr.pak
%lang(gu) %{_qt6_translationdir}/qtwebengine_locales/gu.pak
%lang(he) %{_qt6_translationdir}/qtwebengine_locales/he.pak
%lang(hi) %{_qt6_translationdir}/qtwebengine_locales/hi.pak
%lang(hr) %{_qt6_translationdir}/qtwebengine_locales/hr.pak
%lang(hu) %{_qt6_translationdir}/qtwebengine_locales/hu.pak
%lang(id) %{_qt6_translationdir}/qtwebengine_locales/id.pak
%lang(it) %{_qt6_translationdir}/qtwebengine_locales/it.pak
%lang(ja) %{_qt6_translationdir}/qtwebengine_locales/ja.pak
%lang(kn) %{_qt6_translationdir}/qtwebengine_locales/kn.pak
%lang(ko) %{_qt6_translationdir}/qtwebengine_locales/ko.pak
%lang(lt) %{_qt6_translationdir}/qtwebengine_locales/lt.pak
%lang(lv) %{_qt6_translationdir}/qtwebengine_locales/lv.pak
%lang(ml) %{_qt6_translationdir}/qtwebengine_locales/ml.pak
%lang(mr) %{_qt6_translationdir}/qtwebengine_locales/mr.pak
%lang(ms) %{_qt6_translationdir}/qtwebengine_locales/ms.pak
%lang(nb) %{_qt6_translationdir}/qtwebengine_locales/nb.pak
%lang(nl) %{_qt6_translationdir}/qtwebengine_locales/nl.pak
%lang(pl) %{_qt6_translationdir}/qtwebengine_locales/pl.pak
%lang(pt_BR) %{_qt6_translationdir}/qtwebengine_locales/pt-BR.pak
%lang(pt_PT) %{_qt6_translationdir}/qtwebengine_locales/pt-PT.pak
%lang(ro) %{_qt6_translationdir}/qtwebengine_locales/ro.pak
%lang(ru) %{_qt6_translationdir}/qtwebengine_locales/ru.pak
%lang(sk) %{_qt6_translationdir}/qtwebengine_locales/sk.pak
%lang(sl) %{_qt6_translationdir}/qtwebengine_locales/sl.pak
%lang(sr) %{_qt6_translationdir}/qtwebengine_locales/sr.pak
%lang(sv) %{_qt6_translationdir}/qtwebengine_locales/sv.pak
%lang(sw) %{_qt6_translationdir}/qtwebengine_locales/sw.pak
%lang(ta) %{_qt6_translationdir}/qtwebengine_locales/ta.pak
%lang(te) %{_qt6_translationdir}/qtwebengine_locales/te.pak
%lang(th) %{_qt6_translationdir}/qtwebengine_locales/th.pak
%lang(tr) %{_qt6_translationdir}/qtwebengine_locales/tr.pak
%lang(uk) %{_qt6_translationdir}/qtwebengine_locales/uk.pak
%lang(vi) %{_qt6_translationdir}/qtwebengine_locales/vi.pak
%lang(zh_CN) %{_qt6_translationdir}/qtwebengine_locales/zh-CN.pak
%lang(zh_TW) %{_qt6_translationdir}/qtwebengine_locales/zh-TW.pak

%files devel
%{_rpmmacrodir}/macros.qt6-qtwebengine
%dir %{_qt6_headerdir}/QtWebEngineCore
%{_qt6_headerdir}/QtWebEngineCore/*
%dir %{_qt6_headerdir}/QtWebEngineQuick
%{_qt6_headerdir}/QtWebEngineQuick/*
%dir %{_qt6_headerdir}/QtWebEngineWidgets
%{_qt6_headerdir}/QtWebEngineWidgets/*
%{_qt6_libdir}/qt6/metatypes/qt6webengine*.json
%{_qt6_libdir}/qt6/modules/WebEngine*.json
%{_qt6_libdir}/libQt6WebEngineCore.so
%{_qt6_libdir}/libQt6WebEngineQuick.so
%{_qt6_libdir}/libQt6WebEngineQuickDelegatesQml.so
%{_qt6_libdir}/libQt6WebEngineWidgets.so
%{_qt6_libdir}/libQt6WebEngineCore.prl
%{_qt6_libdir}/libQt6WebEngineQuick.prl
%{_qt6_libdir}/libQt6WebEngineQuickDelegatesQml.prl
%{_qt6_libdir}/libQt6WebEngineWidgets.prl
%dir %{_qt6_libdir}/cmake/Qt6Designer
%dir %{_qt6_libdir}/cmake/Qt6WebEngineCore
%dir %{_qt6_libdir}/cmake/Qt6WebEngineCorePrivate
%dir %{_qt6_libdir}/cmake/Qt6WebEngineCoreTools
%dir %{_qt6_libdir}/cmake/Qt6WebEngineQuick
%dir %{_qt6_libdir}/cmake/Qt6WebEngineQuickDelegatesQml
%dir %{_qt6_libdir}/cmake/Qt6WebEngineQuickPrivate
%dir %{_qt6_libdir}/cmake/Qt6WebEngineWidgets
%dir %{_qt6_libdir}/cmake/Qt6WebEngineWidgetsPrivate
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtWebEngine*
%{_qt6_libdir}/cmake/Qt6Designer/Qt6QWebEngine*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6qtwebengine*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineCore/*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineCorePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineCoreTools/*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineQuick/*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineQuickDelegatesQml/*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineQuickPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineWidgets/*.cmake
%{_qt6_libdir}/cmake/Qt6WebEngineWidgetsPrivate/*.cmake
%{_qt6_libdir}/pkgconfig/Qt6WebEngineCore.pc
%{_qt6_libdir}/pkgconfig/Qt6WebEngineQuick.pc
%{_qt6_libdir}/pkgconfig/Qt6WebEngineQuickDelegatesQml.pc
%{_qt6_libdir}/pkgconfig/Qt6WebEngineWidgets.pc
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_webengine*.pri
%{_qt6_plugindir}/designer/libqwebengineview.so

%files devtools
%{_qt6_datadir}/resources/qtwebengine_devtools_resources.pak

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/webengine*
%endif

%files -n qt6-qtpdf
%license LICENSE.*
%{_qt6_libdir}/libQt6Pdf.so.*
%{_qt6_libdir}/libQt6PdfQuick.so.*
%{_qt6_libdir}/libQt6PdfWidgets.so.*
%dir %{_qt6_libdir}/qt6/qml/QtQuick/Pdf
%{_qt6_libdir}/qt6/qml/QtQuick/Pdf/*
%{_qt6_plugindir}/imageformats/libqpdf.so

%files -n qt6-qtpdf-devel
%dir %{_qt6_headerdir}/QtPdf
%{_qt6_headerdir}/QtPdf/*
%dir %{_qt6_headerdir}/QtPdfQuick
%{_qt6_headerdir}/QtPdfQuick/*
%dir %{_qt6_headerdir}/QtPdfWidgets
%{_qt6_headerdir}/QtPdfWidgets/*
%{_qt6_libdir}/qt6/metatypes/qt6pdf*.json
%{_qt6_libdir}/qt6/modules/Pdf*.json
%{_qt6_libdir}/libQt6Pdf.so
%{_qt6_libdir}/libQt6PdfQuick.so
%{_qt6_libdir}/libQt6PdfWidgets.so
%{_qt6_libdir}/libQt6Pdf.prl
%{_qt6_libdir}/libQt6PdfQuick.prl
%{_qt6_libdir}/libQt6PdfWidgets.prl
%dir %{_qt6_libdir}/cmake/Qt6Pdf
%dir %{_qt6_libdir}/cmake/Qt6PdfPrivate
%dir %{_qt6_libdir}/cmake/Qt6PdfQuick
%dir %{_qt6_libdir}/cmake/Qt6PdfQuickPrivate
%dir %{_qt6_libdir}/cmake/Qt6PdfWidgets
%dir %{_qt6_libdir}/cmake/Qt6PdfWidgetsPrivate
%{_qt6_libdir}/cmake/Qt6Gui/Qt6QPdf*.cmake
%{_qt6_libdir}/cmake/Qt6Pdf/*.cmake
%{_qt6_libdir}/cmake/Qt6PdfPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6PdfQuick/*.cmake
%{_qt6_libdir}/cmake/Qt6PdfQuickPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6PdfWidgets/*.cmake
%{_qt6_libdir}/cmake/Qt6PdfWidgetsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/Qt6Pdf*.cmake
%{_qt6_libdir}/pkgconfig/Qt6Pdf.pc
%{_qt6_libdir}/pkgconfig/Qt6PdfQuick.pc
%{_qt6_libdir}/pkgconfig/Qt6PdfWidgets.pc
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_pdf*.pri

%if 0%{?examples}
%files -n qt6-qtpdf-examples
%{_qt6_examplesdir}/pdf*
%endif

%changelog
* Tue Feb 10 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.1-5
- Fix Quick popup window positioning under X11

* Sun Jan 11 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.1-4
- Apply the "Move GPU info logging into the GPU thread" patch

* Thu Jan 08 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.1-3
- Move GPU info logging into the GPU thread

* Fri Nov 21 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-2
- Rebuild for Koji infra issue

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Thu Oct 30 2025 Dominik Mierzejewski <dominik@greysector.net> - 6.10.0-4
- Rebuilt for FFmpeg 8

* Thu Oct 30 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-3
- Fix FTBS in rawhide due to glib and PipeWire updates

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-2
- 6.10.0

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Mon Sep 08 2025 Sandro Mani <manisandro@gmail.com> - 6.9.2-2
- Revert commit bcee2dbf412cc655c1b467091b581c696d234e3f

* Fri Aug 29 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 6.9.1-3
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Tue Apr 22 2025 Marie Loise Nolden <loise@kde.org> - 6.9.0-2
- global define all optional system libs, enable XFA
- cleanup spec

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Mon Mar 24 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-0.1
- 6.9.0 RC

* Thu Mar 13 2025 Fabio Valentini <decathorpe@gmail.com> - 6.8.2-5
- Rebuild for noopenh264 2.6.0

* Tue Mar 04 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-4
- Unbundle libxml and libxslt

* Mon Mar 03 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-3
- Rework OpenH264 support following Chromium package
- Backport upstream change for ffmpeg codec selection issues.

* Mon Feb 17 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-2
- Bump build for ppc64le enablement

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 15 2024 Pavel Solovev <daron439@gmail.com> - 6.8.1-3
- Add optional deps

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-2
- Move Software Bill of Materials from -devel

* Tue Dec 03 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
- 6.8.1

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Mon Sep 23 2024 Fabio Valentini <decathorpe@gmail.com> - 6.7.2-4
- Rebuild for ffmpeg 7

* Mon Aug 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-3
- Fix building with system ffmpeg

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Wed May 22 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Wed Apr 24 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-2
- Rework and enable openh264 patches

* Wed Apr 03 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Sun Mar 3 2024 Marie Loise Nolden <loise@kde.org> - 6.6.2-3
- move qt designer plugin to -devel
- remove old doc package code (docs are in qt6-doc)

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Fri Oct 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-2
- Move v8_context_snapshot file to correct subpackage

* Wed Oct 11 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Tue Sep 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.2-2
- Separate qtpdf subpackages

* Mon Jul 24 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-3
- Python 3.12 Fixes

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-2
- Rebuilt for ICU 73.2

* Thu May 25 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Tue Apr 04 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Fri Mar 24 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.4.2-4
- Rebuild for ffmpeg 6.0

* Sat Feb 25 2023 Marek Kasik <mkasik@redhat.com> - 6.4.2-3
- Rebuild for freetype-2.13.0

* Wed Feb 15 2023 Tom Callaway <spot@fedoraproject.org> - 6.4.2-2
- rebuild for libvpx

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1

- Initial package
