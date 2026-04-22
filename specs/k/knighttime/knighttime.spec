# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           knighttime
Summary:        Helpers for scheduling the dark-light cycle
Version:        6.6.0
Release: 2%{?dist}

License:        GPL-3.0-only AND BSD-3-Clause AND MIT AND GPL-2.0-only AND LGPL-2.1-only AND CC0-1.0 AND LGPL-3.0-only
URL:            https://invent.kde.org/plasma/%{name}

Source0:        https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{name}-%{version}.tar.xz
Source1:        https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{name}-%{version}.tar.xz.sig

# Upstream Patches

BuildRequires:  extra-cmake-modules >= %{version}
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  kf6-rpm-macros
BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils

BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Positioning)

BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6Holidays)
BuildRequires:  cmake(KF6I18n)

%description
%{summary}.

%package devel
Summary:        Developer files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
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
%autosetup -p1

%build
%cmake_kf6
%cmake_build_kf6

%install
%cmake_install_kf6
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.knighttimed.desktop

%post
%systemd_user_post plasma-knighttimed.service

%preun
%systemd_user_preun plasma-knighttimed.service

%postun
%systemd_user_postun_with_restart plasma-knighttimed.service
%systemd_user_postun_with_reload plasma-knighttimed.service
%systemd_user_postun plasma-knighttimed.service

%files
%license LICENSES/*.txt
%{_userunitdir}/plasma-knighttimed.service
%{_kf6_libdir}/libKNightTime.so.0
%{_kf6_libdir}/libKNightTime.so.%{version}
%{_libexecdir}/knighttimed
%{_datadir}/applications/org.kde.knighttimed.desktop
%{_datadir}/dbus-1/interfaces/org.kde.NightTime.xml
%{_datadir}/dbus-1/services/org.kde.NightTime.service
%{_datadir}/qlogging-categories6/knighttime.categories

%files devel
%{_includedir}/KNightTime/
%{_kf6_libdir}/cmake/KNightTime/
%{_kf6_libdir}/libKNightTime.so

%files doc
%{_qt6_docdir}/*.qch

%files html
%{_qt6_docdir}/*/*
%exclude %{_qt6_docdir}/*/*.tags
%exclude %{_qt6_docdir}/*/*.index

%changelog
* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 6.6.0-1
- 6.6.0

* Tue Jan 27 2026 Steve Cossette <farchord@gmail.com> - 6.5.91-1
- 6.5.91

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 farchord@gmail.com - 6.5.90-1
- 6.5.90

* Tue Jan 13 2026 farchord@gmail.com - 6.5.5-1
- 6.5.5

* Tue Dec 09 2025 Steve Cossette <farchord@gmail.com> - 6.5.4-1
- 6.5.4

* Tue Nov 18 2025 Steve Cossette <farchord@gmail.com> - 6.5.3-1
- 6.5.3

* Tue Nov 04 2025 Steve Cossette <farchord@gmail.com> - 6.5.2-1
- 6.5.2

* Tue Oct 28 2025 Steve Cossette <farchord@gmail.com> - 6.5.1-1
- 6.5.1

* Fri Oct 17 2025 Steve Cossette <farchord@gmail.com> - 6.5.0-1
- 6.5.0

* Fri Oct 03 2025 Steve Cossette <farchord@gmail.com> - 6.4.91-1
- 6.4.91

* Fri Sep 26 2025 Steve Cossette <farchord@gmail.com> - 6.4.90-1
- Initial Release
