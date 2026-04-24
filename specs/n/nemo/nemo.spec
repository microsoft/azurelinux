# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit0 32ab5b1c7893054b266afaa6c88b45c43e8ebd25
%global date 20231109
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

Name:           nemo
Summary:        File manager for Cinnamon
Version:        6.4.5
Release: 3%{?dist}
# Automatically converted from old format: GPLv2+ and LGPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+
URL:            https://github.com/linuxmint/%{name}
%if 0%{?tag:1}
Source0: %url/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0: %url/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif
Source1:        nemo-fedora.gschema.override
Patch0:         remove_desktop_search.patch
Patch1:         Don-t-scale-text-size-when-zooming.patch

ExcludeArch:   %{ix86}

Requires:       redhat-menus
Requires:       gvfs-fuse%{?_isa}
Requires:       gvfs-goa%{?_isa}
Requires:       xapps%{?_isa} >= 2.2.0
# required for for gtk-stock fallback
Requires:       adwaita-icon-theme
Recommends:     cinnamon-translations >= 6.4.0
Recommends:     nemo-search-helpers
Recommends:     folder-color-switcher-nemo

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  intltool
BuildRequires:  python3-gobject-base
BuildRequires:  python3-packaging
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk+-wayland-3.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-no-export-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(cinnamon-desktop) >= 6.4.0
BuildRequires:  pkgconfig(gail-3.0)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xapp) >= 2.2.0
BuildRequires:  pkgconfig(exempi-2.0)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libgsf-1)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(pango)

# the main binary links against libnemo-extension.so
# don't depend on soname, rather on exact version
Requires:       %{name}-extensions%{?_isa} = %{version}-%{release}

%description
Nemo is the file manager and graphical shell for the Cinnamon desktop
that makes it easy to manage your files and the rest of your system.
It allows to browse directories on local and remote filesystems, preview
files and launch applications associated with them.
It is also responsible for handling the icons on the Cinnamon desktop.

%package extensions
Summary: Nemo extensions library
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2+
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description extensions
This package provides the libraries used by nemo extensions.

%package search-helpers
Summary: Nemo search helpers
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2+
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   exif
Requires:   ghostscript
Requires:   odt2txt
Requires:   poppler-utils
Requires:   python3-xlrd

%description search-helpers
This package provides the search helpers used by nemo.


%package devel
Summary: Support for developing nemo extensions
# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License: LicenseRef-Callaway-LGPLv2+
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   %{name}-extensions%{?_isa} = %{version}-%{release}


%description devel
This package provides libraries and header files needed
for developing nemo extensions.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

%build
%meson \
  -D deprecated_warnings=false \
  -D gtk_doc=false \
  -D selinux=true
%meson_build

%install
%meson_install

install -D -m 0644 %{SOURCE1} %{buildroot}/%{_datadir}/glib-2.0/schemas/nemo-fedora.gschema.override

# Only autostart in cinnamon and budgie
desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  --add-only-show-in "X-Cinnamon;Budgie" \
  %{buildroot}%{_datadir}/applications/nemo-autostart.desktop
desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/{nemo,nemo-autorun-software}.desktop

# create extensions directoy
mkdir -p %{buildroot}%{_libdir}/nemo/extensions-3.0/

rm %{buildroot}%{_datadir}/nemo/search-helpers/id3.nemo_search_helper
rm %{buildroot}%{_datadir}/nemo/search-helpers/pdf2txt.nemo_search_helper

%ldconfig_scriptlets extensions

%files
%doc AUTHORS NEWS
%license COPYING COPYING-DOCS
%{_bindir}/nemo
%{_bindir}/nemo-autorun-software
%{_bindir}/nemo-connect-server
%{_bindir}/nemo-desktop
%{_bindir}/nemo-action-layout-editor
%{_bindir}/nemo-open-with
%{_libexecdir}/nemo-*
%dir %{_datadir}/nemo/
%{_datadir}/nemo/action-info.md
%{_datadir}/nemo/nemo-action-layout-editor-resources.gresource
%{_datadir}/nemo/actions/
%{_datadir}/nemo/icons/
%{_datadir}/nemo/layout-editor/
%{_datadir}/nemo/script-info.md
%{_datadir}/applications/*
%{_datadir}/mime/packages/nemo.xml
%{_datadir}/icons/hicolor/*/*/*.png
%{_datadir}/icons/hicolor/scalable/*/*.svg
%{_datadir}/dbus-1/services/nemo*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/polkit-1/actions/org.nemo.root.policy
%{_datadir}/gtksourceview-*/language-specs/nemo_*.lang
%{_mandir}/man1/nemo*

