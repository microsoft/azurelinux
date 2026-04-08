# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} || 0%{?rhel} > 6
%global python3_dbus_dir %(%{__python3} -c "import dbus.mainloop; print(dbus.mainloop.__path__[0])" 2>/dev/null || echo "%{python3_sitearch}/dbus/mainloop")
%endif

#define snap dev2503211311

Summary: PyQt6 is Python bindings for Qt6
Name:    python-pyqt6
Version: 6.10.2
Release: 3%{?dist}
License: gpl-3.0-only
Url:     http://www.riverbankcomputing.com/software/pyqt/
Source0: https://pypi.python.org/packages/source/P/PyQt6/pyqt6-%{version}%{?snap:.%{snap}}.tar.gz
Source1: macros.pyqt6

BuildRequires: make
BuildRequires: chrpath
BuildRequires: findutils
BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(dbus-python)
BuildRequires: pkgconfig(libpulse-mainloop-glib)

BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Bluetooth)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Designer)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6Multimedia)
BuildRequires: cmake(Qt6Nfc)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGL)
%if 0%{?fedora} || 0%{?epel}
%ifarch %{qt6_qtwebengine_arches}
BuildRequires: cmake(Qt6Pdf) cmake(Qt6PdfWidgets)
%endif
%endif
BuildRequires: cmake(Qt6Positioning)
BuildRequires: cmake(Qt6Quick) cmake(Qt6QuickWidgets)
BuildRequires: cmake(Qt6Sensors)
BuildRequires: cmake(Qt6SerialPort)
BuildRequires: cmake(Qt6Sql)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6Test)
BuildRequires: cmake(Qt6TextToSpeech)
BuildRequires: cmake(Qt6Xml)
BuildRequires: cmake(Qt6WebChannel)
BuildRequires: cmake(Qt6WebSockets)
BuildRequires: cmake(Qt6Quick3D)
BuildRequires: cmake(Qt6Quick3DRuntimeRender)
BuildRequires: cmake(Qt6RemoteObjects)

BuildRequires: python%{python3_pkgversion}-devel python%{python3_pkgversion}
BuildRequires: python%{python3_pkgversion}-dbus
BuildRequires: %{py3_dist PyQt-builder} >= 1.1.0
BuildRequires: %{py3_dist sip}

%description
%{summary}.

%global __provides_exclude_from ^(%{_qt6_plugindir}/.*\\.so)$

%package rpm-macros
Summary: RPM macros %{name}
BuildArch: noarch
%description rpm-macros
%{summary}.

%package -n python%{python3_pkgversion}-pyqt6
Summary: Python 3 bindings for Qt6
Provides: PyQt6 = %{version}-%{release}
Provides: PyQt6%{?_isa} = %{version}-%{release}
Provides: python%{python3_pkgversion}-PyQt6 = %{version}-%{release}
Provides: python%{python3_pkgversion}-PyQt6%{?_isa} = %{version}-%{release}
Requires: python%{python3_pkgversion}-pyqt6-base%{?_isa} = %{version}-%{release}
%{?py_provides:%py_provides python%{python3_pkgversion}-pyqt6}

%description -n python%{python3_pkgversion}-pyqt6
%{summary}.

%package -n python%{python3_pkgversion}-pyqt6-base
Summary: Python 3 bindings for Qt6 base
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
Provides: python%{python3_pkgversion}-PyQt6-base = %{version}-%{release}
Provides: python%{python3_pkgversion}-PyQt6-base%{?_isa} = %{version}-%{release}
Requires: %{name}-rpm-macros = %{version}-%{release}
Requires: python%{python3_pkgversion}-dbus
%{?py_provides:%py_provides python%{python3_pkgversion}-pyqt6-base}

%description -n python%{python3_pkgversion}-pyqt6-base
%{summary}.

%package -n python%{python3_pkgversion}-pyqt6-devel
Summary: Development files for python3-qt6
Requires: python%{python3_pkgversion}-pyqt6%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel
Provides: python%{python3_pkgversion}-PyQt6-devel = %{version}-%{release}
%{?py_provides:%py_provides python%{python3_pkgversion}-pyqt6-devel}

%description -n python%{python3_pkgversion}-pyqt6-devel
Files needed to build other bindings for C++ classes that inherit from any
of the Qt6 classes.

%package doc
Summary: Developer documentation for %{name}
Provides: PyQt6-doc = %{version}-%{release}
BuildArch: noarch
%description doc
%{summary}.


%prep
%autosetup -n pyqt6-%{version}%{?snap:.%{snap}} -p1

%build

PATH=%{_qt6_bindir}:$PATH ; export PATH

