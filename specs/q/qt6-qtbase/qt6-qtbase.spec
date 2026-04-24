# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# See http://bugzilla.redhat.com/223663
%global multilib_archs x86_64 %{ix86} %{?mips} ppc64 ppc s390x s390 sparc64 sparcv9
%global multilib_basearchs x86_64 %{?mips64} ppc64 s390x sparc64

%ifarch s390x ppc64le aarch64 armv7hl riscv64
%global no_sse2  1
%endif

%if 0%{?rhel} && 0%{?rhel} < 9
%ifarch %{ix86}
%global no_sse2  1
%endif
%endif

%if 0%{?rhel} >= 10
# Use mutter on RHEL 10+ since it's the only shipped compositor
%global wlheadless_compositor mutter
%else
# Use the simple reference compositor to simplify dependencies
%global wlheadless_compositor weston
%endif

%global platform linux-g++

%if 0%{?use_clang}
%global platform linux-clang
%endif

%global qt_module qtbase

# use external qt_settings pkg
%if 0%{?fedora}
%global qt_settings 1
%endif

%global journald 1
BuildRequires: pkgconfig(libsystemd)

%global examples 1
## skip for now, until we're better at it --rex
#global tests 1

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

Name:    qt6-qtbase
Summary: Qt6 - QtBase components
Version: 6.10.2
Release: 3%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://qt-project.org/
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1227295
Source1: qtlogging.ini

# header file to workaround multilib issue
# https://bugzilla.redhat.com/show_bug.cgi?id=1036956
Source5: qconfig-multilib.h

# xinitrc script to check for OpenGL 1 only drivers and automatically set
# QT_XCB_FORCE_SOFTWARE_OPENGL for them
Source6: 10-qt6-check-opengl2.sh

# macros
Source10: macros.qt6-qtbase

Patch1:  qtbase-CMake-Install-objects-files-into-ARCHDATADIR.patch
Patch2:  qtbase-use-only-major-minor-for-private-api-tag.patch

# upstreamable patches
# namespace QT_VERSION_CHECK to workaround major/minor being pre-defined (#1396755)
Patch50: qtbase-version-check.patch

# 1. Workaround moc/multilib issues
# https://bugzilla.redhat.com/show_bug.cgi?id=1290020
# https://bugreports.qt.io/browse/QTBUG-49972
# 2. Workaround sysmacros.h (pre)defining major/minor a breaking stuff
Patch51: qtbase-moc-macros.patch

# drop -O3 and make -O2 by default
Patch54: qtbase-cxxflag.patch

# fix for new mariadb
Patch56: qtbase-mysql.patch

# fix FTBFS against libglvnd-1.3.4+
Patch58: qtbase-libglvnd.patch

# upstream patches
Patch100: qtbase-wayland-convey-preference-for-server-side-decorations.patch
Patch101: qtbase-wayland-compress-high-frequency-mouse-events.patch
Patch102: qtbase-wayland-optimize-scroll-operations.patch
Patch103: qtbase-wayland-enable-event-compression-and-fix-scroll-end-event.patch
Patch104: qtbase-wayland-fix-crash-in-qwaylandshmbackingstore-scroll.patch

# Do not check any files in %%{_qt6_plugindir}/platformthemes/ for requires.
# Those themes are there for platform integration. If the required libraries are
# not there, the platform to integrate with isn't either. Then Qt will just
# silently ignore the plugin that fails to load. Thus, there is no need to let
# RPM drag in gtk3 as a dependency for the GTK+3 dialog support.
%global __requires_exclude_from ^%{_qt6_plugindir}/platformthemes/.*$
# filter plugin provides
%global __provides_exclude_from ^%{_qt6_plugindir}/.*\\.so$

%if 0%{?use_clang}
BuildRequires: clang >= 6.0.0
%else
BuildRequires: gcc-c++
%endif
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
%if 0%{?fedora} || 0%{?epel}
BuildRequires: double-conversion-devel
%else
Provides:      bundled(double-conversion)
%endif
%if 0%{?fedora} || 0%{?epel}
BuildRequires: libb2-devel
%else
Provides:      bundled(libb2)
%endif
Provides:      bundled(emoji-segmenter)
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: libzstd-devel
BuildRequires: mtdev-devel
%if 0%{?fedora} || 0%{?epel}
BuildRequires: tslib-devel
%endif
BuildRequires: pkgconfig(alsa)
# required for -accessibility
BuildRequires: pkgconfig(atspi-2)
# http://bugzilla.redhat.com/1196359
%global dbus_linked 1
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libproxy-1.0)
BuildRequires: pkgconfig(libsctp)
# xcb-sm
BuildRequires: pkgconfig(ice) pkgconfig(sm)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libudev)
BuildRequires: openssl-devel
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(libinput)
BuildRequires: pkgconfig(xcb-xkb) >= 1.10
BuildRequires: pkgconfig(xcb-util)
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: pkgconfig(xkbcommon-x11) >= 0.4.1
BuildRequires: pkgconfig(xkeyboard-config)
%global vulkan 1
BuildRequires: pkgconfig(vulkan)
%global egl 1
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libglvnd)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-cursor)
BuildRequires: pkgconfig(wayland-egl)

%global sqlite 1
BuildRequires: pkgconfig(sqlite3) >= 3.7
BuildRequires: pkgconfig(harfbuzz) >= 0.9.42
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libpcre2-16) >= 10.20
%global pcre 1
BuildRequires: pkgconfig(xcb-xkb)
BuildRequires: pkgconfig(xcb) pkgconfig(xcb-glx) pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil) pkgconfig(xcb-cursor)
BuildRequires: pkgconfig(zlib)
BuildRequires: perl
BuildRequires: perl-generators
BuildRequires: python3
BuildRequires: qt6-rpm-macros

%if 0%{?tests}
BuildRequires: dbus-x11
BuildRequires: mesa-dri-drivers
BuildRequires: time
BuildRequires: (wlheadless-run and %{wlheadless_compositor})
%endif

Requires:      qt6-filesystem

Requires: %{name}-common = %{version}-%{release}

