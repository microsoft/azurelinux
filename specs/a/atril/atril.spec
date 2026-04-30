## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


Name:          atril
Version:       1.28.1
Release:       %autorelease
Summary:       Document viewer
# Automatically converted from old format: GPLv2+ and LGPLv2+ and MIT - review is highly recommended.
License:       GPL-2.0-or-later AND LicenseRef-Callaway-LGPLv2+ AND LicenseRef-Callaway-MIT
URL:           http://mate-desktop.org
Source0:       http://pub.mate-desktop.org/releases/1.28/%{name}-%{version}.tar.xz

BuildRequires: gcc-c++
BuildRequires: gtk3-devel
BuildRequires: poppler-glib-devel
BuildRequires: libarchive-devel
BuildRequires: libXt-devel
BuildRequires: libsecret-devel
BuildRequires: libtiff-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libspectre-devel
BuildRequires: desktop-file-utils
BuildRequires: gobject-introspection-devel
BuildRequires: make
BuildRequires: mate-common
BuildRequires: mate-desktop-devel
BuildRequires: cairo-gobject-devel
BuildRequires: yelp-tools

# for the xps back-end
BuildRequires: libgxps-devel
# for the caja properties page
BuildRequires: caja-devel
# for the dvi back-end
BuildRequires: texlive-lib-devel
# for the djvu back-end
BuildRequires: djvulibre-devel
# for epub back-end
BuildRequires: webkit2gtk4.1-devel

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
#  fix (#974791)
Requires:       mate-desktop-libs
Requires:       mathjax

%description
Mate-document-viewer is simple document viewer.
It can display and print Portable Document Format (PDF),
PostScript (PS), Encapsulated PostScript (EPS), DVI, DJVU, epub and XPS files.
When supported by the document format, mate-document-viewer
allows searching for text, copying text to the clipboard,
hypertext navigation, table-of-contents bookmarks and editing of forms.


%package libs
Summary: Libraries for the mate-document-viewer

%description libs
This package contains shared libraries needed for mate-document-viewer.


%package devel
Summary: Support for developing back-ends for the mate-document-viewer
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files needed for
mate-document-viewer back-ends development.


%package caja
Summary: Mate-document-viewer extension for caja
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: caja

%description caja
This package contains the mate-document-viewer extension for the
caja file manager.
It adds an additional tab called "Document" to the file properties dialog.

%package thumbnailer
Summary: Atril thumbnailer extension for caja
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: caja

%description thumbnailer
This package contains the atril extension for the
caja file manager.


%prep
%autosetup -p1
#NOCONFIGURE=1 ./autogen.sh

%build
%configure \
        --disable-static \
        --disable-schemas-compile \
        --enable-introspection \
        --enable-comics \
        --enable-dvi=yes \
        --enable-djvu=yes \
        --enable-t1lib=no \
        --enable-pixbuf \
        --enable-xps \
        --enable-epub \
        --enable-synctex

# remove unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

make %{?_smp_mflags} V=1


%install
%{make_install}

%find_lang %{name} --with-gnome --all-name

find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'


%check
desktop-file-validate ${RPM_BUILD_ROOT}%{_datadir}/applications/atril.desktop


%files -f %{name}.lang
%doc README.md COPYING NEWS AUTHORS
%{_bindir}/*
%dir %{_datadir}/atril
%{_datadir}/atril/*
%{_datadir}/applications/atril.desktop
%{_datadir}/icons/hicolor/*/apps/atril.*
%{_libexecdir}/atrild
%{_datadir}/dbus-1/services/org.mate.atril.Daemon.service
%{_datadir}/glib-2.0/schemas/org.mate.Atril.gschema.xml
%{_datadir}/metainfo/atril.appdata.xml
%{_mandir}/man1/atril-*.1.*
%{_mandir}/man1/atril.1.*

