# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global qt_module qttools

# Disable automatic .la file removal
%global __brp_remove_la_files %nil

#global bootstrap 1

%if ! 0%{?bootstrap}
## don't enable until crasher fixed: https://bugzilla.redhat.com/show_bug.cgi?id=1470778
#global webkit 1
%endif

Summary: Qt5 - QtTool components
Name:    qt5-qttools
Version: 5.15.18
Release: 2%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-opensource-src-%{version}.tar.xz

## upstream patches
## repo: https://invent.kde.org/qt/qt/qttools
## branch: kde/5.15
## git format-patch v5.15.16-lts-lgpl
Patch1: 0001-Ensure-FileAttributeSetTable-is-filled-ordered-so-we.patch
Patch2: 0002-Drop-superfluous-network-dependency-from-assistant-h.patch
Patch3: 0003-qdoc-Ensure-the-generated-temporary-header-file-is-c.patch

# help lrelease/lupdate use/prefer qmake-qt5
# https://bugzilla.redhat.com/show_bug.cgi?id=1009893
Patch102: qttools-opensource-src-5.13.2-runqttools-with-qt5-suffix.patch

# 32-bit MIPS needs explicit -latomic
Patch104: qttools-opensource-src-5.7-add-libatomic.patch
# Link against libclang-cpp.so
# https://fedoraproject.org/wiki/Changes/Stop-Shipping-Individual-Component-Libraries-In-clang-lib-Package
Patch105: Link-against-libclang-cpp.so-instead-of-the-clang-co.patch

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qdbusviewer.desktop

BuildRequires: make
# %%check needs cmake (and don't want to mess with cmake28)
%if 0%{?fedora} || 0%{?rhel} > 6
BuildRequires: cmake
%endif
BuildRequires: desktop-file-utils
BuildRequires: /usr/bin/file
BuildRequires: qt5-rpm-macros >= %{version}

BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-qtbase-static >= %{version}
BuildRequires: qt5-qtdeclarative-static >= %{version}
BuildRequires: pkgconfig(Qt5Qml)
# libQt5DBus.so.5(Qt_5_PRIVATE_API)
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}

%if 0%{?bootstrap}
%global no_examples CONFIG-=compile_examples
Obsoletes: %{name}-examples < %{version}-%{release}
%else
# for qdoc
BuildRequires: clang-devel llvm-devel
%endif

Requires: %{name}-common = %{version}-%{release}

%description
%{summary}.

%package common
Summary: Common files for %{name}
BuildArch: noarch
Obsoletes: qt5-qttools-libs-clucene < 5.9.0
%if ! 0%{?webkit}
Obsoletes: qt5-designer-plugin-webkit < 5.9.0
%endif
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-help%{?_isa} = %{version}-%{release}
Requires: qt5-doctools = %{version}-%{release}
Requires: qt5-designer = %{version}-%{release}
Requires: qt5-linguist = %{version}-%{release}
Requires: qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%package libs-designer
Summary: Qt5 Designer runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designer
%{summary}.

%package libs-designercomponents
Summary: Qt5 Designer Components runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designercomponents
%{summary}.

%package libs-help
Summary: Qt5 Help runtime library
Requires: %{name}-common = %{version}-%{release}
# when split happened
Conflicts: qt5-tools < 5.4.0-0.2
%description libs-help
%{summary}.

%package -n qt5-assistant
Summary: Documentation browser for Qt5
Requires: %{name}-common = %{version}-%{release}
%description -n qt5-assistant
%{summary}.

%package -n qt5-designer
Summary: Design GUIs for Qt5 applications
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
%description -n qt5-designer
%{summary}.

%if 0%{?webkit}
%package -n qt5-designer-plugin-webkit
Summary: Qt5 designer plugin for WebKit
BuildRequires: pkgconfig(Qt5WebKitWidgets)
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
%description -n qt5-designer-plugin-webkit
%{summary}.
%endif

%package -n qt5-linguist
Summary: Qt5 Linguist Tools
Requires: %{name}-common = %{version}-%{release}
%description -n qt5-linguist
Tools to add translations to Qt5 applications.

