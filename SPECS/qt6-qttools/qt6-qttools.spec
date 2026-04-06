# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global qt_module qttools

#global unstable 0
%if 0%{?unstable}
%global prerelease rc
%endif

%global examples 1
# disable once Qt7 is stable and providing the apps
%global metainfo 1

Summary: Qt6 - QtTool components
Name:    qt6-qttools
Version: 6.10.2
Release: 1%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

# help lrelease/lupdate use/prefer qmake-qt6
# https://bugzilla.redhat.com/show_bug.cgi?id=1009893
Patch1: qttools-run-qttools-with-qt6-suffix.patch

# 32-bit MIPS needs explicit -latomic
Patch2: qttools-add-libatomic.patch

## upstream patches

Source20: assistant.desktop
Source21: designer.desktop
Source22: linguist.desktop
Source23: qdbusviewer.desktop

# borrowed from Flathub with adjustments for Fedora
Source31: io.qt.Designer.metainfo.xml
Source32: io.qt.Linguist.metainfo.xml
Source33: io.qt.qdbusviewer.metainfo.xml

BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: desktop-file-utils
BuildRequires: /usr/bin/file
BuildRequires: libappstream-glib
BuildRequires: qt6-rpm-macros >= %{version}
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-qtbase-static >= %{version}
BuildRequires: qt6-qtdeclarative-static >= %{version}
BuildRequires: qt6-qtdeclarative >= %{version}
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: clang-devel llvm-devel
BuildRequires: libzstd-devel

Requires: %{name}-common = %{version}-%{release}

%description
%{summary}.

%package common
Summary: Common files for %{name}
BuildArch: noarch

%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-help%{?_isa} = %{version}-%{release}
Requires: qt6-doctools = %{version}-%{release}
Requires: qt6-designer = %{version}-%{release}
Requires: qt6-linguist = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
%description static
%{summary}.

%package libs-designer
Summary: Qt6 Designer runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designer
%{summary}.

%package libs-designercomponents
Summary: Qt6 Designer Components runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-designercomponents
%{summary}.

%package libs-help
Summary: Qt6 Help runtime library
Requires: %{name}-common = %{version}-%{release}
%description libs-help
%{summary}.

%package -n qt6-assistant
Summary: Documentation browser for Qt6
Requires: %{name}-common = %{version}-%{release}
%description -n qt6-assistant
%{summary}.

%package -n qt6-designer
Summary: Design GUIs for Qt6 applications
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
%description -n qt6-designer
%{summary}.

%package -n qt6-linguist
Summary: Qt6 Linguist Tools
Requires: %{name}-common = %{version}-%{release}
%description -n qt6-linguist
Tools to add translations to Qt6 applications.

%package -n qt6-qdbusviewer
Summary: D-Bus debugger and viewer
Requires: %{name}-common = %{version}-%{release}
%{?_qt6:Requires: %{_qt6}%{?_isa} >= %{_qt6_version}}
%description -n qt6-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%package -n qt6-doctools
Summary: Qt6 doc tools package
%description -n qt6-doctools
%{summary}.

%if 0%{?examples}
%package examples
Summary: Programming examples for %{name}
Requires: %{name}-common = %{version}-%{release}
%description examples
%{summary}.
%endif

%prep
%setup -q -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}}

%patch -P1 -p1 -b .run-qttools-with-qt6-suffix
%ifarch %{mips32}
%patch -P2 -p1 -b .libatomic
%endif

%build
%cmake_qt6 \
  -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF} \
  -DQT_INSTALL_EXAMPLES_SOURCES=%{?examples:ON}%{!?examples:OFF}

%cmake_build


%install
%cmake_install

# Add desktop files, --vendor=... helps avoid possible conflicts with qt3/qt4
desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications \
  --vendor="qt6" \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23}

%if 0%{?metainfo}
install -Dm0644 -t %{buildroot}%{_metainfodir} \
  %{SOURCE31} %{SOURCE32} %{SOURCE33}
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
%endif

# icons
install -m644 -p -D src/assistant/assistant/images/assistant.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/assistant-qt6.png
install -m644 -p -D src/assistant/assistant/images/assistant-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/assistant-qt6.png
install -m644 -p -D src/designer/src/designer/images/designer.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/designer-qt6.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/qdbusviewer-qt6.png
install -m644 -p -D src/qdbus/qdbusviewer/images/qdbusviewer-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/qdbusviewer-qt6.png
# linguist icons
for icon in src/linguist/linguist/images/icons/linguist-*-32.png ; do
  size=$(echo $(basename ${icon}) | cut -d- -f2)
  install -p -m644 -D ${icon} %{buildroot}%{_datadir}/icons/hicolor/${size}x${size}/apps/linguist-qt6.png
