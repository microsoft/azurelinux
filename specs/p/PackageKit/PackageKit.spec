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

%global glib2_version 2.80
%global libdnf_version 0.43.1
%global libdnf5_version 5.2.17.0

# For https://fedoraproject.org/wiki/Changes/PackageKit-DNF5
%bcond dnf5_default %[0%{?fedora} >= 44 || 0%{?rhel} >= 11]
%bcond dnf4 %[(0%{?rhel} && 0%{?rhel} < 11) || (0%{?fedora} && 0%{?fedora} < 44)]

Summary:   Package management service
Name:      PackageKit
Version:   1.3.4
Release:   %autorelease
License:   GPL-2.0-or-later AND LGPL-2.1-or-later AND FSFAP
URL:       http://www.freedesktop.org/software/PackageKit/
Source0:   http://www.freedesktop.org/software/PackageKit/releases/%{name}-%{version}.tar.xz

# Backports from upstream (1~500)
## Fix turning off the Python backend
Patch0001:    https://github.com/PackageKit/PackageKit/commit/11c5f1f34f48b58ee10acec839dd01a31728704b.patch

# Patches proposed upstream (501~1000)
## Alias "dnf" to "dnf5"
## Pulled out from https://github.com/PackageKit/PackageKit/pull/938
Patch0501:    PackageKit-alias-dnf-to-dnf5.patch

# Downstream only patches (1001+)
## https://pagure.io/fedora-workstation/issue/233
## https://github.com/PackageKit/PackageKit/pull/404
Patch1001:    package-inst+rem-sysupgrade-password-prompt.patch

## Fedora patches (2001~3000)
Patch2001:    PackageKit-0.3.8-Fedora-Vendor.conf.patch

## RHEL patches (3001~4000)
Patch3001:    PackageKit-0.3.8-RHEL-Vendor.conf.patch

BuildRequires: docbook-utils
BuildRequires: docbook5-schemas
BuildRequires: docbook5-style-xsl
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: meson
BuildRequires: vala
BuildRequires: xmlto
BuildRequires: pkgconfig(bash-completion)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(jansson)
BuildRequires: pkgconfig(libdnf5) >= %{libdnf5_version}
BuildRequires: pkgconfig(libsystemd)
BuildRequires: pkgconfig(pangoft2)
BuildRequires: pkgconfig(ply-boot-client)
BuildRequires: pkgconfig(polkit-gobject-1) >= 0.114
BuildRequires: pkgconfig(sdbus-c++)
BuildRequires: pkgconfig(sqlite3)
BuildRequires: systemd
BuildRequires: python3-devel

%if %{with dnf4}
BuildRequires: pkgconfig(appstream)
BuildRequires: pkgconfig(libdnf) >= %{libdnf_version}
Requires: libdnf%{?_isa} >= %{libdnf_version}
%endif

# Validate metainfo
BuildRequires: libappstream-glib

Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: shared-mime-info
Requires: systemd

# functionality moved to udev itself
Obsoletes: PackageKit-udev-helper < %{version}-%{release}
Obsoletes: udev-packagekit < %{version}-%{release}

# No more GTK+-2 plugin
Obsoletes: PackageKit-gtk-module < %{version}-%{release}

# No more zif, smart or yum in Fedora
Obsoletes: PackageKit-smart < %{version}-%{release}
Obsoletes: PackageKit-yum < 0.9.1
Obsoletes: PackageKit-yum-plugin < 0.9.1
Obsoletes: PackageKit-zif < 0.8.13-2

# components now built-in
Obsoletes: PackageKit-debug-install < 0.9.1
Obsoletes: PackageKit-hawkey < 0.9.1
Obsoletes: PackageKit-backend-devel < 0.9.6

# Udev no longer provides this functionality
Obsoletes: PackageKit-device-rebind < 0.8.13-2

%if ! %{with dnf4}
# No longer needed since we don't support DNF4
Obsoletes: dnf4-plugin-notify-PackageKit < %{version}-%{release}
# No longer needed since we don't support DNF4+DNF5
Obsoletes: libdnf5-plugin-notify-PackageKit < %{version}-%{release}
%endif