%files extensions
%license COPYING.EXTENSIONS COPYING.LIB
%{_libdir}/libnemo-extension.so.*
%{_libdir}/nemo/
%{_libdir}/girepository-1.0/Nemo-3.0.typelib

%files search-helpers
%{_bindir}/nemo-epub2text
%{_bindir}/nemo-mso-to-txt
%{_bindir}/nemo-odf-to-txt
%{_bindir}/nemo-ppt-to-txt
%{_bindir}/nemo-xls-to-txt
%{_datadir}/nemo/search-helpers/

%files devel
%{_includedir}/nemo/
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 26 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.5-1
- Update to 6.4.5

* Sat Feb 08 2025 Leigh Scott <leigh123linux@gmail.com> - 6.4.4-1
- Update to 6.4.4

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 06 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.3-1
- Update to 6.4.3

* Mon Dec 02 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.1-1
- Update t0 6.4.1

* Wed Nov 27 2024 Leigh Scott <leigh123linux@gmail.com> - 6.4.0-1
- Update to 6.4.0

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 6.2.8-2
- convert license to SPDX

* Tue Aug 13 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.8-1
- Update to 6.2.8

* Sat Jul 20 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.5-1
- Update to 6.2.5

* Wed Jul 17 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.4-1
- Update to 6.2.4

* Mon Jul 08 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.3-1
- Update to 6.2.3

* Tue Jun 18 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.1-1
- Update to 6.2.1

* Thu Jun 13 2024 Leigh Scott <leigh123linux@gmail.com> - 6.2.0-1
- Update to 6.2.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 12 2024 Leigh Scott <leigh123linux@gmail.com> - 6.0.2-2
- Add buildrequires python3-packaging

* Fri Dec 29 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.2-1
- Update to 6.0.2 release

* Tue Dec 19 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.1-1
- Update to 6.0.1 release

* Sun Nov 19 2023 Leigh Scott <leigh123linux@gmail.com> - 6.0.0-1
- Update to 6.0.0 release

* Thu Nov 09 2023 Leigh Scott <leigh123linux@gmail.com> - 5.9.0-1.20231109git32ab5b1
- Update to git snapshot

* Fri Nov 03 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.5-3
- Add recommends folder-color-switcher-nemo

* Sat Sep 23 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.5-2
- Show nemo app in other DE's

* Fri Sep 22 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.5-1
- Update to 5.8.5 release

* Mon Aug 14 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.4-3
- Add requires gvfs-fuse

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 09 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.4-1
- Update to 5.8.4 release

* Tue Jun 27 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.3-1
- Update to 5.8.3 release

* Thu Jun 08 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.1-1
- Update to 5.8.1 release

* Fri Jun 02 2023 Leigh Scott <leigh123linux@gmail.com> - 5.8.0-1
- Update to 5.8.0 release

* Mon Mar 20 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.4-1
- Update to 5.6.4 release

* Sat Feb 04 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.2-3
- Add Budgie to OnlyShowIn

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 08 2023 Leigh Scott <leigh123linux@gmail.com> - 5.6.2-1
- Update to 5.6.2 release

* Tue Dec 13 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.1-1
- Update to 5.6.1 release

* Mon Nov 21 2022 Leigh Scott <leigh123linux@gmail.com> - 5.6.0-1
- Update to 5.6.0 release

* Mon Aug 15 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.3-1
- Update to 5.4.3 release

* Wed Jul 27 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.2-1
- Update to 5.4.2 release

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.1-1
- Update to 5.4.1 release

* Sat Jun 11 2022 Leigh Scott <leigh123linux@gmail.com> - 5.4.0-1
- Update to 5.4.0 release

* Sat May 28 2022 Leigh Scott <leigh123linux@gmail.com> - 5.2.4-1
- Update to 5.2.4 release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 01 2022 Leigh Scott <leigh123linux@gmail.com> - 5.2.3-1
- Update to 5.2.3 release

* Thu Dec 16 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.2-1
- Update to 5.2.2 release

* Thu Dec 09 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.1-1
- Update to 5.2.1 release