done

# hardlink files to {_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
   assistant|designer|lconvert|linguist|lrelease|lupdate|pixeltool| \
   qcollectiongenerator|qdbus|qdbusviewer|qhelpconverter|qhelpgenerator| \
   qtplugininfo|qdistancefieldgenerator|qdoc|qtdiag)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ln -sv ${i} ${i}-qt6
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
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


## work-in-progress... -- rex
%check
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


%files
%{_qt6_archdatadir}/sbom/%{qt_module}-%{qt_version}.spdx
%{_bindir}/qdbus-qt6
%{_qt6_bindir}/qdbus
%{_qt6_bindir}/qdbus-qt6
%{_qt6_libdir}/libQt6UiTools.so.6*

%files common
%license LICENSES/LGPL*

%files  libs-designer
%{_qt6_libdir}/libQt6Designer.so.6*
%dir %{_qt6_libdir}/cmake/Qt6Designer/
%{_qt6_plugindir}/designer/*

%files  libs-designercomponents
%{_qt6_libdir}/libQt6DesignerComponents.so.6*

%files  libs-help
%{_qt6_libdir}/libQt6Help.so.6*

%files -n qt6-assistant
%{_bindir}/assistant-qt6
%{_qt6_bindir}/assistant*
%{_datadir}/applications/*assistant.desktop
%{_datadir}/icons/hicolor/*/apps/assistant*.*

%files -n qt6-doctools
%{_bindir}/qdoc*
%{_qt6_bindir}/qdoc*
%{_bindir}/qdistancefieldgenerator*
%{_qt6_bindir}/qdistancefieldgenerator*
%{_qt6_libexecdir}/qhelpgenerator*
%{_qt6_libexecdir}/qtattributionsscanner*

%files -n qt6-designer
%{_bindir}/designer*
%{_qt6_bindir}/designer*
%{_datadir}/applications/*designer.desktop
%{_datadir}/icons/hicolor/*/apps/designer*.*
%if 0%{?metainfo}
%{_metainfodir}/io.qt.Designer.metainfo.xml
%endif

%files -n qt6-linguist
%{_bindir}/linguist*
%{_qt6_bindir}/linguist*
# phrasebooks used by linguist
%{_datadir}/qt6/phrasebooks/*.qph
%{_datadir}/applications/*linguist.desktop
%{_datadir}/icons/hicolor/*/apps/linguist*.*
# linguist friends
%{_bindir}/lconvert*
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_qt6_bindir}/lconvert*
%{_qt6_bindir}/lrelease*
%{_qt6_bindir}/lupdate*
%{_qt6_libexecdir}/lprodump*
%{_qt6_libexecdir}/lrelease*
%{_qt6_libexecdir}/lupdate*
%if 0%{?metainfo}
%{_metainfodir}/io.qt.Linguist.metainfo.xml
%endif

%files -n qt6-qdbusviewer
%{_bindir}/qdbusviewer*
%{_qt6_bindir}/qdbusviewer*
%{_datadir}/applications/*qdbusviewer.desktop
%{_datadir}/icons/hicolor/*/apps/qdbusviewer*.*
%if 0%{?metainfo}
%{_metainfodir}/io.qt.qdbusviewer.metainfo.xml
%endif

