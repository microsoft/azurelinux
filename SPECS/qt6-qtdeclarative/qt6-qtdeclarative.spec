# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global qt_module qtdeclarative

%define _lto_cflags %{nil}

# definition borrowed from qtbase
%global multilib_archs x86_64 %{ix86} %{?mips} ppc64 ppc s390x s390 sparc64 sparcv9

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

%global examples 1

Summary: Qt6 - QtDeclarative component
Name:    qt6-%{qt_module}
Version: 6.10.2
Release: 2%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

# header file to workaround multilib issue
# https://bugzilla.redhat.com/show_bug.cgi?id=1441343
Source5: qv4global_p-multilib.h

## upstream patches
# https://codereview.qt-project.org/c/qt/qtdeclarative/+/678924
Patch0:  qtdeclarative-quickshapes-make-module-public.patch
Patch1:  qtdeclarative-qtqml-do-not-clear-objects-propertycaches-on-last-gc-run.patch

## upstreamable patches

# filter qml provides
%global __provides_exclude_from ^%{_qt6_qmldir}/.*\\.so$

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: ninja-build
BuildRequires: qt6-rpm-macros
BuildRequires: qt6-qtbase-devel >= %{version}
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-qtbase-static
BuildRequires: qt6-qtlanguageserver-devel >= %{version}
BuildRequires: qt6-qtshadertools-devel >= %{version}
BuildRequires: qt6-qtsvg-devel >= %{version}
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: python%{python3_pkgversion}
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1

%if 0%{?tests}
BuildRequires: dbus-x11
BuildRequires: mesa-dri-drivers
BuildRequires: time
BuildRequires: xorg-x11-server-Xvfb
%endif

Obsoletes:     qt6-qtquickcontrols2 < 6.2.0~beta3-1
Provides:      qt6-qtquickcontrols2 = %{version}-%{release}

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Provides:  %{name}-private-devel = %{version}-%{release}
Requires:  %{name}%{?_isa} = %{version}-%{release}
Requires:  qt6-qtbase-devel%{?_isa}
Obsoletes: qt6-qtquickcontrols2-devel < 6.2.0~beta3-1
Provides:  qt6-qtquickcontrols2-devel = %{version}-%{release}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires:  %{name}%{?_isa} = %{version}-%{release}
Obsoletes: qt6-qtquickcontrols2-examples < 6.2.0~beta3-1
Provides:  qt6-qtquickcontrols2-examples = %{version}-%{release}
# BuildRequires: qt6-qtdeclarative-devel >= %{version}
%description examples
%{summary}.
%endif

%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1


%build

# HACK so calls to "python" get what we want
ln -s %{__python3} python
export PATH=`pwd`:$PATH

%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install

%ifarch %{multilib_archs}
# multilib: qv4global_p.h
  mv %{buildroot}%{_qt6_headerdir}/QtQml/%{qt_version}/QtQml/private/qv4global_p.h \
     %{buildroot}%{_qt6_headerdir}/QtQml/%{qt_version}/QtQml/private/qv4global_p-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt6_headerdir}/QtQml/%{qt_version}/QtQml/private/qv4global_p.h
%endif

# hardlink files to %{_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
    qmlcachegen|qmlleasing|qmlformat|qmleasing|qmlimportscanner|qmllint| \
    qmlpreview|qmlscene|qmltestrunner|qmltyperegistrar|qmlplugindump| \
    qmlprofiler|qml|qmlbundle|qmlmin|qmltime)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  rm -fv "$(basename ${prl_file} .prl).la"
  sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
done
popd

%check
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt6_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt6_libdir}
make sub-tests-all %{?_smp_mflags}
xvfb-run -a \
dbus-launch --exit-with-session \
time \
make check -k -C tests ||:
%endif


%ldconfig_scriptlets