* Fri Nov 19 2021 Leigh Scott <leigh123linux@gmail.com> - 5.2.0-1
- Update to 5.2.0 release

* Thu Nov 04 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.5-1
- Update to 5.0.5 release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.3-1
- Update to 5.0.3 release

* Fri Jun 25 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.2-1
- Update to 5.0.2 release

* Fri Jun 18 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.1-2
- Move search helpers to sub-package

* Thu Jun 10 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.1-1
- Update to 5.0.1 release

* Fri May 28 2021 Leigh Scott <leigh123linux@gmail.com> - 5.0.0-1
- Update to 5.0.0 release

* Fri Mar 05 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.6-1
- Update to 4.8.6 release

* Mon Mar 01 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.5-1
- Update to 4.8.5 release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan  3 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.4-1
- Update to 4.8.4 release

* Sat Jan  2 2021 Leigh Scott <leigh123linux@gmail.com> - 4.8.3-1
- Update to 4.8.3 release

* Tue Dec  8 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.2-1
- Update to 4.8.2 release

* Tue Dec  8 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.1-1
- Update to 4.8.1 release

* Thu Nov 26 2020 Leigh Scott <leigh123linux@gmail.com> - 4.8.0-1
- Update to 4.8.0 release

* Tue Aug 11 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.5-1
- Update to 4.6.5 release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 21 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.4-1
- Update to 4.6.4 release

* Sat Jun 06 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.3-1
- Update to 4.6.3 release

* Wed May 27 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.2-1
- Update to 4.6.2 release

* Thu May 21 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.1-1
- Update to 4.6.1 release

* Wed May 13 2020 Leigh Scott <leigh123linux@gmail.com> - 4.6.0-1
- Update to 4.6.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Leigh Scott <leigh123linux@googlemail.com> - 4.4.2-3
- Add patch to fix gcc-10 compile issue

* Thu Jan 23 2020 Leigh Scott <leigh123linux@googlemail.com> - 4.4.2-2
- Workaround gcc-10 issue till upstream addresses it

* Thu Dec 12 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.2-1
- Update to 4.4.2 release

* Mon Dec 09 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.1-3
- Add patch to fix 'Disable GLib deprecation warnings'

* Mon Dec 09 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.1-2
- Add patch to fix 'Don't hyphenate long filenames'
- Add patch to fix 'fix copying from the trash'

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.1-1
- Update to 4.4.1 release

* Sat Nov 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.4.0-1
- Update to 4.4.0 release

* Fri Sep 06 2019 Nikola Forró <nforro@redhat.com> - 4.2.3-2
- Rebuilt for exempi 2.5.1

* Wed Aug 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.3-1
- Update to 4.2.3 release

* Wed Jul 31 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.2-1
- Update to 4.2.2 release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 14 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.1-1
- Update to 4.2.1 release

* Sun Jun 23 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.2.0-1
- Update to 4.2.0 release

* Tue Jun 18 2019 Leigh Scott <leigh123linux@googlemail.com> - 4.0.6-3
- Fix gtk-3.24.8 scroll issue

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 16 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.6-1
- Update to 4.0.6 release

* Thu Dec 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.4-1
- Update to 4.0.4 release

* Tue Nov 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.3-1
- Update to 4.0.3 release

* Tue Nov 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.2-1
- Update to 4.0.2 release

* Mon Nov 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.1-1
- Update to 4.0.1 release

* Thu Nov 01 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.0.0-1
- Update to 4.0.0 release

* Sun Oct 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.6-2
- Drop EPEL/RHEL support

* Fri Sep 21 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.6-1
- Update to 3.8.6 release

* Thu Aug 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.5-1
- Update to 3.8.5 release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.4-1
- Update to 3.8.4 release

* Fri Jun 08 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.3-1
- Update to 3.8.3 release

* Sun May 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.2-1
- Update to 3.8.2 release

* Tue May 01 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.1-1
- Update to 3.8.1 release

* Fri Apr 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.8.0-1
- Update to 3.8.0 release

* Sun Apr 15 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.9.20180415gitd0e6d21
- update to git snapshot

* Sun Apr 08 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.8.20180407git6fe68b0
- update to git snapshot

* Mon Apr 02 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.7.20180316gitb78adbc
- update to git snapshot