## Sql drivers
%if 0%{?fedora} || 0%{?epel}
%global ibase 1
%endif


%description
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package common
Summary: Common files for Qt6
Requires: %{name} = %{version}-%{release}
Obsoletes: qgnomeplatform-common <= 0.9.3
Provides:  qgnomeplatform-common = %{version}-%{release}
BuildArch: noarch
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-gui%{?_isa}
%if 0%{?egl}
Requires: pkgconfig(egl)
%endif
Requires: pkgconfig(gl)
%if 0%{?vulkan}
Requires: pkgconfig(vulkan)
%endif
# Optional dev dependency of Qt6::Gui
Requires: pkgconfig(xkbcommon)
# for Qt6::WaylandClient
Requires: pkgconfig(wayland-server)
Requires: pkgconfig(wayland-client)
Requires: pkgconfig(wayland-cursor)
Requires: pkgconfig(wayland-egl)
Requires: qt6-rpm-macros
%if 0%{?use_clang}
Requires: clang >= 3.7.0
%endif
%if 0%{?ibase}
Requires: %{name}-ibase%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-mysql%{?_isa} = %{version}-%{release}
Requires: %{name}-odbc%{?_isa} = %{version}-%{release}
Requires: %{name}-postgresql%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package private-devel
Summary: Development files for %{name} private APIs
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
# QtPrintSupport/private requires cups/ppd.h
Requires: cups-devel
%description private-devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description examples
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig(fontconfig)
Requires: pkgconfig(glib-2.0)
Requires: pkgconfig(libinput)
Requires: pkgconfig(xkbcommon)
Requires: pkgconfig(zlib)

%description static
%{summary}.

%if 0%{?ibase}
%package ibase
Summary: IBase driver for Qt6's SQL classes
BuildRequires: firebird-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description ibase
%{summary}.
%endif

%package mysql
Summary: MySQL driver for Qt6's SQL classes
%if 0%{?fedora} > 27 || 0%{?rhel} > 8
BuildRequires: mariadb-connector-c-devel
%else
BuildRequires: mysql-devel
%endif
Requires: %{name}%{?_isa} = %{version}-%{release}
%description mysql
%{summary}.

%package odbc
Summary: ODBC driver for Qt6's SQL classes
BuildRequires: unixODBC-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description odbc
%{summary}.

%package postgresql
Summary: PostgreSQL driver for Qt6's SQL classes
BuildRequires: libpq-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description postgresql
%{summary}.

# debating whether to do 1 subpkg per library or not -- rex
%package gui
Summary: Qt6 GUI-related libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Recommends: mesa-dri-drivers%{?_isa}
# Required for some locales: https://pagure.io/fedora-kde/SIG/issue/311
Recommends: qt6-qttranslations
Obsoletes: adwaita-qt6 <= 1.4.2
Obsoletes: libadwaita-qt6 <= 1.4.2
Obsoletes: qgnomeplatform-qt6 <= 0.9.3
Provides:  qgnomeplatform-qt6 = %{version}-%{release}
# for Source6: 10-qt6-check-opengl2.sh:
# glxinfo
Requires: glx-utils
%description gui
Qt6 libraries used for drawing widgets and OpenGL items.


%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1

# move some bundled libs to ensure they're not accidentally used
pushd src/3rdparty
mkdir UNUSED
mv harfbuzz-ng freetype libjpeg libpng sqlite zlib UNUSED/
popd

# builds failing mysteriously on f20
# ./configure: Permission denied
# check to ensure that can't happen -- rex
test -x configure || chmod +x configure


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
# https://bugzilla.redhat.com/1900527
%define _lto_cflags %{nil}

## FIXME/TODO:
# * for %%ix86, add sse2 enabled builds for Qt6Gui, Qt6Core, QtNetwork, see also:
#   http://anonscm.debian.org/cgit/pkg-kde/qt/qtbase.git/tree/debian/rules (234-249)

## adjust $RPM_OPT_FLAGS
# remove -fexceptions
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`
RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{?qt6_arm_flag} %{?qt6_deprecated_flag} %{?qt6_null_flag}"

%if 0%{?use_clang}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fno-delete-null-pointer-checks||g'`
%endif

export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS $RPM_LD_FLAGS"
export MAKEFLAGS="%{?_smp_mflags}"

%cmake_qt6 \
 -DFEATURE_accessibility=ON \
 -DFEATURE_fontconfig=ON \
 -DFEATURE_glib=ON \
 -DFEATURE_sse2=%{?no_sse2:OFF}%{!?no_sse2:ON} \
 -DFEATURE_icu=ON \
 -DFEATURE_enable_new_dtags=ON \
 -DFEATURE_emojisegmenter=ON \
 -DFEATURE_journald=%{?journald:ON}%{!?journald:OFF} \
 -DFEATURE_openssl_linked=ON \
 -DFEATURE_openssl_hash=ON \
 -DFEATURE_libproxy=ON \
 -DFEATURE_sctp=ON \
 -DFEATURE_separate_debug_info=OFF \
 -DFEATURE_reduce_relocations=OFF \
 -DFEATURE_relocatable=OFF \
 -DFEATURE_system_jpeg=ON \
 -DFEATURE_system_png=ON \
 -DFEATURE_system_zlib=ON \
 %{?ibase:-DFEATURE_sql_ibase=ON} \
 -DFEATURE_sql_odbc=ON \
 -DFEATURE_sql_mysql=ON \
 -DFEATURE_sql_psql=ON \
 -DFEATURE_sql_sqlite=ON \
 -DFEATURE_rpath=OFF \
 -DFEATURE_zstd=ON \
 -DFEATURE_elf_private_full_version=ON \
 %{?dbus_linked:-DFEATURE_dbus_linked=ON} \
 %{?pcre:-DFEATURE_system_pcre2=ON} \
 %{?sqlite:-DFEATURE_system_sqlite=ON} \
 -DBUILD_SHARED_LIBS=ON \
 -DQT_BUILD_EXAMPLES=%{?examples:ON}%{!?examples:OFF} \
 -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF} \
 -DQT_BUILD_TESTS=%{?tests:ON}%{!?tests:OFF} \
 -DQT_QMAKE_TARGET_MKSPEC=%{platform}

