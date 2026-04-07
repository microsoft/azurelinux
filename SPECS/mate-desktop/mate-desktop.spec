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

%global branch 1.28

Summary:       Shared code for mate-panel, mate-session, caja, etc
Name:          mate-desktop
# Automatically converted from old format: GPLv2+ and LGPLv2+ and MIT - review is highly recommended.
License:       GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+ AND LicenseRef-Callaway-MIT
Version:       %{branch}.2
Release:       %autorelease
URL:           http://mate-desktop.org
Source0:       http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz

# fedora specific settings
Source1:       mate-fedora-f34.gschema.override
Source2:       mate-rhel.gschema.override
Source3:       mate-mimeapps.list
Source4:       80-mate-compiz.preset

BuildRequires: dconf-devel
BuildRequires: desktop-file-utils
BuildRequires: gobject-introspection-devel
BuildRequires: make
BuildRequires: mate-common
BuildRequires: startup-notification-devel
BuildRequires: gtk3-devel
BuildRequires: iso-codes-devel
BuildRequires: gobject-introspection-devel
BuildRequires: cairo-gobject-devel

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-configs = %{version}-%{release}
%if 0%{?fedora} && 0%{?fedora} >= 34
Obsoletes: %{name}-systemd <= 1.26.0-5
%endif
Requires: redhat-menus
Requires: xdg-user-dirs-gtk
Requires: mate-control-center-filesystem
Requires: mate-panel
Requires: mate-notification-daemon
Requires: mate-user-guide
%if 0%{?fedora} && 0%{?fedora} >= 40
Requires: f40-backgrounds-mate
%endif
%if 0%{?fedora} && 0%{?fedora} == 39
Requires: f39-backgrounds-mate
%endif
%if 0%{?fedora} && 0%{?fedora} == 38
Requires: f38-backgrounds-mate
%endif

# Need this to pull in the right imsettings in groupinstalls
# See https://bugzilla.redhat.com/show_bug.cgi?id=1349743
Suggests:  imsettings-mate

%description
The mate-desktop package contains an internal library
(libmatedesktop) used to implement some portions of the MATE
desktop, and also some data files and other shared components of the
MATE user environment.

%package libs
Summary:   Shared libraries for libmate-desktop
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:   LicenseRef-Callaway-LGPLv2+

%description libs
Shared libraries for libmate-desktop

%package configs
Summary:    Configurations for Mate desktop
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:    LicenseRef-Callaway-LGPLv2+
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}
%if 0%{?fedora} && 0%{?fedora} >= 40
Recommends: systemd-oomd-defaults
%endif
%if 0%{?fedora} && 0%{?fedora} <= 39
Recommends: earlyoom
%endif

%description configs
Configurations for Mate desktop

%package devel
Summary:    Libraries and headers for libmate-desktop
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:    LicenseRef-Callaway-LGPLv2+
Requires:   %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
Libraries and header files for the MATE-internal private library
libmatedesktop.


%prep
%autosetup -p1

#NOCONFIGURE=1 ./autogen.sh

%build
%configure                                                 \
     --enable-gtk-doc                                      \
     --disable-schemas-compile                             \
     --with-x                                              \
     --disable-static                                      \
     --with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids"      \
     --enable-gtk-doc-html                                 \
     --enable-introspection=yes

make %{?_smp_mflags} V=1


%install
%{make_install}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
find %{buildroot} -name '*.a' -exec rm -f {} ';'


desktop-file-install                                         \
        --delete-original                                    \
        --dir=%{buildroot}%{_datadir}/applications           \
%{buildroot}%{_datadir}/applications/mate-about.desktop

desktop-file-install                                         \
        --delete-original                                    \
        --dir=%{buildroot}%{_datadir}/applications           \
%{buildroot}%{_datadir}/applications/mate-color-select.desktop

%if 0%{?fedora} >= 34
install -D -m 0644 %SOURCE1 %{buildroot}%{_datadir}/glib-2.0/schemas/10_mate-fedora.gschema.override
%endif

%if 0%{?rhel}
install -D -m 0644 %SOURCE2 %{buildroot}%{_datadir}/glib-2.0/schemas/10_mate-rhel.gschema.override
%endif

mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %SOURCE3 %{buildroot}/%{_datadir}/applications/mate-mimeapps.list

%if 0%{?fedora} <= 39
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 644 %SOURCE4 %{buildroot}/%{_prefix}/lib/systemd/system-preset/80-mate-compiz.preset
%endif