* Fri Mar 09 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.6.20180309git86927cb
- update to git snapshot

* Sat Feb 10 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.5.20180210gitd6348aa
- update to git snapshot

* Tue Feb 06 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.4.20180206gita5bf015
- update to git snapshot

* Mon Feb 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.3.20180205git1a20ae1
- Fix some minor issues

* Mon Feb 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.2.20180205git1a20ae1
- update to git snapshot

* Mon Feb 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 3.6.6-0.1.20180205git7723f6a
- update to git snapshot

* Mon Dec 18 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.5-1
- update to 3.6.5 release

* Mon Nov 20 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.4-1
- update to 3.6.4 release

* Fri Nov 17 2017 Björn Esser <besser82@fedoraproject.org> - 3.6.3-1
- update to 3.6.3 release

* Thu Oct 26 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.2-2
- Add upstream fix for desktop scale

* Tue Oct 24 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.2-1
- update to 3.6.2 release

* Tue Oct 24 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.6.1-1
- update to 3.6.1 release

* Sat Sep 09 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.7-8
- Add several more fixes for gDrive

* Fri Sep 08 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.7-7
- Fix renaming on gDrive

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.7-6
- Preserve mode of files when changing hashbang

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.7-5
- Fix regex for EPEL

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.7-4
- Use Python2 on EPEL <= 7

* Thu Aug 31 2017 Björn Esser <besser82@fedoraproject.org> - 3.4.7-3
- Adjustments for EPEL7

* Wed Aug 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.7-2
- fix desktop file

* Wed Aug 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.7-1
- update to 3.4.7 release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 06 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.6-1
- update to 3.4.6 release

* Mon Jun 26 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.5-1
- update to 3.4.5 release
- Disable verbose build

* Sun Jun 25 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.4-2
- Fix control-n (new window) action callback when used from
  the desktop process

* Thu Jun 22 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.4-1
- update to 3.4.4 release
- Remove build requires rarian-compat

* Thu Jun 22 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.3-2
- Add patch to fix desktop auto-layout crash.

* Wed Jun 21 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.3-1
- update to 3.4.3 release

* Sun Jun 04 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.2-2
- Remove desktop search
- Remove nemo-desktop decoration
- Fix scaling issue in 'List View' zoom

* Tue May 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.2-1
- update to 3.4.2 release

* Sat May 06 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.0-2
- Add upstream fix for desktop hidpi scaling

* Thu May 04 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.4.0-1
- update to 3.4.0 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Björn Esser <besser82@fedoraproject.org> - 3.2.2-4
- Use Noto Sans font on Fedora 24+, too

* Sun Jan 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 3.2.2-3
- Clean up

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.2.2-2
- Rebuild for Python 3.6

* Mon Dec 12 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.2-1
- update to 3.2.2 release

* Sat Dec 10 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.1-1
- update to 3.2.1 release

* Tue Nov 22 2016 leigh scott <leigh123linux@googlemail.com> - 3.2.0-2
- add 'send by email' action for thunderbird

* Mon Nov 07 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.2.0-1
- update to 3.2.0 release

* Fri Oct 28 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.7-2.git6e2dcd3
- update to latest git snapshot

* Mon Oct 24 2016 leigh scott <leigh123linux@googlemail.com> - 3.0.7-1.git6c2a9ca
- update to git snapshot

* Tue Oct 11 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.6-6
- rebuilt

* Sun Jul 24 2016 leigh scott <leigh123linux@googlemail.com> - 3.0.6-5
- rebuilt yet again (gtk-3.21.3 desktop window redraw issue)

* Sun Jul 24 2016 leigh scott <leigh123linux@googlemail.com> - 3.0.6-4
- rebuilt

* Sat Jul 23 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.6-3
- fix gtk-3.21.3 desktop window redraw issue

* Sun Jul 10 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.6-2
- remove unwanted build flags

* Fri Jun 24 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.6-1
- update to 3.0.6 release

* Fri Jun 17 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.5-3
- change source tag
- fix log spam

* Sun Jun 05 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.5-2
- fix scrolled window issue (raveit65)

* Tue May 31 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.5-1
- update to 3.0.5 release

* Thu May 26 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.3-2
- fix desktop font highlighting when renaming (raveit65)

* Tue May 24 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.3-1
- update to 3.0.3 release

* Fri May 20 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.2-1
- update to 3.0.2 release