%files
%license LICENSES/LGPL*
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%{_qt6_libdir}/libQt6LabsAnimation.so.6*
%{_qt6_libdir}/libQt6LabsFolderListModel.so.6*
%{_qt6_libdir}/libQt6LabsPlatform.so.6*
%{_qt6_libdir}/libQt6LabsQmlModels.so.6*
%{_qt6_libdir}/libQt6LabsSettings.so.6*
%{_qt6_libdir}/libQt6LabsSynchronizer.so.6*
%{_qt6_libdir}/libQt6LabsSharedImage.so.6*
%{_qt6_libdir}/libQt6LabsWavefrontMesh.so.6*
%{_qt6_libdir}/libQt6Qml.so.6*
%{_qt6_libdir}/libQt6QmlCompiler.so.*
%{_qt6_libdir}/libQt6QmlCore.so.6*
%{_qt6_libdir}/libQt6QmlLocalStorage.so.6*
%{_qt6_libdir}/libQt6QmlMeta.so.6*
%{_qt6_libdir}/libQt6QmlModels.so.6*
%{_qt6_libdir}/libQt6QmlNetwork.so.6*
%{_qt6_libdir}/libQt6QmlWorkerScript.so.6*
%{_qt6_libdir}/libQt6QmlXmlListModel.so.6*
%{_qt6_libdir}/libQt6Quick.so.6*
%{_qt6_libdir}/libQt6QuickControls2.so.6*
%{_qt6_libdir}/libQt6QuickControls2Basic.so.6*
%{_qt6_libdir}/libQt6QuickControls2BasicStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2FluentWinUI3StyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Fusion.so.6*
%{_qt6_libdir}/libQt6QuickControls2FusionStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Imagine.so.6*
%{_qt6_libdir}/libQt6QuickControls2ImagineStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Impl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Material.so.6*
%{_qt6_libdir}/libQt6QuickControls2MaterialStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickControls2Universal.so.6*
%{_qt6_libdir}/libQt6QuickControls2UniversalStyleImpl.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2QuickImpl.so.6*
%{_qt6_libdir}/libQt6QuickDialogs2Utils.so.6*
%{_qt6_libdir}/libQt6QuickEffects.so.6*
%{_qt6_libdir}/libQt6QuickLayouts.so.6*
%{_qt6_libdir}/libQt6QuickParticles.so.6*
%{_qt6_libdir}/libQt6QuickShapes.so.6*
%{_qt6_libdir}/libQt6QuickShapesDesignHelpers.so.6*
%{_qt6_libdir}/libQt6QuickTemplates2.so.6*
%{_qt6_libdir}/libQt6QuickTest.so.6*
%{_qt6_libdir}/libQt6QuickVectorImageHelpers.so.6*
%{_qt6_libdir}/libQt6QuickVectorImage.so.6*
%{_qt6_libdir}/libQt6QuickVectorImageGenerator.so.6*
%{_qt6_libdir}/libQt6QuickWidgets.so.6*
%{_qt6_plugindir}/qmltooling/
%{_qt6_plugindir}/qmllint/
%{_qt6_plugindir}/qmlls/
%dir %{_qt6_qmldir}
%{_qt6_qmldir}/QML/
%{_qt6_qmldir}/QmlTime/
%{_qt6_qmldir}/Qt/
%{_qt6_qmldir}/QtCore/
%{_qt6_qmldir}/QtNetwork/
%{_qt6_qmldir}/QtQml/
%{_qt6_qmldir}/QtQuick/
%{_qt6_qmldir}/QtTest/
%{_qt6_qmldir}/builtins.qmltypes
%{_qt6_qmldir}/jsroot.qmltypes

