# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global scintilla_ver 3.10.1

%bcond_without qt5
%bcond_without qt6

Summary: A Scintilla port to Qt
Name:    qscintilla
Version: 2.14.1
Release: 6%{?dist}

# Automatically converted from old format: GPLv3 - review is highly recommended.
License: GPL-3.0-only
Url:     http://www.riverbankcomputing.com/software/qscintilla/
%if 0%{?snap:1}
Source0: https://www.riverbankcomputing.com/static/Downloads/QScintilla/%{version}/QScintilla_gpl-%{version}-snapshot-%{snap}.tar.gz
%else
Source0: https://www.riverbankcomputing.com/static/Downloads/QScintilla/%{version}/QScintilla_src-%{version}.tar.gz
%endif

BuildRequires: make
BuildRequires: gcc-c++

Provides: bundled(scintilla) = %{scintilla_ver}

%description
QScintilla is a port of Scintilla to the Qt GUI toolkit.

%{?scintilla_ver:This version of QScintilla is based on Scintilla v%{scintilla_ver}.}

%if %{with qt5}
%package qt5
Summary: A Scintilla port to Qt5
Provides: bundled(scintilla) = %{scintilla_ver}
BuildRequires: pkgconfig(Qt5Designer)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)

%description qt5
%{summary}.


%package qt5-devel
Summary:  QScintilla Development Files
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel

%description qt5-devel
%{summary}.


# EPEL 10 does not have python3-qt5 yet
%if %{defined fedora}
%package -n python3-qscintilla-qt5
Summary:  QScintilla-qt5 python3 bindings
BuildRequires: python3-devel
BuildRequires: python3-qt5
BuildRequires: python3-qt5-devel
BuildRequires: %{py3_dist sip} >= 5.3
BuildRequires: %{py3_dist PyQt-builder} >= 1
Requires: %{name}-qt5%{?_isa} = %{version}-%{release}
Requires: python3-qt5%{?pyqt5_version: >= %{pyqt5_version}}

%description -n python3-qscintilla-qt5
%{summary}.


%package -n python3-qscintilla-qt5-devel
Summary:  Development files for QScintilla-qt5 python3 bindings
Requires: python3-qt5-devel

%description -n python3-qscintilla-qt5-devel
%{summary}.
%endif
%endif


%if %{with qt6}
%package qt6
Summary: A Scintilla port to Qt6
Provides: bundled(scintilla) = %{scintilla_ver}
BuildRequires: pkgconfig(Qt6Designer)
BuildRequires: pkgconfig(Qt6Gui)
BuildRequires: pkgconfig(Qt6Widgets)

%description qt6
%{summary}.


%package qt6-devel
Summary:  QScintilla Development Files
Requires: %{name}-qt6%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel

%description qt6-devel
%{summary}.


%package -n python3-qscintilla-qt6
Summary:  QScintilla-qt6 python3 bindings
BuildRequires: python3-devel
BuildRequires: python3-pyqt6
BuildRequires: python3-pyqt6-devel
BuildRequires: %{py3_dist sip} >= 5.3
BuildRequires: %{py3_dist PyQt-builder} >= 1
Requires: %{name}-qt6%{?_isa} = %{version}-%{release}
Requires: python3-pyqt6%{?pyqt6_version: >= %{pyqt6_version}}

%description -n python3-qscintilla-qt6
%{summary}.


%package -n python3-qscintilla-qt6-devel
Summary:  Development files for QScintilla-qt6 python3 bindings
Requires: python3-pyqt6-devel

%description -n python3-qscintilla-qt6-devel
%{summary}.
%endif



%prep
%autosetup -p1 -n QScintilla_src-%{version}%{?snap:-snapshot-%{snap}}


%build
export QMAKEFEATURES=$PWD/src/features;

%if %{with qt5}
cp -a src src-qt5
pushd src-qt5
%qmake_qt5 qscintilla.pro
%make_build
popd

cp -a designer designer-qt5
pushd designer-qt5
%qmake_qt5 designer.pro INCLUDEPATH+=../src-qt5 LIBS+=-L../src-qt5
%make_build
popd