%package -n qt5-qdbusviewer
Summary: D-Bus debugger and viewer
Requires: %{name}-common = %{version}-%{release}
%{?_qt5:Requires: %{_qt5}%{?_isa} >= %{_qt5_version}}
%description -n qt5-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%package -n qt5-doctools
Summary: Qt5 doc tools package
Provides: qt5-qdoc = %{version}
Obsoletes: qt5-qdoc < 5.8.0
Provides: qt5-qhelpgenerator = %{version}
Obsoletes: qt5-qhelpgenerator < 5.8.0
Provides: qt5-qtattributionsscanner = %{version}
Obsoletes: qt5-qtattributionsscanner < 5.8.0
Requires: qt5-qtattributionsscanner = %{version}

%description -n qt5-doctools
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}-common = %{version}-%{release}
%description examples
%{summary}.


%prep
%setup -q -n %{qt_module}-everywhere-src-%{version}
%autopatch -M 99 -p1
%patch -P102 -p1 -b ..runqttools-with-qt5-suffix.patch

%ifarch %{mips32}
%patch -P104 -p1 -b .libatomic
%endif
%patch -P105 -p1 -b .libclang-cpp


%build
%{qmake_qt5} \
  CONFIG+=disable_external_rpath \
  %{?no_examples}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

# Add desktop files, --vendor=... helps avoid possible conflicts with qt3/qt4
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt5" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}

# icons
install -m644 -p -D src/assistant/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant-qt5.png
install -m644 -p -D src/assistant/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant-qt5.png
install -m644 -p -D src/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/designer-qt5.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer-qt5.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer-qt5.png
# linguist icons
for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist-qt5.png
done

# hardlink files to {_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
   assistant|designer|lconvert|linguist|lrelease|lupdate|lprodump|pixeltool|qcollectiongenerator|qdbus|qdbusviewer|qhelpconverter|qhelpgenerator|qtplugininfo|qtattributionsscanner)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt5
      ln -sv ${i} ${i}-qt5
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

## Qt5Designer.pc references non-existent Qt5UiPlugin.pc, remove the reference for now
sed -i -e 's| Qt5UiPlugin||g' %{buildroot}%{_qt5_libdir}/pkgconfig/Qt5Designer.pc


## work-in-progress... -- rex
%if 0%{?fedora} || 0%{?rhel} > 6
%check
# verify validity of Qt5Designer.pc
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig:$PKG_CONFIG_PATH
pkg-config --print-requires --print-requires-private Qt5Designer
export CMAKE_PREFIX_PATH=%{buildroot}%{_qt5_prefix}:%{buildroot}%{_prefix}
export PATH=%{buildroot}%{_qt5_bindir}:%{_qt5_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt5_libdir}
mkdir tests/auto/cmake/%{_target_platform}
pushd tests/auto/cmake/%{_target_platform}
cmake ..
ctest --output-on-failure ||:
popd


# check icon resolutions
pushd %{buildroot}%{_datadir}/icons
for RES in $(ls hicolor); do
  for APP in designer assistant linguist qdbusviewer; do
    if [ -e hicolor/$RES/apps/${APP}*.* ]; then
      file hicolor/$RES/apps/${APP}*.* | grep "$(echo $RES | sed 's/x/ x /')"
    fi
  done
done
popd

%endif


%files
%{_bindir}/qdbus-qt5
%{_bindir}/qtpaths
%{_qt5_bindir}/qdbus
%{_qt5_bindir}/qdbus-qt5
%{_qt5_bindir}/qtpaths

%files common
%license LICENSE.LGPL*

%ldconfig_scriptlets libs-designer

%files  libs-designer
%{_qt5_libdir}/libQt5Designer.so.5*
%dir %{_qt5_libdir}/cmake/Qt5Designer/

%ldconfig_scriptlets libs-designercomponents

%files  libs-designercomponents
%{_qt5_libdir}/libQt5DesignerComponents.so.5*

%ldconfig_scriptlets libs-help

%files  libs-help
%{_qt5_libdir}/libQt5Help.so.5*

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -n qt5-assistant
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-assistant
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5-assistant
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi
%endif

%files -n qt5-assistant
%{_bindir}/assistant-qt5
%{_qt5_bindir}/assistant*
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*.*

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -n qt5-doctools
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-doctools
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5-doctools
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi
%endif

