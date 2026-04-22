# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global with_mingw 0

%if 0%{?fedora}
%global with_mingw 1
%endif

Name:           gcab
Version:        1.6
Release: 10%{?dist}
Summary:        Cabinet file library and tool

# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:        LicenseRef-Callaway-LGPLv2+
#VCS:           git:git://git.gnome.org/gcab
URL:            http://ftp.gnome.org/pub/GNOME/sources/gcab
Source0:        http://ftp.gnome.org/pub/GNOME/sources/gcab/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  git-core
BuildRequires:  gettext
BuildRequires:  gtk-doc
BuildRequires:  vala
BuildRequires:  glib2-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  zlib-devel
BuildRequires:  meson
BuildRequires:  git

Requires:       libgcab1%{?_isa} = %{version}-%{release}

%if %{with_mingw}
BuildRequires: mingw32-filesystem >= 95
BuildRequires: mingw32-gcc
BuildRequires: mingw64-filesystem >= 95
BuildRequires: mingw64-gcc
BuildRequires: mingw64-glib2
BuildRequires: mingw32-glib2
BuildRequires: mingw64-zlib
BuildRequires: mingw32-zlib
%endif

%description
gcab is a tool to manipulate Cabinet archive.

%package -n libgcab1
Summary:        Library to create Cabinet archives

%description -n libgcab1
libgcab is a library to manipulate Cabinet archive using GIO/GObject.

%package -n libgcab1-devel
Summary:        Development files to create Cabinet archives
Requires:       libgcab1%{?_isa} = %{version}-%{release}
Requires:       glib2-devel
Requires:       pkgconfig

%description -n libgcab1-devel
libgcab is a library to manipulate Cabinet archive.

Libraries, includes, etc. to compile with the gcab library.

%if %{with_mingw}
%package -n mingw32-libgcab1
Summary: MinGW library to create Cabinet archive.
BuildArch: noarch

%description -n mingw32-libgcab1
libgcab is a library to manipulate Cabinet archive.

%package -n mingw64-libgcab1
Summary: MinGW library to create Cabinet archive.
BuildArch: noarch

%description -n mingw64-libgcab1
libgcab is a library to manipulate Cabinet archive.

%{?mingw_debug_package}
%endif

%prep
%autosetup -S git_am

%build
%meson
%meson_build

%if %{with_mingw}
%mingw_meson -Dintrospection=false -Ddocs=false
%mingw_ninja
%endif

%check
%meson_test

%install
%meson_install

%find_lang %{name}

%ldconfig_scriptlets -n libgcab1

%if %{with_mingw}
%mingw_ninja_install
%mingw_debug_install_post
%mingw_find_lang %{name}
%endif


%files
%{_bindir}/gcab
%{_mandir}/man1/gcab.1*

%files -n libgcab1 -f %{name}.lang
%license COPYING
%doc NEWS
%{_libdir}/girepository-1.0/GCab-1.0.typelib
%{_libdir}/libgcab-1.0.so.*

%files -n libgcab1-devel
%{_datadir}/gir-1.0/GCab-1.0.gir
%{_datadir}/gtk-doc/html/gcab/*
%{_datadir}/vala/vapi/libgcab-1.0.vapi
%{_datadir}/vala/vapi/libgcab-1.0.deps
%{_includedir}/libgcab-1.0/*
%{_libdir}/libgcab-1.0.so
%{_libdir}/pkgconfig/libgcab-1.0.pc

%if %{with_mingw}
%files -n mingw32-libgcab1 -f mingw32-%{name}.lang
%license COPYING
%{mingw32_bindir}/gcab.exe
%{mingw32_bindir}/libgcab-1.0-0.dll
%{mingw32_libdir}/libgcab-1.0.dll.a
%{mingw32_includedir}/libgcab-1.0/
%{mingw32_libdir}/pkgconfig/libgcab-1.0.pc
%{mingw32_mandir}/man1/gcab.1

%files -n mingw64-libgcab1 -f mingw64-%{name}.lang
%license COPYING
%{mingw64_bindir}/gcab.exe
%{mingw64_bindir}/libgcab-1.0-0.dll
%{mingw64_libdir}/libgcab-1.0.dll.a
%{mingw64_includedir}/libgcab-1.0/
%{mingw64_libdir}/pkgconfig/libgcab-1.0.pc
%{mingw64_mandir}/man1/gcab.1
%endif

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1.6-7
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.6-3
- Add MinGW packages.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.6-1
- new version

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 05 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.5-1
- new version

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.4-1
- New upstream release

* Tue Oct 08 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.3-1
- New upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 1.1-6
- Update BRs for vala packaging changes

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.1-4
- Fix LZX decompression corruption regression.

* Thu Aug  2 2018 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.1-3
- fix 'rewind' regression rhbz#1608301

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Richard Hughes <richard@hughsie.com> - 1.1-1
- New upstream release
- Add git version in --version
- Fix list of new symbols in index page

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0-2
- Switch to %%ldconfig_scriptlets

* Tue Jan 23 2018 Richard Hughes <richard@hughsie.com> - 1.0-1
- New upstream release
- This fixes the security bug known as CVE-2018-5345
- Add new API for fwupd
- Do not encode timezone in generated files
- Fix countless memory leaks when parsing corrupt files
- Fix the calculation of the checksum on big endian machines
- Switch to the Meson buildsystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 09 2016 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7-1
- 0.7 release update.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 01 2015 Fabiano Fidêncio <fidencio@redhat.com> - 0.6-5
- Bump NVR and rebuild due to a mistakenly deleted build

* Thu Jul 30 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.6-4
- Fix wrong file modification date when creating cab.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 0.6-2
- Pull in the base library package when installing -devel

* Tue Mar 17 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.6-1
- Update to upstream release v0.6

* Tue Jan 06 2015 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-7
- Avoid directory traversal CVE-2015-0552. rhbz#1179126

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.4-5
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 12 2013 Simone Caronni <negativo17@gmail.com> - 0.4-2
- Removed rpm 4.5 macros/tags, it cannot be built with the vala in el5/el6.
- Removed redundant requirement on libgcab1%%{_isa}, added automatically by rpm.

* Fri Feb  8 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-1
- Update to upstream v0.4.

* Fri Feb  8 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.3-3
- Align more fields.
- Use double percentage in comment.
- Include COPYING file in gcab package too.

* Fri Feb  8 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.3-2
- Untabify.
- Use %%{buildroot} consitantly.
- Do not use -1.0 in package names.
- Add more tags based on the el5 spec template.
- Re-add --enable-fast-install trick, to make gcab relink.

* Sun Jan 26 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.3-1
- Initial package (rhbz#895757)
