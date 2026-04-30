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

Name:           at-spi2-core
Version:        2.58.3
Release:        %autorelease
Summary:        Protocol definitions and daemon for D-Bus at-spi

License:        LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/%{name}/
Source0:        https://download.gnome.org/sources/%{name}/2.58/%{name}-%{version}.tar.xz
# scriptlet to set AT_SPI_BUS for XWayland apps that run as root (i.e. anaconda)
# https://bugzilla.redhat.com/show_bug.cgi?id=1821345
Source1:        xwayland-session-scriptlet

BuildRequires:  /usr/bin/sphinx-build
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  gobject-introspection-devel
BuildRequires:  meson
BuildRequires:  python3-devel
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libei-1.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xtst)

Requires:       dbus
# For xwayland-session-scriptlet
# https://bugzilla.redhat.com/show_bug.cgi?id=2137281
Requires:       /usr/bin/xprop

%description
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

%package devel
Summary: Development files and headers for at-spi2-core
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The at-spi2-core-devel package includes the header files and
API documentation for libatspi.

%package -n atk
Summary: Interfaces for accessibility support
# Dependency required for translations.
Requires: at-spi2-core%{?_isa} = %{version}-%{release}

%description -n atk
The ATK library provides a set of interfaces for adding accessibility
support to applications and graphical user interface toolkits. By
supporting the ATK interfaces, an application or toolkit can be used
with tools such as screen readers, magnifiers, and alternative input
devices.

%package -n atk-devel
Summary: Development files for the ATK accessibility toolkit
Requires: atk%{?_isa} = %{version}-%{release}

%description -n atk-devel
This package includes libraries, header files, and developer documentation
needed for development of applications or toolkits which use ATK.

%package -n at-spi2-atk
Summary: A GTK+ module that bridges ATK to D-Bus at-spi
Requires: atk%{?_isa} = %{version}-%{release}
Requires: at-spi2-core%{?_isa} = %{version}-%{release}

%description -n at-spi2-atk
at-spi allows assistive technologies to access GTK-based
applications. Essentially it exposes the internals of applications for
automation, so tools such as screen readers, magnifiers, or even
scripting interfaces can query and interact with GUI controls.

This version of at-spi is a major break from previous versions.
It has been completely rewritten to use D-Bus rather than
ORBIT / CORBA for its transport protocol.

This package includes a gtk-module that bridges ATK to the new
D-Bus based at-spi.

%package -n at-spi2-atk-devel
Summary: A GTK+ module that bridges ATK to D-Bus at-spi
Requires: at-spi2-atk%{?_isa} = %{version}-%{release}

%description -n at-spi2-atk-devel
The at-spi2-atk-devel package includes the header files for the at-spi2-atk
library.

%prep
%autosetup -p1

%build
%meson -Ddocs=true -Ddefault_bus=dbus-broker -Ddbus_daemon=/usr/bin/dbus-daemon -Ddbus_broker=/usr/bin/dbus-broker-launch
%meson_build

%install
%meson_install
install -Dpm 0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/Xwayland-session.d/00-at-spi

%{find_lang} %{name}

%files -f %{name}.lang
%license COPYING
%doc NEWS README.md
%{_libexecdir}/at-spi2-registryd
%dir %{_datadir}/defaults
%dir %{_datadir}/defaults/at-spi2
%{_datadir}/defaults/at-spi2/accessibility.conf
%{_sysconfdir}/xdg/autostart/at-spi-dbus-bus.desktop
# the 'logical' owner of this dir is gnome-settings-daemon, but g-s-d
# indirectly depends on this package, so depending on it to provide
# this directory would create a circular dependency. so we just co-own
# it instead
%dir %{_sysconfdir}/xdg/Xwayland-session.d
%{_sysconfdir}/xdg/Xwayland-session.d/00-at-spi
%{_libdir}/libatspi.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Atspi-2.0.typelib
%{_libexecdir}/at-spi-bus-launcher
%dir %{_datadir}/dbus-1/accessibility-services/
%{_datadir}/dbus-1/accessibility-services/org.a11y.atspi.Registry.service
%{_datadir}/dbus-1/services/org.a11y.Bus.service
%{_userunitdir}/at-spi-dbus-bus.service
%dir %{python3_sitearch}/gi/overrides/
%{python3_sitearch}/gi/overrides/Atspi.py
%{python3_sitearch}/gi/overrides/__pycache__/Atspi.*