%files -n qt5-doctools
%{_bindir}/qdoc*
%{_qt5_bindir}/qdoc*
%{_bindir}/qdistancefieldgenerator*
%{_bindir}/qhelpgenerator*
%{_qt5_bindir}/qdistancefieldgenerator*
%{_qt5_bindir}/qhelpgenerator*
%{_bindir}/qtattributionsscanner-qt5
%{_qt5_bindir}/qtattributionsscanner*

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -n qt5-designer
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-designer
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun -n qt5-designer
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi
%endif

%files -n qt5-designer
%{_bindir}/designer*
%{_qt5_bindir}/designer*
%{_datadir}/applications/*designer.desktop
%{_datadir}/icons/hicolor/*/apps/designer*.*
%dir %{_qt5_libdir}/cmake/Qt5DesignerComponents
%{_qt5_libdir}/cmake/Qt5DesignerComponents/Qt5DesignerComponentsConfig*.cmake

%if 0%{?webkit}
%files -n qt5-designer-plugin-webkit
%{_qt5_plugindir}/designer/libqwebview.so
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_QWebViewPlugin.cmake
%endif

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -n qt5-linguist
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-linguist
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun -n qt5-linguist
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi
%endif

%files -n qt5-linguist
%{_bindir}/linguist*
%{_qt5_bindir}/linguist*
# phrasebooks used by linguist
%{_qt5_datadir}/phrasebooks/
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/linguist*.*
# linguist friends
%{_bindir}/lconvert*
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_bindir}/lprodump*
%{_qt5_bindir}/lconvert*
%{_qt5_bindir}/lrelease*
%{_qt5_bindir}/lupdate*
%{_qt5_bindir}/lprodump*
# cmake config
%dir %{_qt5_libdir}/cmake/Qt5LinguistTools/
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsConfig*.cmake
%{_qt5_libdir}/cmake/Qt5LinguistTools/Qt5LinguistToolsMacros.cmake

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -n qt5-qdbusviewer
touch --no-create %{_datadir}/icons/hicolor ||:

%posttrans -n qt5-qdbusviewer
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:

%postun -n qt5-qdbusviewer
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
fi
%endif

%files -n qt5-qdbusviewer
%{_bindir}/qdbusviewer*
%{_qt5_bindir}/qdbusviewer*
%{_datadir}/applications/*qdbusviewer.desktop
%{_datadir}/icons/hicolor/*/apps/qdbusviewer*.*

%files devel
%{_bindir}/pixeltool*
%{_bindir}/qcollectiongenerator*
#{_bindir}/qhelpconverter*
%{_bindir}/qtdiag*
%{_bindir}/qtplugininfo*
%{_qt5_bindir}/pixeltool*
%{_qt5_bindir}/qtdiag*
%{_qt5_bindir}/qcollectiongenerator*
#{_qt5_bindir}/qhelpconverter*
%{_qt5_bindir}/qtplugininfo*
%{_qt5_headerdir}/QtDesigner/
%{_qt5_headerdir}/QtDesignerComponents/
%{_qt5_headerdir}/QtHelp/
%{_qt5_headerdir}/QtUiPlugin
%{_qt5_libdir}/libQt5Designer*.prl
%{_qt5_libdir}/libQt5Designer*.so
%{_qt5_libdir}/libQt5Help.prl
%{_qt5_libdir}/libQt5Help.so
%{_qt5_libdir}/Qt5UiPlugin.la
%{_qt5_libdir}/libQt5UiPlugin.prl
%{_qt5_libdir}/cmake/Qt5Designer/Qt5DesignerConfig*.cmake
%dir %{_qt5_libdir}/cmake/Qt5Help/
%{_qt5_libdir}/cmake/Qt5Help/Qt5HelpConfig*.cmake
%{_qt5_libdir}/cmake/Qt5UiPlugin/
%{_qt5_libdir}/pkgconfig/Qt5Designer.pc
%{_qt5_libdir}/pkgconfig/Qt5Help.pc
%{_qt5_libdir}/pkgconfig/Qt5UiPlugin.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_designer.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_designer_private.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_designercomponents_private.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_help.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_help_private.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_uiplugin.pri
# putting these here for now, new stuff in 5.14, review for accuracy -- rdieter
%{_qt5_libdir}/cmake/Qt5AttributionsScannerTools/
%{_qt5_libdir}/cmake/Qt5DocTools/

