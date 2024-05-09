Summary:      Qt6 - QtTool components
Name:         qttools
Version:      6.6.1
Release:      1%{?dist}
Vendor:       Microsoft Corporation
Distribution:   Azure Linux

License: LGPLv3 or LGPLv2
Url:     https://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: https://download.qt.io/archive/qt/%{majmin}/%{version}/submodules/qttools-everywhere-src-%{version}.tar.xz

BuildRequires: coreutils

BuildRequires: qtbase-private-devel
# Qt macros
BuildRequires: qt-rpm-macros >= %{version}
BuildRequires: qtbase-static >= %{version}
BuildRequires: qtdeclarative-static >= %{version}
BuildRequires: cmake
BuildRequires: ninja-build

Requires: %{name}-common = %{version}-%{release}

%global examples 1

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
Requires: qt-doctools = %{version}-%{release}
Requires: qt-designer = %{version}-%{release}
Requires: qt-linguist = %{version}-%{release}
Requires: qtbase-devel%{?_isa}
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

%package -n qt-assistant
Summary: Documentation browser for Qt6
Requires: %{name}-common = %{version}-%{release}
%description -n qt-assistant
%{summary}.

%package -n qt-designer
Summary: Design GUIs for Qt6 applications
Requires: %{name}-libs-designer%{?_isa} = %{version}-%{release}
Requires: %{name}-libs-designercomponents%{?_isa} = %{version}-%{release}
%description -n qt-designer
%{summary}.

%package -n qt-linguist
Summary: Qt6 Linguist Tools
Requires: %{name}-common = %{version}-%{release}
%description -n qt-linguist
Tools to add translations to Qt6 applications.

%package -n qt-qdbusviewer
Summary: D-Bus debugger and viewer
Requires: %{name}-common = %{version}-%{release}
%{?_qt:Requires: %{_qt}%{?_isa} >= %{_qt_version}}
%description -n qt-qdbusviewer
QDbusviewer can be used to inspect D-Bus objects of running programs
and invoke methods on those objects.

%package -n qt-doctools
Summary: Qt6 doc tools package
Provides: qt-qdoc = %{version}
BuildRequires: clang-devel
BuildRequires: llvm-devel
Provides: qt-qhelpgenerator = %{version}

%description -n qt-doctools
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}-common = %{version}-%{release}
%description examples
%{summary}.

%prep
%setup -q -n qttools-everywhere-src-%{version}

%build
%cmake_qt -DQT_BUILD_EXAMPLES:BOOL=%{?examples:ON}%{!?examples:OFF}
%ninja_build