%files devel
%dir %{_qt6_libdir}/cmake/Qt6LabsAnimation
%dir %{_qt6_libdir}/cmake/Qt6LabsFolderListModel
%dir %{_qt6_libdir}/cmake/Qt6LabsPlatform
%dir %{_qt6_libdir}/cmake/Qt6LabsQmlModels
%dir %{_qt6_libdir}/cmake/Qt6LabsSettings
%dir %{_qt6_libdir}/cmake/Qt6LabsSharedImage
%dir %{_qt6_libdir}/cmake/Qt6LabsSynchronizer
%dir %{_qt6_libdir}/cmake/Qt6LabsWavefrontMesh
%dir %{_qt6_libdir}/cmake/Qt6Qml
%dir %{_qt6_libdir}/cmake/Qt6QmlCompiler
%dir %{_qt6_libdir}/cmake/Qt6QmlCore
%dir %{_qt6_libdir}/cmake/Qt6QuickEffects
%dir %{_qt6_libdir}/cmake/Qt6QmlImportScanner
%dir %{_qt6_libdir}/cmake/Qt6QmlIntegration
%dir %{_qt6_libdir}/cmake/Qt6QmlLocalStorage
%dir %{_qt6_libdir}/cmake/Qt6QmlMeta
%dir %{_qt6_libdir}/cmake/Qt6QmlModels
%dir %{_qt6_libdir}/cmake/Qt6QmlNetwork
%dir %{_qt6_libdir}/cmake/Qt6QmlTools
%dir %{_qt6_libdir}/cmake/Qt6QmlWorkerScript
%dir %{_qt6_libdir}/cmake/Qt6QmlXmlListModel
%dir %{_qt6_libdir}/cmake/Qt6Quick
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Basic
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2BasicStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2FluentWinUI3StyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Fusion
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2FusionStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Imagine
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2ImagineStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Impl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Material
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2MaterialStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Universal
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2UniversalStyleImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2QuickImpl
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2Utils
%dir %{_qt6_libdir}/cmake/Qt6QuickLayouts
%dir %{_qt6_libdir}/cmake/Qt6QuickShapes
%dir %{_qt6_libdir}/cmake/Qt6QuickTemplates2
%dir %{_qt6_libdir}/cmake/Qt6QuickTest
%dir %{_qt6_libdir}/cmake/Qt6QuickTools
%dir %{_qt6_libdir}/cmake/Qt6QuickVectorImage
%dir %{_qt6_libdir}/cmake/Qt6QuickVectorImageHelpers/
%dir %{_qt6_libdir}/cmake/Qt6QuickWidgets
%{_bindir}/qml*
%{_bindir}/svgtoqml
%{_qt6_bindir}/qml*
%{_qt6_bindir}/svgtoqml
%{_qt6_libexecdir}/qmlcachegen
%{_qt6_libexecdir}/qmlimportscanner
%{_qt6_libexecdir}/qmltyperegistrar
%{_qt6_libexecdir}/qmljsrootgen
%{_qt6_libexecdir}/qmlaotstats
%{_qt6_headerdir}/QtLabs*/
%{_qt6_headerdir}/QtQml/
%{_qt6_headerdir}/QtQmlCompiler/
%{_qt6_headerdir}/QtQmlCore/
%{_qt6_headerdir}/QtQmlIntegration/
%{_qt6_headerdir}/QtQmlFormat/
%{_qt6_headerdir}/QtQmlLocalStorage/
%{_qt6_headerdir}/QtQmlMeta/
%{_qt6_headerdir}/QtQmlModels/
%{_qt6_headerdir}/QtQmlNetwork/
%{_qt6_headerdir}/QtQmlWorkerScript/
%{_qt6_headerdir}/QtQmlXmlListModel/
%{_qt6_headerdir}/QtQuick/
%{_qt6_headerdir}/QtQuickControls2*StyleImpl/
%{_qt6_headerdir}/QtQuickControls2/
%{_qt6_headerdir}/QtQuickControls2Basic/
%{_qt6_headerdir}/QtQuickControls2Fusion/
%{_qt6_headerdir}/QtQuickControls2Imagine/
%{_qt6_headerdir}/QtQuickControls2Impl/
%{_qt6_headerdir}/QtQuickControls2Material/
%{_qt6_headerdir}/QtQuickControls2Universal/
%{_qt6_headerdir}/QtQuickDialogs2/
%{_qt6_headerdir}/QtQuickDialogs2QuickImpl/
%{_qt6_headerdir}/QtQuickDialogs2Utils/
%{_qt6_headerdir}/QtQuickEffects/
%{_qt6_headerdir}/QtQuickLayouts/
%{_qt6_headerdir}/QtQuickParticles/
%{_qt6_headerdir}/QtQuickShapes/
%{_qt6_headerdir}/QtQuickShapesDesignHelpers/
%{_qt6_headerdir}/QtQuickTemplates2/
%{_qt6_headerdir}/QtQuickTest/
%{_qt6_headerdir}/QtQuickVectorImage/
%{_qt6_headerdir}/QtQuickVectorImageGenerator/
%{_qt6_headerdir}/QtQuickVectorImageHelpers/
%{_qt6_headerdir}/QtQuickWidgets/
%{_qt6_libdir}/libQt6Labs*.prl
%{_qt6_libdir}/libQt6Labs*.so
%{_qt6_libdir}/libQt6Qml.prl
%{_qt6_libdir}/libQt6Qml.so
%{_qt6_libdir}/libQt6QmlCompiler.prl
%{_qt6_libdir}/libQt6QmlCompiler.so
%{_qt6_libdir}/libQt6QmlCore.prl
%{_qt6_libdir}/libQt6QmlCore.so
%{_qt6_libdir}/libQt6QmlLocalStorage.prl
%{_qt6_libdir}/libQt6QmlLocalStorage.so
%{_qt6_libdir}/libQt6QmlMeta.prl
%{_qt6_libdir}/libQt6QmlMeta.so
%{_qt6_libdir}/libQt6QmlModels.prl
%{_qt6_libdir}/libQt6QmlModels.so
%{_qt6_libdir}/libQt6QmlNetwork.prl
%{_qt6_libdir}/libQt6QmlNetwork.so
%{_qt6_libdir}/libQt6QmlWorkerScript.prl
%{_qt6_libdir}/libQt6QmlWorkerScript.so
%{_qt6_libdir}/libQt6QmlXmlListModel.prl
%{_qt6_libdir}/libQt6QmlXmlListModel.so
%{_qt6_libdir}/libQt6Quick*Impl.prl
%{_qt6_libdir}/libQt6Quick*Impl.so
%{_qt6_libdir}/libQt6Quick.prl
%{_qt6_libdir}/libQt6Quick.so
%{_qt6_libdir}/libQt6QuickControls2.prl
%{_qt6_libdir}/libQt6QuickControls2.so
%{_qt6_libdir}/libQt6QuickControls2Basic.prl
%{_qt6_libdir}/libQt6QuickControls2Basic.so
%{_qt6_libdir}/libQt6QuickControls2Fusion.prl
%{_qt6_libdir}/libQt6QuickControls2Fusion.so
%{_qt6_libdir}/libQt6QuickControls2Imagine.prl
%{_qt6_libdir}/libQt6QuickControls2Imagine.so
%{_qt6_libdir}/libQt6QuickControls2Material.prl
%{_qt6_libdir}/libQt6QuickControls2Material.so
%{_qt6_libdir}/libQt6QuickControls2Universal.prl
%{_qt6_libdir}/libQt6QuickControls2Universal.so
%{_qt6_libdir}/libQt6QuickDialogs2.prl
%{_qt6_libdir}/libQt6QuickDialogs2.so
%{_qt6_libdir}/libQt6QuickDialogs2Utils.prl
%{_qt6_libdir}/libQt6QuickDialogs2Utils.so
%{_qt6_libdir}/libQt6QuickEffects.prl
%{_qt6_libdir}/libQt6QuickEffects.so
%{_qt6_libdir}/libQt6QuickLayouts.prl
%{_qt6_libdir}/libQt6QuickLayouts.so
%{_qt6_libdir}/libQt6QuickParticles.prl
%{_qt6_libdir}/libQt6QuickParticles.so
%{_qt6_libdir}/libQt6QuickShapes.prl
%{_qt6_libdir}/libQt6QuickShapes.so
%{_qt6_libdir}/libQt6QuickShapesDesignHelpers.prl
%{_qt6_libdir}/libQt6QuickShapesDesignHelpers.so
%{_qt6_libdir}/libQt6QuickTemplates2.prl
%{_qt6_libdir}/libQt6QuickTemplates2.so
%{_qt6_libdir}/libQt6QuickTest.prl
%{_qt6_libdir}/libQt6QuickTest.so
%{_qt6_libdir}/libQt6QuickVectorImage.prl
%{_qt6_libdir}/libQt6QuickVectorImage.so
%{_qt6_libdir}/libQt6QuickVectorImageGenerator.prl
%{_qt6_libdir}/libQt6QuickVectorImageGenerator.so
%{_qt6_libdir}/libQt6QuickVectorImageHelpers.prl
%{_qt6_libdir}/libQt6QuickVectorImageHelpers.so
%{_qt6_libdir}/libQt6QuickWidgets.prl
%{_qt6_libdir}/libQt6QuickWidgets.so
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtDeclarativeTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6LabsAnimation/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsFolderListModel/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsPlatform/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsQmlModels/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSettings/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSharedImage/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSynchronizer/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsWavefrontMesh/*.cmake
%{_qt6_libdir}/cmake/Qt6Qml/*.cmake*
%{_qt6_libdir}/cmake/Qt6Qml/*.conf.in
%{_qt6_libdir}/cmake/Qt6Qml/*.cpp.in
%{_qt6_libdir}/cmake/Qt6Qml/*.qrc.in
%{_qt6_libdir}/cmake/Qt6Qml/QmlPlugins/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlCompiler/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlCore/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickEffects/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlImportScanner/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlIntegration/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlLocalStorage/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlMeta/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlModels/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlNetwork/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlTools/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlWorkerScript/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlXmlListModel/*.cmake
%{_qt6_libdir}/cmake/Qt6Quick/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Basic/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2BasicStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2FluentWinUI3StyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Fusion/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2FusionStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Imagine/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2ImagineStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Impl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Material/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2MaterialStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Universal/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2UniversalStyleImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2QuickImpl/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2Utils/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickLayouts/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickShapes/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTemplates2/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTest/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTools/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickVectorImage/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickVectorImageHelpers/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickWidgets/*.cmake
%dir %{_qt6_mkspecsdir}/features
%{_qt6_mkspecsdir}/features/qmlcache.prf
%{_qt6_mkspecsdir}/features/qmltypes.prf
%{_qt6_mkspecsdir}/features/qtquickcompiler.prf
%{_qt6_descriptionsdir}/Labs*.json
%{_qt6_descriptionsdir}/Qml.json
%{_qt6_descriptionsdir}/QmlCompiler.json
%{_qt6_descriptionsdir}/QmlCore.json
%{_qt6_descriptionsdir}/QmlIntegration.json
%{_qt6_descriptionsdir}/QuickEffects.json
%{_qt6_descriptionsdir}/QmlLocalStorage.json
%{_qt6_descriptionsdir}/QmlMeta.json
%{_qt6_descriptionsdir}/QmlModels.json
%{_qt6_descriptionsdir}/QmlNetwork.json
%{_qt6_descriptionsdir}/QmlWorkerScript.json
%{_qt6_descriptionsdir}/QmlXmlListModel.json
%{_qt6_descriptionsdir}/Quick.json
%{_qt6_descriptionsdir}/QuickControls2*Impl.json
%{_qt6_descriptionsdir}/QuickControls2.json
%{_qt6_descriptionsdir}/QuickControls2Basic.json
%{_qt6_descriptionsdir}/QuickControls2Fusion.json
%{_qt6_descriptionsdir}/QuickControls2Imagine.json
%{_qt6_descriptionsdir}/QuickControls2Material.json
%{_qt6_descriptionsdir}/QuickControls2Universal.json
%{_qt6_descriptionsdir}/QuickDialogs2.json
%{_qt6_descriptionsdir}/QuickDialogs2QuickImpl.json
%{_qt6_descriptionsdir}/QuickDialogs2Utils.json
%{_qt6_descriptionsdir}/QuickLayouts.json
%{_qt6_descriptionsdir}/QuickShapes.json
%{_qt6_descriptionsdir}/QuickTemplates2.json
%{_qt6_descriptionsdir}/QuickTest.json
%{_qt6_descriptionsdir}/QuickVectorImage.json
%{_qt6_descriptionsdir}/QuickVectorImageHelpers.json
%{_qt6_descriptionsdir}/QuickWidgets.json
%{_qt6_metatypesdir}/qt6labs*_metatypes.json
%{_qt6_metatypesdir}/qt6qml_metatypes.json
%{_qt6_metatypesdir}/qt6qmlcompiler_metatypes.json
%{_qt6_metatypesdir}/qt6qmlcore_metatypes.json
%{_qt6_metatypesdir}/qt6qmllocalstorage_metatypes.json
%{_qt6_metatypesdir}/qt6qmlmeta_metatypes.json
%{_qt6_metatypesdir}/qt6qmlmodels_metatypes.json
%{_qt6_metatypesdir}/qt6qmlnetwork_metatypes.json
%{_qt6_metatypesdir}/qt6qmlworkerscript_metatypes.json
%{_qt6_metatypesdir}/qt6qmlxmllistmodel_metatypes.json
%{_qt6_metatypesdir}/qt6quick*impl*_metatypes.json
%{_qt6_metatypesdir}/qt6quick_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2_*.json
%{_qt6_metatypesdir}/qt6quickcontrols2basic_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2fusion_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2imagine_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2material_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrols2universal_metatypes.json
%{_qt6_metatypesdir}/qt6quickdialogs2_*.json
%{_qt6_metatypesdir}/qt6quickdialogs2utils_metatypes.json
%{_qt6_metatypesdir}/qt6quickeffects_metatypes.json
%{_qt6_metatypesdir}/qt6quicklayouts_metatypes.json
%{_qt6_metatypesdir}/qt6quicktest_metatypes.json
%{_qt6_metatypesdir}/qt6quickshapes_metatypes.json
%{_qt6_metatypesdir}/qt6quicktemplates2_metatypes.json
%{_qt6_metatypesdir}/qt6quickvectorimage_metatypes.json
%{_qt6_metatypesdir}/qt6quickvectorimagehelpers_metatypes.json
%{_qt6_metatypesdir}/qt6quickwidgets_metatypes.json
%{_qt6_mkspecsdir}/modules/qt_lib_labs*.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qml.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlcompiler.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlcore.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickeffects.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlintegration.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmllocalstorage.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlmeta.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlmodels.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlnetwork.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmltest.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlworkerscript.pri
%{_qt6_mkspecsdir}/modules/qt_lib_qmlxmllistmodel.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quick*impl.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quick.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2basic.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2fusion.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2imagine.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2material.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickcontrols2universal.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickdialogs2.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickdialogs2utils.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quicklayouts.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickshapes.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quicktemplates2.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickvectorimage.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickvectorimagehelpers.pri
%{_qt6_mkspecsdir}/modules/qt_lib_quickwidgets.pri
%{_qt6_libdir}/pkgconfig/Qt6Labs*.pc
%{_qt6_libdir}/pkgconfig/Qt6Qml.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlCompiler.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlCore.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickEffects.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlIntegration.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlLocalStorage.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlMeta.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlModels.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlNetwork.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlWorkerScript.pc
%{_qt6_libdir}/pkgconfig/Qt6QmlXmlListModel.pc
%{_qt6_libdir}/pkgconfig/Qt6Quick*Impl.pc
%{_qt6_libdir}/pkgconfig/Qt6Quick.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Basic.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Fusion.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Imagine.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Material.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickControls2Universal.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickDialogs2.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickDialogs2Utils.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickLayouts.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickShapes.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickTemplates2.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickTest.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickVectorImage.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickVectorImageHelpers.pc
%{_qt6_libdir}/pkgconfig/Qt6QuickWidgets.pc
# FIXME:
# This (split to -private-devel) didn't work out because of rhbz#2330219
# Might be something to consider in the future.
# Private stuff
# {_qt6_headerdir}/*/{qt_version}
%dir %{_qt6_libdir}/cmake/Qt6LabsAnimationPrivate
%dir %{_qt6_libdir}/cmake/Qt6LabsFolderListModelPrivate
%dir %{_qt6_libdir}/cmake/Qt6LabsPlatformPrivate
%dir %{_qt6_libdir}/cmake/Qt6LabsQmlModelsPrivate
%dir %{_qt6_libdir}/cmake/Qt6LabsSettingsPrivate
%dir %{_qt6_libdir}/cmake/Qt6LabsSynchronizerPrivate
%dir %{_qt6_libdir}/cmake/Qt6LabsSharedImagePrivate
%dir %{_qt6_libdir}/cmake/Qt6LabsWavefrontMeshPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlCompilerPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlCorePrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlFormatPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlLocalStoragePrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlMetaPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlModelsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlNetworkPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlWorkerScriptPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlXmlListModelPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2BasicPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2BasicStyleImplPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2FluentWinUI3StyleImplPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2FusionPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2FusionStyleImplPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2ImaginePrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2ImplPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2MaterialPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2MaterialStyleImplPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2Private
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2UniversalPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControls2UniversalStyleImplPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2Private
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2QuickImplPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickDialogs2UtilsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickEffectsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickLayoutsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickParticlesPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickShapesPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickShapesDesignHelpersPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickTemplates2Private
%dir %{_qt6_libdir}/cmake/Qt6QuickTestPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickVectorImageGeneratorPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickVectorImageHelpers
%dir %{_qt6_libdir}/cmake/Qt6QuickVectorImagePrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickVectorImageHelpersPrivate/
%dir %{_qt6_libdir}/cmake/Qt6QuickWidgetsPrivate
%{_qt6_libdir}/cmake/Qt6LabsAnimationPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsFolderListModelPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsPlatformPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsQmlModelsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSettingsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSharedImagePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsSynchronizerPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6LabsWavefrontMeshPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlCompilerPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlCorePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlFormatPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlLocalStoragePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlMetaPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlModelsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlNetworkPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlWorkerScriptPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlXmlListModelPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2BasicPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2BasicStyleImplPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2FluentWinUI3StyleImplPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2FusionPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2FusionStyleImplPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2ImaginePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2ImplPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2MaterialPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2MaterialStyleImplPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2Private/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2UniversalPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControls2UniversalStyleImplPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2Private/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2QuickImplPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickDialogs2UtilsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickEffectsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickLayoutsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickParticlesPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickShapesPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickShapesDesignHelpersPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTemplates2Private/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTestPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickVectorImageGeneratorPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickVectorImageHelpersPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickVectorImagePrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickWidgetsPrivate/*.cmake
%{_qt6_descriptionsdir}/QmlFormatPrivate.json
%{_qt6_descriptionsdir}/QuickParticlesPrivate.json
%{_qt6_descriptionsdir}/QuickVectorImageGeneratorPrivate.json
%{_qt6_descriptionsdir}/QuickShapesDesignHelpersPrivate.json
%{_qt6_metatypesdir}/qt6qmlformatprivate_metatypes.json
%{_qt6_metatypesdir}/qt6quickparticlesprivate_metatypes.json
%{_qt6_metatypesdir}/qt6quickshapesdesignhelpersprivate_metatypes.json
%{_qt6_metatypesdir}/qt6quickvectorimagegeneratorprivate_metatypes.json
%{_qt6_mkspecsdir}/modules/qt_lib_*_private.pri

%files static
%dir %{_qt6_archdatadir}/objects-*
%dir %{_qt6_libdir}/cmake/Qt6PacketProtocolPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlDebugPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlDomPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlLSPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlToolingSettingsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QmlTypeRegistrarPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickControlsTestUtilsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QuickTestUtilsPrivate
%{_qt6_libdir}/cmake/Qt6PacketProtocolPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlDebugPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlDomPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlLSPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QmlToolingSettingsPrivate/*cmake
%{_qt6_libdir}/cmake/Qt6QmlTypeRegistrarPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickControlsTestUtilsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QuickTestUtilsPrivate/*.cmake
%{_qt6_headerdir}/QtPacketProtocol/
%{_qt6_headerdir}/QtQmlDebug/
%{_qt6_headerdir}/QtQmlDom/
%{_qt6_headerdir}/QtQmlLS/
%{_qt6_headerdir}/QtQmlToolingSettings/
%{_qt6_headerdir}/QtQmlTypeRegistrar/
%{_qt6_headerdir}/QtQuickControlsTestUtils/
%{_qt6_headerdir}/QtQuickTestUtils/
%{_qt6_libdir}/libQt6PacketProtocol.a
%{_qt6_libdir}/libQt6PacketProtocol.prl
%{_qt6_libdir}/libQt6QmlDebug.a
%{_qt6_libdir}/libQt6QmlDebug.prl
%{_qt6_libdir}/libQt6QmlDom.a
%{_qt6_libdir}/libQt6QmlDom.prl
%{_qt6_libdir}/libQt6QmlFormat.a
%{_qt6_libdir}/libQt6QmlFormat.prl
%{_qt6_libdir}/libQt6QmlLS.a
%{_qt6_libdir}/libQt6QmlLS.prl
%{_qt6_libdir}/libQt6QmlToolingSettings.a
%{_qt6_libdir}/libQt6QmlToolingSettings.prl
%{_qt6_libdir}/libQt6QmlTypeRegistrar.a
%{_qt6_libdir}/libQt6QmlTypeRegistrar.prl
%{_qt6_libdir}/libQt6QuickControlsTestUtils.a
%{_qt6_libdir}/libQt6QuickControlsTestUtils.prl
%{_qt6_libdir}/libQt6QuickTestUtils.a
%{_qt6_libdir}/libQt6QuickTestUtils.prl
%{_qt6_descriptionsdir}/PacketProtocolPrivate.json
%{_qt6_descriptionsdir}/QmlDebugPrivate.json
%{_qt6_descriptionsdir}/QmlDomPrivate.json
%{_qt6_descriptionsdir}/QmlLSPrivate.json
%{_qt6_descriptionsdir}/QmlToolingSettingsPrivate.json
%{_qt6_descriptionsdir}/QmlTypeRegistrarPrivate.json
%{_qt6_descriptionsdir}/QuickControlsTestUtilsPrivate.json
%{_qt6_descriptionsdir}/QuickTestUtilsPrivate.json
%{_qt6_metatypesdir}/qt6packetprotocolprivate_metatypes.json
%{_qt6_metatypesdir}/qt6qmldebugprivate_metatypes.json
%{_qt6_metatypesdir}/qt6qmldomprivate_metatypes.json
%{_qt6_metatypesdir}/qt6qmllsprivate_metatypes.json
%{_qt6_metatypesdir}/qt6qmltoolingsettingsprivate_metatypes.json
%{_qt6_metatypesdir}/qt6qmltyperegistrarprivate_metatypes.json
%{_qt6_metatypesdir}/qt6quickcontrolstestutilsprivate_metatypes.json
%{_qt6_metatypesdir}/qt6quicktestutilsprivate_metatypes.json
# FIXME:
# Same to qtbase, we probably cannot have mkspecs separate from -devel
#{_qt6_mkspecsdir}/modules/qt_lib_packetprotocol_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmldebug_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmldom_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmlls_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmltoolingsettings_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_qmltyperegistrar_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_quickcontrolstestutilsprivate_private.pri
#{_qt6_mkspecsdir}/modules/qt_lib_quicktestutilsprivate_private.pri
%{_qt6_archdatadir}/objects-*/QmlTypeRegistrarPrivate_resources_1/

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

