# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# first two digits of version
%global release_version %(echo %{version} | awk -F. '{print $1}')

Name:           mingw-gsettings-desktop-schemas
Version:        49.0
Release: 2%{?dist}
Summary:        MinGW Windows gsettings-desktop-schemas

License:        LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/gsettings-desktop-schemas
Source0:        https://download.gnome.org/sources/gsettings-desktop-schemas/%{release_version}/gsettings-desktop-schemas-%{version}.tar.xz

BuildArch:      noarch

BuildRequires:  meson
# For glib-compile-schemas
BuildRequires:  glib2
# For translations
BuildRequires:  gettext

BuildRequires:  mingw32-filesystem
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-glib2

BuildRequires:  mingw64-filesystem
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-glib2

%description
This package contains a collection of GSettings schemas for
settings shared by various components of a desktop.


%package -n mingw32-gsettings-desktop-schemas
Summary:        MinGW Windows gsettings-desktop-schemas

%description -n mingw32-gsettings-desktop-schemas
This package contains a collection of GSettings schemas for
settings shared by various components of a desktop.


%package -n mingw64-gsettings-desktop-schemas
Summary:        MinGW Windows gsettings-desktop-schemas

%description -n mingw64-gsettings-desktop-schemas
This package contains a collection of GSettings schemas for
settings shared by various components of a desktop.


%prep
%autosetup -p1 -n gsettings-desktop-schemas-%{version}


%build
%mingw_meson -Dintrospection=false
%mingw_ninja


%install
%mingw_ninja_install

%mingw_find_lang %{name} --all-name


%files -n mingw32-gsettings-desktop-schemas -f mingw32-%{name}.lang
%license COPYING
%{mingw32_includedir}/*
%{mingw32_datadir}/pkgconfig/*
%dir %{mingw32_datadir}/glib-2.0/
%dir %{mingw32_datadir}/glib-2.0/schemas/
%{mingw32_datadir}/glib-2.0/schemas/*
%dir %{mingw32_datadir}/GConf/
%dir %{mingw32_datadir}/GConf/gsettings/
%{mingw32_datadir}/GConf/gsettings/gsettings-desktop-schemas.convert
%{mingw32_datadir}/GConf/gsettings/wm-schemas.convert

%files -n mingw64-gsettings-desktop-schemas -f mingw64-%{name}.lang
%license COPYING
%{mingw64_includedir}/*
%{mingw64_datadir}/pkgconfig/*
%dir %{mingw64_datadir}/glib-2.0/
%dir %{mingw64_datadir}/glib-2.0/schemas/
%{mingw64_datadir}/glib-2.0/schemas/*
%dir %{mingw64_datadir}/GConf/
%dir %{mingw64_datadir}/GConf/gsettings/
%{mingw64_datadir}/GConf/gsettings/gsettings-desktop-schemas.convert
%{mingw64_datadir}/GConf/gsettings/wm-schemas.convert


%changelog
* Thu Sep 18 2025 Sandro Mani <manisandro@gmail.com> - 49.0-1
- Update to 49.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 48.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Mar 22 2025 Sandro Mani <manisandro@gmail.com> - 48.0-1
- Update to 48.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 47.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 18 2024 Sandro Mani <manisandro@gmail.com> - 47.1-1
- Update to 47.1

* Thu Aug 15 2024 Sandro Mani <manisandro@gmail.com> - 46.1-1
- Update to 46.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 46.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Mar 23 2024 Sandro Mani <manisandro@gmail.com> - 46.0-1
- Update to 46.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 18 2023 Sandro Mani <manisandro@gmail.com> - 45.0-1
- Update to 45.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 44.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 05 2023 Sandro Mani <manisandro@gmail.com> - 44.0-4
- Fix %%{mingw_datadir}/GConf/ ownership

* Sat Apr 22 2023 Sandro Mani <manisandro@gmail.com> - 44.0-3
- BR: gettext

* Fri Apr 21 2023 Sandro Mani <manisandro@gmail.com> - 44.0-2
- Package locale files
- Add dir ownership
- Change %%define to %%global

* Wed Apr 05 2023 Sandro Mani <manisandro@gmail.com> - 44.0-1
- Initial package
