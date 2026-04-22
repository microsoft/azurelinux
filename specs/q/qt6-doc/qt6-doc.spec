# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:    qt6-doc
Summary: Qt6 - Complete documentation
Version: 6.9.1
Release: 4%{?dist}
BuildArch: noarch

License: GFDL
# The tarball for this docs are self generated through provided script on SOURCES generate-qt-doc.sh
Url:     http://qt-project.org/
Source0: qt-doc-opensource-src-%{version}.tar.xz
Source1: generate-qt6-doc.sh
Source2: qtbase-tell-the-truth-about-private-API.patch

# optimize build, skip unecessary steps
%global debug_package   %{nil}
%global __spec_install_post %{nil}

BuildRequires: qt6-rpm-macros

%description
Documentation for Qt6 API in QCH format
%{summary}.

%package html
Summary: Qt API Documentation in HTML format

%description html
%{summary}.


%package devel
Summary: tags files for crosslinking to Qt QCH files

%description devel
%{summary}.


%prep
# intentionally left blank
# though could be used to initially unpack (rex)


%build
# intentionally left blank


%install
mkdir -p %{buildroot}
tar xf %{SOURCE0} -C %{buildroot}

%files
%{_qt6_docdir}/*.qch

%files html
%{_qt6_docdir}/*/*
%exclude %{_qt6_docdir}/*/*.tags
%exclude %{_qt6_docdir}/*/*.index

%files devel
%{_qt6_docdir}/*/*.tags
%{_qt6_docdir}/*/*.index

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 10 2025 Marie Loise Nolden <loise@kde.org> - 6.9.1-2
- add *.index files to devel

* Sun Jun 08 2025 Marie Loise Nolden <loise@kde.org> - 6.9.1-1
- 6.9.1

* Wed Apr 16 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 6.9.0-2
- Rebuilt

* Tue Apr 15 2025 Marie Loise Nolden <loise@kde.org> - 6.9.0-1
- 6.9.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 30 2024 Marie Loise Nolden <loise@kde.org> - 6.8.1-1
- 6.8.1  

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 26 2024 LuK1337 <priv.luk@gmail.com> - 6.7.0-2
- Regenerate sources

* Tue Apr 02 2024 Marie Loise Nolden <loise@kde.org> - 6.7.0-1
- update to 6.7.0

* Sat Feb 17 2024 Marie Loise Nolden <loise@kde.org> - 6.6.2-1
- update to 6.6.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Marie Loise Nolden <loise@kde.org> - 6.6.1-1
- Initial import based on qt5-doc. Simplify and split into qt6-doc,
  qt6-doc-devel (QCH) and qt6-doc-html (only HTML files)
