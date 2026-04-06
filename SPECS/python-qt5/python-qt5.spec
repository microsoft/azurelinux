# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} || 0%{?rhel} > 6
%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])" 2>/dev/null || echo "%{python3_sitearch}/dbus/mainloop")
%endif

# enable/disable individual modules
# drop power64, it's not supported yet (than)
%if 0
%ifarch %{?qt5_qtwebengine_arches}%{?!qt5_qtwebengine_arches:%{ix86} x86_64 %{arm} aarch64 mips mipsel mips64el}
%global webengine 1
%endif
%endif

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# see also https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/JQQ66XJSIT2FGTK2YQY7AXMEH5IXMPUX/
%undefine _strict_symbol_defs_build

%global snap dev2507081429

Summary: PyQt5 is Python bindings for Qt5
Name:    python-qt5
Version: 5.15.12
Release: 0.1%{?dist}

# Automatically converted from old format: GPLv3 - review is highly recommended.
License: GPL-3.0-only
Url:     http://www.riverbankcomputing.com/software/pyqt/
Source0: https://www.riverbankcomputing.com/static/Downloads/PyQt5/%{version}/pyqt5-%{version}%{?snap:.%{snap}}.tar.gz
#Source0: https://pypi.python.org/packages/source/P/PyQt5/PyQt5-{version}.tar.gz

Source1: macros.pyqt5

## upstream patches

## upstreamable patches
# support newer Qt5 releases, but may not be needed anymore?  -- rdieter
#Patch0: PyQt5-Timeline.patch

BuildRequires: make
BuildRequires: chrpath
BuildRequires: findutils
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-python)
%if ! 0%{?rhel}
BuildRequires: pkgconfig(phonon4qt5)
%endif
BuildRequires: qt5-qtbase-private-devel
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
BuildRequires: pkgconfig(Qt5Core) >= 5.5
%if 0%{?enginio}
BuildRequires: pkgconfig(Enginio)
%endif
BuildRequires: pkgconfig(Qt5Bluetooth)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Designer)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Location)
BuildRequires: pkgconfig(Qt5Multimedia) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(Qt5Nfc)
BuildRequires: pkgconfig(Qt5Network) pkgconfig(Qt5OpenGL)
BuildRequires: pkgconfig(Qt5Positioning)
BuildRequires: pkgconfig(Qt5Quick) pkgconfig(Qt5QuickWidgets)
#BuildRequires: pkgconfig(Qt5Script)
BuildRequires: pkgconfig(Qt5Sensors)
BuildRequires: pkgconfig(Qt5SerialPort)
BuildRequires: pkgconfig(Qt5Sql) pkgconfig(Qt5Svg) pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5Xml) pkgconfig(Qt5XmlPatterns)
BuildRequires: pkgconfig(Qt5WebChannel)
BuildRequires: pkgconfig(Qt5WebSockets)
BuildRequires: python%{python3_pkgversion}-devel python%{python3_pkgversion}
BuildRequires: python%{python3_pkgversion}-dbus
BuildRequires: %{py3_dist PyQt-builder} >= 1.1.0
BuildRequires: %{py3_dist sip} >= 5.3

# when split out
%if 0%{?webengine}
Obsoletes: python-qt5 < 5.5.1-10
%endif

%description
%{summary}.

%global __provides_exclude_from ^(%{_qt5_plugindir}/.*\\.so)$

%package rpm-macros
Summary: RPM macros %{name}
# when split out
Conflicts: python-qt5 < 5.6
Conflicts: python3-qt5 < 5.6
BuildArch: noarch
%description rpm-macros
%{summary}.

%package -n python%{python3_pkgversion}-qt5
Summary: Python 3 bindings for Qt5
# when split out
%if 0%{?webengine}
Obsoletes: python3-qt5 < 5.5.1-10
%endif
Provides: PyQt5 = %{version}-%{release}
Provides: PyQt5%{?_isa} = %{version}-%{release}
Provides: python%{python3_pkgversion}-PyQt5 = %{version}-%{release}
Provides: python%{python3_pkgversion}-PyQt5%{?_isa} = %{version}-%{release}
Requires: python%{python3_pkgversion}-qt5-base%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-qt5}
# When python-qt5-webkit was dropped
Obsoletes: python%{python3_pkgversion}-qt5-webkit < 5.15.11-4
%description -n python%{python3_pkgversion}-qt5
%{summary}.

