# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# Disable debuginfo subpackages and debugsource packages for now to use old logic
%undefine _debugsource_packages
%undefine _debuginfo_subpackages

# Override the __debug_install_post argument as this package
# contains both native as well as cross compiled binaries
%global __debug_install_post %%{mingw_debug_install_post}; %{_bindir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%%{?buildsubdir}" %{nil}

%global qt_module qtbase
#global pre rc

#global commit d725239c3e09c2b740a093265f6a9675fd2f8524
#global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?commit:1}
%global source_folder %{qt_module}-%{commit}
%else
%global source_folder %{qt_module}-everywhere-src-%{version}%{?pre:-%{pre}}
%endif

# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           mingw-qt5-qtbase
Version:        5.15.18
Release: 2%{?dist}
Summary:        Qt5 for Windows - QtBase component

# See LGPL_EXCEPTIONS.txt, for exception details
License:        LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
URL:            http://qt.io/

%if 0%{?commit:1}
Source0:        https://github.com/qt/%{qt_module}/archive/%{commit}/%{qt_module}-everywhere-src-%{commit}.tar.gz
%else
Source0:        https://download.qt.io/archive/qt/%{release_version}/%{version}%{?pre:-%pre}/submodules/%{qt_module}-everywhere-opensource-src-%{version}%{?pre:-%pre}.tar.xz
%endif

# Add profile for for mingw to match our environment
Patch1:          qt5-qtbase-mingw-profile.patch

# Unbundle angle
Patch2:          qt5-qtbase-external-angle.patch

# Avoid conflicts between the static qtmain library and the one provided by mingw-qt4.
# The mkspecs profile is already updated by Adjust-win32-g-mkspecs-profile.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1092465
Patch3:         qt5-qtbase-qt5main.patch

# Upstream always wants the host libraries to be static instead of shared.
# This violates the packaging guidelines so disable this 'feature'.
Patch4:         qt5-qtbase-dynamic-hostlib.patch

# Fix qmake to create implibs with .dll.a extension for MinGW
Patch5:         qt5-qtbase-importlib-ext.patch

# https://github.com/Martchus/PKGBUILDs/issues/11
Patch6:         qt5-qtbase-cmake-macros.patch

# Use versioned python shebang
Patch7:         qt5-qtbase-python3.patch

# The --static flags should be used to detect static libraries with pkg-config.
# Ignore failing tests
Patch8:         qt5-qtbase-pkgconfig.patch

# Fix iconv test condition
Patch9:         qt5-qtbase-iconv.patch

# Don't use bundled zlib when cross-compiling
Patch10:        qt5-qtbase-zlib-cross.patch

# Fix linking against the static version of Qt
Patch11:        qt5-qtbase-static-linking.patch

# Fix installing pkg-config files (fixes silent errors resulting in empty pkg-config files)
Patch12:        qt5-qtbase-fix-installing-pc-files.patch

# Prevent debug library names in pkg-config files
Patch13:        qt5-qtbase-prevent-debug-library-names-in-pkg-config-files.patch

# Don't use relocatable heuristics to guess prefix when using -no-feature-relocatable (#1823118)
Patch14:        qt5-qtbase-no-relocatable.patch

# Restart spnego authentication if handles are null, even if challenge is not
# Fixes crash when authenticating twice to the same target
Patch15:        qt5-qtbase-spnego.patch

# Fix undefined references when building Qt5Bootstrap
Patch16:        qt5-qtbase-bootstrap.patch

# Fix issues building with gcc-11
Patch17:        %{name}-gcc11.patch

# Fix build with openssl-linked
Patch18:        qt5-qtbase-link-openssl.patch

# Fix missing qtsan_impl include
Patch19:        qtbase-5.15.8-fix-missing-qtsan-include.patch

# Fix linking against static harfbuzz
Patch20:        qtbase-fix-linking-against-static-harfbuzz.patch

# https://invent.kde.org/qt/qt/qtbase, kde/5.15 branch
# git diff v5.15.15-lts-lgpl..HEAD | gzip > kde-5.15-rollup-$(date +%Y%m%d).patch.gz
# patch100 in lookaside cache due to large'ish size -- rdieter
Source100: kde-5.15-rollup-20251104.patch.gz


BuildRequires:  gcc-c++
BuildRequires:  gzip
BuildRequires:  make
BuildRequires:  perl-interpreter
# For Qt5Bootstrap
BuildRequires:  pkgconfig(zlib)

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-pkg-config
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-vulkan-headers
BuildRequires:  mingw32-angleproject >= 0-0.16.git8613f49
BuildRequires:  mingw32-angleproject-static >= 0-0.16.git8613f49
BuildRequires:  mingw32-bzip2
BuildRequires:  mingw32-bzip2-static
BuildRequires:  mingw32-dbus
BuildRequires:  mingw32-dbus-static
BuildRequires:  mingw32-freetype
BuildRequires:  mingw32-freetype-static
BuildRequires:  mingw32-harfbuzz
BuildRequires:  mingw32-harfbuzz-static
BuildRequires:  mingw32-libjpeg-turbo
BuildRequires:  mingw32-libjpeg-turbo-static
BuildRequires:  mingw32-libpng
BuildRequires:  mingw32-libpng-static
BuildRequires:  mingw32-openssl
BuildRequires:  mingw32-openssl-static
BuildRequires:  mingw32-pcre2
BuildRequires:  mingw32-pcre2-static
BuildRequires:  mingw32-postgresql
BuildRequires:  mingw32-postgresql-static
BuildRequires:  mingw32-sqlite
BuildRequires:  mingw32-sqlite-static
BuildRequires:  mingw32-win-iconv
BuildRequires:  mingw32-win-iconv-static
BuildRequires:  mingw32-winpthreads
BuildRequires:  mingw32-winpthreads-static
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-zlib-static
BuildRequires:  mingw32-zstd

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-pkg-config
BuildRequires:  mingw64-dlfcn
BuildRequires:  mingw64-vulkan-headers
BuildRequires:  mingw64-angleproject >= 0-0.16.git8613f49
BuildRequires:  mingw64-angleproject-static >= 0-0.16.git8613f49
BuildRequires:  mingw64-bzip2
BuildRequires:  mingw64-bzip2-static
BuildRequires:  mingw64-dbus
BuildRequires:  mingw64-dbus-static
BuildRequires:  mingw64-freetype
BuildRequires:  mingw64-freetype-static
BuildRequires:  mingw64-harfbuzz
BuildRequires:  mingw64-harfbuzz-static
BuildRequires:  mingw64-libjpeg-turbo
BuildRequires:  mingw64-libjpeg-turbo-static
BuildRequires:  mingw64-libpng
BuildRequires:  mingw64-libpng-static
BuildRequires:  mingw64-openssl
BuildRequires:  mingw64-openssl-static
BuildRequires:  mingw64-pcre2
BuildRequires:  mingw64-pcre2-static
BuildRequires:  mingw64-postgresql
BuildRequires:  mingw64-postgresql-static
BuildRequires:  mingw64-sqlite
BuildRequires:  mingw64-sqlite-static
BuildRequires:  mingw64-win-iconv
BuildRequires:  mingw64-win-iconv-static
BuildRequires:  mingw64-winpthreads
BuildRequires:  mingw64-winpthreads-static
BuildRequires:  mingw64-zlib
BuildRequires:  mingw64-zlib-static
BuildRequires:  mingw64-zstd


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt5-qtbase
Summary:        Qt5 for Windows - QtBase component
# This package contains the cross-compiler setup for qmake
Requires:       mingw32-qt5-qmake = %{version}-%{release}
# Public headers require vulkan/vulkan.h
Requires:       mingw32-vulkan-headers
BuildArch:      noarch

%description -n mingw32-qt5-qtbase
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%package -n mingw32-qt5-qmake
Summary:       Qt5 for Windows build environment

%description -n mingw32-qt5-qmake
This package contains the build environment for cross compiling
applications with the Fedora Windows Qt Library and cross-compiler.


%package -n mingw32-qt5-qtbase-devel
Summary:       Qt5 for Windows build environment
Requires:      mingw32-qt5-qtbase = %{version}-%{release}

%description -n mingw32-qt5-qtbase-devel
Contains the files required to get various Qt tools built
which are part of the mingw-qt5-qttools package


%package -n mingw32-qt5-qtbase-static
Summary:       Static version of the mingw32-qt5-qtbase library
Requires:      mingw32-qt5-qtbase = %{version}-%{release}
Requires:      mingw32-angleproject-static
Requires:      mingw32-libjpeg-turbo-static
Requires:      mingw32-libpng-static
Requires:      mingw32-harfbuzz-static
Requires:      mingw32-pcre2-static
Requires:      mingw32-win-iconv-static
Requires:      mingw32-winpthreads-static
Requires:      mingw32-zlib-static
BuildArch:     noarch

%description -n mingw32-qt5-qtbase-static
Static version of the mingw32-qt5 library.


# Win64
%package -n mingw64-qt5-qtbase
Summary:        Qt5 for Windows - QtBase component
# This package contains the cross-compiler setup for qmake
Requires:       mingw64-qt5-qmake = %{version}-%{release}
# Public headers require vulkan/vulkan.h
Requires:       mingw64-vulkan-headers
BuildArch:      noarch

%description -n mingw64-qt5-qtbase
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


%package -n mingw64-qt5-qmake
Summary:       Qt for Windows build environment

%description -n mingw64-qt5-qmake
This package contains the build environment for cross compiling
applications with the Fedora Windows Qt Library and cross-compiler.


%package -n mingw64-qt5-qtbase-devel
Summary:       Qt5 for Windows build environment
Requires:      mingw64-qt5-qtbase = %{version}-%{release}

%description -n mingw64-qt5-qtbase-devel
Contains the files required to get various Qt tools built
which are part of the mingw-qt5-qttools package


%package -n mingw64-qt5-qtbase-static
Summary:       Static version of the mingw64-qt5-qtbase library
Requires:      mingw64-qt5-qtbase = %{version}-%{release}
Requires:      mingw64-angleproject-static
Requires:      mingw64-libjpeg-turbo-static
Requires:      mingw64-libpng-static
Requires:      mingw64-harfbuzz-static
Requires:      mingw64-pcre2-static
Requires:      mingw64-win-iconv-static
Requires:      mingw64-winpthreads-static
Requires:      mingw64-zlib-static
BuildArch:     noarch

%description -n mingw64-qt5-qtbase-static
Static version of the mingw64-qt5-qtbase library.


%{?mingw_debug_package}


%prep
%autosetup -N -n %{source_folder}
%autopatch -M 100 -p1

gunzip -c %SOURCE100 | patch -p1

# Remove bundled ANGLE
rm -rf src/3rdparty/angle include/QtANGLE/{EGL,GLES2,KHR}
# Remove bundled libraries
rm -rf src/3rdparty/{freetype,libjpeg,libpng,pcre2,sqlite,zlib}
# TODO harfbuzz,harfbuzz-ng


%build
# RPM automatically sets the environment variable PKG_CONFIG_PATH to point to
# the native pkg-config files, which we don't want when cross-compiling.
unset PKG_CONFIG_PATH

# Generic configure arguments
qt_configure_args_generic="\
    -xplatform mingw-w64-g++ \
    -verbose \
    -opensource \
    -confirm-license \
    -release \
    -force-debug-info \
    -make tools \
    -nomake examples \
    -pkg-config \
    -sql-sqlite \
    -openssl-linked \
    -iconv \
    -opengl dynamic\
    -no-direct2d \
    -no-feature-relocatable \
    -system-freetype \
    -system-harfbuzz \
    -system-libjpeg \
    -system-libpng \
    -system-pcre \
    -system-sqlite \
    -system-zlib"

# The odd paths for the -hostbindir argument are on purpose.
# The qtchooser tool assumes that the tools 'qmake', 'moc' and others are all
# available in the same folder with these exact file names.
# Put these in a dedicated folder to prevent conflicts with the mingw-qt (Qt4).
qt_configure_args_win32="\
    -hostprefix %{_prefix}/%{mingw32_target} \
    -hostbindir %{_prefix}/%{mingw32_target}/bin/qt5 \
    -hostlibdir %{_prefix}/%{mingw32_target}/lib \
    -hostdatadir %{mingw32_datadir}/qt5 \
    -prefix %{mingw32_prefix} \
    -bindir %{mingw32_bindir} \
    -archdatadir %{mingw32_libdir}/qt5 \
    -datadir %{mingw32_datadir}/qt5 \
    -docdir %{mingw32_docdir}/qt5 \
    -examplesdir %{mingw32_datadir}/qt5/examples \
    -headerdir %{mingw32_includedir}/qt5 \
    -libdir %{mingw32_libdir} \
    -plugindir %{mingw32_libdir}/qt5/plugins \
    -sysconfdir %{mingw32_sysconfdir} \
    -translationdir %{mingw32_datadir}/qt5/translations \
    -device-option CROSS_COMPILE=%{mingw32_target}-"

qt_configure_args_win64="\
    -hostprefix %{_prefix}/%{mingw64_target} \
    -hostbindir %{_prefix}/%{mingw64_target}/bin/qt5 \
    -hostlibdir %{_prefix}/%{mingw64_target}/lib \
    -hostdatadir %{mingw64_datadir}/qt5 \
    -prefix %{mingw64_prefix} \
    -bindir %{mingw64_bindir} \
    -archdatadir %{mingw64_libdir}/qt5 \
    -datadir %{mingw64_datadir}/qt5 \
    -docdir %{mingw64_docdir}/qt5 \
    -examplesdir %{mingw64_datadir}/qt5/examples \
    -headerdir %{mingw64_includedir}/qt5 \
    -libdir %{mingw64_libdir} \
    -plugindir %{mingw64_libdir}/qt5/plugins \
    -sysconfdir %{mingw64_sysconfdir} \
    -translationdir %{mingw64_datadir}/qt5/translations \
    -device-option CROSS_COMPILE=%{mingw64_target}-"

###############################################################################
srcdir=`pwd`

# NOTE: Adding setting LD_LIBRARY_PATH as host tools are executed during the
# build which are linked against the built libQt5Bootstrap.so.

# Win32
rm -rf ../build_%{name}_static_win32
mkdir ../build_%{name}_static_win32
pushd ../build_%{name}_static_win32
$srcdir/configure -static $qt_configure_args_win32 $qt_configure_args_generic
LD_LIBRARY_PATH=$PWD/lib %make_build
popd

rm -rf ../build_%{name}_shared_win32
mkdir ../build_%{name}_shared_win32
pushd ../build_%{name}_shared_win32
$srcdir/configure -shared $qt_configure_args_win32 $qt_configure_args_generic
LD_LIBRARY_PATH=$PWD/lib %make_build
popd

###############################################################################
# Win64
rm -rf ../build_%{name}_static_win64
mkdir ../build_%{name}_static_win64
pushd ../build_%{name}_static_win64
$srcdir/configure -static $qt_configure_args_win64 $qt_configure_args_generic
LD_LIBRARY_PATH=$PWD/lib %make_build
popd

rm -rf ../build_%{name}_shared_win64
mkdir ../build_%{name}_shared_win64
pushd ../build_%{name}_shared_win64
$srcdir/configure -shared $qt_configure_args_win64 $qt_configure_args_generic
LD_LIBRARY_PATH=$PWD/lib %make_build
popd


%install
make install -C ../build_%{name}_static_win32 INSTALL_ROOT=%{buildroot}
make install -C ../build_%{name}_shared_win32 INSTALL_ROOT=%{buildroot}
make install -C ../build_%{name}_static_win64 INSTALL_ROOT=%{buildroot}
make install -C ../build_%{name}_shared_win64 INSTALL_ROOT=%{buildroot}

# Drop unneeded files
find %{buildroot} -name '*.la' -delete

rm -f %{buildroot}%{_prefix}/%{mingw32_target}/lib/libQt5Bootstrap.a
rm -f %{buildroot}%{_prefix}/%{mingw32_target}/lib/libQt5BootstrapDBus.a
rm -f %{buildroot}%{_prefix}/%{mingw64_target}/lib/libQt5Bootstrap.a
rm -f %{buildroot}%{_prefix}/%{mingw64_target}/lib/libQt5BootstrapDBus.a

# Add qtchooser support
mkdir -p %{buildroot}%{_sysconfdir}/xdg/qtchooser
echo "%{_prefix}/%{mingw32_target}/bin/qt5" >  %{buildroot}%{_sysconfdir}/xdg/qtchooser/mingw32-qt5.conf
echo "%{mingw32_prefix}" >> %{buildroot}%{_sysconfdir}/xdg/qtchooser/mingw32-qt5.conf
echo "%{_prefix}/%{mingw64_target}/bin/qt5" >  %{buildroot}%{_sysconfdir}/xdg/qtchooser/mingw64-qt5.conf
echo "%{mingw64_prefix}" >> %{buildroot}%{_sysconfdir}/xdg/qtchooser/mingw64-qt5.conf

# Create lib/qt5/mkspecs/features, used by other packages
mkdir -p %{buildroot}%{mingw32_libdir}/qt5/mkspecs/features
mkdir -p %{buildroot}%{mingw64_libdir}/qt5/mkspecs/features

# Manually install qmake and other native tools so we don't depend anymore on
# the version of the native Fedora Qt and also fix issues as illustrated at
# http://stackoverflow.com/questions/6592931/building-for-windows-under-linux-using-qt-creator
#
# Also make sure the tools can be found by CMake
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_prefix}/%{mingw32_target}/bin
mkdir -p %{buildroot}%{_prefix}/%{mingw64_target}/bin

