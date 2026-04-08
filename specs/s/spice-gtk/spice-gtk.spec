## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 8;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#define _version_suffix

Name:           spice-gtk
Version:        0.42
Release:        %autorelease
Summary:        A GTK+ widget for SPICE clients

License:        LGPL-2.1-or-later AND MIT AND MIT-open-group and BSD-3-Clause
URL:            https://www.spice-space.org/spice-gtk.html
#VCS:           git:git://anongit.freedesktop.org/spice/spice-gtk
Source0:        https://www.spice-space.org/download/gtk/%{name}-%{version}%{?_version_suffix}.tar.xz
#Source1:        https://www.spice-space.org/download/gtk/%{name}-%{version}%{?_version_suffix}.tar.xz.sig
#Source2:        victortoso-E37A484F.keyring

BuildRequires: git-core
BuildRequires: meson
BuildRequires: usbredir-devel >= 0.7.1
BuildRequires: libusb1-devel >= 1.0.21
BuildRequires: pixman-devel libjpeg-turbo-devel
BuildRequires: opus-devel
BuildRequires: zlib-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libcacard-devel
BuildRequires: gobject-introspection-devel
BuildRequires: libacl-devel
%if ! 0%{?flatpak}
BuildRequires: polkit-devel
%endif
BuildRequires: gtk-doc
BuildRequires: vala
BuildRequires: usbutils
BuildRequires: libsoup3-devel
BuildRequires: libphodav-devel >= 3.0
BuildRequires: lz4-devel
BuildRequires: gtk3-devel
BuildRequires: json-glib-devel
BuildRequires: spice-protocol >= 0.14.1
BuildRequires: gstreamer1-devel >= 1.10 gstreamer1-plugins-base-devel >= 1.10
BuildRequires: python3-six
BuildRequires: python3-pyparsing
BuildRequires: openssl-devel
BuildRequires: gnupg2
BuildRequires: libcap-ng-devel
BuildRequires: wayland-protocols-devel

Obsoletes: spice-gtk-python < 0.32

Requires: spice-glib%{?_isa} = %{version}-%{release}

%description
Client libraries for SPICE desktop servers.

%package -n spice-glib
Summary: A GObject for communicating with Spice servers

%description -n spice-glib
spice-client-glib-2.0 is a SPICE client library for GLib2.

%package -n spice-glib-devel
Summary: Development files to build Glib2 applications with spice-glib-2.0
Requires: spice-glib%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: glib2-devel

%description -n spice-glib-devel
spice-client-glib-2.0 is a SPICE client library for GLib2.

Libraries, includes, etc. to compile with the spice-glib-2.0 libraries

%package -n spice-gtk3
Summary: A GTK3 widget for SPICE clients
Requires: spice-glib%{?_isa} = %{version}-%{release}

%description -n spice-gtk3
spice-client-glib-3.0 is a SPICE client library for Gtk3.

%package -n spice-gtk3-devel
Summary: Development files to build GTK3 applications with spice-gtk-3.0
Requires: spice-gtk3%{?_isa} = %{version}-%{release}
Requires: spice-glib-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig
Requires: gtk3-devel
Obsoletes: spice-gtk-devel < 0.32

%description -n spice-gtk3-devel
spice-client-gtk-3.0 provides a SPICE viewer widget for GTK3.

Libraries, includes, etc. to compile with the spice-gtk3 libraries

%package -n spice-gtk3-vala
Summary: Vala bindings for the spice-gtk-3.0 library
Requires: spice-gtk3%{?_isa} = %{version}-%{release}
Requires: spice-gtk3-devel%{?_isa} = %{version}-%{release}

%description -n spice-gtk3-vala
A module allowing use of the spice-gtk-3.0 widget from vala

%package tools
Summary: Spice-gtk tools
Requires: spice-gtk3%{?_isa} = %{version}-%{release}

%description tools
Simple clients for interacting with SPICE servers.
spicy is a client to a SPICE desktop server.
spicy-screenshot is a tool to capture screen-shots of a SPICE desktop.


