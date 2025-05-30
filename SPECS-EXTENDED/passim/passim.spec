%global glib2_version 2.45.8
%global systemd_version 231
Summary:        Local caching server
Name:           passim
Version:        0.1.8
Release:        3%{?dist}
License:        LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/hughsie/%{name}
Source0:        https://github.com/hughsie/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  glib2-devel
BuildRequires:  gnutls-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libsoup-devel
BuildRequires:  meson
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       glib2%{?_isa} >= %{glib2_version}

%description
Passim is a daemon that allows software to share files on your local network.

%package libs
Summary:        Local caching server library

%description libs
libpassim is a library that allows software to share files on your local network
using the passimd daemon.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install
rm %{buildroot}%{_sharedstatedir}/passim/data/*
%find_lang %{name}

%check
%meson_test

%post
%systemd_post passim.service

%preun
%systemd_preun passim.service

%postun
%systemd_postun_with_restart passim.service

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/passim
%config(noreplace)%{_sysconfdir}/passim.conf
%dir %{_datadir}/passim
%{_datadir}/passim/*.ico
%{_datadir}/passim/*.css
%{_datadir}/dbus-1/system.d/org.freedesktop.Passim.conf
%{_datadir}/dbus-1/interfaces/org.freedesktop.Passim.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Passim.service
%{_datadir}/icons/hicolor/scalable/apps/org.freedesktop.Passim.png
%{_datadir}/metainfo/org.freedesktop.Passim.metainfo.xml
%{_libdir}/girepository-1.0/Passim-1.0.typelib
%{_libexecdir}/passimd
%{_mandir}/man1/passim.1*
%{_unitdir}/passim.service
%{_libdir}/sysusers.d/passim.conf

%files libs
%license LICENSE
%{_libdir}/libpassim.so.1*

%files devel
%{_datadir}/gir-1.0/Passim-1.0.gir
%dir %{_includedir}/passim-1
%{_includedir}/passim-1/passim*.h
%{_libdir}/libpassim*.so
%{_libdir}/pkgconfig/passim.pc

%changelog
* Fri Oct 18 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 0.1.8-3
- Integrating the spec into Azure Linux
- Disabled appstream-util tests due to the large number of undesirable depdendencies
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 29 2024 Richard Hughes <richard@hughsie.com> - 0.1.8-1
- New upstream release

* Wed Apr 17 2024 Richard Hughes <richard@hughsie.com> - 0.1.7-1
- New upstream release

* Mon Apr 15 2024 Richard Hughes <richard@hughsie.com> - 0.1.6-1
- New upstream release

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Richard Hughes <richard@hughsie.com> - 0.1.5-1
- New upstream release

* Fri Oct 27 2023 Richard Hughes <richard@hughsie.com> - 0.1.4-1
- New upstream release

* Mon Oct 09 2023 Richard Hughes <richard@hughsie.com> - 0.1.3-1
- New upstream release

* Mon Sep 25 2023 Richard Hughes <richard@hughsie.com> - 0.1.2-1
- New upstream release

* Sat Sep 09 2023 Richard Hughes <richard@hughsie.com> - 0.1.1-5
- Recommend avahi for the daemon package

* Fri Sep 08 2023 Adam Williamson <awilliam@redhat.com> - 0.1.1-4
- Obsolete versions from before the -libs split

* Fri Aug 25 2023 Richard Hughes <richard@hughsie.com> - 0.1.1-3
- Split out a -libs subpackage

* Fri Aug 25 2023 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.1.1-2
- Misc changes
- Move meson_test to check section
- Reorder BuildRequires alphabetically
- Reorder install files
- Use %%{buildroot} instead of RPM_BUILD_ROOT
- Use %%autorelease for Release tag

* Thu Aug 24 2023 Richard Hughes <richard@hughsie.com> - 0.1.1-1
- New upstream release

* Thu Aug 24 2023 Richard Hughes <richard@hughsie.com> - 0.1.0-1
- Initial release