%cmake_build


%install
%cmake_install

install -m644 -p -D %{SOURCE1} %{buildroot}%{_qt6_datadir}/qtlogging.ini

# Qt6.pc
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat << EOF > %{buildroot}%{_libdir}/pkgconfig/Qt6.pc
prefix=%{_qt6_prefix}
archdatadir=%{_qt6_archdatadir}
bindir=%{_qt6_bindir}
datadir=%{_qt6_datadir}

docdir=%{_qt6_docdir}
examplesdir=%{_qt6_examplesdir}
headerdir=%{_qt6_headerdir}
importdir=%{_qt6_importdir}
libdir=%{_qt6_libdir}
libexecdir=%{_qt6_libexecdir}
moc=%{_qt6_libexecdir}/moc
plugindir=%{_qt6_plugindir}
qmake=%{_qt6_bindir}/qmake
settingsdir=%{_qt6_settingsdir}
sysconfdir=%{_qt6_sysconfdir}
translationdir=%{_qt6_translationdir}

Name: Qt6
Description: Qt6 Configuration
Version: 6.10.2
EOF

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{_rpmmacrodir}/macros.qt6-qtbase
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{_rpmmacrodir}/macros.qt6-qtbase

# create/own dirs
mkdir -p %{buildroot}%{_qt6_plugindir}/{designer,iconengines,script,styles}
mkdir -p %{buildroot}%{_sysconfdir}/xdg/QtProject

# hardlink files to {_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
    qdbuscpp2xml|qdbusxml2cpp|qtpaths)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd


%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt6_headerdir}/QtCore/qconfig.h %{buildroot}%{_qt6_headerdir}/QtCore/qconfig-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt6_headerdir}/QtCore/qconfig.h
%endif


## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

install -p -m755 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt6-check-opengl2.sh