* Wed May 11 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.1-1
- update to 3.0.1 release

* Sun Apr 24 2016 Leigh Scott <leigh123linux@googlemail.com> - 3.0.0-1
- update to 3.0.0 release

* Sat Mar 26 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.8.7-3
- fix another gtk-3.19 issue

* Fri Mar 25 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.8.7-2
- fix gtk-3.19 issue

* Wed Mar 09 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.8.7-1
- update to 2.8.7 release

* Thu Feb 18 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.8.6-4
- add another style class patch (raveit65)
- add only show in cinnamon for desktop files

* Sun Feb 14 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.8.6-3
- fix gcc-6.0 compile error
- add style classes patch (raveit65)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.6-1
- update to 2.8.6 release
- patch to fix bz 1287917 & 1288324

* Sat Nov 21 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.5-1
- update to 2.8.5 release

* Mon Nov 09 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.2-2
- rebuilt

* Mon Nov 09 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.2-1
- update to 2.8.2 release
 
* Mon Oct 26 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.1-1
- update to 2.8.1 release

* Thu Oct 22 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.8.0-1
- update to 2.8.0 release

* Tue Sep 01 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.7-2
- fix deprecation warning

* Sun Jun 28 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.7-1
- update to 2.6.7 release
- clean up scriptlets

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.6-1
- update to 2.6.6 release
- drop adwaita sub-package

* Thu Jun 11 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.5-2
- fix extension list for 64bit
- add patch for preferences

* Wed May 27 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.5-1
- update to 2.6.5 release

* Mon May 25 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.4-1
- update to 2.6.4 release

* Thu May 21 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.3-1
- update to 2.6.3 release

* Thu May 21 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.2-1
- update to 2.6.2 release

* Wed May 20 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.1-1
- update to 2.6.1 release

* Wed May 20 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.6.0-1
- update to 2.6.0 release

* Sat May 16 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.5.0-0.2.gita06e815
- update to git snapshot

* Tue May 05 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.5.0-0.1.git1afb0a3
- update to git snapshot

* Thu Apr 02 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.5-2
- drop merged patch

* Thu Apr 02 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.5-1
- update to 2.4.5

* Sun Jan 18 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.4-4
- f20 also needs a adwaita fix

* Sun Jan 18 2015 Leigh Scott <leigh123linux@googlemail.com> - 2.4.4-3
- add patch to fix statusbar size

* Sun Dec 21 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.4-2
- add patch to fix nemo desktop font colour
- raise thunbnail file size limit

* Wed Nov 26 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.4-1
- update to 2.4.4

* Sun Nov 23 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.3-1
- update to 2.4.3

* Wed Nov 12 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.2-1
- update to 2.4.2

* Fri Oct 31 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-1
- update to 2.4.0

* Tue Oct 28 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.3.gitb157906
- update to latest git

* Fri Oct 10 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.2.git88705b5
- update to latest git

* Tue Sep 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.4.0-0.1.git676b171
- update to latest git

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.4-1
- update to 2.2.4
- drop upstream patch

* Tue Aug 12 2014 Rex Dieter <rdieter@fedoraproject.org> 2.2.3-3
- update mime scriptlet

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 2.2.3-2
- Rebuilt for gobject-introspection 1.41.4

* Fri Jun 27 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.3-1
- update to 2.2.3

* Tue Jun 17 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.2-4
- Fix bookmark crash when umount

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.2-2
- add requires gnome-icon-theme-legacy

* Wed May 21 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.2-1
- update to 2.2.2

* Fri May 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.1-1
- update to 2.2.1

* Sat Apr 12 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.2.0-1
- update to 2.2.0

* Mon Mar 03 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-9
- remove tracker support (bz 1071601) so search works
- fix adwaita-nemo theme issue (bz 1066547)

* Thu Feb 20 2014 Adam Williamson <awilliam@redhat.com> - 2.0.8-8
- rebuild against updated tracker

* Fri Jan 24 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-7
- fix adwaita theme issue

* Thu Jan 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-6
- patch to make background transparent

* Thu Jan 02 2014 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-5
- hopefully fix rename position issue (bz 1045181)

* Mon Dec 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-4
- add patch to build against tracker-1.8

* Mon Dec 23 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-3
- change tracker build requires

* Sun Dec 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-2
- add git rollup patch (bz 1045181)

