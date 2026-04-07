# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# explicitely set clang as toolchain to avoid gcc usage
%global toolchain clang

# needed to ship deploy_lib template files
%global _python_bytecompile_errors_terminate_build 0

%global pypi_name pyside6
%global camel_name PySide6
%global qt6ver 6.10.2

Name:           python-%{pypi_name}
Version:        6.10.2
Release:        1%{?dist}
Summary:        Python bindings for the Qt 6 cross-platform application and UI framework

License:        LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
URL:            https://wiki.qt.io/Qt_for_Python

Source0:        https://download.qt.io/official_releases/QtForPython/%{pypi_name}/%{camel_name}-%{qt6ver}-src/pyside-setup-everywhere-src-%{version}.tar.xz
# for documentation generation
%global docs 0
%global qt_module qtbase
%global  majmin %(echo %{version} | cut -d. -f1-2)
#Source1:	https://download.qt.io/official_releases/qt/%{majmin}/%{qt6ver}/submodules/%{qt_module}-everywhere-src-%{qt6ver}.tar.xz

# OpenSuse patches
Patch:          0001-Revert-Modify-headers-installation-for-CMake-builds.patch
Patch:          0001-Always-link-to-python-libraries.patch
Patch:          0001-Fix-installation.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  clang-devel
BuildRequires:  clang-tools-extra
BuildRequires:  llvm-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-packaging

BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  graphviz
BuildRequires:  python3-sphinx >= 7.4.7

%if 0%{?docs}
# for generating the documentation, see requirements-doc.txt
BuildRequires:  python3-sphinx-design >= 0.6.0
BuildRequires:  python3-sphinx-copybutton >= 0.5.2
BuildRequires:  python3-sphinx-tags >= 0.4
BuildRequires:  python3-sphinx-toolbox >= 3.7.0
BuildRequires:  python3-sphinx-reredirects >= 0.1.5
BuildRequires:  python3-myst-parser >= 3.0.1
BuildRequires:  python3-furo
%endif

# essential modules
BuildRequires:  cmake(Qt6Core) >= %{qt6ver}
BuildRequires:  cmake(Qt6Gui) >= %{qt6ver}
BuildRequires:  cmake(Qt6Widgets) >= %{qt6ver}
BuildRequires:  cmake(Qt6Help) >= %{qt6ver}
BuildRequires:  cmake(Qt6Network) >= %{qt6ver}
BuildRequires:  cmake(Qt6Concurrent) >= %{qt6ver}
BuildRequires:  cmake(Qt6DBus) >= %{qt6ver}
BuildRequires:  cmake(Qt6Designer) >= %{qt6ver}
BuildRequires:  cmake(Qt6OpenGL) >= %{qt6ver}
BuildRequires:  cmake(Qt6OpenGLWidgets) >= %{qt6ver}
BuildRequires:  cmake(Qt6PrintSupport) >= %{qt6ver}
BuildRequires:  cmake(Qt6Qml) >= %{qt6ver}
BuildRequires:  cmake(Qt6Quick) >= %{qt6ver}
BuildRequires:  cmake(Qt6QuickControls2) >= %{qt6ver}
BuildRequires:  cmake(Qt6Xml) >= %{qt6ver}
BuildRequires:  cmake(Qt6Test) >= %{qt6ver}
BuildRequires:  cmake(Qt6Sql) >= %{qt6ver}
BuildRequires:  qt6-qtbase-mysql >= %{qt6ver}
BuildRequires:  qt6-qtbase-odbc >= %{qt6ver}
BuildRequires:  qt6-qtbase-postgresql >= %{qt6ver}
BuildRequires:  cmake(Qt6Svg) >= %{qt6ver}
BuildRequires:  cmake(Qt6SvgWidgets) >= %{qt6ver}
BuildRequires:  cmake(Qt6UiTools) >= %{qt6ver}

BuildRequires:  qt6-qtbase-gui >= %{qt6ver}
BuildRequires:  qt6-qtbase-static >= %{qt6ver}