%files devel
%{_libdir}/libatspi.so
%{_docdir}/libatspi
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Atspi-2.0.gir
%{_includedir}/at-spi-2.0
%{_libdir}/pkgconfig/atspi-2.pc

%files -n atk
%license COPYING
%{_libdir}/libatk-1.0.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Atk-1.0.typelib

%files -n atk-devel
%{_libdir}/libatk-1.0.so
%{_includedir}/atk-1.0
%{_libdir}/pkgconfig/atk.pc
%{_docdir}/atk
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Atk-1.0.gir

%files -n at-spi2-atk
%license COPYING
%dir %{_libdir}/gtk-2.0
%dir %{_libdir}/gtk-2.0/modules
%{_libdir}/gtk-2.0/modules/libatk-bridge.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/at-spi2-atk.desktop
%{_libdir}/libatk-bridge-2.0.so.*

%files -n at-spi2-atk-devel
%{_includedir}/at-spi2-atk/2.0/atk-bridge.h
%{_libdir}/libatk-bridge-2.0.so
%{_libdir}/pkgconfig/atk-bridge-2.0.pc

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 2.58.3-2
- test: add initial lock files

* Thu Jan 22 2026 Barry Dunn <badunn@redhat.com> - 2.58.3-1
- Update to 2.58.3

* Wed Dec 10 2025 Adrian Vovk <adrianvovk@gmail.com> - 2.58.2-1
- Update to 2.58.2

* Mon Oct 13 2025 Petr Schindler <pschindl@redhat.com> - 2.58.1-1
- Update to 2.58.1

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.58.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 15 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.58.0-1
- Update to 2.58.0

* Thu Sep 04 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 2.57.2-1
- Update to 2.57.2

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.57.1-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Tue Aug 05 2025 nmontero <nmontero@redhat.com> - 2.57.1-1
- Update to 2.57.1

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.57.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Milan Crha <mcrha@redhat.com> - 2.57.0-1
- Update to 2.57.0

* Wed Jun 25 2025 Milan Crha <mcrha@redhat.com> - 2.56.2-2
- Claim ownership of %%{_datadir}/dbus-1/accessibility-services/

* Tue Apr 29 2025 nmontero <nmontero@redhat.com> - 2.56.2-1
- Update to 2.56.2

* Mon Mar 31 2025 nmontero <nmontero@redhat.com> - 2.56.1-1
- Update to 2.56.1

* Mon Mar 17 2025 nmontero <nmontero@redhat.com> - 2.56.0-1
- Update to 2.56.0

* Mon Mar 03 2025 nmontero <nmontero@redhat.com> - 2.55.90-1
- Update to 2.55.90

* Mon Feb 03 2025 nmontero <nmontero@redhat.com> - 2.55.2-1
- Update to 2.55.2

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.55.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 15 2025 nmontero <nmontero@redhat.com> - 2.55.0.1-1
- Update to 2.55.0.1

* Mon Jan 13 2025 nmontero <nmontero@redhat.com> - 2.55.0-1
- Update to 2.55.0

* Tue Sep 17 2024 Michel Lind <salimma@fedoraproject.org> - 2.54.0-2
- Fix project URL, old page is 404

* Tue Sep 17 2024 nmontero <nmontero@redhat.com> - 2.54.0-1
- Update to 2.54.0

* Sun Sep 01 2024 David King <amigadave@amigadave.com> - 2.53.90-1
- Update to 2.53.90

* Mon Aug 19 2024 Adam Williamson <awilliam@redhat.com> - 2.53.1-2
- Backport MR #166 to fix crash in Orca (#2305763)

* Thu Aug 08 2024 nmontero <nmontero@redhat.com> - 2.53.1-1
- Update to 2.53.1

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.53.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 David King <amigadave@amigadave.com> - 2.53.0-1
- Update to 2.53.0

* Fri Apr 12 2024 Lukáš Tyrychtr <ltyrycht@redhat.com> - 2.52.0-2
- Add missing requires for atk-devel

* Sun Mar 17 2024 David King <amigadave@amigadave.com> - 2.52.0-1
- Update to 2.52.0

* Thu Mar 07 2024 David King <amigadave@amigadave.com> - 2.51.91-1
- Update to 2.51.91

* Sat Feb 17 2024 David King <amigadave@amigadave.com> - 2.51.90-1
- Update to 2.51.90

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.51.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 David King <amigadave@amigadave.com> - 2.51.0-1
- Update to 2.51.0

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.50.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Kalev Lember <klember@redhat.com> - 2.50.1-1
- Update to 2.50.1