%prep
#gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -S git_am


%build

# meson macro has --auto-features=enabled

%meson \
  -Dbuiltin-mjpeg=false \
%ifarch s390x # https://gitlab.freedesktop.org/spice/spice-gtk/issues/120
  -Dusbredir=disabled \
%endif
%if 0%{?flatpak}
  -Dpolkit=disabled
%else
  -Dusb-acl-helper-dir=%{_libexecdir}/spice-gtk-%{_arch}/
%endif

%meson_build


%check
%meson_test


%install
%meson_install


%find_lang %{name}

%ldconfig_scriptlets
%ldconfig_scriptlets -n spice-glib
%ldconfig_scriptlets -n spice-gtk3


%files
%doc AUTHORS
%doc COPYING
%doc README.md
%doc CHANGELOG.md
%{_mandir}/man1/spice-client.1*

%files -n spice-glib -f %{name}.lang
%{_libdir}/libspice-client-glib-2.0.so.*
%{_libdir}/girepository-1.0/SpiceClientGLib-2.0.typelib
%if ! 0%{?flatpak}
%dir %{_libexecdir}/spice-gtk-%{_arch}/
%attr(4755, root, root) %{_libexecdir}/spice-gtk-%{_arch}/spice-client-glib-usb-acl-helper
%{_datadir}/polkit-1/actions/org.spice-space.lowlevelusbaccess.policy
%endif

