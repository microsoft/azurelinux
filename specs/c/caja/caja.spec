## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 10;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global branch 1.28

Name:        caja
Summary:     File manager for MATE
Version:     %{branch}.0
Release:     %autorelease
# Automatically converted from old format: GPLv2+ and LGPLv2+ - review is highly recommended.
License:     GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+
URL:         http://mate-desktop.org
Source0:     http://pub.mate-desktop.org/releases/%{branch}/%{name}-%{version}.tar.xz

Patch1:      caja_0001-caja-file-operations-fix-caption-button-in-destinati.patch
Patch2:      caja_0003-wayland-background-use-mate-appearance-properties-if.patch
Patch3:      caja_0004-build-remove-configure-dependency-on-perl-1789.patch
Patch4:      caja_0005-wayland-ensure-windows-can-be-moved-if-compositor-is.patch
Patch5:      caja_0009-caja-file-operations-fix-estimate-for-queued-copy-17.patch
Patch6:      caja_0010-caja-file-operations-restart-timer-also-for-moves.patch

BuildRequires: dbus-glib-devel
BuildRequires: desktop-file-utils
BuildRequires: exempi-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gtk-layer-shell-devel
BuildRequires: cairo-gobject-devel
BuildRequires: libexif-devel
BuildRequires: libselinux-devel
BuildRequires: libSM-devel
BuildRequires: libxml2-devel
BuildRequires: make
BuildRequires: mate-common
BuildRequires: mate-desktop-devel
BuildRequires: pango-devel
BuildRequires: startup-notification-devel
BuildRequires: libnotify-devel

Requires:   filesystem
Requires:   redhat-menus
Requires:   gvfs
# >= f43 , see rhbz (#2411809)
%if 0%{?fedora} && 0%{?fedora} >= 43
Requires:   glycin-thumbnailer
%endif

# the main binary links against libcaja-extension.so
# don't depend on soname, rather on exact version
Requires:       %{name}-core-extensions%{?_isa} = %{version}-%{release}

# needed for using mate-text-editor as stanalone in another DE
Requires:       %{name}-schemas%{?_isa} = %{version}-%{release}

%description
Caja (mate-file-manager) is the file manager and graphical shell
for the MATE desktop,
that makes it easy to manage your files and the rest of your system.
It allows to browse directories on local and remote file systems, preview
files and launch applications associated with them.
It is also responsible for handling the icons on the MATE desktop.

%package core-extensions
Summary:  Mate-file-manager extensions library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description core-extensions
This package provides the libraries used by caja extensions.

# needed for using mate-text-editor (pluma) as stanalone in another DE
%package schemas
Summary:  Mate-file-manager schemas
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:  LicenseRef-Callaway-LGPLv2+

%description schemas
This package provides the gsettings schemas for caja.

%package devel
Summary:  Support for developing mate-file-manager extensions
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides libraries and header files needed
for developing caja extensions.


%prep
%autosetup -p1

# disable startup notification
sed -i s/StartupNotify=true/StartupNotify=false/g data/caja-computer.desktop.in.in
sed -i s/StartupNotify=true/StartupNotify=false/g data/caja-home.desktop.in.in

#Patch2
NOCONFIGURE=1 ./autogen.sh

%build
%configure \
        --disable-static \
        --disable-schemas-compile \
        --disable-update-mimedb \
        --enable-wayland

#drop unneeded direct library deps with --as-needed
# libtool doesn't make this easy, so we do it the hard way
sed -i -e 's/ -shared / -Wl,-O1,--as-needed\0 /g' libtool

make %{?_smp_mflags} V=1

%install
%{make_install}

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name '*.a' -exec rm -f {} ';'

rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/.icon-theme.cache

mkdir -p $RPM_BUILD_ROOT%{_libdir}/caja/extensions-2.0

desktop-file-install                              \
    --delete-original                             \
    --dir=$RPM_BUILD_ROOT%{_datadir}/applications \
$RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

