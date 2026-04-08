# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global		framework kcoreaddons

Name:		kf6-%{framework}
Version:	6.23.0
Release:	1%{?dist}
Summary:	KDE Frameworks 6 Tier 1 addon with various classes on top of QtCore
License:	BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND GPL-2.0-or-later AND MPL-1.1 AND LGPL-2.0-only AND LGPL-2.1-or-later AND LGPL-3.0-only AND LGPL-2.1-only WITH Qt-LGPL-exception-1.1
URL:		https://invent.kde.org/frameworks/%{framework}
Source0:	https://download.kde.org/%{stable_kf6}/frameworks/%{majmin_ver_kf6}/%{framework}-%{version}.tar.xz
Source1:	https://download.kde.org/%{stable_kf6}/frameworks/%{majmin_ver_kf6}/%{framework}-%{version}.tar.xz.sig

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  extra-cmake-modules >= %{version}
BuildRequires:  kf6-rpm-macros
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6DBusTools)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6QmlTools)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  systemd-devel

# required for pyside6 python bindings
BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  clang-devel
BuildRequires:  cmake(Shiboken6)
BuildRequires:  cmake(PySide6)

Requires:       kf6-filesystem

%description
KCoreAddons provides classes built on top of QtCore to perform various tasks
such as manipulating mime types, autosaving files, creating backup files,
generating random sequences, performing text manipulations such as macro
replacement, accessing user information and many more.

%package -n python3-%{name}
Summary:    Qt for Python bindings for %{name}
%description -n python3-%{name}
The package contains the pyside6 bindings library for %{name}

%package    devel
Summary:    Development files for %{name}
Requires:   %{name} = %{version}-%{release}
Requires:   qt6-qtbase-devel
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Developer Documentation files for %{name}
BuildArch:      noarch

%description    doc
Developer Documentation files for %{name} for use with KDevelop or QtCreator.

%package        html
Summary:        Developer Documentation files for %{name}
BuildArch:      noarch
%description    html
Developer Documentation files for %{name} in HTML format

%prep
%autosetup -n %{framework}-%{version} -p1

%build
%cmake_kf6
%cmake_build_kf6

%install
%cmake_install_kf6

%find_lang_kf6 kcoreaddons6_qt
%find_lang_kf6 kde6_xml_mimetypes
cat *.lang > all.lang

%files -f all.lang
%doc README.md
%{_kf6_datadir}/mime/packages/kde6.xml
%{_kf6_datadir}/qlogging-categories6/%{framework}.*
%{_kf6_libdir}/libKF6CoreAddons.so.*
%{_kf6_libdir}/qt6/qml/org/kde/coreaddons/libkcoreaddonsplugin.so
%{_kf6_libdir}/qt6/qml/org/kde/coreaddons/qmldir
%{_datadir}/kf6/jsonschema/kpluginmetadata.schema.json
%{_libdir}/qt6/qml/org/kde/coreaddons/kcoreaddonsplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/coreaddons/kde-qmlmodule.version

%files -n python3-%{name}
%{python3_sitearch}/KCoreAddons.cpython-%{python3_version_nodots}*.so

%files devel
%{_kf6_includedir}/KCoreAddons/
%dir %{_includedir}/PySide6/KCoreAddons/
%{_includedir}/PySide6/KCoreAddons/kcoreaddons_python.h
%dir %{_kf6_datadir}/PySide6/typesystems/
%{_kf6_datadir}/PySide6/typesystems/typesystem_kcoreaddons.xml
%{_kf6_libdir}/cmake/KF6CoreAddons/
%{_kf6_libdir}/pkgconfig/KF6CoreAddons.pc
%{_kf6_libdir}/libKF6CoreAddons.so
%{_qt6_docdir}/*/*.tags
%{_qt6_docdir}/*/*.index

%files doc
%{_qt6_docdir}/*.qch

%files html
%{_qt6_docdir}/*/*
%exclude %{_qt6_docdir}/*/*.tags
%exclude %{_qt6_docdir}/*/*.index