%changelog
* Thu Feb 19 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-2
- QtQml: Do not clear objects propertyCaches on last GC run

* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jan 14 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.1-3
- QtQml: Do not clear objects propertyCaches on last GC run

* Tue Dec 09 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-2
- QtQml: Invalidate fallback lookups after each call from AOT code

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Tue Oct 21 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-2
- Backport - QmlCompiler: Fix write access to optional QVariantMap

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Mon Sep 22 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-3
- This time really drop "Requires: qt6-qtbase-private-devel"

* Mon Sep 22 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-2
- Drop "Requires: qt6-qtbase-private-devel"

* Thu Aug 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-3
- Backport - qmlcachgen: fix crash on unresolved type with required property

* Mon Jun 16 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-2
- Backport - CMake: Do not automatically link against Qt6::QmlPrivate
  Fixes rhbz#2330219

* Mon Jun 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Mon Apr 14 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-2
- Fix qmlcachegen crash in QQmlJSTypeResolver::genericType

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Fri Mar 21 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0~rc-1
- 6.9.0 RC

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.1-6
- Install CMake modules for plugins

* Sat Dec 07 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-5
- Make -devel subpkg to require qtbase-private-devel for cmake >= 3.31.0
  Workaround for rhbz#2330219

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-4
- Revert 'introduce -private-devel subpkg'

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-3
- Move more stuff to -static subpkg and introduce -private-devel subpkg

