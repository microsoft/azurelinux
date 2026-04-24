# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

%global qt_module qtbase
# Disable debugsource packages
%undefine _debugsource_packages

#global pre rc

#global commit d725239c3e09c2b740a093265f6a9675fd2f8524
#global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?commit:1}
%global source_folder %{qt_module}-%{commit}
%else
%global source_folder %{qt_module}-everywhere-src-%{qt_version}%{?pre:-%{pre}}
%endif

# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')
%define qt_version %(echo %{version} | cut -d~ -f1)

Name:           mingw-qt6-qtbase
Version:        6.10.2
Release: 2%{?dist}
Summary:        Qt6 for Windows - QtBase component
# Can't make package noarch as it could lead to -DQT_HOST_PATH_CMAKE_DIR=%%{_libdir}/cmake ponting to the wrong libdir

License:        LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
URL:            http://qt.io/

%if 0%{?commit:1}
Source0:        https://github.com/qt/%{qt_module}/archive/%{commit}/%{qt_module}-everywhere-src-%{commit}.tar.gz
%else
Source0:        http://download.qt.io/%{?pre:development}%{?!pre:official}_releases/qt/%{release_version}/%{qt_version}%{?pre:-%pre}/submodules/%{qt_module}-everywhere-src-%{qt_version}%{?pre:-%pre}.tar.xz
%endif

# Fix import library suffix
Patch0:         qtbase-import-lib-suffix.patch
# Resolve symlinks in wrapper scripts
Patch1:         qtbase-readlink.patch
# Include toolchain file automatically if it exists
# Rather than having to specify -DCMAKE_TOOLCHAIN_FILE="$toolchain_path" manually when invoking cmake...
Patch2:         qtbase-include-toolchain.patch
# Specify correct Header path in qmake config
Patch3:         qtbase-qmakeconf.patch
# Fix mingw build
Patch4:         qtbase-mingw.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  perl-interpreter
BuildRequires:  qt6-qtbase-devel = %{version}
BuildRequires:  xmlstarlet

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-pkg-config
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-bzip2
BuildRequires:  mingw32-fontconfig
BuildRequires:  mingw32-freetype
BuildRequires:  mingw32-harfbuzz
BuildRequires:  mingw32-libjpeg-turbo
BuildRequires:  mingw32-libpng
BuildRequires:  mingw32-openssl
BuildRequires:  mingw32-pcre2
BuildRequires:  mingw32-postgresql
BuildRequires:  mingw32-sqlite
BuildRequires:  mingw32-vulkan-headers
BuildRequires:  mingw32-vulkan-loader
BuildRequires:  mingw32-win-iconv
BuildRequires:  mingw32-winpthreads
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-pkg-config
BuildRequires:  mingw64-dlfcn
BuildRequires:  mingw64-bzip2
BuildRequires:  mingw64-fontconfig
BuildRequires:  mingw64-freetype
BuildRequires:  mingw64-harfbuzz
BuildRequires:  mingw64-libjpeg-turbo
BuildRequires:  mingw64-libpng
BuildRequires:  mingw64-openssl
BuildRequires:  mingw64-pcre2
BuildRequires:  mingw64-postgresql
BuildRequires:  mingw64-sqlite
BuildRequires:  mingw64-vulkan-headers
BuildRequires:  mingw64-vulkan-loader
BuildRequires:  mingw64-win-iconv
BuildRequires:  mingw64-winpthreads
BuildRequires:  mingw64-zlib

Provides:       bundled(libb2)
Provides:       bundled(libmd4c)
Provides:       bundled(double-conversion)


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the 32-bit Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt6-qtbase
Summary:        Qt6 for Windows - QtBase component
# Dependency for host tools
Requires:       qt6-qtbase-devel = %{version}
# Public headers require vulkan/vulkan.h
Requires:       mingw32-vulkan-headers

%description -n mingw32-qt6-qtbase
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the 64-bit Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.



# Win64
%package -n mingw64-qt6-qtbase
Summary:        Qt6 for Windows - QtBase component
# Dependency for host tools
Requires:       qt6-qtbase-devel = %{version}
# Public headers require vulkan/vulkan.h
Requires:       mingw64-vulkan-headers

%description -n mingw64-qt6-qtbase
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.



%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{source_folder}

# Remove bundled libraries
rm -rf src/3rdparty/{freetype,libjpeg,libpng,pcre2,sqlite,zlib}