%package -n python%{python3_pkgversion}-qt5-base
Summary: Python 3 bindings for Qt5 base
%{?_qt5:Requires: %{_qt5}%{?_isa} = %{_qt5_version}}
Provides: python%{python3_pkgversion}-PyQt5-base = %{version}-%{release}
Provides: python%{python3_pkgversion}-PyQt5-base%{?_isa} = %{version}-%{release}
Requires: %{name}-rpm-macros = %{version}-%{release}
Requires: python%{python3_pkgversion}-dbus
%{?python_provide:%python_provide python%{python3_pkgversion}-qt5-base}
%description -n python%{python3_pkgversion}-qt5-base
%{summary}.

%package -n python%{python3_pkgversion}-qt5-devel
Summary: Development files for python3-qt5
Requires: python%{python3_pkgversion}-qt5%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel
Provides: python%{python3_pkgversion}-PyQt5-devel = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-qt5-devel}
%description -n python%{python3_pkgversion}-qt5-devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt5 classes

%package doc
Summary: Developer documentation for %{name}
Provides: PyQt5-doc = %{version}-%{release}
BuildArch: noarch
%description doc
%{summary}.

%if 0%{?webengine}
%package -n python%{python3_pkgversion}-qt5-webengine
Summary: Python3 bindings for Qt5 WebEngine
BuildRequires: pkgconfig(Qt5WebEngine)
Obsoletes: python3-webengine < 5.5.1-13
Obsoletes: python3-qt5 < 5.5.1-10
Requires:  python%{python3_pkgversion}-qt5%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-qt5-webengine}
%description -n python%{python3_pkgversion}-qt5-webengine
%{summary}.
%endif


%prep
%setup -q -n pyqt5-%{version}%{?snap:.%{snap}}

#patch0 -p1


%build
## see also https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html

PATH=%{_qt5_bindir}:$PATH ; export PATH

# Python 3 build:
sip-build \
  --no-make \
  --qt-shared \
  --confirm-license \
  --qmake=%{_qt5_qmake} \
  --api-dir=%{_qt5_datadir}/qsci/api/python \
  --verbose \
  --dbus=%{_includedir}/dbus-1.0/ \
  --pep484-pyi \
  --qmake-setting 'QMAKE_CFLAGS_RELEASE="%{optflags}"' \
  --qmake-setting 'QMAKE_CXXFLAGS_RELEASE="%{optflags} `pkg-config --cflags dbus-python`"' \
  --qmake-setting 'QMAKE_LFLAGS_RELEASE="%{?__global_ldflags}"'

%make_build -C build


%install