%files libs
%{_libdir}/libatrilview.so.*
%{_libdir}/libatrildocument.so.*
%{_libdir}/atril/3/backends/
%{_libdir}/girepository-1.0/AtrilDocument-1.5.0.typelib
%{_libdir}/girepository-1.0/AtrilView-1.5.0.typelib

%files caja
%{_libdir}/caja/extensions-2.0/libatril-properties-page.so
%{_datadir}/caja/extensions/libatril-properties-page.caja-extension

%files thumbnailer
%{_datadir}/thumbnailers/atril.thumbnailer

%files devel
%dir %{_includedir}/atril/
%{_includedir}/atril/1.5.0/
%{_libdir}/libatrilview.so
%{_libdir}/libatrildocument.so
%{_libdir}/pkgconfig/atril-view-1.5.0.pc
%{_libdir}/pkgconfig/atril-document-1.5.0.pc
%{_datadir}/gir-1.0/AtrilDocument-1.5.0.gir
%{_datadir}/gir-1.0/AtrilView-1.5.0.gir
%{_datadir}/gtk-doc/html/libatrildocument-1.5.0/
%{_datadir}/gtk-doc/html/libatrilview-1.5.0/
%{_datadir}/gtk-doc/html/atril/


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 1.28.1-4
- test: add initial lock files

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Feb 26 2025 raveit65 <mate@raveit.de> - 1.28.1-2
- update to 1.28.1

* Wed Feb 26 2025 raveit65 <mate@raveit.de> - 1.28.1-1
- update to 1.28.1

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 1.28.0-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.28.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Feb 23 2024 Wolfgang Ulbrich <fedora@raveit.de> - 1.28.0-1
- update to 1.28.0

* Wed Jan 31 2024 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.2-2
- fix gcc14 build error and another epub crash
- use https://github.com/mate-desktop/atril/commit/479e927
- use https://github.com/mate-desktop/atril/commit/d901a9d

* Wed Jan 24 2024 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.2-1
- update to 1.26.2

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.1-2
- switch to webkit2gtk4.1

* Fri Apr 28 2023 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.1-1
- update to 1.26.1 release

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 06 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.26.0-1
- update to 1.26.0 release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 23 2021 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.1-1
- update to 1.24.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.24.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-2
- drop libglade2 build requires

* Tue Feb 11 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.24.0-1
- update to 1.24.0

* Mon Feb 03 2020 Wolfgang Ulbrich <fedora@raveit.de> - 1.23.2-1
- update to 1.23.2

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Marek Kasik <mkasik@redhat.com> - 1.22.3-2
- Rebuild for poppler-0.84.0

* Sun Dec 08 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.3-1
- update to 1.22.3

* Sat Nov 23 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.2-2
- use https://github.com/mate-desktop/atril/commit/ecd0d8c
- Reset text selection after Drag and Drop

* Wed Sep 18 2019 Wolfgang Ulbrich <fedora@raveit.de> - 1.22.2-1
- update to 1.22.2

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

* Thu Jul 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.20.2-3
- Add BuildRequires gcc-c++

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-1
- update to 1.20.2
- use webkit2gtk3-devel for f28

* Tue Mar 27 2018 Wolfgang Ulbrich <fedora@raveit.de> - 1.20.1-1
- update to 1.20.1

