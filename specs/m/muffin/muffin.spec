# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 4b87bf9e647f26136a86b7cf15c9a8db0d313226
%global date 20231107
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

Name:          muffin
Version:       6.4.1
Release: 4%{?dist}
Summary:       Window and compositing manager based on Clutter

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:       GPL-2.0-or-later
URL:           https://github.com/linuxmint/%{name}
%if 0%{?tag:1}
Source0:       %url/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0:       %url/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif
Patch0:        libinput.patch

ExcludeArch:   %{ix86}

BuildRequires: meson
BuildRequires: gcc
BuildRequires: cvt
BuildRequires: pkgconfig(graphene-gobject-1.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(gdk-pixbuf-2.0)
BuildRequires: pkgconfig(pango)
BuildRequires: pkgconfig(cairo)
BuildRequires: pkgconfig(cairo-gobject)
BuildRequires: pkgconfig(pangocairo)
BuildRequires: pkgconfig(fribidi)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gmodule-no-export-2.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(cinnamon-desktop) >= 6.2.0
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xkeyboard-config)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbcommon-x11)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(x11-xcb)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xcb-randr)
BuildRequires: pkgconfig(xcb-res)
BuildRequires: pkgconfig(xinerama)
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(ice)
BuildRequires: pkgconfig(atk)
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(xwayland)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(gl)
BuildRequires: mesa-libEGL-devel
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libinput)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(libpipewire-0.3)
BuildRequires: pkgconfig(libwacom)
BuildRequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(pangoft2)
BuildRequires: zenity

Requires: dbus-x11
Requires: zenity
Recommends: xorg-x11-server-Xwayland

%description
Muffin is a window and compositing manager that displays and manages
your desktop via OpenGL. Muffin combines a sophisticated display engine
using the Clutter toolkit with solid window-management logic inherited
from the Metacity window manager.

Muffin is very extensible via plugins, which
are used both to add fancy visual effects and to rework the window
management behaviors to meet the needs of the environment.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: mesa-libEGL-devel


%description devel
Header files and libraries for developing Muffin plugins. Also includes
utilities for testing Metacity/Muffin themes.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

%build
%meson \
 -Degl_device=true
%meson_build

%install
%meson_install

rm -rf %{buildroot}%{_bindir}/
rm -rf %{buildroot}%{_mandir}/man1/
rm -rf %{buildroot}%{_datadir}/applications/