for tool in qmake moc rcc uic qdbuscpp2xml qdbusxml2cpp syncqt.pl; do
    ln -s ../%{mingw32_target}/bin/qt5/$tool %{buildroot}%{_bindir}/%{mingw32_target}-$tool-qt5
    ln -s ../%{mingw64_target}/bin/qt5/$tool %{buildroot}%{_bindir}/%{mingw64_target}-$tool-qt5
done

ln -s %{mingw32_target}-qmake-qt5 %{buildroot}%{_bindir}/mingw32-qmake-qt5
ln -s %{mingw64_target}-qmake-qt5 %{buildroot}%{_bindir}/mingw64-qmake-qt5


# Win32
%files -n mingw32-qt5-qtbase
%license LICENSE.LGPL*
%{mingw32_bindir}/Qt5Concurrent.dll
%{mingw32_bindir}/Qt5Core.dll
%{mingw32_bindir}/Qt5DBus.dll
%{mingw32_bindir}/Qt5Gui.dll
%{mingw32_bindir}/Qt5Network.dll
%{mingw32_bindir}/Qt5OpenGL.dll
%{mingw32_bindir}/Qt5PrintSupport.dll
%{mingw32_bindir}/Qt5Sql.dll
%{mingw32_bindir}/Qt5Test.dll
%{mingw32_bindir}/Qt5Widgets.dll
%{mingw32_bindir}/Qt5Xml.dll
%{mingw32_libdir}/libQt5Concurrent.dll.a
%{mingw32_libdir}/libQt5Core.dll.a
%{mingw32_libdir}/libQt5DBus.dll.a
%{mingw32_libdir}/libQt5Gui.dll.a
%{mingw32_libdir}/libQt5Network.dll.a
%{mingw32_libdir}/libQt5OpenGL.dll.a
%{mingw32_libdir}/libQt5PrintSupport.dll.a
%{mingw32_libdir}/libQt5Sql.dll.a
%{mingw32_libdir}/libQt5Test.dll.a
%{mingw32_libdir}/libQt5Widgets.dll.a
%{mingw32_libdir}/libQt5Xml.dll.a
%{mingw32_libdir}/libqt5main.a
%{mingw32_libdir}/pkgconfig/Qt5Concurrent.pc
%{mingw32_libdir}/pkgconfig/Qt5Core.pc
%{mingw32_libdir}/pkgconfig/Qt5DBus.pc
%{mingw32_libdir}/pkgconfig/Qt5Gui.pc
%{mingw32_libdir}/pkgconfig/Qt5Network.pc
%{mingw32_libdir}/pkgconfig/Qt5OpenGL.pc
%{mingw32_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%{mingw32_libdir}/pkgconfig/Qt5PrintSupport.pc
%{mingw32_libdir}/pkgconfig/Qt5Sql.pc
%{mingw32_libdir}/pkgconfig/Qt5Test.pc
%{mingw32_libdir}/pkgconfig/Qt5Widgets.pc
%{mingw32_libdir}/pkgconfig/Qt5Xml.pc
%dir %{mingw32_libdir}/qt5/
%dir %{mingw32_libdir}/qt5/mkspecs
%dir %{mingw32_libdir}/qt5/mkspecs/features
%dir %{mingw32_libdir}/qt5/plugins
%dir %{mingw32_libdir}/qt5/plugins/bearer
%{mingw32_libdir}/qt5/plugins/bearer/qgenericbearer.dll
%dir %{mingw32_libdir}/qt5/plugins/generic
%{mingw32_libdir}/qt5/plugins/generic/qtuiotouchplugin.dll
%dir %{mingw32_libdir}/qt5/plugins/imageformats
%{mingw32_libdir}/qt5/plugins/imageformats/qgif.dll
%{mingw32_libdir}/qt5/plugins/imageformats/qico.dll
%{mingw32_libdir}/qt5/plugins/imageformats/qjpeg.dll
%dir %{mingw32_libdir}/qt5/plugins/platforms
%{mingw32_libdir}/qt5/plugins/platforms/qoffscreen.dll
%{mingw32_libdir}/qt5/plugins/platforms/qminimal.dll
%{mingw32_libdir}/qt5/plugins/platforms/qwindows.dll
%dir %{mingw32_libdir}/qt5/plugins/platformthemes/
%{mingw32_libdir}/qt5/plugins/platformthemes/qxdgdesktopportal.dll
%dir %{mingw32_libdir}/qt5/plugins/printsupport
%{mingw32_libdir}/qt5/plugins/printsupport/windowsprintersupport.dll
%dir %{mingw32_libdir}/qt5/plugins/sqldrivers
%{mingw32_libdir}/qt5/plugins/sqldrivers/qsqlite.dll
%{mingw32_libdir}/qt5/plugins/sqldrivers/qsqlodbc.dll
%{mingw32_libdir}/qt5/plugins/sqldrivers/qsqlpsql.dll
%dir %{mingw32_libdir}/qt5/plugins/styles
%{mingw32_libdir}/qt5/plugins/styles/qwindowsvistastyle.dll
%{mingw32_libdir}/cmake/Qt5/
%{mingw32_libdir}/cmake/Qt5AccessibilitySupport/
%{mingw32_libdir}/cmake/Qt5BootstrapDBus/
%{mingw32_libdir}/cmake/Qt5Core/
%{mingw32_libdir}/cmake/Qt5Concurrent/
%{mingw32_libdir}/cmake/Qt5DBus/
%{mingw32_libdir}/cmake/Qt5DeviceDiscoverySupport/
%{mingw32_libdir}/cmake/Qt5EdidSupport/
%{mingw32_libdir}/cmake/Qt5EventDispatcherSupport/
%{mingw32_libdir}/cmake/Qt5FbSupport/
%{mingw32_libdir}/cmake/Qt5FontDatabaseSupport/
%{mingw32_libdir}/cmake/Qt5Gui/
%{mingw32_libdir}/cmake/Qt5Network/
%{mingw32_libdir}/cmake/Qt5OpenGL/
%{mingw32_libdir}/cmake/Qt5OpenGLExtensions/
%{mingw32_libdir}/cmake/Qt5PlatformCompositorSupport/
%{mingw32_libdir}/cmake/Qt5PrintSupport/
%{mingw32_libdir}/cmake/Qt5Sql/
%{mingw32_libdir}/cmake/Qt5Test/
%{mingw32_libdir}/cmake/Qt5ThemeSupport/
%{mingw32_libdir}/cmake/Qt5VulkanSupport/
%{mingw32_libdir}/cmake/Qt5Widgets/
%{mingw32_libdir}/cmake/Qt5WindowsUIAutomationSupport/
%{mingw32_libdir}/cmake/Qt5Xml/
%dir %{mingw32_libdir}/metatypes
%{mingw32_libdir}/metatypes/qt5core_metatypes.json
%{mingw32_libdir}/metatypes/qt5gui_metatypes.json
%{mingw32_libdir}/metatypes/qt5widgets_metatypes.json
%dir %{mingw32_includedir}/qt5/
%{mingw32_includedir}/qt5/*
%{mingw32_docdir}/qt5/

%files -n mingw32-qt5-qmake
%{_bindir}/%{mingw32_target}-moc-qt5
%{_bindir}/%{mingw32_target}-qdbuscpp2xml-qt5
%{_bindir}/%{mingw32_target}-qdbusxml2cpp-qt5
%{_bindir}/%{mingw32_target}-qmake-qt5
%{_bindir}/%{mingw32_target}-rcc-qt5
%{_bindir}/%{mingw32_target}-syncqt.pl-qt5
%{_bindir}/%{mingw32_target}-uic-qt5
%{_bindir}/mingw32-qmake-qt5
%dir %{_prefix}/%{mingw32_target}/bin/qt5/
%{_prefix}/%{mingw32_target}/bin/qt5/fixqt4headers.pl
%{_prefix}/%{mingw32_target}/bin/qt5/moc
%{_prefix}/%{mingw32_target}/bin/qt5/qdbuscpp2xml
%{_prefix}/%{mingw32_target}/bin/qt5/qdbusxml2cpp
%{_prefix}/%{mingw32_target}/bin/qt5/qlalr
%{_prefix}/%{mingw32_target}/bin/qt5/qmake
%{_prefix}/%{mingw32_target}/bin/qt5/qvkgen
%{_prefix}/%{mingw32_target}/bin/qt5/rcc
%{_prefix}/%{mingw32_target}/bin/qt5/syncqt.pl
%{_prefix}/%{mingw32_target}/bin/qt5/tracegen
%{_prefix}/%{mingw32_target}/bin/qt5/uic
%{_prefix}/%{mingw32_target}/lib/libQt5Bootstrap.so.5*
%{_prefix}/%{mingw32_target}/lib/libQt5BootstrapDBus.so.5*
%{mingw32_datadir}/qt5/

# qtchooser
%dir %{_sysconfdir}/xdg/qtchooser/
# not editable config files, so not using %%config here
%{_sysconfdir}/xdg/qtchooser/mingw32-qt5.conf

%files -n mingw32-qt5-qtbase-devel
%{_prefix}/%{mingw32_target}/lib/libQt5Bootstrap.so
%{_prefix}/%{mingw32_target}/lib/libQt5Bootstrap.prl
%{_prefix}/%{mingw32_target}/lib/libQt5BootstrapDBus.so
%{_prefix}/%{mingw32_target}/lib/libQt5BootstrapDBus.prl

%files -n mingw32-qt5-qtbase-static
%{mingw32_libdir}/*.a
%{mingw32_libdir}/*.prl
%exclude %{mingw32_libdir}/*.dll.a
%dir %{mingw32_libdir}/qt5/plugins
%dir %{mingw32_libdir}/qt5/plugins/bearer
%{mingw32_libdir}/qt5/plugins/bearer/libqgenericbearer.a
%{mingw32_libdir}/qt5/plugins/bearer/qgenericbearer.prl
%dir %{mingw32_libdir}/qt5/plugins/generic
%{mingw32_libdir}/qt5/plugins/generic/libqtuiotouchplugin.a
%{mingw32_libdir}/qt5/plugins/generic/qtuiotouchplugin.prl
%dir %{mingw32_libdir}/qt5/plugins/imageformats
%{mingw32_libdir}/qt5/plugins/imageformats/libqgif.a
%{mingw32_libdir}/qt5/plugins/imageformats/qgif.prl
%{mingw32_libdir}/qt5/plugins/imageformats/libqico.a
%{mingw32_libdir}/qt5/plugins/imageformats/qico.prl
%{mingw32_libdir}/qt5/plugins/imageformats/libqjpeg.a
%{mingw32_libdir}/qt5/plugins/imageformats/qjpeg.prl
%dir %{mingw32_libdir}/qt5/plugins/platforms
%{mingw32_libdir}/qt5/plugins/platforms/libqoffscreen.a
%{mingw32_libdir}/qt5/plugins/platforms/qoffscreen.prl
%{mingw32_libdir}/qt5/plugins/platforms/libqminimal.a
%{mingw32_libdir}/qt5/plugins/platforms/qminimal.prl
%{mingw32_libdir}/qt5/plugins/platforms/libqwindows.a
%{mingw32_libdir}/qt5/plugins/platforms/qwindows.prl
%dir %{mingw32_libdir}/qt5/plugins/platformthemes/
%{mingw32_libdir}/qt5/plugins/platformthemes/libqxdgdesktopportal.a
%{mingw32_libdir}/qt5/plugins/platformthemes/qxdgdesktopportal.prl
%dir %{mingw32_libdir}/qt5/plugins/printsupport
%{mingw32_libdir}/qt5/plugins/printsupport/libwindowsprintersupport.a
%{mingw32_libdir}/qt5/plugins/printsupport/windowsprintersupport.prl
%dir %{mingw32_libdir}/qt5/plugins/sqldrivers
%{mingw32_libdir}/qt5/plugins/sqldrivers/libqsqlite.a
%{mingw32_libdir}/qt5/plugins/sqldrivers/qsqlite.prl
%{mingw32_libdir}/qt5/plugins/sqldrivers/libqsqlodbc.a
%{mingw32_libdir}/qt5/plugins/sqldrivers/qsqlodbc.prl
%{mingw32_libdir}/qt5/plugins/sqldrivers/libqsqlpsql.a
%{mingw32_libdir}/qt5/plugins/sqldrivers/qsqlpsql.prl
%dir %{mingw32_libdir}/qt5/plugins/styles
%{mingw32_libdir}/qt5/plugins/styles/libqwindowsvistastyle.a
%{mingw32_libdir}/qt5/plugins/styles/qwindowsvistastyle.prl

# Win64
%files -n mingw64-qt5-qtbase
%license LICENSE.LGPL*
%{mingw64_bindir}/Qt5Concurrent.dll
%{mingw64_bindir}/Qt5Core.dll
%{mingw64_bindir}/Qt5DBus.dll
%{mingw64_bindir}/Qt5Gui.dll
%{mingw64_bindir}/Qt5Network.dll
%{mingw64_bindir}/Qt5OpenGL.dll
%{mingw64_bindir}/Qt5PrintSupport.dll
%{mingw64_bindir}/Qt5Sql.dll
%{mingw64_bindir}/Qt5Test.dll
%{mingw64_bindir}/Qt5Widgets.dll
%{mingw64_bindir}/Qt5Xml.dll
%{mingw64_libdir}/libQt5Concurrent.dll.a
%{mingw64_libdir}/libQt5Core.dll.a
%{mingw64_libdir}/libQt5DBus.dll.a
%{mingw64_libdir}/libQt5Gui.dll.a
%{mingw64_libdir}/libQt5Network.dll.a
%{mingw64_libdir}/libQt5OpenGL.dll.a
%{mingw64_libdir}/libQt5PrintSupport.dll.a
%{mingw64_libdir}/libQt5Sql.dll.a
%{mingw64_libdir}/libQt5Test.dll.a
%{mingw64_libdir}/libQt5Widgets.dll.a
%{mingw64_libdir}/libQt5Xml.dll.a
%{mingw64_libdir}/libqt5main.a
%{mingw64_libdir}/pkgconfig/Qt5Concurrent.pc
%{mingw64_libdir}/pkgconfig/Qt5Core.pc
%{mingw64_libdir}/pkgconfig/Qt5DBus.pc
%{mingw64_libdir}/pkgconfig/Qt5Gui.pc
%{mingw64_libdir}/pkgconfig/Qt5Network.pc
%{mingw64_libdir}/pkgconfig/Qt5OpenGL.pc
%{mingw64_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%{mingw64_libdir}/pkgconfig/Qt5PrintSupport.pc
%{mingw64_libdir}/pkgconfig/Qt5Sql.pc
%{mingw64_libdir}/pkgconfig/Qt5Test.pc
%{mingw64_libdir}/pkgconfig/Qt5Widgets.pc
%{mingw64_libdir}/pkgconfig/Qt5Xml.pc
%dir %{mingw64_libdir}/qt5/
%dir %{mingw64_libdir}/qt5/mkspecs
%dir %{mingw64_libdir}/qt5/mkspecs/features
%dir %{mingw64_libdir}/qt5/plugins
%dir %{mingw64_libdir}/qt5/plugins/bearer
%{mingw64_libdir}/qt5/plugins/bearer/qgenericbearer.dll
%dir %{mingw64_libdir}/qt5/plugins/generic
%{mingw64_libdir}/qt5/plugins/generic/qtuiotouchplugin.dll
%dir %{mingw64_libdir}/qt5/plugins/imageformats
%{mingw64_libdir}/qt5/plugins/imageformats/qgif.dll
%{mingw64_libdir}/qt5/plugins/imageformats/qico.dll
%{mingw64_libdir}/qt5/plugins/imageformats/qjpeg.dll
%dir %{mingw64_libdir}/qt5/plugins/platforms
%{mingw64_libdir}/qt5/plugins/platforms/qoffscreen.dll
%{mingw64_libdir}/qt5/plugins/platforms/qminimal.dll
%{mingw64_libdir}/qt5/plugins/platforms/qwindows.dll
%dir %{mingw64_libdir}/qt5/plugins/platformthemes/
%{mingw64_libdir}/qt5/plugins/platformthemes/qxdgdesktopportal.dll
%dir %{mingw64_libdir}/qt5/plugins/printsupport
%{mingw64_libdir}/qt5/plugins/printsupport/windowsprintersupport.dll
%dir %{mingw64_libdir}/qt5/plugins/sqldrivers
%{mingw64_libdir}/qt5/plugins/sqldrivers/qsqlite.dll
%{mingw64_libdir}/qt5/plugins/sqldrivers/qsqlodbc.dll
%{mingw64_libdir}/qt5/plugins/sqldrivers/qsqlpsql.dll
%dir %{mingw64_libdir}/qt5/plugins/styles
%{mingw64_libdir}/qt5/plugins/styles/qwindowsvistastyle.dll
%{mingw64_libdir}/cmake/Qt5/
%{mingw64_libdir}/cmake/Qt5AccessibilitySupport/
%{mingw64_libdir}/cmake/Qt5BootstrapDBus/
%{mingw64_libdir}/cmake/Qt5Core/
%{mingw64_libdir}/cmake/Qt5Concurrent/
%{mingw64_libdir}/cmake/Qt5DBus/
%{mingw64_libdir}/cmake/Qt5DeviceDiscoverySupport/
%{mingw64_libdir}/cmake/Qt5EdidSupport/
%{mingw64_libdir}/cmake/Qt5EventDispatcherSupport/
%{mingw64_libdir}/cmake/Qt5FbSupport/
%{mingw64_libdir}/cmake/Qt5FontDatabaseSupport/
%{mingw64_libdir}/cmake/Qt5Gui/
%{mingw64_libdir}/cmake/Qt5Network/
%{mingw64_libdir}/cmake/Qt5OpenGL/
%{mingw64_libdir}/cmake/Qt5OpenGLExtensions/
%{mingw64_libdir}/cmake/Qt5PlatformCompositorSupport/
%{mingw64_libdir}/cmake/Qt5PrintSupport/
%{mingw64_libdir}/cmake/Qt5Sql/
%{mingw64_libdir}/cmake/Qt5Test/
%{mingw64_libdir}/cmake/Qt5ThemeSupport/
%{mingw64_libdir}/cmake/Qt5VulkanSupport/
%{mingw64_libdir}/cmake/Qt5Widgets/
%{mingw64_libdir}/cmake/Qt5WindowsUIAutomationSupport/
%{mingw64_libdir}/cmake/Qt5Xml/
%dir %{mingw64_libdir}/metatypes
%{mingw64_libdir}/metatypes/qt5core_metatypes.json
%{mingw64_libdir}/metatypes/qt5gui_metatypes.json
%{mingw64_libdir}/metatypes/qt5widgets_metatypes.json
%dir %{mingw64_includedir}/qt5/
%{mingw64_includedir}/qt5/*
%{mingw64_docdir}/qt5/

%files -n mingw64-qt5-qmake
%{_bindir}/%{mingw64_target}-moc-qt5
%{_bindir}/%{mingw64_target}-qdbuscpp2xml-qt5
%{_bindir}/%{mingw64_target}-qdbusxml2cpp-qt5
%{_bindir}/%{mingw64_target}-qmake-qt5
%{_bindir}/%{mingw64_target}-rcc-qt5
%{_bindir}/%{mingw64_target}-syncqt.pl-qt5
%{_bindir}/%{mingw64_target}-uic-qt5
%{_bindir}/mingw64-qmake-qt5
%dir %{_prefix}/%{mingw64_target}/bin/qt5/
%{_prefix}/%{mingw64_target}/bin/qt5/fixqt4headers.pl
%{_prefix}/%{mingw64_target}/bin/qt5/moc
%{_prefix}/%{mingw64_target}/bin/qt5/qdbuscpp2xml
%{_prefix}/%{mingw64_target}/bin/qt5/qdbusxml2cpp
%{_prefix}/%{mingw64_target}/bin/qt5/qlalr
%{_prefix}/%{mingw64_target}/bin/qt5/qmake
%{_prefix}/%{mingw64_target}/bin/qt5/qvkgen
%{_prefix}/%{mingw64_target}/bin/qt5/rcc
%{_prefix}/%{mingw64_target}/bin/qt5/syncqt.pl
%{_prefix}/%{mingw64_target}/bin/qt5/tracegen
%{_prefix}/%{mingw64_target}/bin/qt5/uic
%{_prefix}/%{mingw64_target}/lib/libQt5Bootstrap.so.5*
%{_prefix}/%{mingw64_target}/lib/libQt5BootstrapDBus.so.5*
%{mingw64_datadir}/qt5/

# qtchooser
%dir %{_sysconfdir}/xdg/qtchooser/
# not editable config files, so not using %%config here
%{_sysconfdir}/xdg/qtchooser/mingw64-qt5.conf

%files -n mingw64-qt5-qtbase-devel
%{_prefix}/%{mingw64_target}/lib/libQt5Bootstrap.so
%{_prefix}/%{mingw64_target}/lib/libQt5Bootstrap.prl
%{_prefix}/%{mingw64_target}/lib/libQt5BootstrapDBus.so
%{_prefix}/%{mingw64_target}/lib/libQt5BootstrapDBus.prl

%files -n mingw64-qt5-qtbase-static
%{mingw64_libdir}/*.a
%{mingw64_libdir}/*.prl
%exclude %{mingw64_libdir}/*.dll.a
%dir %{mingw64_libdir}/qt5/plugins
%dir %{mingw64_libdir}/qt5/plugins/bearer
%{mingw64_libdir}/qt5/plugins/bearer/libqgenericbearer.a
%{mingw64_libdir}/qt5/plugins/bearer/qgenericbearer.prl
%dir %{mingw64_libdir}/qt5/plugins/generic
%{mingw64_libdir}/qt5/plugins/generic/libqtuiotouchplugin.a
%{mingw64_libdir}/qt5/plugins/generic/qtuiotouchplugin.prl
%dir %{mingw64_libdir}/qt5/plugins/imageformats
%{mingw64_libdir}/qt5/plugins/imageformats/libqgif.a
%{mingw64_libdir}/qt5/plugins/imageformats/qgif.prl
%{mingw64_libdir}/qt5/plugins/imageformats/libqico.a
%{mingw64_libdir}/qt5/plugins/imageformats/qico.prl
%{mingw64_libdir}/qt5/plugins/imageformats/libqjpeg.a
%{mingw64_libdir}/qt5/plugins/imageformats/qjpeg.prl
%dir %{mingw64_libdir}/qt5/plugins/platforms
%{mingw64_libdir}/qt5/plugins/platforms/libqoffscreen.a
%{mingw64_libdir}/qt5/plugins/platforms/qoffscreen.prl
%{mingw64_libdir}/qt5/plugins/platforms/libqminimal.a
%{mingw64_libdir}/qt5/plugins/platforms/qminimal.prl
%{mingw64_libdir}/qt5/plugins/platforms/libqwindows.a
%{mingw64_libdir}/qt5/plugins/platforms/qwindows.prl
%dir %{mingw64_libdir}/qt5/plugins/platformthemes/
%{mingw64_libdir}/qt5/plugins/platformthemes/libqxdgdesktopportal.a
%{mingw64_libdir}/qt5/plugins/platformthemes/qxdgdesktopportal.prl
%dir %{mingw64_libdir}/qt5/plugins/printsupport
%{mingw64_libdir}/qt5/plugins/printsupport/libwindowsprintersupport.a
%{mingw64_libdir}/qt5/plugins/printsupport/windowsprintersupport.prl
%dir %{mingw64_libdir}/qt5/plugins/sqldrivers
%{mingw64_libdir}/qt5/plugins/sqldrivers/libqsqlite.a
%{mingw64_libdir}/qt5/plugins/sqldrivers/qsqlite.prl
%{mingw64_libdir}/qt5/plugins/sqldrivers/libqsqlodbc.a
%{mingw64_libdir}/qt5/plugins/sqldrivers/qsqlodbc.prl
%{mingw64_libdir}/qt5/plugins/sqldrivers/libqsqlpsql.a
%{mingw64_libdir}/qt5/plugins/sqldrivers/qsqlpsql.prl
%dir %{mingw64_libdir}/qt5/plugins/styles
%{mingw64_libdir}/qt5/plugins/styles/libqwindowsvistastyle.a
%{mingw64_libdir}/qt5/plugins/styles/qwindowsvistastyle.prl


%changelog
* Fri Nov 07 2025 Sandro Mani <manisandro@gmail.com> - 5.15.18-1
- Update to 5.15.18

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu May 29 2025 Sandro Mani <manisandro@gmail.com> - 5.15.17-1
- Update to 5.15.17

* Mon Jan 20 2025 Sandro Mani <manisandro@gmail.com> - 5.15.16-1
- Update to 5.15.6

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Sep 05 2024 Sandro Mani <manisandro@gmail.com> - 5.15.15-1
- Update to 5.15.15

* Tue Jul 30 2024 Sandro Mani <manisandro@gmail.com> - 5.15.14-4
- Fix for CVE-2024-39936

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Sandro Mani <manisandro@gmail.com> - 5.15.14-2
- Bump

* Thu Jun 06 2024 Sandro Mani <manisandro@gmail.com> - 5.15.14-1
- Update to 5.15.14

* Wed May 01 2024 Sandro Mani <manisandro@gmail.com> - 5.15.13-1
- Update to 5.15.13

* Thu Feb 15 2024 Sandro Mani <manisandro@gmail.com> - 5.15.12-2
- Backport fix for CVE-2024-25580

* Thu Feb 15 2024 Sandro Mani <manisandro@gmail.com> - 5.15.12-1
- Update to 5.15.12

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 14 2023 Sandro Mani <manisandro@gmail.com> - 5.15.11-1
- Update to 5.15.11

* Wed Aug 16 2023 Sandro Mani <manisandro@gmail.com> - 5.15.10-4
- Backport fix for CVE-2023-37369

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 5.15.10-2
- Backport fix for CVE-2023-38197

* Thu Jun 15 2023 Sandro Mani <manisandro@gmail.com> - 5.15.10-1
- Update to 5.15.10

* Fri May 05 2023 Orion Poplawski <orion@nwra.com> - 5.15.9-2
- Fixup static requires

* Wed Apr 12 2023 Sandro Mani <manisandro@gmail.com> - 5.15.9-1
- Update to 5.15.9

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Sandro Mani <manisandro@gmail.com> - 5.15.8-3
- Fix -std=gnu++1Z -> -std=gnu++1z in qt5-qtbase-mingw-profile.patch

* Mon Jan 09 2023 Sandro Mani <manisandro@gmail.com> - 5.15.8-2
- Backport fix for QTBUG-44096

* Sun Jan 08 2023 Sandro Mani <manisandro@gmail.com> - 5.15.8-1
- Update to 5.15.8

* Mon Dec 05 2022 Sandro Mani <manisandro@gmail.com> - 5.15.7-3
- Drop mingw-pcre BR (only keep mingw-pcre2)

* Fri Nov 18 2022 Sandro Mani <manisandro@gmail.com> - 5.15.7-2
- Rebuild (mingw-postgresql)

* Thu Nov 03 2022 Sandro Mani <manisandro@gmail.com> - 5.15.7-1
- Update to 5.15.7

* Thu Sep 22 2022 Sandro Mani <manisandro@gmail.com> - 5.15.6-1
- Update to 5.15.6

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Sandro Mani <manisandro@gmail.com> - 5.15.5-1
- Update to 5.15.5

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 5.15.4-1
- Update to 5.15.4

* Tue May 03 2022 Sandro Mani <manisandro@gmail.com> - 5.15.3-3
- Move host libs below mingw prefix

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 5.15.3-2
- Rebuild with mingw-gcc-12

* Fri Mar 11 2022 Sandro Mani <manisandro@gmail.com> - 5.15.3-1
- Update to 5.15.3

* Mon Feb 21 2022 Sandro Mani <manisandro@gmail.com> - 5.15.2-9
- Configure with -openssl-linked
- Refresh rollup patch
- Fix prl packaging

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 07 2021 Sandro Mani <manisandro@gmail.com> - 5.15.2-6
- Add kde rollup patches

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Apr 22 2021 Jan Blackquill <uhhadd@gmail.com> - 5.15.2-4
- Don't strip .prl files from build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 00:23:17 CET 2021 Sandro Mani <manisandro@gmail.com> - 5.15.2-2
- Rebuild (angle)

* Mon Nov 23 2020 Sandro Mani <manisandro@gmail.com> - 5.15.2-1
- Update to 5.15.2

* Fri Oct 30 2020 Jeff Law <law@redhat.com> - 5.15.1-2
- Fix missing #includes for gcc-11

* Tue Oct 06 2020 Sandro Mani <manisandro@gmail.com> - 5.15.1-1
- Update to 5.15.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 09:30:50 GMT 2020 Sandro Mani <manisandro@gmail.com> - 5.14.2-4
- Add -fstack-protector to QMAKE_LFLAGS

* Thu Apr 30 2020 Sandro Mani <manisandro@gmail.com> - 5.14.2-3
- Add patch to fix Negotiate crash

* Tue Apr 14 2020 Sandro Mani <manisandro@gmail.com> - 5.14.2-2
- Update qt5-qtbase-importlib-ext.patch to fix cmake config for static libraries looking for import libs
- Build with -no-feature-relocatable, add qt5-qtbase-no-relocatable.patch

* Sun Apr 05 2020 Sandro Mani <manisandro@gmail.com> - 5.14.2-1
- Update to 5.14.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Sandro Mani <manisandro@gmail.com> - 5.13.2-1
- Update to 5.13.2

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 5.12.5-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Tue Sep 24 2019 Sandro Mani <manisandro@gmail.com> - 5.12.5-1
- Update to 5.12.5

* Mon Aug 26 2019 Sandro Mani <manisandro@gmail.com> - 5.12.4-5
- Prevent debug library names in pkg-config files (#1745257)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Sandro Mani <manisandro@gmail.com> - 5.12.4-3
- Update qt5-qtbase-qt5main.patch
- Fix import libraries in -static subpackages

* Wed Jul 17 2019 Sandro Mani <manisandro@gmail.com> - 5.12.4-2
- Update qt5-qtbase-importlib-ext.patch to fix qt module link path

* Tue Jul 16 2019 Sandro Mani <manisandro@gmail.com> - 5.12.4-1
- Update to 5.12.4

* Wed May 01 2019 Sandro Mani <manisandro@gmail.com> - 5.12.3-2
- Own %%{mingw32,64_libdir}/qt5/mkspecs/features

* Wed Apr 17 2019 Sandro Mani <manisandro@gmail.com> - 5.12.3-1
- Update to 5.12.3

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Sandro Mani <manisandro@gmail.com> - 5.11.3-1
- Update to 5.11.3

* Fri Sep 21 2018 Sandro Mani <manisandro@gmail.com> - 5.11.2-1
- Update to 5.11.2

* Fri Aug 24 2018 Richard W.M. Jones <rjones@redhat.com> - 5.11.1-6
- Rebuild for new mingw-openssl.

* Wed Aug 08 2018 Sandro Mani <manisandro@gmail.com> - 5.11.1-5
- Silence tons of "redeclared without dllimport attribute after being referenced with dll linkage inline" warnings in QDataStream
- Update Kerberos/SPNEGO authentication support patch

* Thu Jul 19 2018 Sandro Mani <manisandro@gmail.com> - 5.11.1-4
- Fix build with recent glibc
- Backport proposed Kerberos/SPNEGO authentication support
- Require: mingw{32,64}-vulkan-headers

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Sandro Mani <manisandro@gmail.com> - 5.11.1-2
- Rebuild (vulkan)

* Tue Jun 19 2018 Sandro Mani <manisandro@gmail.com> - 5.11.1-1
- Update to 5.11.1

* Tue May 22 2018 Sandro Mani <manisandro@gmail.com> - 5.11.0-1
- Update to 5.11.0

* Mon Feb 19 2018 Sandro Mani <manisandro@gmail.com> - 5.10.1-2
- Add missing BR: gcc-c++, make

* Thu Feb 15 2018 Sandro Mani <manisandro@gmail.com> - 5.10.1-1
- Update to 5.10.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 Sandro Mani <manisandro@gmail.com> - 5.10.0-1
- Update to 5.10.0

* Tue Nov 28 2017 Sandro Mani <manisandro@gmail.com> - 5.9.3-2
- Fix missing QtSql PostgreSQL support

* Sun Nov 26 2017 Sandro Mani <manisandro@gmail.com> - 5.9.3-1
- Update to 5.9.3

* Mon Oct 09 2017 Sandro Mani <manisandro@gmail.com> - 5.9.2-1
- Update to 5.9.2

* Tue Aug 15 2017 Sandro Mani <manisandro@gmail.com> - 5.9.1-6
- Rebuild (pcre2)

* Wed Aug 09 2017 Sandro Mani <manisandro@gmail.com> - 5.9.1-5
- Force old debuginfo package logic for now

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Sandro Mani <manisandro@gmail.com> - 5.9.1-2
- Rebuild for mingw-angleproject-0-0.19.git8613f49

* Fri Jun 30 2017 Sandro Mani <manisandro@gmail.com> - 5.9.1-1
- Update to 5.9.1

* Tue Jun 13 2017 Sandro Mani <manisandro@gmail.com> - 5.9.0-1
- Update to 5.9.0

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon May 08 2017 Sandro Mani <manisandro@gmail.com> - 5.8.0-2
- Drop 0022-Allow-usage-of-static-version-with-CMake.patch

* Sat Apr 22 2017 Sandro Mani <manisandro@gmail.com> - 5.8.0-1
- Update to 5.8.0

* Tue Apr 04 2017 Sandro Mani <manisandro@gmail.com> - 5.7.1-3
- Add patch to ensure OpenSSL is preferred as crypto implementation (#1438740)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 07 2017 Sandro Mani <manisandro@gmail.com> - 5.7.1-1
- Update to 5.7.1

* Sat May 07 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-4
- Rebuild against mingw-gcc 6.1

* Wed Apr 13 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-3
- Re-enable QSharedMemory (got broken between Qt 5.3 and Qt 5.4)
- Fixes FTBFS of mingw-qt5-qsystems package (RHBZ #1288928)

* Sat Apr  9 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-2
- Add BR: mingw{32,64}-gstreamer1

* Sun Mar 27 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.6.0-1
- Update to 5.6.0
- Build with -optimized-qmake again

* Sun Feb  7 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-4
- Temporary build without -optimized-qmake on Fedora24+ to prevent
  a build failure with GCC6 on i686 environments

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 31 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-2
- Prevent warning output when QWebView loads QNetworkRequest (QTBUG-49174)
- Re-add QMAKE_LRELEASE qmake parameter which accidently got lost some time ago

* Thu Dec 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.1-1
- Update to 5.5.1
- Fixes RHBZ #1293056

* Thu Aug 27 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-2
- Add static versions of various plugin libraries like qwindows to the -static subpackages (RHBZ #1257630)

* Wed Aug  5 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-2
- Fix CVE-2015-0295, CVE-2015-1858, CVE-2015-1859 and CVE-2015-1860

* Sun Mar  8 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1
- Added some more BuildRequires for mingw*-static libraries as the ./configure
  script now needs them to be available in the buildroot
- Fix detection of the static dbus and harfbuzz libraries

* Mon Jan 26 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-4
- Rebuild against mingw-w64 v4.0rc1

* Wed Dec 31 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-3
- Added some more Requires tags to the -static subpackages

* Wed Dec 31 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-2
- Added various Requires tags to the -static subpackages

* Mon Dec 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.4.0-1
- Update to 5.4.0
- Thanks to Philip A Reimer (ArchLinux MinGW maintainer)
  for rebasing the ANGLE patches
- Use external harfbuzz library (unfortunately this also introduces
  additional runtime dependencies on mingw-freetype, mingw-bzip2,
  mingw-glib2 and mingw-gettext)

* Thu Dec  4 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.2-2
- Rebuild against gcc 4.9.2 (to fix paths mentioned in mkspecs/qconfig.pri)

* Fri Sep 19 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.2-1
- Update to 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.1-3
- Rebuild against gcc 4.9.1 (to fix paths mentioned in mkspecs/qconfig.pri)

* Sun Jul  6 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.1-2
- Remove references to obsolete packages

* Sat Jul  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.1-1
- Update to 5.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.3.0-1
- Update to 5.3.0

* Sat May  3 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-3
- Fix invalid reference to qtmain when using CMake (RHBZ #1092465)
- Fix DoS vulnerability in the GIF image handler (QTBUG-38367, RHBZ #1092837)

* Sun Apr 13 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-2
- Rebuild against gcc 4.9 (to fix paths mentioned in mkspecs/qconfig.pri)

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.1-1
- Update to 5.2.1

* Sat Jan 11 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-4
- Remove hard dependency on qtchooser and co-own the /etc/xdg/qtchooser folder

* Mon Jan  6 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-3
- Split the cmake patch and moved half of its contents to the 'implib dll'
  patch and the other to the 'use external angle' patch as those are more
  proper locations

* Sun Jan  5 2014 Yaakov Selkowitz <yselkowitz@users.sourceforge.net> - 5.2.0-2
- Fix qmake to use .dll.a extension for implibs (avoids renaming hacks in
  all mingw-qt5-* packages)
- Force usage of system zlib in Qt5Bootstrap
- Install shared libQt5BootstrapDBus for qdbuscpp2xml and qdbusxml2cpp
- Fix QMAKE_LIBS_NETWORK for static linkage
- Closes RHBZ #1048677

* Sun Jan  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-1
- Update to 5.2.0
- Use the generic win32-g++ mkspecs profile instead of win32-g++-cross
  and win32-g++-cross-x64 (as is preferred by upstream)
- Add support for qtchooser
- Moved the native tools to /usr/$target/bin/qt5 (qtchooser requires the
  tools to be in an unique folder with their original file names)
  All symlinks in %%{_bindir} are updated to reflect this as well
- Prevent invalid Libs.private references in generated pkg-config files
- Prevent patch backups from ending up in the mkspecs folders
- Reorganized and cleaned up the patches

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.4.rc1
- Update to 5.2.0 RC 1

* Wed Nov 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.3.beta1
- Try harder to fix detection of the uic tool when using CMake

* Tue Nov 26 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.2.beta1
- Fix detection of the uic tool when using CMake (RHBZ #1019952)

* Tue Oct 22 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.2.0-0.1.beta1
- Update to 5.2.0 beta 1
- Fix CMake support (RHBZ #1019952, RHBZ #1019947)

* Thu Sep 12 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.1-2
- Removed DBus 'interface' workaround patch as the issue is resolved in DBus upstream

* Thu Aug 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.1-1
- Update to 5.1.1
- Fix FTBFS against latest mingw-w64

* Fri Aug  2 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-5
- Re-enable R: mingw{32,64}-qt5-qttools-lrelease now that
  bootstrapping Qt5 on ARM has completed

* Wed Jul 31 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-4
- Make sure the native Qt5Bootstrap library is a shared library
- Enabled PostgreSQL support
- Removed the reference to the 'demos' folder as demos are
  bundled as separate tarballs

* Tue Jul 30 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-3
- Temporary build without R: mingw{32,64}-qt5-qttools-lrelease
  to allow mingw-qt5-qttools to be built on arm

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-2
- Rebuild against libpng 1.6

* Wed Jul 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0
- Fix detection of external pcre library
- Added BR: mingw32-pcre mingw64-pcre

* Wed Jul 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.2-3
- Display message box if platform plugin cannot be found (QTBUG-31765, QTBUG-31760)

* Fri May 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.2-2
- Fix references to the tools qdoc and qhelpgenerator (needed to build qtdoc)

* Sat Apr 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2
- Remove DirectWrite support for now as the necessary API
  isn't available on Windows XP (as mentioned in RHBZ #917323)

* Thu Mar 28 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.1-4
- Have the -qmake packages require mingw{32,64}-qt5-qttools-lrelease
  and update the reference to it in the mkspecs profiles

* Tue Mar 26 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.1-3
- Make sure the .pc files of the Qt5 modules are installed correctly

* Thu Feb  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.1-2
- Replaced the OpenSSL patch with a more proper one
- Improve detection of the Qt5Bootstrap library (needed by mingw-qt5-qttools)
- Workaround cross-compilation issue when using a non-x86 host (RHBZ #905863, QTBUG #29426)
- Resolve build failure caused by QtDBus headers which use the reserved keyword 'interface'

* Thu Jan 31 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1
- Removed the -fast configure argument (upstream dropped support for it)

* Fri Jan 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-4
- Moved the libQt5Bootstrap.a library (required to build tools like lrelease
  and lupdate which are part of mingw-qt5-qttools) to separate -devel subpackages
  as it is a native library instead of a cross-compiled one
- Removed the pkg-config file for Qt5Bootstrap as it doesn't work as expected
  when Qt5 is cross-compiled

* Sat Dec 29 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-3
- The define QT_NEEDS_QMAIN also needs to be set for our mkspecs profiles
- To make linking against qt5main.a (which contains a Qt specific WinMain) work
  binaries need to be linked with -lmingw32 -lqt5main
- Resolves some initialisation issues
- Don't enable ICU support as it introduces over 20MB of dependency bloat

* Sat Dec 29 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-2
- Don't segfault when no suitable platform dll could be located

* Mon Dec 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-1
- Update to Qt 5.0.0 Final
- Use the qplatformdefs.h header which is included in the
  win32-g++ mkspecs profile instead of providing our own
- Replaced the bundled copy of the ANGLE libraries with
  a seperate mingw-angleproject package

* Thu Dec 13 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.15.rc2
- Update to Qt 5.0.0 RC2
- Dropped upstreamed DirectWrite patch

* Fri Dec  7 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.14.rc1
- Update to Qt 5.0.0 RC1
- Replaced various hack with proper patches
- Use the configure argument -archdatadir as it is used to decide
  where the mkspecs profiles should be installed

* Sat Nov 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.13.beta1.git20121110.d725239c
- Update to 20121110 snapshot (rev d725239c)
- Dropped the configure argument -qtlibinfix 5 as upstream
  has resolved the file conflicts with Qt4 properly now
- Added several missing flags to the mkspecs profiles
- Dropped the pkg-config file renames as they're not needed any more
- Dropped two obsolete patches

* Sat Nov 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.12.beta1.git20121103.ccc4fbdf
- Update to 20121103 snapshot (rev ccc4fbdf)
- Use -std=c++11 instead of -std=c++0x as the latter is deprecated in gcc 4.7
- Added DirectWrite support
- Added Angle support

* Sun Oct  7 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.11.beta1
- Fix compilation failure of the win64 build when using c++11 mode

* Sat Sep 15 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.10.beta1
- Re-added some configure arguments as they're apparently still needed to build
  the individual Qt components
- Removed -ltiff from the mkspecs profiles
- Added BR: mingw32-icu mingw64-icu
- Fix directory ownership of %%{mingw32_datadir}/qt5/ and %%{mingw64_datadir}/qt5/

* Thu Sep 13 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.9.beta1
- Add QT_TOOL.lrelease.command to the mkspecs profiles
- Fixed detection of mingw-icu
- Removed some obsolete configure arguments

* Wed Sep 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.8.beta1
- Make sure that Qt components which are built as static library also
  contain the version number (TARGET_VERSION_EXT) when it is set

* Mon Sep 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.7.beta1
- Added syncqt to the mkspecs profiles
- Set the qtlibinfix parameter correctly to avoid needing to use other hacks

* Sun Sep  9 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.6.beta1
- Make sure that Qt is built with debugging symbols and that these
  debugging symbols are placed in the -debuginfo subpackage

* Sat Sep  8 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.5.beta1
- Removed -javascript-jit from the configure arguments as it's only needed
  for QtWebKit (which is provided in a seperate package)
- Added QMAKE_DLLTOOL to the mkspecs profiles

* Sat Sep  8 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.4.beta1
- Use the lrelease tool from mingw-qt4 for now until mingw-qt5-qttools is packaged

* Fri Sep  7 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.3.beta1
- Added win32 static release and win64 static release builds

* Tue Sep  4 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.2.beta1
- Moved headers to %%{mingw32_includedir}/qt5 and %%{mingw64_includedir}/qt5
- Renamed the pkgconfig files to avoid conflict with qt4

* Tue Sep  4 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0.0-0.1.beta1
- Initial package (based on mingw-qt spec file)