%if %{defined fedora}
cp -a Python Python-qt5
pushd Python-qt5
ln -s pyproject-qt5.toml pyproject.toml
LD_LIBRARY_PATH=$PWD/../src-qt5 sip-build --no-make   --qmake=%{_qt5_qmake} --api-dir=%{_qt5_datadir}/qsci/api/python --verbose \
    --qmake-setting 'QMAKE_CXXFLAGS+="%{build_cxxflags}"' --qmake-setting 'QMAKE_LDFLAGS+="%{build_ldflags}"' \
    --qsci-include-dir=../src-qt5 --qsci-library-dir=../src-qt5/ --qsci-features-dir=../src-qt5/features
%make_build -C build
popd
%endif
%endif

%if %{with qt6}
cp -a src src-qt6
pushd src-qt6
%qmake_qt6 qscintilla.pro
%make_build
popd

cp -a designer designer-qt6
pushd designer-qt6
%qmake_qt6 designer.pro INCLUDEPATH+=../src-qt6 LIBS+=-L../src-qt6
%make_build
popd

cp -a Python Python-qt6
pushd Python-qt6
ln -s pyproject-qt6.toml pyproject.toml
LD_LIBRARY_PATH=$PWD/../src-qt6 sip-build --no-make   --qmake=%{_qt6_qmake} --api-dir=%{_qt6_datadir}/qsci/api/python --verbose \
    --qmake-setting 'QMAKE_CXXFLAGS+="%{build_cxxflags}"' --qmake-setting 'QMAKE_LDFLAGS+="%{build_ldflags}"' \
    --qsci-include-dir=../src-qt6 --qsci-library-dir=../src-qt6/ --qsci-features-dir=../src-qt6/features
%make_build -C build
popd
%endif


%install
%if %{with qt5}
%make_install -C src-qt5 INSTALL_ROOT=%{buildroot}
%make_install -C designer-qt5 INSTALL_ROOT=%{buildroot}
%if %{defined fedora}
%make_install -C Python-qt5/build INSTALL_ROOT=%{buildroot}
%endif

# Drop Python api files
rm -f %{buildroot}%{_qt5_datadir}/qsci/api/python/Python*.api
%endif

%if %{with qt6}
%make_install -C src-qt6 INSTALL_ROOT=%{buildroot}
%make_install -C designer-qt6 INSTALL_ROOT=%{buildroot}
%make_install -C Python-qt6/build INSTALL_ROOT=%{buildroot}

# Drop Python api files
rm -f %{buildroot}%{_qt6_datadir}/qsci/api/python/Python*.api
%endif

%if 0%{?flatpak}
# prefix is not configurable at build time
mv %{buildroot}/usr/include %{buildroot}/usr/%{_lib} %{buildroot}%{_prefix}/
mv %{buildroot}/usr/share/qt5/translations %{buildroot}%{_qt5_datadir}
mv %{buildroot}/usr/share/qt6/translations %{buildroot}%{_qt6_datadir}
rm -f %{buildroot}/usr/share/qt*/qsci/api/python/Python*.api
%endif

%find_lang qscintilla --with-qt
%if %{with qt5}
grep "%{_qt5_translationdir}" qscintilla.lang > qscintilla-qt5.lang
%endif
%if %{with qt6}
grep "%{_qt6_translationdir}" qscintilla.lang > qscintilla-qt6.lang
%endif


%if %{with qt5}
%files qt5 -f qscintilla-qt5.lang
%doc NEWS
%license LICENSE
%{_qt5_libdir}/libqscintilla2_qt5.so.15*
%{_qt5_plugindir}/designer/libqscintillaplugin.so

%files qt5-devel
%doc doc/html doc/Scintilla example
%{_qt5_headerdir}/Qsci/
%{_qt5_libdir}/libqscintilla2_qt5.so
%{_qt5_archdatadir}/mkspecs/features/qscintilla2.prf

%if %{defined fedora}
%files -n python3-qscintilla-qt5
%{python3_sitearch}/PyQt5/Qsci.*
%{_qt5_datadir}/qsci/
%{python3_sitearch}/qscintilla-%{version}.dist-info/