%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.23.0-1
- 6.23.0

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 02 2026 farchord@gmail.com - 6.22.0-1
- 6.22.0

* Fri Dec 05 2025 Steve Cossette <farchord@gmail.com> - 6.21.0-1
- 6.21.0

* Tue Dec 02 2025 Jan Grulich <jgrulich@redhat.com> - 6.20.0-2
- Rebuild (python-pyside6)

* Thu Nov 13 2025 Steve Cossette <farchord@gmail.com> - 6.20.0-1
- 6.20.0

* Sun Oct 05 2025 Steve Cossette <farchord@gmail.com> - 6.19.0-1
- 6.19.0

* Mon Sep 29 2025 Pavel Solovev <daron439@gmail.com> - 6.18.0-2
- Remove pyside6 from requires

* Tue Sep 16 2025 farchord@gmail.com - 6.18.0-1
- 6.18.0

* Fri Aug 01 2025 Steve Cossette <farchord@gmail.com> - 6.17.0-1
- 6.17.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 05 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.16.0-1
- 6.16.0

* Tue Jun 17 2025 Marie Loise Nolden <loise@kde.org> - 6.15.0-2
- 6.15 and plasma 3.4 compatibility rebuild

* Sat Jun 07 2025 Steve Cossette <farchord@gmail.com> - 6.15.0-1
- 6.15.0

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 6.14.0-2
- Rebuilt for Python 3.14

* Sat May 03 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.14.0-1
- 6.14.0

* Tue Apr 22 2025 Jan Grulich <jgrulich@redhat.com> - 6.13.0-2
- Rebuild (python-pyside6)

* Sun Apr 06 2025 Steve Cossette <farchord@gmail.com> - 6.13.0-1
- 6.13.0

* Thu Mar 13 2025 Marie Loise Nolden <loise@kde.org> - 6.12.0-2
- add pyside6 python bindings build and packaging

* Fri Mar 07 2025 Steve Cossette <farchord@gmail.com> - 6.12.0-1
- 6.12.0

* Fri Feb 07 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.11.0-1
- 6.11.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Steve Cossette <farchord@gmail.com> - 6.10.0-1
- 6.10.0

* Sat Dec 14 2024 Steve Cossette <farchord@gmail.com> - 6.9.0-1
- 6.9.0

* Sat Nov 02 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.8.0-1
- 6.8.0

* Fri Oct 04 2024 Steve Cossette <farchord@gmail.com> - 6.7.0-1
- 6.7.0

* Mon Sep 16 2024 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Sat Aug 10 2024 Steve Cossette <farchord@gmail.com> - 6.5.0-1
- 6.5.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.4.0-1
- 6.4.0

* Sat Jun 01 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.3.0-1
- 6.3.0

* Sat May 04 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Wed Apr 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-1
- 6.1.0

* Sat Mar 09 2024 Marie Loise Nolden <loise@kde.org> - 6.0.0-2
- add missing BuildArch: noarch to -doc package
- convert named -devel BuildRequires to cmake() BuildRequires

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.249.0-1
- 5.249.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.248.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.248.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.248.0-1
- 5.248.0

* Tue Jan 09 2024 Marie Loise Nolden <loise@kde.org> - 5.247.0-2
- add doc package for KF6 API

* Wed Dec 20 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.247.0-1
- 5.247.0

* Sat Dec 02 2023 Justin Zobel <justin.zobel@gmail.com> - 5.246.0-1
- Update to 5.246.0

* Thu Nov 09 2023 Steve Cossette <farchord@gmail.com> - 5.245.0-1
- 5.245.0

* Tue Oct 03 2023 Steve Cossette <farchord@gmail.com> - 5.240.0^20230915.190519.c53eeac-2
- Fixed a spec issue with some files and missing macros

* Wed Sep 27 2023 Steve Cossette <farchord@gmail.com> - 5.240.0^20230915.130519.c53eeac-1
- Initial release