%build
export MINGW32_CXXFLAGS="%{mingw32_cflags} -msse2"
export MINGW64_CXXFLAGS="%{mingw64_cflags} -msse2"
%mingw_cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DQT_HOST_PATH=%{_prefix} \
    -DQT_HOST_PATH_CMAKE_DIR=%{_libdir}/cmake \
    -DINSTALL_ARCHDATADIR=lib/qt6 \
    -DINSTALL_BINDIR=bin \
    -DINSTALL_DATADIR=share/qt6 \
    -DINSTALL_DOCDIR=share/doc/qt6 \
    -DINSTALL_INCLUDEDIR=include/qt6 \
    -DINSTALL_MKSPECSDIR=lib/qt6/mkspecs \
    -DQT_FEATURE_relocatable=OFF \
    -DFEATURE_pkg_config=ON \
    -DQT_FEATURE_accessibility=ON \
    -DQT_FEATURE_egl=OFF \
    -DQT_FEATURE_fontconfig=ON \
    -DQT_FEATURE_icu=ON \
    -DQT_FEATURE_openssl_linked=ON \
    -DQT_FEATURE_separate_debug_info=OFF \
    -DQT_FEATURE_system_harfbuzz=ON \
    -DQT_FEATURE_system_sqlite=ON
%mingw_ninja


%install
%mingw_ninja_install


# Delete unused files
rm %{buildroot}%{mingw32_libdir}/qt6/bin/{ensure_pro_file.cmake,qt-internal-configure-tests}
rm %{buildroot}%{mingw64_libdir}/qt6/bin/{ensure_pro_file.cmake,qt-internal-configure-tests}
rm %{buildroot}%{mingw32_bindir}/qt-configure-module
rm %{buildroot}%{mingw64_bindir}/qt-configure-module
rm %{buildroot}%{mingw32_bindir}/qmake6
rm %{buildroot}%{mingw64_bindir}/qmake6
rm %{buildroot}%{mingw32_bindir}/qtpaths6
rm %{buildroot}%{mingw64_bindir}/qtpaths6
rm -rf %{buildroot}%{mingw32_datadir}/qt6/wayland/protocols
rm -rf %{buildroot}%{mingw64_datadir}/qt6/wayland/protocols
rm -rf %{buildroot}%{mingw32_datadir}/qt6/wayland/extensions
rm -rf %{buildroot}%{mingw64_datadir}/qt6/wayland/extensions

# Move host scripts
mkdir -p %{buildroot}%{_prefix}/%{mingw32_target}/bin/qt6
mkdir -p %{buildroot}%{_prefix}/%{mingw64_target}/bin/qt6
mv %{buildroot}%{mingw32_bindir}/{target_qt.conf,qmake,qt-cmake,qtpaths,qt-cmake-create} %{buildroot}%{_prefix}/%{mingw32_target}/bin/qt6
mv %{buildroot}%{mingw64_bindir}/{target_qt.conf,qmake,qt-cmake,qtpaths,qt-cmake-create} %{buildroot}%{_prefix}/%{mingw64_target}/bin/qt6

# Fix relative path to toolchain file
sed -Ei 's|toolchain_path="$script_dir_path/(.*)/cmake/(.*)"|toolchain_path=$script_dir_path/../../sysroot/mingw/libs/\2|' %{buildroot}%{_prefix}/%{mingw32_target}/bin/qt6/qt-cmake
sed -Ei 's|toolchain_path="$script_dir_path/(.*)/cmake/(.*)"|toolchain_path=$script_dir_path/../../sysroot/mingw/libs/\2|' %{buildroot}%{_prefix}/%{mingw64_target}/bin/qt6/qt-cmake

# Fix relative paths to prefixes
sed -i 's|Prefix=.*|Prefix=%{mingw32_prefix}|g' %{buildroot}%{_prefix}/%{mingw32_target}/bin/qt6/target_qt.conf
sed -i 's|HostPrefix=.*|HostPrefix=%{_prefix}|g' %{buildroot}%{_prefix}/%{mingw32_target}/bin/qt6/target_qt.conf
sed -i 's|Prefix=.*|Prefix=%{mingw64_prefix}|g' %{buildroot}%{_prefix}/%{mingw64_target}/bin/qt6/target_qt.conf
sed -i 's|HostPrefix=.*|HostPrefix=%{_prefix}|g' %{buildroot}%{_prefix}/%{mingw64_target}/bin/qt6/target_qt.conf

# target-prefixed symlinks
mkdir -p %{buildroot}%{_bindir}
ln -s %{_prefix}/%{mingw32_target}/bin/qt6/qmake %{buildroot}%{_bindir}/%{mingw32_target}-qmake-qt6
ln -s %{_prefix}/%{mingw64_target}/bin/qt6/qmake %{buildroot}%{_bindir}/%{mingw64_target}-qmake-qt6
ln -s %{_prefix}/%{mingw32_target}/bin/qt6/qt-cmake %{buildroot}%{_bindir}/%{mingw32_target}-qt6-cmake
ln -s %{_prefix}/%{mingw64_target}/bin/qt6/qt-cmake %{buildroot}%{_bindir}/%{mingw64_target}-qt6-cmake