%files -n python3-qscintilla-qt5-devel
%{python3_sitearch}/PyQt5/bindings/Qsci/
%dir %{_qt5_datadir}/qsci/
%dir %{_qt5_datadir}/qsci/api/
%dir %{_qt5_datadir}/qsci/api/python/
%doc %{_qt5_datadir}/qsci/api/python/QScintilla.api
%endif
%endif

%if %{with qt6}
%files qt6 -f qscintilla-qt6.lang
%doc NEWS
%license LICENSE
%{_qt6_libdir}/libqscintilla2_qt6.so.15*
%{_qt6_plugindir}/designer/libqscintillaplugin.so

%files qt6-devel
%doc doc/html doc/Scintilla example
%{_qt6_headerdir}/Qsci/
%{_qt6_libdir}/libqscintilla2_qt6.so
%{_qt6_archdatadir}/mkspecs/features/qscintilla2.prf

%files -n python3-qscintilla-qt6
%{python3_sitearch}/PyQt6/Qsci.*
%{_qt6_datadir}/qsci/
%{python3_sitearch}/pyqt6_qscintilla-%{version}.dist-info/

%files -n python3-qscintilla-qt6-devel
%{python3_sitearch}/PyQt6/bindings/Qsci/
%dir %{_qt6_datadir}/qsci/
%dir %{_qt6_datadir}/qsci/api/
%dir %{_qt6_datadir}/qsci/api/python/
%doc %{_qt6_datadir}/qsci/api/python/PyQt6-QScintilla.api
%endif


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.14.1-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jul 29 2024 Miroslav Suchý <msuchy@redhat.com> - 2.14.1-3
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.14.1-1
- Update to 2.14.1

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.13.4-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 2.13.4-2
- Rebuilt for Python 3.12

* Mon Apr 03 2023 Sandro Mani <manisandro@gmail.com> - 2.13.4-1
- Update to 2.13.4

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Sandro Mani <manisandro@gmail.com> - 2.13.0-5
- Add qt6 build

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.13.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 15 2021 Sandro Mani <manisandro@gmail.com> - 2.13.0-1
- Update to 2.13.0
- Drop qt4/py2 code

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 03 2021 Scott Talbert <swt@techie.net> - 2.11.6-1
- Update to new upstream release 2.11.6 and build with sip 5

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.11.5-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 17 2020 Rex Dieter <rdieter@fedoraproject.org> - 2.11.5-1
- 2.11.5, fix FTBFS harder

* Tue Aug 11 2020 Rex Dieter <rdieter@fedoraproject.org> - 2.11.2-14
- fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-13
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.11.2-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 2.11.2-9
- drop qt4/python2 support for f32+

