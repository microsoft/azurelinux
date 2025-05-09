Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global glib2_version 2.44
%global gtk3_version 3.20

Name:           gspell
Version:        1.14.0
Release:        1%{?dist}
Summary:        Spell-checking library for GTK+

License:        LGPLv2.1+
URL:            https://gitlab.gnome.org/GNOME/gspell
Source0:        https://gitlab.gnome.org/GNOME/gspell/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gettext
BuildRequires:  gobject-introspection-devel
BuildRequires:  meson
BuildRequires:  pkgconfig(enchant-2)
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  vala

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
find $RPM_BUILD_ROOT -name '*.la' -delete

%find_lang gspell-1


%ldconfig_scriptlets


%files -f gspell-1.lang
%license LICENSES/*
%{_libdir}/girepository-1.0/
%{_libdir}/libgspell-1.so.3*

%files devel
%{_bindir}/gspell-app1
%{_includedir}/gspell-1/
%{_libdir}/libgspell-1.so
%{_libdir}/pkgconfig/gspell-1.pc
%{_datadir}/gir-1.0/
%{_datadir}/vala/
%exclude %dir %{_datadir}/installed-tests/%{name}-1/
%exclude %{_datadir}/installed-tests/%{name}-1/*
%exclude %dir %{_libexecdir}/installed-tests/%{name}-1/
%exclude %{_libexecdir}/installed-tests/%{name}-1/*

%files doc
%{_datadir}/gtk-doc/


%changelog
* Tue Oct 15 2024 Kevin Lockwood <v-klockwood@microsoft.com> - 1.14.0-1
- Upgrade to latest upstream
- Change to meson build system
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.8.4-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

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
