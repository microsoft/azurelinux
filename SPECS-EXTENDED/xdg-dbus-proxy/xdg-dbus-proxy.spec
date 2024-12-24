Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           xdg-dbus-proxy
Version:        0.1.6
Release:        1%{?dist}
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
* Mon Dec 23 2024 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.1.6-1
- Upgraded to version 0.1.6
- License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.1.2-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