* Wed Oct 30 2019 Rex Dieter <rdieter@fedoraproject.org> - 2.11.2-8
- revive qt4/python2 support on fedora, still needed by hgview (see also #1738953)

* Wed Oct 30 2019 Rex Dieter <rdieter@fedoraproject.org> - 2.11.2-7
- cleanup/fix conditionals
- drop qt4/python2 support for f32+

* Mon Sep  9 2019 Orion Poplawski <orion@nwra.com> - 2.11.2-6
- Build without python2 and qt4 for EPEL8

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.11.2-5
- Rebuilt for Python 3.8

* Mon Aug 05 2019 Rex Dieter <rdieter@fedoraproject.org> - 2.11.2-4
- re-enable python2, python-qt5 FTBFS fixed (#1737206)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Rex Dieter <rdieter@fedoraproject.org> - 2.11.2-2
- cleanup, fix qsci docs and %%check logic
- include python dist-info for qt5 builds
- drop python2 on f31+ for now due to FTBFS

* Thu Jun 27 2019 Rex Dieter <rdieter@fedoraproject.org> - 2.11.2-1
- 2.11.2

* Fri Feb 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 2.11.1-1
- 2.11.1

* Mon Feb 11 2019 Rex Dieter <rdieter@fedoraproject.org> - 2.11-1
- 2.11

* Thu Oct 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.8-1
- 2.10.8

* Sun Aug 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.7-5
- %build: --verbose --sip=/usr/bin/sip-pyqt? wrapper

* Fri Aug 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.7-4
- drop py3_sip hacks
- use python?-pyqt?-sip-api dep

* Sun Jul 22 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.7-3
- fix build (adapt to related sip changes)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.7-1
- qscintilla-2.10.7

* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 2.10.5-2
- Rebuilt for Python 3.7
- BR pythonX-devel not to be forgotten next time

* Sat Jun 23 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.5-1
- qscintilla-2.10.5

* Wed Apr 11 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.4-1
- qscintilla-2.10.4

* Fri Mar 23 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.10.3-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.3-1
- qscintilla-2.10.3
- BR: gcc-c++, use %%make_build

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.10.2-2
- rebuild (qt5,PyQt5)

* Sat Nov 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.10.2-1
- qscintilla-2.10.2

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.10.1-1
- qscintilla-2.10.1

* Thu Apr 27 2017 Sandro Mani <manisandro@gmail.com> - 2.10-5
- Add python2-qscintilla-qt5

* Thu Mar 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.10-4
- rebuild (python-qt5), -qscintilla: relax pyqt runtime dep

* Wed Mar 01 2017 Sandro Mani <manisandro@gmail.com> - 2.10-3
- Fix incorrect requires for python3-qscintilla-qt5-devel on python-qt5-devel -> python3-qt5-devel

* Mon Feb 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.10-2
- -devel: introduce compat symlinks

* Mon Feb 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 2.10-1
- qscintilla-2.10

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 01 2017 Rex Dieter <rdieter@math.unl.edu> - 2.9.4-1
- qscintilla-2.9.4

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.9.3-3
- Rebuild for Python 3.6

* Wed Jul 27 2016 Rex Dieter <rdieter@fedoraproject.org> 2.9.3-2
- rebuild (python-qt5)

* Tue Jul 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.9.3-1
- qscintilla-2.9.3

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.2-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.9.2-4
- rebuild (python-qt5)

* Wed Apr 20 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.9.2-3
- rebuild (qt)

* Mon Apr 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.9.2-2
- support bootstapping
- rename qscintilla-python => python2-qscintilla
- Provides: python(2|3)-PyQt(4|5)-Qsci

* Mon Apr 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.9.2-1
- qscintilla-2.9.2

* Wed Apr 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 2.9.1-6
- rebuild (sip), Provides: python2-qscintilla(-devel)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 11 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 05 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9.1-3
- python3-qscintilla-qt5: use python3-qt5 consistently

* Wed Oct 28 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9.1-2
- rebuild (python-qt5)

* Sat Oct 24 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9.1-1
- qscintilla-2.9.1

* Tue Sep 08 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9-5
- -python-qt5: tighten python-qt5 dep (#1260876)

* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9-4
- fix libqscintillaplugin.so linkage (#1231721)

* Sun Apr 26 2015 Rex Dieter <rdieter@fedoraproject.org> - 2.9-3
- use %%qmake_qt4 macroo
- Qt5 qscintilla2.prf is installed in bad location (#1215380)

* Thu Apr 23 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9-2
- Provides: bundled(scintilla) = 3.5.4

* Mon Apr 20 2015 Rex Dieter <rdieter@fedoraproject.org> 2.9-1
- 2.9

* Wed Feb 18 2015 Orion Poplawski <orion@cora.nwra.com> - 2.8.4-3
- Rebuild for gcc 5 C++11

* Sun Dec 28 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.4-2
- enable -qt5 support

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.4-1
- QScintiall-2.8.4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 03 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.3-1
- QScintiall-2.8.3

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.3-0.3.9b7b5393f228
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Rex Dieter <rdieter@fedoraproject.org> - 2.8.3-0.2.9b7b5393f228
- QScintilla-gpl-2.8.3-snapshot-9b7b5393f228
- python: explicitly set QMAKEFEATURES (bug #1104559)

* Mon Jun 02 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.3-0.1.f7b1c9821894
- QScintiall-2.8.3-f7b1c9821894 snapshot (2.8.2 FTBFS)

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 17 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.1-3
- enable python3 bindings (#1065223)

* Mon Mar 17 2014 Rex Dieter <rdieter@fedoraproject.org> 2.8.1-2
- designer plugin: Undefined reference to QsciScintilla::QsciScintilla... (#1077146)

* Sun Mar 16 2014 Rex Dieter <rdieter@fedoraproject.org> - 2.8.1-1
- QScintilla-2.8.1
- Provides: python-qscintilla
- experimental qt5/python3 support (not enabled yet)

* Fri Nov 08 2013 Rex Dieter <rdieter@fedoraproject.org> 2.8-1
- QScintilla-2.8

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 2.7.2-3
- rebuild (PyQt4), refresh incpath patch

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 2.7.2-1
- QScintilla-2.7.2
- prune changelog

* Mon Jun 17 2013 Rex Dieter <rdieter@fedoraproject.org> 2.7.1-2
- rebuild (sip)

* Sun Mar 03 2013 Rex Dieter <rdieter@fedoraproject.org> 2.7.1-1
- 2.7.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 17 2012 Rex Dieter <rdieter@fedoraproject.org> 2.7-1
- 2.7

* Mon Oct 01 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.2-3
- rebuild (sip)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.2-1
- 2.6.2

* Sat Feb 11 2012 Rex Dieter <rdieter@fedoraproject.org> 2.6.1-1
- 2.6.1
- pkgconfig-style deps

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2.6-2
- rebuild (sip/PyQt4)

* Sat Dec 03 2011 Rex Dieter <rdieter@fedoraproject.org> 2.6-1
- 2.6

* Fri Nov 11 2011 Rex Dieter <rdieter@fedoraproject.org> 2.5.1-2
- rebuild (sip)

* Fri May 06 2011 Rex Dieter <rdieter@fedoraproject.org> 2.5.1-1
- 2.5.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.6-1
- 2.4.6

* Thu Sep 09 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.5-1
- 2.4.5

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 14 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.4-1
- 2.4.4

* Thu Mar 18 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.3-1
- 2.4.3

* Thu Jan 21 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.2-1
- 2.4.2

* Fri Jan 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4.1-1
- 2.4.1 
- pyqt4_version 4.7

* Thu Jan 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.4-10 
- rebuild (sip)

* Fri Nov 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-9
- -python: Requires: sip-api(%%_sip_api_major) >= %%_sip_api
- -python-devel: Requires: sip-devel

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-8 
- rebuild (for qt-4.6.0-rc1, f13+)

* Wed Nov 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-7
- pyqt4_version 4.6.1

* Wed Oct 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-6
- autocomplete_popup patch

* Fri Oct 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-5
- rebuild (PyQt4)

* Tue Aug 11 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-4
- -python-devel: make noarch, drop dep on -python

* Sat Aug 08 2009 Rex Dieter <rdieter@fedoraproject.org - 2.4-3
- include designer plugin in main pkg, Obsoletes: qscintilla-designer

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 2.4-1
- QScintilla-gpl-2.4

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.3.2-2
- Rebuild for Python 2.6

* Mon Nov 17 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3.2-1
- Qscintilla-gpl-2.3.2
- soname bump 4->5

* Mon Nov 10 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3.1-1
- Qscintilla-gpl-2.3.1

* Mon Sep 22 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.3-1
- Qscintilla-gpl-2.3
- scintilla_ver is missing (#461777)

* Fri Jul 18 2008 Dennis Gilmore <dennis@ausil.us> - 2.2-3
- rebuild for newer PyQT4
- fix #449423 properly

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.2-2
- fix build (#449423)

* Mon May 05 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.2-1
- Qscintilla-gpl-2.2
- License: GPLv3 or GPLv2 with exceptions

* Thu Feb 14 2008 Rex Dieter <rdieter@fedoraproject.org> - 2.1-4
- use %%_qt4_* macros (preparing for qt4 possibly moving %%_qt4_datadir)
- -python: fix Requires
- -python-devel: new pkg
- omit Obsoletes: PyQt-qscintilla 
  (leave that to PyQt, that can get the versioning right)

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-3
- fix typo in Obsoletes: on python package

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-2
- remove dumb require on di from qscintilla-python

* Mon Jan 28 2008 Dennis Gilmore <dennis@ausil.us> - 2.1-1
- update to 2.1 branch