%if %{with dnf5_default}
Requires: libdnf5%{?_isa} >= %{libdnf5_version}
# Ensure AppStream repodata is processed
Requires: libdnf5-plugin-appstream%{?_isa}
# DNF5 backend is now built-in
Obsoletes: PackageKit-backend-dnf5 < %{version}-%{release}
Provides: PackageKit-backend-dnf5 = %{version}-%{release}
Provides: PackageKit-backend-dnf5%{?_isa} = %{version}-%{release}
Provides: PackageKit-dnf5 = %{version}-%{release}
Provides: PackageKit-dnf5%{?_isa} = %{version}-%{release}
%endif

%description
PackageKit is a D-Bus abstraction layer that allows the session user
to manage packages in a secure way using a cross-distro,
cross-architecture API.

%if ! %{with dnf5_default}
%package backend-dnf5
Summary: DNF5 backend for PackageKit
%dnl Supplements: (libdnf5%{?_isa} and PackageKit%{?_isa})
Provides: %{name}-dnf5 = %{version}-%{release}
Provides: %{name}-dnf5%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libdnf5%{?_isa} >= %{libdnf5_version}
# Ensure AppStream repodata is processed
Requires: libdnf5-plugin-appstream%{?_isa}

%description backend-dnf5
PackageKit is a D-Bus abstraction layer that allows the session user
to manage packages in a secure way using a cross-distro,
cross-architecture API.

This package provides the DNF5 backend for PackageKit.
%endif

%if %{with dnf4}
%package -n dnf4-plugin-notify-PackageKit
Summary: DNF4 plugin to notify PackageKit of DNF4 actions
Supplements: (dnf4 and PackageKit)
Conflicts: %{name} < 1.3.1-3
BuildArch: noarch

%description -n dnf4-plugin-notify-PackageKit
DNF4 plugin to notify PackageKit of DNF4 actions.

%package -n libdnf5-plugin-notify-PackageKit
Summary: DNF5 plugin to notify PackageKit of DNF5 actions
Supplements: (libdnf5%{?_isa} and PackageKit%{?_isa})
Conflicts: %{name} < 1.3.1-2

%description -n libdnf5-plugin-notify-PackageKit
DNF5 plugin to notify PackageKit of DNF5 actions.
%endif

%package glib
Summary: GLib libraries for accessing PackageKit
Requires: dbus >= 1.1.1
Requires: glib2 >= %{glib2_version}
Obsoletes: PackageKit-libs < %{version}-%{release}
Provides: PackageKit-libs = %{version}-%{release}

%description glib
GLib libraries for accessing PackageKit.

%package cron
Summary: Cron job and related utilities for PackageKit
Requires: crontabs
Requires: %{name}%{?_isa} = %{version}-%{release}

%description cron
Crontab and utilities for running PackageKit as a cron job.

%package devel
Summary: Libraries and headers for PackageKit
Requires: %{name}-glib-devel%{?_isa} = %{version}-%{release}
# Additional deps needed for multilibs computation.
# Needed for (gtk3-module & gstreamer-plugin), see also rhbz#1901065
Requires: %{name}-gtk3-module%{?_isa} = %{version}-%{release}
Requires: %{name}-gstreamer-plugin%{?_isa} = %{version}-%{release}

%description devel
Headers and libraries for PackageKit.

%package glib-devel
Summary: GLib Libraries and headers for PackageKit
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Requires: dbus-devel%{?_isa} >= 1.1.1
Requires: sqlite-devel%{?_isa}
Obsoletes: PackageKit-docs < %{version}-%{release}
Provides: PackageKit-docs = %{version}-%{release}

%description glib-devel
GLib headers and libraries for PackageKit.

%package gstreamer-plugin
Summary: Install GStreamer codecs using PackageKit
Requires: %{name}-glib%{?_isa} = %{version}-%{release}
Obsoletes: codeina < 0.10.1-10
Provides: codeina = 0.10.1-10

%description gstreamer-plugin
The PackageKit GStreamer plugin allows any Gstreamer application to install
codecs from configured repositories using PackageKit.

%package gtk3-module
Summary: Install fonts automatically using PackageKit
Requires: pango
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

%description gtk3-module
The PackageKit GTK3+ module allows any Pango application to install
fonts from configured repositories using PackageKit.

%package command-not-found
Summary: Ask the user to install command line programs automatically
Requires: bash
Requires: %{name} = %{version}-%{release}
Requires: %{name}-glib%{?_isa} = %{version}-%{release}

%description command-not-found
A simple helper that offers to install new packages on the command line
using PackageKit.

%prep
%autosetup -N

# Fun patching times :)
%autopatch -p1 -M 2000
%if 0%{?fedora}
%autopatch -p1 -m 2001 -M 3000
%elif 0%{?rhel}
%autopatch -p1 -m 3001 -M 4000
%endif

