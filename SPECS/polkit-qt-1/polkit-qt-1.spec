%global __cmake_in_source_build 1

Name:            polkit-qt-1
Version:         0.114.0
Release:         5%{?dist}
Summary:         Qt bindings for PolicyKit
# Licenses retrieved from source files with:
# grep -hR -oP "(?<=SPDX-License-Identifier: ).*" <source_dir>/* | sort | uniq
# and:
# ls -la <source_dir>/LICENSES/
License:         BSD-3-Clause AND GPL-2.0-or-later AND LGPL-2.0-or-later
URL:             https://api.kde.org/kdesupport-api/polkit-qt-1-apidocs/
Source0:         https://download.kde.org/stable/%{name}/%{name}-%{version}.tar.xz
Vendor:          Microsoft Corporation
Distribution:    Mariner

BuildRequires:   cmake
BuildRequires:   gcc-c++
BuildRequires:   pkgconfig(polkit-agent-1) pkgconfig(polkit-gobject-1)
BuildRequires:   pkgconfig(Qt5DBus) pkgconfig(Qt5Gui) pkgconfig(Qt5Widgets)

%description
Polkit-qt is a library that lets developers use the PolicyKit API
through a nice Qt-styled API.

%package -n polkit-qt5-1
Summary: PolicyKit Qt5 bindings
Provides:  polkit-qt5 = %{version}-%{release}
%description -n polkit-qt5-1
Polkit-qt is a library that lets developers use the PolicyKit API
through a nice Qt-styled API.

%package -n polkit-qt5-1-devel
Summary: Development files for PolicyKit Qt5 bindings
Provides:  polkit-qt5-devel = %{version}-%{release}
Requires: polkit-qt5-1%{?_isa} = %{version}-%{release}
%description -n polkit-qt5-1-devel
%{summary}.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%cmake \
  -DBUILD_EXAMPLES:BOOL=OFF

%cmake_build

%install
%cmake_install

%ldconfig_scriptlets -n polkit-qt5-1

%files -n polkit-qt5-1
%doc AUTHORS README
%license LICENSES/*
%{_libdir}/libpolkit-qt5-core-1.so.1*
%{_libdir}/libpolkit-qt5-gui-1.so.1*
%{_libdir}/libpolkit-qt5-agent-1.so.1*

%files -n polkit-qt5-1-devel
%{_includedir}/polkit-qt5-1/
%{_libdir}/libpolkit-qt5-core-1.so
%{_libdir}/libpolkit-qt5-gui-1.so
%{_libdir}/libpolkit-qt5-agent-1.so
%{_libdir}/pkgconfig/polkit-qt5-1.pc
%{_libdir}/pkgconfig/polkit-qt5-core-1.pc
%{_libdir}/pkgconfig/polkit-qt5-gui-1.pc
%{_libdir}/pkgconfig/polkit-qt5-agent-1.pc
%{_libdir}/cmake/PolkitQt5-1/

%changelog
* Tue May 23 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.114.0-5
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.

%changelog
* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.114.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.114.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.114.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.114.0-1
- polkit-qt-1-0.114.0
- .spec cleanup

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.113.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 21 2020 Troy Dawson <tdawson@redhat.com> - 0.113.0-5
- Fix FTBFS - cmake issues (#1863703)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.113.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.113.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.113.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.113.0-1
- new qt5-only polkit-qt-1 package, let polkit-qt remain for qt4 legacy
