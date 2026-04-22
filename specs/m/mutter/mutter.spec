## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global glib_version 2.81.1
%global gobject_introspection_version 1.41.4
%global gtk3_version 3.19.8
%global gtk4_version 4.14.0
%global gsettings_desktop_schemas_version 47~beta
%global libdrm_version 2.4.118
%global libinput_version 1.27.0
%global pixman_version 0.42
%global pipewire_version 1.2.7
%global lcms2_version 2.6
%global colord_version 1.4.5
%global libei_version 1.3.901
%global mutter_api_version 17
%global wayland_protocols_version 1.45
%global wayland_server_version 1.24

%global major_version %%(echo %{version} | cut -d '.' -f1 | cut -d '~' -f 1)
%global tarball_version %%(echo %{version} | tr '~' '.')

Name:          mutter
Version:       49.4
Release:       %autorelease
Summary:       Window and compositing manager based on Clutter

# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:       GPL-2.0-or-later
URL:           http://www.gnome.org
Source0:       http://download.gnome.org/sources/%{name}/%{major_version}/%{name}-%{tarball_version}.tar.xz

# https://pagure.io/fedora-workstation/issue/357
Source1:       org.gnome.mutter.fedora.gschema.override

# https://bugzilla.redhat.com/show_bug.cgi?id=1936991
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/4786
Patch:         mutter-42.alpha-disable-tegra.patch

BuildRequires: cvt
BuildRequires: desktop-file-utils
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: pam-devel
BuildRequires: pkgconfig(bash-completion)
BuildRequires: pkgconfig(colord) >= %{colord_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib_version}
BuildRequires: pkgconfig(gobject-introspection-1.0) >= %{gobject_introspection_version}
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(lcms2) >= %{lcms2_version}
BuildRequires: pkgconfig(libadwaita-1)
BuildRequires: pkgconfig(libwacom)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(graphene-gobject-1.0)
BuildRequires: pkgconfig(libdisplay-info)
BuildRequires: pkgconfig(libpipewire-0.3) >= %{pipewire_version}
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(umockdev-1.0)
BuildRequires: python3-argcomplete
BuildRequires: python3-docutils
# Bootstrap requirements
BuildRequires: gettext-devel git-core
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(gsettings-desktop-schemas) >= %{gsettings_desktop_schemas_version}
BuildRequires: pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires: pkgconfig(gnome-settings-daemon)
BuildRequires: meson
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(glycin-2)
BuildRequires: pkgconfig(gnome-desktop-4)
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(libdrm) >= %{libdrm_version}
BuildRequires: pkgconfig(libei-1.0) >= %{libei_version}
BuildRequires: pkgconfig(libeis-1.0) >= %{libei_version}
BuildRequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires: pkgconfig(wayland-server) >= %{wayland_server_version}
BuildRequires: sysprof-devel

BuildRequires: pkgconfig(libinput) >= %{libinput_version}
BuildRequires: pkgconfig(pixman-1) >= %{pixman_version}
BuildRequires: pkgconfig(xwayland)

BuildRequires: python3-dbusmock

Requires: control-center-filesystem
Requires: glib2%{?_isa} >= %{glib_version}
Requires: gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires: gnome-settings-daemon
Requires: gtk4%{?_isa} >= %{gtk4_version}
Requires: libeis%{?_isa} >= %{libei_version}
Requires: libinput%{?_isa} >= %{libinput_version}
Requires: pipewire%{_isa} >= %{pipewire_version}
Requires: startup-notification
Requires: dbus
Requires: python3-argcomplete

# Need common
Requires: %{name}-common = %{version}-%{release}

Recommends: mesa-dri-drivers%{?_isa}

Provides: firstboot(windowmanager) = mutter

# Cogl and Clutter were forked at these versions, but have diverged
# significantly since then.
Provides: bundled(cogl) = 1.22.0
Provides: bundled(clutter) = 1.26.0

Conflicts: mutter < 45~beta.1-2

# Make sure dnf updates gnome-shell together with this package; otherwise we
# might end up with broken gnome-shell installations due to mutter ABI changes.
Conflicts: gnome-shell < 45~rc