%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%doc README.md NEWS
%license COPYING
%{_libdir}/libmuffin.so.*
%{_libdir}/muffin/
%{_libexecdir}/muffin-restart-helper
%exclude %{_libdir}/muffin/*.gir
%{_datadir}/glib-2.0/schemas/org.cinnamon.muffin.*.xml

%files devel
%{_includedir}/muffin/
%{_libdir}/libmuffin.so
%{_libdir}/muffin/*.gir
%{_libdir}/pkgconfig/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 02 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.1-1
- Update t0 6.4.1

* Tue Nov 26 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.0-1
- Update to 6.4.0

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 6.2.0-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-1
- Update to 6.2.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.1-3
- Fix compile issue

* Sun Jan 07 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.1-2
- Fix f38 build issue

* Thu Dec 28 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.1-1
- Update to 6.0.1 release

* Mon Dec 04 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.0-2
- Drop eglstreams support

* Sun Nov 19 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.0-1
- Update to 6.0.0 release

* Wed Nov 08 2023 Leigh Scott <leigh123linux@gmail.com> - 5.9.0-1.20231107git4b87bf9
- Update to git snapshot

* Mon Jul 24 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.1-1
- Update to 5.8.1 release

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 02 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.0-1
- Update to 5.8.0 release

* Thu May 18 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.4-4
- Fix the last commit

* Thu May 18 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.4-3
- Patch to fix issue with new libinput on f38+

* Sat May 06 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.4-2
- Patch to fix issue with new zenity on f38+

* Fri Mar 17 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.4-1
- Update to 5.6.4 release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 08 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.3-1
- Update to 5.6.3 release

* Tue Dec 13 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.2-1
- Update to 5.6.2 release

* Wed Nov 30 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.1-1
- Update to 5.6.1 release

* Mon Nov 28 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.0-2
- Readd lost window placement modes

* Fri Nov 18 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.0-1
- Update to 5.6.0 release

* Tue Sep 06 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.7-1
- Update to 5.4.7 release

* Thu Sep 01 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.6-2
- Remove muffin binary

* Sun Aug 21 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.6-1
- Update to 5.4.6 release

* Tue Aug 02 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.5-1
- Update to 5.4.5 release

* Mon Jul 25 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.4-1
- Update to 5.4.4 release

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.3-1
- Update to 5.4.3 release

* Sun Jul 17 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.2-1
- Update to 5.4.2 release

* Mon Jun 20 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.1-1
- Update to 5.4.1 release

* Sat Jun 11 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-3
- Clean up

* Sat Jun 11 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-2
- Add requires mesa-libEGL-devel to devel sub-package

* Fri Jun 10 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-1
- Update to 5.4.0 release

* Sat May 28 2022 Leigh Scott <leigh123linux@gmail.com> - 5.2.1-1
- Update to 5.2.1 release

* Sun Feb 13 2022 Jeff Law <jeffreyalaw@gmail.com> - 5.2.0-3
- Re-enable LTO

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 19 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.0-1
- Update to 5.2.0 release

* Thu Nov 04 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.2-1
- Update to 5.0.2 release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 12 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.1-1
- Update to 5.0.1 release

* Fri May 28 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.0-1
- Update to 5.0.0 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.1-1
- Update to 4.8.1 release

* Thu Nov 26 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.0-1
- Update to 4.8.0 release

* Tue Aug 11 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.3-1
- Update to 4.6.3 release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 4.6.2-2
- Disable LTO

* Sat Jun 06 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.2-1
- Update to 4.6.2 release

* Wed May 27 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.1-1
- Update to 4.6.1 release

* Wed May 13 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.0-1
- Update to 4.6.0 release

* Mon May 11 2020 Leigh Scott <leigh123linux@gmail.com> - 4.4.3-1
- New upstream release 4.4.3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.2-1
- Update to 4.4.2 release

* Fri Nov 22 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.1-1
- Update to 4.4.1 release

* Thu Nov 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-4
- Add upstream fixes for reverted commits

* Thu Nov 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-3
- Revert another bad commit

* Thu Nov 21 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-2
- Revert bad commit

* Wed Nov 20 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-1
- Update to 4.4.0 release

* Tue Oct 01 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.2-2
- Remove --warn-error from gir scannerflags

* Wed Jul 31 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.2-1
- Update to 4.2.2 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.1-1
- Update to 4.2.1 release

* Sat Jul 06 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-3
- Revert last commit

* Sat Jul 06 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-2
- Add upstream pull request

* Fri Jun 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-1
- Update to 4.2.0 release

* Wed Jun 12 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.6.20190611git6b11adb
- Update snapshot

* Wed Jun 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.5.20190604git5774eb2
- Add upstream pull request #514

* Wed Jun 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.4.20190604git5774eb2
- Update snapshot

* Wed Apr 17 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.3.20190417gitc72054b
- Update snapshot

* Tue Apr 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.2.20190416gitb625cfb
- Update snapshot

* Fri Apr 05 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.8-0.1.20190405git462a534
- Update to git master snapshot

* Wed Apr 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.7-1
- Update to 4.0.7 release

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.6-1
- Update to 4.0.6 release

* Sun Dec 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.5-1
- Update to 4.0.5 release

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.4-1
- Update to 4.0.4 release

* Wed Nov 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.3-1
- Update to 4.0.3 release

* Tue Nov 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.2-1
- Update to 4.0.2 release

* Mon Nov 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.1-1
- Update to 4.0.1 release

* Sat Nov 03 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.0-1
- Update to 4.0.0 release
- Readd muffin binary, useful for debug only

