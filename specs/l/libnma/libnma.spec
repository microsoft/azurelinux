# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/libnma.azl.macros}

%global gtk3_version          %(pkg-config --modversion gtk+-3.0 2>/dev/null || echo bad)
%global gtk4_version          %(pkg-config --modversion gtk4 2>/dev/null || echo bad)
%global glib2_version         %(pkg-config --modversion glib-2.0 2>/dev/null || echo bad)
%global nm_version            1:1.8.0
%global mbp_version           0.20090602
%global old_libnma_version    1.10.4

%if 0%{?fedora} >= 34 || 0%{?rhel} >= 10
%bcond_without libnma_gtk4
%else
%bcond_with libnma_gtk4
%endif

Name:           libnma
Summary:        NetworkManager GUI library
Version:        1.10.6
Release: 11%{?dist}
# The entire source code is GPLv2+ except some files in shared/ which are LGPLv2+
License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/libnma/
Source0:        https://download.gnome.org/sources/libnma/1.10/%{name}-%{version}.tar.xz
Source9999: libnma.azl.macros

Patch1:         0001-nm-applet-no-notifications.patch

Requires:       mobile-broadband-provider-info >= %{mbp_version}

Conflicts:      libnma < %{old_libnma_version}
Conflicts:      nm-connection-editor < 1.30.0

BuildRequires:  gcc
BuildRequires:  NetworkManager-libnm-devel >= %{nm_version}
BuildRequires:  ModemManager-glib-devel >= 1.0
BuildRequires:  glib2-devel >= 2.38
BuildRequires:  gtk3-devel >= 3.12
%if %{with libnma_gtk4}
BuildRequires:  gtk4-devel >= 4.0
%endif
BuildRequires:  gobject-introspection-devel >= 0.10.3
BuildRequires:  gettext-devel
BuildRequires:  pkgconfig
BuildRequires:  meson
BuildRequires:  gtk-doc
BuildRequires:  iso-codes-devel
BuildRequires:  gcr-devel
BuildRequires:  mobile-broadband-provider-info-devel >= %{mbp_version}

%description
This package contains the library used for integrating GUI tools with
NetworkManager.


%package devel
Summary:        Header files for NetworkManager GUI library
Requires:       NetworkManager-libnm-devel >= %{nm_version}
Obsoletes:      NetworkManager-gtk-devel < 1:0.9.7
Requires:       libnma%{?_isa} = %{version}-%{release}
Requires:       gtk3-devel%{?_isa}
Requires:       pkgconfig
Conflicts:      libnma < %{old_libnma_version}

%description devel
This package contains header and pkg-config files to be used for integrating
GUI tools with NetworkManager.


%package gtk4
Summary:        Experimental GTK 4 version of NetworkManager GUI library
Requires:       gtk4%{?_isa} >= %{gtk4_version}
Requires:       mobile-broadband-provider-info >= %{mbp_version}
Conflicts:      libnma < %{old_libnma_version}

%description gtk4
This package contains the experimental GTK4 version of library used for
integrating GUI tools with NetworkManager.


%package gtk4-devel
Summary:        Header files for experimental GTK4 version of NetworkManager GUI library
Requires:       NetworkManager-libnm-devel >= %{nm_version}
Requires:       libnma-gtk4%{?_isa} = %{version}-%{release}
Requires:       gtk4-devel%{?_isa}
Requires:       pkgconfig
Conflicts:      libnma < %{old_libnma_version}

%description gtk4-devel
This package contains the experimental GTK4 version of header and pkg-config
files to be used for integrating GUI tools with NetworkManager.


%prep
%autosetup -p1


%build
%meson \
        -Dgcr=true \
        -Dvapi=false \
%if %{with libnma_gtk4}
        -Dlibnma_gtk4=true \
%else
        -Dlibnma_gtk4=false \
%endif
%meson_build


%install
%meson_install
%find_lang %{name}


%check
%meson_test


%files -f %{name}.lang
%{_libdir}/libnma.so.*
%{_libdir}/girepository-1.0/NMA-1.0.typelib
%exclude %{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.nm-applet.eap.gschema.xml
%doc NEWS CONTRIBUTING
%license COPYING


%files devel
%{_includedir}/libnma
%{_libdir}/pkgconfig/libnma.pc
%{_libdir}/libnma.so
%{_datadir}/gir-1.0/NMA-1.0.gir
%{_datadir}/gtk-doc


%if %{with libnma_gtk4}
%files gtk4
%{_libdir}/libnma-gtk4.so.*
%{_libdir}/girepository-1.0/NMA4-1.0.typelib
%license COPYING


%files gtk4-devel
%{_includedir}/libnma
%{_libdir}/pkgconfig/libnma-gtk4.pc
%{_libdir}/libnma-gtk4.so
%{_datadir}/gir-1.0/NMA4-1.0.gir
%endif


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 30 2023 Thomas Haller <thaller@redhat.com> - 1.10.6-5
- Use SPDX license identifier in package

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 19 2023 Kalev Lember <klember@redhat.com> - 1.10.6-3
- Rebuilt for gcr soname bump

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 08 2023 Lubomir Rintel <lkundrak@v3.sk> - 1.10.6-1
- Update to 1.10.6 release

* Mon Nov 07 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.10.4-1
- Update to 1.10.4 release

* Fri Sep 09 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.10.2-1
- Update to 1.10.2 release

* Thu Sep 08 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.10.0-1
- Update to 1.10.0 release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.8.40-1
- Update to 1.8.40 release

* Thu Apr 07 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.8.38-1
- Update to 1.8.38 release

* Fri Mar 18 2022 Adam Williamson <awilliam@redhat.com> - 1.8.34-2
- Backport MR #26 to fix UI files in GTK4 (#2060868)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.34-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Lubomir Rintel <lkundrak@v3.sk> - 1.8.34-1
- Update to 1.8.34 release
- Enable gtk4 subpackage

* Fri Aug 20 2021 Thomas Haller <thaller@redhat.com> - 1.8.32-1
- Update to 1.8.32 release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.30-1.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.30-1.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.30-1.2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.30-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  9 2020 Jérôme Parmentier <jerome@prmntr.me> - 1.8.30-1
- Update to 1.8.30 release

* Fri Mar  6 2020 Thomas Haller <thaller@redhat.com> - 1.8.28-1
- Update to 1.8.28 release
- move org.gnome.nm-applet.gschema.xml from network-manager-applet to here.
- introduce wireless security dialogs

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.26-3
- Clarify licensing
- Add a missing mobile-broadband-provider-info provide

* Fri Nov 08 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.26-2
- Fixes suggested in review by Matthew Krupcale (#1763285):
- Add gcc BR
- Fixed the libnma-gtk4 conditional
- Made dependencies arch-specific where relevant
- Dropped obsolete macros
- Install license file with libnma-gtk4

* Fri Oct 18 2019 Lubomir Rintel <lkundrak@v3.sk> - 1.8.26-1
- Initial package split from nm-connection-editor