%files devel
%{_bindir}/pixeltool*
%{_bindir}/qtdiag*
%{_bindir}/qtplugininfo*
%{_qt6_bindir}/pixeltool*
%{_qt6_bindir}/qtdiag*
%{_qt6_bindir}/qtplugininfo*
%{_qt6_headerdir}/QtQDocCatch/
%{_qt6_headerdir}/QtQDocCatchConversions/
%{_qt6_headerdir}/QtQDocCatchGenerators/
%{_qt6_headerdir}/QtDesigner/
%{_qt6_headerdir}/QtDesignerComponents/
%{_qt6_headerdir}/QtHelp/
%{_qt6_headerdir}/QtUiPlugin
%{_qt6_headerdir}/QtUiTools/
%{_qt6_headerdir}/QtTools/
%{_qt6_libdir}/libQt6Designer*.so
%{_qt6_libdir}/libQt6Help.so
%{_qt6_libdir}/libQt6UiTools.so
%dir %{_qt6_libdir}/cmake/Qt6Designer
%dir %{_qt6_libdir}/cmake/Qt6DesignerComponentsPrivate
%dir %{_qt6_libdir}/cmake/Qt6DesignerPrivate
%dir %{_qt6_libdir}/cmake/Qt6Help/
%dir %{_qt6_libdir}/cmake/Qt6HelpPrivate
%dir %{_qt6_libdir}/cmake/Qt6Linguist
%dir %{_qt6_libdir}/cmake/Qt6LinguistTools
%dir %{_qt6_libdir}/cmake/Qt6LinguistTools
%dir %{_qt6_libdir}/cmake/Qt6QDocCatchConversionsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QDocCatchGeneratorsPrivate
%dir %{_qt6_libdir}/cmake/Qt6QDocCatchPrivate
%dir %{_qt6_libdir}/cmake/Qt6Tools/
%dir %{_qt6_libdir}/cmake/Qt6ToolsTools/
%dir %{_qt6_libdir}/cmake/Qt6UiPlugin/
%dir %{_qt6_libdir}/cmake/Qt6UiToolsPrivate
%{_qt6_libdir}/cmake/Qt6/FindWrapLibClang.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtToolsTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6Designer/*.cmake
%{_qt6_libdir}/cmake/Qt6DesignerComponentsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6DesignerPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Help/*.cmake
%{_qt6_libdir}/cmake/Qt6HelpPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Linguist/*.cmake
%{_qt6_libdir}/cmake/Qt6LinguistTools/*.cmake
%{_qt6_libdir}/cmake/Qt6QDocCatchConversionsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QDocCatchGeneratorsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6QDocCatchPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Tools/*.cmake
%{_qt6_libdir}/cmake/Qt6ToolsTools/*.cmake
%{_qt6_libdir}/cmake/Qt6UiPlugin/*.cmake
%{_qt6_libdir}/cmake/Qt6UiTools/
%{_qt6_libdir}/cmake/Qt6UiToolsPrivate/*.cmake
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_qdoccatch_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_qdoccatchconversions_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_qdoccatchgenerators_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_designer.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_designer_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_designercomponents_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_help.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_help_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_linguist.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_tools_private.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_uiplugin.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_uitools.pri
%{_qt6_archdatadir}/mkspecs/modules/qt_lib_uitools_private.pri
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_libdir}/pkgconfig/*.pc

%files static
%{_qt6_libdir}/libQt6Designer*.prl
%{_qt6_libdir}/libQt6Help.prl
%{_qt6_libdir}/libQt6UiTools.prl

%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif


%changelog
* Mon Feb 09 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-1
- 6.10.2

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Nov 20 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.1-1
- 6.10.1

* Tue Oct 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Thu Sep 25 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0~rc-1
- 6.10.0 RC

* Thu Aug 28 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.2-1
- 6.9.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Wed Apr 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Mon Mar 24 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0~rc-1
- 6.9.0 RC

* Sun Mar 09 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 6.8.2-2
- Rebuilt for LLVM 20

* Fri Jan 31 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.2-1
- 6.8.2

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.1-3
- Fix directory ownership

* Thu Dec 05 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-2
- Move Software Bill of Materials from -devel

* Thu Nov 28 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.1-1
- 6.8.1

* Fri Oct 11 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Tue Oct 01 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 6.7.2-4
- Rebuilt for LLVM 19

* Mon Jul 22 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 6.7.2-3
- Add appstream data for apps

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 01 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.2-1
- 6.7.2

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-1
- 6.7.1

* Tue Apr 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- 6.7.0

* Sat Mar 2 2024 Marie Loise Nolden <loise@kde.org> - 6.6.2-3
- minor cleanups

* Mon Feb 19 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-2
- Examples: also install source files

* Thu Feb 15 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.2-1
- 6.6.2

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

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-2
- Rebuild for qtbase private API version change

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Tue Apr 04 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

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

* Mon Sep 19 2022 Pete Walter <pwalter@fedoraproject.org> - 6.3.1-3
- Rebuild for llvm 15

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-1
- 6.3.1

* Wed May 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-3
- Fix path to lprodump

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

* Thu Oct 07 2021 Tom Stellard <tstellar@redhat.com> - 6.2.0-3
- Rebuild for llvm-13.0.0

* Thu Sep 30 2021 Kalev Lember <klember@redhat.com> - 6.2.0-2
- Rebuild for clang 13.0.0~rc1

* Thu Sep 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-1
- 6.2.0

* Mon Sep 27 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc2-1
- 6.2.0 - rc2

* Sat Sep 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1

* Mon May 24 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-2
- Rebuild with correct libexecdir path

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-2
- Rebuild (clang)

* Wed Jan 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0
- 6.0.0
