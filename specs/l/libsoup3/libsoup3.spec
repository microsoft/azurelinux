## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global glib2_version 2.70.0

%global with_mingw 0

%if 0%{?fedora}
%global with_mingw 0
%endif

Name:    libsoup3
Version: 3.6.6
Release: %autorelease
Summary: Soup, an HTTP library implementation

License: LGPL-2.0-or-later AND LGPL-2.1-or-later
URL:     https://wiki.gnome.org/Projects/libsoup
Source0: https://download.gnome.org/sources/libsoup/3.6/libsoup-%{version}.tar.xz

# Downstream patch, needed due to glib2 gnutls-hmac.patch
Patch:   no-ntlm-in-fips-mode.patch

BuildRequires: gcc
BuildRequires: gettext
BuildRequires: glib-networking >= %{glib2_version}
BuildRequires: gi-docgen >= 2021.1
BuildRequires: krb5-devel
BuildRequires: meson
BuildRequires: vala
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(gnutls)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(libbrotlidec)
BuildRequires: pkgconfig(libnghttp2)
BuildRequires: pkgconfig(libpsl)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: /usr/bin/ntlm_auth

Recommends: glib-networking%{?_isa} >= %{glib2_version}

%if %{with_mingw}
BuildRequires: mingw32-filesystem >= 107
BuildRequires: mingw32-binutils
BuildRequires: mingw32-gcc
BuildRequires: mingw32-glib2
BuildRequires: mingw32-brotli
BuildRequires: mingw32-libpsl
BuildRequires: mingw32-sqlite
BuildRequires: mingw32-libnghttp2

BuildRequires: mingw64-filesystem >= 107
BuildRequires: mingw64-gcc
BuildRequires: mingw64-binutils
BuildRequires: mingw64-glib2
BuildRequires: mingw64-brotli
BuildRequires: mingw64-libpsl
BuildRequires: mingw64-sqlite
BuildRequires: mingw64-libnghttp2
%endif

%description
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it), but the SOAP parts were removed
long ago.

%package devel
Summary: Header files for the Soup library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Libsoup is an HTTP library implementation in C. This package allows
you to develop applications that use the libsoup library.

%package doc
Summary: Documentation files for %{name}
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends: gi-docgen-fonts
BuildArch: noarch

%description doc
This package contains developer documentation for %{name}.

%if %{with_mingw}

%package -n mingw32-libsoup3
Summary: MinGW library for HTTP functionality
Recommends: mingw32-glib-networking

%description -n mingw32-libsoup3
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

This is the MinGW build of libsoup3

%package -n mingw64-libsoup3
Summary: MinGW library for HTTP functionality
Recommends: mingw64-glib-networking

%description -n mingw64-libsoup3
Libsoup is an HTTP library implementation in C. It was originally part
of a SOAP (Simple Object Access Protocol) implementation called Soup, but
the SOAP and non-SOAP parts have now been split into separate packages.

libsoup uses the Glib main loop and is designed to work well with GTK
applications. This enables GNOME applications to access HTTP servers
on the network in a completely asynchronous fashion, very similar to
the Gtk+ programming model (a synchronous operation mode is also
supported for those who want it).

This is the MinGW build of libsoup3

%{?mingw_debug_package}

%endif

%prep
%autosetup -p1 -n libsoup-%{version}

%build
%meson -Ddocs=enabled -Dautobahn=disabled
%meson_build

%if %{with_mingw}
%mingw_meson \
    -Ddocs=disabled \
    -Dintrospection=disabled \
    -Dtests=false \
    -Dtls_check=false \
    -Dvapi=disabled
%endif

%install
%meson_install
install -m 644 -D tests/libsoup.supp %{buildroot}%{_datadir}/libsoup-3.0/libsoup.supp

%if %{with_mingw}
%mingw_ninja_install
%mingw_find_lang libsoup-3.0
%mingw_debug_install_post
%endif

%find_lang libsoup-3.0

%ifnarch s390x
%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%meson_test
%endif

%files -f libsoup-3.0.lang
%license COPYING
%doc README NEWS AUTHORS
%{_libdir}/libsoup-3.0.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Soup-3.0.typelib

%files devel
%{_includedir}/libsoup-3.0
%{_libdir}/libsoup-3.0.so
%{_libdir}/pkgconfig/libsoup-3.0.pc
%dir %{_datadir}/libsoup-3.0
%{_datadir}/libsoup-3.0/libsoup.supp
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Soup-3.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libsoup-3.0.deps
%{_datadir}/vala/vapi/libsoup-3.0.vapi

%files doc
%{_docdir}/libsoup-3.0/

%if %{with_mingw}
%files -n mingw32-libsoup3 -f mingw32-libsoup-3.0.lang
%license COPYING
%doc README NEWS AUTHORS
%{mingw32_bindir}/libsoup-3.0-0.dll
%{mingw32_includedir}/libsoup-3.0
%{mingw32_libdir}/libsoup-3.0.dll.a
%{mingw32_libdir}/pkgconfig/libsoup-3.0.pc

%files -n mingw64-libsoup3 -f mingw64-libsoup-3.0.lang
%license COPYING
%doc README NEWS AUTHORS
%{mingw64_bindir}/libsoup-3.0-0.dll
%{mingw64_includedir}/libsoup-3.0
%{mingw64_libdir}/libsoup-3.0.dll.a
%{mingw64_libdir}/pkgconfig/libsoup-3.0.pc
%endif

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 3.6.6-2
- test: add initial lock files

* Mon Feb 16 2026 Jan Grulich <jgrulich@redhat.com> - 3.6.6-1
- Update to 3.6.6