* Sat Sep 16 2023 Kalev Lember <klember@redhat.com> - 2.50.0-1
- Update to 2.50.0

* Tue Sep 05 2023 Kalev Lember <klember@redhat.com> - 2.49.91-2
- Fix whitespace

* Tue Sep 05 2023 Kalev Lember <klember@redhat.com> - 2.49.91-1
- Update to 2.49.91

* Sat Aug 05 2023 Kalev Lember <klember@redhat.com> - 2.49.90-1
- Update to 2.49.90

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.49.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 David King <amigadave@amigadave.com> - 2.49.1-1
- Update to 2.49.1

* Wed May 24 2023 Kalev Lember <klember@redhat.com> - 2.48.3-1
- Update to 2.48.3

* Fri May 12 2023 David King <amigadave@amigadave.com> - 2.48.2-1
- Update to 2.48.2

* Thu May 11 2023 David King <amigadave@amigadave.com> - 2.48.1-1
- Update to 2.48.1

* Sun Mar 19 2023 David King <amigadave@amigadave.com> - 2.48.0-1
- Update to 2.48.0

* Sat Mar 04 2023 David King <amigadave@amigadave.com> - 2.47.90-1
- Update to 2.47.90

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.47.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 08 2023 David King <amigadave@amigadave.com> - 2.47.1-1
- Update to 2.47.1

