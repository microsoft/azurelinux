# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           kdsoap-ws-discovery-client
Version:        0.4.0
Release:        5%{?dist}
Summary:        Library for finding WS-Discovery devices in the network using Qt6 and KDSoap

License:        GPL-3.0-or-later AND LicenseRef-OASIS AND LicenseRef-WS-Addressing AND LicenseRef-Discovery AND W3C
URL:            https://invent.kde.org/libraries/kdsoap-ws-discovery-client/
Source0:        https://download.kde.org/stable/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  extra-cmake-modules
BuildRequires:  cmake(KDSoap-qt6)
BuildRequires:  cmake(Qt6)

%description
%{summary}.


%package        devel
Summary:        Development libraries and header files for Qt6 %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake(KDSoap-qt6)
%description    devel
%{summary}.

%package        doc
Summary:        Developer Documentation files for %{name}
BuildArch:      noarch

%description    doc
Developer Documentation files for %{name} for use with KDevelop or QtCreator.

%prep
%autosetup -p1

%build
%cmake_kf6 -DBUILD_WITH_QT6=ON
%cmake_build

%install
%cmake_install

%check
# Tests fail without internet
%ctest || :

%files
%doc README.md
%license LICENSES/*
%{_libdir}/libKDSoapWSDiscoveryClient.so.0{,.*}

%files devel
%{_includedir}/KDSoapWSDiscoveryClient/
%{_libdir}/cmake/KDSoapWSDiscoveryClient/
%{_libdir}/libKDSoapWSDiscoveryClient.so
%{_qt6_docdir}/*.tags

%files doc
%{_docdir}/KDSoapWSDiscoveryClient/
%{_qt6_docdir}/*.qch

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 10 2024 Marie Loise Nolden <loise@kde.org> - 0.4.0-2
- add missing BuildArch: noarch to -doc package

* Wed Feb 21 2024 Alessandro Astone <ales.astone@gmail.com> - 0.4.0-1
- 0.4.0

* Mon Jan 29 2024 Alessandro Astone <ales.astone@gmail.com> - 0.3.0-4
- Add developer documentation in the doc subpackage

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 14 2023 Alessandro Astone <ales.astone@gmail.com> - 0.3.0-1
- Initial Release