* Tue Dec 03 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-2
- Drop QmlAssetDownloader

* Thu Nov 28 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
- 6.8.1

* Thu Nov 14 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-3
- Backport upstream fixes for QTBUG-130767

* Mon Nov 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-2
- Backport upstream fix:
  QQuickItem::map{To,From}Item: Account for not having a window yet

* Thu Oct 10 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-2
- Do not own /usr/lib[64]/qml directory

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Mon Jun 10 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-4
- Move all *prl files to -devel subpacakge

* Thu Jun 06 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-3
- Backport upstream fix - dom: avoid asserts during dom construction

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-2
- Rebuild for updated qtbase private api tag

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Wed Apr 03 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-2
- Move libQt6QmlBuiltins.a to -devel subpackage

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-3
- Backport Qt patches for crashes

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Nov 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.1-1
- 6.6.1

* Tue Oct 10 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-4
- Rebuild for qtlanguageserver private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-2
- Rebuild for qtbase private API version change

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Mon Apr 03 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.0-2
- Enable qmlls

* Mon Apr 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Wed Mar 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.4.2-5
- Backport fix for crashes in V4 JIT (#2177696)

* Fri Mar 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-4
- Fix directory ownership

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- 6.4.2

* Wed Nov 23 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.1-1
- 6.4.1

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-1
- 6.3.1

* Wed May 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-2
- Enable examples

* Wed Apr 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-1
- 6.3.0

* Fri Feb 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-2
- Enable s390x builds

* Mon Jan 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-1
- 6.2.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

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

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- Obsoletes: qt6-qtquickcontrols2

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Mon Aug 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-1
- 6.2.0 - beta3

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-1
- 6.0.0