# from qt6-qtbase for XKB
BuildRequires: pkgconfig(xcb-xkb) >= 1.10
BuildRequires: pkgconfig(xcb-util)
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: pkgconfig(xkbcommon-x11) >= 0.4.1
BuildRequires: pkgconfig(xkeyboard-config)

# Add-On modules
BuildRequires:  cmake(Qt6Multimedia) >= %{qt6ver}
BuildRequires:  cmake(Qt6MultimediaWidgets) >= %{qt6ver}
BuildRequires:  cmake(Qt6Positioning) >= %{qt6ver}
BuildRequires:  cmake(Qt6Location) >= %{qt6ver}
BuildRequires:  cmake(Qt6NetworkAuth) >= %{qt6ver}
BuildRequires:  cmake(Qt6Nfc) >= %{qt6ver}
BuildRequires:  cmake(Qt6Quick3D) >= %{qt6ver}
BuildRequires:  cmake(Qt6QuickWidgets) >= %{qt6ver}
BuildRequires:  cmake(Qt6RemoteObjects) >= %{qt6ver}
BuildRequires:  cmake(Qt6Scxml) >= %{qt6ver}
BuildRequires:  cmake(Qt6Sensors) >= %{qt6ver}
BuildRequires:  cmake(Qt6SerialPort) >= %{qt6ver}
BuildRequires:  cmake(Qt6SerialBus) >= %{qt6ver}
BuildRequires:  cmake(Qt6StateMachine) >= %{qt6ver}
BuildRequires:  cmake(Qt6TextToSpeech) >= %{qt6ver}
BuildRequires:  cmake(Qt6Charts) >= %{qt6ver}
BuildRequires:  cmake(Qt6SpatialAudio) >= %{qt6ver}
BuildRequires:  cmake(Qt6DataVisualization) >= %{qt6ver}
BuildRequires:  cmake(Qt6Graphs) >= %{qt6ver}
BuildRequires:  cmake(Qt6Bluetooth) >= %{qt6ver}
BuildRequires:  cmake(Qt6WebChannel) >= %{qt6ver}
%ifarch %{qt6_qtwebengine_arches}
BuildRequires:  cmake(Qt6WebEngineCore) >= %{qt6ver}
BuildRequires:  cmake(Qt6WebEngineWidgets) >= %{qt6ver}
BuildRequires:  cmake(Qt6WebEngineQuick) >= %{qt6ver}
BuildRequires:  cmake(Qt6Pdf) >= %{qt6ver}
BuildRequires:  cmake(Qt6PdfWidgets) >= %{qt6ver}
BuildRequires:  cmake(Qt6WebView) >= %{qt6ver}
%endif
BuildRequires:  cmake(Qt6WebSockets) >= %{qt6ver}
BuildRequires:  cmake(Qt6HttpServer) >= %{qt6ver}
BuildRequires:  cmake(Qt63DCore) >= %{qt6ver}
BuildRequires:  cmake(Qt63DRender) >= %{qt6ver}
BuildRequires:  cmake(Qt63DInput) >= %{qt6ver}
BuildRequires:  cmake(Qt63DLogic) >= %{qt6ver}
BuildRequires:  cmake(Qt63DAnimation) >= %{qt6ver}
BuildRequires:  cmake(Qt63DExtras) >= %{qt6ver}

BuildRequires:  qt6-qtbase-private-devel >= %{qt6ver}

# Qt Tools
BuildRequires:  cmake(Qt6UiPlugin) >= %{qt6ver}
BuildRequires:  qt6-assistant >= %{qt6ver}
BuildRequires:  qt6-designer >= %{qt6ver}
BuildRequires:  qt6-doctools >= %{qt6ver}

# Tests use a fake graphical environment
BuildRequires:  /usr/bin/wlheadless-run
BuildRequires:  mesa-dri-drivers

%description
PySide6 is the official Python module from the Qt for Python project, which
provides access to the complete Qt 6+ framework.


