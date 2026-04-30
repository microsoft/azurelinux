## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 9;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           kdsoap
Version:        2.2.0
Release:        %autorelease
Summary:        A Qt-based client-side and server-side SOAP component

# Note that this project requires the 3rd party 'libkode' submodule
# that is licensed separately with LGPL-2.0-or-later; however, libkode
# is used for code-generation only and the resulting code can be made
# available under any license.
# 
# Various other freely distributable files are contained in the unittests
# and are not used in the library code itself.
License:        MIT
URL:            https://github.com/KDAB/KDSoap
Source0:        https://github.com/KDAB/KDSoap/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/KDAB/KDSoap/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz.asc
Source2:        https://www.kdab.com/kdab-products.asc

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  qt6-rpm-macros
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  gnupg2
# for doc generation
BuildRequires:  doxygen
BuildRequires:  cmake(Qt6ToolsTools)
BuildRequires:  qt6-doc-devel

%global _description %{expand:
KDSoap can be used to create client applications for web services
and also provides the means to create web services without the need
for any further component such as a dedicated web server.}

%description %{_description}

For more information, see
https://www.kdab.com/development-resources/qt-tools/kd-soap/

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel-common%{?_isa} = %{version}-%{release}
%description    devel
This package contains header files and associated tools and libraries to
develop programs which need to access web services using the SOAP protocol.

%package     -n kdsoap6
Summary:        Qt 6 version of %{name}
%description -n kdsoap6
%{_description}

%package     -n kdsoap6-devel
Summary:        Development files for kdsoap6
Requires:       kdsoap6%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel-common%{?_isa} = %{version}-%{release}
%description -n kdsoap6-devel
This package contains header files and associated tools and libraries to
develop programs which need to access web services using the SOAP protocol.

%package        devel-common
Summary:        Header files and other common development files for kdsoap and kdsoap6
%description    devel-common
%{summary}.

%package        doc
Summary:        Developer Documentation files for %{name}
BuildArch:      noarch

%description    doc
Developer Documentation files for %{name} for use with KDevelop or QtCreator.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup

%build
%global _vpath_builddir %{_target_platform}-qt5
%cmake -DKDSoap_EXAMPLES=false -DKDSoap_QT6=OFF
%cmake_build

%global _vpath_builddir %{_target_platform}-qt6
# qhelpgenerator needs to be in $PATH to be detected
export PATH=%{_qt6_libexecdir}:$PATH
%cmake -DKDSoap_EXAMPLES=false -DKDSoap_QT6=ON -DKDSoap_DOCS=ON
%cmake_build

%install
%global _vpath_builddir %{_target_platform}-qt5
%cmake_install

%global _vpath_builddir %{_target_platform}-qt6
%cmake_install
mkdir -p %{buildroot}%{_qt6_docdir}
mv %{buildroot}%{_docdir}/KDSoap-qt6/*.qch %{buildroot}%{_qt6_docdir}/
mv %{buildroot}%{_docdir}/KDSoap-qt6/*.tags %{buildroot}%{_qt6_docdir}/
rm -rf %{buildroot}%{_datarootdir}/doc/KDSoap{,-qt6}

%check
%global _vpath_builddir %{_target_platform}-qt5
%ctest
%global _vpath_builddir %{_target_platform}-qt6
%ctest


%files
%doc README.md
%license LICENSES/MIT.txt
%{_libdir}/libkdsoap-server.so.2*
%{_libdir}/libkdsoap.so.2*

%files -n kdsoap6
%doc README.md
%license LICENSES/MIT.txt
%{_libdir}/libkdsoap-server-qt6.so.2*
%{_libdir}/libkdsoap-qt6.so.2*

%files devel
%doc kdsoap.pri kdwsdl2cpp.pri
%{_libdir}/libkdsoap-server.so
%{_libdir}/libkdsoap.so
%{_bindir}/kdwsdl2cpp
%{_libdir}/cmake/KDSoap/
%{_libdir}/qt5/mkspecs/modules/*
%{_includedir}/KDSoapClient/
%{_includedir}/KDSoapServer/

%files -n kdsoap6-devel
%doc kdsoap.pri kdwsdl2cpp.pri
%{_libdir}/libkdsoap-server-qt6.so
%{_libdir}/libkdsoap-qt6.so
%{_bindir}/kdwsdl2cpp-qt6
%{_libdir}/cmake/KDSoap-qt6/
%{_libdir}/qt6/mkspecs/modules/*
%{_includedir}/KDSoapClient-Qt6/
%{_includedir}/KDSoapServer-Qt6/
%{_qt6_docdir}/kdsoap.tags

%files devel-common
%dir %{_datadir}/mkspecs
%dir %{_datadir}/mkspecs/features
%{_datadir}/mkspecs/features/kdsoap.prf


%files doc
%doc docs/CHANGES* docs/manual
%{_qt6_docdir}/kdsoap-api.qch

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.2.0-9
- test: add initial lock files

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Mar 10 2024 Marie Loise Nolden <loise@kde.org> - 2.2.0-5
- add doc package with QCH API Docs

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Alessandro Astone <ales.astone@gmail.com> - 2.2.0-2
- Move qt5 headers to the right package

* Mon Jan 15 2024 Steve Cossette <farchord@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Mon Nov 27 2023 Alessandro Astone <ales.astone@gmail.com> - 2.1.1-10
- Split devel-common subpackage

* Fri Nov 24 2023 Alessandro Astone <ales.astone@gmail.com> - 2.1.1-9
- Add Qt6 build

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Feb 17 2023 Casper Meijn <casper@meijn.net> - 2.1.1-7
- Check GPG signature on source file

* Thu Feb 16 2023 Casper Meijn <casper@meijn.net> - 2.1.1-4
- Update description to be in line with upstream

* Wed Feb 15 2023 Casper Meijn <casper@meijn.net> - 2.1.1-1
- Update to KDSoap 2.1.1 (rhbz#2126596)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Casper Meijn <casper@meijn.net> - 2.0.0-1
- Update to KDSoap 2.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 29 2020 Casper Meijn <casper@meijn.net> - 1.10.0-1
- Update to KDSoap 1.10.0

* Sat Nov 14 2020 Marie Loise Nolden <loise@kde.org> - 1.9.1-1
- Update to 1.9.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Feb 20 2020 Casper Meijn <casper@meijn.net> - 1.9.0-6
- Update to KDSoap 1.9.0
- Disable building examples
- Remove RPath patch

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 18 2019 Casper Meijn <casper@meijn.net> - 1.8.0-3
- Update to KDSoap 1.8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Casper Meijn <casper@meijn.net> - 1.7.0-1
- First kdsoap package

## END: Generated by rpmautospec