# Inject CROSS_COMPILE var to win32-g++ spec
sed -i "1i CROSS_COMPILE=%{mingw32_target}-" %{buildroot}%{mingw32_libdir}/qt6/mkspecs/win32-g++/qmake.conf
sed -i "1i CROSS_COMPILE=%{mingw64_target}-" %{buildroot}%{mingw64_libdir}/qt6/mkspecs/win32-g++/qmake.conf

# FIXME Remove files which should not get installed?
rm -rf %{buildroot}/%{mingw32_libdir}/objects-RelWithDebInfo/
rm -rf %{buildroot}/%{mingw64_libdir}/objects-RelWithDebInfo/


# Win32
%files -n mingw32-qt6-qtbase
%license LICENSES/GPL*
%license LICENSES/LGPL*
%{mingw32_bindir}/Qt6Concurrent.dll
%{mingw32_bindir}/Qt6Core.dll
%{mingw32_bindir}/Qt6DBus.dll
%{mingw32_bindir}/Qt6Gui.dll
%{mingw32_bindir}/Qt6Network.dll
%{mingw32_bindir}/Qt6OpenGL.dll
%{mingw32_bindir}/Qt6OpenGLWidgets.dll
%{mingw32_bindir}/Qt6PrintSupport.dll
%{mingw32_bindir}/Qt6Sql.dll
%{mingw32_bindir}/Qt6Test.dll
%{mingw32_bindir}/Qt6Widgets.dll
%{mingw32_bindir}/Qt6Xml.dll
%{mingw32_libdir}/libQt6Concurrent.dll.a
%{mingw32_libdir}/libQt6Core.dll.a
%{mingw32_libdir}/libQt6DBus.dll.a
%{mingw32_libdir}/libQt6ExampleIcons.a
%{mingw32_libdir}/libQt6ExamplesAssetDownloader.a
%{mingw32_libdir}/libQt6Gui.dll.a
%{mingw32_libdir}/libQt6Network.dll.a
%{mingw32_libdir}/libQt6OpenGL.dll.a
%{mingw32_libdir}/libQt6OpenGLWidgets.dll.a
%{mingw32_libdir}/libQt6PrintSupport.dll.a
%{mingw32_libdir}/libQt6Sql.dll.a
%{mingw32_libdir}/libQt6Test.dll.a
%{mingw32_libdir}/libQt6Widgets.dll.a
%{mingw32_libdir}/libQt6Xml.dll.a
%{mingw32_libdir}/libQt6DeviceDiscoverySupport.a
%{mingw32_libdir}/libQt6EntryPoint.a
%{mingw32_libdir}/libQt6FbSupport.a
%{mingw32_libdir}/Qt6Concurrent.prl
%{mingw32_libdir}/Qt6Core.prl
%{mingw32_libdir}/Qt6DBus.prl
%{mingw32_libdir}/Qt6DeviceDiscoverySupport.prl
%{mingw32_libdir}/Qt6EntryPoint.prl
%{mingw32_libdir}/Qt6ExampleIcons.prl
%{mingw32_libdir}/Qt6ExamplesAssetDownloader.prl
%{mingw32_libdir}/Qt6FbSupport.prl
%{mingw32_libdir}/Qt6Gui.prl
%{mingw32_libdir}/Qt6Network.prl
%{mingw32_libdir}/Qt6OpenGL.prl
%{mingw32_libdir}/Qt6OpenGLWidgets.prl
%{mingw32_libdir}/Qt6PrintSupport.prl
%{mingw32_libdir}/Qt6Sql.prl
%{mingw32_libdir}/Qt6Test.prl
%{mingw32_libdir}/Qt6Widgets.prl
%{mingw32_libdir}/Qt6Xml.prl
%dir %{mingw32_libdir}/qt6/
%dir %{mingw32_libdir}/qt6/bin/
%{mingw32_libdir}/qt6/bin/qt_cyclonedx_generator.py
%{mingw32_libdir}/qt6/bin/qt-cmake-private
%{mingw32_libdir}/qt6/bin/qt-cmake-private-install.cmake
%{mingw32_libdir}/qt6/bin/qt-cmake-standalone-test
%{mingw32_libdir}/qt6/bin/qt-internal-configure-examples
%{mingw32_libdir}/qt6/bin/qt-testrunner.py
%{mingw32_libdir}/qt6/bin/sanitizer-testrunner.py
%dir %{mingw32_libdir}/qt6/metatypes/
%{mingw32_libdir}/qt6/metatypes/qt6concurrent_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6core_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6dbus_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6devicediscoverysupportprivate_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6exampleiconsprivate_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6examplesassetdownloaderprivate_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6fbsupportprivate_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6gui_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6network_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6opengl_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6openglwidgets_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6printsupport_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6sql_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6test_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6widgets_metatypes.json
%{mingw32_libdir}/qt6/metatypes/qt6xml_metatypes.json
%{mingw32_libdir}/qt6/mkspecs/
%{mingw32_libdir}/qt6/modules/
%{mingw32_libdir}/qt6/modules/Concurrent.json
%{mingw32_libdir}/qt6/modules/Core.json
%{mingw32_libdir}/qt6/modules/DBus.json
%{mingw32_libdir}/qt6/modules/DeviceDiscoverySupportPrivate.json
%{mingw32_libdir}/qt6/modules/EntryPointPrivate.json
%{mingw32_libdir}/qt6/modules/FbSupportPrivate.json
%{mingw32_libdir}/qt6/modules/Gui.json
%{mingw32_libdir}/qt6/modules/Network.json
%{mingw32_libdir}/qt6/modules/OpenGL.json
%{mingw32_libdir}/qt6/modules/OpenGLWidgets.json
%{mingw32_libdir}/qt6/modules/PrintSupport.json
%{mingw32_libdir}/qt6/modules/Sql.json
%{mingw32_libdir}/qt6/modules/Test.json
%{mingw32_libdir}/qt6/modules/Widgets.json
%{mingw32_libdir}/qt6/modules/Xml.json
%dir %{mingw32_libdir}/qt6/plugins
%dir %{mingw32_libdir}/qt6/plugins/generic
%{mingw32_libdir}/qt6/plugins/generic/qtuiotouchplugin.dll
%dir %{mingw32_libdir}/qt6/plugins/imageformats
%{mingw32_libdir}/qt6/plugins/imageformats/qgif.dll
%{mingw32_libdir}/qt6/plugins/imageformats/qico.dll
%{mingw32_libdir}/qt6/plugins/imageformats/qjpeg.dll
%dir %{mingw32_libdir}/qt6/plugins/networkinformation
%{mingw32_libdir}/qt6/plugins/networkinformation/qnetworklistmanager.dll
%dir %{mingw32_libdir}/qt6/plugins/platforms
%{mingw32_libdir}/qt6/plugins/platforms/qdirect2d.dll
%{mingw32_libdir}/qt6/plugins/platforms/qoffscreen.dll
%{mingw32_libdir}/qt6/plugins/platforms/qminimal.dll
%{mingw32_libdir}/qt6/plugins/platforms/qwindows.dll
%dir %{mingw32_libdir}/qt6/plugins/sqldrivers
%{mingw32_libdir}/qt6/plugins/sqldrivers/qsqlite.dll
%{mingw32_libdir}/qt6/plugins/sqldrivers/qsqlodbc.dll
%{mingw32_libdir}/qt6/plugins/sqldrivers/qsqlpsql.dll
%dir %{mingw32_libdir}/qt6/plugins/styles
%{mingw32_libdir}/qt6/plugins/styles/qmodernwindowsstyle.dll
%dir %{mingw32_libdir}/qt6/plugins/tls
%{mingw32_libdir}/qt6/plugins/tls/qcertonlybackend.dll
%{mingw32_libdir}/qt6/plugins/tls/qopensslbackend.dll
%{mingw32_libdir}/qt6/plugins/tls/qschannelbackend.dll
%dir %{mingw32_libdir}/qt6/sbom
%{mingw32_libdir}/qt6/sbom/%{qt_module}-%{qt_version}.spdx
%{mingw32_libdir}/cmake/Qt6/
%{mingw32_libdir}/cmake/Qt6BuildInternals/
%{mingw32_libdir}/cmake/Qt6Concurrent/

