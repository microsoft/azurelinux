Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           xdg-dbus-proxy
Version:        0.1.6
Release:        2%{?dist}
Summary:        Filtering proxy for D-Bus connections

License:        LGPL-2.1-or-later
URL:            https://github.com/flatpak/xdg-dbus-proxy/
Source0:        https://github.com/flatpak/xdg-dbus-proxy/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  meson
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  /usr/bin/xsltproc

Requires:       dbus

%description
xdg-dbus-proxy is a filtering proxy for D-Bus connections. It was originally
part of the flatpak project, but it has been broken out as a standalone module
to facilitate using it in other contexts.

%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%files
%doc NEWS README.md
%license COPYING
%{_bindir}/xdg-dbus-proxy
%{_mandir}/man1/xdg-dbus-proxy.1*

%changelog
* Thu Dec 26 2024 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.1.6-2
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Fri Oct 11 2024 David King <amigadave@amigadave.com> - 0.1.6-1
- Update to 0.1.6 (#2307503)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 07 2023 Kalev Lember <klember@redhat.com> - 0.1.5-1
- Update to 0.1.5 (rhbz#2229713)

* Wed Jul 19 2023 Bastien Nocera <bnocera@redhat.com> - 0.1.4-2
- Fix D-Bus disconnection when an object path was overly long

* Wed Jul 19 2023 Bastien Nocera <bnocera@redhat.com> - 0.1.4-1
- Update to 0.1.4

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Mar 02 2022 Debarshi Ray <rishi@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Kalev Lember <klember@redhat.com> - 0.1.2-1
- Update to 0.1.2

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Kalev Lember <klember@redhat.com> - 0.1.1-1
- Update to 0.1.1
- Build man pages
- Include COPYING file as license

* Fri Nov 23 2018 Kalev Lember <klember@redhat.com> - 0.1.0-1
- Initial Fedora packaging