# install privat headers for qtxcb
mkdir -p %{buildroot}%{_qt6_headerdir}/QtXcb
install -m 644 src/plugins/platforms/xcb/*.h %{buildroot}%{_qt6_headerdir}/QtXcb/

# Copied from OpenSUSE packages

# These files are only useful for the Qt continuous integration
rm %{buildroot}%{_qt6_libexecdir}/ensure_pro_file.cmake
rm %{buildroot}%{_qt6_libexecdir}/qt-android-runner.py
rm %{buildroot}%{_qt6_libexecdir}/qt-testrunner.py
rm %{buildroot}%{_qt6_libexecdir}/sanitizer-testrunner.py

# Not useful for desktop installs
rm -r %{buildroot}%{_qt6_libdir}/cmake/Qt6ExamplesAssetDownloaderPrivate
rm -r %{buildroot}%{_qt6_headerdir}/QtExamplesAssetDownloader
rm %{buildroot}%{_qt6_descriptionsdir}/ExamplesAssetDownloaderPrivate.json
rm %{buildroot}%{_qt6_libdir}/libQt6ExamplesAssetDownloader.*
rm %{buildroot}%{_qt6_libdir}/qt6/metatypes/qt6examplesassetdownloaderprivate_metatypes.json

# These shouldn't be probably installed
rm -r %{buildroot}%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/*.patch

# This is only for Apple platforms and has a python2 dep
rm -r %{buildroot}%{_qt6_mkspecsdir}/features/uikit


%check
# verify Qt6.pc
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion Qt6)" = "%{qt_version}"
%if 0%{?tests}
## see tests/README for expected environment (running a plasma session essentially)
## we are not quite there yet
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt6_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt6_libdir}
# dbus tests error out when building if session bus is not available
dbus-launch --exit-with-session \
%make_build sub-tests  -k ||:
wlheadless-run -c %{wlheadless_compositor} -- \
dbus-launch --exit-with-session \
time \
make check -k ||:
%endif

%ldconfig_scriptlets

%files
%license LICENSES/GPL*
%license LICENSES/LGPL*
%dir %{_sysconfdir}/xdg/QtProject/
%{_qt6_archdatadir}/sbom/qtbase-%{qt_version}.spdx
%{_qt6_libdir}/libQt6Concurrent.so.6*
%{_qt6_libdir}/libQt6Core.so.6*
%{_qt6_libdir}/libQt6DBus.so.6*
%{_qt6_libdir}/libQt6Network.so.6*
%{_qt6_libdir}/libQt6Sql.so.6*
%{_qt6_libdir}/libQt6Test.so.6*
%{_qt6_libdir}/libQt6Xml.so.6*
%{_qt6_docdir}/global/
%{_qt6_docdir}/config/
%{_qt6_datadir}/qtlogging.ini
%dir %{_qt6_plugindir}/designer/
%dir %{_qt6_plugindir}/generic/
%dir %{_qt6_plugindir}/iconengines/
%dir %{_qt6_plugindir}/imageformats/
%dir %{_qt6_plugindir}/networkinformation/
%dir %{_qt6_plugindir}/platforminputcontexts/
%dir %{_qt6_plugindir}/platforms/
%dir %{_qt6_plugindir}/platformthemes/
%dir %{_qt6_plugindir}/printsupport/
%dir %{_qt6_plugindir}/script/
%dir %{_qt6_plugindir}/sqldrivers/
%dir %{_qt6_plugindir}/styles/
%dir %{_qt6_plugindir}/tls/
%{_qt6_plugindir}/networkinformation/libqglib.so
%{_qt6_plugindir}/networkinformation/libqnetworkmanager.so
%{_qt6_plugindir}/sqldrivers/libqsqlite.so
%{_qt6_plugindir}/tls/libqcertonlybackend.so
%{_qt6_plugindir}/tls/libqopensslbackend.so
%{_bindir}/qtpaths*
%{_qt6_bindir}/qtpaths*

%files common
# mostly empty for now, consider: filesystem/dir ownership, licenses
%{_rpmmacrodir}/macros.qt6-qtbase

%files devel
%dir %{_qt6_libdir}/cmake/Qt6
%dir %{_qt6_libdir}/cmake/Qt6/libexec
%dir %{_qt6_libdir}/cmake/Qt6/platforms
%dir %{_qt6_libdir}/cmake/Qt6/platforms/Platform
%dir %{_qt6_libdir}/cmake/Qt6/config.tests
%dir %{_qt6_libdir}/cmake/Qt6/3rdparty
%dir %{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules
%dir %{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/find-modules
%dir %{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/modules
%dir %{_qt6_libdir}/cmake/Qt6/3rdparty/kwin
%dir %{_qt6_libdir}/cmake/Qt6BuildInternals
%dir %{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests
%dir %{_qt6_libdir}/cmake/Qt6BuildInternals/QtStandaloneTestTemplateProject
%dir %{_qt6_libdir}/cmake/Qt6Concurrent
%dir %{_qt6_libdir}/cmake/Qt6Core
%dir %{_qt6_libdir}/cmake/Qt6CoreTools
%dir %{_qt6_libdir}/cmake/Qt6DBus
%dir %{_qt6_libdir}/cmake/Qt6DBusTools
%dir %{_qt6_libdir}/cmake/Qt6Gui
%dir %{_qt6_libdir}/cmake/Qt6GuiTools
%dir %{_qt6_libdir}/cmake/Qt6HostInfo
%dir %{_qt6_libdir}/cmake/Qt6Network
%dir %{_qt6_libdir}/cmake/Qt6OpenGL
%dir %{_qt6_libdir}/cmake/Qt6OpenGLWidgets
%dir %{_qt6_libdir}/cmake/Qt6PrintSupport
%dir %{_qt6_libdir}/cmake/Qt6Sql
%dir %{_qt6_libdir}/cmake/Qt6Test
%dir %{_qt6_libdir}/cmake/Qt6WaylandClient/
%dir %{_qt6_libdir}/cmake/Qt6WaylandClientPrivate
%dir %{_qt6_libdir}/cmake/Qt6WaylandGlobalPrivate/
%dir %{_qt6_libdir}/cmake/Qt6WaylandScannerTools/
%dir %{_qt6_libdir}/cmake/Qt6WlShellIntegrationPrivate/
%dir %{_qt6_libdir}/cmake/Qt6Widgets
%dir %{_qt6_libdir}/cmake/Qt6WidgetsTools
%dir %{_qt6_libdir}/cmake/Qt6Xml
%{_bindir}/androiddeployqt
%{_bindir}/androiddeployqt6
%{_bindir}/androidtestrunner
%{_bindir}/qdbuscpp2xml*
%{_bindir}/qdbusxml2cpp*
%{_bindir}/qmake*
%{_bindir}/qt-cmake
%{_bindir}/qt-cmake-create
%{_bindir}/qt-configure-module
%{_libdir}/qt6/bin/qmake6
%{_qt6_bindir}/androiddeployqt
%{_qt6_bindir}/androiddeployqt6
%{_qt6_bindir}/androidtestrunner
%{_qt6_bindir}/qdbuscpp2xml
%{_qt6_bindir}/qdbusxml2cpp
%{_qt6_bindir}/qmake
%{_qt6_bindir}/qt-cmake
%{_qt6_bindir}/qt-cmake-create
%{_qt6_bindir}/qt-configure-module
%{_qt6_libexecdir}/qt-cmake-private
%{_qt6_libexecdir}/qt-cmake-private-install.cmake
%{_qt6_libexecdir}/qt-cmake-standalone-test
%{_qt6_libexecdir}/cmake_automoc_parser
%{_qt6_libexecdir}/qt-internal-configure-examples
%{_qt6_libexecdir}/qt-internal-configure-tests
%{_qt6_libexecdir}/syncqt
%{_qt6_libexecdir}/moc
%{_qt6_libexecdir}/tracegen
%{_qt6_libexecdir}/tracepointgen
%{_qt6_libexecdir}/qlalr
%{_qt6_libexecdir}/qt_cyclonedx_generator.py
%{_qt6_libexecdir}/qvkgen
%{_qt6_libexecdir}/rcc
%{_qt6_libexecdir}/uic
%{_qt6_libexecdir}/qtwaylandscanner
%{_qt6_headerdir}/QtConcurrent/
%{_qt6_headerdir}/QtCore/
%{_qt6_headerdir}/QtDBus/
%{_qt6_headerdir}/QtGui/
%{_qt6_headerdir}/QtNetwork/
%{_qt6_headerdir}/QtOpenGL/
%{_qt6_headerdir}/QtOpenGLWidgets
%{_qt6_headerdir}/QtPrintSupport/
%{_qt6_headerdir}/QtSql/
%{_qt6_headerdir}/QtTest/
%{_qt6_headerdir}/QtWaylandClient/
%{_qt6_headerdir}/QtWaylandGlobal/
%{_qt6_headerdir}/QtWlShellIntegration/
%{_qt6_headerdir}/QtWidgets/
%{_qt6_headerdir}/QtXcb/
%{_qt6_headerdir}/QtXml/
%{_qt6_libdir}/libQt6Concurrent.prl
%{_qt6_libdir}/libQt6Concurrent.so
%{_qt6_libdir}/libQt6Core.prl
%{_qt6_libdir}/libQt6Core.so
%{_qt6_libdir}/libQt6DBus.prl
%{_qt6_libdir}/libQt6DBus.so
%{_qt6_libdir}/libQt6Gui.prl
%{_qt6_libdir}/libQt6Gui.so
%{_qt6_libdir}/libQt6Network.prl
%{_qt6_libdir}/libQt6Network.so
%{_qt6_libdir}/libQt6OpenGL.prl
%{_qt6_libdir}/libQt6OpenGL.so
%{_qt6_libdir}/libQt6OpenGLWidgets.prl
%{_qt6_libdir}/libQt6OpenGLWidgets.so
%{_qt6_libdir}/libQt6PrintSupport.prl
%{_qt6_libdir}/libQt6PrintSupport.so
%{_qt6_libdir}/libQt6Sql.prl
%{_qt6_libdir}/libQt6Sql.so
%{_qt6_libdir}/libQt6Test.prl
%{_qt6_libdir}/libQt6Test.so
%{_qt6_libdir}/libQt6WaylandClient.so
%{_qt6_libdir}/libQt6WlShellIntegration.so
%{_qt6_libdir}/libQt6WaylandClient.prl
%{_qt6_libdir}/libQt6WlShellIntegration.prl
%{_qt6_libdir}/libQt6Widgets.prl
%{_qt6_libdir}/libQt6Widgets.so
%{_qt6_libdir}/libQt6XcbQpa.prl
%{_qt6_libdir}/libQt6XcbQpa.so
%{_qt6_libdir}/libQt6Xml.prl
%{_qt6_libdir}/libQt6Xml.so
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/REUSE.toml
%{_qt6_libdir}/cmake/Qt6/3rdparty/kwin/REUSE.toml
%{_qt6_libdir}/cmake/Qt6/*.in
%{_qt6_libdir}/cmake/Qt6/*.h.in
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6/*.cmake.in
%{_qt6_libdir}/cmake/Qt6/PkgConfigLibrary.pc.in
%{_qt6_libdir}/cmake/Qt6/config.tests/*
%{_qt6_libdir}/cmake/Qt6/libexec/*
%{_qt6_libdir}/cmake/Qt6/platforms/*.cmake
%{_qt6_libdir}/cmake/Qt6/platforms/Platform/*.cmake
%{_qt6_libdir}/cmake/Qt6/qbatchedtestrunner.in.cpp
%{_qt6_libdir}/cmake/Qt6/ModuleDescription.json.in
%{_qt6_libdir}/cmake/Qt6/QtFileConfigure.txt.in
%{_qt6_libdir}/cmake/Qt6/QtConfigureTimeExecutableCMakeLists.txt.in
%{_qt6_libdir}/cmake/Qt6/QtSeparateDebugInfo.Info.plist.in
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/COPYING-CMAKE-SCRIPTS
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/find-modules/*.cmake
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/modules/*.cmake
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/qt_attribution.json
%{_qt6_libdir}/cmake/Qt6/3rdparty/kwin/COPYING-CMAKE-SCRIPTS
%{_qt6_libdir}/cmake/Qt6/3rdparty/kwin/*.cmake
%{_qt6_libdir}/cmake/Qt6/3rdparty/kwin/qt_attribution.json
%{_qt6_libdir}/cmake/Qt6BuildInternals/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/QtStandaloneTestTemplateProject/CMakeLists.txt
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtBaseTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/QtStandaloneTestTemplateProject/Main.cmake
%{_qt6_libdir}/cmake/Qt6Concurrent/*.cmake
%{_qt6_libdir}/cmake/Qt6Core/*.cmake
%{_qt6_libdir}/cmake/Qt6Core/Qt6CoreResourceInit.in.cpp
%{_qt6_libdir}/cmake/Qt6Core/Qt6CoreConfigureFileTemplate.in
%{_qt6_libdir}/cmake/Qt6CoreTools/*.cmake
%{_qt6_libdir}/cmake/Qt6DBus/*.cmake
%{_qt6_libdir}/cmake/Qt6DBusTools/*.cmake
%{_qt6_libdir}/cmake/Qt6Gui/*.cmake
%{_qt6_libdir}/cmake/Qt6GuiTools/*.cmake
%{_qt6_libdir}/cmake/Qt6HostInfo/*.cmake
%{_qt6_libdir}/cmake/Qt6Network/*.cmake
%{_qt6_libdir}/cmake/Qt6OpenGL/*.cmake
%{_qt6_libdir}/cmake/Qt6OpenGLWidgets/*.cmake
%{_qt6_libdir}/cmake/Qt6PrintSupport/*.cmake
%{_qt6_libdir}/cmake/Qt6Sql/Qt6Sql*.cmake
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QSQLiteDriverPlugin*.cmake
%{_qt6_libdir}/cmake/Qt6Test/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandClient/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandClientPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandGlobalPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WaylandScannerTools/*.cmake
%{_qt6_libdir}/cmake/Qt6WlShellIntegrationPrivate/
%{_qt6_libdir}/cmake/Qt6Widgets/*.cmake
%{_qt6_libdir}/cmake/Qt6WidgetsTools/*.cmake
%{_qt6_libdir}/cmake/Qt6Xml/*.cmake
%{_qt6_descriptionsdir}/Concurrent.json
%{_qt6_descriptionsdir}/Core.json
%{_qt6_descriptionsdir}/DBus.json
%{_qt6_descriptionsdir}/Gui.json
%{_qt6_descriptionsdir}/Network.json
%{_qt6_descriptionsdir}/OpenGL.json
%{_qt6_descriptionsdir}/OpenGLWidgets.json
%{_qt6_descriptionsdir}/PrintSupport.json
%{_qt6_descriptionsdir}/Sql.json
%{_qt6_descriptionsdir}/Test.json
%{_qt6_descriptionsdir}/WaylandClient.json
%{_qt6_descriptionsdir}/WaylandGlobalPrivate.json
%{_qt6_descriptionsdir}/WlShellIntegrationPrivate.json
%{_qt6_descriptionsdir}/Widgets.json
%{_qt6_descriptionsdir}/Xml.json
%{_qt6_metatypesdir}/qt6concurrent_metatypes.json
%{_qt6_metatypesdir}/qt6core_metatypes.json
%{_qt6_metatypesdir}/qt6dbus_metatypes.json
%{_qt6_metatypesdir}/qt6gui_metatypes.json
%{_qt6_metatypesdir}/qt6network_metatypes.json
%{_qt6_metatypesdir}/qt6opengl_metatypes.json
%{_qt6_metatypesdir}/qt6openglwidgets_metatypes.json
%{_qt6_metatypesdir}/qt6printsupport_metatypes.json
%{_qt6_metatypesdir}/qt6sql_metatypes.json
%{_qt6_metatypesdir}/qt6test_metatypes.json
%{_qt6_metatypesdir}/qt6widgets_metatypes.json
%{_qt6_metatypesdir}/qt6xml_metatypes.json
%{_qt6_libdir}/pkgconfig/*.pc
%{_qt6_mkspecsdir}/*
## private-devel globs
%exclude %{_qt6_headerdir}/*/%{qt_version}/

