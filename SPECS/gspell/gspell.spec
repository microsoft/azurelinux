# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global glib2_version 2.44
%global gtk3_version 3.20

Name:           gspell
Version:        1.14.2
Release:        1%{?dist}
Summary:        Spell-checking library for GTK+

License:        LGPL-2.1-or-later
URL:            https://wiki.gnome.org/Projects/gspell
Source0:        https://download.gnome.org/sources/%{name}/1.14/%{name}-%{version}.tar.xz

BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  meson
BuildRequires:  vala
BuildRequires:  pkgconfig(enchant-2)
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(iso-codes)

Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       gtk3%{?_isa} >= %{gtk3_version}
Requires:       iso-codes

%description
gspell provides a flexible API to implement the spell checking
in a GTK+ application.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tests
Summary:        Installed tests for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.


%package        doc
Summary:        API documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q


%build
%meson
%meson_build


%install
%meson_install

%find_lang gspell-1


%ldconfig_scriptlets


%files -f gspell-1.lang
%license LICENSES/LGPL-2.1-or-later.txt
%doc NEWS README.md
%{_libdir}/girepository-1.0/
%{_libdir}/libgspell-1.so.3*

%files devel
%{_bindir}/gspell-app1
%{_includedir}/gspell-1/
%{_libdir}/libgspell-1.so
%{_libdir}/pkgconfig/gspell-1.pc
%{_datadir}/gir-1.0/
%{_datadir}/vala/

%files doc
%{_datadir}/gtk-doc/

%files tests
%{_libexecdir}/installed-tests/
%{_datadir}/installed-tests/


%changelog
* Wed Dec 10 2025 Adrian Vovk <adrianvovk@gmail.com> - 1.14.2-1
- Update to 1.14.2

* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 1.14.0-5
- Rebuilt for icu 77.1

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 1.14.0-2
- Rebuild for ICU 76

* Mon Sep 16 2024 nmontero <nmontero@redhat.com> - 1.14.0-1
- Update to 1.14.0

* Thu Aug 29 2024 David King <amigadave@amigadave.com> - 1.13.2-1
- Update to 1.13.2

* Sat Aug 17 2024 David King <amigadave@amigadave.com> - 1.13.1-1
- Update to 1.13.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 1.12.2-4
- Rebuild for ICU 74

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jul 31 2023 Kalev Lember <klember@redhat.com> - 1.12.2-1
- Update to 1.12.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 1.12.1-2
- Rebuilt for ICU 73.2

* Tue May 02 2023 David King <amigadave@amigadave.com> - 1.12.1-1
- Update to 1.12.1

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 1.12.0-2
- Rebuild for ICU 72

* Fri Sep 30 2022 Kalev Lember <klember@redhat.com> - 1.12.0-1
- Update to 1.12.0

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 1.11.1-3
- Rebuilt for ICU 71.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Kalev Lember <klember@redhat.com> - 1.11.1-1
- Update to 1.11.1

* Tue Apr 19 2022 David King <amigadave@amigadave.com> - 1.10.0-1
- Update to 1.10.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 1.9.1-2
- Rebuild for ICU 69

* Thu Feb 18 2021 Kalev Lember <klember@redhat.com> - 1.9.1-1
- Update to 1.9.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 04 2020 Kalev Lember <klember@redhat.com> - 1.8.4-1
- Update to 1.8.4

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Kalev Lember <klember@redhat.com> - 1.8.3-1
- Update to 1.8.3

* Fri Sep 06 2019 Kalev Lember <klember@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Kalev Lember <klember@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 1.6.1-1
- Update to 1.6.1

* Sun Sep 10 2017 Kalev Lember <klember@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Mon Aug 28 2017 Kalev Lember <klember@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 1.5.3-1
- Update to 1.5.3

* Mon Jun 12 2017 Kalev Lember <klember@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 1.4.1-1
- Update to 1.4.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Mon Feb 27 2017 Richard Hughes <rhughes@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 1.3.2-1
- Update to 1.3.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 16 2016 Kalev Lember <klember@redhat.com> - 1.2.2-1
- Update to 1.2.2

* Wed Nov 23 2016 Kalev Lember <klember@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Thu Sep 22 2016 Kalev Lember <klember@redhat.com> - 1.2.0-2
- BR vala instead of obsolete vala-tools subpackage

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Sun Aug 14 2016 Kalev Lember <klember@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Sun Jul 17 2016 Kalev Lember <klember@redhat.com> - 1.1.2-1
- Update to 1.1.2

* Sun Jul 10 2016 Kalev Lember <klember@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Fri Jun 10 2016 Kalev Lember <klember@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Sun Mar 20 2016 Kalev Lember <klember@redhat.com> - 1.0.0-1
- Update to 1.0.0

* Mon Mar 14 2016 Kalev Lember <klember@redhat.com> - 0.2.6-1
- Update to 0.2.6

* Tue Feb 16 2016 David King <amigadave@amigadave.com> - 0.2.4-1
- Update to 0.2.4

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 0.2.3-1
- Update to 0.2.3

* Mon Dec 14 2015 Kalev Lember <klember@redhat.com> - 0.2.2-1
- Update to 0.2.2
- This update relicensed gspell from GPLv2+ to LGPLv2+

* Mon Dec 07 2015 Kalev Lember <klember@redhat.com> - 0.2.1-1
- Update to 0.2.1

* Sun Dec 06 2015 Kalev Lember <klember@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 0.1.0-1
- Initial Fedora packaging (#1271944)