# Python 3 build:
sip-build \
  --no-make \
  --qt-shared \
  --confirm-license \
  --qmake=%{_qt6_qmake} \
  --api-dir=%{_qt6_datadir}/qsci/api/python \
  --verbose \
  --dbus=%{_includedir}/dbus-1.0/ \
  --pep484-pyi \
  --qmake-setting 'QMAKE_CFLAGS_RELEASE="%{build_cflags}"' \
  --qmake-setting 'QMAKE_CXXFLAGS_RELEASE="%{build_cxxflags} `pkg-config --cflags dbus-python` -DQT_NO_INT128 -std=c++17"' \
  --qmake-setting 'QMAKE_LFLAGS_RELEASE="%{build_ldflags}"'

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
%py_byte_compile %{__python3} %{buildroot}%{python3_sitearch}/PyQt6

# ensure .so modules are executable for proper -debuginfo extraction
find %{buildroot} -type f -name '*.so' | xargs chmod a+rx

# rpm macros
install -p -m644 -D %{SOURCE1} \
  %{buildroot}%{_rpmmacrodir}/macros.pyqt6
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{_rpmmacrodir}/macros.pyqt6


%files rpm-macros
%{_rpmmacrodir}/macros.pyqt6

%files -n python%{python3_pkgversion}-pyqt6

%{python3_sitearch}/PyQt6/QtBluetooth.*
%{python3_sitearch}/PyQt6/QtDesigner.*
%{python3_sitearch}/PyQt6/QtHelp.*
%{python3_sitearch}/PyQt6/QtMultimedia.*
%{python3_sitearch}/PyQt6/QtMultimediaWidgets.*
%{python3_sitearch}/PyQt6/QtNfc.*
%if 0%{?fedora} || 0%{?epel}
%ifarch %{qt6_qtwebengine_arches}
%{python3_sitearch}/PyQt6/QtPdf.*
%{python3_sitearch}/PyQt6/QtPdfWidgets.*
%endif
%endif
%{python3_sitearch}/PyQt6/QtPositioning.*
%{python3_sitearch}/PyQt6/QtQml.*
%{python3_sitearch}/PyQt6/QtQuick.*
%{python3_sitearch}/PyQt6/QtQuickWidgets.*
%{python3_sitearch}/PyQt6/QtSensors.*
%{python3_sitearch}/PyQt6/QtSerialPort.*
%{python3_sitearch}/PyQt6/QtSvg.*
%{python3_sitearch}/PyQt6/QtTextToSpeech.*
%{python3_sitearch}/PyQt6/QtWebChannel.*
%{python3_sitearch}/PyQt6/QtWebSockets.*
%{python3_sitearch}/PyQt6/QtOpenGLWidgets.*
%{python3_sitearch}/PyQt6/QtSvgWidgets.*
%{python3_sitearch}/PyQt6/QtQuick3D.*
%{python3_sitearch}/PyQt6/QtRemoteObjects.*
%{python3_sitearch}/PyQt6/QtSpatialAudio.*


%files -n python%{python3_pkgversion}-pyqt6-base
%doc NEWS
%license LICENSE
%{python3_dbus_dir}/pyqt6.abi3.so
%dir %{python3_sitearch}/PyQt6/
%{python3_sitearch}/pyqt6-%{version}%{?snap:.%{snap}}.dist-info
%{python3_sitearch}/PyQt6/__pycache__/__init__.*
%{python3_sitearch}/PyQt6/__init__.py*
%{python3_sitearch}/PyQt6/QtCore.*
%{python3_sitearch}/PyQt6/QtDBus.*
%{python3_sitearch}/PyQt6/QtGui.*
%{python3_sitearch}/PyQt6/QtNetwork.*
%{python3_sitearch}/PyQt6/QtOpenGL.*
%{python3_sitearch}/PyQt6/QtPrintSupport.*
%{python3_sitearch}/PyQt6/QtSql.*
%{python3_sitearch}/PyQt6/QtTest.*
%{python3_sitearch}/PyQt6/QtWidgets.*
%{python3_sitearch}/PyQt6/QtXml.*

# plugins
%{_qt6_plugindir}/PyQt6/
%{_qt6_plugindir}/designer/libpyqt6.so
%{python3_sitearch}/PyQt6/uic/
%{python3_sitearch}/PyQt6/lupdate/
%{_bindir}/pylupdate6
%{_bindir}/pyuic6
%{python3_sitearch}/PyQt6/py.typed
%{python3_sitearch}/PyQt6/sip.pyi

%files -n python%{python3_pkgversion}-pyqt6-devel
%{python3_sitearch}/PyQt6/bindings/


%files doc
#doc doc/*
%doc examples/
# avoid dep on qscintilla-python, own %%_qt6_datadir/qsci/... here for now
%dir %{_qt6_datadir}/qsci/
%dir %{_qt6_datadir}/qsci/api/
%dir %{_qt6_datadir}/qsci/api/python/
%doc %{_qt6_datadir}/qsci/api/python/PyQt6.api


%changelog
* Tue Feb 10 2026 Jan Grulich <jgrulich@redhat.com> - 6.10.2-3
- Rebuild (qt6)

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 09 2026 Sandro Mani <manisandro@gmail.com> - 6.10.2-1
- Update to 6.10.2

