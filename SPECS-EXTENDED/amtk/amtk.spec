Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           amtk
Version:        5.6.1
Release:        8%{?dist}
Summary:        Actions, Menus and Toolbars Kit for GTK+ applications

License:        LGPL-3.0-or-later
URL:            https://wiki.gnome.org/Projects/Amtk
Source0:        https://download.gnome.org/sources/amtk/5.6/amtk-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)

# Removed in F34
Obsoletes: amtk-tests < 5.3.1

%description
Amtk is the acronym for “Actions, Menus and Toolbars Kit”. It is a basic
GtkUIManager replacement based on GAction. It is suitable for both a
traditional UI or a modern UI with a GtkHeaderBar.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%meson -Dgtk_doc=true
%meson_build


%install
%meson_install

%find_lang amtk-5


%files -f amtk-5.lang
%license LICENSES/LGPL-3.0-or-later.txt
%doc NEWS README.md
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Amtk-5.typelib
%{_libdir}/libamtk-5.so.0*

%files devel
%{_includedir}/amtk-5/
%{_libdir}/libamtk-5.so
%{_libdir}/pkgconfig/amtk-5.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Amtk-5.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/amtk-5/


%changelog
* Fri Mar 14 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 5.6.1-8
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Kalev Lember <klember@redhat.com> - 5.6.1-1
- Update to 5.6.1
- Switch to SPDX license tags

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 18 2021 Kalev Lember <klember@redhat.com> - 5.3.1-1
- Update to 5.3.1
- Switch to meson build system
- Remove -tests sub package as the installed tests are gone upstream

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 10 2020 Kalev Lember <klember@redhat.com> - 5.2.0-1
- Update to 5.2.0

* Fri Sep 04 2020 Kalev Lember <klember@redhat.com> - 5.1.2-1
- Update to 5.1.2

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 29 2020 Kalev Lember <klember@redhat.com> - 5.1.1-1
- Update to 5.1.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Kalev Lember <klember@redhat.com> - 5.0.2-1
- Update to 5.0.2

* Fri Sep 06 2019 Kalev Lember <klember@redhat.com> - 5.0.1-1
- Update to 5.0.1

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 5.0.0-2
- Rebuilt against fixed atk (#1626575)

* Fri Sep 07 2018 Pete Walter <pwalter@fedoraproject.org> - 5.0.0-1
- Initial Fedora package