%files static
%{_qt5_headerdir}/QtUiTools/
%{_qt5_libdir}/libQt5UiTools.*a
%{_qt5_libdir}/libQt5UiTools.prl
%{_qt5_libdir}/cmake/Qt5UiTools/
%{_qt5_libdir}/pkgconfig/Qt5UiTools.pc
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_uitools.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_uitools_private.pri

%if ! 0%{?no_examples:1}
%files examples
%{_qt5_examplesdir}/
%{_qt5_plugindir}/designer/*
%dir %{_qt5_libdir}/cmake/Qt5Designer
%{_qt5_libdir}/cmake/Qt5Designer/Qt5Designer_*
%endif


%changelog
* Tue Nov 04 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.18-1
- 5.15.18

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 26 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.17-1
- 5.15.17

* Fri May 02 2025 Than Ngo <than@redhat.com> - 5.15.16-4
- Fix rhbz#2293758, Directory is missing in RPM database

* Sun Mar 16 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 5.15.16-3
- Rebuilt for LLVM 20

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Zephyr Lykos <fedora@mochaa.ws> - 5.15.16-1
- 5.15.16

* Sun Oct 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 5.15.15-2
- Rebuilt for LLVM/Clang 19

* Wed Sep 04 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.15-1
- 5.15.15

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 29 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.14-1
- 5.15.14

* Thu Mar 14 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.13-1
- 5.15.13

* Thu Feb 29 2024 David Abdurachmanov <davidlt@rivosinc.com> - 5.15.12-4
- Set disable_external_rpath to avoid RPATHs in qdoc

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.12-1
- 5.15.12

* Fri Oct 06 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.11-1
- 5.15.11

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 25 2023 Kalev Lember <klember@redhat.com> - 5.15.10-2
- Fix self tests when building for flatpak

* Mon Jun 12 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.10-1
- 5.15.10

* Tue Apr 11 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.9-1
- 5.15.9

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.8-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.8-1
- 5.15.8

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.7-1
- 5.15.7

* Tue Sep 20 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-1
- 5.15.6

* Mon Sep 19 2022 Pete Walter <pwalter@fedoraproject.org> - 5.15.5-3
- Rebuild for clang 15

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.5-1
- 5.15.5

* Mon May 16 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.4-1
- 5.15.4

* Fri Mar 04 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.3-1
- 5.15.3

* Mon Jan 24 2022 Timm Bäeder <tbaeder@redhat.com> - 5.15.2-10
- Disable automatic .la file removal
- https://fedoraproject.org/wiki/Changes/RemoveLaFiles

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Oct 07 2021 Tom Stellard <tstellar@redhat.com> - 5.15.2-8
- Rebuild for llvm-13.0.0

* Thu Sep 30 2021 Kalev Lember <klember@redhat.com> - 5.15.2-7
- Rebuild for clang 13.0.0~rc1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Tom Stellard <tstellar@redhat.com> - 5.15.2-4
- Rebuild for clang-11.1.0

* Thu Dec 10 14:18:27 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-3
- Bump for eln build

* Tue Nov 24 07:54:16 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-2
- Rebuild for qtbase with -no-reduce-relocations option

* Fri Nov 20 09:30:47 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.2-1
- 5.15.2

* Tue Oct 27 2020 Leigh Scott <leigh123linux@gmail.com> - 5.15.1-3
- Bump to fix hash issue on rpmfusion koji

* Mon Oct 19 2020 Kalev Lember <klember@redhat.com> - 5.15.1-2
- Disable lto to work around lconvert segfaulting on armv7hl (#1884681)

* Thu Sep 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.1-1
- 5.15.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Tom Stellard <tstellar@redhat.com> - 5.13.2-4
- Link against libclang-cpp.so
- https://fedoraproject.org/wiki/Changes/Stop-Shipping-Individual-Component-Libraries-In-clang-lib-Package

* Wed Dec 18 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-3
- Use -qt5 suffix for linguist tools

* Wed Dec 18 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-2
- Move lprodump to qt5-linguist

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-1
- 5.13.2

* Thu Sep 26 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-2
- rebuild (clang)

* Tue Sep 24 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.5-1
- 5.12.5

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.4-1
- 5.12.4

* Tue Jun 04 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.3-1
- 5.12.3

* Fri Feb 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1
- better bootstrap support (examples)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.2-1
- 5.11.2

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Sat May 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-1
- 5.11.0
- use %%make_build

* Thu Mar 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-2
- BR: qt5-rpm-macros

* Tue Feb 13 2018 Jan Grulich <jgrulich@redhat.com> - 5.10.1-1
- 5.10.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.10.0-2
- Remove obsolete scriptlets

* Tue Dec 19 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Thu Nov 23 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Fri Oct 27 2017 Miro Hrončok <mhroncok@redhat.com> - 5.9.2-3
- Qt 5 Designer has 128x128 icon in 32x32 folder (#1400972)

* Tue Oct 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-2
- BR: qt5-qtbase-private-devel

* Mon Oct 09 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.2-1
- 5.9.2

* Fri Sep 29 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-4
- Obsoletes: qt5-designer-plugin-webkit (upgrade path when webkit support is not enabled)
- resurrect bootstrap macro (commented)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Fri Jun 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-3
- drop shadow/out-of-tree builds (#1456211,QTBUG-37417)

* Fri Jun 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-2
- rebuild

* Wed May 31 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-1
- Upstream official release

* Fri May 26 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.1.rc
- Upstream Release Candidate retagged

* Tue May 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-0.4.beta3
- fix Release, Obsoletes: qt5-qttools-libs-clucene (#1454531)

* Tue May 09 2017 Helio Chissini de Castro <helio@kde.org> - 5.9.0-0.beta.3
- Upstream beta 3

* Fri Mar 31 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-6
- -devel: restore Requires: qt5-designer qt5-linguist

* Thu Mar 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-5
- de-bootstrap

* Mon Mar 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-4
- bootstrap 5.8.0 (rawhide)
- Created a meta package called qt5-doctools to avoid the mess of multiple tools

* Tue Mar 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-6
- -assistant: Provides: bundled(clucene09) (f26+)

* Fri Feb 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-5
- disable system_lucene on f26+ (#1424227, #1424046)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-4
- 5.7.1 dec5 snapshot

* Fri Dec 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-3
- Qt 5 Designer has 128x128 icon in 32x32 folder (#1400972)

* Thu Dec 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- de-bootstrap, enable -doc/-webkit

* Wed Nov 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.1-1
- New upstream version

* Mon Nov 21 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-4
- -static: move qt_lib_uitools*.pri here (#1396836)

* Fri Aug 12 2016 Michal Toman <mtoman@fedoraproject.org> - 5.7.0-3
- Add explicit -latomic on 32-bit MIPS

* Mon Jul 04 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-2
- Compiled with gcc

* Tue Jun 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-1
- Qt 5.7.0 release

* Mon Jun 13 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.0-0.1
- Prepare 5.7.0

* Sun Mar 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-3
- rebuild

* Fri Mar 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-2
- rebuild

* Wed Mar 16 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-2
- 5.6.0 final release

* Mon Mar 14 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-1
- 5.6.0 final release

* Tue Feb 23 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.12.rc
- Update to final RC

* Fri Feb 19 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.11.rc
- workaround Qt5Designer.pc reference to non-existent Qt5UiPlugin.pc

* Mon Feb 15 2016 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.10
- Update RC release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-0.9.rc
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 17 2016 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.8.rc
- port QTBUG-43057 workaround

* Mon Dec 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.7.rc
- update source URL, use %%license

* Mon Dec 21 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.6
- Update to final rc release

* Fri Dec 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.6.0-0.5
- (re)fix bootstrap macro
- include qt5-qdoc/qt5-qhelpgenerator build dep deps in -doc subpkg only
- fix whitespace

* Thu Dec 10 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.4
- Official rc release

* Tue Dec 08 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-3
- Reenable examples. Some interfaces marked as examples are needed from phonon
- Update to second rc snapshot

* Sun Dec 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.6.0-0.2
- de-bootstrap

* Tue Nov 03 2015 Helio Chissini de Castro <helio@kde.org> - 5.6.0-0.1
- Start to implement 5.6.0 rc, bootstrapped

* Thu Oct 15 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-2
- Update to final release 5.5.1

* Tue Sep 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.1-1
- Update to Qt 5.5.1 RC1

* Sat Aug 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-4
- qt5-linguist: move lconvert,lrelease,lupdate, cmake Qt5LinguistTools  here

* Wed Jul 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- de-bootstrap

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- qt5-designer, qt5-linguist, qt5-qhelpgenerator subpkgs

* Wed Jul 1 2015 Helio Chissini de Castro <helio@kde.org> 5.5.0-1
- New final upstream release Qt 5.5.0

* Mon Jun 29 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.4.rc
- Second round of builds now with bootstrap enabled due new qttools

* Sat Jun 27 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.3.rc
- Disable bootstrap

* Thu Jun 25 2015 Helio Chissini de Castro <helio@kde.org> - 5.5.0-0.2.rc
- Update for official RC1 released packages

* Mon Jun 15 2015 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-0.1.rc
- Qt 5.5.0 RC1

* Wed Jun 03 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-1
- 5.4.2

* Sat May 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-3
- rebuild (gcc5)

* Fri Feb 27 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-2
- rebuild (gcc5)

* Tue Feb 24 2015 Jan Grulich <jgrulich@redhat.com> 5.4.1-1
- 5.4.1

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.0-2
- rebuild (gcc5)

* Wed Dec 10 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-1
- 5.4.0 (final)

* Tue Dec 09 2014 Daniel Vrátil <dvratil@redhat.com> 5.4.0-0.10.rc
- fix icon name in qdbusviewer-qt5.desktop

* Sun Nov 30 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.9.rc
- install Linguist icon as linguist-qt5.png, fixes file conflict (#1169127)

* Fri Nov 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.8.rc
- 5.4.0-rc

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.7.rc
- out-of-tree build, use %%qmake_qt5

* Fri Oct 31 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.6.rc
- respin system-clucene.patch

* Sun Oct 26 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.5.rc
- system-clucene patch: create path recursively in QtCLucene, CLucene can't

* Sun Oct 26 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.4.rc
- disable bootstrap (reenable -doc)
- system-clucene patch: drop -fpermissive flag
- system-clucene patch: use toLocal8Bit instead of toStdString
- system_clucene: BR clucene09-core-devel >= 0.9.21b-12 (-11 was broken)

* Sat Oct 25 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.4.0-0.3.rc
- libQt5Designer should be in a subpackage (#1156685)
- -doc: disable(boostrap for new clucene), drop dep on main pkg

* Sat Oct 25 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.4.0-0.2.rc
- BR and rebuild against reference-counting-enabled clucene09 (#1128293)

* Sat Oct 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-0.1.rc
- 5.4.0-rc

* Fri Oct 17 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-2
- -devel: Requires: qt5-designer-plugin-webkit

* Tue Sep 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Jan Grulich <jgrulich@redhat.com> - 5.3.1-1
- 5.3.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.3.0-2
- restore system-clucene patch, rm the bundled copy

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-3
- -examples subpkg

* Tue Jan 14 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- epel7 bootstrapped

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.rc1
- enable -doc only on primary archs (allow secondary bootstrap)

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.rc1
- rebuild (arm/qreal)

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.rc1
- 5.2.0-rc1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.2.alpha
- bootstrap ppc

* Tue Oct 01 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.1.alpha
- 5.2.0-alpha
- -doc subpkg

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-6
- lupdate can't find qmake configuration file default (#1009893)

* Sat Sep 21 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-4
- use upstream cmake fix(es) (QTBUG-32570, #1006254)

* Wed Sep 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-3
- wrong path to lrelease (#1006254)
- %%check: first try

* Tue Sep 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- ExclusiveArch: {ix86} x86_64 {arm}
- epel-6 love

* Wed Aug 28 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- qttools-5.1.1
- qt5-assistant, qt5-qdbusviewer, qt5-designer-plugin-webkit subpkgs (to match qt4)

* Mon Aug 19 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- use system clucene09-core

* Mon Apr 29 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-3
- drop deprecated Encoding= key from .desktop files
- add justification for desktop vendor usage

* Fri Apr 19 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- add .desktop/icons for assistant, designer, linguist, qdbusviewer

* Thu Apr 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-1
- 5.0.2

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- BR: pkgconfig(zlib)
- -static subpkg

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- first try