# Revert dnf->dnf5 for <F43 and <EL11
%if ! %{with dnf5_default}
%patch -p1 -P 501 -R
%endif


%conf
%meson \
        -Dgtk_doc=true \
        -Dpython_backend=false \
        -Dpackaging_backend=%{?with_dnf4:dnf,}dnf5 \
        -Dlegacy_tools=true \
        -Dlocal_checkout=false

%build
%meson_build

%install
%meson_install

# Create cache dir
mkdir -p %{buildroot}%{_localstatedir}/cache/PackageKit

%if %{with dnf4}
# Create directories for downloaded appstream data
mkdir -p %{buildroot}%{_localstatedir}/cache/app-info/{icons,xmls}
%endif

# create a link that GStreamer will recognize
pushd %{buildroot}%{_libexecdir} > /dev/null
ln -s pk-gstreamer-install gst-install-plugins-helper
popd > /dev/null

%find_lang %{name}

%check
# FIXME: Validation fails in appstream-util because it does not recognize component type "service"
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml || :

%post
# Remove leftover symlinks from /etc/systemd; the offline update service is
# instead now hooked into /usr/lib/systemd/system/system-update.target.wants
systemctl disable packagekit-offline-update.service > /dev/null 2>&1 || :

%files -f %{name}.lang
%license COPYING
%doc README.md AUTHORS NEWS
%dir %{_datadir}/PackageKit
%dir %{_sysconfdir}/PackageKit
%dir %{_localstatedir}/lib/PackageKit
%if %{with dnf4}
%dir %{_localstatedir}/cache/app-info
%dir %{_localstatedir}/cache/app-info/icons
%dir %{_localstatedir}/cache/app-info/xmls
%endif
%dir %{_localstatedir}/cache/PackageKit
%{_datadir}/bash-completion/completions/pkcon
%{_datadir}/bash-completion/completions/pkgcli
%dir %{_libdir}/packagekit-backend
%config(noreplace) %{_sysconfdir}/PackageKit/PackageKit.conf
%config(noreplace) %{_sysconfdir}/PackageKit/Vendor.conf
%{_datadir}/man/man1/pkgcli.1*
%{_datadir}/man/man1/pkcon.1*
%{_datadir}/man/man1/pkmon.1*
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/polkit-1/rules.d/*
%{_datadir}/PackageKit/pk-upgrade-distro.sh
%{_datadir}/PackageKit/helpers/test_spawn/search-name.sh
%{_metainfodir}/org.freedesktop.packagekit.metainfo.xml
%{_libexecdir}/packagekitd
%{_libexecdir}/packagekit-direct
%{_bindir}/pkgcli
%{_bindir}/pkmon
%{_bindir}/pkcon
%exclude %{_libdir}/libpackagekit*.so.*
%{_libdir}/packagekit-backend/libpk_backend_dummy.so
%{_libdir}/packagekit-backend/libpk_backend_test_*.so
%ghost %verify(not md5 size mtime) %attr(0644,-,-) %{_localstatedir}/lib/PackageKit/transactions.db
%{_datadir}/dbus-1/system.d/*
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/interfaces/*.xml
%{_unitdir}/packagekit-offline-update.service
%{_unitdir}/packagekit.service
%{_unitdir}/system-update.target.wants/
%{_libexecdir}/pk-*offline-update
%if %{with dnf4}
%{_libexecdir}/packagekit-dnf-refresh-repo
%{_libdir}/packagekit-backend/libpk_backend_dnf.so
%endif
%if %{with dnf5_default}
%{_libdir}/packagekit-backend/libpk_backend_dnf5.so
%{_libdir}/rpm-plugins/notify_packagekit.so
%{_rpmmacrodir}/macros.transaction_notify_packagekit
%endif

%if ! %{with dnf5_default}
%files backend-dnf5
%{_libdir}/packagekit-backend/libpk_backend_dnf5.so
%{_libdir}/rpm-plugins/notify_packagekit.so
%{_rpmmacrodir}/macros.transaction_notify_packagekit
%endif

%if %{with dnf4}
%files -n dnf4-plugin-notify-PackageKit
%pycached %{python3_sitelib}/dnf-plugins/notify_packagekit.py

%files -n libdnf5-plugin-notify-PackageKit
%{_libdir}/libdnf5/plugins/notify_packagekit.so
%config(noreplace) %{_sysconfdir}/dnf/libdnf5-plugins/notify_packagekit.conf
%endif

%files glib
%{_libdir}/*packagekit-glib2.so.*
%{_libdir}/girepository-1.0/PackageKitGlib-1.0.typelib

%files cron
%config %{_sysconfdir}/cron.daily/packagekit-background.cron
%config(noreplace) %{_sysconfdir}/sysconfig/packagekit-background

%files gstreamer-plugin
%{_libexecdir}/pk-gstreamer-install
%{_libexecdir}/gst-install-plugins-helper

%files gtk3-module
%{_libdir}/gtk-3.0/modules/*.so
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/*.desktop

%files command-not-found
%{_sysconfdir}/profile.d/*
%{_libexecdir}/pk-command-not-found
%config(noreplace) %{_sysconfdir}/PackageKit/CommandNotFound.conf

%files devel
# Empty on purpose
# helper for multilibs computation - See rhbz#1901065

%files glib-devel
%{_libdir}/libpackagekit-glib2.so
%{_libdir}/pkgconfig/packagekit-glib2.pc
%dir %{_includedir}/PackageKit
%dir %{_includedir}/PackageKit/packagekit-glib2
%{_includedir}/PackageKit/packagekit-glib*/*.h
%{_datadir}/gir-1.0/PackageKitGlib-1.0.gir
%{_datadir}/gtk-doc/html/PackageKit
%{_datadir}/vala/vapi/packagekit-glib2.vapi
%{_datadir}/vala/vapi/packagekit-glib2.deps

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.3.4-2
- Latest state for PackageKit