* Fri Mar 16 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-2
- fix for rhbz (#1554134)

* Sun Feb 11 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.20.0-1
- update to 1.20.0 release
- drop desktop-database rpm scriptlet
- drop GSettings Schema rpm scriptlet
- drop IconCache Schema rpm scriptlet
- switch to using autosetup

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Tomas Popela <tpopela@redhat.com> - 1.19.6-3
- Adapt to the webkitgtk4 rename

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.19.6-2
- Remove obsolete scriptlets

* Thu Jan 04 2018 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.6-1
- update to 1.19.6
- fixes https://bugzilla.redhat.com/show_bug.cgi?id=1525313

* Mon Nov 27 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.5-1
- update to 1.19.5

* Thu Nov 23 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.4-2
- fix rhbz (#1513826)

* Sat Oct 14 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.4-1
- update to 1.19.4

* Wed Sep 06 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.3-1
- update to 1.19.3 release

* Tue Aug 29 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.2-1
- update to 1.19.2 release

* Tue Aug 15 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.1-1
- update to 1.19.1 release

* Wed Aug 09 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.0-4
- remove virtual provides

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.19.0-1
- update to 1.19.0 release

* Tue Mar 14 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.18.0-1
- update to 1.18.0 release

* Fri Mar 10 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.1-1
- update to 1.17.1 release

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 28 2017 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-2
- fix running under gnome-wayland session

* Tue Dec 06 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.17.0-1
- update 1.17.0 release

* Wed Nov 16 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.1-1
- update to 1.16.1 release

* Thu Sep 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.16.0-1
- update to 1.16.0 release

* Wed Jul 27 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.3-1
- update to 1.15.3 release

* Wed Jul 27 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.2-1
- update to 1.15.2 release

* Thu Jun 30 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.1-1
- update to 1.15.1 release

* Thu Jun 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.15.0-1
- update to 1.15.0 release
- switch to gtk+3

* Sat May 21 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14-1-1
- update to 1.14.1 release
- fix for https://bugzilla.redhat.com/show_bug.cgi?id=1303999

* Mon May 09 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-3
- revert fix for rhbz (#1303999), which introduced regressions

* Tue Apr 26 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-2
- fix for rhbz (#1303999)

* Tue Apr 05 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.14.0-1
- update to 1.14.0 release

* Mon Feb 22 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.1-1
- update to 1.13.1 release

* Sun Feb 07 2016 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.13.0-1
- update to 1.13.0 release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Dec 27 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.2-1
- update to 1.12.2 release

* Wed Dec 02 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.1-1
- update to 1.12.1 release
- removed upstreamed patch

* Fri Nov 06 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.12.0-1
- update to 1.12.0 release
- fix regression with dvi documents, https://github.com/mate-desktop/atril/issues/164

* Thu Oct 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.11.0-1
- update to 1.11.0 release
- drop runtime require mate-icon-theme
- add runtime require mathjax for epub

* Mon Aug 31 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.2-1
- update to 1.10.2 release

* Mon Jul 13 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.1-1
- update to 1.10.1 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 05 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.10.0-1
- update to 1.10.0 release

* Sat Apr 04 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.90-1
- update to 1.9.90 release

* Thu Jan 22 2015 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.2-1
- update to 1.9.2 release

* Thu Dec 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.1-1
- update to 1.9.1 release
- remove atril_epub-mimetypes.patch

* Mon Dec 08 2014 Adam Jackson <ajax@redhat.com> 1.9.0-2
- Don't build against t1lib, freetype is sufficient (#852489)

* Sun Oct 26 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.9.0-1
- update to 1.9.0
- Add epub support (part of GSoC 2014).
- Use MateAboutDialog from libmate-desktop
- remove upstreamed patches
- add configure patch

* Sat Oct 11 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-2
- enable thumbnailer support and use a -thumbnailer subpackage for it
- fix rhbz (#1150875)

* Mon Sep 29 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.1-1
- update to 1.8.1 release

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-7
- disable thumbnailer

* Fri Aug 01 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-6
- rebuild to obsolete mate-document-viewer correctly

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 1.8.0-5
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-3
- fix rhbz (#1082143)

* Wed Mar 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.8.0-2
- fix rhbz (#999912)
- use better conditionals for obsoleting mate-document-viewer

* Wed Mar 05 2014 Dan Mashal <dan.mashal@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Wed Feb 19 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.90-1
- update to 1.7.90
- no need of autoreconf anymore

* Mon Feb 10 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.2.1
- update to 1.7.2 release
- add autoreconf to fix building

* Fri Jan 24 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-1
- update to 1.7.1 release
- add gtk-doc dir for release builds

* Wed Jan 22 2014 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.1-0.1.git20140122.26539f8
- update to git snapshot from 2014.01.22

* Wed Dec 18 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.2.git20131120.26539f8
- make Maintainers life easier and use better git snapshot usage, Thanks to Björn Esser
- use modern 'make install' macro
- limit obsoletes/provides

* Sat Dec 14 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.7.0-0.1.git26539f8
- rename to atril
- use 1.7 git snaphot
- fix rpm scriptlets

* Sat Oct 12 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-6
- fix rhbz (#1005519)

* Thu Aug 08 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-5
- rebuild for mate-desktop package split
- add runtime require mate-desktop-libs, fix #974791
- change caja subpackage requires
- remove -libs subpackage requires to main package
- add icon cache scriplets for internal icons
- use autoreconf instead of autogen

* Mon Aug 05 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.6.1-4
- fix deps so main pkg isn't multilib'd
- workaround libtool breakage
- .spec cleanup

* Sat Aug 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-3
- fix obsoleting old -data subpackage

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Aug 02 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.1-1
- update to 1.6.1
- remove -data subpackage
- remove NOCONFIGURE=1 ./autogen.sh line

* Sun Jun 16 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-6
- add require mate-desktop, fix #974791

* Mon May 13 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-5
- remove isa tag from -data subpackage requires

* Sat May 11 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-4
- remove gsettings convert file
- create -data noarch subpackage
- move docs in -data subpackage
- move help dir in -data subpackage
- move locale in -data subpackage

* Fri May 10 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-3
- remove -dvi, -djvu, -xps subpackages and move the libs to -libs subpackage
- add Requires: %%{name}%%{?_isa} = %%{version}-%%{release} to -libs subpackage
- remove sed commands for desktop file
- add hicolor-icon-theme require
- fix last changelog date
- rename atril to mate-document-viewer in summarys and descriptions
- to avoid rpmlint warnings
- rename evince to mate-document-viewer in description
- update description
- fix mixed-use-of-spaces-and-tabs in spec file
- move additional doc files to valid doc dir

* Thu May 09 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-2
- use libmate-keyring-devel as BR instead of mate-keyring-devel
- fix spelling-error in %%description of -devel subpackage
- fix gsettings schema rpm scriptlets

* Wed Apr 03 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.6.0-1
- update to 1.6.0

* Thu Mar 21 2013 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.0-2
- initial build for fedora

* Fri Nov 16 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.5.0-1
- build against official fedora
- update to 1.5.0
- remove scrollkeeper BR
- remove mate-conf schema directory
- remove upstreamed mate-document-viewer_change_ev_api_version.patch
- remove epoch

* Mon Nov 05 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1:1.4.0-0102
- add epoch
- add desktop-file-validate
- remove (noreplace) from schema files

* Sat Oct 06 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-0101
- improve and review spec file
- own include dir
- add mate-document-viewer_change_ev_api_version.patch
- fix license information
- add ChangeLog
- fix description
- fix unused-direct-shlib-dependency
- fix scriplet section

* Mon Aug 27 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-0100
- build for f18

* Tue Jul 17 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-2
- rebuild for f17 and f18

* Tue Jul 17 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.4.0-1
- update to 1.4.0

* Tue Jun 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.1-3
- test build

* Tue Jun 19 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.1-2
- Silence rpm scriptlet output in fc17

* Thu Mar 15 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.1-1
- update to 1.2.1

* Mon Mar 12 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.2.0-1
- update to 1.2.0

* Tue Jan 17 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.1-2
- rebuild for enable builds for .i686

* Tue Jan 17 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.1-1
- updated to 1.1.1 version

* Wed Jan 04 2012 Wolfgang Ulbrich <chat-to-me@raveit.de> - 1.1.0-1
- atril.spec based on evince-2.32.0-4.fc14 spec

## END: Generated by rpmautospec