%package -n     python%{python3_pkgversion}-%{pypi_name}
Provides:       python%{python3_pkgversion}-%{camel_name} = %{version}-%{release}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{camel_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
PySide6 is the official Python module from the Qt for Python project, which
provides access to the complete Qt 6 framework.


%package -n     python%{python3_pkgversion}-%{pypi_name}-devel
Requires:       pyside6-tools
Requires:       shiboken6
Summary:        Development files related to %{name}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}-devel}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{camel_name}-devel}

%description -n python%{python3_pkgversion}-%{pypi_name}-devel
%{summary}.


%package -n pyside6-tools
Requires:       qt6-qtbase-devel
Requires:       qt6-qtdeclarative-devel
Requires:       qt6-assistant
Requires:       qt6-designer
Requires:       qt6-linguist
Requires:       python3-%{pypi_name}
Summary:        PySide6 tools for the Qt 6 framework

%description -n pyside6-tools
PySide6 provides Python bindings for the Qt6 cross-platform application
and UI framework.


%package -n shiboken6
Summary:        Python / C++ bindings generator for %camel_name

%description -n shiboken6
Shiboken is the Python binding generator that Qt for Python uses to create the
PySide module, in other words, is the system we use to expose the Qt C++ API to
Python.


%package -n python%{python3_pkgversion}-shiboken6
Summary:        Python / C++ bindings libraries for %camel_name

%description -n python%{python3_pkgversion}-shiboken6
Shiboken is the Python binding generator that Qt for Python uses to create the
PySide module, in other words, is the system we use to expose the Qt C++ API to
Python.


%package -n python%{python3_pkgversion}-shiboken6-devel
Summary:        Python / C++ bindings helper module for %camel_name
Requires:       shiboken6
Requires:       python%{python3_pkgversion}-shiboken6

%description -n python%{python3_pkgversion}-shiboken6-devel
Shiboken is the Python binding generator that Qt for Python uses to create the
PySide module, in other words, is the system we use to expose the Qt C++ API to
Python.

%if 0%{?docs}
%package doc
Summary: Qt API Documentation in HTML and QCH format
%description doc
%{summary}.
%endif


%prep
%autosetup -p1 -n pyside-setup-everywhere-src-%{qt6ver}
# https://build.opensuse.org/package/view_file/KDE:Qt6/python3-pyside6/python3-pyside6.spec?expand=1
# Restore 6.6.1 RPATH value. rpmlint will complain otherwise
sed -i 's#${base}/../shiboken6/##' sources/pyside6/CMakeLists.txt

%if 0%{?docs}
# Generate documentation, requires qtbase sources as parameter
# sphinx-build output accepts several options of the format, default is html, use qthelp which calls qhelpgenerator for qch file generation
tar xf %{SOURCE1}
%endif

%build
# https://src.fedoraproject.org/rpms/polyclipping/c/02c70e17ef9e9fcdfbc65021418a3e332e465b20?branch=rawhide
# Prior to Fedora 43, %%cmake set the nonstandard -DLIB_SUFFIX=... variable.
# cmake %["%{?_lib}" == "lib64" ? "-DLIB_SUFFIX=64" : ""]
%cmake_qt6 %["%{?_lib}" == "lib64" ? "-DLIB_SUFFIX=64" : ""] \
    -DCMAKE_BUILD_TYPE=None \
    -DSHIBOKEN_PYTHON_LIBRARIES=`pkgconf python3-embed --libs` \
    -DBUILD_TESTS=OFF \
    -DCMAKE_BUILD_RPATH_USE_ORIGIN:BOOL=ON \
    -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
    -DFORCE_LIMITED_API=no \
%if 0%{?docs}
    -DBUILD_DOCS:BOOL=ON \
    -DQT_SRC_DIR= %{qt_module}-everywhere-src-%{qt6ver} \
    -DFULLDOCSBUILD:BOOL=ON \
    -DDOC_OUTPUT_FORMAT=qthelp \
%endif
    -DNO_QT_TOOLS=yes

# Generate a build_history entry (for tests) manually, since we're performing
# a cmake build.
TODAY=$(date -Id)
mkdir build_history/$TODAY
echo $PWD/%{__cmake_builddir}/sources > build_history/$TODAY/build_dir.txt
export PYTHONPATH=$PWD/%{__cmake_builddir}/sources