%files -n spice-glib-devel
%{_libdir}/libspice-client-glib-2.0.so
%{_includedir}/spice-client-glib-2.0
%{_libdir}/pkgconfig/spice-client-glib-2.0.pc
%{_datadir}/gir-1.0/SpiceClientGLib-2.0.gir
%doc %{_datadir}/gtk-doc/html/*

%files -n spice-gtk3
%{_libdir}/libspice-client-gtk-3.0.so.*
%{_libdir}/girepository-1.0/SpiceClientGtk-3.0.typelib

%files -n spice-gtk3-devel
%{_libdir}/libspice-client-gtk-3.0.so
%{_includedir}/spice-client-gtk-3.0
%{_libdir}/pkgconfig/spice-client-gtk-3.0.pc
%{_datadir}/gir-1.0/SpiceClientGtk-3.0.gir

%files -n spice-gtk3-vala
%{_datadir}/vala/vapi/spice-client-glib-2.0.deps
%{_datadir}/vala/vapi/spice-client-glib-2.0.vapi
%{_datadir}/vala/vapi/spice-client-gtk-3.0.deps
%{_datadir}/vala/vapi/spice-client-gtk-3.0.vapi

%files tools
%{_bindir}/spicy
%{_bindir}/spicy-screenshot
%{_bindir}/spicy-stats

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 0.42-8
- Latest state for spice-gtk

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 19 2023 Daniel P. Berrangé <berrange@redhat.com> - 0.42-2
- Convert license to SPDX format

* Mon Jan 23 2023 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.42-1
- Update to v0.42

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 04 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.41-3
- BR on phodav >= 3.0

* Mon Jul 04 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.41-2
- BR on libsoup3

* Mon Jul 04 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.41-1
- Update to 0.41

* Thu Feb 10 2022 Victor Toso <victortoso@redhat.com> - 0.40-1
- Update to v0.40

* Thu Jan 27 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.39-7
- Fix FTBFS. rhbz#2047026

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 0.39-5
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.39-3
- Fix potential div/0. Resolves: rhbz#1941627

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec  1 2020 Victor Toso <victortoso@redhat.com> - 0.39-1
- Update to v0.39

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Mar 16 2020 Victor Toso <victortoso@redhat.com> - 0.38-1
- Update to v0.38
- s390x: disable usbredir

* Tue Feb 25 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.37-6
- Fix FTBFS https://bugzilla.redhat.com/show_bug.cgi?id=1800106

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 04 2019 Adam Williamson <awilliam@redhat.com> - 0.37-4
- Backport clipboard-race patches for #1755038

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 14 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.37-2
- Add 0001-vmcstream-Fix-buffer-overflow-sending-data-to-task.patch fix. rhbz#1720532

* Thu May 16 2019 Victor Toso <victortoso@redhat.com> - 0.37-1
- Update to v0.37
- Add gpg check to release's signature

* Thu Mar 07 2019 Christophe Fergeau <cfergeau@redhat.com> - 0.36-5
- Use actual upstream patches, I made a mistake in the previous build
  and used patches which were only applied locally

* Thu Feb 21 2019 Christophe Fergeau <cfergeau@redhat.com> - 0.36-4
- Add upstream patches fixing issues with the cursor becoming invisible
  in wayland environments
  Resolves: rhbz#1528200

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.36-3
- Update BRs for vala packaging changes

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.36-1
- v0.36 release

* Wed Sep 19 2018 Christophe Fergeau <cfergeau@redhat.com> - 0.35-3
- Fix scrolling with mousewheel
  https://bugzilla.redhat.com/show_bug.cgi?id=1627823

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Victor Toso <victortoso@redhat.com> - 0.35-1
- v0.35 release

* Wed May 30 2018 Christophe Fergeau <cfergeau@redhat.com> - 0.34-5
- Fix keyboard input under Xwayland
  Resolves: rhbz#1512564

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.34-3
- Switch to %%ldconfig_scriptlets

* Thu Aug 24 2017 Christophe Fergeau <cfergeau@gmail.com> - 0.34-2
- Build against OpenSSL 1.1.0 rather than the older 1.0

* Mon Jul 31 2017 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.34-1
- v0.34 release

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Cole Robinson <crobinso@redhat.com> - 0.33-5
- channel-usbredir: Fix crash on channel-up. Resolves: rhbz#1399838
- usbutils no longer ships usb.ids, it is hwdata now, set path manually.
- Backport fixes for "Couldn't find current GL or GLX context" Resolves: rhbz#1461802

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 25 2016 Victor Toso <victortoso@redhat.com> - 0.33-2
- Fix crash due clipboard failure with text conversion
  Resolves: rhbz#1384676

* Fri Oct 07 2016 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.33-1
- Update to new 0.33 upstream release

* Thu Oct 06 2016 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.32-3
- Fix display refresh unless scaling is forced (rhbz#1382325)

* Mon Jul 11 2016 Christophe Fergeau <cfergeau@redhat.com> 0.32-2
- Add upstream patches fixing USB event thread leak
  Resolves: rhbz#1217202 (virt-manager)
  May help with rhbz#1338042 (gnome-boxes)

* Tue Jun 21 2016 Marc-André Lureau <marcandre.lureau@redhat.com> 0.32-1
- Update to new 0.32 upstream release

* Fri Apr 15 2016 Christophe Fergeau <cfergeau@redhat.com> - 0.31-2
- Add upstream patch fixing flickering bug
  Resolves: rhbz#1266484

* Fri Mar 11 2016 Marc-André Lureau <marcandre.lureau@redhat.com> 0.31-1
- Update to new 0.31 upstream release

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Christophe Fergeau <cfergeau@redhat.com> 0.30-1
- Update to new 0.30 upstream release

* Sat Sep 12 2015 Cole Robinson <crobinso@redhat.com> 0.29-4
- Fix virt-manager default screen resolution and resolution across reboots
- Resolves: rhbz#1240721

* Tue Sep 08 2015 Christophe Fergeau <cfergeau@redhat.com> 0.29-3
- Don't crash on volume sync when there is no audio channel
  Resolves: rhbz#1257210

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Marc-Andre Lureau <marcandre.lureau@redhat.com> 0.29-1
- Update to spice-gtk v0.29

* Mon May 11 2015 Marc-Andre Lureau <marcandre.lureau@redhat.com> 0.28-3
- Fix audio and usb channels with GNOME Boxes.
  Resolves: rhbz#1220026

* Tue Mar 31 2015 Christophe Fergeau <cfergeau@redhat.com> 0.28-2
- Add upstream patch fixing an USB redirection crash
  Resolves: rhbz#1182226
- Adjust build requires to new naming of phodav package

* Wed Mar 4 2015 Marc-André Lureau <marcandre.lureau@redhat.com> 0.28-1
- Update to spice-gtk v0.28

* Mon Feb 23 2015 Christophe Fergeau <cfergeau@redhat.com> 0.27-6
- Rebuild for phodav soname bump

* Tue Jan 27 2015 Marc-André Lureau <marcandre.lureau@redhat.com> 0.27-5
- Fix reconnection on same session regressions introduced in 27-2.

* Tue Dec 30 2014 Christophe Fergeau <cfergeau@redhat.com> 0.27-4
- Enable lz4 support

* Mon Dec 22 2014 Marc-André Lureau <marcandre.lureau@redhat.com> 0.27-3
- Fix usbredir crash on disconnection.

* Tue Dec 16 2014 Marc-André Lureau <marcandre.lureau@redhat.com> 0.27-2
- Fix authentication error handling regression.

* Thu Dec 11 2014 Marc-André Lureau <marcandre.lureau@redhat.com> 0.27-1
- Update to spice-gtk v0.27

* Wed Oct 29 2014 Christophe Fergeau <cfergeau@redhat.com> 0.26-1
- Update to spice-gtk v0.26

* Wed Sep 24 2014 Christophe Fergeau <cfergeau@redhat.com> 0.25-6
- Run make install in gtk3 build after doing so in gtk2 build, otherwise
  we'll end up packaging gtk2 builds of spicy et al in spice-client-tools
  instead of gtk3 ones (#1145829)

* Wed Aug 20 2014 Kalev Lember <kalevlember@gmail.com> - 0.25-5
- Rebuilt for rpm dependency generator failure (#1131892)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.25-3
- Rebuilt for gobject-introspection 1.41.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 25 2014 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.25-1
- Update to upstream release v0.25
- Added phodav dependency

* Tue Feb 25 2014 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.23-2
- Fix crash on finishing display rhbz#1069546

* Mon Feb 10 2014 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.23-1
- Update to spice-gtk 0.23

* Wed Nov 27 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.22-1
- Update to spice-gtk 0.22

* Sun Nov 17 2013 Cole Robinson <crobinso@redhat.com> - 0.21-5
- Fix grub graphical corruption after VM reboot (bz #1017955)

* Mon Oct 21 2013 Alon Levy <alevy@redhat.com> - 0.21-4
- Fix mono invert only cursor contract. rhbz#998529

* Thu Oct  3 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.21-3
- Fix palette cache regression. rhbz#1011936

* Mon Sep 30 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.21-2
- Fix usbredir being broken in 0.21 release

* Wed Sep 18 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.21-1
- Update to spice-gtk 0.21

* Fri Sep 13 2013 Christophe Fergeau <cfergeau@redhat.com> 0.20-6
- Add misc upstream patches fixing various 0.20 bugs

* Wed Aug 28 2013 Alon Levy <alevy@redhat.com> - 0.20-5
- Fix wrong mono cursor local rendering (rhbz#998529)

* Wed Aug 28 2013 Hans de Goede <hdegoede@redhat.com> - 0.20-4
- Fix the spice-client-glib-usb-acl-helper no longer being suid root

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul  6 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.20-2
- Fix spice_channel_string_to_type symbol visibility (rhbz#981815)

* Wed Jun 26 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.20-1
- Update to spice-gtk 0.20

* Thu Apr 11 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.19-1
- Update to spice-gtk 0.19

* Thu Mar 14 2013 Hans de Goede <hdegoede@redhat.com> - 0.18-2
- Fix "Warning no automount-inhibiting implementation available" warnings

* Wed Feb 13 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.18-1
- Update to spice-gtk 0.18

* Wed Feb  6 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.17-1
- Update to spice-gtk 0.17

* Thu Jan 31 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.16-2
- Remove perl-text-csv build requirement. (rhbz#873174)

* Sat Jan 12 2013 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.16-1
- Update to spice-gtk 0.16

* Mon Dec 31 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.15.3-1
- Update to spice-gtk 0.15.3, fixes TLS & password regressions

* Fri Dec 21 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.15-2
- Update to spice-gtk 0.15

* Thu Oct 25 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-2
- Add various upstream patches

* Fri Sep 21 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.14-1
- Update to 0.14 release

* Fri Sep 14 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-4
- Add patch fixing CVE 2012-4425

* Thu Sep 13 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-3
- Run autoreconf after applying patch 2 as it only modifies Makefile.am

* Tue Sep 11 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13.29-2
- Add patch to fix symbol versioning

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 0.13.29-1
- Update to the spice-gtk 0.13.29 development release
- Rebuild for new usbredir

* Mon Sep 03 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.13-2
- Update to spice-gtk 0.13

* Tue Aug 07 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.12.101-1
- Update to the spice-gtk 0.12.101 development release (needed by Boxes
  3.5.5)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-4
- re-Add back spice-protocol BuildRequires to help some deps magic happen

* Thu May 10 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-3
- Fix Spice.Audio constructor Python binding
  https://bugzilla.redhat.com/show_bug.cgi?id=820335

* Wed May  2 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-2
- Fix virt-manager console not showing up, rhbz#818169

* Tue Apr 24 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.12-1
- New upstream release 0.12

* Tue Apr 10 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.11-5
- Fix build on PPC
- Remove ExclusiveArch. While spice-gtk will build on ARM and PPC, it
  hasn't been tested on these arch, so there may be some bugs.

* Tue Mar 20 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-4
- Add missing BuildRequires: usbutils, so that we get proper USB device
  descriptions in the USB device selection menu

* Wed Mar 14 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-3
- Fix a crash triggered when trying to view a usbredir enabled vm from
  virt-manager

* Mon Mar 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-2
- Add back spice-protocol BuildRequires to help some deps magic happen

* Fri Mar  9 2012 Hans de Goede <hdegoede@redhat.com> - 0.11-1
- New upstream release 0.11
- Fix multilib conflict in spice-glib

* Thu Feb 23 2012 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.10-1
- New upstream release 0.10

* Mon Jan 30 2012 Hans de Goede <hdegoede@redhat.com> - 0.9-1
- New upstream release 0.9

* Mon Jan 16 2012 Hans de Goede <hdegoede@redhat.com> - 0.8-1
- New upstream release 0.8
- Various small specfile improvements
- Enable vala bindings

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Adam Jackson <ajax@redhat.com> 0.7.39-2
- Rebuild to break bogus libpng dependency
- Fix summaries for gtk3 subpackages to not talk about gtk2

* Fri Sep  2 2011 Hans de Goede <hdegoede@redhat.com> - 0.7.39-1
- Update to git snapshot 0.7.39-ab64, to add usbredir support

* Tue Jul 26 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7.1-1
- Upstream version 0.7.1-d5a8 (fix libtool versionning)

* Tue Jul 19 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.7-1
- Upstream release 0.7

* Wed May 25 2011 Christophe Fergeau <cfergeau@redhat.com> - 0.6-1
- Upstream release 0.6

* Tue Mar  1 2011 Hans de Goede <hdegoede@redhat.com> - 0.5-6
- Fix spice-glib requires in .pc file (#680314)

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-5
- Fix build against glib 2.28

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-4
- Rebuild against newer gtk

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 0.5-2
- Rebuild against newer gtk

* Thu Jan 27 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.5-1
- Upstream release 0.5

* Fri Jan 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.4-2
- Add support for parallel GTK3 build

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 0.4-2
- add ExclusiveArch as only x86 is supported

* Sun Jan 09 2011 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.4-1
- Upstream release 0.4
- Initial release (#657403)

* Thu Nov 25 2010 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.1.0-1
- Initial packaging

## END: Generated by rpmautospec