%files private-devel
%{_qt6_headerdir}/QtEglFSDeviceIntegration
%{_qt6_headerdir}/QtEglFsKmsGbmSupport
%{_qt6_headerdir}/QtEglFsKmsSupport
%dir %{_qt6_libdir}/cmake/Qt6CorePrivate
%dir %{_qt6_libdir}/cmake/Qt6DBusPrivate
%dir %{_qt6_libdir}/cmake/Qt6GuiPrivate
%dir %{_qt6_libdir}/cmake/Qt6NetworkPrivate
%dir %{_qt6_libdir}/cmake/Qt6OpenGLPrivate
%dir %{_qt6_libdir}/cmake/Qt6PrintSupportPrivate
%dir %{_qt6_libdir}/cmake/Qt6SqlPrivate
%dir %{_qt6_libdir}/cmake/Qt6TestInternalsPrivate
%dir %{_qt6_libdir}/cmake/Qt6TestInternalsPrivate/3rdparty/cmake
%dir %{_qt6_libdir}/cmake/Qt6TestPrivate
%dir %{_qt6_libdir}/cmake/Qt6WidgetsPrivate
%dir %{_qt6_libdir}/cmake/Qt6XmlPrivate
%dir %{_qt6_libdir}/cmake/Qt6EglFSDeviceIntegrationPrivate
%dir %{_qt6_libdir}/cmake/Qt6EglFsKmsGbmSupportPrivate
%dir %{_qt6_libdir}/cmake/Qt6EglFsKmsSupportPrivate
%dir %{_qt6_libdir}/cmake/Qt6XcbQpaPrivate
%{_qt6_libdir}/cmake/Qt6CorePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6DBusPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6GuiPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6NetworkPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6OpenGLPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6PrintSupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6SqlPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6TestInternalsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6TestInternalsPrivate/3rdparty/cmake/*.cmake
%{_qt6_libdir}/cmake/Qt6TestPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6WidgetsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6XmlPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6EglFSDeviceIntegrationPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6EglFsKmsGbmSupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6EglFsKmsSupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6XcbQpaPrivate/*.cmake
%if 0%{?egl}
%{_qt6_libdir}/libQt6EglFsKmsSupport.prl
%{_qt6_libdir}/libQt6EglFsKmsSupport.so
%endif
%{_qt6_libdir}/libQt6EglFSDeviceIntegration.prl
%{_qt6_libdir}/libQt6EglFSDeviceIntegration.so
%{_qt6_libdir}/libQt6EglFsKmsGbmSupport.prl
%{_qt6_libdir}/libQt6EglFsKmsGbmSupport.so
%{_qt6_descriptionsdir}/EglFSDeviceIntegrationPrivate.json
%{_qt6_descriptionsdir}/EglFsKmsGbmSupportPrivate.json
%{_qt6_descriptionsdir}/EglFsKmsSupportPrivate.json
%{_qt6_descriptionsdir}/XcbQpaPrivate.json
%{_qt6_metatypesdir}/qt6eglfsdeviceintegrationprivate_metatypes.json
%{_qt6_metatypesdir}/qt6eglfskmsgbmsupportprivate_metatypes.json
%{_qt6_metatypesdir}/qt6eglfskmssupportprivate_metatypes.json
%{_qt6_metatypesdir}/qt6xcbqpaprivate_metatypes.json
%{_qt6_metatypesdir}/qt6waylandclient_metatypes.json
%{_qt6_metatypesdir}/qt6wlshellintegrationprivate_metatypes.json
%{_qt6_headerdir}/*/%{qt_version}/
%{_qt6_descriptionsdir}/TestInternalsPrivate.json