%find_lang %{name} --with-gnome --all-name


%files
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_bindir}/mate-about
%{_bindir}/mate-color-select
%{_datadir}/applications/mate-about.desktop
%{_datadir}/applications/mate-color-select.desktop
%{_datadir}/mate-about
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/scalable/apps/mate-desktop-symbolic.svg
%{_datadir}/icons/hicolor/scalable/apps/mate-desktop.svg
%{_mandir}/man1/*

%files libs -f %{name}.lang
%{_libdir}/libmate-desktop-2.so.*
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml
%{_libdir}/girepository-1.0/MateDesktop-2.0.typelib

%files configs
%if 0%{?fedora} <= 39
%{_prefix}/lib/systemd/system-preset/80-mate-compiz.preset
%endif
%if 0%{?fedora}
%{_datadir}/glib-2.0/schemas/10_mate-fedora.gschema.override
%endif
%{_datadir}/applications/mate-mimeapps.list
%{_datadir}/xdg-desktop-portal/mate-portals.conf
%if 0%{?rhel}
%{_datadir}/glib-2.0/schemas/10_mate-rhel.gschema.override
%endif

%files devel
%{_libdir}/libmate-desktop-2.so
%{_libdir}/pkgconfig/mate-desktop-2.0.pc
%{_includedir}/mate-desktop-2.0
%doc %{_datadir}/gtk-doc/html/mate-desktop
%{_datadir}/gir-1.0/MateDesktop-2.0.gir


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.28.2-8
- Latest state for mate-desktop

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.28.2-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 12 2024 Wolfgang Ulbrich <fedora@raveit.de> - 1.28.2-1
- update to 1.28.2

* Thu Feb 22 2024 Wolfgang Ulbrich <fedora@raveit.de> - 1.28.1-1
- update to 1.28.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 15 2023 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.2-1
- update to 1.26.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Apr 01 2023 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.1-3
- bump version to get higher version than f37 build

* Sun Mar 26 2023 John Hein <c0eh3p702@sneakemail.com> - 1.26.1-2
- Remove systemd-oom-defaults conflict. It causes too many dnf upgrade failures.
- See https://bugzilla.redhat.com/show_bug.cgi?id=2078108

* Wed Mar 15 2023 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.1-1
- update to 1.26.1
- Fixes several issues with libmate-desktop
- Allow adjustment of audio-volume above 100 percent

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 15 2022 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.0-5
- obsolete mate-desktop-systemd
- use earlyoom instead of systemd-oomd-defaults
- make earlyoom uninstallable
- fixes rhbz (#2068699)

* Thu Apr 07 2022 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.0-4
- add dummy subpackage mate-desktop-systemd
- use earlyoom instead of systemd-oomd-defaults
- fixes rhbz (#2068699)

* Thu Mar 31 2022 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.0-3
- add subpackage mate-desktop-configs
- install 80-mate-compiz.preset

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.0-1
- update to 1.26.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 03 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.1-6
- update MATE terminal name in gsettings override

* Thu Apr 01 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.1-5
- add f34 gsettings overrides and use f34 night and day background

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 15 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.1-3
- update gsettings override files

* Tue Aug 25 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.1-2
- update fedora backgrounds requires

* Wed Aug 12 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.1-1
- update to 1.24.1

* Sun Aug 09 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-5
- Deactivate previews in the window-list-applet with a gsettings override

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Mar 15 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-3
- fix double requires of f31/32 background packages

* Sun Mar 15 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-2
- add gsettings override for f32
- add upstream patch
- fix pt and pt_BR locale translation issues

* Mon Feb 10 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-1
- update to 1.24.0

* Sun Feb 02 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.23.3-1
- update to 1.23.3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 20 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.2-1
- update 1.22.2 release

* Thu Sep 12 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.1-3
- use f31-backgrounds

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 25 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.1-1
- update 1.22.1 release

* Thu Mar 28 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-3
- update f30 gsettings override file for mate-menu icon

* Thu Mar 14 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-2
- use f30 default background

* Mon Mar 04 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-1
- update to 1.22.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 20 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.4-1
- update to 1.20.4

* Thu Sep 06 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.3-2
- add mate-language apis from upstream master
- https://github.com/mate-desktop/mate-desktop/commit/ecf2fbd

* Thu Sep 06 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.3-1
- update to 1.20.3
- use f29 default wallpaper
- add f29 gsettings override file

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 03 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.2-1
- update to 1.20.2

* Wed Apr 25 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-5
- Change default cursor size to 24px,
- better for modern HIDIPI displays

* Wed Apr 18 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-4
- fix dependencies to fedora backgrounds

* Wed Apr 18 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-3
- improve background handling for HIDPI monitors
- use https://github.com/mate-desktop/mate-desktop/pull/310

* Thu Apr 05 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-2
- use upstream patch, mate-rr-labeler: fix font-color for dark themes
- https://github.com/mate-desktop/mate-desktop/commit/abaa1e4

* Tue Mar 27 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-1
- update to 1.20.1

* Mon Mar 12 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.0-2
- use f28 backgrounds
- drop IconCache scriplets

* Sat Feb 10 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.0-1
- update to 1.20.0
- add f28 gsettings override file
- updated 27 gsettings override file
- drop GSettings Schema rpm scriplet
- switch to using autosetup

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.3-1
- update to 1.19.3

* Mon Jan 01 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.2-1
- update to 1.19.2
- update gsettings override file for touchpad libinput changes

* Sat Oct 14 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.1-1
- update to 1.19.1 release

* Wed Sep 20 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.0-4
- bump version
- use default f27-backgrounds for f27

* Wed Sep 20 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.0-3
- use default f27-backgrounds for f27

* Sun Sep 10 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.0-2
- use https://github.com/mate-desktop/mate-desktop/pull/282
- use https://github.com/mate-desktop/mate-desktop/pull/283
- add f27 fedora gsettings override file

* Thu Aug 17 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.0-1
- update to 1.19.0 release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 09 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.18.0-5
- fix rhel7 build

* Tue Jul 04 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.18.0-4
- update gsetting override file for touchpad settings with libinput
- disable SNI-Support for na-tray applets in override file
- use default-animated background for f26

* Sat Jun 17 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.18.0-3
- remove runtime requires pygtk2, rhbz(#1428281)

* Tue Apr 04 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.18.0-2
- update default wallpaper path in gsettings override

* Tue Mar 14 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.18.0-1
- update to 1.18.0 release
- add mate-fedora-f26.gschema.override file

* Sun Feb 26 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.2-3
- update gsettings override file
- remove dock from required-components-list

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 19 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.2-1
- update to 1.17.2 release

* Sun Jan 15 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.1-1
- update to 1.17.1 release

* Sat Dec 03 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-1
- update to 1.17.0 release
- move synaptic symlinks to m-s-d

* Wed Oct 19 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.1-1
- update to 1.16.1 release

* Thu Oct 13 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-2
- use default f25 wallpaper

* Wed Sep 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-1
- update to 1.16.0 release

* Fri Sep 02 2016 Peter Hutterer <peter.hutterer@redhat.com> 1.15.1-4
- Move the synaptics override to /etc/ (related #1338585)

* Thu Aug 11 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-3
- set a priority for the gsettings override file

* Sat Jul 02 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-2
- adjust spec file for rhel

* Sat Jul 02 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-1
- update to 1.15.1 release

* Thu Jun 30 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-2
- Add a Suggests imsettings-mate to workaround dnf issue. Bug #1349743

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release
- switch to gtk+3

* Thu May 26 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.1-2
- use compositor as default for f24

* Sat May 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.1-1
- update to 1.14.1 release
- fix MATE logo
- Backgrounds, take EXIF rotation tags into consideration

* Tue Apr 05 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release

* Sat Mar 26 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-2
- update gsettings overrride file for f24

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 01 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-11
- update to 1.12.1 release
- removed uptreamed patch

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-2
- fix crash with display-properties

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-2
- add runtime requires mate-user-guide

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release

* Tue Oct 13 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-4
- use fedora default background in gsettings override file

* Thu Sep 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-3
- set compositor to disable as default in gsettings override file

* Thu Sep 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-2
- add upstream patch to disable overlay-scrollbars in mate-session

* Mon Aug 24 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-1
- update to 1.10.2 release
- remove patch, issue is fixed in upstream
- do not obsolete mate-user-guide package
- adjust gsettings override for mate-terminal and set compositor true as default

* Sat Aug 08 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-4
- fix rhbz (#1251246)

* Mon Jul 20 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-3
- fix timing with xml backgrounds, rhbz (#1226604)

* Mon Jul 13 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-2
- add requires mate-notification-daemon, fix rhbz (#1242496)

* Sat Jul 11 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-1
- update to 1.10.1 release
- fix mimeapp.list
- add runtime requires xorg-x11-drv-synaptics
- remove upstreamed patches

* Fri Jul 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-10
- fix rhbz (#1231446, #1206985)
- do not crash on buggy image types

* Fri Jul 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-9
- use old help from 1.8
- use updated mate-mimeapps.list

* Fri Jun 26 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-8
- move synaptics conf to posttrans
- ghost the synaptics conf file

* Wed Jun 24 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-7
- update mate-mimeapps.list

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 30 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-5
- fix fix scriptlet

* Thu May 28 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-4
- add 99-synaptics-mate.conf

* Thu Apr 23 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-3
- bump version

* Thu Apr 23 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-2
- add mate-mimeapps.list, fix rhbz (#1214442), (#1074145)
- update gsettings override file

* Mon Apr 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release
- remove upstreamed patches

* Wed Mar 25 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90.3
- fix pkexec issues with mate-control-center
- set side-by-side-tiling=false as default for marco
- set enable-delete=true as default for caja
- fix glib-2.43 gsettings breakage

* Wed Mar 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90.2
- adjust gsettings override file for f22 default background

* Wed Feb 25 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90.1
- update to 1.9.90 release

* Thu Jan 15 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.4.1
- update to 1.9.4 release
- enable introspection build
- spec file cleanup

* Thu Dec 18 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.3-2
- update override file

* Tue Nov 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.3-1
- update to 1.9.3 release

* Fri Nov 7 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-3
- switch to use xml backgrounds

* Sun Oct 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-2
- set cursor theme to mate in gsettings override file
- adjust obsoletes

* Fri Oct 03 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-1
- update to 1.9.2 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jul 20 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-2
- revert obsolete mate-calc

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1.1
- update to 1.9.1 release
- obsolete mate-calc for f21
- obsolete mate-dialogs for f22

* Sun Jul 06 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-3
- fix gschema override file

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1
- clean up spec file

* Sat Mar 22 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-3
- add new f21 gsettings overrride file
- remove caja-autostart override
- add mate-panel-menubar override
- enable fedora.layout for mate-panel in override file
- obsolete mate-doc-utils and mate-character-map for f21
- remove BR mate-doc-utils for f21
- use more conditionals to make spec file usable for every fedora branch
- remove configure flag --with-omf-dir for f21

* Wed Mar 05 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- enable desktop-docs
- remove conficting files during build
- obsolete libmatewnck, compiz is updated in rawhide

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Feb 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90 release

* Thu Feb 13 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.5-3
- comment out obsoletes tag for libmatewnck
- libmatewnck is currently needed for compiz

* Wed Feb 12 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.5-2
- Add obsoletes tag for libmatewnck

* Mon Feb 10 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.5-1
- update to 1.7.5 release
- add mate-user-guide desktop file
- rename patch for f21

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.4-1
- Update to 1.7.4

* Thu Jan 16 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.3-1
- update to 1.7.3 release
- enable gnucat
- clean up spec file

* Tue Jan 14 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2-1
- update to 1.7.1 release
- move gtk-doc dir to -devel subpackage
- use modern 'make install' macro
- remove obsolete configure flags
- enable mpaste

* Fri Dec 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-2
- fix previous build, add forgotten fedora's override file again!!!!!

* Wed Dec 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.1-1
- Update to 1.7.1

* Thu Nov 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.12.git81c245b
- BlueMenta is now default theme in fedora 20

* Thu Nov 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.11.git81c245b
- use Menta-Blue as default theme in fedora 20, change gesettings overrides

* Tue Nov 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.10.git81c245b
- add gsettings overrides again for caja f20

* Thu Nov 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.9.git81c245b
- use Menta-Blue as default theme in fedora 20, change gesettings overrides

* Tue Nov 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.8.git81c245b
- let caja starts with mate-session-manager for > f19
- adjust mate-fedora gesettings override file

* Sat Oct 19 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.7.git81c245b
- switch to gnome-keyring for > f19

* Fri Oct 18 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2.-0.6.git81c245b
- Fix typo

* Tue Oct 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.5.git81c245b
- remove gsettings overrides from last update

* Wed Oct 09 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2.-0.4.git81c245b
- Further fix for #886029 (disable background-fade)


* Wed Oct 09 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2.-0.3.git81c245b
- Possible fix for #886029 (disable background draw and mate-settings-daemon background plugin)

* Fri Oct 04 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.2-0.2.git81c245b
- Get rid of obsoletes tag as we no longer need it. (#1015335)

* Mon Sep 23 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-0.1.git81c245b
- update to latest git snapshot
- fix https://github.com/mate-desktop/mate-settings-daemon/issues/32

* Sat Sep 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-14
- versioned mate-bluetooth obsolete

* Sat Sep 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-13
- obsolete mate-bluetooth-libs and mate-bluetooth-devel too

* Fri Sep 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-12
- obsolete mate-bluetooth for f20

* Wed Aug 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-11
- move schemas and locale to -libs subpackage to fix rhbz #988944
- add better font rendering settings to gsettings.override file
- use mate-control-center-filesystem instead of control-center-filesystem
- as runtime require
- clean up BRs, most of them are already called
- remove BR gsettings-desktop-schemas-devel
- remove BRs gtk2-devel and gtk3-devel
- remove BR gtk-doc
- remove BR pangox-compat-devel
- remove runtime require libnotify, no need of this anymore

* Sun Jul 28 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-10
- Undo obsolete consolekit RHBZ 989208

* Sat Jul 27 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-9
- obsolete ConsoleKit

* Sat Jun 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-8
- remove gsettings convert file

* Tue Jun 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-7
- Obsolete more packages to fix RHBZ 972548
- Remove obsolete for libmatenotify for debugging purposes
- Add control-center-filesystem for debugging purposes

* Fri May 31 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-6
- Obsolete all mate-conf packages for depsolving issues.
- Keep changelogs in sync and bump release version.

* Tue May 28 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-5
- Remove mate-notification-daemon from hard requires.

* Sat May 25 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-4
- Own mateconf gsettings dir

* Fri May 24 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-3
- Obsolete mate-conf as compiz no longer uses it, obsoleted upstream.
- Add requires mate-notification-daemon as nothing else does.

* Fri May 24 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-2
- workaround for x-caja-desktop window issue
- add mate-fedora.gschema.override file

* Thu May 23 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release
- Readd gnucat

* Fri May 03 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-3
- Own dirs we are supposed to own (961950)
- Move docs to main package and mark them with doc macro
- Add pangox-compat-devel to BRs

* Mon Apr 22 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-2
- Remove obsletes for libmatenotify as compiz requires it.

* Tue Apr 02 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0 release.

* Mon Mar 25 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.8-1
-Update to latest upstream release

* Fri Feb 22 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.7-1
-Update to latest upstream release

* Fri Feb 08 2013 - Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.6-1
-Update to latest upstream release

* Mon Dec 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
- Update to 1.5.5 release

* Sun Nov 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.4-1
- update to 1.5.4 release
- no need to drop upstream commits patch as some twat blew it away

* Sat Nov 24 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-7
- Add disable schemas compile configure flag

* Wed Nov 21 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-6
- add upstream commits patch

* Thu Nov 15 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-5
- remove omf directory hack and do it properly

* Wed Nov 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-4
- add requires xdg-user-dirs-gtk
- set default directories

* Mon Nov 05 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-3
- Fix tabs/spaces
- Switch to new buildroot macro instead of old RPM_BUILD_ROOT macro

* Sat Nov 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.3-2
- enable gnucat

* Sat Nov 03 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.3-1
- update to 1.5.3 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.2-1
- update to 1.5.2 release

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-2
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1 release
- remove all the false mate requires (breached package guidelines)
- remove unused build require and change style
- add schema scriptlets
- clean up spec file
- fix Summary

* Wed Oct 17 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.4.1-12
- Add runtime requirements to avoid confusion

* Wed Sep 19 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.1-11
- drop problematic bg-crossfade patch (breaks mate-settings-daemon)
- remove .desktop Only-Show-In mods

* Sun Aug 12 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.1-10
- fix deps wrt -libs subpkg

* Sat Aug 11 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-9
- add isa tag to -libs

* Sat Aug 11 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-8
- change file section for own directories
- change 'to avoid conflicts with gnome' part
- add libs subpackage for shared libraries

* Fri Aug 03 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-7
- add desktop file install for mate-about.desktop
- add BuildRequires desktop-file-utils
- remove BuildRequires intltool gtk-doc

* Fri Aug 03 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.1-6
- start initial for fedora
- remove unnecessary buildRequires
- Drop pycairo from Requires
- change --with-pnp-ids-path="/usr/share/hwdata/pnp.ids" to
- --with-pnp-ids-path="%%{_datadir}/hwdata/pnp.ids"

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- mate-desktop.spec based on gnome-desktop-2.32.0-9.fc16 spec

## END: Generated by rpmautospec
