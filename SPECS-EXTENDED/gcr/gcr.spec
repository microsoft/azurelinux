%define majmin %(echo %{version} | cut -d. -f1-2)

Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%ifarch %{valgrind_arches}
%global has_valgrind 1
%endif
 
Name:           gcr
Version:        3.41.1
Release:        10%{?dist}
Summary:        A library for bits of crypto UI and parsing
# gck/pkcs11n.h is MPL 1.1/GPL 2.0/LGPL 2.1
# for LicenseRef-Fedora-Public-Domain see https://gitlab.com/fedora/legal/fedora-license-data/-/merge_requests/424
# gck/pkcs11x.h is FSFULLRWD
# ui/icons/render-icons.py is LGPL-3.0-or-later OR CC-BY-SA-3.0
# docs/COPYING is GCR-docs
License:        LGPL-2.1-or-later AND LicenseRef-Fedora-Public-Domain AND FSFULLRWD AND (LGPL-3.0-or-later OR CC-BY-SA-3.0) AND (MPL-1.1 OR GPL-2.0-or-later OR LGPL-2.1-or-later) AND GCR-docs
URL:            https://wiki.gnome.org/Projects/CryptoGlue
Source0:        https://download.gnome.org/sources/%{name}/%{majmin}/%{name}-%{version}.tar.xz
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  meson
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  systemd-devel
BuildRequires:  pkgconfig(p11-kit-1)
BuildRequires:  docbook-style-xsl
BuildRequires:  libgcrypt-devel
BuildRequires:  desktop-file-utils
BuildRequires:  systemd-rpm-macros
BuildRequires:  vala
BuildRequires:  python3-markdown
BuildRequires:  python3-markupsafe
BuildRequires:  python3-typogrify
BuildRequires:  python3-jinja2
%if 0%{?has_valgrind}
BuildRequires:  valgrind-devel
%endif
BuildRequires:  /usr/bin/gpg2
BuildRequires:  /usr/bin/ssh-add
BuildRequires:  /usr/bin/ssh-agent
BuildRequires:  /usr/bin/xsltproc
 
Requires: %{name}-base%{?_isa} = %{version}-%{release}
Requires: /usr/bin/ssh-add
Requires: /usr/bin/ssh-agent
 
# Explicitly conflict with older gcr package that ships the same libraries
Conflicts: gcr < 3.90.0
 
%description
gcr is a library for displaying certificates, and crypto UI, accessing
key stores. It also provides a viewer for crypto files on the GNOME
desktop.
 
gck is a library for accessing PKCS#11 modules like smart cards.
 
%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# Explicitly conflict with older gcr package that ships the same libraries
Conflicts: gcr-devel < 3.90.0
 
%description devel
The %{name}-devel package includes the header files for the gcr library.
 
%package base
Summary: Library files for gcr
# Explicitly conflict with older gcr package that ships the same libraries
Conflicts: gcr-base < 3.90.0
 
%description base
The %{name}-base package includes the gcr-base library.
 
%prep
%autosetup -p1 -n gcr-%{version}
 
%build
%meson
%meson_build
%install
%meson_install
%find_lang gcr
 
# Remove the bits that would conflict with gcr 4 package
rm -rf $RPM_BUILD_ROOT%{_libexecdir}/gcr-ssh-agent
rm -rf $RPM_BUILD_ROOT%{_userunitdir}/gcr-ssh-agent.service
rm -rf $RPM_BUILD_ROOT%{_userunitdir}/gcr-ssh-agent.socket
 
%files -f gcr.lang
%doc NEWS README.md
%license COPYING
%{_bindir}/gcr-viewer
%{_datadir}/applications/gcr-viewer.desktop
%dir %{_datadir}/GConf
%dir %{_datadir}/GConf/gsettings
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp.convert
%{_datadir}/GConf/gsettings/org.gnome.crypto.pgp_keyservers.convert
%{_datadir}/glib-2.0/schemas/org.gnome.crypto.pgp.gschema.xml
%{_libdir}/girepository-1.0
%{_libdir}/libgcr-ui-3.so.*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/mime/packages/gcr-crypto-types.xml
%{_libexecdir}/gcr-prompter
%{_libexecdir}/gcr-ssh-askpass
%{_datadir}/dbus-1/services/org.gnome.keyring.PrivatePrompter.service
%{_datadir}/dbus-1/services/org.gnome.keyring.SystemPrompter.service
%{_datadir}/applications/gcr-prompter.desktop
 
%files devel
%{_includedir}/gck-1/
%{_includedir}/gcr-3/
%{_libdir}/libgck-1.so
%{_libdir}/libgcr-base-3.so
%{_libdir}/libgcr-ui-3.so
%{_libdir}/pkgconfig/gck-1.pc
%{_libdir}/pkgconfig/gcr-3.pc
%{_libdir}/pkgconfig/gcr-base-3.pc
%{_libdir}/pkgconfig/gcr-ui-3.pc
%{_datadir}/gir-1.0/
%{_datadir}/vala/
%doc %{_datadir}/doc/gck-1/
%doc %{_datadir}/doc/gcr-3/
%doc %{_datadir}/doc/gcr-ui-3/
 
%files base
%{_libdir}/libgck-1.so.*
%{_libdir}/libgcr-base-3.so.*

%changelog
* Wed Mar 19 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 3.41.1-10
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.41.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.41.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.41.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.41.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.41.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 3.41.1-4
- Explicitly BR pkgconfig(systemd); fixes RHBZ#2142295

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.41.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Kalev Lember <klember@redhat.com> - 3.41.1-2
- Add back a few more needed bits instead of just libraries

* Tue Jul 19 2022 Kalev Lember <klember@redhat.com> - 3.41.1-1
- Initial build of parallel-installable gcr3 version, based on earlier gcr packaging