* Sat Dec 27 2025 Sandro Mani <manisandro@gmail.com> - 6.10.1-2
- Revert changes to createMimeDataFromSelection

* Sat Dec 13 2025 Sandro Mani <manisandro@gmail.com> - 6.10.1-1
- Update to 6.10.1

* Fri Nov 21 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-2
- Rebuild (qt6)

* Thu Oct 23 2025 Jan Grulich <jgrulich@redhat.com> - 6.10.0-1
- 6.10.0

* Wed Oct 08 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-8
- Rebuild (qt6)

* Tue Sep 30 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-7
- Rebuild (qt6)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.9.1-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 01 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-5
- Rebuild (qt6)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 6.9.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 08 2025 Python Maint <python-maint@redhat.com> - 6.9.1-2
- Rebuilt for Python 3.14

* Fri Jun 06 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.1-1
- 6.9.1

* Fri Jun 06 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-3
- Rebuild (qt6)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 6.9.0-2
- Rebuilt for Python 3.14

* Fri Apr 11 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- Update to stable 6.9.0

* Fri Apr 04 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-0.2^dev2503211311
- Rebuild (qt6)

* Wed Mar 26 2025 Jan Grulich <jgrulich@redhat.com> - 6.9.0-0.1^dev2503211311
- Update to snapshot of 6.9.0

* Tue Mar 04 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 6.8.1-0.2
- Rebuild for ppc64le enablement of QtPdf/QtWebEngine

* Mon Feb 03 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.1-0.1^dev2502011625
- Update to snapshot of 6.8.1

* Mon Feb 03 2025 Jan Grulich <jgrulich@redhat.com> - 6.8.0-3
- Rebuild (qt6)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 09 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-1
- 6.8.0

* Fri Dec 06 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.0-0.3^dev2412041050
- Update to latest snapshot

* Wed Dec 04 2024 Jan Grulich <grulja@gmail.com> - 6.8.0-0.2^dev2410141303
- Rebuild (qt6)

* Wed Oct 16 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-0.1^dev2410141303
- Update to snapshot of 6.8.0

* Mon Oct 14 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.1-2
- Rebuild (qt6)

* Sat Jul 20 2024 Sandro Mani <manisandro@gmail.com> - 6.7.1-1
- Update to 6.7.1

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-5
- Rebuild (qt6)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.7.0-4
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.7.0-3
- Rebuilt for Python 3.13

* Tue May 21 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-2
- Rebuild (qt6)

* Fri Apr 26 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-1
- Update to 6.7.0

* Mon Apr 08 2024 Jan Grulich <jgrulich@redhat.com> - 6.7.0-0.1^dev2404051544
- Update to snapshot of 6.7.0

* Thu Apr 04 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.1-6
- Rebuild (qt6)

* Fri Feb 16 2024 Jan Grulich <jgrulich@redhat.com> - 6.6.1-5
- Rebuild (qt6)

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 06 2023 Jonathan Wright <jonathan@almalinux.org> - 6.6.1-1
- Update to 6.1.2 rhbz#2252735

* Wed Nov 29 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-2
- Rebuild (qt6)

* Mon Oct 30 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sat Oct 14 2023 Sandro Mani <manisandro@gmail.com> - 6.5.3-1
- Update to 6.5.3

* Fri Oct 13 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-4
- Rebuild (qt6)

* Thu Oct 05 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.2-3
- Rebuild for Qt Private API

* Tue Sep 05 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.2-2
- Enable QtPdf and QtTextToSpeech bindings

* Mon Jul 24 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-5
- Rebuild for qtbase private API version change

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-4
- Rebuild for qtbase private API version change

* Mon Jun 26 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 6.5.1-3
- Rebuilt for Python 3.12 with patched python-pyqt6-sip

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 6.5.1-2
- Rebuilt for Python 3.12

* Mon Jun 05 2023 Sandro Mani <manisandro@gmail.com> - 6.5.1-1
- Update to 6.5.1

* Fri May 26 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-2
- Rebuild (qt6)

* Thu May 18 2023 Miro Hrončok <mhroncok@redhat.com> - 6.5.0-1
- Update to 6.5.0

* Tue Apr 04 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.0-7
- Rebuild (qt6)

* Wed Mar 29 2023 Tomas Popela <tpopela@redhat.com> - 6.4.0-6
- Rebuild to fix ELN build

* Mon Mar 27 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.0-5
- Rebuild (qt6)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.0-3
- Rebuild (qt6)

* Thu Nov 24 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-2
- Rebuild (qt6)

* Tue Nov 08 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0

* Tue Sep 06 2022 Onuralp Sezer <thunderbirdtr@fedoraproject.org> - 6.3.1-1
- 6.3.1

* Tue Sep 06 2022 Onuralp Sezer <thunderbirdtr@fedoraproject.org> - 6.3.0-1
- Initial PyQt6