# Python 3 build:
%make_install INSTALL_ROOT=%{buildroot} -C build
if [ "%{_prefix}" != "/usr" ]; then
  cp -ru %{buildroot}/usr/* %{buildroot}%{_prefix}/ || echo "Nothing to copy"
  rm -rf %{buildroot}/usr/*
fi

# Explicitly byte compile as the automagic byte compilation doesn't work for
# /app prefix in flatpak builds
%py_byte_compile %{__python3} %{buildroot}%{python3_sitearch}/PyQt5

# ensure .so modules are executable for proper -debuginfo extraction
find %{buildroot} -type f -name '*.so' | xargs chmod a+rx

# rpm macros
install -p -m644 -D %{SOURCE1} \
  %{buildroot}%{rpm_macros_dir}/macros.pyqt5
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{rpm_macros_dir}/macros.pyqt5


%files rpm-macros
%{rpm_macros_dir}/macros.pyqt5

%files -n python%{python3_pkgversion}-qt5
%if 0%{?enginio}
%{python3_sitearch}/PyQt5/Enginio.*
%endif
%{python3_sitearch}/PyQt5/QtBluetooth.*
%{python3_sitearch}/PyQt5/QtDesigner.*
%{python3_sitearch}/PyQt5/QtHelp.*
%{python3_sitearch}/PyQt5/QtLocation.*
%{python3_sitearch}/PyQt5/QtMultimedia.*
%{python3_sitearch}/PyQt5/QtMultimediaWidgets.*
%{python3_sitearch}/PyQt5/QtNfc.*
%{python3_sitearch}/PyQt5/QtPositioning.*
%{python3_sitearch}/PyQt5/QtQml.*
%{python3_sitearch}/PyQt5/QtQuick.*
%{python3_sitearch}/PyQt5/QtQuickWidgets.*
%{python3_sitearch}/PyQt5/QtSensors.*
%{python3_sitearch}/PyQt5/QtSerialPort.*
%{python3_sitearch}/PyQt5/QtSvg.*
%{python3_sitearch}/PyQt5/QtWebChannel.*
%{python3_sitearch}/PyQt5/QtWebSockets.*
%{python3_sitearch}/PyQt5/QtX11Extras.*
%{python3_sitearch}/PyQt5/QtXmlPatterns.*

%files -n python%{python3_pkgversion}-qt5-base
%doc NEWS README.md
%license LICENSE
%{python3_dbus_dir}/pyqt5.abi3.so
%dir %{python3_sitearch}/PyQt5/
%{python3_sitearch}/pyqt5-%{version}%{?snap:.%{snap}}.dist-info
%{python3_sitearch}/PyQt5/__pycache__/__init__.*
%{python3_sitearch}/PyQt5/__init__.py*
%{python3_sitearch}/PyQt5/Qt.*
%{python3_sitearch}/PyQt5/QtCore.*
%{python3_sitearch}/PyQt5/QtDBus.*
%{python3_sitearch}/PyQt5/QtGui.*
%{python3_sitearch}/PyQt5/QtNetwork.*
%{python3_sitearch}/PyQt5/QtOpenGL.*
%{python3_sitearch}/PyQt5/QtPrintSupport.*
%{python3_sitearch}/PyQt5/QtSql.*
%{python3_sitearch}/PyQt5/QtTest.*
%{python3_sitearch}/PyQt5/QtWidgets.*
%{python3_sitearch}/PyQt5/QtXml.*
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_2_0.*
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_2_1.*
%{python3_sitearch}/PyQt5/_QOpenGLFunctions_4_1_Core.*
# plugins
%{_qt5_plugindir}/PyQt5/
%{_qt5_plugindir}/designer/libpyqt5.so
%{python3_sitearch}/PyQt5/uic/
# *was* in python3-qt5-devel
%{_bindir}/pylupdate5
%{_bindir}/pyrcc5
%{_bindir}/pyuic5
%{python3_sitearch}/PyQt5/pylupdate.abi3.so
%{python3_sitearch}/PyQt5/pylupdate_main.py*
%{python3_sitearch}/PyQt5/__pycache__/pylupdate_main*
%{python3_sitearch}/PyQt5/pyrcc.abi3.so
%{python3_sitearch}/PyQt5/pyrcc_main.py*
%{python3_sitearch}/PyQt5/__pycache__/pyrcc_main*
%{python3_sitearch}/PyQt5/py.typed
%{python3_sitearch}/PyQt5/sip.pyi

%if 0%{?webengine}
%files -n python%{python3_pkgversion}-qt5-webengine
%{python3_sitearch}/PyQt5/QtWebEngine.*
%{python3_sitearch}/PyQt5/QtWebEngineCore.*
%{python3_sitearch}/PyQt5/QtWebEngineWidgets.*
%endif

%files -n python%{python3_pkgversion}-qt5-devel
%{python3_sitearch}/PyQt5/bindings/

%files doc
#doc doc/*
%doc examples/
# avoid dep on qscintilla-python, own %%_qt5_datadir/qsci/... here for now
%dir %{_qt5_datadir}/qsci/
%dir %{_qt5_datadir}/qsci/api/
%dir %{_qt5_datadir}/qsci/api/python/
%doc %{_qt5_datadir}/qsci/api/python/PyQt5.api


%changelog
* Tue Nov 04 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.12-0.1^dev2507081429
- Update to snapshot of pyqt5 5.15.12

* Tue Nov 04 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.11-13
- Rebuild (qt5)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.15.11-12
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.15.11-11
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Aug 04 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.11-10
- Fix build against Python 3.14

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.15.11-8
- Rebuilt for Python 3.14

* Mon May 26 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.11-7
- Rebuild (qt5)

* Tue Mar 25 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.11-6
- Move -webkit obsoletes to python3-qt5 package

* Mon Mar 24 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.11-5
- Fix -webkit obsoletes

* Wed Mar 19 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.11-4
- Obsolete python-qt5-webkit

* Wed Jan 22 2025 Jan Grulich <jgrulich@redhat.com> - 5.15.11-3
- Rebuild (qt5)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Zephyr Lykos <fedora@mochaa.ws> - 5.15.11-1
- new version

* Thu Sep 05 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.10-11
- Rebuild (qt5)

* Mon Jul 29 2024 Miroslav Suchý <msuchy@redhat.com> - 5.15.10-10
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.15.10-8
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.15.10-7
- Rebuilt for Python 3.13

* Thu May 30 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.10-6
- Rebuild (qt5)

* Fri Mar 15 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.10-5
- Rebuild (qt5)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Jan Grulich <jgrulich@redhat.com> - 5.15.10-2
- Rebuild (qt5)

* Sat Dec 02 2023 Scott Talbert <swt@techie.net> - 5.15.10-1
- 5.15.10 (#2252490)

* Mon Oct 09 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.9-7
- Rebuild (qt5)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 26 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 5.15.9-5
- Rebuilt for Python 3.12 with patched python-pyqt5-sip

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 5.15.9-4
- Rebuilt for Python 3.12

* Wed Jun 14 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.9-3
- Rebuild (qt5)

* Wed Apr 12 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.9-2
- Rebuild (qt5)

* Mon Mar 13 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.9-1
- 5.15.9

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Jan Grulich <jgrulich@redhat.com> - 5.15.6-10
- Rebuild (qt5)

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-9
- Rebuild (qt5)

* Wed Sep 21 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-8
- Rebuild (qt5)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-6
- Rebuild (qt5)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.15.6-5
- Rebuilt for Python 3.11

* Tue May 17 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-4
- Rebuild (qt5)

* Tue Mar 08 2022 Jan Grulich <jgrulich@redhat.com> - 5.15.6-3
- Rebuild (qt5)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 02 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.15.6-1
- 5.15.6

* Wed Sep 29 2021 FeRD (Frank Dana) <ferdnyc@gmail.com> - 5.15.4-2
- Eliminate conditional python3 build, associated redundancies
- Don't install py2+py3 wrappers for tool commands

* Wed Sep 15 2021 Sandro Mani <manisandro@gmail.com> - 5.15.4-1
- Update to 5.15.4

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Scott Talbert <swt@techie.net> - 5.15.0-12
- Fix build with sip 6

* Wed Jul 14 2021 Scott Talbert <swt@techie.net> - 5.15.0-11
- Remove sip depends from -devel package (to allow older sips)

* Sun Jun 06 2021 Scott Talbert <swt@techie.net> - 5.15.0-10
- Rebuild with sip 5; remove unused Python 2 support for clarity

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 5.15.0-9
- Rebuilt for Python 3.10

* Mon Feb 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.15.0-8
- Do not require Phonon on ELN/RHEL

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 16 12:00:16 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.0-6
- Bump for eln build

* Tue Dec  8 16:28:30 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.0-5
- Require webkit only on Fedora builds

* Thu Nov 26 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.15.0-4
- BR: qt5-qtbase-private-devel globally

* Mon Nov 23 07:54:30 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.0-3
- rebuild (qt5)

* Fri Sep 11 2020 Jan Grulich <jgrulich@redhat.com> - 5.15.0-2
- rebuild (qt5)

* Mon Aug 17 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.15.0-1
- 5.15.0

* Tue Aug 11 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-6
- fix FTBFS

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 5.14.2-3
- Rebuilt for Python 3.9

* Mon Apr 06 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-2
- rebuild (qt5)
- disable QtEnginio support f32+

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 26 2020 Kalev Lember <klember@redhat.com> - 5.13.2-4
- Fix building as a flatpak module

* Mon Dec 09 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.2-3
- rebuild (qt5)

* Fri Nov 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.13.2-2
- drop python2 support for f32+

* Sun Nov 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.13.2-1
- 5.13.2

* Tue Oct 01 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.13.1-1
- 5.13.1

* Wed Sep 25 2019 Jan Grulich <jgrulich@redhat.com> - 5.13.0-3
- rebuild (qt5)

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 5.13.0-2
- Rebuilt for Python 3.8

* Sun Aug 04 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.13.0-1
- 5.13.0

* Tue Jul 30 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-5
- move pyuic and friends to -base (#1728273)
- move Provides: PyQt5 to python3-qt5 (#1730635)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 26 2019 Gwyn Ciesla <gwync@protonmail.com> - 5.12.3-3
- Add ugly hack to work around setuptools issue for flatpak.
- https://github.com/pypa/setuptools/issues/1808

* Fri Jun 28 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-2
- rebuild (qtbase/qtmultimedia)

* Thu Jun 27 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-1
- 5.12.3

* Mon Jun 17 2019 Jan Grulich <jgrulich@redhat.com> - 5.12.2-5
- rebuild (qt5)

* Wed Jun 05 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.2-4
- rebuild (qt5)

* Sun May 12 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.2-3
- ship designer/qml plugins for python3 (only)

* Fri May 10 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.2-2
- python2-qt5-base: move qt plugins here (#1708274)

* Mon May 06 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.2-1
- 5.12.2

* Sun Apr 21 2019 Orion Poplawski <orion@nwra.com> - 5.12.1-2
- Build for python3 for EPEL

* Thu Mar 21 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.12.1-1
- 5.12.1
- omit webengine (now packaged separately)

* Sun Mar 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-6
- re-enable webengine support

* Fri Feb 15 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-5
- rebuild (qt5)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.11.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-3
- drop BR: python3-enum34

* Tue Dec 11 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-2
- rebuild (Qt5)

* Wed Oct 03 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3 (final)

* Fri Sep 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.3-0.4.dev1808131157
- rebuild (qt5)

* Thu Aug 30 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-0.3.dev1808131157
- unconditionally create rpm-macros
- handle api generation when one of python2/python3 is disabled

* Fri Aug 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-0.2.dev1808131157
- drop backward-compat py3_sipdir
- drop dep on python?-sip, rely only on python?-pyqt?-sip-api
- move versioned qt5/sip-api deps to -base

* Tue Aug 14 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-0.1.dev1808131157
- 5.11.3.dev1808131157 snapshot
- enable dist-info, include in -base (#1558187)

* Tue Aug 14 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.2-3
- support compat py3_sipdir
- python3-qt5: fix sip-api dep

* Mon Jul 30 2018 Sandro Mani <manisandro@gmail.com> - 5.11.2-2
- Add missing Requires: python2-enum34

* Tue Jul 10 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.2-1
- 5.11.2
- %%build: --no-dist-info (not supported when using DESTDIR= yet)
- configure.py: make check for PyQt5.sip module non-fatal

* Fri Jun 22 2018 Miro Hrončok <mhroncok@redhat.com> - 5.10.2-0.4.dev1805251538
- Rebuilt for Qt update in Python 3.7 side tag

* Thu Jun 21 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.2-0.3.dev1805251538
- rebuild (qt5)

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 5.10.2-0.2.dev1805251538
- Rebuilt for Python 3.7

* Tue May 29 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.2-0.1.dev1805251538
- 5.10.2.dev1805251538 snapshot

* Mon May 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-3
- rebuild (qt5)

* Tue Mar 20 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.10.1-2
- Add missing %%python_provide macros
- Rename python2 packages to python2-*

* Tue Mar 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1, use %%make_build

* Sat Mar 03 2018 Sérgio Basto <sergio@serjux.com> - 5.10-4
- Enable python3 on epel7

* Wed Feb 14 2018 Jan Grulich <jgrulich@redhat.com> - 5.10-3
- rebuild (qt5)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.10-1
- PyQt5-5.10

* Mon Jan 08 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-5
- explicitly support Qt5 newer than just 5.9.3 (+5.9.4,5.10.0,5.10.1)

* Wed Dec 20 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.2-4
- rebuild (qt5)

* Mon Dec 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-3
- License: GPLv3 (#1520186)

* Sun Nov 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-2
- rebuild (qt5)

* Sat Nov 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.2-1
- 5.9.2

* Mon Nov 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-2
- rebuild (sip)

* Sat Nov 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.1-1
- 5.9.1

* Mon Oct 09 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9-8
- rebuild (qt5)

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.7.19-5
- Cleanup spec file conditionals

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Florian Weimer <fweimer@redhat.com> - 5.9-5
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Than Ngo <than@redhat.com> - 5.9-4
- fixed bz#1348507, pyqt5 with python2 in isolated mode

* Wed Jul 26 2017 Than Ngo <than@redhat.com> - 5.9-3
- fixed bz#1348507 - Arbitrary code execution due to insecure loading
  of Python module from CWD

* Wed Jul 19 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9-2
- rebuild (qt5)

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9-1
- PyQt5-5.9

* Wed Jul 05 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-5
- rebuild (sip)

* Sun May 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-4
- restore -webengine

* Fri May 12 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-3
- (temp) disable -webengine support

* Thu May 11 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-2
- rebuild (qt5)

* Mon Apr 03 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-1
- PyQt5-5.8.2

* Wed Mar 29 2017 Thomas Woerner <twoerner@redhat.com> - 5.8.1-3
- New base sub package to provide QtBase only (RHBZ#1394626)
- New requirement from the main package to the base sub package

* Tue Mar 28 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-2
- add missing -webengine/-webkit descriptions
- better python3-qt5-devel description

* Tue Mar 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-1
- PyQt5-5.8.1

* Fri Feb 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8-2
- python3-qt5: omit sip files inadvertantly added in 5.7.1-5

* Thu Feb 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8-1
- PyQt5-5.8

* Thu Feb 16 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-5
- move -devel binaries to main pkg(s) (#1422613)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 30 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-3
- fix pyrcc5 wrapper typo

* Fri Jan 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-2
- add wrappers for pyrcc5,pylupdate5 (#141116,#1415812)
- update provides filtering

* Sat Dec 31 2016 Rex Dieter <rdieter@math.unl.edu> - 5.7.1-1
- PyQt5-5.7.1

* Wed Dec 21 2016 Kevin Fenzi <kevin@scrye.com> - 5.7-6
- Rebuild again for Python 3.6

* Thu Dec 15 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7-5
- restore qtwebengine support

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 5.7-4
- Rebuild for Python 3.6

* Sat Dec 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7-3
- (temporarily) omit webengine support on fc26

* Wed Nov 30 2016 Than Ngo <than@redhat.com> - 5.7-2
- rebuild against new qt5-qtbase-5.7.1

* Tue Jul 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7-1
- PyQt5-5.7

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Jul 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-7
- enable -webengine on f25+

* Sun Jul 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-6
- rebuild (qt5-qtbase), disable -webengine (temp on f25, until fixed)

* Wed Jul 06 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-5
- BR: qt5-qtbase-private-devel
- python3-qt5: add versioned qt5 dep (like base python-qt5 pkg has)

* Wed Jun 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-4
- rebuild (qt5)

* Wed Jun 15 2016 Than Ngo <than@redhat.com> - 5.6-3
- drop ppc ppc64 ppc64le, it's not supported yet

* Mon May 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-2
- -rpm-macros: Conflicts: python(3)-qt5 < 5.6

* Mon Apr 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6-1
- PyQt5-5.6

* Wed Apr 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.1-20
- rebuild (sip), re-enable -webengine for secondary archs

* Thu Mar 24 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-19
- limit -webengine support to just primary archs (for now)

* Thu Mar 24 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-18
- -rpm-macros subpkg

* Tue Mar 15 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-17
- rebuild (qt5-qtenginio)

* Mon Mar 14 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-16
- -webengine: add ExclusiveArch (matching qt5-qtwebengine's)

* Mon Mar 07 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-15
- add Obsoletes for misnamed -webengine/-webkit pkgs (#1315025)

* Sat Mar 05 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-14
- python-qt5 is not built with $RPM_OPT_FLAGS (#1314998)

* Thu Mar 03 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-13
- fix python3-qt5-webengine name

* Thu Mar 03 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-12
- fix python3-qt5-webkit name

* Wed Mar 02 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-11
- use safer subdir builds

* Wed Mar 02 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-10
- -webengine,-webkit subpkgs

* Sat Feb 27 2016 Christian Dersch <lupinix@mailbox.org> - 5.5.1-9
- Enabled QtWebEngine for Fedora >= 24

* Sat Feb 27 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-8
- rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-6
- explicitly set CFLAGS,CXXFLAGS,LFLAGS

* Wed Jan 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.1-5
- %%description: mention PyQt5

* Mon Dec 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-4
- rebuild (qt5), Provides: python2-qt5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-2
- rebuild (qt5)

* Mon Oct 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.1-1
- 5.5.1
- enable qtenginio, fix pyuic5 wrapper, use %%license

* Mon Oct 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5-2
- rebuild (qt5)

* Thu Jul 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5-1
- 5.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-1
- 5.4.2

* Fri Jun 05 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-5
- wrong python release used in pyuic5 launch script (#1193107)
- -doc: add qsci doc QyQt5.api content
- enable Qt5WebChannel/Qt5WebSockets support

* Fri Jun 05 2015 Sandro Mani <manisandro@gmail.com> - 5.4.1-4
- Add patch to fix python3 sip installation dir (#1228432)

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 5.4.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- rebuild (sip)

* Thu Feb 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-1
- 5.4.1

* Wed Feb 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-6
- rebuild (sip)

* Tue Jan 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-5
- +macros.pyqt5

* Fri Jan 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4-4
- -devel: restore dep on base pkg

* Sun Dec 28 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.4-3
- python3-qt5-devel subpkg

* Sat Dec 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4-2
- ensure .so modules are executable (for proper -debuginfo extraction)

* Fri Dec 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.4-1
- 5.4

* Thu Nov 13 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-6
- restore python3 support

* Tue Nov 11 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-5
- pkgconfig(QtOpenGL) being satisfied by qt4 devel (#1162415)

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-4
- try to determine dbus-python install paths dynamically (#1161121)

* Thu Nov 06 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.3.2-3
- Build failure in sipQtWebKitWidgestQWebInspector: qprinter.h not found (#1160932)
- python2_sitelib should be python2_sitearch (#1161121)

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- PyQt-gpl-5.3.2

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-1
- PyQt-gpl-5.3.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3-2
- python3: (Build)Requires: python3-dbus

* Mon Jun 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3-1
- PyQt-gpl-5.3
- +Qt5Bluetooth,Qt5Quick,Qt5SerialPorts support

* Mon May 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- rebuild (f21-python)
- +Qt5Positioning,Qt5Sensors support

* Sun Mar 16 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- PyQt-5.2.1

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.2-5
- Rebuild against fixed qt5-qtbase to fix -debuginfo (#1065636)

* Sat Feb 15 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-4
- python3-qt5 support

* Thu Feb 13 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-3
- Provides: PyQt5

* Thu Feb 06 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-2
- BR: python2-devel, use %%__python2 macro

* Wed Jan 08 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2-1
- PyQt-5.2