%cmake_build
%if 0%{?docs}
# build api documentation
cd redhat-linux-build
ninja apidoc
%endif


%install
%cmake_install
%if 0%{?docs}
# install api documentation
cd redhat-linux-build
ninja apidocinstall
%endif

# Generate egg-info manually and install since we're performing a cmake build.
#
# Copy CMake configuration files from the BINARY dir back to the SOURCE dir so
# setuptools can find them.
cp %{__cmake_builddir}/sources/shiboken6/shibokenmodule/{*.py,*.txt} sources/shiboken6/shibokenmodule/
cp %{__cmake_builddir}/sources/pyside6/PySide6/*.py sources/pyside6/PySide6/
%{__python3} setup.py --qtpaths=/usr/%{_lib}/qt6/bin/qtpaths install_scripts --install-dir=%{buildroot}%{_bindir}
for name in PySide6 shiboken6 shiboken6_generator; do
  mkdir -p %{buildroot}%{python3_sitearch}/$name-%{version}-py%{python3_version}.egg-info
  cp -p $name.egg-info/{PKG-INFO,top_level.txt} \
        %{buildroot}%{python3_sitearch}/$name-%{version}-py%{python3_version}.egg-info/
  if [ -f $name.egg-info/entry_points.txt ]; then
    cp -p $name.egg-info/entry_points.txt %{buildroot}%{python3_sitearch}/$name-%{version}-py%{python3_version}.egg-info/
  fi
done

# Add symlinks for tools used by pyside_tool.py
mkdir -p %{buildroot}%{python3_sitelib}/%{camel_name}/Qt/libexec
ln -sf /usr/%{_lib}/qt6/libexec/{qmlcachegen,qmlimportscanner,qmltyperegistrar,rcc,uic} %{buildroot}%{python3_sitelib}/%{camel_name}/Qt/libexec
ln -sf /usr/%{_lib}/qt6/bin/{assistant,balsam,balsamui,designer,linguist,lrelease,lupdate,qmlformat,qmllint,qmlls,qsb} %{buildroot}%{python3_sitelib}/%{camel_name}

# Create scripts folders (this basically replicates prepare_packages() in build_scripts/main.py)
mkdir -p %{buildroot}%{python3_sitelib}/%{camel_name}/scripts
mv %{buildroot}%{_bindir}/{android_deploy.py,deploy_lib,deploy.py,metaobjectdump.py,project_lib,project.py,pyside_tool.py,qml.py,qtpy2cpp_lib,qtpy2cpp.py,requirements-android.txt} %{buildroot}%{python3_sitelib}/%{camel_name}/scripts
mkdir -p %{buildroot}%{python3_sitelib}/shiboken6_generator/scripts
mv %{buildroot}%{_bindir}/shiboken_tool.py %{buildroot}%{python3_sitelib}/shiboken6_generator/scripts

# Install shiboken6
mv redhat-linux-build/sources/shiboken6/generator/shiboken6 %{buildroot}%{python3_sitelib}/shiboken6_generator

# Fix CMake config files to use correct absolute paths (OpenSUSE solution)
# The upstream build is designed for wheel installation with relative paths,
# but for system installation we need absolute paths
sed -i 's#/typesystems#/share/PySide6/typesystems#g' %{buildroot}%{_libdir}/cmake/PySide6/*.cmake
sed -i 's#/glue#/share/PySide6/glue#g' %{buildroot}%{_libdir}/cmake/PySide6/*.cmake

# Fix all Python shebangs recursively
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# Need to list files that do not match ^[a-zA-Z0-9_]+\.py$ explicitly!
%py3_shebang_fix %{buildroot}%{python3_sitelib}/%{camel_name}/scripts
%py3_shebang_fix %{buildroot}%{python3_sitelib}/shiboken6_generator/scripts

%check
# Do basic import test (even without the test bcond)
export LD_LIBRARY_PATH="%{buildroot}%{_libdir}"
%py3_check_import PySide6
%py3_check_import shiboken6


%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSES/*
%doc README.md
%{_libdir}/libpyside6*.so.6.10*
%{python3_sitelib}/%{camel_name}/
%{python3_sitearch}/%{camel_name}-%{version}-py%{python3_version}.egg-info/

%files -n python%{python3_pkgversion}-%{pypi_name}-devel
%{_datadir}/PySide6/
%{_includedir}/PySide6/
%{_libdir}/libpyside6*.so
%{_libdir}/libpyside6remoteobjects.a
%{_libdir}/cmake/PySide6*
%{_libdir}/pkgconfig/pyside6.pc

%files -n pyside6-tools
%doc README.pyside*
%license LICENSES/*
%{_bindir}/pyside*
%{_libdir}/qt6/plugins/designer/libPySidePlugin.so

%files -n shiboken6
%doc README.shiboken6-generator.md
%license LICENSES/*
%{_libdir}/cmake/Shiboken6Tools/*

%files -n python%{python3_pkgversion}-shiboken6
%doc README.shiboken6.md
%license LICENSES/*
%{_libdir}/libshiboken6*.so.6.10*
%{python3_sitelib}/shiboken6/
%{python3_sitearch}/shiboken6-%{version}-py%{python3_version}.egg-info/

%files -n python%{python3_pkgversion}-shiboken6-devel
%{_bindir}/shiboken6*
%{_includedir}/shiboken6/
%{_libdir}/cmake/Shiboken6/
%{_libdir}/libshiboken6*.so
%{_libdir}/pkgconfig/shiboken6.pc
%{python3_sitelib}/shiboken6_generator/
%{python3_sitearch}/shiboken6_generator-%{version}-py%{python3_version}.egg-info/

%if 0%{?docs}
%files doc
%{_docdir}/
%endif

%changelog
* Tue Feb 10 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Dec 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-2
- Fix cmake config files

* Mon Dec 01 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Sat Nov 22 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-4
- Rebuild (qt6)

* Tue Sep 30 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-3
- Rebuild (qt6)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.9.2-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 01 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 6.9.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 08 2025 Python Maint <python-maint@redhat.com> - 6.9.1-2
- Rebuilt for Python 3.14

* Fri Jun 06 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 6.9.0-2
- Rebuilt for Python 3.14

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Tue Mar 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2.1-3
- Rebuild (qt6)

* Sun Mar 16 2025 Marie Loise Nolden <loise@kde.org> - 6.8.2.1-2
- fix build due to %cmake macro change after removal of -DLIB_SUFFIX in rawhide
- prepare documentation build

* Fri Feb 07 2025 Marie Loise Nolden <loise@kde.org> - 6.8.2.1-1
- 6.8.2.1

* Mon Feb 03 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.1.1-3
- Rebuild (qt6)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 05 2025 Marie Loise Nolden <loise@kde.org> - 6.8.1-1
- 6.8.1.1

* Sun Dec 08 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-2
- Rebuild (qt6.8.1)

* Tue Oct 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-5
- Rebuild (qt6)

* Fri Aug 09 2024 Federico Pellegrin <fede@evolware.org> - 6.7.2-4
- Fix pyside6-tools dependencies on python3-pyside

* Wed Jul 31 2024 LuK1337 <priv.luk@gmail.com> - 6.7.2-3
- unbreak python console scripts

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 06 2024 LuK1337 <priv.luk@gmail.com> - 6.7.2-1
- 6.7.2

* Tue Jun 18 2024 LuK1337 <priv.luk@gmail.com> - 6.7.1-3
- fix Python 3.13 build

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 6.7.1-2
- Rebuilt for Python 3.13

* Wed May 29 2024 LuK1337 <priv.luk@gmail.com> - 6.7.1-1
- 6.7.1

* Fri Apr 12 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Sun Mar 24 2024 Marie Loise Nolden <loise@kde.org> - 6.6.2-2
- add  -DFORCE_LIMITED_API=no for freecad building (thanks to nvwarr@hotmail.com) (in rhbz #2266591)
- set toolchain to clang for correct build (rhbz #2271188)

* Mon Feb 19 2024 Marie Loise Nolden <loise@kde.org> - 6.6.2-1
- Initial package