* Fri Jan 30 2026 Michael Catanzaro <mcatanzaro@gnome.org> - 3.6.5-13
- Add downstream patch to disable NTLM authentication in FIPS mode

* Thu Jan 29 2026 Marc-André Lureau <marcandre.lureau@redhat.com> - 3.6.5-12
- Fix tld-test

* Thu Jan 29 2026 Marc-André Lureau <marcandre.lureau@redhat.com> - 3.6.5-11
- Add mingw{32,64}-gcc BR

* Thu Jan 29 2026 Marc-André Lureau <marcandre.lureau@redhat.com> - 3.6.5-10
- Add MinGW packages. rhbz#2102072

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Sep 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 3.6.5-8
- Disable tests on s390x

* Thu Sep 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 3.6.5-7
- Bump EVR

* Thu Sep 18 2025 Gwyn Ciesla <gwync@protonmail.com> - 3.6.5-6
- Bump EVR

* Tue Sep 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 3.6.5-5
- Patch for deadlocks

* Tue Jul 29 2025 Marek Kasik <mkasik@redhat.com> - 3.6.5-4
- Fix multiple CVEs

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Andrew Lukoshko <alukoshko@almalinux.org> - 3.6.5-2
- Move %%find_lang to %%install

* Mon Mar 24 2025 nmontero <nmontero@redhat.com> - 3.6.5-1
- Update to 3.6.5

* Tue Jan 28 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 3.6.4-2
- Actually run tests in %%check

* Mon Jan 20 2025 nmontero <nmontero@redhat.com> - 3.6.4-1
- Update to 3.6.4

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 nmontero <nmontero@redhat.com> - 3.6.3-1
- Update to 3.6.3

* Mon Nov 25 2024 nmontero <nmontero@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Tue Aug 27 2024 David King <amigadave@amigadave.com> - 3.6.0-1
- Update to 3.6.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 David King <amigadave@amigadave.com> - 3.5.2-1
- Update to 3.5.2

* Wed Jun 26 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 3.5.1-3
- Run tests in %%check

* Wed Jun 26 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 3.5.1-2
- Remove useless README

* Mon May 06 2024 David King <amigadave@amigadave.com> - 3.5.1-1
- Update to 3.5.1

* Sun Apr 28 2024 Michel Lind <salimma@fedoraproject.org> - 3.4.4-4
- Add version constraint to glib-networking BR as well

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Gwyn Ciesla <gwync@protonmail.com> - 3.4.4-1
- 3.4.4

* Fri Sep 15 2023 Gwyn Ciesla <gwync@protonmail.com> - 3.4.3-1
- 3.4.3

* Fri Aug 25 2023 Adam Williamson <awilliam@redhat.com> - 3.4.2-4
- Backport MR #374 to fix some crashes

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 02 2023 David King <amigadave@amigadave.com> - 3.4.2-2
- Drop reverted patch

* Tue May 02 2023 David King <amigadave@amigadave.com> - 3.4.2-1
- Update to 3.4.2

* Fri Apr 21 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 3.4.1-2
- Add patch to maybe fix connection crashes?

* Fri Apr 21 2023 David King <amigadave@amigadave.com> - 3.4.1-1
- Update to 3.4.1

* Sat Mar 18 2023 W. Michael Petullo <mike@flyn.org> - 3.4.0-2
- Distribute libsoup.supp

* Fri Mar 17 2023 David King <amigadave@amigadave.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 08 2023 Gwyn Ciesla <gwync@protonmail.com> - 3.3.1-2
- migrated to SPDX license

* Wed Feb 15 2023 David King <amigadave@amigadave.com> - 3.3.1-1
- Update to 3.3.1

* Mon Feb 06 2023 David King <amigadave@amigadave.com> - 3.3.0-1
- Update to 3.3.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.2.2-2
- Ensure correct fonts are installed for HTML docs

* Thu Nov 03 2022 David King <amigadave@amigadave.com> - 3.2.2-1
- Update to 3.2.2

* Fri Oct 28 2022 David King <amigadave@amigadave.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2022 Kalev Lember <klember@redhat.com> - 3.2.0-2
- Backport upstream MR310 to fix gnome-maps crashes (#2129914)

* Fri Sep 16 2022 Kalev Lember <klember@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 06 2022 Kalev Lember <klember@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Mon Aug 15 2022 Kalev Lember <klember@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Mon Aug 15 2022 Kalev Lember <klember@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 06 2022 David King <amigadave@amigadave.com> - 3.1.1-1
- Update to 3.1.1

* Wed Jul 06 2022 David King <amigadave@amigadave.com> - 3.0.7-1
- Update to 3.0.7

* Tue Apr 26 2022 Adam Williamson <awilliam@redhat.com> - 3.0.6-3
- Revert "Backport MR #281 to fix a crash (#2070240)"

* Tue Apr 26 2022 Adam Williamson <awilliam@redhat.com> - 3.0.6-2
- Backport MR #281 to fix a crash (#2070240)

* Fri Apr 01 2022 David King <amigadave@amigadave.com> - 3.0.6-1
- Update to 3.0.6

* Fri Mar 18 2022 David King <amigadave@amigadave.com> - 3.0.5-1
- Update to 3.0.5

* Tue Jan 25 2022 Patrick Griffis <tingping@fedoraproject.org> - 3.0.4-2
- Remove unecessary dependencies

* Wed Jan 19 2022 Gwyn Ciesla <gwync@protonmail.com> - 3.0.4-1
- Initial import.
## END: Generated by rpmautospec