%{mingw32_libdir}/cmake/Qt6Core/
%{mingw32_libdir}/cmake/Qt6CorePrivate/
%{mingw32_libdir}/cmake/Qt6DBus/
%{mingw32_libdir}/cmake/Qt6DBusPrivate/
%{mingw32_libdir}/cmake/Qt6DeviceDiscoverySupportPrivate/
%{mingw32_libdir}/cmake/Qt6EntryPointPrivate/
%{mingw32_libdir}/cmake/Qt6ExampleIconsPrivate/
%{mingw32_libdir}/cmake/Qt6ExamplesAssetDownloaderPrivate/
%{mingw32_libdir}/cmake/Qt6FbSupportPrivate/
%{mingw32_libdir}/cmake/Qt6Gui/
%{mingw32_libdir}/cmake/Qt6GuiPrivate/
%{mingw32_libdir}/cmake/Qt6HostInfo/
%{mingw32_libdir}/cmake/Qt6Network/
%{mingw32_libdir}/cmake/Qt6NetworkPrivate/
%{mingw32_libdir}/cmake/Qt6OpenGL/
%{mingw32_libdir}/cmake/Qt6OpenGLPrivate/
%{mingw32_libdir}/cmake/Qt6OpenGLWidgets/
%{mingw32_libdir}/cmake/Qt6PrintSupport/
%{mingw32_libdir}/cmake/Qt6PrintSupportPrivate/
%{mingw32_libdir}/cmake/Qt6Sql/
%{mingw32_libdir}/cmake/Qt6SqlPrivate/
%{mingw32_libdir}/cmake/Qt6Test/
%{mingw32_libdir}/cmake/Qt6TestPrivate/
%{mingw32_libdir}/cmake/Qt6TestInternalsPrivate/
%{mingw32_libdir}/cmake/Qt6Widgets/
%{mingw32_libdir}/cmake/Qt6WidgetsPrivate/
%{mingw32_libdir}/cmake/Qt6Xml/
%{mingw32_libdir}/cmake/Qt6XmlPrivate/
%{mingw32_libdir}/pkgconfig/Qt6Concurrent.pc
%{mingw32_libdir}/pkgconfig/Qt6Core.pc
%{mingw32_libdir}/pkgconfig/Qt6DBus.pc
%{mingw32_libdir}/pkgconfig/Qt6Gui.pc
%{mingw32_libdir}/pkgconfig/Qt6Network.pc
%{mingw32_libdir}/pkgconfig/Qt6OpenGL.pc
%{mingw32_libdir}/pkgconfig/Qt6OpenGLWidgets.pc
%{mingw32_libdir}/pkgconfig/Qt6Platform.pc
%{mingw32_libdir}/pkgconfig/Qt6PrintSupport.pc
%{mingw32_libdir}/pkgconfig/Qt6Sql.pc
%{mingw32_libdir}/pkgconfig/Qt6Test.pc
%{mingw32_libdir}/pkgconfig/Qt6Widgets.pc
%{mingw32_libdir}/pkgconfig/Qt6Xml.pc
%dir %{mingw32_includedir}/qt6/
%{mingw32_includedir}/qt6/*
%{mingw32_docdir}/qt6/

%dir %{_prefix}/%{mingw32_target}/bin/qt6/
%{_prefix}/%{mingw32_target}/bin/qt6/qmake
%{_prefix}/%{mingw32_target}/bin/qt6/qt-cmake
%{_prefix}/%{mingw32_target}/bin/qt6/qt-cmake-create
%{_prefix}/%{mingw32_target}/bin/qt6/qtpaths
%{_prefix}/%{mingw32_target}/bin/qt6/target_qt.conf
%{_bindir}/%{mingw32_target}-qmake-qt6
%{_bindir}/%{mingw32_target}-qt6-cmake


# Win64
%files -n mingw64-qt6-qtbase
%license LICENSES/GPL*
%license LICENSES/LGPL*
%{mingw64_bindir}/Qt6Concurrent.dll
%{mingw64_bindir}/Qt6Core.dll
%{mingw64_bindir}/Qt6DBus.dll
%{mingw64_bindir}/Qt6Gui.dll
%{mingw64_bindir}/Qt6Network.dll
%{mingw64_bindir}/Qt6OpenGL.dll
%{mingw64_bindir}/Qt6OpenGLWidgets.dll
%{mingw64_bindir}/Qt6PrintSupport.dll
%{mingw64_bindir}/Qt6Sql.dll
%{mingw64_bindir}/Qt6Test.dll
%{mingw64_bindir}/Qt6Widgets.dll
%{mingw64_bindir}/Qt6Xml.dll
%{mingw64_libdir}/libQt6Concurrent.dll.a
%{mingw64_libdir}/libQt6Core.dll.a
%{mingw64_libdir}/libQt6DBus.dll.a
%{mingw64_libdir}/libQt6ExampleIcons.a
%{mingw64_libdir}/libQt6ExamplesAssetDownloader.a
%{mingw64_libdir}/libQt6Gui.dll.a
%{mingw64_libdir}/libQt6Network.dll.a
%{mingw64_libdir}/libQt6OpenGL.dll.a
%{mingw64_libdir}/libQt6OpenGLWidgets.dll.a
%{mingw64_libdir}/libQt6PrintSupport.dll.a
%{mingw64_libdir}/libQt6Sql.dll.a
%{mingw64_libdir}/libQt6Test.dll.a
%{mingw64_libdir}/libQt6Widgets.dll.a
%{mingw64_libdir}/libQt6Xml.dll.a
%{mingw64_libdir}/libQt6DeviceDiscoverySupport.a
%{mingw64_libdir}/libQt6EntryPoint.a
%{mingw64_libdir}/libQt6FbSupport.a
%{mingw64_libdir}/Qt6Concurrent.prl
%{mingw64_libdir}/Qt6Core.prl
%{mingw64_libdir}/Qt6DBus.prl
%{mingw64_libdir}/Qt6DeviceDiscoverySupport.prl
%{mingw64_libdir}/Qt6EntryPoint.prl
%{mingw64_libdir}/Qt6ExampleIcons.prl
%{mingw64_libdir}/Qt6ExamplesAssetDownloader.prl
%{mingw64_libdir}/Qt6FbSupport.prl
%{mingw64_libdir}/Qt6Gui.prl
%{mingw64_libdir}/Qt6Network.prl
%{mingw64_libdir}/Qt6OpenGL.prl
%{mingw64_libdir}/Qt6OpenGLWidgets.prl
%{mingw64_libdir}/Qt6PrintSupport.prl
%{mingw64_libdir}/Qt6Sql.prl
%{mingw64_libdir}/Qt6Test.prl
%{mingw64_libdir}/Qt6Widgets.prl
%{mingw64_libdir}/Qt6Xml.prl
%dir %{mingw64_libdir}/qt6/
%dir %{mingw64_libdir}/qt6/bin/
%{mingw64_libdir}/qt6/bin/qt_cyclonedx_generator.py
%{mingw64_libdir}/qt6/bin/qt-cmake-private
%{mingw64_libdir}/qt6/bin/qt-cmake-private-install.cmake
%{mingw64_libdir}/qt6/bin/qt-cmake-standalone-test
%{mingw64_libdir}/qt6/bin/qt-internal-configure-examples
%{mingw64_libdir}/qt6/bin/qt-testrunner.py
%{mingw64_libdir}/qt6/bin/sanitizer-testrunner.py
%dir %{mingw64_libdir}/qt6/metatypes/
%{mingw64_libdir}/qt6/metatypes/qt6concurrent_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6core_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6dbus_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6devicediscoverysupportprivate_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6exampleiconsprivate_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6examplesassetdownloaderprivate_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6fbsupportprivate_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6gui_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6network_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6opengl_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6openglwidgets_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6printsupport_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6sql_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6test_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6widgets_metatypes.json
%{mingw64_libdir}/qt6/metatypes/qt6xml_metatypes.json
%{mingw64_libdir}/qt6/mkspecs/
%{mingw64_libdir}/qt6/modules/
%{mingw64_libdir}/qt6/modules/Concurrent.json
%{mingw64_libdir}/qt6/modules/Core.json
%{mingw64_libdir}/qt6/modules/DBus.json
%{mingw64_libdir}/qt6/modules/DeviceDiscoverySupportPrivate.json
%{mingw64_libdir}/qt6/modules/EntryPointPrivate.json
%{mingw64_libdir}/qt6/modules/FbSupportPrivate.json
%{mingw64_libdir}/qt6/modules/Gui.json
%{mingw64_libdir}/qt6/modules/Network.json
%{mingw64_libdir}/qt6/modules/OpenGL.json
%{mingw64_libdir}/qt6/modules/OpenGLWidgets.json
%{mingw64_libdir}/qt6/modules/PrintSupport.json
%{mingw64_libdir}/qt6/modules/Sql.json
%{mingw64_libdir}/qt6/modules/Test.json
%{mingw64_libdir}/qt6/modules/Widgets.json
%{mingw64_libdir}/qt6/modules/Xml.json
%dir %{mingw64_libdir}/qt6/plugins
%dir %{mingw64_libdir}/qt6/plugins/generic
%{mingw64_libdir}/qt6/plugins/generic/qtuiotouchplugin.dll
%dir %{mingw64_libdir}/qt6/plugins/imageformats
%{mingw64_libdir}/qt6/plugins/imageformats/qgif.dll
%{mingw64_libdir}/qt6/plugins/imageformats/qico.dll
%{mingw64_libdir}/qt6/plugins/imageformats/qjpeg.dll
%dir %{mingw64_libdir}/qt6/plugins/networkinformation
%{mingw64_libdir}/qt6/plugins/networkinformation/qnetworklistmanager.dll
%dir %{mingw64_libdir}/qt6/plugins/platforms
%{mingw64_libdir}/qt6/plugins/platforms/qdirect2d.dll
%{mingw64_libdir}/qt6/plugins/platforms/qoffscreen.dll
%{mingw64_libdir}/qt6/plugins/platforms/qminimal.dll
%{mingw64_libdir}/qt6/plugins/platforms/qwindows.dll
%dir %{mingw64_libdir}/qt6/plugins/sqldrivers
%{mingw64_libdir}/qt6/plugins/sqldrivers/qsqlite.dll
%{mingw64_libdir}/qt6/plugins/sqldrivers/qsqlodbc.dll
%{mingw64_libdir}/qt6/plugins/sqldrivers/qsqlpsql.dll
%dir %{mingw64_libdir}/qt6/plugins/styles
%{mingw64_libdir}/qt6/plugins/styles/qmodernwindowsstyle.dll
%dir %{mingw64_libdir}/qt6/plugins/tls
%{mingw64_libdir}/qt6/plugins/tls/qcertonlybackend.dll
%{mingw64_libdir}/qt6/plugins/tls/qopensslbackend.dll
%{mingw64_libdir}/qt6/plugins/tls/qschannelbackend.dll
%dir %{mingw64_libdir}/qt6/sbom/
%{mingw64_libdir}/qt6/sbom/%{qt_module}-%{qt_version}.spdx
%{mingw64_libdir}/cmake/Qt6/
%{mingw64_libdir}/cmake/Qt6BuildInternals/
%{mingw64_libdir}/cmake/Qt6Concurrent/
%{mingw64_libdir}/cmake/Qt6Core/
%{mingw64_libdir}/cmake/Qt6CorePrivate/
%{mingw64_libdir}/cmake/Qt6DBus/
%{mingw64_libdir}/cmake/Qt6DBusPrivate/
%{mingw64_libdir}/cmake/Qt6DeviceDiscoverySupportPrivate/
%{mingw64_libdir}/cmake/Qt6EntryPointPrivate/
%{mingw64_libdir}/cmake/Qt6ExampleIconsPrivate/
%{mingw64_libdir}/cmake/Qt6ExamplesAssetDownloaderPrivate/
%{mingw64_libdir}/cmake/Qt6FbSupportPrivate/
%{mingw64_libdir}/cmake/Qt6Gui/
%{mingw64_libdir}/cmake/Qt6GuiPrivate/
%{mingw64_libdir}/cmake/Qt6HostInfo/
%{mingw64_libdir}/cmake/Qt6Network/
%{mingw64_libdir}/cmake/Qt6NetworkPrivate/
%{mingw64_libdir}/cmake/Qt6OpenGL/
%{mingw64_libdir}/cmake/Qt6OpenGLPrivate/
%{mingw64_libdir}/cmake/Qt6OpenGLWidgets/
%{mingw64_libdir}/cmake/Qt6PrintSupport/
%{mingw64_libdir}/cmake/Qt6PrintSupportPrivate/
%{mingw64_libdir}/cmake/Qt6Sql/
%{mingw64_libdir}/cmake/Qt6SqlPrivate/
%{mingw64_libdir}/cmake/Qt6Test/
%{mingw64_libdir}/cmake/Qt6TestPrivate/
%{mingw64_libdir}/cmake/Qt6TestInternalsPrivate/
%{mingw64_libdir}/cmake/Qt6Widgets/
%{mingw64_libdir}/cmake/Qt6WidgetsPrivate/
%{mingw64_libdir}/cmake/Qt6Xml/
%{mingw64_libdir}/cmake/Qt6XmlPrivate/
%{mingw64_libdir}/pkgconfig/Qt6Concurrent.pc
%{mingw64_libdir}/pkgconfig/Qt6Core.pc
%{mingw64_libdir}/pkgconfig/Qt6DBus.pc
%{mingw64_libdir}/pkgconfig/Qt6Gui.pc
%{mingw64_libdir}/pkgconfig/Qt6Network.pc
%{mingw64_libdir}/pkgconfig/Qt6OpenGL.pc
%{mingw64_libdir}/pkgconfig/Qt6OpenGLWidgets.pc
%{mingw64_libdir}/pkgconfig/Qt6Platform.pc
%{mingw64_libdir}/pkgconfig/Qt6PrintSupport.pc
%{mingw64_libdir}/pkgconfig/Qt6Sql.pc
%{mingw64_libdir}/pkgconfig/Qt6Test.pc
%{mingw64_libdir}/pkgconfig/Qt6Widgets.pc
%{mingw64_libdir}/pkgconfig/Qt6Xml.pc
%dir %{mingw64_includedir}/qt6/
%{mingw64_includedir}/qt6/*
%{mingw64_docdir}/qt6/

%dir %{_prefix}/%{mingw64_target}/bin/qt6/
%{_prefix}/%{mingw64_target}/bin/qt6/qmake
%{_prefix}/%{mingw64_target}/bin/qt6/qt-cmake
%{_prefix}/%{mingw64_target}/bin/qt6/qt-cmake-create
%{_prefix}/%{mingw64_target}/bin/qt6/qtpaths
%{_prefix}/%{mingw64_target}/bin/qt6/target_qt.conf
%{_bindir}/%{mingw64_target}-qmake-qt6
%{_bindir}/%{mingw64_target}-qt6-cmake


%changelog
* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Thu Oct 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- Update 6.10.0 RC

* Tue Sep 02 2025 Sandro Mani <manisandro@gmail.com> - 6.9.2-1
- Update to 6.9.2

* Mon Aug 18 2025 Sandro Mani <manisandro@gmail.com> - 6.9.1-4
- Rebuild (icu)

* Fri Aug 15 2025 Sandro Mani <manisandro@gmail.com> - 6.9.1-3
- Rebuild (icu)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 09 2025 Sandro Mani <manisandro@gmail.com> - 6.9.1-1
- Update to 6.9.1

* Fri Apr 04 2025 Sandro Mani <manisandro@gmail.com> - 6.9.0-1
- Update to 6.9.0

* Tue Feb 04 2025 Sandro Mani <manisandro@gmail.com> - 6.8.2-1
- Update to 6.8.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 6.8.1-2
- Rebuild (mingw-icu)

* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 6.8.1-1
- Update to 6.8.1

* Fri Dec 06 2024 Sandro Mani <manisandro@gmail.com> - 6.8.0-2
- Rebuild (mingw-icu)

* Wed Oct 16 2024 Sandro Mani <manisandro@gmail.com> - 6.8.0-1
- Update to 6.8.0

* Tue Jul 30 2024 Sandro Mani <manisandro@gmail.com> - 6.7.2-3
- Apply fix for CVE-2024-39936

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Sandro Mani <manisandro@gmail.com> - 6.7.2-1
- Update to 6.7.2

* Sat May 25 2024 Sandro Mani <manisandro@gmail.com> - 6.7.1-1
- Update to 6.7.1

* Mon Apr 08 2024 Sandro Mani <manisandro@gmail.com> - 6.7.0-1
- Update to 6.7.0

* Sat Feb 17 2024 Sandro Mani <manisandro@gmail.com> - 6.6.2-1
- Update to 6.6.2

* Mon Feb 05 2024 Sandro Mani <manisandro@gmail.com> - 6.6.1-4
- Rebuild (icu)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Sandro Mani <manisandro@gmail.com> - 6.6.1-1
- Update to 6.6.1

* Tue Oct 17 2023 Sandro Mani <manisandro@gmail.com> - 6.6.0-1
- Update to 6.6.0

* Wed Oct 04 2023 Sandro Mani <manisandro@gmail.com> - 6.5.3-1
- Update to 6.5.3

* Sat Jul 29 2023 Sandro Mani <manisandro@gmail.com> - 6.5.2-1
- Update to 6.5.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 6.5.1-3
- Rebuild (mingw-icu)

* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 6.5.1-2
- Bump release

* Sun May 28 2023 Sandro Mani <manisandro@gmail.com> - 6.5.1-1
- Update to 6.5.1

* Thu Apr 06 2023 Sandro Mani <manisandro@gmail.com> - 6.5.0-1
- Update to 6.5.0

* Wed Mar 29 2023 Sandro Mani <manisandro@gmail.com> - 6.4.3-1
- Update to 6.4.3

* Tue Mar 28 2023 Sandro Mani <manisandro@gmail.com> - 6.4.2-1
- Update to 6.4.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Sandro Mani <manisandro@gmail.com> - 6.4.2-1
- Update to 6.4.2

* Tue Jan 03 2023 Sandro Mani <manisandro@gmail.com> - 6.4.1-3
- Rebuild (mingw-icu)

* Wed Dec 28 2022 Sandro Mani <manisandro@gmail.com> - 6.4.1-2
- Fix broken cross-target qmake

* Wed Nov 23 2022 Sandro Mani <manisandro@gmail.com> - 6.4.1-1
- Update to 6.4.1

* Fri Nov 18 2022 Sandro Mani <manisandro@gmail.com> - 6.4.0-2
- Rebuild (mingw-postgresql)

* Mon Oct 31 2022 Sandro Mani <manisandro@gmail.com> - 6.4.0-1
- Update to 6.4.0

* Mon Aug 08 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-4
- Backport upstream fix needed for Fedora MediaWriter on Windows

* Fri Aug 05 2022 Sandro Mani <manisandro@gmail.com> - 6.3.1-3
- Rebuild (icu)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Sandro Mani <manisandro@gmail.com> - 6.3.1-1
- Update to 6.3.1

* Sat Apr 23 2022 Sandro Mani <manisandro@gmail.com> - 6.3.0-1
- Update to 6.3.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 6.2.3-4
- Rebuild with mingw-gcc-12

* Sat Mar 05 2022 Sandro Mani <manisandro@gmail.com> - 6.2.3-3
- Re-enable s390x build

* Thu Feb 17 2022 Sandro Mani <manisandro@gmail.com> - 6.2.3-2
- Rebuild (openssl)

* Mon Jan 31 2022 Sandro Mani <manisandro@gmail.com> - 6.2.3-1
- Update to 6.2.3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Sandro Mani <manisandro@gmail.com> - 6.2.2-1
- Update to 6.2.2

* Mon Nov 01 2021 Sandro Mani <manisandro@gmail.com> - 6.2.1-1
- Update to 6.2.1

* Sat Oct 02 2021 Sandro Mani <manisandro@gmail.com> - 6.2.0-1
- Update to 6.2.0

* Mon Sep 27 2021 Sandro Mani <manisandro@gmail.com> - 6.2.0-0.2.rc2
- Update to 6.2.0-rc2

* Tue Sep 21 2021 Sandro Mani <manisandro@gmail.com> - 6.2.0-0.1.rc
- Update to 6.2.0-rc

* Thu Aug 12 2021 Sandro Mani <manisandro@gmail.com> - 6.1.2-1
- Update to 6.1.2

* Tue Aug 03 2021 Sandro Mani <manisandro@gmail.com> - 6.1.1-2
- Don't make packages noarch

* Tue Jul 06 2021 Sandro Mani <manisandro@gmail.com> - 6.1.1-1
- Initial package