* Wed Nov 02 2022 David King <amigadave@amigadave.com> - 2.46.0-2
- Require xprop for xwayland scriptlet (#2137281)

* Fri Oct 28 2022 David King <amigadave@amigadave.com> - 2.46.0-1
- Update to 2.46.0

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.44.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 22 2022 David King <amigadave@amigadave.com> - 2.44.1-1
- Update to 2.44.1

* Fri Mar 18 2022 David King <amigadave@amigadave.com> - 2.44.0-1
- Update to 2.44.0

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.42.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 20 2021 Kalev Lember <klember@redhat.com> - 2.42.0-1
- Update to 2.42.0

* Tue Aug 03 2021 Kalev Lember <klember@redhat.com> - 2.40.3-1
- Update to 2.40.3

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.40.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Kalev Lember <klember@redhat.com> - 2.40.2-1
- Update to 2.40.2

* Wed May 05 2021 Kalev Lember <klember@redhat.com> - 2.40.1-1
- Update to 2.40.1

* Sat Apr 17 2021 Adam Williamson <awilliam@redhat.com> - 2.40.0-2
- Fix AT_SPI_BUS for Xwayland apps run as root (#1821345)

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 2.40.0-1
- Update to 2.40.0

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 2.39.91-1
- Update to 2.39.91

* Mon Feb 22 2021 Kalev Lember <klember@redhat.com> - 2.39.90.1-1
- Update to 2.39.90.1

* Wed Feb 17 2021 Kalev Lember <klember@redhat.com> - 2.39.90-2
- Drop unused ldconfig_scriptlets macro call

* Wed Feb 17 2021 Kalev Lember <klember@redhat.com> - 2.39.90-1
- Update to 2.39.90

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Sep 24 2020 Michael Catanzaro <mcatanzaro@gnome.org> - 2.38.0-2
- Add patch to fix a11y on login screen

* Sat Sep 12 2020 Kalev Lember <klember@redhat.com> - 2.38.0-1
- Update to 2.38.0

* Sun Sep 06 2020 Kalev Lember <klember@redhat.com> - 2.37.92-1
- Update to 2.37.92

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 2.37.90-1
- Update to 2.37.90

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Mar 08 2020 Kalev Lember <klember@redhat.com> - 2.36.0-1
- Update to 2.36.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 2.35.92-1
- Update to 2.35.92

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.35.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Kalev Lember <klember@redhat.com> - 2.35.1-1
- Update to 2.35.1

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 2.34.0-1
- Update to 2.34.0

* Tue Sep 03 2019 Kalev Lember <klember@redhat.com> - 2.33.92-1
- Update to 2.33.92

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 2.33.90-1
- Update to 2.33.90

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.33.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 05 2019 Kalev Lember <klember@redhat.com> - 2.33.2-1
- Update to 2.33.2

* Tue May 21 2019 Kalev Lember <klember@redhat.com> - 2.33.1-1
- Update to 2.33.1

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 2.32.1-2
- Rebuild with Meson fix for #1699099

* Tue Apr 09 2019 Kalev Lember <klember@redhat.com> - 2.32.1-1
- Update to 2.32.1

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 2.32.0-1
- Update to 2.32.0

* Mon Mar 04 2019 Kalev Lember <klember@redhat.com> - 2.31.92-1
- Update to 2.31.92

* Tue Feb 19 2019 Kalev Lember <klember@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.31.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 22 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.31.1-2
- Remove obsolete ldconfig scriptlets

* Tue Jan 08 2019 Kalev Lember <klember@redhat.com> - 2.31.1-1
- Update to 2.31.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 2.30.0-2
- Rebuilt against fixed atk (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Tue Aug 28 2018 Stephen Gallagher <sgallagh@redhat.com> - 2.28.0-4
- Update to newer version of dbus-broker support

* Fri Aug 10 2018 David Herrmann <dh.herrmann@gmail.com> - 2.28.0-3
- at-spi2-core: use dbus-broker if available

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Kalev Lember <klember@redhat.com> - 2.27.1-2
- Drop unused buildrequires

* Tue Dec 19 2017 Kalev Lember <klember@redhat.com> - 2.27.1-1
- Update to 2.27.1

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com> - 2.26.2-1
- Update to 2.26.2

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Thu Sep 07 2017 Kalev Lember <klember@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Fri Aug 25 2017 Kalev Lember <klember@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 2.25.90-1
- Update to 2.25.90

* Mon Aug 14 2017 Ville Skyttä <ville.skytta@iki.fi> - 2.25.4-6
- Own %%{_datadir}/gir-1.0 as well

* Mon Aug 14 2017 Ville Skyttä <ville.skytta@iki.fi> - 2.25.4-5
- Own %%{_libdir}/girepository-1.0 and %%{_datadir}/defaults dirs

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.4-4
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 25 2017 Kalev Lember <klember@redhat.com> - 2.25.4-2
- Add missing build dep

* Sun Jun 25 2017 Kalev Lember <klember@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Mon Jun 12 2017 Kalev Lember <klember@redhat.com> - 2.25.2-1
- Update to 2.25.2

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Feb 14 2017 Richard Hughes <richard@hughsie.com> - 2.23.90-2
- Actuall upload sources

* Tue Feb 14 2017 Richard Hughes <richard@hughsie.com> - 2.23.90-1
- Update to 2.23.90

* Mon Feb 13 2017 Richard Hughes <richard@hughsie.com> - 2.23.4-1
- Update to 2.23.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 26 2016 Kalev Lember <klember@redhat.com> - 2.22.0-2
- Don't set group tags

* Mon Sep 26 2016 Kalev Lember <klember@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Wed Jul 20 2016 Richard Hughes <richard@hughsie.com> - 2.21.4-1
- Update to 2.21.4

* Wed Jun 22 2016 Richard Hughes <richard@hughsie.com> - 2.21.2-1
- Update to 2.21.2

* Mon May 09 2016 Kalev Lember <klember@redhat.com> - 2.21.1-1
- Update to 2.21.1

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 2.20.1-2
- Fix dates in old changelog entries

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 2.20.1-1
- Update to 2.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Tue Mar 15 2016 Richard Hughes <richard@hughsie.com> - 2.19.92-2
- Fix filelists

* Tue Mar 15 2016 Richard Hughes <richard@hughsie.com> - 2.19.92-1
- Update to 2.19.92

* Tue Mar 01 2016 Richard Hughes <richard@hughsie.com> - 2.19.91-1
- Update to 2.19.91

* Tue Feb 16 2016 Richard Hughes <richard@hughsie.com> - 2.19.90-1
- Update to 2.19.90

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 2.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 24 2015 Kalev Lember <klember@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Wed Oct 28 2015 Kalev Lember <klember@redhat.com> - 2.19.1-1
- Update to 2.19.1

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.18.0-1
- Update to 2.18.0

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 2.17.90-2
- Use make_install macro

* Mon Aug 17 2015 Kalev Lember <klember@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Tue Jul 28 2015 Kalev Lember <klember@redhat.com> - 2.17.1-2
- Use license macro for COPYING

* Tue Jul 28 2015 Kalev Lember <klember@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 2.16.0-1
- Update to 2.16.0

* Tue Feb 17 2015 Richard Hughes <richard@hughsie.com> - 2.15.90-1
- Update to 2.15.90

* Tue Jan 20 2015 Richard Hughes <richard@hughsie.com> - 2.15.4-1
- Update to 2.15.4

* Wed Dec 17 2014 Kalev Lember <kalevlember@gmail.com> - 2.15.3-1
- Update to 2.15.3

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 2.15.2-1
- Update to 2.15.2

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 2.14.1-1
- Update to 2.14.1

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.14.0-1
- Update to 2.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.92-1
- Update to 2.13.92

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.90-1
- Update to 2.13.90

* Fri Aug 15 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 2.13.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.4-2
- Rebuilt for gobject-introspection 1.41.4

* Sun Jul 20 2014 Kalev Lember <kalevlember@gmail.com> - 2.13.4-1
- Update to 2.13.4

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 2.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Richard Hughes <richard@hughsie.com> - 2.13.1-1
- Update to 2.13.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 2.12.0-2
- Tighten -devel deps

* Mon Mar 24 2014 Richard Hughes <richard@hughsie.com> - 2.12.0-1
- Update to 2.12.0

* Tue Mar 18 2014 Richard Hughes <richard@hughsie.com> - 2.11.92-1
- Update to 2.11.92

* Tue Mar 04 2014 Richard Hughes <richard@hughsie.com> - 2.11.91-1
- Update to 2.11.91

* Wed Feb 19 2014 Richard Hughes <richard@hughsie.com> - 2.11.90-1
- Update to 2.11.90

* Tue Feb 04 2014 Richard Hughes <richard@hughsie.com> - 2.11.5-1
- Update to 2.11.5

* Tue Dec 17 2013 Richard Hughes <richard@hughsie.com> - 2.11.3-1
- Update to 2.11.3

* Tue Nov 19 2013 Richard Hughes <richard@hughsie.com> - 2.11.2-1
- Update to 2.11.2

* Mon Nov 04 2013 Kalev Lember <kalevlember@gmail.com> - 2.11.1-1
- Update to 2.11.1

* Mon Oct 28 2013 Richard Hughes <richard@hughsie.com> - 2.10.1-1
- Update to 2.10.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com> - 2.10.0-1
- Update to 2.10.0

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.92-1
- Update to 2.9.92

* Mon Sep 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.91-1
- Update to 2.9.91

* Wed Aug 21 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.90-1
- Update to 2.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.5-1
- Update to 2.9.5

* Sun Jul 28 2013 Rui Matos <tiagomatos@gmail.com> - 2.9.4-3
- autoreconf harder

* Sat Jul 20 2013 Rui Matos <tiagomatos@gmail.com> - 2.9.4-2
- Run autoreconf instead of a sed hack to avoid RPATH embedding

* Tue Jul 16 2013 Richard Hughes <richard@hughsie.com> - 2.9.4-1
- Update to 2.9.4

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.3-1
- Update to 2.9.3

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 2.9.2-1
- Update to 2.9.2

* Mon Mar 25 2013 Kalev Lember <kalevlember@gmail.com> - 2.8.0-1
- Update to 2.8.0

* Thu Mar 07 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.91-1
- 2.7.91

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.90-1
- 2.7.90

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com> - 2.7.5-1
- 2.7.5

* Wed Jan 16 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.4.1-1
- 2.7.4.1

* Wed Jan 16 2013 Matthias Clasen <mclasen@redhat.com> - 2.7.4-1
- 2.7.4

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.3-1
- Update to 2.7.3

* Tue Nov 27 2012 Rui Matos <tiagomatos@gmail.com> - 2.7.1-2
- Remove unused patch files

* Thu Nov 08 2012 Kalev Lember <kalevlember@gmail.com> - 2.7.1-1
- Update to 2.7.1

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 2.6.1-1
- Update to 2.6.1

* Tue Sep 25 2012 Richard Hughes <richard@hughsie.com> - 2.6.0-1
- Update to 2.6.0

* Wed Sep 19 2012 Richard Hughes <richard@hughsie.com> - 2.5.92-1
- Update to 2.5.92

* Tue Sep 04 2012 Richard Hughes <richard@hughsie.com> - 2.5.91-1
- Update to 2.5.91

* Tue Aug 07 2012 Richard Hughes <richard@hughsie.com> - 2.5.5-1
- Update to 2.5.5

* Fri Jul 27 2012 Dennis Gilmore <dennis@ausil.us> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <richard@hughsie.com> - 2.5.4-1
- Update to 2.5.4

* Tue Jun 26 2012 Richard Hughes <richard@hughsie.com> - 2.5.3-1
- Update to 2.5.3

* Wed Jun 06 2012 Richard Hughes <richard@hughsie.com> - 2.5.2-1
- Update to 2.5.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 2.5.1-1
- 2.5.1

* Mon Apr 16 2012 Kalev Lember <kalevlember@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Wed Mar 28 2012 Matthias Clasen <mclasen@redhat.com> - 2.4.0-1
- 2.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 2.3.92-1
- 2.3.92

* Tue Mar 06 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.91-1
- 2.3.91

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.90-1
- 2.3.90

* Tue Feb 07 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.5-1
- 2.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 2.3.4-1
- 2.3.4

* Tue Jan 10 2012 Peter Robinson <pbrobinson@gmail.com> - 2.3.3-2
- Fix the rpath issue for building gobject-introspection properly as
  suggested from upstream

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.3-1
- 2.3.3

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.2-1
- fix version

* Mon Nov 21 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.3-1
- 2.3.3

* Wed Nov 02 2011 Matthias Clasen <mclasen@redhat.com> - 2.3.1-1
- 2.3.1

* Wed Oct 26 2011 Dennis Gilmore <dennis@ausil.us> - 2.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 2.2.1-1
- 2.2.1

* Wed Sep 28 2011 Ray Strode <rstrode@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.92-1
- 2.1.92

* Wed Sep 07 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.91-1
- 2.1.91

* Tue Jul 26 2011 Matthias Clasen <mclasen@redhat.com> - 2.1.4-1
- 2.1.4

* Thu Jun 16 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.1.2-1
- Update to 2.1.2

* Wed May 11 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 26 2011 Matthias Clasen <mclasen@redhat.com> - 2.0.1-1
- sync with f15

* Mon Apr 04 2011 Matthias Clasen <mclasen@redhat.com> - 2.0.0-1
- 2.0.0

* Fri Apr 01 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.93-3
- forgotten patch

* Fri Apr 01 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.93-2
- Fix 30 second wait during login

* Sat Mar 26 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.93-1
- 1.91.93

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.92-4
- try again

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.92-3
- try again

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.92-2
- fix file list

* Tue Mar 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.92-1
- 2.91.92

* Thu Mar 10 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.91-2
- fix a crash on logout

* Tue Mar 08 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.91-1
- 1.91.91

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.90-1
- 1.91.90

* Tue Feb 08 2011 Dennis Gilmore <dennis@ausil.us> - 1.91.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6.1-1
- Update to 1.91.6.1

* Wed Feb 02 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6-2
- Fix the files list

* Wed Feb 02 2011 Christopher Aillon <caillon@redhat.com> - 1.91.6-1
- Update to 1.91.6

* Sun Jan 23 2011 Christopher Aillon <caillon@redhat.com> - 1.91.5-7
- BR hack to get this to build

* Sat Jan 22 2011 Christopher Aillon <caillon@redhat.com> - 1.91.5-6
- Add gobject-introspection support

* Sat Jan 22 2011 Christopher Aillon <caillon@redhat.com> - 1.91.5-5
- Fix typo in the configure flag

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-4
- fix file list

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-3
- add a devel package

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-2
- fix BRs

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 1.91.5-1
- 1.91.5

* Fri Nov 12 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.2-1
- 1.91.2

* Tue Oct 05 2010 Matthias Clasen <mclasen@redhat.com> - 1.91.0-1
- 1.91.0

* Wed Sep 29 2010 Matthias Clasen <mclasen@redhat.com> - 0.4.0-1
- 0.4.0

* Tue Aug 31 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.91-1
- 0.3.91

* Wed Aug 18 2010 Matthias Clasen <mclasen@redhat.com> - 0.3.90-1
- 0.3.90

* Wed Jul 28 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-2
- dist-git conversion

* Tue Jun 29 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.3.4-1
- 0.3.4

* Wed Jun 09 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.3.3-1
- 0.3.3

* Wed Jun 02 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.3.2-3
- Don't relocate the dbus a11y stack

* Fri May 28 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.3.2-2
- add bug ref

* Fri May 28 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.3.2-1
- 0.3.2

* Sun May 16 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.3.1-1
- 0.3.1

* Wed Mar 31 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.1.8-2
- fix linking

* Wed Mar 31 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.1.8-1
- 0.1.8

* Sun Feb 21 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.1.7-2
- fix spec

* Sun Feb 21 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.1.7-1
- 0.1.7

* Wed Feb 10 2010 Tomas Bzatek <tbzatek@fedoraproject.org> - 0.1.6-1
- Update to 0.1.6

* Wed Jan 20 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.1.5-2
- report dbus daemon location

* Sun Jan 17 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.1.5-1
- 0.1.5

* Mon Jan 04 2010 Matthias Clasen <mclasen@fedoraproject.org> - 0.1.4-1
- initial import
## END: Generated by rpmautospec