* Mon Feb 23 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4 and drop merged patches

* Fri Jan 23 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-16
- Switch to DNF5 by default on F44+ and drop DNF4 backend

* Fri Jan 23 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-15
- Add patch to alias dnf backend to dnf5 backend

* Fri Jan 23 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-14
- Refresh DNF5 backend patch with merged version

* Tue Jan 20 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-13
- Refresh DNF5 backend patch with latest revision

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jan 08 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-10
- Refresh DNF5 backend patch with fixes and RPM transaction awareness

* Thu Jan 08 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-9
- Backport fixes for GNOME Software crashes (rhbz#2422976)

* Sat Jan 03 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-8
- Refresh DNF5 backend patch to support context invalidation

* Fri Jan 02 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-7
- Fix DNF backend runtime dependencies

* Thu Jan 01 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-6
- Build legacy DNF backend for RHEL < 10 and only ship DNF5 backend for
  RHEL 11+

* Thu Jan 01 2026 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-5
- Add DNF5 backend and build as a subpackage

* Sun Dec 14 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-4
- Backport support for DependsOn/RequiredBy for dnf

* Wed Dec 03 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-3
- Drop gobject-introspection dep and raise to glib2 >= 2.80

* Sun Nov 30 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-2
- Add missing build dependency for offline-updates and build new pkgctl
  client

* Sun Nov 30 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.3-1
- Rebase to version 1.3.3 (rhbz#2401193)

* Fri Sep 26 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.1-6
- Backport fix for linking libdnf5 properly to dnf5 plugin

* Fri Sep 26 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.1-5
- Actually apply patch for notify-PK plugin fixes

* Fri Sep 26 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.1-4
- Backport fixes to avoid DNF5 crashes when PackageKit is installed but not
  running

* Fri Sep 26 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.1-3
- Split DNF4 plugin into its own subpackage

* Thu Sep 25 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.1-2
- Split DNF5 plugin into its own subpackage

* Thu Sep 25 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.3.1-1
- Rebase to version 1.3.1

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.2.8-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Aug 25 2025 Nicolas Chauvet <kwizart@gmail.com> - 1.2.8-13
- Add dependencies for multilibs repository - devel

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.2.8-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.2.8-10
- Rebuilt for Python 3.14

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 03 2024 Alessandro Astone <ales.astone@gmail.com> - 1.2.8-8
- Backport patch to fix system upgrade in KDE Plasma

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.8-6
- Rebuilt for Python 3.13

* Fri May 24 2024 AsciiWolf <mail@asciiwolf.com> - 1.2.8-5
- Mark PackageKit as compulsory in AppStream metadata

* Wed May 15 2024 David King <amigadave@amigadave.com> - 1.2.8-4
- Use pkgconfig for BuildRequires (#2272920)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 30 2023 Alessandro Astone <ales.astone@gmail.com> - 1.2.8-1
- Update to 1.2.8

* Tue Jul 25 2023 Adam Williamson <awilliam@redhat.com> - 1.2.6-11
- Backport PR #643 to fix symbol errors on Rawhide

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.2.6-9
- Rebuilt for Python 3.12

* Fri May 19 2023 Petr Písař <ppisar@redhat.com> - 1.2.6-8
- Rebuild against rpm-4.19
  (https://fedoraproject.org/wiki/Changes/RPM-4.19)

* Wed Feb 22 2023 Richard Hughes <richard@hughsie.com> - 1.2.6-7
- migrated to SPDX license

* Tue Jan 24 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.2.6-6
- Add patches to shut down on idle, including new dnf plugin

* Tue Jan 24 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.2.6-5
- Revert "Add patches to shut down on idle, including new dnf plugin"

* Tue Jan 24 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.2.6-4
- Revert "Avoid creating new -dnf-plugin subpackage"

* Mon Jan 23 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.2.6-3
- Avoid creating new -dnf-plugin subpackage

* Mon Jan 23 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.2.6-2
- Add patches to shut down on idle, including new dnf plugin

* Mon Jan 23 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 1.2.6-1
- Update to 1.2.6

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Feb 17 2022 Richard Hughes <rhughes@redhat.com> - 1.2.5-1
- New upstream release
- Properly handle allow-reinstall flag for installations
- Provide better error message if trying to install an installed package
- Searches by name and package details should be case insensitive
- Update appstream xml files if dnf_sack_add_repos() does the download
- Wait until online to activate systemd service

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 27 2021 Rex Dieter <rdieter@fedoraproject.org> - 1.2.4-3
- own /var/cache/PackageKit (#2016636)

* Fri Sep 10 2021 Adam Williamson <awilliam@redhat.com> - 1.2.4-2
- Backport PR #505 to fix offline upgrading (#2002609)

* Fri Jul 30 2021 Richard Hughes <rhughes@redhat.com> - 1.2.4-1
- New upstream release
- Add specific error code when user declined interaction
- Avoid spurious GObject::notify signal emissions
- Fix a leak on calling set_locale() a second time
- Fix a possible use-after-free under pk_client_cancel_cb()
- Honor install_weak_deps=False
- Improve thread safety on an operation cancellation
- Let the finish understand the 'cancelled' exit code
- Only set polkit interactive flag if method call has too
- Read update information also when getting list of updates
- Use 'hy_query_get_advisory_pkgs', if available

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Michael Catanzaro <mcatanzaro@redhat.com> - 1.2.3-2
- Add package-remove-password-prompt.patch for fedora-workstation#233

* Mon Mar 22 2021 Richard Hughes <rhughes@redhat.com> - 1.2.3-1
- New upstream release
- Add support for coercing upgrade to distupgrade
- Append to cron log instead of overwriting it
- Cancel a transaction if calling Cancel fails or the daemon disappears
- Remove large transaction size sanity check

* Mon Mar 08 2021 Richard Hughes <rhughes@redhat.com> - 1.2.2-5
- Drop unused gnome-doc-utils BR

* Tue Feb 09 2021 Kalev Lember <klember@redhat.com> - 1.2.2-4
- Fix multilib conflicts in generated pk-enum-types.h (#1915259)

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov  9 2020 Vít Ondruch <vondruch@redhat.com> - 1.2.2-2
- Fix crash on login.
  Resolves: rhbz#1836304

* Mon Nov 02 2020 Richard Hughes <rhughes@redhat.com> - 1.2.2-1
- New upstream release
- Notify systemd when beginning to shutdown
- Fix possible information disclosure

* Mon Sep 07 2020 Richard Hughes <rhughes@redhat.com> - 1.2.1-1
- New upstream release
- Actually merge in the PolicyKit translation
- Exit pkcon with retval 5 if no packages needed be installed
- Fix command-not-found handling arguments with spaces
- Fix setting libexecdir for command-not-found helper
- Use SQL statements for queries with input

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 08 2020 Adam Williamson <awilliam@redhat.com> - 1.2.0-3
- Fix packagekit-offline-update.service not being enabled (#1833176)

* Tue May 05 2020 Neal Gompa <ngompa13@gmail.com> - 1.2.0-2
- Clean up and simplify spec
- Fix packaging to work properly with EL8+

* Mon May 04 2020 Richard Hughes <rhughes@redhat.com> - 1.2.0-1
- New upstream release
- Do not do failable actions in constructors
- Load all the repos and vars directories
- Port to the meson build system
- Remove the GTK2 gtk-module support
- Revert "Shutdown the daemon on idle by default"

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Richard Hughes <rhughes@redhat.com> - 1.1.13-1
- New upstream release
- Don't use a bash regex to fix command not found on other shells
- Keep a ref on transaction while doing async polkit call
- Properly mark obsoleted packages when simulating upgrade
- Return directly when its state is going backwards
- Shrink the progress bar to fit when run in small spaces
- Support non-x86 arches in gstreamer helper
- zsh command not found should return the same as its bash equivalent

* Tue Aug 13 2019 Richard Hughes <rhughes@redhat.com> - 1.1.12-12
- Fix rpmdb permission of transaction database file

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 19 2019 Richard Hughes <rhughes@redhat.com> - 1.1.12-10
- Do not trigger an inotity event when the AppStream XML data is unchanged
- Remove the unconditional copy to speed up gnome-software startup.

* Fri Jul 12 2019 Kalev Lember <klember@redhat.com> - 1.1.12-9
- Drop unused comps-extras requires

* Wed Jun 19 2019 Kalev Lember <klember@redhat.com> - 1.1.12-8
- Don't override DnfContext's release_ver for the running system

* Mon Jun 10 22:13:21 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.12-7
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:04 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.12-6
- Rebuild for RPM 4.15

* Mon Mar 04 2019 Kalev Lember <klember@redhat.com> - 1.1.12-5
- Use new plymouth "system-upgrade" and "reboot" modes

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 1.1.12-4
- Update BRs for vala packaging changes

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 18 2018 Kalev Lember <klember@redhat.com> - 1.1.12-2
- Invalidate the sack cache after downloading new metadata (#1642878)

* Wed Nov 28 2018 Kalev Lember <klember@redhat.com> - 1.1.12-1
- Update to 1.1.12

* Tue Sep 25 2018 Richard Hughes <rhughes@redhat.com> - 1.1.11-1
- New upstream release
- Add --autoremove option to pkcon
- De-register callbacks on PkClientHelper finalize
- Don't complain if command-not-found get uninstalled while running
- Never assert when an interactive TTY is not available
- Shut down services cleanly before rebooting after offline updates
- Shutdown the daemon on idle by default

* Sat Sep 22 2018 Adam Williamson <awilliam@redhat.com> - 1.1.10-5
- Backport several more fixes from master for libdnf compat

* Tue Jul 24 2018 Stephen Gallagher <sgallagh@redhat.com> - 1.1.10-4
- Add patch to support modularity

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Adam Williamson <awilliam@redhat.com> - 1.1.10-2
- Rebuild for new libdnf

* Mon Apr 23 2018 Richard Hughes <rhughes@redhat.com> - 1.1.10-1
- New upstream release
- This release fixes CVE-2018-1106 which is a moderate security issue.

* Tue Mar 27 2018 Kalev Lember <klember@redhat.com> - 1.1.9-4
- Remove ldconfig scriptlets

* Thu Mar 22 2018 Kalev Lember <klember@redhat.com> - 1.1.9-3
- Create /var/cache/app-info/{icons,xmls} directories

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 1.1.9-2
- Don't abort on daemon startup for invalid .repo files

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 1.1.9-1
- Update to 1.1.9

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Kalev Lember <klember@redhat.com> - 1.1.8-1
- Update to 1.1.8

* Mon Sep 11 2017 Richard Hughes <rhughes@redhat.com> - 1.1.7-1
- New upstream release
- Add fedora-cisco-openh264 repos to supported repos list
- Add missing context pushes and pops in appstream-glib
- Add the ability to install updates on reboot in PackageKit-cron
- Effectively check for previous proxy entries
- Fix an inverted condition that led to frequent crashes
- Show a different progress message for system upgrades

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.6-7
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.6-6
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.1.6-5
- Rebuilt for RPM soname bump

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 15 2017 Richard Hughes <rhughes@redhat.com> - 1.1.6-2
- Fix a crash when refreshing the metadata cache
- Resolves: #1460825

* Wed Jun 07 2017 Richard Hughes <rhughes@redhat.com> - 1.1.6-1
- New upstream release
- Ensure AppStream is deployed when the repo is updated

* Fri Mar 24 2017 Kalev Lember <klember@redhat.com> - 1.1.5-4
- Fix the offline updater to work with latest systemd (#1430920)

* Fri Mar 17 2017 Kalev Lember <klember@redhat.com> - 1.1.5-3
- Build with system libdnf

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 17 2017 Kalev Lember <klember@redhat.com> - 1.1.5-1
- Update to 1.1.5
- Update to latest libdnf git snapshot (#1398429)

* Wed Dec 21 2016 Kalev Lember <klember@redhat.com> - 1.1.5-0.1.20161221
- Update to latest git snapshot

* Mon Dec 19 2016 Kalev Lember <klember@redhat.com> - 1.1.4-3
- Adapt for libhif->libdnf git repo rename

* Fri Dec 16 2016 Kalev Lember <klember@redhat.com> - 1.1.4-2
- Update to latest libdnf git snapshot (#1383819)

* Mon Sep 19 2016 Richard Hughes <rhughes@redhat.com> - 1.1.4-1
- New upstream release
- Change the configuration of the cron script to a sysconfig-like config
- Don't crash when emitting PropertiesChanged for NULL values
- Fix several small memory leaks
- Look for command-not-found dbus socket in /run instead of /var/run
- Use GetFilesLocal in pkcon get-files if argument is a file

* Thu Sep 08 2016 Kalev Lember <klember@redhat.com> - 1.1.4-0.4.20160901
- Update to latest libdnf git snapshot (#1344643)

* Thu Sep 01 2016 Kalev Lember <klember@redhat.com> - 1.1.4-0.3.20160901
- Update to latest git snapshot

* Wed Aug 31 2016 Kalev Lember <klember@redhat.com> - 1.1.4-0.2.20160825
- Update to latest git snapshot

* Fri Aug 05 2016 Kalev Lember <klember@redhat.com> - 1.1.4-0.1.20160805
- Update to today's git snapshot
- Switch to new libdnf based backend

* Wed Jul 27 2016 Kalev Lember <klember@redhat.com> - 1.1.3-2
- engine: Don't crash when emitting PropertiesChanged for NULL values
  (#1359479)

* Thu Jul 14 2016 Kalev Lember <klember@redhat.com> - 1.1.3-1
- Update to 1.1.3

* Tue Jul 12 2016 Kalev Lember <klember@redhat.com> - 1.1.2-1
- Update to 1.1.2
- Set minimum required glib2 and libhif versions

* Tue Jun 07 2016 Kalev Lember <klember@redhat.com> - 1.1.1-3
- Match unavailable packages for the what-provides query

* Sat May 28 2016 Kalev Lember <klember@redhat.com> - 1.1.1-2
- Require admin authorisation to trigger a distro upgrade (#1335458)

* Wed Apr 20 2016 Richard Hughes <rhughes@redhat.com> - 1.1.1-1
- New upstream release
- Add TriggerUpgrade DBus method handling
- Emit UpdatesChanges when installing packages
- Fix GIR annotations for progress callbacks
- Increase the number of packages that can be resolved
- Point offline update/upgrade trigger to the prepared update
- Set ALLOW_DOWNGRADE flag for all transactions

* Fri Feb 12 2016 Richard Hughes <rhughes@redhat.com> - 1.1.0-1
- New upstream release
- Add support for UpgradeSystem
- Correctly store file descriptor from logind
- Do not crash on GetPrepared when there are no offline updates
- Do not crash on transaction database corruption
- Do not crash when parsing a very broken transaction log
- Port to g_autoptr()
- Relax validation performed on input strings passed to backends
- Remove the PackageKit browser plugin
- Use the GLib network monitoring support

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 27 2015 Richard Hughes <rhughes@redhat.com> - 1.0.11-1
- Add support for HTTP proxy
- Allow the use of variadic functions in vala
- By popular demand, reintroduce the UpgradeSystem method
- Improve RefreshCache progress updates
- New upstream release

* Mon Oct 19 2015 Kalev Lember <klember@redhat.com> - 1.0.10-2
- Remove PackageKit-cached-metadata subpackage

* Mon Sep 21 2015 Richard Hughes <rhughes@redhat.com> - 1.0.10-1
- Update to 1.0.10 to fix a couple of bugs in the offline updater

* Tue Sep 15 2015 Richard Hughes <rhughes@redhat.com> - 1.0.9-1
- New upstream release
- Check the offline action trigger before performing the update
- Fix a race with the backend job thread creation

* Sat Sep 05 2015 Kalev Lember <klember@redhat.com> - 1.0.8-3
- Rebuilt for librpm soname bump

* Thu Aug 20 2015 Kalev Lember <klember@redhat.com> - 1.0.8-2
- Revert "Correctly register enum properties" as this broke offline updates

* Wed Aug 19 2015 Richard Hughes <rhughes@redhat.com> - 1.0.8-1
- New upstream release
- Exit quietly if we didn't prepare the offline update
- Record the UID of the session user in the yumdb

* Fri Aug 14 2015 Kalev Lember <klember@redhat.com> - 1.0.7-3
- Rebuild for new libappstream-glib

* Sun Jul 26 2015 Kevin Fenzi <kevin@scrye.com> 1.0.7-2
- Rebuild for new librpm

* Mon Jul 13 2015 Richard Hughes <rhughes@redhat.com> - 1.0.7-1
- New upstream release
- Correct punctuation while applying offline updates
- Define command_not_found_handler for zsh
- Port GTK+ module to org.freedesktop.PackageKit.Modify2
- Return the correct return codes for syntax errors

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.6-6
- Actually apply the patches

* Mon Jun 08 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.6-5
- Backport a few more upstream patches:
- Add missing locking when accessing sack cache (#1146734)
- Improve parallel kernel installation (#1205649)

* Wed May 20 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.6-4
- Update cached metadata in preparation for F22 release

* Fri May 15 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.6-3
- Revert a commit that inadvertantly changed the default value for the
  TriggerAction DBus property

* Mon May 11 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.6-2
- Update cached metadata

* Tue Apr 07 2015 Richard Hughes <rhughes@redhat.com> - 1.0.6-1
- New upstream release
- Add dbus method for returning prepared packages
- Don't recursive lock the debug mutex when using --verbose without a tty
- Make "reboot" the default action for no action file

* Sat Mar 28 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.5-2
- Backport a crash fix from upstream (#1185544)
- Update cached metadata
- Use license macro for the COPYING file

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.5-1
- Update to 1.0.5
- Backport new missing gstreamer codecs API

* Fri Feb 06 2015 Richard Hughes <rhughes@redhat.com> - 1.0.4-2
- Adapt to the new hawkey API.

* Mon Jan 19 2015 Richard Hughes <rhughes@redhat.com> - 1.0.4-1
- New upstream release
- Actually inhibit logind when the transaction can't be cancelled
- Add 'quit' command to pkcon
- Automatically import metadata public keys when safe to do so
- Automatically install AppStream metadata
- Do not attempt to run command-not-found for anything prefixed with '.'
- Don't use PkBackendSpawn helpers in compiled backends
- Fix a hard-to-debug crash when cancelling a task that has never been run
- Look for unavailable packages during resolve
- Make pk_backend_job_call_vfunc() threadsafe
- Make pk_backend_repo_list_changed() threadsafe
- Return 'unavailable' packages for metadata-only repos
- Use a thread-local HifTransaction to avoid db3 index corruption

* Mon Nov 17 2014 Kalev Lember <kalevlember@gmail.com> - 1.0.3-2
- Update cached metadata in preparation for F21 release

* Mon Nov 10 2014 Richard Hughes <rhughes@redhat.com> - 1.0.3-1
- New upstream release
- Add support for reinstallation and downgrades
- Be smarter when using the vendor cache

* Tue Oct 21 2014 Richard Hughes <rhughes@redhat.com> - 1.0.1-1
- New upstream release
- Add a KeepCache config parameter
- Do not install the python helpers
- Invalidate offline updates when the rpmdb changes
- Never allow cancelling a transaction twice

* Wed Oct 15 2014 Kalev Lember <kalevlember@gmail.com> - 1.0.1-0.1.20141015
- Update to today's git snapshot

* Tue Sep 16 2014 Richard Hughes <rhughes@redhat.com> - 1.0.0-2
- Add a new subpackage designed for the workstation spin.
- See http://blogs.gnome.org/hughsie/2014/08/29/ for details.

* Fri Sep 12 2014 Richard Hughes <rhughes@redhat.com> - 1.0.0-1
- New upstream release
- Add a D-Bus interface and helpers for offline support
- Do not shutdown the daemon on idle by default
- Refresh the NetworkManager state when the daemon starts
- Remove pk-debuginfo-install
- Remove the events/pre-transaction.d functionality
- Remove the pkexec systemd helpers
- Remove the plugin interface
- Remove various options from the config file

## END: Generated by rpmautospec
