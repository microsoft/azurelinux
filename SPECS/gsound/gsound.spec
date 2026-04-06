# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           gsound
Version:        1.0.3
Release:        11%{?dist}
Summary:        Small gobject library for playing system sounds

License:        LGPL-2.1-or-later
URL:            https://wiki.gnome.org/Projects/GSound
Source0:        http://download.gnome.org/sources/gsound/1.0/gsound-%{version}.tar.xz

BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  vala
BuildRequires:  gtk-doc
BuildRequires:  meson


%description
GSound is a small library for playing system sounds. 
It's designed to be used via GObject Introspection, 
and is a thin wrapper around the libcanberra C library


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%meson -Dgtk_doc=true
%meson_build


%install
%meson_install


%ldconfig_scriptlets


%files
%doc COPYING README README.md
%{_bindir}/gsound-play
%{_libdir}/*.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/GSound-1.0.typelib
%{_mandir}/man1/gsound-play.*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gsound.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/GSound-1.0.gir
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/gsound-%{version}
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/gsound.*



%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 19 2021 Yanko Kaneti <yaneti@declera.com> - 1.0.3-2
- Move the gsound-play manpage to the main package

* Wed Aug 18 2021 Yanko Kaneti <yaneti@declera.com> - 1.0.3-1
- Update to 1.0.3. Switch to meson.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 1.0.2-9
- Update BRs for vala packaging changes

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov  1 2015 Yanko Kaneti <yaneti@declera.com> - 1.0.2-1
- Update to 1.0.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec  1 2014 Yanko Kaneti <yaneti@declera.com> - 1.0.1-1
- Update to 1.0.1

* Sun Nov 30 2014 Yanko Kaneti <yaneti@declera.com> - 1.0.0-2
- Initial spec for review - 0.98.0-0.1.a648648
- Additional patch + references + using %%autopatch - 0.98.0-0.2.a648648
- Update to 1.0.0. drop upstreamed paches - 1.0.0-1
- Own some more directories as per review (#1167482) - 1.0.0-2