* Mon Dec 02 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.8-1
- update to 2.0.8

* Sun Nov 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.7-1
- update to 2.0.7

* Sun Nov 03 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.5-1
- update to 2.0.5

* Thu Oct 31 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.4-1
- update to 2.0.4
- add obsoletes nemo-open-terminal

* Wed Oct 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.3-1
- update to 2.0.3

* Thu Oct 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.2-1
- update to 2.0.2

* Sun Oct 20 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-2
- add obsoletes nemo-seahorse

* Fri Oct 18 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.1-1
- update to 2.0.1

* Wed Oct 09 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-2
- rebuilt with tracker support

* Wed Oct 02 2013 Leigh Scott <leigh123linux@googlemail.com> - 2.0.0-1
- update to 2.0.0

* Tue Oct 01 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.1-2
- set some defaults

* Mon Sep 30 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.9.1-1
- update to 1.9.1

* Thu Sep 26 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.6-0.8.git60e40aa
- update to latest git

* Thu Sep 19 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.6-0.7.git1c25115
- update to latest git

* Thu Sep 19 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.6-0.6.git07ae0a8
- update to latest git

* Wed Sep 18 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.6-0.5.gitea09d20
- update to latest git

* Sun Aug 25 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.6-0.4.gitfccc703
- update to latest git
- Change buildrequires to cinnamon-desktop-devel
- Change requires to cinnamon-desktop

* Sat Aug 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.6-0.3.git9d08c6c
- add requires cinnamon-translations

* Sat Aug 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.6-0.2.git9d08c6c
- update to latest git

* Sat Aug 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.6-0.1.gitb2776a2
- update to latest git
- adjust for new cinnamon-translations package

* Thu Aug 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.5-3
- rebuilt

* Wed Aug 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.5-2
- supress gtk DEPRECATED

* Wed Aug 21 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.5-1
- Update to version 1.8.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.4-4
- add requires beesu
- drop patch to remove open as root

* Wed Jul 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.4-3
- remove background patch as it breaks cinnamon next

* Mon Jul 22 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.4-2
- patch to fix create launcher

* Wed Jul 10 2013 leigh scott <leigh123linux@googlemail.com> - 1.8.4-1
- Update to version 1.8.4

* Thu Jun 06 2013 leigh scott <leigh123linux@googlemail.com> - 1.8.2-3
- autostart nemo differently so we dont squash nautilus

* Fri May 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.2-2
- Patch to remove open as root

* Mon May 20 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.2-1
- Update to version 1.8.2
- Tidy up patches

* Sun May 12 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.1-2
- add patch to stop nemo from drawing the desktop background

* Thu May 09 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.8.1-1
- update to 1.8.1 release

* Sun Feb 24 2013 Leigh Scott <leigh123linux@googlemail.com> - 1.1.2-4
- Rebuilt for libgnome-desktop soname bump
- Patch for gnome-desktop changes

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 1.1.2-2
- Rebuilt for libgnome-desktop-3 3.7.3 soname bump

* Wed Nov 14 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.1.2-1
- update to 1.1.2 release
- add scriptlets for mimetype key

* Sat Nov 03 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.9-1
- update to 1.0.9 release

* Sun Oct 28 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-1
- update to 1.0.7 release
- change build requires style
- use autogen to prepare source
- make directory for extensions

* Sun Oct 21 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.5-2
- drop requires gksu-pokit

* Sat Oct 20 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.5-1
- update to 1.0.5 release
- revert last commit

* Thu Oct 18 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-3
- patch open as root and add requires gksu-pokit

* Mon Oct 08 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-2
- remove requires gnome-terminal
- patch to remove "open in terminal"

* Mon Oct 01 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-1
- update to 1.0.3 release

* Thu Sep 27 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.2-1
- update to 1.0.2 release
- add requires gnome-terminal

* Tue Sep 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-5
- add theme sub-package

* Tue Sep 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-4
- remove "open as root" option
- fix "open terminal" option

* Tue Sep 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-3
- validate desktop file

* Tue Sep 25 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-2
- add ldconfig to extensions
- fix comment in macro
- fix macro-in-comment
- remove obsolete provides/obsoletes
- fix licence tag

* Fri Sep 21 2012 Leigh Scott <leigh123linux@googlemail.com> - 1.0.1-1
- initial build based on nautilus spec file