# Avoid prelink to mess with caja - rhbz (#1228874)
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/prelink.conf.d
cat << EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/prelink.conf.d/caja.conf
-b %{_libdir}/caja/
-b %{_libdir}/libcaja-extension.so.*
-b %{_libexecdir}/caja-convert-metadata
-b %{_bindir}/caja
-b %{_bindir}/caja-autorun-software
-b %{_bindir}/caja-connect-server
-b %{_bindir}/caja-file-management-properties
EOF

%find_lang %{name} --with-gnome --all-name


%files
%doc AUTHORS COPYING COPYING.LIB NEWS README
%{_bindir}/*
%{_datadir}/caja
%{_libdir}/caja/
%{_sysconfdir}/prelink.conf.d/caja.conf
%{_datadir}/pixmaps/caja/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/emblems/emblem-note.png
%{_mandir}/man1/*
%{_datadir}/metainfo/caja.appdata.xml
%{_datadir}/mime/packages/caja.xml
%{_datadir}/dbus-1/services/org.mate.freedesktop.FileManager1.service

%files core-extensions
%{_libdir}/libcaja-extension.so.*
%{_libdir}/girepository-1.0/*.typelib

%files schemas -f %{name}.lang
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

%files devel
%{_includedir}/caja/
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir
%{_datadir}/gtk-doc/html/libcaja-extension


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.28.0-10
- test: add initial lock files

* Sun Nov 23 2025 raveit65 <raveit65.sun@gmail.com> - 1.28.0-9
- Require glycin-thumbnailer for >=f43

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 14 2025 raveit65 <mate@raveit.de> - 1.28.0-7
- add some upstream commits

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1.28.0-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 23 2024 Wolfgang Ulbrich <fedora@raveit.de> - 1.28.0-1
- update to 1.28.0

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 22 2023 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.3-2
- fix build with libxml-2.12.0

* Fri Oct 13 2023 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.3-1
- update to 1.26.3

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 03 2022 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.1-1
- update to 1.26.1

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 10 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.0-2
- fix https://github.com/mate-desktop/caja/issues/1562
- use https://github.com/mate-desktop/caja/pull/1563

* Wed Aug 04 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.0-1
- update to 1.26.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Mar 25 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.1-1
- update to 1.24.1

* Tue Feb 9 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-7
- drop gamin dependency

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-4
- fix dependencies, hopefully

* Sat May 23 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-3
- drop non needed provides and obsoletes

* Fri May 22 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-2
- drop BR pangox-compat-devel in favour of pango-devel

* Mon Feb 10 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-1
- update to 1.24.0

* Sun Feb 02 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.23.4-1
- update to 1.23.4
- fix f32 mass rebuild
- drop c99 patch

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 23 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.3-1
- update to 1.22.3

* Fri Nov 22 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.2-2
- https://github.com/mate-desktop/caja/commit/ea81a5
- Don't hyphenate filenames with pango-1.44

* Wed Sep 18 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.2-1
- update to 1.22.2

* Tue Sep 10 2019 Florian Weimer <fweimer@redhat.com> - 1.22.1-4
- Fix building in C99 mode

* Fri Sep 06 2019 Nikola Forró <nforro@redhat.com> - 1.22.1-3
- rebuilt for exempi 2.5.1

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 26 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.1-1
- update to 1.22.1

* Mon Mar 04 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.0-1
- update to 1.22.0

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 11 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.3-1
- test 1.20.3

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.2-2
- rename caja-extension sub-package to avoid conflicts with
- debuginfo from caja-extensions

* Fri Apr 06 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.2-1
- update to 1.20.2

* Tue Mar 27 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-1
- update to 1.20.1

* Sun Feb 11 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-3
- fix emblem and backgrounds preferences UI

* Sun Feb 11 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-2
- drop obsolet scriptlet again

* Sun Feb 11 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-1
- update to 1.20.0 release
- drop mimeinfo rpm scriptlet
- drop desktop-database rpm scriptlet
- drop GSettings Schema rpm scriptlet
- switch to using autosetup

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.19.3-2
- Remove obsolete scriptlets

* Mon Jan 01 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.3-1
- update to 1.19.3
- use https://github.com/mate-desktop/caja/pull/891

* Wed Oct 11 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.2-1
- update to 1.19.2 release

* Mon Aug 28 2017 Wolfgang Ulbrich <fedora@raveit.de> - 1.19.1-2
- use https://github.com/mate-desktop/caja/pull/837
- use https://github.com/mate-desktop/caja/pull/838

* Sat Aug 26 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.1-1
- update to 1.19.1

* Wed Aug 09 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.0-4
- remove virtual provides

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 11 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.0-1
- update to 1.19.0 release

* Tue Apr 25 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.2-3
- fix opening download folder from Firefox "freezes" X
- https://github.com/mate-desktop/caja/commit/6ece67f

* Tue Apr 25 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.2-2
- add some upstream patches
- Expand grid width to canvas
- use gtk+-3 bookmark location
- force icons size in open-with-dialog
- show correct right-click menu after making selection

* Tue Apr 04 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.2-1
- update to 1.18.2
- add upstream commit "Expand grid width to canvas"

* Tue Apr 04 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.1-1
- update to 1.18.1

* Tue Mar 14 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.0-1
- update to 1.18.0 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.3-1
- update to 1.17.3

* Mon Jan 09 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.2-1
- update to 1.17.2
- fix running under wayland session

* Sat Dec 03 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.1-1
- update to 1.17.1 release

* Thu Nov 17 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-1
- update to 1.17.0 release

* Wed Oct 19 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.1-1
- update to 1.16.1 release
- fix Orca speaking

* Thu Sep 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-1
- update to 1.16.0 release
- disable startup notification

* Sat Aug 13 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.4-1
- update to 1.15.4 release

* Wed Aug 10 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.3-3
- fix crash on changing wallpapers in non-compositor mode

* Mon Aug 08 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.3-2
- fix desktop background rendering in noncomposited mode

* Thu Aug 04 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.3-1
- update to 1.15.3 release

* Sun Jul 24 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.2-2
- fix desktop redraw issues with gtk+-3.21.4

* Sat Jul 02 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.2-1
- update to 1.15.2 release

* Sat Jul 02 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-1
- update to 1.15.1 release

* Mon Jun 27 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-2
- don't show color and image backgounds menu entry

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release
- switch to gtk+3

* Sat May 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.1-1
- update to 1.14.1 release

* Tue Apr 05 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release

* Mon Feb 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.1-1
- update to 1.13.1 release

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release
- try fix rhbz (#1291540)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 27 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.2-2
- add XFCE to OnlyShowIn in caja-browser.desktop

* Thu Dec 24 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.2-1
- update to 1.12.2 release
- remove upstreamed patch

* Tue Dec 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-2
- change cajas behaviour in xfce session, rhbz (#1278079)

* Tue Dec 01 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-1
- update to 1.12.1 release

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release

* Wed Oct 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release

* Fri Sep 25 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.4-1
- update to 1.10.4 release
- remove upstreamed patches

* Thu Sep 17 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.3-2
- fix crash if restore file from trash in f23
- do not save position from last window

* Tue Jul 21 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.3-1
- update to 1.10.3 release

* Thu Jul 16 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2.1
- update to 1.10.2 release
- remove upstreamed patches

* Sat Jul 11 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-7
- use new help dir

* Fri Jul 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-6
- revert 'allow caja --no-desktop in other desktops'

* Fri Jul 03 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-5
- use old help from 1.8

* Sun Jun 28 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.4
- improve double click detection
- no daemon mode in other desktop environments
- allow caja --no-desktop in other desktops

* Sat Jun 20 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.3
- fix caja help
- fix renaming of files (gtk3)
- add new bookmark behaviour
- drop old bookmarks patch

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1.1
- update to 1.10.1 release
- add bookmarks patch again
- avoid prelink to mess with caja rhbz (#1228874)

* Mon Apr 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Wed Feb 25 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90.1
- update to 1.9.90 release

* Tue Jan 13 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.4.1
- update to 1.9.4 release

* Tue Nov 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.3-1
- update to 1.9.3 release

* Sun Oct 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-1
- update to 1.9.2 release
- adjust obsoletes

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release
- move gtk-docs to -devel subpackage
- removed upstreamed patches

* Tue Jul 08 2014 Rex Dieter <rdieter@fedoraproject.org> 1.8.1-3
- optimize/update scriptlets

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1 release
- remove upstreamed patches

* Sat Mar 22 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- fix for x-caja-window issue, end of a long story
- remove consolekit usage
- don't use caja-autostart script anymore

* Tue Mar 04 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0
- Turn autoreconf bit back on. This is still needed for rpath issue.

* Sun Feb 23 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.91-0.1.git20140223.ee0a62
- update to latest git snapshot from 2014.02.23
- remove debuging patch, fix rhbz (#1067234)
- move autoreconf to the right place
- remove delay from caja-autostart for testing proposal
- remove non existent COPYING-DOCS
- disable gtk-docs for dit snapshot builds

* Wed Feb 12 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-2
- Add autoreconf -fi to fix rpath issues.

* Sun Feb 09 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.2-1
- Update to 1.7.2

* Tue Jan 14 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1
- remove glib-2.39 fix, already fixed in upstream
- use gtk-docs for release build

* Tue Dec 17 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.6.git20131201.0ef48fa
- fix build against new glib2-39.2, 'g_memmove' is removed
- https://git.gnome.org/browse/glib/commit/?id=6e4a7fca431f53fdfd89afbe956212229cf52200

* Tue Dec 17 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.5.git20131201.0ef48fa
- new patch for x-caja-window issue, it surpress creating x-caja-desktop-windows
- rename patches
- fix provides
- use modern 'make install' macro
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser

* Sun Dec 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.4.git0ef48fab
- add mimeinfo rpm scriplets again

* Sun Dec 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.3.git0ef48fab
- fix usage of %%{buildroot}
- use desktop-database rpm scriptlet instead of mimeinfo scriptlet

* Sat Dec 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.2.git0ef48fab
- fix all the macro-in-comment warnings
- add ldconfig scriptlets for the extension subpackage
- add versioned provides for the obsoleted packages
- remove licence tags from subpackages
- remove group tags from subpackages
- fix permission for caja-autostart script

* Thu Dec 05 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.git0ef48fab
- rename mate-file-manager to caja for f21
- use latest git snapshot, 2013.12.05

* Thu Dec 05 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0

* Thu Oct 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.7.gitbf47018
- add add autostart script to desktop file

* Thu Oct 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.6.gitbf47018
- add a 3 secs delay for caja autostart and restart if killed

* Mon Oct 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.5.gitbf47018
- add new caja-sidebar design for f20

* Mon Oct 07 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.4.gitbf47018
- allow dropping files to bookmarks
- fix https://github.com/mate-desktop/mate-file-manager/issues/122

* Sun Oct 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.3.gitbf47018
- fix caja crash if closing properties windows on dropbox folder

* Sun Sep 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.2.git73cc7e9
- update latest git snapshot
- fix rhbz (#1005660)
- change open folders in spatial-mode
- fix spatial mode crash and shift+double click
- https://github.com/mate-desktop/mate-file-manager/issues/120
- https://github.com/mate-desktop/mate-file-manager/issues/161
- fixed thumbnail frame not being displayed for some files
- https://github.com/mate-desktop/mate-file-manager/issues/135

* Wed Sep 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.3-0.1.git6278dcb
- update latest git snapshot
- fix rhbz (959444)
- remove upstreamed mate-file-manager_fix_privat-icons-dir.patch

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-3
- move gsettings schemas to -schemas subpackage, to fix #959607
- move locale to -schemas subpackage
- remove runtime require hicolor-icon-theme

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 20 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.2-1
- update to new upstream release
- remove in release included mate-file-manager_fix-radio-buttons.patch
- add  upstream mate-file-manager_fix_privat-icons-dir.patch
- remove needless runtime require gsettings-desktop-schemas
- remove runtime require mate-icon-theme

* Mon Jul 01 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-9
- set autostart to false in caja-autostart, fix rhbz #969663
- and #978598

* Sun Jun 30 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-8
- add mate-file-manager_fix-radio-buttons.patch to fix rhbz #964357
- clean up BR's
- add runtime require hicolor-icon-theme
- revert 1.6.1-7 changes

* Thu Jun 20 2013 Dan Mashal <dan.mashal@fedoraproejct.org> - 1.6.1-7
- Try caja without the autostart file (886029)

* Sat Jun 15 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-6
- remove gsettings convert file

* Thu Jun 06 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-5
- add AutostartCondition to caja-autostart.desktop

* Wed May 22 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-4
- workaround for x-caja-desktop window issue
- add caja-autostart desktopfile to /etc/xdg/autostart

* Wed May 15 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-3
- Fix previous commit

* Tue May 14 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-2
- Own libdir/caja (961992)

* Thu Apr 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.1-1
- Update to latest upstream release.

* Wed Apr 03 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.6.0-1
- Update to latest 1.6.0 stable release.

* Mon Mar 11 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.5-1
- Update to latest upstream release

* Sat Mar 02 2013 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.4-1
- Update to latest upstream release
- Add upstream patch

* Mon Dec 03 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 release
- Drop all patches
- Update configure flags
- Clean up spec file

* Sun Nov 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-2
- upload source again as upstream switched it
- specfile cleanup

* Fri Nov 23 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- update to 1.5.1 release
- drop upstream commits patch and other merged patch
- change source url and fix packagename in %%prep to suit

* Thu Nov 22 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-6
- update commits patch

* Tue Nov 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-5
- add git commits rollup patch, hopefully it fixes rhbz 868472
- drop merged patch

* Mon Nov 19 2012 Dan Mashal <dan.mashal@fedoraproject.org> - 1.5.0-4
- This change was reverted

* Sun Nov 11 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-3
- add patch to call gdk_pixbuf_loader_close() earlier (#558267)
- fix mistake in scriptlets

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-2
- add requires gsettings-desktop-schemas
- add build requires gsettings-desktop-schemas-devel

* Mon Oct 29 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.5.0-1
- update to 1.5.0 release
- add schema scriptlets and remove mateconf scriptlets
- drop un-needed requires and build requires and change style
- make directory for extensions and move to main package
- drop all patches not needed for building for now
- clean up spec file

* Thu Oct 18 2012 Rex Dieter <rdieter@fedoraproject.org> - 1.4.0-12
- fix mate-doc xml error (patch out reference to non-existent caja-extension-i18n.xml)
- verbose build

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-11
- Drop caja_remove_mate-bg-crossfade patch as it was causing crash

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-10
- add patch to try and fix crash

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-9
- revert last commit "add autostart file for caja desktop"
- add no session delay patch

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-8
- add autostart file for caja desktop
- add build requires libxml2-devel

* Mon Aug 20 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-7
- remove obsoleting stuff

* Thu Aug 16 2012 Rex Dieter <rdieter@fedoraproject.org> 1.4.0-6
- drop needless ldconfig scriptlet on main pkg

* Mon Aug 13 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-5
- fix desktop file handle
- fix obsolete caja from external repo

* Sun Aug 12 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-4
- correct %%build section
- correct rpm scriplets
- correct %%prep section
- change .*z to .* in %%file section
- correct obsoletes
- some other fixes

* Sun Aug 12 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-3
- obsoleting caja from external repo
- remove unecessary build requires

* Tue Aug 07 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-2
- initial package for fedora

* Sun Dec 25 2011 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- mate-file-manager.spec based on nautilus-2.32.0-1.fc14 spec

## END: Generated by rpmautospec