%description
Mutter is a window and compositing manager that displays and manages
your desktop via OpenGL. Mutter combines a sophisticated display engine
using the Clutter toolkit with solid window-management logic inherited
from the Metacity window manager.

While Mutter can be used stand-alone, it is primarily intended to be
used as the display core of a larger system such as GNOME Shell. For
this reason, Mutter is very extensible via plugins, which are used both
to add fancy visual effects and to rework the window management
behaviors to meet the needs of the environment.

%package common
Summary: Common files used by %{name} and forks of %{name}
BuildArch: noarch
Conflicts: mutter < 45~beta.1-2

%description common
Common files used by Mutter and soft forks of Mutter

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libei%{?_isa} >= %{libei_version}
# for EGL/eglmesaext.h that's included from public cogl-egl-defines.h header
Requires: mesa-libEGL-devel

%description devel
Header files and libraries for developing Mutter plugins. Also includes
utilities for testing Metacity/Mutter themes.

%package  tests
Summary:  Tests for the %{name} package
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: libei%{?_isa} >= %{libei_version}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -S git -n %{name}-%{tarball_version}

%build
%meson -Degl_device=true
%meson_build

%install
%meson_install
install -p %{SOURCE1} %{buildroot}%{_datadir}/glib-2.0/schemas

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc NEWS
%{_bindir}/gdctl
%{_bindir}/gnome-service-client
%{_bindir}/mutter
%{_datadir}/polkit-1/actions/org.gnome.mutter.*.policy
%{_libdir}/lib*.so.*
%{_libdir}/mutter-%{mutter_api_version}/
%exclude %{_libdir}/mutter-%{mutter_api_version}/*.gir
%{_libexecdir}/mutter-backlight-helper
%{_libexecdir}/mutter-x11-frames
%{_mandir}/man1/mutter.1*
%{_mandir}/man1/gdctl.1*
%{_mandir}/man1/gnome-service-client.1*
%{bash_completions_dir}/gdctl

%files common
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.fedora.gschema.override
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.wayland.gschema.xml
%{_datadir}/gnome-control-center/keybindings/50-mutter-*.xml
%{_udevrulesdir}/61-mutter.rules

%files devel
%{_datadir}/applications/org.gnome.Mutter.Mdk.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.devkit.gschema.xml
%{_datadir}/icons/hicolor/*/apps/org.gnome.Mutter.Mdk*
%{_includedir}/mutter-%{mutter_api_version}/
%{_libdir}/lib*.so
%{_libdir}/mutter-%{mutter_api_version}/*.gir
%{_libdir}/pkgconfig/*
%{_libexecdir}/mutter-devkit

%files tests
%{_datadir}/installed-tests/mutter-%{mutter_api_version}
%{_datadir}/mutter-%{mutter_api_version}/tests
%{_libexecdir}/installed-tests/mutter-%{mutter_api_version}

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 49.4-2
- Latest state for mutter

* Wed Feb 11 2026 nmontero <nmontero@redhat.com> - 49.4-1
- Update to 49.4

* Thu Jan 22 2026 Barry Dunn <badunn@redhat.com> - 49.3-1
- Update to 49.3

* Thu Nov 27 2025 Adam Williamson <awilliam@redhat.com> - 49.2-2
- Fix libeis dep - it had a stray ) which made it unsolvable

* Thu Nov 27 2025 Debarshi Ray <rishi@fedoraproject.org> - 49.2-1
- Update to 49.2

* Thu Nov 27 2025 Debarshi Ray <rishi@fedoraproject.org> - 49.1.1-14
- Include the *.gir files in only the devel sub-package & exclude the main

* Wed Nov 26 2025 Jonas Ådahl <jadahl@gmail.com> - 49.1.1-9
- Require libei and libeis

* Wed Nov 26 2025 Debarshi Ray <rishi@fedoraproject.org> - 49.1.1-8
- Require GLib 2.81.1

* Wed Nov 26 2025 Debarshi Ray <rishi@fedoraproject.org> - 49.1.1-5
- Require libinput 1.27.0

* Wed Nov 26 2025 Debarshi Ray <rishi@fedoraproject.org> - 49.1.1-3
- Require GTK4 4.14.0 and PipeWire 1.2.7

* Thu Oct 23 2025 Petr Schindler <pschindl@redhat.com> - 49.1.1-1
- Update to 49.1.1

* Thu Oct 16 2025 Petr Schindler <pschindl@redhat.com> - 49.1-1
- Update to 49.1

* Fri Sep 26 2025 Adam Williamson <awilliam@redhat.com> - 49.0-4
- Backport MR #4675 to fix Chrome tab drag issue (#2397256)

* Thu Sep 25 2025 Adam Williamson <awilliam@redhat.com> - 49.0-2
- Backport MR #4667 to fix a keyboard focus issue (#2395731)

* Tue Sep 16 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49.0-1
- Update to 49.0

* Thu Sep 04 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49~rc-3
- Add missing dependency on glycin-2

* Thu Sep 04 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49~rc-2
- Bring back mutter devkit

* Thu Sep 04 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 49~rc-1
- Update to 49.rc

* Tue Sep 02 2025 Fxzx micah <fxzxmicah@outlook.com> - 49~beta-3
- Move the .gir files to the devel package

* Tue Sep 02 2025 Fxzx micah <fxzxmicah@outlook.com> - 49~beta-2
- Move gdctl bash-completion

* Sun Aug 03 2025 Florian Müllner <fmuellner@redhat.com> - 49~beta-1
- Update to 49.beta

* Tue Jul 29 2025 Adam Williamson <awilliam@redhat.com> - 49~alpha.1-3
- Backport MR #4550 to fix crash when locking screen on VM

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 49~alpha.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Milan Crha <mcrha@redhat.com> - 49~alpha.1-1
- Update to 49.alpha.1

* Thu Jun 19 2025 Carlos Garnacho <cgarnach@redhat.com> - 49~alpha.0-1
- Update to 49~alpha.0

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 48.3-4
- Rebuilt for Python 3.14

* Sun Jun 01 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 48.3-3
- Fix window tracker regression

* Thu May 29 2025 Neal Gompa <ngompa@fedoraproject.org> - 48.3-2
- Disable X11 for Fedora 43+ and RHEL

* Mon May 26 2025 nmontero <nmontero@redhat.com> - 48.3-1
- Update to 48.3

* Sun May 18 2025 Michel Lind <salimma@fedoraproject.org> - 48.2-4
- Disable X11 when building for EL10+

* Fri May 16 2025 Adam Williamson <awilliam@redhat.com> - 48.2-2
- Drop workaround for 2239128

* Mon Apr 14 2025 nmontero <nmontero@redhat.com> - 48.2-1
- Update to 48.2

* Tue Apr 01 2025 nmontero <nmontero@redhat.com> - 48.1-1
- Update to 48.1

* Mon Mar 17 2025 nmontero <nmontero@redhat.com> - 48.0-1
- Update to 48.0

* Tue Mar 11 2025 nmontero <nmontero@redhat.com> - 48~rc-6
- Add patch schedule_process.patch

* Mon Mar 10 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 48~rc-4
- Just kidding, remove cursor shape patch

* Mon Mar 10 2025 Michael Catanzaro <mcatanzaro@redhat.com> - 48~rc-3
- Add patch to fix cursor shape crashes...

* Thu Mar 06 2025 nmontero <nmontero@redhat.com> - 48~rc-2
- Rebuild

* Thu Mar 06 2025 nmontero <nmontero@redhat.com> - 48~rc-1
- Update to 48~rc

* Mon Feb 10 2025 nmontero <nmontero@redhat.com> - 48~beta-1
- Update to 48~beta

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 48~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 13 2025 Florian Müllner <fmuellner@redhat.com> - 48~alpha-1
- Update to 48.alpha

* Mon Jan 13 2025 nmontero <nmontero@redhat.com> - 47.4-1
- Update to 47.4

* Fri Dec 06 2024 Florian Müllner <fmuellner@redhat.com> - 47.3-1
- Update to 47.3

* Fri Nov 29 2024 Simone Caronni <negativo17@gmail.com> - 47.2-2
- Drop EGLStream support

* Mon Nov 25 2024 Florian Müllner <fmuellner@redhat.com> - 47.2-1
- Update to 47.2

* Thu Oct 31 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 47.1-3
- Remove dependency on Xvfb

* Wed Oct 30 2024 Teoh Han Hui <teohhanhui@gmail.com> - 47.1-2
- Backport MR #4099 to fix cursor positioning

* Fri Oct 18 2024 Florian Müllner <fmuellner@redhat.com> - 47.1-1
- Update to 47.1

* Thu Sep 26 2024 Neal Gompa <ngompa@fedoraproject.org> - 47.0-2
- Enable xwayland-native scaling for complete fractional scaling support

* Sat Sep 14 2024 Florian Müllner <fmuellner@redhat.com> - 47.0-1
- Update to 47.0

* Thu Sep 05 2024 Florian Müllner <fmuellner@redhat.com> - 47~rc-3
- Fix resizing of electron windows

* Tue Sep 03 2024 Florian Müllner <fmuellner@redhat.com> - 47~rc-2
- Bump gsettings-dektop-schema requires

* Sun Sep 01 2024 Florian Müllner <fmuellner@redhat.com> - 47~rc-1
- Update to 47.rc

* Sun Aug 04 2024 Florian Müllner <fmuellner@redhat.com> - 47~beta-1
- Update to 47.beta

* Tue Jul 30 2024 Adam Williamson <awilliam@redhat.com> - 47~alpha-7
- Backport MR #3848 to fix build with libdrm >= 2.4.122

* Tue Jul 30 2024 Adam Williamson <awilliam@redhat.com> - 47~alpha-6
- Backport MR #3860 to fix desktop crash on Fonts flatpak crash

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 47~alpha-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Florian Müllner <fmuellner@redhat.com> - 47~alpha-3
- Rebuild for libdisplay-info soname bump

* Wed Jul 03 2024 Adam Williamson <awilliam@redhat.com> - 47~alpha-2
- Backport MR #3862 to fix anaconda often being invisible

* Sun Jun 30 2024 Florian Müllner <fmuellner@redhat.com> - 47~alpha-1
- Update to 47.alpha

* Tue Jun 11 2024 Florian Müllner <fmuellner@redhat.com> - 46.2-3
- Only depend on cvt

* Sat May 25 2024 Florian Müllner <fmuellner@redhat.com> - 46.2-2
- Update downstream patch

* Sat May 25 2024 Florian Müllner <fmuellner@redhat.com> - 46.2-1
- Update to 46.2

* Thu Apr 25 2024 Adam Williamson <awilliam@redhat.com> - 46.1-3
- Backport MR #3721 to fix popups not displaying in openQA tests

* Sun Apr 21 2024 Florian Müllner <fmuellner@redhat.com> - 46.1-2
- Update downstream patch

* Sun Apr 21 2024 Florian Müllner <fmuellner@redhat.com> - 46.1-1
- Update to 46.1

* Sat Mar 16 2024 Florian Müllner <fmuellner@redhat.com> - 46.0-1
- Update to 46.0

* Sat Mar 16 2024 Florian Müllner <fmuellner@redhat.com> - 46~rc-4
- Use libdisplay-info

* Tue Mar 12 2024 Adam Williamson <awilliam@redhat.com> - 46~rc-2
- Backport MR #3642 to fix mouse wheel scrolling

* Sun Mar 03 2024 Florian Müllner <fmuellner@redhat.com> - 46~rc-1
- Update to 46.rc

* Sun Feb 11 2024 Florian Müllner <fmuellner@gnome.org> - 46~beta-1
- Update to 46.beta

* Thu Feb 08 2024 Adam Williamson <awilliam@redhat.com> - 46~alpha-5
- Backport MR #3539 to fix RHBZ #2261842

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 46~alpha-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 46~alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Florian Müllner <fmuellner@gnome.org> - 46~alpha-2
- Fix i686 build

* Sun Jan 07 2024 Florian Müllner <fmuellner@gnome.org> - 46~alpha-1
- Update to 46.alpha

* Sat Dec 02 2023 Florian Müllner <fmuellner@gnome.org> - 45.2-1
- Update to 45.2

## END: Generated by rpmautospec
