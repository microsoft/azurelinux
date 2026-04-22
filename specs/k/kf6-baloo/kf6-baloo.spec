# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global framework baloo

Name:    kf6-%{framework}
Summary: A Tier 3 KDE Frameworks 6 module that provides indexing and search functionality
Version: 6.23.0
Release: 2%{?dist}

License: BSD-3-Clause AND CC0-1.0 AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-2.1-or-later AND LGPL-3.0-only AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only) AND bzip2-1.0.6
URL:     https://invent.kde.org/frameworks/%{framework}

Source0: https://download.kde.org/%{stable_kf6}/frameworks/%{majmin_ver_kf6}/%{framework}-%{version}.tar.xz
Source1: https://download.kde.org/%{stable_kf6}/frameworks/%{majmin_ver_kf6}/%{framework}-%{version}.tar.xz.sig

# Upstream Patches
# Missing include for syscall()
# https://invent.kde.org/frameworks/baloo/-/merge_requests/270
Patch0:   270.patch

## upstreamable patches
# http://bugzilla.redhat.com/1235026
Patch100: baloo-5.67.0-baloofile_config.patch

BuildRequires:  extra-cmake-modules >= %{version}
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6FileMetaData)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6IdleTime)
BuildRequires:  cmake(KF6KIO)
BuildRequires:  kf6-rpm-macros
BuildRequires:  cmake(KF6Solid)

BuildRequires:  lmdb-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel

# for systemd-related macros
BuildRequires:  systemd

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       cmake(KF6CoreAddons)
Requires:       cmake(KF6FileMetaData)
Requires:       qt6-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        file
Summary:        File indexing and search for Baloo
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-baloo-file < 6
%description    file
%{summary}.

%package        libs
Summary:        Runtime libraries for %{name}
%description    libs
%{summary}.

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
%cmake_kf6 -DKDE_INSTALL_SYSTEMDUSERUNITDIR=%{_userunitdir}
%cmake_build_kf6

%install
%cmake_install_kf6

# baloodb not installed unless BUILD_EXPERIMENTAL is enabled, so omit translations
#rm -fv %{buildroot}%{_datadir}/locale/*/LC_MESSAGES/baloodb5.*

%find_lang baloodb6
%find_lang baloo_file6
%find_lang baloo_file_extractor6
%find_lang balooctl6
%find_lang balooengine6
%find_lang baloosearch6
%find_lang balooshow6
%find_lang kio6_baloosearch
%find_lang kio6_tags
%find_lang kio6_timeline

cat kio6_tags.lang kio6_baloosearch.lang kio6_timeline.lang \
    balooctl6.lang balooengine6.lang baloosearch6.lang \
    balooshow6.lang baloodb6.lang \
    > %{name}.lang

cat baloo_file6.lang baloo_file_extractor6.lang \
    > %{name}-file.lang

%files -f %{name}.lang
%license LICENSES/*.txt
%{_kf6_bindir}/baloosearch6
%{_kf6_bindir}/balooshow6
%{_kf6_bindir}/balooctl6
%{_kf6_datadir}/qlogging-categories6/%{framework}*

%files file -f %{name}-file.lang
%config(noreplace) %{_kf6_sysconfdir}/xdg/autostart/baloo_file.desktop
%{_userunitdir}/kde-baloo.service
%{_libexecdir}/kf6/baloo_file
%{_libexecdir}/kf6/baloo_file_extractor

%files libs
%license LICENSES/*
%{_kf6_libdir}/libKF6Baloo.so.*
%{_kf6_libdir}/libKF6BalooEngine.so.*
%{_kf6_plugindir}/kio/baloosearch.so
%{_kf6_plugindir}/kio/tags.so
%{_kf6_plugindir}/kio/timeline.so
%{_kf6_plugindir}/kded/baloosearchmodule.so
%{_kf6_qmldir}/org/kde/baloo

%files devel
%{_kf6_libdir}/libKF6Baloo.so
%{_kf6_libdir}/cmake/KF6Baloo/
%{_kf6_libdir}/pkgconfig/KF6Baloo.pc
%{_kf6_includedir}/Baloo/
%{_kf6_datadir}/dbus-1/interfaces/org.kde.baloo.*.xml
%{_kf6_datadir}/dbus-1/interfaces/org.kde.Baloo*.xml
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

* Thu Nov 13 2025 Steve Cossette <farchord@gmail.com> - 6.20.0-1
- 6.20.0

* Sun Oct 05 2025 Steve Cossette <farchord@gmail.com> - 6.19.0-1
- 6.19.0

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

* Sat May 03 2025 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.14.0-1
- 6.14.0

* Sun Apr 06 2025 Steve Cossette <farchord@gmail.com> - 6.13.0-1
- 6.13.0

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

* Mon Sep 30 2024 Alessandro Astone <ales.astone@gmail.com> - 6.6.0-2
- Obsolete any version of kf5-baloo-file

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

* Sat Mar 09 2024 Marie Loise Nolden <loise@kde.org> - 6.0.0-4
- add missing BuildArch: noarch to -doc package

* Mon Feb 26 2024 Steve Cossette <farchord@gmail.com> - 6.0.0-3
- Respin: 6.0.0 (New tarball released by KDE)

* Thu Feb 22 2024 Alessandro Astone <ales.astone@gmail.com> - 6.0.0-2
- Obsolete kf5-baloo-file
- Split translation files in the right subpackage

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

* Tue Nov 21 2023 Alessandro Astone <ales.astone@gmail.com> - 5.245.0-2
- Copy the default configuration from kf5-baloo

* Thu Nov 09 2023 Steve Cossette <farchord@gmail.com> - 5.245.0-1
- 5.245.0

* Sat Sep 23 2023 Steve Cossette <farchord@gmail.com> - 5.240.0^20231011.023811.02a2bd6-1
- Initial release