%files static
%dir %{_qt6_libdir}/cmake/Qt6ExampleIconsPrivate
%{_qt6_libdir}/cmake/Qt6ExampleIconsPrivate/*.cmake
%{_qt6_headerdir}/QtExampleIcons
%{_qt6_libdir}/libQt6ExampleIcons.a
%{_qt6_libdir}/libQt6ExampleIcons.prl
%{_qt6_descriptionsdir}/ExampleIconsPrivate.json
%dir %{_qt6_archdatadir}/objects-*
%{_qt6_archdatadir}/objects-*/ExampleIconsPrivate_resources_1/
%{_qt6_metatypesdir}/qt6exampleiconsprivate_metatypes.json
%dir %{_qt6_libdir}/cmake/Qt6DeviceDiscoverySupportPrivate
%{_qt6_libdir}/cmake/Qt6DeviceDiscoverySupportPrivate/*.cmake
%{_qt6_headerdir}/QtDeviceDiscoverySupport
%{_qt6_libdir}/libQt6DeviceDiscoverySupport.*a
%{_qt6_libdir}/libQt6DeviceDiscoverySupport.prl
%{_qt6_descriptionsdir}/DeviceDiscoverySupportPrivate.json
%{_qt6_metatypesdir}/qt6devicediscoverysupportprivate_metatypes.json
%dir %{_qt6_libdir}/cmake/Qt6FbSupportPrivate
%{_qt6_libdir}/cmake/Qt6FbSupportPrivate/*.cmake
%{_qt6_headerdir}/QtFbSupport
%{_qt6_libdir}/libQt6FbSupport.*a
%{_qt6_libdir}/libQt6FbSupport.prl
%{_qt6_descriptionsdir}/FbSupportPrivate.json
%{_qt6_metatypesdir}/qt6fbsupportprivate_metatypes.json
%dir %{_qt6_libdir}/cmake/Qt6InputSupportPrivate
%{_qt6_libdir}/cmake/Qt6InputSupportPrivate/*.cmake
%{_qt6_headerdir}/QtInputSupport
%{_qt6_libdir}/libQt6InputSupport.*a
%{_qt6_libdir}/libQt6InputSupport.prl
%{_qt6_descriptionsdir}/InputSupportPrivate.json
%{_qt6_metatypesdir}/qt6inputsupportprivate_metatypes.json
%dir %{_qt6_libdir}/cmake/Qt6KmsSupportPrivate
%{_qt6_libdir}/cmake/Qt6KmsSupportPrivate/*.cmake
%{_qt6_headerdir}/QtKmsSupport
%{_qt6_libdir}/libQt6KmsSupport.*a
%{_qt6_libdir}/libQt6KmsSupport.prl
%{_qt6_descriptionsdir}/KmsSupportPrivate.json
%{_qt6_metatypesdir}/qt6kmssupportprivate_metatypes.json

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

%if 0%{?ibase}
%files ibase
%{_qt6_plugindir}/sqldrivers/libqsqlibase.so
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QIBaseDriverPlugin*.cmake
%endif

%files mysql
%{_qt6_plugindir}/sqldrivers/libqsqlmysql.so
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QMYSQLDriverPlugin*.cmake

%files odbc
%{_qt6_plugindir}/sqldrivers/libqsqlodbc.so
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QODBCDriverPlugin*.cmake

%files postgresql
%{_qt6_plugindir}/sqldrivers/libqsqlpsql.so
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QPSQLDriverPlugin*.cmake

%ldconfig_scriptlets gui

%files gui
%dir %{_sysconfdir}/X11/xinit
%dir %{_sysconfdir}/X11/xinit/xinitrc.d/
%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt6-check-opengl2.sh
%{_qt6_libdir}/libQt6Gui.so.6*
%{_qt6_libdir}/libQt6OpenGL.so.6*
%{_qt6_libdir}/libQt6OpenGLWidgets.so.6*
%{_qt6_libdir}/libQt6PrintSupport.so.6*
%{_qt6_libdir}/libQt6WaylandClient.so.6*
%{_qt6_libdir}/libQt6WlShellIntegration.so.6*
%{_qt6_libdir}/libQt6Widgets.so.6*
%{_qt6_libdir}/libQt6XcbQpa.so.6*
# Generic
%{_qt6_plugindir}/generic/libqevdevkeyboardplugin.so
%{_qt6_plugindir}/generic/libqevdevmouseplugin.so
%{_qt6_plugindir}/generic/libqevdevtabletplugin.so
%{_qt6_plugindir}/generic/libqevdevtouchplugin.so
%{_qt6_plugindir}/generic/libqlibinputplugin.so
%if 0%{?fedora} || 0%{?epel}
%{_qt6_plugindir}/generic/libqtslibplugin.so
%endif
%{_qt6_plugindir}/generic/libqtuiotouchplugin.so
# Imageformats
%{_qt6_plugindir}/imageformats/libqico.so
%{_qt6_plugindir}/imageformats/libqjpeg.so
%{_qt6_plugindir}/imageformats/libqgif.so
# Platforminputcontexts
%{_qt6_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%{_qt6_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so
# EGL
%if 0%{?egl}
%{_qt6_libdir}/libQt6EglFSDeviceIntegration.so.6*
%{_qt6_libdir}/libQt6EglFsKmsSupport.so.6*
%{_qt6_libdir}/libQt6EglFsKmsGbmSupport.so.6*
%{_qt6_plugindir}/platforms/libqeglfs.so
%{_qt6_plugindir}/platforms/libqminimalegl.so
%dir %{_qt6_plugindir}/egldeviceintegrations/
%{_qt6_plugindir}/egldeviceintegrations/libqeglfs-kms-integration.so
%{_qt6_plugindir}/egldeviceintegrations/libqeglfs-x11-integration.so
%{_qt6_plugindir}/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so
%{_qt6_plugindir}/egldeviceintegrations/libqeglfs-emu-integration.so
%dir %{_qt6_plugindir}/xcbglintegrations/
%{_qt6_plugindir}/xcbglintegrations/libqxcb-egl-integration.so
%endif
# Platforms
%{_qt6_plugindir}/platforms/libqlinuxfb.so
%{_qt6_plugindir}/platforms/libqminimal.so
%{_qt6_plugindir}/platforms/libqoffscreen.so
%{_qt6_plugindir}/platforms/libqvnc.so
%{_qt6_plugindir}/platforms/libqvkkhrdisplay.so
%{_qt6_plugindir}/platforms/libqwayland.so
%{_qt6_plugindir}/platforms/libqxcb.so
%{_qt6_plugindir}/xcbglintegrations/libqxcb-glx-integration.so
%{_qt6_plugindir}/printsupport/libcupsprintersupport.so
# Platformthemes
%{_qt6_plugindir}/platformthemes/libqxdgdesktopportal.so
%{_qt6_plugindir}/platformthemes/libqgtk3.so
# Wayland plugins and protocols
%{_qt6_plugindir}/wayland-decoration-client/
%{_qt6_plugindir}/wayland-graphics-integration-client
%{_qt6_plugindir}/wayland-shell-integration
%{_qt6_datadir}/wayland/extensions/
%{_qt6_datadir}/wayland/protocols/

%changelog
* Sun Feb 15 2026 Yaakov Selkowitz <yselkowi@redhat.com> - 6.10.2-2
- Add wayland-devel dependencies for cmake(Qt6WaylandClient)

* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Dec 22 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-3
- Fix crash in QWaylandShmBackingStore::scroll()

* Mon Dec 08 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-2
- Re-add wayland fixes for mouse scrolling

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Mon Nov 10 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-3
- Backport wayland fixes for mouse scrolling

* Wed Oct 29 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-2
- Backport: Wayland - convey preference for server side decorations

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Tue Sep 30 2025 Gwyn Ciesla <gwync@protonmail.com> - 6.10.0~rc-2
- Firebird 5 rebuild

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Thu Aug 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Tue Aug 05 2025 František Zatloukal <fzatlouk@redhat.com> - 6.9.1-4
- Rebuilt for icu 77.1

* Mon Jul 28 2025 Adam Williamson <awilliam@redhat.com> - 6.9.1-3
- Adjust for https://fedoraproject.org/wiki/Changes/dropingOfCertPemFile removals

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Mon Apr 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-2
- Fix possible crash in FontConfig database

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Fri Mar 21 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0 RC

* Thu Feb 13 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-3
- Fix rendering of combined emojis

* Thu Feb 06 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-2
- Backport recommended fixes for Qt 6.8.2

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Thu Jan 16 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.1-11
- Backport additional fixes for emoji support

* Mon Jan 13 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.1-10
- Fix directory ownership for 3rdparty cmake plugins

* Thu Jan 09 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.1-9
- Fix directory ownership
  Resolves: rhbz#2292582

* Wed Jan 08 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.1-8
- Install CMake modules for plugins

* Tue Dec 17 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-7
- Fix QGnomePlatform obsolets

* Mon Dec 16 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-6
- Backport additional fixes for emoji support

* Tue Dec 10 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-5
- Obsolete QGnomePlatform and AdwaitaQt

* Sat Dec 07 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-4
- Move all mkspecs to -devel

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-3
- Move more stuff into -private-devel

* Tue Dec 03 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-2
- Do not install ExamplesAssetDownloader

* Thu Nov 28 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
- 6.8.1

* Mon Oct 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-4
- Backport - a11y atspi: Watch for enabled status change

* Wed Oct 16 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-3
- QtPrintSupport: make cups optional target

* Wed Oct 09 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- Backport fix for QAbstractItemModel (kdebz#493116)

* Wed Oct 09 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Wed Sep 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-6
- Backport - QWidget: store initialScreen as QPointer

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-4
- Use qt6-filesystem

* Mon Jul 08 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-3
- HTTP2: Delay any communication until encrypted() can be responded to
  Resolves: CVE-2024-39936

* Wed Jul 03 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-2
- Revert: Consider versioned targets when checking the existens in
  __qt_internal_walk_libs

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-2
- Use only major.minor version for private api tag

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Tue May 07 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-5
- QGtk3Theme: Add support for xdg-desktop-portal to get color scheme

* Wed Apr 24 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-4
- Use bundled double-conversion in RHEL builds

* Fri Apr 12 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-3
- Rebuild (gcc rhbz#2272758)

* Mon Apr 08 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-2
- Upstream backport: Use ifdef instead of if for __cpp_lib_span

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Sat Mar 09 2024 Alessandro Astone <ales.astone@gmail.com> - 6.6.2-6
- Move /usr/bin/qtpaths-qt6 to main package

* Fri Mar 01 2024 David Abdurachmanov <davidlt@rivosinc.com> - 6.6.2-5
- Disable SSE2 on riscv64

* Fri Feb 23 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.6.2-4
- Use wlheadless-run for tests instead of xvfb-run

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-3
- Examples: also install source files

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 6.6.1-5
- Rebuild for ICU 74

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 12 2023 Timothée Ravier <tim@siosm.fr> - 6.6.1-2
- Recommend qt6-qttranslations

* Mon Nov 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Fri Nov 10 2023 Alessandro Astone <ales.astone@gmail.com> - 6.6.0-7
- Add xkbcommon as a devel dependency

* Thu Nov 09 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-6
- Revert: Fix Qt not showing up emoji by handling emoji font family

* Tue Nov 07 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-5
- Fix Qt not showing up emoji by handling emoji font family

* Mon Nov 06 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-4
- Upstream backports
  - a11y - fix race condition on atspi startup on Wayland

* Mon Oct 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-3
- Do not use tslib on RHEL builds

* Sun Oct 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.6.0-2
- Add qtwayland weak dep to -gui subpackage and use arched weak deps

* Tue Oct 10 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Sun Sep 03 2023 LuK1337 <priv.luk@gmail.com> - 6.5.2-5
- Unbreak CMake Qt6::ExampleIconsPrivate package

* Mon Aug 28 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.2-4
- Use bundled libb2 in RHEL builds

* Fri Aug 11 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-3
- Don't use QGnomePlatform by default on F39+

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Wed Jul 12 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-4
- Rebuilt for ICU 73.2

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Bump build for private API version change

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-2
- Rebuilt for ICU 73.2

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Fri Apr 7 2023 Marie Loise Nolden <loise@kde.org> - 6.5.0-2
- fix xcb plugin with new dependency xcb-cursor instead of Xcursor
  introduction with qt 6.5, add firebird sql plugin cleanly, clean up spec file

* Mon Apr 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Mon Apr 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-2
- Enable zstd support

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Sun Mar 05 2023 Jan grulich <jgrulich@redhat.com> - 6.4.2-5
- Use QGnomePlatform as default platform theme on GNOME
  Resolves: bz#2174905

* Wed Feb 08 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-4
- Fix possible DOS involving the Qt SQL ODBC driver plugin
  CVE-2023-24607

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- 6.4.2

* Mon Jan 02 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.1-4
- Make -devel package to require database plugins

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 6.4.1-3
- Rebuild for ICU 72

* Wed Nov 30 2022 Pavel Raiskup <praiskup@redhat.com> - 6.4.1-2
- rebuild for the new PostgreSQL 15

* Wed Nov 23 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.1-1
- 6.4.1

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 6.3.1-4
- Rebuilt for ICU 71.1

* Fri Jul 29 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-3
- Fix moc location in pkgconfig file
  Resolves: bz#2112029

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-1
- 6.3.1

* Wed Apr 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-1
- 6.3.0

* Fri Feb 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-2
- Enable s390x builds

* Mon Jan 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-1
- 6.2.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Filip Januš <fjanus@redhat.com> - 6.2.2-2
- Rebuild for Postgresql 14

* Tue Dec 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.2-1
- 6.2.2

* Fri Oct 29 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.1-1
- 6.2.1

* Thu Sep 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-1
- 6.2.0

* Mon Sep 27 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc2-1
- 6.2.0 - rc2

* Sat Sep 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 6.2.0~beta4-3
- Rebuilt with OpenSSL 3.0.0

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-2
- Skip s390x for qtdeclarative issue

* Fri Sep 10 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Wed Sep 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 6.2.0~beta3-4
- rebuild

* Tue Sep 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-3
- Disable rpath
  Resolves: bz#1982699

* Tue Aug 31 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-2
- Fix file conflict with qt5-qttools
- Rebuild against older libglvnd

* Mon Aug 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-1
- 6.2.0 - beta3

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1

* Mon May 24 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-3
- Rebuild with correct libexecdir path

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 6.1.0-2
- Rebuild for ICU 69

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-1
- 6.0.0
