Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           amtk
Version:        5.0.2
Release:        3%{?dist}
Summary:        Actions, Menus and Toolbars Kit for GTK+ applications

License:        LGPLv2+
URL:            https://wiki.gnome.org/Projects/Amtk
Source0:        https://download.gnome.org/sources/amtk/5.0/amtk-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)

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


%package        tests
Summary:        Tests for the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.


%prep
%autosetup


%build
%configure --enable-installed-tests
%make_build V=1


%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -delete

%find_lang amtk-5


%files -f amtk-5.lang
%license COPYING
%doc AUTHORS NEWS README
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
%{_datadir}/gtk-doc/html/amtk-5.0/

%files tests
%dir %{_libexecdir}/installed-tests
%{_libexecdir}/installed-tests/amtk-5/
%dir %{_datadir}/installed-tests
%{_datadir}/installed-tests/amtk-5/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.0.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