%install
%ninja_install

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
pushd %{buildroot}%{_qt_bindir}
for i in * ; do
  case "${i}" in
   assistant|designer|lconvert|linguist|lrelease|lupdate|pixeltool|qcollectiongenerator|qdbus|qdbusviewer|qhelpconverter|qhelpgenerator|qtplugininfo|qtattributionsscanner)
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
pushd %{buildroot}%{_qt_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

## Qt6Designer.pc references non-existent Qt6UiPlugin.pc, remove the reference for now
sed -i -e 's| Qt6UiPlugin||g' %{buildroot}%{_qt_libdir}/pkgconfig/Qt6Designer.pc


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
%{_bindir}/qdbus-qt6
%{_qt_bindir}/qdbus
%{_qt_libdir}/libQt6UiTools.so.6*

%files common
%license LICENSES/LGPL*
 
%ldconfig_scriptlets libs-designer

%files  libs-designer
%{_qt_libdir}/libQt6Designer.so.6*
%{_qt_plugindir}/designer/*
%dir %{_qt_libdir}/cmake/Qt6Designer/
 
%ldconfig_scriptlets libs-designercomponents

%files  libs-designercomponents
%{_qt_libdir}/libQt6DesignerComponents.so.6*
 
%ldconfig_scriptlets libs-help

%files  libs-help
%{_qt_libdir}/libQt6Help.so.6*

%files -n qt-designer
%{_bindir}/designer*
%{_datadir}/icons/hicolor/*/apps/designer*.*
%{_qt_bindir}/designer*

%files -n qt-linguist
%{_bindir}/linguist*
%{_qt_bindir}/linguist*
# phrasebooks used by linguist
%{_datadir}/icons/hicolor/*/apps/linguist*.*
%{_datadir}/qt6/phrasebooks/*.qph
# linguist friends
%{_bindir}/lconvert*
%{_bindir}/lrelease*
%{_bindir}/lupdate*
%{_qt_bindir}/lconvert*
%{_qt_bindir}/lrelease*
%{_qt_bindir}/lupdate*
%{_qt_libexecdir}/lprodump*
%{_qt_libexecdir}/lrelease*
%{_qt_libexecdir}/lupdate*

%files -n qt-qdbusviewer
%{_bindir}/qdbusviewer*
%{_qt_bindir}/qdbusviewer*
%{_datadir}/icons/hicolor/*/apps/qdbusviewer*.*

%files devel
%{_prefix}/modules/Designer.json
%{_prefix}/modules/DesignerComponentsPrivate.json
%{_prefix}/modules/Help.json
%{_prefix}/modules/Linguist.json
%{_prefix}/modules/QDocCatchConversionsPrivate.json
%{_prefix}/modules/QDocCatchGeneratorsPrivate.json
%{_prefix}/modules/QDocCatchPrivate.json
%{_prefix}/modules/Tools.json
%{_prefix}/modules/UiPlugin.json
%{_prefix}/modules/UiTools.json
%{_datadir}/icons/hicolor/128x128/apps/assistant-qt6.png
%{_datadir}/icons/hicolor/32x32/apps/assistant-qt6.png
%{_bindir}/assistant-qt6
%{_bindir}/pixeltool*
%{_bindir}/qtdiag*
%{_bindir}/qtplugininfo*
%{_qt_archdatadir}/mkspecs/modules/qt_lib_designer_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_designer.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_designercomponents_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_help_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_help.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_linguist_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_linguist.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_qdoccatch_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_qdoccatchconversionsprivate_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_qdoccatchconversionsprivate.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_qdoccatchgeneratorsprivate_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_qdoccatchgeneratorsprivate.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_tools_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_uiplugin.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_uitools_private.pri
%{_qt_archdatadir}/mkspecs/modules/qt_lib_uitools.pri
%{_qt_bindir}/assistant
%{_qt_bindir}/assistant-qt6
%{_qt_bindir}/pixeltool*
%{_qt_bindir}/qdbus-qt6
%{_qt_bindir}/qtdiag*
%{_qt_bindir}/qtplugininfo*
%{_qt_examplesdir}/assistant/remotecontrol/remotecontrol
%{_qt_examplesdir}/assistant/simpletextviewer/simpletextviewer
%{_qt_examplesdir}/designer/calculatorbuilder/calculatorbuilder
%{_qt_examplesdir}/designer/calculatorform_mi/calculatorform_mi
%{_qt_examplesdir}/designer/calculatorform/calculatorform
%{_qt_examplesdir}/help/contextsensitivehelp/contextsensitivehelp
%{_qt_examplesdir}/linguist/arrowpad/arrowpad
%{_qt_examplesdir}/linguist/arrowpad/arrowpad_fr.qm
%{_qt_examplesdir}/linguist/arrowpad/arrowpad_nl.qm
%{_qt_examplesdir}/linguist/hellotr/hellotr
%{_qt_examplesdir}/linguist/hellotr/hellotr_la.qm
%{_qt_examplesdir}/linguist/i18n/i18n
%{_qt_examplesdir}/linguist/trollprint/trollprint
%{_qt_examplesdir}/linguist/trollprint/trollprint_pt.qm
%{_qt_examplesdir}/uitools/textfinder/textfinder
%{_qt_headerdir}/QtDesigner/
%{_qt_headerdir}/QtDesignerComponents/
%{_qt_headerdir}/QtHelp/
%{_qt_headerdir}/QtQDocCatch/
%{_qt_headerdir}/QtQDocCatchConversionsPrivate/
%{_qt_headerdir}/QtQDocCatchGeneratorsPrivate/
%{_qt_headerdir}/QtTools/
%{_qt_headerdir}/QtUiPlugin
%{_qt_headerdir}/QtUiTools/
%{_qt_libdir}/cmake/Qt6/FindWrapLibClang.cmake
%{_qt_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtToolsTestsConfig.cmake
%{_qt_libdir}/cmake/Qt6Designer/*.cmake
%{_qt_libdir}/cmake/Qt6DesignerComponentsPrivate/*.cmake
%{_qt_libdir}/cmake/Qt6Help/*.cmake
%{_qt_libdir}/cmake/Qt6Linguist/*.cmake
%{_qt_libdir}/cmake/Qt6LinguistTools/*.cmake
%{_qt_libdir}/cmake/Qt6QDocCatchConversionsPrivate/*.cmake
%{_qt_libdir}/cmake/Qt6QDocCatchGeneratorsPrivate/*.cmake
%{_qt_libdir}/cmake/Qt6QDocCatchPrivate/*.cmake
%{_qt_libdir}/cmake/Qt6Tools/*.cmake
%{_qt_libdir}/cmake/Qt6ToolsTools/*.cmake
%{_qt_libdir}/cmake/Qt6UiPlugin/*.cmake
%{_qt_libdir}/cmake/Qt6UiTools/
%{_qt_libdir}/libQt6Designer*.so
%{_qt_libdir}/libQt6Help.so
%{_qt_libdir}/libQt6UiTools.so
%{_qt_libdir}/pkgconfig/*.pc
%{_qt_libdir}/qt6/metatypes/qt6*_metatypes.json
%dir %{_qt_libdir}/cmake/Qt6Help/
%dir %{_qt_libdir}/cmake/Qt6Linguist
%dir %{_qt_libdir}/cmake/Qt6LinguistTools
%dir %{_qt_libdir}/cmake/Qt6QDocCatchConversionsPrivate
%dir %{_qt_libdir}/cmake/Qt6QDocCatchGeneratorsPrivate
%dir %{_qt_libdir}/cmake/Qt6QDocCatchPrivate
%dir %{_qt_libdir}/cmake/Qt6Tools/
%dir %{_qt_libdir}/cmake/Qt6ToolsTools/
%dir %{_qt_libdir}/cmake/Qt6UiPlugin/

%files static
%{_qt_libdir}/libQt6Designer*.prl
%{_qt_libdir}/libQt6Help.prl
%{_qt_libdir}/libQt6UiTools.prl

%files -n qt-doctools
%{_bindir}/qdoc*
%{_qt_bindir}/qdoc*
%{_qt_libexecdir}/qhelpgenerator*
%{_qt_libexecdir}/qtattributionsscanner*

%changelog
* Tue Jan 02 2024 Sam Meluch <sammeluch@microsoft.com> - 6.6.1-1
- Update qttools to version 6.6.1

* Mon Nov 28 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 5.12.5-6
- Update source download path
- License verified.

* Tue Mar 31 2020 Joe Schmitt <joschmit@microsoft.com> - 5.12.5-5
- Remove bad buildrequires

* Mon Mar 30 2020 Joe Schmitt <joschmit@microsoft.com> - 5.12.5-4
- Remove unused buildrequires
- Update Vendor and Distribution tags

* Mon Mar 30 2020 Mateusz Malisz <mamalisz@microsoft.com> - 5.12.5-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT).

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
